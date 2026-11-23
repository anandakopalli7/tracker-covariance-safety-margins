"""Fast gridless frontier distances for many run-weight vectors (bootstrap, double bootstrap). Revision v13, packages C/D.

Reproduces revision_v12/analysis/a9_common_v01.Gridless.curve + optA_lib_v02.eval_scoring (step frontier, primary) exactly:
  * per source and weight vector w: T0 = np.tensordot(w, T0[:, pop, :], axes=(0, 0)) (numpy, as Gridless.curve), then the
    points  T0  and  cumsum_i(d_i * w[ri_i])[keep] + T0  (sequential sums, as np.cumsum);
  * rates (optA_lib_v02.rates): caution c = 100 T2 / T3, wrong go w = 100 T1 / T0 (wi = 0);
  * curves_w: every source except F0 and E gets F0's first point (g = 0) prepended;
  * levels: np.linspace(c0, min(nanmax c_F0, nanmax c_E), 201) with c0 = F0's first caution, rebuilt per weight vector
    (numpy's formula i * step + start, last level = stop);
  * frontier (optA_lib_v02.frontier): lowest w among points with finite (c, w) and c <= level; NaN if none. Computed here by
    bucketing each point at the first level >= c and a running minimum (same set, same minimum value, no arithmetic);
  * D(A) = np.sum(F_F0 - F_A) over the 201 levels and denE = np.sum(F_F0 - F_E), summed by numpy on each row.
The identity with the library of record is checked by test_gl_fast_v13.py (old evaluation runs, full sample and resamples).
"""
import numpy as np
import numba as nb

NLEV = 201


class Prepared:
    """Sources (names[0] = 'F0', names[1] = 'E') of a9_common_v01.Gridless objects, one population."""

    def __init__(self, G, names, pop):
        assert names[0] == 'F0' and names[1] == 'E'
        self.names = list(names); self.pop = pop
        self.T0 = [np.ascontiguousarray(G[a].T0[:, pop, :]) for a in names]                  # (nrun, NST) each
        d = [np.ascontiguousarray(G[a].d[:, pop, :]) if G[a].b.size else np.zeros((0, G[a].T0.shape[2])) for a in names]
        self.d = np.ascontiguousarray(np.concatenate(d, axis=0))
        self.ri = np.concatenate([G[a].ri.astype(np.int64) if G[a].b.size else np.zeros(0, np.int64) for a in names])
        self.keep = np.concatenate([G[a].keep.astype(np.int64) if G[a].b.size else np.zeros(0, np.int64) for a in names])
        self.ev_off = np.cumsum([0] + [x.shape[0] for x in d]).astype(np.int64)
        self.keep_off = np.cumsum([0] + [(G[a].keep.size if G[a].b.size else 0) for a in names]).astype(np.int64)
        self.nrun = self.T0[0].shape[0]


@nb.njit(cache=False, inline='always')
def _bucket(lev, c, c0, step, nlev):
    """First index k with lev[k] >= c (np.searchsorted(lev, c, side='left')): an arithmetic first guess, then exact moves."""
    if not (c <= lev[nlev - 1]):
        return nlev
    if step > 0.:
        g = (c - c0) / step
        k = int(g) if g > 0. else 0
        if k > nlev - 1: k = nlev - 1
    else:
        k = 0
    while k < nlev and lev[k] < c: k += 1
    while k > 0 and lev[k - 1] >= c: k -= 1
    return k


@nb.njit(cache=False, inline='always')
def _push(bucket, lev, c, w, c0, step, nlev):
    if np.isfinite(c) and np.isfinite(w):
        k = _bucket(lev, c, c0, step, nlev)
        if k < nlev and w < bucket[k]: bucket[k] = w


@nb.njit(cache=False, parallel=True)
def _frontiers(T0b, d, ri, keep, ev_off, keep_off, W, nlev):
    """T0b (B, S, NST); W (B, nrun). Returns F (B, S, nlev) and lev (B, nlev). Columns 0-3 of the statistics are used
    (decisions, wrong go, caution sum, caution count); the rates are formed exactly as optA_lib_v02.rates."""
    B, S, NST = T0b.shape
    F = np.full((B, S, nlev), np.nan); LEV = np.empty((B, nlev))
    for b in nb.prange(B):
        w = W[b]
        nkF = keep_off[1] - keep_off[0]; nkE = keep_off[2] - keep_off[1]
        cF = np.empty(nkF + 1); wF = np.empty(nkF + 1); cE = np.empty(nkE + 1); wE = np.empty(nkE + 1)
        for s in range(2):
            T00 = T0b[b, s, 0]; T01 = T0b[b, s, 1]; T02 = T0b[b, s, 2]; T03 = T0b[b, s, 3]
            if s == 0:
                cF[0] = 100. * T02 / T03; wF[0] = 100. * T01 / T00
            else:
                cE[0] = 100. * T02 / T03; wE[0] = 100. * T01 / T00
            r0 = 0.; r1 = 0.; r2 = 0.; r3 = 0.
            kk = keep_off[s]; nk = keep_off[s + 1] - keep_off[s]; j = 0; e0 = ev_off[s]
            for i in range(ev_off[s + 1] - e0):
                wi = w[ri[e0 + i]]
                r0 = r0 + d[e0 + i, 0] * wi; r1 = r1 + d[e0 + i, 1] * wi; r2 = r2 + d[e0 + i, 2] * wi; r3 = r3 + d[e0 + i, 3] * wi
                while j < nk and keep[kk + j] == i:
                    cc = 100. * (r2 + T02) / (r3 + T03); ww = 100. * (r1 + T01) / (r0 + T00)
                    if s == 0:
                        cF[j + 1] = cc; wF[j + 1] = ww
                    else:
                        cE[j + 1] = cc; wE[j + 1] = ww
                    j += 1
        c0 = cF[0]
        mF = -np.inf; anyF = False
        for x in cF:
            if not np.isnan(x):
                anyF = True
                if x > mF: mF = x
        mE = -np.inf; anyE = False
        for x in cE:
            if not np.isnan(x):
                anyE = True
                if x > mE: mE = x
        C = min(mF, mE) if (anyF and anyE) else np.nan
        step = (C - c0) / (nlev - 1)
        lev = LEV[b]
        for k in range(nlev):
            lev[k] = k * step + c0
        lev[nlev - 1] = C
        for s in range(S):
            bucket = np.full(nlev, np.inf)
            if s < 2:
                if s == 0:
                    for t in range(cF.shape[0]): _push(bucket, lev, cF[t], wF[t], c0, step, nlev)
                else:
                    for t in range(cE.shape[0]): _push(bucket, lev, cE[t], wE[t], c0, step, nlev)
            else:
                _push(bucket, lev, cF[0], wF[0], c0, step, nlev)                 # F0's first point prepended (curves_w)
                T00 = T0b[b, s, 0]; T01 = T0b[b, s, 1]; T02 = T0b[b, s, 2]; T03 = T0b[b, s, 3]
                _push(bucket, lev, 100. * T02 / T03, 100. * T01 / T00, c0, step, nlev)
                r0 = 0.; r1 = 0.; r2 = 0.; r3 = 0.
                kk = keep_off[s]; nk = keep_off[s + 1] - keep_off[s]; j = 0; e0 = ev_off[s]
                for i in range(ev_off[s + 1] - e0):
                    wi = w[ri[e0 + i]]
                    r0 = r0 + d[e0 + i, 0] * wi; r1 = r1 + d[e0 + i, 1] * wi; r2 = r2 + d[e0 + i, 2] * wi; r3 = r3 + d[e0 + i, 3] * wi
                    while j < nk and keep[kk + j] == i:
                        _push(bucket, lev, 100. * (r2 + T02) / (r3 + T03), 100. * (r1 + T01) / (r0 + T00), c0, step, nlev)
                        j += 1
            m = np.inf
            for k in range(nlev):
                if bucket[k] < m: m = bucket[k]
                F[b, s, k] = m if m < np.inf else np.nan
    return F, LEV


def evaluate(prep, W):
    """W (B, nrun) run weights (bootstrap counts). Returns dict(denE (B,), D {name: (B,)}, n (B,), F (B, S, 201))."""
    W = np.ascontiguousarray(np.asarray(W, float).reshape(-1, prep.nrun))
    B = W.shape[0]; S = len(prep.names)
    T0b = np.empty((B, S, prep.T0[0].shape[1]))
    for b in range(B):
        for s in range(S):
            T0b[b, s] = np.tensordot(W[b], prep.T0[s], axes=(0, 0))
    F, LEV = _frontiers(T0b, prep.d, prep.ri, prep.keep, prep.ev_off, prep.keep_off, W, NLEV)
    out = dict(n=T0b[:, 0, 0].copy(), F=F, lev=LEV, D={})
    out['denE'] = np.array([np.sum(F[b, 0] - F[b, 1]) for b in range(B)])
    for s, a in enumerate(prep.names):
        if s >= 2:
            out['D'][a] = np.array([np.sum(F[b, 0] - F[b, s]) for b in range(B)])
    return out
