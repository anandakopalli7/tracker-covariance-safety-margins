# Recount3: independent second program for Tables S12b, S17 (subsampling), S24b and S25 with the benign-run check

Written 18 Nov 2026. Brief: `RECOUNT3_BRIEF_v01.md` (this folder), with the inputs, scoring definitions and bootstrap of record of `revision_v11\recount\RECOUNT_BRIEF_v01.md`.

## Result in short

- All four analyses were recomputed by a second program. Compared with the first program: **1625 numbers, 0 differ by more than 1e-9** (largest absolute difference 2.8e-14).
- Numbers the brief asks for: item 1: 45 compared, 0 differ; item 2: 48, 0; item 3: 60, 0; item 4: 189, 0.
- Every numeric entry of the first program's four files was compared (item 1: 127, item 2: 168, item 3: 399, item 4: 931), except the block `S20.tuning_runs_of_record` of `REV_F2_BRAKING_PRIOR_v01.json`, which the first program copied from an older file and which is outside this brief.
- `cCK3` identity check: the `cCK3` of `analysis\out\ck\<run>.npz` equals the stored `cCK3` of `A4\fit\extract\<run>.npz` bit for bit in 35 of 35 evaluation runs (158219 entries, of which 140930 on evaluated decisions; 0 entries differ).
- One caveat that is not a difference between the programs (both treat it the same way): in Table S24b, 203 decision-row pairs have a recording that ends before the plan's stop does; 126 of them are counted safe at 2 m on the frames that exist. See "Ambiguities", point 7.

## Independence and order of work

- Read before writing the program: the two briefs; `revision_v11\recount\rc_lib_v01.py` and `rc_items_v01.py`; `revision_v11\recount2\recount2_ext_v01.py` and `recount2_score_v01.py`; a keyword search of `revision_v11\recount\RECOUNT_REPORT_v01.md` (the earlier second program's report: its conventions and the phase-weighted rows of its own tables for R11 and R17, which are other analyses). Its timing log `rc_items_v01_log.txt`. Arrays opened: the stored runs, the extraction, the pack cache, `recount2\out`, `analysis\out\ck`.
- Not opened at any time: `P\11_ojits\A6R\code`, `<excluded folder 1>`, `<excluded folder 2>`, `<excluded folder 3>`. No file of `revision_v11\draft` was opened (a listing of recently changed files, made after the comparison to confirm that nothing was written outside this folder, showed file names there). No network.
- `RECOUNT3_RESULTS_v01.json` was written at 18 Nov 2026 18:20:49 (sha256 `e71c30f4326b7ba2c79dbabced3f205421d5fb0468780805169b746c798c500e`) and has not been changed since. Only after that were the first program's four result files opened, and then its two scripts `rev_g_partial_oracle_draws_v01.py` and `rev_f2_braking_prior_score_v01.py` (and the header of `rev_common_v01.py`), to learn the definitions of entries that the brief does not list.
- The supplementary script `r3_extra_v01.py` was written after that. It recomputes entries of the first program's files that the brief does not list (class C in the comparison) with the unchanged library. Nothing in the program was tuned after the comparison; no difference was found.

## Inputs and checks on them

- 35 evaluation runs, 9307 stored decisions, 8290 evaluated; evaluated decisions by phase: 678 before onset, 755 lead braking, 6857 lead stopped, 0 unknown.
- NaN among evaluated decisions: 3 s clearance 0, pack cache (`t0p75_a6p0`) 0, clearance judged until the stop ends 0, `cCK1`..`cCK7` 0.
- `k` and the evaluated flags of `recount2\out` equal the stored ones in every run; `k` of the `ck` folder equals the stored `k` in every run (the program stops otherwise).
- Clearance judged until the stop ends: key `clearX_t0p75_a6p0` of `recount2\out\<run>.npz`.

## Method

- `r3_lib_v01.py` imports the second-program library `rc_lib_v01.py` for the loader of the 35 runs, the selection on the grid of 202 scales, the batched step frontier, the level grid and the percentile helper. The evaluation for an arbitrary list of arms (`evaluate_g`) and the per-decision statistics are written here. Each run is reduced to per-scale counts (wrong-go count, caution sum, caution count per population), so that a resample is a weighted sum of 35 vectors.
- Bootstrap of record: `numpy.random.default_rng(20261113).integers(0, 35, size=(20000, 35))`; everything, levels included, is rebuilt in every resample; 95% percentile intervals over the resamples with a positive denominator.
- Self-check by a second route (`r3_naive_v01.py`): decisions concatenated (no per-run statistics), selection recomputed from the critical scales, levels by `numpy.linspace`, the frontier by a loop over levels. It shares only the data loader. 305 numbers (every point of items 3 and 4, the full-sample values of item 2, three draws of item 1, and two resamples or subsamples of each bootstrap) agree with the program to 1.4e-14.
- `evaluate_g` gives the same values as `rc_lib_v01.evaluate` on the statistics of item 3 (equal arrays: True).

## Item 1. Table S12b: partial oracles over 50 draws

For draw i = 0..49, `u = default_rng(20261200 + i).random(9307)`, one value per stored decision (runs in sorted-name order, stored order within a run). Share p: the oracle's critical scales where u < p, the class average's elsewhere. The partial arm gets F0's zero-margin point prepended. 3 s commitment, step frontier, points. Cells: mean [minimum, maximum] of RR over the 50 draws.

| Population | n | p = 0.25 | p = 0.50 | p = 0.75 |
|---|---|---|---|---|
| All | 8290 | 0.2827 [0.2555, 0.3142] | 0.5442 [0.4994, 0.5822] | 0.7842 [0.7524, 0.8056] |
| Ego moving | 1863 | -0.0751 [-0.1425, -0.0056] | 0.0903 [-0.0031, 0.1855] | 0.4625 [0.3398, 0.5489] |
| Lead braking (phase 1) | 755 | -0.6448 [-0.7635, -0.5208] | -0.5405 [-0.7186, -0.3972] | 0.0527 [-0.1606, 0.1992] |
| Lead stopped (phase 2) | 6857 | 0.2830 [0.2291, 0.3315] | 0.5521 [0.4984, 0.6014] | 0.7891 [0.7647, 0.8209] |
| Phase-weighted | 8290 | -0.3509 [-0.4452, -0.2558] | -0.1960 [-0.3289, -0.0887] | 0.2841 [0.1443, 0.3836] |

Evaluated decisions on the oracle, mean over draws: 2073.2 (p = 0.25), 4146.9 (0.50), 6216.6 (0.75) of 8290. No frontier level is undefined in any population.
Supplementary (class C): phase 0 and the value of the draw of record (`default_rng(20261118)`) were also recomputed and agree with the first program.

## Item 2. Table S17: subsampling without replacement

One stream `default_rng(20261124)`; for m = 15, 20, 25 in that order, 5,000 subsamples `rng.permutation(35)[:m]` each. Root = sqrt(m) (theta* - theta); (ql, qh) = 2.5 and 97.5 percentiles of the roots; interval [theta - qh / (f sqrt(35)), theta - ql / (f sqrt(35))], f = sqrt(1 - m/35). 3 s commitment, all evaluated decisions.

| Statistic | Full sample | m = 15 | m = 20 | m = 25 |
|---|---|---|---|---|
| R (pp) | 5.5568 | [4.5177, 6.6426] | [4.5093, 6.6426] | [4.4996, 6.6541] |
| RR(N) | 0.0012 | [0.0011, 0.0033] | [0.0013, 0.0038] | [0.0014, 0.0047] |
| RR(NA) | 0.0167 | [0.0072, 0.0266] | [0.0079, 0.0269] | [0.0084, 0.0274] |
| RR(AM) | 0.3758 | [0.3246, 0.4410] | [0.3231, 0.4379] | [0.3245, 0.4325] |
| RR(CK3) | 0.8315 | [0.7581, 0.9150] | [0.7610, 0.9130] | [0.7647, 0.9148] |
| RR(Q) | -0.0018 | [-0.0052, 0.0027] | [-0.0051, 0.0027] | [-0.0051, 0.0030] |
| RR0(CK3) | 0.7705 | [0.7031, 0.8498] | [0.7052, 0.8463] | [0.7036, 0.8445] |
| RR(NA) - RR(N) | 0.0154 | [0.0050, 0.0243] | [0.0055, 0.0245] | [0.0056, 0.0245] |

In all 15000 subsamples denE and den0 are positive and every root is finite (subsamples with denE <= 0: 0, 0, 0; with den0 <= 0: 0, 0, 0; with an undefined frontier level: 0, 0, 0), so the reading of "finite roots" does not matter.

## Item 3. Table S24b: 2 m standstill gap, plans judged until their stop ends (tau 0.75 s, 6 m/s2)

Wrong go: the selected row's clearance judged until the stop ends is <= 2 m. Caution axis: a row is truly safe when its 3 s clearance is > 2 m. Perfect oracle O: first row in cost order whose clearance judged until the stop ends is > 2 m, the fallback row if none. Intervals: draw of record.

| Population | n | den0 (pp) | den0 (decision-equivalents) |
|---|---|---|---|
| All | 8290 | 1.1418 [0.4828, 1.8489] | 94.65 [39.09, 156.18] |
| Ego moving | 1863 | 1.0973 [0.4373, 1.8601] | 20.44 [7.83, 35.31] |
| Phase-weighted | 8290 | 0.1432 [0.0366, 0.2558] | 11.87 [2.99, 21.48] |

| Population | RR0(E) | RR0(N) | RR0(NA) | RR0(CK3) | RR0(AM) |
|---|---|---|---|---|---|
| All | -0.0697 [-2.1384, 0.8729] | -0.0008 [-0.0111, 0.0048] | 0.0210 [-0.0036, 0.0590] | 0.5764 [-0.2596, 0.8559] | 0.8005 [0.7377, 0.8699] |
| Ego moving | -1.5799 [-7.1445, 0.1958] | -0.0219 [-0.0548, 0.0051] | -0.0092 [-0.0447, 0.0382] | -0.9560 [-2.7685, -0.2158] | 0.4067 [0.2551, 0.5015] |
| Phase-weighted | -0.2871 [-3.3254, 0.7140] | -0.0193 [-0.0656, 0.0131] | 0.0859 [-0.1677, 0.2304] | 0.5474 [-0.2305, 0.9268] | 0.2246 [-0.6419, 0.5735] |

Counts over the 8290 evaluated decisions (140930 decision-row pairs):

- decisions without any row whose clearance judged until the stop ends is > 2 m: **631**;
- pairs unsafe at 2 m on the 3 s window's reaction-and-stop clearance of record (pack cache): **19900**;
- pairs unsafe at 2 m when judged until the stop ends: **19934**.

den0 is positive in every resample for the three populations. In phase 0 den0 = 0 in the full sample and in every resample (no ratio), in both programs. The results file also holds phases 0-2 separately, RR0(Q) and denE; all were compared (class B).

## Item 4. Table S25: braking prediction at a0 = 1..7 m/s2, and the benign-run check

Arm = `cCK<a0>` of the `ck` folder; 3 s commitment, step frontier; intervals: draw of record. RR:

| a0 | All | Ego moving | Phase 0 | Phase 1 | Phase 2 | Phase-weighted |
|---|---|---|---|---|---|---|
| 1 | 0.2763 [0.2140, 0.3542] | 0.1290 [0.0944, 0.1753] | 0.0289 [-0.0469, 0.0626] | 0.0291 [0.0187, 0.0436] | 0.7947 [0.7082, 0.8987] | 0.2726 [0.2202, 0.3479] |
| 2 | 0.5649 [0.4741, 0.6667] | 0.2825 [0.2075, 0.3610] | -0.2262 [-1.5912, 0.1037] | 0.2796 [0.2367, 0.3380] | 0.9526 [0.8681, 1.0623] | 0.4853 [0.4328, 0.5613] |
| 3 | 0.8315 [0.7528, 0.9033] | 0.4718 [0.3527, 0.5701] | -0.5357 [-3.7605, 0.1748] | 0.6063 [0.4678, 0.7107] | 0.9934 [0.9136, 1.1085] | 0.7105 [0.6137, 0.7927] |
| 4 | 0.9299 [0.8693, 0.9953] | 0.3856 [0.2288, 0.5006] | -1.3776 [-7.2035, -0.3337] | 0.5305 [0.3131, 0.6971] | 1.0102 [0.9324, 1.1328] | 0.6516 [0.4890, 0.7827] |
| 5 | 0.9291 [0.8684, 1.0006] | 0.1821 [-0.0678, 0.3656] | -2.2228 [-10.6107, -0.8196] | 0.3038 [-0.0441, 0.5783] | 1.0195 [0.9406, 1.1452] | 0.4897 [0.2205, 0.6994] |
| 6 | 0.9171 [0.8402, 0.9925] | 0.0215 [-0.3239, 0.2523] | -2.8588 [-13.1186, -1.1857] | 0.1004 [-0.3428, 0.4681] | 1.0229 [0.9448, 1.1481] | 0.3449 [0.0037, 0.6226] |
| 7 | 0.8983 [0.8127, 0.9805] | -0.1271 [-0.5373, 0.1478] | -3.3793 [-15.1448, -1.4621] | -0.0703 [-0.6096, 0.3450] | 1.0250 [0.9463, 1.1508] | 0.2234 [-0.1899, 0.5366] |

D in decision-equivalents:

| a0 | All | Ego moving | Phase 0 | Phase 1 | Phase 2 | Phase-weighted |
|---|---|---|---|---|---|---|
| 1 | 127.29 | 24.42 | 0.08 | 3.42 | 44.72 | 48.22 |
| 2 | 260.21 | 53.50 | -0.66 | 32.90 | 53.60 | 85.84 |
| 3 | 383.02 | 89.34 | -1.57 | 71.35 | 55.90 | 125.68 |
| 4 | 428.36 | 73.02 | -4.03 | 62.44 | 56.84 | 115.25 |
| 5 | 428.00 | 34.49 | -6.50 | 35.76 | 57.36 | 86.62 |
| 6 | 422.47 | 4.08 | -8.36 | 11.82 | 57.56 | 61.01 |
| 7 | 413.83 | -24.07 | -9.89 | -8.27 | 57.68 | 39.52 |

n: all 8290, moving 1863, phase0 678, phase1 755, phase2 6857, phase_weighted 8290. Phase 0: one resample of 20,000 has denE <= 0 and is left out (the same in the first program).

Zero-margin points (g = 0, all evaluated decisions):

| Arm | Caution (%) | Wrong go (%) | Wrong-go decisions |
|---|---|---|---|
| F0 | 1.0958 | 8.9988 | 746 |
| CK1 | 1.1279 | 8.1665 | 677 |
| CK2 | 1.4144 | 6.6707 | 553 |
| CK3 | 1.7182 | 4.8372 | 401 |
| CK4 | 2.2677 | 2.7624 | 229 |
| CK5 | 2.8574 | 2.0024 | 166 |
| CK6 | 3.3062 | 1.5923 | 132 |
| CK7 | 3.6661 | 1.3872 | 115 |

Benign-driving tuning runs (20 runs with `meta.family == 'benign'`, all of the tuning set; `cCK3` from the `ck` folder, `cF0` from `gateR_rt_v01`):

- evaluated decisions: **5420** (of 6000 stored);
- evaluated decisions whose selected row differs between the braking prediction and the class average: **0** at g = 0, **3** at g = 1;
- wrong-go decisions at zero margin: **0** under the braking prediction, **0** under the class average.

## Comparison with the first program

Details: `RECOUNT3_COMPARE_v01.md` (counts, largest differences) and `RECOUNT3_COMPARE_v01.json` (every comparison).

| Item | Asked for by the brief (A): compared / differ | All classes: compared / differ | Largest absolute difference |
|---|---|---|---|
| 1. Table S12b | 45 / 0 | 127 / 0 | 1.1e-16 |
| 2. Table S17 subsampling | 48 / 0 | 168 / 0 | 8.9e-16 |
| 3. Table S24b | 60 / 0 | 399 / 0 | 2.8e-14 |
| 4. Table S25 and benign check | 189 / 0 | 931 / 0 | 1.4e-14 |

No difference above 1e-9 was found, so there is no cause to report. The largest differences are of the size of floating-point rounding.

What the counts do and do not show:

- Class A (342 numbers) are the brief's numbers, taken from the results file as it stood before the first program's files were opened.
- Class B (772) are further entries of that results file (phases 0-2 of Table S24b, RR0(Q), denE, n, resamples left out) and entries of the first program's files that follow by arithmetic from it (basic intervals, intervals without the finite-population factor, percentiles of the draws, sums instead of pp). The arithmetic ones are not separate tests of the scoring.
- Class C (511) were recomputed after the files were opened: phase 0 and the draw of record of Table S12b (36), RR0 and den0 of Table S25 (342), and the first program's full scoring of the benign runs (133), where the room is 0 and most entries are 0 or undefined.
- Of the 1625 comparisons, 70 are "undefined in both programs" (no ratio: phase 0 of Table S24b, benign runs) and 128 are yes/no flags.
- In the first program's file `REV_F2_BRAKING_PRIOR_v01.json` the sweep over a0 is keyed `S20` and the benign-run check `S18`; in `rev_g_partial_oracle_draws_v01.py` the partial-oracle draws are called check S19. These are the first program's own labels, not the table numbers of the brief (S25, S12b); the blocks were matched by content.

## Ambiguities in the brief and how they were resolved

1. **Phase-weighted aggregate, the n.** Taken as n = n0 + n1 + n2, rebuilt in every resample. No evaluated decision has phase 3 here, so this n equals the number of evaluated decisions (8,290) and the two readings coincide. Decision-equivalents of the aggregate = aggregated D / 201 / 100 x n.
2. **Item 2, "finite roots".** Could mean every finite quotient or only quotients with a positive denominator. Both were computed; they are identical because all 15,000 subsamples have positive denE and den0.
3. **Item 3, "with the 95% interval of record" for den0.** Given for both units (pp and decision-equivalents). In a resample the decision-equivalents use the resample's own n.
4. **Item 3, "the 3 s window's reaction-and-stop clearance of record (the pack cache)".** Taken as key `t0p75_a6p0` of the pack cache. The second program's own 61-frame clearance (`clear61_t0p75_a6p0` of recount2) gives the same count (19900).
5. **Item 4, "at g = 1".** The grid holds the value 1.0 exactly (True); selecting at exactly 1.0 and at the grid value gives the same count (3 and 3).
6. **Item 4, "zero-margin point for each a0".** Taken as the arm's own point at g = 0 (not the prepended F0 point). "Wrong-go decisions at zero margin" in the benign runs: the selected row's 3 s clearance is <= 0.
7. **Item 3, plans whose recording ends before the stop.** The brief does not say how to judge them. The clearances of recount2 were used as stored: the minimum over the frames that exist. Of 140930 pairs, 5798 stop after the 3 s window and 203 of these are cut short by the end of the recording (in 29 decisions); 126 of the cut-short pairs are counted safe at 2 m. The first program's numbers agree with this reading. As a bound (points only, not compared, computed after the comparison): if those 126 pairs are counted unsafe instead, den0 moves from 1.1418 to 1.2105 pp (all), 1.0973 to 1.3670 pp (ego moving) and 0.1432 to 0.2040 pp (phase-weighted; 11.87 to 16.92 decision-equivalents), and RR0(CK3) from 0.5764 to 0.5616 (all) and 0.5474 to 0.4659 (phase-weighted). Table S24b therefore depends visibly on this choice.
8. **Bootstrap of the benign runs (supplementary only).** The first program resamples the 20 benign runs with seed 20261125 through a function of the A6R code, which was not opened. The supplementary script used `default_rng(20261125).integers(0, 20, size=(20000, 20))`. Every resample gives a room of 0 (no wrong go at any scale), so these intervals are [0, 0] or undefined whatever the draw; their agreement does not test the draw.

## Notes on the results file

- `item3_S24b.counts.pairs_late` in `RECOUNT3_RESULTS_v01.json` is an unused placeholder (always 0), not a count. The file was left as written before the comparison; the count of late pairs (5798) is in `r3_extra_v01_out.json`.
- Between the 3 s window and the judgement until the stop ends, 34 pairs change from safe to unsafe at 2 m and 0 the other way; the first safe row changes in 4 decisions.

## Files (all in `revision_v11\recount3`)

- `RECOUNT3_RESULTS_v01.json`: the results, one entry per number (item 1 also holds the 50 draw values per cell).
- `r3_lib_v01.py`, `r3_items_v01.py`: the program. `r3_items_v01_log.txt`, `r3_items_v01_stdout.txt`: its log.
- `r3_naive_v01.py`, `r3_naive_v01_out.json`: the self-check by a second route.
- `r3_extra_v01.py`, `r3_extra_v01_out.json`: supplementary numbers (class C) and the diagnostics of item 3, written after the comparison files were opened.
- `r3_compare_v01.py`, `RECOUNT3_COMPARE_v01.md`, `RECOUNT3_COMPARE_v01.json`: the comparison.
- `r3_probe_v01.py`, `r3_show_v01.py`, `r3_peek_v01.py` (`r3_peek_F2.txt`), `r3_report_v01.py`: helpers (input probe, printout of own results, structure of the first program's files, this report).
- `RECOUNT3_RESULTS_v01_quick.json`: a test run on the first 400 rows of the draw of record; not a result.
