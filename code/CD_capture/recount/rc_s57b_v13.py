"""Recount (second program) of package CD, revision v13: the fixed sensitivities and descriptive outputs of AMENDMENT_10 section 5.7
on the lead-braking runs ("S57B" keys of A_KEYS_CD_v13.json). New file, 20 Nov 2026 (Claude Fable 5.2, claude-fable-5-2).

Written from AMENDMENT_10_v13.md (sections 2, 5.5-5.8, 10.1), CD_DEFINITIONS_v13.md, CD_DEFINITIONS_S57B_v13.md (the writer's
specification), A's interface (RESULTS_INTERFACE_v13.md, A_KEYS_CD_v13.json, gen\\supp_v13.py table code) and the methods of record
(optA_lib_v02, rev_common_v01, rev_a / rev_b / rev_e2 / rev_e3 / rev_e4 of revision_v11, a9_common_v01 / a9_1 of revision_v12).
No file under work\\CD_capture\\analysis or work\\CD_capture\\tools was opened.

Key families (in the order of the brief)
  1 pops    LB.<pop>.{R, R.ci, RR_<src>, RR_<src>.ci, n_dec}; pop in all, mov, pre, brk, stop; src in AM, CK3, E5, IMM, N, NA, Q, TG
  2 rs      LB.RS.<tau>.<A>.{rel, rel.ci, den0.dec, RR0_N, RR0_N.ci, RR0_CK3}; LB.gap2.{RR0_N, RR0_CK3, den0.dec}
  3 trunc   LB.T0/T1/T2/T5/T10/T20.{R, RR_CK3}; LB.cut5.{R, RR_CK3}
  4 caps    LB.cap5/10/15.R; LB.signed.{R, RR_N, RR_CK3}
  5 grid    LB.grid.{RR_N, RR_P, RR_NmP}; LB.hull.{R, RR_N, RR_CK3}

Shared with the first program (A10 10.1(b)): the scoring library of record optA_lib_v02 (select_grid, select_first_safe, stats_scored,
frontier, hull_frontier, levels_of, eval_scoring, dec_eq, vkey), the extracted arrays, the resample draws, and rev_common_v01.load_runs
for the old runs. Own: the row statistics of every scoring (SPrep), the gridless curves (rc_core_v13's own construction, written by
the same recount line), the point path (curve_points + gl_point), the populations, the bootstrap bookkeeping, the keys.

Usage
  rc_s57b_v13.py --test-old --record [--boot 20000]     reproduce the values of record of v11 / v12 on the 35 old runs
  rc_s57b_v13.py --test-old [--boot N] [--fam ...]      old-run values under A's keys (TESTOLD_RC_S57B_v13*.json)
  rc_s57b_v13.py [--fam ...]                            fresh runs; refuses before Lock 2 (RC_S57B_v13*.json)
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import argparse, json, pathlib, sys, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import rc_core_v13 as K                      # noqa: E402  (recount core: gate, own gridless construction, kernel)
L = K.L                                      # scoring library of record, imported unchanged

PROGRAM = 'rc_s57b_v13.py'
FAMILY = 'S57B'
TAUS = [0.5, 0.75, 1.0, 1.25, 1.5, 1.8]
A_MAIN = 6.0
M8_A = [4.0, 5.0, 7.6]
SETTINGS = [(t, A_MAIN) for t in TAUS] + [(0.75, a) for a in M8_A]
TAU_STR = {0.5: '0.5', 0.75: '0.75', 1.0: '1.0', 1.25: '1.25', 1.5: '1.5', 1.8: '1.8'}
A_STR = {6.0: '6', 4.0: '4', 5.0: '5', 7.6: '7.6'}
VMIN = 0.5
SEED_RECORD = 20261113
TS = [0., 1., 2., 5., 10., 20.]
TKEY = ['T0', 'T1', 'T2', 'T5', 'T10', 'T20']
POPS = ['all', 'mov', 'pre', 'brk', 'stop']
SRC = [('N', 'N'), ('NA', 'NA'), ('AM', 'A1'), ('CK3', 'CK3'), ('TG', 'TG'), ('Q', 'Q'), ('E5', 'E5')]     # (A's name, array name)
FAMS = ['pops', 'rs', 'trunc', 'caps', 'grid']


# The gate. The root is fixed by this file's own location (never by an environment variable), and the program refuses to run at
# all when rc_core_v13's root overrides are set (coordinator's rule of 20 Nov 2026).
if os.environ.get('RC_ARS_TRIAL') or os.environ.get('RC_DRYRUN') or os.environ.get('RC_PROGRAMME_A'):
    raise SystemExit('REFUSED: RC_ARS_TRIAL / RC_DRYRUN / RC_PROGRAMME_A must not be set for rc_s57b_v13.py (use --dryrun FOLDER)')
ROOT_FIXED = HERE.parents[2]                                   # ...\revision_v13 (recount -> CD_capture -> work -> revision_v13)
LOCK2 = ROOT_FIXED / 'LOCK_A10_2.txt'
LOCK2C = ROOT_FIXED / 'LOCK_A10_2c.txt'
ARRAYS_REAL = ROOT_FIXED / 'work' / 'CD_capture' / 'arrays'
RUNS_REAL = ROOT_FIXED / 'work' / 'CD_capture' / 'runs'
if K.ROOT13.resolve() != ROOT_FIXED.resolve() or K.ARRAYS.resolve() != ARRAYS_REAL.resolve():
    raise SystemExit('REFUSED: rc_core_v13 points at another root (%s)' % K.ROOT13)
DRY = None                                                     # set by --dryrun FOLDER: a folder outside the project, OLD runs only


def require_stage2(what):
    """The gate of this program (coordinator, 20 Nov 2026: Lock 2 has two stages and this recount is stage 2): no fresh-run file
    is opened unless BOTH revision_v13\\LOCK_A10_2.txt and revision_v13\\LOCK_A10_2c.txt exist."""
    if not (LOCK2.is_file() and LOCK2C.is_file()):
        raise SystemExit('REFUSED: %s is sealed until %s and %s both exist (stage 2 of Lock 2)' % (what, LOCK2, LOCK2C))


def dry_path(q):
    """A path of the dry run: it must lie under the --dryrun folder, outside the project, and never under the real arrays or
    runs folders. The dry run bypasses the gate by name and can therefore open nothing of a fresh run."""
    q = pathlib.Path(q).resolve()
    low = str(q).lower()
    if DRY is None or DRY not in q.parents:
        raise SystemExit('REFUSED: %s is not under the dry-run folder' % q)
    for bad in (ARRAYS_REAL, RUNS_REAL, ROOT_FIXED.parent):
        b = bad.resolve()
        if q == b or b in q.parents:
            raise SystemExit('REFUSED: a dry run may not read %s' % q)
    if 'ars_trial' in low or 'cd_capture' in low:
        raise SystemExit('REFUSED: a dry run may not read %s' % q)
    return q


def fresh_array_file(folder, rid):
    if DRY is not None:
        return dry_path(DRY / 'arrays' / folder / (rid + '.npz'))
    require_stage2('fresh-run arrays')
    return K.check_path(ARRAYS_REAL / folder / (rid + '.npz'))


def fresh_ids():
    if DRY is not None:
        d = json.loads(dry_path(DRY / 'CASES_DRYRUN.json').read_text(encoding='utf-8'))
        return sorted('pc13_%s_native' % c['case'] for c in d['cases'] if c['family'] == 'lead_braking')
    require_stage2('fresh-run arrays')
    return K.fresh_run_ids('lead_braking')


def rs_key(tau, A):
    return 'LB.RS.%s.%s' % (TAU_STR[tau], A_STR[A])


# ------------------------------------------------------------------------------------------------ loaders
def load_old():
    """The 35 old evaluation runs through the loader of record, with the tracker's lead state (v12 out\\lead), TG (v12 out\\tg),
    the reaction-and-stop clearances of record (cache packs, 61 frames) and the extended clearances of rev_e1 (out\\ext)."""
    if str(K.V11) not in sys.path:
        sys.path.insert(0, str(K.V11))
    import rev_common_v01 as C
    runs = []
    for r in C.load_runs():
        z = np.load(K.V12 / 'out' / 'lead' / (r['run'] + '.npz'), allow_pickle=False)
        t = np.load(K.V12 / 'out' / 'tg' / (r['run'] + '.npz'), allow_pickle=False)
        x = np.load(K.V11 / 'out' / 'ext' / (r['run'] + '.npz'), allow_pickle=False)
        for nm, q in (('lead', z), ('tg', t), ('ext', x)):
            if not np.array_equal(q['k'], r['k']):
                raise SystemExit('REFUSED: %s arrays of %s do not match its decisions' % (nm, r['run']))
        crit = dict(r['crit']); crit['TG'] = t['cTG2']
        rs = {}
        for (tau, A) in SETTINGS:
            kk = L.vkey(tau, A)
            rs[kk] = dict(asscored=np.asarray(r['cache'][kk], float), est=np.asarray(x['clearX_' + kk], float),
                          cens=np.asarray(x['cens_' + kk]).astype(bool))
        runs.append(dict(run=r['run'], desired=float(r['desired']), k=np.asarray(r['k']), ev=np.asarray(r['ev'], bool),
                         v0=np.asarray(r['v0'], float), clear1=r['clear1'], vbar=np.asarray(r['vbar'], float),
                         idx55=np.asarray(r['idx55']).astype(np.int64), crit=crit, ph=np.asarray(r['ph']).astype(np.int64),
                         vhat=z['vhat'], ahat_long=z['ahat_long'], lead_found=z['lead_found'].astype(bool), rs=rs))
    return runs


CRIT_MAP = {'F0': 'cF0', 'E': 'cE', 'N': 'cN', 'NA': 'cNA', 'Q': 'cQ', 'A1': 'cA1', 'CK3': 'cCK3', 'TG': 'cTG2'}


def _opt(z, key, conv, default=None):
    return conv(z[key]) if key in z.files else default


def load_fresh(variant):
    """Fresh arrays arrays\\<variant>\\<run_id>.npz (CD_DEFINITIONS 'Inputs'); gated by Lock 2."""
    runs = []
    for rid in fresh_ids():
        z = np.load(fresh_array_file(variant, rid), allow_pickle=False)
        meta = json.loads(str(z['meta']))
        if meta.get('family') != 'lead_braking' or meta.get('lead_variant'):
            raise SystemExit('REFUSED: %s is not a plain lead-braking run (meta %s)' % (rid, meta))
        des = _opt(z, 'des', lambda x: np.asarray(x, float))
        if des is not None and des.size and not np.all(des == des[0]):
            raise SystemExit('REFUSED: %s has more than one desired speed' % rid)
        runs.append(dict(run=rid, desired=(float(des[0]) if des is not None else None), k=np.asarray(z['k']),
                         ev=np.asarray(z['evaluated']).astype(bool),
                         v0=np.asarray(z['v0'], float), clear1=K.clean_clear(z['clear']), vbar=np.asarray(z['vbar'], float),
                         idx55=np.asarray(z['idx55']).astype(np.int64),
                         crit={nm: np.asarray(z[key], float) for nm, key in CRIT_MAP.items() if key in z.files},
                         ph=_opt(z, 'phase', lambda x: np.asarray(x).astype(np.int64)), vhat=_opt(z, 'vhat', lambda x: np.asarray(x, float)),
                         ahat_long=_opt(z, 'ahat_long', lambda x: np.asarray(x, float)),
                         lead_found=_opt(z, 'lead_found', lambda x: np.asarray(x).astype(bool)), rs={}))
    return runs


def attach_s57b(runs):
    """Fresh extended reaction-and-stop arrays arrays\\RSX\\<run_id>.npz (coordinator and CD_DEFINITIONS_v13.md 'Superseded
    20 Nov': the shared extended arrays, the keys of rev_e1); if that folder does not exist, arrays\\S57B\\<run_id>.npz, the
    name in CD_DEFINITIONS_S57B_v13.md section 7 (same fields). Gated by both stages of Lock 2.
    Section 7 of that file: the fields of revision_v11 out\\ext; read here: k, evaluated, clearX_<vkey> (the clearance judged
    until the stop ends, (n, 17)) and cens_<vkey>, vkey = optA_lib_v02.vkey(tau, A), for the 9 settings."""
    if DRY is not None:
        folder = 'RSX'
    else:
        require_stage2('fresh-run arrays')
        folder = 'RSX' if (ARRAYS_REAL / 'RSX').is_dir() else 'S57B'
    for r in runs:
        r['rs_folder'] = folder
        z = np.load(fresh_array_file(folder, r['run']), allow_pickle=False)
        if not (np.array_equal(z['k'], r['k']) and np.array_equal(np.asarray(z['evaluated']).astype(bool), r['ev'])):
            raise SystemExit('REFUSED: S57B arrays of %s do not match its decisions' % r['run'])
        for (tau, A) in SETTINGS:
            kk = L.vkey(tau, A)
            est = np.asarray(z['clearX_' + kk], float)
            if est.shape != (r['k'].size, 17):
                raise SystemExit('REFUSED: clearX_%s of %s has shape %s' % (kk, r['run'], est.shape))
            r['rs'][kk] = dict(est=est, cens=np.asarray(z['cens_' + kk]).astype(bool),
                               asscored=np.asarray(z['clear61_' + kk], float) if ('clear61_' + kk) in z.files else None)


# ------------------------------------------------------------------------------------------------ row statistics of a scoring
class SPrep:
    """Row statistics of one run under a scoring (a generalisation of rc_core_v13.Prep; same attributes, so that
    rc_core_v13.build_curves accepts it). For every decision and row, the contributions if that row is selected:
      RS[0] wrong go (the row is not in the scoring's safe set safe_x)
      RS[1] caution term, RS[2] caution count: from the 3 s clearance minus the gap (c1 > 0 = truly safe; oracle row = first
            truly safe row). Of record: counted on truly safe selections. signed: every decision with a truly safe row counts,
            at its signed speed difference to that row (optA_lib_v02.stats_scored, signed=True).
      RS[3] wrong go where a scoring-safe row exists.
    first_safe: the perfect oracle O of the scoring (first safe_x row in cost order, else the fallback row)."""

    def __init__(self, r, safe_x=None, gap=0., signed=False):
        c1 = r['clear1'] - gap
        vbar = r['vbar']; des = r['desired']
        n = c1.shape[0]; ar = np.arange(n)
        safe1 = c1 > 0.
        if safe_x is None:
            safe_x = safe1
        safe_x = np.asarray(safe_x, bool)
        orc = safe1.argmax(axis=1); any1 = safe1.any(axis=1); anyx = safe_x.any(axis=1)
        diff = (vbar[ar, orc][:, None] - vbar) / des
        self.n = n
        self.safe = safe_x
        self.RS = np.zeros((4, n, 17))
        self.RS[0] = ~safe_x
        if signed:
            self.RS[1] = np.where(any1[:, None], diff, 0.)
            self.RS[2] = np.broadcast_to(any1[:, None], (n, 17))
        else:
            self.RS[1] = np.where(safe1, diff, 0.)
            self.RS[2] = safe1
        self.RS[3] = anyx[:, None] & ~safe_x
        self.idx55 = np.asarray(r['idx55']).astype(np.int64)
        self.first_safe = np.where(anyx, safe_x.argmax(axis=1), self.idx55)


# ------------------------------------------------------------------------------------------------ gridless: curves, point path
def gl_curves(runs, preps, names, masks_of):
    """names -> list (one per population) of rc_core_v13.Curve. 'O' is the scoring's perfect oracle (one point)."""
    return {nm: K.build_curves(runs, preps, nm, masks_of, oracle=(nm == 'O')) for nm in names}


def curve_points(cv, w=None):
    """Operating points (caution %, wrong go %) of one curve under run weights w, and the number of decisions. The g = 0 totals,
    then the running totals after the last event of every distinct breakpoint (a9_common_v01.Gridless.curve's arithmetic)."""
    nrun = cv.T0.shape[0]
    w = np.ones(nrun) if w is None else np.asarray(w, float)
    T0 = np.tensordot(w, cv.T0, axes=(0, 0))
    T = T0[None, 1:4]
    if cv.ri.size:
        cs = np.cumsum(cv.d * w[cv.ri][:, None], axis=0)[cv.last.astype(bool)] + T0[None, 1:4]
        T = np.concatenate([T, cs], axis=0)
    n = float(T0[0])
    with np.errstate(divide='ignore', invalid='ignore'):
        return 100. * T[:, 1] / T[:, 2], 100. * T[:, 0] / n, n


def gl_point(cvs, w=None, cap=None, hull_names=()):
    """Own point path of one population: cvs name -> Curve ('F0' and 'E' required). Every other name gets F0's g = 0 point in
    front (optA_lib_v02.curves_w). Levels: 201 from F0's g = 0 caution to min(F0's, E's largest caution) (levels_of), and to
    min(that, cap) when a cap (in % caution) is given. denE = sum(F_F0 - F_E); D[a] = sum(F_F0 - F_a). Hull beside, on request."""
    pts = {a: curve_points(cv, w) for a, cv in cvs.items()}
    cF0, wF0, n = pts['F0']; cE, wE, _ = pts['E']
    c0, w0 = cF0[0], wF0[0]
    cur = {}
    for a, (c, wg, _) in pts.items():
        cur[a] = (c, wg) if a in ('F0', 'E') else (np.concatenate([[c0], c]), np.concatenate([[w0], wg]))
    with np.errstate(invalid='ignore'):
        C = min(np.nanmax(cF0), np.nanmax(cE)) if (np.isfinite(cF0).any() and np.isfinite(cE).any()) else float('nan')
    Cfull = C
    if cap is not None and np.isfinite(C):
        C = min(C, cap)
    lev = np.linspace(c0, C, L.NLEV)
    f = {a: L.frontier(cur[a][0], cur[a][1], lev) for a in cur}
    out = dict(n=n, c0=float(c0), C=float(C), C_uncapped=float(Cfull), denE=float(np.sum(f['F0'] - f['E'])),
               D={a: float(np.sum(f['F0'] - f[a])) for a in cur if a not in ('F0', 'E')},
               npts={a: int(pts[a][0].size) for a in pts})
    if hull_names:
        h0 = L.hull_frontier(cur['F0'][0], cur['F0'][1], lev)
        out['hdenE'] = float(np.sum(h0 - L.hull_frontier(cur['E'][0], cur['E'][1], lev)))
        out['hD'] = {a: float(np.sum(h0 - L.hull_frontier(cur[a][0], cur[a][1], lev))) for a in hull_names}
    return out


def gl_problem(curves, names, pi):
    """rc_kern_v13.Problem of one population: names[0] = 'F0', names[1] = 'E'."""
    assert names[0] == 'F0' and names[1] == 'E'
    return K.Problem(names, [curves[nm][pi] for nm in names])


def same(a, b):
    a = float(a); b = float(b)
    return (a == b) or (np.isnan(a) and np.isnan(b))


def check_kernel(P, pt, tag, log):
    """The kernel at unit weights against the own point path: every value must be identical (==)."""
    e = P.evaluate(np.ones((1, P.nrun)))
    bad = []
    if not same(e['denE'][0], pt['denE']):
        bad.append(('denE', float(e['denE'][0]), pt['denE']))
    for a in P.names[2:]:
        if not same(e['D'][a][0], pt['D'][a]):
            bad.append((a, float(e['D'][a][0]), pt['D'][a]))
    log.append(dict(what=tag, identical=not bad, differ=bad))
    if bad:
        md = max(abs(x[1] - x[2]) for x in bad)
        print('NOTE kernel vs point path %s: %d values differ, largest %.3g' % (tag, len(bad), md), flush=True)
        if not md < 1e-9:
            raise SystemExit('STOP: kernel and point path disagree beyond 1e-9 at %s' % tag)
    return e


# ------------------------------------------------------------------------------------------------ grid: tables and evaluation
def grid_tables(runs, names, masks_of, safe_fn=None, gap=0., signed=False):
    """names -> (nrun, G, npop, NST) summed statistics on the grid of record (G = 202; 1 for 'O'), with the library's
    select_grid / select_first_safe / stats_scored. safe_fn(run) -> the scoring's safe set (default: the 3 s clearance > gap)."""
    per = {a: [] for a in names}
    for k, r in enumerate(runs):
        c1 = r['clear1'] - gap
        sx = (c1 > 0.) if safe_fn is None else safe_fn(r)
        masks = masks_of(k)
        for a in names:
            sel = L.select_first_safe(sx, r['idx55']) if a == 'O' else L.select_grid(r['crit'][a], K.GRID, r['idx55'])
            per[a].append(L.stats_scored(sel, c1, sx, r['vbar'], r['desired'], masks, signed=signed))
    return {a: np.stack(v) for a, v in per.items()}


def grid_point(X, pop, w=None, hull_names=()):
    names = [a for a in X if a != 'F0']
    if w is None:
        T = {a: X[a].sum(axis=0)[:, pop, :] for a in X}
    else:
        T = {a: np.tensordot(w, X[a][:, :, pop, :], axes=(0, 0)) for a in X}
    return L.eval_scoring(T, names, hull_names)


def grid_boot(X, pop, CNT, hull_names=(), chunk=250):
    """Run bootstrap on the grid: per resample the summed tables (tensordot, in chunks as rev_common_v01.boot) and eval_scoring."""
    names = [a for a in X if a != 'F0']
    B = CNT.shape[0]
    out = dict(n=np.full(B, np.nan), denE=np.full(B, np.nan), D={a: np.full(B, np.nan) for a in names},
               hdenE=np.full(B, np.nan), hD={a: np.full(B, np.nan) for a in hull_names})
    for s0 in range(0, B, chunk):
        cn = CNT[s0:s0 + chunk]
        TB = {a: np.tensordot(cn, X[a][:, :, pop, :], axes=(1, 0)) for a in X}
        for b in range(cn.shape[0]):
            e = L.eval_scoring({a: TB[a][b] for a in X}, names, hull_names)
            i = s0 + b
            out['n'][i] = e['n']; out['denE'][i] = e['denE']
            for a in names:
                out['D'][a][i] = e['D'][a]
            if hull_names:
                out['hdenE'][i] = e['hdenE']
                for a in hull_names:
                    out['hD'][a][i] = e['hD'][a]
    return out


# ------------------------------------------------------------------------------------------------ small helpers
def ratio(D, den):
    return float(D / den) if (np.isfinite(den) and den > 0) else float('nan')


def pct95(b):
    return K.pct_interval(np.asarray(b, float), 0.95)


def num(x):
    """JSON value: None for anything undefined."""
    if x is None:
        return None
    if isinstance(x, (list, tuple)):
        v = [num(y) for y in x]
        return None if any(y is None for y in v) else v
    x = float(x)
    return x if np.isfinite(x) else None


def put_ci(vals, key, ci):
    vals[key + '.ci'] = num(ci)
    vals[key + '.level'] = 0.95
    vals[key + '.cal'] = 'nominal95'


def masks_pops(runs, phases):
    def f(k):
        r = runs[k]; ev = r['ev']; ph = phases[k]
        return [ev, ev & (r['v0'] > VMIN), ev & (ph == 0), ev & (ph == 1), ev & (ph == 2)]
    return f


def masks_all(runs):
    return lambda k: [runs[k]['ev']]


def trunc_masks(runs, phase_key='ph'):
    """rev_b_truncation_phase_scale_v01 R12a: every evaluated decision before the lead's stop, and the after-stop ones whose tick
    is less than T after the run's first stored after-stop decision ((k - k_stop) * 0.05 s < T - 1e-9)."""
    def f(k):
        r = runs[k]; ph = r[phase_key]; kk = r['k']; ev = r['ev']
        i2 = np.nonzero(ph == 2)[0]
        since = (kk - int(kk[i2[0]])) * L.H if i2.size else np.full(kk.shape, np.nan)
        with np.errstate(invalid='ignore'):
            return [ev & ((ph != 2) | (since < T - 1e-9)) for T in TS]
    return f


def cut5_masks(runs, phase_key='ph'):
    """CD_DEFINITIONS_S57B section 5 (no method of record): the recording is treated as ending 5 s after k_stop (the run's first
    stored decision with truth phase 2); an evaluated decision is kept iff its 3 s window ends by then:
    no k_stop, or (k - k_stop) * 0.05 + 3 <= 5 + 1e-9."""
    def f(k):
        r = runs[k]; ph = r[phase_key]; kk = r['k']; ev = r['ev']
        i2 = np.nonzero(ph == 2)[0]
        if not i2.size:
            return [ev.copy()]
        since = (kk - int(kk[i2[0]])) * L.H
        return [ev & (since + 3. <= 5. + 1e-9)]
    return f


def rs_safe(r, tau, A, variant='est', gap=0.):
    kk = L.vkey(tau, A)
    if variant == 'asscored':
        return K.clean_clear(r['rs'][kk]['asscored']) > gap
    sx = K.clean_clear(r['rs'][kk]['est']) > gap
    if variant == 'cens':
        sx = sx & ~(r['rs'][kk]['cens'] & r['ev'][:, None])
    return sx


# ================================================================================================ values of record (old runs)
def record_tests(runs, a, log):
    """Reproduce the values of record of v11 / v12 on the 35 old runs: the conventions of record (grid step frontier unless the
    record is gridless, truth phases, the draw of record default_rng(20261113), 20,000 run resamples)."""
    t00 = time.time()
    n = len(runs)
    CNT = K.boot_counts(n, 20000, SEED_RECORD)[:a.boot]
    full = (a.boot == 20000)
    rows = []

    def cmp(name, here, rec, tol=1e-9, exact=False):
        if isinstance(rec, (list, tuple)):
            for i, (h, q) in enumerate(zip(here, rec)):
                cmp('%s[%d]' % (name, i), h, q, tol, exact)
            return
        here = float(here); rec = float(rec)
        d = 0. if same(here, rec) else abs(here - rec)
        rows.append(dict(name=name, here=here, record=rec, absdiff=d, ok=bool((d == 0.) if exact else (d <= tol))))

    def J(p):
        return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
    truth = [r['ph'] for r in runs]
    mp = masks_pops(runs, truth)
    PN = ['all', 'moving', 'phase0', 'phase1', 'phase2']
    for r in runs:
        r['crit']['P'] = r['crit']['F0'] / (K.RATIO ** 2)

    # ---- 5 (first: cheap) grid placebo, v12 A9-1(a); hull, Option A main results of record
    a91 = J(K.V12 / 'out' / 'A9_1_PLACEBO_GRIDLESS_v01.json')
    X = grid_tables(runs, ['F0', 'E', 'O', 'N', 'P', 'NA', 'A1', 'CK3', 'Q', 'TG'], mp)
    for pi, pn in enumerate(PN):
        e = grid_point(X, pi); rec = a91['a_placebo_grid'][pn]
        cmp('grid %s n' % pn, e['n'], rec['n'], exact=True); cmp('grid %s R_pp' % pn, e['denE'] / L.NLEV, rec['R_pp'])
        for x in ('N', 'P', 'NA', 'A1', 'CK3', 'Q'):
            cmp('grid %s RR_%s' % (pn, x), ratio(e['D'][x], e['denE']), rec['RR_' + x]['point'])
        cmp('grid %s RR_N_minus_P' % pn, ratio(e['D']['N'] - e['D']['P'], e['denE']), rec['RR_N_minus_P']['point'])
    Xs = {x: X[x] for x in ('F0', 'E', 'N', 'P', 'CK3')}
    b = grid_boot(Xs, 0, CNT)
    if full:
        rec = a91['a_placebo_grid']['all']
        cmp('grid all RR_N ci', pct95(K.ratio_arr(b['D']['N'], b['denE'])), rec['RR_N']['ci'])
        cmp('grid all RR_P ci', pct95(K.ratio_arr(b['D']['P'], b['denE'])), rec['RR_P']['ci'])
        cmp('grid all RR_N_minus_P ci', pct95(K.ratio_arr(b['D']['N'] - b['D']['P'], b['denE'])), rec['RR_N_minus_P']['ci'])
        cmp('grid all R ci', pct95(b['denE'] / L.NLEV), rec['R']['ci'])
        cmp('grid all RR_CK3 ci', pct95(K.ratio_arr(b['D']['CK3'], b['denE'])), rec['RR_CK3']['ci'])
    bW = b                                                           # the 3 s reference of the reaction-and-stop ratios
    eW = grid_point(X, 0)
    opt = J(K.P / '11_ojits' / 'A6R' / 'run' / 'OPTIONA_MAIN_RESULTS_v02.json')['part1']['scorings']['W1']['pops']
    for pi, pn in enumerate(PN):
        e = grid_point({x: X[x] for x in ('F0', 'E', 'O', 'N', 'NA', 'CK3', 'A1', 'Q')}, pi, hull_names=('O', 'N', 'NA', 'CK3', 'A1', 'Q'))
        rec = opt[pn]
        cmp('hull %s hdenE' % pn, e['hdenE'], rec['hdenE']); cmp('hull %s hden0' % pn, e['hD']['O'], rec['hden0'])
        for x in ('N', 'NA', 'CK3', 'A1', 'Q'):
            cmp('hull %s hrr0_%s' % (pn, x), ratio(e['hD'][x], e['hD']['O']), rec['arms'][x]['hrr0']['point'])
    a97 = J(K.V12 / 'out' / 'A9_7B_TIMEGAP_SCORE_v01.json')['w1']
    for pi, pn in enumerate(PN):
        e = grid_point(X, pi)
        cmp('grid %s RR_TG2' % pn, ratio(e['D']['TG'], e['denE']), a97[pn]['RR_TG2']['point'])
        cmp('grid %s D_TG2_deceq' % pn, L.dec_eq(e['D']['TG'], e['n']), a97[pn]['D_TG2_deceq'])
    print('record: grid placebo, hull, TG done (%.0f s)' % (time.time() - t00), flush=True)

    # ---- 1 gridless populations of record (truth phases), v12 A9-1(c)
    preps = [SPrep(r) for r in runs]
    gn = ['F0', 'E', 'N', 'P', 'NA', 'A1', 'CK3', 'Q']
    cv = gl_curves(runs, preps, gn, mp)
    for pi, pn in enumerate(PN):
        e = gl_point({x: cv[x][pi] for x in gn}); rec = a91['c_gridless'][pn]
        check_kernel(gl_problem(cv, gn, pi), e, 'record gridless %s' % pn, log)
        cmp('gridless %s n' % pn, e['n'], rec['n'], exact=True); cmp('gridless %s R_pp' % pn, e['denE'] / L.NLEV, rec['R_pp'])
        for x in gn[2:]:
            cmp('gridless %s RR_%s' % (pn, x), ratio(e['D'][x], e['denE']), rec['RR_' + x])
    nb = min(2000, a.boot)
    bg = gl_problem(cv, gn, 0).evaluate(CNT[:nb])
    if nb == 2000:
        rec = a91['c_gridless']['all_intervals']
        cmp('gridless all R ci (first 2000)', pct95(bg['denE'] / L.NLEV), rec['R']['ci'])
        for x in gn[2:]:
            cmp('gridless all RR_%s ci (first 2000)' % x, pct95(K.ratio_arr(bg['D'][x], bg['denE'])), rec['RR_' + x]['ci'])
        cmp('gridless all RR_N_minus_P ci (first 2000)', pct95(K.ratio_arr(bg['D']['N'] - bg['D']['P'], bg['denE'])),
            rec['RR_N_minus_P']['ci'])
    print('record: gridless populations done (%.0f s)' % (time.time() - t00), flush=True)

    # ---- 3 truncation, v11 rev_b R12a (grid, truth phase)
    rb = J(K.V11 / 'out' / 'REV_B_TRUNC_PHASESCALE_v01.json')['R12a']
    tm = trunc_masks(runs)
    XT = grid_tables(runs, ['F0', 'E', 'O', 'CK3', 'N'], tm)
    for i, tk in enumerate(TKEY):
        e = grid_point(XT, i); rec = rb[tk]
        cmp('trunc %s n' % tk, e['n'], rec['n'], exact=True); cmp('trunc %s R_pp' % tk, e['denE'] / L.NLEV, rec['R_pp'])
        cmp('trunc %s RR_CK3' % tk, ratio(e['D']['CK3'], e['denE']), rec['arms']['CK3']['rrE']['point'])
        cmp('trunc %s RR0_CK3' % tk, ratio(e['D']['CK3'], e['D']['O']), rec['arms']['CK3']['rr0']['point'])
        if full:
            bt = grid_boot({x: XT[x] for x in ('F0', 'E', 'CK3')}, i, CNT)
            cmp('trunc %s RR_CK3 ci' % tk, pct95(K.ratio_arr(bt['D']['CK3'], bt['denE'])), rec['arms']['CK3']['rrE']['ci'])
            cmp('trunc %s R_pp ci' % tk, pct95(bt['denE'] / L.NLEV), rec['denE']['R_pp_ci'])
    print('record: truncation done (%.0f s)' % (time.time() - t00), flush=True)

    # ---- 4 signed caution, v11 rev_a R11 (grid)
    ra = J(K.V11 / 'out' / 'REV_A_SIGNED_GAP_v01.json')
    XS = grid_tables(runs, ['F0', 'E', 'O', 'N', 'CK3'], mp, signed=True)
    for pi, pn in enumerate(PN):
        e = grid_point(XS, pi); rec = ra['R11']['W1_signed'][pn]
        cmp('signed %s R_pp' % pn, e['denE'] / L.NLEV, rec['denE']['R_pp'])
        cmp('signed %s RR_N' % pn, ratio(e['D']['N'], e['denE']), rec['arms']['N']['rrE']['point'])
        cmp('signed %s RR_CK3' % pn, ratio(e['D']['CK3'], e['denE']), rec['arms']['CK3']['rrE']['point'])
    print('record: signed caution done (%.0f s)' % (time.time() - t00), flush=True)

    # ---- 2 reaction-and-stop grid (plans judged until their stop ends), v11 rev_e2; 2 m gap, rev_e3 and rev_e4; rev_a R17
    re2 = J(K.V11 / 'out' / 'REV_E2_EXTENDED_TRUTH_v01.json')['scorings']
    ma = masks_all(runs)
    for (tau, A) in SETTINGS:
        kk = L.vkey(tau, A); rec = re2['est_' + kk]['pops']['all']
        XR = grid_tables(runs, ['F0', 'E', 'O', 'N', 'CK3'], ma, safe_fn=lambda r: rs_safe(r, tau, A, 'est'))
        e = grid_point(XR, 0)
        cmp('rs est %s n' % kk, e['n'], rec['n'], exact=True)
        cmp('rs est %s denE_over_3s' % kk, ratio(e['denE'], eW['denE']), rec['denE_over_3s']['point'])
        cmp('rs est %s den0 dec_eq' % kk, L.dec_eq(e['D']['O'], e['n']), rec['den0']['dec_eq'])
        cmp('rs est %s RR0_N' % kk, ratio(e['D']['N'], e['D']['O']), rec['arms']['N']['rr0']['point'])
        cmp('rs est %s RR0_CK3' % kk, ratio(e['D']['CK3'], e['D']['O']), rec['arms']['CK3']['rr0']['point'])
        if full and re2['est_' + kk]['bootstrap']:
            bt = grid_boot(XR, 0, CNT)
            cmp('rs est %s denE_over_3s ci' % kk, pct95(K.ratio_arr(bt['denE'], bW['denE'])), rec['denE_over_3s']['ci'])
            cmp('rs est %s RR0_N ci' % kk, pct95(K.ratio_arr(bt['D']['N'], bt['D']['O'])), rec['arms']['N']['rr0']['ci'])
            cmp('rs est %s RR0_CK3 ci' % kk, pct95(K.ratio_arr(bt['D']['CK3'], bt['D']['O'])), rec['arms']['CK3']['rr0']['ci'])
            cmp('rs est %s den0 dec_eq ci' % kk, pct95(L.dec_eq(bt['D']['O'], bt['n'])), rec['den0']['dec_eq_ci'])
        print('record: reaction-and-stop %s done (%.0f s)' % (kk, time.time() - t00), flush=True)
    re3 = J(K.V11 / 'out' / 'REV_E3_EXTENDED_GAP2_v01.json')['pops']['all']
    XG = grid_tables(runs, ['F0', 'E', 'O', 'N', 'CK3'], ma, safe_fn=lambda r: rs_safe(r, 0.75, 6.0, 'est', 2.0), gap=2.0)
    e = grid_point(XG, 0)
    cmp('gap2 est den0 dec_eq', L.dec_eq(e['D']['O'], e['n']), re3['den0']['dec_eq'])
    cmp('gap2 est RR0_N', ratio(e['D']['N'], e['D']['O']), re3['arms']['N']['rr0']['point'])
    cmp('gap2 est RR0_CK3', ratio(e['D']['CK3'], e['D']['O']), re3['arms']['CK3']['rr0']['point'])
    if full:
        bt = grid_boot(XG, 0, CNT)
        cmp('gap2 est RR0_N ci', pct95(K.ratio_arr(bt['D']['N'], bt['D']['O'])), re3['arms']['N']['rr0']['ci'])
        cmp('gap2 est RR0_CK3 ci', pct95(K.ratio_arr(bt['D']['CK3'], bt['D']['O'])), re3['arms']['CK3']['rr0']['ci'])
    re4 = J(K.V11 / 'out' / 'REV_E4_GAP2_CENS_UNSAFE_v01.json')['pops']['all']
    XG = grid_tables(runs, ['F0', 'E', 'O', 'N', 'CK3'], ma, safe_fn=lambda r: rs_safe(r, 0.75, 6.0, 'cens', 2.0), gap=2.0)
    e = grid_point(XG, 0)
    cmp('gap2 cens-unsafe den0 dec_eq', L.dec_eq(e['D']['O'], e['n']), re4['den0_dec_eq'])
    cmp('gap2 cens-unsafe RR0_N', ratio(e['D']['N'], e['D']['O']), re4['arms']['N']['rr0'])
    cmp('gap2 cens-unsafe RR0_CK3', ratio(e['D']['CK3'], e['D']['O']), re4['arms']['CK3']['rr0'])
    r17 = ra['R17']['WR_t0p75_a6p0_gap2']['all']
    XG = grid_tables(runs, ['F0', 'E', 'O', 'N', 'CK3'], ma, safe_fn=lambda r: rs_safe(r, 0.75, 6.0, 'asscored', 2.0), gap=2.0)
    e = grid_point(XG, 0)
    cmp('gap2 as-scored den0 dec_eq', L.dec_eq(e['D']['O'], e['n']), r17['den0']['dec_eq'])
    cmp('gap2 as-scored RR0_N', ratio(e['D']['N'], e['D']['O']), r17['arms']['N']['rr0']['point'])
    cmp('gap2 as-scored RR0_CK3', ratio(e['D']['CK3'], e['D']['O']), r17['arms']['CK3']['rr0']['point'])
    print('record: 2 m gap done (%.0f s)' % (time.time() - t00), flush=True)
    nbad = sum(not x['ok'] for x in rows)
    return dict(n_compared=len(rows), n_differ=nbad, max_absdiff=max(x['absdiff'] for x in rows), boot=a.boot,
                draw='default_rng(20261113), the draw of record', rows=rows)


# ================================================================================================ checks of the key path (old runs)
def checks_old(runs, imm, conv):
    """Checks of the constructions the keys use, on the 35 old runs, points only (no value of record exists for them):
    (1) grid identity: every gridless curve, read at the 202 grid scales (state after every breakpoint below the scale), equals the
        grid table of the library (select_grid + stats_scored) for the same scoring and population: counts exactly, the caution
        sum within 1e-9. Covers SPrep for W1, the signed caution, the reaction-and-stop scoring, the 2 m gap, and every mask.
    (2) library of record: the own point path (curve_points + gl_point) against a9_common_v01.gridless_sources +
        optA_lib_v02.eval_scoring for the scorings a9 can express (W1 populations, IMM, est, 2 m gap, truncation, cut5)."""
    t00 = time.time()
    rows = []
    est = [K.est_phase(r['vhat'], r['ahat_long'], r['lead_found'], conv['phase_thr']) for r in runs]
    u, _ = K.e5_u(runs, 'F0', 'E')
    for r, uu in zip(runs, u):
        r['crit']['E5'] = K.oracle_crit(r['crit']['F0'], K.RATIO, K.E5_AMP, uu)
    mp = masks_pops(runs, est); ma = masks_all(runs); tm = trunc_masks(runs); cm = cut5_masks(runs)
    mpI = lambda k: [m & imm[k]['ev'] for m in mp(k)]                                # noqa: E731
    src = ['F0', 'E', 'N', 'NA', 'A1', 'CK3', 'TG', 'Q', 'E5']
    GAP = 2.0
    cases = [
        ('W1 populations', runs, src, mp, dict(), None, 0.),
        ('W1 IMM populations', imm, ['F0', 'E', 'N'], mpI, dict(), None, 0.),
        ('W1 truncation', runs, ['F0', 'E', 'CK3'], tm, dict(), None, 0.),
        ('W1 cut5', runs, ['F0', 'E', 'CK3'], cm, dict(), None, 0.),
        ('W1 signed', runs, ['F0', 'E', 'N', 'CK3'], ma, dict(signed=True), None, 0.),
        ('est t0p75_a6p0', runs, ['F0', 'E', 'O', 'N', 'CK3'], ma, dict(), (0.75, 6.0, 'est'), 0.),
        ('est t1p80_a6p0', runs, ['F0', 'E', 'O', 'N', 'CK3'], ma, dict(), (1.8, 6.0, 'est'), 0.),
        ('est t0p75_a4p0', runs, ['F0', 'E', 'O', 'N', 'CK3'], ma, dict(), (0.75, 4.0, 'est'), 0.),
        ('gap2 est t0p75_a6p0', runs, ['F0', 'E', 'O', 'N', 'CK3'], ma, dict(), (0.75, 6.0, 'est'), GAP),
        ('gap2 cens-unsafe t0p75_a6p0', runs, ['F0', 'E', 'O', 'N', 'CK3'], ma, dict(), (0.75, 6.0, 'cens'), GAP),
    ]
    A9 = K.try_a9()
    for label, rr, names, mfn, kw, rs, gap in cases:
        signed = bool(kw.get('signed'))
        sfn = (lambda r, rs=rs, gap=gap: rs_safe(r, rs[0], rs[1], rs[2], gap)) if rs else None
        preps = [SPrep(r, sfn(r) if sfn else None, gap=gap, signed=signed) for r in rr]
        cv = gl_curves(rr, preps, names, mfn)
        X = grid_tables(rr, names, mfn, safe_fn=sfn, gap=gap, signed=signed)
        npop = len(mfn(0))
        # (1) grid identity
        dcount = 0.; dsum = 0.; nval = 0
        for a_ in names:
            for pi in range(npop):
                c = cv[a_][pi]
                T0 = c.T0.sum(axis=0)
                Tr = X[a_].sum(axis=0)[:, pi, :]
                if a_ == 'O':
                    Tg = np.broadcast_to(T0[None, 1:4], (1, 3))
                else:
                    cs = np.concatenate([np.zeros((1, 3)), np.cumsum(c.d, axis=0)]) if c.ri.size else np.zeros((1, 3))
                    j = np.searchsorted(c.b, K.GRID, side='left') if c.ri.size else np.zeros(K.GRID.size, int)
                    Tg = T0[None, 1:4] + cs[j]
                dcount = max(dcount, float(np.abs(Tg[:, [0, 2]] - Tr[:, [1, 3]]).max()), float(np.abs(T0[0] - Tr[:, 0]).max()))
                dsum = max(dsum, float(np.abs(Tg[:, 1] - Tr[:, 2]).max()))
                nval += Tg.size
        rows.append(dict(check='grid identity', case=label, n_values=nval, max_abs_diff_counts=dcount, max_abs_diff_caution_sum=dsum,
                         ok=bool(dcount == 0. and dsum <= 1e-9)))
        # (2) library of record
        if A9 is not None and not signed:
            lib = []
            for k, r in enumerate(rr):
                q = dict(r); q['clear1'] = r['clear1'] - gap; q['_m'] = tuple(mfn(k)); q['_sx'] = sfn(r) if sfn else (q['clear1'] > 0.)
                lib.append(q)
            G = A9.gridless_sources(lib, names, lambda q: q['_sx'], masks_key='_m')
            md = 0.; nv = 0
            for pi in range(npop):
                e = L.eval_scoring({a_: G[a_].curve(None, pops=[pi])[:, 0, :] for a_ in names}, [a_ for a_ in names if a_ != 'F0'])
                pt = gl_point({a_: cv[a_][pi] for a_ in names})
                pairs = [(pt['denE'], e['denE']), (pt['n'], e['n'])] + [(pt['D'][a_], e['D'][a_]) for a_ in names if a_ not in ('F0', 'E')]
                for h, q in pairs:
                    nv += 1
                    if not same(h, q):
                        md = max(md, abs(h - q))
            rows.append(dict(check='library of record (a9 gridless + eval_scoring) vs own point path', case=label, n_values=nv,
                             max_abs_diff=md, identical=bool(md == 0.), ok=bool(md <= 1e-9)))
        print('check %s done (%.0f s)' % (label, time.time() - t00), flush=True)
    return dict(n_checks=len(rows), n_failed=sum(not x['ok'] for x in rows), rows=rows)


# ================================================================================================ the keys
def load_old_imm(runs):
    """Old-run stand-in of the frozen IMM: package B's B1 re-track arrays (B_retrack\\out\\retrack\\B1), same decisions."""
    out = []
    for r in runs:
        z = np.load(K.ROOT13 / 'work' / 'B_retrack' / 'out' / 'retrack' / 'B1' / (r['run'] + '_arrays.npz'), allow_pickle=False)
        if not np.array_equal(z['k'], r['k']):
            raise SystemExit('REFUSED: B1 arrays of %s do not describe the same decisions' % r['run'])
        out.append(dict(run=r['run'], desired=r['desired'], k=r['k'], ev=np.asarray(z['evaluated']).astype(bool),
                        v0=np.asarray(z['v0'], float), clear1=K.clean_clear(z['clear']),
                        vbar=np.asarray(z['vbar'], float), idx55=np.asarray(z['idx55']).astype(np.int64),
                        crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float)}))
    return out


class BootStore:
    """Resample results by label. Mode 'compute': evaluate the rows LO..HI-1 of the draw and keep them (a chunk writes them to a
    file). Mode 'merge': return the rows read from the chunk files, concatenated in row order. A resample result is
    dict(n, denE, D={name: array}) as rc_kern_v13.Problem.evaluate returns it."""

    def __init__(self, data=None):
        self.merge = data is not None
        self.d = {} if data is None else data

    def get(self, label, fn):
        if self.merge:
            if label not in self.d:
                raise SystemExit('REFUSED: the chunk files hold no resamples for %s' % label)
            return self.d[label]
        self.d[label] = fn()
        return self.d[label]

    def flat(self):
        out = {}
        for lab, e in self.d.items():
            out[lab + '|n'] = e['n']; out[lab + '|denE'] = e['denE']
            for x, v in e['D'].items():
                out[lab + '|D|' + x] = v
        return out

    @staticmethod
    def unflat(parts):
        """parts: list of dicts of arrays (chunks in row order) -> label -> dict(n, denE, D)."""
        keys = list(parts[0].keys())
        if any(set(q.keys()) != set(keys) for q in parts):
            raise SystemExit('REFUSED: the chunk files do not hold the same resample arrays')
        d = {}
        for kx in keys:
            v = np.concatenate([q[kx] for q in parts])
            t = kx.split('|')
            e = d.setdefault(t[0], dict(D={}))
            if t[1] == 'D':
                e['D'][t[2]] = v
            else:
                e[t[1]] = v
        return d


def chunk_file(base, lo, hi):
    return K.OUT / ('%s_rows_%05d_%05d.npz' % (base, lo, hi))


def load_chunks(base, seed, n, nboot, fams):
    """All chunk files of this output name; they must tile rows 0..nboot-1 and carry the same seed, run count and families."""
    got = []
    for f in sorted(K.OUT.glob(base + '_rows_*.npz')):
        z = np.load(f, allow_pickle=False)
        m = json.loads(str(z['meta']))
        if m['seed'] != seed or m['n_runs'] != n or m['families'] != fams or m['program'] != PROGRAM:
            raise SystemExit('REFUSED: chunk %s was written for other settings (%s)' % (f.name, m))
        got.append((m['lo'], m['hi'], {kx: z[kx] for kx in z.files if kx != 'meta'}, f.name, m))
    got.sort(key=lambda x: x[0])
    pos = 0
    for lo, hi, _, name, _ in got:
        if lo != pos:
            raise SystemExit('REFUSED: the chunk files do not tile the rows (at row %d, file %s)' % (pos, name))
        pos = hi
    if pos != nboot:
        raise SystemExit('REFUSED: the chunk files cover rows 0..%d, not 0..%d' % (pos - 1, nboot - 1))
    return BootStore.unflat([g[2] for g in got]), [dict(file=g[3], lo=g[0], hi=g[1], program_sha256=g[4].get('program_sha256')) for g in got]


def compute_keys(runs, imm, a, seed, fams, conv, log, store=None, rows=None):
    """Values under A's keys. conv: the conventions that A10 and the methods of record leave open (README, 'Conventions')."""
    t00 = time.time()
    vals = {}; det = {}
    n = len(runs)
    store = BootStore() if store is None else store
    lo, hi = (0, a.boot) if rows is None else rows
    CNT = None if store.merge else K.boot_counts(n, 20000, seed)[lo:hi]
    det['bootstrap'] = dict(draw='default_rng(%d).integers(0, %d, (20000, %d)), rows 0..%d' % (seed, n, n, a.boot - 1), n=a.boot,
                            interval='np.percentile over finite resamples, 2.5 / 97.5 (nominal 95%)')
    ev_all = masks_all(runs)
    est = [K.est_phase(r['vhat'], r['ahat_long'], r['lead_found'], conv['phase_thr']) for r in runs]
    u, uinfo = K.e5_u(runs, 'F0', 'E')
    for r, uu in zip(runs, u):
        r['crit']['E5'] = K.oracle_crit(r['crit']['F0'], K.RATIO, K.E5_AMP, uu)
        r['crit']['P'] = r['crit']['F0'] / (K.RATIO ** 2)
    det['E5'] = dict(uinfo, m=K.RATIO, A=K.E5_AMP)
    preps = [SPrep(r) for r in runs]
    mp = masks_pops(runs, est)
    ref = {}

    def w1_ref():
        """The 3 s commitment on all evaluated decisions: curves of F0 and E, point and resamples of D(E, F0)."""
        if not ref:
            cv = gl_curves(runs, preps, ['F0', 'E'], ev_all)
            pt = gl_point({x: cv[x][0] for x in ('F0', 'E')})
            P = gl_problem(cv, ['F0', 'E'], 0)
            check_kernel(P, pt, 'W1 all (F0, E)', log)
            ref.update(cv={x: cv[x][0] for x in ('F0', 'E')}, pt=pt,
                       bt=(store.get('W1all', lambda: P.evaluate(CNT)) if 'rs' in fams else None))   # resamples only for rel
        return ref

    # ---------------------------------------------------------------- 1 populations
    if 'pops' in fams:
        names = ['F0', 'E'] + [arr for _, arr in SRC if all(arr in r['crit'] for r in runs)]
        cv = gl_curves(runs, preps, names, mp)
        cvI = None
        if imm is not None:
            # the CV0 populations (the same decisions in every row of the table), and B1's own evaluated flag where it differs
            mpI = lambda k: [m & imm[k]['ev'] for m in mp(k)]                        # noqa: E731
            cvI = gl_curves(imm, [SPrep(q) for q in imm], ['F0', 'E', 'N'], mpI)
            det['IMM_arrays'] = dict(
                n_decisions_evaluated_differs=int(sum(int((r['ev'] != q['ev']).sum()) for r, q in zip(runs, imm))),
                runs_v0_differs=int(sum(not np.array_equal(r['v0'], q['v0'], equal_nan=True) for r, q in zip(runs, imm))),
                runs_clear_differs=int(sum(not np.array_equal(r['clear1'], q['clear1'], equal_nan=True) for r, q in zip(runs, imm))),
                runs_vbar_differs=int(sum(not np.array_equal(r['vbar'], q['vbar'], equal_nan=True) for r, q in zip(runs, imm))),
                runs_idx55_differs=int(sum(not np.array_equal(r['idx55'], q['idx55']) for r, q in zip(runs, imm))))
        det['pops'] = {}
        for pi, pop in enumerate(POPS):
            pre = 'LB.%s.' % pop
            pt = gl_point({x: cv[x][pi] for x in names})
            nd = int(round(pt['n']))
            vals[pre + 'n_dec'] = nd
            d = dict(n=nd, denE=pt['denE'], D=pt['D'], c0=pt['c0'], C=pt['C'], npts=pt['npts'])
            if nd == 0:
                vals[pre + 'R'] = None; put_ci(vals, pre + 'R', None)
                for an, _ in SRC + [('IMM', None)]:
                    vals[pre + 'RR_' + an] = None; put_ci(vals, pre + 'RR_' + an, None)
                det['pops'][pop] = d
                continue
            P = gl_problem(cv, names, pi)
            check_kernel(P, pt, 'pops %s' % pop, log)
            bt = store.get('pops_' + pop, lambda: P.evaluate(CNT))
            vals[pre + 'R'] = num(pt['denE'] / L.NLEV); put_ci(vals, pre + 'R', pct95(bt['denE'] / L.NLEV))
            d['R_dec'] = L.dec_eq(pt['denE'], pt['n'])
            d['share_resamples_denE_le0'] = float(np.mean(~(bt['denE'] > 0)))
            for an, arr in SRC:
                if arr in names:
                    vals[pre + 'RR_' + an] = num(ratio(pt['D'][arr], pt['denE']))
                    put_ci(vals, pre + 'RR_' + an, pct95(K.ratio_arr(bt['D'][arr], bt['denE'])))
                else:
                    vals[pre + 'RR_' + an] = None; put_ci(vals, pre + 'RR_' + an, None)
            if cvI is not None:
                ptI = gl_point({x: cvI[x][pi] for x in ('F0', 'E', 'N')})
                PI = gl_problem(cvI, ['F0', 'E', 'N'], pi)
                check_kernel(PI, ptI, 'pops %s IMM' % pop, log)
                btI = store.get('imm_' + pop, lambda: PI.evaluate(CNT))
                vals[pre + 'RR_IMM'] = num(ratio(ptI['D']['N'], ptI['denE']))
                put_ci(vals, pre + 'RR_IMM', pct95(K.ratio_arr(btI['D']['N'], btI['denE'])))
                d['IMM'] = dict(n=ptI['n'], denE=ptI['denE'], D_N=ptI['D']['N'], R_pp=ptI['denE'] / L.NLEV)
            else:
                vals[pre + 'RR_IMM'] = None; put_ci(vals, pre + 'RR_IMM', None)
            det['pops'][pop] = d
            if pop == 'all':
                ref.update(cv={x: cv[x][0] for x in ('F0', 'E')}, pt=pt, bt=bt)
            print('pops %s done (%.0f s): n %d, R %.4f pp' % (pop, time.time() - t00, nd, pt['denE'] / L.NLEV), flush=True)

    # ---------------------------------------------------------------- 2 reaction-and-stop grid, 2 m gap
    if 'rs' in fams:
        W = w1_ref()
        nm = ['F0', 'E', 'O', 'N', 'CK3']
        extra = [(an, arr) for an, arr in SRC if arr not in nm and arr != 'E5' and all(arr in r['crit'] for r in runs)]
        nmx = nm + [arr for _, arr in extra]                                   # A10 5.7: RR0 "for every source" (details)
        det['rs'] = dict(variant=conv['rs_variant'], W1_denE=W['pt']['denE'])
        for (tau, A) in SETTINGS:
            key = rs_key(tau, A)
            pr = [SPrep(r, rs_safe(r, tau, A, conv['rs_variant'])) for r in runs]
            cvr = gl_curves(runs, pr, nmx, ev_all)
            pt = gl_point({x: cvr[x][0] for x in nmx})
            den0 = pt['D']['O']
            vals[key + '.rel'] = num(ratio(pt['denE'], W['pt']['denE']))
            vals[key + '.den0.dec'] = num(L.dec_eq(den0, pt['n']))
            vals[key + '.RR0_N'] = num(ratio(pt['D']['N'], den0))
            vals[key + '.RR0_CK3'] = num(ratio(pt['D']['CK3'], den0))
            d = dict(n=pt['n'], denE=pt['denE'], den0=den0, D_N=pt['D']['N'], D_CK3=pt['D']['CK3'],
                     evaluable=bool(L.dec_eq(den0, pt['n']) >= L.MIN_DEC_EQ),
                     decisions_without_safe_row=int(sum(int((r['ev'] & ~p.safe.any(axis=1)).sum()) for r, p in zip(runs, pr))),
                     RR0_other_sources={an: ratio(pt['D'][arr], den0) for an, arr in extra},
                     censored_pairs=int(sum(int((r['rs'][L.vkey(tau, A)]['cens'] & r['ev'][:, None]).sum()) for r in runs)))
            if all(r['rs'][L.vkey(tau, A)].get('asscored') is not None for r in runs):
                pa = [SPrep(r, rs_safe(r, tau, A, 'asscored')) for r in runs]         # the 3 s window's flags (comparison only)
                cva = gl_curves(runs, pa, nm, ev_all)
                qa = gl_point({x: cva[x][0] for x in nm})
                d['as_scored_3s_window'] = dict(rel=ratio(qa['denE'], W['pt']['denE']), den0_dec=L.dec_eq(qa['D']['O'], qa['n']),
                                                RR0_N=ratio(qa['D']['N'], qa['D']['O']), RR0_CK3=ratio(qa['D']['CK3'], qa['D']['O']))
            if A == A_MAIN:
                P = gl_problem(cvr, nm, 0)
                check_kernel(P, pt, 'rs %s' % key, log)
                bt = store.get('rs_' + key, lambda: P.evaluate(CNT))
                put_ci(vals, key + '.rel', pct95(K.ratio_arr(bt['denE'], W['bt']['denE'])))
                put_ci(vals, key + '.RR0_N', pct95(K.ratio_arr(bt['D']['N'], bt['D']['O'])))
                d['share_resamples_den0_le0'] = float(np.mean(~(bt['D']['O'] > 0)))
                d['den0_dec_ci'] = pct95(L.dec_eq(bt['D']['O'], bt['n']))
            det['rs'][key] = d
            print('rs %s done (%.0f s)' % (key, time.time() - t00), flush=True)
        GAP = 2.0
        pr = [SPrep(r, rs_safe(r, 0.75, 6.0, conv['gap2_variant'], GAP), gap=GAP) for r in runs]
        cvr = gl_curves(runs, pr, nm, ev_all)
        pt = gl_point({x: cvr[x][0] for x in nm})
        den0 = pt['D']['O']
        vals['LB.gap2.den0.dec'] = num(L.dec_eq(den0, pt['n']))
        vals['LB.gap2.RR0_N'] = num(ratio(pt['D']['N'], den0))
        vals['LB.gap2.RR0_CK3'] = num(ratio(pt['D']['CK3'], den0))
        det['rs']['LB.gap2'] = dict(variant=conv['gap2_variant'], n=pt['n'], denE=pt['denE'], den0=den0, D_N=pt['D']['N'],
                                    D_CK3=pt['D']['CK3'], evaluable=bool(L.dec_eq(den0, pt['n']) >= L.MIN_DEC_EQ))
        pr = [SPrep(r, rs_safe(r, 0.75, 6.0, 'cens', GAP), gap=GAP) for r in runs]            # rev_e4: censored pairs unsafe
        cvr = gl_curves(runs, pr, nm, ev_all)
        pt = gl_point({x: cvr[x][0] for x in nm})
        det['rs']['LB.gap2 censored pairs unsafe (rev_e4 sensitivity)'] = dict(
            den0_dec=L.dec_eq(pt['D']['O'], pt['n']), RR0_N=ratio(pt['D']['N'], pt['D']['O']), RR0_CK3=ratio(pt['D']['CK3'], pt['D']['O']))

    # ---------------------------------------------------------------- 3 after-stop truncation
    if 'trunc' in fams:
        nm = ['F0', 'E', 'CK3']
        tm = trunc_masks(runs, conv['trunc_phase'])
        cvt = gl_curves(runs, preps, nm, tm)
        det['trunc'] = dict(phase=conv['trunc_phase'])
        for i, tk in enumerate(TKEY):
            pt = gl_point({x: cvt[x][i] for x in nm})
            vals['LB.%s.R' % tk] = num(pt['denE'] / L.NLEV)
            vals['LB.%s.RR_CK3' % tk] = num(ratio(pt['D']['CK3'], pt['denE']))
            det['trunc'][tk] = dict(n=pt['n'], denE=pt['denE'], D_CK3=pt['D']['CK3'])
        cvc = gl_curves(runs, preps, nm, cut5_masks(runs, conv['trunc_phase']))
        pt = gl_point({x: cvc[x][0] for x in nm})
        vals['LB.cut5.R'] = num(pt['denE'] / L.NLEV)
        vals['LB.cut5.RR_CK3'] = num(ratio(pt['D']['CK3'], pt['denE']))
        det['trunc']['cut5'] = dict(n=pt['n'], denE=pt['denE'], D_CK3=pt['D']['CK3'],
                                    rule='evaluated and (no k_stop or (k - k_stop) * 0.05 + 3 <= 5 + 1e-9), truth phase')
        det['trunc']['runs_without_after_stop_decision'] = [r['run'] for r in runs if not (r[conv['trunc_phase']] == 2).any()]
        print('trunc done (%.0f s)' % (time.time() - t00), flush=True)

    # ---------------------------------------------------------------- 4 caution caps, signed caution
    if 'caps' in fams:
        W = w1_ref()
        det['caps'] = {}
        for cap in (5, 10, 15):
            pt = gl_point(W['cv'], cap=float(cap))
            vals['LB.cap%d.R' % cap] = num(pt['denE'] / L.NLEV) if cap > pt['c0'] else None      # empty window: null
            det['caps']['cap%d' % cap] = dict(denE=pt['denE'], c0=pt['c0'], C=pt['C'], C_uncapped=pt['C_uncapped'])
        nm = ['F0', 'E', 'N', 'CK3']
        cvs = gl_curves(runs, [SPrep(r, signed=True) for r in runs], nm, ev_all)
        pt = gl_point({x: cvs[x][0] for x in nm})
        vals['LB.signed.R'] = num(pt['denE'] / L.NLEV)
        vals['LB.signed.RR_N'] = num(ratio(pt['D']['N'], pt['denE']))
        vals['LB.signed.RR_CK3'] = num(ratio(pt['D']['CK3'], pt['denE']))
        det['caps']['signed'] = dict(n=pt['n'], denE=pt['denE'], D=pt['D'], c0=pt['c0'], C=pt['C'])
        print('caps, signed done (%.0f s)' % (time.time() - t00), flush=True)

    # ---------------------------------------------------------------- 5 grid frontier, placebo, hull
    if 'grid' in fams:
        X = grid_tables(runs, ['F0', 'E', 'N', 'P', 'CK3'], ev_all)
        e = grid_point(X, 0, hull_names=('N', 'CK3'))
        vals['LB.grid.RR_N'] = num(ratio(e['D']['N'], e['denE']))
        vals['LB.grid.RR_P'] = num(ratio(e['D']['P'], e['denE']))
        vals['LB.grid.RR_NmP'] = num(ratio(e['D']['N'] - e['D']['P'], e['denE']))
        vals['LB.hull.R'] = num(e['hdenE'] / L.NLEV)
        vals['LB.hull.RR_N'] = num(ratio(e['hD']['N'], e['hdenE']))
        vals['LB.hull.RR_CK3'] = num(ratio(e['hD']['CK3'], e['hdenE']))
        det['grid'] = dict(n=e['n'], denE=e['denE'], R_pp=e['denE'] / L.NLEV, D=e['D'], hdenE=e['hdenE'], hD=e['hD'],
                           placebo_factor=K.RATIO ** 2, hull='lower convex envelope of the grid points (optA_lib_v02.hull_frontier)')
        if conv.get('hull_gridless_beside'):
            W = w1_ref()
            cvh = gl_curves(runs, preps, ['F0', 'E', 'N', 'CK3'], ev_all)
            ph = gl_point({x: cvh[x][0] for x in ('F0', 'E', 'N', 'CK3')}, hull_names=('N', 'CK3'))
            det['grid']['hull_on_gridless_points'] = dict(hdenE=ph['hdenE'], R_pp=ph['hdenE'] / L.NLEV,
                                                          RR_N=ratio(ph['hD']['N'], ph['hdenE']), RR_CK3=ratio(ph['hD']['CK3'], ph['hdenE']))
        print('grid, hull done (%.0f s)' % (time.time() - t00), flush=True)
    det['_store'] = store
    return vals, det


def make_dryrun(scratch):
    """DRY RUN folder of the fresh-run path, OUTSIDE the project, filled with OLD runs relabelled: CASES_DRYRUN.json (35 made-up
    lead-braking cases), arrays\\CV0, arrays\\B1 (package B's old B1 re-track arrays) and arrays\\RSX (the old extended
    clearances of rev_e1). No lock-like file is written and nothing of a fresh run is read. The program is then run with
    --dryrun <folder>: the gate is bypassed by that flag, the output is named DRYRUN_* and says so inside."""
    scratch = pathlib.Path(scratch).resolve()
    low = str(scratch).lower()
    if 'ars_trial' in low or 'cd_capture' in low or ROOT_FIXED.parent.resolve() in [scratch] + list(scratch.parents):
        raise SystemExit('REFUSED: the dry-run folder must be outside the project')
    for v in ('CV0', 'B1', 'RSX'):
        (scratch / 'arrays' / v).mkdir(parents=True, exist_ok=True)
    old = load_old(); imm = load_old_imm(old)
    cases = []
    for i, (r, q) in enumerate(zip(old, imm)):
        case = 'dryrun_lead_%04d' % i; rid = 'pc13_%s_native' % case
        cases.append(dict(case=case, family='lead_braking', old_run=r['run']))
        meta = json.dumps(dict(family='lead_braking', run_id=rid, case=case, lead_variant=None, dryrun_of=r['run']))
        des = np.full(r['ev'].size, r['desired'])
        np.savez(scratch / 'arrays' / 'CV0' / (rid + '.npz'), k=r['k'], evaluated=r['ev'], v0=r['v0'], des=des, clear=r['clear1'],
                 vbar=r['vbar'], idx55=r['idx55'], cF0=r['crit']['F0'], cE=r['crit']['E'], cN=r['crit']['N'], cNA=r['crit']['NA'],
                 cQ=r['crit']['Q'], cA1=r['crit']['A1'], cCK3=r['crit']['CK3'], cTG2=r['crit']['TG'], phase=r['ph'].astype(np.int8),
                 lead_found=r['lead_found'], vhat=r['vhat'], ahat_long=r['ahat_long'], meta=meta)
        np.savez(scratch / 'arrays' / 'B1' / (rid + '.npz'), k=q['k'], evaluated=q['ev'], v0=q['v0'], des=des, clear=q['clear1'],
                 vbar=q['vbar'], idx55=q['idx55'], cF0=q['crit']['F0'], cE=q['crit']['E'], cN=q['crit']['N'], meta=meta)
        x = dict(k=r['k'], evaluated=r['ev'], meta=meta)
        for kk, d in r['rs'].items():
            x['clearX_' + kk] = d['est']; x['cens_' + kk] = d['cens']; x['clear61_' + kk] = d['asscored']
        np.savez(scratch / 'arrays' / 'RSX' / (rid + '.npz'), **x)
    (scratch / 'CASES_DRYRUN.json').write_text(json.dumps(dict(schema='DRYRUN, old runs relabelled', cases=cases), indent=1),
                                               encoding='utf-8')
    print('dry-run folder written: %s (%d lead runs; old runs only; no lock-like file)' % (scratch, len(old)))


CONV = dict(
    phase_thr=-1.0,                 # A10 2.4: populations pre / brk / stop by the tracker's estimate
    rs_variant='est',               # A10 1: plans judged until the stop ends (the extended clearance); 'asscored' = 3 s window
    gap2_variant='est',             # rev_e3: the extended clearance > 2 m and the 3 s clearance > 2 m for the caution
    trunc_phase='ph',               # rev_b R12a: the truth phase of record
    cut5='CD_DEFINITIONS_S57B section 5: recording ends 5 s after k_stop; a decision is kept iff its 3 s window fits',
    caps='CD_DEFINITIONS_S57B section 6: levels linspace(c0, min(C, cap), 201); null if cap <= c0',
    hull_gridless_beside=True,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--record', action='store_true', help='with --test-old: reproduce the values of record of v11 / v12')
    ap.add_argument('--boot', type=int, default=20000)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--fam', default=','.join(FAMS))
    ap.add_argument('--tag', default='')
    ap.add_argument('--checks', action='store_true', help='with --test-old: grid identity and library checks of the key path')
    ap.add_argument('--rows', default='', help='LO:HI: evaluate only these rows of the draw and write a chunk file (no values)')
    ap.add_argument('--chunk-tag', default=None, help='with --merge: the tag of the chunk files, if it differs from --tag')
    ap.add_argument('--merge', action='store_true', help='take the resamples from the chunk files of this output name')
    ap.add_argument('--make-dryrun', default='', help='write a folder (outside the project) with OLD runs relabelled')
    ap.add_argument('--dryrun', default='', help='DRY RUN of the fresh-run path on that folder (old runs relabelled); bypasses '
                                                 'the gate by name, writes DRYRUN_*, reads nothing under the real arrays or runs')
    ap.add_argument('--seed', type=int, default=0, help='bootstrap seed (default: 20261911 fresh, 20261113 old runs)')
    a = ap.parse_args()
    if a.make_dryrun:
        make_dryrun(a.make_dryrun)
        return
    if a.rows and a.merge:
        raise SystemExit('REFUSED: --rows and --merge exclude each other')
    global DRY
    if a.dryrun:
        if a.test_old or a.record or a.checks:
            raise SystemExit('REFUSED: --dryrun exercises the fresh-run path only')
        DRY = pathlib.Path(a.dryrun).resolve()
        dry_path(DRY / 'CASES_DRYRUN.json')
    if a.workers > 2:
        raise SystemExit('REFUSED: at most 2 workers on the shared laptop')
    nthreads = K.set_workers(a.workers)
    t00 = time.time()
    log = []
    if a.record:
        if not a.test_old:
            raise SystemExit('REFUSED: --record needs --test-old')
        outf = K.OUT / ('TESTOLD_RC_S57B_v13_RECORD%s.json' % a.tag)
        if outf.exists():
            raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % outf)
        runs = load_old()
        res = record_tests(runs, a, log)
        doc = dict(family=FAMILY, program=PROGRAM, test_old=True, what='values of record of v11 / v12 reproduced on the 35 old runs',
                   model='claude-fable-5-2', threads=nthreads, values={},
                   details=dict(record=res, kernel_vs_point_path=log, runs=[r['run'] for r in runs]),
                   written=K.clock(), seconds=time.time() - t00)
        print('record tests: %d values compared, %d differ beyond tolerance, largest |diff| %.3g' % (
            res['n_compared'], res['n_differ'], res['max_absdiff']))
        for x in res['rows']:
            if not x['ok']:
                print('  DIFF %s: here %.15g record %.15g' % (x['name'], x['here'], x['record']))
        print('written %s (%.0f s)' % (K.write_new(outf, doc), time.time() - t00))
        return
    if a.checks:
        if not a.test_old:
            raise SystemExit('REFUSED: --checks needs --test-old')
        outf = K.OUT / ('TESTOLD_RC_S57B_v13_CHECKS%s.json' % a.tag)
        if outf.exists():
            raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % outf)
        runs = load_old()
        res = checks_old(runs, load_old_imm(runs), CONV)
        doc = dict(family=FAMILY, program=PROGRAM, test_old=True, what='checks of the key path on the 35 old runs (points)',
                   model='claude-fable-5-2', values={}, details=dict(checks=res, runs=[r['run'] for r in runs]),
                   written=K.clock(), seconds=time.time() - t00)
        for x in res['rows']:
            print('  %s | %s | %s' % ('ok  ' if x['ok'] else 'FAIL', x['check'], {k: v for k, v in x.items() if k not in ('check', 'ok')}))
        print('checks: %d, failed %d; written %s (%.0f s)' % (res['n_checks'], res['n_failed'], K.write_new(outf, doc), time.time() - t00))
        return
    fams = [f for f in a.fam.split(',') if f]
    if any(f not in FAMS for f in fams):
        raise SystemExit('REFUSED: --fam takes %s' % FAMS)
    seed = a.seed if a.seed else (SEED_RECORD if a.test_old else K.SEED_BOOT)
    base = ('TESTOLD_RC_S57B_v13' if a.test_old else ('DRYRUN_RC_S57B_v13' if DRY is not None else 'RC_S57B_v13')) + a.tag
    outf = K.OUT / (base + '.json')
    if outf.exists():
        raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % outf)
    if a.test_old:
        runs = load_old()
        imm = load_old_imm(runs)
    else:
        if DRY is None:
            require_stage2('fresh lead-braking arrays')       # before anything else: nothing of a fresh run is opened
        runs = load_fresh('CV0')
        imm = load_fresh('B1')
        for r, q in zip(runs, imm):
            if not (r['run'] == q['run'] and np.array_equal(r['k'], q['k'])):
                raise SystemExit('REFUSED: CV0 and B1 arrays of %s do not describe the same decisions' % r['run'])
            if q['desired'] is None:
                q['desired'] = r['desired']
            elif q['desired'] != r['desired']:
                raise SystemExit('REFUSED: CV0 and B1 arrays of %s differ in the desired speed' % r['run'])
        if any(r['desired'] is None or r['ph'] is None or r['vhat'] is None for r in runs):
            raise SystemExit('REFUSED: a CV0 array lacks des, phase or the lead state')
        if 'rs' in fams or 'trunc' in fams:
            attach_s57b(runs)
    rows = None; store = None
    if a.rows:
        lo, hi = (int(x) for x in a.rows.split(':'))
        if not (0 <= lo < hi <= a.boot):
            raise SystemExit('REFUSED: --rows LO:HI needs 0 <= LO < HI <= --boot')
        rows = (lo, hi)
        cf = chunk_file(base, lo, hi)
        if cf.exists():
            raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % cf)
    if a.merge:
        cbase = base if a.chunk_tag is None else base[:len(base) - len(a.tag)] + a.chunk_tag
        data, chunks = load_chunks(cbase, seed, len(runs), a.boot, fams)
        store = BootStore(data)
    vals, det = compute_keys(runs, imm, a, seed, fams, CONV, log, store=store, rows=rows)
    store = det.pop('_store')
    if rows is not None:
        meta = dict(program=PROGRAM, program_sha256=L.sha256_file(HERE / PROGRAM), seed=seed, n_runs=len(runs), families=fams,
                    lo=rows[0], hi=rows[1], test_old=bool(a.test_old), dryrun=bool(DRY is not None), written=K.clock())
        with open(cf, 'xb') as f:
            np.savez(f, meta=json.dumps(meta), **store.flat())
        print('chunk rows %d..%d written: %s (%.0f s); no value is reported from a chunk' % (rows[0], rows[1] - 1, cf, time.time() - t00))
        return
    if a.merge:
        det['bootstrap']['chunks'] = chunks
    det['kernel_vs_point_path'] = log
    # CD_DEFINITIONS_S57B section 0 (revision of 20 Nov 03:40): only keys of A's key list go to values; the rest stays in details
    klist = json.loads((ROOT_FIXED / 'work' / 'CD_capture' / 'export' / 'A_KEYS_CD_v13.json').read_text(encoding='utf-8'))
    akeys = set(e['key'] for lst in klist['keys'].values() for e in lst)
    stem = lambda k: k[:-6] if k.endswith('.level') else (k[:-4] if k.endswith('.cal') else k)      # noqa: E731
    det['values_not_in_key_list'] = {k: v for k, v in vals.items() if stem(k) not in akeys}
    vals = {k: v for k, v in vals.items() if stem(k) in akeys}
    det['key_list'] = dict(file='export\\A_KEYS_CD_v13.json', sha256=L.sha256_file(ROOT_FIXED / 'work' / 'CD_capture' / 'export' / 'A_KEYS_CD_v13.json'),
                           n_keys_written=sum(1 for k in vals if stem(k) == k))
    det['conventions'] = {k: (v if not callable(v) else v.__name__) for k, v in CONV.items()}
    det['runs'] = [r['run'] for r in runs]
    det['rs_arrays'] = ('revision_v11 out\\ext (extended clearances of record)' if a.test_old
                        else 'arrays\\%s' % runs[0].get('rs_folder', '(not read)'))
    det['counts'] = dict(n_runs=len(runs), n_decisions=int(sum(r['ev'].size for r in runs)),
                         n_evaluated=int(sum(int(r['ev'].sum()) for r in runs)))
    doc = dict(family=FAMILY, program=PROGRAM, test_old=bool(a.test_old), model='claude-fable-5-2', threads=nthreads,
               dryrun=('OLD runs relabelled as fresh in a scratch tree; NOT fresh data' if DRY is not None else False),
               families=fams, seed=seed, values=vals, details=det, written=K.clock(), seconds=time.time() - t00)
    print('%d keys; written %s (%.0f s)' % (len(vals), K.write_new(outf, doc), time.time() - t00))


if __name__ == '__main__':
    main()
