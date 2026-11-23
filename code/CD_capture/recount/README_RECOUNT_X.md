# Recount of the crossing sprint X (A11, pedestrian crossing), revision v13

Written 21 Nov 2026 by Claude Sonnet 5.5 (`claude-sonnet-5-5`), second program for A11 section 3 / A10 section 10.1(b).

**Read:** `crossing\CD_DEFINITIONS_X_v13.md`, `CD_DEFINITIONS_v13.md`, `AMENDMENT_11_v13.md` (section 3, as built), `AMENDMENT_10_v13.md` (via the earlier recount), `crossing\CASES_X_PC_v13.json` (structure only). **Not opened:** `x_cross_v13.py`, `x_extract_v13.py`, `crossing\out\`, anything under `analysis\` or `tools\`, the forbidden paths. No fresh crossing array exists or was looked for.

**Shared (allowed):** `optA_lib_v02` (`boot_counts`, `dec_eq`, `ratio`; full-sample cross-check through `a9_common_v01` + `eval_scoring`, never the source of a value); the earlier recount's `rc_core_v13` and `rc_kern_v13` (own gridless curves, numba kernel, E5 family, percentile intervals, double bootstrap, H3 classification), imported unchanged. **Own (new):** `rc_x_cross_v13.py`, `rc_x_kern_v13.py` (statistic group `XStat`, registered as kind `cross`), `rc_x_calib_remote_v13.py` (the pod runner of the C recount plus one import).

## Run
From `recount\`, `..\.venv\Scripts\python.exe -I -B -X utf8` (env OPENBLAS_CORETYPE=Haswell, NUMBA_NUM_THREADS=2 and BelowNormal priority are set by the program):
- Old runs: `rc_x_cross_v13.py --family pedestrian_crossing --test-old --intervals nominal95 [--nboot 2000]` -> `out\TESTOLD_RC_X_CROSS_pedestrian_crossing_v13[_b<nboot>].json`.
- Fresh (needs `revision_v13\LOCK_A11.txt`; refuses before it, tested): `--n 390 --cases-sha 58902be5ce022b314148308140cb8fc9373bc7aee401531367d456755409a31e --intervals calibrated` with `--calib inproc` (default), or
  1. `--calib export --workers N` writes `out\calib\rc_x.job.npz`, `.meta.json`, `.state.npz` and `out\RC_X_CROSS_pedestrian_crossing_v13.PENDING.json`;
  2. pods: `python -I -B rc_x_calib_remote_v13.py JOBDIR rc_x --seeds 20261913 20261914 --outer LO:HI --threads 1` (files needed in JOBDIR: `rc_x_calib_remote_v13.py`, `rc_x_kern_v13.py`, `rc_kern_v13.py`, `rc_x.job.npz`, `rc_x.meta.json`);
  3. `--calib import --calib-chunks DIR` -> `out\RC_X_CROSS_pedestrian_crossing_v13.json`.
  `--intervals nominal95` is also allowed in fresh mode. Outputs are never overwritten. Fresh runs refuse reduced sizes.
- Run set: first 390 study positions (reserve false) of `CASES_X_PC_v13.json` (SHA-256 checked), replaced by `crossing\REPLACEMENTS_X_v13.json` only as `{"replacements": {case: reserve case}}`, job ids from field `job` (`pc13x_<case>_native`), ascending run id; arrays `arrays_x\CV0\<job>.npz`, `meta.family` asserted.

## Definition as implemented
Population all evaluated decisions, 3 s commitment, gridless 201-level frontier. E5_N: m, A from the median and (q95-q05)/(2 median) of sqrt(c_F0/c_N) over evaluated decisions and rows with both finite and positive; u = e5_u(F0, E); E5p_N = u permuted within runs (`default_rng(20261915)`, run order). X0: R lower end > 0 and D(E) > 0 in >= 97.5% of the 20,000 resamples. X1: lower ends of RR(E5_N) and RR(E5_N) - RR(E5p_N) both > 0. X2: H3 rule (r = RR(N), c = RR(E5_N), delta 0.05); eff = r/c with interval r_b/c_b at r's level under (a). Calibrated statistics: R_gl, RR_E5N, RR_E5NmP, RR_N (A10 2.6, seeds 20261912/13, 20261914, 20261920; second seed only where needed, as in the C recount). Descriptive, nominal 95%: RR_E5rec, RR_E5recmP (1.1029, 0.05).

## Choices
- Keys: `X.ped.*` as in the coordinator's note (X0/X1/X2, `.confirmed`, `RR_E5N`, `RR_E5NmP`, `RR_E5rec`, `RR_E5recmP`, `RR_N`, `X2.class`, `X2.eff(.ci)`, `R`, `R.dec`, `R.share_pos`, `ratio.*`, `n_runs`, `n_dec`, `tested`); `.ci`/`.level` for every interval statistic. Undefined = null.
- R_gl is kept in resamples without room (only ratios are NaN there), as in the C recount.
- A resample set smaller than 20,000 (`--nboot`) uses the first rows of the same draw; the output name then carries `_b<nboot>` (so the old-run test file is `..._v13_b2000.json`, not the bare name).
- Ratio summary ("barely varies") uses all evaluated decisions and rows with both finite and positive, as the C recount.
- Added 21 Nov ~14:40: keys `n_contact` (meta contact_k >= 0), `n_replaced`, `under_run` (n < 332, fresh only), `RR_N.inside_delta`.

## Tests (old runs only)
- 51 stored pedestrian runs, `--nboot 2000`, nominal95: 13,821 evaluated decisions. Points equal package B's step 0 exactly (max abs diff 0: R_pp, R_deceq, RR.N, RR.E5N, RR.E5rec); full-sample values equal the library of record (a9 + eval_scoring) bit for bit. Output `out\TESTOLD_RC_X_CROSS_pedestrian_crossing_v13_b2000.json`. Class: inconclusive; X0, X1, X2 false (R = 0.0800 pp, interval [-0.058, 0.256], share D(E)>0 0.8925).
- Calibration plumbing (`--nboot 200 --outer 10 --inner 50 --mc 200 --second-seed always`): in-process vs export -> runner in a copied folder (two chunks, both seeds) -> import: all 36 values, levels and per-statistic calibration records equal.
- Not tested: pods, the full-size double bootstrap, fresh sizes (390 runs).
- 21 Nov 14:23 EST (session CD, Claude Opus 5.5): line 17 corrected to the replacement file the program reads (REPLACEMENTS_X_v13.json only); documentation only, no code changed.
