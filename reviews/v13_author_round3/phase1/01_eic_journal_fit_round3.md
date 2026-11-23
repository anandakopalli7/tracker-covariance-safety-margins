# Round 3, seat EIC (Journal-Fit Reviewer): review of the 22:44 text

## 1. Header

- **Seat:** EIC, Journal-Fit Reviewer. **Card:** "Card 1: Journal-Fit Reviewer (internal role EIC)", `review_v13_output\00_phase0_field_analysis_and_cards.md` (only the card and the field analysis read).
- **Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`). Standards: re-review standards of `academic-research-skills:academic-paper-reviewer`, one seat only. No sub-agents, no web, no manuscript text sent anywhere, one process at a time.
- **Card-confirmation pause not held** (non-interactive run).
- **Files and hashes at start (all five equal the brief):**
  - `MANUSCRIPT_v13.md` 04b6ca9e2c47fb34d0f9b09f980c8e6855e37ebfd0062368649a75636d3e2eb8
  - `MANUSCRIPT_v13.tex` 710a8366cb4aba07bbe8fd67084a38f217f2862cf6d8d8bfc0ebeb4c80f6df8d
  - `SUPPLEMENT_v13.md` e99e2d807a0884af7e53866a69a4b5f7019741e1fa75902a5cfcf56fd2545eba
  - `MANUSCRIPT_v13.pdf` 93926a734b87ea1fb17117928edda98a2603d041b89afdc9521f1e8a5d650914
  - `SUPPLEMENT_v13.pdf` ec81d45527801c11bd0ad4b06f91c94c44ef7c430b03235bf3ef1770f3b03f23
- **Hashes at end:** recomputed after the last read; see the last line of this section (HASH-END).
- **Pages viewed as images:** manuscript `page01.png` to `page14.png` (14 of 14); template `tpl01`, `tpl03`, `tpl04`, `tpl06`, `tpl07`, `tpl08`, `tpl09` (7 of 9; `tpl02` and `tpl05` not opened); supplement page images not opened (the supplement was read as `SUPPLEMENT_v13.md`, only S12, S13 and grep checks).
- **Files read:** the brief; the field analysis and Card 1; my own round-2 report; `work\round2_record_sections_3_4.md`; `work\letter_section_round2.md`; `MANUSCRIPT_v13.md` in full; `MANUSCRIPT_v13.tex` (lines around 50, 54, 123, 426 only); `SUPPLEMENT_v13.md` (S12, S13 and pattern searches); `ojits-template.tex` (pattern search plus lines 472 to 478, 580 to 600). Nothing else.
- **Template line numbers** below are those of `ojits-template.tex`.

## 2. Judgement

- **Recommendation: minor revision.** Borderline with accept-after-one-edit: one REQUIRED-minor wording item (Q-1) and OPTIONAL items remain; nothing needs new analysis. No CRITICAL finding.
- **Score: 7.3 / 10; 3.7 stars out of 5** (round 2: 6.5 as it stood, 7.2 conditional on the author's three items; round 1: 5.8).
- **Likely editorial outcome at OJ-ITS:** major revision on significance and length rather than on any defect of reporting (about 50%); minor revision about 30%; reject (with or without resubmission) about 20%; desk-reject on the AI paragraph under 3%. The two integrity statements an editor would have queried first, who decided and what was read, are now in the text.
- **Send as is, apart from the DOI? No, but only because of Q-1.** Section II says "the others were read at abstract level", while S13 says seven of those others ([4], [10], [41] to [45]) were not read at abstract level and an AI system, not the author, read the rest. That is one clause in the exact sentence an editor will probe, and it should agree with S13 before the text leaves. With that clause fixed I would send it; the rest (14 pages, tables at 6 to 7 pt, "et al.", conference locations, the word "Preregistered" in the title, supplement vocabulary) is the kind of thing a journal asks for in review and does not make the submission wrong. The mostly null headline in one simulator sets the ceiling for the score, not the text.

## 3. The nine open items

| ID | Verdict | Evidence (22:44 text, location) | What remains |
|---|---|---|---|
| N-1 | **Resolved** | ACKNOWLEDGMENT ¶1 (p. 13): "The author conceived the study, set its questions and plans, made or approved every scientific decision, and reviewed and approved all content, and takes full responsibility for the work." ¶3: "Where the amendment files record a design choice as an AI session's, it was made within the author's approval." The two sentences now agree. | Nothing required. Optional: "within the author's approval" does not say whether each choice was approved before its amendment was locked; the author's fact (O-q2). |
| N-5 | **Resolved**, with one new wording item (Q-1) | Section II "Novelty, with its limits" (p. 3): "The author read five of the 47 references in full ([13], [15], [19], [35], [36]); the others were read at abstract level, and every reference's record but that of the author's own manuscript [10] was checked against Crossref or its publisher's page (Supplement S13)." ACKNOWLEDGMENT ¶3 ends: "Section II states what the author read in full." S13 (line 707): "The author read five of the 47 references in full (...); an AI system read the others at abstract level, except [4], [10], [41], [42], [43], [44], and [45]; ... 36 against Crossref and ten against their sources' own pages; [10] is the author's own manuscript. One date was corrected ([45])." The counts agree (36 + 10 + [10] = 47). | Q-1: Section II says "the others" at abstract level, S13 excepts seven, and Section II does not say who read the abstracts. |
| N-20 (6) | **Resolved** | Running head, pages 2 to 14: "Kopalli: Tracker Covariances as Safety Margins in Motion Planning" (`.tex` line 50: `\markboth{...}{Kopalli}`); reference [10] (p. 13): "A. S. K. Kopalli"; byline (p. 1): the full name, with the corresponding-author line repeating it. One surname form is used in the head and in [10], and the full name stands on page 1. The family-name choice is the author's (brief). | Nothing required. |
| P-1 | **Resolved** | Abstract (p. 1): "In simulated tests of one speed planner predicting at constant velocity (straight road, 5 to 15 m/s)"; "With fixed noise and regular updates the covariance is nearly constant and adds nothing"; "beats its within-run permuted twin by 0.05 of the room (a timing effect)"; "Pedestrian crossing (open loop; room 0.16 points) showed variation without recovery". "Regular updates" also in I (contribution 2, and the covariance sentence) and VI. 235 words. | Optional: "nonbraking leads" in the abstract's last sentences versus "leads that do not brake hard" in the body (O-q3). |
| P-2 | **Resolved** | IV-E is four paragraphs (locks; sequences and Holm; the AI panel and second programs; departures); V-C three; IV-C three; V-E "Detection Dropouts" three (pp. 5 to 6, 8 to 11). The class rule of Table 4 sits in a note row (^d^), and its caption is four lines (p. 9). | Two blocks still about 300 words: VI "Limits" (p. 12) and V-E "5) Mechanism Check" (p. 11 to 12). Optional (O-8). |
| P-3 | **Resolved** | V-C (p. 7 to 8): "In these 60 cases the lead brakes to a stop and the ego ends the run behind it, so at the lower level every arm loses 24.5 to 24.8 s of the 30 assessed seconds (Section III-B), and the paired differences are below 1% of that"; "full braking is the planner's hardest row ... and the share of decisions in which a margin source could change the row was not computed." III-B defines time lost over the assessed 30 s. | Nothing. |
| P-4 | **Resolved** | Section II (p. 3): "with fixed noise the covariance is then a function of the arrival sequence and, for noise fixed in the object frame, the heading, so on a straight road a margin that counts missed updates should match it (Section V-E)". Agrees with VI ("follows the update schedule and the geometry"). | Nothing. (Author to check the critical-rate clause against [27], as before; not a text finding.) |
| P-5 | **Resolved** | Table 5 (p. 9), rows "NA share, same columns 0.064 / 0.015 / 0.024", "TG share ... 0.182 / 0.321 / 0.287", "AM share ... 0.278 / 0.382 / 0.369", "CK3 share ... 0.379 / 0.837 / 0.783" beside "N share ... 0.0000 / −0.0004 / 0.0000". I checked the order N < NA < TG < AM < CK3 in each column: it holds in all three, as V-D says. | Nothing. |
| P-6 | **Resolved** | IV-C (p. 5): "Because the permutation is within runs, a positive difference shows that the margins' timing matters; it cannot separate ranking among decisions from a *level effect* ... that follows the lead's phase. Only the dropout test had a control for such an effect, the coast-count margin (Section V-E)." Abstract "(a timing effect)"; VII "only the dropout gain had a control that separates ranking from level". | Nothing. |

**Counts: resolved 9, partly resolved 0, not resolved 0.**

## 4. Findings

Types: W wording; M a value moved in from the supplement; T text the author writes from existing records; A new analysis or evidence. REQUIRED means I would withhold "accept as is" without it. No finding is marked CRITICAL. Round-2 OPTIONAL items are carried under their round-2 labels (o1 and so on).

### 4a. REQUIRED-major (0)

None.

### 4b. REQUIRED-minor (1)

| ID | Location | Finding | Evidence quoted | Fix (fewest words) | Type |
|---|---|---|---|---|---|
| Q-1 | Section II "Novelty, with its limits" (p. 3); S13 (line 707) | The main-text sentence on reading overstates and is passive, in the one place an editor checks. Section II says all 42 others "were read at abstract level"; S13 excepts [4], [10], [41] to [45] (a repository, the author's own manuscript, two standards, two regulations and a UNECE proposal, which have no abstract level) and says an AI system read the rest. A reader who compares the two finds the paper's own claim about its own reading unequal in two places. Introduced by the fix for N-5 (regression, small). | II: "the others were read at abstract level"; S13: "an AI system read the others at abstract level, except [4], [10], [41], [42], [43], [44], and [45]" | In II: "an AI system read the others at abstract level, except the standards and regulations, [4], and [10]". | W |

### 4c. OPTIONAL (9 carried, 5 new)

| ID | Location | Finding | Evidence quoted | Fix | Type |
|---|---|---|---|---|---|
| Q-2 (new) | Title; abstract; IV-E | The title says "Preregistered", the text says "internal locks, not a public registry ... no third-party timestamp", and three amendments followed first results. The term is defined in IV-E and the abstract says "hash-locked internally", so nothing is hidden; but a referee at a clinical-trial-minded venue may read the title as stronger than the evidence. The title is the author's; this is a risk note, not a finding on facts. | Title: "A Preregistered Equal-Caution Study"; IV-E: "By "preregistered" we mean internal locks, not a public registry" | "Hash-locked" or "Pre-specified" in the title, or keep. | W (author) |
| Q-3 (new) | Section II, p. 3 | Typeset glitch: the five full-read references print as "in full ( [13], [15], [19], [35], [36])", a space after the opening bracket, because the source uses separate `\cite` calls. | `.tex` line 123: `in full (\cite{b13,b15}, \cite{b19,b35}, \cite{...` | One `\cite{b13,b15,b19,b35,b36}`. | W |
| Q-4 (new) | Supplement S12 (lines 697, 699) | Process vocabulary left: "the review panel of the author round" and "The reply to the reviews answers the review of the previous draft in full" (a journal reader will take "reply to the reviews" as a reply to the journal's own referees). The earlier terms "response letter", "round-2 panel", "decision log" are gone (checked by search). | S12 "Claim audit": "were read by the review panel of the author round"; "the reply to the reviews lists their findings" | Name panels by date; say "the deposit holds the requests and responses". | W |
| Q-5 (new) | Fig. 2(b), p. 7 | The right panel is an empty axis with "No wrong goes at any caution"; half a figure width to show a flat zero the caption already states. | Fig. 2(b) caption: "F0, E, and N are at zero wrong goes at every caution" | Drop the panel; keep the sentence. Saves about a quarter page. | W |
| Q-6 (new) | Acknowledgment ¶3 | "Made or approved" is now honest, but a reader cannot tell whether the author approved each AI design choice before it was locked or accepted the process in general; IV-E says the AI drafted the amendment plans after a panel report. The author's fact; add a clause only if true. | "it was made within the author's approval" | "approved before the amendment was locked" if that is so. | T (author) |
| o1 (carried) | Whole | 14 pages, body 8,229 words, 47 references, 43-page supplement, against a field target of about 10 and the template's "commensurate" principle (template 622). Down 24 words from round 2, level with it in pages. Contribution 2 and the repeated "(descriptive; ...)" tags are the cheapest cuts; Fig. 2(b) (Q-5) and Table 5 with Fig. 4 are the next. | Pages 1 to 14 | Aim at 12. | W |
| m4 (carried) | II and VI run-in heads | Bold sentence-case run-in heads are not a template level; V-E's "1) ..." heads match template 378 and `tpl04`. | "**Perception judged by its effect on decisions.**" | Title case or plain. | W |
| o2 (carried) | [9], [13], [15], [21], [34] | "et al." where names may be listed (template 495); allowed beyond six authors. | "H. Caesar *et al.*" | List names or keep if over six. | T |
| o3 (carried) | 15 conference references; [46] | No city and country (template 722; `tpl08`). | "in *Proc. IEEE Intell. Veh. Symp. (IV)*, 2018, pp. 1171–1178" | Add if enforced. | T |
| o4 (carried) | Fig. 1 boxes (p. 4); Tables 2 to 6 (pp. 7, 9, 10) | Type about 6 to 7 pt against "8 to 10 point" (template 390 to 391); Table 5 and Table 6 are the densest. | pp. 4, 7, 9, 10 | 8 pt or fewer columns. | W |
| o9 (carried) | Table 5 "Nonbraking leads" rows | Two unlabeled numbers per cell. | "CK3: costs progress (5.3, 0.0)" | Two columns with headers. | W |
| o12 (carried) | Captions of Tables 2, 4, 6 | Four to six lines each, with rules; Table 4's was cut and its class rule is in a note, which helps. | Table 6 caption, p. 10 | Move rules to text. | W |
| m13 (carried) | VI "Limits" | "one in-house planner" while the Acknowledgment says Codex developed the planner software. | "one in-house planner" | "one planner written for this study". | W |
| o13 (carried) | Back matter | No author biography; optional at submission (brief: advisory). | n/a | At acceptance. | T |

**Carried OPTIONAL not repeated because settled this round:** o11 (the companion paper [10] is now disclosed in Section I "Scope": "under review ... shares this paper's detector architecture, tracker configuration, and margin form", which meets template 599 to 600; a cover-letter line is still sensible).

**Counts.** REQUIRED-major 0; REQUIRED-minor 1 (new: 1, Q-1); OPTIONAL 14 (5 new, Q-2 to Q-6; 9 carried). By type for REQUIRED: W 1; none is M, T or A.

## 5. Q1 to Q8: what changed since my round-2 report

**Q1. Labels and sizes.** Unchanged and sound. The abstract's statuses are now carried by wording, the first sentence scopes the claims, and the pedestrian test states "open loop; room 0.16 points". I found no label that overstates. One check I made against the table: the coast-count result still reads "recovers slightly more (descriptive)" with "−0.0024 [−0.0057, −0.0001] ... below zero and within the equivalence margin; failed", and VII and VI say the same.

**Q2. Overreach.** The new sentences are tighter: IV-C now says a within-run permutation "cannot separate ranking among decisions from a level effect"; V-C now says the time-lost differences are "below 1%" of a 24.5 to 24.8 s loss and that the share of decisions where a margin source could change the row "was not computed". The remaining soft spot is the title word (Q-2), which the text itself qualifies.

**Q3. Earlier limits.** All carried. Limit (f), density, is partly handled (paragraph splits) and not by length: still 14 pages.

**Q4. Readability.** Better. IV-E reads in four short blocks, V-C in three, the abstract names its scope, "level effect" is defined in IV-C where first used, and Table 4 marks which classes are tests. The abstract still carries about 25 numerals and a few terms a general reader will not have (CANMOT is absent, which helps; "room" and "permuted twin" are glossed). The take-away for a designer (a fixed-noise covariance acts as a constant; a braking prediction carries the room at a cost; a missed-update count reproduces the dropout gain) is clear in VII.

**Q5. Verdict.** Minor revision, 7.3 / 10, 3.7 stars. The two items that held round 2 at major are closed, and what keeps the score below 7.5 is the paper's own ceiling (null result, one simulator, no decision-level real-log evidence, 14 pages) and the density.

**Q6. Self-containment.** The eight round-1 cases stay closed. The one new dependency, P-5's cross-set order, is now answered in Table 5. The sentence in Section I that the main text holds every result the claims rest on is true as written (it names the two one-program diagnostics).

**Q7. Format and declarations (template lines).**
- **Checked on the page images and fine:**
  - Abstract: 235 words, one paragraph, no references (template 32 to 36; `tpl01`); five index terms, alphabetical.
  - Title case title; author line, one affiliation, ORCID, corresponding-author line, funding sentence in the first-page note and no Funding heading (template 477 to 478).
  - Section heads in capitals I to VII; V-E "1)" to "5)" subheads match the template's subsubsection style (template 211, 378; `tpl04`); "Fig. N" in text with "FIGURE N." below figures and "TABLE N." above tables, Arabic numerals as the rendered template `tpl03` has (template 421 to 424 says Roman; the class decides), captions below figures and above tables (template 448 to 449).
  - Table footnote letters in note rows under Tables 2, 4 and 6, with the whole-table sentence unlettered (template 283 to 284, 518 to 519).
  - Singular ACKNOWLEDGMENT with "acknowledgment" spelling (template 472 to 478); order: responsibility, deposit, AI disclosure, declarations.
  - References with initials, quoted titles, italic abbreviated venues, volume, number, pages, year, DOI; [4] accessed date; [10] "submitted for publication"; no versioned arXiv IDs; American spelling, serial comma, zero before decimals, "multiobject" and "midrank".
  - The companion manuscript is disclosed in Section I "Scope" (template 599 to 600).
  - Running heads and the OJ band on alternate pages as in `tpl01` and `tpl04`; page 14 about half empty.
- **Fixed since round 2:** surname form (N-20 6); N-1 wording; Table 5 rows; Table 3 label "before braking only"; Table 4 test marks.
- **Still open (all optional, as in section 4c):** run-in heads, "et al.", conference locations, type size, unlabeled cell pairs, no biography, the `\cite` space (Q-3).
- Repository name and DOI are the gate and are not counted.

**Q8. AI disclosure (checked against the text and S12/S13).**
- *Does it meet IEEE's rule?* Yes. ¶3 names the systems and models (Claude: Opus 5.5, Fable 5.2, Sonnet 5.5; Codex: GPT-6.1 Sol, GPT-6 Astra, GPT-6.2 Astra), the tasks ("the analysis, simulation-control, and figure code, ran the literature searches, and drafted and revised the text of all sections and of the supplementary material"; Codex "the simulation, recording, and planner software in an earlier phase"; "drafted the amendment plans and proposed design options"), the human role ("the author chose among those options, rejected or changed several, corrected errors and overconfident statements ... and directed further experiments after the systems had judged the manuscript ready"), and "No AI system is an author". It sits in the Acknowledgment where template 472 to 478 puts such statements, after the deposit paragraph.
- *The change to "made or approved".* ¶1 now reads "made or approved every scientific decision, and reviewed and approved all content", and ¶3 "made within the author's approval". These two no longer pull against each other: the first admits that some decisions were the AI's and approved after; the second says the same for the amendment files. I would not touch ¶1 again. What a careful editor can still ask (O: Q-6) is whether "approval" came before each lock; that is the author's fact and one clause if true.
- *Facts checked against the paper.* (1) Models by role agree with S12 (Opus 5.5 first programs; Sonnet 5.5 or Fable 5.2 second programs; audits by Fable 5.2 and Sonnet 5.5). (2) "Separate Claude sessions wrote the second programs and audited the claims (Section IV-E; Supplement S12 names the model of each pass)": IV-E gives "written in separate sessions ... without reading the first programs"; S12 gives the models. (3) "panels of five Claude agents (Claude models, among them these three ...)": S12 line 699 counts nine reviews and names one Sonnet panel whose version is unrecorded, so "among them" is now accurate (O-1 of round 2 done). (4) "Section II states what the author read in full": true (five references), but see Q-1 for who read the rest. (5) "requests and responses of the presubmission reviews" in the deposit: true when the deposit is published (gate). (6) The single-vendor correlation caveat ("All seats are Claude models, so their errors may be correlated") is in S12 and not in the main text; the Acknowledgment does say "Claude agents" and "Separate Claude sessions", so the fact is visible; I do not require more.
- *Would an editor desk-reject?* Under 3%. The cumulative picture (AI-written text, AI-run search, AI panels, local hash locks, amendments after first results) is disclosed in full and in the required place, and the paper is better for it. The one thing I would fix before submission is Q-1.

**Length and density at 14 pages.** Body 8,229 words, 14 pages, 43-page supplement: the same page count as round 2 and a few words shorter. Paragraph structure is now readable; length is not reduced. An OJ-ITS editor will likely ask for a shorter paper (o1), but that is a review-stage request and not a reason to hold the submission.

HASH-END: all five files recomputed at 22 Nov 2026 23:00 (Get-Date clock of the shell) after the last read; all unchanged and equal to the start values.
