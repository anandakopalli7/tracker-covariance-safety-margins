Phase 1 file SHA-256: ced74a7527c207c8a41e2f702dd3990076cbb59a76b5952b3d9837318f8d9976 (`phase1\03_r2_domain.md`, hashed at 18:54:41 EST and not changed after)

# Author-round v13 panel, Phase 2: seat R2, check of the earlier panel's REQUIRED items

## Header
- **Seat:** R2, Peer Reviewer 2 (Domain). **Model:** Claude Opus 5.5 (`claude-opus-5-5`). **Card:** "Card 3: Peer Reviewer 2 (Domain)" (`review_v13_output\00_phase0_field_analysis_and_cards.md`). Card-confirmation pause not held (non-interactive run).
- **Source opened only after Phase 1 was written and hashed:** `work\earlier_required_R1_R19_and_Q7.md`, SHA-256 13f24cd5ee3dae2eeddda3472e0bda371d0e3ed565185f71534a2f5e6fa211ce (18:55 EST).
- **Text checked:** the 18:30 package. Hashes at start of Phase 2 (18:55) and at end (18:56) are the same as in Phase 1: MANUSCRIPT_v13.md 29125167…51d0; MANUSCRIPT_v13.tex bd4d08d9…1345; SUPPLEMENT_v13.md fab98c1f…9a09; MANUSCRIPT_v13.pdf 4fabfd9f…8299; SUPPLEMENT_v13.pdf a8ad3602…6b16 (full values in the Phase 1 header).
- **Pages viewed:** the same as Phase 1 (`pages\page01.png` to `page13.png`, `pages_supplement\sup01.png`, `pages_template\tpl01.png`); no new images.
- Locations below are in the 18:30 text. Phase 1 is unchanged; anything this list showed me that Phase 1 missed is under "Noted after Phase 1".

## Verdicts

| ID | Verdict | Evidence from the 18:30 text (location) | What remains |
|---|---|---|---|
| R-1 | Resolved | V-E: "its factors (0.216, 0.107, and 0.065 for the first, second, and third missed update; 0.925 after reacquisition) are the median ratios of the covariance margin's critical scale to the class average's, relative to steady decisions, fitted on the 105 earlier runs"; "a level effect that needs no per-decision covariance"; "10 Hz … was not compared with a coast-count margin". "Instead of through the covariance" is gone from VI. | Nothing of the item. My Phase 1 R2-m3 adds that the 10 Hz class average is the 2 Hz one, which the text does not say. |
| R-2 | Resolved | V-E and Table 6: "0.210 [0.158, 0.255] (99% interval) around misses and 0.093 [0.066, 0.116] over all pairs"; abstract: "the fixed-noise tracker's spread ranks the realized error weakly around missed detections". VII no longer states the mechanism result. | Nothing of the item (class composition of the pairs: my R2-m5). |
| R-3 | Resolved | V-E: "(2.8%, 3.0%, and 2.2%) are, as point values, inside the paper's ±5% equivalence margin … At start probabilities 0.20 and 0.30 the dropout share is about 5%". VII says only "recovered a few percent of the room", so it makes no margin claim needing "as point values". | Nothing. |
| R-4 | Resolved | V-E: "This share holds for the position–velocity interface (Section III-D) only; a wider interface was not tested."; VI Limits: "holds for that interface only (a wider interface was not tested) and is no verdict on maneuver-adaptive covariances". "A lower bound" is gone. | The fix asked for was made, but I judge it insufficient: the margin omits process noise over the look-ahead and the maneuver mode is a CA filter whose acceleration is dropped, and the abstract and VII carry no qualifier (my R2-M2). |
| R-5 | Resolved | Abstract: "with a constant-velocity prediction"; VI: "The room itself lies almost wholly in braking (Table 3: 1.63, 23.62, and 0.08 points …): there the error is mainly that of the predicted mean path"; Limits: "whether a covariance adds anything on top of the braking prediction's path was not tested"; VII next steps: "a covariance added to a braking prediction's path". | Nothing of the item (planner scope in the abstract: my R2-m8). |
| R-6 | Resolved | IV-E: "The original lead-braking sequence, which is not Holm-adjusted, is room; …"; "six primary hypotheses are Holm-adjusted (the H rows of Table 6): the dropout replication, the slope …, the two-noise IMM's class, the adaptive filter's twin replication, the closed loop with dropouts, and the nuScenes mechanism check". | Nothing. |
| R-7 | Resolved | Table 6: "failed, Holm 0.99"; "failed, Holm 0.18"; caption: "Holm: Holm-adjusted one-sided p within the third amendment's two tests"; V-E: "the third amendment's two fail under their own Holm adjustment as well (adjusted p 0.99 and 0.18; Table 6)". | Nothing. |
| R-8 | Resolved | Abstract: "Where it is nearly constant it adds nothing … In three lead-braking tests where it varies, it recovers 2% to 5% of the room: 2.8% …, 2.2% …, and 4.6% … A margin that only counts missed updates reproduces the dropout gain"; contribution 2 adds "replicated against its permuted twin"; VII is now written for a designer and does not repeat the abstract in order; abstract 245 words. | Wording of the dropout clause (my R2-m2) and the interface qualifier (my R2-M2). |
| R-9 | Resolved | Abstract: "Plans were hash-locked internally; amendment tests followed the first results." Title unchanged. | Nothing. |
| R-10 | Resolved | V-E: "An exploratory decomposition (R² 0.47; decision-level R² 0.06; Supplement S15) attributes 54% … to the update schedule, 38% to the geometry, and 8% to the realized error: by this exploratory reading it varies there mostly for other reasons"; the abstract, contribution 2 and VII drop the clause. | Nothing. |
| R-11 | Resolved | ACKNOWLEDGMENT: recount "every value printed in the main text and all but the marked (‡) values of the supplement" (same as IV-E); "Claude (Anthropic; models Opus 5.5, Fable 5.2, and Sonnet 5.5) … drafted and revised the text of all sections"; opens "The author conceived the study, …" (has a verb); AI-panel sentence kept: "the presubmission review by an AI panel". | S12's first sentence still states a narrower recount scope, and S12 does not name the auditing models the ACKNOWLEDGMENT names (my R2-m12, Q8). |
| R-12 | Partly resolved | IV-E: "The three amendments were written and locked on Nov. 21 and 22, 2026 (file times in Table S29), each after a report of an artificial intelligence (AI) review panel …, and the third's two controls were asked for by that panel (Table S5)." ACKNOWLEDGMENT: "made every scientific decision" and, later, "where the amendment files record a design choice as an AI session's, it was made within the author's approval". | The IV-E sentence is in. The author's own paragraph now says "made every scientific decision" while also saying the files record some design choices as an AI session's (and Table S5 says "the domain seat asked for the coast count"); "approved every scientific decision" or similar would remove the tension, if true. |
| R-13 | Resolved | III-A: "a pedestrian walks across the ego's lane from a drawn side at a drawn speed of 1 to 3 m/s, starting so that it would reach the ego's path together with an ego that keeps its desired speed, after a drawn 1 to 4 s … The planner treats the pedestrian like any other actor, predicted at constant velocity. The study recorded 390 runs … after a check on 51 stored runs (step 0) had shown little room … many crossing decisions have no binding constraint at any margin scale". | One gap: "each case also carries an occluder flag" is not explained anywhere (what occludes, and how). |
| R-14 | Resolved | III-B: "Time lost is the run's duration minus the distance traveled divided by the desired speed, for runs without contact; the rest gap is the gap to the stopped lead at the end of the run." | Nothing. |
| R-15 | Resolved | V-E: "a window starts with probability 0.10 (the primary start probability; on the new runs it masks 16.2% of updates) … the class average is computed under the same masks and output rule on the tuning runs (the dropout-estimated class average)". | Nothing. |
| R-16 | Resolved | V-E: "read by linear interpolation between scales 4 and 8 of its frontier at scales 4, 8, and 16 on the same cases, is 25.7% against the covariance arm's 20.7%; time lost is taken over the 89 of 135 cases without contact in any arm and lies between 25.24 and 25.84 s"; Table 6 gives the four frontier points. | Nothing (rest-gap version: my optional R2-o7). |
| R-17 | Resolved | Table 2 caption: "shares with 95% intervals, except N's share (99.4%, calibrated) and the IMM's share (99%, nominal)". The abstract states no level. | Nothing. |
| R-18 | Partly resolved | II: "With fixed noise and under regular updates, a Kalman filter's covariance settles to a steady state [26]. With intermittent observations it follows the arrival sequence instead, and there is a critical arrival rate beyond which the expected covariance is unbounded [27]"; "Filters that account for data-association uncertainty [28] … detectors that estimate their own uncertainty [29]"; threat assessment [35], [36]; misdetection-aware MPC [19]. | [27] is misstated ("beyond" should be "below", and its critical rate does not bear on a constant-velocity model with three-update coasting: my R2-m1); [19]'s 66% is not reconciled with the ~3% here (R2-m6); existence-probability tracking and the threat-assessment and IMM-for-ACC works in the paper's own search are uncited (R2-m7). |
| R-19 | Partly resolved | See Q7-1 to Q7-19 below: 11 resolved, 5 partly, 3 not (all three I judge unnecessary). | "multi-object" hyphen, NIS before its definition, corporate authors of [43] and [44], "et al." author counts to check, and the optional or conditional items. |

### R-19, item by item

| Q7 item | Verdict | Evidence from the 18:30 text (location) | What remains |
|---|---|---|---|
| Q7-1 | Partly resolved | "presubmission", "nonbraking", "retuned", "Redetected", "prestated", "rescore" are now joined (ACKNOWLEDGMENT, III-A, V-D, V-E). "multi-object" stays in the abstract, I (twice) and II "Novelty". | Join "multiobject" (template lines 195 to 197); reference titles keep their own spelling. |
| Q7-2 | Resolved | VII: "For a designer, three things follow. …" is organized by design consequence, not in the abstract's order. | Nothing. |
| Q7-3 | Resolved | [26]: "New York, NY, USA: Wiley, 2001"; [42]: "Geneva, Switzerland: ISO, 2018"; the earlier [37], [38] now point to journal articles. | Nothing. |
| Q7-4 | Resolved | The one web source, [4], has "commit 54c1dab, May 2024. Accessed: Nov. 22, 2026." | Nothing. |
| Q7-5 | Partly resolved | [43]: "Oct. 30, 2020"; [44]: "Mar. 9, 2021" (month first); the free-text tails are gone. | [43] and [44] still open with the title and no corporate author, while [45] has "UNECE"; give them a consistent author. |
| Q7-6 | Resolved | Conference references now share one form without city or month (for example [1] "in *Proc. IEEE Intell. Veh. Symp. (IV)*, 2018, pp. 1171–1178"). | Nothing. |
| Q7-7 | Partly resolved | "et al." after one name remains in [9], [13], [15], [21], [34]. The template itself shows "et al." in its example (lines 864 to 867), and IEEE practice uses it above six authors. | The author should check that [13] and [15] have more than six authors (I cannot check offline); [9], [21], [34] have more by my unverified memory. |
| Q7-8 | Resolved | II: "IMM estimators [7], [8], [22]". | Nothing. |
| Q7-9 | Resolved | Fig. 4 (p. 9): "(a)" and "(b)" centered below each panel, not bold. | Nothing (Fig. 2 has no sub-figure labels at all: my Phase 1 Q7 miss 3). |
| Q7-10 | Resolved | Fig. 2 right panel (p. 7) has axis labels "Wrong goes (% of decisions)" and "Caution (% of desired speed)" and the note "No wrong goes at any caution". | Nothing. |
| Q7-11 | Resolved | Fig. 2 caption: "The IMM's share is measured against its own class average, F0 (IMM), drawn dashed."; legend: IMM solid, "F0 (IMM)" dashed. | Nothing. |
| Q7-12 | Resolved | "Generative AI was used and is disclosed here under IEEE policy." has a verb, and the paragraph opens with "The author conceived the study …". | Nothing. |
| Q7-13 | Partly resolved | "256-bit Secure Hash Algorithm (SHA-256)" (IV-E); "CARLA (Car Learning to Act)" (I); Table 1 now sits in Section I (p. 2) before F0, N and E are used. | "NIS" now appears in Table 1 (p. 2) before III-D defines it (p. 4): my Phase 1 Q7 miss 2. |
| Q7-14 | Resolved | p. 11, Limits: "younger than" ends a line and "1 s." begins the next, number and unit together. | Nothing. |
| Q7-15 | Resolved | V-E: "(lead braking, this mask law, and this output rule only)". | Nothing. |
| Q7-16 | Not resolved | First page: "Independent Researcher, Troy, MI, USA (ORCID: 0009-0002-5241-9922)"; template line 24: "Boulder, CO 80305 USA". | Form only. I consider it unnecessary: a ZIP code adds nothing for an independent researcher, and production sets the form. |
| Q7-17 | Not resolved | II and VI keep bold run-in heads ("Novelty, with its limits.", "Which commitment applies."). | Advisory; I consider it unnecessary, since run-in paragraph heads are common in published IEEE papers and break no template rule I can find. |
| Q7-18 | Not resolved | Supplement headings stay in title case ("S1.1. Planner Rows and Margin Projection"). | Conditional only; the supplement is typeset outside the template (sup01.png), so I consider it unnecessary. |
| Q7-19 | Partly resolved | Drop cap now present ("A MULTI-OBJECT tracker reports", p. 1). | No author biography; optional at submission (brief), advisory. |

## Counts
- R-1 to R-19: **resolved 16, partly resolved 3 (R-12, R-18, R-19), not resolved 0**.
- Q7-1 to Q7-19 (within R-19): resolved 11 (Q7-2, 3, 4, 6, 8, 9, 10, 11, 12, 14, 15), partly 5 (Q7-1, 5, 7, 13, 19), not 3 (Q7-16, 17, 18).

## Earlier items I think wrong or unnecessary
- **Q7-16, Q7-17, Q7-18:** unnecessary in my view (form of an independent researcher's address; common run-in heads; supplement not typeset in the template).
- **Q7-7:** the template's own example uses "et al." (lines 864 to 867), so this is a check of author counts, not a miss.
- **R-4:** not wrong, but insufficient: "a wider interface was not tested" leaves out that the margin carries no process noise over the look-ahead and that the maneuver mode's acceleration is discarded (my R2-M2).

## Noted after Phase 1
These come from the earlier list and are not in my Phase 1 report, which stays as written:
1. **Q7-5:** [43] and [44] have no corporate author while [45] has "UNECE" (reference consistency).
2. **Q7-7:** whether [13] and [15] have more than six authors; I accepted "et al." in Phase 1 without checking counts.
3. **R-12:** the tension between "made every scientific decision" and "where the amendment files record a design choice as an AI session's" in the ACKNOWLEDGMENT; Phase 1 (Q8) addressed only the second sentence's wording.
4. **R-13:** the "occluder flag" in III-A is never explained (found while checking R-13).
