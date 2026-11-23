"""FN5B recount (second program) v01: AMENDMENT_12 section 5b, the DR decision test under injected detection dropouts on the nuScenes val logs.

Written 22 Nov 2026 from the TEXT of A12_5b_TEXT_v01.md, AMENDMENT_10_v13.md sections 2 and 8, CD_DEFINITIONS_v13.md and A11 6c (spec v02), reusing
the statistic machinery of the DR recounts (gridless step frontier, E5 family, bootstrap, A10 2.6 calibration). It does not read or import the
first program (F_dropout_nus\\code, F_nuscenes\\code). Imports: numpy, the standard library, optA_lib_v02 (frozen library of record), numba if installed.

v02 = v01 plus one change (22 Nov 2026, approved before any masked value): the float part of the 5b.4 check (keys within 1e-9, equal NaN patterns)
applies to EVALUATED decisions only, because a CPU-dependent last-bit tie of two equal-cost planner rows moves vbar in an unevaluated decision
(scene-0966, decision 151); the exact-key check stays on all decisions.

--set unmasked : TEST. Recomputes F's unmasked T1 val values of record (scene bootstrap default_rng(20261923)) from F's unmasked val arrays
                 and the clearance of record (cache\\clear_v02), and compares them with out\\ACCEPT3_SCORED_v01.json. Needs no lock.
--set masked   : the section 5b values on the masked val arrays (cache\\arrays_masked\\val). Refuses without revision_v13\\LOCK_A12e.txt.
Usage: python -I fn_recount_v01.py --set unmasked|masked [--threads N] [--nboot N] [--out PATH]
Environment: DR_P_ROOT (programme P root or the folder holding optA_lib_v02.py), FN_ROOT (the F_dropout_nus folder), DR_LOCK (lock file).
"""
import os, sys, json, hashlib, argparse, math, pathlib, time, glob, warnings

# ------------------------------------------------------------------------------------------------ arguments (before numba import)
_ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
_ap.add_argument('--set', choices=['unmasked', 'masked'], required=True)
_ap.add_argument('--threads', type=int, default=0)
_ap.add_argument('--nboot', type=int, default=None)
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
DEFAULT_ROOT = r'ARS_TRIAL\revision_v13\work\F_dropout_nus'
P_ROOT = pathlib.Path(os.environ.get('DR_P_ROOT', DEFAULT_P_ROOT))
ROOT = pathlib.Path(os.environ.get('FN_ROOT', DEFAULT_ROOT))
NUS = ROOT.parent / 'F_nuscenes'
_lib = P_ROOT / '11_ojits' / 'A6R' / 'code'
if not (_lib / 'optA_lib_v02.py').exists():
    _lib = P_ROOT
sys.path.insert(0, str(_lib))
import optA_lib_v02 as L                           # noqa: E402  frozen library of record, read-only

LOCK = pathlib.Path(os.environ.get('DR_LOCK', str(ROOT.parent.parent / 'LOCK_A12e.txt')))

NLEV = L.NLEV                                      # 201
SEEDS = dict(boot=20261923, outer=20261912, inner1=20261913, inner2=20261914, perm=20261915, mc=20261920)
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
    """Fresh run pc13_<case>_native or pl12_<case>_native -> <case>."""
    for pre in ('pc13_', 'pl12_'):
        if rid.startswith(pre) and rid.endswith('_native'):
            return rid[len(pre):-len('_native')]
    return None


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


# ------------------------------------------------------------------------------------------------ nuScenes val data (A12 5b.4)
EXACT_KEYS = ['sweep', 'kf', 'now', 'age', 'idx55', 'evaluated', 'evaluated2', 'inpath', 'n_truth']
TOL_KEYS = ['vbar', 'v0', 'des', 'clear', 'clear2']


def load_arrays(path):
    z = np.load(path, allow_pickle=True)
    return {k: z[k] for k in z.files}


def nan_equal(a, b):
    return bool(np.array_equal(np.isnan(a), np.isnan(b)))


def load_scenes(kind):
    """kind 'unmasked': F's val arrays of record (cache\\arrays_T1\\val); 'masked': cache\\arrays_masked\\val. Clearance: F_nuscenes\\cache\\clear_v02\\val.
    Scenes sorted by name. Checks of 5b.4 (stop on any failure)."""
    ref_dir = NUS / 'cache' / 'arrays_T1' / 'val'
    arr_dir = ref_dir if kind == 'unmasked' else ROOT / 'cache' / 'arrays_masked' / 'val'
    clr_dir = NUS / 'cache' / 'clear_v02' / 'val'
    names = sorted(p.stem for p in ref_dir.glob('*.npz'))
    if sorted(p.stem for p in arr_dir.glob('*.npz')) != names:
        raise SystemExit('scene sets differ between %s and %s' % (ref_dir, arr_dir))
    scenes = []
    checks = dict(exact_keys_equal=True, tol_keys_ok=True, clear_pattern_ok=True, max_abs_tol_keys=0.0, failures=[])
    for nm in names:
        a = load_arrays(arr_dir / (nm + '.npz'))
        c = load_arrays(clr_dir / (nm + '.npz'))
        ev = a['evaluated'].astype(bool)
        if not np.array_equal(a['sweep'], c['sweep']):
            checks['failures'].append((nm, 'sweep differs from clear_v02'))
        if not nan_equal(np.asarray(a['clear'], float), np.asarray(c['clear'], float)):
            checks['failures'].append((nm, 'NaN pattern of clear differs from clear_v02'))
        if kind == 'masked':
            f = load_arrays(ref_dir / (nm + '.npz'))
            for k in EXACT_KEYS:
                if not np.array_equal(a[k], f[k]):
                    checks['exact_keys_equal'] = False
                    checks['failures'].append((nm, 'key %s differs' % k))
            for k in TOL_KEYS:
                x, y = np.asarray(a[k], float)[ev], np.asarray(f[k], float)[ev]      # float part: EVALUATED decisions only
                if not nan_equal(x, y):
                    checks['tol_keys_ok'] = False
                    checks['failures'].append((nm, 'NaN pattern of %s differs' % k))
                else:
                    d = np.nan_to_num(np.abs(np.where(np.isinf(x) | np.isinf(y), 0.0, x - y)))
                    mx = float(d.max()) if d.size else 0.0
                    checks['max_abs_tol_keys'] = max(checks['max_abs_tol_keys'], mx)
                    if mx > 1e-9:
                        checks['tol_keys_ok'] = False
                        checks['failures'].append((nm, 'key %s differs by %.3g' % (k, mx)))
        des = np.asarray(a['des'], float)
        r = dict(id=nm, ev=ev, n_dec=int(len(ev)), des0=float(des[0]), des_const=bool(np.all(des == des[0])))
        r['clear1'] = L.clean_clear(np.asarray(c['clear'], float))[ev]
        r['vbar'] = np.asarray(a['vbar'], float)[ev]
        r['idx55'] = np.asarray(a['idx55'])[ev].astype(int)
        r['cF0'] = np.asarray(a['cF0'], float)[ev]
        r['cE'] = np.asarray(a['cE'], float)[ev]
        r['cN'] = np.asarray(a['cN'], float)[ev]
        r['kf'] = np.asarray(a['kf']).astype(int)[ev]
        r['inpath'] = np.asarray(a['inpath']).astype(bool)[ev]
        r['dr_masked_key'] = (np.asarray(a['dr_masked']).astype(bool)[ev] if 'dr_masked' in a else None)
        scenes.append(r)
    if checks['failures']:
        raise SystemExit('5b.4 checks failed: %s' % checks['failures'][:10])
    return scenes, checks


def ds_of(scenes, crit, names, pops):
    return DataSet(names, [build_source(scenes, crit[nm], pops) for nm in names])


def point_stats(ds, ones):
    D, n = eval_W(ds, ones)
    return D[0], float(n[0])


def run_unmasked():
    outp = pathlib.Path(ARGS.out) if ARGS.out else ROOT / 'recount' / 'FN5B_RECOUNT_unmasked_v01.json'
    if outp.exists():
        raise SystemExit('REFUSED: %s exists' % outp)
    nboot = ARGS.nboot or 20000
    scenes, checks = load_scenes('unmasked')
    n_sc = len(scenes)
    log('scenes', n_sc, 'des constant in all:', all(s['des_const'] for s in scenes))
    crit = dict(F0=[s['cF0'] for s in scenes], E=[s['cE'] for s in scenes], N=[s['cN'] for s in scenes])
    Wb = L.boot_counts(n_sc, nboot, SEEDS['boot'])
    ones = np.ones((1, n_sc))
    vals = {}
    pops = dict(pop0=[np.ones(len(s['clear1']), bool) for s in scenes], pop1=[s['inpath'] for s in scenes])
    for pn, pop in pops.items():
        ds = ds_of(scenes, crit, ['F0', 'E', 'N'], pop)
        D0, n0 = point_stats(ds, ones)
        den = D0[1]
        vals['T1.%s.n' % pn] = n0
        vals['T1.%s.R_pp' % pn] = float(den / NLEV)
        vals['T1.%s.R_deceq' % pn] = float(L.dec_eq(den, n0))
        vals['T1.%s.D_N' % pn] = float(D0[2])
        vals['T1.%s.RR_N' % pn] = float(D0[2] / den) if (np.isfinite(den) and den > 0) else float('nan')
        vals['T1.%s.D_N_deceq' % pn] = float(L.dec_eq(D0[2], n0))
        if pn == 'pop0':
            Db, nb = eval_W(ds, Wb)
            vals['T1.R_ci95'] = ci_at(Db[:, 1] / NLEV, 0.95)
            vals['T1.share_R_nonpositive'] = float(np.mean(~(Db[:, 1] > 0)))
    tgt = json.loads((ROOT / 'out' / 'ACCEPT3_SCORED_v01.json').read_text(encoding='utf-8'))['values']['F']
    cmp = {}
    for pn in ('pop0', 'pop1'):
        for k, kk in (('n', 'n'), ('R_pp', 'R_pp'), ('R_deceq', 'R_deceq'), ('D_N', 'D_N'), ('RR_N', 'RR_N'), ('D_N_deceq', 'D_N_deceq')):
            a, b = vals['T1.%s.%s' % (pn, k)], tgt[pn][kk]
            cmp['%s.%s' % (pn, k)] = dict(recount=a, target=b, diff=(0.0 if (a != a and b != b) else abs(a - b)))
    for j in (0, 1):
        cmp['R_ci95[%d]' % j] = dict(recount=vals['T1.R_ci95'][j], target=tgt['R_ci95'][j], diff=abs(vals['T1.R_ci95'][j] - tgt['R_ci95'][j]))
    cmp['share_R_nonpositive'] = dict(recount=vals['T1.share_R_nonpositive'], target=tgt['share_R_nonpositive'], diff=abs(vals['T1.share_R_nonpositive'] - tgt['share_R_nonpositive']))
    mx = max(v['diff'] for v in cmp.values())
    log('unmasked: max |difference| to the targets = %.3g' % mx)
    doc = dict(values=vals, comparison_with_ACCEPT3=cmp, max_abs_difference=mx, checks=checks, nboot=nboot,
               code_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(), seconds=time.time() - T_START)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(doc, indent=1, allow_nan=True, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o)), encoding='utf-8')
    log('wrote', outp)


def run_masked():
    if not LOCK.exists():
        raise SystemExit('REFUSED: %s does not exist' % LOCK)
    outp = pathlib.Path(ARGS.out) if ARGS.out else ROOT / 'recount' / 'FN5B_RECOUNT_masked_v01.json'
    if outp.exists():
        raise SystemExit('REFUSED: %s exists' % outp)
    nboot = ARGS.nboot or 20000
    nout, ninn, nmc = 2000, 1000, 2000
    scenes, checks = load_scenes('masked')
    n_sc = len(scenes)
    ids = [s['id'] for s in scenes]
    log('scenes', n_sc, 'first', ids[0], 'last', ids[-1], 'checks', {k: v for k, v in checks.items() if k != 'failures'})

    # ---- masks: regenerated from the scene name and the keyframe count (kf_t of the val cache); compared with the mask file
    mf = json.loads((ROOT / 'masks' / 'FN5B_MASKS_v01.json').read_text(encoding='utf-8'))
    ident, bad = True, []
    tot_kf, tot_mk = 0, 0
    masks = {}
    if sorted(mf['scenes'].keys()) != ids:
        ident = False
        bad.append(('scenes', 'scene set differs from the mask file'))
    for s in scenes:
        nm = s['id']
        nkf = int(np.load(NUS / 'cache' / 'val' / (nm + '.npz'), allow_pickle=True)['kf_t'].shape[0])
        mk, _ = make_mask(nm, nkf, 0.10)
        masks[nm] = mk
        e = mf['scenes'].get(nm)
        if e is None or int(e['n_kf']) != nkf or [int(x) for x in e['masked']] != mk:
            ident = False
            bad.append((nm, 'mask or keyframe count differs from the mask file'))
        s['in'] = np.isin(s['kf'], np.array(mk, dtype=int))
        if s['dr_masked_key'] is not None and not np.array_equal(s['dr_masked_key'], s['in']):
            ident = False
            bad.append((nm, 'dr_masked in the arrays differs from the regenerated mask'))
        tot_kf += nkf
        tot_mk += len(mk)
    masked_share = tot_mk / tot_kf
    log('masks identical:', ident, bad[:3], 'masked share of keyframes %.5f (%d / %d)' % (masked_share, tot_mk, tot_kf))

    # ---- populations and sources
    counts = [int(len(s['clear1'])) for s in scenes]
    n_dec = int(sum(counts))
    pops_all = [np.ones(c, dtype=bool) for c in counts]
    pops_in = [s['in'].copy() for s in scenes]
    n_in = int(sum(int(p.sum()) for p in pops_in))
    gF = np.concatenate([s['cF0'] for s in scenes], axis=0)
    gE = np.concatenate([s['cE'] for s in scenes], axis=0)
    gN = np.concatenate([s['cN'] for s in scenes], axis=0)
    inmask = np.concatenate(pops_in)
    rs_all = ratio_summary(ratio_values(gF, gN))
    rs_in = ratio_summary(ratio_values(gF[inmask], gN[inmask]))
    m_n, A_n = rs_all['m'], rs_all['A']
    u, n_no_rows = e5_u_vec(gF, gE, 'valid')
    up = permute_u(u, counts)
    cF_list = [s['cF0'] for s in scenes]
    crit = dict(F0=cF_list, E=[s['cE'] for s in scenes], N=[s['cN'] for s in scenes],
                E5=make_oracle(cF_list, counts, u, m_n, A_n), E5p=make_oracle(cF_list, counts, up, m_n, A_n))
    log('m %.9f A %.9f within5 %.6f; decisions %d, in dropout %d, without rank rows %d' % (m_n, A_n, rs_all['within5'], n_dec, n_in, n_no_rows))
    dsA = ds_of(scenes, crit, ['F0', 'E', 'E5', 'E5p', 'N'], pops_all)
    dsI = ds_of(scenes, crit, ['F0', 'E', 'E5', 'N'], pops_in) if n_in > 0 else None
    log('built source sets: events %s' % dsA.nev)

    ones = np.ones((1, n_sc))
    D0, _ = eval_W(dsA, ones)
    st0 = hyp_stats(D0)
    theta = {k: float(st0[k][0]) for k in STATS}
    Dfull = D0[0]
    log('full sample: D(E) %.9g R_gl %.9g c %.9g cdiff %.9g r %.9g' % (Dfull[1], theta['R_gl'], theta['c'], theta['cdiff'], theta['r']))

    Wb = L.boot_counts(n_sc, nboot, SEEDS['boot'])
    DB, nB = eval_W(dsA, Wb)
    sb = hyp_stats(DB)
    share_pos = float(np.mean(DB[:, 1] > 0))
    if dsI is not None:
        DIb, nIb = eval_W(dsI, Wb)
        DI0, nI0 = eval_W(dsI, ones)
        sI = hyp_stats(np.column_stack([DIb[:, :2], DIb[:, 2], DIb[:, 2], DIb[:, 3]]))
        sI0 = hyp_stats(np.column_stack([DI0[:, :2], DI0[:, 2], DI0[:, 2], DI0[:, 3]]))
    log('single bootstrap done (%d resamples)' % nboot)

    # ---- calibration (A10 2.6)
    outer_idx = np.random.default_rng(SEEDS['outer']).integers(0, n_sc, (nout, n_sc))
    mc_idx = np.random.default_rng(SEEDS['mc']).integers(0, nout, (nmc, nout))
    need_all = np.ones(len(dsA.names), dtype=bool)
    t = time.time()
    cal1, cal2, final = calibrate(lambda W: hyp_stats(eval_W(dsA, W, need_all)[0]), STATS, n_sc, theta, nout, ninn, nmc, outer_idx, mc_idx)
    log('calibration done (%.1f s)' % (time.time() - t))

    # ---- values
    lv = {k: final[k]['level'] for k in STATS}
    ci = {k: ci_at(sb[k], lv[k]) for k in STATS}
    with np.errstate(invalid='ignore', divide='ignore'):
        eff_b = np.where(np.isfinite(sb['c']) & (sb['c'] != 0), sb['r'] / sb['c'], np.nan)
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
    c_, r_ = theta['c'], theta['r']
    with np.errstate(invalid='ignore', divide='ignore'):
        eff = float(r_ / c_) if (np.isfinite(c_) and c_ != 0) else float('nan')
    dec_eq_b = np.where(np.isfinite(DB[:, 1]), DB[:, 1] / NLEV / 100. * nB, np.nan)
    dN_b = np.where(np.isfinite(DB[:, 4]), DB[:, 4] / NLEV / 100. * nB, np.nan)
    vals = {}
    vals['DR.n_runs'] = float(n_sc)
    vals['DR.n_dec'] = float(n_dec)
    vals['DR.n_in_dropout'] = float(n_in)
    vals['DR.dec_in_share'] = float(n_in / n_dec)
    vals['DR.masked_share'] = float(masked_share)
    vals['DR.R_gl'] = theta['R_gl']
    vals['DR.R_gl.ci'] = ci['R_gl']
    vals['DR.R_gl.level'] = lv['R_gl']
    vals['DR.R_gl.share_pos'] = share_pos
    vals['DR.R_gl.share_nonpos'] = float(1.0 - share_pos)
    vals['DR.R_deceq'] = float(L.dec_eq(Dfull[1], n_dec))
    vals['DR.R_deceq.ci'] = ci_at(dec_eq_b, 0.95)
    vals['DR.D_N_deceq'] = float(L.dec_eq(Dfull[4], n_dec))
    vals['DR.D_N_deceq.ci'] = ci_at(dN_b, 0.95)
    vals['DR.c'] = theta['c']
    vals['DR.c.ci'] = ci['c']
    vals['DR.c.level'] = lv['c']
    vals['DR.cdiff'] = theta['cdiff']
    vals['DR.cdiff.ci'] = ci['cdiff']
    vals['DR.cdiff.level'] = lv['cdiff']
    vals['DR.r'] = r_
    vals['DR.r.ci'] = ci['r']
    vals['DR.r.level'] = lv['r']
    vals['DR.eff'] = eff if cls == 'recovers' else None
    vals['DR.eff.ci'] = ci_at(eff_b, lv['r']) if cls == 'recovers' else None
    vals['DR.m'] = float(m_n)
    vals['DR.A'] = float(A_n)
    vals['DR.within5'] = float(rs_all['within5'])
    vals['DR.barely_varies'] = bool(rs_all['within5'] >= 0.95)
    vals['DR.DR0.passes'] = dr0
    vals['DR.DR1.passes'] = dr1
    vals['DR.DR2.class'] = cls
    vals['DR.DR2.passes'] = bool(dr2)
    vals['DR.p_r'] = float((1 + int(np.sum(~(sb['r'] > 0)))) / (nboot + 1))
    if dsI is not None:
        vals['DR.in.R_gl'] = float(sI0['R_gl'][0])
        vals['DR.in.R_gl.ci'] = ci_at(sI['R_gl'], 0.95)
        vals['DR.in.RR_N'] = float(sI0['r'][0])
        vals['DR.in.RR_N.ci'] = ci_at(sI['r'], 0.95)
        vals['DR.in.c'] = float(sI0['c'][0])
        vals['DR.in.c.ci'] = ci_at(sI['c'], 0.95)
        vals['DR.in.R_deceq'] = float(L.dec_eq(DI0[0, 1], nI0[0]))
        vals['DR.in.R_deceq.ci'] = ci_at(np.where(np.isfinite(DIb[:, 1]), DIb[:, 1] / NLEV / 100. * nIb, np.nan), 0.95)
        vals['DR.in.D_N_deceq'] = float(L.dec_eq(DI0[0, 3], nI0[0]))
        vals['DR.in.D_N_deceq.ci'] = ci_at(np.where(np.isfinite(DIb[:, 3]), DIb[:, 3] / NLEV / 100. * nIb, np.nan), 0.95)
    vals['DR.in.within5'] = float(rs_in['within5'])
    vals['DR.in.m'] = float(rs_in['m'])
    vals['DR.in.q05'] = float(rs_in['q05'])
    vals['DR.in.q95'] = float(rs_in['q95'])
    vals['DR.masks_identical'] = bool(ident)
    details = dict(set='masked', nboot=nboot, nout=nout, ninn=ninn, nmc=nmc, seeds=SEEDS, delta=DELTA, numba=HAVE_NUMBA,
                   confirmed=dict(DR0=dr0, DR1=bool(dr0 and dr1), DR2=bool(dr0 and dr1 and dr2)),
                   theta=theta, full_D=[fl(x) for x in Dfull], ratio_summary_all=rs_all, ratio_summary_in=rs_in,
                   n_decisions_without_rank_rows=n_no_rows, masks_mismatches=bad[:20], checks=checks,
                   mask_totals=dict(keyframes=tot_kf, masked=tot_mk),
                   n_resamples_D_le0=int((~(DB[:, 1] > 0)).sum()),
                   calibration=dict(seed1=cal1, seed2=cal2 if cal2 else None, final=final, levels_grid=LEVELS_NOM),
                   lock=str(LOCK), library_sha256=L.sha256_file(_lib / 'optA_lib_v02.py'),
                   code_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(), seconds=time.time() - T_START)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(dict(values=vals, details=details), indent=1, allow_nan=True,
                               default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o)), encoding='utf-8')
    log('wrote', outp)


if __name__ == '__main__':
    log('numba', HAVE_NUMBA, 'threads', (numba.get_num_threads() if HAVE_NUMBA else 1), 'set', ARGS.set)
    if ARGS.set == 'unmasked':
        run_unmasked()
    else:
        run_masked()
