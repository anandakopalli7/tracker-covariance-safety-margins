# FREEZE_B_add11: what changed since add10 and why (22 Nov 2026, about 00:48 EST, package B)

`work\locks\FREEZE_B_add11.json`, SHA-256 `c5ae85ea837301fd8b42996f7a82c9dd98652932551e16db6a3eb9c821ac5901`. It is layered on FREEZE_B and add1–add10: 4 files changed, 2 new, 0 missing, library unchanged.

## Why

At about 00:44 EST, session CD described its layout of the new runs:
- A run's logs are in `CD_capture\runs\<rid>\`.
- `<rid>` is the capture run id. For a run captured on an allowed retry it differs from the job id (suffix `__p1` or `__r1`).
- `CD_capture\l12\out\L12_RUNS_v13.json` maps each job id to its rid. CD writes it when the runs are down.

add10's code assumed rid = job id, which is wrong for retried runs.

## Changes, all on the new-run path only

| File | Old SHA (add10) | New SHA (add11) | Change |
|---|---|---|---|
| `code\b_l12_ids_v02.py` (new) | — | `03f7f9fa…` | v01 plus the job → rid map (REFUSED while the map is missing). `capture_dir` and `logs_ok` resolve through it. `markers <folder>` writes job-named LOGS_OK markers for the frozen second programs. `l12_run_ids` is unchanged. |
| `code\b_imm2_v01.py` | `1fb4857e…` | `a4e05c78…` | The new-run branch imports v02. With a runs root (new runs only), `job_fresh` takes `rd, cap` from `L12.capture_dir(root, job)`. With no root (pbar, combine, C runs), the lines are the same as before. |
| `code\b_l12_retrack_v01.py` | `b8b5776a…` | `500635cb…` | The import becomes `b_l12_ids_v02`; the docstring sentence is updated. |
| `code\b_fresh_analysis_v04.py` | `9ec76638…` | `4ee93bac…` | `--set new` imports `b_l12_ids_v02`; the docstring wording is updated. |
| `code\b_modeprob_v01.py` | `1ddeb09f…` | `5c6b28b1…` | Mode `new` imports `b_l12_ids_v02`; the docstring wording is updated. |
| `pods\b_recount_pod_v04.py` (new) | — | `6621f3b9…` | The IMM2 recount on a CPU pod, adapted from v03. Stage `new` uses `b_l12_ids_v02`. |

The frozen Sonnet second programs, `recount_fresh\imm2_v04.py` and `modeprob2_v01.py`, are unchanged. They test `<runs root>\<job id>\LOGS_OK`, so B gives them the marker folder written by `b_l12_ids_v02.py markers`, which yields the same set as B's first programs.

## Tests re-run on the changed files (old runs only)

- **Analysis** (00:47–00:48): `b_fresh_analysis_v04.py B1 --test-old` gives 89 of 89 values identical to v01. Points, intervals and the 2,000 resample rows are identical to add10's test.
- **Mode probabilities** (00:47): `b_modeprob_v01.py B1old ...\retrack\B1 old` is identical to add10's test, and agrees 21 of 21 with the second program (`b_imm2_checks_v01.py modeprob B1old old`).
- **Map reader:** `b_l12_ids_v02.job_map` was tested on three synthetic map shapes in a temporary folder: a plain dict, `{"runs": …}`, and a list of `{job, rid}`.
- **Retracking code:** `b_imm2_v01` and `b_l12_retrack_v01` cannot be tested without new runs. Their C-run and tuning-run paths are unchanged, and P̄_IMM2 was computed before the change.

No value of any run was computed under add10's versions of these files.
