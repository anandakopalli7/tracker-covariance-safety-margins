# Recount4: comparison with the first program

Written 2026-11-18 19:28:44 by `r4_compare_v01.py`.

- First program: `revision_v11\analysis\out\REV_E2_EXTENDED_TRUTH_v01.json` (written 2026-11-18 17:19:07, sha256 `86b670aef106ea626b5a7e0e79050511f4f3f99b05f802b349a51a42c044b8f8`).
- Second program: `RECOUNT4_RESULTS_v01.json` (sha256 `b5d428524e066e270d52cc31057c23d5c5accf4b1d88659391a5cfcb2f66f04c`, unchanged since it was recorded before the first file was opened).
- Tolerance: absolute difference 1e-9. An entry that is undefined (no ratio) in both programs counts as compared and not differing.

## Result

**8618 numbers compared, 0 differ by more than 1e-9.** Largest absolute difference: 2.84e-14. Of the 8618 comparisons, 278 are "undefined in both programs" and 557 are yes/no flags.

Classes: A = on the brief's list, from the results file as it stood before the first program's file was opened; B = not on the list, in that results file or following from it by arithmetic (resamples left out, the flag "point outside its interval", the basic interval, the point of the perfect oracle, the flag signed caution, the 3 s commitment's unsafe pairs); C = recomputed after the first program's file and script were opened (minimum, maximum and undefined levels of the perfect oracle's frontier; the first program's branch number, by its rule applied to the second program's numbers).

| Scoring family | Compared | Differ | A: compared / differ | B: compared / differ | C: compared / differ | Largest absolute difference |
|---|---|---|---|---|---|---|
| est (9 settings) | 5811 | 0 | 3270 / 0 | 2256 / 0 | 285 / 0 | 2.84e-14 |
| cens (6 settings) | 1728 | 0 | 1110 / 0 | 498 / 0 | 120 / 0 | 2.84e-14 |
| est_signed (0.75 s, 6 m/s2) | 757 | 0 | 420 / 0 | 298 / 0 | 39 / 0 | 3.55e-15 |
| asscored (0.75 s, 6 m/s2) | 241 | 0 | 210 / 0 | 16 / 0 | 15 / 0 | 1.33e-15 |
| pair counts (9 settings) | 81 | 0 | 72 / 0 | 9 / 0 | 0 / 0 | 0 |
| **Total** | **8618** | **0** | 5082 / 0 | 3077 / 0 | 459 / 0 | 2.84e-14 |

## Per scoring

| Scoring | Compared | Differ | A: compared / differ | B | C | Undefined in both | Largest absolute difference |
|---|---|---|---|---|---|---|---|
| `est_t0p50_a6p0` | 841 | 0 | 444 / 0 | 358 / 0 | 39 / 0 | 45 | 1.33e-15 |
| `est_t0p75_a6p0` | 973 | 0 | 510 / 0 | 418 / 0 | 45 / 0 | 55 | 1.33e-15 |
| `est_t1p00_a6p0` | 841 | 0 | 444 / 0 | 358 / 0 | 39 / 0 | 45 | 1.33e-15 |
| `est_t1p25_a6p0` | 841 | 0 | 444 / 0 | 358 / 0 | 39 / 0 | 45 | 1.33e-15 |
| `est_t1p50_a6p0` | 841 | 0 | 444 / 0 | 358 / 0 | 39 / 0 | 0 | 2.84e-14 |
| `est_t1p80_a6p0` | 841 | 0 | 444 / 0 | 358 / 0 | 39 / 0 | 0 | 2.84e-14 |
| `est_t0p75_a4p0` | 211 | 0 | 180 / 0 | 16 / 0 | 15 / 0 | 9 | 1.33e-15 |
| `est_t0p75_a5p0` | 211 | 0 | 180 / 0 | 16 / 0 | 15 / 0 | 9 | 1.33e-15 |
| `est_t0p75_a7p6` | 211 | 0 | 180 / 0 | 16 / 0 | 15 / 0 | 9 | 1.33e-15 |
| `cens_t0p50_a6p0` | 151 | 0 | 120 / 0 | 16 / 0 | 15 / 0 | 5 | 1.33e-15 |
| `cens_t0p75_a6p0` | 973 | 0 | 510 / 0 | 418 / 0 | 45 / 0 | 0 | 1.33e-15 |
| `cens_t1p00_a6p0` | 151 | 0 | 120 / 0 | 16 / 0 | 15 / 0 | 0 | 1.33e-15 |
| `cens_t1p25_a6p0` | 151 | 0 | 120 / 0 | 16 / 0 | 15 / 0 | 0 | 1.42e-14 |
| `cens_t1p50_a6p0` | 151 | 0 | 120 / 0 | 16 / 0 | 15 / 0 | 0 | 1.33e-15 |
| `cens_t1p80_a6p0` | 151 | 0 | 120 / 0 | 16 / 0 | 15 / 0 | 0 | 2.84e-14 |
| `est_signed_t0p75_a6p0` | 757 | 0 | 420 / 0 | 298 / 0 | 39 / 0 | 45 | 3.55e-15 |
| `asscored_t0p75_a6p0` | 241 | 0 | 210 / 0 | 16 / 0 | 15 / 0 | 11 | 1.33e-15 |
| `pair_counts` | 81 | 0 | 72 / 0 | 9 / 0 | 0 / 0 | 0 | 0 |

## Differences

None above 1e-9.

## Entries of the first program's file that were not compared

| Entry | Numeric entries | Reason |
|---|---|---|
| `scorings.est_t0p75_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.cens_t0p75_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.asscored_t0p75_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.ii_t0p75_a6p0` | 242 | outside the brief (ii_* and est_gap2_* are to be ignored) |
| `scorings.est_signed_t0p75_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.est_gap2_t0p75_a6p0` | 242 | outside the brief (ii_* and est_gap2_* are to be ignored) |
| `scorings.est_t0p50_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.cens_t0p50_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.est_t1p00_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.cens_t1p00_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.est_t1p25_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.cens_t1p25_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.est_t1p50_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.cens_t1p50_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.est_t1p80_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.cens_t1p80_a6p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.est_t0p75_a4p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.est_t0p75_a5p0.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `scorings.est_t0p75_a7p6.bootstrap` | 1 | a switch of the first program (whether it bootstrapped this scoring), not a result |
| `seconds` | 1 | run time of the first program |
| `code` | 0 | text, not a number |
| `status` | 0 | text, not a number |
| `written` | 0 | text, not a number |
| `common_sha256` | 0 | text, not a number |

Every other numeric entry of the file (scorings `est_*`, `cens_*`, `est_signed_*`, `asscored_*`, their `oracle_diag` blocks, and `pair_counts`) was compared.

## Numbers on the brief's list for which the first program's file has no counterpart

The second program computed every number the brief lists. The first program did not bootstrap every scoring and did not score every source in every scoring, so these numbers of the second program stand alone (they are checked only by the self-check `r4_naive_v01.py`).

| Scoring | On the brief's list | With counterpart | Without | What is without counterpart |
|---|---|---|---|---|
| `asscored_t0p75_a6p0` | 630 | 210 | 420 | interval: 408; share: 12 |
| `cens_t0p50_a6p0` | 630 | 120 | 510 | interval: 408; point: 90; share: 12 |
| `cens_t0p75_a6p0` | 630 | 510 | 120 | interval: 120 |
| `cens_t1p00_a6p0` | 630 | 120 | 510 | interval: 408; point: 90; share: 12 |
| `cens_t1p25_a6p0` | 630 | 120 | 510 | interval: 408; point: 90; share: 12 |
| `cens_t1p50_a6p0` | 630 | 120 | 510 | interval: 408; point: 90; share: 12 |
| `cens_t1p80_a6p0` | 630 | 120 | 510 | interval: 408; point: 90; share: 12 |
| `est_signed_t0p75_a6p0` | 630 | 420 | 210 | interval: 180; point: 30 |
| `est_t0p50_a6p0` | 630 | 444 | 186 | interval: 156; point: 30 |
| `est_t0p75_a4p0` | 630 | 180 | 450 | interval: 408; point: 30; share: 12 |
| `est_t0p75_a5p0` | 630 | 180 | 450 | interval: 408; point: 30; share: 12 |
| `est_t0p75_a6p0` | 630 | 510 | 120 | interval: 120 |
| `est_t0p75_a7p6` | 630 | 180 | 450 | interval: 408; point: 30; share: 12 |
| `est_t1p00_a6p0` | 630 | 444 | 186 | interval: 156; point: 30 |
| `est_t1p25_a6p0` | 630 | 444 | 186 | interval: 156; point: 30 |
| `est_t1p50_a6p0` | 630 | 444 | 186 | interval: 156; point: 30 |
| `est_t1p80_a6p0` | 630 | 444 | 186 | interval: 156; point: 30 |
| pair counts | 72 | 72 | 0 | - |
| **Total** | **10782** | **5082** | **5700** | |

Detail per scoring (groups of entries without counterpart) is in `RECOUNT4_COMPARE_v01.json`, key `own_brief_numbers_without_counterpart`.

