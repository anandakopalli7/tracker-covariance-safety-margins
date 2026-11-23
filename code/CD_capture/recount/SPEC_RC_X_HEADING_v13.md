# Second program: crossing margin ratio against heading, schedule and realised error (EXPLORATORY)

Written 22 Nov 2026 by session CD (Claude Opus 5.5) for an independent second program on Claude Sonnet 5.5. Sprint panel item E4 / S4 (R2 F1); coordinator's A12 task 4. It tests nothing: every value is descriptive.

## Inputs

`work\CD_capture\crossing\heading\pc13x_*.npz`: 390 files, one per X study run, written by the first program's extraction. Each file is per decision tick (length n_dec, about 300), with these keys:

| Key | Meaning |
|---|---|
| `k` | tick |
| `status` | 0 evaluated, 1 contact-truncated, 2 truncated, 3 no truth match (NaN for none) |
| `prim` | index of the primary actor, or NaN |
| `bind_ok` | 1 when a binding constraint was found, 0 when none, NaN when not attempted |
| `y_bind` | 0.5·ln(Pr/Sbar) at the binding constraint |
| `cos_phi` | cosine between the tracker's velocity estimate and the constraint normal; NaN when speed ≤ 0.5 m/s |
| `speed` | speed of the velocity estimate |
| `e_n` | realised error along the normal, divided by sqrt(Sbar) |
| `te` | look-ahead of the binding constraint (s) |
| `offset` | offset of the binding constraint |
| `age_s` | track age (s) |
| `age_upd` | track age in updates |
| `miss` | updates since the last detection |
| `y_dec` | 0.5·ln(cF0/cN) at row idx55 |
| `chkF0`, `chkN` | cF0 and cN at idx55 |
| `vx`, `vy` | velocity estimate, planner frame |
| `P` | (n, 4, 4): the actor's state covariance [x, y, vx, vy], planner frame; NaN where there is no primary actor |
| `Pbar` | (n, 4, 4): the class P-bar |
| `evaluated`, `prim_idx` | from the stored arrays of record |
| `meta` | JSON string |

## Part 1: recount of the analysis

Write `work\CD_capture\recount\rc_x_heading_v13.py`, which writes `recount\out\RC_X_HEADING_v13.json` (never overwritten).

**Selection.** Process the files in ascending file-name order. A tick is analysed when all of these hold:
- `status == 0` and `bind_ok == 1`;
- `cos_phi` is finite;
- `y_bind`, `cos_phi`, `te`, `miss`, `age_upd` and `e_n` are all finite.

**Variables.**
- y = `y_bind`.
- Regressors, in this column order:
  - x1 = cos_phi²;
  - x2 = te;
  - x3 = miss;
  - x4 = ln(1 + age_upd);
  - x5 = |e_n|.
- Groups:
  - geometry = {x1, x2};
  - schedule = {x3, x4};
  - error = {x5}.

**OLS.** Fit with an intercept, pooled over all analysed ticks.
- Compute R² for every subset of the 5 regressors (the intercept always included): R² = 1 − SSR/SST, with SST about the mean.
- Report the coefficients of the full model.

**Shapley (LMG) by group.** This is exact over the 3 groups. For group g,
  sh_g = Σ over subsets S of the other groups of |S|!·(3 − |S| − 1)!/3! · [R²(S ∪ g) − R²(S)],
where R²(S) is the R² of the model with the regressors of the groups in S (R² of the empty set = 0).

Report:
- `r2_full`;
- `shapley_r2`, by group;
- `shapley_share_of_r2` = sh_g / r2_full;
- `r2_single_group`, by group.

**Run-clustered bootstrap.**
- The unit is a run, and only runs with at least one analysed tick enter, in file order.
- Use `rng = numpy.random.default_rng(20261951)` and B = 2000. For each b:
  - `idx = rng.integers(0, n_runs, n_runs)`;
  - `c = numpy.bincount(idx, minlength=n_runs)`;
  - weight each run's ticks by c (equivalently, stack c copies);
  - recompute r2_full and the three Shapley values.
- Intervals are percentile 2.5 / 97.5 with numpy's default linear percentile: `r2_full_ci95`, `shapley_r2_ci95`.

**The same for y_dec.**
- Within the analysed ticks, keep only those with finite `y_dec`.
- Runs with no such tick are dropped before the bootstrap.
- The same regressors, groups, bootstrap and seed. Restart the rng for this block, i.e. a new `default_rng(20261951)`.

**Spearman.** Spearman ρ uses average ranks (Pearson correlation of `scipy.stats.rankdata` ranks) of y with each of x1…x5, pooled. It is computed for y_bind on the analysed ticks and for y_dec on its subset.

**Object-frame check** (analysed ticks):
- Take the 2×2 position block of `P` and use `numpy.linalg.eigh`.
- The major axis is the eigenvector of the larger eigenvalue.
- With u = (vx, vy)/|(vx, vy)|, compute |sin| of the angle between the major axis and u: |m_x·u_y − m_y·u_x|.
- The axis ratio is sqrt(λ_max / λ_min).
- Report, for each of the two:
  - median, IQR (25/75) and the 5/95 percentiles;
  - the share with |sin| < sin 10° ("aligned");
  - the share with |sin| > cos 10° ("across").

**Counts.** Report:
- n_runs;
- ticks: all, evaluated (status 0), primary (status 0 and finite prim), binding (status 0 and bind_ok 1), analysed;
- for y_bind: median, IQR and SD (numpy std, ddof 0).

## Part 2: independent per-tick check on three runs

From the logs, recompute `y_bind`, `cos_phi`, `e_n`, `te` and `y_dec` for three runs:
- `pc13x_c1109_eval_0002_native`;
- the median-numbered run of the sorted list;
- the last run.

**How to compute them.**
- Use the modules of record exactly as `work\shared\trackers\trk_arrays_v01.py` (`extract`) does: library rows, D, Pr, `gc.geometry`, `gc.s_P` with the class P-bar of record, `gc.crit_rows`, `gc.match_many`, `oc.match_actors`, `ox.window_truth(T, k, kmax, draw, False)`, `gc.planner_centres`.
- For the primary actor at row idx55 (the library row whose `targets == (-5., -5.)`), over its 120 constraints:
  - j* = argmin of D²/Sbar, where Sbar > 0 (otherwise +inf); undefined if any of its D < 0.
  - y_bind = 0.5·ln(Pr_j*/Sbar_j*).
  - The normal n = N[idx55, 120·prim + j*].
  - te = TE[120·prim + j*].
  - For the constraint position p = offset + (j* mod 60), with offset = j* // 60: e = truth centre[p] − MU[prim][p], and e_n = (n·e)/sqrt(Sbar_j*).
    - The truth centres are `gc.planner_centres(tr['ego'], wt[m[prim]][0])`, where m is the first return value of `gc.match_many` (truth id per actor) and wt is the window truth above.
    - A tick has no primary actor when `gc.match_many` returns prim None, or `oc.match_actors` gives no index, or m[prim] is None.
  - cos_phi = (v·n)/|v|, with v the actor's velocity estimate from `consumer.finite_array([a[k] for k in gc.ACTOR_KEYS])[2:4]`, and NaN if |v| ≤ 0.5.
- y_dec = 0.5·ln(cF0[idx55]/cN[idx55]).

**Logs.** Each archive is `work\CD_capture\archives\<capture id>\claude_main_<id>.tar.gz`. These three runs have no retry alias. Extract each to a temporary folder under your scratch area, skipping `raw/` and `clean/` .npy members; delete it after use.

**Comparison.** Compare with the npz values (equal NaN pattern; maximum absolute difference) and write the result into the same JSON under `per_tick_check`.

**Rules.**
- Laptop: one process, BelowNormal priority, `python -I -B`.
- Use the CD venv: `work\CD_capture\.venv\Scripts\python.exe`.
- Never open anything named `<excluded folder 1>` or `<excluded folder 2>`, nor `<user folder>`.
- Do not read `crossing\x_heading_v13.py` or `crossing\x_heading_analyse_v13.py` (the first programs).
- No pods, no network.
