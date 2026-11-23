# Author-round v13 panel: seat launch messages, v01 (coordinator, 22 Nov 2026, 18:38 EST by Get-Date)

| Item | Path | SHA-256 |
|---|---|---|
| Brief ({BRIEF}) | ARS_TRIAL\review_v13_author_round_output\work\panel_brief_author_round_v01.md | 47198b07517f3ac881f51c2768e0e71162814536952eef5033b647528d80feab |
| Cards | ARS_TRIAL\review_v13_output\00_phase0_field_analysis_and_cards.md | |
| Writers | Opus 5.5 for the early text; Claude Fable 5.2 (session A) for round 2, the submission pass, the fix round and the format pass; the author for the full name and the ACKNOWLEDGMENT's first paragraph | |

Every seat message below starts with the line "You are seat X ... Your model is Y." and then gives these steps:
1. Read the common brief in full and follow it: {BRIEF}. It has two phases: Phase 1 is a blind review, and Phase 2 is the earlier items, done only after Phase 1 is hashed.
2. Read your card (named per seat) and the field analysis in the cards file, and nothing else in review_v13_output. Re-point the card's focus anchors to the sections the brief names.
3. Seat-specific duties and extra reads (below).
4. You may load the skill academic-research-skills:academic-paper-reviewer for its review standards. Run ONLY your one seat: do not spawn sub-agents, and do not run other seats or a synthesis.
5. Outputs: phase1\0N_<seat>.md and phase2_r_check\0N_<seat>_r_check.md under ARS_TRIAL\review_v13_author_round_output\.

Final reply: as the brief says (under 200 words).

## EIC (sonnet)
- **Card:** "Card 1: Journal-Fit Reviewer (internal role EIC)".
- **Q7, in full.** Open every manuscript page image (page01 to page13), every template page image (tpl01 to tpl09) and the supplement's first pages (sup01 to sup03). Check every Q7 item against ojits-template.tex, citing its line numbers.
- **Q8, in depth.** Would an OJ-ITS editor desk-reject on the AI paragraph? Check its factual claims against the paper.
- **Extra reads:** none.

## R1 (fable)
- **Card:** "Card 2: Peer Reviewer 1 (Methodology)".
- **Writer note.** Later parts of this text were written by your own model, Claude Fable 5.2. Be deliberately skeptical.
- **Extra reads, read-only:**
  - AMENDMENT_10 to AMENDMENT_13_v13.md;
  - LOCK_A11/b/c, LOCK_A12a to e and LOCK_A13a to c in revision_v13\;
  - any A_EXPORT_* / A_RECOUNT_* pair under revision_v13\work\ (B_retrack\out, CD_capture\out, E_closedloop\out, F_nuscenes\out, F_dropout\out);
  - work\shared\holm\A12_HOLM_v01.json and A13_HOLM_v01.json;
  - RECOUNT_COVERAGE_v13.md in out\freeze_v13_1830\.
- **Spot-check at least 40 printed values** and report how many match. Include every value in:
  - Table 5 and Table 6;
  - the Fig. 3 and Fig. 4 captions;
  - V-E's paragraphs on dropouts, the coast-count control, the equal-time-lost comparison and the nuScenes mechanism;
  - the abstract.

  For each value, say whether it has an agreeing second-program recount or is marked one-program.
- **Recount statements.** Check the paper's recount-scope statements (Section IV-E and the ACKNOWLEDGMENT) against RECOUNT_COVERAGE.
- **Q6 from the methods side.** Give Q6 full attention: any method step, definition or value that a main-text claim needs and that is only in the supplement.

## R2 (opus)
- **Card:** "Card 3: Peer Reviewer 2 (Domain)".
- **Writer note.** Much of the earlier text was written by your own model, Claude Opus 5.5. Be deliberately skeptical.
- **Give particular attention to:**
  - what the failed coast-count control leaves of the dropout result;
  - whether the closed-loop result is stated as what it is;
  - the two-noise IMM's interface;
  - the null's scope (prediction model and planner);
  - whether the related work places the paper fairly against misdetection-aware planning, intermittent-observation filtering, data-dependent covariances and ITS threat assessment.
- **References.** Any reference you suggest is from memory: mark it "unverified".
- **Extra reads:** none.

## R3 (sonnet)
- **Card:** "Card 4: Peer Reviewer 3 (Cross-disciplinary / Practical)".
- **Give particular attention to:**
  - whether a safety engineer could act on the conclusions without over-reading them;
  - the closed-loop cost: time lost, and who bears it.
- **Second Q7 pass**, independent of EIC, on:
  - the first page: author, affiliation, ORCID, corresponding author, funding note and running head;
  - the ACKNOWLEDGMENT and its order;
  - the abstract: word count and no abbreviations;
  - the index terms;
  - every reference against IEEE style.

  Open the page images for the first page, the back matter and the reference pages, and the template images.
- **Extra reads:** none.

## DA (fable)
- **Card:** none; the Devil's Advocate is a fixed seat.
- **Writer note.** Later parts of this text were written by your own model, Claude Fable 5.2. Be deliberately skeptical.
- **Job.** Find the strongest case against publishing this paper as written:
  - the claim most likely to be wrong or over-read;
  - the analysis choice most open to a forking-paths objection;
  - the reasons an editor would desk-reject, including on the AI disclosure (Q8), on material left in the supplement (Q6) and on format (Q7);
  - what a hostile but fair reviewer would write first.

  Then judge honestly how much of that case survives the paper's own disclosures.
- **Extra reads, read-only:** AMENDMENT_11, AMENDMENT_12 and AMENDMENT_13_v13.md, to judge what was fixed before the data and what was chosen after.
