# ARS Pre-Submission Review of Draft v12 (target: IEEE OJ-ITS, regular paper)

**Time stamp:** 2026-11-19 10:34 −05:00 (local clock, read before writing)

**Manuscript:** "Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution: A Fixed-Noise Kalman Tracker in CARLA Lead Braking" (`revision_v12\package_v12\`: `MANUSCRIPT_v12.md`, `SUPPLEMENT_v12.md`, figures). Treated as a fresh submission. Nothing in the package was changed.

**Models**
- v12 was written by Claude Opus 5.5.
- The five reviewer seats ran on a Claude Sonnet model (alias `sonnet`; expected Sonnet 5.5), a different model from the v12 writer.
- The Phase 0 cards were written by Claude Sonnet 5.5.
- The user switched this session to Claude Opus 5.5 when accepting the cards. So the synthesis, the Step 2 verification and this summary were written by the same model that wrote v12. See Section 2.

**Record files**
- `ARS_DECISION_PACKAGE_v12_v01.md`: the record.
- `ARS_AUTHOR_LETTER_v12_v01.md`: the author's version.

## 1. Decision and confidence

| Question | Answer |
|---|---|
| **Most likely referee decision** | **Major Revision.** All four card-backed seats recommend Major Revision, each with confidence 4. The Devil's Advocate's one CRITICAL issue (C1) was adjudicated **VALIDATED** in substance and judged repairable: `da_critical_adjudications: [C1=VALIDATED]`. No seat recommends Reject or Minor Revision. |
| **Confidence in that decision** | **High.** Five of five seats point the same way. My reading of what a human editor would do: Major Revision about 75%; Reject about 15% (an editor who reads it as an expected null in one simulated scenario, at an estimated 15–18 pages); Minor Revision about 10%. This is a judgement, not a calibrated probability. |
| **Change since v11** | v11 was a "soft" Major Revision: no blocked dimension, no DA CRITICAL, and about 35% chance of Minor in that review's own reading. v12 resolved 17 of v11's 19 required items (one is partly done; one is the author's deposit), and the arithmetic is clean. Even so, v12 is a **firmer** Major Revision than v11: the DA CRITICAL is validated and every seat now asks for new runs or re-scoping, not only rewording. The decisions were reached by different routes (v11 with a sprint contract, v12 without), so the comparison is qualitative. |
| **Core result** | No seat doubts the tracker-covariance null, or the arithmetic: about 15 conversions were recomputed and every abstract number was traced. The objections concern reach, which takes three forms. (1) The confirmatory result is the null the steady state predicts, and no arm uses a covariance that varies. (2) The positive control grades between-phase allocation, not information at the tracker's scale. (3) The quotable numbers (90% and 99.9% held out, 83%, 12%) are exploratory, conditional on test-bed choices (2 Hz without latency, filter tuning, a stop that out-brakes every lead), and they move with the recording policy. |
| **Desk-rejection risk** | **Moderate** (Journal-Fit seat). In scope, with a 248-word abstract. But 12,451 words of main text plus 34,240 of supplement, against a 10-page recommendation, and an expected null as the one confirmatory result. |
| **Volume** | **13 required items (R1–R13)** and **25 suggested items (S1–S25**: 21 should-fix, 4 consider). New data or offline re-runs are needed for R2, R10 and R13 (re-tracking or re-detection on the stored data), for R8 (fresh runs, or a tuning-run transfer test), and optionally for R5, R6, R12 and S18. The others are rewording or re-analysis of stored arrays. |

**Submission gates (author-only; not scientific findings)**
- the author block (manuscript line 5);
- the repository and DOI in Data and Code Availability;
- the "[AUTHOR CONFIRMATION: …]" at the end of the AI-generated-content statement.

## 2. How the review ran, and what bounds it

- **Skill.** `academic-research-skills:academic-paper-reviewer` v1.11.1 (plugin 3.24.3), mode `full`, **without a sprint contract**: Synthesis Protocol plus the qualitative decision standards. v11 used contract `reviewer/reviewer_full/v2`. The two decisions therefore come by different routes, and the contract's phase-conformance and panel-synthesis checkers do not apply here.
- **Phase 0.** Coverage and four cards (`00_phase0_field_analysis_and_cards.md`).
  - The whole package was read: manuscript, supplement, all figure PNGs.
  - Not read: the PDF duplicates of Figs. 1–4, and the deposit, which was not supplied.
  - The user accepted the cards unchanged ("Accept cards").
- **Phase 1.** Five seats, each a separate fresh subagent given only the package and its card.
  - Journal-Fit (OJ-ITS associate editor).
  - Methodology (resampling and evaluation design).
  - Domain (tracking and Kalman estimation).
  - Practical (ADAS/AEB safety assurance; stakeholder check).
  - Devil's Advocate.
  - Reports are in `phase1\01_…05_…md`.
- **Phase 2 (Step 1).** `10_step1_editorial_decision_package.md` was written before any Step 2 file was opened. It is the blind panel view: sub-claim inventory, six arbitrated splits, DA adjudication, roadmap.
  - Its provenance section was corrected afterwards. I had first said the provenance builder was not installed; it is, in the plugin's root `scripts\`.
  - No finding or decision changed.
- **Step 2.** Only after Step 1 was saved, I opened the following, in order:
  1. `review_v11_output\ARS_REVIEW_v11_v01.md`;
  2. `revision_v12\RESPONSE_TO_REVIEW_v12.md`;
  3. `AMENDMENT_09_ARS_REVISION_v01.md` and `AMENDMENT_09_ADDENDUM_01.md`;
  4. `recount_v12\RECOUNT_COMPARE_v12.md` and `RECOUNT_COMPARE_A93_v02.md`;
  5. the headings of `notes\CLAIM_AUDIT_v12_v01.md`;
  6. the file times of `revision_v12\analysis\`.

  Every verdict in Section 5 was judged from the v12 text, with the line or table cited.
- **Provenance.** Built and replay-validated with `review_panel_provenance.py` (`validate` PASS; `validate-carrier` PASS).
  - It ran through an LF-line-ending wrapper, because this Windows install's `full.json` has CRLF endings. The v11 review used the same workaround. Plugin files were not changed.
  - Role-separated: true. Fresh context within the panel: true.
  - **Blind to peer outputs: unknown.** Seats were told not to open each other's files, but the task logs are empty, so file access is not observable.
  - Model family, provider and human distinct: false. The correlated-error disclosure is required: *all model-executed review seats used one model family; role separation does not remove correlated-error risk.*
  - Calibration: `NOT_CALIBRATED`.
  - No cross-model check was run.
- **Same model as the writer.** The synthesis, the Step 2 verdicts and this file share the v12 writer's model (Opus 5.5), so self-preference cannot be ruled out. The mitigations:
  - the synthesis adds no comment of its own (every item traces to a seat's report);
  - the six splits were arbitrated on quoted manuscript evidence;
  - every Step 2 verdict cites the v12 line or table.

  The seats, which carry the review judgements, are a different model (Sonnet).
- **Checks run.**
  - `check_author_letter.py`: `AUTHOR-LETTER: PASS` (exit 0, first run).
  - `check_acronyms.py`: exit 0.
  - The reviewer claim check (#1002) was not run, because it needs a judge dispatch. Instead I checked eleven seat claims against the text by hand; all agree.
  - The suggested-reference check was done by hand against Crossref: 6 of 7 found.
- **External traffic.** arXiv and Crossref records reached by identifier, or by the suggested references' own titles and authors. **No manuscript text and no personal details left the machine.** Scholar Sidekick refused (subscription, then rate limits).

## 3. Required items (R1–R13 of this review)

Each item gives the passage it refers to and what would fix it. The record is Part 2 of `ARS_DECISION_PACKAGE_v12_v01.md`, where every item has its sub-claim, anchor, confidence and source. The order is source order, not a work order.

**Framing and fit**
- **R1: Lead with one take-away** (Journal-Fit major; DA C1).
  - **Passage:** §I "so a null is expected; we measure it at decision level and size it"; §VI and §VII offer conditional readings.
  - **Fix:** re-centre on the evaluation protocol and on what an open-loop decision score depends on, with the tracker null as the worked example. Do not present exploratory results as co-equal claims.
- **R2: An arm whose covariance varies, or narrower framing** (CONSENSUS-3: Journal-Fit, Domain, Practical; DA C1).
  - **Passage:** §V-B "It changes the critical values in only 217 decisions, because it can only inflate and the innovation covariance is already too wide"; the §V-B heading "An Adaptive Covariance…"; Table I "Tested".
  - **Fix:** re-run offline on the stored detections with a covariance that varies with the lead's motion (CV/CA IMM; fading-memory or innovation-adaptive Q on the velocity block), or a family whose ratio varies (crossings, track births). Otherwise rename NA "output-scalar NIS inflation" and say in the abstract and contributions that no covariance-varying tracker was tested.
- **R3: Length** (Journal-Fit major; Practical).
  - **Passage:** the whole paper. 12,451 words in the main text and 34,240 in the supplement, against 10 pages; about 40 supplement items are needed to verify the abstract.
  - **Fix:**
    - move interval mechanics, resolution rules, hash strings, the 2 m gap paragraph and most decision-equivalent detail to the supplement;
    - cut the supplement to what the main text needs (S3 and S9 unless used);
    - give a typeset page count.
- **R4: Abstract numbers in main-text tables** (Journal-Fit major; Practical).
  - **Passage:** Abstract, §I, §VII. The held-out 90% and 99.9%, the calibrated 4.4–6.7, the 2.2 decisions, the 83% after-stop share and the 12% range are in no table among II–V.
  - **Fix:** add one main-text table of the exploratory per-phase results, labelled exploratory, or remove those numbers from the three texts.

**Inference and design**
- **R5: Scope of the positive control** (split, arbitrated: Methodology and Domain upheld against the Journal-Fit and Practical strengths; DA M1).
  - **Passage:** §IV-B "Pooled and after the stop, the measure therefore grades partial information, and the null of Section V-A is not a blunt measure". Phase-weighted and before the stop, the mixtures score below the class average (Tables S12, S38). The mixtures are far larger in amplitude than the tracker's 2–5% variation.
  - **Fix:** limit the sentence to where the control grades. Add a test at the tracker's scale: a rank-matched oracle compressed into ±5%, or the graded check on the per-phase-scale frontier. State the grading criterion first.
- **R6: One estimand for the tracker covariance's share** (Methodology major; DA m3).
  - **Passage:** §V-A; Tables S16, S30–S31c. The grid statistic stays primary although it is a grid artefact; the placebo contrast and the gridless interval are uncalibrated; there is no equivalence margin; the 2.2 is a post-hoc maximum over interval ends of mixed validity.
  - **Fix:** gridless or smoothed estimand first, one calibrated interval for it and for N − placebo, an equivalence margin from stakes, and the 2.2 presented as a descriptive range.
- **R7: Held-out per-phase figures** (split on severity, arbitrated Major: Methodology and Journal-Fit major, Domain minor).
  - **Passage:** Abstract "90% … with true phases and 99.9% with the tracker's own phase estimate". These are like-for-like values; against the single-scale frontier of record they are 0.868 and 0.964 (Table S32). There is no interval for the estimated phase, and 0.999 held out exceeds 0.984 in sample.
  - **Fix:** give both bases or state the basis, intervals for every held-out value, two significant figures, and "exploratory" in the abstract.
- **R8: Confirmatory status** (Methodology major; DA C1).
  - **Passage:** contribution 3 "A measured confirmation of the steady state"; Abstract "On 35 runs not used to design the margins"; §III-A "a transfer … not a replication". The same 35 runs have steered three analysis rounds.
  - **Fix:** make the status plain in the abstract.
    - Preferably, generate fresh runs (new seeds, same generator) and run the locked final plan once, with the R6 estimand and the R7 schedule fixed in advance.
    - Otherwise, a tuning-run transfer test of the evaluation-chosen schedule, or take the allocation claim out of the headline.
- **R9: The transfer sentence** (split on severity, arbitrated Major: Practical major, Methodology minor; DA M5).
  - **Passage:** §VI Limits "only comparisons between sources on the same decisions are meant to transfer". Table S35 contradicts it: CK3 0.377 against 0.831; AM in the stopped phase 0.063 against 0.702.
  - **Fix:** restrict the sentence to the null for N and any ordering that holds in both run sets; compute tuning-run intervals. A third recording policy is optional.

**Test-bed conditions behind the quotable numbers**
- **R10: Filter tuning** (Domain major; Practical).
  - **Passage:** §III-A "the simulated sensor data are a likely reason, which we did not test". With position NIS at 0.24 against 2, the velocity lag that carries the after-stop room and the 83% depends on the noise setting.
  - **Fix:** offline re-tracking with NIS near 2, and with a CA or IMM variant. Report the lag (Table S34), the room by phase (Table S33) and the CK3 share. Otherwise add tuning to Limits and to the conditions on the 83%.
- **R11: The 83% needs its condition** (split on severity, arbitrated must-fix: Practical major, Domain minor; DA M6).
  - **Passage:** Abstract "A fixed 3 m/s² braking prediction recovers 83% of the room, open loop and off-policy."
  - **Fix:** add, in the abstract and contribution 2, that every lead brakes to a stop and that the cost behind a non-braking lead is untested.
- **R12: The 12% needs its two assumptions** (Practical major; DA M7).
  - **Passage:** Abstract "a perfect 6 m/s² emergency stop 0.75 s after each decision leaves 12% of it". The stop is perfect, free and independent of perception, and 6 m/s² exceeds every lead's realised deceleration of 2.09–5.46 m/s² (Supplement S1, Table S28).
  - **Fix:** state the first assumption in the abstract (preferably with a scoring where the stop starts from the tracker's belief or after a delay). For the second, report the room by terciles of lead deceleration, or restrict the wording to leads up to 5.5 m/s².
- **R13: Update rate and latency** (Practical major; Domain; DA M4).
  - **Passage:** §III-A "run at 2 Hz, with no latency simulated".
  - **Fix:** re-run detection and tracking on the 20 Hz recordings at 5 and 10 Hz with a stated latency, and report R, the after-stop room and CK3 at each rate. Otherwise say in the abstract that all magnitudes hold for 2 Hz with no latency.

## 4. Suggested items (S1–S25 of this review)

Each line gives the location, then the fix. Severity is minor unless marked.
- **S1** · Abstract · Say that the pooled 5.6 pp and 83% scale with recording length after the stop (8.58 pp without those decisions); consider making per-phase results primary. (Split arbitrated Minor; Journal-Fit's Major dissent recorded.)
- **S2** · §II, S6 · List queries and engines. Read the full ITS threat-assessment texts or restate the finding as abstract-level. Add the suggested references: Mazor 1998; Li & Zhao 2006; Treiber 2006; Naus 2010; Lindemann 2023; Hardy & Campbell 2013; Schubert 2008 (not found in Crossref's top results; to verify).
- **S3** · Abstract, title · Three results, one defining sentence, fewer numerals. Consider a title that names the tested object rather than "Lead Braking".
- **S4** (consider) · §IV–§VII · Fewer labels; each fence stated once in Scope and once in Limits.
- **S5** · Table II, Fig. 2(a), §V-C · One labelled interval type per quantity. Note N's mean outside its interval. Label the 0.90/0.88/0.87 bases.
- **S6** · §IV-D, S4, S10, Table S13 · One provenance paragraph. "External pre-submission review" (S10) and "an independent reviewer" (S4, Table S13) become "AI-based review panel" and "AI session".
- **S7** · S11.4, S11.8, Fig. S4 and Table S29 captions · Remove "A4 extraction", "A9-3", the local path `recount_v12\RECOUNT_COMPARE_A93_v02.md`, `derive_v03.py` and "the earlier draft".
- **S8** · Abstract, §I, §VII · Same claims, same order. The 12% with its range (0.29 to 0.06 at 4 to 7.6 m/s²). Time gap in the abstract or out of §VII. Split §VII.
- **S9** · Abstract, §I, §VII · One wording for 2.2, with scoring, population and post-hoc status.
- **S10** · S10.9, S11.8 · A hand-checkable subset with an independent clearance routine; N-share intervals by a second program.
- **S11** · §IV-B, Table S21 · R and shares under caution windows to 5/10/15%. Argue for the of-record caution definition, or report signed beside it (DA M8 rates this MAJOR).
- **S12** · Table II · Decision-equivalents, not shares, for non-grading populations.
- **S13** · §V-C, Tables S33–S34 · Run-level breakdown of the 132 decisions; staleness against smoothing; intervals.
- **S14** · §V-E, Table V, S10.7 · Ratio against heading offset and track age; why benign is 60.45%; the 0.703–1.043 run; row flips under ±5%.
- **S15** · Contribution 4, Table V · Cut-in carry-over: ratios around the cut-in event and by track age, or drop cut-in from the list.
- **S16** · Table S34b, Fig. S1 · NIS/NEES per phase at update time, with intervals.
- **S17** · §V-C · Add the table behind "435.2 decision-equivalents with a tracker speed above 2 m/s". The pre-stop total is 419.1.
- **S18** (major) · §VI · Runs with a lead that does not brake hard (constant speed, mild braking, stop-and-go): wrong goes and caution for CK3 and the phase schedule.
- **S19** (consider) · Limits · One event-level table: runs with contact and impact speed, by source, at two matched cautions.
- **S20** · Abstract, §VII · Carry "It does not justify removing a covariance margin from a deployed stack" into both.
- **S21** · §IV-C, S3, [42] · Cite the adopted R157 text and its status; remove compliance-sounding sentences from S3; relate 6 m/s² to AEB and ACC envelopes.
- **S22** (consider) · §III-C, Table S37 · TG+N and TG+F0 arms; headway range against ACC practice.
- **S23** (consider) · S3.4 · Put the fallback share into the quoted closed-loop sentence, or drop the R157-unit statement.
- **S24** · Abstract, §V-C, §VII · The tracker-phase schedule is a diagnostic, not a design result, until tested on pull-away and gentle-brake leads.
- **S25** · §II · Relate the time gap, the stop and the lead decelerations to ISO 15622, ISO 22179, UN R152 and IEEE 2846.

**Questions for the author** (from the seats, not covered by an item above)
- What does companion manuscript [9] share, and does the editor need it?
- Was the −1.0 m/s² phase threshold fixed before the held-out values? (Step 2: yes. Amendment 09 fixed −1.0, with −0.5 and −2.0 as sensitivities, before any value.)
- How do R and the shares change if recordings are cut 5 s after the stop?
- Would N's ratio stay near 1.10 if the planner propagated with the tracker's own process noise?
- Why is Table S36's before-onset row 5.0% for every source, the oracles included?
- Will the deposit's file times show each amendment before its values?

## 5. Verification of the v11 review's items against v12

**Resolved** means the v11 fix is in the v12 text. **Partly** means some of it is; the rest is named. **Not resolved** means it is absent. "→ v12 Rn/Sn" points to where this panel picks the topic up again. Line numbers are those of `MANUSCRIPT_v12.md`.

**Summary**
- **Required R1–R19:** 17 resolved, 1 partly (R14), 1 not resolved (R15, the deposit; author gate).
- **Suggested S1–S32:** 26 resolved, 3 partly (S5, S12, S31), 3 not resolved (S1; S4, which got worse; S32, author).
- **Compiler notes C1–C3:** 2 resolved, 1 partly (C2).
- **Section 6 new issues:** 10 resolved, 1 partly (#10).

The response file claims 18 Done and 1 Author for R; 26 Done and 6 Partly for S; and 3 Done for C. The differences:

| Item | Response file | This review | Why |
|---|---|---|---|
| R14 | Done | Partly | Sentences now use decisions, but Table II still prints CK3 0.472/0.606 as shares for ego-moving and lead-braking (line 172), and §V-D gives shares in parentheses beside "where the measure does not grade" (line 194) → v12 S12 |
| S1 | Partly | Not resolved | Asked for the abstract. The abstract still reads only "On 35 runs not used to design the margins" (line 9). §III-A already had it in v11 → v12 R8 |
| S3 | Partly | Resolved | The item allowed the hedge, and §II now has "we did not read the full texts" → v12 S2 |
| S4 | Partly | Not resolved | Longer: body 8,926 vs 7,561 words; supplement 34,240 vs about 27,500 → v12 R3 |
| S5 | Done | Partly | §V-B–D open with a finding (§V-C line 180), but the "keep only numbers used by the Abstract, §VI, §VII" half is not met (Journal-Fit W3) |
| S12 | Done | Partly | §IV-D (line 141) and S11.8 are plain, but S10's introduction still says "after an external pre-submission review", and S4 and Table S13 say "an independent reviewer" → v12 S6 |
| S16 | Partly / Author | Resolved | The item allowed "state and justify the restriction"; line 261 does |
| S32 | Partly / Author | Not resolved (author) | Listed in Data and Code Availability (line 261); no archive yet |
| C2 | Done | Partly | Draft-by-draft rows are gone ("Added in draft" no longer occurs), but internal labels, a local path and "earlier draft" captions remain in S11 and in the Fig. S4 and Table S29 captions → v12 S7 |

### Required items (v11 R1–R19)

| v11 item | Verdict | Evidence in v12 |
|---|---|---|
| R1 Null measured in steady tracking only | Resolved | §I line 21 "The test covers the steady state only"; Abstract "untested for track births, missed updates and real sensors"; Scope line 30 |
| R2 Contribution 3 as a measured confirmation | Resolved | Line 27 "**A measured confirmation of the steady state.**" with its size. (This panel now asks to soften "confirmation": → v12 R8; see Section 7) |
| R3 Abstract fence | Resolved | Abstract line 9; 248 words (manifest; Journal-Fit's own count) |
| R4 Where the measure grades | Resolved | Contribution 1 (line 25), §IV-B (line 125), §VI (line 251), §VII (line 257) use the compiler's corrected qualifier. (→ v12 R5 asks for more) |
| R5 Population mix beside headline numbers | Resolved | Abstract "(83% of 8,290 decisions follow the lead's stop)"; Scope: 82.7% and 77.5% |
| R6 The 89% uses truth phases | Resolved | Abstract "with true phases"; contribution 2 "with the phase taken from the logged truth" |
| R7 Label added analyses | Resolved | Abstract "Exploratory analyses added later …"; contributions 2 and 4; §IV-D (line 141) |
| R8 Null as a bound | Resolved | "none of the room that we can measure" is gone. The bound is 2.2 decisions (§V-A line 149, contribution 3, §VII). (→ v12 R6, S9) |
| R9 Grid effect | Resolved | Placebo, offset family and gridless frontier (Tables S30–S30c); §V-A "not distinguishable from a grid offset" (line 149) |
| R10 Calibrated interval | Resolved | Monte Carlo SD 0.0005, same level under new inner draws (S11.2, Table S31); estimated-rate subsampling (Table S31b). The N-share interval is out of the abstract. (→ v12 R6) |
| R11 Tuning-run values | Resolved | §V-A room 1.18 (line 147, Tables S2, S35); §V-B CK3 0.38 (line 159), AM 0.25 |
| R12 Recording planner as a condition | Resolved as asked | Abstract last sentence; §III-B (line 70); Limits (line 253). The requested transfer sentence is now contradicted by v12's own Table S35 (→ v12 R9) |
| R13 In-sample optimism of the 89% | Resolved | LORO 0.90 and five-fold 0.88 [0.81, 1.00] (Table S32); 0.89 labelled "in sample". (→ v12 R7 on reporting basis and intervals) |
| R14 Grading rule wherever shares are read | Partly | See the differences table → v12 S12 |
| R15 Deposit with reviewer access | Not resolved (author gate) | Data and Code Availability placeholder |
| R16 Tracker as run | Resolved | §III-A: EKF, object-frame noise rotated by heading; Table I: P̄ = mean of reported route-frame covariances (line 86); Fig. 1 "extended KF" |
| R17 Cross-family reach | Resolved | Contribution 4 (line 28) "where the check is silent"; §V-E rotation reason |
| R18 Mechanism of the per-phase and after-stop findings | Resolved (after the stop) | Tables S33–S34b. §V-C: 52.2 of 56.3 decision-equivalents in 132 decisions with tracker speed above 0.5 m/s; before the stop "the attribution does not separate that lag from the braking itself" (line 182). (→ v12 R10, S13) |
| R19 Unscored safety costs in the stop branch | Resolved | §VI line 249: reliance 5.8%, 19.0% and 41.7% (Table S36); "the reading assumes that the stop always comes"; following traffic and occupants named. (→ v12 R12) |

### Suggested items (v11 S1–S32)

| v11 item | Verdict | Evidence in v12 |
|---|---|---|
| S1 Earlier exploratory look, in the abstract | Not resolved | Abstract unchanged on this point → v12 R8 |
| S2 Time-gap margin | Resolved | TG in Table I (line 93), Table II (line 173), Table S37; §VI names 0.314 |
| S3 Full texts or hedge | Resolved (hedge) | §II "we did not read the full texts" → v12 S2 |
| S4 Length toward 10 pages | Not resolved (worse) | 8,926 and 34,240 words → v12 R3 |
| S5 Subsections open with the finding; trim numbers | Partly | See the differences table |
| S6 Define D | Resolved | Notation row D(A) (line 105) |
| S7 Signed caution out of Table II | Resolved | Table II columns All / Ego moving / Lead braking (line 165); Table S21 |
| S8 CARLA sentence | Resolved | Abstract "In CARLA, a CenterPoint lidar detector and the tracker perceive a braking lead at 2 Hz." |
| S9 The 0.5% bound | Resolved | Withdrawn; 2.2 "a bound formed after the values were read" (line 149). (→ v12 R6, S9; see Section 7) |
| S10 Nominal intervals for N not valid | Resolved | Line 149; Table II caption (line 163); Tables III and IV notes (lines 200, 211) |
| S11 Amendment hashes and dates | Resolved | §IV-D (line 141); S11 introduction (full hashes) |
| S12 Who wrote the second programs; qualify "independent" | Partly | See the differences table → v12 S6 |
| S13 ρ_N − ρ_F0 | Resolved | "about as well as" (line 228) |
| S14 Frontier alternates | Resolved | Line 159: CK3 0.79 and 0.75 hull; AM 0.15 hull |
| S15 Caution under the stop scoring | Resolved | Table S36b; §V-D (line 194) |
| S16 Raw recordings | Resolved (restriction) | Line 261 |
| S17 N not on-policy | Resolved | Line 70 "The recording margin is not g p at any g, so every source, the tracker covariance included, is scored on states that another policy visited" |
| S18 NIS by phase; velocity consistency | Resolved | Table S34b; §VI line 245 |
| S19 1.10 is a velocity-block, look-ahead ratio | Resolved | §V-A; Table S14 (1.02–1.05 at t = 0) |
| S20 Map g; "spacing policy" for TG | Resolved | Line 68 and Notation (line 103); lines 44 and 93 |
| S21 MPC car-following and fading-factor references | Resolved | [21], [22], [37] (line 351) |
| S22 Restate [17] | Resolved | Line 36 "the nearest published analogue of the null reported here" |
| S23 Withdrawn wording in S8; dropped NIS sentence | Resolved | S8.2 rewritten (the old phrases survive only as quoted "replaced" rows of Table S4, lines 146 and 155); Table S4 row "The NIS-inflated sentence in the abstract" (line 156) |
| S24 Direction of each simplification | Resolved | S11.9; Limits (line 253). (→ v12 R10, R13 ask to measure them) |
| S25 R as value of perfect information | Resolved | Notation lines 104 and 107: "within the fixed decision rule; not a bound"; den₀ the closer counterpart |
| S26 Tuning-only column of Table S26 | Resolved | §V-E (line 224) |
| S27 Phase schedule from the tracker's own state | Resolved | Table S32; Abstract 99.9%. (→ v12 R7, S24) |
| S28 Register of the 2 m gap | Resolved | §IV-C (line 133) "a model parameter at standstill, not part of the main scoring" |
| S29 "Legal following distance" | Resolved | S3 "the R157 minimum following distance [41, §5.2.3.3] … the test beds lie outside that regulation's domain" (supplement line 52). (→ v12 S21 for the S3.4 sentence) |
| S30 The 12% assumes 6 m/s² | Resolved | §IV-C (line 133) "stronger than the planner's own 5 m/s² fallback"; §V-D 0.18 at 5 m/s² |
| S31 Impact speed | Partly | Stated in the Notation (line 101) and Limits (line 253); closing speed not computed → v12 S19 |
| S32 Deposit of six families' arrays and scripts | Not resolved (author) | Listed (line 261); no archive |

### Compiler notes (v11 C1–C3)

| v11 item | Verdict | Evidence in v12 |
|---|---|---|
| C1 Quoted fixed wording altered by the rename | Resolved | S8.1 quotes "braking prior's share" with "(the plan's wording; the source is now called the braking prediction)" (supplement line 291); Table S4 quotes the plan's wording |
| C2 Draft history inside the supplement | Partly | See the differences table → v12 S7 |
| C3 Abstract numbers | Resolved | Every abstract number traced by the Journal-Fit and Methodology seats; 248 words |

### The v11 review's Section 6 issues

| v11 new issue | Verdict | Evidence in v12 |
|---|---|---|
| 1 Stale S8.2 paragraph | Resolved | Its phrases survive only as quoted "replaced" wording in Table S4 |
| 2 Calibrated interval in the abstract | Resolved | Replaced by the 2.2 bound (→ v12 R6) |
| 3 "None of the room that we can measure" | Resolved | Absent |
| 4 The 89% (in sample, truth labels, no mechanism) | Resolved | Held out, truth labels stated, after-stop mechanism (→ v12 R7, R10) |
| 5 Family check's reach | Resolved | "silent" (contribution 4, §V-E) |
| 6 "Comfort and progress" | Resolved | §VI now names reliability, following traffic, occupants and progress (line 249). The phrase remains only in S3's closed-loop text |
| 7 Notation mappings | Resolved | g: squared quantile; R: analogous to VPI "within the fixed decision rule; not a bound" |
| 8 Register of the 2 m gap | Resolved | Line 133 |
| 9 Dropped NIS sentence | Resolved | Table S4 row (supplement line 156) |
| 10 Altered quotations; supplement length | Partly | Quotations fixed; supplement grew to 34,240 words → v12 R3 |
| 11 Table II layout | Resolved | Signed caution moved to Table S21 |

### Were the consequence rules applied as written, and does the stated verification match the files?

Each rule below was checked against the v12 text and the analysis files.

| Rule | Applied? | Evidence |
|---|---|---|
| A9-1 grid placebo / gridless | Yes | Both intervals contain zero. "not distinguishable from a grid offset" appears in §V-A, §VI and §VII (lines 149, 247, 257) |
| A9-2 calibration and the bound | Yes | MC SD 0.0005 ≤ 0.002 and both inner seeds give 0.9960, so "calibrated" is allowed. The largest end of 2.16 is rounded up to 2.2 and named over every method. The 0.5% wording is withdrawn |
| A9-3 held-out per-phase | As written, with two notes | The abstract and contribution 2 quote held-out values and call 0.89 in sample. Note 1: the rule itself defined the like-for-like gain as primary, so the basis this panel criticises (R7) was **pre-specified, not chosen after the values**. Note 2: "(b) … as in (a)" can be read to require the five-fold interval for the estimated phase as well; v12 gives none. The lowest-level no-choice case was not specified; it was resolved as the recount read it and is disclosed in S11.8 (variant 0.904 / 1.000) |
| A9-4 mechanism | Yes | After-stop concentration shown (52.2 of 56.3 in 132 decisions); before the stop, "does not separate" |
| A9-5 tuning runs | Yes | Printed beside the evaluation values; Tables S2 and S35 cited |
| A9-6 reliance on the stop | Yes | Table S36 cited in §VI |
| A9-7 time gap | Yes | §VI's ranking sentence names 0.314 |
| A9-8 (Addendum 01) before-stop grading | Yes | Mixtures −0.365, −0.258, 0.232: increasing, but the 25% share is below zero, so the measure does not grade. The 29% and 43% are dropped from the abstract; §V-C gives decision-equivalents |

**Verification against the files**
- **Order of writing and computing.** Amendment 09 was saved at 00:17 (clock 00:16, as printed), and its first output at 00:21. Addendum 01 was saved at 01:08:49, and its script and output at 01:09:02 and 01:09:16. So both were defined before their values, as stated.
- **Recount.** The files match the response and S11.8: 338 values, 330 agreeing and 8 differing, all in A9-3. The corrected first program then agrees on 10 of 10 (`RECOUNT_COMPARE_A93_v02.md`). The large differences (first program 0.298 and 0.390 against the recount's 0.903 and 0.999) are consistent with one bogus point at the lowest level dominating a step frontier, as S11.8 explains.
- **Two gaps between the stated verification and the files.** Neither changes a number found by the seats, and both are compiler notes, not seat findings.
  1. Table S38 (Addendum 01) was computed at 01:09, after the recount's last file (01:03). S11.8 does not list it among the one-program results, although Amendment 09 §3 asks that values printed in §V–VII be recounted.
  2. The claim audit (`CLAIM_AUDIT_v12_v01.md`, saved 01:07) covered an earlier draft, and the package was written at 01:13. The response says the fixed text has had no second audit; the paper does not say so. The audit's O10 (calling the AI reviews "external") was fixed in §IV-D and the S11 introduction, but not in the S10 introduction, S4 or Table S13.
- **Response inaccuracy.** The response gives the abstract as 249 words (R3 and S1 rows); the manifest and the Journal-Fit seat count 248.

## 6. Issues introduced by this revision

Each comes from new v12 text or a new v12 analysis.
1. **Length grew** (→ v12 R3): body from 7,561 to 8,926 words; supplement from about 27,500 to 34,240.
2. **The held-out headline** (→ v12 R7, R4, S24). The abstract's 90% and 99.9% are like-for-like (0.868 and 0.964 against the frontier of record), with no estimated-phase interval and false precision. §V-C opens with "most of it is an allocation of caution between phases that the tracker's own state can steer" (line 180), and §VI says the same, stronger than the exploratory status allows (DA m5 also flags the conclusion's version).
3. **The transfer sentence** (→ v12 R9). Added for v11 R12, it is contradicted by v12's own Table S35.
4. **The 2.2 bound** (→ v12 R6, S9). Adopted as v11 S9 suggested, it reads in the abstract and §VII as an inferential bound but is a post-hoc maximum over interval ends of mixed validity, and it is not scoring-qualified (5.3 decisions under a 2 m gap).
5. **"A measured confirmation"** (→ v12 R8). Added for v11 R2, it now heads a contribution computed on runs reused across three rounds.
6. **"435.2 decision-equivalents"** in §V-C has no table (→ v12 S17).
7. **Internal identifiers** in S11 ("A4 extraction", "A9-3", a local recount path) (→ v12 S7).
8. **Review-provenance wording** is fixed in §IV-D but not in S4, S10 or Table S13 (→ v12 S6).
9. **Stop-reliance data** (Table S36: 41.7% of lead-braking decisions rely on the stop). This is not a defect; it is new evidence that sharpens the 12% caveat (→ v12 R12).
10. **Verification of the final text** (compiler note; Section 5): Table S38 is not recounted and not listed as one-program, and there was no second claim audit.

**What the revision did well** (seat strengths, confirmed in the text)
- The grid placebo and gridless frontier settle what the 0.0012 was.
- The held-out schedule, including one built on the tracker's own phase estimate, answers the in-sample objection.
- The after-stop mechanism is shown on the logged lead state.
- The tuning-run values are reported honestly, including the unfavourable ones.
- A time-gap baseline is scored.
- Every consequence rule was applied as written.
- The recount caught and fixed a real held-out error (30% → 90%) before it reached the package.

## 7. Where this panel revisits what v11 asked

Several v12 required items deepen, or partly reverse, wording that the v11 review requested and v12 delivered. They are not regressions: the author did what v11 asked, and a different panel, given new analyses, reads further.
- **v11 R2** asked for "a measured confirmation"; **v12 R8** asks to drop "confirmation" while the runs are reused.
- **v11 S9** proposed "the largest upper end across methods (2.2 decisions)"; **v12 R6 and S9** ask to present it as a descriptive range, not a bound.
- **v11 R12** asked to say "only relative comparisons between sources are meant to transfer"; **v12 R9** finds that the new Table S35 contradicts it.
- **v11 R4** (compiler-corrected qualifier) settled where the measure grades; **v12 R5** says "not a blunt measure" still overreaches at the tracker's amplitude.
- **v11 R13 and S27** asked for held-out and tracker-phase schedules; **v12 R7 and S24** accept them but ask for the record basis, intervals and a non-design reading.
- **v11 S24** asked for the direction of each simplification; **v12 R10 and R13** ask to measure two of them (tuning, update rate).
- **v11 S2** asked for a time-gap arm; **v12 S22** asks for TG plus covariance.

**What follows for the next round.** Another pass of rewording and new analyses on the same 35 runs is likely to produce a fourth list like this one. Two steps close most of the remaining required items at once:
- **(a) One offline re-tracking campaign** on the stored detections and recordings, with re-tuned noise, a CA or IMM variant, and 5 and 10 Hz with latency (R2, R10, R13).
- **(b) A fresh batch of evaluation runs** scored once under a plan locked in advance, with the estimand, the equivalence margin and the schedule fixed (R6, R7, R8, R9).

Together with re-centring and cutting to about 10 pages (R1, R3, R4), the rest is wording (R5, R11, R12).

## 8. Plain-language summary (coffee shop)

This is the best-made cup the café has served. Nearly every note from the last tasting was dealt with: 17 of 19 must-fix notes, with the last two being the recipe card that only the owner can put on the counter and one note half-done. The measuring spoon was checked against a dummy spoon set one notch over on the scale (they taste the same). The flavour was traced to its source (the tracker still thinks the lead car is rolling in the second after it stops). Even the barista's own taste test caught a mistake before the cup left the kitchen.

But the five tasters now judge the coffee rather than the menu card, and all five send it back for adjustment. The devil's-advocate taster's main complaint was upheld. The one thing the menu promises for certain, that this bean adds nothing, was guaranteed by how the machine is built. The interesting flavours (90%, 99.9%, 83%, 12%) were all found by re-tasting the same 35 cups after the fact. They change when a different barista pulls the shot, and they depend on a slow grinder (2 Hz), a misadjusted dial and an emergency brake that always works. The cup has also grown to about three times the size the shop serves.

So the score stays at **about three and a half stars**, the same as last time. The coffee is better, but rewording the menu no longer moves the score. The next half-star needs two things. First, a fresh batch the tasters have never sipped, tasted once with the rules written down beforehand. Second, one shot from a machine whose pressure actually varies (a tracker whose covariance changes), pulled from the beans already in the fridge. Serving it in a normal-size cup does the rest.

## 9. Files (all in `review_v12_output\`)

- `ARS_REVIEW_v12_v01.md`: this summary.
- `ARS_DECISION_PACKAGE_v12_v01.md`: the record. It holds the decision letter, consensus and six arbitrated splits, the DA adjudication, the full roadmap (R1–R13, S1–S25) with sub-claims, anchors and confidences, the reviewer summaries, the sub-claim inventory, the claim-to-table trace, the provenance and the advisory attachments.
- `ARS_AUTHOR_LETTER_v12_v01.md`: the author's version (38 numbered changes; item map in its appendix). `check_author_letter.py`: PASS.
- `10_step1_editorial_decision_package.md`: the blind Step 1 synthesis, written before any Step 2 file was opened. Its provenance section was corrected afterwards, as marked.
- `00_phase0_field_analysis_and_cards.md`: Phase 0 coverage, cards and stakeholder coverage.
- `phase1\01_journal_fit_reviewer.md`, `02_reviewer1_methodology.md`, `03_reviewer2_domain.md`, `04_reviewer3_practical.md`, `05_devils_advocate.md`: the five seat reports.
- `work\panel_provenance_input_v12.json`, `panel_provenance_v12.json`, `panel_provenance_carrier_v12.json`: provenance, replay-validated.
- `work\acronym_check_v12.json`: acronym check.
