r"""Revision v13, AMENDMENT_13 sec. 3 (v02): N_DR against a fixed COAST-COUNT margin (F0_coast); v01's two-population flag as a
descriptive secondary (F0_flag2). New file, 22 Nov 2026 (Claude Opus 5.5, session F): a copy of dr_flag_v01.py (FREEZE_DR_A13) with
the arm changed to F_dropout\A13_3_DRFLAG_v02.md (the coordinator's decision, from the domain seat's report, before any value).
  Populations by the decision's frame (dr_dose_v01's decomposition): in-dropout split by its consecutive-masked-frame count dr_age
  (c = 1, 2, 3; above 3 -> 3), re-acquisition, steady.
  k (sec. 3.3): M_S = median of cN / cF0 over the finite, positive rows of the evaluated decisions in S, on A11's 105 fresh runs
  (F_dropout\out\arrays\DR\); k_c = M_c / M_st, k_re = M_re / M_st, k_in = M_in / M_st (pooled in-dropout); a coast-count population
  with fewer than 50 rows falls back to k_in.
  F0_coast = cF0 times k_c / k_re / 1; F0_flag2 = cF0 times k_in / k_re / 1 (secondary).
  Test (sec. 3.4): on the 150 new runs (F_dropout\out_a12\p010\arrays\DR\, DR2's room): RR_gl(F0_coast), RR_gl(N_DR),
  delta = RR_gl(N) - RR_gl(F0_coast) with boot_counts(150, 20000, 20261911), plain 95% percentile intervals (no calibration);
  p_F = (1 + #{delta* <= 1e-12 or NaN}) / 20,001 (ties within round-off count against); passes if delta's lower end > 0; within_equiv if both ends lie in (-0.05, 0.05).
  Secondary: RR_gl(F0_flag2) and delta_flag2 on the same draw.
Refuses without LOCK_A13b.txt. --test-old: k fitted on, and the test run on, the 35 old test runs (F_dropout\out\testold\DR\), a code
test only; writes out_a13\TESTOLD_DRF_RESULTS_v02.json.
Usage: python -I -B -X utf8 dr_flag_v02.py [--test-old] [--nboot N]   -> F_dropout\out_a13\DRF_RESULTS_v02.json (refuses to overwrite)
"""
import argparse, json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
DRD = HERE.parent
WORK = DRD.parent
V13 = WORK.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(WORK / 'CD_capture' / 'analysis'))
sys.path.insert(0, str(WORK / 'shared' / 'trackers'))
import cd_common_v13 as CC               # noqa: E402
import trk_env_v01 as env                # noqa: E402
env.setup()
import trk_score_v01 as TS               # noqa: E402
L = CC.L
LOCK = V13 / 'LOCK_A13b.txt'
EQUIV = 0.05
MIN_ROWS = 50
TIE = 1e-12                               # sec. 3.4: delta* <= TIE counts against the test (ties within round-off)

ap = argparse.ArgumentParser()
ap.add_argument('--test-old', action='store_true'); ap.add_argument('--nboot', type=int, default=CC.NBOOT)
args = ap.parse_args()
if not args.test_old and not LOCK.is_file():
    raise SystemExit('REFUSED: no LOCK_A13b.txt (AMENDMENT_13 sec. 3); no DRF value before the lock')
TOLD = DRD / 'out' / 'testold' / 'DR'      # the 35 old test runs under the A11 masks (p = 0.10), dr_extract_v01 --test-old
FIT_DIR = TOLD if args.test_old else DRD / 'out' / 'arrays' / 'DR'
TEST_DIR = TOLD if args.test_old else DRD / 'out_a12' / 'p010' / 'arrays' / 'DR'
OUTD = DRD / 'out_a13'
OUTF = OUTD / (('TESTOLD_' if args.test_old else '') + 'DRF_RESULTS_v02.json')
if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)
t00 = time.time()
log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)


def stems(d):
    return sorted(q.stem for q in d.glob('*.npz') if not q.name.endswith('.partial.npz'))


fit_ids = stems(FIT_DIR)
if args.test_old:
    test_ids = stems(TEST_DIR)
else:
    test_ids = sorted(json.loads((DRD / 'out_a12' / 'p010' / 'DR_MASKS_p010.json').read_text(encoding='utf-8'))['fresh'])
    if len(fit_ids) != 105 or len(test_ids) != 150: raise SystemExit('REFUSED: run sets %d / %d, expected 105 / 150' % (len(fit_ids), len(test_ids)))
    if set(fit_ids) & set(test_ids): raise SystemExit('REFUSED: fit and test runs overlap')


def pops(z, meta):
    """Per decision: coast count c (0 if not in dropout; 1..3, above 3 -> 3), re-acquisition, steady (dr_dose_v01's decomposition)."""
    ms = np.zeros(int(meta['n_det_rows']) + 3, bool); ms[list(meta['masked'])] = True
    fr = z['dr_frame']; dm = z['dr_masked'].astype(bool)
    m_in = dm & (fr >= 0)
    prev1 = np.where(fr >= 1, ms[np.clip(fr - 1, 0, None)], False); prev2 = np.where(fr >= 2, ms[np.clip(fr - 2, 0, None)], False)
    m_re = (~dm) & (fr >= 0) & (prev1 | prev2)
    c = np.where(m_in, np.clip(np.asarray(z['dr_age'], np.int64), 1, 3), 0)
    return c, m_in, m_re, ~(m_in | m_re)


# ------------------------------------------------------------------------------------------------ k on the fit runs (sec. 3.3)
POPS = ('1', '2', '3', 'in', 're', 'st')
rat = {S: [] for S in POPS}
for rid in fit_ids:
    z = np.load(FIT_DIR / (rid + '.npz'), allow_pickle=False); meta = json.loads(str(z['meta']))
    ev = z['evaluated'].astype(bool); cN = np.asarray(z['cN'], float); cF = np.asarray(z['cF0'], float)
    c, m_in, m_re, m_st = pops(z, meta)
    for S, m in (('1', c == 1), ('2', c == 2), ('3', c == 3), ('in', m_in), ('re', m_re), ('st', m_st)):
        sel = ev & m; a = cN[sel]; b = cF[sel]
        ok = np.isfinite(a) & np.isfinite(b) & (a > 0) & (b > 0)
        rat[S].append(a[ok] / b[ok])
rat = {S: np.concatenate(v) if v else np.array([]) for S, v in rat.items()}
M = {S: float(np.median(v)) if v.size else float('nan') for S, v in rat.items()}
k_in, k_re = M['in'] / M['st'], M['re'] / M['st']
kc, fb = {}, {}
for c_ in ('1', '2', '3'):
    fb[c_] = bool(rat[c_].size < MIN_ROWS)
    kc[c_] = k_in if fb[c_] else M[c_] / M['st']
log('k on %d runs: M %s rows %s; k_c %s (fallback %s), k_re %.6f, k_in %.6f' % (len(fit_ids), M, {S: int(v.size) for S, v in rat.items()},
                                                                               kc, fb, k_re, k_in))


# ------------------------------------------------------------------------------------------------ the test runs (sec. 3.4)
def load_test():
    runs = []; npop = {'c1': 0, 'c2': 0, 'c3': 0, 'reacq': 0, 'steady': 0}
    for rid in test_ids:
        z = np.load(TEST_DIR / (rid + '.npz'), allow_pickle=False)
        meta = json.loads(str(z['meta']))
        ev = z['evaluated'].astype(bool)
        c, m_in, m_re, m_st = pops(z, meta)
        k_coast = np.where(c == 1, kc['1'], np.where(c == 2, kc['2'], np.where(c == 3, kc['3'], np.where(m_re, k_re, 1.0))))
        k_flag2 = np.where(m_in, k_in, np.where(m_re, k_re, 1.0))
        cF = np.asarray(z['cF0'], float)
        runs.append(dict(run=rid, desired=float(z['des'][0]), meta=meta, k=z['k'], ev=ev, v0=z['v0'], ph=z['phase'], vbar=z['vbar'],
                         idx55=z['idx55'].astype(np.int64), clear_raw=z['clear'], clear1=L.clean_clear(z['clear']), masks=(ev,),
                         crit={'F0': cF, 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float),
                               'F0coast': cF * k_coast[:, None], 'F0flag2': cF * k_flag2[:, None]},
                         sel={}, late={}))
        for c_ in (1, 2, 3): npop['c%d' % c_] += int((ev & (c == c_)).sum())
        npop['reacq'] += int((ev & m_re).sum()); npop['steady'] += int((ev & m_st).sum())
    return runs, npop


runs, npop = load_test()
NR = len(runs)
NAMES = ['F0', 'E', 'N', 'F0coast', 'F0flag2']
G = TS.gridless(runs, NAMES)
pt = TS.rr_gl(G, 'F0', 'E', NAMES[2:], pop=0)
st = CC.GLStat(CC.prep(G, NAMES, 0), [('RR', 'N'), ('RR', 'F0coast'), ('RRdiff', 'N', 'F0coast'), ('RR', 'F0flag2'),
                                      ('RRdiff', 'N', 'F0flag2')])
f = st(np.ones((1, NR)))[0]
for x, y in ((f[0], pt['RR']['N']), (f[1], pt['RR']['F0coast']), (f[3], pt['RR']['F0flag2'])):
    if not ((np.isnan(x) and np.isnan(y)) or abs(x - y) <= 1e-12 * max(abs(x), abs(y), 1.)):
        raise RuntimeError('gl_fast differs from the library at the full sample: %s %s' % (f, pt['RR']))
W = CC.counts(NR, args.nboot, CC.SEED_BOOT)
b = st(W)
ci = lambda j: [float(x) for x in CC.interval(b[:, j], f[j], 0.95)['ci_level']]
d_ci = ci(2)
p_F = float((1 + np.sum(~(b[:, 2] > TIE))) / (b.shape[0] + 1))
passes = bool(d_ci[0] > 0)
within = bool(-EQUIV < d_ci[0] and d_ci[1] < EQUIV)
vals = {'DRF.n_runs': NR, 'DRF.n_fit_runs': len(fit_ids)}
for S, nm in (('1', '1'), ('2', '2'), ('3', '3'), ('re', 're'), ('st', 'st'), ('in', 'in')):
    vals['DRF.M_' + nm] = M[S]; vals['DRF.n_fit_rows.' + nm] = int(rat[S].size)
for c_ in ('1', '2', '3'):
    vals['DRF.k_' + c_] = float(kc[c_]); vals['DRF.k_%s.fallback' % c_] = fb[c_]
vals.update({'DRF.k_re': float(k_re), 'DRF.k_in': float(k_in),
             'DRF.n_dec.c1': npop['c1'], 'DRF.n_dec.c2': npop['c2'], 'DRF.n_dec.c3': npop['c3'], 'DRF.n_dec.reacq': npop['reacq'],
             'DRF.n_dec.steady': npop['steady'],
             'DRF.RR_N': float(f[0]), 'DRF.RR_N.ci': ci(0), 'DRF.RR_coast': float(f[1]), 'DRF.RR_coast.ci': ci(1),
             'DRF.delta': float(f[2]), 'DRF.delta.ci': d_ci, 'DRF.delta.p': p_F, 'DRF.passes': passes, 'DRF.within_equiv': within,
             'DRF.status': 'passed (amendment)' if passes else 'failed (amendment)',
             'DRF.RR_flag2': float(f[3]), 'DRF.RR_flag2.ci': ci(3), 'DRF.delta_flag2': float(f[4]), 'DRF.delta_flag2.ci': ci(4)})
doc = dict(code='dr_flag_v02.py', amendment='AMENDMENT_13 sec. 3 (v02, coast count)', test_old=args.test_old, fit_runs=fit_ids,
           test_runs=test_ids, draw='optA_lib_v02.boot_counts(%d, %d, %d)' % (NR, args.nboot, CC.SEED_BOOT),
           interval='plain 95% percentile, no calibration', min_rows_fallback=MIN_ROWS,
           n_delta_le_tie_or_nan=int(np.sum(~(b[:, 2] > TIE))), n_delta_abs_le_tie=int(np.sum(np.abs(b[:, 2]) <= TIE)), n_delta_nan=int(np.sum(~np.isfinite(b[:, 2]))),
           lock=str(LOCK) if LOCK.is_file() else None)
if not args.test_old:
    dr2 = json.loads((DRD / 'out_a12' / 'p010' / 'DR2_RESULTS_v01.json').read_text(encoding='utf-8'))['values']
    doc['RR_N_equals_DR2_r'] = bool(vals['DRF.RR_N'] == dr2['DR.r'])
doc['values'] = vals
doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
OUTD.mkdir(parents=True, exist_ok=True)
OUTF.write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
log('WROTE %s: %s' % (OUTF, {k: vals[k] for k in ('DRF.k_1', 'DRF.k_2', 'DRF.k_3', 'DRF.k_re', 'DRF.RR_N', 'DRF.RR_coast', 'DRF.delta',
                                                  'DRF.delta.ci', 'DRF.status', 'DRF.RR_flag2')}))
