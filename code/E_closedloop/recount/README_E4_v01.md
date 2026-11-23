# README_E4_v01: second program for set E4 (detection dropout, A11 6c/6d)

Written from `E_DROPOUT_A11_6d_v01.md` and the coordinator's final mask law; the first program was not read. `e_recount_v04.py` is `e_recount_v03.py` plus the items below (nothing else changed; regression on the synthetic sets identical to v03). Single process, light memory.

## Mask law (one place: `dropout_mask`, `draw_L`)
Seed `int.from_bytes(sha256("A11/D/" + case_id).digest()[:8], "big")`, `numpy.random.default_rng`. Update row i is detector frame k = 19 + 10 i. Row 0 is never masked and draws nothing. From row 1, at a row not inside a window and not a gap row: `u = rng.random()`; if u < 0.10, `L = rng.integers(1, 4)` (the L draw call is only in `draw_L`, to change if F's line differs), rows i..i+L-1 are masked (cut at the last row), the row i+L is never masked and draws nothing, draws resume at i+L+1.

## outcomes (e4_ runs)
`outcomes <runs> e4_ --punish-num 3 --out X`. An e4_ run is invalid unless: the `dropout` block's `mask` and `windows` equal the law's for the case (windows exactly as logged: a list of [start_row, L] with L the drawn length, even when the mask is cut at the run end); every detection row's `masked` equals the law at its tick (k = 19 + 10 i), and `tracker_rows` is 0 if masked else `len(model)`; the `law` string is `A11D2`; `punish_num` is pinned to 3 (`--punish-num`, if given, must be 3); the case is in the locked table `out4_MASKS_v01.json` and this program's law mask equals the table's (differences are printed; `--masks-table none` switches the table check off, for tests). Extra row field `masked_share` = masked share of detector rows with k >= 99. A warning is written if the rows do not cover n_updates distinct ticks.

## compare_e4
`compare_e4 <e4 outcomes> --e3 <e3 outcomes> --jobs-dir jobs --out X`. At each level, N vs F0 and N_IMM vs F0_IMM, paired by case over valid runs; same statistics, classes and "no interval below 2 pairs" rule as `compare`. Exploratory: `deg` (each arm's E4 run vs its E3 twin, same comparison) and `did` (per case with all four runs valid at E4 and E3, [(arm-ref) contact E4] - [(arm-ref) contact E3]; mean; case bootstrap, fresh `default_rng(20261922)`, 20,000 resamples, percentile 2.5/97.5, no interval below 2 cases). A level is complete when every e4_ job id of `jobs\JOBS_E4L_*_v01.json` (lo) / `JOBS_E4H_*_v01.json` (hi) has a run of record; incomplete levels get no comparisons.

## Export: `e_recount_export_e4_v01.py`
`--e4 --compare-e4 --matched --punish-num [--status ran] --out out\A_RECOUNT_E4.json`. Format as the E export plus `"set": "E4"` and `lock_sha256` (of `revision_v13\LOCK_A11b.txt`, null if absent). Keys exactly those of `tests\out\E4_EXPORT_KEYS_v01.json` (179). Summaries as the E export (`.masked` = mean masked_share over valid runs; `.fallback` pooled). `.caution` from the matched recount (`caution` of the arm, F0: `F0_caution_at_gL`), percent. Undefined values and intervals are null. A level that is not complete is omitted (only the two `completed` flags remain).

## Tests (recount\test)
- `test_mask_law_v04.py`: 2,000 ids x 69 ticks: start rate, L shares, no stretch above 3, row 0 never masked, no window without a gap row; prints three masks.
- `make_synth_e4.py` writes `synth_e4\` (80 E4 + 80 E3 runs, masks by the law, three corrupted runs): the corrupted runs are invalid (mask, tracker_rows, punish_num); compare_e4, the export (179 keys, no missing or extra) and the incomplete-level case run.
- Not tested: real E4 data (none exists).
