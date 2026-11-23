# Text for AMENDMENT_13 §3: N_DR against a fixed coast-count margin (session F), v02

Drafted by session F (Claude Opus 5.5), 22 Nov 2026, for the coordinator to merge verbatim. No value of this test on A11's or the new
runs exists before LOCK_A13b.
- **v01** (frozen in FREEZE_DR_A13) carried the coordinator's 07:12 changes: an amendment label with a Holm entry, a plain percentile
  interval, and the failure wording.
- **v02** makes the primary arm a COAST-COUNT margin (F0_coast) and keeps v01's two-population flag as a descriptive secondary. Only
  §3.2–3.3, the secondary and the keys change.

---

### 3. N_DR against a fixed coast-count margin (F0_coast)

**3.0 Record of the design change.**
- **Whose decision:** the coordinator's. It acts on the domain seat's report, which asked for a class average that knows how many
  updates in a row a track has missed. That is the fairer baseline for a covariance that grows with the coast count.
- **What was known:** the coordinator made the change before any value of this test on A11's or the new runs existed.
- **The v01 code test:** it ran on the 35 old test runs only, and its values are in `notes\DR_A13_RECORDS_v01.md`. The coordinator had
  not seen them, and they did not inform the change. Session F had seen them, but did not make the change.

**3.1 Question.** Under detection dropouts, does N_DR rank decisions better than a fixed extra margin that knows only the dropout
state and the number of consecutive missed frames?

**3.2 Arm F0_coast.**
- **Scales:** F0_DR's critical scales (P̄_DR, A11 §6c.5), multiplied per decision by a k chosen by the frame the decision uses
  (`dr_frame`, with the run's masked frames from its metadata):
  - **k_c** if the frame is masked and is the c-th consecutive masked frame, c = 1, 2, 3 (`dr_age`). By the mask law L ≤ 3; a count
    above 3 would use k_3.
  - **k_re** (re-acquisition) if the frame is not masked and frame − 1 or frame − 2 is masked.
  - **1** (steady) otherwise, including decisions with no frame yet.
- **Value rules:** multiplication keeps inf, −inf, 0 and NaN as they are.
- **Available online:** the coast count is known at decision time.
- **Support:** dropouts are whole-frame, so every actor of a dropout frame coasts the same number of frames. F0_coast inflates every
  actor, as N does.

**3.3 k.**
- **Relative to steady:** RR_gl does not change when all of a source's critical scales are multiplied by one constant, so each k is
  taken relative to steady: k_c = M_c / M_st and k_re = M_re / M_st.
- **M_S:** the MEDIAN of cN / cF0 over the rows (actors) of the evaluated decisions in population S where both are finite and > 0.
- **Fallback:** a coast-count population with fewer than 50 such rows on the fit runs takes the pooled in-dropout k instead,
  k_in = M_in / M_st, with M_in over all in-dropout rows.
- **Fit set:** A11's 105 fresh lead-braking runs (`F_dropout\out\arrays\DR\`: p = 0.10, punish_num 3, P̄_DR), which are disjoint from
  the test runs. k uses no data of the 150 new runs.

**3.4 Test.** On the 150 new runs of A12 §3a (`F_dropout\out_a12\p010\arrays\DR\`, DR2's room F0_DR, E_DR):
- **Statistics:**
  - RR_gl(F0_coast);
  - RR_gl(N_DR), reused (equal to DR2's r);
  - Δ = RR_gl(N_DR) − RR_gl(F0_coast) = (D_gl(N) − D_gl(F0_coast)) / D_gl(E, F0).
- **Draw:** DR2's, `optA_lib_v02.boot_counts(150, 20000, 20261911)`.
- **Interval:** a plain 95% percentile interval. A10 §2.6 calibration is not applied.
- **One-sided p:** p_F = (1 + #{Δ\* ≤ 1e-12, NaN counted}) / 20,001.
  - Δ\* within 1e-12 of 0 is a tie. Exact ties occur when a resample's runs give N and F0_coast the same D, and floating-point round-off
    can give them either sign. They count against the test, so that both programs count alike.
- **Pass:** "passed (amendment)" if Δ's lower end > 0; otherwise "failed (amendment)".
- **Secondary, descriptive, not in Holm:** v01's two-population flag F0_flag2 (k_in on in-dropout decisions, k_re on re-acquisition
  decisions, 1 on steady ones), with RR_gl(F0_flag2) and Δ2 = RR_gl(N) − RR_gl(F0_flag2) on the same draw.

**3.5 Label and Holm.**
- An AMENDMENT test, like E6: one new arm against an arm whose results are already public.
- p_F enters A13 §4's Holm with E6's (m = 2).
- **Disclosure:** the test was designed after DR2 and its decomposition were seen, and N's arm is reused.

**3.6 Wording.**
- **Pass:** "N's gain over a fixed coast-count margin is shown: Δ = [..], 95% [..]."
- **Fail:** "N's gain over a fixed coast-count margin was not shown; the interval [..] includes 0".
  - If both ends also lie inside (−0.05, 0.05) on the share scale, add: "and is within the equivalence margin".

**3.7 Missing data.**
- Rows with a non-finite or non-positive cN or cF0 are left out of M_S.
- A resample with D_gl(E, F0) ≤ 0 gives Δ\* = NaN, which counts against the test.
- All 150 runs enter, and all 105 fit runs enter.

**3.8 Programs, verification, export.**
- **First program:** `F_dropout\code\dr_flag_v02.py`, laptop, BelowNormal. It refuses without `LOCK_A13b.txt`.
  - Its `--test-old` mode fits k on, and scores, the 35 old test runs (`out\testold\DR\`): a code test only.
- **Second program:** Claude Sonnet 5.5 extends its recount from this text, without reading the first program.
- **Agreement:** per A10 §10.1(c).
- **Export:** `work\F_nuscenes\out\A_EXPORT_DRF.json` / `A_RECOUNT_DRF.json`, prefix `DRF.`. Keys:
  - DRF.n_runs, DRF.n_fit_runs;
  - DRF.M_1, DRF.M_2, DRF.M_3, DRF.M_re, DRF.M_st, DRF.M_in;
  - DRF.k_1, DRF.k_2, DRF.k_3, DRF.k_re, DRF.k_in;
  - DRF.k_1.fallback, DRF.k_2.fallback, DRF.k_3.fallback (true when the pooled k_in is used);
  - DRF.n_fit_rows.{1, 2, 3, re, st, in};
  - DRF.n_dec.{c1, c2, c3, reacq, steady};
  - DRF.RR_N (.ci), DRF.RR_coast (.ci), DRF.delta (.ci), DRF.delta.p, DRF.passes, DRF.within_equiv, DRF.status;
  - secondary: DRF.RR_flag2 (.ci), DRF.delta_flag2 (.ci).
