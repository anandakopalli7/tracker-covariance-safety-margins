# Phase 1 report, round 3: seat 05, Devil's Advocate (package v13 of 22 Nov 2026, 22:44)

## 1. Header

- **Seat:** 05, Devil's Advocate (fixed seat). **Card:** none.
- **Model:** Claude Fable 5.2 (`claude-fable-5-2`). The revision under review was written by a session on this same model. Its new sentences were therefore checked against the tables, the supplement and the amendment files and not taken on trust.
- **Card-confirmation pause not held.**
- **Brief:** `work\panel_brief_round3_v01.md`, SHA-256 dfd806d0a83fba1c6664dfb99de2ed72434c06eee13b81e69d5130a29c7b63e3 (as named in the launch message).
- **Skill:** not loaded; the round-1 standards (Q1 to Q8) were applied as in my round-2 report. One seat only; no sub-agents; no web; no text sent anywhere. One light `python -I` call (a row count of Table S5: 60 rows, as Section IV-E says).
- **Clock:** started 22:58 EST, written 23:02 EST (system clock).

**Files and SHA-256, at start and at end (identical both times):**

| File | SHA-256 | Read |
|---|---|---|
| `MANUSCRIPT_v13.md` | 04b6ca9e2c47fb34d0f9b09f980c8e6855e37ebfd0062368649a75636d3e2eb8 | in full, every section, table, caption and reference |
| `MANUSCRIPT_v13.tex` | 710a8366cb4aba07bbe8fd67084a38f217f2862cf6d8d8bfc0ebeb4c80f6df8d | front matter, running head, float list |
| `SUPPLEMENT_v13.md` | e99e2d807a0884af7e53866a69a4b5f7019741e1fa75902a5cfcf56fd2545eba | S1 (configuration rows), S5 (Table S5 rows on the closed loop and the tuning runs), S6.2 (Table S16), S9 (Tables S21 to S23), S12 (presubmission reviews), S13 in full, S15 overview |
| `MANUSCRIPT_v13.pdf` | 93926a734b87ea1fb17117928edda98a2603d041b89afdc9521f1e8a5d650914 | hash only |
| `SUPPLEMENT_v13.pdf` | ec81d45527801c11bd0ad4b06f91c94c44ef7c430b03235bf3ef1770f3b03f23 | hash only |
| `AMENDMENT_11_v13.md` | b33d8281848c9bf1fbe47a706adbba8e0e063dc4d7480f3fe6fd95e8bb677cf3 | same hash as in rounds 1 and 2; searched again for the approval records |
| `AMENDMENT_12_v13.md` | a9911f1222b5fa386c28d39b2f3816cb3e0ec00d0eb4c4d082a58dc8d4ac0e42 | same |
| `AMENDMENT_13_v13.md` | bc7c2bf47c9a29810aa84c5dd4827a0f2d9404f9b684a94d0a918967180498bf | same; "Whose decision: the coordinator's" is still at line 197 |

**Pages viewed (PNG):** manuscript `page01`, `page02`, `page03`, `page07`, `page08`, `page09`, `page10`, `page11`, `page12`, `page13`, `page14`; all eleven hashes are in `work\pages_sha256.txt`. Not viewed: `page04` to `page06`, the supplement pages, the template pages.

**Also read:** my own round-2 report; `work\round2_record_sections_3_4.md`; `work\letter_section_round2.md`; `BUILD_REPORT_v13.md` of `freeze_v13_2244` (word counts). **Not read:** any other seat's report from any round, the full response letter, the manifest, session notes, the draft fourth amendment, `TEXT_FREEZE`, `RECOUNT_COVERAGE`, `DERIVED`, `OUTCOMES`, the failed public copy.

## 2. Judgement

| Recommendation | Score | Stars | Send as is (apart from the DOI)? |
|---|---|---|---|
| **minor revision** | **6.7 / 10** | 3.5 of 5 | **No, not quite.** Five sentences first; no new analysis. |

No finding is marked CRITICAL. No finding is REQUIRED-major.

**Most likely editorial outcome at OJ-ITS.** About one chance in four of a return without review (the AI disclosure, 14 pages, and now a main-text sentence that says the author read five of 47 references in full). If it goes to referees, the most likely first decision is major revision: referees will ask for decision-level evidence on real logs or for the covariance on top of the braking prediction, which the paper names as next steps. Acceptance without changes is unlikely. Rejection on the grounds of honesty or of wrong values is unlikely: I found no wrong value and no hidden limit.

**Why not as is.** The three author items are settled and all six P items were acted on. What withholds "accept as is" is small and all of it is wording. (1) The new reading sentence in Section II says the other 42 references "were read at abstract level"; Supplement S13 says that an AI system read them and that seven were not read even at that level. This is a statement about the author's conduct, and the main text and the supplement should say the same thing. (2) Section V-D and Section VI say two statements hold "in every run set", while Section III-A now lists six run sets and Table 6 prints a covariance share on one of them (pedestrian crossing) whose interval is not inside the equivalence margin. (3) Contribution 2 and Section VII present "2% to 5%" and "a few percent ... against its own class average" as test results for all three trackers; for the adaptive filter the share against its class average was never tested. (4) Section V-C offers the full-braking share as a cost to occupants and following traffic, while the same paragraph shows that the ego stands for about four fifths of the assessed time. (5) No sentence says that trackers were never compared with one another in absolute terms, although Table 3 shows that the retuned filters start from a larger braking room and a longer lag. Each fix is one clause. The body has 24 words of room under the project's own limit, so each needs a cut elsewhere.

### The strongest case against sending this text as it is

1. **Significance, unchanged.** No evidence was added in this round or the last. The one confirmed covariance result could hardly have failed. Every positive effect is an amendment test written after results, at 2% to 5% of the room, against each tracker's own class average. Both controls that would give the dropout gain meaning failed. The paper says all of this, in the abstract's last sentence and in Sections VI and VII.
2. **The closed loop measures little, and the revision now shows why.** Section V-C says every arm loses 24.5 to 24.8 s of 30 assessed seconds, so the ego is standing behind a stopped lead for about four fifths of the window. The class average is in full braking in 52.7% and 78.6% of its decisions. The text now says the share of decisions in which a margin source could change the row "was not computed". A hostile reader concludes that the closed-loop equivalence within ±0.10 at a 20% contact rate, on 60 cases, is close to automatic. The paper answers with "with 60 cases per arm contact differences much below 0.10 cannot be resolved" and "Equivalent here does not mean safe." That is a fair answer; the remaining gap is finding P-3 below.
3. **"Where it varies it recovers" still reads as a recommendation for adaptive filters.** The abstract, contribution 2 and Section VII each say "against its own class average". None says that the adaptive filter is built on a retuned filter whose braking room is 29.5 points against 23.6 and whose lag is 2.48 m against 1.42 m (Table 3). A share of a larger room against a weaker baseline is not a gain for a designer who already has the tracker of record (Q-3).
4. **Scope words that are wider than the tables** (Q-1, Q-2 below).
5. **Desk grounds.** (a) The AI disclosure is now consistent with the amendment files ("made or approved"), 367 words in four paragraphs, and it is complete; an editor who rejects on it rejects the fact, not the wording. (b) The new sentence "The author read five of the 47 references in full" is honest and is the most exposed sentence in the paper. (c) Fourteen pages; the last is about 40% empty. (d) "Preregistered" in the title against "internal locks, not a public registry" in Section IV-E; the title is the author's, and the abstract says "hash-locked internally". (e) Three amendments "written and locked on Nov. 21 and 22, 2026", each after an AI panel's report, with reference [4] accessed on Nov. 22, 2026: the record shows a paper finished in the two days before submission.

### How much of that case survives the paper's own disclosures

- **Point 1** survives in full as an objection to significance and not at all as an objection to honesty. It is a referee's question, not a defect of the text.
- **Point 2** is mostly answered. One clause is missing (P-3).
- **Point 3** survives in the three summary places. The body does not claim more, but it does not say what was not compared.
- **Point 4** survives; two clauses repair it.
- **Point 5** cannot be answered by the paper except for (b), where the main text should match S13 (N-5).

## 3. The nine open items

| ID | Verdict | Evidence (22:44 text) | What remains |
|---|---|---|---|
| N-1 | **resolved** | ACKNOWLEDGMENT, paragraph 1: "made or approved every scientific decision". Paragraph 3: "Where the amendment files record a design choice as an AI session's, it was made within the author's approval." | None. Amendment 13, line 197, "Whose decision: the coordinator's", is now covered by "approved". |
| N-5 | **partly resolved** | II, "Novelty, with its limits": "The author read five of the 47 references in full ([13], [15], [19], [35], [36]); the others were read at abstract level, and every reference's record but that of the author's own manuscript [10] was checked against Crossref or its publisher's page (Supplement S13)." S13: "an AI system read the others at abstract level, except [4], [10], [41], [42], [43], [44], and [45]". | The main text does not say who read the others, and it says all 42 were read at abstract level; S13 says an AI system did and that seven were not. One clause. |
| N-20 (6) | **resolved** | `.tex`: `\markboth{...}{Kopalli}`; `page02` running head "Kopalli: Tracker Covariances as Safety Margins in Motion Planning"; [10] "A. S. K. Kopalli"; byline "ANANDA SIVA KUMAR KOPALLI NAGA VENKATA" (`page01`). | None required. Advisory: the family name sits inside the full name, so the author should mark "Kopalli" as the family name in the submission system. |
| P-1 | **resolved** | Abstract: "In simulated tests of one speed planner predicting at constant velocity (straight road, 5 to 15 m/s)"; "With fixed noise and regular updates the covariance is nearly constant"; "beats its within-run permuted twin by 0.05 of the room (a timing effect)"; "Pedestrian crossing (open loop; room 0.16 points)". "And regular updates" stands in I (three places), II, VI and VII. | Optional: "equivalent within ±0.10" has no unit in the abstract (O-3). |
| P-2 | **resolved** | IV-C three paragraphs, IV-E four, V-C three, "Detection Dropouts" three (`page10`, `page11`); Table 4's class rule is note d (`page09`). | None. |
| P-3 | **partly resolved** | III-B: "Time lost is the assessed 30 s of a run (after 5 s of warm-up) minus the distance traveled in them divided by the desired speed". V-C: "the lead brakes to a stop and the ego ends the run behind it, so at the lower level every arm loses 24.5 to 24.8 s of the 30 assessed seconds"; "the share of decisions in which a margin source could change the row was not computed". | The same paragraph still reads full braking as a cost: "Table 4 shows where unscored cost to following traffic and occupants would fall (full braking and peak deceleration)". It does not say whether decisions at standstill count; Table S23 heads the column "Fallback". See the findings. |
| P-4 | **resolved** | II: "with fixed noise the covariance is then a function of the arrival sequence and, for noise fixed in the object frame, the heading, so on a straight road a margin that counts missed updates should match it". | None. |
| P-5 | **resolved** | Table 5, "Recording policy": "NA share, same columns 0.064 / 0.015 / 0.024"; "TG share 0.182 / 0.321 / 0.287"; "AM share 0.278 / 0.382 / 0.369". The order N, NA, TG, AM, CK3 holds in all three columns. | The sentence's reach ("in every run set") is a separate finding, Q-2. |
| P-6 | **resolved** | IV-C: "Because the permutation is within runs, a positive difference shows that the margins' timing matters; it cannot separate ranking among decisions from a *level effect* ... that follows the lead's phase. Only the dropout test had a control for such an effect". VII: "only the dropout gain had a control that separates ranking from level". | None. |

**Counts:** resolved 7 (N-1, N-20 (6), P-1, P-2, P-4, P-5, P-6); partly resolved 2 (N-5, P-3); not resolved 0.

## 4. Findings

Types: **W** wording; **M** a value moved in from the supplement; **T** text the author writes from existing records; **A** new analysis or evidence.

### REQUIRED-major (0)

None.

### REQUIRED-minor (5; 3 new)

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| N-5 (residual; regression) | II, "Novelty, with its limits"; S13 | The new reading sentence is in the passive and does not match S13. S13 names the reader (an AI system) and excepts seven references that were not read at abstract level. Among the 42 are a textbook [26], standards and regulations, a code repository [4], and [45], from which the paper takes its stop parameters. | II: "the others were read at abstract level". S13: "an AI system read the others at abstract level, except [4], [10], [41], [42], [43], [44], and [45]"; "The standards and regulations [42], [43], [41] are cited by identifier; their full texts were not read". | "an AI system read the others at abstract level, except seven without one (Supplement S13)". | W (author) |
| P-3 (residual) | V-C, paragraph 2; Table 4; Table S23 | Full braking is offered as an unscored cost to occupants and following traffic. The same paragraph shows the ego standing for about four fifths of the assessed window. The rest gaps (class average 3.57 m with 52.7%; braking prediction 4.83 m with 1.6%) suggest that most full-braking decisions are the fallback while the ego already stands, which costs nobody anything. The text does not say whether such decisions count. | "Table 4 shows where unscored cost to following traffic and occupants would fall (full braking and peak deceleration): against the class average's full braking in about half of its decisions"; S23 column head "Fallback". | Say whether decisions at standstill count. If they do, rest the cost sentence on peak deceleration only: "(peak deceleration; the full-braking share includes decisions at standstill)". | W |
| Q-1 | I, contribution 2; VII, sentence 3 | A label slip. "Later amendments' tests show small gains of 2% to 5% of the room as point values, each against the tracker's own class average" covers three trackers. For the adaptive filter the tested quantity is its share minus its twin's; its share against its class average (4.6%) is descriptive. The dropout values near 5% are descriptive too. The abstract has this right. | I: quoted above. VII: "(under detection dropouts, for a two-noise IMM, and for a noise-adaptive filter) it recovered a few percent of the room against its own class average". V-E: "Its fresh-run share is 4.6% (descriptive; Table 3)". Table 6: "new runs, share at start probability ... descriptive". | I: "gains of 2% to 3% of the room ... against the tracker's own class average, and an adaptive filter's 0.05 over its permuted twin". VII: "(the adaptive filter's share is descriptive)" or the abstract's own wording. | W |
| Q-2 | V-D, "Recording policy"; VI, "Limits" | "Every run set" is wider than the evidence. Section III-A lists six run sets. Table 5 shows three. On the pedestrian-crossing set the covariance's share is defined and its interval is not inside the equivalence margin. | V-D: "Only these statements hold in every run set where they are defined: the tracker covariance's share lies inside the equivalence margin". VI: "only Section V-D's cross-set statements hold in every run set". III-A: "Six run sets are used: tuning, old evaluation, fresh, new, pedestrian-crossing, and closed-loop." Table 6: "−0.067 [−0.221, 0.034]". | "in the three lead-braking run sets of Table 5" in both places. | W |
| Q-3 | VI, "Limits"; Table 3 | No tracker is compared with another in absolute wrong goes. The retuned filters, on which the adaptive filter is built, have a larger braking room and a longer lag than the tracker of record. A share against a tracker's own class average therefore does not show that the varying covariance leaves a designer better off than the tracker of record with a class average. I rated this optional in round 2 (O-2); on a full reading of Table 3 I would not accept without one sentence. | Table 3: "CV filter, online (of record) ... 1.63 / 23.62 / 0.08 ... 1.42"; "CV filter, retuned ... 1.71 / 29.52 / 0.07 ... 2.48"; "CV filter, adaptive process noise ... 1.97 / 28.34 / 0.07 ... 1.72". | One sentence in VI: "Each share is against that tracker's own class average; trackers were not compared with one another in absolute wrong goes, and the retuned filters' braking room is larger (Table 3)." Or compute the comparison from the existing arrays. | W (or A) |

### OPTIONAL (10)

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| O-1 (carried) | VI; VII | The test that would answer the significance objection is still a next step. | "whether a covariance adds anything on top of the braking prediction's path was not tested". | One more amendment test, labeled as such. | A |
| O-2 | III-A; Table 5 | The number of tuning runs is not in the main text. Table 5's tuning column rests on the 20 lead-braking tuning runs (S5, Table S5: "the 20 lead-braking tuning runs are among the 120 tuning runs"). | "Tuning runs, recorded with a small fixed margin, designed the margin sources and the trackers". | "(120 runs, 20 of them lead braking)". | M |
| O-3 | Abstract | "it is equivalent within ±0.10" has no unit. | Quoted. | "±0.10 of contact share". | W |
| O-4 | VI, "Which commitment applies" | "The two" has three nouns before it. | "the braking prediction, the time gap, and the per-phase schedule remove the contacts alike ..., so the closed loop does not decide between the two". | "between the two commitments". | W |
| O-5 | VII, sentence 1 | "Three things follow" is followed by four statements. | "For a designer, three things follow." | Drop the count. | W |
| O-6 | `page03`, right column | A stray space after the parenthesis. | "in full ( [13], [15], [19], [35], [36])". | Fix the citation spacing in the `.tex`. | W |
| O-7 (carried) | Fig. 2(a), `page07` | F0 is in the legend and cannot be seen under N. | Legend "F0". | Draw F0 dashed on top. | W |
| O-8 | S12, "Presubmission reviews"; S23 | "Nine reviews" will be out of date once this round counts. Table S23 heads its last column "Fallback" where its caption and Table 4 say "full braking". | S12: "Nine reviews by panels of five agents". | Update at submission; one name for the column. | T |
| O-9 | Table 3 | The adaptive filter's row has no class label, while both IMM rows carry "would classify as recovers (descriptive)". | "CV filter, adaptive process noise | 21.5% | 0.0459 [0.0390, 0.0533]". | Add the same label, or drop it from the IMM rows. | W |
| O-10 (carried) | Whole; front matter | Length: 14 pages, body 8,229 of the project's 8,253, tables and captions 2,746 words. Largely exploratory Section V-D with Table 5 and Fig. 4 is about a page. Title: "Preregistered" against "internal locks, not a public registry" (the author's choice). No biography (advisory). | Build report; IV-E. | The author's choice. | W |

**Counts:** REQUIRED-major 0; REQUIRED-minor 5 (3 new: Q-1, Q-2, Q-3; 2 residual: N-5, P-3); OPTIONAL 10. By type: all five REQUIRED are W. Marked "(regression)": the N-5 residual only (the sentence is new in this revision and does not match S13).

## 5. Q1 to Q8, briefly: what changed since my round-2 report

1. **Labels and sizes.** The abstract is now correct in every label I checked, and "(a timing effect)" and "(descriptive)" are in the right places. I recomputed the values that can be recomputed from the printed ones (1,204 decision-equivalents; −1.1 and 1.8; the contact differences of Tables 4 and 6; the interpolation to 25.7%; the slope; the order of sources in Table 5's three columns; the eight settings of Table S16; the 60 rows of Table S5) and all agree. Remaining: Q-1, where two summary sentences lag behind the abstract.
2. **Overreach.** The abstract's first sentence is scoped. New or newly seen: Q-2 ("every run set") and Q-3 (no absolute comparison across trackers).
3. **Earlier limits.** None removed. The twin's reach is now stated where the twin is defined, and Section VII says which gain had a control. The significance objection and the absence of decision-level evidence on real logs stand as before.
4. **Readability.** Better. The long paragraphs are split, "level effect" is defined at first use, and the abstract parses. The text is still dense: Section V-E has 1,489 words, and the body sits 24 words under the project's own limit.
5. **Verdict.** Round 2: major revision, 6.0 as it stood; minor revision, 6.6 under the three assumptions. Now: minor revision, 6.7. The assumptions were met and the P items were done; the small rise above 6.6 is for P-5 and P-6, and it stops there because the evidence is the same and I found five more sentences to mend.
6. **Self-contained main text.** The run length behind the time lost is given. One small gap is left (O-2, the number of tuning runs).
7. **Format and declarations.** The surname is settled in the running head and in [10]. The four closing paragraphs are in order. The repository bracket is the gate. New and advisory: the stray space on `page03`.
8. **AI disclosure.** Paragraph 1 no longer contradicts the amendment files. The disclosure is complete and names models, tasks, panels and audits. The new last sentence, "Section II states what the author read in full", points to the sentence that now needs the clause of N-5.
