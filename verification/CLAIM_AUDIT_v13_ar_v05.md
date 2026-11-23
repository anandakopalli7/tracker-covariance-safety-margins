# Fifth claim audit: the final edits after the third review (v05)

- **Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`). The text was written by Claude Fable 5.2. Read-only except this file. No build, no web (neither the repository address nor the DOI was opened), no text sent anywhere; one light `python -I` process at a time; nothing under `holm_recount\`; no code under `gen\` or `build\`.
- **Computer clock:** start 23:31:51; closing hash check 23:35:06 (2026-11-22).
- **SHA-256 of the three input texts** (`out\audit_ar5_input\`), at the start and at the end, equal both times:
  - `MANUSCRIPT_v13.md` 62f809fe06c35ac01cdd57eda802007243b942c730ce5293bf647334ec4d5424
  - `SUPPLEMENT_v13.md` 1b72cc6c2b63f0e5ca2b840cc69c8661fabf7abc1bf26ec486b654447ab4d3ec
  - `RESPONSE_TO_REVIEW_v13.md` 361c918154e9fdb1aac443d95b9b46760fb42905c8a65b114c317acf0fb553fd
- **Read:** the brief and the "Rules for you"; the four difference files; the whole manuscript text; S12, S13, the departures-table row, and the letter's changed parts; `DERIVED_v13.json` (BOLD and XSET:old keys, Table 4 design-caution keys); `RECOUNT_COVERAGE_v13.md`; `BUILD_REPORT_v13.md`; `FINAL_EDITS_BRIEF_v13.md`; sections 1 to 4a and 10 of the third review's record; `A_EXPORT_C.json` and `A_RECOUNT_C.json` (key `TRANSFER.structured`); `.tex` source and `pdftotext` of PDF pages 3 and 13 to 14. **Not opened:** the code, the web, `<excluded folder 1>`, `<excluded folder 2>`, `local_secrets`.

## Check 1. Section II reading sentence against S13

| Statement | Source | Verdict |
|---|---|---|
| Section II and S13 say the same: five read in full ([13], [15], [19], [35], [36]); an AI system read 35 others at abstract level; [4], [10], [41] to [45] not read at abstract level; every record but [10]'s checked against Crossref or the source's page | II line 64; S13 line 707 | Same content. S13 adds "what the paper says about them stays within their abstracts" and the 36 + ten split. |
| The reference list has 47 entries | list [1] to [47] | Yes (BUILD_REPORT: 47 entries) |
| 5 + 35 + 7 = 47 | count | Yes; none of the seven is among the five |
| 36 + 10 + 1 = 47 | count | Yes. Eleven entries have no DOI ([4], [5], [10], [15], [32], [40], [42] to [46]), so 47 - 11 = 36 with a DOI; ten without one are checked at their sources, [10] excepted |
| [4], [10], [41] to [45] are the seven the 22:44 S13 excepted | difference file, old S13 line "except [4], [10], [41], [42], [43], [44], and [45]" | Yes, same seven |
| "35 others" rather than "that have an abstract" | writer's note; [10] has an abstract | Correct reasoning: that phrase would describe 36 |
| No other sentence of II, S13, the Acknowledgment or the letter contradicts it | grep of both texts and the letter | None in substance. Two soft points: F4 (how [45] was read) and F5 |
| Space between "(" and the first citation in the `.tex` | `.tex` source `(\citenosp{b13,b15}, ...)`; PDF page 3 text "([13], [15], [19], [35], [36]);" | No space; fixed |
| The `.tex` renders the same sentence | `.tex` | Same wording |

## Check 2. Supplement S12's counts

| Statement | Source | Verdict |
|---|---|---|
| 418 of 418 values; 7 old-run values | S12 line 530; RECOUNT_COVERAGE line 21 | Agrees with the coverage file (7, of which 6 in table rows; "prints 7 and 6") |
| The seven values | DERIVED keys `BOLD:points.all.R_pp` 5.51; `BOLD:points.all.RR.N|sh4` -0.0004; `XSET:old.NA` 0.015; `XSET:old.TG` 0.321; `XSET:old.AM` 0.382; `BOLD:points.all.RR.CK3|sh3` 0.837; `BOLD:points.all.RR.CK3|pct0` 84% | 7 keys, all `recount_agrees` true, no `one_program` |
| 6 in Table 5, one of these again as a percentage | Table 5, "old evaluation" column: 5.51, -0.0004, 0.015, 0.321, 0.382, 0.837; "84%" is 0.837 printed again in the abstract ("38% to 84% across run sets") and in Section VII | Correct. (38% is the tuning run's 0.379, a different set, key `C:TU.RR_CK3`) |
| Second programs: stored-run recount for 4, package CD's recount for the 3 shares | coverage line 21; `A_RECOUNT_C.json` | Matches: 5.51, -0.0004, 0.837, 84% from the B file; NA, TG, AM from the C file; values equal to every digit |
| Ten reviews: 2 + 1 + 1 + 6 | S12 line 699 | 10. Adds up. The third review is the sixth of 21 and 22 Nov |
| Third review's record gives seats' models and names the seats sharing a writer's model | review record section 1 (EIC Sonnet 5.5; R1 Fable 5.2; R2 Opus 5.5; R3 Sonnet 5.5; DA Fable 5.2) and section 10 (R1 and DA are the model that wrote the later text; R2 the earlier text; EIC, R3, synthesis Sonnet 5.5) | Yes. The record's own caveat says Sonnet 5.5 also audited the changed passages |
| "in five passes" | notes folder: `CLAIM_AUDIT_v13_ar_v01` to `v04` exist; this is v05 | Five, counting this one |
| Ten Fable audits and four Sonnet audits (unchanged lines) | notes folder: `v02` to `v11` (10), `r2_v01`, `fix_v01`, `fix_v02_E6`, `fix_final_v01` (4) | Counts match the files; models not re-checked here |

## Check 3. Sections V-D and VI against Tables 5 and 6

| Statement | Source | Verdict |
|---|---|---|
| N's share lies inside the margin in each of the three sets | Table 5: 0.0000 / -0.0004 / 0.0000 (tuning, old, fresh); `TRANSFER.structured.N_inside_delta_all_sets` true in both files | True (point values; the tuning interval [-0.0006, 0.0011] in Table S12 and the fresh interval are inside ±0.05) |
| Order N, NA, TG, AM, CK3 rising in each set | per_set, export and recount identical: tuning 0 < 0.064 < 0.182 < 0.278 < 0.379; old -0.0004 < 0.015 < 0.321 < 0.382 < 0.837; fresh 0.000 < 0.024 < 0.287 < 0.369 < 0.783 | True for each of the three, in both files |
| Real logs (set F) | `per_set.F` all null, `sets_missing` empty | Not defined there, so correctly outside the claim |
| Reach: pedestrian crossing is not covered | Table 6 share -0.067 [-0.221, 0.034], outside the ±0.05 margin as a point value | Right: the pedestrian run set is not a lead-braking set and is not named |
| VI: "only Section V-D's cross-set statements hold in the three lead-braking run sets of Table 5" | VI line 303 | True. The pointer "(Table 5)" moved before the colon in V-D; the closing parenthesis keeps only the order |
| Any remaining "every run set" claim | grep of manuscript, supplement, letter | None in the manuscript or supplement. One stale phrase in the letter (F3) |

## Check 4. The repository sentence

| Statement | Source | Verdict |
|---|---|---|
| Author's strings, verbatim: `<repository address>`; `10.5281/zenodo.24454179` | `FINAL_EDITS_BRIEF_v13.md` line 18 | `.md`: one occurrence of each, equal character by character |
| `.tex` `\url{...}` | `.tex` line 412 | Equal to the author's address (checked by string compare) |
| `.tex` `\href{...}{\nolinkurl{...}}` | `.tex` line 412 | Second argument equal to the author's DOI; first argument is `https://doi.org/` + the DOI (a resolver form of the same string; not opened) |
| PDF page 13 | `pdftotext` | Break after "https://github." with no added hyphen; no overfull text visible |
| No placeholder left | search of the `.md` and `.tex`, supplement, letter for REPOSITORY, placeholder, to be added | None left. Matches are the reference [4] "GitHub repository", S9 "CA defaults are placeholders" (unrelated), and the letter's own sentences about the removed bracket |
| Letter: "the author gave the DOI and the address ... no placeholder is left" | letter lines 92 and 241 | True of the text. Not said: the Zenodo record is a reserved draft, not yet published (see F1) |

## Check 5. The letter and the gates

| Statement | Source | Verdict |
|---|---|---|
| New section: "no wrong value; eight of nine resolved, one partly; three changes of one clause each; all three made" | review record section 3 (resolved 8, partly 1 (N-5)) and 4a (three required items) | True |
| Rows N-5 (remainder), Q-1, Q-2 | same | Each states what the text now says; Q-1 matches S12 and the coverage file; Q-2 matches V-D and VI |
| Row N-5, S2: follow the new wording | difference file | Yes |
| Row N-14: order "holds in the three lead-braking run sets of the table of Section V-D (both programs' exports hold it, as Supplement S12 says)" | S12 says only that this paper's old-run values are "in the table of Section V-D, from both programs' exports" | The clause "as S12 says" gives the order more than S12 says (F6, L) |
| Row "Optional": "level effect" defined at its first use in Section IV-C | manuscript line 112 (first use and definition); not used earlier | True; the V-E claim was wrong before and is right now |
| Last paragraph on author-only items | letter line 241 | True, see F1 |
| BUILD_REPORT says PASS | line "Result: PASS" | Yes |
| Word gates | BUILD_REPORT: abstract 235 (limit 245); body 8,237 (8,261); whole 12,347 (12,350); supplement 21,511 (21,511) | The letter's "Structure and length" says 8,237, 12,347, 21,511 and 235: agree. Row of departures table "budgets of 8,261 and 12,350, and 21,511 for the supplement": agrees. Body and whole both rose by 8 words; abstract unchanged (the difference file shows no abstract line) |
| Pages | letter and brief: 14 | PDF text pages 3 and 13 to 14 read; page count not measured here |

## Findings

No H.

**M**

- **F1 (M).** Acknowledgment, second paragraph, and the letter's "Author-only items": "The deposit is archived at Zenodo (doi: 10.5281/zenodo.24454179) and mirrored at <repository address>/..." and "no placeholder is left". The brief for these edits says the Zenodo record is a reserved draft and not published; until the author publishes it the DOI does not resolve and "is archived" is not yet true. Fix: no text change if the author publishes before submission; add to the letter's last paragraph one clause: "The author publishes the Zenodo record before submission." (cut the same number of words from the letter's Optional row).

**L**

- **F2 (L).** S12 "7 of them old-run values, recomputed: 6 in Table 5 ...". Table 4's design cautions (14.10, 22.30, 11.88) are also old-evaluation values by Table 4's note, and are not among the seven (they come from the closed-loop export). Fix: "recomputed from the stored old runs" in place of "recomputed" (S12 has no room: cut "(the whole paper from the abstract to the conclusion," to "(abstract to conclusion,").
- **F3 (L).** Letter, the row of the first review round ("Result"), line 163: "Done with three run sets (tuning, old, fresh) and the real logs where defined ... The Limits list only the statements that hold in every set". The Limits now say "the three lead-braking run sets of Table 5". Fix: "in the three run sets".
- **F4 (L).** Section II / S13: [45] is "not read at abstract level", yet IV-A takes the stop parameters from it and S13 says the status of UN R157 "was read from the consolidated text of its 01 series [45]". A referee may ask what of [45] was read. Fix: in S13 end of the sentence "[45] for its parameters and status" (4 words; cut 4 in the same paragraph, for instance "under the author's direction,").
- **F5 (L).** S12 "in five passes: every changed passage ... and every summary sentence ..." followed by "Every finding was fixed and every changed sentence audited again". The fifth pass covered only the last edits and their consequences, and any fix to its findings is not audited. Fix: the replacement of "AUDIT PENDING." in the letter should say so (below); S12 can stay if the fifth pass's scope is stated in the letter.
- **F6 (L).** Letter N-14: "(both programs' exports hold it, as Supplement S12 says)". S12 says only that this paper's old-run values stand in Table 5 from both programs' exports. The order itself is in `TRANSFER.structured` of both files (checked). Fix: "(both programs' exports hold it; Supplement S12)" or drop "as ... says".
- **F7 (L).** V-D and Table 5 do not say that the tuning column is lead braking (20 lead-braking runs, Table S12), so the phrase "three lead-braking run sets" is checkable only in the supplement. Fix: "lead-braking tuning / old evaluation / fresh runs" in the Recording-policy row (+2 words; body room is 24).

## Gates

Abstract unchanged (no line in the difference file); build count 235 of 245. Body 8,237 of 8,261 (24 words of room). Whole text 12,347 of 12,350 (3 words). Supplement 21,511 of 21,511 (0). BUILD_REPORT: PASS; open markers 0; no placeholder. Any word added for F2 to F7 must be cut as named above: F7 fits in the body room; F2 and F4 are word-neutral in the supplement.

## What the replacement of "AUDIT PENDING." must state

That a fifth claim audit by an agent on Claude Sonnet 5.5, a model other than the writer's (Claude Fable 5.2), checked on 22 Nov 2026 (computer clock 23:31 to 23:35) only the changes made after the 22:44 text: Section II's reading sentence against Supplement S13 (47 references, 5 + 35 + 7 and 36 + 10 + 1), Supplement S12's counts (7 old-run values, 6 in Table 5 and one as a percentage; ten reviews; five passes), the two cross-set statements of Sections V-D and VI against Table 5 and both programs' exports, the repository sentence against the author's two strings in the text and the typeset file, this letter, and the word gates (build PASS). It found no wrong value and no high finding; one medium and six low (F1 to F7). It must then say which of F1 to F7 were fixed, and that any change made after the audited text (hash 62f809fe... for the manuscript) has had no separate audit. It must not say that every summary sentence was checked in this pass: only those touched by the changes were. Counts of word gates to repeat if the letter quotes them: body 8,237, whole 12,347, supplement 21,511, abstract 235.

## Verdict

The three edits do what the third review asked: the reading sentence agrees with S13 and the counts (47, 5 + 35 + 7, 36 + 10 + 1), S12's old-run count is exactly the seven keys the coverage file recounts, the cross-set statements are true in each of the three lead-braking sets in both programs' files, and the repository sentence matches the author's strings with no placeholder left. No wrong value and no high finding; the one medium finding is the unpublished Zenodo record behind "is archived", an author gate rather than a text error. The gates hold (PASS; 24 and 3 words of room in the body and whole text, none in the supplement).
