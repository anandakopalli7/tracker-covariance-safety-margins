# Review of the E5 build (A12 §6), v01

Reviewer: Fable 5.2 (independent of the author), 22 Nov 2026. Nothing was edited. All checks below were run read-only on the laptop (one process).

## Verdict: PASS WITH FIXES

No blocking finding. The E5C calibration capture can start on packet v05 and the written job lists as they are. Two major findings (M1, M2) are in `e5_analyse_v01.py` and must be fixed before `cal` is run on the fetched runs, because `cal` writes the settings file that LOCK_A12b records.

## What was checked and holds

1. **Packet v05**
   - `diff -rq src_v04 src_v05`: only `E_PBAR_CANMOT_v01.json` differs (plus `__pycache__` in v04).
   - `packets\packet_e_v05\claude_smoke_v01` differs from v04 only in that file and `RUNTIME_SOURCE_BINDING_SMOKE_v01.json`; the two manifests differ accordingly. The old P̄ hash (`fd89f69e…`) appears nowhere in packet v05 or its receipt; the new one (`4b373f6e…`) is in the binding, both manifests and the receipt. The file inside `packet_e_v05.tar.gz` has the new hash.
   - `Pbar` (both 4×4 matrices) and `counts` are equal, value for value, to `F_dropout\out\PBAR_DR_v01.json`; the recorded source SHA-256 (`a50b3a1d…`) is that file's. Both matrices are symmetric to 1e-17 and positive definite.
   - `e_arms_v01.load_pbar` (L256–261) reads `data['Pbar']`, classes vehicle / pedestrian, 4×4: unchanged, and the file has that shape.
   - Other users of the file: `e_sources_v01.apply_source` (L251–266) uses P̄ for Z, F0, BRAKE, CK3 and PS; N reads the tracker's own `tr['p']` and does not use it. The review scripts do not read P̄. No P̄ hash is hard-coded in `tools\`, `analysis\`, `tests\*.py` or the reviews. The method record carries `pbar_sha256` for every arm.
2. **`e5_match_v01.py`**
   - The run dict is built as `rev_common_v01.load_runs` builds it: `clear1 = L.clean_clear(clear)`, `masks_of(ev, v0, phase)`, `idx55`, `vbar`, `desired` from the meta.
   - F's `phase` is the truth phase of `oxsb_extract_v05` (`trk_arrays_v01.py` L125, L248–250; values 0–3, default 3): the same coding as rev_common's `ph`. The caution used is population "all" (mask 0 = evaluated), which does not depend on the phase.
   - All 105 arrays: mode `dr`, `punish_num` 3, `pbar` "P-bar_DR (PBAR_DR_v01.json)", `test_old` false, family lead_braking. Each file's `masked` rows equal `e_dropout_v01.mask_for_case(case_id, n_det_rows)` (0 mismatches). `cF0` differs from the record-P̄ copy in `DRrec\` in all 105 files; `cN` is identical in all 105.
   - I recomputed both curves and the four rows: identical to `E5_MATCH_TABLE_v01.json` (curves bit-equal; 21,574 evaluated decisions; list hash equal). Both curves are monotone with no NaN; no row is at a grid end.
   - The 105 design cases are disjoint from the 135 main cases and from the 30 tuning cases.
3. **`E5_MASKS_v01.json`**
   - `tuning_cases` = the 30 lead-braking tuning cases of the protocol (E2's rule). `main_cases` = positions 55+ of the lead-braking evaluation pool at each speed, in order (51 / 33 / 51 = 135). None of the 135 is in any earlier E job list or in C's case list.
   - All 165 masks, windows and seeds equal the law in `src_v05\e_dropout_v01.py` at 69 rows; `law_file_sha256` is that file's.
   - All 165 cases exist in the packet's protocol file.
4. **Job lists**
   - 120 study jobs, unique ids, 30 cases × g ∈ {4, 8, 16, 32}, all `E_F0`, CANMOT, phase `E5C`, level `cal`, `dropout` A11D2, `punish_num` 3. Each case's four runs are on one pod (8 / 8 / 7 / 7 cases). Each list starts with A1 crash, A1 benign and one crash control.
   - `worker_main_v01.py` L96–98 validates the knobs whenever either is present, whatever the phase; L281–285 (E4_METHOD_MISMATCH) keys on `job['dropout']`, not on the phase. `level` and `phase` are free strings. E5C / E5 jobs pass.
5. **`e5_analyse_v01.py`**
   - **One-sided p:** it rebuilds the pairs exactly as `compare` does (sorted common cases, both valid) and draws `default_rng(20261922).integers(0, n, (20000, n))`: the same index matrix. `≥ 0` is the right tail for H1 "N has fewer contacts" (difference N − F0_D < 0). The resampled means of integer differences are exactly 0 when the sum is 0, so there is no rounding risk at the boundary.
   - **Export:** 45 keys, equal to `E5_EXPORT_KEYS_v01.json`.
   - **`level`:** `e_collect_v01.one()` only copies `level` from the job. `cal` never reads it; `main` overwrites it with `'D'` before `compare`. Nothing breaks.
   - The lock gate (L104–105) and the g_D rule's order (low-power first, then nearest 0.20) follow §6.4.

## Findings

### M1. No check that a run used packet v05's P̄, the job's g, or the expected arm
`analysis\e5_analyse_v01.py:45–76` (`mask_check`, `collect`), `:79–90` (`cal`), `:109–118` (`main_stage`).

The one change of this set is the P̄ file, and §6.3 says the method records its SHA-256. Nothing reads it. `collect` also does not compare the method's `g`, arm, tracker or case with the job, or (in `main`) with `g_D` / `g_N` of the settings.

- **Failure scenario:** the job lists use the same `volume_folder` (`claude_v13_e_v01`) as E4. A pod that starts from a volume still holding packet v04 runs `E_F0` with the P̄ of record. Every run passes the review and the mask checks. `cal` then picks g_D from the wrong class average, or `main` compares N with F0 instead of F0_D, with no message.
- **Fix:** in `collect`, mark a run invalid unless `SUMMARY['method']['pbar_sha256']` equals `sha(src_v05\E_PBAR_CANMOT_v01.json)` (`4b373f6e…`), `method['tracker'] == 'CANMOT'`, `method['knobs']['g'] == e_job['g']`, and the arm is `E_F0` (cal) or `E_F0` / `E_N` (main). In `main`, also require `g == s['g_D']` for `E_F0` and `g == s['g_N']` for `E_N`. Add the P̄ hash to `E5_SETTINGS_v01.json` so LOCK_A12b records it.

### M2. The g_D tie rule is decided by float rounding
`analysis\e5_analyse_v01.py:90`.

`abs(s - 0.20)` on float shares does not give equal distances for exact ties. With 30 valid runs per g: 5/30 gives 0.033333333333333354 and 7/30 gives 0.033333333333333326. The same holds for 4/8, 3/9, 2/10 and 1/11.

- **Failure scenario:** the smaller g has 5 contacts and a larger g has 7 (a non-monotone pair, possible at n = 30). The exact distances are equal, so §6.4 gives the smaller g. The code picks the larger. A second program written with exact fractions disagrees on g_D, the value LOCK_A12b locks.
- **Fix:** compare exact distances, for example `abs(5 * contacts - n_valid) / (5 * n_valid)` as `fractions.Fraction`, and take the first minimum. Tell the second program's writer the same rule.

### m1. `mask_check` crashes on a run without a method record
`analysis\e5_analyse_v01.py:49–50, 57`. `ARM_METHOD_v01.json`, `contract.json` and `detections.jsonl` are read unguarded, although `e_collect_v01.one()` (L45–46) allows for a missing method record.
- **Failure scenario:** one capture that failed early leaves a capture folder without `ARM_METHOD_v01.json`; `cal` or `main` stops with FileNotFoundError near the 08:45 limit.
- **Fix:** if `r['valid']` is already false and a file is missing, return `(False, ['no method record'], None)`.

### m2. The one-sided p crashes with no valid pair
`analysis\e5_analyse_v01.py:120`. `integers(0, 0, …)` raises before the `if n` guard on L121. Fix: `idx = … if n else None`.

### m3. `main` does not re-check the masks and match-table hashes
`analysis\e5_analyse_v01.py:108`. The settings file holds `masks_sha256` and `match_table_sha256`, but `main` (and `make_jobs_e5_v01.py:31`) read `E5_MASKS_v01.json` without comparing. A changed table would still be caught by the law check, so the risk is small. Fix: assert `sha(MASKS) == s['masks_sha256']` and `sha(TABLE) == s['match_table_sha256']`.

### m4. `E5.n_cases` counts cases with any run, valid or not
`analysis\e5_analyse_v01.py:122`. §6.9 does not say which. The second program may count valid pairs and differ. Fix: state the rule in the text given to the second program (or export `c['pairs']`).

### m5. Missing runs do not change `E5.status`
`analysis\e5_analyse_v01.py:110–113, 122`. `missing` is written to the outcomes file but the export says `ran`. `cal` likewise does not check that all 120 runs (30 per g) are present. Fix: print and record the missing count in `cal`; refuse or flag in `main` when `missing` is not empty.

### m6. One control per pod, at the start only
`tools\make_jobs_e_v01.py:183–187` (`CTL_EVERY = 50`), used by `make_jobs_e5_v01.py:45`. E5C pods have 28–32 study jobs and E5 pods will have 45, so no control follows the study runs. §6.2 asks only for "controls on every pod", so this meets the text; a closing control would show drift.

### m7. No E5 pod-finish or admission check exists yet
`tools\finish_pod_e4_v01.py:17` accepts pods 11–16 only, and `tools\e4s_check_v01.py:52` globs `e4s` ids. §6.7's "controls identical" is checked by neither E5 program. Fix: an E5 copy that checks A1 and `ctl_e5c_*` / `ctl_e5_*` (`comparison_to_reference.identical`) before a pod is deleted.

### m8. The worker does not require the knobs for phase E5 / E5C
`src_v05\worker_main_v01.py:97`. Only phase `E4` forces them. A hand-made E5 job without `dropout` would run unmasked. The lists are correct and `mask_check` would reject such a run ("no dropout record"), so no packet change is needed.

### m9. Packet v05 changes F0-based arms other than F0
`src_v05\e_sources_v01.py:256–266`. Z, BRAKE, CK3 and PS would also use P̄_DR. E5 runs none of them. Note in STATUS that packet v05 is for E5 only.
