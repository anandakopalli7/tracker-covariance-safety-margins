"""Revision v12, AMENDMENT_09 A9-2(a): Monte Carlo error of the calibrated levels of R and RR(N). New file, 19 Nov 2026.
D2 of revision_v11/analysis/rev_d_bootstrap_v01.py repeated for R and RR(N) only, with its seeds and the same draw order
(outer default_rng(20261120).integers(0, 35, (2000, 35)); inner default_rng(<seed>), one stream, 1,000 resamples of each
outer sample's runs), storing per outer sample the inner shares below / at-or-below the full-sample value, from which the
coverage at every nominal level follows. Run twice: inner seed 20261121 (identity with v11: calibrated levels 0.964 and
0.996) and 20261126 (inner Monte Carlo). Monte Carlo error of the calibrated level from 2,000 resamples of the outer samples
(seed 20261125). Usage: python -B -X utf8 a9_2a_double_bootstrap_mc_v01.py
"""
import time
import numpy as np
import a9_common_v01 as A
C = A.C; L = A.L

OUTF = A.OUT / 'A9_2A_DOUBLE_BOOTSTRAP_MC_v01.json'
if OUTF.exists():
    raise SystemExit('REFUSED: %s exists' % OUTF)
t00 = time.time()
runs = C.load_runs(); NRUN = len(runs)
X = C.tables(runs, ('W1',), ['F0', 'E', 'N'])
Xa = {a: X[a][:, :, 0, :] for a in X}
STATS = ['R', 'RR_N']


def stat_of(T):
    e = L.eval_scoring(T, ['E', 'N'])
    den = e['denE']
    if not (np.isfinite(den) and den > 0):
        return [np.nan, np.nan]
    return [den / L.NLEV, e['D']['N'] / den]


def stats_counts(CN):
    out = np.empty((CN.shape[0], 2))
    for s0 in range(0, CN.shape[0], 250):
        cn = CN[s0:s0 + 250]
        TB = {a: np.tensordot(cn, Xa[a], axes=(1, 0)) for a in Xa}
        for b in range(cn.shape[0]):
            out[s0 + b] = stat_of({a: TB[a][b] for a in Xa})
    return out


def counts_of(idx, n=NRUN):
    cn = np.zeros((idx.shape[0], n))
    for b in range(idx.shape[0]):
        cn[b] = np.bincount(idx[b], minlength=n)
    return cn


full = np.array(stat_of({a: Xa[a].sum(axis=0) for a in Xa}))
B1, B2 = 2000, 1000
FINE = np.concatenate([np.arange(0.90, 0.9991, 0.001), [0.9995, 0.9999, 1.0]])


def cover_two(lt, le, nom):
    a = 1. - nom
    ok = np.isfinite(lt)
    return float(((le[ok] >= a / 2. - 1e-12) & (lt[ok] <= 1. - a / 2. + 1e-12)).mean())


def calibrate(lt, le):
    for nm in FINE:
        if cover_two(lt, le, nm) >= 0.95:
            return float(nm)
    return None


def double(seed_inner):
    rng_o = np.random.default_rng(20261120); rng_i = np.random.default_rng(seed_inner)
    IDX_O = rng_o.integers(0, NRUN, (B1, NRUN))
    p_lt = np.full((B1, 2), np.nan); p_le = np.full((B1, 2), np.nan)
    for b in range(B1):
        io = IDX_O[b]
        ii = rng_i.integers(0, NRUN, (B2, NRUN))
        S = stats_counts(counts_of(io[ii]))
        for j in range(2):
            v = S[:, j]; v = v[np.isfinite(v)]
            if v.size:
                p_lt[b, j] = (v < full[j]).mean(); p_le[b, j] = (v <= full[j]).mean()
        if (b + 1) % 200 == 0:
            print('  inner seed %d: outer %d / %d (%.0f s)' % (seed_inner, b + 1, B1, time.time() - t00), flush=True)
    return p_lt, p_le


doc = dict(code='a9_2a_double_bootstrap_mc_v01.py', status='post hoc, descriptive; AMENDMENT_09 A9-2(a)', stats=STATS,
           full_sample=dict(zip(STATS, map(float, full))), runs={})
rng_mc = np.random.default_rng(20261125)
IDX_MC = rng_mc.integers(0, B1, (2000, B1))
for seed in (20261121, 20261126):
    p_lt, p_le = double(seed)
    ent = {}
    for j, s in enumerate(STATS):
        cal = calibrate(p_lt[:, j], p_le[:, j])
        cov = {('%.4f' % nm): cover_two(p_lt[:, j], p_le[:, j], nm) for nm in FINE}
        mc = []
        for k in range(IDX_MC.shape[0]):
            ix = IDX_MC[k]
            mc.append(calibrate(p_lt[ix, j], p_le[ix, j]))
        mc = np.array([np.nan if x is None else x for x in mc], float)
        ent[s] = dict(calibrated_nominal=cal, coverage_fine=cov,
                      mc_calibrated_mean=float(np.nanmean(mc)), mc_calibrated_sd=float(np.nanstd(mc, ddof=1)),
                      mc_calibrated_q=[float(x) for x in np.nanpercentile(mc, [2.5, 25, 50, 75, 97.5])],
                      mc_n_none=int(np.isnan(mc).sum()), share_outer_lt_mean=float(np.nanmean(p_lt[:, j])))
    doc['runs'][str(seed)] = ent
    print('seed %d: %s' % (seed, {s: ent[s]['calibrated_nominal'] for s in STATS}), flush=True)
doc['identity_with_v11'] = dict(R=doc['runs']['20261121']['R']['calibrated_nominal'] == 0.9640000000000001
                                or abs(doc['runs']['20261121']['R']['calibrated_nominal'] - 0.964) < 1e-9,
                                RR_N=abs(doc['runs']['20261121']['RR_N']['calibrated_nominal'] - 0.996) < 1e-9)
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
A.write_out(OUTF, doc)
print('written %s (%.0f s)' % (OUTF, time.time() - t00))
