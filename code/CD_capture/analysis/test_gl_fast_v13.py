"""Identity of gl_fast_v13 with the library of record (a9_common_v01.Gridless.curve + optA_lib_v02.eval_scoring) on the 35 old
evaluation runs (exploratory data of record; nothing fresh is read). Full sample and the first NB rows of the draw of record.
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\test_gl_fast_v13.py [NB]
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path[:0] = [str(HERE), r'ARS_TRIAL\revision_v12\analysis']
import a9_common_v01 as A          # noqa: E402  (imports rev_common_v01 and optA_lib_v02 unchanged)
import gl_fast_v13 as GF           # noqa: E402
C = A.C; L = A.L

NB = int(sys.argv[1]) if len(sys.argv) > 1 else 60
t0 = time.time()
runs = C.load_runs()
A.add_placebo(runs, 'P')
NAMES = ['F0', 'E', 'N', 'P', 'NA', 'A1', 'CK3', 'Q']
G = A.gridless_sources(runs, NAMES, lambda r: r['clear1'] > 0.)
print('loaded and events built %.0f s' % (time.time() - t0), flush=True)
CNT = C.cnt_of_record()[:NB]
W = np.vstack([np.ones(len(runs)), CNT])
res = {}
for pop in (0, 2, 3, 4):
    prep = GF.Prepared(G, NAMES, pop)
    t1 = time.time(); fast = GF.evaluate(prep, W[:1]); fast = GF.evaluate(prep, W); tf = time.time() - t1
    t1 = time.time(); maxd = 0.; ndiff = 0
    for b in range(W.shape[0]):
        cb = {x: G[x].curve(W[b], pops=[pop]) for x in NAMES}
        e = L.eval_scoring({x: cb[x][:, 0, :] for x in NAMES}, NAMES[2:])
        pairs = [(e['denE'], fast['denE'][b]), (e['n'], fast['n'][b])] + [(e['D'][a], fast['D'][a][b]) for a in NAMES[2:]]
        for x, y in pairs:
            if not (x == y or (np.isnan(x) and np.isnan(y))):
                ndiff += 1; maxd = max(maxd, abs(x - y))
    tl = time.time() - t1
    res[pop] = dict(evals=W.shape[0], values_not_identical=ndiff, max_abs_diff=maxd, fast_s=tf, library_s=tl)
    print(pop, res[pop], flush=True)
ok = all(v['values_not_identical'] == 0 for v in res.values())
(HERE / 'out').mkdir(exist_ok=True)
(HERE / 'out' / 'TEST_GL_FAST_v13.json').write_text(json.dumps(dict(status='PASS' if ok else 'FAIL', populations=res, nboot=NB,
    note='old evaluation runs of record; full sample + first NB rows of default_rng(20261113)'), indent=1), encoding='utf-8')
print('PASS' if ok else 'FAIL')
