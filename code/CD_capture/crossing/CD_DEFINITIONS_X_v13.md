# Crossing sprint (A11): definitions of package CD's analysis

Written 21 Nov 2026, about 13:50 EST (Claude Opus 5.5, session CD), before amendment A11 and its lock, and before any fresh crossing run existed. This file and A11's text are the specification for both programs. The first program is `crossing\x_cross_v13.py`; the second, a recount, is written by another model from this file and A11 only. Where this file and A11 differ, A11 wins.

The definitions are those of package C's lead-braking analysis (`CD_DEFINITIONS_v13.md`; A10 §2, §5.3; `analysis\c_lead_v13.py`). §8 lists what does not carry over.

## 1. Cases and runs
- **Cases:** `crossing\CASES_X_v13.json` (SHA-256 `9e2c95f8c2ec7c6e5ac38de106505d2799b6a4f17dd48416dceea6b2b9a1d46b`), made by `make_cases_x_v13.py`.
  - Two families: `vehicle_crossing` and `pedestrian_crossing`, with 200 study cases and 10 reserves each.
  - The rule is in the file. These are the C1109 sampler's pre-drawn evaluation cases (role `eval`, consumer `finite`). Speeds are interleaved 5, 10, 15 by position, and α = β follows C's cycle.
- **Run set of a family:** the first n study cases (positions 0 … n−1; n is set by A11), with job ids `px13_<case>_native`, in ascending run id.
  - A failed capture is replaced only by A11's rule, using the family's reserves in order. Replacements are recorded in `crossing\REPLACEMENTS_X_v13.json` as `{"replacements": {case: reserve case}}`.
- **Capture:** packet_main_v03 unchanged (tar `6ae57b9f…`), native arm, C's settings, keep_raw false. Job lists come from `make_jobs_x_v13.py`.

## 2. Arrays (shared by both programs)
- Made by `crossing\x_extract_v13.py`: the online tracker of record (CV0, the logged files) with the P-bar of record (`P\09_redesign\m2_decisions\openloop\pbar_tuning_v01.json`).
- The call is package B's frozen `trk_arrays_v01.extract(run_dir, cap_dir, PB, lead=False, a4=False)`, the call B's b0b harness makes for crossing runs. It builds the arrays with the expressions of record (`ol_gateR_rt_extract_v02.run_arms`).
- Output: `arrays_x\CV0\<rid>.npz`. The keys used are `evaluated`, `clear`, `vbar`, `idx55`, `cF0`, `cN`, `cE`. The `meta` JSON carries `run_id`, `family` and `desired`.
- Old-run check: on old crossing tuning runs the arrays equal the stored arrays of record (`gateR_rt_v01`) bit for bit (`crossing\out\TESTOLD_X_EXTRACT_*.json`).
- Each run's `meta.family` must equal the family analysed.

## 3. Population, scoring, frontier
- **Population:** all evaluated decisions (`evaluated == 1`). There is no other population.
- **Scoring:** the 3 s commitment, the same rule as lead braking. A wrong go means the selected row's 3 s true clearance to any true actor is ≤ 0.
  - It is computed by `trk_score_v01.gridless` / `safe_w1` on `clear`, `vbar` and `idx55` (the library of record, `optA_lib_v02.clean_clear` and friends).
- **Frontier:** the gridless step frontier at 201 caution levels (A10 §2.3).
  - The levels are linspace(c0, min(max c_F0, max c_E), 201), where c0 is F0's first caution.
  - D_gl(A) = Σ over the levels of (F_F0 − F_A). The room is R_gl = D_gl(E) / 201 (pp) and RR_gl(A) = D_gl(A) / D_gl(E).
  - RR_gl is undefined when D_gl(E) ≤ 0.

## 4. Sources
- **F0, E, N:** the class-average P-bar of record, the true-state error and the tracker covariance of record (`cF0`, `cE`, `cN`).
- **E5 (record amplitude, as C's H1):**
  - u = `trk_score_v01.e5_u(runs, 'F0', 'E')`.
  - E5 = `add_oracle(runs, 'E5', 'F0', m = 1.1029, A = 0.05, u)`.
  - E5p = the same with u permuted within each run's evaluated decisions (`permute_u`, `default_rng(20261915)`, runs in run order).
- **E5_N (N's own amplitude, as C's H3 and K2, and B's step 0):**
  - From `ratio_summary(margin_ratios(runs, 'N', 'F0'))` on this family's run set: m = median and A = (q95 − q05) / (2·median).
  - E5_N = `add_oracle(runs, 'E5N', 'F0', m, A, u)`, with the same u as E5.
  - 'barely varies' holds when ≥ 95% of binding rows are within 5% of the median ratio.

## 5. Intervals
- **Resamples:** 20,000 run resamples, `optA_lib_v02.boot_counts(n_runs, 20000, 20261911)` (C's draw), with runs in ascending run id.
- **Statistics:** R_gl, RR_gl(E5), RR_gl(E5) − RR_gl(E5p), RR_gl(N) and RR_gl(E5_N). Each ratio is NaN in a resample whose D_gl(E) ≤ 0.
- **Interval:** the percentile interval (`np.percentile`) over the finite resamples, at level L.
  - L is 0.95 when A11 sets nominal intervals.
  - L is the calibrated level when A11 sets A10 §2.6: the double bootstrap 2,000 × 1,000, seeds 20261912/20261913, check seeds 20261914 and 20261920, as C.
- One-sided tests at 0.025 use the lower end of the two-sided interval.

## 6. Pre-registered sequence (per family, in this order)

| Step | Rule | Passes when |
|---|---|---|
| XA, room | C's H0 | R_gl's lower end > 0, and D_gl(E) > 0 in ≥ 97.5% of resamples |
| XB, E5 detection | C's H1 | the lower ends of RR_gl(E5) and of RR_gl(E5) − RR_gl(E5p) are > 0 |
| XC, N's classification | Section IV-C rule, C's H3 on the tracker of record | class (a), (b) or (c) below |

XC uses r = RR_gl(N) and c = RR_gl(E5_N):
- (a) **recovers** if r's lower end > 0;
- otherwise (b) **uninformative variation** if c's lower end > δ = 0.05;
- otherwise (c) **amplitude-limited** if c's interval is inside (−δ, δ);
- otherwise (d) **inconclusive**.

Under (a), the efficiency r / c is also reported: its point and its interval over resamples (r_b / c_b, finite only) at r's level.

A step is **confirmed** when it and every earlier step pass. If XA fails, the statement is: "No measurable room in that data set. Nothing is tested there." (A10 §9). XB and XC are still computed and labelled "not tested".

## 0. Update of 21 Nov 14:25 EST: A11 §3 governs X
AMENDMENT_11_v13.md §3 is the specification. Where this file differs, A11 wins. The changes are:
- **Family:** pedestrian crossing only.
- **Cases:** `crossing\CASES_X_PC_v13.json` (SHA-256 `58902be5ce022b314148308140cb8fc9373bc7aee401531367d456755409a31e`, made by `make_cases_x_pc_v13.py`).
  - 390 study positions (130 per speed) and 15 reserves (5 per speed).
  - The protocol's 300 never-run cases come first; the rest come from the generator extension (indices ≥ 1800).
  - Job ids `pc13x_<case>_native` (field `job`). Replacements go in `crossing\REPLACEMENTS_X_v13.json` only, as `{"replacements": {case: reserve case}}`, a reserve of the same speed. No other name is used.
- **Analysed set:** the listed runs (with replacements) that have arrays, i.e. those CAPTURED_AND_REVIEWED by 18:30. With fewer than n_min = 332 runs, the result is "descriptive, under-run" and no step is confirmatory.
- **Steps:** X0 (= XA), X1 and X2 (= XC).
  - **X1:** the lower ends of RR_gl(E5_N) and of RR_gl(E5_N) − RR_gl(E5p_N) are both > 0. E5p_N is E5_N with u permuted within runs (`default_rng(20261915)`).
  - The record-amplitude E5 and E5p (1.1029, 0.05) are descriptive only, at nominal 95%.
- **Intervals:** A10 §2.6 calibrated, in both programs, for R_gl, RR_E5N, RR_E5N − RR_E5pN and RR_N. Seeds are C's. The emergency rule: if the calibration is not done by 21:15, the nominal 99% interval is used.
- **Flat keys (prefix `X.ped.`)**, which replace those of §7:
  - Counts: `n_runs`, `n_dec`, `n_contact` (runs whose arrays' `meta.contact_k` ≥ 0), `n_replaced`, `under_run` (bool; n_runs < 332, false in the old-run test).
  - Room: `R`, `R.dec`, `R.share_pos`, `R.ci`, `R.level`.
  - Main statistics: `RR_E5N`, `RR_E5NmP` and `RR_N`, each with `.ci` and `.level`.
  - Descriptive: `RR_E5rec` and `RR_E5recmP`, each with `.ci` and `.level` = 0.95. `RR_N.inside_delta` (bool: RR_N's interval inside (−δ, δ) at its level).
  - Ratio check: `ratio.median`, `ratio.A`, `ratio.within5`, `ratio.barely`.
  - Classification: `X2.class`, `X2.eff`, `X2.eff.ci`.
  - Steps: `X0`, `X1`, `X2` and their `.confirmed`; `tested` (= X0).

## 7. Outputs
- First program: `crossing\out\X_CROSS_<family>_v13.json`.
- Second program: `recount\out\RC_X_CROSS_<family>_v13.json`. Old-run tests carry a `TESTOLD_` prefix.
- Both write a flat `values` dict with these keys; F is `veh` or `ped`:
  - `X.F.n_runs`, `X.F.n_dec` (int); `X.F.R` (pp), `X.F.R.dec`, `X.F.R.share_pos` (share of resamples with D_gl(E) > 0);
  - `X.F.R.ci`, `X.F.R.level`;
  - for S in `RR_E5`, `RR_E5mP` (= RR_E5 − RR_E5p), `RR_N`, `RR_E5N`: `X.F.S`, `X.F.S.ci`, `X.F.S.level`;
  - `X.F.ratio.median`, `X.F.ratio.A`, `X.F.ratio.within5`, `X.F.ratio.barely` (bool);
  - `X.F.XC.class` (one of: "recovers", "uninformative variation", "amplitude-limited", "inconclusive"); `X.F.XC.eff` and `X.F.XC.eff.ci` (null unless recovers);
  - `X.F.XA`, `X.F.XB`, `X.F.XC` and `X.F.<step>.confirmed` (bool); `X.F.tested` (= XA).
- An undefined number or interval is null. The comparison is `crossing\compare_x_v13.py`.
- Values to compare (A10 §10.1(c): within 1e-9, counts exact, levels equal, classes equal):
  - n_runs; n (evaluated decisions); R_gl and R in decision-equivalents (`dec_eq` = D / 201 / 100 · n);
  - the five statistics (point and interval);
  - share of resamples with D_gl(E) > 0;
  - the ratio summary (median, A, share within 5%, barely varies);
  - the class, and r / c under (a);
  - XA, XB and XC, and the confirmed flags.

## 8. Not carried over from package C (lead-braking constructs)
- The tracker-estimated lead phases (before braking, braking, stopped) and their populations.
- H4, the per-phase schedule.
- CK3, the braking prior.
- TG, NA, AM and Q.
- The IMM re-track: C's H3 used the IMM tracker. Here XC uses the tracker of record's N, as the sprint asks.
- The extractor runs with lead=False and a4=False, so no lead-state, CK3, NA, AM or Q arrays exist.
- If A11 sets nominal intervals, that is a stated departure from A10 §2.6.

## 9. Gate
- Both programs refuse to read a fresh crossing array unless `revision_v13\LOCK_A11.txt` exists.
- Each has an old-run test mode on the stored arrays of record (`gateR_rt_v01`, all stored runs of the family, tuning and fit), which reads no fresh run.
- The first program's old-run points equal package B's step 0 (`B_retrack\out\step0\STEP0_CROSSING_v01.json`) for R, RR_N, RR_E5N and RR_E5.
