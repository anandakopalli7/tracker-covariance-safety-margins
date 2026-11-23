# Package C, lead braking: definitions of the supplement sensitivities of A10 §5.7 (S57B keys) for the second program

Written 20 Nov 2026, 02:25 EST, by the first-program writer of S57B (Claude Opus 5.5, `claude-opus-5-5`), before any value of a fresh
run exists (`LOCK_A10_2.txt` does not exist; no file under `arrays\`, `runs\` or `archives\` was opened). Revised as marked below; every
revision is dated and was made before any fresh value. It adds to `CD_DEFINITIONS_v13.md` (which still holds) and to
`..\..\AMENDMENT_10_v13.md` (A10). A second program is written from A10, the methods of record named here and this file, never from
`analysis\c_s57b_v13.py` or `analysis\x_rsx_extract_v13.py`.

First programs: `analysis\x_rsx_extract_v13.py` (per-run RSX arrays; named by the CD lead on 20 Nov, about 02:50 EST, replacing the
planned `x_s57b_extract_v13.py`, which was never run on fresh data and is deleted) and `analysis\c_s57b_v13.py` (keys). Both are
**stage-2** programs of the two-stage Lock 2: their fresh paths refuse unless both `LOCK_A10_2.txt` and `LOCK_A10_2c.txt` exist
(`cd_common_v13.require_lock2c`); before that they never open a fresh CV0 / B1 array or run folder.
Output: `analysis\out\S57B_v13.json` (fresh) / `analysis\out\TESTOLD_S57B_v13.json` (old runs), format of `export\BRIEF_COMMON_v13.md`.

## 0. Keys (those of `export\A_KEYS_CD_v13.json`; 172 computed, 170 in the key list of 03:29, plus `.level` / `.cal` beside every `.ci`)
| Group | Keys |
|---|---|
| 1 By population | `LB.<pop>.{n_dec, R, R.ci, RR_<src>, RR_<src>.ci}`, pop ∈ all, mov, pre, brk, stop; src ∈ AM, CK3, E5, IMM, N, NA, Q, TG |
| 2 Reaction and stop | `LB.RS.<tau>.6.{rel, rel.ci, den0.dec, RR0_N, RR0_N.ci, RR0_CK3}`, tau ∈ 0.5, 0.75, 1.0, 1.25, 1.5, 1.8; `LB.RS.0.75.<A>.{rel, den0.dec, RR0_N, RR0_CK3}`, A ∈ 4, 5, 7.6; `LB.gap2.{den0.dec, RR0_N, RR0_CK3}` |
| 3 After-stop truncation | `LB.T<T>.{R, RR_CK3}`, T ∈ 0, 1, 2, 5, 10, 20; `LB.cut5.{R, RR_CK3}` |
| 4 Caution | `LB.cap5.R`, `LB.cap10.R`, `LB.cap15.R`; `LB.signed.{R, RR_N, RR_CK3}` |
| 5 Grid and hull | `LB.grid.{RR_N, RR_P, RR_NmP}`; `LB.hull.{R, RR_N, RR_CK3}` |

The program reads the key list at run time and writes into `values` only keys that are in it; anything else it computes goes to
`details.values_not_in_key_list` (revision 20 Nov 03:40 EST: the key list of 03:29 no longer holds `LB.RS.0.75.6.rel` and
`LB.RS.0.75.6.rel.ci`, which A's `gen\rename_v13.json` maps to package B's `LB.RS075.rel`; this program still computes them, as the
cross-check that the two agree, and keeps them in `details`; 170 keys are then in `values`).

Not produced here (other writers): `LB.<pop>.PO25/50/75`, `LB.T1/T2/T3.{rel, range, den0.dec, evaluable}` (terciles), `LB.DS.*`,
`LB.RS075.rel(.ci)`, `LB.REL_*`. The tau string in a key is the decimal as listed (`0.5`, `0.75`, `1.0`, `1.25`, `1.5`, `1.8`); A as
`4`, `5`, `6`, `7.6`.

Units (BRIEF_COMMON): R in percentage points (D/201); shares as fractions; `den0.dec` in decision-equivalents; intervals `[lo, hi]`;
`null` where undefined (a share whose denominator is not > 0; a capped room whose window is empty). Every `.ci` has `.level` = 0.95 and
`.cal` = "nominal95" (descriptive, A10 §5.7; no calibration).

## 1. Inputs
- **Run set**: the 105 C lead-braking runs, `cd_common_v13.c_run_ids('lead_braking')` (ascending run id; that order is the run order of
  every resample).
- **CV0 arrays** `arrays\CV0\<rid>.npz` (`c_extract_v13.py`; keys in `CD_DEFINITIONS_v13.md`): `k, evaluated, v0, des, clear, vbar,
  idx55, cF0, cE, cN, cNA, cQ, cA1, cCK3, cTG2, phase, lead_found, vhat, ahat_long`.
- **B1 arrays** `arrays\B1\<rid>.npz` (the frozen IMM, same extractor): `cF0, cE, cN` (and `k, evaluated, v0, clear, vbar, idx55`).
- **RSX arrays** `arrays\RSX\<rid>.npz` (`x_rsx_extract_v13.py`, §7): the reaction-and-stop clearances judged until the stop ends
  (SHARED: package B's `LB.RS075.rel`, terciles and stop reliance, D2's reaction-and-stop column, the second programs).
- **Old-run tests**: `revision_v11\analysis\rev_common_v01.load_runs()` (35 runs; crit F0, E, N, NA, A1, CK3, Q; truth `phase`), lead state
  `revision_v12\analysis\out\lead\<run>.npz`, TG `revision_v12\analysis\out\tg\<run>.npz` (`cTG2`), old B1 arrays
  `work\B_retrack\out\retrack\B1\<run>_arrays.npz`, extended clearances `revision_v11\analysis\out\ext\<run>.npz` (of record) and this
  program's re-extraction of them.

## 2. Common definitions
- **Libraries of record**, imported unchanged: `optA_lib_v02` (L), `revision_v12\analysis\a9_common_v01` (A9: `gridless_sources`,
  `Gridless`, `row_stats`, `run_events`, `sel_path`), `revision_v11\analysis\rev_common_v01` (C: grid tables, points, bootstrap) and
  package B's `trk_score_v01` (`e5_u`, `add_oracle`, `est_phase`, `gridless`). Gridless resamples are evaluated with
  `cd_common_v13.prep/evaluate` (`gl_fast_v13`, identical to `A9.Gridless.curve` + `L.eval_scoring`).
- **3 s scoring (W1)**: a row is safe iff `L.clean_clear(clear) > 0`.
- **Reaction-and-stop scoring "est" (tau, A)** (A10 §1 "plans judged until the stop ends"; the method of record
  `rev_e1_extended_truth_extract_v01.py` + `rev_e2_extended_truth_score_v01.py`, scoring `est_<vkey>`): a row is safe for the wrong go iff
  `L.clean_clear(clearX_<vkey>) > 0`, where `clearX` is the clearance judged against the logged truth until the stop ends (§7); pairs
  whose recording ends before the stop ("censored") are judged on the frames that exist. Caution keeps W1 (first W1-safe row; W1-safe
  selections), i.e. `row_stats(r, safe_x, masks)` with `r['clear1']` the W1 clearance (A9 = `L.stats_scored` per row).
  `vkey(tau, A)` = `L.vkey` (e.g. `t0p75_a6p0`).
- **Perfect oracle O** of a scoring: `L.select_first_safe(safe_x, idx55)` (first safe row in cost order, else idx55): one point per run
  (A9 `gridless_sources` name `'O'`), with F0's g = 0 point prepended like every source except F0 and E.
- **Frontier (primary): gridless step frontier** (A10 §2.3; `CD_DEFINITIONS_v13.md` "Gridless step frontier"): points at every scale in
  [0, 1000] where a selection changes; 201 levels `linspace(c_F0(0), min(max c_F0, max c_E), 201)`, rebuilt per resample and per
  population and scoring; F0's g = 0 point prepended to every source except F0 and E.
  - D(A) = Σ_levels (F_F0 − F_A); R = D(E)/201 (pp); RR(A) = D(A)/D(E) if D(E) > 0 (finite), else undefined (null / NaN, excluded from
    percentiles); den0 = D(O); RR0(A) = D(A)/den0 if den0 > 0 else undefined; decision-equivalents `L.dec_eq(D, n)` = D/201/100·n, n the
    population's decisions (in a resample, weighted by the run counts).
- **Grid frontier** (groups 5 only, and the old-run comparisons): grid `[0] + logspace(-2, 3, 201)`, `L.select_grid`, `L.stats_scored`,
  `L.eval_scoring` (rev_common_v01 `tables` / `points` / `boot`).
- **Bootstrap** (groups 1 and 2): `L.boot_counts(105, 20000, 20261911)` (rows = resamples, columns = runs in ascending id); 95% percentile
  interval `np.percentile(x[finite], [2.5, 97.5])` (= `L.pct`). Points from the full sample (all counts 1). The same count matrix serves
  every key (groups 1 and 2 share it; `rel` uses the W1 and the est room of the same row).
- **Old-run tests**: the draw of record `L.boot_counts(35, 20000, 20261113)` (first 2,000 rows where the value of record used them).

## 3. Group 1: populations (A10 §5.7 "RR_gl of NA, AM, CK3, TG and Q"; interface §4 prefixes)
- **Populations** (`cd_common_v13.masks_tracker_phase`): all = evaluated; mov = evaluated and `v0 > 0.5`; pre / brk / stop = evaluated
  and the **online tracker's (CV0's) phase estimate** `est_phase(vhat, ahat_long, lead_found, -1.0)` = 0 / 1 / 2 (A10 §2.4). Each
  population on its own frontier and levels. `n_dec` = number of its decisions (integer).
- **Sources** on the CV0 room (F0 = `cF0`, E = `cE`): N `cN`, NA `cNA`, AM `cA1`, CK3 `cCK3`, Q `cQ`, TG `cTG2` (r0 = 2 m/s),
  E5 = `add_oracle(F0, m = 1.1029, A = 0.05, u)`, u = `e5_u(runs, 'F0', 'E')` computed ONCE over all evaluated decisions of the run set
  (not per population), exactly as `c_lead_v13.py` (A10 §2.2).
- **RR_IMM (my reading of A10 §2.1 and interface §4)**: the share of N_IMM **on the IMM's own room**, RR_gl(N_IMM) =
  D(N_IMM, F0_IMM)/D(E_IMM, F0_IMM), from the B1 arrays (F0_IMM = `cF0`, E_IMM = `cE`, N_IMM = `cN`), NOT a share of the CV0 room. In
  population `all` its point equals `LB.IMM.r` (whose interval is calibrated; this one is nominal 95%). Its populations are the **CV0**
  masks above (the same decisions in every row of the table). The B1 arrays must have the same `k` (asserted); `v0`, `clear`, `vbar`,
  `idx55` and `evaluated` are compared and any run that differs is listed in `details` (on the 35 old runs all are identical). The IMM
  room uses B1's own `clear`, `vbar`, `idx55`; IMM's masks are the CV0 masks AND B1's `evaluated`. Sensitivity in `details` only
  (points): the populations by the IMM's own phase estimate (B1's vhat / ahat_long / lead_found, −1.0 m/s²), as package B's B_B1.
- R.ci = percentile interval of D(E)/201 over the resamples; RR_<src>.ci over the finite resamples (share of non-finite in details).

## 4. Group 2: reaction and stop (A10 §5.7; methods of record rev_e2 / rev_e3 / rev_e4, gridless here)
- Population: all evaluated decisions. Scoring est(tau, A) of §2; sources F0, E, O, N, CK3 (NA, AM, Q in details).
- `rel` = D_est(E, F0) / D_W1(E, F0) on the same resample (the 3 s oracle's advantage under est relative to its 3 s value; rev_e2
  `denE_over_3s`), undefined if D_W1(E, F0) ≤ 0. `den0.dec` = `L.dec_eq(D_est(O, F0), n)`. `RR0_N` = D_est(N)/D_est(O); `RR0_CK3` likewise.
- Intervals (`rel.ci`, `RR0_N.ci`) for the six tau at 6 m/s² only; A = 4, 5, 7.6 at 0.75 s are points (as rev_e2: `do_boot` False).
- `LB.RS.0.75.6.*` must equal the writer of `LB.RS075.rel` (same scoring est, gridless, same draw). Since the key list of 03:29,
  `LB.RS.0.75.6.rel(.ci)` are read by A from package B (`rename_v13.json`); this program writes them to `details` as the cross-check.
- **Gap 2 m** (`LB.gap2.*`, rev_e3 convention, points): tau 0.75 s, 6 m/s²; wrong-go safe set `clean_clear(clearX_t0p75_a6p0) > 2`;
  the caution's truly safe rows (and its oracle row) from the 3 s clearance minus 2 (`clear1 − 2 > 0`, i.e. `row_stats` with
  `r['clear1'] − 2`); O = first row with `clearX > 2`, else idx55. den0.dec, RR0_N, RR0_CK3 as above. Details: rev_e4's sensitivity
  (censored pairs unsafe: safe set `clearX > 2` AND NOT `cens`), points.
- Not evaluable rule (den0 < 10 decision-equivalents): applied by the text, not here; the values are exported as computed.

## 5. Group 3: after-stop truncation (A10 §5.7, S1; method of record `rev_b_truncation_phase_scale_v01.py` R12a, gridless here)
- 3 s scoring W1; sources F0, E, CK3 (N, NA, AM, Q, O in details). Population per run (truth phase of record, CV0 array `phase`):
  `k_stop` = k of the run's FIRST stored decision (evaluated or not) with truth phase 2 (lead stopped); `since` = (k − k_stop)·0.05 s
  (undefined if the run has no such decision).
- **T ∈ {0, 1, 2, 5, 10, 20}**: keep evaluated decisions with truth phase ≠ 2, and those with phase 2 and `since < T − 1e-9` (record;
  T = 0 drops the after-stop phase). R = D(E)/201 and RR_CK3 = D(CK3)/D(E) on each population's own frontier. Points.
- **cut5** ("every recording cut 5 s after the lead's stop", review question): the recording is treated as ending at frame k_stop + 100;
  an evaluated decision is kept iff its 3 s truth window ends by then: no k_stop, or `(k − k_stop)·0.05 + 3 ≤ 5 + 1e-9`
  (equivalently `since ≤ 2 s`, inclusive, by time alone, whatever the phase). It differs from T2 only by decisions at exactly 2 s after
  k_stop and by any phase-≠-2 decisions more than 2 s after k_stop (open choice O3).
- The truth phase (not the tracker's estimate) is used because S1 is about recording length after the lead's real stop (record).

## 6. Groups 4 and 5
- **Caution caps** `LB.cap<c>.R`, c ∈ 5, 10, 15 (% of the desired speed; caution as of record in percent): W1, all evaluated, gridless.
  Levels `linspace(c0, min(C, c), 201)` with c0 = F0's g = 0 caution and C = min(max c_F0, max c_E) of record (the window of record
  with its upper end capped at c); R_cap = Σ (F_F0 − F_E)/201 over these levels. If c ≤ c0 the window is empty: null. If C ≤ c the
  value equals `LB.all.R`. Points (RR_N, RR_CK3 under each cap in details).
- **Signed caution** `LB.signed.*`: W1, all evaluated, gridless, caution counted at its signed value as `L.stats_scored(signed=True)`
  (rev_a_signed_gap_v01 R11): per decision with any W1-safe row, caution term (vbar[oracle row] − vbar[selected row])/desired whatever the
  selected row's safety, and that decision counted in the caution denominator; decisions without a W1-safe row add 0 to both. Implemented
  as a copy of `A9.row_stats` with column 2 = that signed term and column 3 = "any W1-safe row" (broadcast over the 17 rows). R, RR_N,
  RR_CK3 as §2. Points.
- **Grid frontier and placebo** `LB.grid.*` (A9-1(a), `a9_1_placebo_gridless_v01.py`): grid frontier, W1, all evaluated; P = F0's
  critical scales / 1.1029²; RR_N = D(N)/D(E), RR_P = D(P)/D(E), RR_NmP = (D(N) − D(P))/D(E). Points.
- **Hull** `LB.hull.*`: the convex-hull frontier of record (`L.hull_frontier` inside `L.eval_scoring`, hull_names) on the **grid**
  points (as of record; A10 groups the hull with the grid frontier), W1, all evaluated: R = hdenE/201, RR_N = hD(N)/hdenE,
  RR_CK3 = hD(CK3)/hdenE. Points. Details: the same hull on the gridless points (sensitivity).

## 7. `arrays\RSX\<rid>.npz` (SHARED; written by `x_rsx_extract_v13.py`, one per run; a faithful port of `rev_e1_extended_truth_extract_v01.py`: the same keys, dtypes and expressions as `revision_v11\analysis\out\ext\<run>.npz`)
- Gate: refuses unless `LOCK_A10_2.txt` and `LOCK_A10_2c.txt` both exist (`cd_common_v13.require_lock2c`), except `--test-old` (old
  runs only, written to `analysis\out\rsx_testold_arrays\`). Reads the run folder `runs\<rid>\<rid>\` (SUMMARY.json, `capture\<case>\`;
  if `runs\<rid>\LOGS_OK` is missing it calls `c_extract_v13.extract_logs`, which verifies the archive's SHA-256 first) and
  `arrays\CV0\<rid>.npz` (for `k` and `evaluated`; asserts `k` equals the capture's decisions). Writes `<rid>.partial.npz`, then renames;
  an existing `<rid>.npz` is never overwritten. At most 2 worker processes on the shared laptop (`--not-laptop` lifts the limit on
  another machine).
- Loader: `trk_arrays_v01.load_capture(rd, cap)` (truth `T`, `kmax`). On the old runs its `T`, `kmax`, decisions, draw and contact
  frame are checked to equal those of rev_e1's loader `ol_gateR_rt_extract_v01.load_run('fit', run, 'route_yaw_rh')`.
- Old-run identity (`--test-old`): every key of every variant equal to `revision_v11\analysis\out\ext\<run>.npz`, and `clear61` equal to the
  cache packs of record (`11_ojits\review\optionA_recount_v01\cache\<run>_pack.npz`, key `vkey`) on evaluated decisions.
- Fresh-run identity (logged in `meta` and the run log, no outcome): `clear61_t0p75_a6p0` against `c_extract_v13`'s `clearR075`.
- `meta`: JSON string (run_id, case, code, variants, n_dec, n_evaluated, kmax, seconds, mode, checks: per variant n_pairs, n_late,
  n_late_safe61, n_cens_safe61, n_flag_changed_by_extension, n_nonlate_changed, jend_max).
- `k` (n,) int64; `evaluated` (n,) bool (copied from CV0). (rev_e1's files hold `k` and `meta` only; `evaluated` is added.)
- For each of the 9 variants kk = vkey(tau, A), (tau, A) ∈ {(0.5, 6), (0.75, 6), (1.0, 6), (1.25, 6), (1.5, 6), (1.8, 6), (0.75, 4),
  (0.75, 5), (0.75, 7.6)}, arrays (n, 17), NaN / −1 / False on non-evaluated decisions:
  - `clearX_kk` float64: smallest rectangle distance to any true actor over frames 0..J_r (J_r = max(60, ceil(t_stop_r/0.05 − 1e-9)),
    capped by the frames the recording holds);
  - `clear61_kk` float64: the same over frames 0..60 (= the cached clearance of record; identity check);
  - `tstop_kk` float64: jr·0.05 + t_stop (stop end, s); `jend_kk` int64: J_r before capping; `late_kk` bool: tstop > 3 + 1e-9;
    `cens_kk` bool: late and J_r > kmax − k (recording ends before the stop); `jmin_kk` int64: frame of the minimum.
- Trajectory (rev_e1 = oxsb_replan_v03 `replan_s` 'r157' + `brake_profile`): rows from `finite_primitive.build_library` (the logged
  decision's model state); jr = tau/0.05; s[0..jr] = the row's s; from frame jr on, s[jr] + pos((j − jr)·0.05) with pos, t_stop of
  `L.brake_profile(v0 = row v[jr], a0 = row a[jr − 1], A)` (jerk 12.65 m/s³, position held after standstill), also after frame 60.
  Ego rectangle along the decision's ego heading from the decision's ego pose (truth T[k]['ego']); truth actors: true frames only
  (no extrapolation) up to frame min(max J_r, max(kmax − k, 60)); distance `oc.rect_corners` + `oc.poly_dist` as `ox.clearance`.

## 7b. Implementation notes a second program may need
- Gridless tables are built as `A9.gridless_sources` builds them (`row_stats`, `sel_path`, events sorted by breakpoint, last event per
  breakpoint kept), with the row statistics computed once per run and scoring and the selection paths cached per run and source
  (same arithmetic, same order). Every table set holds one population mask (group 1: all, mov, pre, brk, stop in turn; group 2: "all"
  per setting; group 3: T0, T1, T2, T5, T10, T20, all, cut5 in turn); a table set with several masks gives the same numbers.
- Points: `L.eval_scoring` on the full-sample curves; resamples: `gl_fast` on the bootstrap counts, asserted equal to the library at
  the full sample (exactly). For speed the resamples drop the events whose statistics are zero in the population (decisions outside it
  or not evaluated): they add exactly 0.0 to the running sums, so every curve point and frontier value is unchanged (asserted equal,
  bit for bit, to the unfiltered evaluation on the first 200 resamples of every bootstrap). A second program need not do this. `rel`'s denominator in a resample is that resample's W1 room of population `all` (group 1).
- E5 and the placebo P are added to every run before any table is built (`TS.add_oracle`, `A9.add_placebo`).
- `n_dec` and `den0.dec` use the population's decision count (full sample); interval ends of `dec` quantities in `details` use each
  resample's own count.

## 8. Open choices (recorded before any fresh value)
- O1 RR_IMM on the IMM's own room with CV0's populations (§3).
- O2 (settled by the CD lead, 20 Nov ~02:50 EST) The reaction-and-stop keys use the scoring "est" on the RSX arrays (judged until the
  stop ends, A10 §1, Supplement S6.1), not the 3 s-window clearance (`clearR075`, cache packs, `delayed_stop_clearance`). Package B
  reads the same RSX arrays for `LB.RS075.rel`, so `LB.RS.0.75.6.rel` and `LB.RS075.rel` agree if both use the gridless frontier and
  the same draw. The as-scored (3 s window, `clear61`) values are in `details` for comparison.
- O3 cut5 = recording ends 5 s after k_stop, decisions kept only if their 3 s window fits (§5).
- O4 Caps: window `[c0, min(C, cap)]` with 201 levels (§6), not the 201 levels of record truncated at the cap.
- O5 Hull on the grid points (§6).
- O6 Truncation by the truth phase of record (§5).

## 9. Old-run tests (`analysis\out\TESTOLD_S57B_v13*.json`, summary `analysis\out\TEST_S57B_v13.json`)
- `x_rsx_extract_v13.py --test-old` on all 35 old runs (`TEST_S57B_v13_rsx_extract_*.json`): every key of every variant equal to
  rev_e1's `out\ext` (largest difference 0), the loader equal to rev_e1's, `clear61` within 6.4e-14 of the cache packs (no flag differs).
- `c_s57b_v13.py --test-old` with `--frontier grid --phase truth` reproduces the grid values of record with the draw of record (v12 A9-1(a)
  populations and A9-7B TG with 20,000-resample intervals; v11 rev_e2 for all nine settings, rev_e3, rev_e4, rev_b R12a, rev_a R11;
  Option A main's as-scored reaction-and-stop and W1 hull); `--frontier gridless --phase truth --nboot 2000` reproduces v12 A9-1(c)
  (points by population and the pooled intervals on the first 2,000 rows); `--frontier gridless --phase est` reproduces package B's old-run
  B_CV0 and B_B1 (points by estimated-phase population; with `--nboot 2000` also the pooled intervals). The program's own settings
  (`gridless`, `est`, 20,000) on the old runs give `TESTOLD_S57B_v13.json`.
