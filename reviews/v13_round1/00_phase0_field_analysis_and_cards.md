# Field Analysis Report: draft v13 (Phase 0)

Written 2026-11-21 (clock read 02:59 EST) by the reviewing session, Claude Fable 5.2 (`claude-fable-5-2`). The v13 text was written by Claude Opus 5.5. The reviewing model differs from the writing model on purpose.

**Card confirmation (Checkpoint Rule 1): the pause was not held.** This review runs as a non-interactive sub-agent that cannot ask the user. To keep the user's control over the yardstick, no new reviewer identity was invented: the four identities below are, word for word, the cards the user accepted unchanged for the v12 review on 19 Nov 2026 (`review_v12_output\00_phase0_field_analysis_and_cards.md`). Only the Review Focus anchors were re-pointed to v13's sections and tables, because v13 was restructured. That re-pointing has not been confirmed by the user. If the user wants different cards, Phase 1 must be run again.

**Freeze note (added 03:17).** This file was written against the 02:51 freeze. The text was re-frozen at 03:03 and 03:08; the review is based on the 03:08 files (manuscript hash 433be494), where the counts are: abstract 217 words, body 5,230, whole manuscript 8,467, supplement 11,966, still 10 typeset pages. The coverage and the cards are unchanged.

## Paper basic information
- **Title:** Do Fixed-Noise and Interacting-Multiple-Model Tracker Covariances Improve Planning Decisions? An Equal-Caution Test on Fresh Simulation Runs, in Closed Loop and on Real Driving Logs
- **Abstract:** 218 words (build report)
- **Length:** body 5,191 words; whole manuscript 8,405; supplement 11,950 (build report; `wc -w` gives 8,406 and 11,950). Typeset: 10 pages in `ieeetj.cls` (LaTeX log and `pdftotext`).
- **References:** 42
- **Tables and figures:** five tables, four figures

## Field analysis

| Dimension | Result |
|---|---|
| Primary discipline | Intelligent transportation systems: perception-to-planning safety evaluation of automated vehicles (car following) |
| Secondary disciplines | Multi-object tracking and Kalman estimation; simulation-based and log-replay safety assessment; statistical evaluation methodology (pre-registration, bootstrap inference, equivalence testing) |
| Paradigm | Quantitative; simulation experiment with open-loop and closed-loop scoring, plus log replay on a public data set |
| Methodology type | Pre-registered confirmatory tests in fixed sequences, with oracle positive controls; labelled exploratory and descriptive analyses |
| Target journal | IEEE Open Journal of Intelligent Transportation Systems, regular paper, about 10 pages. No criteria binding or Target Criteria Brief was supplied, so `criteria_binding_unavailable` applies: seats judge fit against these stated parameters and general field norms and cite no criterion ids |
| Maturity | Pre-submission. Three author-only placeholders remain: author block, repository and DOI, author confirmation in the AI-content statement |

## Coverage

| Part | Status |
|---|---|
| Title, abstract, index terms | read |
| Sections I–VII, Tables I–V | read |
| Data and Code Availability, Funding, Competing Interests, Acknowledgment | read |
| References [1]–[42] (the list as text; the cited works were not opened; no online lookup) | read |
| Figs. 1–4 (PNG) | read (viewed) |
| Supplement S1–S13, Tables S1–S29 | read |
| `MANUSCRIPT_v13.tex` | read in part (structure, floats, bibliography) |
| `MANUSCRIPT_v13.pdf` | **not readable as pages**: no PDF renderer is installed on this machine. The page count (10) and the layout warnings were taken from the LaTeX log; the text layer was extracted with `pdftotext` and checked for page count, unresolved references and placeholders. Page images (table placement, column overflow) were not seen |
| Deposit (code, arrays, lock manifests, file-time manifest) | not read: not part of the frozen package; the repository is a placeholder |

No seat makes a statement about the deposit. Statements about the typeset layout rest on the log and the text layer only.

## Reviewer configuration cards

Identities as accepted for v12. Focus anchors re-pointed to v13.

### Card 1: Journal-Fit Reviewer (internal role `EIC`)
**Identity:** Senior associate editor for *IEEE Open Journal of Intelligent Transportation Systems* (regular papers), with editorial experience in automated-vehicle perception, planning and safety evaluation; judges novelty, significance, fit with the journal's readership and the clarity and length of a submission, and does not review methodology in depth.
**Review focus:**
1. Novelty and significance of the three contributions for a regular paper [Section I, contributions 1–3; Section II "Novelty, with its limits"; Supplement S13].
2. Whether the title, abstract, introduction and conclusion state the same claims, and whether each is carried by a main-text table [Title; Abstract; Section I; Section VII; Tables II–V].
3. Clarity and length against about 10 pages: vocabulary, table density, how much of the supplement a reader needs [Sections IV–V; Supplement].
4. How the paper handles its disclosed AI assistance and AI-panel reviews for a journal submission [Section IV-E; Acknowledgment]. Author placeholders are submission gates, not findings.
**Cares about:** one clear, useful take-away for the journal's readers.
**Blind spots:** interval methods, filter theory, regulation detail.

### Card 2: Peer Reviewer 1 (Methodology)
**Identity:** Applied statistician and simulation-evaluation methodologist, specialising in resampling inference for non-smooth statistics, operating-curve and frontier comparisons, positive controls and the separation of planned from exploratory analyses; experience reviewing log-replay evaluations of automated-driving components.
**Review focus:**
1. Whether the scoring construct (wrong go, caution, gridless step frontier, room, share, partial-oracle grading, the amplitude-matched ranking oracle) supports the claims [Section IV-A to IV-C; Table II; Supplement S2, Table S8].
2. The inference: run bootstrap, double-bootstrap calibration and its fallbacks, the equivalence margin, fixed hypothesis sequences, the IMM classification rule [Section IV-C to IV-E; Tables II, S4, S9].
3. Design and status: fresh runs scored once, the two-stage lock, deviations, second programs that share the library and draws, the closed-loop matching and paired tests, the real-log clearance change [Sections III, IV-E; Supplement S3 (Table S5), S9, S10, S12].
4. Whether numbers in the abstract, Section I and Section VII are reproduced by the tables, with consistent interval types [Abstract; Tables II–V; Table S9].
**Cares about:** whether an interval or classification is stated for the quantity actually estimated, and whether anything descriptive is worded as more.
**Blind spots:** filter theory; automotive practice.

### Card 3: Peer Reviewer 2 (Domain)
**Identity:** Researcher in multi-object tracking and Kalman-filter-based estimation for road vehicles, familiar with covariance consistency (NIS/NEES), adaptive and multiple-model filtering and with how tracker uncertainty is passed to prediction and planning.
**Review focus:**
1. The account of why a fixed-noise filter's covariance is nearly constant, and the margin-ratio evidence [Sections V-B, VI; Table III; Supplement S11].
2. The tracker variants: re-tuned CV, CA, IMM and adaptive process noise; their tuning rules, consistency by phase, and whether the IMM arm is a fair test of "a covariance that varies" [Section III-D; Section V-B; Table III; Supplement S4, Tables S6, S7].
3. Literature coverage and positioning [Section II; Supplement S13; reference list].
4. The interpretation of lag, update rate, latency and filter tuning [Section V-D; Table V; Supplement S6.2].
**Cares about:** whether the null is a property of these filters as tuned or something broader, and whether the wording stays on the narrower side.
**Blind spots:** statistical inference; regulation and deployment.

### Card 4: Peer Reviewer 3 (Cross-disciplinary / Practical)
**Identity:** Automated-driving safety-assurance practitioner (adaptive cruise control and emergency braking, scenario-based testing, regulation and responsibility-sensitive models), experienced in the gap between open-loop offline metrics and closed-loop fleet behaviour and in who carries the cost of a safety function.
**Review focus:**
1. External validity of the test beds: simulated lidar, 2 Hz, straight road, the closed-loop operating points, the nuScenes adapter [Section III; Section VI "Limits"; Supplement S1, S9, S10].
2. Use of regulation- and standards-derived parameters and the "no compliance" wording [Section II; Section IV-A; Supplement S6.1].
3. **Stakeholder scope:** who is assumed to benefit from a margin source, who bears the cost (occupants, traffic behind the ego, progress), and which road users are outside the tests [Section I "Scope"; Sections V-C, V-D; Section VI; Supplement S8, S9].
4. The practical reading offered to designers and assessors: closed-loop classifications, the time-gap baseline, costs behind non-braking leads, "does not justify removing a covariance margin" [Sections V-C, V-D, VI, VII; Table IV].
**Cares about:** whether a safety engineer could act on the conclusions without over-reading them.
**Blind spots:** estimator theory; bootstrap detail.

The fifth seat is the fixed Devil's Advocate. It has no card.

## Stakeholder coverage

Seat: Peer Reviewer 3 (Practical), Review Focus item 3.
Check: who the evaluation assumes benefits from a margin source, who bears the cost, and which road users are left out.
Competence basis: the card's identity is a safety-assurance practitioner experienced in the allocation of safety cost between occupants and surrounding traffic.

## Review strategy
- Seats treat v13 as a fresh submission and read only the frozen package (manuscript, supplement, figures). The response letter, the pre-registration and the v12 review are read by the synthesizing session only, in a second step.
- Route: no sprint contract, as in the v12 review, so that the decision and the star rating are comparable with v12's.
- Author placeholders are listed as submission gates, not findings.
