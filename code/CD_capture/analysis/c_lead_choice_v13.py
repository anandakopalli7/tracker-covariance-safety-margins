"""single_choice and triple_choice, copied verbatim from revision_v12/analysis/a9_3_phase_scale_cv_v02.py (that script runs its
analysis on import, so it cannot be imported). Only the module name of frontier_argmin changes (A -> A9: a9_common_v01)."""
import numpy as np
import cd_common_v13 as CC
A9 = CC.A9; L = CC.L


def single_choice(T, lev):
    """T (G, NST) training -> per level the scale index with the lowest wrong go among caution <= level (-1 if none)."""
    rt = L.rates(T); c = rt[1]; w = rt[0]
    _, a = A9.frontier_argmin(c, w, lev)
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
