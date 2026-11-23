"""Package E review (v13): review_case_v01.py with the stages that apply to an E-arm capture.

Stages: (1) outcome accounting, unchanged (747 audit_physical_outcomes_v01, independent S and T); (2) perception prefix,
unchanged (noise, ten-sweep input and detector re-executed, CANMOT replay exact) for arms on the CANMOT tracker; skipped
and recorded for the IMM arms, whose tracker is not CANMOT; (3) E record: ARM_METHOD schema, one e_decisions.jsonl record
per assessment decision with the arm's targets and fallback equal to the logged decision, policy-failure flag.
The native-ego replay of review_case_v01 (which rebuilds an old-arm executor) is replaced by stage 3 here and by the
laptop decision replay of package E (tests). The terminal status rule is unchanged: PASS iff outcome accounting passes."""
import argparse,datetime,hashlib,json,os,pathlib,sys,traceback
from prefix_contract_v01 import need
from review_perception_prefix_v01 import run as perception,sha,load


def native(workspace,folder,backup):
    """Stage 3 (E record), in place of the native-ego replay."""
    def lines(p):
        with open(p,encoding='utf-8') as f:return [json.loads(x) for x in f if x.strip()]
    method=json.loads((folder/'ARM_METHOD_v01.json').read_text())
    need(method.get('schema')=='E_ARM_METHOD_V01','Not an E-arm capture')
    for name in ('ARM_METHOD_v01.json','e_decisions.jsonl','frames.jsonl'):
        need((folder/name).read_bytes()==(backup/name).read_bytes(),'Dual evidence differs: '+name)
    recs=lines(folder/'e_decisions.jsonl');decs=[]
    for fr in lines(folder/'frames.jsonl'):
        ex=fr.get('execution') or {}
        d=ex.get('new_decision')
        if d and d['mode']=='assessment':decs.append(d)
    need(len(recs)==len(decs),'E record count differs from assessment decisions')
    for r,d in zip(recs,decs):
        need(r['tick']==d['tick'] and r['arm']==method['arm'],'E record tick or arm differs')
        need([float(x) for x in r['targets']]==[float(x) for x in d['output']['targets']] and bool(r['fallback'])==bool(d['output']['fallback']),'E record selection differs')
        need(d['alpha']==method['alpha'] and d['beta']==0.,'Decision alpha/beta differ from the E method')
    dropout=None
    if method.get('dropout') is not None:
        # E4 (A11 §6d): the run followed the pre-registered mask law, on every detector update tick
        sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
        import e_dropout_v01 as edrop
        d=method['dropout'];contract=json.loads((folder/'contract.json').read_text())
        need(d['law']==edrop.LAW and d['punish_num']==edrop.PUNISH_NUM and d['case_id']==contract['case']['id'],'Dropout record differs from the law, punish_num 3 or the case')
        need(d.get('law_file_sha256')==hashlib.sha256((pathlib.Path(__file__).resolve().parents[1]/'e_dropout_v01.py').read_bytes()).hexdigest(),'Law file differs from the one the run used')
        mask,windows=edrop.mask_for_case(d['case_id'],d['n_updates'])
        need(d['mask']==[int(x) for x in mask] and d['windows']==[list(w) for w in windows] and d['seed']==edrop.seed_for(d['case_id']),'Recorded mask differs from the law')
        dets=lines(folder/'detections.jsonl')
        for r in dets:
            i=edrop.tick_index(r['k']);need(bool(r.get('masked'))==bool(mask[i]),'Detector tick masked flag differs from the law')
            need(r.get('tracker_rows')==(0 if mask[i] else len(r['model'])),'Tracker input differs from the mask')
        imm_checked=None
        if method.get('tracker')!='CANMOT':
            # IMM arms (review M3): independent evidence that the tracker received no detections on masked rows
            trk=json.loads((folder/'E_IMM_TRACKER_v01.json').read_text())
            need(trk.get('punish_num')==d['punish_num'],'IMM tracker punish_num differs from the dropout record')
            ev=lines(folder/'imm_filter_events.jsonl')
            # the detector row of an IMM event is its 'timestamp' (B's Recorder; 'index' is the event's sequence number)
            bad=[e for e in ev if e.get('kind') in ('update','birth') and e.get('timestamp') is not None and 0<=int(e['timestamp'])<len(mask) and mask[int(e['timestamp'])]]
            need(not bad,'IMM update or birth event on a masked row')
            imm_checked=dict(events=len(ev),masked_rows_without_update=int(sum(mask[:len(dets)])))
        dropout=dict(masked_ticks=int(sum(mask[:len(dets)])),detector_updates=len(dets),windows=len(windows),punish_num=d['punish_num'],imm_event_check=imm_checked)
    return dict(status='PASS_E_RECORD',arm=method['arm'],tracker=method['tracker'],assessment_decisions=len(decs),dropout=dropout,
        fallbacks=sum(bool(d['output']['fallback']) for d in decs),policy_failure=(folder/'policy_failure.json').exists(),
        native_intervals_replayed=False,native_origins_replayed=False,laptop_replay='package E tests')


def save(a,b,value):
    raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    for p in (a,b):
        p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        need(p.read_bytes()==raw,'Review save readback differs')


def main():
    ap=argparse.ArgumentParser()
    for name in ('workspace','folder','backup','out','out-backup'):ap.add_argument('--'+name,type=pathlib.Path,required=True)
    ap.add_argument('--expected-pod',required=True)
    args=ap.parse_args();args.detector=True
    need(not args.out.exists() and not args.out_backup.exists(),'Review case already attempted')
    need(args.out.resolve()!=args.out_backup.resolve(),'Review copies coincide')
    for out in (args.out,args.out_backup):
        need(not out.resolve().is_relative_to(args.folder.resolve()) and not out.resolve().is_relative_to(args.backup.resolve()),'Review would alter frozen acquisition')
    args.out.mkdir(parents=True);args.out_backup.mkdir(parents=True)
    begin=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),pid=os.getpid(),pod_id=os.environ.get('RUNPOD_POD_ID'),
        acquisition_folder=str(args.folder),acquisition_backup=str(args.backup),review_source_sha256=sha(__file__))
    save(args.out/'attempt.json',args.out_backup/'attempt.json',begin)
    stage='outcome_accounting';results={};rc=2
    try:
        outcome=load('a769_outcome_review',args.workspace/'747_full_scenario_binding_20261103/audit_physical_outcomes_v01.py')
        value=outcome.review(args.folder,args.workspace/'claude_smoke_v01/DEVELOPMENT_PROTOCOL_SMOKE_v01.json')
        save(args.out/'outcome_accounting.json',args.out_backup/'outcome_accounting.json',value)
        results[stage]=value['status']
        # A failed physical measurement is retained and cannot be promoted by
        # successful policy replay. Review its recorded prefix anyway if complete.
        stage='perception'
        tracker=json.loads((args.folder/'ARM_METHOD_v01.json').read_text()).get('tracker')
        if tracker=='CANMOT':value=perception(args)
        else:value=dict(status='SKIPPED_TRACKER_NOT_CANMOT',tracker=tracker)
        save(args.out/'perception.json',args.out_backup/'perception.json',value);results[stage]=value['status']
        stage='e_record';value=native(args.workspace,args.folder,args.backup)
        save(args.out/'native_ego_and_geometry.json',args.out_backup/'native_ego_and_geometry.json',value);results[stage]=value['status']
        valid=results['outcome_accounting']=='PASS_INDEPENDENT_OUTCOME_ACCOUNTING_ONLY'
        terminal=dict(status='PASS769_RECORDED_SENSOR_EGO_PREFIX' if valid else 'HOLD769_PHYSICAL_MEASUREMENT',stages=results,
            sensor_and_native_prefix_replayed=True,actor_policy_replay_pending=True,actor_competence_pending=True,
            detector_competence_pending=True,full_scenario_go=False,paper_go=False);rc=0 if valid else 2
    except Exception as exc:
        terminal=dict(status='FAILED769_REVIEW_STAGE',stage=stage,error=type(exc).__name__+': '+str(exc),traceback=traceback.format_exc(),completed_stages=results,
            acquisition_repeated=False,original_data_unchanged=True,full_scenario_go=False,paper_go=False)
    terminal['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    save(args.out/'terminal.json',args.out_backup/'terminal.json',terminal)
    print(json.dumps({k:terminal[k] for k in ('status','stage','error') if k in terminal}),flush=True)
    return rc


if __name__=='__main__':raise SystemExit(main())
