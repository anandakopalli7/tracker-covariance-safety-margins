# Packages C and D of revision v13: definitions for the second programs

Written 19 Nov 2026, 17:15 EST, by session CD (Claude Opus 5.5). It states every definition the first programs fix beyond the text of `..\..\AMENDMENT_10_v13.md` (§2, §5, §6, §10). All were fixed before any value of a fresh run was computed. A second program is written from A10 and this file, never from the first programs (`analysis\*.py`).

## Inputs (shared, allowed by A10 §10.1(b))
- **Scoring library of record**, imported unchanged: `<library folder>\optA_lib_v02.py` (`stats_scored`, `rates`, `frontier`, `levels_of`, `curves_w`, `eval_scoring`, `boot_counts`, `dec_eq`, `clean_clear`, `select_grid`, `select_first_safe`, `NLEV = 201`).
- **Shared tracker library**: `work\shared\trackers\trk_score_v01.py`, i.e. package B's E5 family (`e5_u`, `permute_u`, `add_oracle`, `margin_ratios`, `ratio_summary`) and `est_phase`. A second program may import these or re-implement them.
- **Extracted arrays** (after Lock 2): `work\CD_capture\arrays\<variant>\<run_id>.npz`, with variant `CV0` (online tracker of record) or `B1` (frozen IMM).
  - Keys (one row per decision; `(n, 17)` for the 17 planner rows): `k, evaluated, v0, des, clear, vbar, idx55, cF0, cE, cN, cNA, cQ, cA1` (= AM), `cCK3, phase` (truth phase of record), `lead_found, vhat, ahat_long`.
  - `CV0` only: `cTG1, cTG2, cTG4, clearR075`.
  - `meta` is JSON: family, run_id, case, `lead_variant`.
- **Old evaluation runs** (H4 design set and D1 matched settings): `ARS_TRIAL\revision_v11\analysis\rev_common_v01.load_runs()` (35 runs).
  - Tracker estimate of the lead state: `revision_v12\analysis\out\lead\<run>.npz` (`vhat, ahat_long, lead_found`).
  - TG: `revision_v12\analysis\out\tg\<run>.npz` (`cTG2`).
- **Run sets**:
  - C lead braking: `pc13_<case>_native` for the lead_braking rows of `work\CD_capture\CASES_C_v13.json`.
  - C cut-in: the same for the cutin rows.
  - D1: `pd13_<case>_native` for the `d1_openloop` rows of `work\CD_capture\d1\CASES_D1_v13.json`, per `lead_variant.kind`.

## Common
- **Safety under the 3 s commitment**: row safe iff `clean_clear(clear) > 0`.
- **Reaction-and-stop at τ = 0.75 s** (D2 only): safe iff `clean_clear(clearR075) > 0`. Caution keeps the 3 s definition (`stats_scored` with `safe_x` = the R&S safe set).
  - **Superseded 20 Nov 2026, 03:30 EST (before Lock 2):** A10 §1 fixes the reaction-and-stop scoring "with plans judged until the stop ends", which is v11's extended clearance (`revision_v11\analysis\rev_e1_extended_truth_extract_v01.py`, `clearX_<vkey>`; safe iff `clearX > 0`, rev_e2's 'est'), not the 61-frame `clearR075`. D2's reaction-and-stop column (and its first-loss tick, which can then lie beyond tick 60, up to the stop's end) is therefore moved to stage 2, computed from the shared extended arrays `arrays\RSX\<rid>.npz` (format in `CD_DEFINITIONS_S57B_v13.md`) and frozen in FREEZE_CD_2. The stage-1 D2 scripts compute the 3 s columns only; `clearR075` stays in the CV0 arrays as the 61-frame identity anchor. The same extended clearance is used for every reaction-and-stop key of v13 (LB.RS.*, LB.RS075, terciles, DS, REL, gap2).
- **Populations**: evaluated decisions (`evaluated == 1`).
- **Phase**: the tracker estimate (A10 §2.4) with `est_phase(vhat, ahat_long, lead_found, thr)`; thr −1.0 primary, −0.5 and −2.0 as sensitivities. Truth phase = `phase` ∈ {0, 1, 2}.
- **Gridless step frontier (A10 §2.3)**: every margin scale in [0, 1000] at which some decision's selected row changes (the v12 A9-1(c) construction, `revision_v12\analysis\a9_common_v01.gridless_sources`).
  - Each curve point is the source's summed statistics.
  - Every source except F0 and E gets F0's g = 0 point prepended.
  - 201 levels: `linspace(c_F0(0), min(max c_F0, max c_E), 201)`, rebuilt per resample.
  - D(A) = Σ (F_F0 − F_A); R_gl = D(E)/201; RR_gl(A) = D(A)/D(E); decision-equivalents = D/201/100·n.
- **Bootstrap**: `boot_counts(n_runs, 20000, 20261911)` (run counts) over the run set; 95% percentile intervals (`np.percentile` 2.5/97.5 over finite resamples).
- **Calibration (A10 §2.6)**: rev_d_bootstrap_v01's method with A10's seeds.
  - Outer: `default_rng(20261912).integers(0, n, (2000, n))`.
  - Inner: `default_rng(20261913)`, one stream, `integers(0, n, (1000, n))` per outer sample in order, indexing that outer sample's runs.
  - Coverage at level ℓ: share of outer samples with share(inner ≤ full) ≥ (1−ℓ)/2 and share(inner < full) ≤ 1 − (1−ℓ)/2, where "full" is the full-sample value.
  - If the coverage at 0.95 is below 0.94: take the smallest ℓ in 0.950–0.9995 (step 0.0005) with coverage ≥ 0.95. Accept it only if its Monte Carlo SD ≤ 0.002 (2,000 resamples of the outer samples, `default_rng(20261920)`) and the second inner seed (20261914) gives a level within 0.002. Otherwise use 0.99.
  - A hypothesis "lower end" is the lower end of the two-sided percentile interval at the calibrated level.

## C, lead braking (A10 §5.3)
- **E5**: `u = e5_u(F0, E)` over the run set's evaluated decisions; crit_E5 = crit_F0 / f², f = 1.1029·(1 + 0.05·(2u − 1)).
- **E5p**: u permuted within each run, `default_rng(20261915)`, runs in run-id order of the run set.
- **H3 (IMM)**: from the `B1` arrays. F0_IMM = `cF0`, E_IMM = `cE`, N_IMM = `cN`.
  - Ceiling E5_IMM: m = median and A = (q95 − q05)/(2m) of sqrt(cF0/cN) over evaluated decisions and rows with both finite and positive; u = `e5_u(F0_IMM, E_IMM)`.
  - "Barely varies": ≥ 95% of those ratios within 5% of m.
  - Classification exactly as A10 H3.
- **H4**:
  - **Design**: the 35 old runs, tracker-phase populations, grid of record `[0] + logspace(-2, 3, 201)`. Levels from the design set's F0/E grid curves (all decisions).
  - **Triple**: per level, the triple (one grid scale per phase 0, 1, 2) with the lowest pooled design wrong-go among triples whose pooled design caution ≤ level. Ties: lowest caution, then the lowest flat index over the unique per-phase (wrong-go, caution sum, count) tuples. This is v12's `triple_choice`.
  - **Single scale**: same rule (v12 `single_choice` / `frontier_argmin`).
  - **Transfer**: per design level with a choice, the fresh point is the sums over phases at the chosen scales (wrong-go / all evaluated decisions; caution sum / caution count). With F0's g = 0 point on the fresh runs, take the step frontier on the fresh runs' own 201 levels.
  - **Record basis**: Σ(F_F0 − F_ps) / Σ(F_F0 − F_E). F_F0 and F_E are the fresh runs' own grid frontiers.
  - **Like-for-like basis**: Σ(F_1 − F_ps) / Σ(F_F0 − F_E), with F_1 the transferred single scale (also with F0's g = 0 point).
  - **Single scale** (added 20 Nov 2026, 02:40 EST, before Lock 2; A's key `LB.PS.single`): Σ(F_F0 − F_1) / Σ(F_F0 − F_E), the transferred single scale's share on the record basis; nominal 95% interval on the same 20,000 resamples (descriptive, not calibrated).
  - **Resamples**: no re-selection; fresh levels rebuilt per resample.

## C, cut-in (A10 §5.4; as package B's B9)
- **Event tick**: in the truth of the run (route frame), the first tick with the primary actor `along > 0` and |across − lane| ≤ 1.75 m. Lane = median of the ego's lateral route coordinate over the run. Window: evaluated decisions with (k − k_c)·0.05 ∈ [−1, 4] s.
- **Track age**: `now` − the birth detector time of the track matched to the primary actor (`gc.match_many`, nearest within 4 m; several → youngest). Strata: < 1 s, 1–4 s, ≥ 4 s, "untracked".
- **den₀** (K0): D_gl(O, F0) in decision-equivalents. O is the perfect oracle: first safe row in cost order, else the fallback row `idx55`, one point.
- **K2**: m_N and A_N from sqrt(cF0/cN) over the young-track population's decisions and rows; u over all evaluated decisions of the cut-in runs. Not evaluable if R_gl in that population is below 10 decision-equivalents (point estimate).

## D1 (A10 §6)
- **Matched settings** on the old runs (all evaluated decisions, 3 s): c* = F0's pooled caution at g = 1 (grid index of 1.0).
  - Each source: the grid index whose pooled caution is nearest c*. Ties: smaller g.
  - PS: v12's `triple_choice` on the old runs' tracker-phase tables at level c*.
- **Per variant**: pooled caution = 100·Σ caution sum / Σ count; wrong go = 100·Σ wrong / Σ decisions. Report the differences source − F0(g = 1) with 20,000-resample run-bootstrap percentile intervals (`default_rng(20261911)`, per variant).
- **Classification**: as A10 D-H1. "Within ±1 point" means both interval ends lie in [−1, 1].

## D2
- **Operating point**: per source and scoring, the grid points pooled over the 105 runs. Frontier points are those not dominated (no point with caution ≤ and wrong go <). Take the frontier point with caution nearest the target (2 or 5 points). Ties: smaller g.
- **Wrong go**: an evaluated decision whose selected row is unsafe under the scoring.
- **First loss of clearance**: the first of the 61 ticks of the committed plan at which the ego rectangle is at distance ≤ 0 from a true actor's rectangle.
  - Plan: the row's s(t); for R&S, the row until 0.75 s, then the stop of record (`trk_score_v01.stop_profile_cont`, 6 m/s², jerk 12.65).
  - Truth: true frames only.
- **Closing speed**: the plan's speed at that tick minus the true actor's velocity along the ego heading at that tick.
- **Report per run**: the median of its wrong-go decisions' closing speeds. Across runs: the median of the per-run medians. Also the number of runs with ≥ 1 wrong go.

## Additions (19 Nov 2026, 17:40 EST, before any fresh value; from the second programs' questions)
- **Fresh logs** (after Lock 2): `work\CD_capture\runs\<rid>\<rid>\` holds the run's `SUMMARY.json`, and its single `capture\<case>\` folder holds the capture files (extracted from the verified archive `work\CD_capture\archives\<rid>\claude_main_<rid>.tar.gz` without the .npy sweeps).
- **D2 frontier**: grid points only (202 scales), no extra point added; the literal non-domination rule (a point with equal wrong go and higher caution stays eligible).
- **D2 ties at one tick**: when several actors lose clearance at the same first tick, the first actor in the truth window's order counts. Actor velocity: the truth velocity at the loss tick, projected on the ego heading at the decision tick, signed.
- **D2 R&S plan speed**: before τ the row's speed at the tick; after τ the derivative of `stop_profile_cont`'s position (ramp v0 + a0·t + ½·jr·t² up to t1, then v1 − A·(t − t1)), and 0 from the first stop on.
- **D2 missing loss tick**: a wrong-go decision without a loss tick (not expected) is counted, left out of the run's median, and reported.
- **D-H classification order**: as A10 writes it (costs progress; costs safety; no measurable cost; otherwise inconclusive), the first rule that holds.
- **PS**: one grid scale per tracker phase applied to F0's critical values; the triple is v12's `triple_choice` (unique per-phase tuples in lexicographic order, each represented by its smallest grid index).
- **TG**: `cTG2` (r0 = 2 m/s) everywhere.
- **Run order** (19 Nov 18:10 EST): for every resampling (bootstrap counts, double bootstrap, E5p permutation order), the runs of a set are in **ascending run id** order (C lead braking: the 105 `pc13_c1109_eval_<i>_native` ids of the lead_braking rows sorted; C cut-in likewise; D1 per variant: `pd13_d1v13_<kind>_<i>_native` sorted). `boot_counts(n, ...)` row b gives the count of the j-th run in that order.
- **Calibration details** (19 Nov 18:20 EST, aligning both programs): outer samples whose own estimate (the statistic on the outer counts) is not finite are skipped (rev_d_bootstrap_v01); shares are over finite inner values; the coverage comparison uses the 1e-12 tolerance of `cover_two`; if no outer sample is valid, the nominal 99% interval; the Monte Carlo SD is the SD (ddof = 1) over 2,000 resamples of the valid outer samples (`default_rng(20261920)`, the same index draw for every statistic) of the smallest level reaching 0.95 (1.0 when none does); both generators restart for every statistic group (so all groups use the same draws); R_gl stays defined (finite) in resamples with D(E, F0) <= 0, every RR is NaN there.
- **Cut-in details**: the per-second bins are [-1, 0), [0, 1), [1, 2), [2, 3) and **[3, 4] (closed)**; a matched track without a birth record is skipped (b9_cutin_v01: `book.birth.get(...)` None → not counted), so the decision is 'untracked' unless another matched track has a birth; the route frame and lane centre are b9_cutin_v01.event_tick's (truth from `trk_arrays_v01.load_capture(rd, cap)['T']`, ego tuple (x, y, yaw)); runs without an event stay in the resampled set (empty windows) and in K2's u.
- **Monte Carlo SD index draw** (19 Nov 18:40 EST, confirming the second program's reading): one draw over ALL outer samples, `default_rng(20261920).integers(0, 2000, (2000, 2000))`, the same for every statistic; in each resample the coverage uses the drawn rows that are valid for that statistic; a resample with no valid row, or in which no level reaches 0.95, counts as 1.0.
