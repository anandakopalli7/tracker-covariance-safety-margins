"""Revision v12, AMENDMENT_09 A9-2(b) (review items R10, S9): subsampling with an estimated rate (Bertail, Politis and Romano
1999). New file, 19 Nov 2026. 3 s commitment, all evaluated decisions.
Statistics: RR(N) and D(N, F0) in decision-equivalents, on the grid of record and gridless (A9-1(c)).
m = 10, 15, 20, 25 runs without replacement, 2,000 subsamples each (one stream, seed 20261127, the same subsamples for all four
statistics). Rate: beta = -slope of log(q75 - q25 of theta*_m) on log m (least squares over the four m). Interval at m = 20 from
the root m^beta (theta*_m - theta_hat): [theta_hat - q97.5 / (fpc n^beta), theta_hat - q2.5 / (fpc n^beta)], fpc = sqrt(1 - m/n)
as in rev_d (v11); the interval without fpc is printed beside it. Also the same interval with beta = 1/2 for comparison.
Usage: python -B -X utf8 a9_2b_subsampling_rate_v01.py
"""
import time
import numpy as np
import a9_common_v01 as A
C = A.C; L = A.L

OUTF = A.OUT / 'A9_2B_SUBSAMPLING_RATE_v01.json'
if OUTF.exists():
    raise SystemExit('REFUSED: %s exists' % OUTF)
t00 = time.time()
runs = C.load_runs(); NRUN = len(runs)
X = C.tables(runs, ('W1',), ['F0', 'E', 'N'])
Xa = {a: X[a][:, :, 0, :] for a in X}
G = A.gridless_sources(runs, ['F0', 'E', 'N'], lambda r: r['clear1'] > 0.)
MS = (10, 15, 20, 25); NS = 2000


def st_grid(w):
    T = {a: np.tensordot(w, Xa[a], axes=(0, 0)) for a in Xa}
    e = L.eval_scoring(T, ['E', 'N'])
    if not (np.isfinite(e['denE']) and e['denE'] > 0):
        return np.nan, np.nan
    return e['D']['N'] / e['denE'], L.dec_eq(e['D']['N'], e['n'])


def st_gridless(w):
    T = {a: G[a].curve(w, pops=[0])[:, 0, :] for a in G}
    e = L.eval_scoring(T, ['E', 'N'])
    if not (np.isfinite(e['denE']) and e['denE'] > 0):
        return np.nan, np.nan
    return e['D']['N'] / e['denE'], L.dec_eq(e['D']['N'], e['n'])


w1 = np.ones(NRUN)
full = dict(zip(['RR_N_grid', 'D_N_grid'], st_grid(w1)))
full.update(dict(zip(['RR_N_gridless', 'D_N_gridless'], st_gridless(w1))))
STATS = list(full)
rng = np.random.default_rng(20261127)
S = {m: np.full((NS, 4), np.nan) for m in MS}
for m in MS:
    for b in range(NS):
        w = np.zeros(NRUN); w[rng.permutation(NRUN)[:m]] = 1.
        S[m][b, 0:2] = st_grid(w); S[m][b, 2:4] = st_gridless(w)
    print('m = %d done (%.0f s)' % (m, time.time() - t00), flush=True)
doc = dict(code='a9_2b_subsampling_rate_v01.py', status='post hoc, descriptive; AMENDMENT_09 A9-2(b)', m=list(MS), n_sub=NS,
           seed=20261127, full_sample=full, stats={})
for j, s in enumerate(STATS):
    iqr = []
    for m in MS:
        v = S[m][:, j]; v = v[np.isfinite(v)]
        iqr.append(float(np.percentile(v, 75) - np.percentile(v, 25)))
    lm = np.log(np.array(MS, float)); li = np.log(np.array(iqr))
    slope = float(np.polyfit(lm, li, 1)[0]); beta = -slope
    m = 20; v = S[m][:, j]; v = v[np.isfinite(v)]; th = full[s]
    fpc = np.sqrt(1. - m / NRUN)
    ent = dict(iqr_by_m=dict(zip(map(str, MS), iqr)), beta_hat=beta)
    for nm, bb in (('estimated', beta), ('half', 0.5)):
        root = (m ** bb) * (v - th)
        ql, qh = np.percentile(root, [2.5, 97.5])
        ent['interval_m20_' + nm] = dict(raw=[float(th - qh / NRUN ** bb), float(th - ql / NRUN ** bb)],
                                         fpc=[float(th - qh / fpc / NRUN ** bb), float(th - ql / fpc / NRUN ** bb)])
    ent['subsample_q2p5_q97p5_by_m'] = {str(mm): [float(x) for x in np.nanpercentile(S[mm][:, j], [2.5, 97.5])] for mm in MS}
    doc['stats'][s] = ent
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
A.write_out(OUTF, doc)
print('written %s (%.0f s)' % (OUTF, time.time() - t00))
