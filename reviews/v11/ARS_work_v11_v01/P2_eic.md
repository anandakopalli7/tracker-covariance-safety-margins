contract_role: eic
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: warn
trigger: "The manuscript is reviewable but carries correctable presentation defects, such as redundant or overlong sections"

Basis: the organisation, figures and tables let me locate and check every main claim, and the figures agree with the text; the defects are length against the 10-page recommendation, numerically dense results prose, one undefined symbol, one confusingly built table and one hard-to-parse sentence (W8 to W12).

### D6: venue_fit_and_contribution
score: warn
trigger: "the case for significance to the venue's readers is weaker or less explicit than it should be and needs sharpening"

Basis: the topic is in scope and the contribution is identifiable, well positioned and not overstated; the case that an expected null, measured in a clean simulated test bed, matters to this journal's readers needs sharpening (W1 to W7, with W1 the main item).

## Review Body

Reviewer identity: Associate Editor, IEEE Open Journal of Intelligent Transportation Systems (OJ-ITS), safety evaluation of automated driving and the perception–planning interface. Calibration Status: `NOT_CALIBRATED`. Overall confidence: 4 (journal fit, framing and presentation are within my remit; bootstrap theory and tracker internals are not, and findings that touch them carry lower confidence).

Binding note: this is an unbound call (`criteria_binding_unavailable`). No criteria manifest or target brief was supplied, so this card makes no venue-alignment claim against a criteria registry. Fit judgements rest on the configuration card's description of the venue (regular paper, 250-word abstract, no page limit, 10 pages recommended) and on the journal's public scope statement, checked by a keyword look-up only.

I read the whole manuscript and supplement and viewed Figs. 1 to 4. The manuscript contains no text addressed to reviewers.

### Summary Assessment

The paper asks whether a multi-object tracker's state covariance, used as a planner's safety margin, improves car-following decisions over a class-average margin. It builds an open-loop, decision-level evaluation in CARLA lead braking (35 evaluation runs; CenterPoint and the fixed-noise CANMOT tracker; an in-house 17-row speed planner). Margin sources are compared at equal caution by their wrong-go decisions against the logged future, with an oracle margin as a positive control and graded oracles that test whether the measure registers partial information. The tracker's covariance is a near-constant 1.10 multiple of the class average and recovers no material share of the 5.6-point room. The secondary analyses show that the room itself depends on the commitment assumed (12% left with a 0.75 s reaction and stop) and on the population mix (89% recovered by one scale per phase; the braking prediction's share runs from 29% to 83% with the after-stop segment). The work is careful and candid about its limits; every number in the abstract traces to a section or table, and the abstract is 247 words. My concerns are framing and presentation: the clean simulated test bed rarely exercises the conditions that make an expected null worth measuring; the evaluation design discriminates information only on pooled decisions; the abstract omits fences that the body states; and the main text is longer and denser than the venue recommends. The paper is in scope, and its contribution is narrow but real.

### Criterion-Bound Judgements

| Dimension / criterion | Criterion source | Judgement | Evidence anchors | Rationale | Uncertainty or scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| D6: topic within the venue's scope | Phase 1 plan D6; configuration card; journal's public scope | MEETS | S1 | Car following, adaptive cruise control, the perception–planning interface and simulation-based safety evaluation sit inside ITS as the journal describes it | Unbound call: no registry criteria; public scope only | Yes: a scope failure would be fatal; none found |
| D6: identifiable, positioned contribution | Phase 1 plan D6; card focus (1) | MEETS | S2, S3, W7 | Novelty is stated with its limits and set against the closest relatives | The ITS references were read from abstracts only (W7) | Yes: supports the absence of a fatal or block trigger |
| D6: significance for the venue's readers | Phase 1 plan D6; card focus (1) | PARTLY_MEETS | W1, W2, W6 | An expected null in a clean regime, plus conditional, after-the-fact secondary results; the transferable lesson is real but undersold | Tracker internals are a blind spot of this seat | Yes: sets the warn |
| Abstract traceability, limit and fences | Card focus (2) | PARTLY_MEETS | S4, W3, W4, W5 | All numbers trace; 247 words; three fences missing; one wording departs from the body | none identified | No: wording fixes within 250 words |
| Length against the 10-page recommendation | Card focus (3) | DOES_NOT_MEET | W8 | Estimated 12 to 13 typeset pages | Unverified estimate; no typeset file supplied | No: a recommendation, not a limit |
| Practical reading stated and fenced | Card focus (4) | MEETS | S5, W6 | Conditional reading in §VI and §VII, with explicit "not tested" fences | The ranking lacks the field's usual spacing policy (W6) | No |
| D5: organisation, figures, tables, conventions | Phase 1 plan D5 | PARTLY_MEETS | S6, W8 to W12 | Clear arc and legible figures; overlong and dense; minor notation and table defects | none identified | No: normal priority, repairable |

### S1: In scope for the journal, with ITS framing and vocabulary
**Evidence Anchor**: text: Index Terms, "Adaptive cruise control, autonomous vehicles, car following, collision avoidance"

The problem (does a tracker's uncertainty improve a planner's car-following decisions?) sits at the perception–planning interface of automated driving, and §II connects it to the journal's own literature: threat assessment and collision probability [41]–[44], automatic emergency braking and forward collision warning [45]–[47], criticality metrics and scenario-based assessment [50], [51], spacing policies in adaptive cruise control [52] and UN R157 [38], [39]. The index terms match how ITS readers search.

### S2: Novelty stated with its limits and positioned against the closest work
**Evidence Anchor**: text: §II, "Deglurkar et al. [13], our closest methodological relative, grid the value of a forecaster's uncertainty" and "Our contribution is the evaluation, the measured decision consequence, and what the measurement shows about open-loop decision scores."

The paragraph "Novelty, with its limits" says plainly that the mechanism is not new, dates and scopes the search (Supplement S6), and separates the paper from [13], [15] and [17] by what each does and does not test. An editor can check the novelty claim rather than take it on trust.

### S3: Title and abstract sell the evaluation design, not the null
**Evidence Anchor**: text: title and Abstract, "Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution" and "with an oracle margin, set from each decision's realised error, as a positive control"

The title leads with the evaluation and names the fixed-noise tracker as the case. The abstract runs question, design, positive control, null, conditional findings, and a closing lesson about open-loop scores. This is the right framing for a paper whose headline result is expected; it answers the main concern I set out with.

### S4: Every abstract number traces to the body, within the limit
**Evidence Anchor**: text: Abstract, "the oracle removes 5.6 percentage points of wrong-go decisions when plans are followed for 3 s (calibrated 95% interval 4.4 to 6.7)"

I traced each figure: 35 runs (§III-A); 5.6 points and its calibrated interval (§V-A, Table S16); within 5% of 1.10 in over 99% of rows (§V-A, Table V); 0.1% and −0.2% to 0.2% (§V-A); 89% (§V-C, Table S23); 83% (§V-B, Table II); 29% (§V-C, Table S22, Fig. 3(a)); 12% (§V-D, Table III); the families of the ratio check (§V-E, Table V). All match, and the abstract is 247 words against the limit of 250.

### S5: The practical reading is stated and fenced
**Evidence Anchor**: text: §VI, "The practical reading is conditional." and "It does not justify removing a covariance margin from a deployed stack"

§VI gives practitioners a two-branch reading tied to the commitment, warns against over-applying the null (new tracks, crossing scenarios), names what was not tested (time-gap margins, comfort, following traffic, closed loop), and offers a check needing no ground truth with its reach stated. §VII repeats the conditionality. This is the fencing I wanted to see.

### S6: Clear organisation; figures legible, cited and consistent with the text
**Evidence Anchor**: figure: Figs. 1–4 with Tables II–V, Sections III–V

The paper moves from problem to test bed, scoring, results and discussion without backtracking. Each figure is cited, legible at column width and captioned self-sufficiently, and the values I checked agree with the text: R = 5.56 points and N's mean difference of 0.0068 points in Fig. 2(a); 461, 383, 78 and 50 decisions in Fig. 3(b) against Table S23; 0.12 in Fig. 4(a).

### S7: Limits and analysis history are disclosed where readers will see them
**Evidence Anchor**: text: §VI Limits, "One tracker, one in-house planner and one scenario family were tested."

The Limits paragraph, §IV-D (two analysis plans, additions after the first results, verification status) and §III-A (the earlier exploratory look at the evaluation runs) leave no hidden degree of freedom that I could find. For a negative result this candour is what makes the paper credible to the journal's readers.

### W1: The test bed rarely exercises what makes the expected null worth measuring
**Severity**: Major
**Evidence Anchor**: text: §I, "It still has to be measured: the covariance also depends on detections, misses and track age" and "The evaluated decisions contain almost no newly started tracks (10 of 8,290)"
**Confidence**: 3 — significance and framing are within my remit; tracker internals are a declared blind spot

The Introduction concedes that the null is expected for a fixed-noise Kalman filter. It justifies measuring it anyway because the covariance also depends on detections, misses and track age. The evaluated data barely exercise those dependences. Ten of 8,290 decisions have a young track, all after one re-initialisation in one run. The lidar is simulated with simulator noise off and 0.02 m of added range noise, weather and lighting are at defaults, and there is one lead on a straight road (Table S28). The innovation covariance is too wide (median run-mean NIS 0.24 against 2; §III-A), and 99.26% of binding rows lie within 5% of one constant ratio. Where misses do occur, the ratio departs from the constant (1.68 after two missed updates; Table S27). So the regime in which a fixed-noise covariance could carry decision value is the one this test bed seldom visits.

As written, contribution 3 is mostly a measured confirmation of the steady state that §II attributes to the Riccati recursion. An ITS reader with real sensors, occlusions and dropped detections cannot tell from the paper how often their stack is in that regime. This is the main gap between "a careful study" and "a result this journal's readers can act on".

Remedy (the author's choice):
- Minimum: rewrite the Introduction's justification and contribution 3 to say that the null is measured in the steady-tracking regime under clean simulated sensing, and add to the abstract that track births, misses and real sensing are untested.
- Intermediate, with no new recordings: re-run the tracker offline on the logged detections with detections dropped at a controlled rate, and score the resulting covariance on the same decisions. The result is open loop and off-policy, like every other share in the paper.
- Stronger and costlier: add a degraded-perception condition to the capture pipeline (for example an occluding vehicle, a lower detector rate or adverse weather) and repeat the equal-caution comparison there.

### W2: The evaluation design discriminates information only on pooled decisions, and the framing does not say so
**Severity**: Minor
**Evidence Anchor**: text: §IV-B, "Within the lead-braking phase and with the ego moving, the same mixtures can score below the class average"
**Confidence**: 3 — framing judgement; the measure's statistical behaviour belongs to the methodology seat

The title and contribution 1 offer the evaluation design as the main contribution. The paper's own graded oracles show that the design grades partial information on pooled decisions (0.27, 0.54 and 0.78 for oracle shares of 25%, 50% and 75%). It does not grade them while the lead brakes (−0.68, −0.63 and 0.05) or with the ego moving (−0.11, 0.05 and 0.44; Table II, Table S12b). The pooled population is 82.7% after-stop decisions. The design's discriminating power is therefore demonstrated where the ego is mostly stationary, not where safety-relevant car-following decisions are taken.

The paper turns this into sound guidance (§VI, "What carries over"), but contribution 1 and the abstract present the design without the qualifier.

Remedy: state in contribution 1, and in one clause of the abstract, that the design grades information on pooled decisions only. Optionally, use the per-phase-scale machinery of Table S23 on the stored arrays to report whether the partial oracles grade once each phase has its own scale. If they do, that would give readers a variant that works within phases.

### W3: The abstract does not state the population mix of its own headline numbers
**Severity**: Minor
**Evidence Anchor**: text: Abstract and §III-A, "Open-loop decision scores should state their commitment and population." and "Of the evaluated decisions, 77.5% have the ego at or below 0.5 m/s, and 82.7% come after the lead has stopped."

**Confidence**: 4 — abstract reporting is squarely within my remit

The abstract ends by telling readers that open-loop decision scores should state their commitment and population. It states the commitment of its headline (3 s) but not the population. Most evaluated decisions come after the lead has stopped, with the ego nearly at rest, and §V-C shows that both the room and the braking prediction's share move with that mix (Table S22).

Remedy: add one clause to the sentence that gives the 5.6 points, saying that most evaluated decisions follow the lead's stop.

### W4: Three fences that the body applies are missing from the abstract
**Severity**: Minor
**Evidence Anchor**: text: Abstract, "A class-average margin with one scale per phase of the lead's motion recovers 89% of the room"
**Confidence**: 4 — abstract reporting is squarely within my remit

The abstract leaves out three fences:
- The per-phase scale takes its phase labels from the logged truth, and §V-C says a planner would have to estimate the phase, which was not tested.
- The 89%, 29% and 12% come from analyses added after the first results (§IV-D). The Conclusion says so; the abstract does not.
- The 35 evaluation runs are described as not used to design the margins, which is true. But the room and the tracker covariance's difference had been examined on them in an earlier exploratory analysis, which makes them a transfer rather than a replication (§III-A).

Most readers will rely on the abstract. A practitioner could read the 89% as "use one margin scale per phase" without seeing that the phase was known exactly.

Remedy: add three short qualifiers within the 250 words. Merging the first two sentences and recasting the CARLA sentence (W12) frees roughly the words needed.

### W5: "None that we can measure" departs from the bound the body reports
**Severity**: Minor
**Evidence Anchor**: text: Abstract, "recovers none of the room that we can measure (0.1%; calibrated interval −0.2% to 0.2%)"
**Confidence**: 3 — wording consistency is my remit; interval validity is not

The abstract and the Conclusion say that the tracker's covariance recovers none of the room that can be measured. The body states a bound instead. The calibrated percentile interval contains zero, but the basic interval [0.0012, 0.0035] and every subsampling interval in Table S17 lie above zero. Table S4 also records the plan's rule that this share is never to be printed as not distinguishable from zero. "None that we can measure" reads as that excluded claim.

The practical message does not change (at most 0.6 of 8,290 decisions), but the abstract should use the body's wording.

Remedy: state the bound already in §V-A: at most 0.2% of the room by the calibrated interval, and below 0.5% by every interval method tried. Make the same change in §VII.

### W6: The practical ranking omits the spacing policy ACC practitioners actually use
**Severity**: Minor
**Evidence Anchor**: text: §VI, "a time-gap margin, the usual spacing policy [52], was not among them"
**Confidence**: 4 — car following and ACC are within my editorial specialism

§VI rightly calls its result a ranking among the tested sources. For ACC and car-following readers, though, the first question is how the tracker's covariance and the braking prediction compare with a constant time gap. Without that source, the practical reading cannot be mapped onto the spacing policies these readers deploy.

Remedy: if a time-gap margin can be written as a variance along the constraint normal (for instance growing with the square of the ego's speed times a headway), score it on the stored arrays as one more source at equal caution. Otherwise, say in §VI why it cannot be put on the same footing.

### W7: The ITS positioning rests on references read from their abstracts only
**Severity**: Minor
**Evidence Anchor**: text: §II and Supplement S6, "In this literature we found no evaluation that carries a tracker's covariance through to the warning, braking or planning decision" and "their content is summarised from abstracts only"
**Confidence**: 3 — I know this literature in outline, not each paper's body

The §II paragraph on threat assessment, tracking and safety evaluation anchors the paper in this journal's literature, and its no-prior-evaluation sentence supports the novelty claim. Per Supplement S6, its twelve references [41]–[52] were summarised from abstracts only, and publisher full texts were not searched. Comparisons of the kind the sentence rules out, where they exist, are usually reported in a paper's body rather than its abstract.

Remedy: read the full texts of at least [41]–[47], then either confirm the sentence or position the paper against what they show, and record the full-text check in S6.

### W8: The main text is likely 12 to 13 typeset pages against a 10-page recommendation
**Severity**: Minor
**Evidence Anchor**: absence: whole manuscript — expected a length near the 10-page recommendation, or material moved to the supplement; checked the main-text word count (about 10,800 words, 7,561 of them body text), Tables I–V, the notation table, Figs. 1–4 and the 55 references
**Confidence**: 3 — the page count is an unverified estimate; no typeset file was supplied

The estimate assumes about 7.5 pages of body text, 1.2 pages of figures (four of double-column width), 1.3 pages of tables, 1.8 pages of references and the front matter. The venue sets no limit, but the main text already relies on about twenty supplementary tables. It can lose detail without losing claims.

Candidates to move or compress:
- §IV-B, the "Intervals" paragraph: keep one sentence and move the double-bootstrap detail to S10.1.
- §IV-C, third paragraph: move the discussion of the resolution-rule thresholds (5 and 20) to S8.1.
- §IV-D: reduce to two sentences pointing to S4.
- §V-A, second paragraph: keep the point, the calibrated interval and the 0.5% bound; move the comparison of interval methods and the leave-one-out range to S10.1.
- §V-D, "A 2 m standstill gap": keep one sentence and move the rest to S10.5.
- §V-E, last paragraph (the Spearman consistency check): keep one sentence, since S9 already holds it.
- Table IV: merge it into Table III, which already carries den₀ and RR₀(N), or move it.
- §II, "Adaptive covariances in tracking": shorten.

Together these should come close to the recommendation (estimate).

### W9: Results prose is dense enough to bury the findings
**Severity**: Minor
**Evidence Anchor**: text: §V-B, "With the ego moving the prediction recovers 0.47 [0.35, 0.57], and while the lead brakes 0.61 [0.47, 0.71]"
**Confidence**: 4 — readability for the journal's readership is within my remit

The second paragraph of §V-B carries eight bracketed intervals and about a dozen further numbers in five sentences, and §V-B, §V-C and §V-D read similarly. ITS readers will look for the finding first and the numbers second.

Remedy: open each results subsection with a one-sentence finding in words. Keep in the text only the numbers that the abstract, §VI and §VII use, and move the rest into Tables II–IV or the supplement.

### W10: The symbol D is used in the notation table but never defined in the main text
**Severity**: Minor
**Evidence Anchor**: text: notation table, "A frontier difference in decisions, $D/201/100 \times n$, with $n$ the population's decisions"
**Confidence**: 5 — checked by searching the main text

D (the summed frontier difference over the 201 caution levels) is defined only in Supplement S8.1. The main text uses it only in this formula.

Remedy: define D in §IV-B next to R and RR, or give the conversion in words.

### W11: Table II carries signed caution both as a column and as a row
**Severity**: Minor
**Evidence Anchor**: table: Table II, the column "All, signed caution" and the row "RR(CK3), signed caution"
**Confidence**: 4 — table design is within my remit

The pooled signed-caution values are a column, while the braking prediction's signed-caution values for the other populations form an extra row with dashes in the pooled cells. Readers have to work out which cell answers which question.

Remedy: give signed caution its own small table, or place it consistently as columns for every population (Table S21 already does this).

### W12: A hard-to-parse sentence in the Abstract and the Introduction
**Severity**: Minor
**Evidence Anchor**: text: Abstract, "CARLA runs in which a lead vehicle brakes are perceived by the CenterPoint detector and CANMOT, a fixed-noise Kalman tracker."
**Confidence**: 5 — language

The sentence reads at first as though "brakes" were a noun, and it says that the runs, rather than the lead, are perceived. It appears in both the Abstract and §I.

Remedy: rewrite it, for example as "In CARLA runs the ego follows a lead vehicle that brakes; the lead is perceived by …". This also frees words for W3 and W4.

### Detailed Comments

#### Journal Fit
The topic is squarely within ITS: car following, ADAS-type margins, the perception–planning interface, and scenario-based safety evaluation in simulation. The writing addresses engineers rather than statisticians, though the results sections drift toward the latter (W9). The reference list includes ITS-venue work (Trans. ITS, ITSC, IV), though some of it was read from abstracts only (W7).

#### Originality
The source of originality is a new evaluation design applied to a question that, per a dated and scoped search, has not been tested: a real tracker's covariance against a class constant at equal caution, with an oracle positive control. The mechanism is known, and the paper says so.

#### Significance
The null is expected, so the paper's value to readers lies in three things:
1. The measured scale of the effect (0.6 of 8,290 decisions).
2. The demonstration that open-loop decision scores move strongly with the commitment and the population mix.
3. A ground-truth-free ratio check that tells a team whether a decision-level test is worth running.

Items 2 and 3 are the transferable lessons. They would carry more weight if the test bed exercised the non-steady-state regime (W1) and if the design were shown to grade information where safety decisions are taken (W2).

#### Structural Coherence
The title, abstract, introduction, results and conclusion are consistent. The research question is answered directly, and the conclusion does not over-promise. Section I defines the four key terms before use, and the notation table maps them to established terms.

#### Title & Abstract
The title is good (S3). The abstract is within the limit and traceable (S4), but it needs three fences (W4), the population mix (W3), a bound in place of "none" (W5) and a clearer CARLA sentence (W12).

#### Conclusion
The Conclusion restates the null with its conditionality, flags that the conditional results come from analyses added after the first results, and lists the next steps. It should carry the W5 wording fix, and one sentence on the steady-state regime (W1).

### Questions for Authors
1. Please provide [9], which is under review elsewhere, to the editor as a confidential file so that overlap can be checked, and confirm that no run, table or figure is shared.
2. How many of the lead track's updates in the 35 evaluation runs were missed detections or coasting steps, and during which phase?
3. Could the tracker be re-run offline on the logged detections with controlled drop-outs, so that the covariance is tested where it departs from the steady state (W1)?
4. Do the partial oracles grade information once each phase has its own margin scale (W2)?
5. Can a time-gap margin be expressed as a variance along the constraint normal and scored on the stored arrays (W6)?

### Submission Gates (not findings)
The author block and the repository name and DOI are author-only placeholders and must be filled before submission; an open placeholder would lead to an administrative return. The AI-use statement in the Acknowledgment names the tool, the period and the sections affected, which appears to meet IEEE's disclosure requirement; the editorial office should confirm it against the policy text in force. The related manuscript [9] is disclosed, with the statement that none of its data, results or figures is used here.

### Desk-Rejection Risk and Preliminary Signal
Desk-rejection risk: low to moderate. The paper is in scope, clearly framed and candid. The risk is an editor reading an expected null in one clean simulated scenario, with an in-house planner, as too narrow, made worse by a long and dense main text and by any placeholder left open.

Preliminary journal-fit signal: major revision. The reframing in W1 and the length cut in W8 change much of the text and should be re-reviewed, but no finding of mine threatens the core result. This is a baseline for the synthesizer, not a decision.
