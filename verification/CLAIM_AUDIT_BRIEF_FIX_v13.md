# Brief: delta claim audit of the fix round (after the round-2 panel and the round-2 claim audit)

For a fresh agent on **Claude Sonnet 5.5**. The fix-round text was written by Claude Fable 5.2 and the text before round 2 by Claude Opus 5.5, so the auditor must be neither. Prepared 22 Nov 2026, 07:40 EST (computer clock), by session A, before the fix-round freeze. It starts when the text is frozen and `out\audit_fix_input\` is filled.

## Rules for you
- Write only your output file. Do not edit any other file, and do not run builds.
- No web or external service; send no text anywhere.
- Do **not** read the generator code in `work\A_text\gen\` or `work\A_text\build\`: judge the text against the amendments and the data.
- Never open anything named `<excluded folder 1>` or `<excluded folder 2>`, nor any folder whose name contains `local_secrets`.
- The laptop is shared and its memory is tight: read files, and run at most one light Python process at a time (`python -I`).

## Inputs
All paths are under `ARS_TRIAL\`.
- **The new text:** `revision_v13\work\A_text\out\audit_fix_input\`
  - `MANUSCRIPT_v13.md`, `SUPPLEMENT_v13.md`, `RESPONSE_TO_REVIEW_v13.md`;
  - `OUTCOMES_v13.json` (statuses) and `DERIVED_v13.json` (each printed value with its export key, source file and recount);
  - `BUILD_REPORT_v13.md` (counts against the caps; its first line lists the export files).
- **What changed against the round-2 freeze (`out\freeze_v13_0623\`, which the round-2 audit and the panel read):** `DIFF_MANUSCRIPT_v13.txt`, `DIFF_SUPPLEMENT_v13.txt`, `DIFF_RESPONSE_TO_REVIEW_v13.txt` in the same folder.
- **What asked for the changes:**
  - the panel synthesis, `review_v13_round2_output\ARS_REVIEW_ROUND2_v01.md`, section 5: required items R-1 to R-14 (section 4 gives the facts behind each);
  - the round-2 claim audit, `revision_v13\work\A_text\notes\CLAIM_AUDIT_v13_r2_v01.md`: 1 H, 11 M, 13 L;
  - the coordinator's decisions, recorded in `revision_v13\work\A_text\STATUS.md`, section "Now", entries of 22 Nov from 06:55 on.
- **The third amendment ("A13"):** `revision_v13\AMENDMENT_13_v13.md`, in full. It adds two amendment tests:
  - section 2, E6: the class average at scales 4, 8 and 16 on the closed loop's cases, compared with the covariance arm at equal closed-loop time lost. **Label rule (the coordinator's note at the head of section 2): "passed (amendment)" only if `E6.bracket` is bracketed and the upper end of `E6.delta.ci` is below zero; otherwise "failed (amendment)".** `E6.pass_alone` and `E6.delta.ub95` do not set the label.
  - section 3: the covariance against a fixed coast-count margin in open loop. Section 3.6 gives the wording; the coordinator adapted the failure wording, because the interval excludes zero on the other side (see "The writer's account" below).
  - section 4: Holm across A13's two tests (m = 2), reported beside the second amendment's and not merged with it.
- **Earlier rules that still hold:** `revision_v13\AMENDMENT_12_v13.md` (labels, section 1; Holm, section 4; the closed loop, section 6), `AMENDMENT_10_v13.md` section 9 and `AMENDMENT_11_v13.md` section 3.8.
- **The sprint panel's required wording:** `review_v13_sprint_output\ARS_REVIEW_SPRINT_v01.md`, section 3 (R1–R12).
- **Exports** (first program; the second program's file has `RECOUNT` for `EXPORT` unless a path is given):

| What | First program | Second program |
|---|---|---|
| Coast-count margin (A13 §3) | `revision_v13\work\F_nuscenes\out\A_EXPORT_DRF.json` | `A_RECOUNT_DRF.json` |
| E6 (A13 §2) | `revision_v13\work\E_closedloop\out\A_EXPORT_E6.json` | `A_RECOUNT_E6.json` |
| Holm, second amendment (six) | `revision_v13\work\shared\holm\A12_HOLM_v01.json` | `revision_v13\work\shared\holm_recount\A12_HOLM_RECOUNT_v01.json` |
| Holm, third amendment (two) | `revision_v13\work\shared\holm\A13_HOLM_v01.json` | `revision_v13\work\shared\holm_recount\A13_HOLM_RECOUNT_v01.json` |
| Post hoc resample count, first amendment's dropout class | `revision_v13\work\F_dropout\out\posthoc\DR_A11_PR_POSTHOC_v01.json` (`posthoc_p_r`) | `revision_v13\work\F_dropout\recount\DR_A11_PR_POSTHOC_RECOUNT_v01.json` (`DR.posthoc.*`) |
| Post hoc Bonferroni check (one program; its rule beside it) | `revision_v13\work\CD_capture\a11_bonferroni\BONFERRONI_A11_v13.json` | none |
| Closed loop matched in open-loop caution | `revision_v13\work\E_closedloop\out\A_EXPORT_E5.json` | `A_RECOUNT_E5.json` |
| Dropouts on the new runs; at 10 Hz | `revision_v13\work\F_nuscenes\out\A_EXPORT_DR2.json`, `A_EXPORT_DR10.json` | `A_RECOUNT_DR2.json`, `A_RECOUNT_DR10.json` |

## Scope (stop rule)
Audit the changed lines in the three diffs, and an unchanged sentence only where a change elsewhere makes it wrong. Nothing else is re-audited.

## The four checks
1. **Each required item is fixed as the letter says.** The letter's paragraph "Round-2 panel and claim audit (22 Nov 2026)" maps each of R-1 to R-14, each H and M finding of the round-2 audit, and the seats' other major points to a change. For each row: is the change in the text, and does it do what the item asked? Quote the new text.
2. **Every new or changed sentence** against the exports, A13's text and its labels:
   - numbers match their source at the printed rounding, with the interval and level the text states;
   - labels: "confirmed" only for the original plan; "passed (amendment)" or "failed (amendment)" for amendment tests ("(A)" or "failed" in Table V); "replicated under rules fixed before the data"; secondary, descriptive, exploratory and post hoc labels where required;
   - no claim beyond its rule: no closed-loop equal-caution claim beyond what E6 shows; no "tracks the error" for the dropout gain; no decision claim from the mechanism check; no numbers from two run sets paired in one sentence;
   - every pointer goes to a place that holds the value (tables were renumbered: see below).
3. **Nothing has regressed.** The sprint panel's R1–R12 and the round-2 text's labels and disclosures must survive. The round-2 audit's section 2, item (l), lists where each of R1–R12 stood at the 06:23 freeze; check each again.
4. **The page gate and the caps.** `BUILD_REPORT_v13.md` must say PASS with: 10 typeset pages; abstract at most 250 words; body at most 5,950; whole at most 9,250; supplement at most 21,500 (the coordinator's caps of 22 Nov, in Table S5's budget row). Count the abstract's words yourself.

Rate each finding H (wrong number, or a claim beyond its rule), M (missing required wording or label, or a required item not fixed) or L (clarity).

## The writer's account of the fixes
**Panel items (R-1 to R-14).**
- **R-1; audit 1, 2, 13:** "matched in open-loop caution" replaces "caution-matched" in the abstract, contribution 2, §V-E, the conclusion, S15, Table S5 and the letter. §V-E names the run set of the match (the older fresh runs, 18.2% against 18.4%) in its own sentence, then the 135 new cases; it prints the extra time lost and the rest gap; it names the 30 tuning cases.
- **R-2:** S15 and its closed-loop table give the class as "safer; time cost within the plan's 0.5 s tolerance". §V-C and Table IV keep the plan's class name for the braking prediction, with the rule in the caption.
- **R-3; audit 6, 12:** no heading or sentence says "tracks the error". §V-E reports the decomposition as descriptive and then the coast-count result.
- **R-4; audit 22:** the abstract and the conclusion open "In these tests … rarely beat/improved …, and then by little".
- **R-5; audit 4, 12:** the abstract gives the interval's level (99%) and "slightly inversely over all tracks"; §VI says "is consistent with"; §V-E says that the primary pairs mostly compare missed with steady tracks. **Not done:** the training-split τ is not printed, because no export pair holds it.
- **R-6; audit 3:** the abstract: "in closed loop it is equivalent within 0.10 contact share".
- **R-7:** the abstract, §V-E and the conclusion say that the recovered shares lie inside the ±5% margin; §V-E adds that no equivalence test was registered for them.
- **R-8:** §V-E's opening and the Limits scope the dropout results.
- **R-9; audit 9, 16; the domain seat:** the lower-bound sentence is in §V-E and the Limits (not §V-B: the 2.2% is reported in §V-E); Table III's row reads "IMM, two-noise (older runs, secondary)"; the pointer is Supplement S15.
- **R-10; audit 7, 11:** "no permuted-twin test of the covariance"; "mostly for other reasons" in the abstract, §V-E and the conclusion; §VI is narrowed to "under injected lead-braking misses".
- **R-11:** S15: "before any of those runs was extracted or scored".
- **R-12; audit 8, 10:** S15 gives the share among dropout decisions at 2 Hz and at 10 Hz and the 10 Hz limits; the stale parenthesis in Supplement S14's dropout table is gone.
- **R-13; audit 18:** §IV-E scopes the second programs' recount and names the Holm family. The Holm values are now two-program values and stand in Table V (column "Label", after "H"; the convention is (1 + k)/(n + 1) for all six).
- **R-14; audit 5:** the abstract ends "mainly at 2 Hz without latency".

**Other changes.**
- **Table V is new:** the tests of the later amendments with their labels. To stay at ten pages, the former Table V (what the score depends on) moved whole to Supplement S6, and §V-D points there. Supplement table numbers changed with it, and S15's overview table became one paragraph.
- **The abstract** gives the verdict first. It lost the per-phase schedule's share, crossing's room in points and the clause on the braking prediction's closed loop (the sprint panel's R5). The coordinator approved this on condition that the clause's content stays in §V-C and the conclusion and that the letter says so. Check both.
- **§IV-E** says what "preregistered" means here (internal locks, not a public registry); the lock hashes are in the order-of-work table of the supplement.
- **The coast-count margin (A13 §3): failed (amendment).** The interval of the difference lies wholly below zero, inside the equivalence margin. A13 §3.6's failure wording says "the interval includes 0", which is false here, so the text says what happened and S15 records the adaptation. The dropout test's own labels ("recovers", "replicated") are unchanged: the control explains the gain and does not reverse it. The two-population variant is in S15 only, as descriptive.
- **E6 (A13 §2):** read its outcome from the export pair and the label rule above, then check §V-E's sentence, the abstract's and the conclusion's clause, contribution 2, Table V's row and S15's paragraph and table against it.
- **Post hoc:** S15 has one sentence on a Bonferroni check across the first amendment's four sequences. Its p for the dropout class comes from the two post hoc files above; the value is 0.00515, printed to two significant figures.
- **The sprint's closed loop with dropouts** is one sentence in §V-E: equivalence at the lower level, and at the higher (secondary) fewer contacts for more time lost, "which cannot be told from a wider margin". This is decided (coordinator, 22 Nov): the sprint panel's R4 stays in the main text. Check that the sentence is there and that its numbers stand in Supplement S14.
- **Table S5** has new rows: the two stated times in locked text, the third amendment, the change of the coast-count baseline before its data, and the new budgets.
- **Audit items not taken:** 24 (the arrival time of the 10 Hz arrays) is for the coordinator; 25 was a count.
- **Not from the panel or the audit:** two escaped apostrophes in §III-C of the 06:23 Markdown were removed (the PDF was right).

## Output
`revision_v13\work\A_text\notes\CLAIM_AUDIT_v13_fix_v01.md`, containing:
- which model you are, and the SHA-256 of the three input texts at the start and at the end;
- one table with a row per required item (R-1 to R-14) and per H and M finding of the round-2 audit: fixed / fixed in part / not fixed, with the quoted new text;
- the round-2 audit's L findings: taken, or not taken with the reason above, and whether the reason is acceptable;
- new findings, rated H, M or L, each with the fewest-words fix;
- the regression check: R1–R12 of the sprint panel, one line each;
- the gate and the caps, with your own count of the abstract.

Keep fixes word-neutral where you can. The abstract is at its 250-word limit and the paper is at 10 typeset pages, so for any words you add, say what could be cut.
