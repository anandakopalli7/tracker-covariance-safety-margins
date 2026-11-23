# Peer Review Report

## Manuscript Information
- **Title**: Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution: A Fixed-Noise Kalman Tracker in CARLA Lead Braking
- **Manuscript ID**: not assigned (draft v12, unpublished)
- **Review Date**: 2026-11-19
- **Review Round**: Phase 1 seat report, fresh submission (full mode)
- **Target**: IEEE Open Journal of Intelligent Transportation Systems, regular paper; abstract limit 250 words; no page limit, 10 pages recommended. No journal criteria brief was supplied; fit is judged against these parameters and general field norms.

---

## Reviewer Information

### Reviewer Role
Journal-Fit Reviewer (EIC seat)

### Reviewer Identity
Senior associate editor for IEEE Open Journal of Intelligent Transportation Systems (regular papers), with editorial experience in automated-vehicle perception, planning and safety evaluation. Judges novelty, significance, fit with the readership, and clarity and length. Does not review methodology in depth. No final-decision authority.

### Review Focus
(1) Novelty and significance of the four stated contributions and whether the disclosed search limits carry the novelty claim. (2) Consistency of abstract, introduction and conclusion, the 250-word limit, and tracing of every headline number to a main-text table. (3) Clarity and length against the 10-page recommendation. (4) Handling of the disclosed revision history and the AI-assistance statement.

---

## Overall Assessment

### Recommendation
**Major Revision** (seat signal only; the synthesiser decides).

### Confidence Score
**4** — core expertise: editorial fit, novelty and clarity for this venue. Statistical interval methods, filter theory and regulation details are outside this seat and are not judged here.

### Calibration Status
`NOT_CALIBRATED`

### Summary Assessment
The paper asks whether a fixed-noise Kalman tracker's covariance gives a planner a better safety margin than a class-average margin, scored decision by decision against the logged future at equal caution, with an oracle margin as positive control. It reports that the covariance is a near-constant 1.10 multiple of the class average, so it adds nothing beyond a grid offset; that the oracle's "room" is 5.6 points under a 3 s commitment and about 12% of that under a prompt perfect stop; and, in analyses added after earlier AI-panel reviews, that most of the room is an allocation of caution between lead phases.

The evaluation design is careful and unusually candid about its limits, and the commitment-dependence message is useful to this readership. But the headline result is a null the authors say theory predicts, the magnitudes are conditional on a recording planner and a population that is 82.7% stationary, and the most actionable findings are exploratory and open loop. The reader does not get one clear take-away, the abstract and introduction lead with numbers that no main-text table carries, and 12,451 main-text words plus 34,240 supplement words are far beyond the 10-page recommendation. The fit is credible; the contribution as packaged is closer to a method note on an expected null than a regular paper. A shorter, re-centred paper could be suitable.

---

## Strengths

### S1: A positive control built into the question
The evaluation shows that a null can be told apart from a blunt measure: an oracle margin and graded (partial) oracles are scored on the same decisions, and the paper states where the measure does and does not grade information.
**Evidence Anchor**: `text: §I, para. 3 "a positive control showing that better per-decision information could help on the same decisions at all"`

### S2: Unusual candour about scope, exploratory status and search limits
Scope fences, post-hoc status of added analyses, the abstract-only literature reading, and the non-independence of the second programs are all stated, not buried.
**Evidence Anchor**: `text: §II, "Threat assessment" para. "we did not read the full texts"; §IV-D "All added analyses ... are exploratory and descriptive"`

### S3: A ground-truth-free diagnostic with stated reach
The margin-ratio check (tracker margin over class-average margin on binding constraints) is cheap, reusable by other groups, and the paper says where it is silent (crossing and benign runs).
**Evidence Anchor**: `table: Table V — lead braking 99.26% of 152,264 rows within 5% of median 1.103; pedestrian crossing 8.51%`

### S4: A transferable lesson on open-loop decision scores
That the measured room depends on commitment (0.019 to 0.732 of the 3 s value across τ), on population mix and on the recording policy is a point the intelligent-vehicle evaluation community can use beyond this tracker.
**Evidence Anchor**: `table: Table III — relative room 0.019, 0.122, 0.241, 0.384, 0.537, 0.732 for τ = 0.5 to 1.8 s`

### S5: Traceable provenance and legible figures
Plans are hash-locked, deviations are tabulated beside the wording they replaced, and Figs. 2 to 4 are readable and match the tables I checked (R = 5.56, 461 and 383 decisions, 0.12 at τ = 0.75 s).
**Evidence Anchor**: `figure: Fig. 3(b) and Fig. 4(a) — 461, 383, 78, 50 decisions and 0.12 at τ = 0.75 s agree with Tables S23 and III`

---

## Weaknesses

### W1: The core result is an expected null; the scope fences leave no single take-away beyond a method note
**Problem**: The paper's confirmatory question is answered "no" by a mechanism the authors say is textbook. The positive content is exploratory (phase scheduling, after-stop lag, the 83% braking-prediction share) and open loop only. After the paper's own fences (one tracker, one manoeuvre, straight road, simulated sensors, steady state, one in-house planner, no track births or misses), a reader of this journal cannot say what to do differently. The abstract and Section VI offer several conditional readings (if committed for seconds, one conclusion; if a prompt stop exists, another) rather than one.
**Evidence Anchor**: `text: §I "so a null is expected; we measure it at decision level and size it"; §II "The mechanism is not new: a nearly constant covariance follows from the Riccati recursion"`
**Why it matters**: Regular-paper significance for this journal rests on a usable finding. A measured-and-expected null on one fixed-noise filter in one scenario is narrow, and the contributions that would interest the readership (an evaluation protocol; commitment dependence; phase-scheduled margins) are either methodological housekeeping or unvalidated closed loop. The closed-loop check in Supplement S3 runs no covariance margin, so no arm tests the actionable claims.
**Suggestion**: Decide the one take-away and lead with it (for example, "open-loop decision scores need a stated commitment and population; a fixed-noise tracker's covariance adds nothing in steady following"). Either re-scope to a short paper on that, or add a case where the covariance does vary (the crossing or track-birth families the ratio check already flags) so the study is not a null by construction. Do not promote the exploratory phase-scheduling result to a co-equal claim without closed-loop evidence.
**Severity**: Major
**Confidence**: 4 — core expertise: significance and fit for this venue

### W2: Headline magnitudes are conditional on the recording planner and a stationary-dominated population, by the paper's own account
**Problem**: The abstract and Section VII lead with 5.6 points, 83% and 12%. The paper states that 82.7% of decisions come after the lead has stopped, that only 755 of 8,290 decisions are while the lead brakes, that 91% of the room lies before the stop in a population dominated by the first second after it, and that on the tuning runs the room is 1.18 points against 5.56. It then limits transfer to comparisons between sources.
**Evidence Anchor**: `text: §I Scope "so pooled figures are dominated by stationary decisions"; §VI Limits "only comparisons between sources on the same decisions are meant to transfer"`
**Why it matters**: A reader of the abstract takes away three magnitudes that the authors say should not be carried over. The title says "Lead Braking", yet most of the evaluated decisions are of a stopped lead.
**Suggestion**: Report per-phase results as the primary table, put the pooled figures second, and state in the abstract that magnitudes depend on the recording policy. Consider retitling around the tested object (the covariance) and the decision-score lesson, not the manoeuvre.
**Severity**: Major
**Confidence**: 4 — core expertise: significance and generalisability

### W3: Length and supplement dependence: the argument cannot be followed from the main text
**Problem**: The main text is 12,451 words (8,926 without tables, captions and references) and the supplement 34,240 words, 2.7 times the paper. The main text cites about 40 distinct supplement items (50 table citations), and the claims in contributions 2 and 3 are resolved only in Tables S23, S30 to S32 and S36. Several main-text paragraphs are lists of numbers with table pointers (Section V-A third paragraph, V-C, V-D). The supplement also holds material that does not bear on the question: Section S3 states that it "runs no covariance margin and does not test the question".
**Evidence Anchor**: `dataset: PACKAGE_MANIFEST_v12.txt — whole manuscript 12451 words; abstract 248; body without tables, captions and references 8926; supplement 34240 words`
**Why it matters**: The 10-page recommendation is probably exceeded by a wide margin (my estimate, not a typeset count: 15 to 18 two-column pages). A reviewer or reader must open about 40 supplement items to verify the abstract. That weakens the claim that the paper's argument is self-contained.
**Suggestion**: Move to the supplement: Section II's threat-assessment and adaptive-covariance paragraphs (cut by about half); Section IV-B interval details and IV-C resolution rule; IV-D hash strings; the 2 m gap paragraph; most of Section V-D's decimal-equivalents; half of Limits. Remove Supplement S3 and S9 from this paper unless used. Keep in the main text: Table I, one results table by phase, Table V, Fig. 2, Fig. 4. Target the 10 pages, with the supplement limited to what the main text needs.
**Severity**: Major
**Confidence**: 4 — core expertise: clarity and length for journal submissions

### W4: Abstract, introduction and conclusion carry headline numbers that no main-text table carries
**Problem**: I traced every number in the Abstract, §I and §VII. None contradicts a source. But the following are carried by main-text prose and supplement tables only, not by Tables II to V: the 83% post-stop share of decisions (Table S5); the "calibrated 95% interval 4.4–6.7" (Table II prints nominal [4.50, 6.60]; calibrated is in Table S16); the 2.2-decision bound (Table S31c); the 90% held-out and 99.9% phase-estimate shares and the 89% in-sample share (Tables S23, S32); and the 12% at other stop decelerations, 0.29 and 0.18 at 4 and 5 m/s², which Table III omits (Table S19). Contribution 2 is one of four contributions and its numbers come from analyses the paper calls exploratory and added after the first results.
**Evidence Anchor**: `absence: Tables II–V — expected the held-out per-phase shares (0.90 and 0.999), the 2.2-decision bound and the calibrated room interval that the Abstract states; checked Tables I–V, Fig. 3 caption and §V-A and §V-C text`
**Why it matters**: A claim in the abstract that a reader can verify only in the supplement, and that the paper calls exploratory and added after seeing results, has the same visual weight as the confirmatory result. The 99.9% figure exceeds the truth-phase result because the estimate mislabels 128 decisions (Table S32 note, §V-C), which is not a performance figure a reader should take at face value.
**Suggestion**: Add one main-text table for the exploratory per-phase and held-out results, or remove those numbers from the abstract. If kept, label them exploratory in the abstract and give the 12% with its range (6 to 29% across 4 to 7.6 m/s²).
**Severity**: Major
**Confidence**: 4 — core expertise: claim-to-evidence tracing in abstracts; statistical validity is another seat's remit

### W5: The novelty claim rests on a search whose ITS-literature arm was abstract-only
**Problem**: The novelty statement is correctly hedged ("we found no study"). But the intelligent-transportation arm, the part most relevant to this journal (collision probability from track uncertainty, IMM tracking for adaptive cruise control and warning, lidar trackers with data-set covariances), was read from abstracts only, in English, from one web engine with 59 queries. Supplement S6 does not list the queries. The paper's own closest relatives ([13] Deglurkar et al., [17] Shah et al.) are preprints.
**Evidence Anchor**: `text: §II "Threat assessment" para. "In the abstracts of this literature that we read (we did not read the full texts), we found no evaluation"`
**Why it matters**: Contribution 1 and the novelty sentence carry the case for a regular paper. A journal editor cannot judge an absence claim without the query list and the full-text reading of the ITS items.
**Suggestion**: Read the full texts of the roughly twelve ITS items, list the queries and engines in S6, and weaken contribution 1 to the evaluation-design claim, which is the part that survives a miss.
**Severity**: Minor
**Confidence**: 3 — adjacent field: I cannot independently confirm absence of prior work

### W6: The abstract is a dense single paragraph for an interdisciplinary readership
**Problem**: The abstract is 248 words (I counted it; the manifest also gives 248, within the 250 limit) but holds 18 numerals and undefined internal terms (wrong goes, room, placebo on the scale grid, one scale per lead phase, a perfect emergency stop 0.75 s after each decision). The title also uses "at Equal Caution", a coined measure.
**Evidence Anchor**: `text: Abstract "does no better than a placebo that only shifts the class-average margin on the scale grid"`
**Why it matters**: The abstract must stand alone for readers of an open-access transportation journal; as written, it needs the notation table.
**Suggestion**: Keep three results with plain words, put "room" and "wrong go" in one defining sentence, and move the held-out and bound numbers out.
**Severity**: Minor
**Confidence**: 4 — core expertise: abstract craft for this venue

### W7: Notation and qualification load hinders reading
**Problem**: Nine defined terms in the notation table, eight source codes in Table I (F0, N, NA, E, CK3, AM, Q, TG) plus O, den₀, RR, RR₀, D, and the "count (i) and (ii)" and "branch" labels in the supplement. Hedges recur: "exploratory" eight times, "does not grade" seven times, "we did not" five times, "not evaluable" four times in the main text. Each is justified, but together they bury the claim, and the same caveat is restated in Scope, Section IV, V, VI and VII.
**Evidence Anchor**: `table: Notation table (§IV) and Table I — nine defined terms and eight source codes before the first result`
**Why it matters**: A reader must hold roughly 25 labels in mind; the hedging reduces the signal that the one tested hypothesis (the covariance adds nothing) is what the paper is about.
**Suggestion**: Use the established terms in the body (collision under assumed manoeuvre, conservatism) and keep the coined codes in the supplement; state each fence once in Scope and once in Limits.
**Severity**: Minor
**Confidence**: 4 — core expertise: readability for this journal

### W8: Interval types differ between abstract, text and Table II; a point sits on its interval's edge
**Problem**: The abstract and §V-A give the calibrated interval for the room [4.43, 6.68], while Table II prints the nominal interval [4.50, 6.60] for the same quantity. In Table II, RR(N) = 0.0012 sits at the upper end of its printed interval [−0.0011, 0.0012]. The caption says nominal intervals are not valid for this statistic, but the table of record still prints them.
**Evidence Anchor**: `table: Table II, column "All", rows Room R and RR(N) — 5.56 [4.50, 6.60] and 0.0012 [−0.0011, 0.0012]`
**Why it matters**: A reader checking the abstract against the main table sees two intervals for the same number, and a headline cell that looks like a printing error.
**Suggestion**: Print the calibrated interval in Table II for R and RR(N), and give the nominal ones in the supplement.
**Severity**: Minor
**Confidence**: 4 — verified against text and Table S16

### W9: The revision history and AI-assistance disclosure are complete in substance but scattered and inconsistently worded
**Problem**: Section IV-D states "two pre-submission reviews by an AI-based review panel", but Supplement S10 says the analyses "were added after an external pre-submission review", and S4 refers to "an independent reviewer's own code" and S11 to an "independent claim audit". A reader could take "external" and "independent" to mean human reviewers. The history is spread over Section IV-D, a 45-row Table S4, the S10 and S11 introductions and a DRAFT_HISTORY file that sits in a deposit not yet created. Internal identifiers appear in a journal supplement (file `recount_v12\RECOUNT_COMPARE_A93_v02.md`, "A4 extraction", "A9-3", `derive_v03.py`, "the earlier draft" references in Fig. S4 and Table S29 captions). The Acknowledgment lists what Claude did in plain terms, which is good, and the author confirmation is a gate (not counted here).
**Evidence Anchor**: `text: §IV-D "After two pre-submission reviews by an AI-based review panel"; Supplement S10 "added after an external pre-submission review of an earlier draft"`
**Why it matters**: A new submission should tell the editor in one place who or what reviewed earlier drafts, what changed because of it, and which verification was done by AI sessions that share code and results with the first program. The wording variance could be read as overstating independence.
**Suggestion**: Write one provenance paragraph in the main text (what was reviewed by AI panels, twice, which analyses were added in response, which verification is non-blind), use "AI-based" consistently, delete internal file names and draft-relative captions, and cut Table S4 to the deviations that affect a reader's reading of a claim.
**Severity**: Minor
**Confidence**: 4 — core expertise: editorial handling of disclosure; I do not judge the verification itself

### W10: Abstract, §I and §VII are not parallel; a conclusion-only claim and one selective figure
**Problem**: §VII states that a time-gap margin "recovers 0.314 of it" and that little room remains "for any source" under a prompt stop; the abstract and the four contributions mention neither. The abstract's 12% is the 6 m/s² value, one point in a range the text gives (0.29, 0.18, 0.12, 0.06 at 4, 5, 6, 7.6 m/s²). The conclusion is a single paragraph of about 360 words.
**Evidence Anchor**: `text: §VII "a time-gap margin on the ego's speed recovers 0.314 of it"; Abstract "leaves 12% of it"`
**Why it matters**: The time-gap margin is the one result that connects to the established adaptive-cruise-control practice this readership knows, and it is absent from the abstract and contributions, whereas a single point of the stop-deceleration range (12%) is present.
**Suggestion**: Make the three texts state the same three or four claims in the same order; give the 12% with its range; split §VII into findings and next steps.
**Severity**: Minor
**Confidence**: 4 — core expertise: structural coherence

---

## Detailed Comments

### Journal Fit
Topic and venue match: automated-vehicle perception, planning and safety evaluation, simulation-based testing, adaptive cruise control. The tracker-to-planner chain is within scope. What the venue's readers will expect and not find: a scenario in which the tested quantity varies, real-sensor data, or any closed-loop test of a covariance margin. Length is the main fit problem (W3). A shorter paper aimed at this readership, with the protocol and commitment-dependence lesson at its centre, would fit better.

### Originality
Three claims: the evaluation design (equal caution, oracle control, graded oracles), the commitment dependence of the open-loop room, and the ground-truth-free ratio check. The evaluation design is a new combination of known ingredients, and Deglurkar et al. [13], which the paper names as its closest relative, already grids uncertainty values and splits outcomes by forecast error. The Riccati-recursion mechanism is declared not new. The after-stop lag result (the room lies where the 2 Hz tracker's velocity still lags the stop) is a finding about this test bed's update rate (Supplement S11.9 predicts it grows with latency). The novelty case is honest but modest (W1, W5).

### Significance
If the conclusions hold, a tracking-and-planning developer learns that a fixed-noise Kalman tracker's covariance is a constant in straight following, which was known, and that a stated commitment matters when scoring open loop, which matches prior warnings [28], [29]. The potentially stronger result, that a margin scheduled on the tracker's own phase estimate recovers most of the room, is exploratory, open loop, from one planner (W1, W4). Timeliness is good (AI-panel and open-loop evaluation debates), reach is narrow.

### Structural Coherence
Title, abstract, §I contributions, §VII align on the main line. Numbers traced (abstract and §I and §VII to main-text tables or prose): 5.6 (Table II); 4.4 to 6.7 (§V-A, S16; Table II differs, W8); 83% of decisions after the stop (§III-A, S5); 1.10 (Table V, 1.103); 2.2 decisions (§V-A, S31c); 83% braking prediction (Table II, 0.831); 90% and 99.9% and 89% (§V-C, S23, S32); 12% (Table III, 0.122); 99.26% of 152,264 rows (Table V); 0.314 (Table II). No contradiction found. Items carried only outside Tables II to V are listed in W4. The conclusion adds items absent from the abstract (W10). The research question is clear and the conclusion answers it, but it is joined to three secondary conclusions.

### Title & Abstract
Abstract measured at 248 words by my own count (line 9 of the manuscript; the manifest also gives 248), under the 250 limit. See W6 for readability. The title is accurate but long (18 words) and uses "at Equal Caution"; "Lead Braking" overstates the population (83% after the stop).

### Conclusion
Consistent with the results and appropriately fenced, but a single long paragraph, and it states conditional readings ("If decisions are committed for 3 s ...; if a prompt and reliable stop is available ...") that give no single recommendation (W1, W10).

---

## Questions for Authors
1. If a reader takes away one sentence, which is it? Would you consider recasting the paper around the protocol and the commitment dependence, with the tracker null as the worked example, within the 10-page recommendation?
2. The schedule on the tracker's own phase estimate recovers 99.9% held out (Table S32) but the estimate mislabels 128 after-stop decisions as braking, where the room lies. Is this result a margin you would propose a planner use, and could it be tested in closed loop with the margin sources as arms?
3. The reviewed claim of "two independent programs": please state in the main text who or what wrote each, which share the scoring library and arrays, and whether any human other than the author reviewed an earlier draft (Supplement S10 says "external").
4. The companion manuscript [9], under review at IEEE Access, shares the detector, tracker configuration and margin form. What, concretely, is shared in text and analysis, and does the editor need [9] to judge this paper?
5. What is the typeset page count of the main text in the journal template? My estimate (15 to 18 pages) is unverified.
6. Can you add one scenario family in which the ratio varies (crossing or track births) and run the decision-level test, so that the paper is not a null by construction?

---

## Minor Issues

(No Severity or anchors; copyedit-level.)

### Language / Grammar
- Replace "wrong go" and "caution" with the established terms in running text, or define them once in the first paragraph of §I.
- §VII is one paragraph of about 360 words; split.

### Citation Format
- Several key references are arXiv-only and 2026 (for example [8], [14], [17], [19], [25]); give published versions where they exist. Reference verification is left to the editor.
- [9] is cited as "submitted"; the Scope paragraph is the only place its overlap is stated.

### Figures and Tables
- Fig. 2(b): the cluster near ratio 1.68 (84 rows after two missed updates, Supplement S10.7) is not explained in the caption.
- Fig. 4(b): "3 s" plotted as a categorical point on a numeric τ axis.
- Table II mixes three populations and nine rows; Table IV uses "n.e." with bracketed points. Consider one table per population or moving Table IV to the supplement.
- Supplement table numbering is not sequential (Table S28 inside S1.1, S29 inside S8, S12b, S20a to S20d, S30 to S38); Fig. S3 and Fig. S4 map to files named `fig5` and `fig3_rr`.

### Layout
- Submission gates (author's, not findings): the author block (manuscript line 5); the repository name and DOI in Data and Code Availability; the "[AUTHOR CONFIRMATION: …]" at the end of the AI-generated-content statement.

---

## Criterion-Bound Judgements

Calibration status: `NOT_CALIBRATED`

| Dimension / criterion | Criterion source | Judgement | Evidence anchors | Rationale | Uncertainty or scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| Journal fit and scope | criteria binding unavailable; general field norms | PARTLY_MEETS | `text: §I "In CARLA, a lead vehicle brakes in front of the ego"` | Topic is within perception, planning and safety evaluation for automated vehicles; the contribution is narrow and the length is far above the recommendation. | No journal criteria brief; my reading of readership is from field norms. | yes: fit is credible but depends on W1 and W3 |
| Originality | criteria binding unavailable; general field norms | PARTLY_MEETS | `text: §II "The mechanism is not new: a nearly constant covariance follows from the Riccati recursion"` | New combination of an equal-caution sweep, oracle control and graded oracles; mechanism declared known; novelty rests on an abstract-only search. | I cannot confirm absence of prior work (W5). | yes: W5 is minor but W1 bears on significance |
| Significance and impact | criteria binding unavailable; general field norms | PARTLY_MEETS | `text: §VI Limits "only comparisons between sources on the same decisions are meant to transfer"` | Useful lesson on stating commitment and population; confirmatory result is an expected null; actionable findings are exploratory and open loop. | Real-sensor and closed-loop relevance untested. | yes: W1, W2 |
| Structural coherence (abstract, introduction, conclusion) | criteria binding unavailable; general field norms | PARTLY_MEETS | `absence: Tables II–V — expected the held-out per-phase shares and the 2.2-decision bound that the Abstract states; checked Tables I–V, Fig. 3 caption and §V-A and §V-C text` | The three texts agree on the main line and no number contradicts a source; some headline numbers lack a main-text table and the conclusion adds a claim. | Traced only to the main text and tables; supplement values taken as printed. | yes: W4 |
| Abstract limit (250 words) | criteria binding unavailable; general field norms | MEETS | `text: Abstract (248 words by my count; manifest 248)` | Within the stated limit. | none identified | no: readability is a separate item (W6) |
| Clarity and length (10 pages recommended) | criteria binding unavailable; general field norms | DOES_NOT_MEET | `dataset: PACKAGE_MANIFEST_v12.txt — whole manuscript 12451 words; supplement 34240 words` | Main text and supplement are well above what a reader needs to follow one argument; notation and hedging load is high. | Page count is my estimate (15 to 18), not a typeset count. | yes: W3 |
| Handling of revision history and AI-assistance statement | criteria binding unavailable; general field norms | PARTLY_MEETS | `text: §IV-D "After two pre-submission reviews by an AI-based review panel"; Supplement S10 "added after an external pre-submission review of an earlier draft"` | Disclosure is substantive and mostly plain; scattered, uses "external" and "independent" for AI sessions, and leaks internal identifiers. Author confirmation is a gate. | I do not judge the verification itself. | no: wording and placement (W9) |

Recommendation rationale: unresolved decision-bearing criteria are significance (W1, W2), clarity and length (W3) and claim-to-table traceability (W4), all repairable by re-scoping and rewriting. Strengths on candour and design do not offset the length and take-away problems; the two are not weighed against each other numerically.
