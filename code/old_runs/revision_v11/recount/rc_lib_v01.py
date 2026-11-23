"""Recount (independent second program) for the revision analyses of revision_v11. Library v01, 18 Nov 2026.

Written from revision_v11\\recount\\RECOUNT_BRIEF_v01.md and revision_v11\\AMENDMENT_08_ARS_REVISION_v01.md only.
Reads the stored arrays directly with numpy. Imports nothing from the data project (not the A6R lineage, not
revision_v11\\analysis, and not optA2_lib_v02 either: that file was read for its definitions, nothing is imported).

Definitions (brief, "Scoring definitions"):
  grid        g = 0 and 201 log-spaced values 1e-2 .. 1e3 (202 values).
  selection   first row (index order) whose critical scale is >= g; if none, the fallback row idx55.
  wrong go    the selected row is unsafe under the scoring (clearance <= G; NaN clearance = -1 = unsafe).
  caution     over evaluated decisions whose selected row is truly safe (3 s clear > G): mean of
              (vbar[first truly safe row] - vbar[selected row]) / desired, in %.
  signed      mean over every evaluated decision that has a truly safe row, each at its signed difference.
  frontier    step: lowest wrong go among the arm's points with caution <= level (undefined = NaN if no point).
  levels      201 equally spaced from F0's zero-margin caution to min(max caution of F0, max caution of E).
  prepend     every arm other than F0 and E, and the perfect oracle O, get F0's zero-margin point in front.
  denE = sum_levels(F_F0 - F_E); D(A) = sum_levels(F_F0 - F_A); den0 = D(O); R = denE / 201.
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '2')
import json, pathlib, time, warnings
import numpy as np

P = pathlib.Path(r'<library folder>')
STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
EXTRACT = P / '11_ojits' / 'A4' / 'fit' / 'extract'
CACHE = P / '11_ojits' / 'review' / 'optionA_recount_v01' / 'cache'
A4_JSON = P / '11_ojits' / 'A4' / 'fit' / 'analysis' / 'A4_RESULTS_FIT_v01.json'
HERE = pathlib.Path(__file__).resolve().parent

RUNS = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
GRID = np.concatenate([[0.], np.logspace(-2, 3, 201)])
NG = GRID.size
NLEV = 201
ARMS = ('F0', 'E', 'N', 'NA', 'AM', 'CK3', 'Q')
SRC = dict(F0=('g', 'cF0'), E=('g', 'cE'), N=('g', 'cN'), NA=('x', 'cNA'), AM=('x', 'cA1'), CK3=('x', 'cCK3'), Q=('x', 'cQ'))
SEED = 20261113
NBOOT = 20000
H = 0.05
KEY_RS = 't0p75_a6p0'


def log(*a, file=None):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    if file is not None:
        with open(file, 'a', encoding='utf-8') as f:
            f.write(time.strftime('%H:%M:%S ') + s + '\n')


# ------------------------------------------------------------------------------------------------ data
def load_run(run):
    zg = np.load(STORED / (run + '.npz'), allow_pickle=False)
    ze = np.load(EXTRACT / (run + '.npz'), allow_pickle=False)
    zc = np.load(CACHE / (run + '_pack.npz'), allow_pickle=False)
    meta = json.loads(str(zg['meta']))
    if meta['run'] != run or meta['family'] != 'lead_braking' or meta['set'] != 'fit':
        raise RuntimeError('unexpected metadata in %s' % run)
    if not np.array_equal(zg['k'], ze['k']):
        raise RuntimeError('%s: k of the extraction differs from the stored k' % run)
    ev = zg['evaluated'].astype(bool)
    n = int(ev.sum())
    clear = np.asarray(zg['clear'], float)[ev]
    n_nan_ev = int(np.isnan(clear).sum())
    clear = np.where(np.isnan(clear), -1., clear)
    rs = np.asarray(zc[KEY_RS], float)[ev]
    n_nan_rs = int(np.isnan(rs).sum())
    rs = np.where(np.isnan(rs), -1., rs)
    des = np.asarray(zg['des'], float)[ev]
    if not np.all(des == float(meta['desired'])):
        raise RuntimeError('%s: des array differs from meta.desired' % run)
    d = dict(run=run, n=n, n_stored=int(ev.size), meta=meta, clear=clear, rs=rs, n_nan_clear_eval=n_nan_ev, n_nan_rs_eval=n_nan_rs,
             vbar=np.asarray(zg['vbar'], float)[ev], idx55=np.asarray(zg['idx55'])[ev].astype(np.int64), des=des,
             v0=np.asarray(zg['v0'], float)[ev], k=np.asarray(zg['k'])[ev].astype(np.int64),
             phase=np.asarray(ze['phase'])[ev].astype(np.int64), prim_age=np.asarray(zg['prim_age'], float)[ev],
             prim_miss=np.asarray(zg['prim_miss'])[ev].astype(np.int64),
             k_all=np.asarray(zg['k']).astype(np.int64), phase_all=np.asarray(ze['phase']).astype(np.int64), ev_all=ev)
    d['crit'] = {a: np.asarray((zg if s == 'g' else ze)[key], float)[ev] for a, (s, key) in SRC.items()}
    for a in ARMS:
        if np.isnan(d['crit'][a]).any():
            raise RuntimeError('%s: NaN critical scale in arm %s' % (run, a))
    d['sel'] = {a: select(d['crit'][a], d['idx55']) for a in ARMS}
    ph2 = np.flatnonzero(d['phase_all'] == 2)
    d['k_stop'] = int(d['k_all'][ph2[0]]) if ph2.size else None
    return d


def load_all():
    return [load_run(r) for r in RUNS]


def select(C, idx55):
    """(202, n): first row with critical scale >= g, else the fallback row."""
    feas = C[None, :, :] >= GRID[:, None, None]
    return np.where(feas.any(2), feas.argmax(2), idx55[None, :])


def oracle_sel(safe, idx55):
    """(1, n): first row the scoring judges safe, else the fallback row."""
    return np.where(safe.any(1), safe.argmax(1), idx55)[None, :]


def sel_stats(d, sel, safe_w, safe_c, masks, signed):
    """(n_masks, G, 3): wrong-go count, caution sum, caution count, for the selection sel (G, n).
    safe_w (n, 17): rows safe under the scoring (wrong go).  safe_c (n, 17): truly safe rows (caution axis)."""
    n = d['n']; ar = np.arange(n)
    bad = ~safe_w[ar[None, :], sel]
    has = safe_c.any(1); first = safe_c.argmax(1)
    diff = (d['vbar'][ar, first][None, :] - d['vbar'][ar[None, :], sel]) / d['des'][None, :]
    if signed:
        term = np.where(has[None, :], diff, 0.); cnt = np.broadcast_to(has[None, :], sel.shape)
    else:
        ok = safe_c[ar[None, :], sel]
        term = np.where(ok, diff, 0.); cnt = ok
    out = np.zeros((len(masks), sel.shape[0], 3))
    for mi, m in enumerate(masks):
        out[mi, :, 0] = bad[:, m].sum(1); out[mi, :, 1] = term[:, m].sum(1); out[mi, :, 2] = cnt[:, m].sum(1)
    return out


def run_row(d, masks, safe_w, safe_c, signed):
    """One run's sufficient statistics as a flat vector: [n per mask | arms (P, A, G, 3) | oracle (P, 3)]."""
    Pm = len(masks)
    nm = np.array([float(m.sum()) for m in masks])
    S = np.zeros((Pm, len(ARMS), NG, 3))
    for ai, a in enumerate(ARMS):
        S[:, ai] = sel_stats(d, d['sel'][a], safe_w, safe_c, masks, signed)
    O = sel_stats(d, oracle_sel(safe_w, d['idx55']), safe_w, safe_c, masks, signed)[:, 0, :]
    return np.concatenate([nm, S.ravel(), O.ravel()])


def build_M(ds, mask_fn, scoring='W1', gap=0., signed=False):
    """Matrix (runs, K) of per-run statistics. mask_fn(d) -> list of boolean masks over the run's evaluated decisions.
    scoring 'W1': wrong go by the 3 s clearance; 'RS': by the reaction-and-stop cache clearance (tau 0.75 s, 6 m/s2).
    The caution axis always uses the 3 s clearance (> gap)."""
    rows = []
    for d in ds:
        safe_c = d['clear'] > gap
        safe_w = safe_c if scoring == 'W1' else (d['rs'] > gap)
        rows.append(run_row(d, mask_fn(d), safe_w, safe_c, signed))
    return np.stack(rows)


def masks_std(d):
    return [np.ones(d['n'], bool), d['v0'] > 0.5, d['phase'] == 0, d['phase'] == 1, d['phase'] == 2]


POPS_STD = ('all', 'moving', 'phase0', 'phase1', 'phase2')


def masks_all(d):
    return [np.ones(d['n'], bool)]


# ------------------------------------------------------------------------------------------------ frontier
def linspace_rows(a, b, num=NLEV):
    """Row-wise numpy.linspace(a[i], b[i], num), bit-identical to the scalar call (including its zero-step branch)."""
    div = num - 1
    delta = b - a
    with np.errstate(invalid='ignore'):
        step = delta / div
        y = np.arange(num)[None, :] * step[:, None] + a[:, None]
        z = step == 0
        if z.any():
            y[z] = (np.arange(num)[None, :] / div) * delta[z][:, None] + a[z][:, None]
    y[:, -1] = b
    return y


def step_frontier(c, w, lev):
    """Batched step frontier. c, w (B, Pn) points; lev (B, L). Lowest w among points with c <= level; NaN if none."""
    B, L = lev.shape
    c = np.where(np.isfinite(c), c, np.inf)
    o = np.argsort(c, axis=1, kind='stable')
    cs = np.take_along_axis(c, o, 1)
    cm = np.minimum.accumulate(np.take_along_axis(w, o, 1), axis=1)
    j = np.empty((B, L), np.int64)
    for b in range(B):
        j[b] = np.searchsorted(cs[b], lev[b], side='right')
    j -= 1
    F = np.take_along_axis(cm, np.maximum(j, 0), 1).astype(float)
    F[(j < 0) | ~np.isfinite(lev)] = np.nan
    return F


def unpack(agg, Pm):
    B = agg.shape[0]; A = len(ARMS)
    n = agg[:, :Pm]
    S = agg[:, Pm:Pm + Pm * A * NG * 3].reshape(B, Pm, A, NG, 3)
    O = agg[:, Pm + Pm * A * NG * 3:].reshape(B, Pm, 3)
    return n, S, O


def evaluate(agg, Pm, want_curves=False):
    """agg (B, K) pooled statistics -> n (B, P), D (B, P, A+1) with columns ARMS then O: D = sum_levels(F_F0 - F_arm)
    (so D[..., 1] = denE and D[..., -1] = den0), nan_levels (B, P): levels at which some frontier is undefined."""
    agg = np.atleast_2d(agg)
    B = agg.shape[0]; A = len(ARMS)
    n, S, O = unpack(agg, Pm)
    D = np.full((B, Pm, A + 1), np.nan); nanlev = np.zeros((B, Pm), np.int64)
    curves = {}
    with np.errstate(invalid='ignore', divide='ignore'), warnings.catch_warnings():
        warnings.simplefilter('ignore', RuntimeWarning)
        for p in range(Pm):
            npop = n[:, p]
            W = 100. * S[:, p, :, :, 0] / npop[:, None, None]
            C = 100. * S[:, p, :, :, 1] / S[:, p, :, :, 2]
            c0 = C[:, 0, 0]; w0 = W[:, 0, 0]
            hi = np.minimum(np.nanmax(C[:, 0], axis=1), np.nanmax(C[:, 1], axis=1))
            lev = linspace_rows(c0, hi)
            fF = step_frontier(C[:, 0], W[:, 0], lev)
            D[:, p, 0] = 0.
            fr = {'F0': fF}
            fE = step_frontier(C[:, 1], W[:, 1], lev)
            D[:, p, 1] = np.sum(fF - fE, axis=1); fr['E'] = fE
            nl = np.isnan(fF).any(1) | np.isnan(fE).any(1)
            for ai in range(2, A):
                c2 = np.concatenate([c0[:, None], C[:, ai]], 1); w2 = np.concatenate([w0[:, None], W[:, ai]], 1)
                fA = step_frontier(c2, w2, lev)
                D[:, p, ai] = np.sum(fF - fA, axis=1); fr[ARMS[ai]] = fA
            cO = 100. * O[:, p, 1] / O[:, p, 2]; wO = 100. * O[:, p, 0] / npop
            fO = step_frontier(np.stack([c0, cO], 1), np.stack([w0, wO], 1), lev)
            D[:, p, A] = np.sum(fF - fO, axis=1); fr['O'] = fO
            nanlev[:, p] = nl
            if want_curves:
                curves[p] = dict(lev=lev, C=C, W=W, cO=cO, wO=wO, fr=fr)
    if want_curves:
        return n, D, nanlev, curves
    return n, D, nanlev


def counts_from_idx(idx, nruns):
    """(B, nruns) multiplicities of the resamples given as index rows."""
    cnt = np.zeros((idx.shape[0], nruns))
    for j in range(nruns):
        cnt[:, j] = (idx == j).sum(1)
    return cnt


def draw_of_record():
    return np.random.default_rng(SEED).integers(0, 35, size=(NBOOT, 35))


def boot(M, idx, Pm, chunk=400, logfile=None, tag=''):
    """Evaluate every resample (rows of idx = run indices into M)."""
    B = idx.shape[0]; A = len(ARMS)
    n = np.zeros((B, Pm)); D = np.full((B, Pm, A + 1), np.nan); nl = np.zeros((B, Pm), np.int64)
    t0 = time.time()
    for s in range(0, B, chunk):
        cnt = counts_from_idx(idx[s:s + chunk], M.shape[0])
        n[s:s + chunk], D[s:s + chunk], nl[s:s + chunk] = evaluate(cnt @ M, Pm)
        if logfile is not None and ((s // chunk) % 10 == 0 or s + chunk >= B):
            log('  %s bootstrap %d / %d, %.0f s' % (tag, min(s + chunk, B), B, time.time() - t0), file=logfile)
    return n, D, nl


# ------------------------------------------------------------------------------------------------ summaries
def pct(v, lo=2.5, hi=97.5):
    v = np.asarray(v, float); v = v[np.isfinite(v)]
    if v.size == 0:
        return None
    a, b = np.percentile(v, [lo, hi])
    return [float(a), float(b)]


def ratio_ci(num, den):
    """Percentile interval of num / den over resamples with a positive (finite) denominator."""
    num = np.asarray(num, float); den = np.asarray(den, float)
    keep = np.isfinite(den) & (den > 0) & np.isfinite(num)
    return pct(num[keep] / den[keep]), int((~keep).sum())


def weighted(n, D, cols=(2, 3, 4)):
    """Phase-weighted aggregate over the phase populations (columns of n, D): sum_p (n_p / n) D_p, an empty phase contributing 0.
    n (B, P), D (B, P, X) -> ntot (B,), Dw (B, X)."""
    cols = list(cols)
    nn = n[:, cols]; ntot = nn.sum(1)
    Dp = np.where(nn[:, :, None] > 0, D[:, cols, :], 0.)
    with np.errstate(invalid='ignore', divide='ignore'):
        Dw = np.sum((nn / ntot[:, None])[:, :, None] * Dp, axis=1)
    Dw[ntot <= 0] = np.nan
    return ntot, Dw


def jdump(obj, path):
    def conv(o):
        if isinstance(o, dict):
            return {str(k): conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [conv(v) for v in o]
        if isinstance(o, np.ndarray):
            return conv(o.tolist())
        if isinstance(o, (np.floating,)):
            o = float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, float) and not np.isfinite(o):
            return None if np.isnan(o) else ('inf' if o > 0 else '-inf')
        return o
    pathlib.Path(path).write_text(json.dumps(conv(obj), indent=1), encoding='utf-8')
