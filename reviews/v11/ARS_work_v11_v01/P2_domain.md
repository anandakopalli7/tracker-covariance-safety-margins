contract_role: domain
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: warn
trigger: "imprecise or inconsistent terminology, a missing or outdated citation for a supporting statement, prior work summarised loosely but not wrongly, or a generalisation that reaches modestly beyond the evaluated conditions"
Basis: no domain error carries the central null; the steady-state mechanism is correct for straight-road lead braking and is confirmed by the paper's own tables. The deductions are an imprecise estimator description with a reach claim that goes beyond the evidence for other scenario families (W1), unexplained per-phase and after-stop mechanisms (W2), loose terminology and summaries of prior work (W5, W7), missing adjacent literature (W6) and stale supplement wording (W8).

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

### Reviewer Identity
Researcher in multi-object tracking and uncertainty-aware motion planning for automated vehicles (Kalman and IMM filtering, chance-constrained planning, CARLA-based perception-in-the-loop evaluation), serving as Peer Reviewer 2 (domain seat).

### Overall Recommendation
Major Revision (domain view only; the panel decision belongs to the synthesizer).

### Confidence Score
4

Confidence is an uncertainty/scope disclosure only; it never changes consensus counts, severity, decision bearing, or arbitration.

### Calibration Status
`NOT_CALIBRATED`

### Criterion-Bound Judgements
criteria_binding_unavailable

This is an unbound call; the rows below use the Reviewer Configuration Card and the dispatch brief as their source and make no venue-alignment claim.

| Dimension / criterion | Criterion source | Judgement | Evidence anchors | Rationale | Uncertainty or scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| Steady-state argument and the 1.10 ratio (update rate, step, state age) | Card focus 1 | PARTLY_MEETS | see S1, W1, W4 | Mechanism correct and confirmed for straight-road lead braking; tracker described as linear although run as an EKF with object-frame noise; the 1.10 is look-ahead dependent | Frame and construction of the class-average covariance are not stated | yes: main basis of the D2 warn |
| Margin projection, propagation without process noise, separate allowance Q | Card focus 2 | MEETS | see S2 | The projection is the exact variance of the constant-velocity position along the normal; Q is the random-constant-acceleration variance | none identified | no |
| Literature coverage and fairness to the closest works | Card focus 3 | PARTLY_MEETS | see S3, W6, W7 | [8], [13] and [17] checked against their records: fair, with [17] summarised loosely; stochastic-MPC car following and fading-factor filtering missing | Only three references checked beyond abstracts | yes, minor |
| NIS-inflated source and what it can test | Card focus 4 | PARTLY_MEETS | see W3 | Limits are conceded; position-block run means cannot test the velocity block that sets the margin, nor the onset | none identified | no |
| Test-bed realism | Card focus 5 | PARTLY_MEETS | see W10, W2 | Limits listed but their direction of effect on the room is not discussed | Effect sizes not estimable from the paper | yes, minor |
| Domain claims of Abstract and Sections I, II, VI, VII against the tables | Dispatch brief | PARTLY_MEETS | see W1, W9 | Every headline number checked matches Tables II-V and S5, S16, S19, S22, S23, S26; the reach sentence of contribution 4 and the per-phase sentence of the Abstract go beyond what the tables show | none identified | yes |
| Main text against supplement | Dispatch brief | PARTLY_MEETS | see W8 | Supplement S8 keeps withdrawn wording | none identified | no |
| Scope to a single-model fixed-noise Kalman filter in lead braking | Card, particular care | MEETS | see S6 | Scope paragraph and Section VI limits are explicit and accurate | none identified | no |
| Per-phase and after-stop findings physically explained | Card, particular care | DOES_NOT_MEET | see W2 | Statistical decomposition given, physical mechanism not | none identified | yes |

Do not total, weight, average, or mechanically map these judgements to the recommendation.

### Summary Assessment
The paper asks a well-posed domain question: does the state covariance of a fixed-noise Kalman tracker (CANMOT on CenterPoint detections in CARLA) improve a margin-type speed planner's decisions over a class-average covariance, at equal caution, with an oracle margin as positive control? From a tracking standpoint the answer is the expected one, and the authors say so: in steady following a fixed-noise filter's covariance converges, so it is a near-constant multiple of any class constant and a swept margin scale absorbs it. The paper confirms this empirically and convincingly (Fig. 2(b), Tables S14-S15: the tracker's deviation takes five discrete levels set by state age). The margin projection is exact for constant-velocity propagation, the chance-constraint mapping follows [1], the braking prediction is correctly distinguished from an RSS bound, and the prior work I checked is fairly represented. The domain weaknesses lie around this core. The tracker is described as a linear filter although the supplement runs it as an extended Kalman filter with object-frame noise, and this matters for reading the ratio check in other scenario families (contribution 4). The per-phase and after-stop findings, which set the headline 83% and 89% figures, are decomposed statistically but never explained physically, so they cannot be transferred to other trackers or sensors. Adjacent literature on stochastic-MPC car following and fading-factor filtering is missing, and some terminology is mapped loosely. All of this can be repaired with the stored arrays and rewording.

### Strengths
Six domain strengths, each with its anchor.

### S1: The steady-state null is anticipated correctly and confirmed directly
The paper states in advance that a fixed-noise filter should give a near-constant covariance and then shows it at the level a tracking specialist would want: at t = 0 the tracker's deviation along the lead normal takes the values 0.400, 0.419, 0.452, 0.495 and 0.545 m, one per state age of 0 to 0.4 s at the 2 Hz update rate, in every phase. That is the steady-state posterior propagated over the state's age, nothing more.
**Evidence Anchor**: table: Supplement Table S15, quintiles of the tracker deviation at t = 0 s by phase

### S2: The margin projection is technically exact
The variance s = zᵀPz with z = (n, t_e n) is exactly the variance of the constant-velocity predicted position along the normal, cross terms included, and keeping the acceleration allowance Q = t⁴σ_a²/4 separate (the variance of a random constant acceleration) is the right way to keep the source comparison clean. The feasibility test g s ≤ d² is the chance-constraint tightening of [1] with the per-constraint quantile absorbed into g, so sweeping g legitimately removes the risk level.
**Evidence Anchor**: equation: Section III-B, feasibility condition with the critical scale and the projection s = zᵀPz

### S3: Closest prior work is described fairly where I checked it
The description of Deglurkar et al. [13] matches its case study (the forecaster's uncertainty parameter is gridded, the planner rerun per value, outcomes split by prediction error); CANMOT's report of overconfidence on nuScenes [8] is correctly contrasted with the underconfidence found here.
**Evidence Anchor**: text: Section II "grid the value of a forecaster's uncertainty, run the planner at each value and split the outcomes by forecast error"

### S4: Braking prediction and regulatory parameters are positioned correctly
The constant-deceleration prediction is correctly distinguished from an RSS worst-case bound, and the R157 values are used as nominal parameters with no compliance claim, which avoids a common category error in this literature.
**Evidence Anchor**: text: Section II "Our braking prediction is not such a bound: it is a nominal constant-deceleration prediction of the lead"

### S5: The reliability check is interpreted correctly
The class-average deviation ranks the realised error as well as the tracker's does, and the paper draws the right conclusion: the ranking comes from state age and constraint direction, plus a systematic lag behind the braking lead, not from per-decision calibration.
**Evidence Anchor**: text: Section V-E "so the ranking comes from those two, not from the tracker's covariance"

### S6: Scope is stated precisely
The claims are confined to the raw covariance of a single-model fixed-noise filter in lead braking; calibrated, IMM and two-way adaptive covariances, track births and other road users are explicitly excluded, and Section VI says the result does not justify removing a covariance margin from a deployed stack.
**Evidence Anchor**: text: Section I Scope "We do not test a calibrated covariance, a manoeuvre-adaptive (IMM) tracker, or a covariance that adapts in both directions."

### Weaknesses
Ten weaknesses, each banded by its own decision impact.

### W1: The steady-state argument is stated for a linear filter, but the tracker is an EKF with object-frame noise, and the reach claim does not separate geometry from information
Sections II and VI explain the near-constant covariance by the steady state of a linear, time-invariant Kalman filter, and Section I, Fig. 1 and Section III-A call CANMOT a constant-velocity Kalman filter. Table S28 describes the filter as run as an extended Kalman filter with a constant-velocity model in the object frame, and CANMOT's published abstract describes class-specific noise that can be expressed in each object's own frame. For such a filter the covariance passed to the planner in the planner frame depends on the estimated heading, through the rotation of process and measurement noise and through the linearisation. The Riccati steady-state result therefore holds only while heading and constraint geometry stay fixed and updates arrive regularly. That is true on this straight road, which is why the lead-braking result stands, but the paper never states the condition. It matters for Section V-E and contribution 4. In the crossing and benign families, the ratio to the class-average covariance can vary simply because a fixed object-frame steady-state covariance is rotated against a fixed class average, with no per-decision information in the variation. The paper does not say whether the class average is in the planner or the object frame, or whether it is the mean of logged covariances or the second moment of realised errors. Hence "not expected to carry over" (Section V-E; contribution 4 says the same) reads more into the variation than the check supports; Section VI's statement that the check is silent there is the accurate one. Minimum remedy: describe the filter as it is run (EKF; frames of state, noise and P̄; how P̄ was formed), state when the steady-state argument holds (fixed heading, regular updates, no misses), and reword Section V-E and contribution 4 to "silent". Stronger option, on stored arrays only: repeat Table V against a heading-aligned class average, the object-frame P̄ rotated by each track's heading, to see how much of the crossing-family variation is geometric.
**Severity**: Major
**Evidence Anchor**: text: Section II "With fixed noise, a linear Kalman filter's covariance and gain do not depend on the measured values and settle to a steady state"; Supplement Table S28 "extended Kalman filter with a constant-velocity model in the object frame"; Section V-E "so the null of this paper is not expected to carry over to them"
**Confidence**: 3 (tracking and EKF expertise; the frame and construction of P̄ are not visible in the paper)

### W2: The per-phase and after-stop findings are decomposed statistically but not explained physically
Of the evaluated decisions, 82.7% follow the lead's stop and 77.5% have the ego at or below 0.5 m/s. The braking prediction's share rises from 0.29 to 0.83 as up to about 20 s of after-stop decisions are added (Table S22). After the stop it recovers 0.99 of that phase's room (Table S5), and the supplement says only that "any braking assumption helps" there. A wrong go behind a lead that has been at rest for 10-20 s requires the planner to predict free road ahead of a stationary car: a forward velocity estimate or a position bias of the stopped lead, or an accelerating row that the 3 s blind commitment cannot undo. The paper reports none of these: not the tracker's estimated lead speed and acceleration against time since the stop, not the rows selected in after-stop wrong-go decisions. The lead-braking room (15.59 points) is explained only in Supplement S9, as a systematic lag (mean error −3.2 m at 1 s). One plausible mechanism links both phases but is untested. The class-level measurement noise, tuned for nuScenes, is much larger than this simulated sensor's error (lead-track NIS 0.24 against 2). That gives a small gain and a lagging velocity estimate, at the onset and after the stop. Without a mechanism, three results cannot be transferred to other trackers, detectors or sensors: the 83%, the 89% recovered by one scale per phase, and the conclusion of Sections VI and VII that information about the lead's motion state recovers the room. They may partly reflect a tracker artefact on stationary targets. Minimum remedy, on stored arrays: report the estimated lead speed and acceleration around the onset and against time since the stop; tabulate the rows selected in after-stop wrong-go decisions; state the mechanism in Section V-C. Also note in the scope that most decisions are a standstill queue rather than following in motion.
**Severity**: Major
**Evidence Anchor**: text: Section V-C "The 83% is therefore a figure for recordings that continue for about 20 s after the stop."
**Confidence**: 3 (planning and tracking expertise; mechanism inferred, not observed)

### W3: The NIS-inflated source can test little in this test bed, and its trigger checks the wrong block
With a median run-mean NIS of 0.24 and an inflate-only factor max(1, NIS/2), the source acts only when the last three position NIS average above 2. It changed critical values in 217 of 8,290 decisions, 27 of them in the five short contact runs. The authors concede this. Two further domain points are not made. (a) The NIS is that of the position block, but at a 3 s look-ahead the margin is dominated by the velocity block (Supplement S1, weight t_e² = 9). A position-innovation consistency check says little about the velocity variance that sets the margin, yet λ scales both. (b) The run-level mean in Fig. S1 averages over long after-stop segments, so it cannot show whether innovations grow at the braking onset, the one place where an adaptive covariance could matter. Remedy: report NIS by phase (an onset window in particular) and the velocity-error consistency against CARLA truth (velocity NEES or z-scores), and state that the NA result does not bear on velocity-block adaptation.
**Severity**: Minor
**Evidence Anchor**: text: Section III-A "the median over runs of the mean NIS of the lead track's position block is 0.24, against an expected 2"
**Confidence**: 4 (filter consistency testing)

### W4: The 1.10 is a look-ahead-dependent ratio, not a scalar multiple of the covariance
The tracker's deviation over the class average's is 1.02-1.05 at t = 0 and about 1.10 at 2-3 s (Table S14), so the tracker's covariance is not a scalar multiple of P̄. The position block sits about 3.5% above it in deviation, the velocity block about 10%. The ratio of 1.10 at binding constraints therefore reflects that constraints bind at long look-ahead, where the velocity block dominates. A swept g removes a global scale, not this shape difference. Its effect here is evidently small, but Section VI should say that the 1.10 is a velocity-block property and that state age (0-0.4 s at about 2 Hz) and look-ahead move the ratio, rather than present it as one constant.
**Severity**: Minor
**Evidence Anchor**: table: Supplement Table S14, column of the deviation ratio at t = 0 s against t = 2 s and t = 3 s
**Confidence**: 4 (direct reading of the table)

### W5: The margin scale is mapped to the wrong established term
The notation table equates the margin scale g with the "safety distance of a spacing policy [52]", and Section II says the planner's margin plays the role of a spacing policy. In adaptive cruise control a spacing policy prescribes a desired gap as a function of speed, as in the time-gap policy of [52], which Section VI itself correctly names as a source not tested. The margin √g·σ is a chance-constraint tightening, and g corresponds to the squared standard-normal quantile of a per-constraint risk level, as in [1]. Remedy: map g to the confidence or risk level of the chance constraint, and keep "spacing policy" for the time-gap baseline.
**Severity**: Minor
**Evidence Anchor**: text: Section II "the planner's margin plays the role of a spacing policy in adaptive cruise control [52]"
**Confidence**: 4 (chance-constrained planning and ACC literature)

### W6: Adjacent literature on stochastic car following and fading-factor filtering is missing
Section II covers chance constraints, learned planners and threat assessment. It omits the stochastic-MPC line of work that sizes car-following or traffic margins from uncertainty about the other vehicle, the closest application to a margin set from lead uncertainty: Moser et al. (2018) on flexible-spacing ACC by stochastic MPC; Brüdigam et al. (2023) on stochastic MPC with a safety guarantee for automated driving. It also omits innovation-driven fading-factor filtering (Xia et al. 1994), the direct prior art for scaling a covariance by an innovation statistic as the NA source does. Supplement S6 discloses that the IMM and adaptive-filtering literature was not searched for a planner-side test and that [41]-[52] were summarised from abstracts only. Remedy: add these works with one sentence each on how they differ (they design margins; this paper evaluates the source).
**Severity**: Minor
**Evidence Anchor**: absence: Section II Related Work — expected stochastic-MPC car following with an uncertain lead vehicle and fading-factor adaptive Kalman filtering; checked Section II, the reference list [1]-[55], Supplement S6
**Confidence**: 4 (references verified against Crossref records in this session)

### W7: The closest planner-in-the-loop study is summarised loosely
Section II says [17] finds that propagating class uncertainty helps a learned predictor. In [17], the closed-loop nuPlan comparison cannot use class uncertainty, which is not available there; its closed-loop gain is attributed to better-calibrated distributions, and class propagation helps prediction metrics on another dataset. The second half of the sentence is accurate and deserves more weight: the constant-velocity baseline with a fixed covariance in [17] has badly calibrated likelihoods yet a closed-loop score between those of the two learned pipelines. That is the nearest published analogue of this paper's null. Remedy: restate [17] as above.
**Severity**: Minor
**Evidence Anchor**: text: Section II "The closest planner-in-the-loop study [17] finds that propagating class uncertainty helps a learned predictor"
**Confidence**: 3 (based on a look-up of the arXiv full text of [17], not a full reading)

### W8: The supplement keeps wording that the main text has withdrawn
Supplement S8.2 still says that, under the 0.75 s stop, the pooled braking-prediction share comes from "a mechanism that no analysis here isolates". It also says "the location of the room under the 3 s commitment (Section VI) does not hold". Section V-C and Supplement S10.4 now isolate that mechanism (one scale per phase recovers 89%), and Table S4 records that the Section VI location statement was replaced. Supplement S8.1 likewise describes abstract sentences that the current Abstract no longer contains (Table S4, last rows). Remedy: update S8.1-S8.2 or mark them as the earlier draft's record.
**Severity**: Minor
**Evidence Anchor**: text: Supplement S8.2 "a mechanism that no analysis here isolates"
**Confidence**: 5 (direct comparison of the two texts)

### W9: The Abstract's per-phase sentence omits that the phase labels come from the logged truth
Section V-C is explicit that a scale per phase uses truth-derived phase labels, is itself information, and was not tested as a realisable rule. The Abstract states the 89% without this qualifier, so a reader can take a phase-scheduled class-average margin as an information-free baseline. Remedy: add "with the phase taken from the logged truth" or equivalent.
**Severity**: Minor
**Evidence Anchor**: text: Abstract "A class-average margin with one scale per phase of the lead's motion recovers 89% of the room"
**Confidence**: 4 (direct comparison with Section V-C)

### W10: The direction in which test-bed simplifications move the room is not discussed
The perception chain is idealised in ways that bear on the size and location of the room rather than on the covariance null:
- the detector runs at 2 Hz with no latency, under a planner deciding at 10 Hz;
- simulator lidar noise is off, apart from 0.02 m of range noise;
- a nuScenes checkpoint is applied to CARLA sweeps without adaptation;
- one car model, a straight flat road and default weather;
- the tracker configuration is shared with [9].
The Limits paragraph lists several of these but does not say which way each pushes the lead-braking room or the braking prediction's share. For example, a faster detector shortens the state age that drives the error ranking (Section V-E), while latency or a better-tuned measurement noise changes the lag behind a braking lead (see W2). Remedy: one paragraph in Section VI on the expected direction of each simplification. The covariance null itself is robust to them, so no new runs are needed for the core claim.
**Severity**: Minor
**Evidence Anchor**: text: Supplement Table S28 "run every tenth frame (2 Hz); no latency simulated"
**Confidence**: 4 (CARLA perception-in-the-loop experience)

### Detailed Comments

#### Literature Review
- **Coverage**: Good coverage of decision-aware perception metrics, open- versus closed-loop evaluation, IMM and adaptive filtering, and threat assessment. Missing: stochastic-MPC car following and fading-factor filtering (W6).
- **Integration quality**: Synthetic rather than a list; each strand is tied to what this paper does and does not test.
- **Research gap argument**: Persuasive and appropriately hedged; the paper concedes that the mechanism (Riccati steady state) is textbook and claims the evaluation and its measured consequence.

#### Theoretical Framework
- **Appropriateness**: Chance-constrained margins with a swept scale, steady-state Kalman filtering and value of information are the right frameworks for the question.
- **Application depth**: Deep for the covariance null. Shallower for the room: the per-phase and after-stop results are decomposed but not tied to filter dynamics (W2).
- **Alternative frameworks**: Filter consistency (NEES of the velocity estimate against CARLA truth) would test directly what the NIS check only approximates (W3).

#### Academic Argument Quality
- **Factual accuracy**: Numbers in the Abstract and Sections I, II, VI and VII match the tables I checked (Tables II-V; S5, S16, S19, S22, S23, S26). The estimator is mis-described (W1).
- **Argument logic**: The null follows. The reach claim for other scenario families infers too much from ratio variation (W1).
- **Terminology precision**: Spacing-policy mapping (W5); "near-constant multiple" without its look-ahead dependence (W4).

#### Contribution to the Field
- **Incremental contribution**: A decision-level, equal-caution test with a positive control, showing that a fixed-noise tracker's covariance adds nothing over a class constant in lead braking, and that open-loop decision scores depend strongly on the commitment and the population mix.
- **Positioning**: Clear, and the paper is honest that the null is expected.
- **Overclaiming**: Limited to the reach sentence for other families (W1) and the per-phase sentence of the Abstract (W9).

#### Missing Key References
- Moser, Schmied, Waschl and del Re (2018), stochastic-MPC adaptive cruise control with flexible spacing: the closest application of uncertainty-sized margins to car following.
- Brüdigam, Olbrich, Wollherr and Leibold (2023), stochastic MPC with a safety guarantee for automated driving: margins from uncertain other-vehicle predictions.
- Xia, Rao, Ying and Shen (1994), adaptive fading Kalman filter: prior art for innovation-driven covariance scaling.

~~~yaml suggested-references
- title: "Flexible Spacing Adaptive Cruise Control Using Stochastic Model Predictive Control"
  authors: ["Moser, D.", "Schmied, R.", "Waschl, H.", "del Re, L."]
  year: "2018"
  doi: "10.1109/TCST.2017.2658193"
  arxiv_id: null
- title: "Stochastic Model Predictive Control With a Safety Guarantee for Automated Driving"
  authors: ["Brüdigam, T.", "Olbrich, M.", "Wollherr, D.", "Leibold, M."]
  year: "2023"
  doi: "10.1109/TIV.2021.3074645"
  arxiv_id: null
- title: "Adaptive fading Kalman filter with an application"
  authors: ["Xia, Q.", "Rao, M.", "Ying, Y.", "Shen, X."]
  year: "1994"
  doi: "10.1016/0005-1098(94)90112-0"
  arxiv_id: null
~~~

### Questions for Authors
1. Is CANMOT run as an extended Kalman filter with object-frame noise? In which frame is the class-average covariance expressed, and is it the mean of logged tracker covariances or the second moment of realised errors?
2. After the lead stops, what are the tracker's estimated lead speed and acceleration as a function of time since the stop, and which rows are selected in the after-stop wrong-go decisions?
3. Does the tracker's measurement include CenterPoint's velocity output? What are the NIS by phase (especially in a window around the braking onset) and the consistency of the velocity estimate against CARLA truth?
4. Against a heading-aligned class average, how much of the ratio variation in the crossing and benign families remains?
5. Would a detector at 10 Hz, or with simulated latency, be expected to shrink or enlarge the lead-braking room?

### Minor Issues
- Relating the room to the value of perfect information [55] is an analogy (Howard's quantity is an expected-utility difference); "analogous to" would be more precise.
- The ratio check of Table V includes the tuning runs on which the class average was computed; the tuning-only column of Table S26 shows the same pattern, which could be said in the main text.
- Section II's statement that no threat-assessment work compares a tracker covariance with a constant rests on abstract-level reading of [41]-[52] (Supplement S6); a hedge naming that limit would help.
- The regulatory reading of the R157 01-series performance model is outside my competence and was not assessed.
- No text addressed to reviewers was found in the manuscript or the supplement.
