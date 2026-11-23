"""Revision v12, AMENDMENT_09 A9-3, v02. New file, 19 Nov 2026. v02 = a9_3_phase_scale_cv_v01.py (kept unchanged) with ONE
correction, found by the independent recount (revision_v12/recount_v12/RECOUNT_COMPARE_v12.md): v01 summed the held-out counts
of a caution level over the folds that had a qualifying choice at that level, so a level at which some folds had none (the lowest
level, for 30 of 35 left-out runs) gave a point that counted only some runs' wrong goes, an operating point that does not exist.
v02 drops the held-out point of every level at which any fold with held-out runs has no qualifying choice (the recount's reading of
the amendment: the held-out frontier is formed from points that cover every run). Everything else is unchanged.
v01 docstring follows.
Revision v12, AMENDMENT_09 A9-3 (review items R13, S27, R6): the per-phase margin scale out of sample and on the tracker's own
phase estimate. New file, 19 Nov 2026. Class average F0 only (the source whose per-phase gain is quoted), 3 s commitment.

(a) Truth phase (the A4 phases 0-2). In sample: the frontier over all scale triples (rev_b2_phase_scale_v02, identity checked).
    Leave one run out: per fold and per pooled caution level of record, the triple with the lowest training wrong-go among triples
    with training caution <= level (ties: lowest caution, then lowest flat index) is applied to the left-out run; left-out counts
    are summed over folds; the held-out frontier is the step frontier of the 201 points with F0's zero-margin point. The same
    with one scale. Gains: G_cv = sum(F1_cv - Fps_cv), G_cv_vs_in = sum(F1_in - Fps_cv), as points (/201) and as shares of the
    in-sample room. Interval: 200 resamples of the draw of record, 5-fold CV over each resample's distinct runs (seed 20261128),
    levels and room rebuilt in each resample.
(b) Estimated phase from A9-4(a): stopped if vhat <= 0.5 m/s; braking if vhat > 0.5 and ahat_long <= thr (thr = -1.0 primary;
    -0.5, -2.0); otherwise before braking. In sample and leave one run out; agreement with the truth phase.
Usage: python -B -X utf8 a9_3_phase_scale_cv_v01.py
"""
import json, time
import numpy as np
import a9_common_v01 as A
C = A.C; L = A.L

OUTF = A.OUT / 'A9_3_PHASE_SCALE_CV_v02.json'
if OUTF.exists():
    raise SystemExit('REFUSED: %s exists' % OUTF)
t00 = time.time()
runs = C.load_runs(); NRUN = len(runs)
CNT = C.cnt_of_record()
PH = [2, 3, 4]
doc = dict(code='a9_3_phase_scale_cv_v02.py', supersedes='A9_3_PHASE_SCALE_CV_v01.json (held-out values only; see docstring)', status='post hoc, descriptive; AMENDMENT_09 A9-3')


def tables_for(masks_key):
    X = C.tables(runs, ('W1',), ['F0', 'E'], masks_key=masks_key)
    return X['F0'], X['E']                       # (35, G, 6, NST)


def levels_from(TF0all, TEall):
    cur = L.curves_w({'F0': TF0all, 'E': TEall}, 0)
    cF0, wF0 = cur['F0']; cE, wE = cur['E']
    lev = L.levels_of(cF0, cE, cF0[0])
    return lev, cF0, wF0, cE, wE


def single_choice(T, lev):
    """T (G, NST) training -> per level the scale index with the lowest wrong go among caution <= level (-1 if none)."""
    rt = L.rates(T); c = rt[1]; w = rt[0]
    _, a = A.frontier_argmin(c, w, lev)
    return a


def triple_choice(Tph, lev):
    """Tph: three (G, NST) training tables -> per level (g0, g1, g2) scale indices (or -1)."""
    U = []; IX = []
    for T in Tph:
        Arr = np.stack([T[:, 1], T[:, 2], T[:, 3]], axis=1)
        u, ix = np.unique(Arr, axis=0, return_index=True)
        U.append(u); IX.append(ix)
    n = float(Tph[0][0, 0] + Tph[1][0, 0] + Tph[2][0, 0])
    W = (U[0][:, 0][:, None, None] + U[1][:, 0][None, :, None] + U[2][:, 0][None, None, :]).ravel()
    S = (U[0][:, 1][:, None, None] + U[1][:, 1][None, :, None] + U[2][:, 1][None, None, :]).ravel()
    K = (U[0][:, 2][:, None, None] + U[1][:, 2][None, :, None] + U[2][:, 2][None, None, :]).ravel()
    with np.errstate(divide='ignore', invalid='ignore'):
        c = 100. * S / K; w = 100. * W / n
    ok = np.isfinite(c) & np.isfinite(w)
    idx_ok = np.nonzero(ok)[0]
    o = np.argsort(c[ok], kind='stable'); cs = c[ok][o]; ws = w[ok][o]; src = idx_ok[o]
    cm = np.minimum.accumulate(ws)
    new = np.concatenate([[True], cm[1:] < cm[:-1]])
    pos = np.maximum.accumulate(np.where(new, np.arange(ws.size), 0))
    j = np.searchsorted(cs, lev, side='right') - 1
    flat = np.where(j >= 0, src[pos[np.clip(j, 0, None)]], -1)
    sh = (U[0].shape[0], U[1].shape[0], U[2].shape[0])
    out = np.full((lev.size, 3), -1, int)
    okl = flat >= 0
    i0, i1, i2 = np.unravel_index(flat[okl], sh)
    out[okl, 0] = IX[0][i0]; out[okl, 1] = IX[1][i1]; out[okl, 2] = IX[2][i2]
    return out


def insample_ps(F0p, Ep, w):
    """In-sample per-phase frontier gain (rev_b2 definition) for run weights w. Returns dict."""
    Tall = np.tensordot(w, F0p[:, :, 0, :], axes=(0, 0)); TE = np.tensordot(w, Ep[:, :, 0, :], axes=(0, 0))
    lev, cF0, wF0, cE, wE = levels_from(Tall, TE)
    f1 = L.frontier(cF0, wF0, lev); fE = L.frontier(cE, wE, lev)
    Tph = [np.tensordot(w, F0p[:, :, pi, :], axes=(0, 0)) for pi in PH]
    ch = triple_choice(Tph, lev)
    W = np.zeros(lev.size); S = np.zeros(lev.size); K = np.zeros(lev.size)
    for q, pi in enumerate(PH):
        g = ch[:, q]; okg = g >= 0
        W[okg] += Tph[q][g[okg], 1]; S[okg] += Tph[q][g[okg], 2]; K[okg] += Tph[q][g[okg], 3]
    n = float(Tall[0, 0])
    with np.errstate(divide='ignore', invalid='ignore'):
        cp = 100. * S / K; wp = 100. * W / n
    cp = np.where(ch[:, 0] >= 0, cp, np.nan); wp = np.where(ch[:, 0] >= 0, wp, np.nan)
    fps = L.frontier(np.concatenate([[cF0[0]], cp]), np.concatenate([[wF0[0]], wp]), lev)
    return dict(den1=float(np.sum(f1 - fE)), gain=float(np.sum(f1 - fps)), n=n)


def cv_gain(F0p, Ep, w, folds):
    """Cross-validated per-phase and single-scale frontiers. w: run weights; folds: list of arrays of run indices (the held-out
    runs of each fold; runs with w = 0 are ignored). Levels and the room from the full weighted sample."""
    Tall = np.tensordot(w, F0p[:, :, 0, :], axes=(0, 0)); TE = np.tensordot(w, Ep[:, :, 0, :], axes=(0, 0))
    lev, cF0, wF0, cE, wE = levels_from(Tall, TE)
    f1 = L.frontier(cF0, wF0, lev); fE = L.frontier(cE, wE, lev)
    acc_ps = np.zeros((lev.size, 3)); acc_1 = np.zeros((lev.size, 3)); none_ps = 0; none_1 = 0
    bad_ps = np.zeros(lev.size, bool); bad_1 = np.zeros(lev.size, bool)          # v02: levels missing a choice in some fold
    for fo in folds:
        wtr = w.copy(); wtr[fo] = 0.
        wte = np.zeros_like(w); wte[fo] = w[fo]
        if wte.sum() == 0 or wtr.sum() == 0:
            continue
        Tph = [np.tensordot(wtr, F0p[:, :, pi, :], axes=(0, 0)) for pi in PH]
        ch = triple_choice(Tph, lev)
        Tte = [np.tensordot(wte, F0p[:, :, pi, :], axes=(0, 0)) for pi in PH]
        for q in range(3):
            g = ch[:, q]; okg = g >= 0
            acc_ps[okg, 0] += Tte[q][g[okg], 1]; acc_ps[okg, 1] += Tte[q][g[okg], 2]; acc_ps[okg, 2] += Tte[q][g[okg], 3]
        none_ps += int((ch[:, 0] < 0).sum()); bad_ps |= ch[:, 0] < 0
        Ttr1 = np.tensordot(wtr, F0p[:, :, 0, :], axes=(0, 0)); Tte1 = np.tensordot(wte, F0p[:, :, 0, :], axes=(0, 0))
        g1 = single_choice(Ttr1, lev); okg = g1 >= 0
        acc_1[okg, 0] += Tte1[g1[okg], 1]; acc_1[okg, 1] += Tte1[g1[okg], 2]; acc_1[okg, 2] += Tte1[g1[okg], 3]
        none_1 += int((~okg).sum()); bad_1 |= ~okg
    n = float(Tall[0, 0])

    def fr(acc):
        with np.errstate(divide='ignore', invalid='ignore'):
            c = 100. * acc[:, 1] / acc[:, 2]; ww = 100. * acc[:, 0] / n
        return L.frontier(np.concatenate([[cF0[0]], c]), np.concatenate([[wF0[0]], ww]), lev)
    acc_ps[bad_ps] = np.nan; acc_1[bad_1] = np.nan                                 # v02: such levels give no point
    fps = fr(acc_ps); f1cv = fr(acc_1)
    den1 = float(np.sum(f1 - fE))
    return dict(den1=den1, n=n, G_cv=float(np.nansum(f1cv - fps)), G_cv_vs_in=float(np.nansum(f1 - fps)),
                F1cv_minus_F1=float(np.nansum(f1cv - f1)), nan_levels=int((~np.isfinite(fps)).sum() + (~np.isfinite(f1cv)).sum()),
                none_ps=none_ps, none_1=none_1, levels_dropped_ps=int(bad_ps.sum()), levels_dropped_1=int(bad_1.sum()))


def summarise(pt, B):
    out = dict(point=pt)
    for k in ('G_cv', 'G_cv_vs_in'):
        out[k + '_pp'] = L.summ(B[k] / L.NLEV, pt[k] / L.NLEV)
        out[k + '_share'] = L.summ(C.rat(B[k], B['den1']), L.ratio(pt[k], pt['den1']))
    return out


# ------------------------------------------------------------------------------------------------ (a) truth phase
F0p, Ep = tables_for('masks')
w1 = np.ones(NRUN)
ins = insample_ps(F0p, Ep, w1)
b2 = json.loads((A.V11 / 'out' / 'REV_B2_PHASESCALE_v02.json').read_text(encoding='utf-8'))['R12b']['point']
doc['identity_insample_vs_v11'] = dict(gain_here=ins['gain'], gain_v11=b2['gain_F0'], den1_here=ins['den1'], den1_v11=b2['den1'],
                                       max_abs_diff=max(abs(ins['gain'] - b2['gain_F0']), abs(ins['den1'] - b2['den1'])))
print('in-sample identity: %s (%.0f s)' % (doc['identity_insample_vs_v11'], time.time() - t00), flush=True)
loro = cv_gain(F0p, Ep, w1, [np.array([i]) for i in range(NRUN)])
print('LORO truth phase: %s (%.0f s)' % (loro, time.time() - t00), flush=True)
rng = np.random.default_rng(20261128)
NB = 200
keys = ['G_cv', 'G_cv_vs_in', 'den1', 'n']
B = {k: np.full(NB, np.nan) for k in keys}
Bin = np.full(NB, np.nan)
for b in range(NB):
    w = CNT[b]
    dist = np.nonzero(w > 0)[0]
    perm = rng.permutation(dist)
    folds = np.array_split(perm, 5)
    e = cv_gain(F0p, Ep, w, folds)
    for k in keys:
        B[k][b] = e[k]
    if (b + 1) % 25 == 0:
        print('  CV bootstrap %d / %d (%.0f s)' % (b + 1, NB, time.time() - t00), flush=True)
# 5-fold point on the full sample (same fold rule, first permutation of a separate stream)
perm0 = np.random.default_rng(20261129).permutation(NRUN)
k5 = cv_gain(F0p, Ep, w1, np.array_split(perm0, 5))
doc['a_truth_phase'] = dict(insample=dict(gain_pp=ins['gain'] / L.NLEV, share=ins['gain'] / ins['den1'], R_pp=ins['den1'] / L.NLEV),
                            loro=dict(G_cv_pp=loro['G_cv'] / L.NLEV, G_cv_share=loro['G_cv'] / loro['den1'],
                                      G_cv_vs_in_pp=loro['G_cv_vs_in'] / L.NLEV, G_cv_vs_in_share=loro['G_cv_vs_in'] / loro['den1'],
                                      raw=loro),
                            fivefold_full_sample=dict(G_cv_pp=k5['G_cv'] / L.NLEV, G_cv_share=k5['G_cv'] / k5['den1'], raw=k5),
                            bootstrap_fivefold=dict(nboot=NB, fold_seed=20261128, **summarise(k5, B)))

# ------------------------------------------------------------------------------------------------ (b) estimated phase
LEAD = A.HERE / 'out' / 'lead'
est = {}
for thr in (-1.0, -0.5, -2.0):
    conf = np.zeros((3, 3), int)
    for r in runs:
        z = np.load(LEAD / (r['run'] + '.npz'), allow_pickle=False)
        if not np.array_equal(z['k'], r['k']):
            raise SystemExit('REFUSED: lead arrays of %s do not match the decisions' % r['run'])
        vh = z['vhat']; ah = z['ahat_long']; fd = z['lead_found'].astype(bool)
        ph = np.zeros(vh.size, np.int64)
        brk = fd & (vh > 0.5) & np.isfinite(ah) & (ah <= thr)
        stp = fd & (vh <= 0.5)
        ph[brk] = 1; ph[stp] = 2
        r['ph_hat'] = ph
        r['masks_hat'] = C.masks_of(r['ev'], r['v0'], ph)
        ev = r['ev']; tp = r['ph'][ev]; hp = ph[ev]
        for i in range(3):
            for j in range(3):
                conf[i, j] += int(((tp == i) & (hp == j)).sum())
    F0h, Eh = tables_for('masks_hat')
    for r in runs:
        r['sel'].clear()
    ins_h = insample_ps(F0h, Eh, w1)
    loro_h = cv_gain(F0h, Eh, w1, [np.array([i]) for i in range(NRUN)])
    est['%.1f' % thr] = dict(confusion_truth_rows_estimate_cols=conf.tolist(),
                             agreement=float(np.trace(conf) / conf.sum()),
                             insample=dict(gain_pp=ins_h['gain'] / L.NLEV, share=ins_h['gain'] / ins_h['den1']),
                             loro=dict(G_cv_pp=loro_h['G_cv'] / L.NLEV, G_cv_share=loro_h['G_cv'] / loro_h['den1'],
                                       G_cv_vs_in_pp=loro_h['G_cv_vs_in'] / L.NLEV, G_cv_vs_in_share=loro_h['G_cv_vs_in'] / loro_h['den1'],
                                       raw=loro_h))
    print('estimated phase thr %.1f: %s (%.0f s)' % (thr, {k: v for k, v in est['%.1f' % thr].items() if k != 'loro'},
                                                     time.time() - t00), flush=True)
doc['b_estimated_phase'] = est
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
doc['common_sha256'] = L.sha256_file(A.HERE / 'a9_common_v01.py')
A.write_out(OUTF, doc)
print('written %s (%.0f s)' % (OUTF, time.time() - t00))
