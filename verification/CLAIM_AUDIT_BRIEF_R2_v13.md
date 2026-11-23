# Brief: claim audit of the round-2 text (A10 §10.3, extended by A11 and A12)

For a fresh agent on **Claude Sonnet 5.5**. The round-2 text was written by Claude Fable 5.2 and the text before it by Claude Opus 5.5, so the auditor must be neither. Prepared 22 Nov 2026, 05:40 EST, by session A. It starts when the text is frozen and the folder `out\audit_r2_input\` is filled.

## Rules for you
- Write only your output file. Do not edit any other file, and do not run builds.
- No web or external service; send no text anywhere.
- Do **not** read the generator code in `work\A_text\gen\` or `work\A_text\build\`: judge the text against the amendments and the data.
- Never open anything named `<excluded folder 1>` or `<excluded folder 2>`, nor the author's local secrets folder.
- The laptop is shared and its memory is tight: read files, and run at most one light Python process at a time (`python -I`).

## Read
- `revision_v13\AMENDMENT_12_v13.md` (the second amendment, "A12"), in full. Note especially:
  - §1, the labels;
  - §2, the under-run rule for the new runs;
  - §3a, the dropout replication, dose-response and decomposition;
  - §3b and §3c, the adaptive filter's twin and the two-noise IMM;
  - §3d, dropouts at 10 Hz (secondary);
  - §4, the Holm family of six;
  - §5 and §5b, the real-log mechanism check and the real-log decision test under dropouts;
  - §6, the caution-matched closed loop;
  - §7, the cut-off.
- `revision_v13\AMENDMENT_10_v13.md` §0, §2, §7.5, §9, §10, and `revision_v13\AMENDMENT_11_v13.md` §3.8 and §6b–§6d, for the rules that A12 leaves unchanged.
- `review_v13_sprint_output\ARS_REVIEW_SPRINT_v01.md` §2 and §3: the sprint panel's required wording (R1–R12). Round 2 must not undo it.
- `work\A_text\STATUS.md`, section "Now", entries of 22 Nov from 03:45 on: the coordinator's decisions on framing, caps and wording.
- `work\A_text\notes\AUDIT_FOCUS_R2_v13.md`: **the focus list; every item must get an explicit verdict.**
- `work\A_text\notes\RESULTS_INTERFACE_ROUND2_v13.md`: the round-2 keys and files.
- The inputs, all in `work\A_text\out\audit_r2_input\`:
  - `MANUSCRIPT_v13.md`, `SUPPLEMENT_v13.md`, `RESPONSE_TO_REVIEW_v13.md`;
  - `OUTCOMES_v13.json` (statuses) and `DERIVED_v13.json` (each printed value with its export key, source file and recount);
  - `BUILD_REPORT_v13.md` (its first line lists the export files);
  - `DIFF_MANUSCRIPT_v13.txt`, `DIFF_SUPPLEMENT_v13.txt` and `DIFF_RESPONSE_TO_REVIEW_v13.txt`: the differences from the 00:05 freeze, which the sprint's audits covered.

## Framing you will meet (the coordinator's, 03:45 and 05:30)
- The paper leads with a conditional finding: a covariance margin helps only where the covariance varies with the real error.
- Order of emphasis: that finding; the caution-matched closed loop with dropouts, with its caveats; the dropout replication and dose-response; the nuScenes mechanism check; and the limit that no real-log decision test was possible.
- Labels: "confirmed" only for the original plan (A10); "passed (amendment)" for tests of A11 and A12, or "(passed; amendment)" inside brackets; "replicated under rules fixed before the data" for the dropout replication; "(A)" in tables.
- For the pages, some older material moved to tables or to the supplement: Fig. 3 (now Fig. S2), §V-C's per-arm numbers, most of §V-D's detail, the sprint closed loop's higher-level numbers, the dropout efficiency, the two-noise IMM's twin difference.

## Audit
Every sentence of the **title, Abstract, Sections I and V–VII**, every **main-table and figure caption**, all of **Supplement S15**, **Table S5's rows on the second amendment and the word budgets**, and the letter's paragraph "**Round 2.**". The diffs show what changed since the last audited text; audit unchanged sentences only where a change elsewhere makes them wrong. For each, check:
1. **Numbers match their source** at the printed rounding; the interval is the one the text or caption says, at its level.
2. **Wording follows A12** (and A10 §9, A11 §3.8) for the outcome in OUTCOMES, and the coordinator's decisions.
3. **Labels** are the ones listed above; secondary, descriptive, exploratory and "not tested" labels are present where required; nothing of A11 or A12 is called "confirmed".
4. **No claim exceeds its rule:** no decision claim from the mechanism check; no equal-caution claim beyond the open-loop match; no magnitude carried to another configuration; no result of a test whose room test failed; no pairing of numbers from two run sets in one sentence.
5. **Nothing required is missing after the moves:** each disclosure A12 asks for is printed somewhere, and each pointer goes to a place that holds the value.

Rate each finding H (wrong number, or a claim beyond its rule), M (missing required wording or label) or L (clarity).

## Output
`work\A_text\notes\CLAIM_AUDIT_v13_r2_v01.md`, containing:
- which model you are;
- a table with one row per finding: location, quoted sentence, check 1–5, the rule or value it breaks, rating, and the fix in the fewest words;
- each focus item with its verdict;
- the sentences checked without findings, by section.

Keep fixes word-neutral where you can. The abstract is at its 250-word limit, the body has about 20 spare words, and the paper is at 10 typeset pages with almost no slack, so say what could be cut for any words you add.
