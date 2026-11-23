# Recount of package C (second programs), revision v13

Written 19 Nov 2026 by a subagent on Claude Fable 5.2 (`claude-fable-5-2`), for `AMENDMENT_10_v13.md` §10.1(b).

**Independence.** The programs were written from `AMENDMENT_10_v13.md` (§0, §2, §5.1–5.5, §5.8, §10.1) and `CD_DEFINITIONS_v13.md`. Nothing under `work\CD_capture\analysis\` was opened. No fresh-run array, run folder or archive was opened. The programs refuse to open them until `revision_v13\LOCK_A10_2.txt` exists (tested: all three fresh entry points print `REFUSED`). Everything was developed and tested on old runs only: the 35 old evaluation runs and the 20 cut-in tuning runs, exploratory data of record.

**Read besides the two specifications** (each is cited by them, or is shared code they allow):
- `optA_lib_v02.py`, `a9_common_v01.py`, `rev_common_v01.py`, `trk_score_v01.py`, `trk_arrays_v01.py`, `trk_env_v01.py`, `ol_gateR_core_v01.py`, `olcore_v01.py`, `olcore_rt_v01.py`.
- `rev_d_bootstrap_v01.py` (v11) and `a9_2a_double_bootstrap_mc_v01.py` (v12): CD_DEFINITIONS defines the calibration as "rev_d_bootstrap_v01's method with A10's seeds".
- `a9_3_phase_scale_cv_v02.py` (v12): CD_DEFINITIONS defines the H4 choice as "v12's `triple_choice`".
- Package B's `B_ANALYSIS_DEFINITIONS_v01.md`, decisions D-B9-1 and D-B9-2 of `IMM_AND_VARIANTS_SPEC_v01.md`, and the B9 **outputs** on the tuning runs (`B_retrack\out\b9\`), used to check the event ticks and strata counts. Package B's programs and its recount were not read.
- `work\CD_capture\STATUS.md` and `work\README_COORDINATION.md` (status and rules; no code).

## Files

| File | What it is |
|---|---|
| `rc_core_v13.py` | Shared core: Lock 2 gate, loaders, own gridless event construction, numba kernel for the frontiers of many resamples, E5 family, phase estimate, A10 §2.6 calibration, H3/K2 classification |
| `rc_c_lead_v13.py` | Lead braking: H0–H5, H3 classification, H4 transfer (two bases, three sensitivities), calibrated levels, the sequence, descriptive RR_gl of NA, AM, Q, TG |
| `rc_c_cutin_v13.py` | Cut-in: event tick, window, track-age strata, K0–K2, den₀, K2 classification, calibrated levels, the sequence; per stratum and per second: RR_gl(N), room, den₀, ratio spread |
| `rc_kern_v13.py` | Added 20 Nov 2026. Pure module (numpy and numba only, no project path): the numba kernel, `Problem`, `ratio_arr`, `counts_of` (moved from `rc_core_v13.py`, text unchanged), `_h4_kernel` and the H4 evaluation (moved from `rc_c_lead_v13.py`, text unchanged), the two statistic groups as objects (`LeadStat`, `CutinStat`), job files and `calib_rows`. `rc_core_v13` and `rc_c_lead_v13` import them from here, so the in-process path and the pod path run the same code |
| `rc_calib_remote_v13.py` | Added 20 Nov 2026. Standalone runner of chunks of the double bootstrap (see "Pod path") |
| `test_rc_calib_chunks_v13.py` | Added 20 Nov 2026. Test of export -> runner on chunks -> import against the in-process path, on old runs |
| `test_rc_kernel_v13.py` | Identity test of the kernel against `a9_common_v01.Gridless` + `optA_lib_v02.eval_scoring`, and of the E5 family and phase estimate against `trk_score_v01`, on old runs |
| `test_rc_calibration_v13.py` | Test of the calibration plumbing against a plain transcription of the v11/v12 method, on toy numbers (reads no run) |
| `dryrun_fresh_path_v13.py` | Builds a scratch tree outside the project with OLD runs relabelled, so that the fresh-run code path (loaders, IMM branch) can be exercised before Lock 2 |
| `out\` | Test outputs on old runs (below). After Lock 2: `RC_C_LEAD_v13.json`, `RC_C_CUTIN_v13.json` |

## What is shared with the first programs, and what is not

- **Shared (allowed by A10 §10.1(b)):** the scoring library `optA_lib_v02` (grid selection and statistics for H4; `curves_w`, `levels_of`, `frontier` for H4's design levels; `dec_eq`, `ratio`); the extracted arrays; the resample draws (seeds of A10 §5.8); and, for the cut-in truth, package B's `trk_arrays_v01.load_capture` with `ol_gateR_core_v01` (`decisions`, `match_many`, `Book`).
- **Own:** the gridless construction (selection paths, events, curves); the frontier evaluation of resamples; `e5_u`, the permutation, the oracle scales, the margin-ratio summary; the phase estimate; the H4 triple and single-scale choice and its transfer; the event detector, the track age, the populations; the double bootstrap, the calibration rule, the classifications and the sequences.
- **Library points.** Each program also computes every full-sample gridless value with the library of record (`a9_common_v01.gridless_sources` + `optA_lib_v02.eval_scoring`) and writes both, with an `identical` flag. H4's point is also computed on a Python path with `optA_lib_v02.frontier` and `levels_of`.

## How the kernel stays equal to the library

A single evaluation equals `eval_scoring` on the a9 curves bit for bit, by construction:
- the events are ordered as a9 orders them (run, decision, breakpoint; stable sort by breakpoint); the caution sum is accumulated in that order, then the g = 0 total is added;
- the g = 0 totals of a resample come from the same `numpy.tensordot(weights, T0)` call as a9's;
- the 201 levels use `numpy.linspace`'s arithmetic; `C` is Python's `min(nanmax(cF0), nanmax(cE))`;
- the frontier is the minimum of wrong go over the same set of points with caution ≤ level (the library sorts and takes a running minimum; a minimum does not depend on order). NaN levels and empty populations follow the library's behaviour;
- the 201-term sums are taken by `numpy.sum`.

Two shortcuts, both exact:
- events whose three deltas are zero are dropped (they only repeat a point of the curve);
- for every source except F0 and E, a point's caution is compared with a level through a product with a 1e-12 guard band; whenever that comparison is not certain, the exact quotient is formed. The minimum of wrong go is taken on the counts and divided once.

## Tests on old runs

The laptop was heavily loaded by other sessions during every measurement: in the same period `numpy.cumsum` on a 47,000 × 3 array took about 20 ms. Run times below are therefore upper bounds, useful only relative to each other.

| Test | Result | Output |
|---|---|---|
| Kernel against the library, 35 old evaluation runs: 11 sources (F0, E, N, CK3, E5, E5p, NA, AM, Q, TG, O), 6 populations (all, three estimated phases, truth phase 2, a thinned set), 11 weight vectors (full sample, 8 resamples, 2 single-run vectors) | **792 values compared, 0 differ** (==, bit for bit). Library 60 s, recount 20 s including compilation | `out\TEST_RC_KERNEL_v13_dev2.json` |
| Same, 20 cut-in tuning runs: F0, E, N, O; 3 populations; 9 weight vectors | **135 values compared, 0 differ**. Library 5.5 s, recount 0.2 s | same file |
| An earlier kernel version (no shortcuts), 9 weight vectors | 648 values, 0 differ | `out\TEST_RC_KERNEL_v13_dev1.json` |
| E5 family and phase estimate against `trk_score_v01` (u, permuted u, E5 and E5p scales, ratio summary, phases at three thresholds) | all equal | both files |
| Calibration plumbing against a plain transcription (toy data, 300 × 200) | inner shares, coverage at all 100 levels, calibrated level and Monte Carlo SD equal | `out\TEST_RC_CALIBRATION_v13.json` |
| Lead braking, `--test-old --boot 200 --outer 10 --inner 50 --mc 200 --workers 2` | Ran end to end in 392 s. Full-sample gridless values identical to the library (max difference 0), and equal to v12's `A9_1_PLACEBO_GRIDLESS_v01.json` (R_gl, RR_gl of N, NA, AM, CK3, Q) to every printed digit. H4: the four in-sample shares of the design set equal v12's `A9_3_PHASE_SCALE_CV_v02.json` (differences 0); kernel and library path of the H4 point equal (difference 0) | `out\RC_C_LEAD_TESTOLD_b200_o10_i50.json`, `out\lead_testold_log.txt` |
| Cut-in truth stage, 20 tuning runs | 245 s. Event ticks equal package B's B9 output in 20 of 20 runs | `out\RC_C_CUTIN_TESTOLD_TRUTH_v13.json` |
| Cut-in, `--test-old --truth-file … --boot 200 --outer 10 --inner 50 --mc 200 --workers 2` | 69 s. Window sizes, strata counts and evaluated counts per run equal B9's output; ratio summaries in the window equal B9's to every digit; the 12 populations identical to the library. On these runs the room in the window is zero and no decision is in the young-track stratum, so K0–K2 are degenerate there (as B9 reported) | `out\RC_C_CUTIN_TESTOLD_b200_o10_i50.json` |
| Dry run of the fresh-run path (old runs relabelled in a scratch tree; B1 stand-in = the same runs with cN := cNA) | Both programs ran end to end through the fresh-run loaders (lead 308 s, cut-in 186 s). Lead: 84 points, interval ends, coverages and levels compared with the `--test-old` output, 0 differ; the IMM branch (H3 classification, ceiling, r/c) ran, and its full-sample values are identical to the library. Cut-in: counts equal the `--test-old` output | `out\DRYRUN_*.json` (marked inside as not fresh data) |

**Run times measured (loaded laptop, 2 threads, 35 old runs, about 47,000 curve points per source).**
- Compilation of the kernel: 16–95 s on first use; cached afterwards (`__pycache__` in this folder).
- H4 design (four variants): 37 s. Curves of 10 sources: 35 s. Library points of 10 sources: about 240 s.
- Main bootstrap: 0.10 s per resample for 10 gridless sources plus H4 (20,000 resamples: about 35 min at that rate).
- Double bootstrap: 0.054 s per inner resample for 6 gridless sources plus H4. At that rate 2,000 × 1,000 would take about 30 h per inner seed on this laptop for 35 runs, and about three times more for 105 runs with the IMM group. It has to run on a many-core, unloaded machine: the cost is linear in the number of curve points and divides by the thread count (`--workers`). See "Pod path" for the split and a later single-thread measurement.

## Pod path of the double bootstrap (added 20 Nov 2026)

The double bootstrap is split off so that it can run in parallel chunks on Linux machines. Nothing under `work\CD_capture\analysis\` or `work\CD_capture\tools\` was opened for this. Every Lock 2 gate is unchanged: `--calib export` and `--calib import` on fresh runs print `REFUSED` before Lock 2 (tested).

1. **Export** (laptop; everything except the double bootstrap):
   - `rc_c_lead_v13.py --calib export --workers N` -> label `rc_lead`
   - `rc_c_cutin_v13.py --truth-file out\RC_C_CUTIN_TRUTH_v13.json --calib export --workers N` -> label `rc_cutin`
   - Each writes `out\calib\<label>.job.npz` (every array the runner needs; `numpy.load(..., allow_pickle=False)`), `out\calib\<label>.meta.json` (`n_outer`, `n_inner`, `n_run`, `pod_seeds` = [20261913, 20261914], `job_sha256`, the statistics, the runner's files and call), `out\calib\<label>.state.npz` (the main-bootstrap results, reused by import; it stays on the laptop) and a pending output `out\<output name>.PENDING.json` (points and main bootstrap; marked `PENDING`; no level, interval or hypothesis).
   - With `--test-old` the folder is `out\calib_testold\`; in a dry run `out\calib_dryrun\`. Jobs are never overwritten; `--calib-label rc_...` gives another label.
   - The job holds one statistic group per program (choice 5 below): for lead, the online-tracker problem, the IMM problem and H4 together.
2. **Runner** (pod; one process per call, one thread):
   `python -I -B rc_calib_remote_v13.py JOBDIR LABEL --seeds SEED --outer LO:HI --threads 1`
   - **Files it needs in JOBDIR:** `rc_calib_remote_v13.py`, `rc_kern_v13.py`, `<label>.job.npz`, `<label>.meta.json`. Nothing else; CPython 3.12, numpy 2.5.4, numba 0.68.1. It runs from any working directory and holds no absolute path.
   - It writes `JOBDIR/<LABEL>_<SEED>_o<LO>_<HI>.npz`, first as `...npz.tmp<pid>`, then by rename. An existing chunk is not computed again.
   - The chunk holds rows LO..HI-1 of an unsplit run: the outer draw is the full draw `default_rng(20261912).integers(0, n, (2000, n))`; the inner draws of outer samples 0..LO-1 are generated and discarded; the outer estimates are rows of the job's `outer_est`, which export computed with the same call as an in-process run. It records label, seed, lo, hi, n_outer, n_inner, the job file's SHA-256, its run time and the versions.
   - numba compiles the kernel in each process (10-25 s here) unless its cache is there; it writes the cache to `JOBDIR/__pycache__` (optional).
   - The runner sets `OPENBLAS_CORETYPE=Haswell` if it is not set, and one BLAS thread: the caution sums of a resample come from BLAS products, and another BLAS kernel can change their last bit. The laptop runs with the same setting. A chunk from a machine with another BLAS build could still differ in a last bit from this laptop's; that would move a share only if an inner value fell within one rounding of the full-sample value. This was not tested on Linux.
3. **Import** (laptop): the same command as export with `--calib import --calib-chunks DIR` in place of `--calib export` (DIR = the folder with the chunk files; the job stays in `out\calib\`).
   - The job must be the job of this run: every array of the job is formed again from the data and compared; the job file must have the SHA-256 of its meta file.
   - For each inner seed it needs, the chunks must tile 0..n_outer exactly (a gap or an overlap is refused) and each must record this label, seed, range, sizes and job SHA-256, and hold the job's outer estimates.
   - `--second-seed auto` (default): the existing rule decides from seed 20261913 whether seed 20261914 is used; its chunks are read only then. `always` and `never` work as before.
   - The output has the name and the content of an in-process run, plus `calib_mode` and `calib_import` (job SHA-256, chunk names, summed run time).
4. The in-process path (`--calib inproc`, the default) is unchanged.

**Time measured** (old lead job, 35 runs, 16 statistics, 1,000 inner resamples, one thread, loaded laptop, an upper bound): **10.6 s per outer sample** after the first; the first took 11.0 s including compilation. 2,000 outer samples are then about 5.9 CPU-hours per inner seed for 35 runs; for the 105 fresh runs with the IMM group expect several times that (the cost is linear in the number of curve points). Generating and discarding the inner draws of earlier outer samples is a small cost per chunk. Job size: 1.8 MB (lead, old runs).

**Test** (`test_rc_calib_chunks_v13.py`, old runs, `--test-old --boot 200 --outer 12 --inner 50 --mc 200`; record `out\TEST_RC_CALIB_CHUNKS_v13.json`, log `out\test_rc_calib_chunks_log.txt`):

| Check | Result |
|---|---|
| Lead: in-process output against export -> chunks 0:5 and 5:12 for both seeds (four processes, run from another folder) -> import | **5,600 values compared, 0 differ**. The second seed was needed (`RR_E5p`) and used in both |
| Cut-in: the same | **1,461 values compared, 0 differ** (second seed not needed). With `--second-seed always` (run by hand, not in the record): 1,461 compared, 0 differ |
| Chunks against checkpoints written by the programs before this change (`out\ckpt\*_b200_o10_i50*_inner1.npz`, rows 0..9) | lead 840 values, cut-in 360 values, 0 differ; full-sample values equal |
| Standalone: job files, runner and `rc_kern_v13.py` copied to a fresh folder under `%TEMP%`, chunk 5:12 run with `-I -B` from the home folder | equal to the chunk from the project folder (588 values and the header) |
| Refusals of import (run by hand, not in the record) | a missing chunk (gap), an overlapping chunk, and chunks of another job (wrong label) are each refused. A chunk with the right label and a wrong SHA-256 was not tried |
| `test_rc_kernel_v13.py --resamples 8 --cutin` after the move | 792 + 135 values, 0 differ, `ALL IDENTICAL` (`out\TEST_RC_KERNEL_v13_podpath.json`) |
| `test_rc_calibration_v13.py` | `ALL EQUAL` (`out\TEST_RC_CALIBRATION_v13_podpath.json`) |

Not compared between the two outputs: time stamps, run times, thread counts, `calib_mode`, `calib_import`. Not tested: a Linux machine (no pod was used), and the fresh-run sizes.

## How to run after Lock 2

All commands from `work\CD_capture\recount\`, with `..\.venv\Scripts\python.exe -I -B -X utf8`.

1. `test_rc_kernel_v13.py --resamples 40 --cutin --workers 4 --tag _postlock` (old runs; must print `ALL IDENTICAL`).
2. `rc_c_lead_v13.py --workers N` writes `out\RC_C_LEAD_v13.json`.
3. `rc_c_cutin_v13.py --stage truth` writes `out\RC_C_CUTIN_TRUTH_v13.json` (event ticks and track ages; needs the run folders). Then `rc_c_cutin_v13.py --truth-file out\RC_C_CUTIN_TRUTH_v13.json --workers N` writes `out\RC_C_CUTIN_v13.json`. Without `--truth-file` the program does both.

Options: `--boot`, `--outer`, `--inner`, `--mc` (defaults 20,000, 2,000, 1,000, 2,000; smaller values use the first rows of the same draws, and the output name then carries the sizes); `--second-seed auto|always|never` (default `auto`: the second inner seed is run only if some statistic's coverage at 95% is below 0.94 and a calibrated level exists); `--no-calibration`; `--no-library`; `--tag`. Outputs are never overwritten. The double bootstrap writes a checkpoint every 25 outer samples to `out\ckpt\` and resumes from it.

**On another machine.** Set `RC_ARS_TRIAL` and `RC_PROGRAMME_A` to copies that keep the folder layout of:
- `revision_v13\LOCK_A10_2.txt`, `revision_v13\work\CD_capture\{CASES_C_v13.json, arrays\}`;
- `revision_v11\analysis\rev_common_v01.py`; `revision_v12\analysis\{a9_common_v01.py, out\lead, out\tg, out\A9_3_PHASE_SCALE_CV_v02.json}`;
- under Programme A: `11_ojits\{A6R\code, A6R\run, A4\fit, review\optionA_recount_v01\cache}` and `09_redesign\m2_decisions\openloop\gateR_rt_v01` (the old runs are H4's design set).

For the double bootstrap alone none of this is needed: see "Pod path". `rev_common_v01.py` and `a9_common_v01.py` hold absolute paths. If they cannot be imported there, the old-run loader fails and H4 cannot be designed; this was not solved here. The identity test should be repeated on that machine, because a different BLAS can change the last bit of `tensordot`.

## Choices where A10 and CD_DEFINITIONS were silent or unclear

**None was made after seeing a fresh value.** Where an alternative reading is cheap, the output JSON carries it beside the value used.

### Calibration (A10 §2.6)
1. **Tolerance and valid samples.** CD_DEFINITIONS gives the coverage rule as "share(inner ≤ full) ≥ (1−ℓ)/2 and share(inner < full) ≤ 1 − (1−ℓ)/2" and names `rev_d_bootstrap_v01`'s method. That program adds three things the text does not state, and I follow all three: a tolerance of 1e-12 on both comparisons; inner shares over the **finite** inner values only; an outer sample counts only if its own estimate is finite and it has at least one finite inner value. The tolerance matters: (1 − 0.95)/2 is 0.025000000000000022 in floating point, so a share of exactly 25/1000 passes only with the tolerance. The JSON also gives the coverage without tolerance and with every outer sample (`coverage_95_no_tolerance`, `coverage_95_any_outer`, and the corresponding levels).
2. **Monte Carlo SD "of the calibrated level".** Taken as in v12's `a9_2a`: in each of 2,000 resamples of the outer samples (`default_rng(20261920).integers(0, B1, (2000, B1))`, drawn once and used for every statistic), the smallest level of the grid with coverage ≥ 0.95; SD with ddof = 1, a resample in which no level reaches 0.95 counting as 1.0 (CD_DEFINITIONS addition of 18:20 EST). The index draw is over all outer samples; validity is applied inside each resample.
3. **Second inner seed "agrees within 0.002".** Its level is the smallest grid level with coverage ≥ 0.95 under seed 20261914, whatever its coverage at 0.95; agreement is |difference| ≤ 0.002 (+1e-12).
4. **No level reaches 0.95, or no valid outer sample.** The nominal 99% interval is used, with the reason in the JSON.
5. **One stream per statistic group.** "2,000 outer × 1,000 inner per statistic group": I restart both generators for a program's statistics and evaluate all of them on the same draws. This equals separate groups only if the first program also restarts the generators for each group. If it lets one inner stream run on across groups, the levels of the later groups can differ.
6. **R_gl in resamples without room.** R_gl = D(E, F0)/201 is kept whenever it is finite, also when it is ≤ 0 (the v11 program sets every statistic to NaN there). The counts of such resamples are written (`n_den_le0_or_nonfinite`, `outer_den_le0`); with none, the two readings agree.
7. **Interval at a calibrated level.** `np.percentile(finite resamples, [100·a/2, 100·(1 − a/2)])`, a = 1 − level (the v11 form); exactly [2.5, 97.5] at 95% and [0.5, 99.5] at 99%.
8. **Which statistics are calibrated.** Lead: R_gl, RR_gl(E5), RR_gl(E5) − RR_gl(E5p), RR_gl(N), RR_gl(CK3), RR_gl(E5p); IMM: its room, r, c, r/c; H4: both bases for the primary and the three sensitivities. Cut-in: R_gl and RR_gl(N) in the window; room, r, c, r/c in the young-track population. Descriptive values carry nominal 95% intervals.

### Lead braking
9. **u for E5.** A10 §2.2 says "(rank of r_i − 0.5) / n over the run set's evaluated decisions … A decision without such rows gets u_i = 0.5". The shared library ranks only the decisions that have a ratio and divides by their number. CD_DEFINITIONS says `u = e5_u(F0, E)`, so I follow the library (my own code, equal to it on the old runs, where every evaluated decision has a ratio).
10. **E5p run order.** "runs in run-id order of the run set": ascending run id as a string.
11. **"Barely varies".** A10 says "≥ 95% of binding rows"; CD_DEFINITIONS says the ratios over "evaluated decisions and rows with both finite and positive". I follow CD_DEFINITIONS (all such rows).
12. **Efficiency r/c.** The ratio of the two shares in each resample; NaN where the room is not positive or c = 0. It is computed and calibrated always, and reported under H3 only for "recovers".
13. **H0's second condition.** The share of the 20,000 main resamples with D_gl(E, F0) > 0; non-finite counts as not > 0.
14. **H4, decisions outside phases 0–2.** With the truth phase, an evaluated decision may have phase 3. The transferred point divides wrong go by all evaluated decisions (CD_DEFINITIONS), so such a decision would count in the denominator and in no phase. Their number is written (`H4_phase_outside_0_1_2_evaluated`; 0 on the old runs).
15. **H4 sums.** `numpy.sum` over the 201 levels (a NaN level makes the value NaN). The transferred frontier always holds F0's g = 0 point, so no NaN arises unless a resample has no decision.
16. **H4, knife edge.** A triple qualifies at a level if its pooled caution is ≤ the level. At the lowest and highest level a triple can equal the level up to rounding of a three-term sum. I form the sums as v12's `triple_choice` does (same order), and the old-run values equal v12's exactly; a first program that sums in another order could differ at such a level.
17. **H3 in `--test-old`.** Skipped (no B1 arrays for old runs); the sequence then runs H0, H1, H2, H4, H5.

### Cut-in
18. **Route frame.** "Lateral route coordinate" of a point = −sin ψ·x + cos ψ·y with ψ the ego's route yaw at that tick; "ahead" = cos ψ·(x_a − x_e) + sin ψ·(y_a − y_e) > 0. With a constant route yaw this is the reading of D-B9-1; on a curved route the lane median would mix frames. The event ticks equal B9's on the 20 tuning runs.
19. **Primary actor** = the truth record's `target` at each tick; ticks without it are skipped.
20. **Track without a birth record** (track id never listed by the detector log): the track is skipped (CD_DEFINITIONS addition), so the decision is untracked unless another matched track has a birth. Counted per run (`n_matched_tracks_without_birth`; 0 on the tuning runs).
21. **Strata bounds.** age < 1; 1 ≤ age < 4; age ≥ 4. Ages carry the float32 noise of the logged times (for example 4.000000059604645), so a track exactly at a bound falls on the upper side.
22. **Seconds relative to t_c.** Bins [−1, 0), [0, 1), [1, 2), [2, 3) and [3, 4] closed (CD_DEFINITIONS addition): decisions at exactly +4 s belong to the last bin.
23. **Resampled set.** All cut-in runs of the set, including runs without an event (they contribute nothing to the window).
24. **K2.** u is ranked over all evaluated decisions of all cut-in runs, including runs without an event. If the young-track population is empty, E5_N is undefined and K2 is "not evaluable".
25. **K0's den₀ and K2's 10-decision-equivalent rule** use point estimates.
26. **Lock file path.** `revision_v13\LOCK_A10_2.txt` (my brief and coordination rule 3). The coordination table also says `locks\` holds it; if it is written only there, the gate path must be changed, which is a change to these programs.
