"""v13 package B: after bug fix D-B4-3 (CA covariance symmetrised, 19 Nov 15:45 EST), re-evaluate B4's tuning statistic (median over the
20 lead-braking tuning runs of the lead track's mean position NIS) at the chosen sigma_a^2 = 0.001 and at grid points j = 0, 1, 2, 60
(10^-3, 10^-2.95, 10^-2.9, 1) to confirm that the tuning outcome (no sign change; nearest value 0.001) is unchanged.
Writes out\b3\B4_RECHECK_AFTER_FIX_v01.json. Usage: python -I -B -X utf8 b4_recheck_v01.py"""
import sys, json, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import b3_nis_tune_v01 as M
before = json.loads((M.OUT / 'B3_TUNE_SIGMA_A2_v01.json').read_text(encoding='utf-8'))
const = json.loads(pathlib.Path(r'ARS_TRIAL\revision_v13\work\shared\trackers\trk_constants_v01.json').read_text(encoding='utf-8'))
M._init(M.lb_tuning_caps())
res = []
for j in (0, 1, 2, 60):
    s2 = M.GRID[j]
    m, vals, ns = M.evaluate(('B4', dict(const, sigma_a2=s2)))
    res.append(dict(j=j, sigma_a2=s2, median_after_fix=m, median_before_fix=before['grid_median'][j], abs_diff=abs(m - before['grid_median'][j])))
    print(res[-1], flush=True)
(M.OUT / 'B4_RECHECK_AFTER_FIX_v01.json').write_text(json.dumps(dict(code='b4_recheck_v01.py', rows=res, written=time.strftime('%Y-%m-%d %H:%M:%S')), indent=1), encoding='utf-8')
