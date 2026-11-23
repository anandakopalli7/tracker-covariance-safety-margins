# DR (AMENDMENT_11 §6c): records and deviations before LOCK_A11c

Session F (Claude Opus 5.5), 21 Nov 2026, EST by this laptop's clock. Each entry was recorded before LOCK_A11c and before any DR value
on fresh runs. Entries are frozen in `work\locks\FREEZE_DR.json`.

## R1. The second program's brief misstated the divisor of u_i (found and fixed on old runs, before the lock)

- **What:** the brief F wrote for the second program (Claude Sonnet 5.5, 14:16) said that u_i, the rank variable of the
  amplitude-matched ranking oracle (A10 §2.2), divides by n = all evaluated decisions. F took this from A10 §2.2's wording without
  checking the frozen code. Two later messages repeated it: "your u_i convention ... is the one meant; keep it", 14:40.
- **The convention of record:** the frozen `shared\trackers\trk_score_v01.e5_u`, which produced every E5 value of package C, divides
  the mid-rank by n_r, the number of evaluated decisions that have a ratio. Decisions without a ratio keep u_i = 0.5.
  The step-0 Sonnet recount reached the same convention independently (coordinator, 15:10).
- **How it was found:** comparing the two programs on the 35-run pre-lock test set (old lead-braking fit runs, exploratory). The
  first program's file was `out\TESTOLD_DR_RESULTS_v01.json`; the second program's was `dr_recount_v02.py` before the fix (SHA-256
  `d2a4501a…`), now set aside as `logs\TESTOLD_DR_RECOUNT_v02_stale_u_all_n.json`.
  - 53 of 65 keys agreed within 1e−9, including every count, level, verdict and P̄, the masks, the re-association counts and the
    reference values.
  - 12 values differed, all built from the oracle: c, c − RR(E5p), and c in the two descriptive populations. The differences were
    about 1e−4, the largest 4.4e−4 (`logs\DR_COMPARE_TESTOLD_v01_stale_u.json`).
  - The second program's own diagnostic under the other reading gave c 0.426074, equal to the first program's test value.
- **Fix:**
  - The second program now uses n_r: `recount\dr_recount_v02.py`, SHA-256 `5c1cc1c1399f30f2d3678d834041a35d9d33d8c87f8ba94d41e2c57f3c00766a`.
    The other reading stays as a diagnostic, `details.alt_u_all_n`.
  - The program history: `dr_recount_v01.py` (first text, v01 masks) → `dr_recount_v02.py` (v02 text) → the n_r edit in place.
  - The §6c text spells the convention out: v04, merged by the coordinator (`A11_6c_DROPOUT_SPEC_v04.md`, `c26b093f…53e8`).
  - The first program was not changed; it calls the frozen `e5_u`.
- **Check after the fix:** the rerun of the 35-run test on pod d01 (`recount\TESTOLD_DR_RECOUNT_v02.json` against
  `out\TESTOLD_DR_RESULTS_v01.json`, `out\DR_COMPARE_TESTOLD_v01.json`).

## R2. Mask law: first wording superseded before any value

`code\dr_masks_v01.py` and `masks\DR_MASKS_v01.json` (run-id seeds, no gap row) implemented §6c v01. They were superseded at 14:30 by
the one mask law shared with §6d (protocol case id, gap row): `code\dr_masks_v02.py` and `masks\DR_MASKS_v02.json`. The old files
are kept and unused. Test outputs made under the old law were moved to `out\superseded_v01_test\` locally and
`/root/dr/superseded_v01_test` on the pod.

## R3. Identity check (i): the rule of comparison

The first evaluation of check (i), at 14:33, used CD's replay-against-replay pod rule (bit-identical on read keys, equal key sets).
It failed on key sets only: CD's arrays carry four extra sources (cTG1, cTG2, cTG4, clearR075).

The record is A10 B0(b), "arrays rebuilt from the replayed actor lists reproduce the stored ones ... within 1e−12", because CD's CV0
arrays are built from the logged tracks (session B, 14:30). Under it check (i) passes: 104 of 105 runs bit-identical on the read
keys; one run differs in the last bit (≤ 5.7e−14). The first evaluation is kept: `logs\DR_IDENTITY_v01_first_rule_*.json`.

## R4. Lock stage

DR's lock is `LOCK_A11c.txt` (coordinator, 14:49); `LOCK_A11b.txt` covers §6d only. Every DR program refuses DR values without
LOCK_A11c: `dr_extract` P̄, combine and dr; `dr_analysis`; the pod lock bundle; the post-lock chain; the second program.
