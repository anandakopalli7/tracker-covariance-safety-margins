"""Heading-vs-error extraction (crossing/x_heading_v13.py) on one pod. Uses crossing/x_pods_v13 (frozen) for the code bundle, setup and
acceptance (with the openloop link as xlink.py), then uploads the 390 X archives + stored arrays and runs x_heading there.
Usage: python hpod.py stage | up NAME | run NAME [W] | status NAME | fetch NAME"""
import json, pathlib, sys, tarfile
CD = pathlib.Path(r'ARS_TRIAL\revision_v13\work\CD_capture')
sys.path[:0] = [str(CD / 'crossing'), str(CD / 'tools')]
import x_pods_v13 as XP                  # noqa: E402
import x_heading_v13 as XH               # noqa: E402
BP = XP.BP; pv = XP.pv
STAGE = CD / 'pods' / 'h_staging'
PRE = 'ARS_TRIAL/revision_v13/work/CD_capture/'
WIN = r'<library folder>\openloop'
LINK = "mkdir -p %s/job && cd %s/job && ( [ -L '%s' ] || ln -s %s/P/09_redesign/m2_decisions/openloop '%s' ) && ls -la | grep -c openloop" % (XP.R, XP.R, WIN, XP.R, WIN)
HX = XP.R + '/' + PRE + 'crossing/x_heading_v13.py'
HOUT = XP.R + '/' + PRE + 'crossing/heading'


def stage():
    STAGE.mkdir(parents=True, exist_ok=True)
    m = [(CD / 'crossing' / f, PRE + 'crossing/' + f) for f in ('x_heading_v13.py', 'CASES_X_PC_v13.json', 'REPLACEMENTS_X_v13.json')]
    m += [(CD / 'crossing' / 'out' / 'ALIAS_RETRIES_X_v13.json', PRE + 'crossing/out/ALIAS_RETRIES_X_v13.json')]
    for rid, cid in XH.run_list():
        m += [(CD / 'arrays_x' / 'CV0' / (rid + '.npz'), PRE + 'arrays_x/CV0/%s.npz' % rid)]
        for f in ('claude_main_%s.tar.gz' % cid, 'claude_main_%s.tar.gz.receipt.json' % cid):
            m += [(CD / 'archives' / cid / f, PRE + 'archives/%s/%s' % (cid, f))]
    man = BP.bundle(STAGE / 'heading_data.tar', m)
    print('heading data: %d files, %.0f MB' % (len(man), (STAGE / 'heading_data.tar').stat().st_size / 1e6))


def up(name):
    try: print('link', BP.ssh(name, LINK).strip())
    except SystemExit as e: print('link step (before the bundle exists):', str(e)[:200])
    XP.setup(name)
    BP.ssh(name, LINK)
    XP.accept(name)
    BP.put(name, STAGE / 'heading_data.tar', XP.R + '/heading_data.tar')
    BP.ssh(name, 'cd %s && tar xf heading_data.tar && rm -f heading_data.tar' % XP.R, timeout=1800)
    lst = STAGE / 'heading_data.sha256.txt'
    man = json.loads((STAGE / 'heading_data.json').read_text(encoding='utf-8'))['files']
    lst.write_text(''.join('%s  %s\n' % (h, a) for a, h in man.items()), encoding='ascii', newline='\n')
    BP.put(name, lst, XP.R + '/' + lst.name)
    out = BP.ssh(name, 'cd %s && sha256sum -c --quiet %s > %s.check 2>&1; echo rc=$?' % (XP.R, lst.name, lst.name), timeout=1800)
    print('data verified' if 'rc=0' in out else 'DATA CHECK FAILED ' + out[-400:])
    BP.put(name, CD / 'crossing' / 'x_heading_v13.py', HX)            # the current program (the bundle may hold an earlier copy)
    h = BP.ssh(name, 'sha256sum %s' % HX).split()[0]
    print('x_heading on the pod', h, 'matches' if h == XP.sha(CD / 'crossing' / 'x_heading_v13.py') else 'DIFFERS')


def run(name, w=12):
    BP.ssh(name, '%s && cd %s/job && (setsid nohup %s -I -B -X utf8 %s --workers %d > %s/heading.log 2>&1 < /dev/null &) ; sleep 2; echo started'
           % (XP.ENV, XP.R, XP.PY, HX, int(w), XP.R))
    print('started', name, pv.est())


def status(name):
    print(BP.ssh(name, 'echo npz=$(ls %s/*.npz 2>/dev/null | grep -v partial | wc -l) errors=$(grep -c ERROR %s/heading.log || true) '
                       'running=$(pgrep -fc [x]_heading_v13 || true); tail -2 %s/heading.log' % (HOUT, XP.R, XP.R)).strip())


def fetch(name):
    dest = CD / 'crossing' / 'heading'
    BP.ssh(name, 'cd %s && sha256sum *.npz X_HEADING_EXTRACT_*.json > SHA_H.txt && tar cf %s/heading.tar *.npz X_HEADING_EXTRACT_*.json SHA_H.txt' % (HOUT, XP.R), timeout=1800)
    loc = STAGE / 'heading.tar'
    BP.get(name, XP.R + '/heading.tar', str(loc))
    with tarfile.open(loc) as t:
        shas = dict(reversed(l.split()) for l in t.extractfile('SHA_H.txt').read().decode().splitlines())
        if any((dest / n).exists() for n in shas): raise SystemExit('REFUSED: target files exist in crossing/heading')
        for n in shas:
            mm = t.getmember(n); assert mm.isfile() and '/' not in n
            t.extract(mm, dest, filter='data')
    bad = [n for n, h in shas.items() if XP.sha(dest / n) != h]
    print('fetched %d files, %d differ' % (len(shas), len(bad)))


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'stage': stage()
    elif c == 'up': up(sys.argv[2])
    elif c == 'run': run(sys.argv[2], *(sys.argv[3:4]))
    elif c == 'status': status(sys.argv[2])
    elif c == 'fetch': fetch(sys.argv[2])
