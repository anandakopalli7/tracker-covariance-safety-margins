# Editorial Decision Package: draft v12, Step 1 (blind panel view)

Written 2026-11-19. This file is the Phase 2 editorial synthesis of the five Phase 1 reports in `phase1\`. It was written **before any Step 2 file was opened**.

**Blindness record at the time of writing**
- Opened: the v12 package (manifest, manuscript, supplement, figure PNGs), the skill's own files, and the five Phase 1 reports.
- Opened for reference checks: public arXiv and Crossref records, reached by identifier only.
- Not opened: anything else under `revision_v12\` (response letter, claim audit, recount, amendments, notes); anything under `review_v11_output\`; any side-session notes folder; `<excluded folder 1>`; `<excluded folder 2>`; `<excluded folder 3>`.

**Who did what**
- The five seats ran as separate fresh subagents with the `sonnet` model alias (Claude Sonnet family).
- This synthesis was written by the session model, Claude Opus 5.5. The user switched the session to Opus 5.5 at card acceptance, so the synthesizer is the same model that wrote v12.
- The seats, which carry the review judgements, are a different model from the v12 writer.
- See "Review Panel Provenance" at the end.

## Calibration Resolution

`calibration_status: NOT_CALIBRATED`

This is the current runtime boundary. The package is not upgraded from any candidate or prose-named profile. `PROFILE_MEASURED` remains unavailable until a closed profile artifact and replay validator bind the target fields to the completed panel's `execution_topology_sha256`.

Criteria binding: unavailable. No pointer-only criteria brief was supplied, and all five reports disclose `criteria binding unavailable; general field norms`. No criterion-level venue-alignment claim is made. The seats judged fit against the target parameters given in the brief:
- IEEE OJ-ITS, regular paper;
- abstract limit 250 words;
- no page limit, 10 pages recommended.

---

## Part 1: Editorial Decision Letter

Dear Author,

Thank you for submitting "Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution: A Fixed-Noise Kalman Tracker in CARLA Lead Braking" to *IEEE Open Journal of Intelligent Transportation Systems*. It was reviewed through five role-separated, AI-simulated review seats: a Journal-Fit Reviewer, three peer reviewers and a Devil's Advocate. Their execution provenance is reported at the end of this package and is not reduced to a binary independence claim.

### Decision: Major Revision

**Confidence in the decision: high.**
- All four card-backed seats independently recommend Major Revision, each with confidence 4.
- No seat recommends Reject.
- No seat recommends Minor Revision.
- The Devil's Advocate's one CRITICAL issue is validated below. It blocks Accept and Minor Revision, and the panel judges it repairable.

### Consensus Analysis

#### Points of Agreement (Consensus)
- **[CONSENSUS-3] (SC-2): the confirmatory null is expected by construction, and no arm uses a covariance that varies.**
  - Raised by the Journal-Fit Reviewer (W1) and Reviewer 2 (W1, Major); corroborated by Reviewer 3 (W3: the null is "close to guaranteed by construction"). Reviewer 1 is silent; their summary calls the null "probably right" and does not dispute it.
  - The paper tests only a fixed-noise filter in steady state.
  - Its one adaptive source (NA, NIS inflation) can only inflate, and changes 217 of 8,290 decisions.
  - So the study cannot show that its design would register the decision value of a covariance that does vary. Section V-B's heading and Table I's "Tested" label invite a wider reading.
  - DA-corroborated (C1).

#### Below the Consensus Bar
- **[CORROBORATED] Journal-Fit Reviewer, R3**: length and supplement dependence far beyond the 10-page recommendation (SC-4).
- **[CORROBORATED] Journal-Fit Reviewer, R3**: abstract, §I and §VII numbers that no main-text table carries (SC-5).
- **[CORROBORATED] Journal-Fit Reviewer, R2**: the novelty claim rests partly on an abstract-only search, with no query list and gaps in the tracking and car-following literature (SC-6).
- **[CORROBORATED] Journal-Fit Reviewer, R3**: the abstract is dense with coined terms, and the title's "Lead Braking" overstates the population (SC-7).
- **[CORROBORATED] Journal-Fit Reviewer, R1**: interval types are mixed between the abstract, text and Table II; a point sits at or outside its own interval (SC-9).
- **[CORROBORATED] Journal-Fit Reviewer, R1**: internal file names, labels and a local path appear in the supplement (SC-11).
- **[CORROBORATED] R2, R3**: the room's location and the braking prediction's share rest on a filter whose noise is mis-tuned for the simulated sensor (position NIS 0.24 against 2) (SC-23).
- **[CORROBORATED] R2, R3**: the cross-family carry-over expectation (stopped vehicle, cut-in) rests on whole-run row shares (SC-27). DA-corroborated (m7).
- **[CORROBORATED] R3, R2**: the room, the 83% and the 12% hold for a 2 Hz detector with no latency; no update-rate or latency variation was run (SC-32). DA-corroborated (M4).
- **[SINGLE-REVIEWER] Journal-Fit Reviewer**: no single take-away; as packaged, the contribution is closer to a method note on an expected null (SC-1). DA-corroborated: the DA reports the same sub-claim (C1). The DA is not an independent seat and does not change the count.
- **[SINGLE-REVIEWER] Journal-Fit Reviewer**: notation and hedging load (SC-8).
- **[SINGLE-REVIEWER] Journal-Fit Reviewer**: the abstract, §I and §VII are not parallel; the time-gap 0.314 appears only in §VII; the abstract gives 12% without its range (SC-12).
- **[SINGLE-REVIEWER] R1**: there is no single stated estimand for the tracker covariance's share, no calibrated interval for the placebo contrast or the gridless share, and no equivalence margin; the 2.2-decision figure is a post-hoc maximum over interval ends (SC-14). DA-corroborated (m3).
- **[SINGLE-REVIEWER] R1**: only the scale triple is held out, not the structure; the per-phase schedule is not transferred to the tuning runs (0.632 against 0.893) (SC-16).
- **[SINGLE-REVIEWER] R1**: no untouched confirmatory data remain. The evaluation runs have steered several analysis rounds, yet contribution 3 is called a "confirmation" (SC-17). DA-corroborated (C1, option a).
- **[SINGLE-REVIEWER] R1**: the 2.2-decision statement is worded differently in the Abstract, §I and §VII, and is not scoring-qualified (5.3 decisions under a 2 m gap) (SC-18). DA-corroborated (m4).
- **[SINGLE-REVIEWER] R1**: verification is independent of code only; the S11 intervals rest on one program (SC-20). DA-corroborated (m3).
- **[SINGLE-REVIEWER] R1**: the caution window is not varied, and the caution definition's denominator changes with the source (SC-21). DA-corroborated: DA M8 rates the caution definition MAJOR and m1 rates the window MINOR; R1 rates both Minor (severities shown side by side; the DA is not one of the four).
- **[SINGLE-REVIEWER] R1**: Table II prints shares for populations the paper says do not grade (SC-22).
- **[SINGLE-REVIEWER] R2**: the after-stop mechanism explains 9% of the room; staleness and filter smoothing are not separated; there is no run-level breakdown of the 132 decisions (SC-25).
- **[SINGLE-REVIEWER] R2**: the heading explanation of the ratio exceptions is untested; benign driving (60.45%) and the S10.7 run are unexplained (SC-26).
- **[SINGLE-REVIEWER] R2**: the NIS/NEES summaries are dominated by population mix, computed at decision time, and given without intervals (SC-28).
- **[SINGLE-REVIEWER] R2**: the "435.2 decision-equivalents" figure in §V-C has no supporting table (SC-29). DA-corroborated (m2).
- **[SINGLE-REVIEWER] R3**: the 12% assumes a perfect, free stop that does not depend on the perception under study (SC-30). DA-corroborated (M7).
- **[SINGLE-REVIEWER] R3**: the 6 m/s² stop exceeds every lead's realised deceleration (2.09–5.46 m/s²) (SC-31).
- **[SINGLE-REVIEWER] R3**: the braking prediction's cost behind a lead that does not brake is unmeasured; no non-braking runs exist (SC-33). DA-corroborated (M6).
- **[SINGLE-REVIEWER] R3**: results are per decision only, with no event-level or severity outcome (SC-34). DA-corroborated (m6).
- **[SINGLE-REVIEWER] R3**: the sentence "does not justify removing a covariance margin" appears only in §VI (SC-35).
- **[SINGLE-REVIEWER] R3**: the regulation parameters come from an ALKS motorway model; Supplement S3 drifts toward compliance wording; a proposal document is cited (SC-36).
- **[SINGLE-REVIEWER] R3**: the time-gap baseline was added post hoc and acts as a competitor; there is no TG+N arm (SC-37).
- **[SINGLE-REVIEWER] R3**: the closed-loop check's R157-unit gap figures can be over-read (SC-38).
- **[SINGLE-REVIEWER] R3**: the phase schedule's 99.9% could be read as a design recommendation (SC-39).
- **[SINGLE-REVIEWER] R3**: ACC/AEB standards and test protocols are not engaged (SC-40).

#### Points of Disagreement
Every split below is arbitrated by the editor on evidence first and expertise second. The author receives the arbitrated recommendation.

- **Whether the positive control shows that the null is not a blunt measure (SC-13)**
  - R1 (W1, Major) and R2 (W1, Major) argue that it does not. The mixture oracles grade only pooled and after the stop, where the room is largely a between-phase allocation. They are also far larger in amplitude than the tracker's 2–5% variation.
  - The Journal-Fit Reviewer (S1) and R3 (S1) list the positive control as a strength that makes the null interpretable.
  - **Editor's Resolution: R1 and R2 upheld, Major, must fix.**
    - Evidence: §IV-B itself limits grading to "Pooled and after the stop" and then concludes "the null of Section V-A is not a blunt measure". Phase-weighted and before the stop, the mixtures score below the class average (DA's reading of Tables S12 and S38: −0.383, −0.266, 0.266 phase-weighted; −0.365, −0.258, 0.232 before the stop). §V-C attributes 89% of the pooled room to one scale per phase.
    - Expertise: detectability of a positive control is the methodology seat's core competence.
    - The two strengths are not wrong: the control exists and its failures are disclosed. They do not engage with the amplitude or the phase-weighted result.
- **Severity of the held-out per-phase figures in the abstract, 90% and 99.9% (SC-15)**
  - R1 (W3, Major) and the Journal-Fit Reviewer (W4, Major) object to three things: the favourable like-for-like baseline (0.868 and 0.964 against the frontier of record), no interval for the estimated-phase values, and false precision.
  - R2 (W7, Minor) agrees on the baseline, but holds that the allocation message survives either denominator.
  - **Editor's Resolution: Major, must fix.**
    - Evidence: Table S32 confirms 0.903 and 0.999 like for like against 0.868 and 0.964 against record, with no interval for the estimated-phase values. The 0.999 held out exceeds the 0.984 in sample, which shows a baseline effect. The figure is in the abstract and contribution 2.
    - Expertise: held-out inference is R1's remit.
    - R2's point is accepted: the fix is reporting and labelling, not withdrawing the allocation finding.
- **Whether "only comparisons between sources on the same decisions are meant to transfer" is supported (SC-19)**
  - R3 (W4, Major) and R1 (W7, Minor) agree that Table S35 contradicts it: RR(CK3) is 0.377 against 0.831, and RR(AM) in the lead-stopped phase is 0.063 against 0.702. They differ on severity.
  - **Editor's Resolution: Major, must fix.**
    - Evidence: the sentence is the paper's safeguard for every transferred statement, including the 83% in the abstract. Table S35 shows source shares, not only magnitudes, moving several-fold.
    - Expertise: open-loop versus closed-loop transfer is R3's core competence.
    - The repair can be a narrower sentence plus tuning-run intervals; a third recording policy is optional.
- **Severity of the braking prediction's missing scenario condition in the abstract (SC-24)**
  - R3 (W5, Major) and R2 (W3, Minor) agree that the abstract's 83% omits that every lead brakes to a stop and that the prediction's cost behind a non-braking lead is untested. They differ on severity.
  - **Editor's Resolution: must fix, at the level of the abstract and contribution wording.**
    - The 83% is the abstract's main positive number. A reader stopping at the abstract would take it as a property of the predictor.
    - New non-braking-lead runs (R3's further request) are carried as a suggested item (SC-33), not a requirement.
- **Severity of the dependence of the pooled magnitudes on population and recording length (SC-3)**
  - The Journal-Fit Reviewer (W2, Major) holds that the abstract presents magnitudes the paper says do not transfer.
  - R1 (W6, Minor) and R3 (W6, Minor) hold that the dependence is disclosed.
  - **Editor's Resolution: Minor, should fix.**
    - Evidence: the abstract already states that 83% of the 8,290 decisions follow the lead's stop, and its last sentence asks open-loop scores to state population and recording policy. The body gives R without the after-stop decisions (8.58 pp) and per phase.
    - What is missing is one clause saying that the pooled 5.6 pp and 83% scale with recording length.
    - The Journal-Fit Reviewer's dissent is recorded. The related main-text-table requirement (SC-5, R4 below) carries the decision-bearing part.
- **Whether the revision-history and AI disclosure is plainly worded (SC-10)**
  - The Journal-Fit Reviewer (W9), R1 (W9) and R2 (Minor Issues) find the wording inconsistent. "External pre-submission review" (Supplement S10 introduction) and "an independent reviewer" (Table S13 footnote; S4 status paragraph) can be read as human or independent review.
  - R3 (S7) calls the disclosure complete and plainly worded.
  - **Editor's Resolution: upheld, Minor, should fix.** The two quoted phrases are in the supplement as cited. R3's point that the substance is complete is accepted; the defect is wording.

### Devil's Advocate CRITICAL adjudication

`da_critical_adjudications: [C1=VALIDATED]`

**C1: the confirmatory content is fixed by construction, and the non-trivial contributions are exploratory and unstable across the two run sets.**

- **The DA's argument.** The only confirmatory result is the null for the tracker covariance. The paper says the null is expected from the Riccati steady state, and the ratio check shows it without ground truth. Everything with discriminating content is declared exploratory in §IV-D: the room's location, per-phase scheduling, the 12%, the time gap, and "what an open-loop score depends on". Its key magnitudes differ between the only two run sets (room 1.18 against 5.56 pp; CK3 0.377 against 0.831). Repairable only by (a) a confirmatory test on fresh runs, or (b) a tracker whose covariance varies.
- **Corroboration by the four seats.**
  - Journal-Fit Reviewer W1 (Major): an expected null with no single take-away.
  - R2 W1 (Major): no covariance-varying arm.
  - R1 W4 (Major): no untouched confirmatory data.
  - R3 W3 and W4 (Major): conditional on the update rate; results move with the recording policy.
- **Assessment: VALIDATED in substance, at a severity the panel judges repairable.** The structure the DA describes is accurate on the paper's own statements. The strong form is not upheld: that a reader "can rely on 'a constant is constant'" and nothing else. Seats credit two parts that transfer:
  - the ground-truth-free ratio check, with its stated reach (Journal-Fit Reviewer S3; R3 S5);
  - the lesson that an open-loop decision score depends on commitment and population (Journal-Fit Reviewer S4; R3 S6).
- **Required author response.** Covered by R1, R2 and R8 of the Revision Roadmap. Do (i), (ii) or (iii), and acknowledge C1 in the response letter:
  - (i) add an arm in which the covariance varies;
  - (ii) run the final locked plan once on fresh runs;
  - (iii) re-centre the paper on the evaluation protocol, with the null as its worked example, and state plainly in the abstract which results are exploratory.

### Decision Rationale

All four card-backed seats recommend Major Revision, and the Devil's Advocate's CRITICAL issue is validated. Under the decision standards, a validated decision-bearing weakness that is repairable gives Major Revision. Accept and Minor Revision are both blocked.

**What the panel finds sound**
- The evaluation is careful.
- The arithmetic holds: R1 recomputed about 15 conversions; the Journal-Fit Reviewer traced every number in the Abstract, §I and §VII; R2 and R3 checked the tables they relied on. No mismatch affects a claim.
- The paper is unusually candid about its exploratory status, its search limits and its verification.

**What blocks acceptance**
- **Reach of the confirmatory result.** A null expected from theory, with no arm that could show the design detects a varying covariance (R2 of the roadmap).
- **The positive control's scope.** It grades between-phase allocation, not within-phase information at the tracker's scale (R5).
- **Status of the quotable numbers.** The held-out per-phase figures, the 83% and the 12% are exploratory, depend on test-bed choices (2 Hz without latency, filter tuning, a stop that out-brakes every lead), and move with the recording policy (R7–R13).

**Fit and length**
- The topic fits the journal.
- The main text of 12,451 words and the supplement of 34,240 words are far beyond the 10-page recommendation (R3).
- About 40 supplement items must be opened to verify the abstract (R4).

None of these is fatal. Several can be met offline from the stored detections: re-tracking with re-tuned noise, a constant-acceleration or IMM tracker, and higher update rates. Others can be met by narrower wording. Reject is not supported, because no seat found a design flaw that invalidates the central null.

### Blocking Issues (immutable source order)

| Transport ref | Blocking issue | Source reviewer(s) | Evidence anchor | Resolving roadmap item |
|---|---|---|---|---|
| R2 | The confirmatory null is expected by construction; no arm uses a covariance that varies, so the design's sensitivity to a realistic covariance is untested | EIC, R2, R3; DA C1 | `text: §V-B "It changes the critical values in only 217 decisions, because it can only inflate and the innovation covariance is already too wide"` | REV-2 |
| R5 | The positive control grades only pooled and after-stop allocation, at amplitudes far above the tracker's variation; "not a blunt measure" is overstated | R1, R2 (SPLIT, arbitrated); DA M1 | `text: §IV-B "the measure therefore grades partial information, and the null of Section V-A is not a blunt measure"` | REV-5 |
| R8 | No untouched confirmatory data; the quotable results are exploratory on runs that steered several analysis rounds | R1; DA C1 | `text: §III-A "for them these runs are a transfer to another planner setting, not a replication"` | REV-8 |

---

## Part 2: Revision Roadmap

`schema_version: revision-roadmap/1.1` (rendered as Markdown; the JSON emitter script is not installed). Items are in source order: the first raising seat in the order EIC, R1, R2, R3, then by finding number. `R<n>` and `S<n>` are transport references, not ranks.

### Required Revisions (Must Fix)

| Ref | Revision item | Sub-claim(s) | Severity | Evidence anchor | Conf. | Source | Obligation | Cost scope | Consequence |
|---|---|---|---|---|---|---|---|---|---|
| R1 | State one take-away and lead with it. Re-centre the paper on the evaluation protocol and what an open-loop decision score depends on, with the tracker null as its worked example, and do not present exploratory results as co-equal claims. | SC-1 | major | `text: §I "so a null is expected; we measure it at decision level and size it"` | 4 | EIC (W1); DA C1 | must_fix | section: Abstract, §I contributions, §VII | acceptance_criterion_unmet → claim: significance for a regular paper |
| R2 | Add one arm whose covariance varies with the lead's motion: CV/CA IMM, or a fading-memory or innovation-adaptive Q on the velocity block, re-run offline on the stored detections; or a family where the ratio varies, such as crossings or track births. Otherwise rename NA "output-scalar NIS inflation", change the §V-B heading and the Table I label, and state in the abstract and contributions that no covariance-varying tracker was tested. | SC-2 | major | `text: §V-B "It changes the critical values in only 217 decisions, because it can only inflate and the innovation covariance is already too wide"` | 4 | EIC (W1), R2 (W1), R3 (W3); DA C1 | must_fix | re_analysis: offline re-tracking; §V-B; Table I | claim_scope_unsupported → claim: "Tracker-Covariance Safety Margins" (title), contribution 3 |
| R3 | Bring the main text toward the 10-page recommendation. Move interval mechanics, resolution rules, hash strings, the 2 m gap paragraph and most decision-equivalent detail to the supplement. Cut the supplement to what the main text needs; remove S3 and S9 unless used. Give a typeset page count. | SC-4 | major | `dataset: PACKAGE_MANIFEST_v12.txt — whole manuscript 12451 words; supplement 34240 words` | 4 | EIC (W3); R3 (Minor Issues) | must_fix | section: whole manuscript and supplement | editorial_conformance_unmet → manuscript |
| R4 | Every number in the Abstract, §I and §VII must be carried by a main-text table, or leave those texts. Applies to the per-phase and held-out shares, the calibrated room interval, the 2.2-decision figure, the 83% after-stop decision share and the 12% range. One option is a main-text table of the exploratory per-phase results, labelled exploratory. | SC-5 | major | `absence: Tables II–V — expected the held-out per-phase shares (0.90 and 0.999), the 2.2-decision bound and the calibrated room interval that the Abstract states; checked Tables I–V, Fig. 3 caption and §V-A and §V-C text` | 4 | EIC (W4); R3 (Minor Issues) | must_fix | section: Abstract, §I, §VII, §V tables | reader_traceability_reduced → section: Abstract |
| R5 | Limit "not a blunt measure" to where the control grades: pooled and after the stop. Add one test of the measure at the tracker's scale, either an oracle rank-matched to the realised error but compressed into the observed N/F0 ratio range (about ±5%), or the graded-oracle check repeated on the per-phase-scale frontier (remaining room 0.95 pp). State the criterion for "grades" before computing it. | SC-13 | major | `text: §IV-B "the measure therefore grades partial information, and the null of Section V-A is not a blunt measure"` | 4 | R1 (W1), R2 (W1); SPLIT vs EIC S1, R3 S1, arbitrated; DA M1 | must_fix | re_analysis: §IV-B, §V-A, Tables S12, S38 | evidence_gap_remains → claim: §IV-B "not a blunt measure" |
| R6 | Name one estimand for the tracker covariance's share before any interval: the gridless or a smoothed frontier. Give one calibrated interval for it and for the N-minus-placebo contrast. Fix an equivalence margin from stakes and report against it. Present the 2.2-decision figure as a descriptive range of interval ends, not a bound. | SC-14 | major | `table: Table S31c — largest absolute end 2.16 decisions (Table S17, subsampling m = 25); Table S30 — grid RR(N) − RR(P) −0.0003 [−0.0009, 0.0001], gridless D(N) −0.19 [−0.34, 0.02]` | 4 | R1 (W2); DA m3 | must_fix | re_analysis: §IV-B, §V-A, Tables S16, S30–S31c | evidence_gap_remains → claim: contribution 3 and Abstract 2.2 statement |
| R7 | Report the held-out per-phase results against the single-scale frontier of record (0.868; 0.964), or state the basis wherever 0.90 and 0.999 appear. Give intervals for every held-out value, including the estimated phase. Drop the third significant figure, and label the values exploratory in the abstract. | SC-15 | major | `table: Table S32 — logged truth: in sample 0.893, LOO like-for-like 0.903, five-fold 0.885 [0.81, 1.00], against single scale of record 0.868; estimated phase −1.0: 0.984, 0.999, 0.964` | 4 | R1 (W3), EIC (W4), R2 (W7); SPLIT on severity, arbitrated Major | must_fix | section: Abstract, §I, §V-C, Table S32 | claim_scope_unsupported → claim: Abstract "90% … and 99.9%" |
| R8 | Make the confirmatory status plain. Replace "confirmation" in contribution 3, and say in the abstract that the tracker-versus-class-average difference was viewed on the evaluation runs before the plan, and which results are exploratory. Preferably, generate fresh runs (new seeds, same generator) and run the final locked plan once, with the R6 estimand, the R7 schedule and phase estimator fixed in advance. Otherwise, at least apply the evaluation-chosen schedule to the tuning runs (and the reverse) as a transfer test, or remove the allocation claim from the headline. | SC-16, SC-17 | major | `text: §III-A "for them these runs are a transfer to another planner setting, not a replication"` | 4 | R1 (W3, W4); DA C1 | must_fix | new_data: fresh evaluation runs; or re_analysis: tuning-run transfer; section: Abstract, §I | evidence_gap_remains → claim: contributions 2 and 3 |
| R9 | Restrict "only comparisons between sources on the same decisions are meant to transfer" to what both run sets support: the null for N, and any ordering that holds in both. Compute tuning-run intervals (Table S2 footnote says none were computed). Optional: a third recording policy, such as a time-gap or ACC-style recorder. | SC-19 | major | `table: Table S35 — Room R all 1.18 vs 5.56 pp; RR(CK3) all 0.377 vs 0.831; RR(AM) lead stopped 0.063 vs 0.702` | 4 | R3 (W4), R1 (W7); SPLIT on severity, arbitrated Major; DA M5 | must_fix | re_analysis: tuning-run intervals; section: §VI Limits, Abstract last sentence | claim_scope_unsupported → claim: §VI "only comparisons between sources … are meant to transfer" |
| R10 | Re-run the tracker offline on the stored detections, once with noise set so that position NIS is near 2 and once with a CA or IMM variant. Report the after-stop lag (Table S34), the room by phase (Table S33) and the braking prediction's share. Otherwise add filter tuning to the Limits list of conditions and to the abstract's conditions on the 83%. | SC-23 | major | `text: §III-A "the simulated sensor data are a likely reason, which we did not test"` | 3 | R2 (W2); R3 (W3) | must_fix | re_analysis: offline re-tracking; §III-A, §V-C, §VI Limits | evidence_gap_remains → claim: contribution 2 (velocity lag) and Abstract 83% |
| R11 | In the abstract and contribution 2, state that the 83% is measured on runs in which every lead brakes to a stop and that its cost behind a lead that does not brake is untested. | SC-24 | major (arbitrated; R2 Minor, R3 Major) | `text: §VI "The share is an open-loop, off-policy quantity on runs in which the lead always brakes"` | 4 | R2 (W3), R3 (W5); SPLIT on severity, arbitrated; DA M6 | must_fix | sentence: Abstract; §I contribution 2 | claim_scope_unsupported → claim: Abstract "recovers 83% of the room" |
| R12 | Qualify the 12% with its two assumptions. (a) The stop is perfect, free and independent of the perception under study; state this in the abstract, and preferably add a scoring in which the stop starts from the tracker's own belief or after a stated delay distribution. (b) The 6 m/s² stop exceeds every lead's realised deceleration (2.09–5.46 m/s²); report the reaction-and-stop room by terciles of the lead's deceleration, or restrict the wording to leads braking at up to 5.5 m/s². | SC-30, SC-31 | major | `text: §VI "the reading assumes that the stop always comes"`; `table: Table S28 — realised lead deceleration 2.09–5.46 m/s² (evaluation runs), against the 6 m/s² stop of Table III` | 4 | R3 (W1, W2); DA M7 | must_fix | re_analysis: Table III by lead deceleration; sentence: Abstract | claim_scope_unsupported → claim: Abstract "leaves 12% of it" |
| R13 | Re-run the detector and tracker on the 20 Hz recordings at 5 and 10 Hz with a stated latency, and report R, the after-stop room and the braking prediction's share at each rate. Otherwise state in the abstract that all magnitudes hold for a 2 Hz detector with 0.5 s tracker steps and no latency. | SC-32 | major | `text: §III-A "run at 2 Hz, with no latency simulated"` | 4 | R3 (W3); R2 (summary); DA M4 | must_fix | re_analysis: offline re-detection and re-tracking; or sentence: Abstract | claim_scope_unsupported → claim: Abstract 5.6 pp, 83%, 12% |

### Suggested Revisions (Should Fix / Consider)

| Ref | Revision item | Sub-claim(s) | Severity | Evidence anchor | Conf. | Source | Obligation | Cost scope | Consequence |
|---|---|---|---|---|---|---|---|---|---|
| S1 | Add one clause to the abstract: the pooled 5.6 pp and 83% scale with recording length after the stop (8.58 pp without the after-stop decisions). Consider making per-phase results the primary table. | SC-3 | minor (arbitrated; EIC Major dissent recorded) | `text: §I Scope "so pooled figures are dominated by stationary decisions"` | 4 | EIC (W2), R1 (W6), R3 (W6); DA M3 | should_fix | sentence: Abstract | interpretive_ambiguity_remains → claim: Abstract 5.6 pp |
| S2 | List the queries and engines in S6. Read the full texts of the ITS threat-assessment items, or restate the finding as an abstract-level observation. Add the missing tracking and car-following references (motion-model comparisons, IMM survey, estimator credibility, anticipation in car following, conformal planning; to be verified). | SC-6 | minor | `text: §II "In the abstracts of this literature that we read (we did not read the full texts), we found no evaluation"` | 3 | EIC (W5), R2 (W6) | should_fix | section: §II, S6, references | claim_scope_unsupported → claim: §II novelty statement |
| S3 | Make the abstract readable for a general ITS reader: three results, one defining sentence for "room" and "wrong go", fewer numerals. Consider a title that names the tested object rather than "Lead Braking". | SC-7 | minor | `text: Abstract "does no better than a placebo that only shifts the class-average margin on the scale grid"` | 4 | EIC (W6); R3 (Minor Issues) | should_fix | section: Abstract, title | reader_traceability_reduced → section: Abstract |
| S4 | Reduce notation and repeated hedges. State each fence once in Scope and once in Limits, and use established terms in running text. | SC-8 | minor | `table: Notation table (§IV) and Table I — nine defined terms and eight source codes before the first result` | 4 | EIC (W7) | consider | section: §IV–§VII | reader_traceability_reduced → manuscript |
| S5 | Use one labelled interval type per quantity: print calibrated intervals in Table II for R and RR(N). Note on Fig. 2(a) that N's mean lies outside its interval. Label the held-out baselines wherever 0.90, 0.88 and 0.87 appear. | SC-9 | minor | `table: Table II, column "All", rows Room R and RR(N) — 5.56 [4.50, 6.60] and 0.0012 [−0.0011, 0.0012]` | 4 | EIC (W8), R1 (W8) | should_fix | section: Table II, Fig. 2, §V-C | reporting_requirement_unmet → table: Table II |
| S6 | Write one provenance paragraph in the main text. Say that both earlier reviews were by AI panels, which analyses were added in response, and that the second programs and recounts were AI sessions sharing code and arrays. Replace "external" and "independent reviewer" accordingly. | SC-10 | minor | `text: §IV-D "After two pre-submission reviews by an AI-based review panel"; Supplement S10 "added after an external pre-submission review of an earlier draft"` | 4 | EIC (W9), R1 (W9), R2 (Minor Issues); SPLIT vs R3 S7, arbitrated | should_fix | section: §IV-D, S4, S10, S11, Table S13 footnote | interpretive_ambiguity_remains → section: §IV-D |
| S7 | Remove or define internal identifiers in the supplement, such as "A4 extraction", "A9-3", the local path `recount_v12\RECOUNT_COMPARE_A93_v02.md`, `derive_v03.py`, and captions that refer to "the earlier draft". | SC-11 | minor | `text: S11.4 and S11.8 internal labels ("A4 extraction", "A9-3") and a local file path` | 4 | EIC (W9), R1 (W9, Minor Issues) | should_fix | section: Supplement S11, Fig. S4, Table S29 captions | editorial_conformance_unmet → section: Supplement |
| S8 | Make the Abstract, §I and §VII state the same claims in the same order. Give the 12% with its range (0.29 to 0.06 across 4 to 7.6 m/s²). Add the time-gap result to the abstract or drop it from §VII. Split §VII into findings and next steps. | SC-12 | minor | `text: §VII "a time-gap margin on the ego's speed recovers 0.314 of it"; Abstract "leaves 12% of it"` | 4 | EIC (W10) | should_fix | section: Abstract, §I, §VII | interpretive_ambiguity_remains → section: §VII |
| S9 | Use one wording for the 2.2-decision statement everywhere, with its scoring, population and post-hoc status. | SC-18 | minor | `text: §VII "its frontier stays within 2.2 of 8,290 decisions of the class average's under every interval method we used"` | 4 | R1 (W5); DA m4 | should_fix | sentence: Abstract, §I, §VII | interpretive_ambiguity_remains → claim: 2.2 statement |
| S10 | Add a hand-checkable subset: a few decisions whose true clearance is computed by a routine independent of the scoring library. Have the N-share intervals recomputed by a second program. | SC-20 | minor | `text: S10.9 "so this agreement covers the extension, the truth window, the flags and the counting, not those shared functions"` | 3 | R1 (W9); DA m3 | should_fix | re_analysis: S10.9, S11.8 | method_reproducibility_unresolved → section: S10.9, S11.8 |
| S11 | Report R and the shares under caution windows up to 5%, 10% and 15%. Argue for the of-record caution definition against the signed one, or report both in the main text. | SC-21 | minor (R1); DA M8 rates the definition MAJOR | `text: §IV-B "to the smaller of the class average's and the oracle's largest caution"` | 3 | R1 (W10); DA M8, m1 | should_fix | re_analysis: §IV-B, Table S21 | interpretive_ambiguity_remains → claim: room R definition |
| S12 | In Table II, print decision-equivalents rather than shares for populations that the paper says do not grade. | SC-22 | minor | `text: §IV-B "to the smaller of the class average's and the oracle's largest caution"` (W10 parent) | 3 | R1 (W10) | should_fix | section: Table II | reader_traceability_reduced → table: Table II |
| S13 | Give a run-level breakdown of the 132 after-stop decisions. Separate staleness from filter smoothing, for example by scoring on the state at its own timestamp. Give intervals for Tables S33, S33b and S34. | SC-25 | minor | `text: §VI "The share is an open-loop, off-policy quantity on runs in which the lead always brakes"` | 4 | R2 (W3) | should_fix | re_analysis: Tables S33–S34 | evidence_gap_remains → claim: §V-C after-stop mechanism |
| S14 | Tabulate the ratio's spread against heading offset and track age for the crossing and benign families. Explain benign driving at 60.45% and the S10.7 run (ratios 0.703–1.043). Report the share of decisions whose first-feasible row would change under a ±5% change in the ratio. | SC-26 | minor | `text: §V-E "so the ratio can vary with a crossing actor's heading alone, without carrying information about the error"` | 4 | R2 (W4) | should_fix | re_analysis: Table V, S10.7 | evidence_gap_remains → claim: contribution 4 |
| S15 | Support the carry-over expectation with ratios in a window around the cut-in event and by track age, or drop cut-in from the expected-carry-over list. | SC-27 | minor | `table: Table V — Cut-in 20 runs, 90,227 rows, 99.86% within 5% of the median 1.102` | 3 | R3 (W12), R2 (W4); DA m7 | should_fix | re_analysis: Table V; or sentence: contribution 4 | claim_scope_unsupported → claim: contribution 4 carry-over |
| S16 | Give NIS and NEES per phase at update time, with run-level intervals and the truth at the state time. Phrase the "opposite of nuScenes" remark as applying to stationary decisions. | SC-28 | minor | `table: Table S34b — Lead braking: 150 updates, mean NIS 1.47, mean velocity NEES 5.08 (755 decisions); After stop: 1,383 updates, mean NIS 0.10` | 4 | R2 (W5) | should_fix | re_analysis: Table S34b, Fig. S1 | interpretive_ambiguity_remains → claim: §III-A consistency statement |
| S17 | Add the table row behind "435.2 decision-equivalents with a tracker speed above 2 m/s" (§V-C), with the complementary pre-stop subtotal. The pre-stop total in Table S33 is 419.1. Decision-equivalent subtotals can be negative, so a reader cannot tell whether this is a partition or a typo. | SC-29 | minor [SEVERITY-SOURCE: letter-fallback] | `absence: Supplement Tables S33, S33b and S34 — expected a decision-equivalent figure of 435.2 split by tracker speed above 2 m/s; checked Sections S11.4, S11.9 and Tables S33 to S34b` | 3 | R2 (Detailed Comments, Q7) [CONFIDENCE-SOURCE: report-level for R2 is 4; DA row 3]; DA m2 | should_fix | sentence: §V-C; table: S33 | reader_traceability_reduced → claim: §V-C 435.2 |
| S18 | Add lead-following runs without a hard brake (constant speed, mild braking, stop and pull away) and report wrong goes and caution for the braking prediction and the phase schedule. | SC-33 | major (R3 W5 parent; obligation set by the SC-24 arbitration) | `text: §VI "behind a lead that does not brake, its cost is untested"` | 4 | R3 (W5); DA M6 | should_fix | new_data: non-braking-lead runs | evidence_gap_remains → claim: braking prediction's cost |
| S19 | Add one event-level table: runs with contact, and impact speed where there is contact, for F0, N, CK3 and TG at two matched caution levels. | SC-34 | minor | `text: §VI Limits "Wrong-go counts ignore impact speed."` | 4 | R3 (W6); DA m6 | consider | re_analysis: new table | interpretive_ambiguity_remains → claim: room R as a safety quantity |
| S20 | Add to the abstract and §VII that the null concerns a fixed-noise tracker in steady lead following and does not justify removing a covariance margin; crossing actors, young tracks and other road users are not covered. | SC-35 | minor | `absence: Abstract and Section VII — expected the sentence that the null does not justify removing a covariance margin; checked Abstract, Section I Scope, Section VII, Section VI first paragraph` | 5 | R3 (W7) | should_fix | sentence: Abstract, §VII | claim_scope_unsupported → claim: Abstract null sentence |
| S21 | Cite the adopted R157 text and its amendment status. Remove compliance-sounding sentences from S3. Relate the 6 m/s² stop to AEB and ACC deceleration envelopes. | SC-36 | minor | `text: §VI Limits "nominal reference parameters, read in the text adopted in June 2022 [42]"` | 4 | R3 (W8) | should_fix | section: S3, §IV-C, reference [42] | interpretive_ambiguity_remains → section: Supplement S3 |
| S22 | Add a TG+N and a TG+F0 arm, and state the time-gap policy's headway range against ACC practice. | SC-37 | minor | `text: §III-C "was defined in Amendment 09 (Section IV-D) and computed on the evaluation runs only"` | 3 | R3 (W9) | consider | re_analysis: new arms | evidence_gap_remains → claim: time-gap comparison |
| S23 | Put the fallback share into the quoted closed-loop statement, or drop the R157-unit statement from the supplement summary. | SC-38 | minor | `text: S3.4 "corresponds to a starting gap on average 0.021 s above the R157 minimum"` | 3 | R3 (W10) | consider | sentence: S3.4 | interpretive_ambiguity_remains → section: Supplement S3 |
| S24 | Present the phase schedule as a diagnostic of where the room lies, and say that it is not a design result until tested on pull-away and gentle-brake runs. | SC-39 | minor | `table: Table S32 — tracker-estimate phase labels, threshold −1.0 m/s²: in sample 0.984, held out like for like 0.999, against the single scale of record 0.964; agreement with truth 95.6%` | 4 | R3 (W11) | should_fix | sentence: Abstract, §V-C, §VII | claim_scope_unsupported → claim: per-phase schedule |
| S25 | Relate the time gap, the stop deceleration and the lead decelerations to ACC and AEB standards and test protocols (ISO 15622, ISO 22179, UN R152, IEEE 2846; to be verified). | SC-40 | minor | `absence: Section II and the reference list — expected ACC and AEB performance standards and test protocols (for example ISO 15622, ISO 22179, UN R152, IEEE 2846); checked Section II, references [1]-[58], Supplement S6` | 4 | R3 (W13) | should_fix | section: §II, references | claim_scope_unsupported → section: §II |

Counts: **13 required (must_fix)**; **25 suggested** (21 should_fix, 4 consider).

### Source-Traceability Checklist
- [ ] R1 — must_fix: one take-away; re-centre on the protocol
- [ ] R2 — must_fix: covariance-varying arm, or narrowed framing of NA and the title
- [ ] R3 — must_fix: length toward 10 pages; trim the supplement
- [ ] R4 — must_fix: abstract, §I and §VII numbers carried by main-text tables
- [ ] R5 — must_fix: scope of "not a blunt measure"; a test at the tracker's scale
- [ ] R6 — must_fix: one estimand, a calibrated interval and an equivalence margin for N's share
- [ ] R7 — must_fix: held-out per-phase figures against record, with intervals
- [ ] R8 — must_fix: confirmatory status; fresh runs or a transfer test
- [ ] R9 — must_fix: restrict the transfer sentence; tuning-run intervals
- [ ] R10 — must_fix: filter re-tuning re-run, or a stated condition
- [ ] R11 — must_fix: the 83% condition in the abstract
- [ ] R12 — must_fix: the 12%'s stop assumptions
- [ ] R13 — must_fix: update rate and latency, or a stated condition
- [ ] S1–S25 — should_fix or consider, as listed

### Response Letter Template
Answer every item, R1–R13 and S1–S25, and the DA's C1 point by point. Use `templates/revision_response_template.md`.

---

## Part 3: Reviewer Report Summary

### Journal-Fit Review Report Summary
- Recommendation: Major Revision | Confidence: 4
- Key point: the fit is credible, but as packaged the paper is a method note on an expected null. It is about 15–18 pages against 10 (a seat estimate, not a typeset count), and the abstract leads with numbers that no main-text table carries.

### Reviewer 1 (Methodology) Summary
- Recommendation: Major Revision | Confidence: 4
- Key point: the arithmetic is sound (about 15 conversions recomputed), but:
  - the positive control does not grade at the tracker's scale;
  - the N-share inference has no single calibrated estimand;
  - the held-out figures use a favourable baseline;
  - no untouched confirmatory data remain.

### Reviewer 2 (Domain) Summary
- Recommendation: Major Revision | Confidence: 4
- Key point: the steady-state account is correct and every traced figure reconciles. But no arm has a covariance that varies, and the lag mechanism rests on one mis-tuned filter. Both can be addressed offline from the stored detections.

### Reviewer 3 (Perspective) Summary
- Recommendation: Major Revision | Confidence: 4
- Key point: the null for this tracker is credible. The 12% and 83% hold only for:
  - a 2 Hz detector without latency;
  - leads braking at up to 5.5 m/s²;
  - a perfect, independent stop;
  - one recording policy.

  The removal caution should travel with the headline.

### Devil's Advocate Summary
- Recommendation: N/A (findings only)
- Key challenge: C1, validated. The confirmatory result is fixed by construction, and the discriminating content is exploratory and unstable across the two run sets.

---

## Appendix A: Reviewer Summary Matrix

| Dimension | Journal-Fit Reviewer | R1 (Methodology) | R2 (Domain) | R3 (Practical) |
|---|---|---|---|---|
| Overall recommendation | Major Revision | Major Revision | Major Revision | Major Revision |
| Confidence / scope | 4: fit, novelty, clarity; not statistics or filter theory | 4: resampling and evaluation design; not tracker theory or the deposit | 4: tracking, NIS/NEES, adaptive filtering; not bootstrap or regulation | 4: test bed, regulation, practice; not estimator or bootstrap |
| Key strengths | Positive control; candour; ratio check; commitment lesson; provenance and legible figures | Perfect and graded oracles; measured interval validity; placebo, jitter, gridless; ratio check; disclosure; sensitivity analyses | Steady-state account; placebo; disclosed control failures; deviation check; lead-state table; narrow wording; disclosure; departures reported | Positive control; plain limits; stop reliance counted; no-compliance register; ratio check; actionable commitment statement; disclosure |
| Weaknesses (→ Appendix B) | 4 Major, 6 Minor | 4 Major, 6 Minor | 2 Major, 5 Minor | 5 Major, 8 Minor |
| Questions | 6 | 7 | 7 | 4 |
| Minor Issues (non-finding) | 9 | 9 | 10 | 8 |

## Appendix B: Weakness Sub-Claim Inventory (Step 1b)

Positions: raised, corroborated, disputed or not-mentioned. Severity and confidence are transported from the seat's finding; DA rows never count.

| SC | Parent weakness | EIC | R1 | R2 | R3 | DA row | Disposition |
|---|---|---|---|---|---|---|---|
| SC-1 | EIC W1: no single take-away | raised (Major, 4) | n-m | n-m | n-m | C1 (CRITICAL, 3) | SINGLE-REVIEWER, DA-corroborated |
| SC-2 | EIC W1 / R2 W1: no covariance-varying arm; NA framed as adaptive | raised (Major, 4) | n-m | raised (Major, 4) | corroborated (W3, Major, 4) | C1 | CONSENSUS-3 (R1 silent) |
| SC-3 | EIC W2: pooled magnitudes conditional on population and recording length | raised (Major, 4) | raised (W6, Minor, 4) | n-m | raised (W6, Minor, 4) | M3 (MAJOR, 4) | SPLIT (severity), arbitrated Minor |
| SC-4 | EIC W3: length and supplement dependence | raised (Major, 4) | n-m | n-m | corroborated (Minor Issues) | Observation | CORROBORATED |
| SC-5 | EIC W4: abstract numbers not in main-text tables | raised (Major, 4) | n-m | n-m | corroborated (Minor Issues: S28, S36 deserve main text) | — | CORROBORATED |
| SC-6 | EIC W5 / R2 W6: novelty search, missing references | raised (Minor, 3) | n-m | raised (Minor, 3) | n-m | — | CORROBORATED |
| SC-7 | EIC W6: abstract density, title | raised (Minor, 4) | n-m | n-m | corroborated (Minor Issues) | — | CORROBORATED |
| SC-8 | EIC W7: notation and hedging | raised (Minor, 4) | n-m | n-m | n-m | — | SINGLE-REVIEWER |
| SC-9 | EIC W8 / R1 W8: interval types | raised (Minor, 4) | raised (Minor, 4) | n-m | n-m | — | CORROBORATED |
| SC-10 | EIC W9: disclosure wording | raised (Minor, 4) | corroborated (W9) | corroborated (Minor Issues) | disputed (S7) | — | SPLIT, upheld Minor |
| SC-11 | EIC W9 / R1 W9: internal identifiers | raised (Minor, 4) | raised (Minor, 3) | n-m | n-m | — | CORROBORATED |
| SC-12 | EIC W10: abstract, §I and §VII not parallel | raised (Minor, 4) | n-m | n-m | n-m | — | SINGLE-REVIEWER |
| SC-13 | R1 W1: positive control scope and amplitude | disputed (S1) | raised (Major, 4) | corroborated (W1, Major, 4) | disputed (S1) | M1 (MAJOR, 4) | SPLIT, upheld Major |
| SC-14 | R1 W2: N-share estimand and calibration | n-m | raised (Major, 4) | n-m | n-m | m3 (MINOR, 4) | SINGLE-REVIEWER, DA-corroborated |
| SC-15 | R1 W3: held-out figures, baseline and intervals | raised (W4, Major, 4) | raised (Major, 4) | raised (W7, Minor, 4) | n-m | M2 (MAJOR, 4) | SPLIT (severity), arbitrated Major |
| SC-16 | R1 W3: structure not held out; tuning-run transfer | n-m | raised (Major, 4) | n-m | n-m | M5 (MAJOR, 4) | SINGLE-REVIEWER, DA-corroborated |
| SC-17 | R1 W4: no untouched confirmatory data; "confirmation" | n-m | raised (Major, 4) | n-m | n-m | C1 | SINGLE-REVIEWER, DA-corroborated |
| SC-18 | R1 W5: 2.2 wording | n-m | raised (Minor, 4) | n-m | n-m | m4 (MINOR, 4) | SINGLE-REVIEWER, DA-corroborated |
| SC-19 | R1 W7 / R3 W4: transfer sentence vs Table S35 | n-m | raised (Minor, 4) | n-m | raised (Major, 4) | M5 | SPLIT (severity), arbitrated Major |
| SC-20 | R1 W9: verification common-mode | n-m | raised (Minor, 3) | n-m | n-m | m3 | SINGLE-REVIEWER, DA-corroborated |
| SC-21 | R1 W10: caution window and definition | n-m | raised (Minor, 3) | n-m | n-m | M8 (MAJOR, 4), m1 (MINOR, 3) | SINGLE-REVIEWER, DA-corroborated |
| SC-22 | R1 W10: shares in non-grading populations | n-m | raised (Minor, 3) | n-m | n-m | — | SINGLE-REVIEWER |
| SC-23 | R2 W2: filter mis-tuned; lag depends on tuning | n-m | n-m | raised (Major, 3) | corroborated (W3, Major, 4) | — | CORROBORATED |
| SC-24 | R2 W3 / R3 W5: abstract omits the condition on the 83% | n-m | n-m | raised (Minor, 4) | raised (Major, 4) | M6 (MAJOR, 4) | SPLIT (severity), arbitrated must_fix |
| SC-25 | R2 W3: after-stop reach; staleness vs smoothing | n-m | n-m | raised (Minor, 4) | n-m | — | SINGLE-REVIEWER |
| SC-26 | R2 W4: ratio exceptions untested | n-m | n-m | raised (Minor, 4) | n-m | — | SINGLE-REVIEWER |
| SC-27 | R3 W12 / R2 W4: carry-over on whole-run row shares | n-m | n-m | raised (Minor, 4) | raised (Minor, 3) | m7 (MINOR, 3) | CORROBORATED |
| SC-28 | R2 W5: NIS/NEES summaries | n-m | n-m | raised (Minor, 4) | n-m | — | SINGLE-REVIEWER |
| SC-29 | R2 Detailed Comments: 435.2 untraceable | n-m | n-m | raised (no tag; letter-fallback Minor) | n-m | m2 (MINOR, 3) | SINGLE-REVIEWER, DA-corroborated |
| SC-30 | R3 W1: perfect, independent stop | n-m | n-m | n-m | raised (Major, 4) | M7 (MAJOR, 4) | SINGLE-REVIEWER, DA-corroborated |
| SC-31 | R3 W2: stop deceleration above every lead's | n-m | n-m | n-m | raised (Major, 3) | — | SINGLE-REVIEWER |
| SC-32 | R3 W3: update rate and latency | n-m | n-m | corroborated (summary) | raised (Major, 4) | M4 (MAJOR, 4) | CORROBORATED |
| SC-33 | R3 W5: braking prediction's cost; non-braking runs | n-m | n-m | n-m | raised (Major, 4) | M6 | SINGLE-REVIEWER, DA-corroborated |
| SC-34 | R3 W6: no event-level or severity outcome | n-m | n-m | n-m | raised (Minor, 4) | m6 (MINOR, 3) | SINGLE-REVIEWER, DA-corroborated |
| SC-35 | R3 W7: removal caution only in §VI | n-m | n-m | n-m | raised (Minor, 5) | — | SINGLE-REVIEWER |
| SC-36 | R3 W8: regulation parameters and S3 wording | n-m | n-m | n-m | raised (Minor, 4) | — | SINGLE-REVIEWER |
| SC-37 | R3 W9: TG post hoc; no TG+N arm | n-m | n-m | n-m | raised (Minor, 3) | — | SINGLE-REVIEWER |
| SC-38 | R3 W10: closed-loop R157 figures | n-m | n-m | n-m | raised (Minor, 3) | — | SINGLE-REVIEWER |
| SC-39 | R3 W11: phase schedule as a design reading | n-m | n-m | n-m | raised (Minor, 4) | — | SINGLE-REVIEWER |
| SC-40 | R3 W13: ACC/AEB standards | n-m | n-m | n-m | raised (Minor, 4) | — | SINGLE-REVIEWER |

n-m = not-mentioned (silence, not opposition). Every non-DA weakness appears in the table. The Minor Issues channel enters only as corroboration and creates no sub-claim.

## Appendix C: Claim-to-table trace (from the seat reports)

| Claim (Abstract, §I, §VII) | Carried by | Checked by | Status |
|---|---|---|---|
| 248 words, under the 250 limit | Abstract | EIC (own count) | holds |
| 83% of 8,290 decisions follow the stop | Scope; Table S5 | EIC, R1 | holds; not in a main-text table (R4) |
| Room 5.6 pp | Table II (5.56) | EIC, R1 | holds; scales with recording length (S1) |
| Calibrated 95% interval 4.4–6.7 | Table S16; Table II prints nominal [4.50, 6.60] | EIC, R1 | holds; interval type differs (S5) |
| Ratio 1.10; 99.26% of 152,264 rows within 5% | Table V (1.103) | EIC, R1, R2, R3 | holds |
| No better than the placebo | Table S30 (−0.0003 [−0.0009, 0.0001]) | R1, R2 | holds as a nominal interval; uncalibrated (R6) |
| Within 2.2 decisions | Table S31c from Table S17 (2.16) | R1 | arithmetic holds (2.16 = 0.0047 × 460.7); post hoc, not scoring-qualified (R6, S9) |
| Braking prediction 83% | Table II (0.831) | EIC, R1 | holds; conditions missing (R10, R11, R13) |
| Per-phase 89% in sample | Table S23 (0.893) | R1, DA | holds (4.96/5.56 = 0.892) |
| Held-out 90% and 99.9% | Table S32 (0.903, 0.999 like for like) | R1, R2, R3 | holds on its stated basis; against record 0.868 and 0.964 (R7) |
| 12% with a 6 m/s² stop at 0.75 s | Table III (0.122) | EIC, R1, R3 | holds; assumptions (R12); range omitted (S8) |
| Time gap 0.314 (§VII only) | Table II | EIC | holds; not in the abstract (S8) |

No seat found an arithmetic mismatch that affects a claim. Three presentation points:
- R1, EIC: RR(N) 0.0012 sits at the edge of its printed interval in Table II (0.00122 against 0.00119; disclosed in Table S5).
- R1: Fig. 2(a) shows N's mean outside its interval, with no note.
- R2, DA: "435.2" has no table (S17).

## Appendix D: Devil's Advocate issues and where they are carried

| DA issue | Level | Carried in |
|---|---|---|
| C1 | CRITICAL | VALIDATED; R1, R2, R8 |
| M1 positive control grades only between-phase information | MAJOR | R5 (SC-13) |
| M2 the "room" is largely the cost of a one-scale sweep; RR not rebased on the scheduled baseline | MAJOR | Overlaps R5 (amplitude-limited test on the per-phase frontier) and R7. The DA's call to rebase the headline room is a DA-only sub-claim and creates no separate item (#1098). |
| M3 recording-length dependence | MAJOR | S1 (SC-3) |
| M4 2 Hz tracker-lag effect | MAJOR | R13 (SC-32) |
| M5 recording-policy inference rests on confounded run sets | MAJOR | R9 (SC-19), R8 (SC-16) |
| M6 the braking prediction's 83% | MAJOR | R11 (SC-24), S18 (SC-33) |
| M7 neither commitment closed loop; perfect stop | MAJOR | R12 (SC-30) |
| M8 equal caution is outcome-conditioned | MAJOR | S11 (SC-21) |
| m1–m7 | MINOR | S11, S17, S10/R6, S9, (m5: no non-DA seat; not carried), S19, S15 |

DA m5 is not carried. In it the conclusion conflates lead-state information with allocation: §VII says the room "is recovered by information about the lead's motion state and by allocating caution between its phases". No card-backed seat raised it, so it creates no item. It is recorded here for the author's attention.

---

## Review Panel Provenance (#540/#740)

**Correction made after Step 1 was written.** This section first said the provenance builder was not installed. That was wrong. The scripts are in the plugin's root `scripts\` folder, not in the skill's own folder. The correction changes no finding and not the decision.

**How the record was built.** The builder was run on the hand-recorded input `work\panel_provenance_input_v12.json`, through a wrapper (`prov_lf_wrapper_v12.py`, in the session scratchpad). The wrapper hands the builder an LF-line-ending copy of `shared\contracts\reviewer\full.json`. This Windows install stores that file with CRLF endings; with LF endings its digest equals the pinned `d958bc2a…`. The v11 review used the same workaround. No plugin file was changed.

**Results.** `build` exit 0; `validate` PASS; `build-carrier` exit 0; `validate-carrier` PASS.

```
artifact: work\panel_provenance_v12.json   carrier: work\panel_provenance_carrier_v12.json
role_separated: true | fresh_context: true (within_panel_attempt_only) | blind_to_peer_outputs: unknown
model_family_distinct: false | provider_distinct: false | human_distinct: false
correlated_error_disclosure: required (same_model_family) — "All model-executed review seats used one model family; role separation does not remove correlated-error risk."
independence_claim: not_computed_from_personas
execution_topology_sha256: b7e84332d480b461e6a7a3ad6578006edda0842a2bb5d43f96ec083b62bb3094
```

**No sprint contract.** This panel ran the skill's `full` mode **without** a sprint contract: the Synthesis Protocol plus the qualitative decision standards, with no dimension scores or fired conditions. The v11 review ran with contract `reviewer/reviewer_full/v2`, and its decision was mechanical. The two decisions are therefore reached by different routes and are not strictly comparable. The `contract_id` in the provenance artifact is the closed binding the builder requires for `reviewer_full`; it does not mean that a contract governed this synthesis. Without contract cards, `check_phase_conformance.py` and `check_panel_synthesis.py` do not apply, and they were not run.

The table below is the hand-recorded observation behind the input file.

| Seat | role_id | context | peer outputs visible | actor | model family / provider | human reviewer |
|---|---|---|---|---|---|---|
| EIC | eic | own fresh subagent invocation | not recorded (see note) | model | claude (alias `sonnet`) / anthropic | none |
| R1 | methodology | own fresh subagent invocation | not recorded | model | claude (alias `sonnet`) / anthropic | none |
| R2 | domain | own fresh subagent invocation | not recorded | model | claude (alias `sonnet`) / anthropic | none |
| R3 | perspective | own fresh subagent invocation | not recorded | model | claude (alias `sonnet`) / anthropic | none |
| DA | da | own fresh subagent invocation | not recorded | model | claude (alias `sonnet`) / anthropic | none |

**Axes (derived by the builder from the input above; the reasons are this session's)**
- `role_separated`: true. Five distinct role ids were recorded at dispatch.
- `fresh_context`: true, within this panel attempt only. Five separate invocations.
- `blind_to_peer_outputs`: unknown.
  - The five seats were dispatched at the same moment.
  - Each was told not to open `review_v12_output\` except its own file, and each wrote its report to a separate file.
  - The rule was not technically enforced. A later-finishing seat could have opened an earlier seat's file.
  - The task logs that would show each seat's file reads are empty (0 bytes), so absence of peer reads is not proven. No report cites another seat.
- `model_family_distinct`: false (all one family). Disclosure required, reason `same_model_family`: correlated errors across seats cannot be ruled out, and agreement between seats is not evidence of independent judgement.
- `provider_distinct`: false.
- `human_distinct`: false. No human reviewer. The accountable human for the review run is the user who accepted the cards.

**Model versions.** The seats were requested with the alias `sonnet`. The tool does not echo the resolved version; the expected model is Claude Sonnet 5.5. The synthesizer (this file) is Claude Opus 5.5, the same model that wrote v12. The Phase 0 field analysis and cards were written by Claude Sonnet 5.5.

**Writer and reviewer.**
- The seats carrying the review judgements differ in model from the v12 writer (Sonnet against Opus 5.5) but share its family and provider.
- The synthesis shares the v12 writer's model.
- Self-preference bias in the synthesis cannot be ruled out. To limit it, the synthesis adds no review comment of its own, and every item traces to a seat's report.

## Advisory attachments

The acronym check, suggested-reference check and reviewer claim check are script-driven. When this section was first written they had not been run (see the correction above). Their status is reported in the final review file. Nothing in this package comes from them.

**Manual reference spot-check, done instead**
- Method: public arXiv and Crossref records, reached by identifier only. No manuscript text and no personal details were sent.
- Matched (title and authors as cited):
  - [8] arXiv:2606.03590, with the IROS 2026 acceptance comment;
  - [14] arXiv:2610.09520;
  - [17] arXiv:2602.16035;
  - [19] arXiv:2603.10407;
  - [27] arXiv:2510.15505, plus DOI 10.1109/ICRA57385.2026.11697367 (ICRA 2026, pp. 4547–4554);
  - [24] DOI 10.1109/CDC57313.2025.11312370 (CDC 2025, pp. 3081–3088).
- Scholar Sidekick was unavailable: one subscription error, then rate limits.
- The references the seats suggested (R2's seven tracking works; R3's standards) are marked "to be verified" and were not checked.
