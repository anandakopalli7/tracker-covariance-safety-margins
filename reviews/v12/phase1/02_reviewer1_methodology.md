# Peer Review Report

## Manuscript Information
- **Title**: Decision-Level Evaluation of Tracker-Covariance Safety Margins at Equal Caution: A Fixed-Noise Kalman Tracker in CARLA Lead Braking (draft v12, unpublished)
- **Manuscript ID**: not assigned (simulated submission to IEEE Open Journal of Intelligent Transportation Systems, regular paper)
- **Review Date**: 2026-11-19
- **Review Round**: Round 1 (reviewed as a fresh submission; Phase 1, seat 1 of 5)
- **Files read**: PACKAGE_MANIFEST_v12.txt; MANUSCRIPT_v12.md (all lines); SUPPLEMENT_v12.md (all lines); figures fig1, fig2, fig3_pooled_room, fig3_rr, fig4, figS2 (PNG). Not read as images: fig5_closedloop and figS1 (their content is described in the Supplement text and captions). The deposit (code, arrays, amendments) is not in the package; I make no claim about it.

---

## Reviewer Information

### Reviewer Role
Peer Reviewer 1 (Methodology)

### Reviewer Identity
Applied statistician and simulation-evaluation methodologist: resampling inference for non-smooth statistics, operating-curve and frontier comparisons, positive controls, separation of planned from exploratory analyses; experience with log-replay evaluations of automated-driving components. Blind spots: filter and tracking theory, automotive practice (covered by other seats).

### Review Focus
(1) Whether the scoring construct (wrong go, caution, step frontier, room R, share RR, perfect oracles O, partial-oracle grading) can carry the claims, including the populations where it "does not grade". (2) Whether the inference for the tracker covariance's share (run bootstrap on 35 runs, double bootstrap, grid placebo, gridless frontier, subsampling, the "2.2 decisions" bound) is stated for the quantity actually estimated. (3) Design and status of the analyses (tuning/evaluation split, earlier exploratory use of the evaluation runs, plans and amendments, "second programs", held-out per-phase scales). (4) Whether numbers in Abstract, §I and §VII are reproduced by the tables, with consistent interval choices.

---

## Overall Assessment

### Recommendation
- [ ] Accept
- [ ] Minor Revision
- [x] **Major Revision** — the evaluation design is careful and unusually candid, but the core "null is informative" claim and the most quotable exploratory results are not yet supported at the level the abstract and conclusion state them.
- [ ] Reject

### Confidence Score
4 (core expertise in resampling inference and evaluation design; limited on tracker theory and the deposit, which I could not open).

Confidence is an uncertainty/scope disclosure only; it never changes consensus counts, severity, decision bearing, or arbitration.

### Summary Assessment

The paper asks whether a fixed-noise EKF tracker's covariance, used as a planner margin, beats a class-average margin at equal caution, using an oracle margin as positive control on 35 CARLA lead-braking runs (8,290 decisions). The answer is a null: the tracker's margin is a near-constant multiple (1.10) of the class average's in 99.26% of binding rows, and its frontier is indistinguishable from a grid-shifted placebo. The design is strong in several respects: an explicit oracle and perfect oracles, graded oracles that report where the measure fails, a double bootstrap that exposes 53% coverage for the headline share, a grid placebo and gridless frontier, and a long table of reporting deviations. I recomputed the principal conversions (shares to decision-equivalents, phase counts, ratios to the room) and found them consistent with the tables.

The main weaknesses are inferential rather than arithmetic. The grading evidence is obtained where the pooled room is mostly a cross-phase allocation effect and at an amplitude far above the covariance's 2-5% variation, so it does not show that the measure can detect what a covariance could add. The tracker-share inference rests on a grid-artefact statistic, an uncalibrated placebo contrast, and a post hoc "2.2 decisions" maximum over heterogeneous interval methods. The headline held-out per-phase figures (90%, 99.9%) use a favourable baseline, carry no interval, and are not held out with respect to the analysis structure. The evaluation runs have been reused over several analysis rounds. These are repairable with re-analysis and rewriting, hence Major Revision.

---

## Strengths

### S1: Positive control, perfect oracles and graded oracles, with failures of the measure reported
The paper does not stop at an oracle margin. It adds a perfect oracle per scoring, random-mixture partial oracles (25/50/75%) with 50 further draws, and log-normal noisy oracles, and it reports that in the lead-braking and ego-moving populations the mixtures score below the class average (e.g. −0.682 at 25%), so shares there are demoted to frontier distances in decisions. This is better practice than most log-replay evaluations.
**Evidence Anchor**: table: Table S12 and Table S12b — partial oracle 25% lead braking −0.682 [−0.933, −0.486]; 50 further draws 0.28/0.54/0.78 pooled

### S2: Interval validity is measured, not assumed
A double bootstrap (2,000 × 1,000) shows nominal 95% percentile intervals cover in 92-93% for R and three shares and in 53% for RR(N), and the paper states that the point estimate 0.00122 sits outside its own percentile interval. Reporting this, and marking the affected cells, is rare and correct.
**Evidence Anchor**: table: Table S16 — RR(N) point 0.0012, percentile [−0.0011, 0.0012], estimated coverage 0.528, calibrated level 0.996

### S3: Diagnosing the source of non-smoothness (grid placebo, grid jitter, gridless frontier)
Dividing the class average's critical scales by 1.1029² gives a zero-information source that recovers 0.0015; shifts by fractions of a grid step give 0.0000-0.0017; gridless, the tracker covariance's share is −0.0004. This separates a grid offset (3.40 steps) from information and is the right design for a frontier statistic on a log grid.
**Evidence Anchor**: table: Table S30 and Table S30c — RR(P) 0.0015; jitter shares 0.0000-0.0017; gridless RR(N) −0.0004 [−0.0008, 0.0001]

### S4: Ground-truth-free mechanism check with stated reach
The ratio of tracker to class-average margin on binding constraints (99.26% within 5% of 1.10 in lead braking; 60.45%, 8.51% and 4.09% in benign driving and the two crossing families) explains the null mechanically and is explicitly declared silent where it varies. The track-age split (ratio 1.68 after two missed updates) bounds the claim honestly.
**Evidence Anchor**: table: Table V and Table S27 — lead braking 152,264 rows, 99.26%; track age [0.5, 1) s median ratio 1.682

### S5: Disclosure of plan status and reporting changes
The plans are hash-locked, the earlier exploratory use of the evaluation runs is stated, every added analysis is labelled exploratory, and Table S4 lists each reporting change beside the wording it replaced. Section IV-D states that the second programs share the scoring library, arrays and draws and were not blind to results.
**Evidence Anchor**: text: §IV-D "All added analyses, including every per-phase, after-stop and cross-family result of Sections V-C to V-E and the time-gap margin, are exploratory and descriptive."

### S6: Sensitivity analyses that bear on the construct
Convex-hull frontier, signed caution (Table S21), plans judged until the stop ends (Tables S18-S19), a 2 m standstill gap, leave-one-run-out, stratification by recording setting, removal of the five contact-terminated runs, and a stated evaluability rule (den₀ at least 10 decision-equivalents) with its effect at thresholds 5 and 20 (S11.9). Shares in unevaluable populations are not interpreted.
**Evidence Anchor**: table: Table S17 and Table S21 — leave-one-run-out R 5.36-5.80; signed-caution pooled room 4.86 [4.05, 5.61]

---

## Weaknesses

### W1: The positive control shows grading where the room is cross-phase allocation, and at amplitudes far above the covariance's variation; it does not establish that the null is not a blunt measure
**Problem**: §I states that a positive control is needed "without which a null result cannot be told apart from a blunt measure", and §IV-B concludes from pooled and after-stop grading that the null "is not a blunt measure". But (a) §V-C and Table S23 show that 89% of the pooled room (411.3 of 460.7 decision-equivalents) is recoverable by one class-average scale per phase, so the pooled mixture oracles are largely scoring the cross-phase allocation a mixture inherits, not within-decision information about the error; (b) where within-phase information would act (lead braking, ego moving) the same mixtures score negative or near zero (75% oracle in lead braking: 0.046 [−0.187, 0.227]), so the measure is declared non-grading exactly there; (c) every graded oracle is large in amplitude (the oracle's critical values on 25-75% of decisions, or divided by exp(σZ) with σ of 0.5, 1 or 2), whereas the tracker's margin varies by about 2-5% around its mean ratio (σ_N/σ_F0 5th-95th percentile 1.020-1.054 at t = 0; Table S14). No control asks what a margin that varies by only a few percent but ranks the realised error perfectly would recover, which is the quantity that bounds what a fixed-noise covariance could add. The Spearman check (ρ_N 0.453 vs ρ_F0 0.458) shows the ranking comes from state age and direction, which the class average also has.
**Evidence Anchor**: text: §IV-B "the measure therefore grades partial information, and the null of Section V-A is not a blunt measure"
**Why it matters**: the paper's own criterion for an informative null is not demonstrated in the populations and at the effect size that matter. The mechanism (near-constant ratio) still makes the null expected, so the conclusion is probably right, but the positive-control claim is overstated.
**Suggestion**: (i) add a rank-matched, amplitude-limited oracle (the oracle's critical-scale order compressed into the observed N/F0 ratio range, e.g. ±5%) and report its share as the ceiling for a covariance of this variability; (ii) repeat the graded-oracle check on the per-phase-scale frontier of Table S23 (remaining room 0.95 pp, 78.4 decision-equivalents), where allocation has been removed; (iii) state the criterion for "grades" before looking (for example, share within a stated tolerance of the mixing fraction and monotone in it).
**Severity**: Major
**Confidence**: 4 — core expertise: positive controls and detectability in evaluation design

### W2: Inference for the tracker covariance's share is built on a statistic the authors show to be a grid artefact, and the uncertainty statements are not for one stated estimand
**Problem**: The primary RR(N) is a grid statistic whose bootstrap distribution is shifted (point at the 97.7th percentile; median 0.0001). The paper then gives (i) a nominal interval with 53% coverage (Tables II, S5); (ii) a calibrated interval [−0.0016, 0.0017] at nominal level 0.996, calibrated by treating the full-sample value as truth for a bootstrap the paper itself says may be inconsistent; (iii) a placebo contrast −0.0003 [−0.0009, 0.0001] that is a nominal percentile interval on the same grid with no coverage estimate, although the placebo's own interval (0.0015 [−0.0007, 0.0015]) shows the same pathology; (iv) a gridless share −0.0004 with an interval from the first 2,000 resamples only, uncalibrated, whose basic and subsampling intervals lie below zero (the opposite side from the grid subsampling intervals, which lie above zero); (v) a "bound" of 2.2 decisions. The sign of the headline quantity changes between grid (0.6 decisions below the class average) and gridless (0.19 above). The paper concludes the grid is the cause, which implies the gridless frontier is the estimand and should be primary, with calibrated or smoothed inference and a pre-stated equivalence margin; instead the grid share remains the quantity in Tables II-IV and Figs. 2 and 4.
The 2.2 bound is the largest absolute end over fourteen intervals from methods of differing validity (including basic and subsampling intervals the paper calls unreliable for this statistic); it is formed after reading the values and equals 0.47% of the room (2.16/460.7), which is the content of the 0.5% statement the paper withdraws as post hoc (Table S31c, S11.2). It bounds interval ends, not the estimand with a stated coverage, and no equivalence margin was fixed.
**Evidence Anchor**: table: Table S31c — largest absolute end 2.16 decisions (Table S17, subsampling m = 25); Table S30 — grid RR(N) − RR(P) −0.0003 [−0.0009, 0.0001], gridless D(N) −0.19 [−0.34, 0.02]
**Why it matters**: the abstract and §VII rest the central null on this chain; at present a reader cannot tell which interval is the inferential statement about which quantity.
**Suggestion**: designate the gridless frontier (or a smoothed frontier) as the estimand before any interval; compute its double-bootstrap coverage with all resamples and report one calibrated interval; run the N-versus-placebo contrast through the same calibration; fix an equivalence margin from stakes (in decisions or share of the room) and report an equivalence-style conclusion against it; present the 2.2 maximum as a descriptive range of interval ends, not as a bound.
**Severity**: Major
**Confidence**: 4 — core expertise: resampling inference for non-smooth statistics

### W3: The held-out per-phase results in the abstract (90% and 99.9%) use a favourable baseline, carry no interval, and are not held out with respect to the analysis structure
**Problem**: The abstract and §I state that one class-average scale per phase recovers 90% of the room held out with true phases and 99.9% with the tracker's phase estimate. Table S32 shows these are leave-one-run-out "like for like" values, i.e. the gain over a single scale chosen out of sample, which lies 0.036 of the room above the single-scale frontier of record. Against that frontier the same quantities are 0.868 and 0.964. The five-fold value is 0.885 [0.81, 1.00], and no interval is given for 0.999 (or for any estimated-phase held-out value). The estimated-phase schedule (0.984 in sample) scores higher held out (0.999) than in sample, an artefact of the baseline, and "99.9%" implies a precision the data cannot give. At the lowest caution level no training choice qualifies for 30 of the 35 left-out runs, so the held-out curve omits that level. Only the scale triple is held out: the phase partition, the speed/acceleration thresholds (three tried: 0.980-0.999) and the idea of per-phase scales were chosen after the first results on these same runs. On the 20 tuning runs the per-phase in-sample gain is 0.632 against 0.893, and the pooled room is 0.63 times its phase-weighted sum there against 2.60 here (Table S35), so the "allocation" reading is not reproduced on the only other run set, which is not used to test the evaluation-chosen schedule.
**Evidence Anchor**: table: Table S32 — logged truth: in sample 0.893, LOO like-for-like 0.903, five-fold 0.885 [0.81, 1.00], against single scale of record 0.868; estimated phase −1.0: 0.984, 0.999, 0.964
**Why it matters**: this is the paper's main positive finding about "where the room is" and drives the claim that "most of the pooled room is an allocation of caution between phases".
**Suggestion**: report the held-out gain against the in-sample single-scale frontier (or both) in the abstract; give intervals for every held-out value including the estimated phase; fix the phase estimator and threshold in writing before testing; apply the evaluation-chosen schedule to the tuning runs (and the reverse) as a transfer test; drop the third significant figure.
**Severity**: Major
**Confidence**: 4 — core expertise: held-out evaluation and selection effects

### W4: No untouched confirmatory data remain; the evaluation runs have steered three rounds of analysis, and the null is labelled a "confirmation"
**Problem**: The room and the tracker covariance's difference from the class average were examined on these runs before the plan; the 35 runs are "a transfer to another planner setting, not a replication". Since then, each round of AI-panel review has added analyses on the same 35 runs (Amendments 05, 08, 09 and Addendum 01), and several claim wordings for the tracker share changed across versions (Table S4: from a basic-interval bound of "about 0.4%", to a calibrated interval, to the 2.2-decision bound; the 0.5% statement withdrawn). The hashes are self-attested rather than registered with a third party, and the package shows Amendment 09 at 00:16 EST, Addendum 01 at 01:08 EST and the package written at 01:13, so the order "defined before computed" cannot be checked from the paper. Contribution 3 is titled "A measured confirmation of the steady state", and the abstract says the 35 runs were "not used to design the margins" without saying that the tracker-versus-class-average difference had been viewed on them. The paper labels all added analyses exploratory, which is to its credit, but the abstract still states the exploratory per-phase and after-stop results with the same precision as the planned ones.
**Evidence Anchor**: text: §III-A "for them these runs are a transfer to another planner setting, not a replication"
**Why it matters**: the numbers cannot be read as confirmatory, and the specific figures a reader will quote (room location, per-phase shares, the bound) are the exploratory ones. Because the data are simulated, a fresh batch is cheap.
**Suggestion**: generate a new, untouched set of runs (new seeds, same generator) and run the final locked plan once, with the N-share estimand and equivalence margin of W2 and the phase schedule of W3 fixed in advance; deposit time-stamped, third-party-registered locks; replace "confirmation" by "consistency check"; in the abstract mark which results are exploratory.
**Severity**: Major
**Confidence**: 4 — core expertise: separation of planned and exploratory analyses

### W5: Scope and wording of the 2.2-decision statement differ across Abstract, §I, §V-A and §VII
**Problem**: The abstract says the frontier "stays within 2.2 decisions of the class average's at every interval end computed"; §I (contribution 3) and §VII say "under every interval method we used"; only §V-A and S11.2 say it was formed after the values were read. The figure is for the 3 s commitment, zero standstill gap and the pooled population. Under a 2 m gap the point estimate is 5.3 decisions on the wrong side (Table S24, RR₀(N) −0.0087 × 612.0), and per-phase and reaction-and-stop shares have only nominal intervals that the paper says are invalid. The §VII sentence does not carry the scoring qualifier.
**Evidence Anchor**: text: §VII "its frontier stays within 2.2 of 8,290 decisions of the class average's under every interval method we used"
**Why it matters**: the claim as worded in the conclusion reads as an inferential bound on the covariance's value; it is a descriptive maximum for one scoring.
**Suggestion**: use one wording everywhere, with the scoring, population and post hoc status stated, or replace it as in W2.
**Severity**: Minor
**Confidence**: 4 — arithmetic recomputed from Table S24 and Table S31c

### W6: Headline magnitudes depend on recording length and population mix
**Problem**: 82.7% of evaluated decisions follow the stop and 77.5% have the ego at or below 0.5 m/s. The paper states that the 83% is "a figure for recordings that continue for about 20 s after the stop" (§V-C), and R is 8.58 pp without the after-stop decisions and 15.59 pp while the lead brakes, against 5.56 pp pooled. The abstract gives 5.6 pp and 83% as properties of the oracle and braking prediction, with only the 83% decision fraction beside them. The tuning runs give R = 1.18 pp and CK3 share 0.377 (Table S35).
**Evidence Anchor**: text: §V-C "the 83% is a figure for recordings that continue for about 20 s after the stop"
**Why it matters**: pooled R and RR(CK3) are functions of an arbitrary run length; the abstract should say so or report them per phase.
**Suggestion**: give R and RR per phase in the abstract or state the dependence there.
**Severity**: Minor
**Confidence**: 4 — recomputed from Tables S22 and S35

### W7: "Only comparisons between sources are meant to transfer" is not supported by the paper's own two run sets
**Problem**: The Limits paragraph says that only source-to-source comparisons are meant to transfer across recording policies. Table S35 shows source shares moving by large factors between the tuning and evaluation runs: RR(CK3) 0.377 vs 0.831, RR(AM) 0.245 vs 0.376, RR(NA) 0.063 vs 0.017; only RR(N) (0.0022 vs 0.0012) is stable. Tuning-run intervals were not computed (Table S2 footnote).
**Evidence Anchor**: table: Table S35 — RR(CK3) all 0.377 vs 0.831; RR(NA) all 0.063 vs 0.017
**Why it matters**: it limits what the source ranking can claim and contradicts the transfer sentence.
**Suggestion**: compute tuning-run intervals; restrict the transfer sentence to the ordering and the near-zero N share, or drop it.
**Severity**: Minor
**Confidence**: 4 — direct table comparison

### W8: Mixed interval types, a point outside its interval, and uneven precision
**Problem**: The abstract and §V-A quote calibrated intervals (R [4.43, 6.68]; CK3 [0.74, 0.91]), Table II quotes nominal ones (R [4.50, 6.60]; CK3 [0.753, 0.903]); Tables III-IV and Fig. 4(b) give nominal intervals for RR₀(N) that the paper says are not valid, and Fig. 2(a) shows N's mean 0.0068 pp (Table S1 dagger: outside [−0.0061, 0.0065]) without a note. Table II reports RR(N) 0.0012 with upper limit 0.0012 (0.00122 against 0.00119). The held-out phase results appear as 0.90, 0.88 and 0.87 in different places without a label of which baseline. The NIS wording rule, defined on the nominal interval, is applied to the calibrated one (S10.1).
**Evidence Anchor**: table: Table II — RR(N) pooled 0.0012 [−0.0011, 0.0012]; R 5.56 [4.50, 6.60] against Abstract "calibrated 95% interval 4.4–6.7"
**Why it matters**: readers cannot tell which interval a number belongs to; for the N share the nominal interval is known to be invalid.
**Suggestion**: one interval type per quantity, labelled; in Tables III-IV and Fig. 4(b) either calibrate RR₀(N) or print the calibrated bound of W2.
**Severity**: Minor
**Confidence**: 4 — direct comparison of Abstract, V-A, Table II, Table S16

### W9: Verification is independent of code only; shared functions, arrays, draws and the author's model are common to all programs, and the intervals behind the N claim rest on one program
**Problem**: Every "second program" and recount was written by a Claude session from the same plans and shares the scoring library, stored arrays, resample draws and extraction modules; S10.9 says the agreement "covers the extension, the truth window, the flags and the counting, not those shared functions" (rectangle distance and stop profile). S11.8 states that the Monte Carlo levels of Table S31, the subsampling of Table S31b and "every interval of Section S11" rest on one program, which are the intervals that support the N bound and the gridless inference. Internal labels (A4 extraction, A9-3) and a Windows path to a file outside the package appear in S11.4 and S11.8.
**Evidence Anchor**: text: S10.9 "so this agreement covers the extension, the truth window, the flags and the counting, not those shared functions"
**Why it matters**: a common-mode error in the true-clearance geometry, the stored arrays or the draw design would pass every cross-check. Most likely it would not change the N null, but it would change absolute rooms and shares.
**Suggestion**: add a hand-checkable subset (a few decisions, true clearance by an independent routine); have the N-share intervals recomputed by a second program; define internal labels or remove them. In the deposit I would check that the lock hashes match the plan and amendment files, that clearance geometry is covered by a test independent of the scoring library, that the seeds in S8.1 and S10.1 reproduce the printed resamples, and that the gridless code handles ties and the [0, 10³] range as described.
**Severity**: Minor
**Confidence**: 3 — adjacent expertise: software verification; deposit not seen

### W10: Presentation of shares in populations that the paper itself says do not grade
**Problem**: Table II prints RR columns for "Ego moving" and "Lead braking" (for example CK3 0.472 and 0.606, TG 0.168, 0.088) beside a caption saying they are not to be read as shares there, and the Discussion and §VII quote partly from them. Shares of −9.000 and 18.232 appear in Tables S9-S10 for unevaluable cells. The caution definition averages over truly safe selections, so its denominator changes with the source. The caution window is fixed by the smaller of the class average's and the oracle's largest caution (about 27%) while the oracle's frontier is near zero beyond about 2.5% (Fig. 2a), so R is in effect the class average's mean wrong-go share over an arbitrary window; no sensitivity to the window is shown.
**Evidence Anchor**: text: §IV-B "to the smaller of the class average's and the oracle's largest caution"
**Why it matters**: the headline R and every RR depend on a window choice that is not varied.
**Suggestion**: print decision-equivalents, not shares, for non-grading populations in Table II; add R and RR under caution windows of, for example, up to 5%, 10% and 15%.
**Severity**: Minor
**Confidence**: 3 — reading of Fig. 2(a) and §IV-B definition

---

## Detailed Comments

### Title & Abstract
- The abstract is within the 250-word limit (248, per manifest). It states the null, the positive control and the main caveats, but gives exploratory per-phase figures (90%, 99.9%) at full precision with no interval (W3), omits that the tracker-versus-class-average difference was viewed on the evaluation runs earlier (W4), and words the 2.2 statement differently from §VII (W5).
- The title is accurate for the content; "at Equal Caution" is the construct.

### Introduction
- The statement of the evaluation requirement (decisions scored against the realised future, equal caution, positive control) is clear and is the right one. The positive control claim in §IV-B does not fully meet it (W1).
- Contribution 3 ("A measured confirmation of the steady state") should be reworded (W4).

### Methodology / Research Design
- *Scoring construct.* Wrong go, caution, step frontier, R and RR are defined clearly and the equal-caution frontier removes a global scale as intended. Points to tighten: the caution window and uniform weighting (W10); the criterion for "grades" is not stated as a rule; the oracle is an unbounded reference (shares above 1 occur, for example 1.108 upper limit for CK3 after stop).
- *Tuning/evaluation split.* The split is by run, which is right for serially dependent decisions, but the tuning runs were recorded under a different planner setting (α = 0.105, unit variance) from the evaluation runs (α = β of 1.642, 5.412 or 7.550), so the evaluation is a transfer by design (stated). Class-average P̄ comes from 120 tuning runs across six families; the 3 m/s² prediction deceleration was chosen on the tuning runs and on the evaluation runs pooled shares keep rising to 4-7 m/s² (Table S25), which is disclosed.
- *Intervals.* Run-level bootstrap with 20,000 resamples, everything recomputed per resample, seeds stated: good. With 35 clusters and about 21 braking decisions per run, per-phase intervals are wide and several are one-code only. Coverage of the double bootstrap is itself estimated with Monte Carlo SE about 0.005.
- *Analysis plan and status.* Handled in W4, W9.

### Results / Findings
- *Arithmetic checks performed* (all agree with the tables unless noted): R 5.56 pp × 8,290 = 460.7 decision-equivalents (Table S23); shares to decisions: 0.831 → 383.0, 0.376 → 173.1, 0.0167 → 7.7, 0.0012 → 0.56 (Table S33); placebo 0.0015 → 0.69; per-phase rooms 0.43 × 678 + 15.59 × 755 + 0.82 × 6,857 divided by 8,290 = 2.13 pp, and 5.56/2.13 = 2.61 (text 2.60); 4.96/5.56 = 0.892 (text 0.89); Table III ratios R/5.56 (0.018, 0.122, 0.241, 0.385, 0.536, 0.732; text 0.019, 0.122, 0.241, 0.384, 0.537, 0.732, rounding only); den₀ 0.71 pp → 58.9 (text 58.8); phase-weighted 0.045 pp → 3.7; 6,557 = 300 + 900 + 1,500 + 3,857; 132 = 53 + 43 + 36 and 52.2 = 6.7 + 18.6 + 26.9 (Table S33b); 1,127 off-band rows = 864 + 135 + 84 + 44, 152,264 × (1 − 0.9926) = 1,127; 2.16 = 0.0047 × 460.7; 30 × 271 + 160 = 8,290. No numerical mismatch affects a claim.
- *Items that are consistent but differently labelled* (W8): 0.90 (leave-one-run-out, like for like), 0.88 (five-fold) and 0.87 (against the frontier of record) for the same held-out quantity.
- *Selective emphasis*: V-A does not mention that the gridless basic interval for RR(N) [−0.0009, −0.0001] excludes zero in the unfavourable direction (Table S30); it is explained as grid-related in S11.2, but the main text should say so.

### Discussion
- The Discussion is careful about conditionality (open loop, off-policy, simulated sensing, steady state). The statement that the data "support a narrower statement than 'the decision value lies in anticipating braking'" is appropriate. The claim that "most of the pooled room is an allocation of caution between phases" is exploratory and see W3 and W7.

### Conclusion
- Over-reaches in two places: the 2.2-decision wording (W5) and the held-out 99.9% (W3). The conditional reading of the commitment results is well calibrated.

### References
- Not my remit; [9] is a related unpublished manuscript by the author and shares the configuration; the paper states no data are shared.

### Methodological fallacies checklist
- Overfitting / no holdout: partly (W3, W4). Garden of forking paths: partly (W4). Confirmation bias: reporting is open about failures, so low. Simpson-type composition: yes, the pooled room is a phase-mix effect, and the paper discloses it (W6). Survivorship: five contact-terminated runs handled by sensitivity.

---

## Questions for Authors

1. What share of the room would an oracle recover if its critical scales were rank-matched to the realised error but compressed into the range that the tracker's ratio actually spans (about ±5%)? This is the ceiling for the covariance as tested.
2. After allocation is removed (per-phase scales, remaining room 78.4 decision-equivalents), do random-mixture oracles grade in that setting, and what do they recover?
3. What equivalence margin, in decisions or share of the room, would you have called practically meaningful before seeing the data, and what does the gridless, calibrated interval say against it?
4. Was the −1.0 m/s² threshold of the tracker-based phase estimator fixed before the held-out values (0.999, 0.996, 0.980) were computed? What happens when the evaluation-chosen triple is applied to the 20 tuning runs?
5. How do R and the shares change if the caution window is cut at 5%, 10% and 15%, and if recordings are cut to 5 s after the stop?
6. Can a fresh batch of evaluation runs (new seeds) be generated and the final locked plan run once on it?
7. In the deposit: do the amendment hashes and file timestamps show that Amendment 09 and Addendum 01 precede the S11 and S38 values, and is the true-clearance geometry covered by a test that does not use the shared scoring library?

---

## Minor Issues

### Language / Grammar
- Dense, number-heavy sentences in §V-A and §V-C (several statistics per sentence); splitting them and moving some to tables would help readers.
- Terms used without an early definition in the text: "decision-equivalent" (defined only in the notation table), "grades"/"does not grade", "one code".
- Shares are printed to 3 decimals in some places and 4 in others (Table II caption states this); the abstract's "99.9%" implies more precision than the held-out data give (W3).

### Citation Format
- Not assessed in depth. Reference [42] and [41] are cited with annex and table pages in the main text; consistent with IEEE style.

### Figures and Tables
- Fig. 2(a): N's mean 0.0068 pp is outside its own percentile interval (Table S1 dagger); add the note that Fig. S4 has.
- Fig. 3(a): error bars are nominal; say so in the caption, and add intervals for the estimated-phase held-out values in Fig. 3(b)/Table S32.
- Fig. 4(b): RR₀(N) intervals are nominal and the paper says they are not valid for this statistic.
- Table S4 is very long; the main text should say that it is a reporting-change log and not a results table.
- Supplement S11.4 and S11.8 contain internal labels ("A4 extraction", "A9-3") and a local file path (`recount_v12\RECOUNT_COMPARE_A93_v02.md`) that are not in the package; remove or define.

### Layout
- **Submission gates (author-owned, no severity)**: (1) the author block, manuscript line 5; (2) the repository name and DOI in Data and Code Availability; (3) the "[AUTHOR CONFIRMATION: …]" at the end of the AI-generated-content statement. The AI-use disclosure and the revision history are otherwise complete and plainly worded.

---

## Criterion-Bound Judgements

Calibration status: `NOT_CALIBRATED`

Current seat reports cannot know the final actual panel topology and never self-upgrade from a candidate profile.

| Dimension | Criterion source | Judgement | Evidence anchor(s) | Rationale | Uncertainty / scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| Methodological Rigor: scoring construct (wrong go, caution, frontier, R, RR, oracles, grading) | criteria binding unavailable; general field norms | PARTLY_MEETS | text: §IV-B "the measure therefore grades partial information, and the null of Section V-A is not a blunt measure"; table: Table S12 lead braking 25% −0.682 | Clear definitions, perfect and graded oracles, and honest reporting of non-grading populations; but grading is shown at the wrong amplitude and where the room is cross-phase allocation, and the caution window is not varied | Judged without the deposit; the null itself is mechanically expected | yes: the positive control is the paper's stated condition for an informative null (W1, W10) |
| Methodological Rigor: inference for the tracker covariance's share | criteria binding unavailable; general field norms | PARTLY_MEETS | table: Table S16 RR(N) coverage 0.528; Table S31c largest end 2.16 | Strong diagnosis of the problem (double bootstrap, placebo, jitter, gridless) but no single estimand with a calibrated interval, uncalibrated placebo contrast, post hoc maximum | Intervals for gridless rest on 2,000 resamples and one program | yes (W2, W5) |
| Methodological Rigor: design and status of analyses (split, exploratory reuse, plans, second programs, held-out per-phase scales) | criteria binding unavailable; general field norms | PARTLY_MEETS | text: §III-A "not a replication"; table: Table S32 and Table S35 | Disclosure is plain and complete; but no untouched data, a favourable held-out baseline, structure not held out | I cannot verify hash timing without the deposit | yes (W3, W4, W9) |
| Evidence Sufficiency: numbers in Abstract, §I, §VII against tables; rounding and interval choice | criteria binding unavailable; general field norms | MEETS (numbers); PARTLY_MEETS (interval consistency) | table: Table S23, S33, S19; Table II against Table S16 | All cited figures I recomputed follow from the tables; interval type and baseline labels vary between places | Sample of key numbers, not every cell | yes, in part (W3, W8) |
| Originality | criteria binding unavailable; general field norms | NOT_ASSESSED | — | Outside the methodology seat | none identified | no |
| Argument Coherence | criteria binding unavailable; general field norms | NOT_ASSESSED | — | Outside this seat beyond the points above | none identified | no |
| Writing Quality | criteria binding unavailable; general field norms | NOT_ASSESSED | — | Outside this seat; comments listed under Minor Issues | none identified | no |
| Literature Integration | criteria binding unavailable; general field norms | NOT_ASSESSED | — | Reviewer 2's remit | none identified | no |
| Significance & Impact | criteria binding unavailable; general field norms | NOT_ASSESSED | — | Other seats | none identified | no |

Unresolved decision-bearing criteria, all repairable by re-analysis and rewriting: the detectability of the positive control (W1), the single calibrated estimand for the tracker share with an equivalence margin (W2), the held-out claims (W3), and untouched confirmatory data (W4). None invalidates the central mechanism-based null, so I recommend Major Revision, not Reject.
