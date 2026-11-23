# v13 shared tracker library (`work\shared\trackers\`) — API

Owner: session B (package B of revision v13, Claude Opus 5.5). **Other sessions import this library and never edit it.**
Status (19 Nov 2026, 20:45 EST): **FROZEN** (`work\locks\FREEZE_B.json`). Code unchanged since 15:44 EST (bug fix D-B4-3, spec §7).
**Tuned constants** (`trk_constants_v01.json`): car R diagonal
(x 0.0469, y 0.00592, vx 0.267, vy 0.0446), κ = 0.16788 (median lead NIS 1.994), σ_a² = 0.001 (B4's NIS window [1.8, 2.2] is not
reachable: median NIS 1.63 at the smallest grid value; nearest value taken, as A10's rule says). Cut-in threshold stays 1.75 m
(events in 20 of 20 cut-in tuning runs; B9).
Freeze manifest: `work\locks\FREEZE_B.json` (written 19 Nov 2026, ~20:50 EST). After the freeze nothing here changes; a fix would be a
recorded departure needing the coordinator's OK.
Definitions: `IMM_AND_VARIANTS_SPEC_v01.md` (this folder) — exact arithmetic of B1–B4 and every choice A10 left open (§7 there).

## Files
| File | What |
|---|---|
| `trk_env_v01.py` | Environment: paths to Codex/CANMOT, stand-ins for missing packages (`shims_v01\`), correctly rounded trig (Windows), BLAS pin |
| `trk_filters_v01.py` | Filter classes: `RecEKFRotate` (online CV of record + recording), `AdaptiveQEKF` (B2), `CALinearKF` (B4), `IMMFilter` (B1); CANMOT dispatch |
| `trk_tracker_v01.py` | **Step-wise tracker** `V13Tracker`, variant configurations, `planner_actors`, offline `retrack_capture` |
| `trk_arrays_v01.py` | **Decision arrays of record** rebuilt from a (re-tracked) capture: `overlay`, `extract`, `pbar_accumulate` |
| `trk_constants_v01.json` | Tuned constants (R terms, κ, σ_a²) — written by package B before the freeze |
| `trk_score_v01.py` | Scoring add-ons of A10 §2–3: margin ratio and E5 / E5p / E5_x (`margin_ratios`, `ratio_summary`, `e5_u`, `permute_u`, `add_oracle`), gridless estimand (`gridless`, `rr_gl`, `boot_gl`, `rr_summary`), estimated phase (`est_phase`), terciles (`realised_decel`, `terciles`), delayed stop (`draw_delays`, `delayed_stop_clearance`) |
| `IMM_AND_VARIANTS_SPEC_v01.md` | The specification both IMM implementations follow |

## 1. Set-up (every process)
```python
import sys; sys.path.insert(0, r'<...>\work\shared\trackers')
import trk_env_v01 as env          # import FIRST (before numpy) if bit-exact replay of logged pod output is wanted on Windows
env.setup(codex_root=None, exact_trig=None)
```
- `codex_root`: the tree that holds `code\`, `vendor\CANMOT\src`, `contracts\tracker_config.json` (Codex's 149 package). Default:
  env `V13_CODEX_ROOT`, else `<library folder>\149_supported_sensor_preparation_20261101`.
  **On a pod** set `V13_CODEX_ROOT` to the packet's copy of that tree.
- `exact_trig`: None → on for Windows (needed for bit-identity with the Linux pods), off elsewhere.
- Run Python as `python -I -B -X utf8`; on Windows with `OPENBLAS_CORETYPE=Haswell` in the environment.
- **One tracker library per process.** CANMOT builds filters through a module-global name; this library rebinds it (and
  re-asserts it on every `step`). Do not load other code that rebinds `canmot.tracking.nusc_trajectory.ExtendedKalmanFilterRotate`
  in the same process (the independent second IMM is run in its own process for this reason).

## 2. Online, step-wise tracker (sessions E and F)
```python
import trk_tracker_v01 as T
trk = T.V13Tracker(variant='B1', const=None, base_cfg=None, dt=0.5, q_scale=True, record=True)
tracks = trk.step(detections, state_time)     # ONE call per detector frame, in time order
actors = T.planner_actors(tracks, ego_world_rh, route_yaw)   # Codex's planner_actors, unchanged
```
- `detections`: the list CANMOT/Codex's `OnlineTracker.step` takes (nuScenes submission rows: `translation`, `size`, `velocity`,
  `rotation`, `detection_score`, `detection_name`), e.g. `detector_to_world(pred, reference_world_rh)` in CARLA, or a nuScenes
  CenterPoint result list on nuScenes.
- `tracks`: the `OnlineTracker` output format: dicts `id, name, center, size, yaw, velocity, P9 (9x9), state_time, score`. For B1 the
  P9 is the IMM's **combined** covariance (spread-of-means included); the planner's 4×4 block is `covariance4(P9, route_yaw)` inside
  `planner_actors`.
- `variant`: `CV0` (online tracker of record), `B3`, `B2`, `B4`, `B1`, `B1_d090`, `B1_d098` (definitions: spec). Variants change the
  **car class (label 2) only**; every other class runs the filter of record.
- `const`: tuned constants dict; default = `trk_constants_v01.json` (frozen). `base_cfg`: tracker configuration (default: the CARLA
  configuration of record). For nuScenes (F) pass CANMOT's released nuScenes configuration as `base_cfg` if F's plan says so; the
  car-class B3/B4 matrices are then built from `base_cfg`'s car R (diagonal replaced by the frozen R terms) and `kappa × base_cfg`'s car Q
  (spec §1). Say in F's text which base was used.
- Rates (B7): `dt=0.2` or `0.1`; Q of every class (and the CA Q) × dt/0.5 unless `q_scale=False`; R unchanged; deletion ages kept in
  seconds; IMM transition Π^(dt/0.5). Latency is the caller's (the state from time t is given to the planner at t + L).
- `trk.rec` (when `record=True`): `events` (birth / predict / update / miss / reset, the `filter_events.jsonl` format),
  `algebra` (update records: prior state, prior P, measurement, rotated R — the `filter_algebra.jsonl` fields used downstream),
  `modes` (B1: mode probabilities per track and frame).
- **F0_x** for E's IMM pair (F0_IMM): P̄_IMM from package B's output `work\B_retrack\out\pbar\PBAR_<variant>_v01.json`
  (`{'Pbar': {'vehicle': 4x4, 'pedestrian': 4x4}}`, the rule of record on the 120 tuning runs) — written before the freeze.

## 3. Offline re-tracking and decision arrays (session CD on fresh runs, package B on old runs)
```python
import trk_env_v01 as env; env.setup()
import trk_tracker_v01 as T, trk_arrays_v01 as A
ov, rec = T.retrack_capture(cap_dir, variant='B1')     # logged detections -> variant -> planner actors at every decision tick
with A.overlay(cap_dir, ov):                            # serves the re-tracked files to the extractors of record
    meta, arrs = A.extract(run_dir, cap_dir, PB, lead=True, a4=True)
```
- `run_dir`: the folder holding the run's `SUMMARY.json` (with `assessment_outcomes.base_frame`, `first_contact_frame`, `knobs`, `arm`).
  `cap_dir`: the capture folder with `detections.jsonl, frames.jsonl, evaluation_truth.jsonl, scenario_frames.jsonl, contract.json,
  filter_events.jsonl, filter_algebra.jsonl`. Old archives: `run_dir = archives\<run>`, `cap_dir = <run_dir>\x\<run>\capture\<case>`.
  Any run folder works (no fixed run list); the entry point takes the two paths.
- For `CV0` the overlay reproduces the logs (B0(b) identity); without `overlay` the logged files are used (= CV0).
- **B7 (CD):** `retrack_capture(cap_dir, variant, det_rows=rows, dt=0.2 or 0.1, q_scale=True, latency=L)` with `rows` = the re-detected
  frames of one rate in time order (dicts with `k`, `time`, `model`; e.g. the rows of `b7_detections_v13.jsonl` whose `rates_hz` holds
  the rate). A decision at tick k uses the last frame with `k_frame * 0.05 + L <= k * 0.05`; with the logged rows and L = 0 this is the
  paid chain exactly. The overlay's `detections.jsonl` then holds those rows, so track ages, a-hat and NIS follow the new rate.
- `PB`: `{'vehicle': 4x4, 'pedestrian': 4x4}` — the class average of the tracker variant (P̄ of record for CV0:
  `P\09_redesign\m2_decisions\openloop\pbar_tuning_v01.json` key `Pbar`; P̄_x: package B outputs, §2).
- `arrs` keys (one row per assessment decision; `(n_dec, 17)` for critical scales):
  - as `gateR_rt_v01` (`ol_gateR_rt_extract_v02.run_arms`): `k, evaluated, v0, des, clear, vbar, idx55, cF0, cN, cE, cl, clx, status,
    prim_idx, n_act, n_match, prim_track, prim_age, prim_miss, ego_speed, flag_task, flag_strict` (not rebuilt: `cF1, cF1x, cR2, cR3,
    delta, c2_rad`);
  - as the A4 extract (`oxsb_extract_v05.run_one`, `a4=True`): `cNA, cQ, cA1` (= AM), `cCK3, phase` (truth phase of record:
    0 before onset, 1 lead moving, 2 lead stopped, 3 unknown), `prebrake, lam_max`;
  - as the v12 lead-state extract (`a9_4a`, `lead=True`): `lead_found, track_id, vhat, vhat_x, ahat_long, ahat_mag, age, v_true,
    nis_last, nees_v, gap_true, now, dx_pred0..3`. The tracker-estimated phase (A10 §2.4) is: stopped if `vhat ≤ 0.5`; braking if
    `vhat > 0.5` and `ahat_long ≤ −1.0` (sensitivities −0.5, −2.0); otherwise (or `lead_found` false) before braking.
  - `meta`: family, desired, arm, knobs, n_dec, contact_k, kmax, check counters (as the extractors of record).
- The extractors of record are imported read-only from `P\09_redesign\m2_decisions\openloop\` (laptop path). `a4=True` works for any
  family (the CK3 shift and the truth phase use the run's own primary actor; `prebrake` needs `draw.brake_start_s`, absent → False).
- Cost: about 1 s (CV) to 3 s (IMM) per run to re-track, 20–60 s per run to extract (one core).
- `A.pbar_accumulate(cap_dir, acc, cnt)` applies the P̄ rule of record (`ol_pbar_v01`) to one run (inside an overlay for a variant).

## 4. Scoring add-ons (`trk_score_v01.py`)
See the module text; choices in the spec §8. Validated: the gridless RR(N), RR(CK3) and room on the 35 old runs equal v12's
A9-1(c) record exactly; the continuous-τ stop equals the cached reaction-and-stop clearances of record at τ = 0.75 and 1.0 s
within 5.7e-14. Runs are dicts (`make_run(arrs, masks, crit_map)` builds one from `extract` output). E5 on a tracker x's room:
`u, _ = e5_u(runs, 'F0', 'E'); add_oracle(runs, 'E5', 'F0', 1.1029, 0.05, u)`; ceiling: `rs = ratio_summary(margin_ratios(runs, 'N', 'F0'));
add_oracle(runs, 'E5x', 'F0', rs['median'], rs['A'], u)`; E5p: `permute_u(runs, u)` (seed 20261915).
Gridless shares: `G = gridless(runs, ['F0','E','N','E5x']); p = rr_gl(G, 'F0', 'E', ['N','E5x'], pop=0)`; resamples: `boot_gl(G, ..., CNT)`.

## 5. Verification done
- B0(a): the replay of record is exact in today's Python (55/55 lead-braking runs bit-identical; 151/155 runs bit-identical, 4 within
  8.9e-16): `work\B_retrack\out0\`.
- The library's CV0 replay (`retrack_capture`) reproduces the logged tracks, actors, filter events and update algebra exactly.
- B0(b): arrays rebuilt through `overlay` + `extract` reproduce the stored gateR_rt_v01, A4 and lead arrays within 1e-12 in 151 of 155 runs
  (all 55 lead-braking and 20 cut-in runs), grid selections identical in all 155; the 4 crossing tuning runs above 1e-12 absolute have
  relative differences ≤ 1.6e-13 (last-bit replay / arithmetic; `work\B_retrack\STATUS.md`).
- P̄ rule: CV0's re-tracked P̄ equals `pbar_tuning_v01.json` within 5.4e-15 (identical counts).
- Scoring add-ons: gridless RR and room equal v12's A9-1(c) record; continuous-τ stop equals the cached stop within 5.7e-14.
- Second IMM (independent, Claude Sonnet, from the spec only; `work\B_retrack\imm2\`): with the frozen constants and fix D-B4-3, combined
  covariances agree with `IMMFilter` within 9.0e-15 relative, identical ids, on 7 stored runs. The A10 §10.1(b) check on five fresh runs
  (default_rng(20261917)) runs after Lock 2 (`work\B_retrack\code\imm_compare_v01.py`).
- Package B's results on the stored runs agree with an independent second program on all 838 compared items
  (`work\B_retrack\out\compare\`).
