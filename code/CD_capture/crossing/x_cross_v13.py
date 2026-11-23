"""X (AMENDMENT_11_v13.md sec. 3): the locked confirmatory pedestrian-crossing test, open loop. First program. New file, 21 Nov 2026
(Claude Opus 5.5, session CD); rewritten 14:20 EST for A11 sec. 3 (pedestrian only, X0-X2 with E5_N, calibrated intervals), before
any fresh crossing value existed. Specification: A11 sec. 3 and crossing\\CD_DEFINITIONS_X_v13.md. C's definitions and seeds
(c_lead_v13.py, A10 sec. 2, 5.3) with the departures listed there.

Runs: the 390 study positions of CASES_X_PC_v13.json (SHA-256 given with --cases-sha), replacements from REPLACEMENTS_X_v13.json
({case: reserve case}, A11 sec. 3.2), job ids pc13x_<case>_native, ascending run id. The analysed set is those whose arrays exist
(the frozen extractor writes arrays only for CAPTURED_AND_REVIEWED archives); fewer than n_min = 332 -> 'descriptive, under-run'.
Arrays: arrays_x/CV0/<rid>.npz (online tracker of record, P-bar of record); meta family must be pedestrian_crossing.
Population: all evaluated decisions; 3 s commitment; gridless step frontier at 201 caution levels (gl_fast_v13 = the library of
record, checked at the full sample against trk_score_v01.rr_gl).
Sources (package B's frozen library trk_score_v01): F0, E, N; u = e5_u(F0, E);
  E5_N  = add_oracle(F0, m_N, A_N, u), m_N = median and A_N = (q95 - q05) / (2 m_N) of margin_ratios(N, F0) on these runs (A10 sec. 2.2);
  E5p_N = add_oracle(F0, m_N, A_N, permute_u(u)) (default_rng(20261915));
  E5rec, E5recp = the same with the record amplitude (1.1029, 0.05) - descriptive only (A11 sec. 3.5).
Intervals: percentile over 20,000 run resamples, default_rng(20261911). Main statistics (R_gl, RR_gl(E5_N), RR_gl(E5_N) - RR_gl(E5p_N),
RR_gl(N)) at A10 sec. 2.6's calibrated level (cd_common_v13.calibrate_all, group x_ped_main; --calib local|export|import); descriptive
ones at nominal 95%. --intervals nominal95 (old-run test only) or nominal99 (A11 sec. 3.7 emergency rule) skip the calibration.
Sequence (A11 sec. 3.5): X0 room (R_gl lower end > 0 and D_gl(E, F0) > 0 in >= 97.5% of resamples); X1 (lower ends of RR_gl(E5_N) and
RR_gl(E5_N) - RR_gl(E5p_N) > 0); X2 = A10 H3's class with r = RR_gl(N), c = RR_gl(E5_N) (recovers / uninformative variation /
amplitude-limited / inconclusive; 'barely varies' flag; passes with the first three; r / c under 'recovers').
'Confirmed' = it and every earlier one passed. Under-run: no hypothesis is confirmatory. X0 fails: 'No measurable room on fresh crossing
runs; nothing is tested there.' (A11 sec. 3.8).
Descriptive here (A11 sec. 3.6): RR_gl(N)'s interval against (-delta, delta); the margin-ratio check; record-amplitude E5; counts (runs,
evaluated decisions, contact runs, replacements). The other sec. 3.6 outputs (E5q_N, grid placebo, partial oracles) are a separate program.
Gate: refuses unless revision_v13/LOCK_A11.txt exists. --test-old runs on the STORED arrays of record of the 51 old pedestrian-crossing runs
(gateR_rt_v01) as stand-in runs; it never reads a fresh run and writes TESTOLD_ files.
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 crossing\\x_cross_v13.py (--test-old | --cases-sha SHA) --intervals calibrated|nominal95|nominal99
         [--calib local|export|import] [--nboot N]
Writes crossing/out/[TESTOLD_]X_CROSS_pedestrian_crossing_v13[_PENDING_CALIB].json (never overwritten).
"""
import argparse, json, os, pathlib, sys, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
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
L = CC.L
FAM = 'pedestrian_crossing'
N_STUDY, N_MIN = 390, 332
LOCK_A11 = CC.V13 / 'LOCK_A11.txt'
STORED = pathlib.Path(r'<library folder>\gateR_rt_v01')
ARRX = CD / 'arrays_x' / 'CV0'
OUTD = HERE / 'out'

ap = argparse.ArgumentParser()
ap.add_argument('--test-old', action='store_true'); ap.add_argument('--cases-sha')
ap.add_argument('--intervals', required=True, choices=('calibrated', 'nominal95', 'nominal99'))
ap.add_argument('--calib', choices=('local', 'export', 'import'), default='export'); ap.add_argument('--nboot', type=int, default=CC.NBOOT)
ap.add_argument('--outer', type=int, default=CC.N_OUTER)
args = ap.parse_args()
D = CC.DELTA
CC.N_OUTER = args.outer; CC.CALIB_MODE = args.calib
if args.test_old:
    CC.CALIB_DIR = OUTD / 'calib_testold'
    gate = 'TEST_OLD: stored arrays of record of old runs only; no fresh value'
else:
    if not LOCK_A11.is_file(): raise SystemExit('REFUSED: LOCK_A11.txt does not exist; no fresh crossing value may be computed (A11 sec. 3.3)')
    gate = 'LOCK_A11 sha256 ' + CC.sha(LOCK_A11)
    if args.cases_sha is None: raise SystemExit('REFUSED: --cases-sha is required')
    if args.nboot != CC.NBOOT or args.outer != CC.N_OUTER or args.intervals == 'nominal95':
        raise SystemExit('REFUSED: --nboot, --outer and nominal95 are test options (--test-old only)')
t00 = time.time()
log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)
PEND = args.intervals == 'calibrated' and args.calib == 'export'
OUTF = OUTD / (('TESTOLD_' if args.test_old else '') + f'X_CROSS_{FAM}_v13' + ('_PENDING_CALIB' if PEND else '') + '.json')
if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)


# ------------------------------------------------------------------------------------------------ runs
def run_dict(rid, z, desired):
    ev = z['evaluated'].astype(bool)
    return dict(run=rid, desired=float(desired), idx55=z['idx55'].astype(np.int64), clear1=L.clean_clear(z['clear']), vbar=z['vbar'],
                ev=ev, masks=(ev,), sel={}, late={},
                crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float)})


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


contact = None
if args.test_old:
    runs = []; contact = 0
    for f in sorted(STORED.glob('*.npz')):
        z = np.load(f, allow_pickle=False); m = json.loads(str(z['meta']))
        if m.get('family') == FAM:
            runs.append(run_dict(f.stem, z, m['desired'])); contact += int(m.get('contact_k', -1) >= 0)
    run_ids = [r['run'] for r in runs]; listed = run_ids; replacements = {}
else:
    listed, replacements = fresh_list(); runs = []; run_ids = []; contact = 0
    for rid in listed:
        f = ARRX / (rid + '.npz')
        if not f.is_file(): continue
        z = np.load(f, allow_pickle=False); m = json.loads(str(z['meta']))
        assert m['family'] == FAM and m['run_id'] == rid, rid
        runs.append(run_dict(rid, z, m['desired'])); run_ids.append(rid); contact += int(m.get('contact_k', -1) >= 0)
NR = len(runs)
UNDER = (not args.test_old) and NR < N_MIN
log('runs %d of %d listed (%s)%s' % (NR, len(listed), 'TEST: stored arrays of old runs' if args.test_old else 'fresh pedestrian crossing',
                                     '; UNDER-RUN' if UNDER else ''))

# ------------------------------------------------------------------------------------------------ sources
u, uinfo = TS.e5_u(runs, 'F0', 'E')
up = TS.permute_u(runs, u)                                   # default_rng(20261915)
rs = TS.ratio_summary(TS.margin_ratios(runs, 'N', 'F0'))
TS.add_oracle(runs, 'E5N', 'F0', rs['median'], rs['A'], u)
TS.add_oracle(runs, 'E5pN', 'F0', rs['median'], rs['A'], up)
TS.add_oracle(runs, 'E5rec', 'F0', CC.RATIO, 0.05, u)
TS.add_oracle(runs, 'E5recp', 'F0', CC.RATIO, 0.05, up)
NAMES = ['F0', 'E', 'N', 'E5N', 'E5pN', 'E5rec', 'E5recp']
G = TS.gridless(runs, NAMES)
pt = TS.rr_gl(G, 'F0', 'E', NAMES[2:], pop=0)
P1 = CC.prep(G, NAMES, 0)
Wfull = np.ones((1, NR))
chk = CC.evaluate(P1, Wfull)
assert chk['denE'][0] == pt['denE'] and all(chk['D'][a][0] == pt['D'][a] for a in NAMES[2:]), 'gl_fast differs from the library'
log('gl_fast identical to the library at the full sample')
W = CC.counts(NR, args.nboot, CC.SEED_BOOT)
B1 = CC.evaluate(P1, W)
stats = CC.GLStat(CC.prep(G, ['F0', 'E', 'N', 'E5N', 'E5pN'], 0), [('R',), ('RR', 'E5N'), ('RRdiff', 'E5N', 'E5pN'), ('RR', 'N')])
SN = ['R_gl', 'RR_E5N', 'RR_E5N_minus_E5pN', 'RR_N']
full = stats(Wfull)[0]; boot = stats(W)
if args.intervals == 'calibrated':
    cal = CC.calibrate_all(stats, NR, full, SN, log=log, label='x_ped_main' if not args.test_old else 'x_ped_main_testold')
else:
    cal = {nm: dict(level=0.95 if args.intervals == 'nominal95' else 0.99, rule=args.intervals + ' (no double bootstrap)') for nm in SN}
lev = {nm: cal[nm]['level'] for nm in SN}
S = {nm: CC.interval(boot[:, j], full[j], lev[nm]) for j, nm in enumerate(SN)}
desc = CC.GLStat(CC.prep(G, ['F0', 'E', 'E5rec', 'E5recp'], 0), [('RR', 'E5rec'), ('RRdiff', 'E5rec', 'E5recp')])
fd = desc(Wfull)[0]; bd = desc(W)
SD = {'RR_E5rec': CC.interval(bd[:, 0], fd[0], 0.95), 'RR_E5rec_minus_E5recp': CC.interval(bd[:, 1], fd[1], 0.95)}
doc = dict(code='x_cross_v13.py', amendment='AMENDMENT_11_v13.md sec. 3 (X)', family=FAM, gate=gate, runs=run_ids, n_runs=NR, n_listed=len(listed),
           listed_without_arrays=sorted(set(listed) - set(run_ids)), replacements=replacements, test_old=args.test_old, under_run=UNDER,
           intervals=args.intervals, calib_mode=args.calib if args.intervals == 'calibrated' else None, calibration=cal,
           draw='default_rng(%d), %d run resamples' % (CC.SEED_BOOT, args.nboot), delta=D, e5_u=uinfo, ratio_summary_N_F0=rs, main=S,
           descriptive=dict(SD, RR_N_inside_delta=bool(S['RR_N']['ci_level'][0] > -D and S['RR_N']['ci_level'][1] < D)))
doc['room'] = dict(R_pp=pt['R_pp'], R_deceq=pt['R_deceq'], n=pt['n'], share_resamples_denE_gt0=float(np.mean(B1['denE'] > 0)),
                   R_deceq_ci=L.pct(L.dec_eq(B1['denE'], B1['n'])))
doc['D_deceq'] = {a: dict(point=pt['D_deceq'][a], ci=L.pct(L.dec_eq(B1['D'][a], B1['n']))) for a in NAMES[2:]}
doc['counts'] = dict(runs=NR, evaluated_decisions=int(pt['n']), contact_runs=contact, replacements=len(replacements))
log('intervals done (%s)' % args.intervals)

# ------------------------------------------------------------------------------------------------ the sequence (A11 sec. 3.5)
X0 = bool(S['R_gl']['ci_level'][0] > 0 and doc['room']['share_resamples_denE_gt0'] >= 0.975)
X1 = bool(S['RR_E5N']['ci_level'][0] > 0 and S['RR_E5N_minus_E5pN']['ci_level'][0] > 0)
rlo = S['RR_N']['ci_level'][0]; clo, chi = S['RR_E5N']['ci_level']
if rlo > 0: cls = 'recovers'
elif clo > D: cls = 'uninformative variation'
elif clo > -D and chi < D: cls = 'amplitude-limited'
else: cls = 'inconclusive'
with np.errstate(divide='ignore', invalid='ignore'):
    eff = CC.interval(boot[:, 3] / boot[:, 1], full[3] / full[1], lev['RR_N']) if cls == 'recovers' else None
X2 = cls in ('recovers', 'uninformative variation', 'amplitude-limited')
doc['X2'] = dict(classification=cls, barely_varies=rs['barely_varies'], r=S['RR_N'], c=S['RR_E5N'], efficiency_r_over_c=eff, passes=X2)
seq = {}; ok = not UNDER
for h, p in (('X0', X0), ('X1', X1), ('X2', X2)):
    ok = ok and p
    seq[h] = dict(passes=p, confirmed=ok, label=('descriptive, under-run' if UNDER else 'confirmatory' if ok else 'not confirmatory'))
doc['sequence'] = seq
doc['statement'] = ('descriptive, under-run' if UNDER else None if X0 else 'No measurable room on fresh crossing runs; nothing is tested there.')
doc['pending_calibration'] = PEND


def _f(x):
    return None if x is None or not np.isfinite(x) else float(x)


def _ci(s):
    c = s['ci_level']; return None if not (np.isfinite(c[0]) and np.isfinite(c[1])) else [float(c[0]), float(c[1])]


V = {}; pre = 'X.ped.'                                      # flat values (CD_DEFINITIONS_X sec. 7)
V[pre + 'n_runs'] = NR; V[pre + 'n_dec'] = int(pt['n']); V[pre + 'n_contact'] = contact; V[pre + 'n_replaced'] = len(replacements)
V[pre + 'under_run'] = UNDER
V[pre + 'R'] = _f(pt['R_pp']); V[pre + 'R.dec'] = _f(pt['R_deceq']); V[pre + 'R.share_pos'] = doc['room']['share_resamples_denE_gt0']
for nm, k in (('R_gl', 'R'), ('RR_E5N', 'RR_E5N'), ('RR_E5N_minus_E5pN', 'RR_E5NmP'), ('RR_N', 'RR_N')):
    if k != 'R': V[pre + k] = _f(full[SN.index(nm)])
    V[pre + k + '.ci'] = _ci(S[nm]); V[pre + k + '.level'] = float(lev[nm])
V[pre + 'RR_E5rec'] = _f(fd[0]); V[pre + 'RR_E5rec.ci'] = _ci(SD['RR_E5rec']); V[pre + 'RR_E5rec.level'] = 0.95
V[pre + 'RR_E5recmP'] = _f(fd[1]); V[pre + 'RR_E5recmP.ci'] = _ci(SD['RR_E5rec_minus_E5recp']); V[pre + 'RR_E5recmP.level'] = 0.95
V[pre + 'RR_N.inside_delta'] = doc['descriptive']['RR_N_inside_delta']
V[pre + 'ratio.median'] = _f(rs['median']); V[pre + 'ratio.A'] = _f(rs['A']); V[pre + 'ratio.within5'] = _f(rs['share_within_5pct'])
V[pre + 'ratio.barely'] = bool(rs['barely_varies'])
V[pre + 'X2.class'] = cls; V[pre + 'X2.eff'] = _f(eff['point']) if eff else None; V[pre + 'X2.eff.ci'] = _ci(eff) if eff else None
for h in ('X0', 'X1', 'X2'): V[pre + h] = seq[h]['passes']; V[pre + h + '.confirmed'] = seq[h]['confirmed']
V[pre + 'tested'] = X0
doc['values'] = V
doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
doc['code_sha256'] = {str(f.relative_to(CD)): CC.sha(f) for f in (HERE / 'x_cross_v13.py', CD / 'analysis' / 'cd_common_v13.py', CD / 'analysis' / 'gl_fast_v13.py')}
OUTD.mkdir(exist_ok=True)
CC.write_once(OUTF, doc)
log('written %s; sequence %s; X2 %s' % (OUTF.name, {h: v['passes'] for h, v in seq.items()}, cls))
