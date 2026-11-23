# Package B on the fresh lead-braking runs: definitions for both programs (v02)

Written 20 Nov 2026, ~02:10 EST (this machine's clock), by the package-B session (Claude Opus 5.5), before Lock 2, for the
coordinator's task of 20 Nov (A10 §5.7 fixed sensitivities: "Variants B2–B4; B1's transition sensitivities; the ceilings E5_x;
the margin-ratio check for every variant"; and the B3/B4 rule inputs on fresh runs, A10 §3 B3 row, "fresh (descriptive)").
Status of every value: **descriptive** (A10 §5.7). No hypothesis, no calibration.

The first program (`code\b_fresh_*_v02.py`) and the independent second program (`recount_fresh\`) implement this file, A10 §2–§3
and `B_ANALYSIS_DEFINITIONS_v01.md`. Where this file is silent, `B_ANALYSIS_DEFINITIONS_v01.md` applies unchanged.

## 1. Lock gate
No program reads a fresh run's arrays or logs unless `revision_v13\LOCK_A10_2.txt` exists. Every program has a test mode on the
35 old evaluation runs (`--test-old`), which never reads a fresh run.

## 2. Run sets, trackers and inputs
| Name in keys | Variant | Fresh arrays (105 runs) | Old arrays (test mode, 35 runs) |
|---|---|---|---|
| CV | CV0 (online CV of record) | `CD_capture\arrays\CV0\<rid>.npz` | `B_retrack\out\retrack\CV0\<run>_arrays.npz` |
| IMM | B1 (IMM, diagonal 0.95) | `CD_capture\arrays\B1\<rid>.npz` | `...\retrack\B1\<run>_arrays.npz` |
| CV2 | B3 (CV re-tuned) | `B_retrack\out\retrack_fresh\B3\<rid>_arrays.npz` | `...\retrack\B3\<run>_arrays.npz` |
| CA | B4 (CA) | `...\retrack_fresh\B4\<rid>_arrays.npz` | `...\retrack\B4\<run>_arrays.npz` |
| AQ | B2 (adaptive Q) | `...\retrack_fresh\B2\<rid>_arrays.npz` | `...\retrack\B2\<run>_arrays.npz` |
| IMM090 | B1_d090 | `...\retrack_fresh\B1_d090\<rid>_arrays.npz` | `...\retrack\B1_d090\<run>_arrays.npz` |
| IMM098 | B1_d098 | `...\retrack_fresh\B1_d098\<rid>_arrays.npz` | `...\retrack\B1_d098\<run>_arrays.npz` |

- **Fresh run ids:** the lead-braking cases of `CD_capture\CASES_C_v13.json`, each replaced by its replacement if
  `CD_capture\REPLACEMENTS_C_v13.json` lists one, as `pc13_<case>_native`, sorted ascending (105). This order is the run order of
  every resample.
- **Old run ids (test mode):** `p1b_fit_finite_0005` … `p1b_fit_finite_0039`, in that order.
- Every arrays file has the keys of `trk_arrays_v01.extract` (lead and A4 keys): `k`, `evaluated`, `clear`, `vbar`, `idx55`, `des`,
  `v0`, `now`, `phase` (truth phase: 0 before onset, 1 lead moving after onset, 2 stopped), `cF0`, `cE`, `cN`, `cCK3`, `vhat`,
  `ahat_long`, `lead_found`, `dx_pred3`, among others. F0_x, E_x, N_x, CK3_x are x's own (`cF0` uses P̄_x, A10 §2.1).
- The fresh arrays of CV2, CA, AQ, IMM090, IMM098 are made by re-tracking CD's extracted logs
  (`CD_capture\runs\<rid>\<rid>\capture\<case>\`, after `runs\<rid>\LOGS_OK`) with the frozen library: `retrack_capture(cap, x)`,
  overlay, `extract(rd, cap, P̄_x, lead=True, a4=True)` with `P̄_x` = `B_retrack\out\pbar\PBAR_<x>_v01.json` (as for the old runs).

## 3. Scoring (as of record)
3 s commitment: a row is safe if its cleaned true clearance (`optA_lib_v02.clean_clear(clear)`) is > 0. Evaluated decisions only.
Gridless step frontier on 201 caution levels (A10 §2.3, A9-1(c)); D_gl(A, B) and RR_gl(A) = D_gl(A, F0_x) / D_gl(E_x, F0_x), each on
x's own room. Room R_gl in pp = D_gl(E_x, F0_x) / 201; in decision-equivalents = D_gl(E_x, F0_x) / 201 / 100 · n (n = decisions in
the population).

## 4. Populations
- **all**: all evaluated decisions.
- **pre / brk / stop**: x's estimated phase (A10 §2.4, threshold −1.0 m/s², from x's `vhat`, `ahat_long`, `lead_found`):
  stop if lead_found and vhat ≤ 0.5; brk if lead_found, vhat > 0.5 and ahat_long ≤ −1.0; pre otherwise.
- **after-stop**: truth phase 2 (lead stopped), as of record for the B3/B4 rule.

## 5. Quantities and keys (prefix `B.<name>.`, name from §2)
| Key | Quantity |
|---|---|
| `R`, `R.ci` | R_gl (pp), all |
| `R.dec` | R_gl in decision-equivalents, all |
| `RR`, `RR.ci` | RR_gl(N_x), all |
| `c`, `c.ci` | c_x = RR_gl(E5_x), all (A10 §2.2: m_x, A_x from the scored run set; ranks u_i from F0_x / E_x over its evaluated decisions) |
| `RR_minus_c`, `RR_minus_c.ci` | RR_gl(N_x) − RR_gl(E5_x) on the same resamples |
| `RR_CK3`, `RR_CK3.ci` | RR_gl(CK3_x), all |
| `m`, `A`, `q05`, `q95`, `within5`, `barely` | margin ratio √(c_F0x / c_Nx) at the binding rows (as `B_ANALYSIS_DEFINITIONS_v01.md`): median, A_x, quantiles, share within 5% of the median, barely varies (within5 ≥ 0.95) |
| `class` | the H3 wording applied descriptively to (RR, c) with δ = 0.05 ("recovers" / "uninformative variation" / "amplitude-limited" / "inconclusive") |
| `room_pre`, `room_brk`, `room_stop` | R_gl (pp) in x's estimated-phase populations |
| `as_room` | after-stop room: R_gl in decision-equivalents, truth phase 2 |
| `as_room.pp` | the same in pp |
| `lag` | median over evaluated truth-phase-2 decisions in the first second after the run's first truth-phase-2 decision (0 ≤ t − t_stop < 1 s, t = `now`) of x's `dx_pred3` (finite values, pooled over runs), with `lead_found` |
| `n_dec`, `n_runs` | evaluated decisions, runs |

**B3/B4 rule (A10 §3, fresh, descriptive):** `B.rule.CV2` and `B.rule.CA`, each {as_room_below_half: as_room_x < 0.5 · as_room_CV,
ck3_differs: |RR_CK3_x − RR_CK3_CV| > 0.10}; `B.rule.outcome` = "depends on filter tuning" if any is true, else "mechanism persists".

## 6. Intervals
- **Fresh:** `numpy.random.default_rng(20261911).integers(0, 105, (20000, 105))`, counts per run (`optA_lib_v02.boot_counts(105, 20000,
  20261911)`), runs in the order of §2. Percentile 95% (`[2.5, 97.5]`), over resamples with D_gl(E_x, F0_x) > 0 for shares.
  m_x, A_x and the ranks u_i stay at their full-sample values in every resample (as of record for the old runs).
- **Test mode (old runs):** the first 2,000 rows of `default_rng(20261113).integers(0, 35, (20000, 35))` (the draw of record).
- **Per-resample values** are saved by both programs (`denE`, `n`, `D_N`, `D_E5x`, `D_CK3`, one row per resample, in draw order) so the
  comparison can check them row by row.

## 6b. B6 and the stop reliance on the fresh runs (coordinator, 20 Nov ~01:53: LB.RS075, terciles, DS, REL; online tracker of record)
Port of `b6_stop_v01.py` (B6 of record for B) and of revision_v12 `a9_6_stop_reliance_v01.py` part (1). Online tracker CV0 only:
`CD_capture\arrays\CV0\<rid>.npz` (crit cF0, cE, cN, cNA, cA1 (AM), cCK3, cQ; P̄ of record). Population: all evaluated decisions.
- **Scorings (changed ~03:40, before any value: agreed with package CD; A10 §1 "the reaction-and-stop scoring, with plans judged
  until the stop ends").** W1: clean clearance > 0 (3 s commitment). W_R: reaction and stop, τ = 0.75 s, A = 6 m/s², **judged until the
  stop ends**: clean `clearX_t0p75_a6p0` > 0 — fresh: CD's `CD_capture\arrays\RSX\<rid>.npz` (CD's port of revision_v11
  rev_e1_extended_truth_extract_v01); test: `revision_v11\analysis\out\ext\<run>.npz`. DS: τ_i = 0.75 + δ_i,
  δ_i = `default_rng(20261916).uniform(0, 0.75, n)` drawn once over all evaluated decisions, runs in the order of §2, decisions in k
  order; A = 6 m/s²; also judged until the stop ends (rev_e1's continuation with the stop started at τ_i, also inside a step);
  clearances computed by the first program (`b_stop_ext_v02.py`; fresh `out\fresh_b6\clear\<rid>.npz`, test
  `out\fresh_testold\b6_clear_ext\<run>.npz`; key `clear` = the extended clearance, plus clear61, tstop, jend, late, cens, tau, k).
  Its identity on old runs: with τ = 0.75 everywhere it reproduces v11 out\ext clearX_t0p75_a6p0, and its 61-frame part reproduces
  the delayed clearances of b6_stop_v01. The second program recomputes the τ draw, checks it against the stored tau, and recounts
  the scoring. Caution is always counted under the 3 s commitment (as of record). O = the scoring's perfect oracle (first safe row).
  The 61-frame scoring (stop cache of record; B6 v01) is kept only as an old-run test of the code path ("horizon").
- **LB.RS075.rel** = R_gl(W_R) / R_gl(W1) on all runs; **.ci** from the same resamples (per resample D_gl(E,F0) under W_R over that under
  W1; resamples with W1 room ≤ 0 dropped).
- **Terciles**: realised lead deceleration per run (`trk_score_v01.realised_decel` rule = rev_h_run_facts_v01: minus the least-squares
  slope of the true lead speed between 90% and 10% of its pre-brake speed); ascending, ties by id, `numpy.array_split` into three
  (35/35/35). Per tercile i on its own frontier: **LB.T<i>.rel** = R_gl(W_R) / R_gl(W1); **LB.T<i>.den0.dec** = D_gl(F0, O) under W_R in
  decision-equivalents; **LB.T<i>.evaluable** = den0 ≥ 10; **LB.T<i>.range** = "%.2f–%.2f" of its realised decelerations (m/s²).
  **LB.T.relmin / LB.T.relmax** = min / max of rel over the evaluable terciles (absent if none).
- **LB.DS.rel** = R_gl(DS) / R_gl(W1), **.ci** as RS075; **LB.DS.den0.dec** = D_gl(F0, O) under DS in decision-equivalents.
- **LB.REL_F0, LB.REL_N, LB.REL_CK3** (stop reliance, A9-6 (1)): under W_R, on the **grid** frontier (202-value grid of record), at each
  of the 201 levels each source's frontier operating point (the point attaining the step frontier; point 0 of N or CK3 is F0's
  zero-margin point); the share of all evaluated decisions whose selected row is unsafe under W1 but safe under W_R, averaged over
  the levels. (Old-run check: with v11's extended clearance this reproduces revision_v12 `A9_6_STOP_RELIANCE_v01.json`.)
- Intervals: the fresh draw of §6 (all 105 runs) for RS075.rel and DS.rel. Only points are exported for the terciles; their own
  intervals in the JSON use `boot_counts(n_tercile, 20000, 20261911)` over the tercile's runs (as b6_stop_v01 did with its seed).

## 6c. TU: the 20 lead-braking tuning runs (A10 §5.6; old data, no lock)
Online tracker of record on the 20 lead-braking tuning runs listed by `P\11_ojits\A4\dryrun\extract\*.npz` (name order):
crit cF0, cE, cN from the stored arrays of record (`P\09_redesign\m2_decisions\openloop\gateR_rt_v01\<run>.npz`), cNA, cA1 (AM),
cCK3, cQ and the truth phase from the A4 tuning extraction; the tracker-estimated phase from the lead keys of B's CV0 replay
(`B_retrack\out\retrack\CV0\<run>_arrays.npz`, matched on k). Gridless (primary): **TU.R** (pp), **TU.R.ci**, **TU.RR_<src>** and
**.ci** for src in N, NA, AM, CK3 (Q in the JSON), **TU.R_pre / R_brk / R_stop** (pp, estimated phase). Intervals:
`optA_lib_v02.boot_counts(20, 20000, 20261918)`. Grid points beside (must equal revision_v12 `A9_5_TUNING_RUNS_v01.json`).
TU.RR_TG is not computed (supplement).

## 6e. TU.RR_TG (added 21 Nov 2026 ~02:35 EST, coordinator request; recorded in FREEZE_B_add4)
A10 §5.6 lists TG among the tuning-run shares: "TG's tuning-run arrays rebuilt by the A9-7 method with its identity check".
- **TG critical scales** on the 20 tuning runs of §6c: for every constraint of every planner row (rows rebuilt from the logged
  decision), s = (r0 + v_e)², v_e = the row's speed at the constraint's sample (column j < 60 of an actor block at sample j, column
  60 + j at sample j + 1), critical scale = the planner's crit_rows(D, s); r0 = 2 m/s (primary). First program: package CD's frozen
  `c_extract_v13.tg_arrays`, written to `B_retrack\out\tu\tg\<run>.npz` (k, cTG1, cTG2, cTG4); the second program may read these
  shared extracted arrays (A10 §10.1(b)). **Identity check:** the class-average critical scales recomputed from the same rows and
  geometry with the P-bar of record equal the stored cF0 of record (gateR_rt_v01) in every cell (0 differing cells per run).
- **Keys:** `TU.RR_TG` = RR_gl(TG) = D_gl(TG, F0) / D_gl(E, F0), all evaluated decisions of the 20 runs, gridless step frontier
  (TG's point 0 = F0's zero-margin point, as for every source other than F0 and E); `TU.RR_TG.ci` = 95% percentile interval over
  `optA_lib_v02.boot_counts(20, 20000, 20261918)` (resamples with D_gl(E, F0) > 0), as the other TU shares. Grid RR(TG) beside in the
  JSON (not exported). All other TU values unchanged.
- **Old-run check available:** v12 A9-7 (revision_v12 `out\tg\<run>.npz` cTG2 and its scoring output) on the 35 old evaluation runs.

## 7. Outputs
- First program: `B_retrack\out\fresh\B_FRESH_<variant>_v02.json` (all quantities), `out\fresh\boot_<variant>.npz`, and the flat
  export `B_retrack\out\A_EXPORT_B.json` ({key: value}; intervals as [lo, hi]).
- Second program: `B_retrack\out\A_RECOUNT_B.json` (same flat keys) and its per-resample arrays in `recount_fresh\out\`
  (named by key name: `boot_<CV|CV2|CA|IMM|AQ|IMM090|IMM098>.npz`, `boot_b6.npz`, `boot_tu.npz`; test mode prefixed `testold_`).
  Its fresh output also carries the lock files' SHA-256 (`B.lock_sha256`, provenance, not compared).
- Comparison: counts exact; points and per-resample values within 1e-9 (relative to max(1, |value|)); interval ends within 1e-9 where
  both have all 20,000 resamples; strings equal.
