# Claim audit and layout after the review of the author round: report of session A

Written 22 Nov 2026, 21:20 EST (computer clock), by session A (Claude Fable 5.2), for the author-facing session. It answers that session's message written at 20:10 (three items: the Holm second programs, a claim audit of the changed passages, stretched columns).

**Frozen 21:15:53, packaged 21:16:16. Two audits by Claude Sonnet 5.5 found no wrong value; their findings are fixed, answered, or left to the author. The manuscript has 14 pages and its log has no underfull vertical box.**

## 1. Folders, hashes, counts

- Freeze: `out\freeze_v13_2115\`. Package: `package_v13\`, identical snapshot `package_v13_2115\` (227 files).
- Kept: `package_v13_2016\`, `package_v13_1122_2002\`, and every earlier package and freeze. `out\freeze_v13_2100\` is the interim freeze the second audit read; it was never packaged.

| File | SHA-256 |
|---|---|
| PACKAGE_MANIFEST_v13.txt | `fce01b607ff32828382a12440ed40106f2b75fbbb9d644964e50cc3d7938797a` |
| MANUSCRIPT_v13.md | `c440adca7a70b2b74a373ee3a135d3eeac2c44a35ee6e28cb1c7280893d771b7` |
| MANUSCRIPT_v13.tex | `8e9e648ef0290856f5c0dbdb841ebb2ecf0dea57cca6b8e2cc81749e856386ac` |
| MANUSCRIPT_v13.pdf | `dc83ce17a652e734399f84005631649fe3801b936a589499a9ed1f0f68a51ccb` (1,503,536 bytes, 14 pages) |
| SUPPLEMENT_v13.md | `d18eee97e3f02f08159b1aaf81311a2663870818a42268dba706a1ba24d31b2b` |
| SUPPLEMENT_v13.pdf | `084091af1a419f0bff64b643da112a70133ad382d2e51c929fb077ceee8e5692` (43 pages) |
| RESPONSE_TO_REVIEW_v13.md | `326765eadd389d95d55a8a27ca1580dd2376b559352b85d8f95ef153e82f2153` |
| SANITIZE_NOTE_v13.md | `35a5d5416312f14095e8f6fd7e7ddf1325bf90bfbf0bdf792aa835496161b755` (PASS, 88 files) |

| Count | 20:16 package | Now | Limit |
|---|---|---|---|
| Typeset pages | 14 | 14 | 14 |
| Abstract, build's count | 238 | 237 | 245 |
| Abstract, strict count (compounds split at hyphens, en dashes, slashes) | 248 | 249 | 250 |
| Body | 8,251 | 8,253 | 8,253 |
| Whole text | 12,314 | 12,340 | 12,342 |
| Supplement | 21,303 | 21,491 | 21,500 |
| Named-passage values with an agreeing second program | 405 of 405 | 404 of 404 | all |
| Main-text or letter values without a second program | 0 | 0 | 0 |
| Overfull horizontal boxes | 0 | 0 | |
| Underfull vertical boxes | 21 | 0 | |
| Placeholders | 1 | 1 (repository and DOI) | |

- The word gates did not move. The body is at its limit, the whole text 2 below, the supplement 9 below.
- One value left the main text (the paired rest-gap difference of Section V-C), so coverage is 404 of 404.
- The strict abstract count is mine. Your count of the 20:02 abstract was one above mine, so expect 250.

## 2. Item 1: the Holm second programs

Done in the 20:16 package, which your message crossed. Supplement S12 has a sentence on the two recovered programs, and Table S29 two rows with their file times and hashes. I reran both into scratch files at 20:13: each reproduces its record file byte for byte apart from the "written" time. The caveat is gone from `STATUS.md`.

## 3. Item 2: the claim audit

**Procedure.** As in the earlier audit briefs: a fresh agent on Claude Sonnet 5.5 (the writer is Claude Fable 5.2), read-only, with no access to the generator code. Two passes:

| Pass | Brief | Text audited | Report | Findings |
|---|---|---|---|---|
| 1 | `notes\CLAIM_AUDIT_BRIEF_AR_v13.md` | `out\audit_ar_input\` (the 20:16 freeze and its differences from the 18:30 freeze) | `notes\CLAIM_AUDIT_v13_ar_v01.md` | 0 H, 7 M, 15 L |
| 2 | `notes\CLAIM_AUDIT_BRIEF_AR2_v13.md` | `out\audit_ar2_input\` (the 21:00 interim freeze and its differences from 20:16) | `notes\CLAIM_AUDIT_v13_ar_v02.md` | 0 H, 1 M, 9 L |

Both reports and both briefs are in the package's `verification\` with the earlier ones.

**What the first audit established.** About 220 printed values looked up: all match their export and an agreeing second program. Nothing in the main text or letter rests on one program. N-1, N-5 and N-20 (6) are unchanged. Every other required item is done. R-1 to R-19 of the earlier panel all hold.

**First audit, medium findings.**

| # | Finding | What I did |
|---|---|---|
| M-1 | S12 said two panels' records "name the model family only". The v12 record names the `sonnet` alias without a version; the first v13 round names Fable 5.2. | S12 corrected. I checked both records. |
| M-2 | Abstract and contribution 2 called the dropout shares "inside ±5%" without the start probability and without the 5.25% and 5.14% at higher ones. | Abstract: "(start probability 0.10; replicated; about 5% at higher ones)". Contribution 2: "at start probability 0.10 (the test and its replication; about 5% at 0.20 and 0.30)". |
| M-3 | Section V-E paired 2.8% (fresh runs) with 3.0% and 2.2% (new runs) in one sentence. | Each share now stands with its run set, under its own heading. |
| M-4 | "Recovers slightly more" for the coast-count margin reads the reverse direction of a one-sided test. | Marked "descriptive" in the abstract and contribution 2. Section V-E: "the test was one-sided, so the excess is descriptive". |
| M-5 | Section IV-E said the scoring library "was checked by hand on 20 decisions". S12 supports only the true clearance. | "the library's true clearance was recomputed without it on 20 decisions". |
| M-6 | The order of the sources across run sets was said to rest on one-program values of the old runs. | **Answered, not fixed as proposed: the premise was mistaken.** See below. |
| M-7 | The letter's older paragraphs quote wording the manuscript no longer has. | One sentence says that those paragraphs describe the text as it stood after each round. |

**M-6 in detail.** The auditor read the old runs' NA and AM shares from Table S13, which holds the earlier analysis's values (one program). The order claim does not rest on that table. Both programs' exports (`work\CD_capture\out\A_EXPORT_C.json` and `A_RECOUNT_C.json`, key `TRANSFER.structured`) hold the five sources' shares on the tuning, old evaluation and fresh runs under this paper's frontier, and they agree. The order N < NA < TG < AM < CK3 holds in all three. I checked this myself, and the second auditor checked it independently and agrees. The text now says so: Section V-D points to Supplement S12, and S12 has one sentence on it. Residue the second audit raised: the tuning and old-run values of NA, TG and AM are printed nowhere, and the order is one of point values (the fresh TG and AM intervals touch). Section V-D now says "point values"; the values are not printed.

**First audit, low findings.**

- Fixed: L-1, L-3, L-4 (contribution 2 only), L-6, L-7, L-8, L-9, L-10, L-11 (c) and (d), L-12, L-13.
- Not taken, for lack of room in the abstract (each is in the body): L-2 ("in open loop"), L-4b ("under dropouts"), L-5 (a unit for "0.05"), and the real-log ranking check in the abstract.
- Not taken: L-14 (a pass mark on Table 6's row for the first amendment's closed loop). Supplement S14's own table gives that class without a mark, and I found no record that settles it. The second auditor accepted this.

**L-9 changes your wording.** Your brief gave "was expected to match" for the clause after [27]. The auditor found no plan that records such an expectation before the test. The text now says "should match it".

**Second audit, and what I did.**

| # | Finding | What I did |
|---|---|---|
| M-A1 | My cut of "for a test" left "showed no room", which reads as a result. | Abstract: "showed no measurable room". |
| L-A1 | The adaptive filter's 4.6% had no run set. | "Its fresh-run share". |
| L-A2 | "A count ... scaled by" names the wrong object. | "a missed-update count, with factors from the covariance margin's median ratios". |
| L-A3 | "amendments followed first results" lost "tests". | Not taken: no room in the abstract. |
| L-A4 | Who bears each cost had become implicit in Section V-C. | "where unscored cost to following traffic and occupants would fall (full braking and peak deceleration)". |
| L-A5 | See M-6 above. | "point values" in Section V-D and S12. |
| L-A6 | The replication's interval was missing beside the fresh runs'. | Both are given: [0.0064, 0.0496] and [0.0077, 0.0518]. |
| L-A7 | S12 said every low finding was fixed or answered in the letter. | S12: "fixed, answered in the response letter, or left to the author". The letter lists them. |
| L-A8 | "Ranking is not shown" had no rate. | "not shown there" (the sentence is about 2 Hz). |
| L-A9 | "the same three models" for the panels reads against S12's list. | Left to the author. |

**The changes made in answer to the second audit have had no further audit.** S12 and the letter say so, and the letter lists them. They are the eight small edits in the table above.

**Left to the author** (from the first audit's L-11 and the second's L-A9):
- "No AI system is an author." stands between the author's second and third sentences. It came from your fix brief, not from the author's statement.
- "(the same three models; ...)" for the panels: each of the first four panels used one model, and the v12 panel's version is not recorded.
- The Acknowledgment says the deposit holds "the requests and responses of the presubmission reviews". The review folders hold letters, packages and reviews; the auditor did not find the requests there.

**S12 now says:** which model audited (Claude Sonnet 5.5, 22 Nov 2026), what (every changed passage against the plans and result files; every summary sentence against the size and status the body gives), the findings of both passes, and that the last wording changes have had no further audit.

## 4. Item 3: stretched columns

**Cause.** The class sets flush column bottoms, `\parskip` 0pt, 2 pt of stretch per heading, and club and widow penalties of 10000. A heading cannot sit at the foot of a column, so a column sometimes ends a few lines short. All the white space then went above the one heading in that column.

**Remedies tried** on the 20:16 text, in a scratch folder. All give 14 pages and no overfull box.

| Remedy | Underfull vertical boxes | of which from columns |
|---|---|---|
| none (as packaged at 20:16) | 21 | 14 |
| `\parskip` 0ex plus 0.2ex minus 0.1ex (the base class's own value) | 14 | 7 |
| `\parskip` 0pt plus 1pt | 14 | 7 |
| `\parskip` 0pt plus 1.5pt | 13 | 6 |
| `\parskip` 0pt plus 2pt | 12 | 5 |
| `\raggedbottom` | 7 | 0 |
| `\raggedbottom` and a filled logo box | 0 | 0 |

**Kept:** `\raggedbottom`, set in the preamble at `\begin{document}`. The class file is untouched. A stretch in `\parskip` only spread the large gaps over a heading and its paragraph (page 4: 54 pt above the heading and 27 pt below it).

**The seven other entries** came from the running head, one per odd page: the class puts the logo in a box of 29 pt, and my logo definition filled 26 pt. `\par\vss` at the end of that definition fills the box. I compared the page contents with and without it: all 14 pages are identical to the byte.

**Underfull vertical boxes per page (badness).**

| Page | Before | After |
|---|---|---|
| 1 | 10000, 10000, 10000 | none |
| 2 | 1838 | none |
| 3 | 2990, 1810, 10000 | none |
| 4 | 10000, 2401 | none |
| 5 | 10000 | none |
| 6 | 1810, 10000 | none |
| 7 | 10000 | none |
| 8 | none | none |
| 9 | 10000, 10000 | none |
| 10 | 10000, 10000 | none |
| 11 | 10000, 10000 | none |
| 12 | 10000 | none |
| 13 | 10000 | none |
| 14 | none | none |

**Gaps above headings.** I cannot view pages here, so I measured baselines in an uncompressed test PDF. Before: 68 pt above III-B and 31 pt above III-D (page 4), 42 pt above V-B, and 39, 38, 39 and 54 pt above the numbered headings of V-E. After: 25 pt above every section and lettered heading and 35 pt above every numbered heading. These are the class's own distances (13 pt and 23 pt of space plus the line). The first heading under a float has 37 pt, as before.

**Local hints.** With ragged bottoms the white space sits at the foot of a short column. Three columns ended more than a line and a half short: page 4 left (19 pt), page 9 left (39 pt), page 11 right (31 pt). One `\looseness=1` in one paragraph of each (the list `LOOSENESS` in the converter) leaves them 7, 27 and 19 pt short. The log's loose-line count stays at 17. Two more lines would bring pages 9 and 11 to 15 and 7 pt but add two loose lines, so I kept one. No `\enlargethispage` is used.

**The hints belong to this text.** After any change of wording they must be measured again. A stale hint is harmless (its paragraph runs one line longer), but it no longer helps. The converter reports a hint whose paragraph it cannot find.

**Unchanged and not mine to change:** 24 "Overfull \vbox ... while \output is active" entries. They come from the class's running head, which is taller than its `\headheight`.

`PAGES.txt` and the manifest now also record the underfull-vbox count.

**Please look at:** pages 4, 9 and 11 (the column feet), and page 9's left column, which still ends about two lines above the right one.

## 5. What changed in the texts, in one list

- **Abstract:** start probability and the larger shares at higher ones; "(descriptive)"; "no measurable room"; "a missed-update count, with factors from"; "position–velocity only". Cut: "(its uncertainty)", "on", "tests", "for a test".
- **Section I:** contribution 2 as the abstract, plus "only a ranking check (Section V-E)"; "no ranking shown inside the group". Cut: "as expected from its near-constancy".
- **Section II:** "should match it".
- **Section III-D:** "the retuned CV filter with its velocity process noise scaled by".
- **Section IV-E:** the hand check as S12 has it.
- **Section V-A:** "the old evaluation runs".
- **Section V-C:** "these contact rates are far above any deployable level"; "median peak"; the columns that carry the unscored cost; "the lower-level differences are below 1%". Cut: the rest-gap number (Table 4 has the rest gaps), "in that order", the clause on who pays.
- **Section V-D:** "(point values rising: N, NA, TG, AM, CK3; Table 2 and Supplement S12)".
- **Section V-E:** the Holm summary opens the section; the dropout shares, their margin and both intervals stand under "Detection Dropouts"; the two-noise share and the adaptive filter's share under "Other Trackers"; the one-sided test.
- **Section VI:** "a level effect at 2 Hz".
- **Table 4:** note (a) "the same runs at both levels"; note (b) on the IMM rows.
- **Supplement S12:** the third amendment's model lines; the order across run sets; both audits; each panel's models.
- **Letter:** rows N-3, N-7, N-8, N-14 and N-17; a paragraph on the audits and the layout; the note on earlier rounds' paragraphs.
- **Converter:** `\raggedbottom`; the logo box; three hints; the underfull count in `PAGES.txt`.

## 6. What I could not do, and what is open

- **I have not seen a page.** There is no PDF renderer here. All layout statements rest on the log and on measured baselines.
- **The last eight wording changes are not audited.** S12 says so.
- **Waiting for the author, untouched:** N-1, N-5, N-20 (6), the repository and DOI, and the three points of section 3.
- **S12 says "Eight reviews".** A further panel makes that nine.
- **The word gates are full.** Any added word needs a cut or a gate decision.
- Nothing installed or downloaded; no text sent to any external service; no pods.
