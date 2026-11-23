# ARS round 3: check of three final edits (editor-synthesis seat)

- Model: Claude Sonnet 5.5. Short check, not a new review round. No target score was given to me.
- Time (computer clock, Get-Date): start 2026-11-22 23:46:42; hashes re-checked and file written 2026-11-22 23:48:24 to 23:50.
- Hashes at start and at end (all equal to the ones given):
  - package_v13_2340 MANUSCRIPT_v13.md fdbe26861133beb904537c94e1d2551c60ccb674bd94a638edb28fdd2d99c1e9
  - package_v13_2340 SUPPLEMENT_v13.md 065ab3003d4645ef204f786afc8cf8613ee5adea56793e192e35c0ea0de3e622
  - package_v13_2340 MANUSCRIPT_v13.tex 9a42337d2ee749bf38852df596b1984459f510aad028991c38cb730ed7a6f7c9
  - package_v13_2244 MANUSCRIPT_v13.md 04b6ca9e... and SUPPLEMENT_v13.md e99e2d80... (start only; match)
  - ARS_REVIEW_ROUND3_v01.md 0a3eb0e4... and edit_check_diff_2244_2340.txt 07beda69... (start; match)
- Read: round-3 record sections 2, 3, 4a, 6, 8, 9; the coordinator's diff; the new md, tex and the built MANUSCRIPT_v13.pdf (text layer via pdftotext, 14 pages); Table 5, the Limits and the Acknowledgment in full; S12, S13; the official template (grep).
- Disclosure: my searches of the package's `verification` folder (not the forbidden `notes\` folder) also returned lines from the fifth claim-audit file. I used them only to see what the author's side claims; every ruling below rests on my own check of the text. I did not open the response letter, the amendment draft or `notes\`.
- Not done: I did not run the counting program, so the S12 count is checked against the printed values, not recomputed.

## 1. The three required items

### N-5 (remainder): RESOLVED

New text, II line 64: "The author read five of the 47 references in full ([13], [15], [19], [35], [36]); an AI system read 35 others at abstract level; [4], [10], and [41] to [45] were not read at abstract level; every reference's record but [10]'s was checked against Crossref or its source's page (Supplement S13)."

New text, S13 line 707: "...an AI system read 35 others at abstract level, and what the paper says about them stays within their abstracts; [4], [10], and [41] to [45] were not read at abstract level. On 22 Nov 2026 an AI system, under the author's direction, checked every reference's record but [10]'s: 36 against Crossref and ten against their sources' own pages."

Evidence:
- Count: 47 references; 5 read in full by the author; 42 others; 7 exceptions ([4], [10], [41], [42], [43], [44], [45]), all seven among the 42 ([10] is not one of the five). 47 − 5 − 7 = 35. 5 + 35 + 7 = 47. The record's own arithmetic (42 − 7 = 35) agrees; the reference list confirms the seven (a GitHub message definition, [10] the author's manuscript, a standard, two regulations, a UNECE proposal, an ISO standard).
- Record checks: 36 Crossref + 10 source pages = 46, plus [10] = 47. Agrees with "every reference's record but [10]'s".
- Wording: "35 others at abstract level" without "that have an abstract" is accurate and in fact better, as session A said. [10] has an abstract and was not read at that level, so "the 35 that have an abstract" would describe 36. The new sentence names the reader (an AI system), no longer says all 42 were read, and II and S13 now say the same thing with the same seven. The two statements about reading in the Acknowledgment ("Section II states what the author read in full") still point at the right sentence.
- The stray space is gone: the built PDF reads "in full ([13], [15], [19], [35], [36])" (this was O-6).
- Nit, not required: S13 line 705 says [45]'s status "was read from the consolidated text of its 01 series" and [42], [43], [41] "full texts were not read", while II/S13 say [41] to [45] "were not read at abstract level". These do not contradict (abstract level against scope or status), and S13 says what was taken from them.

### Q-1: RESOLVED

New text, S12 line 530: "418 of 418 result values printed in the main text (... each value counted once per print format; 7 of them the recomputed old-run values of Table 5: its 6, and one of these again as a percentage) had an agreeing second-program value".

Evidence from Table 5's old-evaluation column as printed: 5.51 (room), −0.0004 (N share), 0.015 (NA), 0.321 (TG), 0.382 (AM), 0.837 (CK3). That is six. CK3 is the braking prediction (fresh 0.783 prints as "78%" in the abstract and VII), so 0.837 prints again as "84%" ("38% to 84% across run sets", abstract and VII). One value per print format gives 6 + 1 = 7. The wording says exactly this, replaces the stale 4, and leaves the total 418 unchanged, as it should (the count of 409 + 9 added rows was already in). The "its 6" can be read against the table by any reader. I could not rerun the counter. One thing a pedantic reader could raise: Table 4's design cautions are also "old evaluation" values by Table 4's note; the sentence says "of Table 5" only, so it is not wrong.

### Q-2: RESOLVED

New text, V-D line 215: "Only these statements hold in the three lead-braking run sets of Table 5: the tracker covariance's share lies inside the equivalence margin and the sources' shares keep one order (point values rising: N, NA, TG, AM, CK3)". New text, VI line 303: "only Section V-D's cross-set statements hold in the three lead-braking run sets of Table 5". Table 5 row now reads "Room R (pp), lead braking: tuning / old evaluation / fresh runs", and the .tex agrees.

Evidence: the three columns of Table 5 are tuning, old evaluation, fresh. N share is 0.0000, −0.0004, 0.0000 (inside ±5%). Order N < NA < TG < AM < CK3 holds in each column (0, .064, .182, .278, .379; −.0004, .015, .321, .382, .837; 0, .024, .287, .369, .783). The crossing share (−0.067, outside the margin) is no longer covered by the wording. The tuning column is lead braking (S-tables speak of "the 20 lead-braking tuning runs"), so the label is true. No other "every run set" remains in the md or tex; the abstract's "38% to 84% across run sets" is about lead-braking room and is backed by the same three columns. Mild point, optional: III-A names six run sets and the "new" runs (150) are also lead braking, so "three lead-braking run sets of Table 5" is exact only because of "of Table 5"; it is.

## 2. New required items from the changed lines

I read all five manuscript lines (64, 215, 233, 303, 313), all five supplement passages (157, 530, 697, 699, 707) and the .tex hunks against the 22:44 text. The diff is as the coordinator describes; I confirmed it against the files. **No change opened a new REQUIRED item.** Checks:

- Line 64 / S13 707 / tex: consistent with each other and with the reference list; the new `\citenosp` and `\urlstyle{same}` compile (the PDF was rebuilt at 23:41, has 14 pages, and the rendered text matches the md).
- Lines 215, 233, 303: consistent with Table 5 and with each other.
- S5 budget row: "limit of fourteen typeset pages and budgets of 8,261 and 12,352, and 21,516 for the supplement" agrees with the build report's limits (8,261; 12,352; 21,516) and with the PDF page count (14). The build's counts are 8,237, 12,349, 21,513, all within.
- S12 line 697: "second and third rounds" and "five passes" follow from the record (this round is the third); line 699: "Ten reviews ... 2 + 1 + 1 + 6" adds up, matches the Acknowledgment's "Claude models, among them these three", and no "Nine reviews" is left in the md. The sentence "Every finding was fixed and every changed sentence audited again" sits next to "five passes"; the fifth pass cannot re-audit its own last fixes, which is a small overreach of wording, optional (O).
- Optional (L): the Acknowledgment's reference to "presubmission reviews by panels of five Claude agents" and S12's "Ten reviews" count this round's panel; this edit check is not a tenth review, and S12 counts only reviews that led to changes, which is said.

## 3. The repository sentence (form only)

Text, Acknowledgment paragraph 2: "The deposit is archived at Zenodo (doi: 10.5281/zenodo.24454179) and mirrored at https://github.com/anandakopalli7/tracker-covariance-safety-margins."

- Complete: it names the archive (Zenodo), the DOI, and a mirror with a full URL, and it follows the sentence that says what the deposit holds, so "the deposit" has its antecedent. It takes the place of the old placeholder; no marker is left in md, tex or supplement.
- Consistent: the rest of the paragraph (what is "available on request", nuScenes license, third-party code by hash in S1) is unchanged and agrees with it; S12's "the requests and responses are in the deposit" agrees.
- Style: "doi: 10.5281/..." follows the IEEE reference form used in the list ("doi: 10.xxxx"); the .tex sets the DOI as a link to doi.org with `\nolinkurl` (text prints without the prefix), and the URL with `\url` in `\urlstyle{same}`. The template has no data-availability heading and puts the paragraph where the Acknowledgment goes, so the place is right. In the PDF the URL breaks across two lines at "https://github." and "com/..." and the sentence period follows the URL directly; both are normal for IEEE and can stay.
- Optional only: add a version or "version 1" to the DOI if the author publishes a versioned record (a Zenodo concept DOI and a version DOI differ); say "deposited at Zenodo". The sentence is a statement of fact, so the record must be published before submission: it is a reserved draft, and this is the author's gate, not a text gate. I did not and could not judge whether the DOI resolves.

## 4. Bottom line

**Nothing is REQUIRED in the text before it is sent except the author's own gate (publish the Zenodo record so that the DOI resolves and the sentence is true); the round-3 decision (minor revision, 7.0) stands, and with the three edits the text is a firm 7.1 to 7.2, which I keep at 7.2 against the record's "about 7.1–7.2"; no change to the score, because the edits closed wording defects and added no evidence, and the ceiling near 7.5 (one simulator, one planner, small gains from amendments) is unchanged.**

Optional items left, unchanged from the record (O-1 to O-17), plus the three nits above (S13 705 against II wording, "five passes" sentence, a version in the DOI).
