# Brief for the independent second program (recount) of the revision analyses

Written 18 Nov 2026 by the revision session, before the first program's results were read. The second program is written from this file, the paper's definitions and `AMENDMENT_08_ARS_REVISION_v01.md`. It must not open anything under `revision_v11\analysis\` (the first program and its outputs) until its own results are written.

## Inputs (read-only)
Root `P = <library folder>`.
- The 35 evaluation runs, sorted names `p1b_fit_finite_0005` … `p1b_fit_finite_0039`.
- `P\09_redesign\m2_decisions\openloop\gateR_rt_v01\<run>.npz`: `evaluated` (bool per decision), `v0` (ego speed), `clear` (decision × 17 rows: true clearance in m under the 3 s commitment; NaN only outside the evaluated set → treat as −1), `vbar` (row mean speed), `idx55` (index of the full-braking fallback row), `cF0`, `cE`, `cN` (critical margin scales per row: class average, oracle, tracker covariance), `k` (tick, 0.05 s), `prim_age`, and `meta` (JSON string with `desired`).
- `P\11_ojits\A4\fit\extract\<run>.npz`: `cNA`, `cA1` (the acceleration margin AM), `cCK3`, `cQ`, `phase` (0 before onset, 1 lead braking, 2 lead stopped, 3 unknown).
- `P\11_ojits\review\optionA_recount_v01\cache\<run>_pack.npz`: reaction-and-stop clearances per row, keys `t0p75_a6p0` etc.
- `P\11_ojits\A4\fit\analysis\A4_RESULTS_FIT_v01.json`: `splits.alpha.<value>.runs` gives each run's recording setting α.
- Allowed scoring library: `P\11_ojits\review\optionA_recount_v01\optA2_lib_v02.py` (the project's own second-program library). Forbidden: `P\11_ojits\A6R\code\` (the first-program lineage) and `revision_v11\analysis\`.

## Scoring definitions (as in the paper, Sections III-B, IV-A, IV-B, IV-C)
- Margin scale grid: `g` = 0 and 201 values log-spaced from 1e-2 to 1e3 (202 values). At scale `g` the planner selects the first row (index order = cost order) whose critical scale is ≥ `g`; if none, the fallback row `idx55`.
- Wrong go: the selected row is unsafe under the scoring (3 s commitment: `clear` ≤ 0; reaction-and-stop: cache clearance ≤ 0; with a standstill gap `G`: clearance ≤ `G`).
- Caution of an arm at a scale: over evaluated decisions whose selected row is truly safe under the 3 s commitment (`clear` > 0; with a gap `G`: `clear` > `G`), the mean of (speed of the first truly safe row − speed of the selected row) / desired speed, in %. **Signed caution**: the mean over every evaluated decision that has at least one truly safe row, each at its signed difference (selected row safe or not).
- Each arm and scale give a point (caution %, wrong-go %). Every arm other than F0 and E gets F0's zero-margin point prepended. Step frontier at a level = lowest wrong-go among the arm's points with caution ≤ level. Levels: 201 equally spaced from F0's zero-margin caution to min(largest caution of F0, largest caution of E), rebuilt for every population and every resample.
- `denE` = Σ over levels (F_F0 − F_E); room R = denE/201 (pp). `D(A)` = Σ (F_F0 − F_A). RR(A) = D(A)/denE. Perfect oracle O: one selection per decision, the first row the scoring judges safe (fallback row if none); `den0` = D(O); RR₀(A) = D(A)/den0. Decision-equivalents = D/201/100 × n.
- Populations: all evaluated; ego moving (`v0` > 0.5); phases 0, 1, 2; each on its own frontier and levels. Phase-weighted aggregate: Σ_p (n_p/n) D_p and likewise den0, over phases 0–2.
- Bootstrap of record: `numpy.random.default_rng(20261113).integers(0, 35, size=(20000, 35))`, rows = resamples of the 35 runs in sorted-name order; everything recomputed per resample; 95% percentile intervals over resamples with a positive denominator.

## What to compute
1. **R11.** 3 s commitment with signed caution: R, den0, and RR and RR₀ of N, NA, AM, CK3, Q, for all / ego moving / phase 1 / phase 2 / phase-weighted. Points and intervals of record.
2. **R17.** Standstill gap 2 m: (a) 3 s commitment; (b) reaction-and-stop τ = 0.75 s, 6 m/s² (`t0p75_a6p0`). den0 (pp and decision-equivalents), denE, RR₀ of N, NA, AM, CK3, Q, E: all, ego moving, phase-weighted. Points; intervals for "all" and phase-weighted.
3. **R12a.** Populations keeping all evaluated decisions before the lead's stop and those after it with (k − k_stop)·0.05 s < T, where k_stop is the tick of the run's first stored decision with phase 2; T = 0, 1, 2, 5, 10, 20 s. For each: n, R, RR and RR₀ of N, NA, AM, CK3. Points and intervals.
4. **R12b.** One margin scale per phase. For each arm, the points are all triples (g0, g1, g2) of the grid; wrong go = pooled wrong-go share; caution = pooled caution (sum of caution terms / number of truly safe selections, over the three phases). Per-phase-scale step frontier at the pooled single-scale levels; every arm other than F0 and E gets F0's single-scale zero-margin point prepended. Report (sums over levels): `den1` = Σ(F1_F0 − F1_E) single scale; `gain_F0` = Σ(F1_F0 − Fps_F0); `den_ps` = Σ(Fps_F0 − Fps_E); `den0_ps` = Σ(Fps_F0 − F_O); `Dps(A)` = Σ(Fps_F0 − Fps_A) for N, NA, AM, CK3, Q. Points; intervals over the first 400 rows of the draw of record.
5. **R9.** For the statistics R, RR(N), RR(NA), RR(AM), RR(CK3), RR(Q), RR₀(CK3), RR(NA) − RR(N) (3 s commitment, all evaluated decisions):
   - the 95% percentile and basic intervals of the draw of record;
   - double bootstrap: outer indices `default_rng(20261120).integers(0, 35, (2000, 35))`; one inner stream `rng = default_rng(20261121)`; for outer sample b = 0, 1, … in order draw `ii = rng.integers(0, 35, (1000, 35))` and resample the outer sample's runs as `outer[b][ii]`. Truth = the full-sample value. For each outer sample store the share of inner values below and at-or-below the truth. Coverage of the two-sided percentile interval at nominal level 1 − a = share of outer samples with share(inner ≤ truth) ≥ a/2 and share(inner < truth) ≤ 1 − a/2. Report coverage at nominal 0.90, 0.95, 0.99, 0.999, 1.0, and the smallest nominal level on the grid 0.900, 0.901, …, 0.999, 0.9995, 0.9999, 1.0 with coverage ≥ 0.95, and the percentile interval of the draw of record at that level;
   - percentile intervals stratified by α (`default_rng(20261122)`; for each α group in increasing α, `g[rng.integers(0, g.size, (20000, g.size))]`, concatenated);
   - the 30 runs with at least 100 evaluated decisions: points and percentile intervals (`default_rng(20261123)`, `long[rng.integers(0, 30, (20000, 30))]`).
6. **R19 / R20.** For every stored run of every family in `gateR_rt_v01` (223 files; `meta.family`, `meta.set`): on evaluated decisions and rows with finite positive `cN` and `cF0`, margin ratio m = 1/sqrt(cN/cF0); per family (all runs): rows, median m, share of rows with |m/median − 1| > 0.05. Lead braking: evaluated decisions of the 35 evaluation runs by `prim_age` (< 0.5, 0.5–1, 1–2, 2–4, ≥ 4 s).

## Output
`revision_v11\recount\RECOUNT_RESULTS_v01.json` with one entry per number, plus `RECOUNT_REPORT_v01.md`. Then, and only then, open `revision_v11\analysis\out\*.json`, compare every shared number and write `RECOUNT_COMPARE_v01.md`: agreement within 1e-9 for points and for intervals that use the same draw; list every difference with both values.
