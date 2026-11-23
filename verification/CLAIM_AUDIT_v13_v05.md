# Delta claim audit of the re-frozen v13 text (A10 §10.3), v05

**Auditor:** Claude Fable 5.2 (`claude-fable-5-2`), a different model from the writer (Claude Opus 5.5). Run 21 Nov 2026.

**Audited:** the text frozen at 03:08 (`out\freeze_v13\`) against the 03:03 freeze (`out\freeze_v13_0303\`), through `notes\DELTA_FREEZE_0303_v05.md`.

**Read:** the brief; `CLAIM_AUDIT_v13_v04.md`; the diff; the frozen manuscript (.md, .tex), supplement, letter, `BUILD_REPORT_v13.md` and `OUTCOMES_v13.json`; `STATUS.md` (for the record of the coordinator's Fig. 2 check); CD's export `A_EXPORT_C.json` (frontier curves, room, shares). Not read: `gen\`, `build\`. No other file edited; nothing sent off this machine.

## Result

| | Count |
|---|---|
| Open items of v04 (N4, V1, V2): fixed | 3 of 3 |
| Changed lines audited (my own diff of the two freezes gives the same 8 lines: 2 + 4 + 2) | 8 |
| New findings | 0 |
| Unfilled labels in the three frozen .md files | 0 |

**The text passes.** One remark on provenance (section 3), which changes no result and needs no text change if the coordinator confirms it.

## 1. The three open items

| # | Status | New text (quoted) | Check |
|---|---|---|---|
| N4 | **Fixed** | Supplement line 119 (Table S5): "…approved by the coordinator on 21 Nov 2026, who checked that the oracle's gap to F0, averaged over the caution levels, reproduces the room recounted by the second program, and each other curve's gap its share)" | The wording now agrees with the Fig. 2 caption, §IV-B and §V-A. I recomputed it from the exported curves (201 caution levels): the oracle's mean gap to F0 is 5.579177441798148 = `LB.R` exactly; the gaps of N, E5 and CK3 over the room give −0.0000083, 0.01253 and 0.78281 = `LB.RR_N`, `LB.RR_E5`, `LB.RR_CK3`; the IMM against its own class average and oracle gives 0.0000321 = `LB.IMM.r`. See the remark in section 3. |
| V1 | **Fixed** | Manuscript line 124 (Table II caption): "(C) confirmed in its sequence; (F) not passed." Frozen TeX: "(C) confirmed in its sequence; (F) not passed." | "(F)" stands in the table twice (line 129: cut-in room and real-log room) and nowhere else; `conf.K0` and `conf.FH0` are "failed", and K1, K2, FH1, FH2 are "not_run" (printed n.t.). "(C)" is on H0 to H5 only, all "confirmed". In the TeX, "(F)" occurs in the caption and the row, and "not passed" once. |
| V2 | **Fixed** | Supplement line 457: "**TABLE S27.** Real logs (nuScenes): splits, the horizon rule on the design split, and descriptive frontier distances." | The table's descriptive rows are the E5 and TG frontier distances; no share is printed (CK3, AM and NA: "not computed"). |

## 2. The changed lines, by the four checks

| Line | 1 Numbers | 2 Wording (§9) | 3 Labels | 4 Claim within its rule |
|---|---|---|---|---|
| Manuscript 124 (Table II caption) | No number changed | "not passed" is the plan's wording for a failed room test; no equivalence or absence claimed | (C) and (F) defined and used correctly | "n.t." kept for the data sets without room |
| Supplement 119 (Table S5 row) | Recomputed, agrees (section 1) | A departure row; no result wording | None | Says what was checked, no more than the curves show |
| Supplement 457 (Table S27 caption) | No number | "descriptive" kept: nothing was tested on the real logs after the room test failed | None | Removes the promise of shares, which the rule forbids there |
| Letter 20 (Structure and length) | Body 5,230, whole 8,467, abstract 217, supplement 11,966: each equals the frozen build report (5230, 8467, 217, 11966; all within their limits). The changes of +3 and +12 words equal the words added in the three lines above. "10 pages" and the v12 counts are unchanged from the line checked in v04 | Not applicable | None | None |

(Each line appears twice in the diff, as old and new: 8 diff lines, 4 text lines.)

## 3. Remark

- **Who checked the shares (Table S5, line 119).** The row says the coordinator checked both the room and each other curve's share. `STATUS.md` records the coordinator's check as "each curve's summed gap to F0 reproduces the recounted room" (02:39/02:41); its source note is in `gen\`, which I do not read. The statement is true of the data (I recomputed both parts), but I cannot confirm from the readable record that the coordinator's own check covered the shares. If it covered the room only, end the clause after "second program", as v04 offered. Severity L.

## 4. Unfilled labels

Searched the frozen `MANUSCRIPT_v13.md`, `SUPPLEMENT_v13.md` and `RESPONSE_TO_REVIEW_v13.md` for `S{`, `@@`, `[[`, `<<`, `??`, TODO, TBD, PENDING and SLOT: **none**. The only `{name}` matches are LaTeX mathematics (`{F0}`, `{E5}`, `{N}`, `{NIS}`, `{N_x}`, `{F0_x}`, `{A}`, `{rank}`). The build report gives the same: "unfilled labels or placeholders (S{...}, @@...@@): 0", Result PASS.

## 5. Other checks

- The three frozen .md files are byte-identical to the copies in `out\`.
- `STATUS.md` now gives body 5,230 and whole 8,467 for this freeze, in agreement with the build report (v04's remark is settled).
- Supplement S12's "Every finding was fixed and every changed sentence audited again" now holds, subject to the remark above.
