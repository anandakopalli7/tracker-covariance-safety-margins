# DR on the new runs (A12 §3a): run log after LOCK_A12a (not frozen; appended as the runs go)

Session F (Claude Opus 5.5), 22 Nov 2026, EST by this laptop's clock (pod clock is UTC).

## 1. Second restart failed on a staging slip (02:49–02:51); third start 02:52:44

- **What happened:** the code bundle for the second start was built at 02:32:40, a few minutes before the ADD01 fix (02:35). The pod
  therefore ran the pre-fix `dr_extract_v02.py` (pod SHA 9e14318e…; fixed and frozen SHA 1a59c338…, FREEZE_DR_A12_ADD01).
  - The P̄ steps failed exactly as in B1 (Windows path); combine and dr then failed for lack of P̄ (150 errors per p).
  - id0 and id3 (no mask) completed with 0 errors. No P̄, DR array, analysis or dose value was computed.
- **Fix:** the frozen `dr_extract_v02.py` (1a59c338…) uploaded alone; every code file on the pod compared with the laptop by SHA-256 (all
  equal; the four absent files are laptop-only launchers and the §3d test script).
- **Outputs of the failed start** moved aside on the pod to `F_dropout/failed_0750/` (out_a12 and the log); nothing from them is used.
- **Third start** at 02:52:44 with a clean `out_a12`, the same script (`dr_pod_a12_postlock_v01.sh`).

## 2. Calibration start slip (03:02–03:17) and pods

- The first calibration starts (03:02–03:10, `dr_pods_v03.py run` from Git Bash) died at once: Git Bash rewrote the pod paths
  (`/root/dr/...`) given to the Windows python into `C:/Program Files/Git/root/dr/...`. Nothing ran and no value was computed.
- Restarted 03:17 with path conversion off (MSYS_NO_PATHCONV=1). Each job reproduced its full-sample value first
  (dr_main: all 4 statistics; slope 0.15217106012649576):
  - dr_main seed 20261913 on a3;
  - the slope seed 20261913 in two outer chunks, 0:1000 on a2 and 1000:2000 on a4.
- Pod a5 was created at 03:01 but got no SSH endpoint within 16 min. It was deleted at 03:18 (rc = 0, gone from the list) and never used.
- The recount runs on r3 (3 × 4090, CPU quota 20.4): v01 03:07, stopped; v02 from 03:10 (record B2).

## 3. §3d launcher written after LOCK_A12d (03:40)

- `code\dr_pod_hz10_postlock_v01.sh` only starts the frozen 10 Hz programs (FREEZE_DR_A12_ADD03) in §3d's order:
  - the arrays: id0, id3, dr;
  - the analysis with the calibration exported;
  - the calibration's first inner seed.
- It runs on a2 after a2's slope chunk, so the 2 Hz work is never delayed. LOCK_A12d (eb4b6326…) is on a2, SHA checked.

## 4. Recount v02, first run died silently (r3); rerun 03:56

- Run 1 (`--threads 20`, from 03:10) finished the dr_main double bootstrap (seed 20261913, 2,000 outer) at about 03:25. The process then
  disappeared: no traceback in the log, no output file, no out-of-memory event (cgroup peak 2.4 GB, failcnt 0, oom_kill 0). Most likely
  a native crash in the threaded code at the next step. No value was written; its log is kept on the pod as
  `recount_a12_v02_run1_died.log`.
- Run 2 from 03:56: the same frozen program (v02, sha 337d0fc2…) with `--threads 13`, the setting under which this code path ran to
  completion twice (A11's full recount; A12's pre-lock test). It runs with `python -X faulthandler`, and its exit code is logged.

## 5. Cause of the recount crashes: OpenBLAS's forced Haswell kernel on r3's CPU (04:18)

- Run 2 (13 threads, 03:56) also died at the same point, after the dr_main double bootstrap: "Segmentation fault (core dumped)",
  exit 139, at 04:14.
- The step after the double bootstrap is the first large matrix product (calib_one: (2000 × 2000) @ (2000 × 91)).
- Reproduced on r3 with two lines of numpy and no project code (the same product of random integer matrices):
  - `OPENBLAS_CORETYPE=Haswell` crashes at 1 and at 13 BLAS threads;
  - with no override, or with SkylakeX, it runs.
  - r3's CPU is an AMD Ryzen 9 7950X (Zen 4, AVX-512); OpenBLAS 0.3.34 (scipy-openblas64, DYNAMIC_ARCH).
- The override comes from CD's environment of record. It ran cleanly on the other pods' CPUs, which ran F's calibration and imports.
- Run 3 (04:18): the same frozen program and inputs, with `OPENBLAS_CORETYPE` unset (OpenBLAS picks the native kernel), 1 BLAS thread,
  20 numba threads.
  - The product it crashed in is an exact integer count. A kernel choice can change only last bits elsewhere, inside the comparison's
    1e-9.
- A bounds-check diagnostic run (NUMBA_BOUNDSCHECK=1) was stopped once the cause was found; it wrote no output.

## 6. §3d (10 Hz) after LOCK_A12d

- **Chain on a2, 04:01–04:36:** id0, id3 and dr arrays at 10 Hz, 150/150 runs, 0 errors; analysis export; calibration seed 20261913
  (1,794 s).
- **Coverage of the nominal 95% interval:**
  - R_gl 0.9505, c − c_p 0.9505, r 0.9510;
  - c 0.9390, below 0.94, so the second inner seed (20261914) runs, as A10 §2.6 asks. Started on a2 at 04:37.
- **Identity:**
  - (i) passed: 150 runs, every read key; max 2.8e-14, on cA1 and cQ (44 runs);
  - (ii) 644 of 29,926 decisions change with punish_num 15 and no mask (`out_a12\DR10_IDENTITY_v01.json`).
- **The 10 Hz second program** (`dr_recount_a12_hz10_v01.py`, frozen in ADD03) runs on a new pod, a6. r3 stays on the 2 Hz recount
  (priority). The run has no OpenBLAS core-type override (see §5) and uses 1 BLAS thread.
- **Local copy of the arrays:** `pods_dr_a12\hz10_arrays.tgz`, 710c9dfb…. A first extraction used the wrong strip depth; the files were
  moved into `out_a12\hz10\` unchanged and the stray folder was removed.
