# Package F (nuScenes): independent second program ("recount")

- **Model:** Claude Fable 5.2 (`claude-fable-5-2`). The first program is by Claude Opus 5.5.
- **Written:** 19 Nov 2026, in a separate session, from `AMENDMENT_10_v13.md` (§0, §2.2, §2.3, §2.6, §8, §10.1), `notes\ARRAYS_FORMAT_F_v01.md` and `notes\ADAPTER_SPEC_F_v01.md`.
- **Not read:** anything in `work\F_nuscenes\code\`, `work\shared\trackers\trk_score_v01.py`, or `work\F_nuscenes\out\` (the first program's outputs). `STATUS.md` of package F was read once for context; it holds no value of F.
- **Shared with the first program (A10 §10.1(b)):** the extracted decision arrays, the resample draws, and the scoring library of record `optA_lib_v02.py` (imported read-only from `<earlier-phase folder 1>\11_ojits\A6R\code\`).
- **Read as definitions only:** `revision_v12\analysis\a9_common_v01.py` and `a9_1_placebo_gridless_v01.py` part (c) (the gridless step frontier), and `revision_v11\analysis\rev_c_ratio_tracks_v01.py` (the rule of record for "binding rows"). No code was copied from them.

## Files

| File | Content |
|---|---|
| `fr_core_v01.py` | Own code: loader (refuses `val` before Lock 2), gridless events, two numba kernels, E5_x, margin-ratio summary, calibration rule |
| `fr_run_v01.py` | Populations, source packing, summaries |
| `fr_horizon_v01.py` | The horizon rule on the train arrays (T1; F0 and E only) → `F_RECOUNT_HORIZON_v01.json` |
| `fr_heldout_v01.py` | The held-out quantities on the val arrays → `F_RECOUNT_HELDOUT_v01.json`. **Prepared, not run.** |
| `fr_synth_v01.py`, `fr_test_v01.py` | Synthetic arrays in the documented format, and the tests |
| `synth\` | Synthetic arrays and synthetic outputs (no nuScenes data) |

Run every script with `..\venv\Scripts\python.exe -I <script>` from this folder.

## What is implemented

**Gridless curve (own code).** For each evaluated decision of a population, the rows that can ever be selected are the strict running maxima of the critical scale in cost order (NaN skipped). At g = 0 the first of them with a scale ≥ 0 is selected (the fallback row if none). Just above each such scale b < 1e3 the selection moves to the next one, and after the last to the fallback row. Each move is an event carrying the change of the totals (wrong go, caution sum, caution count). Events of all scenes are sorted by b (stable). A curve under scene weights is the g = 0 totals plus the running sum, read after the last event of each distinct b.

**Scoring.** As the format note: a row is safe when its clearance is > 0; wrong go = the selected row is not safe; caution = (mean speed of the first safe row − mean speed of the selected row) / desired, over safe selections. Rates in percent.

**Frontier and D (own code).** As `optA_lib_v02.eval_scoring`: 201 levels, equally spaced from F0's g = 0 caution to the smaller of F0's and E's largest caution; the step frontier is the lowest wrong go among points with caution ≤ level; every source other than F0 and E gets F0's g = 0 point in front; D_gl(A, F0) = Σ(F_F0 − F_A). R_gl = D_gl(E, F0)/201 in percentage points. RR_gl(A) = D_gl(A, F0)/D_gl(E, F0), NaN when the denominator is not > 0. Decision-equivalents = D/201/100 × decisions.

**Kernels.** `kernel` is the plain version; `kernel2` is faster and is the one used. The test requires them to be equal bit for bit.

**E5_IMM (§2.2).** On the val IMM arrays at the primary horizon: ρ = √(cF0/cE) on rows where both are finite and positive; r_i = median over those rows; u_i = (mid-rank − 0.5)/n; f_i = m(1 + A(2u_i − 1)); critical scales cF0/f_i². m, q05 and q95 come from √(cF0/cN) at the binding rows; A = (q95 − q05)/(2m).

**Intervals.** `default_rng(20261923).integers(0, n, (20000, n))`, scenes in sorted name order, turned into scene counts; levels are rebuilt in every resample; percentiles over the finite resamples (`numpy.percentile`, linear).

**Calibration (§2.6).** Outer `default_rng(20261912).integers(0, n, (2000, n))`; inner one stream `default_rng(20261913)`, `integers(0, n, (1000, n))` per outer sample in order, indexing that outer sample's scene list. For each outer sample and each nominal level 0.9500, 0.9505, …, 0.9995, the inner percentile interval either contains the full-sample point or not; the coverage of a level is the share of outer samples that do. The rule is then applied as written. The second inner seed (20261914) is run only if some statistic's nominal-95% coverage is below 0.94. The double bootstrap checkpoints every 50 outer samples and resumes.

**Lock 2.** The val split opens only when `revision_v13\LOCK_A10_2.txt` exists.

**Verdicts.** F-H0: calibrated lower end of R_gl (T1) > 0 and fewer than 2.5% of the 20,000 resamples with D ≤ 0. F-H1: calibrated interval of RR_gl(N) inside (−0.05, 0.05). F-H2: the H3 classification (a)–(d) on the calibrated intervals of r and c, with the "barely varies" flag. "Confirmed" needs every earlier hypothesis to pass.

## Tests (synthetic arrays, `fr_test_v01.py`)

1. **Fast path against the library of record.** For 12 synthetic scenes, the full sample and 3 resamples, both trackers, both horizons, both populations (32 comparisons of 12 values each), every source's curve is rebuilt by brute force with `optA_lib_v02.select_grid` and `stats_scored` at g = 0 and just above every critical value in [0, 1e3), and D is formed by `optA_lib_v02.eval_scoring`. Sources F0, E, N, TG, E5_x, E5, E5p and PO25/50/75. Decisions, c0, C and every D agree; the largest difference is reported by the test (tolerance 1e-9).
2. Kernel levels equal `numpy.linspace` exactly.
3. Mid-ranks equal a direct count.
4. The calibration rule on constructed coverage tables.

The horizon and held-out scripts were also run end to end on synthetic arrays (`--synth`, the held-out one with `--quick`).

## Ambiguities in the amendment, and how each was resolved

| # | Text | Ambiguity | Resolution here |
|---|---|---|---|
| 1 | §2.2 "binding rows of the scored run set" | Which rows | Rows of **evaluated** decisions with finite positive critical scales under both N and F0 (the rule of record, `rev_c_ratio_tracks_v01`). The format note says "rows with finite positive values of both" without "evaluated". The summary over all built decisions is written beside it as a variant |
| 2 | §2.2 "u_i = (rank of r_i − 0.5)/n over the run set's evaluated decisions" | Is n the number of evaluated decisions, or of those that have an r_i | Ranks are taken over the evaluated decisions that have an r_i, and **n is their number**; the others get 0.5. The point value of c with n = all evaluated decisions is written as a variant |
| 3 | §2.2 | Is E5_x rebuilt in each resample | **No.** m, A and u_i are fixed from the full val set; resamples re-weight scenes, as for every other source |
| 4 | §2.2, §8.4 | E5 for the in-path population | Built once on all evaluated decisions, then scored on the subset |
| 5 | §2.6 "estimated coverage" | Coverage of what | Of the full-sample point estimate, by the inner percentile interval of each outer sample |
| 6 | §2.6 "its Monte Carlo SD" | SD of what; divisor | SD (ddof = 1) over the 2,000 resamples of the outer samples of the **calibrated level itself**, i.e. the smallest grid level with coverage ≥ 0.95, recomputed in each resample. Also written: ddof = 0, and a variant that applies the whole rule in each resample |
| 7 | §2.6 "a repeat with a second inner seed agrees within 0.002" | What is repeated | The calibrated level (smallest grid level with coverage ≥ 0.95) from a full second double bootstrap with inner seed 20261914 and the same outer draw |
| 8 | §2.6 | No grid level reaches 0.95 | Treated as a failed check: nominal 99% |
| 9 | §2.6 | Inner resamples without room (ratio undefined) | Percentiles over the finite inner values; an outer sample with none counts as not covering |
| 10 | §2.6 "each hypothesis statistic" | Which | R_gl (T1), RR_gl(N), R_gl,IMM, r, c and r/c, on the primary population. The in-path population gets 95% percentile intervals only |
| 11 | §5.3 H3 "efficiency r/c" | Definition in resamples | r/c in each resample; non-finite values are invalid |
| 12 | §8.5 "fewer than 2.5% of resamples non-positive" | Non-finite resamples | Counted as non-positive |
| 13 | §2.3 | Largest margin scale on nuScenes | 1e3, as in the v12 gridless code |
| 14 | §8.3 | 2 s horizon: caution | The arrays hold one `vbar` (mean speed over 3 s); it is used at 2 s too. Safety uses `clear2`, the population `evaluated2`, the scales the `_2` keys |
| 15 | §8.6 | In-path population on the design split | R_gl of the in-path population is computed (it is the same quantity, D(E, F0)); it does not decide the rule. Nothing else is read: the N, TG and IMM arrays of train are never opened |
| 16 | Coordination rule 3 | Where Lock 2 lives | Only `revision_v13\LOCK_A10_2.txt` opens the val split (coordinator, 19 Nov) |
| 17 | §8.5 F-H2 "barely varies" | Rows | The binding rows of item 1 |

## Additions of 19 Nov (coordinator's message, before Lock 2)

Written from the message's text, `RESULTS_INTERFACE_v13.md` §1 and, as a definition, `revision_v11nalysisev_g_partial_oracle_draws_v01.py`. No first-program code or output was read.

- **T1's descriptive sources on the val arrays, primary horizon, both populations, 95% percentile intervals over the 20,000 resamples:**
  - **E5:** §2.2 with f_i = 1.1029 · (1 + 0.05 (2u_i − 1)); u_i from T1's own √(cF0/cE), by the same rule as E5_IMM.
  - **E5p:** u_i permuted within each scene among its evaluated decisions; one `default_rng(20261915)`, one `rng.permutation(u of the scene's evaluated decisions, in decision order)` per scene, scenes in sorted order.
  - **RR_E5mP** = (D_gl(E5) − D_gl(E5p)) / D_gl(E, F0), formed in each resample.
  - **PO25, PO50, PO75:** U = `default_rng(20261919).random(N)`, one uniform per stored decision of the val T1 arrays (evaluated or not) in (sorted scene name, decision index) order; PO_p takes E's critical scales where U < p and F0's elsewhere.
  - All are built once on the full val set and fixed in every resample; the in-path population scores the same scales on its subset.
- **Decision-equivalents:** D/201/100 × decisions, in each resample with that resample's decision count. For a hypothesis statistic the interval is at the level of its share's §2.6 interval; for the others at 95%.
- **Export:** `fr_heldout_v01.py` also writes `work\F_nuscenes\out\A_RECOUNT_F.json` (write-once; it does not read or list anything else in `out\`). `F.status` and `F.provenance` are written as the coordinator gave them; the recount does not determine them. `F.RR_CK3` and `F.RR_AM` are left out (recorded departure of package F).
- **Lock 2:** only `revision_v13\LOCK_A10_2.txt`.
- **Tests:** the library comparison now covers E5 (1.1029, 0.05), E5p and PO25/50/75 as well; the permutation is checked to stay within scenes and evaluated decisions, and the PO mask against a direct draw.

Further ambiguities:

| # | Text | Ambiguity | Resolution here |
|---|---|---|---|
| 18 | E5p "permuted within each scene" | How the generator is used | `rng.permutation(values)` on the scene's evaluated u in decision order (equal to indexing by `rng.permutation(n)`); scenes without evaluated decisions still make one (empty) call |
| 19 | E5 − E5p, in-path population | Which permutation | The one made over all evaluated decisions; not redrawn for the subset |
| 20 | `X.dec.ci` | Decision count in a resample | The resample's own count |
| 21 | `F.IMM.eff` | Decision-equivalents | None exported (a ratio of two shares has none) |

## Results

See the end of this file (added when computed).

### Horizon rule (A10 §8.3), design split, T1 — computed 19 Nov 2026, about 23:25 EST

Output: `F_RECOUNT_HORIZON_v01.json` (log: `horizon_run_log.txt`). 700 train scenes, 110,266 built decisions; 20,000 scene resamples of `default_rng(20261923)`.

| Horizon | Population | Decisions | R_gl (pp) | 95% percentile interval | Share of resamples with D ≤ 0 |
|---|---|---|---|---|---|
| 3 s | all evaluated | 88,737 | 0.000000 (exactly 0) | [−0.001122, 0.002244] | 0.75265 |
| 3 s | in-path | 23,503 | −0.004234 | [−0.021831, 0.027237] | 0.76290 |
| 2 s | all evaluated | 95,871 | 0.000000 (exactly 0) | [−0.001027, 0.141910] | 0.41660 |
| 2 s | in-path | 25,506 | 0.240447 | [−0.052851, 0.488097] | 0.14015 |

**Rule outcome in this recount:** the lower 95% end is not > 0 at 3 s or at 2 s on all evaluated decisions, so "F stops and reports no measurable room on design data at 2 or 3 s". No resample was non-finite.

**Why the room is exactly zero (a diagnostic of D(E, F0) only; nothing else was computed on train).** For both F0 and E the wrong-go count is lowest at margin scale 0 and rises with the scale: at 3 s from 4,490 of 88,737 decisions at g = 0 to 17,088 (F0) and 17,032 (E) at the largest scale; at 2 s from 805 to 2,076 and 2,074. Both step frontiers are therefore flat at the g = 0 value on all 201 levels, and their difference is 0. In these arrays, more margin selects slower rows, and slower rows are more often unsafe by the truth clearance. About 35% (3 s) and 24% (2 s) of the rows of evaluated decisions have a critical scale of −inf under both sources. Whether this is a property of open-loop replay on nuScenes (for example, traffic behind a braking ego) or of the adapter is for package F to judge; the recount scored the arrays as given.

**Consequence for the held-out script.** `fr_heldout_v01.py` reads the primary horizon from the file above and stops when there is none. It runs only with an explicit `--horizon 3` or `--horizon 2`, which it records.

## Clearance departure of 19 Nov 2026 (prepared 20 Nov, about 00:10 EST)

From the coordinator's message and `notes\F_DEPARTURE_CLEARANCE_v01.md` §2. The recount does not recompute the clearances; it reads them from `cache\clear_v02\<split>\<scene>.npz` (extracted arrays, A10 §10.1(b)) and scores them. Everything else is as before. The v01 scripts and `F_RECOUNT_HORIZON_v01.json` are unchanged.

| File | Content |
|---|---|
| `fr_core_v01.py` (additions) | `swap_clear_v02` (replaces `clear`/`clear2`; checks sweep, shape and NaN pattern against the arrays; refuses val before Lock 2) and `removed_counts` |
| `fr_horizon_v02.py` | The §8.3 rule on clear_v02, once, → `F_RECOUNT_HORIZON_v02.json`, with the removed-contact counts |
| `fr_heldout_v02.py` | Held-out recount on `clear_v02\val`; horizon from the v02 file; export with `F.clearance`, `F.prereg.*`, `F.design.*` (v02) and `F.design.removed<h>.<source>`. If v02 also stops, it writes only the export (`F.status = "no_room_design"`) and opens no val file |
| `fr_test_v02_scripts.py` | Synthetic check of the v02 scripts against the v01 outputs |

**Removed-contact counts (train, F0 and E only, all evaluated decisions, 3 s and 2 s).** Selection at g = 1: first row with critical scale ≥ 1, else `idx55`. "Removed" = the selected row is unsafe (≤ 0) under the arrays' clearance and safe (> 0) under clear_v02; "added" is the reverse. Also the evaluated (decision, row) pairs whose safety changes, in each direction.

**Synthetic tests (20 Nov).**
- With a clear_v02 equal to the arrays' clearance, the loaded scenes are identical, `fr_horizon_v02.py` reproduces every v01 horizon number exactly, `fr_heldout_v02.py` reproduces all 70 export values of v01 exactly, and every removed count is 0.
- With a modified clear_v02 (some contacts removed), the fast path still equals the library path (largest difference 8.5e-13), and `removed_counts` equals a plain loop.
- The stop branch of the export was exercised with `--force-stop` (synthetic only).

**Notes.** `fr_heldout_v02.py` has no `--horizon` override. `F.prereg.horizon` and, if v02 stops, `F.horizon` are the sentence "no measurable room on design data at 2 or 3 s".
