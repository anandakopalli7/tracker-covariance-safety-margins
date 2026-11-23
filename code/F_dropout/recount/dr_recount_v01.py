"""DR recount (second program) v01: independent recount of AMENDMENT_11 section 6c (detection dropouts, scenario DR).

Written 21 Nov 2026 from the TEXT of A11_6c_DROPOUT_SPEC_v01.md (6c.4-6c.7), AMENDMENT_10_v13.md section 2 and 5.3, and the
definitions files CD_DEFINITIONS_v13.md / B_*_DEFINITIONS (gridless frontier, calibration details). It does not read or import the
first program. Imports: numpy, the standard library, optA_lib_v02 (frozen scoring library of record: boot_counts, NLEV, dec_eq,
clean_clear, and, for --selfcheck only, frontier / levels_of / curves_w / eval_scoring / select_grid / stats_scored). numba is used when
installed (no fastmath; parallelism only over resamples, each resample is computed by one thread, so results are deterministic).

Usage:  python -I dr_recount_v01.py [--test-old] [--quick] [--threads N] [--nboot N] [--selfcheck] [--out PATH]
Environment: DR_P_ROOT (programme P root or the folder holding optA_lib_v02.py), DR_ROOT (the F_dropout folder), DR_LOCK (lock file).
"""
import os, sys, json, hashlib, argparse, math, pathlib, time, glob, warnings

# ------------------------------------------------------------------------------------------------ arguments (before numba import)
_ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
_ap.add_argument('--test-old', action='store_true')
_ap.add_argument('--quick', action='store_true', help='test only: 200 outer x 100 inner, 2000 single resamples')
_ap.add_argument('--threads', type=int, default=0)
_ap.add_argument('--nboot', type=int, default=None)
_ap.add_argument('--selfcheck', action='store_true', help='compare the gridless kernel with the library on a small subset, then exit')
_ap.add_argument('--out', default=None)
ARGS = _ap.parse_args()
if ARGS.threads > 0:
    os.environ['NUMBA_NUM_THREADS'] = str(ARGS.threads)
    os.environ.setdefault('OMP_NUM_THREADS', str(ARGS.threads))
    os.environ.setdefault('OPENBLAS_NUM_THREADS', str(ARGS.threads))
    os.environ.setdefault('MKL_NUM_THREADS', str(ARGS.threads))

import numpy as np

try:
    import numba
    from numba import njit, prange
    HAVE_NUMBA = True
except Exception:                                   # pure-python fallback (tiny tests only)
    HAVE_NUMBA = False

    def njit(*a, **k):
        if len(a) == 1 and callable(a[0]) and not k:
            return a[0]
        return lambda f: f
    prange = range

DEFAULT_P_ROOT = r'<library folder>'
DEFAULT_ROOT = r'ARS_TRIAL\revision_v13\work\F_dropout'
P_ROOT = pathlib.Path(os.environ.get('DR_P_ROOT', DEFAULT_P_ROOT))
ROOT = pathlib.Path(os.environ.get('DR_ROOT', DEFAULT_ROOT))
_lib = P_ROOT / '11_ojits' / 'A6R' / 'code'
if not (_lib / 'optA_lib_v02.py').exists():
    _lib = P_ROOT
sys.path.insert(0, str(_lib))
import optA_lib_v02 as L                           # noqa: E402  frozen library of record, read-only

LOCK = pathlib.Path(os.environ.get('DR_LOCK', str(ROOT.parent.parent / 'LOCK_A11b.txt')))

NLEV = L.NLEV                                      # 201
SEEDS = dict(boot=20261911, outer=20261912, inner1=20261913, inner2=20261914, perm=20261915, mc=20261920)
DELTA = 0.05
GMAX = 1000.0
LEVELS_NOM = [round(0.95 + 0.0005 * j, 4) for j in range(91)]      # 0.9500 ... 0.9995 (step 0.0005)
TOL = 1e-12
STATS = ['R_gl', 'c', 'cdiff', 'r']


def log(*a):
    print('[%7.1f s]' % (time.time() - T_START), *a, flush=True)


T_START = time.time()


# ------------------------------------------------------------------------------------------------ masks (6c.4)
def make_mask(rid, n):
    """6c.4: rng = default_rng(int.from_bytes(sha256(('A11/D/' + rid).encode('utf-8')).digest()[:8], 'big')); frame 0 never masked;
    for i = 1..n-1 in order, at each frame not inside a window: u = rng.random(); if u < 0.10: L = rng.integers(1, 4), mask frames
    i..i+L-1 (truncated at n-1). Frames inside a window draw nothing."""
    rng = np.random.default_rng(int.from_bytes(hashlib.sha256(('A11/D/' + rid).encode('utf-8')).digest()[:8], 'big'))
    masked = []
    free_from = 1                                   # first frame not inside a window
    for i in range(1, n):
        if i < free_from:
            continue
        u = rng.random()
        if u < 0.10:
            Ln = int(rng.integers(1, 4))
            for j in range(i, min(i + Ln, n)):
                masked.append(j)
            free_from = i + Ln
    return masked


# ------------------------------------------------------------------------------------------------ loading
def load_npz(path):
    z = np.load(path, allow_pickle=True)
    d = {k: z[k] for k in z.files}
    d['meta'] = json.loads(str(d['meta']))
    return d


def load_runs(dirDR, dirREC):
    fa = sorted(glob.glob(str(dirDR / '*.npz')))
    fb = sorted(glob.glob(str(dirREC / '*.npz')))
    ids = [pathlib.Path(f).stem for f in fa]
    idsb = [pathlib.Path(f).stem for f in fb]
    if ids != sorted(ids) or ids != idsb:
        raise SystemExit('DR and DRrec run sets differ: %d vs %d files' % (len(ids), len(idsb)))
    if not ids:
        raise SystemExit('no DR arrays in %s' % dirDR)
    runs = []
    for rid, f1, f2 in zip(ids, fa, fb):
        a = load_npz(f1)
        b = load_npz(f2)
        ev = a['evaluated'].astype(bool)
        if not np.array_equal(ev, b['evaluated'].astype(bool)):
            raise SystemExit('DR / DRrec evaluated differ in %s' % rid)
        des = np.asarray(a['des'], float)
        des_const = bool(np.all(des == des[0]))
        same = {}
        for key in ('cE', 'cN', 'clear', 'vbar', 'idx55', 'k', 'dr_masked', 'dr_age'):
            same[key] = bool(np.array_equal(a[key], b[key], equal_nan=True)) if key in a and key in b else None
        r = dict(id=rid, n_dec=int(len(ev)), ev=ev, des0=float(des[0]), des_const=des_const, meta=a['meta'], same_rec=same)
        r['clear1'] = L.clean_clear(np.asarray(a['clear'], float))[ev]
        r['vbar'] = np.asarray(a['vbar'], float)[ev]
        r['idx55'] = np.asarray(a['idx55'])[ev].astype(int)
        r['cF0'] = np.asarray(a['cF0'], float)[ev]
        r['cE'] = np.asarray(a['cE'], float)[ev]
        r['cN'] = np.asarray(a['cN'], float)[ev]
        r['cFr'] = np.asarray(b['cF0'], float)[ev]
        r['cE_rec'] = np.asarray(b['cE'], float)[ev]
        r['cN_rec'] = np.asarray(b['cN'], float)[ev]
        r['dr_masked'] = np.asarray(a['dr_masked']).astype(bool)[ev]
        r['dr_age'] = np.asarray(a['dr_age']).astype(int)[ev]
        r['dr_frame_all'] = np.asarray(a['dr_frame']).astype(int) if 'dr_frame' in a else None
        r['dr_masked_all'] = np.asarray(a['dr_masked']).astype(bool)
        runs.append(r)
    return runs


# ------------------------------------------------------------------------------------------------ gridless events (A10 2.3)
def sel_path(c, idx55):
    """The selected row of one decision as the margin scale g rises from 0 to GMAX: (row at g = 0, [(breakpoint b, row selected for g
    just above b)]). Row selected at g = first row j (cost order) with c[j] >= g, else idx55; NaN entries never qualify."""
    recs = []
    m = -np.inf
    for j in range(len(c)):
        v = c[j]
        if v != v:
            continue
        if v > m:
            recs.append((v, j))
            m = v
    t0 = None
    for t, (v, _) in enumerate(recs):
        if v >= 0.0:
            t0 = t
            break
    if t0 is None:
        return int(idx55), []
    s0 = recs[t0][1]
    ev = []
    for t in range(t0, len(recs)):
        b = recs[t][0]
        if not (b < GMAX):
            break
        nxt = recs[t + 1][1] if t + 1 < len(recs) else int(idx55)
        ev.append((float(b), int(nxt)))
    return int(s0), ev


def row_stats_run(r, sel):
    """Per decision (in the run's evaluated set restricted to sel) and per row: (wrong go, caution term, safe count) under the 3 s
    commitment: safe iff clean clearance > 0; caution term = (vbar of the first safe row - vbar of the row) / des when the row is safe."""
    clear1 = r['clear1'][sel]
    vbar = r['vbar'][sel]
    safe = clear1 > 0.0
    orc = safe.argmax(axis=1)
    n = clear1.shape[0]
    ar = np.arange(n)
    ct = np.where(safe, (vbar[ar, orc][:, None] - vbar) / r['des0'], 0.0)
    return (~safe).astype(float), ct, safe.astype(float)


def build_source(runs, crit_list, popsel):
    """Events of one source over the runs (ascending ids). Returns per-run T0 (nrun, 4) = [decisions, wrong go, caution sum, count] at
    g = 0 and the events (breakpoint, delta wrong go, delta caution sum, delta count) with the run index, sorted by breakpoint (stable)."""
    nrun = len(runs)
    T0 = np.zeros((nrun, 4))
    bs, ds, ris = [], [], []
    for ri, r in enumerate(runs):
        sel = popsel[ri]
        idxs = np.nonzero(sel)[0]
        if idxs.size == 0:
            continue
        crit = crit_list[ri][sel]
        wr, ct, sf = row_stats_run(r, sel)
        idx55 = r['idx55'][sel]
        T0[ri, 0] = float(idxs.size)
        t1 = t2 = t3 = 0.0
        for i in range(idxs.size):
            s0, ev = sel_path(crit[i], idx55[i])
            t1 += wr[i, s0]
            t2 += ct[i, s0]
            t3 += sf[i, s0]
            cur = s0
            for b, nxt in ev:
                if nxt != cur:
                    bs.append(b)
                    ds.append((wr[i, nxt] - wr[i, cur], ct[i, nxt] - ct[i, cur], sf[i, nxt] - sf[i, cur]))
                    ris.append(ri)
                cur = nxt
        T0[ri, 1], T0[ri, 2], T0[ri, 3] = t1, t2, t3
    if bs:
        b = np.array(bs)
        d = np.array(ds)
        ri = np.array(ris, dtype=np.int64)
        o = np.argsort(b, kind='stable')
        b, d, ri = b[o], d[o], ri[o]
        keep = np.concatenate([b[1:] != b[:-1], [True]])
    else:
        b = np.zeros(0)
        d = np.zeros((0, 3))
        ri = np.zeros(0, dtype=np.int64)
        keep = np.zeros(0, dtype=bool)
    return dict(T0=T0, b=b, d=d, ri=ri, keep=keep)


class DataSet:
    """Sources (in a fixed order; source 0 is the reference F0, source 1 is E) concatenated for the numba kernel."""

    def __init__(self, names, srcs):
        self.names = list(names)
        S = len(srcs)
        self.T0 = np.ascontiguousarray(np.stack([s['T0'] for s in srcs]))               # (S, nrun, 4)
        self.off = np.zeros(S + 1, dtype=np.int64)
        for i, s in enumerate(srcs):
            self.off[i + 1] = self.off[i] + s['b'].size
        self.ri = np.ascontiguousarray(np.concatenate([s['ri'] for s in srcs]).astype(np.int64))
        self.d = np.ascontiguousarray(np.concatenate([s['d'] for s in srcs], axis=0).reshape(-1, 3))
        self.keep = np.ascontiguousarray(np.concatenate([s['keep'] for s in srcs]).astype(np.bool_))
        self.maxm = int(max(s['b'].size for s in srcs)) + 2
        self.nev = [int(s['b'].size) for s in srcs]


# ------------------------------------------------------------------------------------------------ numba kernels
@njit(error_model='numpy')
def _points(w, T0s, ri, dd, keep, lo, hi, cs, ws):
    """Curve points of one source under run weights w: the g = 0 point, then one point after each distinct breakpoint (cumulative
    sums, T = running sum of w*delta + T0, as the library's cumsum(...) + T0). Returns the number of points."""
    nrun = w.shape[0]
    t0 = 0.0
    t1 = 0.0
    t2 = 0.0
    t3 = 0.0
    for r in range(nrun):
        wr = w[r]
        t0 += wr * T0s[r, 0]
        t1 += wr * T0s[r, 1]
        t2 += wr * T0s[r, 2]
        t3 += wr * T0s[r, 3]
    cs[0] = 100. * t2 / t3
    ws[0] = 100. * t1 / t0
    n = 1
    s1 = 0.0
    s2 = 0.0
    s3 = 0.0
    dirty = False
    for e in range(lo, hi):
        wr = w[ri[e]]
        if wr != 0.0:
            s1 += dd[e, 0] * wr
            s2 += dd[e, 1] * wr
            s3 += dd[e, 2] * wr
            dirty = True
        if keep[e] and dirty:
            cs[n] = 100. * (s2 + t2) / (s3 + t3)
            ws[n] = 100. * (s1 + t1) / t0
            n += 1
            dirty = False
    return n


@njit(error_model='numpy')
def _bucket(cs, ws, n, lev, best, mono, inv):
    """best[j] = lowest w among finite points with c <= lev[j] (inf where none). mono: levels ascending (step >= 0); inv = 1 / step
    (0 when step == 0). The level index of a point is the first j with lev[j] >= c, found from a linear estimate and then corrected
    against the levels themselves, so the result does not depend on the estimate."""
    m = lev.shape[0]
    for j in range(m):
        best[j] = np.inf
    for p in range(n):
        c = cs[p]
        w = ws[p]
        if not (np.isfinite(c) and np.isfinite(w)):
            continue
        if mono:
            if c <= lev[0]:
                j = 0
            elif c > lev[m - 1]:
                continue
            else:
                j = int((c - lev[0]) * inv)
                if j < 0:
                    j = 0
                if j > m - 1:
                    j = m - 1
                while j > 0 and lev[j - 1] >= c:
                    j -= 1
                while lev[j] < c:
                    j += 1
            if w < best[j]:
                best[j] = w
        else:
            for j in range(m):
                if c <= lev[j] and w < best[j]:
                    best[j] = w
    if mono:
        cur = np.inf
        for j in range(m):
            if best[j] < cur:
                cur = best[j]
            best[j] = cur


@njit(error_model='numpy')
def _one(w, T0, off, ri, dd, keep, need, maxm, outD):
    """One resample: D[s] = sum over 201 levels of (F_src0 - F_s), s >= 1 ; returns weighted decision count of source 0."""
    S = T0.shape[0]
    cs0 = np.empty(maxm)
    ws0 = np.empty(maxm)
    cs1 = np.empty(maxm)
    ws1 = np.empty(maxm)
    n0 = _points(w, T0[0], ri, dd, keep, off[0], off[1], cs0, ws0)
    n1 = _points(w, T0[1], ri, dd, keep, off[1], off[2], cs1, ws1)
    nd = 0.0
    for r in range(w.shape[0]):
        nd += w[r] * T0[0, r, 0]
    for s in range(S):
        outD[s] = np.nan
    cmax0 = np.nan
    for p in range(n0):
        if np.isfinite(cs0[p]) and not (cs0[p] <= cmax0):
            cmax0 = cs0[p]
    cmax1 = np.nan
    for p in range(n1):
        if np.isfinite(cs1[p]) and not (cs1[p] <= cmax1):
            cmax1 = cs1[p]
    c0 = cs0[0]
    if not (np.isfinite(c0) and np.isfinite(cmax0) and np.isfinite(cmax1)):
        return nd
    C = cmax0 if cmax0 < cmax1 else cmax1
    lev = np.empty(NLEV)
    delta = C - c0
    step = delta / (NLEV - 1)
    for j in range(NLEV):
        if step == 0.0:
            lev[j] = c0
        else:
            lev[j] = j * step + c0
    lev[NLEV - 1] = C
    mono = C >= c0
    inv = 1.0 / step if step > 0.0 else 0.0
    f0 = np.empty(NLEV)
    _bucket(cs0, ws0, n0, lev, f0, mono, inv)
    f1 = np.empty(NLEV)
    _bucket(cs1, ws1, n1, lev, f1, mono, inv)
    # E
    tot = 0.0
    ok = True
    for j in range(NLEV):
        if np.isinf(f0[j]) or np.isinf(f1[j]):
            ok = False
            break
        tot += f0[j] - f1[j]
    if ok:
        outD[1] = tot
    w00 = ws0[0]
    c00 = cs0[0]
    if S > 2:
        cs = np.empty(maxm + 1)
        ws = np.empty(maxm + 1)
        best = np.empty(NLEV)
        for s in range(2, S):
            if not need[s]:
                continue
            cs[0] = c00                                     # F0's g = 0 point prepended
            ws[0] = w00
            n = _points(w, T0[s], ri, dd, keep, off[s], off[s + 1], cs[1:], ws[1:])
            _bucket(cs, ws, n + 1, lev, best, mono, inv)
            tot = 0.0
            ok = True
            for j in range(NLEV):
                if np.isinf(f0[j]) or np.isinf(best[j]):
                    ok = False
                    break
                tot += f0[j] - best[j]
            if ok:
                outD[s] = tot
    return nd


@njit(parallel=True, error_model='numpy')
def _batch(W, T0, off, ri, dd, keep, need, maxm, outD, outN):
    for b in prange(W.shape[0]):
        row = np.empty(T0.shape[0])
        outN[b] = _one(W[b], T0, off, ri, dd, keep, need, maxm, row)
        for s in range(T0.shape[0]):
            outD[b, s] = row[s]


def eval_W(ds, W, need=None):
    """D (R, S) and weighted decision counts (R,) for the run-weight matrix W (R, nrun)."""
    W = np.ascontiguousarray(W, dtype=np.float64)
    S = len(ds.names)
    if need is None:
        need = np.ones(S, dtype=np.bool_)
    outD = np.full((W.shape[0], S), np.nan)
    outN = np.zeros(W.shape[0])
    _batch(W, ds.T0, ds.off, ds.ri, ds.d, ds.keep, np.asarray(need, dtype=np.bool_), ds.maxm, outD, outN)
    return outD, outN


# ------------------------------------------------------------------------------------------------ statistics
def hyp_stats(D):
    """D columns: 1 = E, 2 = E5, 3 = E5p, 4 = N (sources F0, E, E5, E5p, N). Returns dict of arrays over the resamples."""
    D = np.atleast_2d(D)
    den = D[:, 1]
    valid = np.isfinite(den) & (den > 0)
    with np.errstate(invalid='ignore', divide='ignore'):
        R = den / NLEV
        RR5 = np.where(valid, D[:, 2] / den, np.nan)
        RR5p = np.where(valid, D[:, 3] / den, np.nan)
        RRN = np.where(valid, D[:, 4] / den, np.nan)
        return dict(R_gl=R, c=RR5, cdiff=RR5 - RR5p, r=RRN, den=den)


def ci_at(b, level):
    b = np.asarray(b, float)
    f = b[np.isfinite(b)]
    if f.size == 0:
        return [float('nan'), float('nan')]
    if abs(level - 0.95) < 1e-12:
        q = [2.5, 97.5]
    else:
        a = 1.0 - level
        q = [round(100.0 * a / 2.0, 8), round(100.0 * (1.0 - a / 2.0), 8)]
    return [float(x) for x in np.percentile(f, q)]


def fl(x):
    return float(x) if x is not None else float('nan')


# ------------------------------------------------------------------------------------------------ calibration (A10 2.6)
def double_boot(ds, need, n_run, inner_seed, nout, ninn, theta, outer_idx):
    """Per statistic: arrays p_lt, p_le, kept (over the outer samples). theta: dict stat -> full-sample value."""
    rng = np.random.default_rng(inner_seed)
    # the outer samples' own statistics
    Wout = np.zeros((nout, n_run))
    for b in range(nout):
        Wout[b] = np.bincount(outer_idx[b], minlength=n_run)
    Dout, _ = eval_W(ds, Wout, need)
    own = hyp_stats(Dout)
    res = {k: dict(p_lt=np.full(nout, np.nan), p_le=np.full(nout, np.nan), kept=np.zeros(nout, dtype=bool)) for k in STATS}
    base = np.arange(ninn)[:, None] * n_run
    t_start = time.time()
    for b in range(nout):
        ii = rng.integers(0, n_run, (ninn, n_run))
        want = [k for k in STATS if np.isfinite(theta[k]) and np.isfinite(own[k][b])]
        if not want:
            continue
        runs_b = outer_idx[b][ii]
        W = np.bincount((runs_b + base).ravel(), minlength=ninn * n_run).reshape(ninn, n_run).astype(np.float64)
        D, _ = eval_W(ds, W, need)
        v = hyp_stats(D)
        for k in want:
            x = v[k]
            x = x[np.isfinite(x)]
            if x.size == 0:
                continue
            res[k]['p_lt'][b] = np.mean(x < theta[k])
            res[k]['p_le'][b] = np.mean(x <= theta[k])
            res[k]['kept'][b] = True
        if (b + 1) % max(1, nout // 10) == 0:
            log('  double bootstrap seed %d: %d / %d outer (%.0f s)' % (inner_seed, b + 1, nout, time.time() - t_start))
    return res


def cover_matrix(p_lt, p_le, kept):
    """(len(LEVELS_NOM), nout) boolean: the outer sample covers at the level."""
    a = 1.0 - np.array(LEVELS_NOM)
    half = (a / 2.0)[:, None]
    return (p_le[None, :] >= half - TOL) & (p_lt[None, :] <= 1.0 - half + TOL) & kept[None, :]


def choose_level(cov):
    """A10 2.6 first stage: nominal 95% if its coverage >= 0.94, else the smallest level (0.950 ... 0.9995) with coverage >= 0.95
    (None when no level reaches it)."""
    if cov[0] >= 0.94:
        return 0.95
    ok = np.nonzero(cov >= 0.95)[0]
    return float(LEVELS_NOM[ok[0]]) if ok.size else None


def calib_one(res_k, nout, mc_idx):
    kept = res_k['kept']
    nk = int(kept.sum())
    out = dict(n_kept=nk)
    if nk == 0:
        out.update(coverage=None, cov95=None, level_stage1='none valid', mc_sd=None)
        return out
    cover = cover_matrix(res_k['p_lt'], res_k['p_le'], kept)
    cov = cover[:, kept].mean(axis=1)
    out['coverage'] = [float(x) for x in cov]
    out['cov95'] = float(cov[0])
    ch = choose_level(cov)
    out['level_stage1'] = ch
    out['needs_checks'] = bool(cov[0] < 0.94)
    # Monte Carlo SD of the smallest level reaching 0.95 (1.0 when none does), 2000 resamples of the outer samples
    nres = mc_idx.shape[0]
    flat = (mc_idx + nout * np.arange(nres)[:, None]).ravel()
    Cnt = np.bincount(flat, minlength=nres * nout).reshape(nres, nout).astype(np.float64)
    num = Cnt @ cover.astype(np.float64).T                  # (nres, nlevels) exact integer sums
    den = Cnt @ kept.astype(np.float64)
    chosen = np.ones(nres)
    with np.errstate(invalid='ignore', divide='ignore'):
        covr = num / den[:, None]
    okm = (covr >= 0.95) & (den[:, None] > 0)
    anyok = okm.any(axis=1)
    first = okm.argmax(axis=1)
    lv = np.array(LEVELS_NOM)
    chosen = np.where(anyok, lv[first], 1.0)
    out['mc_sd'] = float(np.std(chosen, ddof=1))
    out['mc_mean_level'] = float(np.mean(chosen))
    return out


# ------------------------------------------------------------------------------------------------ E5 family (A10 2.2)
def midranks(x):
    u, inv, cnt = np.unique(x, return_inverse=True, return_counts=True)
    cum = np.cumsum(cnt)
    avg = cum - (cnt - 1) / 2.0
    return avg[inv]


def e5_u_vec(gF, gE, n_mode='all'):
    """u_i = (mid-rank of r_i - 0.5) / n; r_i = median over rows with finite positive g*_F0 and g*_E of (g*_F0 / g*_E)^(1/2);
    decisions without such rows get 0.5. n_mode 'all': n = number of evaluated decisions (rank among decisions that have an r_i);
    'valid': n = number of decisions that have an r_i."""
    N = gF.shape[0]
    ok = np.isfinite(gF) & (gF > 0) & np.isfinite(gE) & (gE > 0)
    with np.errstate(invalid='ignore', divide='ignore'):
        rho = np.sqrt(np.where(ok, gF / np.where(ok, gE, 1.0), np.nan))
    has = ok.any(axis=1)
    rv = np.full(N, np.nan)
    if has.any():
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            rv[has] = np.nanmedian(rho[has], axis=1)
    u = np.full(N, 0.5)
    if has.any():
        rk = midranks(rv[has])
        nn = N if n_mode == 'all' else int(has.sum())
        u[has] = (rk - 0.5) / nn
    return u, int((~has).sum())


def ratio_values(gF, gN):
    ok = np.isfinite(gF) & (gF > 0) & np.isfinite(gN) & (gN > 0)
    with np.errstate(invalid='ignore', divide='ignore'):
        rr = np.sqrt(gF[ok] / gN[ok])
    return rr


def ratio_summary(rr):
    if rr.size == 0:
        return dict(n=0, m=float('nan'), q05=float('nan'), q95=float('nan'), A=float('nan'), within5=float('nan'))
    m = float(np.median(rr))
    q05, q95 = [float(x) for x in np.percentile(rr, [5, 95])]
    A = (q95 - q05) / (2.0 * m)
    w5 = float(np.mean(np.abs(rr - m) <= 0.05 * m))
    return dict(n=int(rr.size), m=m, q05=q05, q95=q95, A=float(A), within5=w5)


def split_runs(arr, counts):
    out, p = [], 0
    for c in counts:
        out.append(arr[p:p + c])
        p += c
    return out


def make_oracle(cF_list, counts, u, m, A):
    f = m * (1.0 + A * (2.0 * u - 1.0))
    f2 = (f ** 2)[:, None]
    allF = np.concatenate(cF_list, axis=0)
    return split_runs(allF / f2, counts)


def permute_u(u, counts):
    rng = np.random.default_rng(SEEDS['perm'])
    out = np.empty_like(u)
    p = 0
    for c in counts:
        seg = u[p:p + c]
        perm = rng.permutation(c)
        out[p:p + c] = seg[perm]
        p += c
    return out


# ------------------------------------------------------------------------------------------------ pbar
def pbar_dr(pdir, expect=None):
    files = sorted(glob.glob(str(pdir / '*_pbar.npz')))
    if not files:
        return None
    acc = {}
    cnt = {}
    for f in files:
        z = np.load(f, allow_pickle=True)
        for cl in ('vehicle', 'pedestrian'):
            a = np.asarray(z['acc_' + cl], float)
            c = np.asarray(z['cnt_' + cl], float)
            acc[cl] = a if cl not in acc else acc[cl] + a
            cnt[cl] = c if cl not in cnt else cnt[cl] + c
    out = dict(n_files=len(files), files_first_last=[pathlib.Path(files[0]).name, pathlib.Path(files[-1]).name])
    for cl in ('vehicle', 'pedestrian'):
        with np.errstate(invalid='ignore', divide='ignore'):
            P = acc[cl] / cnt[cl]
        out[cl] = P.tolist()
        out['cnt_' + cl] = cnt[cl].tolist() if np.ndim(cnt[cl]) else float(cnt[cl])
    out['names'] = [pathlib.Path(f).name[:-len('_pbar.npz')] for f in files]
    return out


# ------------------------------------------------------------------------------------------------ self check against the library
def selfcheck(runs):
    """Compare the kernel with the library's grid pipeline on dense 'just above every breakpoint' grids (small subset)."""
    sub = runs[:min(3, len(runs))]
    rs = []
    for r in sub:
        keep_i = np.zeros(r['clear1'].shape[0], dtype=bool)
        keep_i[::3] = True
        q = dict(r)
        for key in ('clear1', 'vbar', 'idx55', 'cF0', 'cE', 'cN', 'cFr', 'dr_masked', 'dr_age'):
            q[key] = r[key][keep_i]
        rs.append(q)
    n = len(rs)
    popsel = [np.ones(q['clear1'].shape[0], dtype=bool) for q in rs]
    names = ['F0', 'E', 'N']
    crit = {'F0': [q['cF0'] for q in rs], 'E': [q['cE'] for q in rs], 'N': [q['cN'] for q in rs]}
    ds = DataSet(names, [build_source(rs, crit[nm], popsel) for nm in names])
    rng = np.random.default_rng(7)
    W = np.vstack([np.ones(n), rng.integers(0, 4, (3, n)).astype(float)])
    D, _ = eval_W(ds, W)
    # library: breakpoints of all sources
    bps = set([0.0])
    for nm in names:
        for ri, q in enumerate(rs):
            for i in range(q['clear1'].shape[0]):
                _, ev = sel_path(crit[nm][ri][i], q['idx55'][i])
                for b, _ in ev:
                    bps.add(b)
    # point at 'just above b' for every breakpoint b, plus the g = 0 point (g = 0 itself)
    pts = np.concatenate([[0.0], np.nextafter(np.array(sorted(bps)), np.inf)])
    worst = 0.0
    for wi in range(W.shape[0]):
        Ts = {nm: 0 for nm in names}
        for ri, q in enumerate(rs):
            if W[wi, ri] == 0:
                continue
            safe_x = q['clear1'] > 0
            m = np.ones(q['clear1'].shape[0], dtype=bool)
            for nm in names:
                sel = L.select_grid(crit[nm][ri], pts, q['idx55'])
                st = L.stats_scored(sel, q['clear1'], safe_x, q['vbar'], q['des0'], [m])[:, 0, :]
                Ts[nm] = Ts[nm] + W[wi, ri] * st
        out = L.eval_scoring(Ts, ['N'])
        dE = out['denE']
        dN = out['D']['N']
        worst = max(worst, abs(dE - D[wi, 1]), abs(dN - D[wi, 2]))
        log('selfcheck resample %d: library denE %.12g kernel %.12g | library D(N) %.12g kernel %.12g' % (wi, dE, D[wi, 1], dN, D[wi, 2]))
    log('selfcheck: max |difference| = %.3g (grid of %d points, %d runs)' % (worst, len(pts), n))
    return worst


# ------------------------------------------------------------------------------------------------ main
def main():
    test = ARGS.test_old
    quick = ARGS.quick
    if not test:
        if not LOCK.exists():
            raise SystemExit('REFUSED: %s does not exist (non-test mode needs the lock)' % LOCK)
        if quick:
            raise SystemExit('--quick is for --test-old only')
    base = ROOT / 'out' / ('testold' if test else '')
    dirDR, dirREC, dirP = base / 'DR', base / 'DRrec', (base / 'pbar') if test else (ROOT / 'out' / 'pbar')
    if not test:
        dirDR, dirREC = ROOT / 'out' / 'arrays' / 'DR', ROOT / 'out' / 'arrays' / 'DRrec'
    outp = pathlib.Path(ARGS.out) if ARGS.out else ROOT / 'recount' / ('TESTOLD_DR_RECOUNT_v01.json' if test else 'DR_RECOUNT_v01.json')
    if outp.exists():
        raise SystemExit('REFUSED: %s exists' % outp)
    nboot = ARGS.nboot if ARGS.nboot else (2000 if quick else 20000)
    nout, ninn, nmc = (200, 100, 200) if quick else (2000, 1000, 2000)

    log('numba', HAVE_NUMBA, 'threads', (numba.get_num_threads() if HAVE_NUMBA else 1), 'test', test, 'quick', quick, 'nboot', nboot)
    runs = load_runs(dirDR, dirREC)
    n_run = len(runs)
    if not test and n_run != 105:
        raise SystemExit('expected 105 fresh runs, found %d' % n_run)
    ids = [r['id'] for r in runs]
    log('runs', n_run, 'first', ids[0], 'last', ids[-1])
    if ARGS.selfcheck:
        selfcheck(runs)
        return

    # ---- masks (identity check iii)
    mask_report = dict(mode='test-old: regenerated with n = meta n_det_rows, compared with meta masked' if test else 'regenerated and compared with DR_MASKS_v01.json')
    ident = True
    bad = []
    mask_by_run = {}
    for r in runs:
        n_fr = int(r['meta']['n_det_rows'])
        mk = make_mask(r['id'], n_fr)
        mask_by_run[r['id']] = mk
        if 'masked' in r['meta'] and r['meta']['masked'] is not None:
            if [int(x) for x in r['meta']['masked']] != mk and test:
                ident = False
                bad.append((r['id'], 'meta masked differs'))
        if r['dr_frame_all'] is not None:
            exp = np.isin(r['dr_frame_all'], np.array(mk, dtype=int))
            if not np.array_equal(exp, r['dr_masked_all']):
                ident = False
                bad.append((r['id'], 'dr_masked differs from the mask at dr_frame'))
    shares = {}
    if not test:
        mf = json.loads((ROOT / 'masks' / 'DR_MASKS_v01.json').read_text(encoding='utf-8'))
        tun_ids = sorted(mf['tuning'].keys())
        pb = pbar_dr(dirP)
        if pb is None:
            raise SystemExit('no pbar files in %s' % dirP)
        if sorted(pb['names']) != tun_ids:
            ident = False
            bad.append(('tuning', 'pbar archive names differ from the mask file tuning ids'))
        if sorted(mf['fresh'].keys()) != ids:
            ident = False
            bad.append(('fresh', 'run ids differ from the mask file'))
        tot = dict(fresh=[0, 0], tuning=[0, 0])
        for part, keys in (('fresh', ids), ('tuning', tun_ids)):
            for rid in keys:
                e = mf[part].get(rid)
                if e is None:
                    continue
                mk = make_mask(rid, int(e['n']))
                if part == 'fresh' and int(e['n']) != int([r for r in runs if r['id'] == rid][0]['meta']['n_det_rows']):
                    ident = False
                    bad.append((rid, 'n differs from meta n_det_rows'))
                if [int(x) for x in e['masked']] != mk:
                    ident = False
                    bad.append((rid, 'masked frames differ'))
                tot[part][0] += len(mk)
                tot[part][1] += int(e['n'])
        shares = dict(fresh_frames=dict(masked=tot['fresh'][0], frames=tot['fresh'][1], share=tot['fresh'][0] / tot['fresh'][1]),
                      tuning_frames=dict(masked=tot['tuning'][0], frames=tot['tuning'][1], share=tot['tuning'][0] / tot['tuning'][1]),
                      file_totals=mf.get('totals'))
    else:
        pb = pbar_dr(dirP)
        tm = sum(len(v) for v in mask_by_run.values())
        tf = sum(int(r['meta']['n_det_rows']) for r in runs)
        shares = dict(test_runs_frames=dict(masked=tm, frames=tf, share=tm / tf))
    mask_report.update(identical=ident, mismatches=bad[:20])
    log('masks identical:', ident, bad[:3])

    # ---- populations and sources
    counts = [int(r['clear1'].shape[0]) for r in runs]
    n_dec = int(sum(counts))
    pops_all = [np.ones(c, dtype=bool) for c in counts]
    pops_in = [r['dr_masked'].copy() for r in runs]
    n_in = int(sum(int(p.sum()) for p in pops_in))
    des_nonconst = [r['id'] for r in runs if not r['des_const']]
    gF = np.concatenate([r['cF0'] for r in runs], axis=0)
    gE = np.concatenate([r['cE'] for r in runs], axis=0)
    gN = np.concatenate([r['cN'] for r in runs], axis=0)
    inmask = np.concatenate(pops_in)
    rr_all = ratio_values(gF, gN)
    rs_all = ratio_summary(rr_all)
    rs_in = ratio_summary(ratio_values(gF[inmask], gN[inmask]))
    m_dr, A_dr = rs_all['m'], rs_all['A']
    u, n_no_rows = e5_u_vec(gF, gE, 'all')
    u_alt, _ = e5_u_vec(gF, gE, 'valid')
    up = permute_u(u, counts)
    cF_list = [r['cF0'] for r in runs]
    crit = dict(F0=cF_list, E=[r['cE'] for r in runs], N=[r['cN'] for r in runs],
                E5=make_oracle(cF_list, counts, u, m_dr, A_dr), E5p=make_oracle(cF_list, counts, up, m_dr, A_dr),
                F0rec=[r['cFr'] for r in runs])
    log('m_DR %.9f A_DR %.9f within5 %.6f; decisions %d, in-dropout %d, decisions without rank rows %d' % (m_dr, A_dr, rs_all['within5'], n_dec, n_in, n_no_rows))

    def ds_of(names, pops):
        return DataSet(names, [build_source(runs, crit[nm], pops) for nm in names])

    t = time.time()
    dsA = ds_of(['F0', 'E', 'E5', 'E5p', 'N'], pops_all)
    log('built main source set: events %s (%.1f s)' % (dsA.nev, time.time() - t))
    dsI = ds_of(['F0', 'E', 'E5', 'N'], pops_in) if n_in > 0 else None
    dsR = ds_of(['F0rec', 'E', 'N'], pops_all)

    # ---- full sample points
    ones = np.ones((1, n_run))
    D0, nd0 = eval_W(dsA, ones)
    st0 = hyp_stats(D0)
    theta = {k: float(st0[k][0]) for k in STATS}
    Dfull = D0[0]
    log('full sample: D(E) %.9g R_gl %.9g c %.9g cdiff %.9g r %.9g' % (Dfull[1], theta['R_gl'], theta['c'], theta['cdiff'], theta['r']))
    # alternative u definition (diagnostic only)
    alt = {}
    try:
        crit_alt = dict(crit)
        crit_alt['E5'] = make_oracle(cF_list, counts, u_alt, m_dr, A_dr)
        crit_alt['E5p'] = make_oracle(cF_list, counts, permute_u(u_alt, counts), m_dr, A_dr)
        crit_bak = crit
        dsAlt = DataSet(['F0', 'E', 'E5', 'E5p', 'N'], [build_source(runs, crit_alt[nm], pops_all) for nm in ['F0', 'E', 'E5', 'E5p', 'N']])
        sta = hyp_stats(eval_W(dsAlt, ones)[0])
        alt = dict(note="u_i = (rank - 0.5)/n_valid (n = decisions that have an r_i), instead of n = all evaluated decisions",
                   c=float(sta['c'][0]), cdiff=float(sta['cdiff'][0]))
    except Exception as e:                                                  # diagnostic only
        alt = dict(error=repr(e))

    # ---- bootstrap (single level)
    Wb = L.boot_counts(n_run, nboot, SEEDS['boot'])
    t = time.time()
    DB, nB = eval_W(dsA, Wb)
    sb = hyp_stats(DB)
    log('bootstrap main: %d resamples (%.1f s); finite D(E) in %.4f' % (nboot, time.time() - t, np.mean(np.isfinite(DB[:, 1]))))
    share_pos = float(np.mean(DB[:, 1] > 0))
    if dsI is not None:
        DIb, nIb = eval_W(dsI, Wb)
        DI0, nI0 = eval_W(dsI, ones)
        sI = hyp_stats(np.column_stack([DIb[:, :2], DIb[:, 2], DIb[:, 2], DIb[:, 3]]))
        sI0 = hyp_stats(np.column_stack([DI0[:, :2], DI0[:, 2], DI0[:, 2], DI0[:, 3]]))
    DRb, _ = eval_W(dsR, Wb)
    DR0, _ = eval_W(dsR, ones)
    with np.errstate(invalid='ignore', divide='ignore'):
        rec_b = np.where(np.isfinite(DRb[:, 1]) & (DRb[:, 1] > 0), DRb[:, 2] / DRb[:, 1], np.nan)
        rec_0 = float(DR0[0, 2] / DR0[0, 1]) if (np.isfinite(DR0[0, 1]) and DR0[0, 1] > 0) else float('nan')

    # ---- calibration
    outer_idx = np.random.default_rng(SEEDS['outer']).integers(0, n_run, (nout, n_run))
    mc_idx = np.random.default_rng(SEEDS['mc']).integers(0, nout, (nmc, nout))
    need_all = np.ones(len(dsA.names), dtype=bool)
    t = time.time()
    res1 = double_boot(dsA, need_all, n_run, SEEDS['inner1'], nout, ninn, theta, outer_idx)
    log('double bootstrap seed 1 done (%.1f s)' % (time.time() - t))
    cal1 = {k: calib_one(res1[k], nout, mc_idx) for k in STATS}
    need2 = [k for k in STATS if cal1[k].get('needs_checks')]
    cal2 = {}
    if need2:
        t = time.time()
        res2 = double_boot(dsA, need_all, n_run, SEEDS['inner2'], nout, ninn, theta, outer_idx)
        log('double bootstrap seed 2 done (%.1f s)' % (time.time() - t))
        cal2 = {k: calib_one(res2[k], nout, mc_idx) for k in STATS}
    final = {}
    for k in STATS:
        c1 = cal1[k]
        why = ''
        if c1['n_kept'] == 0 or c1['coverage'] is None:
            lvl, why = 0.99, 'no valid outer sample: nominal 99%'
        elif c1['cov95'] >= 0.94:
            lvl, why = 0.95, 'nominal 95%% (coverage %.4f >= 0.94)' % c1['cov95']
        else:
            cand = c1['level_stage1']
            if cand is None:
                lvl, why = 0.99, 'no level reaches coverage 0.95: nominal 99%'
            else:
                sd_ok = c1['mc_sd'] <= 0.002 + 1e-12
                c2 = cal2.get(k)
                l2 = choose_level(np.array(c2['coverage'])) if (c2 and c2.get('coverage')) else None
                agree = (l2 is not None) and abs(l2 - cand) <= 0.002 + 1e-9
                if sd_ok and agree:
                    lvl, why = cand, 'calibrated level %.4f (MC SD %.5f, second seed level %.4f)' % (cand, c1['mc_sd'], l2)
                else:
                    lvl, why = 0.99, 'calibrated candidate %.4f rejected (MC SD %.5f ok=%s; second seed level %s agrees=%s): nominal 99%%' % (
                        cand, c1['mc_sd'], sd_ok, l2, agree)
        final[k] = dict(level=float(lvl), why=why, second_seed_level=(choose_level(np.array(cal2[k]['coverage'])) if (k in cal2 and cal2[k].get('coverage')) else None))
        log('level', k, lvl, why)

    # ---- values
    R, c_, cd_, r_ = theta['R_gl'], theta['c'], theta['cdiff'], theta['r']
    lv = {k: final[k]['level'] for k in STATS}
    ci = {k: ci_at(sb[k], lv[k]) for k in STATS}
    with np.errstate(invalid='ignore', divide='ignore'):
        eff_b = np.where(np.isfinite(sb['c']) & (sb['c'] != 0), sb['r'] / sb['c'], np.nan)
    # class
    r_lo, c_lo, c_hi = ci['r'][0], ci['c'][0], ci['c'][1]
    if r_lo > 0:
        cls = 'recovers'
    elif c_lo > DELTA:
        cls = 'uninformative variation'
    elif (c_lo > -DELTA) and (c_hi < DELTA):
        cls = 'amplitude-limited'
    else:
        cls = 'inconclusive'
    dr0 = bool((ci['R_gl'][0] > 0) and (share_pos >= 0.975))
    dr1 = bool((ci['c'][0] > 0) and (ci['cdiff'][0] > 0))
    dr2 = cls in ('recovers', 'uninformative variation', 'amplitude-limited')
    with np.errstate(invalid='ignore', divide='ignore'):
        eff = float(r_ / c_) if (np.isfinite(c_) and c_ != 0) else float('nan')
    barely = bool(rs_all['within5'] >= 0.95)
    dec_eq_b = np.where(np.isfinite(DB[:, 1]), DB[:, 1] / NLEV / 100. * nB, np.nan)
    vals = {}
    vals['DR.n_runs'] = float(n_run)
    vals['DR.n_dec'] = float(n_dec)
    vals['DR.n_in_dropout'] = float(n_in)
    vals['DR.R_gl'] = float(R)
    vals['DR.R_gl.ci'] = ci['R_gl']
    vals['DR.R_gl.level'] = lv['R_gl']
    vals['DR.R_gl.share_pos'] = share_pos
    vals['DR.R_deceq'] = float(L.dec_eq(Dfull[1], n_dec))
    vals['DR.R_deceq.ci'] = ci_at(dec_eq_b, 0.95)
    vals['DR.c'] = float(c_)
    vals['DR.c.ci'] = ci['c']
    vals['DR.c.level'] = lv['c']
    vals['DR.cdiff'] = float(cd_)
    vals['DR.cdiff.ci'] = ci['cdiff']
    vals['DR.cdiff.level'] = lv['cdiff']
    vals['DR.r'] = float(r_)
    vals['DR.r.ci'] = ci['r']
    vals['DR.r.level'] = lv['r']
    vals['DR.eff'] = eff if cls == 'recovers' else None
    vals['DR.eff.ci'] = ci_at(eff_b, lv['r']) if cls == 'recovers' else None
    vals['DR.m'] = float(m_dr)
    vals['DR.A'] = float(A_dr)
    vals['DR.within5'] = float(rs_all['within5'])
    vals['DR.barely_varies'] = barely
    vals['DR.DR0.passes'] = dr0
    vals['DR.DR1.passes'] = dr1
    vals['DR.DR2.class'] = cls
    vals['DR.DR2.passes'] = bool(dr2)
    if dsI is not None:
        vals['DR.in.R_gl'] = float(sI0['R_gl'][0])
        vals['DR.in.R_gl.ci'] = ci_at(sI['R_gl'], 0.95)
        vals['DR.in.RR_N'] = float(sI0['r'][0])
        vals['DR.in.RR_N.ci'] = ci_at(sI['r'], 0.95)
        vals['DR.in.c'] = float(sI0['c'][0])
        vals['DR.in.c.ci'] = ci_at(sI['c'], 0.95)
    else:
        for kx in ('DR.in.R_gl', 'DR.in.RR_N', 'DR.in.c'):
            vals[kx] = float('nan')
            vals[kx + '.ci'] = [float('nan'), float('nan')]
    vals['DR.in.within5'] = float(rs_in['within5'])
    vals['DR.rec.RR_N'] = rec_0
    vals['DR.rec.RR_N.ci'] = ci_at(rec_b, 0.95)
    vals['DR.dec_in_share'] = float(n_in / n_dec) if n_dec else float('nan')
    if pb is not None:
        vals['DR.pbar.vehicle'] = pb['vehicle']
        vals['DR.pbar.pedestrian'] = pb['pedestrian']
        vals['DR.pbar.cnt_vehicle'] = pb['cnt_vehicle']
        vals['DR.pbar.cnt_pedestrian'] = pb['cnt_pedestrian']
    else:
        for kx in ('vehicle', 'pedestrian', 'cnt_vehicle', 'cnt_pedestrian'):
            vals['DR.pbar.' + kx] = float('nan')
    vals['DR.masks_identical'] = bool(ident)

    # ---- details
    age_counts = np.bincount(np.concatenate([r['dr_age'][r['dr_masked']] for r in runs]) if n_in else np.zeros(0, dtype=int), minlength=4)
    details = dict(
        mode=dict(test_old=test, quick=quick, nboot=nboot, nout=nout, ninn=ninn, nmc=nmc, numba=HAVE_NUMBA),
        run_ids_first_last=[ids[0], ids[-1]], seeds=SEEDS, delta=DELTA,
        confirmed=dict(DR0=dr0, DR1=bool(dr0 and dr1), DR2=bool(dr0 and dr1 and dr2)),
        theta=theta, full_D=[fl(x) for x in Dfull], share_D_pos=share_pos,
        n_resamples_finite_D=int(np.isfinite(DB[:, 1]).sum()), n_resamples_D_le0=int((~(DB[:, 1] > 0)).sum()),
        ratio_summary_all=rs_all, ratio_summary_in=rs_in, n_decisions_without_rank_rows=n_no_rows,
        alt_u_valid_n=alt, des_nonconstant_runs=des_nonconst,
        masks=mask_report, mask_shares=shares,
        evaluated_decisions_masked_share=float(n_in / n_dec) if n_dec else None,
        in_dropout_by_dr_age={str(i): int(age_counts[i]) for i in range(len(age_counts))},
        rec=dict(point=rec_0, DR_vs_DRrec_same={k: all((r['same_rec'].get(k) in (True, None)) for r in runs) for k in ('cE', 'cN', 'clear', 'vbar', 'idx55', 'k', 'dr_masked', 'dr_age')},
                 cE_cN_equal_in_rec_file=all(np.array_equal(r['cE'], r['cE_rec'], equal_nan=True) and np.array_equal(r['cN'], r['cN_rec'], equal_nan=True) for r in runs)),
        calibration=dict(seed1=cal1, seed2=cal2 if cal2 else None, final=final, levels_grid=LEVELS_NOM),
        pbar=dict(n_files=(pb or {}).get('n_files'), names_first_last=(pb or {}).get('files_first_last')),
        note_option2_lead_absent_share='not computed (option 2 only; needs the tracker outputs)',
        lock=str(LOCK), library=str(_lib / 'optA_lib_v02.py'), library_sha256=L.sha256_file(_lib / 'optA_lib_v02.py'),
        code_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(), seconds=time.time() - T_START)
    doc = dict(values=vals, details=details)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(doc, indent=1, allow_nan=True, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o)), encoding='utf-8')
    log('wrote', outp)


if __name__ == '__main__':
    main()
