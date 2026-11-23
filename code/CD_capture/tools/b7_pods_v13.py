"""B7 re-tracking on a RunPod pod (revision v13, package C; 20 Nov 2026, Claude Opus 5.5). Executes tools\\trk_pod_plan_v13.md.
This file only moves files and starts the frozen extractor (analysis\\x_trk_extract_v13.py) on the pod; it computes no value and never
opens a fresh array (it hashes their bytes). Pods are created and deleted only through tools\\pods_v13.py (spend-log rows).

Usage (CD venv: .venv\\Scripts\\python.exe -I -B -X utf8 tools\\b7_pods_v13.py CMD NAME [...]):
  stage-code                 build pods\\b7_staging\\code_bundle.tar(.json) (code + the 0037 acceptance data)
  setup NAME                 install CPython 3.12 + the laptop venv's pins (uv), upload and verify the code bundle, make the 5 links
  accept NAME                run --test-old (0037) on the pod; download the 8 arrays; compare with analysis\\out\\testold_b7_arrays_final
  stage-fresh FAMILY         build pods\\b7_staging\\fresh_<family>.tar (+ .json sha manifest): per run SUMMARY.json, LOGS_OK, the four
                             capture files, b7\\<rid>\\ files; plus LOCK_A10_2.txt, LOCK_A10_2c.txt (refuses unless all 105 have LOGS_OK)
  upload-fresh NAME FAMILY   upload and verify the fresh bundle (sha256 of every file on the pod)
  run NAME FAMILY [WORKERS]  start the extractor on the pod in the background (family arrays to /root/b7/out)
  status NAME FAMILY         counts of finished / error files on the pod (no value)
  fetch NAME FAMILY          sha256 on the pod, download, extract into arrays\\, verify each file's sha256 (never overwrites)
"""
import hashlib, json, os, pathlib, sys, tarfile, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(CD / 'analysis'))
import pods_v13 as pv                                   # noqa: E402

DL = pathlib.Path(r'<user folder>')
CODEX = DL / '<earlier-phase folder 2>' / '149_supported_sensor_preparation_20261101'
P = DL / '<earlier-phase folder 1>'
V13 = DL / 'ARS_TRIAL' / 'revision_v13'
WORK = V13 / 'work'
STAGE = CD / 'pods' / 'b7_staging'
R = '/root/b7'
PY = '/opt/b7py/bin/python'
PINS = ('numpy==2.5.4 numba==0.68.1 llvmlite==0.50.0 scipy==1.18.1 pandas==2.2.2 matplotlib==3.11.2 opencv-python-headless==4.14.0.94 '
        'scikit-learn==1.9.1 pillow==13.0.0 PyYAML==6.0.2 cloudpickle==3.1.2 joblib==1.6.0 tqdm==4.70.1 psutil==7.0.0 cachetools==7.3.0 '
        'threadpoolctl==3.8.0 contourpy==1.4.0 kiwisolver==1.5.1 fonttools==4.68.0 cycler==0.12.1 pyparsing==3.3.3 '
        'python-dateutil==2.9.0.post0 pytz==2024.1 tzdata==2024.1 packaging==24.2 six==1.16.0 narwhals==2.28.0 cffi==2.1.1 pycparser==2.22 '
        'charset-normalizer==3.4.1')                    # = analysis\out\VENV_FREEZE.txt for every package a B7 job imports
OPENLOOP = ['olcore_v01.py', 'olcore_rt_v01.py', 'ol_gateR_core_v01.py', 'ol_gateR_rt_extract_v01.py', 'ol_extract_v01.py',
            'ox12_core_v01.py', 'oxsb_core_v01.py', 'pbar_tuning_v01.json']
LINKS = {r'<library folder>\openloop': R + '/P/09_redesign/m2_decisions/openloop',
         r'<library folder>': R + '/P',
         r'ARS_TRIAL\revision_v12\analysis': R + '/ARS_TRIAL/revision_v12/analysis',
         r'ARS_TRIAL\revision_v11\analysis': R + '/ARS_TRIAL/revision_v11/analysis',
         r'<library folder>\149_supported_sensor_preparation_20261101': R + '/codex'}
ENV = ('export V13_CODEX_ROOT=%s/codex V13_P_ROOT=%s/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 '
       'MKL_NUM_THREADS=1 NUMBA_NUM_THREADS=1 NUMBA_CACHE_DIR=%s/numba_cache' % (R, R, R))
XT = R + '/ARS_TRIAL/revision_v13/work/CD_capture/analysis/x_trk_extract_v13.py'
COMBOS = ['%s_%d_%s' % ('{p}', r, L) for r, L in ((2, '0'), (2, '0.1'), (5, '0'), (5, '0.1'), (5, '0.2'), (10, '0'), (10, '0.1'), (10, '0.2'))]
PREFIX = {'lead_braking': 'B7', 'cutin': 'B7CI'}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def ssh(name, cmd, timeout=1800):
    r = pv.ssh(name, cmd, timeout=timeout)
    if r.returncode != 0:
        raise SystemExit('%s: remote command failed rc=%d: %s\n%s' % (name, r.returncode, cmd[:200], (r.stdout + r.stderr)[-1500:]))
    return r.stdout


def put(name, local, remote):
    r = pv.sftp(name, ['put "%s" "%s"' % (local, remote)])
    if r.returncode != 0: raise SystemExit('%s: upload of %s failed: %s' % (name, local, r.stderr[-600:]))


def get(name, remote, local):
    r = pv.sftp(name, ['get "%s" "%s"' % (remote, local)])
    if r.returncode != 0: raise SystemExit('%s: download of %s failed: %s' % (name, remote, r.stderr[-600:]))


def bundle(path, members):
    """members: list of (local file, arcname). Plain tar (the npz/json are written as they are) + a sha manifest."""
    man = {}
    with tarfile.open(path, 'w') as t:
        for f, arc in members:
            t.add(str(f), arcname=arc, recursive=False); man[arc] = sha(f)
    (path.with_suffix('.json')).write_text(json.dumps(dict(files=man, n=len(man), tar_sha256=sha(path), written=pv.est()), indent=0), encoding='utf-8')
    return man


def walk(root, arcroot, skip=lambda p: False):
    out = []
    for p in sorted(root.rglob('*')):
        if p.is_file() and not skip(p):
            out.append((p, arcroot + '/' + p.relative_to(root).as_posix()))
    return out


def stage_code():
    STAGE.mkdir(parents=True, exist_ok=True)
    junk = lambda p: '__pycache__' in p.parts or p.suffix in ('.pyc', '.nbi', '.nbc') or p.name.startswith('tmp')
    m = []
    for sub in ('code', 'sources', 'vendor', 'legacy86/vendor/nuscenes-devkit/python-sdk', 'contracts'):
        m += walk(CODEX / sub, 'codex/' + sub, junk)
    m += [(P / '09_redesign' / 'm2_decisions' / 'openloop' / f, 'P/09_redesign/m2_decisions/openloop/' + f) for f in OPENLOOP]
    m += [(P / '11_ojits' / 'A6R' / 'code' / 'optA_lib_v02.py', 'P/11_ojits/A6R/code/optA_lib_v02.py')]
    a37 = P / '07_fit_runs' / 'archives' / 'p1b_fit_finite_0037'; c37 = a37 / 'x' / 'p1b_fit_finite_0037' / 'capture' / 'fit_finite_0037'
    m += [(a37 / 'SUMMARY.json', 'P/07_fit_runs/archives/p1b_fit_finite_0037/SUMMARY.json')]
    m += [(c37 / f, 'P/07_fit_runs/archives/p1b_fit_finite_0037/x/p1b_fit_finite_0037/capture/fit_finite_0037/' + f)
          for f in ('contract.json', 'evaluation_truth.jsonl', 'frames.jsonl', 'scenario_frames.jsonl')]
    m += [(DL / 'ARS_TRIAL' / 'revision_v11' / 'analysis' / 'rev_common_v01.py', 'ARS_TRIAL/revision_v11/analysis/rev_common_v01.py'),
          (DL / 'ARS_TRIAL' / 'revision_v12' / 'analysis' / 'a9_common_v01.py', 'ARS_TRIAL/revision_v12/analysis/a9_common_v01.py')]
    m += walk(WORK / 'shared' / 'trackers', 'ARS_TRIAL/revision_v13/work/shared/trackers', junk)
    m += [(CD / 'analysis' / f, 'ARS_TRIAL/revision_v13/work/CD_capture/analysis/' + f) for f in ('x_trk_extract_v13.py', 'cd_common_v13.py', 'gl_fast_v13.py')]
    m += [(CD / f, 'ARS_TRIAL/revision_v13/work/CD_capture/' + f) for f in ('CASES_C_v13.json', 'REPLACEMENTS_C_v13.json') if (CD / f).is_file()]
    m += [(CD / 'b7' / 'p1b_fit_finite_0037' / f, 'ARS_TRIAL/revision_v13/work/CD_capture/b7/p1b_fit_finite_0037/' + f)
          for f in ('b7_detections_v13.jsonl', 'B7_MANIFEST_v13.json')]
    # the pod-side set-up script: links named literally after the Windows paths (CD_DEFINITIONS / trk_pod_plan sec. 3)
    ps = STAGE / 'pod_links_b7.py'
    ps.write_text('import os, json\nL = %s\nos.makedirs(%r, exist_ok=True)\nos.chdir(%r)\nfor k, v in L.items():\n'
                  '    if not os.path.islink(k): os.symlink(v, k)\nprint(json.dumps({k: os.path.realpath(k) for k in L}))\n'
                  % (json.dumps(LINKS), R + '/job', R + '/job'), encoding='utf-8')
    m += [(ps, 'pod_links_b7.py')]
    man = bundle(STAGE / 'code_bundle.tar', m)
    print('code bundle: %d files, %.1f MB' % (len(man), (STAGE / 'code_bundle.tar').stat().st_size / 1e6))


def verify_remote(name, manifest_path, base=R):
    man = json.loads(manifest_path.read_text(encoding='utf-8'))['files']
    lst = STAGE / (manifest_path.stem + '.sha256.txt')
    lst.write_text(''.join('%s  %s\n' % (h, a) for a, h in man.items()), encoding='ascii', newline='\n')
    put(name, lst, base + '/' + lst.name)
    out = ssh(name, 'cd %s && sha256sum -c --quiet %s > %s.check 2>&1; echo rc=$?; grep -c . %s.check || true' % (base, lst.name, lst.name, lst.name))
    if 'rc=0' not in out: raise SystemExit('%s: sha256 check of %s failed: %s' % (name, manifest_path.name, out[-500:]))
    return len(man)


def setup(name):
    nproc = int(ssh(name, 'nproc').strip())
    check = '%s -c "import sys,numpy,numba,scipy,pandas,matplotlib,cv2,sklearn,PIL,yaml; print(sys.version.split()[0], numpy.__version__, numba.__version__)"' % PY
    have = pv.ssh(name, check, timeout=120)
    if have.returncode != 0:
        ssh(name, '( python3 -m pip install -q uv && uv venv -q --clear -p 3.12 /opt/b7py && uv pip install -q --python %s %s ) > /root/b7_setup.log 2>&1; '
                  'tail -3 /root/b7_setup.log' % (PY, PINS), timeout=2400)
        have = pv.ssh(name, check, timeout=120)
    vers = have.stdout.strip()
    if have.returncode != 0 or vers.split()[1:] != ['2.5.4', '0.68.1']:
        raise SystemExit('%s: environment not ready: %s %s' % (name, vers, have.stderr[-800:]))
    ssh(name, 'mkdir -p %s' % R)
    put(name, STAGE / 'code_bundle.tar', R + '/code_bundle.tar')
    ssh(name, 'cd %s && tar xf code_bundle.tar' % R)
    n = verify_remote(name, STAGE / 'code_bundle.json')
    links = ssh(name, 'cd %s && /usr/bin/env python3 pod_links_b7.py' % R)
    imp = ssh(name, '%s && cd %s/job && %s -I -B -X utf8 -c "import sys; sys.path.insert(0, \'%s\'); import x_trk_extract_v13 as X, trk_tracker_v01, '
                    'trk_arrays_v01, trk_score_v01; import trk_env_v01 as e; print(e.STATE)"' % (ENV, R, PY, XT.rsplit('/', 1)[0]), timeout=600)
    rec = dict(nproc=nproc, python_numpy_numba=vers, code_files_verified=n, links=json.loads(links.strip().splitlines()[-1]), import_check=imp.strip()[-400:],
               at=pv.est())
    (CD / 'pods' / name / 'B7_SETUP.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print(json.dumps(rec))


# Amended acceptance rule (CD lead, 20 Nov ~06:30 EST; A10 sec. 11 departure recorded in B7_POD_RUN_v13.json): bit-identical on every key
# that c_b7_v13.py / c_b7ci_v13.py read for a value (grep of both programs), every other key within 1e-12 absolute with an equal
# finite/NaN pattern: A10 B0(b)'s tolerance for rebuilt arrays ("Arrays rebuilt from the replayed actor lists reproduce the stored ones
# (critical scales of F0, N, E, NA, CK3, AM, Q; ...) ... Within 1e-12"), which covers AM (cA1) and Q (cQ). Settled by the coordinator,
# 20 Nov ~06:40 EST (first amended at ~06:30 with B0(a)'s 1e-14, which attempt 1 did not meet: max 1.42e-14). The original rule
# (bit-identical on all keys) is still evaluated and recorded.
READ_KEYS = ['k', 'idx55', 'evaluated', 'clear', 'vbar', 'des', 'cF0', 'cE', 'cN', 'cCK3', 'phase', 'lead_found', 'dx_pred3', 'now', 'age']
TOL_OTHER = 1e-12
TOL_CITATION = ('A10 sec. 3 B0(b): "Arrays rebuilt from the replayed actor lists reproduce the stored ones (critical scales of F0, N, E, NA, '
                'CK3, AM, Q; clearances; selections)" with the rule "(b) Within 1e-12"; it covers AM (cA1) and Q (cQ). Coordinator decision, '
                '20 Nov 2026 ~06:40 EST, relayed by the CD lead.')


def compare_npz(a, b):
    import numpy as np
    za = np.load(a, allow_pickle=False); zb = np.load(b, allow_pickle=False)
    ka = sorted(set(za.files) - {'meta'}); kb = sorted(set(zb.files) - {'meta'})
    if ka != kb: return dict(all_keys_identical=False, read_keys_identical=False, other_keys_within_tol=False, why='key sets differ')
    per = {}
    for k in ka:
        x, y = za[k], zb[k]
        same = x.dtype == y.dtype and x.shape == y.shape and np.array_equal(x, y, equal_nan=x.dtype.kind == 'f')
        if same: continue
        d = dict(dtype_shape_equal=bool(x.dtype == y.dtype and x.shape == y.shape))
        if d['dtype_shape_equal'] and x.dtype.kind in 'fiub':
            xx = x.astype(float); yy = y.astype(float); m = np.isfinite(xx) & np.isfinite(yy)
            d.update(finite_pattern_equal=bool(np.array_equal(np.isfinite(xx), np.isfinite(yy)) and np.array_equal(np.isnan(xx), np.isnan(yy))),
                     max_abs=float(np.max(np.abs(xx[m] - yy[m]))) if m.any() else 0.,
                     max_rel=float(np.max(np.abs(xx[m] - yy[m]) / np.maximum(np.abs(yy[m]), 1e-300))) if m.any() else 0.,
                     n_values_differing=int((xx[m] != yy[m]).sum()))
        per[k] = d
    read_ok = not any(k in per for k in READ_KEYS)
    other_ok = all(v.get('dtype_shape_equal') and v.get('finite_pattern_equal') and v.get('max_abs', 1.) <= TOL_OTHER
                   for k, v in per.items() if k not in READ_KEYS)
    return dict(all_keys_identical=not per, read_keys_identical=read_ok, other_keys_within_tol=other_ok, differing=per, n_keys=len(ka))


def accept(name):
    """Old run 0037 only (no fresh file is on the pod yet)."""
    out = ssh(name, '%s && cd %s/job && rm -rf %s/testold && %s -I -B -X utf8 %s --test-old --workers 8 --out-root %s/testold > %s/testold.log 2>&1; '
                    'echo rc=$?; tail -1 %s/testold.log | cut -c1-200' % (ENV, R, R, PY, XT, R, R, R), timeout=3600)
    if 'rc=0' not in out: raise SystemExit('%s: acceptance run failed: %s' % (name, out[-800:]))
    loc = CD / 'pods' / name / 'accept'; loc.mkdir(parents=True, exist_ok=True)
    ref = CD / 'analysis' / 'out' / 'testold_b7_arrays_final'
    res = {}
    for c in COMBOS:
        f = c.format(p='B7')
        (loc / f).mkdir(exist_ok=True)
        get(name, '%s/testold/%s/p1b_fit_finite_0037.npz' % (R, f), str(loc / f / 'p1b_fit_finite_0037.npz'))
        c = compare_npz(loc / f / 'p1b_fit_finite_0037.npz', ref / f / 'p1b_fit_finite_0037.npz')
        res[f] = dict(c, sha256_pod=sha(loc / f / 'p1b_fit_finite_0037.npz'))
    doc = dict(run='p1b_fit_finite_0037 (old)', reference=str(ref), chains=res,
               original_rule=dict(rule='bit-identical on every key', passed=all(v['all_keys_identical'] for v in res.values())),
               amended_rule=dict(rule='bit-identical on the keys c_b7/c_b7ci read (%s); every other key within %g absolute with an equal finite/NaN '
                                      'pattern' % (', '.join(READ_KEYS), TOL_OTHER), tolerance_abs=TOL_OTHER, tolerance_citation=TOL_CITATION,
                                 check1_read_keys_bit_identical=all(v['read_keys_identical'] for v in res.values()),
                                 check2_other_keys_within_tol=all(v['other_keys_within_tol'] for v in res.values())),
               pod_log_tail=out.strip()[-300:], at=pv.est())
    doc['accepted'] = doc['amended_rule']['check1_read_keys_bit_identical'] and doc['amended_rule']['check2_other_keys_within_tol']
    doc['all_identical'] = doc['accepted']           # the gate read by upload-fresh (amended rule)
    (CD / 'pods' / name / 'B7_ACCEPT.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(json.dumps(dict(accepted=doc['accepted'], original=doc['original_rule']['passed'], check1=doc['amended_rule']['check1_read_keys_bit_identical'],
                          check2=doc['amended_rule']['check2_other_keys_within_tol'],
                          chains={k: [v['all_keys_identical'], v['read_keys_identical'], v['other_keys_within_tol']] for k, v in res.items()})))
    if not doc['accepted']: raise SystemExit('ACCEPTANCE FAILED')


def run_ids(family):
    import cd_common_v13 as CC                          # run lists only (CASES_C_v13.json, REPLACEMENTS_C_v13.json)
    ids = CC.c_run_ids(family); assert len(ids) == 105
    return ids


def stage_fresh(family):
    ids = run_ids(family)
    miss = [r for r in ids if not (CD / 'runs' / r / 'LOGS_OK').is_file() or not (CD / 'b7' / r / 'B7_MANIFEST_v13.json').is_file()]
    if miss: raise SystemExit('REFUSED: %d %s runs lack LOGS_OK or the B7 manifest' % (len(miss), family))
    m = [(V13 / f, 'ARS_TRIAL/revision_v13/' + f) for f in ('LOCK_A10_2.txt', 'LOCK_A10_2c.txt')]
    base = 'ARS_TRIAL/revision_v13/work/CD_capture/'
    for r in ids:
        rd = CD / 'runs' / r / r; caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]; assert len(caps) == 1, r
        m.append((CD / 'runs' / r / 'LOGS_OK', base + 'runs/%s/LOGS_OK' % r))
        m.append((rd / 'SUMMARY.json', base + 'runs/%s/%s/SUMMARY.json' % (r, r)))
        for f in ('contract.json', 'evaluation_truth.jsonl', 'frames.jsonl', 'scenario_frames.jsonl'):
            m.append((caps[0] / f, base + 'runs/%s/%s/capture/%s/%s' % (r, r, caps[0].name, f)))
        for f in ('b7_detections_v13.jsonl', 'B7_MANIFEST_v13.json'):
            m.append((CD / 'b7' / r / f, base + 'b7/%s/%s' % (r, f)))
    man = bundle(STAGE / ('fresh_%s.tar' % family), m)
    print('fresh bundle %s: %d files, %.0f MB' % (family, len(man), (STAGE / ('fresh_%s.tar' % family)).stat().st_size / 1e6))


def upload_fresh(name, family):
    acc = json.loads((CD / 'pods' / name / 'B7_ACCEPT.json').read_text(encoding='utf-8'))
    if not acc['all_identical']: raise SystemExit('REFUSED: the pod did not pass the acceptance test')
    t = STAGE / ('fresh_%s.tar' % family)
    put(name, t, R + '/' + t.name)
    ssh(name, 'cd %s && tar xf %s && rm -f %s' % (R, t.name, t.name))
    n = verify_remote(name, STAGE / ('fresh_%s.json' % family))
    print('%s: %d fresh files verified on the pod' % (family, n))


def run(name, family, workers):
    ssh(name, '%s && cd %s/job && (setsid nohup %s -I -B -X utf8 %s --family %s --workers %d --out-root %s/out > %s/run_%s.log 2>&1 < /dev/null &) ; '
              'sleep 2; echo started' % (ENV, R, PY, XT, family, workers, R, R, family))
    print('started', family, 'workers', workers, pv.est())


def status(name, family):
    p = PREFIX[family]
    out = ssh(name, 'cd %s/out 2>/dev/null && echo npz=$(ls %s_*/*.npz 2>/dev/null | grep -v partial | wc -l) err=$(ls %s_*/*.err.json 2>/dev/null | wc -l) '
                    'json=$(ls XB7_EXTRACT_%s_*.json 2>/dev/null | wc -l); grep -c \'"status": "ok"\' %s/run_%s.log; pgrep -fc x_trk_extract || true'
              % (R, p, p, family, R, family))
    print(out.strip())
    return out


def fetch(name, family):
    p = PREFIX[family]; arr = CD / 'arrays'
    ssh(name, 'cd %s/out && sha256sum %s_*/*.npz > SHA_%s.txt && tar cf %s/arrays_%s.tar %s_*/*.npz SHA_%s.txt XB7_EXTRACT_%s_*.json XB7_EXTRACT_%s_*.log'
        % (R, p, family, R, family, p, family, family, family), timeout=1800)
    loc = STAGE / ('arrays_%s.tar' % family)
    get(name, '%s/arrays_%s.tar' % (R, family), str(loc))
    shas = {}; extracted = []
    with tarfile.open(loc) as t:
        names = t.getnames()
        sha_txt = t.extractfile('SHA_%s.txt' % family).read().decode()
        for line in sha_txt.splitlines():
            h, f = line.split(); shas[f] = h
        exp = ['%s/%s.npz' % (c.format(p=p), r) for c in COMBOS for r in run_ids(family)]
        missing = [x for x in exp if x not in shas]
        if missing: raise SystemExit('%s: %d arrays missing on the pod, e.g. %s' % (family, len(missing), missing[:3]))
        exists = [x for x in exp if (arr / x).exists()]
        if exists: raise SystemExit('REFUSED: %d target files exist in arrays\\ (never overwrite), e.g. %s' % (len(exists), exists[:3]))
        for m in t.getmembers():
            if m.name in exp:
                assert m.isfile() and '..' not in m.name
                t.extract(m, arr, filter='data'); extracted.append(m.name)
        logs = {}
        for m in t.getmembers():
            if m.name.startswith('XB7_EXTRACT_'):
                (CD / 'pods' / name / m.name).write_bytes(t.extractfile(m).read()); logs[m.name] = str(CD / 'pods' / name / m.name)
    bad = [x for x in extracted if sha(arr / x) != shas[x]]
    if bad: raise SystemExit('%s: %d downloaded files differ from the pod sha256: %s' % (family, len(bad), bad[:3]))
    rec = dict(family=family, n_files=len(extracted), all_sha256_verified=True, files={x: shas[x] for x in extracted}, extractor_logs=logs,
               tar_sha256=sha(loc), fetched=pv.est())
    (CD / 'pods' / name / ('B7_FETCH_%s.json' % family)).write_text(json.dumps(rec, indent=0), encoding='utf-8')
    loc.unlink()
    print('%s: %d arrays downloaded into arrays\\, all sha256 verified' % (family, len(extracted)))


# ------------------------------------------------------------------------------------------------ the analyses (c_b7, c_b7ci) on a pod
ANALYSES = {'lead_braking': ('c_b7_v13.py', 'C_B7_v13.json'), 'cutin': ('c_b7ci_v13.py', 'C_B7CI_v13.json')}
ANALYSIS_THREADS = {'lead_braking': 7, 'cutin': 6}      # the two run in parallel; 7 + 6 = 13 = the pod's cgroup cores (13.6); values do not
                                                          # depend on the thread count (gl_fast: one resample per prange iteration)


def stage_analysis():
    """Every input c_b7_v13.py / c_b7ci_v13.py read on fresh runs (from their code): the two scripts, both lock files, arrays\\B7_* and
    arrays\\B7CI_* (840 each), arrays\\CV0\\<rid>.npz of both families, runs\\<rid>\\LOGS_OK; per lead-braking run the capture's
    detections.jsonl and frames.jsonl (B7 identity); per cut-in run SUMMARY.json and contract.json, evaluation_truth.jsonl,
    scenario_frames.jsonl, frames.jsonl, detections.jsonl, filter_events.jsonl (event window: trk_arrays_v01.load_capture, gc.decisions;
    identity); b7\\<rid>\\ files of both families. Logs gzip-compressed; arrays as they are (npz)."""
    base = 'ARS_TRIAL/revision_v13/work/CD_capture/'
    logs = [(V13 / f, 'ARS_TRIAL/revision_v13/' + f) for f in ('LOCK_A10_2.txt', 'LOCK_A10_2c.txt')]
    logs += [(CD / 'analysis' / f, base + 'analysis/' + f) for f in ('c_b7_v13.py', 'c_b7ci_v13.py')]
    arrs = []
    for fam in ('lead_braking', 'cutin'):
        p = PREFIX[fam]
        for r in run_ids(fam):
            rd = CD / 'runs' / r / r; caps = [q for q in (rd / 'capture').iterdir() if q.is_dir()]; assert len(caps) == 1, r
            cap = caps[0]; cb = base + 'runs/%s/%s/capture/%s/' % (r, r, cap.name)
            logs.append((CD / 'runs' / r / 'LOGS_OK', base + 'runs/%s/LOGS_OK' % r))
            fl = ['detections.jsonl', 'frames.jsonl']
            if fam == 'cutin':
                fl += ['contract.json', 'evaluation_truth.jsonl', 'scenario_frames.jsonl', 'filter_events.jsonl']
                logs.append((rd / 'SUMMARY.json', base + 'runs/%s/%s/SUMMARY.json' % (r, r)))
            logs += [(cap / f, cb + f) for f in fl]
            logs += [(CD / 'b7' / r / f, base + 'b7/%s/%s' % (r, f)) for f in ('b7_detections_v13.jsonl', 'B7_MANIFEST_v13.json')]
            arrs.append((CD / 'arrays' / 'CV0' / (r + '.npz'), base + 'arrays/CV0/%s.npz' % r))
            arrs += [(CD / 'arrays' / c.format(p=p) / (r + '.npz'), base + 'arrays/%s/%s.npz' % (c.format(p=p), r)) for c in COMBOS]
    for name, m, gz in (('analysis_logs', logs, True), ('analysis_arrays', arrs, False)):
        path = STAGE / (name + ('.tar.gz' if gz else '.tar'))
        man = {}
        with tarfile.open(path, 'w:gz', compresslevel=3) if gz else tarfile.open(path, 'w') as t:
            for f, arc in m:
                t.add(str(f), arcname=arc, recursive=False); man[arc] = sha(f)
        (STAGE / (name + '.json')).write_text(json.dumps(dict(files=man, n=len(man), tar=path.name, tar_sha256=sha(path), written=pv.est()), indent=0),
                                               encoding='utf-8')
        print('%s: %d files, %.0f MB' % (name, len(man), path.stat().st_size / 1e6))


def stage_vid():
    """Inputs of the frozen c_b7_v13.py --test-old (old run 0037) beyond the code bundle: the two analysis scripts, the laptop's 0037 B7
    arrays (analysis\\out\\testold_b7_arrays_final), package B's stored CV0 array of 0037, and the 0037 capture's logged detections,
    filter_events and filter_algebra (B7 identity; the logged-extract comparison)."""
    base = 'ARS_TRIAL/revision_v13/work/'
    m = [(CD / 'analysis' / f, base + 'CD_capture/analysis/' + f) for f in ('c_b7_v13.py', 'c_b7ci_v13.py')]
    m += [(CD / 'analysis' / 'out' / 'testold_b7_arrays_final' / c.format(p='B7') / 'p1b_fit_finite_0037.npz',
           base + 'CD_capture/analysis/out/testold_b7_arrays_final/%s/p1b_fit_finite_0037.npz' % c.format(p='B7')) for c in COMBOS]
    m += [(WORK / 'B_retrack' / 'out' / 'retrack' / 'CV0' / 'p1b_fit_finite_0037_arrays.npz', base + 'B_retrack/out/retrack/CV0/p1b_fit_finite_0037_arrays.npz')]
    c37 = P / '07_fit_runs' / 'archives' / 'p1b_fit_finite_0037' / 'x' / 'p1b_fit_finite_0037' / 'capture' / 'fit_finite_0037'
    m += [(c37 / f, 'P/07_fit_runs/archives/p1b_fit_finite_0037/x/p1b_fit_finite_0037/capture/fit_finite_0037/' + f)
          for f in ('detections.jsonl', 'filter_events.jsonl', 'filter_algebra.jsonl')]
    man = bundle(STAGE / 'vid_bundle.tar', m)
    print('vid bundle: %d files' % len(man))


def run_vid(name, tag, threads):
    an = R + '/ARS_TRIAL/revision_v13/work/CD_capture/analysis'
    put(name, STAGE / 'vid_bundle.tar', R + '/vid_bundle.tar')
    ssh(name, 'cd %s && tar xf vid_bundle.tar && rm -f vid_bundle.tar' % R)
    verify_remote(name, STAGE / 'vid_bundle.json')
    out = ssh(name, '%s NUMBA_NUM_THREADS=%d && cd %s/job && %s -I -B -X utf8 %s/c_b7_v13.py --test-old --arrays %s/out/testold_b7_arrays_final --tag %s '
                    '> %s/vid_%s.log 2>&1; echo rc=$?; tail -1 %s/vid_%s.log | cut -c1-160' % (ENV, threads, R, PY, an, an, tag, R, tag, R, tag), timeout=3600)
    if 'rc=0' not in out: raise SystemExit('%s: c_b7 --test-old failed: %s' % (name, out[-600:]))
    loc = CD / 'pods' / name / ('TESTOLD_B7_v13_%s.json' % tag)
    get(name, '%s/out/TESTOLD_B7_v13_%s.json' % (an, tag), str(loc))
    ref = CD / 'analysis' / 'out' / 'TESTOLD_B7_v13_vid_lap1.json'
    a = json.loads(loc.read_text(encoding='utf-8'))['values']; b = json.loads(ref.read_text(encoding='utf-8'))['values']
    diff = sorted(k for k in set(a) | set(b) if a.get(k, 'MISSING') != b.get(k, 'MISSING'))
    doc = dict(check='frozen c_b7_v13.py --test-old on the pod (old run 0037, the laptop\'s 0037 arrays) vs the laptop\'s TESTOLD_B7_v13_vid_lap1.json: '
                     '`values` bit-identical (exact equality of every JSON value)', pod=name, tag=tag, numba_threads=threads,
               n_values_pod=len(a), n_values_laptop=len(b), n_differing=len(diff), differing_keys=diff, identical=not diff and len(a) == len(b),
               pod_output=str(loc), pod_output_sha256=sha(loc), laptop_reference=str(ref), laptop_reference_sha256=sha(ref), at=pv.est())
    (CD / 'pods' / name / 'B7_VALUE_IDENTITY_POD.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(json.dumps({k: doc[k] for k in ('identical', 'n_values_pod', 'n_values_laptop', 'n_differing')}))
    if not doc['identical']: raise SystemExit('VALUE IDENTITY FAILED')


def upload_replaced(name, spec):
    """spec 'family:rid,family:rid,...': the arrays the CD lead re-extracted on the laptop (8 chains each) replace the pod-made ones on the
    analysis pod (cross-machine last-bit differences; README of the run in B7_POD_RUN_v13.json). Uploaded as one tar, SHA-256 checked."""
    base = 'ARS_TRIAL/revision_v13/work/CD_capture/'
    m = []
    for item in spec.split(','):
        fam, rid = item.split(':'); p = PREFIX[fam]
        assert rid in run_ids(fam), item
        m += [(CD / 'arrays' / c.format(p=p) / (rid + '.npz'), base + 'arrays/%s/%s.npz' % (c.format(p=p), rid)) for c in COMBOS]
    man = bundle(STAGE / 'replaced_arrays.tar', m)
    put(name, STAGE / 'replaced_arrays.tar', R + '/replaced_arrays.tar')
    ssh(name, 'cd %s && tar xf replaced_arrays.tar && rm -f replaced_arrays.tar' % R)
    n = verify_remote(name, STAGE / 'replaced_arrays.json')
    rec = dict(spec=spec, n_files=n, files_sha256=man, uploaded=pv.est(),
               reason='cross-machine last-bit differences in B7-read keys (laptop Windows libm vs pod glibc in the extraction geometry); re-extracted '
                      'on the laptop by the CD lead with the frozen x_trk_extract_v13.py; the pod versions are kept aside by the CD lead')
    (CD / 'pods' / name / 'B7_REPLACED.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print('%d replaced arrays verified on the pod' % n)


def upload_analysis(name, which):
    j = json.loads((STAGE / (which + '.json')).read_text(encoding='utf-8'))
    put(name, STAGE / j['tar'], R + '/' + j['tar'])
    ssh(name, 'cd %s && tar x%sf %s && rm -f %s' % (R, 'z' if j['tar'].endswith('.gz') else '', j['tar'], j['tar']), timeout=3600)
    n = verify_remote(name, STAGE / (which + '.json'))
    print('%s: %d files verified on the pod' % (which, n))


def run_analysis(name, threads=None):
    an = R + '/ARS_TRIAL/revision_v13/work/CD_capture/analysis'
    for fam, (script, _) in ANALYSES.items():
        threads = ANALYSIS_THREADS[fam]
        ssh(name, '%s NUMBA_NUM_THREADS=%d && cd %s/job && (setsid nohup %s -I -B -X utf8 %s/%s > %s/analysis_%s.log 2>&1 < /dev/null &) ; sleep 1; echo started'
            % (ENV, threads, R, PY, an, script, R, fam))
        print('started', script, 'NUMBA_NUM_THREADS', threads, pv.est())


def status_analysis(name):
    out = ssh(name, 'cd %s && for f in analysis_lead_braking.log analysis_cutin.log; do echo "$f: $(wc -l < $f) lines; $(grep -c -E \'Error|Traceback|REFUSED\' $f) errors; '
                    'written: $(grep -c written $f)"; done; ls ARS_TRIAL/revision_v13/work/CD_capture/analysis/out/ 2>/dev/null; pgrep -fc "c_b7" || true' % R)
    print(out.strip())


def fetch_analysis(name):
    loc_out = CD / 'analysis' / 'out'; res = {}
    ao = R + '/ARS_TRIAL/revision_v13/work/CD_capture/analysis/out'
    for fam, (script, outj) in ANALYSES.items():
        dest = loc_out / outj
        if dest.exists(): raise SystemExit('REFUSED: %s exists on the laptop (never overwrite)' % dest)
        h = ssh(name, 'sha256sum %s/%s %s/analysis_%s.log' % (ao, outj, R, fam)).split()
        tmp = STAGE / (outj + '.download'); get(name, '%s/%s' % (ao, outj), str(tmp))
        if sha(tmp) != h[0]: raise SystemExit('%s: sha256 differs after download' % outj)
        tmp.replace(dest)
        logp = CD / 'pods' / name / ('analysis_%s.log' % fam); get(name, '%s/analysis_%s.log' % (R, fam), str(logp))
        if sha(logp) != h[2]: raise SystemExit('%s log: sha256 differs after download' % fam)
        res[fam] = dict(output=str(dest), sha256=h[0], log=str(logp), log_sha256=h[2])
    rec = dict(outputs=res, fetched=pv.est())
    (CD / 'pods' / name / 'B7_ANALYSIS_FETCH.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print(json.dumps({k: dict(output=v['output'].split('\\')[-1], sha256=v['sha256']) for k, v in res.items()}))


def record(names):
    """analysis\\out\\B7_POD_RUN_v13.json: pods, times, acceptance, jobs (status and timing only), per-file sha256. Never overwrites."""
    out = CD / 'analysis' / 'out' / 'B7_POD_RUN_v13.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out)
    doc = dict(program='tools/b7_pods_v13.py', plan='tools/trk_pod_plan_v13.md', extractor='analysis/x_trk_extract_v13.py',
               extractor_sha256=sha(CD / 'analysis' / 'x_trk_extract_v13.py'), code_bundle=json.loads((STAGE / 'code_bundle.json').read_text(encoding='utf-8')),
               pods={}, families={}, written=pv.est())
    doc['acceptance'] = dict(
        original_rule=dict(rule='the pod\'s x_trk_extract_v13.py --test-old output for old run 0037 (8 arrays) bit-identical to '
                                'analysis/out/testold_b7_arrays_final on every key', source='tools/trk_pod_plan_v13.md (frozen in FREEZE_CD_2)'),
        attempt_1=dict(pod='claude-v13cd-b01', result='failed the original rule: 3 of 8 chains bit-identical; 5 differ only in cA1 (AM) and cQ (Q) '
                       'at the last bit (max 1.42e-14 absolute, 4.2e-16 relative), equal finite/NaN pattern; every key B7 reads bit-identical; '
                       'pod deleted, no fresh file uploaded', record='analysis/out/B7_POD_RUN_v13_attempt1_FAILED.json',
                       amended_check_offline='analysis/out/B7_POD_ACCEPT_attempt1_amended_rule_offline.json (1e-14 version; failed check 2)'),
        amendment=dict(rule='bit-identical on every key c_b7_v13.py / c_b7ci_v13.py read (%s); every other array key within %g absolute with an '
                            'equal finite/NaN pattern' % (', '.join(READ_KEYS), TOL_OTHER), tolerance_citation=TOL_CITATION,
                       reason='cA1/cQ last-bit differences (<= 4.2e-16 relative) from the Linux maths library, in keys B7 never reads; all read keys '
                              'bit-identical',
                       decided='CD lead, 20 Nov 2026 ~06:30 EST (read keys bit-identical; first tolerance 1e-14 per A10 B0(a)); tolerance settled by the '
                               'coordinator ~06:40 EST as A10 B0(b)\'s 1e-12; reported by the CD lead as an A10 sec. 11 departure',
                       pre_upload_gate='the CD lead\'s B7 output-identity check on 0037 and the lead\'s "go"'),
        value_identity_gate=dict(record='analysis/out/B7_VALUE_IDENTITY_0037_v13.json',
                                 sha256=sha(CD / 'analysis' / 'out' / 'B7_VALUE_IDENTITY_0037_v13.json') if (CD / 'analysis' / 'out' / 'B7_VALUE_IDENTITY_0037_v13.json').is_file() else None,
                                 summary='the coordinator\'s gate: c_b7 and rc_b7 on attempt 1\'s pod 0037 arrays vs the laptop\'s 0037 arrays give bit-identical '
                                         'outputs, 76 of 76 values each; passed; GO from the CD lead at 07:05 EST',
                                 content=(json.loads((CD / 'analysis' / 'out' / 'B7_VALUE_IDENTITY_0037_v13.json').read_text(encoding='utf-8'))
                                          if (CD / 'analysis' / 'out' / 'B7_VALUE_IDENTITY_0037_v13.json').is_file() else None)),
        this_run={n: (json.loads((CD / 'pods' / n / 'B7_ACCEPT.json').read_text(encoding='utf-8')) if (CD / 'pods' / n / 'B7_ACCEPT.json').is_file() else None)
                  for n in names})
    for name in names:
        d = CD / 'pods' / name; rd = lambda f: json.loads((d / f).read_text(encoding='utf-8')) if (d / f).is_file() else None
        pod = rd('pod.json') or {}
        doc['pods'][name] = dict(id=pod.get('id'), gpu=pod.get('gpu'), costPerHr=pod.get('costPerHr'), created=pod.get('created'),
                                 terminated=(d / 'TERMINATED').read_text(encoding='utf-8').strip() if (d / 'TERMINATED').is_file() else None,
                                 setup=rd('B7_SETUP.json'), acceptance=rd('B7_ACCEPT.json'))
        for fam in ('lead_braking', 'cutin'):
            f = rd('B7_FETCH_%s.json' % fam)
            if not f: continue
            jobs = []
            for lf in f['extractor_logs'].values():
                if lf.endswith('.json'):
                    x = json.loads(pathlib.Path(lf).read_text(encoding='utf-8'))
                    jobs += [{k: v for k, v in j.items() if k != 'n_dec'} for j in x['jobs']]
                    gate = x['gate']
            doc['families'][fam] = dict(pod=name, n_files=f['n_files'], all_sha256_verified=f['all_sha256_verified'], fetched=f['fetched'],
                                        tar_sha256=f['tar_sha256'], gate_on_pod=gate, jobs=jobs,
                                        job_status_counts={s: sum(1 for j in jobs if j['status'].startswith(s)) for s in ('ok', 'exists', 'waiting', 'ERROR')},
                                        files_sha256=f['files'])
        vid, af = rd('B7_VALUE_IDENTITY_POD.json'), rd('B7_ANALYSIS_FETCH.json')
        if vid or af:
            doc['analysis'] = dict(
                pod=name, gpu=pod.get('gpu'), why_this_gpu='RTX 4090 and RTX PRO 6000 Server Edition out of stock in EU-RO-1 at 08:00-08:15 EST; '
                'CD lead option A (RTX PRO 6000, either edition)', cpu_quota='cgroup cfs quota 1,360,000 / period 100,000 = 13.6 cores (nproc 64)',
                pre_check=dict(rule='CD lead ~08:00 EST: on this pod, the frozen c_b7_v13.py --test-old --arrays analysis/out/testold_b7_arrays_final '
                                    '--tag vid_pro6000 must give `values` bit-identical to the laptop\'s TESTOLD_B7_v13_vid_lap1.json (all 76), because '
                                    'numba compiles for the host CPU and the coordinator\'s identity proof covered RTX 4090 pods only', result=vid),
                inputs=dict(note='every input c_b7_v13.py / c_b7ci_v13.py read on fresh runs (tools/b7_pods_v13.py stage_analysis docstring)',
                            bundles={b: {k: v for k, v in json.loads((STAGE / (b + '.json')).read_text(encoding='utf-8')).items() if k != 'files'}
                                     for b in ('analysis_arrays', 'analysis_logs') if (STAGE / (b + '.json')).is_file()},
                            files_sha256={b: json.loads((STAGE / (b + '.json')).read_text(encoding='utf-8'))['files']
                                          for b in ('analysis_arrays', 'analysis_logs') if (STAGE / (b + '.json')).is_file()}),
                commands=['c_b7_v13.py (fresh, default options)', 'c_b7ci_v13.py (fresh, default options)'],
                numba_threads=ANALYSIS_THREADS, outputs=af, replaced_arrays=rd('B7_REPLACED.json'),
                superseded_first_run=dict(note='first run of c_b7 / c_b7ci on b04 (08:35 EST) on the pod-made arrays only: c_b7ci REFUSED at its '
                    'consistency check (B7CI_2_0 pc13_c1109_eval_0184_native: clearance differs from the CV0 array at the last bit); c_b7 finished '
                    'before the CD lead stop message arrived; its C_B7_v13.json was never downloaded or opened, moved on the pod to '
                    '/root/b7/superseded_run1/ and deleted with the pod', c_b7_output_sha256='685cb80bb9bbcc6e85d7bd19a09307b56b59b177cff5563fdf336c7b038f8b4b',
                    crossmachine_record='analysis/out/B7_CROSSMACHINE_DIFF_v13.json (CD lead)'))
    rr = CD / 'analysis' / 'out' / 'B7_REPLACED_RUNS_v13.json'
    doc['replacements'] = dict(note='after the extraction, 48 pod-made arrays were replaced by laptop re-extractions (frozen x_trk_extract_v13.py) '
                               'because of cross-machine last-bit differences in B7-read keys: lead pc13_c1109_eval_0114 (8 B7_* chains) and cut-in '
                               '0184, 0226, 0238, 0358, 0418 (8 B7CI_* chains each); pod versions kept in arrays_pod_superseded; '
                               'families.*.files_sha256 lists the pod-made files as downloaded; the replaced files and their sha256 are in '
                               'analysis.replaced_arrays', record='analysis/out/B7_REPLACED_RUNS_v13.json',
                               record_sha256=sha(rr) if rr.is_file() else None)
    import datetime as _dt
    cost = {}
    for n, v in doc['pods'].items():
        try:
            t0 = _dt.datetime.fromisoformat(v['created']); t1s = v['terminated'].split(' rc=')[0].replace(' Eastern Standard Time', '')
            t1 = _dt.datetime.strptime(t1s, '%Y-%m-%d %H:%M:%S').replace(tzinfo=t0.tzinfo)
            h = (t1 - t0).total_seconds() / 3600.; cost[n] = dict(hours=round(h, 3), usd=round(h * float(v['costPerHr']), 2))
        except Exception as e:
            cost[n] = dict(error=repr(e)[:100])
    doc['cost_estimate'] = dict(per_pod=cost, total_usd=round(sum(c.get('usd', 0) for c in cost.values()), 2),
                                note='created-to-terminated time x cost per hour; the spend log SPEND_LOG_v13.csv has the rows')
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('written', out, {k: (v['n_files'], v['job_status_counts']) for k, v in doc['families'].items()})


def main():
    a = sys.argv[1:]
    c = a[0]
    if c == 'record': record(a[1:]); return
    if c == 'stage-analysis': stage_analysis(); return
    if c == 'stage-vid': stage_vid(); return
    if c == 'upload-replaced': upload_replaced(a[1], a[2]); return
    if c == 'run-vid': run_vid(a[1], a[2], int(a[3])); return
    if c == 'upload-analysis': upload_analysis(a[1], a[2]); return
    if c == 'run-analysis': run_analysis(a[1]); return
    if c == 'status-analysis': status_analysis(a[1]); return
    if c == 'fetch-analysis': fetch_analysis(a[1]); return
    if c == 'stage-code': stage_code()
    elif c == 'setup': setup(a[1])
    elif c == 'accept': accept(a[1])
    elif c == 'stage-fresh': stage_fresh(a[1])
    elif c == 'upload-fresh': upload_fresh(a[1], a[2])
    elif c == 'run': run(a[1], a[2], int(a[3]) if len(a) > 3 else 30)
    elif c == 'status': status(a[1], a[2])
    elif c == 'fetch': fetch(a[1], a[2])
    else: raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
