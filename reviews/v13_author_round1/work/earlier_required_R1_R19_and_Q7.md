# Earlier REQUIRED items R-1 to R-19 and the Q7 list, from the 12:01 panel (review_v13_final_output\ARS_REVIEW_FINAL_v01.md, sections 4 and 7, copied verbatim by the coordinator)

Open this file only AFTER your own blind report is written and its SHA-256 recorded. Locations refer to the 12:01 text (12 pages); find each item's place in the 18:30 text yourself.

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

