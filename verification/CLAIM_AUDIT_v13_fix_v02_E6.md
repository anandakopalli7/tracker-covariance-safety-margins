# Follow-up claim audit of the final freeze (22 Nov 09:07:22), v02, E6 and A13 Holm

**Auditor:** Claude Sonnet 5.5 (text by Claude Fable 5.2). Read-only; this is the only file written. No build run, no code read, nothing named <excluded folder 1>, <excluded folder 2> or local secrets opened. 22 Nov 2026.

**Inputs, SHA-256 at start and at end (equal both times):** MANUSCRIPT_v13.md `41961ed58386cada2b91d3f315016edacc41331eddffc5d686b8ccd19f408937`; SUPPLEMENT_v13.md `1a064bd2d17de2dda86edcda973bf457b5f924eadccda029d1d40bbce58e69b8`. Checked against: A_EXPORT_E6 / A_RECOUNT_E6 (agree on every value), AMENDMENT_13 section 2, A13_HOLM_v01 and its recount, the three DIFF_SINCE_INTERIM files, BUILD_REPORT, TEXT_FREEZE, the earlier audit v01.

**Result: 0 H, 1 M, 3 L. No wrong E6 or Holm number; no label error.**

## 1. E6 sentences: OK
Source values: bracketed 4-8; contact N 0.2074, class average at scale 4/8/16 0.3259/0.2444/0.1111; time lost 25.42/25.24/25.45/25.84; c_F0 at N's time 0.2574; delta -0.0500 [-0.1212, 0.0223]; one-sided p 0.0878; finite share 1.0; pass_alone false. Upper end 0.0223 is not below 0, so by the coordinator's label rule E6 is FAILED. Every place agrees:
- Abstract: "at equal time lost fewer contacts were not shown" (no claim beyond not shown; 21% against 33% and the 0.18 s kept).
- Contribution 2: "though not shown at equal time lost".
- V-E: "(difference -0.05 [-0.12, 0.02]; failed; third amendment): they cannot be told from a wider margin"; "might come from a wider margin" for the E5 result, whose label "(passed; amendment)" is unchanged and qualified.
- Table V row: "-0.05 [-0.12, 0.02] | failed"; caption defines "failed: not passed".
- Conclusion: "at equal time lost fewer contacts were not shown, so this cannot be told from a wider margin".
- S15: "25.7%, against ... 20.7%"; "-0.05 [-0.12, 0.02] (one-sided p 0.088; 100.0% of resamples bracketed): failed (amendment). The label needs ... the upper end of the interval to lie below zero"; limits stated (one point, straight-frontier assumption, one level). Table S45 points and the scale-8 and scale-16 differences (-0.04 [-0.11, 0.03], -0.03 [-0.10, 0.05]; 0.10 [0.03, 0.17], -0.37 [-0.45, -0.30]; "inconclusive", "worse") match the export at printed rounding.
- Letter: "at equal closed-loop time lost fewer contacts were not shown, and the text says so."
- Table S30 rows: lock 4428e5dc, export 72a520cf...147e (09:01:59), recount 87c32b32...deb2 (09:03:16) match the files.

## 2. A13 Holm: OK
Table S39 and its caption: E6 p 0.088, Holm 0.18 (0.08780 x 2 = 0.1756); coast-count 0.99, Holm 0.99 (0.9856, max step); "no" on both; m = 2; two programs agree (exports_agree true); the file hashes in Table S30 equal the freeze list. "The adjustment changes no label" matches the coordinator's note.

## 3. Earlier audit's items
- **H1 fixed.** Marks are back (kappa 0.168‡, 1.99‡, 0.001‡, 1.63‡, Table S7, E5q 0.073‡, Table S15, Table S34 -11.5‡, Identity paragraph, 20‡ runs). I checked the 152 of the 164 one-program values that I could find as printed text in DERIVED_v13.json: all have a ‡ within three characters; the other 12 are not printed as that text. Build report: 164 needing the mark, 187 marks printed.
- **M1 fixed:** "three later amendments" in IV-E, V-E first sentence, Table V caption; "the third reuses arms the second had scored".
- **M2 fixed:** "matched by a coasting margin" (V-E, letter).
- **M3 fixed:** "matched only in design caution (without dropouts)"; Table S30 rows now "matched in open-loop caution" (L1 of the earlier audit).
- **R9 fixed:** contribution 2 has "as expected from its near-constancy"; VI keeps the full sentence.
- Also taken: abstract "point values" (L3), "level-type effects" (L6), Table V "(Table V; Supplement S15)" (L5), "failed: not passed" and (1 + k)/(n + 1) (L7, L9), Bonferroni "counted by two programs; the Bonferroni check itself by one" (L8), letter's table references (L2).

## 4. New findings

| # | Rating | Location | Quoted | Fix |
|---|---|---|---|---|
| N1 | M | Supplement S12 | "At this build, 260 of 260 result values printed in the main text (Sections III to VII, the tables and the captions ...)" | RECOUNT_COVERAGE_v13.md (same freeze) gives 258 of 258 for the named passages and "255 distinct result values" for the S12 scope. The printed 260 matches neither; the interim text said 258. Print the coverage file's number for the stated scope, or state the scope that gives 260. |
| N2 | L | Supplement S15 closed-loop paragraph | "so its fewer contacts cannot yet be told from a wider margin" | Stale: the next paragraph is the equal-time test. "cannot be told" (or "might come from a wider margin", as in V-E). |
| N3 | L | Table I, last row | "passed in a sequence of the later amendment, locked before its own values but written after the fresh lead-braking results were seen" | Singular after "three later amendments": "of a later amendment". |
| N4 | L | V-E, Holm sentence ("All six of the second amendment's primary hypotheses stay significant after the Holm adjustment ... earlier tests are outside it") | The third amendment's own Holm (m = 2, neither rejects; S15, Table S39) is not mentioned in the main text | Optional, needs words (body has 7 spare): "the third amendment's two tests are adjusted separately (Supplement S15); neither rejects" (about 14), or leave in S15. |

## 5. Nothing else new
All other changes since the interim (Table S39 to S47 renumbering, with S44/S47 references updated and the sequence S1 to S47 unbroken; Table V caption; "level-type"; letter edits; S5/S30 rows; letter lengths 5,943 / 9,035 / 249 / 21,251) carry no new claim, wrong number or mislabel. The word "worse" in Table S45's scale-16 class compares equal scales, where the class average is the more cautious arm (time -0.37 s); the caption prints the time, so I do not rate it.

## 6. Gates: OK
BUILD_REPORT: Result PASS; abstract 249 (limit 250); body 5,943 (5,950); whole 9,035 (9,250); supplement 21,251 (21,500); open markers 0 (PENDING 0, FIGURE PENDING 0, AUTHOR DECISION NEEDED 0, FORMAT ERROR 0). My own whitespace token counts: abstract 249, whole 9,035, supplement 21,251 (body not recounted). Typeset pages: PAGES.txt and the LaTeX log say 10 pages, and the PDF hash 9dac3048... equals the freeze's. The "n.c." tokens in Table IV and S-tables are the defined "no contact" and "not definable", not markers. "[AUTHOR BLOCK ...]" in the manuscript's front matter is not one of the counted markers.
