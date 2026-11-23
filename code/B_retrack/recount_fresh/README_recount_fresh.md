# Package B, fresh runs: independent second program (recount_fresh), v13

Written 20 Nov 2026 by the second-program agent (Claude Sonnet 5.5) from `B_FRESH_DEFINITIONS_v02.md`, `B_ANALYSIS_DEFINITIONS_v01.md`,
A10 s2-s3 and s5.7, and the predecessor recount `..\recount\` (rc_core.py, b_variants.py; copied and generalised). The first program
(`code\`, `shared\trackers\`, `CD_capture\analysis\`) was not read. Scoring library `optA_lib_v02.py` imported unchanged (read-only).

## Files
- `rf_core.py`: gridless frontier engine (interval-based, equal to select_grid + stats_scored at every breakpoint; from rc_core), margin
  ratio, E5 ranks and oracle scales, run-set container.
- `recount_fresh.py`: CLI, per-variant computation, combine step.
- `compare_to_predecessor.py`: test-mode comparison with `..\recount\RECOUNT_B_v01.json`.
- `out\`: `part_testold_<name>.json`, `testold_boot_<name>.npz`, `TESTOLD_A_RECOUNT_B.json`, `testold_sensitivities.json`, logs.

## CLI (run with `python -I -B -X utf8 recount_fresh.py ...`; numpy, scipy.stats.rankdata, optA_lib only)
- `--test-old [--variants CV IMM CV2 CA AQ IMM090 IMM098] [--K 2000]`: 35 old runs, draw of record, first K rows. With no `--variants`
  it runs all seven and combines. With a subset, run `--test-old --combine` afterwards.
- `--fresh [--variants ...] [--K n]`: **refuses (exit 1) unless `revision_v13\LOCK_A10_2.txt` exists** (checked in `__main__` and again
  in `setup()`, before any fresh path, CASES or REPLACEMENTS file is touched; tested now: "REFUSED"). Writes `out\part_fresh_<name>.json`
  and `out\boot_<name>.npz`; `--fresh --combine` writes `B_retrack\out\A_RECOUNT_B.json` and `out\fresh_sensitivities.json`. Default K = 20000.
- Fresh run ids: lead_braking cases of `CASES_C_v13.json`, replaced via `REPLACEMENTS_C_v13.json` if present, as `pc13_<case>_native`,
  sorted; must be 105 distinct. **Ambiguity:** the REPLACEMENTS file did not exist when I wrote this and its layout is unknown. The loader
  accepts a dict case -> replacement id (or {"replacement": ...}), a dict with a "replacements" key, or a list of {case|original,
  replacement}; any other layout aborts, and a missing file prints a WARNING and applies no replacements. Read that printed line when running.
- Draw: `default_rng(seed).integers(0, n, (20000, n))[:K]` converted to counts per run in id order (same as `boot_counts`, truncated);
  seeds 20261113 (n = 35) and 20261911 (n = 105).

## Method (every choice)
- Rows are evaluated decisions only; scoring `clean_clear(clear) > 0`, caution on 3 s clearance (as stats_scored).
- Frontier: breakpoints = 0, every distinct critical scale in (0, 1000), 1000, per source; levels and D sums by `eval_scoring` on each
  (re)sampled population. Room pp = denE / 201; decision-equivalents = `dec_eq(denE, n)` = denE / 201 / 100 * n, n of that population.
- Margin ratio sqrt(cF0 / cN) over all evaluated rows with finite positive cF0 and cN ("binding rows" read as such rows, as the
  predecessor did; the spec gives no narrower rule). m = median, q05/q95 = `np.percentile` linear, A = (q95 - q05) / (2m), `within5` =
  share with |ratio / m - 1| <= 0.05, `barely` = within5 >= 0.95.
- E5_x: ranks u_i = (midrank(r_i) - 0.5)/n over evaluated decisions that have rows with finite positive g*_F0 and g*_E (`cF0`, `cE` are
  the critical scales), r_i = median_r sqrt(cF0 / cE); others u = 0.5; f_i = m_x (1 + A_x (2u_i - 1)); oracle scale = cF0 / f_i^2 for
  each row. c_x = RR_gl(E5_x). No permutation (E5p is not in this spec).
- Estimated phase (thr -1.0): stop = lead_found and vhat <= 0.5; brk = lead_found, vhat > 0.5, ahat_long <= -1.0; else pre (NaN compares
  false, so no-track or NaN rows are pre). After-stop = truth phase 2.
- Intervals: percentile [2.5, 97.5] (`optA_lib.pct`, non-finite dropped). R.ci uses all resamples; the shares RR, c, RR - c, RR_CK3 are
  NaN (dropped) in resamples where denE <= 0 (never occurs in test mode: share 1.0). m_x, A_x and u_i stay at full-sample values.
- `class` (spec: H3 wording, delta 0.05): "recovers" if RR.ci lower > 0; else "uninformative variation" if c.ci lower > 0.05; else
  "amplitude-limited" if c.ci lies inside (-0.05, 0.05); else "inconclusive" (strict inequalities, as the A10 H3 text).
- Lag: spec text "median over evaluated truth-phase-2 decisions in the first second after the run's first truth-phase-2 decision (0 <= t -
  t_stop < 1 s, t = `now`) of x's `dx_pred3` (finite values, pooled over runs), with `lead_found`". I take t_stop = `now` at the first
  truth-phase-2 decision among ALL decisions of the run (evaluated or not), t = `now`, finite dx_pred3 and lead_found. **Ambiguities
  probed** (`*_sensitivities.json`): (i) tick clock (k - k_stop) x 0.05 instead of `now`; (ii) t_stop from the first *evaluated* phase-2
  decision. In test mode all seven variants give identical medians for (i), (ii) and the primary (n = 300 each).
- B3/B4 rule: `as_room_below_half` = as_room_x < 0.5 * as_room_CV (decision-equivalents); `ck3_differs` = |RR_CK3_x - RR_CK3_CV| > 0.10;
  `B.rule.outcome` = "depends on filter tuning" if any flag of CV2 or CA is true, else "mechanism persists".
- `n_dec` = evaluated decisions, `n_runs` = runs. Per-resample npz: `denE` (sum over 201 levels, not pp), `n`, `D_N`, `D_E5x`, `D_CK3`.

## Test results (35 old runs, K = 2000, draw of record)
All seven variants run; `out\TESTOLD_A_RECOUNT_B.json` and `out\testold_boot_<name>.npz` written.
Comparison with `..\recount\RECOUNT_B_v01.json` (`compare_to_predecessor.py`): **175 items compared (25 per variant: R, R.dec, RR, c,
RR_CK3, the three intervals as two ends each, m, A, q05, q95, within5, barely, room_pre/brk/stop, as_room, as_room.pp, lag, n_dec, class),
175 agree, maximum relative difference 0.0** (bitwise equal). B3/B4 rule in test mode: both flags false for CV2 and CA, outcome
"mechanism persists" (the predecessor's rule text: "persists with NIS near 2 and with a CA filter", the same outcome).
Not in the predecessor (new here, so not compared): RR_CK3.ci, RR_minus_c and its interval, the per-resample arrays.
Caveat: this program is the predecessor's lineage, so the agreement shows the generalisation and the key names are right, not that the
shared reading of the definitions matches the first program's. The comparison with the first program decides that.

## Timing (test mode, two processes in parallel on this 8-thread machine)
Setup plus stats 30-35 s per variant; resampling 58-158 ms per resample (CA 58, CV2 85, IMM098 88, IMM 124, IMM090 133, AQ 148, CV 158),
about 62-69k distinct breakpoints per source; the cost is dominated by `eval_scoring`. Variant totals 2.3-6.3 min at K = 2000.
**Fresh estimate** (not measured: sealed): about 3x the decisions, so about 3x the breakpoints (about 200k) and about 3x the cost per
resample: roughly 0.17 s (CA) to 0.47 s (CV), i.e. about 2,500 to 7,000 resamples in 20 minutes.
**Plan: K = 2,000 for every variant (about 6-16 min each plus 2-3 min setup), more (2,500-3,000) where time allows. 20,000 is not
feasible in the window** (about 1.3-2.6 h per variant). The run must state the K used; the comparison then checks per-resample arrays row
by row on the first K rows. Memory: the per-run tables are 5 sources x 105 runs x about 200k x 5 x 8 B, about 4 GB per process; free RAM
was only about 0.3 GB at the last check here (16 GB total), so run one variant at a time unless at least 10 GB is free.

## Added 20 Nov: B6 / stop reliance (spec 6b, `LB.*`) and tuning runs (spec 6c, `TU.*`)  [code: `b6tu.py`; CLI flags in `recount_fresh.py`]
- CLI: `--test-old --b6 [--K 2000]`, `--fresh --b6 [--K n]` (lock check as before), `--tu [--K 20000]` (same in both modes, no lock);
  `--combine` merges `part_<mode>_b6.json` and `part_tu.json` into the flat JSON (warns if a part is missing). Per-resample:
  `out\testold_boot_b6.npz` / `boot_b6.npz` (WR, W1, DS = denE sums), `out\boot_tu.npz` (denE, n, D_N, D_NA, D_AM, D_CK3, 20000 rows).
- Terciles: points only (no tercile intervals computed). Realised deceleration by the rule of record (3-D speed norm, t = 0.05 k); old runs'
  truth from the archive capture dirs, fresh runs' from `CD_capture\runs\<rid>\<rid>\capture\*\` (not yet exercised).
- REL: grid frontier on the 202-value grid; levels = `levels_of` of F0's and E's caution curves; at each level the operating point is the first
  (lowest-caution, stable order) point that reached the running minimum of wrong-go under W_R (N and CK3 get F0's g = 0 point prepended, as
  `curves_w`); share = (selected row unsafe under W1 and safe under W_R) / n, averaged over 201 levels. Tie rule is my reading; test agrees to 7e-18.
- Fresh runs: W_R = `clearR075` of the CV0 arrays (sliced to evaluated rows when full length); DS from `out\fresh_b6\clear\<rid>.npz`; tau draw
  checked against the stored tau (the max abs diff is in the sensitivities file).
- TU: runs = names of `A4\dryrun\extract`; cF0, cE, cN, clear, vbar, idx55, des from gateR_rt_v01; cNA, cA1, cCK3, cQ, phase from the A4 extraction;
  estimated phase (thr -1.0) from CV0 retrack arrays matched on k. Gridless primary; grid points kept in `part_tu.json` (sens.grid).
- Test results: B6 vs predecessor RECOUNT_B_v01 and `out\b6\B6_STOP_v01.json`: 43 items, 43 agree (max rel diff 1.0e-11, from summation order in
  the tercile den0; all within 1e-9). REL with v11 extended clearance vs v12 A9-6 `share_safe_only_with_stop`: F0, N, CK3 3 of 3 (diff 7e-18);
  REL with the stop cache (primary) is 0.05827 / 0.05825 / 0.03287. TU grid vs v12 A9-5 `tuning` (all, phase0-2 x n, R_pp, RR N/NA/A1/CK3/Q): 28 of 28.
  Earlier 175 of 175 still agree. Timing: B6 tables ~40 s, bootstrap ~0.19 s/resample with another job running (3 scorings); fresh ~3x, so
  K = 2,000 is about 20 min; TU 20,000 resamples = 9 min.

## Update 20 Nov (after the A10 s1 change): B6 / REL primary scoring judged until the stop ends; second lock
- W_R = clean `clearX_t0p75_a6p0` > 0 (test: `revision_v11\analysis\out\ext`; fresh: `CD_capture\arrays\RSX\<rid>.npz`, with k and evaluated checked
  against the CV0 arrays, abort on mismatch). DS = clean `clear` (extended) of `out\fresh_testold\b6_clear_ext\<run>.npz` (test) /
  `out\fresh_b6\clear\<rid>.npz` (fresh); tau draw checked (test max abs diff reported in sensitivities). REL uses the same W_R.
- The 61-frame stop cache is now a test-mode sensitivity only (`sens.stopcache61`, `sens.REL_stopcache61`, `sens.ds61` = DS with `clear61`).
  Those reproduce the predecessor / B6_STOP values (R_pp, den0) within 1e-11; the primary REL reproduces v12 A9-6 (3 of 3, 7e-18).
- Locks: every `--fresh` path (variants, `--b6`, fresh `--combine`) refuses unless BOTH `LOCK_A10_2.txt` and `LOCK_A10_2c.txt` exist
  (tested: all four invocations REFUSED now); their SHA-256 are printed and stored in each part's `sens.lock_sha256` and in the combined fresh
  JSON under `B.lock_sha256`. `--tu` and `--test-old` are ungated.
