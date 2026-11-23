# Phase 1, round 3, seat R1 (Peer Reviewer 1, Methodology): v13 package of 22 Nov 2026, 22:44

## 1. Header

- **Seat:** R1, Peer Reviewer 1 (Methodology). **Model:** Claude Fable 5.2 (`claude-fable-5-2`). The later text, including this revision, was written by a session on this same model. I therefore checked the printed values against the export files, the labels against the amendments, and the scope sentences against the coverage record, and did not rely on the text's or the letter's own account.
- **Card:** "Card 2: Peer Reviewer 1 (Methodology)" of `review_v13_output\00_phase0_field_analysis_and_cards.md`, identity unchanged. **Card-confirmation pause not held** (non-interactive run). `criteria_binding_unavailable`.
- **Brief:** `work\panel_brief_round3_v01.md`, SHA-256 dfd806d0a83fba1c6664dfb99de2ed72434c06eee13b81e69d5130a29c7b63e3 (matches the launch message).
- **Files reviewed, SHA-256 at start and at end (identical both times, equal to the brief's table):**

| File | SHA-256 (start = end) |
|---|---|
| `MANUSCRIPT_v13.md` | 04b6ca9e2c47fb34d0f9b09f980c8e6855e37ebfd0062368649a75636d3e2eb8 |
| `MANUSCRIPT_v13.tex` | 710a8366cb4aba07bbe8fd67084a38f217f2862cf6d8d8bfc0ebeb4c80f6df8d |
| `SUPPLEMENT_v13.md` | e99e2d807a0884af7e53866a69a4b5f7019741e1fa75902a5cfcf56fd2545eba |
| `MANUSCRIPT_v13.pdf` (not opened; page images used) | 93926a734b87ea1fb17117928edda98a2603d041b89afdc9521f1e8a5d650914 |
| `SUPPLEMENT_v13.pdf` (not opened) | ec81d45527801c11bd0ad4b06f91c94c44ef7c430b03235bf3ef1770f3b03f23 |

- **Read in full:** `MANUSCRIPT_v13.md`. **Read in part:** `SUPPLEMENT_v13.md` (outline; S12 "Second programs", the count paragraph, "Hand-checked decisions", "Claim audit", "Presubmission reviews"; S13 in full to Table S30; S1 and S3 by search); `MANUSCRIPT_v13.tex` (running head, [10]); `BUILD_REPORT_v13.md` (section word counts).
- **Read under "what you may read":** the round-3 brief; my card and the field analysis; my own round-2 report; `work\round2_record_sections_3_4.md`; `work\letter_section_round2.md`. The round-1 brief was not reopened (its standards are in my earlier reports).
- **Seat extra reads:** `AMENDMENT_10_v13.md`, `AMENDMENT_11_v13.md`, `AMENDMENT_12_v13.md`, `AMENDMENT_13_v13.md` by search (label rules, Holm lists, the twin, step 0; all four were read in round 1 or 2); the `LOCK_A11*`, `LOCK_A12a-e`, `LOCK_A13a-c` files listed, not reopened line by line (their contents were checked in round 2 and no label of this revision depends on a new reading of them); every `A_EXPORT_*`/`A_RECOUNT_*` pair of record in `B_retrack\out`, `CD_capture\out`, `E_closedloop\out`, `F_nuscenes\out` (19 pairs, compared key by key; `F_dropout\out` holds none), the old-run pairs `TESTOLD_A_EXPORT_C/D` and `TESTOLD_A_RECOUNT_C/D`, `shared\checks\step0_recount\A_RECOUNT_S0.json`, `shared\holm\A12_HOLM_v01.md` and `A13_HOLM_v01.md`, both result files in `shared\holm_recount\`, and `RECOUNT_COVERAGE_v13.md` of `freeze_v13_2244`.
- **Page images viewed:** manuscript pages 1, 8, 9, 10, 13, 14 (of 14); no supplement or template image this round.
- **Not done:** no web; no text sent anywhere; no sub-agent; no other seat's file opened; `AMENDMENT_14_v13_DRAFT.md`, `DERIVED_v13.json`, `OUTCOMES_v13.json`, `TEXT_FREEZE_v13.md`, the manifest and the full letter not opened; nothing changed outside this file. One light `python -I` process at a time (JSON comparisons only; my script is in the session scratchpad).
- Clock: start 22:58, end 23:03 EST, 22 Nov 2026.

## 2. Judgement

| Recommendation | Score | Stars | Most likely editorial outcome at OJ-ITS |
|---|---|---|---|
| **Minor revision** (two one-line wording items) | **7.4 / 10** | 3.5 of 5 | Major revision as the editor's first decision, on significance and length and not on any error; minor revision is the second most likely |

**Send as is, apart from the DOI? Yes.** No value, label or scope sentence that I could check is wrong: 190 printed values checked, 190 match, every one with an agreeing second-program value, and every label agrees with its amendment's rule. All nine items of the round-2 record are answered in the text; the author's three items read clearly and consistently. The two items I still call required are a clause in Section II and one count in Supplement S12; each takes a minute, neither changes a result, and a referee would return them as minor points. If one more build is made before submission, take them; I would not hold the submission for them. What keeps the score at 7.4 is what wording cannot change, and the paper states all of it: the confirmatory result was expected; every positive result comes from an amendment written after first results; the positive shares are 2% to 5% of a 5-point room and the one with a control is reproduced by a count; one in-house planner, one simulator; no decision-level evidence on real logs; 14 pages against a recommended ten. Against round 2 (6.9 as it stood, 7.2 conditional): the declaration now agrees with the deposited plans, the reading statement is in Section II, the twin's reach is stated where the twin is defined and wherever its result is summarized, the cross-set order rests on printed and recounted values, and the three long paragraphs are split.

## 3. The nine open items

Counts: **resolved 8, partly resolved 1, not resolved 0.**

| ID | Verdict | Evidence (22:44 text, location) | What remains |
|---|---|---|---|
| N-1 | **Resolved** | ACKNOWLEDGMENT ¶1: "made or approved every scientific decision, and reviewed and approved all content"; ¶3: "Where the amendment files record a design choice as an AI session's, it was made within the author's approval." The two sentences now agree with each other and with the deposited amendments (AMENDMENT_13 line 22 records a coordinator's rule; AMENDMENT_11 line 43 records the author's). | None. |
| N-5 | **Partly resolved** | II, "Novelty, with its limits": "The author read five of the 47 references in full ([13], [15], [19], [35], [36]); the others were read at abstract level, and every reference's record but that of the author's own manuscript [10] was checked against Crossref or its publisher's page (Supplement S13)." S13: "an AI system read the others at abstract level, except [4], [10], [41], [42], [43], [44], and [45]". The reading and its counts are in; what the author read is the author's fact and is stated clearly. | The main text's passive leaves out who read the other abstracts (S13: an AI system) and that seven sources were not read at abstract level. See Q-1. |
| N-20 (6) | **Resolved** | Byline (page 1): "ANANDA SIVA KUMAR KOPALLI NAGA VENKATA"; running head (pages 8, 10, 14; `.tex` line 50): "Kopalli: Tracker Covariances as Safety Margins in Motion Planning"; [10]: "A. S. K. Kopalli". One family-name form in the running head and in [10]; the full name on the first page. The author's choice, stated consistently. | Advisory: one line in the cover letter that [10] is by the same author. |
| P-1 | **Resolved** | Abstract: "In simulated tests of one speed planner predicting at constant velocity (straight road, 5 to 15 m/s)"; "With fixed noise and regular updates the covariance is nearly constant"; "beats its within-run permuted twin by 0.05 of the room (a timing effect)"; "Pedestrian crossing (open loop; room 0.16 points)". "And regular updates": I (¶ after Table 1; contribution 2), VI ¶1, VII. 235 words. Values checked (Section 5). | None. |
| P-2 | **Resolved** | IV-E is four paragraphs, V-C three, IV-C four, "Detection Dropouts" three; Table 4's class rule is note d. Build report: V-C 443 words over three paragraphs. | Section V-E is still 1,489 words; optional (length). |
| P-3 | **Resolved** | III-B: "Time lost is the assessed 30 s of a run (after 5 s of warm-up) minus the distance traveled in them divided by the desired speed, for runs without contact". V-C: "In these 60 cases the lead brakes to a stop and the ego ends the run behind it, so at the lower level every arm loses 24.5 to 24.8 s of the 30 assessed seconds (Section III-B), and the paired differences are below 1% of that"; "full braking is the planner's hardest row, taken as its fallback or as the first feasible row (Section III-E), and the share of decisions in which a margin source could change the row was not computed." The seven arm means are 24.48 to 24.78 s in both programs' exports; the largest paired difference is 0.17 s (0.7%). | None. |
| P-4 | **Resolved** | II: "with fixed noise the covariance is then a function of the arrival sequence and, for noise fixed in the object frame, the heading, so on a straight road a margin that counts missed updates should match it (Section V-E)". Agrees with VI: "follows the update schedule and the geometry". | None. |
| P-5 | **Resolved** | Table 5, "Recording policy": "NA share, same columns: 0.064 / 0.015 / 0.024"; "TG share: 0.182 / 0.321 / 0.287"; "AM share: 0.278 / 0.382 / 0.369"; V-D: "(point values rising: N, NA, TG, AM, CK3; Table 5)". All nine values match both programs' exports (`TU.RR_*`, the old-run pair's `LB.all.RR_*`, `LB.all.RR_*`), and the order holds in each column. | S12's count of old-run values did not follow: Q-2. |
| P-6 | **Resolved** | IV-C: "Because the permutation is within runs, a positive difference shows that the margins' timing matters; it cannot separate ranking among decisions from a *level effect* ... that follows the lead's phase. Only the dropout test had a control for such an effect, the coast-count margin (Section V-E)." Abstract: "(a timing effect)". VII: "only the dropout gain had a control that separates ranking from level, and at 2 Hz a margin counting missed updates reproduces it." | None. |

## 4. Findings

Types: **W** wording; **M** a value or fact moved in from the supplement; **T** text the author writes from existing records; **A** new analysis. No finding is CRITICAL. None is type A.

### 4.1 REQUIRED-major (0)

None.

### 4.2 REQUIRED-minor (2; both new)

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| Q-1 (remainder of N-5) | Section II, "Novelty, with its limits"; against S13 | The main text does not say who read the other references, and reads as if the author did; the supplement says an AI system did, and that seven sources were not read at abstract level. The Acknowledgment sends the reader to this sentence ("Section II states what the author read in full"), so it is the paper's reading declaration and should say the same as S13. | II: "the others were read at abstract level"; S13: "an AI system read the others at abstract level, except [4], [10], [41], [42], [43], [44], and [45]" | "an AI system read the others at abstract level, except seven cited by identifier or page (Supplement S13)". | W |
| Q-2 (regression, from the P-5 fix) | Supplement S12, the count paragraph; `RECOUNT_COVERAGE_v13.md` | The count of old-run values is the one from before Table 5 gained its three rows. Table 5 now prints six old-run values (5.51, −0.0004, 0.015, 0.321, 0.382, 0.837), and the abstract and Section VII print "84%". I could not run the counting program, so the "4" may follow a rule the sentence does not state; as printed it does not agree with the table. The total (418 of 418) is consistent with nine values added since round 2 (409). | S12: "418 of 418 result values printed in the main text (... 4 of them the old-run values of Table 5, recomputed)"; coverage record: "Of them 416 are in Sections III to VII, 4 the old-run values (second program: the stored-run recount)." | Recount the old-run values and print the number, or say which four are meant. | T |

### 4.3 OPTIONAL (11; 5 carried, 6 new)

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| P-4r2 (my round-2 P-4, carried) | `RECOUNT_COVERAGE_v13.md` (deposit record) | The counts support the paper (413 of 413 in the named passages; 418 of 418 over the whole main text, equal to S12; 164 supplement results, 188 marks, which I counted in the supplement). The labels are still the old ones: Roman table numbers, "TABLE V." for what is Table 6, no line for Table 5, no per-passage line for Sections II to IV. | "Named passages: Abstract, Sections I and V-VII, Tables II-V, figure captions"; "TABLE V.: 83 value placeholders; typed constants: 0.05, 0.1, 0.10, 0.20, 0.30, 10, 16, 95, 99" | Regenerate with the paper's labels and one line per section and table. | T |
| Q-3 | Section I, last paragraph | "Two tuning diagnostics computed by one program" names the two that the main text cites in words; the supplement holds 164 results computed by one program. A reader may take "two" as the whole of it. Section IV-E's sentence is exact. | I: "the supplement holds the configuration, the plans, the full tables, the verification record, and two tuning diagnostics computed by one program"; coverage record: "164 result values without an agreeing second program" | "and values computed by one program (marked ‡), among them two tuning diagnostics cited here". | W |
| Q-4 | V-E, "Pedestrian Crossing", first sentence; Table 6 row 1 | "(exploratory)" can be read as the status of step 0 or of the crossing test; the test's row carries "(A)". The amendment says the step-0 values are exploratory and the crossing test a departure by the author. | "was tested despite the prestated no-go of step 0 (exploratory)"; Table 6: "uninformative variation (A)"; AMENDMENT_11 line 46: "Step-0 values are exploratory (stored runs)." | "despite the prestated no-go of step 0, whose values are exploratory". | W |
| Q-5 | Table 6, first-amendment closed-loop row | The label has no status, although the amendment lists the lower-level class as a hypothesis (`E4H1`). Round-2 record: "Row status label: optional". | "equivalent"; AMENDMENT_11 line 502: "**Hypotheses:** `E4H1`, `E4H2` (the lo classes)." | "equivalent (A)", or one word on why not. | W |
| Q-6 | V-C, second paragraph | The arms' mean time lost is taken over each arm's own runs without contact (48 of 60 for the class average, 60 of 60 for the braking prediction), so the range 24.5 to 24.8 s is over different case sets; the paired differences are not. | "every arm loses 24.5 to 24.8 s of the 30 assessed seconds" | "(each arm's mean over its own runs without contact)". | W |
| Q-7 | Response letter, round-2 section | The prose and the table disagree on where "level effect" is defined. The paper defines it in IV-C. | Prose: "defined in Section IV-C, where it is first used, and no longer in Section V-E"; table row "Optional": "defined at its first use in Section V-E" | Correct the table row. | T |
| P-10 (carried) | Abstract; VII | "38% to 84% across run sets" are point values; the 38% is 20 tuning runs with interval [−0.22, 0.86] (`TU.RR_CK3.ci`, both programs). | "78% of the room (38% to 84% across run sets)" | "point values of 38% to 84%". | W |
| P-11 (carried) | V-E, coast-count factors | The text still does not say that the factors multiply the class average's critical scale, so that 0.216 means a wider margin. | "its factors (0.216, 0.107, and 0.065 ...) are the median ratios of the covariance margin's critical scale to the class average's" | Add "a factor below 1 widens the margin". | W |
| P-9 (carried) | V-E, closed loop with dropouts | The equal-time-lost comparison takes contact share over 135 cases and time lost over the 89 without contact in any arm; stated, not named as a limit. | "time lost is taken over the 89 of 135 cases without contact in any arm" | "(a limit: the two axes use different case sets)". | W |
| P-8 (carried) | Table 6 row labels | Decision counts absent; 5,085 in-dropout decisions of 29,926 (`DR2.n_in_dropout`, `DR2.n_dec`) show how thin the dropout population is. | S15 holds them. | Add to the row labels. | M |
| P-12 (carried) | Page 14; length | The last page is one column of references and an empty right column; 14 pages against a recommended ten; V-E 1,489 words. Advisory. | Page image 14; build report "E. Where the Covariance Varies: 1489" | Balance the last page; cut only if the editor asks. | W |

## 5. Q1 to Q8: what changed since my round-2 report

**Q1. Labels and sizes.** No label changed in status. I checked each against its rule again:

| Label in the text | Rule or record | Agrees |
|---|---|---|
| Lead-braking room, detection, equivalence, IMM class, schedule transfer, braking prediction: "confirmed" | Original sequence; exports `LB.*` with calibrated levels | yes |
| Pedestrian crossing "uninformative variation (A)" | `X.PC.X0`, `X1`, `X2.confirmed` true; class as exported; oracle interval nominal 99% | yes |
| Dropouts "recovers (A)"; new runs "replicated, H 0.0079"; slope "(A), H 0.0079" | `DR.RR_N.ci` above 0; `DR2.DR2.passes`; `DR2.slope.passes`; A12 Holm table, one convention | yes |
| Coast-count "failed, Holm 0.99" | AMENDMENT_13 §3.5; `DRF.status` "failed (amendment)"; p 0.9856 | yes |
| Two-noise IMM "recovers (A), H 0.0003" | `B.IMM2N.class`; Holm table | yes |
| Adaptive filter's twin "(A), post hoc; replicated, H 0.0003" | AMENDMENT_11 line 159 (specified after fresh values were seen); `Y.Y1`, `YN.Y1` | yes |
| Closed loop with dropouts "(A), H 0.0003"; equal time lost "failed, Holm 0.18" | `E5.dc.ci` below 0; AMENDMENT_13 line 23 (label from the two-sided interval; Holm changes no label); `E6.delta.ci` [−0.121, 0.022]; p 0.0878, doubled | yes |
| nuScenes mechanism "(A), H 0.0003"; all pairs and IMM "descriptive" | AMENDMENT_12 lines 408 and 490; `M.passes` | yes |
| "The second amendment's six primary hypotheses stay significant ...; the third amendment's two fail under their own Holm adjustment as well (adjusted p 0.99 and 0.18)" | `A12_HOLM_v01.md` (m = 6), `A13_HOLM_v01.md` (m = 2), and both second-program result files (`exports_agree` true throughout) | yes |

*Value check.* I checked **190 printed values** against the first-program exports (a point with its interval counted once): **190 match** at the printed rounding. **188** have an agreeing second-program value in my own key-by-key comparison of the 19 export pairs, the old-run pair and the two Holm recounts (no result value differs in any current pair; the differences are file metadata and NaN entries that are NaN in both). **The other 2** (step 0: 51 runs; 0.08 [−0.06, 0.25]) I compared with the second program's file `A_RECOUNT_S0.json` only, which holds them. **No one-program value is printed in the main text**; the two one-program diagnostics are given in words and say so (III-D "computed by one program"; V-E "computed by one program, are in Supplement S15").

Every value this revision changed or added:

| Item | Printed | Export key (pair) | Match | Second program |
|---|---|---|---|---|
| Abstract, the twin's difference | "0.05 of the room" | `Y.delta` 0.0498; `YN.delta` 0.0508 (Y, YN) | yes | agrees |
| Abstract, pedestrian room | "room 0.16 points" | `X.PC.R` 0.1618 (X) | yes | agrees |
| V-C, time every arm loses | "24.5 to 24.8 s" | `E3.<arm>.lo.tlost`: 24.48 to 24.78 over seven arms (E) | yes (2) | agrees |
| V-C, "below 1% of that" | paired differences | largest `E3.<arm>.lo.dt` 0.165 s, 0.7% | yes | agrees |
| V-C, full braking | 52.7%; 78.6%; 1.6% | `E3.F0.lo.fallback`, `E3.F0.hi.fallback`, `E3.CK3.lo.fallback` | yes (3) | agrees |
| V-C, peaks and time | 6.17; 4.31; 0.16 s | `E3.F0.lo.peakdec`, `E3.CK3.lo.peakdec`, `E3.CK3.lo.dt` | yes (3) | agrees |
| Table 5, NA / TG / AM rows | 0.064 / 0.015 / 0.024; 0.182 / 0.321 / 0.287; 0.278 / 0.382 / 0.369 | `TU.RR_NA`, `TU.RR_TG`, `TU.RR_AM` (B); old-run pair `LB.all.RR_NA`, `RR_TG`, `RR_AM`; `LB.all.RR_*` (C) | yes (9) | agrees. In the old-run recount the structured copy `TRANSFER.structured.per_set.old.TG` is empty, but its value of record `LB.all.RR_TG` (0.3212) is there and agrees |
| Table 5, room, N and CK3 rows; "38% to 84%" | 1.16 / 5.51 / 5.58; 0.0000 / −0.0004 / 0.0000; 0.379 / 0.837 / 0.783 | `TU.R`, `TU.RR_N`, `TU.RR_CK3`; old-run `LB.all.*`; `LB.all.*` | yes (11) | agrees |

The other 159, all matching and all recounted except the two step-0 values noted above: Table 4, six rows in full (31); V-C behind nonbraking leads (8); V-E closed loop with dropouts and Table 6's four closed-loop rows (23); dropouts, coast count, 10 Hz (22); the eight Holm values; the two-noise IMM in Table 6, Table 3 and the mode probabilities (13); the twin's two rows (2); pedestrian crossing and its decomposition (11); nuScenes mechanism check, the injected-dropout room, 6,122, scene and decision counts (10); step 0 (2); V-A and V-D with Table 5's other rows (29).

*Recount-scope sentences against `RECOUNT_COVERAGE`.* Section IV-E and S12 use one sentence ("recount every result value printed in the main text and all but the marked (‡) values of the supplement"). The record supports it: 413 of 413 in its named passages; 418 of 418 over the whole main text, and S12 prints 418; 164 supplement results under 188 marks, and the supplement has 188 marks. The shared library, arrays and draws, and the 20 hand-checked decisions, are in the main text. Two things do not line up: the count of old-run values (Q-2) and the record's labels (P-4r2). Section I's "two tuning diagnostics" is narrower than the record (Q-3).

**Q2. Overreach.** None new. The abstract's first sentence is now scoped to one planner; the twin's result is called "a timing effect" in the abstract and has its limit in IV-C and VII; contribution 2 says "small gains of 2% to 5% of the room as point values". One soft spot carried: "38% to 84%" without "point values" (P-10).

**Q3. Earlier limits.** Unchanged in substance, as expected of a text-only revision, and all stated: an expected confirmatory result, post hoc amendments, small effects, one planner and simulator, no decision-level real-log evidence. The process limit that was open (N-1) is closed.

**Q4. Readability.** Better. The three long paragraphs are split; the abstract's pronoun has its noun; the time-lost sentence can be read from the main text alone. V-E remains dense (1,489 words; Table 6 with up to four intervals in a cell).

**Q5. Verdict.** Section 2. Minor revision from this seat; no required item is of substance.

**Q6. Self-containment.** The one case I raised in round 2 (the run length) is closed by III-B and V-C. The cross-set order now rests on Table 5. I found no claim that needs the supplement to be read.

**Q7. Format and declarations.** The surname form is settled as the author chose (byline in full, "Kopalli" in the running head and in [10]). ACK order, table notes and panel labels as in round 2. Page 14 still has an empty right column (advisory).

**Q8. AI disclosure.** Sentence 1 now reads "made or approved"; the panels are "Claude models, among them these three"; S12 counts nine reviews and names the models of the audits, including that the last wording changes were not audited further (stated in the letter section I was given). The one gap is that Section II does not name the AI system as the reader of the other abstracts, while S13 does (Q-1).
