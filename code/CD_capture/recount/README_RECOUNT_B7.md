# Recount (second program): B7, rate × latency (package CD, v13)

Written 20 Nov 2026 by a subagent on Claude Fable 5.2 (the first program's writer is Claude Opus 5.5), before either stage of Lock 2
and before any value of a fresh run existed. Program: `rc_b7_v13.py` (this folder). It uses this recount's own core
(`rc_core_v13.py`, `rc_kern_v13.py`: selection paths, gridless curves, numba kernel, estimated phase, percentile intervals).

**Scope.** B7 only (coordinator decision of 20 Nov 2026: Table III on fresh runs, all `B.<x>.*` keys and `B.ca_window`, is package
B's). No `B.<x>.*` key is written; the program refuses to write a key that does not start with `B7.`.
An earlier draft that also covered Table III is kept, unused, as `superseded_rc_trackers_v13.py.txt` (its README:
`superseded_README_RECOUNT_TRK.md.txt`; its old-run test outputs: `out\superseded_trk\`). It is not part of the recount.

## Independence
- Not opened: any `.py` under `CD_capture\analysis\` or `CD_capture\tools\` (in particular `c_trackers_v13.py`, `c_b7_v13.py`,
  `x_trk_extract_v13.py`), `cd_common_v13.py`, `gl_fast_v13.py`, the shared library's `trk_score_v01.py`, any E or F output.
- Read: A10 (§0, §2, §3, §4, §5, §10), `CD_DEFINITIONS_v13.md`, `CD_DEFINITIONS_TRK_v13.md` (first the file of 20 Nov 02:14 EST, then
  its B7-only revision of 02:45 EST, which this program follows), `BRIEF_COMMON_v13.md`, `A_KEYS_CD_v13.json`, A's interface (§2, §4 lines on B7),
  `README_COORDINATION.md` (two-stage lock), package B's definitions (`B_ANALYSIS_DEFINITIONS_v01.md`, `B_FRESH_DEFINITIONS_v02.md`),
  package B's recount (`B_retrack\recount\rc_core.py`, `b_variants.py`, README; another model's work), the lag and load lines of
  `B_retrack\code\b_analysis_v01.py` (method of record), the README and constants of `shared\trackers\`.
- Shared with the first program (A10 §10.1(b)): the extracted arrays (fresh: `arrays\CV0`, `arrays\B7_*`; old-run test: the first
  program's `analysis\out\testold_b7_arrays\B7_<r>_<L>\p1b_fit_finite_0037.npz`, data files only), the B7 detection files, the
  resample draw. The scoring library
  of record (`optA_lib_v02`, v12's `a9_common_v01`) is used only for a full-sample cross-check of every chain
  (`details.B7.<key>.library_of_record.max_abs_diff`) and for `dec_eq` / `ratio`.
- No fresh file was opened. One slip to record: a directory listing of `CD_capture\b7\` printed the names of the fresh-run folders
  there (names only; nothing inside them was listed, opened or read). The old run's folder `b7\p1b_fit_finite_0037\` was read (allowed).

## Gate
Fresh mode refuses unless **both** `revision_v13\LOCK_A10_2.txt` (stage 1) and `revision_v13\LOCK_A10_2c.txt` (stage 2) exist,
because B7 is a stage-2 addition. Every function that opens a fresh array or log calls the same gate first. Fresh arrays that
appear on disk after stage 1 stay unopened until stage 2.

## What it computes
Run set: the lead-braking runs found in `arrays\CV0\` (`pc13_*.npz`, meta family `lead_braking`, no lead variant), ascending run
id. It must equal the lead-braking cases of `CASES_C_v13.json` (a difference is accepted only if `REPLACEMENTS_C_v13.json` lists
replacements; it lists none on 20 Nov), and must count 105.
Every chain must have a file for each of these runs, and its `k`, `idx55`, `evaluated` and cleaned clearance must equal the CV0
file's (else the program stops). The truth phase of every chain is the CV0 file's `phase`.

Per chain (r, L) ∈ {(2,0), (2,0.1), (5,0), (5,0.1), (5,0.2), (10,0), (10,0.1), (10,0.2)}, arrays `arrays\B7_<r>_<L>\<rid>.npz`,
on the chain's own room (F0 = `cF0`, E = `cE`, N = `cN`, CK3 = `cCK3`), 3 s commitment, evaluated decisions, gridless step
frontier on 201 levels:
- `B7.<r>.<L>.R`: R_gl in pp, all decisions.
- `B7.<r>.<L>.as_room`: R_gl in decision-equivalents in the truth-phase-2 population, on its own frontier (`.as_room.pp` beside).
- `B7.<r>.<L>.RR_N`, `.RR_N.ci` (+ `.level` 0.95, `.cal` "nominal95"): RR_gl(N), all decisions.
- `B7.<r>.<L>.RR_CK3`: RR_gl(CK3), all decisions (interval only with `--ck3-ci`, in details).
- `B7.<r>.<L>.lag`: median of the chain's `dx_pred3` over evaluated truth-phase-2 decisions with the chain's `lead_found` and
  0 ≤ now − t_stop < 1, t_stop = `now` of the run's first truth-phase-2 decision (any decision); finite values pooled over runs.
- `B7.ratio_10_2` = as_room(10, 0.1) / as_room(2, 0); `B7.rule_rate` = "consequence" if as_room(10, 0.1) < 0.5 · as_room(2, 0),
  else "holds"; `B7.rule_N` = "qualified" if any chain's RR_N interval is not inside (−0.05, 0.05), "holds" if all eight are inside.
- `B7.identity`: recomputed here, per run, from the logged `runs\<rid>\<rid>\capture\<case>\detections.jsonl` and
  `b7\<rid>\b7_detections_v13.jsonl`: every logged row has a B7 row with the same k, equal `combined_hash`, equal box count, and
  every component of translation and size within 1e-6 m. "pass" only if every run passes.
- Details: populations (n, D, shares), room by the chain's estimated phase, margin-ratio summary, R interval, lag n and quartiles,
  resamples dropped (D(E) ≤ 0), the lead track's state age (median, q90, max), decisions whose own phase differs from CV0's, and for `B7_2_0` the largest difference of each
  critical-scale array from the CV0 array.

Intervals: nominal 95% percentile over the finite resamples; draw `default_rng(20261911).integers(0, 105, (20000, 105))` as counts
per run, runs in ascending id, one draw for every chain. Per-resample `denE, n, D_N` are saved in `out\RC_B7_v13<tag>_boot_<folder>.npz`
for a row-by-row comparison.

## How to run (after both locks)
```
set OPENBLAS_CORETYPE=Haswell
.venv\Scripts\python.exe -I -B -X utf8 recount\rc_b7_v13.py                                  -> out\RC_B7_v13.json
... rc_b7_v13.py --only B7_2_0,B7_2_0.1 --tag _p1        (pieces, any split; then)
... rc_b7_v13.py --combine _p1,_p2,_p3 --tag _all         (merges the pieces; rules and identity)
```
Two threads. Expected time for 105 runs and 20,000 resamples on the shared laptop: roughly 10–15 minutes per chain (extrapolated
from the old-run test; not measured on 105 runs), about 2 hours in all. Outputs are never overwritten (use a new `--tag`).

## Tests on old runs
See "Test results" at the end.

## Disagreements with, and remarks on, the writer's specification (`CD_DEFINITIONS_TRK_v13.md`, B7 sections)
None that changes a value. Remarks:
1. **Key list.** `A_KEYS_CD_v13.json` holds no `B7.ratio_10_2`, `B7.rule_rate`, `B7.rule_N`, `B7.<r>.<L>.as_room.pp`; A's interface
   text names the first three. They are written under the specification's names and listed in `details.keys_beyond_A_KEYS_CD_v13`.
2. **`as_room` unit.** Decision-equivalents, as the key list says; A's interface §4 still says "(pp)". Same reading as the writer.
3. **Families.** A10 B7 says "fresh runs' kept sweeps, both families"; the specification and A's keys cover the lead-braking runs
   only (after-stop room and lag are lead-braking quantities). This program follows the specification. A departure from A10's
   wording that the coordinator may want in Table S4.
4. **Identity tolerance.** A10: "boxes within 1e-6 m". The specification applies it to translation and size; so does this program.
   The stricter all-component result (velocity, rotation, score, class) is in `details.B7_identity` for information.
5. **Identity with missing files.** The specification says "pass if every run passes". If a run has no B7 file or no logged file
   and no checked run fails, this program writes `null` (not "pass") and lists the runs; any failing run gives "fail".
6. **`B7.rule_N` with missing chains.** "qualified" if any available interval leaves the band; "holds" only if all eight intervals
   exist and are inside; otherwise `null`. The specification does not say what a missing chain gives.
7. **Lag clock.** Method of record (`now`, plain comparison, `lead_found`), as the specification. The tick-clock reading
   (k − k_stop in 0..19) is printed beside as a diagnostic (`details.B7.<key>.lag.tick_clock`).
8. **Lock.** The specification names only `LOCK_A10_2.txt`; this program also requires `LOCK_A10_2c.txt` (coordinator's two-stage
   lock).
9. **Old-run test.** The revised specification (§1, §6) defines the old-run test as run `p1b_fit_finite_0037` alone, but names neither
   the folder of its B7 arrays nor its reference CV0 array. This program reads the arrays the first program's extraction wrote to
   `analysis\out\testold_b7_arrays\`, and takes package B's old CV0 array of that run
   (`B_retrack\out\retrack\CV0\p1b_fit_finite_0037_arrays.npz`) as the reference (truth phase, consistency check). If the first
   program uses another reference file, the two should still agree, since CV0's old arrays equal the record (B0(b)).
10. **Populations.** The revised specification scores two populations (all; truth phase 2). This program also prints the room by
   the chain's estimated phase in details; no key depends on it.

## Not done
- The fresh path has not run; only its refusal was tested. The fresh loaders (`fresh_cv0_lead`, `load_fresh_folder`,
  `fresh_capture_dir`) and `--combine` are therefore untested on real files; their format assumptions are those of the
  specification (§1–2) and `CD_DEFINITIONS_v13.md` (meta keys `family`, `lead_variant` in the CV0 files).
- No intervals for R per phase, the after-stop room or the lag (not keys).
- No second extraction or re-detection: arrays and B7 detection files are shared, as A10 §10.1(b) allows.

## Test results (20 Nov 2026, old runs only; logs and outputs in `out\`)
1. **Gate.** Without the locks the fresh mode stops at once (`b7_gate_check_log.txt`). In a scratch tree with a stage-1 file only it
   stops on the missing `LOCK_A10_2c.txt`.
2. **Old run `p1b_fit_finite_0037`** (`TESTOLD_RC_B7_v13_v2.json`, log `b7_testold_v2_log.txt`; a pipeline exercise on one run, not
   results). Identity: "pass" (69 logged ticks, each with a B7 row of the same k and the same combined hash; 71 boxes; largest
   difference 0 in translation, size, velocity, rotation and score; no offline 2 Hz row outside the logged ticks). Scores from the
   eight old-run B7 arrays, 271 evaluated decisions, 10 decisions in the lag window; every chain passes the consistency check
   against the CV0 array:

   | Chain | R (pp) | as_room (dec.-eq.) | RR_N | RR_CK3 | lag (m) |
   |---|---|---|---|---|---|
   | 2 Hz, 0 s | 7.3066 | 4.3582 | −0.00025 | 0.3910 | 2.221 |
   | 2 Hz, 0.1 s | 7.8097 | 6.0498 | 0 | 0.4062 | 2.346 |
   | 5 Hz, 0 s | 6.5301 | 1.3085 | 0 | 0.3599 | 0.386 |
   | 5 Hz, 0.1 s | 6.8899 | 2.4925 | 0 | 0.3770 | 0.735 |
   | 5 Hz, 0.2 s | 6.9854 | 3.0448 | 0 | 0.3879 | 1.592 |
   | 10 Hz, 0 s | 6.3502 | 0.9005 | 0 | 0.4258 | −0.096 |
   | 10 Hz, 0.1 s | 6.6274 | 1.7910 | 0 | 0.4047 | 0.118 |
   | 10 Hz, 0.2 s | 6.9487 | 2.7612 | 0 | 0.4230 | 0.534 |

   With one run every resample is the run itself, so each interval is the point twice. These are to be compared key by key with
   the first program's old-run output; I did not open that output.
   (`TESTOLD_RC_B7_v13.json` and `TESTOLD_RC_B7_v13_final.json` are earlier runs of the same test made before the specification
   defined the old-run B7 test; their score keys are null and their stand-in test is the same as below.)
3. **Scoring path on stand-in arrays** (`details.format_test`; not B7 values). The eight chain slots were fed package B's old
   arrays of CV0, B3, B4, B1, B2, B1_d090, B1_d098 and B3 (35 runs, same file format as the B7 arrays). Each slot reproduces package
   B's values of record for that tracker (`B_retrack\out\banalysis\B_<x>_v01.json`): 14 values per slot (decision count, R, after-stop
   room in decision-equivalents and pp, RR_gl(N) and its interval, RR_gl(CK3) and its interval, the R interval, lag and its n), largest
   absolute difference 0 in every slot, on the first 2,000 rows of the draw of record. The full-sample cross-check against the
   library of record (`a9_common_v01` + `optA_lib_v02.eval_scoring`) gives a largest difference of 0 in every slot. The rules ran
   on these stand-ins (ratio 1.364 → "holds"; the AQ stand-in's interval leaves the band → "qualified"), which exercises both branches
   of `B7.rule_N` but says nothing about B7.
4. **Fresh code path, dry run** (`DRYRUN_RC_B7_v13_q1/_q2/_qall.json`, `b7_dryrun2_log.txt`): a scratch tree outside the project
   holding the 35 old runs relabelled `pc13_dryrun_lead_*` (CV0 and the eight `B7_<r>_<L>` folders from the same stand-ins, one cut-in
   decoy in `arrays\CV0`, copies of run 0037's two detection files for every run, two files standing for the locks). Two pieces with
   `--only`, then `--combine`: run set 35 (decoy left out), consistency with CV0 passed, the 57 point values equal those of test 3
   exactly, identity "pass" on 35 of 35, 76 keys written, all starting with `B7.`. The first attempt stopped on a NumPy warning
   (inf − inf in the `B7_2_0` versus CV0 diagnostic, turned into an error by `-W error`); fixed with an error-state guard and re-run
   (the first attempt's files are in `out\superseded_b7_dryrun1\`). Time: 10–25 s per chain for 35 runs and 2,000 resamples.
5. Not tested: real fresh files, 105 runs, 20,000 resamples (see "Not done").
6. **Final code** (SHA-256 of `rc_b7_v13.py`: 0a71e93d73a4376f17ebd4e61a8d39c1b90622fa0c4fd41c4ba869466e52b3cd). Tests 1–3 were run on it
   (`TESTOLD_RC_B7_v13_v2.json`, `b7_gate_check_v2_log.txt`). The dry run of test 4 was made just before the last edits (the old-run
   0037 branch, the state-age detail, the stricter replacement check); the fresh path of the final file was re-run in the scratch
   tree on one chain with an empty replacement list (`DRYRUN_RC_B7_v13_r1.json`, `b7_dryrun3_log.txt`): same points as before.
   The stand-in lock files of the scratch tree were deleted after the test.

---

# Addition, 20 Nov 2026 (~03:40–04:10 EST): B7 on the cut-in runs (B7CI)

Coordinator's decision of 03:35 EST (A10's B7 row says "both families"). Same program, `rc_b7_v13.py --family cutin`; it stays
stage-2 code (both locks). Written from the coordinator's message, `CD_DEFINITIONS_v13.md` "C, cut-in" and §8 of
`CD_DEFINITIONS_TRK_v13.md` (file of 03:38 EST), without opening any first program. This closes remark 3 above ("Families").

## What it computes
- **Run set:** the fresh cut-in runs of `CASES_C_v13.json` (`pc13_<case>_native`, ascending), read from `arrays\CV0\` (meta family
  `cutin`, no lead variant; `rc_core_v13.load_fresh_runs`); 105 required.
- **Event tick k_c** per run, from truth, once for all chains: this recount's own `rc_c_cutin_v13.truth_of_run` (first truth tick
  with the primary actor ahead of the ego and within 1.75 m of the lane centre; lane centre = median ego lateral route coordinate), or
  with `--truth-file` the truth file that program writes for the same runs and decisions (`--stage truth`).
- **Population:** the event window = evaluated decisions with −20 ≤ k − k_c ≤ 80 ticks (t − t_c in [−1, +4] s, both ends closed, tick
  clock). Runs without an event have an empty window and stay in the resampled set.
- **Arrays:** `arrays\B7CI_<r>_<L>\<rid>.npz` for the eight chains; `k`, `idx55`, `evaluated` and the cleaned clearance must equal
  the run's CV0 array (else stop). Sources `cF0`, `cE`, `cN`, `cCK3` of the chain; 3 s commitment; gridless frontier on the window.
- **Keys:** `B7CI.<r>.<L>.R` (pp, window), `.RR_N`, `.RR_N.ci`, `.RR_N.level` (0.95), `.RR_N.cal` ("nominal95"), `.RR_CK3`;
  `.as_room` and `.lag` = "not applicable"; `B7CI.identity` (the B7 (i) rule on the cut-in runs' detection files). 65 keys.
  A missing chain gives nulls and a reason in details.
- **Intervals:** `default_rng(20261911).integers(0, 105, (20000, 105))` as counts, cut-in runs in ascending id; percentile 2.5/97.5
  over resamples with D(E) > 0.
- **Details:** events found, runs without an event, window size per run, the all-decisions population, R in decision-equivalents, the
  R interval, the margin-ratio summary over the window decisions, for `B7CI_2_0` the largest difference from the CV0 arrays.
- No `--combine` for this family (run it in one piece; it is short when the window is small).
- Outputs: `out\RC_B7_v13_cutin<tag>.json`, `out\TESTOLD_RC_B7_v13_cutin<tag>.json`.

## Remarks on §8 of the specification
1. **Old-run chain (2, 0).** The specification builds it with the extractor from the logged detection rows and says it must equal the
   logged arrays. This program does not extract; it scores the logged (stored) arrays of the 20 cut-in tuning runs directly.
2. **Reference of the old-run test.** The specification names the first program's `TESTOLD_C_CUTIN_K0_K2_v13.json`; this program
   compares with its own K0/K1 recount (`rc_c_cutin_v13.py --test-old`), as the coordinator asked. I did not open the first program's
   file.
3. **`RR_CK3` on old cut-in runs.** The stored arrays of the cut-in tuning runs hold no CK3 scales, so `B7CI.2.0.RR_CK3` is null in
   the old-run test.
4. **Identity with missing files:** as for the lead family (null if a run lacks files and none fails).

## Tests (old runs only)
See "Test results, cut-in" below.

## Test results, cut-in (20 Nov 2026, old runs only)
1. **Gate** (`out\b7_gate_check_v3_log.txt`): both families refuse without the locks. In the dry run (4) the gate was exercised
   in-process: no lock → refused; stage 1 only → refused; both → ran. No lock-named file was created anywhere.
2. **Old-run test** (`out\TESTOLD_RC_B7_v13_cutin_v1.json`, log `b7ci_testold_v1_log.txt`): chain (2, 0) = the logged arrays of the 20
   cut-in tuning runs. Events in 20 of 20 runs; 1,007 window decisions of 5,420 evaluated. Window: D(E) = 0, R = 0 pp, RR_N
   undefined (null) — every row of every evaluated decision of these runs is 3 s-safe, as package B's B9 and my K0–K2 recount found.
   Equal to `rc_c_cutin_v13.py --test-old` (`RC_C_CUTIN_TESTOLD_b200_o4_i1000_matched.json`): window and all-decisions n, D(E), R
   identical, RR_N undefined in both, same 20 runs, same window count. **This test is weak, because the room is zero.**
3. **Window scoring where there is room** (same file, `details.window_scoring_check_on_lead_runs`; a stand-in, not a cut-in value):
   the same window code on the 35 old lead-braking runs with a stand-in event tick (the first truth-phase-1 decision): 1,650 window
   decisions, R = 15.6376 pp, RR_N = −0.00135; the kernel's D(E), D(N), D(CK3) equal the library of record
   (`a9_common_v01` + `optA_lib_v02.eval_scoring`) on that population exactly (largest difference 0).
4. **Event ticks from the logs** (`out\b7ci_event_tick_check_log.txt`): `ci_event_ticks` without a truth file (the path the fresh run
   uses by default) gives the same 20 event ticks as the stored truth file of the K0–K2 recount.
5. **Fresh cut-in path, dry run** (`out\DRYRUN_RC_B7_v13_cutin_ci1.json`, log `b7ci_dryrun_log.txt`): a scratch tree outside the project
   with the 20 old cut-in tuning runs relabelled (CV0 and seven `B7CI_*` folders, one chain left out on purpose, copies of run 0037's
   detection files, a relabelled truth file). Run set, consistency check, window, the seven chains (zero room, as in 2), the missing
   chain reported with nulls, identity "pass" on 20 of 20, 65 keys, all starting with `B7CI.`.
6. **Lead family unchanged** by the refactoring: `out\TESTOLD_RC_B7_v13_v3.json` (final code) has the same 76 values as
   `TESTOLD_RC_B7_v13_v2.json`, and the stand-in test again reproduces package B's record with difference 0 in all eight slots.
7. Not tested: real fresh cut-in files, 105 runs, 20,000 resamples; `truth_of_run` on fresh run folders (it is the routine of the
   K0–K2 recount, which reads the same folders); a non-zero cut-in room on cut-in data (none exists among old runs).
8. **Final code for FREEZE_CD_2** (both families): SHA-256 of `rc_b7_v13.py` =
   829ebfdd02002e7c168fe2492ef8f1c578a975b6d7cbf860dcf87aa001b77cde (it replaces the hash 0a71e93d… given in test 6 of the lead
   section, which was the lead-only version). Tests 1, 2, 3, 4 and 6 of this section and the lead old-run test `_v3` ran on this
   file; the dry run (5) ran just before the last edit, which changed only the module docstring.
   When the gate check of 03:50 EST ran, stage 1 (`LOCK_A10_2.txt`) already existed and the program stopped on the missing
   `LOCK_A10_2c.txt`, as it must; no fresh file was opened.
