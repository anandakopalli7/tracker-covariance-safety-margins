# Package B recount (independent second program)

Code (this folder only): `rc_core.py` (loaders, gridless engine, E5 oracles), `b_variants.py` (per variant), `b6.py`, `b9.py`,
`combine.py`, `watcher.py`, `selftest.py`. Output: `RECOUNT_B_v01.json` (per-variant parts in `parts\`). Scoring library
`optA_lib_v02.py` imported unchanged (eval_scoring, curves_w, frontier, levels_of, select_grid, stats_scored, select_first_safe, rates,
ratio, dec_eq, pct).

## Method notes (what is mine)
- **Gridless frontier.** Breakpoints = 0, every distinct critical scale in (0,1000), and 1000, per source. Per-run summed statistics at
  every breakpoint are built from the interval of g on which each row is selected (row r iff prefix-max(C before r) < g <= C_r; fallback
  idx55 iff g > max C). This is an equivalent fast path to select_grid + stats_scored; checked against the library at random and edge
  breakpoints (max abs diff 1e-14) and against v12 on the online tracker: R = 5.512545835358791 pp, RR_gl(N) = -0.00041369549833977597,
  RR_gl(CK3) = 0.8366011648794295, RR_gl(NA) = 0.01506722551848021, 8,290 evaluated decisions (all identical to A9_1 of v12). My point
  counts per source differ from v12's "n_points" (I count distinct breakpoints over evaluated decisions, plus 0 and 1000); this does not
  change any frontier.
- Variant CV0 arrays reproduce the record (room, RR_N, c, lag identical to the stored-array run to the last digit).
- Intervals: first 2,000 rows of the draw of record, percentile 95%, levels rebuilt in each resample (library eval_scoring per resample);
  m_x, A_x and the E5 ranks are fixed at the full-data values in the resamples.
- **E5 ranks (D-E5-1).** r_i = median over rows with finite positive g*_F0 and g*_E of sqrt(g*_F0/g*_E); u = (midrank - 0.5)/n over
  decisions that have such rows; others 0.5. Oracle scales = cF0/f^2. **Permutation:** one `default_rng(20261915)`, runs in name order,
  `u_run[rng.permutation(n_eval_run)]` over all of the run's evaluated decisions in k order (decisions with u = 0.5 take part).
- **m_x, A_x:** all evaluated decisions and rows with finite positive cF0 and cN; sqrt(cF0/cN); q05/q95 by np.percentile (linear).
  "within 5%": |ratio/median - 1| <= 0.05.
- **H3 classification (print only):** r = RR_gl(N_x), c = RR_gl(E5_x) with delta = 0.05 and the A10 wording; "barely varies" if share
  within 5% >= 0.95. Efficiency r/c only when (a).
- **Estimated phase:** stopped if lead_found and vhat <= 0.5; braking if lead_found, vhat > 0.5 and ahat_long <= thr; else before
  braking (no lead track, or NaN, counts as before braking). thr = -1.0 primary; -0.5 and -2.0 also in the JSON (`populations`).
- **After-stop room:** gridless R in the truth-phase-2 population (evaluated decisions), decision-equivalents = D/201/100*n.
- **Lag:** t_stop = `now` at the run's first truth-phase-2 decision among ALL decisions of the run; evaluated truth-phase-2 decisions
  with 0 <= now - t_stop < 1 s; median of dx_pred3 pooled over runs (finite values).
- **NIS / NEES:** one value per distinct (run, track_id, round(now - age, 3)) among evaluated decisions with lead_found; the FIRST such
  decision (k order) carries the NIS (`nis_last`), the velocity NEES (`nees_v`) and the phase. Means by phase with run-level percentile
  intervals (ratio of sums over resampled runs, first 2,000 draws); medians beside. I could not tell from the definitions whether the NEES
  should be taken at the first or another decision of the update; first was my choice.
- **B6(a):** realised deceleration = minus the least-squares slope of the target's horizontal speed (velocity_lh) vs truth time between 0.9
  and 0.1 of the pre-brake speed. Quote of definition used: "the slope of the true lead speed between 90% and 10% of its speed before the
  onset" (v12 supplement). Onset tick = the truth tick nearest t(k=99) + draw.brake_start_s (the braking onset sits at that offset from
  the tick of k = 100, checked visually on five runs); pre-brake speed = speed 3 ticks before it; fitted ticks start 2 ticks before it.
  Range 2.0896-5.4592, matching the 2.09-5.46 of v12. **Sensitivity:** with pre-brake speed taken 0-1 ticks before the onset (instead of
  3), one run swaps between terciles 2 and 3 (offset 5 ticks: none, max 5.499). Terciles: ascending, ties by id, array_split 12/12/11.
  Scoring W_R = cached clearance of `t0p75_a6p0` > 0 (NaN -> -1), caution by the 3 s clearance, as stats_scored. den0 = D(F0,O) with O =
  select_first_safe under W_R. Gridless is primary; grid values are beside in the JSON.
- **B6(b):** tau_i = 0.75 + rng.uniform(0, 0.75) drawn from one `default_rng(20261916)`, runs in name order, evaluated decisions in k order
  (the draw order is my reading of D-B6-1); compared with the stored `tau` at evaluated decisions (max abs diff in the JSON). Scoring
  recount from the stored clearances. **Status: see below.**
- **B9:** event = first truth tick with the target (primary actor) along-route distance > 0 and |lateral - lane centre| <= 1.75 m, lane
  centre = median ego lateral route coordinate (D-B9-1). Window = evaluated decisions with now - t_c in [-1, 4] s (inclusive). Track age =
  now - birth time (first detector frame holding the id) of the youngest track matched (own matching, nearest within 4 m of the actor
  predicted to `now`, planner frame at the decision tick, planner frame convention checked: errors < 1 m). Note: the stored `prim_age` is
  the age at the state time (steps of 0.5 s) and differs from mine by 0-0.4 s; the strata are unaffected. Bootstrap over all 20 runs with
  the 20-run draw (runs without events would add nothing).

## Findings you should know about
- B9: events found in 20/20 runs (identical with the instantaneous ego lane coordinate, 20/20; 20/20 also at 2.5 m); 993 evaluated decisions
  in the windows; ALL are in the >= 4 s stratum (young-track and 1-4 s strata empty, nothing untracked); and the room is exactly zero: in
  the 20 cut-in tuning runs every row of every evaluated decision is 3 s-safe (clear > 0), so D(E,F0) = 0 in the window and everywhere in the
  20 runs; RR_gl(N) is undefined (0/0), den0 = 0, K0/K2 not evaluable.
- B6(a): only the lowest tercile has den0 >= 10 decision-equivalents; terciles 2 and 3 are not evaluable (see JSON).

## Not computed / caveats
See the end of this file (appended after the last run).

### Status at hand-over (19 Nov 2026, ~17:45 EST)
- All 7 variants x 35 runs present and recounted (CV0, B3, B2, B4, B1, B1_d090, B1_d098).
- **B6(b) delayed-stop clearances (`out\b6\clear\`) did not exist yet.** The scoring and the tau check are coded and tested on a
  stand-in (stored tau = my tau, W_R clearances reused: max abs tau diff 0, room equal to the W_R room). `watcher.py` keeps polling
  (until about 18:25 EST) and, when all 35 files exist, re-runs `b6.py` and `combine.py`, which fills `B6.delayed` in
  `RECOUNT_B_v01.json` (`B6.delayed` is null until then; check `B6.b6b_files_present`).
- Not computed: B8(a); intervals for after-stop room and phase rooms (points only); intervals for NA, AM, CK3, Q; per-stratum
  N/F0 ratio in B9 beyond the window population (empty strata, zero room); a young-track K2 classification (population empty).
- Interpretations to compare with the first program: realised-deceleration pre-brake speed and onset tick (T2/T3 boundary is sensitive
  by one run); permutation convention; NEES taken at the first decision of an update; lag t_stop from all decisions; track age = now - birth.

## Update 19 Nov 2026, ~18:10 EST (after the coordinator's comparison; A10 s10.1(c))
Changed only these, then re-ran B9 and B6 (and the lag):
1. **Clock comparisons on the 0.05 s tick clock.** B9 window: dt = (k_decision - k_event) x 0.05, rounded to the 0.05 grid, inclusive test
   against [-1, +4] (1e-9 tolerance). Window total **993 -> 1,007**; all 1,007 still in the >= 4 s stratum; room still exactly 0 (den0 0).
   Lag (first second after the stop): (k - k_stop) x 0.05 from tick indices; **no change** (medians and n = 300 identical for all 7 variants;
   old values kept in `lag_before_tick_fix` of each part).
2. **Realised deceleration, rule of record as written** ("v_pre = median of v over 3 < t < 5 + brake_start_s - 0.2 ... samples with
   0.1 v_pre < v < 0.9 v_pre and t > 5 + brake_start_s - 0.5; if at least 4, take the contiguous index range ... polyfit"), with
   t = 0.05 k and v = |velocity_lh| (3-D norm). Range now 2.0904-5.4592 (was 2.0896-5.4592). Terciles: T1 unchanged (12 runs, 2.09-3.49);
   one run moved between T2 and T3. New T2 2.69 dec-eq W_R room (3 s room 125.81, ratio 0.0214, den0 2.86); T3 5.25 (98.31, 0.0534, 5.31);
   T1 46.89 (233.66, 0.2007, 47.94). T2 and T3 still not evaluable. My onset-based reading is kept as a printed sensitivity
   (`realised_decel_onset_reading_sensitivity`, `terciles_onset_reading` in `B6`). All-35 W_R room 54.69, den0 57.03 unchanged.
3. **B6(b) now computed** (all 35 clearance files present): stored tau equals my tau (max abs diff 0.0). Delayed stop, gridless:
   room 1.627 pp = 134.88 dec-eq, den0 143.08 (evaluable); RR(N) -0.0004, RR(NA) 0.0192, RR(AM) 0.565, RR(CK3) 1.0036, RR(Q) -0.0231.
   Grid: room 136.28 dec-eq, den0 144.64, RR(N) 0.0013, NA 0.0209, AM 0.558, CK3 1.0006, Q -0.0204.

## Update 19 Nov 2026 (NIS/NEES amendment 1, 18:40 EST definition)
NIS and NEES by phase recomputed as written in "Amendment 1": distinct updates = (run, track id, state time rounded 1 ms) at evaluated
decisions with a lead track and finite `nis_last`, each assigned to the phase of its first evaluated decision (truth 0-3 and estimated, thr
-1.0, separately); NIS = `nis_last`; NEES_v = e' Pvv^-1 e with v_trk and the 2x2 velocity block of `trk_P4` taken from the `trk_*` entry with
the same id and state time (all matched, 0 unmatched), v_true = target velocity_lh with y negated at the truth tick nearest the state time,
both rotated into the route frame by the ego route yaw at that tick (0 in these runs). Results are in `RECOUNT_B_v01.json` per variant under
`nis_nees_amend1` (code `nis_amend1.py`); the earlier `nis_nees` (decision-time NEES, first-decision rule) is kept unchanged.

## Update 19 Nov 2026 (B2 oracle check)
Post-hoc diagnostics (a)-(d) for B2 in `RECOUNT_B_v01.json` under `B2_oracle_check` (code `b2_check.py`): RR_gl(N)-RR_gl(E5_x) and RR_gl(E5q) with E5q = cF0/quantile(binding-row ratios, u_i)^2 on the same ranks; first 2,000 resamples; percentile intervals over resamples with room > 0.

## Update 19 Nov 2026 (oracle check, all trackers)
Items (a)-(d) of the B2 check for every variant, each on its own arrays, in `RECOUNT_B_v01.json` under `oracle_check` (code `oc_one.py`); `B2_oracle_check` kept.
