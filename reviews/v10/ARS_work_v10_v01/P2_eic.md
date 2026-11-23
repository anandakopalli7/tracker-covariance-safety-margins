# Journal-Fit Review Card (Phase 2, paper-visible)

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
trigger: "The manuscript is followable but needs editing before acceptance"

### D6: venue_fit_and_contribution
score: warn
trigger: "makes a genuine but incremental or under-argued contribution"

## Review Body

Reviewer: Senior Associate Editor, IEEE Open Journal of Intelligent Transportation Systems (the requester-stated target), handling automated-driving perception and planning submissions. Calibration status: NOT_CALIBRATED. No criteria manifest was supplied, so I judge venue fit only against the stated constraints (regular paper; abstract at most 250 words; no page limit, 10 pages recommended) and general knowledge of an ITS readership. I read the main text, the full captions, the whole Supplement and all seven figure images.

**Summary.** The manuscript asks whether a multi-object tracker's state covariance, used as a chance-constraint margin in a speed planner, improves decisions over a class-average margin. CARLA lead-braking runs are replayed open-loop through CenterPoint and CANMOT; for each margin source the margin scale is swept and wrong-go decisions are traced against caution (speed given up), with an oracle margin set from each decision's realised error as a positive control. Under a 3 s commitment the oracle has 5.6 points of room; the tracker's covariance recovers essentially none of it because its margin is a near-constant 1.10 multiple of the class average; an innovation-inflated variant recovers 0.7 to 2.5%; an RSS-style 3 m/s² braking prior recovers 83%. Under a reaction-and-stop scoring with UN R157 01-series values the room falls to 12% (53% when plans the 3 s window cannot judge count as unsafe), and within phases too little remains to grade most sources. The work is careful, candid about its limits and internally consistent where I checked. Its weaknesses on my dimensions are framing (the headline is a null the paper itself calls expected), an unstated practical take-away under the realistic commitment, length and density well beyond what an ITS reader will absorb, an abstract that is not self-contained, and submission-readiness placeholders.

**Desk-rejection risk: moderate as the text stands; low once the gating items are fixed.** For acceptance into review: the topic is squarely in scope (car following under lead braking, the perception-planning interface of automated driving, UN R157 performance models), the design is careful and the scoping candid. Against: (1) the unfilled author block, repository statement and AI-use disclosure (W11, W12) would cause an administrative return before any scientific screening; (2) the title, abstract and Section I lead with a null the paper itself calls expected (W1), which is what a screening editor weighs first for significance; (3) the abstract cannot be parsed by a general ITS reader (W4); (4) the main text runs an estimated 20 to 40% over the recommended length, mostly with appendix-grade detail (W3). Items (1) and (4) are mechanical, (2) and (3) are rewriting; none needs new experiments.

**Likely referee outcome.** As a preliminary signal for the synthesizer, not a decision: I expect referees to ask for a major revision. On my dimensions the paper needs substantial restructuring and reframing but no new data; referees focused on methods are likely to add questions about the non-smooth step-frontier statistic and the post hoc intervals, which I do not assess.

**Journal fit.** The question (does tracker uncertainty improve automated car-following decisions) and the regulatory anchoring are ones an OJ-ITS readership recognises, and the work is a transportation-systems contribution rather than a pure estimation or learning one. Fit is weakened by presentation rather than topic: the register is that of a pre-registered statistical report (claim-wording rules, branch numbers, counts of independent programs) rather than an ITS paper, and the reference list draws mainly on robotics, learning and control venues (W5).

**Originality.** The source of originality is a new combination: comparison of margin sources at equal caution, an oracle positive control with graded oracles, and an explicit commitment model, applied to a real detector-tracker pipeline. The closest relative [13] is differentiated in Section II. The covariance diagnostic itself is, by the paper's own account, an expected consequence of the Riccati steady state (W1).

**Significance.** If the conclusions hold, the impact is at sub-field level: evaluators of perception-planning interfaces gain a ground-truth-free screen (Fig. 2(b)) and a quantified reminder that open-loop decision scores depend on the assumed commitment; developers learn that, for a fixed-noise tracker, feeding the covariance into a margin planner buys nothing over a class average. The braking-prior result is the most actionable number but holds under the scoring the paper calls a stress case (W2).

**Structural coherence.** Title, abstract, Section I and Conclusion ask and answer the same question, methods precede results, and the Conclusion answers the research question directly. The mismatch is one of emphasis: the title promises a general answer about Kalman trackers that the Scope paragraph rightly narrows to one fixed-noise tracker, and contribution 3 promises a location of the room that, under the realistic commitment, is mostly not measurable within phases.

**Length and format (estimate).** Counting whitespace-separated words: abstract 249 (at the 250-word limit); Sections I to VII about 9,150 words of prose plus about 1,250 words in the five main tables (I, Notation, II, III, IV); four full-width figures, three of them two-panel; 43 references. I estimate 12 to 14 printed IEEE two-column pages against the recommended 10; this is an estimate from word and display-item counts, not a typeset count. The Supplement adds about 16,800 words, 15 tables and 3 figures, more than the paper itself; acceptable as supplementary material, but it signals that the main text should carry less.

**D5 (warn).** The organisation is sound, core metrics are defined (Section IV and the Notation table), figures are legible with units, and the abstract is within the limit, so the block conditions of my plan (untraceable headline results, undefined core metrics, an abstract far over the limit) do not hold. The length estimate sits near the 30% line of my block trigger, but the excess comes mainly from appendix-grade material rather than pure redundancy and the venue sets no page limit, so I score warn: followable, with substantial editing needed before acceptance.

**D6 (warn).** The work is in scope and has an identifiable contribution beyond the expected steady-state result (the evaluation design and the commitment dependence), so the fatal trigger does not apply. Novelty is differentiated from the closest relative and significance is partly argued in Section VI ("What carries over"), so the block trigger does not apply either. What remains is framing, positioning and an unstated practical take-away, fixable by rewriting the framing, contributions and discussion without new experiments.

### W1: The headline question has an answer the paper itself calls expected
**Severity**: Major
**Evidence Anchor**: text: §I para. 4 "For a fixed-noise Kalman filter the covariance's null is expected"; §II Novelty "our contribution is to measure its decision consequence against an oracle with demonstrated room"
**Confidence**: 4 — editorial judgement of contribution framing, squarely within the handling editor's remit

Section I and the novelty paragraph of Section II state that the covariance's null follows from the steady state of a fixed-noise filter, yet the title poses exactly that question and contribution 2 presents its confirmation as a contribution. A screening editor will read the headline as a known result. What is new to an ITS reader is the evaluation design (equal caution, an oracle positive control, the graded-oracle check of Table S12, an explicit commitment model) and the finding that the open-loop room moves strongly with the commitment; these are under-sold. Fix: retitle around the question actually answered (a decision-level, equal-caution evaluation of tracker-covariance margins, with the fixed-noise tracker in lead braking as the case); reorder the contributions so the method and the commitment dependence come first and the covariance diagnostic third, introduced as a confirmatory test of an expected steady state; and add one sentence in Section I on why measuring an expected null was still needed (the covariance also depends on detections, misses and track age, as Section VI notes). This is rewriting, not new experiments. A stronger, costlier option is to apply the same evaluation to one source whose covariance does vary per decision (the calibrated covariance of [9], or an IMM tracker), which would show the method discriminating on a real tracker rather than only on synthetic graded oracles.

### W2: The practical take-away under the realistic commitment is not stated
**Severity**: Major
**Evidence Anchor**: text: §IV-C "The 3 s commitment scoring is a stress scoring."; §VII "the decision value we could measure lies in anticipating braking under the 3 s commitment, not in the covariance"
**Confidence**: 4 — judgement of significance for an ITS testing and development readership

Section IV-C calls the 3 s scoring a stress scoring and a worst case; Section V-C shows that under the reaction-and-stop scoring with the R157 01-series values about 12% of the room remains and, as scored, too little within any phase to grade any source. The positive result the Conclusion keeps, the braking prior's 83%, therefore comes from the scoring the paper itself regards as least representative, while the more realistic scoring leaves most within-phase shares not evaluable. Section VI says open-loop scores should state their commitment, but it does not tell a developer, tester or type-approval assessor what to do differently, nor which scoring should guide practice. Fix: add a short paragraph on implications for testing and development to Section VI that (a) states which commitment model the author considers representative of the planner's replanning and why, (b) gives the practical reading under each (for example, with a fixed-noise tracker a class-average margin suffices; the value of anticipating braking is established only under the stress scoring), and (c) names the closed-loop test that would settle it; then word the Conclusion's last sentence conditionally in the same terms. A stronger option, needing new runs, is to run the braking prior in the simplified closed loop of Supplement S3, which S3.1 says was not tested.

### W3: The main text is an estimated 20 to 40% over the recommended length, mostly with appendix-grade material
**Severity**: Major
**Evidence Anchor**: table: Table IV (main text; 16 quantity rows across five population columns)
**Confidence**: 4 — page estimate derived from word and display-item counts; typeset length may differ by about a page

By my estimate (not a typeset count) the main text needs 12 to 14 IEEE pages against the recommended 10. The venue sets no hard limit, so this is a reader-burden problem rather than a compliance failure, but for an ITS audience the density hides the findings. The excess is mostly appendix-grade material: Table IV's sixteen rows of RR₀, RR_E, D and decision-equivalents; the signed-caution and stop-deceleration paragraphs of Section V-C; the deviation-ranking check of Section V-D; the stopping-point error paragraph of Section III-A, which serves only the supplementary closed-loop simulator; and inline provenance markers (one code, two programs, recounts, hash prefixes). Repetition adds to it: in the main text, 83% appears six times, "not robust to the convex-hull" six, "costs 2.4 points of caution" four and "0.11 [0.06, 0.18]" four. Fix: (1) replace Table IV with a five-row table (den₀ and the RR₀ of N, NA, CK3 and AM) for the pooled and phase-weighted populations, as scored and under count (ii), and move the rest to Supplement S8; (2) move Section V-D to S9, keeping a two-sentence summary in Section V-A; (3) move the stopping-point paragraph of Section III-A to S2; (4) cut the signed-caution and stop-deceleration paragraphs to one sentence each; (5) replace inline provenance markers with one sentence in Section IV-D pointing to S4; (6) state each headline number once in Results and refer back to it in Discussion and Conclusion; (7) cut contribution 3 to two sentences. These cuts should bring the paper to about 10 to 11 pages without removing any result.

### W4: The abstract is not self-contained for a general ITS reader
**Severity**: Major
**Evidence Anchor**: text: Abstract "not robust to the convex-hull frontier (step frontier: 0.09 percentage points; phase shares −0.6% while the lead brakes, +7.9% after it stops)"; Abstract "With that stop, unless those plans count as unsafe, too little room remains, phase by phase, for the braking prior's share to be measured."
**Confidence**: 5 — abstract conventions and readability for the venue's readership are core editorial competence

The abstract is at the limit (249 words by whitespace count) yet uses step and convex-hull frontiers, phase shares and "those plans" without definition, carries about twenty numerical values, and ends on a sentence about what cannot be measured. A general ITS reader cannot extract the take-away, and the abstract is what the handling editor screens. Fix: rewrite to about 200 to 230 words in plain terms: the question; the method in one sentence (open-loop replay of CARLA lead-braking runs through CenterPoint and CANMOT, sweeping the margin scale and comparing at equal speed given up against a class-average margin and an oracle); three results (oracle room 5.6 points; the covariance's share near zero because its margin is a near-constant multiple of the class average; the braking prior's 83% under a 3 s commitment, with the room falling to 12%, or 53% under the stricter count, under a reaction-and-stop model with R157 values); and one sentence of implication. Drop frontier types, phase shares and the count (ii) clause, or define them in words. If the analysis plan's consequence rules bind the abstract's claims, keep the claims, word them plainly, and record the mapping in Table S4 as was done for earlier abstract edits.

### W5: Positioning against ITS-venue work is thin, and the novelty search skipped the closest literature
**Severity**: Minor
**Evidence Anchor**: text: Supplement S6 "the literature on interacting-multiple-model and adaptive filtering was not searched for a planner-side test"
**Confidence**: 3 — based on the reference list and the stated search scope; without database access I cannot name a specific missed study

For an OJ-ITS readership the closest applied literature is uncertainty-aware forward-collision warning, threat assessment and adaptive cruise control, where tracker covariances, often from IMM or adaptive filters, feed decision thresholds. Section II positions mainly against robotics, learning and control venues: of the 43 references, only [7] and [11] (IEEE IV), [20] (IEEE T-IV) and [40] (Accid. Anal. Prev.) come from ITS or transport venues, besides the regulations [38] and [39], and none from T-ITS, ITSC or this journal. Supplement S6 states that the IMM and adaptive-filtering literature was not searched for a planner-side test, which is where a prior test of covariance-driven decisions would most likely sit. The novelty claim is not shown wrong, but it is under-supported for this audience. Fix: extend the search to ITS venues and to IMM and adaptive-filter trackers in ACC and collision-warning studies; add a Section II paragraph positioning against that work; narrow the novelty sentence if a planner-side test turns up.

### W6: Overlap with the author's related manuscript and reliance on unrefereed preprints need managing
**Severity**: Minor
**Evidence Anchor**: text: §I Scope "A related manuscript by the author [9], under review, asks how to size a margin from a tracker's covariance"
**Confidence**: 4 — standard editorial handling of related submissions and preprint citations

The related manuscript [9], under review at IEEE Access, shares the detector architecture, the tracker configuration and the margin form; Section I discloses this and states that no data, result or figure of [9] is used. The editor will still need [9] to judge overlap. Positioning also rests partly on 2026 preprints: the tracker itself [8] (arXiv, noted as accepted to IROS 2026) and [14], [17] and [19]. Fix: upload [9] as a confidential related manuscript and state in the cover letter what is shared and what is new; cite the IROS proceedings version of [8] if it is available; check [14], [17] and [19] for published versions; make sure no positioning sentence rests on a preprint alone.

### W7: Paper-specific terms are used before definition, and names drift
**Severity**: Minor
**Evidence Anchor**: text: §I contribution 3 "Against a perfect oracle for that scoring, the phase-weighted avoidable wrong-go is 6% of the pooled amount"; §V-C "the inflated covariance 0.012"
**Confidence**: 4 — read directly from the text

Section I and the contribution list use room, caution, commitment, phase-weighted, avoidable wrong-go and "a perfect oracle" before Section IV defines them, and the Notation table arrives only after Section IV-C. Names drift for one object: the NA arm is the NIS-inflated covariance, an innovation-inflated variant or the inflated covariance; CK3 is the braking prior, a braking prediction or a constant-deceleration braking prediction; F0 is the class average, the class-average covariance or the class-average margin. Fix: give one-sentence plain definitions of room, caution and the two commitment models in Section I; move the Notation table to the start of Section IV and add the arm codes to it; after Section III-C use one name per arm consistently in text, tables and figures.

### W8: The symbols R and RR(N) mean different things in Table III and Fig. 4(b) than in the Notation table
**Severity**: Minor
**Evidence Anchor**: table: Table III, header columns R (pp) and RR(N), read against the Notation table rows for R and RR_E(A)
**Confidence**: 4 — read directly from the tables and captions

The Notation table defines R as the oracle's room under the 3 s commitment and RR_E(A) as a source's share of the 3 s oracle's advantage under another scoring. Table III (and Table S6) nevertheless heads that advantage under the reaction-and-stop scoring R, its caption calling it "the 3 s oracle's advantage", and heads the share RR(N); Fig. 4(b) labels its axis RR(N); Table IV calls the same share RR_E(N). Fix: relabel Table III, Table S6 and Fig. 4(b) with RR_E(N) and a distinct symbol for the 3 s oracle's advantage under the reaction-and-stop scoring, and use the same symbols in Section V-C.

### W9: The check that governs how every phase share is read sits only in the Supplement
**Severity**: Minor
**Evidence Anchor**: table: Table S12 (graded oracles), cited from Sections IV-B, V-B, V-C and VI
**Confidence**: 4 — structural judgement from the cross-references

Sections IV-B, V-B, V-C and VI interpret the phase and ego-moving shares through the graded oracles of Table S12 (whether the measure grades partial information in that population), and Section VI offers that check as one of two transferable contributions, yet the table is only in the Supplement while Table IV's secondary rows are in the main text. Fix: bring a compact version of Table S12 (partial oracles at p = 0.25, 0.5 and 0.75 for all decisions, ego moving, lead braking and phase-weighted, 3 s scoring) into Section IV-B, or as a small panel beside Fig. 3, and move the Table IV rows it displaces to the Supplement.

### W10: The main text narrates the project's history and refers to earlier reviews
**Severity**: Minor
**Evidence Anchor**: text: §IV-C "Two further checks follow review requests"; §V-C "the weakest of the three statistics that the plan fixed for the abstract"
**Confidence**: 4 — editorial convention

Section IV-C says two checks follow review requests, Section IV-D says analyses were added after the first results and two reviews had been read, Section V-C refers to statistics that the plan fixed for the abstract, and the Acknowledgment cites the template of a review. An editor cannot tell whether these reviews were a previous journal's referees, which would normally be declared, or internal reviews. Fix: describe post hoc analyses neutrally (added after the primary results were known; descriptive), drop references to reviews and to rules governing the abstract, keep the audit trail in Supplement S4, and, if the work was reviewed at another venue, say so in the cover letter.

### W11: The author block and the repository statement are unfilled placeholders
**Severity**: Minor
**Evidence Anchor**: text: Author block "[AUTHOR BLOCK: filled by the author]"; Data and Code Availability "[repository and DOI to be added by the author]"
**Confidence**: 5 — direct observation; submission-readiness is core editorial competence

Submitted as is, the manuscript would be returned administratively before review. Section IV-D also states that the plan, its SHA-256 and every amendment are released with the code, and much of the paper's credibility rests on that pre-specification; until the repository is given, the claim cannot be checked. Fix: complete the author block; give the repository URL and an archived DOI containing the plan, the hashes and amendments, the code, and the per-decision arrays needed to recompute Tables II to IV. I rate it Minor only because the fix is a link; if the repository is not public at submission, referees will treat the unverifiable pre-specification as a major issue.

### W12: The AI-use disclosure is an unapproved draft
**Severity**: Minor
**Evidence Anchor**: text: Acknowledgment "AI-generated content (IEEE policy): Claude [model and version] drafted the text of the Abstract, Sections I–VII and the Supplementary Material"
**Confidence**: 5 — direct observation of bracketed placeholders and an approval note

The Acknowledgment carries a note asking the author to approve a proposed disclosure, with bracketed placeholders for the model and version and for whether the code and the literature summaries were checked. IEEE asks authors to disclose AI-generated content in the acknowledgments, so the disclosure must be final at submission. Fix: delete the approval note; name the tool and version; state the sections with AI-generated text and the extent of AI involvement in code and literature summaries; state what the author verified; and reconcile it with the first Acknowledgment paragraph.

### W13: Captions are split across two files, and Fig. 2(b) leaves its outlying rows unexplained
**Severity**: Minor
**Evidence Anchor**: figure: Fig. 2(b) and its two captions (main text and supplementary full caption)
**Confidence**: 4 — figure image and both captions viewed

Each main figure and table has a short caption in the paper and a longer full caption in a supplementary captions file; in the typeset paper only the in-paper caption travels with the figure. Fig. 2(b) shows rows well outside the 5% band, including a small separate group near a ratio of 1.7 and a spread below 1.0, which neither caption explains. Fix: give each figure and table one self-contained caption in the paper (data, number of decisions, interval type, frontier) and drop the supplementary duplicate; add a sentence on what the outlying rows in Fig. 2(b) are (for example, re-initialised or secondary tracks), or state that they are among the 1,127 rows outside the band.

### W14: Number formats and precision are inconsistent
**Severity**: Minor
**Evidence Anchor**: table: Table II, row RR(N)
**Confidence**: 4 — read directly from the text and tables

Shares appear as percentages in the Abstract and Section I (0.7 to 2.5%, 83%) and as decimals with three to six significant figures in the body and tables (0.0167 [0.00729, 0.0252]; −0.000131 [−0.00577, 0.00159] in Table II), and the braking prior's share is printed as 0.8315, 0.831 and 83%. Fix: one convention, for example percentages with two significant figures in prose and decimals with three significant figures in tables, with intervals rounded to the precision the bootstrap supports.

### W15: The abstract's held-out framing omits the earlier exploratory look at the evaluation runs
**Severity**: Minor
**Evidence Anchor**: text: Abstract "On 35 runs not used to design the margins"; §III-A "for them the evaluation runs are a transfer to runs recorded with another planner setting, not a replication"
**Confidence**: 3 — disclosure reading; the methodology seat is better placed to weigh it

The abstract's phrase is accurate for the margin sources, but Sections III-A and IV-D disclose that the room and the tracker covariance's difference from the class average had been examined on these runs in an earlier exploratory analysis, so for the primary statistic the evaluation is a transfer rather than a held-out replication. A reader of the abstract alone would infer a clean held-out test. Fix: add a short qualifier in the abstract (for example, that the runs were examined earlier in an exploratory analysis, or that they were recorded with a different planner setting).

### W16: The abstract presents a post hoc interval limit as a bound
**Severity**: Minor
**Evidence Anchor**: text: Abstract "recovers at most about 0.4% of it"; §V-A "an interval chosen after the results because the percentile interval excludes the point; its coverage is not verified for this non-smooth statistic"
**Confidence**: 3 — bootstrap details are outside my competence; the point concerns only abstract wording

Section V-A explains that "at most about 0.4%" is the upper limit of a basic bootstrap interval chosen after the results, with unverified coverage for a non-smooth statistic. Fix: give the point and the basis in the abstract, for example "about 0.1% (upper limit about 0.4% by a post hoc bootstrap interval)", or use "near zero", as the abstract already does for the other scorings. The choice of interval itself is for the methodology seat.

### W17: The Index Terms miss the ITS vocabulary readers search with
**Severity**: Minor
**Evidence Anchor**: text: Index Terms "Autonomous vehicles, collision avoidance, Kalman filters, motion planning, object tracking, uncertainty"
**Confidence**: 4 — discoverability convention for the venue

None of the terms names car following, adaptive cruise control, safety evaluation or simulation-based testing, which is how this journal's readers would search for the work. Fix: add two or three such terms from the IEEE taxonomy.

### S1: Decisions are scored at equal caution with a working positive control
**Evidence Anchor**: text: §I para. 2 "a positive control showing that better per-decision information could help on the same decisions at all"

The evaluation asks the right question for a perception-planning interface: decisions are scored against the realised future at equal caution, and an oracle margin shows on the same decisions that per-decision information could help at all, so the pooled null is not a blunt-measure artefact (Section IV-B; the graded oracles of Table S12 confirm the measure grades partial information pooled).

### S2: Reporting changes after the results are listed in full
**Evidence Anchor**: table: Table S4 (reporting added or changed after the results)

Table S4 sets every reporting change beside the wording fixed beforehand, Section IV-D separates planned from added analyses, and the Limits paragraph names the weak points (transfer not replication, simulated sensor data, one tracker, planner and scenario family). This degree of candour is uncommon and eases the referees' task.

### S3: A cheap, ground-truth-free screen that carries over to other trackers
**Evidence Anchor**: text: §VI "needs no ground truth: where it is nearly constant, the covariance can change few decisions once the margin's scale is tuned"

The ratio of the tracker's margin to a class-average margin on the planner's binding rows can be run by any team before investing in passing covariances to a planner; it is the most portable idea in the paper and suits an ITS practitioner audience.

### S4: The commitment models are anchored in regulation
**Evidence Anchor**: text: §IV-C "In performance model 2 of the 01 series of UN R157, 0.75 s and 6 m/s² are the reaction time and the maximum deceleration"

Using the R157 01-series performance-model values for the reaction-and-stop scoring, and framing the braking prior as RSS-style, makes the commitment analysis legible to ITS and type-approval readers.

### S5: One figure carries the methodological message
**Evidence Anchor**: figure: Fig. 4(a)

Fig. 4(a) shows in one panel how strongly the open-loop room depends on the commitment and on how unjudgeable plans are counted; it is the clearest carrier of the paper's message to open-loop evaluators.

### S6: Figures are clean and honest about awkward points
**Evidence Anchor**: figure: Fig. 3, panels (a) and (b)

Colours are consistent per arm across figures, axes are labelled with units, panel (b) zooms on the near-zero shares, and the point that lies above its own percentile interval is annotated rather than hidden.

### S7: Derived numbers reconcile across sections
**Evidence Anchor**: text: §IV-B "it is 2.6 times the decision-weighted mean of the three phase rooms (2.13 points)"

Quantities I spot-checked agree: the pooled room of 5.56 points is 2.6 times the decision-weighted phase rooms; the braking prior's 0.8315 of the room corresponds to about 383 of 8,290 decisions; its phase gains of 71 and 56 decisions sum to the "about 127" of Section VI; and the phase counts 678, 755 and 6,857 sum to 8,290.

### S8: Claims are scoped to the evidence
**Evidence Anchor**: text: §I Scope "Every conclusion concerns car following under lead braking and this tracker"

The Scope paragraph limits every conclusion to this tracker, this planner and lead braking, and Section VI repeats that the claim concerns this covariance, not uncertainty in planning generally.

### Questions for the author
1. Is the repository (plan, hashes, amendments, code, per-decision arrays) public now, and can referees access it during review?
2. Do the review requests and the two reviews mentioned in Sections IV-C and IV-D refer to a previous submission of this work to another venue?
3. Which commitment model do you regard as representative of the planner's real replanning behaviour, and why?
4. Beyond the shared configuration stated in Section I, is there any overlap in runs, code or text with [9]?
