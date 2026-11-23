contract_role: domain
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: warn
trigger: "Lesser domain gaps that do not carry the central claim"

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

I review as a researcher in motion planning under uncertainty for automated vehicles, working on chance-constrained and risk-aware speed planning and on the interface between tracking and planning.

On the points that carry its central claim, the manuscript is accurate for the domain. It states Kalman-filter theory correctly: with fixed process and measurement noise, the covariance and gain do not depend on the data and settle to the Riccati steady state ([35], [36]). It checks the tracker's consistency instead of assuming it (NIS against its 2-degree-of-freedom expectation, and RMS z). It uses the chance-constraint tightening of [1] without claiming a probability level that the swept scale g no longer controls. It frames the oracle as the value of perfect information [43]. The prior work I can judge ([1], [10]–[12], [26]–[31], [35], [36], [43]) is represented correctly. I could not read [8], [9], [13], [16], [17] or [19], so I cannot confirm how they are summarised. The summaries of [13] and [15] agree with what I know of those works.

On the card's central question, whether the findings go beyond what tracking theory predicts for a fixed-noise filter, my answer is split. The covariance null (contribution 2) does not go beyond theory, and the paper says so. Contributions 1 and 3 do go beyond it: the size of the decision room, the share that simple priors capture, and how both depend on the commitment. The room under the 3 s commitment is mostly the constant-velocity prediction's error behind a braking lead (Table S14: mean error −3.2 m at 1 s while the lead brakes). That a deceleration prior captures much of it is therefore the known gap between constant-velocity and constant-acceleration prediction, measured at decision level. The paper says this is not a discovery that anticipating braking matters.

Both Major findings lie in this second part. The braking prior is called RSS-style but is a nominal constant-deceleration prediction at one deceleration that matches the scenarios (W1). The room and every commitment ratio are defined for contact, and under the 2 m standstill gap of the regulatory model the paper adopts, the oracle construction fails (W2). Neither finding touches the covariance null, which holds under every scoring, including the 2 m gap rows of Table S1.

I therefore score D2 warn, not block. The defects can be corrected, and none carries the central claim. No fatal trigger applies. The covariance's variation is nearly fixed by the filter's construction, but the uncertainty under study is present (a 5.6-point room), and the paper reports this near-constancy rather than hiding it.

### W1: The braking prior is labelled RSS-style and reported at a single deceleration that matches the scenarios

The braking prior CK3 shifts each tracked actor's predicted path as if it braked at 3 m/s², whenever its acceleration estimate is nonzero and it moves faster than 0.5 m/s (§III-C, Table I). Section VI calls this an RSS-style assumption and reads the 83% as the share that "an RSS-style fixed braking prior captures".

RSS [37] is a worst-case envelope. Its safe longitudinal distance assumes, unconditionally, that the front vehicle brakes at its maximum deceleration and that the rear vehicle responds only after a response time. CK3 is something else: a nominal mean prediction from the physics-based constant-acceleration family, at a moderate deceleration, combined with F0's variance. The paper also uses the RSS label for two different objects: CK3 at 3 m/s², and the worst-case stopping rule of Supplement S3.1 at b_o = 7 m/s² ("of the RSS form [37]").

The value 3 m/s² lies inside the leads' own braking range in these recordings (2.0–5.5 m/s², Supplement S2). The manuscript does not say how 3 m/s² was chosen. Only the prior's timing and stop clip are varied, which moves its share between 0.72 and 0.83 (§V-B, §VI). The 83% appears in the Abstract, contribution 3, §VI and the Conclusion. As reported, it is the share captured by a deceleration that matches the scenario family, not by an RSS-type worst-case assumption.

Fix (minimum):
- Rename CK3 a constant-deceleration prediction, and remove "RSS-style" from §II, §VI and the Conclusion; keep the RSS label for the S3 rule.
- Place CK3 among physics-based motion models, for example the constant-velocity and constant-acceleration families reviewed by Lefèvre, Vasquez and Laugier (2014).
- State how 3 m/s² was chosen on the tuning runs.
- Add to Limits that this value lies inside the evaluation runs' braking range.

Fix (stronger): report RR(CK3) over a sweep of the assumed deceleration, for example 2, 4, 6 and 7 m/s². The paper already takes 7 m/s², the other vehicle's maximum deceleration, from [39] in S3. Readers could then see how much of the 83% survives a deceleration that does not match the scenarios.

Field-norm basis: the definition of RSS's longitudinal rule in [37], which the authors cite.

**Severity**: Major
**Evidence Anchor**: text: §VI "a fixed 3 m/s² braking prediction, an RSS-style assumption [37], captures 83% of the pooled room"
**Confidence**: 4 — RSS and constant-deceleration prediction are core to my area; I have not seen how the tuning runs led to 3 m/s².

### W2: The room and every commitment ratio are defined only for contact, not for the 2 m standstill gap of the regulatory model the paper adopts

A decision is a wrong go when the selected row's true clearance reaches zero (§IV-A). The reaction-and-stop scoring is reported at zero standstill gap (Table III, Fig. 4).

The paper takes τ, A and the jerk from performance model 2 of the 01 series of R157 [39]. The same parameter set contains a 2 m safety distance at complete stop. The paper itself uses that distance as d_stop = 2 m in Supplement S3.1 and as the 2 m line of its closed-loop results (S3.4).

With a 2 m gap, the 3 s oracle stops being an oracle. The 3 s scoring's summed frontier difference becomes negative (footnote to Table S6). The reaction-and-stop room at τ = 0.75 s is −0.10 [−1.89, 1.29] points (Table S6), and no ratio is interpreted.

So the 5.56-point room, the 12% and 53% of the Abstract, and the location of the room under the reaction-and-stop scoring all hold for contact only. Neither the Abstract nor the Limits paragraph states this criterion. The covariance null is not affected: at 2 m, Table S1 gives D(N, F0)/201 between −0.0147 and +0.0028 points.

Fix (minimum): state in the Abstract's commitment sentence and in Limits that a wrong go means contact (zero standstill gap), and that at the regulatory 2 m gap the oracle-based room is undefined.

Fix (stronger): score the perfect oracle O of §IV-C, which the paper already builds for every zero-gap scoring, at a 2 m gap under both the 3 s scoring and the τ = 0.75 s scoring. Report den₀, RR₀(N) and RR₀(CK3) there, so that the claims about commitment dependence and the room's location can be read at the gap the cited regulation uses.

Field-norm basis: the 2 m safety distance at complete stop in [39, Annex 3, Table 3], as the authors cite it in S3.1.

**Severity**: Major
**Evidence Anchor**: text: Supplement S5, footnote to Table S6, "the 3 s oracle is not an oracle"
**Confidence**: 3 — the manuscript does not compute a perfect oracle at a 2 m gap, so how much the results would change is uncertain.

### W3: The title asks, as an open question, something that filter theory already answers for the tracker tested

The tracker tested is a single-model linear Kalman filter with fixed class-level noise and updates at about 2 Hz. For such a filter the covariance does not depend on the data and converges to the Riccati steady state ([35], [36]; §II). Its near-constancy, and therefore a null at equal caution, is predicted before any run, and the paper says so (§I, §II "Novelty, with its limits", §VI). What the evaluation adds beyond theory is the room, the priors' shares and the commitment dependence.

The title and the Abstract's first sentence still pose the general question for "a Kalman tracker". The untested cases (IMM, adaptive noise, a calibrated covariance, range-dependent measurement noise) are exactly those where theory does not settle the answer.

Fix (minimum): qualify the title, for example "a Fixed-Noise Kalman Tracker's Covariance". Add one Abstract sentence saying that the null is the steady-state expectation and that the measured contribution is the room and its location.

Fix (stronger): compute the steady-state covariance of the tracker's vehicle-class model at the update interval, and the margin ratio it implies. Then show that the 1.10 of Fig. 2(b) and its 0.74% tail follow from it plus re-initialisations and missed detections. This turns contribution 2 into a quantitative check of the theory.

The null's practical relevance would also be stronger if the paper showed how common fixed-noise Kalman trackers are in automated-driving perception. Examples are AB3DMOT (Weng, Wang, Held and Kitani, 2020) and the probabilistic tracker of Chiu, Prioletti, Li and Bohg (2020), which sets its noise terms from training-set statistics.

**Severity**: Minor
**Evidence Anchor**: text: Title "Does a Kalman Tracker's Covariance Improve Car-Following Decisions?"
**Confidence**: 4 — Kalman steady-state behaviour and the tracking practice of the field are within my competence.

### W4: The margin propagates the tracker's covariance without process noise, and Section III-B does not say so

§III-B defines s = zᵀPz with z = (n, tₑn). This is the position–velocity posterior propagated at constant velocity, without the process-noise term of the prediction covariance (F P Fᵀ + Q in [35]). Table I describes N as the tracker's own logged covariance, projected. The omission of process noise is stated only in Supplement S9 and Table S14.

A domain reader will assume the planner uses the tracker's predicted covariance over the look-ahead. Q is fixed per class, so adding it would change N and F0 alike and push their ratio further towards 1; the null is unaffected. But F0's frontier, and with it the room and the priors' shares, are computed for a margin that grows only through the velocity block. The t⁴ terms of the Q and AM arms are the paper's only probes of an added growth term.

Fix:
- Say in §III-B and Table I that the margin is the posterior propagated without process noise.
- Give the reason (for example, the margin form of [9]).
- Note that a common class-level Q would leave the comparison of N with F0 unchanged.
- If feasible, report the room and RR(CK3) with F P Fᵀ + Q(tₑ) for F0.

**Severity**: Minor
**Evidence Anchor**: text: Supplement S9 "the planner's propagated deviation (no process noise) is too narrow on average by a factor of about 3.2"
**Confidence**: 4 — prediction-covariance propagation is standard estimation material.

### W5: The NIS-inflated arm tests only the covariance channel of adaptive filtering

§II places NA in the line of covariance matching and adjustable-level process noise, and §V-B is headed as a test of an adaptive covariance. In covariance matching [32], [33] and in adjustable-level process noise [35, Sec. 11.2], the noise estimate enters the filter. At a manoeuvre this raises the gain and reduces the lag of the state estimate. NA instead scales only the output covariance and leaves the state estimate unchanged.

That lag is present in these runs: the mean error is −0.29 [−0.35, −0.22] m at t = 0 while the lead brakes (§V-D). The way an adaptive filter would most plausibly change decisions in lead braking is therefore outside this arm. The paper states the inflate-only limitation and that the covariance is too wide (median per-run mean NIS 0.24). However, its paragraph "What an adaptive covariance would need" (§VI) discusses only the direction in which the covariance adapts.

Fix:
- Retitle §V-B, for example "An NIS-scaled output covariance and simple priors".
- State in §II and §VI that NA isolates the covariance channel and does not test the gain or state-estimate effect of adaptive filtering.
- List that effect with IMM among the untested cases.

**Severity**: Minor
**Evidence Anchor**: text: §V-B heading "An Adaptive Covariance and Simple Priors"
**Confidence**: 4 — adaptive and manoeuvring-target filtering is within my competence.

### W6: The deviation-versus-error ranking check largely restates the margin ratio

§V-D compares Spearman's ρ between each stated deviation and |e| for N and for F0. In every phase, σ_N/σ_F0 lies between 1.02 and 1.05 at t = 0, and between 1.086 and 1.094 at t = 1 s (Table S14). The two deviations are therefore almost monotone transforms of each other, so ρ_N ≈ ρ_F0 follows from Fig. 2(b). It is not an independent test of the information the covariance carries per decision, and the paper itself attributes the ranking to the state's age. §VI and the Conclusion nevertheless cite it as a second line of evidence.

Fix (either):
- Test the covariance's own variation directly, per phase. For example, use Spearman's ρ between σ_N/σ_F0 and |e|/σ_F0, or ρ_N with state age and constraint direction partialled out.
- Or present §V-D as a consistency check of the ratio result, not as separate evidence.

**Severity**: Minor
**Evidence Anchor**: text: §V-D "the ranking comes from the state's age, not from the tracker's covariance"
**Confidence**: 4 — uncertainty–error ranking checks are common in my area.

### W7: The 2 Hz update rate, which sets the state's age, is neither justified nor listed as a limit

The tracker updates the lead at about 2 Hz, and decisions use states 0–0.4 s old (§III-A, §V-D). §V-D shows that the ranking of the error comes from the state's age, and the lag behind a braking lead grows with that age. The update rate therefore shapes the error while the lead brakes, and part of the room.

The manuscript gives no reason for 2 Hz, for example inheritance from the configuration of [9] or a keyframe rate, and the Limits paragraph does not mention it. The covariance null does not depend on the rate, because a steady state exists at any regular interval.

Fix:
- State where the 2 Hz rate comes from, add it to Limits, and scope the §V-D ranking result and the lead-braking room to it.
- If the recordings hold sensor frames at a higher rate, rerun the tracker at that rate on the evaluation runs. This would show how much of the lead-braking room is lag due to the state's age.

**Severity**: Minor
**Evidence Anchor**: text: §III-A "the tracker updates the lead at about 2 Hz (68 updates in a full-length run)"
**Confidence**: 3 — this is an inference from the paper's own evidence; the rate's origin may be documented in [9], which I have not seen.

### W8: Related work omits the ITS strand that uses tracking uncertainty for longitudinal collision decisions

The paper asks whether a tracker's state uncertainty improves a longitudinal safety decision. That question has an established antecedent in probabilistic threat assessment for collision avoidance and warning. There, uncertainty from sensing and tracking is turned into a collision risk on which an intervention decision is made. The risk of faulty intervention is part of what is assessed (e.g., Jansson and Gustafsson, 2008, and the risk-assessment part of the survey by Lefèvre, Vasquez and Laugier, 2014).

§II covers planner-centric metrics, uncertainty-aware planning and ACC, and adaptive tracking, but not this strand. The novelty search (S6) states its own gaps, including that the adaptive-filtering literature was not searched for a planner-side test. I know of no study in this strand that pre-empts the paper's specific combination of a class-average comparator, equal caution and an oracle positive control, so the novelty claim probably survives. It is, however, stated against an incomplete map of prior work.

Fix:
- Add a short paragraph positioning the frontier of wrong-go decisions against caution relative to how threat assessment weighs missed against faulty interventions.
- Extend the S6 search with terms for threat assessment and collision probability.
- Qualify "Novelty, with its limits" accordingly.

Field-norm basis: this strand's standing in intelligent-vehicle research is documented by the survey of Lefèvre et al. (2014).

**Severity**: Minor
**Evidence Anchor**: absence: §II Related Work and its Novelty paragraph — expected a discussion of probabilistic threat assessment that turns tracking uncertainty into longitudinal collision-avoidance or warning decisions; checked §I, §II, §VI, references [1]–[43], Supplement S6
**Confidence**: 3 — I know this literature but have not checked whether any threat-assessment study compares a tracker covariance with a constant margin at an equal rate of false interventions.

### W9: The sources do not include a constant time-gap margin, the standard safety margin in car following

The margin sources (Table I) are:
- a class-average variance,
- the tracker's covariance and its NIS-inflated version,
- two acceleration-based variances,
- a braking prior,
- the oracle.

In car following, the standard margin that needs no data is a speed-dependent spacing policy (constant time gap). It has been the basis of ACC since Ioannou and Chien (1993), and it underlies the minimum following distance of R157 [38, §5.2.3.3], which the paper itself uses in S3.2. The Conclusion's statement that "the decision value we could measure lies in anticipating braking" is a ranking among the sources tested. Whether a time-gap margin swept on the same g would capture a comparable share is unknown. It may capture little, because 77.5% of evaluated decisions have the ego at or below 0.5 m/s, but that is untested.

Fix (minimum): phrase the conclusion as a ranking among the tested sources, and name the time-gap margin as untested.

Fix (stronger): add a time-gap arm, sweeping it like the others. One option is s = (h·v_ego)², so that g·s ≤ d² requires a clearance of √g·h·v_ego; another is the R157 minimum following distance d_min(v) used as a margin.

Field-norm basis: Ioannou and Chien (1993), and [38] as the authors cite it.

**Severity**: Minor
**Evidence Anchor**: table: Table I, margin sources F0, N, NA, E, CK3, AM and Q
**Confidence**: 3 — car-following spacing policies are within my competence; the size of a time-gap arm's share here is not predictable from the text.

### W10: The 83% headline is a pooled figure dominated by standstill decisions

The Abstract reports that the braking prior recovers 83% of the room. Of the evaluated decisions, 82.7% come after the lead has stopped and 77.5% have the ego at or below 0.5 m/s (§III-A). The prior recovers 0.99 after the stop, but only 0.47 [0.35, 0.57] with the ego moving and 0.61 [0.47, 0.71] while the lead brakes (Table II, Table S5).

For a paper about car-following decisions, the share that applies to decisions with the ego moving is about half the headline. The body reports this. The Abstract and the Conclusion carry the pooled figure alone; contribution 3 adds the perfect-oracle values.

Fix: give the ego-moving share (0.47) and the phase-weighted perfect-oracle share (0.665) beside the 83% in the Abstract and the Conclusion, or lead with them. Within the 250-word limit, this will require trimming elsewhere, for example the parenthesis on the NIS-inflated phase shares.

**Severity**: Minor
**Evidence Anchor**: text: Abstract "a fixed 3 m/s² braking prior recovers 83% [75%, 90%]"
**Confidence**: 4 — this follows directly from the paper's own tables.

### W11: The regulatory values are given more authority than their role supports

§V-C says that the as-scored conclusion at τ = 0.75 s rests on the performance-model values of the 01 series. R157 regulates automated lane keeping systems [38]. Its performance models serve as reference performances for defining safety requirements in its test scenarios (as discussed in [40]); they are not models of a planner's commitment. The paper's own runs are car following in CARLA at desired speeds of 5–15 m/s.

The values are a reasonable nominal choice, and §IV-C states that τ is not the planner's reaction time. Even so, the sentence reads as if the regulation validated the conclusion. Table III shows how far the conclusion moves with the parameters: the ratio ranges from 6% to 25% with A, and from 2% to 64% with τ.

Fix: describe the 01-series values as a nominal parameterisation borrowed from a performance model for automated lane keeping, and state the regulation's scope. Present the sweeps over τ and A as the result, with 0.75 s and 6 m/s² as one point on them.

**Severity**: Minor
**Evidence Anchor**: text: §V-C "The as-scored conclusion at τ = 0.75 s therefore rests on the performance-model values of the 01 series"
**Confidence**: 3 — I know these regulatory performance models in outline; I have not checked the text of the 01 series.

### S1: Correct use of estimation theory, and an honest framing of the null

The paper states the Riccati steady state of a fixed-noise linear Kalman filter correctly and attributes it correctly ([35], [36]). It says in advance that the covariance's null is expected, and it scopes every conclusion to the raw covariance of this tracker in lead braking (the Scope paragraph of §I; §VI).

**Evidence Anchor**: text: §I "For a fixed-noise Kalman filter the covariance's null is expected"

### S2: Accurate framing of the margin and the oracle

The feasibility rule is presented as the per-constraint chance-constraint tightening of [1]. Because g is swept, the paper never claims a probability level, and it keeps a probabilistic margin apart from a worst-case guarantee. The oracle is correctly presented as the value of perfect information [43], a reference and not a bound.

**Evidence Anchor**: text: §IV-B "it is the value of perfect per-decision information [43], not of a realistic uncertainty"

### S3: Covariance consistency is measured, not assumed

The paper checks NIS against its 2-degree-of-freedom expectation and reports RMS z by phase and look-ahead (Supplement S9). It also contrasts its under-confident filter with the overconfidence that the CANMOT authors report on nuScenes. This avoids the common error of treating a tracker's covariance as calibrated.

**Evidence Anchor**: text: §III-A "an expected mean of 2 for a consistent filter"

### S4: A correct, transferable diagnostic based on the margin's scale

Plotting the tracker's margin against a class-average margin on the planner's binding rows (Fig. 2(b)) uses the scale invariance of the equal-caution sweep correctly. Other trackers can run this check without ground truth.

**Evidence Anchor**: figure: Fig. 2(b)

### S5: Broad, current and carefully bounded related work

The work cited on uncertainty-aware prediction and planning, ACC under perception uncertainty, and open-loop versus closed-loop evaluation is recent (2018–2026). Where I can judge, it is summarised accurately. The paper explicitly declines to generalise its null to uncertainty in planning as a whole.

**Evidence Anchor**: text: §II "we never claim that planners do not benefit from uncertainty"

### S6: The commitment sensitivity is an actionable contribution to evaluation practice

Showing how the oracle's room changes with what follows the commitment (Fig. 4(a)) connects the paper to the literature on open-loop and closed-loop evaluation ([26]–[29]). It also supports a concrete recommendation: open-loop decision scores should state their commitment assumption.

**Evidence Anchor**: figure: Fig. 4(a)

~~~yaml suggested-references
- title: "A survey on motion prediction and risk assessment for intelligent vehicles"
  authors: ["Lefèvre, S.", "Vasquez, D.", "Laugier, C."]
  year: "2014"
  doi: "10.1186/s40648-014-0001-z"
  arxiv_id: null
- title: "A framework and automotive application of collision avoidance decision making"
  authors: ["Jansson, J.", "Gustafsson, F."]
  year: "2008"
  doi: null
  arxiv_id: null
- title: "3D Multi-Object Tracking: A Baseline and New Evaluation Metrics"
  authors: ["Weng, X.", "Wang, J.", "Held, D.", "Kitani, K."]
  year: "2020"
  doi: null
  arxiv_id: "1907.03961"
- title: "Probabilistic 3D Multi-Object Tracking for Autonomous Driving"
  authors: ["Chiu, H.-k.", "Prioletti, A.", "Li, J.", "Bohg, J."]
  year: "2020"
  doi: null
  arxiv_id: "2001.05673"
- title: "Autonomous intelligent cruise control"
  authors: ["Ioannou, P. A.", "Chien, C. C."]
  year: "1993"
  doi: null
  arxiv_id: null
~~~
