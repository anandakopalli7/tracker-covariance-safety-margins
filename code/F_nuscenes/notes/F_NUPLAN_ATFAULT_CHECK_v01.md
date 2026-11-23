# nuPlan's at-fault collision rule, as read in the nuplan-devkit source (for package A's wording)

Written 20 Nov 2026, about 00:15 EST, by session F, as required by condition 5 of the coordinator's decision of 19 Nov (23:58 EST). Purpose: F's clearance departure (`notes\F_DEPARTURE_CLEARANCE_v01.md`) may cite nuPlan's convention **only as comparable**. This note records what that convention is in the source, not from memory.

## Source read
- **Repository and revision:** public GitHub repository `motional/nuplan-devkit`, branch `master`, commit `e9241677997dd86bfc0bcd44817ab04fe631405b` (commit date 2025-08-27). Read on 20 Nov 2026.
- **Files** (saved in F's scratch folder; SHA-256 of the copies read):
  - `nuplan/planning/metrics/evaluation_metrics/common/no_ego_at_fault_collisions.py`: `6d1a5a1aef78bc22e3d1bf1fa943bf0a49e20c48d28dc1dd737cee1440f4cb03`
  - `nuplan/planning/metrics/utils/collision_utils.py`: `99f130d4fa9e1bf9a8444d94050d443478f033402fdeaf69c1f5836b139c8c3a`
  - `nuplan/planning/simulation/observation/idm/utils.py`: `f818aebc8637ef5ce5eec82cef8b4992c5620ad57a9013de1c04a78705463fef`
- `collision_utils.py` and the IDM utilities were fetched at `master` / that commit.

## The rule in the source (paraphrased)
- **Collision events.** A collision is the first time step at which the ego's oriented box intersects a tracked object's box. Each track can collide at most once per scenario (`find_new_collisions`). The collision is classified at that time step (`_get_collision_type`), in this order:
  1. **Stopped ego:** ego speed ≤ 0.05 m/s.
  2. **Stopped track:** the object is not an agent (a static object), or its speed is ≤ 0.05 m/s.
  3. **Active rear:** the track is behind the ego (`is_agent_behind`). The angle between the ego's heading and the vector from the ego's **rear-axle** pose to the track's **box centre** exceeds **150°** (`get_agent_relative_angle`, `angle_tolerance=150`).
  4. **Active front:** the ego box's front edge intersects the track's box.
  5. **Active lateral:** otherwise.
- **At fault** (`classify_at_fault_collisions`): active-front and stopped-track collisions always count. Active-lateral collisions count only at time steps where the ego is in multiple lanes or a non-drivable area (from the lane-change metric). **Stopped-ego and active-rear collisions are not at fault.**
- **Not complete by its own account:** the source's own docstring calls these "collisions that could have been prevented if planner performed differently" and says the classification "is not complete".

## How F's departure differs (so "comparable", not "the same")
| Aspect | nuPlan (source above) | F's departure |
|---|---|---|
| What is excluded | Whole collision events, classified once per track | (actor, frame) pairs inside the clearance minimum |
| "Behind" test | Angle > 150° from the ego heading, measured from the **rear axle** to the track centre | Longitudinal coordinate < 0 in the ego frame, measured from the **box centre** (angle > 90°) |
| Ego stopped | Never at fault | No special case: contacts with actors not behind still count |
| Track stopped | Always at fault (even if behind) | No special case: a stopped actor behind is dropped |
| Lateral contacts | At fault only when the ego spans lanes | No special case: counted unless the actor's centre is behind |
| Use | A pass/fail metric score | The W1 safety test (clearance > 0) inside the scoring of record |

- **Shared idea:** neither counts a contact in which a moving agent strikes the ego from behind.
- **Where F excludes more:** F's rule also drops side-rear pairs (90°–150° from the ego centre), which nuPlan would classify as front or lateral, and it also drops stopped actors behind the ego.
- **Where nuPlan excludes more:** every collision while the ego is stopped.

## Suggested wording for package A (to be checked by A)
"…a rule comparable to, but not the same as, nuPlan's at-fault collision classification (nuplan-devkit, `no_ego_at_fault_collisions.py`), which does not count rear collisions by moving agents…"
- Do not write that F "follows" or "uses" nuPlan's rule.
