r"""v13 sprint, step 2: re-tune the CA filter of the IMM (B1r) to its NIS window (AMENDMENT_11_v13 §6; coordinator 21 Nov 13:58 EST).
New file, 21 Nov 2026 (Claude Opus 5.5). The frozen b3_nis_tune_v01.py is imported unchanged for the statistic (lead-track mean
position NIS per run, median over the 20 lead-braking TUNING runs) and its run loading; only the search grids are new.
Criterion (A10 B3 rule (2), unchanged): median in [1.8, 2.2]; first sign change of (median - 2) in grid order, then bisection on log10
of the parameter inside that step until |median - 2| <= 0.01. Variant B4 (the CA filter); constants of record trk_constants_v01.json.
  stage1  sigma_a2 = 10^(-3 + 0.05 j), j = 0, -1, ..., -120 (0.001 down to 1e-9), visited from the old grid's end downward.
  stage2  only if stage 1 finds no sign change: sigma_a2 frozen at 0.001 and kappa_ca = 10^(-0.05 j), j = 0..120 (shared\trackers\
          trk_tracker_v02.py: kappa_ca scales only the CA filter's position and velocity process-noise terms). No sign change: the
          grid value nearest 2, and the window is reported as not reached.
The grid is evaluated in order, two points at a time, and stops after the first sign change. Writes out\b3\B4_TUNE_<STAGE>_v02.json and,
for the stage that is used, out\b3\B1R_CONSTANTS_v02.json (the constants of record plus the new value).
Usage: python -I -B -X utf8 b3_nis_tune_v02.py stage1|stage2
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, math, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import b3_nis_tune_v01 as V1                     # frozen: env.setup, run loading, the NIS statistic
import trk_tracker_v02                           # noqa: F401  (kappa_ca; inert without it)
import numpy as np

OUT = V1.OUT
CONST = pathlib.Path(r'ARS_TRIAL\revision_v13\work\shared\trackers\trk_constants_v01.json')
STAGES = {'stage1': ('sigma_a2', [10. ** (-3 + 0.05 * j) for j in range(0, -121, -1)]),
          'stage2': ('kappa_ca', [10. ** (-0.05 * j) for j in range(0, 121)])}


def main():
    stage = sys.argv[1]; param, GRID = STAGES[stage]
    t00 = time.time()
    const = json.loads(CONST.read_text(encoding='utf-8'))
    base = {k: const[k] for k in ('R_car_diag', 'kappa', 'sigma_a2', 'ca_acc_init_var')}
    mk = (lambda p: dict(base, sigma_a2=p)) if param == 'sigma_a2' else (lambda p: dict(base, kappa_ca=p))   # noqa: E731
    caps = V1.lb_tuning_caps()
    if len(caps) != 20:
        raise SystemExit('REFUSED: %d tuning runs' % len(caps))
    from multiprocessing import Pool
    med = []; vals = []; j_cross = None
    with Pool(2, initializer=V1._init, initargs=(caps,)) as pool:
        for s in range(0, len(GRID), 2):
            res = pool.map(V1.evaluate, [('B4', mk(p)) for p in GRID[s:s + 2]])
            for r in res:
                med.append(r[0]); vals.append(r[1])
            dev = np.array(med) - 2.
            j_cross = next((j for j in range(len(dev) - 1) if np.sign(dev[j]) != np.sign(dev[j + 1]) or dev[j] == 0), None)
            print('%s %d/%d medians %s (%.0f s)' % (stage, len(med), len(GRID), [round(x, 4) for x in med[-2:]], time.time() - t00), flush=True)
            if j_cross is not None:
                break
    V1._init(caps)
    hist = []
    if j_cross is None:
        dev = np.array(med) - 2.; jn = int(np.argmin(np.abs(dev)))
        best = GRID[jn]; status = 'no sign change on the grid; nearest grid value taken'
    elif med[j_cross] == 2.:
        best = GRID[j_cross]; status = 'grid value exactly 2'
    else:
        lo, hi = math.log10(GRID[j_cross]), math.log10(GRID[j_cross + 1]); dlo = med[j_cross] - 2.
        best = None
        for it in range(40):
            mid = 0.5 * (lo + hi)
            m, v, ns = V1.evaluate(('B4', mk(10. ** mid)))
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
    final = V1.evaluate(('B4', mk(best)))
    reached = bool(1.8 <= final[0] <= 2.2)
    doc = dict(code='b3_nis_tune_v02.py', stage=stage, param=param, variant='B4', rule='A10 B3 rule (2); AMENDMENT_11 section 6',
               base_constants=base, grid=GRID[:len(med)], grid_median=med, grid_evaluated=len(med), grid_size=len(GRID), j_first_sign_change=j_cross,
               bisection=hist, chosen=best, chosen_median=final[0], chosen_per_run=final[1], chosen_n_updates=final[2],
               runs=[n for n, _ in caps], window_reached=reached, status=status, seconds=time.time() - t00, written=time.strftime('%Y-%m-%d %H:%M:%S'))
    (OUT / ('B4_TUNE_%s_v02.json' % stage.upper())).write_text(json.dumps(doc, indent=1), encoding='utf-8')
    use = reached or stage == 'stage2'
    if use:
        c = dict(const); c[param] = best
        c['b1r'] = dict(stage=stage, param=param, value=best, median=final[0], window_reached=reached, source='B4_TUNE_%s_v02.json' % stage.upper())
        (OUT / 'B1R_CONSTANTS_v02.json').write_text(json.dumps(c, indent=1), encoding='utf-8')
    print(json.dumps(dict(stage=stage, chosen=best, median=final[0], reached=reached, status=status, constants_written=use,
                          seconds=round(doc['seconds']))), flush=True)


if __name__ == '__main__':
    main()
