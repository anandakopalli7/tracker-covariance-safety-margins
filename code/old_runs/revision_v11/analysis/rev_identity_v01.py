"""Identity check of rev_common_v01 against the Option A results of record (OPTIONA_MAIN_RESULTS_v02.json), before any new
quantity is computed. Compares points AND 20,000-resample percentile intervals for: W1 (all, moving, phases, phase-weighted):
den0, denE, D, RR0 and RR_E of N, NA, CK3, A1, Q; W_R(0.75 s, 6 m/s^2) and reading (ii) at 0.75 s likewise; the signed-caution
scoring at 0.75 s (N, NA, CK3). Tolerance 1e-9 (relative to max(1, |a|, |b|)). Writes out/IDENTITY_REV_v01.json (never overwrites).
Usage: python -B -X utf8 rev_identity_v01.py"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rev_common_v01 as C                   # noqa: E402
L = C.L

OUT = HERE / 'out' / 'IDENTITY_REV_v01.json'
OUT.parent.mkdir(exist_ok=True)
if OUT.exists():
    sys.exit('REFUSED: %s exists' % OUT)
rec = json.loads(C.OPTA_JSON.read_text(encoding='utf-8'))
runs = C.load_runs()
CNT = C.cnt_of_record()
fails = []
nchk = [0]


def close(a, b):
    a = float(a); b = float(b)
    if np.isnan(a) and np.isnan(b):
        return True
    return abs(a - b) <= 1e-9 * max(1., abs(a), abs(b))


def chk(label, mine, theirs):
    nchk[0] += 1
    if not close(mine, theirs):
        fails.append((label, float(mine), float(theirs)))


def compare(sc, key, group, signed=False, arms=C.MAIN_ARMS):
    tab = ['F0', 'E', 'O'] + list(arms)
    names = ['E', 'O'] + list(arms)
    X = C.tables(runs, sc, tab, signed=signed)
    pts = C.points(X, names, pops=range(5))
    R = C.boot(X, names, (), [0, 1, 2, 3, 4], CNT)
    rp = rec['part1'][group][key]['pops']
    for pi in range(5):
        r = rp[C.POPS[pi]]
        chk('%s %s den0' % (key, C.POPS[pi]), pts[pi]['D']['O'], r['den0']['point'])
        chk('%s %s denE' % (key, C.POPS[pi]), pts[pi]['denE'], r['denE']['point'])
        ci = L.summ_den(R[pi]['D']['O'], pts[pi]['D']['O'])['ci']
        for j in (0, 1):
            chk('%s %s den0 ci%d' % (key, C.POPS[pi], j), ci[j], r['den0']['ci'][j])
        for a in arms:
            ra = r['arms'][a]
            chk('%s %s D[%s]' % (key, C.POPS[pi], a), pts[pi]['D'][a], ra['D']['point'])
            for nm, den_b, den_p in (('rr0', R[pi]['D']['O'], pts[pi]['D']['O']), ('rrE', R[pi]['denE'], pts[pi]['denE'])):
                s = L.summ(C.rat(R[pi]['D'][a], den_b), L.ratio(pts[pi]['D'][a], den_p))
                chk('%s %s %s[%s] point' % (key, C.POPS[pi], nm, a), s['point'], ra[nm]['point'])
                for j in (0, 1):
                    chk('%s %s %s[%s] ci%d' % (key, C.POPS[pi], nm, a, j), s['ci'][j], ra[nm]['ci'][j])
    sp = C.strat_point(pts, names); sb = C.strat_boot(R, names)
    r = rp['strat']
    chk('%s strat den0' % key, sp['D']['O'], r['den0']['point'])
    for a in arms:
        s = L.summ(C.rat(sb['D'][a], sb['D']['O']), L.ratio(sp['D'][a], sp['D']['O']))
        chk('%s strat rr0[%s] point' % (key, a), s['point'], r['arms'][a]['rr0']['point'])
        for j in (0, 1):
            chk('%s strat rr0[%s] ci%d' % (key, a, j), s['ci'][j], r['arms'][a]['rr0']['ci'][j])
    print('  %s compared (%d checks so far, %d fail)' % (key, nchk[0], len(fails)), flush=True)


t0 = time.time()
compare(('W1',), 'W1', 'scorings')
compare(('WR', 0.75, 6.0), 'WR_t0p75_a6p0', 'scorings')
compare(('ii', 0.75, 6.0), 'ii_t0p75_a6p0', 'scorings')
compare(('WRs', 0.75, 6.0), 'WRs_t0p75_a6p0', 'signed', signed=True, arms=['N', 'NA', 'CK3'])
doc = dict(written=time.strftime('%Y-%m-%d %H:%M:%S'), n_checks=nchk[0], n_fail=len(fails), fails=fails[:50],
           passed=len(fails) == 0, seconds=time.time() - t0,
           reference=str(C.OPTA_JSON), reference_sha256=L.sha256_file(C.OPTA_JSON),
           lib_sha256=L.sha256_file(C.OJ / 'A6R' / 'code' / 'optA_lib_v02.py'),
           common_sha256=L.sha256_file(HERE / 'rev_common_v01.py'))
OUT.write_text(C.jdump(doc), encoding='utf-8')
print('identity: %d checks, %d fail, %.0f s' % (nchk[0], len(fails), time.time() - t0))
for f in fails[:20]:
    print('  FAIL', f)
