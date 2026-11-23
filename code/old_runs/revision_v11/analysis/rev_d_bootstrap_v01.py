"""Revision v11, post hoc check R9 (ARS review of draft v10): are the run-bootstrap intervals valid for these statistics?
New file, 18 Nov 2026. Descriptive; declared in AMENDMENT_08 (revision_v11), which fixed the design and the consequence rule
before any value was read.

Statistics (3 s commitment, all evaluated decisions, step frontier), each recomputed from scratch in every resample, the 201
caution levels included (optA_lib_v02.eval_scoring rebuilds the levels from the resample's own F0 and E curves):
  R = denE / 201;  RR(A) = D(A, F0) / denE for A in N, NA, AM ('A1'), CK3, Q;  RR0(CK3) = D(CK3, F0) / den0;  NA - N.

D1  Description of the bootstrap distribution of record (20,000 resamples, seed 20261113) for each statistic.
D2  Double bootstrap. Outer: 2,000 run resamples (default_rng(20261120).integers(0, 35, (2000, 35))). Inner: for each outer
    sample, 1,000 resamples of its 35 runs (default_rng(20261121), one stream). The full-sample value plays the truth.
    For every nominal level the estimated coverage of the percentile interval, of the basic interval and of the one-sided
    upper percentile bound is the share of outer samples whose inner interval contains the full-sample value.
    Calibration: the smallest nominal level on a fine grid at which the percentile interval's estimated coverage is at least
    95%; the calibrated interval is the percentile interval of the draw of record at that level.
D3  Sensitivities (percentile intervals, 20,000 resamples each): resampling stratified by the recording setting alpha
    (seed 20261122); the five short runs left out (30 runs; seed 20261123); m-out-of-n subsampling without replacement,
    m = 15, 20, 25 (5,000 subsamples each; seed 20261124), with the root sqrt(m) (theta*_m - theta_hat) and the finite-
    population factor sqrt(1 - m / n).
Usage: python -B -X utf8 rev_d_bootstrap_v01.py
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rev_common_v01 as C                   # noqa: E402
L = C.L

OUT = HERE / 'out' / 'REV_D_BOOTSTRAP_v01.json'
if OUT.exists():
    sys.exit('REFUSED: %s exists' % OUT)
t00 = time.time()
runs = C.load_runs()
NRUN = len(runs)
ARMS = ['N', 'NA', 'A1', 'CK3', 'Q']
tab = ['F0', 'E', 'O'] + ARMS
names = ['E', 'O'] + ARMS
X = C.tables(runs, ('W1',), tab)
Xa = {a: X[a][:, :, 0, :] for a in X}                 # (35, G, NST): all evaluated decisions
STATS = ['R', 'RR_N', 'RR_NA', 'RR_A1', 'RR_CK3', 'RR_Q', 'RR0_CK3', 'NA_minus_N']


def stat_of(T):
    e = L.eval_scoring(T, names)
    den = e['denE']; d0 = e['D']['O']
    if not (np.isfinite(den) and den > 0):
        return [np.nan] * len(STATS)
    rr = {a: e['D'][a] / den for a in ARMS}
    return [den / L.NLEV, rr['N'], rr['NA'], rr['A1'], rr['CK3'], rr['Q'], (e['D']['CK3'] / d0) if d0 > 0 else np.nan,
            rr['NA'] - rr['N']]


def stats_counts(CN):
    """CN (B, 35) run counts -> (B, len(STATS))."""
    out = np.empty((CN.shape[0], len(STATS)))
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
doc = dict(code='rev_d_bootstrap_v01.py', status='post hoc, descriptive; AMENDMENT_08', stats=STATS,
           full_sample={s: float(v) for s, v in zip(STATS, full)},
           levels_rebuilt_in_each_resample=True)

# ------------------------------------------------------------------------------------------------ D1
CNT = C.cnt_of_record()
B0 = stats_counts(CNT)
d1 = {}
for j, s in enumerate(STATS):
    b = B0[:, j]; f = np.isfinite(b); bb = b[f]
    q = np.percentile(bb, [0, 0.05, 0.5, 2.5, 5, 25, 50, 75, 95, 97.5, 99.5, 99.95, 100])
    d1[s] = dict(point=float(full[j]), n_invalid=int((~f).sum()), mean=float(bb.mean()), sd=float(bb.std(ddof=1)),
                 q_0_0p05_0p5_2p5_5_25_50_75_95_97p5_99p5_99p95_100=[float(x) for x in q],
                 share_below_point=float((bb < full[j]).mean()), share_equal_point=float((bb == full[j]).mean()),
                 share_le_zero=float((bb <= 0).mean()), n_distinct=int(np.unique(np.round(bb, 12)).size),
                 percentile_95=[float(q[3]), float(q[9])], basic_95=[float(2 * full[j] - q[9]), float(2 * full[j] - q[3])],
                 bias_boot_mean_minus_point=float(bb.mean() - full[j]))
doc['D1_draw_of_record'] = d1
print('D1 done (%.0f s)' % (time.time() - t00), flush=True)

# ------------------------------------------------------------------------------------------------ D2 double bootstrap
B1, B2 = 2000, 1000
rng_o = np.random.default_rng(20261120); rng_i = np.random.default_rng(20261121)
IDX_O = rng_o.integers(0, NRUN, (B1, NRUN))
outer_est = np.full((B1, len(STATS)), np.nan)
p_lt = np.full((B1, len(STATS)), np.nan); p_le = np.full((B1, len(STATS)), np.nan)      # inner share below / at-or-below truth
r_lt = np.full((B1, len(STATS)), np.nan); r_le = np.full((B1, len(STATS)), np.nan)      # ... 2 * outer estimate - truth
n_inner_valid = np.zeros((B1, len(STATS)))
for b in range(B1):
    io = IDX_O[b]
    co = np.bincount(io, minlength=NRUN).astype(float)
    outer_est[b] = stat_of({a: np.tensordot(co, Xa[a], axes=(0, 0)) for a in Xa})
    ii = rng_i.integers(0, NRUN, (B2, NRUN))
    S = stats_counts(counts_of(io[ii]))
    for j in range(len(STATS)):
        v = S[:, j]; v = v[np.isfinite(v)]
        n_inner_valid[b, j] = v.size
        if v.size == 0 or not np.isfinite(outer_est[b, j]):
            continue
        p_lt[b, j] = (v < full[j]).mean(); p_le[b, j] = (v <= full[j]).mean()
        piv = 2. * outer_est[b, j] - full[j]
        r_lt[b, j] = (v < piv).mean(); r_le[b, j] = (v <= piv).mean()
    if (b + 1) % 100 == 0:
        print('  D2 outer %d / %d (%.0f s)' % (b + 1, B1, time.time() - t00), flush=True)
NOM = [0.80, 0.90, 0.95, 0.975, 0.99, 0.995, 0.998, 0.999, 0.9995, 1.0]
FINE = np.concatenate([np.arange(0.90, 0.9991, 0.001), [0.9995, 0.9999, 1.0]])


def cover_two(lt, le, nom):
    """Share of outer samples whose inner two-sided interval at nominal level nom contains the pivot value:
    lower quantile <= value <= upper quantile, i.e. share(inner <= value) >= a/2 and share(inner < value) <= 1 - a/2."""
    a = 1. - nom
    ok = np.isfinite(lt)
    return float(((le[ok] >= a / 2. - 1e-12) & (lt[ok] <= 1. - a / 2. + 1e-12)).mean())


d2 = dict(B_outer=B1, B_inner=B2, seeds=dict(outer=20261120, inner=20261121), stats={})
for j, s in enumerate(STATS):
    ok = np.isfinite(p_lt[:, j])
    cov_p = {('%.4f' % nm): cover_two(p_lt[:, j], p_le[:, j], nm) for nm in NOM}
    cov_b = {('%.4f' % nm): cover_two(r_lt[:, j], r_le[:, j], nm) for nm in NOM}
    # one-sided upper percentile bound at level nm: truth <= q_nm  <=>  share(inner < truth) <= nm
    cov_u = {('%.4f' % nm): float((p_lt[ok, j] <= nm + 1e-12).mean()) for nm in NOM}
    cov_l = {('%.4f' % nm): float((p_le[ok, j] >= 1. - nm - 1e-12).mean()) for nm in NOM}
    cal = None
    for nm in FINE:
        if cover_two(p_lt[:, j], p_le[:, j], nm) >= 0.95:
            cal = float(nm); break
    calb = None
    for nm in FINE:
        if cover_two(r_lt[:, j], r_le[:, j], nm) >= 0.95:
            calb = float(nm); break
    calu = None
    for nm in FINE:
        if float((p_lt[ok, j] <= nm + 1e-12).mean()) >= 0.95:
            calu = float(nm); break
    b = B0[:, j]; b = b[np.isfinite(b)]
    ent = dict(n_outer_valid=int(ok.sum()), outer_mean=float(np.nanmean(outer_est[:, j])),
               coverage_percentile=cov_p, coverage_basic=cov_b, coverage_upper_bound=cov_u, coverage_lower_bound=cov_l,
               calibrated_nominal_percentile=cal, calibrated_nominal_basic=calb, calibrated_nominal_upper_bound=calu,
               mc_se_at_95=float(np.sqrt(0.95 * 0.05 / ok.sum())))
    if cal is not None:
        a = 1. - cal
        ent['calibrated_percentile_interval'] = [float(x) for x in np.percentile(b, [100. * a / 2., 100. * (1. - a / 2.)])]
    if calb is not None:
        a = 1. - calb
        q = np.percentile(b, [100. * a / 2., 100. * (1. - a / 2.)])
        ent['calibrated_basic_interval'] = [float(2. * full[j] - q[1]), float(2. * full[j] - q[0])]
    if calu is not None:
        ent['calibrated_upper_bound'] = float(np.percentile(b, 100. * calu))
    d2['stats'][s] = ent
doc['D2_double_bootstrap'] = d2
print('D2 done (%.0f s)' % (time.time() - t00), flush=True)

# ------------------------------------------------------------------------------------------------ D3 sensitivities
d3 = {}
# (a) stratified by the recording setting alpha
# the recording setting of each run: the descriptive split of record (A4_RESULTS_FIT_v01.json, splits.alpha.<value>.runs)
a4 = json.loads(C.A4_JSON.read_text(encoding='utf-8'))
amap = {}
for val, ent in a4['splits']['alpha'].items():
    for rn in ent['runs']:
        amap[rn] = float(val)
alpha = np.array([amap.get(r['run'], np.nan) for r in runs])
d3['alpha_source'] = 'A4_RESULTS_FIT_v01.json splits.alpha'
if np.isfinite(alpha).all():
    rng = np.random.default_rng(20261122)
    groups = [np.nonzero(alpha == v)[0] for v in np.unique(alpha)]
    idx = np.concatenate([g[rng.integers(0, g.size, (C.NBOOT, g.size))] for g in groups], axis=1)
    S = stats_counts(counts_of(idx))
    d3['stratified_by_alpha'] = dict(groups={str(v): int((alpha == v).sum()) for v in np.unique(alpha)}, seed=20261122,
                                     ci={s: L.pct(S[:, j]) for j, s in enumerate(STATS)})
    print('D3 stratified done (%.0f s)' % (time.time() - t00), flush=True)
# (b) the five short runs left out
nev = np.array([int(r['ev'].sum()) for r in runs])
long_i = np.nonzero(nev >= 100)[0]
co = np.zeros(NRUN); co[long_i] = 1.
pt30 = stat_of({a: np.tensordot(co, Xa[a], axes=(0, 0)) for a in Xa})
rng = np.random.default_rng(20261123)
idx = long_i[rng.integers(0, long_i.size, (C.NBOOT, long_i.size))]
S = stats_counts(counts_of(idx))
d3['short_runs_left_out'] = dict(n_runs=int(long_i.size), short_runs=[runs[i]['run'] for i in np.nonzero(nev < 100)[0]],
                                 evaluated_in_short_runs=[int(nev[i]) for i in np.nonzero(nev < 100)[0]], seed=20261123,
                                 point={s: float(v) for s, v in zip(STATS, pt30)}, ci={s: L.pct(S[:, j]) for j, s in enumerate(STATS)})
print('D3 short runs done (%.0f s)' % (time.time() - t00), flush=True)
# (c) m-out-of-n subsampling without replacement
rng = np.random.default_rng(20261124)
d3['m_out_of_n'] = {}
for m in (15, 20, 25):
    CN = np.zeros((5000, NRUN))
    for b in range(5000):
        CN[b, rng.permutation(NRUN)[:m]] = 1.
    S = stats_counts(CN)
    ent = {}
    for j, s in enumerate(STATS):
        v = S[:, j]; v = v[np.isfinite(v)]
        root = np.sqrt(m) * (v - full[j])
        ql, qh = np.percentile(root, [2.5, 97.5])
        raw = [float(full[j] - qh / np.sqrt(NRUN)), float(full[j] - ql / np.sqrt(NRUN))]
        fpc = np.sqrt(1. - m / NRUN)
        cor = [float(full[j] - qh / fpc / np.sqrt(NRUN)), float(full[j] - ql / fpc / np.sqrt(NRUN))]
        ent[s] = dict(interval_raw=raw, interval_fpc=cor, subsample_q2p5_q97p5=[float(x) for x in np.percentile(v, [2.5, 97.5])],
                      n_invalid=int(S.shape[0] - v.size))
    d3['m_out_of_n'][str(m)] = ent
    print('D3 m = %d done (%.0f s)' % (m, time.time() - t00), flush=True)
# (d) leave one run out and leave five runs out (ranges)
loo = np.empty((NRUN, len(STATS)))
for i in range(NRUN):
    co = np.ones(NRUN); co[i] = 0.
    loo[i] = stat_of({a: np.tensordot(co, Xa[a], axes=(0, 0)) for a in Xa})
d3['leave_one_run_out'] = {s: dict(min=float(np.nanmin(loo[:, j])), max=float(np.nanmax(loo[:, j]))) for j, s in enumerate(STATS)}
doc['D3_sensitivities'] = d3
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
doc['common_sha256'] = L.sha256_file(HERE / 'rev_common_v01.py')
OUT.write_text(C.jdump(doc), encoding='utf-8')
print('written %s (%.0f s)' % (OUT, time.time() - t00))
