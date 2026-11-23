# Phase 1, round 2, seat R1 (Peer Reviewer 1, Methodology): v13 package of 22 Nov 2026, 21:15

## 1. Header

- **Seat:** R1, Peer Reviewer 1 (Methodology). **Model:** Claude Fable 5.2 (`claude-fable-5-2`). The later text, including this revision, was written by a session on this same model. I therefore checked values against the exports, the new twin definition against the plan, and the scope sentences against the coverage record, and did not rely on the text's or the letter's own account.
- **Card:** "Card 2: Peer Reviewer 1 (Methodology)" of `review_v13_output\00_phase0_field_analysis_and_cards.md`, identity unchanged. **Card-confirmation pause not held** (non-interactive run). `criteria_binding_unavailable`.
- **Brief:** `work\panel_brief_round2_v01.md`, SHA-256 d4d0827044c96076ba2adefb90d9322ae27f96f6076de549f0260e19bf7c27b4 (matches the launch message).
- **Files reviewed, SHA-256 at start and at end (identical both times, equal to the brief's table):**

| File | SHA-256 (start = end) |
|---|---|
| `MANUSCRIPT_v13.md` | c440adca7a70b2b74a373ee3a135d3eeac2c44a35ee6e28cb1c7280893d771b7 |
| `MANUSCRIPT_v13.tex` | 8e9e648ef0290856f5c0dbdb841ebb2ecf0dea57cca6b8e2cc81749e856386ac |
| `SUPPLEMENT_v13.md` | d18eee97e3f02f08159b1aaf81311a2663870818a42268dba706a1ba24d31b2b |
| `MANUSCRIPT_v13.pdf` (not opened; page images used) | dc83ce17a652e734399f84005631649fe3801b936a589499a9ed1f0f68a51ccb |
| `SUPPLEMENT_v13.pdf` (not opened) | 084091af1a419f0bff64b643da112a70133ad382d2e51c929fb077ceee8e5692 |

- **Read in full:** `MANUSCRIPT_v13.md`. **Read in part:** `SUPPLEMENT_v13.md` (S1.4, S4 prose, S12 in full, Table S5 by search, S14 prose, S15 in full; the rest by outline and search); `MANUSCRIPT_v13.tex` (table notes by search); `BUILD_REPORT_v13.md`.
- **Read under "what you may read":** the round-2 brief; my card and the field analysis; my own round-1 report (`02_r1_methodology.md`); `work\round1_record_sections_5_7_8.md`; `work\letter_section_author_round.md`. The round-1 brief was not reopened (its standards are in my round-1 report).
- **Seat extra reads:** `AMENDMENT_11_v13.md` §6b in full and by search; `AMENDMENT_12_v13.md` by search (§3d, §5 lines 406 to 460) and `AMENDMENT_10_v13.md` by search (line 183); `AMENDMENT_13_v13.md` not reopened (read in full in round 1); `LOCK_A12a.txt` by search (line 64); every `A_EXPORT_*`/`A_RECOUNT_*` pair of record in `B_retrack\out`, `CD_capture\out`, `E_closedloop\out`, `F_nuscenes\out` (19 pairs, compared key by key; `F_dropout\out` holds none), the old-run pair `TESTOLD_A_EXPORT_C`/`TESTOLD_A_RECOUNT_C`, `shared\checks\step0_recount\A_RECOUNT_S0.json`, `A12_HOLM_v01.md`, `A13_HOLM_v01.md`, both recount result files and both recovered programs in `shared\holm_recount\`, and `RECOUNT_COVERAGE_v13.md` of `freeze_v13_2115`.
- **Page images viewed:** manuscript pages 1, 2, 5, 7, 8, 9, 10, 11, 12, 13, 14 (of 14); no supplement or template image this round.
- **Not done:** no web; no text sent anywhere; no sub-agent; no other seat's file opened; nothing changed outside this file. One light `python -I` process at a time (JSON comparisons only; my script is in the session scratchpad).
- Clock (Get-Date): start 21:25, writing 21:35 EST, 22 Nov 2026.

## 2. Judgements

| | Recommendation | Score | Stars |
|---|---|---|---|
| **(a) The text as it stands** | Minor revision | **6.9 / 10** | 3.5 of 5 |
| **(b) CONDITIONAL** (N-1 reads "made or approved every scientific decision"; the author's reading sentence is in the paper; [10] carries the byline's surname; nothing else changed) | Minor revision, at its lower edge (one required wording item left, P-1) | **7.2 / 10** | 3.5 of 5 |

**What separates them.** In (a) one declaration is still contradicted by the plans that the same paragraph deposits (N-1), and Section II now says in the main text that the works it characterizes "were read at abstract level" (N-5): both are statements an editor reads before any result. In (b) both are gone and the only required item left from my seat is a one-clause fix (P-1). Neither judgement reaches "accept as is", and neither can by wording: the confirmatory result was expected, every positive result comes from an amendment written after first results, the positive shares are 2% to 5% of a 5-point room, and there is one in-house planner, one simulator, and no decision-level evidence on real logs. Against round 1 (6.6): the registered twin test is now defined, the summary sentences carry the body's sizes, the first amendment's null closed loop has its row, and the main text is self-contained on every case I raised; the cost is density (14 pages, Section V-E at 1,503 words, Table 4 at ten columns).

## 3. N-1 to N-20

Counts: **resolved 17, partly resolved 1, not resolved 2.**

| ID | Verdict | Evidence (21:15 text) | What remains |
|---|---|---|---|
| N-1 | **Not resolved** (waits for the author) | ACK ¶1: "set its questions and plans, made every scientific decision, and reviewed and approved all content" | The sentence; see (b). |
| N-2 | Resolved | IV-C: "A tracker's *permuted twin* asks whether the order of its margins matters beyond their amplitudes: each decision's factor (the median over its rows of the square root of the class average's critical scale over the covariance margin's) is permuted among the decisions of its run and applied to the class average, and the twin's share is the mean over 20 such permutations. The covariance's share minus its twin's tests whether that order carries information." Checked against AMENDMENT_11 §6b (lines 162 to 165): factor, within-run permutation, K = 20, mean over twins, and the null all agree. | Three details of the plan are left out (permuted "among each run's decisions that have a factor"; drawn once before any value; critical scales divided by the factor squared). Optional, P-3. |
| N-3 | Resolved | Abstract: "for one longitudinal speed planner predicting at constant velocity, on a straight simulated road (5 to 15 m/s)"; "against each tracker's own class average"; "both inside a ±5% margin as point values; a noise-adaptive filter beats its permuted twin by 0.05"; "At 2 Hz a missed-update count, with factors from the covariance margin's median ratios, recovers slightly more (descriptive)"; "78% of the room (38% to 84% across run sets) but costs progress"; "(60 cases, contact rates far above any deployable level)"; last sentence "replacing per-track covariances by class averages". VII: "showed no recovery of a small room". 237 words. All eight parts done. | A pronoun slip the rewrite introduced (P-2, optional). |
| N-4 | Resolved | Present in the main text: III-D "clip($m$, 0.25, 10)"; IV-C the twin; IV-E "a classification step passing unless its class is inconclusive"; V-E "58,970 decisions of 366 runs", "Shapley shares", "0.0347 [0.0109, 0.0581]", "(their capture had begun)", "its class average is the 2 Hz one under the 2 Hz masks", "the transition diagonal is 0.95"; III-B "open-loop caution on the old evaluation runs"; Table 6 first-amendment row. | The maneuver mode's variance and the braking-phase NIS stay in the supplement because one program computed them; the main text says so in words. Acceptable. Decision counts for Table 6 (tier-2, optional) not added (P-8). |
| N-5 | **Not resolved** (waits for the author) | II: "publisher full texts were not searched, and the works found were read at abstract level"; "[35], [36] ... makes no such comparison" | The author's reading and the sentence the record proposes. The limits are now stated, which is honest and makes the gap more visible. |
| N-6 | Resolved | III-E: "$P$ is the covariance the tracker reports, and no process noise is added over the look-ahead"; V-E: "neither the maneuver mode's acceleration nor a prediction conditioned on the mode does"; VI Limits: "a wider one, with the mode-weighted process noise in the predicted covariance, was not tested" | None. |
| N-7 | Resolved | ACK ¶3: "panels of five Claude agents (the same three models; reviewer workflow of the Academic Research Skills plug-in)"; S12 "Claim audit" and "Presubmission reviews" name the model of each pass | "Eight reviews" in S12 will be out of date at submission (P-13, optional). The deposit is a gate. |
| N-8 | Resolved | IV-E: "recount every result value printed in the main text and all but the marked (‡) values of the supplement; they share the scoring library, stored arrays, and resample draws, and the library's true clearance was recomputed without it on 20 decisions (Supplement S12)"; S12 ¶1 uses the same sentence; ACK points to both | None in the paper. The coverage record's labels are stale (P-4, optional). |
| N-9 | Resolved | I: "three scenario families (lead braking, cut-in, and leads that do not brake hard) ... Later amendments, written after those results, added pedestrian crossing" | None. |
| N-10 | Resolved | V-E: "under rules fixed before any new run was extracted or scored (their capture had begun)"; LOCK_A12a line 64 agrees | None. |
| N-11 | Resolved | I: "a *level effect* (more margin for an identifiable group of decisions, with no ranking shown inside the group) that a count of missed updates reproduces at 2 Hz"; VI: "a level effect at 2 Hz; the wider spread around real misses on the nuScenes logs is partly one"; VII: "at 2 Hz the dropout gain is a level effect" | None. |
| N-12 | Resolved | Table 6: "Closed loop, dropouts, first amendment, matched in design caution only (60 cases) ... −0.03 [−0.10, 0.03]; 0.15 [0.08, 0.24] ... equivalent"; "least-squares slope of that share on the start probability (four values)"; "second amendment, matched in open-loop caution only (135 cases)" | None. |
| N-13 | Resolved | Table 4 columns "Peak decel.", "Rest gap", "Full braking" for all twelve rows; V-C: "Table 4 shows where unscored cost to following traffic and occupants would fall" | The new sentence on time lost needs its denominator (P-1, required-minor). |
| N-14 | Resolved | Table 2 rows NA 0.024 [0.015, 0.034], TG 0.287 [0.231, 0.332], AM 0.369 [0.331, 0.404]; V-A: "the shares rise in the order N, NA, TG, AM, CK3"; V-D: "(point values rising: N, NA, TG, AM, CK3; Table 2 and Supplement S12)". I confirmed the order in both programs' exports on the tuning, old evaluation, and fresh runs. | None. |
| N-15 | Resolved (in words) | III-D: "The retuning holds before braking only: on the old evaluation runs the retuned filters' NIS during braking is several times its expected value (exploratory; computed by one program; Supplement S4)"; "A two-noise IMM, whose maneuver mode was tuned on braking frames" | The values stay in Table S7 with ‡, by the paper's own recount rule. Acceptable. |
| N-16 | Resolved | V-E: "among tracks of four-wheel vehicles (cars, trucks, buses, and trailers) at the same scene and keyframe; pairs are not stratified by class or motion"; "The primary population was chosen on the training split, after the all-pairs statistic had come out negative there ... it is the one Holm entry whose population was chosen again after design data had been seen". AMENDMENT_12 lines 406 to 460 agree. | None. |
| N-17 | Resolved (wording) | II: "a critical arrival rate below which the expected covariance of an unstable system is unbounded [27]; with fixed noise the covariance is then a function of the arrival sequence alone, so a margin that counts missed updates should match it" | The letter says the check was against the abstract of [27]; falls under N-5. |
| N-18 | Resolved | Table S5 slips row: "in the third amendment, the list of dropped arms carries the time "06:52" although its text and its two locks have earlier file times" | None. |
| N-19 | Resolved | Table 1, row NA: "output-scalar inflation by the normalized innovation squared (NIS)" | None. |
| N-20 | **Partly resolved** (5 of 6) | (1) ACK order: responsibility, deposit, AI disclosure, declarations (pages 12 and 13): done. (2) Fig. 2 panels "(a)", "(b)" (page 7): done. (3) "multiobject", "midrank"; "multi-object" only in reference titles: done. (4) Lettered notes under Tables 2, 4, 6 (pages 7, 9, 10): done. (5) [21] "driving?" in: done. (6) [10] "A. S. K. Kopalli" against the byline "Kopalli Naga Venkata": **not resolved** (author decides). | Part (6). |

## 4. Findings

Types: **W** wording; **M** a value or fact moved in from the supplement; **T** text the author writes from existing records; **A** new analysis. No finding is CRITICAL. None is type A.

### 4.1 REQUIRED-major (2; none new)

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| N-1 | ACKNOWLEDGMENT ¶1 | Unchanged. The deposited amendment files record design choices as the coordinating AI session's, and the paragraph's own later sentence says so; the first sentence is larger than the record. | "made every scientific decision"; ¶3: "Where the amendment files record a design choice as an AI session's, it was made within the author's approval." | "made or approved every scientific decision", after the author confirms. | W (author) |
| N-5 | Section II, "Novelty, with its limits"; S13 | Unchanged in substance. The main text now states that the works it characterizes were read at abstract level while still asserting what [35], [36] do not do. | "the works found were read at abstract level"; "[35], [36] ... makes no such comparison" | The author reads the closest works in full and adds the record's sentence. | T (author-only) |

### 4.2 REQUIRED-minor (2; one new)

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| N-20 (6) | Reference [10]; byline | One surname form. | [10] "A. S. K. Kopalli"; byline "Ananda Siva Kumar Kopalli Naga Venkata" | Author chooses one form. | W (author) |
| P-1 (new sentence of this revision) | Section V-C | The run length is nowhere in the main text, so "a mean time lost of about 24.5 s per run" cannot be read, and "below 1%" divides by a quantity that is almost all time standing behind a stopped lead, common to every arm. As a relative cost it understates: the avoidable part of time lost is what a margin changes. Table S1 gives 35 s with 30 s assessed for the recordings; the closed-loop run length is not in the passages I read. | "Against a mean time lost of about 24.5 s per run for every arm, the lower-level differences are below 1%." | State the run length and that nearly all of the time lost is common to every arm (the lead stops), or drop "below 1%" and keep the seconds. | W, M (S1) |

### 4.3 OPTIONAL (12; all P)

| ID | Location | Finding | Evidence quoted | Fix in the fewest words | Type |
|---|---|---|---|---|---|
| P-2 (regression) | Abstract, sentence 4 | "it" has lost its antecedent: the sentence on plans and amendments now stands between it and "covariance". | "Plans were hash-locked internally; amendments followed first results. With fixed noise it is nearly constant and adds nothing" | "With fixed noise the covariance is nearly constant". | W |
| P-3 | IV-C, twin definition | Matches the plan; three details are missing, and the test's reach is not said: a permutation within runs cannot tell ranking inside a phase from a level that follows the phase, which is the distinction the paper draws elsewhere ("level effect"). The adaptive filter's share (0.0459) is about its amplitude-matched oracle's (0.0477). | AMENDMENT_11 §6b: "permute f_i among each run's decisions that have a factor"; "drawn once, before any value" | Add "among the run's decisions that have a factor; drawn once" and one clause on what the within-run null cannot separate. | W |
| P-4 | `RECOUNT_COVERAGE_v13.md` (deposit record) | Counts agree with the paper (404 of 404 in the named passages; 409 of 409 over the whole main text, equal to S12; 164 supplement results, 188 marks, which I counted). Labels are still the old ones: "Tables II-V", "TABLE V." for what is Table 6; Table 5 has no line of its own; Sections II to IV have no per-passage line although the whole-text count includes them. My round-1 O-9, unchanged. | "Named passages: Abstract, Sections I and V-VII, Tables II-V, figure captions"; "TABLE V.: 83 value placeholders" | Regenerate with the paper's labels and one line per section. | T |
| P-5 | Table 4, Classification column | The caption says the classes are a test only for N, CK3, and the IMM at the lower level; only the PS rows carry "descriptive". TG and all higher-level rows read as test outcomes. | "TG, time gap ... safer, no extra cost"; caption: "a test only for N, CK3, and the IMM at the lower level and descriptive elsewhere" | Mark the tested rows, or add "descriptive" to the others. | W |
| P-6 (regression) | V-C (401 words, one paragraph); IV-C (319, one); IV-E (467, one) | The values moved in were added to existing paragraphs. V-C now holds classes, power, costs, the schedule's mismatch, and the nonbraking leads in one block. | Build report: "C. Closed Loop: 401"; "E. Locked Plans, Hypotheses, and Verification: 467" | Break each at its natural joints (V-C: before "These classes concern" and before "Behind leads"). | W |
| P-7 | III-D; Table 3 "retuned (median NIS near 2)" | The median is near 2 but no tuning run lies inside the window (two groups of ten runs, below and above). One-program diagnostic, so in words only. | S4: "no run lies inside the window: 10‡ runs lie between 0.48‡ and 1.77‡ and 10‡ between 2.22‡ and 10.99‡" | One clause: "the median falls between two groups of runs (Supplement S4)". | M (in words) |
| P-8 | Table 6 row labels | Decision counts still absent; 5,085 in-dropout decisions of 29,926 show how thin the dropout population is. My round-1 O-7. | S15: "29,926 decisions, 5,085 of them inside a dropout" | Add to the row labels. | M |
| P-9 | V-E, closed loop with dropouts | The equal-time-lost comparison takes contact share over 135 cases and time lost over the 89 without contact in any arm; stated, not named as a limit; no figure. My round-1 O-1, O-2. | "time lost is taken over the 89 of 135 cases without contact in any arm" | "(a limit: the two axes use different case sets)". | W |
| P-10 | Abstract; VII | "38% to 84% across run sets" are point values; the 38% is 20 tuning runs with interval [−0.22, 0.86] (export `TU.RR_CK3.ci`). | "78% of the room (38% to 84% across run sets)" | "point values of 38% to 84%". | W |
| P-11 | V-E, coast-count factors | The text does not say that the factors multiply the class average's critical scale, so that 0.216 means a wider margin. | "its factors (0.216, 0.107, and 0.065 ...) are the median ratios of the covariance margin's critical scale to the class average's" | Add "a factor below 1 widens the margin". | W |
| P-12 | Page 14; references | Last page has one column of references and an empty right column; [47] has no month; [24] "J. Geodesy". Advisory. | Page image 14 | Balance the last page. | W |
| P-13 | S12 "Presubmission reviews" | "Eight reviews" will not count this round. | "Eight reviews by panels of five agents" | Update at the next build. | T |

## 5. Q1 to Q8: what changed since my round-1 report

**Q1. Labels and sizes.** All three label slips of round 1 are fixed (N-9, N-10, the coast-count wording). The first amendment's closed loop now has its Table 6 row. One small gap remains in Table 4's class column (P-5).

*Value check.* I checked **382 printed values** against the first-program exports: **382 match** at the printed rounding. Every one has an agreeing second-program value (my key-by-key comparison of the 19 export pairs, the old-run pair, the step-0 recount, and the two Holm recounts found no differing result value; differences are file metadata, and NaN entries that are NaN in both). Coverage of the 382: Table 4, every cell (117); Section V-C beyond Table 4 (13); Table 2 (34); Table 3, four rows (48); Table 6, every cell with its adjusted p-values (106); Section V-E beyond Table 6 (44); Section V-D and Table 5 (15); Section III (5).

The values the revision brought into the main text, one by one:

| Item | Printed | Export key (pair) | Match | Second program |
|---|---|---|---|---|
| Two-noise IMM's modes | "0.18 before braking to 0.48 during it"; diagonal 0.95 | `B.MP.IMM2N.pre.mean`, `.braking.mean` (B12X); 0.95 is a design constant | yes | agrees (86 of 86 keys). Variance and window NIS: **one-program, not printed**, flagged in the sentence ("computed by one program") and ‡ in S15 |
| Adaptive filter's rule | "clip($m$, 0.25, 10) ... last three or fewer position updates" | Design constant: AMENDMENT_10 line 183; S4 | yes | not a result value (typed constant) |
| Decomposition's sample | "58,970 decisions of 366 runs"; 0.47; 0.06; 54%, 38%, 8% | `XH.n_ticks`, `XH.n_runs`, `XH.bind.r2`, `XH.dec.r2`, `XH.bind.share.*` | yes (7 of 7) | agrees |
| One-factor coast variant | 0.0347 [0.0109, 0.0581]; −0.0049 [−0.0094, −0.0006] | `DRF.RR_flag2`, `DRF.delta_flag2` | yes (6 of 6) | agrees |
| 10 Hz class average | "the 2 Hz one under the 2 Hz masks"; 0.0321 [0.0087, 0.0553]; 0.035 [0.014, 0.054] | `DR10.pbar.*` is identical to `DR.pbar.*` and `DR2.pbar.*`; `DR10.RR_N`, `DR10.in.RR_N`; AMENDMENT_12 §3d.4 | yes | agrees |
| First amendment's closed-loop row | −0.03 [−0.10, 0.03]; 0.15 [0.08, 0.24]; 60 cases | `E4.N.lo.dc`, `E4.N.lo.dt`, `E4.n_cases` | yes (7 of 7) | agrees (185 of 185 keys) |
| Table 4 cost columns | 36 cells (peak deceleration, rest gap, full braking) | `E3.<arm>.<level>.peakdec`, `.restgap`, `.fallback` | yes (36 of 36) | agrees (443 of 443 keys) |
| NA, AM, TG shares | 0.024 [0.015, 0.034]; 0.369 [0.331, 0.404]; 0.287 [0.231, 0.332]; the order in every run set | `LB.all.RR_NA`, `RR_AM`, `RR_TG`; `TRANSFER.structured.per_set.*` | yes (9 of 9; order holds on tuning, old, fresh) | agrees |
| Braking-phase NIS | "several times its expected value" (no number) | Table S7, ‡ | words agree with S7 | **one-program, not printed**, flagged in the sentence |
| nuScenes pair classes | cars, trucks, buses, trailers; 2.0 m; not stratified; 5.21 m against 2.45 m | AMENDMENT_12 lines 448 to 460; `M.s.in_miss.mean_s`, `M.s.steady.mean_s` | yes | agrees for the two values; the classes are definitions |

**I found no one-program value printed in the main text.** The two one-program diagnostics are described in words and say so.

*Recount-scope sentences against `RECOUNT_COVERAGE`.* Section IV-E and S12 now use one sentence ("every result value printed in the main text and all but the marked (‡) values of the supplement"). The record supports it: 404 of 404 in its named passages, 409 of 409 over the whole main text (S12 prints the same 409), 164 supplement results marked with 188 marks (I counted 188). The shared-library limit and the 20-decision check are in the main text. The record's own labels are stale (P-4).

*Permuted twin against AMENDMENT_11.* Matches (N-2 row).

**Q2. Overreach.** The summary sentences now carry "at 2 Hz", "partly", "slightly more (descriptive)", the planner, the interface, and the speed range. "Recovered nothing" is gone. I found no new overreach. Two soft spots, both optional: the range "38% to 84%" without "point values" (P-10), and the twin test's reach (P-3).

**Q3. Earlier limits.** Unchanged in substance, as expected of a text-only revision: (a) to (e) addressed as in round 1, now also in the summaries; density (f) is worse; an expected confirmatory result, small positive effects, one simulator and planner, and no decision-level real-log evidence remain and are stated. The process limits are disclosed; N-1 is the open part.

**Q4. Readability.** Better: Section V-E has five headed parts, "level effect" is defined at first use, the twin and the pass rule are defined. Worse: three long single paragraphs (P-6), a dangling pronoun in the abstract (P-2), and one sentence whose number cannot be read without the supplement (P-1).

**Q5. Verdict.** Section 2. Most likely editorial outcome at OJ-ITS for (a): major revision, because of the declaration and the abstract-level reading stated in Section II; for (b): minor to major, on the structural limits and the length.

**Q6. Self-containment.** All ten of my round-1 cases are closed. One new case: the closed-loop run length (P-1). Two facts stay in the supplement by the paper's own recount rule and are announced in the main text.

**Q7. Format and declarations.** Five of the six N-20 parts are done and verified on the page images (ACK order, Fig. 2 labels, joined prefixes, lettered table notes, [21]). Open: [10]'s surname. Advisory: the last page's empty column, [47]'s month, [24]'s abbreviation.

**Q8. AI disclosure.** Now its own paragraph, third, naming the panels, their models, and the workflow, and pointing to S12 for the model of each pass; S12 does name them and states that the last wording changes had no further audit. I confirmed from the files that the Holm recounts name Claude Sonnet 5.5 and that the recovered programs read only the export pairs. Open: sentence 1 (N-1).

**Length and density at 14 pages.** The body's 8,253 words are at the project's own ceiling. The added facts were needed and each is short, but they landed inside existing paragraphs, so the densest places got denser: Section V-E is 1,503 words, V-C one 401-word paragraph, Table 4 ten columns at about 7 pt, Table 6 up to four intervals in a cell. The journal recommends ten pages. If anything is cut, cut from Section II's standards paragraph and from Table 5's tercile and drawn-reaction rows, not from Sections IV-E or V-E. Paragraph breaks (P-6) would help more than cuts.
