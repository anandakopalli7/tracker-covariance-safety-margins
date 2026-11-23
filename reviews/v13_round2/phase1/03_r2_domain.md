# Round-2 panel, seat R2: Peer Reviewer 2 (Domain)

| Item | Value |
|---|---|
| Seat | R2, Peer Reviewer 2 (Domain); `contract_role: domain` |
| Model | Claude Opus 5.5 (`claude-opus-5-5`). Much of the paper's earlier text was written by this same model, so I read it with deliberate skepticism and checked claims against the supplement tables, not the prose |
| Skill | `academic-research-skills:academic-paper-reviewer` v1.11.1, mode `full`, this one seat only. I spawned no sub-agents, ran no other seat and wrote no synthesis |
| Card | "Card 3: Peer Reviewer 2 (Domain)" from `review_v13_output\00_phase0_field_analysis_and_cards.md`. I used its identity, "cares about" and blind spots word for word. I read only that card and the file's field analysis |
| Card-confirmation pause | **Not held.** This is a non-interactive run, so I could not ask the user (Checkpoint Rule 1 was not met by a user reply). I used the card as given and re-pointed its focus anchors as the brief directs |
| Criteria binding | `criteria_binding_unavailable`: I make no venue-alignment claim beyond general IEEE OJ-ITS norms |
| Calibration status | `NOT_CALIBRATED` |
| Written | 22 Nov 2026, clock read 06:24:55 EST (start) and 06:33:14 EST (end-hash read) |

**Files reviewed** (folder `revision_v13\work\A_text\out\freeze_v13_0623\`). SHA-256 at the start (06:24:55) and at the end (06:33:14) were identical:

| File | SHA-256 at start | SHA-256 at end |
|---|---|---|
| `MANUSCRIPT_v13.md` | `893442e4437e01fa6159dd9bbb8ebae21af65508a70064890b17929cf70db958` | same |
| `SUPPLEMENT_v13.md` | `f915fd798bbc9d3c53c56cea74d5b0ea4279463f3f3385b0e93488dba802f426` | same |
| `MANUSCRIPT_v13.pdf` | `4bd544e9ce3aff7eab8940c1f371ccd709da9910b963d3833e540f560b755da8` | same (not rendered: no PDF renderer) |
| `MANUSCRIPT_v13.tex` | `6e3d0acabd8decf2a61e186512822d3b6e89f3ecb1c086b6ffb33235fbfc6269` | same (used only to confirm one V-E sentence) |

The first three hashes match the brief.

**Coverage.**
- **Read in full:** the manuscript `.md`.
- **Supplement sections read:** S1.1, S1.3–S1.4, S3 (Tables S4–S5), S4 (Tables S6–S7), S5 (Tables S8–S12), S6 (Tables S14–S17), S10 (Table S27), S11 (Table S28), the opening of S13, S14 (Tables S31–S36) and S15 (Tables S37–S45).
- **Other files:** Fig. 2 (PNG) and the word counts in `BUILD_REPORT_v13.md`.
- **Not read:** S2, S7–S9 (seen only through search hits), S12 (search hits only), the response letter, `TEXT_FREEZE`, `RECOUNT_COVERAGE`, earlier reports and the other seats' files. The deposit is a placeholder, so I make no statement about it.

**Card 3 focus anchors, re-pointed to the round-2 sections:**
1. **Why a fixed-noise covariance is nearly constant, and the margin-ratio evidence:** Sections V-A, V-B and VI; Table III; Supplement S11 (Table S28).
2. **The tracker variants, including whether the two-noise IMM is a fair test of a manoeuvre-adaptive covariance:**
   - Main text: Sections III-D, V-B and V-E (its two-noise IMM paragraph); Table III.
   - Supplement: S4 (Tables S6, S7) and S15 (Tables S41, S42).
   - Departures: the rows of Table S5.
3. **Literature and positioning:** Section II; Supplement S13.
4. **Lag, update rate, latency and tuning, and whether the dropout and 10 Hz results are a property of these filters or broader:**
   - Section V-D and Table V.
   - Section V-E: dropouts, the replication and its dose-response, 10 Hz, the online-versus-permuted check, the caution-matched closed loop, and the nuScenes mechanism and decision tests.
   - Supplement: S6.2 (Table S16) and S14–S15 (Tables S32–S45).
   - Sections VI–VII.

**Identity (Card 3, unchanged).** Researcher in multi-object tracking and Kalman-filter-based estimation for road vehicles, familiar with covariance consistency (NIS/NEES), adaptive and multiple-model filtering and with how tracker uncertainty is passed to prediction and planning. Cares about whether the null is a property of these filters as tuned or something broader, and whether the wording stays on the narrower side. Blind spots: statistical inference; regulation and deployment.

**Overall recommendation:** Major Revision. **Score:** 6.5/10. **Confidence:** 4 of 5 (strong on Kalman, IMM and coasting behaviour; moderate on closed-loop simulator practice; statistical inference is outside my remit).

---

## Summary assessment

**What holds.** From a tracking point of view, the account of the null is right and now honestly framed. A CV extended Kalman filter with fixed class-level noise, updated at a regular 2 Hz on a straight road, settles to its Riccati steady state. Once the margin scale is swept, a near-constant multiple of the class average can change almost no decision. The paper now says the confirmatory equivalence was expected and that the test adds a bound. The margin-ratio check (Supplement S11) is a useful diagnostic that needs no ground truth. The update-rate analysis correctly traces the after-stop room to lag.

**What round 2 adds, and where it falls short.** Round 2 adds three things where the covariance does vary:
- a working manoeuvre-mode IMM;
- a replicated dropout effect with a dose-response;
- a real-log mechanism check.

Each is real but small, and each has a domain gap that keeps it from saying what its wording suggests:
- **The two-noise IMM** reaches the planner through the same interface as the first IMM: only the position–velocity block, a constant-velocity mean, and no process noise over the look-ahead. Its 2.2% measures that interface, not a manoeuvre-adaptive covariance. The paper's own acceleration margin shows the dropped channel is worth about a third of the room.
- **The dropout gain** comes from coasting (between-group allocation), not from ranking errors. The obvious coast-count baseline was not run.
- **The "caution-matched" closed loop** is matched in open loop only: the covariance arm lost 0.18 s more in the loop itself.
- **The mechanism account in Section VI** calls the update-schedule variation "other reasons" in crossing but "tracks the error" under injected dropouts.

All four can be fixed with offline re-scoring of stored arrays or with narrower wording, with one exception: a fair closed-loop comparison needs new F0 runs.

## Findings

Severity follows decision impact alone. Each finding has one typed evidence anchor. Conf. is my confidence (1–5); its basis is in the text. The body is at 5,747 of 5,750 words and the abstract at 250 of 250, so the text fixes below are written to be word-neutral or to go to the supplement.

| # | Location | Finding | Severity | Evidence | Fix (fewest words) | Conf. |
|---|---|---|---|---|---|---|
| W1 | §V-E ¶4; §VI ¶2; §VI Limits; §III-D; Suppl. S1.1, S15 | **The two-noise IMM is tested through an interface that discards how a manoeuvre mode expresses itself.**<br>(1) **The interface.** As for every variant, the planner receives only the 4×4 position–velocity covariance. It predicts the mean at constant velocity. The margin s = zᵀPz with z = (n, t_e n) adds no process noise over the 3 s look-ahead (S1.1).<br>(2) **What is lost.** A CA manoeuvre mode carries its information mainly in the acceleration estimate and variance propagated over the look-ahead, the (t²/2)² term. The paper's own acceleration margin AM, t⁴(σ_a²+â²)/4, which uses exactly that term, recovers 0.369 [0.331, 0.404] of the room (Table S8). The IMM covariance recovers 0.022.<br>(3) **What the paper says.** §III-D states this limit for "the IMM as tuned here" but V-E, VI and the Limits do not carry it to the two-noise IMM. VI then reads the 2.2% as "a manoeuvre mode does the same at braking onset" and sets it against the braking prediction ("The gains are small beside the braking prediction's"), which compares a channel, not the information.<br>(4) **Reading.** The 2.2% is a lower bound for this interface at 2 Hz. | MAJOR | `text: Section III-D "so acceleration terms never reach the margin"` | On the stored new runs, re-score the two-noise IMM with its full propagated covariance (mode-weighted CA prediction plus look-ahead Q). Put beside it its mode-mixed CA mean as a path-moving source. Else add to V-E and Limits: "same position–velocity interface; a lower bound". | 4: Kalman prediction step [25]; the paper's own AM definition and Table S8 |
| W2 | Abstract; §V-E ¶3; §VII; Suppl. Tables S34, S40 | **The dropout gain's source is coasting, and the coast-count baseline is missing.**<br>(1) **The decomposition.** The covariance margin used only inside dropouts recovers 0.0206 [0.0050, 0.0363] of the pooled room. Among dropout decisions alone, its share of their own room is 0.009 [−0.008, 0.024]. So the gain is an allocation between groups: dropout decisions get more margin. The covariance does not rank them.<br>(2) **What the covariance carries here.** Updates since the last detection, which is a track attribute every tracker exposes. The effect also needs the 3-update output rule, which is not the pipeline of record (Table S5).<br>(3) **The missing baseline.** A class average conditioned on coast count (F0 for 0, 1, 2 and 3 missed updates) is the natural baseline, and V-E itself says "A fixed margin increase during dropouts might give much of this gain; that was not tested."<br>(4) **Consequence.** Without that baseline the paper cannot say the covariance adds anything a coast flag does not. The abstract and conclusion ("where it tracks the error, it helps a little") invite the stronger reading. The same applies to the closed loop. | MAJOR | `table: Supplement Table S40 (substitution share inside a dropout 0.0206 [0.0050, 0.0363]; within-dropout share 0.009 [−0.008, 0.024])` | Add a coast-count class average to the dropout test and its replication; this is offline, on the stored arrays. Else write "mostly from coasting; a coast-count margin was not tested" in V-E and VII. | 4: the paper's own decomposition; standard track-status attributes |
| W3 | Abstract; §V-E ¶4; Suppl. S15 (Table S43); Table S5 last rows | **The "caution-matched" closed loop is matched in open loop only.**<br>(1) **The match.** The arms are matched by open-loop caution on other runs (18.22% against 18.39%). In the closed loop itself the covariance arm lost 0.18 [0.11, 0.26] s more, so it was more cautious where the outcome was measured.<br>(2) **0.18 s is not small here.** Without dropouts the braking prediction removed every contact for 0.16 s (Table IV).<br>(3) **No F0 curve.** F0's scale is the lowest of its calibration grid (4.0; contacts 17% on tuning cases, 32.6% on the 135 test cases). No F0 run at a larger scale exists on those cases.<br>(4) **Consequence.** The 12-point contact reduction cannot be separated from extra closed-loop caution. This is the paper's own objection to the earlier loop: "which cannot be told from a wider margin". | MAJOR | `table: Supplement Table S43, paired-difference row (contact −0.12 [−0.18, −0.05]; time lost 0.18 [0.11, 0.26] s)` | Run F0 at 2–3 scales above 4.0 on the same 135 cases and place N on F0's closed-loop contact-versus-time-lost curve. Else write "matched in open-loop caution" in the abstract and V-E. | 4: the paper's own equal-caution standard (§I ¶2) |
| W4 | §VI ¶2; §VII ¶1; §V-E ¶2; Suppl. Table S45 | **The mechanism account in VI is post hoc.**<br>(1) **What VI says.** In crossing the fixed-noise covariance follows "the update schedule and the geometry" and gives variation without rank information. Then: "Missed detections make it grow when the estimate is worse".<br>(2) **What the crossing data show.** The update-schedule group (misses since the last detection, and track age) explains 54% of the variation at the binding constraint and 89% at the decision level, with no recovery (share −0.067 [−0.221, 0.034]).<br>(3) **The problem.** The same physical source is "other reasons" in crossing and "tracks the error" under injected lead-braking dropouts. The sorting is done after seeing results; it is not yet a predictive mechanism.<br>(4) **Possible reconciliations.** Crossing variation may be driven by age (track births) rather than misses, or crossing misses may fall where no constraint binds. | MAJOR | `table: Supplement Table S45, row "Update schedule" (54%; 89% at the decision level)` | Split misses from track age in Table S45. Narrow VI to "injected misses during lead braking". | 3: interpretive; the reconciliation may exist in data I could not see |
| W5 | §V-E ¶4; Suppl. S15, Table S42; Table S5 | **The two-noise IMM's details are underspecified.**<br>(a) **Quiet mode.** It is "the constant-velocity filter of record, already tuned on whole tuning runs". That could be the online CANMOT filter or the re-tuned CV (κ = 0.168).<br>(b) **Transition sensitivity.** The diagonal is 0.95 per 0.5 s step (expected sojourn 5 s), with no sensitivity rows; the first IMM had 0.90 and 0.98.<br>(c) **Slow detection at 2 Hz.** The manoeuvre-mode probability averages only 0.48 in braking (46% of decisions above 0.5) and 0.18 before braking.<br>(d) **Untested cost.** There is no test behind non-braking leads and no closed-loop test, so the cost of false manoeuvre detections is unknown.<br>(e) **Wrong pointer.** V-E points to "Supplement S4", but the details are in S15. | MINOR | `table: Supplement Table S42, two-noise IMM new-runs row (0.18 / 0.48 / 0.08)` | Name the quiet filter. Add rows for diagonals 0.90 and 0.98. Score the stored non-braking-lead runs. Change the pointer to S15. | 4 |
| W6 | §V-B ¶1; Table III; Suppl. Table S42 | **V-B understates what the earlier IMMs show.**<br>(1) **The re-tuned IMM is not a manoeuvre detector.** Its manoeuvre-mode probability is highest when the lead is stopped (0.71) and lower during braking (0.39).<br>(2) **Its share is positive.** It is 0.0055 [0.0040, 0.0067], which is "recovers" under §IV-C. V-B gives only "still barely varies".<br>(3) **Why it matters.** Saying both plainly would show why the round-1 IMM arm was not a manoeuvre test. | MINOR | `table: Supplement Table S42, re-tuned IMM row (0.41 / 0.39 / 0.71)` | One clause in V-B. | 4 |
| W7 | §V-E ¶3 (10 Hz sentence); Suppl. S15 | **The 10 Hz dropout result cannot be read without the mask law in seconds.**<br>(1) **What is missing.** S15 reports the result without stating the mask law or the coast limit in seconds.<br>(2) **Why it matters.** If masks are 1–3 updates at 10 Hz, gaps last 0.1–0.3 s and tracks coast for 0.3 s at most, a different regime from 0.5–1.5 s at 2 Hz. Either way "the same class" cannot be read as breadth without this.<br>(3) **What else is 2 Hz only.** The two-noise IMM and both closed loops were run at 2 Hz only. | MINOR | `text: Supplement S15 "In a second configuration, with detection at 10 Hz and 0.1 s latency on the 150 new runs"` | State the masks and the coast limit in seconds. | 4 |
| W8 | §V-E ¶3; Suppl. Table S39 | **The dose-response plateau is probably a property of the mask law.** The share flattens above a start probability of 0.20 (0.0525, then 0.0514). That is where the mask law's caps bind: windows of 1–3 updates, never back-to-back, and coasting for at most 3 updates. These caps limit how far the covariance can grow. | MINOR | `table: Supplement Table S39, rows 0.20 and 0.30` | One clause attributing the plateau to the mask law's caps. | 3 |
| W9 | Abstract; §V-E ¶5; Suppl. Table S44 | **The real-log τ is understated in sign and computed on the wrong quantity.**<br>(a) **Sign.** "but not over all tracks" understates the result. All-pairs τ is −0.038 [−0.070, −0.006] and steady-track τ is −0.075 [−0.109, −0.043]: inverse ranking.<br>(b) **Quantity.** τ is computed on the raw spread within scene and keyframe, and class handling is not stated. With class-level noise, pairs across classes rank partly by class, which F0 already knows. The planner-relevant statistic is τ of N/F0, or τ within class.<br>(c) **Unlabelled level.** The abstract's [0.04, 0.17] is a 99% interval.<br>(d) **Omitted IMM result.** The IMM's real-log τ (0.210 around misses; 0.093 over all pairs) is better than CANMOT's and appears in no main-text sentence, although it bears on the IMM question. | MINOR | `table: Supplement Table S44, online-tracker row` | Write "inversely over all tracks". State the class handling. Add τ of N/F0. Give the IMM's τ in one clause. | 3 |
| W10 | §V-E ¶4 | **The class label contradicts the measured cost.** "safer at no extra cost by the plan's class" is attached to a measured 0.18 s cost. A reader takes "no extra cost" literally. | MINOR | `text: Section V-E "safer at no extra cost by the plan's class"` | Rename the class "safer, cost below 0.5 s". | 5 |
| W11 | Suppl. Table S43 | **The secondary closed-loop outcomes do not add up.**<br>(1) **Peak deceleration.** The paired difference is −2.99 [−4.32, −1.74] m/s², yet the arm medians are 6.25 and 6.11. Deceleration "from the ego speed" includes the collision impulse in contact runs.<br>(2) **Full braking.** The per-arm shares are 65.4% and 58.9%, against a paired difference of −0.01.<br>(3) **Masked share.** It differs between paired arms: 18.2% against 16.9%. | MINOR | `table: Supplement Table S43, columns Peak deceleration, Full braking and Masked` | Report deceleration over contact-free pairs. State that masks are identical per case and explain the masked-share gap. | 3 |
| W12 | §II; §VI Limits; reference list | **Domain literature is missing.**<br>(a) **Intermittent observations.** The dropout amendment is exactly the setting of Kalman filtering with intermittent observations, which predicts covariance growth with the drop rate.<br>(b) **Origin of innovation-based adaptation.** It goes back to Mehra (1970), not [23].<br>(c) **Motion models.** For the CV/CA choice, the motion-model survey (Li & Jilkov, Part I).<br>(d) **Detector uncertainty.** The most common source of a varying covariance in current stacks is per-detection (heteroscedastic) measurement noise from probabilistic detectors. It is neither tested nor named in the Limits, which matters for "It concerns this covariance". | MINOR | `absence: Section II and Section VI Limits — expected intermittent-observation Kalman filtering and detector-driven measurement-noise covariances; checked Section II, Section VI, references [1]–[42], Supplement S13` | Two citations in II and one clause in Limits. | 4 (literature need is my judgement; graded Minor) |
| W13 | Abstract; Table I | **Terms and scope words are loose.**<br>(a) **Undefined term.** "Two-noise IMM" is coined and not in Table I; the tracking literature would call it a CV/CA IMM with a manoeuvre-tuned mode.<br>(b) **Pronoun drift.** In the abstract "it" moves from the fixed-noise covariance to the dropout and IMM results ("In later-amendment tests where it tracks the error").<br>(c) **Configuration.** "Magnitudes hold in one simulated configuration at 2 Hz", but V-E reports a 10 Hz configuration. | MINOR | `text: Abstract "In later-amendment tests where it tracks the error, it helps a little"` | Define the term in Table I. Write "covariances" (plural). Write "mainly at 2 Hz". | 4 |
| W14 | §VI ¶2; Abstract | **The largest covariance gain is absent from VI.** The NIS-adaptive filter is the most direct innovation-driven, manoeuvre-reactive covariance tested. It has the largest share (0.046) and passed its twin test on new runs (difference 0.0508, (A)). VI's "What a varying covariance needs" leaves it out. | MINOR | `table: Table III, row "CV filter, adaptive process noise"` | One clause in VI. | 4 |
| W15 | §V-E ¶2 | **Ambiguous twin wording.** V-E says "no permuted-twin test was run here", but Table S33 lists the oracle-minus-twin test (A), 0.591. | MINOR | `table: Supplement Table S33, row "The oracle minus its permuted twin"` | Write "no twin test for N". | 5 |
| W16 | Table III | **Table III mislabels the two-noise IMM row.** The row "IMM, two-noise (amendment)" prints the secondary older-run value (0.0250), not the amendment's primary value (0.0220 on the new runs). | MINOR | `table: Table III, row "IMM, two-noise (amendment)"` | Label the row "(secondary, older fresh runs)". | 5 |

Totals: 0 CRITICAL, 4 MAJOR, 12 MINOR.

### Strengths (domain)

- **S1. The fixed-noise null is correctly explained.** The account is the Riccati steady state, plus object-frame noise rotated by heading, plus scale removal by the equal-caution sweep. It is backed by a ground-truth-free ratio check across six families. That check honestly says "where it varies, the check is silent and a decision-level test is needed". Anchor: `table: Supplement Table S28`.
- **S2. The two-noise IMM works as a filter, unlike its predecessors.**
  - The NIS window is reached on braking frames (1.997).
  - The mode probability rises at braking and falls when the lead stops.
  - Its permuted twin shows the ordering carries information (difference 0.0210).
  - It was scored on new runs under rules fixed before the data.
  - Anchor: `table: Supplement Table S41`.
- **S3. The dropout analysis is self-critical.** It includes a replication, a dose-response, a decomposition that exposes the gain's source, and an "output rule alone" control (share −0.0016). Anchor: `table: Supplement Table S40`.
- **S4. The real-log mechanism check is informative.** It is stratified (steady, in a miss, after a miss, young tracks), and the training-split choice of population is disclosed. Anchor: `table: Supplement Table S44`.
- **S5. The update-rate analysis is right on lag.** Process noise is scaled by dt/0.5, and an unscaled sensitivity is run. The after-stop room is traced to lag (173 → 78 decision-equivalents from 2 to 10 Hz). Anchor: `table: Supplement Table S16`.
- **S6. The scope wording mostly stays on the narrow side.** Example: "It concerns this covariance, not uncertainty in planning in general [15]". The paper does not claim that covariance margins should be removed. Anchor: `text: Section VI "It concerns this covariance, not uncertainty in planning in general"`.

### Criterion-bound judgements (domain remit)

| Dimension | Criterion source | Judgement | Evidence anchors | Decision bearing? |
|---|---|---|---|---|
| Account of the fixed-noise null | Card 3, anchor 1 | MEETS | Table S28; Section VI ¶1 | yes, for the confirmatory claim |
| Fairness of the manoeuvre-adaptive arm | Card 3, anchor 2 | PARTLY_MEETS | W1, W5; Table S41/S42 | yes, for VI and VII |
| Source and breadth of the dropout and 10 Hz results | Card 3, anchor 4; brief Q2 | PARTLY_MEETS | W2, W7, W8 | yes |
| Accuracy of the mechanism account | domain reviewer Step 3 | PARTLY_MEETS | W4 | yes |
| Literature coverage and positioning | Card 3, anchor 3 | PARTLY_MEETS | W12 | no |
| Terminology | domain reviewer Step 3c | PARTLY_MEETS | W13 | no |

---

## The two questions this seat was asked to weigh

### Is the two-noise IMM now a fair test of a manoeuvre-adaptive covariance?

**At the filter level, mostly yes. At the planner interface, no.**

What round 2 fixed:
- The manoeuvre mode is now tuned on braking frames and reaches its NIS window.
- Its probability tracks the lead's phase: 0.18, 0.48 and 0.08 before braking, during braking and when stopped. The re-tuned IMM gave 0.41, 0.39 and 0.71.
- The margin varies (89% of rows within 5% of the median, against 99.7%).
- The twin test shows the ordering matters.
- The test ran on 150 new runs under rules fixed before the data.

What still stops the 2.2% from answering the question:
1. **The interface (W1).** The planner sees only the position–velocity block, a constant-velocity mean and no look-ahead process noise. That removes the very terms by which a manoeuvre mode says "the next 3 s are uncertain". The paper's own acceleration margin shows those terms are worth about 0.37 of the room.
2. **Switching speed.** At 2 Hz, with an expected sojourn of 5 s and no sensitivity on the transition matrix, the mode is still below 0.5 in more than half of braking decisions (W5).
3. **Untested cost.** There is no closed-loop test and no test behind leads that do not brake hard, so the cost of false manoeuvre detections is unknown.

So the 2.2% is a lower bound for a manoeuvre-adaptive covariance under this interface. It should not be set against the braking prediction's 78% as "covariance versus prediction" evidence. The fair contrast is the IMM's own mode-mixed constant-acceleration prediction (moving the path) beside its full propagated covariance (widening the margin). Both can be computed on the stored new runs.

### Are the dropout and 10 Hz results a property of these filters as tuned, or something broader?

**The direction is broad. The size, and even whether the effect appears at all, depend on choices specific to this setup.**

Why the direction is broad:
- Any Kalman tracker that coasts a track grows its covariance with each prediction step (the intermittent-observation setting).
- A constant-velocity prediction from a stale velocity is wrong in proportion to the lead's deceleration.
- So a coasting-driven margin will help where misses fall during manoeuvres.

What ties the size to this setup:
- **The output rule.** The pipeline of record keeps an unmatched track for one update. Without the 3-update rule, no margin acts during a gap.
- **The mask law.** It is independent of the scene and capped at 3 updates, which explains the plateau (W8). Real misses depend on range and occlusion.
- **The scenario.** Lead braking only.
- **The baseline.** A single pooled class average under dropouts.

What is broader is not really the covariance; it is the coast state, which a coast-count margin would probably capture (W2).

On the 10 Hz result and the real logs:
- The 10 Hz dropout result cannot yet be read as breadth until its mask law and coast limit are given in seconds (W7).
- By contrast, the confirmatory null is broad within this simulator. The share stays inside the margin at 2, 5 and 10 Hz and at every latency (Table S16), as the Riccati argument predicts regardless of rate.
- On real data, the nuScenes check supports covariance growth around real misses, though only on the raw spread (W9). The logs had no decision room, so there is no real-log evidence on decisions.

---

## Answers to the five common questions

### 1. Is each result reported at its true size, with its label right?

**Mostly yes.**
- "Confirmed" is used only for the original sequences (Table II, Table S4).
- Section V-E marks the amendment tests "passed (amendment)".
- The dropout and twin replications are "replicated under rules fixed before the data".
- The first twin test is "specified post hoc".
- The 10 Hz and older-run IMM results are "secondary".
- Holm across the six round-2 primaries is stated beside the V-E results ("all six stay significant") and tabulated in Table S38.

**Exceptions:**
- "caution-matched" is true in open loop only (W3).
- "safer at no extra cost" sits beside a 0.18 s cost (W10).
- The sign of the real-log τ is understated and its 99% level is not labelled in the abstract (W9).
- Table III's two-noise row shows the secondary value under an "(amendment)" label (W16).
- The re-tuned IMM's positive share is not reported in the text (W6).
- The abstract gives shares as points (2.8%, 3.0%, 2.2%) without their wide intervals (for example [0.6%, 5.0%]). That is acceptable at 250/250 words, but V-E should keep the intervals, which it does.

### 2. Does any sentence claim more than its test allows?

- **Dropout gain's source.** V-E discloses it fairly ("not from ranking them among themselves"; the fixed-increase alternative was "not tested"). The abstract's and VII's "where it tracks the error" invite a reading the decomposition does not support, and the coast-count baseline is missing (W2).
- **Caution-matched closed loop.** "caution-matched" in the abstract outruns an open-loop match, given a 0.18 s closed-loop time-lost difference and F0 at the bottom of its grid (W3). V-E does disclose the grid-bottom scale and the open-loop match.
- **nuScenes mechanism check.** Choosing the primary population on the training split and scoring the validation split once is ordinary held-out practice, and it is disclosed in V-E, S15 and Table S5. The label is fair. The overreach is elsewhere:
  - "not over all tracks" hides an inverse ranking;
  - τ on the raw spread does not test information beyond the class average;
  - VI's "as the nuScenes check shows on real data" leans on a mechanism check with no decision test behind it (W9).
- **Real-log decision test.** It is reported correctly as "no room, nothing tested" in the abstract, V-E and VII. No overclaim.
- **Further VI sentences:**
  - "a manoeuvre mode does the same at braking onset" and "The gains are small beside the braking prediction's" overread an interface-limited test (W1).
  - "Missed detections make it grow when the estimate is worse" is contradicted in kind by the crossing decomposition (W4).

### 3. The previous round's main limits

| Previous limit | This version | What remains |
|---|---|---|
| The headline equivalence could hardly fail (near-constant covariance) | **Addressed in framing.** The text now says it was expected and that the test adds a bound (§V-A ¶2, §VI ¶1) | Nothing more is possible on that test. The paper's interest now rests on V-E |
| Thin evidence where the covariance varies | **Partly addressed.** The paper adds crossing, dropouts (with a replication and a dose-response), the adaptive filter's twin test, the two-noise IMM and the real-log mechanism check | All decision tests with room are simulated lead braking. The gains are 2–5% of the room. The coast-count baseline is missing (W2). The mechanism account is post hoc (W4). Real logs have no room |
| Same-day amendments without multiplicity control | **Partly addressed.** Holm across the six round-2 primaries | The first amendment's tests and the cross-sequence family are still unadjusted ("Sequences are not adjusted for one another"). This is outside my remit; I defer to R1 |
| One configuration at 2 Hz with no latency | **Partly addressed.** Update rate and latency are covered descriptively for the null (Table S16), and there is one secondary 10 Hz dropout run | Every confirmatory and amendment test, both closed loops and the two-noise IMM are at 2 Hz. The 10 Hz mask law is unstated (W7) |
| An unfair IMM arm | **Partly addressed.** The manoeuvre mode now works (S2) | The interface still discards acceleration and look-ahead terms (W1). There is no transition sensitivity, no closed loop and no test behind non-braking leads (W5) |
| A closed loop that was not caution-matched | **Partly addressed.** Matched in open-loop caution | The closed-loop time-lost difference is 0.18 s. F0 sits at the bottom of its grid and has no closed-loop curve. One level and lead braking only (W3) |

### 4. Readability

- **Bottom line first.** Yes: the abstract's first sentence states the claim. But the abstract is dense (250/250 words, more than a dozen numbers). "Room" is defined in an awkward parenthesis, and the pronoun "it" drifts (W13).
- **Coined terms.** Most are defined once, in Table I. "Two-noise IMM", "dropout-estimated class average" and the plan's class names ("safer at no extra cost") are not.
- **Finding the evidence.** V-E's claims trace cleanly to Tables S32–S45. One pointer is wrong: S4 instead of S15 for the two-noise IMM (W5).
- **Words.** With the body at 5,747 of 5,750 words, the fixes above are worded to be word-neutral or to go to the supplement.

### 5. Recommendation

- **Recommendation:** Major Revision.
- **Score:** 6.5/10, or about 3¼ of 5 stars (★★★☆☆).
- **Most likely editorial outcome at IEEE OJ-ITS:** major revision. Nothing is fatal and the reporting is unusually honest. A tracking-literate referee would ask for the coast-count baseline, the IMM interface fix and a closed-loop F0 curve before accepting the claims about where a covariance helps.
- **The single change that would raise my score most:** re-score the dropout open-loop test and its replication (stored arrays, no new runs) against a coast-count class average, that is, F0 conditioned on updates since the last detection. That decides whether the paper's main positive covariance result is about the covariance at all.
- **Runner-up:** re-score the two-noise IMM with its full propagated covariance (W1).

---

## Questions for the author

1. Which constant-velocity filter is the two-noise IMM's quiet mode: the online CANMOT filter or the re-tuned CV (κ = 0.168)?
2. Does each variant's class-average arm use that variant's own state means, so that the share isolates the covariance? The two-noise IMM's lag (0.40 m against 1.42 m) shows that its mean differs from the online tracker's.
3. In the caution-matched closed loop, is the mask sequence identical per case across the two arms? What explains 18.2% against 16.9% masked?
4. At 10 Hz, how long are the masked stretches and the coast limit, in seconds?
5. In the nuScenes τ, are pairs across object classes included? Are static objects included?
6. For the online CV filter, where does the acceleration margin's estimate â come from?

## Missing key references

- **Sinopoli, Schenato, Franceschetti, Poolla, Jordan and Sastry (2004), "Kalman filtering with intermittent observations."** This is the canonical analysis of covariance growth under random measurement loss, which is the dropout amendment's setting.
- **Mehra (1970), "On the identification of variances and adaptive Kalman filtering."** The origin of innovation-based noise adaptation, which the NIS-adaptive filter uses.
- **Li and Jilkov (2003), "Survey of maneuvering target tracking. Part I: Dynamic models."** The standard reference for the CV/CA model choice; the paper already cites Part V [21].
- **Feng, Harakeh, Waslander and Dietmayer (2022), "A review and comparative study on probabilistic object detection in autonomous driving."** Detector-driven measurement uncertainty is the main untested source of a varying covariance (W12).
- **Lefèvre, Vasquez and Laugier (2014), "A survey on motion prediction and risk assessment for intelligent vehicles."** It links prediction-mean and uncertainty choices to risk assessment, which positions VI's distinction between moving the path and widening the margin.

I have left the DOIs null because I cannot verify them in this session.

~~~yaml suggested-references
- title: "Kalman filtering with intermittent observations"
  authors: ["Sinopoli, B.", "Schenato, L.", "Franceschetti, M.", "Poolla, K.", "Jordan, M. I.", "Sastry, S. S."]
  year: "2004"
  doi: null
  arxiv_id: null
- title: "On the identification of variances and adaptive Kalman filtering"
  authors: ["Mehra, R. K."]
  year: "1970"
  doi: null
  arxiv_id: null
- title: "Survey of maneuvering target tracking. Part I: Dynamic models"
  authors: ["Li, X. R.", "Jilkov, V. P."]
  year: "2003"
  doi: null
  arxiv_id: null
- title: "A review and comparative study on probabilistic object detection in autonomous driving"
  authors: ["Feng, D.", "Harakeh, A.", "Waslander, S. L.", "Dietmayer, K."]
  year: "2022"
  doi: null
  arxiv_id: null
- title: "A survey on motion prediction and risk assessment for intelligent vehicles"
  authors: ["Lefèvre, S.", "Vasquez, D.", "Laugier, C."]
  year: "2014"
  doi: null
  arxiv_id: null
~~~

## Submission gates (author placeholders, not findings)

These are the author's to complete and are not counted as findings:
- the author block (affiliation, e-mail and ORCID);
- the repository name and DOI;
- the author's confirmation in the AI-use statement.

The title is the author's choice, and no sentence of the paper contradicts it.
