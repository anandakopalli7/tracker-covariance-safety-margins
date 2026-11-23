# Field Analysis Report (ARS academic-paper-reviewer v1.11.1, mode `full`, Phase 0)

Time stamp: 2026-11-18 13:29 −05:00 (read from the local clock)
Skill: `academic-research-skills:academic-paper-reviewer` (plugin 3.24.3), agent `field_analyst_agent`
Input: `review_v10_input\` (MANUSCRIPT_v10.md, SUPPLEMENT_v10.md, SUPPLEMENT_FULL_CAPTIONS_v10.md, figures\ ×7; INPUT_MANIFEST.txt)
Status: **waiting for confirmation of the cards (skill Checkpoint Rule 1, #1030). No reviewer seat has run.**

## Paper Basic Information
- **Title**: Does a Kalman Tracker's Covariance Improve Car-Following Decisions? A Decision-Level Evaluation in CARLA Lead-Braking Scenarios
- **Abstract length**: 249 words (whitespace count of the Markdown source; the stated limit is 250)
- **Full text length**: about 10,900 words for title through Section VII including tables and front/back matter; Supplement about 16,800 words
- **Number of references**: 43 (all 43 cited in the main text)
- **Display items**: Figs. 1–4, Tables I–IV and a notation table (main); Figs. S1–S3, Tables S1–S15 (supplement)

## Field Analysis

| Dimension | Analysis Result |
|-----------|----------------|
| Primary Discipline | Intelligent transportation systems: automated driving, the perception–tracking–planning interface (motion planning under uncertainty) |
| Secondary Disciplines | State estimation / multi-object tracking (Kalman filtering); statistical evaluation methodology (run-level bootstrap, value-of-information style oracle comparison); automated-vehicle safety regulation (UN R157 performance models, RSS) |
| Research Paradigm | Quantitative |
| Methodology Type | Experimental (simulation-based, open-loop counterfactual replay of recorded runs) with comparative analysis of margin sources; a supporting closed-loop check on a simplified simulator |
| Target Journal Tier | IEEE Open Journal of Intelligent Transportation Systems (OJ-ITS); track: none given; article type: regular paper (as stated by the requesting session for the researcher). No criteria-binding manifest was supplied, so `criteria_binding_unavailable` for formal venue criteria; the stated constraints (abstract ≤ 250 words; no page limit, 10 pages recommended) are used as given |
| Paper Maturity | Pre-submission: complete structure, full reference list and supplement; open items are the author block, the repository/DOI and the AI-use disclosure, all marked as placeholders for the author |

## Target Journal
IEEE Open Journal of Intelligent Transportation Systems (OJ-ITS); track: none given; article type: regular paper. Abstract limit 250 words; no page limit, 10 pages recommended. (Supplied by the requesting session on the researcher's behalf; no pointer-only Target Criteria Brief was supplied, so `criteria_binding_unavailable` applies to venue criteria beyond these stated constraints.)

## Coverage

| Part | Status |
|------|--------|
| Title, abstract, index terms | read |
| Sections I–VII (body) | read |
| Notation table (after §IV-C) | read |
| Tables I, II, III, IV (Markdown tables) | read |
| Fig. 1 (fig1_method_v05.png) | read (image viewed) |
| Fig. 2 (fig2_frontiers_v04.png) | read (image viewed) |
| Fig. 3 (fig3_rr_v02.png) | read (image viewed) |
| Fig. 4 (fig4_commitment_v04.png) | read (image viewed) |
| Data and Code Availability, Funding, Competing Interests, Acknowledgment / AI disclosure | read (the repository line and parts of the AI disclosure are author placeholders) |
| Author block | read (placeholder only: "[AUTHOR BLOCK: filled by the author]") |
| References [1]–[43] | read (as printed; not checked against external records) |
| Supplement S1–S9 with Tables S1–S15 | read |
| Fig. S1 (figS1_nis_v04.png), Fig. S2 (figS2_hull_v04.png), Fig. S3 (fig5_closedloop_v04.png) | read (images viewed) |
| Supplement full-caption file (Figs. 1–4, Tables I–IV) | read |
| Appendices in the main paper | none |
| Author HTML comments in the source drafts | none supplied (removed before supply, per INPUT_MANIFEST; not part of the submitted text) |
| Linked code and data repository | none (placeholder in the manuscript; not supplied) |

Every supplied part was read. No part is `not read` or `not readable`, so no readable copy is requested.

**Embedded text aimed at reviewers (§2A check):** none found. The manuscript mentions earlier reviews ("Two further checks follow review requests", §IV-C; "[AUTHOR TO APPROVE … from the template of the review (B3)]", Acknowledgment) as history, not as directions to this panel. The requesting session's note that three internal reviews recounted every number is context only; the panel neither relies on it nor assumes errors it cannot point to.

## Reviewer Configuration Cards

### Reviewer Configuration Card #1

**Role**: EIC
**Display role**: Journal-Fit Reviewer (serialized source ID: EIC)
**Identity Description**: Senior Associate Editor of *IEEE Open Journal of Intelligent Transportation Systems* (the requester-stated target), handling automated-driving perception and planning submissions; background in simulation-based testing and evaluation of driver-assistance and automated-driving functions.
**Review Focus**:
  1. Check whether the title, abstract and introduction state the question and the take-away in terms a general ITS reader can act on, and whether paper-specific terms (room, caution, commitment, count (ii), phase-weighted, decision-equivalents) are defined before use [Title; Abstract; §I].
  2. Check the abstract against the 250-word limit and the IEEE abstract conventions (self-contained, no undefined symbols) [Abstract].
  3. Check length and structure against the recommended 10 pages: main-text length, number and width of tables, and which parts of §IV–§V and Tables II–IV could move to the Supplement [§IV–§V; Tables II–IV; Notation table].
  4. Check the novelty and significance case: the novelty paragraph and the stated expectation that a fixed-noise Kalman filter's covariance is nearly constant [§II "Novelty, with its limits"; §I para. 4; §VI para. 1].
  5. Check submission-readiness items: placeholders, the AI-use disclosure, and reliance on unpublished or under-review sources [Author block; Data and Code Availability; Acknowledgment; refs [8], [9], [14], [17], [19]].
**Will particularly care about**: Whether a null result that the paper itself calls expected, plus a commitment-dependence finding, is framed as a contribution of journal significance and readable for the OJ-ITS audience.
**Possible blind spots**: Bootstrap and frontier-statistic details; Kalman-filter theory.

### Reviewer Configuration Card #2

**Role**: Peer Reviewer 1
**Display role**: Peer Reviewer 1 — Methodology
**Identity Description**: Statistician specializing in resampling inference for clustered data (cluster/run-level bootstrap, intervals for non-smooth functionals) and in pre-specified evaluation designs, with experience in off-policy (counterfactual) evaluation of decision systems.
**Review Focus**:
  1. Check the run-level bootstrap for RR and R: 35 unequal clusters (five short runs), no stratification, percentile intervals with coverage stated as unverified, the RR(N) point outside its own percentile interval, and the basic interval used for "at most about 0.4%" [§IV-B para. 4; §V-A para. 2; Table II; Table S5 footnote].
  2. Check the definitions and behaviour of the step and convex-hull frontiers, R, RR, den₀, RR₀, RR_E and the 10-decision-equivalent resolution rule, including ratio behaviour when the denominator is small [§IV-B; §IV-C; Notation table; Table IV; S8.1].
  3. Check the off-policy replay (evaluation runs recorded by a planner using the tracker's covariance, scored for other margin sources) and the handling of plans the 3 s truth window cannot judge (counts (i), (ii)) [§III-B last para.; §IV-C para. 2; §V-C].
  4. Check the analysis-plan and deviation trail: what was fixed before which values were computed, the earlier exploratory analysis on the same runs, the amendments, and the multiplicity statement [§III-A para. 1; §IV-D; S4; Table S4].
  5. Check the graded-oracle validation of the measure and what it implies for reading shares outside the pooled population [§IV-B para. 3; Table S12; §V-B para. 2; §V-C].
**Will particularly care about**: Whether the intervals and fixed decision rules support each numeric claim printed in the abstract.
**Possible blind spots**: Plausibility of the planner and scenario for ITS practice; journal fit.

### Reviewer Configuration Card #3

**Role**: Peer Reviewer 2
**Display role**: Peer Reviewer 2 — Domain
**Identity Description**: Researcher in motion planning under uncertainty for automated vehicles, specializing in chance-constrained and risk-aware speed planning and in the tracking–planning interface (Kalman and multiple-model tracking for planning).
**Review Focus**:
  1. Check the planner and margin construction: 17 candidate rows and their cost order, the feasibility rule g·s ≤ d², constant-velocity prediction, the projection z = (n, tₑn) and the weight of the velocity block at 3 s [§III-B; S1; Table S7].
  2. Check whether the arms are fair comparators: F0 built from 120 tuning runs of six scenario families, the inflate-only NA, E as "reference, not a bound", CK3 shifting the path rather than s, AM and Q [§III-C; Table I].
  3. Check related-work coverage and positioning against planner-centric perception metrics, uncertainty-aware car following/ACC and adaptive or IMM tracking, and the Riccati steady-state argument [§II; §VI para. 1; refs [10]–[36]].
  4. Check representativeness of the test bed: simulated sensor data, NIS levels, the share of decisions at ego ≤ 0.5 m/s and after the lead stops, desired speeds 5–15 m/s [§III-A; Fig. S1; §VI "Limits"].
  5. Check the deviation-versus-error check (Spearman ρ, ρ*, RMS z) as evidence about the covariance's per-decision information [§V-D; S9; Tables S14–S15].
**Will particularly care about**: Whether the findings go beyond what tracking theory predicts for a fixed-noise filter, and whether the closest prior work [13], [15]–[17] is represented fairly.
**Possible blind spots**: Bootstrap inference details; regulatory and safety-case implications.

### Reviewer Configuration Card #4

**Role**: Peer Reviewer 3
**Display role**: Peer Reviewer 3 — Cross-disciplinary / Practical
**Identity Description**: Automotive safety-assurance engineer and researcher in scenario-based safety validation of automated driving systems (SOTIF-style safety argumentation, UN R157 ALKS performance models, RSS), experienced in turning simulation evidence into safety cases.
**Review Focus**:
  1. Check how UN R157 (original and 01 series) and RSS values are used (0.75 s, 6 m/s², 12.65 m/s³, 7.6 m/s², 2 m standstill gap) and whether they match the cited tables [§IV-C para. 1; S8.1; S3.1; refs [37]–[40]].
  2. Check whether the practical take-aways (state the commitment assumption; the two checks that carry over) are actionable for teams that build or validate automated-driving stacks [§VI "What the commitment sensitivity means…"; §VI "What carries over"].
  3. Check the costs reported beside wrong-go: caution and progress, comfort, the untested case where braking never comes, and the closed-loop fallback share [§VI "The prior has costs"; S3.4].
  4. Stakeholder scope: check whom the conclusions are framed to serve (tracker developers, planner designers, evaluators, regulators), who bears the costs of the trade-offs reported (ego occupants' progress and comfort, following traffic), and which road users and scenarios the scope leaves out [§I "Scope"; §VI "Limits"; §III-C six scenario families].
  5. Check the role given to the supporting closed-loop check and whether its limits are stated where readers meet it [S3; Fig. S3; §III-A para. 3; §VI].
**Will particularly care about**: Whether a reader could misapply the result (for example, removing covariance margins from a deployed stack) and whether the scope statements prevent that.
**Possible blind spots**: Statistical detail; tracker theory.

The fifth execution seat is the fixed Devil's Advocate; it has no configuration card.

## Stakeholder Coverage

Seat: Card #4 (Peer Reviewer 3 — Cross-disciplinary / Practical), Review Focus item 4
Check: whom the conclusions are framed to serve, who bears the costs of the reported trade-offs, and which road users and scenarios the scope leaves out [§I "Scope"; §VI "Limits"; §III-C]
Competence basis: safety-assurance and scenario-based validation background, which deals with operational design domains, affected road users and residual-risk allocation

## Review Strategy Recommendations
- The paper is heavily qualified and numerically dense; the main risks are likely significance, fit and readability for a general ITS audience rather than arithmetic. Reviewers should not re-derive numbers; they should check that each claim is supported by the cited table and interval, and flag only errors they can point to.
- Expect tension between the Methodology seat (which may ask for more hedging) and the Journal-Fit seat (which may ask for fewer qualifiers and a shorter paper); the synthesizer should weigh both.
- The paper is cross-disciplinary (tracking, planning, statistics, regulation): R2 covers planning and tracking (§II, §III, §V-D), R1 the statistics (§IV, §V, S4, S8), R3 the regulatory and practical reading (§IV-C, §VI, S3, S8.1).
- Reference [9] is the author's own manuscript under review; the overlap statement [§I "Scope"] should be checked for adequacy, not assumed.
