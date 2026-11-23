# AMENDMENT_13 §3: records after LOCK_A13b (continues DR_A13_RECORDS_v01.md, which is frozen in FREEZE_DR_A13_ADD01)

Session F (Claude Opus 5.5), 22 Nov 2026, about 06:50 EST by this laptop's clock. The laptop clock was corrected during the night;
earlier stamps in this folder read about one hour later.

## R7. Crossed messages: the lock fixes v01

- **What crossed:**
  - The coordinator asked for the coast-count version v02 (message stamped 06:39).
  - It then wrote LOCK_A13b at 06:40:47 (c85f39c3…). The lock fixes §3 v01, the two-population flag F0_flag, and states that the
    coast-count version is not adopted, because the code-test values were known.
  - F, working from the 06:39 message, froze v02 at about 06:46 as FREEZE_DR_A13_ADD01 (f1a60d84…), after the lock.
- **Consequence:** ADD01 and v02 are not part of the locked design and are not run. They stay on disk as a record.
- **The locked second program:** the Sonnet program from the v01 text (`recount\dr_recount_a13_flag_v01.py`) and its code test are
  frozen in FREEZE_DR_A13_ADD02 (42d84e95…). That name is used because ADD01 was taken. Both programs' v01 code tests agree on all 23
  keys, DRF.delta.p included.
- **Ties:** the v01 text counts Δ\* ≤ 0. If the real run's counts differ only at ties within round-off, both counts and the tie count
  will be reported. Nothing is changed.
- **Gate:** no real run starts before the coordinator confirms.

## R8. LOCK_A13c adopts v02; the run and the result

- **The lock:** the coordinator then wrote LOCK_A13c (06:48:18, 67088c15…). It supersedes LOCK_A13b's §3 before any real value and
  adopts v02 (F0_coast primary, F0_flag2 descriptive). The chain runs through FREEZE_DR_A13_ADD01 (121 files). FREEZE_DR_A13_ADD02 (the
  v01 Sonnet program) is not used.
- **Lock checks:** `dr_flag_v02.py` checks only that `LOCK_A13b.txt` exists, which it does. The governing lock is LOCK_A13c (the
  coordinator's 06:49 instruction). The second program was run with DR_LOCK set to LOCK_A13c. No v01 program was run on real data.
- **First program:** `dr_flag_v02.py` → `out_a13\DRF_RESULTS_v02.json` (dd3948a4…), 168 s.
- **Second program:** `dr_recount_a13_flag_v02.py` with DR_LOCK = LOCK_A13c → `recount\DRF_RECOUNT_v02.json` (76d11dfc…), 141 s.
  - F's first launch used the system Python without numba (pure-Python fallback). It was stopped at its k step with no output
    written; its log is kept as `logs\drf_recount_real_v02_nonumba_stopped.log`. It was rerun with the venv Python (numba 0.68.1).
- **Agreement:** all 41 keys, max 5.6e-17 (`out_a13\DRF_COMPARE_v02.json`).
- **Exports:** `F_nuscenes\out\A_EXPORT_DRF.json` (06aa86d8…) and `A_RECOUNT_DRF.json` (7615053b…), agreeing on all 41 keys.
- **Result: FAILED (amendment).**
  - Δ = −0.0024, 95% [−0.0057, −0.00013], within the equivalence margin.
  - p_F = 0.986, from 19,711 resamples ≤ 1e-12 (2 ties).
  - RR_N 0.0298 (equal to DR2's r), RR_coast 0.0322.
