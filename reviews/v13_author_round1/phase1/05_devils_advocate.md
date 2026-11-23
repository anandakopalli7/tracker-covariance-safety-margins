# Phase 1 report: seat 05, Devil's Advocate (author-round panel, package v13 of 22 Nov 2026, 18:30)

## 1. Header

- **Seat:** 05, Devil's Advocate (fixed seat). **Card:** none; the seat has no Phase-0 card. Only the field-analysis section of `review_v13_output\00_phase0_field_analysis_and_cards.md` was read (lines 1 to 40).
- **Model:** Claude Fable 5.2 (`claude-fable-5-2`). Later parts of the reviewed text were written by a session on the same model, so its wording was checked against the records and not taken on trust.
- **Card-confirmation pause not held** (non-interactive run).
- **Brief:** `work\panel_brief_author_round_v01.md`, SHA-256 47198b07517f3ac881f51c2768e0e71162814536952eef5033b647528d80feab (checked).
- **Skill:** `academic-research-skills:academic-paper-reviewer`, mode full, this seat only; no sub-agents, no other seats, no synthesis. No web access; no text sent anywhere.
- **Clock:** started about 18:39 EST; this file written after 18:47:39 EST (Get-Date).

**Files and SHA-256, at start and at end (identical both times):**

| File | SHA-256 | Read |
|---|---|---|
| `MANUSCRIPT_v13.md` | 29125167b108bc27833c16e3b639cbb07af5f4c105c49d375deff3d5b4a951d0 | in full |
| `MANUSCRIPT_v13.tex` | bd4d08d954d3595de2b5ac2653c18476c7bb3281e1c264604f995f018da01345 | preamble, front matter, floats and captions |
| `SUPPLEMENT_v13.md` | fab98c1fe24c8c5b95f86da8b1e664662401055232409a236d963938f5b99a09 | S1.1, S3 (Table S4, parts of Table S5), S12, S13, S14, S15, and searches of the rest |
| `MANUSCRIPT_v13.pdf` | 4fabfd9f611013fd4e7f60b8a59fcdcc2d782dbd3192a77c2efe54e77beb8299 | hash only (seen as page images) |
| `SUPPLEMENT_v13.pdf` | a8ad36027dee70c8c48cf2b998cb2512b55ca568c400eb1ecd340923ddeb8b16 | hash only |
| `AMENDMENT_11_v13.md` (seat's extra read) | b33d8281848c9bf1fbe47a706adbba8e0e063dc4d7480f3fe6fd95e8bb677cf3 | sections 0, 6c (head), 10, and searches |
| `AMENDMENT_12_v13.md` (seat's extra read) | a9911f1222b5fa386c28d39b2f3816cb3e0ec00d0eb4c4d082a58dc8d4ac0e42 | sections 0 to 2, 3c (head), 4, 5 (head), 8, and searches |
| `AMENDMENT_13_v13.md` (seat's extra read) | bc7c2bf47c9a29810aa84c5dd4827a0f2d9404f9b684a94d0a918967180498bf | sections 0 to 2 (to E6.6), 3 and 4 |
| `BUILD_REPORT_v13.md` | not hashed | word counts and house-style lines |
| `ojits-template.tex` | not hashed | lines 18 to 31, 62 to 89, 190 to 200, 393 to 396, 420 to 426, 472 to 480, 640 to 660 |

**Pages viewed (PNG):** manuscript `page01` to `page13` (all 13); template `tpl01`; supplement `sup01`. The 25 images' hashes match `work\pages_sha256.txt`. The four figures were seen on the page images, not opened as separate files. Not seen: `tpl02` to `tpl09`, `sup02`, `sup03`.

**Not read (blinding kept):** the response letter, the manifest, earlier review folders, other seats' files, session notes, diffs, `TEXT_FREEZE`, `RECOUNT_COVERAGE`, `DERIVED`, `OUTCOMES`. The deposit does not exist yet, so no lock file, hash list or program was inspected: every statement below about locks rests on the paper's and the amendments' own words.

## 2. Recommendation and score

- **Recommendation: major revision.**
- **Score: 5.5 out of 10; 3 stars out of 5.**
- No finding is marked CRITICAL. One structural objection (the first paragraph below) could alone produce a rejection from a hostile referee, but it is an objection to significance, not to correctness, and the paper states it itself.

### The strongest case against publishing the paper as written

The one confirmed covariance result could hardly fail. A fixed-noise filter's covariance is nearly constant on these runs, the sweep of the margin scale removes any constant, and even perfect ranking at the tracker's amplitude recovers 0.0001 of the room, against an equivalence margin of 0.05. The paper says so ("expected from this constancy"; "is not new [26]"). Everything a reader would want to know, namely what happens where the covariance varies, comes from three amendments written in about 36 hours, after the results were seen, by AI sessions working to an explicit instruction to raise an AI panel's score ("The paper has to be strong, for that use whatever scenario is most useful"; Amendment 11, section 0). Those tests give gains of 2% to 5% of the room, all against each tracker's own class average, and both controls that would have given them meaning failed: a table of three coast-count factors does as well as the covariance, and the closed-loop gain is not shown at equal time lost. On real logs there was no room, twice. And 78% of the room that the whole score is built on is the error of a deliberately simple constant-velocity prediction, so the covariance was tested in a regime that a designer would first repair in the predictor. What is left is a careful scoring protocol and a set of honest nulls for one in-house planner on one straight simulated road.

### How much of that case survives the paper's own disclosures

Most of it is disclosed, and that is the paper's main strength: it labels the amendments, reports both failed controls in the abstract, says the logs neither support nor contradict it, and states that nothing justifies removing a covariance margin. What survives:

1. **The author-role statement does not match the records that will be deposited** (R-M1). This is the point most likely to turn an editor against the paper.
2. **Three summary sentences still read stronger than the body** (R-M2, R-M3): the coast-count result without the source of its factors; "recovers 2% to 5%" set beside "adds nothing" under one ±5% margin.
3. **The novelty statement rests on abstracts** that an AI system read (R-M4).
4. **The constant-velocity regime** (R-M5): disclosed, but the cheapest test that would answer it, the covariance on top of the braking prediction's path, uses arrays the study already has and was left as future work.
5. **The significance objection itself** cannot be removed by wording. It can only be met by one test with room where the covariance varies for a reason other than the update schedule.

## 3. Findings

Types: **W** wording; **M** a value moved in from the supplement; **T** text the author writes from existing records; **A** new analysis or evidence. Locations are in `MANUSCRIPT_v13.md` unless stated.

### REQUIRED-major

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| R-M1 | ACKNOWLEDGMENT, sentence 1 and the sentence "where the amendment files record..."; Section IV-E | The claim that the author "set its questions and plans, made every scientific decision" is contradicted by the amendment files, which the deposit will hold. They record design decisions as an AI coordinator's, and a blanket approval to choose scenarios and experiments. The paragraph then half-withdraws its own first sentence. An editor who opens the deposit sees a responsibility statement that its own record disproves. | Paper: "The author conceived the study, set its questions and plans, made every scientific decision". Amendment 13, section 3.0: "**Whose decision:** the coordinator's." Amendment 12, section 5: "**Coordinator's decision on the design split** (about 03:27 EST...)"; section 0: "Download whatever you want and run whatever the experiment you want." Amendment 11, section 0: "change the scenarios how ever you want ... The paper has to be strong, for that use whatever scenario is most useful"; section 6c: "Proposed by 'Paper work summary' and approved in scope by the author". | Replace sentence 1 by what the records show: the author conceived the study, approved the confirmatory plan and each amendment's scope before its lock, decided the items the files record as the author's (for example the pedestrian test despite the no-go, the nuScenes primary population), and delegated the remaining design choices within the amendments to the AI sessions, which the files record. Add to IV-E that the amendments aimed at the panel's objections. | T, W |
| R-M2 | Abstract, sentence 7; Section I, "For a designer..."; Section VII, sentence 3 | The coast-count margin's factors are the covariance margin's own medians per count. For a fixed-noise filter the covariance while coasting is close to a function of the count, so the test shows that nothing beyond the count matters. It does not show that a designer can do without the covariance's growth law, which is where the factors come from. The three summary sentences drop that qualifier; only V-E and VI carry it. The text also says "as much" where the interval lies wholly below zero. | Abstract: "A margin that only counts missed updates reproduces the dropout gain". Section VII: "the dropout gain is a level effect that a margin counting missed updates reproduces". Section V-E: "its factors (0.216, 0.107, and 0.065 ...) are the median ratios of the covariance margin's critical scale to the class average's"; "difference −0.0024 [−0.0057, −0.0001]". | In the abstract, I and VII add "with factors taken from the covariance's own median growth". In V-E say the coast-count margin recovered slightly more (interval below zero, inside the margin). | W |
| R-M3 | Abstract, sentences 4 and 6; Section I, contribution 2 | (i) "adds nothing" is said of a share inside ±5%, and "recovers 2% to 5%" of shares that, as point values, are also inside ±5%; only V-E says so. (ii) The 4.6% for the adaptive filter is a descriptive share (Table 3); the test was its difference from the permuted twin. (iii) Each share is against the tracker's own class average and its own room, which the abstract does not say. | Abstract: "it recovers 2% to 5% of the room: 2.8% ..., 2.2% ..., and 4.6% for a noise-adaptive filter". Section V-B: "a small 0.0459 [0.0390, 0.0533] (Table 3; descriptive)". Section V-E: "inside the paper's ±5% equivalence margin: detectable, but small by that margin (no equivalence test was registered for them)". | Abstract: "in three amendment tests ... 2% to 5% of the room against its own class average, small by the same ±5% margin". Give the adaptive filter's tested value (0.051 above its permuted twin) or mark 4.6% descriptive. | W |
| R-M4 | Section II, "Novelty, with its limits"; ACKNOWLEDGMENT; Supplement S13 | The novelty statement and the statements about [19], [35], [36] rest on abstracts read by an AI system. The main text says only "In the sources we searched". IEEE expects an author to have read what the paper characterizes, and "makes no such comparison" is a claim about two papers' full content. | Supplement S13: "no full text was opened"; "the related-work statements about intelligent-vehicle threat assessment therefore rest on abstracts"; "[19], [27], [28], [29], [35], [36]; what the paper says about them stays within those abstracts"; "[42], [43], [41] ... their full texts were not read". Section II: "the work on criticality and worst-case performance under uncertainty [35], [36] ... makes no such comparison". | The author reads [13], [15], [19], [35], [36] in full and corrects II if needed; II then says which works were read in full and that the rest of the search read abstracts. | T |
| R-M5 | Section V-A; Section VI, "Limits"; abstract | The room is mostly the constant-velocity prediction's error (78% recovered by a fixed braking prediction; 23.6 of the room's points lie in braking). A covariance is tested for ranking an error that a designer would first remove in the predictor. Whether it ranks the remaining error is the question of practical interest, it needs no new runs, and it is left untested. This is the first thing a hostile referee will write. | Section VI: "Every test used a constant-velocity prediction; whether a covariance adds anything on top of the braking prediction's path was not tested." Section VII: "Next steps are ... a covariance added to a braking prediction's path". | Score N and the class average on the braking prediction's path on the fresh and new lead-braking arrays (one more amendment test, labeled as such), or state in the abstract that the room tested is mainly prediction error that a braking prediction removes. | A (or W) |

### REQUIRED-minor

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| R-m1 | Section V-E, nuScenes paragraph and the Holm sentence | The primary population replaced an all-pairs statistic that was negative on the training split and, in the amendment's words, expected to fail. The paper says only that it was "dominated by steady tracks", and then counts the test among six that "stay significant" after Holm. Validation gave 0.108 against 0.24 and 0.14 on training. | Paper: "after the all-row statistic there was found to be dominated by steady tracks". Amendment 12, section 5: "all-pairs within-cell τ was −0.0108 [−0.0216, −0.0001]"; "Train showed it dominated by steady pairs and expected to fail." | Say "after the all-pairs statistic was negative on the training split (−0.011)"; in the Holm sentence add that one of the six had its population rechosen on training data. | W |
| R-m2 | Section V-E (twice), Table 6 label "replicated" | "Under rules fixed before the data" is stronger than the record: capture of the new runs had begun before the lock. | Supplement S15: "under rules fixed before any of those runs was extracted or scored (their capture had begun before the lock, which records them as sealed)". | "under rules fixed before those runs were extracted or scored". | W |
| R-m3 | Section V-E, 10 Hz sentence | The 10 Hz dropout result uses the 2 Hz class average. The main text reports its class and a positive in-dropout share without that limit. | Supplement S15: "its class average is the 2 Hz one under the 2 Hz masks, because no 10 Hz class average could be made from the tuning runs". | Add "against the 2 Hz class average" to the sentence. | M (S15) |
| R-m4 | Abstract, sentence 9 | The 78% for the braking prediction is given without its cost, which the conclusion and V-C give. All fresh leads brake to a stop, which is the case the prediction assumes. | Abstract: "A braking prediction recovers 78% of the lead-braking room." Section VII: "at a cost in progress behind leads that do not brake hard". | Add "at a cost in progress behind leads that do not brake hard". | W |
| R-m5 | Tables 3 and 6; abstract | Shares of different trackers are each against their own class average and room, so "recovers 2.2%" does not say whether the two-noise IMM's covariance margin beats the tracker of record with a class average. A designer needs that comparison. | Table 1: "N_x, variant x's, against its own F0_x". Table 3: rooms by phase differ by tracker (23.62 against 29.52 points in braking). | Add, for the two-noise IMM and the adaptive filter, the frontier distance to the online tracker's class-average frontier (existing arrays), or say it was not computed. | A (existing arrays) or W |
| R-m6 | Supplement S12, "Claim audit" and "Second programs"; ACKNOWLEDGMENT | S12 says the audit and the second programs were by "a model other than the writer's". The ACKNOWLEDGMENT names Fable 5.2 among the models that drafted and revised the text and also as an auditor and a second-program writer. Both cannot hold for every pass. | S12: "an agent on a model other than the writer's audited every sentence". ACKNOWLEDGMENT: "Claude (... Opus 5.5, Fable 5.2, and Sonnet 5.5) ... drafted and revised the text of all sections"; "Claude Fable 5.2 and then Claude Sonnet 5.5 audited the claims". | State per pass which model wrote and which audited; drop "other than the writer's" where it does not hold. | T |
| R-m7 | Supplement Table S5 (slips row) and Table S29 | A third stated time is later than its file's time and is not listed: Amendment 13 records a decision at 06:52 in a text whose file time is 06:47:56. Table S5 lists two such slips, both in the second amendment. With internal locks and no third-party timestamp, every unlisted slip costs trust. | Amendment 13, E6.0: "**Dropped by decision (coordinator, 06:52):**". Table S29: "Third amendment ... 22 Nov 06:47:56". Table S5: "Two stated times are later than the file times of their locks". | Add the third slip to the Table S5 row. | T |
| R-m8 | Section III-E; Section IV-A | Caution is defined by the "first truly safe row in cost order", but the rows and their cost are only in Supplement S1.1. The main measure rests on a definition that the main text does not give. | Section IV-A: "Caution is the speed of the first truly safe row in cost order". Supplement S1.1: "The cost of a row sums ... the mean squared deviation of its speed from the desired speed ..., 0.05 times its mean squared acceleration ... and 0.02 times its mean squared jerk". | One sentence in III-E: the 16 pairs of target accelerations from {−5, −2, 0, 2} m/s² plus one, and the cost's three terms. | M (S1.1) |
| R-m9 | Table 6, row 4; Section V-E | The slope is called "on the dropout rate" in Table 6 and "on the start probability" in IV-E; it is a least-squares slope over four points, of which the last two are flat. | Table 6: "slope of that share on the dropout rate". Section IV-E: "the slope of the dropout share on the start probability". Supplement S15: "the least-squares slope of the share on the probability". | Use "start probability" in Table 6 and say "least-squares slope over the four start probabilities". | W, M |
| R-m10 | Q7 items (see answer 7) | Six format misses: order inside the ACKNOWLEDGMENT; "multi-object"; Fig. 2 without (a) and (b); reference [21] punctuation; the author's name form in [10]; "position-velocity" with a hyphen once. | See answer 7. | See answer 7. | W |

### OPTIONAL

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| O-1 | Title; Section IV-E; Table 1 | The title says "Preregistered"; IV-E redefines the word, and the non-null results come from amendments "written after the fresh lead-braking results were seen". Not a contradiction, but a referee will read the title first. | Section IV-E: "By 'preregistered' we mean internal locks, not a public registry". | The author's choice; "with Internally Locked Plans" would remove the objection. | W |
| O-2 | Section V-E | One subsection of about 1,220 words carries eight results. It is the hardest part to read. | Build report: "E. Where the Covariance Varies: 1223". | Split into subsubsections with title-case headings (pedestrians; dropouts; other trackers; closed loop; real logs). | W |
| O-3 | Whole text | Six run-set names: tuning, old evaluation, stored, fresh, older fresh, new. "Older fresh" and "fresh" are the same set. | Section V-E: "matched in open-loop caution on the older fresh runs". | Name the sets once in III-A and use "fresh" and "new" only. | W |
| O-4 | Table 2, row "Classification" | The row does not say whose class it is. The text gives the tracker of record's class as descriptive and the IMM's as confirmed. | Table 2: "Classification / amplitude-limited". | "Classification (IMM, registered)". | W |
| O-5 | Fig. 2 | F0 lies under N and cannot be seen; the right panel is empty. | Fig. 2, `page07`. | Draw F0 dashed on top; replace the right panel by a line in the caption. | W |
| O-6 | Fig. 4(a) | The legend is small and the caption does not name the three latencies. | Fig. 4, `page09`. | Name 0, 0.1 and 0.2 s in the caption. | W |
| O-7 | Abstract, sentence 4 | "no contact difference above 0.10 was resolved" does not give the number of cases or the base rate of 20%. | Section V-C: "with 60 cases per arm contact differences much below 0.10 cannot be resolved". | Add "(60 cases)". | W |
| O-8 | Supplement Table S43 | The paired peak-deceleration difference is −2.99 m/s² while the arms' medians are 6.25 and 6.11. A mean beside medians may be right, but it looks like an error. | Table S43: "6.25 ... 6.11 ... −2.99 [−4.32, −1.74]". | Check; say "mean paired difference" in that cell. | T |
| O-9 | ACKNOWLEDGMENT | The paragraph has about 250 words and reads as a defense. The Codex sentence could not be checked against the records this seat may read. | "Codex (OpenAI; models GPT-6.1 Sol, GPT-6 Astra, and GPT-6.2 Astra) developed the simulation, recording, and planner software in an earlier phase." | Shorten to system, sections and level of use; move the process detail to the supplement. | W |
| O-10 | Length | 13 typeset pages; the supplement says the journal recommends ten. | Table S5: "the journal sets none and recommends ten". | Decide before submission whether the overlength is accepted. | none |
| O-11 | References [45], [47] | [47] has no month; [45] is a UN document with no access note. | "[47] ... vol. 2, no. 1, pp. 22–26, 1966". | Add "Aug." to [47]; add "[Online]. Available" and "Accessed" to [45] if a link is given. | W |
| O-12 | End of paper | No author biography (optional at submission). | `page13`. | Advisory. | none |

## 4. The eight answers

### 1. Labels and sizes

Mostly right. "Confirmed" appears only for the original plan (room, detection, equivalence, the IMM's class, the per-phase schedule, the braking prediction). Amendment tests carry "(A)", "failed" or "replicated". Holm is beside the labels and changes none; the two third-amendment controls are reported as failed with adjusted p of 0.18 and 0.99. I recomputed both Holm families from the printed p-values and they agree. I also checked about thirty printed values against each other (abstract against tables, decision-equivalents, the interpolated 25.7%) and found no mismatch.

Three label problems remain:
- The abstract lists 4.6% for the adaptive filter among tested results; it is a descriptive share (R-M3).
- "Replicated under rules fixed before the data" overstates by a little (R-m2).
- "Recovered as much" understates a difference whose interval is wholly below zero (R-M2).

### 2. Overreach

- **Dropout gain's source.** The body is right. The abstract, the introduction and the conclusion omit that the coast-count factors come from the covariance (R-M2).
- **Closed loop.** Not overreached. The text says twice that fewer contacts cannot be told from a wider margin. The equal-time-lost test conditions on the 89 cases without contact in any arm and interpolates between two points; the text says both.
- **nuScenes mechanism check.** The size is stated fairly ("weakly", "partly a level effect"). The history of the primary population is softened (R-m1).
- **Real-log decision test.** Not overreached: "they neither support nor contradict the simulated results".
- **Two-noise IMM.** The interface limit is stated in V-E and VI. The share is against its own class average (R-m5).
- **Scope of the null.** Stated in the abstract ("with a constant-velocity prediction"), the Scope paragraph and VI. The untested combination with the braking prediction is the gap (R-M5).
- **Not on the brief's list:** the author-role statement (R-M1) and the novelty statement (R-M4) both claim more than the records allow.

### 3. Earlier limits

| Limit | Status | What remains |
|---|---|---|
| (a) closed loop matched only in open-loop caution | addressed by a test, which failed | No closed-loop evidence for the covariance at equal cost; one level, lead braking. |
| (b) dropout gain may be a coasting margin | addressed by a test, which failed | The summary sentences lack the factors' source (R-M2). No coast-count comparison at 10 Hz or on nuScenes. |
| (c) abstract and conclusion stronger than the body | mostly addressed; the three quoted phrases are gone | R-M2, R-M3 and R-m4. |
| (d) two-noise IMM's interface | partly addressed (disclosed in III-D, V-E, VI) | A wider interface was not tested. |
| (e) scope of Holm and of the recount | addressed in IV-E | The recount shares the scoring library, arrays and draws, as stated. |
| (f) density; round-2 results only in the supplement | results moved in (Table 6); density not addressed | 13 pages; V-E is one block of about 1,220 words (O-2). |
| A confirmed result that could hardly fail | not addressed (cannot be by wording) | Disclosed in V-A and VI. |
| Small positive effects | not addressed | Disclosed; and now matched by controls. |
| One simulator, one configuration | partly: a 10 Hz dropout configuration was added | It uses the 2 Hz class average (R-m3). |
| No decision-level real-log evidence | not addressed; a second attempt again found no room | Disclosed. |
| Process: amendments after results, local locks, AI authorship | disclosed, not addressed | R-M1, R-m6, R-m7; the deposit does not exist yet. |

### 4. Readability

- **Bottom line first?** No. The abstract gives the setting, the question and the process before the first result in its fourth sentence, and it carries about fifteen numbers in 245 words. The paragraph "For a designer the short version is this" at the end of Section I is the clearest statement in the paper and belongs in the abstract's place.
- **Coined terms.** Each is defined once, in Table 1 or Section IV. The run-set names are the exception (O-3).
- **Evidence in the main text.** Yes for every headline claim: each number in the abstract is in Tables 2 to 6 or the body. The cases where a supplement fact is needed are in answer 6.

### 5. Verdict

- **Recommendation:** major revision.
- **Score:** 5.5 out of 10; 3 stars out of 5.
- **Most likely editorial outcome at OJ-ITS:** major revision if the paper reaches referees. Desk rejection is a real possibility, roughly one in three by my estimate, on the AI disclosure together with length and density.
- **The single change that would raise the score most:** one decision-level test with room in which the covariance varies for a reason other than the update schedule. The cheapest is the covariance on top of the braking prediction's path on the existing lead-braking arrays (R-M5). Among wording changes, R-M1.

### 6. Self-contained main text

The main text now holds every headline result. Six claims still need a supplement fact:

| # | Main-text location | Supplement item it rests on | Fact to bring in |
|---|---|---|---|
| 1 | IV-A, "first truly safe row in cost order" | S1.1 | What the 17 rows are and the three terms of their cost (R-m8). |
| 2 | V-E, 10 Hz sentence | S15, "Dropouts at 10 Hz" | The class average there is the 2 Hz one (R-m3). |
| 3 | V-E, "under rules fixed before the data" | S15, "Dropouts on the new runs" | Capture had begun before the lock; the runs were sealed (R-m2). |
| 4 | II, "In the sources we searched" | S13 | The search read abstracts only; no full text was opened (R-M4). |
| 5 | V-E, "An earlier closed loop with dropouts ... found equivalence at the lower level" | S14, Table S35 | The values: contact difference −0.03 [−0.10, 0.03], time lost 0.15 [0.08, 0.24] s. |
| 6 | V-D, "the tracker covariance's share stays inside the margin at every rate and latency" | S6, Table S16 | Only the 10 Hz value is in Table 5; give the range over the other settings in one clause. |

None of the six carries a contribution alone. Cases 2 to 4 change how a claim reads and should be fixed; 1, 5 and 6 are one clause each. I do not expect a rejection on this ground as the text stands.

### 7. Format and declarations

Checked on the page images and the .tex, against the template lines cited.

**Passes:** section and subsection headings in capitals (`page01` to `page12`; template lines 62, 472); no subsubsections, so no title-case case arises; "Fig. N" in text and "FIGURE N." in captions; "Table N" and "TABLE N." in Arabic; "Table S5", "Table S29" and "Supplement Sn" for the supplement; American spelling (no British form found by search); no contractions; "preregistered" in one spelling; periods and commas inside closing quotation marks; funding in the first-page note with no Funding heading (template line 29); one ACKNOWLEDGMENT, singular (template lines 472 to 474); first page with author, affiliation, ORCID, corresponding author and e-mail (template lines 20 to 28); running head "Kopalli Naga Venkata: Tracker Covariances as Safety Margins in Motion Planning" on even pages (template line 30); abstract 245 words in one paragraph with no abbreviation; five index terms in alphabetical order (template line 39); table titles above and figure captions below (template lines 448 to 449); tables within the column or the page width; abbreviations defined at first use in the body (IMM, CARLA, CV, CA, NIS, SHA-256, AI).

**Misses (six):**

| # | Location | Miss | Template line |
|---|---|---|---|
| 1 | ACKNOWLEDGMENT (`page11`, `page12`) | Order is responsibility, AI disclosure, data and code, competing interests. The required order puts data and code availability before the AI disclosure. | brief, Q7 |
| 2 | Abstract; Section I (twice); Section II | "multi-object" in running text, four times. The template joins "multi" to its word. (Titles in [5], [31], [32] keep their own spelling.) | 196 to 197 |
| 3 | Fig. 2 (`page07`) | Two panels without (a) and (b); the caption says "Right:". Fig. 4 has the labels. | 393 to 396 |
| 4 | Reference [21] | `driving?,"` has a comma after the question mark. | 640 to 660 (reference form) |
| 5 | Reference [10] against the byline | The author is "A. S. K. Kopalli" in [10] and "Kopalli Naga Venkata" in the byline and running head. One form of the surname is needed. | 20 to 30 |
| 6 | Section III-D | "position-velocity block" with a hyphen; elsewhere "position–velocity" with an en dash (III-E, V-E, VI). | 71 (complex modifiers) |

**Advisory, not counted:** no author biography; 13 pages against a recommended ten; [47] without a month.

### 8. AI disclosure

**Does it meet IEEE's rule?** In form, yes. It is in the acknowledgments, names the systems and models, names the parts (analysis, simulation-control and figure code; literature searches; "the text of all sections and of the supplementary material"; the simulation, recording and planner software; the amendment plans) and gives the level (wrote, drafted and revised). It does not understate the use.

**Would an editor desk-reject on it?** Possibly. The rule asks for disclosure and the disclosure is full, so a rejection would be on judgment, not on the rule: the text, the code, the amendment plans, the literature search, the verification and the presubmission review are all AI work, and the sole author's part is direction, choice and approval. I put the chance of a desk rejection at roughly one in three, with the disclosure as the main reason. The paragraph's present wording raises that risk in two ways: it opens with a claim the records do not support, and it argues its case at length.

**Factual claims checked:**

| Claim | Check | Result |
|---|---|---|
| "set its questions and plans, made every scientific decision" | Amendments 11 to 13 | **Not supported.** Decisions are recorded as the coordinator's (A13 3.0; A12 5; A11 6c and 6d; A12 3c). The author approved scope, money and time, and decided named items (R-M1). |
| "directed further experiments after the systems had judged the manuscript ready" | A11 section 0; A12 section 0 | Supported: "Tell me what it take to bring it to 8/10 score atleast"; "I don't think it would get even 7 out of 10". |
| "The AI systems also drafted the amendment plans and proposed design options" | A11 to A13 headers | Supported. |
| "where the amendment files record a design choice as an AI session's, it was made within the author's approval" | A11 and A12 section 0 | Supported as a blanket approval. Amendment 13 has no approval record of its own; it runs under the second round's approval. |
| Second programs by "Sonnet 5.5 and Fable 5.2" that had not read the first programs | A11 section 10; A12 section 8; A13 3.8 | Models supported. "Had not read" cannot be checked from here. |
| "share the scoring library, stored arrays, and resample draws" | A13 3.4 ("Draw: DR2's"); S12 | Supported. |
| "Claude Fable 5.2 and then Claude Sonnet 5.5 audited the claims" | S12 | S12 names no model and says "a model other than the writer's", which conflicts with Fable 5.2 as a writer (R-m6). |
| The author chose "the presubmission review by an AI panel" | IV-E; A11 section 0 | Supported. |
| Codex sentence | not in this seat's reads | Not checkable here. |
| "The requests and responses of the presubmission reviews are deposited" | deposit is a placeholder | Not checkable; it must be true at submission. |
| "the third's two controls were asked for by that panel" (IV-E) | A13 section 0 | Supported. |

**Wording that would lower the risk without understating the use.** Keep the systems, parts and level. Change the first sentence to what the records show, and shorten the rest:

> The author conceived the study, approved its confirmatory plan and each amendment before its lock, decided which results to report and how to label them, reviewed and approved all content, and takes full responsibility for the work. Generative AI was used throughout and is disclosed here under IEEE policy. Under the author's direction, Claude (Anthropic; models ...) wrote the analysis, simulation-control, and figure code, ran the literature searches, drafted the amendment plans, and drafted and revised the text of all sections and of the supplementary material; Codex (OpenAI; models ...) developed the simulation, recording, and planner software. Within the amendments, design choices were made by the AI sessions under the author's approval of their scope, and the amendment files record each as such. Separate Claude sessions wrote the second programs and audited the claims (Section IV-E; Supplement S12). The presubmission reviews, by an AI panel, are deposited.

The author must confirm each clause, in particular "decided which results to report and how to label them", before using it.

## 5. Devil's Advocate additions

**Forking paths, in order of weight.**
1. The dropout scenario, its mask law (start probability 0.10, one to three updates) and the output-rule change from one to three kept updates were all chosen after the fresh results, by sessions told to make the paper strong. With the tracker's own output rule "no margin could act" (Table S5). The replication on new runs shows that the result is stable under sampling; it cannot show that the design choices were neutral. Disclosed ("this mask law, and this output rule only").
2. The nuScenes primary population (R-m1).
3. Each tracker against its own class average and room (R-m5).
4. Interval levels differ by quantity (95%, 99% nominal, 99.4% calibrated). Disclosed in the captions.
5. The equal-time-lost estimator. It failed, so it did not help the paper.

**Alternative explanations the paper does not rule out.**
- The two-noise IMM's 2.2% may reflect a better state estimate (lag 0.40 m against 1.42 m in Table 3) changing its own class average's frontier, not information in its covariance. Its permuted-twin difference (Supplement S15, 0.0210) speaks against this, but is descriptive and only in the supplement.
- The recording policy used the tracker's own covariance in its margin, so the visited states are those a covariance margin produces. Disclosed as off-policy.

**Who is left out.** Following traffic and occupants (rear contacts and hard braking are unscored; disclosed), and every road user but a lead car and a pedestrian.

**Observations that are not defects.** The reporting of the two failed controls in the abstract; the sentence that the logs "neither support nor contradict" the simulation; the count of departures in IV-E (60 rows, 21 after results); and the agreement of every printed value I cross-checked.
