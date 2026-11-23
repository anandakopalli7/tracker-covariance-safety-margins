# Claim audit v10: delta audit after the v09 fixes

- **Auditor:** Claude Fable 5.2 (`claude-fable-5-2`). The writer is Claude Opus 5.5.
- **Written:** 21 Nov 2026, after the 19:53 build.
- **Input audited:** the changed lines only, from `out\audit_v10_input\DIFF_MANUSCRIPT_v13.txt`, `DIFF_SUPPLEMENT_v13.txt` and `DIFF_RESPONSE_TO_REVIEW_v13.txt` (build report 19:53:10, PASS).
- **Checked against:** the exports X, DR, Y, E4 and S0 (every new value), AMENDMENT_11 (§3.8, §6c.5, §6c.11, §6d.5, §6d.7), the build report's word counts, and the manuscript of `out\freeze_v13_1301\` (for the Table S5 word-budget row only).
- **Not read:** `gen\`, `build\`. Nothing was built or edited; no external service was used.

**Result: both H and all 11 M findings of v09 are resolved. New findings: 0 H, 1 M, 2 L.**

**Numbers.** Every value added by the changed lines matches its export at the printed rounding and level. No number from an export is wrong. The one M finding is a count in a disclosure row ("two sections"), not a result value.

## 1. The v09 findings

| # | v09 rating | Status | New text (quoted) and check |
|---|---|---|---|
| 1 | H | Resolved, with one remainder (new finding N1) | Table S5: "existing captions, Table I, the abstract and two sections were shortened, and one exploratory figure moved to the supplement". The false "no existing text was cut" is gone. "Two" is too low: see N1 |
| 2 | H | Resolved | S14: "In pedestrian crossing the covariance's share is −0.432 and its amplitude-matched ranking oracle's 0.638, both with wide intervals; in vehicle crossing they are 0.165 and 0.226. Stored runs, not a test." All four match `S0.PC.RR_N`, `S0.PC.RR_E5N`, `S0.VC.RR_N`, `S0.VC.RR_E5N` and Table S31 |
| 3 | M | Resolved | §VII: "in closed loop with dropouts (not caution-matched) it was equivalent to the class average and, at the higher level (secondary), safer at no extra cost" |
| 4 | M | Resolved | §V-B: "its permuted twin is tested in Section V-E" |
| 5 | M | Resolved | §V-E: "under dropouts (open loop; lead braking, this mask law and output rule only) there is room" |
| 6 | M | Resolved | §V-E: "We read the bottleneck in both as the information in the covariance, not its amplitude." Labelled as a reading; "would allow" is gone; the crossing share and the dropout efficiency (0.071 [0.016, 0.129]) are printed in the clauses before it. The shorter form is acceptable |
| 7 | M | Resolved (see N2 for a remainder) | Contribution 2: "where the fixed-noise covariance varies more, it varies without rank information in pedestrian crossing and recovers a small 2.8% of the room under dropouts" |
| 8 | M | Resolved | Abstract: "it recovers none of a small room (0.16 points) in fresh pedestrian crossing". Matches A11 §3.8's row ("it recovers none of it"). The abstract is still 247 words |
| 9 | M | Resolved | Table S33: "Runs; evaluated decisions; runs with a contact: 390; 105,419; 1"; "The oracle minus its permuted twin (detection at the amplitude; second hypothesis) (C): 0.591 [0.382, 0.941]". Table S34: "0.253 [0.214, 0.296]" and "105; 21,574; 3,644". All match `X.PC.*` and `DR.*`; both differences are at the 95% level the exports record, as the captions say |
| 10 | M | Resolved (see N3 for a remainder) | Table S35's caption: "Design caution, F0 / N: 14.10 / 14.19% (lower level), 22.30 / 22.32% (higher level); open-loop caution difference under dropouts: not computed." Matches `E4.<F0|N>.<lo|hi>.caution` |
| 11 | M | Resolved | Table S35: N "−0.02 [−0.05, 0.00]; −0.10 [−0.18, −0.03]"; IMM "−0.02 [−0.05, 0.00]; −0.05 [−0.13, 0.02]". All four match `E4.did.*`; the exploratory label and the two-changes caveat are on both rows |
| 12 | M | Resolved | Letter: "Crossing was tested despite a pre-stated no-go, and the dropout test, the twin test and the re-tune were specified after the fresh lead-braking results were seen (Table S5)." |
| 13 | M | Resolved | Table S33: "Grid frontier: N's share; placebo at the runs' own median ratio; placebo at the lead-braking median: −0.067; −0.003; −0.005". Matches `X.PC.grid.RR_N`, `.RR_P`, `.RR_Prec` |
| 14 | L | Taken | "(nominal 99%, the plan's fallback)" |
| 15 | L | Not taken (pages). Reason accepted | Table S32 gives the class name beside the share |
| 16 | L | Taken | Table S32's caption: "a room is called small below a tenth of lead braking's" |
| 17 | L | Taken | §V-E: "(values in Supplement S14)"; the oracle's share and its 99% level are now in Table S33, and Table S32's caption no longer names a level for a value it does not print |
| 18 | L | Taken | "(recorded afterwards)" on the calibration-step row |
| 19 | L | Taken | "Specified on 21 Nov 2026, after…" (A11 §6c.11 gives this date) |
| 20 | L | Not taken (the author's title). Reason accepted | It must reach the author; I could not see whether the author items list it |
| 21 | L | Taken | "(by 0.0498 [0.0424, 0.0569]; specified after its share was seen)" |
| 22 | L | Taken | "where the fixed-noise covariance varies more" |
| 23 | L | Not taken (pages). Reason accepted | The counts are now in Table S33 |
| 24 | L | Taken | Captions of S33 and S34: "(descriptive unless marked (C); nominal 95% intervals unless stated)"; S36: "the difference is the test, the other rows descriptive; nominal 95% intervals". Levels match `Y.*.level` |
| 25 | L | Taken | "the supplement at most 15,000" is in "Planned"; S2 now reads "$(\mathrm{rank}(r_i) - 0.5)/n_r$ among the $n_r$ evaluated decisions of the run set that have such rows", which is A11 §6c.5's formula; the reading row is present and marked "recorded afterwards" |
| 26 | L | Not taken (pages). Reason accepted | The next clause, "in closed loop with dropouts", sets the dropout share apart as open loop |
| 27 | L | Not taken. Reason accepted | §V-E now carries the limit (finding 5); Limits stays general |

## 2. New findings

| # | Location | Sentence (quoted) | What is wrong | Rating | Fix, fewest words |
|---|---|---|---|---|---|
| N1 | Table S5, word-budget row | "existing captions, Table I, the abstract and two sections were shortened" | The count is too low. Against the 13:01 freeze, at least four prose sections lost existing text: §VII (the room, the 0.01% oracle, "99.7% of rows", the adaptive filter's 4.6%, the schedule's 92%, the closed-loop prediction and time gap, the 10 Hz sentence), §VI (the adaptive-filter sentence), §II (four trims) and Data availability (three trims). §I and the opening of §III were also reworded shorter | M | Replace "two sections" with "several sections" (same word count) |
| N2 | §I, contribution 2 | "it varies without rank information in pedestrian crossing" | The abstract was changed to "recovers none of a small room" (v09 finding 8), but this sentence keeps the stronger wording with neither the oracle's share nor the room's size. The conclusion keeps it too, but prints "its oracle: 69%" beside it | L | "it recovers none of the room in pedestrian crossing and a small 2.8% under dropouts" (three words fewer than now) |
| N3 | Table S35's caption | "Design caution, F0 / N: 14.10 / 14.19% (lower level), 22.30 / 22.32% (higher level)" | A11 §6d.5 asks for each arm's design caution. The table has IMM rows, and the two IMM arms are not given. The export has them: 13.94 / 14.09% (lower), 22.30 / 22.32% (higher); the lower-level IMM gap, 0.15 points, is the largest of the four | L | "Design caution, F0/N and the IMM pair: 14.10/14.19 and 13.94/14.09% (lower level), 22.30/22.32 and 22.30/22.32% (higher level)". Written without spaces round the slashes, this adds 2 tokens under the project counter; the supplement has 11 spare |

## 3. Changed lines checked without findings

- **Abstract.** The twin clause and the crossing clause; 247 words (build report).
- **§V-B.** The twin pointer.
- **§V-E.** The pointer to Supplement S14; the 99% note; the dropout limits; the reading sentence.
- **§VII.** The caveat.
- **Letter.** Word counts 5,570, 8,692, 247 and 16,189 match the build report; the disclosure sentence.
- **S2.** The mid-rank formula.
- **Table S5.** The dropout row's date; the mid-rank reading row; the calibration-step label; the word-budget row apart from N1 (caps 250, 5,650, 8,800 and 16,200 match the build).
- **S12.** The hand-check sentence ("all 20 within 1e-6 m").
- **S14.** The step-0 sentence; the captions of Tables S32, S33, S34, S35 and S36; the four new rows of S33; the three new rows of S34; the two difference-in-differences rows of S35.
