"""v13 package B, B3 step (2) and B4's sigma_a^2 (AMENDMENT_10_v13 section 3, rows B3 and B4; spec section 2): one scalar chosen on
the 20 lead-braking TUNING runs so that the median over runs of the lead track's mean position NIS is 2 (window [1.8, 2.2]).
New file, 19 Nov 2026 (Claude Opus 5.5). Read-only on P; writes only B_retrack\\out\\b3\\.

  param = kappa (variant B3: car Q = kappa * Q of record) or sigma_a2 (variant B4, with the frozen kappa).
  Search: param = 10^(-3 + 0.05 j), j = 0..120, all evaluated (6 processes); the first sign change of (median - 2) in j order;
  then bisection on log(param) inside that step until |median - 2| <= 0.01. No sign change: the grid value nearest 2.
  Lead track: at every decision of record, the re-tracked planner actor matched to the true lead (gc.match_many of record; several:
  nearest at `now`, as a9_4a); per track, its updates with frame index <= the largest state frame at which it was matched; per run,
  the mean NIS over those updates; NIS = nu' S^-1 nu, nu = z[0:2] - x_prior[0:2], S = P_prior[0:2,0:2] + R_rot[0:2,0:2].
Usage: python -I -B -X utf8 b3_nis_tune_v01.py kappa|sigma_a2 [constants_json_for_sigma]
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, math, pathlib, time, copy
LIB = pathlib.Path(r'ARS_TRIAL\revision_v13\work\shared\trackers')
sys.path.insert(0, str(LIB))
import trk_env_v01 as env
env.setup()
import numpy as np
OPENLOOP = pathlib.Path(r'<library folder>\openloop')
sys.path.insert(0, str(OPENLOOP))
import olcore_rt_v01 as rt                      # noqa: E402  (read-only)
import ol_gateR_core_v01 as gc                  # noqa: E402  (read-only: match_many, decisions)
import trk_tracker_v01 as T                     # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[1] / 'out' / 'b3'
OUT.mkdir(parents=True, exist_ok=True)
M4 = pathlib.Path(r'<library folder>\m4_perception_model')
R_FILE = OUT / 'B3_R_EXTRACT_v01.json'
GRID = [10. ** (-3 + 0.05 * j) for j in range(121)]
_RUNS = None


def lb_tuning_caps():
    import csv
    rows = [r for r in csv.DictReader(open(M4 / 'run_index_m4_v02.csv', encoding='utf-8'))
            if r['set'] == 'tune' and r['family'] == 'lead_braking' and r['use'] == '1']
    rows.sort(key=lambda r: r['archive'])
    assert len(rows) == 20
    return [(r['archive'], pathlib.Path(r['cap'])) for r in rows]


def load_run(cap):
    det = list(env.jl(cap / 'detections.jsonl'))
    Tr = rt.load_truth(cap, 'route_yaw_rh')
    truth0 = next(env.jl(cap / 'evaluation_truth.jsonl'))
    route_yaw = float(truth0['ego']['derived']['route_yaw_rh'])
    decs = []
    for k, dec in gc.decisions(cap):
        decs.append((k, dec['now']))
    centers = {}
    for fr in env.jl(cap / 'frames.jsonl'):
        ex = fr.get('execution')
        if ex and ex.get('new_decision') is not None and ex['new_decision']['mode'] == 'assessment':
            c = fr['state']['center_lh']; centers[fr['k']] = np.array([c[0], -c[1], c[2]])
    return dict(det=det, T=Tr, route_yaw=route_yaw, decs=decs, centers=centers, det_time=np.array([d['time'] for d in det]))


def run_stat(R, variant, const):
    trk = T.V13Tracker(variant, const=const)
    outs = [trk.step(copy.deepcopy(row['model']), row['time']) for row in R['det']]
    by_k = {d['k']: o for d, o in zip(R['det'], outs)}
    maxdi = {}
    for k, now in R['decs']:
        tr = R['T'].get(k)
        if tr is None:
            continue
        kd = 19 + 10 * ((k - 19) // 10)
        actors = T.planner_actors(by_k[kd], R['centers'][k], R['route_yaw'])
        ids, prim, order = gc.match_many(actors, now, tr)
        if prim is None:
            continue
        cand = [oi for oi, aid in enumerate(ids) if aid == prim]
        if not cand:
            continue
        if len(cand) > 1:
            tp = gc.oc.to_planner(tr['ego'], tr['actors'][prim][0], tr['actors'][prim][1])
            cand.sort(key=lambda oi: math.hypot(actors[oi]['x'] + (now - actors[oi]['state_time']) * actors[oi]['vx'] - tp[0],
                                                actors[oi]['y'] + (now - actors[oi]['state_time']) * actors[oi]['vy'] - tp[1]))
        a = actors[cand[0]]
        di = int(np.argmin(np.abs(R['det_time'] - a['state_time'])))
        tid = int(a['track_id'])
        maxdi[tid] = max(maxdi.get(tid, -1), di)
    nis = []
    for r in trk.rec.algebra:
        if r.get('kind') != 'update':
            continue
        tid = int(r['track'])
        if tid in maxdi and int(r['timestamp']) <= maxdi[tid]:
            x = np.asarray(r['prior']['state'], float).ravel(); P = np.asarray(r['prior']['P'], float)
            z = np.asarray(r['measurement'], float).ravel(); Rr = np.asarray(r['rotated_R'], float)
            nu = z[0:2] - x[0:2]; S = P[0:2, 0:2] + Rr[0:2, 0:2]
            nis.append(float(nu @ np.linalg.solve(S, nu)))
    return (float(np.mean(nis)) if nis else float('nan')), len(nis)


def _init(caps):
    global _RUNS
    _RUNS = [(name, load_run(cap)) for name, cap in caps]


def evaluate(args):
    variant, const = args
    per = [run_stat(R, variant, const) for _, R in _RUNS]
    vals = [p[0] for p in per]
    return float(np.median(vals)), vals, [p[1] for p in per]


def main():
    what = sys.argv[1]
    rx = json.loads(R_FILE.read_text(encoding='utf-8'))
    base = dict(R_car_diag=rx['R_car_diag'], kappa=1.0, sigma_a2=1.0, ca_acc_init_var=10.0)
    if what == 'kappa':
        variant = 'B3'
        mk = lambda p: dict(base, kappa=p)                                # noqa: E731
    elif what == 'sigma_a2':
        variant = 'B4'
        kc = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding='utf-8'))
        base['kappa'] = float(kc['kappa'])
        mk = lambda p: dict(base, sigma_a2=p)                             # noqa: E731
    else:
        raise SystemExit('usage: kappa|sigma_a2 [constants]')
    # PSD check of R_B3
    cfg = env.tracker_config()
    cm = T.car_matrices(base, cfg)
    ev = np.linalg.eigvalsh(cm['R'])
    caps = lb_tuning_caps()
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(6, initializer=_init, initargs=(caps,)) as pool:
        grid_res = pool.map(evaluate, [(variant, mk(p)) for p in GRID], chunksize=4)
    med = np.array([g[0] for g in grid_res])
    dev = med - 2.
    j_cross = next((j for j in range(len(GRID) - 1) if np.sign(dev[j]) != np.sign(dev[j + 1]) or dev[j] == 0), None)
    mono = bool(np.all(np.diff(med) <= 0) or np.all(np.diff(med) >= 0))
    hist = []
    _init(caps)
    if j_cross is None:
        jn = int(np.argmin(np.abs(dev)))
        best = GRID[jn]; best_med = float(med[jn]); reached = bool(abs(dev[jn]) <= 0.2)
        status = 'no sign change on the grid; nearest grid value taken'
    elif dev[j_cross] == 0:
        best = GRID[j_cross]; best_med = float(med[j_cross]); reached = True; status = 'grid value exactly 2'
    else:
        lo, hi = math.log10(GRID[j_cross]), math.log10(GRID[j_cross + 1])
        dlo = dev[j_cross]
        best, best_med = None, None
        for it in range(60):
            mid = 0.5 * (lo + hi)
            m, vals, ns = evaluate((variant, mk(10. ** mid)))
            hist.append(dict(log10=mid, param=10. ** mid, median=m))
            if abs(m - 2.) <= 0.01:
                best, best_med = 10. ** mid, m
                break
            if np.sign(m - 2.) == np.sign(dlo):
                lo = mid
            else:
                hi = mid
        if best is None:
            best, best_med = 10. ** mid, m
        reached = True; status = 'bisection'
    final = evaluate((variant, mk(best)))
    res = dict(code='b3_nis_tune_v01.py', what=what, variant=variant, rule='A10 B3 (2) / B4; spec section 2', base_constants=base,
               R_B3_min_eigenvalue=float(ev.min()), grid=GRID, grid_median=med.tolist(), grid_monotone=mono, j_first_sign_change=j_cross,
               bisection=hist, chosen=best, chosen_median=final[0], chosen_per_run=final[1], chosen_n_updates=final[2],
               runs=[n for n, _ in caps], window_reached=bool(1.8 <= final[0] <= 2.2), status=status,
               seconds=time.time() - t0, written=time.strftime('%Y-%m-%d %H:%M:%S'))
    (OUT / ('B3_TUNE_%s_v01.json' % what.upper())).write_text(json.dumps(res, indent=1), encoding='utf-8')
    print(json.dumps({k: res[k] for k in ('what', 'R_B3_min_eigenvalue', 'grid_monotone', 'j_first_sign_change', 'chosen', 'chosen_median',
                                         'window_reached', 'status', 'seconds')}, indent=1))


if __name__ == '__main__':
    main()
