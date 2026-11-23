# Packages C and D: steps after Lock 2 (written 19 Nov 2026, revised 20 Nov 02:30 EST; before any fresh value)

All commands from `work\CD_capture`, with `PY = .venv\Scripts\python.exe -I -B -X utf8` and `OPENBLAS_CORETYPE=Haswell`.
Targets (coordinator, 20 Nov 01:10): Lock 2 about 10:30; C and D results with their second-program comparison by 20:00.
The stop rules do not change: A10 §0.5's deadlines are the only cut-offs; nothing is dropped and no check is skipped.
Until package CD's extraction ends, F keeps at most 3 processes on the laptop.

**Two-stage Lock 2 (coordinator, 20 Nov 01:53 EST; recorded as an A10 §11 departure).** Stage 1: `LOCK_A10_2.txt` after FREEZE_CD (this core) and FREEZE_F verify. Stage 2: `LOCK_A10_2c.txt` after FREEZE_CD_2 (the A10 §5.7 additions) and B's FREEZE_B_add3 verify, before 18:00.
- **Between the two locks** only steps 1a and 1 run (the frozen core extractor writes logs and the CV0/B1 arrays). No fresh C or D value is computed, and no person or agent reads any value from those files. Step 1a's `LOGS_OK` files (and B's five runs) may be reported to B as present; B may only read them as the coordinator's rules allow.
- **From `LOCK_A10_2c`:** steps 2–6 here and the stage-2 steps (`RUN_AFTER_LOCK2C.md`, frozen in FREEZE_CD_2: B7 and RSX extraction, the §5.7 programs, the hand check, the exports).
- D2's reaction-and-stop column is not computed by this core (see CD_DEFINITIONS, "Superseded 20 Nov"); it comes from stage 2.

0. **Gate.** `..\..\LOCK_A10_2.txt` exists. `PY make_freeze_cd_v13.py --verify` prints no changed or missing file. `..\locks\FREEZE_B.json` exists. For step 2 onwards, `..\..\LOCK_A10_2c.txt` exists too and `PY make_freeze_cd_v13.py --stage 2 --verify` is clean.
1a. **Logs first** (about 45–60 min; tested 19 Nov on two re-simulated old runs: ~105 s per run under load, no .npy kept): `PY analysis\c_extract_v13.py --set c_lead --logs-only --workers 4`. Package B reads five fresh lead-braking runs (picked by its `default_rng(20261917)`) from `runs\<rid>\` for the A10 §10.1(b) second-IMM check; a run is complete when `runs\<rid>\LOGS_OK` exists. **Tell B at once** (one line) when all 105 have `LOGS_OK`.
1. **Arrays** (laptop, in this order; runs whose `LOGS_OK` exists are not extracted again):
   - `PY analysis\c_extract_v13.py --set c_lead --variants CV0,B1 --workers 5`
   - `PY analysis\c_extract_v13.py --set c_cutin --variants CV0 --workers 5`
   - `PY analysis\c_extract_v13.py --set d1 --variants CV0 --workers 5`

   Logs go to `runs\<rid>\` (sweeps excluded); arrays to `arrays\<variant>\<rid>.npz`.
2. **Exports**, each as soon as its arrays exist (lead first):
   - first program: `PY analysis\c_lead_v13.py --calib export` → `analysis\out\C_LEAD_H0_H5_v13_PENDING_CALIB.json` and `analysis\out\calib\lead_{main,imm,h4}.{job.npz,meta.json}`; `PY analysis\c_cutin_v13.py --calib export` → `cutin_window` (and `cutin_young` when evaluable);
   - second program (recount): its export commands from `recount\README_RECOUNT_C.md` ("Pod path"); labels start with `rc_`. Its main bootstrap runs on the laptop (about 1–2 h for lead at 105 runs); start it while the first program's chunks run on the pods.
3. **Double bootstraps (A10 §2.6) on pods**, `tools\calib_pods_v13.py` (`RUN = pods\calib_run`); tested 20 Nov 01:18–01:37 on one pod with old-run jobs (pod rows equal the laptop's bit for bit; chunked = unsplit):
   - `PY tools\calib_pods_v13.py plan --jobdir analysis\out\calib --labels lead_main,lead_imm,lead_h4` (chunks of 20 outer samples for gridless jobs, 200 for H4; both inner seeds);
   - `PY tools\calib_pods_v13.py up claude-v13cd-k01 claude-v13cd-k02 claude-v13cd-k03 --deadline-h 6` (RTX 4090, EU-RO-1; each pod: CPython 3.12 + numpy 2.5.4 + numba 0.68.1 via uv, all files SHA-256-checked after upload, one single-threaded worker per vCPU); start a session-tracked backstop that deletes any `claude-v13cd-k*` pod after 6 h;
   - `PY tools\calib_pods_v13.py assign`, then `PY tools\calib_pods_v13.py loop` in the background (fetch every 5 min with SHA-256 check, move queued tasks to idle pods, requeue a failed task once);
   - each later export: `plan` its labels (recount: `--runner rc_calib_remote_v13.py --code <its modules> --chunk N`), `up` the live pods again (uploads the new jobs; nothing else is redone), `assign`. More pods may be added with `up` + `assign` (one pod per label is allowed). After the last label: `final` (the loop then deletes each pod once its chunk files are on the laptop).
   - Spend: every create and delete is in `..\SPEND_LOG_v13.csv`. Budget $22 left of my $70; ask the coordinator before going above.
   - Expected (from the dry run, 4.5 s per outer sample per vCPU at 35 runs): the first program's gridless labels ~15 vCPU-h each at 105 runs; three or four 32-vCPU pods finish them in about an hour.
4. **Join and finalize**:
   - first program: `PY tools\calib_merge_v13.py pods\calib_run\chunks analysis\out\calib lead_main lead_imm lead_h4 cutin_window [cutin_young]` (checks tiling, full-sample identity and the job's values), then `PY analysis\c_lead_v13.py --calib import` → `analysis\out\C_LEAD_H0_H5_v13.json` and `PY analysis\c_cutin_v13.py --calib import` → `C_CUTIN_K0_K2_v13.json`;
   - recount: its import commands with `--calib-chunks pods\calib_run\chunks` (it merges its own chunks);
   - D needs no double bootstrap; run it as soon as the D1 and lead arrays exist: `PY analysis\d_nonbraking_v13.py` → `D_NONBRAKING_DH1_DH2_v13.json`; `PY analysis\d2_event_table_v13.py` → `D2_EVENT_TABLE_v13.json`; then `PY recount_d\rc_d_nonbraking_v13.py` and `PY recount_d\rc_d2_event_table_v13.py --logs-root runs`.
5. **Compare** (A10 §10.1(c): counts exact; points and interval ends on the same draws within 1e-9; calibrated levels equal):
   - `PY compare_c_v13.py` → `out\COMPARE_C_v13.json` (tested on old runs: 288 items agree);
   - `PY compare_d_v13.py` → `out\COMPARE_D_v13.json` (tested on old runs: 83 of 83).
   A disagreement stops the work: record both versions, the cause and the fix.
6. Copy the final JSONs to `out\`. **STATUS.md**: outputs with paths. Tell the coordinator only if blocked or if a target time slips.
