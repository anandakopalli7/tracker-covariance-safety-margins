# Step-0 recount (second program), 21 Nov 2026, Claude Sonnet 5.5

Written from AMENDMENT_11 s2 and AMENDMENT_10 s2.1-2.3. The first program's code (`B_retrack\code\b_*.py`) was not opened. Its output files were opened only after `STEP0_RECOUNT_v01.json` and `A_RECOUNT_S0.json` were written. The program was not changed after that.

**Shared with the first program:** the stored arrays (gateR_rt_v01, runs in file-name order); `trk_score_v01` (`make_run`, `gridless`, `rr_gl` used only as a cross-check); `optA_lib_v02` (`boot_counts(n, 20000, 20261121)`, `dec_eq`, `clean_clear`); `gl_fast_v13` (frontier kernel: 201 levels, step frontier, 3 s commitment, all evaluated decisions). The resample draw is the same.

**Own code (`step0_recount_v01.py`):** run selection by meta (family; set tuning/fit), margin ratio and its summary, ranks u, E5_N and E5 scales, shares and intervals, the unbound/unsafe shares, the lead-braking reference, `make_export_v01.py` (45 keys), `compare_v01.py`. Full-sample gridless values were also computed with the library path (a9 curves + `eval_scoring`); difference 0.0 in all four sets (`crosscheck_lib`).

**Conventions chosen**
- Margin ratio = sqrt(cF0 / cN) at rows with finite positive cF0 and cN in evaluated decisions (the convention of record, m = 1.1029 on lead braking). A = (q95 - q05) / (2 m), numpy linear quantiles. "Within 5%" = |ratio - median| <= 0.05 median.
- u_i = (mid-rank - 0.5) / n, where n is the number of evaluated decisions with at least one row with finite positive cF0 and cE; the others get u = 0.5 (same as rf_core and the library).
- E5_N scales cF0 / f^2 with f = m (1 + A (2u - 1)), m and A from the family's own ratio of the same run set; E5 uses 1.1029 and 0.05.
- Intervals: numpy percentiles (2.5/97.5 and 5/95) over finite resamples. R intervals use all 20,000 resamples (pp = denE/201; decision-equivalents = dec_eq(denE_b, n_b) with n_b the resample's decision count); shares use resamples with denE > 0.
- "No binding F0 constraint" = evaluated decision with no row of finite positive cF0 (the stored critical scale is inf or non-positive in every row). "Some row unsafe at 3 s" = any of the 17 rows with clean clearance <= 0.
- Tuning-only sets: vehicle 20, pedestrian 20; all-stored sets: vehicle 22, pedestrian 51. Lead braking reference: 20 tuning runs.

**Result:** see `STEP0_COMPARE_v01.json`. No bug found in the recount; no change made after seeing the first program's numbers.
