"""Claude main-study worker: run a pod's job list with N concurrent CARLA servers (one server per running job).

Derived from worker_smoke_v01.py (smoke-verified). Capture, review and actor review calls are unchanged.
Changes for the main study (blueprint v02):
  * continuous slot scheduling (a free slot starts the next pending job; starts are staggered);
  * resume: jobs whose SUMMARY already sits on the volume are skipped; a job that failed for a
    technical reason is retried once (outcome-blind: the retry rule never reads S or T);
  * archives keep every log but drop the LiDAR .npy frames (raw/ and clean/) unless the job has
    keep_raw=true; FILE_HASHES.json records the SHA-256 of every captured file, frames included;
  * after the archive is copied to the volume and its hash verified, the local job folder and
    local archive are deleted (local disk would otherwise fill); nothing on /workspace is deleted;
  * a status file (counts, running jobs, last control result, rate) on local disk and on the volume.

Revision 2 (10 Nov 2026), after an orphaned CARLA server on pod main-02 blocked one slot (Codex's stop_group raised
FileNotFoundError on /proc/<pid>/task while the server was exiting, so the server survived and later jobs on that slot
failed with 'Previous/unowned simulator listener remains'):
  * before a server starts, any process listening on THIS slot's three ports and owned by the carla user is killed
    (process group, SIGKILL); a slot's ports are used only by that slot, so such a listener is necessarily stale;
  * if stop_group raises, the server's process group is killed with SIGKILL and the ports are waited for;
  * a run counts as an attempt only if its capture was launched; failures before launch (server/ports) are retried
    up to 3 times without consuming an attempt; a slot with 3 consecutive pre-launch failures is paused.

Package E (revision v13, 19 Nov 2026), same file name so the unchanged remote chain runs it:
  * E arms (E_Z, E_F0, E_N, E_CK3, E_TG, E_PS, E_F0_IMM, E_N_IMM, E_BRAKE) with job fields g, triple, brake_from_k,
    level, tracker; they capture with 'cuda_entry_smoke_v01.py capture_e' (probe_e_v01.py) and review with 'review_e'
    (review/review_case_e_v01.py); the old arms (A1 controls) keep the unchanged capture and review commands.
  * Nothing else changes (slots, resume, retry, archive, control halt).

Parent:  worker_main_v01.py --jobs JOBS.json [--slots 2] [--simulate]
Child:   worker_main_v01.py --jobs ... --run-job ID --attempt K --port PORT   (started by the parent)
"""
import argparse,datetime,hashlib,json,os,pathlib,shutil,signal,subprocess,sys,tarfile,threading,time,traceback
P=pathlib.Path(__file__).resolve().parent            # /opt/programme_a_gpu750/workspace/claude_smoke_v01
W=P.parent;Q=W.parent
LOCAL=pathlib.Path('/opt/claude_main_simulate' if '--simulate' in sys.argv else '/opt/claude_main')
PY=str(Q/'.venv/bin/python')
OLD_ARMS=('fixed','native','learned_without','learned_with')
E_ARMS=('E_Z','E_F0','E_N','E_CK3','E_TG','E_PS','E_F0_IMM','E_N_IMM','E_BRAKE')
ARMS=OLD_ARMS+E_ARMS
JOB_FIELDS={'id','case','arm','alpha','beta','kappa','phase','role','scenario','keep_raw','reference','note','knob','history','history_model','history_model_sha256',
            'g','triple','brake_from_k','level','tracker','dropout','punish_num'}
read=lambda p:json.loads(pathlib.Path(p).read_bytes())
def now():return datetime.datetime.now(datetime.timezone.utc)


def sha(path):
    h=hashlib.sha256()
    with pathlib.Path(path).open('rb') as f:
        for block in iter(lambda:f.read(8*1024**2),b''):h.update(block)
    return h.hexdigest()


def save(path,value):
    path=pathlib.Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    return raw


def state(path,value):
    path=pathlib.Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=pathlib.Path(str(path)+'.partial')
    with tmp.open('w') as f:json.dump(dict(value,utc=now().isoformat()),f);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)


def volume_root(cfg,simulate):
    return pathlib.Path('/workspace')/(cfg.get('volume_folder','claude_main_v01')+('_simulate' if simulate else ''))


def child_env(port):
    env={k:v for k,v in os.environ.items() if k not in ('RUNPOD_API_KEY','CLAUDE_SMOKE_WORKSPACE_ROOT')}
    env.update(XDG_RUNTIME_DIR=f'/tmp/programme_a_carla_runtime_{port}',OPENBLAS_CORETYPE='HASWELL',CUBLAS_WORKSPACE_CONFIG=':4096:8',
               PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    return env


def load_jobs(path):
    cfg=read(path);assert cfg['schema']=='CLAUDE_MAIN_JOBS_V01'
    protocol=read(P/cfg['protocol']);cases={c['id'] for c in protocol['cases']}
    ids=[j['id'] for j in cfg['jobs']];assert len(ids)==len(set(ids)),'Duplicate job id'
    for j in cfg['jobs']:
        assert j['arm'] in ARMS and j['case'] in cases,j['id']
        assert set(j)-JOB_FIELDS==set(),'Unknown job field: '+j['id']
        assert '__' not in j['id'],'Job ids must not contain a double underscore'
        h=j.get('history','off');assert h in ('off','log','model'),j['id']
        if h!='off':assert j['arm'] in ('learned_without','learned_with'),'history modes are for learned arms only: '+j['id']
        if h=='model':assert j.get('history_model') and j.get('history_model_sha256'),'model mode needs history_model and history_model_sha256: '+j['id']
        else:assert not j.get('history_model') and not j.get('history_model_sha256'),j['id']
        if j['arm'] in E_ARMS:
            assert all(j.get(k) is None for k in ('alpha','beta','kappa')) and h=='off','E arms take g / triple / brake_from_k only: '+j['id']
            if j['arm']=='E_PS':assert j.get('triple') is not None and len(j['triple'])==3 and j.get('g') is None,j['id']
            elif j['arm'] in ('E_Z','E_BRAKE'):assert j.get('g') in (None,0,0.) and j.get('triple') is None,j['id']
            else:assert j.get('g') is not None and float(j['g'])>=0 and j.get('triple') is None,j['id']
            if j['arm']!='E_BRAKE':assert j.get('brake_from_k') is None,j['id']
            # E4 (A11 §6d): both dropout knobs or neither; only the four E4 arms
            if j.get('dropout') is not None or j.get('punish_num') is not None or j.get('phase')=='E4':
                assert j.get('dropout')=='A11D2' and j.get('punish_num')==3 and j['arm'] in ('E_F0','E_N','E_F0_IMM','E_N_IMM'),'Invalid or missing dropout knobs (phase E4: law A11D2, punish_num 3): '+j['id']
        else:assert all(j.get(k) is None for k in ('g','triple','brake_from_k','dropout','punish_num')),j['id']
    return cfg


def history_args(job):
    h=job.get('history','off')
    if h=='off':return []
    args=['--history',h]
    if h=='model':args+=['--history-model',job['history_model'],'--history-model-sha256',job['history_model_sha256']]
    return args


def knob_args(job):
    args=[]
    for name in ('alpha','beta','kappa'):
        if job.get(name) is not None:args+=['--'+name,repr(float(job[name]))]
    if job['arm'] in E_ARMS:
        if job.get('g') is not None and job['arm'] not in ('E_Z','E_BRAKE'):args+=['--g',repr(float(job['g']))]
        if job.get('triple') is not None:args+=['--triple',','.join(repr(float(x)) for x in job['triple'])]
        if job.get('brake_from_k') is not None:args+=['--brake-from-k',str(int(job['brake_from_k']))]
        if job.get('dropout') is not None:args+=['--dropout',str(job['dropout']),'--punish-num',str(int(job['punish_num']))]
    return args


def stages(job):
    return ('capture_e','review_e') if job['arm'] in E_ARMS else ('capture','review')


def run_id(job_id,attempt,pre=0):
    base=job_id if attempt==1 else f'{job_id}__r{attempt-1}'
    return base if pre==0 else f'{base}__p{pre}'


def kill_stale_listeners(ports):
    """Kill (SIGKILL, whole process group) any carla-owned process listening on these TCP ports. Returns what was killed."""
    import pwd
    try:carla_uid=pwd.getpwnam('carla').pw_uid
    except KeyError:return []
    inodes={}
    for table in ('/proc/net/tcp','/proc/net/tcp6'):
        try:lines=open(table).read().splitlines()[1:]
        except OSError:continue
        for ln in lines:
            f=ln.split()
            if len(f)>9 and f[3]=='0A' and int(f[1].split(':')[1],16) in ports:inodes[f[9]]=int(f[1].split(':')[1],16)
    killed=[]
    if not inodes:return killed
    for pid in [p for p in os.listdir('/proc') if p.isdigit()]:
        try:
            if os.stat(f'/proc/{pid}').st_uid!=carla_uid:continue
            for fd in os.listdir(f'/proc/{pid}/fd'):
                try:target=os.readlink(f'/proc/{pid}/fd/{fd}')
                except OSError:continue
                if target.startswith('socket:[') and target[8:-1] in inodes:
                    pgid=os.getpgid(int(pid));os.killpg(pgid,signal.SIGKILL);killed.append(dict(pid=int(pid),pgid=pgid,port=inodes[target[8:-1]]));break
        except (OSError,ProcessLookupError):continue
    if killed:time.sleep(3)
    return killed


class GpuSampler(threading.Thread):
    def __init__(self,path,period=15):
        super().__init__(daemon=True);self.path=path;self.period=period;self.stop_event=threading.Event()
    def run(self):
        while not self.stop_event.is_set():
            try:
                out=subprocess.run(['nvidia-smi','--query-gpu=memory.used,memory.total,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=10).stdout.strip()
                with open(self.path,'a') as f:f.write(json.dumps(dict(utc=now().isoformat(),sample=out))+'\n')
            except Exception as exc:
                with open(self.path,'a') as f:f.write(json.dumps(dict(utc=now().isoformat(),error=str(exc)))+'\n')
            self.stop_event.wait(self.period)


def decisions_and_fallbacks(case_folder):
    calls=fallbacks=0
    for f in sorted((case_folder/'ordered_capture/frames').glob('*/decision.json')):
        payload=read(f)['payload']
        if payload.get('selection') is not None:
            calls+=1;fallbacks+=bool(payload['selection']['decision']['output']['fallback'])
    return calls,fallbacks


def run_job(cfg,jobs_path,job_id,attempt,port,simulate,pre=0):
    job=next(j for j in cfg['jobs'] if j['id']==job_id);case=job['case'];rid=run_id(job_id,attempt,pre)
    J=LOCAL/'jobs'/rid
    if J.exists():J.rename(LOCAL/'jobs'/(rid+'__abandoned_'+now().strftime('%Y%m%dT%H%M%SZ')))
    J.mkdir(parents=True)
    out=J/'capture'/case;copy=J/'capture_copy'/case
    pod=os.environ['RUNPOD_POD_ID'];env=child_env(port);t={}
    save(J/'JOB.json',dict(job=job,attempt=attempt,run_id=rid,port=port,pid=os.getpid(),pod_id=pod,utc=now().isoformat(),jobs_file_sha256=sha(jobs_path),
        release_sha256=sha(P/'RELEASE_SMOKE_v01.json') if (P/'RELEASE_SMOKE_v01.json').exists() else None,worker_sha256=sha(__file__),simulate=simulate))
    assert shutil.disk_usage('/opt').free>15*1024**3,'Local evidence reserve below 15 GiB'
    capture_rc=review_rc=actor_rc=None;failure=None
    if simulate:
        time.sleep(3);t['server_start_utc']=now().isoformat();capture_rc=review_rc=actor_rc=0
        out.mkdir(parents=True);copy.mkdir(parents=True)
        for d in (out,copy):(d/'raw').mkdir();(d/'raw/0000.npy').write_bytes(b'x'*1000);(d/'log.jsonl').write_text('{}\n')
        t['actor_review_end_utc']=now().isoformat()
    else:
        sys.path.insert(0,str(Q/'remote'))
        from server_lifecycle import assert_ports_free,capture_lease,listener_owned_by_group,stop_group,wait_ports_free
        subprocess.run(['install','-d','-o','carla','-g','carla','-m','700',env['XDG_RUNTIME_DIR']],check=True)
        sampler=GpuSampler(J/'gpu_samples.jsonl');sampler.start()
        server=lease=probe=None;ports=(port,port+1,port+2)
        try:
            stale=kill_stale_listeners(set(ports))
            if stale:save(J/'STALE_LISTENERS_KILLED.json',dict(killed=stale,utc=now().isoformat()))
            assert_ports_free(ports);t['server_start_utc']=now().isoformat()
            with (J/'server.log').open('xb') as log:
                server=subprocess.Popen(['runuser','-u','carla','--','./CarlaUE4.sh','-RenderOffScreen','-quality-level=Epic','-nosound',f'-carla-rpc-port={port}'],
                    cwd=Q/'carla_runtime/carla-0.9.15',env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
                lease=capture_lease(server);save(J/'SERVER_LEASE.json',lease);ready=False;until=time.monotonic()+cfg['server_ready_timeout_s']
                while time.monotonic()<until and server.poll() is None:
                    if listener_owned_by_group(port,lease['pgid']):
                        try:
                            r=subprocess.run([PY,'-c',f"import carla;c=carla.Client('127.0.0.1',{port});c.set_timeout(2);assert c.get_server_version()=='0.9.15';c.get_world()"],
                                env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=5)
                            if r.returncode==0:ready=True;break
                        except subprocess.TimeoutExpired:pass
                    time.sleep(1)
                assert ready,'CARLA server not ready'
                t['server_ready_utc']=now().isoformat()
                command=[PY,'-B',str(P/'cuda_entry_smoke_v01.py'),stages(job)[0],'--case',case,'--arm',job['arm'],*knob_args(job),
                         '--out',str(out),'--backup',str(copy),'--carla-port',str(port),*history_args(job)]
                with (J/'capture.log').open('xb') as log:
                    probe=subprocess.Popen(command,env=env,stdout=log,stderr=subprocess.STDOUT)
                    save(J/'CAPTURE_LAUNCH.json',dict(pid=probe.pid,utc=now().isoformat(),case=case,command=command))
                    try:capture_rc=probe.wait(timeout=cfg['capture_timeout_s'])
                    except subprocess.TimeoutExpired:capture_rc='TIMEOUT'
                save(J/'CAPTURE_TERMINAL.json',dict(exit_code=capture_rc,utc=now().isoformat(),case=case,timeout_s=cfg['capture_timeout_s']))
        except BaseException as exc:
            failure=dict(stage='server_or_capture',error=type(exc).__name__+': '+str(exc),traceback=traceback.format_exc())
        finally:
            if probe is not None and probe.poll() is None:
                probe.terminate()
                try:probe.wait(timeout=10)
                except subprocess.TimeoutExpired:probe.kill();probe.wait(timeout=10)
            if server is not None and lease is not None:
                try:save(J/'SHUTDOWN.json',dict(shutdown=stop_group(server,lease),ports=wait_ports_free(ports)))
                except BaseException as exc:
                    # Revision 2: force the group down so the slot's ports are released; record it; the run's
                    # capture result is kept, but a shutdown error still marks the run as a technical failure.
                    forced=None
                    try:os.killpg(lease['pgid'],signal.SIGKILL);time.sleep(3);forced=dict(killpg=lease['pgid'],stale=kill_stale_listeners(set(ports)))
                    except BaseException as exc2:forced=dict(error=type(exc2).__name__+': '+str(exc2))
                    save(J/'SHUTDOWN_FORCED.json',dict(stop_group_error=type(exc).__name__+': '+str(exc),forced=forced,utc=now().isoformat()))
                    failure=failure or dict(stage='shutdown',error=type(exc).__name__+': '+str(exc),forced=forced)
            t['server_stopped_utc']=now().isoformat()
        if capture_rc==0 and failure is None:
            t['review_start_utc']=now().isoformat()
            with (J/'review.log').open('xb') as log:
                try:review_rc=subprocess.run([PY,'-B',str(P/'cuda_entry_smoke_v01.py'),stages(job)[1],'--workspace',str(W),'--folder',str(out),'--backup',str(copy),
                    '--out',str(J/'review'),'--out-backup',str(J/'review_copy'),'--expected-pod',pod],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=cfg['review_timeout_s']).returncode
                except subprocess.TimeoutExpired:review_rc='TIMEOUT'
            t['review_end_utc']=now().isoformat()
            with (J/'actor_review.log').open('xb') as log:
                try:actor_rc=subprocess.run([PY,'-B',str(P/'review/review_actor_records_v04.py'),'--workspace',str(W),'--folder',str(out),'--backup',str(copy),
                    '--review-code',str(P/'review'),'--out',str(J/'actor_review.json'),'--out-backup',str(J/'actor_review_copy.json')],
                    env=env,stdout=log,stderr=subprocess.STDOUT,timeout=cfg['actor_review_timeout_s']).returncode
                except subprocess.TimeoutExpired:actor_rc='TIMEOUT'
            t['actor_review_end_utc']=now().isoformat()
        sampler.stop_event.set();sampler.join(timeout=20)
    summary=summarize(job,attempt,rid,port,J,out,capture_rc,review_rc,actor_rc,failure,t,simulate)
    summary['pre_launch_retry']=pre
    save(J/'SUMMARY.json',summary);state(LOCAL/'summaries'/f'{rid}.json',summary)
    archive_and_publish(cfg,rid,J,out,copy,summary,bool(job.get('keep_raw')),simulate)
    return 0 if summary['status']=='CAPTURED_AND_REVIEWED' else (2 if summary['capture_launched'] else 3)


def summarize(job,attempt,rid,port,J,out,capture_rc,review_rc,actor_rc,failure,t,simulate):
    opt=lambda p:read(p) if pathlib.Path(p).is_file() else None
    launch=opt(J/'CAPTURE_LAUNCH.json');terminal=opt(J/'CAPTURE_TERMINAL.json')
    wall=None
    if launch and terminal:wall=(datetime.datetime.fromisoformat(terminal['utc'])-datetime.datetime.fromisoformat(launch['utc'])).total_seconds()
    outcome=opt(out/'assessment_outcomes.json');accounting=opt(J/'review/outcome_accounting.json')
    calls=fallbacks=None
    if (out/'ordered_capture/frames').is_dir():calls,fallbacks=decisions_and_fallbacks(out)
    review_terminal=opt(J/'review/terminal.json');actor=opt(J/'actor_review.json');native=opt(J/'review/native_ego_and_geometry.json')
    status='CAPTURED_AND_REVIEWED' if capture_rc==0 and review_rc==0 and actor_rc==0 and failure is None else 'INCOMPLETE_OR_FAILED'
    agree=(outcome is not None and accounting is not None and all(outcome.get(k)==accounting.get(k) for k in ('S','T','first_contact_frame','first_policy_failure_frame')))
    if simulate:agree=True
    if status=='CAPTURED_AND_REVIEWED' and not agree:status='READERS_DISAGREE'
    if job.get('dropout') is not None and status=='CAPTURED_AND_REVIEWED' and not simulate:
        # E4 (review M4): the run's method and review must carry the job's dropout law and punish_num
        dm=(opt(out/'ARM_METHOD_v01.json') or {}).get('dropout') or {}
        er=((review_terminal or {}).get('stages') or {}).get('e_record')
        if not (dm.get('law')==job['dropout'] and dm.get('punish_num')==job['punish_num'] and er=='PASS_E_RECORD'):status='E4_METHOD_MISMATCH'
    ref=job.get('reference') or {}
    comparison=None
    if outcome and outcome.get('S') is not None and 'T' in ref:
        comparison=dict(S_equal=outcome['S']==ref.get('S'),T_reference=ref['T'],T_observed=outcome['T'],T_abs_difference=abs(outcome['T']-ref['T']),
                        T_bit_identical=outcome['T']==ref['T'],identical=outcome['S']==ref.get('S') and outcome['T']==ref['T'])
    return dict(schema='CLAUDE_MAIN_SUMMARY_V01',status=status,job=job['id'],attempt=attempt,run_id=rid,capture_launched=launch is not None,case=job['case'],arm=job['arm'],
        phase=job.get('phase'),role=job.get('role'),scenario=job.get('scenario'),knob=job.get('knob'),keep_raw=bool(job.get('keep_raw')),
        history=job.get('history','off'),history_model=job.get('history_model'),history_model_sha256=job.get('history_model_sha256'),
        knobs={k:job.get(k) for k in ('alpha','beta','kappa')},e_job={k:job.get(k) for k in ('g','triple','brake_from_k','level','tracker','dropout','punish_num')},
        port=port,pod_id=os.environ.get('RUNPOD_POD_ID'),
        method=opt(out/'ARM_METHOD_v01.json'),assessment_outcomes=outcome,outcome_accounting=accounting,S_T_reader_agree=agree,
        decision_count=calls,fallback_count=fallbacks,capture_wall_seconds=wall,capture_exit=capture_rc,review_exit=review_rc,actor_review_exit=actor_rc,
        review_status=review_terminal and review_terminal.get('status'),review_stages=review_terminal and review_terminal.get('stages'),
        native_intervals_replayed=native and native.get('native_intervals_replayed'),native_origins_replayed=native and native.get('native_origins_replayed'),
        actor_review_status=actor and actor.get('status'),failure=failure,timings=dict(t,capture_launch_utc=launch and launch['utc'],capture_terminal_utc=terminal and terminal['utc']),
        reference=ref or None,comparison_to_reference=comparison,simulate=simulate)


def is_frame(rel):
    parts=rel.parts
    return rel.suffix=='.npy' and len(parts)>=2 and parts[-2] in ('raw','clean')


def archive_and_publish(cfg,rid,J,out,copy,summary,keep_raw,simulate):
    pairs=[];mismatch=[]
    if out.is_dir():
        for f in sorted(p for p in out.rglob('*') if p.is_file()):
            rel=f.relative_to(out);other=copy/rel;h=sha(f)
            if not other.is_file() or sha(other)!=h:mismatch.append(rel.as_posix())
            pairs.append(dict(path=rel.as_posix(),sha256=h,bytes=f.stat().st_size))
    save(J/'CASE_COPY_CHECK.json',dict(files=len(pairs),mismatches=mismatch,all_match=not mismatch))
    save(J/'FILE_HASHES.json',dict(case_folder='capture/'+summary['case'],files=pairs,frames_kept=keep_raw))
    dest=LOCAL/'archives'/f'claude_main_{rid}.tar.gz';dest.parent.mkdir(parents=True,exist_ok=True)
    if dest.exists():dest.unlink()
    part=pathlib.Path(str(dest)+'.partial')
    if part.exists():part.unlink()
    dropped=0
    with tarfile.open(part,'x:gz',compresslevel=6) as tar:
        for f in sorted(p for p in J.rglob('*') if p.is_file()):
            rel=f.relative_to(J)
            if rel.parts[0]=='capture_copy' or f.name.endswith('.partial'):continue
            if not keep_raw and rel.parts[0]=='capture' and is_frame(rel):dropped+=1;continue
            tar.add(f,arcname=f'{rid}/{rel.as_posix()}',recursive=False)
    with part.open('rb') as f:os.fsync(f.fileno())
    os.replace(part,dest)
    receipt=dict(archive=dest.name,sha256=sha(dest),bytes=dest.stat().st_size,run_id=rid,status=summary['status'],frames_dropped=dropped,keep_raw=keep_raw,utc=now().isoformat())
    target=volume_root(cfg,simulate)/'results'/rid
    if target.exists():target=volume_root(cfg,simulate)/'results'/(rid+'__dup_'+now().strftime('%Y%m%dT%H%M%SZ'))
    target.mkdir(parents=True,exist_ok=False)
    with dest.open('rb') as src,(target/dest.name).open('xb') as dst:shutil.copyfileobj(src,dst,8*1024**2);dst.flush();os.fsync(dst.fileno())
    assert sha(target/dest.name)==receipt['sha256'],'Volume archive copy differs'
    save(target/(dest.name+'.receipt.json'),receipt);save(target/'SUMMARY.json',summary)
    # Local cleanup only after the verified volume copy (the volume keeps everything).
    shutil.rmtree(J);dest.unlink()


def done_runs(cfg,simulate):
    """Map job id -> list of (attempt, status) already published on the volume."""
    seen={}
    root=volume_root(cfg,simulate)/'results'
    if root.is_dir():
        for s in root.glob('*/SUMMARY.json'):
            try:d=read(s)
            except Exception:continue
            launched=d.get('capture_launched',(d.get('timings') or {}).get('capture_launch_utc') is not None)
            seen.setdefault(d['job'],[]).append((d.get('attempt',1),d['status'],bool(launched)))
    return seen


def parent(args):
    cfg=load_jobs(args.jobs);pod=os.environ.get('RUNPOD_POD_ID')
    assert pod and 'RUNPOD_API_KEY' not in os.environ and os.path.ismount('/workspace')
    if not args.simulate:
        ok=read(pathlib.Path('/opt/claude_smoke/BOOTSTRAP_OK.json'));assert ok['status']=='BOOTSTRAP_OK_CLAUDE_SMOKE_V01' and ok['pod_id']==pod,'Run the bootstrap on this pod first'
        release=read(P/'RELEASE_SMOKE_v01.json');assert release['pod_id']==pod and release['protocol_sha256']==sha(P/cfg['protocol'])
    assert 1<=args.slots<=8
    vol=volume_root(cfg,args.simulate);(vol/'status').mkdir(parents=True,exist_ok=True)
    max_attempts=int(cfg.get('max_attempts',2));stagger=float(cfg.get('concurrent_start_stagger_s',15))
    seen=done_runs(cfg,args.simulate)
    pending=[];finished=[]
    for j in cfg['jobs']:
        runs=sorted(seen.get(j['id'],[]),key=lambda x:x[0])
        if any(s=='CAPTURED_AND_REVIEWED' for _,s,_ in runs):finished.append(dict(job=j['id'],status='CAPTURED_AND_REVIEWED',resumed=True));continue
        launched=[r for r in runs if r[2]]                       # revision 2: only launched captures are attempts
        if len(launched)>=max_attempts:finished.append(dict(job=j['id'],status='FAILED_FINAL',resumed=True));continue
        pending.append((j,len(launched)+1,0))
    stamp=now().strftime('%Y%m%dT%H%M%SZ');status_path=LOCAL/'worker_status.json'
    save(LOCAL/f'WORKER_STARTED_{stamp}.json',dict(pid=os.getpid(),pod_id=pod,utc=now().isoformat(),jobs_file=str(args.jobs),jobs_file_sha256=sha(args.jobs),
        slots=args.slots,total=len(cfg['jobs']),resumed_finished=len(finished),pending=len(pending),simulate=args.simulate))
    logs=LOCAL/'job_logs';logs.mkdir(parents=True,exist_ok=True)
    running={};last_start=0.0;t0=time.monotonic();last_control=None;prefail={};disabled=set()
    def report(status):
        ok=sum(f['status']=='CAPTURED_AND_REVIEWED' for f in finished);bad=[f['job'] for f in finished if f['status']!='CAPTURED_AND_REVIEWED']
        fresh=[f for f in finished if not f.get('resumed')];hours=(time.monotonic()-t0)/3600
        value=dict(status=status,pod_id=pod,total=len(cfg['jobs']),done_ok=ok,failed_final=bad,pending=len(pending),
                   running=[dict(job=r['job']['id'],attempt=r['attempt'],slot=s,since=r['since']) for s,r in running.items()],
                   runs_this_session=len(fresh),runs_per_hour=(len(fresh)/hours if hours>0.05 else None),last_control=last_control,slots=args.slots,
                   disabled_slots=sorted(disabled),worker_revision=2)
        state(status_path,value);state(vol/'status'/f'{pod}.json',value)
    report('RUNNING')
    while pending or running:
        if not running and len(disabled)>=args.slots:break        # every slot paused: stop, pending jobs stay pending
        free=[s for s in range(args.slots) if s not in running and s not in disabled]
        if free and pending and time.monotonic()-last_start>=stagger:
            slot=free[0];j,attempt,pre=pending.pop(0);port=2000+10*slot;rid=run_id(j['id'],attempt,pre)
            out=(logs/f"{rid}_{stamp}.stdout.log").open('wb');err=(logs/f"{rid}_{stamp}.stderr.log").open('wb')
            cmd=[sys.executable,'-B',str(pathlib.Path(__file__).resolve()),'--jobs',str(args.jobs),'--run-job',j['id'],'--attempt',str(attempt),'--pre',str(pre),'--port',str(port)]
            if args.simulate:cmd.append('--simulate')
            (LOCAL/'summaries'/f'{rid}.json').unlink(missing_ok=True)          # never read a stale summary for this run id
            p=subprocess.Popen(cmd,stdout=out,stderr=err)
            running[slot]=dict(job=j,attempt=attempt,pre=pre,proc=p,out=out,err=err,since=now().isoformat());last_start=time.monotonic()
            report('RUNNING');continue
        time.sleep(2)
        for slot,r in list(running.items()):
            rc=r['proc'].poll()
            if rc is None:continue
            r['out'].close();r['err'].close();del running[slot]
            j=r['job'];rid=run_id(j['id'],r['attempt'],r['pre'])
            summ=LOCAL/'summaries'/f'{rid}.json'                          # the child's own copy (volume path may carry a __dup suffix)
            s=read(summ) if summ.is_file() else {}
            status=s.get('status','NO_SUMMARY');launched=bool(s.get('capture_launched'))
            if status=='CAPTURED_AND_REVIEWED':
                prefail[slot]=0
                finished.append(dict(job=j['id'],status=status,attempt=r['attempt']))
                if j.get('role')=='control':
                    cmp_=s.get('comparison_to_reference') or {}
                    last_control=dict(job=j['id'],identical=bool(cmp_.get('identical')),utc=now().isoformat())
                    if not cmp_.get('identical') and not args.simulate:
                        pending.clear();report('HALTED_CONTROL_MISMATCH')   # E2: halt this pod
            elif not launched and r['pre']<3:
                prefail[slot]=prefail.get(slot,0)+1                         # revision 2: pre-launch failure, not an attempt
                if prefail[slot]>=3:disabled.add(slot)
                pending.insert(0,(j,r['attempt'],r['pre']+1))
            elif launched and r['attempt']<max_attempts:
                prefail[slot]=0
                pending.insert(0,(j,r['attempt']+1,0))                      # E5: one outcome-blind retry
            else:
                finished.append(dict(job=j['id'],status='FAILED_FINAL',attempt=r['attempt'],launched=launched))
            report('RUNNING')
    final='HALTED_CONTROL_MISMATCH' if last_control and not last_control['identical'] and not args.simulate else ('HALTED_ALL_SLOTS_PAUSED' if pending else 'FINISHED')
    report(final)
    save(LOCAL/f'WORKER_TERMINAL_{stamp}.json',dict(status=final,pod_id=pod,utc=now().isoformat(),finished=finished))
    print(json.dumps(dict(status=final,done=len(finished))),flush=True)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--jobs',type=pathlib.Path,required=True);ap.add_argument('--slots',type=int,default=2)
    ap.add_argument('--run-job',default=None);ap.add_argument('--attempt',type=int,default=1);ap.add_argument('--port',type=int,default=None)
    ap.add_argument('--simulate',action='store_true');ap.add_argument('--pre',type=int,default=0)
    args=ap.parse_args();args.jobs=args.jobs.resolve()
    if args.run_job is None:return parent(args)
    cfg=load_jobs(args.jobs)
    def stop(*_):raise RuntimeError('Stop signal; partial evidence preserved')
    signal.signal(signal.SIGTERM,stop)
    return run_job(cfg,args.jobs,args.run_job,args.attempt,args.port,args.simulate,args.pre)


if __name__=='__main__':raise SystemExit(main())
