r"""v13 round 2 (AMENDMENT_12 s3c): tune IMM2, the two-noise IMM = library B1 (IMM over the B3 CV filter and the B4 CA filter,
transition diagonal 0.95, initial mode probabilities (0.9, 0.1)) with its own constants: a quiet CV mode (kappa_q) and a high-noise CA
mode (sigma_a2_hi, kappa_ca = 1, i.e. absent). New file, 22 Nov 2026 (Claude Opus 5.5). No library change: kappa and sigma_a2 are
existing constants (trk_tracker_v01.car_matrices); kappa_ca is not used.

Statistic (A10 B3 rule (2), the frozen b3_nis_tune_v01.run_stat, restricted to a truth phase): on the 20 lead-braking TUNING runs, per
run the mean position NIS of the lead track's updates (lead track and update set exactly as run_stat: the re-tracked planner actor
matched to the true lead at each decision of record; per track, its updates with frame index <= the largest state frame at which it was
matched), keeping only the updates whose detector frame lies in the phase; the median over the runs that have at least one such update.
Truth phases of a detector frame at simulation tick k (the truth phase of record, trk_arrays_v01 / oxsb_extract_v05):
  k_on   = the first tick whose scenario request time assessment_time_s >= the case's brake_start_s (contract.json case.draw)
  k_stop = the first tick >= k_on at which the true lead (evaluation_truth target) has speed <= 0.5 m/s (VMIN of record)
  pre = k < k_on;  brk = k_on <= k < k_stop;  stop = k >= k_stop
Searches (first sign change of median - 2 in grid order, evaluated two grid points at a time, then bisection on log10 of the parameter
inside that step until |median - 2| <= 0.01; no sign change: the grid value nearest 2, said so):
  kq   variant B3 (the CV filter alone), phase pre, kappa = 10^(-3 + 0.05 j), j = 0..120 (the A10 B3 grid)
  sa2  variant B4 (the CA filter alone, built on the CV diagonal of kappa_q), phase brk, sigma_a2 = 10^(-3 + 0.05 j), j = 0..160
  check  identity: phase 'all' reproduces the frozen run_stat bit for bit (B3 at the kappa of record, 20 runs); no search
Writes out\imm2t\IMM2_TUNE_<KQ|SA2|CHECK>_v01.json and, after sa2, out\imm2t\IMM2_CONSTANTS_v01.json (the constants of record with
kappa = kappa_q and sigma_a2 = sigma_a2_hi).
Usage: python -I -B -X utf8 b_imm2_tune_v01.py check|kq|sa2
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, math, pathlib, time, copy
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import b3_nis_tune_v01 as V1                     # frozen: env.setup, run loading, lead matching, the statistic of record
import numpy as np
T = V1.T; gc = V1.gc; env = V1.env
import trk_arrays_v01 as A                       # frozen: prebrake_map (scenario request times per tick)

OUT = V1.OUT.parent / 'imm2t'
OUT.mkdir(parents=True, exist_ok=True)
CONST = pathlib.Path(r'ARS_TRIAL\revision_v13\work\shared\trackers\trk_constants_v01.json')
VMIN = 0.5
GRID_KQ = [10. ** (-3 + 0.05 * j) for j in range(121)]
GRID_SA2 = [10. ** (-3 + 0.05 * j) for j in range(161)]
_RUNS = None


def phases(cap):
    """per tick k: 0 pre, 1 brk, 2 stop (definition in the module text); plus k_on, k_stop and the lead id."""
    cap = pathlib.Path(cap); rd = cap.parents[3]
    S = json.loads((rd / 'SUMMARY.json').read_text(encoding='utf-8'))
    base = S['assessment_outcomes']['base_frame']
    draw = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))['case']['draw']
    bs = draw.get('brake_start_s')
    at = A.prebrake_map(cap, base)
    k_on = min((k for k, t in at.items() if t is not None and bs is not None and t >= bs), default=None)
    Tr = V1.rt.load_truth(cap, 'route_yaw_rh')
    k_stop = None
    if k_on is not None:
        for k in sorted(Tr):
            if k < k_on:
                continue
            tid = Tr[k]['target_id']; a = Tr[k]['actors'].get(tid) if tid is not None else None
            if a is not None and math.hypot(a[5], a[6]) <= VMIN:
                k_stop = k
                break
    return dict(k_on=k_on, k_stop=k_stop, brake_start_s=bs)


def phase_of(k, ph):
    if ph['k_on'] is None or k < ph['k_on']:
        return 0
    if ph['k_stop'] is None or k < ph['k_stop']:
        return 1
    return 2


def run_stat_phase(R, variant, const, want):
    """V1.run_stat (verbatim lead matching and update set) with the updates restricted to truth phase `want` (0, 1, 2 or 'all')."""
    trk = T.V13Tracker(variant, const=const)
    outs = [trk.step(copy.deepcopy(row['model']), row['time']) for row in R['det']]
    by_k = {d['k']: o for d, o in zip(R['det'], outs)}
    maxdi = {}; prim_is_target = []
    for k, now in R['decs']:
        tr = R['T'].get(k)
        if tr is None:
            continue
        kd = 19 + 10 * ((k - 19) // 10)
        actors = T.planner_actors(by_k[kd], R['centers'][k], R['route_yaw'])
        ids, prim, order = gc.match_many(actors, now, tr)
        if prim is None:
            continue
        prim_is_target.append(prim == tr.get('target_id'))
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
            if want != 'all' and phase_of(R['det'][int(r['timestamp'])]['k'], R['ph']) != want:
                continue
            x = np.asarray(r['prior']['state'], float).ravel(); P = np.asarray(r['prior']['P'], float)
            z = np.asarray(r['measurement'], float).ravel(); Rr = np.asarray(r['rotated_R'], float)
            nu = z[0:2] - x[0:2]; S = P[0:2, 0:2] + Rr[0:2, 0:2]
            nis.append(float(nu @ np.linalg.solve(S, nu)))
    return (float(np.mean(nis)) if nis else float('nan')), len(nis), (float(np.mean(prim_is_target)) if prim_is_target else float('nan'))


def _init(caps):
    global _RUNS
    _RUNS = []
    for name, cap in caps:
        R = V1.load_run(cap); R['ph'] = phases(cap)
        _RUNS.append((name, R))


def evaluate(args):
    variant, const, want = args
    per = [run_stat_phase(R, variant, const, want) for _, R in _RUNS]
    vals = [p[0] for p in per]
    ok = [v for v in vals if np.isfinite(v)]
    return (float(np.median(ok)) if ok else float('nan')), vals, [p[1] for p in per], [p[2] for p in per]


def base_constants():
    c = json.loads(CONST.read_text(encoding='utf-8'))
    return c, {k: c[k] for k in ('R_car_diag', 'kappa', 'sigma_a2', 'ca_acc_init_var')}


def search(name, variant, want, grid, mk):
    caps = V1.lb_tuning_caps()
    if len(caps) != 20:
        raise SystemExit('REFUSED: %d tuning runs' % len(caps))
    t00 = time.time()
    from multiprocessing import Pool
    med = []; j_cross = None
    with Pool(2, initializer=_init, initargs=(caps,)) as pool:
        for s in range(0, len(grid), 2):
            for r in pool.map(evaluate, [(variant, mk(p), want) for p in grid[s:s + 2]]):
                med.append(r[0])
            dev = np.array(med) - 2.
            j_cross = next((j for j in range(len(dev) - 1) if np.sign(dev[j]) != np.sign(dev[j + 1]) or dev[j] == 0), None)
            print('%s %d/%d medians %s (%.0f s)' % (name, len(med), len(grid), [round(x, 4) for x in med[-2:]], time.time() - t00), flush=True)
            if j_cross is not None:
                break
    _init(caps)
    hist = []
    if j_cross is None:
        dev = np.array(med) - 2.; jn = int(np.nanargmin(np.abs(dev)))
        best = grid[jn]; status = 'no sign change on the grid; nearest grid value taken'
    elif med[j_cross] == 2.:
        best = grid[j_cross]; status = 'grid value exactly 2'
    else:
        lo, hi = math.log10(grid[j_cross]), math.log10(grid[j_cross + 1]); dlo = med[j_cross] - 2.
        best = None
        for it in range(40):
            mid = 0.5 * (lo + hi)
            m = evaluate((variant, mk(10. ** mid), want))[0]
            hist.append(dict(it=it, param=10. ** mid, median=m))
            if abs(m - 2.) <= 0.01:
                best = 10. ** mid; break
            if np.sign(m - 2.) == np.sign(dlo):
                lo = mid; dlo = m - 2.
            else:
                hi = mid
        if best is None:
            best = 10. ** (0.5 * (lo + hi))
        status = 'bisection'
    final = evaluate((variant, mk(best), want))
    phs = [dict(run=n, **R['ph']) for n, R in _RUNS]
    doc = dict(code='b_imm2_tune_v01.py', search=name, variant=variant, phase={0: 'pre', 1: 'brk', 2: 'stop'}[want],
               rule='A10 B3 rule (2) restricted to a truth phase; AMENDMENT_12 s3c', base_constants=mk(best), grid=grid[:len(med)],
               grid_median=med, grid_evaluated=len(med), grid_size=len(grid), j_first_sign_change=j_cross, bisection=hist, chosen=best,
               chosen_median=final[0], chosen_per_run=final[1], chosen_n_updates=final[2], chosen_prim_is_target_share=final[3],
               runs_used=int(np.sum(np.isfinite(final[1]))), runs=[n for n, _ in caps], phases=phs,
               window_reached=bool(1.8 <= final[0] <= 2.2), status=status, seconds=time.time() - t00, written=time.strftime('%Y-%m-%d %H:%M:%S'))
    (OUT / ('IMM2_TUNE_%s_v01.json' % name.upper())).write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(json.dumps(dict(search=name, chosen=best, median=final[0], reached=doc['window_reached'], status=status, runs_used=doc['runs_used'],
                          seconds=round(doc['seconds']))), flush=True)
    return doc


def main():
    what = sys.argv[1]
    full, base = base_constants()
    if what == 'check':
        caps = V1.lb_tuning_caps(); V1._init(caps); _init(caps)
        ref = V1.evaluate(('B3', dict(base)))
        mine = evaluate(('B3', dict(base), 'all'))
        same = bool(ref[1] == mine[1] and ref[2] == mine[2] and ref[0] == mine[0])
        per_phase = {nm: evaluate(('B3', dict(base), w))[0] for w, nm in ((0, 'pre'), (1, 'brk'), (2, 'stop'))}
        per_phase_b4 = {nm: evaluate(('B4', dict(base), w))[0] for w, nm in ((0, 'pre'), (1, 'brk'), (2, 'stop'))}
        doc = dict(code='b_imm2_tune_v01.py check', identical_to_frozen_run_stat=same, median_frozen=ref[0], median_all=mine[0],
                   per_run_frozen=ref[1], per_run_all=mine[1], n_frozen=ref[2], n_all=mine[2], prim_is_target_share=mine[3],
                   B3_record_median_by_phase=per_phase, B4_record_median_by_phase=per_phase_b4,
                   phases=[dict(run=n, **R['ph']) for n, R in _RUNS], written=time.strftime('%Y-%m-%d %H:%M:%S'))
        (OUT / 'IMM2_TUNE_CHECK_v01.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')
        print(json.dumps({k: doc[k] for k in ('identical_to_frozen_run_stat', 'median_frozen', 'median_all', 'B3_record_median_by_phase',
                                             'B4_record_median_by_phase')}), flush=True)
        print('k_on / k_stop:', [(p['k_on'], p['k_stop']) for p in doc['phases']], flush=True)
    elif what == 'kq':
        search('kq', 'B3', 0, GRID_KQ, lambda p: dict(base, kappa=p))
    elif what == 'sa2':
        kq = json.loads((OUT / 'IMM2_TUNE_KQ_v01.json').read_text(encoding='utf-8'))
        b2 = dict(base, kappa=float(kq['chosen']))
        doc = search('sa2', 'B4', 1, GRID_SA2, lambda p: dict(b2, sigma_a2=p))
        c = dict(full); c['kappa'] = float(kq['chosen']); c['sigma_a2'] = float(doc['chosen'])
        c['imm2'] = dict(kappa_q=c['kappa'], kappa_q_median_pre=kq['chosen_median'], kappa_q_window_reached=kq['window_reached'],
                         kappa_q_status=kq['status'], sigma_a2_hi=c['sigma_a2'], sigma_a2_median_brk=doc['chosen_median'],
                         sigma_a2_window_reached=doc['window_reached'], sigma_a2_status=doc['status'], kappa_ca='absent (1)',
                         variant='B1 (diag 0.95, mu0 (0.9, 0.1))', sources=['IMM2_TUNE_KQ_v01.json', 'IMM2_TUNE_SA2_v01.json'])
        (OUT / 'IMM2_CONSTANTS_v01.json').write_text(json.dumps(c, indent=1), encoding='utf-8')
        print('constants written', flush=True)
    elif what == 'sa2rec':          # alternative for the coordinator (22 Nov 00:16): kappa_q = the kappa of record (B3, whole runs)
        doc = search('sa2rec', 'B4', 1, GRID_SA2, lambda p: dict(base, sigma_a2=p))
        c = dict(full); c['sigma_a2'] = float(doc['chosen'])
        c['imm2'] = dict(kappa_q=c['kappa'], kappa_q_source='kappa of record (A10 B3 rule (2) on whole runs, median 1.994)',
                         sigma_a2_hi=c['sigma_a2'], sigma_a2_median_brk=doc['chosen_median'], sigma_a2_window_reached=doc['window_reached'],
                         sigma_a2_status=doc['status'], kappa_ca='absent (1)', variant='B1 (diag 0.95, mu0 (0.9, 0.1))',
                         sources=['IMM2_TUNE_SA2REC_v01.json'])
        (OUT / 'IMM2_CONSTANTS_REC_v01.json').write_text(json.dumps(c, indent=1), encoding='utf-8')
        print('constants written (record kappa)', flush=True)
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
