# Second round, v13 package of 22 Nov 2026 21:15: seat R2, Peer Reviewer 2 (Domain)

## 1. Header

- **Seat:** R2, Peer Reviewer 2 (Domain). One seat only; no other seat, no synthesis, no sub-agents.
- **Model:** Claude Opus 5.5 (`claude-opus-5-5`). Much of the earlier text was written by the same model; I read it with deliberate skepticism, including my own round-1 suggestions (one of which, P-3, I now correct).
- **Card:** "Card 3: Peer Reviewer 2 (Domain)" in `review_v13_output\00_phase0_field_analysis_and_cards.md` (SHA-256 21571d5c…c1ee172): multi-object tracking and Kalman-filter estimation for road vehicles; covariance consistency (NIS/NEES); adaptive and multiple-model filtering; how tracker uncertainty reaches prediction and planning. Only that card and the field analysis were read in that file.
- **Card-confirmation pause not held** (non-interactive run).
- **Criteria binding:** none supplied (`criteria_binding_unavailable`); format judged against the brief's rules and the official template.
- **Brief:** `work\panel_brief_round2_v01.md`, SHA-256 d4d0827044c96076ba2adefb90d9322ae27f96f6076de549f0260e19bf7c27b4 at start (21:25 EST, Get-Date) and at end (21:36 EST).
- **Skill:** `academic-research-skills:academic-paper-reviewer` loaded for its re-review standards only.

| File (`package_v13_2115\`) | SHA-256 at start (21:25:42 EST) | SHA-256 at end (21:36:44 EST) |
|---|---|---|
| MANUSCRIPT_v13.md | c440adca7a70b2b74a373ee3a135d3eeac2c44a35ee6e28cb1c7280893d771b7 | same |
| MANUSCRIPT_v13.tex | 8e9e648ef0290856f5c0dbdb841ebb2ecf0dea57cca6b8e2cc81749e856386ac | same |
| SUPPLEMENT_v13.md | d18eee97e3f02f08159b1aaf81311a2663870818a42268dba706a1ba24d31b2b | same |
| MANUSCRIPT_v13.pdf (not opened) | dc83ce17a652e734399f84005631649fe3801b936a589499a9ed1f0f68a51ccb | same |
| SUPPLEMENT_v13.pdf (not opened) | 084091af1a419f0bff64b643da112a70133ad382d2e51c929fb077ceee8e5692 | same |

All five start hashes equal the brief's, and all five were unchanged at the end, as was the brief's (d4d08270…7c27b4 at 21:36:44 EST).

- **Pages viewed:** `pages\page01.png` to `page14.png` (all 14); their hashes match `work\pages_sha256.txt`. Every layout statement below comes from these images. Supplement and template images were not viewed; I make no layout statement about the supplement, and template rules are cited by line from `ojits-template.tex`.
- **Read, all within "what you may read":** the manuscript Markdown in full; the supplement Markdown for S1 and S2, S4 (Tables S6, S7), S5 (Tables S8 to S13), S6.2 (Tables S16, S17), S10, S11, S12, S13 (Table S30), S14 (Tables S31 to S36), S15 (Tables S37 to S46), and the Table S5 "slips" row; `MANUSCRIPT_v13.tex` for heading commands; `out\freeze_v13_2115\BUILD_REPORT_v13.md` (word counts; SHA-256 919a5a78…b16a7); the template's lines 180, 193 to 198, 211, 393 to 397, 470 to 479 and 516 to 520; my own round-1 report (`03_r2_domain.md`, SHA-256 ced74a75…8d9976); `work\round1_record_sections_5_7_8.md` (3f3d53c0…ee1d18); `work\letter_section_author_round.md` (77b2e165…7127ab1); the round-1 brief (47198b07…d80feab).
- **Not read:** other seats' reports of either round, the full response letter, the manifest, the notes folder, the amendment draft, and the freeze, coverage, derived and outcome files.
- **Limits:** read only; no web; one light `python -I` call (abstract word count: 237 by whitespace, as the build report says). I did not open any cited work. Every statement about a reference's content is from memory and marked so; every suggested reference is "unverified". Statistics are outside my card.

## 2. Judgements

| | Recommendation | Score | Stars |
|---|---|---|---|
| **(a) The text as it stands** | Major revision | **6.5 / 10** | ★★★☆☆ (3 of 5; 3.25 rounded) |
| **(b) CONDITIONAL** (N-1 reads "made or approved every scientific decision"; the paper reports the author's full reading of the closest references, with counts and the publisher/Crossref check; [10] carries the byline's surname) | Minor revision | **7.0 / 10** | ★★★½☆ (3.5 of 5) |

**What separates them.** The science is the same in both. In my domain the round-1 problems that mattered are fixed: the margin interface is now stated where it binds (III-E, V-E, VI, VII), NA, AM and TG are reported with intervals, the dropout and closed-loop results are stated as what they are, and the 10 Hz and nuScenes facts are in the main text. What I still ask for is six text items (P-1 to P-6), none needing new analysis. Under (a), two author-only items stay open. The authorship sentence contradicts the paragraph after it (N-1), and Section II characterizes its "closest methodological relative" [13] and the closest ITS result [19] from abstracts (N-5). An editor cannot accept with either open, and the reading behind N-5 may change Section II, which would need a domain re-read. That is why (a) is major. Under (b) those are settled, and what remains is a short list of wording that an editor can check: minor revision. The half point between the scores is the declarations, not the science.

## 3. N-1 to N-20

| ID | Verdict | Evidence from the 21:15 text (location) | What remains |
|---|---|---|---|
| N-1 | **Not resolved** (author gate) | "The author conceived the study, set its questions and plans, made every scientific decision, and reviewed and approved all content" (ACKNOWLEDGMENT ¶1, p. 12); ¶3 still says "Where the amendment files record a design choice as an AI session's, it was made within the author's approval" (p. 13) | The author confirms, then writes "made or approved". |
| N-2 | Resolved | "A tracker's *permuted twin* asks whether the order of its margins matters beyond their amplitudes: each decision's factor (…) is permuted among the decisions of its run and applied to the class average, and the twin's share is the mean over 20 such permutations. The covariance's share minus its twin's tests whether that order carries information." (IV-C, p. 5) | None. |
| N-3 | Resolved (parts a to h) | (a) "a noise-adaptive filter beats its permuted twin by 0.05"; (b) "against each tracker's own class average … both inside a ±5% margin as point values"; (c) "At 2 Hz a missed-update count, with factors from the covariance margin's median ratios, recovers slightly more (descriptive)"; (d) "78% of the room (38% to 84% across run sets) but costs progress behind nonbraking leads"; (e) "for one longitudinal speed planner predicting at constant velocity", "(position–velocity only)"; (f) "on a straight simulated road (5 to 15 m/s)"; (g) "(60 cases, contact rates far above any deployable level) it is equivalent within ±0.10"; (h) "This does not justify replacing per-track covariances by class averages." (abstract, p. 1); "showed no recovery of a small room" (VII, p. 12). Abstract leads with the answer; 237 words. | New wording problems in the abstract's lead sentence and fourth sentence: P-1 (regression), P-2. |
| N-4 | Resolved | All 21 listed facts found, for example "clip($m$, 0.25, 10)" (III-D, p. 4); "on 58,970 decisions of 366 runs … Shapley shares" (V-E 1, p. 9); "its class average is the 2 Hz one under the 2 Hz masks" (V-E 2, p. 11); "equally spaced from F0's zero-margin caution to the smaller of F0's and E's largest caution" (IV-B, p. 5); the first amendment's closed-loop row (Table 6, p. 10). The two one-program values are described in words and cited (III-D; V-E 3). | One new case, P-6 (old-evaluation values behind the cross-set order). |
| N-5 | **Not resolved** (author gate) | "publisher full texts were not searched, and the works found were read at abstract level" (II, Novelty, p. 3); S13: "what the paper says about them stays within those abstracts" | Author reads the closest works in full and writes the counts sentence. P-5 and P-14 depend on that reading. |
| N-6 | Resolved | "$P$ is the covariance the tracker reports, and no process noise is added over the look-ahead" (III-E, p. 5); "only the position–velocity block of its combined covariance reaches the margin: neither the maneuver mode's acceleration nor a prediction conditioned on the mode does" and "a CA filter (its maneuver mode) whose acceleration variance was tuned by the NIS rule on the tuning runs' frames from braking onset to the stop" (V-E 3, p. 11); "a wider one, with the mode-weighted process noise in the predicted covariance, was not tested" (VI, p. 12); "a predicted covariance that includes process noise over the look-ahead" (VII, p. 12) | Optional only: P-8, P-10. |
| N-7 | Resolved | "presubmission reviews by panels of five Claude agents (the same three models; reviewer workflow of the Academic Research Skills plug-in) … Supplement S12 names the model of each pass" (ACKNOWLEDGMENT ¶3, p. 13); S12 "Claim audit" and "Presubmission reviews" name writer and auditor per pass | "Reviews and responses are deposited" waits for the deposit (gate). Optional P-20. |
| N-8 | Resolved | "recount every result value printed in the main text and all but the marked (‡) values of the supplement; … the library's true clearance was recomputed without it on 20 decisions (Supplement S12)" (IV-E, p. 6); S12 first sentence uses the same scope | None. |
| N-9 | Resolved | "fresh runs … in three scenario families (lead braking, cut-in, and leads that do not brake hard), recorded and scored once under a plan fixed in advance; … Later amendments, written after those results, added pedestrian crossing" (I, pp. 1–2) | None. |
| N-10 | Resolved | "under rules fixed before any new run was extracted or scored (their capture had begun)" (V-E 2, p. 10) | None. |
| N-11 | Resolved | "the dropout gain is a *level effect* (more margin for an identifiable group of decisions, with no ranking shown inside the group) that a count of missed updates reproduces at 2 Hz" (I, p. 2); "the wider spread around real misses on the nuScenes logs is partly one" (VI, p. 12) | None. |
| N-12 | Resolved | Table 6 (p. 10): "Closed loop, dropouts, first amendment, matched in design caution only (60 cases)"; "least-squares slope of that share on the start probability (four values)"; "second amendment, matched in open-loop caution only (135 cases)" | Optional P-19 (status of the first-amendment row). |
| N-13 | Resolved | Table 4 (p. 9) has peak deceleration, rest gap and full braking for every arm at both levels; V-C (p. 8): "Table 4 shows where unscored cost to following traffic and occupants would fall … Against a mean time lost of about 24.5 s per run for every arm, the lower-level differences are below 1%" | None. |
| N-14 | Resolved | Table 2 rows "NA, NIS inflation 0.024 [0.015, 0.034]", "TG, time gap 0.287 [0.231, 0.332]", "AM, acceleration margin 0.369 [0.331, 0.404]" (p. 7); "the shares rise in the order N, NA, TG, AM, CK3" (V-A, p. 6) | P-6: the "every run set" order rests partly on values printed nowhere. |
| N-15 | Resolved | "The retuning holds before braking only: on the old evaluation runs the retuned filters' NIS during braking is several times its expected value (exploratory; computed by one program; Supplement S4)"; "A two-noise IMM, whose maneuver mode was tuned on braking frames" (III-D, pp. 4–5) | Optional P-9 (Table 3 row label), P-13. |
| N-16 | Resolved | "among tracks of four-wheel vehicles (cars, trucks, buses, and trailers) at the same scene and keyframe; pairs are not stratified by class or motion"; "The primary population was chosen on the training split, after the all-pairs statistic had come out negative there … it is the one Holm entry whose population was chosen again" (V-E 5, p. 11) | None. |
| N-17 | Resolved (the direction) | "there is a critical arrival rate below which the expected covariance of an unstable system is unbounded [27]; with fixed noise the covariance is then a function of the arrival sequence alone, so a margin that counts missed updates should match it" (II, p. 3) | The direction is right. The clause and "alone" have new domain problems (P-3). |
| N-18 | Resolved | Table S5, slips row: "in the third amendment, the list of dropped arms carries the time "06:52" although its text and its two locks have earlier file times" | None. |
| N-19 | Resolved | Table 1 (p. 2): "NA, output-scalar inflation by the normalized innovation squared (NIS)" | None. |
| N-20 | **Partly resolved** (5 of 6) | (1) ACKNOWLEDGMENT in four paragraphs, in the order responsibility, data and code, AI disclosure, declarations (pp. 12–13); (2) Fig. 2 panels labeled "(a)" and "(b)" (p. 7; template 393–396); (3) "multiobject" (abstract), "midrank" (IV-C); hyphenated forms only in reference titles (template 195–197); (4) letters in note rows under Table 2 ("^a^Contacts from behind…"), Table 4 ("^a^Not caution-matched…") and Table 6 ("^a^Nominal 99% interval.") (pp. 7, 9, 10; template 518–519); (5) [21] "…autonomous driving?" in" with no comma; **(6) not resolved:** [10] "A. S. K. Kopalli" against the byline "ANANDA SIVA KUMAR KOPALLI NAGA VENKATA" and the running head "Kopalli Naga Venkata" (pp. 1, 2, 13) | Part 6: the author's choice of surname form. |

**Counts:** resolved 17 (N-2 to N-4, N-6 to N-19); partly 1 (N-20); not resolved 2 (N-1, N-5).

## 4. Findings

No finding is CRITICAL. Types: W wording; M value moved in from the supplement; T text from existing records; A new analysis.

### REQUIRED-major

| ID | Location | Finding | Evidence quoted | Fix (fewest words) | Type |
|---|---|---|---|---|---|
| N-1 | ACKNOWLEDGMENT ¶1 and ¶3 (pp. 12–13) | Unresolved author gate. The first sentence contradicts the third paragraph's account of design choices that the amendment files record as an AI session's. | "made every scientific decision"; "Where the amendment files record a design choice as an AI session's, it was made within the author's approval" | "made or approved every scientific decision", after the author confirms. | W (author) |
| N-5 | II, all four themed paragraphs and Novelty (p. 3); S13 | Unresolved author gate. In my domain this is concrete. The paper's closest methodological relative [13], the closest ITS result [19] (">66%"), and the direction of [15] ("upstream") are all characterized from abstracts. | "the works found were read at abstract level" | The author reads them in full, corrects II if needed, and adds the counts sentence. | T (author) |

### REQUIRED-minor

| ID | Location | Finding | Evidence quoted | Fix (fewest words) | Type |
|---|---|---|---|---|---|
| P-1 (regression) | Abstract, first sentence (p. 1) | The new lead sentence, written to lead with the answer, states the result as a property of trackers "in autonomous driving". The planner, prediction and test bed are named only in the next sentence. This is the sentence that gets quoted, and it reads as a field-wide null, which is the reading my card warns against. | "In autonomous driving, a multiobject tracker's covariance, used as a planner's safety margin, improved decisions barely or not at all over one class-average margin." | Begin "In our simulated tests of one speed planner, …", or move "for one longitudinal speed planner predicting at constant velocity" into this sentence. | W |
| P-2 | Abstract, fourth sentence (p. 1); I, designer paragraph (p. 2); VI, "What a varying covariance needs" (p. 12) | "With fixed noise it is nearly constant" is false as written. The dropout covariance is the same fixed-noise tracker under masks, and it varies and recovers 2.8%. In pedestrian crossing the fixed-noise covariance also varies (11.3% of rows within 5%). Near-constancy needs regular updates (and, as V-E 1 shows, a fixed heading). II and VII already carry this qualifier, so the abstract now contradicts itself two sentences later. | "With fixed noise it is nearly constant and adds nothing" (abstract); "in lead braking with fixed noise the covariance acts as a constant" (I); "in lead braking that makes it a constant" (VI); compare "In lead braking with fixed noise and regular updates" (VII) and "With fixed noise and under regular updates" (II) | Add "and regular updates" in all three places. | W |
| P-3 | II, "Adaptive covariances in tracking" (p. 3) | Two domain inaccuracies remain in the [27] sentence now that the direction is right. (i) The critical-rate result concerns systems with unstable modes. A constant-velocity model has all eigenvalues on the unit circle, and its covariance grows polynomially over a gap. From memory (confidence 3; the author checks [27]), the expected covariance therefore stays bounded for any positive arrival rate. Here tracks coast for at most three updates anyway. The clause invites a mechanism that plays no part in this paper. (ii) "A function of the arrival sequence alone" contradicts the paper's own VI and S11: CANMOT's noise is fixed in the object frame and rotated with heading, so the covariance also follows geometry (38% of the explained variance in pedestrian crossing). "Alone" holds only on a straight road with constant heading. I proposed the "function of the arrival sequence" wording in round 1 (R2-m1), so this corrects my own suggestion. | "a critical arrival rate below which the expected covariance of an unstable system is unbounded [27]; with fixed noise the covariance is then a function of the arrival sequence alone" (II); "With fixed noise the covariance follows the update schedule and the geometry" (VI); S11: "rotates it with the track's heading … so the ratio can vary with a crossing actor's heading alone" | Replace "alone" with "and, for noise fixed in the object frame, of the heading (on a straight road, of the arrival sequence alone)". Drop the critical-rate clause, or add "(a constant-velocity model, coasted at most three updates here, is not in that regime)". | W |
| P-4 | II (p. 3); V-E 2 (pp. 10–11); VI (p. 12) | Intermittent-observation filtering is placed only against the control result [27]. In target tracking, missed detections are standard through the detection probability of probabilistic data association ([26], [28], both cited) and through track-existence or track-status measures (IPDA; unverified). The paper's dropout conclusion, that a count of missed updates reproduces the gain, reads naturally as "the track's status already carries it". A tracking referee will expect that link, and it strengthens the designer message. Raised as R2-m7(a) in round 1; it was not carried into the panel's N list. | "Filters that account for data-association uncertainty [28] have a covariance that depends on the data" (II); "Every arm keeps an unmatched track for up to three updates" (V-E 2); "a level effect that needs no per-decision covariance" (V-E 2) | One sentence in II or VI: "In target tracking, missed detections enter through the detection probability [26], [28] and a track's existence or status; the coast-count margin of Section V-E is the simplest such measure." | W |
| P-5 | II, "Uncertainty in prediction and planning"; VI, "What a varying covariance needs" (pp. 3, 12) | The closest work in the target journal reports that a misdetection-aware chance-constrained MPC cut collision risk by more than 66% against a noise-only one. This paper finds about 3% of the room under dropouts, matched by a coast count. [19] is cited twice, but the two results are never reconciled, and an OJ-ITS reader will ask first. Likely reasons, in the paper's own terms: here the noise-only baseline's covariance already grows while coasting; the comparison is at equal caution, not at one controller; masks are one to three updates at 2 Hz; the detection-rate regime differs. Raised as R2-m6 in round 1; it was not carried into the N list. Depends on reading [19] in full (N-5). | "cut collision risk by over 66% against a noise-only controller [19]" (II); "chance constraints can also account for misdetections explicitly [19]" (VI) | Two sentences in VI on why the results differ. | W |
| P-6 | V-D, "Recording policy" (p. 8); Table 5 (p. 9) | One of the only two statements said to hold "in every run set" is the order of the sources' shares. For the old evaluation runs it rests on values printed nowhere. Table 5 gives only the room, CK3 and N per run set. Table S13 is the earlier analysis's grid frontier and has no TG row. S12 says the order is "in both programs' exports". This contradicts I's "The main text holds every result on which the claims rest". | "the sources' shares keep one order (point values rising: N, NA, TG, AM, CK3; Table 2 and Supplement S12)" (V-D); S12: "the old-run values of Table S13 are the earlier analysis's" | Add NA, TG and AM rows ("tuning / old evaluation / fresh") to Table 5's recording-policy block, from the existing two-program exports. | T |
| N-20 (6) | [10] (p. 13), byline, running head | Unresolved author gate. | "A. S. K. Kopalli" | One surname form, the author's choice. | W (author) |

### OPTIONAL

| ID | Location | Finding | Evidence quoted | Fix (fewest words) | Type |
|---|---|---|---|---|---|
| P-7 | V-A (p. 6); VI | NA is the fixed-noise covariance inflated by its own innovations: the simplest innovation-adaptive covariance. On the nominal fresh runs it recovers 0.024 [0.015, 0.034], as much as the amendments' dropout and IMM gains, but it never enters the "where it varies" story. | "NIS inflation recovers 0.024 of the room" (V-A) | One clause in VI next to the adaptive filter (descriptive). | W |
| P-8 | Abstract | "beats its permuted twin by 0.05" has no unit, and the twin is undefined for an abstract reader. "(position–velocity only)" is cryptic. | "a noise-adaptive filter beats its permuted twin by 0.05"; "(position–velocity only)" | "by 0.05 of the room against a copy whose margins are shuffled within runs"; "(through its position–velocity covariance)". | W |
| P-9 | Table 3, row 2 (p. 7) | The row label still reads as a consistent filter, although III-D now says the retuning holds before braking only (S4: no tuning run inside the window). | "CV filter, retuned (median NIS near 2)" | "(median NIS near 2; before braking only)". | W |
| P-10 | Table 3 (p. 7); VI; VII | The two-noise IMM's post-stop lag is 0.40 m against 1.42 m, but its braking-phase room equals the CV filter's (23.51 against 23.62). Its value lies mainly in the mean path, which a constant-velocity prediction from the mixed velocity discards. This supports VI's "path" message. The natural next test is the IMM's own mode-conditioned prediction, mean and covariance together. | Table 3: "0.40", "1.72 / 23.51 / 0.03"; VII next steps list "a covariance added to a braking prediction's path" | One sentence in VI; add "an IMM's mode-conditioned prediction" to VII's next steps. | W |
| P-11 | Table 3, retuned IMM row; V-B | The retuned IMM's maneuver-mode probability is higher after the stop (0.71) than during braking (0.39), so its "would classify as recovers" is not maneuver detection (R2-o1). | Table S42: "0.71 [0.70, 0.71]; 87%" | One clause. | M (Table S42) |
| P-12 | V-E 3 (p. 11) | Both the adaptive filter's tested twin difference and the two-noise IMM's descriptive one (0.0210 [0.0184, 0.0242], S15) say that the timing of the variation matters (it follows the phase), not that decisions are ranked within a phase (R2-o3). | "The adaptive filter's share exceeds its permuted twin's" | One clause for each. | W + M (S15) |
| P-13 | III-D | The tracker of record's own consistency is absent. On the old runs its NIS is about 2 during braking but about 0.5 before and 0.07 after the stop (Table S7, one program). A covariance that is consistent on average during braking still ranks nothing per decision, which is a useful domain point tied to [30]. | Table S7: "0.49‡", "1.87‡", "0.07‡" | One clause, in words (one program). | W |
| P-14 | II (p. 3) | Planning is downstream of perception. Check "upstream" against [15] (R2-o6). | "a pipeline that propagates perceptual uncertainty upstream" | Correct after reading [15]. | W |
| P-15 | II (p. 3) | [24] is an INS/GPS application. Innovation-based adaptive estimation predates it (Mehra; unverified) (R2-o10). | "innovation-based filters reestimate the noise [24]" | Add the original source beside [24]. | W |
| P-16 | S6.2 | Process noise is scaled by dt/0.5 at 5 and 10 Hz. For a white-noise-acceleration model the blocks scale as dt³, dt² and dt, which changes the steady-state shape between rates (R2-o8). | "with its process noise scaled by dt/0.5" | State CANMOT's process-noise form, or call it an approximation. | T |
| P-17 | V-D, "Update rate and latency" (p. 8) | The comparison mixes latencies (2 Hz at 0 s against 10 Hz at 0.1 s). At equal 0.1 s latency the fall is 227.1 to 77.8 (Table S16), which is stronger. | "falls from 173.4 decision-equivalents at 2 Hz to 77.8 at 10 Hz with the plan's 0.1 s latency" | Add "(at 0.1 s latency throughout: 227.1 to 77.8)". | M (Table S16) |
| P-18 | VI, "Which commitment applies" (p. 12) | "The two" has no antecedent in that sentence. | "so the closed loop does not decide between the two" | "between the two open-loop commitments". | W |
| P-19 | Table 6, first-amendment closed-loop row (p. 10) | The label "equivalent" carries neither "(A)" nor "descriptive", so its status in the first amendment's sequence is unclear. | "equivalent" | Add its status. | W |
| P-20 | ACKNOWLEDGMENT ¶3 (p. 13); S12 | "The same three models" is not fully supported: S12 records one panel on "a Claude Sonnet model whose version its record does not name". | "(the same three models; …)" | "(Claude models: Opus 5.5, Fable 5.2, Sonnet 5.5, and one Sonnet panel of unrecorded version)". | W |

**Counts:** REQUIRED-major 2 (N-1, N-5; 0 new); REQUIRED-minor 7 (P-1 to P-6 new, N-20 (6)); OPTIONAL 14 (all new P numbers; six restate my round-1 optional items that remain open). CRITICAL 0. Regression: P-1.

```yaml suggested-references
# All from memory; none checked (no web access). Each must be verified and read before use.
- {authors: "D. Musicki, R. Evans, S. Stankovic", title: "Integrated probabilistic data association", venue: "IEEE Trans. Autom. Control", year: 1994, status: unverified, for: P-4}
- {authors: "R. K. Mehra", title: "On the identification of variances and adaptive Kalman filtering", venue: "IEEE Trans. Autom. Control", year: 1970, status: unverified, for: P-15}
```

## 5. Q1 to Q8, briefly: what changed since my round-1 report

**Q1. Labels and sizes.** Improved. The abstract now uses the adaptive filter's tested twin difference, not its descriptive 4.6%. The coast-count result reads "slightly more (descriptive)", with the interval below zero stated in V-E. Table 6 flags "matched in open-loop caution only" and adds the first amendment's closed loop. Holm stays beside the labels and changes none. "Confirmed" appears only for the original sequence. Left: the first-amendment closed-loop row's status (P-19); the abstract's "0.05" without a unit (P-8).

**Q2. Overreach.**
- The dropout gain's source is now stated correctly everywhere ("matched at 2 Hz by a coasting margin … ranking among dropout decisions is not shown there").
- The 10 Hz caveats (2 Hz class average, 5 to 15 missed updates, no coast-count comparison) are in V-E.
- The closed loop is stated as what it is ("Equivalent here does not mean safe"; "The fewer contacts thus cannot be told from a wider margin").
- The nuScenes check discloses unstratified pairs, the level reading and the re-chosen population. The real-log decision test says "nothing was tested there".
- The two-noise IMM's interface is named in III-E, V-E, VI and VII.
- Scope of the null: the planner and prediction are named in sentence 2 of the abstract, and VII has a full scope sentence.
- New: the abstract's lead sentence is unscoped (P-1, regression). "With fixed noise it is nearly constant" contradicts the dropout result (P-2). II's "arrival sequence alone" contradicts VI (P-3).

**Q3. Earlier limits.**
- (a) Closed loop matched only in open-loop caution: addressed. The equal-time-lost comparison was run, failed, and is stated; one level and interpolation are disclosed.
- (b) Dropout gain as a coasting margin: addressed.
- (c) Abstract and conclusion stronger than the body: largely addressed; P-1 and P-2 remain.
- (d) The two-noise IMM's interface: addressed.
- (e) Holm and recount scope: addressed; IV-E and S12 now match.
- (f) Density: self-containment is achieved, but at a cost. V-E is 1,503 words and the paper grew to 14 pages.
- Structural limits (a confirmed null that was expected, "what the test adds is the bound"; small effects; one simulated configuration at 2 Hz; no decision-level real-log evidence; amendments after results, local locks, AI authorship) are unchanged and disclosed. They are limits of the study, not of the text.

**Q4. Readability.** The abstract now leads with the answer. "Level effect" is defined at first use, and V-E's five subheads make the varying-covariance results findable. The abstract is still jargon-dense for an ITS reader ("share of the room", "permuted twin", "position–velocity only"). "Two-noise IMM" is a misleading name for a tracking reader, who will expect two CV modes with different process noise rather than a CV/CA pair. V-E 3 defines it, but a one-word gloss ("CV and high-noise CA") in Table 1 would help. Every claim's evidence can now be found in the main text, except P-6.

**Q5. Verdict.** (a) Major revision, 6.5 / 10. (b) Conditional: minor revision, 7.0 / 10. Most likely OJ-ITS outcome for the text as it stands: major revision on the declarations, or minor revision if the editor treats N-1 and N-5 as checks. The single change that would raise my score most is the author's full reading of [13], [15], [19], [35] and [36], with Section II corrected and [19] reconciled with this paper's dropout result (N-5, P-5). After that, the abstract's two wording fixes (P-1, P-2).

**Q6. Self-contained main text.** The 21 round-1 cases are all closed. One new case: V-D's cross-set order on the old evaluation runs rests on values in the exports only (P-6). The two one-program tuning values (the maneuver variance 0.917 with its median NIS, and the braking-phase NIS) are described in words and cited. I accept that under the paper's stated rule.

**Q7. OJ-ITS format and declarations.** All round-1 misses are fixed except N-20 (6): ACKNOWLEDGMENT order (template 472–478 for the single section), Fig. 2 (a)/(b) (393–396), prefixes (195–197), table-footnote letters (518–519), NIS defined in Table 1, and the [21] comma. Checked and correct:
- headings in capitals, with subsubsections in title case ("1) Pedestrian Crossing"; template line 211 style);
- "Fig. N" in text and "FIGURE N." in captions; Arabic table numbers;
- funding on the first page; running head;
- five alphabetical index terms; abstract 237 words with no abbreviations;
- tables fit; no contrastive "while" (template 180).

Advisory: visible white space above the level-3 heads on pp. 8 and 11; p. 14 holds only half a column of references; "CANMOT" is never expanded (a name).

**Q8. AI disclosure.** It now sits in its own third paragraph. It names the systems and models, what each did, and the level of use. It names the presubmission panels and points to S12 for each pass's models. That meets IEEE's rule, and a desk rejection on the disclosure itself is unlikely. Left:
- N-1, the "made every scientific decision" sentence, which the same paragraph's "within the author's approval" contradicts;
- "the same three models", which S12 does not fully support (P-20);
- the phrase "after the systems had judged the manuscript ready", which still suggests that the systems judged readiness ("directed further experiments after drafts were complete" says the same without that suggestion; optional).

**Length and density.** At 14 pages (body 8,253 words, tables and captions 2,724, 47 references) the paper is well past the roughly ten pages OJ-ITS papers usually run. It is denser than a reader needs. IV-E and V-E read as an audit record, and V-E alone, at 1,503 words, is longer than most papers' results sections. The extra page bought self-containment, which was the right trade given the author's earlier rejection. The page can be recovered without moving any result to the supplement:
- shorten IV-E's departures accounting to the counts and a pointer to Table S5;
- cut Table 1 rows that repeat IV-A to IV-C;
- fold V-C's nonbraking-lead sentences into Table 5;
- tighten the closed-loop-with-dropouts paragraph, whose numbers are in Table 6.

None of this is a condition for acceptance in my view.
