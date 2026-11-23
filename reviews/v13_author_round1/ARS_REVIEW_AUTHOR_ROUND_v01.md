# ARS review, author round: panel record (editor synthesis), v01

- **Text reviewed:** revision v13, package of 22 Nov 2026 18:30 EST (`package_v13_1830`; 13 typeset pages; supplement PDF 43 pages).
- **Synthesis seat:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), skill standards of `academic-research-skills:academic-paper-reviewer`. Read only; no sub-agents, no web, no seat re-run, no manuscript text sent anywhere. No process was run other than file hashing and text searches (one at a time).
- **Written:** 22 Nov 2026 19:02 to 19:30 (clock from Get-Date at 19:01:57). No target score was given to me or to the seats.
- **Checks I made in the package** (beyond reading the ten seat files): the ACKNOWLEDGMENT in full; the three amendment passages named in the brief; abstract, Section I, VII, Table 2 and Fig. 2 (page 7 image); text searches that confirm what is and is not in the main text for each Q6 case; supplement S12, S13, S29, Table S5 rows and S36; template lines 180, 195-197, 463-467, 518-519. Where a seat's finding is kept below, I say what I found.

## 1. Seat table

| Seat | Model | Recommendation | Score /10 | Stars /5 | REQUIRED-major | REQUIRED-minor | OPTIONAL |
|---|---|---|---|---|---|---|---|
| EIC, journal fit | Claude Sonnet 5.5 | major | 5.8 | 2.9 | 3 | 14 | 13 |
| R1, methodology | Claude Fable 5.2 | minor (upper edge) | 6.6 | 3.5 | 2 | 10 | 11 |
| R2, domain | Claude Opus 5.5 | major | 6.0 | 3.0 | 2 | 12 | 10 |
| R3, practical | Claude Sonnet 5.5 | major | 6.3 | 3.2 | 2 | 10 | 8 |
| DA, devil's advocate | Claude Fable 5.2 | major | 5.5 | 3.0 | 5 | 10 | 12 |

Counts are the seats' own tables, before my adjudication. No seat marked a CRITICAL finding.

## 2. Panel decision and score

- **Decision: major revision.** Four seats say major; R1 says minor and calls itself the upper edge of minor. R1 is also the seat that checked 404 printed values against the exports. I accept its finding that the numbers are sound, but I do not accept minor: five items below are substantive (a declaration the deposited records contradict, a tested quantity that is defined nowhere, an abstract that overstates its own tests, a self-containment sentence that is false as written, and references characterised from abstracts).
- **Seat mean: 6.04 / 10 (3.12 stars).** Range 5.5 to 6.6.
- **My own judgement: 6.1 / 10 (3.1 stars).** I land at the mean for these reasons.
  - I weight R1's 6.6 upward because its numeric verification is the best evidence in the panel, but R1 also scored the paper as if the Acknowledgment fix and the twin definition were small, and I find both real.
  - I weight DA's 5.5 downward: its estimate of about one in three for a desk rejection is not supported by the text (see section 11), and half of its significance case is a structural limit the paper states itself and does not hide.
  - EIC's 5.8 rests partly on the abstract and Q6 findings, which I keep, and partly on format counts that I mostly rate advisory.
- **Against the earlier panel's 6.3 (12:01 text, same scale).**
  - *What moved the score up:* the earlier panel's required items are almost all done (16 resolved, 3 partly, 0 not; section 9). The text now holds Table 6, the pedestrian scenario, the definitions of time lost and rest gap, the coast-count factors, the IMM secondary and the Holm scope. This is a real improvement in what a reader can verify.
  - *What moved it down:* (a) the author's new Acknowledgment sentence claims more than the records show, so the one earlier item on which the text got worse is also the one a deposit reader will meet first; (b) the added material raised density (V-E about 1,220 words; 13 pages) and opened new self-containment gaps; (c) the seats found a second round of wording, label and format problems of about the earlier panel's size.
  - *What did not change:* the structural limits. A confirmed null that could hardly fail; 2% to 5% effects, small by the paper's own margin; one simulator, one planner, one configuration; no decision-level real-log evidence; amendments after results with internal locks; AI-written text. None of these can be fixed by editing, and they set the ceiling.
  - *Net:* the earlier 6.3 and today's 6.1 are within the spread between seats (0.5 to 1.1 points). I read the change as "no real movement in the score, a clear movement in what remains to be done". The seats differ in strictness from the earlier panel, so I do not call it a fall.

## 3. CRITICAL items

None. I checked the two candidates.
- **DA's structural objection** (the one confirmed result could hardly fail; everything else comes from amendments written after the first results): this is an objection to significance, and the paper states each part of it ("expected from this constancy", "amendment tests followed the first results", the two failed controls in the abstract). It would not by itself justify rejection of a paper that discloses it. Not critical.
- **The Acknowledgment sentence** (N-1): it is wrong in a way the author can fix in four words, and the paragraph's own later clause already concedes the point. Not critical; but it is the first item to fix.

## 4. Disputes between seats, with my rulings

| # | Dispute | Ruling | Facts checked |
|---|---|---|---|
| D1 | Recommendation: R1 minor, four seats major. | Major. | See section 2. Five major items hold up on my check (N-1 to N-5). |
| D2 | DA R-M5: score N and the class average on the braking prediction's path (type A) as REQUIRED-major. | **Not required; OPTIONAL (A), O-1.** | The abstract says "with a constant-velocity prediction"; VI says the room "lies almost wholly in braking" and that a covariance on top of the braking path "was not tested"; VII lists it as a next step. The limit is stated four times. A wording-only fix (say in the abstract that the room is mostly prediction error) is already partly there. The test would raise the score; its absence does not stop "accept". |
| D3 | R2-M2: the margin omits process noise over the look-ahead; the maneuver mode is a CA filter whose acceleration is dropped; the abstract and VII state 2.2% and 4.6% without that. Stronger option: rerun (A). | **Wording is REQUIRED (minor, N-6, with the abstract part in N-3); the rerun is OPTIONAL (O-2).** | III-D (line 88) says "acceleration terms never reach the margin"; V-E (line 230) and VI (line 265) say a wider interface was not tested. So the limit is disclosed. What is missing is the omitted process noise term and the CA mode's description, which are in S15 (line 890) and not in the main text. R2 rated this major; I downgrade because the limit is stated and the missing pieces are two sentences. |
| D4 | R3-2: closed-loop baseline and cost columns (peak deceleration, jerk, rest gap, fallback share) belong in Table 4; R3 rated major. | **REQUIRED-minor (N-13).** | V-C already gives the fallback shares (52.7% and 78.6%) and says costs to following traffic and occupants are not scored; the numbers are in S23 and S24, and the claim "equivalent" is not changed by them. A referee wants the columns; none would reject on their absence. |
| D5 | R2-M1: NA, AM and TG are announced in Table 1 and Fig. 1 and never reported in the main text (AM recovers 37%, Table S8). R2 major; EIC (o7) and R3 (R3-10) would delete NA and AM instead. | **REQUIRED-minor (N-14): report them or drop them.** | Confirmed that NA and AM are defined in Table 1 and appear in no result sentence; V-D (line 196) claims "the sources' shares keep one order", whose values for NA, AM and TG sit in Tables S8, S12, S13. Either carry the order and three numbers, or delete NA and AM and say TG is in S5. The paper's contributions do not rest on them. |
| D6 | EIC J3 and DA R-M4: references read at abstract level; R1, R2 and R3 do not raise it as required. | **REQUIRED-major (N-5), type T, author-only.** | S13 (line 699): "no full text was opened"; the ACKNOWLEDGMENT says Claude "ran the literature searches". Section II characterises [19], [35], [36] and states a negative novelty claim from them. IEEE expects the author to stand behind what the paper says about a cited work. The fix is the author's reading, not an analysis. |
| D7 | EIC m7: the first adaptive-twin test is labelled "(A)" although specified after the values were seen; wants "post hoc, descriptive". | **Dropped.** | Table 6 already reads "(A), post hoc" for the fresh-run test and "replicated, H 0.0003" for the new-run test (line 250); V-E says the test was "specified after its fresh share ... had been seen". The label is already honest. |
| D8 | "multi-object": EIC, R1, R2, DA say miss; R3 says style call (the template says "usually"). | **REQUIRED-minor format item, in N-20.** | Template lines 195-197 name the prefix "multi" and say "usually without a hyphen". Occurs in the abstract, Section I and Section II ("mid-rank" in IV-E too). Four seats found it; reference titles ([5], [31], [32]) keep their own spelling. |
| D9 | Q7-16 (ZIP code), Q7-17 (bold run-in heads), Q7-18 (supplement headings), Q7-13 (CANMOT). | **Advisory or not applicable.** | R1, R2, DA call the ZIP unnecessary for an independent researcher; run-in heads are not a template rule; the supplement is typeset outside the template (sup01 per seats); CANMOT is a published name. |
| D10 | Desk-reject risk on the AI paragraph: EIC about 5%, DA about one in three. | **About 10%, and that risk comes mainly from N-1.** | The paragraph discloses system, sections and level; nothing names an AI as author. The exposure is the stack of AI-run work plus the one sentence that the records contradict. |
| D11 | R1 and DA: the Acknowledgment sentence "made every scientific decision". EIC, R3, R2 rate it minor or note it under Q8. | **REQUIRED-major (N-1).** | See the ruling in section 8. |
| D12 | S12 versus the Acknowledgment on who audited. | **REQUIRED-minor (N-7).** | S12 line 695: "an agent on a model other than the writer's audited every sentence". The ACKNOWLEDGMENT says Fable 5.2 and then Sonnet 5.5 audited, and names Fable 5.2 among the models that drafted and revised text. S12 names no model and no order. The two cannot be checked against each other as written. |
| D13 | EIC m14 (table footnote letters) and the "while" item. | Footnote letters REQUIRED-minor (the brief says tables follow the template; template 518-519 says "Use letters for table footnotes"); "while" advisory (template line 180, one word). | Tables 2, 4, 6 carry † and * inside captions (Table 2 caption seen on page 7). |

## 5. REQUIRED items, N-1 onward

Type: W wording; M a value moved in from the supplement; T text the author writes from existing records; A new analysis or evidence. Where an item mixes types, the first is the main one. Raised-by uses the seats' own IDs. Every item below was checked against the text; what I checked is in the last column.

### REQUIRED-major (5)

| ID | Location | Seats | Fix, fewest words | Type | What I found |
|---|---|---|---|---|---|
| N-1 | ACKNOWLEDGMENT, sentence 1 | R1 RM-2, DA R-M1, EIC m13, R3-6b, R2 (Q8 and R-12) | "made every scientific decision" becomes "made or approved every scientific decision". The author confirms the facts first (section 8 gives the check and a fallback). | W (author confirms) | Text line 273 has "set its questions and plans, made every scientific decision"; the same paragraph then says design choices the files record as an AI session's "were made within the author's approval". Amendment files record some as the coordinator's (A11 line 182; A12 line 406; A13 line 197). |
| N-2 | Section I contribution 2; V-B; V-E adaptive-filter paragraph; Table 6 row "share minus permuted twin's"; Table S36 | R1 RM-1 (only seat to read the plans) | Add two sentences (IV-C or V-E): what the per-decision factor is, that it is permuted within runs, 20 twins averaged, and what null the difference tests. Source: AMENDMENT_11 section 6b. | T | Main text defines a permuted twin only for the oracle ("E5p permutes that order within runs", line 110). No main-text or supplement definition exists for the tracker's twin (searched; Table S36 uses the term bare). It is a Holm primary and is named in the contributions. |
| N-3 | Abstract; Section I contribution 2 and "For a designer"; VI; VII | EIC J1, m8, m10, m11; R1 Rm-2, Rm-3, Rm-4; R2 m2, m8, m9; R3-1, R3-3, R3-4; DA R-M2, R-M3, R-m4 | Make the summary sentences carry the size and status the body gives. Parts: (a) mark 4.6% as a descriptive share (Table 3) or use the tested twin difference 0.05; (b) say shares are against each tracker's own class average and, as point values at start probability 0.10, inside the ±5% margin; (c) coast-count: "slightly more of the room (interval below zero)", "with factors taken from the covariance's own median growth", "at 2 Hz"; (d) 78% "(38% to 84% across run sets) at a cost in progress behind leads that do not brake hard"; (e) name the planner ("one longitudinal speed planner") and the position-velocity interface for the IMM result; (f) "at desired speeds of 5 to 15 m/s on a straight road"; (g) closed loop: "contact rates far above any deployable level", "within ±0.10 (60 cases)"; (h) last sentence: say what was replaced ("the per-track covariance by its class average"); VII: "showed no recovery" for "recovered nothing". Lead the abstract with the answer; stay at or under 250 words. | W | Abstract read in full: it lists "4.6%" among "three lead-braking tests"; Table 3 line 153 labels it "descriptive". V-E line 228 says "recovered as much ... −0.0024 [−0.0057, −0.0001]". VII line 269 says "recovered nothing of a small room" where Table 6 has −0.067 [−0.221, 0.034]. Abstract has no planner scope, speed range or 78% range (Table 5: 0.379 / 0.837 / 0.783). VII does carry the progress cost; the abstract does not. |
| N-4 | Section I, "The main text holds every result on which the claims rest" (line 52), and the Q6 cases in section 7 | EIC J2; R1, R2, R3, DA (Q6) | Bring in the tier-1 facts of section 7 (one or two sentences each), or soften the sentence. | M | Searches confirm absence from the main text of: the maneuver-mode variance 0.917 and transition diagonal 0.95; the adaptive filter's clip(0.25, 10) rule; the decomposition's sample (58,970 decisions, 366 runs) and Shapley method; the 29,926 new-run decisions; the one-factor coast-count variant 0.0347; "capture had begun"; the classification pass rule; the 10 Hz class average. |
| N-5 | Section II "Novelty, with its limits" and the ACKNOWLEDGMENT; S13 | EIC J3, DA R-M4 | The author reads in full the works the paper characterises ([13], [15], [19], [35], [36] and the closest others), corrects II if needed, and writes one sentence: how many references were read in full, how many at abstract level, and that every reference was checked against its publisher or Crossref record. | T (author-only) | S13 line 699: "no full text was opened"; "what the paper says about them stays within those abstracts". Section II: "makes no such comparison". |

### REQUIRED-minor (15)

| ID | Location | Seats | Fix, fewest words | Type | What I found |
|---|---|---|---|---|---|
| N-6 | III-E; V-E two-noise IMM paragraph; VI Limits | R2 M2, EIC C1, R3-7 | Say the margin $s = z^\top P z$ omits process noise over the look-ahead; say the maneuver mode is a constant-acceleration filter (variance 0.917, NIS-tuned on braking frames; own class average) whose acceleration and mode-conditioned prediction do not reach the margin. | M (S15, Table S41) | See D3. |
| N-7 | ACKNOWLEDGMENT; S12 "Claim audit" and "Second programs" | EIC m13, R3-6a, R2 (Q8), DA R-m6, R1 | Name the model(s) of the presubmission AI panel; in S12 name which model wrote and which audited each pass, or drop "other than the writer's" where it does not hold; make the sentence "reviews and responses are deposited" true at submission. | T | See D12. The panel is named only as "an AI panel" (line 273; IV-E "AI review panel"). |
| N-8 | IV-E; ACKNOWLEDGMENT; S12 first paragraph | EIC m12, R2 m12, R1 Rm-7 | One scope sentence everywhere: "every result value printed in the main text and all but the marked (‡) values of the supplement", plus "the scoring library was checked by hand on 20 decisions (S12)". | W + M (S12) | S12 line 528: "Every value printed in the Abstract, Sections I and V-VII ... and every supplement value they cite" differs from IV-E line 118. |
| N-9 | Section I, paragraph 4 (line 42) | R1 Rm-1 | Name the original families (lead braking, cut-in, nonbraking leads); add "a later amendment added pedestrian crossing". | W | Line 42 lists pedestrian crossing among families "recorded and scored once under a plan fixed in advance"; V-E says it was tested "despite the prestated no-go". |
| N-10 | V-E; Table 6 "replicated" | R1 Rm-5, DA R-m2 | "under rules fixed before any new run was extracted or scored (capture had begun)". | W + M (S15) | S15 says so; main text says "fixed before the data". |
| N-11 | Section I, V-E, VI, VII | EIC m9, R2 m10, R3-10, R1 Rm-3 | Define "level effect" once (a margin raised for an identifiable group of decisions, with no ranking inside the group); VI: "partly" where V-E says partly; add "at 2 Hz". | W | "level effect" occurs at lines 52, 228, 236, 269; no definition. |
| N-12 | Table 6; V-E | R1 Rm-6, Rm-9; EIC o10; DA R-m9; R2 o5 | Add a row for the first amendment's closed loop with dropouts (60 cases; −0.03 [−0.10, 0.03]; 0.15 [0.08, 0.24] s; equivalent; Table S35); name the slope "least-squares slope of the share on the start probability (four values)"; flag that the closed-loop row is not matched in closed loop. | M (S14 Table S35, S15) | Table 6 title is "Tests of the three later amendments"; the passed closed loop has a row and the null has one sentence. Slope called "dropout rate" in the table, "start probability" in IV-E. |
| N-13 | V-C; Table 4 | R3-2 | Add peak deceleration, rest gap and fallback share for F0, N, CK3, TG at both levels (or a compact table); two sentences on who bears each cost; time lost as a share of the 25 s run. | M (S23, S24) | See D4. |
| N-14 | Table 1, Fig. 1, V-A, V-D | R2 M1, EIC o7, R3-10 | Report NA, AM, TG fresh shares with intervals and the order (N < NA < TG < AM < CK3 per R2), or drop NA and AM and point to S5. | M (Tables S8, S12) | See D5. |
| N-15 | III-D; Table 3 | R2 m4 | One sentence with the braking-phase NIS of the retuned filters (7.9 to 9.6 against an expected 2; exploratory), and say the two-noise IMM is the variant tuned for consistency during braking. | M (S4, Table S7) | Table 3 row reads "retuned (median NIS near 2)"; S4 says no run lies inside the window (seat quote; I did not open Table S7). |
| N-16 | V-E nuScenes paragraph | R2 m5, DA R-m1 | State which classes enter the pairs and whether pairs cross classes (if they do, give within-class tau or write "not stratified by class or motion"); say the primary population was chosen after the all-pairs statistic was negative on the training split (about −0.011), and that one of the six Holm entries had its population rechosen. | T (becomes A only if within-class tau is requested) | Line 236 reads "after the all-row statistic there was found to be dominated by steady tracks". AMENDMENT_12 line 406 records the −0.0108 figure and the choice as the coordinator's on training data. |
| N-17 | Section II, [27] sentence | R2 m1 | "a critical arrival rate below which the expected covariance of an unstable system is unbounded [27]"; add that with fixed noise the covariance is a function of the arrival sequence, so a coast-count margin was expected to match. Author checks [27]. | W (author checks) | Text says "beyond which". I cannot check the reference offline; R2's reading of its direction is plausible and the wording is ambiguous either way. |
| N-18 | Supplement Table S5 "slips" row; Table S29 | DA R-m7 | Add the third stated time that is later than its lock's file time. | T | AMENDMENT_13 line 41: "Dropped by decision (coordinator, 06:52)"; Table S29 line 682: file time 22 Nov 06:47:56 (hash bc7c2bf4...). S5 lists two slips, both in the second amendment. |
| N-19 | Table 1 (page 2), row NA | EIC m6, R1, R2, R3-10 | Define NIS at first use (or in Table 1's legend). | W | Table 1 line 36 uses "NIS inflation"; the definition is at III-D (line 88). |
| N-20 | Q7 misses I rate REQUIRED (details in section 8) | all five | (1) ACKNOWLEDGMENT order; (2) Fig. 2 panel labels (a), (b); (3) "multiobject", "midrank"; (4) table footnote letters under Tables 2, 4, 6; (5) comma after "?" in [21]; (6) one surname form across byline, running head and [10]. | W | Section 8. |

## 6. Type-A statement

**No REQUIRED item is type A.** Every one of N-1 to N-20 is wording (9 items), a value moved in from the supplement (6) or text the author writes from existing records (5). Two items could turn into A only if the author chooses the stronger route: within-class tau in N-16, and the process-noise rerun noted in O-2. Neither is required.

Type-A items do exist, and they bound the score above about 7 (section 12): a covariance added on the braking prediction's path (O-1), a rerun with process noise in the predicted covariance (O-2), a real-log decision test with room (O-3). They are OPTIONAL. They do not withhold "accept as is"; the REQUIRED W, M and T items do.

Counts of REQUIRED items by type (main type): W 9, M 6, T 5, A 0; total 20 (5 major, 15 minor).

## 7. Q6, self-containment: one deduplicated list, each case checked

Method: for each case I searched the main text for the fact (for example "0.917", "clip", "Shapley", "58,970", "29,926", "0.0347", "had begun", "passes unless", "0.95") and found it absent. "Tier 1" means a claim reads differently without the fact; do these under N-4. "Tier 2" is one clause each.

| # | Main-text location | Rests on (supplement) | Fact to bring in | Seats | Tier |
|---|---|---|---|---|---|
| 1 | V-E two-noise IMM; abstract's 2.2%; contribution 2 | S15, Table S41 | Quiet mode = CV filter of record; maneuver mode = CA filter, acceleration variance 0.917, NIS-tuned on braking frames (median 1.997); transition diagonal 0.95; own class average | EIC C1, R2 #2, R3-7 | 1 |
| 2 | III-D, V-B, V-E: adaptive filter | S4 | Velocity process noise scaled by clip(m, 0.25, 10), m = mean NIS/2 over the last at most 3 position updates | EIC C2 | 1 |
| 3 | Contribution 2, V-B, V-E, Table 6: tracker "permuted twin" | none (plan only) | The definition (N-2) | R1 | 1 |
| 4 | V-E dropouts; abstract; VII: "level effect" | S15 (one-factor variant) | One-factor margin recovers 0.0347 [0.0109, 0.0581]; covariance minus it −0.0049 [−0.0094, −0.0006] (descriptive) | R1 #9, R3-8, R2 o4 | 1 |
| 5 | V-E 10 Hz sentence | S15 "Dropouts at 10 Hz" | Class average is the 2 Hz one under 2 Hz masks; masks are 5 to 15 missed updates at 10 Hz | R1, R2, DA | 1 |
| 6 | V-E "under rules fixed before the data" | S15 | Capture had begun before the lock; rules fixed before extraction and scoring | R1, DA | 1 (N-10) |
| 7 | V-E pedestrian: "54%, 38%, 8%", "mostly for other reasons" | S15, Table S46 | Variables in each group (geometry; update schedule; realized error); sample 58,970 decisions of 366 runs; Shapley shares | EIC C3, R3-9 | 1 |
| 8 | V-E nuScenes: tau within scene and keyframe | S15, Table S45 | Realized error = error of 3 s CV prediction; "all pairs" versus "around misses"; classes in pairs | EIC C4, R2 m5 | 1 (N-16) |
| 9 | V-E "An earlier closed loop with dropouts ... found equivalence" | S14, Table S35 | −0.03 [−0.10, 0.03]; 0.15 [0.08, 0.24] s; 60 cases | R1 #4, DA #5 | 1 (N-12) |
| 10 | IV-E "confirmed"; Table 6 "(A)" on classes | Table S4 | A classification step passes unless the class is inconclusive | R1 #2 | 1 |
| 11 | V-D "the sources' shares keep one order" | Tables S8, S12, S13 | NA, AM, TG shares and the order | R2 #1 | 2 (N-14) |
| 12 | II "In the sources we searched (Supplement S13)" | S13 | Limits of the search: English only, one engine blocked, abstract-level reads, no full text | EIC C7, DA #4 | 1 (N-5) |
| 13 | V-C and Tables 4, 5: "costs progress", contact differences behind nonbraking leads | S8, S9, S23, S24 | The rule and the intervals; the 60 nonbraking closed-loop contact differences | EIC C5, C6, R3-2 | 2 (N-13) |
| 14 | IV-E recount scope | S12 "Hand-checked decisions" | 20 decisions recomputed without the scoring library, all within 1e-6 m | R1 #5 | 2 (N-8) |
| 15 | IV-E "mid-rank" | S2 | mid-rank u = (rank − 0.5)/n_r over decisions with such rows (0.5 without) | EIC C8 | 2 |
| 16 | IV-B "201 caution levels" | S2 "Frontiers" | Range of the levels (equally spaced from F0's zero-margin caution to the smaller of F0's and E's largest) | R2 #4 | 2 |
| 17 | IV-A "first truly safe row in cost order" (line 102) | S1.1 | The 17 rows (16 pairs of target accelerations from {−5, −2, 0, 2} m/s² plus one) and the cost's three terms | DA #1 | 2 |
| 18 | III-B and Table 4 "caution matches there / design runs" | S2 "Matched settings" | Matched on the old evaluation runs | R1 #8 | 2 |
| 19 | Table 6 slope row | S15, Table S39 | Least-squares slope on start probability, four values | R1 #7 | 2 (N-12) |
| 20 | Table 6 row labels | S15, Table S33 | Decision counts (29,926, of which 5,085 inside a dropout; 105,419 in crossing) | R1 #10 | 2 (optional) |
| 21 | V-D "stays inside the margin at every rate and latency" | S6, Table S16 | The range over the other settings, one clause | DA #6 | 2 |

Pointers that only offer more detail (S1 configuration, S3 plan text, S5 full tables, S6, S10, S14) are not cases. The recount's shared-library limit is already in the main text.

## 8. Q7, format and declarations: one deduplicated list

Checked against the text, a page image (page07 seen by me; the other pages as the seats report) or the official template (`ojits-template.tex`). The repository and DOI placeholder, the publisher-filled lines and the missing biography are not counted.

| # | Miss | Location | Check | Status |
|---|---|---|---|---|
| Q7-A | ACKNOWLEDGMENT order. Responsibility and AI disclosure are in paragraph 1, data and code in paragraph 2, declarations in paragraph 3. Required: responsibility, data and code, AI disclosure, declarations. Make the AI disclosure its own paragraph, third. | pp. 11-12; lines 273-279 | Text read in full | **REQUIRED** (N-20) |
| Q7-B | Fig. 2 has two panels and no (a), (b); the caption says "Right:". Fig. 4 has them. | p. 7 | Page 7 image: no labels; template 393-396 | **REQUIRED** |
| Q7-C | "multi-object" (abstract, Section I twice, Section II); "mid-rank" (IV-E). Join the prefixes; reference titles keep their own spelling. | pp. 1, 2, 3, 5 | Template 195-197 | **REQUIRED** |
| Q7-D | Table footnotes are symbols in captions (Tables 2, 4, 6); use letters in a note row under the table. | pp. 7, 8, 11 | Table 2 caption on page 7; template 518-519 | **REQUIRED** |
| Q7-E | NIS used in Table 1 before its definition (N-19). | p. 2 | Text lines 36, 88 | **REQUIRED** (N-19) |
| Q7-F | [21]: comma after the question mark ("driving?,"). | refs | Text line 321 | **REQUIRED** (trivial) |
| Q7-G | [10] gives "A. S. K. Kopalli"; byline and running head give "Kopalli Naga Venkata". Use one form so the self-citation is recognisable. The author chooses the form. | page 1, running head, [10] | Byline and running head as the seats report; [10] as quoted by EIC, R1, R3, DA | **REQUIRED** (author decides) |
| Q7-H | "while" used contrastively (V-E, "most of the gain, while among those decisions alone"). Use "whereas". | p. 8 | Template 180; text line 228 | advisory |
| Q7-I | Bold sentence-case run-in heads in II and VI. | pp. 3, 10-11 | Not a template rule; R1, R2, R3, DA call it unnecessary | advisory |
| Q7-J | "et al." in [9], [13], [15], [21], [34]; the template says list all names, IEEE allows "et al." beyond six. The author counts authors. | refs | Template 495 | advisory (author check) |
| Q7-K | Fifteen conference references carry no city, country or month. | refs | Template 722-723 | advisory |
| Q7-L | arXiv IDs with and without a version ([5], [15], [40] against [32]). | refs | Seats | advisory |
| Q7-M | [47] has no month; [45] is a UN proposal document with no access note; [43] and [44] have no corporate author while [45] has one. | refs | Seats | advisory |
| Q7-N | Table and figure type below 8 pt (tables about 7 pt, Fig. 1 about 6 pt). | pp. 2, 4, 7-9, 11 | Seats | advisory |
| Q7-O | Affiliation has no ZIP; ORCID inside the affiliation parentheses. | p. 1 | Template 24-27; three seats call it unnecessary | advisory |
| Q7-P | "position-velocity" hyphen once (III-D), en dash elsewhere; CANMOT not expanded in the body; abstract is 245 words by whitespace and over 250 if hyphens split words. | text | Seats | advisory |
| Q7-Q | Length: 13 pages against a recommended ten (S5 says the journal sets none and recommends ten). | whole | S5 | advisory (author decides) |
| Q7-R | Supplement headings in title case; supplement not in the template. | supplement | R1, R2, R3, DA | not applicable |

Checked and in order (agreed by the seats and spot-checked by me): section and subsection heads in capitals; "Fig. N" in text and "FIGURE N." in captions; Arabic table numbers; funding in the first-page note with no Funding heading; one ACKNOWLEDGMENT; running head; five index terms in alphabetical order; arXiv form, "Accessed:" on [4], [10] "submitted for publication"; "preregistered" in one spelling.

**Total:** 7 REQUIRED misses (grouped as N-20 and N-19), 10 advisory, 1 not applicable.

## 9. The earlier panel's R-1 to R-19, checked on the 18:30 text

Each seat's Phase 2 verdict is in the table; the ruling is mine, after checking the quoted text.

| ID | EIC | R1 | R2 | R3 | DA | Ruling | Evidence from the 18:30 text |
|---|---|---|---|---|---|---|---|
| R-1 | res | res | res | res | res | **Resolved** | V-E: coast-count factors "(0.216, 0.107, 0.065; 0.925 after reacquisition) are the median ratios ... fitted on the 105 earlier runs"; "a level effect that needs no per-decision covariance"; 10 Hz "not compared". |
| R-2 | res | res | res | res | res | **Resolved** | V-E: IMM "0.210 [0.158, 0.255] ... around misses and 0.093 [0.066, 0.116] over all pairs"; abstract "the fixed-noise tracker's spread". |
| R-3 | part | res | res | res | part | **Partly** | V-E has "as point values, inside the ±5% equivalence margin" and "about 5% at 0.20 and 0.30". The item named the abstract and VII; neither carries the clause (abstract has "about 5% at higher rates"). Carried by N-3. |
| R-4 | res | res | res | res | res | **Resolved** | V-E "holds for the position-velocity interface only; a wider interface was not tested"; "lower bound" gone. Remaining gap is N-6. |
| R-5 | res | res | res | res | res | **Resolved** | Abstract "with a constant-velocity prediction"; VI "room lies almost wholly in braking (1.63, 23.62, 0.08 points)"; next steps in VII. |
| R-6 | res | res | res | res | res | **Resolved** | IV-E: original sequence "not Holm-adjusted"; six Holm primaries named (H rows of Table 6). |
| R-7 | res | res | res | res | res | **Resolved** | Table 6: "failed, Holm 0.99", "failed, Holm 0.18". |
| R-8 | res | res | res | res | res | **Resolved** | Abstract two-sided; VII rewritten for a designer. 245 words. Residual labelling items in N-3. |
| R-9 | res | res | res | res | res | **Resolved** | Abstract: "Plans were hash-locked internally; amendment tests followed the first results." |
| R-10 | res | res | res | res | res | **Resolved** | Clause gone from abstract and VII; V-E adds 54%, 38%, 8%, R² 0.47, decision-level 0.06. Method still in S15 (Q6 case 7). |
| R-11 | res | res | res | res | res | **Resolved** | ACKNOWLEDGMENT opens with a verb; recount scope matches IV-E; Fable 5.2 listed as drafting and revising; AI panel sentence kept. S12 disagrees on scope (N-8). |
| R-12 | part | part | part | part | part | **Partly (text is worse in the Acknowledgment half)** | IV-E sentence added: three amendments written and locked 21-22 Nov after an AI panel's report; third's controls asked for by the panel. The Acknowledgment changed "made the scientific decisions" to "made every scientific decision". N-1. |
| R-13 | res | res | res | res | res | **Resolved** | III-A describes the crossing scenario (speed 1 to 3 m/s, drawn side, 390 runs, step 0). The occluder flag is unexplained and unused (O-15). |
| R-14 | res | res | res | res | res | **Resolved** | III-B defines time lost and rest gap. |
| R-15 | res | res | res | res | res | **Resolved** | V-E: start probability 0.10, "masks 16.2% of updates", dropout-estimated class average. |
| R-16 | res | res | res | res | res | **Resolved** | V-E: "25.7% against ... 20.7%"; 89 of 135 cases; 25.24 to 25.84 s. |
| R-17 | res | res | res | res | res | **Resolved** | Table 2 caption: 95% except N's share (99.4%, calibrated) and the IMM's share (99%, nominal). |
| R-18 | res | res | part | res | res | **Resolved (form); reference facts are an author gate** | II adds steady state [26], intermittent observations [27], data association [28], threat assessment [33] to [36]. R2's points (wording of [27], placement) go to N-17 and O-7; the added references' facts cannot be checked offline (N-5). |
| R-19 | part | part | part | part | part | **Partly** | Q7 list: see below. |

**R-1 to R-19 counts, my ruling: resolved 16, partly 3 (R-3, R-12, R-19), not resolved 0.** Seat counts were 16/3/0 (EIC, R2, DA) and 17/2/0 (R1, R3); the difference is R-3 and R-18.

**Q7-1 to Q7-19 (inside R-19), my ruling: resolved 12, partly 3, not resolved 4.**

| Q7 | Ruling | Note |
|---|---|---|
| 1 | Partly | Prefixes fixed except "multi-object" and "mid-rank" (N-20). |
| 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15 | Resolved | Conclusion no longer repeats the abstract; [26], [37], [38], [39], [40] to [44] corrected; conference references are now uniform (city and country absent: Q7-K, advisory); group order fixed; Fig. 4 labels and Fig. 2 axis labels fixed; verb present; "1 s." together; serial comma. |
| 7 | Not resolved | "et al." stays; the author counts authors (advisory). |
| 13 | Partly | SHA-256 and CARLA expanded; the same kind of miss now at NIS in Table 1 (N-19). CANMOT is a name. |
| 16 | Not resolved | ZIP: form only; advisory. |
| 17 | Not resolved | Bold run-in heads: advisory. |
| 18 | Not resolved | Supplement heading case: not applicable. |
| 19 | Partly | Drop cap present; no biography (advisory at submission). |

Earlier items I judge wrong or unnecessary: Q7-16, Q7-17, Q7-18; Q7-7 as a miss (it is an author check); R-3's request for "as point values" in VII (VII makes no margin claim; the request belongs in the abstract only).

## 10. Q8, AI disclosure: ruling

### The ACKNOWLEDGMENT ruling (made whether or not a seat raised it)

The paragraph is the author's, line 273 of `MANUSCRIPT_v13.md`. Sentence 1: "The author conceived the study, set its questions and plans, made every scientific decision, and reviewed and approved all content, and takes full responsibility for the work." A later sentence: "where the amendment files record a design choice as an AI session's, it was made within the author's approval."

**Question 1: is the paragraph, read as a whole, accurate and enough under IEEE's AI-disclosure rule (system, sections, level of use)?**
- **Enough, in substance: yes.** It names the systems and models (Claude: Opus 5.5, Fable 5.2, Sonnet 5.5; Codex: GPT-6.1 Sol, GPT-6 Astra, GPT-6.2 Astra); the parts (analysis, simulation-control and figure code; the literature searches; "the text of all sections and of the supplementary material"; simulation, recording and planner software; the amendment plans); and the level (wrote, drafted and revised; the author chose, rejected or changed options, corrected errors, directed experiments). No AI system is named as an author. It is unusually full.
- **Accurate as a whole: mostly, not entirely.** Four statements need attention.
  1. "made every scientific decision" is larger than the records. The amendment files record several design decisions as the coordinating AI session's: AMENDMENT_11 line 182 ("Coordinator's decisions binding on DR and E4", including the output-rule change under dropouts, line 183); AMENDMENT_12 line 406 ("Coordinator's decision on the design split", the nuScenes primary population, which the author then accepted: "Yes, keep it", line 427); AMENDMENT_13 line 197 ("Whose decision: the coordinator's") and line 41 ("Dropped by decision (coordinator, 06:52)"). The author's own recorded decisions are real but narrower: the pedestrian test despite the no-go (A11 line 43), the title option, the money and time approvals, a blanket instruction (A11 line 19; A12 line 10: "Download whatever you want and run whatever the experiment you want").
  2. The presubmission AI panel is not named, though it caused the three amendments (IV-E says the third's two controls "were asked for by that panel"). IEEE asks for the system used.
  3. "Claude Fable 5.2 and then Claude Sonnet 5.5 audited the claims (Supplement S12)": S12 (line 695) says "an agent on a model other than the writer's" and names no model or order; Fable 5.2 is also named as a text writer. The pointer does not support the sentence.
  4. Nothing says who checked that the references exist and say what the paper says about them, although Claude "ran the literature searches" and S13 says no full text was opened (N-5).
- Also: "directed further experiments after the systems had judged the manuscript ready" is supported by AMENDMENT_11 and AMENDMENT_12 section 0 (the author asked what it would take to reach a higher score); R2 suggests "after drafts were complete" as a safer phrase; I leave that to the author.

**Question 2: would an editor or a later reader of the deposited records see a contradiction?**
- **An editor who reads only the paper:** a mild tension. The paragraph's first sentence says the author "made every" decision; a later sentence in the same paragraph says some choices were an AI session's, "made within the author's approval". The two can be reconciled (approval is a form of decision), but an attentive reader will ask which is meant.
- **A reader of the deposited records** (the paragraph itself says the plans and requests are deposited): **yes, a plain contradiction at the first sentence.** "Whose decision: the coordinator's" sits against "made every scientific decision". The later clause is the true size of the claim. The mismatch is in a responsibility declaration, which is where it costs most; it is also the only earlier item on which the 18:30 text is worse than the 12:01 text (R-12).
- **Severity:** REQUIRED-major, because the fix is cheap and the risk is to the author's credibility, not to the science. It is not CRITICAL.

**Smallest change that keeps the author's own sentences.** Change two words:
- "made every scientific decision" becomes "**made or approved** every scientific decision".
- Keep the later sentence ("where the amendment files record a design choice as an AI session's, it was made within the author's approval") unchanged; with "or approved" it no longer contradicts the first.

**What the author must confirm** before using it (these are facts only the author knows; I did not decide them):
1. That every design choice the amendment files attribute to the coordinating AI session was, at least in scope, approved by the author before the data it affects were scored. The files support this for the second amendment (the nuScenes primary: "Yes, keep it") and for the first (A11 section 6c: "approved in scope by the author"). For the third amendment, which has no approval record of its own (it runs under the second round's standing approval), the claim holds only as a blanket approval. If the author means only that, the accurate fallback wording is "made or approved every scientific decision, or delegated it within an approved scope", which would still need no change to the later sentence.
2. Whether the author wants to add, as IV-E already hints, that the amendments were aimed at the AI panel's objections (DA's wording).

**Other wording that lowers risk without understating use** (author's choice; N-7, N-20): name the panel's system and models; give per pass who wrote and who audited; put the disclosure third in the ACKNOWLEDGMENT with a short plain opening ("Generative AI was used as follows, in line with IEEE policy; no AI system is an author"); consider shortening the paragraph by about a third (it is about 250 words; DA and EIC both note it reads as a defence) and moving the recount description to IV-E, where it already is.

### Other Q8 points

- **Desk rejection on the paragraph alone:** unlikely; I put it at about 10%. The rule asks for disclosure and this is disclosure. The risk is cumulative (AI-written text, AI-run search, AI review panel, local hash locks, amendments after results, a single AI-supported author) and rises if a reader finds the sentence contradicted by the deposit.
- **Codex statement** and the exact model names cannot be checked in the paper or by any seat; nothing in the paper contradicts them. The author confirms them.
- **"The requests and responses of the presubmission reviews are deposited"** is a promise about the deposit (the repository gate); it must be true at submission, and the deposit paragraph's list does not mention it.
- **Recount claim:** matches IV-E, not S12's first sentence (N-8).

## 11. Likely editorial outcome

**Major revision, sent to reviewers.** Reasons: the topic fits OJ-ITS (perception-to-planning safety evaluation); the statistical care, the labelling of what was confirmed and what was added later, and the failed controls reported in the abstract are unusual and will be liked; the checked numbers are sound (R1: 404 of 404). Reviewers will weigh against it: simulation only on one straight road at 5 to 15 m/s with one in-house planner; a confirmed headline result that the paper itself says was expected from near-constancy; small effects (2% to 5%) against each tracker's own class average, with both controls that would have given them meaning failed; no decision-level real-log evidence; the density of V-E; 13 pages; and an AI-written, AI-reviewed, internally locked process by a single author.

My rough judgement, not a model output: desk rejection about 10%; major revision about 55%; reject after review about 30%; minor revision about 5%. The desk-reject risk comes from the Acknowledgment plus length, and N-1 reduces it. Of the seats, EIC (about one in three chance of reject-and-resubmit) and DA (about one in three desk) are more pessimistic; R1 and R3 are more optimistic.

## 12. Distance to 7 and to 8

**What stands between this text and 7.** Everything listed is wording, a value moved in, or text from existing records; none needs new analysis.
1. The Acknowledgment sentence (N-1) and the AI-disclosure gaps (N-7), because a declaration contradicted by the deposit is the single item most likely to lower a reviewer's trust.
2. The tracker's permuted twin defined (N-2).
3. An abstract and summary sentences that carry the body's size and status labels (N-3), including the 4.6% and the coast-count wording.
4. A main text that is self-contained, or an honest sentence about what is not (N-4); the author's earlier paper was rejected on this ground.
5. The author's reading of the closest references and a statement of what was read in full (N-5).
6. The minor items N-6 to N-20.

Even after all of these, density (V-E at about 1,200 words, 13 pages) will still cost points with some referees, and adding the N-4 facts adds length; budget by cutting elsewhere (O-6). Wording cannot remove the structural limits, which cap a text-only revision at about 7.

**What stands between this text and 8.** New evidence, not wording:
- a decision-level test on real logs where there is room (type A, O-3); the real-log tests found no room twice;
- a covariance tested on top of the braking prediction's path (type A, O-1), since the room is mostly prediction error;
- a rerun of the two-noise IMM and the adaptive filter through a predicted covariance that includes process noise over the look-ahead (type A, O-2), since the current interface cannot test what those trackers vary;
- a closed-loop comparison at equal cost that does not fail (the current one failed);
- ideally a public registration of the plan for any further test.
I do not know whether any of these would change the result; the paper's honesty makes a null at that stage as informative as a gain. Without at least two of these I would not expect a panel of this family to go above about 7.

**Forecast.** After one fix round on the 20 REQUIRED items and no new analysis: **6.6 on this scale, plausible range 6.2 to 7.0.** Probability of reaching 7.0 or more at the next panel: about one in four. The earlier panel forecast 6.7 after its fix round; this panel, on the text that came out of that round, gave 6.04 by mean. I therefore take my forecast down from the naive sum of the items and note that forecasts of this kind have been about 0.5 too high. A text with the REQUIRED items done and one of the type-A items in hand would forecast about 7.2 to 7.5.

## 13. OPTIONAL items

| ID | Finding | Seats | Type |
|---|---|---|---|
| O-1 | Test the covariance on top of the braking prediction's path on the existing fresh and new lead-braking arrays (one more amendment test, labelled as such). Downgraded from REQUIRED-major (D2). | DA R-M5 | A |
| O-2 | Rerun the two-noise IMM and the adaptive filter with a predicted covariance that includes their (mode-weighted) process noise over the look-ahead. | R2 M2 (stronger option) | A |
| O-3 | A decision-level real-log test with room. The single change that would raise the score most (EIC, R1, DA). Outside this revision. | EIC, R1, DA | A |
| O-4 | Distance of the two-noise IMM's and the adaptive filter's frontier to the online tracker's class-average frontier (existing arrays), or say it was not computed. | DA R-m5 | A or W |
| O-5 | Equal-time-lost comparison: a four-point figure (R1 O-1); name the 89-case population as a limit and add a common-population sensitivity (R1 O-2); the rest-gap version of the frontier (R2 o7). | R1, R2 | T or A |
| O-6 | Density: split V-E (about 1,220 words, six paragraphs) with title-case sub-subsection headings (for example pedestrians, dropouts, other trackers, closed loop, mechanism check); compress IV-E and V-E; Table 6's frontier row into columns. 13 pages against a recommended ten. | EIC o1, R1 O-10, R3-13, DA O-2, O-10 | W |
| O-7 | Positioning: reconcile [19]'s "over 66%" with the roughly 3% here (R2 m6); existence-probability tracking and the threat-assessment, IMM-for-ACC and AEB works found in the paper's own Table S30 search (R2 m7, o10). All suggested references are unverified; the author reads them first. | R2 | W |
| O-8 | Closed-loop time-gap result into the abstract: at the lower level TG gives 0% contacts and less time lost than F0 (Table 4). | R3-1b | W |
| O-9 | Table 5: like-for-like latency (227.1 to 77.8 m); cells "costs progress (5.3, 0.0)" split into columns. | R1 O-4, EIC o9 | M or W |
| O-10 | "2% to 5%" is a range of point estimates; intervals run from 0.6% to 7.5%. | R1 O-5 | W |
| O-11 | Title "Preregistered": IV-E defines it as internal locks. The title is the author's choice and no sentence contradicts it; I record this only so the author weighs it (an alternative that DA suggested is "with Internally Locked Plans"). | DA O-1, R1 O-6 | none |
| O-12 | Decision counts in Table 6 rows (R1 O-7); a clause on the post hoc Bonferroni check for the first amendment (R1 O-8); the no-count two-population variant (in Q6 case 4). | R1 | M |
| O-13 | Run-set names: "older fresh" and "fresh" are the same set; name the six sets once in III-A. Table 2 row "Classification": say it is the IMM's, registered. | DA O-3, O-4 | W |
| O-14 | Figures: Fig. 2 F0 lies under N and the right panel is empty; Fig. 4(a) legend is small and the caption does not name the three latencies; Fig. 3's y-axis label reads "against F0" for a difference; Fig. 1 text size. | DA O-5, O-6; R1; EIC o4 | W |
| O-15 | Pedestrian: the occluder flag is described and never used or explained; say "open loop, room 0.16 points" in the abstract. | R2 (Phase 2), R3-14 | W |
| O-16 | Deposit and cover-letter items: regenerate RECOUNT_COVERAGE with the paper's labels (R1 O-9); one sentence in the cover letter about the companion paper under review (EIC o11); check Table S43's mean beside medians (DA O-8). | R1, EIC, DA | T |
| O-17 | Shorten the ACKNOWLEDGMENT by about a third (the recount detail is in IV-E). | DA O-9, EIC | W |
| O-18 | Domain asides: the two-noise IMM's mode probability is higher after the stop (0.71) than during braking (0.39) (R2 o1, Table S42); its lag 0.40 m against 1.42 m supports VI's message (R2 o2); the adaptive filter's twin shows timing, not ranking (R2 o3); the process noise scaled by dt/0.5 at 5 and 10 Hz (R2 o8); "oracle is a reference, not a bound" (R2 o9). | R2 | W or M |
| O-19 | Author biography at acceptance. | EIC o13, DA O-12 | T |

Dropped on my check: EIC m7 (D7); R3's request to restore "as point values" in VII (the clause belongs in the abstract, under N-3).

## 14. Correlated-error caveat

All five seats and I are Claude models of one family (Sonnet 5.5, Fable 5.2, Opus 5.5). Two seats (R1 and DA) run on Fable 5.2, the model that wrote the later text (round 2, the submission pass, the fix round, the format pass); one (R2) runs on Opus 5.5, which wrote the earlier text; EIC, R3 and I run on Sonnet 5.5, which did not write the text. The same family ran the earlier panels whose required items the text was revised against. A same-family panel can share blind spots: it may under-weight a limit that an outside referee would find obvious (for example that the paper is a single-author, single-simulator study that an AI panel helped shape), and it may over-trust the paper's own labels. Two things lessen the risk here: the seats disagreed in substance (D2 to D5) and R1 checked printed values against exports rather than against the text. They do not remove it. The scores and the 6.6 forecast carry that uncertainty; none of this is a substitute for a human editor's or an outside referee's read. The repository-and-DOI placeholder and the title are the author's and are not findings.

## 15. Hashes

Check at start (all five package files and the ten seat files match the values in my instructions) and at end (re-computed at 22 Nov 2026 19:01:57 and again after writing both files; all unchanged).

| File | SHA-256 |
|---|---|
| phase1\01_eic_journal_fit.md | cc695cdf347f6e94a05aa5185208b2aed8527e3cfcf2f888c3c759c13a2f6eb6 |
| phase1\02_r1_methodology.md | 47f9bbce10c4e6598bccea8e5e74121e149d7b35ed30fa8227741eaae534d0c6 |
| phase1\03_r2_domain.md | ced74a7527c207c8a41e2f702dd3990076cbb59a76b5952b3d9837318f8d9976 |
| phase1\04_r3_practical.md | 8795bc733e80492af661f558809904fb8c35686241878a6ae534143d0e4b226b |
| phase1\05_devils_advocate.md | f015fa6a4dabb10e31f1e5986367baef0703ca23afb53b532ba0836bc715ec8a |
| phase2_r_check\01_eic_journal_fit_r_check.md | 2761503f0b1b843b0a15e356fc53ff5138c61c9bcf855e99834d03e4b0a88fc0 |
| phase2_r_check\02_r1_methodology_r_check.md | b17e48ea04f9fdf5d5e76f7c6c1903beb214f5713ddeb3462bbaaafc8cec1c15 |
| phase2_r_check\03_r2_domain_r_check.md | 77a5e53f0bcbde25a068db5c3e787b99ca7a1041a3f0b3944e7c4fe71de088b9 |
| phase2_r_check\04_r3_practical_r_check.md | 0e1ca9c6f1bdf3ad7da93e4b115448eac5780d4f2255106aef5d664172680ac5 |
| phase2_r_check\05_devils_advocate_r_check.md | 2122ec09c82b995226f341fa48ca1146b6f3e11c0320b92633b68b915f9725f8 |
| work\panel_provenance_author_round.json | 154239756d07ff73f6491ba8e4b186be69d96e4092da6c547573f721660b2a8e |
| work\panel_brief_author_round_v01.md | 47198b07517f3ac881f51c2768e0e71162814536952eef5033b647528d80feab |
| work\earlier_required_R1_R19_and_Q7.md | 13f24cd5ee3dae2eeddda3472e0bda371d0e3ed565185f71534a2f5e6fa211ce |
| work\synthesis_prompt_author_round_v01.md | 45d45ad63f07814894af22219b40eb849e6c8f45d7150582b6a132ae8230f9e6 |
| pages\page07.png | cd0a226a82a19539256a2892ba56264340061ca2c02c632d3442c8dcef219404 |
| MANUSCRIPT_v13.md | 29125167b108bc27833c16e3b639cbb07af5f4c105c49d375deff3d5b4a951d0 |
| MANUSCRIPT_v13.tex | bd4d08d954d3595de2b5ac2653c18476c7bb3281e1c264604f995f018da01345 |
| SUPPLEMENT_v13.md | fab98c1fe24c8c5b95f86da8b1e664662401055232409a236d963938f5b99a09 |
| MANUSCRIPT_v13.pdf (not opened; page images used) | 4fabfd9f611013fd4e7f60b8a59fcdcc2d782dbd3192a77c2efe54e77beb8299 |
| AMENDMENT_11_v13.md (lines 19, 43, 180-183 read) | b33d8281848c9bf1fbe47a706adbba8e0e063dc4d7480f3fe6fd95e8bb677cf3 |
| AMENDMENT_12_v13.md (lines 10, 400-427 read) | a9911f1222b5fa386c28d39b2f3816cb3e0ec00d0eb4c4d082a58dc8d4ac0e42 |
| AMENDMENT_13_v13.md (lines 1-44, 197 read) | bc7c2bf47c9a29810aa84c5dd4827a0f2d9404f9b684a94d0a918967180498bf |
| ojits-template.tex (lines 180, 195-197, 463-467, 518-519 read) | 770ddac436bfa2609e8f436c66c70ccf0b88d478e72b2493bced8dc4b188ced2 |

Not opened by me: the response letter, session notes, earlier review reports beyond the R-1 to R-19 file, anything named <excluded folder 1> or <excluded folder 2>, the author's local secrets folder. Page images other than page 7 and tpl pages were not opened by me; layout findings other than Fig. 2 rest on the seats' reports, which agree with each other.
