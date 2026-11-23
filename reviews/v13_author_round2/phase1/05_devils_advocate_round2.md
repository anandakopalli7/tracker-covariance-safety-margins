# Phase 1 report, round 2: seat 05, Devil's Advocate (package v13 of 22 Nov 2026, 21:15)

## 1. Header

- **Seat:** 05, Devil's Advocate (fixed seat). **Card:** none. The field-analysis section of the Phase-0 file was read in round 1 and not reopened.
- **Model:** Claude Fable 5.2 (`claude-fable-5-2`). The revision under review was written by a session on this same model, so its new wording was checked against the tables, the supplement and the amendment files and not taken on trust.
- **Card-confirmation pause not held.**
- **Brief:** `work\panel_brief_round2_v01.md`, SHA-256 d4d0827044c96076ba2adefb90d9322ae27f96f6076de549f0260e19bf7c27b4 (checked).
- **Skill:** not loaded this round; the round-1 standards (questions 1 to 8 of the round-1 brief) were applied from my own round-1 report. One seat only; no sub-agents; no web; no text sent anywhere. One light `python -I` call (a word count of the abstract).
- **Clock:** started 21:25 EST, written 21:30 EST (system clock).

**Files and SHA-256, at start and at end (identical both times):**

| File | SHA-256 | Read |
|---|---|---|
| `MANUSCRIPT_v13.md` | c440adca7a70b2b74a373ee3a135d3eeac2c44a35ee6e28cb1c7280893d771b7 | in full |
| `MANUSCRIPT_v13.tex` | 8e9e648ef0290856f5c0dbdb841ebb2ecf0dea57cca6b8e2cc81749e856386ac | hash only; layout facts taken from the page images |
| `SUPPLEMENT_v13.md` | d18eee97e3f02f08159b1aaf81311a2663870818a42268dba706a1ba24d31b2b | Table S5 (slips row and amendment rows), S12 (second programs, hand check, claim audit, presubmission reviews), S13, and searches of S9, S14, S15 |
| `MANUSCRIPT_v13.pdf` | dc83ce17a652e734399f84005631649fe3801b936a589499a9ed1f0f68a51ccb | hash only |
| `SUPPLEMENT_v13.pdf` | 084091af1a419f0bff64b643da112a70133ad382d2e51c929fb077ceee8e5692 | hash only |
| `AMENDMENT_11_v13.md` | b33d8281848c9bf1fbe47a706adbba8e0e063dc4d7480f3fe6fd95e8bb677cf3 | unchanged since round 1 (same hash); my round-1 reading stands |
| `AMENDMENT_12_v13.md` | a9911f1222b5fa386c28d39b2f3816cb3e0ec00d0eb4c4d082a58dc8d4ac0e42 | same |
| `AMENDMENT_13_v13.md` | bc7c2bf47c9a29810aa84c5dd4827a0f2d9404f9b684a94d0a918967180498bf | same; searched again for "coordinator" (eight places) |

**Pages viewed (PNG):** manuscript `page01`, `page07`, `page09`, `page10`, `page11`, `page12`, `page13`, `page14`; their hashes match `work\pages_sha256.txt`. Not viewed: `page02` to `page06`, `page08`, the supplement pages and the template pages (the template was checked in round 1).

**Also read:** my own round-1 report; `work\round1_record_sections_5_7_8.md`; `work\letter_section_author_round.md`; `BUILD_REPORT_v13.md` of `freeze_v13_2115`. **Not read:** any other seat's report, the full response letter, the manifest, session notes, the draft fourth amendment, `TEXT_FREEZE`, `RECOUNT_COVERAGE`, `DERIVED`, `OUTCOMES`.

## 2. Judgements

| | Recommendation | Score | Stars |
|---|---|---|---|
| **(a) The text as it stands** | major revision | 6.0 / 10 | 3 of 5 |
| **(b) CONDITIONAL** on the three assumptions of the brief | minor revision | 6.6 / 10 | 3.5 of 5 |

No finding is marked CRITICAL.

**What separates them.** In (a) the paper still opens its ACKNOWLEDGMENT with "made every scientific decision", which the amendment files that it will deposit contradict in eight places of the third amendment alone, and its Related Work now says in the main text that the works it characterizes "were read at abstract level". Both are statements about the author's own conduct. An editor does not treat such a mismatch as a wording matter, so I keep "major" although no remaining item needs new analysis. In (b) those two are gone and what remains is five small wording and record items. The gap between the two scores is small because the three assumptions change no evidence: the objection to the paper's significance (below) is the same under both.

### The strongest case against publishing the revised paper as written

1. **The evidence did not change; the text grew around it.** The revision added no result. The one confirmed covariance finding could still hardly have failed (perfect ranking at the tracker's amplitude recovers 0.0001 of the room against a margin of 0.05). Every positive effect is an amendment test written after the results, at 2% to 5% of the room against each tracker's own class average, and the two controls that would give them meaning both failed. The paper says all of this. The case is therefore not that the paper misleads but that a referee may ask what a designer learns from 14 pages beyond "a constant covariance acts as a constant, and a prediction of braking matters far more".
2. **The revision exposed two facts that make the closed loop look worse.** Table 4 now shows that the class-average arm is in full braking in 52.7% of its decisions at the lower level and 78.6% at the higher, and Section V-C says every arm loses "about 24.5 s per run". The text gives neither the run length nor the reason. A hostile reader concludes that the planner spends most of its closed-loop time in its fallback, where no margin source can act, and that the closed-loop equivalence is close to automatic (P-3).
3. **The one positive result with no level-effect control now stands alone in the abstract.** The dropout gain was shown to be a level effect by the coast-count control. The adaptive filter's "beats its permuted twin by 0.05" has no such control: a permutation within runs destroys the timing of the lead's braking, so the test shows that timing matters, and a per-phase schedule that uses no covariance recovers 0.916 of the same room (P-2).
4. **The new first sentence of the abstract generalizes.** "In autonomous driving, a multiobject tracker's covariance ... improved decisions barely or not at all" precedes every limit. This is the claim most likely to be quoted and over-read (P-1).
5. **Desk rejection.** The grounds are the same as in round 1 and none got smaller: the AI disclosure (now 354 words in four paragraphs, with the contested sentence standing alone as the first paragraph), 14 pages against the ten the supplement says the journal recommends, a 1,503-word Section V-E, 2,724 words of tables and captions, and an abstract with fourteen numbers and five coined terms. I still put the chance at about one in three as the text stands, and about one in four under (b).

### How much of that case survives the paper's own disclosures

- **Point 1 survives in full as an objection to significance and not at all as an objection to honesty.** The abstract's last sentence, Section VI and Section VII state the limits. Only one new test could answer it (O-1 below), and the record rightly did not require it.
- **Point 2 survives.** The values are printed; their meaning is not. One or two sentences repair it.
- **Point 3 survives in the abstract and in Section VII**, where "recovered a few percent" covers three cases and the level-effect qualifier covers one. The body does not claim more than the twin test shows, but it does not say what the twin test cannot show.
- **Point 4 is half-answered** by the second sentence of the abstract, which gives the scope at once. A reader who quotes one sentence gets the unscoped one.
- **Point 5 cannot be answered by the paper.** It is an editor's judgement on a correctly disclosed fact. Under (b) the disclosure no longer contradicts its own record, which is the part the author controls.

## 3. N-1 to N-20

| ID | Verdict | Evidence (21:15 text) | What remains |
|---|---|---|---|
| N-1 | **not resolved** (waits for the author) | ACKNOWLEDGMENT, paragraph 1: "set its questions and plans, made every scientific decision". Paragraph 3: "Where the amendment files record a design choice as an AI session's, it was made within the author's approval." | The sentence. It now stands alone as its own paragraph, which makes it more prominent than before. |
| N-2 | resolved | IV-C: "A tracker's *permuted twin* asks whether the order of its margins matters beyond their amplitudes: each decision's factor ... is permuted among the decisions of its run and applied to the class average, and the twin's share is the mean over 20 such permutations." | See P-2 for what the test cannot show. |
| N-3 | resolved | Abstract: "against each tracker's own class average"; "both inside a ±5% margin as point values"; "beats its permuted twin by 0.05"; "with factors from the covariance margin's median ratios, recovers slightly more (descriptive)"; "(38% to 84% across run sets) but costs progress behind nonbraking leads"; "one longitudinal speed planner"; "(5 to 15 m/s)"; "(60 cases, contact rates far above any deployable level)"; "replacing per-track covariances by class averages". VII: "showed no recovery of a small room". | All eight parts are met. The rewrite brought side effects: P-1 and P-6. |
| N-4 | resolved | III-D: "clip($m$, 0.25, 10)"; V-E: "58,970 decisions of 366 runs", "Shapley shares", "0.0347 [0.0109, 0.0581]", "its class average is the 2 Hz one under the 2 Hz masks", "transition diagonal is 0.95"; IV-E: "a classification step passing unless its class is inconclusive". | Two values stay in the supplement by a stated rule (one program computed them). Acceptable. |
| N-5 | **not resolved** (waits for the author) | II: "publisher full texts were not searched, and the works found were read at abstract level". S13: "no full text was opened". | The author's reading and the sentence the record proposes. The limit is now in the main text, which is honest and also the first thing an editor will see in Section II. |
| N-6 | resolved | III-E: "no process noise is added over the look-ahead". V-E: "neither the maneuver mode's acceleration nor a prediction conditioned on the mode does". | None. |
| N-7 | partly resolved | ACKNOWLEDGMENT: "panels of five Claude agents (the same three models; reviewer workflow of the Academic Research Skills plug-in)". S12: "The text written with Claude Opus 5.5 was audited by Claude Fable 5.2 ... written with Claude Fable 5.2, by Claude Sonnet 5.5". | S12 says "Eight reviews"; this round is at least the ninth. S12 names one panel on "a Claude Sonnet model whose version its record does not name", so "the same three models" is slightly too exact. "The requests and responses are in the deposit" must be true at submission. |
| N-8 | resolved | IV-E: "recount every result value printed in the main text and all but the marked (‡) values of the supplement ... the library's true clearance was recomputed without it on 20 decisions". S12 uses the same sentence. | None. |
| N-9 | resolved | I: "three scenario families (lead braking, cut-in, and leads that do not brake hard) ... Later amendments, written after those results, added pedestrian crossing". | See O-3. |
| N-10 | resolved | V-E: "under rules fixed before any new run was extracted or scored (their capture had begun)". | None. |
| N-11 | resolved | I: "a *level effect* (more margin for an identifiable group of decisions, with no ranking shown inside the group)"; VI: "is partly one". | None. |
| N-12 | resolved | Table 6: "Closed loop, dropouts, first amendment, matched in design caution only (60 cases) ... −0.03 [−0.10, 0.03]; 0.15 [0.08, 0.24]"; "least-squares slope of that share on the start probability (four values)". | None. |
| N-13 | resolved | Table 4 columns "Peak decel.", "Rest gap", "Full braking"; V-C: "Table 4 shows where unscored cost to following traffic and occupants would fall". | The new values raise P-3. |
| N-14 | resolved | V-A: "NIS inflation recovers 0.024 of the room, the time gap 0.287, and the acceleration margin 0.369 (descriptive; Table 2): the shares rise in the order N, NA, TG, AM, CK3". | None. |
| N-15 | partly resolved | III-D: "the retuned filters' NIS during braking is several times its expected value (exploratory; computed by one program; Supplement S4)". | The value (7.9 to 9.6 against 2) is given in words only. Acceptable under the stated rule; optional. |
| N-16 | resolved | V-E: "pairs are not stratified by class or motion"; "chosen on the training split, after the all-pairs statistic had come out negative there ... the one Holm entry whose population was chosen again". | None. |
| N-17 | resolved | II: "a critical arrival rate below which the expected covariance of an unstable system is unbounded [27]". | The author's check of [27] falls under N-5. |
| N-18 | resolved | Table S5: "in the third amendment, the list of dropped arms carries the time \"06:52\" although its text and its two locks have earlier file times". | None. |
| N-19 | resolved | Table 1, row NA: "inflation by the normalized innovation squared (NIS)". | None. |
| N-20 | partly resolved | (1) four paragraphs in the required order (`page12`, `page13`): resolved. (2) "(a)" and "(b)" under Fig. 2 (`page07`): resolved. (3) "multiobject", "midrank" in running text: resolved. (4) lettered notes under Tables 2, 4 and 6 (`page07`, `page09`, `page10`): resolved. (5) "driving?\" in" in [21] (`page13`): resolved. (6) [10] "A. S. K. Kopalli" against the byline: **not resolved** (waits for the author). | Part 6. |

**Counts:** resolved 15; partly resolved 3 (N-7, N-15, N-20); not resolved 2 (N-1, N-5).

## 4. Findings

Types: **W** wording; **M** a value moved in from the supplement; **T** text the author writes from existing records; **A** new analysis or evidence.

### REQUIRED-major (2; none new)

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| N-1 | ACKNOWLEDGMENT, paragraph 1 | The responsibility sentence is contradicted by the records to be deposited. Unchanged; now a paragraph of its own. | "made every scientific decision"; Amendment 13, section 3.0: "**Whose decision:** the coordinator's." | "made or approved every scientific decision", after the author confirms it. | W (author) |
| N-5 | Section II, "Novelty, with its limits"; S13 | The paper characterizes works that nobody read in full, and now says so in the main text without the author's own reading beside it. | "the works found were read at abstract level"; "[35], [36] ... makes no such comparison". | The author reads the closest works in full and adds the record's sentence. | T (author) |

### REQUIRED-minor (5; 3 new)

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| N-20 (6) | Reference [10]; byline | Two surname forms. | "[10] A. S. K. Kopalli"; byline "Kopalli Naga Venkata". | One form. | W (author) |
| N-7 | S12 "Presubmission reviews"; ACKNOWLEDGMENT | The count of reviews is out of date and "the same three models" is too exact. | S12: "Eight reviews by panels of five agents"; "one on a Claude Sonnet model whose version its record does not name". | Update the count at submission; "Claude models, among them the same three". | T |
| P-1 (regression) | Abstract, sentences 1 and 4 | The first sentence states the result for autonomous driving at large before any limit. In sentence 4 "it" has no near antecedent: the nearest nouns are "amendments" and "first results". | "In autonomous driving, a multiobject tracker's covariance, used as a planner's safety margin, improved decisions barely or not at all"; "With fixed noise it is nearly constant and adds nothing". | "In a simulation study of one speed planner, a tracker's covariance ... improved decisions barely or not at all"; "With fixed noise the covariance is nearly constant". | W |
| P-2 | Abstract, sentence 5; V-E, "Other Trackers", paragraph 2; VII, sentence 3 | The adaptive filter's twin test permutes within runs, so it shows that the timing of the margin inside a run matters. It cannot separate ranking from a level effect by the lead's phase, and the paper ran a level-effect control only for dropouts. The per-phase schedule, with no covariance, recovers far more of the same room. The summary sentences leave the adaptive filter as an unqualified positive. | Abstract: "a noise-adaptive filter beats its permuted twin by 0.05". IV-C: "permuted among the decisions of its run". V-A: "The per-phase schedule ... recovers 0.916". VII: "it recovered a few percent of the room against its own class average, and at 2 Hz the dropout gain is a level effect". | V-E: add "no test separates this from a level effect by the lead's phase; a schedule by phase was not compared with it". VII: "none was shown to rank decisions beyond a level effect" or the same in other words. | W |
| P-3 (regression) | V-C; Table 4 | Two values moved in without what a reader needs to interpret them. The main text does not give the run length or say why every arm loses about 24.5 s, and it does not say what full braking in 52.7% and 78.6% of decisions means for a comparison of margin sources (in full braking no source acts). | "Against a mean time lost of about 24.5 s per run for every arm"; "the class average brakes fully in 52.7% of its decisions at the lower level and 78.6% at the higher". | One sentence: the run's length and that most of the time lost is waiting behind the stopped lead; one clause: the share of decisions in which a margin source could change the row, or that it was not computed. | M (S1, S9) |

### OPTIONAL (10)

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| O-1 (round-1 R-M5) | VI, "Limits"; VII | The test that would answer the significance objection is still future work: the covariance on top of the braking prediction's path, on arrays the study has. The wording half of my round-1 request is now met in VI. | "whether a covariance adds anything on top of the braking prediction's path was not tested". | One more amendment test, labeled as such. Not required for acceptance of the paper as a set of bounded nulls. | A |
| O-2 (round-1 R-m5) | Table 3; abstract | No comparison across trackers in absolute terms: does the two-noise IMM or the adaptive filter with its covariance beat the tracker of record with a class average? | "N_x, variant x's, against its own F0_x". | Compute from existing arrays, or say "not computed". | A or W |
| O-3 | I, paragraph 4 | "data not used for any design choice" holds for the confirmatory plan. The amendment tests reuse the fresh runs after their results were seen (dropouts rescored on them; coast-count factors "fitted on the 105 fresh runs"). The next sentence helps but does not say so. | "Here we test on data not used for any design choice". | "Later amendments ... added pedestrian crossing and the other tests of Section V-E, some on the same fresh runs". | W |
| O-4 (regression) | Whole text | Length and density grew. 14 pages (13 before); V-E 1,503 words (1,223 before); ACKNOWLEDGMENT 354 words (about 250 before); tables and captions 2,724 words; the body sits exactly on the project's own limit (8,253 of 8,253). | Build report: "body: 8253 (limit 8253)"; "E. Where the Covariance Varies: 1503". | Decide whether Section V-D with Table 5 and Fig. 4 (largely exploratory) moves to the supplement; it would save about a page. | W |
| O-5 | Abstract | 237 words by whitespace; 251 when hyphenated compounds are split. Fourteen numbers; "room", "equal caution", "permuted twin", "start probability" and "two-noise" are used before any definition. | "2.8% under detection dropouts (start probability 0.10; replicated; about 5% at higher ones)". | Drop the start probability and the bracketed interval; keep one number per result. | W |
| O-6 (round-1 O-5) | Fig. 2(a), `page07` | F0 is listed in the legend and cannot be seen under N. | Legend "F0"; no gray curve visible. | Draw F0 dashed on top. | W |
| O-7 | `page09`, `page10` | Tables 4 and 5 land inside the text of V-E, a page after V-C and V-D; column bottoms are ragged on `page11`. | Page images. | Float placement at the final build. | W |
| O-8 | S12, "Claim audit" | The last wording changes have had no audit. For this seat's part: every number in the abstract, Section I, V-C and V-E that I compared with Tables 2 to 6 agrees, and the two new differences recompute (0.0298 − 0.0322; 0.0298 − 0.0347). | S12: "The wording changed in answer to that second audit ... has had no further audit." | Run the audit, or keep the sentence. | T |
| O-9 | N-15 | The braking-phase NIS is in words only. | "several times its expected value". | Recount it and print it, or leave as is. | M |
| O-10 | VI; references | Carried advisories: bold run-in heads in II and VI; [47] without a month; conference references without place and month; no biography. | `page12`, `page14`. | The author's choice. | W |

**Counts:** REQUIRED-major 2 (0 new); REQUIRED-minor 5 (3 new: P-1, P-2, P-3); OPTIONAL 10.

## 5. The eight questions, briefly: what changed since round 1

1. **Labels and sizes.** Improved. The abstract no longer lists a descriptive 4.6% as a test result; "replicated" carries "capture had begun"; the coast-count result reads "slightly more ... the test was one-sided, so the excess is descriptive", which is the right label. The Holm families are unchanged. I found no value that disagrees with its table. Remaining: P-2 (a label of meaning, not of status).
2. **Overreach.** My round-1 R-M2 and R-M3 are met in the abstract, Section I and Section VII. New overreach comes only from the rewrite: the first sentence of the abstract (P-1). The nuScenes history is now stated plainly, including that it is "the one Holm entry whose population was chosen again".
3. **Earlier limits.** No limit was removed, because no evidence was added. All are still disclosed; two are disclosed better (the IMM interface; the search). The significance objection, the failed controls and the absence of decision-level evidence on real logs stand as in round 1.
4. **Readability.** Mixed. The abstract now leads with the answer, V-E has five headed parts, the run sets are named once in III-A, and "level effect" and the tracker's twin are defined. Against that, the abstract is harder to parse than before (O-5), and the main text carries more parentheses per sentence than a referee will enjoy.
5. **Verdict.** Round 1: major revision, 5.5. Now: (a) major revision, 6.0; (b) minor revision, 6.6. The rise reflects seventeen items done without a new error that I could find. It stops there because the evidence is the same.
6. **Self-contained main text.** All six of my round-1 cases are closed (rows and cost in III-E; the 10 Hz class average; "capture had begun"; the search's limits in II; the first closed loop's values in V-E and Table 6; the range over rates and latencies in V-D). One new case: the run length behind "24.5 s" (P-3).
7. **Format and declarations.** Five of my six round-1 misses are fixed; the surname form in [10] waits for the author. The placeholder for the repository and DOI is a gate, not a finding. New and advisory only: float placement (O-7).
8. **AI disclosure.** In form it still meets the rule, and it now names the panel and, through S12, the model of each pass; my round-1 R-m6 is met. Its two weak points are unchanged: the first sentence (N-1), and its length, which grew. The statement in S12 that all seats are Claude models "so their errors may be correlated" is a disclosure few papers make and it applies to this report as well.

**Length and density at 14 pages.** The journal sets no hard limit, so length alone is not a ground I would use to withhold acceptance. It is a ground an editor may use together with the disclosure. The revision bought self-containment with about a page and with denser sentences; that was the right trade for referees and the wrong one for a first read by an editor. The cheapest relief is to move the largely exploratory Section V-D, Table 5 and Fig. 4 to the supplement and to cut the abstract to one number per result. Neither changes a claim.
