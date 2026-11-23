"""Diagnostic (post comparison): alternative constructions of the A9-3 held-out frontier, to locate the disagreement with the
first program. Does not change RECOUNT_VALUES_v12.json. Writes rc_diag_a93_v12.json."""
import json, numpy as np
import rc_lib_v12 as R
L = R.L; C = R.C; GRID = R.GRID; NLEV = R.NLEV; NG = GRID.size
runs = C.load_runs(); cbs = [R.contrib(r) for r in runs]
XF = R.grid_tables(runs, 'F0', cbs); XE = R.grid_tables(runs, 'E', cbs)
TS = {'F0': XF.sum(0), 'E': XE.sum(0)}
cur0 = R.curves({a: TS[a][:, 0, :] for a in TS}); LEV = R.levels(cur0)
c0, w0 = cur0['F0'][0][0], cur0['F0'][1][0]
F_F0 = R.step_front(*cur0['F0'], LEV); F_E = R.step_front(*cur0['E'], LEV); DEN = float(np.sum(F_F0 - F_E))
N_ALL = float(TS['F0'][0, 0, 0])
W1r = XF[:, :, 0, 1]; S1r = XF[:, :, 0, 2]; K1r = XF[:, :, 0, 3]


def choose(c, Wc, lev):
    o = np.argsort(c, kind='stable'); cs = c[o]; ws = Wc[o]; rm = np.minimum.accumulate(ws)
    p = np.searchsorted(cs, lev, side='right') - 1
    out = np.full(lev.size, -1, np.int64); ok = p >= 0
    best = rm[np.clip(p, 0, None)]; q = np.searchsorted(-rm, -best, side='left'); out[ok] = o[q[ok]]
    return out


def triple(A):
    return ((A[0][:, None, None] + A[1][None, :, None]) + A[2][None, None, :]).ravel()


def loro(phase_arrays):
    W = np.zeros((len(runs), 3, NG)); S = np.zeros_like(W); K = np.zeros_like(W)
    for ri, (r, cb) in enumerate(zip(runs, cbs)):
        ph = phase_arrays[ri]; masks = tuple(r['ev'] & (ph == p) for p in range(3))
        sel = L.select_grid(r['crit']['F0'], GRID, r['idx55'])
        st = L.stats_scored(sel, r['clear1'], cb['sx'], r['vbar'], r['desired'], masks)
        W[ri] = st[:, :, 1].T; S[ri] = st[:, :, 2].T; K[ri] = st[:, :, 3].T
    HO = np.zeros((NLEV, 3)); HO1 = np.zeros((NLEV, 3)); nof = np.zeros(NLEV, int); nof1 = np.zeros(NLEV, int)
    for ri in range(len(runs)):
        oth = np.array([j for j in range(len(runs)) if j != ri])
        Wtr, Str, Ktr = W[oth].sum(0), S[oth].sum(0), K[oth].sum(0)
        ch = choose(100. * triple(Str) / triple(Ktr), triple(Wtr), LEV)
        ok = ch >= 0; nof += ~ok
        g0, rem = np.divmod(np.where(ok, ch, 0), NG * NG); g1, g2 = np.divmod(rem, NG)
        HO[ok] += np.stack([W[ri, 0, g0] + W[ri, 1, g1] + W[ri, 2, g2], S[ri, 0, g0] + S[ri, 1, g1] + S[ri, 2, g2],
                            K[ri, 0, g0] + K[ri, 1, g1] + K[ri, 2, g2]], 1)[ok]
        ch1 = choose(100. * S1r[oth].sum(0) / K1r[oth].sum(0), W1r[oth].sum(0), LEV)
        ok1 = ch1 >= 0; nof1 += ~ok1; g = np.where(ok1, ch1, 0)
        HO1[ok1] += np.stack([W1r[ri, g], S1r[ri, g], K1r[ri, g]], 1)[ok1]
    return HO, HO1, nof == 0, nof1 == 0


def fronts(HO, valid, variant):
    c = 100. * HO[:, 1] / HO[:, 2]; w = 100. * HO[:, 0] / N_ALL
    if variant == 'literal':
        return R.step_front(np.concatenate([[c0], c[valid]]), np.concatenate([[w0], w[valid]]), LEV)
    if variant == 'no_zero_point':
        return R.step_front(c[valid], w[valid], LEV)
    if variant == 'at_own_level':                      # point of level l counted at level l whatever its held-out caution
        f = np.where(valid, w, np.nan)
        f = np.where(np.isnan(f), w0, f)
        return np.minimum.accumulate(np.minimum(f, w0))
    if variant == 'at_own_level_no_cummin':
        return np.where(valid, w, w0)
    if variant == 'all_points_qualify':
        return np.full(NLEV, min(w0, np.nanmin(w[valid])))
    raise ValueError(variant)


res = {}
for tag, pha in (('truth', [r['ph'] for r in runs]),):
    HO, HO1, v, v1 = loro(pha)
    out = {}
    for var in ['literal', 'no_zero_point', 'at_own_level', 'at_own_level_no_cummin', 'all_points_qualify']:
        Fps = fronts(HO, v, var); F1 = fronts(HO1, v1, var)
        out[var] = dict(G_cv=float(np.nansum(F1 - Fps)), G_cv_vs_in=float(np.nansum(F_F0 - Fps)),
                        F1cv_minus_F1=float(np.nansum(F1 - F_F0)), n_nan=int(np.isnan(Fps).sum() + np.isnan(F1).sum()))
    # held-out points versus their levels
    cps = 100. * HO[:, 1] / HO[:, 2]; c1 = 100. * HO1[:, 1] / HO1[:, 2]
    out['heldout_caution_minus_level_ps'] = dict(min=float(np.nanmin((cps - LEV)[v])), max=float(np.nanmax((cps - LEV)[v])),
                                                 n_above=int(((cps - LEV) > 0)[v].sum()))
    out['heldout_caution_minus_level_single'] = dict(min=float(np.nanmin((c1 - LEV)[v1])), max=float(np.nanmax((c1 - LEV)[v1])),
                                                     n_above=int(((c1 - LEV) > 0)[v1].sum()))
    out['sum_F_F0'] = float(F_F0.sum()); out['DEN'] = DEN
    res[tag] = out
    print(tag, json.dumps(out, indent=1))
open('rc_diag_a93_v12.json', 'w', encoding='utf-8').write(json.dumps(res, indent=1))
