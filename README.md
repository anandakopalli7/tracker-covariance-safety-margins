# Tracker Covariances as Safety Margins in Motion Planning: plans, code, and result files

DOI: 10.5281/zenodo.24454179 (https://doi.org/10.5281/zenodo.24454179)

Repository: https://github.com/anandakopalli7/tracker-covariance-safety-margins

This repository is the code and record deposit for the manuscript

> A. S. K. Kopalli, "Tracker Covariances as Safety Margins in Motion Planning: A Preregistered Equal-Caution Study in Simulation," manuscript submitted to the IEEE Open Journal of Intelligent Transportation Systems (version v13).

The per-decision arrays are in the Zenodo record named above (six zip files, about 2.5 GB; see "Arrays" below), together with their manifest and a snapshot of this repository.

## What the study is

The study asks whether the covariance that an object tracker reports for each road user is useful to a motion planner as a safety margin, compared with a fixed class-average margin set to the same overall caution. It tests this on simulated driving in CARLA, in open loop and with the planner driving the car, and on recorded driving logs from nuScenes. The plans were written and hash-locked before the values they cover were computed, and every value printed in the main text was computed by one program and recounted by a second, independently written one.

The manuscript and its supplement are not in this repository. The scripts that generate the manuscript's text and tables from the result files contain the manuscript's wording and will be added when the article is published.

## Folder layout

| Folder | Content |
|---|---|
| `plans/` | The plan (`PLAN_v13.md`), the feasibility note, and every amendment, including the copy of each amendment as it stood at each lock (`..._at_LOCK_...`) |
| `locks/` | The lock files (`LOCK_*.txt`): each records SHA-256 hashes of a plan and of the freeze manifests |
| `locks/work_locks/` | The freeze manifests (`FREEZE_*.json`): file lists with SHA-256, written when each part's code was frozen |
| `code/shared/` | The tracker library used by every part (`trackers/`) and small tools (`tools/`) |
| `code/scoring_library/` | The scoring library that both programs import (`optA_lib_v02.py` and the modules it is used with) |
| `code/B_retrack/` | Offline re-tracking with other filters: first programs (`code/`), second programs (`recount/`, `recount_fresh/`), the second IMM (`imm2/`), definitions |
| `code/CD_capture/` | Fresh simulated runs: case files, job lists and job scripts, extraction and analysis (`analysis/`), second programs (`recount/`, `recount_d/`, `recount_imm2/`), the crossing study (`crossing/`), the later lead-braking set (`l12/`), exports (`export/`) |
| `code/E_closedloop/` | Closed-loop software (`src/`, `src_v04/`, `src_v05/`), its tests, tools and job lists, the analysis (`analysis/`) and the second programs (`recount/`) |
| `code/F_nuscenes/` | Real-log software: adapter, tracking, scoring (`code/`), second programs (`recount/`, `recount_mech/`, `check2/`), notes |
| `code/F_dropout/`, `code/F_dropout_nus/` | Detection-dropout studies in simulation and on the real logs: specifications, first programs, second programs (`recount/`), masks |
| `code/A_text/` | `RESULTS_INTERFACE_v13.md`, which lists the result keys the text reads, and the figure script |
| `code/old_runs/` | First and second programs of the two earlier, exploratory analyses of the old evaluation runs (drafts v11 and v12) |
| `results/<part>/` | Result files by part: each part's `out/` folders and the outputs written beside the second programs. `results/CD_capture/REPLACEMENTS_C_v13.json` and `results/CD_capture/crossing/REPLACEMENTS_X_v13.json` list the replaced runs |
| `results/shared/` | The multiplicity (Holm) results with their second programs and outputs, and the cross-part checks |
| `results/old_runs/` | Result files of the earlier exploratory analyses of the old evaluation runs. `tables/` holds the full tables of that analysis: every table of draft v12's supplement and manuscript (tables and captions only), and the two table files they were built from |
| `verification/` | The verification record of the paper package: both programs' exports as read by the text, their comparisons, the claim audits, the build report and the text freeze (`TEXT_FREEZE_v13.md`, which lists the input result files with their hashes) |
| `reviews/` | Every presubmission review round by an AI panel (drafts v10 to v13, including the three author rounds of v13): the briefs sent to the panel, the seat reports, the reviews, and the response to the review of draft v12 |
| `tools/rebuild_tree.py` | Rebuilds the original folder layout from this repository (see below) |

Three files at the top level relate deposited files to their sources:

- `PROVENANCE_MAP.tsv`: for every copied file, its original path, its SHA-256 here and at the source, and the source's file time.
- `SANITIZE_NOTE_DEPOSIT.md`: the changes made to copied files (local machine paths and a short list of masked names), with the original and new SHA-256 of every changed file.
- `MANIFEST_SHA256.txt`: every file of this repository with its size and SHA-256.

**File times.** A git repository does not keep file times. The time of every source file (the author's machine clock) is in `PROVENANCE_MAP.tsv`, and the array zips keep the file times of their members.

Code and results sit side by side in the project (`work/<part>/code`, `work/<part>/out`, ...). Here the same relative paths appear under `code/<part>/` and `results/<part>/`: a file is under `results/` when one of its folders is named `out...` (or `sealing`), or when it is a replacement list; everything else is under `code/`. Result files that a second program wrote into its own folder therefore stay beside it under `code/`. A few folders named `pods`, `logs` or `packets` hold only the files that a freeze manifest names.

## Where the paper's input files are

`verification/TEXT_FREEZE_v13.md` lists the result files the frozen text reads. All of them are in this repository; `PROVENANCE_MAP.tsv` gives their places. For example:

| In the freeze list | Here |
|---|---|
| `B_retrack\out\A_EXPORT_B.json`, `A_RECOUNT_B.json` | `results/B_retrack/out/` |
| `CD_capture\out\A_EXPORT_C.json`, `A_RECOUNT_C.json`, and the D, X, Y, YN, XH pairs | `results/CD_capture/out/` |
| `E_closedloop\out\A_EXPORT_E*.json`, `A_RECOUNT_E*.json` | `results/E_closedloop/out/` |
| `F_nuscenes\out\A_EXPORT_F.json` and the DR, DR2, DR10, DRF, M, N5B pairs | `results/F_nuscenes/out/` |
| `shared\holm\`, `shared\holm_recount\`, `shared\checks\step0_recount\` | `results/shared/` |
| `F_dropout\recount\DR_A11_PR_POSTHOC_RECOUNT_v01.json` | `code/F_dropout/recount/` |

Some of these files held a local path and were changed by the path rule, so their SHA-256 here differs from the freeze list; `SANITIZE_NOTE_DEPOSIT.md` gives both hashes.

## The two programs

For every printed value there is a first program and a second program (a "recount").

- The second programs were written in separate sessions from the plan text and the definitions files, without reading the first programs.
- The two share three things, as the plan allows: the scoring library (`code/scoring_library/optA_lib_v02.py`), the stored per-decision arrays, and the resample draws (fixed seeds).
- Each part exports its values under agreed keys: `A_EXPORT_<part>.json` from the first program and `A_RECOUNT_<part>.json` from the second. The comparison files (`*COMPARE*.json`) and `verification/RECOUNT_COVERAGE_v13.md` record their agreement.

## Rerunning the recounts

The calls below are quoted from the programs' own notes. They were not re-run when this deposit was assembled.

**Before running anything:**

1. Rebuild the layout: `python tools/rebuild_tree.py <folder>` writes every file to `<folder>/ARS_TRIAL/<original path>`.
2. Unzip the arrays: `arrays_B.zip`, `arrays_CD.zip`, `arrays_F_dropout.zip` and `arrays_F_nuscenes.zip` into `<folder>/ARS_TRIAL/revision_v13/work/`, and `arrays_old_runs.zip` into `<folder>/ARS_TRIAL/`. Unzip `arrays_old_runs_record.zip` anywhere: its top folder `earlier_phase_folder_1` stands for `<earlier-phase folder 1>`.
3. Set the paths. Most programs held absolute paths of the author's machine. In this deposit those read `ARS_TRIAL\...` (the project folder), `<library folder>\...` or `<earlier-phase folder N>` (the earlier-phase folders), or `<user folder>\...`. Replace them with your own folders. The dropout recounts take their roots from the environment instead (`DR_P_ROOT`, `DR_ROOT`, `DR_LOCK`).
4. Put the scoring library where the program looks for it (the folder named in its `sys.path` line, or `DR_P_ROOT`).

**Python.** The parts' notes give CPython 3.12 (3.12.2 on the author's machine) with numpy 2.5.4 and numba 0.68.1 (llvmlite 0.50.0); some second programs also use `scipy.stats.rankdata`. The full package list of the capture and analysis environment is `results/CD_capture/analysis/out/VENV_FREEZE.txt`; package B's is `code/B_retrack/VENV_FREEZE_B.txt`. The notes run every script with `python -I` (isolated mode).

| Part | Second program | Call, as documented | Documented in |
|---|---|---|---|
| B, old runs | `code/B_retrack/recount/` | `python run_all.py` | `recount/README_recount.md`, docstring of `run_all.py` |
| B, fresh runs | `code/B_retrack/recount_fresh/recount_fresh.py` | `python -I -B -X utf8 recount_fresh.py --fresh [--variants ...] [--K n]`, then `--fresh --combine`; also `--fresh --b6`, `--tu`, `--test-old` | `recount_fresh/README_recount_fresh.md` |
| C, lead braking and cut-in | `code/CD_capture/recount/rc_c_lead_v13.py`, `rc_c_cutin_v13.py` | Three steps (export, runner, import); the runner is `python -I -B rc_calib_remote_v13.py JOBDIR LABEL --seeds SEED --outer LO:HI --threads 1` | `recount/README_RECOUNT_C.md` |
| C, rate and latency (B7) | `recount/rc_b7_v13.py` | `.venv\Scripts\python.exe -I -B -X utf8 recount\rc_b7_v13.py` | `recount/README_RECOUNT_B7.md` |
| C, supplement families | `recount/rc_s57a_v13.py`, `rc_s57b_v13.py` | `python -I -B -X utf8 rc_s57a_v13.py --workers 2`; `rc_s57b_v13.py --workers 1 --merge` | `recount/README_RECOUNT_S57A.md`, `README_RECOUNT_S57B.md` |
| Crossing | `recount/rc_x_cross_v13.py` | `rc_x_cross_v13.py --family pedestrian_crossing ...` with `--calib export`, the runner `rc_x_calib_remote_v13.py`, then `--calib import` | `recount/README_RECOUNT_X.md` |
| Permuted twin (Y) | `recount/rc_y_twin_v13.py` | `rc_y_twin_v13.py --intervals calibrated\|nominal99\|nominal95` | `recount/README_RECOUNT_Y.md` |
| D, other lead behaviour | `code/CD_capture/recount_d/` | `.venv\Scripts\python.exe -I -B -X utf8 recount_d\rc_d_nonbraking_v13.py`; `recount_d\rc_d2_event_table_v13.py --logs-root <folder>` | `recount_d/README_RECOUNT_D.md` |
| E, closed loop | `code/E_closedloop/recount/e_recount_v03.py` (and `_v04`, `e_recount_e5_v01.py`, `e_recount_e6_v01.py`) | `python -I -B e_recount_v03.py outcomes <runs_dir> <prefix> --out <file>`; then `brake`, `calibration`, `compare` | `recount/README_RECOUNT_v03.md`, `README_E4_v01.md`, `README_E5_v01.md` |
| F, real logs | `code/F_nuscenes/recount/fr_horizon_v02.py`, `fr_heldout_v02.py` | `..\venv\Scripts\python.exe -I <script>` from the `recount` folder | `recount/README_RECOUNT.md` |
| F, mechanism | `code/F_nuscenes/recount_mech/fm_recount_v02.py` | `python -I fm_recount_v02.py train\|val T1\|IMM [--scenes N] [--no-calib]` | its docstring |
| Dropouts, simulation | `code/F_dropout/recount/dr_recount_v02.py` (and the `a12`, `a12_hz10`, `a13_flag`, `a11_pr_posthoc` programs) | `python -I dr_recount_v02.py [--test-old] [--threads N] [--nboot N] [--out PATH]` | its docstring |
| Dropouts, real logs | `code/F_dropout_nus/recount/fn_recount_v02.py` | `python -I fn_recount_v01.py --set unmasked\|masked [--threads N] [--nboot N] [--out PATH]` (the docstring of v02 still names v01) | its docstring |
| Multiplicity (Holm) | `results/shared/holm_recount/A12_HOLM_RECOUNT_PROGRAM_v01.py`, `A13_HOLM_RECOUNT_PROGRAM_v01.py` | `python -I A12_HOLM_RECOUNT_PROGRAM_v01.py` (it reads `work\` by an absolute path); from `work\`, `python -I shared\holm_recount\A13_HOLM_RECOUNT_PROGRAM_v01.py` | the file headers |

### What each recount reads

This is what the parts' notes, or the programs' own path lines, say. It was not tested. The fresh-run programs also check that the lock files exist before they open fresh arrays.

**These need run logs (not deposited, available on request):**

- E, closed loop: every recount reads the run folders (`<runs_dir>`). The per-run outcome files that both programs wrote from them are deposited (`results/E_closedloop/out/OUTCOMES_*.json`, `*_RECOUNT_OUTCOMES_*.json`).
- D2 (the event table, `--logs-root`) and the reaction-and-stop part of the supplement families (`recount_d\rc_d2_rs_v13.py`): the arrays and each run's logs.
- C, cut-in: the event truth is made from each run's logs. Its saved result is deposited (`results/CD_capture/recount/out/RC_C_CUTIN_TRUTH_v13.json`) and the recount accepts it with `--truth-file`.
- B, fresh runs, stop reliance (`recount_fresh.py --fresh --b6`): the stop clearances and each run's truth log.

**These need the record arrays of the old runs, which were kept in an earlier-phase folder:**

- B, old runs (`code/B_retrack/recount/`), B's tuning-run intervals (`--tu`), and every `--test-old` mode of the fresh-run recounts.
- C, lead braking, and the supplement families: the design step of the per-phase schedule loads the 35 old evaluation runs.
- The `matched` step of the closed-loop recount, which loads the 35 old evaluation runs.
- The second programs of the earlier exploratory analyses (`code/old_runs/`).

The old runs' record arrays are in the deposit (`arrays_old_runs_record.zip`):

- the base arrays of 223 runs (`09_redesign/m2_decisions/openloop/gateR_rt_v01/`: clearances, critical scales of the class average, of the tracker covariance and of the oracle);
- the extracts with the NIS-inflated, acceleration-margin and braking-prediction sources of the 35 evaluation runs (`11_ojits/A4/fit/extract/`) and of 20 tuning runs (`11_ojits/A4/dryrun/extract/`);
- the reaction-and-stop arrays of the 35 evaluation runs (`11_ojits/A5/fit/main/extract/` and `11_ojits/review/optionA_recount_v01/cache/`);
- the class-average data file (`pbar_tuning_v01.json`).

These are the array folders named by the loader of record (`code/scoring_library/rev_common_v01.py`), by the second programs of parts B and CD, and by the deposit list of the earlier draft. The arrays of the earlier analyses that lie in the project folder are in `arrays_old_runs.zip`.

Still not in the deposit, and available on request:

- the modules of record that those programs import from earlier-phase folders (the open-loop extraction and scoring helpers). They are program code and are not deposited, except the copies in `code/scoring_library/`. A recount that imports one of the others cannot run from the deposit alone;
- the old runs' raw recordings, which the stop-reliance and cut-in parts of the old-run recounts read;
- the run index of the earlier phase (`run_index_m4_v02.csv`), which the recount core of parts C and D names.

**This one needs a nuScenes extract that is not deposited:**

- Dropouts on the real logs: the masked arrays are deposited, but the program also reads each scene's keyframe times from the per-scene extract of the dataset.

**For these, the notes name only arrays and files that are in this deposit.** Whether the programs read anything from the groups above was not checked for each one.

- C, rate and latency (B7): the fresh arrays and the re-detection files; the note says no second extraction is made.
- Crossing and the permuted twin (Y): the crossing arrays, the adaptive filter's arrays, the case lists and the replacement lists.
- D1 (other lead behaviour, open loop): the fresh arrays of the D1 cases.
- B, fresh runs, the tracker variants (`recount_fresh.py --fresh`): the fresh arrays of parts B and CD, the case list and the replacement list.
- F, real logs (`fr_horizon`, `fr_heldout`): the decision arrays, the clearances, the resample draws and the scoring library.
- Dropouts in simulation: the dropout arrays, the class averages and the mask files.
- Multiplicity (Holm): the exports of the tests in the family.

## Arrays

The Zenodo record holds six array zip files. `ARRAYS_MANIFEST.txt` (in the record) lists every member with its SHA-256. The zips keep the file times of their members.

| Zip | Members | Content |
|---|---|---|
| `arrays_B.zip` | 2,904 | Re-tracked arrays of every tracker variant on the old runs, the fresh runs and the later lead-braking set; stop clearances; resample rows of both programs |
| `arrays_CD.zip` | 4,335 | Fresh-run arrays (tracker of record, IMM, rate and latency chains, reaction-and-stop, cut-in, crossing, the later set), the re-detection files of the rate and latency chains, heading arrays, calibration jobs and resample rows |
| `arrays_F_dropout.zip` | 3,279 | Dropout arrays in simulation at every dropout rate and at 10 Hz, class averages, calibration rows |
| `arrays_F_nuscenes.zip` | 2,023 | Real-log decision arrays (both trackers, design and held-out scenes), clearances, masked-detection arrays, calibration rows |
| `arrays_old_runs.zip` | 263 | Arrays of the earlier analyses that lie in the project folder: lead state, time gap, extended clearances, braking prediction, and the arrays kept beside the earlier second programs |
| `arrays_old_runs_record.zip` | 349 | Record arrays of the old runs from the earlier phase: the base arrays of 223 runs, the source extracts of the 35 evaluation runs and of 20 tuning runs, the reaction-and-stop arrays of the 35 evaluation runs, and the class-average data file |

Members are byte-identical copies of the source files, with two exceptions. 101 array files in `arrays_CD.zip` held a local machine path in their metadata member; in each, only that member was rewritten, and every other member is unchanged. The class-average data file in `arrays_old_runs_record.zip` is a JSON text in which one path value was changed by the path rule. `SANITIZE_NOTE_DEPOSIT.md` gives the SHA-256 of each such file before and after, and `ARRAYS_MANIFEST.txt` marks them.

The real-log arrays are derived from nuScenes logs; see `LICENSE-DATA.md`.

## Not deposited, available from the author on request

- **The 20 Hz lidar sweeps** of the simulated runs.
- **The raw simulation run logs:** the closed-loop run folders (about 24 GB) and the run folders of the fresh runs of parts C and D (truth, frames, detections and tracker logs of each run).
- **The old runs' raw recordings and the earlier programs that sit in earlier-phase folders:** the raw recordings of the old runs, the modules of record that the old-run recounts import, and the programs and result files of the analyses before draft v11. The old runs' record arrays are deposited (see "Arrays").
- **The earlier-phase simulation, recording and planner software,** on which the closed-loop and capture programs here are built, and the software bundles that were sent to the cloud machines.

## Not included

- **nuScenes data.** Available from its publisher under its terms. No nuScenes data itself is included.
- **Detector.** Third-party: the CenterPoint voxel model in its nuScenes configuration; checkpoint SHA-256 `59936925…e8ca32` (in full: `59936925ca42c53e8b7cf37afffca6549de282d2440b23b8e0ae168d69e8ca32`), as identified in Supplement S1.
- **Tracker.** Third-party: CANMOT, commit `515d0792…` (in full: `515d0792a4a2dddf4f3f26c2fa26c54bb1c14167`) with one recorded local change (the yaw innovation folded into a half turn), as identified in Supplement S1.
- **nuScenes devkit, the simulator (CARLA) and other third-party packages.** Not redistributed. Small local stand-ins for a few packages, written for this project, are in `code/shared/trackers/shims_v01/` and `code/F_nuscenes/lib/shims_v01/`.
- **Cloud job logs, machine addresses and credentials.**
- **The manuscript and supplement,** the text fragments they are built from, and the scripts that generate the text (see above).

## Named in a freeze manifest, not deposited

The freeze manifests in `locks/work_locks/` list files with their SHA-256. Most of the listed files are in this deposit. These are not; most of them are third-party code:

| Where (in the project folder `work\`, or an earlier-phase folder) | Files | Why not deposited |
|---|---|---|
| `CD_capture\packets\` | `packet_d1_v13.tar.gz`, `packet_l12_v13.tar.gz`, `packet_main_v03.tar.gz`, `packet_x_v13.tar.gz` | Software bundle sent to the cloud machines; it packs the earlier-phase software (available on request) |
| `E_closedloop\packets\` | `packet_e_v02.tar.gz`, `packet_e_v03.tar.gz`, `packet_e_v04.tar.gz`, `packet_e_v05.tar.gz` | Software bundle sent to the cloud machines; it packs the earlier-phase software (available on request) |
| `E_closedloop\tools\` | `runpodctl.exe` | Third-party program (cloud provider command-line tool) |
| `F_nuscenes\lib\code149\` | `consumer.py`, `finite_primitive.py`, `online_tracker.py`, `sensor_adapter.py`, `tracker_audit.py` | Earlier-phase software (available on request) |
| `F_nuscenes\lib\devkit\` | 165 files | Third-party code (nuScenes devkit) |
| `F_nuscenes\lib\vendor149\CANMOT\` | 63 files | Third-party code (CANMOT tracker) |
| `F_nuscenes\lib\vendor149\` | `design_core_v85.py`, `fast_hull.py`, `fast_overlap.py`, `fast_overlap_array.py` | Earlier-phase software (available on request) |
| `F_nuscenes\logs\` | `f01_prepare_train_v01.json` | Copies nuScenes metadata: the scene table of the 700 training scenes (tokens, descriptions, log file names) |
| `<earlier-phase folder 1>\09_redesign\m2_decisions\openloop\` | `olcore_rt_v01.py`, `ox12_core_v01.py`, `oxsb_core_v01.py`, `ol_gateR_rt_extract_v01.py` | Module or data file of record kept in an earlier-phase folder, outside the project folder (available on request) |
| `<earlier-phase folder 2>\149_supported_sensor_preparation_20261101\code\` | `online_tracker.py`, `consumer.py`, `finite_primitive.py`, `sensor_policy.py` | Module or data file of record kept in an earlier-phase folder, outside the project folder (available on request) |
| `<earlier-phase folder 2>\149_supported_sensor_preparation_20261101\vendor\` | `fast_overlap_array.py` | Module or data file of record kept in an earlier-phase folder, outside the project folder (available on request) |
| `<earlier-phase folder 2>\149_supported_sensor_preparation_20261101\vendor\CANMOT\src\canmot\motion_module\` | `kalman_filter.py`, `motion_model.py` | Module or data file of record kept in an earlier-phase folder, outside the project folder (available on request); third-party tracker code |
| `<earlier-phase folder 2>\149_supported_sensor_preparation_20261101\vendor\CANMOT\src\canmot\tracking\` | `nusc_trajectory.py`, `nusc_tracker.py` | Module or data file of record kept in an earlier-phase folder, outside the project folder (available on request); third-party tracker code |
| `<earlier-phase folder 1>\06_phase0\scenarios\` | `DEVELOPMENT_PROTOCOL_MAIN_v01.json` | Module or data file of record kept in an earlier-phase folder, outside the project folder (available on request) |
| `<earlier-phase folder 1>\09_redesign\m4_perception_model\` | `run_index_m4_v02.csv` | Module or data file of record kept in an earlier-phase folder, outside the project folder (available on request) |

Named in a freeze manifest at a place in an earlier-phase folder, with an identical copy (same SHA-256 at the source) in this deposit:

- `<earlier-phase folder 1>\09_redesign\m2_decisions\openloop\olcore_v01.py`: deposited as `code/scoring_library/olcore_v01.py`
- `<earlier-phase folder 1>\09_redesign\m2_decisions\openloop\ol_gateR_core_v01.py`: deposited as `code/scoring_library/ol_gateR_core_v01.py`
- `<earlier-phase folder 1>\09_redesign\m2_decisions\openloop\ol_extract_v01.py`: deposited as `code/scoring_library/ol_extract_v01.py`
- `<earlier-phase folder 1>\09_redesign\m2_decisions\openloop\pbar_tuning_v01.json`: deposited as `arrays_old_runs_record.zip, member earlier_phase_folder_1/09_redesign/m2_decisions/openloop/pbar_tuning_v01.json (a path value changed by the path rule)`
- `<earlier-phase folder 1>\11_ojits\A6R\code\optA_lib_v02.py`: deposited as `code/scoring_library/optA_lib_v02.py`
- `<earlier-phase folder 2>\149_supported_sensor_preparation_20261101\contracts\tracker_config.json`: deposited as `code/F_nuscenes/lib/tracker_config.json`

## How the plans were locked

Each plan and amendment was hashed (SHA-256) into a lock file before the values it covers were computed, and each part's code was frozen in a manifest that the lock files also hash. The locks were made on the author's machine: the evidence of their order is the hash chain and the local file times, which `PROVENANCE_MAP.tsv` records. There is no third-party timestamp.

Some plan, lock and manifest files held local paths or one of the masked names and were changed, so their SHA-256 here differs from the one a lock records. `SANITIZE_NOTE_DEPOSIT.md` gives the original hash of each such file.

## Use of generative AI

Generative AI wrote the code in this repository under the author's direction: Claude (Anthropic) wrote the analysis, simulation-control, text and figure programs, the first programs and, in separate sessions, the second programs; Codex (OpenAI) was used to develop the simulation, recording and planner software of the earlier phase. AI sessions also drafted the plans and amendments, which the author approved. The reviews in `reviews/` are by AI panels.

## Licences

- Code: MIT (`LICENSE`).
- Everything derived from nuScenes logs: CC BY-NC-SA 4.0 and the nuScenes Dataset Terms (non-commercial). `LICENSE-DATA.md` lists what this covers.
- All other data, plans and documents: CC BY 4.0 (`LICENSE-DATA.md`).

## How to cite

Please cite the manuscript above and this archive:

> A. S. K. Kopalli, "Tracker Covariances as Safety Margins in Motion Planning: plans, code, and result files," version v13, 2026. DOI: 10.5281/zenodo.24454179

`CITATION.cff` holds the same in machine-readable form.
