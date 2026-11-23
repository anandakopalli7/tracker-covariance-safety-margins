"""Package E, first program: per-run closed-loop outcomes (A10 section 7.4), from the 20 Hz truth logs.

Writer: session E (Claude Opus 5.5). The independent second program is written by a different model from the
amendment text and the raw truth logs (A10 section 10.1(b)); it must not read this file.

Input: one capture folder (the probe's --out, e.g. <archive>/x/<job>/capture/<case>), holding
  evaluation_truth.jsonl (one record per physical tick k = 0..N-1, 0.05 s apart, ego and target boxes and velocities),
  frames.jsonl (applied controls and the planner's decisions), contacts.jsonl (absent when no contact event),
  assessment_outcomes.json (frame bookkeeping of the run).

Definitions (A10 7.4), fixed here before any closed-loop run exists:
  assessment window  ticks k = 99 .. last tick; tick 99 is the first assessment decision (frames base+100 .. base+700).
  contact            any collision-sensor contact event at or after the window start, or a tick of the window at which the
                     truth gap (directional_gap_m, ego to the scenario's primary actor) is <= 0 while the two boxes also overlap
                     in the ground plane (separating-axis test on the axes of both boxes, from the truth box vertices): the gap alone is longitudinal and is negative for an actor beside or behind the ego (review M5; revised 19 Nov before any
                     E data existed).
  first contact tick the earlier of the first contact event's tick and the first such overlapping tick.
  impact speed       closing speed along the route at the first contact: (ego velocity - target velocity) . route tangent,
                     from the truth velocities of the last tick before the first contact tick (the contact tick's velocities may
                     already include the collision impulse; review Minor 7), or of the contact tick if it is the window's first.
                     NaN without contact.
  time lost          for runs without contact: window length (s) minus distance travelled along the route over the
                     window divided by the desired speed. Window length = (last tick - 99) * 0.05 s; distance =
                     route projection of the ego centre at the last tick minus that at tick 99. NaN with contact.
  rest gap           the gap to the stopped lead at the end of the run: truth gap at the last tick, for runs without contact
                     whose primary actor at that tick is stopped (speed <= 0.5 m/s), ahead (gap > 0) and laterally overlapping
                     the ego (in path); NaN otherwise (revised 19 Nov before any E data existed). lead_end_speed_mps beside it.
  peak deceleration  max over the window of -dv/dt, v = ego speed (norm of the truth velocity), smoothed by a centred
                     0.25 s moving average (5 samples at 20 Hz; samples outside the window are not used, so the
                     smoothed series covers ticks 101 .. last-2); dv/dt by forward difference / 0.05 s.
  RMS jerk           root mean square of the forward difference of that acceleration series / 0.05 s.
  fallback share     share of the window's planner decisions (frames with execution.new_decision, tick >= 99) in full
                     braking: the selected plan is the (-5, -5) row, whether as the fallback (output.fallback) or as the first
                     feasible row (review Minor 8).
"""
import json, math, pathlib, sys

DT = 0.05
WINDOW_START_K = 99
SMOOTH = 5


def jl(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def _route_axis(truth0):
    yaw = float(truth0['ego']['derived']['route_yaw_rh'])
    return (math.cos(yaw), math.sin(yaw))


def _vel_rh(rec):
    v = rec['velocity_lh']
    return (float(v[0]), -float(v[1]))            # left-handed CARLA world -> right-handed (y flipped)


def _span(rec, ax, ay):
    vs = [float(v[0]) * ax + float(v[1]) * ay for v in rec['derived']['vertices_rh']]
    return min(vs), max(vs)


def _lateral_overlap(t, yaw):
    """Do the ego and target boxes overlap across the route (vertices projected on the route normal)?"""
    a0, a1 = _span(t['ego'], -math.sin(yaw), math.cos(yaw)); b0, b1 = _span(t['target'], -math.sin(yaw), math.cos(yaw))
    return max(a0, b0) <= min(a1, b1)


def _box_overlap(t, yaw):
    """Do the two boxes overlap in the ground plane? Separating-axis test on the four axes of the two boxes (each box's
    heading and its normal); vertices are the truth box vertices (x, y)."""
    axes = []
    for rec in (t['ego'], t['target']):
        h = float(rec['derived']['heading_rh'])
        axes += [(math.cos(h), math.sin(h)), (-math.sin(h), math.cos(h))]
    for ax, ay in axes:
        a0, a1 = _span(t['ego'], ax, ay); b0, b1 = _span(t['target'], ax, ay)
        if max(a0, b0) > min(a1, b1):
            return False
    return True


def outcomes(cap, desired_mps):
    cap = pathlib.Path(cap)
    truth = list(jl(cap / 'evaluation_truth.jsonl'))
    if not truth:
        raise ValueError('empty truth log: ' + str(cap))
    ks = [int(t['k']) for t in truth]
    if ks != list(range(len(truth))):
        raise ValueError('truth ticks not consecutive from 0: ' + str(cap))
    if len(truth) <= WINDOW_START_K:
        raise ValueError('run ended before the assessment window: ' + str(cap))
    ux, uy = _route_axis(truth[0]); yaw0 = float(truth[0]['ego']['derived']['route_yaw_rh'])
    base = json.loads((cap / 'assessment_outcomes.json').read_text(encoding='utf-8'))
    base_frame = int(base['base_frame'])
    # contact events (collision sensor), mapped to ticks k = frame - base_frame - 1
    events = list(jl(cap / 'contacts.jsonl')) if (cap / 'contacts.jsonl').exists() else []
    event_ks = sorted(int(e['frame']) - base_frame - 1 for e in events)
    warmup_event = any(k < WINDOW_START_K for k in event_ks)
    event_ks = [k for k in event_ks if k >= WINDOW_START_K]
    gap_ks = [t['k'] for t in truth if t['k'] >= WINDOW_START_K and float(t['directional_gap_m']) <= 0.0 and _box_overlap(t, yaw0)]
    candidates = ([event_ks[0]] if event_ks else []) + ([gap_ks[0]] if gap_ks else [])
    contact = bool(candidates)
    first_k = min(candidates) if contact else None
    last_k = len(truth) - 1
    out = dict(capture=str(cap), desired_mps=float(desired_mps), ticks=len(truth), last_k=last_k,
               contact=int(contact), contact_by_event=int(bool(event_ks)), contact_by_gap=int(bool(gap_ks)),
               warmup_contact_event=int(warmup_event), first_contact_k=first_k)
    if contact:
        kk = max(first_k - 1, WINDOW_START_K) if first_k > WINDOW_START_K else first_k
        t = truth[min(kk, len(truth) - 1)]
        ve, vt = _vel_rh(t['ego']), _vel_rh(t['target'])
        out['impact_speed_mps'] = (ve[0] - vt[0]) * ux + (ve[1] - vt[1]) * uy
    else:
        out['impact_speed_mps'] = float('nan')
    # distance and time lost
    def proj(t):
        c = t['ego']['derived']['center_rh']
        return float(c[0]) * ux + float(c[1]) * uy
    window_s = (last_k - WINDOW_START_K) * DT
    dist = proj(truth[last_k]) - proj(truth[WINDOW_START_K])
    out['window_s'] = window_s
    out['distance_m'] = dist
    out['time_lost_s'] = float('nan') if contact else window_s - dist / float(desired_mps)
    if contact:
        out['rest_gap_m'] = float('nan')
    else:
        tl = truth[last_k]; g = float(tl['directional_gap_m']); vt_end = _vel_rh(tl['target'])
        stopped_ahead = math.hypot(vt_end[0], vt_end[1]) <= 0.5 and g > 0. and _lateral_overlap(tl, yaw0)
        out['rest_gap_m'] = g if stopped_ahead else float('nan')
    vt = _vel_rh(truth[last_k]['target'])
    out['lead_end_speed_mps'] = math.hypot(vt[0], vt[1])
    # smoothed speed, deceleration, jerk over the window
    v = []
    for t in truth[WINDOW_START_K:]:
        ve = _vel_rh(t['ego'])
        v.append(math.hypot(ve[0], ve[1]))
    half = SMOOTH // 2
    vs = [sum(v[i - half:i + half + 1]) / SMOOTH for i in range(half, len(v) - half)]
    acc = [(vs[i + 1] - vs[i]) / DT for i in range(len(vs) - 1)]
    jerk = [(acc[i + 1] - acc[i]) / DT for i in range(len(acc) - 1)]
    out['peak_decel_mps2'] = max([-a for a in acc]) if acc else float('nan')
    out['rms_jerk_mps3'] = math.sqrt(sum(j * j for j in jerk) / len(jerk)) if jerk else float('nan')
    # fallback share
    n = f = 0
    for fr in jl(cap / 'frames.jsonl'):
        ex = fr.get('execution')
        if not ex or not ex.get('new_decision'):
            continue
        d = ex['new_decision']
        if int(d['tick']) < WINDOW_START_K:
            continue
        n += 1
        tg = [float(x) for x in (d['output'].get('targets') or [])]
        f += int(bool(d['output'].get('fallback')) or tg == [-5., -5.])
    out['decisions'] = n
    out['fallback_decisions'] = f
    out['fallback_share'] = f / n if n else float('nan')
    return out


if __name__ == '__main__':
    cap, desired = sys.argv[1], float(sys.argv[2])
    print(json.dumps(outcomes(cap, desired), indent=1, allow_nan=True))
