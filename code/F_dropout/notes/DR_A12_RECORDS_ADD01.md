# DR on the new runs (A12 §3a): record ADD01, after LOCK_A12a and before any new-run DR value

Session F (Claude Opus 5.5), 22 Nov 2026, about 02:35 EST by this laptop's clock.

## B1. A path bug in dr_extract_v02's P̄ branch; one-line fix (FREEZE_DR_A12_ADD01)

- **What failed:** the first post-lock chain on pod `claude-v13f-a2` (07:31 UTC = 02:31 EST) stopped at its first P̄ step.
  - `dr_extract_v02.main` builds the tuning runs' masks from each run's detector-row count, and it took the capture folder straight from
    P's run index, a Windows absolute path.
  - On the pod that path does not exist (FileNotFoundError), so no P̄, mask file or array was written.
  - The tracking step itself (`one` → `run_paths`) already maps the same path through `p_local`. The A11 code (`dr_extract_v01`) read
    the tuning masks from the pre-written DR_MASKS_v02.json and never had this step.
  - The pre-lock pod test ran on the old fit runs (`--test-old`), whose paths go through `run_paths`, so it did not reach this line.
- **Fix:** `caps = {r: p_local(tr[r][1]) ...}`, the same mapping as `run_paths`. Nothing else changed. The masks, the law, the P̄ rule and
  every numeric step are unchanged, and the files read are the same files.
- **Also in that chain:** the new runs' logs were not yet on the pod (the upload's first SSH call hung for 30 min and timed out), so the
  identity and dr steps refused ("0 of the 150 new runs have logs"). The chain produced no value. It is restarted after the upload.
- **Frozen:** `work\locks\FREEZE_DR_A12_ADD01.json` (layered on FREEZE_DR and FREEZE_DR_A12) records the fixed `dr_extract_v02.py` and
  this note.
