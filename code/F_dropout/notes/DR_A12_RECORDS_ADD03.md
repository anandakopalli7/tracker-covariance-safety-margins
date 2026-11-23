# DR at 10 Hz (A12 §3d): record ADD03, before LOCK_A12d and before any new-run 10 Hz value

Session F (Claude Opus 5.5), 22 Nov 2026, about 03:25 EST by this laptop's clock.

## C1. Pre-lock test on the pod (old run 0037 only; exploratory data)

- Pod `claude-v13f-a2`, 07:54 UTC (02:54 EST), `dr_pod_hz10_test_v01.sh`: id0, id3 and dr on `p1b_fit_finite_0037` (the one old run with
  B7 10 Hz rows), 0 errors each; then the analysis code path (`dr_analysis_v03.py --test-old --no-calib --nboot 2000`), which wrote
  `out_a12\testold_hz10\TESTOLD_DR10_RESULTS_v01.json`.
- Identity of the configuration of record at 10 Hz: F's id0 array of 0037 against CD's accepted `B7_10_0.1` test array
  (`CD_capture\analysis\out\testold_b7_arrays_final\B7_10_0.1\p1b_fit_finite_0037.npz`), A10 B0(b): passed. The key sets are equal
  (45 keys); the largest differences are 7.1e-15 (cA1, cQ). Script `code\dr_identity_hz10test_v01.py`.

## C2. The second program at 10 Hz (§3d.7)

- `recount\dr_recount_a12_hz10_v01.py` (sha 11e8368f…), written by the second program's author (Claude Sonnet 5.5) from the §3d text and its
  own `dr_recount_a12_v02.py`, without reading F's code.
- Its test on the same run (`--test-old --quick`) against F's test: all 66 keys agree, max abs diff 2.1e-14
  (`out_a12\DR10_COMPARE_TESTOLD_v01.json`). One run, so the bootstrap is degenerate: a code test only.

## C3. Readings fixed before the lock (both programs already read them the same way)

1. **The gap population of the descriptives** (A11 §6c's "in-dropout plus gap row"): at 10 Hz it is the decisions whose frame is the
   FIRST row after a window (0.1 s). The five rows after a window are the law's no-draw interval (§3d.2); they are not all a "gap row"
   in the descriptives. Both programs use the arrays' `dr_gap` flag (first row only). Descriptive only; no hypothesis uses it.
2. **ref3** (the no-mask reference) is ID3 at 10 Hz: punish_num = 15 and no mask.
3. **DR.pbar.*** reports the 2 Hz P̄_DR used as F0 (§3d.4), not a 10 Hz P̄.
4. **In-dropout age** goes up to 15 rows at 10 Hz (16 bins).

## C4. Frozen in `work\locks\FREEZE_DR_A12_ADD03.json` (layered on FREEZE_DR, FREEZE_DR_A12, _ADD01, _ADD02)

- Text: `A12_3d_DR_10HZ_v01.md`.
- Code: `dr_extract_v03.py`, `dr_analysis_v03.py`, `dr_identity_v03.py`, `dr_pods_v03.py`, `dr_pod_hz10_test_v01.sh`, `dr_masks_v04.py`, and
  `dr_identity_hz10test_v01.py`.
- Export and merge: `dr_export_v02.py` (DR2) and `dr_export_v03.py` (DR10), pure renamings; `dr_merge_first_v01.py`.
- Second program: `dr_recount_a12_hz10_v01.py` and its test output.
- Test outputs: F's test results and the comparison.
- This note.
