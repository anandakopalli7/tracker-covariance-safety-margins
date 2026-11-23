# Recount4: independent second program for the scoring of the reaction-and-stop estimate

Brief: `RECOUNT4_BRIEF_v01.md` (this folder), with the inputs, scoring definitions and bootstrap of record of `revision_v11\recount\RECOUNT_BRIEF_v01.md`.

## Record made before the first program's file was opened

- `RECOUNT4_RESULTS_v01.json` written 18 Nov 2026 19:14:20, sha256 `b5d428524e066e270d52cc31057c23d5c5accf4b1d88659391a5cfcb2f66f04c` (also in `RECOUNT4_RESULTS_v01.sha256.txt`, written by the program itself).
- Program at that moment: `r4_items_v01.py` sha256 `bef455ca89b045fe167ae04d85df7655da088e823118a630fea9e87400f8f786`.
- Self-check by a second route finished before the comparison: `r4_naive_v01.py` (sha256 `5428c121c10e7ecce7706922e6851724e82cb206afc049b8229f48f459936bd4`), output `r4_naive_v01_out.json` (sha256 `12e57e78e5dc7fdc543c6fe672f67482c5327d5d73742a7ac63ca9453be9378f`).
- This record was written 18 Nov 2026 19:18. Up to this moment nothing of `revision_v11\analysis`, `revision_v11\draft`, `revision_v11\package_v11` or `P\11_ojits\A6R\code` had been opened.
- Readings of the brief fixed before the comparison (details in "Ambiguities" below, written after it without changing them):
  1. "Relative to 3 s": denominator = the 3 s commitment scoring (unsafe when `clear` <= 0), entry `rel.3s_commitment`. A second denominator, the 3 s-window scoring at the same setting (`clear61`), is stored as `rel.3s_window_same_setting` as an addition.
  2. `est_signed`, relative to 3 s: `rel.3s_commitment` uses the 3 s commitment with the paper's caution (literal reading, taken as the primary one); `rel.3s_commitment_signed` uses the 3 s commitment with signed caution.
  3. `cens`: a pair is unsafe when `clearX` <= 0 or `cens` is true.
  4. Shares "den <= 0" are over all 20,000 resamples.
  5. "Unsafe on the 3 s window" in the pair counts: `clear61` <= 0.
  6. Intervals of sums, percentage points and decision-equivalents: over all resamples with a finite value; intervals of ratios: over the resamples with a positive denominator.

(The rest of this report is written after the comparison.)
