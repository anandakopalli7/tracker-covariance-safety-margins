# A11 DR, post hoc: the resample-count p of r (descriptive)

Session F (Claude Opus 5.5), 22 Nov 2026, about 06:40 EST. Requested by the coordinator (06:25) after CD's post hoc Bonferroni check.
That check rated A11's DR2 step against α = 0.00625 with a normal approximation from the exported 95% interval, which gave p ≈ 0.0057.
This note replaces that approximation with the count over A11's own resamples. It is POST HOC and descriptive; no A11 file or decision
changes.

## Method

- **Program:** `code\dr_posthoc_pr_a11_v01.py` (sha 26c392df…). It is a copy of the frozen `code\dr_analysis_v01.py` (FREEZE_DR) with
  only these changes:
  - the output path is `out\posthoc\DR_A11_PR_POSTHOC_v01.json`;
  - no calibration (A11's levels were all nominal 95%);
  - the p of r is added exactly as `dr_analysis_v02.py` writes DR.p_r: (1 + #{r* ≤ 0, NaN counted}) / (20,000 + 1).
- **Draw:** A11's own draw, `optA_lib_v02.boot_counts(105, 20000, 20261911)`, over A11's arrays (`out\arrays\`).
- **Built-in check:** DR.r, DR.r.ci, DR.R_gl, DR.R_gl.ci, DR.c and DR.c.ci equal `out\DR_RESULTS_v01.json` exactly. All True.
- **Run:** laptop, BelowNormal, 4 numba threads, one process, 511 s. Log `logs\posthoc_pr_a11.log`.

## Result (first program)

- 102 of the 20,000 resamples have r* ≤ 0; none is NaN.
- **p_r = (1 + 102) / 20,001 = 0.00515.** This is below α = 0.00625, so A11's DR2 step survives the post hoc Bonferroni check on the
  resample count.
- r = 0.0283, 95% interval [0.0064, 0.0496] (as exported).

## Second program

The A11 recount's author (Claude Sonnet 5.5) reproduced the count with a post hoc copy of its own `recount\dr_recount_v02.py`:
`recount\dr_recount_a11_pr_posthoc_v01.py` (af1e0f42…).
- It differs from v02 only by the output name, the skipped calibration and the new count keys.
- Output: `recount\DR_A11_PR_POSTHOC_RECOUNT_v01.json` (32acc55d…). Run: 237 s, laptop, BelowNormal, 4 threads.
- Result: **102 resamples with r\* ≤ 0, 0 NaN, p_r = 0.005149742512874356.** This is identical to the first program.
- DR.r and DR.r.ci reproduce its A11 recount exactly.
