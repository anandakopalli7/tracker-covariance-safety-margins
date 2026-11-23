r"""DRF recount (second program) v02: AMENDMENT_13 section 3 (text v02), N_DR against a fixed coast-count margin (arm F0_coast);
F0_flag2 (v01's two-population flag) is the descriptive secondary. v02 = the v01 program with the coast-count arm.

Written 22 Nov 2026 from the TEXT of A13_3_DRFLAG_v02.md, reusing the loading, populations (A12 3a.5), gridless kernel and draw of the A12
recount (dr_recount_a12_v02.py). It does not read or import the first program. Imports: numpy, the standard library, optA_lib_v02, numba if installed.

k is fitted on A11's 105 runs (out\arrays\DR): M_S = median of cN / cF0 over the rows of the evaluated decisions of population S with both finite
and > 0; k_in = M_in / M_st, k_re = M_re / M_st. F0_flag = F0_DR's scales times k_in (in-dropout), k_re (re-acquisition), 1 (steady). Test on the 150
new runs at p = 0.10: Delta = RR_gl(N_DR) - RR_gl(F0_flag), draw boot_counts(150, 20000, 20261911), plain 95% percentile interval, no calibration.

--test-old : fit k on, and test on, the old test runs in out\testold\DR (code test, no lock).
Non-test   : refuses without revision_v13\\LOCK_A13b.txt.
Usage: python -I dr_recount_a13_flag_v02.py [--test-old] [--threads N] [--nboot N] [--out PATH]
Environment: DR_P_ROOT (programme P root or the folder holding optA_lib_v02.py), DR_ROOT (the F_dropout folder), DR_LOCK (lock file).
"""
import os, sys, json, hashlib, argparse, math, pathlib, time, glob, warnings

# ------------------------------------------------------------------------------------------------ arguments (before numba import)
_ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
_ap.add_argument('--test-old', action='store_true')
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
DEFAULT_ROOT = r'ARS_TRIAL\revision_v13\work\F_dropout'
P_ROOT = pathlib.Path(os.environ.get('DR_P_ROOT', DEFAULT_P_ROOT))
ROOT = pathlib.Path(os.environ.get('DR_ROOT', DEFAULT_ROOT))
_lib = P_ROOT / '11_ojits' / 'A6R' / 'code'
if not (_lib / 'optA_lib_v02.py').exists():
    _lib = P_ROOT
sys.path.insert(0, str(_lib))
import optA_lib_v02 as L                           # noqa: E402  frozen library of record, read-only

LOCK = pathlib.Path(os.environ.get('DR_LOCK', str(ROOT.parent.parent / 'LOCK_A13b.txt')))

NLEV = L.NLEV                                      # 201
BOOT_SEED = 20261911
GMAX = 1000.0
EQUIV = 0.05


def log(*a):
    print('[%7.1f s]' % (time.time() - T_START), *a, flush=True)


T_START = time.time()


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


# ------------------------------------------------------------------------------------------------ A13 3 (v02): populations, k, test
MIN_ROWS = 50


def populations(r):
    """A12 3a.5 by the frame each decision uses (dr_frame) and the run's masked frames (meta['masked']), over the run's evaluated decisions:
    in = frame masked; reacq = frame not masked and frame-1 or frame-2 masked; steady = the rest (including decisions with no frame yet).
    c = coast count of an in-dropout decision = dr_age clipped to 3 (the mask law gives 1..3; a count above 3 would use k_3)."""
    fr = r['dr_frame_all'][r['ev']]
    mk = np.array([int(x) for x in r['meta']['masked']], dtype=int)
    inn = np.isin(fr, mk)
    rea = (~inn) & (np.isin(fr - 1, mk) | np.isin(fr - 2, mk))
    ste = ~inn & ~rea
    age = np.minimum(r['dr_age'], 3)
    return dict(inn=inn, reacq=rea, steady=ste, c1=inn & (age == 1), c2=inn & (age == 2), c3=inn & (age == 3),
                bad_age=int((inn & (r['dr_age'] < 1)).sum()))


def fit_k(fit_runs):
    """M_S = median of cN / cF0 over the rows of the evaluated decisions in population S where both are finite and > 0;
    S in {1, 2, 3 (coast count), re, st, in (all in-dropout)}. Returns {S: (M_S, rows)}."""
    keys = {'1': 'c1', '2': 'c2', '3': 'c3', 're': 'reacq', 'st': 'steady', 'in': 'inn'}
    vals = {k: [] for k in keys}
    bad = 0
    for r in fit_runs:
        P = populations(r)
        bad += P['bad_age']
        for k, pk in keys.items():
            m = P[pk]
            cN, cF = r['cN'][m], r['cF0'][m]
            ok = np.isfinite(cN) & (cN > 0) & np.isfinite(cF) & (cF > 0)
            vals[k].append(cN[ok] / cF[ok])
    out = {}
    for k in keys:
        v = np.concatenate(vals[k]) if vals[k] else np.zeros(0)
        out[k] = (float(np.median(v)) if v.size else float('nan'), int(v.size))
    return out, bad


def run():
    test = ARGS.test_old
    if not test and not LOCK.exists():
        raise SystemExit('REFUSED: %s does not exist (non-test mode needs the lock)' % LOCK)
    outp = pathlib.Path(ARGS.out) if ARGS.out else ROOT / 'recount' / ('TESTOLD_DRF_RECOUNT_v02.json' if test else 'DRF_RECOUNT_v02.json')
    if outp.exists():
        raise SystemExit('REFUSED: %s exists' % outp)
    nboot = ARGS.nboot or 20000
    if test:
        fit_dir = test_dir = ROOT / 'out' / 'testold' / 'DR'
    else:
        fit_dir = ROOT / 'out' / 'arrays' / 'DR'
        test_dir = ROOT / 'out_a12' / 'p010' / 'arrays' / 'DR'
    fit_runs = load_runs(fit_dir, fit_dir)
    test_runs = fit_runs if test else load_runs(test_dir, test_dir)
    if not test:
        mf = json.loads((ROOT / 'out_a12' / 'p010' / 'DR_MASKS_p010.json').read_text(encoding='utf-8'))
        if sorted(mf['fresh'].keys()) != [r['id'] for r in test_runs]:
            raise SystemExit('the arrays at p010 are not the runs of the mask file')
        if len(fit_runs) != 105:
            raise SystemExit('expected 105 fit runs, found %d' % len(fit_runs))
    n_fit, n_test = len(fit_runs), len(test_runs)
    log('fit runs', n_fit, 'test runs', n_test, 'test_old', test)
    M, bad_age_fit = fit_k(fit_runs)
    M_st = M['st'][0]
    k_in = M['in'][0] / M_st
    k_re = M['re'][0] / M_st
    k, fb = {}, {}
    for c in ('1', '2', '3'):
        fb[c] = bool(M[c][1] < MIN_ROWS)
        k[c] = k_in if fb[c] else M[c][0] / M_st
    log('M %s; k_1 %.6f k_2 %.6f k_3 %.6f k_re %.6f k_in %.6f; fallback %s; fit rows %s' % (
        {s: round(v[0], 6) for s, v in M.items()}, k['1'], k['2'], k['3'], k_re, k_in, fb, {s: v[1] for s, v in M.items()}))

    crit_coast, crit_flag2 = [], []
    n_pop = dict(c1=0, c2=0, c3=0, reacq=0, steady=0)
    bad_age_test = 0
    for r in test_runs:
        P = populations(r)
        bad_age_test += P['bad_age']
        fc = np.where(P['c1'], k['1'], np.where(P['c2'], k['2'], np.where(P['c3'], k['3'], np.where(P['reacq'], k_re, 1.0))))[:, None]
        f2 = np.where(P['inn'], k_in, np.where(P['reacq'], k_re, 1.0))[:, None]
        crit_coast.append(r['cF0'] * fc)               # inf, -inf, 0 and NaN are kept by multiplication with a finite positive factor
        crit_flag2.append(r['cF0'] * f2)
        for key in n_pop:
            n_pop[key] += int(P[key].sum())
    crit = dict(F0=[r['cF0'] for r in test_runs], E=[r['cE'] for r in test_runs], N=[r['cN'] for r in test_runs],
                Coast=crit_coast, Flag2=crit_flag2)
    pop = [np.ones(int(r['clear1'].shape[0]), dtype=bool) for r in test_runs]
    names = ['F0', 'E', 'N', 'Coast', 'Flag2']
    ds = DataSet(names, [build_source(test_runs, crit[nm], pop) for nm in names])
    D0, _ = eval_W(ds, np.ones((1, n_test)))
    Wb = L.boot_counts(n_test, nboot, BOOT_SEED)
    Db, _ = eval_W(ds, Wb)

    def shares(D):
        den = D[:, 1]
        ok = np.isfinite(den) & (den > 0)
        with np.errstate(invalid='ignore', divide='ignore'):
            rrN = np.where(ok, D[:, 2] / den, np.nan)
            rrC = np.where(ok, D[:, 3] / den, np.nan)
            rrF = np.where(ok, D[:, 4] / den, np.nan)
            dc = np.where(ok, (D[:, 2] - D[:, 3]) / den, np.nan)
            df = np.where(ok, (D[:, 2] - D[:, 4]) / den, np.nan)
        return rrN, rrC, rrF, dc, df
    rN0, rC0, rF0, dc0, df0 = [float(x[0]) for x in shares(D0)]
    rNb, rCb, rFb, dcb, dfb = shares(Db)
    ci_d = ci_at(dcb, 0.95)
    passes = bool(ci_d[0] > 0)
    within = bool((ci_d[0] > -EQUIV) and (ci_d[1] < EQUIV))
    vals = {}
    vals['DRF.n_runs'] = float(n_test)
    vals['DRF.n_fit_runs'] = float(n_fit)
    for key in ('1', '2', '3', 're', 'st', 'in'):
        vals['DRF.M_' + key] = M[key][0]
        vals['DRF.n_fit_rows.' + key] = float(M[key][1])
    for c in ('1', '2', '3'):
        vals['DRF.k_' + c] = k[c]
        vals['DRF.k_%s.fallback' % c] = fb[c]
    vals['DRF.k_re'] = k_re
    vals['DRF.k_in'] = k_in
    for key in ('c1', 'c2', 'c3', 'reacq', 'steady'):
        vals['DRF.n_dec.' + key] = float(n_pop[key])
    vals['DRF.RR_N'] = rN0
    vals['DRF.RR_N.ci'] = ci_at(rNb, 0.95)
    vals['DRF.RR_coast'] = rC0
    vals['DRF.RR_coast.ci'] = ci_at(rCb, 0.95)
    vals['DRF.delta'] = dc0
    vals['DRF.delta.ci'] = ci_d
    TIE = 1e-12                                        # A13 3.4: a resample with delta* <= 1e-12 (or NaN) counts against the test
    vals['DRF.delta.p'] = float((1 + int(np.sum(~(dcb > TIE)))) / (nboot + 1))
    vals['DRF.passes'] = passes
    vals['DRF.within_equiv'] = within
    vals['DRF.status'] = 'passed (amendment)' if passes else 'failed (amendment)'
    vals['DRF.RR_flag2'] = rF0
    vals['DRF.RR_flag2.ci'] = ci_at(rFb, 0.95)
    vals['DRF.delta_flag2'] = df0
    vals['DRF.delta_flag2.ci'] = ci_at(dfb, 0.95)
    details = dict(test_old=test, nboot=nboot, numba=HAVE_NUMBA, seed=BOOT_SEED, full_D=[float(x) for x in D0[0]],
                   n_resamples_delta_nan=int(np.sum(np.isnan(dcb))), n_resamples_delta_le0_or_nan=int(np.sum(~(dcb > TIE))),
                   n_resamples_abs_delta_le_1e12=int(np.sum(np.abs(dcb) <= TIE)),
                   delta_flag2_p=float((1 + int(np.sum(~(dfb > TIE)))) / (nboot + 1)),
                   in_dropout_decisions_with_age_below_1=dict(fit=bad_age_fit, test=bad_age_test),
                   des_nonconstant_runs=[r['id'] for r in test_runs if not r['des_const']],
                   fit_ids=[fit_runs[0]['id'], fit_runs[-1]['id']], test_ids=[test_runs[0]['id'], test_runs[-1]['id']],
                   lock=str(LOCK), library_sha256=L.sha256_file(_lib / 'optA_lib_v02.py'),
                   code_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(), seconds=time.time() - T_START)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(dict(values=vals, details=details), indent=1, allow_nan=True,
                               default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o)), encoding='utf-8')
    log('wrote', outp)


if __name__ == '__main__':
    log('numba', HAVE_NUMBA, 'threads', (numba.get_num_threads() if HAVE_NUMBA else 1), 'test', ARGS.test_old)
    run()
