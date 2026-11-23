# Recount4: independent second program for the scoring of the reaction-and-stop estimate

Written 18 Nov 2026. Brief: `RECOUNT4_BRIEF_v01.md` (this folder), with the inputs, scoring definitions and bootstrap of record of `revision_v11\recount\RECOUNT_BRIEF_v01.md`.

## Result in short

- The scoring behind Tables III and IV was recomputed by a second program for every setting, every population and both variants: 17 scorings (the estimate at 9 settings, censored pairs unsafe at the 6 settings with 6 m/s2, signed caution and the 3 s window at 0.75 s and 6 m/s2), 6 populations each, points and 95% percentile intervals of the draw of record (20,000 resamples), and the pair counts at 9 settings. That is 10782 numbers on the brief's list.
- Compared with the first program (`REV_E2_EXTENDED_TRUTH_v01.json`): **8618 numbers, 0 differ by more than 1e-9** (largest absolute difference 2.8e-14). 5082 of them are on the brief's list (class A), 3077 are further entries that were in the results file or follow from it by arithmetic (class B), and 459 were recomputed after the first program's file was opened (class C).
- 5700 numbers on the brief's list have no counterpart in the first program's file, because the first program did not bootstrap every scoring and did not score every source in every scoring (list under "Comparison"). They stand on the second program alone and are covered only by its self-check.
- Entries of the first program's file not compared: the scorings `ii_*` and `est_gap2_*` (242 numeric entries each; outside this brief), the 17 `bootstrap` switches and `seconds`.
- Self-check by a second route (`r4_naive_v01.py`, finished before the first program's file was opened): 1296 points and 4374 values of three resamples per scoring recomputed without the libraries' scoring code, largest difference 5.7e-14; all 19788 intervals, shares and ratios of the results file recomputed from the stored resamples with a hand-written percentile, largest difference 5.7e-14; 126 pair counts recounted, 0 differ.
- Headline values (0.75 s, 6 m/s2, all 8290 evaluated decisions): den0 = 0.7093 [0.2584, 1.2286] pp = 58.80 [20.90, 103.23] decision-equivalents; denE = 0.6793 [0.2491, 1.1721] pp; relative to the 3 s commitment denE 0.1222 [0.0518, 0.1879] and den0 0.1183 [0.0504, 0.1820]. With censored pairs unsafe: den0 = 0.8386 [0.3697, 1.3806] pp = 69.52 [31.04, 113.19] decision-equivalents.

## Record made before the first program's file was opened

- `RECOUNT4_RESULTS_v01.json` written 18 Nov 2026 19:14:20, sha256 `b5d428524e066e270d52cc31057c23d5c5accf4b1d88659391a5cfcb2f66f04c` (also in `RECOUNT4_RESULTS_v01.sha256.txt`, written by the program itself).
- Program at that moment: `r4_items_v01.py` sha256 `bef455ca89b045fe167ae04d85df7655da088e823118a630fea9e87400f8f786`.
- Self-check by a second route finished before the comparison: `r4_naive_v01.py` (sha256 `5428c121c10e7ecce7706922e6851724e82cb206afc049b8229f48f459936bd4`), output `r4_naive_v01_out.json` (sha256 `12e57e78e5dc7fdc543c6fe672f67482c5327d5d73742a7ac63ca9453be9378f`).
- This record was written 18 Nov 2026 19:18. Up to this moment nothing of `revision_v11\analysis`, `revision_v11\draft`, `revision_v11\package_v11` or `P\11_ojits\A6R\code` had been opened.
- Readings of the brief fixed before the comparison (details in "Ambiguities" below, written after it without changing them):
  1. "Relative to 3 s": denominator = the 3 s commitment scoring (unsafe when `clear` <= 0), entry `rel.3s_commitment`. A second denominator, the 3 s-window scoring at the same setting (`clear61`), is stored as `rel.3s_window_same_setting` as an addition.
  2. `est_signed`, relative to 3 s: `rel.3s_commitment` uses the 3 s commitment with the paper's caution (literal reading, taken as the primary one); `rel.3s_commitment_signed` uses the 3 s commitment with signed caution.
  3. `cens`: a pair is unsafe when `clearX` <= 0 or `cens` is true.
  4. Shares "den <= 0" are over all 20,000 resamples.
  5. "Unsafe on the 3 s window" in the pair counts: `clear61` <= 0.
  6. Intervals of sums, percentage points and decision-equivalents: over all resamples with a finite value; intervals of ratios: over the resamples with a positive denominator.

## Independence and order of work

- Read before the program was written: the two briefs; `revision_v11\recount\rc_lib_v01.py`; `revision_v11\recount3\r3_lib_v01.py`, `r3_items_v01.py`, the start of `r3_naive_v01.py`, `RECOUNT3_REPORT_v01.md` and the timing log; of `revision_v11\recount2`: `recount2_score_v01.py`, the headers of `recount2_ext_v01.py` and `probe_v01.py`, the start of `RECOUNT2_SCORING_v01.json`. Arrays opened: the stored runs, the extraction, the pack cache (through `rc_lib_v01.load_all`) and `recount2\out`.
- Not opened before the results file was hashed: anything of `revision_v11\analysis`, `revision_v11\draft`, `revision_v11\package_v11`, `P\11_ojits\A6R\code`. Not opened at any time: `revision_v11\draft`, `revision_v11\package_v11`, `<excluded folder 1>`, `<excluded folder 2>`, `<excluded folder 3>`. No network. Nothing was written outside this folder; Python ran with `-B`. (A listing of files changed since the brief, made at the end to confirm this, showed names of files in `revision_v11\analysis`, `revision_v11\draft` and `revision_v11` itself that other sessions changed in the meantime; none was opened or written by this recount.)
- Order: program (`r4_items_v01.py`), test on 400 resamples, full run, self-check (`r4_naive_v01.py`), record of the hashes, and only then the first program's file. After that, to learn the meaning of entries the brief does not list (`outside`, `basic`, `branch`, `oracle_diag`), `revision_v11\analysis\rev_e2_extended_truth_score_v01.py`, `rev_common_v01.py` and parts of `P\11_ojits\A6R\code\optA_lib_v02.py` were read.
- Nothing in the program or in the results file was changed after the comparison. `RECOUNT4_RESULTS_v01.json` still has the recorded hash (`r4_compare_v01.py` refuses to run otherwise). Written after the comparison: `r4_compare_v01.py`, `r4_diag_v01.py`, `r4_extra_v01.py`, `r4_report_v01.py` and the helpers `r4_peek*_v01.py`.

## Inputs and checks on them

- 35 evaluation runs, 9307 stored decisions, 8290 evaluated; by phase: 678 before onset, 755 lead braking, 6857 lead stopped, 0 unknown; ego moving: 1863.
- `k` and the evaluated flags of `recount2\out` equal the stored ones in every run (the program stops otherwise).
- NaN among evaluated decisions: 3 s clearance 0; `clearX` 0 and `clear61` 0 over all nine settings.
- In every setting `clearX` <= `clear61` for every pair (0 pairs above), `clearX` = `clear61` wherever `late` is false (0 pairs differ), and every censored pair is late (0 not late).
- The pack cache clearance (the first program's "as scored") and recount2's own `clear61` give the same safe flag for every pair in all nine settings (0 flags differ; 0 values differ by more than 1e-9).
- Anchor inside the second-program lineage: the points of recount2's optional scoring (`RECOUNT2_SCORING_v01.json`: 3 s commitment, 3 s window, estimate, censored pairs unsafe; all and ego moving; denE and den0) are reproduced, largest difference 0.0e+00 (16 values).

## Method

- Wrong go of a scoring: the selected row is not judged safe by it. `est`: safe when `clearX` > 0. `cens`: safe when `clearX` > 0 and `cens` is false. `asscored`: safe when `clear61` > 0. Reference `w1` (the 3 s commitment): safe when `clear` > 0.
- Caution always uses the 3 s commitment: truly safe rows and the first truly safe row from `clear` > 0; caution = mean over evaluated decisions whose selected row is truly safe of (speed of the first truly safe row - speed of the selected row) / desired speed, in %. Signed caution: mean over every evaluated decision with a truly safe row, at its signed difference.
- Grid of 202 margin scales, selection of the first row whose critical scale is >= the scale (fallback row otherwise), step frontier on 201 levels from F0's zero-margin caution to min(largest caution of F0, largest caution of E), levels rebuilt in every population and resample; every arm other than F0 and E, and the perfect oracle O, get F0's zero-margin point in front. denE = sum over levels of F_F0 - F_E; D(A) likewise; den0 = D(O), O = per decision the first row the scoring judges safe (fallback row if none). Percentage points = sum / 201; decision-equivalents = sum / 201 / 100 x n with the resample's own n.
- Populations: all evaluated; ego moving (`v0` > 0.5); phases 0, 1, 2; phase-weighted = sum over phases 0-2 of (n_p / n) x the phase's sum, n = n_0 + n_1 + n_2, ratios formed from the aggregated sums.
- Bootstrap of record: `numpy.random.default_rng(20261113).integers(0, 35, size=(20000, 35))`. Each run is reduced to per-scale counts (wrong-go count, caution sum, caution count per population and arm), so a resample is a weighted sum of 35 vectors. Intervals: `numpy.percentile` at 2.5 and 97.5; for ratios over the resamples with a positive denominator, the number left out is stored.
- Relative to 3 s: denE (or den0) of the scoring divided by denE (den0) of the 3 s commitment, numerator and denominator from the same resample.
- Code: `r4_items_v01.py` uses `rc_lib_v01.load_all` and `run_row` (loader, selection, per-run statistics, signed caution), `r3_lib_v01.evaluate_g`, `boot_g`, `weighted`, `ci_ratio`, `ci_plain` (frontier, bootstrap, aggregate, intervals). The safe flags of the four scorings, the references, the ratios to 3 s, the shares, the decision-equivalents and the pair counts are written in `r4_items_v01.py`. The per-resample sums are kept in `boot\<scoring>.npz`.
- Self-check (`r4_naive_v01.py`), sharing only the loader and the grid: decisions concatenated, selection by a loop over rows, unsafe flags written out again, levels by `numpy.linspace`, frontier by a loop over levels; all 1296 points (27 scorings x 6 populations x n, denE, den0, D of five sources) and resamples 0, 7 and 19999 of the draw (4374 values); every summary of the results file from the stored resamples with name-based column lookup and a hand-written percentile (19788 values); the pair counts with other expressions (126). Largest difference 5.7e-14; no mismatch. Limit of this check: its second part tests the summaries, not the 20,000 resampled sums themselves, of which three per scoring are tested by the first part.

## Results

All numbers, with intervals, are in `RECOUNT4_RESULTS_v01.json` (`scorings.<name>.pops.<population>`; `counts.<setting>`). Intervals in brackets are 95% percentile intervals of the draw of record.

### The estimate, all evaluated decisions (n = 8290), by setting

| Setting | den0 (pp) | den0 (decision-equivalents) | denE (pp) | denE / denE(3 s) | den0 / den0(3 s) | Share of resamples den0 <= 0 / denE <= 0 |
|---|---|---|---|---|---|---|
| 0.50 s, 6.0 m/s2 | 0.1124 [0.0000, 0.3293] | 9.32 [0.00, 27.22] | 0.1038 [0.0000, 0.3027] | 0.0187 [0.0000, 0.0517] | 0.0187 [0.0000, 0.0517] | 0.1280 / 0.1280 |
| 0.75 s, 6.0 m/s2 | 0.7093 [0.2584, 1.2286] | 58.80 [20.90, 103.23] | 0.6793 [0.2491, 1.1721] | 0.1222 [0.0518, 0.1879] | 0.1183 [0.0504, 0.1820] | 0.0000 / 0.0000 |
| 1.00 s, 6.0 m/s2 | 1.4088 [0.6777, 2.1935] | 116.79 [55.00, 184.65] | 1.3396 [0.6483, 2.0887] | 0.2411 [0.1365, 0.3308] | 0.2349 [0.1329, 0.3215] | 0.0000 / 0.0000 |
| 1.25 s, 6.0 m/s2 | 2.2667 [1.2915, 3.2615] | 187.91 [105.50, 274.50] | 2.1364 [1.2270, 3.0833] | 0.3845 [0.2589, 0.4879] | 0.3780 [0.2548, 0.4784] | 0.0000 / 0.0000 |
| 1.50 s, 6.0 m/s2 | 3.1979 [2.0350, 4.3584] | 265.11 [165.97, 366.23] | 2.9848 [1.8972, 4.0851] | 0.5371 [0.4047, 0.6434] | 0.5333 [0.4014, 0.6383] | 0.0000 / 0.0000 |
| 1.80 s, 6.0 m/s2 | 4.3711 [3.0254, 5.6389] | 362.37 [248.39, 473.01] | 4.0686 [2.8190, 5.2932] | 0.7322 [0.6012, 0.8291] | 0.7290 [0.5983, 0.8253] | 0.0000 / 0.0000 |
| 0.75 s, 4.0 m/s2 | 1.7168 [0.8367, 2.6484] | 142.32 [68.46, 222.82] | 1.6273 [0.8001, 2.5138] | 0.2929 [0.1677, 0.3995] | 0.2863 [0.1641, 0.3919] | 0.0000 / 0.0000 |
| 0.75 s, 5.0 m/s2 | 1.0378 [0.4120, 1.7288] | 86.03 [33.75, 145.30] | 0.9919 [0.3962, 1.6542] | 0.1785 [0.0836, 0.2635] | 0.1731 [0.0812, 0.2558] | 0.0000 / 0.0000 |
| 0.75 s, 7.6 m/s2 | 0.3723 [0.0795, 0.7382] | 30.86 [6.47, 61.79] | 0.3540 [0.0765, 0.7014] | 0.0637 [0.0155, 0.1133] | 0.0621 [0.0150, 0.1105] | 0.0005 / 0.0005 |

RR0 (share of den0), all evaluated decisions:

| Setting | N | NA | AM | CK3 | Q | E |
|---|---|---|---|---|---|---|
| 0.50 s, 6.0 m/s2 | -0.0027 [-0.0098, 0.0208] | -0.0048 [-0.0106, 0.0194] | 0.5729 [0.4489, 0.7153] | 0.8793 [0.8395, 0.9448] | -0.1447 [-0.2165, 0.0376] | 0.9237 [0.8683, 0.9887] |
| 0.75 s, 6.0 m/s2 | 0.0004 [-0.0058, 0.0054] | 0.0118 [-0.0038, 0.0390] | 0.5699 [0.4718, 0.6637] | 0.9360 [0.9078, 0.9586] | -0.0313 [-0.0737, 0.0133] | 0.9577 [0.9200, 0.9878] |
| 1.00 s, 6.0 m/s2 | 0.0008 [-0.0049, 0.0037] | 0.0145 [0.0028, 0.0334] | 0.5364 [0.4575, 0.6184] | 0.9432 [0.9194, 0.9621] | -0.0255 [-0.0483, 0.0004] | 0.9509 [0.9084, 0.9860] |
| 1.25 s, 6.0 m/s2 | 0.0010 [-0.0030, 0.0017] | 0.0231 [0.0082, 0.0427] | 0.5060 [0.4315, 0.5812] | 0.9434 [0.9180, 0.9621] | -0.0160 [-0.0322, -0.0040] | 0.9425 [0.8881, 0.9853] |
| 1.50 s, 6.0 m/s2 | 0.0011 [-0.0016, 0.0013] | 0.0216 [0.0098, 0.0346] | 0.4522 [0.3838, 0.5156] | 0.9329 [0.9048, 0.9538] | -0.0117 [-0.0243, -0.0025] | 0.9333 [0.8669, 0.9838] |
| 1.80 s, 6.0 m/s2 | 0.0011 [-0.0012, 0.0012] | 0.0192 [0.0087, 0.0299] | 0.3861 [0.3215, 0.4425] | 0.8447 [0.7907, 0.8874] | -0.0077 [-0.0167, -0.0015] | 0.9308 [0.8612, 0.9828] |
| 0.75 s, 4.0 m/s2 | -0.0001 [-0.0042, 0.0024] | 0.0129 [0.0030, 0.0287] | 0.4887 [0.4132, 0.5670] | 0.9493 [0.9280, 0.9668] | -0.0149 [-0.0337, 0.0063] | 0.9479 [0.9001, 0.9863] |
| 0.75 s, 5.0 m/s2 | 0.0005 [-0.0042, 0.0040] | 0.0131 [0.0008, 0.0358] | 0.5420 [0.4588, 0.6248] | 0.9458 [0.9212, 0.9645] | -0.0224 [-0.0519, 0.0100] | 0.9558 [0.9171, 0.9879] |
| 0.75 s, 7.6 m/s2 | -0.0026 [-0.0078, 0.0083] | 0.0089 [-0.0043, 0.0338] | 0.5973 [0.4811, 0.7141] | 0.9167 [0.8815, 0.9473] | -0.0495 [-0.1151, 0.0253] | 0.9508 [0.9056, 0.9877] |

### The estimate at 0.75 s and 6 m/s2, by population

| Population | n | den0 (pp) | den0 (decision-equivalents) | denE (pp) | denE / denE(3 s) | den0 / den0(3 s) | Share den0 <= 0 |
|---|---|---|---|---|---|---|---|
| All evaluated | 8290 | 0.7093 [0.2584, 1.2286] | 58.80 [20.90, 103.23] | 0.6793 [0.2491, 1.1721] | 0.1222 [0.0518, 0.1879] | 0.1183 [0.0504, 0.1820] | 0.0000 |
| Ego moving | 1863 | 0.6524 [0.2470, 1.0815] | 12.15 [4.34, 21.08] | 0.6206 [0.2379, 1.0510] | 0.0611 [0.0269, 0.0942] | 0.0623 [0.0269, 0.0950] | 0.0000 |
| Phase 0 (before onset) | 678 | 0.0000 [0.0000, 0.0000] | 0.00 [0.00, 0.00] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 1.0000 |
| Phase 1 (lead braking) | 755 | 0.1937 [0.0486, 0.3630] | 1.46 [0.33, 2.96] | 0.1937 [0.0486, 0.3630] | 0.0124 [0.0036, 0.0208] | 0.0123 [0.0035, 0.0205] | 0.0001 |
| Phase 2 (lead stopped) | 6857 | 0.0326 [0.0017, 0.0933] | 2.23 [0.11, 6.33] | 0.0264 [0.0012, 0.0739] | 0.0322 [0.0015, 0.0880] | 0.0334 [0.0018, 0.0916] | 0.0048 |
| Phase-weighted | 8290 | 0.0446 [0.0093, 0.1049] | 3.70 [0.75, 8.74] | 0.0395 [0.0088, 0.0891] | 0.0185 [0.0047, 0.0384] | 0.0196 [0.0047, 0.0422] | 0.0000 |

| Population | RR0(N) | RR0(NA) | RR0(AM) | RR0(CK3) | RR0(Q) | RR0(E) |
|---|---|---|---|---|---|---|
| All evaluated | 0.0004 [-0.0058, 0.0054] | 0.0118 [-0.0038, 0.0390] | 0.5699 [0.4718, 0.6637] | 0.9360 [0.9078, 0.9586] | -0.0313 [-0.0737, 0.0133] | 0.9577 [0.9200, 0.9878] |
| Ego moving | -0.0127 [-0.0313, 0.0065] | -0.0209 [-0.0571, 0.0204] | 0.2567 [0.1674, 0.3375] | 0.0381 [-0.4605, 0.3806] | -0.0438 [-0.0929, 0.0225] | 0.9513 [0.9400, 1.0000] |
| Phase 0 (before onset) | n/a | n/a | n/a | n/a | n/a | n/a |
| Phase 1 (lead braking) | -0.0034 [-0.0559, 0.0730] | -0.1531 [-0.3648, 0.0255] | -0.6769 [-1.5889, -0.1869] | -1.1088 [-4.6364, 0.5097] | -0.0476 [-0.2048, 0.2162] | 1.0000 [1.0000, 1.0000] |
| Phase 2 (lead stopped) | 0.0000 [-0.0319, 0.0465] | 0.0423 [-0.0245, 0.2500] | 0.3497 [-0.3636, 0.6471] | 0.7884 [0.6618, 1.0000] | -0.2517 [-0.5015, 0.0645] | 0.8107 [0.6525, 0.9824] |
| Phase-weighted | -0.0013 [-0.0293, 0.0377] | -0.0350 [-0.1303, 0.0783] | -0.0565 [-0.6932, 0.2084] | 0.0377 [-2.1639, 0.7045] | -0.1709 [-0.3026, 0.1111] | 0.8856 [0.7776, 0.9959] |

| Population | D(N) | D(NA) | D(AM) | D(CK3) | D(Q) |
|---|---|---|---|---|---|
| All evaluated | 0.02 [-0.32, 0.29] | 0.69 [-0.20, 1.90] | 33.51 [12.30, 57.70] | 55.03 [19.50, 96.33] | -1.84 [-5.57, 0.42] |
| Ego moving | -0.15 [-0.39, 0.07] | -0.25 [-0.80, 0.17] | 3.12 [1.01, 5.66] | 0.46 [-5.05, 5.30] | -0.53 [-1.46, 0.14] |
| Phase 0 (before onset) | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| Phase 1 (lead braking) | -0.00 [-0.07, 0.08] | -0.22 [-0.60, 0.02] | -0.99 [-2.17, -0.15] | -1.62 [-5.94, 0.71] | -0.07 [-0.28, 0.22] |
| Phase 2 (lead stopped) | 0.00 [-0.06, 0.04] | 0.09 [-0.04, 0.27] | 0.78 [-0.11, 2.37] | 1.76 [0.11, 4.68] | -0.56 [-1.82, 0.04] |
| Phase-weighted | -0.00 [-0.10, 0.08] | -0.13 [-0.51, 0.13] | -0.21 [-1.30, 1.07] | 0.14 [-4.04, 3.94] | -0.63 [-1.89, 0.15] |

(D in decision-equivalents. In phase 0 the estimate leaves no room at this setting: den0 = denE = 0 in the full sample and in every resample, so no ratio exists there; the same holds in both programs.)

### Censored pairs unsafe, all evaluated decisions, by setting

| Setting | den0 (pp) | den0 (decision-equivalents) | denE / denE(3 s) | den0 / den0(3 s) | RR0(AM) | RR0(CK3) | RR0(E) |
|---|---|---|---|---|---|---|---|
| 0.50 s, 6.0 m/s2 | 0.1726 [0.0212, 0.4059] | 14.31 [1.85, 32.69] | 0.0289 [0.0038, 0.0644] | 0.0288 [0.0037, 0.0642] | 0.3905 [0.0087, 0.6478] | 0.7201 [0.2220, 0.9105] | 0.9315 [0.8777, 0.9845] |
| 0.75 s, 6.0 m/s2 | 0.8386 [0.3697, 1.3806] | 69.52 [31.04, 113.19] | 0.1442 [0.0726, 0.2121] | 0.1399 [0.0706, 0.2060] | 0.4919 [0.3409, 0.6128] | 0.8288 [0.6232, 0.9458] | 0.9557 [0.9174, 0.9862] |
| 1.00 s, 6.0 m/s2 | 1.6103 [0.8528, 2.4307] | 133.50 [71.63, 199.88] | 0.2746 [0.1702, 0.3678] | 0.2686 [0.1662, 0.3600] | 0.4765 [0.3679, 0.5735] | 0.8595 [0.7077, 0.9518] | 0.9477 [0.9035, 0.9832] |
| 1.25 s, 6.0 m/s2 | 2.5291 [1.5142, 3.5728] | 209.66 [127.73, 294.19] | 0.4264 [0.3011, 0.5340] | 0.4218 [0.2972, 0.5289] | 0.4537 [0.3661, 0.5359] | 0.8595 [0.7199, 0.9478] | 0.9369 [0.8813, 0.9804] |
| 1.50 s, 6.0 m/s2 | 3.5196 [2.3013, 4.7251] | 291.78 [193.39, 388.16] | 0.5863 [0.4525, 0.6998] | 0.5870 [0.4514, 0.7015] | 0.4087 [0.3343, 0.4793] | 0.8503 [0.7274, 0.9339] | 0.9257 [0.8604, 0.9775] |
| 1.80 s, 6.0 m/s2 | 4.6955 [3.2727, 6.0030] | 389.25 [275.82, 492.89] | 0.7759 [0.6404, 0.8858] | 0.7831 [0.6420, 0.8955] | 0.3577 [0.2920, 0.4208] | 0.7673 [0.6541, 0.8546] | 0.9182 [0.8513, 0.9746] |

### The four scorings at 0.75 s and 6 m/s2

| Scoring | Population | den0 (pp) | den0 (decision-equivalents) | RR0(AM) | RR0(CK3) | RR0(E) |
|---|---|---|---|---|---|---|
| Estimate | All evaluated | 0.7093 [0.2584, 1.2286] | 58.80 [20.90, 103.23] | 0.5699 [0.4718, 0.6637] | 0.9360 [0.9078, 0.9586] | 0.9577 [0.9200, 0.9878] |
| Estimate | Ego moving | 0.6524 [0.2470, 1.0815] | 12.15 [4.34, 21.08] | 0.2567 [0.1674, 0.3375] | 0.0381 [-0.4605, 0.3806] | 0.9513 [0.9400, 1.0000] |
| Estimate | Phase-weighted | 0.0446 [0.0093, 0.1049] | 3.70 [0.75, 8.74] | -0.0565 [-0.6932, 0.2084] | 0.0377 [-2.1639, 0.7045] | 0.8856 [0.7776, 0.9959] |
| Censored pairs unsafe | All evaluated | 0.8386 [0.3697, 1.3806] | 69.52 [31.04, 113.19] | 0.4919 [0.3409, 0.6128] | 0.8288 [0.6232, 0.9458] | 0.9557 [0.9174, 0.9862] |
| Censored pairs unsafe | Ego moving | 1.0372 [0.4566, 1.6631] | 19.32 [8.44, 30.18] | 0.1782 [0.0837, 0.2851] | 0.0865 [-0.2549, 0.3240] | 0.9575 [0.9476, 1.0141] |
| Censored pairs unsafe | Phase-weighted | 0.1134 [0.0202, 0.2434] | 9.40 [1.76, 18.64] | -0.1037 [-0.4271, 0.0882] | 0.1365 [-0.7929, 0.5239] | 0.9841 [0.8514, 1.1028] |
| Estimate, signed caution | All evaluated | 0.6481 [0.2393, 1.0994] | 53.73 [19.39, 92.81] | 0.5324 [0.4366, 0.6253] | 0.8033 [0.7238, 0.8510] | 0.9301 [0.8834, 0.9649] |
| Estimate, signed caution | Ego moving | 0.7371 [0.2734, 1.2612] | 13.73 [4.78, 24.74] | 0.0696 [-0.0258, 0.1769] | -0.8949 [-1.4373, -0.4845] | 0.6754 [0.5348, 0.8091] |
| Estimate, signed caution | Phase-weighted | 0.1403 [0.0388, 0.2494] | 11.63 [3.14, 20.93] | -0.0364 [-0.2231, 0.0998] | -1.7625 [-3.2308, -1.1217] | 0.3945 [0.3046, 0.5697] |
| 3 s window only | All evaluated | 0.7016 [0.2526, 1.2193] | 58.16 [20.41, 102.52] | 0.5704 [0.4715, 0.6646] | 0.9357 [0.9075, 0.9582] | 0.9575 [0.9196, 0.9877] |
| 3 s window only | Ego moving | 0.6452 [0.2400, 1.0750] | 12.02 [4.23, 20.97] | 0.2575 [0.1675, 0.3392] | 0.0344 [-0.4710, 0.3774] | 0.9512 [0.9396, 1.0000] |
| 3 s window only | Phase-weighted | 0.0445 [0.0091, 0.1048] | 3.69 [0.74, 8.73] | -0.0513 [-0.6836, 0.2158] | 0.0418 [-2.1751, 0.7055] | 0.8853 [0.7770, 0.9958] |

Signed caution, relative to 3 s (all evaluated): against the 3 s commitment with the paper's caution, denE 0.1085 [0.0470, 0.1614] and den0 0.1081 [0.0466, 0.1641]; against the 3 s commitment with signed caution, denE 0.1240 [0.0526, 0.1908] and den0 0.1192 [0.0500, 0.1897].

### Pair counts over the 8290 evaluated decisions (140930 decision-row pairs)

| Setting | Unsafe on the 3 s window | Unsafe under the estimate | Late and safe on the window | of those unsafe under the estimate | Censored and safe on the window | of those safe under the estimate | Decisions without a row the estimate judges safe |
|---|---|---|---|---|---|---|---|
| 0.50 s, 6.0 m/s2 | 1417 | 1425 | 2897 | 8 | 94 | 90 | 0 |
| 0.75 s, 6.0 m/s2 | 3334 | 3362 | 5356 | 28 | 153 | 145 | 0 |
| 1.00 s, 6.0 m/s2 | 5631 | 5757 | 5301 | 126 | 230 | 200 | 0 |
| 1.25 s, 6.0 m/s2 | 8530 | 8745 | 7048 | 215 | 296 | 247 | 0 |
| 1.50 s, 6.0 m/s2 | 12714 | 13088 | 8583 | 374 | 372 | 291 | 0 |
| 1.80 s, 6.0 m/s2 | 15824 | 16475 | 9900 | 651 | 487 | 348 | 0 |
| 0.75 s, 4.0 m/s2 | 4373 | 4813 | 8905 | 440 | 773 | 714 | 0 |
| 0.75 s, 5.0 m/s2 | 3740 | 3901 | 6781 | 161 | 365 | 339 | 0 |
| 0.75 s, 7.6 m/s2 | 2802 | 2802 | 2431 | 0 | 37 | 37 | 0 |

Further counts in the results file (not on the brief's list): late pairs, censored pairs, pairs unsafe under the 3 s commitment (24902), decisions with a censored pair, decisions without a safe row when censored pairs count as unsafe.

## Comparison with the first program

Details: `RECOUNT4_COMPARE_v01.md` (counts per scoring) and `RECOUNT4_COMPARE_v01.json` (every comparison with both values). First program's file: written 2026-11-18 17:19:07, sha256 `86b670aef106ea626b5a7e0e79050511f4f3f99b05f802b349a51a42c044b8f8`.

| Scoring family | Compared | Differ | A: compared / differ | B: compared / differ | C: compared / differ | Largest absolute difference |
|---|---|---|---|---|---|---|
| est (9 settings) | 5811 | 0 | 3270 / 0 | 2256 / 0 | 285 / 0 | 2.8e-14 |
| cens (6 settings) | 1728 | 0 | 1110 / 0 | 498 / 0 | 120 / 0 | 2.8e-14 |
| est_signed (0.75 s, 6 m/s2) | 757 | 0 | 420 / 0 | 298 / 0 | 39 / 0 | 3.6e-15 |
| asscored (0.75 s, 6 m/s2) | 241 | 0 | 210 / 0 | 16 / 0 | 15 / 0 | 1.3e-15 |
| pair counts (9 settings) | 81 | 0 | 72 / 0 | 9 / 0 | 0 / 0 | 0.0e+00 |
| **Total** | **8618** | **0** | 5082 / 0 | 3077 / 0 | 459 / 0 | 2.8e-14 |

No difference above 1e-9 was found, so there is no cause to report.

What the counts do and do not show:

- Class A (5082) are numbers on the brief's list, taken from the results file as it stood before the first program's file was opened. Class B (3077) are entries not on the list that were in that file or follow from it by arithmetic: resamples left out of a ratio (count and share), the count of resamples with a sum <= 0, the flag "point outside its interval", the basic interval 2 x point - percentile, the perfect oracle's point, F0's zero-margin caution, the flag signed caution, the pairs unsafe under the 3 s commitment. The arithmetic ones are not separate tests of the scoring. Class C (459) were recomputed after the first program's file and script were read: minimum, maximum and number of undefined levels of the perfect oracle's frontier (from the stored points), and the first program's branch number (its rule and its two thresholds, 2.5% of resamples left out and 10 decision-equivalents, applied to the second program's numbers; 204 entries).
- Of the 8618 comparisons, 278 are "undefined in both programs" (ratios in phase 0, where numerator and denominator are 0), 557 are yes/no flags, 1685 are numbers that are exactly 0 in both programs, and 7497 numbers are bit-identical.
- The two programs share the draw of record and the stored inputs. They do not share the clearances judged until the stop ends (first program: `analysis\out\ext`; second: `recount2\out`), the "as scored" clearance (first: the pack cache; second: recount2's own 61-frame clearance) or any scoring code.
- Negative control of the comparison script (`r4_compare_v01.py negctl`): with the second program's blocks `est_t0p75_a6p0` and `cens_t0p75_a6p0` swapped and the pair counts of two settings swapped, it reports 1170 differences (est_t0p75_a6p0: 579 of 973; cens_t0p75_a6p0: 579 of 973; pair_counts: 12 of 81).

### Numbers on the brief's list without a counterpart in the first program's file (5700 of 10782)

The first program bootstrapped `est` at the six settings with 6 m/s2, `cens` at 0.75 s and `est_signed`; it gave points only for `est` at 4, 5 and 7.6 m/s2, for `cens` at the five other settings and for `asscored`. It scored N, NA, CK3, AM and Q at 0.75 s and 6 m/s2 (`est`, `cens`, `asscored`), N, NA, CK3 and AM for the other `est` settings and for `est_signed`, and N and CK3 for `cens` at the other settings. So without counterpart are:

- `est` at 0.75 s with 4, 5 and 7.6 m/s2: every interval and share, and source Q (450 numbers each);
- `cens` at 0.5, 1.0, 1.25, 1.5 and 1.8 s: every interval and share, and sources NA, AM and Q (510 each);
- `asscored`: every interval and share (420);
- `est` at 0.5, 1.0, 1.25, 1.5 and 1.8 s: source Q, and the intervals of D as a sum and in pp (186 each);
- `est_signed`: source Q, the intervals of the ratios to 3 s, and the intervals of D as a sum and in pp (210);
- `est` and `cens` at 0.75 s and 6 m/s2: only the intervals of D as a sum and in pp (120 each; the first program gives the interval of D in decision-equivalents only).

| Scoring | On the brief's list | With counterpart | Without |
|---|---|---|---|
| `est_t0p50_a6p0` | 630 | 444 | 186 |
| `est_t0p75_a6p0` | 630 | 510 | 120 |
| `est_t1p00_a6p0` | 630 | 444 | 186 |
| `est_t1p25_a6p0` | 630 | 444 | 186 |
| `est_t1p50_a6p0` | 630 | 444 | 186 |
| `est_t1p80_a6p0` | 630 | 444 | 186 |
| `est_t0p75_a4p0` | 630 | 180 | 450 |
| `est_t0p75_a5p0` | 630 | 180 | 450 |
| `est_t0p75_a7p6` | 630 | 180 | 450 |
| `cens_t0p50_a6p0` | 630 | 120 | 510 |
| `cens_t0p75_a6p0` | 630 | 510 | 120 |
| `cens_t1p00_a6p0` | 630 | 120 | 510 |
| `cens_t1p25_a6p0` | 630 | 120 | 510 |
| `cens_t1p50_a6p0` | 630 | 120 | 510 |
| `cens_t1p80_a6p0` | 630 | 120 | 510 |
| `est_signed_t0p75_a6p0` | 630 | 420 | 210 |
| `asscored_t0p75_a6p0` | 630 | 210 | 420 |
| pair counts | 72 | 72 | 0 |
| **Total** | **10782** | **5082** | **5700** |

### Entries of the first program's file that were not compared

- `scorings.ii_t0p75_a6p0`: 242 numeric entries; outside the brief (ii_* and est_gap2_* are to be ignored).
- `scorings.est_gap2_t0p75_a6p0`: 242 numeric entries; outside the brief (ii_* and est_gap2_* are to be ignored).
- `scorings.<name>.bootstrap` (17 entries): a switch of the first program (whether it bootstrapped the scoring), not a result.
- `seconds`: run time. `code`, `status`, `written`, `common_sha256`: text.
- Every other numeric entry of the file was compared.

## Ambiguities in the brief and how they were resolved

1. **"Relative to 3 s".** The definition names "the 3 s commitment" (unsafe when `clear` <= 0), while the list of scorings also has a "3 s window only" scoring (`clear61`). The 3 s commitment was used (`rel.3s_commitment`). The first program reads it the same way and every ratio agrees. As an addition, the ratio to the 3 s-window scoring at the same setting is stored (`rel.3s_window_same_setting`; at 0.75 s and 6 m/s2, all: denE 1.0113 [1.0000, 1.0515], den0 1.0110 [1.0000, 1.0510]). It has no counterpart in the first program's file.
2. **Signed caution, relative to 3 s.** The denominator can be the 3 s commitment with the paper's caution or with signed caution. Both are stored; the first was taken as the reading of record before the comparison (`rel.3s_commitment`: denE 0.1085 [0.0470, 0.1614]). The first program gives this ratio as a point only and uses the paper's caution in the denominator; the points agree. The ratio with signed caution in the denominator (`rel.3s_commitment_signed`: denE 0.1240 [0.0526, 0.1908]) has no counterpart.
3. **`cens`.** Read as: a pair is unsafe when `clearX` <= 0 or `cens` is true. recount2's optional scoring had instead flagged only censored pairs that are safe on the 3 s window. The two readings give the same flags for every pair in all nine settings (0 pairs differ), because no censored pair is unsafe on the window and safe under the estimate.
4. **Shares "den <= 0".** Taken over all 20,000 resamples. No resample has an undefined den0 or denE in any scoring or population (0), so counting an undefined sum as "<= 0" (as the first program does) gives the same share.
5. **Point of a ratio whose full-sample denominator is not positive.** The brief does not say. The results file stores the plain quotient with a flag `point_denominator_positive`; the comparison applies the first program's convention (undefined). It occurs in 213 entries of the results file, all in phase 0: in 203 numerator and denominator are both 0 (undefined either way); in the other 10 a positive sum stands over a denominator of 0, and all of these are the added ratio to the 3 s-window scoring of point 1 (not on the brief's list, no counterpart). No quotient with a non-positive denominator is stored as a number (0).
6. **Intervals.** Sums, percentage points and decision-equivalents: over all resamples (all are finite). Ratios: over the resamples with a positive denominator; for "relative to 3 s" the denominator is the 3 s commitment's denE or den0 of the same resample. The number of resamples left out is stored with every ratio.
7. **"D (sum, percentage points, decision-equivalents with interval)".** Intervals are given for all three forms. The first program gives one for the decision-equivalents only.
8. **Phase-weighted aggregate.** n = n_0 + n_1 + n_2 of the resample (no evaluated decision has phase 3, so this is every evaluated decision); the sums are aggregated with weights n_p / n and every ratio, share and decision-equivalent is formed from the aggregated sums.
9. **Perfect oracle of `cens` and `est_signed`.** O selects by the scoring's own safe flag (for `cens`: `clearX` > 0 and not censored); its caution follows the scoring's caution (signed for `est_signed`).
10. **Pair counts, "unsafe on the 3 s window".** Read as `clear61` <= 0 (the reaction-and-stop clearance on the 61 frames), not the 3 s commitment. The first program counts on the pack cache; the counts agree at all nine settings. The pairs unsafe under the 3 s commitment are stored as well.
11. **`asscored` at the other settings.** The brief asks for 0.75 s and 6 m/s2 only. It was computed at all nine settings because it is the denominator of the added ratio of point 1; the eight others are not on the brief's list and have no counterpart.
12. **Source names.** AM is `cA1`; the first program's file calls it `A1`. Its population `strat` is the phase-weighted aggregate.

## Notes on the results

- Phase 0 under the estimate: den0 = 0 in the full sample and in every resample at 7 of the 9 settings (0.50 s, 6.0 m/s2; 0.75 s, 6.0 m/s2; 1.00 s, 6.0 m/s2; 1.25 s, 6.0 m/s2; 0.75 s, 4.0 m/s2; 0.75 s, 5.0 m/s2; 0.75 s, 7.6 m/s2). Ratios do not exist there.
- The estimate's den0 (all evaluated) is <= 0 in some resamples at 2 of the 9 settings: 0.50 s, 6.0 m/s2: 2559 of 20,000 (12.80%); 0.75 s, 7.6 m/s2: 10 of 20,000 (0.05%). At 0.5 s the interval of den0 starts at 0. At the other settings no resample has den0 <= 0.
- The censored pairs come from few runs: 3 to 5 of the 35 runs hold a censored pair (by setting: 0.50 s, 6.0 m/s2: 3; 0.75 s, 6.0 m/s2: 5; 1.00 s, 6.0 m/s2: 5; 1.25 s, 6.0 m/s2: 5; 1.50 s, 6.0 m/s2: 5; 1.80 s, 6.0 m/s2: 5; 0.75 s, 4.0 m/s2: 5; 0.75 s, 5.0 m/s2: 5; 0.75 s, 7.6 m/s2: 3). The `cens` intervals therefore rest on whether those runs are drawn.
- Between the 3 s window and the estimate no pair changes from unsafe to safe (the estimate's clearance is a minimum over more frames); the first row judged safe moves in 0 to 116 decisions (by setting: 0.50 s, 6.0 m/s2: 0; 0.75 s, 6.0 m/s2: 1; 1.00 s, 6.0 m/s2: 9; 1.25 s, 6.0 m/s2: 19; 1.50 s, 6.0 m/s2: 64; 1.80 s, 6.0 m/s2: 116; 0.75 s, 4.0 m/s2: 40; 0.75 s, 5.0 m/s2: 15; 0.75 s, 7.6 m/s2: 0).

## Files (all in `revision_v11\recount4`)

- `RECOUNT4_RESULTS_v01.json`: the results, one entry per number (sha256 `b5d428524e066e270d52cc31057c23d5c5accf4b1d88659391a5cfcb2f66f04c`). `RECOUNT4_RESULTS_v01.sha256.txt`: hash and time written by the program.
- `r4_items_v01.py`: the program (sha256 `bef455ca89b045fe167ae04d85df7655da088e823118a630fea9e87400f8f786`, unchanged since the run). `r4_items_v01_log.txt`, `r4_items_v01_stdout.txt`: its log. `boot\<scoring>.npz`: the per-resample sums of the 27 scorings (226 MB in all; read by the self-check and by class C of the comparison; a rerun of the program reproduces them and the numbers of the results file, but not that file's hash, because it holds the run time).
- `r4_naive_v01.py`, `r4_naive_v01_out.json`, `r4_naive_v01_stdout.txt`: the self-check by a second route.
- `r4_compare_v01.py`, `RECOUNT4_COMPARE_v01.md`, `RECOUNT4_COMPARE_v01.json`: the comparison; `r4_compare_negctl_v01_out.json`: its negative control.
- `r4_diag_v01.py` (`r4_diag_v01_out.json`, `r4_diag_v01_stdout.txt`), `r4_extra_v01.py` (`r4_extra_v01_out.json`): diagnostics and supplementary checks written after the comparison.
- `r4_record_before_compare_v01.md`: the report as it stood before the first program's file was opened (sha256 `76f40fab80cfe28d8ec606d0955954e2d2e9edce577eda5f9d0a6c4ff43edd45`).
- `r4_probe_v01.py`, `r4_show_v01.py`, `r4_peek_v01.py`, `r4_peek2_v01.py`, `r4_peek3_v01.py`, `r4_report_v01.py`: helpers (input probe, printout of own results, structure of the first program's file, this report).
- `RECOUNT4_RESULTS_v01_quick.json`, `boot_quick\`: a test run on the first 400 rows of the draw of record; not a result.
