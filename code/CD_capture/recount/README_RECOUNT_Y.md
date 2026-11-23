# Recount of test Y (A11 section 6b: B2 against its permuted twin), revision v13

Written 21 Nov 2026 by Claude Sonnet 5.5 (`claude-sonnet-5-5`), second program.

**Read:** `AMENDMENT_11_v13.md` (6b, 3.7), `work\CD_capture\ycheck\CD_DEFINITIONS_Y_v13.md` (only file opened under `ycheck\`), `CD_DEFINITIONS_v13.md`, `FREEZE_B_add7.json` (manifest), the earlier recounts' code. **Not opened:** `y_twin_v13.py`, `ycheck\out\`, anything under `analysis\`, `tools\`, `crossing\`, the forbidden paths. No fresh B2 or CV0 array value was loaded (only the member names of one B2 npz were listed, to learn that `des` is in it). Fresh mode was not run.

**Shared (allowed):** `optA_lib_v02` (`boot_counts`, `ratio`; `a9_common_v01` + `eval_scoring` only as a full-sample cross-check); `rc_core_v13` and `rc_kern_v13` imported unchanged (own gridless curves, numba kernel, percentile intervals, A10 2.6 double bootstrap, export/import). **Own (new):** `rc_y_twin_v13.py`, `rc_y_kern_v13.py` (statistic `YStat`, registered as kind `ytwin`), `rc_y_calib_remote_v13.py` (pod runner, the rc_x one with the new kern).

## Run
From `recount\`, `..\.venv\Scripts\python.exe -I -B -X utf8` (OPENBLAS_CORETYPE, NUMBA_NUM_THREADS and BelowNormal priority are set by the program):
- Old runs: `rc_y_twin_v13.py --test-old --intervals nominal95 --nboot 2000` -> `out\TESTOLD_RC_Y_TWIN_v13_b2000.json`.
- Fresh (needs `revision_v13\LOCK_A11.txt`): `rc_y_twin_v13.py --intervals calibrated|nominal99|nominal95`, with `--calib inproc` (default), or `--calib export --workers N` (writes `out\calib\rc_y.job.npz`, `.meta.json`, `.state.npz` and a `.PENDING.json`), then on pods `python -I -B rc_y_calib_remote_v13.py JOBDIR rc_y --seeds 20261913 20261914 --outer LO:HI --threads 1` (files in JOBDIR: `rc_y_calib_remote_v13.py`, `rc_y_kern_v13.py`, `rc_kern_v13.py`, `rc_y.job.npz`, `rc_y.meta.json`), then `--calib import --calib-chunks DIR` -> `out\RC_Y_TWIN_v13.json`. Fresh runs refuse reduced sizes. Outputs are never overwritten.
- Fresh order of work: gate; REPLACEMENTS_C empty; SHA-256 of FREEZE_B_add7.json and of all 105 B2 files (size and hash against the manifest) before any value is read; B2 and CV0 `des` and `evaluated` must agree.

## Definition as implemented
Population: evaluated decisions; 3 s commitment (safe iff `clean_clear(clear) > 0`); gridless step frontier (201 levels, on the variant's own F0 and E: B2's cF0/cE for B2, the record's for the reference). f_i = median over the 17 rows with finite positive cF0 and cN of sqrt(cF0/cN) (NaN = no factor). B2s: cF0/f^2 where there is a factor, else cN. B2p_k, k = 1..20: one `default_rng(20261931)`; k outer, runs in ascending id inner; J = evaluated decisions with a factor; `perm = rng.permutation(len(J))`; decision J[j] gets factor f[J[perm[j]]]; crit = cF0/f_pi^2 on J, cN elsewhere. The twins are fixed per run, not redrawn per resample. RR_gl(B2p) = mean over the 20 twins within the resample. Delta = RR_gl(N_B2) - RR_gl(B2p); Delta_s = RR_gl(B2s) - RR_gl(B2p). Resamples: `boot_counts(n, 20000, 20261911)`, runs in ascending id. Delta's interval: percentile at the A10 2.6 level (double bootstrap 2,000 x 1,000, seeds 20261912/13, second 20261914, MC 20261920, as the C recount; second inner seed run when needed), or nominal 99% (emergency rule) or 95%. Descriptive intervals: nominal 95%. Reference: same construction on CV0 (cF0 of record, cN), own `default_rng(20261931)`, same resamples. `Y.Y1` = lower end of Delta's interval > 0. Keys are exactly definitions section 5 (undefined = null).

## Choices (points the definitions leave open)
- A decision's factor is computed for all decisions, but only evaluated decisions with a factor (J) enter the counts and the permutation; `Y.n_factor(_ref)` counts evaluated decisions with a factor.
- "f_pi(J[j]) = f_J[perm[j]]" read as: decision J[j] receives the factor of decision J[perm[j]] (same as `u[ev][perm]` in the earlier permutation code).
- B2 and the reference each use a fresh generator `default_rng(20261931)` (the definitions say so for the reference; for B2 one generator, drawn before any value).
- `Y.R`, `Y.ref.R`: D_gl(E)/201 at the full sample (pp). `Y.share_pos` is over B2's main resamples (the reference's in the old-run test); D_gl(E) <= 0 gives NaN ratios, finite R as in the C recount.
- Calibration statistic is Delta only (job stat `delta`); the main-bootstrap problem includes B2s (23 sources), the calibration problem does not (22 sources: F0, E, N_B2, p01..p20).
- Old-run test: only the reference keys exist (`Y.n_runs`, `Y.n_dec`, `Y.n_factor_ref`, `Y.share_pos`, `Y.ref.*`); `Y.n_factor` is null. With `--intervals calibrated` in `--test-old` the double bootstrap runs on the reference's Delta_N (plumbing test only); the output name then ends in `_calibrated`.
- The old runs are the 35 of `rc_core_v13.load_old_eval_runs` (order of `rev_common_v01.load_runs`), as the earlier recounts.

## Tests (old runs only)
- `--test-old --intervals nominal95 --nboot 2000`: 35 runs, 8,290 evaluated decisions, all with a factor; full-sample values of all 24 sources equal the library of record (`a9` + `eval_scoring`) bit for bit; 3 min 20 s. Output `out\TESTOLD_RC_Y_TWIN_v13_b2000.json`.
- Calibration plumbing (`--nboot 200 --outer 10 --inner 50 --mc 200 --second-seed always`, reference Delta_N): in-process vs export -> runner (copied folder, two chunks, both seeds) -> import: values, levels and calibration records equal. This tiny setting lands on the 99% fallback rule, so the "calibrated level accepted" branch is exercised only by the shared, unchanged `calibrate_stat`.
- Not tested: pods, the full-size double bootstrap, any fresh run (B2 hashes, CV0 loading, the gate).
