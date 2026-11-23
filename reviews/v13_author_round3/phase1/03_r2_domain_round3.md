# Third round, v13 package of 22 Nov 2026 22:44: seat R2, Peer Reviewer 2 (Domain)

## 1. Header

- **Seat:** R2, Peer Reviewer 2 (Domain). One seat only. I wrote no synthesis and ran no sub-agents.
- **Model:** Claude Opus 5.5 (`claude-opus-5-5`). Much of the text under review was written by the same model, and so were my own earlier suggestions. I read both with deliberate skepticism.
- **Card:** "Card 3: Peer Reviewer 2 (Domain)" in `review_v13_output\00_phase0_field_analysis_and_cards.md` (SHA-256 21571d5c…c1ee172). Identity: multi-object tracking and Kalman-filter estimation for road vehicles, covariance consistency (NIS/NEES), adaptive and multiple-model filtering, and how tracker uncertainty reaches prediction and planning. In that file I read only the card and the field analysis (lines 1 to 46 and 67 to 76).
- **Card-confirmation pause not held** (non-interactive run).
- **Criteria binding:** none was supplied (`criteria_binding_unavailable`). Format is judged against the round-1 brief's Q7 list and the official template.
- **Brief:** `work\panel_brief_round3_v01.md`. SHA-256 dfd806d0a83fba1c6664dfb99de2ed72434c06eee13b81e69d5130a29c7b63e3 at the start (22:58:04 EST) and the same at the end (23:06:17 EST).
- **Skill:** I loaded `academic-research-skills:academic-paper-reviewer` for its re-review standards only.

| File (`package_v13_2244\`) | SHA-256 at start (22:58:04 EST) | SHA-256 at end (23:06:17 EST) |
|---|---|---|
| MANUSCRIPT_v13.md | 04b6ca9e2c47fb34d0f9b09f980c8e6855e37ebfd0062368649a75636d3e2eb8 | same |
| MANUSCRIPT_v13.tex | 710a8366cb4aba07bbe8fd67084a38f217f2862cf6d8d8bfc0ebeb4c80f6df8d | same |
| SUPPLEMENT_v13.md | e99e2d807a0884af7e53866a69a4b5f7019741e1fa75902a5cfcf56fd2545eba | same |
| MANUSCRIPT_v13.pdf (not opened) | 93926a734b87ea1fb17117928edda98a2603d041b89afdc9521f1e8a5d650914 | same |
| SUPPLEMENT_v13.pdf (not opened) | ec81d45527801c11bd0ad4b06f91c94c44ef7c430b03235bf3ef1770f3b03f23 | same |

All five start hashes equal the brief's.

- **Pages viewed:** `pages\page01.png` to `page14.png` (all 14). Their hashes match `work\pages_sha256.txt`, and every layout statement below rests on these images. I viewed no supplement or template images, so I make no layout statement about the supplement.
- **Read, all within the brief's allowed list:**
  - the manuscript Markdown in full;
  - `MANUSCRIPT_v13.tex`: front matter, running head and line 123 only;
  - the supplement: S1.1 to S1.4, S4 (Tables S6 and S7), S6.2 (Table S16), S11 (Table S28), S13 (Table S30), S14 (Tables S31 to S36) and S15 (Tables S37 to S46);
  - my own round-2 report, `03_r2_domain_round2.md` (026ec405…589cb0);
  - `work\round2_record_sections_3_4.md` (4bc02ba6…0f6d63);
  - `work\letter_section_round2.md` (28a0673f…2bf2650);
  - the round-1 brief's Q1 to Q8 list (47198b07…d80feab).
- **Not read:** other seats' reports from any round, the full response letter, the manifest, the notes folder, the amendment draft, the freeze, coverage, derived and outcome files, the build report itself (I used the brief's word counts), and the failed public-copy folder.
- **Limits:**
  - Read only, with no web access and no Python process.
  - I opened no cited work. Every statement about a reference's content is from memory and marked so, and every suggested reference is "unverified".
  - Statistics are outside my card.

## 2. Judgement

| Recommendation | Score | Stars | Most likely OJ-ITS outcome | Send as is (apart from the DOI)? |
|---|---|---|---|---|
| **Minor revision** | **7.0 / 10** | ★★★½☆ (3.5 of 5) | Minor revision. Major revision is possible if a referee weighs the post-results amendments and the 14-page length. | **No.** Two short text edits first. |

**Reasons.**

**What is fixed.** The three author gates are settled:
- the Acknowledgment says "made or approved every scientific decision";
- the running head and [10] agree on "Kopalli";
- Section II reports that the author read [13], [15], [19], [35] and [36] in full, and that every reference's record was checked.

The record's P-1 to P-6 are all fixed in the text:
- the abstract is scoped in its first sentence;
- the twin is limited to timing;
- Table 5 carries the NA, TG and AM rows, and the order N < NA < TG < AM < CK3 holds in all three columns (checked);
- the [27] sentence now names the heading.

In my domain the margin interface is stated where it binds (III-D, III-E, V-E "Other Trackers", VI Limits, VII). The closed-loop and dropout statements say what was shown and what was not.

**What still keeps me from "accept as is".** Two items, each a sentence or two, with no new analysis:

1. **(N-5 residual, introduced in this revision.)** The new reading sentence in Section II says that "the others were read at abstract level". Supplement S13 says that seven references ([4], [10], [41] to [45]) were not. A declaration about which sources were read must agree with its own supplement.
2. **(O-4a, raised to required.)** The closest result in the target journal, [19], reports a cut in collision risk of more than 66% from modelling misdetections. It is still not reconciled with this paper's dropout result. The record downgraded this item only because it depended on the author's reading of [19]. That reading is now done, so the reason no longer holds. The paper's own closed loop with dropouts already supplies the reconciliation an OJ-ITS referee will ask for: fewer contacts at matched open-loop caution (21% against 33%), not shown at equal time lost.

**Why the score is not higher.** The structural limits are disclosed but unchanged:
- the confirmed null was expected from the Riccati steady state;
- the gains where the covariance varies are a few percent of the room;
- there is one simulated configuration at 2 Hz;
- there is no decision-level real-log evidence;
- the amendments came after first results.

The page is dense: 14 pages, body 8,229 words. I give the same 7.0 as my round-2 conditional score, because the science is unchanged and the wording items I expected have been done.

## 3. The nine open items

| ID | Verdict | Evidence from the 22:44 text (location) | What remains |
|---|---|---|---|
| N-1 | **Resolved** | "The author conceived the study, set its questions and plans, made or approved every scientific decision, and reviewed and approved all content" (ACKNOWLEDGMENT ¶1, p. 13); ¶3 "Where the amendment files record a design choice as an AI session's, it was made within the author's approval" now agrees with it. | None. |
| N-5 | **Partly resolved** | "The author read five of the 47 references in full ([13], [15], [19], [35], [36]); the others were read at abstract level, and every reference's record but that of the author's own manuscript [10] was checked against Crossref or its publisher's page (Supplement S13)" (II, Novelty, p. 3); ACKNOWLEDGMENT ¶3: "Section II states what the author read in full." Against S13: "an AI system read the others at abstract level, except [4], [10], [41], [42], [43], [44], and [45]"; "36 against Crossref and ten against their sources' own pages". | The reading and the counts are in. Section II and S13 still disagree on seven references and on who read them (see REQUIRED-minor). |
| N-20 (6) | **Resolved** | Running head "Kopalli: Tracker Covariances as Safety Margins in Motion Planning" (pp. 2, 4, …; tex line 50 `\markboth{…}{Kopalli}`); [10] "A. S. K. Kopalli" (p. 13); full name on the first page (p. 1). | None (the form is the author's choice). |
| P-1 | **Resolved** | Abstract (p. 1): "In simulated tests of one speed planner predicting at constant velocity (straight road, 5 to 15 m/s)"; "With fixed noise and regular updates the covariance is nearly constant"; "beats its within-run permuted twin by 0.05 of the room (a timing effect)"; "Pedestrian crossing (open loop; room 0.16 points)". The qualifier also appears in I ("With fixed noise and regular updates, the covariance of a vehicle followed on a straight road settles", p. 1; contribution 2, p. 2) and VI ¶1 ("With fixed class-level noise and regular updates", p. 12). | Optional only: VI ¶2 "in lead braking that makes it a constant" (Q-3). |
| P-2 | **Resolved** | IV-E is now four paragraphs (p. 6), V-C three (pp. 7–8) and IV-C three (p. 5). "Detection Dropouts" is split into three paragraphs (pp. 10–11). Table 4's rule sits in note ^d^ (p. 9). | Optional only: "Closed Loop With Dropouts" (p. 11) and VI Limits (p. 12) are still single paragraphs of about 300 words (O-8). |
| P-3 | **Resolved** | "In these 60 cases the lead brakes to a stop and the ego ends the run behind it, so at the lower level every arm loses 24.5 to 24.8 s of the 30 assessed seconds (Section III-B)"; "full braking is the planner's hardest row, taken as its fallback or as the first feasible row (Section III-E), and the share of decisions in which a margin source could change the row was not computed" (V-C, pp. 7–8); III-B defines time lost over "the assessed 30 s of a run (after 5 s of warm-up)" (p. 4). | None. |
| P-4 | **Resolved** | "with fixed noise the covariance is then a function of the arrival sequence and, for noise fixed in the object frame, the heading, so on a straight road a margin that counts missed updates should match it (Section V-E)" (II, p. 3); this agrees with VI: "follows the update schedule and the geometry". | Optional only: the critical-rate clause (Q-2). |
| P-5 | **Resolved** | Table 5 (p. 9): "NA share, same columns 0.064 / 0.015 / 0.024"; "TG share … 0.182 / 0.321 / 0.287"; "AM share … 0.278 / 0.382 / 0.369", beside N and CK3. V-D: "the sources' shares keep one order (point values rising: N, NA, TG, AM, CK3; Table 5)". I checked the order in each column. | None. |
| P-6 | **Resolved** | "Because the permutation is within runs, a positive difference shows that the margins' timing matters; it cannot separate ranking among decisions from a *level effect* … that follows the lead's phase. Only the dropout test had a control for such an effect, the coast-count margin (Section V-E)" (IV-C, p. 5); abstract "(a timing effect)"; VII "only the dropout gain had a control that separates ranking from level" (p. 12). | None. |

**Counts:** resolved 8 (N-1, N-20 (6), P-1 to P-6); partly resolved 1 (N-5); not resolved 0.

## 4. Findings

There is no CRITICAL finding. Types: W, wording; M, a value moved in from the supplement; T, text the author writes from existing records; A, new analysis or evidence. No REQUIRED item is type A.

### REQUIRED-major

None.

### REQUIRED-minor

| ID | Location | Finding | Evidence quoted | Fix (fewest words) | Type |
|---|---|---|---|---|---|
| N-5 (residual; regression: new sentence) | II, Novelty (p. 3); S13 "Reading and record checks" | The new reading sentence says that every reference other than the five was read at abstract level. S13 lists seven that were not: the GitHub message definition, the author's manuscript, and the standards and regulations. [45]'s parameters (IV-A) come from its text. Section II's passive voice also hides what S13 says, that an AI system did the abstract-level reading. "Its publisher's page" does not fit arXiv or GitHub, whose records S13 says were checked against "their sources' own pages". | II: "the others were read at abstract level, and every reference's record … was checked against Crossref or its publisher's page"; S13: "an AI system read the others at abstract level, except [4], [10], [41], [42], [43], [44], and [45]" | "an AI system read 35 others at abstract level, and none of the seven without an abstract ([4], [10], [41]–[45]); every record but [10]'s was checked against Crossref or its source's page" (the author confirms the count). | W |
| O-4a (carried: my round-2 P-5; raised from optional) | II, "Uncertainty in prediction and planning" (p. 3); VI, "What a varying covariance needs" (p. 12); V-E, "Closed Loop With Dropouts" (p. 11) | The closest work in OJ-ITS reports a cut in collision risk of more than 66% from modelling misdetections. This paper finds about 3% of the room at equal caution, matched by a coast count, and finds that fewer closed-loop contacts under dropouts were not shown at equal time lost. [19] is cited twice, and the two results are never related. The record deferred this item to the author's full reading of [19], which is now done. The paper's own result is the natural bridge: at matched open-loop caution its covariance arm also had fewer contacts (21% against 33%), and the gap was not shown at equal closed-loop time lost. I have not read [19], so the author's reading must supply how its comparison was set (baseline margin, caution or progress matching, miss regime). | "cut collision risk by over 66% against a noise-only controller [19]" (II); "chance constraints can also account for misdetections explicitly [19]" (VI); "The fewer contacts thus cannot be told from a wider margin" (V-E) | Two sentences in VI: how [19]'s comparison differs from an equal-caution one, and that here the open-loop-matched gain (21% against 33%) was not shown at equal time lost. | T |

### OPTIONAL

Numbers P-7 to P-19 are from my round-2 report (the record's P-1 to P-6 are a different list). O-numbers are the record's.

| ID | Location | Finding | Evidence quoted | Fix (fewest words) | Type |
|---|---|---|---|---|---|
| Q-1 (regression) | II, Novelty (p. 3); tex line 123 | A stray space before the first citation. `(\cite{b13,b15}` typesets as "( [13]". It is the only citation placed directly after a parenthesis. | Page image p. 3: "in full ( [13], [15], [19], [35], [36])" | Rephrase as "in full: [13], [15], [19], [35], and [36];" or use `(\unskip\cite…`. | W |
| Q-2 (P-4 residual) | II, [27] sentence (p. 3) | The clause on a critical arrival rate is correctly qualified ("of an unstable system"), but it invites the reader to apply it here. From memory (confidence 3 of 5; the author checks [27], which was read at abstract level): for a constant-velocity model, whose eigenvalues lie on the unit circle, the covariance grows polynomially in a gap, and its expected value stays bounded for any positive arrival rate. Tracks here coast for at most three updates in any case. "Should match it" is also slightly strong: the covariance depends on the whole arrival history, and the coast count uses four factors. | "there is a critical arrival rate below which the expected covariance of an unstable system is unbounded [27]"; "a margin that counts missed updates should match it" | Add "(not the regime here: a constant-velocity model, coasted at most three updates)"; "should nearly match it". | W |
| Q-3 (P-1 residual) | VI, "What a varying covariance needs" (p. 12) | The sentence calls the lead-braking covariance "a constant". Two sentences later the same paragraph says that it grows under injected misses. | "in lead braking that makes it a constant"; "Under injected lead-braking misses the covariance grows" | "in nominal lead braking (regular updates) that makes it a constant". | W |
| Q-4 | S15, Table S43 | The paired peak-deceleration difference looks inconsistent with the per-arm medians. In a stop-behind-a-stopped-lead scenario both arms must brake hard, so a mean paired difference of about 3 m/s² is hard to square with medians that differ by 0.14. The main text does not use the value. | Per-arm "6.25", "6.11"; paired difference "−2.99 [−4.32, −1.74]" | Check the column, or explain it in one clause. | T |
| Q-5 | S11, Table S28; S4 | "Benign driving" and "stopped vehicle" are never defined. With fixed noise on a straight road, benign driving has only 60% of rows within 5%, which a reader will set against "with fixed noise and regular updates … nearly constant". Possible reasons are oncoming or young tracks and long-range misses; the text gives none. | "Benign driving \| 20‡ \| 40,120‡ \| 1.093‡ \| 60.45‡"; S4: "the 120 tuning runs of all six scenario families" | One sentence in S1.2 defining the six tuning families, and one clause in S11 on why benign driving varies. | T |
| Q-6 | V-E, "Detection Dropouts", 10 Hz paragraph (p. 11) | "Every arm keeps an unmatched track for up to three updates" plus masks of "5, 10, or 15 updates there" reads as if tracks die inside the 10 Hz windows. S15 says that the lead is output through every window. | V-E: "its masks last as long as the 2 Hz ones (5, 10, or 15 updates there)"; S15: "a coasting lead is output through every window" | Add "(a coasting lead is output through the window)". | M |
| Q-7 | V-C ¶2 (p. 8); Table 4 | "Safer at no extra cost" sits beside "pays in progress … losing 0.16 s more" (interval 0.10 to 0.22 s, above zero). The class name is the plan's tolerance, not zero cost. S15 already uses the clearer phrase. | "the braking prediction is safer at no extra cost (the plan's class; Table 4)"; S15: "time cost within the plan's 0.5 s tolerance" | "safer, with a time cost within the plan's 0.5 s" at first use. | W |
| Q-8 | Abstract (p. 1) | ±0.10 has no unit, while contribution 2 gives one. | "it is equivalent within ±0.10" | "within ±0.10 of contact share". | W |
| O-4b (carried: my round-2 P-4) | II or VI | Missed detections in target tracking enter through the detection probability of PDA ([26], [28]) and through track-existence or track-status measures (IPDA; unverified). The coast-count margin is the simplest such measure, which strengthens the designer message. | "Filters that account for data-association uncertainty [28] have a covariance that depends on the data" | One clause linking the coast count to track-status measures. | W |
| O-8 | Whole; V-E; VI Limits | The paper is 14 pages (body 8,229 words) against OJ-ITS's usual length of about ten. "Closed Loop With Dropouts" (p. 11) and VI Limits (p. 12) are still about 300 words each. | Page count; p. 14 half empty | Split those two paragraphs. Optionally tighten IV-E's departures accounting and Table 1 rows that repeat IV-A to IV-C. | W |
| P-7 | VI, "What a varying covariance needs" | NA is the simplest innovation-adaptive covariance. It recovers a few percent (0.024 fresh, 0.064 tuning), as much as the amendments' gains, but the "where it varies" story leaves it out. | Table 5 "NA share … 0.064 / 0.015 / 0.024" | One clause beside the adaptive filter (descriptive). | W |
| P-8 (part) | Abstract; Table 1 | "(position–velocity only)" is cryptic, and "two-noise IMM" is not a standard name: a tracking reader expects two CV modes with different process noise, not a CV/CA pair. | "(position–velocity only)"; "two-noise interacting-multiple-model tracker" | "(through its position–velocity covariance)"; gloss once as "CV and high-noise CA modes". | W |
| P-10 | VI; VII next steps | The two-noise IMM's lag after the stop is 0.40 m against 1.42 m, yet its braking-phase room equals the CV filter's (23.51 against 23.62). Its value lies mainly in the mean path, which a constant-velocity prediction from the mixed velocity discards. | Table 3: "0.40", "1.72 / 23.51 / 0.03" | One sentence in VI; add "an IMM's mode-conditioned prediction" to VII. | W |
| P-11 | Table 3, retuned-IMM row | The retuned IMM's maneuver mode is more probable after the stop (0.71) than during braking (0.39), so its "would classify as recovers" is not maneuver detection. | Table S42: "0.71 [0.70, 0.71]; 87%" | One clause. | M |
| P-13 | III-D | The tracker of record's own consistency is missing. Its lead-track NIS is about 0.5 before braking, 1.9 during it and 0.07 when stopped (one program). A covariance that is consistent on average in braking still ranks nothing, a useful point next to [30]. | Table S7: "0.49‡", "1.87‡", "0.07‡" | One clause in words (one program). | W |
| P-14 | II, "Uncertainty in prediction and planning" (p. 3) | Planning is downstream of perception, so "upstream" names the wrong direction unless [15] uses the word in its own sense. The author has now read [15] in full and can check it. | "a pipeline that propagates perceptual uncertainty upstream" | "propagates upstream (perceptual) uncertainty to the planner", or as [15] puts it. | W |
| P-15 | II (p. 3) | [24] is an INS/GPS application. Innovation-based noise estimation predates it (Mehra, 1970; unverified). | "innovation-based filters reestimate the noise [24]" | Cite the original beside [24]. | W |
| P-16 | S6.2 | Scaling all process noise by dt/0.5 is exact only for a diagonal discrete Q. For white-noise acceleration the blocks scale as dt³, dt² and dt. | "with its process noise scaled by dt/0.5 (sensitivity: unscaled)" | State CANMOT's Q form, or call the scaling an approximation. | T |
| P-17 | V-D, "Update rate and latency" (p. 8) | The comparison mixes latencies. At equal 0.1 s latency the fall is larger (227.1 to 77.8). | "falls from 173.4 decision-equivalents at 2 Hz to 77.8 at 10 Hz with the plan's 0.1 s latency"; Table S16 "2 Hz, 0.1 s … 227.1" | Add "(227.1 at 2 Hz with the same latency)". | M |
| P-18 | VI, "Which commitment applies" (p. 12) | Three sources are named just before "the two", so the antecedent is ambiguous. | "so the closed loop does not decide between the two" | "between the two open-loop commitments". | W |
| P-19 | Table 6, first-amendment closed-loop row (p. 10) | "Equivalent" carries neither "(A)" nor "descriptive", so its status in the first amendment's sequence is unclear. | "equivalent" | Add its status. | W |

**Counts:**
- REQUIRED-major: 0.
- REQUIRED-minor: 2 (N-5 residual; O-4a). Neither is new (Q). One is a regression (N-5's new sentence).
- OPTIONAL: 21, of which 8 are new (Q-1 to Q-8; Q-1 is a regression) and 13 are carried (O-4b, O-8, P-7, P-8, P-10, P-11, P-13 to P-19).
- CRITICAL: 0.

```yaml suggested-references
# All from memory; none checked (no web access). Each must be verified and read before use.
- {authors: "D. Musicki, R. Evans, S. Stankovic", title: "Integrated probabilistic data association", venue: "IEEE Trans. Autom. Control", year: 1994, status: unverified, for: O-4b}
- {authors: "R. K. Mehra", title: "On the identification of variances and adaptive Kalman filtering", venue: "IEEE Trans. Autom. Control", year: 1970, status: unverified, for: P-15}
```

## 5. Q1 to Q8, briefly: what changed since my round-2 report

**Q1. Labels and sizes.**
- The abstract now gives the twin difference its unit ("0.05 of the room") and its reading ("a timing effect").
- Table 4 marks which classes are tests (note ^c^).
- Holm stays beside the labels and changes none.
- Left: the first-amendment closed-loop row's status (P-19) and the abstract's ±0.10 without a unit (Q-8).

**Q2. Overreach.** Every round-2 overreach in my domain is fixed:
- the abstract's first sentence is scoped to "one speed planner predicting at constant velocity (straight road, 5 to 15 m/s)";
- the "regular updates" qualifier stands in the abstract, I and VI ¶1;
- II no longer says "alone";
- the twin claim is limited to timing.

On the five points the launch message named:
- **Scope of the null.** It stays on the narrow side: "It concerns this covariance, not uncertainty in planning in general [15]" (VI); "This does not justify replacing per-track covariances by class averages" (abstract).
- **Margin interface.** It is explicit, with "no process noise is added over the look-ahead" (III-E) and "a wider one … was not tested" (VI).
- **Closed-loop and dropout statements.** They are accurate: "fewer closed-loop contacts were not shown at equal time lost"; "matched at 2 Hz by a coasting margin … a level effect".
- **NA/TG/AM order.** It is now shown in all three run sets (Table 5).

Residuals are wording only: Q-2, Q-3 and Q-7.

**Q3. Earlier limits.** The structural limits are unchanged and disclosed:
- a confirmed null that was expected ("what the test adds is the bound");
- small effects;
- one configuration at 2 Hz;
- no real-log decision test;
- post-results amendments, local locks and AI authorship.

These are limits of the study, not of the text. Section II now states the reading behind the related work. The one test that would lift significance, a covariance on top of the braking prediction's path, stays a next step in VII (type A, optional).

**Q4. Readability.** The split paragraphs (IV-C, IV-E, V-C, Detection Dropouts) read much better. CANMOT is expanded at first use, "level effect" is defined in IV-C, and "steady decisions" is defined in V-E. The abstract is still dense for an ITS reader, though better. "Two-noise IMM" and "(position–velocity only)" remain (P-8). Every claim's evidence can now be found in the main text.

**Q5. Verdict.**
- Minor revision, 7.0 / 10 (★★★½☆).
- Most likely outcome at OJ-ITS: minor revision.
- The single change that would raise my score most: two sentences in VI that relate [19]'s result to this paper's open-loop-matched and equal-time-lost closed-loop results (O-4a). This turns the paper's main method point, that equal caution matters, into a direct comment on the closest result in the journal.

**Q6. Self-contained main text.**
- The round-2 case is closed: V-D's cross-set order now rests on Table 5 (P-5).
- No new case. Q-6 is a clarity detail, not a missing result.
- The two one-program tuning values stay described in words, under the paper's stated rule.

**Q7. OJ-ITS format and declarations.**
- N-20 (6) is resolved.
- New: the stray space "( [13]" (Q-1).
- Checked and correct on the page images:
  - capital section and subsection heads, and title-case subsubsections ("1) Pedestrian Crossing");
  - "Fig. N" in text and "FIGURE N." in captions;
  - Arabic table numbers;
  - the ACKNOWLEDGMENT in the order responsibility, data and code, AI disclosure, declarations;
  - funding on the first page;
  - running head with a short title;
  - five index terms;
  - abstract 235 words (the brief's build facts) with no abbreviations;
  - abbreviations defined at first use (CANMOT, CV, CA, IMM, NIS, CARLA, AI, SHA-256);
  - tables fit their columns.
- Advisory:
  - white space above the level-3 heads on pp. 9 and 11;
  - p. 14 holds half a column of references;
  - wrapped row labels in Table 5 ("Nonbraking leads", "Recording policy") leave visually empty rows (p. 9).

**Q8. AI disclosure.**
- N-1 is fixed.
- "Claude models, among them these three" replaces the unsupported "the same three models".
- "Section II states what the author read in full" links the disclosure to the reading statement. That statement now needs to agree with S13 (N-5 residual).
- Optional, carried: "after the systems had judged the manuscript ready" still suggests that the systems judged readiness.
- The disclosure meets IEEE's rule, and a desk rejection on it is unlikely.
