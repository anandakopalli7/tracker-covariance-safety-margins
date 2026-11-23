"""Revision v13, package D1 (AMENDMENT_10_v13.md sec. 6): three non-braking lead variants on the lead-braking generator.

New actor-policy version for packet_d1_v13. It changes ONLY the primary actor's requested speed in cases that carry
a `lead_variant` record; the case's `draw` stays a valid 746 lead-braking Draw, so placement, initial gap, steering
aim, PID, sensors, detector, tracker and planner are the lead-braking generator unchanged. Cases without
`lead_variant` get the unchanged 746 ActorRequests (this module then returns that class itself).

Variants (t = assessment time in s, as in 746: (frame - first_frame) * 0.05 - 5; v = desired speed):
  constant      the lead keeps its initial speed: request = v.
  mild_braking  from start_s (U(1,3), = draw.brake_start_s) the lead decelerates at decel_mps2 (U(0.5,1.5)) to
                floor_fraction * v (floor_fraction = 0.5), then holds it: request = max(0.5 v, v - a * max(0, t - start_s)).
  stop_and_go   the lead brakes at decel_mps2 (U(2,6), = draw.brake_mps2) from start_s (= draw.brake_start_s) to a stop,
                holds hold_s = 3 s, then accelerates at resume_mps2 = 1.5 m/s^2 to its initial speed:
                t_stop = start_s + v / b;  t < t_stop + hold_s: request = max(0, v - b * max(0, t - start_s))  (746 law)
                otherwise: request = min(v, resume_mps2 * (t - t_stop - hold_s)).
Pure functions of t, like the 746 lead_braking law; no reactivity.
"""
import math, pathlib, sys

_WS = pathlib.Path(__file__).resolve().parent.parent          # /opt/programme_a_gpu750/workspace on the pod
_P746 = str(_WS / '746_actual_actor_policy_development_20261103')
if _P746 not in sys.path:
    sys.path.insert(0, _P746)
from actor_policy_v01 import ActorRequests, Draw   # noqa: E402  (the same module object scene_actors_v03 imports)

SCHEMA = 'LEAD_VARIANT_D1V13_V01'
KINDS = ('constant', 'mild_braking', 'stop_and_go')
FIELDS = ('schema', 'kind', 'start_s', 'decel_mps2', 'floor_fraction', 'hold_s', 'resume_mps2')


def check_variant(variant, draw):
    """Validate a lead_variant record against its case draw (a dict or a Draw). Raises ValueError."""
    if not isinstance(variant, dict) or set(variant) != set(FIELDS) or variant['schema'] != SCHEMA:
        raise ValueError('Invalid lead_variant record')
    d = draw if isinstance(draw, dict) else draw.__dict__
    if d['family'] != 'lead_braking':
        raise ValueError('lead_variant is defined on the lead_braking family only')
    k = variant['kind']
    if k not in KINDS:
        raise ValueError('Unknown lead variant')
    def num(x):
        return type(x) in (int, float) and math.isfinite(x)
    if k == 'constant':
        if any(variant[f] is not None for f in ('start_s', 'decel_mps2', 'floor_fraction', 'hold_s', 'resume_mps2')):
            raise ValueError('constant variant takes no parameters')
    elif k == 'mild_braking':
        if not (num(variant['start_s']) and num(variant['decel_mps2']) and 1 <= variant['start_s'] <= 3 and 0.5 <= variant['decel_mps2'] <= 1.5):
            raise ValueError('mild_braking parameters outside their support')
        if variant['start_s'] != d['brake_start_s'] or variant['floor_fraction'] != 0.5 or variant['hold_s'] is not None or variant['resume_mps2'] is not None:
            raise ValueError('mild_braking record inconsistent')
    else:
        if not (num(variant['start_s']) and num(variant['decel_mps2']) and 1 <= variant['start_s'] <= 3 and 2 <= variant['decel_mps2'] <= 6):
            raise ValueError('stop_and_go parameters outside their support')
        if (variant['start_s'] != d['brake_start_s'] or variant['decel_mps2'] != d['brake_mps2'] or variant['floor_fraction'] is not None
                or variant['hold_s'] != 3.0 or variant['resume_mps2'] != 1.5):
            raise ValueError('stop_and_go record inconsistent')
    return True


def requested_speed(variant, v, t):
    """Requested lead speed (m/s) at assessment time t (s) for a validated variant and desired speed v."""
    k = variant['kind']
    if k == 'constant':
        return float(v)
    a, t0 = variant['decel_mps2'], variant['start_s']
    if k == 'mild_braking':
        return float(max(variant['floor_fraction'] * v, v - a * max(0., t - t0)))
    t_stop = t0 + v / a
    if t < t_stop + variant['hold_s']:
        return float(max(0., v - a * max(0., t - t0)))
    return float(min(v, variant['resume_mps2'] * (t - t_stop - variant['hold_s'])))


class LeadVariantRequests(ActorRequests):
    """746 ActorRequests with the lead's speed request replaced by the variant law. Everything else is 746's step."""

    def __init__(self, d, first_frame, *, reactive=True, variant):
        super().__init__(d, first_frame, reactive=reactive)
        check_variant(variant, d)
        self.variant = dict(variant)

    def step(self, frame, **kw):
        out = super().step(frame, **kw)          # validates frame order and inputs; computes aim and the 746 request
        request = requested_speed(self.variant, self.draw.desired_mps, out['assessment_time_s'])
        self.request = request
        out['requested_speed_mps'] = request
        out['reason'] = 'lead_variant_' + self.variant['kind']
        return out

    def snapshot(self):
        s = super().snapshot()
        s['schema'] = 'ACTOR_REQUESTS746_D1V13_V01'
        s['lead_variant'] = dict(self.variant)
        return s

    @classmethod
    def restore(cls, state):
        raise NotImplementedError('Restore is not used in capture or review')


def make_requests(case, draw, first_frame):
    """The actor-request object for a protocol case (used by the actor-record review)."""
    variant = case.get('lead_variant')
    if variant is None:
        return ActorRequests(draw, first_frame, reactive=case['reactive'])
    check_variant(variant, case['draw'])
    return LeadVariantRequests(draw, first_frame, reactive=case['reactive'], variant=variant)
