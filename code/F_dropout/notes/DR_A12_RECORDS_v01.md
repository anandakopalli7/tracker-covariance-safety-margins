# DR on the new runs (AMENDMENT_12 §3a): records before LOCK_A12a

Session F (Claude Opus 5.5), 22 Nov 2026, EST by this laptop's clock. Frozen in `work\locks\FREEZE_DR_A12.json`.

## A1. The masks at different p are not nested (text v01 → v02)

§3a v01 said that the masks at different p differ only through u < p. That is wrong. Once one p starts a window where another does
not, the L draw and the gap shift the two draw sequences apart. Example: case c1109_eval_1110 with 69 rows has 14 masked frames at
p = 0.05 and 10 at p = 0.10. The law itself was never in question, and at p = 0.10 it is A11 §6c's exactly (`dr_masks_v03 check02`:
225 of 225 runs). §3a v02 (`ca5f058c…bfa0`) states it correctly. Found while testing, before any new-run value.

## A2. Pre-lock pod test on the 35 old lead-braking fit runs (exploratory data of record)

Pod `claude-v13f-a1`, 22 Nov 00:23–00:42:
- `dr_pod_a12_test_v01.sh`: per p, masked P̄, combine and arrays; DR0–DR2 at p = 0.10 with calib_remote (100 × 1,000); the dose
  export, the slope's remote double bootstrap (100 × 1,000; 103 s per seed for 35 runs) and the import.
- `dr_pod_a12_test2_v01.sh`: the dose step rerun with the final `dr_dose_v01.py`, which adds `DR.masks_identical_all`. The remote slope
  results were reused, and their full-sample value was checked on import.
- The second program `recount\dr_recount_a12_v01.py` ran on the same test set.

Comparison (`out_a12\DR2_COMPARE_TESTOLD_v01.json`): all 111 shared value keys agree. The largest difference is 7.96e−13, and the
levels and verdicts are equal. The one key only the second program writes, `DR.dec.r.ci`, is allowed: it is an interval the
first program does not export. The strict key-set report is kept in `logs\DR2_COMPARE_TESTOLD_v01_strict_keys.json`.

Aligned before the test, both from the second program's reported ambiguities:
- `DR.masks_identical` is the p = 0.10 check, and `DR.masks_identical_all` covers all four p.
- The Monte Carlo convention of A10 §2.6 is CD's: in each MC resample, the smallest level with coverage ≥ 0.95, or 1.0 if none, with
  validity applied inside the resample.

## A3. Cost plan of the slope's calibration

At full size (2,000 × 1,000 on about 150 runs) the slope's double bootstrap takes about 2.5 h per seed on one 13-thread pod. It is
split into outer chunks (`dr_slope_remote_v01.py --outer A:B`, then `merge`) over several pods, about $2 per seed. The second seed is
run only if a statistic's coverage at the nominal 95% is below 0.94.

## A4. CD's folder map and the identity check on the new runs (before LOCK_A12a)

CD (22 Nov, about 00:45) gave the layout of the new runs. A run captured on an allowed retry has a suffixed folder id (__p1 / __r1),
and CD maps job ids to folders in `CD_capture\l12\out\L12_RUNS_v13.json`. CD's CV0 arrays are in `CD_capture\arrays_l12\CV0\<job id>.npz`.
- `dr_extract_v02.py` now reads the map: `l12_map`, used by `cap_of`. Without the map it uses the job id.
- `dr_pods_v02.py` stages the map and `arrays_l12`.
- New: `dr_identity_v02.py`, the A12 copy of `dr_identity_v01.py` with only the run set and folders changed.
FREEZE_DR_A12 was re-issued with these files. The first issue (00:43, 266814fc…a3a8) is kept as
`logs\FREEZE_DR_A12_first_issue_0043.json`. No lock referenced it.
