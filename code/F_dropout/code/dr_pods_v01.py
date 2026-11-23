"""Revision v13, AMENDMENT_11 sec. 6c (DR): runs DR's extraction and analysis on a RunPod pod. New file, 21 Nov 2026 (Claude Opus 5.5,
session F); adapted from CD_capture\\tools\\b7_pods_v13.py (the B7 pod route, accepted bit-identical; CD_capture\\tools\\trk_pod_plan_v13.md
sec. 3: V13_CODEX_ROOT, V13_P_ROOT and five links named literally after the Windows paths, so no frozen file is edited). This file only
moves files and starts programs; it computes no value. Pods are created and deleted through F_nuscenes\\code\\fpods_v01.py (spend-log
rows, session watchdog).
  stage-code                  pods_dr\\code_bundle.tar.gz (+ .json sha manifest): codex tree, P's openloop modules, run index and
                              optA_lib_v02, v11/v12 helpers, the shared trackers, CD's cd_common / gl_fast / calib_remote, F_dropout
                              code + masks, the 0037 test data
  stage-data WHICH            fresh: per fresh run LOGS_OK, SUMMARY.json and 5 capture files; tuning: per tuning run SUMMARY.json and 5
                              capture files (under P's own relative paths); lock: LOCK_A11c.txt (refuses without it)
  up NAME [--gpu G] [--deadline-h H]   create (fpods) and set up: CPython 3.12 + CD's pins (uv), code bundle (sha-checked), links
  upload NAME WHICH           upload and verify a data bundle (sha256 of every file on the pod)
  run NAME TAG CMD...         start `python -I -B -X utf8 CMD...` in <pod>/job with the environment of record (background; log TAG.log)
  status NAME [TAG]           tail of the log(s), npz counts, running processes
  fetch NAME SUBDIR           tar <pod>/ARS_TRIAL/revision_v13/work/F_dropout/out/SUBDIR, download, verify every sha256, extract into
                              F_dropout\\out\\SUBDIR (never overwrites)
  down NAME NOTE              delete the pod (fpods; spend-log row)
Usage: python -I -B dr_pods_v01.py CMD ...
"""
import hashlib, json, pathlib, sys, tarfile, time
HERE = pathlib.Path(__file__).resolve().parent
DRD = HERE.parent
WORK = DRD.parent
V13 = WORK.parent
sys.path.insert(0, str(WORK / 'F_nuscenes' / 'code'))
import fpods_v01 as pv                                  # noqa: E402

DL = pathlib.Path(r'<user folder>')
CODEX = DL / '<earlier-phase folder 2>' / '149_supported_sensor_preparation_20261101'
P = DL / '<earlier-phase folder 1>'
CD = WORK / 'CD_capture'
STAGE = DRD / 'pods_dr'
R = '/root/dr'
PY = '/opt/drpy/bin/python'
PINS = ('numpy==2.5.4 numba==0.68.1 llvmlite==0.50.0 scipy==1.18.1 pandas==2.2.2 matplotlib==3.11.2 opencv-python-headless==4.14.0.94 '
        'scikit-learn==1.9.1 pillow==13.0.0 PyYAML==6.0.2 cloudpickle==3.1.2 joblib==1.6.0 tqdm==4.70.1 psutil==7.0.0 cachetools==7.3.0 '
        'threadpoolctl==3.8.0 contourpy==1.4.0 kiwisolver==1.5.1 fonttools==4.68.0 cycler==0.12.1 pyparsing==3.3.3 '
        'python-dateutil==2.9.0.post0 pytz==2024.1 tzdata==2024.1 packaging==24.2 six==1.16.0 narwhals==2.28.0 cffi==2.1.1 pycparser==2.22 '
        'charset-normalizer==3.4.1')                    # = CD's pins (CD_capture\analysis\out\VENV_FREEZE.txt), as b7_pods_v13.py
OPENLOOP = ['olcore_v01.py', 'olcore_rt_v01.py', 'ol_gateR_core_v01.py', 'ol_gateR_rt_extract_v01.py', 'ol_extract_v01.py',
            'ox12_core_v01.py', 'oxsb_core_v01.py', 'pbar_tuning_v01.json']
LINKS = {r'<library folder>\openloop': R + '/P/09_redesign/m2_decisions/openloop',
         r'<library folder>': R + '/P',
         r'ARS_TRIAL\revision_v12\analysis': R + '/ARS_TRIAL/revision_v12/analysis',
         r'ARS_TRIAL\revision_v11\analysis': R + '/ARS_TRIAL/revision_v11/analysis',
         r'<library folder>\149_supported_sensor_preparation_20261101': R + '/codex'}
ENV = ('export V13_CODEX_ROOT=%s/codex V13_P_ROOT=%s/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 '
       'MKL_NUM_THREADS=1 NUMBA_CACHE_DIR=%s/numba_cache' % (R, R, R))
FD = R + '/ARS_TRIAL/revision_v13/work/F_dropout'
CAPF = ('contract.json', 'evaluation_truth.jsonl', 'frames.jsonl', 'scenario_frames.jsonl', 'detections.jsonl')


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


def put(name, local, remote, tries=3):
    for t in range(tries):
        r = pv.sftp(name, ['put "%s" "%s"' % (local, remote)])
        if r.returncode == 0: return
        print('upload try %d failed: %s' % (t + 1, r.stderr[-300:])); time.sleep(20)
    raise SystemExit('%s: upload of %s failed' % (name, local))


def get(name, remote, local):
    r = pv.sftp(name, ['get "%s" "%s"' % (remote, local)])
    if r.returncode != 0: raise SystemExit('%s: download of %s failed: %s' % (name, remote, r.stderr[-600:]))


def bundle(path, members):
    man = {}
    with tarfile.open(path, 'w:gz', compresslevel=6) as t:
        for f, arc in members:
            t.add(str(f), arcname=arc, recursive=False); man[arc] = sha(f)
    (path.parent / (path.name.split('.')[0] + '.json')).write_text(json.dumps(dict(files=man, n=len(man), tar_sha256=sha(path),
                                                                                    written=pv.est()), indent=0), encoding='utf-8')
    print('%s: %d files, %.1f MB' % (path.name, len(man), path.stat().st_size / 1e6))
    return man


def walk(root, arcroot, skip=lambda p: False):
    return [(p, arcroot + '/' + p.relative_to(root).as_posix()) for p in sorted(root.rglob('*')) if p.is_file() and not skip(p)]


def p_rel(win_path):
    s = str(win_path); assert s.startswith(str(P)), s
    return 'P/' + '/'.join(x for x in s[len(str(P)):].split('\\') if x)


def stage_code():
    STAGE.mkdir(parents=True, exist_ok=True)
    junk = lambda p: '__pycache__' in p.parts or p.suffix in ('.pyc', '.nbi', '.nbc') or p.name.startswith('tmp')
    m = []
    for sub in ('code', 'sources', 'vendor', 'legacy86/vendor/nuscenes-devkit/python-sdk', 'contracts'):
        m += walk(CODEX / sub, 'codex/' + sub, junk)
    m += [(P / '09_redesign' / 'm2_decisions' / 'openloop' / f, 'P/09_redesign/m2_decisions/openloop/' + f) for f in OPENLOOP]
    m += [(P / '09_redesign' / 'm4_perception_model' / 'run_index_m4_v02.csv', 'P/09_redesign/m4_perception_model/run_index_m4_v02.csv')]
    m += [(P / '11_ojits' / 'A6R' / 'code' / 'optA_lib_v02.py', 'P/11_ojits/A6R/code/optA_lib_v02.py')]
    a37 = P / '07_fit_runs' / 'archives' / 'p1b_fit_finite_0037'; c37 = a37 / 'x' / 'p1b_fit_finite_0037' / 'capture' / 'fit_finite_0037'
    m += [(a37 / 'SUMMARY.json', 'P/07_fit_runs/archives/p1b_fit_finite_0037/SUMMARY.json')]
    m += [(c37 / f, 'P/07_fit_runs/archives/p1b_fit_finite_0037/x/p1b_fit_finite_0037/capture/fit_finite_0037/' + f) for f in CAPF]
    m += [(DL / 'ARS_TRIAL' / 'revision_v11' / 'analysis' / 'rev_common_v01.py', 'ARS_TRIAL/revision_v11/analysis/rev_common_v01.py'),
          (DL / 'ARS_TRIAL' / 'revision_v12' / 'analysis' / 'a9_common_v01.py', 'ARS_TRIAL/revision_v12/analysis/a9_common_v01.py')]
    m += walk(WORK / 'shared' / 'trackers', 'ARS_TRIAL/revision_v13/work/shared/trackers', junk)
    m += [(CD / 'analysis' / f, 'ARS_TRIAL/revision_v13/work/CD_capture/analysis/' + f)
          for f in ('cd_common_v13.py', 'gl_fast_v13.py', 'calib_remote_v13.py')]
    m += [(CD / 'tools' / 'calib_merge_v13.py', 'ARS_TRIAL/revision_v13/work/CD_capture/tools/calib_merge_v13.py')]
    m += [(CD / f, 'ARS_TRIAL/revision_v13/work/CD_capture/' + f) for f in ('CASES_C_v13.json', 'REPLACEMENTS_C_v13.json') if (CD / f).is_file()]
    m += [(f, 'ARS_TRIAL/revision_v13/work/F_dropout/code/' + f.name) for f in sorted((DRD / 'code').glob('*'))
          if f.is_file() and f.suffix in ('.py', '.json') and not f.name.startswith('dr_pods')]
    m += [(DRD / 'masks' / f, 'ARS_TRIAL/revision_v13/work/F_dropout/masks/' + f) for f in ('DR_MASKS_v01.json', 'DR_MASKS_v02.json')]
    ps = STAGE / 'pod_links_dr.py'
    ps.write_text('import os, json\nL = %s\nos.makedirs(%r, exist_ok=True)\nos.chdir(%r)\nfor k, v in L.items():\n'
                  '    if not os.path.islink(k): os.symlink(v, k)\nprint(json.dumps({k: os.path.realpath(k) for k in L}))\n'
                  % (json.dumps(LINKS), R + '/job', R + '/job'), encoding='utf-8')
    m += [(ps, 'pod_links_dr.py')]
    bundle(STAGE / 'code_bundle.tar.gz', m)


def stage_data(which):
    STAGE.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(HERE))
    import dr_masks_v02 as M
    m = []
    if which == 'fresh':
        base = 'ARS_TRIAL/revision_v13/work/CD_capture/'
        for rid, (case, cap) in M.fresh_runs().items():
            rd = CD / 'runs' / rid / rid
            m.append((CD / 'runs' / rid / 'LOGS_OK', base + 'runs/%s/LOGS_OK' % rid))
            m.append((rd / 'SUMMARY.json', base + 'runs/%s/%s/SUMMARY.json' % (rid, rid)))
            m += [(cap / f, base + 'runs/%s/%s/capture/%s/%s' % (rid, rid, cap.name, f)) for f in CAPF]
    elif which == 'tuning':
        for rid, (case, cap) in M.tuning_runs().items():
            m.append((cap.parents[3] / 'SUMMARY.json', p_rel(cap.parents[3] / 'SUMMARY.json')))
            m += [(cap / f, p_rel(cap / f)) for f in CAPF]
    elif which == 'testold':          # the 35 OLD lead-braking fit runs (exploratory test set of dr_extract --test-old all)
        sys.path.insert(0, str(HERE))
        import csv
        rows = [r for r in csv.DictReader(open(P / '09_redesign' / 'm4_perception_model' / 'run_index_m4_v02.csv', encoding='utf-8'))
                if r['use'] == '1' and r['set'] == 'fit' and r['family'] == 'lead_braking']
        assert len(rows) == 35
        for r in rows:
            cap = pathlib.Path(r['cap'])
            m.append((cap.parents[3] / 'SUMMARY.json', p_rel(cap.parents[3] / 'SUMMARY.json')))
            m += [(cap / f, p_rel(cap / f)) for f in CAPF]
    elif which == 'lock':
        lk = V13 / 'LOCK_A11c.txt'
        if not lk.is_file(): raise SystemExit('REFUSED: no LOCK_A11c.txt')
        m.append((lk, 'ARS_TRIAL/revision_v13/LOCK_A11c.txt'))
    else:
        raise SystemExit('unknown bundle')
    bundle(STAGE / ('%s_bundle.tar.gz' % which), m)


def verify_remote(name, manifest_path):
    man = json.loads(manifest_path.read_text(encoding='utf-8'))['files']
    lst = STAGE / (manifest_path.stem + '.sha256.txt')
    lst.write_text(''.join('%s  %s\n' % (h, a) for a, h in man.items()), encoding='ascii', newline='\n')
    put(name, lst, R + '/' + lst.name)
    out = ssh(name, 'cd %s && sha256sum -c --quiet %s > %s.check 2>&1; echo rc=$?' % (R, lst.name, lst.name))
    if 'rc=0' not in out: raise SystemExit('%s: sha256 check of %s failed: %s' % (name, manifest_path.name, out[-500:]))
    return len(man)


def upload(name, which):
    t = STAGE / ('%s_bundle.tar.gz' % which)
    ssh(name, 'mkdir -p %s' % R)
    put(name, t, R + '/' + t.name)
    ssh(name, 'cd %s && tar xzf %s && rm -f %s' % (R, t.name, t.name), timeout=1800)
    n = verify_remote(name, STAGE / ('%s_bundle.json' % which))
    print('%s: %s bundle, %d files verified on the pod' % (name, which, n))


def up(name, gpu, deadline_h):
    if not (pv.PODS / name / 'pod.json').is_file():
        pv.create(name, gpu, deadline_h, 'AMENDMENT_11 sec. 6c DR (detection dropouts): extraction / analysis')
    nproc = ssh(name, 'nproc; cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us /sys/fs/cgroup/cpu/cpu.cfs_period_us 2>/dev/null || cat /sys/fs/cgroup/cpu.max').split()
    check = '%s -c "import sys,numpy,numba,scipy,pandas,matplotlib,cv2,sklearn,PIL,yaml; print(sys.version.split()[0], numpy.__version__, numba.__version__)"' % PY
    have = pv.ssh(name, check, timeout=120)
    if have.returncode != 0:
        ssh(name, '( python3 -m pip install -q uv && uv venv -q --clear -p 3.12 /opt/drpy && uv pip install -q --python %s %s ) > /root/dr_setup.log 2>&1; '
                  'tail -3 /root/dr_setup.log' % (PY, PINS), timeout=2400)
        have = pv.ssh(name, check, timeout=120)
    vers = have.stdout.strip()
    if have.returncode != 0 or vers.split()[1:] != ['2.5.4', '0.68.1']:
        raise SystemExit('%s: environment not ready: %s %s' % (name, vers, have.stderr[-800:]))
    upload(name, 'code')
    links = ssh(name, 'cd %s && /usr/bin/env python3 pod_links_dr.py' % R)
    rec = dict(nproc_and_quota=nproc, python_numpy_numba=vers, links=json.loads(links.strip().splitlines()[-1]), at=pv.est())
    (pv.PODS / name / 'DR_SETUP.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print(json.dumps(rec))


def run(name, tag, cmd):
    ssh(name, '%s && cd %s/job && (setsid nohup %s -I -B -X utf8 %s > %s/%s.log 2>&1 < /dev/null &) ; sleep 2; echo started'
        % (ENV, R, PY, ' '.join(cmd), R, tag))
    print('started', tag, pv.est())


def status(name, tag=None):
    t = ('tail -n 4 %s/%s.log; ' % (R, tag)) if tag else ('tail -n 2 %s/*.log; ' % R)
    print(ssh(name, t + 'for d in %s/out/arrays/* %s/out/pbar; do [ -d $d ] && echo $d $(ls $d/*.npz 2>/dev/null | grep -v partial | wc -l) '
                        'err=$(ls $d/*.err.json 2>/dev/null | wc -l); done; pgrep -fc dr_ || true; uptime' % (FD, FD)))


def fetch(name, sub):
    dest = DRD / 'out' / sub
    tarn = 'fetch_%s.tar' % sub.replace('/', '_')
    out_ = ssh(name, 'cd %s/out && find %s -type f ! -name "*.partial.npz" | sort > /root/fl.txt && test -s /root/fl.txt && '
                     'xargs -a /root/fl.txt sha256sum > /root/SHA_fetch.txt < /dev/null && tar cf %s/%s -T /root/fl.txt && echo FETCH_READY'
               % (FD, sub, R, tarn), timeout=1800)
    if 'FETCH_READY' not in out_: raise SystemExit('%s: nothing to fetch under out/%s' % (name, sub))
    loc = STAGE / tarn
    get(name, '%s/%s' % (R, tarn), str(loc))
    get(name, '/root/SHA_fetch.txt', str(STAGE / ('SHA_' + tarn + '.txt')))
    shas = dict(reversed(l.split(None, 1)) for l in (STAGE / ('SHA_' + tarn + '.txt')).read_text().splitlines() if l.strip())
    shas = {k.strip(): v for k, v in shas.items()}
    out = DRD / 'out'; ex = []
    with tarfile.open(loc) as t:
        for mbr in t.getmembers():
            assert mbr.isfile() and '..' not in mbr.name
            if (out / mbr.name).exists():
                if sha(out / mbr.name) != shas[mbr.name]:
                    raise SystemExit('REFUSED: %s exists locally with other content' % mbr.name)
                continue
            t.extract(mbr, out, filter='data'); ex.append(mbr.name)
    bad = [x for x in ex if sha(out / x) != shas[x]]
    if bad: raise SystemExit('%d downloaded files differ from the pod sha256: %s' % (len(bad), bad[:3]))
    rec = dict(sub=sub, n_files=len(shas), n_extracted=len(ex), all_sha256_verified=True, tar_sha256=sha(loc), at=pv.est(),
               files=shas)
    (pv.PODS / name / ('DR_FETCH_%s.json' % sub.replace('/', '_'))).write_text(json.dumps(rec, indent=0), encoding='utf-8')
    loc.unlink()
    print('%s: %d files (%d new) into %s, all sha256 verified' % (sub, len(shas), len(ex), dest))


def main():
    a = sys.argv[1:]
    c = a[0]
    if c == 'stage-code': stage_code()
    elif c == 'stage-data': stage_data(a[1])
    elif c == 'up': up(a[1], a[a.index('--gpu') + 1] if '--gpu' in a else 'NVIDIA GeForce RTX 4090',
                      float(a[a.index('--deadline-h') + 1]) if '--deadline-h' in a else 4.0)
    elif c == 'upload': upload(a[1], a[2])
    elif c == 'run': run(a[1], a[2], a[3:])
    elif c == 'status': status(a[1], a[2] if len(a) > 2 else None)
    elif c == 'fetch': fetch(a[1], a[2])
    elif c == 'down': pv.delete(a[1], a[2] if len(a) > 2 else '')
    else: raise SystemExit('unknown command')


if __name__ == '__main__':
    main()
