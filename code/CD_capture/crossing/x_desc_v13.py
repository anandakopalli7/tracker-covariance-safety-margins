"""X (AMENDMENT_11_v13.md sec. 3.6): the fixed descriptive outputs of the pedestrian-crossing test that x_cross_v13.py does not compute.
First program. New file, 21 Nov 2026 (Claude Opus 5.5, session CD), written from crossing\\CD_DEFINITIONS_X_DESC_v13.md before any fresh
crossing value existed. The second program is recount\\rc_x_desc_v13.py (written independently from the same definitions).

Runs and arrays as x_cross_v13.py (CD_DEFINITIONS_X_v13.md sec. 0): fresh = the 390 study positions of CASES_X_PC_v13.json (SHA-256 given
with --cases-sha), replacements from REPLACEMENTS_X_v13.json, job ids pc13x_<case>_native in ascending run id; the analysed set is those
with arrays arrays_x/CV0/<rid>.npz (meta family pedestrian_crossing). --test-old: the stored arrays of record of the 51 old pedestrian-
crossing runs (gateR_rt_v01, meta.family == pedestrian_crossing, name order); it never reads a fresh run and writes TESTOLD_ files.
Population: all evaluated decisions; 3 s commitment (W1: safe = clean_clear(clear) > 0).
Common inputs (definitions sec. 2): u = trk_score_v01.e5_u(runs, 'F0', 'E'); ratios = trk_score_v01.margin_ratios(runs, 'N', 'F0'),
m_N = median(ratios); resamples optA_lib_v02.boot_counts(n_runs, 20000, 20261911) (--nboot < 20000: the first rows, old-run test only);
intervals: nominal 95% percentile (np.percentile(x[finite], [2.5, 97.5]) = optA_lib_v02.pct), a ratio undefined where D_gl(E) <= 0.
  sec. 3  E5q_N: f_i = np.quantile(ratios, u_i), critical scales cF0 / f_i^2 (as add_oracle); gridless step frontier (201 levels):
          X.ped.RR_E5qN = RR_gl(E5q_N), X.ped.RR_NmE5qN = RR_gl(N) - RR_gl(E5q_N), each with .ci and .level (0.95).
  sec. 4  grid frontier of record ([0] + logspace(-2, 3, 201); rev_common_v01.tables / points = optA_lib_v02 select_grid, stats_scored,
          eval_scoring; F0's g = 0 point prepended to every source except F0 and E), as package C's S57B group 5 (A9-1(a)):
          placebo P = cF0 / m_N^2, record-amplitude placebo P_rec = cF0 / 1.1029^2 (a9_common_v01.add_placebo);
          X.ped.grid.RR_N, RR_P, RR_NmP, RR_Prec, RR_NmPrec (points; undefined if D(E) <= 0), grid.R = D(E) / 201, grid.m_N.
  sec. 5  partial oracles: u_po = default_rng(20261919).random(N_total) over every decision of the analysed runs (evaluated or not), runs
          in ascending run id, array order within a run; crit_Pp = where(u_po < p, cE, cF0), p = 0.25, 0.5, 0.75; gridless points
          X.ped.PO25 / PO50 / PO75 = RR_gl(P_p) and .dec = dec_eq(D_gl(P_p), n); X.ped.grading_ok = PO25 > 0 and PO25 < PO50 < PO75
          (false if any is null), as C's S57A sec. 4.
Point values with package B's library of record (trk_score_v01.rr_gl); resamples with gl_fast_v13 (checked identical at the full sample).
Gate: refuses unless revision_v13/LOCK_A11.txt exists (fresh mode); fresh mode refuses --nboot other than 20,000.
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 crossing\\x_desc_v13.py (--test-old | --cases-sha SHA) [--nboot N]
Writes crossing/out/[TESTOLD_]X_DESC_pedestrian_crossing_v13[_b<n>].json (never overwritten); flat `values` dict with exactly the keys of
the definitions sec. 3-6 (undefined numbers and intervals are null).
"""
import argparse, json, math, os, pathlib, sys, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('NUMBA_NUM_THREADS', '2')          # laptop rule: at most 2 threads
if os.name == 'nt':                                      # laptop rule: BelowNormal priority (no effect on any value)
    import ctypes; ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
import numpy as np
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(CD / 'analysis'))
import cd_common_v13 as CC               # noqa: E402
import trk_env_v01 as env                # noqa: E402
env.setup()
import trk_score_v01 as TS               # noqa: E402
L = CC.L; C11 = CC.C11; A9 = CC.A9
FAM = 'pedestrian_crossing'
N_STUDY = 390
LOCK_A11 = CC.V13 / 'LOCK_A11.txt'
STORED = pathlib.Path(r'<library folder>\gateR_rt_v01')
ARRX = CD / 'arrays_x' / 'CV0'
OUTD = HERE / 'out'
DEFS = HERE / 'CD_DEFINITIONS_X_DESC_v13.md'
SEED_PO = 20261919                        # A11 sec. 3.7: X partial-oracle masks, as C
assert SEED_PO == CC.SEED_PARTIAL
PS_ = (0.25, 0.5, 0.75); PO = ('PO25', 'PO50', 'PO75')
RATIO_REC = 1.1029                        # A9-1(a)'s amplitude (N's median on lead braking)
assert RATIO_REC == CC.RATIO == A9.RATIO
B_STEP0_RR_N = -0.43229869545659005       # package B's step-0 RR_gl(N) on the 51 old pedestrian-crossing runs (old-run sanity check)
CHUNK = 500

ap = argparse.ArgumentParser()
ap.add_argument('--test-old', action='store_true'); ap.add_argument('--cases-sha')
ap.add_argument('--nboot', type=int, default=CC.NBOOT)
args = ap.parse_args()
if args.test_old == (args.cases_sha is not None):
    raise SystemExit('REFUSED: give exactly one of --test-old and --cases-sha')
if not (1 <= args.nboot <= CC.NBOOT):
    raise SystemExit('REFUSED: --nboot must be between 1 and %d (the first rows of the draw of record)' % CC.NBOOT)
if args.test_old:
    gate = 'TEST_OLD: stored arrays of record of old runs only; no fresh value'
else:
    if not LOCK_A11.is_file(): raise SystemExit('REFUSED: LOCK_A11.txt does not exist; no fresh crossing value may be computed (A11 sec. 3.3)')
    gate = 'LOCK_A11 sha256 ' + CC.sha(LOCK_A11)
    if args.nboot != CC.NBOOT: raise SystemExit('REFUSED: a reduced --nboot is a test option (--test-old only)')
t00 = time.time()
log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)   # noqa: E731
OUTF = OUTD / (('TESTOLD_' if args.test_old else '') + f'X_DESC_{FAM}_v13' + ('' if args.nboot == CC.NBOOT else f'_b{args.nboot}') + '.json')
if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)


# ------------------------------------------------------------------------------------------------ runs (as x_cross_v13.py)
def run_dict(rid, z, desired):
    ev = z['evaluated'].astype(bool)
    crit = {'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float)}
    n_all = int(ev.size)
    assert all(c.shape == (n_all, 17) for c in crit.values()), rid
    if 'k' in z.files:                                   # array order is ascending k (definitions sec. 5); checked, never used for a value
        k = np.asarray(z['k'], np.int64); assert k.size == n_all and np.all(np.diff(k) > 0), rid
    return dict(run=rid, desired=float(desired), idx55=z['idx55'].astype(np.int64), clear1=L.clean_clear(z['clear']), vbar=z['vbar'],
                ev=ev, masks=(ev,), sel={}, late={}, n_all=n_all, crit=crit)


def fresh_list():
    cf = HERE / 'CASES_X_PC_v13.json'
    if CC.sha(cf) != args.cases_sha: raise SystemExit('REFUSED: CASES_X_PC_v13.json differs from --cases-sha')
    X = json.loads(cf.read_text(encoding='utf-8'))
    rows = [r for r in X['cases'] if not r['reserve']]
    assert len(rows) == N_STUDY and all(r['position'] == i for i, r in enumerate(rows))
    reserves = {r['case']: r for r in X['cases'] if r['reserve']}
    rep = {}
    rp = HERE / 'REPLACEMENTS_X_v13.json'
    if rp.is_file(): rep = json.loads(rp.read_text(encoding='utf-8'))['replacements']
    out = []
    for r in rows:
        c = rep.get(r['case'], r['case'])
        if c != r['case']:
            s = reserves[c]; assert s['desired_mps'] == r['desired_mps'], 'a replacement must be a reserve of the same speed'
        out.append(f'pc13x_{c}_native')
    return sorted(out), rep


if args.test_old:
    runs = []
    for f in sorted(STORED.glob('*.npz'), key=lambda p: p.name):          # name order
        z = np.load(f, allow_pickle=False); m = json.loads(str(z['meta']))
        if m.get('family') == FAM:
            runs.append(run_dict(f.stem, z, m['desired']))
    run_ids = [r['run'] for r in runs]; listed = run_ids; replacements = {}
    assert run_ids == sorted(run_ids)
else:
    listed, replacements = fresh_list(); runs = []; run_ids = []
    for rid in listed:                                   # ascending run id
        f = ARRX / (rid + '.npz')
        if not f.is_file(): continue
        z = np.load(f, allow_pickle=False); m = json.loads(str(z['meta']))
        assert m['family'] == FAM and m['run_id'] == rid, rid
        runs.append(run_dict(rid, z, m['desired'])); run_ids.append(rid)
NR = len(runs)
if NR == 0: raise SystemExit('REFUSED: no run with arrays')
log('runs %d of %d listed (%s)' % (NR, len(listed), 'TEST: stored arrays of old runs' if args.test_old else 'fresh pedestrian crossing'))

# ------------------------------------------------------------------------------------------------ common inputs (sec. 2)
u, uinfo = TS.e5_u(runs, 'F0', 'E')
ratios = TS.margin_ratios(runs, 'N', 'F0')
m_N = float(np.median(ratios))
rs = TS.ratio_summary(ratios)
assert rs['median'] == m_N

# sec. 3: E5q_N, f_i = N's empirical ratio quantile at u_i (numpy's default linear method), scales as add_oracle
f_ev = []
for r, uu in zip(runs, u):
    f = np.quantile(ratios, uu)
    r['crit']['E5qN'] = r['crit']['F0'] / (f * f)[:, None]
    r['sel'].pop('E5qN', None)
    f_ev.append(f[r['ev']])
f_ev = np.concatenate(f_ev)

# sec. 5: partial oracles, one uniform per decision of the analysed runs (evaluated or not), ascending run id, array order
N_TOTAL = int(sum(r['n_all'] for r in runs))
U_PO = np.random.default_rng(SEED_PO).random(N_TOTAL)
pos = 0; po_share = {nm: 0 for nm in PO}
for r in runs:
    upo = U_PO[pos:pos + r['n_all']]; pos += r['n_all']
    for p, nm in zip(PS_, PO):
        r['crit'][nm] = np.where((upo < p)[:, None], r['crit']['E'], r['crit']['F0'])
        r['sel'].pop(nm, None)
        po_share[nm] += int((upo[r['ev']] < p).sum())
assert pos == N_TOTAL

# sec. 4: placebos (a9_common_v01.add_placebo: crit = cF0 / factor)
A9.add_placebo(runs, 'P', factor=m_N ** 2)
A9.add_placebo(runs, 'Prec', factor=RATIO_REC ** 2)
log('sources built: m_N %.6f (%d ratios); %d decisions for the partial-oracle draw' % (m_N, ratios.size, N_TOTAL))

# ------------------------------------------------------------------------------------------------ gridless: E5q_N and partial oracles
NAMES_GL = ['F0', 'E', 'N', 'E5qN'] + list(PO)
G = TS.gridless(runs, NAMES_GL)
pt = TS.rr_gl(G, 'F0', 'E', NAMES_GL[2:], pop=0)
n_dec = int(round(pt['n'])); assert n_dec == pt['n'] == int(sum(int(r['ev'].sum()) for r in runs))
P1 = CC.prep(G, ['F0', 'E', 'N', 'E5qN'], 0)
Wfull = np.ones((1, NR))
chk = CC.evaluate(P1, Wfull)
assert chk['denE'][0] == pt['denE'] and all(chk['D'][a][0] == pt['D'][a] for a in ('N', 'E5qN')), 'gl_fast differs from the library'
log('gridless events built; gl_fast identical to the library at the full sample')
W = CC.counts(NR, CC.NBOOT, CC.SEED_BOOT)[:args.nboot]          # the draw of record; first rows for a reduced old-run test


def gl_stats(e):
    """cd_common_v13.GLStat's ('RR', 'E5qN') and ('RRdiff', 'N', 'E5qN') columns from one gl_fast evaluation (undefined where D_gl(E) <= 0)."""
    den = e['denE']; ok = np.isfinite(den) & (den > 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        rq = np.where(ok, e['D']['E5qN'] / den, np.nan); rn = np.where(ok, e['D']['N'] / den, np.nan)
    return np.stack([rq, rn - rq], axis=1)


full = gl_stats(chk)[0]
EV = CC.evaluate(P1, W, chunk=CHUNK)
boot = gl_stats(EV)
assert np.array_equal(CC.GLStat(P1, [('RR', 'E5qN'), ('RRdiff', 'N', 'E5qN')])(W[:CHUNK]), boot[:CHUNK], equal_nan=True), 'GLStat differs'
pt_rr_e5q = pt['RR']['E5qN']; pt_diff = pt['RR']['N'] - pt['RR']['E5qN']
same = lambda a, b: (a == b) or (math.isnan(a) and math.isnan(b))          # noqa: E731
assert same(float(full[0]), pt_rr_e5q) and same(float(full[1]), pt_diff), 'GLStat full-sample values differ from the library'
log('E5q_N resamples done (%d)' % W.shape[0])
ci_e5q = L.pct(boot[:, 0]); ci_diff = L.pct(boot[:, 1])
PO_RR = [pt['RR'][nm] for nm in PO]
PO_DEC = [L.dec_eq(pt['D'][nm], pt['n']) for nm in PO]


def fin(x):
    return x is not None and np.isfinite(x)


grading_ok = bool(all(fin(x) for x in PO_RR) and PO_RR[0] > 0 and PO_RR[0] < PO_RR[1] < PO_RR[2])

# ------------------------------------------------------------------------------------------------ grid frontier and placebos (sec. 4)
NAMES_GRID = ['F0', 'E', 'N', 'P', 'Prec']
Xg = C11.tables(runs, ('W1',), NAMES_GRID)
pg = C11.points(Xg, NAMES_GRID[2:], pops=[0])[0]
assert pg['n'] == pt['n'], 'grid and gridless populations differ'
denG = pg['denE']; DG = pg['D']
log('grid frontier done')


# ------------------------------------------------------------------------------------------------ values (sec. 3-6)
def _f(x):
    return None if x is None or not np.isfinite(x) else float(x)


def _ci(c):
    return None if not (np.isfinite(c[0]) and np.isfinite(c[1])) else [float(c[0]), float(c[1])]


V = {}; pre = 'X.ped.'
V[pre + 'desc.n_runs'] = NR
V[pre + 'desc.n_dec'] = n_dec
V[pre + 'RR_E5qN'] = _f(pt_rr_e5q); V[pre + 'RR_E5qN.ci'] = _ci(ci_e5q); V[pre + 'RR_E5qN.level'] = 0.95
V[pre + 'RR_NmE5qN'] = _f(pt_diff); V[pre + 'RR_NmE5qN.ci'] = _ci(ci_diff); V[pre + 'RR_NmE5qN.level'] = 0.95
V[pre + 'grid.RR_N'] = _f(L.ratio(DG['N'], denG))
V[pre + 'grid.RR_P'] = _f(L.ratio(DG['P'], denG))
V[pre + 'grid.RR_NmP'] = _f(L.ratio(DG['N'] - DG['P'], denG))
V[pre + 'grid.RR_Prec'] = _f(L.ratio(DG['Prec'], denG))
V[pre + 'grid.RR_NmPrec'] = _f(L.ratio(DG['N'] - DG['Prec'], denG))
V[pre + 'grid.R'] = _f(denG / L.NLEV)
V[pre + 'grid.m_N'] = _f(m_N)
for nm, x, d in zip(PO, PO_RR, PO_DEC):
    V[pre + nm] = _f(x); V[pre + nm + '.dec'] = _f(d)
V[pre + 'grading_ok'] = grading_ok
KEYS = ['desc.n_runs', 'desc.n_dec', 'RR_E5qN', 'RR_E5qN.ci', 'RR_E5qN.level', 'RR_NmE5qN', 'RR_NmE5qN.ci', 'RR_NmE5qN.level',
        'grid.RR_N', 'grid.RR_P', 'grid.RR_NmP', 'grid.RR_Prec', 'grid.RR_NmPrec', 'grid.R', 'grid.m_N',
        'PO25', 'PO50', 'PO75', 'PO25.dec', 'PO50.dec', 'PO75.dec', 'grading_ok']
assert sorted(V) == sorted(pre + k for k in KEYS), 'values keys differ from the definitions'

# ------------------------------------------------------------------------------------------------ details and checks
checks = dict(gl_fast_equals_library_full_sample=True,
              RR_gl_N=dict(value=pt['RR']['N'], b_step0_old_runs=B_STEP0_RR_N if args.test_old else None,
                           equal=bool(pt['RR']['N'] == B_STEP0_RR_N) if args.test_old else None))
if args.test_old:
    log('check: RR_gl(N) = %r; B step 0 %r; equal %s' % (pt['RR']['N'], B_STEP0_RR_N, checks['RR_gl_N']['equal']))
with np.errstate(divide='ignore', invalid='ignore'):
    rrN_b = C11.rat(EV['D']['N'], EV['denE'])
details = dict(
    common=dict(e5_u=uinfo, ratio_summary_N_F0=rs, m_N=m_N, n_ratios=int(ratios.size),
                f_quantile_evaluated=dict(n=int(f_ev.size), min=float(f_ev.min()), median=float(np.median(f_ev)), max=float(f_ev.max()))),
    gridless=dict(n=pt['n'], denE=pt['denE'], R_pp=pt['R_pp'], R_deceq=pt['R_deceq'], D=pt['D'], RR=pt['RR'], D_deceq=pt['D_deceq'],
                  share_resamples_denE_gt0=float(np.mean(EV['denE'] > 0)),
                  RR_E5qN=L.summ(boot[:, 0], pt_rr_e5q), RR_NmE5qN=L.summ(boot[:, 1], pt_diff), RR_N=L.summ(rrN_b, pt['RR']['N']),
                  D_deceq_ci={a: L.pct(L.dec_eq(EV['D'][a], EV['n'])) for a in ('N', 'E5qN')}),
    grid=dict(grid='[0] + logspace(-2, 3, 201) (rev_common_v01.GRID)', n=pg['n'], denE=denG, R_pp=denG / L.NLEV, c0=pg['c0'], C=pg['C'],
              D=DG, RR={a: L.ratio(DG[a], denG) for a in ('N', 'P', 'Prec')}, D_deceq={a: L.dec_eq(DG[a], pg['n']) for a in ('N', 'P', 'Prec')},
              placebo_factor=dict(P=m_N ** 2, Prec=RATIO_REC ** 2)),
    partial_oracles=dict(seed=SEED_PO, n_uniforms=N_TOTAL, n_decisions_all=N_TOTAL, n_evaluated=n_dec,
                         evaluated_share_with_E={nm: po_share[nm] / n_dec for nm in PO},
                         RR=dict(zip(PO, PO_RR)), D=dict(zip(PO, [pt['D'][nm] for nm in PO])), dec=dict(zip(PO, PO_DEC)),
                         grading_rule='PO25 > 0 and PO25 < PO50 < PO75 strictly; false if any is null'),
    checks=checks)


def clean(x):
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, (float, np.floating)):
        return float(x) if math.isfinite(float(x)) else None
    return x


doc = dict(code='x_desc_v13.py', program='first', amendment='AMENDMENT_11_v13.md sec. 3.6 (X fixed descriptive outputs)',
           definitions='crossing\\CD_DEFINITIONS_X_DESC_v13.md', definitions_sha256=CC.sha(DEFS), family=FAM, gate=gate,
           test_old=bool(args.test_old), runs=run_ids, n_runs=NR, n_listed=len(listed), listed_without_arrays=sorted(set(listed) - set(run_ids)),
           replacements=replacements, draw='optA_lib_v02.boot_counts(%d, %d, %d), first %d rows' % (NR, CC.NBOOT, CC.SEED_BOOT, args.nboot),
           intervals='nominal 95% percentile (np.percentile(x[finite], [2.5, 97.5]))', values=V, details=details)
doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
doc['code_sha256'] = {str(f.relative_to(CD)): CC.sha(f) for f in (HERE / 'x_desc_v13.py', CD / 'analysis' / 'cd_common_v13.py',
                                                                   CD / 'analysis' / 'gl_fast_v13.py')}
doc['code_sha256']['shared/trackers/trk_score_v01.py'] = CC.sha(CC.SHARED / 'trk_score_v01.py')
OUTD.mkdir(exist_ok=True)
CC.write_once(OUTF, clean(doc))
log('written %s: %s' % (OUTF.name, json.dumps(clean(V))))
