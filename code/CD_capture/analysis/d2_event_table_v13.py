"""Revision v13, package D2 (AMENDMENT_10_v13 sec. 6, D2): the event-level table on the 105 fresh lead-braking runs.

For F0, N, CK3 and TG, at the operating points whose caution is nearest 2% and 5% of the desired speed (each source on its own step
frontier over the grid of record, pooled over the runs, all evaluated decisions), under the 3 s commitment and under reaction-and-stop
at tau = 0.75 s (6 m/s^2, jerk 12.65 m/s^3, zero gap; clearR075 of c_extract_v13.py = trk_score_v01.delayed_stop_clearance):
  (i) the number of runs with at least one wrong go;
  (ii) per run, the median closing speed at the first loss of clearance of its wrong-go decisions;
  (iii) across runs, the median of those medians (and their range).
Definitions fixed here (before any fresh value): a source's frontier points are the grid scales whose (caution, wrong go) is not
dominated (no point with caution <= and wrong go <); the operating point is the frontier point with caution nearest the target
(ties: smaller scale). Caution keeps the 3 s definition under both scorings (optA_lib_v02.stats_scored). A wrong go is an evaluated
decision whose selected row is unsafe under the scoring (true clearance <= 0 over the window). Its first loss of clearance is the first
of the 61 ticks (0.05 s) at which the ego rectangle on the committed plan (the row; or the row until 0.75 s then the stop of record)
is at distance <= 0 from a true actor (ol_extract_v01.clearance geometry, per tick; true frames only, as the scoring); the closing speed
is the plan's speed there minus the true actor's velocity along the ego heading (truth velocity of that tick), in m/s.
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\d2_event_table_v13.py [--test-old]
--test-old: the old run p1b_fit_finite_0012 and the 35 old runs' stored arrays (3 s commitment only), code test only.
"""
import argparse, json, math, pathlib, sys, time
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cd_common_v13 as CC               # noqa: E402
import trk_env_v01 as env                # noqa: E402
env.setup()
import trk_arrays_v01 as TA              # noqa: E402
import trk_score_v01 as TS               # noqa: E402
L = CC.L; C11 = CC.C11
H = 0.05; JERK = 12.65

ap = argparse.ArgumentParser(); ap.add_argument('--test-old', action='store_true')
args = ap.parse_args()
gate = CC.require_lock2(args.test_old)
t00 = time.time(); log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)
OUTF = CC.OUT / (('TESTOLD_' if args.test_old else '') + 'D2_EVENT_TABLE_v13.json')
if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)
SRC = ['F0', 'N', 'CK3', 'TG']; TARGETS = (2.0, 5.0)


def stop_velocity(v_row, a_row, tau, A, s_row):
    """Speeds at the 61 ticks of trk_score_v01.stop_profile_cont (the row until tau, then the stop of record)."""
    v = np.array(v_row, float)
    x0, v0, a0 = TS.row_state_at(s_row, v_row, a_row, tau)
    jr = -JERK if a0 > -A else JERK
    t1 = abs(-A - a0) / JERK
    ts = TS._first_stop(v0, a0, jr, t1, A)
    jj = np.arange(61); after = jj * H > tau + 1e-9
    t = np.minimum(jj[after] * H - tau, ts)
    v1 = v0 + a0 * t1 + .5 * jr * t1 ** 2
    tr = np.minimum(t, t1); th = np.maximum(t - t1, 0.)
    ramp = v0 + a0 * tr + .5 * jr * tr ** 2
    hold = v1 - A * th
    vv = np.where(t <= t1, ramp, hold)
    vv = np.where(t >= ts, 0., vv)
    v[after] = np.maximum(vv, 0.)
    return v


def first_loss(s, v, ego, Lg, Wd, wt, T, k):
    """First tick j with distance <= 0 to a true actor, and the closing speed there (plan speed - actor velocity along the heading)."""
    oc = TA.oc
    u = np.array([math.cos(ego[2]), math.sin(ego[2])])
    cx = ego[0] + s * u[0]; cy = ego[1] + s * u[1]
    E = oc.rect_corners(cx[None], cy[None], ego[2], Lg / 2, Wd / 2)[0]      # (61, 4, 2)
    best = None
    for aid, (c, hd, hl, hw) in wt.items():
        ok = np.isfinite(c[:, 0])
        for j in np.flatnonzero(ok):
            A_ = oc.rect_corners(c[j:j + 1, 0], c[j:j + 1, 1], hd[j:j + 1], hl, hw)          # (1, 4, 2)
            dist = float(oc.poly_dist(E[None, j:j + 1], A_[None])[0, 0])
            if dist <= 0.:
                if best is None or j < best[0]:
                    a = T.get(k + j, {}).get('actors', {}).get(aid)
                    va = float(u @ np.array([a[5], a[6]])) if a is not None else float('nan')
                    best = (int(j), float(v[j]) - va, aid)
                break
    return best


def operating_point(T202):
    c, w = 100. * T202[:, 2] / T202[:, 3], 100. * T202[:, 1] / T202[:, 0]
    ok = np.isfinite(c) & np.isfinite(w)
    eff = [g for g in np.flatnonzero(ok) if not np.any(ok & (c <= c[g]) & (w < w[g]))]
    out = {}
    for tg in TARGETS:
        d = np.array([abs(c[g] - tg) for g in eff]); g = eff[int(np.flatnonzero(d == d.min())[0])]
        out[tg] = dict(index=int(g), g=float(C11.GRID[g]), caution_pp=float(c[g]), wrong_go_pp=float(w[g]))
    return out


# ------------------------------------------------------------------------------------------------ runs
if args.test_old:
    runs = CC.load_old_lead(); scorings = ('3s',)
    caps = {}
    for r in runs:
        rd = pathlib.Path(r'<library folder>\archives') / r['run']
        caps[r['run']] = (rd, next(p for p in (rd / 'x' / r['run'] / 'capture').iterdir() if p.is_dir()))
else:
    # 20 Nov 03:30 EST, before Lock 2: the reaction-and-stop column is removed from this (stage-1) script. A10 sec. 1 fixes the
    # reaction-and-stop scoring "with plans judged until the stop ends" (v11 rev_e1's extended clearance); clearR075 is the 3 s
    # (61-frame) clearance. The column is computed in stage 2 from the extended arrays (arrays/RSX), frozen in FREEZE_CD_2.
    ids = CC.c_run_ids('lead_braking'); runs = CC.load_variant(ids, 'CV0'); scorings = ('3s',)
    caps = {}
    for r in runs:
        rd = CC.CD / 'runs' / r['run'] / r['run']; caps[r['run']] = (rd, next(p for p in (rd / 'capture').iterdir() if p.is_dir()))
        r['safe_x'] = {'R075': L.clean_clear(r['clearR075']) > 0.}
CACHE = {}
doc = dict(code='d2_event_table_v13.py', amendment='AMENDMENT_10_v13 sec. 6 D2', gate=gate, test_old=args.test_old, n_runs=len(runs), table={})
for sc_name in scorings:
    sc = ('W1',) if sc_name == '3s' else ('X', 'R075')
    X = C11.tables(runs, sc, SRC)
    for a in SRC:
        ops = operating_point(X[a].sum(axis=0)[:, 0, :])
        for tg, op in ops.items():
            g = op['index']; per_run = []; n_with = 0
            for r in runs:
                sel = C11.sel_of(r, a)[g]
                safe = (r['clear1'] > 0.) if sc_name == '3s' else r['safe_x']['R075']
                ar = np.arange(sel.size)
                wrong = r['ev'] & ~safe[ar, sel]
                if not wrong.any(): continue
                n_with += 1
                if r['run'] not in CACHE:
                    rd, cap = caps[r['run']]
                    Lr = TA.load_capture(rd, cap); CACHE[r['run']] = (Lr['T'], Lr['kmax'], Lr['draw'], list(TA.gc.decisions(Lr['cap'])))
                Tt, kmax, draw, decs = CACHE[r['run']]
                speeds = []
                for di in np.flatnonzero(wrong):
                    k, dec = decs[di]; ms = dec['model_state']; Lg, Wd = dec['ego_length'], dec['ego_width']
                    rows = TA.finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'],
                                                             dec['actors'], Lg, Wd, dec['now'], TA.consumer.Diagnostics())
                    row = rows[int(sel[di])]
                    if sc_name == '3s':
                        s = np.asarray(row['s'], float); v = np.asarray(row['v'], float)
                    else:
                        s = TS.stop_profile_cont(row['s'], row['v'], row['a'], 0.75, 6.0); v = stop_velocity(row['v'], row['a'], 0.75, 6.0, row['s'])
                    wt = TA.ox.window_truth(Tt, k, kmax, draw, False)[0]
                    fl = first_loss(s, v, Tt[k]['ego'], Lg, Wd, wt, Tt, k)
                    if fl is not None: speeds.append(fl[1])
                per_run.append(dict(run=r['run'], wrong_go_decisions=int(wrong.sum()), with_first_loss=len(speeds),
                                    median_closing_speed=float(np.median(speeds)) if speeds else None))
            meds = [p['median_closing_speed'] for p in per_run if p['median_closing_speed'] is not None]
            doc['table'].setdefault(sc_name, {}).setdefault(a, {})['%g%%' % tg] = dict(
                operating_point=op, runs_with_wrong_go=n_with, median_of_run_medians=float(np.median(meds)) if meds else None,
                range_of_run_medians=[float(min(meds)), float(max(meds))] if meds else None, per_run=per_run)
            log('%s %s %g%%: g=%.4g, runs with wrong go %d' % (sc_name, a, tg, op['g'], n_with))
doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
doc['code_sha256'] = {f: CC.sha(CC.HERE / f) for f in ('d2_event_table_v13.py', 'cd_common_v13.py')}
CC.write_once(OUTF, doc)
log('written ' + OUTF.name)
