# Package C (v13): B7 rate × latency on the fresh lead-braking runs (§1–7) and cut-in runs (§8) — definitions for both programs

First written 20 Nov 2026, 02:20 EST (this machine's clock); **revised 20 Nov, ~02:50 EST for the coordinator's scope change of 01:53 EST**:
package B now owns Table III on fresh runs (all `B.<x>.*` keys, the variant re-tracking B2/B3/B4 and B1's sensitivities, E5_x). This file
now defines **B7 only**; the Table III text of the first version is kept at the end, marked **superseded**, and nothing in it is computed
by package CD. Both versions were written by the CD first-program writer for B7 (Claude Opus 5.5) **before Lock 2 and before any value of a
fresh run was computed** (no fresh array, log or B7 detection file was opened).

Source: `..\..\AMENDMENT_10_v13.md` (A10) §2.1 ("For the rate variants of B7, F0_x = P̄ of record"), §2.3, §3 rows B3 (lag) and **B7**,
§5.7 ("B7 at every rate × latency"); package B's method of record for the shared quantities (`work\B_retrack\code\b_analysis_v01.py`,
`B_retrack\B_ANALYSIS_DEFINITIONS_v01.md`: room by population, after-stop room, lag) and its frozen library (`work\shared\trackers\`,
README §3 "B7", `IMM_AND_VARIANTS_SPEC_v01.md` §6). `CD_DEFINITIONS_v13.md` (gridless frontier, bootstrap, run order) applies where this
file is silent. Status of every value: **descriptive** (A10 §5.7): no hypothesis, no calibration; every interval is a nominal 95%
percentile interval (`.level` = 0.95, `.cal` = "nominal95").

A second program is written from A10, the method-of-record files above, `CD_DEFINITIONS_v13.md` and this file, never from the first
programs (`analysis\x_trk_extract_v13.py`, `analysis\c_b7_v13.py`). It may share the frozen tracker library, the scoring library of record,
the extracted arrays (`arrays\B7_*`, `arrays\CV0`) and the resample draw (A10 §10.1(b)).

## 1. Lock gate and run set
- B7 is stage-2 code (README_COORDINATION, 20 Nov 01:53 EST). No fresh log, array or B7 detection file is read unless **both**
  `revision_v13\LOCK_A10_2.txt` and `revision_v13\LOCK_A10_2c.txt` exist (first programs: `cd_common_v13.require_lock2c`). Fresh CV0/B1
  arrays and run folders that appear after stage 1 are not opened before LOCK_A10_2c. Every program has a `--test-old` mode on old run
  p1b_fit_finite_0037 only (the one old run with B7 detection rows).
- **Run set**: the 105 fresh lead-braking runs `cd_common_v13.c_run_ids('lead_braking')` (lead-braking cases of `CASES_C_v13.json`, each
  replaced by its replacement if `REPLACEMENTS_C_v13.json` lists one, as `pc13_<case>_native`), **sorted ascending**; this order is the
  run order of every resample.
- Logs: `CD_capture\runs\<rid>\<rid>\` holds `SUMMARY.json` (run_dir) and one `capture\<case>\` folder (cap_dir); usable when
  `runs\<rid>\LOGS_OK` exists (written by `c_extract_v13.py`). B7 detections: `CD_capture\b7\<rid>\b7_detections_v13.jsonl` with
  `B7_MANIFEST_v13.json` beside it.

## 2. Arrays of the B7 chains (`CD_capture\arrays\B7_<r>_<L>\<rid>.npz`, written by `x_trk_extract_v13.py`)
- Detection rows of rate r ∈ {2, 5, 10}: the rows of the run's B7 file (one row per odd k ≥ 19, keys `k, frame, time, rates_hz,
  online_tick, model, combined_hash, inference_s`; written on the pod by `tools\b7_redetect_v13.py`) whose `rates_hz` contains r, **in file
  order**. Checked: strictly ascending k; 2 Hz: k ≡ 9 (mod 10); 5 Hz: (k − 19) ≡ 0 (mod 4); 10 Hz: odd k ≥ 19. A violation stops the job.
- **The 2 Hz chains also use the offline rows** (not the logged `detections.jsonl`), so all rates share one detection run. When B7 (i)
  passes (§5) the offline 2 Hz rows reproduce the logged ones; when it fails they are A10's reference ("the offline 2 Hz detection is the
  reference").
- Re-tracking: `trk_tracker_v01.retrack_capture(cap, 'CV0', det_rows=rows_r, dt=dt_r, q_scale=True, latency=L)`, dt_2 = 0.5, dt_5 = 0.2,
  dt_10 = 0.1 s (library: every class's process noise × dt/0.5 elementwise; R unchanged; deletion ages in frames = round(max_age · 0.5/dt),
  car 7.5 s). Latency: a decision at tick k uses the tracks of the last frame whose k_frame · 0.05 + L ≤ k · 0.05 + 1e-9; no such frame →
  no actors.
- Arrays: `with trk_arrays_v01.overlay(cap, ov): trk_arrays_v01.extract(run_dir, cap, PB, lead=True, a4=True)` with PB = the P̄ of record
  (`P\09_redesign\m2_decisions\openloop\pbar_tuning_v01.json` key `Pbar`; A10 §2.1). The file holds every array `extract` returns (keys
  `k, evaluated, v0, des, clear, vbar, idx55, cF0, cN, cE, cNA, cQ, cA1, cCK3, phase, lead_found, track_id, vhat, ahat_long, age, now,
  nis_last, nees_v, dx_pred0..3`, …; one row per assessment decision in tick order; `(n, 17)` for critical scales) and `meta` (JSON:
  extract's meta + run_id, variant `B7_<r>_<L>`, rate_hz, latency_s, dt, n_det_rows, timing).
- Combinations (r Hz, L s): (2, 0), (2, 0.1), (5, 0), (5, 0.1), (5, 0.2), (10, 0), (10, 0.1), (10, 0.2). Folder `B7_<r>_<L>` with L printed
  `0`, `0.1`, `0.2` (e.g. `B7_10_0.1`). 2 Hz at 0.2 s is not run (A10 B7 (iv): "2 Hz reference at 0 and 0.1 s").
- **Reference array** of a run: `arrays\CV0\<rid>.npz` (online tracker of record on the logged files, `c_extract_v13.py`). Before scoring,
  every chain's `k`, `idx55`, `evaluated` and `clean_clear(clear)` must equal the reference's (they depend on the ego state and truth only);
  otherwise the program stops (A10 §11).

## 3. Scoring (as of record)
- 3 s commitment: a row is safe iff `optA_lib_v02.clean_clear(clear) > 0`. Evaluated decisions only.
- **Truth phase** for every chain: the reference (CV0) array's `phase` (0 before onset, 1 lead moving, 2 lead stopped, 3 unknown), as
  package B's old-run analysis used the record's truth phase for every variant. A chain's own `phase` (which depends on its actors through
  the matching) is not used; the count of decisions where it differs is printed as a diagnostic.
- Populations (masks within evaluated decisions): pop 0 all; pop 1 truth phase 2 ("after-stop", as of record for the B3/B4 and B7 rules).
- Sources (the chain's own arrays): F0 = `cF0` (states of the chain, P̄ of record), E = `cE`, N = `cN`, CK3 = `cCK3`.
- **Gridless step frontier** (A10 §2.3, A9-1(c)): `trk_score_v01.gridless(runs, ['F0', 'E', 'N', 'CK3'])` (run dicts: `desired` =
  `des[0]`, `idx55`, `clear1` = clean_clear(clear), `vbar`, `ev`, `masks`, `crit`); points `trk_score_v01.rr_gl(G, 'F0', 'E', ['N', 'CK3'],
  pop)`; every source except F0 and E gets F0's g = 0 point; 201 levels `linspace(c_F0(0), min(max c_F0, max c_E), 201)` per population and
  per resample. D(A) = Σ_ℓ (F_F0 − F_A); room R_gl (pp) = D(E)/201; decision-equivalents = D(E)/201/100 · n (n = decisions in the
  population); RR_gl(A) = D(A)/D(E), NaN if D(E) ≤ 0. Resamples: `gl_fast_v13` (bit-identical to the library; checked at the full sample).

## 4. Lag (A10 B3 row "the lag (median of CV-predicted minus true lead position at 3 s in the first second after the stop)"; as of record)
Per run: t_stop = `now` of the run's first decision (any decision, evaluated or not) with truth phase 2 (§3); none → the run contributes
nothing. Selected decisions: evaluated, truth phase 2, 0 ≤ now − t_stop < 1 s, the chain's `lead_found` true. Value: the chain's
`dx_pred3` (the planner's constant-velocity prediction of the matched lead track's longitudinal position at 3 s minus the true one, m).
Pool the finite values over runs; `lag` = `np.median`; details n, q25, q75 (`np.percentile`). No value → null.

## 5. Keys (prefix `B7.<r>.<L>.`, r ∈ {2, 5, 10}, L printed `0`, `0.1`, `0.2`; e.g. `B7.10.0.1.as_room`)
| Key | Quantity (on the chain's own room) |
|---|---|
| `R` | R_gl (pp), pop 0 |
| `as_room` | R_gl in **decision-equivalents**, pop 1 (truth phase 2) |
| `as_room.pp` | the same in pp (extra; see §7.1) |
| `RR_N`, `RR_N.ci`, `RR_N.level`, `RR_N.cal` | RR_gl(N), pop 0; 0.95; "nominal95" |
| `RR_CK3` | RR_gl(CK3), pop 0 (interval in details) |
| `lag` | §4 on the chain's arrays |

Run-set keys:
- `B7.identity` (A10 B7 (i)), per run from the logged `capture\<case>\detections.jsonl` (the online 2 Hz ticks) and the run's B7 file:
  every logged row has a B7 row with the same k; `combined_hash` equal; the same number of boxes; for each box in order,
  |translation − translation'| ≤ 1e-6 m and |size − size'| ≤ 1e-6 m in every component. "pass" if every run passes, else "fail".
  Details per run: ticks, matched, hash matches, box-count matches, max |Δ| of translation, size, velocity, rotation and score, name
  mismatches, and offline 2 Hz rows with no online tick at k ≤ the last decision tick (counted, not deciding).
- `B7.ratio_10_2` = as_room(10, 0.1) / as_room(2, 0) (null unless both are defined and the denominator > 0).
- `B7.rule_rate` = "consequence" if as_room(10, 0.1) < 0.5 · as_room(2, 0), else "holds" (A10 B7 rule; A's `outcomes_v13.py`).
- `B7.rule_N` = "qualified" if for any of the eight combinations the RR_N interval is not inside the open interval (−0.05, 0.05), else
  "holds" (null if any interval is undefined).
- Details (not keys): per chain the margin-ratio check (`trk_score_v01.ratio_summary(margin_ratios(runs, 'N', 'F0'))`: median, q05, q95,
  A, share within 5%, barely varies; A10 §5.7 "the margin-ratio check for every variant"), the R and RR_CK3 intervals, R in
  decision-equivalents, n per population, the lead track's state age at evaluated decisions (median, q90, max; shows the latency and rate),
  chain-phase differences, resamples without room; for `B7_2_0` the per-key comparison with the reference array (B7 (i) at array level).

## 6. Intervals and draws
- Fresh: `optA_lib_v02.boot_counts(105, 20000, 20261911)` (= `default_rng(20261911).integers(0, 105, (20000, 105))` as counts per run,
  runs in §1 order), one draw for every chain. Interval: `np.percentile(b[finite], [2.5, 97.5])` (= `L.pct`); RR is NaN in resamples with
  D(E) ≤ 0 and is dropped (count in details).
- Old-run test (one run, p1b_fit_finite_0037): the same seed over one run (every resample is the run itself); the values are a pipeline
  exercise, not results. A10 B7 asks only for the lag statistics on this run.

## 7. Choices not fixed by A10 or the method of record (recorded before any fresh value)
1. `as_room` is in decision-equivalents (key list `A_KEYS_CD_v13.json` value_type "number, decision-equivalents"; interface §3 "After-stop
   room as_room is in decision-equivalents"), although interface §4 says "(pp)" and A's wording branch prints it with "points"; a `.pp`
   twin is exported beside it. `B7.ratio_10_2` and `B7.rule_rate` are unit-free (both rooms on the same decisions).
2. Truth phase from the CV0 reference array for every chain (§3).
3. The 2 Hz chains use the offline 2 Hz rows (§2).
4. The identity tolerance applies to translation and size (metres); velocity, rotation and score differences are reported only.
5. 2 Hz at L = 0.2 s is not computed (not in A10; not in the key list).

## 8. Cut-in family (B7CI; added 20 Nov 2026, ~03:45 EST, before any fresh value; coordinator 03:35: A10 B7 "both families")
Everything in §1–§7 applies, with these differences.
- **Run set**: the 105 fresh cut-in runs `cd_common_v13.c_run_ids('cutin')`, sorted ascending (run order of every resample).
- **Arrays**: `CD_capture\arrays\B7CI_<r>_<L>\<rid>.npz` (folder prefix `B7CI_`, e.g. `B7CI_10_0.1`), made exactly as §2 (the run's
  B7 file `b7\<rid>\b7_detections_v13.jsonl`, the same eight chains, `retrack_capture(cap, 'CV0', det_rows, dt, q_scale=True, latency=L)`,
  overlay + extract with the P̄ of record). Reference array: the run's `arrays\CV0\<rid>.npz` (cut-in CV0 of `c_extract_v13.py`); the §2
  consistency check (k, idx55, evaluated, clean_clear(clear)) applies.
- **Event tick (from truth; the same for every chain)**, as package B's B9 (`b9_cutin_v01.event_tick`, also in `c_cutin_v13.py`) and
  `CD_DEFINITIONS_v13.md` "C, cut-in": T = `trk_arrays_v01.load_capture(run_dir, cap)['T']` (truth in the route frame, `route_yaw_rh`;
  per tick the ego (x, y, yaw), `target_id` = the primary actor, actors' centres). Lane centre = the median over all truth ticks of
  −sin(yaw_k)·x_k + cos(yaw_k)·y_k (ego). k_c = the first truth tick (ascending) at which the primary actor is present and
  along = cos(yaw)(a_x − e_x) + sin(yaw)(a_y − e_y) > 0 and |−sin(yaw)·a_x + cos(yaw)·a_y − lane| ≤ 1.75 m. No such tick → no event.
- **Event window** (the population): evaluated decisions (decision ticks k of `gc.decisions(cap)` = the arrays' `k`) with
  rel = (k − k_c) · 0.05 in [−1, +4] s (both ends closed; the 0.05 s tick clock, not float timestamps). Runs without an event have an
  empty window and **stay in the resampled set** (as K0/K1). The window is computed once per run from truth and used for every chain.
- **Scoring**: the 3 s commitment (as K0/K1); sources F0 (chain's states, P̄ of record), E, N, CK3 of the chain; gridless step frontier
  on the window population (§3); R_gl (pp) = D(E)/201; RR_gl(N), RR_gl(CK3) = D/D(E), NaN if D(E) ≤ 0.
- **Keys** (prefix `B7CI.<r>.<L>.`): `R` (pp), `RR_CK3`, `RR_N`, `RR_N.ci`, `RR_N.level` = 0.95, `RR_N.cal` = "nominal95";
  `as_room` = "not applicable" and `lag` = "not applicable" (no lead stop in a cut-in run). Interval: `boot_counts(105, 20000, 20261911)`,
  `np.percentile` 2.5/97.5 over resamples with D(E) > 0 (dropped count in details). Extra key `B7CI.identity` = §5's B7 (i) rule on the
  cut-in runs. Details: R interval, R in decision-equivalents, RR_CK3 interval, window size, events found, runs without an event, the
  margin-ratio check of each chain (over the window decisions), for `B7CI_2_0` the per-key comparison with the CV0 array.
- **Old-run test** (no old cut-in run kept its sweeps): the 20 cut-in tuning runs of record (`run_index_m4_v02.csv`, set tune, family
  cutin, sorted). Chain (2, 0) is built by the same extractor from the **logged** detection rows (`detections.jsonl` as logged; the
  tracker reads `k`, `time`, `model`) at dt 0.5, L = 0; it must equal the logged arrays (extract without overlay) exactly, and its
  window values (R, RR_N, with
  their nominal intervals on `default_rng(20261911)` with the test's resample count) must equal `TESTOLD_C_CUTIN_K0_K2_v13.json`'s K0/K1
  and its descriptive `window` and `all_evaluated` populations.

## Superseded (20 Nov 2026, ~02:50 EST): Table III per tracker — moved to package B; nothing below is computed by package CD
The first version (02:20 EST) also defined, for x ∈ {CV, CV2, CA, IMM, AQ} and the sensitivities IMM090/IMM098: variant arrays
`arrays\B3|B4|B2|B1_d090|B1_d098\<rid>.npz` (`retrack_capture(cap, v)`, overlay, extract with `B_retrack\out\pbar\PBAR_<v>_v01.json`), and the
keys `B.<x>.within5, RR(.ci), c(.ci), RR_minus_c(.ci), RR_CK3(.ci), room_pre/brk/stop, as_room(.pp), lag`, `B.tuning`, `B.ca_window`
(E5_x per A10 §2.2 with m_x, A_x from x's margin ratio and u from F0_x/E_x; populations by x's estimated phase; truth phase from CV0).
**Superseded by the coordinator's decision of 20 Nov 01:53 EST: package B owns these keys and their definitions
(`B_retrack\B_FRESH_DEFINITIONS_v02.md` and its successors).** The first program's draft is kept, unused, as
`analysis\superseded_c_trackers_v13.py.txt`; no `B.<x>.*` key appears in any package-CD output.
</content>
