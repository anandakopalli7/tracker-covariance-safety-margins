r"""AMENDMENT_12 sec. 5b, the remaining steps after the stop of 22 Nov 03:49 EST (notes\FN5B_RECORDS_ADD02.md). New file, 22 Nov 2026
(Claude Opus 5.5, worker of package F). It computes no value; it moves files, runs the gate test and starts code\fn_run_score_v02.sh
once (scoring only, fn06_score_v02.py, on the masked tracks and arrays already made on pod claude-v13f-n03). Frozen modules are imported
read only: code\fn_pods_v01.py (bundle, upload, fetch, pod set-up) and post\fn_post_v01.py (values).
  preflight [--need-add02]  FREEZE_F_NUS5B (35 entries) and, if present (required with --need-add02), FREEZE_F_NUS5B_ADD02 match their
                            files; both locks exist; every local masked track and array file equals the SHA-256 recorded when it was
                            fetched from claude-v13f-n03 (pods\claude-v13f-n03\FN_FETCH_*.json); the code / val / locks bundles match
  stage                     pods\masked_bundle.tar.gz (cache\tracks_masked\val and cache\arrays_masked\val, 300 files) and
                            pods\score2_bundle.tar.gz (code\fn06_score_v02.py, code\fn_run_score_v02.sh), each with a SHA-256 manifest
  up NAME                   create the pod (fpods_n via fn_pods.up: spend-log row, local deadline watchdog 3 h, both environments,
                            the code bundle SHA-checked), then upload the val, masked and score2 bundles, each SHA-checked on the pod
  gate-test NAME            with NO lock on the pod: fn06_score_v02.py prep masked val and the runner must both REFUSE, and no
                            scoring output may exist afterwards
  locks NAME                upload LOCK_A12c.txt and LOCK_A12e.txt (pods\locks_bundle), SHA-checked; print their SHA-256 on the pod
  start NAME                (needs FREEZE_F_NUS5B_ADD02 verified) start the runner once; log /root/fn/score_v02.log
  status NAME [--copy]      tail of the log; --copy puts it into logs\score_v02_run.log for the fetch
  fetch NAME                out\masked_val and logs, every file SHA-256 checked (fn_pods.fetch)
  values                    out\FN5B_VALUES_v01.json from out\masked_val\FN5B_RESULTS_v01.json (fn_post_v01.values, unchanged)
Usage: python -I -B fn_post_v02.py CMD ...
"""
import hashlib, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
HOME = HERE.parent
V13 = HOME.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(HOME / 'code'))
sys.path.insert(0, str(HERE))
import fn_pods_v01 as FP                               # noqa: E402  (frozen; read only)
import fn_post_v01 as P1                               # noqa: E402  (frozen; read only)

LOG = FP.R + '/score_v02.log'
FREEZE = V13 / 'work' / 'locks' / 'FREEZE_F_NUS5B.json'
ADD02 = V13 / 'work' / 'locks' / 'FREEZE_F_NUS5B_ADD02.json'
SETS = ('tracks_masked', 'arrays_masked')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def check_freeze(path):
    fz = json.loads(path.read_text(encoding='utf-8'))
    ents = fz['entries']
    bad = [e['path'] for e in ents if sha(V13 / e['path']) != e['sha256']]
    return len(ents), bad


def preflight(need_add02=False):
    rep = {}
    rep['freeze'] = check_freeze(FREEZE)
    if ADD02.is_file():
        rep['add02'] = check_freeze(ADD02)
    elif need_add02:
        raise SystemExit('REFUSED: %s does not exist' % ADD02)
    rep['locks'] = {l: (sha(V13 / l) if (V13 / l).is_file() else None) for l in P1.LOCKS}
    fetched = {}
    for s in SETS:
        rec = json.loads((FP.pv.PODS / 'claude-v13f-n03' / ('FN_FETCH_cache_%s_val.json' % s)).read_text(encoding='utf-8'))
        files = rec['files']
        bad = [k for k, h in files.items() if sha(HOME / k) != h]
        local = sorted(p.name for p in (HOME / 'cache' / s / 'val').glob('*.npz'))
        fetched[s] = dict(n_recorded=len(files), n_local=len(local), mismatches=bad)
    rep['masked_files'] = fetched
    for b in ('code', 'val', 'locks', 'masked', 'score2'):
        mf = FP.STAGE / ('%s_bundle.json' % b)
        if mf.is_file():
            rep['bundle_' + b] = sha(FP.STAGE / ('%s_bundle.tar.gz' % b)) == json.loads(mf.read_text(encoding='utf-8'))['tar_sha256']
    print(json.dumps(rep, indent=0))
    ok = (not rep['freeze'][1] and (not ADD02.is_file() or not rep['add02'][1]) and all(rep['locks'].values())
          and all(not v['mismatches'] and v['n_recorded'] == 150 and v['n_local'] == 150 for v in fetched.values())
          and all(v for k, v in rep.items() if k.startswith('bundle_')))
    if not ok:
        raise SystemExit('PREFLIGHT FAILED')
    return rep


def stage():
    preflight()
    m = []
    for s in SETS:
        fs = sorted(p for p in (HOME / 'cache' / s / 'val').glob('scene-*.npz') if '.tmp' not in p.name)
        assert len(fs) == 150, (s, len(fs))
        m += [(f, FP.A13 + 'work/F_dropout_nus/cache/%s/val/%s' % (s, f.name)) for f in fs]
    FP.bundle(FP.STAGE / 'masked_bundle.tar.gz', m)
    FP.bundle(FP.STAGE / 'score2_bundle.tar.gz', [(HOME / 'code' / f, FP.A13 + 'work/F_dropout_nus/code/' + f)
                                                  for f in ('fn06_score_v02.py', 'fn_run_score_v02.sh')])


def up(name):
    preflight()
    FP.up(name, 'NVIDIA GeForce RTX 4090', 3.0)
    for b in ('val', 'masked', 'score2'):
        FP.upload(name, b)


def gate_test(name):
    has = FP.pv.ssh(name, 'ls %s/ARS_TRIAL/revision_v13/LOCK_A12c.txt %s/ARS_TRIAL/revision_v13/LOCK_A12e.txt 2>/dev/null | wc -l'
                    % (FP.R, FP.R), timeout=60).stdout.strip()
    if has != '0':
        raise SystemExit('gate test needs a pod without the locks (found %s)' % has)
    r1 = FP.pv.ssh(name, '%s && cd %s/job && /opt/fnk/bin/python -I -B -X utf8 %s/code/fn06_score_v02.py prep masked val 2>&1 | tail -n 2; '
                         'echo rc=${PIPESTATUS[0]}' % (FP.ENV, FP.R, FP.HN), timeout=300).stdout
    r2 = FP.pv.ssh(name, '%s && cd %s/job && bash %s/code/fn_run_score_v02.sh 2>&1 | tail -n 2; echo rc=${PIPESTATUS[0]}'
                   % (FP.ENV, FP.R, FP.HN), timeout=300).stdout
    r3 = FP.pv.ssh(name, 'ls %s/out/masked_val 2>/dev/null | wc -l' % FP.HN, timeout=60).stdout.strip()
    ok = ('REFUSED' in r1 and 'rc=0' not in r1 and 'REFUSED' in r2 and 'rc=0' not in r2 and r3 == '0')
    rec = dict(prep=r1.strip(), runner=r2.strip(), scoring_files_after=r3, passed=ok, at=FP.pv.est())
    (FP.pv.PODS / name / 'GATE_TEST_v02.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print(json.dumps(rec, indent=1))
    if not ok:
        raise SystemExit('GATE TEST FAILED')


def locks(name):
    FP.upload(name, 'locks')
    print(FP.ssh(name, 'sha256sum %s/ARS_TRIAL/revision_v13/LOCK_A12c.txt %s/ARS_TRIAL/revision_v13/LOCK_A12e.txt' % (FP.R, FP.R)))


def start(name):
    preflight(need_add02=True)
    gt = FP.pv.PODS / name / 'GATE_TEST_v02.json'
    if not gt.is_file() or not json.loads(gt.read_text(encoding='utf-8'))['passed']:
        raise SystemExit('REFUSED: no passed gate test on this pod')
    if 'NEW' not in FP.pv.ssh(name, 'test -e %s && echo EXISTS || echo NEW' % LOG, timeout=60).stdout:
        raise SystemExit('REFUSED: the run log exists; the run is made once')
    FP.ssh(name, '%s && cd %s/job && (setsid nohup bash %s/code/fn_run_score_v02.sh > %s 2>&1 < /dev/null &) ; sleep 2; echo started'
           % (FP.ENV, FP.R, FP.HN, LOG))
    print('started fn_run_score_v02.sh', FP.pv.est())


def status(name, copy=False):
    print(FP.ssh(name, 'tail -n 8 %s | cut -c1-400; ls %s/out/masked_val 2>/dev/null; uptime' % (LOG, FP.HN)))
    if copy:
        FP.ssh(name, 'cp %s %s/logs/score_v02_run.log' % (LOG, FP.HN))
        print('copied the run log into logs/')


if __name__ == '__main__':
    a = sys.argv[1:]
    c = a[0]
    if c == 'preflight': preflight('--need-add02' in a)
    elif c == 'stage': stage()
    elif c == 'up': up(a[1])
    elif c == 'gate-test': gate_test(a[1])
    elif c == 'locks': locks(a[1])
    elif c == 'start': start(a[1])
    elif c == 'status': status(a[1], '--copy' in a)
    elif c == 'fetch':
        FP.fetch(a[1], 'out/masked_val'); FP.fetch(a[1], 'logs')
    elif c == 'values': P1.values()
    else: raise SystemExit('unknown command')
