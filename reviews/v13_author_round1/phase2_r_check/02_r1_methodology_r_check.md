Phase 1 file `phase1\02_r1_methodology.md`, SHA-256: 47f9bbce10c4e6598bccea8e5e74121e149d7b35ed30fa8227741eaae534d0c6 (computed before this file's source was opened; the Phase 1 file was not changed afterward).

# Phase 2: check of the earlier panel's required items R-1 to R-19, seat R1 (Peer Reviewer 1, Methodology)

## Header

- **Seat:** R1, Peer Reviewer 1 (Methodology). **Model:** Claude Fable 5.2 (`claude-fable-5-2`). **Card:** "Card 2: Peer Reviewer 1 (Methodology)" of `review_v13_output\00_phase0_field_analysis_and_cards.md`, anchors re-pointed as in Phase 1. **Card-confirmation pause not held** (non-interactive run).
- **Source of the items:** `work\earlier_required_R1_R19_and_Q7.md` (items of a panel on the 12:01 freeze, 12 pages), opened only after the Phase 1 hash above was recorded.
- **Text checked (the 18:30 package), SHA-256 at the start of Phase 1 and at the end of Phase 2, identical:**

| File | SHA-256 (start = end) |
|---|---|
| `MANUSCRIPT_v13.md` | 29125167b108bc27833c16e3b639cbb07af5f4c105c49d375deff3d5b4a951d0 |
| `MANUSCRIPT_v13.tex` | bd4d08d954d3595de2b5ac2653c18476c7bb3281e1c264604f995f018da01345 |
| `SUPPLEMENT_v13.md` | fab98c1fe24c8c5b95f86da8b1e664662401055232409a236d963938f5b99a09 |
| `MANUSCRIPT_v13.pdf` (not opened) | 4fabfd9f611013fd4e7f60b8a59fcdcc2d782dbd3192a77c2efe54e77beb8299 |
| `SUPPLEMENT_v13.pdf` (not opened) | a8ad36027dee70c8c48cf2b998cb2512b55ca568c400eb1ecd340923ddeb8b16 |

- **Page images viewed (both phases):** manuscript pages 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13; template page `tpl01.png`; supplement page `sup01.png` (viewed in Phase 2 for Q7-18). Pages 4 and 5 were judged from the .tex and .md.
- No web, no sub-agent, no other seat's file, nothing changed outside my two output files.

## Verdicts on R-1 to R-19

| ID | Verdict | Evidence from the 18:30 text (location) | What remains |
|---|---|---|---|
| R-1 | **Resolved** | Section V-E: "its factors (0.216, 0.107, and 0.065 for the first, second, and third missed update; 0.925 after reacquisition) are the median ratios of the covariance margin's critical scale to the class average's, relative to steady decisions, fitted on the 105 earlier runs"; "a level effect that needs no per-decision covariance"; "10 Hz … was not compared with a coast-count margin". Section VI no longer has "instead of through the covariance". All four factors match the export (0.2165, 0.1065, 0.0647, 0.9250). | Nothing from the item. Beyond it: "as much" understates a control that did slightly better (my Rm-2), and "level effect" lacks "at 2 Hz" in Sections I, VI and VII (my Rm-3). |
| R-2 | **Resolved** | Section V-E: "For the IMM (secondary) … 0.210 [0.158, 0.255] (99% interval) around misses and 0.093 [0.066, 0.116] over all pairs (descriptive)"; Table 6 row "same, IMM (secondary)"; abstract: "the fixed-noise tracker's spread ranks the realized error weakly". Section VII no longer cites the mechanism check, so the wording is not needed there. Values match the export. | Nothing. |
| R-3 | **Resolved** | Section V-E: "(2.8%, 3.0%, and 2.2%) are, as point values, inside the paper's ±5% equivalence margin … At start probabilities 0.20 and 0.30 the dropout share is about 5%"; abstract: "2.8% under random detection dropouts (replicated; about 5% at higher rates)". Section VII now says "a few percent of the room" and makes no margin claim. | Nothing. |
| R-4 | **Resolved** | Section V-E: "This share holds for the position–velocity interface (Section III-D) only; a wider interface was not tested."; Section VI Limits: "holds for that interface only (a wider interface was not tested)". "Lower bound" is gone. | Nothing. |
| R-5 | **Resolved** | Abstract: "with a constant-velocity prediction"; Section VI: "The room itself lies almost wholly in braking (Table 3: 1.63, 23.62, and 0.08 points …) … which a fixed-noise covariance has no way to track"; Limits: "whether a covariance adds anything on top of the braking prediction's path was not tested"; Section VII lists "a covariance added to a braking prediction's path". | Nothing. |
| R-6 | **Resolved** | Section IV-E: "The original lead-braking sequence, which is not Holm-adjusted, is room; detection …"; "six primary hypotheses are Holm-adjusted (the H rows of Table 6): the dropout replication, the slope …, the two-noise IMM's class, the adaptive filter's twin replication, the closed loop with dropouts, and the nuScenes mechanism check". The six agree with AMENDMENT_12 §4 and `A12_HOLM_v01.json`. | Nothing. |
| R-7 | **Resolved** | Table 6: "failed, Holm 0.99" and "failed, Holm 0.18"; caption: "Holm: Holm-adjusted one-sided p within the third amendment's two tests". Both values match `A13_HOLM_v01.json` (0.9856, 0.1756). | Nothing. |
| R-8 | **Resolved** | Abstract: "Where it is nearly constant it adds nothing … In three lead-braking tests where it varies, it recovers 2% to 5% of the room: 2.8% …, 2.2% …, and 4.6% … A margin that only counts missed updates reproduces the dropout gain". Section VII opens "For a designer, three things follow" and does not repeat the abstract's order. Abstract: 245 words by the build's count. | Nothing from the item. I think the item's own wording "matches" is slightly soft: the coast-count margin did slightly better (interval below zero). The permuted twin named in the item is still undefined (my RM-1). |
| R-9 | **Resolved** | Abstract: "Plans were hash-locked internally; amendment tests followed the first results." | Nothing. |
| R-10 | **Resolved** | The clause is gone from the abstract, Section I and Section VII. Section V-E: "An exploratory decomposition (R² 0.47; decision-level R² 0.06; Supplement S15) attributes 54% of its explained variation to the update schedule, 38% to the geometry, and 8% to the realized error: by this exploratory reading". Values match the export. | Nothing. Section VII's "recovered nothing of a small room" is a new overreach (my Rm-4). |
| R-11 | **Resolved** | ACKNOWLEDGMENT: "Generative AI was used and is disclosed here under IEEE policy." (has a verb); "Claude (Anthropic; models Opus 5.5, Fable 5.2, and Sonnet 5.5) wrote the analysis … and drafted and revised the text of all sections" (Fable 5.2 no longer limited to "revised"); "recount every value printed in the main text and all but the marked (‡) values of the supplement; the two sets share the scoring library, stored arrays, and resample draws (Section IV-E)"; the AI-panel sentence is kept. | "every value" should be "every result value" (my Rm-7). |
| R-12 | **Partly resolved** | Done: Section IV-E: "The three amendments were written and locked on Nov. 21 and 22, 2026 (file times in Table S29), each after a report of an artificial intelligence (AI) review panel on the text before it, and the third's two controls were asked for by that panel (Table S5)." The lock files I read agree (LOCK_A11 21 Nov 14:23 to LOCK_A13c 22 Nov 06:48). Not done: the ACKNOWLEDGMENT now says "made every scientific decision", which is stronger than the earlier "made the scientific decisions", not weaker. A qualifying clause was added: "where the amendment files record a design choice as an AI session's, it was made within the author's approval". | The first sentence still claims more than the deposit supports (AMENDMENT_13 §3.0: "Whose decision: the coordinator's"). The paragraph is the author's own; the fix is his to confirm: "made or approved every scientific decision" (my RM-2). |
| R-13 | **Resolved** | Section III-A: "In *pedestrian crossing* (first amendment; Section V-E), a pedestrian walks across the ego's lane from a drawn side at a drawn speed of 1 to 3 m/s, starting so that it would reach the ego's path together with an ego that keeps its desired speed … The planner treats the pedestrian like any other actor, predicted at constant velocity. The study recorded 390 runs, 130 per desired speed, after a check on 51 stored runs (step 0) had shown little room (0.08 [−0.06, 0.25] points): many crossing decisions have no binding constraint at any margin scale". | Nothing. (Section I still lists pedestrian crossing under "a plan fixed in advance": my Rm-1.) |
| R-14 | **Resolved** | Section III-B: "Time lost is the run's duration minus the distance traveled divided by the desired speed, for runs without contact; the rest gap is the gap to the stopped lead at the end of the run." | Nothing. |
| R-15 | **Resolved** | Section V-E: "a window starts with probability 0.10 (the primary start probability; on the new runs it masks 16.2% of updates)"; "the class average is computed under the same masks and output rule on the tuning runs (the dropout-estimated class average)". 16.2% matches the export (0.16198). | Nothing. |
| R-16 | **Resolved** | Section V-E: "read by linear interpolation between scales 4 and 8 of its frontier at scales 4, 8, and 16 on the same cases, is 25.7% against the covariance arm's 20.7%; time lost is taken over the 89 of 135 cases without contact in any arm and lies between 25.24 and 25.84 s for the four arms". All match the export. | Nothing from the item. The population mixing is not named as a limit (my O-2); no figure (my O-1). |
| R-17 | **Resolved** | Table 2 caption: "shares with 95% intervals, except N's share (99.4%, calibrated) and the IMM's share (99%, nominal)". Levels match the export (0.994 calibrated; 0.99 nominal). | Nothing. |
| R-18 | **Resolved** (references not verified by me; no web) | Section II: "With fixed noise and under regular updates, a Kalman filter's covariance settles to a steady state [26]. With intermittent observations it follows the arrival sequence instead, and there is a critical arrival rate … [27]; the coast-count result of Section V-E is consistent with that dependence"; "Filters that account for data-association uncertainty [28]"; "Closed-form distributions of criticality measures under state-estimation and prediction uncertainty [35] … worst-case analysis [36]". | The author must still confirm the added references' details; I could not check them offline. |
| R-19 | **Partly resolved** | See the Q7 table below: 13 of 19 resolved, 2 partly, 1 unchanged and to be checked by the author, 3 unchanged that I judge unnecessary or not applicable. | "multi-object" (Q7-1); the "et al." author counts (Q7-7); no biography (Q7-19). |

**Counts: resolved 17 (R-1 to R-11, R-13 to R-18); partly resolved 2 (R-12, R-19); not resolved 0.**

## R-19: the Q7 list, one by one

| ID | Verdict | Evidence from the 18:30 text | What remains |
|---|---|---|---|
| Q7-1 | Partly | "presubmission", "nonbraking", "retuned", "redetected", "prestated", "rescore" are now joined (search of the .md finds no "pre-", "non-", "re-" prefix forms). | "multi-object" remains four times in running text (abstract; Section I twice; Section II). Template lines 195 to 197. |
| Q7-2 | Resolved | Section VII: "For a designer, three things follow …"; it has one number in common with the abstract (78%) and a different order. | Nothing. |
| Q7-3 | Resolved | [26]: "New York, NY, USA: Wiley, 2001"; [42]: "Geneva, Switzerland: ISO, 2018". | Nothing. I think a place of publication is unnecessary for the IEEE standard [41]. |
| Q7-4 | Resolved | [4]: "commit 54c1dab, May 2024. Accessed: Nov. 22, 2026. [Online]. Available: …". | Nothing. |
| Q7-5 | Resolved | [43]: "*Off. J. Eur. Union*, L 360, pp. 66–89, Oct. 30, 2020."; [44]: "L 82, pp. 75–137, Mar. 9, 2021."; no free-text tails; [45] has the author "UNECE". | Nothing. Title-first entries for [43] and [44] are acceptable for a regulation. |
| Q7-6 | Resolved | No conference reference carries a city or month now; the form is the same throughout ([1], [3], [6], [9], [11] to [14], [18], [20], [21], [23], [31], [35]). | Nothing. |
| Q7-7 | Not resolved (author to check) | "et al." stays in [9], [13], [15], [21], [34]. | Confirm that each has more than six authors; cannot be checked offline. |
| Q7-8 | Resolved | Section II: "IMM estimators [7], [8], [22]". | Nothing. |
| Q7-9 | Resolved | Page 9: "(a)" and "(b)" are centered below each panel in Roman type. | Nothing. |
| Q7-10 | Resolved | Page 7, Fig. 2 right panel: axis labels "Wrong goes (% of decisions)" and "Caution (% of desired speed)", with the note "No wrong goes at any caution". | Nothing. |
| Q7-11 | Resolved | Fig. 2 caption: "The IMM's share is measured against its own class average, F0 (IMM), drawn dashed"; the legend shows F0 (IMM) dashed. | Nothing. |
| Q7-12 | Resolved | "Generative AI was used and is disclosed here under IEEE policy." | Nothing. |
| Q7-13 | Resolved | Section IV-E: "hashes of the 256-bit Secure Hash Algorithm (SHA-256)"; Section I: "the CARLA (Car Learning to Act) simulator"; Table 1 is now on page 2, before F0, N and E are used in running text. | A new miss of the same kind: "NIS" appears in Table 1 before its definition in Section III-D (Phase 1, answer 7). |
| Q7-14 | Resolved | Page 11: "… from a track younger than / 1 s." The number and its unit are on one line. | Nothing. |
| Q7-15 | Resolved | Section V-E: "(lead braking, this mask law, and this output rule only)". | Nothing. |
| Q7-16 | Unchanged; I judge it unnecessary | First page: "Independent Researcher, Troy, MI, USA (ORCID: …)". | An independent researcher has no institutional address; "City, ST, Country" is the IEEE reference form for places and is fine here. |
| Q7-17 | Unchanged; advisory; I judge it unnecessary | Bold run-in headings remain in Sections II and VI. | None. They are paragraph leads, not headings, and help a dense text. |
| Q7-18 | Not applicable | `sup01.png`: the supplement is typeset as a plain single-column document, not in the journal template, so the heading-case rule does not apply. | None. |
| Q7-19 | Partly; advisory | Page 1 now has the drop-cap first paragraph. | No author biography (optional at submission). |

## Noted after Phase 1

Points in the earlier list that my Phase 1 report did not raise. Phase 1 is unchanged.

1. **Q7-7 ("et al." author counts).** I did not check whether [9], [13], [15], [21] and [34] have more than six authors. It cannot be checked offline; the author should confirm.
2. **Q7-16 and Q7-17.** I saw both and did not count them as misses; I still would not.
3. **R-18's reference details.** I checked the forms of the added references ([27], [28], [33], [35], [36]) and not their bibliographic facts.
4. **Agreement with Phase 1.** The earlier R-12 and my RM-2 are the same point; the 18:30 text made the first sentence stronger while adding the qualifying clause. The earlier R-8 named the permuted twin without asking for its definition; my RM-1 is new. No earlier item contradicts a Phase 1 finding, and none leads me to change the Phase 1 recommendation or score (I am not permitted to, and would not).
