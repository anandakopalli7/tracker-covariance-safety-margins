# Methodology Review Card (Peer Reviewer 1), Phase 2

contract_role: methodology

## Dimension Scores

### D1: methodology_rigor
score: warn
trigger: "Reporting or robustness gaps that do not threaten a headline conclusion"
Basis: the design isolates the stated comparison, every interval resamples the true independent unit (the run), and the non-smooth tracker-covariance share is diagnosed and calibrated. The two Major defects (W1, W2) and the Minor ones weaken the inferential footing of the headline interval and the generality of the reported magnitudes. None plausibly reverses the null, the existence of the room, or its dependence on the commitment.

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: warn
trigger: "Local overstatement or loose wording that leaves the central thesis intact"
Basis: the central thesis (this covariance is a near-constant multiple of a class average and recovers no measurable room) matches the evidence at every scoring. Equivalence wording rests on a bound chosen after the values were read (W4), one secondary equivalence is read from overlapping marginal intervals (W7), and sub-population shares are interpreted where the paper's own grading check fails (W8).

### D4: cross_disciplinary_relevance
score: not_assessed

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

### Reviewer identity, scope and status

Statistician specialising in resampling inference for clustered and non-smooth statistics (cluster bootstrap, double bootstrap, subsampling) and in the design of simulation-based evaluation studies. Focus items: the run-level bootstrap and calibrated interval for RR(N); the equal-caution frontier construction; separation of confirmatory and added analyses; the reaction-and-stop scoring, plan extension and den₀ evaluability rule; the off-policy status of the evaluation runs. Not assessed: domain significance and regulatory context. No venue criteria were bound for this call, so this card makes no venue-alignment claim. Calibration status: `NOT_CALIBRATED`.

### Summary assessment

The design is sound for its question. Decisions are scored against a logged future of a lead whose motion is independent of the ego, so a counterfactual row can be scored without a behaviour model. Margin sources are compared at equal caution by sweeping a common scale. An oracle positive control is shown to grade partial information in the pooled population. Every interval resamples the 35 runs and recomputes the caution levels, and the paper reports a double bootstrap, basic, stratified, leave-one-out and subsampling intervals for the non-smooth tracker-covariance share. Plans are hashed and deviations are logged item by item. The null for the tracker covariance is robust: the margin ratio is near-constant, and every estimate lies within a few decisions of zero.

Two defects matter. First (W1), the non-smoothness of RR(N) is plausibly a deterministic artefact of comparing two step frontiers that sample one (caution, wrong-go) path at grid points offset by 3.4 steps. The double-bootstrap calibration used to repair it then lacks its own justification. A grid-free frontier or an information-free placebo source would remove the problem at its source. Second (W2), the main text omits that on the 20 tuning runs, recorded under another planner, the room is 1.18 rather than 5.56 points, the room left with a 0.75 s stop is 2.3% rather than 12%, and the braking prediction's share is 0.38 rather than 0.83. The paper's own lesson about conditional open-loop scores therefore needs the data-collecting policy added. The remaining findings are Minor.

### Configured special interest: is the null bounded, and was the bound fixed in advance?

Partly bounded; the bound was not fixed in advance. For the 3 s commitment the first plan fixed only a three-decimal print of RR(N) (Table S4). The paper now gives the point 0.0012, the calibrated interval [−0.0016, 0.0017], and the statement that no interval method reaches 0.5% of the room. Nothing shows that 0.5% was fixed before the Section S10.1 values were read: the earlier draft's bound was 0.4% from the basic interval, and the new subsampling end of 0.0047 exceeds 0.4% and sits just under 0.5% (W4). Under the reaction-and-stop scoring, the second plan fixed a bounded reporting rule ("the data allowing at most u", Section S8.1, rule 3). That rule bounds by the observed upper limit, not by an a-priori margin. No equivalence margin was fixed anywhere. Substantively the null holds under any reasonable margin: the largest upper end from any method, 0.0047 of the room, is 2.2 of 8,290 decisions.

### S1: Interval validity checked rather than assumed for the non-smooth share
- **Evidence Anchor**: table: Supplement Table S16 (double-bootstrap coverage and calibrated intervals)

The paper resamples runs, the correct clustering unit, recomputes the 201 caution levels in each resample, and estimates coverage by a 2,000 × 1,000 double bootstrap. It shows that the step-frontier share of N covers in only 53% (percentile) and 52% (basic) of outer samples, flags the point lying outside its percentile interval, and reports stratified, 30-run, leave-one-out and subsampling alternatives (Table S17). Few simulation papers diagnose non-smoothness at all.

### S2: A positive control that is itself validated
- **Evidence Anchor**: text: §IV-B "A margin that takes the oracle's value on a random 25%, 50% or 75% of the decisions"

Partial oracles recover 0.27, 0.54 and 0.78 of the pooled room, with draw-to-draw ranges in Table S12b. This shows that the pooled measure grades partial information, so the null is not a blunt-measure artefact. The paper also reports, against its own interest, where the grading fails.

### S3: Pre-specification with hashes and an itemised deviation log
- **Evidence Anchor**: text: Supplement S4 "a lock manifest recorded the hashes of the code, the inputs, the forecast and the plan"

Two plans are hashed, the NIS-inflated claim wording was fixed as ordered rules and applied as fixed (rule 5), and Table S4 lists every reporting change beside the wording it replaced. Its timing corrections ("computed under this scoring", the earlier exploratory look at the room) are exemplary disclosure.

### S4: A ground-truth-free mechanism check that explains the null
- **Evidence Anchor**: figure: Fig. 2(b)

The ratio of N's margin to F0's at the binding constraint (median 1.1029; 99.26% of 152,264 rows within 5%) explains why a swept global scale leaves almost nothing for the covariance to change. Its extension to other families (Table V) is correctly labelled as untested at decision level.

### S5: An explicit, sensitivity-tested evaluability rule
- **Evidence Anchor**: text: §IV-C "a threshold of 5 would change nothing"

The den₀ resolution rule is fixed in advance, its threshold is called a judgement, and the shares that a threshold of 5 or 20 would change are named. The lower-limit version is also reported (Section S10.2).

### S6: Plan extension past the 3 s window, with a censoring sensitivity
- **Evidence Anchor**: table: Supplement Table S19

Stops that end after the window are continued and judged against the logged truth. The 153 pairs whose recording ends first are reported, and counting them unsafe gives 0.144 against 0.122. The overstated count (ii) is withdrawn, with 28 of 5,356 pairs shown to be unsafe.

### S7: Independent re-implementation
- **Evidence Anchor**: text: Supplement S10.9 "A second program was written from the written definitions and the paper, without access to the first program or its outputs"

Several thousand values agree to 10⁻⁹ across programs. One scaling error was found and corrected, and the limits of independence (shared geometry functions, scripts written after files were opened) are stated.

### W1: The non-smooth RR(N) is plausibly a grid-interleaving artefact, and its double-bootstrap calibration is not justified
- **Severity**: Major
- **Evidence Anchor**: text: §V-A "The step-frontier statistic is non-smooth, and nominal 95% intervals are not valid for it"
- **Confidence**: 4 — resampling inference for non-smooth statistics; grid arithmetic recomputed from the printed sweep and ratio

By the paper's own ratio check, N's margin is 1.1029 times F0's on 99.26% of binding rows, so N at scale g selects what F0 selects at about 1.1029² g = 1.216 g. The sweep is log-spaced with step ratio 10^(5/200) = 1.059, so N's 202 operating points sample F0's (caution, wrong-go) path at an offset of 3.40 grid steps: a fractional offset of 0.40 step, plus an end effect where N reaches about 1.2 times F0's largest scale. Two step frontiers drawn through interleaved samples of one path differ by discretisation jitter. Its average over levels is near zero, but its full-sample value depends on where the grid points happen to fall. The lower strip of Fig. 2(a), where N's difference oscillates about zero with mean 0.0068 points, looks like this jitter. So does Section S10.1's finding that the full-sample value sits at the 97.7th percentile of its own bootstrap distribution, whose median is 0.0001.

If so, the double bootstrap is calibrating intervals to cover a grid artefact. Its validity requires the outer-level relation between resample and full-sample values to mirror the relation between the full-sample value and the population quantity, which is exactly what fails here. The calibrated level 0.996 is read from inner intervals of 1,000 resamples, that is, from the second-smallest and second-largest inner values, with no Monte Carlo error reported for the level. The subsampling upper ends rise with m (0.0033, 0.0038, 0.0047), which suggests that the assumed root-n rate does not hold. The abstract's "calibrated interval −0.2% to 0.2%" therefore lacks a demonstrated coverage property. The null itself is not in question.

Remedy, using the stored arrays: (i) add a placebo source, F0 with its variance multiplied by 1.1029². It is information-identical to F0 but sampled at N's grid phase. Report RR(N) − RR(placebo) as the covariance's information effect. (ii) Alternatively, compute every frontier exactly from the per-decision critical scales g*, at which selections change, which removes the grid altogether. (iii) Report the Monte Carlo error of the calibrated level, or use an m-out-of-n bootstrap with an estimated rate.

### W2: The main text omits that the room, the commitment ratio and the braking prediction's share are several times smaller on runs recorded under another planner
- **Severity**: Major
- **Evidence Anchor**: table: Supplement Table S2, tuning and evaluation columns (3 s commitment and τ = 0.75 s rows)
- **Confidence**: 4 — values read directly from Tables S2, S3 and S25(b) and recomputed

On the 20 tuning runs, recorded with α = 0.105 and a unit variance, the 3 s room is 237.24/201 = 1.18 points, against 1,116.91/201 = 5.56 on the evaluation runs. The room left with a stop 0.75 s after committing is 0.023 of the 3 s room, against 0.121 (Table S2). The braking prediction's pooled share is 0.377 [−0.204, 0.840] (Table S25(b)), against 0.831. Within the evaluation runs the room also moves with the recording setting (4.71, 4.64 and 6.76 points; Table S3). None of these comparisons appears in the main text, and Table S2 is not cited there.

Tuning and evaluation runs differ in recording planner and in scenario draws, so the design cannot separate the two. Still, a positive control 4.7 times smaller, a commitment ratio 5 times smaller and a braking share half as large on another run set are material to how the abstract's 5.6 points, 12% and 83% generalise. The paper rightly frames every share as open-loop and off-policy, but its lesson that a score should state "its commitment and its population mix" omits the data-collecting policy, which these tables show to matter as much.

Remedy: report the tuning-run values beside the evaluation-run values in Sections V-A, V-B and V-D. Add the recording policy to the conditions named in the Discussion, Conclusion and abstract. If feasible, decompose the tuning-against-evaluation gap by phase mix and contact-terminated runs, as Table S22 does for the after-stop segment.

### W3: The 89% per-phase result is an in-sample envelope whose optimism is not quantified
- **Severity**: Minor
- **Evidence Anchor**: text: §V-C "we let every source use one margin scale per phase of the lead's motion and took its frontier over all triples of scales"
- **Confidence**: 3 — the size of the optimism is unknown; the mechanism is standard

The per-phase frontier is the envelope over 202³ (about 8.2 million) scale triples, each scored on the evaluation runs' realised outcomes. At each caution level the best split of caution among phases is chosen with outcome knowledge, and the phase labels come from the logged truth (which the paper notes). The single-scale frontier has one free parameter, the per-phase frontier three. Part of the 4.96-point gain may therefore be in-sample optimisation, which a 400-resample bootstrap that re-optimises in each resample does not remove. The independent 2.6-fold ratio of pooled to phase-weighted room supports the qualitative reading, so the conclusion that most of the pooled room is cross-phase allocation probably survives. Remedy: choose the per-phase scale ratios out of sample (leave-runs-out cross-validation within the evaluation runs, given W2), report the held-out gain beside 0.89, and label 0.89 as an in-sample upper value.

### W4: The 0.5% bound on the null was not fixed before the values were read, and the equivalence wording names no margin
- **Severity**: Minor
- **Evidence Anchor**: text: §V-A "no interval method we tried reaches 0.5% of the room"
- **Confidence**: 4 — inferred from Table S4, Section S10.1 and Table S17; the S10 amendment text itself is not in the package

The sentence reads as an equivalence statement, and the Discussion says "a class average does as well as the tracker's covariance". Section S10.1 states only that the choice of the calibrated percentile interval was fixed in advance. The earlier draft's bound was "at most about 0.4%" (Table S4), and the subsampling end that this revision added, 0.0047, would have broken that bound. The new bound sits just above it.

A defensible a-priori margin exists in the paper's own terms. One decision-equivalent is 1/460.66 = 0.0022 of the room, the resolution on which Section S8.1 bases its evaluability rule. Against ±1 decision-equivalent, the calibrated interval passes, but the basic interval (0.0035) and the subsampling ends (0.0033–0.0047) do not; against ±2.5 decision-equivalents, every method passes. Remedy: state when 0.5% was chosen. Adopt a margin justified in decision units, with its provenance, and phrase the null as equivalence within that margin (or as the largest upper end across methods, 2.2 decisions).

### W5: "Slightly narrow" understates the undercoverage of every interval for N's shares
- **Severity**: Minor
- **Evidence Anchor**: text: §IV-B "all other intervals should be read as slightly narrow"
- **Confidence**: 4 — follows from Table S16 and Fig. 4(b)

The 92–93% coverage applies to the smooth shares. For N the double bootstrap gives 53%, and the same step-frontier statistic appears in RR₀(N) of Tables III and IV. Fig. 4(b) shows the point at the upper end of its interval at τ = 1.5 and 1.8 s, and RR₀(N) also appears in the per-phase cells of Table S5 and in Table S24. There the lead-braking cell [0.001, 0.013] is the one interval that excludes zero. The paper's caveat for that cell is right. The general sentence should say that nominal intervals for N's shares are not valid at their nominal level, and that cell should not be read as a signal.

### W6: Most quantitative statements of the abstract rest on analyses added after the first results, and the abstract does not say so
- **Severity**: Minor
- **Evidence Anchor**: text: §IV-D "The analyses of Supplement S10 were added last, each defined before its values were read."
- **Confidence**: 4 — counted from the abstract, Section IV-D, Table S4 and Sections S8–S10

Added after the first results were: the second plan (reaction-and-stop scoring of all sources, perfect oracles, graded oracles, signed caution, deviation check; Tables S9–S15 and S29), then eight S10 subsections (Tables S12b and S16–S27). Of the abstract's seven quantitative statements, six rest wholly or partly on these analyses: the calibrated intervals, 89%, 29%, 12% and the family ratio check. Contributions 2 and 4 rest on them entirely. Section IV-D and the Conclusion label them descriptive, which is good, but the abstract and the contribution list do not. The S10 amendment's hash and date are not printed, although both earlier plans' hashes are. Parts of the verification were not blind: 511 values come from a script written after the result files were opened, and the second program for Table S24b was written after the first's values were known (Sections S10.5 and S10.9). Remedy: mark contributions 2 and 4 and the corresponding abstract sentences as exploratory, and print the S10 amendment's hash and date.

### W7: A secondary equivalence is read from overlapping marginal intervals
- **Severity**: Minor
- **Evidence Anchor**: text: §V-E "ranks the realised error (Spearman's ρ = 0.453 [0.392, 0.508]) no better than the class average's does"
- **Confidence**: 4 — standard paired-comparison reasoning

The two correlations are computed on the same 755 decisions from deviations whose ratio stays within 1.02–1.05, so their difference has a far narrower interval than either. "No better than" is probably right, but it is an equivalence claim made without a paired interval or a margin. Remedy: report the paired run-bootstrap interval of ρ_N − ρ_F0, or say only that the two estimates are nearly equal.

### W8: Shares are interpreted in populations where the paper's own grading check fails
- **Severity**: Minor
- **Evidence Anchor**: text: §VI "With caution counted at its signed value, its share while the lead brakes falls from 0.61 to 0.35."
- **Confidence**: 4 — read from Table II, Table S12 and Section VI

Section VI asks that a measure be shown to grade partial information "in every population whose shares are interpreted". With the ego moving and while the lead brakes, the partial oracles give −0.11, 0.05, 0.44 and −0.68, −0.63, 0.05 (Table II). Under the reaction-and-stop scoring with the ego moving they give −0.41, −0.30, 0.23 (Table S12). Sections V-B, V-D and VI nonetheless use the braking prediction's shares there (0.47, 0.61; signed 0.30, 0.35; 0.04 and −0.89) to qualify the pooled 83%. Section IV-B's reading, that there a share measures what one margin scale can use, is defensible, but it should accompany each such sentence. Alternatively, give the qualifiers in decision-equivalents.

### W9: Frontier-construction sensitivities are given in the main text for NA only
- **Severity**: Minor
- **Evidence Anchor**: table: Supplement Table S5, hull column and footnote
- **Confidence**: 4 — read from Table S5

Prepending F0's zero-margin point is sound. At g = 0 every variance-only source selects the same rows, so the rule is a no-op for N, NA, AM, Q and E, and matters only for CK3, which cannot reach caution below 1.72%. Its alternates, however, move magnitudes by more than the stated intervals and are given only in Table S5: CK3 0.831 (prepended), 0.790 (F0's point replacing its own) and 0.750 (hull); AM 0.376 (step) and 0.153 [0.078, 0.232] (hull). Remedy: give these beside 0.83 and 0.38 in Section V-B, as is done for NA.

### W10: Under the reaction-and-stop scoring, the caution axis is defined by the other scoring
- **Severity**: Minor
- **Evidence Anchor**: text: §IV-C "Only the wrong-go flag changes: caution keeps the 3 s scoring's definition."
- **Confidence**: 3 — design reasoning; the size of the effect outside the reported sensitivity is unknown

Caution is averaged over selections that are safe under the 3 s commitment. Under reaction-and-stop, a selection that is safe under that scoring but unsafe over 3 s therefore drops out of the caution average, so the two axes of the equal-caution comparison are scored differently, and the decision set behind the caution average varies with source and scale. The signed-caution sensitivity (Table S20c) shows that this matters in sub-populations: the braking prediction's ego-moving share goes from 0.04 to −0.89. Remedy: add a variant in which caution is averaged over selections safe under the scoring in use, or state why the 3 s definition is the right reference.

### W11: Code, data and recordings are not yet available for review
- **Severity**: Minor
- **Evidence Anchor**: text: Data and Code Availability "The raw recordings are available from the author on request."
- **Confidence**: 4 — read from the availability statement

The repository and DOI are placeholders, the planner library is an in-house re-implementation, and the raw recordings are available only on request. The described deposit (both plans with hashes, per-decision arrays, second programs, result files) would suffice for regenerating every number. It should exist, with a reviewer-accessible link, before acceptance, and the recordings should be deposited or the restriction justified.

### W12: The tracker covariance is also off-policy, contrary to the implication of Section III-B
- **Severity**: Minor
- **Evidence Anchor**: text: §III-B "visited by a planner whose margin used the tracker's covariance; for every other source they are off-policy"
- **Confidence**: 3 — follows from the stated recording margin; the relative size of the p and q terms is not reported

The recording margin was d² ≥ αp + βq with α = β, whereas the scored source N uses g·p with no allowance term. At no g is it the recording policy, so N's evaluation states are off-policy too. The paper's later sentence that every share is off-policy is correct; the clause should not single out N, and it would help to report how often the recording planner's selection coincides with N's at some g.

### Criterion-bound judgements

| Dimension / criterion | Criterion source | Judgement | Evidence anchors | Rationale | Uncertainty or scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| Run bootstrap, double bootstrap, calibrated interval for RR(N) | Configuration Card, focus 1 | PARTLY_MEETS | see S1, W1, W5 | Correct clustering unit and honest diagnosis; calibration of a likely grid artefact is unjustified | Artefact inferred from the grid arithmetic and Fig. 2(a), not run | yes: the abstract's interval |
| Equal-caution frontier (caution averaging, signed variant, 201 levels, step against hull, F0 zero-margin point) | Configuration Card, focus 2 | PARTLY_MEETS | see W1, W9, W10 | Construction sound and sensitivities reported; grid resolution and alternate magnitudes need main-text treatment | none identified | no: the null survives every variant |
| Confirmatory against added analyses | Configuration Card, focus 3 | PARTLY_MEETS | see S3, W3, W6 | Plans hashed and deviations logged; abstract and contributions draw mainly on added descriptive analyses without a label | S10 amendment text not in the package | yes: contributions 2 and 4 |
| Reaction-and-stop scoring, plan extension, den₀ rule | Configuration Card, focus 4 | MEETS | see S5, S6, W10 | Extension, censoring sensitivity and evaluability rule are explicit and tested | caution axis inherited from the 3 s scoring | no |
| Off-policy status | Configuration Card, focus 5 | PARTLY_MEETS | see W2, W12 | Off-policy status stated; recording-policy dependence of magnitudes not reported in the main text | design cannot separate policy from scenario draws | yes: generality of abstract magnitudes |
| Bounded null with a pre-fixed bound | Configuration Card, special interest | PARTLY_MEETS | see W4, W7 | Bounded descriptively; bound not fixed in advance | substance robust under any reasonable margin | no |
| Statistical reporting (intervals, effect sizes, multiplicity) | Review protocol, Step 4a | MEETS | see S1, W5 | Intervals and effect sizes (shares, decision-equivalents) everywhere; secondary contrasts declared unadjusted | many uncorrected cells, labelled as such | no |
| Reproducibility | Review protocol, Step 6 | PARTLY_MEETS | see S7, W11 | Exhaustive description and independent re-implementation; deposit not yet created | none identified | yes: needed before acceptance |

### Recomputation log (outside the four bounded procedures)

The four bounded receipt procedures cover only p, GRIM, GRIMMER and df checks. The ratio and identity checks below are therefore logged here as internal-consistency checks ("inconsistent table numbers", reporting-only under the receipt standard's §8.5); the GRIM-eligible proportions are in the receipts. No discrepancy was found.

- Room: 1,116.91/201 = 5.5568 points = 460.66 decision-equivalents (Fig. 3(b) 461; Table S23 460.7).
- RR(N): 0.00122 × 5.5568 = 0.00678 points (Table S1 0.0068) = 0.56 decisions ("0.6 of 8,290").
- CK3: 0.831 × 460.66 = 382.8 ("about 383"); 383/461 = 0.831. AM: 0.376 × 460.66 = 173.2 ("about 173"). NA: 0.0167 × 460.66 = 7.69 decisions ("about 7.7") and 0.0928 points ("0.09").
- Commitment ratios (Table III): 0.68/5.5568 = 0.122; 1.34 → 0.241; 4.07 → 0.732. The values 2.14 → 0.385 against 0.384 and 2.98 → 0.536 against 0.537 are consistent within the rounding of R. The window-only column reproduces Table S2 (135.02/1,116.91 = 0.121; 261.13 → 0.234; 407.10 → 0.364; 547.65 → 0.490; 719.58 → 0.644).
- den₀ conversions: 0.71 × 82.9 = 58.9 (58.8), 0.045 → 3.7, 1.14 → 94.5 (94.7). Table S20d's decision-equivalents divided by 82.9 reproduce Table III's den₀ column (0.112, 0.709, 1.409, 2.267, 3.198, 4.372). Interval endpoints do not convert exactly (for example 20.9/82.9 = 0.252 against 0.26), as expected when each resample is scaled by its own n. The 3 s den₀ of 497.08 decision-equivalents is 5.996 points, and 0.71/5.996 = 0.118 (Table S19).
- Phase rooms: (0.43·678 + 15.59·755 + 0.82·6,857)/8,290 = 2.133 ("2.13"); 5.5568/2.133 = 2.60 ("2.6 times").
- Table S23 identity: 4.96 + 0.95 − 0.35 = 5.56 points and 411.3 + 78.4 − 29.0 = 460.7 decision-equivalents; 411.3/460.7 = 0.893; 0.633 × 78.4 = 49.6 (49.7); 50/78.4 = 0.64 (0.63 from unrounded values).
- 2 m gap: 0.0087 × 612.0 = 5.3; 0.0076 × 157.1 = 1.2; 0.0535 × 107.7 = 5.8 decisions (Section V-D).
- Basic intervals (Table S16) reproduce from 2θ − percentile ends: RR(N) [0.00125, 0.00352]; R [4.52, 6.62]; NA [0.0082, 0.0261]; AM [0.327, 0.436]; CK3 [0.759, 0.909]; Q [−0.0048, 0.0030]; RR₀(CK3) [0.707, 0.847]. The coverage ranges quoted in Section IV-B (92–93%; 96–97%; 99.6%) match Table S16.
- Counts: 30 × 271 = 8,130, leaving 160 decisions for the five short runs (Section S10.8: 160). Table S3 is reachable only with 0, 2 and 3 short runs at 5, 10 and 15 m/s and 4, 1 and 0 at α = 1.642, 5.412 and 7.550 (each short run 18–53 decisions), so four of the five contact-terminated runs come from the least conservative recording setting. 17 × 8,290 = 140,930 pairs. Table S18: unsafe as scored plus unsafe when judged to the stop equals the estimate in all nine settings. Table S22 adds 300, 600, 1,500 and 3,000 decisions at T = 1, 2, 5 and 10 s (30 runs × 10 per second) and 5,989 at 20 s, consistent with after-stop segments as short as 18.9 s. Table S27: 80 + 84 + 152,100 = 152,264; Section S10.7: 864 + 135 + 84 + 44 = 1,127 and 35 + 9 + 948 = 992.
- Cross-table repeats: every checked cell of Table II against Tables S5, S12 and S21, of Table III against Tables S19 and S20d, and of Table IV against Tables S20a and S24b agrees at the printed precision.
- Section S3: 0 contacts in 130 episodes gives an exact one-sided 95% upper limit of 1 − 0.05^(1/130) = 0.0228 ("2.3%").
- Inputs to W1 and W4: grid step 10^(5/200) = 1.0593; variance ratio 1.1029² = 1.2164, an offset of 3.40 grid steps; one decision-equivalent is 0.0022 of the room; 0.5% of the room is 2.30 decisions; 0.0047 of the room is 2.17 decisions. Input to W2: tuning-run room 237.24/201 = 1.18 points; 5.50/237.24 = 0.023.

### Questions for the authors

1. Was the 0.5% bound written into the S10 amendment before the Section S10.1 values were read? Please give that amendment's hash and date.
2. What is RR(N) against a placebo source F0 × 1.1029², and on a grid-free frontier computed from the critical scales?
3. How large is the per-phase gain when the scale ratios are chosen on held-out runs?
4. What explains the 4.7-fold difference in room between the tuning and evaluation runs: phase mix, contact-terminated runs, or the recording planner?
5. Under the reaction-and-stop scoring, how do the shares change if caution is averaged over selections that are safe under that scoring?
6. Since a planner runs at one caution level, could RR be reported at a few fixed caution operating points beside the level-averaged value?

## Arithmetic Receipts

### AR1
procedure_id: grim
evidence_anchor: table: Supplement Table S12, footnote (share of stored decisions given the oracle's value, P25)
reported_inputs: P25 share 0.2440 printed to four decimals; n = 9,307 stored decisions; one 0/1 indicator per stored decision
assumptions: the share is the unweighted mean of a 0/1 indicator over all 9,307 stored decisions, as the footnote states; rounding rule unstated, so the verdict must hold under half-up, half-even and truncation
derivation: 0.24395 × 9,307 = 2,270.44 and 0.24405 × 9,307 = 2,271.37, so k = 2,271 is the only candidate; 2,271/9,307 = 0.244010, which prints as 0.2440 under all three rules
derived_value_or_range: k = 2,271; 2,271/9,307 = 0.244010
comparison_rule: consistent if some integer k gives k/9,307 inside the rounding interval of the printed value under every candidate rounding rule
rounding_interval: 0.24395 ≤ x < 0.24405
nearest_achievable: 2,270/9,307 = 0.243902; 2,271/9,307 = 0.244010; 2,272/9,307 = 0.244117
status: consistent

### AR2
procedure_id: grim
evidence_anchor: table: Supplement Table S12, footnote (share of stored decisions given the oracle's value, P50)
reported_inputs: P50 share 0.4977 printed to four decimals; n = 9,307 stored decisions; one 0/1 indicator per stored decision
assumptions: unweighted mean of a 0/1 indicator over all 9,307 stored decisions, as the footnote states; rounding rule unstated, so the verdict must hold under half-up, half-even and truncation
derivation: 0.49765 × 9,307 = 4,631.63 and 0.49775 × 9,307 = 4,632.56, so k = 4,632 is the only candidate; 4,632/9,307 = 0.497690, which prints as 0.4977 under all three rules
derived_value_or_range: k = 4,632; 4,632/9,307 = 0.497690
comparison_rule: consistent if some integer k gives k/9,307 inside the rounding interval of the printed value under every candidate rounding rule
rounding_interval: 0.49765 ≤ x < 0.49775
nearest_achievable: 4,631/9,307 = 0.497582; 4,632/9,307 = 0.497690; 4,633/9,307 = 0.497797
status: consistent

### AR3
procedure_id: grim
evidence_anchor: table: Supplement Table S12, footnote (share of stored decisions given the oracle's value, P75)
reported_inputs: P75 share 0.7456 printed to four decimals; n = 9,307 stored decisions; one 0/1 indicator per stored decision
assumptions: unweighted mean of a 0/1 indicator over all 9,307 stored decisions, as the footnote states; rounding rule unstated, so the verdict must hold under half-up, half-even and truncation
derivation: 0.74555 × 9,307 = 6,938.83 and 0.74565 × 9,307 = 6,939.76, so k = 6,939 is the only candidate; 6,939/9,307 = 0.745568, which prints as 0.7456 under all three rules
derived_value_or_range: k = 6,939; 6,939/9,307 = 0.745568
comparison_rule: consistent if some integer k gives k/9,307 inside the rounding interval of the printed value under every candidate rounding rule
rounding_interval: 0.74555 ≤ x < 0.74565
nearest_achievable: 6,938/9,307 = 0.745460; 6,939/9,307 = 0.745568; 6,940/9,307 = 0.745675
status: consistent

### AR4
procedure_id: grim
evidence_anchor: text: §III-A "82.7% come after the lead has stopped"
reported_inputs: 82.7% of 8,290 evaluated decisions printed to one decimal of a percent; Table S5 lead-stopped count 6,857 and share 0.827
assumptions: the percentage is the unweighted share of evaluated decisions in the lead-stopped phase, as Table S5 defines it; rounding rule unstated
derivation: 0.8265 × 8,290 = 6,851.7 and 0.8275 × 8,290 = 6,860.0, so k = 6,852 to 6,859 round to 82.7%; the tabulated 6,857 gives 6,857/8,290 = 0.827141, inside the interval and away from both boundaries
derived_value_or_range: 6,857/8,290 = 0.827141; reachable k = 6,852 to 6,859
comparison_rule: consistent if the tabulated count, divided by 8,290, lies inside the rounding interval of 82.7% under every candidate rounding rule
rounding_interval: 0.8265 ≤ x < 0.8275
nearest_achievable: 6,856/8,290 = 0.827021; 6,857/8,290 = 0.827141; 6,858/8,290 = 0.827262
status: consistent

### AR5
procedure_id: grim
evidence_anchor: text: §III-A "77.5% have the ego at or below 0.5 m/s"
reported_inputs: 77.5% of 8,290 evaluated decisions; Table II ego-moving count 1,863, where moving means above 0.5 m/s (Section IV-B)
assumptions: at or below 0.5 m/s is the complement of the ego-moving population, as Section IV-B defines it; rounding rule unstated
derivation: 8,290 − 1,863 = 6,427; 0.7745 × 8,290 = 6,420.6 and 0.7755 × 8,290 = 6,428.9, so k = 6,421 to 6,428 round to 77.5%; 6,427/8,290 = 0.775271 lies inside the interval
derived_value_or_range: 6,427/8,290 = 0.775271; reachable k = 6,421 to 6,428
comparison_rule: consistent if the complement count, divided by 8,290, lies inside the rounding interval of 77.5% under every candidate rounding rule
rounding_interval: 0.7745 ≤ x < 0.7755
nearest_achievable: 6,426/8,290 = 0.775151; 6,427/8,290 = 0.775271; 6,428/8,290 = 0.775392
status: consistent

### AR6
procedure_id: grim
evidence_anchor: table: Table V, lead-braking row (rows within 5% of the median)
reported_inputs: 99.26% of 152,264 decision rows; Supplement S10.7 gives 1,127 lead-braking rows more than 5% from the median; Table S27 rows 80 + 84 + 152,100
assumptions: the percentage is the unweighted share of the 152,264 rows, and the 1,127 rows are its complement, as Section S10.7 states; rounding rule unstated
derivation: 80 + 84 + 152,100 = 152,264 and 152,264 − 1,127 = 151,137; 0.99255 × 152,264 = 151,129.6 and 0.99265 × 152,264 = 151,144.9, so k = 151,130 to 151,144 round to 99.26%; 151,137/152,264 = 0.992598 lies inside
derived_value_or_range: 151,137/152,264 = 0.992598; reachable k = 151,130 to 151,144
comparison_rule: consistent if the complement count, divided by 152,264, lies inside the rounding interval of 99.26% under every candidate rounding rule
rounding_interval: 0.99255 ≤ x < 0.99265
nearest_achievable: 151,136/152,264 = 0.992592; 151,137/152,264 = 0.992598; 151,138/152,264 = 0.992605
status: consistent
