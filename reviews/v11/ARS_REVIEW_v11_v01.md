# ARS Pre-Submission Review of Draft v11 (target: IEEE OJ-ITS, regular paper)

**Time stamp:** 2026-11-18 22:17 −05:00 (local clock, read before writing)
**Manuscript:** "Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution: A Fixed-Noise Kalman Tracker in CARLA Lead Braking" (`revision_v11\package_v11\`: `MANUSCRIPT_v11.md`, `SUPPLEMENT_v11.md`, 13 figure files). The SHA-256 prefixes as read match the package manifest: manuscript ea906800b4c3f8f4, supplement 6d8e25d184658950. Nothing in the package was changed.
**Reviewer model:** every seat, the synthesizer and this summary ran on Claude Opus 5.5, not on the model that wrote v11 (Claude Fable 5.2).

## 1. Decision and confidence

| Question | Answer |
|---|---|
| **Most likely referee decision** | **Major Revision.** The contract's mechanical result: `dimension_verdicts: [D1=warn, D2=warn, D3=warn, D4=warn, D5=warn, D6=warn]`, `fired_conditions: [F3, F5]`, `da_critical_adjudications: []`, `editorial_decision=major_revision`. F3 ("two or more mandatory dimensions score 'warn' or worse") fired because all four mandatory dimensions scored warn: methodology, domain accuracy, argument coherence, and venue fit and contribution. |
| **Confidence in that decision** | **Moderate.** The decision is a "soft" Major Revision: **no seat blocked any dimension, no block is fatal, and the Devil's Advocate has no CRITICAL row.** The seats' own advice splits: Journal-Fit major, Domain major, Perspective minor, Methodology none stated. A human editor could reasonably return Minor Revision. My reading: Major Revision about 60%, Minor Revision about 35%, Reject under 5%. |
| **Change since v10** | v10 was Major Revision through F2: two mandatory dimensions (methodology rigour, argument coherence) were **blocked**. v11 has **no block on any dimension**; every dimension sits one step below. The two blocking themes of v10, unvalidated intervals and the "anticipating braking" location claim, are repaired as v10 asked. Panel-wide warnings remain, and they now concern how far the new analyses reach. |
| **Core result** | **No seat doubts the tracker-covariance null.** Methodology calls it robust. Domain finds no domain error carrying it. The Devil's Advocate finds no mismatch between data and conclusion, and every abstract number it checked matches its table. The required work concerns scope wording, the inferential status of the new headline numbers (the calibrated interval and the 89%), the mechanism behind the per-phase and after-stop figures, and the deposit. |
| **Desk-rejection risk** | **Low to moderate** (Journal-Fit seat). The paper is in scope. The abstract is 247 of 250 words, and every abstract number traces to a table. The risks: an editor may read an expected null in one clean simulated scenario as narrow; the paper runs to an estimated 12–13 IEEE pages against the 10 recommended (estimated from counts, not typeset); and two author-only placeholders remain. |
| **Volume** | **19 required items (R1–R19)** and **32 suggested items (S1–S32**: 31 should-fix, 1 consider). Required items that need re-analysis of stored arrays: R9, R10, R13, R18. R11 only moves existing numbers into the main text, and R15 is the deposit. No new CARLA recordings are needed. |

**Submission gates (author-only; not scientific findings):** the author block (manuscript line 5), and the repository name and DOI in Data and Code Availability. Creating the deposit itself is required item R15.

## 2. How the review ran, and what bounds it

- **Skill:** `academic-research-skills:academic-paper-reviewer` v1.11.1 (plugin 3.24.3), mode `full`, sprint contract `reviewer/reviewer_full/v2`.
- **Phase 0:** coverage and four reviewer cards (`ARS_work_v11_v01\P0_field_analysis_v11.md`). Every part of the package was read, every figure image viewed, and nothing was unreadable. **The user accepted the cards unchanged ("Accept, run panel").**
- **Panel:**
  - Journal-Fit Reviewer: OJ-ITS associate editor.
  - Methodology: resampling statistician for clustered and non-smooth statistics.
  - Domain: multi-object tracking and uncertainty-aware planning.
  - Cross-disciplinary/Practical: safety assurance, UN R157/RSS/ISO 21448, value of information.
  - Devil's Advocate.
- **Seat runs:** each seat ran a paper-blind Phase 1 (scoring plan) and a paper-visible Phase 2 in separate fresh subagent contexts.
- **Checks:** all ten seat outputs passed `check_phase_conformance.py`; the panel passed `check_panel_synthesis.py --layer1-only`; the synthesis passed `check_panel_synthesis.py` (exit 0, before and after the attachments were added). I re-ran every checker myself and got the same results.
- **Provenance:** built and replay-validated with `review_panel_provenance.py`.
  - Role-separated: true.
  - Fresh context within the panel: true.
  - Blind to peer outputs: **unknown**. The seats were told not to read each other's files, but I could not observe their file access.
  - Model family, provider and human distinct: false.
  - A correlated-error disclosure is therefore required: *all seats used one model family; role separation does not remove correlated-error risk.*
  - Calibration status: `NOT_CALIBRATED`.
  - No cross-model check was run.
- **Blindness disclosure.** Before Phase 0 I read two hand-over notes in the shared notes folder. They summarise v10's decision, its two blocking themes and the list of v11 analyses. The seats and the synthesizer were not given those notes, and they were barred from `review_v10_output\` and from `revision_v11\` outside the package. I opened the v10 review and the response only after the decision package had been written and checked (package time stamp 22:15).
- **Deviations from the plugin's literal protocol:**
  1. **Line-ending wrapper:** the provenance builder ran through a wrapper (`scratchpad\prov_lf_wrapper.py`), because this Windows install's `full.json` has CRLF line endings. With LF endings its digest equals the pinned one. Plugin files were not changed.
  2. **Pre-send self-check:** Phase 2 seats ran the conformance checker as their pre-send structural check. All passed on the first run with no fixes.
  3. **Claim-check judge used a tool:** the judge read its 289 KB prompt with the Read tool, although the prompt says "no tools".
  4. **Unbound-token wording:** the Methodology card states the unbound condition in words instead of the literal `criteria_binding_unavailable` token. The synthesizer accepted the sentence and flagged it.
  5. **Author letter by a helper:** a helper agent drafted the author letter, and the plugin's letter checker then checked it.
- **External traffic:**
  - Seats ran short keyword and DOI look-ups (journal scope; refs [8], [13] and [17]; the DOIs of suggested references on Crossref). The suggested-reference check sent only the suggested titles and identifiers to bibliographic indexes.
  - **No manuscript text left the machine**, as far as the seats' reports and my own commands show.
  - The Scholar Sidekick bibliography audit was refused ("not subscribed"), so the 55 references were not audited as a batch.

## 3. Required items (R1–R19)

Each item gives the passage it refers to and what would fix it. The record is Part 2 of `ARS_DECISION_PACKAGE_v11_v01.md`, where every item traces to a seat finding with its anchor and confidence. The order follows the record and is not a work order.

**Scope of the null (the significance case)**

- **R1 — State that the null is measured in steady tracking only** (Journal-Fit major; Domain major; DA corroborates).
  - **Passage:** §I para. 4: "It still has to be measured: the covariance also depends on detections, misses and track age". The decisions barely exercise those dependences: 10 of 8,290 decisions have a young track, the median run NIS is 0.24, and sensing is clean and simulated. Where updates are missed, the ratio leaves the constant (1.68; Table S27).
  - **Fix:** say in §I, in contribution 3, and in the steady-state statements of §II and §VI that the null holds for regular updates, no misses or births, and fixed geometry. Optional: re-run the tracker offline on the logged detections with controlled drop-outs.
- **R2 — Recast contribution 3 as a measured confirmation** (Journal-Fit major).
  - **Passage:** §I contribution 3 ("A decision-level test…") and §VII.
  - **Fix:** present it as a measured confirmation, in this population, of what the Riccati steady state predicts, and say what the measurement adds (its size: 0.6 of 8,290 decisions).
- **R3 — Abstract fence** (Journal-Fit major).
  - **Passage:** the Abstract.
  - **Fix:** one clause saying that track births, missed updates and real sensing are untested, within 250 words. Rewriting the CARLA sentence (S8) frees the words.
- **R4 — Say where the measure is shown to grade information** (Journal-Fit minor; DA major).
  - **Passage:** contribution 1; §IV-B ("Pooled, the null … is therefore not a blunt measure"); §VII; the Abstract. Within the lead-braking phase and with the ego moving, the partial oracles do not grade (Table II; Table S12b).
  - **Fix:** qualify the design claim by population. *Compiler's correction:* the record words this as "pooled decisions only". The advisory claim check found, and Table S21 confirms, that the partial oracles also grade within the after-stop phase (0.28, 0.54, 0.78). The accurate qualifier is therefore: **graded pooled and after the stop; not while the lead brakes or with the ego moving.**
- **R5 — State the population mix beside the headline numbers** (Journal-Fit minor; Domain major; split, arbitrated to required).
  - **Passage:** the abstract sentence that gives 5.6 points; §I Scope. 82.7% of the evaluated decisions come after the lead's stop, and 77.5% have the ego at or below 0.5 m/s.
  - **Fix:** one clause in each.
- **R6 — The 89% uses phase labels from the logged truth** (Journal-Fit, Domain, Perspective minor; DA major).
  - **Passage:** the Abstract ("A class-average margin with one scale per phase of the lead's motion recovers 89% of the room") and contribution 2.
  - **Fix:** add "with the phase taken from the logged truth" in both places.
- **R7 — Label the analyses added after the first results** (Journal-Fit, Methodology minor; DA major).
  - **Passage:** the 89%, 29% and 12%, the family ratio check and the calibrated intervals in the Abstract and in contributions 2 and 4. §IV-D and §VII say these analyses were added later; the abstract and the contribution list do not.
  - **Fix:** mark them as exploratory analyses added after the first results.
- **R8 — Word the null as a bound, not as absence** (Journal-Fit, Methodology minor).
  - **Passage:** the Abstract ("recovers none of the room that we can measure"), §VI ("does as well") and §VII. The basic interval and every subsampling interval lie above zero.
  - **Fix:** give the bound reported in §V-A, in the form that R9, R10 and S9 settle.

**Statistics and inference**

- **R9 — Separate the covariance's information effect from the grid** (Methodology major).
  - **Passage:** §V-A ("The step-frontier statistic is non-smooth…"); Supplement S10.1. N's margin is 1.1029 times F0's on 99.26% of binding rows. On the log-spaced grid that offset is 3.40 steps, so N's operating points sample F0's own curve at other grid points. RR(N)'s full-sample value, at the 97.7th percentile of its bootstrap, looks like grid jitter rather than information.
  - **Fix:** add a placebo source (F0 with its variance multiplied by 1.1029²) and report RR(N) − RR(placebo), or compute the frontiers exactly from the per-decision critical scales. Stored arrays only.
- **R10 — Justify or replace the calibrated interval** (Methodology major).
  - **Passage:** the Abstract ("calibrated interval −0.2% to 0.2%"); §IV-B; Tables S16–S17. The 99.6% level rests on the extremes of 1,000 inner resamples, and its Monte Carlo error is not reported. The subsampling upper ends rise with m (0.0033, 0.0038, 0.0047).
  - **Fix:** report the Monte Carlo error, or use m-out-of-n with an estimated rate. Until coverage is shown, or R9 makes the statistic free of grid effects, do not present the interval as having nominal coverage.
- **R11 — Report the tuning-run values** (Methodology major).
  - **Passage:** §V-A, §V-B and §V-D. On the 20 tuning runs (Tables S2 and S25(b)):

    | Quantity | Tuning runs | Evaluation runs |
    |---|---|---|
    | Room under the 3 s commitment | 1.18 pp | 5.56 pp |
    | Room with the 0.75 s stop, relative to its 3 s value | 0.023 | 0.121 |
    | Braking prediction's pooled share | 0.377 [−0.204, 0.840] | 0.831 |

    The main text neither reports these values nor cites Table S2.
  - **Fix:** report them beside the evaluation-run values, cite Table S2, and decompose the difference if feasible.
- **R12 — Name the recording planner as a condition of the magnitudes** (Methodology major; Perspective minor; split, arbitrated to required).
  - **Passage:** the abstract's closing lesson; §VI; §VII; Limits. The recording planner ended 5 of 35 evaluation runs and 10 of 20 tuning runs at contact (Table S28).
  - **Fix:** add the recording policy to the conditions an open-loop score must state, and say in Limits that only relative comparisons between sources are meant to transfer.
- **R13 — Quantify the in-sample optimism of the 89%** (Methodology, Perspective minor; DA major).
  - **Passage:** §V-C ("took its frontier over all triples of scales"); Table S23. The figure is the envelope over 202³ (about 8.2 million) scale triples, chosen on the evaluation runs themselves. The 400 resamples re-optimise in each resample, so they keep the optimism.
  - **Fix:** choose the per-phase scales out of sample (leave runs out), report the held-out gain beside 0.89, and label 0.89 as an in-sample upper value.
- **R14 — Apply the paper's own grading rule wherever shares are read** (Methodology minor; DA major).
  - **Passage:** §VI asks that a measure grade partial information "in every population whose shares are interpreted". Yet §V-B, §V-D and §VI read the braking prediction's shares with the ego moving and while the lead brakes (0.47 and 0.61; signed 0.30 and 0.35; 0.04; −0.89).
  - **Fix:** attach §IV-B's reading to each such sentence, give the value in decision-equivalents, or run the grading check in that population.

**Reproducibility**

- **R15 — Create the deposit with reviewer access** (Methodology minor).
  - **Passage:** Data and Code Availability.
  - **Fix:** plans with hashes, per-decision arrays, second programs and result files, behind a link reviewers can open. The DOI line itself is the author gate.

**Domain accuracy**

- **R16 — Describe the tracker as it is run** (Domain major).
  - **Passage:** §I, §III-A, Fig. 1 and §II call CANMOT a constant-velocity Kalman filter and argue from a linear filter. Table S28 says it runs as an extended Kalman filter with a constant-velocity model in the object frame. The frame of the class-average covariance P̄, and how P̄ was formed, are not stated.
  - **Fix:** describe the EKF; give the frames of the state, the noise and P̄; and say whether P̄ is the mean of logged covariances or the second moment of realised errors.
- **R17 — Reword the cross-family reach claim** (Domain major).
  - **Passage:** §V-E ("so the null of this paper is not expected to carry over to them") and contribution 4. In the crossing and benign families the ratio can vary because a fixed object-frame covariance rotates against a fixed class average, with no information in the variation.
  - **Fix:** say that the check is silent there, as §VI already does. Optional: repeat Table V against a heading-aligned class average.
- **R18 — Give the per-phase and after-stop findings a physical mechanism** (Domain major).
  - **Passage:** §V-C ("The 83% is therefore a figure for recordings that continue for about 20 s after the stop"). The braking prediction recovers 0.99 of the after-stop room (Table S5), but nothing explains why a wrong go happens behind a lead at rest.
  - **Fix:** from the stored arrays, report the tracker's estimated lead speed and acceleration around the onset and against time since the stop, tabulate the rows selected in after-stop wrong-go decisions, and state the mechanism.

**Safety reading**

- **R19 — Name the unscored safety costs in the stop branch** (Perspective minor; DA major).
  - **Passage:** §VI ("the choice of source matters mainly for comfort and progress, which we did not score") and the stop branch of §VII.
  - **Fix:** restrict the statement to ego–lead contact, and name following traffic and the stop's reliability as unscored. Stronger: report, for each source at matched caution, the share of decisions whose selected row is safe only because of the stop.

## 4. Suggested items (S1–S32)

Each line gives the location, then the fix. Severity is minor unless marked.

**Framing and presentation (Journal-Fit)**
- **S1** · Abstract ("35 runs not used to design the margins") · Add that the room and N's difference had been examined on these runs in an earlier exploratory analysis (a transfer, not a replication).
- **S2** (Journal-Fit + Perspective) · §VI ranking · Score a constant time-gap margin, written as a variance along the constraint normal, at equal caution on the stored arrays, or explain why it cannot be put on the same footing.
- **S3** (Journal-Fit + Domain) · §II threat-assessment paragraph; Supplement S6 · Read the full texts of at least [41]–[47] and confirm or reposition the "no prior evaluation" sentence; otherwise hedge it to name the abstract-only reading.
- **S4** · §IV-B "Intervals"; §IV-C para. 3; §IV-D; §V-A para. 2; §V-D 2 m gap; §V-E last paragraph; Table IV; §II "Adaptive covariances" · Move or compress material toward the 10-page recommendation.
- **S5** · §V-B–§V-D · Open each results subsection with its finding in words, and keep in the text only the numbers the Abstract, §VI and §VII use.
- **S6** · §IV-B; Notation table · Define D next to R and RR.
- **S7** · Table II · Give signed caution its own small table, or columns for every population (as Table S21 does).
- **S8** · Abstract; §I · Rewrite the sentence "CARLA runs in which a lead vehicle brakes are perceived by the CenterPoint detector and CANMOT…"

**Statistics and reporting (Methodology)**
- **S9** · §V-A ("no interval method we tried reaches 0.5% of the room") · Say when the 0.5% bound was chosen. Adopt a margin in decision units fixed in advance (one decision-equivalent = 0.0022 of the room), or state the largest upper end across methods (2.2 decisions).
- **S10** · §IV-B; table notes (Tables III, IV, S5, S24) · Say that nominal intervals for N's shares are not valid at their nominal level (coverage 53%), and that the one lead-braking cell excluding zero under the 2 m gap is not a signal.
- **S11** · §IV-D; Supplement S4 · Print the Supplement S10 amendment's hash and date beside the two earlier plans' hashes.
- **S12** (Methodology + Perspective) · §IV-D; Supplement S10.5, S10.9; Acknowledgment · State who or what wrote each second program and recount, name the parts that were not blind, and qualify "independent" to match.
- **S13** · §V-E (ρ 0.453 against 0.458) · Report the paired interval of ρ_N − ρ_F0, or say only that the two are nearly equal.
- **S14** · §V-B · Give the frontier-construction alternates beside 0.83 and 0.38 (CK3 0.831/0.790/0.750; AM hull 0.153), as is done for NA.
- **S15** · §IV-C; §V-D; Table S20c · Add a variant that averages caution over selections safe under the reaction-and-stop scoring, or justify keeping the 3 s definition.
- **S16** (Methodology + Perspective) · Data and Code Availability · Deposit the raw recordings, or state and justify the restriction.
- **S17** · §III-B · Do not single N out as on-policy: the recording margin αp + βq is not g·p at any g. Optionally, report how often the recording planner's choice coincides with N's.

**Domain**
- **S18** · §V-B; §III-A; Fig. S1 · Report NIS by phase (including the onset window) and the consistency of the velocity estimate against CARLA truth. State that the NA result says nothing about adapting the velocity block.
- **S19** · §VI; §V-A · Say that 1.10 is a velocity-block ratio that depends on look-ahead (1.02–1.05 at t = 0; about 1.10 at 2–3 s; Table S14).
- **S20** (Domain + Perspective) · Notation table; §II · Map g to the chance-constraint parameter (a squared quantile of the per-constraint risk level), and keep "spacing policy" for the time-gap baseline.
- **S21** · §II; references · Add stochastic-MPC car following (Moser et al. 2018; Brüdigam et al. 2023) and fading-factor Kalman filtering (Xia et al. 1994). All three were found in an index.
- **S22** · §II on [17] · Restate it: its fixed-covariance constant-velocity baseline is the nearest published analogue of this null.
- **S23** (Domain; DA major) · Supplement S8.1–S8.2; last rows of Table S4 · Remove the withdrawn wording ("a mechanism that no analysis here isolates"; "the location of the room … (Section VI) does not hold"), or mark it as the earlier draft's record. Restore, or record explicitly, the dropped NIS-inflated abstract sentence that the plan fixed.
- **S24** · §VI Limits · Give the expected direction in which each simplification moves the room and the braking prediction's share: 2 Hz detector with no latency, simulator noise off, a nuScenes checkpoint, one car model, straight road, default weather, and the configuration shared with [9].
- **S25** (Domain + Perspective) · Notation table; §IV-B · Describe R as analogous to the value of perfect information, within the fixed rule and not as a bound. den₀ against O is the closer counterpart.
- **S26** (consider) · §V-E · Mention that the tuning-only column of Table S26 shows the same pattern as Table V.

**Safety and practice (Perspective)**
- **S27** · §VI; Table S23(b) · Add a class-average scale scheduled on a phase estimated from the tracker's own state, or say that a deployable schedule is untested.
- **S28** · §V-D ("Performance model 2 asks for 2 m at standstill, not for the absence of contact") · Use the register of Supplement S10.5: a model parameter at standstill; the main scoring counts contact.
- **S29** · Supplement S3, S3.4 ("legal following distance") · Write "the R157 minimum following distance [38, §5.2.3.3]", and note that the test beds lie outside the ALKS domain.
- **S30** · Abstract; §V-D; §VI · The 12% assumes a 6 m/s² stop, but the planner's own fallback brakes at 5 m/s² (0.18 there). State this beside the 12%, or say that the stronger stop stands for a separate emergency-braking function.
- **S31** · Notation table; §VI Limits · Say that wrong-go counts ignore impact speed. Better: report closing speed at first loss of clearance, by phase.
- **S32** · Data and Code Availability · Deposit the binding-row arrays of all six families (Table V, Table S26), the capture scripts and the S3 simulator, or state the restriction.

**Compiler's additional notes** (made by this session while reading, before the v10 review was opened; no seat raised them, so they are not in the record and do not affect the decision; details in `ARS_work_v11_v01\compiler_checks_v11.md`):
- **C1** · Supplement S8.1 and Table S4 (row "The abstract's last sentence") · These print the plan's fixed sentence in quotation marks with "braking prediction's share". Table S4's row "(this version)" prints the same fixed sentence with "braking prior's share". **Fix:** quote fixed wording exactly, and note the rename outside the quotation marks.
- **C2** · Table S4 and the paragraph after it · These print earlier drafts' abstracts and draft-by-draft history ("Added in draft v03/v04/v06"). **Fix:** keep a deviations-from-plan table in the supplement, and move internal draft history to the cover letter or the deposit.
- **C3** · Abstract numbers · I recomputed 13 checks from printed values: decision-equivalents, 2.6×, 0.95 pp, 0.63, 6%, 5.3 / 1.2 / 5.8 decisions, coverage 92–93% and 96–97%, and the commitment ratios. **All agree**; the abstract is 247 words.

## 5. Verification of the v10 review's items against v11

Each verdict is judged from the v11 text, not from the response file. **Resolved** means the v10 fix is present in v11. **Partly** means some of it is present; the remainder is named. **Not resolved** means it is absent. "→ v11 Rn/Sn" points to where the new panel picks the topic up again.

**Summary:** Required items R1–R20: **13 resolved, 7 partly, 0 not resolved**. Suggested items S1–S38: **24 resolved, 9 partly, 5 not resolved** (S1, S3, S16, S21 and S27; S1 and S27 were optional, and S3 is the author's step). The response file claims 17 / 3 / 0 and 26 / 7 / 5 (1 author, 4 not done). The differences:

| Item | Response file | This review |
|---|---|---|
| R2 | Done | Partly |
| R5 | Done | Partly |
| R9 | Done | Partly |
| R13 | Done | Partly |
| S25 | Done | Partly |
| S38 | Done | Partly |
| S11 | Partly | Partly (the two agree) |

### Required items (v10 R1–R20)

| v10 item | Verdict | Evidence in v11 |
|---|---|---|
| R1 Title asks a question theory answers | Resolved | Retitled around the evaluation, with the fixed-noise tracker as the case. §I para. 4: "a null is expected. It still has to be measured". |
| R2 Contribution list leads with an expected result | Partly | The design is now contribution 1, the reason the null needs measuring is in §I para. 4, and the covariance test is third. But contribution 3 reads "A decision-level test", not a confirmatory test of the expected steady state (→ v11 R2). |
| R3 Practical take-away under the realistic commitment | Resolved | New §VI paragraph "Which commitment is representative"; §VII is worded conditionally. Its "comfort and progress" sentence is a new issue (→ v11 R19). |
| R4 Length | Partly | Table IV is down to 5 rows; the old §V-D, the stopping-point paragraph and the planner's cost moved to the supplement; body about 7,000–7,600 words. Still an estimated 12–13 pages, and the 83% / 0.83 appears 8 times in the main text (→ v11 S4, S5). |
| R5 Abstract not self-contained | Partly | Rewritten in plainer terms; it ends on the implication and defines "the room". But it is 247 words (target 200–230) with about 18 numbers, leaving no room for the fences v11 R3, R5, R6 and R7 require. |
| R6 Author block and AI disclosure | Partly (author) | The approval note is gone. The disclosure names Claude Opus/Fable via Claude Code (Nov 2026), the sections drafted and OpenAI Codex. It does not say what the author verified, and the author block (line 5) is still a placeholder. |
| R7 Deposit | Partly (author) | Data and Code Availability lists the deposit's contents; the repository and DOI are still a placeholder (→ v11 R15). |
| R8 Replace "at most about 0.4%" | Resolved | No "0.4%" in the main text. §V-A gives the point, both nominal intervals, the calibrated interval and 0.6 of 8,290 decisions. The new wording raises new issues (→ v11 R8–R10). |
| R9 Validate the step-frontier bootstrap | Partly | Levels rebuilt in each resample (§IV-B); double bootstrap; stratified, 30-run and subsampling sensitivities (Tables S16, S17); NIS rules re-applied. For RR(N), however, no nominal method passes (coverage 53%), and the calibrated interval's own validity is open (→ v11 R9, R10). |
| R10 Censored reaction-and-stop pairs | Resolved | Plans are judged against the logged truth until the stop ends (§IV-C; S10.2): 28 of 5,356 pairs unsafe; the estimate is 0.122 [0.052, 0.188]; counts (i) and (ii) kept as sensitivity analyses (Table S19); abstract updated. |
| R11 Caution conditions on the outcome | Resolved | Signed caution for every source and population (Table S21); a column and a row in Table II; no sign changes; §V-B reports the drops (0.47 → 0.30, 0.61 → 0.35). |
| R12 Post-stop length sets the estimand; mechanism not isolated | Resolved | Truncation at T = 0–20 s (Table S22, Fig. 3(a)); per-phase-scale frontier (Table S23, Fig. 3(b)), which isolates 0.89. Its in-sample status and physical mechanism are new issues (→ v11 R13, R18). |
| R13 The 83% printed only pooled | Partly | The abstract gives 29% beside 83%, and §V-B gives the ego-moving, lead-braking, signed and perfect-oracle values. The abstract still does not name the population that defines the room (82.7% after the stop) (→ v11 R5). |
| R14 Data cannot be regenerated | Resolved | Table S28 gives simulator, world, vehicles, lead script, draws, lidar, detector checkpoint hash, tracker noise values, planner and software versions. Weather is stated as not set. |
| R15 "RSS-style" mislabel | Resolved | Renamed "braking prediction" throughout; §II contrasts it with RSS's worst-case bound; the RSS form is kept for the rule in S3 only. |
| R16 Choice of 3 m/s² | Resolved | §III-C: best of eight values on the tuning runs, inside the recorded range. Evaluation-run sweep in Table S25. |
| R17 Room defined for contact; model 2 uses 2 m | Resolved | §IV-C states that a wrong go means contact, with 2 m as a sensitivity. O and den₀ are scored at 2 m (Tables S24, S24b; §V-D). |
| R18 "Rests on the performance-model values" | Resolved | Sentence gone; the values are "nominal reference parameters … claim no compliance" (§IV-C, §II, Limits). |
| R19 Fence against removing a deployed margin | Resolved | §VI: "It does not justify removing a covariance margin from a deployed stack". Young tracks reported (10 of 8,290; Table S27); crossing and cut-in actors listed as outside (§I Scope). |
| R20 Cross-family reallocation untested | Resolved | Ratio check on all six families (Table V, S26). §V-E states that the cross-family effect is untested. Its reading of the crossings is a new issue (→ v11 R17). |

### Suggested items (v10 S1–S38)

| v10 item | Verdict | Evidence in v11 |
|---|---|---|
| S1 (optional) A source with per-decision varying covariance | Not resolved | Named only as a next step (§VII). |
| S2 Extend the novelty search to ITS venues | Resolved | New §II paragraph with [41]–[52]; S6 updated; novelty sentence narrowed. Abstract-only reading remains (→ v11 S3). |
| S3 Confidential copy of [9]; cover letter; published versions of preprints | Not resolved (author) | [9] is still "submitted"; preprints cited as arXiv. This is a cover-letter step. |
| S4 Plain definitions; Notation table at §IV | Resolved | §I defines wrong go, caution, room and commitment; the Notation table opens §IV. |
| S5 One name per source; relabel the reaction-and-stop columns | Partly | One name per source in the main text and in Figs. 1, 2 and 4. Table III still uses *R* for the 3 s oracle's advantage, and the supplement tables keep the old labels. |
| S6 Graded-oracle table in the main text | Resolved | Three partial-oracle rows in Table II. |
| S7 Describe post hoc analyses neutrally | Resolved | §IV-D is neutral and the main text has no references to reviews; the audit trail stays in S4/S10. |
| S8 Self-contained captions | Resolved | Captions are in the manuscript; the separate captions file is dropped. |
| S9 Characterise the 1,127 rows outside the band | Resolved | S10.7: four runs, by track age, missed updates and phase. |
| S10 One number-format convention | Partly | Table II mixes 4-digit (0.0012) and 3-digit (0.017) shares; earlier tables are unchanged. |
| S11 Abstract: earlier exploratory look at the runs | Partly | Stated in §III-A only, not in the abstract (→ v11 S1). |
| S12 Index terms | Resolved | Car following, ACC, safety evaluation and simulation-based testing are present. |
| S13 Replay identity on the evaluation runs; lead independent of the ego | Resolved | S10.8: 9,307 of 9,307 decisions. §III-A: the lead brakes "independently of the ego". |
| S14 The five short runs | Resolved | They ended at first contact (§III-A, S10.8); 27 of the 217 NA-changed decisions; values without them in Table S17 and §V-A. |
| S15 Resolution rule at 5 and 20; on den₀'s lower limit | Resolved | §IV-C names what would change at each threshold; S10.2 applies the rule to the lower limit. |
| S16 Fieller-type intervals near den₀ = 0 | Not resolved | Not done. The cell belongs to count (ii), which is retired, but count (ii) tables are still printed (S10, S29). |
| S17 Mark the commitment analyses as descriptive in the Abstract and §VII | Partly | §VII says "descriptive analyses added after the first results"; the abstract does not (→ v11 R7). |
| S18 Braking prediction on non-braking runs, or a fence | Resolved | Benign runs tried and found unable to test it; before-onset cost given; §VI: "on runs in which the lead always brakes". |
| S19 Graded oracles over 50 draws | Resolved | Table S12b. |
| S20 (optional) Deceleration sweep | Resolved | Table S25. |
| S21 (optional) Compute the steady-state covariance | Not resolved | The Riccati solution was not computed (the DA notes the same gap). |
| S22 Margin propagated without process noise | Resolved | §III-B states it, with Q carrying the acceleration effect. |
| S23 NA tests only the output-covariance channel | Resolved | §VI, "What an adaptive covariance would need". |
| S24 Present the deviation check as a consistency check | Resolved | §V-E "As a consistency check"; full detail in S9. |
| S25 Justify the update rate; Limits; scope | Partly | 2 Hz is stated in §III-A, in Limits and as the scope of §V-E, but it is not justified (→ v11 S24). |
| S26 Ranking among tested sources; time gap untested | Resolved | §VI: "a ranking among the tested sources; a time-gap margin … was not among them". |
| S27 (optional) Time-gap arm | Not resolved | Named as untested (→ v11 S2). |
| S28 01-series values as nominal parameters | Resolved | §II, §IV-C, Limits. |
| S29 Present the τ and A sweeps as the result | Resolved | Table III and §V-D give the sweeps. |
| S30 State the 2.0–5.5 m/s² range; qualify the 12% | Resolved | §III-A (requested and realised); Limits: "every commitment result holds for such leads only". |
| S31 Fallback share; contacts; not design guidance | Partly | "Not design guidance" is in S3 and Limits; the 0.70–0.72 fallback share stays in S3.4, not in the S3 opening or the Fig. S3 caption. |
| S32 Comfort and following traffic as unmeasured costs | Partly | Named in §VI; no jerk proxy computed (→ v11 R19). |
| S33 List the road users and scenarios left out | Resolved | §I Scope. |
| S34 Map terms to ITS vocabulary | Resolved | Third column of the Notation table. Two mappings are now questioned (→ v11 S20, S25). |
| S35 Worked threshold for the ratio check | Partly | §VI says the data give no threshold and gives one sentence of guidance for planners without a tunable scale. |
| S36 Road type | Resolved | §III-A: "straight, flat and two-lane"; Table S28. |
| S37 (DA) The contrast is not like for like | Resolved | §VI: "the two are different kinds of information and their shares are not like for like". |
| S38 (DA) Call the 83% open-loop and off-policy | Partly | It is in §III-B, §VI and Limits; the abstract's 83% carries neither word, and §VII says "open-loop" only. |

## 6. What the revision introduced

None of these issues was in v10 in this form. Each comes from new v11 text or a new v11 analysis.

1. **A stale supplement paragraph** (v11 S23; also my note). Supplement S8.2 still says that "the location of the room under the 3 s commitment (Section VI) does not hold" and calls the cross-phase effect "a mechanism that no analysis here isolates". §V-C now isolates exactly that, and Table S4 records both phrases as replaced.
2. **The calibrated interval in the abstract** (v11 R9, R10). The v10 fix added a double-bootstrap "calibrated interval". The Methodology seat shows that the non-smoothness it calibrates may be a grid offset: N's margin sits 3.40 grid steps from F0's. The abstract now gives an interval whose coverage is not demonstrated.
3. **"None of the room that we can measure"** (v11 R8). This new abstract wording states absence, while the body reports a bound and both the basic interval and every subsampling interval lie above zero.
4. **The 89% per-phase result** (v11 R6, R13, R18). It is new, it was chosen in sample over about 8.2 million triples, its phase labels come from the truth, and it has no physical mechanism. It now heads contribution 2 and the abstract without those qualifiers.
5. **The family ratio check's reach** (v11 R16, R17). The new reading "not expected to carry over" for crossings ignores that the filter runs as an EKF in the object frame: the ratio can vary through rotation alone.
6. **The new commitment paragraph** (v11 R19). "Matters mainly for comfort and progress" leaves out following traffic and the stop's reliability.
7. **Notation-table mappings added for v10 S34** (v11 S20, S25). Margin scale g is mapped to "safety distance of a spacing policy", and the room to "value of perfect information". Both are looser than those terms' meanings.
8. **The 2 m gap's register** (v11 S28): "Performance model 2 asks for 2 m at standstill, not for the absence of contact".
9. **The abstract rewrite** (DA M5; v11 S23). It dropped the NIS-inflated sentence that the locked plan fixed for the abstract, and Table S4 does not record that removal plainly.
10. **Quoted fixed wording altered by the rename** (my note C1), and **draft history inside the supplement**: the supplement grew to 27,500 words (my note C2).
11. **Table II layout** (v11 S7). The signed-caution column and row added for v10 R11 make the main results table harder to read.

**What the revision did well** (seat strengths, confirmed in the text):
- The interval and censoring problems of v10 are worked through on stored data.
- The 53% is retired on evidence: only 28 of 5,356 pairs are unsafe.
- The location claim is replaced by measured statements.
- The ratio check now covers all six families.
- Table S28 makes the recordings reproducible on paper.
- The fences against deployment ("does not justify removing a covariance margin") are explicit.
- Every abstract number the panel and I checked matches its table.

## 7. Plain-language summary (coffee shop)

Last time the tasting panel sent the coffee back with two real faults. The label overstated where the flavour came from ("it's all in the braking beans"), and the measuring cup used to report the strength had never been checked. This new batch fixes both. The cup has now been checked: the main taste test still says the tracker's covariance adds nothing you can taste. The flavour has been traced to its source: mostly it comes from serving each phase of the drink at its own strength, not from any special bean. So this time **no taster called the coffee undrinkable**: no blocks, no critical complaint. But **every taster still asked for an adjustment**, and the house rule sends a cup back to the roaster when two or more of the main tasters do. That makes the verdict **Major Revision again, but a lighter one**: about three and a half stars now, against roughly two and a half before. To reach five stars, the menu card must say honestly what this cup is:
- tested only with steady pouring, never with a sputtering machine;
- most sips taken after the cup had stopped moving;
- the 89% blend chosen by tasting the same cups it was judged on;
- the extra tastings added after the first ones.

Beyond the card, four jobs remain:
- check whether one measuring spoon is simply sitting at a different notch on the scale (a placebo source);
- explain why sips taken after the cup has stopped still go wrong;
- describe the machine as it actually runs (an extended Kalman filter);
- put the recipe card on the counter (the deposit).

Almost all of this is rewording plus re-tasting samples already in the fridge. No new beans (no new recordings) are needed.

## 8. Advisory checks (script output; they change neither the decision nor any finding)

- **Reviewer claim check (#1002):** of 52 findings, 45 were judged consistent with the text, 3 could not be checked from the text alone, and 4 were marked contradicted:
  - Journal-Fit W9 miscounts the intervals in one paragraph (cosmetic).
  - DA M1 says misses and young tracks are absent; 10 young-track decisions exist, but the point that they are rare stands.
  - DA M4 says the grading caveat is applied only to NA; it is also applied in §IV-B and S8.2.
  - DA M2 says the measure is not shown to grade within any phase; it does grade within the after-stop phase. This is the basis of the correction to R4 above.
- **Suggested-reference check (#1001):** 7 of the 9 references suggested by Domain and Perspective were found in an index. The two ISO standards have no DOI and were not matched. "Found" does not show relevance.
- **Acronym check (#849):** CANMOT, CARLA and RR are used without expansion (CANMOT and CARLA also in the abstract); AI, IEEE and SHA likewise. Flags on AUTHOR, BLOCK, TABLE, AND and NAME are artefacts of the tool. IMM, RSS and NA were not checked (their initials do not spell the expansion).
- **Author letter (#1078):** `ARS_AUTHOR_LETTER_v11_v01.md` restates all 51 changes for the author without internal ids. Items 1–19 are R1–R19; items 20–51 are S1–S32; the item map is in its appendix. `check_author_letter.py` → `AUTHOR-LETTER: PASS` (exit 0, first run; I re-ran it with the same result). The letter keeps R4's wording as recorded; the compiler's correction to R4 is in §3 above only.

## 9. Files (all in `review_v11_output\`)

- `ARS_REVIEW_v11_v01.md`: this summary.
- `ARS_DECISION_PACKAGE_v11_v01.md`: the record. It holds the mechanical decision record, provenance, consensus and two arbitrated splits, the full roadmap (R1–R19, S1–S32) with anchors and confidences, the seat summaries, and the three advisory attachments.
- `ARS_AUTHOR_LETTER_v11_v01.md`: the author-facing letter.
- `ARS_work_v11_v01\`:
  - Phase 0 cards;
  - the contract and metadata;
  - the Phase 1 plans (`P1_*.md`) and Phase 2 reviews (`P2_*.md`);
  - the provenance input and artifact;
  - the claim-check prompt, key and reply;
  - the outputs of the reference and acronym checks;
  - `compiler_checks_v11.md`;
  - `paper_v11_combined.md`, a concatenated copy of the manuscript and supplement used only as checker input.
