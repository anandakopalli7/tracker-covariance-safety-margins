"""Revision v13, package D2 (AMENDMENT_10_v13 sec. 6, D2), STAGE 2: the event-level table's reaction-and-stop column on the 105 fresh
lead-braking runs. New file, 20 Nov 2026, 04:00 EST (Claude Opus 5.5), before Lock 2; frozen in FREEZE_CD_2 (two-stage Lock 2).

Why a separate script: A10 sec. 1 fixes "the reaction-and-stop scoring, with plans judged until the stop ends", i.e. v11's extended
clearance (revision_v11/analysis/rev_e1_extended_truth_extract_v01.py; safe iff clearX > 0, rev_e2's 'est'), not the 61-frame clearance
the stage-1 D2 script had used (CD_DEFINITIONS_v13.md, "Superseded 20 Nov").

For F0, N, CK3 and TG, at the operating points whose caution is nearest 2% and 5% (each source on its own step frontier over the grid
of record, pooled over the runs, all evaluated decisions; caution keeps the 3 s definition, optA_lib_v02.stats_scored), under
reaction-and-stop at tau = 0.75 s, 6 m/s^2 (r157 profile of record, jerk 12.65 m/s^3), judged until the stop ends:
  (i) the number of runs with at least one wrong go; (ii) per run, the median closing speed at the first loss of clearance of its
  wrong-go decisions; (iii) across runs, the median of those medians (and their range).
Operating point, wrong go and ties exactly as d2_event_table_v13.py. The committed plan is rev_e1's: the row until tau, then
oxsb_replan_v03.replan_s(row, j_react, 6.0, 'r157') to tick 60 and s[j_react] + pos((j - j_react) * 0.05) beyond it, up to the stop's end
J = max(60, ceil(t_stop / 0.05)) (true frames only; a pair whose recording ends first is judged on the frames that exist). The first
loss of clearance is the first tick j <= J at which the ego rectangle is at distance <= 0 from a true actor (rev_e1's geometry); the
closing speed is the plan's speed there (the row's speed up to j_react, then the analytic derivative of brake_profile's position,
0 from the stop on) minus the actor's truth velocity along the ego heading at that tick.
Inputs: fresh: arrays/CV0 (decisions, critical scales) and arrays/RSX/<rid>.npz (clearX_t0p75_a6p0, written by x_rsx_extract_v13.py, a
port of rev_e1); old-run test: revision_v11/analysis/out/ext/<run>.npz. Identity check in both: for every wrong-go decision, the minimum
over ticks 0..J of the distance recomputed here equals clearX of the selected row (|diff| <= 1e-9 m; reported).
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\d2_rs_v13.py [--test-old]   (fresh: requires LOCK_A10_2 and LOCK_A10_2c)
"""
import argparse, json, math, pathlib, sys, time
import numpy as np
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cd_common_v13 as CC               # noqa: E402
import trk_env_v01 as env                # noqa: E402
env.setup()
import trk_arrays_v01 as TA              # noqa: E402
P = pathlib.Path(r'<library folder>')
sys.path.insert(0, str(P / '11_ojits' / 'A5' / 'code'))
import oxsb_replan_v03 as rp             # noqa: E402  (read-only; the reaction-and-stop profile of record, as rev_e1)
L = CC.L; C11 = CC.C11; oc = rp.oc
H = rp.H; TAU, AMAX = 0.75, 6.0; KK = rp.vkey(TAU, AMAX)          # 't0p75_a6p0'
EXT_OLD = pathlib.Path(r'ARS_TRIAL\revision_v11\analysis\out\ext')
SRC = ['F0', 'N', 'CK3', 'TG']; TARGETS = (2.0, 5.0)

ap = argparse.ArgumentParser(); ap.add_argument('--test-old', action='store_true')
args = ap.parse_args()
gate = CC.require_lock2c(args.test_old)
t00 = time.time(); log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)
OUTF = CC.OUT / (('TESTOLD_' if args.test_old else '') + 'D2_RS_v13.json')
if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)


def window_truth_ext(T, k, kmax, nfr):
    """rev_e1_extended_truth_extract_v01.window_truth_ext, verbatim: nfr frames, true frames only."""
    out = {}
    nreal = min(nfr - 1, kmax - k) + 1
    for aid in list(T[k]['actors']):
        c = np.full((nfr, 2), np.nan); hd = np.full(nfr, np.nan); hl = hw = None; last = None
        for j in range(nreal):
            a = T[k + j]['actors'].get(aid)
            if a is None:
                break
            c[j] = a[0], a[1]; hd[j] = a[2]; hl, hw = a[3], a[4]; last = j
        if last is None:
            continue
        out[aid] = (c, hd, hl, hw)
    return out


def plan(row, left):
    """rev_e1's continued reaction-and-stop plan of one row: positions S[0..nfr-1], speeds, J (stop end), nfr."""
    jr = rp.j_of(TAU)
    sR, inf_ = rp.replan_s(row, jr, AMAX, 'r157')
    pos, t_stop, _ = rp.brake_profile(inf_['v0'], inf_['a0'], AMAX)
    s0 = float(np.asarray(row['s'], float)[jr]); tst = jr * H + t_stop
    jend = max(60, int(math.ceil(tst / H - 1e-9)))
    nfr = int(min(jend, max(left, 60))) + 1
    S = np.empty(nfr); S[:min(61, nfr)] = sR[:min(61, nfr)]
    for j in range(61, nfr):
        S[j] = s0 + pos((j - jr) * H)
    # speeds: the row's speed up to j_react, then d/dt of brake_profile's position (same expressions, hold=False), 0 from the stop
    v0, a0, J = inf_['v0'], inf_['a0'], rp.JERK
    sJ = -J if a0 > -AMAX else J; tau1 = abs(a0 + AMAX) / J; v1 = v0 + a0 * tau1 + sJ * tau1 ** 2 / 2.
    V = np.empty(nfr); vr = np.asarray(row['v'], float)
    for j in range(nfr):
        if j <= jr:
            V[j] = vr[j]; continue
        t = (j - jr) * H
        if t >= t_stop: V[j] = 0.; continue
        V[j] = (v0 + a0 * t + sJ * t * t / 2.) if t <= tau1 else (v1 - AMAX * (t - tau1))
    return S, np.maximum(V, 0.), jend, nfr


def first_loss_ext(S, V, jend, ego, Lg, Wd, wt, T, k):
    """First tick j <= jend with distance <= 0 to a true actor (rev_e1 geometry), closing speed there; and min distance over 0..jend."""
    nfr = S.size; u = np.array([math.cos(ego[2]), math.sin(ego[2])])
    cx = ego[0] + S * u[0]; cy = ego[1] + S * u[1]
    E = oc.rect_corners(cx[None], cy[None], ego[2], Lg / 2, Wd / 2)          # (1, nfr, 4, 2)
    Dall = np.full(nfr, np.inf); first = None
    for aid, (c, hd, hl, hw) in wt.items():
        ok = np.isfinite(c[:, 0])
        if not ok.any():
            continue
        A_ = oc.rect_corners(c[:, 0][ok], c[:, 1][ok], hd[ok], hl, hw)
        D = np.full(nfr, np.inf); D[ok] = oc.poly_dist(E[:, ok], A_[None])[0]
        Dall = np.minimum(Dall, D)
        hit = np.flatnonzero(D[:min(jend, nfr - 1) + 1] <= 0.)
        if hit.size and (first is None or hit[0] < first[0]):
            j = int(hit[0]); a = T.get(k + j, {}).get('actors', {}).get(aid)
            va = float(u @ np.array([a[5], a[6]])) if a is not None else float('nan')
            first = (j, float(V[j]) - va, aid)
    je = int(min(jend, nfr - 1))
    return first, float(Dall[:je + 1].min())


def operating_point(T202):
    c, w = 100. * T202[:, 2] / T202[:, 3], 100. * T202[:, 1] / T202[:, 0]
    ok = np.isfinite(c) & np.isfinite(w)
    eff = [g for g in np.flatnonzero(ok) if not np.any(ok & (c <= c[g]) & (w < w[g]))]
    out = {}
    for tg in TARGETS:
        d = np.array([abs(c[g] - tg) for g in eff]); g = eff[int(np.flatnonzero(d == d.min())[0])]
        out[tg] = dict(index=int(g), g=float(C11.GRID[g]), caution_pp=float(c[g]), wrong_go_pp=float(w[g]))
    return out


# ------------------------------------------------------------------------------------------------ runs and the extended safe set
caps = {}
if args.test_old:
    runs = CC.load_old_lead()
    for r in runs:
        rd = P / '07_fit_runs' / 'archives' / r['run']
        caps[r['run']] = (rd, next(p for p in (rd / 'x' / r['run'] / 'capture').iterdir() if p.is_dir()))
        x = np.load(EXT_OLD / (r['run'] + '.npz'), allow_pickle=False)
        if not np.array_equal(x['k'], r['k']): raise SystemExit('REFUSED: v11 ext decisions differ for ' + r['run'])
        r['clearX'] = x['clearX_' + KK]
else:
    ids = CC.c_run_ids('lead_braking'); runs = CC.load_variant(ids, 'CV0')
    for r in runs:
        rd = CC.CD / 'runs' / r['run'] / r['run']; caps[r['run']] = (rd, next(p for p in (rd / 'capture').iterdir() if p.is_dir()))
        x = np.load(CC.CD / 'arrays' / 'RSX' / (r['run'] + '.npz'), allow_pickle=False)
        if not np.array_equal(x['k'], r['k']): raise SystemExit('REFUSED: RSX decisions differ for ' + r['run'])
        r['clearX'] = x['clearX_' + KK]
for r in runs:
    r['safe_x'] = {'est': L.clean_clear(r['clearX']) > 0.}
doc = dict(code='d2_rs_v13.py', stage=2, amendment='AMENDMENT_10_v13 sec. 6 D2 (reaction-and-stop column; sec. 1: judged until the stop ends)',
           gate=gate, test_old=args.test_old, n_runs=len(runs), scoring='reaction-and-stop tau 0.75 s, 6 m/s^2, extended (rev_e1 clearX, est)',
           table={}, identity=dict(n_checked=0, max_abs_diff_min_distance_vs_clearX=0.0))
X = C11.tables(runs, ('X', 'est'), SRC)
cache = {}; idmax = 0.; nchk = 0
for a in SRC:
    ops = operating_point(X[a].sum(axis=0)[:, 0, :])
    for tg, op in ops.items():
        g = op['index']; per_run = []; n_with = 0
        for r in runs:
            sel = C11.sel_of(r, a)[g]; ar = np.arange(sel.size)
            wrong = r['ev'] & ~r['safe_x']['est'][ar, sel]
            if not wrong.any(): continue
            n_with += 1
            if r['run'] not in cache:
                rd, cap = caps[r['run']]
                Lr = TA.load_capture(rd, cap); cache[r['run']] = (Lr['T'], Lr['kmax'], list(TA.gc.decisions(Lr['cap'])))
            Tt, kmax, decs = cache[r['run']]
            speeds = []
            for di in np.flatnonzero(wrong):
                k, dec = decs[di]; ms = dec['model_state']; Lg, Wd = dec['ego_length'], dec['ego_width']
                rows = TA.finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'],
                                                         dec['actors'], Lg, Wd, dec['now'], TA.consumer.Diagnostics())
                row = rows[int(sel[di])]
                S, V, jend, nfr = plan(row, int(kmax - k))
                wt = window_truth_ext(Tt, k, kmax, nfr)
                fl, dmin = first_loss_ext(S, V, jend, Tt[k]['ego'], Lg, Wd, wt, Tt, k)
                cx_ = float(r['clearX'][di, int(sel[di])])
                if np.isfinite(cx_) or np.isfinite(dmin):
                    idmax = max(idmax, abs(dmin - cx_) if (np.isfinite(cx_) and np.isfinite(dmin)) else float('inf')); nchk += 1
                if fl is not None: speeds.append(fl[1])
            per_run.append(dict(run=r['run'], wrong_go_decisions=int(wrong.sum()), with_first_loss=len(speeds),
                                median_closing_speed=float(np.median(speeds)) if speeds else None))
        meds = [p['median_closing_speed'] for p in per_run if p['median_closing_speed'] is not None]
        doc['table'].setdefault('RS075', {}).setdefault(a, {})['%g%%' % tg] = dict(
            operating_point=op, runs_with_wrong_go=n_with, median_of_run_medians=float(np.median(meds)) if meds else None,
            range_of_run_medians=[float(min(meds)), float(max(meds))] if meds else None, per_run=per_run)
        log('RS075 %s %g%%: g=%.4g, runs with wrong go %d' % (a, tg, op['g'], n_with))
doc['identity'] = dict(n_checked=nchk, max_abs_diff_min_distance_vs_clearX=idmax, passes=bool(idmax <= 1e-9))
if idmax > 1e-9:
    log('IDENTITY FAILED: recomputed minimum distance differs from clearX by %.3g m' % idmax)
doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
doc['code_sha256'] = {f: CC.sha(CC.HERE / f) for f in ('d2_rs_v13.py', 'cd_common_v13.py')}
CC.write_once(OUTF, doc)
log('written %s; identity %s (%d checked, max %.3g m)' % (OUTF.name, doc['identity']['passes'], nchk, idmax))
