# Recount3: comparison with the first program

Written 18 Nov 2026 18:30 by `r3_compare_v01.py`. First program: `revision_v11\analysis\out\REV_G_PARTIAL_DRAWS_v01.json`, `REV_D_BOOTSTRAP_v01.json` (`D3_sensitivities.m_out_of_n`), `REV_E3_EXTENDED_GAP2_v01.json`, `REV_F2_BRAKING_PRIOR_v01.json`. Second program: `RECOUNT3_RESULTS_v01.json` and `r3_extra_v01_out.json`. The first program's files were opened only after `RECOUNT3_RESULTS_v01.json` had been written (sha256 in the report) and were not changed.

A number "differs" when the absolute difference exceeds 1e-9 (or when it is defined in one program only, or a flag differs). Where both programs give "undefined" (no ratio because the denominator is not positive in the full sample or in every resample), the number counts as compared and equal.

Classes: **A** = asked for by the brief; **B** = other numbers of the results file, or arithmetic on it; **C** = supplementary (r3_extra_v01.py, written after the files were opened).

## Counts

| Item | Class | Compared | Differ by > 1e-9 | Largest absolute difference | Undefined in both |
|---|---|---|---|---|---|
| 1. Table S12b (partial oracles over 50 draws) | A | 45 | 0 | 1.11e-16 | 0 |
| 1.  | B | 46 | 0 | 5.55e-17 | 0 |
| 1.  | C | 36 | 0 | 1.11e-16 | 0 |
| 1.  | all | 127 | 0 | 1.11e-16 | 0 |
| 2. Table S17 (subsampling without replacement) | A | 48 | 0 | 8.88e-16 | 0 |
| 2.  | B | 120 | 0 | 8.88e-16 | 0 |
| 2.  | all | 168 | 0 | 8.88e-16 | 0 |
| 3. Table S24b (2 m gap, plans judged until their stop ends) | A | 60 | 0 | 0 | 0 |
| 3.  | B | 339 | 0 | 2.84e-14 | 30 |
| 3.  | all | 399 | 0 | 2.84e-14 | 30 |
| 4. Table S25 and the benign-run check | A | 189 | 0 | 1.42e-14 | 0 |
| 4.  | B | 267 | 0 | 2.22e-16 | 0 |
| 4.  | C | 475 | 0 | 1.78e-15 | 40 |
| 4.  | all | 931 | 0 | 1.42e-14 | 40 |
| all items | all | 1625 | 0 | 2.84e-14 | 70 |

## Coverage of the first program's files

Numeric leaves of each file (a two-element interval counts as two; flags and undefined values count; the run time, the text fields, the constants under `setting` and the block `S20.tuning_runs_of_record` are left aside) against the number of comparisons made.

| Item | File | Leaves in the first program's file | Compared |
|---|---|---|---|
| 1 | `REV_G_PARTIAL_DRAWS_v01.json` | 127 | 127 |
| 2 | `REV_D_BOOTSTRAP_v01.json: D3_sensitivities.m_out_of_n` | 168 | 168 |
| 3 | `REV_E3_EXTENDED_GAP2_v01.json` | 399 | 399 |
| 4 | `REV_F2_BRAKING_PRIOR_v01.json` | 931 | 931 |

## Differences

None. No compared number differs by more than 1e-9.

## Largest differences per item (all classes, the five largest)

**Item 1**

| Number | First program | Second program | Absolute difference |
|---|---|---|---|
| S12b phase_weighted P75 max | 0.38356819396394115 | 0.38356819396394104 | 1.11e-16 |
| S12b phase_weighted P25 of_record | -0.38255562118527275 | -0.38255562118527264 | 1.11e-16 |
| S12b phase_weighted P25 mean | -0.35086378083424746 | -0.3508637808342474 | 5.55e-17 |
| S12b phase_weighted P25 min | -0.445222625376199 | -0.44522262537619894 | 5.55e-17 |
| S12b phase_weighted P25 max | -0.2557871347003066 | -0.25578713470030656 | 5.55e-17 |

**Item 2**

| Number | First program | Second program | Absolute difference |
|---|---|---|---|
| S17 m=15 R interval (finite-population factor) upper | 6.642641360829991 | 6.642641360829992 | 8.88e-16 |
| S17 m=15 R 2.5 and 97.5 percentiles of the subsample values lower | 4.302926319825871 | 4.30292631982587 | 8.88e-16 |
| S17 m=20 R 2.5 and 97.5 percentiles of the subsample values lower | 4.616440645955573 | 4.616440645955574 | 8.88e-16 |
| S17 m=15 RR_AM interval (finite-population factor) upper | 0.4409586987655092 | 0.44095869876550925 | 5.55e-17 |
| S17 m=20 RR_AM interval (finite-population factor) upper | 0.43789984891091305 | 0.437899848910913 | 5.55e-17 |

**Item 3**

| Number | First program | Second program | Absolute difference |
|---|---|---|---|
| S24b phase1 den0 (sum over levels) interval = 201 x the pp interval upper | 237.67493784946407 | 237.6749378494641 | 2.84e-14 |
| S24b moving den0 (sum over levels) interval = 201 x the pp interval lower | 87.90336154618784 | 87.90336154618785 | 1.42e-14 |
| S24b phase_weighted den0 (sum over levels) interval = 201 x the pp interval upper | 51.42169946188745 | 51.42169946188744 | 7.11e-15 |
| S24b pairs unsafe at 2 m, 3 s window (cache) | 19900 | 19900 | 0 |
| S24b pairs unsafe at 2 m, judged until the stop ends | 19934 | 19934 | 0 |

**Item 4**

| Number | First program | Second program | Absolute difference |
|---|---|---|---|
| S25 a0=2 phase_weighted D decision-equivalents | 85.8407960199005 | 85.84079601990051 | 1.42e-14 |
| benign all over the scale grid max_caution_diff_pp | 0.09967256033465688 | 0.09967256033465866 | 1.78e-15 |
| benign moving over the scale grid max_caution_diff_pp | 0.09967256033465688 | 0.09967256033465866 | 1.78e-15 |
| S25 zero margin CK5 caution % | 2.8574131942135446 | 2.8574131942135432 | 1.33e-15 |
| S25 zero margin F0 caution % | 1.095800460076491 | 1.09580046007649 | 1.11e-15 |

## Not compared

- `REV_F2_BRAKING_PRIOR_v01.json`, `S20.tuning_runs_of_record`: copied by the first program from `OXSB_CTL_RESULTS_v02.json` (20 lead-braking tuning runs, 13 Nov 2026); not part of this brief.
- `REV_D_BOOTSTRAP_v01.json` outside `D3_sensitivities.m_out_of_n`: recounted earlier (`revision_v11\recount`).

Every single comparison (name, both values, difference, class) is in `RECOUNT3_COMPARE_v01.json`.
