"""Recount (second program) of package C, revision v13: the part of the recount that the double bootstrap needs, as a
PURE module (numpy and numba only; no project path, no file of the project tree, no Windows call). New file, 20 Nov 2026
(Claude Fable 5.2).

Why it exists: the A10 section 2.6 double bootstrap has to run in chunks on other machines (rc_calib_remote_v13.py), where
rc_core_v13 cannot be imported (it imports the scoring library and other modules by absolute Windows paths). The numba kernel,
Problem, ratio_arr and counts_of were MOVED here from rc_core_v13.py and _h4_kernel and the H4 evaluation from rc_c_lead_v13.py,
text unchanged; rc_core_v13 and rc_c_lead_v13 import them from here, so the in-process path and the remote path run one and the
same code. Nothing of work\\CD_capture\\analysis or work\\CD_capture\\tools was read.

Contents
  * kernel:    _nanmax ... _kernel, Problem (moved from rc_core_v13, unchanged); Problem.to_arrays / from_arrays (new).
  * H4:        _h4_kernel, H4Eval (frontiers, evaluate; moved from rc_c_lead_v13.H4, unchanged); to_arrays / from_arrays (new).
  * statistic: LeadStat, CutinStat -- the stat_fn of rc_c_lead_v13 / rc_c_cutin_v13 as objects that can be written to and read
               from a job file.
  * job:       save_job, load_job, sha256_file; calib_rows (rows LO..HI-1 of the double bootstrap of one inner seed).
"""
import hashlib
import numpy as np
import numba
from numba import njit, prange

NLEV = 201


# ------------------------------------------------------------------------------------------------ numba kernel
@njit(error_model='numpy', cache=True)
def _nanmax(c, n):
    m = np.nan
    for i in range(n):
        v = c[i]
        if not np.isnan(v):
            if np.isnan(m) or v > m:
                m = v
    return m


@njit(error_model='numpy', cache=True)
def _levels(c0, C, lev):
    """numpy.linspace(c0, C, 201), the same arithmetic (y = arange * step + start; last = stop)."""
    delta = C - c0
    step = delta / 200.
    if step == 0.:
        for i in range(201):
            lev[i] = (i / 200.) * delta + c0
    else:
        for i in range(201):
            lev[i] = i * step + c0
    lev[200] = C


@njit(error_model='numpy', cache=True)
def _sort_levels(lev, sl, sidx):
    """Finite levels in ascending order (values sl, original positions sidx); returns their number."""
    m = 0
    for i in range(201):
        v = lev[i]
        if np.isfinite(v):
            j = m
            while j > 0 and sl[j - 1] > v:
                sl[j] = sl[j - 1]; sidx[j] = sidx[j - 1]
                j -= 1
            sl[j] = v; sidx[j] = i
            m += 1
    return m


@njit(error_model='numpy', cache=True)
def _frontier(c, w, npt, lev, sl, sidx, m, bm, out):
    """optA_lib_v02.frontier: per level the lowest w among finite points with c <= level; NaN where none; a NaN level takes the
    lowest w of all finite points (numpy.searchsorted places NaN after every value)."""
    gmin = np.inf; nok = 0
    for p in range(m):
        bm[p] = np.inf
    hint = 0
    for i in range(npt):
        ci = c[i]; wi = w[i]
        if not (np.isfinite(ci) and np.isfinite(wi)):
            continue
        nok += 1
        if wi < gmin:
            gmin = wi
        if m == 0 or ci > sl[m - 1]:
            continue
        # first position p with ci <= sl[p]
        if ci <= sl[hint] and (hint == 0 or sl[hint - 1] < ci):
            p = hint
        else:
            lo = 0; hi = m - 1
            while lo < hi:
                mid = (lo + hi) >> 1
                if ci <= sl[mid]:
                    hi = mid
                else:
                    lo = mid + 1
            p = lo; hint = p
        if wi < bm[p]:
            bm[p] = wi
    if nok == 0:
        for i in range(201):
            out[i] = np.nan
        return
    for i in range(201):
        if np.isnan(lev[i]):
            out[i] = gmin
        elif not np.isfinite(lev[i]):
            out[i] = gmin if lev[i] > 0 else np.nan
    run = np.inf
    for p in range(m):
        if bm[p] < run:
            run = bm[p]
        out[sidx[p]] = run if run < np.inf else np.nan


@njit(error_model='numpy', cache=True)
def _gen_store(wrow, T0s, lo, hi, ev_ri, ev_d, ev_last, c, t):
    """Points of one curve: c = caution (exact expression of optA_lib_v02.rates), t = wrong-go count; returns their number."""
    t[0] = T0s[1]
    c[0] = 100. * T0s[2] / T0s[3]
    npt = 1
    a1 = 0.; a2 = 0.; a3 = 0.
    for e in range(lo, hi):
        wr = wrow[ev_ri[e]]
        a1 += ev_d[e, 0] * wr; a2 += ev_d[e, 1] * wr; a3 += ev_d[e, 2] * wr
        if ev_last[e]:
            t[npt] = a1 + T0s[1]
            c[npt] = 100. * (a2 + T0s[2]) / (a3 + T0s[3])
            npt += 1
    return npt


@njit(error_model='numpy', cache=True)
def _finish(n0, gmin, lev, sidx, m, bm, out):
    if gmin == np.inf:                              # no finite point
        for i in range(201):
            out[i] = np.nan
        return
    for i in range(201):
        if np.isnan(lev[i]):
            out[i] = 100. * gmin / n0
        elif not np.isfinite(lev[i]):
            out[i] = 100. * gmin / n0 if lev[i] > 0 else np.nan
    run = np.inf
    for p in range(m):
        if bm[p] < run:
            run = bm[p]
        out[sidx[p]] = 100. * run / n0 if run < np.inf else np.nan


@njit(error_model='numpy', cache=True)
def _front_stored(c, t, npt, n0, lev, sl, sidx, m, bm, out):
    """Step frontier of stored points (c, wrong-go count t): per level the lowest w = 100 t / n0 among finite points with
    c <= level. The minimum over w is taken as 100 (min t) / n0 (the map t -> 100 t / n0 is monotone)."""
    if not (n0 > 0.):
        for i in range(201):
            out[i] = np.nan
        return
    gmin = np.inf
    for p in range(m + 1):
        bm[p] = np.inf
    h = 0
    for i in range(npt):
        ci = c[i]
        if not np.isfinite(ci):
            continue
        ti = t[i]
        if ti < gmin:
            gmin = ti
        if (h == 0 or ci > sl[h - 1]) and (h == m or ci <= sl[h]):
            p = h
        else:
            lo = 0; hi = m
            while lo < hi:
                mid = (lo + hi) >> 1
                if ci <= sl[mid]:
                    hi = mid
                else:
                    lo = mid + 1
            p = lo; h = p
        if ti < bm[p]:
            bm[p] = ti
    _finish(n0, gmin, lev, sidx, m, bm, out)


@njit(error_model='numpy', cache=True)
def _pt(T1, T2, T3, sl, m, bm, h, gmin):
    """One point (wrong-go count T1, caution sum T2, caution count T3) of a streamed curve. Its caution c = (100 T2) / T3 is
    compared with the levels without the division where the outcome is certain (products with a 1e-12 relative guard band, far
    above the rounding of one product); otherwise the exact c is formed. Returns the updated (hint bucket, lowest T1 so far)."""
    if not (T3 > 0.):
        return h, gmin                              # c is NaN or infinite: not a finite point
    x = 100. * T2
    if T1 < gmin:
        gmin = T1
    lower = h == 0
    if not lower:
        y = sl[h - 1] * T3
        lower = x >= y + (1e-12 * (abs(x) + abs(y)) + 1e-300)
    if lower:
        if h == m or T1 >= bm[h]:
            return h, gmin                          # beyond the last level, or cannot lower any frontier value
        y = sl[h] * T3
        if x <= y - (1e-12 * (abs(x) + abs(y)) + 1e-300):
            bm[h] = T1
            return h, gmin
    c = x / T3
    lo = 0; hi = m
    while lo < hi:
        mid = (lo + hi) >> 1
        if c <= sl[mid]:
            hi = mid
        else:
            lo = mid + 1
    if lo < m and T1 < bm[lo]:
        bm[lo] = T1
    return lo, gmin


@njit(error_model='numpy', cache=True)
def _front_stream(wrow, T0s, lo, hi, ev_ri, ev_d, ev_last, pre, c0, t0, n0, lev, sl, sidx, m, bm, out):
    """Step frontier of one source generated on the fly (no storage); pre = 1: the point (c0, t0) of F0 at g = 0 comes first."""
    if not (n0 > 0.):
        for i in range(201):
            out[i] = np.nan
        return
    gmin = np.inf
    for p in range(m + 1):
        bm[p] = np.inf
    h = 0
    if pre and np.isfinite(c0):
        gmin = t0
        l2 = 0; h2 = m
        while l2 < h2:
            mid = (l2 + h2) >> 1
            if c0 <= sl[mid]:
                h2 = mid
            else:
                l2 = mid + 1
        h = l2
        if h < m:
            bm[h] = t0
    h, gmin = _pt(T0s[1], T0s[2], T0s[3], sl, m, bm, h, gmin)
    a1 = 0.; a2 = 0.; a3 = 0.
    for e in range(lo, hi):
        wr = wrow[ev_ri[e]]
        a1 += ev_d[e, 0] * wr; a2 += ev_d[e, 1] * wr; a3 += ev_d[e, 2] * wr
        if ev_last[e]:
            h, gmin = _pt(a1 + T0s[1], a2 + T0s[2], a3 + T0s[3], sl, m, bm, h, gmin)
    _finish(n0, gmin, lev, sidx, m, bm, out)


@njit(parallel=True, error_model='numpy', cache=True)
def _kernel(W, T0, off, ev_ri, ev_d, ev_last, prep, maxpts01, nchunk, F, NN, ERR):
    """W (B, nrun) run weights; T0 (B, nsrc, 5); source 0 = F0, 1 = E; prep[s] = 1: F0's g = 0 point is put in front.
    F (B, nsrc, 201) frontiers on the resample's own 201 levels; NN (B,) decisions; ERR (B,) = 1 if the sources of a resample
    do not have the same number of decisions (must not happen)."""
    B = W.shape[0]; nsrc = off.shape[0] - 1
    for ch in prange(nchunk):
        b_lo = (ch * B) // nchunk; b_hi = ((ch + 1) * B) // nchunk
        c0b = np.empty(maxpts01); t0b = np.empty(maxpts01)
        c1b = np.empty(maxpts01); t1b = np.empty(maxpts01)
        lev = np.empty(201); sl = np.empty(202); sidx = np.empty(202, np.int64); bm = np.empty(202)
        for b in range(b_lo, b_hi):
            wrow = W[b]
            n0 = T0[b, 0, 0]
            NN[b] = n0; ERR[b] = 0
            np0 = _gen_store(wrow, T0[b, 0], off[0], off[1], ev_ri, ev_d, ev_last, c0b, t0b)
            np1 = _gen_store(wrow, T0[b, 1], off[1], off[2], ev_ri, ev_d, ev_last, c1b, t1b)
            if T0[b, 1, 0] != n0:
                ERR[b] = 1
            c0 = c0b[0]; t0 = t0b[0]
            CF = _nanmax(c0b, np0); CE = _nanmax(c1b, np1)
            C = CE if CE < CF else CF                  # Python's min(nanmax(cF0), nanmax(cE))
            _levels(c0, C, lev)
            m = _sort_levels(lev, sl, sidx)
            _front_stored(c0b, t0b, np0, n0, lev, sl, sidx, m, bm, F[b, 0])
            _front_stored(c1b, t1b, np1, n0, lev, sl, sidx, m, bm, F[b, 1])
            for s in range(2, nsrc):
                if T0[b, s, 0] != n0:
                    ERR[b] = 1
                _front_stream(wrow, T0[b, s], off[s], off[s + 1], ev_ri, ev_d, ev_last, prep[s], c0, t0, n0,
                              lev, sl, sidx, m, bm, F[b, s])


class Problem:
    """Curves with roles: names[0] plays F0, names[1] plays E (no point put in front); every other name gets F0's g = 0 point
    in front (optA_lib_v02.curves_w). evaluate(W) -> dict(n (B,), denE (B,), D {name: (B,)}) for run weights W (B, nrun):
    denE = sum over the 201 levels of (F_F0 - F_E), D[a] = sum of (F_F0 - F_a)."""

    def __init__(self, names, curves):
        self.names = list(names)
        self.curves = list(curves)
        self.nrun = self.curves[0].T0.shape[0]
        sizes = [c.ri.size for c in self.curves]
        self.off = np.concatenate([[0], np.cumsum(sizes)]).astype(np.int64)
        ne = int(self.off[-1])
        self.ev_ri = np.zeros(max(ne, 1), np.int32); self.ev_d = np.zeros((max(ne, 1), 3)); self.ev_last = np.zeros(max(ne, 1), np.uint8)
        for s, c in enumerate(self.curves):
            self.ev_ri[self.off[s]:self.off[s + 1]] = c.ri
            self.ev_d[self.off[s]:self.off[s + 1]] = c.d
            self.ev_last[self.off[s]:self.off[s + 1]] = c.last
        self.prep = np.array([0, 0] + [1] * (len(self.names) - 2), np.uint8)
        self.maxpts = int(max(self.curves[0].npts, self.curves[1].npts)) + 2
        # the exact tensors a9_common_v01.Gridless.curve multiplies: (nrun, 1, 5)
        self.T0a = [np.ascontiguousarray(c.T0[:, None, :]) for c in self.curves]

    def t0(self, W):
        B = W.shape[0]
        T0 = np.empty((B, len(self.curves), 5))
        for s, Ta in enumerate(self.T0a):
            for b in range(B):
                T0[b, s] = np.tensordot(W[b], Ta, axes=(0, 0))[0]
        return T0

    def frontiers(self, W):
        W = np.ascontiguousarray(W, float)
        if W.ndim == 1:
            W = W[None]
        B = W.shape[0]
        F = np.empty((B, len(self.curves), NLEV)); NN = np.empty(B); ERR = np.zeros(B, np.uint8)
        nchunk = int(max(1, min(B, 4 * numba.get_num_threads())))
        _kernel(W, self.t0(W), self.off, self.ev_ri, self.ev_d, self.ev_last, self.prep, self.maxpts, nchunk, F, NN, ERR)
        if ERR.any():
            raise RuntimeError('the sources of a problem do not share the number of decisions')
        return F, NN

    def evaluate(self, W, chunk=500):
        W = np.ascontiguousarray(W, float)
        if W.ndim == 1:
            W = W[None]
        B = W.shape[0]
        out = dict(n=np.empty(B), denE=np.empty(B), D={a: np.empty(B) for a in self.names[2:]})
        for s0 in range(0, B, chunk):
            F, NN = self.frontiers(W[s0:s0 + chunk])
            sl = slice(s0, s0 + F.shape[0])
            out['n'][sl] = NN
            out['denE'][sl] = np.sum(F[:, 0, :] - F[:, 1, :], axis=1)
            for s, a in enumerate(self.names):
                if s >= 2:
                    out['D'][a][sl] = np.sum(F[:, 0, :] - F[:, s, :], axis=1)
        return out


def ratio_arr(D, den):
    """D / den where den is finite and > 0, else NaN."""
    D = np.asarray(D, float); den = np.asarray(den, float)
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(np.isfinite(den) & (den > 0), D / den, np.nan)


def counts_of(idx, n):
    B = idx.shape[0]
    flat = (idx + (np.arange(B) * n)[:, None]).ravel()
    return np.bincount(flat, minlength=B * n).reshape(B, n).astype(float)


# ------------------------------------------------------------------------------------------------ Problem <-> arrays
_P_KEYS = ('off', 'ev_ri', 'ev_d', 'ev_last', 'prep')


def problem_to_arrays(P, prefix):
    """Everything Problem.evaluate uses, as plain arrays (names as a unicode array; T0 stacked (nsrc, nrun, 1, 5))."""
    d = {prefix + k: getattr(P, k) for k in _P_KEYS}
    d[prefix + 'names'] = np.array(P.names, dtype=np.str_)
    d[prefix + 'maxpts'] = np.int64(P.maxpts)
    d[prefix + 'T0a'] = np.stack(P.T0a)
    return d


def problem_from_arrays(z, prefix):
    P = Problem.__new__(Problem)
    P.names = [str(x) for x in z[prefix + 'names']]
    P.curves = [None] * len(P.names)                     # only its length is used by t0 / frontiers
    P.off = np.ascontiguousarray(z[prefix + 'off'], np.int64)
    P.ev_ri = np.ascontiguousarray(z[prefix + 'ev_ri'], np.int32)
    P.ev_d = np.ascontiguousarray(z[prefix + 'ev_d'], float)
    P.ev_last = np.ascontiguousarray(z[prefix + 'ev_last'], np.uint8)
    P.prep = np.ascontiguousarray(z[prefix + 'prep'], np.uint8)
    P.maxpts = int(z[prefix + 'maxpts'])
    T0a = np.asarray(z[prefix + 'T0a'], float)
    P.T0a = [np.ascontiguousarray(T0a[s]) for s in range(T0a.shape[0])]
    P.nrun = P.T0a[0].shape[0]
    return P


# ------------------------------------------------------------------------------------------------ H4 (grid), evaluation part
@njit(parallel=True, error_model='numpy', cache=True)
def _h4_kernel(NN, TF, TE, T1, v1, TP, vp, F):
    """Pooled sums of B resamples -> frontiers on each resample's own 201 levels.
    NN (B,); TF, TE (B, G, 3) = (wrong go, caution sum, caution count) of F0 / E on the grid; T1 (B, 201, 3) the transferred single
    scale; TP (B, nvar, 201, 3) the transferred triples; v1 (201,), vp (nvar, 201): the level has a choice.
    F (B, 3 + nvar, 201): F_F0, F_E, F_1, F_ps per variant."""
    B = NN.shape[0]; G = TF.shape[1]; nvar = TP.shape[1]
    for b in prange(B):
        c = np.empty(G + 202); w = np.empty(G + 202)
        lev = np.empty(201); sl = np.empty(201); sidx = np.empty(201, np.int64); bm = np.empty(201)
        n = NN[b]
        for g in range(G):
            w[g] = 100. * TF[b, g, 0] / n; c[g] = 100. * TF[b, g, 1] / TF[b, g, 2]
        c0 = c[0]; w0 = w[0]
        CF = _nanmax(c, G)
        ce = np.empty(G); we = np.empty(G)
        for g in range(G):
            we[g] = 100. * TE[b, g, 0] / n; ce[g] = 100. * TE[b, g, 1] / TE[b, g, 2]
        CE = _nanmax(ce, G)
        C = CE if CE < CF else CF
        _levels(c0, C, lev)
        m = _sort_levels(lev, sl, sidx)
        _frontier(c, w, G, lev, sl, sidx, m, bm, F[b, 0])
        _frontier(ce, we, G, lev, sl, sidx, m, bm, F[b, 1])
        npt = 1
        c[0] = c0; w[0] = w0
        for l in range(201):
            if v1[l]:
                w[npt] = 100. * T1[b, l, 0] / n; c[npt] = 100. * T1[b, l, 1] / T1[b, l, 2]; npt += 1
        _frontier(c, w, npt, lev, sl, sidx, m, bm, F[b, 2])
        for v in range(nvar):
            npt = 1
            for l in range(201):
                if vp[v, l]:
                    w[npt] = 100. * TP[b, v, l, 0] / n; c[npt] = 100. * TP[b, v, l, 1] / TP[b, v, l, 2]; npt += 1
            _frontier(c, w, npt, lev, sl, sidx, m, bm, F[b, 3 + v])


_H4_KEYS = ('NEV', 'GF', 'GE', 'ONE', 'PS', 'v1', 'vp')


class H4Eval:
    """The evaluation part of rc_c_lead_v13.H4: per-run grid tables (NEV, GF, GE), the transferred single scale (ONE, v1) and
    triples (PS, vp) -> per variant the record-basis and like-for-like shares of a batch of run counts. rc_c_lead_v13.H4
    derives from it and fills the arrays; from_arrays rebuilds it from a job file."""

    def frontiers(self, CN):
        CN = np.ascontiguousarray(CN, float)
        B = CN.shape[0]
        nv = self.PS.shape[1]
        NN = CN @ self.NEV
        TF = (CN @ self.GF.reshape(self.nrun, -1)).reshape(B, self.G, 3)
        TE = (CN @ self.GE.reshape(self.nrun, -1)).reshape(B, self.G, 3)
        T1 = (CN @ self.ONE.reshape(self.nrun, -1)).reshape(B, 201, 3)
        TP = (CN @ self.PS.reshape(self.nrun, -1)).reshape(B, nv, 201, 3)
        F = np.empty((B, 3 + nv, 201))
        _h4_kernel(NN, TF, TE, T1, self.v1, TP, self.vp, F)
        return F, NN

    def evaluate(self, CN, chunk=1000):
        """-> dict(den (B,), rec (B, nvar), lfl (B, nvar), gain_single (B,))."""
        CN = np.ascontiguousarray(CN, float)
        if CN.ndim == 1:
            CN = CN[None]
        B = CN.shape[0]; nv = self.PS.shape[1]
        out = dict(den=np.empty(B), n=np.empty(B), D_ps=np.empty((B, nv)), D_1=np.empty(B))
        for s0 in range(0, B, chunk):
            F, NN = self.frontiers(CN[s0:s0 + chunk])
            sl = slice(s0, s0 + F.shape[0])
            out['n'][sl] = NN
            out['den'][sl] = np.sum(F[:, 0] - F[:, 1], axis=1)
            out['D_1'][sl] = np.sum(F[:, 0] - F[:, 2], axis=1)
            for v in range(nv):
                out['D_ps'][sl, v] = np.sum(F[:, 0] - F[:, 3 + v], axis=1)
        out['rec'] = ratio_arr(out['D_ps'], out['den'][:, None])
        out['lfl'] = ratio_arr(out['D_ps'] - out['D_1'][:, None], out['den'][:, None])
        return out

    def to_arrays(self, prefix):
        d = {prefix + k: getattr(self, k) for k in _H4_KEYS}
        d[prefix + 'names'] = np.array(self.names, dtype=np.str_)
        return d

    @classmethod
    def from_arrays(cls, z, prefix):
        h = cls.__new__(cls)
        h.names = [str(x) for x in z[prefix + 'names']]
        h.NEV = np.ascontiguousarray(z[prefix + 'NEV'], float)
        for k in ('GF', 'GE', 'ONE', 'PS'):
            setattr(h, k, np.ascontiguousarray(z[prefix + k], float))
        h.v1 = np.ascontiguousarray(z[prefix + 'v1'], np.uint8)
        h.vp = np.ascontiguousarray(z[prefix + 'vp'], np.uint8)
        h.nrun = h.GF.shape[0]; h.G = h.GF.shape[1]
        return h


# ------------------------------------------------------------------------------------------------ the statistic groups
class LeadStat:
    """stat_fn of rc_c_lead_v13: run counts CN (B, nrun) -> (B, len(STATS)). PA: Problem(F0, E, N, E5, E5p, CK3) on the online
    tracker; PI: Problem(F0, E, N, E5x) on the IMM arrays or None; hx: H4Eval."""
    kind = 'lead'

    def __init__(self, PA, PI, hx, STATS):
        self.PA = PA; self.PI = PI; self.hx = hx
        self.STATS = list(STATS)
        self.SI = {s: i for i, s in enumerate(self.STATS)}

    def __call__(self, CN, keep=None):
        PA = self.PA; PI = self.PI; hx = self.hx; SI = self.SI
        CN = np.ascontiguousarray(CN, float)
        if CN.ndim == 1:
            CN = CN[None]
        S = np.full((CN.shape[0], len(self.STATS)), np.nan)
        e = PA.evaluate(CN)
        den = e['denE']
        S[:, SI['R_gl_pp']] = den / NLEV
        rr = {x: ratio_arr(e['D'][x], den) for x in ('N', 'E5', 'E5p', 'CK3')}
        S[:, SI['RR_E5']] = rr['E5']; S[:, SI['RR_E5_minus_E5p']] = rr['E5'] - rr['E5p']; S[:, SI['RR_N']] = rr['N']
        S[:, SI['RR_CK3']] = rr['CK3']; S[:, SI['RR_E5p']] = rr['E5p']
        if PI is not None:
            ei = PI.evaluate(CN)
            S[:, SI['IMM_R_gl_pp']] = ei['denE'] / NLEV
            ri = ratio_arr(ei['D']['N'], ei['denE']); ci = ratio_arr(ei['D']['E5x'], ei['denE'])
            S[:, SI['IMM_r']] = ri; S[:, SI['IMM_c']] = ci
            with np.errstate(divide='ignore', invalid='ignore'):
                S[:, SI['IMM_r_over_c']] = np.where(np.isfinite(ci) & (ci != 0), ri / ci, np.nan)
        h = hx.evaluate(CN)
        for vi, nm in enumerate(hx.names):
            S[:, SI['H4_rec_' + nm]] = h['rec'][:, vi]; S[:, SI['H4_lfl_' + nm]] = h['lfl'][:, vi]
        if keep is not None:
            keep.update(e=e, ei=ei if PI is not None else None, h=h)
        return S

    def to_arrays(self):
        d = dict(has_PI=np.int64(self.PI is not None))
        d.update(problem_to_arrays(self.PA, 'PA_'))
        if self.PI is not None:
            d.update(problem_to_arrays(self.PI, 'PI_'))
        d.update(self.hx.to_arrays('H4_'))
        return d

    @classmethod
    def from_arrays(cls, z, STATS):
        PI = problem_from_arrays(z, 'PI_') if int(z['has_PI']) else None
        return cls(problem_from_arrays(z, 'PA_'), PI, H4Eval.from_arrays(z, 'H4_'), STATS)


class CutinStat:
    """stat_fn of rc_c_cutin_v13: PW = Problem of the event window (F0, E, N, O), PY = Problem of the young-track population
    (F0, E, N, O and, when defined, E5N). Columns: W_R_gl_pp, W_RR_N, Y_R_gl_pp, Y_r, Y_c, Y_r_over_c (the last two NaN when
    E5N is not defined)."""
    kind = 'cutin'

    def __init__(self, PW, PY, STATS):
        self.PW = PW; self.PY = PY; self.STATS = list(STATS)

    def __call__(self, CN):
        CN = np.ascontiguousarray(CN, float)
        if CN.ndim == 1:
            CN = CN[None]
        S = np.full((CN.shape[0], len(self.STATS)), np.nan)
        ew = self.PW.evaluate(CN); ey = self.PY.evaluate(CN)
        S[:, 0] = ew['denE'] / NLEV; S[:, 1] = ratio_arr(ew['D']['N'], ew['denE'])
        rn = ratio_arr(ey['D']['N'], ey['denE'])
        S[:, 2] = ey['denE'] / NLEV; S[:, 3] = rn
        if 'E5N' in ey['D']:
            c = ratio_arr(ey['D']['E5N'], ey['denE'])
            S[:, 4] = c
            with np.errstate(divide='ignore', invalid='ignore'):
                S[:, 5] = np.where(np.isfinite(c) & (c != 0), rn / c, np.nan)
        return S

    def to_arrays(self):
        d = problem_to_arrays(self.PW, 'PW_')
        d.update(problem_to_arrays(self.PY, 'PY_'))
        return d

    @classmethod
    def from_arrays(cls, z, STATS):
        return cls(problem_from_arrays(z, 'PW_'), problem_from_arrays(z, 'PY_'), STATS)


STAT_KINDS = {'lead': LeadStat, 'cutin': CutinStat}


# ------------------------------------------------------------------------------------------------ job files
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def job_arrays(stat, full, outer_est, n_run, n_outer, n_inner, seed_outer, b_outer, b_inner, label):
    """The arrays of a job: the statistic's arrays, the full-sample values, the outer estimates (rows 0..n_outer-1 of the full
    outer draw, computed once by the exporting program with the same call as an in-process run) and the sizes and seeds."""
    d = dict(stat.to_arrays())
    d.update(kind=np.array(stat.kind), label=np.array(label), stats=np.array(stat.STATS, dtype=np.str_),
             full=np.asarray(full, float), outer_est=np.asarray(outer_est, float), n_run=np.int64(n_run),
             n_outer=np.int64(n_outer), n_inner=np.int64(n_inner), seed_outer=np.int64(seed_outer),
             b_outer=np.int64(b_outer), b_inner=np.int64(b_inner))
    return d


def save_job(path, arrays):
    """Write the job file once (refuses to overwrite); returns its SHA-256."""
    with open(path, 'xb') as f:
        np.savez_compressed(f, **arrays)
    return sha256_file(path)


def load_job(path):
    """-> (stat_fn, dict of the job's arrays). allow_pickle=False."""
    with np.load(path, allow_pickle=False) as z:
        J = {k: z[k] for k in z.files}
    stats = [str(x) for x in J['stats']]
    stat = STAT_KINDS[str(J['kind'])].from_arrays(J, stats)
    return stat, J


def same_arrays(A, B):
    """Names of the entries that differ between two dicts of arrays (NaN equals NaN); [] when equal."""
    bad = [k for k in sorted(set(A) | set(B)) if k not in A or k not in B]
    for k in sorted(set(A) & set(B)):
        a = np.asarray(A[k]); b = np.asarray(B[k])
        if a.shape != b.shape or a.dtype.kind != b.dtype.kind:
            bad.append(k)
        elif a.dtype.kind in 'US':
            if not np.array_equal(a, b):
                bad.append(k)
        elif not np.array_equal(a, b, equal_nan=(a.dtype.kind == 'f')):
            bad.append(k)
    return bad


CHUNK_KEYS = ('p_lt', 'p_le', 'p_lt_any', 'p_le_any', 'outer_est', 'n_inner_valid')


def calib_rows(stat_fn, J, seed_inner, lo, hi, progress=None):
    """Rows lo..hi-1 of the double bootstrap of one inner seed, exactly as rc_core_v13.DoubleBoot.run fills them:
    the outer draw is default_rng(seed_outer).integers(0, n, (b_outer, n))[:n_outer] (the full draw; its rows lo..hi-1 are used);
    the inner stream default_rng(seed_inner) draws integers(0, n, (b_inner, n)) for EVERY outer sample from 0 on, in order; the
    draws of outer samples 0..lo-1 are generated and discarded, so the stream stands where an unsplit run has it.
    The outer estimates are rows lo..hi-1 of the job's outer_est."""
    n = int(J['n_run']); n_outer = int(J['n_outer']); n_inner = int(J['n_inner'])
    b_outer = int(J['b_outer']); b_inner = int(J['b_inner'])
    full = np.asarray(J['full'], float); ns = full.size
    if not (0 <= lo < hi <= n_outer):
        raise SystemExit('REFUSED: outer range %d:%d is not inside 0:%d' % (lo, hi, n_outer))
    idx_o = np.random.default_rng(int(J['seed_outer'])).integers(0, n, (b_outer, n))[:n_outer]
    rng_i = np.random.default_rng(int(seed_inner))
    m = hi - lo
    R = dict(p_lt=np.full((m, ns), np.nan), p_le=np.full((m, ns), np.nan), p_lt_any=np.full((m, ns), np.nan),
             p_le_any=np.full((m, ns), np.nan), outer_est=np.array(J['outer_est'][lo:hi], float), n_inner_valid=np.zeros((m, ns)))
    for b in range(hi):
        ii = rng_i.integers(0, n, (b_inner, n))[:n_inner]              # always drawn: keeps the stream in order
        if b < lo:
            continue
        S = stat_fn(counts_of(idx_o[b][ii], n))
        r = b - lo
        for j in range(ns):
            v = S[:, j]; v = v[np.isfinite(v)]
            R['n_inner_valid'][r, j] = v.size
            if v.size == 0:
                continue
            lt = (v < full[j]).mean(); le = (v <= full[j]).mean()
            R['p_lt_any'][r, j] = lt; R['p_le_any'][r, j] = le
            if np.isfinite(R['outer_est'][r, j]):
                R['p_lt'][r, j] = lt; R['p_le'][r, j] = le
        if progress is not None:
            progress(b + 1)
    return R
