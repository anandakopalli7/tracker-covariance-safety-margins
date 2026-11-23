# Package C, A10 §5.6–5.7 additions ("S57A"): definitions for both programs

Written 20 Nov 2026, from 02:25 EST, by the first-program writer of package CD (Claude Opus 5.5), before any lock and before any value
of a fresh run exists. It fixes every choice that `..\..\AMENDMENT_10_v13.md` (A10) and the methods of record leave open for the keys
below. The independent second program implements the same keys from A10, the methods of record and this file (never from
`analysis\c_s57a_v13.py` or `analysis\x_s57a_extract_v13.py`). `CD_DEFINITIONS_v13.md` applies wherever this file is silent.
Changes are listed at the end, dated; none was made after a fresh value was seen (none has been computed).

**Scope (coordinator, 20 Nov 01:53 EST; applied here 02:40 EST).** This file and its programs produce only:
(1) the `.dec` / `.dec.ci` keys of §3; (2) the partial oracles and the grading check of §4; (3) the cut-in window shares of §5.
The reaction-and-stop ratio `LB.RS075.rel`, the B6 terciles (`LB.T<i>.*`, `LB.T.relmin/relmax`), the delayed stop (`LB.DS.*`), stop
reliance (`LB.REL_*`) and every `TU.*` key are **moved to package B** (§6–§9 below are kept only as headings). No key is written by both
packages.

## 0. Programs, gate, outputs
- First program: `analysis\x_s57a_extract_v13.py` (per-run cut-in inputs, §2) and `analysis\c_s57a_v13.py` (keys).
- **Gate (stage 2 of the two-stage Lock 2).** Neither program opens any fresh run, array (CV0, B1, S57A) or log unless BOTH
  `revision_v13\LOCK_A10_2.txt` and `revision_v13\LOCK_A10_2c.txt` exist: `cd_common_v13.require_lock2c(test_old)`, called before
  anything fresh is opened. The CV0/B1 arrays may exist after stage 1; they are not opened before LOCK_A10_2c.
  `--test-old` runs on old runs only (§10). The code is frozen in FREEZE_CD_2 before LOCK_A10_2c.
- **Output.** Fresh: `analysis\out\C_S57A_v13.json`; old-run test: `analysis\out\TESTOLD_S57A_v13.json`; short test record
  `analysis\out\TEST_S57A_v13.json`. Format: `{"family": "C_S57A", "program": "c_s57a_v13.py", "test_old": bool, "values": {<A key>:
  value}, "details": {...}}`. Unrounded numbers; shares as fractions of the room; decision-equivalents where the key says `.dec`;
  intervals `[lo, hi]`; `null` where undefined. For every interval key `X.ci` also `X.level` and `X.cal`: §3a fixes them (the `.dec.ci`
  of a calibrated statistic takes that statistic's level; everything else is nominal 95%). This program runs no double bootstrap.
- **Order.** The fresh run comes after the core import (`c_lead_v13.py --calib import` → `C_LEAD_H0_H5_v13.json`, `c_cutin_v13.py --calib
  import` → `C_CUTIN_K0_K2_v13.json`); it refuses if either file, or any level of §3a, is missing or still pending.

## 1. Run sets and the arrays read
- **Lead braking (LB)**: the 105 ids `c_run_ids('lead_braking')` of `CASES_C_v13.json` (with `REPLACEMENTS_C_v13.json` if it exists),
  `pc13_<case>_native`, **ascending run id**. **Cut-in (CI)**: the 105 cut-in ids, same rule.
  The run order of every draw (bootstrap rows, partial-oracle uniforms, permutations) is ascending run id.
- Arrays of `c_extract_v13.py` (`CD_DEFINITIONS_v13.md`): `arrays\CV0\<rid>.npz` (both families), `arrays\B1\<rid>.npz` (lead braking,
  the frozen IMM). Arrays of this package: `arrays\S57A\<rid>.npz` (cut-in only, §2).
- **Run dict** (as `trk_score_v01.make_run`): `desired = des[0]`, `idx55`, `clear1 = optA_lib_v02.clean_clear(clear)`, `vbar`,
  `ev = evaluated == 1`, critical scales `crit` = {F0: cF0, E: cE, N: cN, CK3: cCK3}.
- **Scoring**: the 3 s commitment only (W1: a row is safe iff `clear1 > 0`).
- **Gridless step frontier** (A10 §2.3, A9-1(c)): `a9_common_v01.gridless_sources(runs, names, safe_fn)` and `optA_lib_v02.eval_scoring`
  (equivalently `trk_score_v01.gridless` + `trk_score_v01.rr_gl`). F0 and E are the run set's own; every other source gets F0's g = 0
  point prepended; 201 levels `linspace(c_F0(0), min(max c_F0, max c_E), 201)`, rebuilt per population and per resample.
  D(A) = Σ_ℓ (F_F0 − F_A); room R = D(E)/201 (pp); RR(A) = D(A)/D(E) (NaN if D(E) ≤ 0 or not finite).
  **Decision-equivalents**: `dec_eq(D, n) = D / 201 / 100 · n`, n = the population's evaluated decisions (the weighted count in a
  resample).
- **Populations (lead braking)**, in this order: all (evaluated), mov (evaluated, v0 > 0.5 m/s), pre / brk / stop (evaluated, tracker's
  estimated phase 0 / 1 / 2 with `trk_score_v01.est_phase(vhat, ahat_long, lead_found, -1.0)`; A10 §2.4) = `cd_common_v13.masks_tracker_phase`.
  Each population is scored on its own frontier and its own levels.
- **Populations (cut-in)**: window = evaluated decisions with finite `rel` and −1 ≤ rel ≤ 4 s (closed); young = window and stratum '<1s'.
- **Bootstrap (fresh)**: `optA_lib_v02.boot_counts(n_runs, 20000, 20261911)` per run set (lead braking: the 105 lead runs; cut-in: the
  105 cut-in runs, event-less runs included with empty windows). Interval = `np.percentile(x[finite], [2.5, 97.5])`.
  Shares: resamples with D(E) ≤ 0 are NaN and excluded. Decision-equivalents: every resample is finite.

## 2. Per-run inputs written by `x_s57a_extract_v13.py`: `arrays\S57A\<rid>.npz` (cut-in runs only)
Logs: `runs\<rid>\<rid>\` (SUMMARY.json) and its single `capture\<case>\` folder (written by `c_extract_v13.py --logs-only`, LOGS_OK).
Every file holds `meta` (JSON string: run_id, kind, family, case, code, seconds, event) and `k` (= the CV0 arrays' `k`, asserted).
- Event and track age exactly as `c_cutin_v13.py` / `b9_cutin_v01.py` (`CD_DEFINITIONS_v13.md`, cut-in; threshold 1.75 m):
  `kc` (int64 scalar, −1 if no event), `rel` (n,) float64 = (k − kc)·0.05 s (all NaN without event), `stratum` (n,) unicode
  '<1s' | '1-4s' | '>=4s' | 'untracked', `spread` (float64, the ego's lateral spread over the run).
- Lead-braking runs need no extraction for these keys (moved to B: the delayed-stop clearances and realised decelerations).

## 3. Decision-equivalent versions (`.dec`, `.dec.ci`) of printed shares
Each `X.dec` is the share's numerator in decision-equivalents, on the same population, frontier and resamples as the share:
| Key | Value |
|---|---|
| `LB.R.dec` | dec_eq(D(E), n), all (point; no `.ci` key) |
| `LB.RR_N.dec`, `LB.RR_E5.dec`, `LB.RR_CK3.dec` | dec_eq(D(A), n), A = N, E5, CK3, all |
| `LB.RR_E5mP.dec` | dec_eq(D(E5) − D(E5p), n) on the same resample |
| `LB.IMM.r.dec`, `LB.IMM.c.dec` | on the B1 arrays (IMM's own F0_IMM, E_IMM, all): dec_eq(D(N_IMM)), dec_eq(D(E5_IMM)) |
| `LB.PS.rec.dec` | dec_eq(Σ_ℓ (F_F0 − F_ps→C), n) on the fresh grid frontiers: the numerator of H4's record-basis share |
| `CI.RR_N.dec` | dec_eq(D(N), n_window), event window |
| `CI.Y.R.dec` | dec_eq(D(E), n_young), young-track population, point; **0 when the population is empty** (no decision, no room; as `c_cutin_v13` K2) |
- E5, E5p, E5_IMM exactly as `CD_DEFINITIONS_v13.md` (C, lead braking): u = `e5_u(runs, 'F0', 'E')` over the run set's evaluated
  decisions; E5 = `add_oracle(F0, 1.1029, 0.05, u)`; E5p with `permute_u(runs, u, 20261915)`; E5_IMM = `add_oracle(F0_IMM, m_IMM,
  A_IMM, e5_u(F0_IMM, E_IMM))` with m_IMM = median and A_IMM = A of `ratio_summary(margin_ratios(N_IMM, F0_IMM))`.
- PS: the design choice (triple and single scale) is `c_lead_v13`'s: the 35 old evaluation runs, tracker-phase tables (thr −1.0),
  `triple_choice` / `single_choice` at the design levels; the transfer and the fresh step frontiers as `cd_common_v13.H4Stat.share`
  (grid of record, fresh levels rebuilt per resample); n = the fresh runs' evaluated decisions (weighted in a resample). No re-selection.
- Intervals: the 20,000 resamples of §1, at the levels of §3a.

## 3a. Levels of the `.dec.ci` intervals (coordinator decision, 20 Nov ~03:30 EST; A's interface §1)
Every `X.dec.ci` of a calibrated statistic X uses X's own level, read from the core output, with `X.dec.level` = that level and
`X.dec.cal` = X's cal:
| `.dec` key | level read from (fresh: `analysis\out\…`; tests: the `TESTOLD_` version) |
|---|---|
| `LB.RR_N.dec`, `LB.RR_E5.dec`, `LB.RR_E5mP.dec`, `LB.RR_CK3.dec` | `C_LEAD_H0_H5_v13.json` `calibration_main` `RR_N` / `RR_E5` / `RR_E5_minus_E5p` / `RR_CK3` |
| `LB.IMM.r.dec`, `LB.IMM.c.dec` | `C_LEAD_H0_H5_v13.json` `H3.calibration` `r` / `c` |
| `LB.PS.rec.dec` | `C_LEAD_H0_H5_v13.json` `H4.calibration.share_record` |
| `CI.RR_N.dec` | `C_CUTIN_K0_K2_v13.json` `K0.calibration.RR_N` |
- `cal` from the entry's `rule` (cd_common_v13.calibrated_levels): rule beginning "calibrated" → "calibrated"; level 0.99 → "nominal99";
  level 0.95 (rule "nominal 95%…") → "nominal95". A pending entry (export mode) or a missing entry: the fresh run refuses.
- Interval at level ℓ: `np.percentile(x[finite], [a, 100 − a])`, a = 100·(1 − ℓ)/2, exactly as `cd_common_v13.interval` forms the share's
  `ci_level` (so at ℓ = 0.95 a = 2.5000000000000022, as there).
- Descriptive keys (partial oracles, `CI.RR_CK3/RR_E5/RR_E5mP`, populations) stay nominal 95% (`[2.5, 97.5]`, `optA_lib_v02.pct`).
- Old-run test: the old-run core output has no H3 (no B1 arrays under CD's arrays for old runs), so `LB.IMM.*.dec.ci` fall back to nominal
  95% there, and say so in `details.dec_ci_levels`; the fresh run never falls back.

## 4. Partial oracles and the grading check (A10 §2.2, §5.7, C3)
- **Construction (of record: rev_g_partial_oracle_draws_v01 / optA add_graded)**: one uniform per stored decision (every decision in
  the arrays, evaluated or not), u = `default_rng(20261919).random(N_total)`, assigned in ascending run id and, within a run, in k order;
  the partial oracle with share p ∈ {0.25, 0.5, 0.75} takes E's critical scales where u < p and F0's elsewhere:
  `crit_Pp = where((u < p)[:, None], cE, cF0)`.
  - Lead braking: one draw over the 105 lead runs (N_total = all their decisions).
  - Cut-in: a separate generator with the same seed, `default_rng(20261919).random(N_total_cutin)` over the 105 cut-in runs.
- **Share**: PO_p = RR_gl(P_p) = D_gl(P_p, F0) / D_gl(E, F0), 3 s commitment, gridless step frontier (primary, A10 §2.3), each
  population on its own frontier: `LB.<pop>.PO25/50/75` for pop ∈ {all, mov, pre, brk, stop}; `LB.PO<p>` = `LB.all.PO<p>`;
  `CI.PO<p>` in the event window. Points only (no interval). Undefined (D(E) ≤ 0) → null.
- **Grading check** `<prefix>.grading_ok` (bool): PO25 > 0 and PO25 < PO50 < PO75 (strictly); false if any is null.
  Keys: `LB.grading_ok` (= `LB.all.grading_ok`), `LB.all/mov/pre/brk/stop.grading_ok`, `CI.grading_ok`.
- The grid-frontier versions (grid of record `[0] + logspace(-2, 3, 201)`, `select_grid`, `stats_scored`) are in `details` only.

## 5. Cut-in window shares (`CI.RR_CK3`, `CI.RR_E5`, `CI.RR_E5mP` and their `.ci`)
- u = `e5_u(runs, 'F0', 'E')` over **all evaluated decisions of the 105 cut-in runs** (the run set's evaluated decisions, A10 §2.2;
  as K2's u). E5 = `add_oracle(F0, 1.1029, 0.05, u)` (the E5 of record, as H1); E5p = the same with `permute_u(runs, u, 20261915)`
  (u permuted within each run among its evaluated decisions; one generator, runs in ascending id).
- Scored in the **event window** population only (gridless, W1, the window's own frontier): RR(CK3), RR(E5), RR(E5) − RR(E5p) (same
  resample). Intervals: §1, cut-in bootstrap, nominal 95%.

## 6. Reaction and stop at 0.75 s (`LB.RS075.rel`) — moved to package B
## 7. B6 terciles and delayed stop (`LB.T<i>.*`, `LB.T.relmin/relmax`, `LB.DS.*`) — moved to package B
## 8. Stop reliance (`LB.REL_F0/N/CK3`) — moved to package B
## 9. Tuning runs (`TU.*`) — moved to package B

## 10. Old-run tests (`--test-old`; nothing fresh is read)
- LB stand-in: the 35 old evaluation runs (`cd_common_v13.load_old_lead()`; tracker phase from v12's lead extract); B1 =
  `B_retrack\out\retrack\B1\<run>_arrays.npz`.
- CI stand-in: the 20 cut-in tuning runs (stored gateR arrays, as `c_cutin_v13 --test-old`; cCK3 from package B's CV0 re-track arrays
  `B_retrack\out\retrack\CV0\<run>_arrays.npz`, accepted only if their k equals the stored k and cF0, cE, cN equal the stored ones within
  1e-12 relative (|b − z| ≤ 1e-12·max(1, |z|); observed ≤ 1.1e-14) with equal finite patterns; events from their logs via
  `x_s57a_extract_v13.py --set test_cutin`). On these 20 runs the window room is 0 (no young-track decision at all), so every CI share is
  undefined there; the cut-in code path is therefore also run on the 35 old lead runs with window = all evaluated decisions, where it
  must reproduce the LB values exactly (self-check).
- Draws: bootstrap of record `boot_counts(n, ·, 20261113)`; the partial-oracle draw of record is `default_rng(20261118).random(9307)`
  (rev_g, A9-8; 20261113 is the bootstrap draw, not the partial-oracle draw); consistency with `TESTOLD_C_LEAD_H0_H5_v13.json` uses
  `boot_counts(35, 200, 20261911)` (its draw). The CI partial oracles in the test use 20261919 (no value of record exists).
- Result (20 Nov 03:50 EST, 20,000 resamples): 60 of 60 checks agree (`analysis\out\TEST_S57A_v13.json`); the fresh paths refuse with
  stage 1 present and LOCK_A10_2c absent (`analysis\out\TEST_S57A_v13_gate.json`).

## 11. Open choices (stated, not resolved by A10)
1. (Resolved 20 Nov ~03:30 EST by the coordinator: §3a.)
2. Partial oracles: gridless primary (A10 §2.3), grid in details; populations by the tracker's phase.
3. Cut-in E5: ranks over all evaluated cut-in decisions, not only the window's; the score is restricted to the window.
4. `CI.Y.R.dec` = 0 for an empty young-track population.

## Changes
- 20 Nov 02:25 EST: first version (all keys of the brief).
- 20 Nov 02:40 EST: scope change of the coordinator (01:53 EST): §6–§9 moved to package B; §2 reduced to cut-in runs; §0 gate also
  requires LOCK_A10_2c. No definition of a remaining key changed.
- 20 Nov ~02:50 EST: gate = `cd_common_v13.require_lock2c` (both lock files in `revision_v13\`; coordinator's gate change). The earlier code is kept as `analysis\superseded_*_before_scope_change.txt`.
- 20 Nov ~03:35 EST: §3a (levels of the `.dec.ci` keys of calibrated statistics; coordinator decision); §0 order (after the core import).
