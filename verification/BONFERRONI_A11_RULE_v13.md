# A11 Bonferroni check: rule, written before any computation (22 Nov 2026, about 06:30 EST, session CD)

The coordinator asked for this at 06:19: optional, quick, laptop only, existing exports and outputs only, reported as it comes out. It is a sensitivity check. It changes no A11 result; A11 §3.5 fixed "no adjustment across families (stated)".

## Sequences (m)
- A11's confirmatory sequences, each one-sided at 0.025 per step (A11 §3.5, §6b, §6c.6), are:
  - X (X0, X1, X2);
  - Y (Y1);
  - DR (DR0, DR1, DR2).
- E4 (§6d) is a classification of a comparison that is not caution-matched, with no equal-caution claim. B1r (§6) is a disclosed addendum. Neither is a one-sided 0.025 test sequence.
- **Primary m = 4:** E4 is counted anyway as a family, which is conservative. Also reported: m = 3.
- Bonferroni level per step: one-sided α_B = 0.025 / m. That is 0.00625 for m = 4 and 0.00833 for m = 3.

## Evidence used (existing exports only)
- X: `CD_capture\out\A_EXPORT_X.json`.
- Y: `CD_capture\out\A_EXPORT_Y.json`.
- DR: `F_dropout\out\DR_RESULTS_v01.json`.
- No resample is recomputed.

## Per inequality (statistic T, its null value t0, point t, exported percentile interval [lo, hi] at two-sided level L)
1. **Direct, if possible.** If L ≥ 1 − 2·α_B (98.75% for m = 4) and lo > t0, the step survives. For example, X1's RR_E5N is exported at 99%.
2. **Otherwise, a normal approximation on the tested side.** SE_low = (t − lo) / z_{(1+L)/2}, z = (t − t0) / SE_low, p ≈ 1 − Φ(z). The step survives if p ≤ α_B. This is an approximation (the record's intervals are percentile intervals), labelled as such.
3. **Share clauses** (X0, DR0: "D > 0 in ≥ 97.5% of resamples") become share ≥ 1 − α_B (99.375% for m = 4), read from the exported share.

## Steps and the inequality each one rests on
- **X0:** R_gl > 0 (t0 = 0) and R.pos_share ≥ 1 − α_B.
- **X1:** RR_E5N > 0 and RR_E5N − RR_E5pN > 0.
- **X2 = "uninformative variation":**
  - r = RR_N is NOT above 0. A wider interval keeps this.
  - c = RR_E5N > δ = 0.05 (t0 = 0.05).
- **Y1:** Δ > 0.
- **DR0:** R_gl > 0 and R_gl.share_pos ≥ 1 − α_B.
- **DR1:** c_DR > 0 and cdiff > 0.
- **DR2 = "recovers":** r = RR_gl(N_DR) > 0.
  - If this step fails, DR2's class is re-read by A11's rule: (b) "uninformative variation" if c_DR's lower end > δ, tested as above with t0 = 0.05.

A sequence survives if each of its confirmed steps survives in order. Every number is reported as it comes out, including a step that does not survive.
