"""Package E (A10 section 7.2): the open-loop margin sources, computed online inside the planner.

Writer: session E (Claude Opus 5.5), 19 Nov 2026. Pure functions plus one online track-history class; no CARLA import.

Every arm uses the planner's 17 rows and its fallback unchanged, and the feasibility rule of the open-loop sources:
a row is feasible iff d >= 0 and g * s_A <= d^2 on every constraint (no acceleration-allowance term: beta = 0).
This module supplies, per row, the constraint clearances d (shifted for CK3) and the margin variances s_A:

  Z      zero margin: any s with g = 0 (the arm uses F0's s and g = 0)
  F0     s = z' Pbar z, Pbar the class average of record (one 4x4 per class 'vehicle' / 'pedestrian', the class of the
         tracker label: 'pedestrian' if name == 'pedestrian' else 'vehicle'), z = [n, n te] as in the consumer
         (P\\09_redesign\\m2_decisions\\openloop\\ol_gateR_core_v01.py s_P; ol_gateR_rt_extract_v01.py L118-120)
  N      s = p, the consumer's own projection of the tracker covariance (consumer.py L88-92)
  CK3    s = s_F0 and d + SH, SH = n . (clip_disp(vel, -3 u, t) - t vel) for actors whose tracker a-hat vector (velocity
         change between the last two birth/update output states) is nonzero and whose speed exceeds 0.5 m/s; normals and
         reserve are not recomputed (11_ojits\\A4\\code\\oxsb_extract_v05.py L42-49, L74-86, L132-147)
  TG     s = (2 + v_e)^2, v_e the candidate row's own speed at the constraint's sample (revision_v12 a9_7a L60-63)
  PS     s = g_phase * s_F0, g_phase from the decision's phase (A10 2.4) and the arm's triple (grid values)
  F0_IMM, N_IMM: as F0 and N, with the IMM tracker's actors and its class average Pbar_IMM

The constraint geometry is a line-for-line copy of consumer.constraints_for_trajectory that also returns the
normals and look-ahead times it computes; test_e_sources_v01.py checks that d, p, q and tags equal the original's
bit for bit on logged decisions.
"""
import math
import numpy as np

TIMES = np.arange(61) * 0.05
ACTOR_KEYS = ['x', 'y', 'vx', 'vy', 'yaw', 'length', 'width', 'state_time', 'sigma_acc']
G_DENSE = np.concatenate([[0.], np.logspace(-2, 3, 201)])     # the 202-value grid of record
VMIN = 0.5            # CK3 gate (oxsb_core_v03.VMIN)
CK_A0 = 3.0           # CK3 deceleration (oxsb_core_v03.CK_A0)
TG_R0 = 2.0           # TG r0 (a9_7a)
PHASE_STOP_V = 0.5    # A10 2.4
PHASE_BRAKE_A = -1.0  # A10 2.4 (primary threshold)
LEAD_LATERAL_M = 1.75  # online lead selection: in-path half-width (A10 2.5 lane rule); see STATUS.md departures
SOURCES = ('Z', 'F0', 'N', 'CK3', 'TG', 'PS', 'F0_IMM', 'N_IMM', 'BRAKE')


def cls_of(name):
    return 'pedestrian' if name == 'pedestrian' else 'vehicle'


# ------------------------------------------------------------------------------------------------ constraint geometry
def constraints_full(consumer, support, tr, actors, ego_length, ego_width, now, diag):
    """consumer.constraints_for_trajectory, same statements in the same order, plus the per-constraint normal,
    look-ahead time, actor index and sample index it already computes (keys e_n, e_te, e_oi, e_j)."""
    finite_array = consumer.finite_array; check_psd = consumer.check_psd
    if not np.isfinite([ego_length, ego_width, now]).all() or min(ego_length, ego_width) <= 0: raise ValueError('Invalid ego/time')
    h = .05; times = np.arange(61) * h; ego = np.column_stack([tr['s'], np.zeros(61)])
    pc = []; qc = []; dc = []; tags = []
    en = []; ete = []; eoi = []; ej = []
    for oi, o in enumerate(actors):
        vals = finite_array([o[k] for k in ['x', 'y', 'vx', 'vy', 'yaw', 'length', 'width', 'state_time', 'sigma_acc']])
        if o['length'] <= 0 or o['width'] <= 0 or o['sigma_acc'] < 0: raise ValueError('Invalid actor shape/process noise')
        age = now - o['state_time']
        if age < 0: raise ValueError('State from future')
        P = check_psd(o['P']); vel = vals[2:4]; t = times + age
        mu = vals[:2] + t[:, None] * vel
        mid = .5 * (mu[:-1] + mu[1:] - ego[:-1] - ego[1:]); lens = np.linalg.norm(mid, axis=1)
        normals = np.zeros_like(mid); valid = lens > 1e-12
        normals[valid] = mid[valid] / lens[valid, None]; normals[~valid] = [1., 0.]
        shapes = support(normals, 0., ego_length / 2, ego_width / 2) + support(normals, o['yaw'], o['length'] / 2, o['width'] / 2)
        reserve = (np.maximum(tr['v'][:-1], tr['v'][1:]) + np.linalg.norm(vel)) * h / 2 + .01
        for offset in [0, 1]:
            te = t[offset:offset + 60]; z = np.column_stack([normals, normals * te[:, None]])
            p = np.einsum('ni,ij,nj->n', z, P, z)
            bound = 64 * np.finfo(float).eps * np.einsum('ni,ij,nj->n', np.abs(z), np.abs(P), np.abs(z))
            if (p < -bound).any(): raise ValueError('Negative projected variance beyond roundoff')
            diag.projected_roundoff += int((p < 0).sum()); p = np.maximum(p, 0.)
            q = te ** 4 * o['sigma_acc'] ** 2 / 4
            d = np.einsum('ni,ni->n', mu[offset:offset + 60] - ego[offset:offset + 60], normals) - shapes - reserve
            pc.extend(p); qc.extend(q); dc.extend(d); tags.extend((oi, k, offset) for k in range(60))
            en.append(normals); ete.append(te); eoi.append(np.full(60, oi, dtype=np.int64)); ej.append(np.arange(offset, offset + 60, dtype=np.int64))
    tr.update(p=finite_array(pc), q=finite_array(qc), d=finite_array(dc), tags=tags)
    tr['e_n'] = np.concatenate(en) if en else np.zeros((0, 2))
    tr['e_te'] = np.concatenate(ete) if ete else np.zeros(0)
    tr['e_oi'] = np.concatenate(eoi) if eoi else np.zeros(0, dtype=np.int64)
    tr['e_j'] = np.concatenate(ej) if ej else np.zeros(0, dtype=np.int64)
    return tr


# ------------------------------------------------------------------------------------------------ source variances
def s_quadratic(tr, Ps):
    """z' P z per constraint, one 4x4 per actor; the consumer's einsum per actor and offset block, floored at 0
    (ol_gateR_core_v01.s_P for one row)."""
    M = len(tr['e_te']); out = np.empty(M)
    for oi, Pm in enumerate(Ps):
        for offset in (0, 1):
            c0 = 120 * oi + 60 * offset; te = tr['e_te'][c0:c0 + 60]; nrm = tr['e_n'][c0:c0 + 60]
            z = np.column_stack([nrm, nrm * te[:, None]])
            out[c0:c0 + 60] = np.einsum('ni,ij,nj->n', z, Pm, z)
    return np.maximum(out, 0.)


def s_class_average(tr, actors, pbar):
    return s_quadratic(tr, [np.asarray(pbar[cls_of(a['name'])], dtype=float) for a in actors])


def s_time_gap(tr):
    """(r0 + v_e)^2, v_e = the row's speed at the constraint's sample (offset 0: j = 0..59, offset 1: j = 1..60)."""
    v = np.asarray(tr['v'], dtype=float)
    return (TG_R0 + v[tr['e_j']]) ** 2


def clip_disp(v, a, t):
    """oxsb_core_v01.clip_disp: displacement under constant acceleration a from velocity v, clipped at the stop."""
    v = np.asarray(v, float); a = np.asarray(a, float); t = np.asarray(t, float)
    sp = math.hypot(v[0], v[1]); tc = np.inf
    if sp > 1e-9:
        au = (a[0] * v[0] + a[1] * v[1]) / sp
        if au < 0.:
            tc = sp / (-au)
    te = np.minimum(t, tc)
    return te[:, None] * v[None, :] + 0.5 * te[:, None] ** 2 * a[None, :]


def ck3_shift(tr, actors, now, hist):
    """SH per constraint (zero for actors outside the support or the gate); returns (SH, list of shifted actor indices)."""
    M = len(tr['e_te']); SH = np.zeros(M); shifted = []
    for oi, a in enumerate(actors):
        ah = hist.a_hat_vec(int(a['track_id']), a['state_time'])
        if not np.any(ah):
            continue
        vals = np.asarray([a[k] for k in ACTOR_KEYS], dtype=np.float64)
        age = now - a['state_time']; vel = vals[2:4]; t = TIMES + age
        sp = math.hypot(vel[0], vel[1])
        if not sp > VMIN:
            continue
        u = np.asarray(vel, float) / sp
        dlt = clip_disp(vel, -CK_A0 * u, t) - t[:, None] * vel[None, :]
        for offset in (0, 1):
            c0 = 120 * oi + 60 * offset; sl = slice(offset, offset + 60); nn = tr['e_n'][c0:c0 + 60]
            SH[c0:c0 + 60] = nn[:, 0] * dlt[sl, 0] + nn[:, 1] * dlt[sl, 1]
        shifted.append(oi)
    return SH, shifted


# ------------------------------------------------------------------------------------------------ online track history
class OnlineHist:
    """ox12_core_v01.Hist built incrementally from the same records: each detector update's emitted tracks (index i =
    detector update number, 0-based) and the filter events (kind birth/update/miss keyed by (track, timestamp))."""

    def __init__(self):
        self.kind = {}; self.n_dup = 0; self.n_reset = 0; self.n_events = 0
        self.raw = {}           # tid -> dict(st, p, v, i)
        self.det_index = -1

    def add_events(self, events):
        for e in events[self.n_events:]:
            if e['kind'] in ('birth', 'update', 'miss'):
                key = (int(e['track']), int(e['timestamp']))
                if key in self.kind:
                    self.n_dup += 1
                    continue
                self.kind[key] = e['kind']
            elif e['kind'] == 'reset':
                self.n_reset += 1
        self.n_events = len(events)

    def add_tracks(self, tracks):
        self.det_index += 1; i = self.det_index
        for t in tracks:
            tid = int(t['id'])
            r = self.raw.setdefault(tid, dict(st=[], p=[], v=[], i=[]))
            r['st'].append(float(t['state_time'])); r['p'].append([float(t['center'][0]), float(t['center'][1])])
            r['v'].append([float(t['velocity'][0]), float(t['velocity'][1])]); r['i'].append(i)

    def update(self, tracks, events):
        """Call once per detector update, after tracker.step, with that update's tracks and the full event list."""
        self.add_events(events)
        self.add_tracks(tracks)
        self._cache = {}

    def _arrays(self, tid):
        cache = getattr(self, '_cache', None)
        if cache is None: cache = self._cache = {}
        if tid in cache:
            return cache[tid]
        r = self.raw.get(tid)
        if r is None:
            cache[tid] = None
            return None
        kinds = [self.kind.get((tid, i)) for i in r['i']]
        out = dict(st=np.array(r['st'], float), p=np.array(r['p'], float).reshape(-1, 2), v=np.array(r['v'], float).reshape(-1, 2),
                   ub=np.array([k in ('birth', 'update') for k in kinds], bool), miss=np.array([k == 'miss' for k in kinds], bool))
        cache[tid] = out
        return out

    def a_hat_vec(self, tid, st):
        """oxsb_core_v01.a_hat_vec."""
        r = self._arrays(tid)
        if r is None:
            return np.zeros(2)
        idx = np.flatnonzero(r['st'] <= st + 1e-6)
        u = idx[r['ub'][idx]] if idx.size else idx
        if u.size < 2:
            return np.zeros(2)
        j, k = u[-2], u[-1]
        return (r['v'][k] - r['v'][j]) / (r['st'][k] - r['st'][j])

    def state_at(self, tid, st):
        """ox12_core_v01.Hist.state_at."""
        r = self._arrays(tid)
        if r is None:
            return None
        hit = np.flatnonzero(np.abs(r['st'] - st) < 1e-6)
        if hit.size == 0:
            return None
        i = hit[-1]
        return r['p'][i], r['v'][i]


# ------------------------------------------------------------------------------------------------ lead and phase (A10 2.4)
def lead_index(actors, now):
    """Online lead track: the actor whose predicted centre at `now` is ahead of the ego centre (x > 0, planner frame)
    within LEAD_LATERAL_M of the route line, nearest in x; None if there is none. (The open-loop analysis matched the
    lead to the true primary actor; truth is not available online. Recorded as a departure in STATUS.md.)"""
    best = None; bx = math.inf
    for oi, a in enumerate(actors):
        age = now - a['state_time']; px = a['x'] + age * a['vx']; py = a['y'] + age * a['vy']
        if px > 0. and abs(py) <= LEAD_LATERAL_M and px < bx:
            bx = px; best = oi
    return best


def phase_of(actors, now, hist, thr=PHASE_BRAKE_A):
    """0 before braking (also with no lead), 1 braking, 2 stopped (a9_3_phase_scale_cv_v02.py L194-198 with the
    a9_4a lead estimates: vhat = |(vx, vy)|; ahat_long = a_hat_vec . v_w / |v_w|, v_w the track's world output velocity
    at its state time)."""
    li = lead_index(actors, now)
    if li is None:
        return 0, dict(lead=None)
    a = actors[li]; tid = int(a['track_id'])
    vh = math.hypot(a['vx'], a['vy'])
    ah = float('nan')
    sa = hist.state_at(tid, a['state_time'])
    if sa is not None:
        vw = np.asarray(sa[1], float); nv = math.hypot(vw[0], vw[1])
        if nv > 0:
            ah = float(hist.a_hat_vec(tid, a['state_time']) @ (vw / nv))
    info = dict(lead=li, track_id=tid, vhat=vh, ahat_long=ah)
    if vh <= PHASE_STOP_V:
        return 2, info
    if math.isfinite(ah) and ah <= thr:
        return 1, info
    return 0, info


# ------------------------------------------------------------------------------------------------ one row, one source
def apply_source(tr, actors, now, source, pbar, hist=None, phase_scale=None):
    """Return (d_used, s) for one row computed by constraints_full. For PS, s already carries the phase scale."""
    d = np.asarray(tr['d'], dtype=np.float64)
    if source in ('N', 'N_IMM'):
        return d, np.asarray(tr['p'], dtype=np.float64)
    if source in ('Z', 'F0', 'F0_IMM', 'BRAKE'):
        return d, s_class_average(tr, actors, pbar)
    if source == 'CK3':
        SH, _ = ck3_shift(tr, actors, now, hist)
        return d + SH, s_class_average(tr, actors, pbar)
    if source == 'TG':
        return d, s_time_gap(tr)
    if source == 'PS':
        if phase_scale is None:
            raise ValueError('PS needs the phase scale of the decision')
        return d, phase_scale * s_class_average(tr, actors, pbar)
    raise ValueError('Unknown source: ' + repr(source))


def crit_row(d, s):
    """ol_gateR_core_v01.crit_rows for one row: the largest g with d >= 0 and g s <= d^2 on every constraint."""
    if len(d) == 0:
        return math.inf
    if (d < 0).any():
        return -math.inf
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = np.where(s > 0, (d * d) / np.where(s > 0, s, 1.), np.inf)
    return float(ratio.min())
