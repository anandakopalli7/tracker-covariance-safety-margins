r"""AMENDMENT_12 sec. 5b: moves the sec. 5b pipeline to a RunPod pod and its outputs back. New file, 22 Nov 2026 (Claude Opus 5.5,
worker of package F); adapted from F_dropout\code\dr_pods_v02.py (read only; the B7 pod route: the Windows paths that the frozen
scoring modules hard-code are links named literally after them in the job folder). This file only moves files and starts programs;
it computes no value. Pods are created and deleted through fpods_n_v01.py (F's helper with prefix claude-v13f-n; spend-log rows).
On the pod, R = /root/fn mirrors ...\Downloads: R/ARS_TRIAL/revision_v13/{LOCK_*.txt, work/F_nuscenes/{lib,cache,out},
work/F_dropout_nus/code, work/shared/trackers}, R/P/11_ojits/A6R/code/optA_lib_v02.py, R/ARS_TRIAL/revision_v1{1,2}/analysis.
Two Python 3.12 environments (uv): /opt/fnt for tracking and arrays = the laptop interpreter's versions of every package the
path imports (PINS_T; no numba, shapely, lap, pyquaternion, hydra, omegaconf, so CANMOT uses F's stand-ins for them, as on
the laptop); /opt/fnk for scoring = F's venv: numpy 2.5.5, numba 0.68.1, llvmlite 0.50.0.
  stage-code                 pods\code_bundle.tar.gz (+ .json manifest): this folder's code, F's lib (code149, vendor149, devkit
                             python-sdk, shims_v01, tracker_config.json), shared trk_score / trk_env, optA_lib_v02, a9_common, rev_common,
                             LOCK_A10_2.txt, the links script
  stage-data val             F's cache\val, cache\clear_v02\val, cache\arrays_T1\val (tracker-independent key check), PBAR_T1_train_v01.json
  stage-data train SCENE...  F's cache\train and cache\clear_v02\train of the named design-split scenes (code test of the masked chain)
  stage-data lock            LOCK_A12c.txt (refuses without it)
  up NAME [--gpu G] [--deadline-h H]   create (fpods_n) and set up both environments, upload the code bundle (sha-checked), links
  upload NAME WHICH          upload a bundle, verify every file's sha256 on the pod
  run NAME TAG ENV CMD...    start `<ENV python> -I -B -X utf8 CMD...` in R/job (background; log R/TAG.log); ENV = t | k
  sh NAME CMD                run a shell command on the pod (prints output)
  fetch NAME SUBPATH         tar R/ARS_TRIAL/revision_v13/work/F_dropout_nus/SUBPATH, download, verify every sha256, extract into this
                             folder (never overwrites a different file)
  down NAME NOTE             delete the pod (fpods_n; spend-log row)
Usage: python -I -B fn_pods_v01.py CMD ...
"""
import hashlib, json, pathlib, sys, tarfile, time
HERE = pathlib.Path(__file__).resolve().parent
HOME = HERE.parent
WORK = HOME.parent
V13 = WORK.parent
sys.path.insert(0, str(HERE))
import fpods_n_v01 as pv                               # noqa: E402

DL = pathlib.Path(r'<user folder>')
P = DL / '<earlier-phase folder 1>'
FN = WORK / 'F_nuscenes'
STAGE = HOME / 'pods'
R = '/root/fn'
PYT = '/opt/fnt/bin/python'
PYK = '/opt/fnk/bin/python'
PINS_T = ('numpy==2.5.4 scipy==1.18.1 pandas==2.2.2 matplotlib==3.11.2 opencv-python-headless==4.14.0.94 scikit-learn==1.9.1 '
          'pillow==13.0.0 PyYAML==6.0.2 cloudpickle==3.1.2 joblib==1.6.0 tqdm==4.70.1 psutil==7.0.0 cachetools==7.3.0 threadpoolctl==3.8.0 '
          'contourpy==1.4.0 kiwisolver==1.5.1 fonttools==4.68.0 cycler==0.12.1 pyparsing==3.3.3 python-dateutil==2.9.0.post0 pytz==2024.1 '
          'tzdata==2024.1 packaging==24.2 six==1.16.0 narwhals==2.28.0 cffi==2.1.1 pycparser==2.22 charset-normalizer==3.4.1')
# = the laptop interpreter's versions of every third-party package the T1 tracker and planner path imports (traced 22 Nov 00:50:
#   CD's pins without numba / llvmlite, which the laptop interpreter does not have, so F's numba stand-in is used as on the laptop)
PINS_K = 'numpy==2.5.5 numba==0.68.1 llvmlite==0.50.0'
LINKS = {r'<library folder>': R + '/P',
         r'ARS_TRIAL\revision_v12\analysis': R + '/ARS_TRIAL/revision_v12/analysis',
         r'ARS_TRIAL\revision_v11\analysis': R + '/ARS_TRIAL/revision_v11/analysis'}
ENV = ('export OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMBA_CACHE_DIR=%s/numba_cache' % R)
HN = R + '/ARS_TRIAL/revision_v13/work/F_dropout_nus'
A13 = 'ARS_TRIAL/revision_v13/'


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


def junk(p):
    return '__pycache__' in p.parts or p.suffix in ('.pyc', '.nbi', '.nbc') or p.name.startswith('tmp')


def stage_code():
    STAGE.mkdir(parents=True, exist_ok=True)
    m = [(f, A13 + 'work/F_dropout_nus/code/' + f.name) for f in sorted(HERE.glob('*')) if f.is_file() and f.suffix in ('.py', '.sh', '.txt')
         and not f.name.startswith(('fn_pods', 'fpods'))]
    for sub in ('code149', 'vendor149', 'shims_v01'):
        m += walk(FN / 'lib' / sub, A13 + 'work/F_nuscenes/lib/' + sub, junk)
    m += walk(FN / 'lib' / 'devkit' / 'python-sdk', A13 + 'work/F_nuscenes/lib/devkit/python-sdk', junk)
    m += [(FN / 'lib' / 'tracker_config.json', A13 + 'work/F_nuscenes/lib/tracker_config.json')]
    m += [(WORK / 'shared' / 'trackers' / f, A13 + 'work/shared/trackers/' + f) for f in ('trk_score_v01.py', 'trk_env_v01.py')]
    m += [(P / '11_ojits' / 'A6R' / 'code' / 'optA_lib_v02.py', 'P/11_ojits/A6R/code/optA_lib_v02.py')]
    m += [(DL / 'ARS_TRIAL' / 'revision_v11' / 'analysis' / 'rev_common_v01.py', 'ARS_TRIAL/revision_v11/analysis/rev_common_v01.py'),
          (DL / 'ARS_TRIAL' / 'revision_v12' / 'analysis' / 'a9_common_v01.py', 'ARS_TRIAL/revision_v12/analysis/a9_common_v01.py')]
    m += [(V13 / 'LOCK_A10_2.txt', A13 + 'LOCK_A10_2.txt')]
    m += [(FN / 'out' / 'F_HELDOUT_v02.json', A13 + 'work/F_nuscenes/out/F_HELDOUT_v02.json')]   # F's exported values (fn09 reference)
    ps = STAGE / 'pod_links_fn.py'
    ps.write_text('import os, json\nL = %s\nos.makedirs(%r, exist_ok=True)\nos.chdir(%r)\nfor k, v in L.items():\n'
                  '    if not os.path.islink(k): os.symlink(v, k)\nprint(json.dumps({k: os.path.realpath(k) for k in L}))\n'
                  % (json.dumps(LINKS), R + '/job', R + '/job'), encoding='utf-8')
    m += [(ps, 'pod_links_fn.py')]
    bundle(STAGE / 'code_bundle.tar.gz', m)


def stage_data(which, scenes=()):
    STAGE.mkdir(parents=True, exist_ok=True)
    m = []
    if which == 'val':
        for sub in ('val', 'clear_v02/val', 'arrays_T1/val'):
            d = FN / 'cache' / pathlib.Path(sub)
            fs = sorted(p for p in d.glob('scene-*.npz') if '.tmp' not in p.name)
            assert len(fs) == 150, (sub, len(fs))
            m += [(f, A13 + 'work/F_nuscenes/cache/%s/%s' % (sub, f.name)) for f in fs]
        m += [(FN / 'out' / 'PBAR_T1_train_v01.json', A13 + 'work/F_nuscenes/out/PBAR_T1_train_v01.json')]
    elif which == 'train':
        assert scenes
        for s in scenes:
            for sub in ('train', 'clear_v02/train'):
                f = FN / 'cache' / pathlib.Path(sub) / (s + '.npz')
                assert f.is_file(), f
                m.append((f, A13 + 'work/F_nuscenes/cache/%s/%s' % (sub, f.name)))
    elif which == 'lock':
        lk = V13 / 'LOCK_A12c.txt'
        if not lk.is_file(): raise SystemExit('REFUSED: no LOCK_A12c.txt')
        m.append((lk, A13 + 'LOCK_A12c.txt'))
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
    t0 = time.time()
    put(name, t, R + '/' + t.name)
    ssh(name, 'cd %s && tar xzf %s && rm -f %s' % (R, t.name, t.name), timeout=1800)
    n = verify_remote(name, STAGE / ('%s_bundle.json' % which))
    print('%s: %s bundle, %d files verified on the pod (%.0f s)' % (name, which, n, time.time() - t0))


def up(name, gpu, deadline_h):
    if not (pv.PODS / name / 'pod.json').is_file():
        pv.create(name, gpu, deadline_h, 'AMENDMENT_12 sec. 5b nuScenes dropouts: tracking / arrays / scoring')
    nproc = ssh(name, 'nproc; cat /sys/fs/cgroup/cpu.max 2>/dev/null || cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us').split()
    ck_t = '%s -c "import sys,numpy,scipy; print(sys.version.split()[0], numpy.__version__, scipy.__version__)"' % PYT
    ck_k = '%s -c "import sys,numpy,numba; print(sys.version.split()[0], numpy.__version__, numba.__version__)"' % PYK
    if pv.ssh(name, ck_t, timeout=120).returncode != 0 or pv.ssh(name, ck_k, timeout=120).returncode != 0:
        ssh(name, '( python3 -m pip install -q uv && uv venv -q --clear -p 3.12 /opt/fnt && uv pip install -q --python %s %s && '
                  'uv venv -q --clear -p 3.12 /opt/fnk && uv pip install -q --python %s %s ) > /root/fn_setup.log 2>&1; tail -3 /root/fn_setup.log'
            % (PYT, PINS_T, PYK, PINS_K), timeout=2400)
    vt = ssh(name, ck_t, timeout=120).strip(); vk = ssh(name, ck_k, timeout=120).strip()
    if vt.split()[1:] != ['2.5.4', '1.18.1'] or vk.split()[1:] != ['2.5.5', '0.68.1']:
        raise SystemExit('%s: environment not ready: %s | %s' % (name, vt, vk))
    frz = ssh(name, '%s -m pip --version >/dev/null 2>&1; uv pip freeze --python %s; echo ---; uv pip freeze --python %s' % (PYT, PYT, PYK))
    upload(name, 'code')
    links = ssh(name, 'cd %s && /usr/bin/env python3 pod_links_fn.py' % R)
    rec = dict(nproc_and_quota=nproc, fnt=vt, fnk=vk, freeze=frz, links=json.loads(links.strip().splitlines()[-1]), at=pv.est())
    (pv.PODS / name / 'FN_SETUP.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print(json.dumps(rec))


def run(name, tag, env, cmd):
    py = {'t': PYT, 'k': PYK}[env]
    ssh(name, '%s && cd %s/job && (setsid nohup %s -I -B -X utf8 %s > %s/%s.log 2>&1 < /dev/null &) ; sleep 2; echo started'
        % (ENV, R, py, ' '.join(cmd), R, tag))
    print('started', tag, pv.est())


def fetch(name, sub):
    tarn = 'fetch_%s.tar' % sub.replace('/', '_')
    out_ = ssh(name, 'cd %s && find %s -type f ! -name "*.tmp.npz" | sort > /root/fl.txt && test -s /root/fl.txt && '
                     'xargs -a /root/fl.txt sha256sum > /root/SHA_fetch.txt < /dev/null && tar cf %s/%s -T /root/fl.txt && echo FETCH_READY'
               % (HN, sub, R, tarn), timeout=1800)
    if 'FETCH_READY' not in out_: raise SystemExit('%s: nothing to fetch under %s' % (name, sub))
    loc = STAGE / tarn
    get(name, '%s/%s' % (R, tarn), str(loc))
    get(name, '/root/SHA_fetch.txt', str(STAGE / ('SHA_' + tarn + '.txt')))
    shas = dict(reversed(l.split(None, 1)) for l in (STAGE / ('SHA_' + tarn + '.txt')).read_text().splitlines() if l.strip())
    shas = {k.strip(): v for k, v in shas.items()}
    ex = []
    with tarfile.open(loc) as t:
        for mbr in t.getmembers():
            assert mbr.isfile() and '..' not in mbr.name
            if (HOME / mbr.name).exists():
                if sha(HOME / mbr.name) != shas[mbr.name]:
                    raise SystemExit('REFUSED: %s exists locally with other content' % mbr.name)
                continue
            t.extract(mbr, HOME, filter='data'); ex.append(mbr.name)
    bad = [x for x in ex if sha(HOME / x) != shas[x]]
    if bad: raise SystemExit('%d downloaded files differ from the pod sha256: %s' % (len(bad), bad[:3]))
    rec = dict(sub=sub, n_files=len(shas), n_extracted=len(ex), all_sha256_verified=True, tar_sha256=sha(loc), at=pv.est(), files=shas)
    (pv.PODS / name / ('FN_FETCH_%s.json' % sub.replace('/', '_'))).write_text(json.dumps(rec, indent=0), encoding='utf-8')
    loc.unlink()
    print('%s: %d files (%d new) into %s, all sha256 verified' % (sub, len(shas), len(ex), HOME))


def main():
    a = sys.argv[1:]
    c = a[0]
    if c == 'stage-code': stage_code()
    elif c == 'stage-data': stage_data(a[1], a[2:])
    elif c == 'up': up(a[1], a[a.index('--gpu') + 1] if '--gpu' in a else 'NVIDIA GeForce RTX 4090',
                      float(a[a.index('--deadline-h') + 1]) if '--deadline-h' in a else 3.0)
    elif c == 'upload': upload(a[1], a[2])
    elif c == 'run': run(a[1], a[2], a[3], a[4:])
    elif c == 'sh': print(ssh(a[1], ' '.join(a[2:])), end='')
    elif c == 'fetch': fetch(a[1], a[2])
    elif c == 'down': pv.delete(a[1], a[2] if len(a) > 2 else '')
    else: raise SystemExit('unknown command')


if __name__ == '__main__':
    main()
