"""Revision v13, package C, cut-in (AMENDMENT_10_v13 sec. 2.5, 5.4): K0-K2 in their own fixed sequence on the 105 fresh cut-in runs,
event window, 3 s commitment, gridless step frontier; descriptive outputs by track-age stratum and by second relative to t_c.

Event, window and track age: as package B's B9 (work/B_retrack/code/b9_cutin_v01.py, copied, same expressions): t_c = the first truth
tick at which the primary actor is ahead of the ego (along > 0) and its centre lies within 1.75 m (Lock 2 threshold) of the ego's lane
centre (the ego's median lateral route coordinate over the run); window: evaluated decisions with t - t_c in [-1, +4] s; track age =
'now' minus the birth (first detector frame) of the track matched to the cutting vehicle (gc.match_many; several -> youngest);
strata < 1 s, 1-4 s, >= 4 s, 'untracked'. Runs without an event are listed and left out of the event population.
  K0  lower end of R_gl in the window > 0, and den0 >= 10 decision-equivalents (den0 = D_gl(O, F0), O the perfect oracle; point)
  K1  RR_gl(N) in the window: interval inside (-0.05, 0.05)
  K2  young-track population (window and < 1 s): not evaluable if R_gl there is below 10 decision-equivalents (point); else classified as
      H3 with N and its ceiling E5_N: m_N, A_N from margin_ratios(N, F0) over the young-track population's decisions; u = e5_u(F0, E) over
      the run set's evaluated decisions. (a) recovers if r's lower end > 0; else (b) uninformative variation if c's lower end > delta;
      else (c) amplitude-limited if c's interval is inside (-delta, delta); else (d) inconclusive; flag 'barely varies'.
Intervals: 20,000 run resamples (default_rng(20261911)) over the 105 cut-in runs (event-less runs included with empty windows),
calibrated per sec. 2.6. 'Confirmed' = it and every earlier one passed. No adjustment across families (stated).
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\c_cutin_v13.py [--test-old] [--nboot N] [--no-calib] [--outer N]
--test-old: the 20 cut-in TUNING runs of record (exploratory; stored gateR arrays) stand in for the fresh runs (code test only).
"""
import argparse, csv, json, math, pathlib, sys, time
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cd_common_v13 as CC               # noqa: E402
import trk_env_v01 as env                # noqa: E402
env.setup()
import trk_score_v01 as TS               # noqa: E402
import trk_arrays_v01 as TA              # noqa: E402
L = CC.L

ap = argparse.ArgumentParser()
ap.add_argument('--test-old', action='store_true'); ap.add_argument('--nboot', type=int, default=CC.NBOOT)
ap.add_argument('--no-calib', action='store_true'); ap.add_argument('--outer', type=int, default=CC.N_OUTER)
ap.add_argument('--calib', choices=('local', 'export', 'import'), default='local')
args = ap.parse_args(); CC.N_OUTER = args.outer; CC.CALIB_MODE = args.calib
gate = CC.require_lock2(args.test_old)
if args.test_old: CC.CALIB_DIR = CC.OUT / 'calib_testold'           # test jobs never mix with the real ones
t00 = time.time()
log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)
OUTF = CC.OUT / (('TESTOLD_' if args.test_old else '') + 'C_CUTIN_K0_K2_v13' + ('_PENDING_CALIB' if args.calib == 'export' else '') + '.json')
if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)
D = CC.DELTA; LAT = 1.75; WIN = (-1.0, 4.0); DT = 0.05
# LAT = 1.75 m: B9 found events in 20 of 20 tuning runs at 1.75 m (work/B_retrack/out/b9/B9_EVENT_COUNT_lat1p75_v01.json), so the
# threshold of A10 sec. 2.5 stands; Lock 2 records it.


def event_tick(T):
    """b9_cutin_v01.event_tick (same lines)."""
    ks = sorted(T); kc = None
    lat_e = np.array([-math.sin(T[k]['ego'][2]) * T[k]['ego'][0] + math.cos(T[k]['ego'][2]) * T[k]['ego'][1] for k in ks])
    lane = float(np.median(lat_e))
    for k in ks:
        tr = T[k]; tid = tr['target_id']
        ex, ey, yaw = tr['ego']
        if tid is None or tid not in tr['actors']: continue
        a = tr['actors'][tid]
        along = math.cos(yaw) * (a[0] - ex) + math.sin(yaw) * (a[1] - ey)
        across = -math.sin(yaw) * a[0] + math.cos(yaw) * a[1] - lane
        if along > 0 and abs(across) <= LAT:
            kc = k; break
    return kc, float(np.ptp(lat_e)) if lat_e.size else float('nan')


def event_info(rd, cap, ks_ref):
    """t_c, relative time and track-age stratum per decision (b9_cutin_v01.main, same lines)."""
    Lr = TA.load_capture(rd, cap); T = Lr['T']; book = Lr['book']
    kc, spread = event_tick(T)
    decs = list(TA.gc.decisions(cap)); ks = np.array([k for k, _ in decs])
    assert np.array_equal(ks, ks_ref)
    rel = (ks - kc) * DT if kc is not None else np.full(ks.size, np.nan)
    age = np.full(ks.size, np.nan)
    for di, (k, dec) in enumerate(decs):
        tr = T.get(k)
        m, prim, order = TA.gc.match_many(dec['actors'], dec['now'], tr)
        if prim is None: continue
        best = None
        for a, aid in zip(dec['actors'], m):
            if aid == prim:
                b = book.birth.get(int(a['track_id']))
                if b is None: continue
                ag = dec['now'] - book.det_time[b]
                best = ag if best is None else min(best, ag)
        if best is not None: age[di] = best
    stratum = np.full(ks.size, 'untracked', dtype='U9')
    stratum[np.isfinite(age) & (age < 1.)] = '<1s'; stratum[np.isfinite(age) & (age >= 1.) & (age < 4.)] = '1-4s'
    stratum[np.isfinite(age) & (age >= 4.)] = '>=4s'
    return kc, spread, rel, stratum


# ------------------------------------------------------------------------------------------------ runs
if args.test_old:
    P = pathlib.Path(r'<library folder>')
    rows = [r for r in csv.DictReader(open(P / '09_redesign' / 'm4_perception_model' / 'run_index_m4_v02.csv', encoding='utf-8'))
            if r['use'] == '1' and r['set'] == 'tune' and r['family'] == 'cutin']
    rows.sort(key=lambda r: r['archive']); assert len(rows) == 20
    STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
    srcs = [(r['archive'], pathlib.Path(r['cap']).parents[3], pathlib.Path(r['cap']), np.load(STORED / (r['archive'] + '.npz'), allow_pickle=False)) for r in rows]
else:
    ids = CC.c_run_ids('cutin')
    srcs = []
    for rid in ids:
        z = np.load(CC.ARR / 'CV0' / (rid + '.npz'), allow_pickle=False)
        rd = CC.CD / 'runs' / rid / rid; cap = next(p for p in (rd / 'capture').iterdir() if p.is_dir())
        assert json.loads(str(z['meta']))['family'] == 'cutin', rid
        srcs.append((rid, rd, cap, z))
SECS = [(-1, 0), (0, 1), (1, 2), (2, 3), (3, 4)]
runs = []; facts = []
for rid, rd, cap, z in srcs:
    ev = z['evaluated'].astype(bool)
    kc, spread, rel, stratum = event_info(rd, cap, z['k'])
    win = ev & np.isfinite(rel) & (rel >= WIN[0]) & (rel <= WIN[1])
    masks = [win, win & (stratum == '<1s'), win & (stratum == '1-4s'), win & (stratum == '>=4s'), ev, win & (stratum == 'untracked')]
    masks += [win & (rel >= lo) & ((rel < hi) if hi < 4 else (rel <= hi)) for lo, hi in SECS]
    runs.append(dict(run=rid, desired=float(z['des'][0]), idx55=z['idx55'].astype(np.int64), clear1=L.clean_clear(z['clear']), vbar=z['vbar'],
                     ev=ev, sel={}, late={}, masks=tuple(masks), crit={'F0': z['cF0'], 'E': z['cE'], 'N': z['cN']}, win=win, stratum=stratum))
    facts.append(dict(run=rid, event_tick=kc, ego_lateral_spread_m=spread, n_eval=int(ev.sum()), n_window=int(win.sum()),
                      window_strata={s: int((win & (stratum == s)).sum()) for s in ('<1s', '1-4s', '>=4s', 'untracked')}))
NR = len(runs)
POP = dict(window=0, young=1, mid=2, old=3, all_evaluated=4, untracked=5, **{'sec[%d,%d)' % s: 6 + i for i, s in enumerate(SECS)})
log('runs %d; events %d' % (NR, sum(f['event_tick'] is not None for f in facts)))
u, uinfo = TS.e5_u(runs, 'F0', 'E')


def ratios_in(rs_, pop):
    out = []
    for r in rs_:
        m = r['masks'][pop]; cN = r['crit']['N'][m]; cF = r['crit']['F0'][m]
        ok = np.isfinite(cN) & np.isfinite(cF) & (cN > 0) & (cF > 0)
        out.append(np.sqrt(cF[ok] / cN[ok]))
    return np.concatenate(out) if out else np.zeros(0)


rsY = TS.ratio_summary(ratios_in(runs, POP['young']))
if rsY.get('n', 0) > 0:
    TS.add_oracle(runs, 'E5x', 'F0', rsY['median'], rsY['A'], u)
else:
    for r in runs: r['crit']['E5x'] = np.full_like(r['crit']['F0'], np.nan)
NAMES = ['F0', 'E', 'N', 'O', 'E5x']
G = TS.gridless(runs, ['F0', 'E', 'N', 'O', 'E5x'])
W = CC.counts(NR, args.nboot, CC.SEED_BOOT); Wfull = np.ones((1, NR))
doc = dict(calib_mode=args.calib, code='c_cutin_v13.py', amendment='AMENDMENT_10_v13 sec. 2.5, 5.4', gate=gate, lat_m=LAT, window_s=WIN, runs=facts,
           runs_without_event=[f['run'] for f in facts if f['event_tick'] is None], e5_u=uinfo, ratio_young=rsY, test_old=args.test_old,
           draw='default_rng(%d), %d run resamples' % (CC.SEED_BOOT, args.nboot))

# descriptive: every population, point (library) + percentile 95% (gl_fast)
desc = {}
for nm, pi in POP.items():
    p = TS.rr_gl(G, 'F0', 'E', ['N', 'O'], pop=pi)
    Pp = CC.prep(G, ['F0', 'E', 'N', 'O'], pi); b = CC.evaluate(Pp, W)
    desc[nm] = dict(n=p['n'], R_pp=L.summ(b['denE'] / L.NLEV, p['R_pp']), R_deceq=dict(point=p['R_deceq'], ci=L.pct(L.dec_eq(b['denE'], b['n']))),
                    den0_deceq=dict(point=p['D_deceq']['O'], ci=L.pct(L.dec_eq(b['D']['O'], b['n']))),
                    RR_N=L.summ(CC.rat(b['D']['N'], b['denE']), p['RR']['N']), ratio=TS.ratio_summary(ratios_in(runs, pi)))
doc['descriptive'] = desc
log('descriptive done')

# K0, K1 (window)
Pw = CC.prep(G, ['F0', 'E', 'N', 'O'], POP['window'])


stats_win = CC.GLStat(Pw, [('R',), ('RR', 'N')])


fw = stats_win(Wfull)[0]; bw = stats_win(W)
calw = {} if args.no_calib else CC.calibrate_all(stats_win, NR, fw, ['R_gl', 'RR_N'], log=log, label='cutin_window')
lw = {nm: (calw[nm]['level'] if nm in calw else 0.95) for nm in ('R_gl', 'RR_N')}
K0R = CC.interval(bw[:, 0], fw[0], lw['R_gl']); K1 = CC.interval(bw[:, 1], fw[1], lw['RR_N'])
den0 = desc['window']['den0_deceq']['point']
k0 = bool(K0R['ci_level'][0] > 0 and np.isfinite(den0) and den0 >= L.MIN_DEC_EQ)
k1 = bool(K1['ci_level'][0] > -D and K1['ci_level'][1] < D)
doc['K0'] = dict(R_gl=K0R, den0_deceq=den0, passes=k0, calibration=calw)
doc['K1'] = dict(RR_N=K1, passes=k1)

# K2 (young-track population)
ry = desc['young']['R_deceq']['point']
if not (np.isfinite(ry) and ry >= L.MIN_DEC_EQ):
    ry = ry if np.isfinite(ry) else 0.   # no young-track decision: no room there
    doc['K2'] = dict(status='not evaluable', reason='R_gl in the young-track population is %.3f decision-equivalents (< 10): too few young-track '
                     'decisions carry room to test it' % ry, passes=False)
else:
    Py = CC.prep(G, ['F0', 'E', 'N', 'E5x'], POP['young'])

    stats_y = CC.GLStat(Py, [('RR', 'N'), ('RR', 'E5x')])
    fy = stats_y(Wfull)[0]; by = stats_y(W)
    caly = {} if args.no_calib else CC.calibrate_all(stats_y, NR, fy, ['r', 'c'], log=log, label='cutin_young')
    ly = {nm: (caly[nm]['level'] if nm in caly else 0.95) for nm in ('r', 'c')}
    Sr = CC.interval(by[:, 0], fy[0], ly['r']); Sc = CC.interval(by[:, 1], fy[1], ly['c'])
    if Sr['ci_level'][0] > 0: cls = 'recovers'
    elif Sc['ci_level'][0] > D: cls = 'uninformative variation'
    elif Sc['ci_level'][0] > -D and Sc['ci_level'][1] < D: cls = 'amplitude-limited'
    else: cls = 'inconclusive'
    with np.errstate(divide='ignore', invalid='ignore'):           # efficiency r/c under (a), as H3 (A10 sec. 5.3 H3; added 20 Nov 02:50)
        eff = CC.interval(by[:, 0] / by[:, 1], fy[0] / fy[1], ly['r']) if cls == 'recovers' else None
    doc['K2'] = dict(status='evaluated', classification=cls, barely_varies=rsY.get('barely_varies'), r=Sr, c=Sc, calibration=caly,
                     efficiency_r_over_c=eff, passes=cls in ('recovers', 'uninformative variation', 'amplitude-limited'))
seq = {}; ok = True
for h in ('K0', 'K1', 'K2'):
    ok = ok and doc[h]['passes']
    seq[h] = dict(passes=doc[h]['passes'], confirmed=ok, label='confirmatory' if ok else 'not confirmatory')
doc['sequence'] = seq
doc['note_K0'] = 'If K0 fails: no measurable room at the cut-in event; nothing is tested there (A10 sec. 9).'
doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
doc['code_sha256'] = {f: CC.sha(CC.HERE / f) for f in ('c_cutin_v13.py', 'cd_common_v13.py', 'gl_fast_v13.py')}
CC.write_once(OUTF, doc)
log('written %s; sequence %s' % (OUTF.name, {h: v['passes'] for h, v in seq.items()}))
