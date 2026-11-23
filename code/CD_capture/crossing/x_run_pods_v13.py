"""X (A11 sec. 3): run the frozen X programs (first: x_cross_v13, x_desc_v13; second: rc_x_cross_v13, rc_x_desc_v13) on one pod over the
full analysed set. Orchestration only (moves files, starts frozen programs; no value is computed here). New file, 21 Nov 2026 (Claude
Opus 5.5, session CD), after LOCK_A11 and FREEZE_CD_add5.
Usage (.venv\\Scripts\\python.exe -I -B -X utf8 crossing\\x_run_pods_v13.py CMD NAME [...]):
  stage                     bundle: code (as ycheck\\y_pods_v13.py) + crossing and recount X programs + CASES_X_PC (+ REPLACEMENTS_X if any)
                            + arrays_x\\CV0\\*.npz (fetched from the capture pods, SHA-256 checked) + LOCK_A11
  setup NAME                install (if needed), upload + verify, links, import check
  run NAME THREADS          start, one after the other at nice 10: x_cross (calibrated, export), x_desc, rc_x_cross (calibrated, export), rc_x_desc
  status NAME | fetch NAME  logs | download every output and calibration job (SHA-256 checked) into pods\\NAME\\x_out\\
"""
import hashlib, json, pathlib, sys, tarfile
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent; WORK = CD.parent; V13 = WORK.parent
sys.path[:0] = [str(CD / 'tools'), str(CD / 'ycheck')]
import pods_v13 as pv                                   # noqa: E402
import b7_pods_v13 as BP                                # noqa: E402
import y_pods_v13 as YP                                 # noqa: E402  (LINKS, ENV, setup pattern; frozen in add5)

STAGE = CD / 'pods' / 'xrun_staging'
R = '/root/xr'
A = YP.A
CASES_SHA = '58902be5ce022b314148308140cb8fc9373bc7aee401531367d456755409a31e'
LINKS = {k: v.replace(YP.R, R) for k, v in YP.LINKS.items()}
ENV = YP.ENV.replace(YP.R, R)
BASE = R + '/' + A + 'work/CD_capture'


def sha(p):
    return YP.sha(p)


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
    cr = ['x_cross_v13.py', 'x_desc_v13.py', 'CASES_X_PC_v13.json', 'CD_DEFINITIONS_X_v13.md', 'CD_DEFINITIONS_X_DESC_v13.md']
    if (HERE / 'REPLACEMENTS_X_v13.json').is_file(): cr.append('REPLACEMENTS_X_v13.json')
    m += [(HERE / f, A + 'work/CD_capture/crossing/' + f) for f in cr]
    m += [(CD / 'recount' / f, A + 'work/CD_capture/recount/' + f) for f in ('rc_core_v13.py', 'rc_kern_v13.py', 'rc_calib_remote_v13.py',
                                                                            'rc_x_cross_v13.py', 'rc_x_kern_v13.py', 'rc_x_calib_remote_v13.py', 'rc_x_desc_v13.py')]
    m += [(V13 / f, A + f) for f in ('LOCK_A11.txt', 'LOCK_A10_2.txt', 'LOCK_A10_2c.txt')]
    arr = sorted((CD / 'arrays_x' / 'CV0').glob('pc13x_*.npz'))
    m += [(p, A + 'work/CD_capture/arrays_x/CV0/' + p.name) for p in arr]
    ps = STAGE / 'pod_links_xr.py'
    ps.write_text('import os, json\nL = %s\nos.makedirs(%r, exist_ok=True)\nos.chdir(%r)\nfor k, v in L.items():\n'
                  '    if not os.path.islink(k): os.symlink(v, k)\nprint(json.dumps({k: os.path.realpath(k) for k in L}))\n'
                  % (json.dumps(LINKS), R + '/job', R + '/job'), encoding='utf-8')
    m += [(ps, 'pod_links_xr.py')]
    man = BP.bundle(STAGE / 'xr_bundle.tar', m)
    print('xr bundle: %d files (%d arrays), %.1f MB' % (len(man), len(arr), (STAGE / 'xr_bundle.tar').stat().st_size / 1e6))


def setup(name):
    check = '%s -c "import sys,numpy,numba,scipy; print(sys.version.split()[0], numpy.__version__, numba.__version__)"' % YP.PY
    have = pv.ssh(name, check, timeout=120)
    if have.returncode != 0:
        BP.ssh(name, '( python3 -m pip install -q uv && uv venv -q --clear -p 3.12 /opt/b7py && uv pip install -q --python %s %s ) > /root/xr_setup.log 2>&1; '
                     'tail -3 /root/xr_setup.log' % (YP.PY, BP.PINS), timeout=2400)
        have = pv.ssh(name, check, timeout=120)
    if have.returncode != 0 or have.stdout.split()[1:] != ['2.5.4', '0.68.1']: raise SystemExit('%s: environment not ready' % name)
    BP.ssh(name, 'rm -rf %s && mkdir -p %s' % (R, R))
    BP.put(name, STAGE / 'xr_bundle.tar', R + '/xr_bundle.tar')
    BP.ssh(name, 'cd %s && tar xf xr_bundle.tar && rm -f xr_bundle.tar' % R)
    man = json.loads((STAGE / 'xr_bundle.json').read_text(encoding='utf-8'))['files']
    lst = STAGE / 'xr_bundle.sha256.txt'
    lst.write_text(''.join('%s  %s\n' % (h, a) for a, h in man.items()), encoding='ascii', newline='\n')
    BP.put(name, lst, R + '/' + lst.name)
    out = BP.ssh(name, 'cd %s && sha256sum -c --quiet %s > %s.check 2>&1; echo rc=$?' % (R, lst.name, lst.name))
    if 'rc=0' not in out: raise SystemExit('%s: sha256 check failed' % name)
    BP.ssh(name, 'cd %s && /usr/bin/env python3 pod_links_xr.py' % R)
    imp = BP.ssh(name, '%s && cd %s/job && %s -I -B -X utf8 -c "import sys; sys.path[:0] = [\'%s/analysis\', \'%s/recount\']; import cd_common_v13, rc_core_v13, '
                       'rc_x_kern_v13; print(\'imports ok\')"' % (ENV, R, YP.PY, BASE, BASE), timeout=900)
    rec = dict(files_verified=len(man), import_check=imp.strip()[-100:], at=pv.est())
    (CD / 'pods' / name / 'XR_SETUP.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print(json.dumps(rec))


def run(name, threads):
    py = YP.PY + ' -I -B -X utf8 '
    steps = [py + BASE + '/crossing/x_cross_v13.py --cases-sha %s --intervals calibrated --calib export > %s/x_cross.log 2>&1' % (CASES_SHA, R),
             py + BASE + '/crossing/x_desc_v13.py --cases-sha %s > %s/x_desc.log 2>&1' % (CASES_SHA, R),
             py + BASE + '/recount/rc_x_cross_v13.py --family pedestrian_crossing --n 390 --cases-sha %s --intervals calibrated --calib export '
                         '> %s/rc_x_cross.log 2>&1' % (CASES_SHA, R),
             py + BASE + '/recount/rc_x_desc_v13.py --cases-sha %s --n 390 > %s/rc_x_desc.log 2>&1' % (CASES_SHA, R)]
    cmd = ('%s NUMBA_NUM_THREADS=%d && cd %s/job && (setsid nohup nice -n 10 bash -c "%s" > /dev/null 2>&1 < /dev/null &) ; sleep 2; echo started'
           % (ENV, int(threads), R, '; '.join(steps)))
    print(BP.ssh(name, cmd).strip(), pv.est())


def status(name):
    print(BP.ssh(name, 'for f in x_cross x_desc rc_x_cross rc_x_desc; do echo == $f; tail -2 %s/$f.log 2>/dev/null; done' % R).strip())


def fetch(name):
    out = BP.ssh(name, 'cd %s && ls crossing/out/X_*.json recount/out/RC_X_*.json analysis/out/calib/x_ped_main.* recount/out/calib*/rc_x* 2>/dev/null; true' % BASE)
    files = [x for x in out.split() if x]
    BP.ssh(name, 'cd %s && sha256sum %s > %s/X_FETCH_SHA.txt && tar cf %s/x_out.tar %s && cp %s/*.log %s/ 2>/dev/null; true'
           % (BASE, ' '.join(files), R, R, ' '.join(files), R, BASE))
    dest = CD / 'pods' / name / 'x_out'; dest.mkdir(parents=True, exist_ok=True)
    loc = STAGE / ('x_out_%s.tar' % name)
    BP.get(name, R + '/x_out.tar', str(loc)); BP.get(name, R + '/X_FETCH_SHA.txt', str(dest / 'X_FETCH_SHA.txt'))
    with tarfile.open(loc) as t:
        for mm in t.getmembers():
            assert mm.isfile() and '..' not in mm.name
            t.extract(mm, dest, filter='data')
    shas = dict(reversed(l.split()) for l in (dest / 'X_FETCH_SHA.txt').read_text().splitlines())
    bad = [f for f, h in shas.items() if sha(dest / f) != h]
    print('fetched', len(shas), 'files into', dest, '; sha mismatches:', bad)


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'stage': stage()
    elif c == 'setup': setup(sys.argv[2])
    elif c == 'run': run(sys.argv[2], int(sys.argv[3]))
    elif c == 'status': status(sys.argv[2])
    elif c == 'fetch': fetch(sys.argv[2])
    else: raise SystemExit(__doc__)
