"""DR recount (second program), AMENDMENT_12 section 3a extension v01: replication at p = 0.10, dose-response over p, decomposition.
Built from the v02 recount of A11 section 6c (same logic) and A12_3a_DR_REPLICATION_v02.md.

Written 21 Nov 2026 from the TEXT of A11_6c_DROPOUT_SPEC_v02.md (6c.4-6c.8) and A12_3a_DR_REPLICATION_v02.md, AMENDMENT_10_v13.md section 2 and 5.3, and the
definitions files CD_DEFINITIONS_v13.md / B_*_DEFINITIONS (gridless frontier, calibration details). It does not read or import the
first program. Imports: numpy, the standard library, optA_lib_v02 (frozen scoring library of record: boot_counts, NLEV, dec_eq,
clean_clear, and, for --selfcheck only, frontier / levels_of / curves_w / eval_scoring / select_grid / stats_scored). numba is used when
installed (no fastmath; parallelism only over resamples, each resample is computed by one thread, so results are deterministic).

E5-type oracles are amplitude-matched ranking oracles (never ceilings); c is the amplitude-matched oracle share.
u_i convention of record: mid-rank among the evaluated decisions that have a ratio, divided by n_r = their number; decisions without a ratio keep 0.5.
Usage:  python -I dr_recount_a12_v01.py [--test-old] [--quick] [--threads N] [--nboot N] [--selfcheck] [--out PATH]
Environment: DR_P_ROOT (programme P root or the folder holding optA_lib_v02.py), DR_ROOT (the F_dropout folder), DR_LOCK (lock file, default revision_v13 LOCK_A12a.txt).
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
_ap.add_argument('--outer', type=int, default=None, help='test only: outer count of the double bootstrap (inner stays 1000, MC resamples 2000)')
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

LOCK = pathlib.Path(os.environ.get('DR_LOCK', str(ROOT.parent.parent / 'LOCK_A12a.txt')))

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
def make_mask(case_id, n, p=0.10):
    """6c.4 (v02, the one mask law): rng = default_rng(int.from_bytes(sha256(('A11/D/' + case_id).encode('utf-8')).digest()[:8], 'big')),
    case_id = the protocol case id. Rows i = 0..n-1; row 0 never masked; from row 1: at a row not inside a window draw u = rng.random();
    if u < 0.10 draw Ln = rng.integers(1, 4) and mask rows i..i+Ln-1 (cut at n-1); the row right after the window (i+Ln) is the gap
    row: never masked, draws nothing, draws resume at i+Ln+1. Otherwise i += 1. Returns (masked rows, gap rows)."""
    rng = np.random.default_rng(int.from_bytes(hashlib.sha256(('A11/D/' + case_id).encode('utf-8')).digest()[:8], 'big'))
    masked, gaps = [], []
    i = 1
    while i < n:
        u = rng.random()
        if u < p:
            Ln = int(rng.integers(1, 4))
            for j in range(i, min(i + Ln, n)):
                masked.append(j)
            if i + Ln < n:
                gaps.append(i + Ln)
            i += Ln + 1
        else:
            i += 1
    return masked, gaps


def case_of_run(rid):
    """Fresh run pc13_<case>_native -> <case>."""
    if rid.startswith('pc13_') and rid.endswith('_native'):
        return rid[len('pc13_'):-len('_native')]
    return None


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
        r['dr_gap_all'] = np.asarray(a['dr_gap']).astype(bool) if 'dr_gap' in a else np.zeros(len(ev), bool)
        r['has_gap_key'] = 'dr_gap' in a
        r['dr_gap'] = r['dr_gap_all'][ev]
        r['lead_found_all'] = np.asarray(a['lead_found']).astype(bool) if 'lead_found' in a else None
        r['track_id_all'] = np.asarray(a['track_id']).astype(int) if 'track_id' in a else None
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
def double_boot(evalfn, names, n_run, inner_seed, nout, ninn, theta, outer_idx):
    """Per statistic name: arrays p_lt, p_le, kept (over the outer samples). evalfn(W) -> dict name -> array over the rows of W.
    theta: dict name -> full-sample value."""
    rng = np.random.default_rng(inner_seed)
    Wout = np.zeros((nout, n_run))
    for b in range(nout):
        Wout[b] = np.bincount(outer_idx[b], minlength=n_run)
    own = evalfn(Wout)
    res = {k: dict(p_lt=np.full(nout, np.nan), p_le=np.full(nout, np.nan), kept=np.zeros(nout, dtype=bool)) for k in names}
    base = np.arange(ninn)[:, None] * n_run
    t_start = time.time()
    for b in range(nout):
        ii = rng.integers(0, n_run, (ninn, n_run))
        want = [k for k in names if np.isfinite(theta[k]) and np.isfinite(own[k][b])]
        if not want:
            continue
        runs_b = outer_idx[b][ii]
        W = np.bincount((runs_b + base).ravel(), minlength=ninn * n_run).reshape(ninn, n_run).astype(np.float64)
        v = evalfn(W)
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


def calibrate(evalfn, names, n_run, theta, nout, ninn, nmc, outer_idx, mc_idx):
    """A10 2.6 for the statistics in names: seed 1, seed 2 only if some statistic needs the checks. Returns (cal1, cal2, final)."""
    res1 = double_boot(evalfn, names, n_run, SEEDS['inner1'], nout, ninn, theta, outer_idx)
    cal1 = {k: calib_one(res1[k], nout, mc_idx) for k in names}
    cal2 = {}
    if any(cal1[k].get('needs_checks') for k in names):
        res2 = double_boot(evalfn, names, n_run, SEEDS['inner2'], nout, ninn, theta, outer_idx)
        cal2 = {k: calib_one(res2[k], nout, mc_idx) for k in names}
    final = {}
    for k in names:
        c1 = cal1[k]
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
                    lvl, why = cand, 'calibrated level %.4f (MC SD %.5f, second seed level %s)' % (cand, c1['mc_sd'], l2)
                else:
                    lvl, why = 0.99, 'calibrated candidate %.4f rejected (MC SD %.5f ok=%s; second seed level %s agrees=%s): nominal 99%%' % (
                        cand, c1['mc_sd'], sd_ok, l2, agree)
        final[k] = dict(level=float(lvl), why=why, second_seed_level=(choose_level(np.array(cal2[k]['coverage'])) if (k in cal2 and cal2[k].get('coverage')) else None))
        log('level', k, lvl, why)
    return cal1, cal2, final


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


def e5_u_vec(gF, gE, n_mode='valid'):
    """u_i = (mid-rank of r_i - 0.5) / n; r_i = median over rows with finite positive g*_F0 and g*_E of (g*_F0 / g*_E)^(1/2);
    decisions without such rows get 0.5. Convention of record (n_mode 'valid', default): mid-rank among the decisions that have an r_i and
    n = n_r = the number of evaluated decisions that have an r_i. n_mode 'all' (diagnostic only): n = number of evaluated decisions."""
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


# ------------------------------------------------------------------------------------------------ A12 3a: layout, masks per p, dose, decomposition
PTAGS = ['p005', 'p010', 'p020', 'p030']
PVALS = [0.05, 0.10, 0.20, 0.30]


def layout(ptag, test):
    if test:
        b = ROOT / 'out_a12' / ('testold_' + ptag)
        return dict(DR=b / 'DR', DRrec=b / 'DRrec', ID3=b / 'ID3', pbar=b / 'pbar', masks=None)
    b = ROOT / 'out_a12' / ptag
    return dict(DR=b / 'arrays' / 'DR', DRrec=b / 'arrays' / 'DRrec', ID3=b / 'arrays' / 'ID3', pbar=b / 'pbar',
                masks=b / ('DR_MASKS_%s.json' % ptag))


def verify_masks(runs, pv, maskfile, pbar_names, test):
    """Identity check (iii) at start probability pv: every run's mask regenerated from its case id and n_det_rows is compared with
    meta['masked'], with dr_masked / dr_gap at dr_frame, and (when the file exists) with the mask file."""
    ids = [r['id'] for r in runs]
    ident, bad = True, []
    for r in runs:
        cid = r['meta'].get('case_id') or case_of_run(r['id'])
        if cid is None:
            raise SystemExit('no case id for %s' % r['id'])
        mk, gp = make_mask(cid, int(r['meta']['n_det_rows']), pv)
        if r['meta'].get('masked') is not None and [int(x) for x in r['meta']['masked']] != mk:
            ident = False
            bad.append((r['id'], 'meta masked differs'))
        if r['dr_frame_all'] is not None:
            if not np.array_equal(np.isin(r['dr_frame_all'], np.array(mk, dtype=int)), r['dr_masked_all']):
                ident = False
                bad.append((r['id'], 'dr_masked differs from the mask at dr_frame'))
            if r['has_gap_key'] and not np.array_equal(np.isin(r['dr_frame_all'], np.array(gp, dtype=int)), r['dr_gap_all']):
                ident = False
                bad.append((r['id'], 'dr_gap differs from the gap rows at dr_frame'))
    shares = {}
    if maskfile is not None and pathlib.Path(maskfile).exists():
        mf = json.loads(pathlib.Path(maskfile).read_text(encoding='utf-8'))
        if sorted(mf['fresh'].keys()) != ids:
            ident = False
            bad.append(('fresh', 'run ids differ from the mask file'))
        tot = dict(fresh=[0, 0], tuning=[0, 0])
        for part in ('fresh', 'tuning'):
            for rid, e in (mf.get(part) or {}).items():
                mk, _ = make_mask(e['case_id'], int(e['n']), pv)
                if part == 'fresh' and e['case_id'] != case_of_run(rid):
                    ident = False
                    bad.append((rid, 'case_id differs from the run id'))
                if [int(x) for x in e['masked']] != mk:
                    ident = False
                    bad.append((rid, 'masked frames differ from the mask file'))
                tot[part][0] += len(mk)
                tot[part][1] += int(e['n'])
        if mf.get('tuning') and pbar_names is not None and sorted(mf['tuning'].keys()) != sorted(pbar_names):
            ident = False
            bad.append(('tuning', 'pbar archive names differ from the mask file tuning ids'))
        for part in ('fresh', 'tuning'):
            if tot[part][1]:
                shares[part + '_frames'] = dict(masked=tot[part][0], frames=tot[part][1], share=tot[part][0] / tot[part][1])
    elif not test and pv == 0.10:
        raise SystemExit('mask file %s missing' % maskfile)
    return ident, bad, shares


def slope_of(rm):
    """OLS slope of r on p over the four p (columns of rm; rows are resamples): b = sum (p - pbar)(r - rbar) / sum (p - pbar)^2;
    NaN if any r is NaN."""
    pc = np.array(PVALS) - np.mean(PVALS)
    rbar = rm.mean(axis=1, keepdims=True)
    return ((rm - rbar) * pc[None, :]).sum(axis=1) / np.sum(pc ** 2)


def r_of(D):
    den = D[:, 1]
    with np.errstate(invalid='ignore', divide='ignore'):
        return np.where(np.isfinite(den) & (den > 0), D[:, 2] / den, np.nan)


def run_dose(runs10, ids, Wb, ones, n_run, nout, ninn, nmc, outer_idx, mc_idx, test, ident10):
    vals, det = {}, {}
    ident_all = ident10
    dss, rb_list, r0_list = {}, [], []
    pbars = {}
    for tag, pv in zip(PTAGS, PVALS):
        lay = layout(tag, test)
        if tag == 'p010':
            rr = runs10
        else:
            rr = load_runs(lay['DR'], lay['DRrec'])
            if [r['id'] for r in rr] != ids:
                raise SystemExit('run set at %s differs from p010' % tag)
        pbt = pbar_dr(lay['pbar']) if pathlib.Path(lay['pbar']).exists() else None
        if tag != 'p010':
            idt, badt, _ = verify_masks(rr, pv, lay['masks'], (pbt or {}).get('names'), test)
            ident_all = ident_all and idt
            det['masks_' + tag] = dict(identical=idt, mismatches=badt[:20])
        pbars[tag] = None if pbt is None else dict(vehicle=pbt['vehicle'], pedestrian=pbt['pedestrian'], cnt_vehicle=pbt['cnt_vehicle'],
                                                   cnt_pedestrian=pbt['cnt_pedestrian'], n_files=pbt['n_files'])
        pop = [np.ones(int(r['clear1'].shape[0]), dtype=bool) for r in rr]
        crit = dict(F0=[r['cF0'] for r in rr], E=[r['cE'] for r in rr], N=[r['cN'] for r in rr])
        ds = DataSet(['F0', 'E', 'N'], [build_source(rr, crit[nm], pop) for nm in ['F0', 'E', 'N']])
        dss[tag] = ds
        Db, _ = eval_W(ds, Wb)
        D0, _ = eval_W(ds, ones)
        rb, r0 = r_of(Db), float(r_of(D0)[0])
        Rb, R0 = Db[:, 1] / NLEV, float(D0[0, 1] / NLEV)
        rb_list.append(rb)
        r0_list.append(r0)
        vals['DR.r_' + tag] = r0
        vals['DR.r_%s.ci' % tag] = ci_at(rb, 0.95)
        vals['DR.R_' + tag] = R0
        vals['DR.R_%s.ci' % tag] = ci_at(Rb, 0.95)
        vals['DR.masked_share_' + tag] = float(sum(len(r['meta']['masked']) for r in rr) / sum(int(r['meta']['n_det_rows']) for r in rr))
        det['n_dec_' + tag] = int(sum(int(r['clear1'].shape[0]) for r in rr))
        if tag != 'p010':
            del rr
    rmat_b = np.column_stack(rb_list)
    rvec0 = np.array(r0_list)
    b_b = slope_of(rmat_b)
    b0 = float(slope_of(rvec0[None, :])[0])
    vals['DR.slope.p'] = float((1 + int(np.sum(~(b_b > 0)))) / (len(Wb) + 1))

    def ev_slope(W):
        cols = [r_of(eval_W(dss[t], W)[0]) for t in PTAGS]
        return dict(slope=slope_of(np.column_stack(cols)))
    cal1, cal2, final = calibrate(ev_slope, ['slope'], n_run, dict(slope=b0), nout, ninn, nmc, outer_idx, mc_idx)
    lv = final['slope']['level']
    ci = ci_at(b_b, lv)
    vals['DR.slope'] = b0
    vals['DR.slope.ci'] = ci
    vals['DR.slope.level'] = lv
    vals['DR.slope.passes'] = bool(ci[0] > 0)
    # Spearman rho of (p, r(p)) on the full sample (mid-ranks, Pearson correlation of the ranks)
    if np.all(np.isfinite(rvec0)):
        rp = midranks(np.array(PVALS))
        rq = midranks(rvec0)
        sd = np.std(rp) * np.std(rq)
        vals['DR.spearman'] = float(np.mean((rp - rp.mean()) * (rq - rq.mean())) / sd) if sd > 0 else float('nan')
    else:
        vals['DR.spearman'] = float('nan')
    det['slope_calibration'] = dict(seed1=cal1, seed2=cal2 if cal2 else None, final=final)
    det['pbar_by_p'] = pbars
    det['slope_resamples_nan_or_le0'] = int(np.sum(~(b_b > 0)))

    # ---- decomposition at p = 0.10 (3a.5)
    parts = {k: [] for k in ('in', 'reacq', 'steady')}
    for r in runs10:
        fr = r['dr_frame_all'][r['ev']]
        mk = np.array([int(x) for x in r['meta']['masked']], dtype=int)
        inn = np.isin(fr, mk)
        rea = (~inn) & (np.isin(fr - 1, mk) | np.isin(fr - 2, mk))
        ste = ~inn & ~rea
        parts['in'].append(inn)
        parts['reacq'].append(rea)
        parts['steady'].append(ste)
    crit = dict(F0=[r['cF0'] for r in runs10], E=[r['cE'] for r in runs10], N=[r['cN'] for r in runs10])
    for k in parts:
        crit['N_' + k] = [np.where(parts[k][i][:, None], runs10[i]['cN'], runs10[i]['cF0']) for i in range(len(runs10))]
    names = ['F0', 'E', 'N', 'N_in', 'N_reacq', 'N_steady']
    pop = [np.ones(int(r['clear1'].shape[0]), dtype=bool) for r in runs10]
    dsd = DataSet(names, [build_source(runs10, crit[nm], pop) for nm in names])
    Db, nb = eval_W(dsd, Wb)
    D0, n0 = eval_W(dsd, ones)
    den_b, den0 = Db[:, 1], D0[0, 1]
    with np.errstate(invalid='ignore', divide='ignore'):
        ok_b = np.isfinite(den_b) & (den_b > 0)
        rr_b = {nm: np.where(ok_b, Db[:, i] / den_b, np.nan) for i, nm in enumerate(names) if i >= 2}
        ok0 = bool(np.isfinite(den0) and den0 > 0)
        rr_0 = {nm: (float(D0[0, i] / den0) if ok0 else float('nan')) for i, nm in enumerate(names) if i >= 2}
    vals['DR.dec.r'] = rr_0['N']
    vals['DR.dec.r.ci'] = ci_at(rr_b['N'], 0.95)
    for i, (k, nm) in enumerate((('in', 'N_in'), ('reacq', 'N_reacq'), ('steady', 'N_steady'))):
        col = 3 + i
        vals['DR.dec.' + k] = rr_0[nm]
        vals['DR.dec.%s.ci' % k] = ci_at(rr_b[nm], 0.95)
        vals['DR.dec.%s.deceq' % k] = float(L.dec_eq(D0[0, col], n0[0]))
        vals['DR.dec.%s.deceq.ci' % k] = ci_at(np.where(np.isfinite(Db[:, col]), Db[:, col] / NLEV / 100. * nb, np.nan), 0.95)
        vals['DR.dec.%s.n' % k] = float(sum(int(x.sum()) for x in parts[k]))
    rest_b = rr_b['N'] - rr_b['N_in'] - rr_b['N_reacq'] - rr_b['N_steady']
    vals['DR.dec.rest'] = rr_0['N'] - (rr_0['N_in'] + rr_0['N_reacq'] + rr_0['N_steady'])
    vals['DR.dec.rest.ci'] = ci_at(rest_b, 0.95)
    return vals, det, ident_all


# ------------------------------------------------------------------------------------------------ main
def main():
    test = ARGS.test_old
    quick = ARGS.quick
    if not test:
        if not LOCK.exists():
            raise SystemExit('REFUSED: %s does not exist (non-test mode needs the lock)' % LOCK)
        if quick:
            raise SystemExit('--quick is for --test-old only')
    lay10 = layout('p010', test)
    dirDR, dirREC, dirP = lay10['DR'], lay10['DRrec'], lay10['pbar']
    outp = pathlib.Path(ARGS.out) if ARGS.out else ROOT / 'recount' / ('TESTOLD_DR2_RECOUNT_v01.json' if test else 'DR2_RECOUNT_v01.json')
    if outp.exists():
        raise SystemExit('REFUSED: %s exists' % outp)
    nboot = ARGS.nboot if ARGS.nboot else (2000 if quick else 20000)
    nout, ninn, nmc = (200, 100, 200) if quick else (2000, 1000, 2000)
    if ARGS.outer:
        if not test:
            raise SystemExit('--outer is for --test-old only')
        nout, ninn, nmc = ARGS.outer, 1000, 2000

    log('numba', HAVE_NUMBA, 'threads', (numba.get_num_threads() if HAVE_NUMBA else 1), 'test', test, 'quick', quick, 'nboot', nboot)
    runs = load_runs(dirDR, dirREC)
    n_run = len(runs)
    if not test:
        mf10 = json.loads(lay10['masks'].read_text(encoding='utf-8'))
        if sorted(mf10['fresh'].keys()) != [r['id'] for r in runs]:
            raise SystemExit('the arrays at p010 are not the runs of %s' % lay10['masks'])
    ids = [r['id'] for r in runs]
    log('runs', n_run, 'first', ids[0], 'last', ids[-1])
    if ARGS.selfcheck:
        selfcheck(runs)
        return

    # ---- masks at p = 0.10 (identity check iii); the other p are checked inside run_dose
    pb = pbar_dr(dirP) if pathlib.Path(dirP).exists() else None
    if not test and pb is None:
        raise SystemExit('no pbar files in %s' % dirP)
    ident, bad, shares = verify_masks(runs, 0.10, lay10['masks'], (pb or {}).get('names'), test)
    mask_report = dict(mode='regenerated from the case id (p = 0.10) and compared with meta masked and the mask file', identical=ident, mismatches=bad[:20])
    mask_by_run = {r['id']: [int(x) for x in r['meta']['masked']] for r in runs}
    if test:
        tm = sum(len(v) for v in mask_by_run.values())
        tf = sum(int(r['meta']['n_det_rows']) for r in runs)
        shares = dict(test_runs_frames=dict(masked=tm, frames=tf, share=tm / tf))
    log('masks identical at p010:', ident, bad[:3])

    # ---- populations and sources
    counts = [int(r['clear1'].shape[0]) for r in runs]
    n_dec = int(sum(counts))
    pops_all = [np.ones(c, dtype=bool) for c in counts]
    pops_in = [r['dr_masked'].copy() for r in runs]
    pops_ig = [r['dr_masked'] | r['dr_gap'] for r in runs]
    n_ig = int(sum(int(p.sum()) for p in pops_ig))
    n_gap = int(sum(int(r['dr_gap'].sum()) for r in runs))
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
    u, n_no_rows = e5_u_vec(gF, gE, 'valid')
    u_alt, _ = e5_u_vec(gF, gE, 'all')
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
    dsIG = ds_of(['F0', 'E', 'E5', 'N'], pops_ig) if n_ig > 0 else None
    dsR = ds_of(['F0rec', 'E', 'N'], pops_all)
    # output rule without masks (punish_num = 3, empty masks, P-bar of record): arrays ID3
    dirID3 = lay10['ID3']
    dsR3 = None
    ref3_note = None
    if dirID3.exists() and list(dirID3.glob('*.npz')):
        runs3 = load_runs(dirID3, dirID3)
        if [r['id'] for r in runs3] != ids:
            raise SystemExit('ID3 run set differs from DR')
        ref3_note = dict(evaluated_equal_DR=all(np.array_equal(a['ev'], b['ev']) for a, b in zip(runs, runs3)))
        p3 = [np.ones(int(r['clear1'].shape[0]), dtype=bool) for r in runs3]
        c3 = dict(F0=[r['cF0'] for r in runs3], E=[r['cE'] for r in runs3], N=[r['cN'] for r in runs3])
        dsR3 = DataSet(['F0', 'E', 'N'], [build_source(runs3, c3[nm], p3) for nm in ['F0', 'E', 'N']])
    # re-association counts (decisions in array order, all decisions)
    reas = {}
    for X in ('in', 'gap'):
        reas[X] = dict(n=0, lead_found=0, new_track=0, no_pre_lead=0)
    for r in runs:
        lf, tid = r['lead_found_all'], r['track_id_all']
        if lf is None or tid is None:
            reas = None
            break
        pre = None
        for i in range(len(r['ev'])):
            mk_, gp_ = bool(r['dr_masked_all'][i]), bool(r['dr_gap_all'][i])
            if not mk_ and not gp_:
                pre = int(tid[i]) if lf[i] else None
                continue
            if not r['ev'][i]:
                continue
            for X, flag in (('in', mk_), ('gap', gp_)):
                if not flag:
                    continue
                reas[X]['n'] += 1
                if lf[i]:
                    reas[X]['lead_found'] += 1
                    if pre is None:
                        reas[X]['no_pre_lead'] += 1
                    elif int(tid[i]) != pre:
                        reas[X]['new_track'] += 1

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
        alt = dict(note="diagnostic: u_i = (rank - 0.5)/n with n = ALL evaluated decisions (previous reading), instead of n_r = decisions that have an r_i",
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
    if dsIG is not None:
        DGb, _ = eval_W(dsIG, Wb)
        DG0, _ = eval_W(dsIG, ones)
        sG = hyp_stats(np.column_stack([DGb[:, :2], DGb[:, 2], DGb[:, 2], DGb[:, 3]]))
        sG0 = hyp_stats(np.column_stack([DG0[:, :2], DG0[:, 2], DG0[:, 2], DG0[:, 3]]))
    if dsR3 is not None:
        D3b, _ = eval_W(dsR3, Wb)
        D30, _ = eval_W(dsR3, ones)
        s3 = hyp_stats(np.column_stack([D3b[:, :2], D3b[:, 1], D3b[:, 1], D3b[:, 2]]))
        s30 = hyp_stats(np.column_stack([D30[:, :2], D30[:, 1], D30[:, 1], D30[:, 2]]))
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
    cal1, cal2, final = calibrate(lambda W: hyp_stats(eval_W(dsA, W, need_all)[0]), STATS, n_run, theta, nout, ninn, nmc, outer_idx, mc_idx)
    log('calibration of the four hypothesis statistics done (%.1f s)' % (time.time() - t))

    # ---- dose-response over p (A12 3a.4) and decomposition (3a.5)
    dose_vals, dose_det, ident_all = run_dose(runs, ids, Wb, ones, n_run, nout, ninn, nmc, outer_idx, mc_idx, test, ident)

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
    vals['DR.n_gap_row'] = float(n_gap)
    if dsIG is not None:
        vals['DR.ig.R_gl'] = float(sG0['R_gl'][0]); vals['DR.ig.R_gl.ci'] = ci_at(sG['R_gl'], 0.95)
        vals['DR.ig.RR_N'] = float(sG0['r'][0]); vals['DR.ig.RR_N.ci'] = ci_at(sG['r'], 0.95)
        vals['DR.ig.c'] = float(sG0['c'][0]); vals['DR.ig.c.ci'] = ci_at(sG['c'], 0.95)
    else:
        for kx in ('DR.ig.R_gl', 'DR.ig.RR_N', 'DR.ig.c'):
            vals[kx] = float('nan'); vals[kx + '.ci'] = [float('nan'), float('nan')]
    for X in ('in', 'gap'):
        for fld in ('n', 'lead_found', 'new_track', 'no_pre_lead'):
            vals['DR.reas.%s.%s' % (X, fld)] = float(reas[X][fld]) if reas else float('nan')
    if dsR3 is not None:
        vals['DR.ref3.R_gl'] = float(s30['R_gl'][0]); vals['DR.ref3.R_gl.ci'] = ci_at(s3['R_gl'], 0.95)
        vals['DR.ref3.RR_N'] = float(s30['r'][0]); vals['DR.ref3.RR_N.ci'] = ci_at(s3['r'], 0.95)
    else:
        for kx in ('DR.ref3.R_gl', 'DR.ref3.RR_N'):
            vals[kx] = float('nan'); vals[kx + '.ci'] = [float('nan'), float('nan')]
    dN_b = np.where(np.isfinite(DB[:, 4]), DB[:, 4] / NLEV / 100. * nB, np.nan)
    vals['DR.D_N_deceq'] = float(L.dec_eq(Dfull[4], n_dec))
    vals['DR.D_N_deceq.ci'] = ci_at(dN_b, 0.95)
    if test:
        vals['DR.masked_share'] = float(sum(len(r['meta']['masked']) for r in runs) / sum(int(r['meta']['n_det_rows']) for r in runs))
    else:
        vals['DR.masked_share'] = float(shares['fresh_frames']['share'])
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
    vals['DR.masks_identical_all'] = bool(ident_all)
    vals['DR.p_r'] = float((1 + int(np.sum(~(sb['r'] > 0)))) / (nboot + 1))
    vals.update(dose_vals)

    # ---- details
    pbar_cmp = None
    pf = ROOT / 'out' / 'PBAR_DR_v01.json'
    if (not test) and pb is not None and pf.exists():
        try:
            fj = json.loads(pf.read_text(encoding='utf-8'))['Pbar']
            pbar_cmp = {cl: float(np.max(np.abs(np.array(fj[cl], float) - np.array(pb[cl], float)))) for cl in ('vehicle', 'pedestrian')}
        except Exception as e:
            pbar_cmp = repr(e)
    age_counts = np.bincount(np.concatenate([r['dr_age'][r['dr_masked']] for r in runs]) if n_in else np.zeros(0, dtype=int), minlength=4)
    details = dict(
        mode=dict(test_old=test, quick=quick, nboot=nboot, nout=nout, ninn=ninn, nmc=nmc, numba=HAVE_NUMBA),
        run_ids_first_last=[ids[0], ids[-1]], seeds=SEEDS, delta=DELTA,
        confirmed=dict(DR0=dr0, DR1=bool(dr0 and dr1), DR2=bool(dr0 and dr1 and dr2)),
        theta=theta, full_D=[fl(x) for x in Dfull], share_D_pos=share_pos,
        n_resamples_finite_D=int(np.isfinite(DB[:, 1]).sum()), n_resamples_D_le0=int((~(DB[:, 1] > 0)).sum()),
        ratio_summary_all=rs_all, ratio_summary_in=rs_in, n_decisions_without_rank_rows=n_no_rows,
        alt_u_all_n=alt, des_nonconstant_runs=des_nonconst,
        masks=mask_report, mask_shares=shares, ref3=ref3_note, n_in_plus_gap=n_ig,
        evaluated_decisions_masked_share=float(n_in / n_dec) if n_dec else None,
        in_dropout_by_dr_age={str(i): int(age_counts[i]) for i in range(len(age_counts))},
        rec=dict(point=rec_0, DR_vs_DRrec_same={k: all((r['same_rec'].get(k) in (True, None)) for r in runs) for k in ('cE', 'cN', 'clear', 'vbar', 'idx55', 'k', 'dr_masked', 'dr_age')},
                 cE_cN_equal_in_rec_file=all(np.array_equal(r['cE'], r['cE_rec'], equal_nan=True) and np.array_equal(r['cN'], r['cN_rec'], equal_nan=True) for r in runs)),
        calibration=dict(seed1=cal1, seed2=cal2 if cal2 else None, final=final, levels_grid=LEVELS_NOM),
        pbar=dict(n_files=(pb or {}).get('n_files'), names_first_last=(pb or {}).get('files_first_last')),
        note_option2_lead_absent_share='not computed (option 2 only; needs the tracker outputs)',
        pbar_vs_PBAR_DR_v01=pbar_cmp, dose=dose_det, masks_identical_p010_only=bool(ident), lock=str(LOCK), library=str(_lib / 'optA_lib_v02.py'), library_sha256=L.sha256_file(_lib / 'optA_lib_v02.py'),
        code_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(), seconds=time.time() - T_START)
    doc = dict(values=vals, details=details)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(doc, indent=1, allow_nan=True, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o)), encoding='utf-8')
    log('wrote', outp)


if __name__ == '__main__':
    main()
