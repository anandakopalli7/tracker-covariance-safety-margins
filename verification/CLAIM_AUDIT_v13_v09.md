# Claim audit v09 of the sprint text (A10 §10.3, extended by A11)

- **Auditor:** Claude Fable 5.2 (`claude-fable-5-2`). The writer is Claude Opus 5.5.
- **Written:** 21 Nov 2026, after the coordinator's 19:50 update.
- **Input audited:** `work\A_text\out\audit_v09b_input\` (build report 19:43:21, PASS). I started on `audit_v09_input\` and switched when the update arrived. The two differ only in the abstract's A11 sentence, Table S5's word-budget row, the letter's word counts and the matching `DERIVED` entries; I checked this by diff.
- **Also read:** A10 (§0, §2, §5.3–5.4, §6, §7.5, §8.5, §9, §10), A11 in full, STATUS "Now", the focus list (items 1–10), both results interfaces, the two crossing deviation files, and the exports of X, DR, Y, B and E4 (data only).
- **Not read:** `gen\`, `build\`. Nothing was built or edited; no external service was used.
- **One comparison beyond the brief:** the manuscript of `out\freeze_v13_1301\` against the audited one, to test Table S5's statement that no existing text was cut (finding 1).

**Counts: 2 H, 11 M, 14 L.**

**Numbers.** Every result token in the title, Abstract, §I, §V–VII and the main captions has a `DERIVED` source at the printed rounding (a script found none without one; the only unmatched tokens are rule constants: 75%, 0.5 s, 1.5 s). Every sprint value in §V-E, Table III's addendum row, S14 and the abstract matches its export key, and its recount agrees. No number is wrong. Both H findings are statements about the document or a table, not result values.

## 1. Findings

Checks: 1 number, 2 wording rule, 3 label, 4 claim beyond its rule.

| # | Location | Sentence (quoted) | Check | What it breaks | Rating | Fix, fewest words |
|---|---|---|---|---|---|---|
| 1 | Table S5, word-budget row | "no existing text was cut for the new results, and one exploratory figure moved to the supplement" | 4 | Not true. Against the 13:01 freeze, existing text was shortened to fit: the captions of Tables II–IV and Figs. 1–2, Table I (merged), the abstract (e.g. "at 10 Hz and 0.1 s the after-stop room is 45% of its 2 Hz value", "as is the time gap"), §VI ("the largest pooled share of any tested covariance margin"), data availability. STATUS itself lists "Trims for 10 pages" | H | "existing captions, Table I and the abstract were shortened, and one exploratory figure moved to the supplement" |
| 2 | S14, step-0 paragraph | "The covariance's share is near zero or below, while its own amplitude-matched ranking oracle recovers much of the room: the pattern of uninformative variation, on stored runs, not a test." | 1, 4 | Table S31 does not show this for vehicle crossing: N 0.165 [−0.020, 0.497] against its oracle 0.226 [0.115, 0.833] (N at about 73% of its oracle). For pedestrian crossing the oracle's interval is [−1.249, 0.860], so "recovers much" is a point value only | H | "In pedestrian crossing the covariance's share is below zero and its oracle's point share 0.64, both with wide intervals; in vehicle crossing the two are close. Stored runs, not a test." |
| 3 | §VII, sentence 1 | "in closed loop with dropouts it was equivalent to the class average and, at the higher level (secondary), safer at no extra cost" | 2, 4 | A11 §6d: the arms are not caution-matched and no equal-caution claim is made; focus item 9 requires the caveat at every mention. Here N also loses 0.25 s [0.15, 0.36] at the higher level, so "safer" without the caveat reads as an equal-caution gain | M | Insert "(not caution-matched)" after "with dropouts" |
| 4 | §V-B, second paragraph | "having no permuted twin, it does not separate information from jitter" | 2 | Contradicts §V-E and the abstract: the twin test now exists and passed (Y1, 0.0498 [0.0424, 0.0569]) | M | Replace the clause with "its permuted twin is tested in Section V-E" |
| 5 | §V-E, the dropout sentences (and S14) | "under dropouts there is room … recovers 0.0283 [0.0064, 0.0496] of it" | 2 | A11 §6c.11: "Whatever the class, the result is not extended beyond lead braking under this mask law and output rule". No such sentence exists in the manuscript or the supplement. §V-E also never says this test is open loop (only the abstract and Table S32 do) | M | "under dropouts (open loop; lead braking, this mask law and output rule only) there is room" |
| 6 | §V-E, bottleneck sentence (focus 6) | "It carries none in pedestrian crossing and little under dropouts of the rank information its amplitude would allow: the bottleneck is the information in the covariance, not its amplitude." | 3, 4 | For crossing this is A11 §3.8's row. For dropouts the class is "recovers", whose row gives only r and r/c; the bottleneck clause there is session A's reading and is not labelled as one. "Would allow" is bound language for an oracle that §IV-C calls "a reference, not a bound" | M | "It recovers none in pedestrian crossing and, under dropouts, 7% of what its amplitude-matched oracle recovers: we read the bottleneck in both as the information in the covariance, not its amplitude." |
| 7 | §I, contribution 2 | "an interacting-multiple-model tracker as tuned here barely varies; where it varies more, it varies without rank information in pedestrian crossing and recovers 2.8% of the room under dropouts" | 4, 2 | "it" now refers to the IMM, which was not tested in crossing or open-loop dropouts. The coordinator's wording for dropouts ("small", inside the margin) is dropped under the heading "A confirmatory test" | M | "where the fixed-noise covariance varies more, it … recovers a small 2.8% of the room under dropouts" |
| 8 | Abstract (focus 10) | "it varies without rank information in fresh pedestrian crossing (a small room, 0.16 points)" | 4 | With the oracle's share dropped, the abstract keeps only the strong half of A11 §3.8's row. What was shown is a share of −0.067 [−0.221, 0.034], not inside the margin, on a 0.16-point room: "recovers none", not an absence of information | M | "it recovers none of a small room (0.16 points) in fresh pedestrian crossing" (one word fewer) |
| 9 | S14, Tables S32–S34 (and S4) | "(C) confirmed in its sequence" | 3, 2 | The second hypothesis of each sequence (detection at the tracker's amplitude) is neither stated nor printed, so "confirmed" for the third cannot be checked by a reader. Values exist and pass: crossing oracle minus twin 0.591 [0.382, 0.941]; dropouts 0.253 [0.214, 0.296]. The crossing counts are also missing everywhere (390 runs, 105,419 decisions, 1 contact run; A11 §3.6) | M | Add rows to Tables S33 and S34: "Oracle minus its permuted twin … (C)"; to S33: "Runs; evaluated decisions; contact runs" |
| 10 | S14, Table S35 | Caption: "…at the locked settings (lower level primary, higher level secondary); not caution-matched." | 2 | A11 §6d: "with the open-loop caution difference reported"; §6d.5: each arm's design caution, and the open-loop difference under dropouts or "not computed". Neither is printed (the export has the design cautions: 14.10 / 14.19 and 22.30 / 22.32) | M | Add to the caption: "Design caution F0 / N: 14.10 / 14.19% (lower), 22.30 / 22.32% (higher); open-loop caution difference under dropouts: not computed" |
| 11 | S14, Table S35, last row | "N, against its runs without dropouts, relative to F0 (higher level; exploratory: it crosses the masks and the output-rule change) −0.10 [−0.18, −0.03]" | 3, 4 | Label and caveat are present. But only one of four pre-specified differences-in-differences is printed, the one whose interval excludes zero. The primary level's is −0.02 [−0.05, 0.00]; the IMM's at the higher level −0.05 [−0.13, 0.02] | M | Print all four in the row, or add the lower-level value beside it |
| 12 | Letter, "Added at the end." | "A later amendment, locked before any of its fresh values, added a pedestrian-crossing test, … detection dropouts on the lead-braking runs, … the adaptive filter against its own permuted twin and an IMM re-tune" | 2, 3 | The letter gives the lock and none of the required disclosures: crossing tested despite the no-go; dropouts, the twin test and the re-tune specified after the fresh lead-braking results were seen (A11 §2, §6, §6b, §6c.11). "Locked before any of its fresh values" alone reads cleaner than the record | M | Add: "Crossing was tested despite a pre-stated no-go, and the dropout test, the twin test and the re-tune were specified after the fresh lead-braking results were seen (Table S5)." |
| 13 | Table S5, grid-placebo row | "the placebo at the lead-braking median is reported beside it" | 4 | No crossing placebo value is printed anywhere in the supplement (Table S33 has none; the export has both: −0.003 and −0.005) | M | Add a row to Table S33 ("Grid frontier: N; placebo; placebo at the lead-braking median"), or change to "is in the deposit" |
| 14 | §V-E | "(a nominal 99%% interval, the plan's fallback)" | — | Doubled percent sign in the Markdown; check the PDF | L | "99%" |
| 15 | §V-E | "but its own share is −0.067 [−0.221, 0.034] (confirmed)" | 3 | "Confirmed" hangs on a share; the class name of Table I is never given in §V-E | L | "(uninformative variation, confirmed)" |
| 16 | §V-E, abstract (focus 10) | "a small room" | 3 | The rule (below a tenth of lead braking's room) is stated nowhere in the text | L | S14, one clause: "small: below a tenth of lead braking's room" |
| 17 | §V-E; Table S32 caption | "(values in Table S32)"; "crossing: the oracle's at the nominal 99% fallback" | — | Table S32 prints no oracle share, efficiency or within-5% value, yet its caption gives the oracle's level | L | Add the oracle's share to S32's result cells, or point §V-E to "Tables S32–S34" |
| 18 | Table S5, calibration-step row | "It stopped twice in the linear-algebra library … (a crash that wrote no output)" | 3 | The caption promises a mark where a record was made afterwards; this one was written after the X results (crossing record X-9) | L | Add "recorded afterwards" |
| 19 | §V-E; Table S5, dropout row | "specified after the fresh lead-braking results had been seen" | 2 | A11 §6c.11 names the date (21 Nov 2026); neighbouring rows carry theirs | L | Add "on 21 Nov 2026" to the Table S5 row |
| 20 | Title | "An Equal-Caution Test on Simulated Lead Braking, Detection Dropouts and Pedestrian Crossing, Open and Closed Loop" | 4 | The title rule is met (X0 and DR0 pass). But the closed loop with dropouts is not caution-matched, and crossing is open loop only; the title can be read otherwise. The author decides the title | L | Leave; the Scope and §V-E carry both limits. Tell the author |
| 21 | Abstract | "carries rank information beyond its own permuted twin (specified after its share was seen: 0.0498 [0.0424, 0.0569])" | — | The value reads as the share that was seen; it is the difference from the twin | L | "…beyond its own permuted twin (by 0.0498 [0.0424, 0.0569]; specified after its share was seen)" (one word more; the abstract has three spare) |
| 22 | Abstract | "In open loop, where the covariance varies more, it varies…" | — | After the IMM and adaptive-filter sentence, "the covariance" is not clearly the fixed-noise tracker's | L | "where the fixed-noise covariance varies more" (one word more) |
| 23 | §V-E; §III-A | "In pedestrian crossing there is a small room" | — | The main text never says how many crossing runs were scored (390), and §III-A lists the fresh runs without them | L | §V-E: "In pedestrian crossing (390 fresh runs) there is…" |
| 24 | Tables S33, S34, S36 | "further details" | 3 | Their rows are descriptive at nominal 95% (A11 §3.6, §6c.7, §6b "beside it"), and the captions do not say so | L | Add "(descriptive; nominal 95%)" to each caption |
| 25 | Table S5, word-budget row; A11 rows | "Abstract at most 220 words, body at most 5,300 and the whole manuscript at most 8,500 (the plan's budgets)" | 2 | A10 §10.4's supplement budget (15,000) is missing from "Planned". A11 §6c.5's reading of A10 §2.2 (rank divided by the number of decisions that enter the ranking) has no row | L | Add "supplement 15,000"; one reading row, or fold it into the existing "definitions where the plan was silent" row |
| 26 | §VII | "recovered a confirmed but small 2.8% of the room … under detection dropouts" | 2 | The conclusion drops "open loop" for the dropout test (the abstract keeps it) | L | "under detection dropouts (open loop)" |
| 27 | §VI, Limits | "Magnitudes depend on the 2 Hz update, leads that brake to a stop and the recording policy" | 2 | A11 §3.8 "Always": the sprint's magnitudes carry conditions too (one synthetic mask law, the output-rule change, crossing in open loop with the tracker of record). Limits names none | L | Add: "the dropout results hold for one mask law and output rule" |

## 2. Focus items: verdicts

1. **B1r: pass, with a note.**
   - §V-B: "detectable" (r's lower end 0.0040 > 0), "very small" and "inside the equivalence margin" (upper end 0.0067 < 0.05), "about what its amplitude-matched ranking oracle recovers" (r − c = 0.0007 [−0.0009, 0.0021]) and "still barely varies" (99.4%) all match `B.IMMr.*`.
   - "Disclosed addendum, decided after the fresh results were seen" and "the registered classification stays the confirmatory result" are present. Table III labels the row "(addendum)"; Limits mentions it.
   - The abstract has **no** B1r clause (STATUS 19:35 says it keeps one; that note is stale). The conclusion has none. Neither the title nor any main claim rests on it.
2. **X, DR, Y, E4 wording: partly fails.**
   - Present and correct: the crossing departure sentence, verbatim; the dropout disclosure (specified after; re-scores those runs; output-rule change); Y's disclosure; E4's "not caution-matched" in the abstract, §V-E and Tables S32 and S35; the title rule.
   - Missing or wrong: the dropout non-extension sentence (finding 5); the caveat in the conclusion (3); the second hypotheses' results (9); E4's caution reporting (10).
3. **Table S5's A11 rows and the word-budget row: fail on two rows.**
   - The word-budget row's caps now match the build (16,200; supplement 15,903), but "no existing text was cut" is false (finding 1).
   - The grid-placebo row points to a value that is not printed (13).
   - Every other A11 row matches A11 and the crossing records X-4 to X-9 and X-11 (minor: 18, 19, 25).
4. **DR: numbers pass; wording fails in three places.**
   - Abstract, contribution 2, conclusion, §V-E and Tables S32 and S34 match `DR.RR_N(.ci)`, `DR.RR_E5N(.ci)`, `DR.eff(.ci)`, `DR.within5`, `DR.in.RR_N(.ci)` and `DR.ref3.*`. All intervals are nominal 95%, the level the export records.
   - "Inside the equivalence margin" is true by a small distance: the upper end is 0.04965 against 0.05. It describes the interval; no equivalence test was registered for dropouts, and the text does not say "equivalent" for it.
   - "Confirmed" is right: DR0, DR1 and DR2 passed in order.
   - Fails: the non-extension sentence (5), contribution 2 (7), the unlabelled bottleneck reading (6).
   - Worth knowing: the share among decisions inside a dropout is −0.003 [−0.020, 0.015], and with the row after the window 0.030 [−0.003, 0.063]. The text makes no claim about where the gain arises, which is right.
5. **Fig. 4: pass.** No main-text reference to Fig. 4 remains. The figure is Fig. S1 in Supplement S6. The letter says so twice ("three figures"; "moved to Supplement S6").
6. **The bottleneck clause: supported in substance, overreaches in form (finding 6).**
   - The printing rule is met: the class is "recovers" and the upper end of r/c is 0.129, below one half.
   - The data support "little": the covariance recovers 7% [2%, 13%] of what its amplitude-matched oracle recovers.
   - It overreaches in two ways. A10 §9's "recovers" row does not give this sentence, and the text does not mark it as a reading. "Would allow" treats the oracle as a ceiling, which the paper elsewhere denies.
7. **The abstract's ladder: pass, with a note.**
   - Present: the lead-braking room and N's interval, the per-phase schedule (92%), the braking prediction (78%), the crossing room (0.16), the dropout room (5.63) and share (2.8%), and Y's difference with its interval.
   - Absent: the size of the three detection controls (lead braking's, already absent in the 04:24 freeze; crossing's 69% and dropouts' 40%, dropped at 19:50). These are confirmed results. If the ladder's rule is read strictly, dropping the two oracle shares breaks it; the coordinator decided this, so I record it and raise no finding beyond 8.
8. **Y: pass.**
   - §V-E has the pass wording ("the same margins in random order within runs"), the difference with its interval, the small share (0.046), "on fresh lead-braking runs" and "a class constant there".
   - The disclosure names the share, the oracle and the ratio spread. Table S36 gives the fixed-noise reference, 0.0003 [−0.0001, 0.0011] (`Y.ref.delta`).
   - Contradicted by one stale clause in §V-B (finding 4); minor: 21, 24.
9. **E4: partly fails.**
   - Lower level primary, both comparisons "equivalent", from the right intervals. Higher level "secondary" everywhere; no sentence calls it confirmed. Classes match E's rules.
   - "Not caution-matched" is missing from the conclusion (finding 3).
   - **The coasting sentence ("more cautious exactly when the tracker is blind") is not in this build** (no match in the manuscript, supplement or letter). There is nothing to judge. If it returns, it needs the "interpretation" label, and it sits badly with the in-dropout share of −0.003 in open loop.
   - The difference-in-differences is labelled exploratory with its two-changes caveat, but it is printed selectively (finding 11). The caution reporting is missing (10).
10. **"A small room": the rule and its use are fair.**
    - The crossing room is 0.16 [0.11, 0.23] points, 2.9% of lead braking's 5.58; its upper end is still below a tenth. It is 170.5 decision-equivalents against about 1,204.
    - The rule is not stated in the text (finding 16).
    - No scenario lacks both its room and its oracle in the abstract: both rooms are printed.
    - "Varies without rank information" does read bigger than the small room and the null allow (finding 8).

## 3. Sentences checked without findings

- **Title.** Follows the confirmed title rule (see L 20).
- **Abstract.** Sentences 1–2 (equivalence, room, detection band); the IMM clause; the adaptive filter's 4.6% (descriptive); the dropout clause's numbers and labels; the closed-loop dropout clause; the braking prediction and schedule; closed loop (0.16 s); no room in cut-in and nuScenes; 2 Hz; "not justified". 247 words.
- **§I.** Paragraphs 1–3; contributions 1 and 3; Scope (crossing "in open loop only"; the related manuscript).
- **§IV-E** (read for the sprint sentence). The three later lock hashes match `LOCK:A11`, `A11b`, `A11c`.
- **§V-A.** All sentences; Table II and its caption; Fig. 2's caption.
- **§V-B.** The IMM sentences; the re-tune sentence; the three-variant sentence; the earlier-runs sentence; Table III and its caption (the addendum row matches `B.IMMr.*`).
- **§V-C.** All sentences; Table IV and its caption; Fig. 3's caption.
- **§V-D.** All five paragraphs; Table V and its caption.
- **§V-E.** The amendment sentence; the crossing departure sentence; the dropout disclosure; the crossing room, within-5% share, oracle (99% level stated) and N's share; the dropout room, within-5% share, r, c and efficiency; the closed-loop sentences (lower level primary; higher level secondary; 5% against 15%); the Y sentence.
- **§VI.** All four paragraphs except the Limits note (L 27).
- **§VII.** The fixed-noise, crossing and dropout numbers (69%, 2.8%, 40%); the IMM and braking-prediction sentence; no-room sentence; conditions; "do not justify"; next steps.
- **Fig. 1's and Table I's captions.**
- **S14.** Table S31 (all cells against `S0.*`); Table S32's cells; Table S33's printed cells (the one-program mark is on the right cell); Table S34's cells; Table S35's four comparison rows; Table S36's cells.
- **Table S5.** The rows on: the crossing departure; the output rule; the unmasked update after a window; the seeds; the extended case list; the capture hardware; the re-run arrays (104 of 105); Y; dropouts; the IMM re-tune; the three lock stages; extraction on the capture machines; the three retry runs; the oracle's 99% level; the six replacements; where the calibration ran.
- **Letter.** "Added at the end." apart from finding 12; the word counts match the build report.
