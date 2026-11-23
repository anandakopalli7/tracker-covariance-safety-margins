"""Crossing sprint (A11): the frozen crossing extractor on the capture pods (C's B7 on-pod path, tools\\b7_pods_v13.py). New file,
21 Nov 2026 (Claude Opus 5.5, session CD). Moves files and starts x_extract_v13.py on a pod; it computes no value and never opens a
fresh array (it hashes their bytes). Pods are created and deleted only through tools\\pods_v13.py (spend-log rows).

Usage (CD venv: .venv\\Scripts\\python.exe -I -B -X utf8 crossing\\x_pods_v13.py CMD NAME [...]):
  stage-code               build pods\\x_staging\\code_bundle.tar(.json): Codex tree, openloop modules of record, the shared tracker
                           library, x_extract_v13.py, and two old crossing runs (logs + stored arrays) for the acceptance test
  setup NAME               CPython 3.12 + the laptop venv's pins (uv), upload + verify the bundle, links, import check
  accept NAME              x_extract --test-old on the pod (old runs p2_c1109_tune_0002/0003): every compared key must equal the
                           stored arrays of record (A10 B0(b): bit-identical, or within 1e-12 with an equal NaN pattern; recorded)
  seal NAME                sealing check (A11 sec. 3.3): each pc13x_ archive equals its receipt; prints pass/fail counts only
  lock NAME                upload revision_v13\\LOCK_A11.txt and verify its SHA-256 on the pod (refuses if the lock does not exist)
  run NAME [WORKERS]       list the pod's pc13x_ archives with a CAPTURED_AND_REVIEWED receipt, start x_extract in the background
  status NAME              counts of finished arrays and errors on the pod (no value)
  fetch NAME               sha256 on the pod, download, extract into arrays_x\\CV0\\, verify every file (never overwrites)
"""
import hashlib, json, pathlib, sys, tarfile
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(CD / 'tools'))
import pods_v13 as pv                                   # noqa: E402
import b7_pods_v13 as BP                                # noqa: E402  (helpers only: bundle, walk, ssh, put, get, PINS, CODEX, P)

V13 = CD.parents[1]; WORK = CD.parent
STAGE = CD / 'pods' / 'x_staging'
R = '/root/xx'
PY = '/opt/b7py/bin/python'
RESULTS = '/opt/claude_v13_xlocal/results'
OUTR = '/opt/claude_v13_xlocal/xx_out'
RUNSR = '/opt/claude_v13_xlocal/xx_runs'
OLD = ('p2_c1109_tune_0002_fixed_c1', 'p2_c1109_tune_0003_fixed_c1')
LINKS = {r'<library folder>': R + '/P',
         r'<library folder>\149_supported_sensor_preparation_20261101': R + '/codex'}
ENV = ('export V13_CODEX_ROOT=%s/codex V13_P_ROOT=%s/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 '
       'MKL_NUM_THREADS=1 NUMBA_NUM_THREADS=1' % (R, R))
XE = R + '/ARS_TRIAL/revision_v13/work/CD_capture/crossing/x_extract_v13.py'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def verify_remote(name, manifest_path):
    man = json.loads(manifest_path.read_text(encoding='utf-8'))['files']
    lst = STAGE / (manifest_path.stem + '.sha256.txt')
    lst.write_text(''.join('%s  %s\n' % (h, a) for a, h in man.items()), encoding='ascii', newline='\n')
    BP.put(name, lst, R + '/' + lst.name)
    out = BP.ssh(name, 'cd %s && sha256sum -c --quiet %s > %s.check 2>&1; echo rc=$?' % (R, lst.name, lst.name))
    if 'rc=0' not in out: raise SystemExit('%s: sha256 check of %s failed: %s' % (name, manifest_path.name, out[-500:]))
    return len(man)


def stage_code():
    STAGE.mkdir(parents=True, exist_ok=True)
    junk = lambda p: '__pycache__' in p.parts or p.suffix in ('.pyc', '.nbi', '.nbc') or p.name.startswith('tmp')
    m = []
    for sub in ('code', 'sources', 'vendor', 'legacy86/vendor/nuscenes-devkit/python-sdk', 'contracts'):
        m += BP.walk(BP.CODEX / sub, 'codex/' + sub, junk)
    m += [(BP.P / '09_redesign' / 'm2_decisions' / 'openloop' / f, 'P/09_redesign/m2_decisions/openloop/' + f) for f in BP.OPENLOOP]
    m += [(BP.P / '11_ojits' / 'A6R' / 'code' / 'optA_lib_v02.py', 'P/11_ojits/A6R/code/optA_lib_v02.py')]
    for rid in OLD:                                   # the run's SUMMARY and its capture folder's .json/.jsonl files (no sweeps, no review)
        rd = BP.P / '08_phase2' / 'archives_c1' / rid / 'x' / rid; arc = 'P/08_phase2/archives_c1/%s/x/%s' % (rid, rid)
        cap = next(p for p in (rd / 'capture').iterdir() if p.is_dir())
        m += [(rd / 'SUMMARY.json', arc + '/SUMMARY.json')]
        m += [(f, '%s/capture/%s/%s' % (arc, cap.name, f.name)) for f in sorted(cap.iterdir()) if f.is_file() and f.suffix in ('.json', '.jsonl')]
        m += [(BP.P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01' / (rid + '.npz'),
               'P/09_redesign/m2_decisions/openloop/gateR_rt_v01/%s.npz' % rid)]
    m += BP.walk(WORK / 'shared' / 'trackers', 'ARS_TRIAL/revision_v13/work/shared/trackers', junk)
    m += [(HERE / 'x_extract_v13.py', 'ARS_TRIAL/revision_v13/work/CD_capture/crossing/x_extract_v13.py')]
    ps = STAGE / 'pod_links_x.py'
    ps.write_text('import os, json\nL = %s\nos.makedirs(%r, exist_ok=True)\nos.chdir(%r)\nfor k, v in L.items():\n'
                  '    if not os.path.islink(k): os.symlink(v, k)\nprint(json.dumps({k: os.path.realpath(k) for k in L}))\n'
                  % (json.dumps(LINKS), R + '/job', R + '/job'), encoding='utf-8')
    m += [(ps, 'pod_links_x.py')]
    man = BP.bundle(STAGE / 'code_bundle.tar', m)
    print('code bundle: %d files, %.1f MB' % (len(man), (STAGE / 'code_bundle.tar').stat().st_size / 1e6))


def setup(name):
    check = '%s -c "import sys,numpy,numba,scipy; print(sys.version.split()[0], numpy.__version__, numba.__version__)"' % PY
    have = pv.ssh(name, check, timeout=120)
    if have.returncode != 0:
        BP.ssh(name, '( python3 -m pip install -q uv && uv venv -q --clear -p 3.12 /opt/b7py && uv pip install -q --python %s %s ) > /root/xx_setup.log 2>&1; '
                     'tail -3 /root/xx_setup.log' % (PY, BP.PINS), timeout=2400)
        have = pv.ssh(name, check, timeout=120)
    vers = have.stdout.strip()
    if have.returncode != 0 or vers.split()[1:] != ['2.5.4', '0.68.1']: raise SystemExit('%s: environment not ready: %s' % (name, vers))
    BP.ssh(name, 'mkdir -p %s' % R)
    BP.put(name, STAGE / 'code_bundle.tar', R + '/code_bundle.tar')
    BP.ssh(name, 'cd %s && tar xf code_bundle.tar && rm -f code_bundle.tar' % R)
    n = verify_remote(name, STAGE / 'code_bundle.json')
    links = BP.ssh(name, 'cd %s && /usr/bin/env python3 pod_links_x.py' % R)
    imp = BP.ssh(name, '%s && cd %s/job && %s -I -B -X utf8 -c "import sys; sys.path.insert(0, \'%s\'); import x_extract_v13 as X; '
                       'import trk_env_v01 as e; e.setup(); import trk_arrays_v01; print(e.STATE)"' % (ENV, R, PY, XE.rsplit('/', 1)[0]), timeout=600)
    rec = dict(python_numpy_numba=vers, code_files_verified=n, links=json.loads(links.strip().splitlines()[-1]), import_check=imp.strip()[-400:], at=pv.est())
    (CD / 'pods' / name).mkdir(parents=True, exist_ok=True)
    (CD / 'pods' / name / 'X_SETUP.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print(json.dumps(rec))


def accept(name):
    out = BP.ssh(name, '%s && cd %s/job && %s -I -B -X utf8 %s --test-old --runs %s > %s/testold.log 2>&1; echo rc=$?; cat %s/testold.log'
                 % (ENV, R, PY, XE, ','.join(OLD), R, R), timeout=1800)
    if 'rc=0' not in out: raise SystemExit('%s: acceptance run failed: %s' % (name, out[-800:]))
    rows = [json.loads(l) for l in out.splitlines() if l.startswith('{"run"')]
    worst = max((v.get('max_abs', 0.) for r in rows for v in r['compare'].values()), default=0.)
    ident = all(v.get('n_diff') == 0 and v.get('same_nan') for r in rows for v in r['compare'].values())
    ok = len(rows) == len(OLD) and all(v.get('same_nan') and 'shape' not in v and v.get('max_abs', 1.) <= 1e-12 for r in rows for v in r['compare'].values())
    rec = dict(rows=rows, bit_identical=ident, max_abs=worst, accepted=ok, rule='A10 B0(b): within 1e-12, equal NaN pattern', at=pv.est())
    (CD / 'pods' / name / 'X_ACCEPT.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print(json.dumps(dict(accepted=ok, bit_identical=ident, max_abs=worst)))
    if not ok: raise SystemExit('%s: acceptance failed' % name)


def lock(name):
    lk = V13 / 'LOCK_A11.txt'
    if not lk.is_file(): raise SystemExit('REFUSED: LOCK_A11.txt does not exist')
    BP.put(name, lk, R + '/LOCK_A11.txt')
    h = BP.ssh(name, 'sha256sum %s/LOCK_A11.txt' % R).split()[0]
    if h != sha(lk): raise SystemExit('%s: lock file differs on the pod' % name)
    (CD / 'pods' / name / 'X_LOCK.json').write_text(json.dumps(dict(lock_sha256=h, at=pv.est())), encoding='utf-8')
    print('lock on the pod', h)


SEAL_PY = r'''
import hashlib, json, pathlib
R = pathlib.Path(%r); ok = []; bad = []
for d in sorted(R.glob('pc13x_*')):
    a = d / ('claude_main_%%s.tar.gz' %% d.name); rp = d / ('claude_main_%%s.tar.gz.receipt.json' %% d.name)
    if not (a.is_file() and rp.is_file()): bad.append([d.name, 'no archive or receipt']); continue
    r = json.loads(rp.read_text()); h = hashlib.sha256()
    with open(a, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    why = [w for w, c in (('sha256', r.get('sha256') == h.hexdigest()), ('bytes', r.get('bytes') == a.stat().st_size),
                          ('status', r.get('status') == 'CAPTURED_AND_REVIEWED'), ('keep_raw', r.get('keep_raw') is False)) if not c]
    (bad.append([d.name, ','.join(why)]) if why else ok.append(d.name))
print(json.dumps(dict(passed=len(ok), failed=len(bad), failed_runs=bad)))
'''


def seal(name):
    """A11 sec. 3.3 / A10 sec. 5.2 sealing check on the pod: each pc13x_ archive equals its receipt (SHA-256, bytes), status
    CAPTURED_AND_REVIEWED, keep_raw false. Prints pass/fail counts and the failing run ids only; reads no content of a run."""
    out = BP.ssh(name, "python3 - <<'PYEOF'\n%s\nPYEOF" % (SEAL_PY % RESULTS), timeout=1800)
    rec = json.loads(out.strip().splitlines()[-1]); rec['at'] = pv.est()
    (CD / 'pods' / name).mkdir(parents=True, exist_ok=True)
    (CD / 'pods' / name / 'X_SEAL.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print(json.dumps(dict(pod=name, passed=rec['passed'], failed=rec['failed'], failed_runs=rec['failed_runs'])))


def run(name, workers=6):
    h = json.loads((CD / 'pods' / name / 'X_LOCK.json').read_text(encoding='utf-8'))['lock_sha256']
    acc = json.loads((CD / 'pods' / name / 'X_ACCEPT.json').read_text(encoding='utf-8'))
    if not acc['accepted']: raise SystemExit('REFUSED: the pod did not pass the acceptance test')
    BP.ssh(name, 'cd %s && for d in pc13x_*; do r=$d/claude_main_$d.tar.gz.receipt.json; [ -f $r ] && grep -q CAPTURED_AND_REVIEWED $r && echo $d; done '
                 '> %s/ids.txt; wc -l < %s/ids.txt' % (RESULTS, R, R))
    BP.ssh(name, '%s && cd %s/job && (setsid nohup %s -I -B -X utf8 %s --archive-root %s --runs-root %s --out-root %s --ids %s/ids.txt --workers %d '
                 '--lock %s/LOCK_A11.txt --lock-sha %s > %s/run.log 2>&1 < /dev/null &) ; sleep 2; echo started'
           % (ENV, R, PY, XE, RESULTS, RUNSR, OUTR, R, int(workers), R, h, R))
    print('started', name, pv.est())


def status(name):
    out = BP.ssh(name, 'echo ids=$(wc -l < %s/ids.txt) npz=$(ls %s/CV0/*.npz 2>/dev/null | grep -v partial | wc -l) '
                       'errors=$(grep -ci error %s/run.log || true) running=$(pgrep -fc x_extract_v13 || true); tail -2 %s/run.log' % (R, OUTR, R, R))
    print(out.strip()); return out


def fetch(name):
    dest = CD / 'arrays_x'
    BP.ssh(name, 'cd %s && sha256sum CV0/*.npz > SHA_X.txt && tar cf %s/arrays_x.tar CV0/*.npz SHA_X.txt X_EXTRACT_*.json' % (OUTR, R), timeout=1800)
    loc = STAGE / ('arrays_x_%s.tar' % name)
    BP.get(name, '%s/arrays_x.tar' % R, str(loc))
    with tarfile.open(loc) as t:
        shas = dict(reversed(l.split()) for l in t.extractfile('SHA_X.txt').read().decode().splitlines())
        ids = [x.strip() for x in BP.ssh(name, 'cat %s/ids.txt' % R).split()]
        exp = ['CV0/%s.npz' % r for r in ids]
        miss = [x for x in exp if x not in shas]
        if miss: raise SystemExit('%s: %d arrays missing on the pod, e.g. %s' % (name, len(miss), miss[:3]))
        exists = [x for x in exp if (dest / x).exists()]
        if exists: raise SystemExit('REFUSED: %d target files exist in arrays_x (never overwrite), e.g. %s' % (len(exists), exists[:3]))
        for m in t.getmembers():
            if m.name in exp or m.name.startswith('X_EXTRACT_'):
                assert m.isfile() and '..' not in m.name
                t.extract(m, dest if m.name in exp else CD / 'pods' / name, filter='data')
    bad = [x for x in exp if sha(dest / x) != shas[x]]
    if bad: raise SystemExit('%s: %d downloaded arrays differ from the pod sha256: %s' % (name, len(bad), bad[:3]))
    rec = dict(n_files=len(exp), all_sha256_verified=True, files={x: shas[x] for x in exp}, tar_sha256=sha(loc), fetched=pv.est())
    (CD / 'pods' / name / 'X_FETCH.json').write_text(json.dumps(rec, indent=0), encoding='utf-8')
    loc.unlink()
    print('%s: %d arrays downloaded into arrays_x\\CV0, all sha256 verified' % (name, len(exp)))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'stage-code': stage_code()
    elif cmd == 'setup': setup(sys.argv[2])
    elif cmd == 'accept': accept(sys.argv[2])
    elif cmd == 'lock': lock(sys.argv[2])
    elif cmd == 'seal': seal(sys.argv[2])
    elif cmd == 'run': run(sys.argv[2], *(sys.argv[3:4]))
    elif cmd == 'status': status(sys.argv[2])
    elif cmd == 'fetch': fetch(sys.argv[2])
    else: raise SystemExit(__doc__)
