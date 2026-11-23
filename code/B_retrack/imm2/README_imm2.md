# imm2_v01.py: independent second implementation of B1 (IMM, CV/CA)

Written from `IMM_AND_VARIANTS_SPEC_v01.md` (sections 1, 2, 4, 5, 7) and the A10 text (rows B1, B3, B4), plus CANMOT / Codex's
`OnlineTracker` / `tracker_config.json`. The first implementation was not read.

## What is implemented
- `derive_matrices(cfg, consts)`: R_B3, Q_B3, Q_CA, P0_CA exactly as spec section 1.
- `IMM2Filter(KalmanFilter)`: the IMM track filter. Mode filters are written here (own Kalman equations); CANMOT's `CV` / `CA`
  model classes only supply F, H, rotation matrices, state transition, output format and yaw warping, so the arithmetic of
  record is reused (including `axis_residual_from_wrapped`, `warp_to_pi`, and the exact-trig patch of `trk_env_v01.setup()`).
  The IMM logic (embedding, mixing, transition, log-likelihoods, mode probabilities, circular moment matching, combined output,
  R-bar for NIS bookkeeping) is own code.
- Integration: `canmot.tracking.nusc_trajectory` builds a track filter with `globals()[cfg filter name]`. The config of record
  names `ExtendedKalmanFilterRotate` for every class, so the module-global of that name is replaced by a dispatcher: label 2
  gives `IMM2Filter`, every other label gives CANMOT's original class with the unchanged config. (Config filter names are not
  edited, so CANMOT's assertion and the config of record stay as they are.) `build_tracker(constants, diag, mu0, imm=True)`
  deep-copies the config of record, sets `matrix_q[2]` = Q_B3 and `matrix_r[2]` = R_B3, and returns `OnlineTracker(cfg)`.
  `imm=False` gives the pure B3 tracker (CANMOT's own EKF with the B3 config), used for the check below.
- `retrack(cap_dir, constants_path, diag=0.95, mu0=(0.9, 0.1), imm=True)` -> list (one entry per line of `detections.jsonl`) of
  lists of `{id, name, P9, center, velocity, yaw}` (deep copies).
- Combined output: `self.state` (13, CANMOT CA output format), `self.P` (13x13), `get_covariance_meas()` = H_CA P H_CA^T;
  `get_measurement_noise_covariance()` = R-bar = c1 R_CV,rotated + c2 R_B3; `self.mu`, `self.log_lik` for diagnostics.

CLI: `python -I -B -X utf8 imm2_v01.py <cap_dir> <constants_json> <diag> <out_json>` (set `OPENBLAS_CORETYPE=Haswell`;
about 45 s per 69-frame capture on this laptop because of the exact-trig patch). Library use: `imm2_v01.CREATED` holds the
IMM filters of the last run.

## Ambiguities and how I resolved them
1. *Zero mixing weight when d = 1* (spec section 5, "c_j = Sum_i Pi_ij mu_i; mu_{i|j} = Pi_ij mu_i / c_j"): with
   Pi = identity and mu = (1, 0), c_2 = 0 and mu_{i|2} is 0/0. Resolved: if c_j = 0, mu_{i|j} = mu_i. The mode probability
   then stays exactly (1, 0) because log c_2 = -inf. Only matters for the diag = 1.0 check.
2. *Likelihood S and R rotation* ("S_j = H_j P_j- H_j^T + R_j (CV: R_B3 rotated by the predicted yaw ...)"): S_j and its inverse
   come from the predict step (CV: R rotated by the post-transition yaw before the yaw is wrapped, as CANMOT does).
   For the CV Joseph update, R is rotated by the predicted yaw after wrapping (again as CANMOT's `update`). The two
   differ only at rounding level.
3. *Update form*: CV mode uses the Joseph form (section 0 / section 2); CA mode uses P = (I - KH)P (section 4), K = P H^T S^-1 with
   S^-1 from the predict.
4. *Circular-yaw reference in the mixing step*: section 5 states the ref rule for "the mixture"; I apply the same rule (ref = yaw of the
   component with the largest weight, first on ties) in the two mixing mixtures (weights mu_{.|j}), the combined prediction
   (weights c) and the combined posterior (weights mu), and at birth (weights mu0).
5. *Birth*: CV mode P = H^T U R U^T H (U rotation by the detection yaw), P[8,8] = 10; CA mode P0_CA (unrotated R_B3);
   mu = mu0 = (0.9, 0.1); combined = mixture with weights mu0. Both mode states are the same detection state, so the
   mixture mean equals it.
6. *Frame interval*: Pi(dt) = (1 + (2d-1)^(dt/0.5))/2 diagonal, dt from `config['basic']['LiDAR_interval']`. The Q scaling of
   section 6 is not applied inside this module (Q_CA is built from the constants unscaled); a caller with dt != 0.5 must scale the
   config and constants itself. Not needed for the 0.5 s runs.
7. *Miss*: modes are not updated, mu stays c, state/P stay the combined prediction. In the next frame the mixing uses the
   mode predictions as the mode "posteriors" (natural reading; spec says only "modes are not updated").
8. *No probability floor*: mu is the plain normalised c_j Lambda_j (in logs). It could underflow to 0 in extreme cases; none
   seen.
9. The `assert q.radians == det_box.yaw` debug check of CANMOT's filters (on the detection quaternion) is not repeated in
   the IMM filter; `getMeasureInfo` of the base class (which has its own assertion) is used.

No contradiction in the spec was found that prevents implementation as written.

## Checks run (placeholder constants; `check_imm2.py`, `misstest` inline)
Captures `fit_finite_0012` and `c1109_tune_0000` (69 frames each, one car track in each):
- Tracker runs without error on both (IMM diag 0.95, mu0 (0.9, 0.1)).
- mode probabilities: range [3.7e-2, 0.9626] and [2.8e-2, 0.9717] (inside (0,1)); max |sum(mu) - 1| = 2.2e-16.
- P (13x13 combined): max relative asymmetry 1.7e-16, min eigenvalue >= 0 (no negative eigenvalue; the script's running minimum
  starts at 0, so the exact smallest value is not shown). Exported P9 of all tracks: min eigenvalue 4.6e-3, relative asymmetry <= 3.3e-16.
- diag = 1.0, mu0 = (1, 0): IMM output (P9, centre, velocity, yaw of every track-frame) vs a pure B3 run (CANMOT
  `ExtendedKalmanFilterRotate` with the B3 config): worst relative difference 0.0 (bit-identical) on both captures.
- Same test with detections removed at frames 20-22 and 40-41 (miss path): 66 non-empty frames, worst relative difference 0.0.
- IMM(0.95, (0.9, 0.1)) differs from B3 (worst relative difference 5.95e-2 and 1.17e-2), so the IMM is not a no-op.

## 19 Nov 2026 (spec change D-B4-3)
CA-mode update now symmetrises after `P = (I - K H) P`: `self.Pa = (self.Pa + self.Pa.T) / 2.0` (one line added in `IMM2Filter.update`).
Re-run with `trk_constants_v01.json`, diag 0.95, on `fit_finite_0012` and `c1109_tune_0000`: runs without error; mu in [3.4e-2, 0.9659] and
[2.2e-2, 0.9780], sum(mu)-1 <= 1.1e-16; combined P13 and P9 relative asymmetry <= 7.8e-17; P9 min eigenvalue 3.3e-3; diag 1.0 / mu0 (1,0)
vs pure B3 (B3 built from the same constants): worst relative difference 0.0 on both.
