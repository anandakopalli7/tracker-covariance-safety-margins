# E recount, second program (v03)

Second program for package E (A10 section 10.1(b)). Written from `AMENDMENT_10_v13.md` (sections 0, 5.8, 7), the brake-test rule and
planner model (`DESIGN_NOTES_v01.md` 6.4e, `PROPOSAL_CARLA_CONFIRMATION_v03.md` 2, `design_core_v85.trajectory`, the stand-in's STOP mode), and the
raw run files. The first program (analysis, src, tests, review) was not read. Python 3.12 + numpy only.

## Run

```
python -I -B e_recount_v03.py outcomes    <runs_dir> <prefix> --out outcomes_e3.json     # prefix: e1_ / e2_ / e3_ / e3b_
python -I -B e_recount_v03.py brake       <runs_dir> --out brake.json
python -I -B e_recount_v03.py calibration outcomes_e2.json --out calibration.json
python -I -B e_recount_v03.py compare     outcomes_e3.json [--e3b outcomes_e3b.json] --low-power true|false --out compare.json
```

`<runs_dir>` holds `<run_id>\SUMMARY.json` and `<run_id>\x\<run_id>\capture\<case>\...`. For every job the last attempt (`__rN`) is the run of
record. Every invalid or unreadable run is kept in the output with `valid: false` and its reasons; nothing is dropped silently. JSON output has
null for undefined values. Reading is slow on Windows with real-time antivirus (about 4 s per 10 runs for old open-loop runs, mostly file opening).

## Readings of the amendment (numbered; each is a choice the first program may have made differently)

### Run of record, validity
1. **Last attempt.** A job id with `__rN` appended is a retry; the highest N is the run of record, even if an earlier attempt was valid.
2. **Valid** means: SUMMARY.status is `CAPTURED_AND_REVIEWED`; no `policy_failure.json`; assessment_outcomes has no `invalid_reasons`, no `instrument_failures`, no `first_policy_failure_frame`, termination `FULL_ASSESSMENT` or `FIRST_PHYSICAL_CONTACT`; truth ticks are contiguous 0..N-1; there are assessment-mode decisions; no contact before the assessment start. An invalid run enters no table.
3. **Tick of a frame** is k = f - base_frame - 1 (as given). The assessment window starts at tick k0 = assessment_start_frame - base_frame - 1 (99 in old runs) and ends at the last truth tick. Warm-up (k < k0) is excluded from every outcome except contact.

### 7.4 outcomes
4. **Contact** = any event in `contacts.jsonl` (any other actor, no filter), **or** a tick with truth gap <= 0 **and** boxes overlapping in the route frame (|longitudinal centre offset| < sum of the two forward supports and |lateral offset| < sum of half-widths, from `derived.*_support_m`). Reason: on old runs `directional_gap_m` is also <= 0 (down to -400 m) for a road user that is beside or already behind the ego, so the bare rule "gap <= 0 means overlap" gives false contacts in crossing/benign scenarios. Where the plain rule and mine differ, results differ only for such cases; in lead scenarios they coincide.
5. **First contact tick** = the earliest of the event ticks and the first overlapping gap <= 0 tick. A disagreement with `assessment_outcomes.first_contact_frame` is written to `warnings`, not used.
6. **Impact speed** = closing speed along the route, (v_ego - v_target) . u, u = (cos, sin) of `route_yaw_rh` at that tick, velocities converted left- to right-handed (y flipped), taken at the tick **before** the first contact tick. Reason: truth record k has CARLA frame base+1+k, the frame the collision callback reports, so the record of the contact tick is already after the impulse (old run tune_0006: 10.4 m/s one tick before, -1.9 m/s at the contact tick). The post-impulse value is kept as `impact_speed_at_contact_tick_mps`. Not clipped at 0 (negative = lead faster).
7. **Time lost** (runs without contact only) = run length - forward distance / desired speed. Run length = (last tick - k0) * 0.05 s (30 s for a full run). Forward distance = ego centre displacement (right-handed centres) from tick k0 to the last tick, projected on the route direction at k0. Desired speed = `case.desired_mps`. Matches `forward_displacement_m` to 0.05 m (otherwise a warning). Null for contact runs.
8. **Rest gap** = `directional_gap_m` at the last tick, only for a run without contact whose lead is stopped (speed <= 0.5 m/s at that tick) and ahead (gap > 0) within the ego's lane width. Otherwise null. `end_gap_m` (last-tick gap, always) is a diagnostic.
9. **Speed for deceleration and jerk** = horizontal norm of the truth ego velocity (`velocity_lh` x, y), not the frames' measured speed.
10. **Smoothing.** Speed -> 5-sample moving average (0.25 s at 20 Hz, 'valid' mode, no padding, over ticks k0..end) -> a = diff/0.05 -> jerk = diff(a)/0.05. This equals the 0.25 s average of the finite-difference deceleration. **Peak deceleration** = max(-a), no restriction to moving ticks. **RMS jerk** = sqrt(mean(jerk^2)) over the same window. For contact runs both include the impact step (the run ends at contact).
11. **Fallback share** = (assessment-mode decisions in full braking) / (assessment-mode decisions). A decision is in full braking when `output.fallback` is true OR the selected `output.targets` equal (-5, -5). Warm-up decisions excluded. The flag-only quantity of v03 is kept as the extra field `fallback_flag_share`.

### 7.1 E1 brake test
12. **First fallback decision** = first `new_decision` in assessment mode with `output.fallback` true; its `tick` is k_f.
13. **Planner's model distance** = final `s` of `trajectory(-5, -5, v0, a0, desired, h = 0.05, H = 12 s)` (my copy of design_core_v85: jerk ramp 8 m/s^3, first target for t < 1 s, speed clipped to [0, 20]); H is doubled until standstill. v0, a0 = the decision's `model_state.model_speed_mps` and `model_acceleration_mps2` (the planner's own initial state), not the measured values (both are written out).
14. **Real stopping distance** = route-projected ego centre displacement from tick k_f to the first tick >= k_f whose measured speed (`frames.state.speed`) < 0.05 m/s (the stand-in's STOP rule). Ratio = real / model; within 10% = |ratio - 1| <= 0.10.
15. **Pass** = for each of 5, 10, 15 m/s (from `desired_mps`) a run with status CAPTURED_AND_REVIEWED, no policy failure (file or outcomes), no problem (no fallback decision, never stopped), within 10%. A contact is reported but does not fail the test (the rule names only policy failure and halted job). More than one run per speed: the last job id in sorted order is used (`n_runs_for_speed` shows it).

### 7.3 levels
16. **Shares** per g from E_F0 runs that are valid, contact / valid n. g = 0 included. **g_lo** = grid g whose share is nearest 0.20, **g_hi** nearest 0.05, ties to the smaller g. If every share is < 0.05 (strictly), g_lo = 0.25, g_hi = 1 and `low_power` true. No rule forces g_hi != g_lo.

### 7.5 analysis
17. **Pairs.** By case, over valid runs of both arms; an invalid run removes its case from that comparison. E_Z (level null) is compared to E_F0 at lo and at hi; E_N, E_CK3, E_TG, E_PS against E_F0 at the same level; E_N_IMM against E_F0_IMM. Extra, not in the amendment and labelled: E_F0_IMM vs E_F0. E3b: per `lead_variant`, E_N, E_CK3, E_PS, E_TG vs E_F0 at lo. Difference = arm - reference.
18. **Cells** a both, b arm only, c reference only, d neither in contact. Contact difference = (b - c)/n.
19. **Newcombe hybrid-score interval for paired proportions** = Newcombe (1998), Statistics in Medicine 17:2635-2650, method 10: Wilson score intervals (z = 1.959964) for the two marginal proportions p1 = (a+b)/n (arm) and p2 = (a+c)/n (reference), combined by square-and-add with the correlation correction phi = C / sqrt((a+b)(c+d)(a+c)(b+d)), where C = ad - bc, reduced by n/2 if it exceeds n/2, set to 0 if 0 <= C <= n/2, left as is if negative; phi = 0 if the denominator is 0. lower = D - sqrt((p1-l1)^2 + (u2-p2)^2 - 2 phi (p1-l1)(u2-p2)); upper = D + sqrt((u1-p1)^2 + (p2-l2)^2 - 2 phi (u1-p1)(p2-l2)). Formula typed from memory of the paper, not fetched (no network).
20. **Exact McNemar** two-sided = min(1, 2 P(X <= min(b,c))), X ~ Binomial(b+c, 0.5); p = 1 if b + c = 0.
21. **Time lost** = mean over the pairs in which neither run has contact of (arm - reference).
22. **Bootstrap.** For each comparison a fresh `numpy.random.default_rng(20261922)`; one matrix `rng.integers(0, n_pairs, size=(20000, n_pairs))` of case indices (rows = resamples) used for every outcome of that comparison. It resamples **all** pairs (cases), then recomputes the statistic on the resample, including which pairs are without contact; a resample with no defined pair is dropped (count in `n_boot_defined`). 95% interval = numpy `percentile` 2.5 and 97.5 (linear). An extra interval that resamples only the defined pairs is written as `ci_conditional_*` for time lost, in case the first program did that.
23. **Other outcomes** (impact speed, rest gap, peak deceleration, RMS jerk, fallback share, and time lost): mean paired difference over pairs where both are defined, same bootstrap. Impact speed is therefore over pairs with contact in both arms.
24. **Classification** by the amendment's four rules in its listed order; the first that holds wins; all that hold are in `rules_satisfied`. "within (-0.10, 0.10)" and "(-0.5, 0.5)" mean the whole 95% interval lies strictly inside. A rule that needs a time-lost bound that is undefined does not hold. Otherwise "inconclusive". Note that "worse" is listed after "equivalent", so an interval inside (0, 0.10) with time within +-0.5 s is called "equivalent" here.
25. **Low power** is only a label passed in with `--low-power`; it does not change a number.
26. **Duplicates.** If two valid runs of record share arm, level, lead variant and case, the last by run id is used and a note is written.

## Change from v02
- **Defect.** In real D1 runs `contract['case']['lead_variant']` is a dict (e.g. `{"schema": "LEAD_VARIANT_D1V13_V01", "kind": "stop_and_go", ...}`), not a string. v02 copied it into the row and keyed runs by (arm, level, lead_variant); a dict is unhashable, so `compare --e3b` would crash on real data.
- **Fix.** `lead_variant` is now the `kind` string when the contract value is a dict; a string or None is kept. New field `lead_variant_spec` holds the full original value. Each `compare` comparison record now has a `lead_variant` field: the kind for E3b, None for E3.
- **Interval convention (compare).** A10 7.5 is silent on an outcome defined for fewer than 2 pairs; v02 bootstrapped it anyway (a single pair drawn in about 13,000 of 20,000 resamples gave ci_lo = ci_hi = that value, false precision). v03: when `n_pairs_used` < 2, for every outcome, `ci_lo`, `ci_hi` and the `ci_conditional_*` fields are None, `n_boot_defined` is 0, and `mean_diff` is kept (the mean over the one pair). The time-lost bounds in the comparison record are then None, so classification rules that need them do not hold. Cells with 2 or more pairs are unchanged.
- Nothing else changed except the version labels and schema strings.
- Tests: `outcomes runs v03s_` gives stop_and_go and mild_braking for the two D1 pilots and None for the others; `test\make_synth_dict.py` writes `test\synth_dict\` (E3b with dict variants constant / mild_braking / stop_and_go): outcomes and `compare --e3b` run and pair within each kind (10 pairs each); the existing synthetic e2, e3, e3b, brake and compare results and the real E2 are identical to v02 apart from schema strings and the new fields.

## Change from v01 (to v02)
- **Disagreement.** The comparison of this program's `outcomes` on E2 with the first program disagreed on fallback share in 31 of 180 E2 runs; every other outcome agreed.
- **Cause (checked in the raw frames).** The planner's library has 16 regular trajectory rows plus a fallback, and the regular rows include the targets pair (-5, -5). In those runs some decisions select that row as a feasible regular row: the command is full braking, but `output.fallback` is false. v01 counted the flag only. Example `e2_c1109_tune_0006_f0_g0`: 66 assessment-mode decisions, 11 with the flag (all 11 also have targets (-5, -5)), 5 more with targets (-5, -5) and flag false.
- **Amendment wording** (AMENDMENT_10_v13.md, 7.4): "Fallback share: the share of decisions in full braking." v02 follows it: `fallback_share` counts flag true or targets (-5, -5); `fallback_flag_share` keeps the v01 quantity.
- Nothing else changed except the version labels and schema strings.

## Tests
(see the end of this file)

### What was run (19 Nov 2026, laptop)
- **`outcomes` on two real old open-loop runs sets** (`archives_c1`, tuning runs 0000-0009 and 0010-0019, 20 runs, all valid, no warning): contact flags agree with `assessment_outcomes.first_contact_frame` in 20 of 20 once reading 4 is used (with the bare "gap <= 0" rule 4 of the first 10 disagreed: crossing and benign cases with a road user beside or behind). `forward_displacement_m` agrees with the truth projection to 0.05 m in all 20. Contact runs end at the contact tick (truth has fewer than 700 ticks); impact speed one tick before contact is plausible (4.5-11.8 m/s) while the contact-tick record is post-impulse (reading 6).
- **Synthetic closed-loop runs** (`test\make_synth.py`, formats as in the data layout; plants with known stopping behaviour): 
  - `brake`: plant following the planner's own -5 m/s^2 jerk-limited plan: model distances 3.858 / 12.798 / 26.738 m (the stand-in's recorded model values are 3.86 / 12.80 / 26.74), ratios 1.000-1.0003, `passed` true. A plant braking at 0.7 of that at 15 m/s: ratio 1.31, `passed` false.
  - `outcomes` (E2/E3/E3b-shaped sets, 520 runs): impact speed, time lost, rest gap, peak deceleration and fallback share checked by hand against the constructed kinematics (impact 6.0 m/s; time lost 26.2 s; rest gap 28.75 m; peak deceleration 6.0 m/s^2). A retried job (`__r1`) is used over its failed first attempt.
  - `calibration`: built-in shares 0.50 / 0.35 / 0.20 / 0.10 / 0.05 / 0.00 give g_lo 1, g_hi 16, low_power false.
  - `compare`: 22 comparisons. McNemar exact checked by hand (4 discordant, p = 0.125; 10 discordant, p = 0.00195); Newcombe interval for (8, 0, 0, 12) checked by hand (-0.0952, +0.0952); Wilson limit for 0 of 10 (0.2775) reproduced. Classification runs through "equivalent", "safer at a cost" (upper time bound exactly 0.5 s counts as >= 0.5), "worse" and "inconclusive". Invalid runs drop their case from a pair; an empty pair set gives "no pairs".
- **Not tested**: the real closed-loop data (none exists yet), a `lead_variant` that is not a string, planner `projected` model states (v0 is read from `model_state` as is), `E_BRAKE` runs with a real policy-failure file, the bootstrap against any other implementation, Newcombe's formula against the paper (no network).

## `matched` (A10 7.3 and 5.5), added on request

```
python -I -B e_recount_v03.py matched --calib ..\out\E2_RECOUNT_CALIB_v03.json --out out\E2_RECOUNT_MATCHED_v03.json
```
Reads g_lo and g_hi from the calibration file, loads the 35 old evaluation runs through the loader of record (`rev_common_v01.load_runs`, scoring library `optA_lib_v03`), TG arrays (`cTG2`), tracker lead state (`lead\*.npz`) and the B1 IMM arrays (`cF0`, `cN`). About 30 s. The output went to `recount\out\` (not `E_closedloop\out\`), because this program may write only inside `recount\`; copy it if needed.

Readings:
M1. **Caution** = the scoring 'W1' (safe = clearance > 0), population 'all' (every evaluated decision), summed over the 35 runs: sum of speed shortfalls to the first W1-safe row over the number of selected-safe decisions (`stats_scored`, `rates`, column 2). This follows the instruction text, not my own definition.
M2. **F0's caution at g_L** is computed at g_L itself (4 and 16 are not on the 202-value grid) by selecting with the critical values at that scale, not at the nearest grid value.
M3. **Other arms**: the grid scale (all 202 values, 0 included) with caution nearest F0's caution at g_L; ties to the smaller g (first minimum on an ascending grid). N, CK3 from the loader's arrays, TG from `cTG2`, F0_IMM and N_IMM from the B1 `cF0` and `cN` (the loader's `idx55`, `clear1`, `vbar` are used for them; k, idx55 and evaluated were checked equal to the B1 files in all 35 runs).
M4. **Phase for PS** from the stored tracker estimate: no lead track -> 0 (before braking); `vhat` <= 0.5 -> 2 (stopped); else `ahat_long` <= -1.0 -> 1 (braking); else 0. Evaluated decisions only. The stored `phase` field in the lead and A4 files is not this (it agrees with the truth phase, not with the estimate: they differ in 360 of 8290 decisions), so it is not used. `vhat` is taken as the lead track's speed and `ahat_long` as its acceleration along its velocity.
M5. **Triple order** is (before braking, braking, stopped) = phases 0, 1, 2, over all 202^3 triples, phase 0 the slowest index; flat index = lexicographic over (i0, i1, i2). The convention of the first program's triple order is not known to me.
M6. **Triple statistics** are additive over phases: wrong go = sum of the three phases' counts of selected-unsafe decisions over all evaluated decisions; caution = summed shortfall over summed selected-safe count. Check: triples (i, i, i) reproduce the single-scale 'all' caution to 1.4e-14 and wrong go exactly.
M7. **Triple choice**: among triples with design caution <= the level (+1e-12), the lowest wrong go; ties to the lowest caution (rounded to 1e-9), then the lowest flat index. The level is F0's caution at g_L (M2).
M8. The PS triple at both levels is the same (wrong go 0.0 is reached below both levels and the tie-break picks the lowest caution).
