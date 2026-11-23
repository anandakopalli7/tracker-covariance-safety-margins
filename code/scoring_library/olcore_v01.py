"""Shared read-only helpers for the open-loop decision measurements (m2_decisions/openloop).

Imports Codex's planner modules read-only (python -I -B: no bytecode is written anywhere).
Nothing here writes outside the caller's own output folder.
"""
import json, math, pathlib, sys
import numpy as np

assert sys.dont_write_bytecode, 'run with python -B'
CODEX = pathlib.Path(r'<library folder>\149_supported_sensor_preparation_20261101')
sys.path[:0] = [str(CODEX / 'code'), str(CODEX / 'vendor')]
import consumer  # noqa: E402
import finite_primitive  # noqa: E402

BETA0 = 0.056961122665147565
GATE_M = 4.0
FAMILIES = ('lead_braking', 'stopped', 'pedestrian_crossing', 'vehicle_crossing', 'cutin', 'benign')


def jl(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def cap_dir(run_dir):
    capr = run_dir / 'x' / run_dir.name / 'capture'
    caps = [d for d in capr.iterdir() if d.is_dir()]
    if len(caps) != 1:
        raise RuntimeError('expected one capture directory in %s, found %d' % (capr, len(caps)))
    return caps[0]


def cls_of(name):
    return 'pedestrian' if name == 'pedestrian' else 'vehicle'


def load_truth(cap):
    """k -> dict(ego=(cx, cy, heading), target_id, actors={actor_id: (cx, cy, heading, half_len, half_wid, vx_rh, vy_rh)}, gap)."""
    T = {}
    for r in jl(cap / 'evaluation_truth.jsonl'):
        e = r['ego']['derived']
        acts = {}
        for a in r.get('scenario_actors') or []:
            d = a['derived']; he = a['half_extents']; v = a['velocity_lh']
            acts[a['actor_id']] = (d['center_rh'][0], d['center_rh'][1], d['heading_rh'], he[0], he[1], v[0], -v[1])
        tg = r.get('target')
        T[r['k']] = dict(ego=(e['center_rh'][0], e['center_rh'][1], e['heading_rh']), target_id=tg['actor_id'] if tg else None,
                         actors=acts, gap=r.get('directional_gap_m'), ego_speed=math.hypot(r['ego']['velocity_lh'][0], r['ego']['velocity_lh'][1]))
    return T


def load_scen(cap, base):
    """k -> (active_reaction, reason, trigger_brake); also returns roles {actor_id: role}."""
    S = {}; roles = {}
    for r in jl(cap / 'scenario_frames.jsonl'):
        k = r['frame'] - base - 1; q = r['request']
        S[k] = (bool(q.get('active_reaction')), q.get('reason'), bool((q.get('reactive_trigger') or {}).get('brake')))
        for m in r.get('measured') or []:
            roles[m['actor_id']] = m['role']
    return S, roles


def to_planner(ego, x, y):
    dx = x - ego[0]; dy = y - ego[1]; c, s = math.cos(ego[2]), math.sin(ego[2])
    return c * dx + s * dy, -s * dx + c * dy


def rot_planner(ego, vx, vy):
    c, s = math.cos(ego[2]), math.sin(ego[2])
    return c * vx + s * vy, -s * vx + c * vy


def match_actors(actors, now, tr, order):
    """Global greedy one-to-one matching of true scenario actors (ids in `order`) to logged actors by centre distance at `now`
    in the planner frame, gate GATE_M. Returns {actor_id: (logged index, distance)}, and the simple nearest match of order[0]."""
    ego = tr['ego']; pairs = []; simple = (-1, float('nan'))
    pos = [(a['x'] + (now - a['state_time']) * a['vx'], a['y'] + (now - a['state_time']) * a['vy']) for a in actors]
    for aid in order:
        if aid not in tr['actors']:
            continue
        t = tr['actors'][aid]; rx, ry = to_planner(ego, t[0], t[1])
        ds = [math.hypot(px - rx, py - ry) for px, py in pos]
        for i, dd in enumerate(ds):
            pairs.append((dd, aid, i))
        if aid == order[0] and ds:
            j = int(np.argmin(ds)); simple = (j if ds[j] < GATE_M else -1, ds[j])
    out = {}; used = set()
    for dd, aid, i in sorted(pairs):
        if dd >= GATE_M:
            break
        if aid in out or i in used:
            continue
        out[aid] = (i, dd); used.add(i)
    return out, simple


# ---------------- rectangle geometry (independent of Codex) ----------------
def rect_corners(cx, cy, h, hl, hw):
    """Corners (..., 4, 2), counter-clockwise, of rectangles with centre (cx, cy), heading h, half length hl, half width hw."""
    cx, cy, h, hl, hw = np.broadcast_arrays(cx, cy, h, hl, hw)
    ch, sh = np.cos(h), np.sin(h)
    out = np.empty(cx.shape + (4, 2))
    for i, (sx, sy) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1))):
        out[..., i, 0] = cx + sx * hl * ch - sy * hw * sh
        out[..., i, 1] = cy + sx * hl * sh + sy * hw * ch
    return out


def _pt_seg(P, Q):
    """Min distance from the vertices P (..., 4, 2) to the edges of polygon Q (..., 4, 2)."""
    Q2 = np.roll(Q, -1, axis=-2)
    e = Q2 - Q                                   # (..., 4, 2) edges
    w = P[..., :, None, :] - Q[..., None, :, :]  # (..., 4 pts, 4 edges, 2)
    ee = np.sum(e * e, axis=-1)                  # (..., 4)
    t = np.sum(w * e[..., None, :, :], axis=-1) / np.maximum(ee[..., None, :], 1e-300)
    t = np.clip(t, 0., 1.)
    diff = w - t[..., None] * e[..., None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=-1)).min(axis=(-1, -2))


def poly_dist(A, B):
    """Distance between convex quadrilaterals A, B (..., 4, 2); 0 when they overlap or touch."""
    sep = np.zeros(A.shape[:-2], dtype=bool)
    for Pn in (A, B):
        e = np.roll(Pn, -1, axis=-2) - Pn
        nrm = np.stack([-e[..., 1], e[..., 0]], axis=-1)        # (..., 4, 2)
        pa = np.einsum('...id,...jd->...ij', nrm, A); pb = np.einsum('...id,...jd->...ij', nrm, B)
        sep |= ((pa.max(-1) < pb.min(-1)) | (pb.max(-1) < pa.min(-1))).any(-1)
    d = np.minimum(_pt_seg(A, B), _pt_seg(B, A))
    return np.where(sep, d, 0.)


def crit_alpha(d, A, B):
    """Largest alpha for which  alpha*A + B <= d^2  and  d >= 0  hold for every constraint (-inf: never; +inf: always)."""
    if d.size == 0:
        return math.inf
    if (d < 0).any():
        return -math.inf
    num = d * d - B
    if (num < 0).any():
        return -math.inf
    pos = A > 0
    if not pos.any():
        return math.inf
    return float(np.min(num[pos] / A[pos]))


def select(crits, alpha, idx55):
    """Row index selected at alpha (first row in cost order with crit >= alpha), and fallback flag."""
    for i, c in enumerate(crits):
        if c >= alpha:
            return i, False
    return idx55, True
