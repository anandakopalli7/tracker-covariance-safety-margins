"""Recount (second program) of D2's reaction-and-stop column with the EXTENDED scoring (stage 2 of Lock 2). New file, 20 Nov 2026
(Claude Fable 5.2, claude-fable-5-2).

Why: AMENDMENT_10_v13.md section 1 fixes "the reaction-and-stop scoring, with plans judged until the stop ends". CD_DEFINITIONS_v13.md
("Superseded 20 Nov 2026") therefore moves D2's reaction-and-stop column to the extended clearance of v11
(rev_e1_extended_truth_extract_v01.py, clearX_<vkey>; safe iff clearX > 0, rev_e2's 'est'); the first loss of clearance may lie
beyond tick 60, up to the stop's end. The existing recount_d files are untouched; rc_d2_event_table_v13.py keeps the 3 s column.

Written from A10 (sections 1, 6 D2), CD_DEFINITIONS_v13.md ("D2", its additions, the superseding note), the method of record
rev_e1 / rev_e2 (v11) and the existing second program rc_d2_event_table_v13.py (same operating-point rule, first-loss tick and
closing speed; its functions nondominated / operating_point / old_dirs / fresh_dirs are imported). No first program was read.

Per source (F0, N, CK3, TG = cTG2), tau = 0.75 s, A = 6 m/s^2, jerk 12.65 m/s^3:
  * safe set of the scoring: clean_clear(clearX_t0p75_a6p0) > 0 (shared extended arrays; old runs: v11 out\\ext; fresh: arrays\\RSX);
    caution by the 3 s commitment; grid points pooled over the run set; non-dominated points; the one with caution nearest 2 and
    5 points (ties: smaller g);
  * at that scale: the wrong-go decisions (evaluated, selected row unsafe under the scoring); runs with >= 1 wrong go;
  * per wrong-go decision, the first loss of clearance: the first tick j in 0..J of the committed plan at which the ego rectangle
    is at distance <= 0 from a true actor's rectangle. Plan: the row until 0.75 s (tick 15), then the stop of record from the row's
    speed v[15] and acceleration a[14] (optA_lib_v02.brake_profile: jerk-limited ramp to -6 m/s^2, then -6 m/s^2 to standstill,
    position held). J = max(60, ceil(t_stop_end / 0.05 - 1e-9)), capped by the frames the recording holds. Truth: true frames
    only (an actor's frames up to its first missing one, as rev_e1.window_truth_ext);
  * closing speed: the plan's speed at that tick (the row's speed up to tick 15; then the derivative of the stop profile, 0 from
    the stop on) minus the true actor's velocity at that tick along the ego heading of the decision tick; ties at one tick: the
    first actor in the truth's order;
  * per run the median over its wrong-go decisions, across runs the median of the run medians.
Identity anchor: for every wrong-go pair, the smallest distance this program finds over frames 0..J equals the arrays' clearX.

Keys: D2.<SRC>.<c2|c5>.rs.runs (integer) and D2.<SRC>.<c2|c5>.rs.vclose (m/s; null if no run has a median).
Usage (python -I -B -X utf8):
  rc_d2_rs_v13.py --test-old [--runs N] [--tag T]     the 35 old runs with v11's out\\ext arrays
  rc_d2_rs_v13.py [--logs-root R] [--tag T]           fresh runs; REFUSED unless LOCK_A10_2.txt AND LOCK_A10_2c.txt exist
Output: out\\RC_D2_RS_v13[_TESTOLD][_T].json (never overwritten).
"""
import argparse, math, os, pathlib, sys, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
HERE = pathlib.Path(__file__).resolve().parent
ROOT13 = HERE.parent.parent.parent
LOCK2 = ROOT13 / 'LOCK_A10_2.txt'
LOCK2C = ROOT13 / 'LOCK_A10_2c.txt'
TEST_OLD = '--test-old' in sys.argv


def require_stage2():
    """Stage 2 of Lock 2: both lock files must exist before anything of a fresh run is opened."""
    if not (LOCK2.is_file() and LOCK2C.is_file()):
        raise SystemExit('REFUSED: fresh runs are sealed until %s and %s both exist (use --test-old)' % (LOCK2, LOCK2C))


if not TEST_OLD and '-h' not in sys.argv and '--help' not in sys.argv:
    require_stage2()                                                       # before anything is imported or read
sys.path.insert(0, str(HERE))                                              # python -I drops the script folder
sys.path.insert(0, str(HERE.parent.parent / 'shared' / 'trackers'))
import trk_env_v01 as env                                                  # noqa: E402  (before numpy)
env.setup()
import numpy as np                                                         # noqa: E402
import trk_arrays_v01 as TA                                                # noqa: E402
import rc_d_common_v13 as K                                                # noqa: E402
import rc_d2_event_table_v13 as D2                                         # noqa: E402  (second program: operating-point rule, folders)

L = K.L; GRID = K.GRID
SOURCES = ['F0', 'N', 'CK3', 'TG']
TARGETS = [(2.0, 'c2'), (5.0, 'c5')]
TAU = 0.75; A_STOP = 6.0; H = 0.05; JERK = 12.65
KEY = L.vkey(TAU, A_STOP)
JR = int(round(TAU / H))
EXT_OLD = K.V11 / 'out' / 'ext'
PROGRAM = 'rc_d2_rs_v13.py'


# ------------------------------------------------------------------------------------------------ the committed plan
def stop_speed(v0, a0, A):
    """Speed of the stop of record as a function of the time since the reaction ends (the derivative of
    optA_lib_v02.brake_profile's position): ramp v0 + a0 t + jk t^2 / 2 up to t1, then v1 - A (t - t1); 0 from the stop on."""
    jk = -JERK if a0 > -A else JERK
    t1 = abs(a0 + A) / JERK
    v1 = v0 + a0 * t1 + .5 * jk * t1 * t1

    def vel(t, ts):
        if t >= ts:
            return 0.
        vv = (v0 + a0 * t + .5 * jk * t * t) if t <= t1 else (v1 - A * (t - t1))
        return max(vv, 0.)
    return vel


def plan(rw, left):
    """Positions and speeds of 'the row until tau, then the stop of record' at frames 0..n-1, n - 1 = min(J, max(left, 60)),
    J = max(60, ceil(t_end / H - 1e-9)), t_end = tau + the stop's duration; left = frames the recording holds after the decision."""
    s = np.asarray(rw['s'], float); v = np.asarray(rw['v'], float); a = np.asarray(rw['a'], float)
    v0 = float(v[JR]); a0 = float(a[JR - 1])
    pos, ts, _ = L.brake_profile(v0, a0, A_STOP)
    tend = JR * H + ts
    J = max(60, int(math.ceil(tend / H - 1e-9)))
    n = int(min(J, max(left, 60))) + 1
    vel = stop_speed(v0, a0, A_STOP)
    S = np.empty(n); V = np.empty(n)
    S[:JR + 1] = s[:JR + 1]; V[:JR + 1] = v[:JR + 1]
    for j in range(JR + 1, n):
        t = (j - JR) * H
        S[j] = s[JR] + pos(t); V[j] = vel(t, ts)
    return S, V, J, tend


def truth_window(T, k, kmax, n):
    """True frames only: for every actor present at the decision tick, its frames 0..min(n - 1, kmax - k) up to its first missing
    one. Returns [(actor id, centres (m, 2), headings (m,), half length, half width)] in the truth's order."""
    out = []
    nreal = min(n - 1, kmax - k) + 1
    for aid in list(T[k]['actors']):
        c = []; hd = []; hl = hw = None
        for j in range(nreal):
            a = T[k + j]['actors'].get(aid)
            if a is None:
                break
            c.append((a[0], a[1])); hd.append(a[2]); hl, hw = a[3], a[4]
        if c:
            out.append((aid, np.array(c, float), np.array(hd, float), hl, hw))
    return out


class Capture:
    """One run's logs: truth and logged decisions; the first loss of clearance of a (decision, row), cached."""

    def __init__(self, rd, cap):
        self.Lr = TA.load_capture(rd, cap)
        self.decs = list(TA.gc.decisions(self.Lr['cap']))
        self.rows = {}; self.done = {}

    def closing(self, i, k_expected, row):
        key = (i, row)
        if key in self.done:
            return self.done[key]
        T = self.Lr['T']; kmax = int(self.Lr['kmax']); k, dec = self.decs[i]
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
        S, V, J, tend = plan(self.rows[i][row], kmax - int(k))
        n = S.size
        ego = T[k]['ego']; u = np.array([math.cos(ego[2]), math.sin(ego[2])])
        E = TA.oc.rect_corners(ego[0] + S * u[0], ego[1] + S * u[1], ego[2], dec['ego_length'] / 2, dec['ego_width'] / 2)
        best = None; dmin = math.inf
        for aid, c, hd, hl, hw in truth_window(T, int(k), kmax, n):
            m = c.shape[0]
            D = TA.oc.poly_dist(E[:m], TA.oc.rect_corners(c[:, 0], c[:, 1], hd, hl, hw))
            dmin = min(dmin, float(D.min()))
            hit = np.nonzero(D <= 0.)[0]
            if hit.size and (best is None or int(hit[0]) < best[0]):       # earliest tick; ties: the first actor in truth order
                best = (int(hit[0]), aid)
        out = dict(found=best is not None, dmin=dmin, J=J, frames=n, t_end=tend, censored=bool(J > kmax - int(k) and tend > 3.0 + 1e-9))
        if best is not None:
            j, aid = best
            act = T[k + j]['actors'][aid]
            va = act[5] * u[0] + act[6] * u[1]
            out.update(tick=j, actor=aid, plan_speed=float(V[j]), actor_speed_along=float(va), closing=float(V[j] - va))
        self.done[key] = out
        return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--runs', type=int, default=0, help='test only: use the first N old runs')
    ap.add_argument('--logs-root', default=str(K.CD / 'runs'), help='fresh: folder holding <run>\\ with SUMMARY.json and the capture')
    ap.add_argument('--run-dir-template', default='')
    ap.add_argument('--cap-dir-template', default='')
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    t0 = time.time()
    outf = K.OUT / ('RC_D2_RS_v13' + ('_TESTOLD' if a.test_old else '') + ('_' + a.tag if a.tag else '') + '.json')
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    if a.test_old:
        runs = K.old_runs()
        if a.runs:
            runs = runs[:a.runs]
        for r in runs:
            r['dirs'] = D2.old_dirs(r['run'])
            x = np.load(EXT_OLD / (r['run'] + '.npz'), allow_pickle=False)
            if not np.array_equal(x['k'], r['k']):
                raise RuntimeError('REFUSED %s: the extended arrays do not match the decisions' % r['run'])
            r['clearX'] = L.clean_clear(x['clearX_' + KEY])
        arrays = 'revision_v11 analysis out\\ext (extended clearances of record)'
    else:
        require_stage2()
        if a.runs:
            raise SystemExit('REFUSED: --runs is a test option')
        ids = K.cases_c_lead()
        if len(ids) != 105:
            raise RuntimeError('REFUSED: %d lead-braking runs' % len(ids))
        runs = []
        for rid, case in ids:
            r = K.fresh_run(rid, need_tg=True, need_rs=False, variant_kind=None)
            r['dirs'] = D2.fresh_dirs(rid, case, a)
            x = np.load(K.ARRAYS / 'RSX' / (rid + '.npz'), allow_pickle=False)
            if not np.array_equal(x['k'], r['k']):
                raise RuntimeError('REFUSED %s: the RSX arrays do not match the decisions' % rid)
            r['clearX'] = L.clean_clear(x['clearX_' + KEY])
            runs.append(r)
        arrays = 'arrays\\RSX'
    for r in runs:
        if r['clearX'].shape != (r['ev'].size, 17):
            raise RuntimeError('REFUSED %s: clearX has shape %s' % (r['run'], r['clearX'].shape))
        r['safe'] = r['clearX'] > 0.
        r['sel'] = {s: K.grid_sel(r, s) for s in SOURCES}
    values = {}; table = {}; caps = {}
    ident = dict(n_pairs=0, max_abs_diff=0., n_above_1e9=0, n_censored=0, n_tick_beyond_60=0)
    for s in SOURCES:
        table[s] = {}
        T = np.stack([K.run_table(r, r['sel'][s], r['safe']) for r in runs]).sum(axis=0)       # (202, NST)
        with np.errstate(divide='ignore', invalid='ignore'):
            w = 100. * T[:, 1] / T[:, 0]; c = 100. * T[:, 2] / T[:, 3]
        for tgt, tk in TARGETS:
            j, nfr, ntie = D2.operating_point(c, w, tgt)
            per_run = {}; n_wg = 0; n_nofound = 0; all_cs = []
            for r in runs:
                n = r['ev'].size; ar = np.arange(n)
                sel = r['sel'][s][j]
                wg = np.nonzero(r['ev'] & ~r['safe'][ar, sel])[0]
                if wg.size == 0:
                    continue
                n_wg += int(wg.size)
                if r['run'] not in caps:
                    caps[r['run']] = Capture(*r['dirs'])
                    if len(caps[r['run']].decs) != n:
                        raise RuntimeError('REFUSED %s: %d logged decisions, %d array rows' % (r['run'], len(caps[r['run']].decs), n))
                cs = []; ticks = []
                for i in wg:
                    fresh_pair = (int(i), int(sel[i])) not in caps[r['run']].done
                    o = caps[r['run']].closing(int(i), int(r['k'][i]), int(sel[i]))
                    if fresh_pair:                                         # identity anchor, once per (decision, row)
                        d = abs(o['dmin'] - float(r['clearX'][i, sel[i]]))
                        ident['n_pairs'] += 1; ident['max_abs_diff'] = max(ident['max_abs_diff'], d)
                        ident['n_above_1e9'] += int(not d <= 1e-9); ident['n_censored'] += int(o['censored'])
                        ident['n_tick_beyond_60'] += int(o['found'] and o['tick'] > 60)
                    if o['found']:
                        cs.append(o['closing']); ticks.append(o['tick'])
                    else:
                        n_nofound += 1
                all_cs += cs
                per_run[r['run']] = dict(n_wrong_go=int(wg.size), n_with_loss_tick=len(cs),
                                         median_closing_mps=float(np.median(cs)) if cs else float('nan'),
                                         max_loss_tick=int(max(ticks)) if ticks else None)
            meds = np.array([v['median_closing_mps'] for v in per_run.values()], float)
            meds = meds[np.isfinite(meds)]
            e = dict(grid_index=j, g=float(GRID[j]), caution=float(c[j]), wrong_go=float(w[j]), n_frontier_points=nfr,
                     n_tied_nearest=ntie, n_decisions=int(round(T[j, 0])), n_wrong_go_decisions=n_wg,
                     n_wrong_go_from_table=int(round(T[j, 1])), n_runs_with_wrong_go=len(per_run),
                     n_wrong_go_without_loss_tick=n_nofound, n_runs_with_a_median=int(meds.size),
                     median_of_run_medians_mps=float(np.median(meds)) if meds.size else float('nan'),
                     median_over_decisions_mps=float(np.median(all_cs)) if all_cs else float('nan'), per_run=per_run)
            if e['n_wrong_go_decisions'] != e['n_wrong_go_from_table']:
                raise RuntimeError('REFUSED: wrong-go counts differ (%s %g)' % (s, tgt))
            table[s][tk] = e
            values['D2.%s.%s.rs.runs' % (s, tk)] = len(per_run)
            values['D2.%s.%s.rs.vclose' % (s, tk)] = float(np.median(meds)) if meds.size else None
            print('%-4s %s: g=%.4g caution=%.3f wrong go=%.3f runs with wrong go=%d median of medians=%.3f m/s (no tick: %d)'
                  % (s, tk, e['g'], e['caution'], e['wrong_go'], e['n_runs_with_wrong_go'], e['median_of_run_medians_mps'], n_nofound),
                  flush=True)
    ident['ok'] = bool(ident['n_above_1e9'] == 0)
    print('identity (smallest distance found here vs the arrays\' clearX): %d pairs, largest |diff| %.3g, above 1e-9: %d; '
          'first loss beyond tick 60: %d pairs' % (ident['n_pairs'], ident['max_abs_diff'], ident['n_above_1e9'], ident['n_tick_beyond_60']))
    doc = dict(family='D2_RS', program=PROGRAM, test_old=bool(a.test_old), model='claude-fable-5-2', values=values,
               details=dict(mode='TEST ON OLD RUNS (exploratory; not a D2 result)' if a.test_old else 'fresh lead-braking runs',
                            spec='AMENDMENT_10_v13.md sections 1 and 6 D2; CD_DEFINITIONS_v13.md D2 and the superseding note of 20 Nov 2026',
                            scoring='extended: safe iff clean_clear(clearX_%s) > 0 (rev_e2 est); caution by the 3 s commitment' % KEY,
                            arrays=arrays, n_runs=len(runs), runs=[r['run'] for r in runs], table=table,
                            identity_dmin_vs_clearX=ident, n_captures_read=len(caps)),
               written=K.clock(), seconds=time.time() - t0)
    K.write_once(outf, doc)
    print('written', outf)
    if not ident['ok']:
        raise SystemExit('STOP: the identity anchor failed (the plan or the truth window differs from the extended arrays)')


if __name__ == '__main__':
    sys.exit(main())
