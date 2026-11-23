"""Recount (second program) of package CD, revision v13: the A10 section 5.7 keys of A's interface that package CD owns
("S57A"). New file, 20 Nov 2026 (Claude Fable 5.2). AMENDMENT_10_v13 section 10.1(b).

Scope (coordinator decision of 20 Nov 2026, 01:53 EST; the keys LB.RS075.*, LB.T*, LB.DS.*, LB.REL_* and TU.* went to package B and
are NOT computed here; the earlier full-scope version of this file is kept as superseded_rc_s57a_v13_fullscope_20261120_0231.txt):
  sec_dec   decision-equivalent versions of printed shares:
            LB.R.dec; LB.RR_N.dec, LB.RR_E5.dec, LB.RR_E5mP.dec, LB.RR_CK3.dec, LB.IMM.r.dec, LB.IMM.c.dec (+ .dec.ci)
  sec_ps    H4 on the grid: LB.PS.rec.dec (+ .ci) and the transferred single scale LB.PS.single (+ .ci)
  sec_po    partial oracles 25 / 50 / 75% and the grading check: LB.PO*, LB.<pop>.PO* (pop = all, mov, pre, brk, stop),
            LB.grading_ok, LB.<pop>.grading_ok
  sec_ci    cut-in event window: CI.RR_CK3, CI.RR_E5, CI.RR_E5mP (+ .ci); CI.RR_N.dec (+ .ci); CI.Y.R.dec; CI.PO*, CI.grading_ok

Written from AMENDMENT_10_v13.md, CD_DEFINITIONS_v13.md, the writer's specification CD_DEFINITIONS_S57A_v13.md, A's interface
(RESULTS_INTERFACE_v13.md, A_KEYS_CD_v13.json) and the methods of record revision_v11\\analysis\\rev_g_partial_oracle_draws_v01.py
and revision_v12\\analysis\\a9_8_grading_before_stop_v01.py. No first program of work\\CD_capture\\analysis or work\\CD_capture\\tools
was read. Reused: the scoring library of record optA_lib_v02 (imported unchanged); the earlier recount modules rc_core_v13 /
rc_kern_v13 (own gridless kernel, E5 family, phase estimate), rc_c_lead_v13 (H4 design and transfer) and rc_c_cutin_v13 (event tick,
track age, populations); extracted arrays as data. Implemented here: the masks, the partial-oracle draw and critical scales, the grid
tables, the decision-equivalents, the intervals, the old-run stand-ins.

Gate: the fresh path refuses unless BOTH revision_v13\\LOCK_A10_2.txt and LOCK_A10_2c.txt (the latter in revision_v13 or in
revision_v13\\work\\locks) exist (two-stage Lock 2,
README_COORDINATION 20 Nov 01:53 EST: this code is frozen in FREEZE_CD_2, and no fresh C value is computed between the two locks).

Usage (python -I -B -X utf8):
  rc_s57a_v13.py --selftest                 the partial oracles of record on the 35 old runs (REV_G, A9-8), draw 20261118
  rc_s57a_v13.py --test-old [--boot N] [--old-seed S]
                                            old runs under A's keys -> out\\TESTOLD_RC_S57A_v13<tag>.json
  rc_s57a_v13.py [--boot N]                 fresh runs -> out\\RC_S57A_v13<tag>.json
  rc_s57a_v13.py --make-dry DIR             write OLD runs in the fresh-array format into DIR (a folder outside the project)
  rc_s57a_v13.py --dry-run DIR [--boot N]   the FRESH code path on that folder: the gate is bypassed by this flag by name, nothing
                                            under work/CD_capture/arrays or runs can be read; output out/DRYRUN_RC_S57A_v13<tag>.json
  --only dec,ps,po,ci                       sections to run (default all);  --workers N (at most 2);  --tag TEXT
  --levels-lead FILE / --levels-cutin FILE  optional: take the level of each .dec.ci from the calibration of an rc_c_lead_v13 /
                                            rc_c_cutin_v13 output (default: nominal 95%, as the writer's specification)
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import argparse, json, math, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))                    # python -I: the script folder is not on sys.path
if os.environ.get('RC_ARS_TRIAL') or os.environ.get('RC_DRYRUN') or os.environ.get('RC_PROGRAMME_A'):
    raise SystemExit('REFUSED: RC_ARS_TRIAL / RC_DRYRUN / RC_PROGRAMME_A are set; this program never takes its roots or its gate '
                     'from the environment (dry runs: --dry-run DIR)')
import rc_core_v13 as K                          # noqa: E402

L = K.L
NLEV = K.NLEV
OUT = K.OUT
LOCK2C = (K.ROOT13 / 'LOCK_A10_2c.txt', K.ROOT13 / 'work' / 'locks' / 'LOCK_A10_2c.txt')
B_RETRACK = K.ROOT13 / 'work' / 'B_retrack' / 'out' / 'retrack'
REPL_C = K.CD / 'REPLACEMENTS_C_v13.json'

SEED_PO_FRESH = 20261919
SEED_PO_RECORD = 20261118
SEED_RECORD = 20261113
PO_P = (0.25, 0.5, 0.75); PO_NM = ('P25', 'P50', 'P75')
VMIN = 0.5
LB_POPS = ('all', 'mov', 'pre', 'brk', 'stop')
SECTIONS = ('dec', 'ps', 'po', 'ci')


def log(*a):
    print(*a, flush=True)


def require_locks(what):
    """Both stages of Lock 2 must exist before anything of a fresh run is opened."""
    K.require_lock2(what)
    if not any(f.is_file() for f in LOCK2C):
        raise SystemExit('REFUSED: %s is sealed until LOCK_A10_2c.txt exists in %s or %s (two-stage Lock 2; this code belongs '
                         'to stage 2)' % (what, LOCK2C[0].parent, LOCK2C[1].parent))


def deceq(D, n):
    """Decision-equivalents of a sum over the 201 levels: D / 201 / 100 * n."""
    return np.asarray(D, float) / NLEV / 100. * np.asarray(n, float)


def fnum(x):
    """float, or None for anything not finite (the interface's null)."""
    x = float(x)
    return x if math.isfinite(x) else None


def ci_of(b, level=0.95):
    c = K.pct_interval(np.asarray(b, float), level)
    return [fnum(c[0]), fnum(c[1])]


def cal_name(lv):
    return 'nominal95' if abs(lv - 0.95) < 1e-12 else ('nominal99' if abs(lv - 0.99) < 1e-12 else 'calibrated')


def put(V, key, pt, bs, lv=0.95):
    V[key] = fnum(pt); V[key + '.ci'] = ci_of(bs, lv); V[key + '.level'] = lv; V[key + '.cal'] = cal_name(lv)


# ================================================================================================ gridless and grid helpers
def problems(runs, names, masks):
    """One rc_kern_v13.Problem per population (3 s commitment). names[0] plays F0, names[1] plays E; every other source gets
    F0's g = 0 point in front. masks: per run a list of (n,) bool arrays."""
    preps = [K.Prep(r) for r in runs]
    mfn = lambda k: masks[k]                                    # noqa: E731
    cur = {nm: K.build_curves(runs, preps, nm, mfn) for nm in names}
    return [K.Problem(list(names), [cur[nm][pi] for nm in names]) for pi in range(len(masks[0]))]


def ev_point(P, n):
    e = P.evaluate(np.ones((1, n)))
    return dict(n=float(e['n'][0]), denE=float(e['denE'][0]), D={a: float(v[0]) for a, v in e['D'].items()})


def share(D, den):
    return L.ratio(D, den)


def grid_tables(runs, names, masks):
    """{name: (202, npop, 5)} pooled statistics on the grid of record [0] + logspace(-2, 3, 201): optA_lib_v02.select_grid and
    stats_scored (3 s commitment), summed over the runs in order."""
    out = {}
    for a in names:
        acc = None
        for r, m in zip(runs, masks):
            sel = L.select_grid(r['crit'][a], K.GRID, r['idx55'])
            t = L.stats_scored(sel, r['clear1'], r['clear1'] > 0., r['vbar'], r['desired'], tuple(m))
            acc = t if acc is None else acc + t
        out[a] = acc
    return out


# ================================================================================================ loaders
def load_old_eval():
    """The 35 old evaluation runs (rev_common_v01.load_runs, the loader of record) with the tracker's lead state (v12 out\\lead)."""
    if str(K.V11) not in sys.path:
        sys.path.insert(0, str(K.V11))
    import rev_common_v01 as C
    runs = []
    for r in C.load_runs():
        z = np.load(K.V12 / 'out' / 'lead' / (r['run'] + '.npz'), allow_pickle=False)
        if not np.array_equal(z['k'], r['k']):
            raise SystemExit('REFUSED: lead arrays of %s do not match its decisions' % r['run'])
        runs.append(dict(run=r['run'], desired=float(r['desired']), k=np.asarray(r['k']), ev=np.asarray(r['ev'], bool),
                         v0=np.asarray(r['v0'], float), clear1=r['clear1'], vbar=r['vbar'],
                         idx55=np.asarray(r['idx55']).astype(np.int64), crit=dict(r['crit']),
                         ph=np.asarray(r['ph']).astype(np.int64), vhat=z['vhat'], ahat_long=z['ahat_long'],
                         lead_found=z['lead_found'].astype(bool), n_dec=int(len(r['k']))))
    return runs


def b_arrays(variant, run, ref, what=('cF0', 'cE', 'cN')):
    """Package B's re-track arrays of an old run, accepted only if they describe the stored decisions: equal k and, for the
    arrays named in what, the same NaN and infinity pattern and finite values within 1e-12 of the stored ones (writer's
    specification, sections 9 and 10)."""
    z = np.load(B_RETRACK / variant / (run + '_arrays.npz'), allow_pickle=False)
    if not np.array_equal(z['k'], ref['k']):
        raise SystemExit('REFUSED: B %s arrays of %s do not have the stored decisions' % (variant, run))
    mx = 0.
    for key in what:
        a = np.asarray(z[key], float); b = np.asarray(ref['crit'][key[1:]], float)
        fa = np.isfinite(a); fb = np.isfinite(b)
        if not (np.array_equal(np.isnan(a), np.isnan(b)) and np.array_equal(fa, fb) and np.array_equal(a[~fa], b[~fb], equal_nan=True)):
            raise SystemExit('REFUSED: B %s arrays of %s: %s has another NaN / infinity pattern than the stored one' % (variant, run, key))
        if fa.any():
            d = np.abs(a[fa] - b[fa])
            mx = max(mx, float(np.max(d)))
            # accepted when within 1e-12 absolutely OR relatively: on the cut-in tuning runs B's cF0 (rebuilt class average)
            # differs from the stored one by up to 8.2e-12 on scales of several hundred (1.1e-14 relative); cE and cN are equal
            if np.any((d > 1e-12) & (d > 1e-12 * np.abs(b[fa]))):
                raise SystemExit('REFUSED: B %s arrays of %s: %s differs from the stored one by %.3g' % (variant, run, key, float(np.max(d))))
    return z, mx


def b_variant_run(variant, r):
    """A run dict from package B's re-track arrays of tracker variant x (its own F0_x, E_x, N_x) for the decisions of r."""
    z = np.load(B_RETRACK / variant / (r['run'] + '_arrays.npz'), allow_pickle=False)
    if not (np.array_equal(z['k'], r['k']) and np.array_equal(np.asarray(z['evaluated']).astype(bool), r['ev'])):
        raise SystemExit('REFUSED: B %s arrays of %s do not describe the same decisions' % (variant, r['run']))
    return dict(run=r['run'], desired=float(np.asarray(z['des'], float)[0]), k=np.asarray(z['k']), ev=r['ev'],
                clear1=L.clean_clear(z['clear']), vbar=np.asarray(z['vbar'], float), idx55=np.asarray(z['idx55']).astype(np.int64),
                n_dec=int(len(z['k'])), crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float),
                                              'N': np.asarray(z['cN'], float)})


def fresh_ids(family):
    """Run ids of a family in ascending order: CASES_C_v13.json; if REPLACEMENTS_C_v13.json exists, the ids present in
    arrays/CV0 with that family in their meta (pc13_*_native, no lead variant), which must number as many as the case list;
    the differences from the case list are returned for the record."""
    ids = K.fresh_run_ids(family)
    if not REPL_C.is_file():
        return ids, None
    require_locks('fresh-run arrays')
    have = []
    for f in sorted((K.ARRAYS / 'CV0').glob('pc13_*_native.npz')):
        with np.load(f, allow_pickle=False) as z:
            meta = json.loads(str(z['meta']))
        if meta.get('family') == family and not meta.get('lead_variant'):
            have.append(f.stem)
    have = sorted(have)
    if len(have) != len(ids):
        raise SystemExit('REFUSED: %d %s runs in arrays/CV0, expected %d' % (len(have), family, len(ids)))
    return have, dict(replacements_file=str(REPL_C), dropped=sorted(set(ids) - set(have)), added=sorted(set(have) - set(ids)))


def dry_root(d):
    """A dry-run folder: outside the project trees, not named like the fresh arrays or runs, holding no lock-like file."""
    d = pathlib.Path(d).resolve()
    low = str(d).lower()
    for bad in (str(K.ARS.resolve()).lower(), str(K.P.resolve()).lower()):
        if low == bad or low.startswith(bad + os.sep):
            raise SystemExit('REFUSED: the dry-run folder must be outside the project trees (%s)' % d)
    if 'cd_capture' in low or low.endswith(os.sep + 'arrays') or low.endswith(os.sep + 'runs'):
        raise SystemExit('REFUSED: the dry-run folder must not be named like the fresh arrays or runs (%s)' % d)
    if d.is_dir() and any(f.name.upper().startswith(('LOCK_', 'FREEZE_')) for f in d.rglob('*')):
        raise SystemExit('REFUSED: the dry-run folder holds a file named like a lock or a freeze (%s)' % d)
    return d


def make_dry(d):
    """OLD runs in the fresh-array format (CD_DEFINITIONS 'Inputs'): DIR/CV0/<old run>.npz for the 35 old evaluation runs
    (family lead_braking) and the 20 cut-in tuning runs (family cutin; cCK3 from package B's CV0 re-track arrays), DIR/B1/<old
    run>.npz for the lead runs (package B's B1 re-track arrays). Run ids are the OLD run names and every meta says it is a dry
    run. No lock-like file is written. 'clear' holds the cleaned clearance (cleaning it again changes nothing)."""
    d = dry_root(d)
    for sub in ('CV0', 'B1'):
        (d / sub).mkdir(parents=True, exist_ok=True)
    note = 'DRY RUN: an OLD run in the fresh-array format; NOT fresh data'

    def save(f, r, meta, extra):
        if f.exists():
            raise SystemExit('REFUSED: %s exists' % f)
        with open(f, 'xb') as fh:
            np.savez_compressed(fh, meta=json.dumps(meta), k=r['k'], evaluated=r['ev'].astype(np.int8),
                                des=np.full(r['n_dec'], r['desired']), clear=r['clear1'], vbar=r['vbar'], idx55=r['idx55'],
                                cF0=r['crit']['F0'], cE=r['crit']['E'], cN=r['crit']['N'], **extra)
    lead = load_old_eval()
    for r in lead:
        m = dict(family='lead_braking', run_id=r['run'], lead_variant=None, dry_run=note)
        save(d / 'CV0' / (r['run'] + '.npz'), r, m, dict(v0=r['v0'], cCK3=r['crit']['CK3'], phase=r['ph'], vhat=r['vhat'],
                                                         ahat_long=r['ahat_long'], lead_found=r['lead_found']))
        save(d / 'B1' / (r['run'] + '.npz'), b_variant_run('B1', r), m, dict(v0=r['v0']))
    cut = K.load_old_cutin_runs()
    for r in cut:
        r['n_dec'] = int(len(r['k']))
        z, _ = b_arrays('CV0', r['run'], r)
        m = dict(family='cutin', run_id=r['run'], lead_variant=None, dry_run=note, rd=str(r['rd']), cap=str(r['cap']))
        save(d / 'CV0' / (r['run'] + '.npz'), r, m, dict(v0=np.asarray(z['v0'], float), cCK3=np.asarray(z['cCK3'], float)))
    log('dry-run folder written: %s (%d lead, %d cut-in OLD runs)' % (d, len(lead), len(cut)))


def load_fresh(family, variant='CV0', dry=None):
    """Fresh arrays arrays/<variant>/<run id>.npz in ascending run id. Gated by both locks.
    dry (a --dry-run folder of OLD runs in the same format): the gate is not consulted and nothing of the project's arrays or
    runs is opened; the run ids are the files of that folder with this family in their meta."""
    cm = {'F0': 'cF0', 'E': 'cE', 'N': 'cN', 'CK3': 'cCK3'}
    if dry is None:
        require_locks('fresh-run arrays (%s, %s)' % (family, variant))
        files = [K.check_path(K.ARRAYS / variant / (rid + '.npz')) for rid in fresh_ids(family)[0]]
    else:
        root = dry_root(dry)
        files = []
        for f in sorted((root / 'CV0').glob('*.npz')):
            with np.load(f, allow_pickle=False) as z0:
                m0 = json.loads(str(z0['meta']))
            if 'dry_run' not in m0:
                raise SystemExit('REFUSED: %s is not a dry-run file' % f)
            if m0.get('family') == family:
                files.append(root / variant / f.name)
    runs = []
    for f in files:
        rid = f.stem
        z = np.load(f, allow_pickle=False)
        meta = json.loads(str(z['meta']))
        if dry is not None and 'dry_run' not in meta:
            raise SystemExit('REFUSED: %s is not a dry-run file' % f)
        if meta.get('family') != family or meta.get('lead_variant'):
            raise SystemExit('REFUSED: %s is not a plain %s run' % (rid, family))
        des = np.asarray(z['des'], float)
        if des.size and not np.all(des == des[0]):
            raise SystemExit('REFUSED: %s has more than one desired speed' % rid)
        r = dict(run=rid, desired=float(des[0]), k=np.asarray(z['k']), ev=np.asarray(z['evaluated']).astype(bool),
                 v0=np.asarray(z['v0'], float), clear1=K.clean_clear(z['clear']), vbar=np.asarray(z['vbar'], float),
                 idx55=np.asarray(z['idx55']).astype(np.int64), n_dec=int(len(z['k'])),
                 crit={nm: np.asarray(z[key], float) for nm, key in cm.items() if key in z.files})
        if 'phase' in z.files:
            r['ph'] = np.asarray(z['phase']).astype(np.int64)
        for kx in ('vhat', 'ahat_long'):
            if kx in z.files:
                r[kx] = np.asarray(z[kx], float)
        if 'lead_found' in z.files:
            r['lead_found'] = np.asarray(z['lead_found']).astype(bool)
        if dry is not None and 'cap' in meta:
            r['rd'] = K.check_path(pathlib.Path(meta['rd'])); r['cap'] = K.check_path(pathlib.Path(meta['cap']))
        runs.append(r)
    return runs


def fresh_cap(rid):
    rd = K.check_path(K.RUNS_DIR / rid / rid)
    d = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
    if len(d) != 1:
        raise SystemExit('REFUSED: expected one capture folder in %s' % (rd / 'capture'))
    return rd, d[0]


# ================================================================================================ masks
def lb_masks(r, phase='est'):
    """Populations of LB_POPS: all evaluated; ego moving (v0 > 0.5 m/s); before braking / braking / stopped by the tracker's
    phase estimate at -1.0 m/s^2 (A10 2.4), or by the truth phase of record (phase='truth': 0, 1, 2)."""
    ev = r['ev']
    ph = K.est_phase(r['vhat'], r['ahat_long'], r['lead_found'], -1.0) if phase == 'est' else r['ph']
    return [ev, ev & (r['v0'] > VMIN), ev & (ph == 0), ev & (ph == 1), ev & (ph == 2)]


# ================================================================================================ partial oracles
def add_partial(runs, seed):
    """Method of record (rev_g_partial_oracle_draws_v01.one): u = default_rng(seed).random(total stored decisions), one uniform
    per stored decision (evaluated or not), runs in the given order and decisions in stored (k) order; the partial oracle with
    share p takes E's critical scales where u < p and F0's elsewhere."""
    tot = int(sum(r['n_dec'] for r in runs))
    U = np.random.default_rng(seed).random(tot)
    pos = 0
    for r in runs:
        u = U[pos:pos + r['n_dec']]; pos += r['n_dec']
        for p, nm in zip(PO_P, PO_NM):
            r['crit'][nm] = np.where((u < p)[:, None], r['crit']['E'], r['crit']['F0'])
    return tot


def grades(v):
    """A10 5.7 (C3) / a9_8 rule: strictly increasing with the 25% share above zero. Any undefined share -> False."""
    a, b, c = (float('nan') if x is None else float(x) for x in v)
    return bool(a < b < c and a > 0)


def partial_shares(runs, masks, pop_names, frontier='gridless'):
    """{pop: dict(P25, P50, P75, grading_ok, n, R_pp, D_deceq)} on each population's own frontier and levels."""
    out = {}
    n = len(runs)
    names = ['F0', 'E'] + list(PO_NM)
    if frontier == 'gridless':
        PB = problems(runs, names, masks)
        E = [ev_point(PB[pi], n) for pi in range(len(pop_names))]
    else:
        T = grid_tables(runs, names, masks)
        E = [L.eval_scoring({a: T[a][:, pi, :] for a in T}, list(PO_NM)) for pi in range(len(pop_names))]
    for pn, e in zip(pop_names, E):
        sh = [share(e['D'][nm], e['denE']) for nm in PO_NM]
        out[pn] = dict(zip(PO_NM, sh))
        out[pn].update(grading_ok=grades(sh), n=e['n'], R_pp=e['denE'] / NLEV, D_deceq={nm: float(deceq(e['D'][nm], e['n'])) for nm in PO_NM})
    return out


# ================================================================================================ sections
def add_e5(runs):
    """E5 and E5p (A10 2.2): u over the run set's evaluated decisions; E5p with u permuted within runs (default_rng(20261915),
    runs in the given order)."""
    u, uinfo = K.e5_u(runs, 'F0', 'E')
    up = K.permute_u(runs, u)
    for r, uu, pp in zip(runs, u, up):
        r['crit']['E5'] = K.oracle_crit(r['crit']['F0'], K.RATIO, K.E5_AMP, uu)
        r['crit']['E5p'] = K.oracle_crit(r['crit']['F0'], K.RATIO, K.E5_AMP, pp)
    return uinfo


def sec_dec(V, D, runs, imm, CNT, level_of, tag='LB'):
    """Decision-equivalents of the gridless room and of the shares' numerators (all evaluated decisions, 3 s commitment), on the
    same resamples as the shares; in a resample n is the weighted number of evaluated decisions."""
    n = len(runs)
    uinfo = add_e5(runs)
    P = problems(runs, ['F0', 'E', 'N', 'E5', 'E5p', 'CK3'], [[r['ev']] for r in runs])[0]
    e = ev_point(P, n); b = P.evaluate(CNT)
    D['dec_lb'] = dict(n=e['n'], denE=e['denE'], D=e['D'], e5=uinfo, R_gl_pp=e['denE'] / NLEV,
                       RR={a: share(e['D'][a], e['denE']) for a in e['D']},
                       boot=dict(n_resamples=int(CNT.shape[0]), share_den_gt0=float(np.mean(b['denE'] > 0))),
                       R_dec_ci95=ci_of(deceq(b['denE'], b['n'])))
    V[tag + '.R.dec'] = fnum(deceq(e['denE'], e['n']))
    put(V, tag + '.RR_N.dec', deceq(e['D']['N'], e['n']), deceq(b['D']['N'], b['n']), level_of('RR_N'))
    put(V, tag + '.RR_E5.dec', deceq(e['D']['E5'], e['n']), deceq(b['D']['E5'], b['n']), level_of('RR_E5'))
    put(V, tag + '.RR_E5mP.dec', deceq(e['D']['E5'] - e['D']['E5p'], e['n']), deceq(b['D']['E5'] - b['D']['E5p'], b['n']),
        level_of('RR_E5_minus_E5p'))
    put(V, tag + '.RR_CK3.dec', deceq(e['D']['CK3'], e['n']), deceq(b['D']['CK3'], b['n']), level_of('RR_CK3'))
    if imm is None:
        D['dec_imm'] = 'no IMM arrays for this run set'
        for k in ('.IMM.r.dec', '.IMM.c.dec'):
            V[tag + k] = None; V[tag + k + '.ci'] = [None, None]; V[tag + k + '.level'] = 0.95; V[tag + k + '.cal'] = 'nominal95'
        return
    ui, uiinfo = K.e5_u(imm, 'F0', 'E')
    rsi = K.ratio_summary(np.concatenate([K.margin_ratio_values(r) for r in imm]))
    for r, uu in zip(imm, ui):
        r['crit']['E5x'] = K.oracle_crit(r['crit']['F0'], rsi['median'], rsi['A'], uu)
    PI = problems(imm, ['F0', 'E', 'N', 'E5x'], [[r['ev']] for r in imm])[0]
    ei = ev_point(PI, n); bi = PI.evaluate(CNT)
    D['dec_imm'] = dict(n=ei['n'], denE=ei['denE'], D=ei['D'], m=rsi['median'], A=rsi['A'], e5=uiinfo,
                        r=share(ei['D']['N'], ei['denE']), c=share(ei['D']['E5x'], ei['denE']))
    put(V, tag + '.IMM.r.dec', deceq(ei['D']['N'], ei['n']), deceq(bi['D']['N'], bi['n']), level_of('IMM_r'))
    put(V, tag + '.IMM.c.dec', deceq(ei['D']['E5x'], ei['n']), deceq(bi['D']['E5x'], bi['n']), level_of('IMM_c'))


def sec_ps(V, D, runs, CNT, level_of, tag='LB'):
    """H4 on the grid (rc_c_lead_v13: design on the 35 old evaluation runs by the tracker's phase at -1.0, transferred once, no
    re-selection): the schedule's numerator sum(F_F0 - F_ps) in decision-equivalents, and the transferred single scale's share on
    the record basis, sum(F_F0 - F_1) / sum(F_F0 - F_E) (F_F0, F_E: the run set's own grid frontiers; own 201 levels)."""
    import rc_c_lead_v13 as RL
    design_runs = K.load_old_eval_runs()
    designs = {nm: RL.h4_design(design_runs, kind, thr) for nm, kind, thr in RL.VARIANTS}
    hx = RL.H4(runs, designs)
    n = len(runs)
    h = hx.evaluate(np.ones((1, n))); hb = hx.evaluate(CNT)
    den = float(h['den'][0]); nn = float(h['n'][0])
    D['ps'] = dict(den=den, n=nn, D_ps=float(h['D_ps'][0, 0]), D_1=float(h['D_1'][0]), rec=float(h['rec'][0, 0]),
                   lfl=float(h['lfl'][0, 0]), variant=hx.names[0], n_levels_with_single=int(np.sum(hx.v1)),
                   n_levels_with_triple=int(np.sum(hx.vp[0])))
    put(V, tag + '.PS.rec.dec', deceq(h['D_ps'][0, 0], nn), deceq(hb['D_ps'][:, 0], hb['n']), level_of('H4_rec_' + hx.names[0]))
    put(V, tag + '.PS.single', share(float(h['D_1'][0]), den), K.ratio_arr(hb['D_1'], hb['den']), 0.95)


def sec_po(V, D, runs, seed, phase='est', tag='LB'):
    tot = add_partial(runs, seed)
    masks = [lb_masks(r, phase) for r in runs]
    res = partial_shares(runs, masks, LB_POPS, 'gridless')
    D['po_lb'] = dict(seed=seed, n_uniforms=tot, phase=phase, frontier='gridless', pops=res,
                      grid_frontier=partial_shares(runs, masks, LB_POPS, 'grid'))
    for pn in LB_POPS:
        for nm in PO_NM:
            V['%s.%s.PO%s' % (tag, pn, nm[1:])] = fnum(res[pn][nm])
        V['%s.%s.grading_ok' % (tag, pn)] = res[pn]['grading_ok']
    for nm in PO_NM:
        V['%s.PO%s' % (tag, nm[1:])] = fnum(res['all'][nm])
    V[tag + '.grading_ok'] = res['all']['grading_ok']


def cutin_truth(runs, test_old):
    """Event tick and track age per run: rc_c_cutin_v13.truth_of_run (from the logs), or the truth file an earlier run of that
    recount wrote for exactly these runs and decisions."""
    import rc_c_cutin_v13 as RC
    f = OUT / ('RC_C_CUTIN_TESTOLD_TRUTH_v13.json' if test_old else 'RC_C_CUTIN_TRUTH_v13.json')
    if f.is_file():
        tdoc = json.loads(f.read_text(encoding='utf-8'))
        if [t['run'] for t in tdoc['truth']] == [r['run'] for r in runs] and all(
                np.array_equal(np.asarray(t['k']), np.asarray(r['k'])) for t, r in zip(tdoc['truth'], runs)):
            return tdoc['truth'], str(f), RC
    return [RC.truth_of_run(r) for r in runs], 'computed here (rc_c_cutin_v13.truth_of_run)', RC


def sec_ci(V, D, runs, CNT, po_seed, level_of, test_old, tag='CI'):
    """Cut-in event window (A10 2.5; evaluated decisions with t - t_c in [-1, +4] s; runs without an event stay in the resampled
    set with empty windows): RR_gl of CK3, E5 and E5 - E5p with intervals; D(N) in decision-equivalents; the young-track room in
    decision-equivalents; the partial oracles (own generator restart for the cut-in run set) and the grading check.
    E5's u: ranks over ALL evaluated decisions of the cut-in runs (A10 2.2: the run set's evaluated decisions)."""
    n = len(runs)
    truth, src, RC = cutin_truth(runs, test_old)
    M = [RC.masks_of(r, t) for r, t in zip(runs, truth)]
    WY = [[m[1], m[2]] for m in M]                       # event window; young tracks (< 1 s) in the window
    uinfo = add_e5(runs)
    have_ck3 = all('CK3' in r['crit'] for r in runs)
    names = ['F0', 'E', 'N', 'E5', 'E5p'] + (['CK3'] if have_ck3 else [])
    PW, PY = problems(runs, names, WY)
    e = ev_point(PW, n); b = PW.evaluate(CNT); ey = ev_point(PY, n)
    D['ci'] = dict(truth_source=src, events=int(sum(t['event_tick'] is not None for t in truth)), n_runs=n,
                   runs_without_event=[t['run'] for t in truth if t['event_tick'] is None], n_window=e['n'], n_young=ey['n'],
                   denE=e['denE'], R_gl_pp=e['denE'] / NLEV, D=e['D'], e5=uinfo, have_ck3=have_ck3,
                   RR={a: share(e['D'][a], e['denE']) for a in e['D']},
                   boot=dict(n_resamples=int(CNT.shape[0]), share_den_gt0=float(np.mean(b['denE'] > 0))),
                   young=dict(denE=ey['denE'], R_gl_pp=ey['denE'] / NLEV))
    rr = lambda a: K.ratio_arr(b['D'][a], b['denE'])            # noqa: E731
    if have_ck3:
        put(V, tag + '.RR_CK3', share(e['D']['CK3'], e['denE']), rr('CK3'))
    else:
        V[tag + '.RR_CK3'] = None; V[tag + '.RR_CK3.ci'] = [None, None]; V[tag + '.RR_CK3.level'] = 0.95; V[tag + '.RR_CK3.cal'] = 'nominal95'
    put(V, tag + '.RR_E5', share(e['D']['E5'], e['denE']), rr('E5'))
    put(V, tag + '.RR_E5mP', share(e['D']['E5'], e['denE']) - share(e['D']['E5p'], e['denE']), rr('E5') - rr('E5p'))
    put(V, tag + '.RR_N.dec', deceq(e['D']['N'], e['n']), deceq(b['D']['N'], b['n']), level_of('W_RR_N'))
    # an empty young-track population has no decision and no room: 0 decision-equivalents (writer's specification, section 3)
    V[tag + '.Y.R.dec'] = 0.0 if ey['n'] == 0 else fnum(deceq(ey['denE'], ey['n']))
    tot = add_partial(runs, po_seed)
    wm = [[m[1]] for m in M]
    res = partial_shares(runs, wm, ['window'], 'gridless')['window']
    D['po_ci'] = dict(seed=po_seed, n_uniforms=tot, frontier='gridless', window=res,
                      grid_frontier=partial_shares(runs, wm, ['window'], 'grid')['window'])
    for nm in PO_NM:
        V['%s.PO%s' % (tag, nm[1:])] = fnum(res[nm])
    V[tag + '.grading_ok'] = res['grading_ok']
    # beside, in details only: the same sources over ALL evaluated decisions of the cut-in runs (exercises this section on old
    # runs, whose event windows hold no room)
    PA = problems(runs, names + list(PO_NM), [[r['ev']] for r in runs])[0]
    ea = ev_point(PA, n)
    D['ci']['all_evaluated_beside'] = dict(n=ea['n'], denE=ea['denE'], R_gl_pp=ea['denE'] / NLEV, D=ea['D'],
                                           RR={a: share(ea['D'][a], ea['denE']) for a in ea['D']},
                                           D_deceq={a: float(deceq(ea['D'][a], ea['n'])) for a in ea['D']})


# ================================================================================================ selftest: values of record
def selftest():
    """The partial oracles of record on the 35 old runs: REV_G_PARTIAL_DRAWS_v01 (draw 20261118, grid step frontier, truth
    phases, each population on its own frontier) and A9_8_GRADING_BEFORE_STOP_v01 (before the lead's stop)."""
    t0 = time.time()
    doc = dict(program='rc_s57a_v13.py', what='selftest: partial oracles of record on the 35 old evaluation runs', started=K.clock(),
               checks={})

    def chk(name, here, rec, tol):
        if isinstance(here, (bool, str)) or isinstance(rec, (bool, str)):
            good = here == rec; diff = None
        else:
            diff = abs(float(here) - float(rec)); good = bool(diff <= tol) or (math.isnan(float(here)) and math.isnan(float(rec)))
        doc['checks'][name] = dict(here=here, of_record=rec, abs_diff=diff, tol=tol, ok=good)
        if not good:
            log('  MISMATCH %s: here %r, of record %r' % (name, here, rec))

    runs = load_old_eval()
    g = json.loads((K.V11 / 'out' / 'REV_G_PARTIAL_DRAWS_v01.json').read_text(encoding='utf-8'))
    tot = add_partial(runs, SEED_PO_RECORD)
    chk('po.n_uniforms', tot, 9307, 0)
    res = partial_shares(runs, [lb_masks(r, 'truth') for r in runs], LB_POPS, 'grid')
    for pn, rn in zip(LB_POPS, ('all', 'moving', 'phase0', 'phase1', 'phase2')):
        for nm in PO_NM:
            chk('REV_G.%s.%s' % (rn, nm), res[pn][nm], g['pops'][rn][nm]['of_record'], 1e-12)
    a8 = json.loads((K.V12 / 'out' / 'A9_8_GRADING_BEFORE_STOP_v01.json').read_text(encoding='utf-8'))
    bs = partial_shares(runs, [[r['ev'] & (r['ph'] <= 1)] for r in runs], ['before_stop'], 'grid')['before_stop']
    for nm in PO_NM:
        chk('A9_8.%s' % nm, bs[nm], a8['of_record'][nm], 1e-12)
    chk('A9_8.n', bs['n'], a8['n'], 0); chk('A9_8.R_pp', bs['R_pp'], a8['R_pp'], 1e-12)
    chk('A9_8.grades_by_rule', bs['grading_ok'], a8['grades_by_rule'], 0)
    # the gridless construction of this program against the library of record (a9_common_v01 + eval_scoring), same populations
    A9 = K.try_a9()
    if A9 is not None:
        for r in runs:
            r['masks_po'] = tuple(lb_masks(r, 'est'))
        G = A9.gridless_sources(runs, ['F0', 'E'] + list(PO_NM), lambda r: r['clear1'] > 0., masks_key='masks_po')
        mine = partial_shares(runs, [lb_masks(r, 'est') for r in runs], LB_POPS, 'gridless')
        for pi, pn in enumerate(LB_POPS):
            el = L.eval_scoring({a: G[a].curve(None, pops=[pi])[:, 0, :] for a in G}, list(PO_NM))
            for nm in PO_NM:
                chk('gridless_vs_library.%s.%s' % (pn, nm), mine[pn][nm], share(el['D'][nm], el['denE']), 0.)
    # the cut-in section's computation on a window stand-in of the lead-braking runs (the old cut-in windows hold no room):
    # evaluated decisions within [-20, +80] ticks of the run's first decision with truth phase >= 1; E5 ranks over all evaluated
    # decisions; this program's kernel against the library of record on the same masks
    if A9 is not None:
        add_e5(runs)
        wm = []
        for r in runs:
            i1 = np.flatnonzero(r['ph'] >= 1)
            dk = (np.asarray(r['k']) - int(r['k'][i1[0]])) if i1.size else None
            wm.append([r['ev'] & (dk >= -20) & (dk <= 80)] if i1.size else [np.zeros(r['ev'].size, bool)])
        names = ['F0', 'E', 'N', 'E5', 'E5p', 'CK3'] + list(PO_NM)
        e = ev_point(problems(runs, names, wm)[0], len(runs))
        for r, m in zip(runs, wm):
            r['masks_w'] = tuple(m)
        G = A9.gridless_sources(runs, names, lambda r: r['clear1'] > 0., masks_key='masks_w')
        el = L.eval_scoring({a: G[a].curve(None, pops=[0])[:, 0, :] for a in G}, names[2:])
        chk('window_standin.n', e['n'], el['n'], 0); chk('window_standin.denE', e['denE'], el['denE'], 0.)
        for a in names[2:]:
            chk('window_standin.D.%s' % a, e['D'][a], el['D'][a], 0.)
        doc['window_standin'] = dict(n=e['n'], R_gl_pp=e['denE'] / NLEV, RR={a: share(e['D'][a], e['denE']) for a in e['D']})
    nbad = sum(1 for v in doc['checks'].values() if not v['ok'])
    doc['summary'] = dict(n_checks=len(doc['checks']), n_failed=nbad, all_ok=nbad == 0,
                          max_abs_diff=max([v['abs_diff'] for v in doc['checks'].values() if v.get('abs_diff') is not None] or [0.]))
    doc['seconds'] = time.time() - t0; doc['written'] = K.clock()
    return doc, nbad == 0


# ================================================================================================ run sets
def old_config(a):
    """Old-run stand-ins (writer's specification, section 10): LB = the 35 old evaluation runs (tracker phase from v12's lead
    extract; IMM = package B's B1 re-track arrays); CI = the 20 cut-in tuning runs (stored arrays; cCK3 from package B's CV0
    re-track arrays, identity checked; events from their logs)."""
    notes = {}

    def load_lb():
        runs = load_old_eval()
        return runs, [b_variant_run('B1', r) for r in runs]

    def load_ci():
        runs = K.load_old_cutin_runs()
        mx = 0.
        for r in runs:
            r['n_dec'] = int(len(r['k']))
            z, m = b_arrays('CV0', r['run'], r)
            mx = max(mx, m)
            r['crit']['CK3'] = np.asarray(z['cCK3'], float)
        notes['ci_b_cv0_max_abs_diff'] = mx
        return runs
    return dict(load_lb=load_lb, load_ci=load_ci, seed_boot=a.old_seed, seed_po=a.old_po_seed, seed_po_ci=SEED_PO_FRESH, notes=notes)


def fresh_config(a):
    notes = {}

    dry = a.dry_run

    def load_lb():
        runs = load_fresh('lead_braking', 'CV0', dry)
        notes['lb_ids'] = fresh_ids('lead_braking')[1] if dry is None else 'dry run'
        imm = load_fresh('lead_braking', 'B1', dry)
        for r, q in zip(runs, imm):
            if not (r['run'] == q['run'] and np.array_equal(r['k'], q['k']) and np.array_equal(r['ev'], q['ev'])):
                raise SystemExit('REFUSED: CV0 and B1 arrays of %s do not describe the same decisions' % r['run'])
        return runs, imm

    def load_ci():
        runs = load_fresh('cutin', 'CV0', dry)
        notes['ci_ids'] = fresh_ids('cutin')[1] if dry is None else 'dry run'
        if dry is None:
            for r in runs:
                r['rd'], r['cap'] = fresh_cap(r['run'])
        return runs
    return dict(load_lb=load_lb, load_ci=load_ci, seed_boot=K.SEED_BOOT, seed_po=SEED_PO_FRESH, seed_po_ci=SEED_PO_FRESH, notes=notes)


def levels_from(path):
    """Calibrated levels (A10 2.6) of hypothesis statistics from an output of rc_c_lead_v13 / rc_c_cutin_v13:
    {statistic: level_used}; statistics without a decided level are left out."""
    d = json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
    cal = d.get('calibration'); out = {}
    if isinstance(cal, dict) and isinstance(cal.get('stats'), dict):
        for s, c in cal['stats'].items():
            if c.get('level_used') is not None:
                out[s] = float(c['level_used'])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--boot', type=int, default=K.NBOOT)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--only', default=','.join(SECTIONS))
    ap.add_argument('--levels-lead', default=None)
    ap.add_argument('--levels-cutin', default=None)
    ap.add_argument('--old-seed', type=int, default=SEED_RECORD, help='--test-old: seed of the run bootstrap (LB and CI stand-ins)')
    ap.add_argument('--old-po-seed', type=int, default=SEED_PO_RECORD, help='--test-old: seed of the partial-oracle uniforms')
    ap.add_argument('--tag', default='')
    ap.add_argument('--make-dry', default=None)
    ap.add_argument('--dry-run', default=None)
    a = ap.parse_args()
    nthreads = K.set_workers(max(1, min(a.workers, 2)))
    t00 = time.time()
    if a.selftest:
        outf = OUT / ('SELFTEST_RC_S57A_v13%s.json' % a.tag)
        if outf.exists():
            raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % outf)
        doc, ok = selftest()
        K.write_new(outf, doc)
        log('selftest: %d checks, %d failed, max |diff| %.3g -> %s' % (doc['summary']['n_checks'], doc['summary']['n_failed'],
                                                                       doc['summary']['max_abs_diff'], outf))
        raise SystemExit(0 if ok else 1)
    if a.make_dry:
        make_dry(a.make_dry)
        return
    if a.dry_run and a.test_old:
        raise SystemExit('REFUSED: --dry-run and --test-old exclude each other')
    only = set(x for x in a.only.split(',') if x)
    if not only <= set(SECTIONS):
        raise SystemExit('REFUSED: unknown section in --only (known: %s)' % ', '.join(SECTIONS))
    if not a.test_old and (a.old_seed != SEED_RECORD or a.old_po_seed != SEED_PO_RECORD):
        raise SystemExit('REFUSED: --old-seed / --old-po-seed apply to --test-old only (fresh seeds are fixed by A10 5.8)')
    full = (a.boot == K.NBOOT and only == set(SECTIONS) and a.old_seed == SEED_RECORD and a.old_po_seed == SEED_PO_RECORD)
    name = '%s_v13%s%s.json' % ('TESTOLD_RC_S57A' if a.test_old else ('DRYRUN_RC_S57A' if a.dry_run else 'RC_S57A'),
                                '' if full else '_PART_b%d' % a.boot, a.tag)
    outf = OUT / name
    if outf.exists():
        raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % outf)
    if a.dry_run:
        dry_root(a.dry_run)
    elif not a.test_old:
        require_locks('fresh-run arrays and logs')              # before anything of a fresh run is opened
    V = {}; D = {}
    doc = dict(family='S57A', program='rc_s57a_v13.py', test_old=bool(a.test_old), values=V, details=D,
               role='second program (recount), AMENDMENT_10_v13 section 10.1(b)', model='claude-fable-5-2', started=K.clock(),
               threads=nthreads, sections=sorted(only), n_boot=int(a.boot))
    if a.dry_run:
        doc['dryrun'] = 'DRY RUN of the fresh code path on OLD runs in the fresh-array format (%s); NOT fresh data' % a.dry_run
    lv_lead = levels_from(a.levels_lead) if a.levels_lead else {}
    lv_cut = levels_from(a.levels_cutin) if a.levels_cutin else {}
    D['levels'] = dict(rule='nominal 95% for every interval unless a calibration file is given', lead_file=a.levels_lead,
                       cutin_file=a.levels_cutin, lead=lv_lead, cutin=lv_cut)
    CFG = old_config(a) if a.test_old else fresh_config(a)
    D['seeds'] = dict(boot=CFG['seed_boot'], partial_oracles_lb=CFG['seed_po'], partial_oracles_ci=CFG['seed_po_ci'], e5_perm=K.SEED_PERM)
    if a.test_old:
        D['old_run_convention'] = ('OLD runs as stand-ins: LB = the 35 old evaluation runs (IMM from package B\'s B1 re-track '
                                   'arrays), CI = the 20 cut-in tuning runs; run bootstrap default_rng(%d), first %d rows; partial '
                                   'oracles: LB default_rng(%d) (20261118 is the draw of record), CI default_rng(%d) (no value of record)'
                                   % (CFG['seed_boot'], a.boot, CFG['seed_po'], CFG['seed_po_ci']))
    if only & {'dec', 'ps', 'po'}:
        runs, imm = CFG['load_lb']()
        D['lb_runs'] = [r['run'] for r in runs]
        D['lb_counts'] = dict(n_runs=len(runs), n_decisions=int(sum(r['n_dec'] for r in runs)), n_evaluated=int(sum(r['ev'].sum() for r in runs)))
        CNT = K.boot_counts(len(runs), K.NBOOT, CFG['seed_boot'])[:a.boot]
        if 'dec' in only:
            sec_dec(V, D, runs, imm, CNT, lambda s: lv_lead.get(s, 0.95)); log('dec done (%.0f s)' % (time.time() - t00))
        if 'ps' in only:
            sec_ps(V, D, runs, CNT, lambda s: lv_lead.get(s, 0.95)); log('ps done (%.0f s)' % (time.time() - t00))
        if 'po' in only:
            sec_po(V, D, runs, CFG['seed_po']); log('po done (%.0f s)' % (time.time() - t00))
    if 'ci' in only:
        cruns = CFG['load_ci']()
        D['ci_runs'] = [r['run'] for r in cruns]
        CNTC = K.boot_counts(len(cruns), K.NBOOT, CFG['seed_boot'])[:a.boot]
        sec_ci(V, D, cruns, CNTC, CFG['seed_po_ci'], lambda s: lv_cut.get(s, 0.95), a.test_old or bool(a.dry_run))
        log('ci done (%.0f s)' % (time.time() - t00))
    D['notes'] = CFG['notes']
    doc['written'] = K.clock(); doc['seconds'] = time.time() - t00
    log('written %s (%d keys, %.0f s)' % (K.write_new(outf, doc), len(V), time.time() - t00))


if __name__ == '__main__':
    main()
