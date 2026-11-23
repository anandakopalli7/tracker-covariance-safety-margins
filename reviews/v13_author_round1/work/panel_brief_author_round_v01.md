# Author-round v13 panel: seat brief (common part), v01, coordinator, 22 Nov 2026

You are one seat of a fresh five-seat ARS pre-submission review panel for the v13 package of 22 Nov 2026, 18:30 EST. Your launch message names your seat, role card and model. Review the paper as a referee of the IEEE Open Journal of Intelligent Transportation Systems (OJ-ITS) would. The work has two phases:
- **Phase 1**: a full blind review.
- **Phase 2**: a check of an earlier panel's required items. Do it only after Phase 1 is written and hashed.

## Hard rules
- **Read only.** Write only your two output files under `ARS_TRIAL\review_v13_author_round_output\` (named below). Never change anything in `revision_v13\` or in any other review folder.
- **Forbidden paths.** Never open anything named `<excluded folder 1>` or `<excluded folder 2>`, nor the author's local secrets folder. The folder `<library folder>` may be read but never changed.
- **No external services.**
  - Send no manuscript text to any external service.
  - No web access at all: no search, no page fetch, no uploads.
  - Judge format and policy against the rules stated in this brief and the template named below.
- **Laptop limits.** Install nothing. The laptop is shared and memory is tight: run at most one light `python -I` process at a time.
- **Gates, not findings.** One placeholder is a submission gate, not a finding: the repository name and its DOI (the deposit is being assembled).
  - The author block is filled in (independent researcher, single author). Check that it is complete and in the template's form, but do not question the author's identity or affiliation.
  - The ACKNOWLEDGMENT's first paragraph was written by the author. Judge it like any other text (Q8).
  - The title is the author's choice. Comment on it only if a sentence of the paper contradicts it.
- **Blinding.** Do not read any of these:
  - the response letter (`RESPONSE_TO_REVIEW_v13.*`);
  - the package manifest;
  - earlier review reports or panels: `review_v13_final_output\`, `review_v13_round2_output\`, `review_v13_sprint_output\`, and `review_v13_output\` other than your card and the field analysis;
  - other seats' files in this panel;
  - session notes, or anything in `revision_v13\work\A_text\notes\`;
  - the diff files in `revision_v13\work\A_text\out\review_sub_input\`;
  - `TEXT_FREEZE_v13.md`, `RECOUNT_COVERAGE_v13.md`, `DERIVED_v13.json` or `OUTCOMES_v13.json`, unless your seat's extra reads allow them.

  The one exception is the Phase 2 file named below, and only in Phase 2.
- **Scoring.** You are not told any target score. Score the text as it stands. Do not raise a score because something looks fixed, and do not lower one to look strict.

## What to review (check SHA-256 at start and end; report both)
Folder: `ARS_TRIAL\revision_v13\work\A_text\package_v13_1830\`. It was frozen at 18:30:33 EST on 22 Nov 2026 and is identical to `out\freeze_v13_1830\`. It typesets to 13 pages with IEEE's official `ieeeoj.cls`.

| File | SHA-256 | Use |
|---|---|---|
| `MANUSCRIPT_v13.md` | 29125167b108bc27833c16e3b639cbb07af5f4c105c49d375deff3d5b4a951d0 | Read this as the paper. |
| `MANUSCRIPT_v13.tex` | bd4d08d954d3595de2b5ac2653c18476c7bb3281e1c264604f995f018da01345 | Floats, captions, headings, references and front matter as typeset. |
| `SUPPLEMENT_v13.md` | fab98c1fe24c8c5b95f86da8b1e664662401055232409a236d963938f5b99a09 | The supplement, which typesets to a 43-page PDF. |
| `MANUSCRIPT_v13.pdf` | 4fabfd9f611013fd4e7f60b8a59fcdcc2d782dbd3192a77c2efe54e77beb8299 | Not viewable here; use the page images. |
| `SUPPLEMENT_v13.pdf` | a8ad36027dee70c8c48cf2b998cb2512b55ca568c400eb1ecd340923ddeb8b16 | Not viewable here; use its first pages as images. |

**Build facts.** `out\freeze_v13_1830\BUILD_REPORT_v13.md` gives the page count and the word counts.

**Figures.** The figure files (PNG, viewable) are in `package_v13_1830\figures\`.

**Page images.** These are PNG files you can open with the Read tool. There is no PDF tool on this machine, so use them for every layout fact: page count, headings, captions, float placement, first page, running head and reference layout.
- `ARS_TRIAL\review_v13_author_round_output\pages\`: the manuscript, `page01.png` to `page13.png`.
- `pages_supplement\`: the supplement's first pages, `sup01.png` onward.
- `pages_template\`: the official template PDF, `tpl01.png` onward.
- If a folder is empty when you start, say so in your header and judge layout from the .tex.
- The SHA-256 of every image is in `work\pages_sha256.txt` once the images are in.

**Template.** The official template is read-only and is the reference for Q7: `ARS_TRIAL\revision_v13\work\A_text\template_ojits_official\unzipped\ojits-latex-template\ojits-template.tex`. It has 938 lines; cite its line numbers. The `ojits-template.pdf` beside it is seen through `pages_template\`.

**Weight.** Review the whole main text. Give extra weight to:
- Section I: the contributions, Scope and the self-containment sentence.
- Section III: the test beds, including the pedestrian crossing, the closed loop and the margin sources.
- Sections IV-B and IV-E: the room, the share, time lost and rest gap, pre-registration, the amendments, Holm and the recount scope.
- Section V-B: the tracker variants, including the two-noise IMM.
- Section V-C: the closed loop, its figure and the equal-time-lost comparison.
- Section V-D: what the score depends on, with its table and figure.
- Section V-E, where the covariance varies:
  - dropouts and the coast-count control;
  - the replication on new runs and its dose trend;
  - the 10 Hz configuration;
  - the online-versus-permuted check;
  - the open-loop-matched closed loop;
  - the nuScenes mechanism check;
  - the real-log decision test.
- Sections VI and VII, the ACKNOWLEDGMENT and the references.
- The supplement, as far as a main-text pointer sends you there, and for Q6.

## How
- Use the skill `academic-research-skills:academic-paper-reviewer`, mode `full`, for your one seat only.
- Your Phase-0 card is in `ARS_TRIAL\review_v13_output\00_phase0_field_analysis_and_cards.md`. Read only your card and the field analysis there, and re-point the card's focus anchors to the sections above.
- The card-confirmation pause is not held, because the run is non-interactive. Say so in your header.
- Do not spawn sub-agents, and do not run other seats or a synthesis.
- Name your model, not just the family, in the header of each file.

## Phase 1: questions every seat answers in its own role
1. **Labels and sizes.** Is each result reported at its true size, with the right label?
   - "Confirmed" is only for the original plan.
   - Amendment tests take "passed (amendment)", "failed (amendment)" or "replicated under rules fixed before the data".
   - Holm is reported beside the labels and changes none of them. It runs across the six second-amendment primaries, and separately across the two third-amendment controls: the equal-time-lost closed-loop comparison and the coast-count control, both failed.
2. **Overreach.** Does any sentence claim more than its test allows? Look in particular at:
   - the dropout gain's source, now that a fixed coast-count margin matched it;
   - the closed loop, which was matched in open-loop caution only, with the equal-time-lost comparison not shown;
   - the nuScenes mechanism check: its primary population was chosen on the training split (disclosed), and the relation is inverse over all tracks;
   - the real-log decision test, which found no room;
   - the two-noise IMM, which has the same position-velocity interface;
   - the scope of the null result: which prediction model, and which planner.
3. **Earlier limits.** A previous panel named these main limits:
   - (a) a closed loop matched only in open-loop caution;
   - (b) a dropout gain that might be no more than a coasting margin;
   - (c) an abstract and conclusion stronger than the body ("only where it varies", "where it tracks the error", "shows on real data");
   - (d) the two-noise IMM's interface;
   - (e) the scope of Holm and of the second-program recount;
   - (f) density, with the round-2 results only in the supplement.

   It also named structural limits it judged unfixable by wording:
   - a confirmed result that could hardly fail (a near-constant covariance);
   - small positive effects;
   - one simulator and one configuration;
   - no decision-level real-log evidence;
   - the process: amendments chosen after results, local hash locks, AI authorship.

   For each, say whether it is addressed, partly addressed or not, and what remains.
4. **Readability.** Does the abstract put the bottom line first? Is each coined term defined once? Can a reader find each claim's evidence in the main text?
5. **Verdict.** Give:
   - your recommendation, one of: accept as is, minor revision, major revision, reject;
   - your score out of 10 and in stars (out of 5);
   - the most likely editorial outcome at OJ-ITS;
   - the single change that would raise your score most.
6. **Self-contained main text.** The author's paper to another IEEE open journal was rejected because significant material sat in the supplement.
   - Does any contribution or claim here rest on something that is only in the supplement: a result, table, figure, method step, definition or value?
   - List each case with its main-text location, the supplement item it rests on, and the fact to bring in.
   - A pointer that only offers more detail is not a case.
7. **IEEE OJ-ITS format and declarations.** Check each item below. Report every miss with its location (section, page image or line), and cite the template line where it applies.
   - Headings are in capitals for sections and subsections, and in title case for subsubsections, as in the template.
   - Running text says "Fig. N" and captions say "FIGURE N.". Tables use Arabic numbers: "Table 1" in text, "TABLE 1." in the caption. The supplement uses "Fig. S1" and "Table S1".
   - The spelling is American English (Merriam-Webster) with the serial comma. Periods and commas go inside closing quotation marks. There are no contractions, and "preregistered" has one spelling throughout.
   - Prefixes follow the template's hyphenation rule.
   - Funding is in the first-page footnote, with no separate Funding heading.
   - There is one ACKNOWLEDGMENT section. It holds, in order:
     1. the author-responsibility statement;
     2. data and code availability;
     3. the AI disclosure;
     4. the competing-interests sentence and the no-human-subjects (no animals) sentence.
   - The first page follows the template: author, affiliation, ORCID, corresponding author with email, and a running head that carries a short title.
   - References follow IEEE style:
     - author initials;
     - the title in quotes;
     - the venue abbreviated and in italics;
     - volume, number, pages, year and DOI;
     - arXiv as "year, arXiv:ID.";
     - web sources with "Accessed:";
     - "submitted for publication" items name no journal.
   - Figures and tables follow the template: sub-figure labels, caption placement, legible axis labels, and tables that fit the column.
   - The abstract has 250 words or fewer and no abbreviations. Each abbreviation is defined at its first use in the body.
   - There are 3 to 5 index terms.

   Facts for Q7, so they are not counted as misses:
   - The author's side checked published 2026 OJ-ITS papers on IEEE Xplore. Running text there uses "Fig. N", captions use "FIGURE N.", and tables are numbered in Arabic. So "Fig. 2" in running text is correct.
   - The template prints some text that the publisher fills in: the society-logo line, the "Received XX Month, XXXX" line, the DOI placeholder, "VOLUME ,", and the licence line. None of it is a miss.
   - The repository and DOI placeholder is a gate, not a miss.
   - There is no author biography yet. It is optional at submission, so treat it as advisory at most.
8. **AI disclosure.** IEEE's rule: the use of AI-generated content (text, figures, images, code) is disclosed in the acknowledgments section, naming the AI system used, the sections that use it, and the level of use.
   - Does the paragraph in the ACKNOWLEDGMENT meet that rule?
   - Would an editor desk-reject on it?
   - Check every factual claim it makes against the paper itself. Where your seat has extra reads, check them against those records too.
   - Say what wording, if any, would lower the risk without understating the use.

## Phase 1 output
Write `phase1\0N_<seat>.md`, in this order:
1. **Header.** Give your seat, model and card; the files and their hashes at start and end; the pages viewed; and "card-confirmation pause not held".
2. **Recommendation and score.** Give your recommendation (accept as is, minor revision, major revision or reject) and your score out of 10 and in stars.
3. **Findings, as three tables.**
   - The tables are **REQUIRED-major**, **REQUIRED-minor** and **OPTIONAL**.
   - Each row gives: ID; location; finding; evidence quoted from the text; the fix in the fewest words; and the type.
   - The types are: **W** wording; **M** a value moved in from the supplement (name it); **T** text the author writes from existing records; **A** new analysis or new evidence.
   - A finding is REQUIRED only if you would withhold "accept" without it.
   - Mark any CRITICAL finding, meaning one that alone justifies rejection.
4. **The eight answers**, numbered.

When the file is complete, compute its SHA-256 (`certutil -hashfile <file> SHA256` or `python -I -c` with hashlib). Write that value into the first line of your Phase 2 file. Do not change the Phase 1 file after this point.

## Phase 2: the earlier panel's required items, after Phase 1 only
- **Source.** Open `ARS_TRIAL\review_v13_author_round_output\work\earlier_required_R1_R19_and_Q7.md`. It holds the REQUIRED items R-1 to R-19 of a panel on an earlier text of this paper, the 12:01 freeze of 12 pages, together with that panel's Q7 list, which R-19 refers to.
- **Verdicts.** For each of R-1 to R-19, decide whether it is **resolved**, **partly resolved** or **not resolved** in the 18:30 text. Give the evidence quoted from the 18:30 text, with its location, and in one line what remains, if anything.
  - For R-19, go through Q7-1 to Q7-19 one by one.
  - Where an earlier item asked for something you think is wrong or unnecessary, say so.
- **Output.** Write `phase2_r_check\0N_<seat>_r_check.md`. Its first line gives your Phase 1 file's SHA-256. It needs a table with ID, verdict, evidence and what remains, then the counts (resolved, partly, not).
- **No changes to Phase 1.** Do not change your Phase 1 report, recommendation or score after reading the earlier items. If the earlier list shows you missed something, note it in Phase 2 under "noted after Phase 1" and leave Phase 1 as it is.

## Final reply
Keep it under 200 words. Give:
- your recommendation and score;
- your top three REQUIRED findings, with their types;
- the counts of REQUIRED-major, REQUIRED-minor and OPTIONAL findings;
- the number of Q6 cases and of Q7 misses;
- the Phase 2 counts (resolved, partly, not);
- both files' SHA-256.
