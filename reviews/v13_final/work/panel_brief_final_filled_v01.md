# Final v13 panel: seat brief (common part) — v01, coordinator, 22 Nov 2026 (filled at launch, 12:08 EST by Get-Date)

You are one seat of a fresh five-seat ARS pre-submission review panel for the final v13 text (after AMENDMENT_13 and the submission pass). Your seat, role card and model are named in your launch message.

## Hard rules
- Read only. Write only your one output file under `ARS_TRIAL\review_v13_final_output\phase1\`. Never change anything in `revision_v13\`.
- Never open anything named `<excluded folder 1>` or `<excluded folder 2>`, nor the author's local secrets folder. The folder `<library folder>` may be read but never changed.
- Send no manuscript text to any external service. No web access at all (no search, no page fetch, no uploads); judge format and policy against the rules stated in this brief and the template file named below. Install nothing. The laptop is shared and memory is tight: at most one light `python -I` process at a time.
- Submission gates, not findings: the repository DOI and the author's own AI-use confirmation sentence. The author block is now filled in (independent researcher, single author): check it is complete and in the template's form, but do not question the author's identity or affiliation. The title is the author's choice: comment only if a sentence of the paper contradicts it.
- Do not read: the response letter; earlier review reports (`review_v13_output\` other than your card and the field analysis, `review_v13_sprint_output\`, `review_v13_round2_output\`); other seats' files; session notes or anything in `revision_v13\work\A_text\notes\`; the diff files in `revision_v13\work\A_text\out\review_sub_input\`. Judge the paper as an editor would.
- You are not told any target score. Score the text as frozen.

## What to review (check SHA-256 at start and end; report both)
Folder: `ARS_TRIAL\revision_v13\work\A_text\out\freeze_v13_1201\` (frozen 22 Nov 2026 12:01:26 EST; 12 typeset pages; final build PASS).
- `MANUSCRIPT_v13.md` sha256 b469bf657af9ddee583b7bda944ca3af639e1ba4b2e61875150d83bafd0f7793 (read this as the paper)
- `MANUSCRIPT_v13.tex` sha256 dd915933edffcebad863c9d1ed02b37ef0a6a493045696b210ff9c94b4dc2eee (floats, captions, headings, references and front matter as typeset)
- `SUPPLEMENT_v13.md` sha256 d1ea32fa94787a0eb44c441714ac8c9183d3ab9707c25336194673170515f9b8
- `MANUSCRIPT_v13.pdf` sha256 d3fec633f7b5ab7d4d9053c2b9a56e23dbd6d5ef9c90455cd477701c0920bcf5 (not viewable here; use the page images)
- `BUILD_REPORT_v13.md` in the same folder may be read for build facts (page count, word counts).
- Figures (PNG, viewable): `ARS_TRIAL\revision_v13\work\A_text\out\figures\`
- Do NOT read `RESPONSE_TO_REVIEW_v13.md` (sha256 b87ffbbf6fce6c5f3c204096cba716c6e6c37bc7902b5ca00fcca9eca2d78c1f), `TEXT_FREEZE_v13.md`, `RECOUNT_COVERAGE_v13.md`, `DERIVED_v13.json` or `OUTCOMES_v13.json` in that folder (seat blinding), except where your seat's extra reads allow.
- Typeset pages (PNG, 1224 x 1584 px, one per page, `page01.png` to `page12.png`, viewable with the Read tool): `ARS_TRIAL\review_v13_final_output\pages\`. There is no PDF tool on this machine: use these images for every layout fact (page count, headings, captions, float placement, first-page footnote, running head, references layout).
- Template (read-only), for Q7: `ARS_TRIAL\revision_v13\work\A_text\template_ieeetj\tj-template-s1.tex` (the PDF beside it is not viewable; use the .tex).

Sections to re-point your card's focus anchors to: the whole main text, with weight on
- Section I (contributions and the self-containment sentence after Scope);
- Section IV-E (pre-registration, departures summary, recount scope);
- Section V-B (tracker variants, including the two-noise IMM);
- Section V-C (closed loop, its figure, and the equal-time-lost comparison);
- Section V-D (what the score depends on: its table and figure, now in the main text);
- Section V-E (where the covariance varies: dropouts, the replication on new runs and its dose trend, the 10 Hz configuration, the online-versus-permuted check, the coast-count control, the open-loop-matched closed loop and the equal-time-lost comparison, the nuScenes mechanism check, the real-log decision test);
- Sections VI-VII, the ACKNOWLEDGMENT and the references;
- the supplement only as far as a main-text pointer sends you there.

## How
- Use the skill `academic-research-skills:academic-paper-reviewer`, mode `full`, for your one seat only. Your Phase-0 card is in `ARS_TRIAL\review_v13_output\00_phase0_field_analysis_and_cards.md`; read only your card and the field analysis there, and re-point the card's focus anchors to the sections above. The card-confirmation pause is not held (non-interactive): say so in your header.
- Do not spawn sub-agents and do not run other seats or a synthesis.
- Name your model (not just the family) in your file's header.

## Questions every seat answers (in its own role)
1. **Labels and sizes.** Is each result reported at its true size, with its label right? "Confirmed" only for the original plan; "passed (amendment)", "failed (amendment)" or "replicated under rules fixed before the data" for amendment tests. Holm is reported beside the labels and changes none: across the six second-amendment primaries, and separately across the two third-amendment controls (the equal-time-lost closed-loop comparison and the coast-count control, both failed).
2. **Overreach.** Does any sentence claim more than its test allows? In particular: the dropout gain's source, now that a fixed coast-count margin matched it; the closed loop, matched in open-loop caution only, with the equal-time-lost comparison not shown; the nuScenes mechanism check (its primary population was chosen on the training split, disclosed; inverse over all tracks); the real-log decision test that found no room; the two-noise IMM (same position-velocity interface).
3. **Earlier limits.** The previous panel's main limits were: (a) a closed loop matched only in open-loop caution; (b) a dropout gain that might be no more than a coasting margin; (c) abstract and conclusion stronger than the body (universal "only where it varies", "where it tracks the error", "shows on real data"); (d) the two-noise IMM's interface; (e) the scope of Holm and of the second-program recount; (f) density, with the round-2 results only in the supplement. Structural limits it judged unfixable by wording: a confirmed result that could hardly fail (near-constant covariance), small positive effects, one simulator and configuration, no decision-level real-log evidence, and the process (amendments chosen after results, local hash locks, AI authorship). For each: addressed, partly addressed, or not, and what remains?
4. **Readability.** Bottom line first in the abstract; coined terms defined once; can a reader find each claim's evidence in the main text?
5. **Verdict.** Your recommendation (accept / minor / major / reject), your score out of 10 and in stars, the most likely editorial outcome at IEEE OJ-ITS, and the single change that would raise your score most.
6. **Self-contained main text.** The author's paper to another IEEE open journal was rejected because significant material sat in the supplement. Does any contribution or claim here rest on something that is only in the supplement (a result, table, figure, method step, definition or value)? List each case with the main-text location, the supplement item it rests on, and the fact to bring in. A pointer that only offers more detail is not a case.
7. **IEEE OJ-ITS format and declarations.** Check, and report every miss with its location (section, page image, or line):
   - headings in capitals (sections and subsections; subsubsections in title case), as in the template;
   - "Fig. N" in running text and "FIGURE N." in captions; Arabic table numbers ("Table 1", caption "TABLE 1."); supplement "Fig. S1", "Table S1";
   - American English (Merriam-Webster spelling) with the serial comma; periods and commas inside closing quotation marks; no contractions; one spelling of "preregistered";
   - funding in the first-page footnote; no separate Funding heading;
   - one ACKNOWLEDGMENT section holding, in order: the author-responsibility sentence; data and code availability; the AI disclosure; the competing-interests and no-human-subjects (no animals) sentence;
   - first page per the template: author, affiliation, ORCID, corresponding author with email, and a running head that carries a short title;
   - IEEE reference style (author initials, title in quotes, abbreviated venue in italics, volume, number, pages, year, DOI; arXiv as "year, arXiv:ID."; web sources with "Accessed:"; "submitted for publication" items name no journal);
   - abstract of 250 words or fewer with no abbreviations; abbreviations defined at first use in the body;
   - 3 to 5 index terms.
   Fact for Q7, from published 2026 OJ-ITS papers checked on IEEE Xplore by the author's side: running text uses "Fig. N" and captions "FIGURE N."; tables are numbered in Arabic. So "Fig. 2" in running text is correct, not a miss. Text the template itself prints and the publisher fills (the society-logo line, the "Received XX Month, XXXX" line, the DOI placeholder, "VOLUME ,", the licence line) is not a miss.
8. **AI disclosure.** IEEE's rule: the use of AI-generated content (text, figures, images, code) is disclosed in the acknowledgments section, naming the AI system used, the sections that use it, and the level of use. Does the paragraph meet the rule? Would an editor desk-reject on it? What wording lowers that risk without understating the use? (The author's own confirmation sentence is a gate: judge the rest.)
   Judge two versions and say which lowers the desk-rejection risk without understating the use, and what you would change in it:
   - **(a) as frozen:** the AI paragraph in the paper's ACKNOWLEDGMENT section (read it there);
   - **(b) a shorter candidate the author is considering** (not in the frozen text), verbatim:
     > "The author conceived the study, set its questions and plans, made every scientific decision, and reviewed and approved all content, and takes full responsibility for the work. Generative AI was used and is disclosed here under IEEE policy. Under the author's direction, Claude (Anthropic; models Opus 5.5, Fable 5.2, and Sonnet 5.5) wrote the analysis, simulation-control, and figure code, ran the literature searches, and drafted and revised the text of all sections and of the supplementary material. Separate Claude sessions that had not seen the first programs recounted every value printed in the main text and audited the claims against the result files. OpenAI Codex assisted in developing the simulation, recording, and planner software."
   Check each version's factual claims against the paper itself (for example, whether the recount scope it states matches what Section IV-E says).

## Output
`phase1\0N_<seat>.md`: header (seat, model, card, files and hashes at start and end, pages viewed, "card-confirmation pause not held"); findings as a table (ID, location, finding, severity CRITICAL / MAJOR / MINOR, evidence quoted from the text, the fix in the fewest words); then the eight answers, numbered. Final reply under 200 words: recommendation, score, top three findings, the number of Q6 and Q7 cases, your file's SHA-256.
