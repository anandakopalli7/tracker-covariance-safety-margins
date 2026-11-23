"""Package F (revision v13): compiled evaluation of gridless step-frontier sums for many bootstrap weight vectors at once.
New file, 19 Nov 2026 (Claude Opus 5.5). Runs in work\\F_nuscenes\\venv (numba). Same arithmetic as optA_lib_v02.eval_scoring
on a9_common_v01.Gridless curves (the reference path, trk_score_v01.rr_gl), with the step frontier found by exact binary
search of each point's caution among the 201 levels instead of by sorting; f06_score_v01 checks it against the reference.

Inputs for S sources (index 0 = the F0 role, 1 = the E role, 2.. = the others, which get F0's g = 0 point in front):
  T0 (S, nrun, 4) initial tables of one population (columns: decisions, wrong go, caution sum, caution count);
  d (sum nev, 4), ri (sum nev,), last (sum nev,) bool (the last event of its breakpoint), ev0 (S + 1,) offsets into d.
Output (B, S): column 0 = n (decisions), column 1 = denE = sum over levels (F0 - E), column s >= 2 = D_s = sum (F0 - s).
"""
import numpy as np
from numba import njit, prange

NLEV = 201


@njit(cache=False, error_model='numpy')
def _points(T0w, d, ri, last, a, b, w):
    npt = 1
    for e in range(a, b):
        if last[e]:
            npt += 1
    c = np.empty(npt); wg = np.empty(npt)
    c[0] = 100. * T0w[2] / T0w[3]; wg[0] = 100. * T0w[1] / T0w[0]
    s0 = 0.; s1 = 0.; s2 = 0.; s3 = 0.
    k = 1
    for e in range(a, b):
        x = w[ri[e]]
        s0 += d[e, 0] * x; s1 += d[e, 1] * x; s2 += d[e, 2] * x; s3 += d[e, 3] * x
        if last[e]:
            t0 = s0 + T0w[0]; t1 = s1 + T0w[1]; t2 = s2 + T0w[2]; t3 = s3 + T0w[3]
            c[k] = 100. * t2 / t3; wg[k] = 100. * t1 / t0
            k += 1
    return c, wg


@njit(cache=False, error_model='numpy')
def _bin(lev, cval):
    """Smallest i with lev[i] >= cval (searchsorted left); NLEV if none."""
    lo = 0; hi = NLEV
    while lo < hi:
        mid = (lo + hi) // 2
        if lev[mid] >= cval:
            hi = mid
        else:
            lo = mid + 1
    return lo


@njit(cache=False, error_model='numpy')
def _frontier(lev, c, wg, prepend, c0, w0):
    binmin = np.full(NLEV + 1, np.inf)
    if prepend:
        if np.isfinite(c0) and np.isfinite(w0):
            i = _bin(lev, c0)
            if w0 < binmin[i]:
                binmin[i] = w0
    for p in range(c.size):
        if np.isfinite(c[p]) and np.isfinite(wg[p]):
            i = _bin(lev, c[p])
            if wg[p] < binmin[i]:
                binmin[i] = wg[p]
    f = np.empty(NLEV)
    m = np.inf
    for k in range(NLEV):
        if binmin[k] < m:
            m = binmin[k]
        f[k] = m if np.isfinite(m) else np.nan
    return f


@njit(parallel=True, cache=False, error_model='numpy')
def eval_many(W, T0, d, ri, last, ev0):
    B = W.shape[0]; S = T0.shape[0]; nrun = W.shape[1]
    out = np.full((B, S), np.nan)
    for bb in prange(B):
        w = W[bb]
        T0w = np.zeros((S, 4))
        for s in range(S):
            for r in range(nrun):
                for j in range(4):
                    T0w[s, j] += w[r] * T0[s, r, j]
        cF, wF = _points(T0w[0], d, ri, last, ev0[0], ev0[1], w)
        cE, wE = _points(T0w[1], d, ri, last, ev0[1], ev0[2], w)
        c0 = cF[0]; w0 = wF[0]
        mF = -np.inf
        for x in cF:
            if not np.isnan(x) and x > mF:
                mF = x
        mE = -np.inf
        for x in cE:
            if not np.isnan(x) and x > mE:
                mE = x
        C = min(mF, mE)
        lev = np.empty(NLEV)
        step = (C - c0) / (NLEV - 1)
        for k in range(NLEV):
            lev[k] = k * step + c0
        lev[NLEV - 1] = C
        fF = _frontier(lev, cF, wF, False, c0, w0)
        fE = _frontier(lev, cE, wE, False, c0, w0)
        out[bb, 0] = T0w[0, 0]
        acc = 0.
        for k in range(NLEV):
            acc += fF[k] - fE[k]
        out[bb, 1] = acc
        for s in range(2, S):
            cs, ws = _points(T0w[s], d, ri, last, ev0[s], ev0[s + 1], w)
            fs = _frontier(lev, cs, ws, True, c0, w0)
            acc = 0.
            for k in range(NLEV):
                acc += fF[k] - fs[k]
            out[bb, s] = acc
    return out


def pack(Gs, pop):
    """Gs: list of a9 Gridless objects in role order (F0, E, others). Returns the kernel's input arrays."""
    T0 = np.stack([g.T0[:, pop, :4] for g in Gs])
    ds = []; ris = []; lasts = []; ev0 = [0]
    for g in Gs:
        if g.b.size:
            ds.append(g.d[:, pop, :4]); ris.append(g.ri.astype(np.int64))
            lst = np.concatenate([g.b[1:] != g.b[:-1], [True]])
            lasts.append(lst)
            ev0.append(ev0[-1] + g.b.size)
        else:
            ev0.append(ev0[-1])
    d = np.concatenate(ds) if ds else np.zeros((0, 4))
    ri = np.concatenate(ris) if ris else np.zeros(0, np.int64)
    last = np.concatenate(lasts) if lasts else np.zeros(0, bool)
    return np.ascontiguousarray(T0), np.ascontiguousarray(d), ri, last, np.array(ev0, np.int64)
