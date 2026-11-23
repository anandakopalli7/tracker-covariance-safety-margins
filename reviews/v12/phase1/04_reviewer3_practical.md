# Peer Review Report

## Manuscript Information
- **Title**: Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution: A Fixed-Noise Kalman Tracker in CARLA Lead Braking (draft v12)
- **Manuscript ID**: not available (fresh submission to IEEE Open Journal of Intelligent Transportation Systems, regular paper)
- **Review Date**: 2026-11-19
- **Review Round**: Round 1 (reviewed as a new submission)

---

## Reviewer Information

### Reviewer Role *
Peer Reviewer 3 (Cross-disciplinary / Practical)

### Reviewer Identity *
Automated-driving safety-assurance practitioner: adaptive cruise control and emergency braking, scenario-based testing, regulation and responsibility-sensitive models. Experienced in the gap between open-loop offline metrics and closed-loop fleet behaviour, and in who carries the cost of a safety function. I am an outsider to estimator theory and to bootstrap details; those are left to other seats.

### Review Focus *
External validity of the test bed for intelligent-transportation practice; the use of regulation- and RSS-derived parameters and the "nominal reference, no compliance" wording; stakeholder scope (who benefits, who bears the cost of stop-dependent plans, which road users are outside the test); and whether a safety engineer could act on the paper's practical reading without over-reading it.

---

## Overall Assessment *

### Recommendation *
- [ ] **Accept**
- [ ] **Minor Revision**
- [x] **Major Revision** — Substantial revisions needed, re-review required after revision
- [ ] **Reject**

### Confidence Score *
4. The test bed, the regulation use and the practical reading are within my practice; estimator and bootstrap details are outside it.

Confidence is an uncertainty/scope disclosure only; it never changes consensus counts, severity, decision bearing, or arbitration.

### Summary Assessment *
The paper asks whether the covariance of a fixed-noise Kalman tracker (CANMOT) beats a class-average margin in a margin-type speed planner, scored at equal caution against logged futures in 35 CARLA lead-braking runs, with an oracle margin as positive control. It finds that the tracker's margin is a near-constant 1.10 multiple of the class average's and recovers nothing distinguishable from a grid offset, while an oracle has 5.6 points of room that mostly sits before the lead's stop and in the first second after it. As an evaluation design, with a placebo, graded oracles and unusually frank limits, the paper is careful and useful. From a practitioner's seat the test bed is narrow where it matters: a 2 Hz detector without latency, a lead that always brakes at no more than 5.5 m/s², and an emergency stop of 6 m/s² that is perfect, free and independent of perception. The headline 12% and 83% figures depend on those choices, and magnitudes move several-fold with the recording policy. The practical reading is well hedged in Section VI but less so in the abstract and conclusion. I recommend major revision: the null for this tracker is credible; the transfer claims need either new runs or narrower wording.

---

## Strengths *

### S1: A positive control and graded oracles make the null interpretable
A practitioner can tell that "the covariance recovers nothing" is not a blunt-measure artefact, because oracle mixtures at 25%, 50% and 75% recover 0.27, 0.54 and 0.78 of the pooled room. The paper also says honestly where the measure does not grade (lead braking, ego moving).
**Evidence Anchor**: `text: §IV-B "Pooled and after the stop, the measure therefore grades partial information"`

### S2: The scope and limits are stated plainly, including expected directions of the simplifications
Section I lists the excluded road users and the dominance of stationary decisions. Supplement S11.9 states the direction in which latency, slower updates, misses and curved roads would move the results. This is rare and helps an assessor.
**Evidence Anchor**: `text: §I Scope "so pooled figures are dominated by stationary decisions"`

### S3: The cost side of stop-dependent plans is at least counted
Table S36 reports the share of decisions whose selected row is safe only because the stop follows: 5.8% of all decisions, 19.0% with the ego moving and 41.7% while the lead brakes, for the class average. The main text carries these figures into Section VI. Many offline-metric papers omit this.
**Evidence Anchor**: `table: Table S36 — class-average column: All 5.8%, Ego moving 19.0%, Lead braking 41.7%; perfect oracle O: 72.3%`

### S4: Regulation values are labelled as nominal reference parameters, with no compliance claim
The 0.75 s, 6 m/s² and 12.65 m/s³ values are named as borrowed, their source table is cited, and the 2 m standstill gap is given as a sensitivity rather than hidden. This is the right register for a regulation-derived parameter set.
**Evidence Anchor**: `text: §IV-C "We borrow them as nominal reference parameters from a motorway lane-keeping regulation and claim no compliance"`

### S5: The ratio check needs no ground truth and is cheap for an assessor to reproduce
The tracker-to-class-average margin ratio by scenario family (Table V) separates families where the null is expected (lead braking, stopped vehicle, cut-in: 98.7–99.9% of rows within 5%) from those where it is silent (crossings: 4.1–8.5%). It is a usable diagnostic beyond this tracker.
**Evidence Anchor**: `table: Table V — Lead braking 99.26%, Pedestrian crossing 8.51%, Vehicle crossing 4.09% of rows within 5% of the median`

### S6: The conditional practical statement and the call to report commitment, population and recording policy are actionable
The abstract's last sentence and the Section VI paragraph on commitments tell an assessor what must be stated with any open-loop decision score.
**Evidence Anchor**: `text: Abstract "Open-loop decision scores should state their commitment, population and recording policy."`

### S7: Disclosure of history and AI use is complete and plainly worded
The paper says the plan was not registered with a third party, lists amendments with hashes, marks every added analysis as exploratory, and says the second programs were written by an AI model and were not blind to results. As a new submission, the disclosure is complete; its density is a readability issue only (Minor Issues).
**Evidence Anchor**: `text: §IV-D "are exploratory and descriptive"`

---

## Weaknesses *

### W1: The "12% remains" reading rests on a perfect, free stop that is independent of the perception being studied
**Problem**: The reaction-and-stop scoring has the ego make an unconditional stop at 6 m/s² (jerk 12.65 m/s³) 0.75 s after each decision, executed perfectly. In practice the function that delivers such a stop is triggered by a perception chain (the same sensors and a tracker of the same state age), so its delay and misses are correlated with the errors the oracle margin removes. The paper does not score a stop whose trigger shares the tracker's lag or whose delay varies, nor any cost for the stop (comfort, rear-end exposure, progress). The abstract states the result as "a perfect 6 m/s² emergency stop 0.75 s after each decision leaves 12% of it".
**Evidence Anchor**: `text: §VI "the reading assumes that the stop always comes"`
**Why it matters**: A designer could read the 12% as "an AEB fallback makes the margin source nearly irrelevant". That follows only if the fallback is independent of the tracker and always fires. The common-cause case is the practically interesting one.
**Suggestion**: Add a scoring in which the stop starts from the tracker's own belief (state age up to 0.4 s, velocity lag), or with a stop delay drawn from a stated distribution, and report how the 12% moves. State in the abstract that the stop is assumed perception-independent.
**Severity**: Major
**Confidence**: 4 — core expertise: emergency-braking function design and common-cause analysis

### W2: The stop deceleration exceeds every lead deceleration in the test bed, so the "little room remains" result is partly built in
**Problem**: Realised lead deceleration is 2.09–5.46 m/s² on the evaluation runs, while the stop scoring uses 6 m/s². The ratio of remaining room moves from 0.29 at 4 m/s² to 0.06 at 7.6 m/s² (Section V-D), which shows how strongly the result depends on the ego-to-lead deceleration relation. The paper's own closed-loop check assumes the other vehicle can brake at 7 m/s² (Supplement S3.1), above the 6 m/s² ego stop. No analysis stratifies the stop-scoring room by the lead's realised deceleration, and no run has a lead braking harder than 5.5 m/s².
**Evidence Anchor**: `table: Table S28 — realised lead deceleration 2.09–5.46 m/s² (evaluation runs), against the 6 m/s² stop of Table III`
**Why it matters**: Hard-braking leads (6–9 m/s², cut-in-and-brake) are the cases an AEB or ACC assessor cares about. The 12% may be an artefact of leads that the stop can always out-brake.
**Suggestion**: Report the stop-scoring room by terciles of the lead's realised deceleration, and add runs with leads braking at 6–8 m/s². Otherwise restrict the abstract and conclusion to "leads braking at up to 5.5 m/s²".
**Severity**: Major
**Confidence**: 3 — adjacent field: judging from the reported ranges, without the per-run data

### W3: The test-bed perception is benign and slow, and the mechanism that carries the room is an artefact of that choice
**Problem**: The detector runs at 2 Hz with no latency, the tracker steps at 0.5 s, the lidar is simulated with simulator noise off, and the tracker's position innovations are about eight times too wide (median mean NIS 0.24 against 2). The paper shows that the after-stop room lies in the first second after the stop, where the tracker's velocity lags (Section V-C), and says that a faster update would shrink the room and the braking prediction's share (Supplement S11.9). Production ADAS and AEB perception runs at 10–20 Hz with tens of milliseconds of latency, and typically has direct range-rate measurements. So the size of the room, and the 83%, are conditional on the slowest-plausible update, and the null for the covariance is close to guaranteed by construction (Riccati steady state).
**Evidence Anchor**: `text: §III-A "run at 2 Hz, with no latency simulated"`
**Why it matters**: The headline numbers cannot be transferred to a stack with a faster tracker, and a safety engineer cannot tell from the paper whether the room becomes small or stays. The expected direction is stated but not measured.
**Suggestion**: Re-run the detector and tracker on the existing 20 Hz recordings at 5 and 10 Hz (overlapping sweep windows) with a stated latency, and report R, the braking prediction's share and the per-phase split at each rate. If that is not possible, say in the abstract that all magnitudes hold for a 2 Hz detector with 0.5 s tracker steps.
**Severity**: Major
**Confidence**: 4 — core expertise: ADAS perception rates and latency budgets

### W4: Absolute and relative results move several-fold with the recording policy, so "only comparisons between sources transfer" is not demonstrated
**Problem**: The paper says that "only comparisons between sources on the same decisions are meant to transfer". Table S35 shows that between the 20 tuning runs and the 35 evaluation runs the room is 1.18 against 5.56 points, the braking prediction's share is 0.377 against 0.831, and in the lead-stopped phase the acceleration margin's share is 0.063 against 0.702. The evaluation runs were recorded by a planner whose margin used the tracker's own covariance (α p + β q) and ended at contact in 5 of 35 runs; the tuning runs used a unit-variance margin and ended at contact in 10 of 20. Source comparisons therefore change with the recorded states, not only the magnitudes.
**Evidence Anchor**: `table: Table S35 — Room R all 1.18 vs 5.56 pp; RR(CK3) all 0.377 vs 0.831; RR(AM) lead stopped 0.063 vs 0.702`
**Why it matters**: An assessor needs to know which statements survive a change of recording planner. The only statement that survives in the tables is the null for N; the ranking of the other sources is not stable per phase.
**Suggestion**: Either restrict the transfer claim to the null for the tracker covariance and to the ordering that holds in both run sets, or add a third recording policy (for example a time-gap or ACC-style recorder) and report the ranking across all three.
**Severity**: Major
**Confidence**: 4 — core expertise: open-loop versus closed-loop evaluation

### W5: The scenario is one-sided: the lead always brakes, so the cost of the best-performing source is unmeasured
**Problem**: The braking prediction recovers 83% of the room and is the source the discussion points to, yet its cost behind a lead that does not brake could not be measured. The benign runs contain no vehicle in the ego's lane, and the prediction changed the selected row in none of 5,420 decisions at zero margin (Supplement S10.6). Its zero-margin caution rises from 1.13% to 3.67% across the tested decelerations, and its costs to comfort and to following traffic were not measured. No run has the lead holding speed, braking mildly, stopping and pulling away, or following a stop-and-go pattern.
**Evidence Anchor**: `text: §VI "behind a lead that does not brake, its cost is untested"`
**Why it matters**: In practice nuisance braking is the dominant cost of any anticipatory margin, and the paper credits information about the lead's motion state with "most of the oracle's room". The benefit is shown on the one scenario that rewards anticipation; the false-alarm side is not.
**Suggestion**: Add lead-following runs without a hard brake (constant speed, mild braking below 1 m/s², stop-and-go) and report wrong-go and caution for the braking prediction and the phase schedule there. Otherwise state in the abstract that the braking prediction's cost is untested.
**Severity**: Major
**Confidence**: 4 — core expertise: ACC and AEB false-activation trade-offs

### W6: Headline figures are per decision, dominated by stationary decisions, with no event-level or severity-weighted outcome
**Problem**: 82.7% of evaluated decisions come after the lead has stopped and 77.5% have the ego at or below 0.5 m/s, and the length of that idle tail is set by the fixed 35 s recording. "Wrong-go counts ignore impact speed", and the paper reports no per-run or per-event outcome (for example the share of runs with contact at a matched caution). The paper recognises the population mix and reports phases, which mitigates the problem.
**Evidence Anchor**: `text: §VI Limits "Wrong-go counts ignore impact speed."`
**Why it matters**: A safety engineer reasons in events and severity. The 5.6 points are not a collision rate, and the pooled share changes with recording length.
**Suggestion**: Add one event-level table (runs with contact, and impact speed where there is contact, for F0, N, CK3 and TG at two matched caution levels) so a reader can relate the decision-level room to events.
**Severity**: Minor
**Confidence**: 4 — core expertise: scenario-based assessment

### W7: The caution against over-reading the null is in Section VI only
**Problem**: Section VI says that the finding "does not justify removing a covariance margin from a deployed stack", and gives the reasons (young tracks, crossings). The abstract and the conclusion carry the untested list but not that sentence. The abstract's "does no better than a placebo" is the sentence most likely to be quoted. The families where the covariance does vary (pedestrian and vehicle crossings) are the vulnerable-road-user and crossing scenarios, where the paper's check is silent.
**Evidence Anchor**: `absence: Abstract and Section VII — expected the sentence that the null does not justify removing a covariance margin; checked Abstract, Section I Scope, Section VII, Section VI first paragraph`
**Why it matters**: The practical reader who stops at the abstract can reach the opposite of the paper's own caution.
**Suggestion**: Add one sentence to the abstract and the conclusion: the null concerns a fixed-noise tracker in steady lead following and does not cover crossing actors, young tracks or other road users.
**Severity**: Minor
**Confidence**: 5 — core expertise: reading of results by assessors

### W8: The regulation parameters come from an ALKS motorway model, and the supplement's wording drifts toward compliance
**Problem**: The 0.75 s, 6 m/s² and 12.65 m/s³ values are from performance model 2 of UN R157 (01 series), an automated lane keeping regulation for motorways, while the test bed is a 5–15 m/s straight two-lane road with ADAS-like car following, and the 6 m/s² stop is said to "stand for a separate emergency-braking function". The 01-series text is cited as a WP.29 proposal document, read "in the text adopted in June 2022", so a reader cannot check whether the values are in force. Section II and IV-C use the right wording; the supplement's S3 measures starting gaps "above the R157 minimum" and quotes a statement that a planner braking as the regulation assumes would "pay 0.000 s". That reads as a compliance comparison, although S3 says the test beds lie outside the regulation's domain.
**Evidence Anchor**: `text: §VI Limits "nominal reference parameters, read in the text adopted in June 2022 [42]"`
**Why it matters**: Regulatory numbers carry authority; "no compliance" in Section IV-C does not protect a reader who meets the S3 sentences alone.
**Suggestion**: Cite the adopted regulation text and its in-force amendment status; say in S3 and in the abstract-level summary that no regulatory margin is claimed; relate the 6 m/s² stop to the deceleration envelopes of AEB and ACC functions the reader would know.
**Severity**: Minor
**Confidence**: 4 — core expertise: type-approval regulation

### W9: The time-gap baseline was added after the results and is a competitor, not a base
**Problem**: The constant time-gap margin was defined in Amendment 09 (after two review rounds) and computed on the evaluation runs only. It is scored as one more margin source (r0 = 2 m/s, with 1 and 4 m/s beside it), not as the policy to which a covariance would be added. The paper does not score a time-gap margin plus the tracker's covariance, which is the question a designer with an ACC stack has. With the ego moving the time-gap interval is [−0.032, 0.308] (Table II).
**Evidence Anchor**: `text: §III-C "was defined in Amendment 09 (Section IV-D) and computed on the evaluation runs only"`
**Why it matters**: The reading offered to designers is a comparison among replacements, not a statement about adding covariance to the policy in use.
**Suggestion**: Add a TG+N arm (time-gap variance plus the tracker covariance) and a TG+F0 arm, and state the headway range of the time-gap policy against the ranges of ACC practice.
**Severity**: Minor
**Confidence**: 3 — adjacent field: judged against ACC practice, not from the data

### W10: The closed-loop check runs no covariance margin, and its starting-gap figures can be over-read
**Problem**: The paper is explicit that Supplement S3 "runs no covariance margin" and is not design guidance. Even so, the quoted pre-fixed contact statement reports a starting gap "0.021 s above the R157 minimum", and the planner was in its full-braking fallback for 0.70–0.72 of decisions at those settings. The start gap is set by construction at 1.00–1.05 times the R157 minimum or the arm's own threshold, so the 0.021 s depends on the starting rule. The simulator understates the tracker's stopping-point error by about 40% at 15–30 m.
**Evidence Anchor**: `text: S3.4 "corresponds to a starting gap on average 0.021 s above the R157 minimum"`
**Why it matters**: A closed-loop figure in regulation units is the number an assessor will copy. Its cost (a fallback in about 70% of decisions) is stated in S3.4 but not in the same sentence.
**Suggestion**: Move the fallback share into the quoted statement, or drop the R157-unit statement from the supplement's summary; keep the main-text sentence that the check does not settle the question.
**Severity**: Minor
**Confidence**: 3 — adjacent field: closed-loop sizing practice

### W11: The phase schedule at 99.9% held out could be read as a design recommendation
**Problem**: The abstract reports that one scale per phase, with the tracker's own phase estimate, recovers 99.9% of the room held out. The schedule relaxes the margin once the tracker believes the lead has stopped, and the phase estimate exceeds the true phase because it labels 128 after-stop decisions as braking where the tracker still reports motion (Table S32 against Section V-C). It was found after the results, on one scenario family, scored open loop, and the lead decelerations are 2.1 m/s² or more. No test covers a lead that stops and pulls away, a mis-stated "stopped" belief or a gentle brake below the −1.0 m/s² threshold.
**Evidence Anchor**: `table: Table S32 — tracker-estimate phase labels, threshold −1.0 m/s²: in sample 0.984, held out like for like 0.999, against the single scale of record 0.964; agreement with truth 95.6%`
**Why it matters**: Relaxing a margin on a belief that the lead is stopped is a safety-relevant design move, and the paper's evidence for it is one benign scenario family.
**Suggestion**: Keep the figure as a diagnostic of where the room lies; say in the abstract that it is not a design result, and test the schedule on pull-away and gentle-brake runs before any design reading.
**Severity**: Minor
**Confidence**: 4 — core expertise: safety-function design review

### W12: The ratio check is a row share over whole runs, and the cut-in expectation is not tested at the critical moment
**Problem**: In cut-in runs 99.86% of 90,227 rows lie within 5% of the median, and the paper expects the null to carry over. The share is taken over all rows of 20 runs, so it is dominated by mature-track rows before and after the manoeuvre. The only age-resolved result shows ratios of 1.14 in the first 0.5 s and 1.68 after two missed updates (Table S27), and a cut-in is where a new track and a changing heading appear. A row share over a whole run can stay at 99.86% while the few rows at the event differ.
**Evidence Anchor**: `table: Table V — Cut-in 20 runs, 90,227 rows, 99.86% within 5% of the median 1.102`
**Why it matters**: The "where we expect the null to carry over" statement covers the scenario an assessor most wants (a cut-in), on evidence that cannot see the critical moment.
**Suggestion**: Report the ratio in a window around the cut-in event, and by track age, for the cut-in family; or drop cut-in from the expected-carry-over list.
**Severity**: Minor
**Confidence**: 3 — adjacent field: the row-level data are not in the package

### W13: ACC and AEB standards and test protocols are not engaged
**Problem**: The related work cites R157 and RSS but not the standards and protocols that govern car-following and emergency-braking functions, which is the community this journal serves.
**Evidence Anchor**: `absence: Section II and the reference list — expected ACC and AEB performance standards and test protocols (for example ISO 15622, ISO 22179, UN R152, IEEE 2846); checked Section II, references [1]-[58], Supplement S6`
**Why it matters**: Without them a practitioner cannot place the time-gap policy, the 6 m/s² stop or the lead decelerations against accepted envelopes.
**Suggestion**: Add a short paragraph relating the time-gap range, the stop deceleration and the lead decelerations to those documents.
**Severity**: Minor
**Confidence**: 4 — core expertise: standards for ADAS

---

## Detailed Comments *

### Title & Abstract
- The title names the tracker type ("Fixed-Noise Kalman Tracker") and the scenario ("Lead Braking"), which is the right scope. "Equal Caution" and "Decision-Level" are specialist terms; the abstract defines "wrong go" and "room" only implicitly.
- The abstract is 248 words and dense with numbers (about twenty). A transport practitioner has to read it three times. The conditional sentence about commitment is useful; the sentence "does not justify removing a covariance margin" is missing (W7). The 12% and 83% are stated without the 2 Hz, 5.5 m/s² and perfect-stop conditions (W1, W2, W3).

### Introduction
- The motivation (covariance as a margin, the class-average alternative) is clear and practical. The decision to size the room first and then test the covariance is persuasive.
- The Scope paragraph is a good model of plain limits, and it names the excluded road users. It would help to say there why those excluded users matter for the claim (see Stakeholder coverage).

### Literature Review / Theoretical Framework
- Primarily for Reviewer 2. From my seat, standards and test protocols for ACC, AEB and scenario-based assessment are the missing literature (W13). RSS is treated correctly as a different object from the nominal braking prediction (Section II), which a practitioner will appreciate.

### Methodology / Research Design
- The planner is a 17-row speed-profile selector with a chance-constraint form, not an ACC or AEB architecture. It is a reasonable vehicle for the question but not representative of deployed car following; the paper says "one in-house planner". The time-gap baseline partly bridges this (W9).
- The test bed: one straight flat road, one car model, a lead independent of the ego, a lead that always brakes at 2.1–5.5 m/s² (realised), default weather, simulated lidar with noise off, 2 Hz detector without latency, 0.5 s tracker step (W2, W3, W5). The lead being independent of the ego means open-loop scoring is exact for this scenario; it would not be for a reactive lead, a cut-in or a pedestrian, a point worth stating.
- The recording policy matters (W4). The evaluation runs were recorded by a planner that used the tracker's covariance in its own margin; this makes N approximately on-policy while other sources are off-policy. The paper states the off-policy character but not this asymmetry.
- The regulation use (W8): the parameter choice is transparent; the domain mismatch and document status are not.

### Results / Findings
- I checked the numbers I rely on against their tables. Section V-A, Table V and Table S26 agree (152,264 rows, 99.26%, median 1.103). Section V-C's split of the room (460.7 = 419.1 + 41.7 − 0.14) matches Table S33, and the 52.2 of 56.3 decision-equivalents in 132 decisions matches Table S33b (6.7 + 18.6 + 26.9; 53 + 43 + 36 decisions). Table III's ratios agree with Table S19; Section VI's 5.8%, 19.0%, 41.7% agree with Table S36; the held-out 0.90, 0.88 and 0.87 agree with Table S32. I found no mismatch among the anchored numbers.
- One item needs explaining: in Table S36 the before-onset row shows 5.0% for every source, including the oracle E and the perfect oracle O. An identical value across sources that otherwise differ suggests a floor from the fallback row or a population property; please explain (Question 4).
- Figures: Fig. 2(b) and Fig. 3 are clear. Fig. 4(b) plots RR₀(N) at a scale of 0.008, so the visual impression is of tight agreement; fine for the claim, but a note that the intervals are nominal and not valid for this statistic is already in the caption. Fig. S3(b) (closed loop) uses open markers well.

### Discussion

**Stakeholder coverage**

*Who the evaluation assumes benefits from a margin source.* The evaluation has one beneficiary: the ego vehicle's occupants (and operator), through fewer contacts with the lead, set against one cost, progress measured as speed given up (caution, in % of desired speed). The lead's occupants appear only as the object of contact, with a same-model car and no severity weighting ("wrong-go counts ignore impact speed"). No other party's benefit is scored: not traffic behind the ego, not the lead's occupants beyond contact, not other road users. All decisions have equal weight, so exposure-heavy stationary decisions (82.7% after the stop) carry most of the count.

*Who bears the cost of plans that are safe only because a stop follows.* Section VI and the conclusion name three cost bearers: occupants, traffic behind the ego, and progress. The paper does not measure any of them. What it does count is the reliance: at matched caution, 5.8% of all decisions with the class average (19.0% with the ego moving, 41.7% while the lead brakes) select a plan that is safe only because the stop follows, and the perfect oracle relies on the stop for 72.3% of its decisions (Table S36). The stop is 6 m/s² with a jerk of 12.65 m/s³, a hard stop well above typical ACC comfort envelopes. The people exposed are the occupants (a hard stop) and the drivers behind (a rear-end exposure that moves risk from the lead to the follower). The road has no vehicle behind the ego, so the displaced risk is not visible in the data. The conclusion states the cost ("at the price of plans that rely on that stop") but the abstract's 12% does not. I suggest adding the deceleration and jerk distribution of the selected plans' stops, and a rear-vehicle gap assumption, to make the cost side at least visible (W1).

*Which road users are outside the test.* Pedestrians, cyclists, crossing vehicles and cut-in vehicles are outside the evaluation, as is traffic behind the ego (Section I). The paper's own check shows why this is not a minor boundary: in pedestrian-crossing and vehicle-crossing runs only 8.51% and 4.09% of rows lie within 5% of one multiple, and the median ratio is 0.883 and 0.915, so these are the scenarios where the tracker's covariance varies and the null's mechanism does not apply. The families where the null is expected to carry over (stopped vehicle, cut-in, lead braking) are those with the lowest exposure of vulnerable road users. A reader who weights the claim by who gets hurt should read the null as covering the least vulnerable cases; the paper says the check is silent for the others, and the Section VI caution should be repeated in the abstract and conclusion (W7). The expectation for cut-in is supported only by a whole-run row share (W12).

*Practical reading offered to designers and assessors.*
- The conditional statement on commitments (Section VI) is useful and correctly conditional. Its weakness is the idealised stop (W1, W2).
- The "does not justify removing a covariance margin" caution is right and should travel with the headline (W7).
- The time-gap baseline is the one comparator familiar to ACC designers; it is helpful but post hoc and not combined with the covariance (W9).
- The supplementary closed-loop check runs no covariance margin; the paper says so. Its figures are in regulation units and risk being copied (W10).
- Could a safety engineer act on the conclusions without over-reading them? On the null for this tracker in steady lead following: yes, with the caution in the abstract. On the 12% and 83%: not yet; they hold for a 2 Hz detector, leads braking below 5.5 m/s², a perfect independent stop and one recording policy.

### Conclusion
- The conclusion is long and holds many qualifiers; the conditional statements are accurate. It over-infers nowhere in substance, but it omits the removal caution (W7) and offers the phase schedule at 99.9% without noting that it is open loop and untested on non-braking leads (W11).
- Future work is well chosen; I would add a closed-loop test with the covariance arms and a lead-following set without hard braking.

### References
- Mostly current and appropriate; two are code repositories and one is a thesis ([5], [6], [16]), acceptable. Standards and ADAS test protocols are absent (W13). [42] is cited as a proposal document; cite the adopted text (W8).

---

## Questions for Authors *

1. Can you report the stop-scoring room (Table III) split by the lead's realised deceleration, and with at least some leads braking at 6–8 m/s²? If the 12% rises when the lead decelerates harder than the ego's 6 m/s² stop, the abstract should say so.
2. Can the detector and tracker be re-run on the 20 Hz recordings at 5 and 10 Hz with a stated latency? How do R, the after-stop room and the braking prediction's share change?
3. What do the braking prediction and the tracker-phase schedule do in runs where the lead holds speed, brakes gently below 1 m/s², or stops and pulls away? Please report wrong-go and caution there.
4. In Table S36 the before-onset row is 5.0% for every source, including the oracles. What produces an identical value, and does it indicate a floor from the fallback row?

---

## Minor Issues

**Non-finding channel:** the entries below carry no Severity, Evidence Anchor or Confidence.

### Language / Grammar
- "Wrong go", "caution" and "room" are defined in the introduction, but the abstract uses them before definition; an ITS reader will expect "collision under the assumed manoeuvre" and "conservatism". The Notation table helps; consider moving a short gloss into the abstract.
- The Acknowledgment says Claude "carried out the literature searches and prepared the literature summaries ... from sources it retrieved"; Section II says abstracts only were read. Please state in Section II who "we" is in "(we did not read the full texts)", for consistency with the AI-use statement.

### Citation Format
- [5] and [6] cite code repositories by commit; [42] is a proposal document (W8). Reference [9] is under review at another IEEE journal and shares the tracker configuration and margin form; the paper says no data are shared, which is clear.

### Figures and Tables
- Several main-text results rest on supplement tables (S28, S35, S36, S37); Table S36 and Table S28 deserve a main-text place because they carry the practical reading (reliance on the stop, test-bed configuration).
- Fig. 4(b) and Fig. S4(b) show intervals "not valid" for RR(N); a one-line note in the figure itself would help the reader who sees the figure alone.

### Layout
- Submission gates, with no severity: the author block (manuscript line 5), the repository name and DOI in Data and Code Availability, and the "[AUTHOR CONFIRMATION: ...]" at the end of the AI-generated-content statement.
- The manuscript is about 12,450 words with 34,000 words of supplement; the recommendation is 10 pages. Sections IV and V are very dense. A shorter main text that moves the grading and interval detail to the supplement would serve the journal's readers.

---

## Criterion-Bound Judgements *

Calibration status: `NOT_CALIBRATED`

Current seat reports cannot know the final actual panel topology and never
self-upgrade from a candidate profile. Live package application remains
unavailable until a closed profile artifact and replay validator ship.

| Dimension | Criterion source | Judgement | Evidence anchor(s) | Rationale | Uncertainty / scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| Originality | criteria binding unavailable; general field norms | MEETS | `text: §II "Novelty, with its limits"`; `table: Table S30` | Placebo, graded oracles and a stated limit on the novelty search are a real design contribution for this question. | I did not search the literature myself. | No |
| Methodological Rigor | criteria binding unavailable; general field norms | PARTLY_MEETS | `text: §III-A "run at 2 Hz, with no latency simulated"`; `table: Table S35` | Careful internally; for practice, the test bed, recording policy and idealised stop limit what transfers. | Estimator and bootstrap detail left to other seats. | Yes (W1, W2, W3, W4, W5) |
| Evidence Sufficiency | criteria binding unavailable; general field norms | PARTLY_MEETS | `table: Table S28`; `table: Table S36`; `table: Table V` | The null for N is supported in this scenario; the practical claims (12%, 83%, carry-over) are not supported beyond it. | The per-run data were not available to me. | Yes |
| Argument Coherence | criteria binding unavailable; general field norms | MEETS | `text: §VI "Which commitment is representative"` | The conditional logic is consistent across Section VI and the conclusion. | The abstract's caution gap (W7) is a wording matter. | No |
| Writing Quality | criteria binding unavailable; general field norms | PARTLY_MEETS | `text: Abstract (about twenty numerals in 248 words)` | Plain limits; very dense, jargon-heavy for the journal's readers, long. | Readability judged for a practitioner reader. | No |
| Literature Integration | criteria binding unavailable; general field norms | PARTLY_MEETS | `absence: Section II — expected ACC and AEB standards and test protocols; checked Section II, references [1]-[58]` | Good on estimation and planning uncertainty; missing the standards a practitioner uses. | Coverage of estimation literature is for Reviewer 2. | No |
| Significance & Impact | criteria binding unavailable; general field norms | PARTLY_MEETS | `text: Abstract "A fixed 3 m/s² braking prediction recovers 83% of the room, open loop and off-policy."` | The evaluation design is useful to assessors; the numbers are not transferable without new runs or narrower wording. | Impact depends on the journal's tolerance for simulation-only evidence. | Yes |

The recommendation rests on the unresolved decision-bearing criteria Methodological Rigor, Evidence Sufficiency and Significance & Impact, taken from W1 to W5. W2, W3 and W5 need new runs; W1 and W4 need re-scoring or narrower wording. All are repairable. I do not let the strengths on Originality offset them.

---

## Cross-Disciplinary Reading Recommendations
- ISO 15622, adaptive cruise control systems: performance requirements and test procedures (time-gap and deceleration envelopes for ACC). Relevance: places the time-gap baseline and the stop deceleration against accepted ACC limits.
- ISO 22179, full speed range adaptive cruise control: relevance as above for low-speed following (the test bed's 5–15 m/s).
- IEEE 2846-2022, assumptions for models in safety-related automated vehicle behavior: relevance to the paper's use of RSS-style and regulation-derived assumptions as nominal reference parameters.
- ISO 21448, SOTIF: relevance to the perception-limitation framing and to the stop's dependence on perception (W1).
- UN Regulation No. 152 on advanced emergency braking systems for light vehicles [UNVERIFIED: citation details; treat as a search lead]: relevance to the 6 m/s² stop that "stands for a separate emergency-braking function".

~~~yaml suggested-references
- title: "Road vehicles — Intelligent transport systems — Adaptive cruise control systems — Performance requirements and test procedures"
  authors: ["ISO"]
  year: "2018"
  doi: null
  arxiv_id: null
- title: "Intelligent transport systems — Full speed range adaptive cruise control (FSRA) systems — Performance requirements and test procedures"
  authors: ["ISO"]
  year: "2009"
  doi: null
  arxiv_id: null
- title: "IEEE Standard for Assumptions in Safety-Related Models for Automated Driving Systems"
  authors: ["IEEE"]
  year: "2022"
  doi: null
  arxiv_id: null
- title: "Road vehicles — Safety of the intended functionality"
  authors: ["ISO"]
  year: "2022"
  doi: null
  arxiv_id: null
~~~
