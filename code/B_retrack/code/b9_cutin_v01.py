"""v13 package B, B9 (AMENDMENT_10_v13 section 3 row B9; section 2.5): cut-in development on the 20 cut-in TUNING runs, online tracker
of record (stored arrays gateR_rt_v01; logged tracks). New file, 19 Nov 2026 (Claude Opus 5.5). Exploratory. Writes out\\b9\\.

Event time t_c (2.5): the first truth tick at which the cutting vehicle (the scenario's primary actor = evaluation_truth 'target') is
  ahead of the ego and its centre lies within LAT m laterally of the ego's lane centre, route frame. Route frame: x along the route
  yaw (route_yaw_rh), y across; "ahead": x_target - x_ego > 0; lane centre: the ego's lateral route coordinate at that tick (the ego
  keeps its lane; its lateral coordinate varies by 0.33-0.36 m over a run, so the lane centre is its MEDIAN lateral route
  coordinate over the run; fixed before any score was computed). LAT = 1.75 m (2.5 m only if events are
  found in fewer than 18 of 20 runs; decided on the counts alone).
Event window: evaluated decisions with t - t_c in [-1, +4] s (t = decision tick time, both on the 0.05 s truth clock).
Track age: decision time ('now') minus the birth time (first detector frame whose output holds the id) of the track matched to the
  cutting vehicle under the matching rule of record (gc.match_many: nearest true actor within 4 m at 'now'); several matched -> the
  youngest (the rule of record of prim_age); none -> 'untracked'. Strata < 1 s, 1-4 s, >= 4 s.
Outputs: events found, window sizes, strata counts (window and young-track population), the margin ratio N/F0 (sqrt(c_F0 / c_N) at
  rows with finite positive scales) by stratum and by second relative to t_c, room and RR_gl(N) in the event window (gridless, own
  frontier; first 2,000 resamples of default_rng(20261113) over the 20 runs), and den0-style decision-equivalents of the room.
Usage: python -I -B -X utf8 b9_cutin_v01.py <lat_m> count   (event counts only: the threshold decision)
       python -I -B -X utf8 b9_cutin_v01.py <lat_m>         (everything)
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, pathlib, time, math, csv
LIB = pathlib.Path(r'ARS_TRIAL\revision_v13\work\shared\trackers')
sys.path.insert(0, str(LIB))
import trk_env_v01 as env
env.setup()
import numpy as np
import trk_arrays_v01 as TA
import trk_score_v01 as S
L = S.L

P = pathlib.Path(r'<library folder>')
STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
M4 = P / '09_redesign' / 'm4_perception_model'
OUT = pathlib.Path(__file__).resolve().parents[1] / 'out' / 'b9'
LAT = float(sys.argv[1]) if len(sys.argv) > 1 else 1.75
COUNT_ONLY = len(sys.argv) > 2 and sys.argv[2] == 'count'      # the threshold decision uses the event counts alone
NB = 2000
WIN = (-1.0, 4.0)
DT = 0.05


def runs():
    rows = [r for r in csv.DictReader(open(M4 / 'run_index_m4_v02.csv', encoding='utf-8')) if r['use'] == '1' and r['set'] == 'tune'
            and r['family'] == 'cutin']
    rows.sort(key=lambda r: r['archive'])
    assert len(rows) == 20
    return rows


def event_tick(T):
    ks = sorted(T)
    kc = None
    lat_e = np.array([-math.sin(T[k]['ego'][2]) * T[k]['ego'][0] + math.cos(T[k]['ego'][2]) * T[k]['ego'][1] for k in ks])
    lane = float(np.median(lat_e))                      # lane centre: the ego's median lateral route coordinate over the run
    for k in ks:
        tr = T[k]; tid = tr['target_id']
        ex, ey, yaw = tr['ego']
        if tid is None or tid not in tr['actors']:
            continue
        a = tr['actors'][tid]
        along = math.cos(yaw) * (a[0] - ex) + math.sin(yaw) * (a[1] - ey)
        across = -math.sin(yaw) * a[0] + math.cos(yaw) * a[1] - lane
        if along > 0 and abs(across) <= LAT:
            kc = k
            break
    return kc, float(np.ptp(lat_e)) if lat_e.size else float('nan')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t00 = time.time()
    res_runs = []; R = []
    if COUNT_ONLY:
        cnt = []
        for r in runs():
            cap = pathlib.Path(r['cap'])
            kc, spread = event_tick(TA.rt.load_truth(cap, 'route_yaw_rh'))
            cnt.append(dict(run=r['archive'], event_tick=kc, ego_lateral_spread_m=spread))
        found = sum(1 for x in cnt if x['event_tick'] is not None)
        doc = dict(code='b9_cutin_v01.py count', lat_m=LAT, events_found=found, of=len(cnt), runs=cnt,
                   rule_18_of_20=('met' if found >= 18 else 'NOT met: threshold may change once to 2.5 m'), written=time.strftime('%Y-%m-%d %H:%M:%S'))
        (OUT / ('B9_EVENT_COUNT_lat%s_v01.json' % str(LAT).replace('.', 'p'))).write_text(json.dumps(doc, indent=1), encoding='utf-8')
        print(json.dumps({k: doc[k] for k in ('lat_m', 'events_found', 'of', 'rule_18_of_20')}))
        return
    for r in runs():
        cap = pathlib.Path(r['cap']); rd = cap.parents[3]
        Lr = TA.load_capture(rd, cap)
        T = Lr['T']; book = Lr['book']
        kc, ego_lat_spread = event_tick(T)
        z = np.load(STORED / (r['archive'] + '.npz'), allow_pickle=False)
        decs = list(TA.gc.decisions(cap))
        ks = np.array([k for k, _ in decs])
        assert np.array_equal(ks, z['k'])
        ev = z['evaluated'].astype(bool)
        rel = (ks - kc) * DT if kc is not None else np.full(ks.size, np.nan)
        win = ev & np.isfinite(rel) & (rel >= WIN[0]) & (rel <= WIN[1])
        age = np.full(ks.size, np.nan)
        for di, (k, dec) in enumerate(decs):
            tr = T.get(k)
            m, prim, order = TA.gc.match_many(dec['actors'], dec['now'], tr)
            if prim is None:
                continue
            best = None
            for a, aid in zip(dec['actors'], m):
                if aid == prim:
                    b = book.birth.get(int(a['track_id']))
                    if b is None:
                        continue
                    ag = dec['now'] - book.det_time[b]
                    best = ag if best is None else min(best, ag)
            if best is not None:
                age[di] = best
        stratum = np.full(ks.size, 'untracked', dtype='U9')
        stratum[np.isfinite(age) & (age < 1.)] = '<1s'
        stratum[np.isfinite(age) & (age >= 1.) & (age < 4.)] = '1-4s'
        stratum[np.isfinite(age) & (age >= 4.)] = '>=4s'
        res_runs.append(dict(run=r['archive'], event_tick=kc, ego_lateral_spread_m=ego_lat_spread, n_eval=int(ev.sum()),
                             n_window=int(win.sum()), window_strata={s: int((win & (stratum == s)).sum()) for s in ('<1s', '1-4s', '>=4s', 'untracked')}))
        R.append(dict(run=r['archive'], desired=float(z['des'][0]), idx55=z['idx55'].astype(np.int64), clear1=L.clean_clear(z['clear']),
                      vbar=z['vbar'], ev=ev, sel={}, late={},
                      masks=(win, win & (stratum == '<1s'), win & (stratum == '1-4s'), win & (stratum == '>=4s'), ev),
                      crit={'F0': z['cF0'], 'E': z['cE'], 'N': z['cN']}, rel=rel, stratum=stratum, win=win))
        print(r['archive'], 'event k', kc, 'window', int(win.sum()), flush=True)
    found = sum(1 for x in res_runs if x['event_tick'] is not None)
    doc = dict(code='b9_cutin_v01.py', status='exploratory; A10 B9 on the 20 cut-in tuning runs (online tracker of record)', lat_m=LAT,
               events_found=found, runs=res_runs, rule_18_of_20=('met' if found >= 18 else 'NOT met: threshold may change once to 2.5 m'))
    # margin ratio N/F0 by stratum and by second relative to t_c (window decisions)
    def ratios(sel_fn):
        out = []
        for x in R:
            cN = x['crit']['N']; cF = x['crit']['F0']
            for i in np.flatnonzero(sel_fn(x)):
                ok = np.isfinite(cN[i]) & np.isfinite(cF[i]) & (cN[i] > 0) & (cF[i] > 0)
                out.append(np.sqrt(cF[i][ok] / cN[i][ok]))
        return np.concatenate(out) if out else np.zeros(0)
    doc['ratio_by_stratum'] = {s: S.ratio_summary(ratios(lambda x, s=s: x['win'] & (x['stratum'] == s))) for s in ('<1s', '1-4s', '>=4s', 'untracked')}
    doc['ratio_window_all'] = S.ratio_summary(ratios(lambda x: x['win']))
    doc['ratio_by_second'] = {}
    for lo in (-1, 0, 1, 2, 3):
        doc['ratio_by_second']['[%d,%d)' % (lo, lo + 1)] = S.ratio_summary(ratios(lambda x, lo=lo: x['win'] & (x['rel'] >= lo) & (x['rel'] < lo + 1)))
    # room and RR_gl(N): window, young tracks, strata, all evaluated decisions
    G = S.gridless(R, ['F0', 'E', 'N'])
    pops = dict(window=0, young=1, mid=2, old=3, all_evaluated=4)
    pts = {}
    for nm, pi in pops.items():
        p = S.rr_gl(G, 'F0', 'E', ['N'], pop=pi)
        pts[nm] = dict(n=p['n'], R_pp=p['R_pp'], R_deceq=p['R_deceq'], RR_N=p['RR']['N'], D_N_deceq=p['D_deceq']['N'])
    CNT = L.boot_counts(len(R), 20000, 20261113)[:NB]
    for nm in ('window', 'young'):
        b = S.boot_gl(G, 'F0', 'E', ['N'], CNT, pop=pops[nm])
        with np.errstate(divide='ignore', invalid='ignore'):
            rr = np.where(b['denE'] > 0, b['D']['N'] / b['denE'], np.nan)
        pts[nm]['RR_N_ci'] = L.summ(rr, pts[nm]['RR_N'])
        pts[nm]['R_pp_ci'] = L.summ(b['denE'] / L.NLEV, pts[nm]['R_pp'])
        pts[nm]['R_deceq_ci'] = L.pct(L.dec_eq(b['denE'], b['n']))
    doc['gridless'] = pts
    doc['draw'] = 'first %d rows of default_rng(20261113).integers(0, 20, (20000, 20)) over the 20 cut-in tuning runs in name order' % NB
    doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    (OUT / ('B9_CUTIN_lat%s_v01.json' % str(LAT).replace('.', 'p'))).write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    print(json.dumps(dict(events_found=found, rule=doc['rule_18_of_20'], window=pts['window'], young=pts['young']), default=float), flush=True)


if __name__ == '__main__':
    main()
