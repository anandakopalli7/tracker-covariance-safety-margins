# Delta claim audit of the re-frozen v13 text (A10 §10.3), v04

**Auditor:** Claude Fable 5.2 (`claude-fable-5-2`), a different model from the writer (Claude Opus 5.5). Run 21 Nov 2026.

**Audited:** the text frozen at 03:03 (`out\freeze_v13\`: manuscript, supplement, response letter; identical to the copies in `out\`) against the 02:51 freeze (`out\freeze_v13_0251\`), through `notes\DELTA_FREEZE_0251_v04.md`: every changed line of the three files (24, 12 and 8), and Figs. 2 and 4 in `out\latex\figures\` (written 03:03).

**Read:** the brief; `CLAIM_AUDIT_v13_v03.md`; the diff; the three frozen files; `OUTCOMES_v13.json`, `DERIVED_v13.json`, `BUILD_REPORT_v13.md`, `RECOUNT_COVERAGE_v13.md` and `TEXT_FREEZE_v13.md` of the freeze; `out\TRACE_MANUSCRIPT_v13.md` (for the count in finding N2); the exports `A_EXPORT_B/C/D/E/F.json`, read directly. Not read: `gen\`, `build\`. No other file edited; nothing sent off this machine.

## Result

| | Count |
|---|---|
| v02 findings 1, 6, 11 (partly fixed in v03): now fixed | 3 of 3 |
| v03 findings N1 to N12: fixed | 11 |
| v03 findings N1 to N12: partly fixed | 1 (N4) |
| v03 findings N1 to N12: not fixed | 0 |
| New findings | 2 (1 M, 1 L) |
| Unfilled labels (`S{…}`, `{name}`, `@@…@@`, `??`, PENDING/TODO) in the three frozen files | 0 |

Every number in a changed line agrees with its export at the printed rounding. No "confirmed" label is misapplied and no changed sentence exceeds its rule. No open item changes a result. Severity as in v02 and v03 (H / M / L).

## 1. Status of the earlier findings

| # | Sev. | Status | New text (quoted) | Remark |
|---|---|---|---|---|
| 1 | H | **Fixed** | Abstract: "In closed loop behind braking leads (lower caution level), the braking prediction is safer at no extra cost by the plan's rule." §VI: "In closed loop behind braking leads at the lower caution level, with the planner's own late reaction, the braking prediction changes the contact share by −0.20 [−0.32, −0.10] for 0.16 [0.10, 0.22] s of time lost (safer at no extra cost by the plan's rule), which supports the 3 s reading". §VII: "In closed loop behind braking leads at the lower caution level, where the car brakes as it can, the braking prediction is safer at no extra cost by the plan's rule." | (a) §VI is changed. (b) The level is named in all three places; `E3.CK3.lo` = "safer_free", `E3.CK3.hi` = "inconclusive", `EH1` = "safer_free". (c) "by the plan's rule" is back in the Abstract. Values: `E3.CK3.lo.dc` −0.2 [−0.3178, −0.0985]; `E3.CK3.lo.dt` 0.1632 [0.1046, 0.2246]. "Lower caution level" is right: the lower level is F0's smaller scale (design caution 14.10% against 22.30%). |
| 6 | M | **Fixed** | Abstract: "…barely varies (99.7% of rows within 5% of its median on fresh runs)". | `LB.IMM.within5` 0.99693. "Fresh runs" is the wording v03 proposed; the previous sentence names the fresh lead-braking runs, and §VII keeps "fresh lead-braking runs". |
| 11 | M | **Fixed** | Table V caption: "What the score depends on (largely exploratory; the non-braking classifications and the update-rate rule are the plan's; fresh lead-braking runs unless stated; gridless step frontier)." Fig. 4 caption: "What the score depends on (largely exploratory)." | Agrees with the §V-D opening and contribution 3. |
| N1 | M | **Fixed** | Letter, line 79: "…every departure with its reason are in Supplement S3 (Table S5)." | Table S5 is the departures table and stands in Supplement S3 (supplement lines 72 to 131). The final build report now lists the check "unfilled labels or placeholders (S{...}, @@...@@): 0". |
| N2 | L | **Fixed** | Supplement S12: "At this build, 207 of 207 values printed in the main text (Sections III to VII, the tables and the captions) from the fresh, closed-loop and real-log analyses had an agreeing second-program value". | I recounted it from the manuscript trace and DERIVED: the manuscript prints 213 distinct values, 207 of them from the package exports (B, C, D, E, F), and all 207 have `recount_agrees` = true. The coverage file's 205 is for its narrower list of passages (Abstract, I, V to VII); the two no longer conflict, since S12 now states its scope. |
| N3 | L | **Fixed** | Table S9: the two rows "N's share / 99% / nominal 99% (calibration fallback)" under Cut-in and Real logs are deleted; "Cut-in / Room / 95%" and "Real logs / Room / 95%" remain. | Every remaining row is a quantity Table II prints. |
| N4 | L | **Partly fixed** | Fig. 2 caption: "The curves come from the first program: the oracle's gap to F0, averaged over the caution levels, reproduces the room, and each other curve's gap its share (the IMM's against its own class average), as recounted by the second program." Table S5 (supplement line 119, unchanged): "…approved by the coordinator on 21 Nov 2026, who checked that each curve's summed gap to F0 reproduces the room recounted by the second program". | The caption is fixed and agrees with §IV-B ($R = D(E)/201$) and §V-A ("averaged over the caution levels"). The departure row keeps the old wording, which v03 asked to change as well. Fix below. |
| N5 | L | **Fixed** | Caption: "Right: the cut-in event window, where F0, E and N are at zero wrong goes at every caution." | Image (03:03): (a) the IMM's class average is drawn dashed in dark purple over the pink IMM curve, with the legend entry "F0 (IMM)", and is visible along the whole curve; (b) "Right:" replaces "Inset:"; (c) the right panel has a y-axis label and the note "No wrong goes at any caution". It has no legend of its own; the colours are those of the left legend, and only the top curve (N) shows, which the caption's "Curves that coincide … are drawn over each other" covers. |
| N6 | L | **Fixed**, with a side effect | Table II caption: "(C) confirmed in its sequence. Shares in other populations, grid and hull frontiers: Supplement S5." | "(P)" and "dec." are gone. The legend "(F) not passed" was deleted with them, although the table still uses "(F)": new finding V1. |
| N7 | L | **Fixed** | §VI: "…no tested covariance margin recovers more of the pooled room on the fresh runs." | Pooled fresh-run shares: N −0.000008, re-tuned CV −0.0009, CA −0.0008, IMM 0.00003 and its two variants −0.0003 and 0.0002 (B's export), NIS inflation 0.024; the adaptive filter 0.0459 (`B.AQ.RR`). |
| N8 | L | **Fixed**, with a side effect | Table S27: "E5: frontier distance from F0 (decision-equivalents; no room, so no share) / 0.0 [−0.5, 2.8]"; "TG: frontier distance from F0 (decision-equivalents; no room, so no share) / −2.0 [−28.4, 1.0]"; "CK3, AM and NA shares / not computed (a departure from the plan: they need inputs the real-log tracker does not provide; Table S5)"; "In-path population: room (pp) / −0.03". | `F.RR_E5.dec` 0.0 [−0.473, 2.766]; `F.RR_TG.dec` −1.990 [−28.438, 0.950]; `F.inpath.R` −0.0344. Three sources are named, as in Table S5 and the letter. The table's caption still promises shares: new finding V2. |
| N9 | L | **Fixed** | Table IV caption: "…worse if its lower end is above 0, otherwise inconclusive; a test only for N, CK3 and the IMM at the lower level and descriptive elsewhere." | A10 §7.5. |
| N10 | L | **Fixed** | Letter, item 5: "A second departure concerns the clearance: under the planned clearance the design split showed no room…" | |
| N11 | L | **Fixed** | §V-D and letter line 100: "The braking prediction still lowers wrong goes behind leads that brake mildly, by 0.9 [0.4, 1.6] points for 18.7 [15.4, 21.9] points of caution, and behind leads that stop and pull away, by 4.7 [3.4, 6.3] points for 1.7 [1.1, 2.2] points of caution." | Exported changes: `D1.mild.CK3.dwg` −0.949 [−1.592, −0.411], `dcau` 18.689 [15.440, 21.857]; `D1.stopgo.CK3.dwg` −4.701 [−6.273, −3.402], `dcau` 1.659 [1.135, 2.237]. The reductions are printed as positive numbers with the interval ends exchanged, correctly. Table V keeps the signed differences (−0.9, −4.7) under the heading "wrong-go differences", which is consistent. |
| N12 | L | **Fixed** | Fig. 4 image: bold "(a)" and "(b)" above the panels. | The caption's letters now have their panels. |

### Fix proposed for the one partly fixed finding

- **N4.** Table S5, row "Fresh runs: frontier curves for Fig. 2 written after the second lock", last clause: "…approved by the coordinator on 21 Nov 2026, who checked that the oracle's gap to F0, averaged over the caution levels, reproduces the room recounted by the second program, and each other curve's gap its share". If the coordinator's check was of the room only, stop after "second program".

## 2. New findings

| # | Sev. | Location | Quoted text | Check | Rule or value broken | Fix |
|---|---|---|---|---|---|---|
| V1 | M | Table II, caption against rows (manuscript lines 124 and 129; the same in the frozen TeX: "(F)" twice, "not passed" nowhere) | Caption: "(C) confirmed in its sequence. Shares in other populations…". Row: "Room $R$ (pp) / 5.58 [4.99, 6.17] (C) / 0.00 [0.00, 0.00] (F) / −0.01 [−0.13, 0.13] (F)". | 3 | The label "(F)" marks the two failed room tests (`conf.K0`, `conf.FH0` = "failed") and is no longer defined anywhere in the manuscript. The 02:51 caption read "(C) confirmed in its sequence; (P) passed, not confirmatory; (F) not passed."; the fix of N6 removed one legend too many. | "(C) confirmed in its sequence; (F) not passed." |
| V2 | L | Supplement Table S27, caption (line 457; unchanged) against its changed rows | "**TABLE S27.** Real logs (nuScenes): splits, the horizon rule on the design split, and descriptive shares." | 1 | After the fix of N8 the table prints no share: E5 and TG are frontier distances "(… no room, so no share)", the N share of the in-path population is removed, and the three other shares are "not computed". | "…the horizon rule on the design split, and descriptive frontier distances." |

## 3. Unfilled labels

Searched `MANUSCRIPT_v13.md`, `SUPPLEMENT_v13.md` and `RESPONSE_TO_REVIEW_v13.md` of the new freeze for `S{`, any `{name}` outside mathematics, `@@`, `[[ ]]`, `<< >>`, `??`, TODO, TBD, PENDING and SLOT: **none remains**. The only brace matches are LaTeX mathematics (`\mathrm{N}_x`, `\overline{\mathrm{NIS}}`, `\sum_{\ell}`, `F_{F0}`, `\rho_{i,r}`). The frozen TeX has one `S{`, the definition `\DeclareUnicodeCharacter{00A7}{\S{}}` in its preamble, which is code and not a label. The author block ("[AUTHOR BLOCK: … to be completed by the author]") is the known author-only item and not a label of this kind.

## 4. Figures

- **Fig. 2** (`fig2_frontiers_v13.png`, 03:03). Left panel "Lead braking, fresh runs": F0, E, E5, N, IMM, CK3 and the dashed "F0 (IMM)", now visible on the IMM curve; the room is shaded. Right panel "Cut-in, event window": a flat line at zero, a y-axis label and the note "No wrong goes at any caution". Agrees with the caption. N5 fixed.
- **Fig. 4** (`fig4_conditions_v13.png`, 03:03). Panels carry "(a)" and "(b)". Panel (a) and (b) content unchanged from v03 (the points at 2 Hz without latency and at 10 Hz with 0.1 s match Table V; terciles at 0.75 s only). N12 fixed.

## 5. Changed lines checked without findings

"Numbers agree" means each printed value equals its export value at the printed rounding.

**Manuscript.**
- Line 9, Abstract. "(99.7% of rows within 5% of its median on fresh runs)"; "so does a per-phase margin schedule (0.916)" (`LB.PS.rec` 0.916; the shorter form loses nothing, the clause before it names the pooled room); the closed-loop sentence (finding 1). 217 words by my count and by the build report (limit 220).
- Line 124, Table II caption: the deletions of "(P)" and "dec.", apart from V1.
- Line 141, Fig. 2 caption: "Right: …"; the last sentence.
- Line 149, Table III caption: "…with their confirmatory intervals, at the levels listed in Supplement S5." Table S9 stands in Supplement S5 and lists 99.4% (calibrated) for N's share and 99% (nominal, calibration fallback) for the IMM's share.
- Line 165, Table IV caption: "otherwise inconclusive".
- Line 196, §V-D "Leads that do not brake hard" (numbers agree; signs and interval ends correctly exchanged).
- Line 200, Table V caption; line 222, Fig. 4 caption.
- Line 228, §VI "What a varying covariance needs" (scope added; 0.046 = `B.AQ.RR` 0.0459).
- Line 230, §VI "Which commitment applies" (numbers agree; the intervals are Table IV's Newcombe and case-bootstrap 95% intervals; the classification is the plan's).
- Line 236, §VII: "at the lower caution level".

**Supplement.**
- Lines 196 and 198 of the 02:51 file (Table S9): the two deleted rows.
- Lines 469 to 472 (Table S27): the four rows (numbers agree), apart from the caption (V2).
- Line 493 (S12): "207 of 207 values printed in the main text (Sections III to VII, the tables and the captions)" (recounted, see N2).

**Response letter.**
- Line 17, item 5: "A second departure concerns the clearance".
- Line 20, "Structure and length": 5,230, 8,464, 217 and 11,954 words equal the frozen build report's counts.
- Line 79: "(Table S5)".
- Line 100: repeats manuscript line 196 word for word.

**Frozen TeX.** Each changed manuscript sentence is present in `MANUSCRIPT_v13.tex` in its new wording (twelve phrases searched, each found once).

## 6. Remarks outside the audited text

- `STATUS.md` line 10 gives "body 5,235, whole 8,469" for this freeze; the frozen build report and the letter give 5,230 and 8,464. The text is consistent with its build report; STATUS is not.
- Supplement S12 says "Every finding was fixed and every changed sentence audited again." This holds once N4, V1 and V2 are fixed and the three lines they change are checked.
