# E2 first-vs-second program comparison: disagreement record (A10 10.1(c))

Written 19 Nov 2026 by session E (Claude Opus 5.5). Comparison program: `analysis/e_compare_v01.py outcomes`.
Output: `out/E_COMPARE_OUTCOMES_E2_v01.json`.

## Result before the fix
- 180 runs compared, all valid in both programs.
- Contact, first contact tick, impact speed, time lost, rest gap, peak deceleration and RMS jerk agree within 1e-9 in every run.
- **Fallback share disagrees in 31 of 180 runs.**

## Cause (checked in all 180 runs, not sampled)
- Both programs use the same decisions: assessment mode, ticks >= 99, the same count in every run.
- First program (`analysis/e_outcomes_v01.py`): it counts a decision as full braking when the selected plan is the (-5, -5) row. This covers two cases: the row is selected as the fallback (`output.fallback`), or it is selected as the first feasible row of the 16-row library.
- Second program (`recount/e_recount_v01.py`, README item 11): it counts only `output.fallback`.
- In every run, the first program's numerator equals the second's plus the number of decisions that selected (-5, -5) as a feasible row without the fallback flag. Those decisions occur in exactly the 31 disagreeing runs.

## Reading of the amendment
- A10 7.4 says: "Fallback share: the share of decisions in full braking."
- The (-5, -5) row commands the same full braking whether the library reaches it as a feasible row or as the fallback.
- The second program's definition is therefore narrower than the text. The first program's definition follows the text; it was also the reading asked for by the build review (Minor 8).

## Fix
- The second program is corrected in a new file, `recount/e_recount_v02.py`, written by a Sonnet subagent from the amendment text. v01 is left as frozen in FREEZE_E.json. The change is recorded in `recount/README_RECOUNT_v02.md`.
- The E2 outcomes are recounted with v02, and the comparison is rerun. The outcome of that rerun is added below.
- Fallback share is descriptive (A10 7.5, "Other outcomes"): it feeds no hypothesis, no level choice and no validity rule. The E2 levels and LOCK_A10_2b are unaffected.

## After the fix (19 Nov 2026, about 22:55 EST)
- The second program, v02, was written by a Sonnet subagent that did not open the first program's code.
  - `recount/e_recount_v02.py`, SHA-256 5bbc7b9ddab4fe68e057d8e87185eecf36ffe0cf533b2baa15461c8acfdabb5f.
  - `recount/README_RECOUNT_v02.md`, SHA-256 9bb0ae47036e42c8b59adb7a6123e8d81f1f2c932b0aaee609a809d20859dad9.
  - In v02, fallback share counts decisions where the fallback flag is set or the targets are (-5, -5). The extra field `fallback_flag_share` keeps the v01 quantity; in all 180 runs it reproduces v01.
- The subagent confirmed the cause in the raw frames. Example job e2_c1109_tune_0006_f0_g0 has 66 assessment decisions. 11 have the fallback flag, and all 11 have targets (-5, -5). 5 more select (-5, -5) without the flag. The two programs' numerators are 16 and 11, both over 66.
- v02's recount of E2 (`out/E2_RECOUNT_OUTCOMES_v02.json`, SHA-256 c9a8e2ac6386d82ddf5405bdca92d6c6f8a74b4c667ff3fcda545b569b16f2c2) reproduces v01 in every other field.
- v02 also reproduces v01's stored test outputs: outcomes on synthetic E2, E3 and E3b; brake good and weak; compare.
- The comparison was rerun (`out/E_COMPARE_OUTCOMES_E2_v02.json`, SHA-256 f284c587ab6cc755d87af89fa48f54a948b24133a7e73280b4321db03eb9de77). Result: **180 runs compared, 0 disagreements.**
- E3 and E3b are recounted with v02.
