"""v13 shared tracker library: decision arrays of record rebuilt from a (re-tracked) capture. New file, 19 Nov 2026 (Claude Opus 5.5).

One pass over the assessment decisions of a run computes, with the SAME expressions as the extractors of record:
  * ol_gateR_rt_extract_v02.run_arms (P\\09_redesign\\m2_decisions\\openloop; route yaw): k, evaluated (status 0), v0, des, clear,
    cl, clx, status, vbar, idx55, cF0 (with the caller's P-bar), cN, cE, prim_idx, n_act, n_match, prim_track, prim_age, prim_miss,
    ego_speed, flag_task, flag_strict.  (The learned F1 arms and the stored margin forms cR2 / cR3 are not rebuilt.)
  * oxsb_extract_v05.run_one (P\\11_ojits\\A4\\code): cNA, cQ, cA1 (= AM), cCK3, phase (truth phase of record), prebrake, lam_max.
  * a9_4a_lead_state_extract_v01.run_one (revision_v12\\analysis): lead_found, track_id, vhat, vhat_x, ahat_long, ahat_mag, age,
    v_true, nis_last, nees_v, gap_true, dx_pred0..3 (look-ahead 0, 1, 2, 3 s).
The tracker-dependent inputs are the four capture files detections.jsonl, filter_events.jsonl, filter_algebra.jsonl and
frames.jsonl. overlay(files) serves replacements for them (from trk_tracker_v01.retrack_capture) to the read-only modules of
record, which all read through olcore_v01.jl. Without an overlay the logged files are used.

    import trk_env_v01 as env; env.setup()
    import trk_arrays_v01 as A
    ov, rec = T.retrack_capture(cap, 'B1')
    with A.overlay(cap, ov):
        meta, arrs = A.extract(run_dir, cap, PB)          # PB = {'vehicle': 4x4, 'pedestrian': 4x4}
"""
import contextlib, json, math, pathlib, sys
import numpy as np
import trk_env_v01 as env

env.setup()
OPENLOOP = pathlib.Path(r'<library folder>\openloop')
if str(OPENLOOP) not in sys.path:
    sys.path.insert(0, str(OPENLOOP))
import olcore_v01 as oc                      # noqa: E402  (read-only modules of record)
import olcore_rt_v01 as rt                   # noqa: E402
import ol_gateR_core_v01 as gc               # noqa: E402
import ol_extract_v01 as ox                  # noqa: E402
import ox12_core_v01 as xc                   # noqa: E402
import oxsb_core_v01 as sb                   # noqa: E402
from olcore_v01 import consumer, finite_primitive   # noqa: E402

YAW = 'route_yaw_rh'
VMIN = 0.5           # oxsb_core_v03.VMIN
CK_A0 = 3.0          # oxsb_core_v03.CK_A0
LOOK = (0, 20, 40, 60)
OVERLAY_FILES = ('detections.jsonl', 'filter_events.jsonl', 'filter_algebra.jsonl', 'frames.jsonl')


@contextlib.contextmanager
def overlay(cap, files):
    """Serve records for the named capture files of `cap` from memory (olcore_v01.jl is the single reader of record)."""
    cap = pathlib.Path(cap).resolve()
    orig = oc.jl
    files = {k: v for k, v in files.items() if k in OVERLAY_FILES}

    def jl(path):
        p = pathlib.Path(path)
        if p.name in files and p.parent.resolve() == cap:
            return iter(files[p.name])
        return orig(path)
    oc.jl = jl
    try:
        yield
    finally:
        oc.jl = orig


def load_capture(rd, cap, yaw=YAW):
    """rx.load_run (ol_gateR_rt_extract_v02) with an explicit run folder rd (SUMMARY.json) and capture folder."""
    rd = pathlib.Path(rd); cap = pathlib.Path(cap)
    S = json.loads((rd / 'SUMMARY.json').read_text(encoding='utf-8'))
    draw = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))['case']['draw']
    ao = S.get('assessment_outcomes') or {}
    base = ao['base_frame']; fc = ao.get('first_contact_frame')
    T = rt.load_truth(cap, yaw); Sc, roles = oc.load_scen(cap, base)
    react_ks = np.array(sorted(k for k, v in Sc.items() if v[0]), dtype=int)
    return dict(rd=rd, cap=cap, S=S, arm=S.get('arm'), draw=draw, contact_k=(fc - base - 1) if fc is not None else -1, T=T, kmax=max(T),
                react_ks=react_ks, first_react=int(react_ks[0]) if react_ks.size else 10 ** 9, book=gc.Book(cap), base=base)


def prebrake_map(cap, base):
    at = {}
    for r in oc.jl(cap / 'scenario_frames.jsonl'):
        at[r['frame'] - base - 1] = r['request'].get('assessment_time_s')
    return at


def sh_cols(Nb, vel, acc, t):
    """oxsb_extract_v05.sh_cols (same lines)."""
    dlt = sb.clip_disp(vel, acc, t) - t[:, None] * vel[None, :]
    out = np.zeros((Nb.shape[0], 120))
    for offset in (0, 1):
        nn = Nb[:, 60 * offset:60 * offset + 60]
        sl = slice(offset, offset + 60)
        out[:, 60 * offset:60 * offset + 60] = nn[..., 0] * dlt[sl, 0] + nn[..., 1] * dlt[sl, 1]
    return out


def rot(vec, yaw):
    ch, sh = math.cos(yaw), math.sin(yaw)
    return np.array([ch * vec[0] + sh * vec[1], -sh * vec[0] + ch * vec[1]])


def extract(rd, cap, PB, lead=True, a4=True):
    """All decision arrays of one run (see the module text). PB: class -> 4x4 P-bar (F0 of the tracker variant)."""
    Lr = load_capture(rd, cap)
    T = Lr['T']; book = Lr['book']; draw = Lr['draw']; kmax = Lr['kmax']; contact_k = Lr['contact_k']; cap = Lr['cap']
    react_ks = Lr['react_ks']; first_react = Lr['first_react']
    hist = xc.Hist(cap); nis = sb.NIS(cap, hist.det_time)
    decs = list(gc.decisions(cap))
    nd = len(decs)
    at = prebrake_map(cap, Lr['base'])
    # CK3 support / gate (oxsb_ctl_extract_v02 pass 1, as in oxsb_extract_v05)
    info = {}
    if a4:
        for di, (k, dec) in enumerate(decs):
            tr = T.get(k); ego = tr['ego'] if tr is not None else None
            for oi, a in enumerate(dec['actors']):
                ah = sb.a_hat_vec(hist, int(a['track_id']), a['state_time'])
                if ego is None or not np.any(ah):
                    continue
                mu, vel, t = sb.actor_mu(a, dec['now'])
                sp = math.hypot(vel[0], vel[1])
                d = dict(vel=vel, t=t, gate=sp > VMIN)
                if d['gate']:
                    d['u'] = np.asarray(vel, float) / sp
                info[(di, oi)] = d
    rec = []
    A4K = ('cNA', 'cQ', 'cA1', 'cCK3')
    a4o = {key: np.full((nd, 17), np.nan) for key in A4K}
    prebrake = np.zeros(nd, bool); lam_max = np.full(nd, np.nan); phase = np.full(nd, 3, np.int8)
    LF = {key: np.full(nd, np.nan) for key in ('vhat', 'vhat_x', 'ahat_long', 'ahat_mag', 'age', 'v_true', 'nis_last', 'nees_v',
                                               'gap_true', 'now', 'dx_pred0', 'dx_pred1', 'dx_pred2', 'dx_pred3')}
    found = np.zeros(nd, bool); tid_arr = np.full(nd, -1, np.int64)
    pmax = 0.; e_missing = 0; n_act_tot = 0; n_match_tot = 0; n_act_ev = 0; n_match_ev = 0
    for di, (k, dec) in enumerate(decs):
        ms = dec['model_state']; actors = dec['actors']; now = dec['now']
        Lg, Wd = dec['ego_length'], dec['ego_width']; desired = dec['desired_mps']
        diag = consumer.Diagnostics()
        rows = finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], desired, actors, Lg, Wd, now, diag)
        n = len(rows); assert n == 17
        idx55 = next(i for i, x in enumerate(rows) if x['targets'] == (-5., -5.))
        na = len(actors); M = 120 * na
        D = np.stack([x['d'] for x in rows]).reshape(n, M); Pr = np.stack([x['p'] for x in rows]).reshape(n, M)
        Qr = np.stack([x['q'] for x in rows]).reshape(n, M)
        N, TE, MU = gc.geometry(rows, actors, now)
        if na:
            pm = gc.s_P(N, TE, [np.asarray(a['P'], float) for a in actors])
            pmax = max(pmax, float(np.abs(pm - Pr).max()))
        Sbar = gc.s_P(N, TE, [np.array(PB[oc.cls_of(a['name'])], float) for a in actors])
        cF0 = gc.crit_rows(D, Sbar); cN = gc.crit_rows(D, Pr)
        feats = [book.features(int(a['track_id']), a['state_time']) for a in actors]
        tr = T.get(k)
        m, prim, order = gc.match_many(actors, now, tr)
        have_truth = prim is not None
        prim_idx = -1
        if have_truth:
            one, (prim_idx, prim_dist) = oc.match_actors(actors, now, tr, order)
        cl = np.full((2, n), np.inf); clx = np.full((2, n), np.inf); status = 3; wt = {}
        if have_truth:
            full = (k + 60 <= kmax)
            truncated_by_contact = (not full) and contact_k >= 0
            wt, nreal = ox.window_truth(T, k, kmax, draw, truncated_by_contact)
            status = 0 if full else (1 if truncated_by_contact else 2)
            if full:
                res = ox.clearance(rows, tr['ego'], Lg, Wd, wt, 61)
                for aid, (mn, d0) in res.items():
                    cl[0 if aid == prim else 1] = np.minimum(cl[0 if aid == prim else 1], mn)
                clx[:] = cl
            elif truncated_by_contact:
                res = ox.clearance(rows, tr['ego'], Lg, Wd, wt, 61)
                for aid, (mn, d0) in res.items():
                    clx[0 if aid == prim else 1] = np.minimum(clx[0 if aid == prim else 1], mn)
                cl[:] = np.nan
            else:
                cl[:] = np.nan; clx[:] = np.nan
        else:
            cl[:] = np.nan; clx[:] = np.nan
        SE = np.zeros((n, M)); nm = 0
        if have_truth:
            wtE = wt if status == 0 else ox.window_truth(T, k, kmax, draw, False)[0]
            cen = {}
            for oi, aid in enumerate(m):
                if aid is None:
                    continue
                nm += 1
                if aid not in cen:
                    cen[aid] = gc.planner_centres(tr['ego'], wtE[aid][0])
                    if status == 0 and not np.isfinite(cen[aid]).all():
                        e_missing += 1
                c = cen[aid]
                for offset in (0, 1):
                    c0 = 120 * oi + 60 * offset
                    e = c[offset:offset + 60] - MU[oi][offset:offset + 60]
                    nn = N[:, c0:c0 + 60]
                    s = (nn[..., 0] * e[:, 0] + nn[..., 1] * e[:, 1]) ** 2
                    SE[:, c0:c0 + 60] = np.where(np.isfinite(s), s, 0.)
        cE = gc.crit_rows(D, SE)
        n_act_tot += na; n_match_tot += nm
        if status == 0:
            n_act_ev += na; n_match_ev += nm
        pa = -1.; pmb = -1; has = 0
        for oi, aid in enumerate(m):
            if aid is not None and aid == prim:
                ag, mb = feats[oi]
                if not has or ag < pa:
                    pa, pmb = ag, mb
                has = 1
        w = react_ks[(react_ks >= k) & (react_ks <= k + 60)]
        rec.append(dict(k=k, evaluated=(status == 0), v0=ms['model_speed_mps'], des=desired,
                        clear=np.minimum(cl[0], cl[1]), vbar=np.array([x['s'][60] / 3. for x in rows]), idx55=idx55,
                        cF0=cF0, cN=cN, cE=cE, cl=cl, clx=clx, status=status, flag_task=bool(w.size), flag_strict=bool(first_react <= k + 60),
                        prim_idx=prim_idx, n_act=na, n_match=nm, prim_track=has, prim_age=pa, prim_miss=pmb,
                        ego_speed=(tr['ego_speed'] if tr else np.nan)))
        if a4:
            # ---- NA, Q, A1 (oxsb_extract_v05)
            SNA = np.zeros((n, M)); lams = []
            for oi, a in enumerate(actors):
                lam = nis.lam(int(a['track_id']), a['state_time']); lams.append(lam)
                SNA[:, 120 * oi:120 * oi + 120] = lam * Pr[:, 120 * oi:120 * oi + 120]
            lam_max[di] = max(lams) if lams else np.nan
            a4o['cNA'][di] = gc.crit_rows(D, SNA)
            ah = np.array([hist.signs(int(a['track_id']), a['state_time'])[0] for a in actors], float)
            sig = np.array([a['sigma_acc'] for a in actors], float)
            sigc = np.repeat(sig, 120); T4 = TE ** 4
            a4o['cQ'][di] = gc.crit_rows(D, Qr)
            a4o['cA1'][di] = gc.crit_rows(D, np.broadcast_to(T4 * (sigc ** 2 + np.repeat(ah, 120) ** 2) / 4, (n, M)))
            # ---- CK3 and truth phase (oxsb_extract_v05)
            m_ids = [None] * na
            if tr is not None:
                ids2, prim2, order2 = gc.match_many(actors, now, tr)
                if prim2 is not None:
                    m_ids = list(ids2)
            SH = np.zeros((n, M)); lead_speed = None
            for oi, a in enumerate(actors):
                d = info.get((di, oi))
                if d is None:
                    continue
                blk = slice(120 * oi, 120 * oi + 120)
                aid = m_ids[oi]
                if aid is not None:
                    ta = tr['actors'].get(aid)
                    if ta is not None:
                        lead_speed = math.hypot(ta[5], ta[6])
                if d['gate']:
                    SH[:, blk] = sh_cols(N[:, blk], d['vel'], -CK_A0 * d['u'], d['t'])
            if (~np.isfinite(SH)).any():
                raise RuntimeError('non-finite CK3 shift')
            a4o['cCK3'][di] = gc.crit_rows(D + SH, Sbar)
            atk = at.get(k)
            if atk is not None and draw.get('brake_start_s') is not None:
                prebrake[di] = bool(atk < draw['brake_start_s'])
            if prebrake[di]:
                phase[di] = 0
            elif lead_speed is not None:
                phase[di] = 1 if lead_speed > VMIN else 2
        if lead:
            # ---- lead track state (a9_4a_lead_state_extract_v01)
            LF['now'][di] = now
            if tr is None or prim is None:
                continue
            cand = [oi for oi, aid in enumerate(m) if aid == prim]
            if not cand:
                continue
            if len(cand) > 1:
                tp = oc.to_planner(tr['ego'], tr['actors'][prim][0], tr['actors'][prim][1])
                cand.sort(key=lambda oi: math.hypot(actors[oi]['x'] + (now - actors[oi]['state_time']) * actors[oi]['vx'] - tp[0],
                                                    actors[oi]['y'] + (now - actors[oi]['state_time']) * actors[oi]['vy'] - tp[1]))
            oi = cand[0]; a = actors[oi]; tid = int(a['track_id']); st = float(a['state_time'])
            found[di] = True; tid_arr[di] = tid
            LF['vhat'][di] = math.hypot(a['vx'], a['vy']); LF['vhat_x'][di] = a['vx']; LF['age'][di] = now - st
            ahv = sb.a_hat_vec(hist, tid, st)
            sa = hist.state_at(tid, st)
            if sa is not None:
                vw = sa[1]; sp = math.hypot(vw[0], vw[1])
                if sp > 1e-6:
                    LF['ahat_long'][di] = float((ahv[0] * vw[0] + ahv[1] * vw[1]) / sp)
            LF['ahat_mag'][di] = hist.signs(tid, st)[0]
            ta = tr['actors'][prim]
            LF['v_true'][di] = math.hypot(ta[5], ta[6])
            if hist.det_time.size:
                dj = int(np.argmin(np.abs(hist.det_time - st)))
                if abs(hist.det_time[dj] - st) < 1e-6 and tid in nis.tr:
                    hit = np.flatnonzero(nis.tr[tid][0] == dj)
                    if hit.size:
                        LF['nis_last'][di] = float(nis.tr[tid][1][hit[-1]])
            vt = rot((ta[5], ta[6]), tr['ego'][2])
            Pm = np.asarray(a['P'], float); Pvv = Pm[2:4, 2:4]
            e = np.array([a['vx'] - vt[0], a['vy'] - vt[1]])
            try:
                LF['nees_v'][di] = float(e @ np.linalg.solve(Pvv, e))
            except np.linalg.LinAlgError:
                pass
            mu, vel, t = sb.actor_mu(a, now)
            nreal = min(60, kmax - k) + 1
            cw = np.full((61, 2), np.nan)
            for j in range(nreal):
                aa = T[k + j]['actors'].get(prim) if (k + j) in T else None
                if aa is None:
                    break
                cw[j] = aa[0], aa[1]
            Cp = gc.planner_centres(tr['ego'], cw)
            LF['gap_true'][di] = Cp[0, 0] - 4.86
            for q, j in enumerate(LOOK):
                LF['dx_pred%d' % q][di] = mu[j, 0] - Cp[j, 0]
    keys = list(rec[0]) if rec else []
    arrs = {kx: np.array([x[kx] for x in rec]) for kx in keys}
    if a4:
        arrs.update(a4o); arrs.update(prebrake=prebrake, phase=phase, lam_max=lam_max)
    if lead:
        arrs.update(lead_found=found, track_id=tid_arr, **LF)
    meta = dict(family=draw['family'], desired=draw['desired_mps'], arm=Lr['arm'], n_dec=nd, contact_k=contact_k, kmax=int(kmax),
                p_rebuilt_max_abs_diff=pmax, e_true_frame_missing_in_evaluated=e_missing, n_act=n_act_tot, n_match=n_match_tot,
                n_act_evaluated=n_act_ev, n_match_evaluated=n_match_ev, knobs=Lr['S'].get('knobs'),
                nis=dict(n_updates=nis.n_upd, n_bad=nis.n_bad, mean=nis.sum_nis / nis.n_upd if nis.n_upd else None),
                book=dict(unknown=book.n_unknown, out=book.n_out, noevent=book.n_noevent, birth_mismatch=book.n_birth_mismatch,
                          dup=book.n_dup, reset=book.n_reset, miss_out=book.n_miss_out), truth_yaw=YAW)
    return meta, arrs


# ------------------------------------------------------------------------------------------------ P-bar (rule of record)
def pbar_accumulate(cap, acc=None, cnt=None):
    """ol_pbar_v01 rule on one run: at every assessment decision with a true target, the actor nearest the true primary
    (oc.match_actors, gate 4 m, simple nearest) contributes its 4x4 P to its class (vehicle / pedestrian). Reads frames through
    olcore_v01.jl (so an overlay applies). Truth: olcore_v01.load_truth (heading yaw), as the rule of record."""
    if acc is None:
        acc = {c: np.zeros((4, 4)) for c in ('vehicle', 'pedestrian')}
    if cnt is None:
        cnt = {c: 0 for c in ('vehicle', 'pedestrian')}
    T = oc.load_truth(pathlib.Path(cap))
    for r in oc.jl(pathlib.Path(cap) / 'frames.jsonl'):
        dec = (r.get('execution') or {}).get('new_decision')
        if not dec or dec['mode'] != 'assessment':
            continue
        k = r['k']; tr = T.get(k)
        if tr is None or tr['target_id'] is None or tr['target_id'] not in tr['actors']:
            continue
        _, (j, dist) = oc.match_actors(dec['actors'], dec['now'], tr, [tr['target_id']])
        if j < 0:
            continue
        a = dec['actors'][j]; c = oc.cls_of(a['name'])
        acc[c] += np.asarray(a['P'], float); cnt[c] += 1
    return acc, cnt
