# Review Letter

Draft v13, target IEEE Open Journal of Intelligent Transportation Systems. Freeze reviewed: 21 Nov 2026, 03:08 (manuscript file hash starts 433be494).

## Decision

Major Revision. All five simulated reviewers recommend it, each with confidence 4 of 5, and the one critical issue raised by the Devil's Advocate was upheld as valid and repairable. No reviewer doubts a number. The objections are to what the title, the abstract and several labels say the numbers show, so the revision is a wording pass: none of the 14 required changes alters a result, and no new run is required.

## Strengths

- Failed hypotheses are printed and not hidden [Table II; Abstract].
- The cost of the paper's own best source behind leads that do not brake hard is reported in the abstract [Section V-D; Table V].
- The table of departures from the plan is complete and includes an error found afterwards [Supplement S3, Table S5].
- The equivalence of the tracker of record with its class average is robust across frontier type, update rate, latency and commitment [Tables II, S10, S14, S16].
- The headline numbers, the conversions to decision-equivalents and the closed-loop intervals were reproduced by the methodology reviewer [Tables II, IV].
- The brake test supports the closed-loop plant model [Supplement S9, Table S21].

## Required Changes

What the control and the null show

1. [Abstract; Section I, contribution 1; Sections IV-C, V-A, VII] The text says “the score detects rank information at the tracker's amplitude”, but the control is a band of 5% either way, and Table III shows the oracle at the tracker's own spread recovering 0.0001 [0.0000, 0.0002]. Say that detection is shown in that band, give the own-spread value beside it, and say that by the rule of Section IV-C the tracker of record is amplitude-limited. The locked plan dictated the present words, so record the change as a departure in Table S5. Wording only.
2. [Abstract; Sections V-A, VI] The equivalence could hardly fail: the margin is 0.05 of the room and perfect ranking in the band recovers 0.013. Say that the equivalence was expected, and lead with the observed bound before the margin. Wording only.
3. [Title; Abstract; Sections I, III-D, V-B, V-D, VI] The interacting-multiple-model result holds for that tracker as tuned here. Its constant-acceleration model has an acceleration term of 0.001, the supplement reports that the search grid did not reach the target window, and the planner receives only the position and velocity block under a constant-velocity prediction. Restrict every statement to the tracker as tuned, state both limits in the main text, take it out of the list of covariances that vary, and qualify the statements about a normalised innovation squared near 2. Wording only.
4. [Abstract; Section VII] The adaptive filter, the one variant whose margin varies, recovers 0.0459 [0.0390, 0.0533] of its room, about what its oracle recovers. It is in Section V-B but not in the abstract or the conclusion. Add one clause, marked descriptive, and say that this share has no permuted twin. Wording only.

Title and framing

5. [Title; Section I, Scope; Section VI, Limits; Fig. 1 caption] The title promises a test on real driving logs, and the Scope speaks of “the nuScenes replication”, while Table II shows that nothing was tested on the logs or in cut-in. Retitle to the confirmed scope, describe the two as attempted test beds without room, and say why the cut-in runs could not test young tracks (Table S18). Wording only.
6. [Abstract; captions of Tables I to V] The abstract is not readable alone: its first sentence has 44 words, and the room and equal caution are used before they are defined. Shorten it, define both terms in one clause, and give shares as percentages. Wording only.

Closed loop and labels

7. [Section VI; Section V-C; Abstract] The Discussion says the closed-loop result “supports the 3 s reading”. In Table IV the time gap, which has no information about the lead's motion, removes the contacts as well and loses less time. Remove or restate the inference and report the time gap beside the braking prediction. Wording only.
8. [Abstract; Sections III-B, V-C, VII; Table IV] State the closed-loop regime: the baseline is in full braking in 52.7% and 78.6% of decisions (Table S23), time lost is taken “over pairs without contact”, and it is about 24.5 s for every arm. Give the measured 0.16 [0.10, 0.22] s wherever the no-extra-cost label stands alone, and carry the contact-share margin with the word equivalent. The re-freeze of 03:03 already did part of this. Wording only.
9. [Abstract; Section VII; Table V] The label that the braking prediction costs progress hides a safety gain behind leads that stop and pull away (1.7 points of caution for 4.7 points fewer wrong goes). Separate that case in the abstract and conclusion. Wording only.
10. [Abstract; Sections V-A, VII; Tables III, S8] The braking prediction recovers most of the room only in the pooled population; while the ego moves its share is 0.411 [0.338, 0.488]. Section IV-C says “where they do not, shares are printed as decision-equivalents”, yet shares are printed for populations in which the partial oracles do not grade. Give the ego-moving value beside the pooled one, and apply the rule or state the limit. This reformats existing values; no result changes.
11. [Abstract; Sections V-D, VII; Fig. 4] The text compares 2 Hz without latency with higher rates at 0.1 s latency, and the abstract says “Magnitudes depend on 2 Hz updates and the recording policy”. At equal latency only the after-stop room falls strongly. Compare at equal latency and say which magnitude depends on the rate. The locked plan also asks the abstract to say 2 Hz without latency and to give the 10 Hz value; add both or record a departure. Wording only.

Who is left out

12. [Section I, Scope; Section III-C; Section VI, Limits] No test bed has a road user behind the ego, and on the real logs “contacts with actors behind the ego were no longer counted” after the design-split result. Say so in Scope and Limits, give the count from Table S27, and say that costs to following traffic and to occupants enter no classification. Wording only.

Author acts and defects

13. [Section IV-E; Acknowledgment; Section II; References; Supplement S3, S13] Complete the author's verification statement; say who the coordinator of Table S5 is; write for a first submission and not for a revision. Read reference [15] in full and confirm that it contains the baseline the text attributes to it, since its title concerns class uncertainty. Check references [26], [27], [37] and [38]. No value; author reading and wording.
14. [Supplement S5.3, S6.2, S7; Table V] Repair the defects: in Table S13 the share of N lies outside its own interval and a bracket is missing; Table V prints old-evaluation values found in no supplement table; Table S17 holds only the not-computed mark, whose definition does not fit undefined values; the after-stop room is never defined; run counts are given two ways. One value check; otherwise wording.

## Suggested Changes

15. [Sections IV-C, V-B] Add a curve of the ranking oracle's share against band width. New analysis, exploratory.
16. [Section III-D; Supplement S4] Add a multiple-model arm tuned for manoeuvres, or report the present one's mode probabilities by phase. New analysis.
17. [Section III-E] Add an arm with the tracker's own predicted covariance over the look-ahead, and a reference with the true current state under a constant-velocity prediction. New analysis.
18. [Tables I, II, III] Print the permuted twin's share with its interval, and add twins at the tracker's own spread and for the adaptive filter. New values.
19. [Table IV] Report closed-loop cost on all 60 pairs and each matched arm's design caution; consider a level at which the baseline has no contact. New values.
20. [Table I; Section III-F] Use the time gap as a second baseline; split the fallback share into moving and standstill decisions; say that the class average is the tracker's own mean.
21. [Section IV-D; Table S9] State the interval type, print the estimated coverages, and quote each interval with its level.
22. [Section IV-E; Supplement S12] Describe the second programs as a recount on shared components; say whether an outside timestamp of the plan hash exists; reconcile the two counts of values without a recount.
23. [Supplement S4, S6.2; Table III] Report innovation consistency by update rate, give units for the tuned constants, and define the lag column.
24. [Section VI, Limits] Name the function under test, the speed range and the absent radar range rate; soften content claims about standards that were not read; carry the scope on vulnerable road users into the conclusion.
25. [Figs. 2, 3; reference 3] Explain why the multiple-model curve lies above the class average in Fig. 2; show the rule bounds in Fig. 3; fix the column overflow of reference [3] reported in the typesetting log.
26. [Abstract; Sections I, VII; Supplement] Remove the triple repetition of the result sentences, cut process-log wording, and tell the editor about the related manuscript [10].
27. [References] Add the missing identifier, date, chapter and access date; cite the threat-assessment work the search found.
28. [Section IV-A; Supplement S2] Say that caution is averaged over an outcome-dependent set and that matching by open-loop caution does not equalise closed-loop risk.
29. [Abstract; Section V-D; Supplement S12] Follow the plan's reporting details: file times in the supplement, the schedule named a diagnostic in the abstract, and orderings stated at point estimates.

## Questions for the Authors

- What are the multiple-model tracker's mode probabilities during braking?
- How many closed-loop full-braking decisions are at standstill?
- Did the cut-in tuning runs already show no room and no young tracks?
- Why do the partial oracles score below the class average inside each phase?
- Is there a timestamp of the plan hash outside the author's machine?

## Appendix

### How This Review Was Run

Five AI-simulated reviewer roles ran, each in its own fresh context: a Journal-Fit Reviewer, three peer reviewers (methodology, domain, practical) and a Devil's Advocate, followed by an editorial synthesis. All ran on Claude Fable 5.2, a different model from the one that wrote the manuscript. All seats used one model family, so role separation does not remove the risk of shared errors. This letter is for reading; a later re-review or revision coach takes the decision package, not this letter.

### Limits of This Review

The review is AI-simulated and is not calibrated against human reviewers. The manuscript, the supplement and the four figures were read in full. The page images of the typeset file were not seen, because no renderer was available; the page count of 10 comes from the typesetting log. The deposit was not read, because it does not exist yet. The reviewer cards were those accepted for the previous review and were not confirmed again. The seats read while the text was re-frozen twice; every point here was re-checked against the 03:08 text.

### Reviewer Summaries

- Journal-Fit Reviewer: Major Revision. The one confirmed result is an expected null, the title promises more than Table II delivers, and the abstract is not readable alone.
- Methodology: Major Revision. The numbers reproduce; three constructs do less than the wording says.
- Domain: Major Revision. The multiple-model tracker as tuned barely varies, and the adaptive filter's positive result is underplayed.
- Practical: Major Revision. No follower in any test bed, a closed-loop baseline in a degenerate regime, and a time-gap arm that contradicts the Discussion.
- Devil's Advocate: Major Revision. The confirmed equivalence could not fail, and detection is not shown at the tracker's own spread.

### Advisory Checks

- Acronym check: ran; it lists some names as undefined; no finding comes from it.
- Suggested-reference check: did not run, because the review used no online service.
- Reviewer claim check: did not run as a separate judge; the carried numbers and quotations were checked against the files instead.

### Item Map

| Item | Record ref |
|------|------------|
| 1 | R1 |
| 2 | R2 |
| 3 | R3 |
| 4 | R4 |
| 5 | R5 |
| 6 | R12 |
| 7 | R6 |
| 8 | R7 |
| 9 | R8 |
| 10 | R9 |
| 11 | R10 |
| 12 | R11 |
| 13 | R13 |
| 14 | R14 |
| 15 | S1 |
| 16 | S2 |
| 17 | S3 |
| 18 | S4 |
| 19 | S5 |
| 20 | S6 |
| 21 | S7 |
| 22 | S8 |
| 23 | S9 |
| 24 | S10 |
| 25 | S11 |
| 26 | S12 |
| 27 | S13 |
| 28 | S14 |
| 29 | S15 |
