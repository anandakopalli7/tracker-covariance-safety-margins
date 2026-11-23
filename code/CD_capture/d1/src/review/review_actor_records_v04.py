"""CPU-only replay of recorded scenario actors; no CARLA server or world ticks.

Exact command/measurement accounting is separate from physical competence.
Observed motion statistics are descriptive, with no new success threshold.
"""
import argparse,datetime,json,math,os,pathlib,sys,traceback
import numpy as np


def run(workspace,folder,backup,review_code):
    sys.path.insert(0,str(review_code))
    from review_perception_prefix_v01 import Inputs,sha
    from review_native_prefix_v01 import strip_wall
    from prefix_contract_v01 import need
    root=workspace.resolve();p=root/'149_supported_sensor_preparation_20261101'
    sys.path[:0]=[str(root/'746_actual_actor_policy_development_20261103'),str(root/'737_native_actor_controller_candidate_20261103'),str(p/'code'),str(p/'sources'),str(p/'vendor')]
    from actor_policy_v01 import Draw,ActorRequests
    from actor_pid_v01 import ActorPID
    from physical_binding import REFLECT,point_velocity_rh,wheel_geometry
    from execution_core import SIM_DT
    from asset_guard import check_asset
    import carla
    data=Inputs(folder,backup);contract=data.json('contract.json');case=contract['case']
    full=root/'claude_smoke_v01'
    protocol=json.loads((full/'DEVELOPMENT_PROTOCOL_SMOKE_v01.json').read_text())
    need(case in protocol['cases'] and contract['protocol_sha256']==sha(full/'DEVELOPMENT_PROTOCOL_SMOKE_v01.json'),'Case/protocol differs')
    sources=json.loads((full/'RUNTIME_SOURCE_BINDING_SMOKE_v01.json').read_text())['files']
    need(contract['source_binding_sha256']==sha(full/'RUNTIME_SOURCE_BINDING_SMOKE_v01.json'),'Source binding differs')
    for item in sources:need(sha(root/item['path'])==item['sha256'],'Source differs: '+item['path'])
    need(not (folder/'exception.json').exists(),'Incomplete acquisition needs separate treatment')
    spawn=data.json('scenario_draw_and_spawn.json');binding=data.json('binding.json');initial=data.json('initialization.json')
    need(spawn['draw']==case['draw'] and spawn['route_yaw_rh']==binding['route_yaw_rh'],'Scenario definition differs')
    draw=Draw(**case['draw']);base=initial['frame'];yaw=spawn['route_yaw_rh'];origin=np.asarray(spawn['assessment_origin_rh'])
    c,s=math.cos(yaw),math.sin(yaw);R=np.array([[c,-s,0.],[s,c,0.],[0.,0.,1.]]);to_route=R.T
    reference=json.loads((p/'sources/velocity_reference_audit.json').read_text())
    need(binding['reference']==reference and binding['reference_sha256']==sha(p/'sources/velocity_reference_audit.json'),'Reference differs')
    declared=spawn['actors'];need(declared and len({x['actor_id'] for x in declared})==len(declared),'Duplicate or missing actor')
    need(declared[0]['role']=='primary' and binding['target_actor_id']==declared[0]['actor_id'],'Primary actor differs')
    by_id={a['actor_id']:a for a in declared};geometry={}
    for actor in declared:
        actual=actor['actual']
        entry=actor['entry'];receipt=data.json('scenario_'+actor['role']+'_catalogue_check.json')
        need(receipt['actual']==actual and receipt['catalogue']==entry and receipt['actor_id']==actor['actor_id'] and receipt['role']==actor['role'],'Raw catalogue receipt differs')
        # Independent checks use the existing contract, not the writer function.
        from asset_guard import GEOMETRY_ATOL_M
        need(actual['asset']==entry['asset'],'Spawned asset identity differs')
        differences={}
        for field in ('bbox_offset','bbox_extent'):
            a,b=actual[field],entry[field]
            need(len(a)==len(b)==3 and all(math.isfinite(x) for x in a+b),'Invalid geometry')
            differences[field]=[a[i]-b[i] for i in range(3)]
            need(all(abs(x)<=GEOMETRY_ATOL_M for x in differences[field]),'Geometry exceeds existing contract')
            if field=='bbox_extent':need(all(x>0 for x in a+b),'Nonpositive dimensions')
        for item in (actual,entry):need(len(item['bbox_rotation_degrees'])==3 and all(math.isfinite(x) and abs(x)<=1e-5 for x in item['bbox_rotation_degrees']),'Non-axis-aligned catalogue geometry')
        need(receipt['check']==dict(status='PASS_CATALOGUE_GEOMETRY',failures=[],actual_minus_catalogue=differences,geometry_absolute_tolerance_m=GEOMETRY_ATOL_M,axis_aligned_rotation_atol_degrees=1e-5,provenance='Existing phase92/149 asset geometry and axis-alignment contract',controller_performance_thresholds_changed=False,measured_geometry_modified=False),'Catalogue check receipt differs')
        physics=folder/('scenario_'+actor['role']+'_physics.json')
        if physics.exists():
            value=data.json(physics.name)
            need(value['checked']==check_asset(value['actual'],reference) and value['checked']['status']=='PASS_ASSET_REFERENCE_BINDING','Actor reference physics differs')
            g=wheel_geometry(value['wheel_positions_native'],value['actor_world_lh'],[w for w in binding['wheel_max_steer_degrees']])
            # Each current qualified vehicle is the same fixed etron asset. Its
            # own declared geometry is used below; wheel steer limits are checked
            # through the immutable qualified asset/source contract.
            need(g==value['geometry'],'Actor wheel geometry differs')
            geometry[actor['actor_id']]=g
    release=data.json('scenario_release.json')
    expected_assignments=[a['actor_id'] for a in declared if a['actual']['asset'].startswith('vehicle.') and np.linalg.norm(a['initial_velocity_route_rh'])>0]
    need(release['initial_velocity_assignments']==expected_assignments and release['walker_uses_control_not_velocity_assignment'] is True and release['frame']==base-2,'Initial actor release differs')
    frames=data.lines('frames.jsonl');truths=data.lines('evaluation_truth.jsonl');observations=data.lines('raw_observations.jsonl')
    need(len(frames)==len(truths)==len(observations),'Physical record counts differ')
    truth_by_frame={t['frame']:t for t in truths};ego_by_frame={base:initial['measured']}
    for row in observations:ego_by_frame[row['frame']]=row['state']
    rows=data.lines('scenario_frames.jsonl')
    seeds=[data.json('scenario_'+name+'_observation.json') for name in ('settled','coast','initial')]
    for measurements,frame in zip(seeds,(base-2,base-1,base)):
        need([m['actor_id'] for m in measurements]==[a['actor_id'] for a in declared] and all(m['frame']==frame for m in measurements),'Prepolicy actor identity or frame differs')
    need(rows[0]['measured']==seeds[2],'Initial policy observation differs from saved physical initialization')
    expected_frames=[base]+[r['frame'] for r in frames if r['k']<699 and r['disposition']!='CONTACT_TERMINAL_NO_NEW_EGO_DECISION']
    need([r['frame'] for r in rows]==expected_frames,'Scenario request chronology differs')
    commands=data.lines('batch_receipts.jsonl')
    selected=[r for r in commands if r['label']=='initial_scenario_controls' or r['label'].startswith('scenario_')]
    expected_labels=['initial_scenario_controls']+['scenario_'+str(f-base-1) for f in expected_frames[1:]]
    need([r['label'] for r in selected]==expected_labels,'Scenario command sequence differs')
    for row,frame in zip(selected,expected_frames):need(row['before']==row['after']==frame and row['errors']==['']*len(declared),'Scenario command rejected or advanced world')
    sys.path.insert(0,str(full));import actor_policy_d1_v01 as lead_variants   # revision v13 D1
    policy=lead_variants.make_requests(case,draw,base);pid=None;previous={};previous_primary=None;initial_fd_unreconstructed=[];metrics=[]
    ego_half=math.hypot(*binding['asset_snapshot']['bbox_extent'][:2])
    def fields(control):return {k:getattr(control,k) for k in ('throttle','brake','steer','reverse','hand_brake','manual_gear_shift')}
    def measure(record,frame):
        need(record['actor_id'] in by_id and record['frame']==frame,'Actor observation identity differs')
        a=by_id[record['actor_id']];actual=a['actual'];T=np.asarray(record['world_lh']);offset=np.asarray(actual['bbox_offset']);extent=np.asarray(actual['bbox_extent'])
        need(record['role']==a['role'] and record['asset']==actual['asset'] and record['bbox_extent']==extent.tolist(),'Actor dimensions/role differ')
        need(T.shape==(4,4) and np.isfinite(T).all(),'Actor transform invalid')
        centre=REFLECT@(T[:3,:3]@offset+T[:3,3]);need(record['center_rh']==centre.tolist() and record['center_route_rh']==(to_route@(centre-origin)).tolist(),'Actor centre differs')
        need(record['body_forward_lh']==T[:3,0].tolist() and record['half_diagonal_m']==float(np.linalg.norm(extent[:2])),'Actor orientation/support differs')
        old=previous.get(a['actor_id']);fd=None if old is None else (centre-np.asarray(old['center_rh']))/SIM_DT
        if old is not None:need(record['center_finite_difference_rh']==fd.tolist(),'Actor measured finite difference differs')
        elif record['center_finite_difference_rh'] is not None:initial_fd_unreconstructed.append(a['actor_id'])
        if a['actor_id'] in geometry:
            rear_local=np.asarray(geometry[a['actor_id']]['rear_axle_local_m']);rear=REFLECT@(T[:3,:3]@rear_local+T[:3,3])
            v=point_velocity_rh(T,offset,reference['local_reference_point_m'],record['reported_velocity_lh'],record['reported_omega_degrees_lh'])
            rv=point_velocity_rh(T,rear_local,reference['local_reference_point_m'],record['reported_velocity_lh'],record['reported_omega_degrees_lh'])
            need(record['velocity_basis']=='EMPIRICALLY_QUALIFIED_RIGID_POINT_TRANSPORT','Actor velocity basis differs')
        else:
            rear=centre;v=None if record['center_finite_difference_rh'] is None else (np.asarray(record['center_finite_difference_rh']) if fd is None else fd);rv=v
            need(record['velocity_basis']=='BACKWARD_CENTRE_DISPLACEMENT_OVER_ONE_PHYSICAL_STEP','Actor finite-difference basis differs')
        need(record['rear_rh']==rear.tolist() and record['rear_route_rh']==(to_route@(rear-origin)).tolist(),'Actor rear position differs')
        need(record['center_velocity_route_rh']==(None if v is None else (to_route@v).tolist()) and record['rear_velocity_rh']==(None if rv is None else rv.tolist()) and record['rear_velocity_route_rh']==(None if rv is None else (to_route@rv).tolist()),'Actor point velocity differs')
        if frame in truth_by_frame:
            truth=next(t for t in truth_by_frame[frame]['scenario_actors'] if t['actor_id']==a['actor_id'])
            need(truth['actor_world_lh']==record['world_lh'] and truth['velocity_lh']==record['reported_velocity_lh'] and truth['omega_degrees_lh']==record['reported_omega_degrees_lh'],'Actor request and evaluation observations differ')
        previous[a['actor_id']]=record
    def pid_observation(m):
        return dict(rear_position_lh=(REFLECT@np.asarray(m['rear_rh'])).tolist(),rear_velocity_lh=(REFLECT@np.asarray(m['rear_velocity_rh'])).tolist(),body_forward_lh=m['body_forward_lh'],applied_steer=m['applied']['steer'])
    for measurements,frame in zip(seeds[:2],(base-2,base-1)):
        for record in measurements:measure(record,frame)
    need(not initial_fd_unreconstructed,'A prepolicy finite-difference value lacked its predecessor')
    walker_roundtrips=[]
    def expected_applied(submitted,asset,frame):
        if not asset.startswith('walker.'):return submitted
        # CARLA 0.9.15 rpc/WalkerControl.h, forward and reverse conversion.
        # Intermediate float32 rounding is part of the actual simulator interface.
        cm=np.float32(np.float32(100.)*np.float32(submitted['speed']))
        speed=float(np.float32(np.float32(.01)*cm))
        expected=dict(submitted,speed=speed)
        walker_roundtrips.append(dict(frame=frame,submitted_speed=submitted['speed'],expected_speed=speed))
        return expected
    for row in rows:
        frame=row['frame'];measurements=row['measured']
        need([m['actor_id'] for m in measurements]==[a['actor_id'] for a in declared],'Actor observation order differs')
        for m in measurements:measure(m,frame)
        m=measurements[0];ego=ego_by_frame[frame]
        if previous_primary is not None:need(m['applied']==expected_applied(previous_primary,m['asset'],frame),'Submitted/applied primary actor control differs after exact native unit conversion')
        for hold in measurements[1:]:need(hold['applied']==fields(carla.VehicleControl(throttle=0.,brake=1.,hand_brake=False)),'Static occluder hold differs')
        ego_c=to_route@(REFLECT@np.asarray(ego['center_lh'])-origin);ego_v=to_route@np.asarray(ego['bbox_velocity_rh'])
        request=policy.step(frame,actor_center=m['center_route_rh'][:2],actor_velocity=m['center_velocity_route_rh'][:2],rear_position=m['rear_route_rh'][:2],rear_velocity=m['rear_velocity_route_rh'][:2],ego_center=ego_c[:2],ego_velocity=ego_v[:2],actor_half_diagonal=m['half_diagonal_m'],ego_half_diagonal=ego_half)
        need(strip_wall(request)==row['request'] and strip_wall(policy.snapshot())==row['request_state'],'Actor request or history differs')
        if m['asset'].startswith('walker.'):
            direction=REFLECT@R@np.array([*request['walker_direction_route_rh'],0.])
            control=carla.WalkerControl(direction=carla.Vector3D(*direction.tolist()),speed=request['requested_speed_mps'],jump=False)
            submitted=dict(speed=float(control.speed),direction=[control.direction.x,control.direction.y,control.direction.z],jump=bool(control.jump))
            need(row['native_pid'] is None and row['pid_state'] is None,'Invented walker PID')
        else:
            if pid is None:pid=ActorPID(pid_observation(m),base)
            aim=origin+R@np.array([*request['target_rear_route_rh'],0.]);aim[2]=m['rear_rh'][2]
            control,detail=pid.step(frame,pid_observation(m),target_rear_lh=(REFLECT@aim).tolist(),target_speed_mps=request['requested_speed_mps'])
            need(strip_wall(detail)==row['native_pid'] and strip_wall(pid.snapshot())==row['pid_state'],'Native PID/history differs')
            submitted=fields(control)
        need(submitted==row['submitted_primary_control'],'Submitted actor command differs');previous_primary=submitted
        metrics.append(dict(frame=frame,center=m['center_route_rh'],velocity=m['center_velocity_route_rh'],speed=float(np.linalg.norm(m['center_velocity_route_rh'][:2])),requested_speed=request['requested_speed_mps'],reason=request['reason']))
    last=frames[-1]
    terminal_expected=last['k']==699 or last['disposition']=='CONTACT_TERMINAL_NO_NEW_EGO_DECISION'
    terminal_path=folder/'scenario_terminal_measurement.json'
    need(terminal_path.exists()==terminal_expected,'Actor terminal measurement presence differs')
    if terminal_expected:
        terminal=data.json(terminal_path.name)
        need([m['actor_id'] for m in terminal]==[a['actor_id'] for a in declared],'Terminal actor order differs')
        for m in terminal:measure(m,last['frame'])
        need(terminal[0]['applied']==expected_applied(previous_primary,terminal[0]['asset'],last['frame']),'Terminal primary control differs after exact native unit conversion')
    outcomes=data.json('assessment_outcomes.json')
    stop=min([base+701]+[f for f in (outcomes['first_contact_frame'],outcomes['first_policy_failure_frame']) if f is not None])
    assessed=[r for r in metrics if base+100<=r['frame']<stop]
    summary=dict(samples=len(assessed),window='Assessment requests before first physical contact or ego-policy failure; descriptive, not independent replicates.')
    if assessed:
        speed=np.array([r['speed'] for r in assessed]);request=np.array([r['requested_speed'] for r in assessed]);xy=np.array([r['center'][:2] for r in assessed])
        summary.update(speed_min=float(speed.min()),speed_max=float(speed.max()),speed_mean=float(speed.mean()),
            speed_vs_current_request_rmse=float(np.sqrt(np.mean((speed-request)**2))),
            lateral_min=float(xy[:,1].min()),lateral_max=float(xy[:,1].max()),first_center=xy[0].tolist(),last_center=xy[-1].tolist(),
            reasons={reason:sum(r['reason']==reason for r in assessed) for reason in sorted({r['reason'] for r in assessed})})
        if len(speed)>1:summary.update(speed_difference_acceleration_min=float(np.diff(speed).min()/SIM_DT),speed_difference_acceleration_max=float(np.diff(speed).max()/SIM_DT))
    data.finish()
    for item in sources:need(sha(root/item['path'])==item['sha256'],'Source changed during replay')
    return dict(status='PASS_RECORDED_ACTOR_REQUEST_AND_PID_REPLAY',case=case['id'],request_frames=len(rows),physical_measurement_frames=len(rows)+int(terminal_expected),
        actual_native_carla_value_types=True,walker_unit_conversion='CARLA_0.9.15_FLOAT32_100_THEN_0.01',walker_exact_roundtrip_checks=walker_roundtrips,prepolicy_seed_measurements_reconstructed=True,all_policy_input_finite_differences_reconstructed=not initial_fd_unreconstructed,first_saved_finite_difference_prior_position_not_recorded=initial_fd_unreconstructed,
        subsequent_finite_differences_reconstructed=True,summary=summary,input_hashes=data.hashes,
        actor_competence_proved=False,new_acceptance_thresholds_introduced=False,full_scenario_go=False,paper_go=False)


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for name in ('workspace','folder','backup','review-code','out','out-backup'):ap.add_argument('--'+name,type=pathlib.Path,required=True)
    args=ap.parse_args()
    assert args.out.resolve()!=args.out_backup.resolve() and not args.out.exists() and not args.out_backup.exists()
    for out in (args.out,args.out_backup):assert not out.resolve().is_relative_to(args.folder.resolve()) and not out.resolve().is_relative_to(args.backup.resolve())
    try:value=run(args.workspace,args.folder,args.backup,args.review_code);rc=0
    except Exception as exc:value=dict(status='FAILED_ACTOR_RECORD_REPLAY',error=type(exc).__name__+': '+str(exc),traceback=traceback.format_exc(),paper_go=False);rc=2
    value['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    for out in (args.out,args.out_backup):
        out.parent.mkdir(parents=True,exist_ok=True)
        with out.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert out.read_bytes()==raw
    print(json.dumps({k:value[k] for k in ('status','case','error') if k in value}));raise SystemExit(rc)
