r"""Revision v13, AMENDMENT_12 sec. 3a.4-3a.5: the dose-response over p in {0.05, 0.10, 0.20, 0.30} and the decomposition of the gain at
p = 0.10, on the new lead-braking runs. New file, 22 Nov 2026 (Claude Opus 5.5, session F). Machinery as dr_analysis_v02.py (CD's
cd_common_v13: gl_fast, GLStat, counts, the A10 sec. 2.6 rule calibrated_levels; trk_score_v01: gridless, rr_gl).
Inputs: F_dropout\out_a12\<ptag>\arrays\DR\<run>.npz (dr_extract_v02.py dr --p <p>) for the four p; the run set = the 'fresh' runs of
out_a12\p010\DR_MASKS_p010.json (the same runs must exist at every p).
Dose-response (sec. 3a.4):
  r(p) = RR_gl(N_DR(p)) on p's own room (F0_DR(p), E_DR(p)); per run resample w (optA_lib_v02.boot_counts(n, 20000, 20261911), the SAME
  w at every p): r*(p); b* = sum_p (p - pbar)(r*(p) - rbar*) / sum_p (p - pbar)^2, pbar = 0.1625; NaN if any r*(p) is NaN.
  Holm: p_b = (1 + #{b* <= 0 or NaN}) / 20,001. Calibration: double bootstrap of b (A10 sec. 2.6: outer default_rng(20261912), inner
  20261913 / 20261914, checks 20261920) by dr_slope_remote_v01.py on four exported GLStat jobs ([('RR', 'N')], one per p); this
  program exports (--calib export) and imports (--calib import; cd_common_v13.calibrated_levels). b passes iff its lower end > 0.
  Descriptive: r(p) and R_gl(p) with 95% percentile intervals; the masked share of frames per p; Spearman rho between p and r(p).
Decomposition (sec. 3a.5, p = 0.10): per evaluated decision, by the frame it uses (dr_frame; the run's masked frames from meta):
  in-dropout = the frame is masked; re-acquisition = not masked and frame - 1 or frame - 2 is masked; steady = the rest.
  N_S = N_DR's critical scales on S, F0_DR's elsewhere; share_S = RR_gl(N_S) on DR's own room; remainder = RR_gl(N_DR) - sum_S share_S.
  95% percentile intervals on the same draw; decision-equivalents of each D_gl(N_S, F0).
Output: out_a12\DR2_DOSE_v01.json (export mode: _PENDING_CALIB), `values` with DR.slope, DR.slope.ci, DR.slope.level, DR.slope.p,
DR.slope.passes, DR.r_<ptag>(.ci), DR.R_<ptag>(.ci), DR.masked_share_<ptag>, DR.spearman, DR.dec.<in|reacq|steady|rest>(.ci) and
DR.dec.<in|reacq|steady>.deceq(.ci). Refuses without LOCK_A12a (except --test-old: out_a12\testold_<ptag>\).
Usage: python -I -B -X utf8 dr_dose_v01.py [--calib local-none|export|import] [--test-old] [--outer N]
"""
import argparse, json, pathlib, sys, time
import numpy as np
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
DRD = HERE.parent
WORK = DRD.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(WORK / 'CD_capture' / 'analysis'))
sys.path.insert(0, str(WORK / 'shared' / 'trackers'))
import cd_common_v13 as CC               # noqa: E402
import trk_env_v01 as env                # noqa: E402
env.setup()
import trk_score_v01 as TS               # noqa: E402
import dr_extract_v02 as X               # noqa: E402
import dr_masks_v03 as M3                # noqa: E402
L = CC.L
PS = M3.P_VALUES
PBAR_ = float(np.mean(PS))

ap = argparse.ArgumentParser()
ap.add_argument('--calib', choices=('none', 'export', 'import'), default='none')
ap.add_argument('--test-old', action='store_true'); ap.add_argument('--outer', type=int, default=CC.N_OUTER)
ap.add_argument('--nboot', type=int, default=CC.NBOOT)
args = ap.parse_args()
CC.N_OUTER = args.outer
if not args.test_old and not X.LOCK.is_file():
    raise SystemExit('REFUSED: no LOCK_A12a.txt (AMENDMENT_12 sec. 3a)')
ROOT = DRD / 'out_a12'
tag = (lambda p: ('testold_' if args.test_old else '') + M3.ptag(p))
CALIB = ROOT / ('calib_dose_testold' if args.test_old else 'calib_dose')
OUTF = ROOT / (('TESTOLD_' if args.test_old else '') + 'DR2_DOSE_v01' + ('_PENDING_CALIB' if args.calib == 'export' else '') + '.json')
if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)
t00 = time.time()
log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)


def arr_dir(p):
    return (ROOT / tag(p) / 'DR') if args.test_old else (ROOT / tag(p) / 'arrays' / 'DR')


if args.test_old:
    run_ids = sorted(q.stem for q in arr_dir(0.10).glob('*.npz') if not q.name.endswith('.partial.npz'))
else:
    run_ids = sorted(json.loads((ROOT / tag(0.10) / ('DR_MASKS_%s.json' % M3.ptag(0.10))).read_text(encoding='utf-8'))['fresh'])
NR = len(run_ids)


def load(p):
    runs = []
    for rid in run_ids:
        z = np.load(arr_dir(p) / (rid + '.npz'), allow_pickle=False)
        meta = json.loads(str(z['meta']))
        ev = z['evaluated'].astype(bool)
        runs.append(dict(run=rid, desired=float(z['des'][0]), meta=meta, k=z['k'], ev=ev, v0=z['v0'], ph=z['phase'], vbar=z['vbar'],
                         idx55=z['idx55'].astype(np.int64), clear_raw=z['clear'], clear1=L.clean_clear(z['clear']), masks=(ev,),
                         crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float)},
                         sel={}, late={}, dr_frame=z['dr_frame'], dr_masked=z['dr_masked'].astype(bool)))
    return runs


W = CC.counts(NR, args.nboot, CC.SEED_BOOT)
Wfull = np.ones((1, NR))
doc = dict(code='dr_dose_v01.py', amendment='AMENDMENT_12 sec. 3a.4-3a.5', runs=run_ids, n_runs=NR, p_values=list(PS),
           draw='optA_lib_v02.boot_counts(%d, %d, %d), the same draw at every p' % (NR, args.nboot, CC.SEED_BOOT), test_old=args.test_old)
vals = {}
R_full = {}; R_boot = {}; r_full = {}; r_boot = {}; stats = {}
for p in PS:
    runs = load(p)
    G = TS.gridless(runs, ['F0', 'E', 'N'])
    pt = TS.rr_gl(G, 'F0', 'E', ['N'], pop=0)
    st = CC.GLStat(CC.prep(G, ['F0', 'E', 'N'], 0), [('R',), ('RR', 'N')])
    f = st(Wfull)[0]; b = st(W)
    assert f[1] == pt['RR']['N']
    R_full[p], r_full[p] = float(f[0]), float(f[1]); R_boot[p], r_boot[p] = b[:, 0], b[:, 1]
    stats[p] = CC.GLStat(CC.prep(G, ['F0', 'E', 'N'], 0), [('RR', 'N')])
    tg = M3.ptag(p)
    vals['DR.r_' + tg] = r_full[p]; vals['DR.r_%s.ci' % tg] = [float(x) for x in CC.interval(b[:, 1], f[1], 0.95)['ci_level']]
    vals['DR.R_' + tg] = R_full[p]; vals['DR.R_%s.ci' % tg] = [float(x) for x in CC.interval(b[:, 0], f[0], 0.95)['ci_level']]
    ms = sum(len(r['meta']['masked']) for r in runs) / sum(r['meta']['n_det_rows'] for r in runs)
    vals['DR.masked_share_' + tg] = float(ms)
    ok_p = all(M3.mask(r['meta']['case_id'], r['meta']['n_det_rows'], p) == list(r['meta']['masked']) for r in runs)
    vals['DR.masks_identical_all'] = bool(vals.get('DR.masks_identical_all', True) and ok_p)
    log('p %.2f: r %.6f R %.6f masked share %.4f' % (p, r_full[p], R_full[p], ms))
    if abs(p - 0.10) < 1e-12:
        runs10 = runs


def slope(rmat):
    """rmat (B, 4) in the order of PS -> OLS slope per row (NaN if any NaN)."""
    x = np.array(PS) - PBAR_
    with np.errstate(invalid='ignore'):
        return (rmat - np.nanmean(rmat, axis=1, keepdims=True)) @ x / (x @ x) if rmat.size else np.array([])


rfull = np.array([[r_full[p] for p in PS]]); rboot = np.stack([r_boot[p] for p in PS], axis=1)
b_full = float(slope(rfull)[0])
b_boot = slope(rboot); b_boot[~np.isfinite(rboot).all(axis=1)] = np.nan
vals['DR.slope'] = b_full
vals['DR.slope.p'] = float((1 + np.sum(~(b_boot > 0))) / (b_boot.size + 1))
from scipy.stats import spearmanr          # noqa: E402
vals['DR.spearman'] = float(spearmanr(np.array(PS), rfull[0]).statistic)
level = 0.95; cal = None
if args.calib == 'export':
    CALIB.mkdir(parents=True, exist_ok=True)
    jobs = {}
    for p in PS:
        jp = CALIB / ('dose_%s.job.npz' % M3.ptag(p)); stats[p].save(jp); jobs[M3.ptag(p)] = CC.sha(jp)
    (CALIB / 'dose_slope.meta.json').write_text(json.dumps(dict(label='dose_slope', n_run=NR, full=[b_full], names=['slope'],
        p_values=list(PS), jobs=jobs, seeds=[CC.SEED_OUTER, CC.SEED_INNER, CC.SEED_INNER2], n_outer=CC.N_OUTER, n_inner=CC.N_INNER)),
        encoding='utf-8')
    cal = dict(level=0.95, rule='PENDING: exported for dr_slope_remote_v01.py', pending=True)
elif args.calib == 'import':
    res = {}
    for seed in (CC.SEED_INNER, CC.SEED_INNER2):
        fz = CALIB / ('dose_slope_%d.npz' % seed)
        if fz.is_file():
            z = np.load(fz); assert np.array_equal(z['full'], np.array([b_full]), equal_nan=True), 'slope full-sample value differs'
            res[seed] = (z['p_lt'], z['p_le'])
    assert CC.SEED_INNER in res, 'no remote result for the slope'
    cal = CC.calibrated_levels(res[CC.SEED_INNER], res.get(CC.SEED_INNER2, res[CC.SEED_INNER]), ['slope'])['slope']
    level = cal['level']
Sb = CC.interval(b_boot, b_full, level)
vals['DR.slope.ci'] = [float(x) for x in Sb['ci_level']]; vals['DR.slope.level'] = level
vals['DR.slope.passes'] = bool(Sb['ci_level'][0] > 0)
doc['slope_calibration'] = cal

# ------------------------------------------------------------------------------------------------ decomposition at p = 0.10
for r in runs10:
    ms = np.zeros(int(r['meta']['n_det_rows']) + 3, bool); ms[list(r['meta']['masked'])] = True
    fr = r['dr_frame']
    m_in = r['dr_masked'] & (fr >= 0)
    prev1 = np.where(fr >= 1, ms[np.clip(fr - 1, 0, None)], False); prev2 = np.where(fr >= 2, ms[np.clip(fr - 2, 0, None)], False)
    m_re = (~r['dr_masked']) & (fr >= 0) & (prev1 | prev2)
    m_st = ~(m_in | m_re)
    for nm, m in (('N_in', m_in), ('N_re', m_re), ('N_st', m_st)):
        r['crit'][nm] = np.where(m[:, None], r['crit']['N'], r['crit']['F0'])
    r['n_pop'] = {nm: int((m & r['ev']).sum()) for nm, m in (('in', m_in), ('reacq', m_re), ('steady', m_st))}
SRC = ['F0', 'E', 'N', 'N_in', 'N_re', 'N_st']
G10 = TS.gridless(runs10, SRC)
pt10 = TS.rr_gl(G10, 'F0', 'E', SRC[2:], pop=0)
P10 = CC.prep(G10, SRC, 0)
sd = CC.GLStat(P10, [('RR', 'N'), ('RR', 'N_in'), ('RR', 'N_re'), ('RR', 'N_st')])
fd = sd(Wfull)[0]; bd = sd(W)
B10 = CC.evaluate(P10, W)
rest_full = fd[0] - fd[1:].sum(); rest_boot = bd[:, 0] - bd[:, 1:].sum(axis=1)
for j, nm in ((1, 'in'), (2, 'reacq'), (3, 'steady')):
    vals['DR.dec.' + nm] = float(fd[j]); vals['DR.dec.%s.ci' % nm] = [float(x) for x in CC.interval(bd[:, j], fd[j], 0.95)['ci_level']]
    src = SRC[2 + j]
    vals['DR.dec.%s.deceq' % nm] = float(pt10['D_deceq'][src])
    vals['DR.dec.%s.deceq.ci' % nm] = [float(x) for x in L.pct(L.dec_eq(B10['D'][src], B10['n']))]
    vals['DR.dec.%s.n' % nm] = int(sum(r['n_pop'][nm] for r in runs10))
vals['DR.dec.rest'] = float(rest_full); vals['DR.dec.rest.ci'] = [float(x) for x in CC.interval(rest_boot, rest_full, 0.95)['ci_level']]
vals['DR.dec.r'] = float(fd[0])
doc['values'] = vals
doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
OUTF.write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
log('WROTE %s: slope %.6f (p %.5f) level %.4f ci %s' % (OUTF, b_full, vals['DR.slope.p'], level, vals['DR.slope.ci']))
