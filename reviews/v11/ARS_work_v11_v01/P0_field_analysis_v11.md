# Field Analysis Report (Phase 0) — draft v11

Skill: academic-research-skills:academic-paper-reviewer v1.11.1 (plugin 3.24.3), mode `full`. Written 18 Nov 2026 by the review session on Claude Opus 5.5. Read-only review; nothing in the package was changed.

## Paper Basic Information
- **Title**: Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution: A Fixed-Noise Kalman Tracker in CARLA Lead Braking
- **Abstract length**: 247 words (counted; limit 250)
- **Full text length**: about 10,800 words in the manuscript file (package manifest); about 7,000–7,600 words of body text without tables, captions and references; supplement about 27,500 words
- **Number of references**: 55

## Field Analysis

| Dimension | Analysis Result |
|-----------|----------------|
| Primary Discipline | Intelligent transportation systems: automated-vehicle motion planning and safety evaluation |
| Secondary Disciplines | Target tracking and estimation (Kalman filtering); resampling statistics; safety assurance and regulation of automated driving |
| Research Paradigm | Quantitative |
| Methodology Type | Simulation-based experimental evaluation (open-loop, off-policy replay of recorded CARLA runs) with run-level bootstrap inference |
| Target Journal Tier | IEEE Open Journal of Intelligent Transportation Systems; regular paper (as stated by the author in the package manifest, line 3, and the task brief). No #683 ReviewTargetContext or criteria manifest was supplied, so no criterion ids are bound: `criteria_binding_unavailable` for formal criteria; fit is judged against the journal's public scope as the Journal-Fit Reviewer reads it |
| Paper Maturity | Pre-submission (revised draft v11 after one round of internal review): complete structure, IEEE reference style, two author-only placeholders (author block, line 5; repository/DOI, Data and Code Availability) |

## Target Journal
IEEE Open Journal of Intelligent Transportation Systems; track: regular paper; article type: research article (abstract limit 250 words; no page limit, 10 pages recommended — from the task brief and package manifest).

## Coverage

| Part | Status |
|------|--------|
| Manuscript body, Sections I–VII, Abstract, Index Terms | read |
| Data and Code Availability, Funding, Competing Interests, Acknowledgment (AI disclosure) | read |
| References [1]–[55] | read |
| Tables I–V and the Notation table (main paper) | read |
| Figs. 1–4 (PNG and vector PDF) | read (each image viewed; PDF and PNG versions match) |
| Supplement S1–S10 and Tables S1–S29 (incl. S12b, S20a–S20d, S24b) | read |
| Figs. S1–S4 (figS1_nis_v04.png, figS2_hull_v04.png, fig5_closedloop_v04.png = Fig. S3, fig3_rr_v02.png = Fig. S4) | read |
| Embedded images in the markdown files | none |
| Appendices other than the Supplement | none |
| Raw data, code, analysis plans, amendments, lock manifests | not supplied (cited in Data and Code Availability and Supplement S4; deposit not yet created). Not needed for a manuscript review; the panel judges the text and tables only |

**Disclosure about blindness.** Before Phase 0 the dispatching session read two hand-over notes in the shared notes folder. They summarise the v10 review's decision (Major Revision), name its two blocking themes (bootstrap validity; the "anticipating braking" location claim) and list the v11 analyses. The first review itself and the response to it were not opened. The panel's Step 1 is therefore blind to the v10 review text and to the response, not to that summary.

## Reviewer Configuration Cards

### Reviewer Configuration Card #1

**Role**: EIC
**Display role**: Journal-Fit Reviewer
**Identity Description**: Associate Editor of the IEEE Open Journal of Intelligent Transportation Systems, specialising in safety evaluation of automated driving and in the interface between perception and motion planning; handles simulation-based studies of advanced driver assistance and car following.
**Review Focus**:
  1. Check whether the four contributions are framed as a contribution of interest to ITS readers, given that the paper itself says the tracker null is expected [§I contributions list; §II "Novelty, with its limits"].
  2. Check whether every number and claim in the abstract traces to a table or section, and whether the abstract stays within 250 words while stating the limits [Abstract; Tables II–IV].
  3. Check the length against the 10-page recommendation and which material could move to the supplement [whole manuscript; 5 tables, 4 figures] [unverified page estimate].
  4. Check whether the practical reading for ITS practitioners (commitment, population mix, ratio check) is stated and fenced [§VI; §VII].
**Will particularly care about**: Whether an expected null plus conditional secondary findings is enough for a regular paper, and whether the title and abstract sell the evaluation design rather than the null.
**Possible blind spots**: Bootstrap theory; tracker internals.

### Reviewer Configuration Card #2

**Role**: Peer Reviewer 1
**Display role**: Peer Reviewer 1
**Identity Description**: Statistician specialising in resampling inference for clustered and non-smooth statistics (cluster bootstrap, double bootstrap, subsampling) and in the design of simulation-based evaluation studies.
**Review Focus**:
  1. Check the run-level bootstrap, the double-bootstrap coverage estimate and the calibrated interval for the non-smooth step-frontier share RR(N) [§IV-B "Intervals"; §V-A; Tables S16–S17].
  2. Check the equal-caution frontier construction: caution averaged over truly safe selections, the signed alternative, 201 levels, step versus hull, and F0's zero-margin point prepended to other sources [§IV-A–B; Table S5 footnote; Table S21].
  3. Check how confirmatory and added analyses are separated, and the number of added descriptive analyses relative to the claims drawn from them [§IV-D; Table S4; Supplement S10].
  4. Check the reaction-and-stop scoring, the extension of plans past the 3 s window, and the evaluability rule for den₀ [§IV-C; §V-D; Tables III–IV, S18–S20d].
  5. Check the off-policy status of the evaluation runs, recorded with a planner whose margin used the tracker covariance [§III-B].
**Will particularly care about**: Whether the "null" is stated as a bounded (equivalence-type) claim, and whether the bound used was fixed before the values were read.
**Possible blind spots**: Domain significance; regulatory context.

### Reviewer Configuration Card #3

**Role**: Peer Reviewer 2
**Display role**: Peer Reviewer 2
**Identity Description**: Researcher in multi-object tracking and uncertainty-aware motion planning for automated vehicles (Kalman and IMM filtering, chance-constrained planning, CARLA-based perception-in-the-loop evaluation).
**Review Focus**:
  1. Check the steady-state argument for a fixed-noise Kalman filter and its link to the near-constant margin ratio of 1.10, including update rate, step and state age [§II "Adaptive covariances"; §V-A; §VI first paragraph].
  2. Check the margin projection s = zᵀPz with z = (n, t_e n), propagation without process noise, and the separate allowance Q [§III-B; Table I; Supplement S1].
  3. Check literature coverage and fairness of characterisation of the closest works [§II, refs [13], [15]–[17], [41]–[52]].
  4. Check the NIS-inflated source and what it can test given mean NIS 0.24 [§III-A; §III-C; §V-B; Fig. S1].
  5. Check the test-bed realism: simulated lidar noise, 2 Hz detector, lead speed controller, straight road, shared configuration with [9] [§III-A; Table S28].
**Will particularly care about**: Whether conclusions are scoped to a single-model fixed-noise Kalman filter in lead braking, and whether the per-phase and after-stop findings are physically explained.
**Possible blind spots**: Bootstrap coverage theory; regulatory reading.

### Reviewer Configuration Card #4

**Role**: Peer Reviewer 3
**Display role**: Peer Reviewer 3
**Identity Description**: Safety-assurance engineer for automated driving (scenario-based verification and validation, UN R157 ALKS type approval, RSS, ISO 21448) with a background in decision analysis and value of information.
**Review Focus**:
  1. Check the use of UN R157 01-series performance-model-2 values as nominal reference parameters and the "no compliance" fences [§II; §IV-C; §V-D "A 2 m standstill gap"; Supplement S8.1, S3].
  2. Check the value-of-information reading of the oracle room and of the per-phase-scale baseline [§IV-B; §V-C; §VI].
  3. Check the practical reading under the two commitments and what the closed-loop check can and cannot support [§VI "Which commitment is representative"; Supplement S3].
  4. Check whom the evaluation assumes benefits, who bears the costs of the tested margins (following traffic, occupants' comfort, progress), and which road users and scenarios are outside it [§I Scope; §VI "What the braking prediction's share shows"; §VI Limits].
  5. Check reproducibility and disclosure: data and code availability, configuration table, AI-use statement [Data and Code Availability; Table S28; Acknowledgment].
**Will particularly care about**: Whether the deployment-facing sentences ("does not justify removing a covariance margin", the conditional practical reading) are supported and fenced.
**Possible blind spots**: Fine statistical detail; tracker internals.

## Stakeholder Coverage

Seat: Card #4 (Peer Reviewer 3), Review Focus item 4
Check: Whom the evaluation assumes benefits, who bears the costs of the tested margins and of the braking prediction, and which road users and scenarios are outside the evaluation [§I Scope; §VI; §VI Limits].
Competence basis: Safety-assurance and type-approval experience (scenario coverage, other road users, following traffic) in the card's identity.

## Review Strategy Recommendations
- The text is dense with numbers and hedges after a revision with two claim audits; each seat should check claims in the Abstract, §I, §VI and §VII against Tables II–V and the supplement tables they cite.
- Expected tension: the Methodology seat may judge the null robust and the secondary findings descriptive; the Devil's Advocate will test whether an expected null plus post hoc conditional findings is a contribution, and whether the per-phase-scale result undercuts the paper's own framing.
- The supplement (about 27,500 words) carries version history (Table S4) and superseded scorings; seats should check whether stale wording survives there.
- Placeholders (author block; repository/DOI) are author submission gates, not scientific findings.
