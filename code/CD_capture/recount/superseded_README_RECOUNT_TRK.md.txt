# Recount (second program): Table III per tracker and B7 rate × latency (package CD, v13)

Written 20 Nov 2026 by a subagent on Claude Fable 5.2 (the first program's writer is Claude Opus 5.5), before Lock 2 and before any
value of a fresh run existed. Program: `rc_trackers_v13.py` (this folder). It uses this recount's own core (`rc_core_v13.py`,
`rc_kern_v13.py`: selection paths, gridless curves, numba kernel, E5 ranks, estimated phase, percentile intervals).

## Independence
- Not opened: any `.py` under `CD_capture\analysis\` or `CD_capture\tools\` (in particular `c_trackers_v13.py`, `c_b7_v13.py`,
  `x_trk_extract_v13.py`), `cd_common_v13.py`, `gl_fast_v13.py`, and the shared library's scoring code `trk_score_v01.py`.
- Read: A10 (§0, §2, §3, §4, §5, §10), `CD_DEFINITIONS_v13.md`, `CD_DEFINITIONS_TRK_v13.md` (version of 20 Nov 02:14 EST),
  `BRIEF_COMMON_v13.md`, `A_KEYS_CD_v13.json`, A's interface (§2, §4 lines on B and B7), package B's definitions
  (`B_ANALYSIS_DEFINITIONS_v01.md`, `B_FRESH_DEFINITIONS_v02.md`), package B's recount (`B_retrack\recount\rc_core.py`,
  `b_variants.py`, README; another model's work), the lag and load lines of `B_retrack\code\b_analysis_v01.py` and the interval
  lines of `b2_oracle_check_v01.py` (method of record), the README and constants of `shared\trackers\`.
- Shared with the first program (A10 §10.1(b)): the extracted arrays, the B7 detection files, the resample draws. The scoring
  library of record (`optA_lib_v02`, v12's `a9_common_v01`) is used only for a full-sample cross-check of every tracker and chain
  (`details.*.library_of_record.max_abs_diff`) and for `dec_eq` / `ratio`.
- Before Lock 2 nothing under `arrays\`, `runs\`, `archives\`, `pod_outputs\` was opened. One slip to record: a directory listing of
  `CD_capture\b7\` printed the names of the fresh-run folders there (names only; no file of a fresh run was opened or read). The old
  run's folder `b7\p1b_fit_finite_0037\` was read (allowed).

## What it computes
Run set (fresh): the lead-braking runs found in `arrays\CV0\` (`pc13_*.npz`, meta family `lead_braking`, no lead variant), ascending
run id; this must equal the lead-braking cases of `CASES_C_v13.json` unless `REPLACEMENTS_C_v13.json` exists, and must count 105.
Every other tracker and chain must have a file for each of these runs, and its `k`, `idx55`, `evaluated` and cleaned clearance must
equal the CV0 file's (else the program stops). The truth phase of every tracker and chain is the CV0 file's `phase`.

Per tracker x ∈ {CV (`CV0`), CV2 (`B3`), CA (`B4`), IMM (`B1`), AQ (`B2`)} and, if all runs have arrays, IMM090 (`B1_d090`) and
IMM098 (`B1_d098`), each on its own room (F0_x = `cF0`, E_x = `cE`, N_x = `cN`, CK3_x = `cCK3`), 3 s commitment, evaluated decisions,
gridless step frontier on 201 levels:
- `B.<x>.within5`: share of sqrt(cF0/cN) (evaluated decisions, rows with both finite and > 0) within 5% of its median m_x.
- `B.<x>.RR`, `.RR.ci`: RR_gl(N_x), all decisions. `B.<x>.c`, `.c.ci`: RR_gl(E5_x), with f_i = m_x (1 + A_x (2u_i − 1)),
  A_x = (q95 − q05)/(2 m_x), u from x's own F0_x / E_x (mid-ranks among decisions with a ratio; others 0.5). m_x, A_x and u fixed in
  the resamples. `B.<x>.RR_minus_c`, `.ci`: the difference, per resample.
- `B.<x>.room_pre / room_brk / room_stop`: R_gl (pp) in x's estimated phases (threshold −1.0 m/s²), each on its own frontier.
- `B.<x>.as_room`: R_gl in decision-equivalents in the truth-phase-2 population (`as_room.pp` beside).
- `B.<x>.lag`: median of x's `dx_pred3` over evaluated truth-phase-2 decisions with `lead_found` and 0 ≤ now − t_stop < 1,
  t_stop = `now` of the run's first truth-phase-2 decision (any decision); finite values pooled over runs (method of record).
- `B.<x>.RR_CK3` (+ `.ci`): RR_gl(CK3_x), all decisions.
- `B.tuning`: "depends" / "persists" (A10 B3 rule on point values). `B.ca_window`: from `trk_constants_v01.json`
  (`tuning.sigma_a2`: median NIS 1.634, outside [1.8, 2.2] → false), checked against `B_RESULTS_SUMMARY_v13.json`.

Per B7 chain (r, L) ∈ {(2,0), (2,0.1), (5,0), (5,0.1), (5,0.2), (10,0), (10,0.1), (10,0.2)} from `arrays\B7_<r>_<L>\`:
`B7.<r>.<L>.R` (pp), `.as_room` (decision-equivalents; `.as_room.pp`), `.RR_N` + `.RR_N.ci`, `.RR_CK3`, `.lag`; then
`B7.ratio_10_2`, `B7.rule_rate` ("consequence" / "holds"), `B7.rule_N` ("qualified" / "holds").
`B7.identity`: recomputed here from each run's logged `detections.jsonl` and `b7\<rid>\b7_detections_v13.jsonl` (same k, equal
combined hash, equal box count, every component of translation and size within 1e-6 m; "pass" only if every run passes).

Intervals: nominal 95% percentile over the finite resamples (`.level` 0.95, `.cal` "nominal95"); fresh draw
`default_rng(20261911).integers(0, 105, (20000, 105))` as counts, runs in ascending id; old-run tests: first 2,000 rows of
`default_rng(20261113).integers(0, 35, (20000, 35))`. Per-resample `denE, n, D_N, D_E5x, D_CK3` are saved in
`out\<stem>_boot_<name>.npz` for a row-by-row comparison.

## How to run (after Lock 2)
```
set OPENBLAS_CORETYPE=Haswell
.venv\Scripts\python.exe -I -B -X utf8 recount\rc_trackers_v13.py                      (everything -> out\RC_TRK_v13.json)
... rc_trackers_v13.py --only CV,CV2 --tag _p1      (pieces; any split)
... rc_trackers_v13.py --combine _p1,_p2,_p3 --tag _all   (merges the pieces, then rules and B7 identity)
```
Two threads. Expected time on the shared laptop for 105 runs and 20,000 resamples: roughly 20 min per tracker and 12 min per B7
chain (extrapolated from the old-run test: 35 runs, 2,000 resamples, about 60 s per tracker including a 30 s library cross-check),
about 3.5–4 hours in all; pieces can be run one after another. Outputs are never overwritten (new `--tag`).

## Tests on old runs (20 Nov 2026)
See the end of this file ("Test results").

## Disagreements with, and remarks on, the writer's specification (`CD_DEFINITIONS_TRK_v13.md`)
None that changes a value. Remarks:
1. **Key list.** `A_KEYS_CD_v13.json` holds no `B.<x>.RR_minus_c(.ci)`, `B.<x>.RR_CK3.ci`, `B.IMM.as_room`, `B.AQ.as_room`,
   `B.ca_window`, `B.tuning`, `B7.ratio_10_2`, `B7.rule_rate`, `B7.rule_N`, `*.as_room.pp` (the interface text names some of them).
   They are written anyway, under the names of the specification, and listed in `details.keys_beyond_A_KEYS_CD_v13`.
2. **`as_room` unit.** Decision-equivalents, as the key list says; A's interface §4 still says "(pp)". Same reading as the writer.
3. **`B.ca_window` source.** The specification copies `B_RESULTS_SUMMARY_v13.json`; this program reads the frozen constants
   (`trk_constants_v01.json`), tests the recorded median against the window itself, and stops if the two files disagree.
4. **Lag clock.** Both follow the method of record (`now`, plain comparison, `lead_found`). The tick-clock reading
   (k − k_stop in 0..19) is printed beside as a diagnostic (`details.*.lag.tick_clock`); on the old runs it selects the same decisions.
5. **RR − c.** The specification writes (D_N − D_E5x)/D_E; this program takes RR_N − c per resample (the method of record,
   `b2_oracle_check_v01`). Identical to rounding (about 1e-16).
6. **B7 identity.** The specification's tolerance covers translation and size; A10 says "boxes within 1e-6 m". Same reading here;
   the stricter all-component result (velocity, rotation, score, class) is in `details.B7_identity` for information.
   If some runs lack files and none fails, this program writes `null`, not "pass".
7. **B7 run set and families.** A10 B7 names "both families"; the specification and the keys cover the lead-braking runs only. This
   program follows the specification (no cut-in B7 key exists).
8. **`B7.rule_N` with missing chains.** "qualified" if any available interval leaves (−0.05, 0.05); "holds" only if all eight are
   present and inside; otherwise null.
9. **Old-run B7 arrays** are not defined in the specification; see "Not done".
10. **`B.tuning` strings.** "depends" / "persists" as the specification (A's rule); package B's summary uses a sentence.

## Not done
- No B7 score on `p1b_fit_finite_0037`: the specification defines no old-run B7 arrays, and this program does not extract. The B7
  scoring path was tested on old tracker-variant arrays of the same format (stand-ins, file `TESTB7FMT_RC_TRK_v13*.json`, labelled),
  and the B7 (i) identity check was run on `p1b_fit_finite_0037`.
- The fresh path has not run (Lock 2 absent); only its refusal was tested. The fresh loaders (`fresh_cv0_lead`,
  `load_fresh_folder`, `fresh_capture_dir`) are therefore untested on real files; their format assumptions are those of the
  specification (§1–2) and of `CD_DEFINITIONS_v13.md` (meta keys `family`, `lead_variant`).
- No intervals for the phase rooms, the after-stop room or the lag (not keys). B7 `RR_CK3` intervals only with `--b7-ck3-ci`.
- No second extraction: arrays and B7 detections are shared, as A10 §10.1(b) allows.
