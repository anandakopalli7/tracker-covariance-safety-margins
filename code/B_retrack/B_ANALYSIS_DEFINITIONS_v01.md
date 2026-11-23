# Package B analyses on the stored runs: definitions fixed before any variant score was computed

Written 19 Nov 2026, ~15:20 EST, by the package-B session (Claude Opus 5.5). Turns A10 §3 rows B1–B6, B8 into computations on the
35 old evaluation lead-braking runs (exploratory), plus the 20 cut-in tuning runs (descriptive). Library definitions:
`..\shared\trackers\IMM_AND_VARIANTS_SPEC_v01.md` §7–8. Nothing below was chosen after seeing a value of a variant.

## Inputs
- Per tracker x ∈ {CV0 (online, "N"), B3, B2, B4, B1, B1_d090, B1_d098}: the 35 runs' arrays re-built from x's tracks with P̄_x
  (`out\retrack\<x>\<run>_arrays.npz`; P̄_x = `out\pbar\PBAR_<x>_v01.json`, the rule of record on x's tracks of the 120 tuning runs).
  CV0's arrays equal the stored ones (B0(b)).
- Tracker-independent arrays (rows depend only on the logged ego state; truth): clear, vbar, idx55, evaluated, and the
  reaction-and-stop clearances of record (`11_ojits\review\optionA_recount_v01\cache`, via `rev_common_v01.load_runs`).
- Bootstrap: run resamples, the draw of record `default_rng(20261113).integers(0, 35, (20000, 35))`; for gridless quantities its first
  2,000 rows (the A9-1(c) practice of v12). Percentile 95% intervals.

## Quantities (each on x's own room: F0 := F0_x, E := E_x)
- **Room** R_gl,x = D_gl(E_x, F0_x) (gridless step frontier, 201 levels); grid R beside. Decision-equivalents as of record.
- **Shares** RR_gl(A_x) for A ∈ {N, NA, AM, CK3, Q} (x's tracks); grid RR beside.
- **Margin ratio** at binding rows: sqrt(c_F0x / c_Nx); median m_x, q05, q95, A_x, share within 5% of the median, "barely varies".
- **E5 family** (B5): E5 and E5p (m = 1.1029, A = 0.05, ranks from the record's F0 / E) and E5_x, E5p_x (m_x, A_x; ranks from F0_x / E_x);
  ceiling c_x = RR_gl(E5_x). For N (CV0) the "x" is the online tracker itself.
- **H3-style classification (exploratory print only)** of r = RR_gl(N_x) against c_x with δ = 0.05: recovers / uninformative
  variation / amplitude-limited / inconclusive, flag "barely varies" (A10 H3 wording).
- **Phase.** Primary: x's own estimate (A10 §2.4; thresholds −1.0, sensitivities −0.5 / −2.0, from x's lead track `vhat`, `ahat_long`).
  The truth phase of record beside. **After-stop** (the v12 term, used by the B3/B4 rule): truth phase 2 (lead stopped); by the
  estimate beside.
- **Room by phase**: R_gl in each phase population (estimate primary, truth beside), decision-equivalents.
- **After-stop room**: R_gl in the truth-phase-2 population, decision-equivalents.
- **Lag** (B3/B4): median over evaluated decisions in the first second after the stop (truth phase 2, 0 ≤ t − t_stop < 1 s, t_stop =
  the run's first truth-phase-2 decision) of x's lead track's predicted minus true longitudinal position at 3 s (`dx_pred3`).
- **RR(CK3) pooled**: RR_gl(CK3_x), all evaluated decisions.
- **B3/B4 consequence rule** (A10, point values): "depends on filter tuning" if, under B3 or B4, the after-stop room < ½ × CV0's, or
  |RR_gl(CK3_x) − RR_gl(CK3_CV0)| > 0.10; else "persists with NIS near 2 and with a CA filter". (B4's NIS window was not reachable:
  reported with the rule's outcome.)
- **NIS and NEES by phase** (B1, B8(b)): one value per distinct update of the lead track (run, track id, state time) at evaluated
  decisions: NIS = the update's position NIS (`nis_last`); velocity NEES at the decision (`nees_v`, route frame, 2 dof). Means and
  medians by phase (estimate primary; truth beside); run-level intervals (resample runs, the draw of record's first 2,000 rows).
- **Realised lead deceleration** (rule of record, rev_h_run_facts_v01, Table S28): per run, the true lead (evaluation_truth `target`)
  speed v(k) = |velocity_lh| at ticks k with time t = 0.05 k; v_pre = median of v over 3 < t < 5 + brake_start_s − 0.2 (else the max of
  the first 20 samples); samples with 0.1 v_pre < v < 0.9 v_pre and t > 5 + brake_start_s − 0.5; if at least 4, take the contiguous
  index range from the first to the last such sample and the deceleration = minus the least-squares slope of v against t over it
  (numpy.polyfit degree 1); otherwise undefined (sorts last).
- **B6(a) terciles** (CV0 and the record's arrays): realised lead deceleration (rule above), ascending, ties by id,
  `array_split` into 3 (12/12/11). Per tercile on its own frontier: reaction-and-stop room at τ = 0.75 s, 6 m/s² (scoring W_R of
  record: cached clearance > 0) and its ratio to the tercile's 3 s room; den₀ (D(F0, O) under W_R, the perfect oracle) in
  decision-equivalents; "not evaluable" if den₀ < 10.
- **B6(b) delayed stop**: τ_i = 0.75 + δ_i, δ_i ~ U(0, 0.75) (spec D-B6-1), 6 m/s²; room, den₀ and shares under that scoring.
- **B8(a)** after-stop decisions with the tracker's lead speed > 0.5 m/s: counts per run and their contribution to the after-stop room
  (attribution of record, a9_4b), with intervals.
- **Intervals for the IMM transition sensitivities** (B1_d090, B1_d098; added 19 Nov 18:15 EST, before they were computed): the bootstrap
  covers the all-decisions population only (points for every population); compute-time limit.

## Amendment 1 (19 Nov 2026, 18:40 EST): NIS and NEES by phase — disagreement resolved (A10 §10.1(c))
The first comparison (out\compare\B_COMPARE_RECOUNT_v01.*) showed the two programs counting updates differently, because the bullet
above did not say how an update whose decisions fall in two phases is counted, and both used the decision-time velocity NEES although
A10 B8(b) says "NIS and NEES per phase at update time, truth at the state time". Fixed definition (replaces the bullet above; both programs
recompute it):
- Lead-track states at evaluated decisions with a lead track found; key = (run, track id, state time rounded to 1 ms). An **update** is a
  key whose state is a filter update (finite `nis_last`). Each distinct update is assigned to the phase of its **first evaluated decision**
  in k order (the rule of record of v12, a9_4b: `np.unique(key, return_index)`), truth phase and x's estimated phase (thr −1.0) separately.
- **NIS** = that update's position NIS (`nis_last`).
- **NEES_v** = e' Pvv⁻¹ e, e = v_trk − v_true(t_s): v_trk and Pvv the track's output velocity and velocity covariance at that update
  (the tracker record `trk_*` in `out\retrack\<x>\<run>_arrays.npz`: the entry with the same id and state time), rotated into the route
  frame (route yaw), v_true(t_s) the true lead velocity (evaluation_truth target, velocity_lh with y negated) at the truth tick whose
  `time` is nearest the state time.
- Per phase: n, mean, median; run-level 95% interval of the mean (ratio of run sums; first 2,000 resamples of the draw of record).
