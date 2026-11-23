# Review Letter

## Decision

The decision is Major Revision. Every reviewer who addressed the central result finds it robust: the tracker's covariance recovers essentially none of the oracle's room under any scoring where its share can be estimated, and the margin-ratio check of Fig. 2(b) shows why. The methodology reviewer and the Devil's Advocate each found a problem that blocks acceptance as the paper stands, and both call it repairable: the bootstrap intervals for the step-frontier shares are not validated, and the claim that the measurable decision value lies in anticipating braking rests on premises the paper does not yet support (pooling across phases, imputed censored plans, caution that conditions on the outcome, the unmeasured cost where braking never comes, whether the room is one a covariance can use, and off-policy states). The required work therefore concerns the inferential support and scope of the secondary headline numbers, together with framing, the abstract, scope limits and reproducibility; the methodology reviewer judges its own items repairable by re-analysing the stored arrays and adding documentation, without new recordings.

## Strengths

- The central covariance result is robust. Every reviewer who addressed it finds that, for this tracker in lead braking, the covariance adds essentially no decision value over a class average under every scoring where its share can be estimated, and none of the changes below overturns that result.
- The ratio of the tracker's margin to the class-average margin on the planner's binding rows (Fig. 2(b)) needs no ground truth, explains the null by a mechanism the paper demonstrates, and can be run by other teams on other trackers. All four peer reviewers credit it, and the Devil's Advocate calls it perhaps the paper's most reusable result.
- The oracle positive control, with the graded oracles of Table S12, separates a true absence of value from a blunt measure, and the oracle is correctly framed as the value of perfect per-decision information, a reference rather than a bound. Three reviewers credit it directly and the domain reviewer confirms the framing.
- The lesson that an open-loop decision score must state its commitment assumption and show how its conclusions move with it is a concrete reporting rule for evaluators and benchmark designers, and Fig. 4(a) carries it in one panel. All four peer reviewers credit it.
- The tracker's consistency is measured rather than assumed: NIS is compared with its expected value and RMS z is reported by phase and look-ahead, and the paper contrasts its under-confident filter with the overconfidence reported for Kalman baselines elsewhere.
- The reporting is candid. Table S4 sets every change made after the results beside the wording fixed beforehand, §IV-D separates planned from added analyses, the Limits paragraph names the weak points, and Fig. 3 annotates a point that lies above its own interval instead of hiding it.
- The numbers hold up when checked. A second, independently written program reproduces the key values; the reviewers' checks of the headline numbers against their tables and of derived quantities found no discrepancy; and five granularity checks of reported proportions were all consistent.
- The paper states plainly that “the claim concerns this covariance, not uncertainty in planning in general”, so it cannot fairly be cited as showing that uncertainty does not help planners.

## Required Changes

Every change in this part is required. The topic lines only group related changes; they do not set an order of work. Please answer each numbered change, required and suggested, in your response letter.

**Framing, contributions, length and abstract**

1. [Title; Abstract, first sentence; §I, paragraph 4] The title asks in general whether a Kalman tracker's covariance improves decisions, while §I itself says that for a fixed-noise Kalman filter the covariance's null is expected, so the headline poses an expected result as an open question. Qualify the title to the fixed-noise case or recast it around the decision-level evaluation, and state in the Abstract and §I that the covariance null is the expected steady-state result and that the measured contribution is the room, its location and its dependence on the commitment.
2. [§I, contribution list] Contribution 2 offers confirmation of the Riccati steady state as a contribution, while the evaluation design and the commitment dependence, which the Journal-Fit Reviewer judges new for an ITS reader, are under-sold. Present the evaluation design (equal caution, the oracle positive control, the graded oracles of Table S12, an explicit commitment model) and the commitment dependence as contributions, introduce the covariance diagnostic as a confirmatory test of an expected steady state, and add one sentence to §I on why the expected null still needed measuring (detections, misses, track age). The order within the list is yours to choose.
3. [§VI, new paragraph; §VII, last sentence] The positive result kept in the Conclusion, the braking prior's 83%, comes from the 3 s scoring, which §IV-C itself describes this way: “The 3 s commitment scoring is a stress scoring.” §VI does not tell developers, testers or assessors what to do differently, or which scoring should guide practice. Add a §VI paragraph on implications for testing and development that states which commitment model you consider representative of the planner's replanning and why, gives the practical reading under each model, and names the closed-loop test that would settle the question; then word the Conclusion's last sentence conditionally in the same terms. Running the braking prior in the closed loop of Supplement S3 is an optional stronger fix.
4. [Table IV; §III-A; §IV-D; §V-C; §V-D; §I, contribution 3] By the Journal-Fit Reviewer's estimate from word and display-item counts (not a typeset count), the main text needs 12–14 printed pages against the recommended 10, mostly because of appendix-grade material and repetition. Move appendix-grade material to the Supplement or cut it without removing any result: reduce Table IV to five rows, move §V-D to Supplement S9 with a two-sentence summary, move the §III-A stopping-point paragraph to Supplement S2, condense the signed-caution and stop-deceleration paragraphs, replace inline provenance markers with one sentence, state each headline number once, and cut contribution 3 to two sentences. Keep the 3 s signed-caution values that item 11 adds visible in the main text in compact form, and give the revised page estimate in your response.
5. [Abstract] The 249-word Abstract uses step and convex-hull frontiers, phase shares and the phrase *those plans* without definition, carries about twenty numbers, and ends on what cannot be measured (“unless those plans count as unsafe, too little room remains, phase by phase”). Rewrite it in plain terms in about 200–230 words: the question, the method in one sentence, three results and one sentence of implication. Define the term *commitment* at its first use, drop the frontier types, the phase shares and the count (ii) clause or define them in words, and record any mapping to the plan's consequence rules in Table S4. The rewritten Abstract must stay within 250 words and carry the wording changes that items 1, 8, 10, 11, 13 and 17 require.

**Submission readiness and deposit**

6. [Author block; Acknowledgment] The author block is a placeholder (“[AUTHOR BLOCK: filled by the author]”), and the AI-use disclosure is an unapproved draft with bracketed placeholders for the model, the version and the scope of verification; as it stands, the manuscript would be returned before review. Complete the author block. In the Acknowledgment, delete the approval note, name the tool and its version, state the sections that contain AI-generated text, the extent of AI involvement in the code and the literature summaries, and what you verified, and reconcile the disclosure with the first Acknowledgment paragraph.
7. [Data and Code Availability; external archive] The Data and Code Availability statement is a placeholder (“[repository and DOI to be added by the author]”), while §IV-D says “The plan, its SHA-256 and every amendment are released with the code”, so the pre-specification cannot be checked. Deposit, under an archived DOI that referees can access, both plans with all amendments and lock manifests, the analysis code, and the per-decision arrays needed to recompute Tables II–IV (clearances, critical values for every arm, truth windows, phase labels, run identifiers). Give the repository URL and DOI in the statement, and state which raw recordings can be shared.

**Intervals for the step-frontier shares**

8. [Abstract; §I, contribution 2; §V-A; §VII] The phrase “at most about 0.4%” is the upper end of a basic bootstrap interval chosen after the results, with unverified coverage; the lower end of that interval excludes zero, while the percentile interval includes it. Replace the phrase with a bound from the interval method validated under item 9, or with a descriptive statement (0.6 of 8,290 decisions; largest of 20,000 resamples 0.25%). If you keep a basic interval, print both of its ends.
9. [§IV-B; §V-A; Table II; Table S5] RR(N) and RR(NA) are ratios of step-frontier (running-minimum) differences, for which naive percentile and basic bootstraps are not generally consistent. The RR(N) point lies outside its own intervals (“The point lies above the 97.5th percentile of its run-bootstrap distribution”), the wording for the NIS-inflated covariance rests on the same machinery applied to 35 unequal, unstratified runs, and the paper does not say whether the 201 caution levels are rebuilt in each resample. State in §IV-B whether the caution grid is rebuilt per resample; estimate the actual coverage of the percentile and basic intervals for RR(N) and RR(NA) on the stored arrays, by a run-level double bootstrap or by m-out-of-n subsampling of runs; report the primary intervals from a method that passes, with a sensitivity analysis stratified by recording setting α; and re-apply the five fixed rules for the NIS-inflated wording and print the branch they select.

**Estimands behind the secondary headline numbers**

10. [Abstract; §IV-C; §V-C; Table III; Table S6; Table S10] At τ = 0.75 s, 5,356 decision–row pairs cannot be judged within the 3 s window, against 3,334 pairs judged unsafe (“Count (ii) is driven by these pairs, which outnumber the 3,334 unsafe pairs”). The as-scored result and count (ii) are two single imputations that do not bound the room, yet only 153 pairs have a stop still unfinished when the recording ends. Judge each censored pair against the logged truth beyond the 3 s window until its stop finishes, restricting the evaluated population to decisions whose logged future covers the stop if needed; report that, with its interval, as the reaction-and-stop estimate, keep counts (i) and (ii) as sensitivity analyses, and stop presenting the two counts as separate findings in the Abstract. If the logged truth cannot be used, explain why and present the two counts as imputation alternatives.
11. [§IV-A; Table II; Table S5; Abstract; §VII] Caution is averaged only over decisions whose selected row is truly safe (“Decisions whose selected row is unsafe do not enter this average”), so it conditions on the outcome. At τ = 0.75 s the signed alternative reversed the braking prior's sign with the ego moving and phase-weighted, but the 3 s headline shares (83%, 0.665, 0.61, 38%) were never rerun with it. Rerun the 3 s scoring with caution counted over all evaluated decisions (signed) for every arm and every population of Table S5, using the existing signed-caution code; print the results beside Table II; and revise the Abstract's 83% sentence and the Conclusion wherever the ego-moving or phase-weighted value changes sign or branch.
12. [§IV-B; §V-A; §VI; §VII] Since 82.7% of evaluated decisions come after the stop, the pooled room (5.56 points) is weighted by how long each recording ran after the stop; it is 2.6 times the decision-weighted mean of the phase rooms, and about two-thirds of the braking prior's pooled gain is attributed to a cross-phase mechanism that §IV-B itself calls “a mechanism that no analysis here isolates”. Cap each run's post-stop segment at stated durations (for example 1, 2 and 5 s) and recompute R and every RR. Give F0 and each arm one margin scale per phase and trace the frontier at equal total caution, which separates the value of knowing the phase from per-decision information, and word contribution 3 and §VII according to the result.
13. [Abstract; §VII] The Abstract and the Conclusion give only the pooled figure (“a fixed 3 m/s² braking prior recovers 83% [75%, 90%]”), although with the ego moving the share is 0.47 [0.35, 0.57] and against a perfect oracle, phase-weighted, it is 0.665. Print the ego-moving share and/or the phase-weighted perfect-oracle share beside the 83%, name the population that defines the room, and trim elsewhere to stay within the abstract limit.

**Configuration needed to regenerate the data**

14. [§III-A, new table, or Supplement S1 and Supplement S2] The tracker is “configured as in [9]”, a manuscript under review, and the CARLA version, map, weather and sensor simulation, the CenterPoint checkpoint and its training data, CANMOT's per-class noise and gating, the per-run scenario parameters and the recording planner's settings are not given. Add a configuration table with these items, including CANMOT's per-class process and measurement noise and each run's initial gap, onset time and deceleration, with software versions.

**The braking prior and the regulatory model**

15. [§II; §VI] Calling the braking prior CK3 “an RSS-style assumption [37]” is inaccurate: RSS is a worst-case envelope, whereas CK3 is a nominal constant-deceleration prediction, and the paper uses the same label for both CK3 and the stopping rule of Supplement S3.1. Call CK3 a constant-deceleration braking prediction (3 m/s²) throughout and place it among physics-based motion models, drop the RSS-style label for it, add one sentence contrasting it with RSS's worst-case bound on the front vehicle's braking, and keep the RSS label only for the rule of Supplement S3.1.
16. [§III-C; §VI Limits] The value 3 m/s² lies inside the recorded leads' braking range (2.0–5.5 m/s²), and the manuscript does not say how it was chosen. State how 3 m/s² was chosen on the tuning runs, and state in §VI Limits that it lies inside the evaluation runs' lead-braking range. A sweep over the assumed deceleration is optional and appears as item 40.
17. [Abstract; §IV-C; Table S6; §VI Limits] A wrong go is defined as contact and the reaction-and-stop scoring uses a zero standstill gap, but the adopted performance model 2 of the 01 series of UN Regulation No. 157 also specifies a 2 m gap at standstill and 7 m/s² for the other vehicle. At that 2 m gap the 3 s oracle is no longer an oracle, and no perfect oracle is reported there. State in the Abstract's commitment sentence, in §IV-C and in Limits that a wrong go means contact at zero standstill gap and that model 2's 2 m gap and 7 m/s² are not used, and why. Using the existing safe-row flags, score the perfect oracle O at a 2 m gap under the 3 s and the τ = 0.75 s scorings and report den₀, with RR₀(N) and RR₀(CK3) where evaluable, or state that no share is evaluable.
18. [§V-C; §VI Limits] The sentence “The as-scored conclusion at τ = 0.75 s therefore rests on the performance-model values of the 01 series” implies regulatory backing that the scoring does not have: only two ego parameters of the model are used, with a zero gap, and outside the regulation's scope of automated lane keeping. Replace it, and the matching Limits clause, with wording that the scoring uses two ego parameters of performance model 2 (0.75 s, 6 m/s²) as a nominal parameterisation with a zero standstill gap, so that no sentence says the conclusion rests on the regulation's values.

**Scope of the covariance null**

19. [§I Scope; §VI; §VI Limits] Nothing stops a reader from replacing a deployed stack's covariance margin with a class constant, yet every lead-braking decision has a mature track, and newly detected, re-acquired or cut-in actors are essentially absent from the evaluated decisions. State in §I Scope and §VI that the results do not support removing or freezing a deployed stack's covariance margin; from the stored arrays, count the evaluated decisions within about 1 s of the 45 track initialisations and report D(N, F0) on them, or state that they are too few; and name newly detected, re-acquired and cut-in actors as untested in Limits.
20. [Tuning runs of the other five scenario families] A deployed stack tunes one margin scale across its whole operating domain, and, by the perspective reviewer's inference from the paper's own phase finding, a covariance whose level differs by scenario family could carry value that a single-family test cannot see. Apply the ground-truth-free ratio check of Fig. 2(b) to the tuning runs of the other five scenario families and report the median N/F0 margin ratio on binding rows for each; if the levels differ, state that a single tuned scale could reallocate caution across families and that this is untested.

## Suggested Changes

Please answer each of these as well, saying whether you adopted it and, if not, why. Items marked Optional are stronger fixes that a reviewer offered as optional.

21. [New evaluation on a tracker output with a per-decision covariance] Optional: the method is shown to discriminate only on synthetic graded oracles. Apply the same evaluation to one source whose covariance varies per decision, such as the calibrated covariance of [9] or an IMM tracker.
22. [§II; Supplement S6] Positioning against ITS-venue work is thin: §II does not cover threat assessment and collision probability, or IMM and adaptive-filter trackers in adaptive cruise control and collision warning, and Supplement S6 says the IMM and adaptive-filtering literature was not searched for a planner-side test. Extend the novelty search to these areas, add a §II paragraph positioning the paper against that work, and qualify the Novelty paragraph if needed.
23. [Cover letter; reference list] The related manuscript [9] shares the detector architecture, the tracker configuration and the margin form, and the positioning rests partly on 2026 preprints. Upload [9] as a confidential related manuscript and state in the cover letter what is shared and what is new; cite published versions of [8], [14], [17] and [19] where they exist.
24. [§I; Notation table in §IV] Paper-specific terms (room, caution, commitment, phase-weighted, avoidable wrong-go, perfect oracle) are used before §IV defines them, and there is no plain-language statement of the results. Give plain one-sentence definitions of room, caution and the two commitment models in §I, move the Notation table to the start of §IV, and add a plain summary of two or three sentences.
25. [Text after §III-C; Table III; Table S6; Fig. 4(b)] Arm names drift (the NIS-inflated arm is also called an innovation-inflated variant or the inflated covariance, and CK3 and F0 each have several names), and Table III, Table S6 and Fig. 4(b) use R and RR(N) for quantities the Notation table names differently. Use one name per arm after §III-C, and relabel Table III, Table S6 and Fig. 4(b) with RR_E(N) and a distinct symbol for the 3 s oracle's advantage under the reaction-and-stop scoring.
26. [§IV-B] The graded-oracle check of Table S12, which governs how every phase share is read, appears only in the Supplement. Bring a compact version into §IV-B or beside Fig. 3: partial oracles at p = 0.25, 0.5 and 0.75 for all decisions, ego moving, lead braking and phase-weighted, under the 3 s scoring.
27. [§IV-C; §IV-D; §V-C; Acknowledgment] The main text narrates the project's history and refers to earlier reviews (“Two further checks follow review requests”) and to rules governing the abstract. Describe post hoc analyses neutrally, drop the references to reviews and to rules governing the abstract, keep the audit trail in Supplement S4, and declare any previous venue in the cover letter.
28. [Captions of Figs. 1–4 and Tables I–IV] Each main figure and table has a short caption in the paper and a longer one in a separate supplementary captions file, and only the in-paper caption travels with the figure. Give each figure and table one self-contained caption in the paper (data, number of decisions, interval type, frontier) and drop the supplementary duplicate.
29. [Fig. 2(b) and its caption] The 1,127 rows outside the 5% band of Fig. 2(b), including a small group near a ratio of 1.7, are unexplained. Characterise them by track age, for example whether they come from re-initialised tracks, in the text and the caption; this also supports the deployment fence of item 19.
30. [Throughout] Number formats and precision vary: shares appear as percentages in the Abstract and §I but as decimals with three to six significant figures in the body and tables, and the braking prior's share is printed as 0.8315, 0.831 and 83%. Adopt one convention, for example percentages to two significant figures in prose and decimals to three in tables, with intervals rounded to the precision the bootstrap supports.
31. [Abstract] The phrase “On 35 runs not used to design the margins” is accurate for the margin sources, but an earlier exploratory analysis had examined these runs for the room and the tracker covariance, so for those two quantities the evaluation is a transfer, not a replication. Qualify the phrase accordingly.
32. [Index Terms] None of the Index Terms names car following, adaptive cruise control, safety evaluation or simulation-based testing, which is how ITS readers would search for the work. Add two or three such terms.
33. [Supplement S1] The planner replay was checked on the tuning runs only, and the counterfactual assumption that no actor's logged motion would change with the ego's choice is unstated. Reproduce the logged selections on the evaluation runs with the recorded α, β, p and q, and state that lead braking is scripted and no actor's logged trajectory depends on the ego, or quantify where it does.
34. [§III-A, paragraph 1] Five runs contribute only 18–53 evaluated decisions each, the paper does not say why they are short, and they were never removed together, although they may carry a disproportionate part of the NIS-inflated effect. State why the five runs are short, count how many of the 217 changed NIS-inflated decisions and of the 304 actor-decisions with λ > 1 fall in them, and recompute R, RR(N) and RR(NA) with all five excluded.
35. [§IV-C; §IV-D; Supplement S8.1] The 10-decision-equivalent threshold, described as “a resolution rule of our choosing”, decides the Abstract's last sentence and has no sensitivity check, and §IV-D does not say what was already known when it was set. Report the branch the rule gives at other thresholds (for example 5 and 20), base evaluability on den₀'s lower interval limit as a sensitivity analysis, and disclose in §IV-D what was already known.
36. [Table S9; Table S10] Where den₀'s interval approaches zero, percentile intervals for the ratio are unstable; for example, the braking prior's share while the lead brakes under count (ii) is printed as 0.27 [0.10, 1.24]. In such cells, report D and den₀ with their joint interval or a Fieller-type interval for the ratio, and flag the cell.
37. [Abstract; §VII] The commitment analyses were added after the first results and are descriptive, but neither the Abstract nor the Conclusion says so. Mark them as descriptive analyses added after the first results, in the Abstract or at least in the Conclusion.
38. [Abstract; §VI] Every evaluation run contains a braking lead, so the braking prior's cost where no braking follows is unmeasured (“its cost where braking never comes is untested here”). Score CK3 against F0 on the project's benign-driving and other-family runs, or add to the Abstract's 83% sentence that it holds on runs in which the lead always brakes.
39. [Table S12; Supplement S8.1] The partial and noisy oracles rest on a single random draw per decision. Repeat them over about 50 draws and report the spread across draws in Table S12.
40. [§VI; braking prior CK3] Optional: the 83% is reported at one assumed deceleration, which matches the scenarios. Report RR(CK3) over a sweep of the assumed deceleration, for example 2, 4, 6 and 7 m/s².
41. [§II; contribution 2] Optional: compute the tracker's steady-state covariance at the update interval and the margin ratio it implies, which would make contribution 2 a quantitative check of the theory, and show how common fixed-noise Kalman trackers are in automated-driving perception.
42. [§III-B; Table I] The margin is the posterior propagated without process noise, but §III-B and Table I do not say so; it is stated only in Supplement S9. State this in §III-B and Table I with the reason, and note that a common class-level process noise would leave the comparison of N with F0 unchanged; optionally, report the room and RR(CK3) with F P Fᵀ + Q for F0.
43. [§II; §V-B heading; §VI] The heading “An Adaptive Covariance and Simple Priors” and the framing in §II suggest a test of adaptive filtering, but the NIS-inflated arm scales only the output covariance and leaves the state estimate unchanged. Retitle §V-B, state in §II and §VI that this arm isolates the covariance channel and not the gain or state-estimate effect of adaptive filtering, and list that effect with IMM as untested.
44. [§VI, paragraph 1; §VII] §VI and §VII cite the deviation-ranking check of §V-D as further evidence, but because the tracker's and the class average's deviations are nearly monotone transforms of each other, the check is not independent of the ratio result. Present §V-D in §VI and §VII as a consistency check of the ratio result that locates the ranking in the state's age, or test the covariance's own variation per phase directly.
45. [§III-A; §VI Limits] The update rate (“the tracker updates the lead at about 2 Hz”) sets the state's age, which drives the error ranking of §V-D and part of the lead-braking room, but it is neither justified nor listed as a limit. State where the rate comes from, add it to Limits, and scope the §V-D ranking and the lead-braking room to it.
46. [§VII] The Conclusion's location claim is a ranking among the tested sources, and a constant time-gap margin, the standard margin in car following, was not tested. Phrase the claim as a ranking among the tested sources and name the constant time-gap margin as untested.
47. [Table I] Optional: add a constant time-gap arm swept like the others, for example s = (h·v_ego)², or the minimum following distance of UN Regulation No. 157 used as a margin.
48. [§IV-C] The values of the 01 series are borrowed from outside the regulation's scope of automated lane keeping and are given more authority than their role supports. Describe them in §IV-C as nominal reference parameters borrowed from a lane-keeping performance model, with no claim about lane-keeping systems or about compliance, and state the regulation's scope.
49. [§V-C; Table III] The result is stated at 0.75 s and 6 m/s², although Table III shows the ratio moving widely with τ and with the stop deceleration. Present the sweeps over τ and the stop deceleration as the result, with 0.75 s and 6 m/s² as one point on them.
50. [§I Scope; §III-A; §V-C; §VI] Recorded leads brake at 2.0–5.5 m/s², milder than the assumed 6 m/s² stop and the regulation's following test, and the 12% and 53% do not say so. State the 2.0–5.5 m/s² range in §III-A and §I Scope, qualify the 12% and 53% as holding for leads braking at up to 5.5 m/s², and add to Limits that the closed-loop and open-loop runs cover different braking severities.
51. [Supplement S3; Fig. S3 caption; §VI] The closed-loop check's starting-gap figures appear without the fact that its planners were in full-braking fallback in 0.70–0.72 of decisions, or the count of contacts, so they can be read as design guidance. Add the fallback share and the contact count to the opening of Supplement S3, the Fig. S3 caption and §VI, and state that the gap figures are not design guidance.
52. [§VI; Table S7] The paragraph beginning “The prior has costs” names lost progress but not occupants' comfort or the exposure of following traffic, and no arm's braking demand is reported. Name occupants' comfort and following traffic as unmeasured costs, and as a proxy report each arm's selected-row first target acceleration or peak jerk at matched caution.
53. [§I Scope] §I Scope excludes other road users and scenarios without naming them. List those left out: pedestrians, cyclists, crossing and cut-in actors, vehicles behind the ego, and real sensor data.
54. [Notation table] The paper's terms are not related to established ITS and safety vocabulary. Add a column to the Notation table that maps each term to its nearest established counterpart (criticality metric, proper response, over-conservatism, value of perfect information).
55. [§VI, “What carries over”] The transferable ratio check has no decision rule and no guidance for planners of other types. Give it a worked threshold, stated as unvalidated; say how to find binding constraints in other planner types; require it to be run over the full scenario mix; and note that the graded oracles need ground truth.
56. [§III-A] The road type and setting of the CARLA recordings are not stated. Give them in §III-A.
57. [Table S12; Abstract; §VII] The oracle sets each margin from the realised error, so it sizes a room a covariance may not be able to use: a covariance acts mainly through the per-decision scale, and the room open to that scale is never measured, so the contrast between “at most about 0.4%” and the braking prior's 83% is not like for like. Add a positive control in the covariance's own form (a per-decision covariance, or a multiple of the class average, fitted to the realised 3 s error and projected as N) and report RR(N) and RR(NA) against it; otherwise rephrase the contrast between the braking prior and the covariance as one between a mean-path correction and variance margins.
58. [Abstract; §VII; closed-loop simulator of Supplement S3] Every decision state was produced by a planner whose margin used the tracker's covariance, so the braking prior is scored on states its own planner would not visit, and the closed-loop check never runs it. Run CK3 (and the NIS-inflated arm) in the existing simplified closed-loop simulator on the same episodes, or reweight the open-loop decisions toward states a CK3 planner would visit; until then, call the 83% an open-loop, off-policy share in the Abstract and §VII.

## Questions for the Authors

None beyond the changes: the Journal-Fit Reviewer's four questions (repository access during review, whether the reviews mentioned in §IV-C and §IV-D belong to an earlier submission, which commitment model is representative, and any overlap with [9]) are covered by items 7, 27, 3 and 23.

## Appendix

### How This Review Was Run

- Five AI-simulated reviewer roles reviewed the manuscript: a Journal-Fit Reviewer in the editor's seat, a methodology reviewer, a domain reviewer, a perspective reviewer and a Devil's Advocate. An editorial synthesis then applied the review's decision rules, arbitrated the disagreements between reviewers and wrote the decision package.
- All five roles ran on one model family (claude-opus-5-5, from Anthropic). The recorded provenance shows each role reviewing the paper in its own fresh context, separated by role and without access to the other roles' output; each role's earlier planning step, written before it saw the paper, is reported to have run in a separate fresh context as well. This is role separation, not a claim that the reviewers are independent: with one model family, their errors may be correlated.
- The reviewer configuration cards were accepted by the user before the reviews began.
- This letter is written for reading. A re-review or the revision coach takes the decision package, not this letter.

### Limits of This Review

- The review is AI-simulated and is not calibrated against human reviewers.
- The whole manuscript was read: the main text, the Supplement with all its tables, the supplementary captions file and every figure image. The references were read as printed and not checked against external records, and no code or data repository was available to inspect.
- No criteria from the target journal were supplied, so venue fit was judged only against the stated constraints (regular paper, abstract of at most 250 words, 10 pages recommended).

### Reviewer Summaries

- Journal-Fit Reviewer: the paper is in scope, careful and candid, but the headline leads with an expected null, the practical take-away under the realistic commitment is unstated, and the abstract, the length and the placeholders put the desk-rejection risk at moderate as the text stands, low once those items are fixed. Its preliminary signal was major revision.
- Methodology reviewer: the design is unusually strong and every headline number matches its table, but the step-frontier intervals are unvalidated and three estimand choices (the imputation of censored plans, caution that conditions on the outcome, pooled weighting) move the secondary headline numbers. All of these are repairable from the stored arrays.
- Domain reviewer: the paper is accurate for the domain on its central claim, but the braking prior is mislabelled RSS-style at a deceleration that matches the scenarios, and the room is defined for contact only, under a regulatory model whose 2 m gap is set aside.
- Perspective reviewer: the paper is scoped with care, but the null is not fenced against removing covariance margins in deployed stacks, the regulatory performance model is adopted only in part, and the costs and terms are not framed for safety-assurance readers.
- Devil's Advocate: the title question is settled by the Riccati steady state before any decision is scored; the room and its location, which the decision-level machinery adds, are not mainly about uncertainty, and the location claim rests on pooling, imputation, conditioned caution and off-policy premises. It raised no unresolved critical challenge.

### Advisory Checks

These checks are advisory: they do not change the decision, and nothing in the body above comes from them.

- Acronym check: over the body and the English abstract, it lists CANMOT and CARLA (body and abstract), RR, RMS, SHA, AI and IEEE as used without definition, NIS as defined twice, and capitalised placeholder and heading words (AUTHOR, BLOCK, TABLE, IV, TO); it could not check IMM, RSS and NA, whose initials do not match the words before their parentheses.
- Suggested-reference check: of the nine works the domain and perspective reviewers suggested, eight were found in an index; for ISO 21448:2022 the title was not matched and there was no DOI or arXiv ID to check (found means that the record exists, not that it supports the point).
- Reviewer claim check: of 55 reviewer findings, the judge marked one as contradicted by the manuscript (the domain reviewer's point that the title asks as an open question what filter theory already answers, set against the Abstract's first sentence, which names CANMOT as a fixed-noise Kalman tracker) and two as not checkable from the manuscript alone; you decide what to make of each.

### Item Map

Each numbered change above and its reference in the decision package.

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
| 14 | R14 |
| 15 | R15 |
| 16 | R16 |
| 17 | R17 |
| 18 | R18 |
| 19 | R19 |
| 20 | R20 |
| 21 | S1 |
| 22 | S2 |
| 23 | S3 |
| 24 | S4 |
| 25 | S5 |
| 26 | S6 |
| 27 | S7 |
| 28 | S8 |
| 29 | S9 |
| 30 | S10 |
| 31 | S11 |
| 32 | S12 |
| 33 | S13 |
| 34 | S14 |
| 35 | S15 |
| 36 | S16 |
| 37 | S17 |
| 38 | S18 |
| 39 | S19 |
| 40 | S20 |
| 41 | S21 |
| 42 | S22 |
| 43 | S23 |
| 44 | S24 |
| 45 | S25 |
| 46 | S26 |
| 47 | S27 |
| 48 | S28 |
| 49 | S29 |
| 50 | S30 |
| 51 | S31 |
| 52 | S32 |
| 53 | S33 |
| 54 | S34 |
| 55 | S35 |
| 56 | S36 |
| 57 | S37 |
| 58 | S38 |
