"""Package F (revision v13), steps 04 and 05: the class averages P-bar of a tracker on the design split, and the decision
arrays of every scene. New file, 19 Nov 2026 (Claude Opus 5.5). Adapter: f03_adapter_v01.py.

mode pbar   (design split only): per decision (all built decisions of the train scenes), the truth actors present at `now` are
            matched one-to-one to the tracker's actors (olcore_v01.match_actors: global greedy by centre distance in the planner
            frame at `now`, actor position advanced to `now` with its velocity, gate 4 m); each matched actor's 4 x 4 planner-
            frame P is accumulated by class (olcore cls_of of the track name). P-bar = sum / count (ol_pbar_v01.py's rule, with
            every truth actor in place of the scenario's one primary, which nuScenes does not have). Writes
            out\\PBAR_<tracker>_train_v01.json.
mode arrays (needs that P-bar file): per scene, cache\\arrays_<tracker>\\<split>\\<scene>.npz with, per built decision:
            sweep, kf, now, age (now - keyframe time), v_raw, a_raw, v0, des, evaluated (3 s), evaluated2 (2 s), idx55, vbar
            (n,17), targets (n,17,2), clear / clear2 (n,17; NaN when not evaluated), clear_logged / clear_logged2 (the ego's own
            logged motion; adapter check), l_ego, n_act, n_truth, n_match, inpath (a truth vehicle with 0 < x <= 60 m and
            |y| <= 1.75 m at `now`), and critical scales cF0, cN, cE, cTG (3 s constraints) and cF0_2, cN_2, cE_2, cTG_2
            (constraints at plan times <= 2 s). meta: counts, excluded decisions, identity-check results.
Identity (every scene, decisions whose index in the scene is a multiple of ID_EVERY): the planner library itself
(finite_primitive.build_library with the actor dicts, consumer's p and d) and gc.crit_rows give cN and cF0 equal to the
vectorised values within relative 1e-12 (same +-inf pattern), D within 1e-9 m absolute, and project() equals project_brute().
Gate: require_split.
Usage: python -I f05_arrays_v01.py pbar|arrays <tracker> <split> <nproc> [scene ...]
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402  (before numpy)
import json, multiprocessing as mp, time, traceback   # noqa: E402
import numpy as np                           # noqa: E402
import f03_adapter_v01 as AD                 # noqa: E402

ID_EVERY = 100
PBAR_FILE = FC.OUT / 'PBAR_{tracker}_train_v01.json'
INPATH_X = 60.
INPATH_Y = 1.75
VEHICLE_CLASSES = ('car', 'truck', 'bus', 'trailer', 'motorcycle', 'bicycle')


def planner_mods():
    FC.setup_planner()
    import consumer, finite_primitive
    return consumer, finite_primitive


def keyframe_actors(sc, tr, kf, consumer):
    """The tracker's actors of keyframe kf in absolute route coordinates (s, l) with planner-frame vectors, yaws and P."""
    m = tr['trk_kf'] == kf
    c = tr['trk_center'][m][:, :2]
    s, l, th = sc.project(c)
    vel = AD.rot_vec(tr['trk_vel'][m], th)
    P9 = tr['trk_P'][m]
    P4 = np.array([consumer.covariance4(P9[i], th[i]) for i in range(P9.shape[0])]).reshape(-1, 4, 4)
    names = [str(x) for x in tr['trk_name'][m]]
    return dict(s=s, l=l, vx=vel[:, 0], vy=vel[:, 1], yaw=tr['trk_yaw'][m] - th, length=tr['trk_size'][m][:, 1],
                width=tr['trk_size'][m][:, 0], state_time=tr['trk_state_time'][m], P=P4, name=names,
                sigma_acc=np.array([1.5 if n in ('pedestrian', 'bicycle') else 1. for n in names]), track_id=tr['trk_id'][m])


def truth_planner(sc, now, s_e, nframes=61):
    ids, cen, yw, hl, hw = sc.truth_window(now, nframes)
    n = ids.size
    tc = np.full((n, nframes, 2), np.nan); ty = np.full((n, nframes), np.nan)
    ok = np.isfinite(cen[..., 0])
    if ok.any():
        s, l, th = sc.project(cen[ok])
        tc[ok] = np.column_stack([s - s_e, l]); ty[ok] = yw[ok] - th
    return ids, tc, ty, hl, hw


def scene_inputs(tracker, split, scene):
    FC.require_split(split)
    z = np.load(FC.CACHE / split / (scene + '.npz'), allow_pickle=False)
    tr = np.load(FC.CACHE / ('tracks_' + tracker) / split / (scene + '.npz'), allow_pickle=False)
    return AD.Scene(z), tr


def run_pbar(args):
    tracker, split, scene = args
    if split != 'train':
        raise RuntimeError('REFUSED: P-bar comes from the design split only')
    consumer, finite_primitive = planner_mods()
    sc, tr = scene_inputs(tracker, split, scene)
    acc = {'vehicle': np.zeros((4, 4)), 'pedestrian': np.zeros((4, 4))}; cnt = {'vehicle': 0, 'pedestrian': 0}
    names = {}; nd = 0; nex = 0
    cache = {}
    for j, kf in sc.decision_sweeps():
        now = float(sc.sw_t[j]); v = float(sc.v[j])
        if v < -0.1 or v > 20.:
            nex += 1; continue
        nd += 1
        if kf not in cache:
            cache[kf] = keyframe_actors(sc, tr, kf, consumer)
        A = cache[kf]
        s_e = sc.project(sc.ego_c[j:j + 1])[0][0]
        ids, tc, ty, hl, hw = truth_planner(sc, now, s_e, 1)
        if A['s'].size == 0 or ids.size == 0:
            continue
        age = now - A['state_time']
        pred = np.column_stack([A['s'] - s_e + age * A['vx'], A['l'] + age * A['vy']])
        mt = AD.match_one_to_one(pred, tc[:, 0])
        for ti, ai in mt.items():
            c = AD.cls_of(A['name'][ai])
            acc[c] += A['P'][ai]; cnt[c] += 1
            names[A['name'][ai]] = names.get(A['name'][ai], 0) + 1
    return scene, dict(acc={k: v.tolist() for k, v in acc.items()}, cnt=cnt, names=names, n_dec=nd, n_excluded=nex)


def run_arrays(args):
    tracker, split, scene, PB = args
    out = FC.CACHE / ('arrays_' + tracker) / split / (scene + '.npz')
    if out.exists():
        return scene, 'exists'
    try:
        t0 = time.time()
        consumer, finite_primitive = planner_mods()
        sc, tr = scene_inputs(tracker, split, scene)
        PBm = {c: np.asarray(PB[c], float) for c in PB}
        last = float(sc.kf_t[-1])
        recs = []; nex = 0; cache = {}
        idc = dict(n=0, crit_pattern_differ=0, crit_max_rel=0., d_max_abs=0., proj_max_abs=0., lib_errors=0)
        for di, (j, kf) in enumerate(sc.decision_sweeps()):
            now = float(sc.sw_t[j]); v_raw = float(sc.v[j]); a_raw = float(sc.a[j])
            if v_raw < -0.1 or v_raw > 20.:
                nex += 1; continue
            v0 = max(0., v_raw)
            if kf not in cache:
                cache[kf] = keyframe_actors(sc, tr, kf, consumer)
            A = cache[kf]
            s_e, l_e, th_e = (x[0] for x in sc.project(sc.ego_c[j:j + 1]))
            rows = finite_primitive.build_library(v0, a_raw, sc.desired, [], AD.EGO_L, AD.EGO_W, now, consumer.Diagnostics())
            assert len(rows) == 17
            idx55 = next(i for i, x in enumerate(rows) if x['targets'] == (-5., -5.))
            Srows = np.stack([r['s'] for r in rows])
            act = dict(x=A['s'] - s_e, y=A['l'], vx=A['vx'], vy=A['vy'], yaw=A['yaw'], length=A['length'], width=A['width'],
                       state_time=A['state_time'])
            na = act['x'].size
            ev3 = now + 3. <= last + 1e-9; ev2 = now + 2. <= last + 1e-9
            ids, tc, ty, hl, hw = truth_planner(sc, now, s_e, 61)
            # matching at now (tool's match_many, no primary)
            age = now - act['state_time']
            pred = np.column_stack([act['x'] + age * act['vx'], act['y'] + age * act['vy']])
            mm = AD.match_many(pred, tc[:, 0]) if ids.size else np.full(na, -1)
            matched = mm >= 0
            TC = np.full((na, 61, 2), np.nan)
            TC[matched] = tc[mm[matched]]
            D, Nn, TE, MU = AD.constraints(rows, act, now)
            S_N = AD.s_matrix(Nn, TE, A['P'])
            Pbar = np.array([PBm[AD.cls_of(n)] for n in A['name']]).reshape(-1, 4, 4)
            S_F0 = AD.s_matrix(Nn, TE, Pbar)
            S_E = AD.s_true(Nn, MU, TC, matched)
            S_TG = AD.s_timegap(rows, na)
            rec = dict(sweep=j, kf=kf, now=now, age=now - float(sc.kf_t[kf]), v_raw=v_raw, a_raw=a_raw, v0=v0, des=sc.desired,
                       evaluated=ev3, evaluated2=ev2, idx55=idx55, vbar=np.array([r['s'][60] / 3. for r in rows]),
                       targets=np.array([r['targets'] for r in rows], float), l_ego=l_e, n_act=na, n_truth=int(ids.size),
                       n_match=int(matched.sum()))
            for key, S in (('F0', S_F0), ('N', S_N), ('E', S_E), ('TG', S_TG)):
                rec['c' + key] = AD.crit(D, S)
                rec['c' + key + '_2'] = AD.crit(D, S, AD.MASK2)
            # in-path lead vehicle at now
            veh = np.array([sc.t_cls[i] in VEHICLE_CLASSES for i in ids], bool) if ids.size else np.zeros(0, bool)
            x0 = tc[:, 0, 0] if ids.size else np.zeros(0); y0 = tc[:, 0, 1] if ids.size else np.zeros(0)
            rec['inpath'] = bool(np.any(veh & (x0 > 0.) & (x0 <= INPATH_X) & (np.abs(y0) <= INPATH_Y)))
            # clearances (truth only)
            rec['clear'] = AD.clearance_rows(Srows, tc, ty, hl, hw, 61) if ev3 else np.full(17, np.nan)
            rec['clear2'] = AD.clearance_rows(Srows, tc, ty, hl, hw, 41) if ev2 else np.full(17, np.nan)
            # the ego's logged motion (adapter check): its own box along its logged centres and yaw
            lc, ly = sc.ego_logged_window(now, 61)
            LX = np.full(61, np.nan); LY = np.full(61, np.nan); LH = np.full(61, np.nan)
            okl = np.isfinite(lc[:, 0])
            if okl.any():
                ls_, ll_, lth = sc.project(lc[okl])
                LX[okl] = ls_ - s_e; LY[okl] = ll_; LH[okl] = ly[okl] - lth
            rec['clear_logged'] = float(AD.clearance_rows(LX[None], tc, ty, hl, hw, 61, LY, LH)[0]) if ev3 else np.nan
            rec['clear_logged2'] = float(AD.clearance_rows(LX[None], tc, ty, hl, hw, 41, LY, LH)[0]) if ev2 else np.nan
            # identity sample against the planner library itself
            if di % ID_EVERY == 0 and na:
                identity(rows, act, A, Pbar, now, v0, a_raw, sc, consumer, finite_primitive, rec, idc, tc)
                if ev3:
                    cb = clearance_brute(Srows, tc, ty, hl, hw, 61)
                    lb_ = clearance_brute(LX[None], tc, ty, hl, hw, 61, LY, LH)
                    dif = np.concatenate([np.abs(cb - rec['clear'])[np.isfinite(cb)], np.abs(lb_ - rec['clear_logged'])[np.isfinite(lb_)]])
                    idc['clear_max_abs'] = max(idc.get('clear_max_abs', 0.), float(dif.max()) if dif.size else 0.)
                    idc['clear_inf_differ'] = idc.get('clear_inf_differ', 0) + int((np.isfinite(cb) != np.isfinite(rec['clear'])).sum())
            recs.append(rec)
        keys = list(recs[0]) if recs else []
        arr = {k: np.array([r[k] for r in recs]) for k in keys}
        meta = dict(scene=scene, split=split, tracker=tracker, n_dec=len(recs), n_excluded_speed=nex, desired=sc.desired,
                    n_vertices=sc.n_vertices, identity=idc, seconds=round(time.time() - t0, 1), location=sc.meta['location'])
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix('.tmp.npz')
        np.savez_compressed(tmp, meta=json.dumps(meta), **arr)
        tmp.replace(out)
        return scene, 'ok dec=%d excl=%d id=%s %.1fs' % (len(recs), nex, json.dumps(idc), meta['seconds'])
    except Exception as e:
        return scene, 'ERROR %r %s' % (e, traceback.format_exc()[-1500:])


def clearance_brute(S_rows, tc, ty, hl, hw, nframes, ego_y=None, ego_h=None):
    """Reference for the identity sample: every (row, truth actor, frame) pair, no pruning."""
    R = S_rows.shape[0]; out = np.full(R, np.inf)
    ey = np.zeros(nframes) if ego_y is None else ego_y; eh = np.zeros(nframes) if ego_h is None else ego_h
    for r in range(R):
        for j in range(nframes):
            ok = np.isfinite(tc[:, j, 0])
            if not ok.any() or not np.isfinite(S_rows[r, j]):
                continue
            E = AD.rect_corners(S_rows[r, j], ey[j], eh[j], AD.EGO_L / 2., AD.EGO_W / 2.)
            Aq = AD.rect_corners(tc[ok, j, 0], tc[ok, j, 1], ty[ok, j], hl[ok], hw[ok])
            out[r] = min(out[r], float(AD.poly_dist(np.broadcast_to(E, Aq.shape), Aq).min()))
    return out


def crit_rows_ref(D, S):
    """ol_gateR_core_v01.crit_rows (verbatim copy; the reference of the identity check)."""
    R, M = D.shape
    if M == 0:
        return np.full(R, np.inf)
    bad = (D < 0).any(axis=1)
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = np.where(S > 0, (D * D) / np.where(S > 0, S, 1.), np.inf)
    return np.where(bad, -np.inf, ratio.min(axis=1))


def identity(rows, act, A, Pbar, now, v0, a0, sc, consumer, finite_primitive, rec, idc, tc):
    acts = []
    for i in range(act['x'].size):
        acts.append(dict(x=float(act['x'][i]), y=float(act['y'][i]), vx=float(act['vx'][i]), vy=float(act['vy'][i]),
                         yaw=float(act['yaw'][i]), length=float(act['length'][i]), width=float(act['width'][i]),
                         state_time=float(act['state_time'][i]), sigma_acc=float(A['sigma_acc'][i]), P=A['P'][i],
                         track_id=int(A['track_id'][i]), name=A['name'][i]))
    try:
        lib = finite_primitive.build_library(v0, a0, sc.desired, acts, AD.EGO_L, AD.EGO_W, now, consumer.Diagnostics())
        acts0 = [dict(a, P=Pbar[i]) for i, a in enumerate(acts)]
        lib0 = finite_primitive.build_library(v0, a0, sc.desired, acts0, AD.EGO_L, AD.EGO_W, now, consumer.Diagnostics())
    except Exception:
        idc['lib_errors'] += 1
        return
    na = len(acts); M = 120 * na
    Dl = np.stack([x['d'] for x in lib]).reshape(17, M); Pl = np.stack([x['p'] for x in lib]).reshape(17, M)
    P0 = np.stack([x['p'] for x in lib0]).reshape(17, M)
    cN = crit_rows_ref(Dl, Pl); cF0 = crit_rows_ref(Dl, P0)
    for a, b in ((cN, rec['cN']), (cF0, rec['cF0'])):
        pa = np.where(np.isnan(a), 3, np.where(a == np.inf, 1, np.where(a == -np.inf, 2, 0)))
        pb = np.where(np.isnan(b), 3, np.where(b == np.inf, 1, np.where(b == -np.inf, 2, 0)))
        idc['crit_pattern_differ'] += int((pa != pb).sum())
        fin = (pa == 0) & (pb == 0)
        if fin.any():
            rel = np.abs(a[fin] - b[fin]) / np.maximum(np.maximum(np.abs(a[fin]), np.abs(b[fin])), 1e-300)
            idc['crit_max_rel'] = max(idc['crit_max_rel'], float(rel.max()))
    Dm, _, _, _ = AD.constraints(rows, act, now)
    idc['d_max_abs'] = max(idc['d_max_abs'], float(np.abs(Dm.reshape(17, M) - Dl).max()))
    pts = sc.ego_c[::7]
    s1 = np.column_stack(sc.project(pts)); s2 = np.column_stack(sc.project_brute(pts))
    idc['proj_max_abs'] = max(idc['proj_max_abs'], float(np.abs(s1 - s2).max()))
    idc['n'] += 1


def main():
    mode, tracker, split, nproc = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    FC.require_split(split)
    scenes = sys.argv[5:] or FC.splits()[split]
    if mode == 'pbar':
        if split != 'train':
            raise RuntimeError('REFUSED: P-bar comes from the design split only')
        outp = pathlib.Path(str(PBAR_FILE).format(tracker=tracker))
        if outp.exists() and not sys.argv[5:]:
            raise RuntimeError('REFUSED: %s exists' % outp)
        acc = {'vehicle': np.zeros((4, 4)), 'pedestrian': np.zeros((4, 4))}; cnt = {'vehicle': 0, 'pedestrian': 0}
        names = {}; nd = 0; nex = 0; done = []
        with mp.Pool(nproc) as pool:
            for scene, r in pool.imap_unordered(run_pbar, [(tracker, split, s) for s in scenes]):
                for c in acc:
                    acc[c] += np.asarray(r['acc'][c]); cnt[c] += r['cnt'][c]
                for k, v in r['names'].items():
                    names[k] = names.get(k, 0) + v
                nd += r['n_dec']; nex += r['n_excluded']; done.append(scene)
        res = dict(code='f05_arrays_v01.py pbar', tracker=tracker, split=split, scenes=len(done), written=FC.clock(),
                   rule='every truth actor present at now matched one-to-one (global greedy, 4 m) to the tracker actors; matched '
                        'actor P (4x4, planner frame) averaged by class (pedestrian / vehicle)',
                   n_decisions=nd, n_excluded_speed=nex, counts=cnt, names=names,
                   Pbar={c: (acc[c] / max(cnt[c], 1)).tolist() for c in acc})
        if sys.argv[5:]:
            print(FC.jdump(res)); return
        outp.write_text(FC.jdump(res), encoding='utf-8')
        print('WROTE', outp, cnt, flush=True)
        return
    PB = json.loads(pathlib.Path(str(PBAR_FILE).format(tracker=tracker)).read_text(encoding='utf-8'))['Pbar']
    log = FC.LOGS / ('f05_arrays_%s_%s_v01.log' % (tracker, split))
    with mp.Pool(nproc) as pool:
        for scene, msg in pool.imap_unordered(run_arrays, [(tracker, split, s, PB) for s in scenes]):
            with open(log, 'a', encoding='utf-8') as f:
                f.write('%s %s %s\n' % (FC.clock(), scene, msg))
    print(FC.clock(), 'finished arrays', tracker, split, len(scenes), flush=True)


if __name__ == '__main__':
    main()
