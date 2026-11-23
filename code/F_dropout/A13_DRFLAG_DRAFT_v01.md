# DRAFT for AMENDMENT_13: a fixed dropout-flag margin (F0_flag) against N_DR (session F, 22 Nov 2026, about 06:55 EST)

Draft only. No value of this arm exists. Every choice below is fixed before any is computed.

**A13.1 Question.** Is N_DR's gain under dropouts more than a fixed extra margin in dropout states, i.e. ranking beyond a flag?

**A13.2 Arm F0_flag.**
- F0_DR's critical scales (P̄_DR, A11 §6c.5), multiplied per decision by k_in on in-dropout decisions, by k_re on re-acquisition
  decisions, and by 1 on steady decisions.
- Populations as A12 §3a.5 (the decomposition's code), by the decision's frame:
  - in-dropout: the frame is masked;
  - re-acquisition: the frame is unmasked and one of the two previous frames is masked;
  - steady: everything else, including decisions before the first frame.
- The flag is known online: the tracker knows a frame brought no detection.

**A13.3 k.**
- RR_gl does not change when all of a source's critical scales are multiplied by one constant. Only k relative to steady matters:
  k_in = M_in / M_st and k_re = M_re / M_st.
- M_pop is the MEDIAN of cN / cF0 over the finite, positive rows of the evaluated decisions in that population. The median is used
  because the ratio's right tail would dominate a mean.
- **Fitted on A11's 105 fresh runs** (their DR arrays: p = 0.10, punish_num 3, P̄_DR). Not fitted on the 150 new runs. The 120 tuning
  runs hold P̄ sums only, no decision arrays.

**A13.4 Test (on the 150 new runs, DR2's arrays at p = 0.10).**
- Statistics:
  - RR_gl(F0_flag) on DR2's own room;
  - Δ = RR_gl(N_DR) − RR_gl(F0_flag) = (D_gl(N) − D_gl(F0_flag)) / D_gl(E, F0).
- Draw: `boot_counts(150, 20000, 20261911)`, the same draw as DR2. 95% percentile intervals, with no A10 §2.6 calibration
  (exploratory).
- One-sided p = (1 + #{Δ\* ≤ 0, NaN counted}) / 20,001.
- **N beats the flag** if Δ's lower end > 0. Otherwise the text says "a fixed dropout-flag margin gives the same gain within the
  interval".
- Also reported: k_in, k_re, the population counts, and RR_gl(F0_flag) with its interval.

**A13.5 Label.** EXPLORATORY, designed after DR2's values (including the decomposition) were seen. The p is recorded, not tested in
Holm.

**A13.6 Missing data.**
- Rows with a non-finite or non-positive cN or cF0 are left out of M_pop.
- cF0 × k keeps inf and 0 as they are.
- A resample with D_gl(E, F0) ≤ 0 gives NaN, which counts against Δ.
- All 150 runs enter; no run is dropped.

**A13.7 Verification.** The second program (Claude Sonnet 5.5) extends its A12 recount from this text. Agreement per A10 §10.1(c).
Laptop only.
