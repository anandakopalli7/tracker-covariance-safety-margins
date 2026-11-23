# Compiler's own checks of v11 (not a panel seat; written before the v10 review was opened)

These are the compiling session's spot checks of numbers and wording, made while reading the package for Phase 0. They are not reviewer findings and do not enter the mechanical decision. Where a seat raises the same point, the seat's finding is the record.

## Numbers recomputed from printed values (all agree)

| Claim (location) | Recomputed from | Result |
|---|---|---|
| CK3 "about 383 of 8,290 decisions" (§V-B) | 0.831 × 460.7 dec.-eq. (Table S23 room) | 382.8 ✓ |
| AM "about 173 of 8,290" (§V-B) | 0.376 × 460.7 | 173.2 ✓ |
| Pooled room 2.6 × decision-weighted phase rooms (2.13) (§V-C) | (678×0.43 + 755×15.59 + 6857×0.82)/8290 = 2.133; 5.56/2.133 | 2.61 ✓ |
| 0.95 pp remaining with per-phase scales (§V-C) | 5.56 − 4.96 + 0.35 (oracle's own per-phase gain, Table S23) | 0.95 ✓ |
| CK3 0.63 of the remaining room (§V-C) | 49.7 / 78.4 | 0.634 ✓ |
| Phase-weighted den₀ "6% of the pooled one" (§V-D) | 3.7 / 58.8 | 6.3% ✓ |
| N, 2 m gap, 3 s: 5.3 of 8,290 above F0 (§V-D) | 0.0087 × 612.0 | 5.3 ✓ |
| N, 2 m gap, lead braking: 1.2 of 755 (§V-D) | 0.0076 × 157.1 | 1.19 ✓ |
| N, 2 m gap, after stop: 5.8 of 6,857 (§V-D) | 0.0535 × 107.7 | 5.76 ✓ |
| N within 0.7 decisions at zero gap (§V-A) | max |D/201| in Table S1 at zero gap = 0.0068 pp → 0.0068/100 × 8290 | 0.56 ✓ |
| Coverage 92–93% and calibrated levels 96–97% (§IV-B) | Table S16: 0.934, 0.922, 0.933, 0.932; 0.964, 0.972, 0.962, 0.97 | ✓ |
| Commitment ratios 0.29/0.18/0.12/0.06 and 0.14 (§V-D) | Table S19: 0.293, 0.179, 0.122, 0.064; 0.144 | ✓ |
| Abstract length | word count of the abstract paragraph | 247 (limit 250) ✓ |

## Wording problems found by reading

1. **Stale sentence in Supplement S8.2 (paragraph beginning "With a perfect stop 0.75 s after committing, as scored").** It still says that "the location of the room under the 3 s commitment (Section VI) does not hold" and calls the cross-phase effect "a mechanism that no analysis here isolates". Section V-C of v11 isolates exactly that mechanism (one scale per phase recovers 0.89 of the room), Section VI no longer makes a location claim, and Table S4 (row "The location of the room (this version)") says both phrases were replaced. Fix: rewrite or delete that paragraph of S8.2 so it agrees with §V-C and Table S4.
2. **Quoted pre-fixed wording altered by the rename "braking prior" → "braking prediction".** Supplement S8.1 (abstract consequence rules) and Table S4 (row "The abstract's last sentence") print the plan's fixed sentence in quotation marks with "braking prediction's share", while Table S4 (row "The abstract's last sentence (this version)") prints the same fixed sentence with "braking prior's share". A quotation of pre-registered wording should be verbatim, with the rename noted outside the quotation marks.
3. **Version history inside a journal supplement.** Table S4 and the paragraph after it print earlier drafts' abstracts and draft-by-draft wording changes ("Added in draft v03", "v04", "v06"). A deviations-from-plan table belongs in the supplement; internal draft history belongs in a cover letter or the deposit.
4. **Abstract sentence 3** ("CARLA runs in which a lead vehicle brakes are perceived by the CenterPoint detector and CANMOT…"): grammatical but hard to parse on first reading; the same construction is in §I.

## Method points to watch (for the compiler's comparison with the panel)

- The per-phase-scale frontier (§V-C, Table S23) is the best frontier over all 202³ scale triples, chosen on the evaluation runs themselves; the 400 run resamples redo that choice in each resample, so they carry the same in-sample optimism and do not correct it. A cross-validated version (scales chosen on the tuning runs, or leave-runs-out) would show how much of the 0.89 survives out of sample.
- The double bootstrap takes the full-sample value as the truth. For RR(N), whose full-sample value sits at the 97.7th percentile of its own bootstrap distribution, that calibration rests on a bootstrap that the paper itself suspects is inconsistent; the subsampling intervals all exclude zero. The robust statement is the bound (< 0.5% of the room by every method), which the paper makes; "calibrated" should not be read as "valid".
- The 0.5% bound in "no interval method we tried reaches 0.5% of the room" is not said to be fixed before the values were read.
- Five of 35 evaluation runs and 10 of 20 tuning runs ended at contact under the recording planner (Table S28): a fact about the recording planner that the text reports without comment.
