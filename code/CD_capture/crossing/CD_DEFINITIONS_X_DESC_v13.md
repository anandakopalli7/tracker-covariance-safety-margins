# X: A11 §3.6 fixed descriptive outputs (pedestrian crossing): definitions for both programs

Written 21 Nov 2026, about 14:50 EST (Claude Opus 5.5, session CD), after LOCK_A11 and before any fresh crossing value was computed. This file and A11 §3.6 are the specification for two programs:
- the first program, `crossing\x_desc_v13.py`;
- the second program, `recount\rc_x_desc_v13.py`, written by Claude Sonnet from this file and A11 only.

Both are frozen in FREEZE_CD_add5 before their first fresh run. None of these values is a hypothesis. Where this file and A11 differ, A11 wins.

## 1. Runs and arrays (as X, `CD_DEFINITIONS_X_v13.md` §0)
- **Fresh:** the 390 study positions of `crossing\CASES_X_PC_v13.json` (SHA-256 `58902be5ce022b314148308140cb8fc9373bc7aee401531367d456755409a31e`).
  - Replacements come from `crossing\REPLACEMENTS_X_v13.json` (a reserve of the same speed).
  - Job ids `pc13x_<case>_native`, in ascending run id. The analysed set is the listed runs whose arrays `arrays_x\CV0\<rid>.npz` exist.
  - Each run's `meta.family` must be `pedestrian_crossing`.
  - Gate: refuse unless `revision_v13\LOCK_A11.txt` exists.
- **Old-run test (`--test-old`):** the stored arrays of record of the 51 old pedestrian-crossing runs, every `*.npz` in `P\09_redesign\m2_decisions\openloop\gateR_rt_v01\` whose `meta.family` is `pedestrian_crossing`, in name order.
- **Keys used:** `evaluated`, `clear`, `vbar`, `idx55`, `cF0`, `cN`, `cE`, and `meta.desired` (fresh: `meta.desired`, written by the extractor).
- **Population:** all evaluated decisions. 3 s commitment; safe means `clean_clear(clear) > 0`.

## 2. Common inputs
- **u:** `trk_score_v01.e5_u(runs, 'F0', 'E')`, the per-decision rank variable of record (the same u as X's E5_N).
- **ratios:** `trk_score_v01.margin_ratios(runs, 'N', 'F0')`: √(cF0 / cN) over evaluated decisions and rows with both finite and > 0, pooled over runs in run order.
  - m_N = median(ratios); this is X's m_N.
- **Resamples:** `optA_lib_v02.boot_counts(n_runs, 20000, 20261911)` (C's draw). `--nboot` below 20,000 is for the old-run test only and uses the first rows.
- **Intervals:** where asked for, the 95% percentile interval (`np.percentile(x[finite], [2.5, 97.5])`) over the resamples, nominal. A ratio is undefined in a resample whose D_gl(E) ≤ 0.

## 3. E5q_N, sensitivity (A11 §3.6, third bullet)
- **Factor:** f_i = `np.quantile(ratios, u_i)` (numpy's default, linear) for each decision i. This is N's empirical ratio quantile at u_i: the full amplitude distribution with perfect ranking.
- **Critical scales:** E5q_N = cF0[i, ·] / f_i², as `add_oracle` scales F0.
- **Gridless step frontier** at 201 levels, as X (A10 §2.3):
  - `X.ped.RR_E5qN` = RR_gl(E5q_N);
  - `X.ped.RR_NmE5qN` = RR_gl(N) − RR_gl(E5q_N);
  - each with `.ci` (95% nominal) and `.level` = 0.95.

## 4. Grid frontier and placebo (A11 §3.6, fourth bullet; A9-1(a) as package C's S57B group 5)
- **Grid frontier of record:** the grid `[0] + logspace(-2, 3, 201)`; `optA_lib_v02.select_grid` / `stats_scored` / `eval_scoring` (via `rev_common_v01` tables and points, as C); W1 (the 3 s commitment); all evaluated decisions. F0's g = 0 point is prepended to every source except F0 and E.
- **Placebo:** P = F0's critical scales / m_N², with m_N from §2. This is the family's own median N/F0 ratio; A9-1(a) used N's median on lead braking, 1.1029.
- **Record-amplitude placebo:** P_rec = F0's critical scales / 1.1029², reported beside it.
- **Keys** (points only, as C; undefined if D(E) ≤ 0):
  - `X.ped.grid.RR_N` = D(N)/D(E), `X.ped.grid.RR_P` = D(P)/D(E), `X.ped.grid.RR_NmP` = (D(N) − D(P))/D(E);
  - `X.ped.grid.RR_Prec`, `X.ped.grid.RR_NmPrec`;
  - `X.ped.grid.R` = D(E)/201; `X.ped.grid.m_N` = m_N.

## 5. Partial oracles and the grading check (A11 §3.6, fifth bullet; A10 §5.7 C3; as C's S57A §4)
- **u_po:** `numpy.random.default_rng(20261919).random(N_total)`, where N_total is every decision in the arrays of the analysed runs (evaluated or not), assigned in ascending run id and, within a run, in array order (ascending k).
- **Partial oracle** with share p ∈ {0.25, 0.5, 0.75}: crit_Pp = `where((u_po < p)[:, None], cE, cF0)`.
- **Values:** PO_p = RR_gl(P_p), on the gridless step frontier. Points only.
  - `X.ped.PO25`, `X.ped.PO50`, `X.ped.PO75`.
  - `X.ped.PO25.dec`, `.PO50.dec`, `.PO75.dec` = dec_eq(D_gl(P_p), n) = D/201/100·n. These are printed instead of the shares where grading fails.
- **Grading check:** `X.ped.grading_ok` (bool) is true if PO25 > 0 and PO25 < PO50 < PO75 strictly; false if any is null.

## 6. Output
- First program: `crossing\out\[TESTOLD_]X_DESC_pedestrian_crossing_v13[_b<n>].json`.
- Second program: `recount\out\[TESTOLD_]RC_X_DESC_pedestrian_crossing_v13[_b<n>].json`.
- Each has a flat `values` dict with exactly the keys above, plus `X.ped.desc.n_runs` and `X.ped.desc.n_dec`. An undefined number or interval is null. Never overwrite an output.
- Comparison: within 1e-9; counts, booleans and levels exact.
- Laptop rules: one heavy process; BelowNormal priority; `OPENBLAS_CORETYPE=Haswell`; `NUMBA_NUM_THREADS=2`.
