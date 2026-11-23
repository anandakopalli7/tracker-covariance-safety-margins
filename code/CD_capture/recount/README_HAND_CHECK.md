# Hand-check subset of A10 §10.2 (S10): `hand_check_v13.py`

Written 20 Nov 2026, 02:40 EST (Claude Fable 5.2), before `revision_v13\LOCK_A10_2.txt` and before any fresh-run value existed.
Every rule below is fixed now. Tested on the 35 old evaluation runs only.

## What A10 §10.2 asks
- 20 evaluated fresh lead-braking decisions (`default_rng(20261917)`), stratified 7/7/6 by truth phase.
- The true clearance of F0's selection at g = 1 is computed by a new routine without the scoring library.
- Tolerance 1e-6 m. The cases are tabulated. A's key: `HAND.status`.

## Selection rule
- **Runs:** the 105 fresh lead-braking runs `pc13_<case>_native` (lead_braking rows of `CASES_C_v13.json`, with any reported
  replacement; `cd_common_v13.c_run_ids('lead_braking')`), in ascending run id.
- **Candidates of truth phase p** (p = 0 before the lead's braking onset, 1 braking, 2 stopped; `phase` of the arrays, CD_DEFINITIONS):
  the decisions with `evaluated == 1` and `phase == p`, ordered by (run id, decision index in the run's array = ascending tick k).
  Decisions with phase 3 (undefined) are not candidates.
- **Draw:** one generator `numpy.random.default_rng(20261917)` for the whole draw. For p = 0, 1, 2 in this order:
  `rng.choice(n_p, size, replace=False)` with size 7, 7, 6, where n_p is the number of candidates of phase p. The drawn indices are
  sorted ascending within the phase; cases are numbered 1–20 in that order (phase 0 first).
- **Shortfall** (not expected): a phase with fewer candidates than its size contributes all of them (`rng.choice(n_p, n_p,
  replace=False)`); the shortfall is reported and `HAND.status` then names fewer than 20 cases. No other phase is enlarged.
- The selection uses `k`, `evaluated` and `phase` of the arrays of record (`arrays\CV0\<rid>.npz`). Nothing else of the arrays enters
  the new routine.

## The new routine (PART N of the script; imports `json`, `math`, `numpy` only)
It calls none of `optA_lib_v02`, `a9_common_v01`, `rev_common_v01`, `trk_score_v01`, the gateR / `ol_*` / `ox*` extraction code,
`c_extract_v13`, or the planner modules (`consumer`, `finite_primitive`, `design_core_v85`). The methods of record were read only for
the definitions. Per selected decision (run, tick k):

1. **Decision record** — `frames.jsonl`, the line with this k, `execution.new_decision` (mode `assessment`): model speed and
   acceleration, desired speed, decision time `now`, ego length and width, and the tracked actors (position, velocity, yaw, length,
   width, state time, class name).
2. **Row library** — the 17 candidate rows are rebuilt from the model state: 16 pairs of acceleration targets from {−5, −2, 0, 2} m/s²
   (first second, then the rest), plus the state-dependent row; acceleration slewed at 8 m/s³, speed limited to [0, 20] m/s, 60 steps
   of 0.05 s; rows sorted by the planner's cost, then by target pair. The fallback row is the pair (−5, −5).
3. **F0's critical scale per row** — the largest g with d ≥ 0 and g·s ≤ d² at every constraint (per tracked actor: 60 segments × 2
   end points):
   - d = the planner's nominal distance (separation along the constraint normal − both half supports − the reserve);
   - s = z′ P̄ z with z = [n, n·tₑ], P̄ the class-average covariance of record
     (`P\09_redesign\m2_decisions\openloop\pbar_tuning_v01.json`, key `Pbar`, class `pedestrian` or `vehicle`), floored at 0;
   - −∞ if some d < 0; +∞ if no constraint has s > 0.
4. **Selection at g = 1** — the first row in cost order whose critical scale is ≥ 1; if there is none, the fallback row.
5. **True clearance of that row** — from `evaluation_truth.jsonl`: the smallest distance, over the 61 plan ticks j = 0…60 and over
   every true scenario actor, between
   - the ego box: the true ego centre at tick k moved by the row's s_j along the route yaw (`route_yaw_rh`), with the logged ego
     length and width, and
   - the actor's true box at tick k + j (`center_rh`, `heading_rh`, `half_extents`).

   Box distance: 0 when the boxes overlap or touch, else the smallest corner-to-edge distance. This is the scored clearance (`clear`).
   The clearance to the lead alone (the truth log's `target`) and the number of true actors are tabulated beside it; in a
   lead-braking run the lead is normally the only scenario actor, and the table counts the cases where the two differ.
6. The routine also states whether the decision is evaluated by its own reading of the truth log (lead present at tick k and 60 true
   ticks after it); the table shows it.

## Reference (PART R)
- Fresh runs: `arrays\CV0\<rid>.npz` (`cF0`, `idx55`, `clear`). Old runs: `cd_common_v13.load_old_lead()` (the gateR_rt_v01 arrays of
  record).
- F0's selection at g = 1: `optA_lib_v02.select_grid(cF0, [1.0], idx55)`; reference clearance = `clear[decision, selected row]`.

## Comparison and output
- Per case: |new − reference| ≤ 1e-6 m (two infinite clearances of the same sign count as equal). A case whose rows differ is
  judged by its clearances, as A10 says; the table shows both rows and the count of equal rows.
- `HAND.status` = "all 20 within 1e-6 m", or "k of 20 within 1e-6 m".
- `recount\out\HAND_CHECK_v13.json`: `{"family": "lead_braking", "program": "hand_check_v13.py", "test_old": false, "values":
  {"HAND.status": ...}, "details": {...}}`; `details.table` has, per case: run, decision index, k, truth phase, row by each, the two
  clearances, the difference, F0's critical scale of the selected row by each, the lead-only clearance, actor counts.
- A log is written beside it (`HAND_CHECK_v13_log.txt`). Outputs are never overwritten (`--tag T` gives a new name).
- A disagreement is investigated in the routine, never by changing the reference; both versions and the cause are recorded.

## Commands (from `work\CD_capture`; `PY = .venv\Scripts\python.exe -I -B -X utf8`, `OPENBLAS_CORETYPE=Haswell`)
- Fresh (after Lock 2 and after `arrays\CV0\` and `runs\` exist for all 105 runs): `PY recount\hand_check_v13.py` (about 1 min).
  Refused without `revision_v13\LOCK_A10_2.txt`.
- Test on old runs: `PY recount\hand_check_v13.py --test-old [--tag T]`.

## Test on the old runs (20 Nov 2026, 02:40 EST) — a test, not a result
- Same procedure and seed on the 35 old evaluation runs `p1b_fit_finite_0005…0039` (logs: `P\07_fit_runs\archives\<run>\x\<run>\
  capture\<case>\`). Candidates by truth phase 0/1/2: 678 / 755 / 6,857.
- `recount\out\TESTOLD_HAND_CHECK_v13.json`: all 20 within 1e-6 m; the largest difference is 0 m (equal to the last bit); the same
  row in 20 of 20; 5 of the 20 clearances are 0 (contact); the selected rows are 0, 1, 3, 4, 5, 6 and 16. (`..._dev1.json` is the first run, identical table.)
- Wider development check, not stored (360 evaluated decisions of 6 old runs, generator seed 1; 54 of them fallback selections):
  the same row in 360 of 360; largest clearance difference 3.6e-15 m; F0 critical scales of all 17 rows agree within 1.7e-14
  relative; the routine's evaluated flag equals the arrays' on every decision of those runs.
- Not testable before Lock 2: the fresh layout (`runs\<rid>\<rid>\capture\<case>\`, `arrays\CV0\<rid>.npz`) is read only by the
  fresh path, which has not run.
