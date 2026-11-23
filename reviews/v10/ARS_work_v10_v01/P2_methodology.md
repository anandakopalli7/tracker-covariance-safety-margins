contract_role: methodology

## Dimension Scores

### D1: methodology_rigor
score: block
block_class: repairable
trigger: "an interval method is used that is known to be invalid for the functional reported"

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: warn
trigger: "limitations are acknowledged in one section but not carried into the conclusions"

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

**Summary assessment.** The paper asks a narrow, well-posed question (does a fixed-noise Kalman tracker's per-decision covariance add decision value over a class-average margin once the margin scale is free?) and answers it with a design that is unusually strong for this literature: all margin sources are scored on the same decisions, at equal caution, against the realised future, with an oracle positive control, arms fixed on tuning runs, claim wording fixed before values, hashed plans and a full deviation log. The covariance null is well supported, mainly by the margin-ratio diagnostic (Fig. 2(b)), the absolute size of the difference (0.6 of 8,290 decisions) and the deviation-ranking check (§V-D), not by the share interval. My concerns are with (a) the bootstrap intervals that turn the non-smooth step-frontier statistics into the abstract's interval-based wording (W1); (b) three measurement and estimand choices that move the secondary headline numbers: the imputation of plans the 3 s window cannot judge (W2), a caution axis that conditions on the outcome (W3), and a pooled population weighted by how long recordings ran after the stop (W4); and (c) reproducibility affordances (W5). None of these overturns the covariance null. All can be repaired by re-analysing the stored arrays and adding documentation, and none needs new recordings.

**Headline-claim audit.** I checked every number in the abstract, the contributions list and the conclusion against the table it cites and the rule the paper says fixed its wording. Room 5.6 [4.5, 6.6] = Table II 5.56 [4.50, 6.60]. "At most about 0.4%" = the upper basic limit 0.0035 (Table S5 footnote; 2 × 0.00122 + 0.00108 = 0.00352). NIS-inflated wording = fixed rule 5 (l = 0.00729 > 0, hull l_h = −0.00398 ≤ 0), with bounds 0.007 and 0.025; phase shares −0.6% and +7.9% = Table S5. 83% [75%, 90%] = Table II 0.831 [0.753, 0.903]; 0.771 and 0.665 = Table S9; 38% = Table II. 12% and 53% = Table III. 0.19 points = Table S11 (1.45 of 755 decisions). 6% = 3.69/58.16. 0.11 [0.06, 0.18] = Table IV, branch 5. The abstract's last sentence = branch 1 of the phase-weighted aggregate (den₀ 3.69, below 10), chosen under the S8.1 consequence rule (order 1 < 2 < 3 < 5 < 4; outcomes 4, 1, 5). I found no headline number that departs from its table or its fixed rule, and no reported count, interval or ratio that is impossible. The problems below concern whether the rules, intervals and estimands support the strength of the wording, not transcription.

**Statistical reporting (criterion: uncertainty quantification at the unit of replication, with a valid interval method and pre-specified decision rules).** Judgement: PARTLY_MEETS. The resampling unit (run), replicate count, seed, generator call, pairing across arms and the multiplicity declaration are all correct and stated (S3 below). Two things are unverified: whether the interval method is valid for the step-frontier functional, and the coverage of the intervals that decide the abstract's wording (W1). The bounded recompute procedures barely apply. The paper reports no t, F or chi-square test and no degrees of freedom, so the only GRIM-eligible values are proportions of decisions with a stated N; I checked five of them, and all are consistent (see the receipts section). Outside those procedures I checked the arithmetic that a headline depends on. The basic-interval limits for RR(N) are [0.00125, 0.00352]. The exact one-sided 95% upper limit for 0 contacts in 130 episodes is 1 − 0.05^(1/130) = 2.28%, matching S3.4's 2.3%. The decision-equivalent conversions behind 7.7, 383, 173 and 127 decisions all agree.

**Scores.** D1 is a block of the repairable class. W1 meets my Phase 1 trigger: a percentile or basic bootstrap applied to a running-minimum (step-frontier) functional, with the estimate outside its own interval and no justification of validity, and it carries both primary claims. W2, W3 and W5 add further material but correctable defects. It is not fatal. The compared conditions differ only in the margin source, on the same decisions. The arms and the NIS-inflated claim rules were fixed before evaluation-run values were computed. Every row is scored against logged truth, so there is no extrapolation outside the logged support. Nothing I checked is arithmetically impossible, and the covariance null survives at the run level. D3 is a warn. No headline number outruns its interval in direction. But limitations that the paper states in §IV-B, §IV-D and §VI Limits are not carried into the abstract and conclusion, which headline the pooled 83%, the 12%/53% pair and the final sentence: the dependence on the population mix, the caution definition left untested at 3 s, a scenario selection that favours the prior, and the post-results, descriptive status of the commitment analyses (W3, W4, W10, W11).

### W1: Bootstrap intervals for the step-frontier shares are not validated, and the primary tracker-covariance statistic lies outside its own intervals
**Severity**: Major
**Evidence Anchor**: text: §V-A para. 2 "The point lies above the 97.5th percentile of its run-bootstrap distribution (median 0.0001; largest of 20,000 resamples 0.0025)"
**Confidence**: 4 — resampling theory for non-smooth functionals and clustered data; I could not rerun the bootstrap without the per-run arrays

Location: §IV-B para. 3; §V-A para. 2; Table II; Table S5 footnote; Table S1 (†); Table S4, row "The tracker covariance's share".

Problem. Both primary statistics, RR(N) and RR(NA), are ratios of summed differences between step frontiers. A step frontier is a running minimum over operating points, a non-smooth functional of boundary type for which the naive percentile and basic bootstraps are not generally consistent. The paper's own output shows the failure for RR(N). The bootstrap distribution is centred near 0.0001 while the estimate is 0.00122, so the point lies above the percentile interval [−0.00108, 0.00119]. It also lies just below the basic interval, whose limits are 2(0.00122) − 0.00119 = 0.00125 and 2(0.00122) + 0.00108 = 0.0035. The abstract's "at most about 0.4%" uses only the upper end of this basic interval, which was chosen after the results (Table S4). Its lower end excludes zero. The two interval types therefore disagree on whether RR(N) differs from zero, and neither has verified coverage (§IV-B). The same machinery fixes the NIS-inflated wording through rule 5 (lower limit 0.00729). That effect comes from 217 decisions in 14 of the 35 runs. Run sizes range from 18 to 271 decisions, and the resampling is not stratified over the three recording settings or the three desired speeds. Percentile intervals built on a few clusters of unequal size, with the signal carried by a minority of them, tend to under-cover. Leave-one-run-out stability (0.0137–0.0176) shows that the point is stable, not that the interval covers. The paper also does not say whether the 201 caution levels are recomputed in each resample; their range depends on F0's and E's operating points. If they are recomputed, the grid is a further data-dependent, non-smooth ingredient; if not, each resample is scored on the original sample's grid.

Why it matters. The covariance null does not depend on these intervals. Two pieces of the abstract's wording do: "at most about 0.4%" and "distinguishable from zero, between 0.7% and 2.5%".

Fix.
1. State whether the caution grid is rebuilt in each resample.
2. Estimate the actual coverage of the percentile and basic intervals for RR(N) and RR(NA) on the stored arrays. Use either a run-level double bootstrap (for example 500 outer × 2,000 inner resamples) or m-out-of-n subsampling of runs (m around 15–25), which stays valid for non-smooth functionals.
3. Report the primary intervals from the method that passes, with a sensitivity analysis stratified by recording setting α.
4. Re-apply the five fixed NIS-inflated rules to that interval and print the branch they select; if the branch changes, the abstract sentence changes with it.
5. For the tracker covariance, replace "at most about 0.4%" with a bound from the validated method, or with a plainly descriptive statement (0.6 of 8,290 decisions; largest of 20,000 resamples 0.25%). If the basic interval is kept, print its lower end too.

### W2: The reaction-and-stop results depend mainly on how unjudgeable plans are imputed, although the recordings appear to hold the truth needed to judge most of them
**Severity**: Major
**Evidence Anchor**: text: §V-C para. 2 "Count (ii) is driven by these pairs, which outnumber the 3,334 unsafe pairs"
**Confidence**: 3 — inferred from the paper's definitions of counts (i) and (ii); there may be an unstated reason why the logged future beyond 3 s cannot be used

Location: §IV-C para. 2; §V-C paras 1, 2 and 5; Table III, last column; Tables S6 and S10; the abstract's 12%/53% sentence and its last sentence; contribution 3; Conclusion.

Problem. Under the reaction-and-stop scoring at τ = 0.75 s, the 3 s truth window cannot judge 5,356 decision–row pairs, against 3,334 pairs judged unsafe. "As scored" keeps their 3 s-window flags, which in effect treats them as safe if there is no contact within 3 s; count (ii) calls all of them unsafe. Both are single imputations of a censored outcome. Because the room is a difference of frontiers (§IV-C), the two counts do not even bound it. The paper's own results show the imputation dominating:
- With count (ii), the ratio is 0.800, 0.209, 0.531 and 0.412 at 4, 5, 6 and 7.6 m/s².
- It exceeds the 3 s room from τ = 1.25 s.
- The lead-braking den₀ is at or below zero in 75–88% of resamples from τ = 1.5 s (Table S10).

Yet count (i) shows that only 153 of the 5,356 pairs have a stop unfinished at the end of the recording. For the other 5,203 pairs or so, the recording appears to contain the lead's logged motion until the stop finishes.

Why it matters. The commitment contribution is reported as two imputation regimes rather than as an estimate: the 12% versus 53%, the as-scored "too little room remains" sentence, and the count (ii) phase-weighted 0.11 [0.06, 0.18].

Fix.
1. Score each censored pair against the logged truth beyond the 3 s window until its stop finishes. If needed, restrict the evaluated population to decisions whose logged future covers the stop. Only the 153 count-(i) pairs then remain to be imputed.
2. Report that as the reaction-and-stop result, and keep "as scored" and count (ii) as sensitivity analyses.
3. If the truth beyond 3 s cannot be used (for example because the logged lead or other actors respond to the recorded ego), say so and why. Then present the two regimes in the abstract as imputation alternatives whose order is not guaranteed, not as separate findings.

### W3: Caution, the axis of every frontier, conditions on the outcome, and the headline 3 s shares were never rerun with the unconditioned definition
**Severity**: Major
**Evidence Anchor**: text: §IV-A "Decisions whose selected row is unsafe do not enter this average" and §VI Limits "count caution over truly safe selections only, and their sensitivity to that choice is untested"
**Confidence**: 4 — the selection effect follows from the definition; its size at the 3 s commitment is unknown until it is computed

Location: §IV-A; §V-C para. 4; Table S13(a); §VI Limits.

Problem. Caution is averaged only over decisions whose selected row is truly safe. Each arm's caution is therefore computed on a different subset of decisions, selected by the outcome, so arms with different wrong-go rates are compared at "equal caution" measured over different denominators. The paper ran the obvious alternative (the signed speed difference to the 3 s oracle's row, over all decisions) only at τ = 0.75 s. There it reversed the braking prior's sign with the ego moving (from 0.034 to −0.90 [−1.47, −0.49]) and in the phase-weighted aggregate (to −1.77 [−3.27, −1.12]), and it lowered the pooled share from 0.936 to 0.80. The 3 s results that carry the abstract and the conclusion were not rerun: the 83% [75%, 90%], the 0.665 phase-weighted share, the 0.61 while the lead brakes, and the acceleration margin's 38%.

Why it matters. The conclusion "the decision value we could measure lies in anticipating braking under the 3 s commitment" rests on the 3 s shares. The only evidence on this design choice shows that it can flip signs, in exactly the populations where the measure is weakest.

Fix.
1. Rerun the 3 s scoring with caution counted over all evaluated decisions (signed), for every arm and every population of Table S5, using the existing signed-caution code (two programs already exist).
2. Print the results beside Table II. Revise the abstract's 83% sentence and the conclusion if the ego-moving or phase-weighted value changes sign or branch.
3. In future plans, prefer a caution definition that does not condition on the safety outcome.

### W4: The pooled population, and with it the abstract's room and 83%, is set by how long the recordings ran after the stop
**Severity**: Major
**Evidence Anchor**: text: §IV-B para. 2 "it is 2.6 times the decision-weighted mean of the three phase rooms (2.13 points)"
**Confidence**: 4 — the aggregation arithmetic is the paper's own; whether a truncated estimand changes the conclusions is unknown until it is computed

Location: §III-A para. 1; §IV-B paras 1–2; §V-A para. 1; §VI "Where the decision value lies"; Abstract; Conclusion.

Problem. 82.7% of evaluated decisions come after the lead has stopped, and 77.5% have the ego at or below 0.5 m/s. The pooled estimand is therefore weighted by how long each run dwelt after the stop, which is an artefact of the recordings. The pooled room (5.56 points) is 2.6 times the decision-weighted mean of the phase rooms (2.13). Only about 127 of the braking prior's 383 pooled decisions are gained within phases; the paper attributes the rest to how one margin scale spends caution across phases, a mechanism it does not isolate. This is an aggregation effect of the Simpson type: pooling phases whose rooms are 0.43, 15.59 and 0.82 points under one scale produces most of the headline room. The abstract's intervals measure run-to-run variability of this pooled quantity, not its dependence on the phase mix. The graded-oracle check that licenses reading pooled shares also works only pooled and after the stop, not while the lead brakes or with the ego moving (Table S12).

Why it matters. The abstract and the conclusion headline the pooled 5.6 points and 83%. With the ego moving, the room is 10.16 points and the prior's share 0.47 [0.35, 0.57]. Against a perfect oracle, the phase-weighted share is 0.665.

Fix.
1. Truncation sensitivity: cap each run's post-stop segment at fixed durations (for example 1, 2 and 5 s) and recompute R and every RR. This measures the dependence on recording length directly.
2. Isolate the cross-phase mechanism: give F0 and each arm one margin scale per phase, and trace the frontier over per-phase scale combinations at equal total caution. The gap between this frontier and the single-scale frontier is the value of knowing the phase, which can then be separated from per-decision information.
3. In the abstract and the conclusion, print the ego-moving or phase-weighted value beside the pooled 83%, and name the population that defines the room.

### W5: The recording, perception and planner configuration needed to regenerate the data is missing, and the code and plans are not yet deposited
**Severity**: Major
**Evidence Anchor**: absence: §III-A and Data and Code Availability — expected CARLA version, map, weather and sensor simulation, CenterPoint checkpoint and training data, CANMOT per-class noise matrices and gating, per-run scenario parameters, recording-planner settings, and deposited code, plans and per-decision arrays; checked §III-A, §III-B, Table I, Data and Code Availability, Supplement S1, S2 and S4, and a full-text search of the manuscript and supplement
**Confidence**: 4 — absences confirmed by searching the full text

Location: §III-A; §III-B; Data and Code Availability; Supplement S1 and S4.

Problem. The tracker is "configured as in [9]", a manuscript under review. The following are not given:
- the CARLA version, map, weather and sensor simulation;
- the CenterPoint checkpoint and its training data;
- CANMOT's per-class process and measurement noise and its gating;
- the lead-braking scenario parameters per run (initial gap, onset time, deceleration);
- the recording planner's other settings.

The planner is described through "the project's re-implementation of the planner library". The Data and Code Availability statement is a placeholder. The lock-manifest hashes (S4) can be verified only once the plans, code and inputs are public.

Why it matters. The central diagnostic (a margin within 5% of 1.10 × F0 in 99% of rows, and a median per-run NIS of 0.24) is a property of the noise settings, the update rate and the simulated sensor noise. A reader can neither inspect nor vary any of them.

Fix.
1. Add a configuration table covering the items above, with software versions.
2. Before acceptance, deposit the analysis code, both plans with all amendments and lock manifests, and at least the stored per-decision arrays from which every number in the paper is computed: clearances, critical values for every arm, truth windows, phase labels and run identifiers.
3. State which raw recordings can be shared.

### W6: Replay validity on the evaluation runs is assumed rather than shown
**Severity**: Minor
**Evidence Anchor**: text: Supplement S1 "The replay identity was checked on the tuning runs only"
**Confidence**: 3 — the risk is plausible but unquantified

Location: Supplement S1; §III-B last paragraph; §IV-A.

Problem. The planner replay reproduced the logged selections in 31,645 tuning-run decisions. The evaluation runs, however, were recorded with a different margin (d² ≥ αp + βq, with the tracker's covariance), and the replay was not checked on them. Scoring every row counterfactually against the logged future also assumes that the logged motion of the lead and of any other tracked actor would not have changed had the ego taken a different row. The paper does not state this assumption.

Fix.
1. Reproduce the logged selections on the evaluation runs with the recorded α, β, p and q. This checks the critical-value pipeline, including N's margins, on the runs that carry the results.
2. State that the lead's braking is scripted and that no actor's logged trajectory depends on the ego, or quantify where it does (for example in the 71 decisions with several tracks).

### W7: The five short runs are unexplained and were never removed jointly
**Severity**: Minor
**Evidence Anchor**: text: §III-A para. 1 "Thirty runs contribute 271 evaluated decisions each and five short runs 18–53"
**Confidence**: 3 — a possible concentration of the NIS-inflated effect; not shown either way

Location: §III-A paras 1–2; Fig. S1; §V-B para. 1.

Problem. Five runs contribute 18–53 evaluated decisions, against 271 for each of the others. They have 17–24 tracker updates and per-run mean NIS of 1.02–2.41, against 0.11–0.50 for the full runs. The paper does not say why they are short (scenario end, track loss, contact or recording failure). The NIS-inflated covariance acts only when NIS exceeds 2, so these runs may carry a disproportionate part of its 217 changed decisions. Leave-one-run-out removes one run at a time and cannot show this.

Fix.
1. State why the five runs are short.
2. Report how many of the 217 changed decisions, and of the 304 actor-decisions with λ > 1, fall in them.
3. Recompute R, RR(N) and RR(NA) with all five runs excluded together.

### W8: The 10-decision-equivalent resolution rule decides the abstract's last sentence without a sensitivity check
**Severity**: Minor
**Evidence Anchor**: text: §IV-C para. 3 "a resolution rule of our choosing"
**Confidence**: 3 — the timing is inferred from §IV-D; it is not clear whether phase-level values were among those already known

Location: §IV-C para. 3; Supplement S8.1; §IV-D bullet 4; Table S13(b).

Problem. The threshold was fixed in Amendment 05, when the class average's reaction-and-stop results were already known (§IV-D). At 6 m/s² the perfect oracle's frontier is zero, so den₀ equals the class average's summed frontier and its size could be anticipated. The abstract's final sentence follows from den₀ = 3.69 being below 10. At 4 m/s², however, the phase-weighted den₀ is 14.81 and the prior's share is 0.63, and under signed caution den₀ is 11.52. Evaluability is also judged on the point estimate of den₀, not on its interval.

Fix.
1. Report the branch the rule gives at other thresholds, for example 5 and 20 decision-equivalents.
2. As a sensitivity, base evaluability on den₀'s lower percentile limit.
3. Say in §IV-D whether the phase-level class-average frontiers under the reaction-and-stop scoring were among the values already known.

### W9: Percentile intervals for ratios whose denominators approach zero are unstable
**Severity**: Minor
**Evidence Anchor**: table: Table S10, count (ii), τ = 0.75 s, lead-braking row (RR₀(CK3) 0.266 [0.098, 1.237]; den₀ 45.00 [6.18, 72.22]; 1.57% of resamples at or below zero)
**Confidence**: 4 — standard behaviour of ratio estimators

Location: Tables S9–S10; §V-C para. 5.

Problem. While the lead brakes under count (ii), the braking prior's share is printed as 0.27 [0.10, 1.24]. Resamples with den₀ at or below zero (1.57%) are dropped before the percentile is taken. An upper limit above 1, for a share of a perfect oracle's avoidable wrong-go, reflects resamples in which the denominator nearly vanishes. Dropping up to 2.5% of resamples also conditions the interval on the denominator. The same pattern recurs in Tables S9–S10 (for example RR₀(E) [0.225, 2.056] in the same row).

Fix. Where den₀'s interval approaches zero, report D and den₀ with their joint interval (partly given already in decision-equivalents) or a Fieller-type interval for the ratio, and flag such cells instead of printing a percentile interval for the ratio.

### W10: The abstract presents the runs as held out and the commitment results without their descriptive status
**Severity**: Minor
**Evidence Anchor**: text: Abstract "On 35 runs not used to design the margins"
**Confidence**: 4 — the status is stated in the body and missing from the abstract and conclusion

Location: Abstract; Conclusion; §III-A; §IV-D bullets 1 and 4.

Problem. The phrase is accurate, but the room and the tracker covariance's difference from F0 had already been examined on these runs in an exploratory analysis. For those two quantities the paper itself calls the evaluation a transfer, not a replication. The reaction-and-stop analyses of every margin source were added after the first results and two reviews and are descriptive. Neither status reaches the abstract or the conclusion, where readers look for the inferential status of a result.

Fix.
1. Add a clause to the abstract, for example "a transfer for the room and the tracker's covariance, which an earlier exploratory analysis had examined on these runs".
2. Mark the commitment sentences as descriptive analyses added after the first results, in the abstract or at least in the conclusion.

### W11: The braking prior's cost where no braking follows is untested, although the project holds such runs
**Severity**: Minor
**Evidence Anchor**: text: §VI "its cost where braking never comes is untested here"
**Confidence**: 3 — feasibility depends on the tuning recordings of the other families being scoreable

Location: §VI "Where the decision value lies", para. 3; §III-C.

Problem. Every evaluation run contains a braking lead, so the scenario selection favours the braking prior, as the paper notes; its zero-margin caution is also higher (1.72% against 1.10%). The project already has benign-driving, cut-in and crossing runs, which were used to build P̄. The abstract's 83% sentence does not carry the qualification.

Fix. Score the braking prior against F0 on the benign-driving and other-family runs (wrong-go and caution at a matched scale, or caution at equal wrong-go) to measure its cost where braking never comes. Otherwise, add "on runs in which the lead always brakes" to the abstract's 83% sentence.

### W12: The graded-oracle check rests on a single random mixing draw
**Severity**: Minor
**Evidence Anchor**: text: Supplement S8.1 "one uniform draw per stored decision"
**Confidence**: 3 — the size of the across-draw spread is unknown

Location: Supplement S8.1 para. 4; Table S12.

Problem. The partial oracles use one uniform draw per stored decision, shared across p, and the noisy oracles one normal draw per decision. The intervals in Table S12 are run-bootstrap intervals conditional on those draws. The paper limits the reading of every phase share using the within-phase scores (for example −0.68 and −0.63 while the lead brakes, at p = 0.25 and 0.5). Those scores may depend on which quarter or half of the 755 decisions received the oracle's value.

Fix. Repeat the partial and noisy oracles over, say, 50 draws, and report the across-draw spread beside the run-bootstrap interval in each cell of Table S12.

### S1: Pre-specification and a complete deviation trail
**Evidence Anchor**: table: Table S4 (reporting added or changed after the results), with §IV-D

- The arms were defined on the tuning runs before they were first computed on the evaluation runs.
- The NIS-inflated claim wording was fixed as five ordered rules before that arm was computed.
- Two hashed lock manifests bind the code, inputs and plans.
- Every change made after the results is listed with its fixed and reported wording, and the earlier exploratory exposure of the room and of the tracker covariance is disclosed rather than hidden.

This is the standard I would hold other decision-level evaluations to.

### S2: A positive control, plus a test of whether the measure grades information
**Evidence Anchor**: table: Table S12 (graded oracles)

The oracle shows that there is room to recover. The partial and noisy oracles then test whether the share measure grades partial information. The paper reports honestly where it does not (within phases, with the ego moving) and restricts its interpretation there. Few evaluations of this kind validate their own metric.

### S3: Resampling at the right unit, fully specified and paired
**Evidence Anchor**: text: Supplement S8.1 "over the 35 runs in sorted name order"

- The bootstrap resamples runs, not decisions.
- The replicate count, seed and exact generator call are given.
- All arms are scored on the same decisions, and contrasts use the same draws (Table S3).
- Resamples without room are counted and reported, leave-one-run-out is given, and the multiplicity status of the secondary contrasts is declared.

### S4: Independent re-implementation, with verification status for each value
**Evidence Anchor**: text: Supplement S4 "rebuilt λ and the inflated critical values from the raw logs bit for bit"

A second program, written from the specification, reproduces λ, the critical values and the primary shares within 10⁻¹². The verification status of every table cell (two codes, one code, or one program recounted by an independent reviewer) is reported.

### S5: Mechanistic diagnostics that explain the null instead of only reporting it
**Evidence Anchor**: figure: Fig. 2(b), with §V-D

The ratio of the tracker's margin to the class-average margin on binding rows needs no ground truth and shows directly why the covariance cannot change many decisions once the scale is free. The deviation-ranking check, with the class average and ρ* as references, separates ranking driven by the state's age from ranking driven by the covariance. Both checks transfer to other trackers.

### S6: The commitment assumption is made explicit and varied
**Evidence Anchor**: table: Table III, with Table S6

The scoring assumption behind open-loop decision metrics is stated, and it is varied over delays, stop decelerations and standstill gaps. The paper withdrew its earlier claim that the two scorings bracket the room once its own results contradicted it. W2 concerns how the censored plans are handled within this analysis, not the value of reporting it.

## Arithmetic Receipts

### AR1
procedure_id: grim
evidence_anchor: text: §III-A "Of the evaluated decisions, 77.5% have the ego at or below 0.5 m/s"
reported_inputs: 77.5% (one decimal in percent); analytic N = 8,290 evaluated decisions; binary per-decision indicator (ego speed at or below 0.5 m/s); Table S5 ego-moving count 1,863
assumptions: unweighted proportion of a 0/1 indicator over the 8,290 evaluated decisions as defined in §III-A; rounding rule unstated, so reachability is checked under both half rounding and truncation
derivation: half rounding needs 0.7745 ≤ k/8290 below 0.7755, i.e. k from 6421 to 6428; truncation needs 0.775 ≤ k/8290 below 0.776, i.e. k from 6425 to 6433; both sets are non-empty; Table S5 implies k = 8290 − 1863 = 6427 and 6427/8290 = 0.77527
derived_value_or_range: attainable counts 6421–6428 (half rounding) and 6425–6433 (truncation); paper-implied count 6427 gives 77.527%
rounding_interval: [77.45%, 77.55%) under half rounding; [77.5%, 77.6%) under truncation
nearest_achievable: 6424/8290 = 77.491% and 6425/8290 = 77.503% straddle the reported 77.5%
comparison_rule: reachable if at least one integer count k gives k/N inside the rounding interval under each admissible rounding rule
status: consistent

### AR2
procedure_id: grim
evidence_anchor: text: §V-A "99.26% of rows lie within 5% of it and 0.74% (1,127) outside"
reported_inputs: 0.74% outside and 99.26% within (two decimals in percent); count outside 1,127; analytic N = 152,264 binding decision rows over all 55 lead-braking runs
assumptions: unweighted proportion of a 0/1 indicator (row outside the 5% band) over the stated 152,264 rows; rounding rule unstated, so both half rounding and truncation are checked
derivation: 1127/152264 = 0.0074016 rounds to 0.74% under both rules; half rounding admits k from 1120 to 1134 and truncation k from 1127 to 1141, both containing the stated 1,127; complement 151137/152264 = 0.992598 rounds to 99.26%
derived_value_or_range: 0.74016% outside and 99.2598% within, from the stated count
rounding_interval: [0.735%, 0.745%) under half rounding; [0.74%, 0.75%) under truncation
nearest_achievable: 1126/152264 = 0.73951% and 1127/152264 = 0.74016% straddle the reported 0.74%
comparison_rule: the stated count over the stated N must fall in the rounding interval of the printed percentage, and its complement must round to the printed within-band share
status: consistent

### AR3
procedure_id: grim
evidence_anchor: table: Table S12 footnote, P25 share of the 9,307 stored decisions
reported_inputs: P25 share 0.2440 (four decimals); analytic N = 9,307 stored decisions; binary per-decision indicator (decision given the oracle's critical values)
assumptions: unweighted proportion of a 0/1 indicator over the 9,307 stored decisions named in the footnote; rounding rule unstated, so both half rounding and truncation are checked
derivation: half rounding needs 0.24395 ≤ k/9307 below 0.24405, i.e. k = 2271 only; truncation needs 0.2440 ≤ k/9307 below 0.2441, i.e. k = 2271 only; 2271/9307 = 0.244010
derived_value_or_range: k = 2271 under either rule; 2271/9307 = 0.244010
rounding_interval: [0.24395, 0.24405) under half rounding; [0.2440, 0.2441) under truncation
nearest_achievable: 2270/9307 = 0.243902 and 2271/9307 = 0.244010 straddle the reported 0.2440
comparison_rule: reachable if at least one integer count k gives k/N inside the rounding interval under each admissible rounding rule
status: consistent

### AR4
procedure_id: grim
evidence_anchor: table: Table S12 footnote, P50 share of the 9,307 stored decisions
reported_inputs: P50 share 0.4977 (four decimals); analytic N = 9,307 stored decisions; binary per-decision indicator (decision given the oracle's critical values)
assumptions: unweighted proportion of a 0/1 indicator over the 9,307 stored decisions named in the footnote; rounding rule unstated, so both half rounding and truncation are checked
derivation: half rounding needs 0.49765 ≤ k/9307 below 0.49775, i.e. k = 4632 (0.497690); truncation needs 0.4977 ≤ k/9307 below 0.4978, i.e. k = 4633 (0.497797); each rule has an attainable count
derived_value_or_range: k = 4632 under half rounding or k = 4633 under truncation
rounding_interval: [0.49765, 0.49775) under half rounding; [0.4977, 0.4978) under truncation
nearest_achievable: 4632/9307 = 0.497690 and 4633/9307 = 0.497797 straddle the reported 0.4977
comparison_rule: reachable if at least one integer count k gives k/N inside the rounding interval under each admissible rounding rule
status: consistent

### AR5
procedure_id: grim
evidence_anchor: table: Table S12 footnote, P75 share of the 9,307 stored decisions
reported_inputs: P75 share 0.7456 (four decimals); analytic N = 9,307 stored decisions; binary per-decision indicator (decision given the oracle's critical values)
assumptions: unweighted proportion of a 0/1 indicator over the 9,307 stored decisions named in the footnote; rounding rule unstated, so both half rounding and truncation are checked
derivation: half rounding needs 0.74555 ≤ k/9307 below 0.74565, i.e. k = 6939 (0.745568); truncation needs 0.7456 ≤ k/9307 below 0.7457, i.e. k = 6940 (0.745675); each rule has an attainable count
derived_value_or_range: k = 6939 under half rounding or k = 6940 under truncation
rounding_interval: [0.74555, 0.74565) under half rounding; [0.7456, 0.7457) under truncation
nearest_achievable: 6939/9307 = 0.745568 and 6940/9307 = 0.745675 straddle the reported 0.7456
comparison_rule: reachable if at least one integer count k gives k/N inside the rounding interval under each admissible rounding rule
status: consistent
