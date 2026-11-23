# Second-program check of the nuScenes adapter (A10 10.1(b))

Model: Claude Sonnet 5.5 (claude-sonnet-5-5). Code: `check2_adapter_v01.py`. Output: `ADAPTER_CHECK2_v01.json`.
Written only from `ADAPTER_SPEC_F_v01.md` sections 1-5 and the raw nuScenes metadata. I did not open the first program's code or cache.
Python 3.12, numpy only (plus the shared planner library `finite_primitive.build_library`); run with `python -I`.

## What was implemented
- Streaming readers for the big pretty-printed JSON files (one record per `{` ... `}` block); only the 20 scenes' LIDAR_TOP sweeps, their ego poses and the scenes' sample annotations were kept.
- Train-split assertion: all 20 scenes are in the devkit `train` list (read as text; no val data touched).
- Spec 2: sweeps, yaw, ego box centre (rear axle + 1.294 m), travel, quadratic fit on |t - t_i| <= 0.5 s (+1e-9), v_raw = b, a_raw = 2q, desired speed = clip(max v_raw, 1, 20), route with 0.25 m / forward-direction vertex rule and 400 m extensions, projection over ALL segments (first minimum wins ties), s, l, theta.
- Spec 3: truth classes, truth at time t (keyframe annotation, or linear interpolation through `next`, yaw via wrap), truth actors at `now`, 61-frame windows stopped at first missing frame.
- Spec 4/5: rows from `build_library(v0, a0, desired, [], 4.084, 1.730, now, Diagnostics())`; planner-frame mapping of each actor centre by its own projection, heading = yaw - theta; own rectangle distance (separating-axis overlap test, else min vertex-to-edge distance both directions); clearance = min over actors and frames j = 0..60 (3 s). "inf" when no actor has truth in the window.
- Outputs per decision: v_raw, a_raw, v0, desired, s_e, l_e, theta_e, number of truth actors at now, targets and 3 s clearance of each of the 17 rows (cost order).

## Ambiguities and how I resolved them
1. **Split lists:** the devkit file defines `train = sorted(set(train_detect + train_track))`, with no literal `train` list. I took the union of the two lists (check: 700 scenes).
2. **Keyframe bracketing "last keyframe with kf_t[k] <= t":** applied literally with no tolerance, and then the 1e-9 test against kf_t[k]. A time a hair below kf_t[k+1] therefore uses interpolation with w ~ 1 (continuous with the keyframe value, so no practical effect).
3. **Actors "with truth at now":** an instance needs an annotation at the bracketing keyframe k. Size comes from that annotation (half length size[1]/2, half width size[0]/2).
4. **Frame window:** an actor's window stops at the first j without truth, so later frames are excluded (not treated as NaN distances). Row positions are taken at the same j.
5. **Route tangent for projection:** theta interpolated linearly between the unwrapped point tangents of the segment ends, as stated; extension points take the neighbour's tangent. The actor's heading is yaw (as wrapped by the quaternion formula, unwrapped ego tangents are not re-wrapped) minus theta. Because theta can differ from the wrapped yaw by a multiple of 2 pi, the rectangle is unaffected (corners use cos/sin).
6. **Ego sweep for `now`:** found by exact timestamp match of the decision's `sweep_timestamp_us`; `now` is checked against the decisions file to 1e-6 s.
7. **Ego-centre projection uses c_i** (box centre, not pose), per the spec's "ego centre".
8. **Sweeps of the scene:** LIDAR_TOP records whose `sample_token` is one of the scene's samples (including after the last keyframe if any); not otherwise trimmed.
9. **Touch case:** overlap test uses strict separation, so touching boxes give 0, and the vertex-to-edge distance is also ~0 in that case.

# v02 (clearance under the recorded departure)

Model: Claude Sonnet 5.5 (claude-sonnet-5-5). Code: `check2_adapter_v02.py`. Output: `ADAPTER_CHECK2_v02.json`. Run with `python -I`, numpy plus the shared planner library; run time 290 s. Written once; I did not open the first program's code, cache, out, recount or logs.

## What changed
- Copy of v01 with one addition, implemented from section 2 of `F_DEPARTURE_CLEARANCE_v01.md`: for each row, frame j and actor, x_rel = c_x(j) - S_r[j] (ego centre (S_r[j], 0), heading 0, c_x = the actor centre's planner-frame x already used in v01). The pair is dropped when x_rel < 0 (strict); x_rel = 0 is kept. The clearance is the minimum rectangle distance over kept pairs, "inf" if none remain.
- Each record carries `clearance_3s_v01` (rule of record, same computation as v01) and `clearance_3s` (new rule), plus `n_pairs_dropped` (summed over the 17 rows, over all (actor, frame) pairs inside each actor's truth window).
- Built-in checks: `clearance_3s_v01` equals `clearance_3s` of `ADAPTER_CHECK2_v01.json` for all 20 x 17 values (largest difference 0.0, exact); every new clearance >= the v01 one (true).

## Ambiguities
1. Frame set of dropped pairs: the departure does not say how to count pairs where the actor has no truth at frame j. I count only pairs that exist (frames in the actor's truth window, which stops at the first missing frame, as in v01). Does not affect clearances.
2. "Actor centre x in the planner frame" is the same planner-frame x as in v01 (route-projection s minus s_e); I did not re-derive it. The departure's c_x(f) is read as that quantity.
3. The ego box and the truth box overlap/touch test is unchanged (separating axis, strict separation); dropping happens after the distance is computed, which is equivalent to filtering before it.
