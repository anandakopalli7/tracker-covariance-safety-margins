# TU.RR_TG, second program (v03 addition), written 21 Nov 2026

**Shared inputs and independence.** The second program shares the rebuilt TG arrays (`B_retrack\out\tu\tg\<run>.npz`, the first
program's A9-7 rebuild; for old runs revision_v12 `out\tg\<run>.npz`) and the draws (`optA_lib_v02.boot_counts(20, 20000, 20261918)`), as
A10 s10.1(b) allows and as for the other TU keys. **Computed here, independently:** the gridless and grid frontiers, the shares
(RR_gl(TG) = D_gl(TG,F0)/D_gl(E,F0), grid RR(TG)) and the percentile intervals. I did **not** read `B_retrack\code\` (in particular
`b_tu_tg_v03.py`, `b_tu_v03.py`, `b_fresh_export_v03.py`), `shared\trackers\` or `CD_capture\analysis\`. Frozen files (`recount_fresh.py`,
`rf_core.py`, `b6tu.py`) are unchanged and imported.

## Files
`tu_tg_v03.py`, this README. Outputs: `out\TESTOLD_TU_TG_v03.json` (test); later `out\part_tu_tg_v03.json`, `out\boot_tu_tg_v03.npz`.

## CLI (`python -I -B -X utf8 tu_tg_v03.py ...`)
- `--test-old [--K n]`: 35 old runs (`p1b_fit_finite_0005..0039`), cTG2 from v12 `out\tg`; points (gridless, grid); K = 0 by default
  (optional bootstrap over the 35-run draw of record, a code-path check only).
- `--tuning [--K 20000]`: 20 tuning runs (name order of `B.tu_load`), cTG2 from `out\tu\tg`; **not run yet** (freeze first).
  Writes flat `TU.RR_TG`, `TU.RR_TG.ci` and `boot_tu_tg_v03.npz` (denE, D_TG per resample).
- `--combine-tg`: adds the two keys to `B_retrack\out\A_RECOUNT_B.json`; refuses if a key is already present or any existing value
  would change; keeps the old file as `A_RECOUNT_B_v02_220keys.json` (tested on a scratch copy only).

## Method
Same engine and scoring as the other TU keys (`b6tu.tu_compute`): evaluated decisions, W1 scoring, TG's step frontier on its own
breakpoints (gridless), point 0 = F0's zero-margin point, levels/sums by `eval_scoring`; grid on the 202-value grid. cTG2 (r0 = 2 m/s)
is checked to have the same k as the record. CI: 95% percentile over resamples with denE > 0.

## Test on old runs (35 runs, v12 cTG2)
Grid RR(TG2) = 0.3142172109901504, D_TG2 = 144.7462686567164 decision-equivalents, R_pp = 5.556775831337881, n = 8290: **identical
to the digit** to `A9_7B_TIMEGAP_SCORE_v01.json` w1.all (0.3142172109901504, 144.7462686567164, 5.556775831337881, 8290.0).
Gridless RR_gl(TG2) = 0.3212018942899134 (D_gl 146.786 dec-eq, R_gl 5.5125 pp); v12 has no gridless TG value to compare.
Timing: points 1.8 s; bootstrap 17 ms per resample on 35 runs (so 20 runs at K = 20,000 about 3-6 min).
