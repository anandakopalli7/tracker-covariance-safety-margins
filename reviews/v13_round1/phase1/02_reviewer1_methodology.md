# Peer Reviewer 1 (Methodology) — report on MANUSCRIPT_v13 / SUPPLEMENT_v13

- Seat: Peer Reviewer 1 (Methodology), internal id R1. Applied statistician and simulation-evaluation methodologist (resampling inference for non-smooth statistics, frontier comparisons, positive controls, planned versus exploratory analyses).
- Model: Claude Fable 5.2 (model id claude-fable-5-2).
- Date: 21 November 2026.
- Material read: the frozen manuscript (whole), the frozen supplement (whole), Figs. 1 to 4, the role definition; headings of the report template and the statistical reporting standards. Nothing else. Target: IEEE OJ-ITS regular paper, treated as a fresh submission.
- Calibration status: NOT_CALIBRATED.

## 1. Recommendation

**Major Revision. Confidence 4 of 5.**

The inference that carries the headline (the fixed-noise covariance's share of the room is zero to within about two decisions in 21,574) is robust to any plausible interval miscalibration, and the paper is unusually open about its deviations. But three constructs do less than the wording says: the positive control "at the tracker's amplitude" is run at a fixed ±5% band that is wider than the tracker's measured variation, the equivalence margin is about four times larger than what that positive control itself recovers, and the confirmed share of the braking prediction exists only in a pooled population whose room is mostly not present within any phase. Two of the three confirmatory families and the real logs could test nothing, the tested IMM is close to degenerate by its tuning rule, and the closed-loop "no extra cost" is estimated only on cases where the baseline did not crash; most of this is repairable by wording plus a small number of new values.

## 2. Strengths

- S1. Planned and exploratory work are separated and labelled throughout, with a fixed hypothesis sequence and explicit pass rules (Section IV-E; Table S4). The deviation table is complete in a way I rarely see, including one deviation found afterwards and four post-lock code fixes (Table S5).
- S2. The estimand is stated before the data: gridless step frontier, 201 caution levels recomputed inside every resample, share as a ratio of frontier distances (Section IV-B; Supplement S2 "Intervals and calibration"). Recomputing the caution levels in each resample is the right treatment of a data-dependent grid.
- S3. A positive control (oracle E), a small-amplitude control (E5) and a permuted twin (E5p) are part of the design, and the plan demands that the room exist before any equivalence is read (Table S4, first two rows of each family). Declining to test where the room is zero (cut-in, real logs) is the correct reading of a failed manipulation check (Section V-A; Table II).
- S4. Resampling is done over runs, cases and scenes, not over decisions, so within-run dependence of roughly 205 decisions per run is respected (Section IV-D).
- S5. The pooled-share fragility is disclosed with numbers, not hidden: the share while the ego moves and its dependence on how many after-stop seconds are kept (Section V-A; Table S10).
- S6. The post hoc change to the real-log clearance is flagged in the text, the table note and the limits, with the planned outcome printed beside it (Section III-C; Table II note; Table S27).
- S7. Closed-loop contact differences use a Newcombe paired interval; I could reproduce every printed interval from the counts (Section 4 below).
- S8. The headline numbers in the Abstract, Section I and Section VII match Tables II to V and the supplement in every case I checked (Section 4 below).

## 3. Weaknesses

### W1. The positive control is not run at the tracker's amplitude
- Severity: MAJOR.
- Location: Abstract; Section IV-C; Section V-A; Table I (E5 row); Table III (online CV row, column "Oracle c"); Supplement S2.
- Evidence: "the score detects rank information at the tracker covariance's own amplitude (confirmed)" (Section V-A).
- What is wrong: E5 is defined with a fixed band, f = 1.1029 (1 + 0.05(2u − 1)), that is ±5% around the tracker's median ratio. The tracker's own variation is far smaller: 99.9% of its binding rows lie within 5% of the median, and the oracle built at its own measured spread (Table III, online CV, c) recovers 0.0001 [0.0000, 0.0002], with a lower end that prints as zero. So detection is shown at the threshold of the "barely varies" flag, not at the amplitude the tracker actually has. At the tracker's real amplitude the paper shows the opposite of detection: perfect ranking is worth about 0.1 decision-equivalents. The second hypothesis is confirmed as worded in the plan, but the sentence in the Abstract and in Sections I, V-A and VII says more than E5 establishes.
- Fix: say "detects rank information within a ±5% band around the tracker's median margin" everywhere, and state beside it that at the tracker's own measured spread the ranking oracle recovers 0.0001 of the room. Print c for the online CV with more digits and with its permuted twin, so the reader can see whether it is distinguishable from zero.
- Needs: WORDING, plus one NEW VALUE (permuted twin and unrounded interval for the online CV's own-amplitude oracle).

### W2. The equivalence margin is not a severe test
- Severity: MAJOR.
- Location: Section IV-C; Section V-A; Table II; Abstract.
- Evidence: "it is equivalent to the class average within 5% of the room (confirmed)" (Section V-A).
- What is wrong: δ = 0.05 of the room is about 60 decision-equivalents. E5, a source with perfect rank information inside a ±5% band, recovers 0.013 [0.010, 0.015], about 16 decision-equivalents. A source carrying perfect information at that amplitude would therefore also be declared "equivalent". With 99.9% of rows within 5% of the median and a sweep that removes global scale, the hypothesis could not have failed; Section I itself says "a null is expected". The pre-registered equivalence is true but uninformative as a test. The data support a much stronger and more useful statement, the observed bound: |share| below 0.0015 at the 99.4% level, at most 1.8 decisions.
- Fix: lead with the observed interval and its decision-equivalents, describe the ±0.05 margin as the plan's criterion, and state plainly that the margin exceeds the positive control's own effect, so "equivalent within 5%" does not by itself exclude an informative covariance of small amplitude. The same remark applies to the IMM branch "amplitude-limited" (c inside ±δ).
- Needs: WORDING ONLY.

### W3. The room and the braking prediction's confirmed share are properties of the pooled population
- Severity: MAJOR.
- Location: Section V-A; Table II (CK3 row); Table S8; Table S10.
- Evidence: "each population on its own frontier, so values do not add" (Table S8 caption).
- What is wrong: converting Table S8's rooms to decision-equivalents gives 45.5 (before braking), 473.1 (braking) and 13.4 (stopped), 532 in total, against 1,204 pooled. More than half of the pooled room exists only when one margin scale is shared across phases, that is, it is room for reallocating caution between phases, which is what the per-phase schedule exploits (0.916). 16,781 of 21,574 decisions (78%) are stopped-lead decisions with a room of 0.08 points. The confirmed hypothesis "CK3 share above 0.5" passes only pooled: 0.411 [0.338, 0.488] while the ego moves (whole interval below 0.5), 0.242 / 0.656 / 0.000 by phase, and 0.244 when no after-stop decisions are kept. The confirmed outcome therefore depends on how long recordings run after the stop, a recording choice. The text discloses the numbers, but "recovers most of the room (confirmed)" is still the headline, and Table III reports "room by phase" as if phases partition the room.
- Fix: state in Section V-A and the Abstract that the pooled room is about 2.3 times the sum of the within-phase rooms, that the 0.5 threshold is met only in the pooled population, and that the ego-moving share is below 0.5. Add the decision-equivalent decomposition to Table S8.
- Needs: WORDING, plus NEW VALUE (decision-equivalents per population; these follow from printed numbers).

### W4. Partial-oracle grading fails in every sub-population, and the stated rule is not applied
- Severity: MAJOR.
- Location: Section IV-C (last sentence); Table S8 (last row); Section V-A.
- Evidence: "where they do not, shares are printed as decision-equivalents" (Section IV-C).
- What is wrong: the 25/50/75% partial oracles grade only in the pooled population (0.261 / 0.514 / 0.754). In the ego-moving, before-braking and braking populations the 25% mixture scores below the class average (−0.126, −0.319, −0.248) and the 50% mixture is near or below zero; in the stopped population shares exceed 1 (AM 1.074) and fall to −0.460 (TG). A score on which a quarter of oracle information looks worse than none is not a graded measure of information in those populations. Despite the rule quoted above, Table S8 prints shares there, Section V-A quotes 0.411 as a share, and Table III prints CK3 shares and rooms by phase. No explanation is offered for why grading holds pooled and fails in each part (a likely cause is that E's and F0's variances are on different scales, so a mixture at one common g is badly matched; if so the partial oracle, not the score, is at fault, but then it is not a valid check either).
- Fix: explain the failure; either rebuild the partial oracle so that both parts are caution-matched and report whether grading then holds, or apply the stated rule and print decision-equivalents in the non-grading populations, removing "share" for 0.411 and the phase values.
- Needs: NEW ANALYSIS (re-matched partial oracles) or, at minimum, WORDING and reformatted values.

### W5. The permuted twin is not information-free, and varying variants have no such twin
- Severity: MAJOR.
- Location: Table I (E5p row); Table II; Section V-B; Section VI; Supplement S2 and S4.
- Evidence: "E5 with the order permuted within runs" / "Same amplitude, no information" (Table I).
- What is wrong: E5 is 0.013 and E5 minus E5p is 0.008, so E5p itself recovers about 0.005 of the room, roughly 6 decision-equivalents, with no interval printed. Ranks are computed over the whole run set and permuted within runs, so E5p keeps the between-run component of the ranking; it is "no within-run information", not "no information". Alternatively or additionally, jitter alone gives a gridless minimum-over-scales frontier more attainable points. Either way, a varying margin without decision-level information can score a positive share on this estimand, about 40% of E5's. That matters for the one variant that does vary: the adaptive filter's r = 0.0459 [0.0390, 0.0533] is read as "recovers a small share" (Sections V-B and VI) without any permuted twin, so the reader cannot tell information from jitter. Its interval also straddles δ, and its oracle c = 0.0477 [0.0379, 0.0582] straddles δ too, which the plan's rule would call inconclusive on the c branch.
- Fix: print E5p's share with its interval; relabel it; add a within-run permutation of the adaptive filter's margin ratio (and a whole-set permutation of E5) and report the excess of r over it.
- Needs: NEW VALUE/analysis.

### W6. The tested IMM is close to degenerate by construction; title and abstract generalise
- Severity: MAJOR.
- Location: Title; Abstract; Section III-D; Supplement S4; Table S7.
- Evidence: "The NIS window could not be reached on the search grid" (Supplement S4, CA).
- What is wrong: the CA filter's acceleration process variance is 0.001, chosen by a rule that targets the median over runs of a whole-run mean NIS. That rule is dominated by steady phases and selects against manoeuvre response. An IMM of a CV filter and a nearly-CV CA filter cannot widen at a manoeuvre, and Table S7 confirms it: the IMM's NIS while the lead brakes is 9.24 [7.54, 11.02] against an expected 2, so the filter is inconsistent exactly where the room lies (23 to 29 points in the braking phase). The re-tuned CV's median NIS of 1.99 falls between two groups of runs with none inside the window. "An IMM tracker's covariance barely varies" is therefore a finding about this tuning rule, not about IMM covariances, yet the title names "Interacting-Multiple-Model Tracker Covariances" without qualification. The three transition-diagonal sensitivities (Table S6) do not touch the cause.
- Fix: qualify the title, Abstract and Section VII ("an IMM tuned to whole-run NIS"); report the mode probabilities and covariance ratio at braking onset; if feasible add, as exploratory, an IMM whose CA acceleration noise is tuned on the braking phase.
- Needs: WORDING, and preferably a NEW exploratory analysis.

### W7. Closed loop: "no extra cost" is conditioned on the baseline not crashing, and the baseline is mostly in fallback
- Severity: MAJOR.
- Location: Abstract; Section V-C; Table IV; Table S23; Supplement S2 "Matched settings".
- Evidence: "mean paired difference in time lost (s) over pairs without contact" (Table IV caption).
- What is wrong: (a) Time lost is compared only on pairs without contact. At the lower level F0 has contact in 12 of 60 cases, so the 12 hardest cases, where the braking prediction had to do something different, are dropped from the cost estimate. This is conditioning on a post-treatment outcome. The effect is visible in the paper's own numbers: the difference of arm means in Table S23 is +0.26 s for CK3 (24.78 against 24.52) but the paired value is +0.16 s; for TG it is 0.00 against −0.13. (b) F0 is in full braking in 52.7% of decisions at the lower level and 78.6% at the higher (CK3: 1.6% and 4.9%), with median peak deceleration above the planner's own 5 m/s² fallback. The comparator is a planner driven into bang-bang operation by levels chosen to produce contacts, so "safer at no extra cost" is relative to an unusual baseline. (c) Arms are "matched" on open-loop caution on the old evaluation runs by nearest grid scale; the realised caution of each matched arm is not printed, and the three texts name three bases (Section III-B "tuning cases", Table IV "design runs", Supplement S2 "old evaluation runs"). (d) The equivalence margin of ±0.10 in contact share is half of F0's 20% rate. (e) The closed-loop classifications have a blank status in Table S4 and sit in no sequence, yet the Abstract and contribution 2 ("A confirmatory test") state them in the same register as confirmed results; only Section VII adds "by the plan's rule".
- Fix: report cost on all 60 pairs with an outcome defined for both arms regardless of contact (for example time to the lead's stop line, or time lost censored at contact with a bounding analysis); print each matched arm's design caution and scale; reconcile the matching basis; mark closed-loop outcomes in the Abstract and Section I as classified by a planned rule outside the sequences.
- Needs: NEW VALUE/analysis and WORDING.

### W8. Two confirmatory families and the real logs could test nothing; the title presents them as tests
- Severity: MAJOR.
- Location: Title; Section III-A, III-C; Section V-A; Table II; Tables S18, S27.
- Evidence: "every curve is at zero wrong goes" (Fig. 2 caption).
- What is wrong: the cut-in generator produces no wrong go at any margin, including zero margin, in 105 runs, and exactly one decision on a track younger than 1 s (Table S18). The event rule was tuned on event counts only; whether the tuning cut-in runs had any room was evidently not checked before a confirmatory sequence was spent on them. On the real logs the oracle's room is −0.01 [−0.13, 0.13]: the positive control fails, after the horizon was chosen as the one at which the design split "showed room" with a lower end of 0.02 points, a selection that did not replicate. The base rates of wrong goes for cut-in and real logs are not printed. The evidence base is therefore one scenario family (a lead braking to a stop on a straight road, three speeds), where the null follows from the Riccati steady state. The title still reads "in Closed Loop and on Real Driving Logs". No sample size (105, 60, 20, 150) is justified by a power or precision argument; with 20 cases per variant and no contacts, the Newcombe interval is ±0.16, so "equivalent" (±0.10) was unattainable behind non-braking leads whatever happened (Table S25).
- Fix: retitle or qualify so that the real logs and cut-in are presented as attempted and uninformative; print wrong-go base rates at zero margin for all three data sets and the tuning-run room for cut-in; state the precision each n could deliver.
- Needs: WORDING, plus NEW VALUES (base rates; these should already exist).

### W9. Bootstrap: interval type, estimated coverages and the meaning of the 99% fallback are not reported
- Severity: MINOR.
- Location: Section IV-D; Supplement S2 "Intervals and calibration"; Table S9.
- Evidence: "otherwise the nominal 99% interval is used" (Supplement S2).
- What is wrong: the interval type (percentile, basic, BCa) is never stated. The estimated coverages from the double bootstrap are not printed, only the selected levels. The fallback applies exactly where calibration could not be stabilised (IMM share, cut-in N, real-log N), so the 99% interval there has unknown coverage; it is a convention, not a calibrated interval. The share is a ratio of sums of minima of step functions with a true value at or near zero, a non-smooth functional for which bootstrap consistency is not assured; the double bootstrap inherits that problem because it measures coverage of the plug-in value. Whether resampling is stratified by desired speed and recording margin (the fresh runs cycle three margins within family and speed) is not stated. None of this threatens the conclusions: every confirmatory interval is far from its threshold (N: ±0.0015 against ±0.05; CK3 lower end 0.720 against 0.5).
- Fix: state the interval type and stratification; add to Table S9 the estimated coverage of the nominal 95% interval and of the level used, with Monte Carlo SD; call the fallback "nominal 99%, coverage not established".
- Needs: NEW VALUE (coverages already computed) and WORDING.

### W10. Mixed interval levels are quoted in the text without their level
- Severity: MINOR.
- Location: Section V-A, V-B; Tables II, III.
- Evidence: "the IMM's covariance recovers 0.0000 [−0.0018, 0.0012]" (Section V-B).
- What is wrong: in one sentence of Section V-B a 95% interval (c) stands beside a 99% interval (r); Section V-A quotes N's 99.4% interval; Table III prints the same shares with 95% intervals ([−0.0007, 0.0010] and [−0.0013, 0.0009]). The levels appear only in Table S9. A reader comparing Table II with Table III sees two intervals for one quantity.
- Fix: add a level column or footnote marks to Table II and name the level at each quotation in the text.
- Needs: WORDING ONLY.

### W11. A classification step is labelled "confirmed"
- Severity: MINOR.
- Location: Table S4 (lead braking, fourth row); Section V-B.
- Evidence: "Classified (Section IV-C); passes unless inconclusive" (Table S4).
- What is wrong: a step that passes under three of four outcomes is a classification, not a hypothesis with a direction. Attaching "(confirmed)" to "amplitude-limited" suggests a directional claim was at risk. It also acts as a gate in the sequence that could hardly close.
- Fix: write "classified as amplitude-limited by the planned rule" and reserve "confirmed" for directional hypotheses.
- Needs: WORDING ONLY.

### W12. "Costs progress" hides a favourable trade, and the abstract does not mark these as outside the sequences
- Severity: MINOR.
- Location: Abstract; Section V-D; Supplement S8; Table S19.
- Evidence: "costs progress (1.7, −4.7)" (Table V).
- What is wrong: the open-loop rule has no category for a source that removes wrong goes at a cost. Behind stop-and-go leads the braking prediction removes 4.7 points of wrong goes for 1.7 points of caution, with a caution lower end of 1.1 against a threshold of 1; it gets the same label as the per-phase schedule's 35 to 53 points of caution for nothing. The Abstract's "costs progress behind constant-speed, mildly braking and stop-and-go leads" compresses this, and these classifications are outside the confirmatory sequences (Section V-D says so; the Abstract does not). In closed loop the same lead type is "safer at a cost".
- Fix: in the Abstract say "costs progress behind constant-speed and mildly braking leads, and trades progress for safety behind stop-and-go leads", and mark the status.
- Needs: WORDING ONLY.

### W13. The update-rate comparison confounds rate with latency; "after-stop room" is undefined
- Severity: MINOR.
- Location: Section V-D "Update rate and latency"; Table V; Table S16; Fig. 4a.
- Evidence: "The after-stop room is largely a consequence of the 2 Hz update." (Section V-D).
- What is wrong: the text compares 2 Hz without latency against 5 and 10 Hz with 0.1 s latency. Like for like at 0.1 s the room goes 5.89, 5.31, 5.07; at 0 s it goes 5.58, 4.99, 4.75. At 10 Hz with 0.2 s latency 130.5 of 173.4 after-stop decision-equivalents remain (75%), so state age matters about as much as rate. The total room falls by only 14 to 15% from 2 to 10 Hz, which sits oddly with "Magnitudes depend on 2 Hz updates" in the Abstract. Separately, "after-stop room" is never defined in the manuscript or supplement, and 173.4 decision-equivalents cannot be the room of the "stopped" population in Table S8 (0.08 points of 16,781 decisions, 13.4).
- Fix: compare at equal latency, say "state age (update interval plus latency)", and define the after-stop room.
- Needs: WORDING ONLY.

### W14. Caution is averaged over a set that depends on the outcome
- Severity: MINOR.
- Location: Section IV-A; Table S10 (signed caution).
- Evidence: "averaged over decisions whose selected row is truly safe" (Section IV-A).
- What is wrong: a source that converts wrong goes into safe decisions changes the set over which its caution is averaged, so "equal caution" compares averages over different decision subsets for different sources. The signed-caution sensitivity (room 4.89, N 0.0000, CK3 0.764) indicates the conclusions survive, but the choice and its consequence are not discussed in the main text. About 1.05% of decisions remain wrong goes for every source including the oracle at the highest caution (Fig. 2), and the room depends on the caution range (6.00 / 7.03 / 7.17 points when capped).
- Fix: one sentence in Section IV-A stating the conditioning, pointing to the signed-caution result, and noting the irreducible floor.
- Needs: WORDING ONLY.

### W15. Verification and priority claims are weaker than they read
- Severity: MINOR.
- Location: Section IV-E; Supplement S3, S12; Table S5.
- Evidence: "they share the scoring library, stored arrays and resample draws" (Section IV-E).
- What is wrong: agreement of two programs that share the library, arrays and draws checks transcription and orchestration, not the scoring. The supplement records a case where exactly this failed ("the second program had shared the cache and did not catch it"). The only library-independent check is the true clearance of F0's selection at g = 1 on 20 decisions; caution, the frontier, the room and the share have no independent recount. "Recount every printed value" also sits beside many ‡ values computed by one program (S4, S7, S13 to S15). The plan's priority rests on SHA-256 hashes and file times in the author's own deposit, with no third-party timestamp; plan, both lock stages, runs, scoring and text all fall within about two days.
- Fix: describe the second programs as a recount on shared components; add a library-independent recomputation of room and one share on a small subset; state whether any external timestamp of the plan hash exists.
- Needs: WORDING, plus a small NEW check.

### W16. The real-log clearance change removes thousands of contacts and should carry its count in the main text
- Severity: MINOR.
- Location: Section III-C; Table S27.
- Evidence: "contacts with actors behind the ego were no longer counted" (Section III-C).
- What is wrong: on the design split the change turns 6,122 of F0's decisions at g = 1 from unsafe to safe at 3 s (Table S27). That is a change of the outcome definition after seeing a result on the split that also set the class averages and horizon. It is disclosed and the held-out split was unread, so the held-out result is not contaminated in the usual sense, but the real-log arm then yields a failed positive control and should be described as a failed test bed, not as a replication.
- Fix: put the count in Section III-C and call the real-log arm uninformative.
- Needs: WORDING ONLY.

## 4. Arithmetic and consistency checks

Checks that agree:
1. Room in decision-equivalents: 5.58/100 × 21,574 = 1,203.8; printed "about 1,204". Agrees.
2. N's frontier distance: −0.0009 × 1,203.8 = −1.08 and 0.0015 × 1,203.8 = 1.81; printed [−1.1, 1.8]. Agrees.
3. Populations in Table S8: 2,790 + 2,003 + 16,781 = 21,574. Agrees.
4. Brake test errors: 3.83/3.86, 12.61/12.79, 26.22/26.70 give 0.8%, 1.4%, 1.8%; printed 1%, 1%, 2%, "largest error 2%". Agrees.
5. Calibration shares on 30 cases (40, 37, 27, 17, 7, 0%) are all attainable as k/30; g = 4 is nearest 0.20 and g = 16 nearest 0.05. Agrees.
6. Table IV contact shares on 60 cases (20% = 12, 18% = 11, 5% = 3, 8% = 5, 10% = 6) are attainable. Agrees.
7. Newcombe paired intervals recomputed from counts (minimal discordance): N lower −0.017 [−0.076, 0.040]; CK3 lower −0.200 [−0.318, −0.099]; IMM lower 0.000 [−0.048, 0.048]; N higher 0.000 [−0.063, 0.063]; CK3 higher −0.050 [−0.137, 0.019]; IMM higher −0.017 [−0.086, 0.046]; n = 20 with no contacts 0.00 [−0.161, 0.161]; 0 against 5 of 20: −0.25 [−0.469, −0.038]; 5 against 5 of 20: [−0.121, 0.121]. All agree with Tables IV and S25 after rounding. (TG behind stop-and-go leads, printed [−0.42, 0.02]: reproducible only with some discordant pairs in both directions; consistent, not a mismatch.)
8. Abstract, Section I and Section VII against tables: 5.58 [4.99, 6.17]; 99.7%; 0.0009; 0.783; 0.916. All match Tables II and III.
9. Section V-B variant values against Table III (−0.0009, −0.0008, 0.0459; 0.0002, 0.0027, 0.0477; 21.5%). Match. "0.046" in Section VI is 0.0459 rounded.
10. Section V-D and Table V against Tables S14, S16, S19, S12: 0.101 [0.068, 0.134]; 0.072 / 0.168 / 0.055; 0.334; 6%; 5.58 / 5.31 / 5.07; 173.4 / 115.2 / 77.8; 0.0000 [−0.0004, 0.0006]; 238.1 / 153.0; 0.753 / 0.816; all six non-braking pairs; 1.16; 0.379. Match.
11. After-stop sensitivity "0.244 to 0.774" against Table S10. Match.
12. Table III online CV room by phase 1.63 / 23.62 / 0.08 against Table S8. Match.
13. Hypothesis order in Section IV-E against Table S4. Match.
14. Fig. 3 point positions against Table IV. Match by eye.

Mismatches, gaps and oddities:
- M1. Table V, "old evaluation" column: room 5.51, CK3 0.837, N −0.0004. The only old-evaluation table in the supplement (S13) prints 5.56, 0.831 and 0.00122 on a different estimand (grid frontier, truth phases). The Table V values are therefore not reproduced anywhere in the supplement, although the caption points to it.
- M2. Table S13, share of N, all decisions: 0.00122 [−0.00108, 0.00119]. The point estimate lies above its own interval's upper end.
- M3. Within-phase rooms in decision-equivalents sum to 532.0 (45.5 + 473.1 + 13.4) against 1,203.8 pooled (see W3). Not an error, but nowhere stated.
- M4. "After-stop room" 173.4 decision-equivalents (Tables V, S16) against the stopped population's room of 13.4 decision-equivalents (Table S8): different, undefined quantity (see W13).
- M5. Run counts: Table S28 uses 223 runs (55 + 55 + 20 + 20 + 51 + 22); Table S5 and S4 "Identity" speak of "155 distinct runs" (120 tuning + 35 old evaluation); Section III-A lists old evaluation runs as "35 lead-braking runs". Old evaluation runs of other families (about 68) appear in S28 but in no other count.
- M6. The same share with two intervals: N 0.0000 [−0.0009, 0.0015] (Table II, 99.4%) and [−0.0007, 0.0010] (Tables III, S8, S16, 95%); IMM [−0.0018, 0.0012] (99%) and [−0.0013, 0.0009] (95%). Consistent once Table S9 is read, but unlabelled in the main text (see W10).
- M7. den₀ against "relative to 3 s" in Table S14: den₀/relative ranges from 1,167 to 1,271, not the 1,204 of the 3 s room, so the two columns use different oracles (O and E). Not an error, but the relation is not explained; 123.9/1,203.8 = 0.103 while 0.101 is printed.
- M8. Tercile den₀ values sum to 123.1 against 123.9 for all (separate frontiers; acceptable). The tercile pattern is non-monotone (0.072 / 0.168 / 0.055) and differs from the old runs (0.203 / 0.021 / 0.053), so it supports no statement about deceleration.
- M9. Matching basis for the closed loop named three ways: "tuning cases" (Section III-B), "design runs" (Table IV caption), "old evaluation runs" (Supplement S2).
- M10. Table II mixes estimands: the per-phase schedule is on the grid frontier, all else gridless (stated in the caption). The Abstract places 0.916 beside 0.783 without that note.
- M11. Table S13 header "Room $R$ (pp" lacks a closing parenthesis. Table S18's caption says "the young-track test is in Table II", where it is "n.t.".
- M12. Table S11 "Single scale, same rule −0.002 [−0.005, −0.002]": point estimate at the interval's upper end.
- M13. Fig. 2: the IMM curve sits about 0.5 points above F0 across the range because it is another tracker with another class average; the legend entry "F0 (IMM)" overlaps it completely. Acceptable, but the room printed in the Abstract (5.58) is not the IMM's room, and the IMM's pooled room is printed nowhere (Table III gives only its room by phase), so "0.0009 of the room" in the Abstract refers to an unprinted denominator.
- M14. Abstract: "99.7% of rows" is, per Table III, 99.7% of binding rows.

No bounded-procedure statistics (t, F, chi-square with p, means with SD on integer scales, df) are reported, so no GRIM, GRIMMER, p-from-statistic or N-from-df recomputation applies.

## 5. Questions for the author

1. What is the online CV tracker's own measured amplitude A (q95 − q05 over 2m), and what are its own-amplitude oracle's share and permuted twin to four significant digits? Why was E5's band fixed at ±5% and not at that measured value?
2. What is E5p's share with its interval, and why is it positive? Is it between-run rank information retained by within-run permutation, or an effect of jitter on the gridless minimum?
3. What does a within-run permutation of the adaptive filter's margin ratio score on its own room?
4. Why do the partial oracles grade in the pooled population and score below the class average in every sub-population? How are the oracle and class-average parts placed on one margin scale?
5. Which bootstrap interval type is used? Is resampling stratified by desired speed and recording margin? What were the estimated coverages behind each row of Table S9, including the three fallback rows?
6. Was the room on the cut-in tuning runs computed before the plan was locked? What is the wrong-go share at zero margin in the cut-in event window and on the held-out nuScenes scenes?
7. In closed loop, what are the time-lost differences on all 60 pairs under a definition that is valid with contact? What scale and design caution did each "matched" arm receive, and which run set defined the match?
8. How do the IMM's mode probabilities and its covariance ratio behave in the second after braking onset? Was any tuning of the CA acceleration noise on the braking phase considered?
9. How is "after-stop room" defined, and how does it relate to the stopped population of Table S8?
10. Where do the old-evaluation values of Table V (5.51, 0.837, −0.0004) come from, and why does the N share in Table S13 lie outside its interval?
11. Does any third-party timestamp exist for the plan hash and the two lock hashes?
12. Why is F0 in full braking in 53% and 79% of closed-loop decisions, and is a baseline in that regime a fair comparator for "no extra cost"?
