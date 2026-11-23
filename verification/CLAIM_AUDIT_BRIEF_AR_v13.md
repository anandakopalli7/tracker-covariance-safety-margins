# Brief: claim audit of the changes made after the review of the author round

For a fresh agent on **Claude Sonnet 5.5**. The changed text was written by Claude Fable 5.2, so the auditor must be another model. Prepared 22 Nov 2026, 20:24 EST (computer clock), by session A, at the request of the author-facing session (its message of 20:10). The text is frozen (20:16:34) and `out\audit_ar_input\` is filled.

**Why this audit.** A panel of five reviewed the 18:30 text and asked for twenty items (N-1 to N-20). The fix round moved many facts from the supplement into the main text, rewrote the abstract, extended three tables, and split Section V-E into five parts. Such a round can open as many gaps as it closes. Your job is to find them before the next panel reads the text.

## Rules for you
- Write only your output file. Do not edit any other file, and do not run builds.
- No web or external service; send no text anywhere.
- Do **not** read the generator code in `work\A_text\gen\` or `work\A_text\build\` (one exception: the data file `gen\model_record_v13.json`). Judge the text against the plans and the result files.
- Never open anything named `<excluded folder 1>` or `<excluded folder 2>`, nor any folder whose name contains `local_secrets`.
- The laptop is shared and its memory is tight: read files, and run at most one light Python process at a time (`python -I`). Do not search whole folder trees.
- Do not run any program under `work\shared\holm_recount\`: as written, each rewrites its record file.
- Take every clock time from the computer (`Get-Date`), not from memory.

## Inputs
All paths are under `ARS_TRIAL\`.
- **The new text:** `revision_v13\work\A_text\out\audit_ar_input\`
  - `MANUSCRIPT_v13.md`, `SUPPLEMENT_v13.md`, `RESPONSE_TO_REVIEW_v13.md` (and `MANUSCRIPT_v13.tex`, `.pdf`);
  - `OUTCOMES_v13.json` (statuses);
  - `DERIVED_v13.json`: each printed value with its export key, its source file, the second program's value (`recount`), whether the two agree (`recount_agrees`), and whether only one program computed it (`one_program`);
  - `BUILD_REPORT_v13.md` (counts against the limits; its "Inputs" line lists the first programs' export files; the second program's file has `RECOUNT` for `EXPORT` in its name), `RECOUNT_COVERAGE_v13.md`.
- **What changed** against the 18:30 freeze, which the panel read: `DIFF_SINCE_1830_MANUSCRIPT_v13.txt`, `DIFF_SINCE_1830_SUPPLEMENT_v13.txt`, `DIFF_SINCE_1830_RESPONSE_TO_REVIEW_v13.txt` in the same folder. The old text is in `revision_v13\work\A_text\out\freeze_v13_1830\`. Lines are whole paragraphs, so compare at sentence level yourself.
- **What asked for the changes:**
  - the panel record `review_v13_author_round_output\ARS_REVIEW_AUTHOR_ROUND_v01.md`: section 5 (N-1 to N-20), section 7 (the facts the main text lacked, case by case), section 8 (format), section 10 (the Acknowledgment ruling);
  - the fix brief `revision_v13\work\A_text\notes\FIX_ROUND_AUTHOR_REVIEW_BRIEF_v13.md`;
  - the author's own statement on AI use: `revision_v13\work\A_text\notes\AUTHOR_ROUND_BRIEF_v13.md`, section 3.
- **The writer's account of the fixes:** `revision_v13\work\A_text\notes\FIX_ROUND_AUTHOR_REVIEW_REPORT_v13.md`: section 2 (N-1 to N-20 with status and place), section 3 (the section-7 cases), section 4 (values newly printed in the main text, with their export keys), section 7 (two late additions). Treat it as a claim to test, not as evidence.
- **The plans:** `revision_v13\PLAN_v13.md`, `AMENDMENT_10_v13.md`, `AMENDMENT_11_v13.md`, `AMENDMENT_12_v13.md`, `AMENDMENT_13_v13.md` (all in `revision_v13\`). Label rules: `AMENDMENT_10_v13.md` section 9; `AMENDMENT_11_v13.md` section 3.8; `AMENDMENT_12_v13.md` section 1 (labels), section 4 (Holm), section 6 (closed loop); `AMENDMENT_13_v13.md` section 2 (its head note gives the pass rule of the closed-loop frontier test) and section 3.
- **The last audit before this one**, for the regression check: `revision_v13\work\A_text\notes\CLAIM_AUDIT_v13_fix_final_v01.md` (Check 1 lists where each of R-1 to R-19 stood).

## Scope (stop rule)
Audit every sentence, table cell, table note, and caption that the three difference files show as new or changed, and an unchanged sentence only where a change elsewhere makes it wrong. In the manuscript this covers at least: the abstract; Section I (contribution 2, the paragraph that says what the main text holds, the data paragraph); Section II (the sentence on intermittent observations); the changed sentences of Sections III and IV; Table 2 with its three new rows and its notes; Section V-C and Table 4 with its three new columns and its note; Section V-D; Section V-E with its five headed parts; Table 6 with its new and renamed rows and its note; Sections VI and VII; the Acknowledgment's four paragraphs. In the supplement: S12's paragraphs on second programs, the claim audit, and the presubmission reviews; the two new rows of the order-of-work table; the changed rows of the departures table. In the letter: rows S6 and S13, the section on the review of the author round, and the paragraph on what waits for the author.

Three items wait for the author and must be **unchanged**: N-1 (the Acknowledgment's first sentence), N-5 (the author's reading of the closest references), N-20 part 6 (the surname form in one reference). Confirm that, and do not rate them. Do not judge what a cited paper says.

## The six checks
1. **Each changed claim against the plans and the result files.**
   - Every number matches its source at the printed rounding, with the interval and level the text states. Look values up in `DERIVED_v13.json` by text or key, and open the export and recount files for at least every value that section 4 of the writer's report lists as newly printed in the main text.
   - **Two-program rule.** Every result value in the main text and in the letter must have an agreeing second program. No value that only one program computed (marked ‡ in the supplement) may appear in the main text or the letter as a number; where the main text mentions such a result, it must do so in words and say that one program computed it.
   - Labels: "confirmed" only for the original plan; "passed (amendment)" or "failed (amendment)" for amendment tests; "replicated under rules fixed before the data"; "secondary", "descriptive", "exploratory", and "post hoc" where the plans require them.
   - No claim beyond its rule; no numbers from two run sets paired in one sentence without naming both sets; every pointer (section, table, figure, supplement section, table note letter) goes to a place that holds what it says.
2. **The summary test (the panel's N-3).** Take each summary sentence: every sentence of the abstract; Section I's contribution list and its paragraph for a designer; the opening of Section VI; Section VII. For each, find the body passage or table cell that supports it and compare: (i) the size (the number, or the size word such as "rarely", "by little", "about 5%", "slightly"); (ii) the status label the body gives that result; (iii) the conditions the body attaches (run set, planner, interface, update rate, speed range, start probability); (iv) whether the summary leaves out a counter-case that the body reports. Give one table row per summary sentence. Item N-3 in the record lists the parts the panel asked for; check each part.
3. **Each required item is fixed as the letter says.** The letter's section on the review of the author round maps each of N-1 to N-20 to a change. For each row: is the change in the text, and does it do what the item asked? Quote the new text. Section 7 of the record lists the facts that the main text lacked; for each case say whether the fact is now in the main text with its number and its label.
4. **Consistency inside the new text.** The same quantity printed in two places must agree (abstract, body, tables, Section VII, supplement, letter). Table 2's new rows, Table 4's new columns (units, and which arm and caution level each cell belongs to), and Table 6's new and renamed rows must agree with the prose that cites them. Each of the five headings of Section V-E must hold what its heading says and nothing that belongs under another. Names of run sets, arms, and margins must be used the same way throughout the changed passages.
5. **The Acknowledgment and Supplement S12 against the records.** The author's sentences must be word for word those of the author's statement (first sentence untouched). Every statement about which system or model did what must be supported by a record: `gen\model_record_v13.json`; the model lines of the amendments (`AMENDMENT_11_v13.md` section 10, `AMENDMENT_12_v13.md` section 8); the first lines of the audit reports `notes\CLAIM_AUDIT_v13_*.md`; the two Holm result files in `work\shared\holm_recount\`; the provenance files in the folders `review_v1*_output\` at the top level. S12's counts (audits per model, review rounds) must match the files. S12 says that the changes after the review of the author round "have had no separate claim audit": that sentence will be replaced once your audit is done, so do not rate it; say what an accurate replacement must state.
6. **Nothing has regressed, and the gates hold.** Each of R-1 to R-19 of the earlier panel must survive in the new text; one line each. `BUILD_REPORT_v13.md` must say PASS with: abstract at most 245 by the build's count; body at most 8,253; whole text at most 12,342; supplement at most 21,500. Count the abstract's words yourself, with a hyphenated compound as one word and each number as one word; the limit by that count is 250.

Rate each finding **H** (a wrong number, a value without an agreeing second program in the main text or letter, or a claim beyond its rule), **M** (a missing required label or condition, a summary sentence that does not carry the body's size or status, a required item not fixed, or a regression) or **L** (clarity or wording).

## Output
`revision_v13\work\A_text\notes\CLAIM_AUDIT_v13_ar_v01.md`, containing:
- which model you are; the SHA-256 of the three input texts at the start and at the end; what you read and what you did not open;
- check 2's table: one row per summary sentence, with the supporting passage and a verdict;
- check 3's table: one row per item N-1 to N-20 (done / done in part / not done / waits for the author, unchanged), with the quoted new text, and one row per case of the record's section 7;
- the number check: how many values you looked up, how many matched, and each mismatch;
- findings, numbered, rated H, M or L, each with its place, the quoted sentence, the source that contradicts or fails to support it, and the fix in the fewest words;
- the regression check, one line per R-1 to R-19;
- the gates, with your own count of the abstract;
- a verdict in two or three sentences.

Keep fixes word-neutral where you can: the manuscript is at its limit of 14 typeset pages, the body has 2 words of room and the whole text 28. For any words you add, say what could be cut.
