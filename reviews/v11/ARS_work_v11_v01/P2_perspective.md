# Perspective Review Report (Peer Reviewer 3), Phase 2

contract_role: perspective
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: warn
trigger: "Adjacent-field connections are asserted with only partial support"

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

### Reviewer Identity

Safety-assurance engineer for automated driving (scenario-based verification and validation, UN R157 ALKS type approval, RSS, ISO 21448) with a background in decision analysis and value of information. I am an outsider to tracker internals and to fine statistical detail; where a point below touches either, I say so and leave the weight to the methodology seat.

### Overall Recommendation

Minor Revision (seat-level advice only; the panel decision belongs to the synthesizer).

### Confidence Score

4

Confidence is an uncertainty/scope disclosure only; it never changes consensus counts, severity, decision bearing, or arbitration.

### Calibration Status

`NOT_CALIBRATED`

### Criterion-Bound Judgements

This is an unbound call (`criteria_binding_unavailable`); the rows below use the contract's D4 and the five focus items of my Reviewer Configuration Card, and make no venue-alignment claim.

| Dimension / criterion | Criterion source | Judgement | Evidence anchors | Rationale | Uncertainty or scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| D4 cross_disciplinary_relevance | Contract D4; my Phase 1 scoring plan | PARTLY_MEETS | S1 to S9; W1 to W12 | Framing and definitions are accessible and most bridges are fenced; two notation-table mappings and two regulatory phrasings are looser than the adjacent fields' meanings, and one practical inference leaves out a stakeholder | Outsider to tracking internals and fine statistics | yes: sets D4 to warn |
| Focus 1: R157 performance-model-2 values and no-compliance fences | Reviewer Configuration Card | MEETS | S1; W6, W7, W8 | Fences recur in Sections II, IV-C, Limits and S3; remaining issues are wording and which stop deceleration carries the headline | I did not re-read the 01-series Annex 3 text for this review | no: textual repairs |
| Focus 2: value-of-information reading of the room and the per-phase baseline | Reviewer Configuration Card | PARTLY_MEETS | S2, S8; W2, W3 | The per-phase decomposition is the right control; the EVPI label and the in-sample selection of scale triples overstate what the numbers are | Size of the in-sample optimism unknown | yes: contributes to warn |
| Focus 3: practical reading under the two commitments; reach of the closed-loop check | Reviewer Configuration Card | PARTLY_MEETS | S4; W1, W4, W8 | Conditional reading and closed-loop fence are sound; the stop branch omits safety costs and uses a stop harder than the planner's own fallback | None beyond the paper's own open-loop limits | yes: contributes to warn |
| Focus 4: stakeholder coverage | Reviewer Configuration Card | PARTLY_MEETS | S6; W1, W9, W10 | Exclusions are stated candidly; following traffic, severity and base-planner representativeness are not carried into the practical reading | Simulation-only evaluation | yes: contributes to warn |
| Focus 5: reproducibility and disclosure | Reviewer Configuration Card | PARTLY_MEETS | S7; W11, W12 | Configuration table and AI-use statement are strong; the described deposit omits the arrays behind contribution 4, and "independent" verification lacks provenance; author block and repository/DOI placeholders treated as submission gates | D1 (methodology seat) owns reproducibility | no: repairs are deposit contents and wording |

### Summary Assessment

The manuscript asks whether a fixed-noise Kalman tracker's covariance, used as a planner's safety margin, improves car-following decisions over a class-average margin, and answers with a decision-level evaluation at equal caution with an oracle positive control. Read from safety assurance and decision analysis, it is unusually careful about the fences my communities care about: the UN R157 performance-model-2 values are borrowed as nominal parameters with no compliance claim, the closed-loop check is explicitly not a test of the question, the sentence against removing a covariance margin from a deployed stack is supported by a ground-truth-free ratio check, and the AI-use statement is specific. The per-phase-scale analysis is the strongest decision-analytic result: most of the oracle's pooled room is an allocation of caution between phases, not per-decision information. My concerns are with the bridges, not the core null. The stop-reliant branch of the practical reading treats the remaining consequences of source choice as comfort and progress and leaves out traffic behind the ego and fallback reliability; the notation table maps the room to the value of perfect information and the margin scale to a spacing policy's safety distance, both looser than those fields' meanings; the 89% is an in-sample, truth-labelled value of phase information; the 12% headline uses a stop harder than the planner's own fallback; wrong-go counts ignore severity; and the deposit as described does not hold the arrays behind the cross-family ratio check. Each is repairable with text and modest offline analyses of stored arrays.

### S1: Regulatory parameters borrowed with a clear no-compliance fence

**Evidence Anchor**: text: Section IV-C "We borrow them as nominal reference parameters from a motorway lane-keeping regulation and claim no compliance"

The three performance-model-2 values (0.75 s, 6 m/s², 12.65 m/s³) carry a no-compliance fence that recurs in Section II, Section IV-C, the Limits ("read in the text adopted in June 2022") and Supplement S3. S8.1 traces them to the original R157 driver model (0.4 s, 0.75 s, 0.6 s to 0.774 g), and the 2 m standstill gap is reported as a sensitivity rather than silently dropped. I checked the minimum following distances used in S3 (10.30, 13.60 and 17.18 m at 8, 10 and 12 m/s) against R157's time-gap table; they agree. This is how an assurance reader wants regulatory numbers handled.

### S2: The per-phase-scale baseline separates regime information from per-decision information

**Evidence Anchor**: text: Section V-C "it is recovered by knowing the phase, not the error of each decision"

Giving the class average one scale per phase (Table S23, Fig. 3(b)) is the decision-analytically correct control: it separates the value of knowing the regime from the value of knowing each decision's error, and it shrinks the braking prediction's gain from 383 to 50 decisions. The abstract, contributions and conclusion carry this qualification instead of leaving the 83% unqualified.

### S3: The deployment-facing sentence on covariance margins is supported and fenced

**Evidence Anchor**: text: Section VI "It does not justify removing a covariance margin from a deployed stack"

The sentence a practitioner is most likely to quote is tied to two concrete reasons (almost no newly started tracks; crossing families where the covariance is not a constant multiple, Table V), and it stops short of the over-reading that a null invites.

### S4: The closed-loop check is described for what it is

**Evidence Anchor**: text: Supplement S3 "it runs no covariance margin and does not test the question" and "Its gap figures are not design guidance."

The check is presented as information-free sizing on a simplified simulator that understates the tracker's stopping-point error by about 40%, and its 0.70 to 0.72 fallback share at the critical commitment time is reported as a cost rather than hidden. Fig. S3 matches the text (scan brackets, Td's 10 runs below 2 m, F0's closest gap of 1.864 m at 0.60 s).

### S5: Defined terms and an established-term column bridge to adjacent fields

**Evidence Anchor**: text: Section I "Four terms carry the paper." and Section IV notation "with the established term each corresponds to"

Four defined terms in Section I and a notation table that names each quantity's counterpart in the wider literature are exactly what an adjacent-field reader needs. W2 and W5 concern two rows of that table, not the device itself.

### S6: Excluded road users and unmeasured costs are named

**Evidence Anchor**: text: Section I Scope "Pedestrians, cyclists, crossing and cut-in vehicles, traffic behind the ego and real sensor data are outside the evaluation."

Section VI adds that the braking prediction's costs to occupants' comfort and to following traffic were not measured, and reports the benign-run check (no vehicle in the ego's lane; 0 and 3 changed selections) instead of claiming the prediction is harmless.

### S7: Specific AI-use disclosure and a detailed configuration table

**Evidence Anchor**: text: Acknowledgment "drafted the text of the Abstract, Sections I–VII and the Supplementary Material"

The statement names the system, period, tasks (searches, summaries, code, derivations, drafting) and the sections affected; Table S28 gives the recording configuration down to noise terms and hashes. This meets the substance of IEEE's disclosure expectations as I understand them.

### S8: The positive control is validated as a measuring instrument

**Evidence Anchor**: text: Section IV-B "Pooled, the null of Section V-A is therefore not a blunt measure."

The graded partial oracles play the role of a gauge study in quality engineering: the score is shown to respond to graded information before a null is read from it, and the paper discloses where it does not grade (within the lead-braking phase and with the ego moving).

### S9: A ground-truth-free screening test practitioners can run on their own logs

**Evidence Anchor**: text: Section VI "Two checks need no new data."

The binding-row ratio check lets an engineer decide, before any decision-level test, whether a covariance margin can change which plan is chosen at all. Section VI states its reach and that no threshold separates the families.

### W1: The stop-reliant practical reading omits following traffic and fallback reliability

**Severity**: Minor
**Evidence Anchor**: text: Section VI "the choice of source matters mainly for comfort and progress, which we did not score"
**Confidence**: 4 — practitioner basis in fallback and minimal-risk-manoeuvre safety arguments

In the reaction-and-stop branch of the conditional reading, the consequences of choosing a margin source are reduced to comfort and progress. A safety argument would not accept that ledger: a policy that leans on an unconditional 6 m/s² stop exports rear-end exposure to traffic behind the ego, which the Scope places outside the evaluation, and its residual risk depends on the fallback's own reliability, which the scoring assumes perfect. The sentence therefore gives zero safety weight to a road user the evaluation excluded. The measured result (about 12% of the room remains) is unaffected; the practical inference drawn from it is what needs repair. Minimum remedy: name following-traffic exposure and fallback reliability as unscored safety costs in this sentence and in the conclusion's stop branch. Stronger and cheap with the stored flags: report, per source at matched caution, the share of decisions whose selected row is unsafe under the 3 s commitment but safe under the reaction-and-stop scoring, i.e. how often the evaluated policy relies on the stop. This is the finding I consider most important for the practical message.

### W2: The room is mapped to the value of perfect information although E is not a bound

**Severity**: Minor
**Evidence Anchor**: text: Section IV notation table "Value of perfect information [55]" and Section IV-B "A source can exceed RR = 1 because E is a reference, not a bound"
**Confidence**: 4 — decision-analysis background

In decision analysis the expected value of perfect information is the value of the best decision made with perfect information, and it bounds the value of any information source. R is instead the advantage of plugging a perfect-information variance into a fixed single-scale rule, averaged over 201 caution levels, and the paper itself reports shares above 1 (braking prediction after the stop, 0.993 [0.914, 1.11]; Table S25, 1.01 to 1.03). The paper's own perfect oracle O is the closer analogue: under the 3 s commitment E reaches 0.927 of den₀ (Table S9). A decision-analysis reader using the established-term column would read R as a ceiling. Remedy: relabel R as the value of a perfect-information margin within the fixed rule (not a bound), and map den₀ against O to the value of perfect information for each scoring.

### W3: The 89% is an in-sample, truth-labelled value of phase information

**Severity**: Minor
**Evidence Anchor**: text: Section V-C "took its frontier over all triples of scales"
**Confidence**: 3 — decision-analytic basis; the methodology seat may weigh the statistics

At each caution level the per-phase frontier is the lower envelope over all 202³ scale triples, chosen on the 35 evaluation runs with phase labels from the logged truth. The run bootstrap repeats this selection in each resample, so its interval reflects sampling spread, not the optimism of choosing three free scales after seeing the outcomes, whereas the single-scale frontier has one free parameter. The oracle's own per-phase gain (0.35 [0.09, 0.72] points, Table S23) is a partial control, but the oracle is already near zero wrong-go over most levels, so it bounds the flexibility effect only loosely. Because "89%" appears in the abstract and the contributions, state that it is an in-sample value; better, choose the triples on the 20 tuning runs, as was done for the 3 m/s² deceleration, or by leaving runs out, and report the out-of-sample gain. The correction can only lower the figure; I do not presume it overturns "most".

### W4: The allocation finding is not connected to a rule a planner could run

**Severity**: Minor
**Evidence Anchor**: text: Section VI "a time-gap margin, the usual spacing policy [52], was not among them"
**Confidence**: 3 — practitioner basis in ACC and ALKS spacing design

The practical takeaway is that most of the pooled room is an allocation of caution between phases. An engineer's next question is whether a deployable schedule captures it: a class-average scale scheduled on a phase estimated from the tracker's own state (speed and acceleration estimate), or the constant-time-gap spacing that production ACC and R157's minimum following distance already use. The paper says neither was tested. Both are offline re-scorings of stored arrays; without one, the allocation result is diagnostic rather than actionable. Remedy: add one realizable phase-scheduled or time-gap source to Table S23(b), or say in Section VI that the result does not yet show whether a deployable schedule captures the allocation.

### W5: The margin scale is mapped to a spacing policy's safety distance

**Severity**: Minor
**Evidence Anchor**: text: Section IV notation table "Safety distance of a spacing policy [52]"
**Confidence**: 4 — ACC spacing-policy and chance-constraint background

g multiplies a variance; its square root is the number of standard deviations in the chance constraint [1]. A spacing policy's safety distance [52] is a distance, usually a standstill gap plus a time gap times speed, and Section VI itself treats a time-gap margin as a different, untested source. An ACC reader following the table would take the sweep to be over a spacing distance. Remedy: map g to the squared safety factor of the chance constraint, a tuning parameter comparable in role to a spacing policy's time gap.

### W6: Section V-D gives the performance model's 2 m a normative register the paper does not need

**Severity**: Minor
**Evidence Anchor**: text: Section V-D "Performance model 2 asks for 2 m at standstill, not for the absence of contact."
**Confidence**: 3 — type-approval background; I did not re-read the 01-series Annex 3 text for this review

Performance model 2 is a reference model whose parameters include a 2 m distance at complete stop; Supplement S3 calls it "the safety distance at complete stop" and S10.5 says the model "specifies a 2 m gap at standstill". Saying it "asks for" 2 m and "not for the absence of contact" reads, to a type-approval audience, as a statement about the regulation's acceptance criterion, which the paper neither needs nor supports. Remedy: use the S10.5 register (a 2 m model parameter at standstill; the main scoring counts contact).

### W7: "Legal following distance" for R157's minimum following distance

**Severity**: Minor
**Evidence Anchor**: text: Supplement S3 "at about 0.31–0.35 s of extra starting gap over the legal following distance"
**Confidence**: 4 — UN R157 type-approval background

S3 and S3.4 also speak of the "legal minimum". The values themselves are right (see S1), but R157's time-gap table is an ALKS type-approval requirement, not a legal following distance for traffic in general, and as I read R157's scope ALKS is limited to roads without pedestrians and cyclists and with physically separated directions, which the paper's CARLA road (one lane per direction, Table S28) is not. In a paper that otherwise fences compliance carefully, "legal" is the word an assurance reader would lift into a safety case. Remedy: write "the R157 minimum following distance [38, §5.2.3.3]" and note in one clause that the test beds lie outside the ALKS domain.

### W8: The 12% headline uses a stop harder than this planner's own fallback

**Severity**: Minor
**Evidence Anchor**: text: Abstract "With a perfect 6 m/s² stop 0.75 s after each decision, 12% of the room remains." and Table S28 "fallback: the (−5, −5) row"
**Confidence**: 4 — reading of Section IV-C, Section V-D and Table S28

The scored stop is 6 m/s² at 12.65 m/s³, taken from performance model 2; the test-bed planner's own full braking is the (−5, −5) row with jerk at most 8 m/s³. Section VI reads the reaction-and-stop scoring as closer to a planner with a reliable fallback, but for this planner the matched figure is the 5 m/s² value of Section V-D (0.18, still at the faster jerk), not 0.12. The deceleration sweep is reported, so nothing is hidden; the issue is which number carries the abstract and the practical reading. Remedy: state beside the 12% that 6 m/s² exceeds the planner's own fallback and give the planner-matched value; if the stronger stop is meant to stand for a separate emergency-braking function, say so.

### W9: Wrong-go counts ignore severity

**Severity**: Minor
**Evidence Anchor**: text: Section IV notation table "A collision under the assumed manoeuvre; a criticality outcome [50]" and Section III-A "77.5% have the ego at or below 0.5 m/s"
**Confidence**: 3 — safety-assurance basis; the closing-speed distribution is not reported, so its effect is unknown

A wrong go is counted as a binary event. Most evaluated decisions have the ego nearly stopped and come after the lead has stopped, where a wrong go may be a low-speed creep into a stopped lead (the closed-loop contacts of S3 were at 0.09 to 2.31 m/s), while wrong goes during the lead's braking can carry substantial closing speed. Safety assurance weights hazards by severity, and the after-stop segment is where the 83% comes from (Section V-C). The ego-moving population is a coarse proxy, but the paper does not say that the score is severity-blind. Remedy: one sentence saying so; better, report the closing speed at first loss of clearance for wrong-go decisions, by phase, for F0, E and the braking prediction, from the stored clearances.

### W10: The recording planner's contact rate bounds what the absolute numbers mean

**Severity**: Minor
**Evidence Anchor**: text: Table S28 "Five of the 35 evaluation runs and 10 of the 20 tuning runs ended at the first physical contact"
**Confidence**: 3 — practitioner judgement of transferability

Under the recording planner, contact with the lead ended a seventh of the evaluation runs and half of the tuning runs. With 2 Hz perception, states up to 0.4 s old and no separate emergency-braking layer described, the test bed is a research planner well below a deployable safety level. This does not undermine the equal-caution comparison between sources, but it limits what the absolute quantities (9.00% wrong-go at zero margin, the size of the room) say about a deployed stack. The Limits mention one in-house planner without drawing this consequence. Remedy: one sentence in the Limits that only the relative comparisons between sources are meant to transfer.

### W11: The deposit as described does not cover contribution 4 or the recording pipeline

**Severity**: Minor
**Evidence Anchor**: text: Data and Code Availability "the per-decision arrays of the 55 lead-braking runs" and Table S26 "Stored arrays of all runs of the project"
**Confidence**: 4 — direct reading of the availability statement and Supplement S10

Table V and Table S26 (contribution 4) and the benign-run check of S10.6 use arrays from all six scenario families (223 runs), but the deposit lists only the lead-braking arrays; the capture and scenario code and the simplified simulator of S3 are not listed, and the raw recordings are on request. A reader can re-run the lead-braking analysis but not the cross-family ratio check, which is the paper's most transferable tool. Remedy: deposit the binding-row arrays of all families, the capture scripts and the S3 simulator, or state the restriction. The author block and repository/DOI placeholders are submission gates and are not counted here.

### W12: "Independent" verification needs its provenance stated

**Severity**: Minor
**Evidence Anchor**: text: Section IV-D "independent second programs re-implement the scoring" and Acknowledgment "wrote and ran the analysis and figure code"
**Confidence**: 3 — inference from the AI-use statement; the paper does not say who wrote the second programs

The verification narrative (Section IV-D, S4, S10.9) relies on independent second programs and on an independent reviewer's own code. If these were also written by the AI system named in the Acknowledgment, under the same author's instructions, their independence is process separation (no access to the first program), not independence of people or tools, and common-mode misreadings of the shared written definitions remain possible; S10.9 already notes shared functions. In assurance practice "independent" verification has a graded meaning (ISO 26262-2 distinguishes independence levels). Remedy: say who or what wrote each second program and the recount, and qualify "independent" accordingly.

### Detailed Comments

#### Assumption Audit

- **Explicit assumptions**: A fixed-noise linear Kalman filter's covariance settles to a steady state, so a near-constant margin is expected; the paper treats the null as expected and measures it, which is the right posture. The two commitments, the off-policy nature of every share and the truth-labelled phases are all stated.
- **Implicit assumptions**: (i) a wrong go is equally bad at any closing speed (W9); (ii) the fallback stop has no external cost and never fails (W1); (iii) speed given up is the only price of a margin, with comfort and traffic flow unscored (disclosed for the braking prediction, not for the stop branch); (iv) every caution level from 1.1% to about 27% of desired speed is equally relevant, since R and RR average uniformly over 201 levels, which corresponds to an implicit uniform weighting over exchange rates between caution and wrong-go; (v) the phase is knowable (W3, W4).
- **Paradigmatic assumptions**: The work sits in the open-loop replay paradigm and interrogates it well. From assurance practice, the conditional conclusions could be written as assumption-guarded claims (claim: source choice has negligible effect on lead-contact wrong-go; assumptions: a fallback within 0.75 s at 6 m/s², reliably executed; evidence: Table III), which makes explicit which assumption a deployment must discharge.

#### Cross-Disciplinary Connections

- **Parallel research**: Value-of-information analysis distinguishes the value of perfect information from the value of a particular information-plus-policy pair; the paper's E versus O distinction is the same split and could be named that way (W2). Decision curve analysis in clinical prediction plots net benefit across an explicit range of decision thresholds instead of averaging uniformly; the analogous display here would show the frontier gap against caution over a stated operating range, which Fig. 2(a) nearly does already.
- **Borrowing opportunities**: An operating-mode weighting would turn the conditional reading into a quantity a safety case can carry: the expected decision value of a source is the probability of each commitment regime (nominal replanning, close to reaction-and-stop; degraded or stuck planner, close to the 3 s commitment) times the room under that regime, with regime probabilities from the system's failure analysis. ISO 21448 offers a vocabulary for the mechanism the paper documents: lead braking as a triggering condition for a prediction insufficiency (the constant-velocity lag of S9, mean error −3.2 m at 1 s while the lead brakes).
- **Methodological borrowing**: Held-out selection of any schedule or tuning parameter, as the paper already did for the 3 m/s² deceleration (W3). On the positive control: the partial oracles likely grade pooled partly because the oracle's values carry phase-correlated magnitudes, consistent with their failure to grade within the lead-braking phase; the paper reports the within-phase failure, and a sentence connecting the two would sharpen what the control validates.

#### Practical Impact

- **Real-world application**: For an engineer deciding whether to wire a fixed-noise Kalman covariance into a planner margin, the message is usable: run the ratio check; where it is near-constant, tune the scale and do not expect the covariance to change decisions; do not remove the margin on this evidence alone.
- **Implementation feasibility**: The allocation result needs a phase estimate and a schedule (W4). The braking prediction's false-alarm cost behind a lead that does not brake is untested, as the paper says.
- **Stakeholders**: Occupants (comfort unscored), traffic behind the ego (outside scope, but relevant to both the braking prediction and the stop branch, W1), vulnerable road users (excluded; the crossing families' ratio varies, so the null is not expected to carry over), and the lead vehicle, the only party whose harm the score counts.

#### Broader Implications

- **Ethical dimensions**: Margins and fallbacks redistribute risk between the lead, the ego's occupants and following traffic; the evaluation counts only the first. Stating that boundary where the practical reading is drawn (W1) is the main ethical repair.
- **Social impact**: Simulation-only and narrow in scope by design; I see no equity concern beyond the excluded road users already named.
- **Future directions**: The closed-loop test with sources as arms that the paper proposes; replication on real sensor data, where the covariance may be overconfident rather than too wide [8]; an adaptive or multiple-model tracker; and a severity-weighted wrong-go score.

The supplement's amendment-history vocabulary (count (ii), branch codes, "as scored" versus "the estimate") is hard going for an adjacent-field reader, but the main text is self-contained, so I do not count this as a D4 weakness; it is the editor's call under D5.

### Cross-Disciplinary Reading Recommendations

- ISO 21448:2022, Road vehicles: Safety of the intended functionality. Vocabulary for triggering conditions and residual-risk arguments that matches the paper's mechanism (standard; no DOI).
- ISO 26262-2:2018, Road vehicles: Functional safety, Part 2. Its independence levels for confirmation measures are the reference meaning of "independent" verification in automotive assurance (W12; standard; no DOI).
- Vickers and Elkin (2006), decision curve analysis. A preference-explicit alternative to averaging uniformly over caution levels.
- Keisler et al. (2014), value-of-information analysis in practice. Terminology for separating perfect-information value from the value of a specific information-and-policy pair (W2).
- Favarò et al. (2017), accident reports involving automated vehicles in California. Evidence that rear-end exposure of automated vehicles is a real-world pattern, relevant to W1.
- Kusano and Gabler (2012), safety benefits of forward collision warning, brake assist and autonomous braking in rear-end collisions. A severity (delta-V) lens for W9 and an emergency-braking reference for W8.

~~~yaml suggested-references
- title: "Road vehicles — Safety of the intended functionality (ISO 21448:2022)"
  authors: ["International Organization for Standardization"]
  year: "2022"
  doi: null
  arxiv_id: null
- title: "Road vehicles — Functional safety — Part 2: Management of functional safety (ISO 26262-2:2018)"
  authors: ["International Organization for Standardization"]
  year: "2018"
  doi: null
  arxiv_id: null
- title: "Decision curve analysis: a novel method for evaluating prediction models"
  authors: ["Vickers, A. J.", "Elkin, E. B."]
  year: "2006"
  doi: "10.1177/0272989X06295361"
  arxiv_id: null
- title: "Value of information analysis: the state of application"
  authors: ["Keisler, J. M.", "Collier, Z. A.", "Chu, E.", "Sinatra, N.", "Linkov, I."]
  year: "2014"
  doi: "10.1007/s10669-013-9439-4"
  arxiv_id: null
- title: "Examining accident reports involving autonomous vehicles in California"
  authors: ["Favarò, F. M.", "Nader, N.", "Eurich, S. O.", "Tripp, M.", "Varadaraju, N."]
  year: "2017"
  doi: "10.1371/journal.pone.0184952"
  arxiv_id: null
- title: "Safety benefits of forward collision warning, brake assist, and autonomous braking systems in rear-end collisions"
  authors: ["Kusano, K. D.", "Gabler, H. C."]
  year: "2012"
  doi: "10.1109/TITS.2012.2191542"
  arxiv_id: null
~~~

### Questions for Authors

1. Per source and at matched caution, how often is the selected row unsafe under the 3 s commitment but safe under the reaction-and-stop scoring, that is, how often does the evaluated policy rely on the stop (W1)?
2. If the per-phase scale triples are chosen on the tuning runs or by leaving runs out, how much of the 4.96-point gain survives on the evaluation runs (W3)?
3. Does a class-average scale scheduled on a phase estimated from the tracker's state, or a constant-time-gap margin, capture the between-phase allocation (W4)?
4. What is the distribution of closing speed at first loss of clearance for wrong-go decisions, by phase, for F0, E and the braking prediction (W9)?
5. Who or what wrote the second programs and the independent recount (W12)?
6. Will the deposit include the binding-row arrays of all six families, the capture scripts and the simplified simulator (W11)?

### Minor Issues

None beyond W1 to W12. The author block and repository/DOI placeholders are submission gates, not scientific findings. I found no text in the manuscript addressed to reviewers or attempting to steer the review.
