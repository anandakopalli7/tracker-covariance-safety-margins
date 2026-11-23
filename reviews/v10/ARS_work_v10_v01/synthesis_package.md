# Editorial Decision Package

## Calibration Resolution

`calibration_status: NOT_CALIBRATED`

Current runtime boundary: this package is not upgraded from a candidate or prose-named profile. `PROFILE_MEASURED` remains unavailable until a closed profile artifact and replay validator bind the exact target fields to the actual completed-panel `execution_topology_sha256`. Schema 6 machine output is not emitted in this run.

**Criteria binding (#684).** This is an explicitly unbound run. All five seats disclose `criteria_binding_unavailable` in their Phase 1 cards; in Phase 2 the Devil's Advocate restates it and the Journal-Fit seat states that no criteria manifest was supplied. No #684 marker set exists to verify. This package makes no venue-criteria or venue-alignment claim beyond the requester-stated constraints: IEEE Open Journal of Intelligent Transportation Systems (OJ-ITS), regular paper, abstract at most 250 words, no page limit, 10 pages recommended. Binding status is not a score, failure condition, severity or verdict.

## Review Panel Provenance (#540/#740)

- **Typed artifact**: `ARS_work_v10_v01/provenance_artifact.json`, schema `review-panel-provenance/1.0`. The dispatching session reports `review_panel_provenance.py validate` → PASS (schema and deterministic replay). The synthesizer did not re-run the validator.
- **Artifact SHA-256 (raw bytes)**: `56e4cd08c5198427dd489de66b841a5f47cc4412ee0717bb6992180707301633`
- **Panel ID**: `ars-review-v10-round-1`
- **Mode and contract**: `reviewer_full`; `reviewer/reviewer_full/v2`; contract SHA-256 `d958bc2ade7d9d154954c33fd424766697a8b6ef664854800a3106d804ee7e5c`
- **Normalized manifest SHA-256**: `532d5c78b2d172bcfd6d550d6619241b217e647adf28125f59daefc444b8e32a`
- **Execution topology SHA-256**: `ad26ca82216010e9ee1892fb6e43b08702eefecce51bc36d2c2b11ab7d8b3b07`
- **Fresh-context scope**: `within_panel_attempt_only`. It does not compare retries or prior rounds, and it does not show that any context was new relative to attempt history.
- **Build note (CRLF wrapper)**: this Windows install's `shared/contracts/reviewer/full.json` has CRLF line endings. Its raw SHA-256 is 900290ba…b300, while the builder pins d958bc2a…e5c, which is the SHA-256 of the same bytes with LF line endings. The dispatcher therefore ran the unchanged builder through a wrapper (`run_provenance_lf.py`) that points only the contract-digest check at an LF-normalised copy (`full_contract_LF_copy.json`). The plugin files were not modified.
- **Context note**: the artifact records each seat's Phase 2 (paper-visible) invocation context. The dispatching session reports that each seat's paper-blind Phase 1 ran in a separate fresh context and that no seat saw another seat's output. Only the Phase 2 contexts are artifact observations.
- **Machine carrier**: no Schema 6 output is emitted, so no `review_panel_provenance` carrier is validated here. This prose is not the machine carrier.

| Seat | Role ID | Actor type | Context ID | Peer outputs visible | Model family | Provider | Human reviewer ID |
|---|---|---|---|---|---|---|---|
| EIC | eic | model | round1-eic-phase2-subagent | false | claude-opus-5-5 | anthropic | null |
| R1 | methodology | model | round1-methodology-phase2-subagent | false | claude-opus-5-5 | anthropic | null |
| R2 | domain | model | round1-domain-phase2-subagent | false | claude-opus-5-5 | anthropic | null |
| R3 | perspective | model | round1-perspective-phase2-subagent | false | claude-opus-5-5 | anthropic | null |
| DA | da | model | round1-da-phase2-subagent | false | claude-opus-5-5 | anthropic | null |

| Provenance axis | Status (`true` / `false` / `unknown`) |
|---|---|
| Role-separated | true |
| Within-panel invocation-context separation | true |
| Blind to peer outputs | true |
| Model-family distinct | false |
| Provider distinct | false |
| Human-reviewer distinct | false |

- **Binary independence claim**: not computed (`independence_claim: not_computed_from_personas`). Persona or role diversity establishes only `role_separated`. The panel is not described as independent.
- **Correlated-error disclosure** (required; reason `same_model_family`): All model-executed review seats used one model family; role separation does not remove correlated-error risk.

---

## Part 1: Editorial Decision Letter

Dear Author,

Thank you for submitting your manuscript, "Does a Kalman Tracker's Covariance Improve Car-Following Decisions? A Decision-Level Evaluation in CARLA Lead-Braking Scenarios", for this simulated pre-submission review targeting the IEEE Open Journal of Intelligent Transportation Systems (regular paper). Five role-separated review seats reviewed it: a Journal-Fit Reviewer, a methodology reviewer, a domain reviewer, a perspective reviewer and the fixed Devil's Advocate. Their execution provenance is reported above and is not reduced to a binary independence claim. All five seats ran on one model family.

### Decision: Major Revision

### Mechanical Decision Record (v3.6.2 sprint contract `reviewer/reviewer_full/v2`)

Under a sprint contract the mechanical engine decides the outcome (`references/editorial_decision_standards.md` §0). The narrative below explains that outcome and does not change it.

**Step 1: role-scoped scoring matrix.** The matrix counts only assessed scores from eligible seats. Scores from ineligible seats (`not_assessed`) are excluded. No eligible seat abstained.

| Dimension | Priority | Eligible roles | Assessed eligible scores | Verdict |
|---|---|---|---|---|
| D1 methodology_rigor | mandatory | methodology | R1: block (repairable) | block |
| D2 domain_accuracy | mandatory | domain | R2: warn | warn |
| D3 argumentative_coherence | mandatory | da, methodology | DA: block (repairable); R1: warn | block |
| D4 cross_disciplinary_relevance | high | perspective | R3: warn | warn |
| D5 writing_and_structure | normal | eic | EIC: warn | warn |
| D6 venue_fit_and_contribution | mandatory | eic | EIC: warn | warn |

**Step 2: failure conditions.** Each condition is evaluated in two stages. First the cross-reviewer quantifier is applied within each selected dimension, then the expression's dimension quantifier is applied across dimensions.

| Condition | Severity | Quantifier | Expression | Evaluation | Fired |
|---|---|---|---|---|---|
| F1 | 95 | any | any mandatory dimension has a fatal block | No assessed eligible seat on D1, D2, D3 or D6 declared a fatal block | false |
| F2 | 90 | any | any mandatory dimension scores 'block' | D1: R1 block → true; D3: DA block → true | true |
| F3 | 70 | majority | two or more mandatory dimensions score 'warn' or worse | D1 (n=1, needs 1): true; D2 (n=1): true; D3 (n=2, needs both): R1 warn and DA block → true; D6 (n=1): true; 4 dimensions ≥ 2 | true |
| F4 | 60 | any | any high-priority dimension scores 'block' | D4: R3 warn → false | false |
| F5 | 40 | any | any dimension scores 'warn' or worse | All six dimensions are warn or block | true |
| F0 | 10 | all | every dimension scores 'pass' | D1 is block (no dimension passes) → false | false |

**Step 3: precedence.** The fired conditions are F2 (90), F3 (70) and F5 (40). F2 has the highest severity, so its action applies.

```text
dimension_verdicts: [D1=block, D2=warn, D3=block, D4=warn, D5=warn, D6=warn]
fired_conditions: [F2, F3, F5]
da_critical_adjudications: []
editorial_decision=major_revision
```

The DA's CRITICAL table is empty, so no DA-CRITICAL ID needs adjudication and the decision is not accept. No DA-CRITICAL-versus-accept marker applies.

### Consensus Analysis

Consensus is counted per sub-claim (Step 1b inventory, Part 3). The denominator is always the four non-DA seats: EIC, R1, R2 and R3. A seat that did not mention a sub-claim is counted as silent, not as agreeing. A Major/Minor gap between seats on the same sub-claim is recorded as `disputed (severity)`, so that sub-claim becomes a SPLIT.

#### Points of Agreement (Consensus)

- **[CONSENSUS-4]**: None.
- **[CONSENSUS-3]**: None. No weakness sub-claim was raised or corroborated by three or four non-DA seats.
- The seats do agree on several strengths. These are not roadmap items:
  - All four non-DA seats credit the ground-truth-free margin-ratio check of Fig. 2(b) (EIC S3, R1 S5, R2 S4, R3 S5).
  - All four credit the lesson that open-loop decision scores must state their commitment assumption (EIC S5, R1 S6, R2 S6, R3 S4).
  - Three credit the oracle positive control (EIC S1, R1 S2, R3 S1). R2 S2 confirms that it is correctly framed as the value of perfect information.

#### Below the Consensus Bar (#1100)

Few seats does not mean low importance. Each finding is judged on its named criterion and anchored evidence. Transport references are in parentheses.

- [CORROBORATED] EIC, R2. Positioning against ITS-venue, threat-assessment and IMM/adaptive-filter literature is thin, and the novelty search skipped that literature. SC-8 (S2)
- [CORROBORATED] EIC, R3. Paper-specific terms are used before they are defined, and there is no plain-language statement of results. SC-11 (S4)
- [CORROBORATED] EIC, R1. The abstract's held-out framing omits the earlier exploratory look at the evaluation runs. SC-22 (S11)
- [CORROBORATED] R2, R3. The room and commitment ratios are defined for contact only. The adopted R157 model 2 specifies a 2 m standstill gap and 7 m/s² for the other vehicle, and the perfect oracle is not scored at the 2 m gap. SC-45, SC-46 (R17)
- [CORROBORATED] R2, R3. The R157 values are borrowed outside the regulation's ALKS scope and given more authority than their role supports. SC-55 (S28)
- [SINGLE-REVIEWER] EIC. The contribution list presents confirmation of an expected steady state as a contribution. SC-2 (R2)
- [SINGLE-REVIEWER] EIC. Optional: apply the evaluation to a source whose covariance varies per decision. SC-3 (S1)
- [SINGLE-REVIEWER] EIC. The practical take-away under the realistic commitment is unstated, and the Conclusion is not conditional on the commitment. SC-4, SC-5 (R3)
- [SINGLE-REVIEWER] EIC. The main text is an estimated 20–40% over the recommended length. SC-6 (R4)
- [SINGLE-REVIEWER] EIC. Overlap with the author's related manuscript [9], and reliance on preprints. SC-9, SC-10 (S3)
- [SINGLE-REVIEWER] EIC. Arm names drift, and the symbols R and RR(N) are inconsistent with the Notation table. SC-12, SC-13 (S5)
- [SINGLE-REVIEWER] EIC. The graded-oracle check that governs how phase shares are read sits only in the Supplement. SC-14 (S6)
- [SINGLE-REVIEWER] EIC. The main text narrates project history and refers to earlier reviews. SC-15 (S7)
- [SINGLE-REVIEWER] EIC. The author block and the AI-use disclosure are unfilled placeholders. SC-16, SC-18 (R6)
- [SINGLE-REVIEWER] EIC. Captions are split across two files. SC-19 (S8)
- [SINGLE-REVIEWER] EIC. Number formats and precision are inconsistent. SC-21 (S10)
- [SINGLE-REVIEWER] EIC. The Index Terms lack ITS vocabulary. SC-24 (S12)
- [SINGLE-REVIEWER] R1. The step-frontier bootstrap intervals are unvalidated, the NIS-inflated wording depends on them, and the caution-grid handling is unstated. SC-25, SC-26, SC-27 (R9)
- [SINGLE-REVIEWER] R1. The reaction-and-stop results rest on single imputations of censored plans. SC-28 (R10)
  - DA-corroborated (M5): the DA reports the same sub-claim. The DA is not an independent seat and does not change the count.
- [SINGLE-REVIEWER] R1. Caution conditions on the outcome, and the 3 s shares were not rerun with signed caution. SC-29 (R11)
  - DA-corroborated (M3): the DA reports the same sub-claim. The DA is not an independent seat and does not change the count.
- [SINGLE-REVIEWER] R1. The pooled estimand is set by post-stop recording length, and the cross-phase mechanism is not isolated. SC-30, SC-31 (R12)
  - DA-corroborated (M1): the DA reports the same sub-claim. The DA is not an independent seat and does not change the count.
- [SINGLE-REVIEWER] R1. The recording, perception and planner configuration needed to regenerate the data is missing. SC-33 (R14)
- [SINGLE-REVIEWER] R1. Replay validity on the evaluation runs is not shown, and the counterfactual assumption is unstated. SC-34, SC-35 (S13)
- [SINGLE-REVIEWER] R1. The five short runs are unexplained and were never removed jointly. SC-36 (S14)
- [SINGLE-REVIEWER] R1. The 10-decision-equivalent resolution rule has no sensitivity check. SC-37 (S15)
- [SINGLE-REVIEWER] R1. Ratio percentile intervals are unstable where the denominator approaches zero. SC-38 (S16)
- [SINGLE-REVIEWER] R1. The descriptive, post-results status of the commitment analyses is missing from the abstract and conclusion. SC-39 (S17)
- [SINGLE-REVIEWER] R1. The braking prior's cost where no braking follows is untested. SC-40 (S18)
  - DA-corroborated (M2): the DA reports the same sub-claim. The DA is not an independent seat and does not change the count. Severities differ: R1 minor, DA major.
- [SINGLE-REVIEWER] R1. The graded-oracle check rests on a single random draw. SC-41 (S19)
- [SINGLE-REVIEWER] R2. The choice of 3 m/s² is unstated, and the value lies inside the recorded leads' braking range. SC-43 (R16)
- [SINGLE-REVIEWER] R2. Optional: a sweep over the braking prior's deceleration. SC-44 (S20)
- [SINGLE-REVIEWER] R2. Optional: a steady-state computation of the margin ratio, and evidence on how common fixed-noise trackers are. SC-47, SC-48 (S21)
- [SINGLE-REVIEWER] R2. The margin is propagated without process noise, and this is not stated in §III-B. SC-49 (S22)
- [SINGLE-REVIEWER] R2. The NIS-inflated arm tests only the output-covariance channel. SC-50 (S23)
- [SINGLE-REVIEWER] R2. The 2 Hz update rate is not justified or stated as a limit. SC-52 (S25)
- [SINGLE-REVIEWER] R2. The Conclusion's location claim is a ranking among the tested sources, and a time-gap margin is untested. SC-53 (S26)
- [SINGLE-REVIEWER] R2. Optional: add a time-gap arm. SC-54 (S27)
- [SINGLE-REVIEWER] R2. Present the τ and A sweeps as the result. SC-57 (S29)
- [SINGLE-REVIEWER] R3. The null is not fenced against removing or freezing covariance margins in a deployed stack. SC-58 (R19)
- [SINGLE-REVIEWER] R3. Cross-family scale reallocation is untested. SC-59 (R20)
- [SINGLE-REVIEWER] R3. Recorded lead braking (at most 5.5 m/s²) is milder than the assumed stop and the regulation's test. SC-60 (S30)
- [SINGLE-REVIEWER] R3. The closed-loop fallback share is missing where readers meet the sizing figures. SC-61 (S31)
- [SINGLE-REVIEWER] R3. Comfort and following-traffic costs are unnamed and unmeasured. SC-62 (S32)
  - DA-corroborated (M3): the DA reports the same sub-claim. The DA is not an independent seat and does not change the count. Severities differ: R3 minor, DA major.
- [SINGLE-REVIEWER] R3. §I Scope does not list the road users and scenarios it leaves out. SC-63 (S33)
- [SINGLE-REVIEWER] R3. The paper's terms are not mapped to established ITS and safety vocabulary. SC-64 (S34)
- [SINGLE-REVIEWER] R3. The transferable ratio check has no decision rule or guidance for other planner types. SC-65 (S35)
- [SINGLE-REVIEWER] R3. The road type and setting of the recordings are not stated. SC-66 (S36)

#### Devil's Advocate Findings (outside the four-seat count)

- **DA-CRITICAL**: none. The DA states that its CRITICAL table is "empty by judgement, not by omission". No adjudication is due.
- **DA MAJOR rows**: these are the stated basis of the DA's repairable block on D3. Each row maps to the roadmap as follows:
  - M1 (pooling and cross-phase allocation) corroborates SC-30 and SC-31 (R12).
  - M2 (cost where braking never comes) corroborates SC-40 (S18).
  - M3 (equal caution is not equal cost) corroborates SC-29 (R11) and SC-62 (S32).
  - M5 (censored plans) corroborates SC-28 (R10).
  - M4 (whether the room is one a covariance can use) and M6 (the prior's off-policy value) match no non-DA sub-claim. They appear as DA-only items S37 and S38, set to should_fix because a DA row never sets an obligation by itself. EIC W2 offers the closed-loop run of M6 as an optional stronger fix.
- **DA Minor Points and Ignored Alternatives**: these are not issue rows and create no roadmap items. Three of them overlap roadmap items: pre-specification deposit (R7), the NIS-inflated interval wording (R9) and the two senses of "room" (S5). The author may answer the rest in the response letter.

#### Points of Disagreement

All cards were written blind to one another, and the Journal-Fit seat is itself a party to five of the nine SPLITs. The synthesizer therefore records the arbitration, acting as handling editor. It applies evidence first, then expertise, then the unresolved-dissent principle (#574 B1), and checks disputed points against the manuscript. Wording style was not used as evidence (§1c parity check).

**Disagreement 1: Title and headline pose the expected null as an open question (SC-1 → R1)**
- **EIC view** (W1, major, conf 4): the title, abstract and §I lead with a null that §I itself calls expected. A screening editor will read the headline as a known result. The EIC asks for a retitle around the question actually answered.
- **R2 view** (W3, minor, conf 4): filter theory settles this case. The minimum fix is to qualify the title to the fixed-noise case and add one abstract sentence.
- **Disagreement type**: severity. Both seats agree on existence and on compatible remedies.
- **Editor's Resolution**: must_fix (R1) at sentence and section scope. R2's minimum fix is the acceptance floor. The EIC's reordering of contributions is carried separately as R2 (SC-2).
- **Resolution Rationale**: the manuscript confirms the mismatch. §I says "For a fixed-noise Kalman filter the covariance's null is expected", yet the title asks about "a Kalman Tracker". The consequence the EIC names falls on significance screening under D6, a mandatory dimension owned by that seat, so the EIC's weight sets the obligation. No experiment is required.

**Disagreement 2: The abstract is not self-contained (SC-7 → R5)**
- **EIC view** (W4, major, conf 5): the abstract, at 249 words, uses frontier types, phase shares and "those plans" without definition. It carries about twenty numbers and ends on what cannot be measured. The EIC asks for a plain rewrite of about 200–230 words.
- **R3 view** (W7, minor, conf 4): the abstract's last sentences cannot be parsed without the Notation table, and "commitment" is undefined at first use.
- **Disagreement type**: severity.
- **Editor's Resolution**: must_fix (R5) at section scope.
- **Resolution Rationale**: both seats quote the same final sentence. Abstract conventions are the Journal-Fit seat's core competence (conf 5). Several required items (R1, R8, R10, R11, R13, R17) may change the abstract's wording, and with only one word of headroom under the 250-word limit, that can only be absorbed by a rewrite.

**Disagreement 3: Repository and deposit (SC-17 → R7)**
- **EIC view** (W11, minor, conf 5): the repository statement is a placeholder. The EIC rates it Minor "only because the fix is a link" and adds that referees will treat an unverifiable pre-specification as a major issue if the repository is not public.
- **R1 view** (W5, major, conf 4): the code, both plans with their amendments and lock manifests, and the per-decision arrays must be deposited before acceptance. The Supplement S4 hashes can be verified only once these are public.
- **Disagreement type**: severity.
- **Editor's Resolution**: must_fix (R7).
- **Resolution Rationale**: D1's definition includes reproducibility, which is the methodology seat's domain. §IV-D's credibility claim ("The plan, its SHA-256 and every amendment are released with the code") cannot be checked without the deposit. The EIC's own conditional statement reaches R1's severity if the repository is not public at resubmission.

**Disagreement 4: Fig. 2(b)'s outlying rows (SC-20 → S9)**
- **EIC view** (W13, minor, conf 4) and **R2 view** (W3 stronger fix, minor, conf 4): the rows outside the 5% band, including a group near 1.7, are unexplained. The EIC asks what they are. R2 suggests showing that the tail follows from re-initialisations and missed detections.
- **R3 view** (W1, major, conf 4): the uncharacterised 0.74% is part of why the null is not fenced for deployment. R3 asks for the 1,127 rows to be characterised by track age.
- **Disagreement type**: severity.
- **Editor's Resolution**: should_fix (S9). R3's characterisation by track age is the acceptance test.
- **Resolution Rationale**: two seats rate the characterisation Minor. R3 attaches its Major weight to the deployment fence, which stays must_fix as R19 (SC-58) and is not diminished. The characterisation is supporting evidence for R19, and the author must respond to S9 either way.

**Disagreement 5: "At most about 0.4%" presented as a bound (SC-23 → R8)**
- **EIC view** (W16, minor, conf 3): this concerns only the abstract's wording. Give the point estimate and its basis, or say "near zero". The EIC leaves the choice of interval to the methodology seat.
- **R1 view** (W1, major, conf 4): the bound is the upper end of a basic interval chosen after the results. Its lower end (0.00125) excludes zero while the percentile interval includes zero, and neither interval has verified coverage.
- **Disagreement type**: severity.
- **Editor's Resolution**: must_fix (R8) at sentence scope, tied to R9.
- **Resolution Rationale**: resampling inference is R1's domain, and the EIC defers to it. §V-A confirms that the interval was "chosen after the results". The phrase appears in the Abstract, contribution 2 and the Conclusion.

**Disagreement 6: The 83% is printed only as a pooled figure (SC-32 → R13)**
- **R1 view** (W4 fix 3, major, conf 4): name the population, and print the ego-moving or phase-weighted value beside the 83%.
- **R2 view** (W10, minor, conf 4): the same remedy. With the ego moving the share is 0.47; against a perfect oracle, phase-weighted, it is 0.665.
- **Disagreement type**: severity. The remedies are identical.
- **Editor's Resolution**: must_fix (R13) at sentence scope.
- **Resolution Rationale**: the paper's own figures show that 82.7% of evaluated decisions come after the stop and 77.5% have the ego at or below 0.5 m/s. The question of which estimand to report belongs to the methodology seat, and both cards give the same fix.

**Disagreement 7: The "RSS-style" label (SC-42 → R15)**
- **R2 view** (W1, major, conf 4): RSS [37] is an unconditional worst-case envelope, whereas CK3 is a nominal constant-deceleration prediction. The paper also uses the label for two different objects.
- **R3 view** (W5, minor, conf 4): the same point. The label invites readers to take the 83% as evidence for an RSS-compliant design.
- **Disagreement type**: severity.
- **Editor's Resolution**: must_fix (R15) at sentence scope.
- **Resolution Rationale**: both seats, each within its core competence, find the label inaccurate for a cited framework. The manuscript uses it in §II and twice in the §VI paragraph that carries the 83% claim. That makes it a domain-accuracy defect on a mandatory dimension (D2), and the fix costs a few sentences. R2's Major weight on the deceleration choice is carried separately as R16.

**Disagreement 8: Is §V-D a separate line of evidence? (SC-51 → S24)**
- **R2 view** (W6, minor, conf 4): σ_N/σ_F0 is 1.02–1.05 at t = 0 and 1.086–1.094 at t = 1 s. The two deviations are therefore near-monotone transforms of each other, and ρ_N ≈ ρ_F0 follows from Fig. 2(b). §VI and the Conclusion nonetheless cite §V-D as a further check.
- **R1 view** (Review Body summary and S5, no severity tag): counts the deviation-ranking check among the main supports for the null. R1 credits it with separating ranking driven by the state's age from ranking driven by the covariance.
- **Disagreement type**: existence (whether the evidence is independent).
- **Editor's Resolution**: should_fix (S24). Present §V-D in §VI and §VII as a consistency check of the ratio result that locates the ranking in the state's age, or add R2's direct test of the covariance's own variation.
- **Resolution Rationale**: §V-D prints the ratios R2 cites and concludes that "the ranking comes from the state's age, not from the tracker's covariance". R1's credit for the mechanism therefore stands. R2 is also right that the check is not independent of the ratio, and uncertainty–error ranking is R2's field. The null does not depend on it.

**Disagreement 9: "Rests on the performance-model values" (SC-56 → R18)**
- **R2 view** (W11, minor, conf 3): R157's performance models are reference performances for automated lane keeping, not models of a planner's commitment. The sentence reads as regulatory validation.
- **R3 view** (W2, major, conf 3): the same sentence claims reliance on model 2. That model also fixes a 2 m standstill gap and 7 m/s² for the other vehicle, and the primary scoring sets both aside.
- **Disagreement type**: severity.
- **Editor's Resolution**: must_fix (R18) at sentence scope. Either R3's replacement sentence or R2's "nominal parameterisation" wording meets it.
- **Resolution Rationale**: the claim appears in §V-C, while Supplement S3.1 uses d_stop = 2 m from the same model. Once R17 states the zero gap, the sentence as written would contradict it. The fix is one sentence plus the matching Limits clause.

### Decision Rationale

Under the sprint contract, the decision is mechanical, and this letter neither softens nor hardens it. F2 fires because mandatory dimensions are blocked: D1 by R1 and D3 by the DA. F3 also fires, because four mandatory dimensions (D1, D2, D3 and D6) are at warn or worse under the majority quantifier, and F5 fires on any warn. F1 does not fire, since no seat declared a fatal block. Both blocking seats call their blocks repairable: R1 says "It is not fatal", and the DA says the thesis "can be repaired by added analyses … or by substantially narrowed claims". F2 has the highest severity (90), so the decision is Major Revision. The Journal-Fit seat's preliminary signal was also major revision.

The cards agree on what the revision must and need not do. Every seat that addressed the central covariance null finds it robust. R1 writes "None of these overturns the covariance null", and R2 says that neither of its Major findings "touches the covariance null". R3 finds the main claim "scoped with unusual care", and the DA writes "The covariance null survives all six".

The required work concerns the inferential support and scope of the secondary headline numbers:
- the unvalidated step-frontier intervals (R8, R9);
- the imputation of censored plans (R10);
- caution that conditions on the outcome (R11);
- the pooled estimand and its population (R12, R13);
- a room defined for contact only, under a regulatory model whose 2 m gap is set aside (R17, R18).

It also covers framing, the abstract, scope fences and reproducibility (R1–R7, R14–R16, R19, R20). R1 states that its items can be repaired by re-analysing the stored arrays and adding documentation, without new recordings. Items that need new runs are either optional (`consider`) or offer a wording alternative. The DA's CRITICAL table is empty, so no DA adjudication is due. Cross-model verification (`ARS_CROSS_MODEL`) is not set, so Step 4b was skipped.

**Desk-rejection risk (requested by the researcher).** Only the Journal-Fit seat assessed this risk. It rated it "moderate as the text stands; low once the gating items are fixed" and named four gating items:
1. The unfilled author block, repository statement and AI-use disclosure, which would cause an administrative return before any scientific screening (R6, R7).
2. A headline that leads with a null the paper itself calls expected (R1, R2).
3. An abstract a general ITS reader cannot parse (R5).
4. A main text an estimated 20–40% over the recommended 10 pages (R4). This is an estimate from word and display-item counts, not a typeset count.

The seat called items 1 and 4 mechanical and items 2 and 3 rewriting; none needs new experiments. R2 (W3) and R3 (W7) raised items 2 and 3 at Minor severity, and R1 rated the repository gap Major (W5). This is the Journal-Fit seat's estimate, not a claim about the venue's criteria.

### Blocking Issues (0–3, immutable source order)

| Transport ref | Blocking issue | Source reviewer(s) | Evidence anchor | Resolving roadmap item |
|---------------|----------------|--------------------|-----------------|------------------------|
| R9 | Bootstrap intervals for the step-frontier shares RR(N) and RR(NA) are not validated, and the RR(N) point lies outside its own intervals. This is the basis of R1's repairable D1 block, which fires F2 | R1 | text: §V-A para. 2 "The point lies above the 97.5th percentile of its run-bootstrap distribution (median 0.0001; largest of 20,000 resamples 0.0025)" | R9 (with R8 for the abstract's bound) |
| R10 | The headline location claim (contribution 3, §VII: the measurable decision value "lies in anticipating braking") depends on premises the paper does not support: pooling, censored-plan imputation, outcome-conditioned caution, unmeasured cost without braking, the room a covariance can use, and off-policy states. This is the basis of the DA's repairable D3 block, which fires F2 | DA (D3 block, M1–M6); R1 (D3 warn) | text: Section IV-B "how one margin scale spends caution across phases of very different risk, a mechanism that no analysis here isolates"; Section VI "These phase gains, about 127 decisions, are a third of its pooled gain of about 383 decisions" | R10, R11, R12, R13, with R3; also S18, S32, S37, S38 |
| R17 | The room and every commitment ratio are defined for contact only, and the 2 m standstill gap of the adopted R157 model 2 is unscored. This is corroborated by R2 and R3, and is basis for R2's D2 warn on a mandatory dimension | R2, R3 | text: Supplement S5, footnote to Table S6, "the 3 s oracle is not an oracle" | R17 (with R18) |

---

## Part 2: Revision Roadmap

> The `Sub-Claim(s)` column carries the Step 1b `sub_claim_id`s that each item traces to. A DA-only item has no sub-claim and is marked `—`.

The machine `revision-roadmap/1.1` JSON is not emitted, because no block manifest exists to bind `proposed_targets[]`. Without that manifest, no item proposes block targets.

**Obligation basis.** Obligation is an editorial gate under the fired major-revision condition. It is not a work rank.
- By default, a Major driving finding is `must_fix` and a Minor driving finding is `should_fix`.
- A fix step that the seat itself marks as stronger or optional is `consider`.
- For a SPLIT, the arbitration above sets the obligation.
- DA-only items are `should_fix`, because a DA row never sets an obligation by itself.
- One exception: R6 is must_fix at minor severity. The Journal-Fit seat records that these placeholders would cause an administrative return before review (W11) and that IEEE requires a final disclosure (W12). This makes R6 a submission gate; its severity is not re-rated.

Severity, evidence anchor and confidence are transported unchanged from the driving card. For a multi-seat item, every seat's values are shown with the seat named.

### Required Revisions (Must Fix)

> **Ordinal contract (#576/#670):** `R<n>` follows the immutable roadmap source order (EIC → R1 → R2 → R3 → DA, card finding order within each), filtered to `obligation_class == must_fix`. Author-selected display order and triage never enter the derivation. Blocks are exactly `R1..Rn`. Each Acceptance criteria value is a single-line `- **Acceptance criteria**: <text>` bullet. The machine artifact is the closed `revision-roadmap/1.1` core, not an author-editable work list.

| Transport ref | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|
| R1 | Qualify or retitle the headline so it no longer poses the expected fixed-noise null as an open question; state in the Abstract and §I that the null is the steady-state expectation | SC-1 | major (EIC W1) / minor (R2 W3): SPLIT, arbitrated | EIC W1: text: §I para. 4 "For a fixed-noise Kalman filter the covariance's null is expected"; §II Novelty "our contribution is to measure its decision consequence against an oracle with demonstrated room" · R2 W3: text: Title "Does a Kalman Tracker's Covariance Improve Car-Following Decisions?" | EIC 4 (contribution framing, within the handling editor's remit) · R2 4 (Kalman steady state and tracking practice) | EIC; R2 (disputed severity) | must_fix | sentence: Title; Abstract sentence 1; §I para. 4 | `claim_scope_unsupported` → claim: title question |
| R2 | Recast the contribution list: present the evaluation design and the commitment dependence as contributions and the covariance diagnostic as a confirmatory test; add one §I sentence on why the expected null still needed measuring | SC-2 | major (EIC W1) | text: §I para. 4 "For a fixed-noise Kalman filter the covariance's null is expected"; §II Novelty "our contribution is to measure its decision consequence against an oracle with demonstrated room" | 4 (contribution framing, within the handling editor's remit) | EIC | must_fix | section: §I contribution list | `acceptance_criterion_unmet` → section: §I contributions (D6) |
| R3 | Add a §VI implications paragraph (which commitment model is representative and why, the practical reading under each, the closed-loop test that would settle it) and word the Conclusion's last sentence conditionally | SC-4, SC-5 | major (EIC W2) | text: §IV-C "The 3 s commitment scoring is a stress scoring."; §VII "the decision value we could measure lies in anticipating braking under the 3 s commitment, not in the covariance" | 4 (significance for an ITS testing and development readership) | EIC | must_fix | section: §VI (new paragraph); §VII last sentence | `claim_scope_unsupported` → claim: §VII "lies in anticipating braking" |
| R4 | Bring the main text toward the recommended length by moving appendix-grade material to the Supplement without removing results, and state each headline number once | SC-6 | major (EIC W3) | table: Table IV (main text; 16 quantity rows across five population columns) | 4 (estimate from word and display-item counts; typeset length may differ by about a page) | EIC | must_fix | section: Table IV; §III-A; §IV-D; §V-C; §V-D; §I contribution 3 | `editorial_conformance_unmet` → manuscript: main-text length against the recommended 10 pages |
| R5 | Rewrite the Abstract so it is self-contained for a general ITS reader | SC-7 | major (EIC W4) / minor (R3 W7): SPLIT, arbitrated | EIC W4: text: Abstract "not robust to the convex-hull frontier (step frontier: 0.09 percentage points; phase shares −0.6% while the lead brakes, +7.9% after it stops)"; Abstract "With that stop, unless those plans count as unsafe, too little room remains, phase by phase, for the braking prior's share to be measured." · R3 W7: text: Abstract "With that stop, unless those plans count as unsafe, too little room remains, phase by phase, for the braking prior's share to be measured." | EIC 5 (abstract conventions are core editorial competence) · R3 4 (communicating validation evidence to integrators and assessors) | EIC; R3 (disputed severity) | must_fix | section: Abstract | `editorial_conformance_unmet` → section: Abstract |
| R6 | Complete the author block and finalise the AI-use disclosure | SC-16, SC-18 | minor (EIC W11); minor (EIC W12) | EIC W11: text: Author block "[AUTHOR BLOCK: filled by the author]"; Data and Code Availability "[repository and DOI to be added by the author]" · EIC W12: text: Acknowledgment "AI-generated content (IEEE policy): Claude [model and version] drafted the text of the Abstract, Sections I–VII and the Supplementary Material" | 5 (direct observation; submission readiness) · 5 (bracketed placeholders and an approval note observed) | EIC | must_fix (submission gate) | sentence: Author block; Acknowledgment | `reporting_requirement_unmet` → section: Author block and Acknowledgment |
| R7 | Deposit both plans (with amendments and lock manifests), the code and the per-decision arrays under an archived DOI that referees can access; fill in the Data and Code Availability statement; state which raw recordings can be shared | SC-17 | minor (EIC W11) / major (R1 W5): SPLIT, arbitrated | EIC W11: text: Author block "[AUTHOR BLOCK: filled by the author]"; Data and Code Availability "[repository and DOI to be added by the author]" · R1 W5: absence: §III-A and Data and Code Availability — expected CARLA version, map, weather and sensor simulation, CenterPoint checkpoint and training data, CANMOT per-class noise matrices and gating, per-run scenario parameters, recording-planner settings, and deposited code, plans and per-decision arrays; checked §III-A, §III-B, Table I, Data and Code Availability, Supplement S1, S2 and S4, and a full-text search of the manuscript and supplement | EIC 5 (direct observation) · R1 4 (absences confirmed by full-text search) | EIC; R1 (disputed severity) | must_fix | other (surface_id `repository_deposit`): Data and Code Availability; external archive | `method_reproducibility_unresolved` → dataset: plans, code and per-decision arrays |
| R8 | Replace "at most about 0.4%" (Abstract, contribution 2, §V-A, §VII) with a bound from the validated method of R9 or a descriptive statement; if a basic interval is kept, print both ends | SC-23 | minor (EIC W16) / major (R1 W1): SPLIT, arbitrated | EIC W16: text: Abstract "recovers at most about 0.4% of it"; §V-A "an interval chosen after the results because the percentile interval excludes the point; its coverage is not verified for this non-smooth statistic" · R1 W1: text: §V-A para. 2 "The point lies above the 97.5th percentile of its run-bootstrap distribution (median 0.0001; largest of 20,000 resamples 0.0025)" | EIC 3 (bootstrap details outside competence; wording only) · R1 4 (resampling theory; could not rerun without per-run arrays) | EIC; R1 (disputed severity) | must_fix | sentence: Abstract; §I contribution 2; §V-A; §VII | `claim_scope_unsupported` → claim: "at most about 0.4%" |
| R9 | Validate the bootstrap for the step-frontier shares: state the caution-grid handling, estimate actual coverage, report intervals from a method that passes with an α-stratified sensitivity, and re-apply the five fixed NIS-inflated rules | SC-25, SC-26, SC-27 | major (R1 W1) | text: §V-A para. 2 "The point lies above the 97.5th percentile of its run-bootstrap distribution (median 0.0001; largest of 20,000 resamples 0.0025)" | 4 (resampling theory for non-smooth functionals and clustered data; could not rerun without per-run arrays) | R1 | must_fix | re_analysis: stored per-run arrays; §IV-B; §V-A; Table II; Table S5 | `acceptance_criterion_unmet` → claim: RR(N) and RR(NA) intervals and the NIS-inflated "distinguishable from zero" wording |
| R10 | Judge censored reaction-and-stop pairs against the logged truth beyond 3 s until the stop finishes (or explain why that truth cannot be used); report this as the estimate and keep counts (i) and (ii) as sensitivity analyses | SC-28 | major (R1 W2); DA M5: major | R1 W2: text: §V-C para. 2 "Count (ii) is driven by these pairs, which outnumber the 3,334 unsafe pairs" · DA M5: text: Section IV-C "The 3 s truth window cannot judge plans whose stop is not finished inside it; the reaction-and-stop scoring keeps their flags"; Section V-C "Count (ii) is driven by these pairs, which outnumber the 3,334 unsafe pairs" | R1 3 (inferred from the definitions of counts (i) and (ii)) · DA 4 (Section V-C, Tables III, IV, S10 and stopping-time arithmetic) | R1; DA-corroborated (M5) | must_fix | re_analysis: stored truth windows; §IV-C; §V-C; Table III; Tables S6 and S10 | `evidence_gap_remains` → claim: Abstract "12% … 53%" and §VII count (ii) share |
| R11 | Rerun the 3 s scoring with caution counted over all evaluated decisions (signed) for every arm and population; print the results beside Table II; revise the 83% sentence and the Conclusion if a sign or branch changes | SC-29 | major (R1 W3); DA M3: major | R1 W3: text: §IV-A "Decisions whose selected row is unsafe do not enter this average" and §VI Limits "count caution over truly safe selections only, and their sensitivity to that choice is untested" · DA M3: text: Section VI "The 3 s shares, including the 83% and the 0.665, count caution over truly safe selections only"; Section V-C "With the ego moving, however, it recovers less than the class average" | R1 4 (the selection effect follows from the definition) · DA 4 (Table S13 and the Limits paragraph) | R1; DA-corroborated (M3) | must_fix | re_analysis: existing signed-caution code; Table II; Table S5 | `evidence_gap_remains` → claim: 3 s shares (83%, 0.665, 0.61, 38%) |
| R12 | Run a truncation sensitivity on the post-stop segment, and isolate the cross-phase mechanism with a per-phase-scale frontier | SC-30, SC-31 | major (R1 W4); DA M1: major | R1 W4: text: §IV-B para. 2 "it is 2.6 times the decision-weighted mean of the three phase rooms (2.13 points)" · DA M1: text: Section IV-B "how one margin scale spends caution across phases of very different risk, a mechanism that no analysis here isolates"; Section VI "These phase gains, about 127 decisions, are a third of its pooled gain of about 383 decisions" | R1 4 (the aggregation arithmetic is the paper's own) · DA 4 (arithmetic on Tables S5, S9 and Section VI) | R1; DA-corroborated (M1) | must_fix | re_analysis: stored arrays; §IV-B; §V-A; §VI; §VII | `claim_scope_unsupported` → claim: pooled room 5.6 points and 83% |
| R13 | Print the ego-moving share and/or the phase-weighted share beside the pooled 83% in the Abstract and Conclusion, and name the population that defines the room | SC-32 | major (R1 W4) / minor (R2 W10): SPLIT, arbitrated | R1 W4: text: §IV-B para. 2 "it is 2.6 times the decision-weighted mean of the three phase rooms (2.13 points)" · R2 W10: text: Abstract "a fixed 3 m/s² braking prior recovers 83% [75%, 90%]" | R1 4 (the paper's own aggregation arithmetic) · R2 4 (follows from the paper's own tables) | R1; R2 (disputed severity) | must_fix | sentence: Abstract; §VII | `claim_scope_unsupported` → claim: Abstract "83% [75%, 90%]" |
| R14 | Add a configuration table covering everything needed to regenerate the data, with software versions | SC-33 | major (R1 W5) | absence: §III-A and Data and Code Availability — expected CARLA version, map, weather and sensor simulation, CenterPoint checkpoint and training data, CANMOT per-class noise matrices and gating, per-run scenario parameters, recording-planner settings, and deposited code, plans and per-decision arrays; checked §III-A, §III-B, Table I, Data and Code Availability, Supplement S1, S2 and S4, and a full-text search of the manuscript and supplement | 4 (absences confirmed by full-text search) | R1 | must_fix | section: §III-A (new table) or Supplement S1–S2 | `method_reproducibility_unresolved` → section: §III-A |
| R15 | Rename CK3 a constant-deceleration braking prediction; drop "RSS-style" for it; contrast it with RSS's worst-case bound in one sentence; keep the RSS label for the S3.1 rule | SC-42 | major (R2 W1) / minor (R3 W5): SPLIT, arbitrated | R2 W1: text: §VI "a fixed 3 m/s² braking prediction, an RSS-style assumption [37], captures 83% of the pooled room" · R3 W5: text: §VI "a fixed 3 m/s² braking prediction, an RSS-style assumption [37]" | R2 4 (RSS and constant-deceleration prediction are core to the area) · R3 4 (RSS and safe-distance models are core expertise) | R2; R3 (disputed severity) | must_fix | sentence: §II; §VI | `claim_scope_unsupported` → claim: §VI "an RSS-style assumption [37]" |
| R16 | State how 3 m/s² was chosen on the tuning runs, and add to Limits that it lies inside the evaluation runs' braking range | SC-43 | major (R2 W1) | text: §VI "a fixed 3 m/s² braking prediction, an RSS-style assumption [37], captures 83% of the pooled room" | 4 (core to the area; has not seen how the tuning runs led to 3 m/s²) | R2 | must_fix | sentence: §III-C; §VI Limits | `claim_scope_unsupported` → claim: 83% as the share of a scenario-matched deceleration |
| R17 | State that a wrong go means contact (0 m gap) and that model 2's 2 m gap and 7 m/s² are not used, and why; score the perfect oracle O at the 2 m gap and report den₀ (and shares where evaluable) | SC-45, SC-46 | major (R2 W2); major (R3 W2) | R2 W2: text: Supplement S5, footnote to Table S6, "the 3 s oracle is not an oracle" · R3 W2: text: §V-C "The as-scored conclusion at τ = 0.75 s therefore rests on the performance-model values of the 01 series"; Table S6 caption "No ratio is printed at a 2 m gap, where the 3 s oracle is not an oracle" | R2 3 (no perfect oracle computed at 2 m) · R3 3 (relies on the manuscript's statement of model 2 parameters in S3.1) | R2; R3 | must_fix | re_analysis: stored safe-row flags; Abstract; §IV-C; Table S6; §VI Limits | `claim_scope_unsupported` → claim: Abstract "12% / 53%" and the room's location |
| R18 | Reword the §V-C sentence that the conclusion "rests on the performance-model values", and the matching Limits clause, as two ego parameters of model 2 used as a nominal parameterisation with a zero standstill gap | SC-56 | minor (R2 W11) / major (R3 W2): SPLIT, arbitrated | R2 W11: text: §V-C "The as-scored conclusion at τ = 0.75 s therefore rests on the performance-model values of the 01 series" · R3 W2: text: §V-C "The as-scored conclusion at τ = 0.75 s therefore rests on the performance-model values of the 01 series"; Table S6 caption "No ratio is printed at a 2 m gap, where the 3 s oracle is not an oracle" | R2 3 (knows the regulatory models in outline) · R3 3 (could not open Annex 3) | R2; R3 (disputed severity) | must_fix | sentence: §V-C; §VI Limits | `claim_scope_unsupported` → claim: §V-C "rests on the performance-model values" |
| R19 | Fence the covariance null against removing or freezing a deployed stack's covariance margin; report D(N, F0) near the 45 track initialisations or state that they are too few; name new and cut-in actors as untested | SC-58 | major (R3 W1) | text: Supplement S9 "Every lead-braking decision has a track in the oldest age band, so the planned split by track age is empty."; §VI "a class average does as well as the tracker's covariance" | 4 (safety-case scoping and misuse analysis are core expertise) | R3 | must_fix | re_analysis: stored arrays (track initialisations); §I Scope; §VI; §VI Limits | `claim_scope_unsupported` → claim: §VI "a class average does as well as the tracker's covariance" |
| R20 | Apply the ratio check to the tuning runs of the other five scenario families and report the median N/F0 ratio per family; if the levels differ, state that cross-family reallocation of caution is untested | SC-59 | major (R3 W1) | text: Supplement S9 "Every lead-braking decision has a track in the oldest age band, so the planned split by track age is empty."; §VI "a class average does as well as the tracker's covariance" | 4 (core expertise; the cross-family mechanism is R3's inference, not a result of the paper) | R3 | must_fix | re_analysis: tuning runs of the other five families | `evidence_gap_remains` → claim: transfer of the null across scenario families |

### Required Item Details

> **Ordinal contract (#576/#670):** `R<n>` is a transport reference, never a work rank. Numbering follows the immutable roadmap source order filtered to `must_fix`. Required blocks are exactly `R1..R20`, with no gaps, duplicates or extras.

**R1: Title and headline pose the expected null as an open question**
- **Problem**: the title asks in general whether "a Kalman Tracker's Covariance" improves decisions, while §I states that the fixed-noise null is expected.
- **Source**: EIC W1 (major, conf 4) and R2 W3 (minor, conf 4). SPLIT on severity, arbitrated in Disagreement 1.
- **Requirement**: qualify the title to the fixed-noise case, or recast it around the decision-level evaluation. Add one Abstract sentence saying that the null is the steady-state expectation and that the measured contribution is the room, its location and its commitment dependence.
- **Acceptance criteria**: The title names the fixed-noise case or the decision-level evaluation, and the Abstract and §I state that the covariance null is the expected steady-state result and that the measured contribution is the room, its location and its dependence on the commitment.

**R2: The contribution list presents an expected confirmation as a contribution**
- **Problem**: contribution 2 offers confirmation of the Riccati steady state as a contribution. Meanwhile the evaluation design and the commitment dependence, which the Journal-Fit seat judges to be new for an ITS reader, are under-sold.
- **Source**: EIC W1 (major, conf 4).
- **Requirement**: present the evaluation design (equal caution, oracle positive control, graded oracles of Table S12, explicit commitment model) and the commitment dependence as contributions. Introduce the covariance diagnostic as a confirmatory test of an expected steady state. Add one §I sentence on why the expected null still needed measuring (detections, misses, track age). The order within the list is the author's choice.
- **Acceptance criteria**: The §I contribution list presents the evaluation design and the commitment dependence as contributions, introduces the covariance diagnostic as a confirmatory test of an expected steady state, and §I says in one sentence why the expected null was still measured.

**R3: The practical take-away under the realistic commitment, and a conditional Conclusion**
- **Problem**: the positive result kept in the Conclusion (the braking prior's 83%) comes from the 3 s scoring, which §IV-C calls a stress scoring. §VI does not tell developers, testers or assessors what to do differently, or which scoring should guide practice.
- **Source**: EIC W2 (major, conf 4).
- **Requirement**: add a §VI paragraph on implications for testing and development. It should state which commitment model the author considers representative of the planner's replanning, and why. It should give the practical reading under each model and name the closed-loop test that would settle the question. Running the braking prior in the Supplement S3 closed loop is the seat's optional stronger fix. Word the Conclusion's last sentence conditionally in the same terms.
- **Acceptance criteria**: §VI contains an implications paragraph that states which commitment model the author considers representative and why, the practical reading under each, and the closed-loop test that would settle it, and the Conclusion's last sentence is conditional on the commitment model in the same terms.

**R4: Length against the recommended 10 pages**
- **Problem**: the Journal-Fit seat estimates 12–14 printed pages against the recommended 10, mostly from appendix-grade material and repetition. This is an estimate, not a typeset count.
- **Source**: EIC W3 (major, conf 4).
- **Requirement**: apply the seat's cuts:
  - a five-row Table IV;
  - §V-D moved to S9 with a two-sentence summary;
  - the §III-A stopping-point paragraph moved to S2;
  - the signed-caution and stop-deceleration paragraphs condensed;
  - one sentence on provenance;
  - each headline number stated once;
  - contribution 3 cut to two sentences.

  This interacts with R11: the 3 s signed-caution values that R11 adds must stay visible in the main text in compact form.
- **Acceptance criteria**: The appendix-grade material named in EIC W3 is moved to the Supplement or cut without removing any result, the 3 s signed-caution values required by R11 remain visible in the main text, and the response states the revised page estimate.

**R5: The Abstract is not self-contained**
- **Problem**: the 249-word Abstract uses step and convex-hull frontiers, phase shares and "those plans" without definition. It carries about twenty numbers and ends on what cannot be measured.
- **Source**: EIC W4 (major, conf 5) and R3 W7 (minor, conf 4). SPLIT on severity, arbitrated in Disagreement 2.
- **Requirement**: rewrite the Abstract in plain terms in about 200–230 words: the question, the method in one sentence, three results and one sentence of implication. Define "commitment" at first use. Drop the frontier types, the phase shares and the count (ii) clause, or define them in words. Record any mapping to the plan's consequence rules in Table S4.
- **Acceptance criteria**: The Abstract stays within 250 words, defines or avoids every paper-specific term (frontier types, phase shares, count (ii), "those plans", "commitment"), ends on a sentence of implication, and carries any wording changes required by R1, R8, R10, R11, R13 and R17.

**R6: Submission-readiness placeholders**
- **Problem**: the author block is a placeholder. The AI-use disclosure is an unapproved draft with bracketed placeholders for the model, the version and the verification scope.
- **Source**: EIC W11 (minor, conf 5) and EIC W12 (minor, conf 5).
- **Requirement**: complete the author block. Delete the approval note. Name the tool and its version. State the sections that contain AI-generated text, the extent of AI involvement in the code and the literature summaries, and what the author verified. Reconcile the disclosure with the first Acknowledgment paragraph.
- **Acceptance criteria**: The author block is complete and the Acknowledgment's AI-use disclosure names the tool and version, the sections and extent of AI-generated text and of AI involvement in code and literature summaries, and what the author verified, with no bracketed placeholder or approval note left.

**R7: Repository and deposit**
- **Problem**: the Data and Code Availability statement is a placeholder. §IV-D says the plan, its SHA-256 and every amendment are released with the code, but nothing has been deposited, so the pre-specification cannot be checked.
- **Source**: EIC W11 (minor, conf 5) and R1 W5 (major, conf 4). SPLIT on severity, arbitrated in Disagreement 3.
- **Requirement**: deposit the following under an archived DOI that referees can access: both plans with all amendments and lock manifests; the analysis code; and the per-decision arrays (clearances, critical values for every arm, truth windows, phase labels, run identifiers). State which raw recordings can be shared.
- **Acceptance criteria**: The Data and Code Availability statement gives a repository URL and archived DOI, accessible to referees, containing both plans with all amendments and lock manifests, the analysis code and the per-decision arrays needed to recompute Tables II–IV, and states which raw recordings can be shared.

**R8: "At most about 0.4%" presented as a bound**
- **Problem**: the phrase uses the upper end of a basic bootstrap interval chosen after the results, with unverified coverage. The lower end of that interval excludes zero, while the percentile interval includes zero.
- **Source**: EIC W16 (minor, conf 3) and R1 W1 (major, conf 4). SPLIT on severity, arbitrated in Disagreement 5.
- **Requirement**: replace the phrase with a bound from the method validated under R9, or with a descriptive statement: 0.6 of 8,290 decisions, and a largest-of-20,000-resamples value of 0.25%. If a basic interval is kept, print its lower end as well.
- **Acceptance criteria**: No text presents "at most about 0.4%" as a bound unless it comes from the interval method validated under R9; otherwise the tracker covariance's share is stated descriptively, and any basic interval kept is printed with both ends.

**R9: Unvalidated bootstrap for the step-frontier shares**
- **Problem**: RR(N) and RR(NA) are ratios of running-minimum (step-frontier) differences. Naive percentile and basic bootstraps are not generally consistent for such non-smooth functionals. The RR(N) point lies above its own percentile interval and just below its basic interval. The NIS-inflated wording (rule 5) rests on the same machinery, applied to 35 unequal, unstratified clusters. It is also unstated whether the 201 caution levels are rebuilt in each resample.
- **Source**: R1 W1 (major, conf 4). This is the basis of R1's D1 block.
- **Requirement**:
  1. State the caution-grid handling.
  2. Estimate the actual coverage of the percentile and basic intervals on the stored arrays, using a run-level double bootstrap or m-out-of-n subsampling of runs.
  3. Report the primary intervals from a method that passes, with a sensitivity analysis stratified by recording setting α.
  4. Re-apply the five fixed NIS-inflated rules and print the branch they select.
- **Acceptance criteria**: §IV-B states whether the caution grid is rebuilt per resample, the response reports estimated coverage of the percentile and basic intervals for RR(N) and RR(NA) by a run-level double bootstrap or m-out-of-n subsampling, the primary intervals come from a method that passes with an α-stratified sensitivity, and the five fixed NIS-inflated rules are re-applied with the selected branch printed.

**R10: Censored reaction-and-stop plans are imputed rather than judged**
- **Problem**: at τ = 0.75 s, 5,356 decision–row pairs cannot be judged in the 3 s window, against 3,334 pairs judged unsafe. "As scored" and count (ii) are two single imputations that do not bound the room. Yet only 153 pairs have a stop still unfinished when the recording ends.
- **Source**: R1 W2 (major, conf 3). DA M5 (major, conf 4) reports the same sub-claim. The DA is not an independent seat and does not change the count.
- **Requirement**: score each censored pair against the logged truth beyond the 3 s window until its stop finishes. If needed, restrict the evaluated population to decisions whose logged future covers the stop. Report that as the reaction-and-stop result, with "as scored" and count (ii) as sensitivity analyses. If the logged truth cannot be used, explain why and present the two counts as imputation alternatives.
- **Acceptance criteria**: Censored reaction-and-stop pairs are judged against the logged truth until the stop finishes (or the manuscript explains why that truth cannot be used), that result is reported with its interval as the reaction-and-stop estimate, counts (i) and (ii) appear as sensitivity analyses, and the Abstract no longer presents the two counts as separate findings.

**R11: Caution is outcome-conditioned at 3 s**
- **Problem**: caution is averaged only over decisions whose selected row is truly safe. At τ = 0.75 s, the signed alternative reversed the braking prior's sign with the ego moving and phase-weighted. The 3 s headline shares were never rerun with it.
- **Source**: R1 W3 (major, conf 4). DA M3 (major, conf 4) reports the same sub-claim.
- **Requirement**: rerun the 3 s scoring with caution counted over all evaluated decisions (signed), for every arm and every population of Table S5, using the existing signed-caution code. Print the results beside Table II. Revise the Abstract's 83% sentence and the Conclusion if a sign or branch changes.
- **Acceptance criteria**: The 3 s scoring is rerun with signed caution over all evaluated decisions for every arm and every population of Table S5, the values are printed beside Table II, and the Abstract's 83% sentence and the Conclusion are revised wherever the ego-moving or phase-weighted value changes sign or branch.

**R12: The pooled estimand and the cross-phase mechanism**
- **Problem**: 82.7% of evaluated decisions come after the stop, so the pooled room (5.56 points) is weighted by how long each recording ran after the stop. It is 2.6 times the decision-weighted mean of the phase rooms. About two-thirds of the prior's pooled gain is attributed to a cross-phase mechanism that is never isolated.
- **Source**: R1 W4 (major, conf 4). DA M1 (major, conf 4) reports the same sub-claim.
- **Requirement**: cap each run's post-stop segment at stated durations (for example 1, 2 and 5 s) and recompute R and every RR. Give F0 and each arm one margin scale per phase, and trace the frontier at equal total caution. This separates the value of knowing the phase from per-decision information. Word contribution 3 and §VII according to the result.
- **Acceptance criteria**: R and every RR are reported with each run's post-stop segment capped at stated durations, and a per-phase-scale frontier at equal total caution separates the value of knowing the phase from per-decision information, with contribution 3 and §VII worded according to the result.

**R13: The pooled 83% without its population**
- **Problem**: the Abstract and the Conclusion give only the pooled 83%. With the ego moving the share is 0.47 [0.35, 0.57], and phase-weighted against a perfect oracle it is 0.665.
- **Source**: R1 W4 (major, conf 4) and R2 W10 (minor, conf 4). SPLIT on severity, arbitrated in Disagreement 6.
- **Requirement**: print the ego-moving and/or phase-weighted share beside the 83%, and name the population that defines the room. Trim elsewhere to stay within the abstract limit.
- **Acceptance criteria**: The Abstract and the Conclusion print the ego-moving share and/or the phase-weighted perfect-oracle share beside the pooled 83% and name the population that defines the room.

**R14: Regeneration configuration**
- **Problem**: the tracker is "configured as in [9]", a manuscript under review. The CARLA version, map, weather and sensor simulation, the CenterPoint checkpoint and its training data, CANMOT's noise and gating, the per-run scenario parameters and the recording-planner settings are not given.
- **Source**: R1 W5 (major, conf 4).
- **Requirement**: add a configuration table covering these items, with software versions.
- **Acceptance criteria**: A configuration table gives the CARLA version, map, weather and sensor simulation, the CenterPoint checkpoint and training data, CANMOT's per-class process and measurement noise and gating, the per-run scenario parameters (initial gap, onset time, deceleration) and the recording planner's settings, with software versions.

**R15: The "RSS-style" label**
- **Problem**: RSS [37] is a worst-case envelope. CK3 is a nominal constant-deceleration prediction. The paper also uses the label for both CK3 and the S3.1 rule.
- **Source**: R2 W1 (major, conf 4) and R3 W5 (minor, conf 4). SPLIT on severity, arbitrated in Disagreement 7.
- **Requirement**: call CK3 a constant-deceleration braking prediction (3 m/s²) throughout. Place it among physics-based motion models. Add one sentence contrasting it with RSS's worst-case bound on the front vehicle's braking, and keep the RSS label for S3.1.
- **Acceptance criteria**: CK3 is called a constant-deceleration braking prediction (3 m/s²) throughout, no "RSS-style" label is applied to it, one sentence contrasts it with RSS's worst-case bound on the front vehicle's braking, and the RSS label is kept only for the S3.1 rule.

**R16: The choice of 3 m/s²**
- **Problem**: 3 m/s² lies inside the recorded leads' braking range (2.0–5.5 m/s²), and the manuscript does not say how it was chosen.
- **Source**: R2 W1 (major, conf 4).
- **Requirement**: state how 3 m/s² was chosen on the tuning runs, and add the range relation to Limits. The deceleration sweep is optional and carried as S20.
- **Acceptance criteria**: The manuscript states how 3 m/s² was chosen on the tuning runs, and §VI Limits states that it lies inside the evaluation runs' lead-braking range (2.0–5.5 m/s²).

**R17: Contact-only room under a regulatory model with a 2 m gap**
- **Problem**: a wrong go is defined as contact, and the reaction-and-stop scoring uses a zero standstill gap. The adopted performance model 2 also specifies a 2 m gap and 7 m/s² for the other vehicle. At 2 m the 3 s oracle is not an oracle, and no perfect oracle O is reported there.
- **Source**: R2 W2 (major, conf 3) and R3 W2 (major, conf 3). CORROBORATED. R2 offers the scoring of O at 2 m as its stronger fix; R3 lists it as a required step.
- **Requirement**: state the contact criterion and its reason in the Abstract's commitment sentence, in §IV-C and in Limits. Score O at a 2 m gap under the 3 s and τ = 0.75 s scorings, using the existing safe-row flags, and report den₀. Report RR₀(N) and RR₀(CK3) where evaluable, or state that no share is evaluable.
- **Acceptance criteria**: The Abstract's commitment sentence, §IV-C and Limits state that a wrong go means contact at zero standstill gap and that model 2's 2 m gap and 7 m/s² are not used (and why), and den₀ for the perfect oracle O at a 2 m gap is reported under the 3 s and τ = 0.75 s scorings, with RR₀(N) and RR₀(CK3) where evaluable or an explicit statement that no share is evaluable.

**R18: "Rests on the performance-model values"**
- **Problem**: the §V-C sentence implies regulatory backing that the scoring does not have. Only two ego parameters are used, with a zero gap, and outside the regulation's ALKS scope.
- **Source**: R2 W11 (minor, conf 3) and R3 W2 (major, conf 3). SPLIT on severity, arbitrated in Disagreement 9.
- **Requirement**: replace the sentence and the matching Limits clause with wording that the scoring uses two ego parameters of model 2 (0.75 s, 6 m/s²) as a nominal parameterisation with a zero standstill gap.
- **Acceptance criteria**: The §V-C sentence and the matching Limits clause say that the scoring uses two ego parameters of performance model 2 (0.75 s, 6 m/s²) as a nominal parameterisation with a zero standstill gap, and no sentence says the conclusion rests on the regulation's values.

**R19: The deployment fence**
- **Problem**: nothing stops a reader from replacing a deployed stack's covariance margin with a class constant. Yet every lead-braking decision has a mature track, and newly detected, re-acquired or cut-in actors are essentially absent from the evaluated decisions.
- **Source**: R3 W1 (major, conf 4).
- **Requirement**:
  1. Add a fence sentence to §I Scope and §VI.
  2. Count the evaluated decisions within about 1 s of the 45 initialisations, and report D(N, F0) on them or state that they are too few.
  3. Name newly detected and cut-in actors as untested in Limits.
- **Acceptance criteria**: §I Scope and §VI state that the results do not support removing or freezing a deployed stack's covariance margin, the manuscript reports D(N, F0) on evaluated decisions within about 1 s of the 45 track initialisations or states that they are too few, and Limits names newly detected, re-acquired and cut-in actors as untested.

**R20: Cross-family scale reallocation**
- **Problem**: a deployed stack tunes one margin scale across its whole operating domain. The paper's own phase finding suggests that a covariance whose level differs by scenario family could carry value that a single-family test cannot see. This is R3's inference.
- **Source**: R3 W1 (major, conf 4).
- **Requirement**: run the ground-truth-free ratio check of Fig. 2(b) on the tuning runs of the other five scenario families, and report the median N/F0 ratio for each.
- **Acceptance criteria**: The median N/F0 margin ratio on binding rows is reported for the tuning runs of each of the other five scenario families, and if the levels differ the manuscript states that a single tuned scale could reallocate caution across families and that this is untested.

### Suggested Revisions (Should Fix)

| Transport ref | Revision Item | Sub-Claim(s) | Severity | Evidence Anchor | Confidence | Source | Obligation class | Cost scope | Bounded consequence |
|---|---|---|---|---|---|---|---|---|---|
| S1 | Optional stronger fix: apply the same evaluation to one source whose covariance varies per decision (the calibrated covariance of [9], or an IMM tracker) | SC-3 | major (EIC W1) | text: §I para. 4 "For a fixed-noise Kalman filter the covariance's null is expected"; §II Novelty "our contribution is to measure its decision consequence against an oracle with demonstrated room" | 4 (contribution framing) | EIC | consider | new_data: tracker output with a per-decision covariance | `evidence_gap_remains` → claim: the method discriminates on a real tracker |
| S2 | Extend the novelty search to ITS venues, threat assessment and collision probability, and IMM/adaptive-filter trackers in ACC and collision warning; add a §II positioning paragraph; qualify "Novelty, with its limits" if needed | SC-8 | minor (EIC W5); minor (R2 W8) | EIC W5: text: Supplement S6 "the literature on interacting-multiple-model and adaptive filtering was not searched for a planner-side test" · R2 W8: absence: §II Related Work and its Novelty paragraph — expected a discussion of probabilistic threat assessment that turns tracking uncertainty into longitudinal collision-avoidance or warning decisions; checked §I, §II, §VI, references [1]–[43], Supplement S6 | EIC 3 (reference list and stated search scope) · R2 3 (has not checked for a study at equal false-intervention rate) | EIC; R2 | should_fix | section: §II; Supplement S6 | `claim_scope_unsupported` → claim: §II novelty statement |
| S3 | Upload [9] as a confidential related manuscript and state shared and new content in the cover letter; cite published versions of [8], [14], [17] and [19] where available | SC-9, SC-10 | minor (EIC W6) | text: §I Scope "A related manuscript by the author [9], under review, asks how to size a margin from a tracker's covariance" | 4 (standard editorial handling) | EIC | should_fix | other (surface_id `cover_letter`): cover letter; reference list | `reporting_requirement_unmet` → manuscript: related-manuscript disclosure |
| S4 | Give plain one-sentence definitions of room, caution and the two commitment models in §I; move the Notation table to the start of §IV; add a 2–3 sentence plain summary | SC-11 | minor (EIC W7); minor (R3 W7) | EIC W7: text: §I contribution 3 "Against a perfect oracle for that scoring, the phase-weighted avoidable wrong-go is 6% of the pooled amount"; §V-C "the inflated covariance 0.012" · R3 W7: text: Abstract "With that stop, unless those plans count as unsafe, too little room remains, phase by phase, for the braking prior's share to be measured." | EIC 4 (read directly from the text) · R3 4 (communicating evidence to integrators) | EIC; R3 | should_fix | section: §I; §IV (Notation table) | `interpretive_ambiguity_remains` → section: §I and contribution 3 |
| S5 | Use one name per arm after §III-C; relabel Table III, Table S6 and Fig. 4(b) with RR_E(N), plus a distinct symbol for the 3 s oracle's advantage under reaction-and-stop | SC-12, SC-13 | minor (EIC W7); minor (EIC W8) | EIC W7: text: §I contribution 3 "Against a perfect oracle for that scoring, the phase-weighted avoidable wrong-go is 6% of the pooled amount"; §V-C "the inflated covariance 0.012" · EIC W8: table: Table III, header columns R (pp) and RR(N), read against the Notation table rows for R and RR_E(A) | 4 · 4 (read directly from the tables and captions) | EIC | should_fix | sentence: text; Table III; Table S6; Fig. 4(b) | `reader_traceability_reduced` → table: Table III, Table S6 and Fig. 4(b) |
| S6 | Bring a compact version of Table S12 (p = 0.25, 0.5, 0.75; all decisions, ego moving, lead braking, phase-weighted; 3 s) into §IV-B or beside Fig. 3 | SC-14 | minor (EIC W9) | table: Table S12 (graded oracles), cited from Sections IV-B, V-B, V-C and VI | 4 (structural judgement from cross-references) | EIC | should_fix | section: §IV-B | `reader_traceability_reduced` → table: Table S12 |
| S7 | Describe post hoc analyses neutrally; drop references to reviews and to rules governing the abstract; keep the audit trail in S4; declare any previous venue in the cover letter | SC-15 | minor (EIC W10) | text: §IV-C "Two further checks follow review requests"; §V-C "the weakest of the three statistics that the plan fixed for the abstract" | 4 (editorial convention) | EIC | should_fix | sentence: §IV-C; §IV-D; §V-C; Acknowledgment | `editorial_conformance_unmet` → section: §IV-C, §IV-D, §V-C |
| S8 | Give each figure and table one self-contained in-paper caption (data, number of decisions, interval type, frontier) and drop the supplementary duplicate | SC-19 | minor (EIC W13) | figure: Fig. 2(b) and its two captions (main text and supplementary full caption) | 4 (figure image and both captions viewed) | EIC | should_fix | sentence: captions of Figs. 1–4 and Tables I–IV | `editorial_conformance_unmet` → figure: Figs. 1–4 |
| S9 | Characterise the 1,127 rows outside the 5% band of Fig. 2(b), for example by track age or re-initialisation, in the text and caption | SC-20 | minor (EIC W13); minor (R2 W3) / major (R3 W1): SPLIT, arbitrated | EIC W13: figure: Fig. 2(b) and its two captions (main text and supplementary full caption) · R2 W3: text: Title "Does a Kalman Tracker's Covariance Improve Car-Following Decisions?" · R3 W1: text: Supplement S9 "Every lead-braking decision has a track in the oldest age band, so the planned split by track age is empty."; §VI "a class average does as well as the tracker's covariance" | EIC 4 · R2 4 · R3 4 | EIC; R2; R3 (disputed severity) | should_fix | re_analysis: stored binding rows; Fig. 2(b) caption | `interpretive_ambiguity_remains` → figure: Fig. 2(b) |
| S10 | Adopt one number-format convention (for example, percentages to two significant figures in prose and decimals to three in tables), with intervals rounded to the precision the bootstrap supports | SC-21 | minor (EIC W14) | table: Table II, row RR(N) | 4 (read directly) | EIC | should_fix | sentence: throughout | `reader_traceability_reduced` → manuscript |
| S11 | Qualify the Abstract's held-out phrase: for the room and the tracker covariance, an earlier exploratory analysis had examined these runs (a transfer, not a replication) | SC-22 | minor (EIC W15); minor (R1 W10) | EIC W15: text: Abstract "On 35 runs not used to design the margins"; §III-A "for them the evaluation runs are a transfer to runs recorded with another planner setting, not a replication" · R1 W10: text: Abstract "On 35 runs not used to design the margins" | EIC 3 (disclosure reading; defers to methodology) · R1 4 (status in body, missing from abstract) | EIC; R1 | should_fix | sentence: Abstract | `claim_scope_unsupported` → claim: Abstract "On 35 runs not used to design the margins" |
| S12 | Add two or three ITS index terms (for example car following, adaptive cruise control, safety evaluation, simulation-based testing) | SC-24 | minor (EIC W17) | text: Index Terms "Autonomous vehicles, collision avoidance, Kalman filters, motion planning, object tracking, uncertainty" | 4 (discoverability convention) | EIC | should_fix | sentence: Index Terms | `editorial_conformance_unmet` → section: Index Terms |
| S13 | Reproduce the logged selections on the evaluation runs with the recorded α, β, p and q; state that lead braking is scripted and no actor's logged trajectory depends on the ego, or quantify where it does | SC-34, SC-35 | minor (R1 W6) | text: Supplement S1 "The replay identity was checked on the tuning runs only" | 3 (plausible but unquantified risk) | R1 | should_fix | re_analysis: evaluation-run replay; Supplement S1 | `method_reproducibility_unresolved` → section: Supplement S1 |
| S14 | State why the five short runs are short; count how many of the 217 changed NA decisions and 304 λ > 1 actor-decisions fall in them; recompute R, RR(N) and RR(NA) with all five excluded | SC-36 | minor (R1 W7) | text: §III-A para. 1 "Thirty runs contribute 271 evaluated decisions each and five short runs 18–53" | 3 (possible concentration; not shown either way) | R1 | should_fix | re_analysis: stored arrays | `evidence_gap_remains` → claim: NIS-inflated share |
| S15 | Report the branch the resolution rule gives at other thresholds (for example 5 and 20); base evaluability on den₀'s lower limit as a sensitivity; disclose in §IV-D what was already known | SC-37 | minor (R1 W8) | text: §IV-C para. 3 "a resolution rule of our choosing" | 3 (timing inferred from §IV-D) | R1 | should_fix | re_analysis: S8.1 aggregates; §IV-C; §IV-D | `claim_scope_unsupported` → claim: the Abstract's last sentence |
| S16 | Where den₀'s interval approaches zero, report D and den₀ with their joint interval or a Fieller-type interval, and flag the cell | SC-38 | minor (R1 W9) | table: Table S10, count (ii), τ = 0.75 s, lead-braking row (RR₀(CK3) 0.266 [0.098, 1.237]; den₀ 45.00 [6.18, 72.22]; 1.57% of resamples at or below zero) | 4 (standard ratio-estimator behaviour) | R1 | should_fix | re_analysis: Tables S9–S10 | `interpretive_ambiguity_remains` → table: Tables S9–S10 |
| S17 | Mark the commitment analyses as descriptive analyses added after the first results, in the Abstract or at least in the Conclusion | SC-39 | minor (R1 W10) | text: Abstract "On 35 runs not used to design the margins" | 4 (status in body, missing from abstract) | R1 | should_fix | sentence: Abstract; §VII | `claim_scope_unsupported` → claim: the commitment sentences |
| S18 | Score CK3 against F0 on the project's benign-driving and other-family runs, or add "on runs in which the lead always brakes" to the Abstract's 83% sentence | SC-40 | minor (R1 W11); DA M2: major | R1 W11: text: §VI "its cost where braking never comes is untested here" · DA M2: text: Section VI "every evaluation run contains a braking lead, so the scenario selection favours it; its cost where braking never comes is untested here" | R1 3 (feasibility depends on scoreable tuning recordings) · DA 4 (the paper states the gap; Table S5) | R1; DA-corroborated (M2) | should_fix | re_analysis: tuning runs of the other families | `claim_scope_unsupported` → claim: Abstract 83% and the §VII location |
| S19 | Repeat the partial and noisy oracles over about 50 draws and report the across-draw spread in Table S12 | SC-41 | minor (R1 W12) | text: Supplement S8.1 "one uniform draw per stored decision" | 3 (spread unknown) | R1 | should_fix | re_analysis: Table S12 | `evidence_gap_remains` → table: Table S12 |
| S20 | Optional stronger fix: report RR(CK3) over a sweep of the assumed deceleration (for example 2, 4, 6, 7 m/s²) | SC-44 | major (R2 W1) | text: §VI "a fixed 3 m/s² braking prediction, an RSS-style assumption [37], captures 83% of the pooled room" | 4 | R2 | consider | re_analysis: CK3 arm at other decelerations | `evidence_gap_remains` → claim: robustness of the 83% to the assumed deceleration |
| S21 | Optional: compute the steady-state covariance at the update interval and the margin ratio it implies; show how common fixed-noise Kalman trackers are in AD perception | SC-47, SC-48 | minor (R2 W3) | text: Title "Does a Kalman Tracker's Covariance Improve Car-Following Decisions?" | 4 (Kalman steady state and field practice) | R2 | consider | re_analysis: Riccati steady-state computation; §II | `evidence_gap_remains` → claim: contribution 2 as a quantitative check of theory |
| S22 | State in §III-B and Table I that the margin is the posterior propagated without process noise, and why; note that a common class-level Q leaves the N-versus-F0 comparison unchanged (optionally, report room and RR(CK3) with F P Fᵀ + Q) | SC-49 | minor (R2 W4) | text: Supplement S9 "the planner's propagated deviation (no process noise) is too narrow on average by a factor of about 3.2" | 4 (standard estimation material) | R2 | should_fix | sentence: §III-B; Table I | `interpretive_ambiguity_remains` → section: §III-B |
| S23 | Retitle §V-B; state in §II and §VI that NA isolates the covariance channel, not the gain or state-estimate effect of adaptive filtering; list that effect with IMM as untested | SC-50 | minor (R2 W5) | text: §V-B heading "An Adaptive Covariance and Simple Priors" | 4 (adaptive and manoeuvring-target filtering) | R2 | should_fix | sentence: §II; §V-B heading; §VI | `claim_scope_unsupported` → section: §V-B |
| S24 | Present §V-D in §VI and §VII as a consistency check of the ratio result (ranking located in the state's age), or test the covariance's own variation per phase directly | SC-51 | minor (R2 W6); R1 disputes existence (no severity tag): SPLIT, arbitrated | R2 W6: text: §V-D "the ranking comes from the state's age, not from the tracker's covariance" · R1 S5: figure: Fig. 2(b), with §V-D | R2 4 (common uncertainty–error checks) · R1 none (strength entry; no per-finding Confidence) | R2; R1 (disputed existence) | should_fix | sentence: §VI para. 1; §VII | `claim_scope_unsupported` → claim: §VII "its stated deviation ranks the realised error no better than the class average's" |
| S25 | State where the ~2 Hz update rate comes from; add it to Limits; scope the §V-D ranking and the lead-braking room to it | SC-52 | minor (R2 W7) | text: §III-A "the tracker updates the lead at about 2 Hz (68 updates in a full-length run)" | 3 (inference; the origin may be documented in [9]) | R2 | should_fix | sentence: §III-A; §VI Limits | `claim_scope_unsupported` → section: §V-D |
| S26 | Phrase the Conclusion's location claim as a ranking among the tested sources, and name the constant time-gap margin as untested | SC-53 | minor (R2 W9) | table: Table I, margin sources F0, N, NA, E, CK3, AM and Q | 3 (time-gap share not predictable from the text) | R2 | should_fix | sentence: §VII | `claim_scope_unsupported` → claim: §VII location claim |
| S27 | Optional stronger fix: add a constant time-gap arm swept like the others (s = (h·v_ego)², or the R157 d_min(v)) | SC-54 | minor (R2 W9) | table: Table I, margin sources F0, N, NA, E, CK3, AM and Q | 3 | R2 | consider | re_analysis: new margin arm on stored decisions | `evidence_gap_remains` → table: Table I margin sources |
| S28 | Describe the 01-series values in §IV-C as nominal reference parameters borrowed from an ALKS performance model (no claim about ALKS or compliance), and state the regulation's scope | SC-55 | minor (R2 W11); minor (R3 W9) | R2 W11: text: §V-C "The as-scored conclusion at τ = 0.75 s therefore rests on the performance-model values of the 01 series" · R3 W9: absence: §III-A and §IV-C — expected the road type and operating domain of the CARLA recordings and a statement that the R157 values are borrowed outside the regulation's motorway scope; checked §I Scope, §III-A, §IV-C, §VI Limits, Supplement S3.1, S3.2 and S8.1 | R2 3 · R3 3 (confident of the regulation's scope; recording road type unknown) | R2; R3 | should_fix | sentence: §IV-C | `claim_scope_unsupported` → section: §IV-C |
| S29 | Present the τ and A sweeps as the result, with 0.75 s and 6 m/s² as one point on them | SC-57 | minor (R2 W11) | text: §V-C "The as-scored conclusion at τ = 0.75 s therefore rests on the performance-model values of the 01 series" | 3 | R2 | should_fix | section: §V-C; Table III | `interpretive_ambiguity_remains` → table: Table III |
| S30 | State the 2.0–5.5 m/s² lead-braking range in §III-A and §I Scope; qualify the 12% and 53% "for leads braking at up to 5.5 m/s²"; add to Limits that the closed-loop and open-loop runs cover different severities | SC-60 | minor (R3 W3) | text: Supplement S2 "No recording brakes above 5.5 m/s²."; Supplement S3.2 "the regulation's following test uses at least 6 m/s²" | 3 (the lead–ego deceleration link is R3's reading) | R3 | should_fix | sentence: §I Scope; §III-A; §V-C; §VI | `claim_scope_unsupported` → claim: Abstract "it falls to 12%" |
| S31 | Add the fallback share (0.70–0.72) and the contact count to the S3 opening, the Fig. S3 caption and §VI; state that the gap figures are not design guidance | SC-61 | minor (R3 W4) | text: Supplement S3 "at about 0.31–0.35 s of extra starting gap over the legal following distance"; S3.4 "The cost in starting gap therefore leaves out a large cost in comfort and progress." | 4 (interpreting closed-loop safety evidence) | R3 | should_fix | sentence: Supplement S3; Fig. S3 caption; §VI | `claim_scope_unsupported` → section: Supplement S3 |
| S32 | Name occupants' comfort and following traffic as unmeasured costs; as a proxy, report each arm's selected-row first target acceleration or peak jerk at matched caution | SC-62 | minor (R3 W6); DA M3: major | R3 W6: text: §VI "The prior has costs: its zero-margin caution is 1.72% against 1.10%" and "its cost where braking never comes is untested here" · DA M3: text: Section VI "The 3 s shares, including the 83% and the 0.665, count caution over truly safe selections only"; Section V-C "With the ego moving, however, it recovers less than the class average" | R3 4 (how safety cases allocate residual risk) · DA 4 (Table S13 and Limits) | R3; DA-corroborated (M3) | should_fix | re_analysis: stored row labels (Table S7); §VI | `evidence_gap_remains` → claim: §VI "The prior has costs" |
| S33 | List in §I Scope the road users and scenarios left out (pedestrians, cyclists, crossing and cut-in actors, vehicles behind the ego, real sensor data) | SC-63 | minor (R3 W6) | text: §VI "The prior has costs: its zero-margin caution is 1.72% against 1.10%" and "its cost where braking never comes is untested here" | 4 | R3 | should_fix | sentence: §I Scope | `claim_scope_unsupported` → section: §I Scope |
| S34 | Add a Notation-table column mapping each term to its nearest established counterpart (criticality metric, proper response, over-conservatism, value of perfect information) | SC-64 | minor (R3 W7) | text: Abstract "With that stop, unless those plans count as unsafe, too little room remains, phase by phase, for the braking prior's share to be measured." | 4 | R3 | should_fix | section: Notation table | `interpretive_ambiguity_remains` → table: Notation table |
| S35 | Give the ratio check a worked, unvalidated threshold; say how to find binding constraints in other planner types; require the full scenario mix; note that graded oracles need ground truth | SC-65 | minor (R3 W8) | text: §VI "where it is nearly constant, the covariance can change few decisions once the margin's scale is tuned, whatever its calibration" | 3 (adjacent expertise in planner integration) | R3 | should_fix | section: §VI "What carries over" | `interpretive_ambiguity_remains` → section: §VI "What carries over" |
| S36 | Give the road type and setting of the CARLA recordings in §III-A | SC-66 | minor (R3 W9) | absence: §III-A and §IV-C — expected the road type and operating domain of the CARLA recordings and a statement that the R157 values are borrowed outside the regulation's motorway scope; checked §I Scope, §III-A, §IV-C, §VI Limits, Supplement S3.1, S3.2 and S8.1 | 3 | R3 | should_fix | sentence: §III-A | `claim_scope_unsupported` → section: §III-A |
| S37 | Add a positive control in the covariance's own form (a per-decision covariance, or a multiple of the class average, fitted to the realised 3 s error and projected as N) and report RR(N) and RR(NA) against it; otherwise rephrase the CK3-versus-covariance contrast as mean-path correction versus variance margins | — (DA M4) | major (DA M4) | table: Table S12, rows "Noisy, σ = 1" and "Noisy, σ = 2", column "3 s, all: RR" (0.922 and 0.820) | 3 (inference from the graded oracles) | DA (DA-only; outside the four-seat count) | should_fix | re_analysis: stored realised errors | `claim_scope_unsupported` → claim: the "at most about 0.4%" versus 83% contrast |
| S38 | Run CK3 (and NA) in the existing simplified closed-loop simulator on the same episodes, or reweight toward CK3-visited states; until then, call the 83% an open-loop, off-policy share in the Abstract and §VII | — (DA M6) | major (DA M6) | text: Section III-B "for the other margin sources they are off-policy"; Supplement S3.1 "whether the braking prior, which is not a rescaled class average, changes the gap needed is not tested" | 3 (standard open-loop limitation of unknown size) | DA (DA-only; EIC W2 offers the same closed-loop run as an optional fix) | should_fix | new_data: closed-loop simulator episodes (Supplement S3) | `claim_scope_unsupported` → claim: §VII decision-value location |

> Transported metadata reaches the package on every row (#574 A2/A3). Each row carries the driving finding's severity, its typed evidence anchor and its per-finding confidence, plus each corroborating seat's values. No `[SEVERITY-SOURCE: letter-fallback]` or `[CONFIDENCE-SOURCE: report-level]` fallback was needed. One row has no per-finding confidence: R1's disputing strength entry in S24, marked "none".

### Source-Traceability Checklist

> Immutable source order. This is not a work order. The author records `will_address`, `wont_address` or `not_on_point` later, in the separate author-adjudication sidecar.

- [ ] R1 — obligation `must_fix`: qualify or retitle the headline and state that the null is expected
- [ ] R2 — obligation `must_fix`: recast the contribution list
- [ ] S1 — obligation `consider`: evaluate a source whose covariance varies per decision
- [ ] R3 — obligation `must_fix`: add a §VI implications paragraph and a conditional Conclusion
- [ ] R4 — obligation `must_fix`: move appendix-grade material and state each headline number once
- [ ] R5 — obligation `must_fix`: rewrite the Abstract to be self-contained
- [ ] S2 — obligation `should_fix`: extend the novelty search and ITS positioning
- [ ] S3 — obligation `should_fix`: handle the related manuscript [9] and the preprint citations
- [ ] S4 — obligation `should_fix`: define terms before use and add a plain summary
- [ ] S5 — obligation `should_fix`: make arm names and the R/RR symbols consistent
- [ ] S6 — obligation `should_fix`: bring a compact Table S12 into §IV-B
- [ ] S7 — obligation `should_fix`: remove project-history and review narration
- [ ] R6 — obligation `must_fix`: complete the author block and the AI-use disclosure
- [ ] R7 — obligation `must_fix`: deposit plans, code and per-decision arrays with a DOI
- [ ] S8 — obligation `should_fix`: use one self-contained caption per figure and table
- [ ] S9 — obligation `should_fix`: characterise Fig. 2(b)'s outlying rows
- [ ] S10 — obligation `should_fix`: adopt one number-format convention
- [ ] S11 — obligation `should_fix`: qualify the Abstract's held-out phrase
- [ ] R8 — obligation `must_fix`: replace "at most about 0.4%"
- [ ] S12 — obligation `should_fix`: add ITS index terms
- [ ] R9 — obligation `must_fix`: validate the step-frontier bootstrap and re-apply the NIS-inflated rules
- [ ] R10 — obligation `must_fix`: judge censored plans against the logged truth
- [ ] R11 — obligation `must_fix`: rerun the 3 s shares with signed caution
- [ ] R12 — obligation `must_fix`: run the truncation sensitivity and the per-phase-scale frontier
- [ ] R13 — obligation `must_fix`: print the population-specific shares beside the 83%
- [ ] R14 — obligation `must_fix`: add the regeneration configuration table
- [ ] S13 — obligation `should_fix`: check the replay on the evaluation runs and state the counterfactual assumption
- [ ] S14 — obligation `should_fix`: explain the five short runs and exclude them jointly
- [ ] S15 — obligation `should_fix`: run a sensitivity check on the resolution rule
- [ ] S16 — obligation `should_fix`: use joint or Fieller intervals for near-zero denominators
- [ ] S17 — obligation `should_fix`: mark the commitment analyses as descriptive
- [ ] S18 — obligation `should_fix`: measure the prior's cost without braking, or qualify the 83%
- [ ] S19 — obligation `should_fix`: repeat the graded oracles over many draws
- [ ] R15 — obligation `must_fix`: replace the "RSS-style" label
- [ ] R16 — obligation `must_fix`: state how 3 m/s² was chosen and its relation to the braking range
- [ ] S20 — obligation `consider`: sweep the braking prior's deceleration
- [ ] R17 — obligation `must_fix`: state the contact criterion and score O at the 2 m gap
- [ ] S21 — obligation `consider`: compute the steady-state ratio and survey the prevalence of fixed-noise trackers
- [ ] S22 — obligation `should_fix`: state that process noise is omitted from the margin
- [ ] S23 — obligation `should_fix`: scope NA to the covariance channel
- [ ] S24 — obligation `should_fix`: present §V-D as a consistency check
- [ ] S25 — obligation `should_fix`: justify the 2 Hz rate and list it as a limit
- [ ] S26 — obligation `should_fix`: phrase the Conclusion as a ranking among the tested sources
- [ ] S27 — obligation `consider`: add a time-gap arm
- [ ] S28 — obligation `should_fix`: describe the R157 values as nominal reference parameters
- [ ] R18 — obligation `must_fix`: reword "rests on the performance-model values"
- [ ] S29 — obligation `should_fix`: present the τ and A sweeps as the result
- [ ] R19 — obligation `must_fix`: fence the null against removing deployed covariance margins
- [ ] R20 — obligation `must_fix`: run the cross-family ratio check
- [ ] S30 — obligation `should_fix`: state the lead-braking range and qualify the 12% and 53%
- [ ] S31 — obligation `should_fix`: report the closed-loop fallback share where readers meet it
- [ ] S32 — obligation `should_fix`: name the comfort and following-traffic costs and add a comfort proxy
- [ ] S33 — obligation `should_fix`: list the left-out road users and scenarios in §I Scope
- [ ] S34 — obligation `should_fix`: map the terms to established vocabulary
- [ ] S35 — obligation `should_fix`: give the ratio check a rule and a recipe
- [ ] S36 — obligation `should_fix`: state the road type and setting of the recordings
- [ ] S37 — obligation `should_fix`: add a covariance-form positive control or rephrase the contrast
- [ ] S38 — obligation `should_fix`: run CK3 closed-loop or label the 83% as an off-policy share

### Journal-Supplied Deadline (Optional Transport)

- **Exact deadline from source letter**: `NOT PROVIDED`. No deadline, duration or work estimate is inferred.

### Response Letter Template

Please respond to every roadmap item (R1–R20 and S1–S38) in the format of `templates/revision_response_template.md`. The response must include:
1. A response and a description of the change for each Required Revision.
2. A response for each Suggested Revision, stating whether it was adopted and, if not, why.
3. Change markup (colour or tracked changes) in the revised manuscript.
4. A cross-reference table of new page and paragraph numbers.

It should also answer the Journal-Fit seat's four questions (repository access during review; whether the reviews mentioned in §IV-C and §IV-D belong to a previous submission; which commitment model is representative; any overlap with [9] in runs, code or text). It should acknowledge each DA MAJOR row (M1–M6), including those carried as should_fix items.

**Closing.** We encourage you to consider the reviewers' comments carefully and to submit a substantially revised manuscript. The revision would go through another round of review (ARS re-review mode), where the items above are verified.

---

## Part 3: Reviewer Report Summary (Appendix)

### Journal-Fit Review Report Summary
- Recommendation: none issued; the Schema 13.2 card carries scores only (D5 warn, D6 warn). Stated preliminary signal: major revision. | Confidence: per-finding 3–5; NOT_CALIBRATED
- Key Point: the paper is in scope, careful and candid. However, the headline leads with an expected null, the practical take-away under the realistic commitment is unstated, and the abstract, the length and the placeholders put desk-rejection risk at "moderate as the text stands".

### Reviewer 1 (Methodology) Summary
- Recommendation: none issued (D1 block, repairable; D3 warn) | Confidence: per-finding 3–4
- Key Point: the design is unusually strong, and every headline number matches its table (five GRIM receipts, all consistent). However, the step-frontier intervals are unvalidated, and three estimand choices (censored-plan imputation, outcome-conditioned caution, pooled weighting) move the secondary headlines. All of these are repairable from the stored arrays.

### Reviewer 2 (Domain) Summary
- Recommendation: none issued (D2 warn) | Confidence: per-finding 3–4
- Key Point: the paper is domain-accurate on the central claim. However, the braking prior is mislabelled "RSS-style" at a deceleration that matches the scenarios, and the room is defined for contact only, under a regulatory model whose 2 m gap is set aside.

### Reviewer 3 (Perspective) Summary
- Recommendation: none issued (D4 warn) | Confidence: per-finding 3–4
- Key Point: the paper is scoped with care. However, the null is not fenced against removing covariance margins in deployed stacks, R157 model 2 is adopted only in part, and the costs and terms are not framed for safety-assurance readers.

### Devil's Advocate Summary
- Recommendation: N/A (findings only; D3 block, repairable)
- Key Challenge: the title question is settled by the Riccati steady state before any decision is scored. The room and its location, which the decision-level machinery adds, are not mainly about uncertainty, and the location claim rests on pooling, imputation, conditioned-caution and off-policy premises (M1–M6). There is no unresolved Critical challenge: the CRITICAL table is empty by judgement.

### Reviewer Summary Matrix (Step 1a)

| Dimension | Journal-Fit Reviewer (EIC) | R1 (Methodology) | R2 (Domain) | R3 (Perspective) |
|-----------|----------------------|-------------------|-------------|------------------------|
| Overall Recommendation | None issued (scores only); preliminary signal major revision | None issued | None issued | None issued |
| Contract scores (eligible dimensions) | D5 warn; D6 warn | D1 block (repairable); D3 warn | D2 warn | D4 warn |
| Confidence / scope disclosure | Per-finding 3–5; NOT_CALIBRATED; bootstrap details deferred to R1 (W15, W16) | Per-finding 3–4; could not rerun the bootstrap without per-run arrays | Per-finding 3–4; could not read [8], [9], [13], [16], [17], [19] | Per-finding 3–4; statistics and tracker theory outside competence; could not open 01-series Annex 3 |
| Key Strengths | S1–S8: positive control; candour of Table S4; ground-truth-free ratio screen; regulatory anchoring; Fig. 4(a); clean figures; numbers reconcile; claims scoped | S1–S6: pre-specification and deviation trail; positive control with graded oracles; run-level paired bootstrap; independent re-implementation; mechanistic diagnostics; commitment made explicit | S1–S6: correct estimation theory; accurate margin and oracle framing; consistency measured; transferable ratio diagnostic; current related work; actionable commitment sensitivity | S1–S5: oracle turns a null into evidence; regulatory values cited to clause level; claim fenced against overreach; reporting rule for open-loop evaluators; cheap diagnostic |
| Key Weaknesses | 4 Major, 13 Minor (→ Step 1b) | 5 Major, 7 Minor (→ Step 1b) | 2 Major, 9 Minor (→ Step 1b) | 2 Major, 7 Minor (→ Step 1b) |
| # of Questions | 4 | 0 | 0 | 0 |
| # of Minor Issues | 13 | 7 | 9 | 7 |

### Sub-Claim Inventory (Step 1b)

Notes on reading the table:
- Only `raised`, `corroborated` and `disputed` positions are listed. Every seat not listed for a sub-claim is `not-mentioned`, which counts as silence, not opposition.
- DA rows are recorded as `raised (DA row)`. They are never counted in Step 2.
- Severity and confidence are transported from the parent finding.
- The evidence pointer gives the card finding and its typed anchor locator. The full quoted anchor is transported on the roadmap row.

| sub_claim_id | parent_weakness | reviewer_id | position | evidence_pointer | severity | confidence |
|--------------|-----------------|-------------|----------|------------------|----------|------------|
| SC-1 | EIC W1 headline poses an expected null | EIC | raised | EIC W1 · text: §I para. 4; §II Novelty | major | 4 |
| SC-1 | R2 W3 title asks what theory answers | R2 | disputed (severity) | R2 W3 · text: Title | minor | 4 |
| SC-2 | EIC W1 | EIC | raised | EIC W1 · text: §I para. 4; §II Novelty | major | 4 |
| SC-3 | EIC W1 (stronger option) | EIC | raised | EIC W1 · text: §I para. 4; §II Novelty | major | 4 |
| SC-4 | EIC W2 take-away unstated | EIC | raised | EIC W2 · text: §IV-C; §VII | major | 4 |
| SC-5 | EIC W2 | EIC | raised | EIC W2 · text: §IV-C; §VII | major | 4 |
| SC-6 | EIC W3 length | EIC | raised | EIC W3 · table: Table IV | major | 4 |
| SC-7 | EIC W4 abstract not self-contained | EIC | raised | EIC W4 · text: Abstract (two excerpts) | major | 5 |
| SC-7 | R3 W7 headline results hard to use | R3 | disputed (severity) | R3 W7 · text: Abstract last sentence | minor | 4 |
| SC-8 | EIC W5 ITS positioning thin | EIC | raised | EIC W5 · text: Supplement S6 | minor | 3 |
| SC-8 | R2 W8 threat-assessment strand omitted | R2 | corroborated | R2 W8 · absence: §II Related Work and Novelty paragraph | minor | 3 |
| SC-9 | EIC W6 overlap and preprints | EIC | raised | EIC W6 · text: §I Scope | minor | 4 |
| SC-10 | EIC W6 | EIC | raised | EIC W6 · text: §I Scope | minor | 4 |
| SC-11 | EIC W7 terms before definition | EIC | raised | EIC W7 · text: §I contribution 3; §V-C | minor | 4 |
| SC-11 | R3 W7 | R3 | corroborated | R3 W7 · text: Abstract last sentence | minor | 4 |
| SC-12 | EIC W7 | EIC | raised | EIC W7 · text: §I contribution 3; §V-C | minor | 4 |
| SC-13 | EIC W8 R and RR(N) symbols | EIC | raised | EIC W8 · table: Table III headers vs Notation table | minor | 4 |
| SC-14 | EIC W9 Table S12 only in Supplement | EIC | raised | EIC W9 · table: Table S12 | minor | 4 |
| SC-15 | EIC W10 history and earlier reviews | EIC | raised | EIC W10 · text: §IV-C; §V-C | minor | 4 |
| SC-16 | EIC W11 placeholders | EIC | raised | EIC W11 · text: Author block; Data and Code Availability | minor | 5 |
| SC-17 | EIC W11 | EIC | raised | EIC W11 · text: Author block; Data and Code Availability | minor | 5 |
| SC-17 | R1 W5 configuration and deposits missing | R1 | disputed (severity) | R1 W5 · absence: §III-A and Data and Code Availability | major | 4 |
| SC-18 | EIC W12 AI-use disclosure draft | EIC | raised | EIC W12 · text: Acknowledgment | minor | 5 |
| SC-19 | EIC W13 captions and Fig. 2(b) | EIC | raised | EIC W13 · figure: Fig. 2(b) and its two captions | minor | 4 |
| SC-20 | EIC W13 | EIC | raised | EIC W13 · figure: Fig. 2(b) and its two captions | minor | 4 |
| SC-20 | R2 W3 (stronger fix: the 0.74% tail) | R2 | corroborated | R2 W3 · text: Title | minor | 4 |
| SC-20 | R3 W1 deployment fence | R3 | disputed (severity) | R3 W1 · text: Supplement S9; §VI | major | 4 |
| SC-21 | EIC W14 number formats | EIC | raised | EIC W14 · table: Table II, row RR(N) | minor | 4 |
| SC-22 | EIC W15 held-out framing | EIC | raised | EIC W15 · text: Abstract; §III-A | minor | 3 |
| SC-22 | R1 W10 held-out and descriptive status | R1 | corroborated | R1 W10 · text: Abstract | minor | 4 |
| SC-23 | EIC W16 post hoc interval as a bound | EIC | raised | EIC W16 · text: Abstract; §V-A | minor | 3 |
| SC-23 | R1 W1 bootstrap validity | R1 | disputed (severity) | R1 W1 · text: §V-A para. 2 | major | 4 |
| SC-24 | EIC W17 index terms | EIC | raised | EIC W17 · text: Index Terms | minor | 4 |
| SC-25 | R1 W1 | R1 | raised | R1 W1 · text: §V-A para. 2 | major | 4 |
| SC-26 | R1 W1 | R1 | raised | R1 W1 · text: §V-A para. 2 | major | 4 |
| SC-27 | R1 W1 | R1 | raised | R1 W1 · text: §V-A para. 2 | major | 4 |
| SC-28 | R1 W2 censored-plan imputation | R1 | raised | R1 W2 · text: §V-C para. 2 | major | 3 |
| SC-28 | DA M5 | DA | raised (DA row) | DA M5 · text: Section IV-C; Section V-C | major | 4 |
| SC-29 | R1 W3 outcome-conditioned caution | R1 | raised | R1 W3 · text: §IV-A; §VI Limits | major | 4 |
| SC-29 | DA M3 | DA | raised (DA row) | DA M3 · text: Section VI; Section V-C | major | 4 |
| SC-30 | R1 W4 pooled estimand | R1 | raised | R1 W4 · text: §IV-B para. 2 | major | 4 |
| SC-30 | DA M1 | DA | raised (DA row) | DA M1 · text: Section IV-B; Section VI | major | 4 |
| SC-31 | R1 W4 | R1 | raised | R1 W4 · text: §IV-B para. 2 | major | 4 |
| SC-31 | DA M1 | DA | raised (DA row) | DA M1 · text: Section IV-B; Section VI | major | 4 |
| SC-32 | R1 W4 | R1 | raised | R1 W4 · text: §IV-B para. 2 | major | 4 |
| SC-32 | R2 W10 pooled 83% dominated by standstill | R2 | disputed (severity) | R2 W10 · text: Abstract | minor | 4 |
| SC-33 | R1 W5 | R1 | raised | R1 W5 · absence: §III-A and Data and Code Availability | major | 4 |
| SC-34 | R1 W6 replay validity | R1 | raised | R1 W6 · text: Supplement S1 | minor | 3 |
| SC-35 | R1 W6 | R1 | raised | R1 W6 · text: Supplement S1 | minor | 3 |
| SC-36 | R1 W7 five short runs | R1 | raised | R1 W7 · text: §III-A para. 1 | minor | 3 |
| SC-37 | R1 W8 resolution rule | R1 | raised | R1 W8 · text: §IV-C para. 3 | minor | 3 |
| SC-38 | R1 W9 near-zero denominators | R1 | raised | R1 W9 · table: Table S10, count (ii), τ = 0.75 s, lead-braking row | minor | 4 |
| SC-39 | R1 W10 | R1 | raised | R1 W10 · text: Abstract | minor | 4 |
| SC-40 | R1 W11 cost without braking | R1 | raised | R1 W11 · text: §VI | minor | 3 |
| SC-40 | DA M2 | DA | raised (DA row) | DA M2 · text: Section VI | major | 4 |
| SC-41 | R1 W12 single mixing draw | R1 | raised | R1 W12 · text: Supplement S8.1 | minor | 3 |
| SC-42 | R2 W1 RSS-style label, 3 m/s² | R2 | raised | R2 W1 · text: §VI | major | 4 |
| SC-42 | R3 W5 RSS-style overstates | R3 | disputed (severity) | R3 W5 · text: §VI | minor | 4 |
| SC-43 | R2 W1 | R2 | raised | R2 W1 · text: §VI | major | 4 |
| SC-44 | R2 W1 (stronger fix) | R2 | raised | R2 W1 · text: §VI | major | 4 |
| SC-45 | R2 W2 contact-only room | R2 | raised | R2 W2 · text: Supplement S5, footnote to Table S6 | major | 3 |
| SC-45 | R3 W2 model 2 adopted in part | R3 | corroborated | R3 W2 · text: §V-C; Table S6 caption | major | 3 |
| SC-46 | R2 W2 (stronger fix) | R2 | raised | R2 W2 · text: Supplement S5, footnote to Table S6 | major | 3 |
| SC-46 | R3 W2 (fix 2) | R3 | corroborated | R3 W2 · text: §V-C; Table S6 caption | major | 3 |
| SC-47 | R2 W3 (stronger fix) | R2 | raised | R2 W3 · text: Title | minor | 4 |
| SC-48 | R2 W3 | R2 | raised | R2 W3 · text: Title | minor | 4 |
| SC-49 | R2 W4 no process noise | R2 | raised | R2 W4 · text: Supplement S9 | minor | 4 |
| SC-50 | R2 W5 NA covariance channel only | R2 | raised | R2 W5 · text: §V-B heading | minor | 4 |
| SC-51 | R2 W6 ranking check restates ratio | R2 | raised | R2 W6 · text: §V-D | minor | 4 |
| SC-51 | R1 Review Body summary and S5 | R1 | disputed (existence) | R1 S5 · figure: Fig. 2(b), with §V-D | none (strength entry) | none (no per-finding Confidence) |
| SC-52 | R2 W7 2 Hz update rate | R2 | raised | R2 W7 · text: §III-A | minor | 3 |
| SC-53 | R2 W9 no time-gap margin | R2 | raised | R2 W9 · table: Table I | minor | 3 |
| SC-54 | R2 W9 (stronger fix) | R2 | raised | R2 W9 · table: Table I | minor | 3 |
| SC-55 | R2 W11 regulatory authority | R2 | raised | R2 W11 · text: §V-C | minor | 3 |
| SC-55 | R3 W9 operating domain | R3 | corroborated | R3 W9 · absence: §III-A and §IV-C | minor | 3 |
| SC-56 | R2 W11 | R2 | raised | R2 W11 · text: §V-C | minor | 3 |
| SC-56 | R3 W2 (fix 3) | R3 | disputed (severity) | R3 W2 · text: §V-C; Table S6 caption | major | 3 |
| SC-57 | R2 W11 | R2 | raised | R2 W11 · text: §V-C | minor | 3 |
| SC-58 | R3 W1 | R3 | raised | R3 W1 · text: Supplement S9; §VI | major | 4 |
| SC-59 | R3 W1 | R3 | raised | R3 W1 · text: Supplement S9; §VI | major | 4 |
| SC-60 | R3 W3 milder lead braking | R3 | raised | R3 W3 · text: Supplement S2; Supplement S3.2 | minor | 3 |
| SC-61 | R3 W4 closed-loop fallback share | R3 | raised | R3 W4 · text: Supplement S3; S3.4 | minor | 4 |
| SC-62 | R3 W6 who bears the costs | R3 | raised | R3 W6 · text: §VI | minor | 4 |
| SC-62 | DA M3 | DA | raised (DA row) | DA M3 · text: Section VI; Section V-C | major | 4 |
| SC-63 | R3 W6 | R3 | raised | R3 W6 · text: §VI | minor | 4 |
| SC-64 | R3 W7 | R3 | raised | R3 W7 · text: Abstract last sentence | minor | 4 |
| SC-65 | R3 W8 ratio check lacks a rule | R3 | raised | R3 W8 · text: §VI | minor | 3 |
| SC-66 | R3 W9 | R3 | raised | R3 W9 · absence: §III-A and §IV-C | minor | 3 |

Step 2 counts per sub-claim (denominator: the four non-DA seats):
- **SPLIT** (conflict ≥ 1): SC-1, SC-7, SC-17, SC-20, SC-23, SC-32, SC-42, SC-51 and SC-56 each have agree 1 and conflict 1, except SC-20, which has agree 2 and conflict 1.
- **CORROBORATED** (agree 2, conflict 0): SC-8, SC-11, SC-22, SC-45, SC-46 and SC-55.
- **SINGLE-REVIEWER** (agree 1, conflict 0): every other sub-claim. SC-28, SC-29, SC-30, SC-31, SC-40 and SC-62 are DA-corroborated.
- **CONSENSUS-4 or CONSENSUS-3**: none.
