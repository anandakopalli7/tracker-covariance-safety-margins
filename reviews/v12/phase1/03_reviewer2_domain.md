# Peer Review Report

## Manuscript Information
- **Title**: Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution: A Fixed-Noise Kalman Tracker in CARLA Lead Braking (draft v12)
- **Manuscript ID**: not available (unpublished; treated as a fresh submission to IEEE Open Journal of Intelligent Transportation Systems, regular paper)
- **Review Date**: 2026-11-19
- **Review Round**: Round 1 (Phase 1 panel, seat 3 of 5)

---

## Reviewer Information

### Reviewer Role *
Peer Reviewer 2 (Domain)

### Reviewer Identity *
Researcher in multi-object tracking and Kalman-filter-based estimation for road vehicles. Familiar with covariance consistency (NIS/NEES), adaptive and multiple-model filtering, and the way tracker uncertainty is passed to prediction and planning.

### Review Focus *
Whether the steady-state account of a fixed-noise EKF covariance fits the reported ratio and its exceptions; whether the tracker description, the innovation-consistency findings and the NIS-inflated source support what is said about "an adaptive covariance"; literature coverage and positioning; and the reading of the after-stop and lead-state results. Special attention to whether the null is stated as a property of this filter in this regime or as something broader. Statistical inference and regulation or deployment context are left to other seats.

---

## Overall Assessment *

### Recommendation *
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision** — scope and reach, not an error in the reported numbers
- [ ] Reject

### Confidence Score *
4. Tracking, covariance consistency and adaptive/multiple-model filtering are core to my expertise. Planner-side scoring, bootstrap calibration and regulation are outside my remit and I did not judge them.

Confidence is an uncertainty/scope disclosure only; it never changes consensus counts, severity, decision bearing, or arbitration.

### Summary Assessment *
The paper asks whether the covariance of a fixed-noise extended Kalman tracker (CANMOT) improves a margin-type speed planner's car-following decisions over a class-average margin in simulated CARLA lead braking. Wrong-go decisions are scored at equal caution, with an oracle margin as positive control. It reports a null: the tracker's margin is a near-constant 1.10 times the class average on 99.26% of binding rows, and its frontier stays within 2.2 of 8,290 decisions of the class average's. It also reports a pooled oracle room of 5.6 points and exploratory decompositions that place the room before the lead's stop and in the first second after it.

From a tracking standpoint the steady-state account is correct. I could reconcile every figure I checked against Tables S14, S26, S27 and V. The wording stays on the narrow side almost everywhere. The weaknesses concern reach. No arm exercises a covariance that varies with the lead's motion: the NIS-inflated arm is inflate-only on a covariance that is already too wide. The null is therefore a measured confirmation of an expectation the Riccati argument already gives. The room's location, which hinges on the tracker's velocity lag, is tied to a filter whose noise is mis-tuned for the simulated sensor (NIS 0.24 against 2) and to 2 Hz with no latency. Both points can be examined offline from the stored detections. Literature coverage is adequate on the planning side, thin on motion-model and covariance-credibility work, and the negative novelty claim leans partly on abstracts. I recommend Major Revision.

---

## Strengths *

### S1: The steady-state account is stated, quantified and consistent with the logged covariances
The paper says in advance that a fixed-noise filter's covariance should be near constant. It then shows a ratio of N's margin to F0's of 1.103 on 99.26% of lead-braking rows. The ratio is set by the velocity block, rising from 1.035 at zero look-ahead to 1.103 at 3 s (Table S14). The same pattern holds in stopped-vehicle and cut-in runs. The expected exception for variable heading is reported (crossing families). I found no number in this chain that conflicts with another.
**Evidence Anchor**: `table: Table V — lead braking 152,264 rows, median ratio 1.103, 99.26% within 5%; stopped vehicle 98.73%; cut-in 99.86%; crossings 8.51% and 4.09%`

### S2: A grid placebo and a gridless frontier separate the 1.10 offset from information
Dividing the class average's critical scales by 1.1029² gives a source with no information beyond F0. The tracker covariance's frontier is then compared with it, and the comparison is repeated gridless. This is the right control for a near-constant multiple on a log grid and removes a plausible artefact.
**Evidence Anchor**: `table: Table S30 — All: RR(N) − RR(P) −0.0003 [−0.0009, 0.0001]; gridless D(N) −0.19 [−0.34, 0.02]`

### S3: The positive control is tested, and its failures are disclosed
Partial oracles are used to show where the measure grades information. The paper says plainly that it does not grade while the lead brakes or with the ego moving, and it reads shares there only as frontier distances. This is the discipline that makes a tracking null interpretable.
**Evidence Anchor**: `table: Table II — Partial oracle, 25%: all 0.269 [0.222, 0.305]; lead braking −0.682 [−0.933, −0.486]`

### S4: The deviation-versus-error check is a proper consistency diagnostic and is read honestly
The tracker's stated deviation ranks the realised error exactly as well as the class average's (ρ 0.453 against 0.458 while braking). The paper concludes that the ranking comes from the state's age and not from per-decision calibration. This is the correct reading of a covariance that carries no information beyond age.
**Evidence Anchor**: `table: Table S14 — t = 0, lead braking: ρ_N 0.453 [0.392, 0.508], ρ_F0 0.458 [0.396, 0.512], ρ* 0.122`

### S5: The lead-state table gives a checkable mechanism for the after-stop room
In the first second after the stop the tracker's speed estimate has median 0.45 m/s against a true 0. The constant-velocity prediction puts the lead a median 1.49 m too far ahead at 3 s. 132 decisions carry 52.2 of the 56.3 after-stop decision-equivalents. These main-text numbers agree with Tables S33, S33b and S34.
**Evidence Anchor**: `table: Table S34 — after the stop, 0–1 s: tracker speed 0.45 [0.18, 1.05] m/s, true 0.00; predicted − true at 3 s 1.49 [0.54, 3.51] m`

### S6: The scope statement and its wording are narrow and accurate
Untested cases are named in the Scope paragraph, in Limits and in S11.9: IMM, calibrated and two-sided adaptive covariances, births, misses and real sensors. The Discussion explicitly refuses to infer that a covariance margin may be dropped from a deployed stack.
**Evidence Anchor**: `text: §I Scope "We do not test a calibrated covariance, a manoeuvre-adaptive (IMM) tracker, or a covariance that adapts in both directions."`

### S7: The literature-reading limitation is disclosed in plain words
The main text and S6 state that part of the threat-assessment literature was read from abstracts only. S6 also lists the search limits: one engine blocked, publisher full texts not searched, IMM and adaptive filtering not searched for a planner-side test. The novelty claim is scoped to the sources searched.
**Evidence Anchor**: `text: §II "In the abstracts of this literature that we read (we did not read the full texts)"`

### S8: Departures from steady state inside the data are reported, not hidden
Young and coasting tracks (ratio 1.68 after two missed updates), the run with ratios 0.703–1.043 at track ages of 21.5–31.0 s, and the families where the check is silent are all reported.
**Evidence Anchor**: `table: Table S27 — track age [0.5, 1) s: 84 rows, all more than 5% from the median, median ratio 1.682`

---

## Weaknesses *

### W1: No arm exercises a covariance that varies with the lead's motion; the NIS-inflated source is not a fair test of "an adaptive covariance"
**Problem**: The only adaptive source is NA, a scalar λ = max(1, mean NIS/2) on the output covariance. It is inflate-only and driven by position-block NIS averaged over the last three updates, i.e. about 1.5 s. The median per-run mean NIS is 0.24, so λ equals 1 almost everywhere. NA changes critical values in 217 of 8,290 decisions, 27 of them in the five short runs. It cannot act on the velocity block (NEES 5.08 against 2 while the lead brakes), on the gain or on the state, which are the channels where adaptive filtering [34]–[37] and IMM [32], [33] act. Section V-B is headed "An Adaptive Covariance and Simple Predictions", and Table I labels NA "Tested". The headline null for N is also what the Riccati argument of Section II already implies. The paper therefore cannot say whether the design would register a tracker whose covariance does vary. The paper says this in places ("says nothing about adapting the velocity block", "we did not test them"), but the heading and the table label invite the wider reading.
**Evidence Anchor**: `text: §V-B "It changes the critical values in only 217 decisions, because it can only inflate and the innovation covariance is already too wide"`
**Why it matters**: The paper's value over the analytical expectation lies in showing the design can detect decision value from a varying covariance. Without one such arm, the null is a verification of the steady-state argument, and the design's sensitivity to realistic covariance variation is untested. Graded oracles detect random mixing, which is not a tracker-like covariance.
**Suggestion**: Re-run the tracker offline on the stored detections (the Data Availability statement says they are kept) with at least one source whose covariance and state respond to the manoeuvre. Examples: a CV/CA IMM, or a fading-memory or innovation-adaptive Q acting on the velocity block as in [34]–[37]. Score it with the existing machinery, or rename NA "output-scalar NIS inflation", move it out of the "adaptive covariance" frame, and state in the abstract and contributions that no covariance-varying tracker was tested.
**Severity**: Major
**Confidence**: 4 — core expertise: adaptive and multiple-model filtering

### W2: The room's location and the braking prediction's 83% rest on a lag that depends on a filter mis-tuned for the simulated sensor, and no re-tuned or multiple-model tracker is run
**Problem**: Position NIS is far below 2 (median per-run mean 0.24; Fig. S1), so the innovation covariance, hence the measurement and process noise, is over-specified for this sensor. The paper puts this down to the simulated sensor and says it did not test that. Yet the after-stop room (41.7 of 460.7 pooled decision-equivalents; 56.3 on its own frontier) is carried by the velocity lag of this filter: 132 decisions in which the tracker still reports the lead faster than 0.5 m/s. How fast a constant-velocity Kalman filter's velocity responds to a stop depends on the gain, hence on the ratio of the assumed process and measurement noise. A filter whose noise gives NIS near 2, or one with an acceleration state, would have a different lag. Limits and S11.9 name latency, update rate, misses and curved roads as directions of change. They do not name filter tuning, although the NIS finding points straight at it. The braking prediction's recovery of 55.9 of those 56.1 after-stop decision-equivalents follows from the same lag.
**Evidence Anchor**: `text: §III-A "the simulated sensor data are a likely reason, which we did not test"`
**Why it matters**: The second contribution (what sets the pooled room, and that the tracker's velocity still lags the stop) is conditional on one mis-tuned configuration. The generalising sentence "an open-loop decision score should state its commitment, population and recording policy" is then supported by a case in which a tuning choice may itself move the room.
**Suggestion**: Re-run the tracker on the stored detections with noise set so that position NIS is near 2, and with a CA or IMM variant. Report the after-stop lag (Table S34), the room by phase (Table S33) and the braking prediction's share. If the room changes materially, say so in Section VI, and add filter tuning to the list of conditions in Limits. If it does not, the paper gains a robustness result.
**Severity**: Major
**Confidence**: 3 — core expertise, but the size of the tuning effect on this tracker is not shown and I did not recompute it

### W3: The reach of the after-stop explanation and of the braking prediction's recovery is narrower than its prominence suggests
**Problem**: Three points, each partly acknowledged. (a) The lag explains only the after-stop first second, 41.7 of 460.7 (9%) of the pooled room. For the 91% before the stop the paper states that "the attribution does not separate that lag from the braking itself", and offers the per-phase scale schedule, a statistical allocation, in place of a mechanism. (b) The braking prediction's trigger (speed above 0.5 m/s with a nonzero acceleration estimate) selects precisely the decisions with spurious residual speed. In every run the lead brakes to a stop, so "decelerating track ⇒ it stops" is always right here. The 3 m/s² was tuned on 20 runs from the same generator. Its cost behind a lead that does not brake could not be measured because the benign runs have no vehicle in lane. (c) The abstract states the 83% without the condition that every lead brakes to standstill, which appears only in Section VI.
**Evidence Anchor**: `text: §VI "The share is an open-loop, off-policy quantity on runs in which the lead always brakes"`
**Why it matters**: A reader of the abstract and Table II will take 83% as a property of a braking prediction. It is a property of that prediction on a scenario family in which it cannot be wrong about the lead's behaviour. The tracking-side separation (staleness up to 0.4 s, filter smoothing, the CV model) is not attempted.
**Suggestion**: Put the condition in the abstract in four or five words. Add a run-level breakdown of the 132 decisions (runs, decisions per run). Separate staleness from smoothing, for example by scoring the decision on the state at its own timestamp. Give intervals for Tables S33, S33b and S34.
**Severity**: Minor
**Confidence**: 4 — core expertise; the paper already hedges (a) and (b)

### W4: The ratio check's exceptions are explained by heading without a direct test, and one straight-road family is left unexplained
**Problem**: Section V-E attributes the crossing families' variation (8.51% and 4.09% within 5%) to the rotation of object-frame noise by the estimated heading. No analysis of ratio against heading angle, track age or missed updates is given. Benign driving, a straight-road family where heading should be constant, reaches only 60.45% within 5%, and no reason is given. In Supplement S10.7 one evaluation run has ratios between 0.703 and 1.043 over 96 decisions at track ages of 21.5–31.0 s, a long-lived stationary track inside the evaluated population. Heading drift of a stationary track would fit the paper's own mechanism, but the main text does not say so. The ratio also varies with look-ahead (σ_N/σ_F0 1.035 at t = 0, 1.103 at t = 3 s; Table S14), so "a near-constant multiple selects nearly the same rows" holds at the binding constraint but not across a row. The ±5% tolerance is not related to how often two rows' critical scales lie within 10% of each other, which is what would flip a selection.
**Evidence Anchor**: `text: §V-E "so the ratio can vary with a crossing actor's heading alone, without carrying information about the error"`
**Why it matters**: Contribution 4 offers the ratio as a ground-truth-free predictor of where the null carries over. A predictor whose failure mode is asserted but not shown, and which leaves one family unexplained, is weaker than presented. The paper does hedge ("we expect ... but did not test it").
**Suggestion**: Add a table of the ratio's spread against estimated heading offset and track age for the crossing and benign families. Say what happened in the S10.7 run. Report the share of decisions whose first-feasible row would change under a ±5% change in the margin ratio.
**Severity**: Minor
**Confidence**: 4 — core expertise; the lack of a heading analysis is visible in the package, the cause of the benign result is not

### W5: The innovation-consistency findings are summarised on a population-mix basis and on decision-time quantities, without intervals
**Problem**: "The innovation covariance is mostly too wide" and "the opposite of the overconfidence reported on nuScenes" are dominated by the stationary after-stop phase: 1,383 of about 1,684 evaluated updates with mean NIS 0.10. While the lead brakes, mean NIS is 1.47 on 150 updates, below 2 but not far from it, and no interval is given. The velocity NEES (5.08 against 2.06 before onset) is computed at decisions (755, five per tracker update) against the true velocity at decision time. The stale state of up to 0.4 s is therefore folded in, so it mixes filter inconsistency with extrapolation staleness. Neither the NEES at the update time nor an interval allowing for the repetition of decisions is given. The claim "the velocity block of the covariance that the planner uses is too narrow while the lead brakes" is used to motivate the Discussion's "what an adaptive covariance would need".
**Evidence Anchor**: `table: Table S34b — Lead braking: 150 updates, mean NIS 1.47, mean velocity NEES 5.08 (755 decisions); After stop: 1,383 updates, mean NIS 0.10`
**Why it matters**: The consistency picture is used as the paper's evidence of where a covariance could help. Its direction is probably right, but its size and its attribution to the filter and not to staleness are not established.
**Suggestion**: Give NIS and NEES per phase at the update time with run-level intervals, and the NEES with the truth at the state time. Phrase the opposite-to-nuScenes remark as applying to stationary decisions.
**Severity**: Minor
**Confidence**: 4 — core expertise: covariance consistency

### W6: The negative novelty claim and the positioning rest on abstracts and on a narrow conjunction; motion-model and covariance-credibility literature is thin
**Problem**: The claim "found no study that tests whether a real multi-object tracker's state covariance improves an automated vehicle planner's decisions over a class-average covariance, ..." joins six qualifiers (real, multi-object, state covariance, class-average comparator, realised future, equal caution plus oracle). Few studies could meet it, so the absence is weak evidence of novelty. For the threat-assessment and tracking references [44]–[55], whose abstracts only were read, the finding "no evaluation carries a tracker's covariance through to the decision" is exactly what full texts would settle. The disclosure is plain and honest. The closest relatives (Deglurkar [13], Ivanovic [15], Shah [17], Chen [14]) are mostly 2024–2026 preprints. The tracking side cites IMM and adaptive-filter classics but not the motion-model comparisons for vehicle tracking, the credibility-of-covariance literature, or lead-vehicle acceleration anticipation in ACC and car following. These bear directly on the braking-prediction and lag findings. See "Missing Key References".
**Evidence Anchor**: `text: §II "we found no study that tests whether a real multi-object tracker's state covariance improves an automated vehicle planner's decisions"`
**Why it matters**: The paper's own position is "the mechanism is not new; the contribution is the evaluation". A fuller map of vehicle-tracking motion-model comparisons would show readers which varying-covariance sources the design could next be run on.
**Suggestion**: Read the full texts for the closest of [44]–[55], or restate the claim as an abstract-level observation. Add the references listed below (each marked [to verify]). State the peer-review status of the preprint relatives.
**Severity**: Minor [FIELD-NORM UNVERIFIED] — I could not ground, from a checkable external source in this session, the norm that a novelty claim should rest on full texts, so I down-rated it.
**Confidence**: 3 — core expertise in tracking, adjacent for planner-side literature; no external check possible in this review

### W7: The abstract's held-out figures use a different denominator from the room they are quoted against
**Problem**: The abstract says one class-average scale per phase "recovers 90% of the room with true phases and 99.9% with the tracker's own phase estimate" held out. Table S32 gives 0.903 and 0.999 only like for like, against a single scale chosen the same way on the other runs. Against the single-scale frontier of record, which is the frontier that defines the room, the values are 0.868 and 0.964. Section V-C gives both for the true phase (0.90; 0.87) but only 0.999 for the estimated phase. A held-out value of 0.999 above the in-sample 0.984 follows from the denominator. At the lowest caution level 30 of 35 left-out runs have no qualifying training choice, so no point is formed there. The recount's variant at that level gives 0.904 and 1.000.
**Evidence Anchor**: `table: Table S32 — Logged truth: held out like for like 0.903, against single scale of record 0.868; Tracker estimate, threshold −1.0 m/s²: 0.999 and 0.964`
**Why it matters**: The substantive message (most of the room is a cross-phase allocation of caution) survives either denominator. The headline number as printed reads as near-complete recovery of the room, which the record frontier does not support.
**Suggestion**: Quote the against-record value in the abstract and contributions, or state the basis ("relative to a held-out single scale"). Give the 0.964 beside 0.999 in Section V-C.
**Severity**: Minor
**Confidence**: 4 — arithmetic on the cited table; the inference side is for other seats

---

## Coverage Receipt (conditional *)
Not required: both Strengths and Weaknesses are populated.

---

## Detailed Comments *

### Title & Abstract
- The title carries the narrow case in its subtitle ("A Fixed-Noise Kalman Tracker in CARLA Lead Braking"), and the abstract's second sentence and its "This null, expected from the filter's steady state, is untested for track births, missed updates and real sensors" keep the null on the narrow side. The opening "A tracker's covariance can set a planner's safety margin" is true in general; the test is not.
- The abstract's 83% for the braking prediction omits that every lead brakes to a stop (W3). The 90% and 99.9% held-out figures should state their basis (W7).
- The title's "Tracker-Covariance Safety Margins" could be read as covering trackers whose covariance varies; the paper tests none (W1).

### Introduction
- The framing question (does the covariance's variation follow the real prediction error?) is the right one. Stating up front that a fixed-noise null is expected is honest and unusual.
- Contribution 3 is presented as a measured confirmation of the steady state, which is accurate. Contribution 4 is hedged correctly but rests on an exception analysis that is not shown (W4).

### Literature Review / Theoretical Framework
- **Coverage**: Planning-with-uncertainty, planner-centric evaluation, open- versus closed-loop evaluation, IMM, adaptive filtering, RSS and R157 are all covered with correct attributions. The Riccati and steady-state references [38], [39] and the adaptive-filter classics [34]–[37] are the right ones. Check the section locators in [38, Sec. 5.2.5], [38, Sec. 11.2] and [39, Ch. 7] against the editions used.
- **Integration quality**: Thematic and critical. The paragraph on uncertainty passed into prediction and planning is a real synthesis, with the "nearest published analogue" [17] named.
- **Research gap**: Convincing for the question asked, but the narrowness of the gap statement (W6) means the gap is defined partly by the paper's own design choices.
- **Theory**: The steady-state account is correct for a linear time-invariant Kalman filter. CANMOT is an EKF with object-frame noise rotated by an estimated heading. The paper acknowledges this and shows empirically that the heading dependence is negligible in lead braking, stopped-vehicle and cut-in runs. In the evaluated runs the ratio of N to F0 is also affected by two planner-side choices: the covariance is propagated without process noise over the state's age (σ_N 0.400–0.545 at t = 0 is purely age), and F0 is a mean over route-frame covariances of six families. Both are disclosed. Neither changes the near-constancy, because N and F0 share them.
- **Alternative frameworks**: The obvious alternatives are an IMM or CA tracker, a second-moment-calibrated margin conditioned on phase or range (the per-phase scale result is close to this), and conformal or calibrated predictor margins. The paper names them as future work; W1 asks that at least one be run.

### Methodology / Research Design (domain aspects only)
- The planner's constraint form, margin variance z'Pz with z = (n, t_e n), and the 17-row library are described clearly enough to see why the margin is velocity-dominated at look-ahead 2–3 s. That makes the 1.10 ratio a statement about the velocity block.
- The separation between a bias source (the braking prediction shifts the path) and variance sources (everything else scales a variance around a constant-velocity path) is stated and is the right caveat. It also means that the oracle, which sets s to the squared realised error including systematic lag, is a bias-plus-variance positive control for a variance-only source. I read this as a limit on what "room" means for covariance sources, not as an error.

### Results / Findings
- All numbers I traced agree with the supplement tables: 0.0012 and 0.0015 against 460.7 decision-equivalents (0.6 and 0.69), 419.1 + 41.7 (Table S33), the 132 decisions (53 + 43 + 36), 52.2 (6.7 + 18.6 + 26.9), 55.9 (8.3 + 20.8 + 26.8), the 3.40-step grid offset, and the S34b-weighted NIS (about 0.26) against the Fig. S1 median 0.24.
- One figure has no table behind it: "435.2 decision-equivalents with a tracker speed above 2 m/s" (Section V-C) does not appear in S33, S33b, S34 or S34b.

### Discussion
- "Why this covariance carries no measurable decision value here" is correctly bounded: this covariance, steady state, simulated sensing, regular updates. The sentence "It does not justify removing a covariance margin from a deployed stack" is exactly right.
- "What the braking prediction's share shows" is the best paragraph: the 83% is reduced to 0.38 on tuning runs, to 35.5 decisions without the after-stop decisions, and to 50 against a per-phase class average. The data do separate the after-stop first second (lag, which a braking prediction corrects) from the later room. They do not separate lag from braking before the stop. They do not separate filter smoothing from staleness. They do not show the prediction's cost where the lead does not brake. The paper says the first and last of these; the second needs the offline re-run of W2.

### Conclusion
- Conclusions stay inside the evidence except for the abstract-level wording points above.

### References
- Closest relatives [13]–[17] are well chosen. Many are 2024–2026 arXiv preprints, including the tracker [8] (accepted to IROS 2026). Configuration is "as in [9]", an unpublished manuscript under review; Table S28 repeats the values, which mitigates this.

### Missing Key References
All marked [to verify]; I am confident the works exist but have not checked exact bibliographic details.
- R. Schubert, E. Richter and G. Wanielik, "Comparison and evaluation of advanced motion models for vehicle tracking," Int. Conf. Information Fusion, 2008 [to verify]. Compares CV, CA, CTRV-type models on vehicle tracking; bears on the lag question.
- E. Mazor, A. Averbuch, Y. Bar-Shalom and J. Dayan, "Interacting multiple model methods in target tracking: a survey," IEEE Trans. Aerosp. Electron. Syst., 1998 [to verify]. Fits the IMM sentence in Section II.
- X. R. Li and Z. Zhao, "Evaluation of estimation algorithms part I: incomprehensive measures of performance," IEEE Trans. Aerosp. Electron. Syst., 2006 [to verify]. Estimator-credibility measures beyond NIS/NEES.
- M. Treiber, A. Kesting and D. Helbing, "Delays, inaccuracies and anticipation in microscopic traffic models," Physica A, 2006 [to verify]. Estimation error and anticipation in car following; relevant to the finding that anticipating the lead's braking recovers room.
- G. Naus et al., "String-stable CACC design and experimental validation: a frequency-domain approach," IEEE Trans. Veh. Technol., 2010 [to verify]. Use of the lead's acceleration in following control.
- L. Lindemann et al., "Safe planning in dynamic environments using conformal prediction," IEEE Robot. Autom. Lett., 2023 [to verify]. Calibrated predictor uncertainty carried into planning.
- J. Hardy and M. Campbell, "Contingency planning over probabilistic obstacle predictions for autonomous road vehicles," IEEE Trans. Robot., 2013 [to verify]. Obstacle-prediction uncertainty in planning.

~~~yaml suggested-references
- title: "Comparison and evaluation of advanced motion models for vehicle tracking"
  authors: ["Schubert, R.", "Richter, E.", "Wanielik, G."]
  year: "2008"
  doi: null
  arxiv_id: null
- title: "Interacting multiple model methods in target tracking: a survey"
  authors: ["Mazor, E.", "Averbuch, A.", "Bar-Shalom, Y.", "Dayan, J."]
  year: "1998"
  doi: null
  arxiv_id: null
- title: "Evaluation of estimation algorithms part I: incomprehensive measures of performance"
  authors: ["Li, X. R.", "Zhao, Z."]
  year: "2006"
  doi: null
  arxiv_id: null
- title: "Delays, inaccuracies and anticipation in microscopic traffic models"
  authors: ["Treiber, M.", "Kesting, A.", "Helbing, D."]
  year: "2006"
  doi: null
  arxiv_id: null
- title: "String-stable CACC design and experimental validation: a frequency-domain approach"
  authors: ["Naus, G."]
  year: "2010"
  doi: null
  arxiv_id: null
- title: "Safe planning in dynamic environments using conformal prediction"
  authors: ["Lindemann, L."]
  year: "2023"
  doi: null
  arxiv_id: null
- title: "Contingency planning over probabilistic obstacle predictions for autonomous road vehicles"
  authors: ["Hardy, J.", "Campbell, M."]
  year: "2013"
  doi: null
  arxiv_id: null
~~~

---

## Questions for Authors *

1. If the tracker is re-run offline on the stored detections with noise set so that position NIS is near 2, and again with a CA or IMM variant, how much of the after-stop velocity lag (Table S34), the 41.7 pooled decision-equivalents and the braking prediction's 83% remains?
2. What happens in the evaluation run whose ratio falls to 0.703–1.043 over 96 decisions at track ages of 21.5–31.0 s (S10.7)? Is the estimated heading of the stationary lead drifting? If so, "constant heading" is not strictly true for the 82.7% of decisions after the stop.
3. Why does benign driving, a straight-road family, reach only 60.45% within 5% (Table V)? Is the cause track age, missed updates, actors not ahead, or something else?
4. Within a row, how often would a ±5% change in the margin ratio, or the 1.035-to-1.103 look-ahead tilt, change which row is first feasible? In other words, how close is "within 5%" to a decision-level sufficient condition for the null?
5. For the 132 after-stop decisions with tracker speed above 0.5 m/s, how many runs contribute and how many decisions per run? Are the 52.2 decision-equivalents spread across runs or concentrated?
6. The planner propagates P at constant velocity without process noise and adds its own allowance Q. If a stack propagated with the tracker's own process noise, would N's ratio to F0 stay near 1.10, and would the null stand unchanged?
7. Where does the figure "435.2 decision-equivalents with a tracker speed above 2 m/s" in Section V-C come from?

---

## Minor Issues

### Language / Grammar
- Section V-B heading "An Adaptive Covariance and Simple Predictions" and Table I "Tested": rename the NA row and heading to say "output-scalar NIS inflation" (W1).
- Supplement S4 says "An independent reviewer's own code reproduced 841 values". S11.8 says "independent" means independent of the first program's code only, and that the second programs were Claude sessions. State in S4 whether the "independent reviewer" was a human or an AI panel seat, in plain words, to complete the disclosure of earlier AI-panel reviews.
- "Covariance settles to the steady state of the Riccati recursion": add "of the linearised, time-invariant filter" at first use in Section VI.

### Citation Format
- Check the locators [38, Sec. 5.2.5], [38, Sec. 11.2] and [39, Ch. 7].
- [9] is unpublished and underlies the tracker configuration; Table S28 mitigates, and a pointer in the text would help.
- State the peer-review status of the preprint relatives [4], [8], [14], [17], [19].

### Figures and Tables
- Fig. 2(b): add a second panel of the N/F0 ratio against look-ahead (it rises from about 1.03 to 1.10, Table S14), and mark the 84 outlier rows near 1.68.
- Table V: add columns for the median absolute heading offset and the share of rows from tracks younger than 4 s.
- Tables S33, S33b and S34: add run-level intervals or counts.
- Table S32: print the against-record column in the main text for both phase definitions (W7).

### Layout
- Submission gates (author-only placeholders, not findings): the author block (manuscript line 5); the repository name and DOI in Data and Code Availability; the "[AUTHOR CONFIRMATION: ...]" at the end of the AI-generated-content statement.

---

## Criterion-Bound Judgements *

Calibration status: `NOT_CALIBRATED`

Current seat reports cannot know the final actual panel topology and never self-upgrade from a candidate profile.

| Dimension | Criterion source | Judgement | Evidence anchor(s) | Rationale | Uncertainty / scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| Originality | criteria binding unavailable; general field norms | PARTLY_MEETS | `text: §II "Our contribution is the evaluation, the measured size of the decision consequence, and what the measurement shows about open-loop decision scores."` | The evaluation design (equal caution, oracle control, graded oracles, placebo) is new in this form. The headline null is expected from the steady-state argument, which the paper concedes. | No external novelty check possible in this review; literature search by authors only. | Yes: it limits significance unless a varying-covariance arm is added (W1). |
| Methodological Rigor | criteria binding unavailable; general field norms | NOT_ASSESSED | — | Scoring, bootstrap calibration and planner design belong to Reviewer 1. | I judged only the tracking-side aspects (steady state, NIS/NEES, lag). | No |
| Evidence Sufficiency | criteria binding unavailable; general field norms | PARTLY_MEETS | `table: Table S34b — Lead braking: mean NIS 1.47, mean velocity NEES 5.08; After stop: mean NIS 0.10`; `text: §III-A "the simulated sensor data are a likely reason, which we did not test"` | Evidence for the steady-state null in this regime is strong. Evidence for the lag mechanism and for the "adaptive covariance would need" statement rests on one mis-tuned configuration and decision-time statistics without intervals. | Single tracker, simulated sensor, one family; paper says so. | Yes: W2 |
| Argument Coherence | criteria binding unavailable; general field norms | MEETS | `text: §VI "It does not justify removing a covariance margin from a deployed stack"` | Claims stay on the narrow side. The abstract and heading exceptions are listed (W1, W3, W7). | Judged on the manuscript's own words. | No |
| Writing Quality | criteria binding unavailable; general field norms | NOT_ASSESSED | — | Outside my remit; the dense numerical prose is for the editor and Reviewer 3. | — | No |
| Literature Integration | criteria binding unavailable; general field norms | PARTLY_MEETS | `text: §II "we found no study that tests whether a real multi-object tracker's state covariance improves an automated vehicle planner's decisions"` | Planning-side coverage is good and the abstract-only limit is disclosed. Vehicle-tracking motion-model comparisons, credibility measures and lead-acceleration anticipation are missing, and the novelty claim is a six-part conjunction. | Existence of the suggested works is marked [to verify]; I could not check them. | No (W6 Minor) |
| Significance & Impact | criteria binding unavailable; general field norms | PARTLY_MEETS | `text: §I Scope "We do not test a calibrated covariance, a manoeuvre-adaptive (IMM) tracker, or a covariance that adapts in both directions."` | A rigorous account of one filter in one regime, with a design others could reuse. Practical reach depends on W1 and W2, which can be addressed offline. | Deployment and regulatory significance not assessed. | Yes: W1, W2 |

Unresolved decision-bearing criteria and repairability: Originality/Significance (W1) and Evidence Sufficiency (W2) are both repairable by offline re-tracking of the stored detections; neither requires new simulation. Strengths on Argument Coherence do not offset them.
