# Brief: claim audit v09 of the sprint text (A10 §10.3, extended by A11)

For a fresh agent on Claude Fable 5.2 (the writer is Claude Opus 5.5). Prepared 21 Nov 2026, 19:45 EST, by session A.

## Rules for you
- Do not edit any file except your output. Do not run builds. No web or external service; send no text anywhere.
- Do **not** read the generator code in `work\A_text\gen\` or `work\A_text\build\`: judge the text against the amendments and the data.
- Never open anything named `<excluded folder 1>` or `<excluded folder 2>`, nor the author's local secrets folder (its path was given to the auditor; generalized here on 21 Nov 23:40 so that the package's public copy names no local account).
- The laptop is shared and its memory is tight: read files, run at most one light Python process at a time (`python -I`), nothing heavy.

## Read
- `revision_v13\AMENDMENT_10_v13.md`: §0, §2, §5.3–§5.4, §6, §7.5, §8.5, §9, §10.
- `revision_v13\AMENDMENT_11_v13.md` (the later amendment, "A11"), in full; especially §3.8 and §6b–§6d (consequence wording, disclosures, departures).
- `work\A_text\STATUS.md`, section "Now": the coordinator's decisions in this sprint (wording, caps, what was cleared when).
- `work\A_text\notes\AUDIT_FOCUS_SPRINT_v13.md`: **the focus list; every item must get an explicit verdict.**
- `work\A_text\notes\RESULTS_INTERFACE_SPRINT_v13.md` (keys and files of S0, X, DR, Y, B1r, E4) and `work\A_text\RESULTS_INTERFACE_v13.md` §4.
- The crossing records: `work\CD_capture\crossing\DEVIATIONS_X_v13.json` and `DEVIATIONS_X_v13_add1.json`.
- The inputs, all in `work\A_text\out\audit_v09_input\`: `MANUSCRIPT_v13.md`, `SUPPLEMENT_v13.md`, `RESPONSE_TO_REVIEW_v13.md`, `OUTCOMES_v13.json` (statuses), `DERIVED_v13.json` (each printed value with its export key, source file and recount), `BUILD_REPORT_v13.md` (its first line lists the export files).

## Decisions of this sprint you will meet (details in STATUS "Now")
- **Title rule (the author's):** crossing is named if X0 passes; dropouts if DR0 passes or E4's lower-level comparison is reported; lead braking stays.
- **X (cleared 19:35):** "uninformative variation" wording; "a small room" by a stated rule (the crossing room below a tenth of lead braking's); the amplitude-matched oracle's interval at the plan's nominal 99% fallback; the departure (tested despite step 0's no-go) in Table S5.
- **B1r:** a disclosed addendum; "very small", "inside the equivalence margin"; the registered H3 class stays the confirmatory result; no main claim rests on it. For page fit the conclusion no longer mentions it.
- **DR:** "confirmed but small", inside the margin; the "bottleneck" clause is session A's interpretive rule (focus item 6).
- **Y:** pass wording with its disclosure; **E4:** lower level primary, higher level secondary, not caution-matched; the coasting sentence is an interpretation.
- **Fig. 4** moved to Supplement S6. **Caps:** abstract 250, body 5,650, whole 8,800; 10 typeset pages.

## Audit
Every sentence of the **title, Abstract, Sections I and V–VII**, every **main-table and figure caption**, all of **Supplement S14**, **Table S5's rows on the later amendment, the pedestrian crossing and the word budget**, and the letter's paragraph "**Added at the end.**". For each, check:
1. **Numbers match their source** at the printed rounding; the interval is the one the text or caption says (level included).
2. **Wording follows A10 §9 and A11** for the outcome in OUTCOMES, and the coordinator's decisions.
3. **Labels:** "confirmed" only for a hypothesis that passed with every earlier one in its sequence; secondary, descriptive, exploratory, addendum and interpretation labels are present where required.
4. **No claim exceeds its rule** (no equivalence where a test failed, no transfer of magnitudes, nothing named in the title that the rule does not allow, no bound language for the amplitude-matched oracle).

Rate each finding H (wrong number or claim beyond its rule), M (missing required wording or label) or L (clarity).

## Output
`work\A_text\notes\CLAIM_AUDIT_v13_v09.md`: say which model you are; a table with one row per finding (location, quoted sentence, check 1–4, the rule or value it breaks, rating, the fix in the fewest words); then each focus item with its verdict; then the sentences checked without findings, by section. Keep fixes word-neutral where you can: the abstract has 6 words of room and the 10-page limit is tight.
