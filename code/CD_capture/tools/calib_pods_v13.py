"""Run the A10 sec. 2.6 double bootstraps of packages C and D on several RunPod pods in parallel (revision v13; 20 Nov 2026,
Claude Opus 5.5). The statistic code is analysis/calib_remote_v13.py (unchanged numerics); this file only moves files and tasks.

Each (label, inner seed) is split into chunks of outer samples (--outer LO:HI). A chunk is a task file "LABEL SEED LO HI".
Pods are named claude-v13cd-kNN and created with pods_v13.create (spend-log row, SSH config). On each pod tools/calib_worker_v13.sh
runs one single-threaded worker per vCPU, claiming tasks from /opt/calib/todo by atomic rename. Outputs are chunk files
<label>_<seed>_o<LO>_<HI>.npz, fetched to RUN/chunks/ and joined by tools/calib_merge_v13.py into analysis/out/calib/<label>_<seed>.npz.

Usage (python -I calib_pods_v13.py CMD ...; RUN = pods/calib_run or --run DIR):
  plan --jobdir D --labels A,B,... [--chunk-gl 20] [--chunk-h4 200]   write RUN/tasks/*.task (all tasks, unassigned)
  up NAME [NAME ...] [--deadline-h H]       create pods, install numpy/numba (versions of the laptop venv), upload code + jobs, start workers
  assign                                     deal the unassigned tasks to live pods in proportion to their vCPUs
  status                                     per pod: vCPUs, todo/running/done/failed; overall: tasks fetched
  steal                                      move queued (unclaimed) tasks from the pod with the longest queue to pods with idle workers
  fetch                                      download finished chunk files not yet on the laptop (SHA-256 checked after transfer)
  down [NAME ...]                            delete each pod whose tasks are all fetched (or none left), via pods_v13.delete
  requeue                                    move failed tasks back to the queue (prints the end of each failed task's log)
  final                                      mark that all labels are planned and assigned (loop deletes pods only after this)
  loop                                       every 5 min: fetch, steal, (after final) down; requeue a failed task once
Only pods named claude-v13cd-k* are touched.
"""
import hashlib, json, pathlib, subprocess, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(HERE))
import pods_v13 as pv

KPREFIX = 'claude-v13cd-k'
GPU = 'NVIDIA GeForce RTX 4090'
CODE = [CD / 'analysis' / 'calib_remote_v13.py', CD / 'analysis' / 'gl_fast_v13.py',
        pathlib.Path(r'<library folder>\optA_lib_v02.py')]
WORKER = HERE / 'calib_worker_v13.sh'
PINS = 'numpy==2.5.4 numba==0.68.1'          # = analysis/out/VENV_FREEZE.txt (llvmlite follows numba)
ARGS = sys.argv[1:]
RUN = pathlib.Path(ARGS[ARGS.index('--run') + 1]) if '--run' in ARGS else CD / 'pods' / 'calib_run'


def opt(name, default=None):
    return ARGS[ARGS.index(name) + 1] if name in ARGS else default


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def live_pods():
    return sorted(p.name for p in (CD / 'pods').glob(KPREFIX + '*') if (p / 'pod.json').is_file() and not (p / 'TERMINATED').exists())


def ssh(name, cmd, timeout=600):
    r = pv.ssh(name, cmd, timeout=timeout)
    if r.returncode != 0: raise RuntimeError(f'{name}: ssh rc={r.returncode}: {r.stderr[-400:]}')
    return r.stdout


def plan():
    """Adds tasks; may be called once per program: first program (default runner calib_remote_v13.py, chunk by job kind) and
    the recount (--runner rc_calib_remote_v13.py --code its,extra,files --chunk N). PLAN.json accumulates."""
    jobdir = pathlib.Path(opt('--jobdir')).resolve(); labels = opt('--labels').split(',')
    cgl, ch4 = int(opt('--chunk-gl', 20)), int(opt('--chunk-h4', 200)); cfix = opt('--chunk')
    runner = opt('--runner', 'calib_remote_v13.py'); extra = [str(pathlib.Path(x).resolve()) for x in opt('--code', '').split(',') if x]
    td = RUN / 'tasks'; td.mkdir(parents=True, exist_ok=True)
    pf = RUN / 'PLAN.json'
    rec = json.loads(pf.read_text(encoding='utf-8')) if pf.is_file() else dict(labels={}, code=[], written=[])
    rec['written'].append(pv.est())
    rec['code'] = sorted(set(rec['code']) | set(extra))
    import numpy as np
    for lab in labels:
        assert lab not in rec['labels'], f'label {lab} already planned'
        meta = json.loads((jobdir / f'{lab}.meta.json').read_text(encoding='utf-8'))
        z = np.load(jobdir / f'{lab}.job.npz', allow_pickle=False)
        kind = str(z['kind']) if 'kind' in z.files else 'other'
        n_outer = int(meta['n_outer']); c = int(cfix) if cfix else (cgl if kind == 'GL' else ch4)
        seeds = [int(s) for s in meta.get('pod_seeds', (20261913, 20261914))]
        rec['labels'][lab] = dict(jobdir=str(jobdir), runner=runner, kind=kind, n_outer=n_outer, chunk=c, seeds=seeds,
                                  job_sha256=sha(jobdir / f'{lab}.job.npz'), meta_sha256=sha(jobdir / f'{lab}.meta.json'))
        for seed in seeds:
            for lo in range(0, n_outer, c):
                hi = min(lo + c, n_outer)
                (td / f'{lab}__{seed}__{lo:04d}_{hi:04d}.task').write_bytes(f'{lab} {seed} {lo} {hi} {runner}\n'.encode('ascii'))  # LF only
    pf.write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print(json.dumps(dict(tasks=len(list(td.glob('*.task'))), labels=rec['labels'])))


def up():
    names = [a for a in ARGS[1:] if a.startswith(KPREFIX)]
    dl = float(opt('--deadline-h', 6))
    p = json.loads((RUN / 'PLAN.json').read_text(encoding='utf-8'))
    files = CODE + [WORKER] + [pathlib.Path(x) for x in p['code']] + \
        [pathlib.Path(v['jobdir']) / f'{lab}.{x}' for lab, v in p['labels'].items() for x in ('job.npz', 'meta.json')]
    assert len({f.name for f in files}) == len(files), 'two uploaded files share a name'
    for name in names:
        if not (CD / 'pods' / name / 'pod.json').is_file():
            pv.create(name, GPU, dl, 'package C/D calibration (A10 sec. 2.6 double bootstrap)')
        nproc = int(ssh(name, 'nproc').strip())
        # the image's python3 is 3.10; numpy 2.5.4 needs 3.12 (the laptop venv's version): uv provides CPython 3.12 in a venv.
        # Skipped when an earlier run already installed it (resumable).
        check = 'P=$(cat /opt/calib/PY 2>/dev/null) && [ -n "$P" ] && $P -c "import sys,numpy,numba; print(sys.version.split()[0], numpy.__version__, numba.__version__)"'
        setup = ('mkdir -p /opt/calib/jobs /opt/calib/todo && cd /opt/calib && '
                 f'( python3 -m pip install -q uv && uv venv -q --clear -p 3.12 /opt/cv && uv pip install -q --python /opt/cv/bin/python {PINS} '
                 '&& echo /opt/cv/bin/python > PY ) > setup.log 2>&1; ' + check)
        have = pv.ssh(name, check, timeout=120)
        vers = have.stdout.strip() if have.returncode == 0 else ssh(name, setup, timeout=1500).strip()
        print(name, 'nproc', nproc, 'python/numpy/numba:', vers)
        if vers.split()[1:] != [x.split('==')[1] for x in PINS.split()]: raise SystemExit(f'{name}: numpy/numba versions differ: {vers}')
        lines = []
        for f in files:
            dest = '/opt/calib/' + f.name if f in (WORKER,) else '/opt/calib/jobs/' + f.name
            lines.append(f'put "{f}" "{dest}"')
        r = pv.sftp(name, lines)
        if r.returncode != 0: raise SystemExit(f'{name}: upload failed {r.stderr[-400:]}')
        remote = ssh(name, 'cd /opt/calib && sha256sum calib_worker_v13.sh jobs/*')
        got = {pathlib.PurePosixPath(l.split()[1]).name: l.split()[0] for l in remote.splitlines() if l.strip()}
        bad = [f.name for f in files if got.get(f.name) != sha(f)]
        if bad: raise SystemExit(f'{name}: uploaded files differ: {bad}')
        # start the pool only if it is not running; the launch is its own detached command (a trailing '&' after an '&&' list would
        # background the whole list in a subshell that keeps the SSH channel open: 20 Nov dry run)
        if pv.ssh(name, "pgrep -f '[c]alib_worker_v13.sh' > /dev/null", timeout=60).returncode != 0:
            ssh(name, f"cd /opt/calib; setsid nohup bash /opt/calib/calib_worker_v13.sh {nproc} > /opt/calib/workers.log 2>&1 < /dev/null & sleep 2; cat /opt/calib/workers.log", timeout=120)
        (CD / 'pods' / name / 'CALIB_UP').write_text(json.dumps(dict(nproc=nproc, files={f.name: sha(f) for f in files}, at=pv.est())), encoding='utf-8')
        print(name, 'workers started:', nproc)


def nproc_of(name):
    return json.loads((CD / 'pods' / name / 'CALIB_UP').read_text(encoding='utf-8'))['nproc']


def assign():
    td = RUN / 'tasks'; tasks = sorted(td.glob('*.task'))
    pods = [n for n in live_pods() if (CD / 'pods' / n / 'CALIB_UP').is_file()]
    if not tasks or not pods: print('nothing to assign', len(tasks), pods); return
    w = [nproc_of(n) for n in pods]; tot = sum(w)
    # interleave so every pod gets a mix of labels and seeds; quotas in proportion to vCPUs
    quota = [round(len(tasks) * x / tot) for x in w]; quota[-1] = len(tasks) - sum(quota[:-1])
    order = sorted(tasks, key=lambda p: (p.name.split('__')[2], p.name))
    i = 0
    for n, q in zip(pods, quota):
        mine = order[i:i + q]; i += q
        if not mine: continue
        ad = RUN / 'assigned' / n; ad.mkdir(parents=True, exist_ok=True)
        r = pv.sftp(n, [f'put "{t}" "/opt/calib/todo/{t.name}"' for t in mine])
        if r.returncode != 0: raise SystemExit(f'{n}: task upload failed {r.stderr[-300:]}')
        for t in mine: t.replace(ad / t.name)
        print(n, 'assigned', len(mine))


def pod_state(n):
    out = ssh(n, 'cd /opt/calib && for d in todo running done failed; do echo "$d $(ls $d | wc -l)"; done; ls done', timeout=120).split('\n')
    cnt = {l.split()[0]: int(l.split()[1]) for l in out[:4]}
    return cnt, [x for x in out[4:] if x.strip()]


def status():
    have = {p.name for p in (RUN / 'chunks').glob('*.npz')} if (RUN / 'chunks').exists() else set()
    allt = list((RUN / 'assigned').rglob('*.task')) + list((RUN / 'tasks').glob('*.task'))
    print(f'tasks {len(allt)}, unassigned {len(list((RUN / "tasks").glob("*.task")))}, chunk files fetched {len(have)}')
    for n in live_pods():
        try:
            cnt, _ = pod_state(n); print(n, 'vCPU', nproc_of(n), cnt)
        except Exception as e:
            print(n, 'status failed', type(e).__name__, str(e)[:200])


def chunk_name(task):          # lead_main__20261913__0000_0020.task -> lead_main_20261913_o0_20.npz
    lab, seed, rng = task[:-5].split('__'); lo, hi = rng.split('_')
    return f'{lab}_{seed}_o{int(lo)}_{int(hi)}.npz'


def steal():
    st = {n: pod_state(n)[0] for n in live_pods()}
    idle = [n for n, c in st.items() if c['todo'] == 0 and c['running'] < nproc_of(n)]
    for n in idle:
        donor = max(st, key=lambda m: st[m]['todo'])
        k = min(st[donor]['todo'] // 2, nproc_of(n) - st[n]['running'])
        if k <= 0: continue
        moved = ssh(donor, f'cd /opt/calib && for f in $(ls todo | tail -n {k}); do mv todo/$f stolen/$f 2>/dev/null && echo $f; done').split()
        if not moved: continue
        src = RUN / 'assigned' / donor; dst = RUN / 'assigned' / n; dst.mkdir(parents=True, exist_ok=True)
        r = pv.sftp(n, [f'put "{src / f}" "/opt/calib/todo/{f}"' for f in moved])
        if r.returncode != 0: raise SystemExit(f'{n}: task upload failed {r.stderr[-300:]}')
        for f in moved: (src / f).replace(dst / f)
        st[donor]['todo'] -= len(moved); st[n]['todo'] += len(moved)
        print(f'moved {len(moved)} queued tasks {donor} -> {n}')


def fetch():
    cdir = RUN / 'chunks'; cdir.mkdir(parents=True, exist_ok=True)
    for n in live_pods():
        _, done = pod_state(n)
        want = [chunk_name(t) for t in done if not (cdir / chunk_name(t)).is_file()]
        if not want: continue
        sums = dict(l.split()[::-1] for l in ssh(n, 'cd /opt/calib/jobs && sha256sum ' + ' '.join(want)).splitlines() if l.strip())
        tmp = cdir / 'incoming'; tmp.mkdir(exist_ok=True)
        r = pv.sftp(n, [f'get "/opt/calib/jobs/{w}" "{tmp / w}"' for w in want])
        if r.returncode != 0: print(n, 'fetch failed', r.stderr[-300:]); continue
        ok = 0
        for w in want:
            if sha(tmp / w) == sums[w]: (tmp / w).replace(cdir / w); ok += 1
            else: print(n, 'hash mismatch, will retry', w)
        print(n, 'fetched', ok, 'of', len(want))


def down():
    names = [a for a in ARGS[1:] if a.startswith(KPREFIX)] or live_pods()
    cdir = RUN / 'chunks'
    for n in names:
        cnt, done = pod_state(n)
        mine = [t.name for t in (RUN / 'assigned' / n).glob('*.task')] if (RUN / 'assigned' / n).exists() else []
        missing = [t for t in mine if not (cdir / chunk_name(t)).is_file()]
        if cnt['todo'] or cnt['running'] or cnt['failed'] or missing:
            print(n, 'not done:', cnt, 'missing chunk files', len(missing)); continue
        pv.delete(n, f'calibration: all {len(mine)} chunk files fetched and SHA-256 checked')


def requeue():
    for n in live_pods():
        out = ssh(n, 'cd /opt/calib && for f in $(ls failed); do tail -3 logs/$f.log; mv failed/$f todo/$f && echo REQUEUED $f; done')
        if out.strip(): print(n, out.strip()[-1500:])


def loop():
    """Every 5 min: requeue failed tasks once each, fetch, steal, delete finished pods; ends when no claude-v13cd-k pod is left."""
    log = RUN / 'loop.log'; seen_fail = set()
    def say(m):
        line = f'{pv.est()} {m}'; print(line, flush=True)
        with open(log, 'a', encoding='utf-8') as f: f.write(line + '\n')
    while live_pods():
        final = (RUN / 'ASSIGN_FINAL').is_file()          # pods are deleted only after the last labels were planned and assigned
        for step in ((fetch, steal, down) if final else (fetch, steal)):
            try: step()
            except Exception as e: say(f'{step.__name__} failed: {type(e).__name__} {str(e)[:200]}')
        for n in live_pods():
            try:
                cnt, _ = pod_state(n); say(f'{n} {cnt}')
                if cnt['failed']:
                    fl = ssh(n, 'ls /opt/calib/failed').split(); again = [f for f in fl if (n, f) in seen_fail]
                    if again: say(f'{n}: tasks failed twice, left in failed/: {again}')
                    for f in fl:
                        if (n, f) not in seen_fail:
                            seen_fail.add((n, f)); ssh(n, f'cd /opt/calib && tail -2 logs/{f}.log; mv failed/{f} todo/{f}'); say(f'{n}: requeued {f}')
            except Exception as e: say(f'{n} status failed: {type(e).__name__}')
        have = len(list((RUN / 'chunks').glob('*.npz'))) if (RUN / 'chunks').exists() else 0
        say(f'chunk files on the laptop: {have} of {len(list((RUN / "assigned").rglob("*.task")))} assigned')
        if live_pods(): time.sleep(300)
    say('loop done: no calibration pod left')


def final():
    """Mark that every label is planned and assigned: from now on `loop` deletes each pod once its chunks are fetched."""
    left = list((RUN / 'tasks').glob('*.task'))
    if left: raise SystemExit(f'{len(left)} tasks are not assigned yet; run assign first')
    (RUN / 'ASSIGN_FINAL').write_text(pv.est() + '\n', encoding='utf-8'); print('ASSIGN_FINAL written')


if __name__ == '__main__':
    dict(plan=plan, up=up, assign=assign, status=status, steal=steal, fetch=fetch, down=down, requeue=requeue, loop=loop,
         final=final)[ARGS[0]]()
