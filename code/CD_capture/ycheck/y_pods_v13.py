"""Y (A11 sec. 6b) on a RunPod pod: stage a bundle (both Y programs, their frozen imports, the frozen B2 arrays (FREEZE_B_add7), CD's CV0
arrays of the 105 lead-braking runs, LOCK_A11), set it up (CPython 3.12 + the laptop venv's pins, as tools\\b7_pods_v13.py), run the
first and second programs with --calib export, and fetch their outputs and calibration jobs. It moves files and starts the frozen
programs; it computes no value. New file, 21 Nov 2026 (Claude Opus 5.5, session CD), after LOCK_A11 and FREEZE_CD_add4.
Usage (.venv\\Scripts\\python.exe -I -B -X utf8 ycheck\\y_pods_v13.py CMD NAME [...]):
  stage                        build pods\\y_staging\\y_bundle.tar(.json)
  setup NAME                   install, upload + verify the bundle, links, import check of both programs
  run NAME THREADS             start both programs in the background, one after the other (first, then second), --calib export
  status NAME                  tail of the two logs
  fetch NAME                   download the outputs and the calibration jobs into ycheck\\out\\pod\\ and recount\\out\\pod\\ (SHA-256 checked)
"""
import hashlib, json, pathlib, sys, tarfile
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent; WORK = CD.parent; V13 = WORK.parent
sys.path.insert(0, str(CD / 'tools'))
import pods_v13 as pv                                   # noqa: E402
import b7_pods_v13 as BP                                # noqa: E402  (helpers: bundle, walk, ssh, put, get, PINS, CODEX, P, OPENLOOP)

STAGE = CD / 'pods' / 'y_staging'
R = '/root/yy'
PY = '/opt/b7py/bin/python'
A = 'ARS_TRIAL/revision_v13/'
LINKS = {r'<library folder>\openloop': R + '/P/09_redesign/m2_decisions/openloop',
         r'<library folder>': R + '/P',
         r'ARS_TRIAL\revision_v12\analysis': R + '/ARS_TRIAL/revision_v12/analysis',
         r'ARS_TRIAL\revision_v11\analysis': R + '/ARS_TRIAL/revision_v11/analysis',
         r'ARS_TRIAL': R + '/ARS_TRIAL',
         r'<library folder>\149_supported_sensor_preparation_20261101': R + '/codex'}
ENV = ('export V13_CODEX_ROOT=%s/codex V13_P_ROOT=%s/P OPENBLAS_CORETYPE=Haswell OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1' % (R, R))
FIRST = R + '/' + A + 'work/CD_capture/ycheck/y_twin_v13.py'
SECOND = R + '/' + A + 'work/CD_capture/recount/rc_y_twin_v13.py'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def lead_rids():
    d = json.loads((CD / 'CASES_C_v13.json').read_text(encoding='utf-8'))
    return sorted(f"pc13_{c['case']}_native" for c in d['cases'] if c['family'] == 'lead_braking')


def stage():
    STAGE.mkdir(parents=True, exist_ok=True)
    junk = lambda p: '__pycache__' in p.parts or p.suffix in ('.pyc', '.nbi', '.nbc') or p.name.startswith('tmp')
    m = []
    for sub in ('code', 'sources', 'vendor', 'legacy86/vendor/nuscenes-devkit/python-sdk', 'contracts'):
        m += BP.walk(BP.CODEX / sub, 'codex/' + sub, junk)
    m += [(BP.P / '09_redesign' / 'm2_decisions' / 'openloop' / f, 'P/09_redesign/m2_decisions/openloop/' + f) for f in BP.OPENLOOP]
    m += [(BP.P / '11_ojits' / 'A6R' / 'code' / 'optA_lib_v02.py', 'P/11_ojits/A6R/code/optA_lib_v02.py')]
    m += [(BP.DL / 'ARS_TRIAL' / 'revision_v11' / 'analysis' / 'rev_common_v01.py', 'ARS_TRIAL/revision_v11/analysis/rev_common_v01.py'),
          (BP.DL / 'ARS_TRIAL' / 'revision_v12' / 'analysis' / 'a9_common_v01.py', 'ARS_TRIAL/revision_v12/analysis/a9_common_v01.py')]
    m += BP.walk(WORK / 'shared' / 'trackers', A + 'work/shared/trackers', junk)
    m += [(CD / 'analysis' / f, A + 'work/CD_capture/analysis/' + f) for f in ('cd_common_v13.py', 'gl_fast_v13.py', 'calib_remote_v13.py')]
    m += [(CD / f, A + 'work/CD_capture/' + f) for f in ('CASES_C_v13.json', 'REPLACEMENTS_C_v13.json')]
    m += [(HERE / f, A + 'work/CD_capture/ycheck/' + f) for f in ('y_twin_v13.py', 'y_calib_remote_v13.py', 'CD_DEFINITIONS_Y_v13.md')]
    m += [(CD / 'recount' / f, A + 'work/CD_capture/recount/' + f) for f in ('rc_core_v13.py', 'rc_kern_v13.py', 'rc_calib_remote_v13.py',
                                                                            'rc_y_twin_v13.py', 'rc_y_kern_v13.py', 'rc_y_calib_remote_v13.py')]
    m += [(V13 / f, A + f) for f in ('LOCK_A11.txt', 'LOCK_A10_2.txt', 'LOCK_A10_2c.txt')]
    m += [(WORK / 'locks' / 'FREEZE_B_add7.json', A + 'work/locks/FREEZE_B_add7.json')]
    for rid in lead_rids():
        m.append((WORK / 'B_retrack' / 'out' / 'retrack_fresh' / 'B2' / (rid + '_arrays.npz'), A + 'work/B_retrack/out/retrack_fresh/B2/%s_arrays.npz' % rid))
        m.append((CD / 'arrays' / 'CV0' / (rid + '.npz'), A + 'work/CD_capture/arrays/CV0/%s.npz' % rid))
    ps = STAGE / 'pod_links_y.py'
    ps.write_text('import os, json\nL = %s\nos.makedirs(%r, exist_ok=True)\nos.chdir(%r)\nfor k, v in L.items():\n'
                  '    if not os.path.islink(k): os.symlink(v, k)\nprint(json.dumps({k: os.path.realpath(k) for k in L}))\n'
                  % (json.dumps(LINKS), R + '/job', R + '/job'), encoding='utf-8')
    m += [(ps, 'pod_links_y.py')]
    man = BP.bundle(STAGE / 'y_bundle.tar', m)
    print('y bundle: %d files, %.1f MB' % (len(man), (STAGE / 'y_bundle.tar').stat().st_size / 1e6))


def verify_remote(name):
    man = json.loads((STAGE / 'y_bundle.json').read_text(encoding='utf-8'))['files']
    lst = STAGE / 'y_bundle.sha256.txt'
    lst.write_text(''.join('%s  %s\n' % (h, a) for a, h in man.items()), encoding='ascii', newline='\n')
    BP.put(name, lst, R + '/' + lst.name)
    out = BP.ssh(name, 'cd %s && sha256sum -c --quiet %s > %s.check 2>&1; echo rc=$?' % (R, lst.name, lst.name))
    if 'rc=0' not in out: raise SystemExit('%s: sha256 check failed: %s' % (name, out[-500:]))
    return len(man)


def setup(name):
    check = '%s -c "import sys,numpy,numba,scipy; print(sys.version.split()[0], numpy.__version__, numba.__version__)"' % PY
    have = pv.ssh(name, check, timeout=120)
    if have.returncode != 0:
        BP.ssh(name, '( python3 -m pip install -q uv && uv venv -q --clear -p 3.12 /opt/b7py && uv pip install -q --python %s %s ) > /root/yy_setup.log 2>&1; '
                     'tail -3 /root/yy_setup.log' % (PY, BP.PINS), timeout=2400)
        have = pv.ssh(name, check, timeout=120)
    vers = have.stdout.strip()
    if have.returncode != 0 or vers.split()[1:] != ['2.5.4', '0.68.1']: raise SystemExit('%s: environment not ready: %s' % (name, vers))
    BP.ssh(name, 'mkdir -p %s' % R)
    BP.put(name, STAGE / 'y_bundle.tar', R + '/y_bundle.tar')
    BP.ssh(name, 'cd %s && tar xf y_bundle.tar && rm -f y_bundle.tar' % R)
    n = verify_remote(name)
    links = BP.ssh(name, 'cd %s && /usr/bin/env python3 pod_links_y.py' % R)
    imp = BP.ssh(name, '%s && cd %s/job && %s -I -B -X utf8 -c "import sys; sys.path[:0] = [\'%s\', \'%s\', \'%s\']; import cd_common_v13, rc_core_v13, '
                       'rc_y_kern_v13; print(\'imports ok\')"' % (ENV, R, PY, FIRST.rsplit('/', 1)[0].replace('/ycheck', '/analysis'),
                                                               SECOND.rsplit('/', 1)[0], FIRST.rsplit('/', 1)[0]), timeout=900)
    rec = dict(python_numpy_numba=vers, files_verified=n, links=json.loads(links.strip().splitlines()[-1]), import_check=imp.strip()[-300:], at=pv.est())
    (CD / 'pods' / name).mkdir(parents=True, exist_ok=True)
    (CD / 'pods' / name / 'Y_SETUP.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print(json.dumps(rec)[:600])


def run(name, threads):
    cmd = ('%s NUMBA_NUM_THREADS=%d && cd %s/job && (setsid nohup bash -c "%s -I -B -X utf8 %s --intervals calibrated --calib export > %s/first.log 2>&1; '
           '%s -I -B -X utf8 %s --intervals calibrated --calib export > %s/second.log 2>&1" > /dev/null 2>&1 < /dev/null &) ; sleep 2; echo started'
           % (ENV, int(threads), R, PY, FIRST, R, PY, SECOND, R))
    print(BP.ssh(name, cmd).strip(), pv.est())


def status(name):
    print(BP.ssh(name, 'tail -3 %s/first.log 2>/dev/null; echo ---; tail -3 %s/second.log 2>/dev/null; echo; pgrep -fc y_twin_v13 || true' % (R, R)).strip())


def fetch(name):
    base = R + '/' + A + 'work/CD_capture/'
    out = BP.ssh(name, 'cd %s && ls ycheck/out/*.json analysis/out/calib/y_main.* recount/out/*Y_TWIN* recount/out/calib*/rc_y* 2>/dev/null' % base)
    files = [x for x in out.split() if x]
    BP.ssh(name, 'cd %s && sha256sum %s > %s/Y_FETCH_SHA.txt && tar cf %s/y_out.tar %s %s/first.log %s/second.log' % (base, ' '.join(files), R, R, ' '.join(files), R, R))
    loc = STAGE / ('y_out_%s.tar' % name)
    BP.get(name, R + '/y_out.tar', str(loc)); BP.get(name, R + '/Y_FETCH_SHA.txt', str(STAGE / 'Y_FETCH_SHA.txt'))
    shas = dict(reversed(l.split()) for l in (STAGE / 'Y_FETCH_SHA.txt').read_text().splitlines())
    dest = CD / 'pods' / name / 'y_out'; dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(loc) as t:
        for m in t.getmembers():
            assert m.isfile() and '..' not in m.name
            t.extract(m, dest, filter='data')
    bad = [f for f, h in shas.items() if sha(dest / f.lstrip('/')) != h] if all((dest / f.lstrip('/')).exists() for f in shas) else ['missing']
    print('fetched', len(shas), 'files into', dest, '; sha mismatches:', bad)


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'stage': stage()
    elif c == 'setup': setup(sys.argv[2])
    elif c == 'run': run(sys.argv[2], int(sys.argv[3]))
    elif c == 'status': status(sys.argv[2])
    elif c == 'fetch': fetch(sys.argv[2])
    else: raise SystemExit(__doc__)
