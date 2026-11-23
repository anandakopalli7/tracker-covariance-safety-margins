"""Revision v11, post hoc re-analysis R12 (ARS review of draft v10). New file, 18 Nov 2026.
Descriptive analyses added after the results and after a review; declared in AMENDMENT_08 (revision_v11).

R12a  Truncation of the post-stop segment (3 s commitment, step frontier, all sources).
      For T in {0, 1, 2, 5, 10, 20} s and "all": the population keeps every evaluated decision before the lead's stop and those
      evaluated decisions after it whose tick is less than T after the run's first stored after-stop decision
      ((k - k_stop) * 0.05 s < T). T = 0 drops the after-stop phase. Each population is scored on its own frontier and levels,
      exactly as the populations of record. Reported: n, R (pp), den0, D, RR (share of the 3 s oracle's room) and RR0 per source,
      with 95% run-bootstrap percentile intervals (the draw of record, 20,000 resamples).
R12b  A per-phase margin scale (3 s commitment, all evaluated decisions).
      Of record, one margin scale g is swept for all decisions. Here every source may use one scale per phase of the lead's
      motion (before the onset, lead braking, lead stopped): the points are all triples (g0, g1, g2) of the 202-value grid,
      wrong go = the pooled share of wrong-go decisions, caution = the pooled caution (sum of the caution terms over the sum of
      the truly safe selections), and the per-phase-scale frontier F_ps is the step frontier of these points at the pooled
      caution levels of record. As of record, every source other than F0 and E has F0's single-scale zero-margin point
      prepended. Quantities (sums over the 201 levels; /201 = percentage points):
        den1    = sum(F1_F0 - F1_E)        the room of record (single scale)
        gain_F0 = sum(F1_F0 - Fps_F0)      what the class average gains from choosing its scale per phase, with no
                                           per-decision information: the cross-phase allocation of caution, isolated
        den_ps  = sum(Fps_F0 - Fps_E)      the room that remains when both may choose a scale per phase
        den0_ps = sum(Fps_F0 - F_O)        against the perfect oracle
        Dps(A)  = sum(Fps_F0 - Fps_A)      a source's gain over the class average when both choose a scale per phase
      Bootstrap: run resamples from the draw of record (the first NB_PS rows), percentile intervals.
Usage: python -B -X utf8 rev_b_truncation_phase_scale_v01.py
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rev_common_v01 as C                   # noqa: E402
L = C.L

OUT = HERE / 'out' / 'REV_B_TRUNC_PHASESCALE_v01.json'
if OUT.exists():
    sys.exit('REFUSED: %s exists' % OUT)
t00 = time.time()
runs = C.load_runs()
CNT = C.cnt_of_record()
ARMS = C.MAIN_ARMS
doc = dict(code='rev_b_truncation_phase_scale_v01.py', status='post hoc, descriptive; AMENDMENT_08', R12a={}, R12b={})

# ------------------------------------------------------------------------------------------------ R12a truncation
TS = [0., 1., 2., 5., 10., 20., None]
TKEY = ['T0', 'T1', 'T2', 'T5', 'T10', 'T20', 'Tall']
post_dur = []
for r in runs:
    ph = r['ph']; k = r['k']; ev = r['ev']
    i2 = np.nonzero(ph == 2)[0]
    kstop = int(k[i2[0]]) if i2.size else None
    since = (k - kstop) * L.H if kstop is not None else np.full(k.shape, np.nan)
    ms = []
    for T in TS:
        if T is None:
            ms.append(ev.copy())
        else:
            ms.append(ev & ((ph != 2) | (since < T - 1e-9)))
    r['masks_trunc'] = tuple(ms)
    post_dur.append(dict(run=r['run'], k_stop=kstop, n_after_stop_evaluated=int((ev & (ph == 2)).sum()),
                         last_after_stop_s=float(since[ev & (ph == 2)].max()) if (ev & (ph == 2)).any() else None))
doc['R12a']['post_stop_segment'] = post_dur
tab = ['F0', 'E', 'O'] + ARMS
names = ['E', 'O'] + ARMS
X = C.tables(runs, ('W1',), tab, masks_key='masks_trunc')
pts = C.points(X, names, pops=range(len(TS)))
R = C.boot(X, names, (), list(range(len(TS))), CNT)
for i, key in enumerate(TKEY):
    pe = pts[i]; Rp = R[i]; n = pe['n']; den0 = pe['D']['O']; denE = pe['denE']
    e = dict(T_s=TS[i], n=n, R_pp=denE / L.NLEV, denE=dict(L.summ_den(Rp['denE'], denE), R_pp_ci=[x / L.NLEV for x in L.pct(Rp['denE'])]),
             den0=dict(L.summ_den(Rp['D']['O'], den0), R_pp=den0 / L.NLEV), arms={})
    for a in ARMS:
        D = pe['D'][a]
        e['arms'][a] = dict(D_dec_eq=L.dec_eq(D, n), rrE=L.summ(C.rat(Rp['D'][a], Rp['denE']), L.ratio(D, denE)),
                            rr0=L.summ(C.rat(Rp['D'][a], Rp['D']['O']), L.ratio(D, den0)))
    doc['R12a'][key] = e
print('R12a done (%.0f s)' % (time.time() - t00), flush=True)

# ------------------------------------------------------------------------------------------------ R12b per-phase scale
PH = [2, 3, 4]                      # population indices of phases 0, 1, 2 in r['masks']
tabp = ['F0', 'E', 'O'] + ARMS
Xp = C.tables(runs, ('W1',), tabp)          # arm -> (n_runs, G, 6, NST)


def front_bins(c, w, lev):
    """Step frontier at lev of the points (c, w): lowest w among points with c <= level; NaN where none. Equal to
    optA_lib_v02.frontier (checked below), computed by binning instead of sorting (many points)."""
    ok = np.isfinite(c) & np.isfinite(w)
    c = c[ok]; w = w[ok]
    idx = np.searchsorted(lev, c, side='left')          # first level >= c
    keep = idx < lev.size
    best = np.full(lev.size, np.inf)
    np.minimum.at(best, idx[keep], w[keep])
    best = np.minimum.accumulate(best)
    return np.where(np.isfinite(best), best, np.nan)


def uniq_phase(T):
    """T (G, NST) of one phase -> unique rows (wrong go count, caution sum, caution count)."""
    A = np.stack([T[:, 1], T[:, 2], T[:, 3]], axis=1)
    return np.unique(A, axis=0)


def ps_points(Tph, n):
    """Tph: three (G, NST) tables (phases 0-2) of one source -> pooled (caution %, wrong go %) of every scale triple."""
    U = [uniq_phase(T) for T in Tph]
    W = (U[0][:, 0][:, None, None] + U[1][:, 0][None, :, None] + U[2][:, 0][None, None, :]).ravel()
    S = (U[0][:, 1][:, None, None] + U[1][:, 1][None, :, None] + U[2][:, 1][None, None, :]).ravel()
    K = (U[0][:, 2][:, None, None] + U[1][:, 2][None, :, None] + U[2][:, 2][None, None, :]).ravel()
    with np.errstate(divide='ignore', invalid='ignore'):
        return 100. * S / K, 100. * W / n, [u.shape[0] for u in U]


def ps_eval(Tall, Tph):
    """Tall: arm -> (G, NST) pooled; Tph: arm -> [3 x (G, NST)]. Returns the quantities of the docstring."""
    cur = L.curves_w(Tall, 0)
    cF0, wF0 = cur['F0']; cE, wE = cur['E']
    c0 = cF0[0]; w0 = wF0[0]
    lev = L.levels_of(cF0, cE, c0)
    n = float(Tall['F0'][0, 0])
    f1 = {a: L.frontier(cur[a][0], cur[a][1], lev) for a in cur}
    fps = {}; nun = {}
    for a in Tph:
        if a == 'O':
            continue
        c, w, nu = ps_points(Tph[a], n)
        if a not in ('F0', 'E'):
            c = np.concatenate([[c0], c]); w = np.concatenate([[w0], w])
        fps[a] = front_bins(c, w, lev); nun[a] = nu
    out = dict(n=n, den1=float(np.sum(f1['F0'] - f1['E'])), den0_1=float(np.sum(f1['F0'] - f1['O'])),
               gain_F0=float(np.sum(f1['F0'] - fps['F0'])), gain_E=float(np.sum(f1['E'] - fps['E'])),
               den_ps=float(np.sum(fps['F0'] - fps['E'])), den0_ps=float(np.sum(fps['F0'] - f1['O'])),
               D1={a: float(np.sum(f1['F0'] - f1[a])) for a in ARMS},
               Dps={a: float(np.sum(fps['F0'] - fps[a])) for a in ARMS},
               Dx={a: float(np.sum(f1['F0'] - fps[a])) for a in ARMS}, n_unique=nun)
    return out


Tsum = {a: Xp[a].sum(axis=0) for a in Xp}
Tall = {a: Tsum[a][:, 0, :] for a in Xp}
Tph = {a: [Tsum[a][:, pi, :] for pi in PH] for a in Xp}
# check front_bins against the frontier of record on the single-scale points
cur = L.curves_w(Tall, 0); lev = L.levels_of(cur['F0'][0], cur['E'][0], cur['F0'][0][0])
chk = max(float(np.nanmax(np.abs(front_bins(cur[a][0], cur[a][1], lev) - L.frontier(cur[a][0], cur[a][1], lev)))) for a in cur)
t1 = time.time()
pt = ps_eval(Tall, Tph)
dt = time.time() - t1
doc['R12b']['front_bins_vs_frontier_max_abs_diff'] = chk
doc['R12b']['point'] = pt
doc['R12b']['seconds_per_eval'] = dt
print('R12b point done: %.2f s per evaluation; unique points per phase %s' % (dt, pt['n_unique']), flush=True)
NB_PS = 2000 if dt < 0.6 else (1000 if dt < 1.5 else 400)
keys = ['den1', 'den0_1', 'gain_F0', 'gain_E', 'den_ps', 'den0_ps']
B = {k: np.full(NB_PS, np.nan) for k in keys}
for nm in ('D1', 'Dps', 'Dx'):
    for a in ARMS:
        B['%s_%s' % (nm, a)] = np.full(NB_PS, np.nan)
for b in range(NB_PS):
    cn = CNT[b]
    Tb = {a: np.tensordot(cn, Xp[a], axes=(0, 0)) for a in Xp}
    e = ps_eval({a: Tb[a][:, 0, :] for a in Xp}, {a: [Tb[a][:, pi, :] for pi in PH] for a in Xp})
    for k in keys:
        B[k][b] = e[k]
    for nm in ('D1', 'Dps', 'Dx'):
        for a in ARMS:
            B['%s_%s' % (nm, a)][b] = e[nm][a]
    if (b + 1) % 200 == 0:
        print('  R12b bootstrap %d / %d (%.0f s)' % (b + 1, NB_PS, time.time() - t00), flush=True)
n = pt['n']
summ = dict(nboot=NB_PS, draw='the first %d rows of the draw of record (seed 20261113)' % NB_PS)
for k in keys:
    summ[k] = dict(point=pt[k], pp=pt[k] / L.NLEV, dec_eq=L.dec_eq(pt[k], n), ci=L.pct(B[k]), pp_ci=[x / L.NLEV for x in L.pct(B[k])])
summ['gain_F0_over_den1'] = L.summ(C.rat(B['gain_F0'], B['den1']), L.ratio(pt['gain_F0'], pt['den1']))
summ['den_ps_over_den1'] = L.summ(C.rat(B['den_ps'], B['den1']), L.ratio(pt['den_ps'], pt['den1']))
summ['gain_F0_over_den0_1'] = L.summ(C.rat(B['gain_F0'], B['den0_1']), L.ratio(pt['gain_F0'], pt['den0_1']))
summ['arms'] = {}
for a in ARMS:
    summ['arms'][a] = dict(
        rr_single=L.summ(C.rat(B['D1_' + a], B['den1']), L.ratio(pt['D1'][a], pt['den1'])),
        rr_ps=L.summ(C.rat(B['Dps_' + a], B['den_ps']), L.ratio(pt['Dps'][a], pt['den_ps'])),
        rr0_ps=L.summ(C.rat(B['Dps_' + a], B['den0_ps']), L.ratio(pt['Dps'][a], pt['den0_ps'])),
        Dps_over_den1=L.summ(C.rat(B['Dps_' + a], B['den1']), L.ratio(pt['Dps'][a], pt['den1'])),
        Dps_dec_eq=dict(point=L.dec_eq(pt['Dps'][a], n), ci=L.pct(L.dec_eq(B['Dps_' + a], n))),
        D1_dec_eq=dict(point=L.dec_eq(pt['D1'][a], n), ci=L.pct(L.dec_eq(B['D1_' + a], n))))
doc['R12b']['summary'] = summ
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
doc['common_sha256'] = L.sha256_file(HERE / 'rev_common_v01.py')
OUT.write_text(C.jdump(doc), encoding='utf-8')
print('written %s (%.0f s)' % (OUT, time.time() - t00))
