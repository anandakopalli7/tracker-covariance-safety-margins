"""e_recount_v01.py - independent second program for package E (A10 section 10.1(b)).

Written from AMENDMENT_10_v13.md (sections 0, 5.8, 7), the brake-test rule of DESIGN_NOTES_v01 6.4e, the
planner's trajectory model (design_core_v85.trajectory) and the stand-in's STOP mode, NOT from the first program.
Python 3.12 + numpy only.   Run:  python -I -B e_recount_v01.py <command> ...   (see README_RECOUNT_v01.md)

  outcomes <runs_dir> <prefix> --out X.json        per-run outcomes (A10 7.4)
  brake <runs_dir> --out X.json                    E1 brake test (A10 7.1)
  calibration <outcomes_e2.json> --out X.json      levels g_lo, g_hi (A10 7.3)
  matched --calib <calibration.json> --out X.json   matched settings of the other arms (A10 7.3; reads old-run arrays)
  compare <outcomes_e3.json> [--e3b F] --low-power true|false --out X.json     (A10 7.5)
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

DT = 0.05                    # physical tick (20 Hz)
SMOOTH = 5                   # 0.25 s moving average = 5 samples at 20 Hz
BOOT_SEED = 20261922         # A10 5.8: E case bootstrap
BOOT_N = 20000
NEWCOMBE_Z = 1.959963984540054
OUTCOME_KEYS = ('impact_speed_mps', 'time_lost_s', 'rest_gap_m', 'peak_decel_mps2', 'rms_jerk_mps3', 'fallback_share')


# ----------------------------------------------------------------------------- small helpers
def read_json(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def read_jsonl(p):
    out = []
    with open(p, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def clean(o):
    """Make a structure JSON-safe: numpy -> python, NaN/inf -> None."""
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (float, np.floating)):
        return None if (math.isnan(o) or math.isinf(o)) else float(o)
    return o


def write_json(obj, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(clean(obj), f, indent=1)


def load_runs_file(path):
    d = read_json(path)
    return d['runs'] if isinstance(d, dict) else d


def parse_bool(s):
    if s.lower() in ('true', '1', 'yes'):
        return True
    if s.lower() in ('false', '0', 'no'):
        return False
    raise argparse.ArgumentTypeError('expected true or false')


# ----------------------------------------------------------------------------- finding runs of record
def base_run_id(run_id):
    return re.sub(r'__r\d+$', '', run_id)


def attempt_no(run_id):
    m = re.search(r'__r(\d+)$', run_id)
    return int(m.group(1)) if m else 0


def runs_of_record(runs_dir, prefix):
    """{base_id: run_dir} using the last attempt (highest __rN suffix) of every job with the prefix."""
    best = {}
    for d in sorted(Path(runs_dir).iterdir()):
        if not d.is_dir() or not d.name.startswith(prefix) or not (d / 'SUMMARY.json').exists():
            continue
        b = base_run_id(d.name)
        if b not in best or attempt_no(d.name) > attempt_no(best[b].name):
            best[b] = d
    return best


def capture_dir(run_dir, case):
    cap = run_dir / 'x' / run_dir.name / 'capture'
    if case and (cap / case).is_dir():
        return cap / case
    subs = [p for p in cap.iterdir() if p.is_dir()] if cap.is_dir() else []
    return subs[0] if len(subs) == 1 else None


# ----------------------------------------------------------------------------- one run's truth
def rh_velocity(v_lh):
    """CARLA left-handed velocity -> right-handed: flip the y component."""
    return np.array([v_lh[0], -v_lh[1]], dtype=float)


class RunData:
    """Everything read from one run directory (None where a file is absent)."""

    def __init__(self, run_dir):
        self.run_dir = Path(run_dir)
        self.summary = read_json(self.run_dir / 'SUMMARY.json')
        self.case = self.summary.get('case')
        self.cap = capture_dir(self.run_dir, self.case)
        self.problems = []
        self.contract = self.outcomes = self.arm_method = None
        self.truth = self.frames = self.contacts = []
        self.policy_failure = False
        if self.cap is None:
            self.problems.append('no_capture_directory')
            return
        c = self.cap
        self.contract = read_json(c / 'contract.json') if (c / 'contract.json').exists() else None
        self.outcomes = read_json(c / 'assessment_outcomes.json') if (c / 'assessment_outcomes.json').exists() else None
        self.arm_method = read_json(c / 'ARM_METHOD_v01.json') if (c / 'ARM_METHOD_v01.json').exists() else None
        self.policy_failure = (c / 'policy_failure.json').exists()
        if (c / 'evaluation_truth.jsonl').exists():
            self.truth = read_jsonl(c / 'evaluation_truth.jsonl')
        if (c / 'frames.jsonl').exists():
            self.frames = read_jsonl(c / 'frames.jsonl')
        if (c / 'contacts.jsonl').exists():
            self.contacts = read_jsonl(c / 'contacts.jsonl')

    @property
    def desired(self):
        try:
            return float(self.contract['case']['desired_mps'])
        except Exception:
            return None

    def decisions(self):
        out = []
        for fr in self.frames:
            nd = (fr.get('execution') or {}).get('new_decision')
            if nd:
                out.append(nd)
        return out

    def arrays(self):
        """Per-tick truth arrays (right-handed): ego/target centre, route direction, velocities, gap."""
        n = len(self.truth)
        ego_c = np.zeros((n, 2)); yaw = np.zeros(n)
        ve = np.zeros((n, 2)); vt = np.zeros((n, 2)); gap = np.zeros(n)
        lat_overlap = np.zeros(n, dtype=bool)   # target within the ego's lane width (route frame)
        overlap = np.zeros(n, dtype=bool)       # boxes overlap in the route frame (separate from the sign of the gap)
        for i, r in enumerate(self.truth):
            ego_c[i] = r['ego']['derived']['center_rh'][:2]
            yaw[i] = r['ego']['derived']['route_yaw_rh']
            ve[i] = rh_velocity(r['ego']['velocity_lh'])
            vt[i] = rh_velocity(r['target']['velocity_lh'])
            gap[i] = r['directional_gap_m']
            u = np.array([math.cos(yaw[i]), math.sin(yaw[i])]); w = np.array([-u[1], u[0]])
            dc = np.array(r['target']['derived']['center_rh'][:2]) - ego_c[i]
            de, dt_ = r['ego']['derived'], r['target']['derived']
            half_len = de['forward_support_m'] + dt_['forward_support_m']
            half_wid = 0.5 * (de['left_support_m'] + de['right_support_m']) + 0.5 * (dt_['left_support_m'] + dt_['right_support_m'])
            lat_overlap[i] = abs(dc @ w) < half_wid
            overlap[i] = abs(dc @ u) < half_len and lat_overlap[i]
        return dict(ego_c=ego_c, yaw=yaw, ve=ve, vt=vt, gap=gap, overlap=overlap, lat_overlap=lat_overlap)


def tick_of_frame(frame, base_frame):
    return int(frame) - int(base_frame) - 1


# ----------------------------------------------------------------------------- 7.4 outcomes of one run
def smoothed_kinematics(speed):
    """Speed -> 5-sample moving average ('valid', no padding) -> accel = diff/dt -> jerk = diff/dt.
    Returns (accel, jerk) or (None, None) if the series is too short."""
    speed = np.asarray(speed, dtype=float)
    if len(speed) < SMOOTH + 2:
        return None, None
    vs = np.convolve(speed, np.ones(SMOOTH) / SMOOTH, mode='valid')
    a = np.diff(vs) / DT
    j = np.diff(a) / DT
    return a, j


def run_outcome(run_dir):
    rd = RunData(run_dir)
    s = rd.summary
    ej = s.get('e_job') or {}
    knobs = (rd.arm_method or {}).get('knobs') or {}
    lead_variant = None
    try:
        lead_variant = rd.contract['case'].get('lead_variant')
    except Exception:
        pass
    row = dict(run_id=rd.run_dir.name, job=s.get('job'), case=s.get('case'),
               arm=(rd.arm_method or {}).get('arm') or s.get('arm'),
               level=ej.get('level'), g=ej.get('g', knobs.get('g')), triple=ej.get('triple', knobs.get('triple')),
               lead_variant=lead_variant)
    reasons = []
    warnings = []
    if s.get('status') != 'CAPTURED_AND_REVIEWED':
        reasons.append('summary_status_%s' % s.get('status'))
    reasons += list(rd.problems)
    if rd.policy_failure:
        reasons.append('policy_failure_file')
    if rd.outcomes is None:
        reasons.append('no_assessment_outcomes')
    if not rd.truth:
        reasons.append('no_truth')
    if not rd.frames:
        reasons.append('no_frames')
    null = dict(contact=None, first_contact_k=None, impact_speed_mps=None, time_lost_s=None, rest_gap_m=None,
                peak_decel_mps2=None, rms_jerk_mps3=None, fallback_share=None)
    if rd.outcomes is None or not rd.truth:
        row.update(null); row.update(valid=False, invalid_reasons=reasons, warnings=warnings)
        return row

    o = rd.outcomes
    if o.get('invalid_reasons'):
        reasons.append('assessment_invalid:' + ','.join(map(str, o['invalid_reasons'])))
    if o.get('instrument_failures'):
        reasons.append('instrument_failures')
    if o.get('first_policy_failure_frame') is not None:
        reasons.append('policy_failure_frame')
    if o.get('termination') not in ('FULL_ASSESSMENT', 'FIRST_PHYSICAL_CONTACT'):
        reasons.append('termination_%s' % o.get('termination'))
    base = o['base_frame']
    k_start = tick_of_frame(o['assessment_start_frame'], base)
    n = len(rd.truth)
    if [r['k'] for r in rd.truth] != list(range(n)):
        reasons.append('truth_ticks_not_contiguous')
    if rd.desired is None:
        reasons.append('no_desired_speed')
    if n <= k_start + SMOOTH + 2:
        reasons.append('truth_shorter_than_assessment_start')

    A = rd.arrays()
    k_last = n - 1

    # ---- contact: any contact event, or truth gap <= 0 (first of the two)
    ev_k = [tick_of_frame(e['frame'], base) for e in rd.contacts]
    # a gap <= 0 counts only while the two boxes also overlap in the route frame: the directional gap is also <= 0 for a
    # road user that is beside or behind the ego (checked on old runs: -400 m for a passed vehicle)
    gap_k = [int(i) for i in np.flatnonzero((A['gap'] <= 0.0) & A['overlap'])]
    cands = ev_k + gap_k[:1]
    contact = 1 if cands else 0
    kc = min(cands) if cands else None
    if kc is not None:
        kc = min(max(kc, 0), k_last)
        if kc < k_start:
            reasons.append('contact_before_assessment')
    if (o.get('first_contact_frame') is not None) != bool(contact):
        warnings.append('assessment_outcomes_first_contact_disagrees_with_truth_and_contact_events')

    row['contact'] = contact
    row['first_contact_k'] = kc

    # ---- impact speed: closing speed along the route at the first contact tick
    row['impact_speed_mps'] = None
    row['impact_speed_at_contact_tick_mps'] = None  # diagnostic only (post-impulse state)
    if kc is not None:
        def closing(k):
            u = np.array([math.cos(A['yaw'][k]), math.sin(A['yaw'][k])])
            return float((A['ve'][k] - A['vt'][k]) @ u)
        # the truth record of the contact tick is already after the impulse (tick k has CARLA frame base + 1 + k, the
        # frame the collision callback reports), so the speed at impact is the state one tick earlier
        row['impact_speed_mps'] = closing(max(kc - 1, 0))
        row['impact_speed_at_contact_tick_mps'] = closing(kc)

    # ---- time lost (runs without contact): run length - forward distance / desired speed
    row['time_lost_s'] = None
    row['forward_distance_m'] = None
    if n > k_start:
        u0 = np.array([math.cos(A['yaw'][k_start]), math.sin(A['yaw'][k_start])])
        dist = float((A['ego_c'][k_last] - A['ego_c'][k_start]) @ u0)
        row['forward_distance_m'] = dist
        if not contact and rd.desired:
            run_length = (k_last - k_start) * DT
            row['time_lost_s'] = run_length - dist / rd.desired
        fd = o.get('forward_displacement_m')
        if fd is not None and abs(fd - dist) > 0.05:
            warnings.append('forward_displacement_m_differs_from_truth_projection_by_%.3f' % (fd - dist))

    # ---- rest gap: gap to a stopped lead at the end of the run (no contact, lead speed <= 0.5 m/s, lead ahead in the ego's lane)
    row['end_gap_m'] = float(A['gap'][k_last])
    lead_speed_end = float(np.linalg.norm(A['vt'][k_last]))
    in_lane_ahead = bool(A['lat_overlap'][k_last]) and A['gap'][k_last] > 0
    row['rest_gap_m'] = float(A['gap'][k_last]) if (not contact and lead_speed_end <= 0.5 and in_lane_ahead) else None

    # ---- peak deceleration and RMS jerk from the 0.25 s smoothed ego speed over the assessment window
    speed = np.linalg.norm(A['ve'][k_start:], axis=1) if n > k_start else np.array([])
    acc, jerk = smoothed_kinematics(speed)
    row['peak_decel_mps2'] = float(np.max(-acc)) if acc is not None else None
    row['rms_jerk_mps3'] = float(np.sqrt(np.mean(jerk ** 2))) if jerk is not None and len(jerk) else None

    # ---- fallback share: assessment-mode decisions in full braking
    dec = [d for d in rd.decisions() if d.get('mode') == 'assessment']
    row['fallback_share'] = (sum(1 for d in dec if (d.get('output') or {}).get('fallback')) / len(dec)) if dec else None
    row['n_assessment_decisions'] = len(dec)
    if not dec:
        reasons.append('no_assessment_decisions')

    row['valid'] = not reasons
    row['invalid_reasons'] = reasons
    row['warnings'] = warnings
    return row


def cmd_outcomes(a):
    recs = runs_of_record(a.runs_dir, a.prefix)
    rows = []
    for b in sorted(recs):
        try:
            rows.append(run_outcome(recs[b]))
        except Exception as e:     # an unreadable run is reported, never silently dropped
            rows.append(dict(run_id=recs[b].name, job=b, valid=False, invalid_reasons=['read_error:%r' % (e,)]))
    write_json(dict(schema='E_RECOUNT_OUTCOMES_v01', runs_dir=str(a.runs_dir), prefix=a.prefix, n_runs=len(rows), runs=rows), a.out)
    print('wrote %s: %d runs, %d valid' % (a.out, len(rows), sum(1 for r in rows if r.get('valid'))))


# ----------------------------------------------------------------------------- 7.1 E1 brake test
def planner_trajectory_distance(first, second, v0, a0, h=0.05, H=12.0, H_max=120.0):
    """design_core_v85.trajectory, distance only. Acceleration follows the target at +-8 m/s^3 (8*h per step);
    first target for t < 1 s, second afterwards; speed is held in [0, 20]. H is doubled until standstill."""
    if not (0 <= v0 <= 20):
        raise ValueError('initial speed outside the planner domain')
    while True:
        n = round(H / h)
        v, a, s = v0, a0, 0.0
        for k in range(n):
            target = first if k * h < 1.0 - 1e-12 else second
            a += float(np.clip(target - a, -8 * h, 8 * h))
            vn = v + a * h
            if vn < 0 or vn > 20:
                bound = 0.0 if vn < 0 else 20.0
                ts = (bound - v) / a
                s += v * ts + 0.5 * a * ts * ts + bound * (h - ts)
                v = bound
            else:
                s += v * h + 0.5 * a * h * h
                v = vn
        if v <= 1e-9 or H >= H_max:
            return s, H, v
        H *= 2.0


def brake_run(run_dir):
    rd = RunData(run_dir)
    s = rd.summary
    out = dict(run_id=rd.run_dir.name, job=s.get('job'), case=s.get('case'), status=s.get('status'),
               desired_mps=rd.desired, policy_failure=bool(rd.policy_failure), first_fallback_k=None, v0=None, a0=None,
               v0_measured=None, a0_measured=None, model_dist_m=None, stop_dist_m=None, ratio=None, within_10pct=False,
               contact=None, problems=list(rd.problems))
    if rd.outcomes and rd.outcomes.get('first_policy_failure_frame') is not None:
        out['policy_failure'] = True
    if not rd.truth or not rd.frames:
        out['problems'].append('no_truth_or_frames')
        return out
    A = rd.arrays()
    n = len(rd.truth)
    out['contact'] = int(bool(rd.contacts) or bool(np.any((A['gap'] <= 0) & A['overlap'])))
    fb = [d for d in rd.decisions() if d.get('mode') == 'assessment' and (d.get('output') or {}).get('fallback')]
    if not fb:
        out['problems'].append('no_fallback_decision')
        return out
    d0 = fb[0]
    kf = int(d0['tick'])
    ms = d0.get('model_state') or {}
    out['first_fallback_k'] = kf
    out['v0'] = float(ms['model_speed_mps']); out['a0'] = float(ms['model_acceleration_mps2'])   # planner's own initial state
    fr = {f['k']: f for f in rd.frames}
    if kf in fr:
        out['v0_measured'] = float(fr[kf]['state']['speed']); out['a0_measured'] = float(fr[kf]['acceleration'])
    dist, H_used, v_end = planner_trajectory_distance(-5.0, -5.0, out['v0'], out['a0'])
    out['model_dist_m'] = dist; out['model_horizon_s'] = H_used
    # real stopping distance: route-projected travel from the first fallback tick to the first tick with measured speed < 0.05
    speed = np.array([fr[k]['state']['speed'] for k in range(n)]) if all(k in fr for k in range(n)) else None
    if speed is None:
        out['problems'].append('frames_missing_ticks')
        return out
    idx = np.flatnonzero(speed[kf:] < 0.05)
    if len(idx):
        ks = kf + int(idx[0])
        u = np.array([math.cos(A['yaw'][kf]), math.sin(A['yaw'][kf])])
        out['stop_dist_m'] = float((A['ego_c'][ks] - A['ego_c'][kf]) @ u)
        out['stop_tick'] = ks
        out['ratio'] = out['stop_dist_m'] / dist
        out['within_10pct'] = abs(out['ratio'] - 1.0) <= 0.10
    else:
        out['problems'].append('never_stopped')
    return out


def cmd_brake(a):
    recs = runs_of_record(a.runs_dir, 'e1_')
    rows = []
    for b in sorted(recs):
        try:
            sm = read_json(recs[b] / 'SUMMARY.json')
        except Exception:
            continue
        if sm.get('arm') != 'E_BRAKE':
            continue
        rows.append(brake_run(recs[b]))
    by_speed = {}
    for r in rows:
        if r['desired_mps'] is not None:
            by_speed.setdefault(int(round(r['desired_mps'])), []).append(r)
    per = {}
    ok = True
    for sp in (5, 10, 15):
        rs = by_speed.get(sp, [])
        if not rs:
            per[sp] = dict(present=False, ok=False); ok = False
            continue
        r = rs[-1]          # last job (sorted by id) if a speed has more than one
        good = (r['status'] == 'CAPTURED_AND_REVIEWED' and not r['policy_failure'] and r['within_10pct'] and not r['problems'])
        per[sp] = dict(present=True, run_id=r['run_id'], n_runs_for_speed=len(rs), ok=bool(good),
                       ratio=r['ratio'], within_10pct=r['within_10pct'], policy_failure=r['policy_failure'], status=r['status'])
        ok = ok and good
    write_json(dict(schema='E_RECOUNT_BRAKE_v01', runs_dir=str(a.runs_dir), runs=rows, per_speed=per, passed=bool(ok)), a.out)
    print('wrote %s: %d brake runs, passed=%s' % (a.out, len(rows), ok))


# ----------------------------------------------------------------------------- 7.3 calibration
def cmd_calibration(a):
    runs = [r for r in load_runs_file(a.outcomes) if r.get('arm') == 'E_F0' or r.get('arm') == 'F0']
    gs = sorted({float(r['g']) for r in runs if r.get('g') is not None})
    per = {}
    for g in gs:
        rs = [r for r in runs if r.get('g') is not None and float(r['g']) == g]
        valid = [r for r in rs if r.get('valid')]
        k = sum(1 for r in valid if r.get('contact') == 1)
        per[g] = dict(g=g, n_runs=len(rs), n_valid=len(valid), n_invalid=len(rs) - len(valid), contacts=k,
                      share=(k / len(valid)) if valid else None)
    defined = {g: v['share'] for g, v in per.items() if v['share'] is not None}
    low_power = False
    if not defined:
        g_lo = g_hi = None
    elif all(s < 0.05 for s in defined.values()):
        g_lo, g_hi, low_power = 0.25, 1.0, True
    else:
        # nearest share to target; ties go to the smaller g (iterate ascending, strict improvement only)
        def nearest(target):
            best = None
            for g in sorted(defined):
                dist = abs(defined[g] - target)
                if best is None or dist < best[0] - 1e-12:
                    best = (dist, g)
            return best[1]
        g_lo, g_hi = nearest(0.20), nearest(0.05)
    write_json(dict(schema='E_RECOUNT_CALIBRATION_v01', per_g=[per[g] for g in sorted(per)], g_lo=g_lo, g_hi=g_hi,
                    low_power=low_power), a.out)
    print('wrote %s: g_lo=%s g_hi=%s low_power=%s' % (a.out, g_lo, g_hi, low_power))


# ----------------------------------------------------------------------------- 7.5 statistics
def wilson(k, n, z=NEWCOMBE_Z):
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, centre - half), min(1.0, centre + half)


def newcombe_paired(a, b, c, d, z=NEWCOMBE_Z):
    """Newcombe (1998, Stat Med 17:2635-2650), method 10: square-and-add of the two Wilson score intervals with the
    correlation correction phi for paired proportions. Cells: a both, b arm only, c reference only, d neither.
    Returns (difference arm - reference, lower, upper)."""
    n = a + b + c + d
    if n == 0:
        return None, None, None
    p1 = (a + b) / n          # arm
    p2 = (a + c) / n          # reference
    l1, u1 = wilson(a + b, n, z)
    l2, u2 = wilson(a + c, n, z)
    A = (a + b) * (c + d) * (a + c) * (b + d)
    if A == 0:
        phi = 0.0
    else:
        C = a * d - b * c
        if C > n / 2:
            C -= n / 2
        elif C >= 0:
            C = 0.0
        phi = C / math.sqrt(A)
    delta = p1 - p2
    lower = delta - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2 - 2 * phi * (p1 - l1) * (u2 - p2))
    upper = delta + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2 - 2 * phi * (u1 - p1) * (p2 - l2))
    return delta, lower, upper


def mcnemar_exact(b, c):
    """Two-sided exact McNemar p: 2 * P(X <= min(b, c)), X ~ Binomial(b + c, 1/2), capped at 1."""
    m = b + c
    if m == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(m, i) for i in range(k + 1)) / 2.0 ** m
    return min(1.0, 2 * tail)


def paired_stat(arm_vals, ref_vals, idx=None):
    """Mean of (arm - ref) over the pairs where both are defined. idx: resampled pair indices (with repeats)."""
    x = np.asarray(arm_vals, dtype=float); y = np.asarray(ref_vals, dtype=float)
    if idx is not None:
        x = x[idx]; y = y[idx]
    ok = ~(np.isnan(x) | np.isnan(y))
    if not ok.any():
        return float('nan')
    return float(np.mean(x[ok] - y[ok]))


def boot_ci(arm_vals, ref_vals, idx_matrix):
    """Case bootstrap: every resample draws whole cases (pairs); the statistic is recomputed on it, including which
    pairs are defined. Resamples where it is undefined are dropped. 95% percentile interval."""
    x = np.asarray(arm_vals, dtype=float); y = np.asarray(ref_vals, dtype=float)
    d = x - y
    ok = ~np.isnan(d)
    dz = np.where(ok, d, 0.0)
    num = dz[idx_matrix].sum(axis=1)
    cnt = ok[idx_matrix].sum(axis=1)
    good = cnt > 0
    if not good.any():
        return None, None, 0
    stats = num[good] / cnt[good]
    lo, hi = np.percentile(stats, [2.5, 97.5])
    return float(lo), float(hi), int(good.sum())


def boot_ci_conditional(arm_vals, ref_vals, seed=BOOT_SEED, B=BOOT_N):
    """Alternative (extra): resample only the pairs where both are defined."""
    x = np.asarray(arm_vals, dtype=float); y = np.asarray(ref_vals, dtype=float)
    d = (x - y)[~(np.isnan(x) | np.isnan(y))]
    if len(d) == 0:
        return None, None
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(d), size=(B, len(d)))
    lo, hi = np.percentile(d[idx].mean(axis=1), [2.5, 97.5])
    return float(lo), float(hi)


def inside(lo, hi, a, b):
    return lo is not None and hi is not None and lo > a and hi < b


def classify(c_lo, c_hi, t_lo, t_hi):
    """A10 7.5 rules in the order the amendment lists them; the first that holds wins. A rule that needs a time-lost
    bound that is undefined does not hold. Also returns every rule that holds."""
    t_up_ok = t_hi is not None
    rules = [
        ('safer at no extra cost', c_hi is not None and c_hi < 0 and t_up_ok and t_hi < 0.5),
        ('safer at a cost', c_hi is not None and c_hi < 0 and t_up_ok and t_hi >= 0.5),
        ('equivalent', inside(c_lo, c_hi, -0.10, 0.10) and inside(t_lo, t_hi, -0.5, 0.5)),
        ('worse', c_lo is not None and c_lo > 0),
    ]
    holds = [name for name, ok in rules if ok]
    return (holds[0] if holds else 'inconclusive'), holds


def compare_pair(arm_rows, ref_rows, label, extra=None):
    """arm_rows, ref_rows: dict case -> outcome row (valid runs only). Pairs = cases present in both."""
    cases = sorted(set(arm_rows) & set(ref_rows))
    n = len(cases)
    res = dict(label=label)
    if extra:
        res.update(extra)
    res['pairs'] = n
    res['cases'] = cases
    if n == 0:
        res.update(a=0, b=0, c=0, d=0, classification='no pairs')
        return res
    ca = np.array([arm_rows[k]['contact'] for k in cases]); cr = np.array([ref_rows[k]['contact'] for k in cases])
    a = int(np.sum((ca == 1) & (cr == 1))); b = int(np.sum((ca == 1) & (cr == 0)))
    c = int(np.sum((ca == 0) & (cr == 1))); d = int(np.sum((ca == 0) & (cr == 0)))
    delta, lo, hi = newcombe_paired(a, b, c, d)
    res.update(a=a, b=b, c=c, d=d, arm_contact_share=(a + b) / n, ref_contact_share=(a + c) / n,
               contact_diff=delta, contact_diff_lo=lo, contact_diff_hi=hi, mcnemar_p=mcnemar_exact(b, c))
    # one index matrix per comparison, fresh generator with the amendment's seed
    rng = np.random.default_rng(BOOT_SEED)
    idx = rng.integers(0, n, size=(BOOT_N, n))
    outcomes = {}
    for key in OUTCOME_KEYS:
        xs = np.array([np.nan if arm_rows[k].get(key) is None else arm_rows[k][key] for k in cases], dtype=float)
        ys = np.array([np.nan if ref_rows[k].get(key) is None else ref_rows[k][key] for k in cases], dtype=float)
        if key == 'time_lost_s':      # pairs without contact: time lost is null whenever a run has contact
            pass
        both = ~(np.isnan(xs) | np.isnan(ys))
        lo_k, hi_k, nb = boot_ci(xs, ys, idx)
        outcomes[key] = dict(n_pairs_used=int(both.sum()),
                             arm_mean=float(np.mean(xs[both])) if both.any() else None,
                             ref_mean=float(np.mean(ys[both])) if both.any() else None,
                             mean_diff=paired_stat(xs, ys), ci_lo=lo_k, ci_hi=hi_k, n_boot_defined=nb)
        if key == 'time_lost_s':
            cl, ch = boot_ci_conditional(xs, ys)
            outcomes[key]['ci_conditional_lo'] = cl; outcomes[key]['ci_conditional_hi'] = ch
    res['outcomes'] = outcomes
    t = outcomes['time_lost_s']
    res['time_lost_pairs_without_contact'] = t['n_pairs_used']
    res['time_lost_diff'] = t['mean_diff']; res['time_lost_lo'] = t['ci_lo']; res['time_lost_hi'] = t['ci_hi']
    cls, holds = classify(lo, hi, t['ci_lo'], t['ci_hi'])
    res['classification'] = cls
    res['rules_satisfied'] = holds
    return res


def index_runs(runs):
    """Valid runs only, keyed (arm, level, lead_variant) -> {case: row}. Duplicates: the last by run id, with a note."""
    idx = {}
    notes = []
    for r in sorted((r for r in runs if r.get('valid')), key=lambda r: r['run_id']):
        key = (r.get('arm'), r.get('level'), r.get('lead_variant'))
        d = idx.setdefault(key, {})
        if r['case'] in d:
            notes.append('duplicate valid run for %s case %s: using %s over %s' % (key, r['case'], r['run_id'], d[r['case']]['run_id']))
        d[r['case']] = r
    return idx, notes


HYP = {('E_CK3', 'lo', 'E_F0'): 'E-H1', ('E_N', 'lo', 'E_F0'): 'E-H2', ('E_N_IMM', 'lo', 'E_F0_IMM'): 'E-H3'}


def cmd_compare(a):
    low_power = a.low_power
    runs = load_runs_file(a.outcomes)
    idx, notes = index_runs(runs)
    results = []
    n_runs_total = len(runs); n_valid = sum(1 for r in runs if r.get('valid'))

    def get(arm, level, lv=None):
        return idx.get((arm, level, lv), {})

    # lead-braking cases (E3): arm vs F0 at the same level; N_IMM vs F0_IMM; Z vs F0 at each level
    for level in ('lo', 'hi'):
        for arm in ('E_N', 'E_CK3', 'E_TG', 'E_PS'):
            ref = 'E_F0'
            results.append(compare_pair(get(arm, level), get(ref, level), '%s vs %s at %s' % (arm, ref, level),
                                        dict(set='E3', arm=arm, reference=ref, level=level, hypothesis=HYP.get((arm, level, ref)))))
        results.append(compare_pair(get('E_N_IMM', level), get('E_F0_IMM', level), 'E_N_IMM vs E_F0_IMM at %s' % level,
                                    dict(set='E3', arm='E_N_IMM', reference='E_F0_IMM', level=level,
                                         hypothesis=HYP.get(('E_N_IMM', level, 'E_F0_IMM')))))
        results.append(compare_pair(get('E_F0_IMM', level), get('E_F0', level), 'E_F0_IMM vs E_F0 at %s (extra)' % level,
                                    dict(set='E3', arm='E_F0_IMM', reference='E_F0', level=level, hypothesis=None, extra_pair=True)))
        z = idx.get(('E_Z', None, None), {})
        results.append(compare_pair(z, get('E_F0', level), 'E_Z vs E_F0 at %s' % level,
                                    dict(set='E3', arm='E_Z', reference='E_F0', level=level, hypothesis=None)))
    # E3b: per lead variant at lo
    if a.e3b:
        runs_b = load_runs_file(a.e3b)
        idx_b, notes_b = index_runs(runs_b)
        notes += notes_b
        variants = sorted({k[2] for k in idx_b if k[2] is not None})
        for lv in variants:
            for arm in ('E_N', 'E_CK3', 'E_PS', 'E_TG'):
                results.append(compare_pair(idx_b.get((arm, 'lo', lv), {}), idx_b.get(('E_F0', 'lo', lv), {}),
                                            '%s vs E_F0 at lo, lead variant %s' % (arm, lv),
                                            dict(set='E3b', arm=arm, reference='E_F0', level='lo', lead_variant=lv, hypothesis=None)))
        n_runs_total += len(runs_b); n_valid += sum(1 for r in runs_b if r.get('valid'))
    for r in results:
        r['low_power_label'] = bool(low_power) if r.get('set') == 'E3' or r.get('set') == 'E3b' else None
    write_json(dict(schema='E_RECOUNT_COMPARE_v01', low_power=bool(low_power), n_runs=n_runs_total, n_valid_runs=n_valid,
                    notes=notes, comparisons=results), a.out)
    print('wrote %s: %d comparisons (low_power=%s)' % (a.out, len(results), low_power))
    for r in results:
        if r.get('hypothesis'):
            print('  %s %s -> %s' % (r['hypothesis'], r['label'], r['classification']))


# ----------------------------------------------------------------------------- 7.3 matched settings (open-loop, old runs)
RUNS_V11 = r'ARS_TRIAL\revision_v11\analysis\rev_common_v01.py'
TG_DIR = r'ARS_TRIAL\revision_v12\analysis\out\tg'
LEAD_DIR = r'ARS_TRIAL\revision_v12\analysis\out\lead'
IMM_DIR = r'ARS_TRIAL\revision_v13\work\B_retrack\out\retrack\B1'
PS_THRESHOLD = -1.0          # braking if along-velocity acceleration of the lead track <= this (A10 2.4)
STOP_SPEED = 0.5             # stopped if lead track speed <= this


def load_old_runs():
    """The 35 old evaluation runs with their critical arrays, via the loader of record (rev_common_v01.load_runs)."""
    import importlib.util
    sys.path.insert(0, str(Path(RUNS_V11).parent))
    spec = importlib.util.spec_from_file_location('rev_common_v01', RUNS_V11)
    rc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rc)
    return rc, rc.load_runs()


def caution_curve(rc, runs, crit_by_run, grid):
    """Open-loop caution (%) and wrong go (%) at every scale of `grid`: scoring 'W1' (safe = clear1 > 0), population 'all'
    (all evaluated decisions), summed over the 35 runs; caution = sum of speed shortfalls / number of selected-safe decisions."""
    L = rc.L
    T = None
    for r, c in zip(runs, crit_by_run):
        sel = L.select_grid(c, grid, r['idx55'])
        st = L.stats_scored(sel, r['clear1'], r['clear1'] > 0., r['vbar'], r['desired'], (r['ev'],))[:, 0, :]
        T = st if T is None else T + st
    wrong, caution, _ = L.rates(T)
    return caution, wrong


def nearest_scale(caution, target):
    """Index of the grid scale whose caution is nearest target; ties to the smaller scale (ascending grid, first minimum)."""
    return int(np.argmin(np.abs(np.asarray(caution) - target)))


def tracker_phase(lead):
    """A10 2.4 with threshold -1.0 on the stored tracker estimate: 2 stopped (speed <= 0.5), 1 braking (above that and
    along-velocity acceleration <= -1.0), 0 before braking (otherwise, or no lead track)."""
    f = lead['lead_found']; v = lead['vhat']; a = lead['ahat_long']
    return np.where(~f, 0, np.where(v <= STOP_SPEED, 2, np.where(a <= PS_THRESHOLD, 1, 0))).astype(int)


def cmd_matched(a):
    calib = read_json(a.calib)
    levels = {'lo': float(calib['g_lo']), 'hi': float(calib['g_hi'])}
    rc, runs = load_old_runs()
    L = rc.L
    GRID = rc.GRID
    G = len(GRID)
    crit = {'F0': [r['crit']['F0'] for r in runs], 'N': [r['crit']['N'] for r in runs], 'CK3': [r['crit']['CK3'] for r in runs],
            'TG': [], 'F0_IMM': [], 'N_IMM': []}
    problems = []
    for r in runs:
        z = np.load(Path(TG_DIR) / (r['run'] + '.npz'), allow_pickle=False)
        if not np.array_equal(z['k'], r['k']):
            problems.append('TG k differs for ' + r['run'])
        crit['TG'].append(z['cTG2'])
        b = np.load(Path(IMM_DIR) / (r['run'] + '_arrays.npz'), allow_pickle=False)
        if not (np.array_equal(b['k'], r['k']) and np.array_equal(b['idx55'], r['idx55']) and np.array_equal(b['evaluated'], r['ev'])):
            problems.append('IMM arrays differ in k/idx55/evaluated for ' + r['run'])
        crit['F0_IMM'].append(b['cF0']); crit['N_IMM'].append(b['cN'])
    curves = {arm: caution_curve(rc, runs, crit[arm], GRID) for arm in crit}

    # per-phase tables for the PS triple (F0's critical values, tracker-estimated phase)
    TP = None
    for r in runs:
        z = np.load(Path(LEAD_DIR) / (r['run'] + '.npz'), allow_pickle=False)
        if not np.array_equal(z['k'], r['k']):
            problems.append('lead k differs for ' + r['run'])
        ph = tracker_phase(z)
        sel = L.select_grid(r['crit']['F0'], GRID, r['idx55'])
        masks = tuple(r['ev'] & (ph == p) for p in range(3))
        st = L.stats_scored(sel, r['clear1'], r['clear1'] > 0., r['vbar'], r['desired'], masks)
        TP = st if TP is None else TP + st                   # (G, 3, 5)
    ndec = TP[0, :, 0].sum()
    wg = TP[:, :, 1]; ct = TP[:, :, 2]; cn = TP[:, :, 3]
    # all G^3 triples: index order (phase 0, phase 1, phase 2) with phase 0 the slowest index
    W = wg[:, 0][:, None, None] + wg[:, 1][None, :, None] + wg[:, 2][None, None, :]
    CT = ct[:, 0][:, None, None] + ct[:, 1][None, :, None] + ct[:, 2][None, None, :]
    CN = cn[:, 0][:, None, None] + cn[:, 1][None, :, None] + cn[:, 2][None, None, :]
    with np.errstate(divide='ignore', invalid='ignore'):
        CAUT = 100.0 * CT / CN
    WRONG = 100.0 * W / ndec
    cF0, wF0 = curves['F0']
    diag_c = np.array([CAUT[i, i, i] for i in range(G)]); diag_w = np.array([WRONG[i, i, i] for i in range(G)])
    out = dict(schema='E_RECOUNT_MATCHED_v01', calibration_file=str(a.calib), levels=levels, n_runs=len(runs), grid_size=G,
               alignment_problems=problems, n_evaluated_decisions=float(ndec), phase_decisions=[float(x) for x in TP[0, :, 0]],
               ps_single_scale_check_max_abs_diff=dict(caution=float(np.nanmax(np.abs(diag_c - cF0))),
                                                       wrong_go=float(np.nanmax(np.abs(diag_w - wF0)))),
               levels_out={})
    for name, gL in levels.items():
        c_gl, w_gl = caution_curve(rc, runs, crit['F0'], np.array([gL]))
        lvl = float(c_gl[0])
        res = dict(g_L=gL, F0_caution_at_gL=lvl, F0_wrong_go_at_gL=float(w_gl[0]), arms={})
        for arm in ('N', 'CK3', 'TG', 'F0_IMM', 'N_IMM'):
            caut, wrong = curves[arm]
            i = nearest_scale(caut, lvl)
            res['arms'][arm] = dict(g=float(GRID[i]), grid_index=i, caution=float(caut[i]), abs_diff=float(abs(caut[i] - lvl)),
                                    wrong_go=float(wrong[i]))
        ok = np.isfinite(CAUT) & (CAUT <= lvl + 1e-12)
        if ok.any():
            flat = np.flatnonzero(ok.ravel())
            wv = np.round(WRONG.ravel()[flat], 9); cv = np.round(CAUT.ravel()[flat], 9)
            order = np.lexsort((flat, cv, wv))       # primary wrong go, then caution, then flat index
            best = int(flat[order[0]])
            i0, i1, i2 = np.unravel_index(best, (G, G, G))
            res['arms']['PS'] = dict(triple=[float(GRID[i0]), float(GRID[i1]), float(GRID[i2])],
                                     grid_indices=[int(i0), int(i1), int(i2)], flat_index=best, caution=float(CAUT[i0, i1, i2]),
                                     wrong_go=float(WRONG[i0, i1, i2]), n_triples_feasible=int(ok.sum()))
        else:
            res['arms']['PS'] = None
        out['levels_out'][name] = res
    write_json(out, a.out)
    print('wrote', a.out, 'problems:', problems)
    for name, res in out['levels_out'].items():
        print(name, 'g_L', res['g_L'], 'F0 caution', round(res['F0_caution_at_gL'], 4))
        for arm, v in res['arms'].items():
            print('  ', arm, v)


# ----------------------------------------------------------------------------- command line
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('outcomes'); s.add_argument('runs_dir'); s.add_argument('prefix'); s.add_argument('--out', required=True)
    s.set_defaults(f=cmd_outcomes)
    s = sp.add_parser('brake'); s.add_argument('runs_dir'); s.add_argument('--out', required=True); s.set_defaults(f=cmd_brake)
    s = sp.add_parser('calibration'); s.add_argument('outcomes'); s.add_argument('--out', required=True); s.set_defaults(f=cmd_calibration)
    s = sp.add_parser('compare'); s.add_argument('outcomes'); s.add_argument('--e3b', default=None)
    s.add_argument('--low-power', type=parse_bool, required=True); s.add_argument('--out', required=True)
    s.set_defaults(f=cmd_compare)
    s = sp.add_parser('matched'); s.add_argument('--calib', required=True); s.add_argument('--out', required=True)
    s.set_defaults(f=cmd_matched)
    a = p.parse_args(argv)
    a.f(a)


if __name__ == '__main__':
    main()
