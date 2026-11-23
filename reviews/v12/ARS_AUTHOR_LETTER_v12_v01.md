# Review Letter

## Decision

The decision is Major Revision.

All four reviewers who judged the paper as a whole recommend Major Revision, and the Devil's Advocate's main objection was upheld. The objection: the one confirmatory result is the null that a fixed-noise filter's steady state predicts, while everything with discriminating content is exploratory and moves between the two run sets.

The arithmetic holds, the paper is unusually candid, and the topic fits the journal. What blocks acceptance:
- the reach of the confirmatory result;
- the scope of the positive control;
- the status of the numbers a reader will quote;
- the length.

None of this is fatal, and much of it can be met offline from the stored detections or by narrower wording.

## Strengths

- The evaluation design gives a null a fair hearing. Decisions are scored against the logged future at equal caution, with an oracle margin as positive control, perfect oracles for each scoring, and graded oracles whose failures are reported.
- Interval validity is measured rather than assumed. A double bootstrap shows where nominal intervals fail. A grid placebo, a grid-offset family and a gridless frontier separate the 1.10 offset from information.
- The ratio of the tracker's margin to the class-average margin needs no ground truth, is cheap to reproduce, and comes with its stated reach: nearly constant in lead braking, stopped-vehicle and cut-in runs, silent in crossings.
- The lesson that an open-loop decision score depends on its commitment and its population is useful beyond this tracker. The reaction-time sweep makes it concrete.
- The steady-state account is correct from a tracking standpoint, and every figure the reviewers traced reconciles with its table. The reviewers recomputed about fifteen conversions and traced every number in the abstract, introduction and conclusion. No mismatch affects a claim.
- The paper says plainly that the analyses added after the first results are exploratory, that part of the literature was read from abstracts only, and that the second programs share code and arrays with the first.
- Reliance on the stop is counted, not ignored, and the regulation values are used as nominal reference parameters with no compliance claim.

## Required Changes

**What the paper claims, and how it is framed**

1. [Abstract; §I contributions; §VII] As written, the paper offers several conditional readings and no single take-away, and the confirmatory result is a null the paper itself calls expected. Decide the one take-away and lead with it. The reviewers suggest re-centring the paper on the evaluation protocol and on what an open-loop decision score depends on, with the tracker null as its worked example. Do not present exploratory results as co-equal claims.
2. [Title; §V-B heading; Table I; Abstract; §I contribution 3] No margin source uses a covariance that varies with the lead's motion. The one adaptive source, NIS inflation, can only inflate, and it changes the critical values in 217 of 8,290 decisions. So the study cannot show that its design would register a covariance that does vary. Add one such arm, re-run offline on the stored detections: for example, a constant-velocity/constant-acceleration IMM, or a fading-memory or innovation-adaptive process noise on the velocity block. A scenario family in which the margin ratio varies, such as crossings or track births, would also serve. If you do not add one, rename the NIS-inflated source as an output-scalar inflation, change the §V-B heading and the Table I label, and state in the abstract and contributions that no covariance-varying tracker was tested.
3. [Whole manuscript; Supplement] The main text (12,451 words) and the supplement (34,240 words) are far beyond the journal's 10-page recommendation, and a reader must open about forty supplement items to follow the argument. Bring the main text toward 10 pages: move interval mechanics, resolution rules, hash strings, the 2 m gap paragraph and most decision-equivalent detail to the supplement. Cut the supplement to what the main text needs; the closed-loop check and the deviation check can go unless used. Give a typeset page count.
4. [Abstract; §I; §VII; Tables II–V] Several numbers in the abstract, introduction and conclusion appear in no main-text table: the held-out per-phase shares, the calibrated room interval, the 2.2-decision figure, the 83% after-stop decision share and the range of the 12%. Either add one main-text table for them (the exploratory per-phase results, labelled as exploratory) or take them out of those three texts.

**Inference and design**

5. [§IV-B; §V-A; Tables S12, S38] The sentence that concludes “the null of Section V-A is not a blunt measure” rests on grading shown only pooled and after the stop. There the room is largely an allocation of caution between phases, and the mixture oracles are far larger in amplitude than the tracker's 2–5% variation. Phase-weighted and before the stop, the mixtures score below the class average. Limit the sentence to where the control grades. Add one test of the measure at the tracker's scale: an oracle rank-matched to the realised error but compressed into the observed ratio range of about ±5%, or the graded-oracle check repeated on the per-phase-scale frontier. State the criterion for grading before you compute it.
6. [§IV-B; §V-A; Tables S16, S30–S31c] The inference for the tracker covariance's share has no single stated estimand. The grid statistic stays primary although the paper shows it to be a grid artefact. The placebo contrast and the gridless interval are uncalibrated, and no equivalence margin is given. Name the estimand before any interval (the gridless or a smoothed frontier). Give one calibrated interval for it and for the contrast with the placebo, fix an equivalence margin from stakes, and report against it. Present the 2.2-decision figure as a descriptive range of interval ends, not as a bound.
7. [Abstract; §I; §V-C; Table S32] The abstract's held-out 90% and 99.9% are measured against a single scale chosen the same way on the other runs. Against the single-scale frontier that defines the room they are 0.868 and 0.964. No interval is given for the estimated-phase values, and 99.9% held out above 98.4% in sample shows a baseline effect. Report both bases or state the basis wherever these figures appear, give intervals for every held-out value, drop the third significant figure, and label the values exploratory in the abstract.
8. [Abstract; §I contribution 3; §III-A; §V-C] The evaluation runs have now steered several rounds of analysis, so no untouched confirmatory data remain. Yet the third contribution is titled “A measured confirmation of the steady state”, and the abstract's “On 35 runs not used to design the margins” does not say that the difference between the tracker and the class average had been viewed on those runs before the plan. Make the status plain in the abstract and the contributions. Preferably, generate fresh runs with new seeds from the same generator and run the final locked plan once, with the estimand, schedule and phase estimator fixed in advance. Otherwise, apply the schedule chosen on the evaluation runs to the tuning runs, and the reverse, as a transfer test, or take the allocation claim out of the headline.
9. [§VI Limits; Abstract last sentence; Table S35] The sentence that says “only comparisons between sources on the same decisions are meant to transfer” is contradicted by Table S35. Between the tuning and evaluation runs the braking prediction's share moves from 0.377 to 0.831, and the acceleration margin's share in the stopped phase from 0.063 to 0.702. Restrict the sentence to what both run sets support: the null for the tracker covariance, and any ordering that holds in both. Compute tuning-run intervals. A third recording policy, such as a time-gap recorder, is optional.

**Test-bed conditions behind the quotable numbers**

10. [§III-A; §V-C; §VI Limits] The room's location after the stop and the braking prediction's share rest on the tracker's velocity lag. That lag depends on the filter's noise setting, which is mis-tuned for this sensor (position NIS about 0.24 against 2). Re-run the tracker offline on the stored detections, once with noise set so that position NIS is near 2 and once with a constant-acceleration or IMM variant. Report the after-stop lag, the room by phase and the braking prediction's share. If you do not, add filter tuning to the conditions in Limits and to the conditions on the 83%.
11. [Abstract; §I contribution 2] The abstract says the braking prediction “recovers 83% of the room, open loop and off-policy”, without saying that every lead in every run brakes to a stop and that the prediction's cost behind a lead that does not brake is untested. Add both points to the abstract and to the second contribution.
12. [Abstract; §V-D; Table III; Table S28] The abstract's perfect stop “leaves 12% of it”, but that reading rests on two assumptions. First, the stop is perfect, free and independent of the perception being studied. State that in the abstract, and preferably add a scoring in which the stop starts from the tracker's own belief or after a stated delay. Second, the 6 m/s² stop exceeds every lead's realised deceleration (2.09–5.46 m/s²). Report the reaction-and-stop room by terciles of the lead's deceleration, or restrict the wording to leads braking at up to 5.5 m/s².
13. [Abstract; §III-A; §V-C] The room, the 83% and the 12% hold for a detector at 2 Hz with no latency and 0.5 s tracker steps, a rate far below that of production car-following stacks. Re-run detection and tracking on the 20 Hz recordings at 5 and 10 Hz with a stated latency, and report the room, the after-stop room and the braking prediction's share at each rate. If you do not, state in the abstract that all magnitudes hold for the 2 Hz, no-latency setting.

## Suggested Changes

14. [Abstract] Add one clause saying that the pooled 5.6 points and the 83% scale with how long recording continues after the stop (8.58 points without the after-stop decisions). Consider making the per-phase results the primary table.
15. [§II; Supplement S6; References] The novelty statement rests partly on abstracts (§II says “we did not read the full texts”) and on a narrow six-part conjunction. List the queries and engines in S6, and read the full texts of the closest threat-assessment items or restate the finding as an abstract-level observation. Add the tracking and car-following works the reviewers named: motion-model comparisons for vehicle tracking, an IMM survey, estimator-credibility measures, anticipation in microscopic traffic models, a string-stable CACC design, conformal-prediction planning and contingency planning.
16. [Abstract; Title] Make the abstract readable for a general ITS reader: three results, one defining sentence for the room and for a wrong go, fewer numerals. Consider a title that names the tested object rather than lead braking, since 83% of the decisions follow the lead's stop.
17. [§IV–§VII; Notation table; Table I] Reduce the number of labels and repeated hedges. State each fence once in Scope and once in Limits, and use established terms in running text.
18. [Table II; Fig. 2; §V-C] Use one labelled interval type per quantity: print the calibrated intervals in Table II for the room and the tracker covariance's share. Note on Fig. 2(a) that the tracker's mean lies outside its interval. Label which baseline each of 0.90, 0.88 and 0.87 uses.
19. [§IV-D; Supplement S4, S10, S11; Table S13 footnote] Write one provenance paragraph in the main text. Say that both earlier reviews were by AI review panels, which analyses were added in response, and that the second programs and recounts were AI sessions sharing code and arrays with the first. Replace the remaining uses of external review and of an independent reviewer in the supplement accordingly.
20. [Supplement S11; captions of Fig. S4 and Table S29] Remove or define internal identifiers: extraction and analysis labels, a local file path, a script name, and captions that refer to an earlier draft.
21. [Abstract; §I; §VII] Make the abstract, the contributions and the conclusion state the same claims in the same order. Give the 12% with its range (from 0.29 to 0.06 across 4 to 7.6 m/s² stops). Put the time-gap result in the abstract or drop it from the conclusion. Split §VII into findings and next steps.
22. [Abstract; §I; §VII] Use one wording for the 2.2-decision statement everywhere, with its scoring, its population and the fact that it was formed after the values were read.
23. [Supplement S10.9 and S11.8] Add a small hand-checkable subset: a few decisions whose true clearance is computed by a routine independent of the shared scoring library. Have the intervals behind the tracker covariance's share recomputed by a second program.
24. [§IV-B; Table S21] Report the room and the shares under caution windows that stop at 5%, 10% and 15%. Argue for the caution definition of record against the signed one, or report both in the main text.
25. [Table II] For populations in which the paper says the measure does not grade, print decision-equivalents rather than shares.
26. [§V-C; Tables S33, S33b, S34] Give a run-level breakdown of the 132 after-stop decisions that carry the room. Separate the state's staleness from filter smoothing, for example by scoring on the state at its own time stamp. Add intervals to these tables.
27. [§V-E; Table V; Supplement S10.7] Tabulate the margin ratio against heading offset and track age for the crossing and benign-driving families. Explain why benign driving reaches only 60.45% within 5%, and what happens in the evaluation run with ratios between 0.703 and 1.043. Report how often a ±5% change in the ratio would change the first feasible row.
28. [§I contribution 4; §V-E; Table V] The expectation that the null carries over to stopped-vehicle and cut-in runs rests on whole-run row shares. Support it with ratios in a window around the cut-in and by track age, or drop cut-in from the list.
29. [§III-A; Table S34b; Fig. S1] Give NIS and NEES per phase at update time, with run-level intervals and the truth at the state's time. Phrase the contrast with nuScenes as applying to stationary decisions.
30. [§V-C] The text gives “435.2 decision-equivalents with a tracker speed above 2 m/s” before the stop, but no table carries it, and the pre-stop total in Table S33 is 419.1. Add the table row and its complement so a reader can see that it is a partition.
31. [§VI; new runs] Add lead-following runs without a hard brake (constant speed, mild braking, stop and pull away), and report wrong goes and caution there for the braking prediction and the phase schedule.
32. [§VI Limits; new table] The Limits paragraph says “Wrong-go counts ignore impact speed.” Add one event-level table: runs with contact, and impact speed where there is contact, for the class average, the tracker covariance, the braking prediction and the time gap at two matched caution levels.
33. [Abstract; §VII] Carry the §VI sentence “It does not justify removing a covariance margin from a deployed stack” into the abstract and the conclusion, together with the cases it does not cover: crossing actors, young tracks and other road users.
34. [§IV-C; Supplement S3; Reference 42] Cite the adopted regulation text and its amendment status. Remove the sentences in Supplement S3 that read as a compliance comparison. Relate the 6 m/s² stop to the deceleration envelopes of emergency-braking and adaptive-cruise functions.
35. [§III-C; §V-B; Table S37] The time-gap margin was added after the first results and is scored as a competitor. Consider arms that add the tracker covariance (or the class average) to the time gap, and state the time-gap policy's headway range against adaptive-cruise practice.
36. [Supplement S3.4] Consider putting the planner's fallback share into the quoted closed-loop statement, or dropping the statement in regulation units from the supplement summary.
37. [Abstract; §V-C; §VII] Present the schedule on the tracker's own phase estimate as a diagnostic of where the room lies. Say that it is not a design result until tested on leads that stop and pull away or brake gently.
38. [§II; References] Relate the time gap, the stop deceleration and the lead decelerations to the standards and test protocols for adaptive cruise control and emergency braking: ISO 15622, ISO 22179, UN R152 and IEEE 2846 (citation details to be verified).

## Questions for the Authors

- The companion manuscript under review shares the detector, the tracker configuration and the margin form. What exactly is shared in text and analysis, and does the editor need it to judge this paper?
- Was the −1.0 m/s² threshold of the tracker-based phase estimator fixed before any held-out value was computed?
- How do the room and the shares change if every recording is cut 5 s after the lead's stop?
- The planner propagates the covariance at constant velocity without process noise and adds its own allowance. If the stack propagated with the tracker's own process noise, would the ratio stay near 1.10 and the null stand?
- In Table S36 the before-onset row shows 5.0% for every source, the oracles included. What produces an identical value there, and is it a floor set by the fallback row?
- In the deposit, will the amendment hashes and file times show that each amendment precedes the values it governs? Is the true-clearance geometry covered by a test that does not use the shared scoring library?

## Appendix

### How This Review Was Run

This review was AI-simulated by five reviewer roles: a Journal-Fit Reviewer, three peer reviewers (methodology; tracking and estimation; safety practice) and a Devil's Advocate.
- **The reviewers.** Each ran as a separate fresh session of a Claude Sonnet model and read only the submitted package. They were told not to read each other's reports, but their file access was not observed.
- **The synthesis.** An editorial synthesis then compared the five reports, settled the points where reviewers disagreed, and set the decision and the list of changes. It was written by Claude Opus 5.5, the same model that drafted this version, and it adds no criticism of its own: every change above comes from a reviewer's report.
- **No contract.** The panel ran without a scoring contract, so the decision follows the reviewers' recommendations and the editor's arbitration, not a mechanical rule.
- **Which file is the record.** This letter is for reading. A re-review or the revision coach works from the decision package, not from this letter.

### Limits of This Review

- The review is AI-simulated and is not calibrated against human reviewers.
- All five reviewers used one model family, so their errors may be correlated, and agreement between them is not independent confirmation.
- The PDF copies of Figs. 1–4 were not read; they duplicate the PNG images, which were read.
- The deposit (code, per-decision arrays, amendments and raw recordings) was not read, because it was not supplied.
- The rest of the manuscript and the supplement were read in full.

### Reviewer Summaries

- **Journal-Fit Reviewer** (Major Revision, confidence 4). The paper fits the journal. As packaged, however, it is a method note on an expected null, it is far longer than the recommendation, and its abstract leads with numbers that no main-text table carries.
- **Methodology reviewer** (Major Revision, confidence 4). The arithmetic is sound. But:
  - the positive control does not grade at the tracker's scale;
  - the inference for the tracker covariance's share has no single calibrated estimand;
  - the held-out figures use a favourable baseline;
  - no untouched confirmatory data remain.
- **Tracking and estimation reviewer** (Major Revision, confidence 4). The steady-state account is correct and every traced figure reconciles. But no arm has a covariance that varies, and the lag mechanism rests on one mis-tuned filter. Both can be addressed offline.
- **Safety-practice reviewer** (Major Revision, confidence 4). The null for this tracker is credible. The 12% and the 83% hold only for:
  - a 2 Hz detector without latency;
  - leads braking at up to 5.5 m/s²;
  - a perfect, independent stop;
  - one recording policy.

  The caution against removing a covariance margin should travel with the headline.
- **Devil's Advocate.** The confirmatory result is fixed by construction, and the discriminating content is exploratory and unstable across the two run sets. The editor upheld the substance and judged it repairable.

### Advisory Checks

- **Acronym check.** CANMOT and CARLA (also in the abstract), RR, AI, SHA, IEEE and OpenAI are used without expansion. The other flags are artefacts of the tool.
- **Suggested-reference check.** Done by hand against Crossref. Six of the seven tracking references the reviewers suggested were found with matching title, first author and year; the motion-model comparison of 2008 was not found in the top results. The standards were not checked. Being found does not show relevance.
- **Reviewer claim check.** The scripted check did not run. The editor checked eleven reviewer statements against the text instead, and all agree with it.

### Item Map

| Item | Record ref |
|------|------------|
| 1 | R1 |
| 2 | R2 |
| 3 | R3 |
| 4 | R4 |
| 5 | R5 |
| 6 | R6 |
| 7 | R7 |
| 8 | R8 |
| 9 | R9 |
| 10 | R10 |
| 11 | R11 |
| 12 | R12 |
| 13 | R13 |
| 14 | S1 |
| 15 | S2 |
| 16 | S3 |
| 17 | S4 |
| 18 | S5 |
| 19 | S6 |
| 20 | S7 |
| 21 | S8 |
| 22 | S9 |
| 23 | S10 |
| 24 | S11 |
| 25 | S12 |
| 26 | S13 |
| 27 | S14 |
| 28 | S15 |
| 29 | S16 |
| 30 | S17 |
| 31 | S18 |
| 32 | S19 |
| 33 | S20 |
| 34 | S21 |
| 35 | S22 |
| 36 | S23 |
| 37 | S24 |
| 38 | S25 |
