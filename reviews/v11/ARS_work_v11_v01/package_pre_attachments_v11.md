# Editorial Decision Package

Manuscript: draft v11, "Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution: A Fixed-Noise Kalman Tracker in CARLA Lead Braking". Mode: academic-paper-reviewer `full`, contract `reviewer/reviewer_full/v2`, five seats (EIC, R1, R2, R3, DA). Synthesizer: `editorial_synthesizer_agent`, v3.6.2 Sprint Contract Synthesizer Protocol. Date: 18 November 2026.

## Calibration Resolution

`calibration_status: NOT_CALIBRATED`

Current runtime boundary: this package is not upgraded from a candidate or prose-named profile. `PROFILE_MEASURED` remains unavailable until a closed profile artifact and replay validator bind the exact target fields to the completed panel's `execution_topology_sha256`. Every seat card also reports `NOT_CALIBRATED`.

## Part 1: Editorial Decision Letter

Dear Author(s),

Thank you for submitting your manuscript titled "Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution: A Fixed-Noise Kalman Tracker in CARLA Lead Braking" to the IEEE Open Journal of Intelligent Transportation Systems as a regular paper. This is a simulated editorial decision produced by an ARS review run; the journal did not issue it. No criteria manifest was bound to the run (`criteria_binding_unavailable`), so it makes no venue-alignment claim. Your manuscript has been reviewed through five role-separated review seats, including a Journal-Fit Reviewer role. Their execution provenance is reported below and is not reduced to a binary independence claim.

### Manuscript Information

- **Title**: Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution: A Fixed-Noise Kalman Tracker in CARLA Lead Braking
- **Venue as configured**: IEEE Open Journal of Intelligent Transportation Systems, regular paper (abstract limit 250 words; no page limit, 10 pages recommended). Unbound run: fit was judged against the configuration card and the journal's public scope only.
- **Manuscript ID**: none assigned (pre-submission draft v11, reviewed as a fresh submission)
- **Decision date**: 18 November 2026
- **Review round**: Round 1 of this submission

### Decision: Major Revision

#### Mechanical decision record (sprint contract, three steps)

**Binding pre-check (unbound run).** The protocol requires that, in an explicitly unbound run, all five cards disclose `criteria_binding_unavailable` and make no venue-alignment claim. EIC, R2 (Domain), R3 (Perspective) and DA print the token. R1 (Methodology) states the same condition in words ("No venue criteria were bound for this call, so this card makes no venue-alignment claim") but does not print the token. This synthesis treats that sentence as the disclosure and flags the wording gap here without changing the card (Phase Boundary). Binding conformance is not a score or a decision input. No card makes a venue-alignment claim.

**Step 1: role-scoped scoring matrix.** Only scores from seats whose `contract_role` is in a dimension's `eligible_roles` are counted. Ineligible seats score `not_assessed` structurally and are excluded from numerator and denominator. No eligible seat abstained, and no seat declared a block or a fatal block.

| Dimension | Priority | Eligible roles | EIC | R1 | R2 | R3 | DA | Assessed eligible scores (trigger, transported) | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| D1 methodology_rigor | mandatory | methodology | — | warn | — | — | — | R1 warn: "Reporting or robustness gaps that do not threaten a headline conclusion" | warn |
| D2 domain_accuracy | mandatory | domain | — | — | warn | — | — | R2 warn: "imprecise or inconsistent terminology, a missing or outdated citation…, or a generalisation that reaches modestly beyond the evaluated conditions" | warn |
| D3 argumentative_coherence | mandatory | da, methodology | — | warn | — | — | warn | R1 warn: "Local overstatement or loose wording that leaves the central thesis intact"; DA warn: "Localised coherence gaps that leave the central argument standing" | warn |
| D4 cross_disciplinary_relevance | high | perspective | — | — | — | warn | — | R3 warn: "Adjacent-field connections are asserted with only partial support" | warn |
| D5 writing_and_structure | normal | eic | warn | — | — | — | — | EIC warn: "The manuscript is reviewable but carries correctable presentation defects, such as redundant or overlong sections" | warn |
| D6 venue_fit_and_contribution | mandatory | eic | warn | — | — | — | — | EIC warn: "the case for significance to the venue's readers is weaker or less explicit than it should be and needs sharpening" | warn |

"—" marks a structural `not_assessed` from an ineligible seat. These are sprint-contract judgements (`judgement_scale: sprint_contract`) copied without translation.

**Step 2: failure conditions** (closed vocabulary; two-stage evaluation: the cross-reviewer quantifier is applied to each selected dimension's assessed eligible seats, then the expression's dimension quantifier is applied).

| Condition | Severity | Quantifier | Expression | Evaluation | Fired |
|---|---|---|---|---|---|
| F1 | 95 | any | any mandatory dimension has a fatal block | D1, D2, D3, D6: no assessed seat scored block | false |
| F2 | 90 | any | any mandatory dimension scores 'block' | D1, D2, D3, D6: no block from any eligible seat | false |
| F3 | 70 | majority | two or more mandatory dimensions score 'warn' or worse | D1 (n=1, owner R1 warn): true; D2 (n=1, owner R2 warn): true; D3 (n=2, both needed: R1 warn, DA warn): true; D6 (n=1, owner EIC warn): true. Four of four mandatory dimensions, at least two required | true |
| F4 | 60 | any | any high-priority dimension scores 'block' | D4: R3 warn | false |
| F5 | 40 | any | any dimension scores 'warn' or worse | D1 to D6 each have a warn | true |
| F0 | 10 | all | every dimension scores 'pass' | no dimension passes | false |

**Step 3: precedence and audit emission.** Fired: F3 (severity 70) and F5 (severity 40). F3 has the highest severity, so its action applies. The DA card has no CRITICAL row, so the DA adjudication list is empty. The decision is not accept, so no `DA-CRITICAL-VS-ACCEPT` marker applies.

```text
dimension_verdicts: [D1=warn, D2=warn, D3=warn, D4=warn, D5=warn, D6=warn]
fired_conditions: [F3, F5]
da_critical_adjudications: []
editorial_decision=major_revision
```

**Cross-model decision check (Step 4b).** `ARS_CROSS_MODEL` was not set and the panel had no cross-model track. No blind cross-model comparison was run, and no cross-model checkpoint line applies.

### Review Panel Provenance (#540/#740)

- **Typed artifact**: `ARS_work_v11_v01/provenance_v11.json` (`review-panel-provenance/1.0`)
- **Artifact SHA-256** (raw bytes, computed by this synthesis): `abc2835254ec320e2db8b93cad0f694832de44269b185e1706dfe7f1c0566b46`
- **Panel ID**: `ars-review-v11-20261118`
- **Contract binding**: `reviewer/reviewer_full/v2`, pinned contract SHA-256 `d958bc2ade7d9d154954c33fd424766697a8b6ef664854800a3106d804ee7e5c`
- **Normalized manifest SHA-256**: `57ecf4d8f55a958359cad698c8e4dd0b5606440b53265aa7a1063308d15f748c`
- **Execution topology SHA-256**: `4f674d38ae1cd4b94b3a69dbbdb050f529ea0f9e3e0e3a4d37b9d5d254c3d81e`
- **Fresh-context scope**: `within_panel_attempt_only`. This does not compare retries, earlier attempts or the earlier v10 review round.
- **Validation note**: the dispatcher reports the artifact as validated. In this Windows install the stock `scripts/review_panel_provenance.py validate` stops at its contract-pin precondition, because the installed `shared/contracts/reviewer/full.json` has CRLF line endings: its raw digest is `900290ba…`, and its LF-normalised digest equals the pinned `d958bc2a…`. With that precondition met in memory, and no file changed, the artifact replays with zero errors. This is an install line-ending issue, not a defect in the artifact.

| Seat | Role ID | Actor type | Context ID | Peer outputs visible | Model family | Provider | Human reviewer ID |
|---|---|---|---|---|---|---|---|
| EIC | eic | model | ctx-1a56cf2c12201e6c | `unknown` (not recorded) | claude-opus-5-5 | anthropic | `null` |
| R1 | methodology | model | ctx-2d4af8a4b69f5880 | `unknown` (not recorded) | claude-opus-5-5 | anthropic | `null` |
| R2 | domain | model | ctx-914b4d601dd54658 | `unknown` (not recorded) | claude-opus-5-5 | anthropic | `null` |
| R3 | perspective | model | ctx-5127c344c36924ed | `unknown` (not recorded) | claude-opus-5-5 | anthropic | `null` |
| DA | da | model | ctx-59eddefd9c079b5e | `unknown` (not recorded) | claude-opus-5-5 | anthropic | `null` |

| Provenance axis | Status (`true` / `false` / `unknown`) |
|---|---|
| Role-separated | `true` |
| Within-panel invocation-context separation | `true` |
| Blind to peer outputs | `unknown` |
| Model-family distinct | `false` |
| Provider distinct | `false` |
| Human-reviewer distinct | `false` |

- **Blind to peer outputs, why `unknown`**: the seats were instructed not to read each other's files, but the dispatcher could not observe their file access, so no seat's visibility was recorded. `unknown` is not evidence that any seat saw another's output, and it is not evidence that none did.
- **Cross-model track**: none. All five seats ran on one model family (Claude Opus 5.5, artifact ID `claude-opus-5-5`) from one provider. This synthesis was produced by the same model family.
- **Binary independence claim**: Not computed (`independence_claim: not_computed_from_personas`). Persona or role diversity proves only `role_separated`; the panel is not relabelled as independent.
- **Correlated-error disclosure** (required; reason `same_model_family`): "All model-executed review seats used one model family; role separation does not remove correlated-error risk."

### Coverage

- **What the panel read (Phase 0 record)**: the Abstract, Index Terms, Sections I–VII, Data and Code Availability, Funding, Competing Interests, Acknowledgment (AI disclosure), references [1]–[55], Tables I–V and the notation table, Figs. 1–4 (PNG and vector PDF), Supplement S1–S10 with Tables S1–S29 (including S12b, S20a–S20d and S24b), and Figs. S1–S4. Raw data, code, analysis plans, amendments and lock manifests were not supplied, because the deposit does not yet exist. The panel judged the text and tables only.
- **Blindness disclosure (Phase 0 record)**: before Phase 0, the dispatching session read two hand-over notes that summarise the v10 review's decision (Major Revision), its two blocking themes and the v11 analyses. The panel's Step 1 is blind to the v10 review text and to the response to it, but not to that summary.
- **What this synthesis read**: the contract, the five Phase 2 cards, the provenance artifact and the Phase 0 field analysis. It checked seat quotations against `MANUSCRIPT_v11.md` and `SUPPLEMENT_v11.md` for the items under arbitration and for the Required Items. Every quotation checked was found verbatim. No finding was added from that check.
- **Advisory attachments**: the acronym, suggested-reference and reviewer-claim checks are appended later by the dispatching session. The suggested references in the R2 and R3 cards have not been verified here.

### Reviewer Summary

| Reviewer | Role | Recommendation | Confidence |
|---|---|---|---|
| Journal-Fit Reviewer (EIC) | Associate Editor, safety evaluation of automated driving and the perception–planning interface | Preliminary journal-fit signal: major revision (a baseline, not a decision) | 4 |
| Reviewer 1 (Methodology) | Statistician, resampling inference for clustered and non-smooth statistics; simulation-study design | Not stated in the card (D1 warn, D3 warn; two Major and ten Minor weaknesses) | No report-level score; per-finding 3–4 |
| Reviewer 2 (Domain) | Multi-object tracking and uncertainty-aware motion planning | Major Revision (domain view only) | 4 |
| Reviewer 3 (Perspective) | Safety-assurance engineer (scenario-based V&V, UN R157, RSS, ISO 21448); decision analysis | Minor Revision (seat-level advice only) | 4 |
| Devil's Advocate | Fixed adversarial seat | N/A — findings only (0 CRITICAL, 6 MAJOR) | N/A — per-finding only |

Confidence is a self-reported disclosure of uncertainty and scope. It never weights, counts or resolves anything below.

### Consensus Analysis

#### Step 1a: Reviewer Summary Matrix

| Dimension | Journal-Fit Reviewer (EIC) | R1 (Methodology) | R2 (Domain) | R3 (Perspective) |
|---|---|---|---|---|
| Overall Recommendation | Major revision (preliminary signal) | Not stated | Major Revision | Minor Revision |
| Contract scores | D5 warn, D6 warn | D1 warn, D3 warn | D2 warn | D4 warn |
| Confidence / scope disclosure | 4; bootstrap theory and tracker internals outside remit | per-finding 3–4; domain significance and regulatory context not assessed | 4; regulatory reading of R157 not assessed | 4; outsider to tracker internals and fine statistics |
| Key Strengths | 7: in scope with ITS framing; novelty stated with its limits; title and abstract sell the design, not the null; every abstract number traces (247 words); practical reading fenced; clear organisation and consistent figures; limits and analysis history disclosed | 7: interval validity diagnosed for the non-smooth share; positive control itself validated; hashed plans and itemised deviation log; ground-truth-free ratio check; sensitivity-tested evaluability rule; plan extension with censoring sensitivity; independent re-implementation | 6: steady-state null anticipated and confirmed (Table S15); margin projection exact; closest prior work fair where checked; braking prediction and R157 values positioned correctly; reliability check interpreted correctly; scope precise | 9: R157 values fenced; per-phase baseline separates regime from per-decision information; deployment sentence fenced; closed-loop check described for what it is; defined terms bridge fields; excluded road users named; AI-use statement and configuration table; positive control as a gauge study; ground-truth-free screen |
| Key Weaknesses | 12 (1 major, 11 minor) → Step 1b | 12 (2 major, 10 minor) → Step 1b | 10 (2 major, 8 minor) → Step 1b | 12 (all minor) → Step 1b |
| # of Questions | 5 | 6 | 5 | 6 |
| # of Minor Issues (separate list) | 0 (a Submission Gates paragraph, not findings) | 0 | 5 bullets (3 substantive, 2 scope disclosures) | 0 ("None beyond W1 to W12") |

The DA card has no CRITICAL rows and six MAJOR rows (M1–M6), all under D3, plus prose observations.

#### Step 1b: Weakness Sub-Claim Inventory

Rows are listed for raised, corroborated and disputed positions and for DA issue rows. A seat not listed for a sub-claim is `not-mentioned`, which is silence, not opposition. Severity and confidence are transported from the cards. Sub-claims split from one parent share that parent's severity. A DA row never creates a sub-claim and is never counted.

| sub_claim_id | parent_weakness | reviewer_id | position | evidence_pointer | severity | confidence |
|---|---|---|---|---|---|---|
| SC-1 | EIC W1: test bed rarely exercises what makes the null worth measuring | EIC | raised | EIC W1 · text: §I "It still has to be measured: the covariance also depends on detections, misses and track age" | major | 3 |
| SC-1 | R2 W1: steady-state argument stated for a linear filter | R2 | corroborated | R2 W1 remedy: "state when the steady-state argument holds (fixed heading, regular updates, no misses)" | major | 3 |
| SC-1 | DA M1: contribution 3 entailed, not tested | DA | raised | DA M1 · text: §I "It still has to be measured…"; Supplement S9 "Every lead-braking decision has a track in the oldest age band…" | major (DA band) | 4 |
| SC-2 | EIC W1 | EIC | raised | EIC W1: "contribution 3 is mostly a measured confirmation of the steady state" | major | 3 |
| SC-2 | DA M1 | DA | raised | DA M1 remedy: "recast contribution 3 as a confirmation" | major (DA band) | 4 |
| SC-3 | EIC W1 | EIC | raised | EIC W1 remedy: "add to the abstract that track births, misses and real sensing are untested" | major | 3 |
| SC-4 | EIC W2: design discriminates information only on pooled decisions | EIC | raised | EIC W2 · text: §IV-B "Within the lead-braking phase and with the ego moving, the same mixtures can score below the class average" | minor | 3 |
| SC-4 | DA M2: positive control certifies phase, not per-decision error | DA | raised | DA M2 · text: §IV-B "Pooled, the null of Section V-A is therefore not a blunt measure." | major (DA band) | 4 |
| SC-5 | EIC W3: abstract omits the population mix | EIC | raised | EIC W3 · text: §III-A "Of the evaluated decisions, 77.5% have the ego at or below 0.5 m/s, and 82.7% come after the lead has stopped." | minor | 4 |
| SC-5 | R2 W2: per-phase and after-stop findings not explained physically | R2 | disputed (severity: major against EIC's minor; remedy identical) | R2 W2 remedy: "note in the scope that most decisions are a standstill queue rather than following in motion" | major | 3 |
| SC-6 | EIC W4(a): abstract's 89% omits truth-derived phase labels | EIC | raised | EIC W4 · text: Abstract "A class-average margin with one scale per phase of the lead's motion recovers 89% of the room" | minor | 4 |
| SC-6 | R2 W9 | R2 | raised | R2 W9 · text: Abstract (same sentence) | minor | 4 |
| SC-6 | R3 W3: 89% is an in-sample, truth-labelled value | R3 | corroborated | R3 W3: "with phase labels from the logged truth… state that it is an in-sample value" in the abstract and contributions | minor | 3 |
| SC-6 | DA M3 | DA | raised | DA M3 · text: §I contribution 2 "gains 89% of the pooled room knowing only the phase, not any decision's error" | major (DA band) | 3 |
| SC-7 | EIC W4(b): 89%, 29%, 12% from added analyses, unlabelled in the abstract | EIC | raised | EIC W4: "The 89%, 29% and 12% come from analyses added after the first results (§IV-D)" | minor | 4 |
| SC-7 | R1 W6: abstract rests on added analyses | R1 | raised | R1 W6 · text: §IV-D "The analyses of Supplement S10 were added last, each defined before its values were read." | minor | 4 |
| SC-7 | DA M5 | DA | raised | DA M5 · text: §VII "These conditional results come from descriptive analyses added after the first results." | major (DA band) | 4 |
| SC-8 | EIC W4(c): 35 runs examined earlier (transfer, not replication) | EIC | raised | EIC W4 bullet 3 (§III-A) | minor | 4 |
| SC-9 | EIC W5: "none that we can measure" departs from the bound | EIC | raised | EIC W5 · text: Abstract "recovers none of the room that we can measure (0.1%; calibrated interval −0.2% to 0.2%)" | minor | 3 |
| SC-9 | R1 W4(b): equivalence wording names no margin | R1 | corroborated | R1 W4: "the Discussion says 'a class average does as well as the tracker's covariance'… phrase the null as equivalence within that margin" | minor | 4 |
| SC-10 | EIC W6: ranking omits the time-gap spacing policy | EIC | raised | EIC W6 · text: §VI "a time-gap margin, the usual spacing policy [52], was not among them" | minor | 4 |
| SC-10 | R3 W4(b) | R3 | corroborated | R3 W4: "or the constant-time-gap spacing that production ACC… already use" | minor | 3 |
| SC-11 | EIC W7: ITS positioning read from abstracts only | EIC | raised | EIC W7 · text: Supplement S6 "their content is summarised from abstracts only" | minor | 3 |
| SC-11 | R2 Minor Issues, bullet 3 | R2 | corroborated | R2 Minor Issues: "rests on abstract-level reading of [41]-[52] (Supplement S6); a hedge naming that limit would help" | minor [SEVERITY-SOURCE: letter-fallback] | 4 [CONFIDENCE-SOURCE: report-level] |
| SC-12 | EIC W8: main text likely 12–13 pages | EIC | raised | EIC W8 · absence: whole manuscript — expected a length near the 10-page recommendation | minor | 3 |
| SC-13 | EIC W9: dense results prose | EIC | raised | EIC W9 · text: §V-B "With the ego moving the prediction recovers 0.47 [0.35, 0.57]…" | minor | 4 |
| SC-14 | EIC W10: symbol D undefined in the main text | EIC | raised | EIC W10 · text: notation table "$D/201/100 \times n$" | minor | 5 |
| SC-15 | EIC W11: Table II signed-caution layout | EIC | raised | EIC W11 · table: Table II | minor | 4 |
| SC-16 | EIC W12: hard-to-parse CARLA sentence | EIC | raised | EIC W12 · text: Abstract "CARLA runs in which a lead vehicle brakes are perceived by…" | minor | 5 |
| SC-17 | R1 W1(a): non-smooth RR(N) plausibly a grid-interleaving artefact | R1 | raised | R1 W1 · text: §V-A "The step-frontier statistic is non-smooth, and nominal 95% intervals are not valid for it" | major | 4 |
| SC-18 | R1 W1(b): double-bootstrap calibration unjustified | R1 | raised | R1 W1: "The abstract's 'calibrated interval −0.2% to 0.2%' therefore lacks a demonstrated coverage property." | major | 4 |
| SC-19 | R1 W2(a): tuning-run values omitted from the main text | R1 | raised | R1 W2 · table: Supplement Table S2, tuning and evaluation columns | major | 4 |
| SC-20 | R1 W2(b): recording policy missing from the stated conditions | R1 | raised | R1 W2: "its lesson… omits the data-collecting policy" | major | 4 |
| SC-20 | R3 W10: recording planner's contact rate bounds absolute numbers | R3 | disputed (severity: minor against R1's major; remedy compatible) | R3 W10 · text: Table S28 "Five of the 35 evaluation runs and 10 of the 20 tuning runs ended at the first physical contact" | minor | 3 |
| SC-21 | R1 W3: 89% an in-sample envelope | R1 | raised | R1 W3 · text: §V-C "took its frontier over all triples of scales" | minor | 3 |
| SC-21 | R3 W3(a) | R3 | raised | R3 W3 · text: §V-C "took its frontier over all triples of scales" | minor | 3 |
| SC-21 | DA M3 | DA | raised | DA M3: "an in-sample lower envelope over about 8.2 million scale triples" | major (DA band) | 3 |
| SC-22 | R1 W4(a): 0.5% bound not fixed before values were read | R1 | raised | R1 W4 · text: §V-A "no interval method we tried reaches 0.5% of the room" | minor | 4 |
| SC-23 | R1 W5: "slightly narrow" understates undercoverage | R1 | raised | R1 W5 · text: §IV-B "all other intervals should be read as slightly narrow" | minor | 4 |
| SC-24 | R1 W6(b): S10 amendment hash and date not printed | R1 | raised | R1 W6 | minor | 4 |
| SC-25 | R1 W6(c): parts of verification not blind | R1 | raised | R1 W6: "Parts of the verification were not blind" (Sections S10.5, S10.9) | minor | 4 |
| SC-25 | R3 W12: "independent" verification needs provenance | R3 | raised | R3 W12 · text: §IV-D "independent second programs re-implement the scoring" | minor | 3 |
| SC-26 | R1 W7: Spearman equivalence from overlapping marginal intervals | R1 | raised | R1 W7 · text: §V-E "ranks the realised error… no better than the class average's does" | minor | 4 |
| SC-27 | R1 W8: shares interpreted where grading fails | R1 | raised | R1 W8 · text: §VI "its share while the lead brakes falls from 0.61 to 0.35" | minor | 4 |
| SC-27 | DA M4 | DA | raised | DA M4 · text: §VI "in every population whose shares are interpreted" | major (DA band) | 4 |
| SC-28 | R1 W9: frontier sensitivities given for NA only | R1 | raised | R1 W9 · table: Supplement Table S5, hull column and footnote | minor | 4 |
| SC-29 | R1 W10: caution axis under reaction-and-stop | R1 | raised | R1 W10 · text: §IV-C "Only the wrong-go flag changes: caution keeps the 3 s scoring's definition." | minor | 3 |
| SC-30 | R1 W11(a): deposit not yet created or accessible | R1 | raised | R1 W11 · text: Data and Code Availability | minor | 4 |
| SC-31 | R1 W11(b): raw recordings on request only | R1 | raised | R1 W11 · text: Data and Code Availability "The raw recordings are available from the author on request." | minor | 4 |
| SC-31 | R3 W11(b) | R3 | corroborated | R3 W11: "the raw recordings are on request… or state the restriction" | minor | 4 |
| SC-32 | R1 W12: the tracker covariance is also off-policy | R1 | raised | R1 W12 · text: §III-B "for every other source they are off-policy" | minor | 3 |
| SC-33 | R2 W1(b): tracker run as an EKF with object-frame noise | R2 | raised | R2 W1 · text: Supplement Table S28 "extended Kalman filter with a constant-velocity model in the object frame" | major | 3 |
| SC-34 | R2 W1(c): reach claim does not separate geometry from information | R2 | raised | R2 W1 · text: §V-E "so the null of this paper is not expected to carry over to them" | major | 3 |
| SC-35 | R2 W2(a): no physical mechanism for the per-phase and after-stop findings | R2 | raised | R2 W2 · text: §V-C "The 83% is therefore a figure for recordings that continue for about 20 s after the stop." | major | 3 |
| SC-36 | R2 W3: NIS-inflated source tests little; wrong block | R2 | raised | R2 W3 · text: §III-A "the median over runs of the mean NIS… is 0.24, against an expected 2" | minor | 4 |
| SC-37 | R2 W4: 1.10 depends on look-ahead | R2 | raised | R2 W4 · table: Supplement Table S14 | minor | 4 |
| SC-38 | R2 W5: margin scale mapped to a spacing policy | R2 | raised | R2 W5 · text: §II "the planner's margin plays the role of a spacing policy in adaptive cruise control [52]" | minor | 4 |
| SC-38 | R3 W5 | R3 | raised | R3 W5 · text: notation table "Safety distance of a spacing policy [52]" | minor | 4 |
| SC-39 | R2 W6: adjacent literature missing | R2 | raised | R2 W6 · absence: §II Related Work — stochastic-MPC car following and fading-factor filtering | minor | 4 |
| SC-40 | R2 W7: [17] summarised loosely | R2 | raised | R2 W7 · text: §II "The closest planner-in-the-loop study [17] finds…" | minor | 3 |
| SC-41 | R2 W8: supplement keeps withdrawn wording | R2 | raised | R2 W8 · text: Supplement S8.2 "a mechanism that no analysis here isolates" | minor | 5 |
| SC-41 | DA M5 (Table S4 portion) | DA | raised | DA M5: "Table S4… still describes NIS-inflated abstract wording that no longer exists" | major (DA band) | 4 |
| SC-42 | R2 W10: direction of test-bed simplifications not discussed | R2 | raised | R2 W10 · text: Supplement Table S28 "run every tenth frame (2 Hz); no latency simulated" | minor | 4 |
| SC-43 | R2 Minor Issues, bullet 1: room related to VPI is an analogy | R2 | raised | R2 Minor Issues: "'analogous to' would be more precise" | minor [SEVERITY-SOURCE: letter-fallback] | 4 [CONFIDENCE-SOURCE: report-level] |
| SC-43 | R3 W2: room mapped to VPI although E is not a bound | R3 | raised | R3 W2 · text: notation table "Value of perfect information [55]" | minor | 4 |
| SC-44 | R2 Minor Issues, bullet 2: Table V includes the tuning runs | R2 | raised | R2 Minor Issues: "the tuning-only column of Table S26 shows the same pattern, which could be said in the main text" | minor [SEVERITY-SOURCE: letter-fallback] | 4 [CONFIDENCE-SOURCE: report-level] |
| SC-45 | R3 W1: stop-reliant reading omits following traffic and fallback reliability | R3 | raised | R3 W1 · text: §VI "the choice of source matters mainly for comfort and progress, which we did not score" | minor | 4 |
| SC-45 | DA M6 | DA | raised | DA M6 · text: §VI (same sentence); §I Scope "traffic behind the ego and real sensor data are outside the evaluation" | major (DA band) | 3 |
| SC-46 | R3 W4(a): allocation finding not tied to a runnable rule | R3 | raised | R3 W4 · text: §VI "a time-gap margin, the usual spacing policy [52], was not among them" | minor | 3 |
| SC-47 | R3 W6: normative register for the 2 m gap | R3 | raised | R3 W6 · text: §V-D "Performance model 2 asks for 2 m at standstill, not for the absence of contact." | minor | 3 |
| SC-48 | R3 W7: "legal following distance" | R3 | raised | R3 W7 · text: Supplement S3 "over the legal following distance" | minor | 4 |
| SC-49 | R3 W8: the 12% uses a stop harder than the planner's fallback | R3 | raised | R3 W8 · text: Abstract "With a perfect 6 m/s² stop 0.75 s after each decision, 12% of the room remains." | minor | 4 |
| SC-50 | R3 W9: wrong-go counts ignore severity | R3 | raised | R3 W9 · text: notation table "A collision under the assumed manoeuvre; a criticality outcome [50]" | minor | 3 |
| SC-51 | R3 W11(a): deposit omits contribution 4's arrays and the pipeline | R3 | raised | R3 W11 · text: Data and Code Availability "the per-decision arrays of the 55 lead-braking runs" | minor | 4 |

#### Step 1c: Surface-form parity

Each sub-claim was judged on its paper evidence, not on its wording. Two corroborations come from R2's informally worded Minor Issues list (SC-11, SC-43) and one sub-claim originates there (SC-44). All three were kept at full standing; their only differences are the fallback tags for severity and confidence. No sub-claim was credited for technical precision: R1 W1's grid arithmetic is carried as a single-reviewer finding, and the paper evidence it cites was checked (§V-A).

#### Step 2: dispositions (denominator: the four non-DA seats)

| SC | agree (seats) | conflict | silent | Disposition | Roadmap item |
|---|---|---|---|---|---|
| SC-1 | 2 (EIC, R2) | 0 | R1, R3 | CORROBORATED | REV-01 · R1 |
| SC-2 | 1 (EIC) | 0 | R1, R2, R3 | SINGLE-REVIEWER, DA-corroborated | REV-02 · R2 |
| SC-3 | 1 (EIC) | 0 | R1, R2, R3 | SINGLE-REVIEWER | REV-03 · R3 |
| SC-4 | 1 (EIC) | 0 | R1, R2, R3 | SINGLE-REVIEWER, DA-corroborated | REV-04 · R4 |
| SC-5 | 1 (EIC) | 1 (R2, severity) | R1, R3 | SPLIT | REV-05 · R5 |
| SC-6 | 3 (EIC, R2, R3) | 0 | R1 | CONSENSUS-3 | REV-06 · R6 |
| SC-7 | 2 (EIC, R1) | 0 | R2, R3 | CORROBORATED | REV-07 · R7 |
| SC-8 | 1 (EIC) | 0 | R1, R2, R3 | SINGLE-REVIEWER | REV-08 · S1 |
| SC-9 | 2 (EIC, R1) | 0 | R2, R3 | CORROBORATED | REV-09 · R8 |
| SC-10 | 2 (EIC, R3) | 0 | R1, R2 | CORROBORATED | REV-10 · S2 |
| SC-11 | 2 (EIC, R2) | 0 | R1, R3 | CORROBORATED | REV-11 · S3 |
| SC-12 to SC-16 | 1 (EIC) each | 0 | R1, R2, R3 | SINGLE-REVIEWER | REV-12 to REV-16 · S4 to S8 |
| SC-17, SC-18, SC-19 | 1 (R1) each | 0 | EIC, R2, R3 | SINGLE-REVIEWER | REV-17 to REV-19 · R9 to R11 |
| SC-20 | 1 (R1) | 1 (R3, severity) | EIC, R2 | SPLIT | REV-20 · R12 |
| SC-21 | 2 (R1, R3) | 0 | EIC, R2 | CORROBORATED | REV-21 · R13 |
| SC-22, SC-23, SC-24 | 1 (R1) each | 0 | EIC, R2, R3 | SINGLE-REVIEWER | REV-22 to REV-24 · S9 to S11 |
| SC-25 | 2 (R1, R3) | 0 | EIC, R2 | CORROBORATED | REV-25 · S12 |
| SC-26 | 1 (R1) | 0 | EIC, R2, R3 | SINGLE-REVIEWER | REV-26 · S13 |
| SC-27 | 1 (R1) | 0 | EIC, R2, R3 | SINGLE-REVIEWER, DA-corroborated | REV-27 · R14 |
| SC-28, SC-29 | 1 (R1) each | 0 | EIC, R2, R3 | SINGLE-REVIEWER | REV-28, REV-29 · S14, S15 |
| SC-30 | 1 (R1) | 0 | EIC, R2, R3 | SINGLE-REVIEWER | REV-30 · R15 |
| SC-31 | 2 (R1, R3) | 0 | EIC, R2 | CORROBORATED | REV-31 · S16 |
| SC-32 | 1 (R1) | 0 | EIC, R2, R3 | SINGLE-REVIEWER | REV-32 · S17 |
| SC-33, SC-34, SC-35 | 1 (R2) each | 0 | EIC, R1, R3 | SINGLE-REVIEWER | REV-33 to REV-35 · R16 to R18 |
| SC-36, SC-37 | 1 (R2) each | 0 | EIC, R1, R3 | SINGLE-REVIEWER | REV-36, REV-37 · S18, S19 |
| SC-38 | 2 (R2, R3) | 0 | EIC, R1 | CORROBORATED | REV-38 · S20 |
| SC-39, SC-40 | 1 (R2) each | 0 | EIC, R1, R3 | SINGLE-REVIEWER | REV-39, REV-40 · S21, S22 |
| SC-41 | 1 (R2) | 0 | EIC, R1, R3 | SINGLE-REVIEWER, DA-corroborated | REV-41 · S23 |
| SC-42 | 1 (R2) | 0 | EIC, R1, R3 | SINGLE-REVIEWER | REV-42 · S24 |
| SC-43 | 2 (R2, R3) | 0 | EIC, R1 | CORROBORATED | REV-43 · S25 |
| SC-44 | 1 (R2) | 0 | EIC, R1, R3 | SINGLE-REVIEWER | REV-44 · S26 |
| SC-45 | 1 (R3) | 0 | EIC, R1, R2 | SINGLE-REVIEWER, DA-corroborated | REV-45 · R19 |
| SC-46 to SC-51 | 1 (R3) each | 0 | EIC, R1, R2 | SINGLE-REVIEWER | REV-46 to REV-51 · S27 to S32 |

Totals over the 51 sub-claims: CONSENSUS-4: 0; CONSENSUS-3: 1; CORROBORATED: 10; SPLIT: 2; SINGLE-REVIEWER: 38, of which 5 are DA-corroborated. DA-CRITICAL: 0.

#### Points of Agreement (Consensus)

- [CONSENSUS-4] None.
- [CONSENSUS-3] SC-6: the abstract states the 89% recovered by one scale per phase without saying that the phase labels come from the logged truth, so a reader can take it for an information-free baseline (EIC W4, R2 W9, R3 W3; R1 is silent). DA M3 reports the same sub-claim. → REV-06 (R6).

#### Below the Consensus Bar (#1100)

Few seats does not mean low importance: obligation follows the named criterion and the anchored evidence. Each DA-corroborated label below means that the DA reports the same sub-claim. The DA is not an independent seat and does not change the count.

- [CORROBORATED] EIC, R2 — the null is measured in a regime that seldom leaves steady tracking (10 of 8,290 young tracks; few missed updates; clean simulated sensing), and the paper does not state the condition under which its steady-state argument holds — SC-1 (DA M1 also reports it)
- [CORROBORATED] EIC, R1 — the abstract and contributions 2 and 4 do not label the analyses added after the first results — SC-7 (DA M5 also reports it)
- [CORROBORATED] EIC, R1 — the null is worded as absence ("none that we can measure"; "does as well") where the body reports a bound — SC-9
- [CORROBORATED] EIC, R3 — no constant time-gap margin among the compared sources — SC-10
- [CORROBORATED] EIC, R2 — the §II positioning and its no-prior-evaluation sentence rest on [41]–[52] read from abstracts only — SC-11
- [CORROBORATED] R1, R3 — the 89% is an in-sample envelope whose selection optimism is not quantified — SC-21 (DA M3 also reports it)
- [CORROBORATED] R1, R3 — "independent" verification is qualified (parts not blind; the authorship of the second programs is not stated) — SC-25
- [CORROBORATED] R1, R3 — the raw recordings are available only on request — SC-31
- [CORROBORATED] R2, R3 — the margin scale g is mapped to a spacing policy rather than to the chance-constraint parameter — SC-38
- [CORROBORATED] R2, R3 — the room is mapped to the value of perfect information, although E is a reference, not a bound — SC-43
- [SINGLE-REVIEWER] EIC — contribution 3 is mostly a measured confirmation of the steady state — SC-2
  - DA-corroborated (M1). Severities: EIC major; DA major.
- [SINGLE-REVIEWER] EIC — the abstract does not say that track births, missed updates and real sensing are untested — SC-3
- [SINGLE-REVIEWER] EIC — the design is shown to grade partial information on pooled decisions only, and contribution 1 and the abstract omit this — SC-4
  - DA-corroborated (M2). Severities: EIC minor; DA major.
- [SINGLE-REVIEWER] EIC — "35 runs not used to design the margins" implies a cleaner hold-out than exists — SC-8
- [SINGLE-REVIEWER] EIC — main text likely 12–13 typeset pages against a 10-page recommendation — SC-12
- [SINGLE-REVIEWER] EIC — the results prose is dense enough to bury the findings — SC-13
- [SINGLE-REVIEWER] EIC — the symbol D is not defined in the main text — SC-14
- [SINGLE-REVIEWER] EIC — Table II carries signed caution as both a column and a row — SC-15
- [SINGLE-REVIEWER] EIC — a hard-to-parse sentence in the Abstract and §I — SC-16
- [SINGLE-REVIEWER] R1 — the non-smoothness of RR(N) is plausibly a grid-interleaving artefact — SC-17
- [SINGLE-REVIEWER] R1 — the double-bootstrap calibration of RR(N)'s interval is not justified — SC-18
- [SINGLE-REVIEWER] R1 — the main text omits the tuning-run room, commitment ratio and braking-prediction share — SC-19
- [SINGLE-REVIEWER] R1 — the 0.5% bound was not fixed before the values were read — SC-22
- [SINGLE-REVIEWER] R1 — "slightly narrow" understates the undercoverage of N's shares — SC-23
- [SINGLE-REVIEWER] R1 — the S10 amendment's hash and date are not printed — SC-24
- [SINGLE-REVIEWER] R1 — a secondary equivalence (Spearman's ρ) is read from overlapping marginal intervals — SC-26
- [SINGLE-REVIEWER] R1 — shares are interpreted in populations where the paper's own grading check fails — SC-27
  - DA-corroborated (M4). Severities: R1 minor; DA major.
- [SINGLE-REVIEWER] R1 — the frontier-construction alternates for CK3 and AM appear only in Table S5 — SC-28
- [SINGLE-REVIEWER] R1 — under reaction-and-stop scoring, the caution axis is defined by the 3 s scoring — SC-29
- [SINGLE-REVIEWER] R1 — the deposit does not yet exist for review — SC-30
- [SINGLE-REVIEWER] R1 — §III-B singles out N as on-policy, though N is also off-policy — SC-32
- [SINGLE-REVIEWER] R2 — the tracker is described as linear but is run as an EKF with object-frame noise; the frame of P̄ and how it was formed are unstated — SC-33
- [SINGLE-REVIEWER] R2 — "not expected to carry over" reads more into the cross-family ratio variation than the check supports — SC-34
- [SINGLE-REVIEWER] R2 — the per-phase and after-stop findings lack a physical mechanism — SC-35
- [SINGLE-REVIEWER] R2 — the NIS-inflated source tests little, and its trigger checks the position block — SC-36
- [SINGLE-REVIEWER] R2 — the 1.10 is a ratio that depends on look-ahead, not one constant — SC-37
- [SINGLE-REVIEWER] R2 — stochastic-MPC car-following and fading-factor filtering literature is missing — SC-39
- [SINGLE-REVIEWER] R2 — [17] is summarised loosely — SC-40
- [SINGLE-REVIEWER] R2 — Supplement S8.1–S8.2 keep wording the main text has withdrawn — SC-41
  - DA-corroborated (M5, Table S4 portion). Severities: R2 minor; DA major.
- [SINGLE-REVIEWER] R2 — the direction in which test-bed simplifications move the room is not discussed — SC-42
- [SINGLE-REVIEWER] R2 — the main text could say that Table S26's tuning-only column shows the same pattern as Table V — SC-44
- [SINGLE-REVIEWER] R3 — the stop-reliant practical reading omits following traffic and fallback reliability — SC-45
  - DA-corroborated (M6). Severities: R3 minor; DA major.
- [SINGLE-REVIEWER] R3 — the allocation finding is not connected to a rule a planner could run — SC-46
- [SINGLE-REVIEWER] R3 — §V-D gives performance model 2's 2 m a normative register — SC-47
- [SINGLE-REVIEWER] R3 — "legal following distance" is used for R157's minimum following distance — SC-48
- [SINGLE-REVIEWER] R3 — the abstract's 12% uses a stop harder than the planner's own fallback — SC-49
- [SINGLE-REVIEWER] R3 — wrong-go counts ignore severity — SC-50
- [SINGLE-REVIEWER] R3 — the described deposit omits the all-family arrays behind contribution 4, the capture scripts and the S3 simulator — SC-51

#### Points of Disagreement

**Disagreement 1: severity of the population-mix statement (SC-5)**
- **EIC view**: the abstract closes by asking open-loop scores to state their commitment and population, yet it does not state its own population; this is a minor abstract-reporting defect (EIC W3, minor).
- **R2 view**: the scope should say that most decisions are a standstill queue rather than following in motion; this is part of R2's major finding that the per-phase and after-stop results lack a mechanism (R2 W2, major, transported to every sub-claim of that parent).
- **Disagreement type**: Severity disagreement. Both seats agree the problem exists, and the remedy is the same.
- **Editor's Resolution**: required (`must_fix`, REV-05 · R5). Both transported severities stay visible on the roadmap row.
- **Resolution Rationale**: the evidence settles the obligation without picking a severity. The paper's own closing lesson asks for the population to be stated, and §III-A gives the mix (82.7% after the stop; 77.5% with the ego at or below 0.5 m/s). R2's major severity attaches to its mechanism finding, which is carried separately as REV-35 (R18). The requested action is the same either way.

**Disagreement 2: severity of the recording-policy condition (SC-20)**
- **R1 view**: on the 20 tuning runs, recorded under another planner, the room is 1.18 rather than 5.56 points, the commitment ratio 0.023 rather than 0.121, and the braking prediction's share 0.377 rather than 0.831 (Tables S2, S25(b)). The paper's lesson about conditional open-loop scores must therefore add the data-collecting policy (R1 W2, major).
- **R3 view**: the recording planner ended 5 of 35 evaluation runs and 10 of 20 tuning runs at contact, so only relative comparisons between sources should be claimed to transfer; one sentence in the Limits suffices (R3 W10, minor).
- **Disagreement type**: Severity disagreement; the remedies are compatible.
- **Editor's Resolution**: required (`must_fix`, REV-20 · R12). R3's Limits sentence is accepted as part of the fix.
- **Resolution Rationale**: by the expertise principle, how magnitudes depend on the data-collecting policy is a methodology question, and R1's values are read and recomputed from the supplement's tables (evidence first). The design cannot separate the recording planner from scenario draws (R1 W2), so the paper must state the condition, not a cause.

**Apparent tensions examined and not recorded as disputes**
- *Clean sensing and the null (EIC W1, R2 W10).* R2 says the covariance null is robust to the listed idealisations and that no new runs are needed for the core claim. EIC says the regime that could give the covariance value (births, misses) is seldom visited. Both seats ask for the same minimum remedy: state the steady-tracking condition (EIC W1; R2 W1). Both treat new recordings as optional. On the paper's evidence, a fixed-noise filter's covariance does not depend on measured values (§II), so the noise level alone does not move it, but missed updates do (1.68 after two missed updates, Table S27, cited by EIC). REV-01 therefore names missed updates and births, and new runs remain the author's choice.
- *Which bound the abstract should state (EIC W5, R1 W1/W4).* EIC's suggested wording cites the calibrated interval and the 0.5% bound. R1 questions that interval's coverage and when the 0.5% was chosen. EIC declares interval validity outside its remit, so this is not a dispute. By the expertise principle, the bound's statistical form follows R1 (REV-17, REV-18, REV-22), and REV-09 requires a bound rather than "none".
- *Hold-out for the per-phase scales (R1 W3, R3 W3, DA M3).* R3 and the DA suggest the 20 tuning runs. R1 asks for leave-runs-out within the evaluation runs, because the tuning runs differ in recording planner (R1 W2). R3 also lists leave-runs-out, so the acceptance basis for REV-21 is leave-runs-out; a tuning-run selection may be added.
- *Steady-state confirmation as a strength (R2 S1) or as weak significance (EIC W1, DA M1).* This is a perspective difference. R2 does not oppose recasting contribution 3, and the recast (REV-02) keeps the direct confirmation R2 credits (Tables S14, S15).
- *The ratio check's reach (R1 S4, R3 S3 and S9, R2 W1).* R1 credits the "untested at decision level" label and R3 the §VI deployment sentence. R2 objects only to "not expected to carry over" in §V-E and contribution 4 and accepts §VI's "silent". No seat defends the §V-E wording.
- *Spearman comparison (R1 W7, R2 S5).* R2 endorses the conclusion, and R1 calls it "probably right" but asks for a paired interval. The two positions are compatible.
- *Recommendation spread.* EIC signals major revision, R2 recommends Major Revision, R3 recommends Minor Revision, and R1 states no recommendation. Under the sprint contract, seat recommendations do not enter the decision. R3's Minor Revision is recorded. On the two sub-claims where the DA reports what R3 raised (SC-45; SC-21/SC-6 through M3), the DA bands them MAJOR and R3 tags them minor. Both severities are shown, and the DA is not counted.

### Devil's Advocate Findings

- **CRITICAL**: none, so `da_critical_adjudications` is empty and no adjudication, rejection rationale or accept-blocking marker applies.
- **MAJOR rows**: each maps to non-DA sub-claims and travels as a corroborating source, not as a vote. M1 → SC-1, SC-2 (REV-01, REV-02); M2 → SC-4 (REV-04); M3 → SC-6, SC-21 (REV-06, REV-21); M4 → SC-27 (REV-27); M5 → SC-7, SC-41 (REV-07, REV-41); M6 → SC-45 (REV-45).
- **DA content without a non-DA counterpart.** Under #1098 this content creates no roadmap item, but the response letter should answer it:
  - The locked plan's fixed sentence on the NIS-inflated covariance was dropped from the abstract, and DA M5 asks for it to be restored or explicitly recorded; REV-41 carries only the stale-record portion.
  - §V-B explains the NIS-inflated covariance's inaction by "the covariance is already too wide", but Supplement S9 shows the propagated deviation is too narrow while the lead brakes (RMS z 3.17 to 5.89 at 1–3 s).
  - The uniform weighting of the 201 caution levels is not defended; the DA addresses this to the methodology seat, and R1 Q6 asks a related question without raising a weakness.
  - Contribution 4's "nearly constant" is a row-pooled statistic, and for the stopped-vehicle and cut-in families the paper does not show that the decision-critical rows lie inside the 5% band.
  - The analytic steady-state Riccati route is not used as a baseline.
  - By §V-C's own logic, the null is a within-family statement.

### Decision Rationale

The sprint contract sets the decision mechanically. Every assessed score is warn: D1 (R1), D2 (R2), D3 (R1, DA), D4 (R3), D5 and D6 (EIC). No seat scored block, so F1, F2 and F4 do not fire. F3 fires because all four mandatory dimensions (D1, D2, D3, D6) score warn under the majority quantifier, where two are required. F5 fires because at least one dimension scores warn. F3 (severity 70) outranks F5 (severity 40), so the action is major revision. The Devil's Advocate raised no CRITICAL issue, so no DA adjudication bears on the decision.

The decision agrees with the seats' own reading. EIC signals major revision, R2 recommends Major Revision, R3 recommends Minor Revision, and R1 states none. No seat doubts the central null: R1 calls it robust, R2 finds no domain error carrying it, and the DA finds no data–conclusion mismatch. What needs a second round is the claims built around the null:
- whether the abstract's interval for the tracker covariance's share has a demonstrated coverage property (R1 W1);
- how the headline magnitudes move with the recording planner (R1 W2, R3 W10);
- the tracking regime and the filter description that bound contribution 3 and the cross-family reach claim (EIC W1, R2 W1, DA M1);
- the physical mechanism behind the per-phase and after-stop figures (R2 W2);
- the fences the abstract omits: population mix, truth-labelled phases and post hoc analyses.

Several required items need re-analysis of stored arrays, which the re-review must verify. A stricter decision is not warranted: no seat found a fatal or unrepairable defect, and the cards report that the null survives every variant scored. A lighter decision is not available once F3 fires.

### Blocking Issues (0–3, immutable source order)

| Transport ref | Blocking issue | Source reviewer(s) | Evidence anchor | Resolving roadmap item |
|---|---|---|---|---|
| R1 | The null's scope: the evaluated population seldom leaves steady tracking, and §I, contribution 3 and the abstract do not say so | EIC (W1), R2 (W1); DA M1 corroborating | `text: §I "It still has to be measured: the covariance also depends on detections, misses and track age"` | REV-01 (R1), REV-02 (R2), REV-03 (R3) |
| R9 | The abstract's calibrated interval for RR(N) lacks a demonstrated coverage property, and the non-smoothness may be a grid-interleaving artefact | R1 (W1) | `text: §V-A "The step-frontier statistic is non-smooth, and nominal 95% intervals are not valid for it"` | REV-17 (R9), REV-18 (R10) |
| R11 | The headline magnitudes (5.6 points, 12%, 83%) are several times smaller on runs recorded under another planner; the main text omits this and does not name the recording policy as a condition | R1 (W2), R3 (W10) | `table: Supplement Table S2, tuning and evaluation columns` | REV-19 (R11), REV-20 (R12) |

These three issues bear on the abstract's headline quantities and carry major transported severity. The other twelve required items (R4–R8, R13–R19) block acceptance equally; the table is capped at three by the template.

### Required Item Details

> **Ordinal contract (#576/#670):** `R<n>` is a transport reference, never a work rank. Numbering follows the immutable roadmap's source-traceability order filtered to `obligation_class == must_fix`. Required blocks are exactly R1..R19.

**R1: Scope the null to the steady-tracking regime (REV-01)**
- **Problem**: The Introduction justifies measuring an expected null because the covariance "also depends on detections, misses and track age", but the evaluated decisions barely exercise those dependences: 10 of 8,290 decisions have a young track, the median run-mean NIS is 0.24 against 2, and sensing is clean and simulated. Where misses do occur the ratio departs from the constant (1.68 after two missed updates, Table S27). The paper never states that its steady-state argument holds only with regular updates, no misses and fixed geometry.
- **Source**: EIC W1 (major, confidence 3); R2 W1 (major, 3); DA M1 corroborating, not counted.
- **Requirement**: Rewrite the §I justification, contribution 3 and the steady-state statements in §II and §VI to say that the null is measured in the steady-tracking regime under clean simulated sensing, naming missed updates and track births as conditions not exercised. Optional, at the author's choice (EIC W1): re-run the tracker offline on the logged detections with controlled drop-outs and score the result, or add a degraded-perception condition.
- **Acceptance criteria**: §I, contribution 3, §II and §VI each state the steady-tracking condition (regular updates, no misses or births, fixed geometry) under which the null was measured, and any optional drop-out analysis is labelled open-loop and off-policy.

**R2: Recast contribution 3 as a measured confirmation (REV-02)**
- **Problem**: As written, contribution 3 is mostly a measured confirmation of the steady state that §II attributes to the Riccati recursion (EIC W1). The DA adds that in this population the decision-level null is implied by the ratio of Fig. 2(b) and the swept scale (M1).
- **Source**: EIC W1 (major, 3); DA M1 corroborating.
- **Requirement**: Recast contribution 3, and its echo in §VII, as a measured confirmation in this population of what the steady state predicts, stating what the decision-level measurement adds (EIC Significance: the measured scale, 0.6 of 8,290 decisions).
- **Acceptance criteria**: Contribution 3 and §VII present the tracker null as a measured confirmation of the steady-state prediction in this population, not as an open test.

**R3: Abstract fence on births, misses and real sensing (REV-03)**
- **Problem**: The abstract does not say that track births, missed updates and real sensing are untested.
- **Source**: EIC W1 (major, 3), minimum remedy.
- **Requirement**: Add one clause to the abstract within the 250-word limit; rewriting the CARLA sentence (S8) frees words.
- **Acceptance criteria**: The abstract names track births, missed updates and real sensing as untested, and its length stays at or under 250 words.

**R4: State that the design grades information on pooled decisions only (REV-04)**
- **Problem**: The graded oracles grade pooled decisions (0.27, 0.54, 0.78) but not while the lead brakes (−0.68, −0.63, 0.05) or with the ego moving (−0.11, 0.05, 0.44; Table II, Table S12b), and the pooled population is 82.7% after-stop. Contribution 1, §IV-B's "not a blunt measure" and the abstract present the design without this qualifier.
- **Source**: EIC W2 (minor, 3); DA M2 corroborating (major band, 4).
- **Requirement**: State in contribution 1, §IV-B, §VII and one clause of the abstract that the design is shown to grade information on pooled decisions only. Optional (EIC W2; DA M2): report whether the partial oracles grade once each phase has its own scale, using the Table S23 machinery on stored arrays.
- **Acceptance criteria**: Contribution 1, §IV-B, §VII and the abstract each carry the pooled-only qualifier, and any per-phase grading result is reported with its population.

**R5: State the population mix beside the headline numbers (REV-05; SPLIT, arbitrated)**
- **Problem**: The abstract asks open-loop scores to state their population but does not state its own. Of the evaluated decisions, 82.7% come after the lead's stop and 77.5% have the ego at or below 0.5 m/s, and the room and the braking prediction's share move with that mix (Table S22).
- **Source**: EIC W3 (minor, 4); R2 W2 (major, 3). See Disagreement 1.
- **Requirement**: Add a clause to the abstract sentence that gives 5.6 points, and a sentence to the §I Scope, saying that most evaluated decisions follow the lead's stop with the ego nearly at rest.
- **Acceptance criteria**: The abstract and the §I Scope both state the share of evaluated decisions taken after the lead's stop with the ego nearly at rest.

**R6: Truth-derived phase labels for the 89% (REV-06)**
- **Problem**: §V-C says a scale per phase uses phase labels from the logged truth and that no realisable rule was tested, but the abstract and contribution 2 state the 89% without that qualifier.
- **Source**: EIC W4(a) (minor, 4); R2 W9 (minor, 4); R3 W3 (minor, 3); R1 silent; DA M3 corroborating.
- **Requirement**: Add "with the phase taken from the logged truth", or equivalent, to the abstract's 89% sentence and to contribution 2.
- **Acceptance criteria**: Every statement of the 89% in the abstract and in contribution 2 says that the phase labels come from the logged truth.

**R7: Label the analyses added after the first results (REV-07)**
- **Problem**: The 89%, 29%, 12%, the family ratio check and the calibrated intervals come from the second plan and from Supplement S10, which were added after the first results. §IV-D and §VII say so; the abstract and the contribution list do not.
- **Source**: EIC W4(b) (minor, 4); R1 W6 (minor, 4); DA M5 corroborating.
- **Requirement**: Mark contributions 2 and 4, and the corresponding abstract sentences, as exploratory analyses added after the first results.
- **Acceptance criteria**: The abstract and contributions 2 and 4 identify which quantitative statements come from analyses added after the first results.

**R8: Word the null as a bound, not as absence (REV-09)**
- **Problem**: The abstract and §VII say the tracker's covariance recovers "none of the room that we can measure", and the Discussion says a class average "does as well". The body reports a bound, the basic interval and every subsampling interval lie above zero, and Table S4 records the plan's rule that this share is never to be printed as not distinguishable from zero.
- **Source**: EIC W5 (minor, 3); R1 W4 (minor, 4).
- **Requirement**: Replace the absence wording in the abstract, §VI and §VII with the bound reported in §V-A, in the form settled by R9, R10 and S9: for example the largest upper end across interval methods (2.2 of 8,290 decisions), or equivalence within a margin justified in decision units.
- **Acceptance criteria**: No sentence in the abstract, §VI or §VII states or implies that the share is zero or indistinguishable from zero, and each such sentence gives the bound with its interval basis.

**R9: Separate the covariance's information effect from grid phase (REV-17)**
- **Problem**: N's margin is 1.1029 times F0's on 99.26% of binding rows, so N's operating points sample F0's path 3.40 steps along the log-spaced grid. RR(N)'s non-smooth full-sample value (97.7th percentile of its bootstrap distribution, whose median is 0.0001) looks like discretisation jitter rather than information.
- **Source**: R1 W1 (major, 4).
- **Requirement**: Add a placebo source, F0 with its variance multiplied by 1.1029², and report RR(N) − RR(placebo) as the covariance's information effect, or compute every frontier exactly from the per-decision critical scales g*.
- **Acceptance criteria**: §V-A reports a placebo-adjusted or grid-free RR(N) with its interval, computed on the stored arrays.

**R10: Justify or replace the double-bootstrap calibration (REV-18)**
- **Problem**: The calibrated level 0.996 is read from the second-smallest and second-largest of 1,000 inner values with no Monte Carlo error, and the subsampling upper ends rise with m (0.0033, 0.0038, 0.0047). If the non-smoothness is a grid artefact, the calibration covers an artefact. The abstract's "calibrated interval −0.2% to 0.2%" therefore lacks a demonstrated coverage property.
- **Source**: R1 W1 (major, 4).
- **Requirement**: Report the Monte Carlo error of the calibrated level, or use an m-out-of-n bootstrap with an estimated rate. Until coverage is shown, or the statistic is made grid-free by R9, do not present the calibrated interval as having nominal coverage.
- **Acceptance criteria**: The interval for RR(N) printed in the abstract and §V-A either carries a demonstrated coverage basis (Monte Carlo error or rate-estimated subsampling) or is replaced by the interval of the R9 statistic.

**R11: Report the tuning-run values beside the evaluation-run values (REV-19)**
- **Problem**: On the 20 tuning runs the 3 s room is 1.18 points against 5.56, the room left with a 0.75 s stop is 0.023 of the 3 s room against 0.121, and the braking prediction's pooled share is 0.377 [−0.204, 0.840] against 0.831 (Tables S2, S25(b)). None of these appears in the main text, and the main text does not cite Table S2.
- **Source**: R1 W2 (major, 4).
- **Requirement**: Report these values beside the evaluation-run values in §V-A, §V-B and §V-D and cite Table S2. If feasible, decompose the gap by phase mix and by contact-terminated runs, as Table S22 does for the after-stop segment.
- **Acceptance criteria**: §V-A, §V-B and §V-D print the tuning-run room, commitment ratio and braking-prediction share beside the evaluation-run values and cite Table S2.

**R12: Name the recording planner as a condition of the magnitudes (REV-20; SPLIT, arbitrated)**
- **Problem**: The paper's lesson that an open-loop score should state its commitment and its population mix omits the data-collecting policy, which Tables S2 and S3 show matters as much (R1). The recording planner ended 5 of 35 evaluation runs and 10 of 20 tuning runs at contact, which limits what the absolute quantities say about a deployed stack (R3).
- **Source**: R1 W2 (major, 4); R3 W10 (minor, 3). See Disagreement 2.
- **Requirement**: Add the recording policy to the conditions named in the abstract's closing lesson, in §VI and in §VII, and add to the Limits that only relative comparisons between sources are meant to transfer.
- **Acceptance criteria**: The abstract, §VI, §VII and the Limits name the recording planner as a condition of the reported magnitudes, and the Limits restrict transfer to relative comparisons between sources.

**R13: Quantify the in-sample optimism of the 89% (REV-21)**
- **Problem**: The per-phase frontier is the envelope over 202³ (about 8.2 million) scale triples, chosen with outcome knowledge on the evaluation runs. The 400-resample bootstrap re-optimises in each resample, so it does not remove the selection optimism.
- **Source**: R1 W3 (minor, 3); R3 W3 (minor, 3); DA M3 corroborating.
- **Requirement**: Choose the per-phase scale ratios out of sample by leaving runs out within the evaluation runs, and report the held-out gain beside 0.89. A tuning-run selection may be added but cannot by itself separate optimism from the run-set difference of R11. Label 0.89 as an in-sample upper value in the abstract, contribution 2 and §V-C.
- **Acceptance criteria**: §V-C reports a held-out per-phase gain beside 0.89, and every printed 89% is labelled as in-sample.

**R14: Apply the paper's grading rule wherever shares are interpreted (REV-27)**
- **Problem**: §VI asks that a measure be shown to grade partial information "in every population whose shares are interpreted". Yet §V-B, §V-D and §VI read the braking prediction's shares with the ego moving and while the lead brakes (0.47, 0.61; signed 0.30, 0.35; 0.04 and −0.89), where the partial oracles do not grade (Table II, Table S12). DA M4 adds the per-phase remaining-room shares (Table S23) and the before-stop 29% (Table S22).
- **Source**: R1 W8 (minor, 4); DA M4 corroborating (major band, 4).
- **Requirement**: Attach §IV-B's reading (there, a share measures what one margin scale can use) to each such sentence, or give those qualifiers in decision-equivalents. DA M4's alternative is to run the partial oracles on those populations.
- **Acceptance criteria**: Every share interpreted in a population without demonstrated grading carries the §IV-B reading, is given in decision-equivalents, or is accompanied by a reported grading check for that population.

**R15: Create the deposit and give reviewers access (REV-30)**
- **Problem**: The deposit described in Data and Code Availability (both plans with hashes, per-decision arrays, second programs, result files) does not yet exist, and the planner library is an in-house re-implementation. R1 judges that the described deposit would suffice to regenerate every number once it exists.
- **Source**: R1 W11 (minor, 4).
- **Requirement**: Create the deposit and give reviewers a link they can access with the revision. Filling in the repository name and DOI is an author-only submission gate, tracked separately.
- **Acceptance criteria**: At re-review, reviewers can access the plans with hashes, the per-decision arrays, the second programs and the result files.

**R16: Describe the tracker as it is run (REV-33)**
- **Problem**: §I, Fig. 1 and §III-A call CANMOT a constant-velocity Kalman filter, and §II and §VI argue from a linear time-invariant filter. Table S28 says it is run as an extended Kalman filter with a constant-velocity model in the object frame. Neither the frame of the class-average covariance P̄ nor how P̄ was formed is stated.
- **Source**: R2 W1 (major, 3).
- **Requirement**: Describe the filter as run in §III-A and wherever it is named: an EKF; the frames of the state, the noise and P̄; and whether P̄ is the mean of logged covariances or the second moment of realised errors.
- **Acceptance criteria**: §III-A, and §I, §II and the Fig. 1 caption where the filter is named, describe the EKF, the frames of state, noise and P̄, and how P̄ was formed.

**R17: Reword the cross-family reach claim to "silent" (REV-34)**
- **Problem**: In the crossing and benign families, the ratio to a fixed class average can vary simply because a fixed object-frame covariance is rotated against it, with no per-decision information in the variation. §V-E and contribution 4's "not expected to carry over" read more into this than the check supports; §VI's "silent" is the accurate statement.
- **Source**: R2 W1 (major, 3).
- **Requirement**: Reword §V-E and contribution 4 to say that the check is silent on those families. Optional: repeat Table V on stored arrays against a heading-aligned class average (P̄ rotated by each track's heading).
- **Acceptance criteria**: §V-E and contribution 4 state no expectation for other families beyond what the ratio check shows, and any heading-aligned analysis is reported in Table V or the supplement.

**R18: Give the per-phase and after-stop findings a physical mechanism (REV-35)**
- **Problem**: The braking prediction's share rises from 0.29 to 0.83 as after-stop decisions are added (Table S22), and after the stop it recovers 0.99 of that phase's room (Table S5). No analysis shows why a wrong go occurs behind a lead at rest. Without a mechanism, the 83%, the 89% and the motion-state conclusion of §VI and §VII cannot be transferred, and they may partly reflect a tracker artefact on stationary targets.
- **Source**: R2 W2 (major, 3).
- **Requirement**: On stored arrays, report the tracker's estimated lead speed and acceleration around the braking onset and against time since the stop, tabulate the rows selected in after-stop wrong-go decisions, and state the mechanism in §V-C.
- **Acceptance criteria**: §V-C states the mechanism and cites a table or figure of the estimated lead state against time since the stop and of the rows selected in after-stop wrong-go decisions.

**R19: Name the unscored safety costs in the stop-branch reading (REV-45)**
- **Problem**: §VI says that, under a reliable stop, "the choice of source matters mainly for comfort and progress". The reaction-and-stop scoring assumes an unconditional, perfectly executed 6 m/s² stop and counts only ego–lead contact. Traffic behind the ego is outside the evaluation, and the fallback's reliability is assumed perfect.
- **Source**: R3 W1 (minor, 4); DA M6 corroborating (major band, 3).
- **Requirement**: In §VI and in the stop branch of §VII, restrict the statement to ego–lead contact, and name following-traffic exposure and fallback reliability as unscored safety costs. Stronger (R3, DA): report per source, at matched caution, the share of decisions whose selected row is unsafe under the 3 s commitment but safe under reaction-and-stop scoring.
- **Acceptance criteria**: §VI and §VII no longer reduce the stop-branch consequences to comfort and progress, and they name following traffic and fallback reliability as unscored.

### Submission gates and editorial requests (not scientific findings; not roadmap items)

- Author block (manuscript line 5): an author-only placeholder, to be filled before submission (EIC Submission Gates).
- Repository name and DOI in Data and Code Availability: an author-only placeholder (EIC; R3 W11 excludes it from its finding). Creating the deposit and giving reviewers access is REV-30 (R15).
- AI-use statement (Acknowledgment): EIC says it appears to meet IEEE's disclosure requirement and asks the editorial office to confirm it against the policy in force. R3 S7 concurs on substance.
- Related manuscript [9]: disclosed. EIC Q1 asks the author to give the editor a confidential copy for an overlap check and to confirm that no run, table or figure is shared. R2 W10 notes that the tracker configuration is shared with [9].

### Journal-Supplied Deadline (Optional Transport)

- **Exact deadline from source letter**: NOT PROVIDED. No deadline, duration or work estimate is inferred.

### Closing

We encourage you to consider the reviewers' comments carefully and to submit a substantially revised manuscript. The revised manuscript will undergo another round of review, which will verify the nineteen required items against their acceptance criteria.

The Editor (simulated synthesis)

---

## Part 2: Revision Roadmap

> The `Sub-Claim(s)` column carries the Step 1b `sub_claim_id` each item traces to. Item IDs `REV-nn` match `SC-nn`. Rows follow immutable source order: seat order EIC, R1, R2, R3, then the weakness ordinal, then the sub-claim ordinal. Severity, obligation and cost never set the order.
>
> **Obligation classes** are editorial gates set by this synthesis, not ranks, and they are not derived from severity or confidence. `must_fix`: an item on which a mandatory-dimension warn rests and which bears on the abstract's or contributions' claims, or on reviewer verification before acceptance. `should_fix`: a concrete defect whose repair is expected in this revision but which does not by itself bear on a headline claim. `consider`: an optional addition.
>
> **Machine core**: the closed `revision-roadmap/1.1` JSON core is not emitted in this file. No block manifest was bound to this run, so `block_manifest_sha256`, `base_draft_sha256` and the exact `proposed_targets[]` block IDs cannot be filled without fabrication. Each row carries the schema's closed consequence codes and typed cost scopes, so the core can be built by `scripts/revision_roadmap.py` once a manifest exists. DA rows travel as `corroborating_sources[]` and never change `consensus_level` or obligation.

### Required Revisions (Must Fix)

| Transport ref | Revision Item (location → fix) | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source | Consensus level | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 | REV-01. **Location:** §I justification, contribution 3, §II and §VI steady-state statements. **Fix:** state that the null is measured in the steady-tracking regime under clean simulated sensing (regular updates, no misses or births, fixed geometry); optional offline drop-out re-run or degraded-perception condition | SC-1 | EIC major; R2 major | `text: §I "It still has to be measured: the covariance also depends on detections, misses and track age"` | EIC 3; R2 3 | EIC W1; R2 W1; DA M1 (corroborating source: major band, conf 4) | CORROBORATED | must_fix | `section` — §I, §II, §VI | `claim_scope_unsupported` → claim: contribution 3 |
| R2 | REV-02. **Location:** §I contribution 3; §VII. **Fix:** recast as a measured confirmation, in this population, of the steady-state prediction | SC-2 | EIC major (DA major) | `text: §I "It still has to be measured…"` | EIC 3 (DA 4) | EIC W1; DA M1 (corroborating) | SINGLE-REVIEWER | must_fix | `sentence` — §I contribution 3; §VII | `claim_scope_unsupported` → claim: contribution 3 |
| R3 | REV-03. **Location:** Abstract. **Fix:** one clause saying track births, missed updates and real sensing are untested, within 250 words | SC-3 | EIC major | `text: §I "It still has to be measured…"` | EIC 3 | EIC W1 | SINGLE-REVIEWER | must_fix | `sentence` — Abstract | `claim_scope_unsupported` → section: Abstract |
| R4 | REV-04. **Location:** §I contribution 1; §IV-B; §VII; Abstract. **Fix:** state that the design grades information on pooled decisions only; optional per-phase grading check | SC-4 | EIC minor (DA major) | `text: §IV-B "Within the lead-braking phase and with the ego moving, the same mixtures can score below the class average"` | EIC 3 (DA 4) | EIC W2; DA M2 (corroborating) | SINGLE-REVIEWER | must_fix | `sentence` — §I contribution 1; §IV-B; §VII; Abstract | `claim_scope_unsupported` → claim: contribution 1 |
| R5 | REV-05. **Location:** Abstract sentence giving 5.6 points; §I Scope. **Fix:** state that most evaluated decisions follow the lead's stop with the ego nearly at rest | SC-5 | EIC minor; R2 major (SPLIT) | `text: §III-A "Of the evaluated decisions, 77.5% have the ego at or below 0.5 m/s, and 82.7% come after the lead has stopped."` | EIC 4; R2 3 | EIC W3; R2 W2 | SPLIT | must_fix | `sentence` — Abstract; §I Scope | `interpretive_ambiguity_remains` → section: Abstract |
| R6 | REV-06. **Location:** Abstract 89% sentence; §I contribution 2. **Fix:** add "with the phase taken from the logged truth" | SC-6 | minor (EIC, R2, R3) (DA major) | `text: Abstract "A class-average margin with one scale per phase of the lead's motion recovers 89% of the room"` | EIC 4; R2 4; R3 3 (DA 3) | EIC W4; R2 W9; R3 W3; DA M3 (corroborating) | CONSENSUS-3 | must_fix | `sentence` — Abstract; §I contribution 2 | `claim_scope_unsupported` → claim: 89% (contribution 2) |
| R7 | REV-07. **Location:** Abstract; §I contributions 2 and 4. **Fix:** label the statements resting on the second plan and Supplement S10 as exploratory analyses added after the first results | SC-7 | minor (EIC, R1) (DA major) | `text: §IV-D "The analyses of Supplement S10 were added last, each defined before its values were read."` | EIC 4; R1 4 (DA 4) | EIC W4; R1 W6; DA M5 (corroborating) | CORROBORATED | must_fix | `sentence` — Abstract; §I contributions 2 and 4 | `reporting_requirement_unmet` → section: Abstract |
| R8 | REV-09. **Location:** Abstract; §VI; §VII. **Fix:** replace "none of the room that we can measure" and "does as well" with the §V-A bound, in the form settled by R9, R10 and S9 | SC-9 | minor (EIC, R1) | `text: Abstract "recovers none of the room that we can measure (0.1%; calibrated interval −0.2% to 0.2%)"` | EIC 3; R1 4 | EIC W5; R1 W4 | CORROBORATED | must_fix | `sentence` — Abstract; §VI; §VII | `claim_scope_unsupported` → claim: the null (Abstract, §VII) |
| R9 | REV-17. **Location:** §V-A; Supplement S10.1. **Fix:** placebo source F0 × 1.1029² and RR(N) − RR(placebo), or frontiers computed exactly from per-decision critical scales g* | SC-17 | R1 major | `text: §V-A "The step-frontier statistic is non-smooth, and nominal 95% intervals are not valid for it"` | R1 4 | R1 W1 | SINGLE-REVIEWER | must_fix | `re_analysis` — stored per-decision arrays; §V-A; Supplement S10.1 | `evidence_gap_remains` → claim: RR(N) (§V-A) |
| R10 | REV-18. **Location:** Abstract; §V-A; Supplement S10.1, Tables S16–S17. **Fix:** report the Monte Carlo error of the calibrated level, or an m-out-of-n bootstrap with an estimated rate; do not present the calibrated interval as nominal until coverage is shown | SC-18 | R1 major | `text: §V-A "The step-frontier statistic is non-smooth, and nominal 95% intervals are not valid for it"` | R1 4 | R1 W1 | SINGLE-REVIEWER | must_fix | `re_analysis` — Supplement S10.1; Tables S16–S17 | `evidence_gap_remains` → claim: the abstract's calibrated interval |
| R11 | REV-19. **Location:** §V-A, §V-B, §V-D. **Fix:** print the tuning-run room (1.18 points), commitment ratio (0.023) and braking share (0.377) beside the evaluation-run values; cite Table S2; decompose the gap if feasible | SC-19 | R1 major | `table: Supplement Table S2, tuning and evaluation columns` | R1 4 | R1 W2 | SINGLE-REVIEWER | must_fix | `section` — §V-A, §V-B, §V-D | `reporting_requirement_unmet` → table: Table S2 |
| R12 | REV-20. **Location:** Abstract closing lesson; §VI; §VII; §VI Limits. **Fix:** name the recording planner as a condition of the magnitudes; Limits sentence that only relative comparisons transfer | SC-20 | R1 major; R3 minor (SPLIT) | `table: Supplement Table S2` (R1); `text: Supplement Table S28 "Five of the 35 evaluation runs and 10 of the 20 tuning runs ended at the first physical contact"` (R3) | R1 4; R3 3 | R1 W2; R3 W10 | SPLIT | must_fix | `sentence` — Abstract; §VI; §VII; Limits | `claim_scope_unsupported` → claim: the abstract's closing lesson |
| R13 | REV-21. **Location:** §V-C; Supplement S10.4, Table S23; Abstract; §I contribution 2. **Fix:** leave-runs-out choice of per-phase scale ratios with the held-out gain beside 0.89; label 0.89 as an in-sample upper value | SC-21 | minor (R1, R3) (DA major) | `text: §V-C "took its frontier over all triples of scales"` | R1 3; R3 3 (DA 3) | R1 W3; R3 W3; DA M3 (corroborating) | CORROBORATED | must_fix | `re_analysis` — Table S23; §V-C | `evidence_gap_remains` → claim: 89% |
| R14 | REV-27. **Location:** §V-B, §V-D, §VI (and §V-C per DA). **Fix:** attach §IV-B's reading, or decision-equivalents, to each share interpreted where grading is not shown, or report grading checks there | SC-27 | R1 minor (DA major) | `text: §VI "With caution counted at its signed value, its share while the lead brakes falls from 0.61 to 0.35."` | R1 4 (DA 4) | R1 W8; DA M4 (corroborating) | SINGLE-REVIEWER | must_fix | `section` — §V-B to §VI | `interpretive_ambiguity_remains` → section: §V-B to §VI |
| R15 | REV-30. **Location:** Data and Code Availability. **Fix:** create the described deposit (plans with hashes, per-decision arrays, second programs, result files) with a reviewer-accessible link; the DOI placeholder itself is a submission gate | SC-30 | R1 minor | `text: Data and Code Availability "The raw recordings are available from the author on request."` | R1 4 | R1 W11 | SINGLE-REVIEWER | must_fix | `other` (surface_id `data_code_deposit`) — Data and Code Availability | `method_reproducibility_unresolved` → dataset: analysis deposit |
| R16 | REV-33. **Location:** §III-A; §I; §II; Fig. 1 caption. **Fix:** describe the EKF with object-frame noise, the frames of state, noise and P̄, and how P̄ was formed | SC-33 | R2 major | `text: Supplement Table S28 "extended Kalman filter with a constant-velocity model in the object frame"` | R2 3 | R2 W1 | SINGLE-REVIEWER | must_fix | `section` — §III-A and where the filter is named | `method_reproducibility_unresolved` → section: §III-A |
| R17 | REV-34. **Location:** §V-E; §I contribution 4. **Fix:** reword "not expected to carry over" to "the check is silent"; optional heading-aligned Table V | SC-34 | R2 major | `text: §V-E "so the null of this paper is not expected to carry over to them"` | R2 3 | R2 W1 | SINGLE-REVIEWER | must_fix | `sentence` — §V-E; §I contribution 4 | `claim_scope_unsupported` → claim: contribution 4 |
| R18 | REV-35. **Location:** §V-C. **Fix:** report the estimated lead speed and acceleration around the onset and against time since the stop; tabulate the rows selected in after-stop wrong-go decisions; state the mechanism | SC-35 | R2 major | `text: §V-C "The 83% is therefore a figure for recordings that continue for about 20 s after the stop."` | R2 3 | R2 W2 | SINGLE-REVIEWER | must_fix | `re_analysis` — stored arrays; §V-C | `evidence_gap_remains` → claim: 83%, 89% and the §VI–§VII motion-state conclusion |
| R19 | REV-45. **Location:** §VI "Which commitment is representative"; §VII stop branch. **Fix:** restrict to ego–lead contact and name following-traffic exposure and fallback reliability as unscored; stronger: per-source share of decisions relying on the stop | SC-45 | R3 minor (DA major) | `text: §VI "the choice of source matters mainly for comfort and progress, which we did not score"` | R3 4 (DA 3) | R3 W1; DA M6 (corroborating) | SINGLE-REVIEWER | must_fix | `sentence` — §VI; §VII | `claim_scope_unsupported` → claim: §VI stop-branch reading |

### Suggested Revisions (Should Fix / Consider)

| Transport ref | Revision Item (location → fix) | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source | Consensus level | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | REV-08. **Location:** Abstract ("35 runs not used to design the margins"). **Fix:** add that the room and N's difference were examined on these runs in an earlier exploratory analysis (a transfer, not a replication) | SC-8 | EIC minor | `text: Abstract and §III-A` (EIC W4) | EIC 4 | EIC W4 | SINGLE-REVIEWER | should_fix | `sentence` — Abstract | `interpretive_ambiguity_remains` → section: Abstract |
| S2 | REV-10. **Location:** §VI ranking. **Fix:** score a constant time-gap margin, written as a variance along the constraint normal, at equal caution on stored arrays, or explain why it cannot be put on the same footing | SC-10 | minor (EIC, R3) | `text: §VI "a time-gap margin, the usual spacing policy [52], was not among them"` | EIC 4; R3 3 | EIC W6; R3 W4 | CORROBORATED | should_fix | `re_analysis` — stored arrays; §VI | `evidence_gap_remains` → section: §VI |
| S3 | REV-11. **Location:** §II "Threat assessment…" paragraph; Supplement S6. **Fix:** read the full texts of at least [41]–[47] and confirm or reposition the no-prior-evaluation sentence, recording the check in S6; failing that, hedge the sentence to name the abstract-only limit (R2) | SC-11 | EIC minor; R2 minor [SEVERITY-SOURCE: letter-fallback] | `text: Supplement S6 "their content is summarised from abstracts only"` | EIC 3; R2 4 [CONFIDENCE-SOURCE: report-level] | EIC W7; R2 Minor Issues 3 | CORROBORATED | should_fix | `section` — §II; Supplement S6 | `evidence_gap_remains` → claim: §II novelty sentence |
| S4 | REV-12. **Location:** §IV-B "Intervals"; §IV-C third paragraph; §IV-D; §V-A second paragraph; §V-D "A 2 m standstill gap"; §V-E last paragraph; Table IV; §II "Adaptive covariances". **Fix:** move or compress the listed material toward the 10-page recommendation | SC-12 | EIC minor | `absence: whole manuscript — expected a length near the 10-page recommendation; checked main-text word count, Tables I–V, Figs. 1–4, 55 references` | EIC 3 | EIC W8 | SINGLE-REVIEWER | should_fix | `section` — listed locations | `editorial_conformance_unmet` → manuscript: main text |
| S5 | REV-13. **Location:** §V-B, §V-C, §V-D. **Fix:** open each results subsection with a one-sentence finding in words; keep in the text only the numbers used by the Abstract, §VI and §VII | SC-13 | EIC minor | `text: §V-B "With the ego moving the prediction recovers 0.47 [0.35, 0.57], and while the lead brakes 0.61 [0.47, 0.71]"` | EIC 4 | EIC W9 | SINGLE-REVIEWER | should_fix | `section` — §V-B to §V-D | `reader_traceability_reduced` → section: §V |
| S6 | REV-14. **Location:** §IV-B; notation table. **Fix:** define D next to R and RR, or give the conversion in words | SC-14 | EIC minor | `text: notation table "A frontier difference in decisions, $D/201/100 \times n$"` | EIC 5 | EIC W10 | SINGLE-REVIEWER | should_fix | `sentence` — §IV-B | `reader_traceability_reduced` → table: notation table |
| S7 | REV-15. **Location:** Table II. **Fix:** give signed caution its own small table, or place it as columns for every population (as Table S21 does) | SC-15 | EIC minor | `table: Table II, column "All, signed caution" and row "RR(CK3), signed caution"` | EIC 4 | EIC W11 | SINGLE-REVIEWER | should_fix | `section` — Table II | `reader_traceability_reduced` → table: Table II |
| S8 | REV-16. **Location:** Abstract; §I. **Fix:** rewrite the CARLA sentence, e.g. "In CARLA runs the ego follows a lead vehicle that brakes; the lead is perceived by …" | SC-16 | EIC minor | `text: Abstract "CARLA runs in which a lead vehicle brakes are perceived by the CenterPoint detector and CANMOT, a fixed-noise Kalman tracker."` | EIC 5 | EIC W12 | SINGLE-REVIEWER | should_fix | `sentence` — Abstract; §I | `reader_traceability_reduced` → section: Abstract |
| S9 | REV-22. **Location:** §V-A; Supplement S10.1. **Fix:** state when the 0.5% bound was chosen; adopt an a-priori margin in decision units (one decision-equivalent = 0.0022 of the room) and phrase the null as equivalence within it, or as the largest upper end across methods (2.2 decisions) | SC-22 | R1 minor | `text: §V-A "no interval method we tried reaches 0.5% of the room"` | R1 4 | R1 W4 | SINGLE-REVIEWER | should_fix | `sentence` — §V-A; Supplement S10.1 | `reporting_requirement_unmet` → claim: §V-A bound |
| S10 | REV-23. **Location:** §IV-B; notes to Tables III, IV, S5, S24. **Fix:** say that nominal intervals for N's shares (coverage 53%) are not valid at their nominal level, and that the RR₀(N) lead-braking cell [0.001, 0.013] is not a signal | SC-23 | R1 minor | `text: §IV-B "all other intervals should be read as slightly narrow"` | R1 4 | R1 W5 | SINGLE-REVIEWER | should_fix | `sentence` — §IV-B; table notes | `interpretive_ambiguity_remains` → table: Tables III and IV |
| S11 | REV-24. **Location:** §IV-D; Supplement S4. **Fix:** print the S10 amendment's hash and date beside the two earlier plans' hashes | SC-24 | R1 minor | `text: §IV-D "The analyses of Supplement S10 were added last, each defined before its values were read."` | R1 4 | R1 W6 | SINGLE-REVIEWER | should_fix | `sentence` — §IV-D; Supplement S4 | `reporting_requirement_unmet` → section: §IV-D |
| S12 | REV-25. **Location:** §IV-D; Supplement S10.5, S10.9; Acknowledgment. **Fix:** state who or what wrote each second program and the recount, name the parts that were not blind, and qualify "independent" accordingly | SC-25 | minor (R1, R3) | `text: §IV-D "independent second programs re-implement the scoring"` | R1 4; R3 3 | R1 W6; R3 W12 | CORROBORATED | should_fix | `sentence` — §IV-D; Supplement S10.9 | `interpretive_ambiguity_remains` → section: §IV-D |
| S13 | REV-26. **Location:** §V-E; Supplement S9. **Fix:** report the paired run-bootstrap interval of ρ_N − ρ_F0, or say only that the two estimates are nearly equal | SC-26 | R1 minor | `text: §V-E "ranks the realised error (Spearman's ρ = 0.453 [0.392, 0.508]) no better than the class average's does"` | R1 4 | R1 W7 | SINGLE-REVIEWER | should_fix | `sentence` — §V-E | `claim_scope_unsupported` → claim: §V-E "no better than" |
| S14 | REV-28. **Location:** §V-B. **Fix:** give the frontier-construction alternates beside 0.83 and 0.38 (CK3 0.831, 0.790, 0.750; AM 0.376, 0.153 hull), as is done for NA | SC-28 | R1 minor | `table: Supplement Table S5, hull column and footnote` | R1 4 | R1 W9 | SINGLE-REVIEWER | should_fix | `sentence` — §V-B | `reporting_requirement_unmet` → section: §V-B |
| S15 | REV-29. **Location:** §IV-C; §V-D; Table S20c. **Fix:** add a variant averaging caution over selections safe under the reaction-and-stop scoring, or state why the 3 s definition is the right reference | SC-29 | R1 minor | `text: §IV-C "Only the wrong-go flag changes: caution keeps the 3 s scoring's definition."` | R1 3 | R1 W10 | SINGLE-REVIEWER | should_fix | `re_analysis` — stored arrays; §IV-C | `interpretive_ambiguity_remains` → section: §IV-C |
| S16 | REV-31. **Location:** Data and Code Availability. **Fix:** deposit the raw recordings, or state and justify the restriction | SC-31 | minor (R1, R3) | `text: Data and Code Availability "The raw recordings are available from the author on request."` | R1 4; R3 4 | R1 W11; R3 W11 | CORROBORATED | should_fix | `other` (surface_id `data_code_deposit`) — Data and Code Availability | `method_reproducibility_unresolved` → dataset: raw recordings |
| S17 | REV-32. **Location:** §III-B. **Fix:** reword so N is not singled out as on-policy (the recording margin αp + βq is not g·p at any g); optionally report how often the recording planner's selection coincides with N's | SC-32 | R1 minor | `text: §III-B "visited by a planner whose margin used the tracker's covariance; for every other source they are off-policy"` | R1 3 | R1 W12 | SINGLE-REVIEWER | should_fix | `sentence` — §III-B | `interpretive_ambiguity_remains` → section: §III-B |
| S18 | REV-36. **Location:** §V-B; §III-A; Fig. S1. **Fix:** report NIS by phase (onset window) and velocity-error consistency against CARLA truth (NEES or z-scores); state that the NA result does not bear on velocity-block adaptation | SC-36 | R2 minor | `text: §III-A "the median over runs of the mean NIS of the lead track's position block is 0.24, against an expected 2"` | R2 4 | R2 W3 | SINGLE-REVIEWER | should_fix | `re_analysis` — stored arrays; §V-B | `evidence_gap_remains` → claim: NA result (§V-B) |
| S19 | REV-37. **Location:** §VI; §V-A. **Fix:** say that the 1.10 is a velocity-block ratio that depends on look-ahead (1.02–1.05 at t = 0, about 1.10 at 2–3 s) and that state age and look-ahead move it | SC-37 | R2 minor | `table: Supplement Table S14, deviation ratio at t = 0 s against t = 2 s and t = 3 s` | R2 4 | R2 W4 | SINGLE-REVIEWER | should_fix | `sentence` — §VI; §V-A | `interpretive_ambiguity_remains` → claim: "near-constant 1.10 multiple" |
| S20 | REV-38. **Location:** notation table; §II. **Fix:** map g to the chance-constraint parameter (squared quantile or safety factor of the per-constraint risk level [1]) and keep "spacing policy" for the time-gap baseline | SC-38 | minor (R2, R3) | `text: §II "the planner's margin plays the role of a spacing policy in adaptive cruise control [52]"` | R2 4; R3 4 | R2 W5; R3 W5 | CORROBORATED | should_fix | `sentence` — notation table; §II | `interpretive_ambiguity_remains` → table: notation table |
| S21 | REV-39. **Location:** §II; references. **Fix:** add Moser et al. (2018) and Brüdigam et al. (2023) on stochastic-MPC car following and Xia et al. (1994) on fading-factor filtering, with one sentence each on how they differ | SC-39 | R2 minor | `absence: §II Related Work — expected stochastic-MPC car following and fading-factor adaptive Kalman filtering; checked §II, references [1]–[55], Supplement S6` | R2 4 | R2 W6 | SINGLE-REVIEWER | should_fix | `sentence` — §II; reference list | `evidence_gap_remains` → section: §II |
| S22 | REV-40. **Location:** §II. **Fix:** restate [17]: its closed-loop nuPlan comparison cannot use class uncertainty, and its fixed-covariance constant-velocity baseline is the nearest published analogue of this null | SC-40 | R2 minor | `text: §II "The closest planner-in-the-loop study [17] finds that propagating class uncertainty helps a learned predictor"` | R2 3 | R2 W7 | SINGLE-REVIEWER | should_fix | `sentence` — §II | `interpretive_ambiguity_remains` → claim: §II summary of [17] |
| S23 | REV-41. **Location:** Supplement S8.1–S8.2; Table S4 last rows. **Fix:** update the withdrawn wording or mark it as the earlier draft's record; the DA adds: restore or explicitly record the dropped plan-fixed NIS-inflated abstract sentence | SC-41 | R2 minor (DA major) | `text: Supplement S8.2 "a mechanism that no analysis here isolates"` | R2 5 (DA 4) | R2 W8; DA M5 (corroborating) | SINGLE-REVIEWER | should_fix | `section` — Supplement S8.1–S8.2; Table S4 | `reader_traceability_reduced` → section: Supplement S8 |
| S24 | REV-42. **Location:** §VI Limits. **Fix:** add a paragraph on the expected direction in which each simplification (2 Hz detector without latency; lidar noise off; nuScenes checkpoint; one car model, straight road, default weather; configuration shared with [9]) moves the lead-braking room and the braking prediction's share | SC-42 | R2 minor | `text: Supplement Table S28 "run every tenth frame (2 Hz); no latency simulated"` | R2 4 | R2 W10 | SINGLE-REVIEWER | should_fix | `section` — §VI Limits | `interpretive_ambiguity_remains` → section: §VI Limits |
| S25 | REV-43. **Location:** notation table; §IV-B. **Fix:** relabel R as the value of a perfect-information margin within the fixed rule ("analogous to" the value of perfect information), not a bound; map den₀ against O to the value of perfect information for each scoring | SC-43 | R2 minor [SEVERITY-SOURCE: letter-fallback]; R3 minor | `text: notation table "Value of perfect information [55]"` | R2 4 [CONFIDENCE-SOURCE: report-level]; R3 4 | R2 Minor Issues 1; R3 W2 | CORROBORATED | should_fix | `sentence` — notation table; §IV-B | `interpretive_ambiguity_remains` → table: notation table |
| S26 | REV-44. **Location:** §V-E. **Fix:** say that Table S26's tuning-only column shows the same pattern as Table V, which includes the tuning runs on which the class average was computed | SC-44 | R2 minor [SEVERITY-SOURCE: letter-fallback] | `table: Table V; Supplement Table S26` (locator from the card's text; the card gives no typed anchor) | R2 4 [CONFIDENCE-SOURCE: report-level] | R2 Minor Issues 2 | SINGLE-REVIEWER | consider | `sentence` — §V-E | `reader_traceability_reduced` → table: Table V |
| S27 | REV-46. **Location:** §VI; Supplement Table S23(b). **Fix:** add a class-average scale scheduled on a phase estimated from the tracker's state, or say in §VI that the result does not yet show whether a deployable schedule captures the allocation | SC-46 | R3 minor | `text: §VI "a time-gap margin, the usual spacing policy [52], was not among them"` | R3 3 | R3 W4 | SINGLE-REVIEWER | should_fix | `re_analysis` — Table S23(b); §VI | `claim_scope_unsupported` → claim: §VI allocation reading |
| S28 | REV-47. **Location:** §V-D. **Fix:** use S10.5's register (a 2 m model parameter at standstill; the main scoring counts contact) instead of "asks for 2 m … not for the absence of contact" | SC-47 | R3 minor | `text: §V-D "Performance model 2 asks for 2 m at standstill, not for the absence of contact."` | R3 3 | R3 W6 | SINGLE-REVIEWER | should_fix | `sentence` — §V-D | `interpretive_ambiguity_remains` → section: §V-D |
| S29 | REV-48. **Location:** Supplement S3, S3.4. **Fix:** replace "legal following distance" and "legal minimum" with "the R157 minimum following distance [38, §5.2.3.3]", and note that the test beds lie outside the ALKS domain | SC-48 | R3 minor | `text: Supplement S3 "at about 0.31–0.35 s of extra starting gap over the legal following distance"` | R3 4 | R3 W7 | SINGLE-REVIEWER | should_fix | `sentence` — Supplement S3, S3.4 | `interpretive_ambiguity_remains` → section: Supplement S3 |
| S30 | REV-49. **Location:** Abstract; §V-D; §VI. **Fix:** state beside the 12% that 6 m/s² exceeds the planner's own fallback (the (−5, −5) row) and give the planner-matched value (0.18 at 5 m/s²), or say that the stronger stop stands for a separate emergency-braking function | SC-49 | R3 minor | `text: Abstract "With a perfect 6 m/s² stop 0.75 s after each decision, 12% of the room remains."` | R3 4 | R3 W8 | SINGLE-REVIEWER | should_fix | `sentence` — Abstract; §V-D; §VI | `interpretive_ambiguity_remains` → claim: the abstract's 12% |
| S31 | REV-50. **Location:** notation table; §VI Limits. **Fix:** state that wrong-go counts are severity-blind; better, report the closing speed at first loss of clearance for wrong-go decisions, by phase, for F0, E and the braking prediction | SC-50 | R3 minor | `text: notation table "A collision under the assumed manoeuvre; a criticality outcome [50]"` | R3 3 | R3 W9 | SINGLE-REVIEWER | should_fix | `sentence` — §VI Limits (optional re-analysis of stored clearances) | `interpretive_ambiguity_remains` → section: §VI Limits |
| S32 | REV-51. **Location:** Data and Code Availability. **Fix:** deposit the binding-row arrays of all six families (Table V, Table S26, S10.6), the capture and scenario scripts and the S3 simulator, or state the restriction | SC-51 | R3 minor | `text: Data and Code Availability "the per-decision arrays of the 55 lead-braking runs"` | R3 4 | R3 W11 | SINGLE-REVIEWER | should_fix | `other` (surface_id `data_code_deposit`) — Data and Code Availability | `method_reproducibility_unresolved` → dataset: all-family binding-row arrays |

> Transported metadata (severity with any fallback tag, typed evidence anchor, per-finding confidence) is carried on every row. The counts are 19 `must_fix`, 31 `should_fix` and 1 `consider`, for 51 items in total.

### Source-Traceability Checklist

> Immutable source order. This is not a suggested work order. Author triage (`will_address`, `wont_address`, `not_on_point`) is collected later in the separate author-adjudication checkpoint.

- [ ] REV-01 · R1 — obligation `must_fix`: state the steady-tracking condition of the null (§I, contribution 3, §II, §VI)
- [ ] REV-02 · R2 — obligation `must_fix`: recast contribution 3 as a measured confirmation
- [ ] REV-03 · R3 — obligation `must_fix`: abstract clause saying births, misses and real sensing are untested
- [ ] REV-04 · R4 — obligation `must_fix`: pooled-only qualifier for the evaluation design
- [ ] REV-05 · R5 — obligation `must_fix`: population mix in the abstract and the Scope
- [ ] REV-06 · R6 — obligation `must_fix`: truth-derived phase labels for the 89%
- [ ] REV-07 · R7 — obligation `must_fix`: label the analyses added after the first results
- [ ] REV-08 · S1 — obligation `should_fix`: the 35 evaluation runs are a transfer, not a replication
- [ ] REV-09 · R8 — obligation `must_fix`: word the null as a bound
- [ ] REV-10 · S2 — obligation `should_fix`: time-gap margin comparator, or an explanation
- [ ] REV-11 · S3 — obligation `should_fix`: full-text check, or hedge, for [41]–[52]
- [ ] REV-12 · S4 — obligation `should_fix`: shorten toward 10 pages
- [ ] REV-13 · S5 — obligation `should_fix`: lead results subsections with the finding
- [ ] REV-14 · S6 — obligation `should_fix`: define D
- [ ] REV-15 · S7 — obligation `should_fix`: Table II signed-caution layout
- [ ] REV-16 · S8 — obligation `should_fix`: rewrite the CARLA sentence
- [ ] REV-17 · R9 — obligation `must_fix`: placebo or grid-free RR(N)
- [ ] REV-18 · R10 — obligation `must_fix`: justify or replace the calibrated interval
- [ ] REV-19 · R11 — obligation `must_fix`: tuning-run values in the main text
- [ ] REV-20 · R12 — obligation `must_fix`: recording planner as a condition of the magnitudes
- [ ] REV-21 · R13 — obligation `must_fix`: held-out per-phase gain; 89% labelled in-sample
- [ ] REV-22 · S9 — obligation `should_fix`: provenance of the 0.5% bound; margin in decision units
- [ ] REV-23 · S10 — obligation `should_fix`: undercoverage of N's shares stated
- [ ] REV-24 · S11 — obligation `should_fix`: print the S10 amendment's hash and date
- [ ] REV-25 · S12 — obligation `should_fix`: qualify "independent" verification
- [ ] REV-26 · S13 — obligation `should_fix`: paired interval for the Spearman comparison
- [ ] REV-27 · R14 — obligation `must_fix`: apply the grading rule wherever shares are read
- [ ] REV-28 · S14 — obligation `should_fix`: frontier alternates beside 0.83 and 0.38
- [ ] REV-29 · S15 — obligation `should_fix`: caution-axis variant under reaction-and-stop
- [ ] REV-30 · R15 — obligation `must_fix`: create the deposit with reviewer access
- [ ] REV-31 · S16 — obligation `should_fix`: deposit the raw recordings or justify the restriction
- [ ] REV-32 · S17 — obligation `should_fix`: N is also off-policy (§III-B)
- [ ] REV-33 · R16 — obligation `must_fix`: describe the EKF, the frames and P̄
- [ ] REV-34 · R17 — obligation `must_fix`: the reach claim reads "silent"
- [ ] REV-35 · R18 — obligation `must_fix`: physical mechanism for the per-phase and after-stop findings
- [ ] REV-36 · S18 — obligation `should_fix`: NIS by phase; velocity consistency
- [ ] REV-37 · S19 — obligation `should_fix`: 1.10 depends on look-ahead
- [ ] REV-38 · S20 — obligation `should_fix`: remap g to the chance-constraint parameter
- [ ] REV-39 · S21 — obligation `should_fix`: add the adjacent literature
- [ ] REV-40 · S22 — obligation `should_fix`: restate [17]
- [ ] REV-41 · S23 — obligation `should_fix`: remove stale wording from Supplement S8 and Table S4
- [ ] REV-42 · S24 — obligation `should_fix`: direction of the test-bed simplifications
- [ ] REV-43 · S25 — obligation `should_fix`: relabel R in relation to the value of perfect information
- [ ] REV-44 · S26 — obligation `consider`: the Table S26 tuning-only pattern in the main text
- [ ] REV-45 · R19 — obligation `must_fix`: unscored safety costs in the stop-branch reading
- [ ] REV-46 · S27 — obligation `should_fix`: a realisable phase-scheduled rule, or a caveat
- [ ] REV-47 · S28 — obligation `should_fix`: the 2 m gap's register
- [ ] REV-48 · S29 — obligation `should_fix`: "legal following distance" wording
- [ ] REV-49 · S30 — obligation `should_fix`: planner-matched value beside the 12%
- [ ] REV-50 · S31 — obligation `should_fix`: severity-blind wrong-go counts
- [ ] REV-51 · S32 — obligation `should_fix`: all-family arrays and the pipeline in the deposit

### Questions for the Authors (answer in the response letter)

- **EIC**:
  - Q1: confidential copy of [9]; see Submission gates.
  - Q2: missed or coasting updates by phase; bears on REV-01 and REV-03.
  - Q3: REV-01, optional drop-out re-run.
  - Q4: REV-04.
  - Q5: REV-10.
- **R1**:
  - Q1: REV-22.
  - Q2: REV-17.
  - Q3: REV-21.
  - Q4: REV-19.
  - Q5: REV-29.
  - Q6 (RR at a few fixed caution operating points): tied to no weakness; answer in the letter.
- **R2**:
  - Q1: REV-33.
  - Q2: REV-35.
  - Q3: REV-36.
  - Q4: REV-34.
  - Q5: REV-42.
- **R3**:
  - Q1: REV-45.
  - Q2: REV-21.
  - Q3: REV-46 and REV-10.
  - Q4: REV-50.
  - Q5: REV-25.
  - Q6: REV-51.
- **DA**: answer M1–M6 and the DA-only content listed under Devil's Advocate Findings.

### Response Letter Template

Please use the format in `templates/revision_response_template.md` to respond item by item. The response must cover:
- every required item (R1–R19) against its acceptance criterion;
- every suggested item (S1–S32), adopted or with the reason for not adopting it;
- each DA MAJOR row, including the DA-only content;
- the questions above.

Mark all changes in the revised manuscript and supplement, and give a cross-reference table of new section, table and page locations.

---

## Part 3: Reviewer Report Summary (Appendix)

### Journal-Fit Review Report Summary
- Recommendation: preliminary journal-fit signal, major revision (a baseline, not a decision) | Confidence: 4
- Key Point: the paper is in scope, its contribution is narrow but real, and it is candid about its limits. The significance case needs sharpening, mainly because the clean simulated test bed seldom exercises the regime that makes an expected null worth measuring (W1). The abstract also omits fences the body states, and the main text is longer and denser than the venue recommends.

### Reviewer 1 (Methodology) Summary
- Recommendation: not stated in the card (D1 warn, D3 warn) | Confidence: no report-level score; per-finding 3–4
- Key Point: the design is sound and the null robust. The abstract's calibrated interval for RR(N) may be calibrating a grid-interleaving artefact (W1), and the main text omits that the room, the commitment ratio and the braking prediction's share are several times smaller on runs recorded under another planner (W2). Ten minor reporting items follow; six GRIM receipts are consistent.

### Reviewer 2 (Domain) Summary
- Recommendation: Major Revision (domain view) | Confidence: 4
- Key Point: the steady-state mechanism is correct and confirmed for straight-road lead braking. However, the tracker is described as linear although it is run as an EKF with object-frame noise, the cross-family reach claim overreads the ratio variation (W1), and the per-phase and after-stop findings behind the 83% and 89% lack a physical mechanism (W2).

### Reviewer 3 (Perspective) Summary
- Recommendation: Minor Revision (seat-level advice) | Confidence: 4
- Key Point: regulatory and deployment fences are unusually careful. The stop-branch practical reading omits following traffic and fallback reliability (W1, the seat's most important item). The bridges to value of information and to spacing policies are looser than those fields' meanings, the 89% is in-sample and truth-labelled, and the deposit does not cover contribution 4.

### Devil's Advocate Summary
- Recommendation: N/A — findings only
- Key Challenge: no unresolved Critical challenge (0 CRITICAL rows). The strongest counter-argument, carried in six MAJOR rows: in a population with none of the conditions the paper gives for scoring an expected null, the decision-level null is entailed by the steady state and the swept scale (M1). The positive control certifies sensitivity to phase rather than to per-decision error (M2). The 89% is an in-sample, truth-labelled envelope (M3). Shares are read where the paper's own grading rule is not met (M4). The abstract headlines post hoc results (M5). And the "reliable stop" reading assumes away who bears its cost (M6).
