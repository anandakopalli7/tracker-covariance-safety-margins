# Licences for data, plans and documents

Copyright (c) 2026 Ananda Siva Kumar Kopalli Naga Venkata

This deposit uses three licences.

| What | Licence |
|---|---|
| Program code | MIT (see `LICENSE`) |
| Everything derived from nuScenes logs (listed below) | CC BY-NC-SA 4.0, and the nuScenes Dataset Terms |
| All other data, plans and documents | CC BY 4.0 |

To give attribution, cite the manuscript and this archive as shown in `README.md`.

## Data derived from nuScenes logs

Everything in this deposit that is derived from nuScenes logs is shared under the Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International licence (CC BY-NC-SA 4.0,
https://creativecommons.org/licenses/by-nc-sa/4.0/) and under the nuScenes Dataset Terms
(https://www.nuscenes.org/terms-of-use). Those terms allow non-commercial use only, and they say that data derived from
the datasets is subject to the same terms.

No nuScenes data itself is included. The nuScenes data must be obtained from their publisher.

This covers:

- the zip `arrays_F_nuscenes.zip` in the accompanying archive (the real-log decision arrays and clearances, and the
  masked-detection arrays of the real-log dropout study);
- `results/F_nuscenes/` and `results/F_dropout_nus/`;
- the three adapter-check files, which list sample tokens of the dataset:
  `code/F_nuscenes/notes/ADAPTER_CHECK_DECISIONS_v01.json`, `code/F_nuscenes/check2/ADAPTER_CHECK2_v01.json` and
  `code/F_nuscenes/check2/ADAPTER_CHECK2_v02.json`;
- the result files that the second programs of the real-log parts wrote beside themselves:
  `code/F_nuscenes/recount/F_RECOUNT_*.json`, `code/F_nuscenes/recount_mech/MECH_RECOUNT_*.json`,
  `code/F_dropout_nus/recount/FN5B_RECOUNT_*.json` and `code/F_dropout_nus/post/DIAG_INDEP_v01.json`;
- the scene lists and masks of the real-log dropout study: `code/F_dropout_nus/masks/FN5B_MASKS_v01.json` and
  `code/F_dropout_nus/code/val_order_v01.txt`;
- the copies of real-log results in the verification record: `verification/A_EXPORT_M.json`, `A_RECOUNT_M.json`,
  `A_EXPORT_N5B.json`, `A_RECOUNT_N5B.json`, `FN5B_VALUES_v01.json`, `NUS5B_COMPARE_v01.json` and
  `M_COMPARE_EXPORT_v01.json`;
- the real-log values wherever a combined file repeats them (for example `verification/DERIVED_v13.json`).

## All other data, plans and documents

Everything else that is not program code is licensed under the Creative Commons Attribution 4.0 International licence
(CC BY 4.0, https://creativecommons.org/licenses/by/4.0/):

- the plans, amendments, lock files and freeze manifests (`plans/`, `locks/`);
- the definitions, specifications and notes kept beside the programs;
- the result files of the simulated runs (`results/`, and the result files written beside the second programs under `code/`);
- the verification record (`verification/`) and the review record (`reviews/`), except the real-log items listed above;
- the arrays of the simulated runs in the accompanying archive (`arrays_B.zip`, `arrays_CD.zip`, `arrays_F_dropout.zip`,
  `arrays_old_runs.zip`, `arrays_old_runs_record.zip`).
