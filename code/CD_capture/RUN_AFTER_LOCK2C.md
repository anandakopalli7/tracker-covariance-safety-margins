# Packages C and D: stage-2 steps after LOCK_A10_2c (written 20 Nov 2026 before any fresh value; frozen in FREEZE_CD_2)

All commands from `work\CD_capture`, with `PY = .venv\Scripts\python.exe -I -B -X utf8` and `OPENBLAS_CORETYPE=Haswell`; recount
commands from `recount\` or `recount_d\` with `..\.venv\Scripts\python.exe -I -B -X utf8`.
Two-stage Lock 2: every program here needs BOTH `revision_v13\LOCK_A10_2.txt` and `revision_v13\LOCK_A10_2c.txt`.
The core steps 2–6 of `RUN_AFTER_LOCK2.md` (core exports, calibration pods, imports, D) also start only now.
Every step starts as soon as its inputs exist (coordinator, 01:24): nothing waits for a clock time.

## 0. Gate
- `PY make_freeze_cd_v13.py --verify` (stage 1 + FREEZE_CD_add1) and `PY make_freeze_cd_v13.py --stage 2 --verify`: no changed or missing file.
- Steps 1a/1 of `RUN_AFTER_LOCK2.md` (logs; CV0/B1 arrays for c_lead, CV0 for c_cutin and d1) are complete.

## 1. Extraction (arrays only), in parallel where possible
- **RSX** (extended reaction-and-stop clearance, rev_e1 port; shared with package B's B6 and with D2): `PY analysis\x_rsx_extract_v13.py --workers 2`
  → `arrays\RSX\<rid>.npz` (≈1.8 h on the laptop; on a pod `--not-laptop`, ≈10 min). **Tell B when done** (B6 waits for it).
- **S57A cut-in inputs:** `PY analysis\x_s57a_extract_v13.py --set c_cutin --workers 2` → `arrays\S57A\<rid>.npz` (≈5 min).
- **B7, both families, on pods** (`tools\trk_pod_plan_v13.md`): one or two 32-vCPU RTX 4090 pods (claude-v13cd-b01/b02; spend-log rows;
  session-tracked backstop). Environment as the calibration pods (uv CPython 3.12 + the laptop's pinned packages, see the plan). Upload
  code + the 0037 acceptance data; acceptance: `x_trk_extract_v13.py --test-old` on 0037 bit-identical to
  `analysis\out\testold_b7_arrays_final\` (else the laptop). Then upload the fresh run files the plan lists + the B7 detection files and run
  `x_trk_extract_v13.py --family lead_braking` and `--family cutin` (`--part i:n` per worker) → `arrays\B7_<r>_<L>\` and `arrays\B7CI_<r>_<L>\`;
  download with SHA-256 checks; delete the pod(s). Laptop fallback: 2 workers, ≈7–10 h per family.

## 2. First programs (stage 2)
- `PY analysis\d2_rs_v13.py` → `analysis\out\D2_RS_v13.json` (after RSX; identity check against clearX inside).
- `PY analysis\c_s57b_v13.py` → `analysis\out\S57B_v13.json` (after RSX and B1; ≈1.5–2 h).
- `PY analysis\c_s57a_v13.py` → `analysis\out\C_S57A_v13.json` (after the core `--calib import` of C_LEAD and C_CUTIN, whose calibrated levels its `.dec.ci` use, and after S57A extraction; ≈45–60 min).
- `PY analysis\c_b7_v13.py` → `C_B7_v13.json`; `PY analysis\c_b7ci_v13.py` → `C_B7CI_v13.json` (after the B7 arrays; ≈2.5 h each on the laptop).

## 3. Second programs (stage 2)
- `rc_s57a_v13.py --workers 2 --levels-lead out\RC_C_LEAD_v13.json --levels-cutin out\RC_C_CUTIN_v13.json` → `recount\out\RC_S57A_v13.json`
  (after the recount's own core import; levels from the recount's own calibration).
- `rc_s57b_v13.py` → `RC_S57B_v13.json` (two chunk processes per its README if needed).
- `rc_b7_v13.py` → `RC_B7_v13.json`; `rc_b7_v13.py --family cutin [--truth-file out\RC_C_CUTIN_TRUTH_v13.json]` → `RC_B7_v13_cutin.json`.
- `recount_d\rc_d2_rs_v13.py --logs-root ..\runs` → `recount_d\out\RC_D2_RS_v13.json`.
- `hand_check_v13.py` → `recount\out\HAND_CHECK_v13.json` (A10 §10.2; HAND.status).

## 4. Exports and comparisons (A10 §10.1(c), (d): after the last first-program output)
- `PY export\make_export_cd_v13.py first` → `out\A_EXPORT_C.json`, `out\A_EXPORT_D.json`; `PY export\make_export_cd_v13.py second`
  → `out\A_RECOUNT_C.json`, `out\A_RECOUNT_D.json`. TRANSFER.structured needs B's and F's exports; re-run the exporter once they exist.
- `PY export\compare_exports_v13.py` → `out\COMPARE_EXPORTS_v13.json`; `PY compare_c_v13.py` → `out\COMPARE_C_v13.json`;
  `PY compare_d_v13.py <first dnb> <second dnb> <first d2> <second d2>` → `out\COMPARE_D_v13.json`;
  family files key by key: `PY export\compare_values_v13.py <first> <second> out\COMPARE_<FAMILY>_v13.json`.
- A disagreement stops the work: record both versions, the cause and the fix; recount the corrected value.
- Tell A that the exports exist (with `deviations`); STATUS.md.

## Old-run tests behind this runbook (all first vs second, key by key; before any fresh value)
- C core: 343/343 (`out\COMPARE_C_v13_TESTOLD_matched_final.json`); D: 83/83.
- S57A: 74/74 (`out\COMPARE_S57A_v13_TESTOLD_try1.json` + `..._dec_levels.json`); S57B: 282/282 (`out\COMPARE_S57B_v13_TESTOLD.json`);
  B7 lead 76/76 (`out\COMPARE_B7_v13_TESTOLD_lead.json`); B7 cut-in: all values on the one testable chain (`out\COMPARE_B7CI_v13_TESTOLD.json`);
  D2 reaction-and-stop: see `out\COMPARE_D2RS_v13_TESTOLD.json`; hand check 20/20 within 1e-6 m.
