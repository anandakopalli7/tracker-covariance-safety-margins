# B7 re-tracking on Linux pods: compute plan (package C, revision v13)

Written 20 Nov 2026, ~03:30 EST (this machine's clock), by the CD first-program writer for B7 (Claude Opus 5.5). **No pod was created.**
Scope (coordinator, 20 Nov 01:53 EST): B7 only. Table III's variant re-tracking (B2/B3/B4, B1 sensitivities) is package B's; its
measured laptop cost is given in §6 for B's and the coordinator's planning only.

## Conclusion
- **B7 needs 840 jobs (105 fresh lead-braking runs × 8 rate × latency chains). Measured on old run p1b_fit_finite_0037 (a full-length
  run, 300 assessment decisions), three runs: 462–712 worker-seconds per run for the 8 chains on this laptop (mean 595 s).** 105 runs ≈
  13.5–21 worker-hours, i.e. **about 7–10.5 h wall on the laptop with the allowed 2 workers (≈ 8.7 h at the mean)**; the measurements
  include the load of a shared laptop. Starting at LOCK_A10_2c (≤ 18:00 EST) the arrays would be ready at about 01:00–04:30 EST on 21 Nov;
  `c_b7_v13.py` then needs about 2.5 h more on the laptop (§5), so first-program B7 values at about 03:30–07:00 EST on 21 Nov, before the
  second program's comparison.
- **The re-tracking can run on Linux pods without editing any frozen file.** The library honours `V13_CODEX_ROOT`; every other
  hard-coded Windows path is a `sys.path` entry or a path root that Python on Linux reads as a *relative* path, so it is served by five
  symbolic links, named literally after the Windows paths, in the job's working directory (§3). `x_trk_extract_v13.py` already takes
  `--logs-root`, `--b7-root`, `--out-root`, `--part i:n` and the env variable `V13_P_ROOT`.
- **One 32-vCPU pod (RTX 4090 class, about $0.89/h) with 30 single-threaded workers: about 15–45 min of compute per family** (840 jobs ×
  36–89 s ÷ 30, plus each worker's start-up; 36 s per job is the unloaded laptop core of run 4), plus about 30 min of set-up (environment,
  upload, acceptance test) and about 10 min of transfers. Two pods halve the compute. Cost ≈ $1–2.
- **Acceptance rule (proposed):** the pod's `x_trk_extract_v13.py --test-old` output for old run 0037 (8 arrays) must be bit-identical to
  the laptop's (`analysis\out\testold_b7_arrays_final\`, reproduced bit for bit in three laptop runs; its 2 Hz, L = 0 chain equals the
  logged arrays exactly). Otherwise the pod's arrays are not used and the laptop route is taken.
- Fresh data may be uploaded only after `LOCK_A10_2c.txt` exists (the code refuses to run before it in any case). Everything else (pod,
  environment, code upload, acceptance test on 0037) can be done before.
- **Cut-in family (§7, added 03:45 EST): another 840 jobs of the same size.** Both families on the laptop would take ≈ 14–21 h wall
  with 2 workers plus ≈ 5 h of analysis, which does not fit the night after LOCK_A10_2c beside the other work; on pods both families
  take ≈ 1.5–2 pod-hours of compute (one pod for each family in parallel: ≈ 45 min each) and ≈ $2–4.

## 1. Measured cost (old run p1b_fit_finite_0037; laptop, 2 workers, shared with ~8 processes)
Per job = `retrack_capture` + `overlay` + `extract`, seconds (`analysis\out\TESTOLD_TRK_v13_extract_20261120T021957.json` = run 1,
`TESTOLD_B7_v13_extract_20261120T023623.json` = run 2):

| Chain | run 1 retrack + extract | run 2 retrack + extract | run 3 (final code) | detector rows |
|---|---|---|---|---|
| B7_2_0 | 1.3 + 59.6 = 60.8 | 20.2 + 36.2 = 56.4 | 22.5 + 40.8 = 63.2 | 69 |
| B7_2_0.1 | 4.1 + 40.2 = 44.4 | 22.7 + 79.9 = 102.6 | 21.1 + 55.4 = 76.5 | 69 |
| B7_5_0 | 9.1 + 48.7 = 57.8 | 10.6 + 60.2 = 70.9 | 8.0 + 62.0 = 70.0 | 171 |
| B7_5_0.1 | 15.0 + 83.7 = 98.6 | 15.6 + 69.2 = 84.7 | 10.3 + 39.7 = 50.0 | 171 |
| B7_5_0.2 | 32.1 + 46.5 = 78.6 | 6.8 + 39.7 = 46.4 | 6.3 + 32.8 = 39.1 | 171 |
| B7_10_0 | 29.4 + 101.0 = 130.4 | 41.7 + 72.0 = 113.7 | 19.4 + 40.8 = 60.1 | 341 |
| B7_10_0.1 | 29.3 + 102.1 = 131.4 | 13.7 + 55.5 = 69.2 | 27.9 + 33.5 = 61.4 | 341 |
| B7_10_0.2 | 33.0 + 77.0 = 109.9 | 21.6 + 45.3 = 66.8 | 8.6 + 33.1 = 41.7 | 341 |
| **per run (8 chains)** | **711.9** | **610.7** | **462.0** | |

(run 3: `analysis\out\testold_b7_arrays_final\TESTOLD_B7_v13_extract_20261120T031944.json`.)
- Wall time for the 8 jobs of one run with 2 workers: 572 s (run 1, part of 13 jobs), 419 s (run 2), 452 s (run 3, of which ≈ 210 s
  was the two workers' start-up: imports of the codex tree, numba, matplotlib). The spread comes from the laptop's other processes, not
  from the code (the three runs' arrays are bit-identical).
- Start-up is paid once per worker process (≈ 1–3.5 min on the loaded laptop), not per job.
- Run 4 (03:49 EST, the final extractor with `--family`, **one** worker, lighter laptop load; `analysis\out\testold_b7_arrays_v4\`):
  27.2, 27.8, 46.2, 24.9, 31.6, 47.8, 45.3, 37.6 s = **288.5 s per run** for the 8 chains (+ 144 s start-up); arrays bit-identical to
  runs 1–3. So an unloaded core needs ≈ 290 s per run; the 460–710 s above reflect the shared laptop.
- Retracking at 10 Hz costs 5× the tracker steps of 2 Hz, but `extract` (planner rows, clearances, CK3 for 300 decisions × 17 rows)
  dominates every chain.
- 0037 runs the full 35 s (700 frames, 300 assessment decisions). The 35 old evaluation runs average 266 decisions per run (contact
  runs end early). Fresh runs are not looked at before LOCK_A10_2c, so the estimate uses 0037: an upper-side figure.
- Memory: see §5 (measured peak of one 10 Hz job).

## 2. Laptop estimate for 105 runs
- 105 × 462–712 s (mean of the three loaded runs 595 s) = 48,500–74,800 worker-s = 13.5–20.8 worker-h. With 2 workers: **6.7–10.4 h
  wall, about 8.7 h at the mean** (≈ 0.89 × that if fresh runs are as long as the old evaluation runs on average). On an unloaded laptop
  (run 4: 289 s per run) it would be ≈ 4.2 h; the laptop is not expected to be unloaded after the lock. Cut-in: the same again (§7).
- Command (after LOCK_A10_2c): `.venv\Scripts\python.exe -I -B -X utf8 analysis\x_trk_extract_v13.py --workers 2` (skips existing files,
  so it can be stopped and restarted; one log line per job; `analysis\out\XB7_EXTRACT_c_lead_<stamp>.json` at the end).
- It competes with the other laptop work after the lock (package B's Table III re-tracking needs about 11 worker-h, §6).
- Then `c_b7_v13.py`: ≈ 2.5 h (§5). Laptop total for B7 ≈ 11.5–13 h after LOCK_A10_2c; with one pod ≈ 1.5 h for the arrays + 2.5 h
  for the analysis on the laptop (or ≈ 20 min if the analysis also runs on the pod).

## 3. Running on Linux pods: what the code touches, and what to upload or patch
Checked by reading the code and by tracing every file one job opens (Python audit hook, one 5 Hz job on 0037; scratch trace, not kept).

**Environment variables that are honoured** (not affected by `python -I`, which ignores only `PYTHON*` variables):
- `V13_CODEX_ROOT` — `trk_env_v01.setup()` and `tracker_config()` use it before the laptop default (verified in the code: `root =
  codex_root or os.environ.get('V13_CODEX_ROOT') or DEFAULT_CODEX`).
- `V13_P_ROOT` — `x_trk_extract_v13.py` takes the P̄ of record (`<P>\09_redesign\m2_decisions\openloop\pbar_tuning_v01.json`) and, in
  `--test-old`, the old archive (`<P>\07_fit_runs\archives\p1b_fit_finite_0037\`) from it.
- `OPENBLAS_CORETYPE=Haswell`, `OPENBLAS_NUM_THREADS=1`, `NUMBA_NUM_THREADS=1`, `OMP_NUM_THREADS=1`; `NUMBA_CACHE_DIR` (see below).

**Hard-coded Windows paths in the import chain** (none can be overridden by a variable):

| File (frozen or of record) | Constant | Use |
|---|---|---|
| `shared\trackers\trk_env_v01.py` | `DEFAULT_CODEX` = `<library folder>\149_supported_sensor_preparation_20261101` | overridden by `V13_CODEX_ROOT` |
| `shared\trackers\trk_arrays_v01.py` | `OPENLOOP` = `<library folder>\openloop` | `sys.path` entry for `olcore_v01`, `olcore_rt_v01`, `ol_gateR_core_v01`, `ol_gateR_rt_extract_v01`, `ol_extract_v01`, `ox12_core_v01`, `oxsb_core_v01` |
| `shared\trackers\trk_score_v01.py` | `P` = `<library folder>`; `V12` = `ARS_TRIAL\revision_v12\analysis` | `sys.path` entries `P\11_ojits\A6R\code` (optA_lib_v02) and V12 (a9_common_v01) |
| `revision_v12\analysis\a9_common_v01.py` | `V11` = `ARS_TRIAL\revision_v11\analysis` | `sys.path` entry (rev_common_v01); also `OUT = HERE\out` is created at import (must be writable) |
| `revision_v11\analysis\rev_common_v01.py` | `P` (as above) | `sys.path` entry `P\11_ojits\A6R\code`; data paths used only by `load_runs()` (not called by B7 extraction) |
| `P\...\openloop\olcore_v01.py` | `CODEX` (the codex root, as above) | `sys.path` entries `CODEX\code`, `CODEX\vendor` (redundant with `V13_CODEX_ROOT`) |
| `CD_capture\analysis\cd_common_v13.py` | `V12A` (= V12 above) | `sys.path` entry |
| `ol_gateR_core_v01.py`, `oxsb_core_v01.py`, `ox12_core_v01.py` | paths relative to their own folder (`HERE.parents[2]`, …) | defined at import; not opened by `extract` |

On Linux, `pathlib.Path(r'C:\Users\...\openloop')` is a *relative* path with one component whose name contains backslashes, and a
relative `sys.path` entry is resolved against the working directory. So **no patch is needed**: start each job in a working directory
that holds these five symbolic links (names literal, quoted):

| Link name (in the job's cwd) | Target on the pod |
|---|---|
| `<library folder>\openloop` | `<pod>/P/09_redesign/m2_decisions/openloop` |
| `<library folder>` | `<pod>/P` (gives `…/11_ojits/A6R/code`) |
| `ARS_TRIAL\revision_v12\analysis` | `<pod>/ARS_TRIAL/revision_v12/analysis` |
| `ARS_TRIAL\revision_v11\analysis` | `<pod>/ARS_TRIAL/revision_v11/analysis` |
| `<library folder>\149_supported_sensor_preparation_20261101` | `<pod>/codex` (optional; also `V13_CODEX_ROOT=<pod>/codex`) |

(Alternative, if links named with backslashes are not wanted: a ten-line launcher that puts the five pod folders on `sys.path` before
importing `x_trk_extract_v13`. That is new code and would have to enter FREEZE_CD_2 before LOCK_A10_2c; the links need no code.)

**Folders and files to upload** (mirroring the laptop layout under one pod root, because `cd_common_v13.py` finds `CD_capture`, the run
lists, the arrays folder and the lock files relative to its own location):

| What | Laptop source | Size |
|---|---|---|
| Codex tree (tracker, planner, CANMOT, nuScenes devkit, numba-compiled helpers) | `<earlier-phase folder 2>\149_supported_sensor_preparation_20261101\{code, sources, vendor, legacy86\vendor\nuscenes-devkit\python-sdk, contracts}` | ≈ 4.5 MB |
| Extractors of record | `P\09_redesign\m2_decisions\openloop\` (the 7 modules above + `pbar_tuning_v01.json`; the folder has 276 files, a few MB) | small |
| Scoring library of record | `P\11_ojits\A6R\code\optA_lib_v02.py` | small |
| v11 / v12 helpers | `ARS_TRIAL\revision_v11\analysis\rev_common_v01.py`, `ARS_TRIAL\revision_v12\analysis\a9_common_v01.py` | small |
| Frozen tracker library | `revision_v13\work\shared\trackers\` (all, with `shims_v01\`, `trk_constants_v01.json`) | 174 KB |
| Package-C code and run list | `revision_v13\work\CD_capture\analysis\{x_trk_extract_v13.py, cd_common_v13.py, gl_fast_v13.py}`, `revision_v13\work\CD_capture\CASES_C_v13.json` (+ `REPLACEMENTS_C_v13.json` if it exists), `revision_v13\LOCK_A10_2.txt`, `revision_v13\LOCK_A10_2c.txt` | small |
| Acceptance test data (old run) | `P\07_fit_runs\archives\p1b_fit_finite_0037\SUMMARY.json` and `x\p1b_fit_finite_0037\capture\fit_finite_0037\{contract.json, evaluation_truth.jsonl, frames.jsonl, scenario_frames.jsonl}`; `revision_v13\work\CD_capture\b7\p1b_fit_finite_0037\` | ≈ 11 MB |
| **Fresh data (only after LOCK_A10_2c)** | per run: `CD_capture\runs\<rid>\LOGS_OK`, `runs\<rid>\<rid>\SUMMARY.json`, `runs\<rid>\<rid>\capture\<case>\{contract.json, evaluation_truth.jsonl, frames.jsonl, scenario_frames.jsonl}`; `CD_capture\b7\<rid>\{b7_detections_v13.jsonl, B7_MANIFEST_v13.json}` | ≈ 11 MB per full-length run → ≤ 1.2 GB |

The trace shows that a B7 job opens no other capture file: the logged `detections.jsonl`, `filter_events.jsonl` and
`filter_algebra.jsonl` are replaced in memory by the re-tracked ones (`trk_arrays_v01.overlay`). The numba-cached helpers of the codex
`vendor\` folder (`fast_overlap`, `fast_hull`) write cache files next to themselves: that folder must be writable, or set
`NUMBA_CACHE_DIR`.

**Python environment.** CPython 3.12 (the laptop venv's 3.12.2) via `uv`, as `tools\calib_pods_v13.py` does, with the laptop venv's
versions (`analysis\out\VENV_FREEZE.txt`) of what a job imports: numpy 2.5.4, numba 0.68.1 (llvmlite 0.50.0), scipy 1.18.1, pandas
2.2.2, matplotlib 3.11.2, opencv-python-headless 4.14.0.94, scikit-learn 1.9.1, pillow 13.0.0, PyYAML 6.0.2, cloudpickle 3.1.2, joblib
1.6.0, tqdm 4.70.1, psutil 7.0.0, cachetools 7.3.0, threadpoolctl 3.8.0 (and their dependencies at the frozen versions: contourpy,
kiwisolver, fonttools, cycler, pyparsing, python-dateutil, pytz, packaging, six, narwhals). pyquaternion, shapely, lap, hydra and
omegaconf come from the library's `shims_v01\` (as on the laptop). `exact_trig` is off on Linux by default; the laptop's correctly rounded
trig exists to match Linux results (README of `shared\trackers` §1), so bit-identity is expected and is checked by the acceptance test.

## 4. Procedure (nothing here has been run; pods are created only on the CD lead's or coordinator's instruction)
1. **Before LOCK_A10_2c:** create one (or two) 32-vCPU pods with `tools\pods_v13.py` (spend-log rows); install the environment (§3);
   upload code and the acceptance data with SHA-256 checks; create the five links in `<pod>/job`; set the environment variables.
2. **Acceptance:** in `<pod>/job`: `V13_P_ROOT=<pod>/P V13_CODEX_ROOT=<pod>/codex python -I -B -X utf8
   <pod>/ARS_TRIAL/revision_v13/work/CD_capture/analysis/x_trk_extract_v13.py --test-old --workers 8 --out-root <pod>/testold`;
   download the 8 arrays and compare them with `analysis\out\testold_b7_arrays_final\` (every key, `np.array_equal`, NaN-equal). Accept
   the pod only if all 8 are identical.
3. **After LOCK_A10_2c:** upload `LOCK_A10_2c.txt` (and `LOCK_A10_2.txt`), the fresh logs and the B7 files (§3), SHA-256 checked. Run
   `x_trk_extract_v13.py --workers 30 --out-root <pod>/arrays [--part i:n]` (pod i of n). Each job writes `<out-root>/B7_<r>_<L>/<rid>.npz`
   and a log line; the run writes `XB7_EXTRACT_c_lead_<stamp>.json` beside the arrays.
4. Download the 840 arrays (≈ 200 KB each, ≈ 170 MB) to `CD_capture\arrays\B7_<r>_<L>\` with SHA-256 checks; delete the pods.
5. On the laptop: `analysis\c_b7_v13.py` → `analysis\out\C_B7_v13.json` (§5), then the second program and the comparison.

## 5. After the arrays: the analysis (`c_b7_v13.py`, laptop)
- Per chain: gridless events for 105 runs and 4 sources, then 20,000 resamples with `gl_fast_v13` (2 numba threads); B7 identity reads
  the 105 runs' logged `detections.jsonl` and B7 files.
- Measured on the 35 old runs (scratch benchmark on package B's stored CV0 arrays, sources F0, E, N, CK3, 2 numba threads, shared
  laptop): gridless events 50 s (236,201 events); numba compile of `gl_fast` 379 s (once per process, `cache=False`); 2,000 resamples
  28.8 s. Scaled linearly to 105 runs and 20,000 resamples: ≈ 150 s + 860 s per chain, **≈ 2.3 h for the 8 chains plus ≈ 6 min of
  compile on the laptop** (the old-run test of `c_b7_v13.py` on one run took 317 s, mostly the compile).
- If that is too slow after the lock, `c_b7_v13.py` can run on the same pod with `NUMBA_NUM_THREADS` = its vCPUs (the resample loop is
  `prange` over resamples; each resample is computed sequentially, so the values do not depend on the thread count). It then also
  needs `arrays\CV0\<rid>.npz` and each run's logged `capture\<case>\detections.jsonl` and `frames.jsonl` (identity check) on the pod.
- Memory of one 10 Hz extraction job (B7_10_0.1 on 0037): peak working set 188 MB (psutil). 30 workers need about 6 GB.
- Variability: the same 10 Hz job took 287 s while the benchmark's numba compile ran beside it (69–131 s in the two test runs), so
  laptop wall times can exceed §2's range when the laptop is busy.

## 7. Cut-in family (added 20 Nov, ~03:45 EST; coordinator 03:35: A10 B7 "both families")
- Jobs: another 840 (105 fresh cut-in runs × the same 8 chains), `x_trk_extract_v13.py --family cutin` → `arrays\B7CI_<r>_<L>\<rid>.npz`;
  analysis `analysis\c_b7ci_v13.py` → `analysis\out\C_B7CI_v13.json` (event window from truth, `CD_DEFINITIONS_TRK_v13.md` §8).
- Cost per job is set by the number of decisions (extract) and detector rows (retrack), as for lead braking. Measured: the (2, 0) chain
  on the 20 old cut-in tuning runs (logged rows; each run 300 assessment decisions and 69 detector frames, the size of 0037) took
  4.3 + 27.6 = 32.0 s per run on average (2 workers; the laptop was less loaded than during the 0037 runs, where the same chain took
  56–63 s; `analysis\out\TESTOLD_B7_v13_ci_extract_*.json`). The 5 and 10 Hz cut-in chains could not be timed (no old cut-in sweeps);
  the lead-braking ratios apply, so a cut-in run costs about what a lead-braking run costs (≈ 460–710 worker-s for 8 chains).
- Laptop: about the same again as lead braking (§2), i.e. both families ≈ 14–21 h wall with 2 workers: **too long for one night on the
  laptop together with the other post-lock work; the pods are the realistic route for both families.**
- Pods: about one more pod-hour (32 vCPU, ≈ $0.9), or the same pods with `--family cutin` after the lead-braking jobs (or a second pod
  in parallel). Upload per cut-in run the same five log files and the B7 file (≈ 1.2 GB more at most). Acceptance test: the lead-braking
  one (§4.2) covers the code path; the cut-in path is the same function with `--family cutin`.
- Analysis on the laptop: one population (the window) per chain, ≈ the same gridless cost as lead braking (§5): ≈ 2.5 h more, or
  ≈ 20 min on a pod.

## 6. For information: Table III re-tracking (package B's, not run by CD)
Measured in the same first test run (before the scope change; arrays bit-identical to package B's stored ones, then retired to
`analysis\out\testold_trk_arrays\superseded_variants_scope_change\`): per run B3 89.7 s, B4 88.1 s, B2 68.1 s, B1_d090 87.3 s,
B1_d098 53.7 s (retrack + extract; the first two include the workers' import time). Five variants × 105 runs ≈ 11 worker-h on this
laptop (≈ 5.6 h wall with 2 workers). The same pod set-up (§3–4) would serve it, with `b_fresh_retrack_v02.py`'s own paths.
</content>
