"""Engine for the fresh-run recount (package B, v13). Lineage: recount\rc_core.py (gridless frontier engine, margin ratio, E5 ranks),
generalised to an arbitrary run set. Scoring library optA_lib_v02 imported unchanged."""
import sys, os, json
import numpy as np
from scipy.stats import rankdata

sys.path.insert(0, r'<library folder>\code')
import optA_lib_v02 as L

NS = L.NST
GMAX = 1000.
M_REC, A_REC = 1.1029, 0.05
# ---------------------------------------------------------------------------------------------- gridless stats engine
def breakpoints(Cs):
    """g values at which some decision's selected row can change, within [0, 1000]: 0, every distinct critical value in (0,1000),
    and 1000 (selection is constant on (previous breakpoint, breakpoint])."""
    v = np.concatenate([c[np.isfinite(c)].ravel() for c in Cs])
    v = v[(v > 0) & (v < GMAX)]
    return np.concatenate([[0.], np.unique(v), [GMAX]])


def _terms(clear1, safe_x, vbar, des):
    """Per (decision,row) terms of stats_scored: wrong go (1), caution value (2), caution count (3), wrong go if safe exists (4)."""
    safe = clear1 > 0.
    orc = safe.argmax(axis=1)
    ar = np.arange(len(des))
    ct = np.where(safe, (vbar[ar, orc][:, None] - vbar) / des[:, None], 0.)
    anysX = safe_x.any(axis=1)
    w1 = (~safe_x).astype(float)
    w4 = (anysX[:, None] & ~safe_x).astype(float)
    return w1, ct, safe.astype(float), w4


def stats_curve(C, G, clear1, safe_x, vbar, des, idx55, masks):
    """Summed statistics (len(G), len(masks), NST) of the first-feasible-row selection at every g in G, built from the intervals of g
    on which each row is selected: row r is selected iff prefix-max(C_<r) < g <= C_r; fallback row idx55 iff g > max C.
    Equal to select_grid + stats_scored at those g (verified in selftest)."""
    n = C.shape[0]
    Cn = np.where(np.isnan(C), -np.inf, C)
    pm = np.maximum.accumulate(Cn, axis=1)
    pm = np.concatenate([np.full((n, 1), -1.), pm[:, :-1]], axis=1)
    pm = np.maximum(pm, -1.)
    mx = np.maximum(Cn.max(axis=1), -1.)
    w1, ct, cn, w4 = _terms(clear1, safe_x, vbar, des)
    F = np.stack([w1, ct, cn, w4], axis=2)          # (n,17,4) -> columns 1..4
    valid = Cn > pm
    di, ri = np.nonzero(valid)
    s = np.searchsorted(G, pm[di, ri], side='right'); e = np.searchsorted(G, Cn[di, ri], side='right')
    fv = F[di, ri]
    di2 = np.arange(n)
    s2 = np.searchsorted(G, mx, side='right'); e2 = np.full(n, len(G))
    fv2 = F[di2, idx55]
    S = np.concatenate([s, s2]); E = np.concatenate([e, e2]); FV = np.concatenate([fv, fv2]); DI = np.concatenate([di, di2])
    NG = len(G)
    out = np.zeros((NG, len(masks), NS))
    for mi, m in enumerate(masks):
        mm = m[DI].astype(float)
        out[:, mi, 0] = m.sum()
        for c in range(4):
            wts = FV[:, c] * mm
            d = np.bincount(S, wts, minlength=NG + 1) - np.bincount(E, wts, minlength=NG + 1)
            out[:, mi, 1 + c] = np.cumsum(d)[:NG]
    return out


def stats_grid(C, grid, clear1, safe_x, vbar, des, idx55, masks):
    sel = L.select_grid(C, grid, idx55)
    return L.stats_scored(sel, clear1, safe_x, vbar, des, masks)


# ---------------------------------------------------------------------------------------------- run-set container
class RunSet:
    """Evaluated decisions of a list of runs, arrays kept per run (evaluated rows only)."""

    def __init__(self, data, names):
        self.names = names
        self.d = []
        for nm in names:
            r = data[nm]
            ev = r['evaluated'].astype(bool)
            q = {k: (v[ev] if isinstance(v, np.ndarray) and v.ndim >= 1 and v.shape[0] == ev.shape[0] else v) for k, v in r.items()}
            q['_ev_all'] = ev
            self.d.append(q)
        self.n_eval = [int(len(q['k'])) for q in self.d]

# ---------------------------------------------------------------------------------------------- oracle construction (E5 family)
def margin_ratio_rows(rs, masks=None):
    out = []
    for i, q in enumerate(rs.d):
        a, b = q['cF0'], q['cN']
        ok = np.isfinite(a) & np.isfinite(b) & (a > 0) & (b > 0)
        if masks is not None:
            ok = ok & masks[i][:, None]
        out.append(np.sqrt(a[ok] / b[ok]))
    return np.concatenate(out)


def margin_stats(ratio):
    m = float(np.median(ratio)); q05, q95 = [float(v) for v in np.percentile(ratio, [5, 95])]
    A = (q95 - q05) / (2 * m)
    return dict(n=int(ratio.size), median=m, q05=q05, q95=q95, A=A, share_within5=float(np.mean(np.abs(ratio / m - 1) <= 0.05)))


def ranks_u(rs, key_f0='cF0', key_e='cE', masks=None):
    """u_i = (rank(r_i) - 0.5)/n over decisions that have rows with finite positive g*_F0 and g*_E (mid-ranks); others 0.5.
    r_i = median over those rows of sqrt(g*_F0/g*_E)."""
    rvals = []; has = []
    for i, q in enumerate(rs.d):
        a, b = q[key_f0], q[key_e]
        ok = np.isfinite(a) & np.isfinite(b) & (a > 0) & (b > 0)
        if masks is not None:
            ok = ok & masks[i][:, None]
        with np.errstate(divide='ignore', invalid='ignore'):
            rho = np.where(ok, np.sqrt(a / b), np.nan)
        any_ = ok.any(axis=1)
        r = np.full(len(a), np.nan)
        if any_.any():
            r[any_] = np.nanmedian(rho[any_], axis=1)
        rvals.append(r); has.append(any_)
    allr = np.concatenate(rvals); allh = np.concatenate(has)
    n = int(allh.sum())
    u = np.full(len(allr), 0.5)
    if n:
        u[allh] = (rankdata(allr[allh], method='average') - 0.5) / n
    out = []; p = 0
    for r in rvals:
        out.append(u[p:p + len(r)]); p += len(r)
    return out


def oracle_C(rs, us, m, A):
    out = []
    for q, u in zip(rs.d, us):
        f = m * (1. + A * (2. * u - 1.))
        out.append(q['cF0'] / (f ** 2)[:, None])
    return out
