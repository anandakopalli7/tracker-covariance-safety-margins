import json, numpy as np
from rc_core import *
import b_variants as bv
x = 'B2'
data = {r: load_variant(x, r) for r in RUNS}
rs = RunSet(data, RUNS)
ms = margin_stats(margin_ratio_rows(rs)); m, A = ms['median'], ms['A']
rat = margin_ratio_rows(rs)
res = {'m_x': m, 'A_x': A}
res['b_outside_share'] = float(np.mean((rat < m * (1 - A)) | (rat > m * (1 + A))))
res['b_ratio_q01_q99'] = [float(v) for v in np.quantile(rat, [0.01, 0.99])]
res['b_n_rows'] = int(rat.size)
sp = []
for q in rs.d:
    a, b = q['cF0'], q['cN']
    ok = np.isfinite(a) & np.isfinite(b) & (a > 0) & (b > 0)
    with np.errstate(invalid='ignore', divide='ignore'):
        r = np.where(ok, np.sqrt(a / b), np.nan)
    n = ok.sum(axis=1)
    for i in np.nonzero(n >= 2)[0]:
        v = r[i][ok[i]]
        sp.append((v.max() - v.min()) / np.median(v))
sp = np.array(sp)
res['c'] = dict(n_decisions=int(sp.size), median=float(np.median(sp)), p90=float(np.quantile(sp, 0.9)), share_gt_0p05=float(np.mean(sp > 0.05)))
u = ranks_u(rs)
Cs = {'F0': [q['cF0'] for q in rs.d], 'E': [q['cE'] for q in rs.d], 'N': [q['cN'] for q in rs.d]}
Cs['E5x'] = oracle_C(rs, u, m, A)
Cs['E5q'] = [q['cF0'] / (np.quantile(rat, uu) ** 2)[:, None] for q, uu in zip(rs.d, u)]
S = bv.sources_stats(rs, Cs, keep=set(Cs))
pt = bv.pop_eval(S, 0, ['N', 'E5x', 'E5q'])
idx = np.random.default_rng(20261113).integers(0, 35, (20000, 35))[:2000]
cnt = np.stack([np.bincount(i, minlength=35) for i in idx]).astype(float)
B = bv.boot(S, ['N', 'E5x', 'E5q'], cnt)
def iv(v, p): 
    f = v[np.isfinite(v)]
    return dict(point=float(p), ci=[float(a) for a in np.percentile(f, [2.5, 97.5])], n_valid=int(f.size))
res['a_RRN_minus_RRE5x'] = iv(B['RR_N'] - B['RR_E5x'], pt['RR_N'] - pt['RR_E5x'])
res['d_RR_E5q'] = iv(B['RR_E5q'], pt['RR_E5q'])
res['d_RRN_minus_RRE5q'] = iv(B['RR_N'] - B['RR_E5q'], pt['RR_N'] - pt['RR_E5q'])
res['points'] = {k: pt[k] for k in ['RR_N', 'RR_E5x', 'RR_E5q']}
print(json.dumps(res, indent=1))
json.dump(res, open(OUT + r'\parts\b2_check.json', 'w'), indent=1)
d = json.load(open(OUT + r'\RECOUNT_B_v01.json')); d['B2_oracle_check'] = res
json.dump(d, open(OUT + r'\RECOUNT_B_v01.json', 'w'), indent=1, default=float)
open(OUT + r'\README_recount.md', 'a').write("\n## Update 19 Nov 2026 (B2 oracle check)\nPost-hoc diagnostics (a)-(d) for B2 in `RECOUNT_B_v01.json` under `B2_oracle_check` (code `b2_check.py`): RR_gl(N)-RR_gl(E5_x) and RR_gl(E5q) with E5q = cF0/quantile(binding-row ratios, u_i)^2 on the same ranks; first 2,000 resamples; percentile intervals over resamples with room > 0.\n")
