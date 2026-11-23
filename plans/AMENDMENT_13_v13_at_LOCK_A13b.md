# AMENDMENT 13 to the v13 pre-registration (A13): two controls asked for by the round-2 panel

Written 22 Nov 2026 from about 06:30 EST (laptop clock) by the coordinating session (Claude Opus 5.5), with section texts by the package sessions named in each section. It adds two tests. It changes no earlier test, label or result.

## 0. Why, and what was known when this was written

- The round-2 panel (five seats, run on the text frozen at 06:23:03, `freeze_v13_0623`) raised two points in four of its five seats:
  1. The "caution-matched" closed loop (A12 §6, E5) is matched in OPEN-loop caution only. In closed loop the covariance arm lost 0.18 s more time and stopped about 1 m farther back, so its fewer contacts cannot yet be told from a wider margin. The class-average arm ran at one scale only, the bottom of its grid.
  2. The open-loop dropout gain (A12 §3a) looks like a level effect: in-dropout decisions alone give a share near zero. A fixed margin increase during dropouts was not tested.
- Known before this amendment: every A12 result, including E5's two arms on the 135 test cases (contact shares, time lost) and DR2's decomposition on the 150 new runs. Section 2 reuses E5's two arms; section 3 reuses DR2's arrays. Both reuses are stated in the text of the paper.
- Labels (as A12 §1): each test here is an amendment test, "passed (amendment)" or "failed (amendment)". Neither is "confirmed".

## 1. Order, locks and cut-offs

- Each section is locked before any value of it exists: section 2 by LOCK_A13a, section 3 by LOCK_A13b. Each lock records the package's freeze and sealing evidence.
- Cut-off: a result not recounted by 10:00 EST is reported as "not completed" and enters section 4 as p = 1.
- Money: the RunPod balance must stay above $3 with pods running (the author's rule of about 03:25). Section 2 runs at most 6 pods, deleted by a watchdog at $3.5; section 3 runs on the laptop only.

<!--MERGE:E6-->
## 2. The closed-loop caution frontier (E6, session E)

*Added before LOCK_A13a; not part of LOCK_A13b. No E6 run exists at this lock.*


**Coordinator's note on section 3 (laptop clock 06:40 EST, 22 Nov).** The text below is session F's v01, merged verbatim (`work\F_dropout\A13_3_DRFLAG_v01.md`). After the domain seat's report the coordinator asked for a coast-count version (a factor per consecutive missed update); that request reached F only after F had frozen v01 (FREEZE_DR_A13) and run its code test on the 35 old test runs. The coordinator then learned the code test's values. To avoid a choice made after seeing values, the two-population flag of v01 is kept unchanged and the coast-count version is not run. The code test (k fitted and scored on the 35 old runs only; no A11 or new-run value) is design data and is reported as such.

## 3. N_DR against a fixed dropout-flag margin (F0_flag)

**3.1 Question.** Under detection dropouts, does N_DR rank decisions better than a fixed extra margin that is switched on by the
dropout state alone? The text's decomposition puts most of DR2's gain in dropout. This tests whether that gain is more than a flag.

**3.2 Arm F0_flag.**
- **Scales:** F0_DR's critical scales (P̄_DR, A11 §6c.5), multiplied per decision by k_in on in-dropout decisions, by k_re on
  re-acquisition decisions, and by 1 on steady decisions.
- **Populations:** as A12 §3a.5, by the frame the decision uses (`dr_frame`; the run's masked frames from its metadata):
  - in-dropout: the frame is masked;
  - re-acquisition: the frame is not masked, and frame − 1 or frame − 2 is masked;
  - steady: everything else, including decisions with no frame yet.
- **Available online:** the flag is known at decision time, because the tracker knows that a frame brought no detection. Dropouts are
  whole-frame, so every actor of a dropout frame coasts. The flag inflates every actor, as N does.
- **Value rules:** multiplication keeps inf, −inf, 0 and NaN as they are.

**3.3 k.**
- **Relative to steady:** RR_gl does not change when all of a source's critical scales are multiplied by one constant, so only k
  relative to steady matters. k_in = M_in / M_st and k_re = M_re / M_st.
- **M_S:** the MEDIAN of cN / cF0 over the rows (actors) of the evaluated decisions in population S where both cN and cF0 are finite
  and > 0. The median is used because the ratio's right tail would dominate a mean.
- **Fit set:** A11's 105 fresh lead-braking runs (`F_dropout\out\arrays\DR\`: p = 0.10, punish_num 3, P̄_DR), which are disjoint from
  the test runs.
  - The 120 tuning runs hold P̄ sums only and no decision arrays.
  - k uses no data of the 150 new runs.

**3.4 Test.** On the 150 new runs of A12 §3a, using DR2's arrays at p = 0.10 (`F_dropout\out_a12\p010\arrays\DR\`) and DR2's own room
(F0_DR, E_DR):
- **Statistics:**
  - RR_gl(F0_flag);
  - RR_gl(N_DR), which is reused (equal to DR2's r);
  - Δ = RR_gl(N_DR) − RR_gl(F0_flag) = (D_gl(N) − D_gl(F0_flag)) / D_gl(E, F0).
- **Draw:** DR2's, `optA_lib_v02.boot_counts(150, 20000, 20261911)`.
- **Interval:** a plain 95% percentile interval. A10 §2.6 calibration is not applied.
- **One-sided p:** p_F = (1 + #{Δ\* ≤ 0, NaN counted}) / 20,001.
- **Pass:** "passed (amendment)" if Δ's lower end > 0; otherwise "failed (amendment)".

**3.5 Label and Holm.**
- An AMENDMENT test, like E6: one new arm against an arm whose results are already public.
- p_F enters A13 §4's Holm with E6's (m = 2).
- **Disclosure:** the test was designed after DR2 and its decomposition were seen, and N's arm is reused.

**3.6 Wording.**
- **Pass:** "N's gain over a fixed dropout-flag margin is shown: Δ = [..], 95% [..]."
- **Fail:** "N's gain over a fixed dropout-flag margin was not shown; the interval [..] includes 0."
  - If both ends also lie inside (−0.05, 0.05) on the share scale, add: "and is within the equivalence margin".

**3.7 Missing data.**
- Rows with a non-finite or non-positive cN or cF0 are left out of M_S.
- A resample with D_gl(E, F0) ≤ 0 gives Δ\* = NaN, which counts against the test.
- All 150 runs enter, and all 105 fit runs enter.

**3.8 Programs, verification, export.**
- **First program:** `F_dropout\code\dr_flag_v01.py`, laptop, BelowNormal. It refuses without `LOCK_A13b.txt`. Its `--test-old` mode
  fits k on, and scores, the 35 old test runs: a code test with no A11 or new-run value.
- **Second program:** Claude Sonnet 5.5 extends its A12 recount from this text, without reading the first program.
- **Agreement:** per A10 §10.1(c).
- **Export:** `work\F_nuscenes\out\A_EXPORT_DRF.json` / `A_RECOUNT_DRF.json`, prefix `DRF.`. Keys:
  - DRF.k_in, DRF.k_re, DRF.M_in, DRF.M_re, DRF.M_st and the fit row counts;
  - DRF.n_dec.{in, reacq, steady};
  - DRF.RR_flag (.ci), DRF.RR_N (.ci), DRF.delta (.ci), DRF.delta.p;
  - DRF.passes, DRF.within_equiv, DRF.status.

## 4. Multiplicity

Holm across A13's primary hypotheses (section 2's Δ and, if locked, section 3's difference), each with its one-sided p as defined in its section; m = the number of sections locked. Reported beside A12's Holm, not merged with it.
