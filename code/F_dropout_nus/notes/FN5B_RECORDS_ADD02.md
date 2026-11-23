# AMENDMENT_12 §5b: record of the stop at the tracker-independent check and the approved change (ADD02)

Written 22 Nov 2026, about 04:00 EST by the laptop clock, by the package F worker (Claude Opus 5.5). It was written before any masked value existed and before the GO for the remaining steps.

## 1. What stopped
- **The run.** `code\fn_run_masked_v01.sh` ran once on pod claude-v13f-n03 (id `384so6f6ekg1m1`, AMD Ryzen 9 7950X, CPU quota 6.8). It started at 03:43:17 EST, after LOCK_A12c (`f289eea7…1bce`) and LOCK_A12e (`913807a6…a9a4`) existed and their SHA-256 had been checked on the pod.
- **Done:** masked tracking of 150/150 scenes (08:43:14–08:44:44 UTC) and masked arrays of 150/150 scenes (to 08:49:28 UTC).
- **Stopped:** `fn06_score_v01.py prep` stopped in `load_runs` at the pre-registered check, `RuntimeError: tracker-independent keys of scene-0966 differ from F's arrays`.
- **Nothing scored.** No partial result, single bootstrap, calibration or `FN5B_RESULTS` was written, and `out\masked_val\` on the pod was empty. **No masked value existed.**
- **Kept.** The masked tracks and arrays (150 + 150 files) and the logs were fetched, every file SHA-256 checked (`pods\claude-v13f-n03\FN_FETCH_*.json`).
- **Pod deleted** at 03:53:42 (rc = 0, the id gone from the list).

## 2. Diagnosis
- **Method.** `post\fn_diag_indep_v01.py` reads only the tracker-independent keys that the check reads; it reads no critical scale and no outcome. Output: `post\DIAG_INDEP_v01.json`, SHA-256 `420c76c0d2b0a02470ff92e694f15715fd3b97bc0663dc76c10ab1fda689ab40`.
- **What differs.** Across all 150 scenes, exactly one difference exceeds 1e-9: scene-0966, decision 151 (sweep 376, keyframe 38, now 18.800848 s). There, rows 6 and 7 are swapped:
  - vbar: 8.6909 and 6.2809 in F's arrays; 6.2809 and 8.6909 in the masked arrays;
  - targets: (0, +2) and (0, −2), swapped.
- **Cause.** At this decision v0 equals the scene's desired speed (7.48589…), so the two rows tie in the planner's cost order. The tie was broken by a last-bit difference in v0 (2.5e-14) and a_raw (2.8e-14) between the laptop and this pod's CPU.
  - The acceptance pod, claude-v13f-n01, broke the tie as the laptop does. Its accept arrays matched F's within 9.0e-13 on vbar (`out\ACCEPT2_ARRAYS_v01.json`).
- **Not scored.** Decision 151 is not evaluated (`evaluated` is False in both files) and its clearance is NaN on both sides, so it is in no scored population.
- **Everything else passes:**
  - the exact keys (`sweep`, `kf`, `now`, `age`, `idx55`, `evaluated`, `evaluated2`, `inpath`, `n_truth`) are identical in all 150 scenes;
  - the float keys are within 1e-9 at every evaluated decision;
  - the masks match the law.
- **Independent check.** The coordinator checked all 150 scenes independently and found the same: exact keys identical everywhere, floats within 1e-9 at every evaluated decision, and the one difference is scene-0966's vbar at decision 151, not evaluated.

## 3. The change
- **New file.** `code\fn06_score_v02.py` is `fn06_score_v01.py` with one change, plus one docstring line that records it. `fn06_score_v01.py` is untouched.
- **What changed.** The float part of the tracker-independent check (`vbar`, `v0`, `des`, `clear`, `clear2` within 1e-9, NaN patterns) now applies to evaluated decisions only.
- **What did not change.** The exact-key check stays on all decisions. Everything else is unchanged: the scoring, the seeds, the sizes, the sequence, the outputs and their names.
- **Why it is safe.** Only evaluated decisions are scored, and only their F clearances (`clear_v02`) are read.
- **Diff.** `post\fn06_v01_to_v02.diff`.
- **Check of v02 before any value.** v02's `load_runs` was run on the laptop on the fetched masked arrays. It computes no statistic. Result: 150/150 scenes pass, masks identical to the law, decision ticks match. The largest float differences at evaluated decisions are vbar 3.2e-13, v0 8.0e-14, des 1.3e-13, clear 8.8e-13 and clear2 8.2e-13.

## 4. Approval
- **Option (a) approved.** The coordinator approved it after LOCK_A12e at 03:57 EST, before any masked value, with these conditions:
  - freeze first (`work\locks\FREEZE_F_NUS5B_ADD02.json`) and verify;
  - no scoring before the coordinator's GO.

## 5. Remaining steps after the GO (once)
- **Runner.** `post\fn_post_v02.py` drives the steps; `code\fn_run_score_v02.sh` runs them on the pod.
- **Order:**
  1. **preflight:** FREEZE_F_NUS5B and FREEZE_F_NUS5B_ADD02 entries, both locks, and the fetched masked files against their fetch SHA-256;
  2. **up:** a new pod (spend-log row, 3 h watchdog, both environments), then the code, val, masked and score2 bundles, each SHA-checked on the pod;
  3. **gate-test:** with no lock on the pod, both `fn06_score_v02.py prep masked val` and the runner must REFUSE, and no scoring file may exist afterwards;
  4. **locks:** upload LOCK_A12c and LOCK_A12e, SHA-checked;
  5. **start:** once. The runner does prep → calib with seed 20261913 → finish, and calib with seed 20261914 only if finish asks for it;
  6. **fetch:** `out\masked_val` and `logs`, SHA-checked;
  7. **delete the pod:** confirmed (rc = 0 and the id gone);
  8. **values:** `out\FN5B_VALUES_v01.json`.
- **Nothing is re-tracked or rebuilt.**
