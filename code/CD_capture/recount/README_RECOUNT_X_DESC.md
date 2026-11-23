# Recount of X's fixed descriptive outputs (A11 section 3.6, pedestrian crossing), revision v13

Written 21 Nov 2026 by Claude Sonnet 5.5 (`claude-sonnet-5-5`), second program. Read: `crossing\CD_DEFINITIONS_X_DESC_v13.md`, `AMENDMENT_11_v13.md` section 3, `crossing\CD_DEFINITIONS_X_v13.md` section 0. Not opened: `x_desc_v13.py`, `x_cross_v13.py`, `crossing\out\`, anything under `analysis\` or `tools\`, forbidden paths, any fresh array.

Code: `rc_x_desc_v13.py`; imports unchanged `rc_core_v13` (own gridless curves/kernel, e5_u, ratios, percentile interval), `rc_x_cross_v13` (loaders, LOCK_A11 gate, case selection) and `optA_lib_v02` (select_grid, stats_scored, eval_scoring, boot_counts, dec_eq).

## Run (from recount\, `..\.venv\Scripts\python.exe -I -B -X utf8`; env and BelowNormal priority set by the program)
- Old: `rc_x_desc_v13.py --test-old --nboot 2000` -> `out\TESTOLD_RC_X_DESC_pedestrian_crossing_v13_b2000.json`.
- Fresh: `rc_x_desc_v13.py --cases-sha 58902be5ce022b314148308140cb8fc9373bc7aee401531367d456755409a31e [--n 390]` -> `out\RC_X_DESC_pedestrian_crossing_v13.json`. Refuses without LOCK_A11.txt and with a reduced --nboot. Never overwrites.

## Choices
- Resamples: `L.boot_counts(n, nboot, 20261911)` (rows are sequential draws, so a smaller nboot is the first rows). Intervals: np.percentile 2.5/97.5 over finite resamples; ratios NaN where D_gl(E) <= 0.
- u = rc e5_u (mid-rank among evaluated decisions that have an F0/E ratio; others 0.5). f_i = np.quantile(ratios, u_i) (linear) for every decision; only evaluated ones enter the curves.
- Gridless PO and E5q on the own 201-level kernel; grid placebo through select_grid/stats_scored/eval_scoring with the evaluated mask (F0's g=0 point prepended inside the library). `grid.R` = D(E)/201 (pp), reported even if D(E) <= 0.
- u_po drawn over all decisions of the array files (clear.shape[0] per run), runs in loaded order (old: file-name order; fresh: ascending run id).
- grading_ok false if any PO is null.
- Extra (documentation) output fields outside `values`: gridless/grid details.

## Test (old runs, nboot 2000)
51 runs, 13,821 evaluated decisions, 15,300 decisions in all. RR_gl(N) = -0.43229869545659005 (matches package B step 0 exactly). Not tested: fresh mode (no fresh arrays, by rule).
