"""Recount (second program) of D2, the event-level table (AMENDMENT_10_v13.md sec. 6 D2; CD_DEFINITIONS_v13.md "D2").
Claude Fable 5.2. Written from the amendment and the definitions, without reading the first programs.

Per source (F0, N, CK3, TG = cTG2) and scoring (3 s commitment; reaction-and-stop at tau = 0.75 s, 6 m/s^2, jerk 12.65):
  * the grid points pooled over the run set (caution always by the 3 s definition; wrong go by the scoring's safe set);
  * the non-dominated points (no other point with caution <= and wrong go <); the one with caution nearest 2 and 5 points
    (ties: smaller g);
  * at that scale: the wrong-go decisions (evaluated, selected row unsafe under the scoring); the runs with >= 1 wrong go;
    per wrong-go decision the closing speed at the first loss of clearance (first of the 61 ticks of the committed plan at which
    the ego rectangle is at distance <= 0 from a true actor's rectangle; true frames only); per run the median; across runs
    the median of the run medians.

Usage (python -I -B -X utf8):
  rc_d2_event_table_v13.py --test-old [--old-rs] [--runs N] [--tag T]   the 35 old runs, 3 s commitment (--old-rs: also
                                                                       reaction-and-stop from the v11 cache of record)
  rc_d2_event_table_v13.py [--logs-root R | --run-dir-template .. --cap-dir-template ..] [--tag T]    after Lock 2
Output: out\\RC_D2_EVENT_TABLE_v13[_TESTOLD][_T].json (never overwritten).
"""
import argparse, math, os, pathlib, sys, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
HERE = pathlib.Path(__file__).resolve().parent
if '--test-old' not in sys.argv and '-h' not in sys.argv and '--help' not in sys.argv \
        and not (HERE.parent.parent.parent / 'LOCK_A10_2.txt').exists():   # sealing gate before anything is imported or read
    raise SystemExit('REFUSED: LOCK_A10_2.txt does not exist; fresh runs are sealed (use --test-old)')
sys.path.insert(0, str(HERE))                                              # python -I drops the script folder
sys.path.insert(0, str(HERE.parent.parent / 'shared' / 'trackers'))
import trk_env_v01 as env                                                  # noqa: E402  (before numpy)
env.setup()
import numpy as np                                                         # noqa: E402
import trk_arrays_v01 as TA                                                # noqa: E402
import trk_score_v01 as TS                                                 # noqa: E402
import rc_d_common_v13 as K                                                # noqa: E402

L = K.L; GRID = K.GRID
SOURCES = ['F0', 'N', 'CK3', 'TG']
TARGETS = [2.0, 5.0]
TAU = 0.75; A_STOP = 6.0; H = 0.05; JERK = 12.65
SC3 = 'commit_3s'; SCR = 'react_stop_tau0p75'


# ------------------------------------------------------------------------------------------------ operating points
def nondominated(c, w):
    """Indices of the finite points not dominated (no point with caution <= and wrong go <)."""
    ok = np.isfinite(c) & np.isfinite(w)
    keep = []
    for i in np.nonzero(ok)[0]:
        if not np.any(ok & (c <= c[i]) & (w < w[i])):
            keep.append(int(i))
    return np.array(keep, int)


def operating_point(c, w, target):
    fr = nondominated(c, w)
    d = np.abs(c[fr] - target)
    j = int(fr[np.nonzero(d == d.min())[0]].min())                          # ties: smaller g (smaller grid index)
    return j, int(fr.size), int(np.sum(d == d.min()))


# ------------------------------------------------------------------------------------------------ plans
def rs_speed(s_row, v_row, a_row, tau, A):
    """Speed at the 61 ticks of 'the row until tau, then the stop of record' (the companion of trk_score_v01.stop_profile_cont,
    which returns positions): jerk-limited ramp of the acceleration to -A, then -A until standstill, speed never below 0."""
    v = np.array(v_row, float)[:61].copy()
    _, v0, a0 = TS.row_state_at(s_row, v_row, a_row, tau)
    jr = -JERK if a0 > -A else JERK
    t1 = abs(-A - a0) / JERK
    v1 = v0 + a0 * t1 + .5 * jr * t1 * t1
    # stop time: the first time in (0, t1] at which the ramp speed reaches 0, else t1 + v1 / A
    if v0 <= 0. and a0 <= 0.:
        ts = 0.
    else:
        ts = None
        if jr != 0.:
            disc = a0 * a0 - 2. * jr * v0
            if disc >= 0.:
                rts = sorted(x for x in ((-a0 - math.sqrt(disc)) / jr, (-a0 + math.sqrt(disc)) / jr) if 1e-12 < x <= t1)
                if rts:
                    ts = rts[0]
        if ts is None:
            ts = t1 + max(v1, 0.) / A
    for j in range(61):
        if j * H > tau + 1e-9:
            t = min(j * H - tau, ts)
            vv = (v0 + a0 * t + .5 * jr * t * t) if t <= t1 else (v1 - A * (t - t1))
            v[j] = max(vv, 0.)
    return v


class Capture:
    """One run's logs: truth, logged decisions; closing speed of a (decision, row, scoring), cached."""

    def __init__(self, rd, cap):
        self.Lr = TA.load_capture(rd, cap)
        self.decs = list(TA.gc.decisions(self.Lr['cap']))
        self.rows = {}; self.done = {}

    def closing(self, i, k_expected, row, scoring):
        key = (i, row, scoring)
        if key in self.done:
            return self.done[key]
        T = self.Lr['T']; k, dec = self.decs[i]
        if int(k) != int(k_expected):
            raise RuntimeError('REFUSED: decision %d is at tick %d in the capture, %d in the arrays' % (i, k, k_expected))
        if i not in self.rows:
            ms = dec['model_state']
            rows = TA.finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'],
                                                     dec['actors'], dec['ego_length'], dec['ego_width'], dec['now'],
                                                     TA.consumer.Diagnostics())
            if len(rows) != 17:
                raise RuntimeError('REFUSED: %d planner rows' % len(rows))
            self.rows[i] = rows
        rw = self.rows[i][row]
        if scoring == SC3:
            s = np.array(rw['s'], float)[:61]; v = np.array(rw['v'], float)[:61]
        else:
            s = TS.stop_profile_cont(rw['s'], rw['v'], rw['a'], TAU, A_STOP)
            v = rs_speed(rw['s'], rw['v'], rw['a'], TAU, A_STOP)
        ego = T[k]['ego']; u = np.array([math.cos(ego[2]), math.sin(ego[2])])
        E = TA.oc.rect_corners(ego[0] + s * u[0], ego[1] + s * u[1], ego[2], dec['ego_length'] / 2, dec['ego_width'] / 2)
        wt = TA.ox.window_truth(T, k, self.Lr['kmax'], self.Lr['draw'], False)[0]
        best = None; dmin = math.inf
        for aid, (c, hd, hl, hw) in wt.items():
            ok = np.isfinite(c[:61, 0])
            if not ok.any():
                continue
            Arect = TA.oc.rect_corners(c[:61, 0][ok], c[:61, 1][ok], hd[:61][ok], hl, hw)
            D = TA.oc.poly_dist(E[ok], Arect)
            dmin = min(dmin, float(D.min()))
            hit = np.nonzero(ok)[0][D <= 0.]
            if hit.size and (best is None or int(hit[0]) < best[0]):       # earliest tick; ties: the first actor in truth order
                best = (int(hit[0]), aid)
        if best is None:
            out = dict(found=False, dmin=dmin)
        else:
            j, aid = best
            act = T[k + j]['actors'][aid]
            va = act[5] * u[0] + act[6] * u[1]
            out = dict(found=True, tick=j, actor=aid, plan_speed=float(v[j]), actor_speed_along=float(va),
                       closing=float(v[j] - va), dmin=dmin)
        self.done[key] = out
        return out


# ------------------------------------------------------------------------------------------------ run folders
def old_dirs(run):
    rd = K.OLD_ARCH / run
    caps = [p for p in (rd / 'x' / run / 'capture').iterdir() if p.is_dir()]
    if len(caps) != 1:
        raise RuntimeError('REFUSED %s: %d capture folders' % (run, len(caps)))
    return rd, caps[0]


def fresh_dirs(run, case, a):
    K.require_lock()
    if a.run_dir_template and a.cap_dir_template:
        return (pathlib.Path(a.run_dir_template.format(run=run, case=case)),
                pathlib.Path(a.cap_dir_template.format(run=run, case=case)))
    base = pathlib.Path(a.logs_root) / run
    if not base.is_dir():
        raise RuntimeError('REFUSED: %s is not a folder (pass --logs-root or the two templates)' % base)
    sm = sorted(base.rglob('SUMMARY.json'), key=lambda p: (len(p.parts), str(p)))
    fr = sorted((p for p in base.rglob('frames.jsonl') if (p.parent / 'evaluation_truth.jsonl').exists()
                 and (p.parent / 'contract.json').exists()), key=lambda p: (len(p.parts), str(p)))
    if not sm or len(fr) != 1:
        raise RuntimeError('REFUSED %s: SUMMARY.json found %d, capture folders found %d under %s' % (run, len(sm), len(fr), base))
    return sm[0].parent, fr[0].parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--old-rs', action='store_true', help='test: also reaction-and-stop on old runs (v11 cache t0p75_a6p0)')
    ap.add_argument('--runs', type=int, default=0, help='test only: use the first N old runs')
    ap.add_argument('--logs-root', default=str(K.CD / 'archives'), help='fresh: folder holding <run>\\ with SUMMARY.json and the capture')
    ap.add_argument('--run-dir-template', default='', help='fresh: e.g. X:\\logs\\{run}')
    ap.add_argument('--cap-dir-template', default='', help='fresh: e.g. X:\\logs\\{run}\\x\\{run}\\capture\\{case}')
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    t0 = time.time()
    name = 'RC_D2_EVENT_TABLE_v13' + ('_TESTOLD' if a.test_old else '') + ('_' + a.tag if a.tag else '') + '.json'
    outf = K.OUT / name
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    if a.test_old:
        runs = K.old_runs()
        if a.runs:
            runs = runs[:a.runs]
        scorings = [SC3] + ([SCR] if a.old_rs else [])
        for r in runs:
            r['dirs'] = old_dirs(r['run'])
            if a.old_rs:
                r['clearR'] = L.clean_clear(r['cache'][L.vkey(TAU, A_STOP)])
    else:
        K.require_lock()
        if a.old_rs or a.runs:
            raise SystemExit('REFUSED: --old-rs and --runs are test options')
        ids = K.cases_c_lead()
        if len(ids) != 105:
            raise RuntimeError('REFUSED: %d lead-braking runs' % len(ids))
        runs = []
        for rid, case in ids:
            r = K.fresh_run(rid, need_tg=True, need_rs=True, variant_kind=None)
            r['dirs'] = fresh_dirs(rid, case, a)
            runs.append(r)
        scorings = [SC3, SCR]
    for r in runs:
        r['safe'] = {SC3: r['clear1'] > 0.}
        if SCR in scorings:
            r['safe'][SCR] = r['clearR'] > 0.
        r['sel'] = {s: K.grid_sel(r, s) for s in SOURCES}
    doc = dict(code='rc_d2_event_table_v13.py',
               mode='TEST ON OLD RUNS (exploratory; not a D2 result)' if a.test_old else 'fresh lead-braking runs',
               spec='AMENDMENT_10_v13.md sec. 6 D2; CD_DEFINITIONS_v13.md D2', n_runs=len(runs), runs=[r['run'] for r in runs],
               scorings=scorings, targets=TARGETS, table={})
    caps = {}
    for s in SOURCES:
        doc['table'][s] = {}
        for sc in scorings:
            T = np.stack([K.run_table(r, r['sel'][s], r['safe'][sc]) for r in runs]).sum(axis=0)       # (202, NST)
            with np.errstate(divide='ignore', invalid='ignore'):
                w = 100. * T[:, 1] / T[:, 0]; c = 100. * T[:, 2] / T[:, 3]
            doc['table'][s][sc] = {}
            for tgt in TARGETS:
                j, nfr, ntie = operating_point(c, w, tgt)
                per_run = {}; n_wg = 0; n_nofound = 0; all_cs = []
                for r in runs:
                    n = r['ev'].size; ar = np.arange(n)
                    sel = r['sel'][s][j]
                    wg = np.nonzero(r['ev'] & ~r['safe'][sc][ar, sel])[0]
                    if wg.size == 0:
                        continue
                    n_wg += int(wg.size)
                    if r['run'] not in caps:
                        caps[r['run']] = Capture(*r['dirs'])
                        if len(caps[r['run']].decs) != n:
                            raise RuntimeError('REFUSED %s: %d logged decisions, %d array rows' % (r['run'], len(caps[r['run']].decs), n))
                    cs = []
                    for i in wg:
                        o = caps[r['run']].closing(int(i), int(r['k'][i]), int(sel[i]), sc)
                        if o['found']:
                            cs.append(o['closing'])
                        else:
                            n_nofound += 1
                    all_cs += cs
                    per_run[r['run']] = dict(n_wrong_go=int(wg.size), n_with_loss_tick=len(cs),
                                             median_closing_mps=float(np.median(cs)) if cs else float('nan'))
                meds = np.array([v['median_closing_mps'] for v in per_run.values()], float)
                meds = meds[np.isfinite(meds)]
                doc['table'][s][sc]['%g' % tgt] = dict(
                    grid_index=j, g=float(GRID[j]), caution=float(c[j]), wrong_go=float(w[j]), n_frontier_points=nfr,
                    n_tied_nearest=ntie, n_decisions=int(round(T[j, 0])), n_wrong_go_decisions=n_wg,
                    n_wrong_go_from_table=int(round(T[j, 1])), n_runs_with_wrong_go=len(per_run),
                    n_wrong_go_without_loss_tick=n_nofound, n_runs_with_a_median=int(meds.size),
                    median_of_run_medians_mps=float(np.median(meds)) if meds.size else float('nan'),
                    median_over_decisions_mps=float(np.median(all_cs)) if all_cs else float('nan'),
                    per_run=per_run)
                e = doc['table'][s][sc]['%g' % tgt]
                if e['n_wrong_go_decisions'] != e['n_wrong_go_from_table']:
                    raise RuntimeError('REFUSED: wrong-go counts differ (%s %s %g)' % (s, sc, tgt))
                print('%-4s %-20s %g%%: g=%.4g caution=%.3f wrong go=%.3f runs with wrong go=%d median of medians=%.3f m/s (no tick: %d)'
                      % (s, sc, tgt, e['g'], e['caution'], e['wrong_go'], e['n_runs_with_wrong_go'], e['median_of_run_medians_mps'],
                         n_nofound), flush=True)
    doc['n_captures_read'] = len(caps)
    doc['seconds'] = time.time() - t0; doc['written'] = K.clock()
    K.write_once(outf, doc)
    print('written', outf)


if __name__ == '__main__':
    sys.exit(main())
