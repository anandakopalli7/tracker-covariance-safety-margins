"""Package E probe (revision v13, A10 section 7): one 700-frame closed-loop episode for one E arm, with fix F2.

Copy of probe_arms_v01.py (the probe of the old runs). Changes, and nothing else:
  * the arm comes from e_arms_v01 (E_Z, E_F0, E_N, E_CK3, E_TG, E_PS, E_F0_IMM, E_N_IMM, E_BRAKE) with --g, --triple,
    --brake-from-k; the learned-model and score-history options are removed;
  * every arm runs the F2 servo (installed by e_arms_v01.build_execution);
  * after each detector update the arm's context receives the emitted tracks and the filter events (CK3 and PS read
    the tracker's a-hat from them, as the open-loop extraction did from the logs);
  * the IMM arms (E_F0_IMM, E_N_IMM) replace the CANMOT OnlineTracker by the online IMM (e_imm_v01.OnlineIMM, session B's
    frozen B1 through its step-wise interface); everything else, including detection, is unchanged;
  * the arm's per-decision record goes to e_decisions.jsonl; ARM_METHOD_v01.json holds the E method record;
  * from packet_e_v03 (built on session CD's packet_d1_v13): the scenario-actor class comes from
    scene_actors_d1_v01.scenario_actors_class(case), which is ScenarioActors itself for every case without lead_variant
    (the same one-line change as CD's D1 probe), so E3b's D1 cases run their lead variant.
Sensors, detector, actors, 700-frame loop, contacts, truth and outcome accounting are those of probe_arms_v01.py."""
import argparse,contextlib,hashlib,importlib.util,io,json,math,os,pathlib,queue,sys,time,traceback
import numpy as np
L=pathlib.Path(__file__).resolve().parent;ROOT=L.parent
P=ROOT/'149_supported_sensor_preparation_20261101'
MODEL=ROOT/'410_fixed_kernel_sensor_qualification_20261102/package'
sys.path[:0]=[str(P/'code'),str(P/'sources'),str(P/'vendor'),str(P/'vendor/CANMOT/src'),str(P/'legacy86/vendor/nuscenes-devkit/python-sdk')]
from physical_binding import REFLECT,point_velocity_rh,wheel_geometry,straight_route_steer
sys.path.insert(0,str(ROOT/'747_full_scenario_binding_20261103'))
from scene_actors_v03 import ScenarioActors
from actor_policy_v01 import Draw
sys.path.insert(0,str(ROOT/'716_actuation_capture_integration_20261103'))
sys.path.insert(0,str(L))
import arms_adapter_v02 as arms
import e_arms_v01 as earms
import scene_actors_d1_v01 as lead_variants   # packet_e_v03 (on packet_d1_v13): D1 lead variants for cases with lead_variant (session CD's line)
live=arms.live;ARMS=earms.ARMS
sys.path.insert(0,str(ROOT/'711_native_decision_capture_20261103'))
from ordered_capture_v02 import Store
from assessment_outcomes_v01 import Assessment
from failure_policy_v01 import PolicyFailure,CaptureIntegrityError,policy_call
from policy_capture_v01 import SensorExecution,SIM_DT
sys.path.insert(0,str(ROOT/'732_actual700_sensor_scope_integration_20261103'))
sys.path.insert(0,str(ROOT/'742_sensor_snapshot_initialization_20261103'))
import registered_inventory_v02 as scoped_inventory
import review_registered_v01 as inventory_review
from asset_guard import check_asset
from physics_guard import require_supported_physics
from episode_clock import EpisodeClock
from range_noise import NoiseKey,apply_range_noise
from sensor_adapter import Sweep,SweepBuffer,reference_world,keyed_seed
from online_tracker import OnlineTracker,detector_to_world,planner_actors
from consumer import decode_command
from evaluation_geometry import box_from_record,compare_native_vertices,directional_gap


def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def xyz(v):return np.array([v.x,v.y,v.z],dtype=float)
def ints(x):
    if isinstance(x,dict):return {(int(k) if k.isdigit() else k):ints(v) for k,v in x.items()}
    if isinstance(x,list):return [ints(v) for v in x]
    return x
def control(c):return {key:getattr(c,key) for key in ('throttle','brake','steer','reverse','hand_brake','manual_gear_shift')}


def measure(ego,reference):
    tr=ego.get_transform();T=np.array(tr.get_matrix());rv=xyz(ego.get_velocity());omega=xyz(ego.get_angular_velocity())
    velocity=point_velocity_rh(T,xyz(ego.bounding_box.location),reference['local_reference_point_m'],rv,omega)
    center=T[:3,:3]@xyz(ego.bounding_box.location)+T[:3,3]
    return dict(world=T.tolist(),reported_velocity_lh=rv.tolist(),reported_omega_degrees_lh=omega.tolist(),
                bbox_velocity_rh=velocity.tolist(),speed=float(velocity[0]),center_lh=center.tolist(),
                yaw_degrees_lh=float(tr.rotation.yaw),heading_rh=-math.radians(tr.rotation.yaw))


def run(case_id,out,backup,arm,g,triple,brake_from_k,carla_port):
    # This draft cannot dispatch merely because someone invokes its filename.
    release=arms.require_release(L/'RELEASE_SMOKE_v01.json')
    assert os.environ.get('RUNPOD_POD_ID')==release['pod_id'] and release['pod_id']
    assert case_id in release['authorized_cases'],'Case outside the prospective release'
    assert type(carla_port) is int and 1024<carla_port<65000,'Invalid CARLA port'
    knobs=earms.check_knobs(arm,g,triple,brake_from_k)
    emissions=live.ObservationStream()
    EpisodeBridge,arm_capture_binding=earms.make_capture_class(arm)
    assert release['source_binding_sha256']==sha(L/'RUNTIME_SOURCE_BINDING_SMOKE_v01.json')
    assert release['protocol_sha256']==sha(L/'DEVELOPMENT_PROTOCOL_SMOKE_v01.json')
    for item in read(L/'RUNTIME_SOURCE_BINDING_SMOKE_v01.json')['files']:assert sha(ROOT/item['path'])==item['sha256']
    protocol=read(L/'DEVELOPMENT_PROTOCOL_SMOKE_v01.json')
    require_supported_physics(protocol['physics'])
    case=next(c for c in protocol['cases'] if c['id']==case_id)
    draw=Draw(**case['draw'])
    assert draw.desired_mps==case['desired_mps'] and type(case['reactive']) is bool
    catalogue=read(L/'ASSET_CATALOGUE_v01.json')
    assert catalogue['status']=='MEASURED_DETERMINISTIC_ASSET_SELECTION'
    assert sha(L/'ASSET_CATALOGUE_v01.json')==release['asset_catalogue_sha256']
    import carla
    sys.path.insert(0,str(MODEL/'code'))
    backend_spec=importlib.util.spec_from_file_location('programme_a733_fixed_backend',MODEL/'code/centerpoint_backend.py')
    backend=importlib.util.module_from_spec(backend_spec);backend_spec.loader.exec_module(backend)
    CenterPointBackend=backend.CenterPointBackend
    from tracker_audit import audited,record_history
    from fast_overlap_array import install
    install()
    from canmot.motion_module import kalman_filter
    assert pathlib.Path(kalman_filter.__file__).resolve()==(P/'vendor/CANMOT/src/canmot/motion_module/kalman_filter.py').resolve()
    assert not out.exists() and not backup.exists(),'Existingliveworldcapture cannot resume from files'
    out.mkdir(parents=True,exist_ok=False);backup.mkdir(parents=True,exist_ok=False)
    store=Store(out,backup)
    for name in ('clean','raw'):
        (out/name).mkdir();(backup/name).mkdir()
    def append(name,value):
        raw=(json.dumps(value,allow_nan=False)+'\n').encode()
        for root in (out,backup):
            with (root/name).open('ab') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    def save(name,value):return store.put(name,value)
    def save_array(name,value):
        buffer=io.BytesIO();np.save(buffer,value,allow_pickle=False)
        for root in (out,backup):store.write_one(root/name,buffer.getvalue())
    save('contract.json',dict(case=case,protocol_sha256=release['protocol_sha256'],source_binding_sha256=sha(L/'RUNTIME_SOURCE_BINDING_SMOKE_v01.json')))
    save('RUN_CONTEXT_v01.json',dict(arm=arm,knobs=knobs,tracker=earms.tracker_of(arm),carla_port=carla_port,pod_id=os.environ.get('RUNPOD_POD_ID'),
        release_sha256=sha(L/'RELEASE_SMOKE_v01.json'),local_copies=[str(out),str(backup)],package='E',probe_sha256=sha(pathlib.Path(__file__))))
    lock=read(MODEL/'legacy86/40_remote/input_lock.json')
    model=CenterPointBackend(MODEL/'legacy86/vendor/CenterPoint',MODEL/'legacy86/weights/epoch_20.pth',lock['checkpoint_sha256'])
    reference=read(P/'sources/velocity_reference_audit.json')
    client=carla.Client('127.0.0.1',carla_port);client.set_timeout(60)
    assert client.get_server_version()=='0.9.15'
    created=[];sensors=[];ego=None;world=None;bridge=None;outcome=None;contacts=queue.Queue();messages=queue.Queue()
    try:
        world=client.generate_opendrive_world((P/'sources/controlled_road.xodr').read_text(),carla.OpendriveGenerationParameters(vertex_distance=2.,max_road_length=50.,wall_height=0.,additional_width=.6,smooth_junctions=True,enable_mesh_visibility=True))
        settings=world.get_settings()
        for key,value in protocol['physics'].items():setattr(settings,key,value)
        world.apply_settings(settings);settings=world.get_settings()
        observed_settings={key:getattr(settings,key) for key in protocol['physics']}
        require_supported_physics(observed_settings)
        save('world_settings.json',observed_settings)
        def batch(commands,label):
            before=world.get_snapshot().frame;responses=client.apply_batch_sync(commands,False);after=world.get_snapshot().frame
            append('batch_receipts.jsonl',dict(label=label,before=before,after=after,errors=[r.error for r in responses]))
            assert before==after and len(responses)==len(commands) and not any(r.error for r in responses)
            return dict(before_frame=int(before),after_frame=int(after),commands_submitted=len(commands),errors=[r.error for r in responses])
        def canonical_check(wire,k):
            fields=decode_command(bytes.fromhex(wire));obj=carla.VehicleAckermannControl(**fields)
            actual={key:float(getattr(obj,key)) for key in fields}
            append('canonical_field_receipts.jsonl',dict(k=k,wire=wire,fields=fields,object_fields=actual,native_ackermann_applied=False))
            assert fields==actual
        assets=world.get_blueprint_library();spawn=world.get_map().get_waypoint_xodr(1,-1,200.).transform
        origin=REFLECT@xyz(spawn.location);route_yaw=-math.radians(spawn.rotation.yaw)
        ahead=world.get_map().get_waypoint_xodr(1,-1,210.).transform
        assert abs(ahead.location.x-spawn.location.x-10)<.01 and abs(route_yaw)<1e-5
        spawn.location.y+=protocol['initial_lateral_offset_lh_m'];spawn.location.z+=1.
        bp=assets.find('vehicle.audi.etron');bp.set_attribute('sticky_control','true')
        ego=world.spawn_actor(bp,spawn);created.append(ego)
        batch([carla.command.ApplyVehicleControl(ego.id,carla.VehicleControl(hand_brake=True))],'settle_ego')
        assessment_origin=origin.copy();assessment_origin[0]+=5*case['desired_mps']+float(ego.bounding_box.location.x)
        scene=lead_variants.scenario_actors_class(case)(world,carla,draw,catalogue['selected'],assessment_origin,route_yaw,reference,save,append,created)
        batch(scene.spawn(2*ego.bounding_box.extent.x,spawn.location.z),'settle_scenario_actors')
        target=scene.items[0]['actor']
        collision=world.spawn_actor(assets.find('sensor.other.collision'),carla.Transform(),attach_to=ego);created.append(collision);sensors.append(collision)
        lidar_bp=assets.find('sensor.lidar.ray_cast')
        attributes=dict(channels='32',range='100',points_per_second='680000',rotation_frequency='20',upper_fov='10.67',lower_fov='-30.67',horizontal_fov='360',sensor_tick='0.0',noise_stddev='0',dropoff_general_rate='0',dropoff_intensity_limit='.01',dropoff_zero_intensity='0',atmosphere_attenuation_rate='.004',noise_seed='8608')
        for key,value in attributes.items():lidar_bp.set_attribute(key,value)
        lidar=world.spawn_actor(lidar_bp,carla.Transform(carla.Location(x=1,z=2)),attach_to=ego);created.append(lidar);sensors.append(lidar)
        actual_attributes={key:lidar.attributes[key] for key in attributes}
        save('sensor_attributes.json',dict(requested=attributes,actual=actual_attributes))
        assert all(math.isclose(float(attributes[k]),float(actual_attributes[k]),rel_tol=1e-6,abs_tol=1e-8) for k in attributes)
        for _ in range(protocol['settling_ticks']):world.tick()
        scene.bind_settled()
        save('scenario_settled_observation.json',scene.observe(int(world.get_snapshot().frame)))
        phys=ego.get_physics_control();T=np.asarray(ego.get_transform().get_matrix())
        snapshot=dict(asset=ego.type_id,mass=float(phys.mass),com_nudge_native=xyz(phys.center_of_mass).tolist(),bbox_offset=xyz(ego.bounding_box.location).tolist(),bbox_extent=xyz(ego.bounding_box.extent).tolist(),bbox_rotation_degrees=[float(getattr(ego.bounding_box.rotation,k)) for k in ('yaw','pitch','roll')])
        save('asset_snapshot.json',snapshot);asset=check_asset(snapshot,reference);save('asset_check.json',asset)
        assert asset['status']=='PASS_ASSET_REFERENCE_BINDING'
        geometry=wheel_geometry([xyz(w.position) for w in phys.wheels],T,[w.max_steer_angle for w in phys.wheels])
        save('binding.json',dict(geometry=geometry,geometry_actor_world=T.tolist(),wheel_world_native=[xyz(w.position).tolist() for w in phys.wheels],wheel_max_steer_degrees=[w.max_steer_angle for w in phys.wheels],origin_rh=origin.tolist(),route_yaw_rh=route_yaw,asset_snapshot=snapshot,ego_actor_id=ego.id,target_actor_id=None if target is None else target.id,reference=reference,reference_sha256=sha(P/'sources/velocity_reference_audit.json'),active_intensity_scale=1,legacy_lock_is_historical=True))
        before=measure(ego,reference)
        batch([carla.command.ApplyVehicleControl(ego.id,carla.VehicleControl()),carla.command.ApplyTargetVelocity(ego.id,carla.Vector3D(x=case['desired_mps']))]+scene.release_commands(),'release_and_single_velocity_assignment')
        coast_frame=world.tick();coast=measure(ego,reference);coast_dt=float(world.get_snapshot().timestamp.delta_seconds);save('scenario_coast_observation.json',scene.observe(coast_frame))
        init_frame=world.tick();state=measure(ego,reference);base=world.get_snapshot();save('scenario_initial_observation.json',scene.observe(init_frame))
        assert init_frame==coast_frame+1 and coast_dt==float(base.timestamp.delta_seconds)==SIM_DT
        initial_a=(state['speed']-coast['speed'])/SIM_DT
        save('initialization.json',dict(frame=init_frame,release_before=before,coast_before=coast,coast_frame=coast_frame,coast_dt=coast_dt,measured=state,acceleration=initial_a,dt=SIM_DT,target_velocity_assignment=True,target_velocity_assignments=1,requested_initial_speed=case['desired_mps']))
        def steering(s):
            mat=np.asarray(s['world']);rear=REFLECT@(mat[:3,:3]@np.asarray(geometry['rear_axle_local_m'])+mat[:3,3])
            return straight_route_steer(rear[:2],s['heading_rh'],max(0.,s['speed']),origin[:2],route_yaw,geometry['wheelbase_m'],geometry['max_steer_rad'])
        collision.listen(lambda e:contacts.put(dict(frame=e.frame,other_id=e.other_actor.id,other_type=e.other_actor.type_id,impulse=xyz(e.normal_impulse).tolist())))
        lidar.listen(messages.put)
        clock=EpisodeClock(int(base.frame),float(base.timestamp.elapsed_seconds));buffer=SweepBuffer()
        outcome=Assessment(int(base.frame),case['desired_mps'])
        reference_sensor=np.eye(4);reference_sensor[:3,:3]=[[0,1,0],[-1,0,0],[0,0,1]];reference_sensor[:3,3]=[1,0,2]
        execution,arm_method,ectx=earms.build_execution(arm,case,2*ego.bounding_box.extent.x,2*ego.bounding_box.extent.y,geometry['max_steer_rad'],protocol['frames'],**knobs)
        save('ARM_METHOD_v01.json',arm_method)
        save('ARM_CAPTURE_BINDING_v01.json',arm_capture_binding)
        episode_id='sensor747development:'+case_id+':'+str(world.id)+':'+str(base.frame)
        sensor_handles={'lidar':lidar,'collision':collision}
        sensor_registration=scoped_inventory.register(world,episode_id,ego.id,sensor_handles,save)
        assert sensor_registration['registered_frame']==int(base.frame)
        save('sensor_registration.json',sensor_registration)
        bridge=EpisodeBridge(execution,episode_id,int(base.frame),out/'ordered_capture',backup/'ordered_capture','LIVE_SIX_FAMILY_DEVELOPMENT')
        initial=bridge.start(state['speed'],initial_a,steering(state));save('initial_command.json',initial)
        canonical_check(initial['wire'],-1)
        batch([carla.command.ApplyVehicleControl(ego.id,carla.VehicleControl(**initial['direct_control']))],'initial_client_control')
        scene_commands,scene_start=scene.start(int(base.frame),REFLECT@np.asarray(state['center_lh']),state['bbox_velocity_rh'],math.hypot(ego.bounding_box.extent.x,ego.bounding_box.extent.y),reactive=case['reactive'])
        batch(scene_commands,'initial_scenario_controls')
        def evaluation_record(actor):
            pose=actor.get_transform();bb=actor.bounding_box;local=carla.Transform(bb.location,bb.rotation)
            record=dict(actor_id=actor.id,asset=actor.type_id,actor_world_lh=pose.get_matrix(),bbox_actor_lh=local.get_matrix(),half_extents=xyz(bb.extent).tolist(),native_vertices_lh=[xyz(v).tolist() for v in bb.get_world_vertices(pose)],velocity_lh=xyz(actor.get_velocity()).tolist(),omega_degrees_lh=xyz(actor.get_angular_velocity()).tolist())
            derived=box_from_record(record['actor_world_lh'],record['bbox_actor_lh'],record['half_extents'],route_yaw)
            check=compare_native_vertices(derived,record['native_vertices_lh'])
            record.update(derived=derived,vertex_check=check)
            assert check['minimum_bijective_max_vertex_error_m']<=protocol['additional_integrity']['native_vertex_bijection_atol_m']
            assert check['center_error_m']<=protocol['criteria']['bbox_vertex_mean_check_atol_m']
            return record
        events=[];targets=[];algebra=[];counts=[0,0,0];previous=state['speed']
        fault=None;emergency_expected=None;acquired=0
        route_tangent=np.array([math.cos(route_yaw),math.sin(route_yaw),0.])
        def collect_contacts():
            arrived=[]
            while not contacts.empty():
                event=contacts.get();append('contacts.jsonl',event)
                outcome.contact(int(event['frame']),event);arrived.append(event)
            return arrived
        def emergency_brake(actual,frame):
            c=carla.VehicleControl(throttle=0.,brake=1.,steer=float(actual['steer']),reverse=False,hand_brake=False,manual_gear_shift=False)
            expected=control(c)
            receipt=batch([carla.command.ApplyVehicleControl(ego.id,c)],f'policy_failure_brake_{frame}')
            append('emergency_controls.jsonl',dict(frame=frame,control=expected,receipt=receipt))
            return expected
        def flush_e():
            for item in ectx.pending_records():append('e_decisions.jsonl',item)
        imm=earms.tracker_of(arm)=='IMM'
        audit_hooks=contextlib.ExitStack()
        if not imm:
            # CANMOT arms: the recording hooks of record. The IMM arms leave CANMOT's classes unpatched (session B's library
            # dispatches its own filters) and log B's own recorder instead (imm_filter_events/algebra/modes.jsonl).
            audit_hooks.enter_context(record_history(events,targets));audit_hooks.enter_context(audited(algebra))
        with audit_hooks:
            if imm:
                import e_imm_v01
                tracker=e_imm_v01.OnlineIMM();save('E_IMM_TRACKER_v01.json',tracker.describe())
            else:tracker=OnlineTracker(ints(read(P/'contracts/tracker_config.json')))
            for k in range(protocol['frames']):
                fid=world.tick();msg=messages.get(timeout=15);snap=world.get_snapshot()
                now,clock_receipt=clock.observe(k,int(msg.frame),int(snap.frame),float(msg.timestamp),float(snap.timestamp.delta_seconds))
                assert fid==msg.frame
                state=measure(ego,reference);acceleration=(state['speed']-previous)/SIM_DT;previous=state['speed'];actual=control(ego.get_control())
                center=REFLECT@np.asarray(state['center_lh'])
                outcome.observe(int(fid),float((center-origin)@route_tangent));acquired=k+1
                raw=dict(k=k,frame=fid,time=now,clock=clock_receipt,state=state,acceleration=acceleration,
                    applied_interval_control=actual,active_before_wire=None if fault is not None else execution.wire.hex(),
                    last_native_wire_for_diagnostics=execution.wire.hex(),sensor_world=msg.transform.get_matrix(),
                    policy_failure_latched=fault is not None)
                append('raw_observations.jsonl',raw)
                if emergency_expected is not None and actual!=emergency_expected:
                    raise CaptureIntegrityError('Submitted emergency control differs from applied physical interval control')
                clean=np.frombuffer(msg.raw_data,dtype=np.float32).reshape(-1,4).copy()
                assert len(clean)<=34016 and np.all(clean[:,3]>.01)
                episode=case['noise_episode']
                noisy,receipt=apply_range_noise(clean,NoiseKey('driving_binding92',case['seed'],episode,'lidar',k))
                save_array(pathlib.Path('clean')/f'{k:04d}.npy',clean);save_array(pathlib.Path('raw')/f'{k:04d}.npy',noisy);append('noise_receipts.jsonl',receipt)
                arrived=collect_contacts()
                def read_truth():
                    inventory=scoped_inventory.collect(world,int(fid),episode_id,ego.id,carla,sensor_registration,sensor_handles)
                    inventory_hash=save(f'inventory/frame_{k:04d}.json',inventory)
                    if inventory_review.review(inventory,sensor_registration)['status']!=inventory_review.READY:
                        raise CaptureIntegrityError('Actual sensor/actor inventory invalid; preserve raw evidence')
                    truth=dict(k=k,frame=fid,time=now,ego=evaluation_record(ego),target=evaluation_record(target),
                        scenario_actors=[evaluation_record(i['actor']) for i in scene.items],inventory_sha256=inventory_hash)
                    truth['directional_gap_m']=directional_gap(truth['ego']['derived'],truth['target']['derived'])
                    append('evaluation_truth.jsonl',truth);return truth
                if outcome.contacts:
                    truth=read_truth();save('scenario_terminal_measurement.json',scene.observe(int(fid)))
                    append('frames.jsonl',dict(**raw,execution=None,disposition='CONTACT_TERMINAL_NO_NEW_EGO_DECISION',
                        raw_sha256=hashlib.sha256(noisy.tobytes()).hexdigest(),contacts=arrived))
                    break
                interval=None;truth_commit=None;truth=None
                if fault is None:
                    try:
                        T=np.asarray(state['world']);buffer.push(Sweep(fid,float(now),noisy,np.asarray(raw['sensor_world'])))
                        if k>=19 and k%10==9:
                            sensor_reference=reference_world(T,reference_sensor)
                            cloud=buffer.combined(sensor_reference,1,keyed_seed('integration',case['seed'],'lidar','driving_binding92:'+str(k)))
                            prediction=policy_call('detector',model.predict,cloud,'binding_'+str(k))
                            model_rows=policy_call('detector_world_conversion',detector_to_world,prediction,sensor_reference)
                            tracks=policy_call('tracker',tracker.step,model_rows,now)
                            policy_call('emission_metadata',emissions.update,k,int(fid),now,tracks)
                            append('detections.jsonl',dict(k=k,frame=fid,time=now,model=model_rows,tracks=tracks,
                                combined_hash=hashlib.sha256(cloud.tobytes()).hexdigest(),inference_s=prediction['inference_s']))
                            for i,(name,items) in enumerate([('filter_events.jsonl',events),('filter_target_covariances.jsonl',targets),('filter_algebra.jsonl',algebra)]):
                                for item in items[counts[i]:]:append(name,item)
                                counts[i]=len(items)
                            if imm:
                                for name,items in zip(('imm_filter_events.jsonl','imm_filter_algebra.jsonl','imm_modes.jsonl'),tracker.new_records()):
                                    for item in items:append(name,item)
                            policy_call('e_track_history',ectx.on_detector,tracks,events)
                        actors=policy_call('tracker_export',emissions.actors,k,now,center,route_yaw)
                        desired_steer=policy_call('ego_steering',steering,state)
                        def actuate(command,frame,index):
                            assert frame==fid and index==k
                            if k%2==1:canonical_check(execution.wire.hex(),k)
                            return batch([carla.command.ApplyVehicleControl(ego.id,carla.VehicleControl(**command['control']))],f'client_{k}')
                        observed=bridge.observe(dict(k=k,frame=int(fid),time=now,speed=state['speed'],acceleration=acceleration,
                            steer=desired_steer,applied_control=actual,raw_observation=raw),actors,read_truth,actuate)
                        interval=observed['interval'];truth_commit=observed['truth_commit_sha256'];flush_e()
                    except PolicyFailure as exc:
                        flush_e()
                        fault=dict(frame=int(fid),k=k,**exc.record());outcome.policy_failure(int(fid),str(exc))
                        save('policy_failure.json',dict(**fault,traceback=traceback.format_exc(),automatic_policy_retry=False))
                        emergency_expected=emergency_brake(actual,int(fid))
                        truth=read_truth()
                else:
                    # The failed policy is not re-entered. Raw LiDAR, actual physical
                    # state and contacts continue under the recorded emergency action.
                    truth=read_truth()
                if k<protocol['frames']-1:
                    scene_commands,scene_record=scene.step(int(fid),center,state['bbox_velocity_rh'],
                        math.hypot(ego.bounding_box.extent.x,ego.bounding_box.extent.y))
                    batch(scene_commands,f'scenario_{k}')
                else:save('scenario_terminal_measurement.json',scene.observe(int(fid)))
                append('frames.jsonl',dict(**raw,execution=interval,raw_sha256=hashlib.sha256(noisy.tobytes()).hexdigest(),
                    truth_commit_sha256=truth_commit,disposition='POLICY_FAILURE_EMERGENCY_OBSERVATION' if fault else 'NATIVE_EGO_POLICY',
                    policy_failure=fault))
                collect_contacts()
                if outcome.contacts:break
                if k%20==19:print(json.dumps(dict(case=case_id,k=k,speed=state['speed'],detector_updates=tracker.index,policy_failure=fault is not None)),flush=True)
        # Close and retain callbacks at a fixed world frame. This lifecycle evidence
        # still requires the independently qualified contact instrument.
        tail_frame=int(world.get_snapshot().frame)
        if tail_frame!=int(base.frame)+acquired:raise CaptureIntegrityError('Unexpected frame before callback closure')
        listener=collision.is_listening;before_stop=listener() if callable(listener) else listener
        if type(before_stop) is not bool or not before_stop:raise CaptureIntegrityError('Collision listener was not active')
        time.sleep(.5);collect_contacts();collision.stop();time.sleep(.5);collect_contacts()
        listener=collision.is_listening;after_stop=listener() if callable(listener) else listener
        if type(after_stop) is not bool or after_stop:raise CaptureIntegrityError('Collision listener did not stop')
        lidar.stop()
        if not messages.empty():raise CaptureIntegrityError('Unexpected unread LiDAR callbacks after the physical loop')
        tail_end_frame=int(world.get_snapshot().frame)
        if tail_end_frame!=tail_frame:raise CaptureIntegrityError('World advanced during callback closure')
        save('contact_listener_closure.json',dict(before_stop=before_stop,after_stop=after_stop,frame=tail_frame,tail_end_frame=tail_end_frame,
            world_not_advanced_during_tail=True,perfect_delivery_claim=False))
        result=outcome.summarize(callback_collection_closed=True);outcome_hash=save('assessment_outcomes.json',result)
        if outcome.contacts:
            capture=bridge.finish_terminal('PHYSICAL_CONTACT',acquired,outcome_hash)
        elif fault is not None:
            capture=bridge.finish_terminal('POLICY_FAILURE_WITH_CONTINUED_OBSERVATION',acquired,outcome_hash)
        else:capture=bridge.finish()
        save('ordered_capture_receipt.json',capture)
        save('acquisition_complete.json',dict(status='DEVELOPMENT_OBSERVATION_PENDING_INDEPENDENT_AUDITS',
            frames=acquired,planned_frames=protocol['frames'],detector_updates=tracker.index,outcome_sha256=outcome_hash,
            first_contact_frame=result['first_contact_frame'],first_policy_failure_frame=result['first_policy_failure_frame'],
            observed_point_estimate_available=result['observed_point_estimate_available'],actual_research_episodes=0,publication_go=False))
    except Exception as exc:
        if outcome is not None:
            outcome.instrument_failure(type(exc).__name__+': '+str(exc))
            save('incomplete_assessment_outcomes.json',outcome.summarize(callback_collection_closed=False))
        save('exception.json',dict(type=type(exc).__name__,error=str(exc),traceback=traceback.format_exc()))
        if ego is not None and world is not None:
            try:batch([carla.command.ApplyVehicleControl(ego.id,carla.VehicleControl(brake=1.))],'failure_emergency_brake_no_tick')
            except Exception as emergency:save('emergency_exception.json',dict(error=str(emergency)))
        raise
    finally:
        if bridge is not None:bridge.close()
        for sensor in sensors:
            with contextlib.suppress(Exception):sensor.stop()
        for actor in reversed(created):
            with contextlib.suppress(Exception):actor.destroy()


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--case',required=True);ap.add_argument('--out',type=pathlib.Path,required=True)
    ap.add_argument('--backup',type=pathlib.Path,default=None,help='second LOCAL copy; default <out>.local_copy (the unchanged reviews compare both copies)')
    ap.add_argument('--arm',choices=ARMS,required=True)
    ap.add_argument('--g',type=float,default=None)
    ap.add_argument('--triple',default=None,help='E_PS: g_before,g_braking,g_stopped (grid values)')
    ap.add_argument('--brake-from-k',type=int,default=None,help='E_BRAKE: first forced-fallback decision tick (default 199)')
    ap.add_argument('--carla-port',type=int,default=2000)
    args=ap.parse_args();backup=args.backup if args.backup is not None else args.out.with_name(args.out.name+'.local_copy')
    triple=None if args.triple is None else [float(x) for x in args.triple.split(',')]
    run(args.case,args.out,backup,args.arm,args.g,triple,args.brake_from_k,args.carla_port)
