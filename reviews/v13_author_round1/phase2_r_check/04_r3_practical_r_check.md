Phase 1 file SHA-256 (`phase1\04_r3_practical.md`): 8795bc733e80492af661f558809904fb8c35686241878a6ae534143d0e4b226b

# Phase 2: check of the earlier panel's R-1 to R-19 against the 18:30 text, seat R3 (Practical)

## Header

- **Seat, model, card:** Peer Reviewer 3, Cross-disciplinary / Practical; Claude Sonnet 5.5 (`claude-sonnet-5-5`); Card 4. **Card-confirmation pause not held** (non-interactive run).
- **Package files at start and end (unchanged, as in Phase 1):** `MANUSCRIPT_v13.md` 29125167b108bc27833c16e3b639cbb07af5f4c105c49d375deff3d5b4a951d0; `MANUSCRIPT_v13.tex` bd4d08d954d3595de2b5ac2653c18476c7bb3281e1c264604f995f018da01345; `SUPPLEMENT_v13.md` fab98c1fe24c8c5b95f86da8b1e664662401055232409a236d963938f5b99a09; `MANUSCRIPT_v13.pdf` 4fabfd9f611013fd4e7f60b8a59fcdcc2d782dbd3192a77c2efe54e77beb8299; `SUPPLEMENT_v13.pdf` a8ad36027dee70c8c48cf2b998cb2512b55ca568c400eb1ecd340923ddeb8b16.
- **Pages viewed:** manuscript `page01` to `page05`, `page07` to `page13`; template `tpl01`, `tpl02`; supplement `sup01` (added in Phase 2, for Q7-18). Phase 1 file was not changed after the earlier list was opened.
- The earlier list was opened only after the Phase 1 hash above was recorded.

## R-1 to R-19

| ID | Verdict | Evidence from the 18:30 text (location) | What remains |
|---|---|---|---|
| R-1 | resolved | V-E dropout paragraph: "its factors (0.216, 0.107, and 0.065 for the first, second, and third missed update; 0.925 after reacquisition) are the median ratios of the covariance margin's critical scale to the class average's … fitted on the 105 earlier runs"; "a level effect that needs no per-decision covariance"; "10 Hz … was not compared with a coast-count margin". VI: "with factors set to the median ratios … reproduces the dropout gain". | Nothing. |
| R-2 | resolved | V-E last paragraph: "For the IMM (secondary) … 0.210 [0.158, 0.255] (99% interval) around misses and 0.093 [0.066, 0.116] over all pairs"; abstract: "the fixed-noise tracker's spread ranks the realized error weakly around missed detections and slightly inversely over all tracks". | Nothing. |
| R-3 | resolved | V-E paragraph 5: "(2.8%, 3.0%, and 2.2%) are, as point values, inside the paper's ±5% equivalence margin: detectable, but small by that margin (no equivalence test was registered for them). At start probabilities 0.20 and 0.30 the dropout share is about 5%". VII says "a few percent of the room" and no longer claims equivalence. | VII does not carry the words "as point values"; harmless now that VII makes no equivalence claim. |
| R-4 | resolved | V-E: "This share holds for the position–velocity interface (Section III-D) only; a wider interface was not tested." VI Limits: "so the two-noise IMM's share holds for that interface only … and is no verdict on maneuver-adaptive covariances." | Nothing. |
| R-5 | resolved | Abstract: "with a constant-velocity prediction"; VI: "The room itself lies almost wholly in braking (Table 3: 1.63, 23.62, and 0.08 points …) … which a fixed-noise covariance has no way to track"; VI and VII: "whether a covariance adds anything on top of the braking prediction's path was not tested" / "a covariance added to a braking prediction's path". | Nothing. |
| R-6 | resolved | IV-E: "The original lead-braking sequence, which is not Holm-adjusted, is room; detection …; and a braking-prediction share above 0.5." and "six primary hypotheses are Holm-adjusted (the H rows of Table 6): the dropout replication, the slope …, the two-noise IMM's class, the adaptive filter's twin replication, the closed loop with dropouts, and the nuScenes mechanism check". | Nothing. |
| R-7 | resolved | Table 6 rows: "failed, Holm 0.99" and "failed, Holm 0.18"; caption: "Holm: Holm-adjusted one-sided p within the third amendment's two tests. H: … second amendment's six primary hypotheses". V-E last paragraph repeats "(adjusted p 0.99 and 0.18; Table 6)". | Nothing. |
| R-8 | resolved | Abstract now two-sided: "Where it is nearly constant it adds nothing …"; "In three lead-braking tests where it varies, it recovers 2% to 5% of the room: 2.8% … 2.2% … 4.6%"; "A margin that only counts missed updates reproduces the dropout gain". 245 words. VII is rewritten as a designer's summary with few numbers. | VII still follows the abstract's order of findings; it adds next steps and the designer reading, so it is acceptable under template l. 463 to 467. My Phase 1 R3-1 asks for more practical content there. |
| R-9 | resolved | Abstract: "Plans were hash-locked internally; amendment tests followed the first results." Title unchanged. | Nothing. |
| R-10 | resolved | Abstract no longer carries "varies mostly for other reasons"; V-E: "An exploratory decomposition (R² 0.47; decision-level R² 0.06; Supplement S15) attributes 54% … to the update schedule, 38% to the geometry, and 8% to the realized error"; VI: "(an exploratory reading; Section V-E)". | The variable groups behind the three shares are still only in S15 (Phase 1 R3-9). |
| R-11 | resolved | ACKNOWLEDGMENT now opens "The author conceived the study, set its questions and plans …"; the recount sentence matches IV-E ("every value printed in the main text and all but the marked (‡) values of the supplement"); "the presubmission review by an AI panel" kept; models named for each role. | The AI panel's system is not named (Phase 1 R3-6). |
| R-12 | partly resolved | IV-E now says: "The three amendments were written and locked on Nov. 21 and 22, 2026 (file times in Table S29), each after a report of an artificial intelligence (AI) review panel on the text before it, and the third's two controls were asked for by that panel (Table S5)." ACKNOWLEDGMENT still opens "made every scientific decision", with "where the amendment files record a design choice as an AI session's, it was made within the author's approval". | The first sentence was not changed to what the deposit supports; only the author can confirm. Replace by "made the final decision on every scientific question" (Phase 1 R3-6). |
| R-13 | resolved | III-A: "In pedestrian crossing (first amendment; Section V-E), a pedestrian walks across the ego's lane from a drawn side at a drawn speed of 1 to 3 m/s, starting so that it would reach the ego's path together with an ego that keeps its desired speed, after a drawn 1 to 4 s … The planner treats the pedestrian like any other actor, predicted at constant velocity. The study recorded 390 runs … after a check on 51 stored runs (step 0) had shown little room (0.08 [−0.06, 0.25] points): many crossing decisions have no binding constraint …". | Nothing (an unused occluder flag is described; Phase 1 R3-14). |
| R-14 | resolved | III-B: "Time lost is the run's duration minus the distance traveled divided by the desired speed, for runs without contact; the rest gap is the gap to the stopped lead at the end of the run." | Nothing. |
| R-15 | resolved | V-E opening paragraph: "a window starts with probability 0.10 (the primary start probability; on the new runs it masks 16.2% of updates)"; "the class average is computed under the same masks and output rule on the tuning runs (the dropout-estimated class average)". | Nothing. |
| R-16 | resolved | V-E closed-loop paragraph: "read by linear interpolation between scales 4 and 8 of its frontier at scales 4, 8, and 16 on the same cases, is 25.7% against the covariance arm's 20.7%; time lost is taken over the 89 of 135 cases without contact in any arm and lies between 25.24 and 25.84 s for the four arms (Table 6)". | Nothing. |
| R-17 | resolved | Table 2 caption: "shares with 95% intervals, except N's share (99.4%, calibrated) and the IMM's share (99%, nominal)". | Nothing. |
| R-18 | resolved | II: "With fixed noise and under regular updates, a Kalman filter's covariance settles to a steady state [26]. With intermittent observations it follows the arrival sequence instead … [27]; the coast-count result of Section V-E is consistent with that dependence"; data-association filters [28]; threat assessment [33] to [36]. | I cannot verify the added references offline; the author must check [27], [28], [33] to [36]. |
| R-19 | partly resolved | Format misses largely fixed (see below). | Remaining: "multi-object" hyphen (Q7-1), conference city and month (Q7-6), "et al." (Q7-7), CANMOT (Q7-13), ZIP (Q7-16), bold run-ins (Q7-17), no biography (Q7-19). |

## R-19, Q7-1 to Q7-19 one by one

| ID | Verdict | Evidence | What remains |
|---|---|---|---|
| Q7-1 | partly resolved | grep of the .md: "nonbraking", "retuned", "redetected", "prestated", "rescore" are now unhyphenated, and "Pre-submission" is gone; "multi-object" is still hyphenated (7 uses, abstract and Section I included). | "multi-object" against template l. 195 ("multi" … usually without a hyphen). It is the field's standard compound and appears hyphenated in references [5] and [31], so a one-spelling decision is the author's. |
| Q7-2 | resolved | VII is recast as "For a designer, three things follow …" with next steps; no longer the abstract's numbers in the same order. | Nothing. |
| Q7-3 | resolved | [26] "New York, NY, USA: Wiley, 2001"; [37] and [38] are now journal articles with volume, number, pages and DOI. | Nothing. |
| Q7-4 | resolved | [39] is now Treiber et al., *Physica A*, vol. 360, no. 1, pp. 71–88, Jan. 2006, with DOI. | Nothing. |
| Q7-5 | resolved | [40] arXiv entry with authors "2018, arXiv:1708.06374v6."; [41] "IEEE Std 2846-2022, 2022, doi"; [43] and [44] in American date form ("Oct. 30, 2020", "Mar. 9, 2021"), no free-text tails. | Nothing. |
| Q7-6 | partly resolved | Conference entries are now consistent (none has city or month) but all lack city and country; template l. 730 shows "Boston, MA, USA, 1985". | Add city, country and month to the 15 "Proc." entries (Phase 1 R3-12). |
| Q7-7 | not resolved (advisory) | [9], [13], [15], [21], [34] still use "et al." | Template l. 495 says use all names; IEEE allows "et al." beyond six; author to check. |
| Q7-8 | resolved | II: "IMM estimators [7], [8], [22]". | Nothing. |
| Q7-9 | resolved | Page 9: Fig. 4 panels labelled "(a)" and "(b)" centered below each panel. | Nothing. |
| Q7-10 | resolved | Page 7: Fig. 2 right panel now has axis labels ("Wrong goes (% of decisions)", "Caution (% of desired speed)") and the text "No wrong goes at any caution". | Fig. 2 still has no (a)/(b) panel labels (Phase 1 R3-11). |
| Q7-11 | resolved | Fig. 2 caption: "The IMM's share is measured against its own class average, F0 (IMM), drawn dashed"; the legend shows IMM solid and F0 (IMM) dashed. | Nothing. |
| Q7-12 | resolved | ACKNOWLEDGMENT first sentence has a verb ("The author conceived the study …"). | Nothing. |
| Q7-13 | partly resolved | "SHA-256" and "CARLA" expanded (IV-E, I); F0, N, E first appear inside Table 1 itself. "CANMOT" is still not expanded in the body. | CANMOT (name; expanded only in [5]'s title). New: "NIS" appears in Table 1 before its definition in III-D (Phase 1 R3-10). |
| Q7-14 | resolved | Page 11: "younger than 1 s." sits on one line. | Nothing. |
| Q7-15 | resolved | V-E: "(lead braking, this mask law, and this output rule only)". | Nothing. |
| Q7-16 | not resolved (form only) | Page 1: "Independent Researcher, Troy, MI, USA (ORCID: …)". | Add the ZIP code (template l. 24 to 25). |
| Q7-17 | not resolved (advisory) | Section II, V-D and VI still use bold or italic run-in lead-ins. | Advisory; keep or convert. |
| Q7-18 | not resolved (conditional) | The supplement is a separate document with title-case headings ("S1. Configuration", `sup01`), "TABLE S1." captions, and "S" numbering; it is not typeset in the template. | Applies only if the supplement is typeset in the template; otherwise none. |
| Q7-19 | partly resolved | Page 1 now has the drop-cap first paragraph. No biography. | Biography is production-stage and optional at submission (advisory). |

## Counts

- **R-1 to R-19 (19 items):** resolved 17 (R-1 to R-11, R-13 to R-18); partly resolved 2 (R-12, R-19); not resolved 0.
- **Q7-1 to Q7-19 (19 items):** resolved 11 (Q7-2, 3, 4, 5, 8, 9, 10, 11, 12, 14, 15); partly resolved 4 (Q7-1, 6, 13, 19); not resolved 4 (Q7-7 advisory, Q7-16 form only, Q7-17 advisory, Q7-18 conditional).

## Where an earlier item asked for something wrong or unnecessary

- R-3's request to restore "as point values" in VII is unnecessary now that VII makes no equivalence claim.
- Q7-1 on "multi-object": the template says "usually" without a hyphen; the field's standard compound is hyphenated, so this is a style call, not an error.
- Q7-18 (supplement headings) is moot while the supplement is a separate document.
- Q7-19 (biography): optional at submission, and the brief says treat as advisory.
- R-18's added references were not verifiable by me (no web); I did not check them.

## Noted after Phase 1 (Phase 1 left unchanged)

- Phase 1 missed Q7-1's "multi-object" hyphenation: my prefix search printed it and I did not report it. It would be an eleventh Q7 miss (template l. 195, advisory in strength).
- Everything else in the earlier list that I did not raise in Phase 1 was either already fixed or advisory.
- The earlier panel's REQUIRED items were wording and moves of existing values; none overlaps my two REQUIRED-major findings (practical bottom line, closed-loop baseline and cost), which the earlier panel did not ask for.
