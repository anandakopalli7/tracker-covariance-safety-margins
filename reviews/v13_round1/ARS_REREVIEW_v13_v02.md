# Re-review of v13 after the wording pass (verification of R1–R14)

**Time stamp:** 2026-11-21 03:50 −05:00 (local clock).

**Freeze verified:** 03:41:14, in `revision_v13\work\A_text\out\freeze_v13\`. I recomputed the hashes: PDF 2d6ebeee, TeX 99ad44b1, manuscript `.md` a5939bc1, supplement 0d27a140, response letter b5ee0d4d. All five match the coordinator's table.

**How this was done.** A single-pass verification by the synthesizing session (Claude Fable 5.2), not a new five-seat panel and not the skill's three-gate re-review contract. I read the new manuscript in full (title to acknowledgment), every changed supplement line, the reference changes, the build report, the recount coverage file, A's account in `STATUS.md` and `notes\AUTHOR_ITEMS_v13.md`. I did not re-audit values; I checked the numbers that are new or moved in the abstract. No external service was used. Nothing outside `review_v13_output\` was written. The PDF was again not seen as pages (no renderer); the LaTeX log gives 10 pages.

## 1. Result

| Status | Count | Items |
|---|---|---|
| Resolved | 10 | R1, R2, R4, R6, R7, R8, R10, R11, R12, R14 |
| Partly | 4 | R3, R5, R9, R13 |
| Not resolved | 0 | — |

**Updated rating: about 4.5 stars** (03:08 freeze: about 4; v12: about 3.5).

**Readiness: ready to submit once the author's own items are done** (title choice, reference [15] read in full, references [37] and [38], the three placeholders, a look at the 10 PDF pages) **and three small wording residues are fixed** (Section 3, items A1 to A3). Nothing that remains needs a value or a run. If this text went to the same panel, I would expect Minor Revision; that is my judgement, not a panel result.

The validated critical issue of the first review (C1, the detection claim) is repaired: the false statement is gone from the abstract, the contributions, Section V-A and the conclusion, and the departure from the plan's wording is recorded.

## 2. R1–R14 on the 03:41 files

| Item | Status | Evidence (03:41 text) | What is left |
|---|---|---|---|
| R1 Detection claim at ±5% | **Resolved** | Abstract: "the score detects rank information in a ±5% band"; Section V-A: "the tracker of record is amplitude-limited, like the IMM"; Table S5 row "Wording of the detection result (lead braking)" | Nothing required |
| R2 Equivalence was expected | **Resolved** | Section V-A: "as the constancy of its margin led one to expect"; Section VI: "what the test adds is the bound on the covariance's share" | Nothing |
| R3 The IMM as tuned | **Partly** | Abstract: "An interacting-multiple-model tracker as tuned here barely varies"; Section III-D: "so acceleration terms never reach the margin"; Section I now says "we also test other trackers' covariances" | Three labels still say the opposite: the heading "B. Trackers Whose Covariance Varies", the Table II row "Varying covariance: share $r$", and the Table III row "CV filter, re-tuned (NIS near 2)". The title still names IMM covariances as a class (author's choice, with R5) |
| R4 Adaptive filter in abstract and conclusion | **Resolved** | Abstract: "a filter with adaptive process noise recovers 4.6% of its room (descriptive)"; Section V-B: "it has no permuted twin" | Nothing |
| R5 Title and framing of cut-in and real logs | **Partly** | Scope: "neither showed room to test"; Limits: "The cut-in runs could not test young tracks" | The printed title is unchanged ("on Real Driving Logs"); three options are in `AUTHOR_ITEMS_v13.md`, and I agree with option 3. Section III-C still opens "The open-loop test is replicated on nuScenes" |
| R6 Closed-loop inference | **Resolved** | Section VI: "so the closed loop ranks none of them"; Section V-C gives the time gap, "which uses no information about the lead's motion" | Nothing |
| R7 Closed-loop regime and labels | **Resolved** | Section V-C: "the class average brakes fully in 52.7% of its decisions"; "within ±0.10 of contact share"; Abstract: "(0.16 s lost)" | The matching basis is still named two ways (Section III-B "there"; Table IV "design runs"). Not required |
| R8 "Costs progress" and stop-and-go | **Resolved** | Abstract and Section VII: "though both lower wrong goes behind stop-and-go leads" (Table V: −4.7 and −6.5 points) | Nothing |
| R9 Pooled share and grading rule | **Partly** | Section V-A: "The score's sensitivity is shown for the pooled population only"; the abstract says "78% of the pooled room"; 0.411 is no longer quoted as a share | Section V-A says "Supplement S5 gives frontier distances there", but Table S8 still prints shares, with the note "read shares as frontier distances". Either convert the cells or change the sentence |
| R10 Rate, latency, plan's abstract rule | **Resolved** | Section V-D: "the room is 5.58, 4.99 and 4.75 points at 2, 5 and 10 Hz"; Abstract: "Magnitudes are at 2 Hz without latency" with the 10 Hz value (45%; 77.8 / 173.4 = 0.449) | Nothing required (see B1) |
| R11 No road user behind the ego | **Resolved** | Scope: "No test bed scores traffic behind the ego or occupants' comfort"; Section III-C: "which turned 6,122 of the class average's design-split decisions from unsafe to safe" | Nothing |
| R12 Abstract readable alone | **Resolved** | The abstract opens with a 10-word question, defines the room in its second sentence and gives shares as percentages | "Equal caution", "binding rows" and "after-stop room" are still used undefined (B1). Not required |
| R13 Author acts and references | **Partly** | Section IV-E: "shaped this manuscript"; Table S5 now says "recorded in the decision log"; [27] has its DOI; the sentence on [15] was rewritten to "a pipeline that propagates perceptual uncertainty upstream generalised better" | Author only: read [15] in full (the new sentence rests on its abstract); check [26]; date or edition for [37] and [38]; complete the verification line; say who approved the post-lock changes |
| R14 Supplement and table defects | **Resolved** | Table S13 caption: "lies outside its percentile interval"; header bracket fixed; "n.c." now covers "undefined by its rule"; Section V-D defines the after-stop room; Table V caption: "recomputed on the gridless frontier and recounted"; Table S5 reconciles the 155 runs | Table S17 is still a table of "n.c." only. Not required |

## 3. What still has to change

**Wording, for session A (no value involved)**
- **A1 (R3).** Rename the Section V-B heading, the Table II row "Varying covariance" and the Table III row "re-tuned (NIS near 2)" so that they agree with "as tuned here" and with "median over tuning runs".
- **A2 (R5).** Section III-C: replace "The open-loop test is replicated on nuScenes" with wording that fits a test bed that showed no room.
- **A3 (R9).** Make Section V-A and Table S8 agree on whether the non-grading populations print shares or frontier distances.

**Author only**
- The title (R5; option 3 of `AUTHOR_ITEMS_v13.md` matches the confirmed scope).
- Reference [15] read in full; [26]; [37]; [38] (R13).
- Author block, repository and DOI, verification line; who approved the post-lock changes.
- A look at all 10 PDF pages.

## 4. The three pre-registration gaps and the 390-against-98 point

| Point | Status | Evidence |
|---|---|---|
| B7 rule: abstract to say "at 2 Hz without latency" with the 10 Hz value | **Closed** | Abstract: "Magnitudes are at 2 Hz without latency; at 10 Hz and 0.1 s latency the after-stop room is 45% of that" |
| §10.1(d): file times listed in the supplement | **Closed** | Supplement S12, Table S29 "Order of work", with last-modified times and hash ends, generated from the files. The plan, both lock stages and the first lock carry the hashes I verified earlier |
| §10.1(a): Table V's one-program old-run values | **Closed, on A's account** | Table V caption: "recomputed on the gridless frontier and recounted". The coverage file reports 217 of 217 values in the named passages with an agreeing second program. I did not open the recount file itself |
| 390 against 98 | **Mostly reconciled** | The build report now reads "printed result values without an agreeing second program: 160 of 1165 results … 161 marks printed; text records registered but not results: 318". I count 161 "‡" in the supplement. But `RECOUNT_COVERAGE_v13.md` still says "98 without an agreeing second program", and 160 results stand against 161 marks. One line in either file would settle it |

One observation on the order-of-work table, for the author's record: Table S29 gives the first lock as modified at 14:05 on 19 Nov, which is the file's time on disk (14:05:39, the same second as the plan). The lock file's own note says its hash was "rewritten at 14:12 EST after fixing two path typos". The two times do not agree. The hash in the lock does match the plan as it stands, so nothing substantive follows, but an outside reader of the deposit may ask.

## 5. What the pass broke or newly overstated

I found no number that moved wrongly. The new abstract values agree with the tables: 0.01% (0.0001), [−0.09%, 0.15%], 99.7%, 4.6% (0.0459), 78% (0.783), 92% (0.916), 0.16 s, 45%. These are new, minor points.

- **B1. Abstract, last result sentence.** "the after-stop room is 45% of that" has no antecedent: the abstract never introduces the after-stop room or its 2 Hz value, and "Magnitudes" in the first half means all of them. Suggested: say that the room after the lead's stop falls to 45% of its 2 Hz value.
- **B2. Abstract, closed-loop sentence.** "the prediction, like the time gap, is safer at no extra cost by the plan's rule (0.16 s lost)" reads as if both lost 0.16 s. The time gap gained 0.13 s (Table IV).
- **B3. Plan wording for the equivalence.** The plan's rule for this outcome asks the abstract to say "within 5% of the room". The new abstract and conclusion give the tighter observed bound and drop the margin; it remains in Section V-A. This is a second small departure toward a more informative statement. Either add the margin in three words or extend the Table S5 row that records the detection wording.
- **B4. Section VI, last sentence of "Which commitment applies".** The paper asks that a score "show that it detects information at the tested output's amplitude". By its own Table III this paper showed detection in a ±5% band and not at the tracker's own spread (own-spread oracle 0.0001 [0.0000, 0.0002], no permuted twin). One clause of candour would close the loop.
- **B5. Section VI.** "decides between neither open-loop commitment" is ungrammatical; "does not decide between the two open-loop commitments".
- **B6. Response letter.** Its summary item 2 still says the oracle orders decisions "within the tracker's own amplitude" and tests detection of "information that small"; its R5 response still says "where it fails, decision-equivalents replace shares", which Table S8 does not do. The letter's R5 result paragraph is correct.
- **B7. Reference [15].** The old description is gone, which removes the risk I flagged. The new sentence is still taken from an abstract, so it stays an author item until the paper is read.
- **B8. No headroom.** Abstract 219 of 220 words, body 5,288 of 5,300, whole manuscript 8,493 of 8,500. Any further addition (A1 to A3, B1 to B5) must be paid for by a cut. The log still gives 10 pages; the 46 pt overflow of reference [3] is gone, and nine overfull boxes of at most 1.7 pt remain.

## 6. Limits of this verification

- One reviewer on one model (Fable 5.2), which is also the model of v13's claim audits. It is not a second panel.
- I checked wording against my 14 items and the new abstract numbers against the tables. The Sonnet recount and the Fable claim audit that are running separately cover the values.
- The suggested items S1 to S15 of the first review were not re-checked one by one. From the text I read: S11's reference overflow and S13's DOI for [27] are done; the new analyses (S1 to S6) were not run, as expected for a wording pass.
