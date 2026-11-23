"""Package F (revision v13): the nuScenes adapter for the CARLA study's planner library (A10 section 8.1, route F-B).
New file, 19 Nov 2026 (Claude Opus 5.5). Library module; imported by f04 (class averages) and f05 (arrays). Spec:
notes\\ADAPTER_SPEC_F_v01.md (same rules, in words).

Route frame. The route is the ego's logged path in the scene: the centres of the ego box at the LIDAR_TOP sweeps (20 Hz),
kept as vertices when at least VERTEX_MIN m ahead of the last kept vertex along the ego's heading (standstill and reversing
add none), with the ego's yaw at each vertex as the tangent, extended straight by EXT m at both ends. A world point is
projected on the nearest segment: s = arc length, l = signed lateral offset (left +), theta = the tangent interpolated
linearly in s along the segment. The planner frame of a decision is x = s - s_ego, y = l (the ego at the origin heading
along +x, as in the CARLA study's route frame); vectors are rotated by -theta at the point's own projection, yaws reduced by
theta, and a tracker covariance is rotated with consumer.covariance4(P9, theta) (the planner library's own function).
Ego. Renault Zoe (nuScenes paper): length 4.084 m, width 1.730 m, wheelbase 2.588 m (Wikipedia infobox); the ego pose is
the rear-axle midpoint (nuScenes paper, appendix A); the box centre is taken 1.294 m ahead of it (equal overhangs: an
assumption, stated). Speed v0 and acceleration a0 at a sweep: slope and twice the curvature of a least-squares quadratic in
time fitted to the ego's signed travel over the sweeps within +-FIT_HALF s. Desired speed of a scene: the largest fitted
speed over its sweeps, clipped to [1, 20] m/s (the planner's domain).
Decisions. Every second sweep from each keyframe sweep up to the next keyframe (about 0, 0.1, ..., 0.4 s after the keyframe,
the CARLA study's 10 Hz decisions with track states aged 0-0.4 s), for keyframes WARM_KF and later (the first CARLA assessment
decision used the tracker's 9th update). A decision is built when -0.1 <= v0 <= 20 (forward_model_state's domain).
Evaluated (3 s) when now + 3 s <= the last keyframe time (truth over the whole window); 2 s likewise for the horizon rule.
Truth. Annotations of the seven nuScenes tracking classes (devkit category -> detection name), linearly interpolated (centre,
yaw by the shorter arc) between an instance's annotations in consecutive keyframes; an instance's window stops at the first
time without such a pair. Truth actors of a decision: the instances with truth at `now` (the CARLA rule: actors present at
the decision tick).
Sources (constraints exactly as consumer.constraints_for_trajectory, vectorised; identity checked in f05 against the library):
  N    the track's own P;  F0  the class average P-bar of its class (olcore cls_of: pedestrian / vehicle), design split;
  E    squared true error along the constraint normal for tracks matched (nearest true centre within 4 m at `now`, the
       Gate R tool's match_many without a primary) and s = 0 otherwise or where the true frame is missing;
  TG   s = (r0 + v_e)^2, r0 = 2 m/s (A9-7);
  each critical scale = ol_gateR_core_v01.crit_rows(D, S) over all constraints (3 s) or the constraints at plan times <= 2 s.
Clearance: min rectangle distance over frames 0..60 (or 0..40) between each row's ego box (x = s_j, y = 0, heading 0) and each
truth actor's box in the planner frame (olcore_v01 rect_corners / poly_dist, copied), exact (pairs pruned only when a
centre-distance lower bound exceeds the smallest centre distance).
"""
import math
import numpy as np

EGO_L = 4.084
EGO_W = 1.730
REAR_TO_CENTRE = 2.588 / 2.
VERTEX_MIN = 0.25
EXT = 400.
KNN = 24
FIT_HALF = 0.5
WARM_KF = 8
DEC_STEP = 2
H = 0.05
TIMES = np.arange(61) * H
GATE_M = 4.0
R0_TG = 2.0
TRACK_CLASSES = ('car', 'truck', 'bus', 'trailer', 'motorcycle', 'bicycle', 'pedestrian')
# nuscenes-devkit eval/detection/utils.py category_to_detection_name (the seven tracking classes only)
CAT_TO_CLASS = {'vehicle.bicycle': 'bicycle', 'vehicle.bus.bendy': 'bus', 'vehicle.bus.rigid': 'bus', 'vehicle.car': 'car',
                'vehicle.motorcycle': 'motorcycle', 'human.pedestrian.adult': 'pedestrian', 'human.pedestrian.child': 'pedestrian',
                'human.pedestrian.construction_worker': 'pedestrian', 'human.pedestrian.police_officer': 'pedestrian',
                'vehicle.trailer': 'trailer', 'vehicle.truck': 'truck'}


def wrap(a):
    return (np.asarray(a) + np.pi) % (2. * np.pi) - np.pi


def quat_yaw(q):
    """Yaw of nuScenes quaternions (w, x, y, z): rotation of the box x axis about z."""
    q = np.asarray(q, float)
    w, x, y, z = q[..., 0], q[..., 1], q[..., 2], q[..., 3]
    return np.arctan2(2. * (w * z + x * y), 1. - 2. * (y * y + z * z))


def cls_of(name):
    """olcore_v01.cls_of."""
    return 'pedestrian' if name == 'pedestrian' else 'vehicle'


# ------------------------------------------------------------------------------------------------ ego and route
class Scene:
    """Ego motion, route and truth of one cached scene (cache\\<split>\\<scene>.npz)."""

    def __init__(self, z):
        self.z = z
        self.meta = __import__('json').loads(str(z['meta']))
        self.sw_t = z['sw_t']; self.kf_t = z['kf_t']; self.sw_kf = z['sw_kf']
        yaw = quat_yaw(z['ego_q'])
        self.ego_yaw = np.unwrap(yaw)
        rear = z['ego_xyz'][:, :2]
        self.ego_c = rear + REAR_TO_CENTRE * np.column_stack([np.cos(yaw), np.sin(yaw)])
        self._kinematics()
        self._route()
        self._truth()

    # ---- ego kinematics
    def _kinematics(self):
        c = self.ego_c; yw = self.ego_yaw; t = self.sw_t
        d = np.diff(c, axis=0); hm = 0.5 * (yw[1:] + yw[:-1])
        ds = d[:, 0] * np.cos(hm) + d[:, 1] * np.sin(hm)
        self.travel = np.concatenate([[0.], np.cumsum(ds)])
        n = len(t); v = np.empty(n); a = np.empty(n)
        for i in range(n):
            m = np.abs(t - t[i]) <= FIT_HALF + 1e-9
            tt = t[m] - t[i]; ss = self.travel[m]
            A = np.column_stack([np.ones(tt.size), tt, tt * tt])
            coef = np.linalg.lstsq(A, ss, rcond=None)[0]
            v[i] = coef[1]; a[i] = 2. * coef[2]
        self.v = v; self.a = a
        self.desired = float(min(20., max(1., float(np.max(v)))))

    # ---- route
    def _route(self):
        c = self.ego_c; yw = self.ego_yaw
        vx = [c[0]]; vt = [yw[0]]
        for i in range(1, len(c)):
            dlt = c[i] - vx[-1]
            if math.hypot(dlt[0], dlt[1]) >= VERTEX_MIN and dlt[0] * math.cos(yw[i]) + dlt[1] * math.sin(yw[i]) > 0.:
                vx.append(c[i]); vt.append(yw[i])
        vx = np.array(vx); vt = np.array(vt)
        u0 = np.array([math.cos(vt[0]), math.sin(vt[0])]); u1 = np.array([math.cos(vt[-1]), math.sin(vt[-1])])
        P = np.vstack([vx[0] - EXT * u0, vx, vx[-1] + EXT * u1]); T = np.concatenate([[vt[0]], vt, [vt[-1]]])
        seg = np.diff(P, axis=0); ln = np.hypot(seg[:, 0], seg[:, 1])
        self.rP = P; self.rT = T; self.rseg = seg; self.rlen = ln; self.rS = np.concatenate([[0.], np.cumsum(ln)])
        self.n_vertices = len(vx)

    def _project_on(self, Q, cand):
        """Projection of Q (m, 2) on the candidate segments cand (m, c) (indices into the segment list): the nearest, lowest
        segment index on ties."""
        A = self.rP[:-1][cand]; seg = self.rseg[cand]; ln2 = (self.rlen ** 2)[cand]          # (m, c, 2) / (m, c)
        w = Q[:, None, :] - A
        tau = np.clip((w[..., 0] * seg[..., 0] + w[..., 1] * seg[..., 1]) / ln2, 0., 1.)
        cx = A[..., 0] + tau * seg[..., 0]; cy = A[..., 1] + tau * seg[..., 1]
        dd = (Q[:, None, 0] - cx) ** 2 + (Q[:, None, 1] - cy) ** 2
        dmin = dd.min(axis=1)
        big = np.iinfo(np.int64).max
        i = np.where(dd == dmin[:, None], cand, big).min(axis=1)
        col = np.argmax(cand == i[:, None], axis=1); r = np.arange(Q.shape[0])
        tt = tau[r, col]
        ux = self.rseg[i, 0] / self.rlen[i]; uy = self.rseg[i, 1] / self.rlen[i]
        ex = Q[:, 0] - cx[r, col]; ey = Q[:, 1] - cy[r, col]
        s = self.rS[i] + tt * self.rlen[i]
        l = ux * ey - uy * ex
        th = self.rT[i] + tt * (self.rT[i + 1] - self.rT[i])
        return s, l, th

    def project_brute(self, Q):
        """Reference: every segment is a candidate."""
        Q = np.asarray(Q, float).reshape(-1, 2)
        nseg = self.rseg.shape[0]
        return self._project_on(Q, np.broadcast_to(np.arange(nseg), (Q.shape[0], nseg)))

    def project(self, Q):
        """World points Q (m, 2) -> s, l, theta (each (m,)). Candidates: the segments at the KNN nearest route points (the
        vertices and the two far extension ends) and both extension segments; equal to project_brute when the nearest
        segment touches one of those points (checked against project_brute in f05's identity sample)."""
        Q = np.asarray(Q, float).reshape(-1, 2)
        if Q.shape[0] == 0:
            return np.zeros(0), np.zeros(0), np.zeros(0)
        if not hasattr(self, '_tree'):
            from scipy.spatial import cKDTree
            self._tree = cKDTree(self.rP)
        nseg = self.rseg.shape[0]
        k = min(KNN, self.rP.shape[0])
        _, vi = self._tree.query(Q, k=k)
        vi = np.asarray(vi).reshape(Q.shape[0], k)
        cand = np.concatenate([vi - 1, vi, np.zeros((Q.shape[0], 1), int), np.full((Q.shape[0], 1), nseg - 1)], axis=1)
        cand = np.clip(cand, 0, nseg - 1)
        return self._project_on(Q, cand)

    # ---- truth
    def _truth(self):
        z = self.z
        cls = np.array([CAT_TO_CLASS.get(str(c), '') for c in z['ann_cat']])
        keep = cls != ''
        self.ann_cls = cls
        ninst = int(z['ann_inst'].max()) + 1 if z['ann_inst'].size else 0
        nk = len(self.kf_t)
        self.t_xy = np.full((ninst, nk, 2), np.nan); self.t_yaw = np.full((ninst, nk), np.nan)
        self.t_hl = np.full((ninst, nk), np.nan); self.t_hw = np.full((ninst, nk), np.nan)
        self.t_link = np.zeros((ninst, nk), bool)             # annotated at kf and at kf + 1, linked
        self.t_cls = np.array([''] * ninst, dtype='U16')
        yaw = quat_yaw(z['ann_q'])
        for r in np.nonzero(keep)[0]:
            ii = z['ann_inst'][r]; k = z['ann_kf'][r]
            self.t_xy[ii, k] = z['ann_xyz'][r, :2]; self.t_yaw[ii, k] = yaw[r]
            self.t_hw[ii, k] = z['ann_wlh'][r, 0] / 2.; self.t_hl[ii, k] = z['ann_wlh'][r, 1] / 2.
            self.t_cls[ii] = cls[r]
            nx = z['ann_next'][r]
            if nx >= 0 and z['ann_kf'][nx] == k + 1:
                self.t_link[ii, k] = True
        self.t_inst = np.nonzero(self.t_cls != '')[0]

    def truth_window(self, now, nframes=61):
        """Instances with truth at `now`, and their world centres (n, nframes, 2), yaws (n, nframes), half length, half width
        (from the bracketing earlier annotation at `now`); NaN after the first frame without truth."""
        kt = self.kf_t; nk = len(kt)
        ts = now + TIMES[:nframes]
        i = np.searchsorted(kt, ts, side='right') - 1
        i = np.clip(i, 0, nk - 1)
        exact = np.isclose(ts, kt[i], rtol=0., atol=1e-9)
        nxt = np.minimum(i + 1, nk - 1)
        w = np.where(exact | (i == nk - 1), 0., (ts - kt[i]) / np.where(nxt > i, kt[nxt] - kt[i], 1.))
        ids = self.t_inst
        okk = np.isfinite(self.t_xy[ids][:, i, 0]) & (exact[None, :] | self.t_link[ids][:, i])
        okk &= ~((~exact[None, :]) & (i[None, :] == nk - 1))
        present = okk[:, 0]
        ids = ids[present]; okk = okk[present]
        brk = np.cumprod(okk, axis=1).astype(bool)
        x0 = self.t_xy[ids][:, i]; x1 = self.t_xy[ids][:, nxt]
        cen = x0 + w[None, :, None] * np.where(np.isfinite(x1), x1 - x0, 0.)
        y0 = self.t_yaw[ids][:, i]; y1 = self.t_yaw[ids][:, nxt]
        yw = y0 + w[None, :] * np.where(np.isfinite(y1), wrap(y1 - y0), 0.)
        cen[~brk] = np.nan; yw[~brk] = np.nan
        k0 = i[0]
        return ids, cen, yw, self.t_hl[ids, k0], self.t_hw[ids, k0]

    # ---- decisions
    def decision_sweeps(self):
        """(sweep index, keyframe index) of every decision of the scene."""
        out = []
        kfs = np.nonzero(self.sw_kf >= 0)[0]
        for kk, j0 in enumerate(kfs):
            kf = int(self.sw_kf[j0])
            if kf < WARM_KF:
                continue
            j1 = kfs[kk + 1] if kk + 1 < len(kfs) else j0 + 1
            for j in range(j0, j1, DEC_STEP):
                out.append((j, kf))
        return out

    def ego_logged_window(self, now, nframes=61):
        """The ego's logged centre (nframes, 2) and yaw over now + 0.05 j (linear in time between sweeps; NaN past the last
        sweep)."""
        ts = now + TIMES[:nframes]
        ok = ts <= self.sw_t[-1] + 1e-9
        x = np.interp(ts, self.sw_t, self.ego_c[:, 0]); y = np.interp(ts, self.sw_t, self.ego_c[:, 1])
        yw = np.interp(ts, self.sw_t, self.ego_yaw)
        c = np.column_stack([x, y]); c[~ok] = np.nan; yw = np.where(ok, yw, np.nan)
        return c, yw


# ------------------------------------------------------------------------------------------------ planner-frame transforms
def to_planner_points(scene, Q, s_ego):
    s, l, th = scene.project(Q)
    return np.column_stack([s - s_ego, l]), th


def rot_vec(v, th):
    c, s = np.cos(th), np.sin(th)
    return np.column_stack([c * v[:, 0] + s * v[:, 1], -s * v[:, 0] + c * v[:, 1]])


# ------------------------------------------------------------------------------------------------ geometry copies
def rect_corners(cx, cy, h, hl, hw):
    """olcore_v01.rect_corners (same expressions)."""
    cx, cy, h, hl, hw = np.broadcast_arrays(cx, cy, h, hl, hw)
    ch, sh = np.cos(h), np.sin(h)
    out = np.empty(cx.shape + (4, 2))
    for i, (sx, sy) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1))):
        out[..., i, 0] = cx + sx * hl * ch - sy * hw * sh
        out[..., i, 1] = cy + sx * hl * sh + sy * hw * ch
    return out


def _pt_seg(P, Q):
    """olcore_v01._pt_seg (same expressions)."""
    Q2 = np.roll(Q, -1, axis=-2)
    e = Q2 - Q
    w = P[..., :, None, :] - Q[..., None, :, :]
    ee = np.sum(e * e, axis=-1)
    t = np.sum(w * e[..., None, :, :], axis=-1) / np.maximum(ee[..., None, :], 1e-300)
    t = np.clip(t, 0., 1.)
    diff = w - t[..., None] * e[..., None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=-1)).min(axis=(-1, -2))


def poly_dist(A, B):
    """olcore_v01.poly_dist (same expressions)."""
    sep = np.zeros(A.shape[:-2], dtype=bool)
    for Pn in (A, B):
        e = np.roll(Pn, -1, axis=-2) - Pn
        nrm = np.stack([-e[..., 1], e[..., 0]], axis=-1)
        pa = np.einsum('...id,...jd->...ij', nrm, A); pb = np.einsum('...id,...jd->...ij', nrm, B)
        sep |= ((pa.max(-1) < pb.min(-1)) | (pb.max(-1) < pa.min(-1))).any(-1)
    d = np.minimum(_pt_seg(A, B), _pt_seg(B, A))
    return np.where(sep, d, 0.)


FIRST_K = 12


def clearance_rows(S_rows, tc, tyaw, thl, thw, nframes, ego_y=None, ego_h=None, drop_behind=False):
    """Per row: min distance over frames 0..nframes-1 between the ego box (x = S_rows[r, j], y = ego_y[j] (default 0), heading
    ego_h[j] (default 0)) and every truth box (centres tc (n, 61, 2), yaw tyaw (n, 61) in the planner frame; NaN = no truth;
    ego frames with NaN x are skipped). +inf without truth. Exact: the rectangle distance is computed for the FIRST_K pairs
    with the smallest centre-distance lower bound (centre distance minus both circumradii), then for every other pair whose
    lower bound is below the smallest distance found; a pair whose lower bound is not below it cannot attain the minimum.
    drop_behind (departure of 19 Nov 2026, notes\\F_DEPARTURE_CLEARANCE_v01.md; default False = the clearance of record): an
    (actor, frame) pair is dropped when the actor's centre has a negative longitudinal coordinate in the ego frame at that frame,
    x_rel = cos(h) (c_x - e_x) + sin(h) (c_y - e_y) < 0 (ego centre (e_x, e_y), heading h; rows: h = 0, e_y = 0); x_rel = 0 is
    kept. A dropped pair gets an infinite lower bound, so it is never evaluated; +inf when no pair remains."""
    R = S_rows.shape[0]
    out = np.full(R, np.inf)
    if tc.shape[0] == 0:
        return out
    c = tc[:, :nframes]; yw = tyaw[:, :nframes]
    ok = np.isfinite(c[..., 0])
    if not ok.any():
        return out
    ai, fj = np.nonzero(ok)
    cx = c[ai, fj, 0]; cy = c[ai, fj, 1]; yv = yw[ai, fj]; hl = thl[ai]; hw = thw[ai]
    ey = np.zeros(nframes) if ego_y is None else np.asarray(ego_y, float)[:nframes]
    eh = np.zeros(nframes) if ego_h is None else np.asarray(ego_h, float)[:nframes]
    rad_e = math.hypot(EGO_L / 2., EGO_W / 2.); rad_a = np.hypot(hl, hw)
    ex = S_rows[:, fj]                                                    # (R, m)
    cd = np.hypot(ex - cx[None, :], ey[fj][None, :] - cy[None, :])
    lb = np.where(np.isfinite(cd), cd - rad_e - rad_a[None, :], np.inf)
    if drop_behind:
        ehp = eh[fj]
        xr = np.cos(ehp)[None, :] * (cx[None, :] - ex) + (np.sin(ehp) * (cy - ey[fj]))[None, :]
        lb = np.where(xr < 0., np.inf, lb)
    A = rect_corners(cx, cy, yv, hl, hw)                                   # (m, 4, 2)
    m = cx.size; K = min(FIRST_K, m)
    order = np.argsort(lb, axis=1, kind='stable')
    first = order[:, :K]                                                   # (R, K)
    rr = np.repeat(np.arange(R), K); pp = first.ravel()
    fin = np.isfinite(lb[rr, pp])
    best = np.full(R, np.inf)
    if fin.any():
        rr1 = rr[fin]; pp1 = pp[fin]
        E = rect_corners(ex[rr1, pp1], ey[fj[pp1]], eh[fj[pp1]], EGO_L / 2., EGO_W / 2.)
        np.minimum.at(best, rr1, poly_dist(E, A[pp1]))
    if m > K:
        rest = order[:, K:]
        lr = np.take_along_axis(lb, rest, axis=1)
        sel = lr < best[:, None]
        if sel.any():
            rr2 = np.nonzero(sel)[0]; pp2 = rest[sel]
            E = rect_corners(ex[rr2, pp2], ey[fj[pp2]], eh[fj[pp2]], EGO_L / 2., EGO_W / 2.)
            np.minimum.at(best, rr2, poly_dist(E, A[pp2]))
    return best


# ------------------------------------------------------------------------------------------------ constraints (vectorised)
def support_v(n, yaw, hl, hw):
    """design_core_v85.support for arrays: hl |n . a| + hw |n . b|, a = (cos yaw, sin yaw), b = (-sin yaw, cos yaw)."""
    ca = np.cos(yaw); sa = np.sin(yaw)
    return hl * np.abs(n[..., 0] * ca + n[..., 1] * sa) + hw * np.abs(n[..., 0] * (-sa) + n[..., 1] * ca)


def constraints(rows, act, now):
    """The planner library's constraints for all rows and actors at once.
    rows: list of 17 row dicts (s, v); act: dict of arrays x, y, vx, vy, yaw, length, width, state_time (A,).
    Returns D (R, A, 2, 60), N normals (R, A, 60, 2), TE (A, 2, 60), MU (A, 61, 2)."""
    R = len(rows); A = act['x'].shape[0]
    S = np.stack([r['s'] for r in rows]); V = np.stack([r['v'] for r in rows])          # (R, 61)
    age = now - act['state_time']
    t = TIMES[None, :] + age[:, None]                                                     # (A, 61)
    MU = np.stack([act['x'][:, None] + t * act['vx'][:, None], act['y'][:, None] + t * act['vy'][:, None]], axis=-1)
    ego = np.stack([S, np.zeros_like(S)], axis=-1)                                        # (R, 61, 2)
    mid = .5 * (MU[None, :, :-1] + MU[None, :, 1:] - ego[:, None, :-1] - ego[:, None, 1:])   # (R, A, 60, 2)
    lens = np.linalg.norm(mid, axis=-1)
    valid = lens > 1e-12
    Nn = np.where(valid[..., None], mid / np.where(valid, lens, 1.)[..., None], np.array([1., 0.]))
    shapes = support_v(Nn, 0., EGO_L / 2, EGO_W / 2) + support_v(Nn, act['yaw'][None, :, None], act['length'][None, :, None] / 2,
                                                                   act['width'][None, :, None] / 2)
    spd = np.hypot(act['vx'], act['vy'])
    reserve = (np.maximum(V[:, :-1], V[:, 1:])[:, None, :] + spd[None, :, None]) * H / 2 + .01          # (R, A, 60)
    D = np.empty((R, A, 2, 60)); TE = np.empty((A, 2, 60))
    for off in (0, 1):
        dmu = MU[None, :, off:off + 60] - ego[:, None, off:off + 60]
        D[:, :, off] = (dmu[..., 0] * Nn[..., 0] + dmu[..., 1] * Nn[..., 1]) - shapes - reserve
        TE[:, off] = t[:, off:off + 60]
    return D, Nn, TE, MU


def s_matrix(Nn, TE, P):
    """z' P z per constraint, one 4x4 P per actor (A, 4, 4); floored at 0. Shape (R, A, 2, 60)."""
    R, A = Nn.shape[:2]
    out = np.empty((R, A, 2, 60))
    for off in (0, 1):
        te = TE[None, :, off, :]                                                          # (1, A, 60)
        z = np.stack([Nn[..., 0], Nn[..., 1], Nn[..., 0] * te, Nn[..., 1] * te], axis=-1)  # (R, A, 60, 4)
        out[:, :, off] = np.sum(np.matmul(z, P[None]) * z, axis=-1)
    return np.maximum(out, 0.)


def s_true(Nn, MU, TC, matched):
    """E: squared true error along the normal; TC (A, 61, 2) true centres in the planner frame of each actor's matched truth
    (NaN rows for unmatched actors); s = 0 where unmatched or the true frame is missing."""
    R, A = Nn.shape[:2]
    out = np.zeros((R, A, 2, 60))
    for off in (0, 1):
        e = TC[:, off:off + 60] - MU[:, off:off + 60]                                     # (A, 60, 2)
        s = (Nn[..., 0] * e[None, :, :, 0] + Nn[..., 1] * e[None, :, :, 1]) ** 2
        s = np.where(np.isfinite(s), s, 0.)
        s[:, ~matched] = 0.
        out[:, :, off] = s
    return out


def s_timegap(rows, A, r0=R0_TG):
    """TG (A9-7): s = (r0 + v_e)^2, v_e the row's speed at the constraint's sample (column j of offset 0 at sample j, of offset
    1 at sample j + 1)."""
    V = np.stack([r['v'] for r in rows])
    out = np.empty((len(rows), A, 2, 60))
    out[:, :, 0] = ((r0 + V[:, :60]) ** 2)[:, None, :]
    out[:, :, 1] = ((r0 + V[:, 1:61]) ** 2)[:, None, :]
    return out


MASK2 = np.zeros((2, 60), bool)
MASK2[0, :41] = True              # offset 0, column k at sample k: plan time <= 2 s  <=>  k <= 40
MASK2[1, :40] = True              # offset 1, column k at sample k + 1: k + 1 <= 40


def crit(D, S, mask=None):
    """ol_gateR_core_v01.crit_rows over the (A, 2, 60) constraints of each row (optionally only where mask (2, 60))."""
    R = D.shape[0]
    if D.shape[1] == 0:
        return np.full(R, np.inf)
    if mask is not None:
        D = D[:, :, mask]; S = S[:, :, mask]
    Df = D.reshape(R, -1); Sf = S.reshape(R, -1)
    bad = (Df < 0).any(axis=1)
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = np.where(Sf > 0, (Df * Df) / np.where(Sf > 0, Sf, 1.), np.inf)
    return np.where(bad, -np.inf, ratio.min(axis=1))


def match_many(pred_xy, truth_xy):
    """ol_gateR_core_v01.match_many without a primary: each actor's position at `now` gets the nearest true centre closer
    than 4 m (order of the truth list breaks ties: first wins); -1 if none."""
    out = np.full(pred_xy.shape[0], -1)
    if truth_xy.shape[0] == 0 or pred_xy.shape[0] == 0:
        return out
    d = np.hypot(pred_xy[:, None, 0] - truth_xy[None, :, 0], pred_xy[:, None, 1] - truth_xy[None, :, 1])
    j = np.argmin(d, axis=1)
    ok = d[np.arange(len(j)), j] < GATE_M
    out[ok] = j[ok]
    return out


def match_one_to_one(pred_xy, truth_xy):
    """olcore_v01.match_actors (global greedy one-to-one by centre distance, gate 4 m): {truth index: actor index}."""
    pairs = []
    for ti in range(truth_xy.shape[0]):
        ds = np.hypot(pred_xy[:, 0] - truth_xy[ti, 0], pred_xy[:, 1] - truth_xy[ti, 1])
        for ai, dd in enumerate(ds):
            pairs.append((float(dd), ti, ai))
    out = {}; used = set()
    for dd, ti, ai in sorted(pairs):
        if dd >= GATE_M:
            break
        if ti in out or ai in used:
            continue
        out[ti] = ai; used.add(ai)
    return out
