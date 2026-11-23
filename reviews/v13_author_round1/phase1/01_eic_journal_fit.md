# Phase 1: blind full review, seat EIC (Journal-Fit Reviewer)

## 1. Header

- **Seat:** EIC, Journal-Fit Reviewer (author-round v13 panel). **Card:** "Card 1: Journal-Fit Reviewer (internal role EIC)", `review_v13_output\00_phase0_field_analysis_and_cards.md` (only the card and the field analysis were read there). Focus anchors re-pointed to the brief's sections: Section I (contributions, Scope, self-containment sentence); III; IV-B and IV-E; V-B to V-E; VI; VII; ACKNOWLEDGMENT; references; supplement as far as main-text pointers send a reader there.
- **Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`). Skill standards: `academic-research-skills:academic-paper-reviewer`, mode full, one seat only. No sub-agents, no web, no manuscript text sent anywhere.
- **Card-confirmation pause not held** (non-interactive run).
- **Read at start (SHA-256 checked against the brief; all five match):**
  - `MANUSCRIPT_v13.md` 29125167b108bc27833c16e3b639cbb07af5f4c105c49d375deff3d5b4a951d0
  - `MANUSCRIPT_v13.tex` bd4d08d954d3595de2b5ac2653c18476c7bb3281e1c264604f995f018da01345
  - `SUPPLEMENT_v13.md` fab98c1fe24c8c5b95f86da8b1e664662401055232409a236d963938f5b99a09
  - `MANUSCRIPT_v13.pdf` 4fabfd9f611013fd4e7f60b8a59fcdcc2d782dbd3192a77c2efe54e77beb8299
  - `SUPPLEMENT_v13.pdf` a8ad36027dee70c8c48cf2b998cb2512b55ca568c400eb1ecd340923ddeb8b16
  - Template `ojits-template.tex` (938 lines), read in full.
- **Hashes at end:** see the last section ("Hashes at end"), filled after the last read.
- **Pages viewed (as images):** manuscript `page01.png` to `page13.png` (13 of 13); template `tpl01.png` to `tpl09.png` (9 of 9); supplement `sup01.png` to `sup03.png` (3 of 3). All three folders were populated. Supplement text beyond its first pages was read from `SUPPLEMENT_v13.md` only where a main-text pointer needed it (S2, S4, S8, S12, S13, S15 passages).
- **Not read (blinding):** response letter, manifest, earlier panels, other seats, notes, diff files, TEXT_FREEZE, RECOUNT_COVERAGE, DERIVED, OUTCOMES, anything named `<excluded folder 1>` or `<excluded folder 2>`. The Phase 2 file was not opened before this file was written.
- Time of writing: 22 Nov 2026 18:46 (Get-Date).

## 2. Recommendation and score

- **Recommendation: major revision.**
- **Score: 5.8 / 10; 2.9 stars out of 5.**
- **Most likely OJ-ITS editorial outcome:** major revision, with a real chance (about one in three) of reject-and-resubmit if reviewers weigh simulation-only evidence and an already-null headline result. A desk-reject on the AI paragraph alone is unlikely (about 5%, Q8); a desk-reject on scope, density and the process story together is possible but not the modal outcome.
- **No CRITICAL finding.** Nothing alone justifies rejection.
- **Single change that would raise my score most:** decision-level evidence on real logs with room (type A); that cannot be had by editing. The doable change with the largest effect is a rewritten abstract and Section I that give the one-sentence answer first and tag every number with its status (type W), plus the Q6 insertions (type M).

## 3. Findings

Types: W wording; M a value moved in from the supplement (named); T text the author writes from existing records; A new analysis or evidence. A finding is REQUIRED only if I would withhold "accept" without it.

### 3a. REQUIRED-major (3)

| ID | Location | Finding | Evidence quoted | Fix (fewest words) | Type |
|---|---|---|---|---|---|
| J1 | Abstract (p.1); Section I contributions 2 (p.2) | The abstract opens with background, ends with the bottom line, packs about fourteen numerals into one paragraph, and does not tell the reader which numbers are confirmatory, which passed an amendment and which are descriptive. The 4.6% figure is listed among "three lead-braking tests" but is a descriptive value (Table 3), not the tested twin difference. | First sentence: "In autonomous driving, a multi-object tracker's covariance (its uncertainty) can serve as a motion planner's safety margin." Last: "the results do not justify removing a covariance margin." List: "it recovers 2% to 5% of the room: 2.8% under random detection dropouts (replicated; about 5% at higher rates), 2.2% for a two-noise interacting-multiple-model tracker, and 4.6% for a noise-adaptive filter." Body: "a small 0.0459 [0.0390, 0.0533] (Table 3; descriptive)". | Lead with the answer ("a tracker's covariance did not beat a class-average margin where it is nearly constant; where it varies it recovered at most about 5% of the room, and a missed-update count matched the dropout gain"); then tag each number: confirmed / passed (amendment) / descriptive; use the tested adaptive-twin difference (0.05) or call 4.6% descriptive; cut about four numerals; stay at or under 250 words. | W |
| J2 | Section I "The main text holds every result on which the claims rest" (p.2); Q6 cases C1 to C8 (Answer 6) | Eight places where a claim or contribution rests on a definition, method step or value that sits only in the supplement. The self-containment sentence is therefore not true as written. The author's earlier paper was rejected for this. | "The main text holds every result on which the claims rest; the supplementary material holds the configuration, the text of the plans, the full tables behind the summaries given here, and the verification record." | Bring in the facts listed per case in Answer 6 (each one or two sentences or a table row), or soften the sentence. | M |
| J3 | ACKNOWLEDGMENT (p.11); Section II "Novelty, with its limits" (p.3) | The text says Claude "ran the literature searches" but never says who verified that the 47 references exist and say what the paper says. The supplement says no full text was opened and statements "stay within those abstracts". A fabricated-reference worry is the likeliest real trigger of an editorial or reviewer reaction to the AI paragraph. | Ack: "ran the literature searches, and drafted and revised the text of all sections". S13: "no full text was opened"; "what the paper says about them stays within those abstracts." | Add one sentence to the ACKNOWLEDGMENT and one clause to Section II: the author checked every reference against its Crossref or publisher record, and state how many were read in full and how many at abstract level (S13 has the facts). Author must confirm the counts. | T |

### 3b. REQUIRED-minor (14)

| ID | Location | Finding | Evidence quoted | Fix | Type |
|---|---|---|---|---|---|
| m1 | ACKNOWLEDGMENT, pp.11-12 (Q7-1) | Order is wrong: AI disclosure precedes data and code availability. Required order: responsibility, data and code, AI disclosure, competing interests and no human subjects. | Paragraph 1 holds responsibility plus "Generative AI was used and is disclosed here under IEEE policy."; paragraph 2 begins "The deposit holds the plans, locks, and manifests". | Move the deposit paragraph up; make the AI disclosure its own paragraph third. | W |
| m2 | Fig. 2, p.7 (Q7-2); template 393-396 and tpl04 "Subfigure Labels" | Two-panel figure has no (a) and (b) labels; caption says "Right:". Fig. 4 has them. | Caption: "Right: the cut-in event window". | Add (a), (b) under the panels; caption "(a) ... (b) ...". | W |
| m3 | Abstract and Sections I, II (p.1, 2, 3); IV-E (Q7-3); template 195-197 | Prefix rule: "multi-object" should be "multiobject"; "mid-rank" should be "midrank". | "a multi-object tracker's covariance"; "the reading of the oracle's mid-rank". | Join the prefixes (reference titles [31], [32] stay as published). | W |
| m4 | Section II run-in heads (p.3), Section VI run-in heads (pp.10-11) (Q7-4); template 378, 393 | Run-in bold heads at subsubsection level are in sentence case; template subsubsections are title case. | "Perception judged by its effect on decisions."; "Why the fixed-noise covariance carries no measurable decision value on the nominal runs." | Title case, or turn into plain paragraphs. | W |
| m5 | V-E, p.8 (Q7-5); template 180-181 | "while" used contrastively, not for simultaneous events. | "most of the gain, while among those decisions alone its share of their own room is 0.009" | "whereas". | W |
| m6 | Table 1, p.2 (Q7-7); template 63 | NIS is used before it is defined (defined only in III-D, p.4). | Table 1: "NA, output-scalar NIS inflation ... $\overline{\mathrm{NIS}}/2$"; III-D: "normalized innovation squared (NIS)". | Define at Table 1 or at first use. | W |
| m7 | V-E adaptive filter, p.9; Table 6 row "Adaptive filter, share minus permuted twin's: fresh" | The first adaptive-twin test is labelled "(A)" although it was specified after the filter's values were seen, which Table 1 says an amendment test is not ("locked before its own values"). | V-E: "first in a test specified after its fresh share, oracle, and ratio spread had been seen"; Table 6: "(A), post hoc". | Label the fresh-run test "post hoc, descriptive"; keep "replicated" for the new-run test. | W |
| m8 | V-E coast-count, p.9; abstract; Table 6 | Interval excludes zero on the coast-count side, so the crude margin recovered slightly more, not "as much". Text understates. | "It recovered as much of the room (0.0322 against 0.0298; difference −0.0024 [−0.0057, −0.0001]". | "slightly more (by 0.0024)"; abstract "reproduces" can stay. | W |
| m9 | Section I (p.2), V-E (pp.8-10), VI (p.10), VII (p.11) | "Level effect" is a coined key term and is never defined; VI states flatly that the nuScenes result is a level effect where V-E says "partly". | "the dropout gain is a level effect"; V-E: "this too is partly a level effect"; VI: "these are level-type effects." | Define once in IV-C or Table 1 (a margin larger on all decisions of a state class, with no ranking inside it); make VI say "partly". | W |
| m10 | Abstract and VII; Table 5 | The braking-prediction share is quoted as one number although Table 5 shows it depends on the recording policy. | Abstract: "A braking prediction recovers 78% of the lead-braking room." Table 5: "0.379 / 0.837 / 0.783". | Add "(38% to 84% across run sets)". | W |
| m11 | Abstract (p.1) | Abstract gives the prediction model but not the planner, and not the interface limit of the IMM result. | "2.2% for a two-noise interacting-multiple-model tracker"; Scope: "longitudinal decisions of one margin-type speed planner". | Add "one longitudinal speed planner" and "through a position-velocity interface" (trim elsewhere). | W |
| m12 | IV-E (p.5) and ACKNOWLEDGMENT versus S12 | Recount scope is stated two ways. | IV-E: "recount every value printed in the main text and all but the marked (‡) values of the supplement"; S12 first paragraph: "Every value printed in the Abstract, Sections I and V–VII, the main tables and figure captions, and every supplement value they cite". | Make S12, IV-E and the Ack say the same, and name the sections and the supplement scope. | W |
| m13 | ACKNOWLEDGMENT, p.11 (Q8) | Three wording points: "made every scientific decision" sits against "where the amendment files record a design choice as an AI session's"; the AI review-panel system is not named; the Limits calls the planner "in-house" while the Ack says Codex developed it. | "The author conceived the study, set its questions and plans, made every scientific decision"; "the presubmission review by an AI panel"; VI: "one in-house planner". | Use "decided the questions, accepted or rejected each design option, and approved all results"; name the panel's model(s); say "one planner written for this study". | T |
| m14 | Tables 2, 4, 6, pp.7, 8, 11 (Q7-6); template 518-519 | Table footnotes are symbols inside the caption, not letters under the table. | "†Contacts from behind are not counted"; "\*Not computed"; "(†) nominal 99%". | Footnote letters in a note row under each table. | W |

### 3c. OPTIONAL (13)

| ID | Location | Finding | Evidence quoted | Fix | Type |
|---|---|---|---|---|---|
| o1 | Whole paper | 13 pages against the field-analysis target of about 10; V-E and IV-E are the densest paragraphs (V-E runs about two pages of near-continuous numerals). | Page count (pages 1-13); Section V-E pp.8-10. | Compress V-E and IV-E prose; keep Table 6. Mind J2: do not push content out. | W |
| o2 | References [9], [13], [15], [21], [34] (Q7-8); template 495 | "et al." where names are available. IEEE manual allows it beyond six authors, template says list all. | "H. Caesar *et al.*, "nuScenes ..."" | List all authors or keep if each has more than six. | W |
| o3 | 15 conference references (Q7-9); template 722-723 | No city, state, country. | "in *Proc. IEEE Intell. Veh. Symp. (IV)*, 2018, pp. 1171–1178" | Add locations if the style is enforced. | T |
| o4 | Tables 1-6 (about 7 pt, \scriptsize), Fig. 1 box text (about 6 pt) (Q7-10); template 390-391 | Below the 8 to 10 pt that the template gives for figure labels. | Pages 2, 4, 7, 8, 9, 11. | Enlarge Fig. 1 text; consider 8 pt in tables. | W |
| o5 | Byline, running head, [10] (Q7-11) | Three name forms: full byline, "Kopalli Naga Venkata", "A. S. K. Kopalli". | Page 1; page 2; [10]. | Use one form so the self-citation is recognisable. | W |
| o6 | [5], [15], [32], [40] (Q7-12) | arXiv IDs carry a version in some entries (v2, v1, v6) and not in [32]. | "arXiv:2606.03590v2"; "arXiv:2001.05673". | One convention. | W |
| o7 | Table 1 rows NA and AM; Fig. 1 | Defined but never reported in the main text. | "NA, output-scalar NIS inflation ... Descriptive"; "AM, acceleration margin ... Descriptive". | Drop from Table 1 and Fig. 1 or point to S5. | W |
| o8 | Abstract | 245 whitespace-separated words; a hyphen-splitting counter gives over 250. | Word count 245. | Trim 8 to 10 words (J1 does). | W |
| o9 | Table 5 cells, p.9 | "costs progress (5.3, 0.0)" is cryptic; the two numbers are not labelled in the cell. | "Behind leads that keep their speed: CK3; PS (caution, wrong-go differences, points)". | Split into two columns with headers. | W |
| o10 | Table 6 versus IV-E | Slope is "on the dropout rate" in the table and "on the start probability" in IV-E. | "slope of that share on the dropout rate"; "the slope of the dropout share on the start probability". | One name. | W |
| o11 | Section I Scope, [10] | A manuscript under review elsewhere shares detector, tracker and margin form; the paper says so, but the cover letter should too (template 599-600 asks for disclosure of current submissions). | "under review ... shares this paper's detector architecture, tracker configuration, and margin form". | One sentence in the cover letter. | T |
| o12 | Captions of Tables 2, 4, 6 (seven lines each) | Captions carry method rules; heavy for a table title. | Pages 7, 8, 11. | Move rules to the text. | W |
| o13 | Back matter | No author biography yet; optional at submission (advisory). | n/a | Add at acceptance. | T |

## 4. The eight answers

### Answer 1. Labels and sizes

Mostly right. Checked item by item:
- "Confirmed" is used only for the original plan: V-A (room, detection in a +/-5% band, tracker equivalence, braking-prediction share above 0.5, per-phase schedule transfer) and V-B (IMM classification). Nothing in V-E is called confirmed.
- Amendment tests carry "passed (amendment)" (closed loop with dropouts, nuScenes mechanism check), "recovers (A)", "replicated" (new runs) and "failed" (coast-count; equal time lost). The Table 1 legend defines (A).
- Holm sits beside the labels and changes none: six second-amendment primaries (Table 6 H rows: 0.0079, 0.0079, 0.0003 four times), and separately the third amendment's two controls (Holm 0.99 and 0.18), both failed. V-E and IV-E say the same.
- Sizes: effects are called "small", point values are compared with the +/-5% margin, and "equivalent here does not mean safe" is stated.

Misses: the first adaptive-twin test is labelled (A) although specified after values were seen (m7); the abstract's 4.6% is a descriptive value listed among tests (J1); the coast-count difference interval excludes zero but is described as "as much" (m8); the 78% is quoted without its run-set range (m10).

### Answer 2. Overreach

- **Dropout gain source:** handled. "A margin that only counts missed updates reproduces the dropout gain" and "a level effect that needs no per-decision covariance" are supported by the failed control. Residual: m8 (slightly more) and m9 (level effect undefined).
- **Closed loop:** handled. "matched only in design caution" is disclosed; the equal-time-lost comparison is shown and failed; "its fewer contacts might come from a wider margin". The comparison uses three scales of the class-average frontier, so "not shown" is the right strength. Residual: the abstract still leads with "(21% against 33%)", fine since it adds "were not shown at equal time lost".
- **nuScenes mechanism check:** handled. Training-split population choice is disclosed; "slightly inversely over all tracks" is in the abstract; the primary pairs "mostly compare missed with steady tracks". Residual: VI states "these are level-type effects" more firmly than V-E (m9).
- **Real-log decision test:** "found no room" is stated in the abstract, V-A, V-E, VI and VII. Fine.
- **Two-noise IMM:** interface caveat appears in V-E and VI, not in the abstract or conclusion (m11).
- **Scope of the null:** prediction model (constant velocity) is in the abstract; planner scope (one longitudinal speed planner) is not (m11).
- **Also:** "adds nothing" in the abstract is stronger than the confirmed result (share within [-0.09%, 0.15%] of the room, equivalence within 5%); the bound is next to it, so this is a style point only.

### Answer 3. Earlier limits

| Limit | Status | What remains |
|---|---|---|
| (a) closed loop matched only in open-loop caution | Addressed | Equal-time-lost comparison shown and failed (-0.05 [-0.12, 0.02]); text says the fewer contacts "cannot be told from a wider margin". Only three frontier scales were used; stated. |
| (b) dropout gain may be a coasting margin | Addressed | Coast-count margin recovered 0.0322 against 0.0298; abstract says it reproduces the gain. Wording (m8). |
| (c) abstract and conclusion stronger than body | Partly | "only where it varies", "where it tracks the error", "shows on real data" are gone. Remains: statuses untagged in the abstract, 4.6% descriptive, 78% without range, planner and interface scope (J1, m10, m11). |
| (d) two-noise IMM interface | Partly | Stated in V-E, VI. Not in the abstract or conclusion. |
| (e) Holm and recount scope | Partly | Holm scope is clear and correct. Recount scope is stated two ways (m12). |
| (f) density; round-2 only in supplement | Partly | Round-2 results are now in V-E and Table 6. The price is density (o1) and the self-containment cases (J2). |
| Structural: near-constant covariance, a confirmed result that could hardly fail | Acknowledged, not fixable | The paper says it was "expected from its near-constancy" and that "what the test adds is the bound". |
| Small positive effects | Acknowledged | Labelled small, inside the +/-5% margin. |
| One simulator, one configuration | Acknowledged | Limits paragraph and abstract. |
| No decision-level real-log evidence | Acknowledged, not fixable | "no room"; a next step. |
| Process: amendments after results, local hash locks, AI authorship | Disclosed | IV-E names the internal locks, "no third-party timestamp", 21 of 60 departures after results, and the AI panel; the Ack discloses AI use. |

### Answer 4. Readability

- **Abstract:** the bottom line is not first (J1). It is dense, with undefined-in-place terms ("room" is glossed; "wrong-go", "equal caution", "coast" style phrases are not).
- **Coined terms:** most are defined once (Table 1 is a real glossary). Exceptions: "level effect" (m9); "mid-rank" (C8 below); "preregistered" is in the title and defined only at IV-E on p.5, though the abstract's "hash-locked internally" does the job. NA and AM are defined and never used (o7). NIS comes before its definition (m6).
- **Finding evidence:** each headline claim has a main-text table or figure (Tables 2 to 6, Figs. 2 to 4), except the eight Q6 cases.
- **Journal fit and significance:** the topic fits OJ-ITS (perception-to-planning safety evaluation). The take-away for readers is useful but modest: a null in the confirmed test, small effects where the covariance varies, a large effect from a braking prediction. Novelty is claimed with limits (II) whose limits are only in S13 (C7).

### Answer 5. Verdict

- **Recommendation:** major revision. **Score:** 5.8 / 10; 2.9 stars.
- **Likely outcome at OJ-ITS:** major revision (see Section 2).
- **Single change raising the score most:** real-log decision-level evidence (A); doable now: J1 plus J2.

### Answer 6. Self-contained main text: 8 cases

| # | Main-text location | Rests on | Fact to bring in | Type |
|---|---|---|---|---|
| C1 | V-E p.9 and contribution 2 (Section I): "A two-noise IMM, with a quiet constant-velocity mode and a maneuver mode tuned on braking (Supplement S15)" | S15 "The two-noise IMM", Table S41 | Quiet mode is the CV filter of record; maneuver mode is a CA filter with acceleration variance 0.917 (‡), tuned so the median NIS over braking frames is 1.997 (‡); transition diagonal 0.95; own class average. | M |
| C2 | III-D p.4; V-B and V-E: "a CV filter whose velocity process noise follows its recent NIS both ways" | S4 "Adaptive process noise" | Velocity-block noise scaled by clip(m, 0.25, 10), m the mean of NIS/2 over the last (at most 3) position updates. | M |
| C3 | V-E p.8 and VI: "An exploratory decomposition (R² 0.47; decision-level R² 0.06; Supplement S15) attributes 54% ... 38% ... 8%" | S15 "Why the covariance varies in pedestrian crossing", Table S46 | Regression of the log ratio of covariance margin to class margin on three groups (geometry, update schedule, realized error) over 58,970 decisions of 366 runs; shares are Shapley shares. | M |
| C4 | V-E p.10: "asks whether the covariance's predicted 3 s position spread ranks the realized error within scene and keyframe" | S15 "The real-log mechanism check", Table S45 | Realized error = error of the 3 s constant-velocity prediction; Kendall's tau within scene and keyframe; "all pairs" versus "around misses" strata. | M |
| C5 | V-C p.6: "By the plan's classes the braking prediction is inconclusive behind leads that keep their speed or brake mildly and is safer at a cost ...; the per-phase schedule has the same classes (Supplement S9)" | S9 (contact differences and intervals behind nonbraking leads) | The contact differences with intervals for the 60 nonbraking closed-loop cases (one added block in Table 4). | M |
| C6 | V-D p.8 and Table 5 "costs progress" rows | S8 (rule and intervals) | The rule that gives "costs progress" and the intervals, e.g. CK3 "5.3 [2.7, 8.5]; 0.0 [0.0, 0.0]". | M |
| C7 | II p.3 "In the sources we searched (Supplement S13)" | S13 | The limits of the search: English only, one engine blocked, abstract-level reads, IMM and adaptive-filter literature not searched for a planner-side test. | M |
| C8 | IV-E p.5 "the reading of the oracle's mid-rank where the plan read two ways" | S2 "The amplitude-matched ranking oracles" | Definition: mid-rank u = (rank - 0.5)/n_r over decisions with such rows (0.5 without); the departure is the denominator. | M |

Pointers that only offer more detail (S1 configuration, S3 plan text, S5 full tables, S6, S10, S14) are not cases.

### Answer 7. IEEE OJ-ITS format and declarations

Template line numbers cited from `ojits-template.tex`.

**Misses (9, with locations):**
- Q7-1 ACKNOWLEDGMENT order wrong (pp.11-12; m1).
- Q7-2 Fig. 2 has no (a), (b) sub-figure labels (p.7; template 393-396; m2).
- Q7-3 "multi-object" (abstract p.1; Section I p.1; Section II p.3, several times) and "mid-rank" (IV-E p.5): template 195-197 (m3).
- Q7-4 Run-in subsubsection-level heads in sentence case: II (4 heads, p.3) and VI (4 heads, pp.10-11); template 378, 393 (m4).
- Q7-5 "while" for contrast, V-E p.8; template 180-181 (m5).
- Q7-6 Table footnotes as symbols in captions (Tables 2, 4, 6); template 518-519 (m14).
- Q7-7 NIS undefined at first use (Table 1, p.2; m6); template 63.
- Q7-8 "et al." in [9], [13], [15], [21], [34]; template 495 (o2).
- Q7-9 Conference references omit city, state, country; template 722-723 (o3).

**Advisory (3):** text and figure size below 8 pt (o4), three name forms (o5), arXiv version convention (o6).

**Checked and fine:**
- Section and subsection heads are in capitals on every page image (I. INTRODUCTION to VII. CONCLUSION; A. SIMULATED RUNS to F. MARGIN SOURCES, and so on).
- "Fig. N" in running text, "FIGURE N." in captions; "Table N" in text, "TABLE N." in captions, Arabic numbers (consistent with the rendered template; template line 424 still says Roman, which the brief rules out as a miss). Supplement first pages use "TABLE S1.".
- American spelling, serial comma, periods and commas inside closing quotes: no miss found. No contractions. "Preregistered" has one spelling in the title and IV-E.
- Funding is in the first-page footnote; no Funding heading.
- One ACKNOWLEDGMENT section, singular heading, spelling "ACKNOWLEDGMENT" (template 472-478); order is the miss above. Competing-interests and no-human-subjects sentence present.
- First page: author, affiliation, ORCID, corresponding author with e-mail, running head with the short title and surname on the even pages (2, 4, ..., 12), with the OJ logo band on odd pages, as in the template.
- References: initials, titles in quotes, italic abbreviated venues, volume, number, pages, year, DOI; arXiv as "year, arXiv:ID."; [4] has "Accessed:"; [10] says "submitted for publication" with no journal.
- Index terms: 5, alphabetical. Abstract: 245 words, no abbreviations. Tables fit column (Table 1) or page (Tables 2 to 6). Caption placement matches template 448-449. Fig. 2 to 4 axis labels use words and units in parentheses.
- Placeholders (repository and DOI) and publisher-filled lines are not counted.

### Answer 8. AI disclosure

- **Does it meet IEEE's rule?** In substance yes: it names the systems and models (Claude: Opus 5.5, Fable 5.2, Sonnet 5.5; Codex: GPT-6.1 Sol, GPT-6 Astra, GPT-6.2 Astra), the scope ("all sections", the supplement, analysis, simulation-control and figure code, literature searches, amendment plans) and the level (drafted and revised all text; wrote code; the author chose, corrected, directed). Gaps: the AI review panel's system is not named; no statement on reference verification (J3); placement and order (m1).
- **Would an editor desk-reject on it?** Unlikely, about 5%. The rule asks for disclosure, and this is disclosure; nothing names an AI as author. The real exposure is cumulative: AI-drafted text, AI-run literature search, AI review panel, local hash locks, and amendments after results. An editor or referee who dislikes that stack may use it as a reason to be harsh; the paragraph does not create it.
- **Facts checked against the paper:**
  - Second programs written in separate Claude sessions, sharing the scoring library, arrays and draws: matches IV-E and S12 ("a different model from the writer's"). The scope of the recount differs between sources (m12).
  - Audit by Fable 5.2 then Sonnet 5.5 (S12): S12 has a "Claim audit" paragraph by "an agent on a model other than the writer's"; it covers the Abstract, Sections I and V-VII and the main captions, not the whole paper.
  - "The AI systems also drafted the amendment plans": consistent with IV-E ("each after a report of an artificial intelligence (AI) review panel"; the third's controls "were asked for by that panel").
  - "made every scientific decision" against "where the amendment files record a design choice as an AI session's": a reader may see tension (m13).
  - "Codex ... developed the simulation, recording, and planner software" against VI "one in-house planner": reword (m13).
  - "The requests and responses of the presubmission reviews are deposited": the deposit is the repository-and-DOI gate.
  - The model names and Codex role cannot be checked inside the paper; nothing in the paper contradicts them.
- **Wording that lowers risk without understating use:**
  1. Own paragraph, third in the ACKNOWLEDGMENT, headed by one plain sentence: "Generative AI was used as follows, in line with IEEE policy; no AI system is an author."
  2. Keep the specifics (systems, versions, sections, level). Replace "made every scientific decision" by "decided the research questions, accepted or rejected each design option, and approved all results".
  3. Add: "The author checked every reference against its Crossref or publisher record; [N] were read in full, the rest at abstract level (Supplement S13)." (author must confirm N.)
  4. Name the system used for the AI review panel and say the reviews and responses are deposited.
  5. Move the recount description to IV-E (already there) and shorten the Ack by about a third.

## Hashes at end

Re-computed at 22 Nov 2026 18:48 (Get-Date) after the last read; all five package files unchanged and equal to the start values:
- `MANUSCRIPT_v13.md` 29125167b108bc27833c16e3b639cbb07af5f4c105c49d375deff3d5b4a951d0
- `MANUSCRIPT_v13.tex` bd4d08d954d3595de2b5ac2653c18476c7bb3281e1c264604f995f018da01345
- `SUPPLEMENT_v13.md` fab98c1fe24c8c5b95f86da8b1e664662401055232409a236d963938f5b99a09
- `MANUSCRIPT_v13.pdf` 4fabfd9f611013fd4e7f60b8a59fcdcc2d782dbd3192a77c2efe54e77beb8299
- `SUPPLEMENT_v13.pdf` a8ad36027dee70c8c48cf2b998cb2512b55ca568c400eb1ecd340923ddeb8b16
- Template `ojits-template.tex` 770ddac436bfa2609e8f436c66c70ccf0b88d478e72b2493bced8dc4b188ced2
