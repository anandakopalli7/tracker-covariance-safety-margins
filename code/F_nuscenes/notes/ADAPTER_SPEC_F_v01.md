# Package F (nuScenes, route F-B): adapter specification, v01

Written 19 Nov 2026 by session F (Claude Opus 5.5). It states in words what `code\f03_adapter_v01.py` and `code\f05_arrays_v01.py` do, so that a second program can be written from this text and the raw data alone (A10 §10.1(b): "F's adapter is checked by a second program on 20 design-split decisions: truth clearance of the selected row within 1e-6 m").

Every rule here was fixed on the design split (the 700 nuScenes train scenes), before any val scene was read. Lock 2 records this file's SHA-256.

## 1. Data
- **nuScenes v1.0-trainval metadata** in `revision_v13\data\nuscenes\v1.0-trainval\` (`scene, sample, sample_data, ego_pose, sample_annotation, instance, category, calibrated_sensor, sensor, log`).
- **Splits:** the devkit's `nuscenes/utils/splits.py` lists `train` (700 scenes, the design split) and `val` (150, held out).
- **Detections:** CenterPoint results in nuScenes submission format, `Downloads\nusc_results_flip\nusc_results_flip\infos_{train,val}_10sweeps_withvelo_filter_True.json`.
- **Times:** seconds from the scene's first keyframe, `(timestamp_us − t0_us) × 1e-6`.
- **Frame:** the nuScenes global frame (x, y in metres; yaw counter-clockwise from +x).

## 2. Per scene
1. **Keyframes:** the scene's samples in `first_sample_token → next` order, with times `kf_t`.
2. **Sweeps:**
   - Every `sample_data` record whose calibrated sensor's channel is `LIDAR_TOP` and whose `sample_token` is one of the scene's samples, in timestamp order. Times are `sw_t`.
   - A sweep with `is_key_frame = true` is its sample's keyframe sweep.
   - Ego pose of a sweep: the `ego_pose` record of its `ego_pose_token`.
3. **Yaw of a quaternion (w, x, y, z):** `atan2(2(wz + xy), 1 − 2(y² + z²))`.
4. **Ego box:**
   - The nuScenes ego pose is the rear-axle midpoint (nuScenes paper, appendix A). The car is a Renault Zoe:
     - length L = 4.084 m and width W = 1.730 m;
     - wheelbase 2.588 m.
   - The box centre is `c = pose_xy + 1.294 · (cos ψ, sin ψ)`, with ψ the pose yaw. The 1.294 m offset is half the wheelbase, which assumes equal overhangs.
5. **Ego speed and acceleration at sweep i:**
   - **Travel:**
     - travel₀ = 0;
     - travel_{k+1} = travel_k + (c_{k+1} − c_k) · (cos h, sin h), with h = (ψ_k + ψ_{k+1})/2. Here ψ is unwrapped (`numpy.unwrap`) over the scene's sweeps.
   - **Fit:** a least-squares quadratic travel(t) = a + b·τ + q·τ² in τ = t − sw_t[i], over all sweeps with |t − sw_t[i]| ≤ 0.5 s (inclusive, tolerance 1e-9).
   - **Result:** v_raw = b and a_raw = 2q.
6. **Desired speed of the scene:** `clip(max_i v_raw[i], 1, 20)` m/s.
7. **Route:** the ego's logged path.
   - **Vertices:** start with c₀ (tangent ψ₀). Then, in sweep order, add c_i (tangent ψ_i, unwrapped) when both hold:
     - its distance from the last kept vertex is ≥ 0.25 m;
     - (c_i − last kept) · (cos ψ_i, sin ψ_i) > 0.
   - **Extensions:** prepend `first − 400·u(first tangent)` and append `last + 400·u(last tangent)`, each with the neighbouring vertex's tangent.
   - **Segments** join consecutive points. The cumulative arc length at the points is S.
8. **Projection of a world point q onto the route:**
   - **Segment:** the segment whose closest point to q is nearest; ties go to the lower segment index. On segment i, with clamped parameter τ ∈ [0, 1] and closest point p:
     - s = S_i + τ·len_i;
     - l = u_i × (q − p), the 2-D cross product with u_i the segment's unit direction (positive to the left);
     - θ = T_i + τ·(T_{i+1} − T_i), with T the point tangents.
   - The first program searches the segments touching the 24 route points nearest to q, plus both extension segments. On a sample it was checked to equal the search over all segments.
9. **Planner frame of a decision:**
   - **Origin:** s_e, l_e, θ_e = projection of the ego centre at the decision sweep.
   - **Points:** a world point maps to (x, y) = (s − s_e, l), using that point's own projection.
   - **Vectors and headings:** a world vector v at a point with tangent θ maps to R(−θ)·v; a world heading h maps to h − θ.
   - **Track covariance:** the planner library's `consumer.covariance4(P9, θ)` (rows and columns 0, 1, 6, 7 of the 9 × 9 matrix, both 2 × 2 blocks rotated by −θ).

## 3. Truth
- **Truth classes:** annotations whose category maps to one of the seven tracking classes, using the devkit's detection-name mapping:
  - car: vehicle.car;
  - truck: vehicle.truck;
  - bus: vehicle.bus.bendy and vehicle.bus.rigid;
  - trailer: vehicle.trailer;
  - motorcycle: vehicle.motorcycle;
  - bicycle: vehicle.bicycle;
  - pedestrian: human.pedestrian.adult, child, construction_worker and police_officer.
  - Every other category is ignored.
- **Instance at keyframe k:** centre (translation x, y), yaw, half length = size[1]/2 and half width = size[0]/2. The nuScenes size order is (w, l, h).
- **Instance at time t:** let k be the last keyframe with kf_t[k] ≤ t.
  - If t equals kf_t[k] within 1e-9 and the instance is annotated at k, use that annotation.
  - Otherwise the instance needs an annotation at k whose `next` annotation lies at keyframe k + 1. Its centre is then linear in time between the two annotations, and its yaw is y_k + w·wrap(y_{k+1} − y_k) with w = (t − kf_t[k])/(kf_t[k+1] − kf_t[k]).
  - Otherwise it has no truth at t. Times after the last keyframe have none.
- **Truth actors of a decision at time `now`:** the instances with truth at `now`.
  - **Window:** their truth at `now + 0.05 j` for j = 0..60, stopped at the first j without truth (NaN from there on).
  - **Size:** half length and half width from the annotation at the keyframe bracketing `now`.

## 4. Decisions
1. **Decision sweeps:** for every keyframe k ≥ 8 (the tracker has then had nine updates, as at the CARLA study's first assessment decision), the keyframe sweep and every second sweep after it, up to and excluding the next keyframe's sweep. That gives decisions at about 0, 0.1, …, 0.4 s after the keyframe, at 10 Hz as in CARLA. The last keyframe gives only itself.
2. **Built decisions:** only when −0.1 ≤ v_raw ≤ 20. Then v0 = max(0, v_raw), a0 = a_raw, and `now` is the sweep time.
3. **Evaluated:** a decision is evaluated (3 s) when now + 3 ≤ kf_t[last] + 1e-9, and evaluated2 (2 s) when now + 2 ≤ kf_t[last] + 1e-9.
4. **Rows:** `finite_primitive.build_library(v0, a0, desired, [], L, W, now, consumer.Diagnostics())`.
   - It returns the planner's 17 rows in cost order. With no actors the order is the same as with actors.
   - Row r's positions are s_r[j] (j = 0..60, 0.05 s apart) and its mean speed is vbar_r = s_r[60]/3.
   - The fallback row idx55 is the one with targets (−5, −5).
   - The ego box of row r at frame j has centre (s_r[j], 0), heading 0, length L and width W.

## 5. Clearance (the quantity of the second-program check)
- **Row clearance:** for row r, the minimum over truth actors a and frames j = 0..60 with truth of the distance between the ego box of row r at frame j and a's box at frame j. Both boxes are in the planner frame: a's centre (x, y) from its world centre's own projection, and its heading = its world yaw − θ at that projection.
- **Box distance:** 0 when the rectangles overlap or touch. Otherwise the minimum vertex-to-edge distance in either direction (`olcore_v01.poly_dist`, with corners from `rect_corners`).
- **Other cases:**
  - +∞ when no actor has truth in the window;
  - NaN when the decision is not evaluated;
  - frames 0..40 for the 2 s horizon.

## 6. Sources (the first program; the second-program check covers §§1–5)
- **Actors:** the tracker's output at the keyframe bracketing `now`.
  - **State:** state_time = the keyframe time. Position and velocity are mapped to the planner frame as in §2.9.
  - **Box:** length = size[1] and width = size[0].
  - **Process noise:** sigma_acc = 1.5 for pedestrian and bicycle, else 1.
  - **Covariance:** P = covariance4(P9, θ).
- **Constraints:** those of `consumer.constraints_for_trajectory`, rebuilt vectorised. An identity sample checks them against the library: critical scales within relative 1e-12, d within 1e-9 m.
- **N, F0, E, TG** as in the module text of f03:
  - **N** uses the track's own P.
  - **F0** uses the class-average P̄ of the tracker on the train scenes:
    - every truth actor present at `now` is matched one-to-one to the tracker's actors (global greedy by centre distance, gate 4 m; actor positions advanced to `now`);
    - matched P are averaged by class (pedestrian / vehicle).
  - **E** uses the squared true error along the constraint normal for actors matched many-to-one (nearest truth within 4 m at `now`), and 0 otherwise.
  - **TG** uses (2 + v_e)².
- **Critical scale:** the largest g with g·s ≤ d² and d ≥ 0 on every constraint. All constraints for 3 s; for 2 s, those at plan times ≤ 2 s (offset-0 columns 0..40, offset-1 columns 0..39).
- **Selection at scale g:** the first row (cost order) whose critical scale is ≥ g; idx55 if none.

## 7. Scored populations
- **All evaluated decisions:** the primary population.
- **"In-path lead" decisions:** a truth vehicle (car, truck, bus, trailer, motorcycle, bicycle) at `now` with 0 < x ≤ 60 m and |y| ≤ 1.75 m. This is the secondary population.
- **Run unit for the bootstrap:** the scene.
