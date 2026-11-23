# Second round, same seats, on the v13 package of 22 Nov 2026 21:15 EST: common seat brief, v01

Coordinator, 22 Nov 2026, 21:24 EST (Get-Date).

You are one seat of the same five-seat ARS pre-submission panel that reviewed the 18:30 text of this paper. Your launch message names your seat, card and model. The author revised the paper in answer to the panel's record. Read the revised manuscript as a journal referee reads a revised submission:
- judge the whole text as it stands now, not only the changed places;
- give no credit for effort;
- give no penalty for this being a second round.

## Hard rules
- **Read only.** Write only your one output file under `ARS_TRIAL\review_v13_author_round2_output\phase1\`. Never change anything in `revision_v13\` or in any review folder.
- **Forbidden paths.** Never open anything named `<excluded folder 1>` or `<excluded folder 2>`, nor the author's local secrets folder. The folder `<library folder>` may be read but never changed.
- **No external services.** No web at all: no search, no page fetch, no uploads. Send no manuscript text to any external service. Install nothing. Run at most one light `python -I` process at a time; the laptop is shared.
- **Gates, not findings:**
  - the repository name and DOI bracket (the deposit is assembled but not yet published);
  - the three author-only items N-1, N-5 and N-20 (6), which are untouched because the author has not answered yet. Mark them "not resolved", and treat them as judgement (b) below describes.

  The title is the author's choice. Do not question the author's identity or affiliation.
- **What you may read:**
  - the package and the page images (below);
  - your OWN round-1 report;
  - `work\round1_record_sections_5_7_8.md` in this output folder: the panel record's sections 5, 7 and 8, with N-1 to N-20, the self-containment cases and the format list;
  - `work\letter_section_author_round.md` in this output folder: the response letter's section answering N-1 to N-20;
  - the round-1 brief, for the review standards: `ARS_TRIAL\review_v13_author_round_output\work\panel_brief_author_round_v01.md`;
  - your card in `ARS_TRIAL\review_v13_output\00_phase0_field_analysis_and_cards.md`, with only your card and the field analysis;
  - the extra reads your launch message names.
- **What you may not read:**
  - other seats' reports from either round;
  - any other part of the round-1 record (`ARS_REVIEW_AUTHOR_ROUND_v01.md`) or of its author letter;
  - the round-1 Phase 2 files of other seats;
  - the full response letter (`RESPONSE_TO_REVIEW_v13.*`) and the package manifest;
  - anything in `revision_v13\work\A_text\notes\`: claim audits, session A's reports, requests and briefs;
  - `revision_v13\AMENDMENT_14_v13_DRAFT.md`, which is not part of this text;
  - `TEXT_FREEZE_v13.md`, `RECOUNT_COVERAGE_v13.md`, `DERIVED_v13.json` and `OUTCOMES_v13.json`, unless your extra reads allow them;
  - earlier review folders, other than your own round-1 report and the round-1 brief.
- **No target score.** You are not told any target score. Score the text as it stands, on the same 10-point scale as round 1.

## What to review (check SHA-256 at start and end; report both)
Folder: `ARS_TRIAL\revision_v13\work\A_text\package_v13_2115\`. It was frozen at 21:15:53 EST on 22 Nov 2026 and is identical to `out\freeze_v13_2115\`. It typesets to 14 pages with IEEE's official `ieeeoj.cls`.

| File | SHA-256 | Use |
|---|---|---|
| `MANUSCRIPT_v13.md` | c440adca7a70b2b74a373ee3a135d3eeac2c44a35ee6e28cb1c7280893d771b7 | Read this as the paper. |
| `MANUSCRIPT_v13.tex` | 8e9e648ef0290856f5c0dbdb841ebb2ecf0dea57cca6b8e2cc81749e856386ac | Floats, captions, headings, references and front matter as typeset. |
| `SUPPLEMENT_v13.md` | d18eee97e3f02f08159b1aaf81311a2663870818a42268dba706a1ba24d31b2b | The supplement. |
| `MANUSCRIPT_v13.pdf` | dc83ce17a652e734399f84005631649fe3801b936a589499a9ed1f0f68a51ccb | Not viewable here; use the page images. |
| `SUPPLEMENT_v13.pdf` | 084091af1a419f0bff64b643da112a70133ad382d2e51c929fb077ceee8e5692 | Not viewable here; use the page images. |

**Build facts.** `out\freeze_v13_2115\BUILD_REPORT_v13.md` gives the word counts.

**Figures.** In `package_v13_2115\figures\`.

**Page images.** PNG, 1224 x 1584, under `ARS_TRIAL\review_v13_author_round2_output\`:
- `pages\page01.png` to `page14.png`: the manuscript;
- `pages_supplement\sup01.png` to `sup43.png`: the supplement, all pages;
- `pages_template\tpl01.png` to `tpl09.png`: the official template.

Use them for every layout fact. Their hashes are in `work\pages_sha256.txt`.

**Template.** `ARS_TRIAL\revision_v13\work\A_text\template_ojits_official\unzipped\ojits-latex-template\ojits-template.tex`. Cite its line numbers.

## How
- You may load the skill `academic-research-skills:academic-paper-reviewer` (re-review standards) for your one seat. Do not spawn sub-agents, and do not run other seats or a synthesis.
- Name your model, not just the family, in your header. Say "card-confirmation pause not held".

## What to do, in this order
1. **Read the revised manuscript in full,** and the supplement wherever a main-text claim rests on it. Apply the round-1 standards (questions Q1 to Q8 of the round-1 brief):
   - labels and sizes;
   - overreach;
   - readability;
   - self-containment;
   - OJ-ITS format and declarations;
   - the AI disclosure.

   Note anything that would now withhold "accept", including anything the revision made worse or newly unclear. Comment on length and density at 14 pages; the body has 8,253 words by the project's counter.
2. **Mark each of N-1 to N-20** resolved, partly resolved or not resolved. Quote evidence from the 21:15 text with its location. For N-20, go through its six parts. N-1, N-5 and N-20 (6) are expected to be "not resolved", because they wait for the author.
3. **Give two judgements, on the same scale.**
   - **(a) The text as it stands:** recommendation (accept as is, minor revision, major revision or reject), score out of 10, and stars.
   - **(b) CONDITIONAL, labeled as such:** the same three things, assuming:
     - N-1's sentence reads "made or approved every scientific decision";
     - the author reports, in the paper, having read the closest references in full, with the sentence the record proposes: how many were read in full, how many at abstract level, and that every reference was checked against its publisher or Crossref record;
     - reference [10] carries the byline's surname.

     Assume these are true. Change nothing else.

## Output: `phase1\0N_<seat>_round2.md`
1. **Header.** Seat, model and card; files and hashes at start and end; the pages viewed; the files you read under "what you may read"; and "card-confirmation pause not held".
2. **Judgements (a) and (b).** Recommendation, score out of 10 and stars for each, with one paragraph on what separates them.
3. **N-1 to N-20 table.** ID, verdict, evidence (quoted, with location) and what remains. Give counts of resolved, partly and not.
4. **Findings, as three tables: REQUIRED-major, REQUIRED-minor and OPTIONAL.**
   - Each row gives: ID; location; finding; evidence quoted; the fix in the fewest words; and the type.
   - The types are: W wording; M a value moved in from the supplement; T text the author writes from existing records; A new analysis or new evidence.
   - Unresolved round-1 items keep their N number. New items get P-1 onward.
   - A finding is REQUIRED only if you would withhold "accept" without it.
   - Mark anything the revision made worse with "(regression)".
   - Mark any CRITICAL finding.
5. **Q1 to Q8, briefly.** For each, what changed since your round-1 report, plus a paragraph on length and density.

**Final reply.** Keep it under 200 words. Give:
- (a) and (b): recommendation and score;
- the N-1 to N-20 counts;
- the counts of REQUIRED-major, REQUIRED-minor and OPTIONAL findings, and how many are new (P);
- your top three remaining REQUIRED items, with their types;
- your file's SHA-256.
