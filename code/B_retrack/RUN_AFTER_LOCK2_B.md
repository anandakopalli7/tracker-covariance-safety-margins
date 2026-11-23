# Package B after Lock 2: run sheet (fresh lead-braking runs; frozen code only)

Written 20 Nov 2026 (laptop clock ~03:25 EST), before FREEZE_B_add3. Every command runs code listed in the freeze manifests; nothing
here is edited after the freeze. Working folder: `revision_v13\work\B_retrack`. "sys" = `python -I -B -X utf8` (system Python, tracker
stack); "venv" = `.venv\Scripts\python.exe -I -B -X utf8` (numpy 2.5.4, numba 0.68.1).

Gates (coordinator, 20 Nov): from `..\..\LOCK_A10_2.txt` B may write arrays only (re-tracking, delayed-stop clearances) and run the
five-run second-IMM check (pass/fail and covariance differences only); **no fresh value of B before `..\..\LOCK_A10_2c.txt`** (Table
III statistics, B6). Laptop: at most 2 workers for B until CD's core extraction and F's val run are done. No pod.

| # | When | Command | Output |
|---|---|---|---|
| 0 | after FREEZE_B_add3, `LOCK_A10_2.txt` exists, CD reports LOGS_OK for the five picked runs | sys `code\imm_compare_v01.py ..\shared\trackers\trk_constants_v01.json 0.95 out\imm2\IMM_COMPARE_fresh5_v01.json <5 capture dirs>` (ids in STATUS.md; capture dir = `..\CD_capture\runs\<rid>\<rid>\capture\<case>`); then sys `code\b_summary_v01.py`. Read nothing else from those logs. | `out\imm2\IMM_COMPARE_fresh5_v01.json`; summary `second_imm_fresh` |
| 1 | from LOCK_A10_2, as CD's logs arrive | sys `code\b_fresh_retrack_v02.py --workers 2` (re-run until every job is ok or exists; skips runs without LOGS_OK) | `out\retrack_fresh\<B3,B4,B2,B1_d090,B1_d098>\<rid>_arrays.npz` |
| 2 | from LOCK_A10_2, after 1 and after CD's `arrays\CV0\<rid>.npz` exist for all 105 runs (2 workers in all) | sys `code\b_fresh_b6_v02.py clear --workers 2` (delayed-stop clearances judged until the stop ends; arrays only) | `out\fresh_b6\clear\<rid>.npz` |
| 3 | from LOCK_A10_2c, after 1 and CD's `arrays\CV0`, `arrays\B1` | venv `code\b_fresh_analysis_v02.py <x> --threads 2` for x in CV0, B3, B4, B1, B2, B1_d090, B1_d098 | `out\fresh\B_FRESH_<x>_v02.json`, `boot_<x>.npz` |
| 4 | from LOCK_A10_2c, after 2 and CD's `arrays\RSX\<rid>.npz` (stage 2) | venv `code\b_fresh_b6_v02.py score --threads 2` | `out\fresh_b6\B6_FRESH_v02.json`, `boot_b6.npz` |
| 5 | (TU is old data: `out\tu\TU_v02.json`, computed before the freeze by `code\b_tu_v02.py`) | — | — |
| 6 | after 3, 4 | sys `code\b_fresh_export_v02.py` | `out\A_EXPORT_B.json`, `A_EXPORT_B_meta.json` |
| 7 | from LOCK_A10_2c, after 1, 2 and CD's RSX (independent of 3–6) | second program, one variant at a time (memory): `recount_fresh\README_recount_fresh.md` (`recount_fresh.py --fresh --variants <v>`, `--fresh --b6`, `--tu`, then `--fresh --combine`) | `out\A_RECOUNT_B.json`, `recount_fresh\out\boot_*.npz` |
| 8 | after 6, 7 | sys `code\b_fresh_compare_v02.py` | `out\compare\B_FRESH_COMPARE_v02.json/.md` |
| 9 | after 8 | STATUS.md, message A and the coordinator | — |

Rules: every value script checks both lock files; a disagreement in step 8 is handled by A10 §10.1(c) (cause found, fixed, recorded);
any code change after the freeze needs the coordinator's OK.
