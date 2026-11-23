"""Gate R (BRIEF_GATE_R_v01.md): shared definitions. New file; imports the tools of 10 November read-only
(olcore_v01, ol_extract_v01) and, through olcore_v01, Codex's planner modules read-only (python -I -B).

Meaning copied from the stand-in (m5core_v04.py): AGE_EDGES / age_band, label_group, the F1 table class with its
fall-back order, the bookkeeping of track age and missed-frame band (TrackBook.features), f1_samples, arm_s for
F0 / F1 / E, crit_batch with beta = 0.

Track age and missed frames of the logged tracks come from the capture logs themselves:
  detections.jsonl   line i = detector frame i (time 1.0 + 0.5 i s), 'tracks' = the tracker's output list (id, state_time)
  filter_events.jsonl  one 'birth' / 'update' / 'miss' event per track and detector frame ('timestamp' = frame index);
                     'miss' = the track's update step got no detection (Codex tracker_audit.record_history), which is the
                     stand-in's flag  life_management.time_since_update > 0  after that frame.
  age  = state_time - time of the first detector frame whose output list holds the track id   (TrackBook: state_time - birth)
  band = 2 if the flag of the state's frame is 'miss'; 1 if any of the last 4 flags (frames in which the track was
         output, up to the state's frame) is 'miss'; else 0                                       (TrackBook.features)
"""
import json, math, pathlib, sys
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import olcore_v01 as oc                      # noqa: E402
import ol_extract_v01 as ox                  # noqa: E402  (window_truth, clearance; its main() is not run on import)
from olcore_v01 import consumer, finite_primitive   # noqa: E402

ROOT = HERE.parents[2]
SETS = {'tuning': dict(arch=ROOT / '08_phase2' / 'archives_c1', runs=HERE / 'runs_tuning_v01', res=HERE / 'results_tuning_v01'),
        'fit': dict(arch=ROOT / '07_fit_runs' / 'archives', runs=HERE / 'runs_fit_v01', res=HERE / 'results_fit_v01')}
SAMPLES = HERE / 'gateR_samples_v01'
OUT = HERE / 'gateR_v01'
PBAR_FILE = HERE / 'pbar_tuning_v01.json'
TABLE_FILES = {'F1': HERE / 'F1_TABLE_GATER_all_v01.json', 'F1x': HERE / 'F1_TABLE_GATER_noLB_v01.json'}
FAMS = list(oc.FAMILIES)
G = np.array([0., 0.01, 0.03, 0.1, 0.3, 1., 3., 10., 30., 100., 300., 1000.])
TIMES = np.arange(61) * 0.05
F1_T = np.arange(0., 3.01, 0.25)
F1_J = np.round(F1_T / 0.05).astype(int)
AGE_EDGES = (0.25, 0.75, 1.25, 2.25)        # 2 Hz detector frames: age 0 / 0.5 / 1.0 / 1.5-2.0 / >= 2.5 s
NMIN = 40
ACTOR_KEYS = ['x', 'y', 'vx', 'vy', 'yaw', 'length', 'width', 'state_time', 'sigma_acc']


def planned(set_name):
    """Runs of a set = the runs the tool of 10 November extracted (one stored .npz each), in sorted order."""
    return [f.name[:-4] for f in sorted(SETS[set_name]['runs'].glob('*.npz'))]


def age_band(age_s):
    return int(np.searchsorted(AGE_EDGES, age_s, side='right'))


def label_group(name):
    return name if name in ('pedestrian', 'bicycle', 'motorcycle', 'car') else 'large'


def level_of(key):
    if key.startswith('fallback:'):
        return 'last resort'
    if not key.startswith('C'):
        return 'label,age,miss'
    return ('class', 'class,age', 'class,age,miss')[key.count('|')]


class F1Table:
    """m5core_v04.F1Table: second moment E[e e'] (2x2, planner frame) of the centre prediction error at look-ahead te,
    by (label group, age band, miss band); sparse cells fall back to (class, age, miss), (class, age), class."""

    def __init__(self, d):
        self.d = d
        self.knots = np.array(d['te_knots'], float)
        self.cells = {k: np.array(v, float) for k, v in d['cells'].items()}
        self.used = {}

    def lookup(self, name, age_b, miss_b):
        c = oc.cls_of(name)
        for key in ('%s|%d|%d' % (label_group(name), age_b, miss_b), 'C%s|%d|%d' % (c, age_b, miss_b),
                    'C%s|%d' % (c, age_b), 'C%s' % c):
            if key in self.cells:
                self.used[key] = self.used.get(key, 0) + 1
                return self.cells[key]
        cand = [k for k in self.cells if k.startswith('C') and '|' not in k]
        if cand:
            key = max(cand, key=lambda k: sum(self.d['counts'][k]))
            self.used['fallback:' + key] = self.used.get('fallback:' + key, 0) + 1
            return self.cells[key]
        raise KeyError(name)

    def s(self, n, te, tab):
        xx = np.interp(te, self.knots, tab[:, 0]); xy = np.interp(te, self.knots, tab[:, 1]); yy = np.interp(te, self.knots, tab[:, 2])
        return np.maximum(n[..., 0] ** 2 * xx + 2 * n[..., 0] * n[..., 1] * xy + n[..., 1] ** 2 * yy, 0.)


class Book:
    """Observable history of every track id of one run, from the capture logs (see the module text)."""

    def __init__(self, cap):
        dets = list(oc.jl(cap / 'detections.jsonl'))
        self.det_time = np.array([d['time'] for d in dets], float)
        kind = {}; self.n_reset = 0; self.n_dup = 0
        for e in oc.jl(cap / 'filter_events.jsonl'):
            if e['kind'] in ('birth', 'update', 'miss'):
                key = (int(e['track']), int(e['timestamp']))
                if key in kind:
                    self.n_dup += 1          # counted and reported (expected 0); the first event is kept
                    continue
                kind[key] = e['kind']
            elif e['kind'] == 'reset':
                self.n_reset += 1
        self.birth = {}; self.hist = {}
        self.n_out = 0; self.n_noevent = 0; self.n_birth_mismatch = 0; self.n_miss_out = 0
        for i, d in enumerate(dets):
            for t in d['tracks']:
                tid = int(t['id']); kd = kind.get((tid, i)); self.n_out += 1
                if tid not in self.birth:
                    self.birth[tid] = i; self.hist[tid] = ([], [])
                    if kd != 'birth':
                        self.n_birth_mismatch += 1
                if kd is None:
                    self.n_noevent += 1
                self.n_miss_out += (kd == 'miss')
                self.hist[tid][0].append(i); self.hist[tid][1].append(1 if kd == 'miss' else 0)
        self.n_unknown = 0

    def features(self, tid, state_time):
        """(age in s, miss band) of track tid at its state time; (0, 0) for a track without history, as the stand-in."""
        kb = self.birth.get(tid)
        di = int(np.argmin(np.abs(self.det_time - state_time))) if self.det_time.size else -1
        if kb is None or di < 0 or abs(self.det_time[di] - state_time) >= 1e-6:
            self.n_unknown += 1
            return 0., 0
        idx, fl = self.hist[tid]
        h = [f for i, f in zip(idx, fl) if i <= di]
        mb = 2 if (h and h[-1]) else (1 if any(h[-4:]) else 0)
        return float(state_time - self.det_time[kb]), mb


def load_run(set_name, run):
    """Everything read once per run (read-only)."""
    rd = SETS[set_name]['arch'] / run
    S = json.loads((rd / 'SUMMARY.json').read_text(encoding='utf-8'))
    cap = oc.cap_dir(rd)
    draw = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))['case']['draw']
    ao = S.get('assessment_outcomes') or {}
    base = ao['base_frame']; fc = ao.get('first_contact_frame')
    T = oc.load_truth(cap); Sc, roles = oc.load_scen(cap, base)
    react_ks = np.array(sorted(k for k, v in Sc.items() if v[0]), dtype=int)
    return dict(rd=rd, cap=cap, arm=S.get('arm'), draw=draw, contact_k=(fc - base - 1) if fc is not None else -1, T=T, kmax=max(T),
                react_ks=react_ks, first_react=int(react_ks[0]) if react_ks.size else 10 ** 9, book=Book(cap))


def decisions(cap):
    for r in oc.jl(cap / 'frames.jsonl'):
        dec = (r.get('execution') or {}).get('new_decision')
        if dec and dec['mode'] == 'assessment':
            yield r['k'], dec


def match_many(actors, now, tr):
    """The tool's matching of ol_extract_v01 (form R4): every logged actor gets the nearest true scenario actor whose
    centre at `now` (planner frame) is closer than 4 m to the actor's position at `now`; None if there is none.
    Returns (list of actor id or None per logged actor, primary id, order)."""
    prim = tr['target_id'] if tr else None
    if tr is None or prim is None or prim not in tr['actors']:
        return [None] * len(actors), None, []
    order = [prim] + [a for a in tr['actors'] if a != prim]
    tp = {aid: oc.to_planner(tr['ego'], tr['actors'][aid][0], tr['actors'][aid][1]) for aid in order}
    out = []
    for a in actors:
        age = now - a['state_time']; px = a['x'] + age * a['vx']; py = a['y'] + age * a['vy']
        best = None; bd = oc.GATE_M
        for aid in order:
            dd = math.hypot(px - tp[aid][0], py - tp[aid][1])
            if dd < bd:
                bd = dd; best = aid
        out.append(best)
    return out, prim, order


def planner_centres(ego, c):
    """World centres c (61, 2) -> the planner frame fixed at the decision tick (olcore_v01.to_planner, vectorised)."""
    dx = c[:, 0] - ego[0]; dy = c[:, 1] - ego[1]; ch, sh = math.cos(ego[2]), math.sin(ego[2])
    return np.column_stack([ch * dx + sh * dy, -sh * dx + ch * dy])


def geometry(rows, actors, now):
    """Per row and constraint: the unit normal N (R, M, 2); per constraint the look-ahead from the state time TE (M,);
    per actor the predicted centres MU (61, 2). The same numpy calls as consumer.constraints_for_trajectory."""
    R = len(rows); na = len(actors); M = 120 * na
    N = np.empty((R, M, 2)); TE = np.empty(M); MU = []
    for oi, o in enumerate(actors):
        vals = consumer.finite_array([o[k] for k in ACTOR_KEYS])
        age = now - o['state_time']; vel = vals[2:4]; t = TIMES + age
        mu = vals[:2] + t[:, None] * vel
        MU.append(mu); TE[120 * oi:120 * oi + 60] = t[0:60]; TE[120 * oi + 60:120 * oi + 120] = t[1:61]
    for r, tr in enumerate(rows):
        ego = np.column_stack([tr['s'], np.zeros(61)])
        for oi in range(na):
            mu = MU[oi]
            mid = .5 * (mu[:-1] + mu[1:] - ego[:-1] - ego[1:]); lens = np.linalg.norm(mid, axis=1)
            normals = np.zeros_like(mid); valid = lens > 1e-12
            normals[valid] = mid[valid] / lens[valid, None]; normals[~valid] = [1., 0.]
            N[r, 120 * oi:120 * oi + 60] = normals; N[r, 120 * oi + 60:120 * oi + 120] = normals
    return N, TE, MU


def s_P(N, TE, Ps):
    """z' P z per constraint with one 4x4 matrix per actor (Ps), the consumer's einsum form per row and offset, floored at 0."""
    R, M = N.shape[:2]; out = np.empty((R, M))
    for oi, Pm in enumerate(Ps):
        for offset in (0, 1):
            c0 = 120 * oi + 60 * offset; te = TE[c0:c0 + 60]
            for r in range(R):
                nrm = N[r, c0:c0 + 60]
                z = np.column_stack([nrm, nrm * te[:, None]])
                out[r, c0:c0 + 60] = np.einsum('ni,ij,nj->n', z, Pm, z)
    return np.maximum(out, 0.)


def crit_rows(D, S):
    """Largest g with d >= 0 and g * s <= d^2 for every constraint of each row (-inf never, +inf always): olcore_v01.crit_alpha
    with B = 0 for all rows at once (m5core_v04.crit_batch with beta = 0)."""
    R, M = D.shape
    if M == 0:
        return np.full(R, np.inf)
    bad = (D < 0).any(axis=1)
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = np.where(S > 0, (D * D) / np.where(S > 0, S, 1.), np.inf)
    return np.where(bad, -np.inf, ratio.min(axis=1))


# ------------------------------------------------------------------------------------------------ scoring (ol_analyse_v01 Part 2)
NST = 5     # decisions, wrong-go decisions, sum of caution, decisions with a caution value (true-safe selection), fallbacks


def clean_clear(clear):
    """ol_analyse_v01: NaN clearance (only outside the evaluated set) -> -1."""
    return np.where(np.isfinite(clear) | (clear == np.inf), clear, -1.)


def select(C, g, idx55):
    feas = C >= g
    anyf = feas.any(1)
    return np.where(anyf, feas.argmax(1), idx55), ~anyf


def sel_stats(sel, fb, clear, vbar, des, masks, thr=0.):
    """Statistics (len(masks), NST) of one selection in one run. Definitions of ol_analyse_v01.evaluate:
    safe = clearance > thr; wrong go = a true-safe row exists and the selected row is not true-safe;
    caution = (oracle mean speed - selected mean speed) / desired speed, summed over true-safe selections."""
    n = len(sel); ar = np.arange(n)
    safe = clear > thr
    anys = safe.any(1); orc = safe.argmax(1)
    ssel = safe[ar, sel]
    ct = np.where(ssel, (vbar[ar, orc] - vbar[ar, sel]) / des, 0.)
    out = np.empty((len(masks), NST))
    for si, m in enumerate(masks):
        out[si] = (m.sum(), (anys & ~ssel & m).sum(), ct[m].sum(), (ssel & m).sum(), (fb & m).sum())
    return out


def crit_stats(C, gs, idx55, clear, vbar, des, masks, thr=0.):
    """(len(gs), len(masks), NST) for an arm stored as critical values."""
    out = np.empty((len(gs), len(masks), NST))
    for gi, g in enumerate(gs):
        sel, fb = select(C, g, idx55)
        out[gi] = sel_stats(sel, fb, clear, vbar, des, masks, thr)
    return out
