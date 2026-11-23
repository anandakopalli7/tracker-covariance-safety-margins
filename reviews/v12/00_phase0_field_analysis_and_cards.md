# Field Analysis Report — draft v12 (Phase 0)

Written 2026-11-19 by the reviewing session (Claude Sonnet 5.5, `claude-sonnet-5-5`). The model that wrote v12 is Claude Opus 5.5; v11 was written by Claude Fable 5.2. The reviewing model differs from the writing model of v12.

Status: **cards shown to the user; Phase 1 has not started; waiting for the user's acceptance (Checkpoint Rule 1).**

Blindness record at this point: opened only the three parts of `revision_v12\package_v12\` (manifest, manuscript, supplement, all figure PNGs) and the skill's own files. Not opened: anything else in `revision_v12\`, anything in `review_v11_output\`, any side-session notes folder, `<excluded folder 1>`, `<excluded folder 2>`, `<excluded folder 3>`.

## Paper Basic Information
- **Title**: Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution: A Fixed-Noise Kalman Tracker in CARLA Lead Braking
- **Abstract length**: 248 words (as stated in `PACKAGE_MANIFEST_v12.txt`; limit 250) [unverified here; counted in Phase 1]
- **Full text length**: 12,451 words whole manuscript; 8,926 body without tables, captions and references; 1,670 references (manifest); supplement 34,240 words (manifest)
- **Number of references**: 58 in the main paper, plus 1 supplement-only reference [S1]

## Field Analysis

| Dimension | Analysis Result |
|-----------|----------------|
| Primary Discipline | Intelligent transportation systems: perception-to-planning safety evaluation of automated vehicles (car following) |
| Secondary Disciplines | Multi-object tracking and Kalman estimation; simulation-based and scenario-based safety assessment; statistical evaluation methodology (bootstrap inference, operating-curve comparison) |
| Research Paradigm | Quantitative; simulation experiment with offline (open-loop, log-replay) scoring |
| Methodology Type | Statistical modelling / simulation-based evaluation with an oracle positive control; planned analyses plus exploratory analyses added after the first results (§IV-D) |
| Target Journal Tier | IEEE Open Journal of Intelligent Transportation Systems; regular paper; abstract limit 250 words; no page limit, 10 pages recommended; track: none given. Copied from the requesting session's brief. No pointer-only criteria binding or Target Criteria Brief was supplied, so `criteria_binding_unavailable` applies at criterion level: seats judge fit against the stated parameters and general field norms, cite no criterion ids, and say so. |
| Paper Maturity | Pre-submission. Structure, references and supplement are complete; three author placeholders remain (author block, repository/DOI, author confirmation in the AI-content statement); main text is long against the recommended 10 pages |

## Target Journal
IEEE Open Journal of Intelligent Transportation Systems; regular paper; abstract limit 250 words; no page limit, 10 pages recommended; track: none given.

## Coverage

| Part | Status |
|------|--------|
| Title, author line, abstract, index terms | read |
| §I Introduction (four terms, four contributions, scope) | read |
| §II Related Work (six paragraphs, incl. "Novelty, with its limits") | read |
| §III Test Bed, Planner and Margins (A, B, C), Table I | read |
| §IV Scoring (notation table, A–D) | read |
| §V Results (A–E), Tables II–V | read |
| §VI Discussion, §VII Conclusion | read |
| Data and Code Availability, Funding, Competing Interests, Acknowledgment (AI-content statement) | read |
| References [1]–[58] (the list as text; the cited works themselves are not opened) | read |
| Fig. 1–4 (PNG files) | read (viewed) |
| Fig. 1–4 (PDF vector duplicates) | not read: duplicates of the PNGs per the manifest; no card statement relies on them; no readable copy needed |
| Supplement S1–S3 (planner rows, recordings, stopping point, closed loop), Tables S7, S8, S28 | read |
| Supplement S4 (plan, deviations, verification status), Table S4 | read |
| Supplement S5–S7 (full results, literature search, Tables S1–S6), Figs. S1, S2, S4 | read |
| Supplement S8–S9 (reaction-and-stop of every source; deviation check), Tables S9–S15 | read |
| Supplement S10 (bootstrap validity, plans judged until stop ends, signed caution, after-stop, 2 m gap, deceleration, ratio, replay, verification), Tables S16–S27 | read |
| Supplement S11 (grid placebo, intervals, per-phase scales, lead state, tuning runs, stop reliance, time gap, verification, details moved, grading check), Tables S30–S38 | read |
| Supplement Fig. S3 (closed-loop sizing; file `fig5_closedloop_v04.png`) | read (viewed) |
| Supplement-only reference [S1] | read |
| Deposit (analysis code, per-decision arrays, amendments, plan hashes, DRAFT_HISTORY, raw recordings) | not read: not in the package; the manuscript says the archive is not yet created (repository placeholder) and that raw recordings are available on request. A card may name it only as something to check once supplied. |
| Appendices outside the supplement | none |

No part of the package is unreadable. No card makes a statement about the deposit.

## Reviewer Configuration Cards

### Reviewer Configuration Card #1

**Role**: EIC
**Display role**: Journal-Fit Reviewer
**Identity Description**: Senior associate editor for *IEEE Open Journal of Intelligent Transportation Systems* (regular papers), with editorial experience in automated-vehicle perception, planning and safety evaluation; judges novelty, significance, fit with the journal's readership and the clarity and length of a submission, and does not review methodology in depth.
**Review Focus**:
  1. Check whether the four stated contributions [§I, contributions 1–4] are novel and significant for a regular paper in this journal, and whether the novelty claim and its disclosed search limits [§II "Novelty, with its limits"; Supplement S6] carry the weight put on them.
  2. Check that the abstract, introduction and conclusion state the same claims, within the 250-word abstract limit and without claims that are not carried by a main-text table [Abstract; §I; §VII; Tables II–V].
  3. Check clarity and length against the journal's 10-page recommendation: how much of the 12,451-word main text and the 34,240-word supplement a reader needs to follow the argument, and whether the notation, the amount of qualification and the table density help or hinder [§IV notation table; §V; §VI "Limits"; word counts in the manifest].
  4. Check how the paper handles its disclosed revision history and the AI-assistance statement for a journal submission [§IV-D; Acknowledgment]. Treat the author block, the repository/DOI and the author confirmation placeholders as submission gates for the author, not findings about the science.
**Will particularly care about**: whether a reader of this journal gets one clear, useful take-away, and whether the paper's own scope fences leave a contribution that is more than a method note on a null.
**Possible blind spots**: statistical detail of the interval methods; filter theory; regulation details. To be compensated by Reviewers 1–3.

### Reviewer Configuration Card #2

**Role**: Peer Reviewer 1
**Display role**: Peer Reviewer 1 (Methodology)
**Identity Description**: Applied statistician and simulation-evaluation methodologist, specialising in resampling inference for non-smooth statistics, operating-curve and frontier comparisons, positive controls and the separation of planned from exploratory analyses; experience reviewing log-replay evaluations of automated-driving components.
**Review Focus**:
  1. Check whether the scoring construct (wrong go, caution, step frontier, room R, share recovered RR, perfect oracles O, partial-oracle grading checks) can support the claims made, including the stated populations where the measure "does not grade" [§IV-A–C; Table II; Tables S12, S12b, S21, S38].
  2. Check the inference for the tracker covariance's share: run-level bootstrap with 35 runs, the double-bootstrap calibration, the grid placebo, the gridless frontier, the subsampling intervals and the "2.2 decisions" bound formed after values were read [§IV-B "Intervals"; §V-A; Tables S16, S17, S30, S30b, S30c, S31, S31b, S31c].
  3. Check the design and status of the analyses: tuning/evaluation split, earlier exploratory use of the evaluation runs, plans and amendments, "second programs" that share the scoring library and arrays, held-out per-phase scales with cross-validation [§III-A; §IV-D; §V-C; Supplement S4, S10.9, S11.3, S11.8; Table S32].
  4. Check whether the numbers shown in the abstract, §I and §VII are reproduced by the stated tables and whether rounding and interval choices (nominal versus calibrated) are used consistently [Abstract; §V-A; Table II; Tables S5, S16].
**Will particularly care about**: whether an interval, bound or share is stated for the quantity actually estimated, and whether any added analysis is described as more than exploratory.
**Possible blind spots**: filter and tracking theory; automotive practice. To be compensated by Reviewers 2 and 3.

### Reviewer Configuration Card #3

**Role**: Peer Reviewer 2
**Display role**: Peer Reviewer 2 (Domain)
**Identity Description**: Researcher in multi-object tracking and Kalman-filter-based estimation for road vehicles, familiar with covariance consistency (NIS/NEES), adaptive and multiple-model filtering and with how tracker uncertainty is passed to prediction and planning.
**Review Focus**:
  1. Check the theoretical account of why a fixed-noise extended Kalman filter's covariance is nearly constant, and whether the observed ratio of about 1.10 and the exceptions are consistent with it, including the object-frame noise rotated by estimated heading [§II "Adaptive covariances in tracking"; §III-A; §V-A; §V-E; Tables V, S14, S26, S27].
  2. Check the tracker description and configuration, the innovation-consistency findings (position NIS about 0.24 against 2; velocity block too narrow while the lead brakes) and whether the NIS-inflated source is a fair test of "an adaptive covariance" [§III-A; §III-C; §V-B; Fig. S1; Table S34b; Table S28].
  3. Check literature coverage and positioning: the closest relatives, covariance propagation into planning and prediction, adaptive/IMM tracking, calibration of tracker or predictor uncertainty, and the disclosure that part of the threat-assessment literature was read from abstracts only [§II; Supplement S6; references [8]–[27], [32]–[39], [44]–[55]].
  4. Check the interpretation of the after-stop and lead-state results: the tracker's velocity lag, the braking prediction's action on it, and what the data do and do not separate [§V-C; §VI "What the braking prediction's share shows"; Tables S33, S33b, S34].
**Will particularly care about**: whether the reported null is a property of this filter in this regime or something broader, and whether the paper's own words stay on the narrower side.
**Possible blind spots**: statistical inference details; safety-regulation and deployment context. To be compensated by Reviewers 1 and 3.

### Reviewer Configuration Card #4

**Role**: Peer Reviewer 3
**Display role**: Peer Reviewer 3 (Cross-disciplinary / Practical)
**Identity Description**: Automated-driving safety-assurance practitioner (adaptive cruise control and emergency braking, scenario-based testing, regulation and responsibility-sensitive models), experienced in the gap between open-loop offline metrics and closed-loop fleet behaviour and in who carries the cost of a safety function.
**Review Focus**:
  1. Check the external validity of the test bed for intelligent-transportation practice: simulated lidar, detector at 2 Hz without latency, straight road, one car model, a lead that always brakes, a recording planner that visited the scored states [§III-A; §III-B; §VI "Limits"; Table S28].
  2. Check the use of regulation- and RSS-derived parameters and the "nominal reference, no compliance" wording [§II "The tracker, safe distances and regulation"; §IV-C; Supplement S3, S8.1].
  3. Stakeholder scope (§IV, #1098): check who the evaluation assumes benefits from a margin source, who bears the cost of plans that are safe only because a stop follows (occupants, traffic behind the ego, progress), and which road users are outside the test (pedestrians, cyclists, crossing and cut-in vehicles) [§I "Scope"; §VI "Which commitment is representative"; Table S36; §V-E].
  4. Check the practical reading offered to designers and assessors: the conditional statement on commitments, the "does not justify removing a covariance margin" caution, the time-gap baseline, and the supplementary closed-loop check that runs no covariance margin [§VI; Table S37; Supplement S3].
**Will particularly care about**: whether a safety engineer could act on the conclusions without over-reading them.
**Possible blind spots**: estimator theory; bootstrap details. To be compensated by Reviewers 1 and 2.

The fifth seat is the fixed Devil's Advocate. It has no configuration card and is not dynamically configured.

## Stakeholder Coverage

Seat: Peer Reviewer 3 (Cross-disciplinary / Practical), Review Focus item 3
Check: who the evaluation assumes benefits from a margin source, who bears the cost of plans that are safe only because a stop follows, and which road users are outside the test, with the passages named in the item.
Competence basis: the card's identity is an automated-driving safety-assurance practitioner experienced in ADAS/AEB, regulation and the allocation of safety cost between vehicle occupants and surrounding traffic.

## Review Strategy Recommendations
- **Fresh submission.** The manuscript discloses two earlier AI-panel reviews and added analyses [§IV-D; Supplement S4, S10, S11]. Seats review it as a new submission and judge whether the disclosure is complete and plainly worded, not whether earlier review points were met.
- **Length and density.** Main text 12,451 words against a 10-page recommendation, plus a 34,240-word supplement [manifest]. Seats name what a journal reader needs and what could move to the supplement.
- **Claim-to-table traceability.** Abstract, §I contributions and §VII each carry numbers (5.6 pp, 2.2 decisions, 83%, 12%, 90%, 99.9%, 1.10, 99.26%). Seats trace each one to a main-text table.
- **Author gates.** The author block, repository/DOI and the author confirmation are placeholders for the author. Seats list them separately as submission gates, not as scientific findings.
- **Tension to expect.** Reviewer 1 may read the null as under-resolved; Reviewer 2 may read it as expected from filter theory; Reviewer 3 may read both as narrow for practice. The synthesizer arbitrates.
- **Devil's Advocate** attacks the central logic (the null, the room, the oracle as reference, the measure's sensitivity) without a card.
- **Criteria binding unavailable.** No pointer-only criteria brief was supplied; seats make no criterion-level venue-alignment claim.
