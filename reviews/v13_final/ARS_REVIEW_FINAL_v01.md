# ARS final review of revision v13: panel record (editor-synthesis seat)

- **Seat:** editor-synthesis, Claude Sonnet 5.5 (not the final text's writer, Fable 5.2, nor the earlier writer, Opus 5.5). One seat; no sub-agents; read only; no web.
- **Written:** 22 Nov 2026, 12:30 EST (Get-Date).
- **Frozen text judged:** `revision_v13\work\A_text\out\freeze_v13_1201\` (frozen 22 Nov 12:01:26; 12 typeset pages).
- **Seat report hashes:** all five equal the coordinator's 12:24 values (section "Hashes").
- **How I checked:** every kept finding was looked up in the frozen `MANUSCRIPT_v13.md`, and where it rests on the supplement, in `SUPPLEMENT_v13.md`. Layout findings were checked on page images 1, 6, 9, 10 and 11 (the other pages were not needed for any kept layout finding). Where a seat's evidence did not hold, it is dropped or downgraded below.

## 1. Seat table

| Seat | Model | Recommendation | Score /10 | Stars /5 |
|---|---|---|---|---|
| EIC, journal fit | Claude Sonnet 5.5 | Major revision | 6.0 | 3 |
| R1, methodology | Claude Fable 5.2 | Minor revision (states the likely editorial outcome is major) | 6.6 | 3.5 |
| R2, domain | Claude Opus 5.5 | Major revision | 6.5 | 3.5 (3.25) |
| R3, practical | Claude Sonnet 5.5 | Major revision (light) | 6.8 | 3.5 |
| Devil's advocate | Claude Fable 5.2 | Major revision | 5.5 | 3 |
| **Seat mean** | | | **6.28** | 3.3 |

## 2. Panel decision and score as frozen

- **Decision: Major revision (a light one).** Four of five seats say major; R1's "minor" is for the methodology alone and the same seat expects a major outcome at the venue. Every required fix below is a wording change, a value moved from the supplement, or text the author writes from existing records. None needs new analysis.
- **Score as frozen: 6.3 / 10 (about 3 stars of 5; seat range 3 to 3.5).** This is the seat mean (6.28, rounded). My own judgement is the same. Median 6.5; the lowest seat (DA, 5.5) says it scores what a skeptical referee would defend and 7 on craft alone; the two seats that share the final writer's model (R1 at 6.6, DA at 5.5) sit on opposite sides of the mean, so the model overlap does not tilt it in one direction. I make no adjustment, because the gap between mean and median (0.2) is inside the seat spread (1.3).
- **No CRITICAL item.** No seat found one and I found none: I traced the labels (confirmed only for the original plan; "passed", "failed", "replicated" for amendment tests), the Holm values and the abstract numbers against Table 6, Table S37 and Table S38, and found no label or number that contradicts its source. The two open placeholders (repository DOI, AI confirmation sentence) are gates.
- Correlated-error caveat (from the provenance file): all seats and this synthesis are Claude models; the agreement between seats is weaker evidence than five independent humans would give. Where two or more seats agree and the text confirms it, I say so; I did not count votes.

## 3. Adjudication of disputes

**D1. "A level effect that needs no covariance" (coast-count result). Ruling: overshoots as worded. Required (R-1).**
Facts checked: Supplement S15, "A fixed coast-count margin": "Each factor is the median ratio of the covariance margin's critical scale to the class average's, relative to steady decisions, fitted on the first amendment's 105 fresh runs, which share no run with the 150 test runs" (factors 0.216, 0.107, 0.065 and 0.925 after re-acquisition). The main text (V-E, third paragraph, and VI "What a varying covariance needs": "model missed updates explicitly instead of through the covariance, as the coast-count margin does here") never says the factors come from the covariance. What the control shows: nothing in the covariance's per-decision variation beyond its median growth per missed update. It does not show that a designer without a covariance would have found those factors. R1 and DA are right on the facts; R2 reaches the same reading from Kalman theory (with fixed noise the covariance is a function of the miss pattern). R1's further claim that the control "could hardly come out otherwise" is a reasonable inference, not a result, and I do not rule on it; the text can simply state where the factors come from and let the reader see it. The text already says "ranking among dropout decisions is not shown at 2 Hz", which is correct.

**D2. nuScenes check: must the IMM secondary's opposite sign be in the main text? Ruling: yes. Required (R-2).**
Facts: Table S45: the online tracker 0.108 [0.039, 0.172] around misses and −0.038 [−0.070, −0.006] over all pairs; the IMM (secondary) 0.210 [0.158, 0.255] and +0.093 [0.066, 0.116]. The main text (V-E last paragraph; abstract "slightly inversely over all tracks"; VII) reports only the online tracker's pattern and calls it "the covariance's". The inverse sign over all pairs is therefore a property of the fixed-noise tracker, and the one tracker whose covariance can vary has the opposite sign. In a paper whose thesis is that covariances rarely help, leaving that out is an omission of the result that favours a covariance. One clause each in V-E and Table 6, and "the fixed-noise tracker's spread" in the abstract and VII.

**D3. "Inside the ±5% margin": beyond point values and beyond start probability 0.10? Ruling: it holds only for point values at 0.10; the Conclusion drops both qualifiers. Required (R-3).**
Facts: Table 6: share 0.0298 [0.0077, 0.0518] (upper end above 0.05); 0.0525 [0.0287, 0.0745] at start probability 0.20 and 0.0514 at 0.30 (point values above 0.05); two-noise IMM 0.0220 [0.0185, 0.0253] (inside). The abstract says "these point values lie inside the ±5% margin" (qualified as point values, silent on the rate); V-E says "as point values ... (no equivalence test was registered for them)" (qualified, silent on the rate); the Conclusion says "both lie inside the ±5% margin" with neither qualifier. Also the adaptive filter's 4.6% (interval to 0.0533) is outside that sentence and is not mentioned in it. The reading "small by that margin" is fair at the registered rate; it should say so and add that the dropout share is about 5% at two and three times that rate.

**D4. Is the null a property of the constant-velocity prediction (R2)? Ruling: partly yes; the scope is real and not stated where the claim is general. Required as wording (R-5); the one test that would settle it is new analysis and is not required.**
Facts: III-E: planner works "with actors predicted at constant velocity"; Table 3 room by phase for the tracker of record 1.63 / 23.62 / 0.08 points (almost all in braking); CK3, a predicted-path change, recovers 0.783 of the room. So most of the room is the error of a constant-velocity prediction at braking onset, which a second-moment quantity such as a fixed-noise covariance cannot track. The abstract's first sentence, Section I Scope and Section VII state the null without "with a constant-velocity prediction"; the Limits paragraph scopes only the IMM tunings. R2's claim that the retuned variants are strongly overconfident in braking (NIS 7.9 to 9.6) rests on old exploratory runs in the supplement and I did not rely on it. Whether a covariance adds anything on top of CK3's predicted path is untested: stated as a limit, not run.

**D5. Is "lower bound" for the two-noise IMM supported (R2)? Ruling: no. Required (R-4).**
Facts: "Through the position–velocity interface (Section III-D) this share is a lower bound" (V-E); "a lower bound for that interface" (VI Limits). No test and no argument in the main text or S15 shows that a wider interface would raise the share; S15 Table S42 shows the maneuver mode's probability exceeds 0.5 for 13% of before-braking decisions, which could add margin where none is needed, so the sign is open. Four seats (EIC, R1, R2, DA) flag it; R3 accepted it. Replace with "holds for that interface only; a wider interface was not tested."

**D6. "Preregistered" in the title versus the body (EIC, DA). Ruling: the body carries the qualifier; the abstract does not. Title stays the author's choice; required fix is in the abstract (R-9).**
Facts: IV-E begins "By 'preregistered' we mean internal locks, not a public registry: SHA-256 hashes with local file times and no third-party timestamp"; Table 1 says amendment sequences were "written after the fresh lead-braking results were seen"; V-E says dropouts were "specified after the fresh lead-braking results had been seen". So no sentence contradicts the title. The abstract says "under a locked plan" once (for the first result), then "In amendment tests" and "replication", and never says the locks are internal or that the amendments followed the results. The abstract carries most of the positive results; an editor reading title and abstract only will assume a registry. Note also that "preregistered" is used before its definition (III-B "preregistered triple", V-E "a preregistered output-rule change"); this is a suggestion (S-14).

**D7. IV-E Holm sentence (R3, R2). Ruling: misleading antecedent; required (R-6).**
Facts: "within the second amendment, six primary hypotheses are Holm-adjusted (Table 6). In lead braking they are room; detection in a ±5% band; the tracker's equivalence...; the IMM's classification; transfer of the per-phase schedule; and a braking-prediction share above 0.5." "They" reads as the six Holm hypotheses, but the list is the original lead-braking sequence, which is also six and is not Holm-adjusted (Table S37 lists the six real ones: dropout replication, dose slope, two-noise IMM class, adaptive twin replication, closed loop with dropouts, nuScenes mechanism). The Table 6 caption and V-E have it right.

**Other disputes settled**
- *The Conclusion replicates the abstract* (EIC): confirmed (same numbers in the same order); template line 473. In Q7 and R-8.
- *"Rarely beat" counts untestable settings as losses* (DA-1) with the adaptive filter missing from summaries (R2-04): holds in part. The abstract's lead sentence is true of the confirmatory equivalence and false as a count of settings: where the covariance varied and had room (dropouts, replication, two-noise IMM, adaptive filter) it gained 2% to 5% of the room. Required as a wording balance (R-8). I do not accept DA's "near-even desk-reject risk" as a finding; it is a judgement about fit, kept in the forecast.
- *"Equivalent within 0.10 contact share" reports a resolution limit* (DA-7, EIC J11): disclosed in V-C ("with 60 cases per arm contact differences much below 0.10 cannot be resolved. Equivalent here does not mean safe."), absent from the abstract. Suggested (S-2).
- *"Recovers slightly more" is a reverse reading of a failed one-sided test* (R1 F5): true of the point values (0.0322 against 0.0298); the text prints the interval and "failed". Suggested (S-8).
- *Acknowledgment pointer "(Supplement S12)"* (R1 F13 ii): S12 holds the claim audit and the second-program record; the pointer is attached to "audited the claims" and is correct. Dropped. (S12 does not name models; the models are named only in the paragraph. Not a defect.)
- *R3-2, the closed-loop cost read only on easy cases*: true (time lost exists only where no arm made contact: 89 of 135 cases, Table S44). Merged into R-16.
- *EIC J5/R3-6 title*: see D6.
- *DA-6, equivalence could not fail*: the text already says so ("expected from this constancy; what the test adds is the bound"); DA marks it disclosed. A structural limit, not a fix item. I add the δ reason to suggestions (S-20).

## 4. REQUIRED items

Type: **W** wording only; **M** existing value moved from the supplement (named); **T** text the author writes from existing records (no new analysis); **A** new analysis (none required).

| # | Location | Raised by | Fix in the fewest words | Type |
|---|---|---|---|---|
| R-1 | V-E third paragraph ("needs no covariance"); VI "What a varying covariance needs" ("instead of through the covariance"); 10 Hz sentence | R1 F1, DA-2, R2-05, R2-18 | State "its factors (0.216, 0.107, 0.065; 0.925 after re-acquisition) are the covariance margin's median ratios per missed update, fitted on the 105 earlier runs"; replace "needs no covariance" with "needs no per-decision covariance"; add "(10 Hz: not compared with a coast-count margin)". | W + M (S15 coast-count paragraph) |
| R-2 | V-E last paragraph; Table 6 nuScenes row; abstract; VII | R1 F2, R2-08 | Add the IMM secondary: 0.210 [0.158, 0.255] around misses, 0.093 [0.066, 0.116] over all pairs; say "the fixed-noise tracker's spread" in the abstract and VII. | M (Table S45) |
| R-3 | Abstract; VII; V-E | R1 F4, DA-5 | "These point values, at dropout start probability 0.10, lie inside the ±5% margin (about 5% at 0.20 and 0.30)"; VII: restore "as point values". | W |
| R-4 | V-E (two-noise IMM); VI Limits | EIC J10, R1 F8, R2-02, DA-9 | Replace "a lower bound" with "holds for that interface only; a wider interface was not tested". | W |
| R-5 | Abstract line 1 or I Scope; VI; VII; Limits | R2-01 | Add "with a constant-velocity prediction"; one sentence in VI: the room lies almost wholly in braking (Table 3: 1.63 / 23.62 / 0.08 points by phase), a mean-path error a fixed-noise covariance cannot track; list "covariance added to CK3's path" as untested. | W (the test itself would be A, not required) |
| R-6 | IV-E Holm sentence | R2-09, R3-1 | Name the six Holm hypotheses (the H rows of Table 6) in one sentence; give the original lead-braking sequence in a separate sentence, "not Holm-adjusted". | W |
| R-7 | Table 6 rows "share minus a fixed coast-count margin's" and "contacts at equal time lost"; V-E last paragraph | EIC J13, R2-10, R3-7 | Put "Holm within the third amendment's two: 0.99; 0.18" beside the two failed labels and extend the caption. | M (Table S38) |
| R-8 | Abstract sentences 1 and 5; VII sentence 1; Section I contribution 2 | DA-1, R2-04, EIC J3 | Replace "rarely beat ... and then by little" with the two-sided statement: nothing where it is near-constant; 2% to 5% of the room where it varies and there is room (dropouts 2.8%, two-noise IMM 2.2%, noise-adaptive filter 4.6%, replicated against its permuted twin); a coast-count margin matches the dropout gain. Rewrite VII so it does not repeat the abstract (template line 473). Keep the abstract at 245 words or fewer. | W |
| R-9 | Abstract | EIC J5, DA-3 | Add "internally hash-locked plan; amendments written after the fresh results" (about 9 words; trade for words cut under R-8). Title unchanged. | W |
| R-10 | Abstract; I contribution 2; VII ("varies mostly for other reasons") | EIC J4, R1 F11, DA-8 | Add "exploratory" or drop the clause; in V-E add the other two shares (update schedule 54%, geometry 38%) and "decision-level R² 0.06". | W + M (Table S46) |
| R-11 | ACKNOWLEDGMENT AI paragraph | EIC J16, R1 F13, R2-17, R3, DA-12 | See Q8: scope of the recount to IV-E's; "Fable 5.2 revised for the second amendment" understates (provenance: Fable 5.2 wrote the round-2 text and the submission pass); open with a sentence that has a verb; keep the AI-panel sentence. | W |
| R-12 | ACKNOWLEDGMENT first sentence; IV-E | DA-4 | One sentence in IV-E: the three amendments were written and locked 21-22 Nov 2026 (Table S29: 14:23 to 06:48), after AI-panel reports, and the third's two controls were asked for by that panel (Table S5). Change "made the scientific decisions" to what the deposit supports (AMENDMENT_13 records design choices as "the coordinator's"), e.g. "approved its plans and design decisions", only if the author confirms it is true. | W (author confirms facts) |
| R-13 | III-A; V-E; Table 6 row 1; abstract | EIC Q6-1, R3, DA | Describe the pedestrian-crossing scenario in two sentences: who moves, speeds, what the planner constrains, 390 runs, why step 0 showed little room. The scenario is described nowhere in the paper or supplement (S14 and S33 give results only). | T |
| R-14 | III-B; Tables 4 and 6; V-C; V-E | R3 Q6 | Define "time lost" and "rest gap" in one clause each. I found no definition in the main text or in S1 to S3 and S9. | T |
| R-15 | V-E dropouts; Table 6 | R1 F15, R3, DA, EIC | State the primary start probability, 0.10, that it masks 16.2% of updates, and what "dropout-estimated class average" is. | M (Table S39) |
| R-16 | V-E equal-time-lost sentence; Table 6 | R1 F7, R2-19, R3-2, EIC | Add: "read by linear interpolation between scales 4 and 8: 25.7% against 20.7%; time lost over the 89 of 135 cases without contact in any arm"; state the time-lost baseline (about 25 s). | M (S15, Table S44) |
| R-17 | Table 2 caption; abstract | R1 F6, DA Q6-5 | Replace "at the levels of Supplement S5" with the levels: 95% except N's share (99.4%, calibrated) and the IMM's share (99%, nominal). | M (Table S9) |
| R-18 | II ("Adaptive covariances", "Novelty") | R2-03 | Add "under regular updates" to the steady-state sentence; two or three sentences placing intermittent-observation Kalman filtering (predicts the coast-count result), data-dependent covariances (association-uncertainty filters), and ITS threat-assessment work under sensor uncertainty; add the references. R2's suggested references are from memory and unverified; the author must check them. | W + references to verify (no new analysis) |
| R-19 | Q7 list below | EIC, R1, R2, R3, DA | Fix the format misses (reference forms, figure labels, caption, hyphens, fragment). | W / layout |

After R-13 to R-17 the sentence at the end of Section I, "The main text holds every result on which the claims rest", is true; the remaining Q6 items below are minor.

## 5. SUGGESTED items

| # | Location | Raised by | Suggestion |
|---|---|---|---|
| S-1 | Abstract | EIC J1, R3-11, DA | Cut to about 200 words: three claims, four numbers; say "simulated and replayed driving tests" (EIC J2) and "a public data set (nuScenes)". |
| S-2 | Abstract; I | EIC J11, DA-7 | "In closed loop (60 cases, 20% baseline contacts) no difference above 0.10 was resolved." |
| S-3 | End of I | EIC J6 | One designer take-away sentence (the covariance's gain is a level effect; a braking prediction carries far more). |
| S-4 | V-E; Table 1 | EIC J7, R2 Q4, R1 | Road-map sentence at the start of V-E; move Table 1 to Section I; define "rest gap", "decision-equivalent", "off-policy", "young tracks". |
| S-5 | Table 3 rows "IMM re-tuned", "IMM two-noise" | EIC J12, R1 F9 | Print the class ("would classify as recovers; descriptive"). |
| S-6 | Table 4 | R2-11, R1 F3 | "Safer, time cost within tolerance" for CK3; add the class-average check at equal time lost behind braking leads (24.89 s against 24.78 s, Table S23). |
| S-7 | Table 6 | R1 F16, R2-13 | One quantity per cell for the dose rows; use "start probability" throughout; name the run sets once. |
| S-8 | V-E, Abstract | R1 F5 | "Recovers as much (0.032 against 0.030)" instead of "slightly more"; note that the interval is uncalibrated. |
| S-9 | V-D update-rate sentence | R1 F10 | "A consequence of the age of the track state (update interval plus latency)": Fig. 4(a) shows latency moves the room as much as the rate. |
| S-10 | Abstract | R3-3, R3-4 | Add that a plain time gap matched the braking prediction at lower time lost (descriptive), and "random" before "dropouts". |
| S-11 | VI; II | R2-07 | One sentence on whether [19]'s comparison held caution equal. |
| S-12 | VI heading | EIC J9 | "...on the nominal runs". |
| S-13 | Limits | R1 F12, R3-5 | Name the conditioning of time lost on no-contact pairs; no claim about margin size at any contact rate. |
| S-14 | III-B, V-E | (mine) | "preregistered" is used before IV-E defines it; define at first use or write "locked". |
| S-15 | IV-C | DA-6, R1 F18 | Give the reason for δ = 0.05 and say the covariance's interval lies below the ±5% oracle's. |
| S-16 | I Scope; [10] | DA-13 | One clause on how the sibling manuscript's question differs. |
| S-17 | III-E | R2-14 | Say whether process noise over the look-ahead is included. |
| S-18 | V-C | R2-15 | Add the braking-prediction, time-gap and schedule full-braking shares (2% to 9%) next to F0's 52.7% and 78.6%. |
| S-19 | IV-A and V-E | EIC Q7-9 | Rename the reaction time (one symbol, two meanings: reaction time and Kendall's τ). |
| S-20 | V-E; Table 6 | R2-08 | Define a "real missed detection" and say a missed-update count would likely rank the same pairs. |
| S-21 | I contribution 2 | R2-16 | "(Sections V-A and V-E)". |
| S-22 | References | EIC J15 | The paper cites one OJ-ITS paper ([19]) and no T-ITS paper: author to check for two or three ITS journal references (not checked here). |
| S-23 | `RECOUNT_COVERAGE_v13.md` | R1 F14 | R1 reports stale table numbers in the coverage record. I did not read that file; the author can regenerate it. |

## 6. Q6: self-containment (deduplicated, each checked)

All sixteen are pointers where a claim in the main text rests on a supplement-only value or definition. Where the fact is not in the supplement either, it is marked "new text".

| # | Main-text location | Rests on | Fact to bring in | Checked | Item |
|---|---|---|---|---|---|
| Q6-1 | I contribution 2, V-E, Table 6 row 1, abstract: pedestrian crossing | not in the supplement (S14, S33 give results only) | Scenario: who moves, speeds, what the planner constrains, 390 runs, why step 0 showed little room (new text) | III-A describes lead braking, cut-in and non-braking leads only | R-13 |
| Q6-2 | V-E, VI, abstract: coast-count margin | S15 | Factors 0.216, 0.107, 0.065, 0.925; the covariance margin's median ratios; the 105 earlier runs | S15 text | R-1 |
| Q6-3 | V-E equal time lost; Table 6 | S15, Table S44 | Interpolation between scales 4 and 8 (25.7% against 20.7%); time lost over 89 of 135; time-lost baseline | S15, S44 | R-16 |
| Q6-4 | V-E dropouts; Table 6 | S15, Table S39 | Primary start probability 0.10; 16.2% of updates masked; what the dropout-estimated class average is | main text lists four rates without naming the primary | R-15 |
| Q6-5 | Table 2; abstract interval | Table S9 | Interval levels: N's share 99.4% (calibrated); IMM's 99% (nominal) | Table S9 | R-17 |
| Q6-6 | V-E nuScenes; abstract; VII | Table S45 | IMM secondary 0.210 and 0.093 with intervals | Table S45 | R-2 |
| Q6-7 | V-E; abstract: "other reasons" | S15, Table S46 | Three groups of regressors, Shapley shares 54% / 38% / 8%, decision-level R² 0.06 | Table S46 | R-10 |
| Q6-8 | III-B; Tables 4, 6; V-C; V-E: "time lost", "rest gap" | defined nowhere I could find | One clause each (new text) | grep of main text and supplement | R-14 |
| Q6-9 | V-C last two sentences: classes behind non-braking leads | Table S25 | Contact differences: 0.00 for keep-speed and mild-brake leads; −0.25 [−0.47, −0.04] for stop-and-pull-away (CK3 and PS) | Table S25 | S |
| Q6-10 | V-E two-noise IMM "tuned on braking" | S15 | Maneuver variance 0.917, tuned by the NIS rule on tuning-run braking frames; transition diagonal 0.95; never tuned on new runs | S15 | S |
| Q6-11 | V-E nuScenes: "real missed detection", "in or just after a miss" | not in the supplement either | One clause defining a miss (new text) | Table S45 caption and S15 use the phrase without a rule | S-20 |
| Q6-12 | II "Novelty, with its limits" | S13 | Search scope: web, preprint and scholarly engines, English only, 17-18 Nov 2026, abstracts only, no full texts | S13 | S |
| Q6-13 | V-D: "inside the margin at every rate and latency"; "sources' shares keep one order" | S5, S6 | Table 5 gives N only at 10 Hz and 0.1 s; add the 5 Hz and 0.2 s cells or soften | Table 5 | S |
| Q6-14 | V-E adaptive filter "permuted twin" | S15 overview | What is permuted and the twin's own share (−0.0056 on the new runs) | S15 | S |
| Q6-15 | V-E 10 Hz "gave the same class" | S15 | The class average there is the 2 Hz one; no coast-count control was run at 10 Hz | per R2 and EIC; not re-derived by me | R-1 (clause) |
| Q6-16 | V-E last sentences: earlier closed loop with dropouts "found equivalence at the lower level; at the higher ... fewer contacts for more time lost" | S14 | The two levels' contact and time-lost differences (lower: −0.03 [−0.10, 0.03], 0.15 [0.08, 0.24] s, Table S32) | the main text gives no numbers; I read Table S32 only for the lower level | S |

Pointers that only offer more detail (S1 configuration, S4 tuning, S5 full tables, S10 clearance, S11 diagnostic) are not cases.

## 7. Q7: format and declarations (deduplicated; each checked against the text, the template or a page image)

Checked and correct: all headings in capitals (pages 1, 6, 9, 10, 11 seen; the other seats saw the rest); "Fig. N" in running text and "FIGURE N." in captions; Arabic table numbers; "Table S" in supplement pointers; one spelling "preregistered" (4 uses plus the title; none hyphenated); funding in the first-page note, no Funding heading; one ACKNOWLEDGMENT in the required order; running head "Kopalli: Tracker Covariances as Safety Margins in Motion Planning" on even pages; five index terms; author, affiliation, ORCID and corresponding author with email present; no British spelling and no contractions found; the abstract has no abbreviation. Dropped by the brief's fact: the template's "do not abbreviate Figure" (line 452); the society-logo line, "Received XX Month", DOI placeholder, "VOLUME ,", licence line (all the template's). Not counted: the two bracketed placeholders (gates).

| # | Location | Miss | Source of the check |
|---|---|---|---|
| Q7-1 | Throughout: "Pre-submission" (Ack), "non-braking" (3 uses), "multi-object" (abstract, I), "re-tuned", "re-detected", "pre-stated", "re-score" | Template line 226: prefixes such as "non", "multi" are usually joined without a hyphen | grep of the .md; template |
| Q7-2 | VII | Conclusion repeats the abstract (same numbers in the same order); template line 473 | text |
| Q7-3 | [26], [37], [38] | No place of publication (template books: "City, ST, Country: Publisher") | reference list |
| Q7-4 | [39] | No year, no date, no "Accessed:" | reference list |
| Q7-5 | [40], [41] | Day-first dates ("9 Mar. 2021", "4 Jan. 2023"); free-text tails ("authentic text", "in force from", "consolidated as"); [40] has no author | reference list |
| Q7-6 | Conference references [3], [6], [9] and others | City and month given for [1] and [18] only; inconsistent with the template's conference form | reference list; page 11 |
| Q7-7 | [9], [13], [15], [21], [31] "et al." | Template: use all names unless not given; cannot be checked offline (IEEE allows et al. above six authors): author to check | template line 495 |
| Q7-8 | Section II, "[7], [22], [8]" | Group not in numeric order | text |
| Q7-9 | Fig. 4, page 9 | Sub-figure labels "(a)", "(b)" are bold, above and left; template line 424: centered below, 8 pt | page 9 image |
| Q7-10 | Fig. 2 right panel, page 6 | Axis ticks with no label; the panel is a flat line | page 6 image |
| Q7-11 | Fig. 2 caption, page 6 | "The IMM (dashed) is drawn with its own class average": in the legend the IMM is solid and "F0 (IMM)" is dashed | page 6 image |
| Q7-12 | ACKNOWLEDGMENT AI paragraph, first sentence | "Content generated by artificial intelligence (AI), disclosed under IEEE policy." has no verb | page 11 |
| Q7-13 | Abstract, IV-E, III-A | First use of "SHA-256", "CANMOT", "CARLA" not expanded in the body (CANMOT is a name, expanded in [5]); F0, N, E appear before Table 1 on page 4 though Section I points to it | text |
| Q7-14 | Page 10, Limits | "younger than 1 / s." breaks across lines | page 10 image |
| Q7-15 | V-E dropouts | "(lead braking, this mask law and output rule only)": serial comma missing if three items | text (low confidence) |
| Q7-16 | First page, affiliation | Template form is "City, ST ZIP USA"; the paper has "Troy, MI, USA" (form only) | page 1; template line 36 |
| Q7-17 | Section II and VI bold run-in headings | Bold sentence-case run-ins ("Novelty, with its limits.", "Why the fixed-noise covariance carries no measurable decision value.") are not template heading styles; advisory | page 9 image |
| Q7-18 | SUPPLEMENT headings S1 to S15 | Title case; applies only if the supplement is typeset in the template (conditional) | supplement headings |
| Q7-19 | End of paper | No author biography and no drop-cap first paragraph (template lines 60, 802 to 837); production adds these at the final stage (template line 45): advisory | page 1, page 12 per DA |

Risk, not a miss: the abstract is exactly 250 words by a whitespace count (I counted 250; a counter that splits hyphenated words gives 261). The limit is "250 or fewer", so it passes, but R-8, R-9 and S-1 should end at 245 or fewer. Count: 19 entries, of which 15 are misses (Q7-1 to Q7-6, Q7-8 to Q7-12, Q7-14 to Q7-16 and Q7-13), 1 is to be checked (Q7-7) and 3 are advisory or conditional (Q7-17, Q7-18, Q7-19).

## 8. Q8: AI disclosure

**IEEE's rule** asks for disclosure in the acknowledgments, naming the AI system, the sections that use it, and the level of use.

**(a) As frozen.** Meets the three elements in form: Claude (Anthropic) with the three models and OpenAI Codex; Abstract, Sections I-VII, the supplement, code; searches, code written and run, text drafted, recounts, audits; in the ACKNOWLEDGMENT in the right order. Facts against Section IV-E and the provenance file:
- "wrote the second programs that recount every printed value" is wider than IV-E ("every value printed in the main text and all but the marked (‡) values of the supplement; they share the scoring library, stored arrays, and resample draws"). Overstates.
- "Claude Opus 5.5 wrote the first programs and the text, which Claude Fable 5.2 revised for the second amendment" understates: the provenance file records Fable 5.2 as writer of the round-2 text and of the submission pass.
- The opening sentence has no verb; the model-by-model run is long, so the level of use is hard to find.
- Strong points: it names the AI panel's reviews and says requests and responses are deposited.

**(b) The candidate.** Shorter, leads with accountability, and its recount sentence matches IV-E ("every value printed in the main text"; "had not seen the first programs"). It understates the use in four places, so it is not acceptable unchanged:
1. It drops the AI-panel sentence; the supplement records that the second amendment followed a panel review and that the third's two controls were "asked for by the round-2 panel" (Table S5, row "Third amendment").
2. "Made every scientific decision" is contradicted by the deposit: AMENDMENT_13 records design choices as the coordinator's (the coast-count baseline, the arms dropped from the equal-time-lost test, the nuScenes population "the coordinator's decision"). This sentence is not the author's confirmation gate; it is a factual claim I can test and it fails as written.
3. "Wrote" without "ran" understates (the frozen text says "wrote and ran").
4. "Drafted and revised the text of all sections" does not name the Abstract; "assisted" for Codex weakens "developed with" without saying so; it omits that the recount shares the scoring library.

**Desk-rejection risk.** An editor will not reject for breaking the disclosure rule if version (a) or the edited (b) is used; both name system, sections and level. The remaining risk is the fact disclosed (all text and code AI-generated, one author), which no wording removes and none should hide. Open placeholders (repository DOI, author's confirmation sentence) raise the risk more than the wording does.

**Ruling.** Version (b) as the base, with (a)'s completeness restored. It lowers the risk (short, accountability first, recount scope right) and with the edits does not understate. Recommended paragraph:

> The author conceived the study, set its questions, approved its plans and design decisions, and takes responsibility for the work. [AUTHOR CONFIRMATION: the author to state here what the author has verified personally.] Generative AI was used extensively and is disclosed here under IEEE policy. Under the author's direction, Claude (Anthropic) carried out the literature searches and summaries, wrote and ran the analysis, simulation-control, and figure code, and drafted and revised the Abstract, Sections I–VII, and the supplementary material. Claude Opus 5.5 wrote the first programs and the first text; Claude Fable 5.2 revised the text for the later amendments and the submission. AI sessions also wrote the amendment plans and proposed design options; where the amendment files record a design choice as an AI session's, it was made within the author's approval [author to confirm]. Separate Claude sessions (Sonnet 5.5 and Fable 5.2) that had not read the first programs wrote second programs that recount every value printed in the main text and all but the marked (‡) values of the supplement; the two sets share the scoring library, stored arrays, and resample draws (Section IV-E). Claude Fable 5.2 and then Claude Sonnet 5.5 audited the claims against the plan and result files (Supplement S12). OpenAI Codex [model and version, to be added by the author] was used to develop the simulation, recording, and planner software in an earlier phase. Pre-submission reviews by an AI panel shaped this manuscript; the requests and responses are deposited.

Every factual claim matches Section IV-E (recount scope, shared components), Supplement S12 (claim audit), Table S5 (panel origin of the later amendments) and the provenance file (writers). The two bracketed author sentences are gates: the author must confirm each statement is literally true before signing. I could not check which model did each audit beyond what the frozen text says.

## 9. Honest forecast

- **After the required items in one fix round: about 6.7 / 10 (range 6.5 to 6.9), still major revision at a journal, with desk-reject risk falling from moderate to low-moderate.** The gain comes from three sources: the abstract and conclusion stop leaning to the null (R-3, R-8, R-10) and stop omitting the result that favours a covariance (R-2); the two claims that overreach (R-1, R-4) go; and the main text becomes self-contained (R-13 to R-17). Seats' own estimates of the single biggest lever (rewriting the abstract and Conclusion symmetrically, the "internal locks" qualifier visible, the coast-count origin stated) are the same items.
- **What keeps it below 8, and a fix round cannot change:**
  1. The one confirmed covariance result is a near-constancy null that could hardly fail: the tracker's own oracle recovers 0.0001 of the room, the ±5% margin is wider than a perfect ±5% ranking oracle's whole share (1.3%).
  2. The positive effects are 2% to 5% of the room, partly level effects, and both third-amendment controls failed: no covariance-specific gain is shown.
  3. One simulator, one planner, one configuration, mainly 2 Hz without latency; no decision-level real-log test, because the logs showed no room.
  4. Process: the amendments were written after the results, locks rest on one laptop's file times, and all text, code and review were AI-generated under one author.
  5. Density: 12 pages and a 900-word results section.
- **The one change that would lift the score most is new analysis, outside a fix round:** a decision-level test on real logs or a second simulator and planner where there is room and the covariance varies, locked with a third-party timestamp.

## 10. Hashes

SHA-256, computed at the start and re-computed at the end of this run (identical):

| File | SHA-256 |
|---|---|
| phase1\01_eic_journal_fit.md | bdf3ceb8f6ac623f0fb48d4c7a5f4b7bb90f3d4775f932b73b933037c7dafc27 |
| phase1\02_r1_methodology.md | 4145da3065b880eb6eb9819ab046d2e59bfb277c8c47ca1126567c7726d5ac36 |
| phase1\03_r2_domain.md | 2d43926d5763c2cd41a053aa57dc668854703b776489baaadc083d469da2cf88 |
| phase1\04_r3_practical.md | 336d19e8dd4319390456177ba7b2b958c68c23c68ca0edd32f155f43b257e48c |
| phase1\05_devils_advocate.md | f5979a5a9ccd73aeac3fecf7d619776004ea4d4bed6a7860f848128626a90c7e |
| work\panel_brief_final_filled_v01.md | 628fa08854d49cf98c8c38817ffc734de5672e1cfc584c28e431f469a0337266 |
| work\panel_provenance_final.json | 9aea0b43de4d9fd976862c3b8f40e8377a591203945e2b1bb978b06f699f70f6 |
| MANUSCRIPT_v13.md | b469bf657af9ddee583b7bda944ca3af639e1ba4b2e61875150d83bafd0f7793 |
| MANUSCRIPT_v13.tex | dd915933edffcebad863c9d1ed02b37ef0a6a493045696b210ff9c94b4dc2eee |
| SUPPLEMENT_v13.md | d1ea32fa94787a0eb44c441714ac8c9183d3ab9707c25336194673170515f9b8 |
| pages\page01.png | 2ec124efb41204b412d1667e714625f138f1f3e81cf356027968b1ea05a41a01 |
| pages\page06.png | d498a8348baa8eb92a05b5b285b04417370b260bff726903911d706a9841a242 |
| pages\page09.png | dacb57f7a4927512cf42cf0a548a7337a86c3efd791b1db0051215fdee03d984 |
| pages\page10.png | 024dcae4fac4ef28019a9c17621ff09e00a336b978d7b887d7a93918e9de469f |
| pages\page11.png | 05517641b4a60a5287681e2746b7c80fde497cae0c67fb70b940b5cd473083bd |
| AMENDMENT_13_v13.md (searched, not read in full) | bc7c2bf47c9a29810aa84c5dd4827a0f2d9404f9b684a94d0a918967180498bf |
| tj-template-s1.tex (searched for the cited lines) | 96dffaf70bff34d27b9987a59636fe37d56a079fa6a924946e2c9905a16bf873 |

Not read: the response letter, session notes, session A's diff files, earlier review rounds, `AMENDMENT_12_v13.md`, anything named <excluded folder 1> or <excluded folder 2>, the author's secrets folder. Nothing in `revision_v13\` was changed. Pages 2 to 5, 7, 8 and 12 were not opened by me.
