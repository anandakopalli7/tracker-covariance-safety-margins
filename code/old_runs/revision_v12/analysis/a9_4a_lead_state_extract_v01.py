"""Revision v12, AMENDMENT_09 A9-4(a) (review items R18, S18; input of A9-3(b)): the lead track's estimated state per decision.
New file, 19 Nov 2026. Read-only on the logs and on the project; writes only out/lead/<run>.npz and a summary.

Per decision of the 35 evaluation runs (all decisions; the analysis selects the evaluated ones):
  lead_found    a logged actor matched to the true lead (gc.match_many, as the A4 extraction's phase uses it)
  vhat, vhat_x  the lead track's speed and its longitudinal (route-frame x) velocity as passed to the planner (m/s)
  ahat_long     the track's acceleration estimate (sb.a_hat_vec: velocity change between its last two birth/update states)
                projected on the direction of its latest output velocity (world frame; m/s^2; NaN if that speed < 1e-6)
  ahat_mag      the AM source's a-hat (xc.Hist.signs(...)[0], unsigned)
  age           now - state_time (s)
  v_true        the true lead speed at the decision (m/s)
  dx_pred{0,1,2,3}  predicted minus true longitudinal position of the lead centre at look-ahead 0, 1, 2, 3 s from the decision
                (planner frame; the planner's constant-velocity prediction from the state time; true centres from the log;
                positive: the lead is predicted further ahead than it is, so the planner sees more room than there is)
  nis_last      the position-block NIS of the lead track's update at its state time (NaN if that step was not an update)
  nees_v        normalised velocity error at the decision: e' Pvv^-1 e, e = logged minus true velocity (route frame), Pvv the
                logged velocity block (2 dof)
  gap_true      true longitudinal centre distance minus 4.86 m (one car length; ego and lead are the same model)
Identity: the decision ticks equal the stored k; the phase array is read from the A4 extraction (not recomputed).
Usage: python -B -X utf8 a9_4a_lead_state_extract_v01.py
"""
import json, math, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
P = pathlib.Path(r'<library folder>')
OJ = P / '11_ojits'
sys.path.insert(0, str(OJ / 'A4' / 'code'))
import oxsb_extract_v05 as ex                # noqa: E402
c3 = ex.c3; sb = ex.sb; gc = ex.gc; rx = ex.rx; oc = ex.oc; xc = ex.xc

OUTD = HERE / 'out' / 'lead'
OUTD.mkdir(parents=True, exist_ok=True)
SUMMARY = HERE / 'out' / 'A9_4A_LEAD_EXTRACT_SUMMARY_v01.json'
if SUMMARY.exists():
    sys.exit('REFUSED: %s exists' % SUMMARY)
A4X = OJ / 'A4' / 'fit' / 'extract'
FIT_RUNS = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
LOOK = (0, 20, 40, 60)


def rot(vec, yaw):
    ch, sh = math.cos(yaw), math.sin(yaw)
    return np.array([ch * vec[0] + sh * vec[1], -sh * vec[0] + ch * vec[1]])


def run_one(run):
    Lr = rx.load_run('fit', run, sb.YAW); T = Lr['T']; cap = Lr['cap']; kmax = Lr['kmax']
    hist = xc.Hist(cap); nis = sb.NIS(cap, hist.det_time)
    z = np.load(c3.STORED / (run + '.npz'), allow_pickle=False)
    x4 = np.load(A4X / (run + '.npz'), allow_pickle=False)
    decs = list(gc.decisions(cap))
    ks = np.array([k for k, _ in decs], dtype=np.int64)
    if not (ks.shape == z['k'].shape and (ks == z['k']).all()):
        raise RuntimeError('decisions differ from the stored k')
    nd = len(decs)
    f = {key: np.full(nd, np.nan) for key in ('vhat', 'vhat_x', 'ahat_long', 'ahat_mag', 'age', 'v_true', 'nis_last', 'nees_v',
                                               'gap_true', 'now', 'dx_pred0', 'dx_pred1', 'dx_pred2', 'dx_pred3')}
    found = np.zeros(nd, bool); tid_arr = np.full(nd, -1, np.int64)
    for di, (k, dec) in enumerate(decs):
        now = dec['now']; f['now'][di] = now
        tr = T.get(k)
        if tr is None:
            continue
        actors = dec['actors']
        ids, prim, order = gc.match_many(actors, now, tr)
        if prim is None:
            continue
        cand = [oi for oi, aid in enumerate(ids) if aid == prim]
        if not cand:
            continue
        if len(cand) > 1:
            def dist(oi):
                a = actors[oi]; age = now - a['state_time']
                tp = oc.to_planner(tr['ego'], tr['actors'][prim][0], tr['actors'][prim][1])
                return math.hypot(a['x'] + age * a['vx'] - tp[0], a['y'] + age * a['vy'] - tp[1])
            cand.sort(key=dist)
        oi = cand[0]; a = actors[oi]; tid = int(a['track_id']); st = float(a['state_time'])
        found[di] = True; tid_arr[di] = tid
        f['vhat'][di] = math.hypot(a['vx'], a['vy']); f['vhat_x'][di] = a['vx']; f['age'][di] = now - st
        ahv = sb.a_hat_vec(hist, tid, st)
        sa = hist.state_at(tid, st)
        if sa is not None:
            vw = sa[1]; sp = math.hypot(vw[0], vw[1])
            if sp > 1e-6:
                f['ahat_long'][di] = float((ahv[0] * vw[0] + ahv[1] * vw[1]) / sp)
        f['ahat_mag'][di] = hist.signs(tid, st)[0]
        ta = tr['actors'][prim]
        f['v_true'][di] = math.hypot(ta[5], ta[6])
        # NIS of the update at the state time
        if hist.det_time.size:
            dj = int(np.argmin(np.abs(hist.det_time - st)))
            if abs(hist.det_time[dj] - st) < 1e-6 and tid in nis.tr:
                hit = np.flatnonzero(nis.tr[tid][0] == dj)
                if hit.size:
                    f['nis_last'][di] = float(nis.tr[tid][1][hit[-1]])
        # velocity error, route frame (ego heading, as oxsb_core_v01.TruthParts)
        vt = rot((ta[5], ta[6]), tr['ego'][2])
        Pm = np.asarray(a['P'], float); Pvv = Pm[2:4, 2:4]
        e = np.array([a['vx'] - vt[0], a['vy'] - vt[1]])
        try:
            f['nees_v'][di] = float(e @ np.linalg.solve(Pvv, e))
        except np.linalg.LinAlgError:
            pass
        # predicted minus true longitudinal position of the lead centre
        mu, vel, t = sb.actor_mu(a, now)
        nreal = min(60, kmax - k) + 1
        cw = np.full((61, 2), np.nan)
        for j in range(nreal):
            aa = T[k + j]['actors'].get(prim) if (k + j) in T else None
            if aa is None:
                break
            cw[j] = aa[0], aa[1]
        Cp = gc.planner_centres(tr['ego'], cw)
        f['gap_true'][di] = Cp[0, 0] - 4.86
        for q, j in enumerate(LOOK):
            f['dx_pred%d' % q][di] = mu[j, 0] - Cp[j, 0]
    arrs = dict(k=ks, lead_found=found, track_id=tid_arr, phase=x4['phase'], evaluated=z['evaluated'], v0=z['v0'], **f)
    np.savez_compressed(OUTD / (run + '.npz'), meta=json.dumps(dict(run=run, code='a9_4a_lead_state_extract_v01.py')), **arrs)
    ev = z['evaluated'].astype(bool)
    return dict(run=run, n_dec=nd, n_eval=int(ev.sum()), n_found_eval=int((found & ev).sum()),
                n_nis_eval=int(np.isfinite(f['nis_last'][ev]).sum()))


t00 = time.time(); rows = []
for i, run in enumerate(FIT_RUNS):
    rows.append(run_one(run))
    print('%s (%d / %d, %.0f s): %s' % (run, i + 1, len(FIT_RUNS), time.time() - t00, rows[-1]), flush=True)
SUMMARY.write_text(json.dumps(dict(code='a9_4a_lead_state_extract_v01.py', status='post hoc, descriptive; AMENDMENT_09 A9-4(a)',
                                   runs=rows, written=time.strftime('%Y-%m-%d %H:%M:%S'), seconds=time.time() - t00), indent=1),
                   encoding='utf-8')
print('done (%.0f s)' % (time.time() - t00))
