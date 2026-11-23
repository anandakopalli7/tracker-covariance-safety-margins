# Peer Review Report: Reviewer 2 (Domain)

- Seat: Peer Reviewer 2 (Domain), internal id R2. Multi-object tracking and Kalman-filter estimation for road vehicles; covariance consistency (NIS/NEES); multiple-model and adaptive filtering; use of tracker uncertainty in prediction and planning.
- Model: Fable 5.2 (claude-fable-5-2).
- Date: 21 November 2026.
- Material read: MANUSCRIPT_v13.md (whole), SUPPLEMENT_v13.md (whole), Figs. 1-4. Nothing else. No lookups; every reference comment below is from memory and offline.
- Calibration status: NOT_CALIBRATED.

## 1. Recommendation

**Major Revision.** Confidence: 4 of 5.

The confirmatory equivalence for the fixed-noise filter is sound but is close to a mathematical identity (a Kalman covariance with fixed noise does not depend on the data, and the baseline is the mean of that same covariance), so the paper's empirical weight rests on the arms whose covariance could vary. Of those, the IMM as tuned is a degenerate test (its manoeuvre model has an acceleration noise of 0.001, its braking-phase NIS is above 9, and only its position-velocity block reaches a constant-velocity prediction), while the one variant whose margin does vary recovers a clearly positive share and is left out of the title and abstract. The core results survive, but the title, the abstract and the tuning paragraph say more about "IMM covariances", "NIS near 2", "the tracker's amplitude", "2 Hz" and "real driving logs" than the evidence carries; most of this is wording, and one fairly tuned multiple-model arm would settle the rest.

## 2. Strengths

- **S1. The mechanism is stated honestly and early.** The Introduction says that with fixed noise "a null is expected", and Section II says the mechanism "is not new" and follows from the Riccati recursion. The paper does not sell the null as a discovery (Section I, paragraph 4; Section II, last paragraph).
- **S2. The margin-ratio check is a useful, truth-free diagnostic.** Table S28 (Supplement S11) shows the ratio near constant in lead braking, stopped vehicle and cut-in (98.7 to 99.9% of rows within 5%) and varying in crossing families (4 to 9%). The text also says where the check is silent (heading rotation of object-frame noise), which is the correct reading.
- **S3. Consistency is reported by phase, not only pooled.** Table S7 gives NIS and velocity NEES before braking, during braking and stopped for all five filters. This is exactly the table a tracking reader needs, and it is reported even though it weakens the "NIS near 2" label (Supplement S4).
- **S4. Tuning facts that cut against the paper are disclosed.** Supplement S4 states that no tuning run lies inside the NIS window, that the CA window "could not be reached", and gives the tuned constants and the IMM transition sensitivities (Table S6).
- **S5. Update rate and latency are separated in the supplement.** Table S16 crosses three rates with up to three latencies and reports the lag for each, which allows the reader to see that state age, not rate alone, drives the after-stop room (Supplement S6.2; Fig. 4a).
- **S6. Scope limits are explicit.** Section VI ("Limits") and the abstract both say that removing covariance margins is not justified, and name young and coasting tracks and crossing traffic as cases where a covariance varies.
- **S7. The adaptive-noise variant is reported with its own oracle and a post hoc check labelled as such** (Table III; Supplement S4, last paragraph).

## 3. Weaknesses

### W1. The IMM as tuned is not a fair test of "a covariance that varies"

- Severity: **MAJOR**
- Location: Section III-D; Section V-B; Table III; Supplement S4 (CA and IMM bullets), Tables S6 and S7.
- Evidence: "The NIS window could not be reached on the search grid" (Supplement S4, CA bullet); the same bullet gives the acceleration term as 0.001.
- What is wrong: The IMM mixes the re-tuned CV filter (process noise scaled down by κ = 0.168) with a CA filter whose acceleration noise is 0.001 (units not given; if (m/s²)², a standard deviation of about 0.03 m/s²) against leads that brake at 2 to 5.7 m/s² (Table S14 terciles). Neither model is a manoeuvre model in the sense of the literature the paper cites in Section II ("let a covariance react at a manoeuvre's onset"). The paper's own numbers show the IMM does not switch in any useful way: braking-phase NIS 9.24 against 9.58 for the re-tuned CV (Table S7), the same 99.7% within 5% as the re-tuned CV and the CA filter (Table III), a lag of 2.32 m against 2.48 m, and no change at all across transition diagonals 0.90, 0.95 and 0.98 (Table S6: 99.7% and CK3 0.764 in every row). An IMM whose output is insensitive to its transition matrix is one whose two models are nearly the same filter. The cause is the tuning rule: one scalar chosen so that a per-run time-averaged NIS has median near 2, on runs where 78% of decisions are in the stopped phase (16,781 of 21,574 on the fresh runs; NIS 0.46 there). That rule drives process noise down and cannot produce a filter that is consistent during braking. Mode probabilities are reported nowhere, so the reader cannot see whether the CA model ever takes weight. The result "the IMM's covariance barely varies" is therefore a property of this tuning, not of IMM trackers, yet the Introduction presents the IMM among "covariances that vary" and Section V-B groups it with "the steady-state covariances".
- Fix: (a) Add one multiple-model arm designed the usual way: a quiet model plus a manoeuvre model whose process noise covers the scenario's decelerations (for example a CV/CV pair with low and high velocity noise, or a CA model with acceleration noise of the order of the drawn braking rates), tuned on the tuning runs for braking-phase NIS; report its mode-probability trace around braking onset, its NIS/NEES by phase, its within-5% share, and r and c. This arm would be descriptive, which is acceptable if labelled. (b) Whether or not (a) is done, report the mode probabilities of the present IMM by phase and state in the main text that its manoeuvre model has near-zero acceleration noise. (c) Reword every general statement to "the IMM as tuned here by a time-averaged NIS rule".
- Needs: **NEW VALUE/analysis** for (a) and (b); WORDING ONLY for (c).

### W2. The planner interface discards what a CA or IMM filter adds

- Severity: **MAJOR**
- Location: Supplement S4 (first paragraph); Section III-E; Supplement S1.1.
- Evidence: "the planner receives each variant's 4 × 4 position–velocity covariance" (Supplement S4).
- What is wrong: Every variant is reduced to its position-velocity block and projected with z = (n, t_e n), and actors are "predicted at constant velocity" for every tracker (Section III-E; the lag in Table III is defined as a constant-velocity error). So the CA and IMM filters' acceleration estimate and acceleration variance never reach the margin, and no process noise is accumulated over the 3 s look-ahead. In tracking practice a predicted covariance is F P Fᵀ + Q(t), and for a CA or IMM filter the acceleration terms grow as t⁴/4; this is the part of a multiple-model covariance that changes most at a manoeuvre onset. The paper's own AM source, which has the form t⁴(σ_a² + â²)/4, recovers 0.369 of the room (Table S8), which shows that this missing term is where a covariance-shaped margin can carry information. The tested object is therefore "the filtered position-velocity covariance, propagated without process noise under a CV prediction", not "an IMM tracker's covariance". Related: the room is 23.62 pp in the braking phase and 0.08 pp in the stopped phase (Table III), so most of it comes from the constant-velocity prediction of a decelerating lead (a model error of order ½at²), not from state-estimation error. The paper has no arm that separates the two.
- Fix: (a) State the interface limit in Section III-D and in the Limits. (b) Add one descriptive arm in which the IMM (or CA) variant supplies its own predicted covariance over the look-ahead, including the acceleration block and process noise, with its own class average. (c) Add a "true current state, CV prediction" reference so that the room is split into a tracker-attributable part (estimation lag) and a prediction-model part; the first is the most any tracker output could address.
- Needs: WORDING ONLY for (a); **NEW VALUE/analysis** for (b) and (c).

### W3. "NIS near 2" and "the mechanism persists" are not supported by the consistency table

- Severity: **MAJOR**
- Location: Section V-D, "Filter tuning"; Table III row label "CV filter, re-tuned (NIS near 2)"; Section III-D; Supplement S4 and Table S7.
- Evidence: "The mechanism persists with NIS near 2 and with a CA filter." (Section V-D).
- What is wrong: The re-tuned CV filter has a pooled median NIS of 1.99, but "no run lies inside the window" (Supplement S4): ten tuning runs lie between 0.48 and 1.77 and ten between 2.22 and 10.99. By phase its NIS is 1.86 / 9.58 / 0.46 and its velocity NEES 2.69 / 9.49 / 0.04 (Table S7). In the braking phase, where the room is, the re-tuned filter is over-confident by a factor of about five and is less consistent than the online filter it replaces (online: NIS 1.87, NEES 2.37 in braking). The CA filter's pooled NIS is 1.63, which the supplement itself says is "not near 2". The re-tuning also made the filter slower where it matters: lag 2.48 m against 1.42 m, braking-phase room 29.52 pp against 23.62 pp, after-stop room 238.1 against 173.4 decision-equivalents. So the paragraph shows that the result persists under a filter that is less consistent and more lagged in braking, which is not the claim a reader takes from "NIS near 2". No filter in the study is consistent in all three phases, so the paper cannot say what a consistent filter's covariance would do. In addition, Table S7 is computed on the 35 old evaluation runs, is exploratory and single-program (every cell carries ‡); there is no consistency table on the fresh runs that carry the confirmatory claims. NEES is given for velocity only, although the margin at 3 s is a projected position-plus-velocity quantity.
- Fix: Rename the variant (for example "CV, process noise re-tuned to a pooled NIS median of 2") in Table III, Section III-D and Section V-D; put the by-phase NIS in the main text next to the label; replace the last sentence of the paragraph with what was shown (the null and the room persist under a lower-noise CV filter and a low-noise CA filter, both over-confident in braking). Recompute Table S7 on the fresh runs with a second program, and add the normalised projected error (realised 3 s error squared over s) by phase, which is the consistency of the quantity the planner actually uses.
- Needs: WORDING ONLY for the renaming; **NEW VALUE** for the fresh-run table.

### W4. "Detection at the tracker's amplitude" is shown at ±5%, not at the tracker's amplitude

- Severity: **MAJOR**
- Location: Abstract; Section IV-C; Section V-A; Table II (E5 row) against Table III (online CV row, column c).
- Evidence: "moved within a symmetric band of ±5%" (Section IV-C).
- What is wrong: E5 varies the margin by a fixed ±5%. The online tracker's actual variation is far smaller: 99.9% of its binding rows lie within 5% of the median, and the oracle built at its own amplitude (Table III, online CV, c) recovers 0.0001 [0.0000, 0.0002], about a hundred times less than E5's 0.013, with a lower end printed as 0.0000. The abstract and Section V-A say that the score "detects rank information at the tracker's amplitude" and at "the tracker covariance's own amplitude (confirmed)". What was confirmed is detection at a ±5% band, which is an upper envelope of the tracker's variation. At the tracker's own amplitude the paper's own number shows there is essentially nothing to detect, which supports the mechanism (the covariance cannot matter) but is a different statement from the one printed. The same looseness affects the name "amplitude-matched" for E5 as opposed to E5ₓ.
- Fix: In the abstract, Section I (contribution 1), Section V-A and the conclusion, say "at a ±5% amplitude, an upper envelope of the tracker's variation", and add one sentence that at the tracker's own amplitude the ranking oracle recovers 0.0001 of the room. Keep the hypothesis outcome as it is, with its true description.
- Needs: **WORDING ONLY** (the values are already in Table III).

### W5. The only covariance that varies gives a positive result, and the title and abstract omit it

- Severity: **MAJOR**
- Location: Abstract; title; Section V-B, second paragraph; Table III (adaptive row); Section VI, "What a varying covariance needs".
- Evidence: "recovers a small share of its room on these runs" (Section V-B).
- What is wrong: The adaptive-process-noise filter is the single variant whose margin varies (21.5% within 5%). Its share is 0.0459 [0.0390, 0.0533]: the interval is well above zero, so by the paper's own rule in Section IV-C it "recovers room", and it straddles the equivalence margin of 0.05, so it would not pass the equivalence test applied to the online filter. Its share is 96% of its own amplitude-matched oracle (0.0459 against 0.0477), meaning its variation is almost as informative as a truth-ranked variation of the same size; the post hoc oracle on its full ratio distribution reaches 0.073 (Supplement S4). The domain reading is that this filter is amplitude-limited by its design (three-update window, clip at 10), not uninformative. The abstract reports two nulls and no word of this; the title names "Fixed-Noise and Interacting-Multiple-Model" only. A reader of the title and abstract concludes that covariances that vary were tested and found empty, when the one that varied was not.
- Fix: Add one sentence to the abstract and the conclusion (for example: "a filter whose process noise adapts to its innovations does vary its margin and recovers 0.046 [0.039, 0.053] of its room (descriptive)"). In Section VI, state that its share is close to its own ranking oracle and that the limit is amplitude. Optionally add a sensitivity with a wider clip or a covariance-inflating (fading-factor) form, which the paper already cites [24].
- Needs: **WORDING ONLY** (optional sensitivity would be a NEW VALUE).

### W6. The title is broader than the tests

- Severity: **MAJOR**
- Location: Title; Section V-A.
- Evidence: "so nothing is tested on the logs" (Section V-A), against the title's "and on Real Driving Logs".
- What is wrong: The title advertises a test "on Real Driving Logs", but the real-log sequence stopped at its first hypothesis (room −0.01 [−0.13, 0.13] pp) and no covariance was tested there; the same holds for cut-in. The title also names "Interacting-Multiple-Model Tracker Covariances" as a class, while one IMM with one tuning was tested (W1), and it does not name the regime (a single lead braking to a stop on a straight road, at 2 Hz). The abstract is on the narrower side for the logs and cut-in, but it says "An interacting-multiple-model tracker's covariance barely varies", which reads as a statement about IMM trackers.
- Fix: Name the regime and drop the untested bed from the title, for example: "Does a Fixed-Noise Kalman Tracker's Covariance Improve a Speed Planner's Decisions Behind a Braking Lead? An Equal-Caution Test in Simulation, Open and Closed Loop". In the abstract use "the tested IMM, tuned by a pooled NIS rule".
- Needs: **WORDING ONLY**.

### W7. The update-rate reading confounds rate with latency, and the abstract overstates the dependence on 2 Hz

- Severity: MINOR
- Location: Abstract ("Magnitudes depend on 2 Hz updates"); Section V-D, "Update rate and latency"; Table V; Table S16; Fig. 4a.
- Evidence: "The after-stop room is largely a consequence of the 2 Hz update." (Section V-D).
- What is wrong: The main text compares 2 Hz without latency against 5 and 10 Hz with 0.1 s latency. Table S16 shows that latency matters as much as rate: at 5 Hz with 0.2 s latency the after-stop room is 171.2, the same as at 2 Hz without latency (173.4), and at 10 Hz with 0.2 s it is still 130.5. The quantity that drives it is the age of the state the planner uses (update interval plus latency plus the planner's use of states "up to 0.4 s old"), not the rate itself. Second, the headline room barely depends on rate: 5.58, 4.99 and 4.75 pp at 2, 5 and 10 Hz without latency, a fall of 15%; the after-stop room is 173.4 of about 1,204 decision-equivalents, 14% of the total. The braking prediction's share moves from 0.783 to 0.807. So "Magnitudes depend on 2 Hz updates" is true of the after-stop component only. This is a favourable finding for the paper (the room and the null are robust to rate) and is under-reported.
- Fix: Reword to "the after-stop room falls with the age of the planner's state (update interval and latency); the total room changes by 15% or less from 2 to 10 Hz". Give the equal-latency columns in Table V. In the abstract replace "Magnitudes depend on 2 Hz updates" with a statement limited to the after-stop part and the pooled shares.
- Needs: WORDING ONLY.

### W8. The higher-rate re-runs violate the filter's white-noise assumption and report no consistency

- Severity: MINOR
- Location: Supplement S6.2.
- Evidence: "each on the last ten sweeps" (Supplement S6.2).
- What is wrong: At 10 Hz each detection shares nine of its ten accumulated sweeps with the previous one (at 5 Hz, six of ten), so successive detection errors are strongly correlated, while the measurement noise is left "unchanged" and only the process noise is scaled by dt/0.5. A Kalman filter fed correlated measurements with a white-noise R becomes over-confident, and its steady-state covariance shrinks with rate for the wrong reason. No NIS or NEES is given at 5 or 10 Hz, so the reader cannot tell what filter was run there. This does not threaten the null (a fixed-noise covariance is still constant), but it limits what the lag and room columns of Table S16 say about a real 10 Hz tracker. Ten-sweep accumulation also smears a decelerating lead over 0.5 s, which is a latency of the detector itself that "no latency simulated" leaves out.
- Fix: Report lead-track NIS by phase at each rate; state the sweep overlap and the accumulation smear as limits; if cheap, add a 10 Hz row with two or three accumulated sweeps.
- Needs: NEW VALUE (NIS by rate) plus WORDING.

### W9. The mechanism paragraph attributes all near-constant covariances to the Riccati steady state

- Severity: MINOR
- Location: Section VI, first paragraph; Section V-B.
- Evidence: "Unlike the steady-state covariances, the adaptive filter's margin varies" (Section V-B).
- What is wrong: The Riccati argument applies to the three single-model filters: with fixed Q and R and a regular update schedule the covariance is independent of the measurements and converges in a few steps. It does not apply to the IMM, whose combined covariance depends on the data through the mode probabilities and the spread of the means; the IMM's near-constancy here is a tuning outcome (W1). Calling it a steady-state covariance blurs the one distinction a tracking reader will look for. The more exact statement for the fixed-noise case is also slightly different from "settles to a steady state": the covariance depends only on the update and miss pattern, which is why births, coasting and missed detections are the only sources of variation (as Supplement S11 notes for tracks younger than 0.5 s or after two misses). A closed form for the CV steady state exists (the α-β filter and its tracking index) and would let the paper predict the 1.103 median ratio instead of only measuring it.
- Fix: Separate the two cases in Section VI. State the data-independence property explicitly and cite a page or section of [25] for it. Consider one line deriving the steady-state margin for the object-frame noise used.
- Needs: WORDING ONLY.

### W10. Tuned constants lack units, and the IMM's internal state is not reported

- Severity: MINOR
- Location: Supplement S4.
- Evidence: "initial mode probabilities (0.9, 0.1)" (Supplement S4).
- What is wrong: κ = 0.168 is dimensionless, but the CA acceleration term 0.001 has no unit and no statement of whether it is a continuous-time spectral density or a per-step variance at the 0.5 s step. The search grid on which the NIS window "could not be reached" is not given, so the reader cannot tell whether 0.001 is the grid's edge. The re-tuned measurement-noise values are not printed. Mode probabilities, the model-conditioned NIS, and the size of the spread-of-means term are not reported for the IMM. κ, the acceleration term and the tuning NIS values are single-program (‡).
- Fix: Print units, the search grid, the re-tuned R, and a by-phase table of mean CA-mode probability and the share of the combined covariance due to the spread of means.
- Needs: NEW VALUE (small, descriptive).

### W11. The baseline is the tracker's own mean covariance, which makes the confirmatory equivalence close to an identity

- Severity: MINOR
- Location: Table I (F0 row); Section VI, first paragraph.
- Evidence: "the mean of the tracker's reported covariances on the tuning runs" (Table I).
- What is wrong: F0 is not an independently derived class constant (for example from detection-error statistics); it is the average of the object under test. With a data-independent covariance and a sweep that removes global scale, N and F0 can differ only through the few rows off steady state and through the mix of families in the average (which gives the 1.103 median). The paper says a null is expected, so this is not hidden, but the contribution list calls the result "a confirmatory test" without saying that, for the fixed-noise filter, the test confirms a known property of the filter rather than an empirical regularity of driving. The informative arms are then the varying ones, which are descriptive (adaptive) or degenerate (IMM).
- Fix: Say this in one sentence in Section VI or in contribution 2, and consider a sensitivity with a class constant built from error statistics rather than from the tracker.
- Needs: WORDING ONLY (sensitivity optional).

### W12. Literature coverage: the nearest intelligent-vehicle work was searched but is not cited, and the novelty statement rests on abstracts

- Severity: MINOR
- Location: Section II, "Threat assessment..." and "Novelty, with its limits"; Supplement S13 and Table S29; References.
- Evidence: "the literature on interacting-multiple-model and adaptive filtering was not searched for a planner-side test" (Supplement S13).
- What is wrong: The threat-assessment paragraph cites one work [29] for decisions computed from uncertain state estimates. The query list (Table S29, items 15 to 17, 26, 38, 42) names several works that, as I recall them, propagate a filter's state covariance into time-to-collision or braking decisions (Stellet et al.; Berthelot et al.; Stöckle et al.; Nilsson et al.), and none appears in the reference list or is distinguished from the present test. For the journal's readers this is the closest neighbourhood. The main text's novelty sentence says "In the sources we searched" but does not say that the search read abstracts only and did not cover the IMM and adaptive-filtering literature; those limits are in the supplement only. On the tracking side: the adaptive-filtering citation [23] is an INS/GPS application rather than the original innovation-based work; the steady-state claim cites a whole textbook; no source is given for vehicle motion models (the supplement says a seventh suggested reference on that topic could not be found and was dropped); and work on how tracking errors and uncertainty affect downstream forecasting beyond [14] is absent although queried (item 30). I cannot ground a journal norm for how many of these must be cited, so this stays MINOR [FIELD-NORM UNVERIFIED].
- Fix: Add two or three sentences positioning the covariance-to-TTC line of work and say how the present test differs (comparison with a constant at equal caution). Move the two search limits into the main-text novelty sentence. Candidate references, all from memory and **to verify** before use:
  - R. K. Mehra, "On the identification of variances and adaptive Kalman filtering," IEEE Trans. Autom. Control, 1970 (original innovation-based noise estimation). To verify.
  - P. R. Kalata, "The tracking index: A generalized parameter for α-β and α-β-γ target trackers," IEEE Trans. Aerosp. Electron. Syst., 1984 (closed-form steady state). To verify.
  - X. R. Li and V. P. Jilkov, "Survey of maneuvering target tracking. Part I: Dynamic models," IEEE Trans. Aerosp. Electron. Syst., 2003. To verify.
  - R. Schubert, E. Richter and G. Wanielik, "Comparison and evaluation of advanced motion models for vehicle tracking," Int. Conf. Information Fusion, 2008 (possibly the dropped seventh reference). To verify.
  - J. E. Stellet et al., "Uncertainty propagation in criticality measures for driver assistance," IEEE Intelligent Vehicles Symposium, 2015 (title as given in Table S29). To verify.
  - A. Berthelot et al., work on handling uncertainties in criticality assessment / probabilistic time-to-collision, IEEE Intelligent Vehicles Symposium, about 2011-2012 (search lead only). To verify.
  - X. Weng et al., work on robustness of trajectory prediction to tracking errors (search lead only; cf. Table S29 item 30). To verify.
- Needs: WORDING ONLY (plus reference checks by the author).

### W13. A point estimate printed outside its own interval

- Severity: MINOR
- Location: Supplement Table S13, "Share of N", column "All".
- Evidence: "0.00122 [−0.00108, 0.00119]" (Table S13).
- What is wrong: The point value lies above the interval's upper end. The row is exploratory and labelled as carried from an earlier version, but it is the old-run counterpart of the headline share and Table V prints a different old-run value (−0.0004; a different estimand, per the table note). Also a typographic slip in the same table: "Room $R$ (pp" lacks its closing bracket.
- Fix: Check the value against its record, or state why a percentile interval excludes its point estimate; fix the bracket.
- Needs: NEW VALUE check (or WORDING if the record confirms it).

### W14. The "lag" column measures the residual after the stop, not the lag in braking

- Severity: MINOR
- Location: Table III caption and "Lag (m)" column; Table S16.
- Evidence: "in the first second after its stop (m)" (Table III caption).
- What is wrong: The lag is a constant-velocity position error 3 s ahead in the first second after the true stop, i.e. three times the residual speed estimate. The room, by the tracker's own phase, is in braking (23.62 pp) and almost absent once the track reads stopped (0.08 pp). The column therefore characterises the tail of the event and not the phase where a faster filter or a manoeuvre model would act. It does show, usefully, that the CA filter as tuned lags more than the online CV filter (1.88 m against 1.42 m), which is further evidence for W1.
- Fix: Add the velocity-estimate error (or the CV prediction error) at fixed times after braking onset, per tracker.
- Needs: NEW VALUE (small, descriptive).

## 4. Reference-list notes

All checks are offline, from memory; nothing was looked up. "Cannot check offline" means I can neither confirm nor dispute the entry.

- [2] The cited work concerns micro aerial vehicles; the sentence it supports ("obstacle trackers' covariances enter planners directly") does not say so. Suggest adding "(for aerial robots)" or a road-vehicle example.
- [5] arXiv:2606.03590v2 with "accepted to IROS 2026": cannot check offline. The tracker of record rests on this preprint; give the proceedings entry once it exists.
- [10] The author's own manuscript under review; reviewers cannot see it. IEEE style is "submitted for publication". The paper says none of its data or results is used here, which is sufficient provided the editor is told of the overlap in detector, tracker configuration and margin form.
- [13] Pages and DOI cannot be checked offline. The text's description ("grid the value of a forecaster's uncertainty") is plausible from the title.
- [15] Title: "The impact of class uncertainty propagation in perception-based motion planning". The text describes it as showing that "a constant-velocity baseline with a fixed covariance" stays competitive and calls it the nearest published analogue of the null. I cannot reconcile that description with a title about class (classification) uncertainty; the author should confirm from the full text that the CV fixed-covariance baseline is in that paper. arXiv identifier and "et al." author list cannot be checked offline. Section VI also cites [15] for "uncertainty in planning in general".
- [23] Mohamed and Schwarz is an INS/GPS application of innovation-based adaptive estimation; details match my memory. It is a secondary source for the method (see W12).
- [26] Li and Zhao, "Evaluation of estimation algorithms part I: Incomprehensive measures of performance". The text cites it for "consistency statistics judge a filter, not its use downstream". As I recall, that paper treats error measures (RMSE and alternatives), not NIS/NEES consistency or credibility; the credibility papers of the same group would fit the sentence better. To verify by the author.
- [27] No DOI, although Table S29 item 48 holds a candidate DOI for it. Add after checking.
- [28] Preprint only; a later conference version by the same first author exists as I recall, under a somewhat different title. To verify whether the preprint is the right version to cite for "covariances set from training data".
- [34] Preprint only (acceptable; it is the usual citation).
- [36], [37] As I recall, ISO 22179:2009 was withdrawn when ISO 15622:2018 absorbed full-speed-range ACC. To verify; if so, cite [37] as withdrawn or drop it. The supplement says the standards' full texts were not read; the claim "limit automatic deceleration to comfort levels" then rests on scope statements only and should be worded accordingly.
- [38] No year, revision date or series of amendments given.
- [39], [40] Format is detailed and internally consistent; the "in force from 4 Jan. 2023" date cannot be checked offline.
- [25] A whole textbook is cited for the steady-state claim in three places; give a chapter or section.
- [7], [8], [21], [22], [24], [29], [31], [32], [33], [41], [42]: authors, venue, volume, pages and year agree with my memory. [1], [6], [9], [11], [12], [14], [16], [17], [19], [20]: plausible and consistent with my memory of titles and venues; page ranges and DOIs cannot be checked offline.
- [3] A repository file at a commit is cited for "driving stacks carry covariance fields"; acceptable as a software citation, add an access date.
- Four of 42 entries are preprints only ([5], [15], [28], [34]) and one is unpublished ([10]); two of these ([5], [15]) carry substantive weight in the argument.

## 5. Questions for the author

1. What are the units and the discretisation of the CA acceleration term 0.001, what was the search grid, and was 0.001 its edge? What NIS did the largest grid value give, by phase?
2. For the IMM of record, what is the mean CA-mode probability before braking, during braking and after the stop, and what fraction of the combined covariance comes from the spread of the means in the braking phase?
3. Did any variant's acceleration estimate or acceleration covariance enter the prediction or the margin, or were all five trackers predicted at constant velocity with the 4 × 4 block only? If the latter, why is this the right interface for a CA or IMM filter?
4. Why was the tuning target a per-run mean NIS pooled over phases, given that 78% of decisions are in the stopped phase? Was a braking-phase target considered before the freeze?
5. The re-tuned filter's tuning runs split into two groups (NIS 0.48 to 1.77 and 2.22 to 10.99). What separates them (desired speed, braking rate, range)?
6. Table III gives the online filter's own-amplitude oracle as 0.0001 [0.0000, 0.0002]. Do you agree that the detection hypothesis was passed at ±5% and not at the tracker's own amplitude, and that the abstract should say so?
7. The adaptive filter's share is 96% of its ranking oracle. Was a wider clip, a longer window, or a fading-factor form [24] tried on the tuning runs? If not, would you state that the adaptive design was not optimised for decision value?
8. How much of the 5.58 pp room remains if the planner is given the true current state with the same constant-velocity prediction? This separates what any tracker could address from what only a prediction model can.
9. At 5 and 10 Hz, what is the lead-track NIS by phase, given the overlapping ten-sweep inputs and unchanged measurement noise?
10. The median margin ratio is 1.103 in three families. Is this explained by the class average being taken over all six families (crossing families have ratios below 1), and can the steady-state value be derived from the configured noise?
11. For [15]: where in that paper is the constant-velocity, fixed-covariance baseline, and does its "class uncertainty" refer to classification or to a class-level covariance?
12. Table S7 is on the old runs and single-program. Can the same table be produced on the fresh runs by both programs?
