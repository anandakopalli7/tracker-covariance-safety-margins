# Tracker variants B1–B4 of AMENDMENT 10 (v13): specification

Written 19 Nov 2026 by the package-B session (Claude Opus 5.5). It turns A10 §3 (B1–B4) into exact arithmetic. Where A10 leaves a
detail open, the choice is fixed here, **before any value of the variants was computed**, and listed in §7. Both IMM
implementations (the library's `trk_filters_v01.IMMFilter` and the independent second one) follow this text.

## 0. Base: the online tracker of record

- CANMOT (vendored in `<earlier-phase folder 2>\149_supported_sensor_preparation_20261101\vendor\CANMOT\src`), driven by
  Codex's `code\online_tracker.py` `OnlineTracker(cfg).step(detections, state_time)`, configuration
  `contracts\tracker_config.json` (class keys as int). Seven classes; car = label 2. Frame interval `dt` = 0.5 s
  (`cfg['basic']['LiDAR_interval']`).
- Filter of record for every class: `canmot.motion_module.kalman_filter.ExtendedKalmanFilterRotate` with the CV model
  (state x = [x, y, z, w, l, h, vx, vy, vz, yaw], 10; measurement z = [x, y, z, w, l, h, vx, vy, yaw], 9;
  H = rows 0–7 and 9 of I₁₀). Q (10×10, `model_cfg.matrix_q[c]`) and R (9×9, `model_cfg.matrix_r[c]`) are object-frame and are
  rotated by the yaw (rotation of the (x, y) and (vx, vy) pairs). Birth: x from the detection (vz = 0), P = Hᵀ U R Uᵀ H with
  P[8,8] = 10. The yaw innovation is wrapped to [−π, π) and then to the axial range [−π/2, π/2)
  (`axis_residual_from_wrapped`). Update in Joseph form.
- CANMOT builds a track's filter in `canmot.tracking.nusc_trajectory.Trajectory.__init__` through
  `globals()[cfg['motion_model']['filter'][label]](timestamp, config, track_id, det_infos)`. Association (GIoU, two stages,
  Hungarian), life cycle (min_hit 1, max_age), score management and output are CANMOT's and are **not changed** by any variant.
- The planner receives, per track, `covariance4(P9, route_yaw)`: rows/columns [x, y, vx, vy] (indices 0, 1, 6, 7) of the
  9×9 measurement-space covariance P9 = H P Hᵀ that the filter exports (`get_covariance_meas`), rotated into the route frame.

**Scope of every variant: the car class (label 2) only.** Tracks of every other class keep the filter of record with the
configuration of record (A10 B3 and B4 name the car class; B1 and B2 are built on them).

## 1. Constants (tuned on tuning runs only; file `trk_constants_v01.json`)

- `R_car_diag`: R_x, R_y, R_vx, R_vy (B3 step 1).
- `kappa` (B3 step 2); `sigma_a2` (B4); `ca_acc_init_var` = 10 (CANMOT's CA initial variance for accelerations).

Derived matrices (car class):
- **R_B3** (9×9) = R of record for the car, with the diagonal entries (0,0), (1,1), (6,6), (7,7) replaced by R_x, R_y,
  R_vx, R_vy. All other entries unchanged.
- **Q_B3** (10×10) = kappa × Q of record for the car (every entry).
- **Q_CA** (13×13, diagonal): CA state order [x, y, z, w, l, h, vx, vy, vz, ax, ay, az, yaw]. Entries at CA indices
  [0..8, 12] = the diagonal of Q_B3 at CV indices [0..9] (in order); entries at 9, 10, 11 = sigma_a2.
- **P0_CA** (13×13) = H_CAᵀ R_B3 H_CA (H_CA = rows 0–7 and 12 of I₁₃), then P0_CA[8,8] = 10 and
  P0_CA[9,9] = P0_CA[10,10] = P0_CA[11,11] = ca_acc_init_var.

## 2. B3: CV re-tuned

The filter of record with R_B3 and Q_B3 for the car class (i.e. `model_cfg.matrix_r[2]` = R_B3, `model_cfg.matrix_q[2]` = Q_B3).
Nothing else changes. Tuning (A10 B3):
1. R terms = mean squared detection errors in the object frame (along / across the true heading) of car-label boxes that enter
   the tracker (after CANMOT's score threshold and NMS), matched to the nearest true vehicle within 5 m (2-D centre) on the same
   tick, clear view (2-D visibility ≥ 0.99, the M4 measure), range ≤ 54 m from the sensor, on the 120 tuning runs only.
   Velocity error = detected minus true velocity, rotated into the true heading frame.
2. kappa: on the 20 lead-braking tuning runs, re-track with B3(kappa); for each run, the lead track's mean position NIS
   (NIS = νᵀ S⁻¹ ν, ν = z[0:2] − x_prior[0:2], S = P_prior[0:2,0:2] + R_rotated[0:2,0:2], over the updates of the track
   matched to the true lead at the decisions of record) ; statistic = median over runs. Search kappa = 10^(−3 + 0.05 j),
   j = 0..120, for the first sign change of (statistic − 2); then bisection on log kappa until |statistic − 2| ≤ 0.01.
   If no sign change, the j with the statistic nearest 2.
   *Lead track of a run*: at every decision of record, the planner actor matched to the true lead (the matching of record,
   `gc.match_many`, nearest within 4 m; several → nearest); its track id. Its updates are those with frame index ≤ the frame of
   the actor's state time. Per run: mean over the distinct (track, update) pairs so reached.

## 3. B2: innovation-adaptive Q

B3 for the car class, except that before each predict the velocity block of the (object-frame) process noise, Q_B3 entries at
CV indices 6, 7, 8 (rows and columns), is multiplied by f = clip(m, 0.25, 10), where m = (mean of the position NIS of the
track's last at most 3 updates) / 2; m = 1 (f = 1) before the first update. Index 8 (vz) does not reach any exported quantity.

## 4. B4: CA

Code check (A10 B4 rule): `ExtendedKalmanFilterRotate` cannot take CANMOT's CA model unchanged (the CA model has no
`get_rotation_matrix_for_measurement`, and its `get_rotation_matrix_for_state` rotates only x, y, z). So B4 uses CANMOT's
`LinearKalmanFilter` arithmetic with world-frame noise:
- model CANMOT `CA` (13 states, F with dt and dt²/2; az, vz reset to 0 by F); H_CA as above;
- birth: x = detection (accelerations 0, vz 0), P = P0_CA; Q = Q_CA; R = R_B3 (used as world-frame, unrotated);
- predict: x = F x; P = F P Fᵀ + Q_CA; S = H P Hᵀ + R_B3;
- update: ν = z − H x with the yaw component wrapped to [−π, π) and then to [−π/2, π/2) (the online filter's axial rule; §7
  D-B4-1); K = P Hᵀ S⁻¹; x += K ν; P = (I − K H) P, then **P = (P + Pᵀ)/2** (D-B4-3); yaw of x wrapped to [−π, π).
Route yaw is 0 in all 155 stored runs, so world-frame noise equals route-frame noise there.

## 5. B1: IMM (CV/CA)

Modes j = 1 (CV: the B3 filter of §2, a rotated EKF in 10 states) and j = 2 (CA: the B4 filter of §4, 13 states).
Common space: the CA state (13). **Embedding** of a CV state and covariance: CA indices [0..8, 12] ← CV indices [0..9];
accelerations 0 with zero variance and zero covariances. **Projection** of a CA state to CV: indices [0..8, 12].

- **Transition** per 0.5 s step: Π = [[d, 1−d], [1−d, d]], d = 0.95 (sensitivities 0.90, 0.98). For a frame interval dt ≠ 0.5:
  Π(dt) = Π^(dt/0.5), i.e. diagonal (1 + (2d − 1)^(dt/0.5)) / 2.
- **Birth** (a new track from a detection): each mode filter is born by its own rule (§2, §4); μ = (0.9, 0.1). The track's
  combined state and covariance are the moment-matched mixture (below) with weights μ.
- **Each frame**, for a track that exists (CANMOT calls predict, then update with a detection or with none):
  1. *Mixing.* c_j = Σᵢ Π_ij μᵢ; μ_{i|j} = Π_ij μᵢ / c_j. For each j, the mixed initial condition is the mixture of the two
     embedded mode posteriors with weights μ_{·|j}.
  2. *Mode prediction.* CV: its state and covariance are set to the projection of mixed initial condition 1, then the rotated-EKF
     predict of record (Q_B3 rotated by the yaw of that mixed state, F with dt). CA: set to mixed initial condition 2, then the
     linear predict of §4.
  3. *Combined prediction* = mixture of the two embedded predictions with weights c. It is what association uses (the predicted
     box) and what is output if the track is not updated. Mode probabilities become μ = c.
  4. *Update with a detection.* Each mode computes its innovation ν_j (its own residual rule, 9 components) and
     S_j = H_j P_j⁻ H_jᵀ + R_j (CV: R_B3 rotated by the predicted yaw; CA: R_B3 unrotated), then its own update.
     Likelihood Λ_j = N(ν_j; 0, S_j) (9-dimensional Gaussian density, evaluated in logs). μ_j ∝ c_j Λ_j (normalised).
     Combined posterior = mixture of the embedded mode posteriors with weights μ.
  5. *No detection (miss).* Modes are not updated; μ stays c; the combined state is the combined prediction.
- **Mixture (moment match)** of embedded (x_i, P_i) with weights w: m = Σ wᵢ xᵢ; P = Σ wᵢ [Pᵢ + (xᵢ − m)(xᵢ − m)ᵀ] (the
  spread-of-means term). The yaw component (CA index 12) is averaged on the circle: before the sums, each xᵢ's yaw is replaced
  by ref + wrap(yawᵢ − ref), wrap to [−π, π), ref = the yaw of the component with the largest weight (the first on a tie);
  afterwards the mean yaw is wrapped to [−π, π).
- **Output** to CANMOT and the planner: the combined state (13; CANMOT's CA output format) and P9 = H_CA P H_CAᵀ of the combined
  covariance. The planner's 4×4 block is covariance4(P9).
- NIS bookkeeping of the IMM (for NA_IMM and diagnostics): prior = combined prediction; R̄ = c₁ R_CV,rotated + c₂ R_B3.

## 6. Rates and latency (B7, used by session CD)

dt = 0.2 or 0.1 s: every Q entry of every class (and Q_CA, including sigma_a2) × dt/0.5, unless the unscaled sensitivity is
asked; R unchanged; max_age in frames = round(max_age_of_record × 0.5 / dt) (car: 15 → 7.5 s); the IMM transition as in §5.
Latency is applied by the caller (the state from the sweep at t reaches the planner at t + L).

## 7. Choices fixed here (not in A10), recorded before any value

| Id | Choice | Reason |
|---|---|---|
| D-V-1 | Variants change the car class only | A10 B3/B4 name the car class; B1/B2 are built on them |
| D-B3-1 | R_B3 replaces only the four named diagonal terms; off-diagonals of record kept | "position and velocity terms … set to the mean squared errors" names diagonal quantities |
| D-B3-2 | κ search range j = 0..120 (10⁻³ … 10³); lead track and NIS as in §2 | A10 gives the grid start and step, not the end |
| D-B2-1 | m = 1 before the first update; velocity block = CV indices 6, 7, 8 | A10 silent; vz has no effect on any output |
| D-B4-1 | Linear KF uses the online filter's axial yaw residual | Without it, the detector's reversed-yaw boxes (3.1% of vehicle boxes, 28% beyond 40 m; M4 report) turn the CA box by up to π/2 per update, an artefact of the yaw wrap, not of the motion model under test |
| D-B4-2 | Birth covariance P0_CA = Hᵀ R_B3 H with vz 10 and accelerations 10 | CANMOT's CA defaults (P 10 everywhere, Q 100, R 0.001) are nuScenes placeholders; the online CV's birth rule is kept, with CANMOT's CA value for the unobserved accelerations |
| D-B4-3 | **Bug fix (19 Nov 2026, 15:45 EST, before Lock 2):** after each linear-KF update the CA covariance is symmetrised, P = (P + Pᵀ)/2 | Found by the planner's own covariance check (Codex `consumer.check_psd`, tolerance 64 eps): with CANMOT's (I − KH)P form the rounding asymmetry accumulates, and re-tracking stopped with "Asymmetric covariance" in tuning run p2_c1109_tune_0050 (B4) and p2_c1109_tune_0098 (B1). Before: those runs fail; after: they complete. Values elsewhere change at the rounding level. Table S4 entry |
| D-B1-1 | IMM likelihood on each mode's full 9-component innovation; circular yaw averaging in mixtures | Standard IMM; yaw is an angle |
| D-B1-2 | Rate change: Π^(dt/0.5) | A10 gives Π per 0.5 s |

## 8. Scoring add-ons (`trk_score_v01.py`): choices fixed before any value (19 Nov 2026, ~15:15 EST)

| Id | Choice | Reason |
|---|---|---|
| D-E5-1 | u_i ranks only the decisions that have rows with finite positive g*_F0 and g*_E; n = their number; the others get 0.5 | Makes u uniform on (0, 1) among ranked decisions; A10 gives 0.5 to the others |
| D-E5-2 | On tracker x's room, every oracle (E5, E5p at the record amplitude m = 1.1029, A = 0.05; E5_x, E5p_x at x's own m_x, A_x) scales F0_x and ranks r_i from x's own F0_x and E_x (for the online tracker these are the record's F0 and E). Each permuted oracle uses a fresh `default_rng(20261915)`, runs in name order, one permutation per run over its evaluated decisions in k order | A10 §2.2 defines E5_x on x's own room |
| D-E5-3 | m_x, A_x from the margin ratio sqrt(c_F0x / c_Nx) (= sqrt(s_Nx / s_F0x)) at every evaluated decision and row with finite positive scales of both ("binding rows" of record, `rev_c_ratio_tracks_v01` R20) | Same rows as the ratio of record 1.1029 |
| D-B6-1 | Delayed stop: τ_i not on the 0.05 s grid is handled exactly under the row generator's piecewise-constant acceleration; δ_i drawn by one `default_rng(20261916)`, runs in name order, evaluated decisions in k order | The stop of record needs τ on the grid; A10 draws a continuous δ |
| D-B9-1 | Cut-in lane centre = the ego's median lateral route coordinate over the run (it varies 0.33–0.36 m within a run); "ahead" = along-route centre distance > 0 | A10 §2.5 does not define the lane centre numerically. Event ticks are identical with the instantaneous ego coordinate (20/20) |
| D-B9-2 | Track age = decision time − birth time (first detector frame whose output holds the id) of the youngest track matched to the cutting vehicle (rule of record of `prim_age`) | A10 §2.5 |
