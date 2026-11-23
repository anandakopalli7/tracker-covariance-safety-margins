"""Read-only replay of full747 sensor prefixes, including policy/contact endings.

Outputs are written to separate review directories. No input is rewritten, no
simulator is started, and no failed policy call is treated as a successful call.
"""
import argparse, datetime, hashlib, importlib.util, json, os, pathlib, sys, traceback
from prefix_contract_v01 import derive, need


def sha(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open('rb') as f:
        for block in iter(lambda:f.read(8*1024**2),b''):h.update(block)
    return h.hexdigest()


class Inputs:
    def __init__(self,folder,backup):
        self.folder=folder;self.backup=backup;self.hashes={}
    def data(self,name):
        rel=pathlib.PurePosixPath(name)
        need(not rel.is_absolute() and '..' not in rel.parts,'Unsafe evidence path')
        a=self.folder/rel;b=self.backup/rel
        need(a.is_file() and b.is_file() and not a.is_symlink() and not b.is_symlink(),'Missing dual evidence: '+name)
        raw=a.read_bytes();h=hashlib.sha256(raw).hexdigest()
        need(h==sha(b),'Dual evidence differs: '+name)
        need(name not in self.hashes or self.hashes[name]==h,'Input changed during review: '+name)
        self.hashes[name]=h
        return raw
    def json(self,name):return json.loads(self.data(name))
    def lines(self,name,optional=False):
        if optional and not (self.folder/name).exists():
            need(not (self.backup/name).exists(),'Only one optional trace exists')
            self.hashes[name]=None
            return []
        return [json.loads(x) for x in self.data(name).splitlines()]
    def finish(self):
        for name,h in self.hashes.items():
            for root in (self.folder,self.backup):
                if h is None:need(not (root/name).exists(),'Absent input appeared during review')
                else:need(sha(root/name)==h,'Input changed during review: '+name)


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def run(args):
    import io
    import numpy as np
    root=args.workspace.resolve();folder=args.folder.resolve();backup=args.backup.resolve()
    need(folder!=backup and folder.is_dir() and backup.is_dir(),'Independent stored copies required')
    need(not (folder/'exception.json').exists() and not (backup/'exception.json').exists(),'Incomplete acquisition retained; use separate failure review')
    source=root/'733_full700_registered_sensor_preparation_20261103/replay_perception700_v01.py'
    replay=load('a769_saved_perception_replay',source)
    from canmot.motion_module import kalman_filter
    need(pathlib.Path(kalman_filter.__file__).resolve()==(replay.P/'vendor/CANMOT/src/canmot/motion_module/kalman_filter.py').resolve(),'Tracker source path differs')
    from range_noise import NoiseKey,apply_range_noise
    from episode_clock import EpisodeClock
    evidence=Inputs(folder,backup)
    contract=evidence.json('contract.json');case=contract['case']
    protocol_path=root/'claude_smoke_v01/DEVELOPMENT_PROTOCOL_SMOKE_v01.json'
    protocol=json.loads(protocol_path.read_text())
    need(contract['protocol_sha256']==sha(protocol_path) and case in protocol['cases'],'Full747 case/protocol binding differs')
    source_path=root/'claude_smoke_v01/RUNTIME_SOURCE_BINDING_SMOKE_v01.json'
    need(contract['source_binding_sha256']==sha(source_path),'Acquisition source binding differs')
    source_hashes={}
    for item in json.loads(source_path.read_text())['files']:
        need(sha(root/item['path'])==item['sha256'],'Acquisition source changed: '+item['path'])
        source_hashes[item['path']]=item['sha256']
    init=evidence.json('initialization.json');complete=evidence.json('acquisition_complete.json')
    frames=evidence.lines('frames.jsonl');raw=evidence.lines('raw_observations.jsonl')
    detections=evidence.lines('detections.jsonl',optional=True);noise=evidence.lines('noise_receipts.jsonl')
    if (folder/'policy_failure.json').exists():failure=evidence.json('policy_failure.json')
    else:
        need(not (backup/'policy_failure.json').exists(),'Unpaired failure record')
        evidence.hashes['policy_failure.json']=None;failure=None
    prefix=derive(frames,detections,failure,complete,init['frame'])
    need(len(raw)==len(noise)==len(frames),'Raw physical/noise prefix differs')
    clock=EpisodeClock(raw[0]['clock']['base_carla_frame'],raw[0]['clock']['base_carla_time'])
    need(clock.base_frame==init['frame'],'Initial frame differs')
    backend=None
    if args.detector:
        need(os.environ.get('RUNPOD_POD_ID')==args.expected_pod==json.loads((root/'claude_smoke_v01/RELEASE_SMOKE_v01.json').read_bytes())['pod_id'],'Same source-bound acquisition host required')
        import torch
        need(torch.cuda.is_initialized(),'CUDA wrapper required before source imports')
        sys.path.insert(0,str(replay.MODEL/'code'))
        module=load('a769_fixed_backend',replay.MODEL/'code/centerpoint_backend.py')
        lock=json.loads((replay.MODEL/'legacy86/40_remote/input_lock.json').read_text())
        backend=module.CenterPointBackend(replay.MODEL/'legacy86/vendor/CenterPoint',replay.MODEL/'legacy86/weights/epoch_20.pth',lock['checkpoint_sha256'])
    ref=np.eye(4);ref[:3,:3]=[[0,1,0],[-1,0,0],[0,0,1]];ref[:3,3]=[1,0,2]
    buffer=replay.SweepBuffer();by_tick={r['k']:r for r in detections};rebuilt=[]
    for k,row in enumerate(raw):
        need(row['k']==k and {key:frames[k][key] for key in row}==row,'Raw/committed physical observation differs')
        now,clock_receipt=clock.observe(k,row['frame'],row['frame'],row['clock']['carla_time'],row['clock']['simulator_delta_s'])
        need(clock_receipt==row['clock'] and now==row['time'],'Physical clock reconstruction differs')
        clean=np.load(io.BytesIO(evidence.data('clean/%04d.npy'%k)),allow_pickle=False)
        points=np.load(io.BytesIO(evidence.data('raw/%04d.npy'%k)),allow_pickle=False)
        need(clean.dtype==np.float32 and clean.ndim==2 and clean.shape[1]==4 and len(clean)<=34016,'Clean LiDAR shape differs')
        need(np.isfinite(clean).all() and np.all(clean[:,3]>.01),'Clean LiDAR invalid')
        rebuilt_points,receipt=apply_range_noise(clean,NoiseKey('driving_binding92',case['seed'],case['noise_episode'],'lidar',k))
        need(np.array_equal(rebuilt_points,points) and receipt==noise[k],'Noise reconstruction differs')
        need(hashlib.sha256(points.tobytes()).hexdigest()==frames[k]['raw_sha256'],'Raw cloud binding differs')
        # Post-failure/contact clouds are preserved and checked, but are not fed
        # into a fictitious continuation of the failed policy.
        if prefix['failure_tick'] is not None and k>prefix['failure_tick']:continue
        if k in prefix['contact_branch_ticks']:continue
        buffer.push(replay.Sweep(row['frame'],now,points,np.asarray(row['sensor_world'])))
        if k in by_tick:
            expected=by_tick[k];R=replay.reference_world(np.asarray(row['state']['world']),ref)
            cloud=buffer.combined(R,1,replay.keyed_seed('integration',case['seed'],'lidar','driving_binding92:'+str(k)))
            need(hashlib.sha256(cloud.tobytes()).hexdigest()==expected['combined_hash'],'Ten-sweep detector input differs')
            if backend is not None:
                predicted=backend.predict(cloud,'binding_'+str(k));model=replay.detector_to_world(predicted,R)
                need(model==expected['model'],'Same-runtime detector output differs')
            else:model=expected['model']
            # E4 (A11 §6d): a masked tick ran the detector (checked above) but fed the tracker no rows; replay the same
            if expected.get('masked'):
                need(expected.get('tracker_rows')==0,'Masked tick fed rows to the tracker')
                rebuilt.append(dict(expected,model=[]))
            else:
                need(expected.get('tracker_rows',len(model))==len(model),'Unmasked tick tracker input differs')
                rebuilt.append(dict(expected,model=model))
    need(len(rebuilt)==len(detections),'Incomplete successful detector prefix replay')
    tracker_cfg=json.loads((replay.P/'contracts/tracker_config.json').read_text())
    e4=json.loads((args.folder/'ARM_METHOD_v01.json').read_text()).get('dropout') if (args.folder/'ARM_METHOD_v01.json').exists() else None
    if e4 is not None:tracker_cfg['output']['punish_num']=int(e4['punish_num'])   # E4: the run's output rule (all arms)
    tracker=replay.replay_tracker(rebuilt,tracker_cfg)
    for key,name in [('events','filter_events.jsonl'),('targets','filter_target_covariances.jsonl'),('algebra','filter_algebra.jsonl')]:
        need(tracker[key]==evidence.lines(name,optional=True),'Tracker '+key+' differs')
    evidence.finish()
    need(all(sha(root/name)==h for name,h in source_hashes.items()),'Source changed during review')
    return dict(status='PASS_SAME_RUNTIME_SUCCESSFUL_PERCEPTION_PREFIX' if backend is not None else 'PASS_NOISE_AND_TRACKER_PREFIX_ONLY',
        case=case['id'],prefix=prefix,input_hashes=evidence.hashes,source_binding_sha256=sha(source_path),
        reviewer_sha256=sha(__file__),prefix_contract_sha256=sha(pathlib.Path(__file__).with_name('prefix_contract_v01.py')),
        reused_replay_source_sha256=sha(source),detector_weights_reexecuted=backend is not None,
        successful_tracker_outputs_events_algebra_exact=True,noise_and_sweep_inputs_exact=True,
        failed_call_reexecuted=False,ego_policy_replayed=False,actor_competence_proved=False,
        full_sensor_policy_go=False,paper_go=False,actual_research_episodes=0)


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for name in ('workspace','folder','backup','out','out-backup'):ap.add_argument('--'+name,type=pathlib.Path,required=True)
    ap.add_argument('--detector',action='store_true');ap.add_argument('--expected-pod')
    args=ap.parse_args()
    need(not args.out.exists() and not args.out_backup.exists() and args.out.resolve()!=args.out_backup.resolve(),'Review outputs already exist or coincide')
    # Never write review output into the frozen acquisition case.
    for output in (args.out,args.out_backup):
        need(not output.resolve().is_relative_to(args.folder.resolve()) and not output.resolve().is_relative_to(args.backup.resolve()),'Review must use separate output directories')
    try:
        result=run(args);rc=0
    except Exception as exc:
        result=dict(status='FAILED_PERCEPTION_PREFIX_REVIEW',error=type(exc).__name__+': '+str(exc),traceback=traceback.format_exc(),paper_go=False);rc=2
    result['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    data=(json.dumps(result,indent=2,allow_nan=False)+'\n').encode()
    for output in (args.out,args.out_backup):
        output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
        need(output.read_bytes()==data,'Review output readback differs')
    print(json.dumps({k:result[k] for k in ('status','error','case') if k in result}));raise SystemExit(rc)
