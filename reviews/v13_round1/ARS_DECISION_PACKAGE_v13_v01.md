# Editorial Decision Package: draft v13 (the record)

Written 2026-11-21 by the synthesizing session (Claude Fable 5.2). Skill: `academic-research-skills:academic-paper-reviewer` v1.11.1 (plugin 3.24.3), mode `full`, without a sprint contract (the route of the v12 review). Every item below traces to a seat report in `phase1\`. Points found only by the synthesizing session are marked "compiler note" and carry no seat authority.

**Freeze reviewed:** the 03:08:15 freeze of 21 Nov 2026 in `revision_v13\work\A_text\out\freeze_v13\`: manuscript `.md` 433be494, `.tex` 3a09cb42, `.pdf` 1dcbcf2d, supplement 9180a11c, response letter ef7c581f. The seats read the package between about 03:00 and 03:08, while it was re-frozen twice (02:51, 03:03, 03:08). The three versions differ in 11 manuscript lines, 9 supplement lines and 4 response-letter lines (checked by `diff`). Every finding carried here was re-checked against the 03:08 text; where a re-freeze already answered part of a finding, the item says so.

## Calibration Resolution

`NOT_CALIBRATED`. No candidate profile is applied. The decision is a qualitative synthesis, not a score.

## Part 1: Editorial Decision Letter

### Decision: Major Revision

All five seats recommend Major Revision, each with confidence 4 of 5. No seat recommends Reject, Minor Revision or Accept. The Devil's Advocate's one CRITICAL issue is adjudicated VALIDATED and repairable: `da_critical_adjudications: [C1=VALIDATED]`.

The character of the decision differs from v12's. In v12 every seat asked for new runs. Here no seat doubts a number: the methodology seat reproduced the headline values, the conversions and the Newcombe intervals. The objections are to what the title, the abstract and several labels say the numbers show. Of the 14 required items, none needs a result to change; 12 are wording, one reformats existing values, one asks the author to check a printed value and several references.

### Consensus Analysis

| Topic | Seats | Carried as |
|---|---|---|
| "Detects rank information at the tracker's amplitude" is shown in a ±5% band, not at the tracker's own spread | Journal-Fit W4, Methodology W1, Domain W4, DA C1 (4 of 5) | R1 |
| The confirmatory equivalence could hardly fail; it is expected by construction | Journal-Fit W1, Methodology W2, Domain W11, DA M1 (4 of 5) | R2 |
| The IMM as tuned does not vary and is not a fair multiple-model test; "NIS near 2" is loose | Methodology W6, Domain W1 and W3, DA M2 (3 of 5) | R3 |
| The one filter whose margin varies recovers a positive share and is absent from title, abstract and conclusion | Domain W5, DA M3; Methodology W5 adds that it has no permuted twin | R4 |
| The title advertises real driving logs and cut-in, where nothing was tested | Journal-Fit W2, Methodology W8, Domain W6, Practical W10, DA M7 (5 of 5) | R5 |
| The Discussion's closed-loop inference is contradicted by the time-gap arm | Practical W4, DA M4; Journal-Fit W5 | R6 |
| Closed-loop baseline regime, "no extra cost", the ±0.10 margin | Journal-Fit W5, Methodology W7, Practical W2, W3 and W5, DA M5, M6 and m1 (4 of 5) | R7 |
| "Costs progress" hides a safety gain behind stop-and-go leads | Journal-Fit W12, Methodology W12, Practical W6, DA M6 (4 of 5) | R8 |
| "Most of the room" holds only pooled; partial oracles do not grade in any sub-population | Methodology W3 and W4, DA M8 and M9 | R9 |
| Rate confounded with latency; "depends on 2 Hz" overstated for the total room | Methodology W13, Domain W7, DA m7 | R10 |
| No road user behind the ego; costs to followers and occupants unscored | Practical W1, DA M6 and m6, Methodology W16 | R11 |
| Abstract not readable alone; private vocabulary | Journal-Fit W3 and W6 | R12 |
| AI assistance, unnamed "coordinator", literature read from abstracts, one reference not reconcilable with its description | Journal-Fit W8 and W9, Domain reference notes | R13 |
| Inconsistent or unfinished supplement entries | Journal-Fit W13, Methodology checks, Domain W13, DA m4 and m5 | R14 |

**Splits arbitrated.**
1. *Severity of the abstract's readability* (Journal-Fit MAJOR; no other seat raised it). Kept as required: the abstract decides the desk reading at this journal, and the fix is wording only.
2. *New multiple-model arm* (Domain W1(a), DA M2 prefer a new manoeuvre-tuned arm; Methodology accepts narrowed wording). Arbitrated: narrowed wording is required (R3); the new arm is suggested (S2). A new arm would be post hoc and descriptive, and the tested IMM followed a tuning rule fixed in advance.
3. *New closed-loop level where the baseline has no contact* (Practical W2(3)) and *cost on all 60 pairs* (Methodology W7). Arbitrated: stating the regime is required (R7); the new values are suggested (S5).
4. *Whether C1 needs a new value* (DA: permuted twin at the tracker's own spread; Journal-Fit and Domain: wording only, values exist). Arbitrated: wording is sufficient to remove the false statement, because Table III already prints the own-spread oracle; the twin is suggested (S4).

### Devil's Advocate CRITICAL adjudication

**C1. VALIDATED, repairable.** The abstract, contribution 1, Section V-A and the conclusion say the score "detects rank information at the tracker's amplitude". The control E5 is a ±5% band (Table I: "varied by ±5% in the order of each decision's realised error"). Table III shows the tracker of record inside that band for 99.9% of rows, and the oracle built at its own spread recovers 0.0001 [0.0000, 0.0002] of the room, against E5's 0.013. Four seats found this separately, and the synthesizing session confirmed each number in the 03:08 text. The equivalence itself stands. The statement that licenses reading the null as more than a blunt-measure null does not hold at the tracker's own spread.

*Note on the pre-registration (compiler note).* The text follows the plan here: Amendment 10 §2.2 defined E5 as ±5% around the median ratio, and §9 dictated the words "detects rank information at the tracker's amplitude". The defect is in the plan's wording rule, not in the author's compliance. The repair is therefore a departure from §9 toward the narrower statement, to be recorded in Table S5 with its reason, as §11 allows.

### Decision Rationale

Under the qualitative standards a validated DA CRITICAL blocks Accept, and fourteen must-fix items across five concurring seats exclude Minor Revision. Reject is not indicated: the design is sound, the evidence is new and pre-registered, failures are reported, and every must-fix item can be met from values that already exist.

### Blocking Issues (immutable source order)

R1 to R14 below, in source order. This is not a work order.

## Part 2: Revision Roadmap

"Needs" says whether an item changes a value. No item asks for a result to change.

### Required Revisions (Must Fix)

| Ref | Revision | Severity | Evidence anchor (03:08 text) | Source | Location | Needs |
|---|---|---|---|---|---|---|
| R1 | State E5 as detection in a ±5% band and give the tracker of record's own-spread oracle (0.0001 [0.0000, 0.0002], Table III). Say that by the rule of Section IV-C the tracker of record is amplitude-limited, like the IMM. Record the departure from the plan's wording rule. | critical (DA C1, validated) | Abstract: "the score detects rank information at the tracker's amplitude"; Table III online CV row | EIC W4; R1 W1; R2 W4; DA C1 | Abstract; Section I contribution 1; IV-C; V-A; VII; Table I | Wording only (values in Table III) |
| R2 | Say that the equivalence was expected from the measured constancy and that the margin (0.05) is about four times what the ±5% oracle recovers (0.013). Lead with the observed bound (share within [−0.0009, 0.0015]; at most 1.8 decisions of about 1,204). | major | Section I: "so a null is expected"; Table II N row | EIC W1; R1 W2; R2 W11; DA M1 | Abstract; V-A; VI | Wording only |
| R3 | Restrict every IMM statement to the IMM as tuned here. State in the main text that its CA model's acceleration term is 0.001 with the NIS window not reached, and that the planner receives only the position–velocity block under a constant-velocity prediction. Remove the IMM from "covariances that vary". Qualify "NIS near 2" (a median over runs; no tuning run inside the window) and "The mechanism persists". Do not attribute the IMM's constancy to the Riccati steady state. | major | Section I: "we also test covariances that vary, among them an interacting-multiple-model"; Supplement S4: "The NIS window could not be reached on the search grid" | R1 W6; R2 W1, W2, W3, W9; DA M2 | Title; Abstract; I; III-D; V-B; V-D; VI | Wording only. If braking-phase NIS (Table S7, one program, old runs) is quoted in the main text it needs a recount first |
| R4 | Put the adaptive filter's result in the abstract and the conclusion, with its descriptive status: its margin varies (21.5% of rows within 5%) and it recovers 0.0459 [0.0390, 0.0533] of its room, about what its oracle recovers (0.0477). Say that this share has no permuted twin, so information is not separated from jitter. | major | Section V-B: "recovers a small share of its room on these runs" | R2 W5; DA M3; R1 W5 | Abstract; V-B; VI; VII | Wording only |
| R5 | Retitle to the confirmed scope (simulated lead braking, open and closed loop). Describe cut-in and the real logs as attempted test beds that showed no room, not as tests or a "replication". Say in Limits why cut-in could not test young tracks (one decision of 5,293 on a track younger than 1 s; zero wrong goes at any margin). | major | Title: "in Closed Loop and on Real Driving Logs"; Scope: "the nuScenes replication"; Table S18 | EIC W2; R1 W8; R2 W6; R3 W10; DA M7 | Title; I Scope; III-C; VI Limits; Fig. 1 caption | Wording only (values in Tables II, S18) |
| R6 | Remove or restate the inference that closed loop "supports the 3 s reading". The time gap, with no information about the lead's motion, also reaches no contact and loses less time; the arms saturate and closed loop does not rank them. Report the time gap beside the braking prediction. | major | Section VI: "which supports the 3 s reading"; Table IV TG lower level | R3 W4; DA M4; EIC W5 | VI "Which commitment applies"; Abstract; V-C | Wording only |
| R7 | State the closed-loop regime in the main text: the levels were set where the baseline has contact in 20% and 5% of cases, and the baseline is in full braking in 52.7% and 78.6% of decisions (Table S23). Say that time lost is compared on pairs without contact and is about 24.5 s for every arm because the lead stays stopped. Give the number (0.16 [0.10, 0.22] s) instead of "no extra cost" wherever the label stands alone, and carry the ±0.10 margin with "equivalent". Name the matching basis one way. | major | Table IV caption: "over pairs without contact"; Table S23 F0 rows | EIC W5; R1 W7; R3 W2, W3, W5; DA M5, M6, m1 | Abstract; III-B; V-C; VII; Table IV | Wording only. The 03:03 re-freeze already added the level, "by the plan's rule" and the numbers in Section VI |
| R8 | Do not let "costs progress" stand alone for stop-and-go leads in the abstract and conclusion: there the braking prediction lowers wrong goes by 4.7 points for 1.7 points of caution, and in closed loop it is "safer at a cost". | major | Abstract: "costs progress behind constant-speed, mildly braking and stop-and-go leads" | EIC W12; R1 W12; R3 W6; DA M6 | Abstract; VII; Table V | Wording only (Section V-D was repaired at 03:03) |
| R9 | Say that "most of the room" holds only pooled: give the ego-moving value (0.411 [0.338, 0.488]) beside 0.783 or drop "most". Apply the paper's own rule where the partial oracles do not grade (ego moving, before braking, braking): print decision-equivalents, or state as a limit that the score's sensitivity is shown for the pooled population only. | major | Section IV-C: "where they do not, shares are printed as decision-equivalents"; Table S8 last row | R1 W3, W4; DA M8, M9 | Abstract; V-A; VII; Tables III, S8 | Reformatting of existing values (decision-equivalents derived from printed numbers; each new printed value needs its source key and recount) |
| R10 | Separate rate from latency (compare at equal latency, Table S16) and say which magnitude depends on 2 Hz: the after-stop room does; the total room falls only from 5.58 to 5.07 points. Compiler note: the plan's own rule for this outcome asks the abstract to give magnitudes "at 2 Hz without latency" with the 10 Hz value; the abstract has neither, and no departure is recorded. | major | Abstract: "Magnitudes depend on 2 Hz updates and the recording policy" | R1 W13; R2 W7; DA m7; compiler note (Amendment 10, B7 rule and §9 "Always") | Abstract; V-D; VII; Fig. 4 | Wording only (values in Tables V, S16) |
| R11 | State in Scope and Limits that no test bed has a road user behind the ego, that rear contacts were removed from the real-log score after the design-split result (6,122 of F0's design-split decisions change from unsafe to safe), and that costs to following traffic and occupants (deceleration, jerk, fallback share) enter no classification. | major | Section III-C: "contacts with actors behind the ego were no longer counted" | R3 W1; R1 W16; DA M6, m6 | I Scope; III-C; VI Limits | Wording only (values in Tables S23, S24, S27) |
| R12 | Make the abstract readable alone: shorten the first sentence, define the room and equal caution in one clause, give shares as percentages. Reduce source codes and caption length where possible. | major | Abstract, first sentence (44 words) | EIC W3, W6, W7 | Abstract; Tables I to V captions | Wording only |
| R13 | Author acts. Complete the author's verification statement. Replace "this revision" and the unnamed "coordinator" with wording fit for a first submission. Read reference [15] in full and confirm that it contains the fixed-covariance constant-velocity baseline the text attributes to it; its title concerns class uncertainty. Check [26], [37] (possibly withdrawn), [27] (no DOI) and [38] (no date). | major | Section IV-E: "shaped this revision"; Table S5: "approved by the coordinator"; Section II sentence on [15] | EIC W8, W9, W14; R2 reference notes, W12 | IV-E; Acknowledgment; II; References; Supplement S3, S13 | No value; author reading and wording |
| R14 | Repair the supplement and table defects: Table S13's share of N (0.00122) lies outside its own interval [−0.00108, 0.00119] and its header lacks a bracket; Table V's old-evaluation values (5.51, 0.837, −0.0004) appear in no supplement table; Table S17 is all "n.c." and "n.c." is defined as not computed by the deadline although these values are undefined; "after-stop room" is never defined; run counts are given two ways. | major (as a set; each is minor) | Table S13 row "Share of N"; Table S17; supplement line 3 | EIC W13, W17; R1 checks; R2 W13; DA m4, m5 | Supplement S5.3, S6.2, S7; Table V | One value check (Table S13); otherwise wording |

### Suggested Revisions (Should Fix / Consider)

| Ref | Revision | Source | Needs |
|---|---|---|---|
| S1 | Add an amplitude-response curve: the ranking oracle's share against band width (for example ±5, 10, 20, 50%), so a reader sees what amplitude a covariance needs. | DA M1 | New analysis (exploratory) |
| S2 | Add a multiple-model arm tuned for manoeuvres, or at least report the present IMM's mode probabilities by phase. | R2 W1; DA M2 | New analysis (descriptive, post hoc) |
| S3 | Add an arm with the tracker's own predicted covariance over the look-ahead, and a "true current state, constant-velocity prediction" reference that splits the room into tracker lag and prediction-model error. | R2 W2; DA alternative 1 | New analysis |
| S4 | Print E5p's share with its interval and call it "no within-run information"; add a permuted twin at the tracker's own spread and for the adaptive filter. | R1 W5; DA C1 | New values |
| S5 | Report closed-loop cost on all 60 pairs; print each matched arm's design caution and scale; consider a level where the baseline has no contact. | R1 W7; R3 W2 | New values |
| S6 | Use the time gap as a second baseline; split the fallback share into moving and standstill decisions; say in the main text that F0 is the tracker's own mean. | DA M5; R2 W11 | New values and wording |
| S7 | State the interval type and any stratification; print the estimated coverages; call the 99% fallback "coverage not established"; quote each interval with its level; write "classified" rather than "confirmed" for the IMM step. | R1 W9, W10, W11 | Existing values and wording |
| S8 | Describe the second programs as a recount on shared components; say whether an external timestamp of the plan hash exists. Compiler note: the build report counts 390 of 1,383 printed values without an agreeing recount while the supplement marks 98 with ‡; say what the other values are. | R1 W15; DA m2, m3 | Wording |
| S9 | Report NIS by update rate; give units for the tuned constants; define the lag column as the residual after the stop. | R2 W8, W10, W14 | Small new values |
| S10 | Name the function under test, the speed range (5 to 15 m/s) and the absent radar range rate in Limits; soften content claims about standards whose texts were not read; note that the braking prediction's rate matches the generator; carry the vulnerable-road-user scope into the conclusion. | R3 W7, W8, W9, W11 | Wording |
| S11 | Figures: explain why the IMM's curve lies above F0's in Fig. 2; show the rule bounds in Fig. 3. Compiler note from the LaTeX log: reference [3] overflows its column by 46 pt. | EIC W15; R3 W12 | Figure edits |
| S12 | Remove the triple repetition across abstract, contribution 2 and conclusion; say "its own room" for the IMM; cut process-log language from the supplement; tell the editor about the related manuscript [10] in the cover letter. | EIC W10, W11, W14, W18 | Wording |
| S13 | References: add the DOI of [27], the date of [38], a chapter for [25], an access date for [3]; cite the intelligent-vehicle threat-assessment work the search found. | EIC W16, W9; R2 W12 | Wording, after author reading |
| S14 | Say that caution is averaged over decisions whose selected row is safe, a set that depends on the outcome, and that matching by open-loop caution does not equalise closed-loop risk. | R1 W14; DA m8 | Wording |
| S15 | Compiler notes on the plan's reporting rules: the plan asks for file times "listed in the supplement" (S12 points to the deposit); the abstract gives the per-phase schedule without the word "diagnostic"; the orderings "keep one order" only at point estimates (tuning-run intervals overlap). | compiler notes (Amendment 10 §5.6, §9, §10.1(d)) | Wording |

## Part 3: Reviewer Report Summary

| Seat | Recommendation | Confidence | Critical / major / minor | Main point |
|---|---|---|---|---|
| Journal-Fit | Major Revision; desk-rejection risk moderate | 4 | 0 / 9 / 9 | The one confirmed result is an expected null; the title promises more than Table II delivers; the abstract is not readable alone |
| Methodology | Major Revision | 4 | 0 / 8 / 8 | Numbers reproduce; three constructs do less than the wording says (control amplitude, equivalence margin, pooled share) |
| Domain | Major Revision | 4 | 0 / 6 / 8 | The IMM as tuned is near-degenerate; the planner interface discards what a CA or IMM filter adds; the adaptive filter is underplayed |
| Practical | Major Revision | 4 | 0 / 4 / 8 | No follower in any test bed; closed-loop baseline in a degenerate regime; the time-gap arm contradicts the Discussion |
| Devil's Advocate | Major Revision | 4 | 1 / 9 / 8 | The confirmed equivalence could not fail; detection is not shown at the tracker's own spread |

Strengths named by at least two seats: failed hypotheses are printed; the cost of the paper's own best source is reported against its interest; the departures table is complete, including an error found afterwards; the tracker-of-record equivalence is robust across frontier, rate, latency and commitment; the brake test supports the closed-loop plant model.

## Review Panel Provenance (#540/#740)

Built and replay-validated with `scripts\review_panel_provenance.py` (plugin root) through an LF-line-ending copy of `shared\contracts\reviewer\full.json`, as in the v12 review. No plugin file was changed. `build` exit 0; `validate` PASS; `build-carrier` exit 0; `validate-carrier` PASS. Files: `work\panel_provenance_input_v13.json`, `work\panel_provenance_v13.json`, `work\panel_provenance_carrier_v13.json`.

- role_separated: true. Each seat was a separate fresh sub-agent given only its card and the package paths.
- fresh_context: true (within this panel attempt only).
- blind_to_peer_outputs: unknown. Seats were told not to open other seats' files; file access is not observable.
- model_family_distinct, provider_distinct, human_distinct: false. All five seats and the synthesis ran on Claude Fable 5.2. Required disclosure: all model-executed review seats used one model family; role separation does not remove correlated-error risk.
- The reviewing model (Fable 5.2) differs from the writer of v13 (Opus 5.5). It is the same model that wrote some second programs and the claim audits of v13, so it is not independent of the verification chain.
- The `contract_id` in the artifact is the binding the builder requires; no sprint contract governed this synthesis, and `check_phase_conformance.py` and `check_panel_synthesis.py` were not run.
- Card confirmation: the pause was not held (non-interactive sub-agent). The identities are the cards the user accepted for v12; see `00_phase0_field_analysis_and_cards.md`.
- The DA seat's brief listed seven points of the paper's logic to test, written by the synthesizing session after its own first reading. This primed the DA seat. The four card seats received no such list, and three of them reached the C1 finding without it.

## Advisory attachments

### Attachment: Suggested-Reference Check (advisory, #1001)
The suggested-reference check did not run: it sends titles to online indexes, and this review was run with no external traffic.

### Attachment: Reviewer Claim Check (advisory, #1002)
The reviewer claim check did not run as a judge dispatch. In its place the synthesizing session checked each carried finding's numbers and quotations against the 03:08 files by hand and by script.

### Attachment: Acronym Check (advisory, #849)
`check_acronyms.py` exit 0; report in `work\acronym_check_v13.txt`. It lists CANMOT, CARLA, PS, SHA and similar tokens as not defined; none is a reviewer finding.
