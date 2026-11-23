# ARS Pre-Submission Review of Draft v13 (target: IEEE OJ-ITS, regular paper)

**Time stamp:** 2026-11-21 03:17 −05:00 (local clock). The frozen files still had the 03:08 hashes when this file was finished.

**Manuscript:** "Do Fixed-Noise and Interacting-Multiple-Model Tracker Covariances Improve Planning Decisions? An Equal-Caution Test on Fresh Simulation Runs, in Closed Loop and on Real Driving Logs". Nothing in `revision_v13\` was changed.

**Freeze reviewed.** The 03:08:15 freeze of 21 Nov 2026 in `revision_v13\work\A_text\out\freeze_v13\`:

| File | SHA-256 starts |
|---|---|
| MANUSCRIPT_v13.pdf | 1dcbcf2d |
| MANUSCRIPT_v13.tex | 3a09cb42 |
| MANUSCRIPT_v13.md | 433be494 |
| SUPPLEMENT_v13.md | 9180a11c |
| RESPONSE_TO_REVIEW_v13.md | ef7c581f |

The text was re-frozen twice while the review ran (02:51, 03:03, 03:08). I read the 02:51 text in full, then compared it with the 03:08 text by `diff` (11 manuscript lines, 9 supplement lines and 4 response-letter lines differ) and read every changed line. Every finding and quotation below was checked against the 03:08 files.

**Models.** v13 was written by Claude Opus 5.5. This review (all five seats and the synthesis) ran on Claude Fable 5.2, a different model, on purpose. Fable 5.2 also wrote some of v13's second programs and its claim audits, so the reviewer is independent of the writer but not of the verification chain.

**Record files** (all in `review_v13_output\`): `ARS_DECISION_PACKAGE_v13_v01.md` (the record), `ARS_AUTHOR_LETTER_v13_v01.md`, `00_phase0_field_analysis_and_cards.md`, `phase1\01_…05_…md` (seat reports), `work\` (provenance, acronym check).

## 1. Decision, rating and readiness

| Question | Answer |
|---|---|
| **Panel decision** | **Major Revision.** Five of five seats, each with confidence 4 of 5. The Devil's Advocate's one CRITICAL issue (C1) is adjudicated **validated and repairable**. |
| **What kind of Major Revision** | A wording revision. No seat doubts a number; the methodology seat reproduced the headline values, the conversions and the Newcombe intervals. Of 14 required items, **none changes a result**: 12 are wording, one reformats existing values, one is a value check plus author reading of references. No new run is required. |
| **Star rating** | **About 4 stars as frozen** (v12: about 3.5). With the 14 required items done, about 4.5. The remaining half star is outside wording: the one confirmed covariance result is a null that the paper itself calls expected, in one scenario family. |
| **Submission readiness** | **Not ready as frozen. Ready after one wording pass** over the title, the abstract, Sections I, V and VI, the conclusion and a few captions, plus the author-only gates. |
| **My reading of a human editor** (a judgement, not a calibrated probability) | As frozen: Major Revision about 55%, Reject about 25% (expected null, a title that promises more than Table II, heavy AI authorship), Minor Revision about 20%. After the wording pass: Minor Revision or better becomes the most likely outcome. |
| **Change since v12** | v12's required items asked for new evidence. v13 supplied it: fresh runs under a locked plan, a closed-loop test, a real-log attempt, four tracker variants, 10 typeset pages. Of v12's R1–R13, 9 are resolved and 4 partly (Section 4). The new objections are about reach: what the title, the abstract and several labels say the new evidence shows. |

**Submission gates (author-only; not scientific findings):** the author block; the repository name and DOI; the "[AUTHOR CONFIRMATION: …]" line in the AI-content statement; and the journal template's own placeholders (dates, volume, running head).

## 2. How the review ran, and what bounds it

- **Skill.** `academic-research-skills:academic-paper-reviewer` v1.11.1 (plugin 3.24.3), mode `full`, **without a sprint contract**, the route of the v12 review, so that the decision and rating are comparable with v12's.
- **Phase 0.** Coverage and four cards in `00_phase0_field_analysis_and_cards.md`. **The card-confirmation pause was not held**, because this run is a non-interactive sub-agent. The four identities are, word for word, the cards the user accepted for v12; only their focus anchors were re-pointed to v13's sections. If the user wants other cards, Phase 1 must be run again.
- **Phase 1.** Five seats, each a separate fresh sub-agent on Fable 5.2 that received its card and the package paths only (manuscript, supplement, four figures). Seats were told not to read the response letter, the plan, the v12 review or each other's files.
  - The seats read between about 03:00 and 03:08, across the two re-freezes. I re-checked every carried finding against the 03:08 text. Three seat findings were partly answered by the re-freezes; Section 3 says where.
  - The Devil's Advocate's brief listed seven points of the paper's logic to test, which I wrote after my own first reading. That primed the DA seat. The four card seats had no such list, and three of them reached the C1 finding without it.
- **Phase 2.** Synthesis in the decision package. Every item traces to a seat report. Points that only I found are marked "compiler note".
- **Step 2 (my own reading, outside the seats).** The response letter, `AMENDMENT_10_v13.md`, the three lock files, `TEXT_FREEZE_v13.md`, the build report, the recount coverage file, the outcome file, the v12 review, and the headings of the claim audits (v02 to v04).
- **Provenance.** `review_panel_provenance.py`: `validate` PASS, `validate-carrier` PASS (through an LF copy of `full.json`). Role-separated: true. Fresh context within the panel: true. Blind to peer outputs: unknown. Model family, provider and human distinct: false. Required disclosure: all model-executed review seats used one model family; role separation does not remove correlated-error risk. Calibration: `NOT_CALIBRATED`.
- **Checks run.** `check_acronyms.py` exit 0. `check_author_letter.py`: PASS. The suggested-reference check and the reviewer claim check were not run (the first sends titles to online indexes). In their place I checked the carried numbers and quotations against the files.
- **Not seen.** The PDF's page images: no PDF renderer is installed. I took the page count (10) and the layout warnings from the LaTeX log, and extracted the text layer with `pdftotext` (10 pages, no unresolved reference). Table placement and column overflow were not seen. The deposit was not read; it does not exist yet.
- **External traffic.** None. No web search, no fetch, no citation service. References were judged offline from the text.
- **Hashes verified by me.** The five frozen files above; the plan hash `85787f3d…8f6b` against `LOCK_A10_1.txt`; the two lock-stage hashes quoted in Section IV-E (`02048a43…a4df`, `94e06ed6…c0a6`) against the lock files themselves.

## 3. Required items (R1–R14 of this review)

Each item gives the location, the evidence and a concrete fix. "Needs" says whether a value changes. The record is Part 2 of the decision package. The order is source order, not a work order.

**What the control and the null show**

- **R1. The detection claim is made at ±5%, not at the tracker's own spread** (DA C1, validated; Journal-Fit, Methodology, Domain).
  - **Where:** Abstract, contribution 1, Sections IV-C, V-A and VII: "the score detects rank information at the tracker's amplitude".
  - **Evidence:** Table I defines E5 as "varied by ±5%". Table III shows 99.9% of the tracker's rows inside 5% of its median, and the oracle at its own spread recovers 0.0001 [0.0000, 0.0002], against E5's 0.013.
  - **Fix:** say "detects rank information in a ±5% band"; give the own-spread oracle beside it; say that by the rule of Section IV-C the tracker of record is amplitude-limited, like the IMM.
  - **Plan note:** the text follows Amendment 10 here (§2.2 defined E5 at ±5%; §9 dictated these words). The repair is a departure from §9 toward the narrower statement; record it in Table S5.
  - **Needs:** wording only. The values are in Table III.
- **R2. The equivalence could hardly fail** (Journal-Fit, Methodology, Domain, DA).
  - **Where:** Abstract; Section V-A; Section VI.
  - **Evidence:** Section I says "so a null is expected". The margin is 0.05 of the room; perfect ranking in the ±5% band recovers 0.013.
  - **Fix:** say the equivalence was expected from the measured constancy; lead with the observed bound (share within [−0.0009, 0.0015], at most 1.8 of about 1,204 decision-equivalents) and give the margin second.
  - **Needs:** wording only.
- **R3. The IMM result is about this IMM as tuned** (Methodology, Domain, DA).
  - **Where:** Title; Abstract; Section I "we also test covariances that vary, among them an interacting-multiple-model (IMM) tracker's"; Sections III-D, V-B, V-D, VI.
  - **Evidence:** Supplement S4: the CA model's acceleration term is 0.001 and "The NIS window could not be reached on the search grid". Table III: the IMM, the re-tuned CV and the CA filter all have 99.7% of rows within 5%. Table S6: nothing changes across the three transition settings. Supplement S4 also says the planner receives only the 4 × 4 position–velocity block, and Section III-E predicts every actor at constant velocity, so the CA model's acceleration terms never reach the margin. For the re-tuned CV, Supplement S4 says "no run lies inside the window".
  - **Fix:** write "the IMM as tuned here" throughout; take the IMM out of "covariances that vary"; state the two limits (tuning rule, planner interface) in Section III-D and in Limits; write "median over runs near 2" for the re-tuned filter and qualify "The mechanism persists"; do not explain the IMM's constancy by the Riccati steady state.
  - **Needs:** wording only. Caution: the braking-phase NIS values (Table S7) are one-program values on the old runs; quoting them in the main text needs a recount first under the plan's §10.1.
- **R4. The one covariance that varies is missing from the abstract and conclusion** (Domain, DA; Methodology adds the caveat).
  - **Where:** Abstract; Section VII. Section V-B has it: "recovers a small share of its room on these runs".
  - **Evidence:** Table III, adaptive filter: 21.5% within 5%; share 0.0459 [0.0390, 0.0533]; its oracle 0.0477. The interval lies above zero, so by the rule of Section IV-C it "recovers". A reader of the abstract alone would conclude that tracker covariances carry no decision value.
  - **Fix:** one clause in the abstract and conclusion, marked descriptive: the filter whose margin varies recovers about 5% of its room, about what its amplitude allows. Add that it has no permuted twin, so information is not separated from jitter (E5's twin itself recovers about 0.005).
  - **Needs:** wording only.

**Title and framing**

- **R5. The title advertises tests that tested nothing** (all five seats).
  - **Where:** Title "in Closed Loop and on Real Driving Logs"; Scope "the nuScenes replication"; Fig. 1 caption.
  - **Evidence:** Table II: cut-in room 0.00 [0.00, 0.00], real-log room −0.01 [−0.13, 0.13], every later row "n.t.". Table S18: one decision of 5,293 on a track younger than 1 s. The abstract itself is honest about this.
  - **Fix:** retitle to the confirmed scope (simulated lead braking, open and closed loop); call cut-in and the real logs attempted test beds that showed no room; say in Limits why the cut-in runs could not test young tracks.
  - **Needs:** wording only.
- **R12. The abstract is not readable alone** (Journal-Fit).
  - **Where:** Abstract. The first sentence has 44 words; "room" and "equal caution" are used before any definition; results are bare decimals.
  - **Fix:** shorten the first sentence, define the room and equal caution in one clause, give shares as percentages. Shorten the longest captions.
  - **Needs:** wording only. The abstract is at 217 of 220 words, so R1, R4, R8 and R10 must be paid for by cuts (for example the real-log parenthesis and the repeated IMM numbers).

**Closed loop and labels**

- **R6. The closed-loop inference does not follow** (Practical, DA, Journal-Fit).
  - **Where:** Section VI: "which supports the 3 s reading: information about the lead's motion is worth room".
  - **Evidence:** Table IV, lower level: the time gap, which uses no information about the lead's motion, has contact difference −0.20 [−0.32, −0.10] and time lost −0.13 [−0.19, −0.06] s; the braking prediction has the same contact difference and +0.16 s. The per-phase schedule does the same. The arms saturate at zero contacts, so closed loop does not rank them.
  - **Fix:** remove the inference or restate it: every arm that brakes earlier than the class average removes the contacts, and the closed loop does not separate them. Report the time gap beside the braking prediction in Section V-C and, if space allows, the abstract.
  - **Needs:** wording only.
- **R7. The closed-loop regime and its labels need their conditions** (Journal-Fit, Methodology, Practical, DA).
  - **Where:** Abstract; Sections III-B, V-C, VII; Table IV.
  - **Evidence:** Table S23: the baseline is in full braking in 52.7% of decisions at the lower level and 78.6% at the higher. Table IV caption: time lost is taken "over pairs without contact". Time lost is about 24.5 s for every arm because the lead stays stopped. "Equivalent" means within ±0.10 of contact share, half of the baseline's 20%.
  - **Fix:** state the regime in Section V-C; give the number (0.16 [0.10, 0.22] s) wherever "no extra cost" stands alone; carry "within ±0.10 of contact share" with "equivalent"; name the matching basis one way.
  - **Partly done at 03:03:** the abstract now says "(lower caution level)" and "by the plan's rule", and Section VI gives the numbers.
  - **Needs:** wording only.
- **R8. "Costs progress" hides a safety gain** (Journal-Fit, Methodology, Practical, DA).
  - **Where:** Abstract and Section VII: "costs progress behind constant-speed, mildly braking and stop-and-go leads".
  - **Evidence:** Table V, stop-and-go: 1.7 points of caution for 4.7 points fewer wrong goes; in closed loop the same lead type is "safer at a cost" (Table S25).
  - **Fix:** in the abstract and conclusion, separate the stop-and-go case or give its two numbers.
  - **Partly done at 03:03:** Section V-D now says the prediction "still lowers wrong goes" there.
  - **Needs:** wording only.
- **R9. "Most of the room" holds only pooled, and shares are printed where the score does not grade** (Methodology, DA).
  - **Where:** Abstract; Section V-A; Section VII; Tables III and S8.
  - **Evidence:** Table S8: the braking prediction's share is 0.411 [0.338, 0.488] while the ego moves, and Table S10 gives 0.244 to 0.491 with short after-stop windows. Table S8's partial oracles are −0.248 / −0.061 / 0.338 in the braking phase, where the room is largest. Section IV-C says "where they do not, shares are printed as decision-equivalents", but Section V-A prints 0.411 as a share.
  - **Fix:** give 0.411 beside 0.783 or drop "most"; print decision-equivalents in the populations that do not grade, or state as a limit that the score's sensitivity is shown for the pooled population only.
  - **Needs:** reformatting of existing values. Each newly printed decision-equivalent needs its source key and recount under the build rules; no result changes.
- **R10. Rate, latency and the plan's own abstract rule** (Methodology, Domain, DA; compiler note).
  - **Where:** Abstract and Section VII: "Magnitudes depend on 2 Hz updates and the recording policy"; Section V-D; Fig. 4.
  - **Evidence:** Section V-D compares 2 Hz without latency with 5 and 10 Hz at 0.1 s latency. At equal latency (Table S16) the total room is 5.58, 4.99 and 4.75 points; only the after-stop room falls strongly (173.4 to 35.5).
  - **Compiler note:** Amendment 10's rule for this outcome (B7, and §9 "Always") asks the abstract to give magnitudes "at 2 Hz without latency" with the 10 Hz value. The abstract has neither, and Table S5 records no departure.
  - **Fix:** compare at equal latency in the text; say which magnitude depends on 2 Hz; put "at 2 Hz without latency" and one 10 Hz value in the abstract, or record the departure.
  - **Needs:** wording only. The values are in Tables V and S16.

**Who is left out**

- **R11. No road user behind the ego** (Practical; Methodology; DA).
  - **Where:** Scope; Section III-C "contacts with actors behind the ego were no longer counted"; Limits.
  - **Evidence:** the CARLA runs have two vehicles. On the design split the clearance change turns 6,122 of the class average's decisions from unsafe to safe (Table S27). Peak deceleration, jerk and the fallback share sit in Supplement S9 and enter no classification.
  - **Fix:** say in Scope and Limits that no test bed scores traffic behind the ego or occupants' comfort, give the count in Section III-C, and say that rear contacts are a real cost of an over-cautious margin that this score cannot see.
  - **Needs:** wording only.

**Author acts and defects**

- **R13. AI assistance, provenance wording and the literature basis** (Journal-Fit; Domain).
  - **Where:** Section IV-E "shaped this revision"; Acknowledgment; Table S5 "approved by the coordinator"; Section II; Supplement S13 "no full text was opened".
  - **Evidence:** the author's verification line is a placeholder. The "coordinator" is never said to be an AI session or the author. Reference [15] is titled "The impact of class uncertainty propagation in perception-based motion planning", while Section II describes it as a study in which "a constant-velocity baseline with a fixed covariance" stays competitive and calls it the nearest analogue of the null. The Domain seat could not reconcile the two, and I cannot check it offline.
  - **Fix:** the author reads [15] in full and confirms or rewrites that sentence; checks [26] (fit), [37] (possibly withdrawn), [27] (no DOI) and [38] (no date); completes the verification line; names who approved post-lock changes; writes "this manuscript" for a first submission.
  - **Needs:** no value. Author reading and wording.
- **R14. Supplement and table defects** (Journal-Fit, Methodology, Domain, DA).
  - Table S13: the share of N, 0.00122, lies outside its own interval [−0.00108, 0.00119]; the header "Room $R$ (pp" lacks a bracket. The v12 review already noted the first point.
  - Table V prints old-evaluation values (5.51, 0.837, −0.0004) that appear in no supplement table; Table S13 gives the grid values (5.56, 0.831, 0.00122).
  - Table S17 is all "n.c.", and line 3 of the supplement defines "n.c." as not computed by the plan's deadline, although these values are undefined (no room). Table S18 has the same cells. (Table S27 was repaired at 03:08.)
  - "After-stop room" is used in Sections V-D, Table V and Fig. 4 without a definition.
  - Run counts are given two ways (Table S5: 155 distinct stored runs; elsewhere 55 plus 120 and 35).
  - **Needs:** one value check (Table S13); otherwise wording.

## 4. Status of the v12 review's required items (v12 R1–R13)

**Counts: 9 resolved, 4 partly, 0 not resolved.** Quotations are from the 03:08 text.

| v12 item | Status | Evidence in v13 |
|---|---|---|
| R1 Lead with one take-away | **Partly** | Section I now has three contributions with the protocol first ("A protocol with an amplitude-matched control"), and exploratory results are one subsection. But the abstract opens with the test, and the Journal-Fit seat still finds no single take-away → this review's R2, R12 |
| R2 An arm whose covariance varies, or narrower framing | **Partly** | Four variants were added and the IMM is a pre-registered arm; the title names the trackers. But Table III shows the IMM at 99.7% within 5% ("barely varies"), and Section I still lists it among "covariances that vary". The one that varies is descriptive and absent from the abstract → R3, R4 |
| R3 Length | **Resolved** | 10 typeset pages (LaTeX log); body 5,230 words (v12: 8,926); supplement 11,966 (v12: 34,240) |
| R4 Abstract numbers in main-text tables | **Resolved** | 5.58 (Table II), 99.7% (Table III), 0.0009 (Tables II, III), 0.783 and 0.916 (Table II) |
| R5 Scope of the positive control | **Partly** | E5 and its permuted twin were added with a criterion fixed in advance (Section IV-C). But the band is ±5%, not the tracker's spread, and shares are still printed where the partial oracles do not grade → R1, R9 |
| R6 One estimand for N's share | **Resolved** | Table II: "0.0000 [−0.0009, 0.0015] (C)", gridless, one calibrated interval (99.4%, Table S9), margin 0.05; the 2.2 bound is gone. (Its severity is a new point → R2) |
| R7 Held-out per-phase figures | **Resolved** | Table S11: record basis "0.916 [0.864, 0.965]", like-for-like "0.918 [0.867, 0.968]"; chosen on old runs, applied once |
| R8 Confirmatory status | **Resolved** | Section IV-E: "fixed and hashed before any of their values was computed"; 105 + 105 fresh runs; hashes verified against the lock files |
| R9 The transfer sentence | **Resolved** | Section V-D: "magnitudes do not transfer"; only two statements are said to hold in every run set. (They hold at point estimates only → S15) |
| R10 Filter tuning | **Partly** | Re-tuned CV, CA and IMM were run and Tables III and V report lag, room by phase and CK3 share. But "NIS near 2" is a median with "no run lies inside the window", the CA window was not reached, and the consistency table is old-run and one-program → R3 |
| R11 The 83% needs its condition | **Resolved** | Abstract: "behind leads that brake to a stop but costs progress behind"; 105 runs behind three kinds of non-braking lead |
| R12 The 12% needs its two assumptions | **Resolved** | Section V-D: "a perfect, free stop independent of perception"; terciles 0.055 to 0.168; delayed stop; closed loop replaces the assumption |
| R13 Update rate and latency | **Resolved** | Table S16: 2, 5 and 10 Hz at 0, 0.1 and 0.2 s with room, after-stop room, N and CK3 shares. (The abstract wording falls short of the plan's own rule → R10) |

**The response letter.** Its R-item claims match the text. Two checks: the leaked label "Table S{deviations}" of the 02:51 letter is fixed at 03:03 ("Table S5"); the word counts in the letter (5,230; 8,467; 217; 11,966) match the 03:08 build report. I did not audit the 25 suggested items one by one. From what I read: v12 S22 is declared not run; v12 S7 (internal identifiers) is partly met, because "the coordinator" and process-log wording remain in Table S5; v12 S12 (decision-equivalents where shares do not grade) is partly met (R9).

## 5. Pre-registration: outcomes against Amendment 10 §9, and deviations against §11

I compared each outcome in `OUTCOMES_v13.json` with the text and with §9's wording rules.

| Outcome | §9 rule | Text | Verdict |
|---|---|---|---|
| H0 pass | room reported | "The oracle's room is 5.58 [4.99, 6.17] percentage points" | As ruled |
| H1 pass | "detects rank information at the tracker's amplitude" | Those words | As ruled. The rule's wording is the problem (R1) |
| H2 pass | "equivalent … within 5% of the room", confirmatory, with decision-equivalents | Abstract and Section VII have the sentence; decision-equivalents are in Section V-A only | As ruled in substance; the abstract omits the decision-equivalents |
| H3 amplitude-limited, flag "barely varies" | values said; title and contributions name the trackers | Abstract: "barely varies (99.7% …)", "recovers little of the room (0.0009)"; title names both trackers | As ruled. The oracle was renamed from "ceiling" to a reference, a recorded departure |
| H4 pass | schedule as "a diagnostic of where the room lies", with its cost | Section V-A has "a diagnostic"; the abstract gives 0.916 without that word | As ruled in the body; abstract shorter (S15) |
| H5 pass | most of the room, open loop, leads that brake to a stop; cost by D-H1 | Abstract: "most of the pooled room (0.783) behind leads that brake to a stop but costs progress" | As ruled (see R9 on "most") |
| K0 fail, F-H0 fail | "No measurable room in that data set. Nothing is tested there." | "showed no measurable room, so nothing was tested there" | As ruled |
| D-H1, D-H2 all "costs progress" | stated beside H5 and H4 in the abstract | Stated | As ruled (see R8 on what the label hides) |
| E-H1 safer at no extra cost; E-H2, E-H3 equivalent | classifications; null extends to closed loop; say which reading closed loop supports; replace "perfect, free stop" | All present | As ruled. The inference added to the "which reading" sentence fails on Table IV (R6) |
| B7: after-stop room at 10 Hz below half | text says "largely a consequence of the 2 Hz update"; **abstract gives magnitudes "at 2 Hz without latency" with the 10 Hz value** | Text: yes. Abstract: "Magnitudes depend on 2 Hz updates and the recording policy" | **Not as ruled, and not recorded as a departure** (R10) |
| B3/B4: thresholds not crossed | "the mechanism persists with NIS near 2 and with a CA filter" | Those words | As ruled (see R3 on "NIS near 2") |
| Always: no removal of a covariance margin; old-run numbers labelled; data statement on sweeps | — | All present | As ruled |

**Deviations (§11).** Table S5 lists the departures with their reasons, including the two-stage second lock, the real-log clearance change made after the design-split result, the three sources not computed on the real logs, four one-line fixes after the lock, and one deviation found afterwards. The real-log change is disclosed in four places (Section III-C, Table II, Limits, Supplement S10) with the planned outcome printed beside it. I found three gaps, all in reporting:
1. the B7 abstract wording above;
2. §10.1(d) asks for the file times "listed in the supplement"; Supplement S12 says they "are in the deposit's manifest";
3. §10.1(a) says a main-passage value without a second program is not printed there; Table V prints three old-evaluation values marked "(one program)" in its caption. This is disclosed in the caption but not in Table S5.

**Verification files.** The recount coverage file reports 205 of 205 values in the named passages with an agreeing second program; Supplement S12 says 207 of 207 for the main text, a count the v04 claim audit re-derived. The build report also says "printed values without an agreeing recount: 390 of 1383", while the coverage file marks 98 supplement values. I could not reconcile 390 with 98 from the files I read (S8).

## 6. Suggested items (S1–S15 of this review)

- **S1** · Sections IV-C, V-B · Amplitude-response curve: the ranking oracle's share against band width. New analysis, exploratory.
- **S2** · Section III-D, Supplement S4 · A multiple-model arm tuned for manoeuvres, or the present IMM's mode probabilities by phase. New analysis, descriptive.
- **S3** · Section III-E · An arm with the tracker's own predicted covariance over the look-ahead, and a "true current state, constant-velocity prediction" reference that splits the room into tracker lag and prediction-model error. New analysis.
- **S4** · Tables I, II, III · E5p's share with its interval, relabelled "no within-run information"; a permuted twin at the tracker's own spread and for the adaptive filter. New values.
- **S5** · Table IV · Closed-loop cost on all 60 pairs; each matched arm's design caution and scale; consider a level where the baseline has no contact. New values.
- **S6** · Table I, Section III-F · The time gap as a second baseline; the fallback share split into moving and standstill; say that F0 is the tracker's own mean. New values and wording.
- **S7** · Section IV-D, Table S9 · Interval type and stratification; estimated coverages; "coverage not established" for the 99% fallback; each interval quoted with its level; "classified" rather than "confirmed" for the IMM step.
- **S8** · Section IV-E, Supplement S12 · Call the second programs a recount on shared components; say whether an external timestamp of the plan hash exists; reconcile 390 with 98.
- **S9** · Supplement S4, S6.2; Table III · NIS by update rate; units for the tuned constants; define the lag column as the residual after the stop.
- **S10** · Limits · Name the function under test, the speed range (5 to 15 m/s) and the absent radar range rate; soften content claims about standards whose texts were not read; note that the braking prediction's 3 m/s² lies inside the generator's range; carry the vulnerable-road-user scope into the conclusion.
- **S11** · Figs. 2, 3; reference [3] · Explain why the IMM's curve lies above F0's in Fig. 2; show the rule bounds in Fig. 3. The LaTeX log reports reference [3] overflowing its column by 46 pt.
- **S12** · Abstract, Sections I, VII; Supplement · Remove the triple repetition; say "its own room" for the IMM; cut process-log wording; tell the editor about manuscript [10] in the cover letter.
- **S13** · References · DOI of [27], date of [38], a chapter for [25], an access date for [3]; cite the intelligent-vehicle threat-assessment work that the search found.
- **S14** · Section IV-A; Supplement S2 · Say that caution is averaged over an outcome-dependent set, and that matching by open-loop caution does not equalise closed-loop risk (Table S23: the two class averages differ twofold in contacts at the higher level).
- **S15** · Abstract; Section V-D; Supplement S12 · The plan's reporting details: file times in the supplement; "diagnostic" for the schedule in the abstract; "at point estimates" for the orderings (the tuning-run interval for CK3 is [−0.221, 0.864]).

**Questions from the seats** (not covered above): What are the IMM's mode probabilities during braking? How many closed-loop fallback decisions are at standstill? Did the 20 cut-in tuning runs already show no room and no young tracks before 105 runs were recorded? Why do partial oracles score below the class average inside each phase? Is there any timestamp of the plan hash outside the author's machine?

## 7. What would make submission unsafe

1. **The three author placeholders** and the template's own placeholders. With them open the Journal-Fit seat rates desk-rejection risk high.
2. **R1.** The abstract's detection claim is contradicted by the paper's own Table III. A referee finds this in minutes, and it is the sentence that the whole null leans on.
3. **R5.** A title that promises real driving logs over a Table II that says "n.t." in that column.
4. **R13, reference [15].** An AI-drafted description of a preprint whose title does not match it, in a paper that says "no full text was opened". If the description is wrong, it is a citation-integrity problem. Only the author can settle it.
5. **The AI-content statement.** It is candid and complete as a disclosure. But every step (text, code, second programs, audits, this review) is by models of one vendor, and the author's own verification is still blank.
6. **The deposit.** The Data and Code Availability section and Supplement S12 rely on a deposit and its file-time manifest that do not exist yet.
7. **The typeset PDF was not seen as pages** in this review. Someone should look at all 10 pages before upload.

Nothing I found suggests a wrong number, a hidden failure or an undisclosed change of analysis. The risks are in what the words claim.

## 8. Checks and files

- `check_author_letter.py` (run from inside `scripts\`, against the 03:08 manuscript): `AUTHOR-LETTER: PASS`, exit 0, first run.
- `review_panel_provenance.py`: `validate` PASS; `validate-carrier` PASS.
- `check_acronyms.py`: exit 0 (`work\acronym_check_v13.txt`).
- Quotation check: every quotation of the manuscript, supplement or plan in this file was searched for in the 03:08 files by script.

## 9. Plain-language summary (coffee shop)

Last time the tasters sent the cup back and asked for a fresh batch, tasted once with the rules written down first, and for one shot from a machine whose pressure varies. The café did all of it: new beans, sealed rules, a test at a real counter with customers (closed loop), a normal-size cup. Nobody at the table doubts the measurements now.

The complaint this time is the menu card. It says "also tasted with real-world beans", but those beans turned out to have no flavour to measure. It says "our spoon can detect a pinch this small", but the pinch tested was far bigger than the one the house bean actually varies by. It says the varying-pressure machine was tried, but that machine was set so that its pressure hardly moved, and the one machine that did vary, and did add a little flavour, is not on the card at all. And the note "the special syrup works at the counter because it knows what the customer wants" overlooks that plain sugar worked just as well.

So: about **four stars**, up from three and a half. No new batch is needed. Rewrite the menu card so that it says what was actually tasted, fill in the owner's name and signature, and it is ready to serve.
