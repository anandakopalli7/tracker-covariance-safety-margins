"""Independent recount v12 (second program), points only, full sample. Written by the recount agent, 19 Nov 2026.
Definitions: revision_v12/AMENDMENT_09_ARS_REVISION_v01.md (A9-1 a-c, A9-3 a-b, A9-4 b, A9-5, A9-6, A9-7) and the brief of the
recount. Does not read any a9_*.py file nor any first-program JSON. Output: RECOUNT_VALUES_v12.json (this folder).
Usage: python -B -X utf8 rc_main_v12.py
"""
import json, pathlib, time, glob
import numpy as np
import rc_lib_v12 as R

L = R.L; C = R.C; GRID = R.GRID; NLEV = R.NLEV
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'RECOUNT_VALUES_v12.json'
T00 = time.time()
LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    LOG.append(s)
    print('[%6.1f s] %s' % (time.time() - T00, s), flush=True)


V = dict(code='rc_main_v12.py (+ rc_lib_v12.py)', note='independent recount, points only, full sample of 35 runs',
         checks={})
runs = C.load_runs()
cbs = [R.contrib(r) for r in runs]
P_DIV = 1.1029 ** 2
SRC = ['F0', 'E', 'N', 'NA', 'A1', 'CK3', 'Q']
crit_fun = {a: (lambda r, a=a: r['crit'][a]) for a in SRC}
crit_fun['P'] = lambda r: r['crit']['F0'] / P_DIV
X = {a: R.grid_tables(runs, None, cbs, crit_override=crit_fun[a]) for a in crit_fun}
TS = {a: X[a].sum(axis=0) for a in X}
NPOP = 5


def ev_pop(Ts, pi, names):
    e = L.eval_scoring({a: Ts[a][:, pi, :] for a in Ts}, names)
    m = R.my_eval({a: Ts[a][:, pi, :] for a in Ts}, names)
    dd = max([abs(e['denE'] - m['denE'])] + [abs(e['D'][a] - m['D'][a]) for a in names])
    return e, dd


# ================================================================== A9-1 (a)
a1a = {}
mx = 0.
for pi in range(NPOP):
    e, dd = ev_pop({a: TS[a] for a in ['F0', 'E', 'N', 'P']}, pi, ['N', 'P'])
    mx = max(mx, dd)
    den = e['denE']; n = e['n']
    a1a[R.POPNAMES[pi]] = dict(n=n, denE=den, R_pp=den / NLEV, RR_N=L.ratio(e['D']['N'], den), RR_P=L.ratio(e['D']['P'], den),
                               RR_N_minus_RR_P=L.ratio(e['D']['N'], den) - L.ratio(e['D']['P'], den),
                               D_N_F0_dec_eq=L.dec_eq(e['D']['N'], n), D_P_F0_dec_eq=L.dec_eq(e['D']['P'], n))
V['A9_1a'] = a1a
V['checks']['A9_1a_lib_vs_own_frontier_max_abs'] = mx
log('A9-1a', json.dumps({k: (v['R_pp'], v['RR_N'], v['RR_P']) for k, v in a1a.items()}))

# ================================================================== A9-1 (b)
a1b = {}
for j in range(1, 21):
    u = round(0.05 * j, 2)
    f = 10. ** (0.025 * u)
    Xo = R.grid_tables(runs, None, cbs, crit_override=lambda r, f=f: r['crit']['F0'] / f)
    Ts = {'F0': TS['F0'], 'E': TS['E'], 'OFF': Xo.sum(axis=0)}
    e, dd = ev_pop(Ts, 0, ['OFF'])
    a1b['%.2f' % u] = L.ratio(e['D']['OFF'], e['denE'])
vals = np.array(list(a1b.values()))
V['A9_1b'] = dict(RR_by_u=a1b, min=float(vals.min()), max=float(vals.max()), range=float(vals.max() - vals.min()))
log('A9-1b', V['A9_1b']['min'], V['A9_1b']['max'])

# ================================================================== A9-1 (c) gridless
GL = {}
mxg = 0.
for a in ['F0', 'E', 'N', 'P', 'NA', 'A1', 'CK3', 'Q']:
    T, thr = R.gridless_table(runs, crit_fun[a], cbs)
    G = np.stack([R.gridless_at(T, thr, g) for g in GRID])
    mxg = max(mxg, float(np.max(np.abs(G - TS[a]))))
    if not np.array_equal(G[..., [0, 1, 3, 4]], TS[a][..., [0, 1, 3, 4]]):
        raise RuntimeError('gridless table at the grid differs from the grid table for %s' % a)
    GL[a] = T
    log('gridless', a, T.shape[0], 'points')
V['checks']['A9_1c_gridless_at_grid_vs_lib_max_abs_sum'] = mxg
a1c = {}
mxc = 0.
for pi in range(NPOP):
    names = ['N', 'P', 'NA', 'A1', 'CK3', 'Q']
    e, dd = ev_pop(GL, pi, names)
    mxc = max(mxc, dd)
    den = e['denE']; n = e['n']
    a1c[R.POPNAMES[pi]] = dict(n=n, denE=den, R_pp=den / NLEV, C_top=e['C'],
                               **{'RR_' + a: L.ratio(e['D'][a], den) for a in names},
                               D_N_F0_dec_eq=L.dec_eq(e['D']['N'], n), D_P_F0_dec_eq=L.dec_eq(e['D']['P'], n),
                               D_N_P_dec_eq=L.dec_eq(e['D']['N'] - e['D']['P'], n),
                               n_points={a: int(GL[a].shape[0]) for a in GL})
V['A9_1c'] = a1c
V['checks']['A9_1c_lib_vs_own_frontier_max_abs'] = mxc
log('A9-1c all', json.dumps(a1c['all']))

# ================================================================== A9-3 per-phase scales
eP = L.eval_scoring({a: TS[a][:, 0, :] for a in ['F0', 'E']}, [])
cur0 = R.curves({a: TS[a][:, 0, :] for a in ['F0', 'E']})
LEV = R.levels(cur0)
c0, w0 = cur0['F0'][0][0], cur0['F0'][1][0]
F_F0 = R.step_front(*cur0['F0'], LEV); F_E = R.step_front(*cur0['E'], LEV)
DEN = float(np.sum(F_F0 - F_E))
assert abs(DEN - eP['denE']) < 1e-9
N_ALL = float(TS['F0'][0, 0, 0])
NG = GRID.size


def phase_counts(phase_arrays):
    """W, S, K (n_runs, 3, 202) of F0 per phase (phases given per run, over evaluated decisions)."""
    W = np.zeros((len(runs), 3, NG)); S = np.zeros_like(W); K = np.zeros_like(W)
    for ri, (r, cb) in enumerate(zip(runs, cbs)):
        ph = phase_arrays[ri]
        masks = tuple(r['ev'] & (ph == p) for p in range(3))
        assert np.array_equal(masks[0] | masks[1] | masks[2], r['ev'])
        sel = L.select_grid(r['crit']['F0'], GRID, r['idx55'])
        st = L.stats_scored(sel, r['clear1'], cb['sx'], r['vbar'], r['desired'], masks)
        W[ri] = st[:, :, 1].T; S[ri] = st[:, :, 2].T; K[ri] = st[:, :, 3].T
    return W, S, K


def triple(A):
    """A (3, 202) -> flat (202**3,) sums over the three phases, flat index (g0, g1, g2) in C order."""
    return ((A[0][:, None, None] + A[1][None, :, None]) + A[2][None, None, :]).ravel()


def choose(c, Wc, lev):
    """Per level: index of the point with the lowest W among points with c <= level; ties lowest c, then lowest index.
    -1 where none qualifies."""
    if np.isnan(c).any():
        raise RuntimeError('NaN caution in a training set')
    o = np.argsort(c, kind='stable')
    cs = c[o]; ws = Wc[o]
    rm = np.minimum.accumulate(ws)
    p = np.searchsorted(cs, lev, side='right') - 1
    out = np.full(lev.size, -1, np.int64)
    ok = p >= 0
    best = rm[np.clip(p, 0, None)]
    q = np.searchsorted(-rm, -best, side='left')
    out[ok] = o[q[ok]]
    return out


def choose_brute(c, Wc, lev):
    out = np.full(lev.size, -1, np.int64)
    idx = np.arange(c.size)
    for li, lv in enumerate(lev):
        qq = c <= lv
        if qq.any():
            cand = idx[qq]
            out[li] = cand[np.lexsort((cand, c[cand], Wc[cand]))[0]]
    return out


# pooled single-scale per-run tables (partition-free) for the single-scale cross-validation
W1r = X['F0'][:, :, 0, 1]; S1r = X['F0'][:, :, 0, 2]; K1r = X['F0'][:, :, 0, 3]; nr = X['F0'][:, 0, 0, 0]


def per_phase(phase_arrays, tag):
    W, S, K = phase_counts(phase_arrays)
    Wt, St, Kt = W.sum(0), S.sum(0), K.sum(0)
    # identity: the diagonal (g, g, g) equals F0's pooled grid points
    dW = np.max(np.abs((Wt[0] + Wt[1] + Wt[2]) - TS['F0'][:, 0, 1]))
    dS = np.max(np.abs((St[0] + St[1] + St[2]) - TS['F0'][:, 0, 2]))
    if dW != 0:
        raise RuntimeError('phase split does not add up')
    cT = 100. * triple(St) / triple(Kt); wT = 100. * triple(Wt) / N_ALL
    F_ps = R.step_front(cT, wT, LEV)
    gain_in = float(np.sum(F_F0 - F_ps))
    # leave one run out
    nrun = len(runs)
    HO = np.zeros((NLEV, 3)); HO1 = np.zeros((NLEV, 3))
    HOf = np.zeros((NLEV, 3)); HO1f = np.zeros((NLEV, 3))     # variant: no qualifying training point -> index 0 (zero margin)
    nofeas = np.zeros(NLEV, int); nofeas1 = np.zeros(NLEV, int)
    brute_checked = 0
    for ri in range(nrun):
        oth = np.array([j for j in range(nrun) if j != ri])
        Wtr, Str, Ktr = W[oth].sum(0), S[oth].sum(0), K[oth].sum(0)
        ctr = 100. * triple(Str) / triple(Ktr); wtr = triple(Wtr)
        ch = choose(ctr, wtr, LEV)
        if ri < 2:                                     # brute-force check of the choice on a subset of levels
            sub = np.arange(0, NLEV, 25)
            chb = choose_brute(ctr, wtr, LEV[sub])
            if not np.array_equal(chb, ch[sub]):
                raise RuntimeError('choice check failed')
            brute_checked += sub.size
        g0, rem = np.divmod(np.where(ch >= 0, ch, 0), NG * NG); g1, g2 = np.divmod(rem, NG)
        hw = W[ri, 0, g0] + W[ri, 1, g1] + W[ri, 2, g2]
        hs = S[ri, 0, g0] + S[ri, 1, g1] + S[ri, 2, g2]
        hk = K[ri, 0, g0] + K[ri, 1, g1] + K[ri, 2, g2]
        ok = ch >= 0
        nofeas += ~ok
        HO[ok] += np.stack([hw, hs, hk], 1)[ok]
        HOf += np.stack([hw, hs, hk], 1)                       # ch = -1 was mapped to flat index 0 = (0, 0, 0)
        # one scale
        c1 = 100. * S1r[oth].sum(0) / K1r[oth].sum(0); w1 = W1r[oth].sum(0)
        ch1 = choose(c1, w1, LEV)
        chb1 = choose_brute(c1, w1, LEV)
        if not np.array_equal(chb1, ch1):
            raise RuntimeError('single-scale choice check failed')
        ok1 = ch1 >= 0
        nofeas1 += ~ok1
        g = np.where(ok1, ch1, 0)
        HO1[ok1] += np.stack([W1r[ri, g], S1r[ri, g], K1r[ri, g]], 1)[ok1]
        HO1f += np.stack([W1r[ri, g], S1r[ri, g], K1r[ri, g]], 1)
    valid = nofeas == 0; valid1 = nofeas1 == 0
    cps = 100. * HO[valid, 1] / HO[valid, 2]; wps = 100. * HO[valid, 0] / N_ALL
    c1h = 100. * HO1[valid1, 1] / HO1[valid1, 2]; w1h = 100. * HO1[valid1, 0] / N_ALL
    Fps_cv = R.step_front(np.concatenate([[c0], cps]), np.concatenate([[w0], wps]), LEV)
    F1_cv = R.step_front(np.concatenate([[c0], c1h]), np.concatenate([[w0], w1h]), LEV)
    G_cv = float(np.sum(F1_cv - Fps_cv)); G_cv_in = float(np.sum(F_F0 - Fps_cv))
    Fps_f = R.step_front(np.concatenate([[c0], 100. * HOf[:, 1] / HOf[:, 2]]), np.concatenate([[w0], 100. * HOf[:, 0] / N_ALL]), LEV)
    F1_f = R.step_front(np.concatenate([[c0], 100. * HO1f[:, 1] / HO1f[:, 2]]), np.concatenate([[w0], 100. * HO1f[:, 0] / N_ALL]),
                        LEV)
    variant = dict(note='variant: where no training point has caution <= the level, the zero-margin choice (index 0) is applied',
                   G_cv_share=float(np.sum(F1_f - Fps_f)) / DEN, G_cv_vs_in_share=float(np.sum(F_F0 - Fps_f)) / DEN,
                   G_cv_pp=float(np.sum(F1_f - Fps_f)) / NLEV, G_cv_vs_in_pp=float(np.sum(F_F0 - Fps_f)) / NLEV)
    out = dict(gain_in_sum=gain_in, gain_in_pp=gain_in / NLEV, gain_in_share=gain_in / DEN,
               G_cv_sum=G_cv, G_cv_pp=G_cv / NLEV, G_cv_share=G_cv / DEN,
               G_cv_vs_in_sum=G_cv_in, G_cv_vs_in_pp=G_cv_in / NLEV, G_cv_vs_in_share=G_cv_in / DEN,
               single_cv_vs_in_sum=float(np.sum(F_F0 - F1_cv)), single_cv_vs_in_pp=float(np.sum(F_F0 - F1_cv)) / NLEV,
               levels_without_feasible_training_choice_ps=int((~valid).sum()),
               levels_without_feasible_training_choice_single=int((~valid1).sum()),
               run_level_pairs_without_choice_ps=int(nofeas.sum()), run_level_pairs_without_choice_single=int(nofeas1.sum()),
               levels_index_without_choice_ps=np.nonzero(~valid)[0].tolist(),
               levels_index_without_choice_single=np.nonzero(~valid1)[0].tolist(),
               diag_identity_max_abs_S=float(dS), brute_checked_levels=brute_checked, variant_fallback_zero=variant)
    log('A9-3', tag, json.dumps(out))
    return out, F_ps, Fps_cv, F1_cv


V['A9_3'] = dict(R_pp=DEN / NLEV, denE=DEN, n=N_ALL)
ph_truth = [r['ph'] for r in runs]
V['A9_3']['a_truth_phase'], *_ = per_phase(ph_truth, 'truth')

# estimated phase
LEAD = {}
for r in runs:
    z = np.load(R.OUTA / 'lead' / (r['run'] + '.npz'), allow_pickle=False)
    d = {k: z[k] for k in z.files}
    if not np.array_equal(d['k'], r['k']):
        raise RuntimeError('lead k differs: %s' % r['run'])
    if not np.array_equal(d['evaluated'].astype(bool), r['ev']):
        raise RuntimeError('lead evaluated differs: %s' % r['run'])
    if not np.array_equal(d['phase'].astype(np.int64), r['ph']):
        raise RuntimeError('lead phase differs: %s' % r['run'])
    LEAD[r['run']] = d


def est_phase(d, thr_a=-1.0):
    lf = d['lead_found'].astype(bool); vh = d['vhat']; ah = d['ahat_long']
    with np.errstate(invalid='ignore'):
        st = lf & (vh <= 0.5)
        br = lf & (vh > 0.5) & np.isfinite(ah) & (ah <= thr_a)
    return np.where(st, 2, np.where(br, 1, 0)).astype(np.int64)


ph_est = [est_phase(LEAD[r['run']]) for r in runs]
V['A9_3']['b_estimated_phase'], *_ = per_phase(ph_est, 'estimated')
cm = np.zeros((3, 3), int)
for r, pe in zip(runs, ph_est):
    for t in range(3):
        for e_ in range(3):
            cm[t, e_] += int(np.sum(r['ev'] & (r['ph'] == t) & (pe == e_)))
V['A9_3']['b_confusion_truth_rows_est_cols'] = cm.tolist()
V['A9_3']['b_agreement'] = float(np.trace(cm) / cm.sum())
V['A9_3']['b_ratio_Gcv_est_over_Gcv_truth'] = (V['A9_3']['b_estimated_phase']['G_cv_sum'] /
                                               V['A9_3']['a_truth_phase']['G_cv_sum'])
log('confusion', cm.tolist())

# ================================================================== A9-4 (b) attribution
bins_t = ['before the stop', '[0,1)', '[1,2)', '[2,5)', '[5,10)', '>=10']


def tbin(tss):
    out = np.full(tss.shape, 0, np.int64)
    out[(tss >= 0) & (tss < 1)] = 1; out[(tss >= 1) & (tss < 2)] = 2; out[(tss >= 2) & (tss < 5)] = 3
    out[(tss >= 5) & (tss < 10)] = 4; out[tss >= 10] = 5
    return out


bins_v = ['vhat<=0.5', '(0.5,1]', '(1,2]', '>2', 'no estimate']


def vbin(vh):
    out = np.full(vh.shape, 4, np.int64)
    with np.errstate(invalid='ignore'):
        out[vh <= 0.5] = 0; out[(vh > 0.5) & (vh <= 1)] = 1; out[(vh > 1) & (vh <= 2)] = 2; out[vh > 2] = 3
    return out


TB = []; VB = []; first_ev_info = []
for r in runs:
    d = LEAD[r['run']]
    ph = d['phase'].astype(np.int64)
    i2 = np.nonzero(ph == 2)[0]
    if i2.size:
        tss = d['now'] - d['now'][i2[0]]
        first_ev_info.append(bool(r['ev'][i2[0]]))
    else:
        tss = np.full(ph.shape, -np.inf)
    TB.append(tbin(tss))
    vh = np.where(d['lead_found'].astype(bool), d['vhat'], np.nan)
    VB.append(vbin(vh))
V['checks']['A9_4b_runs_with_phase2'] = len(first_ev_info)
V['checks']['A9_4b_first_phase2_decision_is_evaluated_all_runs'] = all(first_ev_info)
V['checks']['A9_4b_runs_whose_first_phase2_decision_is_not_evaluated_have_no_evaluated_phase2'] = all(
    (not r['ev'][np.nonzero(LEAD[r['run']]['phase'] == 2)[0][0]]) <= (not np.any(r['ev'] & (r['ph'] == 2))) for r in runs)
SEL = {a: [L.select_grid(r['crit'][a], GRID, r['idx55']) for r in runs] for a in ['F0', 'E', 'CK3', 'A1', 'N']}
a4b = {}
for pi, pname in ((0, 'all'), (4, 'after_stop_phase2')):
    Tpop = {a: TS[a][:, pi, :] for a in ['F0', 'E', 'CK3', 'A1', 'N']}
    e = L.eval_scoring(Tpop, ['E', 'CK3', 'A1', 'N'])
    cur = R.curves(Tpop)
    lev = R.levels(cur)
    chF0 = R.front_choice(*cur['F0'], lev)
    fl0 = []
    for ri, r in enumerate(runs):
        sel = SEL['F0'][ri][chF0]                        # (201, n)
        fl0.append(cbs[ri]['wg'][np.arange(sel.shape[1])[None, :], sel])
    res = {}
    for a in ['E', 'CK3', 'A1', 'N']:
        ch = R.front_choice(*cur[a], lev)
        tot = 0.; byt = np.zeros(6); byv = np.zeros(5)
        for ri, r in enumerate(runs):
            if a == 'E':
                sel = SEL['E'][ri][ch]
            else:
                sel = np.where((ch == 0)[:, None], SEL['F0'][ri][0][None, :], SEL[a][ri][np.clip(ch - 1, 0, None)])
            fa = cbs[ri]['wg'][np.arange(sel.shape[1])[None, :], sel]
            m = r['masks'][pi]
            contrib = (fl0[ri] - fa).sum(axis=0) / NLEV * m
            tot += contrib.sum()
            byt += np.bincount(TB[ri], weights=contrib, minlength=6)
            byv += np.bincount(VB[ri], weights=contrib, minlength=5)
        res[a] = dict(total_dec_eq=float(tot), dec_eq_of_record=L.dec_eq(e['D'][a], e['n']),
                      by_time_since_stop=dict(zip(bins_t, byt.tolist())), by_vhat=dict(zip(bins_v, byv.tolist())))
        if abs(tot - L.dec_eq(e['D'][a], e['n'])) > 1e-9:
            raise RuntimeError('attribution total differs from dec_eq for %s %s' % (pname, a))
    a4b[pname] = res
V['A9_4b'] = a4b
log('A9-4b', json.dumps({p: {a: v['total_dec_eq'] for a, v in d.items()} for p, d in a4b.items()}))

# ================================================================== A9-6 stop reliance
cbX = []
for r in runs:
    z = np.load(C.pathlib.Path(r'ARS_TRIAL\revision_v11\analysis\out\ext') / (r['run'] + '.npz'),
                allow_pickle=False)
    if not np.array_equal(z['k'], r['k']):
        raise RuntimeError('ext k differs')
    sX = L.clean_clear(z['clearX_t0p75_a6p0']) > 0.
    cbX.append(R.contrib(r, safe_x=sX))
XX = {a: R.grid_tables(runs, None, cbX, crit_override=crit_fun[a]) for a in ['F0', 'E', 'N', 'CK3', 'A1', 'NA']}
SELg = {a: [L.select_grid(crit_fun[a](r), GRID, r['idx55']) for r in runs] for a in XX}
SELO = [L.select_first_safe(cb['sx'], r['idx55']) for r, cb in zip(runs, cbX)]
XX['O'] = np.stack([L.stats_scored(s, r['clear1'], cb['sx'], r['vbar'], r['desired'], r['masks'])
                    for s, r, cb in zip(SELO, runs, cbX)])
TSX = {a: XX[a].sum(axis=0) for a in XX}
FLAG = [cb['sx'] & ~cb['s1'] for cb in cbX]                   # W1-unsafe but stop-safe
a6 = {}
for pi in range(NPOP):
    Tpop = {a: TSX[a][:, pi, :] for a in TSX}
    cur = R.curves(Tpop)
    lev = R.levels(cur)
    e = L.eval_scoring(Tpop, ['N', 'CK3', 'A1', 'NA', 'O'])
    npop = e['n']
    res = dict(n=npop, R_pp_stop_scoring=e['denE'] / NLEV)
    for a in ['F0', 'E', 'N', 'CK3', 'A1', 'NA', 'O']:
        ch = R.front_choice(*cur[a], lev)
        if (ch < 0).any():
            raise RuntimeError('no frontier point at a level')
        cnt = 0.
        for ri, r in enumerate(runs):
            m = r['masks'][pi]
            if a in ('F0', 'E'):
                sel = SELg[a][ri][ch]
            elif a == 'O':
                sel = np.where((ch == 0)[:, None], SELg['F0'][ri][0][None, :], SELO[ri][[0] * NLEV])
            else:
                sel = np.where((ch == 0)[:, None], SELg['F0'][ri][0][None, :], SELg[a][ri][np.clip(ch - 1, 0, None)])
            f = FLAG[ri][np.arange(sel.shape[1])[None, :], sel]
            cnt += float((f & m[None, :]).sum())
        res[a] = cnt / NLEV / npop
        if a == 'O':
            res['O_levels_at_F0_g0_point'] = int((ch == 0).sum())
    # O as one selection, no frontier
    cntO = sum(float((FLAG[ri][np.arange(r['n_dec']), SELO[ri][0]] & r['masks'][pi]).sum()) for ri, r in enumerate(runs))
    res['O_single_selection'] = cntO / npop
    a6[R.POPNAMES[pi]] = res
V['A9_6'] = dict(note='share (fraction of the population) of decisions whose selected row is W1-unsafe but stop-safe, '
                      'averaged over the 201 levels of the population (stop scoring tau 0.75 s, 6 m/s^2)', pops=a6)
log('A9-6', json.dumps({p: {a: a6[p][a] for a in ['F0', 'E', 'N', 'CK3', 'A1', 'O']} for p in ['all', 'moving']}))

# ================================================================== A9-7 time-gap margin
TG = {}
for r in runs:
    z = np.load(R.OUTA / 'tg' / (r['run'] + '.npz'), allow_pickle=False)
    if not np.array_equal(z['k'], r['k']):
        raise RuntimeError('tg k differs')
    TG[r['run']] = {k: z[k] for k in ('cTG1', 'cTG2', 'cTG4')}
XT = {a: R.grid_tables(runs, None, cbs, crit_override=(lambda r, a=a: TG[r['run']][a])) for a in ('cTG1', 'cTG2', 'cTG4')}
a7 = {}
for pi in range(NPOP):
    Ts = {'F0': TS['F0'], 'E': TS['E'], 'TG1': XT['cTG1'].sum(0), 'TG2': XT['cTG2'].sum(0), 'TG4': XT['cTG4'].sum(0)}
    e, dd = ev_pop(Ts, pi, ['TG1', 'TG2', 'TG4'])
    a7[R.POPNAMES[pi]] = dict(n=e['n'], R_pp=e['denE'] / NLEV, **{'RR_' + a: L.ratio(e['D'][a], e['denE'])
                                                                    for a in ['TG1', 'TG2', 'TG4']},
                              D_TG2_dec_eq=L.dec_eq(e['D']['TG2'], e['n']))
V['A9_7'] = a7
log('A9-7', json.dumps({p: a7[p]['RR_TG2'] for p in a7}))

# ================================================================== A9-5 tuning runs
DRY = pathlib.Path(r'<library folder>\extract')
stems = sorted(pathlib.Path(p).stem for p in glob.glob(str(DRY / '*.npz')))
truns = []
for s in stems:
    z = np.load(C.STORED / (s + '.npz'), allow_pickle=False)
    x = np.load(DRY / (s + '.npz'), allow_pickle=False)
    m = json.loads(str(z['meta']))
    if not np.array_equal(z['k'], x['k']):
        raise RuntimeError('tuning k differs: %s' % s)
    if m.get('family') != 'lead_braking' or m.get('set') != 'tuning':
        raise RuntimeError('not a lead-braking tuning run: %s' % s)
    ev = z['evaluated'].astype(bool); v0 = z['v0']; ph = x['phase'].astype(np.int64)
    truns.append(dict(run=s, desired=float(m['desired']), ev=ev, v0=v0, ph=ph, vbar=z['vbar'], idx55=z['idx55'],
                      clear1=L.clean_clear(z['clear']), masks=C.masks_of(ev, v0, ph), n_dec=len(z['k']),
                      crit={'F0': z['cF0'], 'E': z['cE'], 'N': z['cN'], 'NA': x['cNA'], 'A1': x['cA1'], 'CK3': x['cCK3'],
                            'Q': x['cQ']}))
tcbs = [R.contrib(r) for r in truns]
XTu = {a: R.grid_tables(truns, a, tcbs) for a in SRC}
TSu = {a: XTu[a].sum(0) for a in XTu}
a5 = dict(runs=stems, n_runs=len(stems), pops={})
for pi in range(NPOP):
    e, dd = ev_pop(TSu, pi, ['N', 'NA', 'A1', 'CK3', 'Q'])
    a5['pops'][R.POPNAMES[pi]] = dict(n=e['n'], denE=e['denE'], R_pp=e['denE'] / NLEV,
                                      **{'RR_' + a: L.ratio(e['D'][a], e['denE']) for a in ['N', 'NA', 'A1', 'CK3', 'Q']})
ph_n = np.array([a5['pops'][p]['n'] for p in ['phase0', 'phase1', 'phase2']])
ph_R = np.array([a5['pops'][p]['R_pp'] for p in ['phase0', 'phase1', 'phase2']])
wmean = float(np.sum(ph_n * ph_R) / np.sum(ph_n))
a5['phase_room_decision_weighted_mean_pp'] = wmean
a5['ratio_pooled_room_to_weighted_phase_mean'] = a5['pops']['all']['R_pp'] / wmean
a5['phase3_decisions'] = int(sum((r['ev'] & (r['ph'] == 3)).sum() for r in truns))
V['A9_5'] = a5
log('A9-5', json.dumps({p: (a5['pops'][p]['n'], a5['pops'][p]['R_pp']) for p in a5['pops']}), wmean,
    a5['ratio_pooled_room_to_weighted_phase_mean'], a5['pops']['all']['RR_CK3'], a5['pops']['all']['RR_A1'])

V['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); V['seconds'] = time.time() - T00
V['lib_sha256'] = L.sha256_file(HERE / 'rc_lib_v12.py'); V['main_sha256'] = L.sha256_file(HERE / 'rc_main_v12.py')
V['log'] = LOG
OUT.write_text(R.jdump(V), encoding='utf-8')
log('written', OUT)
