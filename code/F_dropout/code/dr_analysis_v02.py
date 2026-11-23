r"""Revision v13, AMENDMENT_12 sec. 3a.3: DR0-DR2 at p = 0.10 on the NEW lead-braking runs, with the Holm p-value of DR2's r.
New file, 22 Nov 2026 (Claude Opus 5.5, session F): a copy of dr_analysis_v01.py (frozen in FREEZE_DR; A11 sec. 6c.6-6c.7) with
these changes only: arrays, masks, P-bar and calibration from F_dropout\out_a12\<ptag>\ (dr_extract_v02.py); the run set = the new
runs in that folder's DR_MASKS_<ptag>.json ('fresh', ascending); lock LOCK_A12a; the mask check with dr_masks_v03 at p; the added
value DR.p_r = (1 + #{r* <= 0, NaN counted}) / (20,000 + 1) (A12 sec. 3a.3, sec. 4). --test-old reads out_a12\testold_<ptag>\.
Usage: python -I -B -X utf8 dr_analysis_v02.py --p 0.10 [--calib local|export|import] [--test-old] [--outer N] [--no-calib]
"""
import argparse, json, pathlib, sys, time
import numpy as np
sys.dont_write_bytecode = True
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
import dr_extract_v02 as X               # noqa: E402  (lock path, punish)
import dr_masks_v03 as M3                # noqa: E402
L = CC.L

ap = argparse.ArgumentParser()
ap.add_argument('--test-old', action='store_true'); ap.add_argument('--nboot', type=int, default=CC.NBOOT)
ap.add_argument('--no-calib', action='store_true'); ap.add_argument('--outer', type=int, default=CC.N_OUTER)
ap.add_argument('--calib', choices=('local', 'export', 'import'), default='local'); ap.add_argument('--p', type=float, default=0.10)
args = ap.parse_args()
CC.N_OUTER = args.outer; CC.CALIB_MODE = args.calib
BASE = DRD / 'out_a12' / (('testold_' if args.test_old else '') + M3.ptag(args.p))
OUT = BASE
CC.CALIB_DIR = BASE / 'calib'
if not args.test_old and not X.LOCK.is_file():
    raise SystemExit('REFUSED: no LOCK_A12a.txt; no new-run DR value before the lock (AMENDMENT_12 sec. 3a)')
t00 = time.time()
log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)
OUTF = OUT / (('TESTOLD_' if args.test_old else '') + 'DR2_RESULTS_v01' + ('_PENDING_CALIB' if args.calib == 'export' else '') + '.json')
if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)
D = CC.DELTA


def load_dr(run_ids, sub, base):
    """DR arrays (dr_extract_v01.py): crit F0, E, N; masks (all evaluated, in-dropout)."""
    runs = []
    for rid in run_ids:
        z = np.load(base / sub / (rid + '.npz'), allow_pickle=False)
        meta = json.loads(str(z['meta']))
        ev = z['evaluated'].astype(bool); dm = z['dr_masked'].astype(bool); dg = z['dr_gap'].astype(bool)
        crit = {'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float)}
        runs.append(dict(run=rid, desired=float(z['des'][0]), meta=meta, k=z['k'], ev=ev, v0=z['v0'], ph=z['phase'], vbar=z['vbar'],
                         idx55=z['idx55'].astype(np.int64), clear_raw=z['clear'], clear1=L.clean_clear(z['clear']),
                         masks=(ev, ev & dm, ev & (dm | dg)), crit=crit, sel={}, late={}, dr_masked=dm, dr_gap=dg,
                         dr_age=z['dr_age'], dr_frame=z['dr_frame'], lead_found=z['lead_found'].astype(bool),
                         track_id=z['track_id'], z=z))
    return runs


if args.test_old:            # DR-format arrays of OLD lead-braking fit runs (dr_extract_v02.py dr --test-old): exploratory only
    ABASE = BASE
    run_ids = sorted(p.stem for p in (ABASE / 'DR').glob('*.npz') if not p.name.endswith('.partial.npz'))
else:
    ABASE = BASE / 'arrays'
    run_ids = sorted(json.loads((BASE / ('DR_MASKS_%s.json' % M3.ptag(args.p))).read_text(encoding='utf-8'))['fresh'])
runs = load_dr(run_ids, 'DR', ABASE)
rec_runs = load_dr(run_ids, 'DRrec', ABASE)
for a, b in zip(runs, rec_runs):              # same tracker output: only F0 differs (P-bar)
    assert a['run'] == b['run'] and np.array_equal(a['crit']['E'], b['crit']['E'], equal_nan=True) \
        and np.array_equal(a['crit']['N'], b['crit']['N'], equal_nan=True) and np.array_equal(a['ev'], b['ev']), a['run']
NR = len(runs)
log('runs %d (%s)' % (NR, 'TEST: old evaluation runs' if args.test_old else 'fresh lead braking under DR masks'))

rs = TS.ratio_summary(TS.margin_ratios(runs, 'N', 'F0'))
u, uinfo = TS.e5_u(runs, 'F0', 'E')
TS.add_oracle(runs, 'E5x', 'F0', rs['median'], rs['A'], u)
TS.add_oracle(runs, 'E5xp', 'F0', rs['median'], rs['A'], TS.permute_u(runs, u))
MAIN = ['F0', 'E', 'N', 'E5x', 'E5xp']
G = TS.gridless(runs, MAIN)
Grec = TS.gridless(rec_runs, ['F0', 'E', 'N'])          # the same tracker output with the P-bar of record as F0
log('gridless events built')
W = CC.counts(NR, args.nboot, CC.SEED_BOOT)
Wfull = np.ones((1, NR))
doc = dict(calib_mode=args.calib, code='dr_analysis_v02.py', amendment='AMENDMENT_12 sec. 3a.3', runs=run_ids, n_runs=NR, p=args.p,
           lock=(None if args.test_old else str(X.LOCK)), punish_num=X.punish(), masks=str(BASE / ('DR_MASKS_%s.json' % M3.ptag(args.p))),
           draw='default_rng(%d), %d run resamples (optA_lib_v02.boot_counts), runs ascending' % (CC.SEED_BOOT, args.nboot),
           delta=D, test_old=args.test_old, e5_u=uinfo, ratio_summary_N_F0=rs, E5x=dict(m=rs['median'], A=rs['A']))

pt = TS.rr_gl(G, 'F0', 'E', MAIN[2:], pop=0)
P1 = CC.prep(G, MAIN, 0)
chk = CC.evaluate(P1, Wfull)
assert chk['denE'][0] == pt['denE'] and all(chk['D'][a][0] == pt['D'][a] for a in MAIN[2:]), 'gl_fast differs from the library'
log('gl_fast identical to the library at the full sample')
B1 = CC.evaluate(P1, W)
SN = ['R_gl', 'c', 'c_minus_E5xp', 'r']
stats_main = CC.GLStat(P1, [('R',), ('RR', 'E5x'), ('RRdiff', 'E5x', 'E5xp'), ('RR', 'N')])
full_main = stats_main(Wfull)[0]
boot_main = stats_main(W)
assert full_main[1] == pt['RR']['E5x'] and full_main[3] == pt['RR']['N']
cal = {} if args.no_calib else CC.calibrate_all(stats_main, NR, full_main, SN, log=log, label='dr_main')
lev = {nm: (cal[nm]['level'] if nm in cal else 0.95) for nm in SN}
S = {nm: CC.interval(boot_main[:, j], full_main[j], lev[nm]) for j, nm in enumerate(SN)}
doc['calibration'] = cal
doc['statistics'] = S
share_pos = float(np.mean(B1['denE'] > 0))
doc['room'] = dict(R_pp=pt['R_pp'], R_deceq=pt['R_deceq'], n=pt['n'], share_resamples_denE_gt0=share_pos,
                   R_deceq_ci=L.pct(L.dec_eq(B1['denE'], B1['n'])))
doc['D_deceq'] = {a: dict(point=pt['D_deceq'][a], ci=L.pct(L.dec_eq(B1['D'][a], B1['n']))) for a in MAIN[2:]}

# ------------------------------------------------------------------------------------------------ the sequence
pending = args.calib == 'export'
lo = lambda nm: S[nm]['ci_level'][0]
dr0 = dict(passes=bool(lo('R_gl') > 0 and share_pos >= 0.975), R_gl_lower=lo('R_gl'), share_resamples_denE_gt0=share_pos)
dr1 = dict(passes=bool(lo('c') > 0 and lo('c_minus_E5xp') > 0), c_lower=lo('c'), diff_lower=lo('c_minus_E5xp'))
rlo = lo('r'); clo, chi = S['c']['ci_level']
if rlo > 0: cls = 'recovers'
elif clo > D: cls = 'uninformative variation'
elif clo > -D and chi < D: cls = 'amplitude-limited'
else: cls = 'inconclusive'
with np.errstate(divide='ignore', invalid='ignore'):
    eff = CC.interval(boot_main[:, 3] / boot_main[:, 1], full_main[3] / full_main[1], lev['r'])
dr2 = dict(classification=cls, passes=cls in ('recovers', 'uninformative variation', 'amplitude-limited'),
           barely_varies=rs['barely_varies'], efficiency_r_over_c=eff if cls == 'recovers' else None)
conf = True
for name, h in (('DR0', dr0), ('DR1', dr1), ('DR2', dr2)):
    h['confirmed'] = bool(conf and h['passes'])
    h['status'] = 'confirmatory' if conf else 'not confirmatory (an earlier hypothesis did not pass)'
    conf = conf and h['passes']
    if pending: h['status'] = 'PENDING calibration (export mode): levels nominal 95% until import'
doc['DR0'], doc['DR1'], doc['DR2'] = dr0, dr1, dr2
log('sequence: DR0 %s, DR1 %s, DR2 %s' % (dr0['passes'], dr1['passes'], cls))

# ------------------------------------------------------------------------------------------------ descriptive (sec. 6c.7)
desc = {}
ev_all = np.concatenate([r['ev'] for r in runs]); dm_all = np.concatenate([r['dr_masked'] for r in runs])
desc['n_evaluated'] = int(ev_all.sum()); desc['n_in_dropout'] = int((ev_all & dm_all).sum())
desc['share_evaluated_in_dropout'] = float((ev_all & dm_all).sum() / max(ev_all.sum(), 1))
ages = np.concatenate([r['dr_age'][r['ev']] for r in runs])
desc['in_dropout_by_age'] = {str(a): int((ages == a).sum()) for a in (1, 2, 3)}
if not args.test_old:
    mk = json.loads((BASE / ('DR_MASKS_%s.json' % M3.ptag(args.p))).read_text(encoding='utf-8'))
    desc['masked_share_frames'] = {k: dict(masked=sum(len(v['masked']) for v in mk[k].values()), frames=sum(v['n'] for v in mk[k].values()))
                                   for k in ('fresh', 'tuning')}
    for k in ('fresh', 'tuning'):
        desc['masked_share_frames'][k]['share'] = desc['masked_share_frames'][k]['masked'] / desc['masked_share_frames'][k]['frames']
if desc['n_in_dropout'] > 0:
    ptd = TS.rr_gl(G, 'F0', 'E', ['N', 'E5x'], pop=1)
    Pd = CC.prep(G, ['F0', 'E', 'N', 'E5x'], 1)
    sd = CC.GLStat(Pd, [('R',), ('RR', 'N'), ('RR', 'E5x')])
    fd = sd(Wfull)[0]; bd = sd(W)
    desc['in_dropout'] = dict(R_pp=ptd['R_pp'], R_deceq=ptd['R_deceq'], n=ptd['n'],
                              R_gl=CC.interval(bd[:, 0], fd[0], 0.95), RR_N=CC.interval(bd[:, 1], fd[1], 0.95),
                              c=CC.interval(bd[:, 2], fd[2], 0.95))
    mr = []
    for r in runs:
        ca = r['crit']['N'][r['ev'] & r['dr_masked']]; cb = r['crit']['F0'][r['ev'] & r['dr_masked']]
        ok = np.isfinite(ca) & np.isfinite(cb) & (ca > 0) & (cb > 0); mr.append(np.sqrt(cb[ok] / ca[ok]))
    desc['ratio_summary_in_dropout'] = TS.ratio_summary(np.concatenate(mr) if mr else np.zeros(0))
gp_all = np.concatenate([r['dr_gap'] for r in runs])
desc['n_gap_row'] = int((ev_all & gp_all).sum())
desc['n_in_dropout_or_gap'] = int((ev_all & (dm_all | gp_all)).sum())
if desc['n_in_dropout_or_gap'] > 0:          # population 2: in-dropout plus the gap row right after each window
    pt2 = TS.rr_gl(G, 'F0', 'E', ['N', 'E5x'], pop=2)
    P2 = CC.prep(G, ['F0', 'E', 'N', 'E5x'], 2)
    s2 = CC.GLStat(P2, [('R',), ('RR', 'N'), ('RR', 'E5x')])
    f2 = s2(Wfull)[0]; b2 = s2(W)
    desc['in_dropout_or_gap'] = dict(R_pp=pt2['R_pp'], R_deceq=pt2['R_deceq'], n=pt2['n'], R_gl=CC.interval(b2[:, 0], f2[0], 0.95),
                                     RR_N=CC.interval(b2[:, 1], f2[1], 0.95), c=CC.interval(b2[:, 2], f2[2], 0.95))
# re-association (coordinator 14:36): evaluated decisions in a window or on its gap row whose lead track id differs from the lead
# track id of the last decision before the window (frame neither masked nor gap, lead found): the lead re-associated as a new track
reas = dict(in_dropout=dict(n=0, lead_found=0, new_track=0, no_pre_lead=0), gap_row=dict(n=0, lead_found=0, new_track=0, no_pre_lead=0))
for r in runs:
    pre = None
    for i in range(r['ev'].size):
        inw = bool(r['dr_masked'][i]); gp = bool(r['dr_gap'][i])
        if not inw and not gp:
            pre = int(r['track_id'][i]) if r['lead_found'][i] else None
            continue
        if not r['ev'][i]: continue
        d = reas['in_dropout' if inw else 'gap_row']; d['n'] += 1
        if r['lead_found'][i]:
            d['lead_found'] += 1
            if pre is None: d['no_pre_lead'] += 1
            elif int(r['track_id'][i]) != pre: d['new_track'] += 1
desc['reassociation'] = reas
if True:
    ptr = TS.rr_gl(Grec, 'F0', 'E', ['N'], pop=0)
    Pr = CC.prep(Grec, ['F0', 'E', 'N'], 0)
    sr = CC.GLStat(Pr, [('R',), ('RR', 'N')])
    fr_ = sr(Wfull)[0]; br = sr(W)
    desc['against_record_pbar'] = dict(R_pp=ptr['R_pp'], RR_N=CC.interval(br[:, 1], fr_[1], 0.95), R_gl=CC.interval(br[:, 0], fr_[0], 0.95))
doc['descriptive'] = desc

# ------------------------------------------------------------------------------------------------ values (the keys the recount writes)
pbf = BASE / 'PBAR_DR_v01.json'
pbd = json.loads(pbf.read_text(encoding='utf-8'))
if args.test_old:
    masks_ok = all(M3.mask(r['meta']['case_id'], r['meta']['n_det_rows'], args.p) == list(r['meta']['masked']) for r in runs)
else:
    masks_ok = all(M3.mask(v['case_id'], v['n'], args.p) == v['masked'] for k in ('fresh', 'tuning') for rid, v in mk[k].items()) \
        and all(list(r['meta']['masked']) == mk['fresh'][r['run']]['masked'] for r in runs)
f = lambda x: float(x)
ci = lambda s: [float(v) for v in s['ci_level']]
vals = {'DR.n_runs': NR, 'DR.n_dec': desc['n_evaluated'], 'DR.n_in_dropout': desc['n_in_dropout'],
        'DR.R_gl': f(full_main[0]), 'DR.R_gl.ci': ci(S['R_gl']), 'DR.R_gl.level': lev['R_gl'], 'DR.R_gl.share_pos': share_pos,
        'DR.R_deceq': f(pt['R_deceq']), 'DR.R_deceq.ci': [float(v) for v in doc['room']['R_deceq_ci']],
        'DR.c': f(full_main[1]), 'DR.c.ci': ci(S['c']), 'DR.c.level': lev['c'],
        'DR.cdiff': f(full_main[2]), 'DR.cdiff.ci': ci(S['c_minus_E5xp']), 'DR.cdiff.level': lev['c_minus_E5xp'],
        'DR.r': f(full_main[3]), 'DR.r.ci': ci(S['r']), 'DR.r.level': lev['r'],
        'DR.eff': (f(full_main[3] / full_main[1]) if cls == 'recovers' else None), 'DR.eff.ci': (ci(eff) if cls == 'recovers' else None),
        'DR.m': rs['median'], 'DR.A': rs['A'], 'DR.within5': rs['share_within_5pct'], 'DR.barely_varies': rs['barely_varies'],
        'DR.DR0.passes': dr0['passes'], 'DR.DR1.passes': dr1['passes'], 'DR.DR2.class': cls, 'DR.DR2.passes': dr2['passes'],
        'DR.dec_in_share': desc['share_evaluated_in_dropout'],
        'DR.rec.RR_N': f(fr_[1]), 'DR.rec.RR_N.ci': ci(desc['against_record_pbar']['RR_N']),
        'DR.pbar.vehicle': pbd['Pbar']['vehicle'], 'DR.pbar.pedestrian': pbd['Pbar']['pedestrian'],
        'DR.pbar.cnt_vehicle': int(pbd['counts']['vehicle']), 'DR.pbar.cnt_pedestrian': int(pbd['counts']['pedestrian']),
        'DR.masks_identical': bool(masks_ok)}
if 'in_dropout' in desc:
    di = desc['in_dropout']
    vals.update({'DR.in.R_gl': f(fd[0]), 'DR.in.R_gl.ci': ci(di['R_gl']), 'DR.in.RR_N': f(fd[1]), 'DR.in.RR_N.ci': ci(di['RR_N']),
                 'DR.in.c': f(fd[2]), 'DR.in.c.ci': ci(di['c']), 'DR.in.within5': desc['ratio_summary_in_dropout'].get('share_within_5pct')})
else:
    vals.update({k: None for k in ('DR.in.R_gl', 'DR.in.R_gl.ci', 'DR.in.RR_N', 'DR.in.RR_N.ci', 'DR.in.c', 'DR.in.c.ci', 'DR.in.within5')})
# output rule without masks (sec. 6c.7): identity check (ii)'s arrays (punish_num = 3, empty masks, P-bar of record)
r3 = []
for rid in run_ids:
    z = np.load(ABASE / 'ID3' / (rid + '.npz'), allow_pickle=False)
    ev3 = z['evaluated'].astype(bool)
    r3.append(dict(run=rid, desired=float(z['des'][0]), k=z['k'], ev=ev3, v0=z['v0'], ph=z['phase'], vbar=z['vbar'],
                   idx55=z['idx55'].astype(np.int64), clear_raw=z['clear'], clear1=L.clean_clear(z['clear']), masks=(ev3,), sel={}, late={},
                   crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float)}))
G3 = TS.gridless(r3, ['F0', 'E', 'N'])
pt3 = TS.rr_gl(G3, 'F0', 'E', ['N'], pop=0)
s3 = CC.GLStat(CC.prep(G3, ['F0', 'E', 'N'], 0), [('R',), ('RR', 'N')])
f3 = s3(Wfull)[0]; b3 = s3(W)
desc['output_rule_without_masks'] = dict(R_pp=pt3['R_pp'], R_deceq=pt3['R_deceq'], R_gl=CC.interval(b3[:, 0], f3[0], 0.95),
                                         RR_N=CC.interval(b3[:, 1], f3[1], 0.95))
vals.update({'DR.ref3.R_gl': f(f3[0]), 'DR.ref3.R_gl.ci': ci(desc['output_rule_without_masks']['R_gl']),
             'DR.ref3.RR_N': f(f3[1]), 'DR.ref3.RR_N.ci': ci(desc['output_rule_without_masks']['RR_N'])})
vals['DR.n_gap_row'] = desc['n_gap_row']
vals['DR.D_N_deceq'] = f(doc['D_deceq']['N']['point']); vals['DR.D_N_deceq.ci'] = [float(v) for v in doc['D_deceq']['N']['ci']]
if args.test_old:
    vals['DR.masked_share'] = float(sum(len(r['meta']['masked']) for r in runs) / sum(r['meta']['n_det_rows'] for r in runs))
else:
    vals['DR.masked_share'] = float(desc['masked_share_frames']['fresh']['share'])
if 'in_dropout_or_gap' in desc:
    dg_ = desc['in_dropout_or_gap']
    vals.update({'DR.ig.R_gl': f(f2[0]), 'DR.ig.R_gl.ci': ci(dg_['R_gl']), 'DR.ig.RR_N': f(f2[1]), 'DR.ig.RR_N.ci': ci(dg_['RR_N']),
                 'DR.ig.c': f(f2[2]), 'DR.ig.c.ci': ci(dg_['c'])})
else:
    vals.update({k: None for k in ('DR.ig.R_gl', 'DR.ig.R_gl.ci', 'DR.ig.RR_N', 'DR.ig.RR_N.ci', 'DR.ig.c', 'DR.ig.c.ci')})
for nm, key in (('in_dropout', 'in'), ('gap_row', 'gap')):
    for fld in ('n', 'lead_found', 'new_track', 'no_pre_lead'):
        vals['DR.reas.%s.%s' % (key, fld)] = reas[nm][fld]
vals['DR.p_r'] = float((1 + np.sum(~(boot_main[:, 3] > 0))) / (boot_main.shape[0] + 1))   # NaN counted as <= 0
doc['values'] = vals
doc['seconds'] = time.time() - t00
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
OUTF.write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
log('WROTE %s' % OUTF)
