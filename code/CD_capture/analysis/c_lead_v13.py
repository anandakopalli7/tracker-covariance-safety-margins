"""Revision v13, package C, lead braking (AMENDMENT_10_v13 sec. 5.3, 5.5): hypotheses H0-H5 in their fixed sequence on the 105
fresh lead-braking runs, 3 s commitment, all evaluated decisions, gridless step frontier (sec. 2.3) except H4 (grid frontier).

Sources (sec. 2.1-2.2; package B's frozen library trk_score_v01, read-only): F0 (class average of record), E (true-state error),
N (tracker covariance of record), CK3 (braking prediction, 3 m/s^2), NA, A1 (= AM), Q, TG (r0 = 2 m/s; descriptive);
E5 = add_oracle(F0, m = 1.1029, A = 0.05, u = e5_u(F0, E)); E5p = E5 with u permuted within runs (default_rng(20261915)).
IMM (H3): the frozen B1 tracker's arrays (re-tracked with B's library, P-bar_IMM): F0_IMM, E_IMM, N_IMM on its own room; ceiling
E5_IMM = add_oracle(F0_IMM, m_IMM = median, A_IMM = (q95 - q05) / (2 median) of margin_ratios(N_IMM, F0_IMM), u = e5_u(F0_IMM, E_IMM)).
Intervals: 95% percentile over 20,000 run resamples (default_rng(20261911)), calibrated per sec. 2.6 (cd_common_v13.calibrate_all:
double bootstrap 2,000 x 1,000, seeds 20261912/20261913, check seeds 20261914 and 20261920). One-sided at 0.025 = the lower end of
the two-sided interval at the calibrated level.
  H0  R_gl lower end > 0, and D_gl(E, F0) > 0 in >= 97.5% of resamples
  H1  lower ends of RR_gl(E5) and RR_gl(E5) - RR_gl(E5p) > 0
  H2  RR_gl(N) interval inside (-0.05, 0.05)
  H3  r = RR_gl(N_IMM), c = RR_gl(E5_IMM) on the IMM's own room: (a) recovers if r's lower end > 0; else (b) uninformative variation if
      c's lower end > delta; else (c) amplitude-limited if c's interval is inside (-delta, delta); else (d) inconclusive. Flag
      'barely varies' if >= 95% of binding rows are within 5% of the median ratio. Passes with (a), (b) or (c). Under (a) r / c.
  H4  per-phase schedule chosen on the 35 old evaluation runs (tracker-estimated phase, thresholds 0.5 m/s and -1.0 m/s^2) and
      transferred once (sec. 5.5): record basis sum(F_F0 - F_ps->C) / sum(F_F0 - F_E) lower end > 0.5 (grid frontiers, fresh levels);
      like-for-like basis sum(F_1->C - F_ps->C) / sum(F_F0 - F_E) beside it; sensitivities: truth phase, thresholds -0.5 and -2.0.
  H5  RR_gl(CK3) lower end > 0.5
'Confirmed' = it and every earlier hypothesis passed; later ones are still computed and labelled 'not confirmatory'.
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\c_lead_v13.py [--test-old] [--nboot N] [--no-calib] [--outer N]
--test-old runs every step on the OLD 35 evaluation runs (exploratory data of record) as stand-in 'fresh' runs, to test the code; it
never reads a fresh run and writes out/TESTOLD_*.json.
"""
import argparse, json, pathlib, sys, time
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cd_common_v13 as CC               # noqa: E402
import trk_env_v01 as env                # noqa: E402
env.setup()
import trk_score_v01 as TS               # noqa: E402
L = CC.L; C11 = CC.C11; A9 = CC.A9

ap = argparse.ArgumentParser()
ap.add_argument('--test-old', action='store_true'); ap.add_argument('--nboot', type=int, default=CC.NBOOT)
ap.add_argument('--no-calib', action='store_true'); ap.add_argument('--outer', type=int, default=CC.N_OUTER)
ap.add_argument('--calib', choices=('local', 'export', 'import'), default='local')
args = ap.parse_args()
CC.N_OUTER = args.outer; CC.CALIB_MODE = args.calib
gate = CC.require_lock2(args.test_old)
if args.test_old: CC.CALIB_DIR = CC.OUT / 'calib_testold'           # test jobs never mix with the real ones
t00 = time.time()
log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)
OUTF = CC.OUT / (('TESTOLD_' if args.test_old else '') + 'C_LEAD_H0_H5_v13' + ('_PENDING_CALIB' if args.calib == 'export' else '') + '.json')
if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)
D = CC.DELTA

# ------------------------------------------------------------------------------------------------ runs
design = CC.load_old_lead()                                      # H4 design set (35 old evaluation runs)
if args.test_old:
    runs = CC.load_old_lead()
    for r in runs: r['masks'] = r['masks_est']
    run_ids = [r['run'] for r in runs]
else:
    run_ids = CC.c_run_ids('lead_braking')
    runs = CC.load_variant(run_ids, 'CV0')
    assert all(r['meta'].get('family') == 'lead_braking' for r in runs)
NR = len(runs)
log('runs %d (%s)' % (NR, 'TEST: old evaluation runs' if args.test_old else 'fresh C lead braking'))
u, uinfo = TS.e5_u(runs, 'F0', 'E')
TS.add_oracle(runs, 'E5', 'F0', CC.RATIO, 0.05, u)
TS.add_oracle(runs, 'E5p', 'F0', CC.RATIO, 0.05, TS.permute_u(runs, u))
MAIN = ['F0', 'E', 'N', 'E5', 'E5p', 'CK3']
DESC = ['NA', 'A1', 'Q', 'TG']
G = TS.gridless(runs, MAIN + DESC)
log('gridless events built')
W = CC.counts(NR, args.nboot, CC.SEED_BOOT)
Wfull = np.ones((1, NR))
doc = dict(calib_mode=args.calib, code='c_lead_v13.py', amendment='AMENDMENT_10_v13 sec. 5.3, 5.5', gate=gate, runs=run_ids, n_runs=NR, e5_u=uinfo,
           draw='default_rng(%d), %d run resamples' % (CC.SEED_BOOT, args.nboot), delta=D, test_old=args.test_old)

# point estimates with the library of record (B's rr_gl), resamples with gl_fast (identical; test_gl_fast_v13.py)
pt = TS.rr_gl(G, 'F0', 'E', MAIN[2:] + DESC, pop=0)
P1 = CC.prep(G, MAIN, 0)
chk = CC.evaluate(P1, Wfull)
assert chk['denE'][0] == pt['denE'] and all(chk['D'][a][0] == pt['D'][a] for a in MAIN[2:]), 'gl_fast differs from the library'
log('gl_fast compiled and identical to the library at the full sample')
B1 = CC.evaluate(P1, W)
log('main resamples done (%d)' % W.shape[0])


stats_main = CC.GLStat(P1, [('R',), ('RR', 'E5'), ('RRdiff', 'E5', 'E5p'), ('RR', 'N'), ('RR', 'CK3')])


SN = ['R_gl', 'RR_E5', 'RR_E5_minus_E5p', 'RR_N', 'RR_CK3']
full_main = stats_main(Wfull)[0]
boot_main = stats_main(W)
cal = {} if args.no_calib else CC.calibrate_all(stats_main, NR, full_main, SN, log=log, label='lead_main')
lev = {nm: (cal[nm]['level'] if nm in cal else 0.95) for nm in SN}
S = {nm: CC.interval(boot_main[:, j], full_main[j], lev[nm]) for j, nm in enumerate(SN)}
doc['calibration_main'] = cal
doc['main'] = S
doc['room'] = dict(R_pp=pt['R_pp'], R_deceq=pt['R_deceq'], n=pt['n'], share_resamples_denE_gt0=float(np.mean(B1['denE'] > 0)),
                   R_deceq_ci=L.pct(L.dec_eq(B1['denE'], B1['n'])))

# descriptive shares (sec. 5.7): RR_gl of NA, AM, Q, TG (percentile 95%, not calibrated)
P2 = CC.prep(G, ['F0', 'E'] + DESC, 0); B2 = CC.evaluate(P2, W)
doc['descriptive_RR_gl'] = {a: L.summ(CC.rat(B2['D'][a], B2['denE']), pt['RR'][a]) for a in DESC}
doc['descriptive_D_deceq'] = {a: dict(point=pt['D_deceq'][a], ci=L.pct(L.dec_eq((B1 if a in MAIN else B2)['D'][a], (B1 if a in MAIN else B2)['n']))) for a in MAIN[2:] + DESC}
log('main and descriptive done')

# ------------------------------------------------------------------------------------------------ H3 (IMM)
h3 = dict(status='not run')
imm_ok = (not args.test_old) or all((CC.ARR / 'B1' / (rid + '.npz')).is_file() for rid in run_ids)
if imm_ok:
    ri = CC.load_variant(run_ids, 'B1', test_old=args.test_old)
    rs = TS.ratio_summary(TS.margin_ratios(ri, 'N', 'F0'))
    ui, uii = TS.e5_u(ri, 'F0', 'E')
    TS.add_oracle(ri, 'E5x', 'F0', rs['median'], rs['A'], ui)
    Gi = TS.gridless(ri, ['F0', 'E', 'N', 'E5x'])
    pti = TS.rr_gl(Gi, 'F0', 'E', ['N', 'E5x'], pop=0)
    Pi = CC.prep(Gi, ['F0', 'E', 'N', 'E5x'], 0)

    stats_imm = CC.GLStat(Pi, [('RR', 'N'), ('RR', 'E5x'), ('R',)])
    fi = stats_imm(Wfull)[0]; bi = stats_imm(W)
    assert fi[0] == pti['RR']['N'] and fi[1] == pti['RR']['E5x']
    cali = {} if args.no_calib else CC.calibrate_all(CC.GLStat(Pi, [('RR', 'N'), ('RR', 'E5x')]), NR, fi[:2], ['r', 'c'], log=log, label='lead_imm')
    li = {nm: (cali[nm]['level'] if nm in cali else 0.95) for nm in ('r', 'c')}
    Sr = CC.interval(bi[:, 0], fi[0], li['r']); Sc = CC.interval(bi[:, 1], fi[1], li['c'])
    rlo = Sr['ci_level'][0]; clo, chi = Sc['ci_level']
    if rlo > 0: cls = 'recovers'
    elif clo > D: cls = 'uninformative variation'
    elif clo > -D and chi < D: cls = 'amplitude-limited'
    else: cls = 'inconclusive'
    with np.errstate(divide='ignore', invalid='ignore'):
        eff = CC.interval(bi[:, 0] / bi[:, 1], fi[0] / fi[1], li['r'])
    h3 = dict(status='run', classification=cls, barely_varies=rs['barely_varies'], ratio_summary=rs, e5_u=uii, r=Sr, c=Sc,
              efficiency_r_over_c=eff if cls == 'recovers' else None, room_IMM=dict(R_pp=pti['R_pp'], R_deceq=pti['R_deceq'],
              ci=L.pct(bi[:, 2])), calibration=cali, passes=cls in ('recovers', 'uninformative variation', 'amplitude-limited'))
    log('H3 done: %s' % cls)
doc['H3'] = h3

# ------------------------------------------------------------------------------------------------ H4 (sec. 5.5)
PHPOP = [2, 3, 4]


from c_lead_choice_v13 import single_choice, triple_choice   # noqa: E402  (v12 functions, verbatim)


def phase_tables(rs_, masks_fn):
    for r in rs_: r['masks_h4'] = masks_fn(r)
    X = C11.tables(rs_, ('W1',), ['F0', 'E'], masks_key='masks_h4')
    return X['F0'], X['E']


def est_masks(thr):
    def f(r):
        eph = TS.est_phase(r['lead']['vhat'], r['lead']['ahat_long'], r['lead']['lead_found'], thr) if 'lead' in r else \
            TS.est_phase(r['z']['vhat'], r['z']['ahat_long'], r['z']['lead_found'], thr)
        return CC.masks_tracker_phase(r['ev'], r['v0'], eph)
    return f


def truth_masks(r):
    return CC.masks_tracker_phase(r['ev'], r['v0'], np.where(r['ph'] <= 2, r['ph'], 9))


def h4_once(mfn):
    dF0, dE = phase_tables(design, mfn)
    wd = np.ones(len(design))
    Tall = np.tensordot(wd, dF0[:, :, 0, :], axes=(0, 0)); TEd = np.tensordot(wd, dE[:, :, 0, :], axes=(0, 0))
    cur = L.curves_w({'F0': Tall, 'E': TEd}, 0)
    levd = L.levels_of(cur['F0'][0], cur['E'][0], cur['F0'][0][0])
    tri = triple_choice([np.tensordot(wd, dF0[:, :, pi, :], axes=(0, 0)) for pi in PHPOP], levd)
    one = single_choice(Tall, levd)
    fF0, fE = phase_tables(runs, mfn)
    st = CC.H4Stat(fF0, fE, tri, one)
    share = st.share
    full = share(np.ones(NR))
    bt = np.array([share(W[b]) for b in range(W.shape[0])])
    return full, bt, st, dict(design_levels=[float(levd[0]), float(levd[-1])], triples_with_choice=int((tri[:, 0] >= 0).sum()))


f4, b4, st4, info4 = h4_once(est_masks(-1.0))
cal4 = {} if args.no_calib else CC.calibrate_all(st4, NR, f4[:1], ['share_record'], log=log, label='lead_h4')
l4 = cal4['share_record']['level'] if cal4 else 0.95
h4 = dict(record_basis=CC.interval(b4[:, 0], f4[0], l4), like_for_like=L.summ(b4[:, 1], f4[1]),
          single_scale=L.summ(b4[:, 2], f4[2]), calibration=cal4, design=info4, sensitivities={})
for nm, mf in (('truth_phase', truth_masks), ('thr_-0.5', est_masks(-0.5)), ('thr_-2.0', est_masks(-2.0))):
    fs, bs, _, _ = h4_once(mf)
    h4['sensitivities'][nm] = dict(record_basis=L.summ(bs[:, 0], fs[0]), like_for_like=L.summ(bs[:, 1], fs[1]),
                                   single_scale=L.summ(bs[:, 2], fs[2]))
doc['H4'] = h4
log('H4 done')

# ------------------------------------------------------------------------------------------------ the sequence
res = {}
res['H0'] = bool(S['R_gl']['ci_level'][0] > 0 and doc['room']['share_resamples_denE_gt0'] >= 0.975)
res['H1'] = bool(S['RR_E5']['ci_level'][0] > 0 and S['RR_E5_minus_E5p']['ci_level'][0] > 0)
res['H2'] = bool(S['RR_N']['ci_level'][0] > -D and S['RR_N']['ci_level'][1] < D)
res['H3'] = bool(h3.get('passes', False))
res['H4'] = bool(h4['record_basis']['ci_level'][0] > 0.5)
res['H5'] = bool(S['RR_CK3']['ci_level'][0] > 0.5)
seq = {}; ok = True
for h in ('H0', 'H1', 'H2', 'H3', 'H4', 'H5'):
    ok = ok and res[h]
    seq[h] = dict(passes=res[h], confirmed=ok, label='confirmatory' if ok else 'not confirmatory')
doc['sequence'] = seq
doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
doc['code_sha256'] = {f: CC.sha(CC.HERE / f) for f in ('c_lead_v13.py', 'cd_common_v13.py', 'gl_fast_v13.py', 'c_lead_choice_v13.py')}
CC.write_once(OUTF, doc)
log('written %s; sequence %s' % (OUTF.name, {h: v['passes'] for h, v in seq.items()}))
