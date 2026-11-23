"""Recount (second program) of package C, revision v13: shared core. New file, 19 Nov 2026 (Claude Fable 5.2).

Written from AMENDMENT_10_v13.md (sections 0, 2, 5.1-5.5, 5.8, 10.1) and CD_DEFINITIONS_v13.md only; no first program of
work\\CD_capture\\analysis was read. Everything here is a separate implementation, except what CD_DEFINITIONS allows to share and
what is imported, read-only, for CROSS-CHECKS and library points: the scoring library of record optA_lib_v02 (stats_scored,
select_grid, frontier, levels_of, curves_w, eval_scoring, boot_counts, dec_eq) and, when importable, v12's a9_common_v01 gridless
construction (used only to verify this module's own gridless curves and to print library points).

Own implementations in this file
  * gate:           require_lock2()  -- every reader of a fresh-run file calls it first.
  * loaders:        old evaluation runs (through rev_common_v01.load_runs), fresh arrays, old cut-in tuning arrays.
  * gridless:       Prep (row statistics of a run), source_events (selection path of every decision as the scale rises from 0 to
                    1000), Curve (events of one source and one population, sorted once), Problem (a set of curves with the roles
                    F0, E, others) and the numba kernel that evaluates the 201-level step frontiers of many run resamples.
                    A single evaluation reproduces optA_lib_v02.eval_scoring on a9_common_v01.Gridless curves bit for bit:
                    the same event order, the same sequential sums, T0 by the same numpy.tensordot call, the levels by numpy.linspace's
                    arithmetic, the frontier as the minimum over the same point set, and the 201-term sums by numpy.sum.
  * E5 family:      e5_u, permute_u, oracle_crit, margin_ratios, ratio_summary (A10 section 2.2).
  * phase:          est_phase (A10 section 2.4).
  * calibration:    DoubleBoot (A10 section 2.6, the v11 rev_d_bootstrap_v01 method with A10's seeds), calibrate_stat.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import json, math, pathlib, sys, time
import numpy as np
import numba
from numba import njit, prange

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import rc_kern_v13 as KN                     # noqa: E402  (pure part of the recount: kernel, statistic groups, job files)
OUT = HERE / 'out'
ARS = pathlib.Path(os.environ.get('RC_ARS_TRIAL', r'ARS_TRIAL'))
P = pathlib.Path(os.environ.get('RC_PROGRAMME_A', r'<library folder>'))
ROOT13 = ARS / 'revision_v13'
CD = ROOT13 / 'work' / 'CD_capture'
LOCK2 = ROOT13 / 'LOCK_A10_2.txt'
ARRAYS = CD / 'arrays'
RUNS_DIR = CD / 'runs'
CASES_C = CD / 'CASES_C_v13.json'
V11 = ARS / 'revision_v11' / 'analysis'
V12 = ARS / 'revision_v12' / 'analysis'
SHARED = ROOT13 / 'work' / 'shared' / 'trackers'
LIBDIR = P / '11_ojits' / 'A6R' / 'code'
STORED_OLD = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
RUN_INDEX = P / '09_redesign' / 'm4_perception_model' / 'run_index_m4_v02.csv'
FORBIDDEN = ('<excluded folder 1>', '<excluded folder 2>', '<excluded folder 3>')
# RC_DRYRUN=1: the tree under RC_ARS_TRIAL is a scratch copy filled with OLD runs relabelled (dryrun_fresh_path_v13.py);
# outputs are then named DRYRUN_* and say so. It never applies to the project tree.
DRYRUN = bool(os.environ.get('RC_DRYRUN'))
if DRYRUN and 'RC_ARS_TRIAL' not in os.environ:
    raise SystemExit('REFUSED: RC_DRYRUN needs RC_ARS_TRIAL (a scratch tree outside the project)')

if str(LIBDIR) not in sys.path:
    sys.path.insert(0, str(LIBDIR))
import optA_lib_v02 as L                     # noqa: E402  (scoring library of record, imported unchanged)

NLEV = 201
GMAX = 1e3
GRID = np.concatenate([[0.], np.logspace(-2, 3, 201)])
RATIO = 1.1029
E5_AMP = 0.05
DELTA = 0.05
SEED_BOOT = 20261911
SEED_OUTER = 20261912
SEED_INNER = 20261913
SEED_INNER2 = 20261914
SEED_PERM = 20261915
SEED_MC = 20261920
NBOOT = 20000
B_OUTER = 2000
B_INNER = 1000
B_MC = 2000
CAL_LEVELS = np.round(0.95 + 0.0005 * np.arange(100), 4)        # 0.9500 ... 0.9995
FALLBACK_LEVEL = 0.99


# ------------------------------------------------------------------------------------------------ gate and files
def require_lock2(what):
    """The Lock 2 gate: no fresh-run file is opened unless LOCK_A10_2.txt exists."""
    if not LOCK2.is_file():
        raise SystemExit('REFUSED: %s is sealed until %s exists (AMENDMENT_10 section 4)' % (what, LOCK2))


def check_path(p):
    s = str(p)
    for f in FORBIDDEN:
        if f in s:
            raise SystemExit('REFUSED: forbidden path %s' % s)
    return p


def clock():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def jdump(obj):
    def conv(o):
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        return str(o)
    return json.dumps(obj, indent=1, default=conv, allow_nan=True)


def write_new(path, doc):
    """Write once: refuses to overwrite."""
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, 'x', encoding='utf-8') as f:
            f.write(jdump(doc))
    except FileExistsError:
        raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % path)
    return path


def clean_clear(clear):
    """NaN clearance (only outside the evaluated set) -> -1; +inf stays."""
    clear = np.asarray(clear, float)
    return np.where(np.isfinite(clear) | (clear == np.inf), clear, -1.)


def try_a9():
    """v12's gridless construction, for cross-checks only. None if it cannot be imported (e.g. on a pod)."""
    try:
        if str(V12) not in sys.path:
            sys.path.insert(0, str(V12))
        import a9_common_v01 as A9
        return A9
    except Exception as e:                       # pragma: no cover
        print('note: a9_common_v01 not importable (%s); library cross-checks are skipped' % e, flush=True)
        return None


# ------------------------------------------------------------------------------------------------ loaders
def load_old_eval_runs():
    """The 35 old evaluation runs (exploratory data of record) through rev_common_v01.load_runs, with the tracker's lead state
    (revision_v12 out\\lead) and TG (out\\tg, cTG2) attached."""
    if str(V11) not in sys.path:
        sys.path.insert(0, str(V11))
    import rev_common_v01 as C
    runs = []
    for r in C.load_runs():
        z = np.load(V12 / 'out' / 'lead' / (r['run'] + '.npz'), allow_pickle=False)
        if not np.array_equal(z['k'], r['k']):
            raise SystemExit('REFUSED: lead arrays of %s do not match its decisions' % r['run'])
        t = np.load(V12 / 'out' / 'tg' / (r['run'] + '.npz'), allow_pickle=False)
        if not np.array_equal(t['k'], r['k']):
            raise SystemExit('REFUSED: TG arrays of %s do not match its decisions' % r['run'])
        crit = dict(r['crit']); crit['TG'] = t['cTG2']
        runs.append(dict(run=r['run'], desired=float(r['desired']), k=np.asarray(r['k']), ev=np.asarray(r['ev'], bool),
                         clear1=r['clear1'], vbar=r['vbar'], idx55=np.asarray(r['idx55']).astype(np.int64), crit=crit,
                         ph=np.asarray(r['ph']).astype(np.int64), vhat=z['vhat'], ahat_long=z['ahat_long'],
                         lead_found=z['lead_found'].astype(bool)))
    return runs


def fresh_run_ids(family):
    """Run ids of package C for one family, from CASES_C_v13.json (the case list; not a fresh-run value), in run-id order."""
    d = json.loads(CASES_C.read_text(encoding='utf-8'))
    ids = sorted('pc13_%s_native' % c['case'] for c in d['cases'] if c['family'] == family)
    return ids


def _run_from_arrays(z, rid, crit_map, extra=()):
    des = np.asarray(z['des'], float)
    if des.size and not np.all(des == des[0]):
        raise SystemExit('REFUSED: %s has more than one desired speed' % rid)
    r = dict(run=rid, desired=float(des[0]), k=np.asarray(z['k']), ev=np.asarray(z['evaluated']).astype(bool),
             clear1=clean_clear(z['clear']), vbar=np.asarray(z['vbar'], float), idx55=np.asarray(z['idx55']).astype(np.int64),
             crit={nm: np.asarray(z[key], float) for nm, key in crit_map.items() if key in z.files})
    for kx in extra:
        if kx in z.files:
            r[kx] = np.asarray(z[kx])
    return r


def load_fresh_runs(family, variant='CV0'):
    """Fresh arrays work\\CD_capture\\arrays\\<variant>\\<run_id>.npz (CD_DEFINITIONS 'Inputs'). Gated by Lock 2."""
    require_lock2('fresh-run arrays')
    cm = {'F0': 'cF0', 'E': 'cE', 'N': 'cN', 'NA': 'cNA', 'Q': 'cQ', 'A1': 'cA1', 'CK3': 'cCK3', 'TG': 'cTG2'}
    runs = []
    for rid in fresh_run_ids(family):
        f = check_path(ARRAYS / variant / (rid + '.npz'))
        z = np.load(f, allow_pickle=False)
        meta = json.loads(str(z['meta']))
        if meta.get('family') != family or meta.get('lead_variant'):
            raise SystemExit('REFUSED: %s is not a plain %s run (meta %s)' % (rid, family, meta))
        r = _run_from_arrays(z, rid, cm, extra=('phase', 'lead_found', 'vhat', 'ahat_long'))
        if 'phase' in r:
            r['ph'] = r.pop('phase').astype(np.int64)
        if 'lead_found' in r:
            r['lead_found'] = r['lead_found'].astype(bool)
        runs.append(r)
    return runs


def old_cutin_tuning_index():
    """The 20 cut-in tuning runs of record: rows use = 1, set = tune, family = cutin of run_index_m4_v02.csv."""
    import csv
    rows = []
    with open(RUN_INDEX, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['use'] == '1' and row['set'] == 'tune' and row['family'] == 'cutin':
                rows.append(row)
    rows.sort(key=lambda x: x['archive'])
    return rows


def load_old_cutin_runs():
    runs = []
    for row in old_cutin_tuning_index():
        z = np.load(STORED_OLD / (row['archive'] + '.npz'), allow_pickle=False)
        r = _run_from_arrays(z, row['archive'], {'F0': 'cF0', 'E': 'cE', 'N': 'cN'})
        cap = pathlib.Path(row['cap'])
        r['cap'] = check_path(cap)
        r['rd'] = check_path(cap.parents[3])            # ...\<archive>\x\<archive>\capture\<case> -> the archive folder (SUMMARY.json)
        if not (r['rd'] / 'SUMMARY.json').is_file():
            raise SystemExit('REFUSED: no SUMMARY.json in %s' % r['rd'])
        runs.append(r)
    return runs


# ------------------------------------------------------------------------------------------------ A10 2.2: E5 family
def margin_ratio_values(r, a='N', b='F0', dec_mask=None):
    """sqrt(c_b / c_a) over the decisions of dec_mask (default: evaluated) and rows with both critical scales finite and positive."""
    m = r['ev'] if dec_mask is None else dec_mask
    ca = r['crit'][a][m]; cb = r['crit'][b][m]
    ok = np.isfinite(ca) & np.isfinite(cb) & (ca > 0) & (cb > 0)
    return np.sqrt(cb[ok] / ca[ok])


def ratio_summary(vals):
    vals = np.asarray(vals, float)
    if vals.size == 0:
        return dict(n=0, median=float('nan'), q05=float('nan'), q95=float('nan'), A=float('nan'),
                    share_within_5pct=float('nan'), barely_varies=False)
    med = float(np.median(vals)); q05, q95 = (float(x) for x in np.quantile(vals, [0.05, 0.95]))
    within = float(np.mean(np.abs(vals / med - 1.) <= 0.05))
    return dict(n=int(vals.size), median=med, q05=q05, q95=q95, A=(q95 - q05) / (2. * med), share_within_5pct=within,
                barely_varies=bool(within >= 0.95))


def e5_u(runs, f0='F0', e='E'):
    """u_i = (mid-rank of r_i - 0.5) / n_r over the run set's evaluated decisions that have a ratio; r_i = median over rows with
    finite positive c_F0 and c_E of sqrt(c_F0 / c_E). Decisions without such rows (and non-evaluated ones) get 0.5.
    (The shared library's reading, CD_DEFINITIONS 'u = e5_u(F0, E)': ranks and n are taken among decisions WITH a ratio.)"""
    rr = []
    for r in runs:
        cf = r['crit'][f0][r['ev']]; ce = r['crit'][e][r['ev']]
        ok = np.isfinite(cf) & np.isfinite(ce) & (cf > 0) & (ce > 0)
        val = np.full(cf.shape[0], np.nan)
        for i in np.flatnonzero(ok.any(axis=1)):
            val[i] = np.median(np.sqrt(cf[i][ok[i]] / ce[i][ok[i]]))
        rr.append(val)
    allv = np.concatenate(rr) if rr else np.zeros(0)
    have = np.isfinite(allv)
    uall = np.full(allv.size, 0.5)
    if have.any():
        v = allv[have]
        uniq, inv, cnt = np.unique(v, return_inverse=True, return_counts=True)
        before = np.cumsum(cnt) - cnt
        rank = before[inv] + (cnt[inv] + 1) / 2.
        uall[have] = (rank - 0.5) / v.size
    out = []; p = 0
    for r, val in zip(runs, rr):
        u = np.full(r['ev'].size, 0.5)
        u[r['ev']] = uall[p:p + val.size]; p += val.size
        out.append(u)
    return out, dict(n_evaluated=int(allv.size), n_with_ratio=int(have.sum()))


def permute_u(runs, u, seed=SEED_PERM):
    """u permuted within each run among its evaluated decisions; one generator, runs in the given (run-id) order."""
    rng = np.random.default_rng(seed)
    out = []
    for r, uu in zip(runs, u):
        uu = uu.copy(); ev = np.flatnonzero(r['ev'])
        uu[ev] = uu[ev][rng.permutation(ev.size)]
        out.append(uu)
    return out


def oracle_crit(cf0, m, A, u):
    """Critical scales c_F0 / f_i^2 with f_i = m (1 + A (2 u_i - 1))."""
    f = m * (1. + A * (2. * u - 1.))
    return cf0 / (f * f)[:, None]


# ------------------------------------------------------------------------------------------------ A10 2.4: phase
def est_phase(vhat, ahat_long, lead_found, thr=-1.0):
    """2 stopped (lead track speed <= 0.5), 1 braking (speed > 0.5 and acceleration along its velocity <= thr), else 0
    (also with no lead track)."""
    vhat = np.asarray(vhat, float); ah = np.asarray(ahat_long, float); fd = np.asarray(lead_found, bool)
    ph = np.zeros(vhat.shape, np.int64)
    with np.errstate(invalid='ignore'):
        ph[fd & (vhat > 0.5) & np.isfinite(ah) & (ah <= thr)] = 1
        ph[fd & (vhat <= 0.5)] = 2
    return ph


# ------------------------------------------------------------------------------------------------ gridless curves (own)
class Prep:
    """Row statistics of one run under the 3 s commitment (row safe iff clean clearance > 0): for every decision and row the
    contributions to wrong go (1), caution sum (2), caution count (3) and wrong go with a safe row (4) if that row is selected."""

    def __init__(self, r):
        clear1 = r['clear1']; vbar = r['vbar']; des = r['desired']
        n = clear1.shape[0]; ar = np.arange(n)
        safe = clear1 > 0.
        orc = safe.argmax(axis=1)
        anys = safe.any(axis=1)
        self.n = n
        self.safe = safe
        self.RS = np.zeros((4, n, 17))
        self.RS[0] = ~safe
        self.RS[1] = np.where(safe, (vbar[ar, orc][:, None] - vbar) / des, 0.)
        self.RS[2] = safe
        self.RS[3] = anys[:, None] & ~safe
        self.idx55 = np.asarray(r['idx55']).astype(np.int64)
        self.first_safe = np.where(anys, orc, self.idx55)


def selection_path(crit, idx55, gmax=GMAX):
    """Selections of every decision as the scale g rises from 0 to gmax (selected row = first row in cost order with c >= g,
    else the fallback row). Returns s0 (n,) = row at g = 0, and the events (decision i, row before, row after, breakpoint b) in
    (decision, breakpoint) order: just above b the selection moves to the next row whose critical scale exceeds every earlier one."""
    crit = np.asarray(crit, float)
    n = crit.shape[0]
    run_max = np.full(n, -np.inf)
    isrec = np.zeros((n, 17), bool)
    for j in range(17):
        v = crit[:, j]
        with np.errstate(invalid='ignore'):
            rec = v > run_max                      # NaN -> False
        isrec[:, j] = rec
        run_max = np.where(rec, v, run_max)
    with np.errstate(invalid='ignore'):
        live = isrec & (crit >= 0.)                # records that can be selected at some g >= 0
    anylive = live.any(axis=1)
    s0 = np.where(anylive, live.argmax(axis=1), idx55)
    # next record to the right of each column (else the fallback row)
    nxt = np.empty((n, 17), np.int64)
    cur = np.asarray(idx55, np.int64).copy()
    for j in range(16, -1, -1):
        nxt[:, j] = cur
        cur = np.where(isrec[:, j], j, cur)
    with np.errstate(invalid='ignore'):
        evm = live & (crit < gmax)
    ii, jj = np.nonzero(evm)                        # row-major: decision, then column (= rising breakpoint)
    to = nxt[ii, jj]
    keep = to != jj
    return s0, ii[keep], jj[keep], to[keep], crit[ii[keep], jj[keep]]


def _seqsum(x):
    """Sequential (left to right) float sum, as a Python accumulation loop."""
    return float(np.cumsum(x)[-1]) if x.size else 0.


class Curve:
    """Events of one source in one population over a run set, sorted once by breakpoint (stable: run, decision, breakpoint).
    T0 (nrun, 5): the g = 0 statistics per run. ri, d (ne, 3), last: run index, deltas of (wrong go, caution sum, caution count)
    and the flag 'last event of its distinct breakpoint'. Events whose three deltas are all zero are dropped (they only repeat
    a point of the curve)."""

    def __init__(self, T0, b, ri, d):
        self.T0 = np.ascontiguousarray(T0, float)
        o = np.argsort(b, kind='stable')
        b = b[o]; ri = ri[o]; d = d[o]
        nz = (d != 0.).any(axis=1)
        self.n_events_all = int(b.size)
        b = b[nz]
        self.b = b
        self.ri = np.ascontiguousarray(ri[nz], np.int32)
        self.d = np.ascontiguousarray(d[nz], float)
        self.last = np.ascontiguousarray(np.concatenate([b[1:] != b[:-1], [True]]) if b.size else np.zeros(0, bool), np.uint8)
        self.npts = 1 + int(self.last.sum())


def build_curves(runs, preps, crit_key, masks_of, oracle=False):
    """One Curve per population for the source crit_key (or the perfect oracle O: first safe row, else the fallback; one point).
    masks_of(run index) -> list of (n,) bool population masks."""
    npop = len(masks_of(0))
    T0 = np.zeros((npop, len(runs), 5))
    bs = [[] for _ in range(npop)]; rs = [[] for _ in range(npop)]; ds = [[] for _ in range(npop)]
    for k, (r, pp) in enumerate(zip(runs, preps)):
        masks = masks_of(k)
        if oracle:
            s0 = pp.first_safe; ii = np.zeros(0, np.int64)
        else:
            s0, ii, frm, to, b = selection_path(r['crit'][crit_key], pp.idx55)
            dd = pp.RS[:3, ii, to] - pp.RS[:3, ii, frm]                     # (3, ne)
        ar = np.arange(pp.n)
        v0 = pp.RS[:, ar, s0]                                               # (4, n)
        for pi, m in enumerate(masks):
            T0[pi, k, 0] = m.sum()
            for c in range(4):
                T0[pi, k, c + 1] = _seqsum(v0[c][m])
            if ii.size:
                me = m[ii]
                bs[pi].append(b[me]); rs[pi].append(np.full(int(me.sum()), k, np.int64)); ds[pi].append(dd[:, me].T)
    out = []
    for pi in range(npop):
        if bs[pi]:
            out.append(Curve(T0[pi], np.concatenate(bs[pi]), np.concatenate(rs[pi]), np.concatenate(ds[pi])))
        else:
            out.append(Curve(T0[pi], np.zeros(0), np.zeros(0, np.int64), np.zeros((0, 3))))
    return out


# ------------------------------------------------------------------------------------------------ numba kernel
# The kernel (_nanmax ... _kernel), Problem, ratio_arr and counts_of were moved, text unchanged, to rc_kern_v13.py (20 Nov 2026):
# a pure module (numpy and numba only) that the remote runner of the double bootstrap can import where this module cannot.
from rc_kern_v13 import (_nanmax, _levels, _sort_levels, _frontier, _gen_store, _finish, _front_stored, _pt,   # noqa: E402,F401
                         _front_stream, _kernel, Problem, ratio_arr, counts_of)


def library_point(A9, runs, names, mask_fn, pop_index, role_f0, role_e):
    """Full-sample point with the library of record: a9_common_v01.gridless_sources + optA_lib_v02.eval_scoring."""
    for k, r in enumerate(runs):
        r['_masks'] = tuple(mask_fn(k))
    G = A9.gridless_sources(runs, names, lambda r: r['clear1'] > 0., masks_key='_masks')
    T = {}
    for a in names:
        key = 'F0' if a == role_f0 else ('E' if a == role_e else a)
        T[key] = G[a].curve(None, pops=[pop_index])[:, 0, :]
    others = [a for a in names if a not in (role_f0, role_e)]
    e = L.eval_scoring(T, others)
    for r in runs:
        r.pop('_masks', None)
    return e, G


# ------------------------------------------------------------------------------------------------ intervals and calibration
def pct_interval(b, level):
    """Two-sided percentile interval at nominal level over the finite resamples."""
    b = np.asarray(b, float); f = np.isfinite(b)
    if not f.any():
        return [float('nan'), float('nan')]
    if abs(level - 0.95) < 1e-12:
        q = [2.5, 97.5]
    elif abs(level - 0.99) < 1e-12:
        q = [0.5, 99.5]
    else:
        a = 1. - level
        q = [100. * a / 2., 100. * (1. - a / 2.)]
    return [float(x) for x in np.percentile(b[f], q)]


def summ(b, pt, level=0.95):
    b = np.asarray(b, float); f = np.isfinite(b)
    return dict(point=float(pt), level=float(level), ci=pct_interval(b, level), ci95=pct_interval(b, 0.95), n_resamples=int(b.size),
                n_invalid=int((~f).sum()))


def boot_counts(n, nboot, seed):
    """default_rng(seed).integers(0, n, (nboot, n)) as counts per run."""
    idx = np.random.default_rng(seed).integers(0, n, (nboot, n))
    return counts_of(idx, n)


def cover_two(lt, le, nom, tol=1e-12):
    """Share of valid outer samples whose inner two-sided percentile interval at nominal level nom contains the full-sample
    value: share(inner <= full) >= a/2 and share(inner < full) <= 1 - a/2 (tolerance 1e-12, as rev_d_bootstrap_v01)."""
    a = 1. - nom
    ok = np.isfinite(lt)
    if not ok.any():
        return float('nan')
    return float(((le[ok] >= a / 2. - tol) & (lt[ok] <= 1. - a / 2. + tol)).mean())


def smallest_level(lt, le, tol=1e-12):
    for nm in CAL_LEVELS:
        cv = cover_two(lt, le, float(nm), tol)
        if np.isfinite(cv) and cv >= 0.95:
            return float(nm)
    return None


class DoubleBoot:
    """A10 section 2.6 / CD_DEFINITIONS: outer default_rng(20261912).integers(0, n, (2000, n)); inner default_rng(seed), one
    stream, integers(0, n, (1000, n)) per outer sample in order, indexing that outer sample's runs. Per outer sample and
    statistic: the shares of finite inner values below / at or below the full-sample value. An outer sample is valid for a
    statistic if its own estimate is finite and it has at least one finite inner value (rev_d_bootstrap_v01).
    stat_fn(CN (B, n) counts) -> (B, nstat). n_outer / n_inner < 2000 / 1000 use the FIRST rows of the same draws."""

    def __init__(self, stat_fn, full, n, seed_inner, n_outer=B_OUTER, n_inner=B_INNER, ckpt=None, label=''):
        self.stat_fn = stat_fn; self.full = np.asarray(full, float); self.n = n; self.seed_inner = seed_inner
        self.n_outer = n_outer; self.n_inner = n_inner; self.ckpt = ckpt; self.label = label
        ns = self.full.size
        self.p_lt = np.full((n_outer, ns), np.nan); self.p_le = np.full((n_outer, ns), np.nan)
        self.p_lt_any = np.full((n_outer, ns), np.nan); self.p_le_any = np.full((n_outer, ns), np.nan)
        self.outer_est = np.full((n_outer, ns), np.nan); self.n_inner_valid = np.zeros((n_outer, ns))
        self.done = 0

    def run(self):
        t0 = time.time()
        idx_o = np.random.default_rng(SEED_OUTER).integers(0, self.n, (B_OUTER, self.n))[:self.n_outer]
        rng_i = np.random.default_rng(self.seed_inner)
        start = 0
        if self.ckpt is not None and pathlib.Path(self.ckpt).is_file():
            z = np.load(self.ckpt, allow_pickle=False)
            if (int(z['n_outer']) == self.n_outer and int(z['n_inner']) == self.n_inner and int(z['seed']) == self.seed_inner
                    and np.array_equal(z['full'], self.full, equal_nan=True)):
                start = int(z['done'])
                for kx in ('p_lt', 'p_le', 'p_lt_any', 'p_le_any', 'outer_est', 'n_inner_valid'):
                    getattr(self, kx)[:start] = z[kx][:start]
                print('  %s: resumed at outer %d' % (self.label, start), flush=True)
        self.outer_est[:] = self.stat_fn(counts_of(idx_o, self.n))
        ns = self.full.size
        for b in range(self.n_outer):
            ii = rng_i.integers(0, self.n, (B_INNER, self.n))[:self.n_inner]      # always drawn: keeps the stream in order
            if b < start:
                continue
            S = self.stat_fn(counts_of(idx_o[b][ii], self.n))
            for j in range(ns):
                v = S[:, j]; v = v[np.isfinite(v)]
                self.n_inner_valid[b, j] = v.size
                if v.size == 0:
                    continue
                lt = (v < self.full[j]).mean(); le = (v <= self.full[j]).mean()
                self.p_lt_any[b, j] = lt; self.p_le_any[b, j] = le
                if np.isfinite(self.outer_est[b, j]):
                    self.p_lt[b, j] = lt; self.p_le[b, j] = le
            self.done = b + 1
            if self.ckpt is not None and ((b + 1) % 25 == 0 or b + 1 == self.n_outer):
                tmp = str(self.ckpt) + '.tmp.npz'
                np.savez(tmp, n_outer=self.n_outer, n_inner=self.n_inner, seed=self.seed_inner, full=self.full, done=b + 1,
                         p_lt=self.p_lt, p_le=self.p_le, p_lt_any=self.p_lt_any, p_le_any=self.p_le_any,
                         outer_est=self.outer_est, n_inner_valid=self.n_inner_valid)
                os.replace(tmp, self.ckpt)
            if (b + 1) % 50 == 0 or b + 1 == self.n_outer:
                print('  %s inner seed %d: outer %d / %d (%.0f s)' % (self.label, self.seed_inner, b + 1, self.n_outer,
                                                                      time.time() - t0), flush=True)
        self.seconds = time.time() - t0
        return self


def mc_levels(lt, le, n_mc=B_MC, seed=SEED_MC):
    """Monte Carlo spread of the calibrated level: n_mc resamples of the outer samples (default_rng(20261920).integers(0, B1,
    (2000, B1)); the first n_mc rows), the smallest-level rule in each (1.0 when no level reaches 0.95; CD_DEFINITIONS
    'Calibration details'); SD with ddof = 1. The index draw is the same for every statistic; validity is applied inside."""
    B1 = lt.shape[0]
    idx = np.random.default_rng(seed).integers(0, B1, (B_MC, B1))[:n_mc]
    ok = np.isfinite(lt)
    flags = np.zeros((B1, CAL_LEVELS.size))
    for li, nm in enumerate(CAL_LEVELS):
        a = 1. - float(nm)
        flags[:, li] = ok & (le >= a / 2. - 1e-12) & (lt <= 1. - a / 2. + 1e-12)
    cnt = counts_of(idx, B1)
    nv = cnt @ ok.astype(float)
    with np.errstate(divide='ignore', invalid='ignore'):
        cov = (cnt @ flags) / nv[:, None]
    reach = cov >= 0.95
    lev = np.where(reach.any(axis=1), CAL_LEVELS[reach.argmax(axis=1)], np.where(nv > 0, 1.0, np.nan))   # 1.0 when no level reaches 0.95
    n_one = int((lev == 1.0).sum())
    f = np.isfinite(lev)
    sd = float(np.std(lev[f], ddof=1)) if f.sum() > 1 else float('nan')
    return dict(sd=sd, mean=float(np.mean(lev[f])) if f.any() else float('nan'), n_none=n_one, n_without_valid_outer=int((~f).sum()), n_mc=int(idx.shape[0]))


def calibrate_stat(db1, j, db2=None, n_mc=B_MC):
    """The A10 section 2.6 rule for statistic j. db1: DoubleBoot with inner seed 20261913; db2: with 20261914 (or None: not run).
    Returns dict(level_used, rule, coverage_95, ...)."""
    lt = db1.p_lt[:, j]; le = db1.p_le[:, j]
    cov95 = cover_two(lt, le, 0.95)
    out = dict(coverage_95=cov95, n_outer_valid=int(np.isfinite(lt).sum()), n_outer=int(lt.size),
               coverage_95_no_tolerance=cover_two(lt, le, 0.95, tol=0.),
               coverage_95_any_outer=cover_two(db1.p_lt_any[:, j], db1.p_le_any[:, j], 0.95),
               mean_inner_valid=float(db1.n_inner_valid[:, j].mean()))
    if not np.isfinite(cov95):
        out.update(level_used=FALLBACK_LEVEL, rule='not computable (no valid outer sample): nominal 99%')
        return out
    if cov95 >= 0.94:
        out.update(level_used=0.95, rule='coverage of the nominal 95% interval >= 0.94: nominal 95%')
        return out
    lv = smallest_level(lt, le)
    out['calibrated_level'] = lv
    out['calibrated_level_no_tolerance'] = smallest_level(lt, le, tol=0.)
    out['calibrated_level_any_outer'] = smallest_level(db1.p_lt_any[:, j], db1.p_le_any[:, j])
    if lv is None:
        out.update(level_used=FALLBACK_LEVEL, rule='no level up to 0.9995 reaches coverage 0.95: nominal 99%')
        return out
    out['coverage_at_level'] = cover_two(lt, le, lv)
    mc = mc_levels(lt, le, n_mc)
    out['mc'] = mc
    ok_mc = bool(np.isfinite(mc['sd']) and mc['sd'] <= 0.002)
    if db2 is None:
        out.update(level_used=None, rule='second inner seed not run: undecided', mc_ok=ok_mc)
        return out
    lv2 = smallest_level(db2.p_lt[:, j], db2.p_le[:, j])
    out['second_seed_level'] = lv2
    out['second_seed_coverage_95'] = cover_two(db2.p_lt[:, j], db2.p_le[:, j], 0.95)
    ok2 = bool(lv2 is not None and abs(lv2 - lv) <= 0.002 + 1e-12)
    out['mc_ok'] = ok_mc; out['second_seed_ok'] = ok2
    if ok_mc and ok2:
        out.update(level_used=lv, rule='calibrated level accepted (MC SD <= 0.002 and second inner seed within 0.002)')
    else:
        out.update(level_used=FALLBACK_LEVEL, rule='calibrated level rejected (MC SD or second inner seed): nominal 99%')
    return out


# ------------------------------------------------------------------------------------------------ pod path of the double bootstrap
# --calib export: everything except the double bootstrap runs here; the job (every array the remote runner needs) is written
# to out\calib\<label>.job.npz with <label>.meta.json; rc_calib_remote_v13.py computes chunks of outer samples elsewhere;
# --calib import --calib-chunks DIR checks and merges the chunks and finishes the run. The in-process path is unchanged.
POD_SEEDS = [SEED_INNER, SEED_INNER2]
RUNNER_FILES = ['rc_calib_remote_v13.py', 'rc_kern_v13.py']


def calib_dir(test_old):
    """out\\calib for fresh runs; separate folders for old-run tests and dry runs, so their jobs never mix with real ones."""
    return OUT / ('calib_dryrun' if DRYRUN else ('calib_testold' if test_old else 'calib'))


def check_label(label):
    import re
    if not re.fullmatch(r'rc_[A-Za-z0-9][A-Za-z0-9_-]*', label or ''):
        raise SystemExit('REFUSED: a calibration label must start with rc_ and hold letters, digits, _ and - only (%r)' % label)
    return label


def calib_job_arrays(stat, full, n, n_outer, label):
    """The job's arrays. The outer estimates are computed here, by the same call as DoubleBoot.run (the whole outer set at once)."""
    idx_o = np.random.default_rng(SEED_OUTER).integers(0, n, (B_OUTER, n))[:n_outer]
    outer_est = stat(counts_of(idx_o, n))
    return outer_est


def calib_export(stat, full, n, n_outer, n_inner, label, cdir, mode, program, state=None):
    """Write <label>.job.npz, <label>.meta.json and (main-bootstrap results, reused by import) <label>.state.npz. Never overwrites."""
    cdir = pathlib.Path(cdir); cdir.mkdir(parents=True, exist_ok=True)
    jobf = cdir / (label + '.job.npz'); metaf = cdir / (label + '.meta.json'); statef = cdir / (label + '.state.npz')
    for f in (jobf, metaf, statef):
        if f.exists():
            raise SystemExit('REFUSED: %s exists (jobs are never overwritten; use another --calib-label)' % f)
    t0 = time.time()
    outer_est = calib_job_arrays(stat, full, n, n_outer, label)
    arrays = KN.job_arrays(stat, full, outer_est, n, n_outer, n_inner, SEED_OUTER, B_OUTER, B_INNER, label)
    sha = KN.save_job(jobf, arrays)
    meta = dict(label=label, kind=stat.kind, program=program, mode=mode, n_outer=int(n_outer), n_inner=int(n_inner), n_run=int(n),
                n_stat=int(len(stat.STATS)), stats=list(stat.STATS), pod_seeds=[int(s) for s in POD_SEEDS], seed_outer=int(SEED_OUTER),
                b_outer_full_draw=int(B_OUTER), b_inner_full_draw=int(B_INNER), job_file=jobf.name, job_sha256=sha,
                job_bytes=int(jobf.stat().st_size), runner_files=RUNNER_FILES,
                runner_call='python -I -B rc_calib_remote_v13.py JOBDIR %s --seeds SEED --outer LO:HI --threads 1' % label,
                chunk_name='%s_<SEED>_o<LO>_<HI>.npz' % label, written=clock(), seconds_outer_estimates=time.time() - t0,
                dryrun=bool(DRYRUN))
    write_new(metaf, meta)
    if state is not None:
        with open(statef, 'xb') as f:
            np.savez(f, job_sha256=np.array(sha), full=np.asarray(full, float), **state)
    return dict(label=label, job=str(jobf), meta=str(metaf), job_sha256=sha, n_outer=int(n_outer), n_inner=int(n_inner),
                pod_seeds=[int(s) for s in POD_SEEDS])


def calib_state(cdir, label, full, n_boot):
    """The main-bootstrap results written by export, if they belong to the job file of this label and to these full-sample
    values and this size; else None (the bootstrap is then computed again; it is deterministic)."""
    cdir = pathlib.Path(cdir)
    statef = cdir / (label + '.state.npz'); jobf = cdir / (label + '.job.npz')
    if not (statef.is_file() and jobf.is_file()):
        return None
    with np.load(statef, allow_pickle=False) as z:
        st = {k: z[k] for k in z.files}
    if (str(st['job_sha256']) != KN.sha256_file(jobf) or int(st['n_boot']) != int(n_boot)
            or not np.array_equal(st['full'], np.asarray(full, float), equal_nan=True)):
        print('note: %s does not belong to this run; the main bootstrap is computed again' % statef, flush=True)
        return None
    return st


class CalibImport:
    """Checks the job of this label against this run and reads chunk files. db(seed) -> a DoubleBoot filled from the chunks."""

    def __init__(self, stat, full, n, n_outer, n_inner, label, cdir, chunks_dir):
        cdir = pathlib.Path(cdir); self.dir = pathlib.Path(chunks_dir)
        self.label = label; self.full = np.asarray(full, float); self.n = n; self.n_outer = n_outer; self.n_inner = n_inner
        jobf = cdir / (label + '.job.npz'); metaf = cdir / (label + '.meta.json')
        if not (jobf.is_file() and metaf.is_file()):
            raise SystemExit('REFUSED: no exported job %s (run --calib export first)' % jobf)
        if not self.dir.is_dir():
            raise SystemExit('REFUSED: --calib-chunks %s is not a folder' % self.dir)
        self.sha = KN.sha256_file(jobf)
        meta = json.loads(metaf.read_text(encoding='utf-8'))
        if meta.get('job_sha256') != self.sha:
            raise SystemExit('REFUSED: %s does not have the SHA-256 that %s records' % (jobf, metaf))
        _, J = KN.load_job(jobf)
        # the job must be the job of THIS run: every array is formed again from the data and compared
        mine = KN.job_arrays(stat, full, calib_job_arrays(stat, full, n, n_outer, label), n, n_outer, n_inner, SEED_OUTER, B_OUTER,
                             B_INNER, label)
        bad = KN.same_arrays(mine, J)
        if bad:
            raise SystemExit('REFUSED: the exported job %s is not the job of this run (differing entries: %s)' % (jobf, bad))
        self.outer_est = np.asarray(J['outer_est'], float)
        self.info = dict(label=label, job=str(jobf), job_sha256=self.sha, chunks_dir=str(self.dir), seeds={})

    def db(self, seed):
        import re
        pat = re.compile(r'^%s_%d_o(\d+)_(\d+)\.npz$' % (re.escape(self.label), seed))
        found = []
        for f in sorted(self.dir.iterdir()):
            m = pat.match(f.name)
            if m:
                found.append((int(m.group(1)), int(m.group(2)), f))
        if not found:
            raise SystemExit('REFUSED: no chunk %s_%d_o<LO>_<HI>.npz in %s' % (self.label, seed, self.dir))
        found.sort(key=lambda x: (x[0], x[1]))
        d = DoubleBoot(None, self.full, self.n, seed, self.n_outer, self.n_inner)
        ns = self.full.size; pos = 0; secs = 0.; files = []
        for lo, hi, f in found:
            if lo != pos:
                raise SystemExit('REFUSED: the chunks of seed %d do not tile 0..%d: %s at %d (%s)'
                                 % (seed, self.n_outer, 'gap' if lo > pos else 'overlap', pos, f.name))
            if not (lo < hi <= self.n_outer):
                raise SystemExit('REFUSED: chunk %s is outside 0..%d' % (f.name, self.n_outer))
            with np.load(f, allow_pickle=False) as z:
                c = {k: z[k] for k in z.files}
            want = dict(label=self.label, seed=seed, lo=lo, hi=hi, n_outer=self.n_outer, n_inner=self.n_inner, job_sha256=self.sha)
            for k, v in want.items():
                got = str(c[k]) if isinstance(v, str) else int(c[k])
                if got != v:
                    raise SystemExit('REFUSED: chunk %s records %s = %s, expected %s' % (f.name, k, got, v))
            for k in KN.CHUNK_KEYS:
                if c[k].shape != (hi - lo, ns):
                    raise SystemExit('REFUSED: chunk %s: %s has shape %s' % (f.name, k, c[k].shape))
            if not np.array_equal(c['outer_est'], self.outer_est[lo:hi], equal_nan=True):
                raise SystemExit('REFUSED: chunk %s does not hold the outer estimates of this job' % f.name)
            for k in KN.CHUNK_KEYS:
                getattr(d, k)[lo:hi] = c[k]
            pos = hi; secs += float(c['seconds']); files.append(f.name)
        if pos != self.n_outer:
            raise SystemExit('REFUSED: the chunks of seed %d end at %d, not at %d (gap)' % (seed, pos, self.n_outer))
        d.done = self.n_outer; d.seconds = secs
        self.info['seeds'][str(seed)] = dict(n_chunks=len(files), cpu_seconds_sum=secs, files=files)
        print('  calibration inner seed %d: %d chunks tile 0..%d (job %s...)' % (seed, len(files), self.n_outer, self.sha[:12]), flush=True)
        return d


def needs_second_seed(db1, STATS):
    """Statistics whose coverage at the nominal 95% is below 0.94 and for which a calibrated level exists (README: --second-seed auto)."""
    return [s for j, s in enumerate(STATS) if (np.isfinite(cover_two(db1.p_lt[:, j], db1.p_le[:, j], 0.95))
                                               and cover_two(db1.p_lt[:, j], db1.p_le[:, j], 0.95) < 0.94
                                               and smallest_level(db1.p_lt[:, j], db1.p_le[:, j]) is not None)]


def set_workers(n):
    if n and n > 0:
        numba.set_num_threads(int(min(n, numba.config.NUMBA_NUM_THREADS)))
    return numba.get_num_threads()


# ------------------------------------------------------------------------------------------------ classification (A10 H3 / K2)
def classify_h3(r_ci, c_ci, delta=DELTA):
    """(a) recovers: r's lower end > 0; else (b) uninformative variation: c's lower end > delta; else (c) amplitude-limited:
    c's interval inside (-delta, delta); else (d) inconclusive."""
    rl = r_ci[0]; cl, cu = c_ci
    if np.isfinite(rl) and rl > 0:
        return 'a', 'recovers'
    if np.isfinite(cl) and cl > delta:
        return 'b', 'uninformative variation'
    if np.isfinite(cl) and np.isfinite(cu) and cl > -delta and cu < delta:
        return 'c', 'amplitude-limited'
    return 'd', 'inconclusive'


def inside(ci, delta=DELTA):
    return bool(np.isfinite(ci[0]) and np.isfinite(ci[1]) and ci[0] > -delta and ci[1] < delta)
