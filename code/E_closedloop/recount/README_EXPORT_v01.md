# README_EXPORT_v01: A_RECOUNT_E.json from the second program

`e_recount_export_v01.py` turns the outputs of `e_recount_v03.py` into the flat key file of RESULTS_INTERFACE_v13.md (section 1 format, section 3 "E" keys, section 2 status keys). Written from the interface and the captions of Tables S9 and IV; the first program was not read. Standard library only.

    python -I -B recount\e_recount_export_v01.py --e3 o_e3.json --e3b o_e3b.json --compare cmp.json --e1 e1.json --calib calib.json --matched matched.json --status ran --e1-attempts 1 --out out\A_RECOUNT_E.json

Output: `package` "E", `written`, `program`, `program_sha256` (of the exporter), `lock2_sha256` (of `revision_v13\LOCK_A10_2.txt`, or null if absent; `--lock2` overrides) and `values` (218 keys: the 211 table keys, E.status, E2.low_power, EH1-EH3, E3.NIMM.dropped, and E3.PS.caution_matched = False, a coordinator caveat not in the interface).

## Definitions
- Runs of record: valid runs; one per (arm, level, lead variant, case), the last by run id.
- Per arm and level: `.contact` share of runs with contact; `.vimp` median impact speed (runs with contact); `.tlost`, `.restgap` means over defined runs; `.peakdec`, `.jerk` medians; `.fallback` pooled: sum of full-braking assessment decisions / sum of assessment decisions (per-run count = fallback_share x n_assessment_decisions, an exact integer).
- `.dc`, `.dc.ci`, `.dt`, `.dt.ci` from the compare file (contact_diff and its Newcombe interval; time_lost_diff and its bootstrap interval). Contact difference is a fraction, time lost in seconds. None where undefined (no pairs, or an interval that v03 leaves null for fewer than 2 pairs). NIMM is against F0IMM, the others against F0. E3b kinds: const = constant, mild = mild_braking, stopgo = stop_and_go.
- EH1, EH2, EH3: classification of CK3 lo, N lo, NIMM lo. `E3.NIMM.dropped` False if both IMM arms have valid E3 runs.
- `E3.F0.<lev>.caution`, `E3.PS.<lev>.caution`: percent, from the matched recount. `E2.<g>.contact` from the calibration shares (key g0, g0_25, g1, g4, g16, g64); `E2.g_lo`, `E2.g_hi` numbers; `E2.low_power` from the calibration file.
- E1: `dist` = measured stopping distance, `model` = planner model distance, `err` = |dist/model - 1|, `maxerr` the largest; the run per speed is the one the brake recount used. `E1.attempts` from `--e1-attempts`; `E.status` from `--status`.
- `E3.n_cases`, `E3b.n_cases`: distinct cases among the runs of record.

Dry run on the relabelled E2 set: `tests\out\RELABEL_A_RECOUNT_DRYRUN.json` (no missing key, one extra: E3.PS.caution_matched).
