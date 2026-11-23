# Round-1 panel record (ARS_REVIEW_AUTHOR_ROUND_v01.md, sha256 3e5824bf...), sections 5, 7 and 8, copied verbatim by the coordinator. Section numbers and N-/Q7- labels as in the record; locations refer to the 18:30 text.

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

