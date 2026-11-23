"""10 Hz option on the L12 capture pods (after LOCK_A12a): chain B7_10_0.1 of l12/l_trk_extract_v13.py (add9) on each pod's own runs, in place
(logs extracted by l_extract under /opt/claude_v13_l12local/ll_runs, B7 detections under /opt/claude_v13_l12local/b7). Uses C's frozen
tools/b7_pods_v13.py set-up at /root/b7 (stage-code, setup, accept done first). Moves files and starts the frozen program; computes no value.
Usage: python lb7run.py prep|run|status|fetch NAME"""
import json, pathlib, sys, tarfile, hashlib
CD = pathlib.Path(r'ARS_TRIAL\revision_v13\work\CD_capture')
sys.path[:0] = [str(CD / 'tools')]
import b7_pods_v13 as BP                 # noqa: E402
pv = BP.pv
VOL = '/opt/claude_v13_l12local'
PRE = BP.R + '/ARS_TRIAL/revision_v13/work/CD_capture/'
LT = PRE + 'l12/l_trk_extract_v13.py'
OUTR = VOL + '/lb7_out'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def prep(name):
    files = [(CD / 'l12' / 'l_trk_extract_v13.py', LT), (CD / 'l12' / 'out' / 'L12_RUNS_v13.json', PRE + 'l12/out/L12_RUNS_v13.json'),
             (CD.parents[1] / 'LOCK_A12a.txt', BP.R + '/ARS_TRIAL/revision_v13/LOCK_A12a.txt')]
    BP.ssh(name, 'mkdir -p %sl12/out' % PRE)
    for loc, rem in files:
        BP.put(name, loc, rem)
        h = BP.ssh(name, 'sha256sum %s' % rem).split()[0]
        if h != sha(loc): raise SystemExit('%s: %s differs on the pod' % (name, loc.name))
    print(name, 'prepared: l_trk_extract, L12_RUNS map, LOCK_A12a (sha256 checked)')


def pod_rids(name):
    out = BP.ssh(name, "python3 -c \"import json,glob; r=[json.load(open(f)) for f in glob.glob('%s/sealing/pl12_*.json')]; "
                       "print(','.join(sorted(x['run_id'] for x in r if x['pass'])))\"" % VOL).strip()
    return [x for x in out.split(',') if x]


def run(name, workers=6):
    rids = pod_rids(name)
    st = BP.ssh(name, "echo $(pgrep -fc '[b]7_redetect_v13' || true) $(ls %s/b7/pl12_*/B7_MANIFEST_v13.json 2>/dev/null | wc -l)" % VOL).split()
    if st[0] != '0' or int(st[1]) != len(rids): raise SystemExit('%s: B7 not finished (running %s, manifests %s of %d)' % (name, st[0], st[1], len(rids)))
    BP.ssh(name, '%s && cd %s/job && (setsid nohup %s -I -B -X utf8 %s --combos 10_0.1 --runs %s --logs-root %s/ll_runs --b7-root %s/b7 '
                 '--out-root %s --workers %d > %s/lb7.log 2>&1 < /dev/null &) ; sleep 2; echo started'
           % (BP.ENV, BP.R, BP.PY, LT, ','.join(rids), VOL, VOL, OUTR, int(workers), BP.R))
    print('started', name, len(rids), 'runs', pv.est())


def status(name):
    print(BP.ssh(name, "echo npz=$(ls %s/B7_10_0.1/*.npz 2>/dev/null | grep -v partial | wc -l) running=$(pgrep -fc '[l]_trk_extract' || true) "
                       "b7=$(pgrep -fc '[b]7_redetect_v13' || true) manifests=$(ls %s/b7/pl12_*/B7_MANIFEST_v13.json 2>/dev/null | wc -l); tail -c 300 %s/lb7.log 2>/dev/null || true"
                       % (OUTR, VOL, BP.R)).strip())


def fetch(name):
    dest = CD / 'arrays_l12' / 'B7_10_0.1'; dest.mkdir(parents=True, exist_ok=True)
    BP.ssh(name, 'cd %s && sha256sum B7_10_0.1/*.npz > SHA_LB7.txt && tar cf /root/lb7.tar B7_10_0.1/*.npz SHA_LB7.txt LB7_EXTRACT_*.json' % OUTR, timeout=1800)
    loc = CD / 'pods' / name / 'lb7.tar'
    BP.get(name, '/root/lb7.tar', str(loc))
    with tarfile.open(loc) as t:
        shas = dict(reversed(l.split()) for l in t.extractfile('SHA_LB7.txt').read().decode().splitlines())
        ex = [n for n in shas if (dest / pathlib.Path(n).name).exists()]
        if ex: raise SystemExit('REFUSED: %d target files exist' % len(ex))
        for m in t.getmembers():
            if m.name in shas: m.name = pathlib.Path(m.name).name; t.extract(m, dest, filter='data')
            elif m.name.startswith('LB7_EXTRACT_'): t.extract(m, CD / 'pods' / name, filter='data')
    bad = [n for n, h in shas.items() if sha(dest / pathlib.Path(n).name) != h]
    loc.unlink()
    print('%s: %d B7_10_0.1 arrays, %d differ' % (name, len(shas), len(bad)))


if __name__ == '__main__':
    c, n = sys.argv[1], sys.argv[2]
    {'prep': prep, 'run': run, 'status': status, 'fetch': fetch}[c](n)
