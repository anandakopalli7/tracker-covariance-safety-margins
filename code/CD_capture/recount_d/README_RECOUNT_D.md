# Recount of package D (second programs), revision v13

Written 19 Nov 2026 by a separate session on Claude Fable 5.2 (`claude-fable-5-2`), per `AMENDMENT_10_v13.md` §10.1(b).
Sources used: A10 (§0, §2, §5.5, §6, §10.1), `CD_DEFINITIONS_v13.md`, package B's `work\shared\trackers\README.md`.
**Not read:** anything under `work\CD_capture\analysis\`, `arrays\`, `runs\`, `archives\`, any `<excluded folder 1>` or `<excluded folder 2>` folder, `<excluded folder 3>`.
No value of a fresh run was computed or read. Everything below was developed and tested on the 35 old evaluation runs (exploratory data of record).

## Files
| File | What |
|---|---|
| `rc_d_common_v13.py` | Lock 2 gate, loaders (old runs; fresh arrays `arrays\CV0\<run>.npz`), run sets, tracker phase (re-implemented), write-once JSON |
| `rc_d_nonbraking_v13.py` | D1: matched settings, per-variant differences with intervals, D-H1 and D-H2 |
| `rc_d2_event_table_v13.py` | D2: operating points, wrong-go runs, closing speeds |
| `out\` | One JSON per run of a program (never overwritten; `--tag` names a new file) |

Shared with the first programs (allowed by §10.1(b), stated here):
- `optA_lib_v02.py`: `stats_scored`, `select_grid`, `clean_clear`, `boot_counts`, `vkey` (and `curves_w`, `levels_of`, `frontier` in the optional v12 check);
- v11's `rev_common_v01.load_runs` and `GRID`;
- package B's library, in D2 only: `trk_arrays_v01` (`load_capture`, `gc.decisions`, `ox.window_truth`, `oc.rect_corners`, `oc.poly_dist`, `finite_primitive.build_library`, `consumer.Diagnostics`) and `trk_score_v01` (`stop_profile_cont`, `row_state_at`);
- the resample draw `boot_counts(35, 20000, 20261911)`.

Written here independently: the tracker phase, the matched-setting search, the triple rule, the pooled rates, the bootstrap differences, the classification, the non-dominated frontier, the operating-point rule, the first loss of clearance, the reaction-and-stop speed profile, the closing speed and the medians.

## How to run (after `LOCK_A10_2.txt` exists)
Both programs refuse to touch a fresh file unless `revision_v13\LOCK_A10_2.txt` exists. From `work\CD_capture`:
```
.venv\Scripts\python.exe -I -B -X utf8 recount_d\rc_d_nonbraking_v13.py
.venv\Scripts\python.exe -I -B -X utf8 recount_d\rc_d2_event_table_v13.py --logs-root <folder holding <run>\ with SUMMARY.json and the capture>
```
- D1 reads `arrays\CV0\pd13_<case id>_native.npz` for the `d1_openloop` rows of `d1\CASES_D1_v13.json` (35 per `lead_variant.kind`; the meta's `lead_variant` kind is checked). Output: `out\RC_D_NONBRAKING_v13.json`.
- D2 reads `arrays\CV0\pc13_<case>_native.npz` for the 105 lead-braking rows of `CASES_C_v13.json` (meta must have no lead variant) and each run's logs. Output: `out\RC_D2_EVENT_TABLE_v13.json`.
  - **The location of the fresh runs' extracted logs is not stated in A10 or CD_DEFINITIONS, and I did not look.** `--logs-root R` (default `work\CD_capture\archives`) expects `R\<run>\` to contain, at any depth, one `SUMMARY.json` and exactly one folder with `frames.jsonl`, `evaluation_truth.jsonl` and `contract.json`. Otherwise pass both `--run-dir-template` and `--cap-dir-template` (with `{run}` and `{case}`), e.g. `...\{run}` and `...\{run}\x\{run}\capture\{case}`.
- Test mode (old runs only, no lock needed): add `--test-old` (D1: the 35 old runs stand in for a variant; `--check-v12` adds the identity check of the triple rule. D2: 3 s commitment; `--old-rs` adds reaction-and-stop from the v11 cache `t0p75_a6p0`; `--runs N` uses the first N runs).

## What each program computes
### `rc_d_nonbraking_v13.py`
1. **Matched settings** on the 35 old runs, all evaluated decisions, 3 s commitment, grid of record (`[0] + logspace(-2, 3, 201)`):
   - c\* = 100·Σ caution sum / Σ caution count of F0 at g = 1 (grid index 81);
   - N, NA, AM (= `cA1`), CK3, Q, TG (= `cTG2`): the grid index with pooled caution nearest c\* (first minimum, so the smaller g on ties);
   - PS: F0's critical scales with one grid scale per tracker phase (0, 1, 2; threshold −1.0). Per phase, the unique (wrong go, caution sum, caution count) tuples in lexicographic order, each standing for its smallest grid index; over all triples, the lowest pooled wrong go (Σ wrong / all evaluated decisions) among pooled caution ≤ c\*; ties to the lowest caution, then the lowest flat index (phase 0 slowest).
2. **Per variant**: per run, the summed statistics of F0 at g = 1 and of each source at its setting (PS selects per decision by that decision's tracker phase in the variant's own arrays). Pooled caution and wrong go; differences source − F0; `CNT = boot_counts(35, 20000, 20261911)` (a fresh draw of the same seed per variant, so every variant uses the same counts); resampled sums `CNT @ per-run statistics`; `np.percentile(…, [2.5, 97.5])` over finite resamples.
3. **Classification** of every source (D-H1 = CK3, D-H2 = PS).

JSON: `matched_settings` (c\*, per source index, g, design caution and wrong go, tie counts; PS triple with tie diagnostics), `variants[kind]` (`F0_g1`, per source: caution, wrong go, counts, `d_caution` and `d_wrong_go` with point and interval, classification; `D-H1`, `D-H2`).

### `rc_d2_event_table_v13.py`
Per source (F0, N, CK3, TG) and scoring (`commit_3s`: safe iff `clean_clear(clear) > 0`; `react_stop_tau0p75`: safe iff `clean_clear(clearR075) > 0`, caution still by the 3 s definition):
1. the 202 grid points pooled over the runs; the non-dominated ones; the one with caution nearest 2 and nearest 5 (ties: smaller grid index);
2. the wrong-go decisions at that scale; the number of runs with ≥ 1;
3. per wrong-go decision: the 17 planner rows rebuilt with `finite_primitive.build_library` from the logged decision; the selected row's plan (3 s: the row's `s`, `v`; reaction-and-stop: `stop_profile_cont(s, v, a, 0.75, 6.0)` and its speed); ego rectangles along the ego yaw of `load_capture`'s truth at the decision tick; true actors from `ox.window_truth(T, k, kmax, draw, False)`; the first tick with `poly_dist ≤ 0`; closing speed = plan speed at that tick − the actor's true velocity (that tick's truth frame) along the ego yaw;
4. per run the median; across runs the median of the run medians.

JSON: `table[source][scoring]['2' | '5']` with grid index, g, caution, wrong go, counts, `n_runs_with_wrong_go`, `per_run` (count and median), `median_of_run_medians_mps`.

## Old-run tests (exploratory data; not results of D)
All on the shared, saturated laptop CPU (one core each). Outputs in `out\` with tags `t1`, `t2`.

**`rc_d_nonbraking_v13.py --test-old`** (35 old runs standing in for a variant; 20,000 resamples): **21 s** (`..._TESTOLD_t2.json`); with `--check-v12`, 232 s (`..._TESTOLD_t1.json`; the check calls the triple rule at 201 levels). The two outputs are identical in every value. Expect about 25–40 s for the three fresh variants.
- c\* = 8.968425 caution points (F0 at g = 1: wrong go 7.5875%, 629 of 8,290 evaluated decisions).
- Matched grid scales: N 0.8414, NA 0.8414, AM 0.1778, CK3 0.6683, Q 0.2113, TG 0.3548 (no ties). PS triple (phase 0, 1, 2): g = 118.85, 105.93, 0.08414 (grid indices 164, 162, 38); design caution 8.9384, design wrong go 0.2654%; 1,969,488 triples from 97 × 144 × 141 unique tuples; no tie; the same triple with `tensordot` sums.
- **Identity check of the triple rule:** the in-sample per-phase gain over the 201 levels of record is 5.465855283294024 points here and 5.465855283294024 in v12's record (`A9_3_PHASE_SCALE_CV_v02.json`, estimated phase, −1.0): difference 0.
- Old runs as a stand-in variant (in-sample, so only a mechanics test): CK3 − F0: caution +0.088 [−0.539, 0.668], wrong go −5.911 [−7.349, −4.578] → "inconclusive"; PS − F0: caution −0.030 [−2.414, 2.259], wrong go −7.322 [−8.913, −5.839] → "inconclusive". The point values equal the design values of the matched settings, as they must.
- Without the lock, the fresh mode exits with `REFUSED`.

**`rc_d2_event_table_v13.py --test-old --old-rs`** (35 old runs; 3 s commitment, and reaction-and-stop from the v11 cache of record): **481 s**, of which most is importing package B's library (about 2 min under the present load) and parsing 34 captures. Expect roughly 15–25 min for 105 fresh runs on this laptop under the same load (one capture parse per run with a wrong go; 16 source × scoring × target cells share the cache).
- Every wrong-go decision of every cell had a loss tick in its 61 true frames (`n_wrong_go_without_loss_tick` = 0 in all 16 cells), under both scorings. For reaction-and-stop this ties my plan to the cached clearances of record.
- The wrong-go count from the per-decision loop equals the count in the pooled table in every cell (the program refuses otherwise).
- Old-run values (exploratory; 3 s commitment): F0 at 5%: g = 0.2239, caution 4.961, wrong go 7.973%, 34 runs with a wrong go, median of run medians 9.26 m/s; CK3 at 5%: g = 0.1679, caution 5.016, wrong go 2.955%, 29 runs, 6.64 m/s. Under reaction-and-stop (old-run cache): F0 at 5%: 12 runs, 3.70 m/s; CK3 at 5%: 0 runs (median undefined, NaN in the JSON).
- For F0 under the 3 s commitment all 202 grid points are non-dominated by the literal rule (choice 10).
- Reaction-and-stop speed profile: against the central difference of `stop_profile_cont`'s positions on 300 synthetic rows, the largest gap is 0.081 m/s, at the kinks of the profile (the bound there is A·H/2 = 0.15 m/s); a coarse check only.
- Without the lock, the fresh mode exits with `REFUSED` before anything is imported.

**Not tested (no old data has it):** reading `arrays\CV0\*.npz` (key names taken from CD_DEFINITIONS), `clearR075`, the fresh log layout, a `des` array per decision.

## Choices made where A10 and CD_DEFINITIONS were silent (each can change a recounted value; compare with the first program)
**D1**
1. **What PS scales.** A10 says "the scale triple"; I took it as scales of **F0's** critical values (`cF0`), one per tracker phase.
2. **Tie order of the triple.** CD_DEFINITIONS: "the lowest flat index over the unique per-phase (wrong-go, caution sum, count) tuples. This is v12's `triple_choice`." The text does not say how the unique tuples are ordered, nor which grid scale stands for a tuple shared by several scales (it matters on fresh runs). **I read v12's `triple_choice` (`revision_v12\analysis\a9_3_phase_scale_cv_v02.py`, that function and its callers' table set-up only) to settle this**: lexicographic order (`np.unique(axis=0)`), first (smallest) grid index. It is a v12 program, not a v13 first program; my implementation is written separately and reproduces v12's in-sample record exactly (below). On the old runs the choice at c\* has no tie at all (one triple attains the minimum; each chosen tuple belongs to one grid index).
3. **Order of the floating-point sums.** Design tables are summed over runs in run order with `ndarray.sum(axis=0)`. The triple is the same with `tensordot` sums (`same_choice_with_tensordot_sums` in the JSON).
4. **Denominator of the triple's wrong go:** the evaluated decisions of the three tracker phases (= all evaluated decisions).
5. **TG = `cTG2`** (the definitions name `cTG2` for the old runs; the fresh arrays also hold `cTG1`, `cTG4`).
6. **Run order within a variant** (it fixes which run each bootstrap count belongs to): ascending run id. The program records whether the case file's order is the same (`d1_run_order_file_equals_sorted`); for the D1 case file it is.
7. **Classification order.** The four rules are applied in the order A10 writes them (costs progress; costs safety; no measurable cost; inconclusive). "Costs safety" and "no measurable cost" can both hold (e.g. a wrong-go interval of [0.1, 0.5]); the earlier one wins. "Lower end > 1 point" and "upper end ≤ 0" are read literally.
8. **Matched settings come from the 3 s commitment tables with F0's g = 0 point not added** (grid points only).
9. `des` in the fresh arrays may be a scalar or one value per decision; both are handled (same arithmetic per decision).

**D2**
10. **Frontier.** A10 says "each source on its own step frontier"; CD_DEFINITIONS says grid points "not dominated (no point with caution ≤ and wrong go <)". I used the grid points only (no F0 g = 0 point added to N, CK3, TG) and the definition literally: a point with equal wrong go and higher caution is **not** dominated and stays eligible.
11. **Several actors.** The first loss tick is the earliest over all true actors; if two actors lose clearance at the same tick, the first in the truth file's actor order is used.
12. **Plan speed under reaction-and-stop.** `stop_profile_cont` returns positions only. I wrote the matching speed: the row's `v` up to 0.75 s; then v₀ + a₀t + ½jt² while the acceleration ramps to −6 m/s² (|j| = 12.65), then v₁ − 6(t − t₁); zero from the stop time; never negative.
13. **Actor velocity:** the truth frame of the loss tick (`T[k + j]`), world right-handed (vx, vy) projected on the ego yaw of the decision tick (route yaw, as `load_capture`). Signed (a receding actor lowers the closing speed).
14. **A wrong-go decision without a loss tick in the 61 true frames** (should not occur for the 3 s commitment; could occur if `clearR075` was scored on more ticks or another routine): counted in `n_wrong_go_without_loss_tick`, left out of its run's median. A run whose wrong-go decisions all lack a tick has no median and is left out of the median of medians but stays in `n_runs_with_wrong_go`.
15. **Pooling.** The median of medians is over the runs with ≥ 1 wrong go. Targets 2 and 5 are in percentage points of desired speed (the unit of the caution rate).
16. **Run ids:** `pc13_<case>_native` (C) and `pd13_<id>_native` (D1; the D1 case file names the case `id`).
