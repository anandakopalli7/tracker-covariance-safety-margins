# Y (AMENDMENT_11_v13.md §6b): definitions of package CD's analysis

Written 21 Nov 2026, about 14:30 EST (Claude Opus 5.5, session CD), before LOCK_A11 and before any Y value. This file and A11 §6b are the specification for both programs. The first program is `ycheck\y_twin_v13.py`; the second (Claude Sonnet) is written from A11 §6b and this file only. Where they differ, A11 wins. The points marked **[fixed here]** are ones A11's text leaves open.

## 1. Data
- **Runs:** the 105 fresh lead-braking runs, `pc13_<case>_native` over `CASES_C_v13.json` lead_braking (`REPLACEMENTS_C_v13.json` is empty), in ascending run id. This is C's run order (`cd_common_v13.c_run_ids('lead_braking')`).
- **B2 arrays:** `work\B_retrack\out\retrack_fresh\B2\<rid>_arrays.npz`.
  - Each file's SHA-256 must equal its entry in `work\locks\FREEZE_B_add7.json` (`arrays_B2_fresh`), and that manifest's SHA-256 must be `d06cc48bbe89ec87b3927c962c041b31b5e7aab1dccbe570188a331e0a7b0c12`. A program refuses otherwise.
  - Keys used: `evaluated`, `clear`, `vbar`, `idx55`, `cF0` (F0_B2 = the class average with P̄_B2), `cN` (N_B2), `cE` (E_B2).
- **Online-N reference:** CD's arrays of record `work\CD_capture\arrays\CV0\<rid>.npz`: `cF0` with the P̄ of record, `cN`, `cE`, and the same other keys.

## 2. Population, scoring, frontier
These are A10 §2 and as C:
- **Population:** all evaluated decisions (`evaluated == 1`).
- **Scoring:** the 3 s commitment, with safe meaning `clean_clear(clear) > 0`.
- **Frontier:** the gridless step frontier at 201 levels, on the variant's own room. For B2, F0 = F0_B2 and E = E_B2 (A10 §2.1); for the reference, the record's F0 and E.
- **Definitions:** D_gl(A) = Σ(F_F0 − F_A); RR_gl(A) = D_gl(A) / D_gl(E). A ratio is undefined when D_gl(E) ≤ 0.

## 3. Factor and twins
- **Factor:** for decision i, f_i is the median over its candidate rows r (the 17 columns) with finite, positive cF0[i, r] and cN[i, r] of √(cF0[i, r] / cN[i, r]). Decisions without such a row have no factor.
- **Scaled twin B2s:** for decisions with a factor, crit[i, r] = cF0[i, r] / f_i² (as `trk_score_v01.add_oracle` scales F0). Decisions without a factor keep N's own scales, cN[i, ·] **[fixed here]**.
- **Permuted twins B2p_k, k = 1 … 20:**
  - One generator, `numpy.random.default_rng(20261931)`, drawn once before any value **[draw order fixed here]**.
  - For k = 1 … 20 (outer loop), and for each run in ascending run id (inner loop): let J be the run's decisions that are evaluated and have a factor, in ascending decision index. Draw `perm = rng.permutation(len(J))`; then twin k has f_π(J[j]) = f_J[perm[j]].
  - Crit is cF0 / f_π(i)² on J. All other decisions keep cN.
  - A run with len(J) = 0 still calls `rng.permutation(0)`, which consumes no draws.
  - The permutations are fixed per run and not redrawn per resample.
- **RR_gl(B2p):** the mean over k of RR_gl(B2p_k), taken within each resample (or the full sample).
- **Online-N reference:** the same construction on the CV0 arrays (cF0 of record, cN), with its own generator `default_rng(20261931)` drawn in the same order **[fixed here]**.

## 4. Statistics and intervals
- **Δ = RR_gl(N_B2) − RR_gl(B2p)**, the Y1 statistic.
  - Interval: the percentile interval over the 20,000 run resamples `optA_lib_v02.boot_counts(105, 20000, 20261911)` (the C draw, runs in ascending id).
  - Level: A10 §2.6's calibrated level (double bootstrap 2,000 × 1,000, seeds 20261912/20261913, check seeds 20261914 and 20261920, as C), with the twins fixed as above.
  - Emergency rule (A11 §3.7): the nominal 99% interval if the calibration has not finished by 21:15.
- **Descriptive, nominal 95%:**
  - RR_gl(N_B2); RR_gl(B2s); RR_gl(B2p); Δs = RR_gl(B2s) − RR_gl(B2p);
  - for the online reference: RR_gl(N); RR_gl(Ns); RR_gl(Np); ΔN = RR_gl(N) − RR_gl(Np); ΔsN = RR_gl(Ns) − RR_gl(Np).
- **Counts:** runs; evaluated decisions; evaluated decisions with a factor (B2 and reference); the share of resamples with D_gl(E) > 0.
- **Y1** passes if Δ's lower end > 0.

## 5. Outputs (flat `values`, prefix `Y.`)
- Counts: `Y.n_runs`, `Y.n_dec`, `Y.n_factor`, `Y.n_factor_ref`, `Y.share_pos`.
- Main statistic: `Y.delta`, `Y.delta.ci`, `Y.delta.level`, `Y.Y1` (bool).
- Descriptive, each X with `.ci` and `.level` (0.95):
  - `Y.RR_NB2`, `Y.RR_B2s`, `Y.RR_B2p`, `Y.delta_s`;
  - `Y.ref.RR_N`, `Y.ref.RR_Ns`, `Y.ref.RR_Np`, `Y.ref.delta`, `Y.ref.delta_s`.
- `Y.R` and `Y.ref.R` (room in pp at the full sample).
- First program: `ycheck\out\Y_TWIN_v13.json`. Second program: `recount\out\RC_Y_TWIN_v13.json`. Old-run tests carry a `TESTOLD_` prefix.
- **Old-run test:** on the 35 old evaluation runs (C's H4 design set, `cd_common_v13.load_old_lead`; `crit` F0, E and N of record), as the online-N reference only. B2 has no old-run arrays in this layout. Both programs must agree on the keys of the reference.
- **Comparison:** within 1e-9; counts and booleans exact.

## 6. Gate
Both programs refuse a fresh value unless `revision_v13\LOCK_A11.txt` exists.
