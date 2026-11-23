"""Open-loop extraction: per assessment decision, the replay proof, the critical alpha of every candidate under each
margin form, and the true 3 s clearance of every candidate. Read-only on the archives; one .npz per run in <out_dir>
(written when the run is finished, so the job can be resumed: finished runs are skipped).

Usage: python -I -B -X utf8 ol_extract_v01.py <archives_root> <out_dir> <pbar_json> <part> <nparts> [run_folder ...]

Margin forms (feasible iff d >= 0 and margin^2 <= d^2), critical alpha = largest alpha at which a row is feasible:
  Fc  alpha*1 + beta0*q        Fn  alpha*p + beta0*q        Tn  alpha*(p+q)        Tm  alpha*(pbar+q)
  R4  true state: every logged actor within 4 m of a true scenario actor (primary, occluder) at `now` gets that actor's
      true position and velocity, state_time = now, P = 0  ->  alpha*q ; other logged actors unchanged (alpha*(p+q)).
  R4o same, but one logged actor per true actor (global nearest first); extra tracks on the same object keep logged state.
  R4p as R4, plus every true scenario actor that has no track within 4 m added with its true state, heading and size (P = 0).
"""
import json, math, os, pathlib, sys, time
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import olcore_v01 as oc
from olcore_v01 import consumer, finite_primitive

H = 0.05
PLAN_IDX = (19, 39, 59)   # constraint samples (offset 1) at plan time 1, 2, 3 s


def window_truth(T, k, kmax, draw, allow_extrap):
    """Per true actor: arrays over j = 0..60 of centre (61, 2), heading (61,), half length, half width.
    Returns (dict actor_id -> arrays, n_real_frames). Frames after kmax are extrapolated only if allow_extrap."""
    ids = list(T[k]['actors'])
    out = {}
    nreal = min(60, kmax - k) + 1
    for aid in ids:
        c = np.full((61, 2), np.nan); hd = np.full(61, np.nan); hl = hw = None
        last = None
        for j in range(nreal):
            a = T[k + j]['actors'].get(aid)
            if a is None:
                break
            c[j] = a[0], a[1]; hd[j] = a[2]; hl, hw = a[3], a[4]; last = j
        if last is None:
            continue
        if last < 60 and allow_extrap:
            kl = k + last
            aprev = T.get(kl - 1, {}).get('actors', {}).get(aid) or T[kl]['actors'][aid]
            alast = T[kl]['actors'][aid]
            vx, vy = aprev[5], aprev[6]; sp = math.hypot(vx, vy)
            fam = draw['family']; is_primary = (aid == T[k]['target_id'])
            pos = np.array([alast[0], alast[1]]); hd_l = alast[2]
            for j in range(last + 1, 61):
                kk = k + j - 1                      # the step from frame kk to kk + 1
                if is_primary and fam in ('stopped', 'benign'):
                    step = np.zeros(2)
                elif is_primary and fam == 'lead_braking':
                    ta = (kk + 1) * H - 5.0
                    if ta >= draw['brake_start_s']:
                        sp = max(0., sp - draw['brake_mps2'] * H)
                    step = sp * H * np.array([math.cos(hd_l), math.sin(hd_l)])
                elif sp < 0.1:
                    step = np.zeros(2)
                else:
                    step = H * np.array([vx, vy])
                pos = pos + step; c[j] = pos; hd[j] = hd_l
        out[aid] = (c, hd, hl, hw)
    return out, nreal


def clearance(rows, ego, L, W, wt, upto):
    """Min rectangle-to-rectangle distance over frames 0..upto-1 for each row and each true actor: {aid: (17,)}."""
    s = np.stack([r['s'] for r in rows])                       # (17, 61)
    u = np.array([math.cos(ego[2]), math.sin(ego[2])])
    cx = ego[0] + s * u[0]; cy = ego[1] + s * u[1]
    E = oc.rect_corners(cx, cy, ego[2], L / 2, W / 2)          # (17, 61, 4, 2)
    res = {}
    for aid, (c, hd, hl, hw) in wt.items():
        ok = np.isfinite(c[:upto, 0])
        if not ok.any():
            continue
        A = oc.rect_corners(c[:upto, 0][ok], c[:upto, 1][ok], hd[:upto][ok], hl, hw)   # (n, 4, 2)
        D = oc.poly_dist(E[:, :upto][:, ok], A[None])
        res[aid] = D.min(axis=1), D[:, 0]
    return res


def process_run(rd, PB):
    S = json.loads((rd / 'SUMMARY.json').read_text(encoding='utf-8'))
    arm = S.get('arm'); cap = oc.cap_dir(rd)
    draw = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))['case']['draw']
    ao = S.get('assessment_outcomes') or {}
    base = ao['base_frame']; fc = ao.get('first_contact_frame')
    contact_k = (fc - base - 1) if fc is not None else -1
    T = oc.load_truth(cap); Sc, roles = oc.load_scen(cap, base)
    kmax = max(T)
    react_ks = np.array(sorted(k for k, v in Sc.items() if v[0]), dtype=int)
    first_react = int(react_ks[0]) if react_ks.size else 10 ** 9
    Pb = {c: np.array(PB[c]) for c in PB}
    rec = []
    for r in oc.jl(cap / 'frames.jsonl'):
        dec = (r.get('execution') or {}).get('new_decision')
        if not dec or dec['mode'] != 'assessment':
            continue
        k = r['k']; ms = dec['model_state']; actors = dec['actors']; now = dec['now']; lo = dec['output']
        L, W = dec['ego_length'], dec['ego_width']; desired = dec['desired_mps']
        diag = consumer.Diagnostics()
        rows = finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], desired, actors, L, W, now, diag)
        n = len(rows); assert n == 17
        idx55 = next(i for i, x in enumerate(rows) if x['targets'] == (-5., -5.))
        # ---- replay proof with the run's own rule and logged alpha, beta
        rr = [dict(x, p=np.ones(np.shape(x['p']))) for x in rows] if arm == 'fixed' else rows
        out = consumer.choose(rr, dec['alpha'], dec['beta'], consumer.Diagnostics(), dec['steer'])
        ok = (out['candidate'] == lo['candidate'] and list(out['targets']) == list(lo['targets'])
              and out['fallback'] == lo['fallback'] and out['wire'].hex() == lo['wire'])
        logged_row = idx55 if lo['fallback'] else lo['candidate']
        # ---- critical alpha per row and form
        cr = {f: np.empty(n) for f in ('Fc', 'Fn', 'Tn', 'Tm', 'R4', 'R4o', 'R4p', 'LOG')}
        for i, x in enumerate(rows):
            d, p, q = x['d'], x['p'], x['q']
            cr['Fc'][i] = oc.crit_alpha(d, np.ones_like(q), oc.BETA0 * q)
            cr['Fn'][i] = oc.crit_alpha(d, p, oc.BETA0 * q)
            cr['Tn'][i] = oc.crit_alpha(d, p + q, 0.)
            cr['LOG'][i] = oc.crit_alpha(d, np.ones_like(q) if arm == 'fixed' else p, dec['beta'] * q)
        sel_log, fb_log = oc.select(cr['LOG'], dec['alpha'], idx55)
        crit_ok = (sel_log == logged_row and fb_log == lo['fallback'])
        # T-mean: every logged actor gets the class-mean covariance of its track class
        am = [dict(a, P=Pb[oc.cls_of(a['name'])]) for a in actors]
        for i, x in enumerate(rows):
            y = consumer.constraints_for_trajectory(dict(x), am, L, W, now, diag)
            cr['Tm'][i] = oc.crit_alpha(y['d'], y['p'] + y['q'], 0.)
        # ---- truth at the decision frame, matching
        tr = T.get(k); prim = tr['target_id'] if tr else None
        have_truth = tr is not None and prim is not None and prim in tr['actors']
        prim_idx = -1; prim_dist = np.nan; n_gate_prim = 0; n_many = 0; n_one = 0; rx = ry = np.nan
        a4 = [dict(a) for a in actors]; a4o = [dict(a) for a in actors]; extra = []
        if have_truth:
            order = [prim] + [a for a in tr['actors'] if a != prim]
            one, (prim_idx, prim_dist) = oc.match_actors(actors, now, tr, order)
            rx, ry = oc.to_planner(tr['ego'], tr['actors'][prim][0], tr['actors'][prim][1])
            tp = {}
            for aid in order:
                t = tr['actors'][aid]
                tp[aid] = oc.to_planner(tr['ego'], t[0], t[1]) + oc.rot_planner(tr['ego'], t[5], t[6])
            covered = set()
            for i, a in enumerate(actors):
                age = now - a['state_time']; px = a['x'] + age * a['vx']; py = a['y'] + age * a['vy']
                best = None; bd = oc.GATE_M
                for aid in order:
                    dd = math.hypot(px - tp[aid][0], py - tp[aid][1])
                    if dd < bd:
                        bd = dd; best = aid
                if best is not None:
                    n_many += 1; n_gate_prim += (best == prim); covered.add(best)
                    a4[i].update(x=tp[best][0], y=tp[best][1], vx=tp[best][2], vy=tp[best][3], state_time=now, P=np.zeros((4, 4)))
            # R4p: true scenario actors that have no track at all are added with their true state, heading and size
            for aid in order:
                if aid not in covered:
                    t = tr['actors'][aid]
                    extra.append(dict(x=tp[aid][0], y=tp[aid][1], vx=tp[aid][2], vy=tp[aid][3], yaw=t[2] - tr['ego'][2], length=2 * t[3], width=2 * t[4],
                                      P=np.zeros((4, 4)), state_time=now, sigma_acc=(1.5 if (aid == prim and draw['family'] == 'pedestrian_crossing') else 1.0),
                                      track_id=-1, name='truth'))
            for aid, (i, dd) in one.items():
                n_one += 1
                a4o[i].update(x=tp[aid][0], y=tp[aid][1], vx=tp[aid][2], vy=tp[aid][3], state_time=now, P=np.zeros((4, 4)))
        for i, x in enumerate(rows):
            y = consumer.constraints_for_trajectory(dict(x), a4, L, W, now, diag)
            cr['R4'][i] = oc.crit_alpha(y['d'], y['p'] + y['q'], 0.)
        if n_one == n_many:
            cr['R4o'][:] = cr['R4']
        else:
            for i, x in enumerate(rows):
                y = consumer.constraints_for_trajectory(dict(x), a4o, L, W, now, diag)
                cr['R4o'][i] = oc.crit_alpha(y['d'], y['p'] + y['q'], 0.)
        if not extra:
            cr['R4p'][:] = cr['R4']
        else:
            for i, x in enumerate(rows):
                y = consumer.constraints_for_trajectory(dict(x), a4 + extra, L, W, now, diag)
                cr['R4p'][i] = oc.crit_alpha(y['d'], y['p'] + y['q'], 0.)
        # ---- true clearance of every candidate over 3 s
        cl = np.full((2, n), np.inf); clx = np.full((2, n), np.inf); cl0 = np.nan; nreal = 0; status = 3
        if have_truth:
            full = (k + 60 <= kmax)
            truncated_by_contact = (not full) and contact_k >= 0
            wt, nreal = window_truth(T, k, kmax, draw, truncated_by_contact)
            status = 0 if full else (1 if truncated_by_contact else 2)   # 0 full window, 1 cut by contact, 2 end of run
            if full:
                res = clearance(rows, tr['ego'], L, W, wt, 61)
                for aid, (mn, d0) in res.items():
                    cl[0 if aid == prim else 1] = np.minimum(cl[0 if aid == prim else 1], mn)
                    if aid == prim:
                        cl0 = float(d0[0])
                clx[:] = cl
            elif truncated_by_contact:
                res = clearance(rows, tr['ego'], L, W, wt, 61)
                for aid, (mn, d0) in res.items():
                    clx[0 if aid == prim else 1] = np.minimum(clx[0 if aid == prim else 1], mn)
                    if aid == prim:
                        cl0 = float(d0[0])
                cl[:] = np.nan
            else:
                cl[:] = np.nan; clx[:] = np.nan
        else:
            cl[:] = np.nan; clx[:] = np.nan
        # ---- reaction flags
        w = react_ks[(react_ks >= k) & (react_ks <= k + 60)]
        flag_task = bool(w.size); flag_strict = bool(first_react <= k + 60)
        # ---- planner's own p, q, d for the primary's track at plan time 1, 2, 3 s in the logged-selected row
        pq = np.full((3, 3), np.nan); Pd = np.full(4, np.nan); age_p = np.nan; sig = np.nan; pname = ''
        if prim_idx >= 0:
            x = rows[logged_row]
            for m, kk in enumerate(PLAN_IDX):
                ii = prim_idx * 120 + 60 + kk
                pq[m] = x['p'][ii], x['q'][ii], x['d'][ii]
            a = actors[prim_idx]; Pd = np.diag(np.asarray(a['P'], float)); age_p = now - a['state_time']; sig = a['sigma_acc']; pname = a['name']
        rec.append(dict(k=k, n_act=len(actors), desired=desired, v0=ms['model_speed_mps'], a0=ms['model_acceleration_mps2'],
                        replay_ok=ok, crit_ok=crit_ok, logged_row=logged_row, logged_fb=bool(lo['fallback']), idx55=idx55,
                        targets=np.array([x['targets'] for x in rows]), cost=np.array([x['cost'] for x in rows]),
                        vbar=np.array([x['s'][60] / 3. for x in rows]), vend=np.array([x['v'][60] for x in rows]),
                        cFc=cr['Fc'], cFn=cr['Fn'], cTn=cr['Tn'], cTm=cr['Tm'], cR4=cr['R4'], cR4o=cr['R4o'], cR4p=cr['R4p'], n_extra=len(extra),
                        cl=cl, clx=clx, cl0=cl0, gap=(tr['gap'] if tr and tr['gap'] is not None else np.nan), nreal=nreal, status=status,
                        flag_task=flag_task, flag_strict=flag_strict, have_truth=have_truth,
                        prim_idx=prim_idx, prim_dist=prim_dist, n_gate_prim=n_gate_prim, n_many=n_many, n_one=n_one, rx=rx, ry=ry,
                        pq=pq, Pd=Pd, age_p=age_p, sig=sig, pname=pname, alpha_log=dec['alpha'], beta_log=dec['beta'],
                        exact_pred=diag.exact_predicates, ego_speed=(tr['ego_speed'] if tr else np.nan)))
    meta = dict(run=rd.name, arm=arm, knobs=S.get('knobs'), family=draw['family'], desired=draw['desired_mps'], occluder=bool(draw.get('occluder')),
                draw=draw, contact_k=contact_k, kmax=int(kmax), termination=ao.get('termination'), first_react=(first_react if first_react < 10 ** 9 else -1),
                n_react_frames=int(react_ks.size), n_dec=len(rec), status_field=S.get('status'))
    return meta, rec


def save(out_dir, meta, rec):
    keys = [k for k in rec[0]] if rec else []
    arrs = {}
    for kx in keys:
        v = [x[kx] for x in rec]
        arrs[kx] = np.array(v) if kx != 'pname' else np.array(v, dtype='U16')
    tmp = out_dir / (meta['run'] + '.tmp.npz')
    np.savez_compressed(tmp, meta=json.dumps(meta), **arrs)
    os.replace(tmp, out_dir / (meta['run'] + '.npz'))


def main():
    root = pathlib.Path(sys.argv[1]); out_dir = pathlib.Path(sys.argv[2]); PB = json.loads(pathlib.Path(sys.argv[3]).read_text(encoding='utf-8'))['Pbar']
    part, nparts = int(sys.argv[4]), int(sys.argv[5]); only = set(sys.argv[6:])
    out_dir.mkdir(parents=True, exist_ok=True)
    runs = [d for d in sorted(root.iterdir()) if d.is_dir()]
    log = out_dir / ('progress_part%d.log' % part)
    for i, rd in enumerate(runs):
        if only and rd.name not in only:
            continue
        if not only and i % nparts != part:
            continue
        if (out_dir / (rd.name + '.npz')).exists() or (out_dir / (rd.name + '.skip.json')).exists():
            continue
        t0 = time.time()
        try:
            meta, rec = process_run(rd, PB)
        except Exception as e:
            (out_dir / (rd.name + '.skip.json')).write_text(json.dumps(dict(run=rd.name, error=repr(e)[:500])), encoding='utf-8')
            msg = 'SKIP %s %s' % (rd.name, repr(e)[:200])
        else:
            if rec:
                save(out_dir, meta, rec)
                msg = '%s %-20s dec=%d replay_ok=%d crit_ok=%d status(full/contact/end/notruth)=%s %.1fs' % (
                    rd.name, meta['family'], len(rec), sum(x['replay_ok'] for x in rec), sum(x['crit_ok'] for x in rec),
                    [sum(x['status'] == s for x in rec) for s in range(4)], time.time() - t0)
            else:
                (out_dir / (rd.name + '.skip.json')).write_text(json.dumps(dict(run=rd.name, error='no assessment decisions')), encoding='utf-8')
                msg = 'SKIP %s no assessment decisions' % rd.name
        print(msg, flush=True)
        with open(log, 'a', encoding='utf-8') as f:
            f.write(time.strftime('%H:%M:%S ') + msg + '\n')


if __name__ == '__main__':
    main()
