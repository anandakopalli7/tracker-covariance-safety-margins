"""Diagnostic 2 (post comparison): candidate single-scale held-out constructions. Does not change RECOUNT_VALUES_v12.json."""
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
W = np.zeros((len(runs), 3, NG)); S = np.zeros_like(W); K = np.zeros_like(W)
for ri, (r, cb) in enumerate(zip(runs, cbs)):
    masks = tuple(r['ev'] & (r['ph'] == p) for p in range(3))
    sel = L.select_grid(r['crit']['F0'], GRID, r['idx55'])
    st = L.stats_scored(sel, r['clear1'], cb['sx'], r['vbar'], r['desired'], masks)
    W[ri] = st[:, :, 1].T; S[ri] = st[:, :, 2].T; K[ri] = st[:, :, 3].T


def choose(c, Wc, lev):
    o = np.argsort(c, kind='stable'); cs = c[o]; ws = Wc[o]; rm = np.minimum.accumulate(ws)
    p = np.searchsorted(cs, lev, side='right') - 1
    out = np.full(lev.size, -1, np.int64); ok = p >= 0
    best = rm[np.clip(p, 0, None)]; q = np.searchsorted(-rm, -best, side='left'); out[ok] = o[q[ok]]
    return out


def heldout(decode):
    HO = np.zeros((NLEV, 3)); nof = np.zeros(NLEV, int)
    for ri in range(len(runs)):
        oth = np.array([j for j in range(len(runs)) if j != ri])
        St = S[oth].sum(0).sum(0); Kt = K[oth].sum(0).sum(0); Wt = W[oth].sum(0).sum(0)
        ch = choose(100. * St / Kt, Wt, LEV); ok = ch >= 0; nof += ~ok; g = np.where(ok, ch, 0)
        g0, g1, g2 = decode(g)
        HO[ok] += np.stack([W[ri, 0, g0] + W[ri, 1, g1] + W[ri, 2, g2], S[ri, 0, g0] + S[ri, 1, g1] + S[ri, 2, g2],
                            K[ri, 0, g0] + K[ri, 1, g1] + K[ri, 2, g2]], 1)[ok]
    v = nof == 0
    c = 100. * HO[v, 1] / HO[v, 2]; w = 100. * HO[v, 0] / N_ALL
    F1 = R.step_front(np.concatenate([[c0], c]), np.concatenate([[w0], w]), LEV)
    return float(np.sum(F1 - F_F0))


z = lambda g: np.zeros_like(g)
out = {'diag (g,g,g) (my reading)': heldout(lambda g: (g, g, g)),
       '(0,0,g)': heldout(lambda g: (z(g), z(g), g)), '(g,0,0)': heldout(lambda g: (g, z(g), z(g))),
       '(0,g,0)': heldout(lambda g: (z(g), g, z(g))), '(0,g,g)': heldout(lambda g: (z(g), g, g)),
       '(g,g,0)': heldout(lambda g: (g, g, z(g))), '(g,0,g)': heldout(lambda g: (g, z(g), g))}
print(json.dumps(out, indent=1))
print('first program F1cv_minus_F1 (LORO): -640.9167671893848')
open('rc_diag_a93b_v12.json', 'w', encoding='utf-8').write(json.dumps(out, indent=1))
