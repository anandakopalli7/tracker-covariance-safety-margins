"""Package F (nuScenes), independent second program ("recount"), core. New file, 19 Nov 2026.
Writer: Claude Fable 5.2 (claude-fable-5-2), a different model from the first program's (Claude Opus 5.5).
Written from AMENDMENT_10_v13.md (sections 0, 2.2, 2.3, 2.6, 8, 10.1), notes\\ARRAYS_FORMAT_F_v01.md and the definitions of record
(optA_lib_v02.py; revision_v12 a9_common_v01.py as the definition of the gridless step frontier), WITHOUT reading the first
program's code (work\\F_nuscenes\\code, shared\\trackers\\trk_score_v01.py) or its outputs.

Own implementations here: the gridless curve (events of each decision's selection path, numba), the frontier and D on the 201
levels (numba kernel), E5_x (section 2.2), the double-bootstrap calibration (section 2.6).
Shared, as A10 10.1(b) allows: the extracted arrays, the resample draws, and optA_lib_v02 (imported read-only; used for the
reference path of the tests and for the summ / dec_eq conventions).
"""
import json, pathlib, sys
sys.dont_write_bytecode = True
import numpy as np
import numba as nb

LIBDIR = r'<library folder>\code'
if LIBDIR not in sys.path:
    sys.path.insert(0, LIBDIR)
import optA_lib_v02 as L                      # noqa: E402  (scoring library of record, read-only)

HERE = pathlib.Path(__file__).resolve().parent
V13 = HERE.parents[2]                                              # ...\revision_v13
ARR = HERE.parent / 'cache'
LOCK2 = [V13 / 'LOCK_A10_2.txt']                 # the only file that opens the val split (README_COORDINATION rule 3)
NLEV = 201
GMAX = 1e3                       # largest margin scale of the gridless curve (record: a9_common_v01.GMAX)
DELTA = 0.05                     # A10 2.7 / 0.2
SEED_PRIMARY = 20261923; NBOOT = 20000
SEED_E5P = 20261915; SEED_PO = 20261919; E5_M = 1.1029; E5_A = 0.05
SEED_OUTER = 20261912; SEED_INNER = 20261913; SEED_INNER2 = 20261914; SEED_MC = 20261920
N_OUTER = 2000; N_INNER = 1000
LEVELS = np.round(0.950 + 0.0005 * np.arange(100), 4)             # 0.9500 ... 0.9995


# ------------------------------------------------------------------------------------------------ loading
def lock2_path():
    for p in LOCK2:
        if p.exists():
            return p
    return None


def load_split(tracker, split, keys, root=None):
    """Scenes in sorted name order. Returns (names, [dict of arrays]). Only `keys` are read from each file.
    The held-out split is refused until Lock 2 exists (A10 8.6), unless root is a synthetic folder."""
    if root is None:
        root = ARR
        if split != 'train' and lock2_path() is None:
            raise SystemExit('REFUSED: split %r before LOCK_A10_2.txt exists (A10 8.6)' % split)
    d = pathlib.Path(root) / ('arrays_' + tracker) / split
    files = sorted([p for p in d.glob('*.npz') if not p.name.endswith('.tmp.npz')], key=lambda p: p.stem)
    names = []; out = []
    for p in files:
        with np.load(p, allow_pickle=False) as z:
            out.append({k: np.array(z[k]) for k in keys})
        names.append(p.stem)
    if names != sorted(names):
        raise RuntimeError('scene order')
    return names, out


STOP_SENTENCE = 'no measurable room on design data at 2 or 3 s'


def swap_clear_v02(names, scenes, split, root=None, sub='clear_v02'):
    """Departure of 19 Nov 2026 (notes\\F_DEPARTURE_CLEARANCE_v01.md): the true clearances are read from
    cache\\clear_v02\\<split>\\<scene>.npz instead of the arrays. Returns new scene dicts with `clear` and `clear2` replaced; every
    other key is the arrays'. Checked per scene: the same decision order (sweep equal to the arrays' sweep), the same shapes and
    the same NaN pattern as the arrays' clearances (whichever of clear / clear2 the scene dict holds).
    The held-out split is refused until Lock 2 exists, as in load_split."""
    if root is None:
        root = ARR
        if split != 'train' and lock2_path() is None:
            raise SystemExit('REFUSED: split %r before LOCK_A10_2.txt exists (A10 8.6)' % split)
    d = pathlib.Path(root) / sub / split
    out = []
    for nm, z in zip(names, scenes):
        with np.load(d / (nm + '.npz'), allow_pickle=False) as c:
            if not np.array_equal(np.asarray(c['sweep']), np.asarray(z['sweep'])):
                raise RuntimeError('clear_v02 %s: sweep differs from the arrays' % nm)
            y = dict(z)
            for k in ('clear', 'clear2'):
                if k in z:
                    v = np.array(c[k])
                    if v.shape != z[k].shape or not np.array_equal(np.isnan(v), np.isnan(z[k])):
                        raise RuntimeError('clear_v02 %s: %s shape or NaN pattern differs from the arrays' % (nm, k))
                    y[k] = v
        out.append(y)
    return out


def removed_counts(old, new, crit_key, clear_key, ev_key, g=1.0):
    """Descriptive: selection at margin scale g (first row with critical scale >= g, else idx55), over evaluated decisions.
    removed = selected row unsafe (clearance <= 0) under the arrays' clearance and safe (> 0) under clear_v02; added = the
    reverse. Also the evaluated (decision, row) pairs whose safety changes, in each direction."""
    r = dict(evaluated=0, removed=0, added=0, selected_unsafe_old=0, selected_unsafe_new=0,
             pairs_unsafe_to_safe=0, pairs_safe_to_unsafe=0, pairs_evaluated=0)
    for zo, zn in zip(old, new):
        ev = zo[ev_key].astype(bool)
        feas = zo[crit_key] >= g
        sel = np.where(feas.any(axis=1), feas.argmax(axis=1), zo['idx55'])
        ar = np.arange(sel.size)
        so = (zo[clear_key] > 0.)[ev]; sn = (zn[clear_key] > 0.)[ev]
        sso = (zo[clear_key] > 0.)[ar, sel][ev]; ssn = (zn[clear_key] > 0.)[ar, sel][ev]
        r['evaluated'] += int(ev.sum()); r['removed'] += int((~sso & ssn).sum()); r['added'] += int((sso & ~ssn).sum())
        r['selected_unsafe_old'] += int((~sso).sum()); r['selected_unsafe_new'] += int((~ssn).sum())
        r['pairs_unsafe_to_safe'] += int((~so & sn).sum()); r['pairs_safe_to_unsafe'] += int((so & ~sn).sum())
        r['pairs_evaluated'] += int(so.size)
    return r


# ------------------------------------------------------------------------------------------------ gridless events (own code)
@nb.njit(cache=True)
def _scene_events(crit, idx55, clear, vbar, des, mask, gmax, T0, eb, ed):
    """One scene, one source, one population (mask). Adds the g = 0 totals to T0 (4: decisions, wrong go, caution sum, caution
    count) and writes the events (breakpoint b, change of the totals just above b) to eb, ed (3: wrong go, caution sum, caution
    count). Selection at scale g: the first row in cost order with critical scale >= g, else the fallback row.
    Returns the number of events."""
    n, R = crit.shape
    ne = 0
    vals = np.empty(R); rows = np.empty(R, np.int64)
    for i in range(n):
        if not mask[i]:
            continue
        orc = -1                                            # first truly safe row (W1: clearance > 0)
        for j in range(R):
            if clear[i, j] > 0.0:
                orc = j
                break
        nr = 0; m = -np.inf                                 # rows that can ever be selected: strict running maxima
        for j in range(R):
            v = crit[i, j]
            if v != v:
                continue
            if v > m:
                vals[nr] = v; rows[nr] = j; nr += 1; m = v
        t0 = -1
        for t in range(nr):
            if vals[t] >= 0.0:
                t0 = t
                break
        cur = idx55[i] if t0 < 0 else rows[t0]
        sc = clear[i, cur] > 0.0
        T0[0] += 1.0
        if sc:
            T0[2] += (vbar[i, orc] - vbar[i, cur]) / des[i]; T0[3] += 1.0
        else:
            T0[1] += 1.0
        if t0 < 0:
            continue
        for t in range(t0, nr):
            b = vals[t]
            if not (b < gmax):
                break
            nxt = rows[t + 1] if t + 1 < nr else idx55[i]
            if nxt != cur:
                sn = clear[i, nxt] > 0.0
                sc = clear[i, cur] > 0.0
                wn = 0.0 if sn else 1.0; wc = 0.0 if sc else 1.0
                cn = (vbar[i, orc] - vbar[i, nxt]) / des[i] if sn else 0.0
                cc = (vbar[i, orc] - vbar[i, cur]) / des[i] if sc else 0.0
                eb[ne] = b
                ed[ne, 0] = wn - wc; ed[ne, 1] = cn - cc; ed[ne, 2] = (1.0 if sn else 0.0) - (1.0 if sc else 0.0)
                ne += 1
            cur = nxt
    return ne


class Source:
    """Events of one source over all scenes, sorted by breakpoint (stable: scene order, then decision order)."""

    def __init__(self, scenes, crit_of, clear_key, mask_of, gmax=GMAX):
        ns = len(scenes)
        self.T0 = np.zeros((ns, 4)); bs = []; ds = []; ss = []
        for k, z in enumerate(scenes):
            crit = np.ascontiguousarray(crit_of(k, z), dtype=np.float64)
            n, R = crit.shape
            eb = np.empty(n * R); ed = np.empty((n * R, 3))
            ne = _scene_events(crit, np.ascontiguousarray(z['idx55'], dtype=np.int64),
                               np.ascontiguousarray(z[clear_key], dtype=np.float64),
                               np.ascontiguousarray(z['vbar'], dtype=np.float64),
                               np.ascontiguousarray(z['des'], dtype=np.float64),
                               np.ascontiguousarray(mask_of(k, z), dtype=np.bool_), gmax, self.T0[k], eb, ed)
            bs.append(eb[:ne].copy()); ds.append(ed[:ne].copy()); ss.append(np.full(ne, k, np.int32))
        b = np.concatenate(bs); d = np.concatenate(ds); s = np.concatenate(ss)
        o = np.argsort(b, kind='stable')
        self.b = b[o]; self.d = np.ascontiguousarray(d[o]); self.s = s[o]
        self.last = np.ones(self.b.size, np.uint8)
        if self.b.size > 1:
            self.last[:-1] = self.b[1:] != self.b[:-1]
        self.n_events = int(self.b.size); self.n_points = int(1 + self.last.sum())


def pack(sources):
    """sources: list, [0] = F0, [1] = E, the rest get F0's g = 0 point put in front (optA_lib_v02.curves_w)."""
    T0 = np.ascontiguousarray(np.stack([s.T0 for s in sources]))
    off = np.zeros(len(sources) + 1, np.int64)
    off[1:] = np.cumsum([s.n_events for s in sources])
    return (T0, np.concatenate([s.last for s in sources]), np.concatenate([s.s for s in sources]),
            np.ascontiguousarray(np.concatenate([s.d for s in sources])), off)


# ------------------------------------------------------------------------------------------------ kernel (own code)
@nb.njit(cache=True)
def _front(c, w, i0, i1, pre, pc, pw, lev, c0, step, f):
    """Step frontier on the levels: f[l] = lowest w among the finite points with c <= lev[l]; NaN where there is none."""
    nlev = lev.size
    for l in range(nlev):
        f[l] = np.inf
    asc = step > 0.0
    for k in range(i0 - 1 if pre else i0, i1):
        if k < i0:
            ck = pc; wk = pw
        else:
            ck = c[k]; wk = w[k]
        if not (np.isfinite(ck) and np.isfinite(wk)):
            continue
        if asc:
            if ck > lev[nlev - 1]:
                continue
            l = int(np.ceil((ck - c0) / step))
            if l < 0:
                l = 0
            if l > nlev - 1:
                l = nlev - 1
            while l > 0 and ck <= lev[l - 1]:
                l -= 1
            while ck > lev[l]:
                l += 1
            if wk < f[l]:
                f[l] = wk
        else:                                               # all levels equal, or descending: direct, level by level
            for l in range(nlev):
                if ck <= lev[l] and wk < f[l]:
                    f[l] = wk
    if asc:
        for l in range(1, nlev):
            if f[l - 1] < f[l]:
                f[l] = f[l - 1]
    for l in range(nlev):
        if f[l] == np.inf:
            f[l] = np.nan


@nb.njit(parallel=True, cache=True)
def kernel(W, T0, last, es, ed, off):
    """W (B, nscene) scene weights. Returns (B, 2 + nsrc): decisions n (of F0), c0, C, then D_gl(source k, F0) for k = 1 .. nsrc-1
    (k = 1 is E: the room's sum over the 201 levels). NaN where a level has no point (as np.sum of the library's frontiers)."""
    B = W.shape[0]; nsrc = T0.shape[0]; ns = T0.shape[1]
    npt = off[nsrc] + nsrc
    out = np.full((B, 2 + nsrc), np.nan)
    for b in nb.prange(B):
        w = W[b]
        c = np.empty(npt); g = np.empty(npt)
        p0 = np.empty(nsrc + 1, np.int64)
        p = 0
        for k in range(nsrc):
            p0[k] = p
            t0 = 0.0; t1 = 0.0; t2 = 0.0; t3 = 0.0
            for s in range(ns):
                ws = w[s]
                t0 += ws * T0[k, s, 0]; t1 += ws * T0[k, s, 1]; t2 += ws * T0[k, s, 2]; t3 += ws * T0[k, s, 3]
            if k == 0:
                out[b, 0] = t0
            c[p] = 100.0 * t2 / t3 if t3 != 0.0 else np.nan
            g[p] = 100.0 * t1 / t0 if t0 != 0.0 else np.nan
            p += 1
            a1 = 0.0; a2 = 0.0; a3 = 0.0
            for e in range(off[k], off[k + 1]):
                ws = w[es[e]]
                a1 += ws * ed[e, 0]; a2 += ws * ed[e, 1]; a3 += ws * ed[e, 2]
                if last[e]:
                    d3 = a3 + t3
                    c[p] = 100.0 * (a2 + t2) / d3 if d3 != 0.0 else np.nan
                    g[p] = 100.0 * (a1 + t1) / t0 if t0 != 0.0 else np.nan
                    p += 1
        p0[nsrc] = p
        c0 = c[p0[0]]; w0 = g[p0[0]]
        mx0 = -np.inf; mx1 = -np.inf
        for k in range(p0[0], p0[1]):
            if c[k] > mx0:
                mx0 = c[k]
        for k in range(p0[1], p0[2]):
            if c[k] > mx1:
                mx1 = c[k]
        if mx0 == -np.inf or mx1 == -np.inf or not np.isfinite(c0):
            continue
        C = mx0 if mx0 < mx1 else mx1
        out[b, 1] = c0; out[b, 2] = C
        lev = np.empty(NLEV)
        step = (C - c0) / (NLEV - 1)
        for l in range(NLEV):
            lev[l] = l * step + c0
        lev[NLEV - 1] = C
        f0 = np.empty(NLEV); fa = np.empty(NLEV)
        _front(c, g, p0[0], p0[1], False, c0, w0, lev, c0, step, f0)
        for k in range(1, nsrc):
            _front(c, g, p0[k], p0[k + 1], k >= 2, c0, w0, lev, c0, step, fa)
            acc = 0.0
            for l in range(NLEV):
                acc += f0[l] - fa[l]
            out[b, 2 + k] = acc
    return out

@nb.njit(cache=True)
def _bin(ck, lev, c0, inv, asc):
    """Index of the first level with ck <= lev[l] (levels ascending), or -1 when ck is above the last level."""
    nlev = lev.size
    if ck > lev[nlev - 1]:
        return -1
    if ck <= c0:                                            # lev[0] = c0 exactly
        return 0
    l = int(np.ceil((ck - c0) * inv))
    if l < 0:
        l = 0
    if l > nlev - 1:
        l = nlev - 1
    while l > 0 and ck <= lev[l - 1]:
        l -= 1
    while ck > lev[l]:
        l += 1
    return l


@nb.njit(parallel=True, cache=True)
def kernel2(W, T0, last, es, ed, off):
    """Same results as kernel (bit for bit; checked in fr_test_v01.py), faster: the wrong-go rate 100 x / n is increasing in the
    count x, so the lowest rate of a level is taken over x and divided once; F0's and E's points are stored (the levels need
    both), the other sources' points go straight to their level."""
    B = W.shape[0]; nsrc = T0.shape[0]; ns = T0.shape[1]
    n01 = off[2] + 2
    out = np.full((B, 2 + nsrc), np.nan)
    for b in nb.prange(B):
        w = W[b]
        c = np.empty(n01); x = np.empty(n01)
        tt = np.empty((nsrc, 4))
        for k in range(nsrc):
            t0 = 0.0; t1 = 0.0; t2 = 0.0; t3 = 0.0
            for s in range(ns):
                ws = w[s]
                t0 += ws * T0[k, s, 0]; t1 += ws * T0[k, s, 1]; t2 += ws * T0[k, s, 2]; t3 += ws * T0[k, s, 3]
            tt[k, 0] = t0; tt[k, 1] = t1; tt[k, 2] = t2; tt[k, 3] = t3
        out[b, 0] = tt[0, 0]
        p = 0; p1 = 0
        for k in range(2):
            t1 = tt[k, 1]; t2 = tt[k, 2]; t3 = tt[k, 3]
            c[p] = 100.0 * t2 / t3 if t3 != 0.0 else np.nan
            x[p] = t1
            p += 1
            a1 = 0.0; a2 = 0.0; a3 = 0.0
            for e in range(off[k], off[k + 1]):
                ws = w[es[e]]
                a1 += ws * ed[e, 0]; a2 += ws * ed[e, 1]; a3 += ws * ed[e, 2]
                if last[e]:
                    d3 = a3 + t3
                    c[p] = 100.0 * (a2 + t2) / d3 if d3 != 0.0 else np.nan
                    x[p] = a1 + t1
                    p += 1
            if k == 0:
                p1 = p
        c0 = c[0]
        mx0 = -np.inf; mx1 = -np.inf
        for k in range(0, p1):
            if c[k] > mx0:
                mx0 = c[k]
        for k in range(p1, p):
            if c[k] > mx1:
                mx1 = c[k]
        if mx0 == -np.inf or mx1 == -np.inf or not np.isfinite(c0) or tt[0, 0] == 0.0:
            continue
        C = mx0 if mx0 < mx1 else mx1
        out[b, 1] = c0; out[b, 2] = C
        lev = np.empty(NLEV)
        step = (C - c0) / (NLEV - 1)
        for l in range(NLEV):
            lev[l] = l * step + c0
        lev[NLEV - 1] = C
        asc = step > 0.0
        inv = 1.0 / step if asc else 0.0
        x0 = x[0]
        f0 = np.empty(NLEV); fa = np.empty(NLEV)
        for k in range(nsrc):
            for l in range(NLEV):
                fa[l] = np.inf
            if k < 2:
                i0 = 0 if k == 0 else p1
                i1 = p1 if k == 0 else p
                for q in range(i0, i1):
                    ck = c[q]
                    if not np.isfinite(ck):
                        continue
                    if asc:
                        l = _bin(ck, lev, c0, inv, asc)
                        if l >= 0 and x[q] < fa[l]:
                            fa[l] = x[q]
                    else:
                        for l in range(NLEV):
                            if ck <= lev[l] and x[q] < fa[l]:
                                fa[l] = x[q]
            else:
                # F0's g = 0 point in front, then the source's own points
                t1 = tt[k, 1]; t2 = tt[k, 2]; t3 = tt[k, 3]
                a1 = 0.0; a2 = 0.0; a3 = 0.0
                ck = np.nan; xk = 0.0
                e = off[k] - 2
                while e < off[k + 1]:
                    if e == off[k] - 2:
                        ck = c0; xk = x0; emit = True
                    elif e == off[k] - 1:
                        ck = 100.0 * t2 / t3 if t3 != 0.0 else np.nan
                        xk = t1; emit = True
                    else:
                        ws = w[es[e]]
                        a1 += ws * ed[e, 0]; a2 += ws * ed[e, 1]; a3 += ws * ed[e, 2]
                        emit = last[e] != 0
                        if emit:
                            d3 = a3 + t3
                            ck = 100.0 * (a2 + t2) / d3 if d3 != 0.0 else np.nan
                            xk = a1 + t1
                    e += 1
                    if not emit or not np.isfinite(ck):
                        continue
                    if asc:
                        l = _bin(ck, lev, c0, inv, asc)
                        if l >= 0 and xk < fa[l]:
                            fa[l] = xk
                    else:
                        for l in range(NLEV):
                            if ck <= lev[l] and xk < fa[l]:
                                fa[l] = xk
            tk0 = tt[k, 0]
            for l in range(NLEV):
                if asc and l > 0 and fa[l - 1] < fa[l]:
                    fa[l] = fa[l - 1]
            for l in range(NLEV):
                fa[l] = 100.0 * fa[l] / tk0 if fa[l] != np.inf else np.nan
            if k == 0:
                for l in range(NLEV):
                    f0[l] = fa[l]
            else:
                acc = 0.0
                for l in range(NLEV):
                    acc += f0[l] - fa[l]
                out[b, 2 + k] = acc
    return out


# ------------------------------------------------------------------------------------------------ draws
@nb.njit(cache=True)
def counts_of(idx, n):
    B = idx.shape[0]
    out = np.zeros((B, n))
    for b in range(B):
        for j in range(idx.shape[1]):
            out[b, idx[b, j]] += 1.0
    return out


def primary_counts(n):
    return counts_of(np.random.default_rng(SEED_PRIMARY).integers(0, n, (NBOOT, n)), n)


def rat(D, den):
    """D / den where den is finite and > 0, else NaN (optA_lib_v02.ratio, elementwise)."""
    D = np.asarray(D, float); den = np.asarray(den, float)
    ok = np.isfinite(den) & (den > 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(ok, D / np.where(ok, den, 1.), np.nan)


def pint(b, level):
    """Percentile interval at a nominal level over the finite resamples."""
    b = np.asarray(b, float); f = np.isfinite(b)
    if not f.any():
        return [float('nan'), float('nan')]
    a = 50. * (1. - level)
    return [float(x) for x in np.percentile(b[f], [a, 100. - a])]


# ------------------------------------------------------------------------------------------------ E5_x (A10 2.2), own code
def midrank(r):
    """1-based mid-ranks of the finite entries of r (NaN elsewhere) and their number."""
    rk = np.full(r.size, np.nan)
    ok = np.isfinite(r)
    x = r[ok]; n = x.size
    if n == 0:
        return rk, 0
    o = np.argsort(x, kind='stable'); xs = x[o]
    new = np.concatenate([[True], xs[1:] != xs[:-1]])
    st = np.nonzero(new)[0]; sz = np.diff(np.concatenate([st, [n]]))
    rg = st + (sz + 1) / 2.                               # average of the 1-based positions st+1 .. st+sz
    t = np.empty(n); t[o] = np.repeat(rg, sz)
    rk[ok] = t
    return rk, n


def ratio_summary(cF0, cN, ev):
    """Margin ratio sqrt(s_N / s_F0) = sqrt(cF0 / cN) at the binding rows: rows of evaluated decisions with finite positive
    critical scales under both (the rule of record, rev_c_ratio_tracks_v01)."""
    ok = ev[:, None] & np.isfinite(cF0) & np.isfinite(cN) & (cF0 > 0) & (cN > 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        m = np.sqrt(cF0 / cN)[ok]
    if m.size == 0:
        return dict(rows=0, median=float('nan'), q05=float('nan'), q95=float('nan'), A=float('nan'),
                    within5_share=float('nan'), within5_n=0)
    med = float(np.median(m)); q05, q95 = (float(x) for x in np.percentile(m, [5, 95]))
    w5 = np.abs(m / med - 1.) <= 0.05
    return dict(rows=int(m.size), median=med, q05=q05, q95=q95, A=(q95 - q05) / (2. * med),
                within5_share=float(w5.mean()), within5_n=int(w5.sum()))


def e5_scales(cF0, cE, ev, m, A, n_all=False):
    """Critical scales of E5_x: cF0 / f_i^2, f_i = m (1 + A (2 u_i - 1)); u_i = (mid-rank of r_i - 0.5) / n, with
    r_i = median over the rows with finite positive cF0 and cE of sqrt(cF0 / cE), ranked over the evaluated decisions that
    have such rows (n = their number); 0.5 for the other decisions.
    n_all=True (variant, point only): n is the number of all evaluated decisions."""
    ok = np.isfinite(cF0) & np.isfinite(cE) & (cF0 > 0) & (cE > 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        rho = np.where(ok, np.sqrt(cF0 / np.where(ok, cE, 1.)), np.nan)
    r = np.full(cF0.shape[0], np.nan)
    for i in np.nonzero(ok.any(axis=1) & ev)[0]:
        r[i] = np.median(rho[i][ok[i]])
    rk, n = midrank(r)
    nd = float(ev.sum()) if n_all else float(max(n, 1))
    u = np.where(np.isfinite(rk), (rk - 0.5) / nd, 0.5)
    c5 = scales_from_u(cF0, u, m, A)
    return c5, u, dict(n_ranked=int(n), n_evaluated=int(ev.sum()), n_without_rows=int(ev.sum() - n))


def scales_from_u(cF0, u, m, A):
    """cF0 / f_i^2 with f_i = m (1 + A (2 u_i - 1))."""
    f = m * (1. + A * (2. * u - 1.))
    with np.errstate(divide='ignore', invalid='ignore'):
        return cF0 / (f * f)[:, None]


def permute_u(u, ev, cut, seed=SEED_E5P):
    """E5p: u permuted within each scene among its evaluated decisions; one default_rng(seed), one permutation per scene in
    sorted scene order (cut: scene boundaries in the concatenated decision order)."""
    rng = np.random.default_rng(seed)
    out = u.copy()
    for k in range(len(cut) - 1):
        idx = cut[k] + np.nonzero(ev[cut[k]:cut[k + 1]])[0]
        out[idx] = rng.permutation(u[idx])
    return out


def po_scales(cF0, cE, ps=(0.25, 0.5, 0.75), seed=SEED_PO):
    """Partial oracles (rule of record: rev_g_partial_oracle_draws_v01): one uniform per stored decision (all built decisions)
    in (sorted scene name, decision index) order; PO_p takes E's critical scales where u < p and F0's elsewhere."""
    U = np.random.default_rng(seed).random(cF0.shape[0])
    return [np.where((U < p)[:, None], cE, cF0) for p in ps]


# ------------------------------------------------------------------------------------------------ calibration (A10 2.6)
def cover_rows(inner, theta):
    """inner (N_INNER, nstat) statistics of one outer sample; theta (nstat,) full-sample points.
    -> (nstat, nlevels) bool: the inner percentile interval at each nominal level contains the point."""
    ns = inner.shape[1]
    out = np.zeros((ns, LEVELS.size), bool)
    a = 50. * (1. - LEVELS)
    for j in range(ns):
        x = inner[:, j]; x = x[np.isfinite(x)]
        if x.size == 0 or not np.isfinite(theta[j]):
            continue
        lo = np.percentile(x, a); hi = np.percentile(x, 100. - a)
        out[j] = (lo <= theta[j]) & (theta[j] <= hi)
    return out


def level_smallest(cov):
    """Index of the smallest nominal level whose coverage is >= 0.95; -1 if none. cov (..., nlevels)."""
    ok = cov >= 0.95
    return np.where(ok.any(axis=-1), ok.argmax(axis=-1), -1)


def calibrate_decide(cover1, cover2=None):
    """cover1 (N_OUTER, nlevels) bool of one statistic (inner seed 1); cover2 the same for the second inner seed (None when
    not needed). Returns the decision of A10 2.6."""
    no = cover1.shape[0]
    cov = cover1.mean(axis=0)
    d = dict(coverage_nominal95=float(cov[0]), n_outer=int(no))
    if cov[0] >= 0.94:
        d.update(level=0.95, cal='nominal95', rule='nominal 95% (estimated coverage >= 0.94)')
        return d
    k = int(level_smallest(cov))
    d['candidate_level'] = float(LEVELS[k]) if k >= 0 else None
    idx = np.random.default_rng(SEED_MC).integers(0, no, (2000, no))
    covr = counts_of(idx, no) @ cover1.astype(float) / no                   # (2000, nlevels)
    kr = level_smallest(covr)
    lr = np.where(kr >= 0, LEVELS[np.clip(kr, 0, None)], np.nan)
    d['mc_n_without_level'] = int((kr < 0).sum())
    fin = bool(np.isfinite(lr).all())
    d['mc_sd'] = float(np.std(lr, ddof=1)) if fin else float('nan')
    d['mc_sd_ddof0'] = float(np.std(lr)) if fin else float('nan')
    lr2 = np.where(covr[:, 0] >= 0.94, 0.95, lr)          # variant, reported only: the whole rule in each resample
    d['mc_sd_fullrule_variant'] = float(np.std(lr2, ddof=1)) if np.isfinite(lr2).all() else float('nan')
    if cover2 is None:
        raise RuntimeError('second inner seed needed but not supplied')
    cov2 = cover2.mean(axis=0); k2 = int(level_smallest(cov2))
    d['second_seed_coverage_nominal95'] = float(cov2[0])
    d['second_seed_level'] = float(LEVELS[k2]) if k2 >= 0 else None
    ok = (k >= 0 and k2 >= 0 and fin and d['mc_sd'] <= 0.002
          and abs(float(LEVELS[k]) - float(LEVELS[k2])) <= 0.002 + 1e-12)
    if ok:
        d.update(level=float(LEVELS[k]), cal='calibrated', rule='calibrated level (both checks hold)')
    else:
        d.update(level=0.99, cal='nominal99', rule='nominal 99% (the calibrated level failed a check or does not exist)')
    return d


def jdump(obj):
    return json.dumps(obj, indent=1, default=float, allow_nan=True)


def write_once(path, doc):
    path = pathlib.Path(path)
    if path.exists():
        raise SystemExit('REFUSED: %s exists' % path)
    path.write_text(jdump(doc), encoding='utf-8')
