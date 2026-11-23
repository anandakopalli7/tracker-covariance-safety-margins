# Recount of the A10 §5.7 supplement sensitivities on the lead-braking runs ("S57B" keys) and of D2's reaction-and-stop column, revision v13

Written 20 Nov 2026 (01:56–04:00 EST) by a subagent on Claude Fable 5.2 (`claude-fable-5-2`), for `AMENDMENT_10_v13.md` §10.1(b).
The first programs are written by Claude Opus 5.5.

**Status.** All five S57B key groups and the D2 reaction-and-stop column are written and tested on old runs. Nothing of a fresh run
was opened. Both programs are stage-2 programs: their fresh paths refuse unless `revision_v13\LOCK_A10_2.txt` **and**
`revision_v13\LOCK_A10_2c.txt` exist.

## Independence

- Not opened: any `.py` under `CD_capture\analysis\` or `CD_capture\tools\`, their outputs, any fresh-run array, run folder or archive.
- Written from: `AMENDMENT_10_v13.md` (§1, §2, §5.5–5.8, §6, §10.1), `CD_DEFINITIONS_v13.md` (including the note "Superseded 20 Nov
  2026"), the writer's specification `CD_DEFINITIONS_S57B_v13.md` (last re-read: the version of 20 Nov 03:39 EST, 18,684 bytes), A's
  interface (`RESULTS_INTERFACE_v13.md`, `A_KEYS_CD_v13.json`, the table code of `A_text\gen\supp_v13.py`), and the methods of record:
  `optA_lib_v02.py`, `rev_common_v01.py`, `rev_a_signed_gap_v01.py`, `rev_b_truncation_phase_scale_v01.py`,
  `rev_e1_extended_truth_extract_v01.py`, `rev_e2_extended_truth_score_v01.py`, `rev_e3_extended_gap2_v01.py`,
  `rev_e4_gap2_cens_unsafe_v01.py`, `a9_common_v01.py`, `a9_1_placebo_gridless_v01.py`, and their outputs of record.
- Also read: `CD_DEFINITIONS_S57A_v13.md` (the sibling family's specification; no code), the existing second programs
  (`recount\rc_core_v13.py`, `rc_kern_v13.py`, `README_RECOUNT_C.md`; `recount_d\rc_d2_event_table_v13.py`, `rc_d_common_v13.py`),
  `trk_score_v01.py` (three functions), a grep of `B_ANALYSIS_DEFINITIONS_v01.md`.
- **Shared with the first program** (allowed by A10 §10.1(b)): the scoring library of record `optA_lib_v02` (`select_grid`,
  `select_first_safe`, `stats_scored`, `frontier`, `hull_frontier`, `levels_of`, `eval_scoring`, `dec_eq`, `vkey`, `brake_profile`),
  the extracted arrays (`arrays\CV0`, `arrays\B1`, `arrays\RSX`), the resample draws, `rev_common_v01.load_runs` for the old runs, and
  for D2 package B's `trk_arrays_v01` (logs, planner rows, rectangle geometry).
- **Own**: the row statistics of every scoring (`SPrep`: 3 s, signed caution, reaction and stop, 2 m gap), the gridless curves
  (`rc_core_v13.selection_path` / `build_curves`, the recount's own construction), the point path (`curve_points` + `gl_point`), the
  resample kernel (`rc_kern_v13.Problem`), the populations and masks, the bootstrap bookkeeping, the keys; for D2 the extended plan,
  its speed, the truth window, the first-loss tick and the closing speed.
  The first program's gridless path is the library of record `a9_common_v01` (+ `gl_fast_v13`). This program uses it for no key; it is
  called only in `--checks`, to compare.

## Files

| File | What it is |
|---|---|
| `recount\rc_s57b_v13.py` | S57B: all five key groups, the record tests, the checks, the dry run. SHA-256 `30b2ebf9…cb5df7` |
| `recount\README_RECOUNT_S57B.md` | This file |
| `recount\out\TESTOLD_RC_S57B_v13_final.json` | **Old-run values under A's keys** (170 keys of the key list of 03:29, plus `.level`/`.cal`), for the key-by-key comparison. Made by the final program from the two chunk files |
| `recount\out\TESTOLD_RC_S57B_v13_rows_00000_10000.npz`, `…_10000_20000.npz` | The 20,000 resamples it was merged from |
| `recount\out\TESTOLD_RC_S57B_v13.json`, `…_v2.json` | The same merge by earlier program versions (identical values; the first still has `LB.RS.0.75.6.rel(.ci)` in `values`) |
| `recount\out\TESTOLD_RC_S57B_v13_RECORD_final.json` (+ `rc_s57b_record_final_log.txt`) | Values of record of v11/v12 reproduced (final record code). `…_RECORD.json`: the same by the first version |
| `recount\out\TESTOLD_RC_S57B_v13_CHECKS.json` (+ `rc_s57b_checks_log.txt`) | Grid identity and library-of-record checks of the key path |
| `recount\out\DRYRUN_RC_S57B_v13_flag_*.json` | The fresh-run code path on old runs relabelled, with `--dryrun` (marked inside as not fresh data) |
| `recount\out\DRYRUN_RC_S57B_v13_b400.json` | An earlier dry run made the old way (see "Dry run") |
| `recount\out\*_dev*.json`, `*_dev3_rows_*.npz`, logs | Development runs with small bootstraps (kept; outputs are never overwritten) |
| `recount_d\rc_d2_rs_v13.py` | D2 reaction-and-stop column, extended scoring. SHA-256 `0386fdad…a89d67` |
| `recount_d\out\RC_D2_RS_v13_TESTOLD.json` (+ `rc_d2_rs_testold_log.txt`), `…_TESTOLD_dev1.json` | D2 old-run test (35 runs; 4 runs) |
| after stage 2: `recount\out\RC_S57B_v13.json` (+ `RC_S57B_v13_rows_*.npz`), `recount_d\out\RC_D2_RS_v13.json` | The fresh-run recounts |

No existing file of `recount\` or `recount_d\` was edited.

## How to run

Python: `CD_capture\.venv\Scripts\python.exe -I -B -X utf8`, `OPENBLAS_CORETYPE=Haswell`; at most 2 workers.

```
rc_s57b_v13.py --test-old --record [--workers 1]                     values of record (grid, truth phases, draw 20261113)
rc_s57b_v13.py --test-old --checks                                   grid identity + library checks of the key path
rc_s57b_v13.py --test-old [--boot N] [--fam pops,rs,trunc,caps,grid] old-run values under A's keys (draw 20261113)
rc_s57b_v13.py [--fam ...]                                           FRESH runs (draw 20261911); REFUSED before both locks
   --rows LO:HI      evaluate only these rows of the draw and write a chunk file (no value is reported from a chunk)
   --merge           take the resamples from the chunk files (they must tile rows 0..boot-1; --chunk-tag if their tag differs)
   --tag _x          suffix of the output name
rc_s57b_v13.py --make-dryrun FOLDER ; rc_s57b_v13.py --dryrun FOLDER  see "Dry run"
recount_d\rc_d2_rs_v13.py --test-old [--runs N] [--tag T]            D2, old runs
recount_d\rc_d2_rs_v13.py [--logs-root R]                            D2, FRESH; REFUSED before both locks
```

After stage 2 (the arrays `arrays\CV0`, `arrays\B1`, `arrays\RSX` and the run folders `runs\<rid>\` must exist):

```
rc_s57b_v13.py --workers 1 --rows 0:10000        (process 1)
rc_s57b_v13.py --workers 1 --rows 10000:20000    (process 2)
rc_s57b_v13.py --workers 1 --merge               -> recount\out\RC_S57B_v13.json
recount_d\rc_d2_rs_v13.py                        -> recount_d\out\RC_D2_RS_v13.json   (default logs root: CD_capture\runs)
```

Any tiling of rows 0..19999 is allowed. Points are recomputed in every call; only the resample arrays come from the chunks.
`--fam trunc,caps,grid` (points only) takes about a minute on 35 runs.

## Gate

- `rc_s57b_v13.py`: `require_stage2` needs both lock files under the root fixed by the file's own location. The program refuses to
  start if `RC_ARS_TRIAL`, `RC_DRYRUN` or `RC_PROGRAMME_A` is set, and if `rc_core_v13` points at another root.
- `rc_d2_rs_v13.py`: the same two files, checked before anything is imported.
- Tested: every fresh entry point prints `REFUSED` (no lock exists); with the environment override set it prints `REFUSED`.

## Dry run (changed on the CD lead's rule of 20 Nov)

- `--make-dryrun FOLDER` writes, outside the project, `CASES_DRYRUN.json` and `arrays\CV0`, `arrays\B1`, `arrays\RSX` from OLD runs
  relabelled. It writes **no lock-like file**.
- `--dryrun FOLDER` runs the fresh-run code path on that folder: the gate is bypassed by this flag by name, the output is named
  `DRYRUN_*` and says so inside, and every path is checked to lie under FOLDER and not under the project (in particular not under
  `CD_capture\arrays` or `runs`; tested: pointing it at `CD_capture` is refused).
- **What happened before the rule.** My first version built a scratch tree with a placeholder `revision_v13\LOCK_A10_2.txt`
  ("this is NOT LOCK_A10_2") and ran with `RC_ARS_TRIAL` / `RC_DRYRUN` (the mechanism of the existing `dryrun_fresh_path_v13.py`).
  One output came from it: `DRYRUN_RC_S57B_v13_b400.json`. I deleted that placeholder and its whole tree
  (`…\scratchpad\dry_s57b`), removed the mechanism from the code and replaced it by the flag. No `LOCK_A10_2c.txt` was ever written.
- **Not mine, left in place:** the shared scratchpad holds other sessions' trees with such placeholders:
  `scratchpad\dry\revision_v13\LOCK_A10_2.txt`, `scratchpad\dry\revision_v13\LOCK_A10_2c.txt`,
  `scratchpad\dryrun_tree\revision_v13\LOCK_A10_2.txt` (and a file `scratchpad\fake_lock.txt`). I did not create or delete them.
- D2's fresh path has no dry run (it needs run logs, not only arrays).

## Conventions of S57B (all from `CD_DEFINITIONS_S57B_v13.md` unless marked)

- **Output**: BRIEF_COMMON's format, `family` = "S57B". Shares as fractions, R in percentage points (D/201), `den0.dec` in
  decision-equivalents, intervals `[lo, hi]`, `null` where undefined. Every `.ci` has `.level` = 0.95 and `.cal` = "nominal95".
  Only keys of `export\A_KEYS_CD_v13.json` (read at run time) go to `values`; anything else to `details.values_not_in_key_list`
  (now `LB.RS.0.75.6.rel` and `.rel.ci`).
- **Runs**: ascending run id. Bootstrap: `default_rng(seed).integers(0, n, (20000, n))` as counts; seed 20261911 on the fresh runs,
  20261113 (the draw of record) on the old runs. Interval: `np.percentile(x[finite], [2.5, 97.5])`.
- **Frontier**: gridless step frontier for groups 1–4; grid frontier and its convex hull for group 5.
- **Group 1**: populations all, mov (`v0 > 0.5`), pre / brk / stop by CV0's phase estimate (−1.0 m/s²), each on its own frontier.
  Sources N, NA, AM (`cA1`), CK3, Q, TG (`cTG2`), E5 (u once over all evaluated decisions). `RR_IMM` = D(N_IMM)/D(E_IMM) on the IMM's
  own room (B1 arrays), in CV0's populations AND B1's own `evaluated`; differences between the two array sets are counted in
  `details.IMM_arrays`. A population without decisions gives `n_dec` = 0 and `null` elsewhere.
- **Group 2**: scoring "est" on the extended clearance (`clean_clear(clearX_<vkey>) > 0`; old runs: v11 `out\ext`; fresh:
  `arrays\RSX`), caution as the 3 s commitment, all evaluated decisions. `rel` = D_est(E)/D_W1(E) on the same resample, `den0.dec`,
  `RR0_N`, `RR0_CK3`; intervals at 6 m/s² only. `LB.gap2.*`: `clearX > 2` for the wrong go, 3 s clearance − 2 for the caution (rev_e3).
  `details.rs` also holds RR0 of NA, AM, Q, TG (A10 §5.7 "for every source"), the count of censored pairs, den₀'s interval, the
  as-scored (61-frame) values where `clear61` exists, and rev_e4's sensitivity (censored pairs unsafe) for the gap.
- **Group 3**: truth phase of record; `k_stop` = the run's first stored decision with truth phase 2; T: evaluated and (phase ≠ 2 or
  `(k − k_stop)·0.05 < T − 1e-9`); cut5: evaluated and (no `k_stop` or `(k − k_stop)·0.05 + 3 ≤ 5 + 1e-9`). Points.
- **Group 4**: caps: 201 levels `linspace(c0, min(C, cap), 201)`; `null` if cap ≤ c0. Signed caution: the definition of
  `stats_scored(signed=True)` on the gridless frontier. Points.
- **Group 5**: grid of record; P = F0's critical scales / 1.1029²; `RR_NmP` = (D(N) − D(P))/D(E); hull = `hull_frontier` on the grid
  points (the same hull on the gridless points is in `details.grid`). Points.
- **Mine, where the specification is silent** (fixed before any fresh value): a value or interval end that is not finite is `null`;
  the fresh arrays are read from `arrays\RSX`, and from `arrays\S57B` only if `RSX` does not exist (the name in the specification's
  first version); the IMM-own-phase sensitivity that the specification places in `details` is not computed.

## D2, reaction-and-stop column (`recount_d\rc_d2_rs_v13.py`)

- Keys `D2.<SRC>.<c2|c5>.rs.runs` and `.vclose`, SRC in F0, N, CK3, TG (`cTG2`); `family` = "D2_RS".
- Operating point, wrong go, ties and medians exactly as `rc_d2_event_table_v13.py` (its `nondominated`, `operating_point`,
  `old_dirs`, `fresh_dirs` are imported), with the safe set `clean_clear(clearX_t0p75_a6p0) > 0`.
- Plan: the row until tick 15, then the stop of record from the row's `v[15]`, `a[14]` (`optA_lib_v02.brake_profile`, as rev_e1),
  followed to J = max(60, ceil(t_end/0.05 − 1e-9)), capped by the frames the recording holds. Speed: the row's up to tick 15, then
  the derivative of the stop profile, 0 from the stop on. Truth: true frames only, each actor up to its first missing frame.
- First loss: the first tick in 0..J with distance ≤ 0; several actors at one tick: the first in the truth's order. Closing speed:
  plan speed minus the actor's truth velocity at that tick along the ego heading of the decision tick.
- Identity anchor in every run: for each wrong-go pair the smallest distance found here must equal the arrays' `clearX` within 1e-9;
  otherwise the program stops after writing.

## Disagreements with the writer's specification

None in a definition: every key follows `CD_DEFINITIONS_S57B_v13.md`, and that file agrees with A10 and the methods of record
wherever those speak. Points to know:

1. **Key list.** The specification's first version listed 172 keys; the key list of 03:29 dropped `LB.RS.0.75.6.rel` and `.rel.ci`
   (A maps them to package B's `LB.RS075.rel`). I follow the 03:40 revision: both are computed and kept in `details`.
2. **Which clearance.** The specification's first version left the reaction-and-stop clearance as an open choice (O2) and the
   sibling specification S57A used the 61-frame clearance. A10 §1 ("judged until the stop ends") decides it; the CD lead settled it
   the same way. On the old runs the two differ little at 0.75 s, 6 m/s² (gridless `rel` 0.1210 extended, 0.1197 as scored).
3. **A10 §5.7 "RR₀ for every source".** The key list has N and CK3 only; the others are in my `details`, not in `values`.
4. **cut5 and the caps** have no method of record; the specification's rules (O3, O4) are definitions of the writer, followed as
   written.
5. **D2.** `CD_DEFINITIONS_v13.md` "D2" still names `trk_score_v01.stop_profile_cont` and "the first of the 61 ticks"; the
   superseding note replaces both for the reaction-and-stop column. I used rev_e1's trajectory; on the old runs it reproduces
   `clearX` exactly.

## Tests (old runs only)

| Test | Result | Output |
|---|---|---|
| Values of record of v11/v12, conventions of record (grid unless the record is gridless, truth phases, draw 20261113, 20,000 resamples): A9-1 grid placebo and gridless populations (points; intervals on the first 2,000 rows), Option A hull, A9-7 TG, rev_b truncation (points and intervals), rev_a signed caution, rev_e2 extended reaction and stop at all 9 settings (points; intervals where the record has them), rev_e3, rev_e4 and rev_a R17 for the 2 m gap | **325 values compared, 0 differ; largest difference 1.78e-15** | `TESTOLD_RC_S57B_v13_RECORD_final.json` |
| Grid identity: every gridless curve of the key path read at the 202 grid scales against the library's grid tables (W1 populations, IMM, truncation, cut5, signed, est at three settings, gap 2, gap 2 with censored pairs unsafe) | 10 of 10 pass: counts exact, caution sums within 2.5e-10 | `TESTOLD_RC_S57B_v13_CHECKS.json` |
| Library of record (`a9_common_v01.gridless_sources` + `eval_scoring`) against the own point path, same cases except signed | 9 of 9 **identical** (106 values, largest difference 0) | same file |
| Kernel at unit weights against the own point path, in every run of the key path | identical (16 of 16 problems) | `details.kernel_vs_point_path` of each output |
| Chunks: rows 0:150 + 150:400 merged against 400 rows unsplit | 286 values, 0 differ | `…_dev2.json`, `…_dev3.json` |
| Fresh path by `--dryrun` (old runs relabelled; loaders of CV0, B1, RSX): all groups at 400 rows; `rs` alone; points alone | 0 values differ from the old-run path | `DRYRUN_RC_S57B_v13_flag_b400.json`, `…_flag_rs400.json`, `…_flag_points*.json` |
| Old-run values under A's keys, 20,000 resamples of the draw of record | written: 170 keys, none null | `TESTOLD_RC_S57B_v13_final.json` |
| D2, 35 old runs, v11 `out\ext` | ran in 56 s. Identity anchor: **227 wrong-go pairs, largest difference 0**; no wrong go without a loss tick; 1 pair loses clearance after tick 60; 4 pairs censored | `recount_d\out\RC_D2_RS_v13_TESTOLD.json` |

Not tested: a comparison with the first program's old-run output (I did not open it; that is the comparison step), and D2's
fresh-run loaders (`rc_d_common_v13.fresh_run`, `fresh_dirs`, `arrays\RSX`), which nothing can exercise before stage 2.
There is no value of record for cut5, the caps, the gridless versions of groups 2–4, E5 and IMM by population, or D2's extended
column: for those the tests above check the construction, not a number.

## Run time (loaded laptop)

- S57B, 35 old runs: 10,000 resamples took 42 min per process with two processes of one thread; merge about 1 min.
- Fresh runs (105): expect about three times that, about 2 h for the two chunk processes side by side. More chunks on more cores
  divide it; the program needs the project tree (it cannot run on a pod as it is).
- Record tests 11–22 min; checks 2–4 min; D2 on 35 old runs about 1 min (5 min when the laptop was busiest).

## Not done

- The IMM-own-phase sensitivity (details only in the specification).
- A pod path for the S57B bootstrap.
- A dry run of D2's fresh path.
