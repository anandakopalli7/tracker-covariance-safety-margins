# Delta claim audit of the fix round (v13, interim freeze 08:45), v01

**Auditor:** Claude Sonnet 5.5 (the fix-round text was written by Claude Fable 5.2, the earlier text by Claude Opus 5.5). 22 Nov 2026. Read-only; this is the only file written. No build was run, no generator code was read, nothing named <excluded folder 1> or <excluded folder 2> or local_secrets was opened. One light `python -I` process at a time.

**Inputs (SHA-256 at start and again at end; both times equal the interim freeze):**
- MANUSCRIPT_v13.md `44ed268c3eb011542a149331fbf6751609346efe1174e320b52c1bad0ddc919f`
- SUPPLEMENT_v13.md `ea77f6727060b0ba0719b552ff6271392d89ecc53395447ed62735679bf51289`
- RESPONSE_TO_REVIEW_v13.md `5b55e3be585f44c02ed836d934172fbd3423d1aa10456db83e56c847c7cde600`

**How I checked.** I read the brief, A13 in full, the round-2 panel's sections 4 and 5, the round-2 audit, the sprint panel's R1-R12, the three diffs and the changed parts of the manuscript, supplement (S5, S12, S14, S15, Table S30) and letter. Numbers were compared with the exports of record and DERIVED_v13.json: DRF (coast count, both programs), E5 (both), DR2 and DR10 (both), M (spread means), the two Holm files, the post hoc resample count (both programs) and the Bonferroni file; lock hashes and file times of LOCK_A13a/b/c and of the new Table S30 rows were recomputed. **Every new or changed number I checked matches its source at the printed rounding and has an agreeing second-program value, except the one disclosure problem in H1 below.** No wrong number found.

Scope notes: E6 slots (five `[PENDING]` markers) not audited, as instructed. The three "not yet known" places (abstract and conclusion closed-loop sentences, V-E "cannot yet be told", contribution 2's clause) are true as they stand: E6 has no export, and the text says only that the fewer contacts cannot yet be told from a wider margin, which the extra 0.18 s and 0.98 m support.

---

## 1. Required items and the round-2 H and M findings

Rows: R-1 to R-14 (panel), then the audit's H/M numbers not already covered. Status: fixed / fixed in part / not fixed.

| Item | Status | Quoted new text and note |
|---|---|---|
| **R-1** (audit 1 H, 2 M, 13 L) | **fixed** | Abstract: "In closed loop with dropouts, matched in open-loop caution, it had fewer contacts (21% against 33%) but lost 0.18 s more, so this cannot yet be told from a wider margin." V-E: "the two arms were matched in open-loop caution on the older fresh runs (18.2% against 18.4%). On 135 new cases the covariance arm made contact in 21% against 33% ... But in closed loop that arm was the more cautious one: where neither made contact, it lost 0.18 s more and stopped 0.98 m farther back (Table V) ... at the bottom of its grid it made contact in 17% of the 30 tuning cases and in 33% of these." Values: E5 export 0.2074/0.3259, dt 0.181 [0.111, 0.258], rest gap 0.984 [0.601, 1.394], cautions 18.22/18.39, cal g4 0.1667 (all with recount). Contribution 2, VII, S15 and Table S5 carry it. Residual L1. |
| **R-2** | **fixed** | S15 overview and Table S43: "safer; time cost within the plan's 0.5 s tolerance"; V-E prints no class. V-C and Table IV keep "safer, no extra cost" with the rule in the caption. |
| **R-3** (audit 6 M, 12 M) | **fixed** (see M2) | No "tracks the error" anywhere (grep). Abstract: "it gains a little where it grows during dropouts or manoeuvres"; VI: "These are level effects through the margin"; V-E reports the decomposition as "(both descriptive...)" then the coast-count result. |
| **R-4** (audit 22 L) | **fixed** | Abstract: "In these tests a tracker's covariance ... rarely beat one class-average margin, and then by little"; VII: "In these tests a tracker's covariance rarely improved ... and then by little." |
| **R-5** (audit 4 M, 12 M) | **fixed in part** | Abstract: "Kendall τ 0.11, 99% interval [0.04, 0.17]) and slightly inversely over all tracks"; VI: "is consistent with a wider spread around real misses"; V-E: "they mostly compare missed with steady tracks, and a missed track's spread is larger (mean 5.21 m against 2.45 m)" (M.s.in_miss.mean_s 5.2110, M.s.steady.mean_s 2.4488, recounted). **Not done:** the training-split τ is not printed (no export pair holds it); the letter says so. I accept the reason, but this is an unmet item for the coordinator. |
| **R-6** (audit 3 M) | **fixed** | Abstract: "and in closed loop it is equivalent within 0.10 contact share." |
| **R-7** | **fixed** | Abstract "these shares lie inside the same ±5% margin"; V-E "as point values, inside the paper's own ±5% equivalence margin: detectable, but small by that margin (no equivalence test was registered for them)"; VII "both lie inside the ±5% margin". See L3. |
| **R-8** | **fixed** | V-E "Under dropouts (lead braking, this mask law and output rule only)"; "random, truth-independent masks"; Limits: "The dropout results hold for random masks of one to three updates with tracks kept three updates, on lead braking, and have no decision-level support on real logs." |
| **R-9** (audit 9 M, 16 L) | **fixed** | V-E "(Supplement S15)" and "Through the position-velocity interface (Section III-D) this share is a lower bound"; Limits "so the two-noise IMM's share is a lower bound for that interface"; Table III "IMM, two-noise (older runs, secondary)"; V-E: "more than its amplitude-matched oracle, a gain from level or shape". The lower-bound sentence is in V-E, not V-B (the 2.2% is reported in V-E): acceptable. |
| **R-10** (audit 7 M, 11 M) | **fixed** | "(no permuted-twin test of the covariance was run, so that oracle is no ceiling)"; "it varies there mostly for other reasons" (V-E, abstract, VII), with "exploratory decomposition (R² 0.47)" in V-E; VI "Under injected lead-braking misses it grows". The abstract and VII do not carry "exploratory" (L, word budget). |
| **R-11** | **fixed** | S15: "under rules fixed before any of those runs was extracted or scored (their capture had begun before the lock, which records them as sealed)". |
| **R-12** (audit 8 M, 10 M) | **fixed** | S15 10 Hz: "Among the decisions inside a dropout alone, the covariance's share of their own room is 0.035 [0.014, 0.054] there (descriptive). Limits: its class average is the 2 Hz one under the 2 Hz masks ... masks last 0.5, 1.0 or 1.5 s ..."; Table S40 caption "(2 Hz; the 10 Hz value follows)"; V-E "ranking among dropout decisions is not shown at 2 Hz". Stale parenthesis in Table S35 deleted. DR10.in.RR_N 0.03458 [0.01385, 0.05448]. |
| **R-13** (audit 18 L) | **fixed** | IV-E: "within the second amendment, six primary hypotheses are Holm-adjusted (Table V)"; "recount every value printed in the main text and all but the marked (‡) values of the supplement" (but see H1); V-E "(H in Table V); earlier tests are outside it". Table V H values (0.0079, 0.0079, 0.0003 x4) equal the one-convention (1+k)/(n+1) column of both Holm files. The family is identified by the H marks, not named in a sentence; acceptable. |
| **R-14** (audit 5 M) | **fixed** | Abstract ends "Magnitudes hold in one simulated configuration, mainly at 2 Hz without latency." |
| Audit 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | as above | Mapped one-to-one in the letter's new paragraph. |
| Seats' other points: Table V and the verdict first | **fixed** | Table V present with label column; abstract opens with the verdict. See M1 for its caption. |
| "Preregistered" | **fixed** | IV-E: "By "preregistered" we mean internal locks, not a public registry: SHA-256 hashes with local file times and no third-party timestamp (Table S30)." Title left to the author, as the letter says. |
| Two stated times in locked text | **fixed** | Table S5 row; I confirmed both: A12 text says "about 00:55" (LOCK_A12a file time 00:47:53) and "about 03:55" (LOCK_A12c 03:35:08). |
| Closed-loop table caption; masked-share sentence | **fixed** | Table IV caption gives population and statistic; S15: "the per-arm masked shares differ only because a run ends at its first contact". |
| Abstract's lost clause (sprint R5) kept elsewhere; letter says so | **fixed** | V-C: "the braking prediction is safer at no extra cost (the plan's class: time lost below 0.5 s), as is the time gap"; VII: "in closed loop (lower level; class-average contacts 20%) it removed the contacts for 0.16 s more time lost, and a plain time gap with less" (Table IV 0.16 [0.10, 0.22]; -0.13); the letter's "Journal-fit seat" bullet says both. |
| Sprint R4 clause in V-E | **fixed in part** | Present: "at the higher (secondary) it had fewer contacts for more time lost, which cannot be told from a wider margin (Supplement S14)". Numbers stand in Table S36 (higher level: -0.10 [-0.20, -0.02], 0.25 [0.15, 0.36]; lower: -0.03 [-0.10, 0.03], 0.15 [0.08, 0.24]). But "not matched at all" is wrong: M3. |
| **A13 section 3 (coast count)** | **correct, one over-reach** | Abstract/V-E/Table V/S15 agree with DRF (delta -0.0024 [-0.0057, -0.0001], both programs; RR_coast 0.0322 [0.0103, 0.0541], RR_N 0.0298 [0.0077, 0.0518], p 0.986, k 0.216/0.107/0.065/0.925, flag2 0.0347, delta2 -0.0049 [-0.0094, -0.0006]). Label "failed (amendment)" (Table V: "failed") follows DRF.status; "within the equivalence margin" is right (both ends inside (-0.05, 0.05)); S15 records the adaptation of the 3.6 wording; the dropout class stays "recovers"/"replicated". See M2. |
| Post hoc Bonferroni (S15) | **correct** | "resample-count p of 0.0051 (102 of 20,000 ...)": PH.p_r 0.0051497 in both programs. Bonferroni file: all steps survive at 0.00625; narrowest is DR2 (p_approx 0.0057). See L8. |
| Table S5 / S30 new rows | **correct** | Lock hashes (LOCK_A13a 4428e5dc, A13b c85f39c3, A13c 67088c15, amendment snapshots bc7c2bf4 / 507af801) and times (06:40:47, 06:48:18, 06:49:05, exports 07:04:36) match the files. Budget row 250 / 5,950 / 9,250 / 21,500. |

---

## 2. Round-2 audit, L findings

| # | Taken? | Note |
|---|---|---|
| 13 | taken | "17% of the 30 tuning cases". |
| 14 | taken, but see M3 | "An earlier closed loop with dropouts, not matched at all" |
| 15 | taken | "(descriptive; Table V; Supplement S15)", "dropout start probability". |
| 16 | taken | Table III row relabelled. |
| 17 | taken | "The nuScenes logs and cut-in events showed no room, so no real-log decision test was possible". |
| 18 | taken | IV-E Holm sentence. |
| 19 | taken | "behind braking leads (Table IV), so the closed loop does not decide". |
| 20 | taken | Table S43 caption: differences are paired means, per-arm values are medians or pooled. |
| 21 | taken | Letter lists the real-log dropout test, 10 Hz and Holm. I confirmed 10 typeset pages from the PDF (last page is 10, none after). |
| 22 | taken | "rarely beat". |
| 23 | taken | The adaptive filter's twin is its own paragraph. |
| 24 | not taken | For the coordinator (arrival time of the 10 Hz arrays); acceptable, and the letter says so. |
| 25 | n/a | A count; body is now 5,900 of 5,950. |

---

## 3. New findings

Ratings: H = wrong number or claim beyond its rule; M = missing required wording or label; L = clarity.

| # | Location | Problem | Rating | Fix (fewest words) |
|---|---|---|---|---|
| **H1** | Supplement, every table and sentence of values with no second program (Table S7 NIS/NEES rows, S4 "κ = 0.168", "1.99", "σ_a² = 0.001", "1.63", E5q "0.073 [0.056, 0.093]", Table S15 terciles and delayed stop, Table S34 "-11.5 [-32.4, 6.3]", the Identity paragraph, and others); IV-E; S12 | The ‡ mark ("a value computed by one program only") was dropped from these values in the fix build. The 06:23 supplement printed 211 marks for 188 unrecounted values; this build prints 88 marks for 164 unrecounted values (BUILD_REPORT: "in the supplement each carries the mark ‡, 88 marks printed"). By DERIVED_v13.json (recount null) at least 79 printed supplement values with no agreeing second program carry no ‡ (for example B.kappa, B.CV.nis_pre, BSUM terciles, B.AQ.E5q.RR). So IV-E's "recount every value printed in the main text and all but the marked (‡) values of the supplement" and the supplement's mark definition are false for them. The main text is unaffected (0 in the main text per the build). | **H** | Restore the marks in the builder (word-neutral: ‡ is a mark, not a counted word); or, if the coordinator decides these design values need none, change the definition in the supplement's opening note and IV-E to say so. |
| **M1** | Table V caption ("Tests of the two later amendments"); V-E first sentence ("Two later amendments added tests"); IV-E ("two later amendments' tests ... each locked before any value of its data") | The coast-count row (and E6 when it lands) belongs to a third amendment, written after the second panel and after the dropout decomposition and DR2 were seen (A13 s0, s3.5). The main text never says so; only S15 and Table S5 do. A13 s0 asks that the reuse of arms be stated in the text of the paper. | M | "later amendments" in the three places (-1 word each); in V-E after "(... failed; amendment)" add "added after the review, from arrays already seen" (+7 words; cut "(both descriptive; Supplement S15)" repeats or "dropout" duplicates). |
| **M2** | V-E dropout paragraph: "The dropout gain is thus a coasting margin, a level effect that a count of missed updates gives without a covariance" | The control shows a coast-count margin recovers at least as much (0.0322 against 0.0298); it does not show the covariance's gain contains no ranking: the in-dropout own-room share is 0.009 [-0.008, 0.024] at 2 Hz, 0.035 [0.014, 0.054] at 10 Hz, and A13 s3's rule only asks whether N beats the margin. The abstract and the letter repeat the stronger form ("so the text now says that the dropout gain is a coasting margin"). | M | "The dropout gain is thus matched by a coasting margin, a level effect that a count of missed updates gives without a covariance" (+2 words); letter: "matched by". |
| **M3** | V-E last sentence: "An earlier closed loop with dropouts, not matched at all" | Table S36's caption gives design caution F0/N 14.10/14.19 and 22.30/22.32 (matched in open loop without dropouts) and "open-loop caution difference under dropouts: not computed". The sprint's R4 wording was "not caution-matched". "Not matched at all" misstates the older closed loop. | M | "not matched in caution under dropouts" (+3 words), or "not caution-matched". |
| L1 | Table S30 rows "First/Second program's export: caution-matched closed loop with dropouts" | R-1 changed the phrase everywhere else. | L | "closed loop with dropouts, matched in open-loop caution". |
| L2 | Letter: R10 "Changes. Section V-D; Tables III and V"; R1 "Section V-D (all exploratory results, one table)"; R4 "printed in Tables II-V" | Stale after Table V moved to S18: V-D has no table now; "21% against 33%" is in V-E text, not in a table. | L | "Table III; Table S18"; "Section V-D (all exploratory results; table in Supplement S6)"; R4 "in Tables II-V and Section V-E". |
| L3 | Abstract: "these shares lie inside the same ±5% margin" | The replication's 3.0% has interval [0.0077, 0.0518], upper end above 0.05; V-E says "as point values", the abstract does not. | L | "these point values lie inside" (+1 word; cut "same"). |
| L4 | Contribution 2 and V-A | Sprint R9 asked for "as its near-constancy led one to expect; the test adds the bound" in contribution 2 (and the round-2 text had it in V-A); the fix build cut both. It survives in VI ("was expected from this constancy; what the test adds is the bound"). | L | Accept if the coordinator agrees VI is enough; else restore four words in contribution 2. |
| L5 | V-E mechanism paragraph: "on steady tracks the spread ranks the error the wrong way (Table V; descriptive)" | The steady-track τ (-0.075) is in Table S44, not Table V (Table V holds the all-pairs value). | L | "(Table V; Supplement S15)" (+2 words). |
| L6 | VI "These are level effects through the margin" | It follows a list that includes a mode probability and a spread, neither a margin. | L | "These are level-type effects" (word-neutral). |
| L7 | Table I and Table V caption | "failed (amendment)" is used (Table V: "failed") but defined nowhere. | L | Caption: "(A): passed; failed: not passed" (+3 words) or Table I row "failed (amendment)". |
| L8 | S15 post hoc check | "(102 of 20,000 resamples; two programs)" reads as if the Bonferroni check had two programs; only the count did. | L | "(check: one program; count 102 of 20,000: two)". |
| L9 | Table V caption | The Holm convention ((1 + k)/(n + 1) for all six) is not named; Table S38 does. | L | "(Supplement S15; (1 + k)/(n + 1))" (+3 words). |

Words: M1, M2, M3, L3, L5, L7 and L9 add about 25 words to the body, which has 50 spare. Candidate cuts if needed: "(both descriptive; Supplement S15)" in V-E, "dropout" before "start probability", "mostly" duplicates.

---

## 4. Regression check, sprint panel R1-R12

- **R1 (one label for amendment tests): survives.** "Confirmed" only in V-A, V-B, IV-E, Table I, Table II; amendment tests "passed (amendment)", "(A)", "replicated", "failed". L7 for "failed".
- **R2 (no dropout equivalence): survives.** "no equivalence test was registered for them"; the only "within the equivalence margin" is the coast-count difference, as A13 allows.
- **R3 (not found inside dropouts; conditions): survives.** In-dropout share 0.009 (2 Hz) and 0.035 (10 Hz) printed; "up to three updates ... longer gaps were not tested".
- **R4 (higher-level closed loop with dropouts): present and numbers stand in Table S36; wording M3.**
- **R5 (braking prediction's closed loop): survives outside the abstract** (V-C, VII), as the coordinator approved; the letter says so.
- **R6 (crossing "shows no recovery of a small room"): survives** (abstract, VII, contribution 2, V-E).
- **R7 (multiplicity; locks are not a registry): survives and improved** (IV-E; Holm named).
- **R8 (operating points flagged): survives** (V-C: "neither is a deployed operating point ... Equivalent here does not mean safe").
- **R9 (equivalence expected, said plainly): partly** (VI only; L4).
- **R10 (V-E split): survives** (six paragraphs; the 99% level is in Table V's caption).
- **R11 (no room is not support): survives** ("not a negative result"; "neither support nor contradict").
- **R12 (scope sentence): survives** (Limits "One simulated configuration ... 5 to 15 m/s"; VII "this one simulated configuration, at 2 Hz without latency").

---

## 5. Gate and caps

- BUILD_REPORT_v13.md: Result PASS (draft build 08:44:10).
- Typeset pages: **10** (PDF read with pdftotext: page 10 is the last; nothing on a page 11). Gate met.
- **Abstract: 250 words by my own count** (whitespace tokens of the paragraph after "## Abstract"), cap 250. Met, at the limit.
- Body 5,900 (cap 5,950); my count of prose lines after the abstract, excluding captions and tables, is 5,866, consistent. Whole manuscript 8,976 (my token count of the file: 8,976; cap 9,250). Supplement 20,837 (my token count: 20,837; cap 21,500). Index terms 5.
- Open markers 4 in the manuscript and supplement plus 1 in the letter, all E6 or A13-Holm slots, as the freeze note says.
- Caps equal the coordinator's of 22 Nov in Table S5's budget row.

---

## 6. Summary

H 1, M 3, L 9. One required item not fully fixed: R-5 (training-split τ not printed; the writer's reason is that no export pair holds it). Nothing in R-1 to R-14 regressed; sprint R9 is reduced to Section VI (L4). The H is a verification-status problem (lost ‡ marks), not a wrong number.
