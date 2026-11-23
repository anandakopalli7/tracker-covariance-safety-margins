"""Diagnostic 4 (post comparison): tie-rule variants of the per-phase LORO choice (truth and estimated phase).
Does not change RECOUNT_VALUES_v12.json."""
import json, numpy as np
import rc_lib_v12 as R
L = R.L; C = R.C; GRID = R.GRID; NLEV = R.NLEV; NG = GRID.size
runs = C.load_runs(); cbs = [R.contrib(r) for r in runs]
XF = R.grid_tables(runs, 'F0', cbs); XE = R.grid_tables(runs, 'E', cbs)
TS = {'F0': XF.sum(0), 'E': XE.sum(0)}
cur0 = R.curves({a: TS[a][:, 0, :] for a in TS}); LEV = R.levels(cur0)
c0, w0 = cur0['F0'][0][0], cur0['F0'][1][0]
F_F0 = R.step_front(*cur0['F0'], LEV)
N_ALL = float(TS['F0'][0, 0, 0])


def est_phase(run):
    z = np.load(R.OUTA / 'lead' / (run + '.npz'))
    lf = z['lead_found'].astype(bool); vh = z['vhat']; ah = z['ahat_long']
    with np.errstate(invalid='ignore'):
        return np.where(lf & (vh <= 0.5), 2, np.where(lf & (vh > 0.5) & np.isfinite(ah) & (ah <= -1.0), 1, 0))


def tables(pha):
    W = np.zeros((len(runs), 3, NG)); S = np.zeros_like(W); K = np.zeros_like(W)
    for ri, (r, cb) in enumerate(zip(runs, cbs)):
        masks = tuple(r['ev'] & (pha[ri] == p) for p in range(3))
        sel = L.select_grid(r['crit']['F0'], GRID, r['idx55'])
        st = L.stats_scored(sel, r['clear1'], cb['sx'], r['vbar'], r['desired'], masks)
        W[ri] = st[:, :, 1].T; S[ri] = st[:, :, 2].T; K[ri] = st[:, :, 3].T
    return W, S, K


def triple(A, order):
    a, b, c = (A[order[0]], A[order[1]], A[order[2]])
    return ((a[:, None, None] + b[None, :, None]) + c[None, None, :]).ravel()


def choose_variant(c, Wc, lev, variant):
    n = c.size
    if variant == 'lowest_c_then_highest_index':
        o = np.lexsort((-np.arange(n), c))
    else:
        o = np.argsort(c, kind='stable')
    cs = c[o]; ws = Wc[o]; rm = np.minimum.accumulate(ws)
    p = np.searchsorted(cs, lev, side='right') - 1
    out = np.full(lev.size, -1, np.int64)
    for li in range(lev.size):
        if p[li] < 0:
            continue
        best = rm[p[li]]
        if variant in ('mine', 'lowest_c_then_highest_index'):
            q = int(np.searchsorted(-rm, -best, side='left')); out[li] = o[q]
        elif variant == 'lowest_index_only':                 # lowest W, then lowest flat index (caution ignored)
            cand = o[:p[li] + 1][ws[:p[li] + 1] == best]; out[li] = cand.min()
        elif variant == 'highest_c':                         # lowest W, then highest caution, then lowest index
            sub = np.nonzero(ws[:p[li] + 1] == best)[0]
            cmax = cs[sub].max(); cand = o[sub[cs[sub] == cmax]]; out[li] = cand.min()
    return out


def loro(W, S, K, variant, order=(0, 1, 2)):
    HO = np.zeros((NLEV, 3)); nof = np.zeros(NLEV, int)
    for ri in range(len(runs)):
        oth = np.array([j for j in range(len(runs)) if j != ri])
        Wtr, Str, Ktr = W[oth].sum(0), S[oth].sum(0), K[oth].sum(0)
        ch = choose_variant(100. * triple(Str, order) / triple(Ktr, order), triple(Wtr, order), LEV, variant)
        ok = ch >= 0; nof += ~ok
        a, rem = np.divmod(np.where(ok, ch, 0), NG * NG); b, cc = np.divmod(rem, NG)
        g = [None] * 3; g[order[0]] = a; g[order[1]] = b; g[order[2]] = cc
        HO[ok] += np.stack([W[ri, 0, g[0]] + W[ri, 1, g[1]] + W[ri, 2, g[2]], S[ri, 0, g[0]] + S[ri, 1, g[1]] + S[ri, 2, g[2]],
                            K[ri, 0, g[0]] + K[ri, 1, g[1]] + K[ri, 2, g[2]]], 1)[ok]
    v = nof == 0
    c = 100. * HO[v, 1] / HO[v, 2]; w = 100. * HO[v, 0] / N_ALL
    Fps = R.step_front(np.concatenate([[c0], c]), np.concatenate([[w0], w]), LEV)
    return float(np.sum(F_F0 - Fps))


out = {}
for tag, pha in (('truth', [r['ph'] for r in runs]), ('estimated', [est_phase(r['run']) for r in runs])):
    W, S, K = tables(pha)
    for variant, order in (('mine', (0, 1, 2)), ('mine', (2, 1, 0)), ('lowest_c_then_highest_index', (0, 1, 2)),
                           ('lowest_index_only', (0, 1, 2)), ('highest_c', (0, 1, 2))):
        key = '%s %s order %s' % (tag, variant, order)
        out[key] = loro(W, S, K, variant, order)
        print(key, out[key], flush=True)
print('first program G_cv_vs_in raw: truth 973.3655006031364, estimated 1076.357056694813')
open('rc_diag_a93d_v12.json', 'w', encoding='utf-8').write(json.dumps(out, indent=1))
