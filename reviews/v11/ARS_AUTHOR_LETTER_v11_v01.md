# Review Letter

## Decision

Major Revision. No reviewer doubts the central result: in these runs the tracker's covariance recovers no measurable share of the oracle's room. What needs a second round is the set of claims built around that result: whether the abstract's interval for the tracker covariance's share has a demonstrated coverage property, how the headline magnitudes move with the planner that recorded the runs, the tracking regime and the filter description that bound contribution 3 and the cross-family reach claim, the physical mechanism behind the per-phase and after-stop figures, and the fences the abstract leaves out (the population mix, the truth-labelled phases and the analyses added after the first results). No reviewer found a fatal or unrepairable defect, and the revised manuscript will be reviewed again against the nineteen required changes.

## Strengths

- The paper is in scope for an ITS journal (car following, the perception–planning interface, simulation-based safety evaluation), and the title and abstract lead with the evaluation design rather than with the null. The novelty is stated with its limits, the literature search is dated and scoped (Supplement S6), and the paper is set against its closest relatives by what each does and does not test.
- Every number in the abstract traces to a section or a table, and the abstract is 247 words, within the 250-word limit.
- The positive control is itself tested: partial oracles show that the pooled measure grades partial information, and the paper reports, against its own interest, where the grading fails. One reviewer likened this to a gauge study in quality engineering.
- Interval validity for the non-smooth tracker-covariance share is checked rather than assumed: runs are resampled as the clustering unit, the caution levels are recomputed in each resample, coverage is estimated by a double bootstrap, and stratified, leave-one-out and subsampling alternatives are reported (Tables S16–S17).
- The analysis history is open: two analysis plans are hashed, Table S4 sets each reporting change beside the wording it replaced, the earlier exploratory look at the evaluation runs is disclosed, an earlier overclaim about anticipating braking was withdrawn, and unfavourable added results (signed caution, the 2 m gap, the braking prediction's negative cells) are reported in the body.
- The steady-state null is anticipated and then confirmed at the level a tracking specialist would want (Table S15: the tracker's deviation takes five levels, one per state age), and the binding-row ratio check of Fig. 2(b) explains it. Engineers can run that check on their own logs without ground truth, and its extension to other scenario families is labelled as untested at decision level. The reading of the reliability check, that the error ranking comes from state age and constraint direction rather than from the tracker's covariance, is the right one.
- Giving the class average one scale per phase is the right control for separating the value of knowing the regime from the value of knowing each decision's error, and it shrinks the braking prediction's gain from 383 to 50 decisions.
- The margin projection is the exact variance of the constant-velocity predicted position along the constraint normal, and keeping the acceleration allowance separate keeps the source comparison clean. The braking prediction is correctly distinguished from an RSS worst-case bound.
- The UN R157 performance-model values are borrowed as nominal parameters, with a no-compliance fence that recurs in §II, §IV-C, the Limits and Supplement S3, and the minimum following distances used in Supplement S3 agree with the regulation's table.
- The evaluability rule for den₀ is fixed in advance and its thresholds are sensitivity-tested, and stops that end after the 3 s window are continued, with a censoring sensitivity (0.144 against 0.122).
- A second implementation of the scoring agrees with the first to 10⁻⁹ over several thousand values, and the scaling error it found was corrected.
- The Scope names what is not tested (calibrated, IMM and two-way adaptive covariances, track births, other road users, traffic behind the ego), the closed-loop check is presented as not testing the question, and the deployment-facing sentence, “It does not justify removing a covariance margin from a deployed stack”, rests on two concrete reasons.
- The four defined terms of §I and the notation table's column of established terms help readers from adjacent fields (two of its rows are the subject of items 39 and 44). The AI-use statement is specific, Table S28 documents the configuration in detail, and the organisation is clear, with figures that are legible and agree with the text.

## Required Changes

The nineteen changes below are required. They are grouped by topic; neither the grouping nor the order is a work order or a ranking. Please mark all changes in the revised manuscript and supplement, give a cross-reference table of the new section, table and page locations, and answer each item in your response letter; the re-review will check each one against what it asks for.

**Scope of the tracker null and how the tracker is described**

1. [§I justification, contribution 3, and the steady-state statements in §II and §VI] §I justifies measuring an expected null with the sentence “It still has to be measured: the covariance also depends on detections, misses and track age”, but the evaluated decisions barely exercise those dependences: 10 of 8,290 decisions have a young track, the median run-mean NIS is 0.24 against an expected 2, and sensing is clean and simulated. Where misses do occur, the ratio departs from the constant (1.68 after two missed updates, Table S27), yet the paper never states that its steady-state argument holds only with regular updates, no misses and fixed geometry. **Change:** in §I, contribution 3, §II and §VI, state that the null was measured in the steady-tracking regime under clean simulated sensing (regular updates, no misses or births, fixed geometry), and name missed updates and track births as conditions not exercised. Optionally, at your choice, re-run the tracker offline on the logged detections with controlled drop-outs and score the result, labelled as open-loop and off-policy, or add a degraded-perception condition.
2. [§I contribution 3; §VII] As written, contribution 3 is mostly a measured confirmation of the steady state that §II attributes to the Riccati recursion, and the Devil's Advocate adds that, in this population, the decision-level null follows from the ratio of Fig. 2(b) and the swept scale. **Change:** recast contribution 3, and its echo in §VII, as a measured confirmation in this population of what the steady state predicts, not as an open test, and say what the decision-level measurement adds (for example, the measured scale of the effect: 0.6 of 8,290 decisions).
3. [Abstract] The abstract does not say that track births, missed updates and real sensing are untested. **Change:** add one clause naming them as untested, keeping the abstract at or under 250 words; rewriting the CARLA sentence (item 27) frees words.
4. [§III-A; §I; §II; Fig. 1 caption] §I, Fig. 1 and §III-A call CANMOT a constant-velocity Kalman filter, and §II and §VI argue from a linear time-invariant filter, but Table S28 says it is run as an “extended Kalman filter with a constant-velocity model in the object frame”. Neither the frame of the class-average covariance P̄ nor how P̄ was formed is stated. **Change:** describe the filter as it is run, in §III-A and wherever it is named (§I, §II, the Fig. 1 caption): an EKF; the frames of the state, the noise and P̄; and whether P̄ is the mean of logged covariances or the second moment of realised errors.
5. [§V-E; §I contribution 4] In the crossing and benign families, the ratio to a fixed class average can vary simply because a fixed object-frame covariance is rotated against it, with no per-decision information in the variation. The §V-E wording “so the null of this paper is not expected to carry over to them”, and the same claim in contribution 4, read more into this than the check supports; the statement in §VI that the check is silent there is the accurate one. **Change:** reword §V-E and contribution 4 to say that the check is silent on those families, with no expectation beyond what the ratio check shows. Optionally, repeat Table V on the stored arrays against a heading-aligned class average (P̄ rotated by each track's heading) and report it in Table V or the supplement.

**Population mix, per-phase scales and how shares are read**

6. [§I contribution 1; §IV-B; §VII; Abstract] The graded oracles grade pooled decisions (0.27, 0.54 and 0.78) but not while the lead brakes (−0.68, −0.63 and 0.05) or with the ego moving (−0.11, 0.05 and 0.44; Table II, Table S12b), and the pooled population is 82.7% after-stop decisions. Contribution 1, the abstract and the conclusion of §IV-B that the pooled null is “not a blunt measure” present the design without this qualifier. **Change:** state in contribution 1, §IV-B, §VII and one clause of the abstract that the design is shown to grade information on pooled decisions only. Optionally, use the Table S23 machinery on the stored arrays to report whether the partial oracles grade once each phase has its own scale, and give any such result with its population.
7. [Abstract sentence giving the 5.6 points; §I Scope] The abstract asks open-loop decision scores to state their commitment and population, but it does not state its own population: 82.7% of the evaluated decisions come after the lead's stop and 77.5% have the ego at or below 0.5 m/s, and the room and the braking prediction's share move with that mix (Table S22). Two reviewers rated this differently (one as minor, one as part of a major point) but asked for the same change. **Change:** add a clause to the abstract sentence that gives the 5.6 points, and a sentence to the §I Scope, stating the share of evaluated decisions taken after the lead's stop with the ego nearly at rest.
8. [Abstract 89% sentence; §I contribution 2] §V-C says that a scale per phase uses phase labels from the logged truth and that no realisable rule was tested, but the abstract and contribution 2 state the 89% without that qualifier, so a reader can take it for an information-free baseline. **Change:** wherever the abstract and contribution 2 state the 89%, add that the phase is taken from the logged truth (for example, with the phase taken from the logged truth, or equivalent wording).
9. [§V-C; Supplement S10.4, Table S23; Abstract; §I contribution 2] The per-phase frontier is the envelope over 202³ (about 8.2 million) scale triples chosen with knowledge of the outcomes on the evaluation runs, and the 400-resample bootstrap re-optimises in each resample, so it does not remove the selection optimism. **Change:** choose the per-phase scale ratios out of sample by leaving runs out within the evaluation runs, report the held-out gain beside 0.89 in §V-C, and label 0.89 as an in-sample upper value in the abstract, contribution 2 and §V-C. A selection on the tuning runs may be added, but on its own it cannot separate the optimism from the run-set difference of item 16.
10. [§V-B, §V-D and §VI (and §V-C)] §VI asks that a measure be shown to grade partial information “in every population whose shares are interpreted”, yet §V-B, §V-D and §VI read the braking prediction's shares with the ego moving and while the lead brakes (0.47 and 0.61; signed 0.30 and 0.35; 0.04 and −0.89), where the partial oracles do not grade (Table II, Table S12). The Devil's Advocate adds the per-phase remaining-room shares (Table S23) and the before-stop 29% (Table S22). **Change:** attach the reading of §IV-B (that there a share measures what one margin scale can use) to each sentence that interprets a share in a population without demonstrated grading, or give those qualifiers in decision-equivalents, or run the partial oracles on those populations and report the grading check.
11. [§V-C] The braking prediction's share rises from 0.29 to 0.83 as after-stop decisions are added (Table S22), and after the stop it recovers 0.99 of that phase's room (Table S5), but no analysis shows why a wrong go occurs behind a lead at rest. Without a mechanism, the 83%, the 89% and the motion-state conclusion of §VI and §VII cannot be transferred, and they may partly reflect a tracker artefact on stationary targets. **Change:** on the stored arrays, report the tracker's estimated lead speed and acceleration around the braking onset and against time since the stop, tabulate the rows selected in after-stop wrong-go decisions, and state the mechanism in §V-C, citing that table or figure.

**Analyses added after the first results**

12. [Abstract; §I contributions 2 and 4] The 89%, the 29%, the 12%, the family ratio check and the calibrated intervals come from the second analysis plan and from Supplement S10, which were added after the first results. §IV-D and §VII say so; the abstract and the contribution list do not. **Change:** mark contributions 2 and 4, and the corresponding abstract sentences, as exploratory analyses added after the first results, so that a reader can tell which quantitative statements come from them.

**The bound on the tracker covariance's share**

13. [Abstract; §VI; §VII] The abstract says that the tracker's covariance recovers “none of the room that we can measure”, §VII says the same, and the Discussion says that “a class average does as well as the tracker's covariance”. The body reports a bound instead: the basic interval and every subsampling interval lie above zero, and Table S4 records the plan's rule that this share is never to be printed as not distinguishable from zero. **Change:** replace the absence wording in the abstract, §VI and §VII with the bound reported in §V-A, in the form settled by items 14, 15 and 28, for example the largest upper end across interval methods (2.2 of 8,290 decisions) or equivalence within a margin justified in decision units. No sentence should state or imply that the share is zero or indistinguishable from zero, and each should give the bound with its interval basis.
14. [§V-A; Supplement S10.1] N's margin is 1.1029 times F0's on 99.26% of binding rows, so N's operating points sample F0's path 3.40 steps along the log-spaced grid of scales. The non-smooth full-sample value of RR(N), at the 97.7th percentile of its own bootstrap distribution, whose median is 0.0001, looks like discretisation jitter rather than information. **Change:** add a placebo source, F0 with its variance multiplied by 1.1029², and report RR(N) − RR(placebo) as the covariance's information effect, or compute every frontier exactly from the per-decision critical scales g*; report the placebo-adjusted or grid-free RR(N) with its interval in §V-A, computed on the stored arrays.
15. [Abstract; §V-A; Supplement S10.1, Tables S16–S17] The calibrated level of 0.996 is read from the second-smallest and second-largest of 1,000 inner values, with no Monte Carlo error, and the subsampling upper ends rise with m (0.0033, 0.0038, 0.0047). If the non-smoothness is a grid artefact (item 14), the calibration covers an artefact, so the abstract's calibrated interval of −0.2% to 0.2% lacks a demonstrated coverage property. **Change:** report the Monte Carlo error of the calibrated level, or use an m-out-of-n bootstrap with an estimated rate. Until coverage is shown, or the statistic is made grid-free by item 14, do not present the calibrated interval as having nominal coverage: the interval printed in the abstract and §V-A should carry a demonstrated coverage basis or be replaced by the interval of the statistic of item 14.

**Dependence of the magnitudes on the recording planner**

16. [§V-A, §V-B, §V-D] On the 20 tuning runs, recorded under another planner, the 3 s room is 1.18 points against 5.56, the room left with a 0.75 s stop is 0.023 of the 3 s room against 0.121, and the braking prediction's pooled share is 0.377 [−0.204, 0.840] against 0.831 (Tables S2, S25(b)). None of these appears in the main text, which does not cite Table S2. **Change:** print the tuning-run room, commitment ratio and braking-prediction share beside the evaluation-run values in §V-A, §V-B and §V-D, and cite Table S2. If feasible, decompose the gap by phase mix and by contact-terminated runs, as Table S22 does for the after-stop segment.
17. [Abstract closing lesson; §VI; §VII; §VI Limits] The paper's lesson that an open-loop score should state its commitment and its population mix omits the data-collecting policy, which Tables S2 and S3 show matters as much. The recording planner also ended 5 of the 35 evaluation runs and 10 of the 20 tuning runs at contact, which limits what the absolute quantities say about a deployed stack. Two reviewers rated this differently (one as major, one as minor), with compatible remedies. **Change:** add the recording planner to the conditions named in the abstract's closing lesson, §VI and §VII, as a condition of the reported magnitudes rather than a cause (the design cannot separate it from the scenario draws), and add to the Limits that only relative comparisons between sources are meant to transfer.

**Data and code availability**

18. [Data and Code Availability] The deposit described there (both analysis plans with hashes, the per-decision arrays, the second programs and the result files) does not yet exist, and the planner library is an in-house re-implementation. The methodology reviewer judges that, once it exists, the described deposit would suffice to regenerate every number. **Change:** create the deposit and give reviewers a link they can access with the revision, so that at re-review they can reach the plans with hashes, the per-decision arrays, the second programs and the result files. Filling in the repository name and DOI is a separate submission gate (see Limits of This Review).

**The practical reading under a reliable stop**

19. [§VI, “Which commitment is representative”; §VII, stop branch] §VI says that, if a prompt and reliable stop is available, “the choice of source matters mainly for comfort and progress, which we did not score”. The reaction-and-stop scoring assumes an unconditional, perfectly executed 6 m/s² stop and counts only ego–lead contact; traffic behind the ego is outside the evaluation, and the fallback's reliability is assumed perfect. **Change:** in §VI and in the stop branch of §VII, restrict the statement to ego–lead contact, and name following-traffic exposure and fallback reliability as unscored safety costs. A stronger option: report, per source at matched caution, the share of decisions whose selected row is unsafe under the 3 s commitment but safe under the reaction-and-stop scoring.

## Suggested Changes

These changes are expected in this revision but do not by themselves bear on a headline claim; item 45 is optional. In your response letter, please say for each whether you adopted it, or why not.

20. [Abstract, “On 35 runs not used to design the margins”] The phrase is true for the margins, but the room and the tracker covariance's difference from the class average had been examined on these runs in an earlier exploratory analysis (§III-A), so the abstract implies a cleaner hold-out than exists. **Change:** add that these runs were examined in that earlier analysis, so that the result on them is a transfer, not a replication.
21. [§VI ranking] The ranking of margin sources leaves out a constant time-gap margin, the spacing policy that adaptive cruise control practitioners use, so the practical reading cannot be mapped onto the policies these readers deploy. **Change:** score a constant time-gap margin, written as a variance along the constraint normal, at equal caution on the stored arrays, or explain in §VI why it cannot be put on the same footing.
22. [§II, “Threat assessment, tracking and safety evaluation in intelligent vehicles” paragraph; Supplement S6] The positioning in this paragraph, and its sentence that no prior evaluation carries a tracker's covariance through to the decision, rest on references [41]–[52], whose content Supplement S6 says is “summarised from abstracts only”. **Change:** read the full texts of at least [41]–[47] and confirm or reposition the sentence, recording the check in Supplement S6; failing that, hedge the sentence to name the abstract-only limit.
23. [§IV-B, Intervals paragraph; §IV-C, third paragraph; §IV-D; §V-A, second paragraph; §V-D, the 2 m standstill gap paragraph; §V-E, last paragraph; Table IV; §II, adaptive covariances paragraph] The main text is likely 12 to 13 typeset pages against the venue's recommendation of 10 (an estimate; no typeset file was supplied). **Change:** move or compress the material at these locations toward the recommendation; for example, keep one sentence of the intervals paragraph and move the double-bootstrap detail to Supplement S10.1, move the discussion of the resolution-rule thresholds to S8.1, reduce §IV-D to two sentences pointing to S4, move the comparison of interval methods to S10.1, keep one sentence on the 2 m gap and move the rest to S10.5, keep one sentence of the Spearman check, merge Table IV into Table III or move it, and shorten the paragraph on adaptive covariances.
24. [§V-B, §V-C, §V-D] The results prose is dense enough to bury the findings. **Change:** open each results subsection with a one-sentence finding in words, keep in the text only the numbers that the abstract, §VI and §VII use, and move the rest to Tables II–IV or the supplement.
25. [§IV-B; notation table] The notation table uses the symbol D in a conversion formula, but D (the summed frontier difference over the 201 caution levels) is defined only in Supplement S8.1. **Change:** define D in §IV-B next to R and RR, or give the conversion in words.
26. [Table II] Signed caution appears both as a column (the pooled values) and as a row (the braking prediction in the other populations, with dashes in the pooled cells), so readers must work out which cell answers which question. **Change:** give signed caution its own small table, or place it as columns for every population, as Table S21 does.
27. [Abstract; §I] The sentence “CARLA runs in which a lead vehicle brakes are perceived by the CenterPoint detector and CANMOT, a fixed-noise Kalman tracker.” reads at first as if brakes were a noun, and it says that the runs, not the lead, are perceived. **Change:** rewrite it in both places, for example as: In CARLA runs the ego follows a lead vehicle that brakes; the lead is perceived by the CenterPoint detector and CANMOT, a fixed-noise Kalman tracker.
28. [§V-A; Supplement S10.1] Nothing shows that the bound in “no interval method we tried reaches 0.5% of the room” was fixed before the Supplement S10.1 values were read: the earlier draft's bound was about 0.4%, which the newly added subsampling end (0.0047) would have broken, and no equivalence margin is named. **Change:** state when the 0.5% bound was chosen; adopt an a-priori margin in decision units (one decision-equivalent is 0.0022 of the room), with its provenance, and phrase the null as equivalence within it, or as the largest upper end across methods (2.2 decisions).
29. [§IV-B; notes to Tables III, IV, S5 and S24] The sentence that “all other intervals should be read as slightly narrow” understates the undercoverage of the intervals for the tracker covariance's shares, whose double-bootstrap coverage is 53%. **Change:** say that nominal intervals for N's shares are not valid at their nominal level, and that the lead-braking cell of RR₀(N), [0.001, 0.013], is not a signal.
30. [§IV-D; Supplement S4] The hash and date of the amendment that added Supplement S10 are not printed, although both earlier plans' hashes are. **Change:** print them beside the two earlier hashes.
31. [§IV-D; Supplement S10.5 and S10.9; Acknowledgment] §IV-D says that “independent second programs re-implement the scoring”, but parts of the verification were not blind (Supplement S10.5 and S10.9), and the paper does not say who or what wrote the second programs and the recount. **Change:** state who or what wrote each second program and the recount, name the parts that were not blind, and qualify the word independent accordingly.
32. [§V-E; Supplement S9] §V-E says that the tracker's deviation ranks the realised error no better than the class average's does, an equivalence claim read from two overlapping marginal intervals, although both correlations are computed on the same 755 decisions. **Change:** report the paired run-bootstrap interval of ρ_N − ρ_F0, or say only that the two estimates are nearly equal.
33. [§V-B] The main text gives the frontier-construction alternates for NA only; those for CK3 and AM, which move the magnitudes by more than the stated intervals, appear only in Table S5. **Change:** give them beside 0.83 and 0.38 in §V-B: CK3 0.831, 0.790 and 0.750 (the last on the hull); AM 0.376, and 0.153 on the hull.
34. [§IV-C; §V-D; Table S20c] Under the reaction-and-stop scoring, “Only the wrong-go flag changes: caution keeps the 3 s scoring's definition.” The two axes of the equal-caution comparison are therefore scored differently. **Change:** add a variant in which caution is averaged over the selections that are safe under the reaction-and-stop scoring, or state why the 3 s definition is the right reference.
35. [Data and Code Availability] The raw recordings are available only on request. **Change:** deposit the raw recordings, or state and justify the restriction.
36. [§III-B] §III-B singles out the tracker's covariance N as on-policy, saying that “for every other source they are off-policy”, but the recording margin αp + βq is not g·p at any g, so N's evaluation states are off-policy too. **Change:** reword so that N is not singled out; optionally, report how often the recording planner's selection coincides with N's.
37. [§V-B; §III-A; Fig. S1] The NIS-inflated source can test little here: its trigger uses the NIS of the position block, while at a 3 s look-ahead the margin is dominated by the velocity block, and run-level means cannot show whether innovations grow at the braking onset. **Change:** report the NIS by phase (with an onset window) and the consistency of the velocity error against CARLA truth (NEES or z-scores), and state that the NA result does not bear on adaptation of the velocity block.
38. [§VI; §V-A] The 1.10 is presented as one constant, but it is a velocity-block ratio that depends on look-ahead: 1.02 to 1.05 at t = 0 and about 1.10 at 2–3 s (Table S14). **Change:** say so, and say that state age and look-ahead move the ratio.
39. [Notation table; §II] §II says that “the planner's margin plays the role of a spacing policy in adaptive cruise control [52]”, and the notation table maps g to a spacing policy's safety distance; but the margin is a chance-constraint tightening, whereas a spacing policy prescribes a gap as a function of speed. **Change:** map g to the chance-constraint parameter (the squared quantile, or safety factor, of the per-constraint risk level, as in [1]), and keep the term spacing policy for the time-gap baseline.
40. [§II; references] §II leaves out the stochastic-MPC work on car following and the fading-factor filtering work that is the direct prior art for scaling a covariance by an innovation statistic. **Change:** add Moser et al. (2018) and Brüdigam et al. (2023) on stochastic-MPC car following and Xia et al. (1994) on fading-factor filtering, with one sentence each on how they differ from this paper.
41. [§II] The summary of the closest planner-in-the-loop study [17] is loose. **Change:** restate it: its closed-loop nuPlan comparison cannot use class uncertainty, and its constant-velocity baseline with a fixed covariance is the nearest published analogue of this paper's null.
42. [Supplement S8.1–S8.2; last rows of Table S4] The supplement keeps wording that the main text has withdrawn: S8.2 still speaks of “a mechanism that no analysis here isolates”, though §V-C and Supplement S10.4 now isolate it, and the last rows of Table S4 describe abstract wording that the current abstract no longer contains. **Change:** update this wording or mark it as the earlier draft's record. The Devil's Advocate adds: restore the sentence on the NIS-inflated covariance that the locked plan fixed for the abstract, or record explicitly that it was dropped.
43. [§VI Limits] The Limits list several test-bed simplifications but do not say which way each moves the results. **Change:** add a paragraph on the expected direction in which each simplification (a 2 Hz detector without latency; lidar noise off; a nuScenes checkpoint; one car model, a straight road and default weather; the configuration shared with [9]) moves the lead-braking room and the braking prediction's share.
44. [Notation table; §IV-B] The notation table maps the room to the “Value of perfect information [55]”, which in decision analysis bounds the value of any information source; but E is a reference, not a bound, and the paper reports shares above 1. **Change:** relabel R as the value of a perfect-information margin within the fixed rule (analogous to the value of perfect information, not a bound), and map den₀ against O to the value of perfect information for each scoring.
45. [§V-E] Optional. The ratio check of Table V includes the tuning runs on which the class average was computed. **Change:** say in §V-E that the tuning-only column of Table S26 shows the same pattern.
46. [§VI; Supplement Table S23(b)] The finding that most of the pooled room is an allocation of caution between phases is not connected to a rule a planner could run. **Change:** add a class-average scale scheduled on a phase estimated from the tracker's state, or say in §VI that the result does not yet show whether a deployable schedule captures the allocation.
47. [§V-D] The sentence “Performance model 2 asks for 2 m at standstill, not for the absence of contact.” gives the model a normative register: to a type-approval reader it reads as a statement about the regulation's acceptance criterion, which the paper neither needs nor supports. **Change:** use the register of Supplement S10.5: 2 m is a model parameter at standstill, and the main scoring counts contact.
48. [Supplement S3, S3.4] Supplement S3 and S3.4 speak of the “legal following distance” and the “legal minimum”, but the time-gap table of UN R157 is an ALKS type-approval requirement, not a legal following distance for traffic in general. **Change:** write the R157 minimum following distance [38, §5.2.3.3] instead, and note that the test beds lie outside the ALKS domain.
49. [Abstract; §V-D; §VI] The abstract's 12% uses a 6 m/s² stop, harder than the planner's own fallback (the (−5, −5) row). **Change:** state beside the 12% that 6 m/s² exceeds the planner's own fallback and give the planner-matched value (0.18 at 5 m/s²), or say that the stronger stop stands for a separate emergency-braking function.
50. [Notation table; §VI Limits] Wrong-go counts treat a low-speed creep into a stopped lead and a contact at high closing speed alike. **Change:** state that the counts are severity-blind; better, from the stored clearances, report the closing speed at first loss of clearance for wrong-go decisions, by phase, for F0, E and the braking prediction.
51. [Data and Code Availability] The deposit as described lists “the per-decision arrays of the 55 lead-braking runs”, but contribution 4 and the benign-run check use arrays from all six scenario families, and the capture and scenario scripts and the simulator of Supplement S3 are not listed. **Change:** deposit the binding-row arrays of all six families (Table V, Table S26, Supplement S10.6), the capture and scenario scripts and the simulator of Supplement S3, or state the restriction.

## Questions for the Authors

Please answer these in your response letter. The six major points of the Devil's Advocate are covered by the changes above (items 1, 2, 6, 8, 9, 10, 12, 19 and 42); please answer each of them there as well.

- Could you give the editor [9], which is under review elsewhere, as a confidential file so that overlap can be checked, and confirm that no run, table or figure is shared with it?
- How many of the lead track's updates in the 35 evaluation runs were missed detections or coasting steps, and in which phase?
- Since a planner runs at one caution level, could RR be reported at a few fixed caution operating points beside the value averaged over levels? The Devil's Advocate also notes that the equal weighting of the 201 caution levels, including operating points no planner would use, is not defended.
- §V-B explains why the NIS-inflated covariance does not act by saying that the covariance is already too wide, yet Supplement S9 shows that the propagated deviation is too narrow while the lead brakes (RMS z of 3.17 to 5.89 at 1 to 3 s). How do the two fit together?
- The near-constant ratio of contribution 4 is pooled over rows. For the stopped-vehicle and cut-in families, do the decision-critical rows lie inside the 5% band, as Supplement S10.7 shows for lead braking?
- Could the analytic steady-state Riccati covariance of the tracker's fixed noise serve as a baseline, and what does the decision-level result add to it?
- By the logic of §V-C, sweeping one scale within one scenario family removes the one channel through which this covariance differs from a class constant, its level across families. Is the null therefore a within-family statement, and should the paper say so?

## Appendix

### How This Review Was Run

This is a simulated review produced by an AI review run in the full review mode; the journal did not issue it. No venue criteria were bound to the run, so fit was judged against the configured venue (IEEE Open Journal of Intelligent Transportation Systems, regular paper) and the journal's public scope only.

Five AI-simulated, role-separated reviewer seats read the manuscript: a Journal-Fit Reviewer (in the role of an associate editor), Reviewer 1 (Methodology), Reviewer 2 (Domain), Reviewer 3 (Cross-disciplinary and practical perspective) and a Devil's Advocate. An editorial synthesis then compared their reports, settled two disagreements about severity, and set the decision and the list of changes. All five seats and the synthesis ran on one model family (Claude Opus 5.5) from one provider, and no cross-model check was run. The seats were instructed not to read one another's reports, but their file access was not recorded.

The decision follows a fixed rule applied to the seats' scores on six review dimensions (methodology, domain accuracy, argument, cross-disciplinary relevance, writing and structure, venue fit and contribution). Every assessed dimension was scored at the warning level and none at the blocking level, which under the rule gives Major Revision; the seats' own recommendations do not enter the decision.

This letter is written for reading. A re-review, or the revision coach, works from the decision package, not from this letter.

### Limits of This Review

- The review is AI-simulated, and it is not calibrated against human reviewers.
- All seats ran on one model family, so role separation does not remove the risk that they share errors, and no second model family checked the decision.
- The whole manuscript was read: the abstract, Sections I–VII, the back matter, references [1]–[55], Tables I–V and the notation table, Figs. 1–4, Supplement S1–S10 with Tables S1–S29, and Figs. S1–S4. The raw data, code, analysis plans, amendments and lock manifests were not supplied, because the deposit does not yet exist, so the reviewers judged the text and tables only and regenerated no number from data.
- The review was not fully blind to the earlier round: before it started, the session that set it up read a short summary of the previous review's decision and main themes, though not that review itself or your response to it.
- The page estimate behind item 23 is unverified, since no typeset file was supplied, and the suggested references were checked only for existence in an index (see Advisory Checks).
- Two author-only placeholders remain open: the author block, and the repository name and DOI in Data and Code Availability. They are submission gates, not review findings, and must be filled before submission. The AI-use statement in the Acknowledgment appears to meet IEEE's disclosure requirement; the editorial office should confirm it against the policy in force.

### Reviewer Summaries

- **Journal-Fit Reviewer** (preliminary signal: major revision; confidence 4). The paper is in scope, its contribution is narrow but real, and it is candid about its limits; the significance case needs sharpening, mainly because the clean simulated test bed seldom exercises the regime that makes an expected null worth measuring, while the abstract omits fences the body states and the main text is longer and denser than the venue recommends.
- **Reviewer 1, Methodology** (no recommendation stated). The design is sound and the null robust, but the abstract's calibrated interval for RR(N) may be calibrating a grid-interleaving artefact, and the main text omits that the room, the commitment ratio and the braking prediction's share are several times smaller on runs recorded under another planner; ten minor reporting points follow, and six arithmetic checks of reported percentages were consistent.
- **Reviewer 2, Domain** (Major Revision; confidence 4). The steady-state mechanism is correct and confirmed for straight-road lead braking, but the tracker is described as linear although it is run as an EKF with object-frame noise, the cross-family reach claim overreads the ratio variation, and the per-phase and after-stop findings behind the 83% and 89% lack a physical mechanism.
- **Reviewer 3, Cross-disciplinary and practical perspective** (Minor Revision; confidence 4). The regulatory and deployment fences are unusually careful; the stop-branch practical reading omits following traffic and fallback reliability (this reviewer's most important point), the bridges to the value of information and to spacing policies are looser than those fields' meanings, the 89% is in-sample and truth-labelled, and the deposit does not cover contribution 4.
- **Devil's Advocate** (findings only; no critical issue, six major points). The strongest counter-argument is that, in this population, the decision-level null follows from the steady state and the swept scale; the reviewer adds that the positive control certifies sensitivity to phase rather than to per-decision error, that the 89% is an in-sample, truth-labelled envelope, that shares are read where the paper's own grading rule is not met, that the abstract headlines analyses added after the first results, and that the reliable-stop reading assumes away who bears its cost.

### Advisory Checks

These automated checks are advisory: they do not change the decision, and nothing above comes from them.

- Acronym check (body and English abstract, partial): it lists terms used without a definition at first use, among them CANMOT and CARLA (also in the abstract), RR, SHA, AI, IEEE and OpenAI, besides capitalised placeholder and label words (AUTHOR, BLOCK, NAME, AND, TABLE); it could not check IMM, RSS and NA.
- Suggested-reference check: of the nine works the reviewers suggested, seven were found in an index (the three of item 40, and four reading suggestions on decision curve analysis, value-of-information practice, automated-vehicle accident reports and rear-end collision countermeasures); the two ISO standards (21448 and 26262-2) could not be matched, as they have no DOI. Being found shows only that the record exists, not that the work supports the suggestion.
- Reviewer claim check: an automated judge checked the 52 reviewer findings against the manuscript and marked 4 as contradicted by it (the Journal-Fit Reviewer's point on dense results prose, and three Devil's Advocate points: on contribution 3, on what the positive control certifies, and on shares read where grading is not shown) and 3 as not checkable from the manuscript alone; what to make of each is your call.

### Item Map

| Item | Record ref |
|------|------------|
| 1 | R1 |
| 2 | R2 |
| 3 | R3 |
| 4 | R16 |
| 5 | R17 |
| 6 | R4 |
| 7 | R5 |
| 8 | R6 |
| 9 | R13 |
| 10 | R14 |
| 11 | R18 |
| 12 | R7 |
| 13 | R8 |
| 14 | R9 |
| 15 | R10 |
| 16 | R11 |
| 17 | R12 |
| 18 | R15 |
| 19 | R19 |
| 20 | S1 |
| 21 | S2 |
| 22 | S3 |
| 23 | S4 |
| 24 | S5 |
| 25 | S6 |
| 26 | S7 |
| 27 | S8 |
| 28 | S9 |
| 29 | S10 |
| 30 | S11 |
| 31 | S12 |
| 32 | S13 |
| 33 | S14 |
| 34 | S15 |
| 35 | S16 |
| 36 | S17 |
| 37 | S18 |
| 38 | S19 |
| 39 | S20 |
| 40 | S21 |
| 41 | S22 |
| 42 | S23 |
| 43 | S24 |
| 44 | S25 |
| 45 | S26 |
| 46 | S27 |
| 47 | S28 |
| 48 | S29 |
| 49 | S30 |
| 50 | S31 |
| 51 | S32 |
