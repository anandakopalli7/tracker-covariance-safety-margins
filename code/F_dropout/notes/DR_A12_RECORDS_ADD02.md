# DR on the new runs (A12 §3a): record ADD02, after LOCK_A12a; second program only

Session F (Claude Opus 5.5), 22 Nov 2026, about 03:12 EST by this laptop's clock.

## B2. The recount's run-id prefix (dr_recount_a12_v02.py; FREEZE_DR_A12_ADD02)

- **What failed:** the frozen second program `recount\dr_recount_a12_v01.py` (Claude Sonnet 5.5; sha c80d1ffc…), started on the 150 new
  runs at about 03:07, logged "masks identical at p010: False" with "case_id differs from the run id" for every run.
  - Its `case_of_run` maps only A11's fresh-run prefix (`pc13_<case>_native`). The new runs are `pl12_<case>_native`, so it returned
    None, and the comparison of each run's case id in the mask file with the run id failed.
  - The masks themselves passed every other check in that log (the masks regenerated from the case ids equal `meta.masked` and the mask
    file). The case ids F used are CD's: `CD_capture\l12\CASES_L12_v13.json` maps job `pl12_<case>_native` to `<case>` for all 165 jobs
    (checked), as A12 §3a.1 ("each run's protocol case id is its seed id").
  - Without the fix, the recount's `DR.masks_identical` and `DR.masks_identical_all` would read False while F's read True.
- **Fix, by the second program's author (the same Sonnet agent), not by F:** `dr_recount_a12_v02.py` = v01 with `case_of_run` also
  mapping `pl12_<case>_native` to `<case>`, plus one docstring line. Nothing else changed (diff checked by F: 2 hunks, 6 lines).
  v01 is unchanged.
- **Run:** the v01 run was stopped after about 2 min (no value kept), and v02 started on pod `claude-v13f-r3` at about 03:10. Its log
  now reads "masks identical at p010: True []". The v01 log is kept on the pod as `recount_a12_v01_stopped.log`.
- **Frozen:** `work\locks\FREEZE_DR_A12_ADD02.json` (layered on FREEZE_DR, FREEZE_DR_A12 and FREEZE_DR_A12_ADD01) records
  `dr_recount_a12_v02.py` and this note.

## Other facts of the run, for the ledger (no decision depends on them)

- P̄_DR at p = 0.10 recomputed on the pod is IDENTICAL to A11's `out\PBAR_DR_v01.json` (max abs diff 0.0; counts equal).
- Identity check (i), A10 B0(b): passed. All 150 runs agree on every read key; the largest differences are 2.8e-14 (cA1, cQ on 44
  runs), inside 1e-12. Check (ii): 201 of 29,926 decisions change with punish_num = 3 and no mask.
- The recount runs on a 3-GPU pod (`claude-v13f-r3`) only for its CPU quota (20.4 CPUs); its double bootstrap cannot be split over pods.
