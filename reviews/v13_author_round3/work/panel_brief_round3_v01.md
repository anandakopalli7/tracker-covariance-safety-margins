# Third round, same seats, on the v13 package of 22 Nov 2026 22:44 EST: common seat brief, v01

Coordinator, 22 Nov 2026, 22:57 EST (Get-Date).

You are one seat of the same five-seat ARS pre-submission panel that reviewed this paper in two earlier rounds. Your launch message names your seat, card and model. The author has now:
- settled the three author-only items;
- revised the text in answer to the round-2 record.

Read the revised manuscript as a journal referee reads a revised submission:
- judge the whole text as it stands;
- give no credit for effort or for the number of rounds, and no penalty for them.

## Hard rules
- **Read only.** Write only your one output file under `ARS_TRIAL\review_v13_author_round3_output\phase1\`. Never change anything in `revision_v13\` or in any review folder.
- **Forbidden paths.** Never open anything named `<excluded folder 1>` or `<excluded folder 2>`, nor the author's local secrets folder. The folder `<library folder>` may be read but never changed.
- **No external services.** No web at all. Send no manuscript text to any external service. Install nothing. Run at most one light `python -I` process at a time; the laptop is shared.
- **The one gate.** The repository name and its DOI bracket stay open by design, because the deposit is not yet published. That is a gate, not a finding.
- **No biography.** An author biography is optional at submission; treat it as advisory at most.
- **Author's facts.** The author block, the title and the author's own statements of fact are the author's. This covers the reading of references and who made which decision. Judge whether the text states them clearly and consistently, not whether they are true. You cannot check them.
- **What you may read:**
  - the package and the page images (below);
  - your OWN round-2 report: `ARS_TRIAL\review_v13_author_round2_output\phase1\0N_<seat>_round2.md`, the one your launch message names;
  - `work\round2_record_sections_3_4.md` in this output folder: the round-2 record's sections 3 and 4, with the status of N-1 to N-20 and the nine items still required;
  - `work\letter_section_round2.md` in this output folder: the response letter's section on round 2;
  - the round-1 brief, for the review standards (Q1 to Q8): `ARS_TRIAL\review_v13_author_round_output\work\panel_brief_author_round_v01.md`;
  - your card and the field analysis in `ARS_TRIAL\review_v13_output\00_phase0_field_analysis_and_cards.md`;
  - the extra reads your launch message names.
- **What you may not read:**
  - other seats' reports from any round;
  - the other parts of any panel record or author letter;
  - the full response letter and the package manifest;
  - anything in `revision_v13\work\A_text\notes\` (claim audits, session A's reports, the author's quotes, requests);
  - `AMENDMENT_14_v13_DRAFT.md`, which the author declined;
  - `TEXT_FREEZE_v13.md`, `RECOUNT_COVERAGE_v13.md`, `DERIVED_v13.json` and `OUTCOMES_v13.json`, unless your extra reads allow them;
  - the folder `package_v13_2244_public_copy_failed\`.
- **No target score.** You are not told any target score. Score the text as it stands, on the same 10-point scale as before.

## What to review (check SHA-256 at start and end; report both)
Folder: `ARS_TRIAL\revision_v13\work\A_text\package_v13_2244\`, frozen at 22:44:09 EST on 22 Nov 2026 and identical to `out\freeze_v13_2244\`. It typesets to 14 pages with IEEE's official `ieeeoj.cls`.

| File | SHA-256 | Use |
|---|---|---|
| `MANUSCRIPT_v13.md` | 04b6ca9e2c47fb34d0f9b09f980c8e6855e37ebfd0062368649a75636d3e2eb8 | Read this as the paper. |
| `MANUSCRIPT_v13.tex` | 710a8366cb4aba07bbe8fd67084a38f217f2862cf6d8d8bfc0ebeb4c80f6df8d | Floats, captions, headings, references and front matter as typeset. |
| `SUPPLEMENT_v13.md` | e99e2d807a0884af7e53866a69a4b5f7019741e1fa75902a5cfcf56fd2545eba | The supplement. |
| `MANUSCRIPT_v13.pdf` | 93926a734b87ea1fb17117928edda98a2603d041b89afdc9521f1e8a5d650914 | Not viewable here; use the page images. |
| `SUPPLEMENT_v13.pdf` | ec81d45527801c11bd0ad4b06f91c94c44ef7c430b03235bf3ef1770f3b03f23 | Not viewable here; use the page images. |

**Build facts.** `out\freeze_v13_2244\BUILD_REPORT_v13.md` gives the word counts: abstract 235, body 8,229, whole 12,339.

**Figures.** `package_v13_2244\figures\`.

**Page images.** PNG, 1224 x 1584, under `ARS_TRIAL\review_v13_author_round3_output\`:
- `pages\page01.png` to `page14.png`;
- `pages_supplement\sup01.png` to `sup43.png`;
- `pages_template\tpl01.png` to `tpl09.png`.

Use them for every layout fact. Their hashes are in `work\pages_sha256.txt`.

**Template.** `ARS_TRIAL\revision_v13\work\A_text\template_ojits_official\unzipped\ojits-latex-template\ojits-template.tex`.

## How
- You may load the skill `academic-research-skills:academic-paper-reviewer` (re-review standards) for your one seat. Do not spawn sub-agents.
- Name your model in your header. Say "card-confirmation pause not held".

## What to do, in this order
1. **Read the revised manuscript in full,** and the supplement wherever a main-text claim rests on it. Apply the round-1 standards Q1 to Q8:
   - labels and sizes;
   - overreach;
   - readability;
   - self-containment;
   - OJ-ITS format and declarations;
   - the AI disclosure.

   Note anything that would withhold "accept as is", including anything this revision made worse or newly unclear.
2. **Mark the nine open items.** Mark each of N-1, N-5, N-20 (6) and P-1 to P-6 as resolved, partly resolved or not resolved. Quote evidence from the 22:44 text with its location.
3. **Give one judgement on the text as it stands:**
   - your recommendation: accept as is, minor revision, major revision or reject;
   - your score out of 10, and in stars;
   - the most likely editorial outcome at OJ-ITS;
   - whether you would send this text to the journal as it is, apart from the DOI (yes or no, and why).

## Output: `phase1\0N_<seat>_round3.md`
1. **Header.** Seat, model and card; files and hashes at start and end; the pages viewed; the files you read; and "card-confirmation pause not held".
2. **Judgement.** Recommendation, score and stars, the likely editorial outcome, and "send as is?" with one paragraph of reasons.
3. **The nine open items.** A table with ID, verdict, quoted evidence with location, and what remains. Give the counts.
4. **Findings, as three tables: REQUIRED-major, REQUIRED-minor and OPTIONAL.**
   - Each row gives: ID; location; finding; evidence quoted; the fix in the fewest words; and the type.
   - The types are: W wording; M a value moved in from the supplement; T text the author writes from existing records; A new analysis or new evidence.
   - Unresolved items keep their N or P number. New items get Q-1 onward.
   - A finding is REQUIRED only if you would withhold "accept as is" without it.
   - Mark anything this revision made worse with "(regression)", and mark any CRITICAL finding.
5. **Q1 to Q8, briefly.** What changed since your round-2 report.

**Final reply.** Keep it under 200 words. Give:
- your recommendation and score;
- "send as is?";
- the counts of the nine open items;
- the counts of REQUIRED-major, REQUIRED-minor and OPTIONAL findings, and how many are new (Q);
- your top three remaining REQUIRED items, with their types, or "none";
- your file's SHA-256.
