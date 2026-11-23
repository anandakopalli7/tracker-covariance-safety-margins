# Delta claim audit of the re-frozen v13 text (A10 §10.3), v03

**Auditor:** Claude Fable 5.2 (`claude-fable-5-2`), a different model from the writer (Claude Opus 5.5). Run 21 Nov 2026.

**Audited:** the text frozen at 02:51 (`out\freeze_v13\`: manuscript, supplement, response letter, OUTCOMES, DERIVED) against the 02:32 freeze, through `notes\DELTA_FREEZE_0232_0251.md`; every changed line of the three files; Figs. 2 and 4 in `out\latex\figures\`.

**Read:** the brief; `CLAIM_AUDIT_v13_v02.md`; `STATUS.md` (the v02 and coordinator sections); A10 §2.6, §5.6, §7.5, §9; the exports `A_EXPORT_B/C/D/F.json` and `A_RECOUNT_B.json`, read directly; `RECOUNT_COVERAGE_v13.md` and `BUILD_REPORT_v13.md` of the freeze. Not read: `gen\`, `build\`.

**Result**

| | Count |
|---|---|
| v02 findings fixed | 16 |
| v02 findings partly fixed | 3 (1, 6, 11) |
| v02 findings not fixed | 0 |
| v02 findings moot (I agree with both) | 2 (3, 4) |
| New findings | 12 (1 M, 11 L) |

Every number in a changed sentence agrees with its export at the printed rounding. No "confirmed" label is misapplied. No new finding changes a result.

Severity as in v02: **H** changes what a reader concludes from the Abstract or a main table; **M** a scope or rule breach, or a visible defect; **L** precision or presentation.

## 1. The v02 findings

| # | v02 sev. | Status | New sentence (quoted) | Remark |
|---|---|---|---|---|
| 1 | H | **Partly fixed** | Abstract: "In closed loop behind braking leads, where the car brakes as it can, the braking prediction is safer at no extra cost." §VII: "In closed loop behind braking leads, … the braking prediction is safer at no extra cost by the plan's rule." §VI (unchanged): "In closed loop, with the planner's own late reaction, the braking prediction reduces contacts at no extra cost, which supports the 3 s reading". | The scope to braking leads is in the Abstract and §VII. Three gaps remain. (a) §VI "Which commitment applies" is not changed, although STATUS says "§VI the same". (b) No sentence names the lower level; at the higher level CK3 is "inconclusive" (`E3.CK3.hi`). (c) The Abstract dropped "by the plan's rule", so "no extra cost" again reads as a zero cost (time lost 0.16 [0.10, 0.22] s). Fix below. |
| 2 | H | Fixed | Table II: "n.t." in every cell below the room row of the cut-in and real-log columns; caption: "n.t.: not tested, because that data set showed no measurable room." | Two legends are now unused (new finding N6). |
| 3 | H | **Moot; I agree** | "Only these statements hold in every run set where they are defined (fresh, old evaluation and tuning runs; the real-log runs define none of these shares): … the sources' shares keep one order (the braking prediction, the acceleration margin, the time gap, the NIS inflation, then the tracker covariance)". | B's export and recount both give `TU.RR_TG` = 0.182 [−0.046, 0.362]. C's `TRANSFER.structured` now has no missing set and the ten orderings hold by point value in all three sets: tuning 0.379 > 0.278 > 0.182 > 0.064 > 0.000; old 0.837 > 0.382 > 0.321 > 0.015 > −0.0004; fresh 0.783 > 0.369 > 0.287 > 0.024 > 0.000. This is A10 §5.6's rule (point difference positive in every set). The departure row and Table S12's "not computed" are gone, correctly. |
| 4 | M | **Moot; I agree** | Fig. 2 caption: "Gridless step frontiers of wrong-go decisions … on the fresh lead-braking runs". | The figure no longer plots shares in populations where the partial oracles fail; it shows the pooled population only (`LB.grading_ok` = true). Table S8 keeps its warning. |
| 5 | M | Fixed | §V-A: "This share is pooled over all decisions: it is 0.411 while the ego moves, and 0.244 to 0.774 as 0 to 20 s of decisions after the stop are kept (Supplement S5)." Abstract, §VII: "most of the pooled room (0.783)". | `LB.mov.RR_CK3` 0.4113, `LB.T0.RR_CK3` 0.2438, `LB.T20.RR_CK3` 0.7743; all recounted. |
| 6 | M | **Partly fixed** | Abstract: "…barely varies (99.7% of rows within 5% of its median there)". Contribution 2, §VII: "…of its median on fresh lead-braking runs". §VI: "on these simulated runs that variation is almost absent". | Contribution 2, §VII and §VI are fixed. In the Abstract "there" follows "it is also equivalent in closed loop", so its nearest antecedent is the closed loop, not the fresh lead-braking runs. Fix below. |
| 7 | M | Fixed | Abstract: "Cut-in events and held-out nuScenes logs showed no measurable room, so nothing was tested there. … within 5% of the room on fresh lead-braking runs". | |
| 8 | M | Fixed | Abstract: "(contacts from behind excluded)". | |
| 9 | M | Fixed | "…within 5% of the room on fresh lead-braking runs; it is also equivalent in closed loop." | The closed-loop rule is now in Table IV's caption. |
| 10 | M | Fixed | Table IV caption: "classification by the plan: equivalent if the contact difference lies within ±0.10 and the time lost within ±0.5 s, safer if the contact difference's upper end is below 0 (at no extra cost if time lost's upper end is below 0.5 s, else at a cost), worse if its lower end is above 0". Table S4: "Classified (Table IV caption)". | Agrees with A10 §7.5. "Otherwise inconclusive" is missing (new finding N9). |
| 11 | M | **Partly fixed** | §V-D heading: "What the Score Depends On". Opening: "These results describe the score's conditions. The classifications behind leads that do not brake hard and the update-rate rule were fixed in the locked plan, outside the confirmatory sequences; the rest is exploratory." Contribution 3: "(largely exploratory)". | The heading, the opening and contribution 3 are fixed. Table V's caption still reads "What the score depends on (exploratory; …) … with the plan's classification", and Fig. 4's caption "(exploratory)" over the update-rate panel. Fix below. |
| 12 | M | Fixed | "On the earlier runs (exploratory), the ratio of the tracker's margin to the class average's…". | |
| 13 | M | Fixed | "On these runs the tested IMM's covariance varies too little for its amplitude-matched ranking oracle to recover much room; the braking prediction, which moves the predicted path rather than widening the margin, recovers most of the pooled room." | No bound language. The added clause "no tested covariance margin recovers more" needs a scope (new finding N7). |
| 14 | L | Fixed | Abstract, §VII: "the score detects rank information at the tracker's amplitude". | |
| 15 | L | Fixed | Table II: "0.0000 [−0.0018, 0.0012]; 0.0009 [0.0006, 0.0010] (C)". | `LB.IMM.r`, `LB.IMM.c` with their intervals; equal to §V-B. |
| 16 | L | Fixed | (a) Table II caption: "gridless step frontier (per-phase schedule: grid frontier)". (b) New Table S9: "Interval level of each confirmatory quantity in Table II and its basis". | Every level agrees with the exports (`LB.RR_N.level` 0.994 "calibrated"; `LB.IMM.r.level` 0.99 "nominal99"; the others 0.95). Two rows belong to quantities Table II no longer prints (new finding N3). Table III's caption still says "at the calibrated levels" for a pair of which one is the nominal-99% fallback; "at the levels of Table S9" would be exact. |
| 17 | L | Fixed | "…and recovers a small share of its room on these runs, about the size of the equivalence margin (descriptive)." | |
| 18 | L | Fixed | Table V caption: "Old evaluation runs: the earlier exploratory analysis, values from its record (one program)." | |
| 19 | L | Fixed | §V-D: "The braking prediction's wrong goes still change behind leads that brake mildly by −0.9 [−1.6, −0.4] points, for 18.7 [15.4, 21.9] points of caution; and behind leads that stop and pull away by −4.7 [−6.3, −3.4] points, for 1.7 [1.1, 2.2] points of caution." | `D1.mild.CK3.*`, `D1.stopgo.CK3.*`; all recounted. Wording: new finding N11. |
| 20 | L | Fixed | Fig. 4 caption: "…against the reaction time (terciles of lead deceleration at 0.75 s)". | In the image the panels no longer overlap and the legend sits below panel (a). The panels carry no "(a)"/"(b)" letters (new finding N12). |
| 21 | L | Fixed | Scope: "The tests concern longitudinal decisions … and in the nuScenes replication; the cut-in events and the real logs showed no room to test." | |

### Fixes proposed for the three partly fixed findings

- **1.** §VI: "In closed loop behind braking leads, at the lower level, the braking prediction avoids contacts for 0.16 s of time lost (safer at no extra cost by the plan's rule), which supports the 3 s reading". Abstract: "In closed loop behind braking leads, the braking prediction is safer at no extra cost by the plan's rule (lower level)." This drops "where the car brakes as it can" and is one word shorter. §VII: add "(lower level)".
- **6.** Abstract: replace "there" by "on those runs" and move the IMM sentence before "it is also equivalent in closed loop", or write "99.7% of rows within 5% of its median on the fresh runs". With the change to finding 1 the Abstract stays within 220 words.
- **11.** Table V caption: "What the score depends on (largely exploratory; the non-braking classifications and the update-rate rule are the plan's; …)". Fig. 4 caption: "(descriptive)" or "(largely exploratory)".

## 2. New findings

| # | Sev. | Location | Quoted sentence | Check | Rule or value broken | Fix |
|---|---|---|---|---|---|---|
| N1 | M | Response letter, response to the request on confirmatory labels (line 79); present in both freezes, not a changed line | "The plan, its two locks and every departure with its reason are in Supplement S3 (Table S{deviations})." | 1 | An unfilled placeholder is printed. The final build reports "no open marker", so its check does not see this form. | "(Table S5)". Add the brace form `S{…}` to the open-marker check. |
| N2 | L | Supplement S12, changed sentence | "At this build, 207 of 207 printed values from the fresh, closed-loop and real-log analyses had an agreeing second-program value" | 1 | `RECOUNT_COVERAGE_v13.md` of the same freeze says "205 of 205 printed values have an agreeing second program"; STATUS also says 205 of 205. DERIVED gives 207 with the generator as its only source (`REC:recount_ok`, `REC:recount_n`). | Print the coverage file's count, or say in S12 which two values the 207 adds. |
| N3 | L | Supplement Table S9 (new) | "Cut-in / N's share / 99% / nominal 99% (calibration fallback)"; "Real logs / N's share / 99% / nominal 99% (calibration fallback)" | 1, 4 | The caption says "each confirmatory quantity in Table II". Table II prints "n.t." for both; K1 and F-H1 were not run (`conf.K1`, `conf.FH1` = "not_run"). The rows give a level to intervals the paper does not print in Table II, and "fallback" suggests a calibration result for a test that was not made. | Delete the two rows, or keep them under "not tested; level the plan would have used". |
| N4 | L | Fig. 2 caption, last sentence; Table S5 row "Fresh runs: frontier curves for Fig. 2…" | "each curve's gap to F0, summed over the caution levels, reproduces the room recounted by the second program" | 1 | Only the oracle's gap to F0 is the room: from the exported curves, E gives 5.5792 = `LB.R`. The other curves reproduce their own frontier distances, i.e. their shares (CK3 0.7828, E5 0.01253, N −0.000008), and the IMM's gap is taken to its own class average, not to F0 (share 0.000032 = `LB.IMM.r`). | "the oracle's gap to F0, averaged over the caution levels, reproduces the room, and each other curve's gap its share (the IMM's against its own class average), as recounted by the second program." Same wording in the departure row. |
| N5 | L | Fig. 2, image against caption | "The IMM covariance is drawn with its own class average (dashed) … Inset: the cut-in event window, where every curve is at zero wrong goes." | 1 | (a) The dashed class average is hidden under the solid IMM curve (largest difference 0.09 points), so the reader sees one pink curve lying 0.26 points above F0 on average (up to 0.57) with no visible comparator. (b) The cut-in window is a second panel, not an inset. (c) Only F0, E and N exist there (`CI.frontier.*`); the panel has no legend and no y-axis label. | (a) Draw the dashed class average on top of the IMM curve, or in a contrasting colour. (b) "Right:" for "Inset:". (c) "where F0, E and N are at zero wrong goes"; label the y-axis. |
| N6 | L | Table II caption | "(P) passed, not confirmatory; … "dec.": decision-equivalents, printed where the partial oracles do not grade." | 1 | Neither "(P)" nor "dec." occurs in the table any more. | Delete both legends. |
| N7 | L | §VI "What a varying covariance needs", sentence 2 (new clause) | "…it recovers a small part of its room (0.046, about the size of the equivalence margin; Section V-B, descriptive); no tested covariance margin recovers more." | 4 | True for the pooled fresh-run shares (N 0.0000, re-tuned CV −0.0009, CA −0.0008, IMM 0.0000, NIS inflation 0.024). Not true without that scope: the NIS inflation, a scaled covariance (Table I), recovers 0.082 while the ego moves, 0.074 in the braking phase (Table S8) and 0.064 on the tuning runs (Table S12). | "no tested covariance margin recovers more of the pooled room on the fresh runs." |
| N8 | L | Supplement Table S27 (S10), against the changed departure row and letter | "CK3 and AM shares: not computed (a departure from the plan: their triggers need inputs the real-log tracker does not provide; Table S5)"; "E5 share: n.c. [−0.023, 2.813]"; "TG share: n.c. [−36.424, 0.404]" | 1, 4 | (a) The departure row and the letter now name three sources not computed on the real logs; this row names two. (b) Table II dropped the real-log shares because no room was found; S10 still prints share intervals on a room of −0.005 points. | (a) "CK3, AM and NA shares: not computed (…)". (b) Print the two rows as decision-equivalents (`F.RR_E5.dec` 0.0 [−0.5, 2.8]; `F.RR_TG.dec` −2.0 [−28.4, 1.0]) or mark them "descriptive; no room". |
| N9 | L | Table IV caption (changed) | "…worse if its lower end is above 0; a test only for N, CK3 and the IMM at the lower level…" | 1 | Four rows of the table are classified "inconclusive", which the caption's rule does not define (A10 §7.5: "otherwise inconclusive"). | Add "otherwise inconclusive". |
| N10 | L | Response letter, new evidence item 5 (changed) | "This departure from the plan was recorded before any real-log value (Supplement S3); no real-log hypothesis uses these sources. One departure concerns the real logs: under the planned clearance…" | 1 | The sentence before it has just described a departure on the real logs, so "One departure" contradicts the count. | "A second departure concerns the clearance: …". |
| N11 | L | §V-D "Leads that do not brake hard" (new sentence); the letter repeats it | "The braking prediction's wrong goes still change behind leads that brake mildly by −0.9 [−1.6, −0.4] points…" | 1 | "Still change … by −0.9" hides the direction; both intervals lie below zero. | "The braking prediction still lowers wrong goes behind leads that brake mildly, by 0.9 [0.4, 1.6] points for 18.7 [15.4, 21.9] points of caution, and behind leads that stop and pull away, by 4.7 [3.4, 6.3] points for 1.7 [1.1, 2.2]." |
| N12 | L | Fig. 4, image against caption | "(a) Room and after-stop room against update rate and latency. (b) Room under the reaction-and-stop commitment…" | 1 | The image has no panel letters. | Add "(a)" and "(b)" to the panels, or write "Left" and "Right" in the caption. |

## 3. Figures

- **Fig. 2** (`fig2_frontiers_v13.png`, 02:50). Curves and legend match the caption's list: F0, E, E5, N, CK3, IMM and the IMM's class average. The shaded area lies between F0 and E. From `LB.frontier.*` (201 levels each): E's mean gap to F0 is 5.5792 points (`LB.R` 5.5792); CK3, E5 and N give shares 0.7828, 0.01253 and −0.000008 (their export values to all printed digits); the IMM against its own class average gives 0.000032 (`LB.IMM.r`). The three cut-in curves are zero at every level. Findings N4 and N5.
- **Fig. 4** (`fig4_conditions_v13.png`, 02:50). Panel (a): room and after-stop room at 2, 5 and 10 Hz for latencies 0, 0.1 and 0.2 s; the points at 2 Hz without latency (5.58; 173.4) and at 10 Hz with 0.1 s (5.07; 77.8) match Table V. Panel (b): the terciles are drawn at 0.75 s only, as the caption now says; the axis labels of the two panels no longer overlap. Finding N12.
- `out\figures\` and `out\latex\figures\` now hold the same four figures, written at 02:50, before the freeze at 02:51. The old `fig2_shares_v13.*` files (02:32) remain in `out\latex\figures\` only and are not used by the text.

## 4. Changed sentences checked without findings

"Numbers agree" means each printed value equals its export value at the printed rounding.

**Abstract.** Sentence 1 ("…held-out nuScenes logs (contacts from behind excluded)"). Sentence 2 ("…detects rank information…"). Sentence 3 ("…so nothing was tested there."). Sentence 4 ("…on fresh lead-braking runs; it is also equivalent in closed loop."; E-H2 "equivalent"). Sentence 5 except "there" (finding 6): "its amplitude-matched ranking oracle recovers little of the room (0.0009)". Sentence 6 ("A braking prediction recovers most of the pooled room (0.783)…"). Last sentence ("Open-loop scores should state their commitment and show detection at the output's amplitude."; §VI keeps the full list). 218 words by the project counter (limit 220).

**I.** Contribution 2 (all three sentences). Contribution 3 ("largely exploratory"). Scope, sentence 1.

**V-A.** "…about 1,204 decision-equivalents (Table II, Fig. 2)…". "The braking prediction recovers 0.783 [0.720, 0.842] of the room, most of it (confirmed). This share is pooled over all decisions…" (numbers agree).

**Table II.** Caption: "(per-phase schedule: grid frontier)"; "n.t.: not tested, because that data set showed no measurable room". Rows: E5, E5 minus E5p, N, varying covariance (four decimals), classification, CK3 ("n.t." for cut-in, "not computed\*" for the real logs), partial oracles.

**Fig. 2 caption.** Sentences 1 to 3 ("Gridless step frontiers…", "The IMM covariance is drawn with its own class average (dashed): its share is measured against that class average and its own oracle, not against F0.", "Curves that coincide at this scale are drawn over each other."). "The curves come from the first program" (CD-15).

**V-B.** "…recovers a small share of its room on these runs, about the size of the equivalence margin (descriptive)." "On the earlier runs (exploratory), the ratio…".

**Table IV caption.** The classification rule, except the missing last clause (N9).

**V-D.** Heading and opening sentences (the plan fixes D-H1, D-H2 and the update-rate rule; "the rest is exploratory" is on the cautious side, since the filter-tuning wording also follows a plan rule). "Recording policy", sentence 2 (see finding 3). Table V caption, the sentence on the old-run record. Fig. 4 caption, the tercile clause.

**VI.** "…and on these simulated runs that variation is almost absent." "On these runs the tested IMM's covariance varies too little…recovers most of the pooled room." "(0.046, about the size of the equivalence margin; Section V-B, descriptive)".

**VII.** Sentences 2 to 7 as changed ("rank information"; "on fresh lead-braking runs; it is also equivalent in closed loop"; "99.7% … on fresh lead-braking runs"; "most of the pooled room (0.783)"; "In closed loop behind braking leads … by the plan's rule", apart from the level, finding 1).

**Supplement.** Table S4's three closed-loop rows ("Classified (Table IV caption)"). Table S5: the row on the time gap's tuning-run share is removed, correctly; the row "Fresh runs: frontier curves for Fig. 2 written after the second lock" agrees with CD-15 apart from N4; the row "Real logs: braking prediction, acceleration margin and NIS inflation" agrees with F's record (the NIS inflation needs the innovations of the capture's filter); the rows on definitions, the acceptance test, the six re-extracted runs and the four code fixes agree with CD-10, CD-4, CD-5 and CD-2/11/12/13/14. Table S9: the eight lead-braking rows and the two room rows agree with the exports. Table S12: "TG 0.182 [−0.046, 0.362]" (B's export and recount). Tables S10 to S29: renumbered only; the one cross-reference in the text ("Table S29 lists its query strings") follows.

**Response letter.** Item 5, the sentence on the three sources not computed (apart from N10). "Structure and length": 5,191, 8,405, 218 and 11,950 words equal the build report's counts. The three "Result" paragraphs repeat the manuscript's changed sentences word for word (§V-A, §V-D recording policy, §V-D non-braking leads).
