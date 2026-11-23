"""Revision v13, package D1: ScenarioActors whose policy is the D1 lead-variant actor-request version.

scenario_actors_class(case) returns scene_actors_v03.ScenarioActors itself for a case without `lead_variant`
(so every other case runs the unchanged class). For a D1 case it returns a subclass whose start() is
ScenarioActors.start with ActorRequests replaced by actor_policy_d1_v01.LeadVariantRequests; every other method
(spawn, release, observe, step, PID) is inherited unchanged.
"""
from scene_actors_v03 import ScenarioActors, ActorPID
from actor_policy_d1_v01 import LeadVariantRequests, check_variant


def scenario_actors_class(case):
    variant = case.get('lead_variant')
    if variant is None:
        return ScenarioActors
    check_variant(variant, case['draw'])

    class VariantScenarioActors(ScenarioActors):
        def start(self, frame, ego_center_rh, ego_velocity_rh, ego_half_diagonal, *, reactive=True):
            # Body of scene_actors_v03.ScenarioActors.start with the policy class replaced.
            if not self.released or self.policy is not None: raise ValueError('Invalid actor-policy start')
            m = self.observe(frame)[0]
            if m['center_velocity_route_rh'] is None: raise ValueError('No causal physical velocity observation')
            self.policy = LeadVariantRequests(self.draw, frame, reactive=reactive, variant=variant)
            if not m['asset'].startswith('walker.'): self.native = ActorPID(self.pid_observation(m), frame)
            return self.step(frame, ego_center_rh, ego_velocity_rh, ego_half_diagonal)

    return VariantScenarioActors
