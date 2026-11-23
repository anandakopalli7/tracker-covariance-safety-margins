# Tables of the supplement of draft v12 (tables only)

> **TABLE S7.** The planner's 17 candidate rows, labelled by their pair of target accelerations (first, second; m/s²). The order in which the planner tries them is its cost order, which changes with the state.

| First target \ second target | −5 | −2 | 0 | 2 |
|---|---|---|---|---|
| −5 | full braking | row | row | row |
| −2 | row | row | row | row |
| 0 | row | row | row | row |
| 2 | row | row | row | row |
| State-dependent (−0.13 to 2.0) | — | — | row | — |

> **TABLE S28.** Configuration of the recordings. Evaluation runs: the 35 lead-braking runs not used to design the margins; tuning runs: the 20 lead-braking runs used to design them.

| Item | Value |
|---|---|
| Simulator | CARLA 0.9.15, synchronous mode, fixed step 0.05 s (16 physics substeps of 0.003125 s); a fresh server process per run |
| World | Generated from an OpenDRIVE description: one straight, flat road of 1,200 m with one 3.5 m driving lane per direction; weather and lighting not set |
| Vehicles | Ego and lead: the same car model (`vehicle.audi.etron`), 4.86 m long and 2.03 m wide, 2,370 kg |
| Lead motion | A requested speed $v_{\mathrm{req}}(t) = \max(0, v - b\,\max(0, t - t_b))$, tracked by a speed controller; independent of the ego except for the initial placement, a bumper gap of 3 m plus $v\tau_0$ |
| Draws, evaluation runs | Desired speed 5, 10, 15 m/s (15, 12, 8 runs); requested deceleration $b$ 2.13–5.97 m/s² (median 3.85), realised 2.09–5.46 (median 3.80); initial time gap $\tau_0$ 1.0–3.0 s; recording margin $\alpha = \beta$ = 1.642 (10 runs), 5.412 (12), 7.550 (13) |
| Draws, tuning runs | Desired speed 5, 10, 15 m/s (9, 7, 4 runs); requested deceleration 2.24–5.49 m/s² (median 3.84), realised 2.20–5.39 (median 3.75); initial time gap 1.0–2.7 s; fixed recording margin, $\alpha$ = 0.105 |
| Run length | 700 frames, 35 s: 5 s of warm-up without the selector and 30 s assessed. Five of the 35 evaluation runs and 10 of the 20 tuning runs ended at the first physical contact between the ego and the lead |
| Lidar | Ray-cast lidar on the ego, 1 m forward and 2 m up: 32 channels, 20 Hz, range 100 m, 680,000 points per second, vertical field of view −30.67° to +10.67°; simulator noise off; added Gaussian range noise along the ray, σ = 0.02 m, seeded per sweep |
| Detector | CenterPoint, voxel model, nuScenes configuration `nusc_centerpoint_voxelnet_0075voxel_fix_bn_z_flip` (voxels 0.075 × 0.075 × 0.2 m; range ±54 m); checkpoint `epoch_20.pth`, SHA-256 `59936925…e8ca32`; input: ten accumulated sweeps; four-flip inference; score threshold 0.1; run every tenth frame (2 Hz); no latency simulated |
| Tracker | CANMOT (commit `515d0792…`, with one recorded local change: the yaw innovation is folded into a half turn); extended Kalman filter with a constant-velocity model, its state in world coordinates and its process and measurement noise fixed in the object frame and rotated by the estimated heading; step 0.5 s; class-level process and measurement noise (car: position and velocity terms of the process noise 0.2005, 0.0255, 2.1560 and 0.0521, and of the measurement noise 0.2260, 0.0778, 0.7915 and 0.0369); detections kept above a class score threshold (car 0.16); two-stage association on generalised intersection over union; a track starts at its first unmatched detection and is deleted after 15 steps without an update; the planner receives each track's 4 × 4 position–velocity covariance |
| Planner | Decision every 0.1 s; horizon 3 s in steps of 0.05 s; 17 rows from the target accelerations −5, −2, 0 and 2 m/s² (jerk at most 8 m/s³, speed 0–20 m/s); cost weights 1 (speed), 0.05 (acceleration) and 0.02 (jerk); fallback: the (−5, −5) row |
| Software | Recordings: Python 3.10.12, NumPy 1.26.4, PyTorch 2.1.0 with CUDA 11.8, spconv 2.3.6, on Linux with an NVIDIA RTX 4090. Analysis: Python 3.12.2, NumPy 2.5.4, SciPy 1.18.1 |

> **TABLE S8.** Arms of the closed-loop check. Each is the state the planner uses with the worst-case stopping rule; none carries a tracker covariance margin.

| Arm | State and margin | Role |
|---|---|---|
| Z0 | Tracker state, no margin | Information-free |
| Zβ | Tracker state, the planner's own acceleration term | Information-free |
| F0 | Tracker state, class-average covariance margin ($k^2=1$) | Information-free |
| Td | True state at the last detector frame, held like a track; no margin | Reference (frame delay only) |

> **TABLE S4.** Reporting added or changed after the results. None changes code, data, arms, measures or populations; every number exists in the locked outputs, in named recounts, or in arithmetic on them (derive_v03.py, derive_v04.py, derive_v06.py, derive_v07.py); rows marked "(second revision)" instead report the analyses of Amendment 09, which add sources, frontier constructions and populations, and their numbers come from Section S11. Fixed wording on the left, reported wording on the right. In the fixed wordings, W1 is the 3 s commitment scoring and W_R(τ) the reaction-and-stop scoring.

| Item | Fixed before the results | Reported |
|---|---|---|
| The room | "a room of R [l, u] percentage points" | Followed by "under a 3 s commitment", with the room under the reaction-and-stop scoring relative to its 3 s value beside it (Amendment 02) |
| The two scorings | "W1 (3 s commitment) and W_R(τ) bracket the open-loop room" (withdrawn) | A strict and a lenient scoring of the same decisions, whose rooms are not ordered with count (ii) from τ = 1.25 s or at a 2 m gap (Amendment 02) |
| The tracker covariance's share | Printed by the analysis to 3 decimals | 3 significant figures; the non-smooth point explained; "at most about 0.4%" from the basic interval; never "not distinguishable from zero" (Amendment 02) |
| The NIS-inflated covariance in the abstract | "The abstract uses only this sentence": "a share distinguishable from zero, between 0.007 and 0.025; not robust to the convex-hull frontier" | Followed by its absolute size and phase estimates, which only weaken it; Results add the changed decisions and phase intervals (Amendments 02 and 03) |
| The NIS-inflated context in the abstract | "(0.09 percentage points; phase estimates −0.006 while the lead brakes, +0.079 after it stops)" (Amendment 03) | "(step frontier: 0.09 percentage points; phase shares −0.6% while the lead brakes, +7.9% after it stops)": the frontier named and the phase shares in percent, with the 83% in a sentence of its own under its own "Under a 3 s commitment" (Amendment 07) |
| The commitment in the abstract | The plan required the room with unjudgeable plans counted unsafe; an earlier abstract gave the primary count only | Both, 12% or 53% (Amendment 04, a correction) |
| The closed loop | The contact statement (Section S3.4) | Statement kept as fixed; added: the 2 m line, $c_2$, the scan brackets, the mechanism, the impacts and the fallback share; no closed-loop sentence in the abstract; validation wording corrected (Amendments 02, 04 and 06; Erratum 01) |
| The earlier pooled analysis | Its −4.5 points printed beside the room | Moved here; not comparable (different scoring and sign) |
| The claim sentence "always printed" | One sentence naming runs, recording setting, the earlier scoring, RR(N) and RR(NA) with intervals | Its content printed across Sections III-A, V-A and V-B in the paper's terms |
| The plan's timing | — | An earlier draft said the plan was fixed "before any evaluation-run value was read"; corrected to "before any evaluation-run value was computed under this scoring", with the earlier exploratory examination of the room and of the tracker covariance's difference from the class average on these runs stated beside it; the NIS-inflated claim rules, said to be fixed "before the evaluation runs were read", corrected to "before the NIS-inflated covariance was computed on the evaluation runs" (Sections III-A, IV-B and IV-D; Supplement S4; Section III-C names the arms computed on these runs before): a correction |
| The analyses added after the first results | Not in the first plan | Planned and hashed before any value (Amendment 05; lock `043b0b64…0e9`); descriptive; disclosed in Section IV-D in the paper's terms ("the A4 and A5 results" → "the first results", "arms" → "margin sources", "W1-oracle" → "3 s-oracle"; "from 13 Nov" left out) |
| The abstract's last sentence | "In lead braking, most decision value lies in anticipating braking, not in this tracker's covariance." | Set by the consequence rule fixed in the plan of Amendment 05: the weakest of the braking prediction's three statistics (branch 1, the phase-weighted aggregate) gives "once the car reacts within 0.75 s, too little room remains for the braking prior's share to be measured" (Section S8.1); printed as the last sentence with a capital letter and "phase by phase": "once the car reacts within 0.75 s, too little room remains, phase by phase, for the braking prior's share to be measured". "Phase by phase" names the population the rule judged (the phase-weighted aggregate) and was added after the results (Amendment 06); Section V-C names the phase-weighted aggregate as the weakest of the three statistics that the plan fixed for the abstract. Amendment 07: "once the car reacts within 0.75 s," → "With that stop, unless those plans count as unsafe,", naming the 6 m/s² stop of the previous sentence, on which the sentence depends (at 4 m/s² the phase-weighted room is 14.8 decision-equivalents), and the count under which the rule's statistic was taken (as scored; under count (ii) the phase-weighted share is 0.11 [0.06, 0.18]). Quotations keep the plan's name "braking prior"; the source is now called the braking prediction |
| The reaction-and-stop conclusions at τ = 0.75 s | The consequence sentence, from branch 1 of the phase-weighted aggregate as scored | Qualified by the count it holds for, with the count (ii) values beside it (Table IV, Table S10): a qualifier added after the results (Amendment 07) |
| The abstract's commitment sentence | Add "and with a perfect stop 0.75 s after committing little W1-oracle advantage remains while the lead brakes (0.19 percentage points)" | "little of it remaining while the lead brakes (0.19 percentage points)", "it" being "the room", the oracle's advantage defined in the abstract's third sentence, with the clause attached to the as-scored count of the 6 m/s² stop, before the count (ii) clause (Amendment 06; Amendment 07) |
| The NIS-inflated sentence and the 83% in the abstract | Unqualified | Both under "Under a 3 s commitment" (the plan's NA rule and its "always" rule for the 83%) |
| The abstract's wording | An earlier abstract: "A tracker's covariance can set a planner's safety margin. We test whether this improves decisions …"; "at equal caution, assuming plans are followed for 3 s"; "An oracle margin set from …"; "The tracker's covariance recovers at most about 0.4% of it, being effectively constant: its margin stays within 5% of 1.10 times the class average in over 99% of decision rows" | "We test whether a tracker's covariance, used as a planner's safety margin, improves decisions …"; "at equal caution under a 3 s commitment"; "An oracle margin from …"; "The tracker's covariance, effectively constant (its margin within 5% of 1.10 times the class average in over 99% of decision rows), recovers at most about 0.4% of it": the same content in fewer words, for the limit of 250 words (Amendment 06) |
| The abstract's wording (Amendment 07) | The Amendment 06 abstract | "beyond simpler information" dropped; "a speed planner's" → "a planner's"; the two oracle sentences merged, with "the room" defined at first use; "emergency" dropped; "the oracle's advantage falls to 12%" → "it falls to 12%"; "at every evaluable delay" → "wherever estimable" (Amendment 07) |
| Branch wording of the added analyses | "… of the remaining room" | "… of the class-average margin's avoidable wrong-go under this scoring" (a clarification written before the lock) |
| The oracle under the reaction-and-stop scoring | "the W1 oracle margin scored under W_R(τ)" | "the 3 s oracle's advantage under the reaction-and-stop scoring" (a change of name) |
| The reliability check's claim sentences | "the tracker's stated deviation ranks it (ρ = …; … ρ\* = …)" | Printed with the class average's ρ on the same decisions, the spread of the deviation ratio, the reference ρ\* (fixed as a ceiling; renamed because a correlation can exceed it) and the propagation over the state's age; "the planner's propagated deviation" at t > 0 |
| Table IV | The table of record: τ = 0.75 s, as scored and count (ii), pooled and phase-weighted | An "Ego moving" column added |
| Section V-D (table of record) | "RMS(z) and the mean error by phase at t = 0" in the main text | Lead-braking phase kept in Section V-D; before-onset and after-stop values, the t = 1 s value, the reliability ends and the NIS-inflated deviation moved to Supplement S9 for length |
| Shares before the onset under the 3 s commitment | Printed with their intervals | "Too few to evaluate" (2.9 decision-equivalents; the resolution rule of Section IV-C) |
| The title (this version) | "Does a Kalman Tracker's Covariance Improve Car-Following Decisions? A Decision-Level Evaluation in CARLA Lead-Braking Scenarios" | Retitled around the evaluation, with the fixed-noise tracker named as the case |
| The abstract (this version) | The 249-word abstract of the earlier draft (in the deposit) | Rewritten in plain terms with fewer numbers: the calibrated intervals, 12% in place of "12% … or 53%", the per-phase and after-stop results, and the ratio check by scenario family |
| The tracker covariance's share (this version) | "at most about 0.4% of the room", from the basic interval | The point, the calibrated percentile interval [−0.0016, 0.0017], and the statement that no interval method reaches 0.5% of the room (Section S10.1) |
| The commitment (this version) | "it falls to 12% … or to 53% when plans whose stop is unfinished within the 3 s window count as unsafe" | 0.122 [0.052, 0.188] with plans judged until their stop ends. Count (ii) is no longer used: 28 of its 5,356 pairs are unsafe (Section S10.2). Tables S6, S9 and S10 keep the earlier scoring as the record |
| The location of the room (this version) | "the decision value we could measure lies in anticipating braking under the 3 s commitment"; "a mechanism that no analysis here isolates" | Replaced by the after-stop and per-phase results and by a conditional statement (Sections V-C and VI; Section S10.4) |
| The braking source's name (this version) | "braking prior", "an RSS-style assumption" | "braking prediction": a nominal constant-deceleration prediction, not a worst-case bound; the RSS form is used only by the rule of Section S3 |
| The abstract's last sentence (this version) | Set by the consequence rule of the second plan and printed as "too little room remains, phase by phase, for the braking prior's share to be measured" ("phase by phase" added after the results) | No longer in the abstract. The statistic it reports is in Section V-D and Table IV: the phase-weighted amount is not evaluable |
| Intervals (this version) | Nominal 95% percentile intervals, their coverage "not verified" | Coverage estimated by a double bootstrap; calibrated intervals for the pooled headline quantities (Section S10.1) |
| Moved for length (this version) | In the main text of the earlier draft | The planner's cost (Section S1), the stopping-point error (Section S2), the check of the tracker's deviation (Section S9), Table IV (Table S29) and Fig. 3 (Fig. S4) |
| Analyses added in revision | — | Section S10: each defined before its values were read; descriptive |
| The tracker covariance's share (second revision) | The calibrated percentile interval [−0.0016, 0.0017] and "no interval method we tried reaches 0.5% of the room" | A grid placebo and a gridless frontier (Section S11.1) and a bound of 2.2 decisions over every interval end computed, formed after the values were read; the calibrated interval kept in Section V-A; the 0.5% statement withdrawn (Amendment 09) |
| The per-phase result (second revision) | "recovers 89% of the room" | 89% in sample, 90% held out, 99.9% held out on the tracker's own phase estimate (Section S11.3; Amendment 09) |
| The braking prediction's share without the after-stop decisions (second revision) | "29%" in the abstract, against the acceleration margin's 43% | Not read as a share: the measure does not grade there (Section S11.10; Addendum 01); frontier distances in decisions instead |
| The location of the room (second revision) | "a mechanism that no analysis here isolates" (Section S8.2 of the first revision) | The room before the lead's stop and in the first second after it, where the tracker's velocity lags the stop (Section S11.4); Section S8.2 rewritten |
| The NIS-inflated sentence in the abstract | "The abstract uses only this sentence": "a share distinguishable from zero, between 0.007 and 0.025; not robust to the convex-hull frontier" | Not in the abstract since the first revision, whose rewritten abstract left it out for length; the rule's outcome (rule 5) is in Section V-B, with the calibrated interval. A deviation from the plan |
| The abstract and the contributions (second revision) | — | Fences for the steady state, the population mix, the truth-labelled phases and the analyses added later; the bound in place of the calibrated interval; the recording policy among the conditions of an open-loop score (Amendment 09) |
| Draft history (second revision) | Rows added in drafts v03, v04 and v06, and the earlier drafts' abstracts | Moved to the deposit (DRAFT_HISTORY); this table keeps the deviations from the plans |

> **TABLE S5.** Room *R* (percentage points of wrong-go decisions) and the share of the room recovered, RR, by population, with 95% run-bootstrap percentile intervals. 35 evaluation runs (recorded with the native-covariance setting; a transfer, not a replication); 3 s commitment; step frontier unless marked "hull". Each population is scored on its own frontier and caution levels, so the phase values do not decompose the pooled value. \* One-code interval; § margins from one extraction.

| Quantity | All | All, hull | Ego moving | Before onset | Lead braking | Lead stopped |
|---|---|---|---|---|---|---|
| Evaluated decisions | 8,290 | 8,290 | 1,863 | 678 | 755 | 6,857 |
| Share of evaluated decisions | 1.000 | 1.000 | 0.225 | 0.082 | 0.091 | 0.827 |
| Room $R$ (pp) | 5.56 [4.50, 6.60] | 3.98 [3.30, 4.50] | 10.16 [7.96, 12.39] | 0.43 | 15.59 | 0.82 |
| RR(N) | 0.00122 [−0.00108, 0.00119] | −0.00197 [−0.00309, 0.00502] | −0.000131 [−0.00577, 0.00159] | 0.00510 [−0.0290, 0.0205]\* | −0.00245 [−0.00478, 0.00518]\* | 0.00186 [−0.00449, 0.00428]\* |
| RR(NA) | 0.0167 [0.00729, 0.0252] | 0.00136 [−0.00398, 0.0118] | 0.0157 [0.00159, 0.0281] | 0.00340 [−0.0297, 0.0205]\* | −0.00638 [−0.0312, 0.0226] | 0.0790 [0.0339, 0.123] |
| RR(AM) | 0.376 [0.316, 0.425] | 0.153 [0.0780, 0.232] | 0.293 [0.207, 0.350]\* | −0.128 | −0.0437 | 0.702 |
| RR(CK3) | 0.831 [0.753, 0.903] | 0.750 [0.647, 0.842] | 0.472 [0.353, 0.570] | −0.536 [−3.76, 0.175]\* | 0.606 [0.468, 0.711]\* | 0.993 [0.914, 1.11]\* |
| RR(Q)§ | −0.00180 [−0.00655, 0.00116] | −0.00328 [−0.0142, 0.00664] | 0.00176 [−0.00670, 0.00499]\* | −0.00340 | −0.000296 | −0.0143 |

> **TABLE S6.** The reaction-and-stop scoring in every setting, and the two counts of the plans the 3 s truth window cannot judge. 35 evaluation runs, all evaluated decisions, step frontier. Columns: τ; the stop deceleration *A*; the required standstill gap; *R*, the 3 s oracle's advantage, with its 95% interval; the share of resamples without room; RR(N), given only where at most 2.5% of resamples have no room; and the advantage relative to the 3 s room (5.56 points) as scored, with count (i) and with count (ii). No ratio is printed at a 2 m gap, where the 3 s oracle is not an oracle; these rows are reported without interpretation. \* One code.

| τ (s) | $A$ (m/s²) | Gap (m) | $R$ (pp) [95%] | No room | RR(N) [95%] | Relative [95%] | (i), relative [95%] | (ii), relative [95%] |
|---|---|---|---|---|---|---|---|---|
| 0.5 | 6 | 0 | 0.10 [0.00, 0.30] | 0.1280 | not estimated (12.8% without room) | 0.019 [0.000, 0.052] | 0.029 [0.004, 0.064]\* | 0.447 [0.203, 0.693]\* |
| 0.75 | 6 | 0 | 0.67 [0.24, 1.17] | 0.0000 | 0.000179 [−0.00680, 0.00524] | 0.121 [0.051, 0.187] | 0.143 [0.071, 0.211]\* | 0.531 [0.259, 0.790] |
| 1.0 | 6 | 0 | 1.30 [0.63, 2.02] | 0.0000 | 0.00111 [−0.00551, 0.00430] | 0.234 [0.133, 0.319] | 0.269 [0.168, 0.359]\* | 0.636 [0.358, 0.892]\* |
| 1.25 | 6 | 0 | 2.03 [1.16, 2.92] | 0.0000 | 0.00101 [−0.00342, 0.00178] | 0.364 [0.246, 0.461] | 0.410 [0.292, 0.512]\* | 1.295 [1.023, 1.538] |
| 1.5 | 6 | 0 | 2.72 [1.75, 3.72] | 0.0000 | 0.00104 [−0.00191, 0.00138] | 0.490 [0.371, 0.584] | 0.547 [0.426, 0.652]\* | 1.360 [1.086, 1.616]\* |
| 1.8 | 6 | 0 | 3.58 [2.47, 4.67] | 0.0000 | 0.00129 [−0.00126, 0.00150] | 0.644 [0.529, 0.730] | 0.708 [0.587, 0.814]\* | 1.146 [0.903, 1.390]\* |
| 0.75 | 4 | 0 | 1.41 [0.69, 2.16] | 0.0000 | −0.000640 [−0.00508, 0.00292] | 0.253 | 0.294\* | 0.800\* |
| 0.75 | 5 | 0 | 0.90 [0.36, 1.51] | 0.0000 | 0.000532 [−0.00449, 0.00424] | 0.162 | 0.200\* | 0.209\* |
| 0.75 | 7.6 | 0 | 0.35 [0.08, 0.70] | 0.0005 | −0.00271 [−0.00825, 0.00860] | 0.064 | 0.066\* | 0.412\* |
| 1.8\* | 4 | 0 | 3.91 [2.81, 4.97] | 0.0000 | 0.00151 [−0.000972, 0.00170] | 0.703 | 0.780 | 1.031 |
| 1.8\* | 5 | 0 | 3.74 [2.63, 4.82] | 0.0000 | 0.00104 [−0.00152, 0.00123] | 0.673 | 0.749 | 1.162 |
| 1.8\* | 7.6 | 0 | 3.45 [2.36, 4.52] | 0.0000 | 0.00122 [−0.00122, 0.00148] | 0.621 | 0.660 | 1.415 |
| 0.75\* | 6 | 2 | −0.10 [−1.89, 1.29] | 0.4481 | no RR (negative room) | — | — | — |
| 1.8\* | 6 | 2 | 2.54 [0.19, 4.39] | 0.0187 | −0.00579 [−0.0230, 0.00410] | — | — | — |
| 0.75\* | 4 | 2 | 0.72 [−1.30, 2.19] | 0.1910 | not evaluable | — | — | — |
| 0.75\* | 5 | 2 | 0.31 [−1.63, 1.80] | 0.2999 | not evaluable | — | — | — |
| 0.75\* | 7.6 | 2 | −0.38 [−2.08, 0.91] | 0.5574 | no RR (negative room) | — | — | — |
| 1.8\* | 4 | 2 | 2.82 [0.42, 4.74] | 0.0141 | −0.00492 [−0.0188, 0.00402] | — | — | — |
| 1.8\* | 5 | 2 | 2.68 [0.29, 4.57] | 0.0165 | −0.00493 [−0.0202, 0.00452] | — | — | — |
| 1.8\* | 7.6 | 2 | 2.51 [0.15, 4.31] | 0.0200 | −0.00570 [−0.0233, 0.00422] | — | — | — |

> **TABLE S1.** The tracker's covariance against the class average under each scoring: D(N, F0)/201, the mean over 201 caution levels of F0 minus N wrong-go, in percentage points, with its 95% run-bootstrap percentile interval; 35 evaluation runs, all evaluated decisions, step frontier; the 3 s commitment and all 20 reaction-and-stop settings. † On the 3 s row, the point, 0.0068, lies above its percentile interval [−0.0061, 0.0065], as for RR(N), because the statistic is non-smooth. \* One code.

| Scoring or τ (s) | $A$ (m/s²) | Gap (m) | D(N, F0)/201 (pp) | 95% interval |
|---|---|---|---|---|
| 3 s commitment† | — | — | 0.0068 | [−0.0061, 0.0065]\* |
| 0.5 | 6 | 0 | −0.0003 | [−0.0021, 0.0007] |
| 0.75 | 6 | 0 | 0.0001 | [−0.0041, 0.0034] |
| 1.0 | 6 | 0 | 0.0014 | [−0.0068, 0.0050] |
| 1.25 | 6 | 0 | 0.0020 | [−0.0067, 0.0033] |
| 1.5 | 6 | 0 | 0.0028 | [−0.0051, 0.0037] |
| 1.8 | 6 | 0 | 0.0046 | [−0.0045, 0.0053] |
| 0.75 | 4 | 0 | −0.0009 | [−0.0067, 0.0036] |
| 0.75 | 5 | 0 | 0.0005 | [−0.0035, 0.0035] |
| 0.75 | 7.6 | 0 | −0.0010 | [−0.0034, 0.0026] |
| 1.8 | 4 | 0 | 0.0059 | [−0.0039, 0.0065]\* |
| 1.8 | 5 | 0 | 0.0039 | [−0.0056, 0.0046]\* |
| 1.8 | 7.6 | 0 | 0.0042 | [−0.0042, 0.0050]\* |
| 0.75 | 6 | 2 | −0.0007 | [−0.0088, 0.0052]\* |
| 1.8 | 6 | 2 | −0.0147 | [−0.0287, 0.0077]\* |
| 0.75 | 4 | 2 | 0.0028 | [−0.0063, 0.0086]\* |
| 0.75 | 5 | 2 | 0.0008 | [−0.0059, 0.0075]\* |
| 0.75 | 7.6 | 2 | −0.0017 | [−0.0081, 0.0044]\* |
| 1.8 | 4 | 2 | −0.0139 | [−0.0289, 0.0086]\* |
| 1.8 | 5 | 2 | −0.0132 | [−0.0279, 0.0089]\* |
| 1.8 | 7.6 | 2 | −0.0143 | [−0.0286, 0.0079]\* |

> **TABLE S2.** The commitment sensitivity on the 20 tuning runs and on the 35 evaluation runs, at *A* = 6 m/s² and zero gap; all evaluated decisions; step frontier. For each set: the summed frontier difference, and the room relative to the set's own 3 s room (tuning 237.24; evaluation 1116.91) as scored and with count (ii).

| τ (s) | Tuning: summed F0 − E frontier difference | Tuning: relative to 3 s | Tuning: count (ii), relative to 3 s | Evaluation: summed F0 − E frontier difference | Evaluation: relative to 3 s [95%] | Evaluation: count (ii), relative to 3 s [95%] |
|---|---|---|---|---|---|---|
| 3 s commitment | 237.24 | 1 | 1 | 1116.91 | 1 | 1 |
| 0.5 | 0.89\* | 0.004\* | 1.105\* | 20.87 | 0.019 [0.000, 0.052] | 0.447 [0.203, 0.693]\* |
| 0.75 | 5.50 | 0.023 | 1.237\* | 135.02 | 0.121 [0.051, 0.187] | 0.531 [0.259, 0.790] |
| 1.0 | 12.66\* | 0.053\* | 1.267\* | 261.13 | 0.234 [0.133, 0.319] | 0.636 [0.358, 0.892]\* |
| 1.25 | 22.66 | 0.096 | 2.315\* | 407.10 | 0.364 [0.246, 0.461] | 1.295 [1.023, 1.538] |
| 1.5 | 41.72\* | 0.176\* | 2.591\* | 547.65 | 0.490 [0.371, 0.584] | 1.360 [1.086, 1.616]\* |
| 1.8 | 99.04 | 0.417 | 1.575\* | 719.58 | 0.644 [0.529, 0.730] | 1.146 [0.903, 1.390]\* |

> **TABLE S3.** Descriptive splits and the secondary contrasts; 35 evaluation runs, 3 s commitment, step frontier, all evaluated decisions. Splits by the recording setting α and by the desired speed give runs, decisions, *R* and RR(NA) as points, each group scored on its own frontier. The three paired contrasts are given with their 95% run-bootstrap percentile intervals and the wording fixed before the results (secondary; not adjusted for multiplicity).

| Group | Value | Runs | Decisions | $R$ (pp) | RR(NA) |
|---|---|---|---|---|---|
| Recording setting α | 1.642 | 10 | 1,761 | 4.71 | 0.0165 |
| Recording setting α | 5.412 | 12 | 3,006 | 4.64 | 0.0112 |
| Recording setting α | 7.550 | 13 | 3,523 | 6.76 | 0.0163 |
| Desired speed | 5.0 m/s | 15 | 4,065 | 3.13 | 0.000586 |
| Desired speed | 10.0 m/s | 12 | 2,774 | 3.88 | 0.00800 |
| Desired speed | 15.0 m/s | 8 | 1,451 | 5.23 | −0.00302 |

| Paired contrast | Point [95%] | Wording fixed before the results |
|---|---|---|
| RR(NA) − RR(N) | 0.0154 [0.00729, 0.0251] | NA recovers more of the room than N |
| RR(NA) − RR(CK3) | −0.815 [−0.891, −0.734] | NA recovers less than CK3 |
| RR(AM) − RR(CK3) | −0.456 [−0.523, −0.391] | AM recovers less than CK3 |

> **TABLE S9.** The 3 s scoring and the reaction-and-stop scoring (R&S) as scored (stop at 6 m/s², jerk 12.65 m/s³, zero gap), by population: den₀ in decision-equivalents with its 95% interval (and the share of resamples with den₀ ≤ 0, when positive), the 3 s oracle's RR₀, and each source's RR₀ with its 95% interval and branch b (S8.1; † not robust to the convex-hull frontier). The 3 s rows use the 3 s scoring's perfect oracle. 35 evaluation runs; step frontier; each population on its own frontier. Caution counted at its signed value: Table S13. Two programs.

| Scoring | τ (s) | Population | n | den₀, dec.-eq. [95%] | RR₀(E) [95%] | RR₀(N) [95%] (b) | RR₀(NA) [95%] (b) | RR₀(CK3) [95%] (b) | RR₀(AM) [95%] (b) | RR₀(Q) [95%] (b) |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 s | — | All | 8,290 | 497.08 [394.02, 597.08] | 0.927 [0.851, 0.983] | 0.001 [−0.001, 0.001] (3) | 0.015 [0.007, 0.023] (5†) | 0.771 [0.695, 0.835] (4) | 0.348 [0.290, 0.396] (5) | −0.002 [−0.006, 0.001] (3) |
| 3 s | — | Ego moving | 1,863 | 194.99 [149.61, 238.74] | 0.971 [0.960, 0.991] | −0.000 [−0.006, 0.002] (3) | 0.015 [0.002, 0.027] (5†) | 0.458 [0.343, 0.555] (5) | 0.285 [0.201, 0.343] (5) | 0.002 [−0.007, 0.005] (3) |
| 3 s | — | Before onset | 678 | 2.97 [0.41, 7.62]; 0.01% ≤ 0 | 0.985 [0.953, 1.000] | 0.005 [−0.029, 0.020] (1) | 0.003 [−0.029, 0.020] (1) | −0.528 [−3.634, 0.174] (1) | −0.126 [−0.407, 0.164] (1) | −0.003 [−0.148, 0.046] (1) |
| 3 s | — | Lead braking | 755 | 119.00 [84.69, 153.24] | 0.989 [0.984, 0.992] | −0.002 [−0.005, 0.005] (3) | −0.006 [−0.031, 0.022] (3) | 0.600 [0.462, 0.703] (5) | −0.043 [−0.191, 0.062] (3) | −0.000 [−0.008, 0.010] (3) |
| 3 s | — | Lead stopped | 6,857 | 66.91 [49.93, 85.37] | 0.841 [0.703, 0.950] | 0.002 [−0.004, 0.004] (3) | 0.066 [0.028, 0.107] (5) | 0.835 [0.749, 0.913] (4) | 0.591 [0.472, 0.703] (5) | −0.012 [−0.030, 0.004] (3) |
| 3 s | — | Phase-weighted | 8,290 | 188.87 [147.18, 231.52] | 0.937 [0.875, 0.977] | −0.001 [−0.003, 0.004] (3) | 0.020 [0.001, 0.043] (5†) | 0.665 [0.575, 0.740] (4) | 0.180 [0.086, 0.260] (5) | −0.005 [−0.012, 0.005] (3) |
| R&S | 0.5 | All | 8,290 | 9.32 [0.00, 27.22]; 12.80% ≤ 0 | 0.924 [0.868, 0.989] | −0.003 [−0.010, 0.021] (1) | −0.005 [−0.011, 0.019] (1) | 0.879 [0.840, 0.945] (1) | 0.573 [0.449, 0.715] (1) | −0.145 [−0.217, 0.038] (1) |
| R&S | 0.5 | Ego moving | 1,863 | 1.72 [0.00, 4.90]; 12.80% ≤ 0 | 0.925 [0.911, 1.000] | −0.006 [−0.042, 0.041] (1) | −0.040 [−0.089, 0.000] (1) | −0.676 [−1.518, 0.085] (1) | 0.254 [0.173, 0.393] (1) | −0.173 [−0.241, 0.083] (1) |
| R&S | 0.5 | Before onset | 678 | 0.00 [0.00, 0.00]; 100.00% ≤ 0 | no room | no room (1) | no room (1) | no room (1) | no room (1) | no room (1) |
| R&S | 0.5 | Lead braking | 755 | 0.06 [0.00, 0.20]; 13.84% ≤ 0 | 1.000 [1.000, 1.000] | 0.000 [−0.115, 0.000] (1) | −0.077 [−0.385, 0.000] (1) | −9.000 [−25.000, −1.444] (1) | −0.231 [−1.442, 0.643] (1) | −0.308 [−0.556, 0.000] (1) |
| R&S | 0.5 | Lead stopped | 6,857 | 1.51 [0.00, 5.30]; 36.20% ≤ 0 | 0.780 [0.629, 0.931] | −0.016 [−0.020, −0.003] (1) | −0.016 [−0.023, −0.005] (1) | 0.737 [0.627, 0.853] (1) | 0.395 [0.238, 0.578] (1) | −0.326 [−0.513, −0.190] (1) |
| R&S | 0.5 | Phase-weighted | 8,290 | 1.58 [0.00, 5.48]; 13.84% ≤ 0 | 0.789 [0.651, 1.000] | −0.016 [−0.020, 0.000] (1) | −0.019 [−0.028, 0.000] (1) | 0.338 [−19.000, 0.683] (1) | 0.369 [0.000, 0.609] (1) | −0.325 [−0.489, 0.000] (1) |
| R&S | 0.75 | All | 8,290 | 58.16 [20.41, 102.52] | 0.957 [0.920, 0.988] | 0.000 [−0.007, 0.005] (3) | 0.012 [−0.004, 0.039] (3) | 0.936 [0.908, 0.958] (4) | 0.570 [0.472, 0.665] (5) | −0.032 [−0.075, 0.012] (3) |
| R&S | 0.75 | Ego moving | 1,863 | 12.02 [4.23, 20.97] | 0.951 [0.940, 1.000] | −0.013 [−0.032, 0.006] (3) | −0.021 [−0.057, 0.020] (3) | 0.034 [−0.471, 0.377] (3) | 0.257 [0.168, 0.339] (5) | −0.045 [−0.095, 0.021] (3) |
| R&S | 0.75 | Before onset | 678 | 0.00 [0.00, 0.00]; 100.00% ≤ 0 | no room | no room (1) | no room (1) | no room (1) | no room (1) | no room (1) |
| R&S | 0.75 | Lead braking | 755 | 1.45 [0.32, 2.94]; 0.01% ≤ 0 | 1.000 [1.000, 1.000] | −0.003 [−0.060, 0.070] (1) | −0.154 [−0.365, 0.021] (1) | −1.106 [−4.727, 0.512] (1) | −0.668 [−1.580, −0.152] (1) | −0.048 [−0.207, 0.212] (1) |
| R&S | 0.75 | Lead stopped | 6,857 | 2.23 [0.11, 6.33]; 0.48% ≤ 0 | 0.811 [0.652, 0.982] | 0.000 [−0.032, 0.047] (1) | 0.042 [−0.024, 0.250] (1) | 0.788 [0.662, 1.000] (1) | 0.350 [−0.364, 0.647] (1) | −0.252 [−0.502, 0.065] (1) |
| R&S | 0.75 | Phase-weighted | 8,290 | 3.69 [0.74, 8.73] | 0.885 [0.777, 0.996] | −0.001 [−0.031, 0.036] (1) | −0.035 [−0.129, 0.078] (1) | 0.042 [−2.175, 0.705] (1) | −0.051 [−0.684, 0.216] (1) | −0.171 [−0.304, 0.109] (1) |
| R&S | 1.0 | All | 8,290 | 113.23 [53.49, 178.52] | 0.951 [0.909, 0.986] | 0.001 [−0.005, 0.004] (3) | 0.014 [0.002, 0.033] (5†) | 0.942 [0.918, 0.961] (4) | 0.538 [0.458, 0.620] (5) | −0.026 [−0.051, 0.001] (3) |
| R&S | 1.0 | Ego moving | 1,863 | 27.22 [12.50, 42.83] | 0.962 [0.952, 1.000] | −0.010 [−0.026, 0.006] (3) | −0.005 [−0.031, 0.022] (3) | 0.292 [−0.054, 0.530] (3) | 0.278 [0.187, 0.348] (5) | −0.040 [−0.070, −0.005] (2) |
| R&S | 1.0 | Before onset | 678 | 0.00 [0.00, 0.00]; 100.00% ≤ 0 | no room | no room (1) | no room (1) | no room (1) | no room (1) | no room (1) |
| R&S | 1.0 | Lead braking | 755 | 6.87 [2.11, 13.00] | 1.000 [1.000, 1.000] | −0.013 [−0.069, 0.038] (1) | −0.079 [−0.225, 0.014] (1) | 0.282 [−0.878, 0.833] (1) | −0.379 [−0.937, −0.102] (1) | −0.059 [−0.184, 0.041] (1) |
| R&S | 1.0 | Lead stopped | 6,857 | 6.23 [1.63, 12.86]; 0.02% ≤ 0 | 0.843 [0.722, 0.956] | −0.006 [−0.026, 0.027] (1) | 0.054 [−0.009, 0.207] (1) | 0.871 [0.728, 0.979] (1) | 0.494 [0.242, 0.768] (1) | −0.220 [−0.336, 0.007] (1) |
| R&S | 1.0 | Phase-weighted | 8,290 | 13.10 [4.46, 24.13] | 0.926 [0.846, 0.984] | −0.010 [−0.035, 0.024] (3) | −0.016 [−0.078, 0.074] (3) | 0.562 [−0.065, 0.868] (3) | 0.036 [−0.308, 0.273] (3) | −0.136 [−0.198, −0.018] (2) |
| R&S | 1.25 | All | 8,290 | 178.01 [99.96, 260.01] | 0.943 [0.890, 0.985] | 0.001 [−0.003, 0.002] (3) | 0.024 [0.008, 0.045] (5†) | 0.943 [0.919, 0.962] (4) | 0.527 [0.449, 0.603] (5) | −0.017 [−0.034, −0.004] (2) |
| R&S | 1.25 | Ego moving | 1,863 | 47.55 [26.24, 69.63] | 0.968 [0.959, 1.000] | −0.003 [−0.016, 0.003] (3) | 0.013 [−0.014, 0.041] (3) | 0.431 [0.179, 0.619] (5) | 0.315 [0.221, 0.385] (5) | −0.016 [−0.043, 0.004] (3) |
| R&S | 1.25 | Before onset | 678 | 0.00 [0.00, 0.00]; 100.00% ≤ 0 | no room | no room (1) | no room (1) | no room (1) | no room (1) | no room (1) |
| R&S | 1.25 | Lead braking | 755 | 16.02 [6.88, 27.72] | 1.000 [0.999, 1.000] | −0.003 [−0.020, 0.020] (3) | −0.053 [−0.161, 0.027] (3) | 0.573 [0.003, 0.900] (5) | −0.203 [−0.533, 0.016] (3) | 0.003 [−0.058, 0.057] (3) |
| R&S | 1.25 | Lead stopped | 6,857 | 12.60 [4.98, 22.78] | 0.856 [0.740, 0.954] | −0.007 [−0.029, 0.009] (3) | 0.117 [0.035, 0.214] (5) | 0.853 [0.738, 0.946] (4) | 0.564 [0.381, 0.742] (5) | −0.082 [−0.210, 0.003] (3) |
| R&S | 1.25 | Phase-weighted | 8,290 | 28.62 [13.62, 46.64] | 0.937 [0.866, 0.984] | −0.005 [−0.016, 0.009] (3) | 0.022 [−0.040, 0.083] (3) | 0.696 [0.365, 0.889] (5) | 0.135 [−0.072, 0.309] (3) | −0.034 [−0.090, 0.019] (3) |
| R&S | 1.5 | All | 8,290 | 242.21 [152.31, 334.07] | 0.933 [0.866, 0.983] | 0.001 [−0.002, 0.001] (3) | 0.023 [0.011, 0.038] (5†) | 0.938 [0.911, 0.958] (4) | 0.482 [0.410, 0.548] (5) | −0.013 [−0.026, −0.003] (2) |
| R&S | 1.5 | Ego moving | 1,863 | 73.54 [45.85, 101.60] | 0.967 [0.945, 0.999] | −0.002 [−0.010, 0.002] (3) | 0.019 [−0.004, 0.041] (3) | 0.528 [0.331, 0.680] (5) | 0.323 [0.226, 0.393] (5) | −0.007 [−0.024, 0.007] (3) |
| R&S | 1.5 | Before onset | 678 | 0.00 [0.00, 0.00]; 100.00% ≤ 0 | no room | no room (1) | no room (1) | no room (1) | no room (1) | no room (1) |
| R&S | 1.5 | Lead braking | 755 | 32.67 [17.73, 50.45] | 0.999 [0.998, 1.000] | −0.004 [−0.012, 0.009] (3) | −0.025 [−0.093, 0.032] (3) | 0.719 [0.384, 0.921] (5) | −0.145 [−0.424, 0.056] (3) | 0.009 [−0.023, 0.041] (3) |
| R&S | 1.5 | Lead stopped | 6,857 | 17.78 [8.30, 30.43] | 0.848 [0.722, 0.952] | 0.001 [−0.010, 0.009] (3) | 0.113 [0.055, 0.200] (5) | 0.855 [0.742, 0.950] (4) | 0.597 [0.425, 0.761] (5) | −0.044 [−0.119, 0.010] (3) |
| R&S | 1.5 | Phase-weighted | 8,290 | 50.45 [28.01, 76.71] | 0.946 [0.886, 0.985] | −0.002 [−0.009, 0.006] (3) | 0.024 [−0.017, 0.071] (3) | 0.767 [0.542, 0.906] (4) | 0.116 [−0.067, 0.268] (3) | −0.010 [−0.041, 0.023] (3) |
| R&S | 1.8 | All | 8,290 | 319.22 [216.22, 420.81] | 0.930 [0.859, 0.983] | 0.001 [−0.001, 0.001] (3) | 0.022 [0.010, 0.034] (5†) | 0.899 [0.851, 0.932] (4) | 0.423 [0.350, 0.488] (5) | −0.009 [−0.019, −0.002] (2) |
| R&S | 1.8 | Ego moving | 1,863 | 111.18 [76.24, 145.50] | 0.967 [0.951, 0.996] | −0.001 [−0.008, 0.001] (3) | 0.019 [0.001, 0.037] (5†) | 0.558 [0.409, 0.678] (5) | 0.311 [0.208, 0.388] (5) | −0.005 [−0.019, 0.004] (3) |
| R&S | 1.8 | Before onset | 678 | 0.69 [0.00, 2.40]; 36.45% ≤ 0 | 1.000 [1.000, 1.000] | −0.022 [−0.034, 0.008] (1) | −0.022 [−0.034, 0.008] (1) | 0.094 [−0.083, 0.179] (1) | −0.239 [−0.532, −0.095] (1) | 0.022 [−0.020, 0.060] (1) |
| R&S | 1.8 | Lead braking | 755 | 60.00 [37.83, 84.68] | 0.999 [0.998, 1.000] | −0.004 [−0.010, 0.005] (3) | −0.014 [−0.057, 0.026] (3) | 0.727 [0.502, 0.867] (4) | −0.087 [−0.315, 0.098] (3) | −0.003 [−0.024, 0.016] (3) |
| R&S | 1.8 | Lead stopped | 6,857 | 27.81 [16.55, 41.46] | 0.859 [0.739, 0.956] | 0.004 [−0.003, 0.009] (3) | 0.115 [0.059, 0.172] (5) | 0.894 [0.804, 0.964] (4) | 0.625 [0.469, 0.764] (5) | −0.031 [−0.077, 0.012] (3) |
| R&S | 1.8 | Phase-weighted | 8,290 | 88.50 [58.13, 122.07] | 0.955 [0.908, 0.987] | −0.002 [−0.006, 0.004] (3) | 0.026 [−0.002, 0.061] (3) | 0.775 [0.616, 0.876] (4) | 0.135 [−0.016, 0.276] (3) | −0.012 [−0.032, 0.011] (3) |

> **TABLE S10.** As Table S9, under count (ii): plans whose stop is unfinished within the 3 s window count as unsafe. The perfect oracle for this count costs caution, so den₀ is not a room at every level. Two programs.

| Scoring | τ (s) | Population | n | den₀, dec.-eq. [95%] | RR₀(E) [95%] | RR₀(N) [95%] (b) | RR₀(NA) [95%] (b) | RR₀(CK3) [95%] (b) | RR₀(AM) [95%] (b) | RR₀(Q) [95%] (b) |
|---|---|---|---|---|---|---|---|---|---|---|
| Count (ii) | 0.5 | All | 8,290 | 300.48 [122.46, 484.78]; 0.01% ≤ 0 | 0.685 [0.610, 0.750] | 0.000 [−0.002, 0.001] (3) | 0.003 [−0.002, 0.006] (3) | 0.507 [0.303, 0.698] (5) | 0.099 [0.056, 0.132] (5†) | −0.005 [−0.016, 0.001] (3) |
| Count (ii) | 0.5 | Ego moving | 1,863 | 171.83 [73.10, 266.57]; 0.01% ≤ 0 | 0.237 [−0.021, 0.397] | −0.002 [−0.005, 0.001] (3) | 0.003 [−0.011, 0.017] (3) | 0.333 [0.165, 0.556] (5) | 0.088 [−0.056, 0.183] (3) | −0.004 [−0.017, 0.003] (3) |
| Count (ii) | 0.5 | Before onset | 678 | 84.64 [36.37, 132.84]; 0.01% ≤ 0 | −0.138 [−0.682, 0.198] | −0.005 [−0.008, 0.001] (3) | 0.004 [−0.008, 0.029] (3) | 0.236 [0.098, 0.388] (5†) | 0.162 [0.070, 0.259] (5†) | −0.002 [−0.022, 0.005] (3) |
| Count (ii) | 0.5 | Lead braking | 755 | 56.79 [17.14, 97.72]; 0.01% ≤ 0 | 0.433 [0.222, 0.895] | −0.003 [−0.008, 0.004] (3) | 0.001 [−0.049, 0.026] (3) | 0.348 [0.171, 0.790] (5) | −0.044 [−0.509, 0.138] (3) | −0.003 [−0.017, 0.008] (3) |
| Count (ii) | 0.5 | Lead stopped | 6,857 | 1.51 [0.00, 5.30]; 36.20% ≤ 0 | 0.780 [0.629, 0.931] | −0.016 [−0.020, −0.003] (1) | −0.016 [−0.023, −0.005] (1) | 0.737 [0.627, 0.853] (1) | 0.395 [0.238, 0.578] (1) | −0.326 [−0.513, −0.190] (1) |
| Count (ii) | 0.5 | Phase-weighted | 8,290 | 142.95 [58.43, 225.67]; 0.01% ≤ 0 | 0.099 [−0.221, 0.308] | −0.004 [−0.006, 0.000] (3) | 0.003 [−0.016, 0.021] (3) | 0.286 [0.140, 0.502] (5) | 0.083 [−0.062, 0.172] (3) | −0.006 [−0.025, 0.004] (3) |
| Count (ii) | 0.75 | All | 8,290 | 341.92 [151.75, 505.42] | 0.715 [0.653, 0.858] | 0.000 [−0.001, 0.001] (3) | 0.003 [−0.000, 0.007] (3) | 0.260 [0.176, 0.356] (5) | 0.151 [0.106, 0.207] (5†) | −0.005 [−0.016, 0.002] (3) |
| Count (ii) | 0.75 | Ego moving | 1,863 | 193.48 [96.03, 260.81] | 0.403 [0.282, 0.512] | −0.002 [−0.004, 0.002] (3) | 0.007 [−0.003, 0.017] (3) | 0.106 [0.051, 0.167] (5) | 0.165 [0.085, 0.241] (5†) | −0.006 [−0.021, 0.002] (3) |
| Count (ii) | 0.75 | Before onset | 678 | 114.42 [52.16, 167.14]; 0.01% ≤ 0 | 0.105 [−0.116, 0.286] | −0.001 [−0.005, 0.002] (3) | 0.005 [−0.003, 0.021] (3) | 0.040 [0.011, 0.076] (5†) | 0.116 [0.049, 0.199] (5†) | −0.005 [−0.022, 0.005] (3) |
| Count (ii) | 0.75 | Lead braking | 755 | 45.00 [6.18, 72.22]; 1.57% ≤ 0 | 0.505 [0.225, 2.056] | −0.006 [−0.025, 0.008] (3) | 0.014 [−0.050, 0.058] (3) | 0.266 [0.098, 1.237] (5) | 0.182 [−0.119, 0.533] (3) | −0.017 [−0.114, 0.004] (3) |
| Count (ii) | 0.75 | Lead stopped | 6,857 | 2.23 [0.11, 6.33]; 0.48% ≤ 0 | 0.811 [0.652, 0.982] | 0.000 [−0.032, 0.047] (1) | 0.042 [−0.024, 0.250] (1) | 0.788 [0.662, 1.000] (1) | 0.350 [−0.364, 0.647] (1) | −0.252 [−0.502, 0.065] (1) |
| Count (ii) | 0.75 | Phase-weighted | 8,290 | 161.66 [82.06, 214.24] | 0.226 [0.040, 0.375] | −0.003 [−0.006, 0.002] (3) | 0.008 [−0.006, 0.023] (3) | 0.113 [0.058, 0.180] (5) | 0.138 [0.052, 0.217] (5†) | −0.011 [−0.034, 0.001] (3) |
| Count (ii) | 1.0 | All | 8,290 | 390.38 [192.86, 556.32] | 0.751 [0.691, 0.911] | 0.001 [−0.002, 0.001] (3) | 0.005 [0.001, 0.011] (5†) | 0.330 [0.233, 0.468] (5) | 0.185 [0.141, 0.250] (5†) | −0.007 [−0.017, 0.001] (3) |
| Count (ii) | 1.0 | Ego moving | 1,863 | 203.39 [106.70, 270.40] | 0.480 [0.380, 0.599] | −0.001 [−0.005, 0.001] (3) | 0.008 [−0.002, 0.018] (3) | 0.144 [0.072, 0.230] (5) | 0.195 [0.121, 0.263] (5) | −0.005 [−0.021, 0.003] (3) |
| Count (ii) | 1.0 | Before onset | 678 | 114.57 [52.54, 167.05] | 0.109 [−0.110, 0.292] | −0.002 [−0.005, 0.002] (3) | 0.005 [−0.004, 0.021] (3) | 0.040 [0.012, 0.076] (5†) | 0.115 [0.047, 0.197] (5†) | −0.005 [−0.022, 0.005] (3) |
| Count (ii) | 1.0 | Lead braking | 755 | 47.26 [10.88, 72.49]; 0.95% ≤ 0 | 0.702 [0.333, 2.584] | −0.003 [−0.022, 0.007] (3) | 0.011 [−0.062, 0.049] (3) | 0.399 [0.151, 1.600] (5) | 0.221 [−0.052, 0.633] (3) | −0.010 [−0.078, 0.005] (3) |
| Count (ii) | 1.0 | Lead stopped | 6,857 | 6.23 [1.63, 12.86]; 0.02% ≤ 0 | 0.843 [0.722, 0.956] | −0.006 [−0.026, 0.027] (1) | 0.054 [−0.009, 0.207] (1) | 0.871 [0.728, 0.979] (1) | 0.494 [0.242, 0.768] (1) | −0.220 [−0.336, 0.007] (1) |
| Count (ii) | 1.0 | Phase-weighted | 8,290 | 168.05 [89.17, 221.58] | 0.303 [0.134, 0.451] | −0.002 [−0.006, 0.002] (3) | 0.008 [−0.006, 0.026] (3) | 0.172 [0.093, 0.273] (5) | 0.159 [0.081, 0.233] (5†) | −0.014 [−0.037, 0.001] (3) |
| Count (ii) | 1.25 | All | 8,290 | 670.08 [414.48, 787.09]; 0.07% ≤ 0 | 0.890 [0.760, 1.515] | 0.000 [−0.002, 0.001] (3) | 0.007 [0.002, 0.012] (5†) | 0.441 [0.318, 0.767] (5) | 0.165 [0.121, 0.281] (5†) | −0.004 [−0.013, −0.001] (2) |
| Count (ii) | 1.25 | Ego moving | 1,863 | 257.54 [75.73, 322.94]; 0.60% ≤ 0 | 0.802 [0.563, 2.361] | −0.001 [−0.009, 0.002] (3) | 0.004 [−0.009, 0.017] (3) | 0.353 [0.216, 1.006] (5) | 0.150 [0.037, 0.501] (5) | −0.004 [−0.025, 0.002] (3) |
| Count (ii) | 1.25 | Before onset | 678 | 186.28 [146.62, 207.56] | 0.256 [0.088, 0.375] | −0.002 [−0.006, 0.003] (3) | −0.000 [−0.005, 0.005] (3) | 0.099 [0.047, 0.163] (5†) | 0.028 [−0.015, 0.078] (3) | −0.001 [−0.016, 0.007] (3) |
| Count (ii) | 1.25 | Lead braking | 755 | 2.70 [−137.50, 74.49]; 46.32% ≤ 0 | 31.985 [1.001, 46.330] | −0.144 [−0.140, 0.014] (1) | −0.436 [−0.727, 0.096] (1) | 18.232 [0.533, 26.452] (1) | 0.956 [−1.701, 2.743] (1) | −0.112 [−0.191, 0.070] (1) |
| Count (ii) | 1.25 | Lead stopped | 6,857 | 12.60 [4.98, 22.78] | 0.856 [0.740, 0.954] | −0.007 [−0.029, 0.009] (3) | 0.117 [0.035, 0.214] (5) | 0.853 [0.738, 0.946] (4) | 0.564 [0.381, 0.742] (5) | −0.082 [−0.210, 0.003] (3) |
| Count (ii) | 1.25 | Phase-weighted | 8,290 | 201.58 [40.54, 275.39]; 1.04% ≤ 0 | 0.718 [0.486, 2.460] | −0.004 [−0.014, 0.002] (3) | 0.001 [−0.019, 0.026] (3) | 0.389 [0.238, 1.391] (5) | 0.073 [−0.043, 0.368] (3) | −0.008 [−0.049, 0.003] (3) |
| Count (ii) | 1.5 | All | 8,290 | 602.34 [218.52, 729.18]; 0.52% ≤ 0 | 1.040 [0.813, 2.789] | 0.001 [−0.001, 0.001] (3) | 0.009 [0.004, 0.022] (5†) | 0.408 [0.272, 1.097] (5) | 0.204 [0.145, 0.537] (5†) | −0.004 [−0.016, 0.000] (3) |
| Count (ii) | 1.5 | Ego moving | 1,863 | 184.73 [−44.22, 275.27]; 4.65% ≤ 0 | 1.321 [0.779, 8.308] | −0.001 [−0.010, 0.011] (1) | 0.013 [0.000, 0.073] (1) | 0.388 [0.186, 2.486] (1) | 0.346 [0.170, 2.311] (1) | 0.004 [−0.002, 0.045] (1) |
| Count (ii) | 1.5 | Before onset | 678 | 174.05 [120.86, 198.10] | 0.381 [0.271, 0.530] | −0.001 [−0.003, 0.005] (3) | 0.001 [−0.004, 0.005] (3) | 0.077 [0.037, 0.137] (5†) | 0.046 [0.007, 0.120] (5†) | 0.010 [0.003, 0.027] (5†) |
| Count (ii) | 1.5 | Lead braking | 755 | −37.11 [−187.88, 49.44]; 75.06% ≤ 0 | no room | no room (1) | no room (1) | no room (1) | no room (1) | no room (1) |
| Count (ii) | 1.5 | Lead stopped | 6,857 | 17.78 [8.30, 30.43] | 0.848 [0.722, 0.952] | 0.001 [−0.010, 0.009] (3) | 0.113 [0.055, 0.200] (5) | 0.855 [0.742, 0.950] (4) | 0.597 [0.425, 0.761] (5) | −0.044 [−0.119, 0.010] (3) |
| Count (ii) | 1.5 | Phase-weighted | 8,290 | 154.72 [−31.25, 243.64]; 4.46% ≤ 0 | 1.118 [0.665, 6.852] | −0.000 [−0.006, 0.023] (1) | 0.017 [0.002, 0.110] (1) | 0.468 [0.238, 3.040] (1) | 0.253 [0.110, 1.715] (1) | 0.008 [−0.002, 0.072] (1) |
| Count (ii) | 1.8 | All | 8,290 | 490.00 [235.07, 627.58]; 0.16% ≤ 0 | 1.078 [0.852, 2.264] | 0.001 [−0.001, 0.002] (3) | 0.014 [0.006, 0.028] (5†) | 0.483 [0.338, 0.991] (5) | 0.255 [0.181, 0.539] (5†) | −0.005 [−0.019, 0.000] (3) |
| Count (ii) | 1.8 | Ego moving | 1,863 | 79.90 [−120.18, 201.78]; 18.57% ≤ 0 | 2.726 [1.005, 31.739] | −0.001 [−0.047, 0.013] (1) | 0.026 [−0.007, 0.222] (1) | 0.766 [0.225, 9.001] (1) | 0.749 [0.235, 8.989] (1) | 0.003 [−0.058, 0.031] (1) |
| Count (ii) | 1.8 | Before onset | 678 | 102.45 [50.52, 144.17]; 0.01% ≤ 0 | 0.504 [0.328, 0.870] | −0.003 [−0.009, 0.005] (3) | −0.005 [−0.022, 0.003] (3) | 0.080 [0.022, 0.193] (5†) | −0.045 [−0.179, 0.005] (3) | 0.008 [−0.000, 0.021] (3) |
| Count (ii) | 1.8 | Lead braking | 755 | −59.57 [−188.14, 30.86]; 87.83% ≤ 0 | no room | no room (1) | no room (1) | no room (1) | no room (1) | no room (1) |
| Count (ii) | 1.8 | Lead stopped | 6,857 | 28.19 [17.06, 41.74] | 0.860 [0.741, 0.956] | 0.004 [−0.003, 0.009] (3) | 0.113 [0.058, 0.169] (5) | 0.896 [0.806, 0.964] (4) | 0.626 [0.469, 0.766] (5) | −0.031 [−0.076, 0.011] (3) |
| Count (ii) | 1.8 | Phase-weighted | 8,290 | 71.07 [−98.91, 192.42]; 18.31% ≤ 0 | 2.273 [0.821, 26.859] | −0.004 [−0.032, 0.033] (1) | 0.034 [−0.002, 0.390] (1) | 1.034 [0.328, 12.807] (1) | 0.471 [0.140, 5.266] (1) | −0.001 [−0.100, 0.045] (1) |

> **TABLE S11.** τ = 0.75 s, the reaction-and-stop scoring as scored: each source's difference from the class average, D, in decision-equivalents with its 95% interval, by population (each on its own frontier), with RR_E and the convex-hull RR₀ for all decisions. "CK3, F0 point replacing its own": the class average's zero-margin point replaces the prior's own instead of being prepended. Two programs.

| Arm | All | Ego moving | Before onset | Lead braking | Lead stopped | Phase-weighted | RR_E, all [95%] | Hull RR₀, all [95%] |
|---|---|---|---|---|---|---|---|---|
| N | 0.01 [−0.34, 0.28] | −0.15 [−0.39, 0.07] | 0.00 [0.00, 0.00] | −0.00 [−0.07, 0.08] | 0.00 [−0.06, 0.04] | −0.00 [−0.10, 0.08] | 0.000 [−0.007, 0.005] | −0.001 [−0.017, 0.015] |
| NA | 0.68 [−0.21, 1.87] | −0.25 [−0.80, 0.17] | 0.00 [0.00, 0.00] | −0.22 [−0.59, 0.02] | 0.09 [−0.04, 0.27] | −0.13 [−0.51, 0.13] | 0.012 [−0.004, 0.040] | 0.001 [−0.017, 0.040] |
| CK3 | 54.42 [18.98, 95.56] | 0.41 [−5.06, 5.23] | 0.00 [0.00, 0.00] | −1.61 [−5.90, 0.72] | 1.76 [0.11, 4.68] | 0.15 [−4.01, 3.94] | 0.977 [0.937, 1.018] | 0.956 [0.937, 0.970] |
| CK3, F0 point replacing its own | 47.25 [16.34, 84.52] | −0.89 [−6.46, 4.01] | 0.00 [0.00, 0.00] | −2.22 [−6.40, 0.16] | 1.16 [0.00, 3.58] | −1.05 [−5.00, 2.38] | 0.848 [0.738, 0.923] | 0.888 [0.810, 0.937] |
| AM | 33.17 [12.04, 57.29] | 3.09 [0.99, 5.64] | 0.00 [0.00, 0.00] | −0.97 [−2.14, −0.12] | 0.78 [−0.11, 2.37] | −0.19 [−1.27, 1.10] | 0.596 [0.497, 0.687] | 0.561 [0.458, 0.673] |
| Q | −1.88 [−5.61, 0.37] | −0.54 [−1.47, 0.13] | 0.00 [0.00, 0.00] | −0.07 [−0.28, 0.22] | −0.56 [−1.82, 0.04] | −0.63 [−1.89, 0.14] | −0.034 [−0.079, 0.012] | −0.018 [−0.077, 0.057] |
| E | 55.69 [19.76, 98.03] | 11.43 [4.09, 20.32] | 0.00 [0.00, 0.00] | 1.45 [0.32, 2.94] | 1.81 [0.08, 4.96] | 3.26 [0.70, 7.50] | 1.000 [1.000, 1.000] | 0.960 [0.927, 0.986] |
| O (= den₀) | 58.16 [20.41, 102.52] | 12.02 [4.23, 20.97] | 0.00 [0.00, 0.00] | 1.45 [0.32, 2.94] | 2.23 [0.11, 6.33] | 3.69 [0.74, 8.73] | 1.044 [1.012, 1.087] | 1.000 [1.000, 1.000] |

> **TABLE S12.** Graded oracles with 95% intervals: RR (the share of the 3 s oracle's room, as in Table II) under the 3 s scoring, and RR₀ under the reaction-and-stop scoring at τ = 0.75 s. Partial: the oracle's critical values on a random fraction p of the decisions, the class average's elsewhere. Noisy: the oracle's critical values divided by a log-normal factor exp(σZ) per decision. Two programs.

| Graded oracle | 3 s, all: RR | 3 s, ego moving: RR | 3 s, lead braking: RR | 3 s, phase-weighted: RR | R&S 0.75 s, all: RR₀ | R&S 0.75 s, ego moving: RR₀ |
|---|---|---|---|---|---|---|
| Partial, p = 0.25 | 0.269 [0.222, 0.305] | −0.109 [−0.227, −0.039] | −0.682 [−0.933, −0.486] | −0.383 [−0.542, −0.241] | 0.341 [0.279, 0.402] | −0.413 [−0.645, −0.229] |
| Partial, p = 0.5 | 0.536 [0.473, 0.582] | 0.051 [−0.120, 0.161] | −0.630 [−0.915, −0.383] | −0.266 [−0.448, −0.090] | 0.600 [0.517, 0.690] | −0.303 [−0.625, 0.047] |
| Partial, p = 0.75 | 0.778 [0.731, 0.811] | 0.440 [0.307, 0.526] | 0.046 [−0.187, 0.227] | 0.266 [0.119, 0.391] | 0.809 [0.741, 0.887] | 0.225 [−0.077, 0.649] |
| Noisy, σ = 0.5 | 0.969 [0.951, 0.977] | 0.779 [0.715, 0.814] | 0.341 [0.193, 0.452] | 0.555 [0.442, 0.646] | 0.953 [0.911, 0.984] | 0.933 [0.891, 0.989] |
| Noisy, σ = 1 | 0.922 [0.889, 0.941] | 0.452 [0.326, 0.525] | −0.381 [−0.656, −0.174] | 0.051 [−0.150, 0.216] | 0.930 [0.876, 0.972] | 0.680 [0.416, 0.893] |
| Noisy, σ = 2 | 0.820 [0.766, 0.854] | −0.022 [−0.240, 0.102] | −1.087 [−1.518, −0.768] | −0.487 [−0.787, −0.246] | 0.832 [0.742, 0.910] | −0.329 [−1.056, 0.256] |

> **TABLE S13.** (a) Caution counted at every decision's signed speed difference to the 3 s oracle's row, τ = 0.75 s: den₀, the 3 s oracle's RR₀, and RR₀ with branch for N, NA and CK3 (and for CK3 with the class average's zero-margin point replacing its own), with CK3's D in decision-equivalents. ‡ One program, recounted by an independent reviewer.

| Population | n | den₀, dec.-eq. [95%] | RR₀(E) [95%] | RR₀(N) [95%] (b) | RR₀(NA) [95%] (b) | RR₀(CK3) [95%] (b) | RR₀(CK3, F0 point replacing its own) [95%] (b) | D(CK3), dec.-eq. [95%] |
|---|---|---|---|---|---|---|---|---|
| All | 8,290 | 53.14 [19.05, 92.17] | 0.930 [0.883, 0.965] | −0.001 [−0.007, 0.005] (3) | 0.007 [−0.007, 0.035] (3) | 0.803 [0.723, 0.850] (4) | 0.680 [0.544, 0.775] (4) | 42.65 [15.38, 70.29] |
| Ego moving‡ | 1,863 | 13.58 [4.67, 24.53] | 0.674 [0.534, 0.809] | −0.013 [−0.021, 0.007] (3) | −0.033 [−0.059, 0.002] (3) | −0.902 [−1.465, −0.489] (2) | −0.998 [−1.604, −0.598] (2) | −12.25 [−26.58, −3.67] |
| Lead braking‡ | 755 | 9.29 [2.49, 16.32] | 0.300 [0.208, 0.484] | −0.000 [−0.016, 0.018] (1) | −0.037 [−0.090, −0.010] (1) | −2.360 [−4.038, −1.915] (1) | −2.492 [−4.210, −2.004] (1) | −21.92 [−44.51, −7.22] |
| Lead stopped‡ | 6,857 | 2.23 [0.11, 6.28]; 0.48% ≤ 0 | 0.786 [0.627, 0.961] | 0.004 [−0.032, 0.046] (1) | 0.042 [−0.028, 0.247] (1) | 0.706 [0.576, 0.940] (1) | 0.457 [−0.222, 0.710] (1) | 1.58 [0.07, 4.22] |
| Phase-weighted‡ | 8,290 | 11.52 [3.08, 20.83] | 0.395 [0.304, 0.570] | 0.001 [−0.014, 0.016] (3) | −0.022 [−0.060, 0.008] (3) | −1.766 [−3.269, −1.119] (2) | −1.920 [−3.460, −1.262] (2) | −20.34 [−42.08, −6.40] |

> *(b)* The stop deceleration at τ = 0.75 s, as scored; points only (the plan fixes no intervals here); the rows at 4, 5 and 7.6 m/s² are ‡.

| A (m/s²) | Population | den₀, dec.-eq. | RR₀(E) | RR₀(CK3) | RR₀(CK3, F0 point replacing its own) | RR₀(NA) |
|---|---|---|---|---|---|---|
| 4 | All | 122.73 | 0.951 | 0.951 | 0.862 | 0.013 |
| 4 | Phase-weighted | 14.81 | 0.961 | 0.630 | 0.511 | −0.018 |
| 5 | All | 78.28 | 0.955 | 0.944 | 0.835 | 0.013 |
| 5 | Phase-weighted | 6.36 | 0.931 | 0.350 | 0.131 | −0.062 |
| 6 | All | 58.16 | 0.957 | 0.936 | 0.812 | 0.012 |
| 6 | Phase-weighted | 3.69 | 0.885 | 0.042 | −0.286 | −0.035 |
| 7.6 | All | 30.86 | 0.951 | 0.917 | 0.768 | 0.009 |
| 7.6 | Phase-weighted | 2.19 | 0.823 | −0.111 | −0.460 | −0.014 |

> **TABLE S29.** (Table IV of the earlier draft; the scoring of record with clearance read on the 3 s window, and count (ii).) The reaction-and-stop scoring at τ = 0.75 s (stop at 6 m/s², jerk 12.65 m/s³, zero gap) against a perfect oracle for that scoring: the class average's avoidable wrong-go den₀ and each source's share of it, RR₀ [95%], with the branch of the wording fixed before the values (1 not evaluable; 2 below the class average; 3 not distinguishable from zero; 4 most; 5 distinguishable from zero; † not robust to the convex-hull frontier). RR_E: share of the 3 s oracle's advantage. Under count (ii) the perfect oracle itself costs 2.4 points of caution, so den₀ is not a room at every caution level. With caution counted at its signed value, the braking prediction's share turns negative with the ego moving and phase-weighted (Table S13). Two programs.

| Quantity | Reaction and stop, all | Ego moving | Phase-weighted | Count (ii), all | Count (ii), phase-weighted |
|---|---|---|---|---|---|
| Evaluated decisions | 8,290 | 1,863 | 8,290 | 8,290 | 8,290 |
| den₀: pp; decision-equivalents [95%] | 0.7016; 58.16 [20.41, 102.52] | 0.6452; 12.02 [4.23, 20.97] | 0.0445; 3.69 [0.74, 8.73] | 4.1244; 341.92 [151.75, 505.42] | 1.9500; 161.66 [82.06, 214.24] |
| Evaluable (den₀ ≥ 10 decision-equivalents) | yes | yes | no | yes | yes |
| RR₀(N) [95%] (branch) | 0.000 [−0.007, 0.005] (3) | −0.013 [−0.032, 0.006] (3) | −0.001 [−0.031, 0.036] (1) | 0.000 [−0.001, 0.001] (3) | −0.003 [−0.006, 0.002] (3) |
| RR_E(N); D(N): pp; dec.-eq. [95%] | 0.000; 0.0001; 0.01 [−0.34, 0.28] | −0.013; −0.0083; −0.15 [−0.39, 0.07] | −0.002; −0.0001; −0.00 [−0.10, 0.08] | 0.000; 0.0010; 0.08 [−0.42, 0.38] | −0.012; −0.0053; −0.44 [−1.03, 0.28] |
| RR₀(NA) [95%] (branch) | 0.012 [−0.004, 0.039] (3) | −0.021 [−0.057, 0.020] (3) | −0.035 [−0.129, 0.078] (1) | 0.003 [−0.000, 0.007] (3) | 0.008 [−0.006, 0.023] (3) |
| RR_E(NA); D(NA): pp; dec.-eq. [95%] | 0.012; 0.0082; 0.68 [−0.21, 1.87] | −0.022; −0.0136; −0.25 [−0.80, 0.17] | −0.040; −0.0016; −0.13 [−0.51, 0.13] | 0.005; 0.0137; 1.13 [−0.03, 2.42] | 0.035; 0.0152; 1.26 [−0.86, 3.74] |
| RR₀(CK3) [95%] (branch) | 0.936 [0.908, 0.958] (4) | 0.034 [−0.471, 0.377] (3) | 0.042 [−2.175, 0.705] (1) | 0.260 [0.176, 0.356] (5) | 0.113 [0.058, 0.180] (5) |
| RR_E(CK3); D(CK3): pp; dec.-eq. [95%] | 0.977; 0.6564; 54.42 [18.98, 95.56] | 0.036; 0.0222; 0.41 [−5.06, 5.23] | 0.047; 0.0019; 0.15 [−4.01, 3.94] | 0.364; 1.0736; 89.00 [34.65, 148.04] | 0.501; 0.2208; 18.30 [6.30, 31.46] |
| RR₀(AM) [95%] (branch) | 0.570 [0.472, 0.665] (5) | 0.257 [0.168, 0.339] (5) | −0.051 [−0.684, 0.216] (1) | 0.151 [0.106, 0.207] (5†) | 0.138 [0.052, 0.217] (5†) |
| RR_E(AM); D(AM): pp; dec.-eq. [95%] | 0.596; 0.4002; 33.17 [12.04, 57.29] | 0.271; 0.1661; 3.09 [0.99, 5.64] | −0.058; −0.0023; −0.19 [−1.27, 1.10] | 0.212; 0.6247; 51.79 [21.05, 84.44] | 0.610; 0.2687; 22.28 [5.61, 38.53] |
| RR₀(Q) [95%] (branch) | −0.032 [−0.075, 0.012] (3) | −0.045 [−0.095, 0.021] (3) | −0.171 [−0.304, 0.109] (1) | −0.005 [−0.016, 0.002] (3) | −0.011 [−0.034, 0.001] (3) |
| RR_E(Q); D(Q): pp; dec.-eq. [95%] | −0.034; −0.0226; −1.88 [−5.61, 0.37] | −0.047; −0.0288; −0.54 [−1.47, 0.13] | −0.194; −0.0076; −0.63 [−1.89, 0.14] | −0.007; −0.0220; −1.83 [−5.86, 0.51] | −0.051; −0.0224; −1.86 [−5.06, 0.17] |
| RR₀(E) [95%] | 0.957 [0.920, 0.988] | 0.951 [0.940, 1.000] | 0.885 [0.777, 0.996] | 0.715 [0.653, 0.858] | 0.226 [0.040, 0.375] |
| D(E): pp; dec.-eq. [95%] | 0.6717; 55.69 [19.76, 98.03] | 0.6137; 11.43 [4.09, 20.32] | 0.0394; 3.26 [0.70, 7.50] | 2.9480; 244.39 [106.12, 388.58] | 0.4404; 36.51 [4.74, 71.53] |
| RR_E(O) [95%] | 1.044 [1.012, 1.087] | 1.051 [1.000, 1.064] | 1.130 [1.004, 1.287] | 1.399 [1.165, 1.531] | 4.427 [2.666, 16.518] |

> **TABLE S14.** The reliability check by look-ahead t and phase of the lead's motion (35 evaluation runs): the spread of the tracker's deviation σ_N and of its ratio to the class average's; Spearman's ρ between deviation and absolute error for the tracker (N), the class average (F0, reference) and the NIS-inflated covariance (NA, secondary), with 95% run-bootstrap intervals; the reference ρ\* for N (a correlation above ρ\* means that the error depends on what drives the deviation more steeply than calibration implies); RMS z for N and F0; the mean error e. At t > 0 the deviation is the planner's propagated deviation, without process noise. Two programs; the spread columns are one program's points.

| t (s) | Phase | n | σ_N (m): 5th / 50th / 95th | σ_N/σ_F0: 5th / 50th / 95th | ρ_N [95%] | ρ_F0 [95%] | ρ_NA [95%] | ρ\*_N | RMS z_N [95%] | RMS z_F0 [95%] | Mean e (m) [95%] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Before onset | 678 | 0.400 / 0.452 / 0.545 | 1.020 / 1.035 / 1.054 | 0.274 [0.200, 0.355] | 0.266 [0.200, 0.344] | 0.257 [0.169, 0.348] | 0.117 | 0.581 [0.491, 0.669] | 0.602 [0.510, 0.694] | 0.187 [0.129, 0.244] |
| 0 | Lead braking | 755 | 0.400 / 0.452 / 0.545 | 1.020 / 1.035 / 1.054 | 0.453 [0.392, 0.508] | 0.458 [0.396, 0.512] | 0.535 [0.478, 0.579] | 0.122 | 0.980 [0.851, 1.103] | 1.022 [0.888, 1.150] | −0.288 [−0.352, −0.216] |
| 0 | Lead stopped | 6,857 | 0.400 / 0.452 / 0.545 | 1.020 / 1.035 / 1.054 | 0.039 [−0.014, 0.098] | 0.033 [0.012, 0.053] | 0.028 [−0.025, 0.088] | 0.123 | 0.685 [0.635, 0.732] | 0.708 [0.655, 0.757] | 0.275 [0.253, 0.298] |
| 0 | Pooled | 8,290 | 0.400 / 0.452 / 0.545 | 1.020 / 1.035 / 1.054 | 0.111 [0.068, 0.160] | 0.111 [0.088, 0.135] | 0.113 [0.069, 0.161] | 0.122 | 0.710 [0.663, 0.754] | 0.734 [0.686, 0.781] | 0.217 [0.193, 0.241] |
| 1 | Before onset | 678 | 0.933 / 1.077 / 1.225 | 1.086 / 1.091 / 1.094 | 0.111 [0.052, 0.173] | 0.104 [0.045, 0.164] | 0.100 [0.041, 0.162] | 0.100 | 0.698 [0.622, 0.773] | 0.761 [0.678, 0.843] | 0.122 [−0.061, 0.301] |
| 1 | Lead braking | 755 | 0.934 / 1.078 / 1.225 | 1.086 / 1.091 / 1.094 | 0.396 [0.330, 0.469] | 0.386 [0.318, 0.459] | 0.420 [0.353, 0.481] | 0.105 | 3.174 [2.866, 3.503] | 3.462 [3.126, 3.821] | −3.209 [−3.543, −2.908] |
| 1 | Lead stopped | 6,857 | 0.934 / 1.078 / 1.225 | 1.086 / 1.091 / 1.094 | 0.039 [−0.015, 0.106] | 0.027 [0.000, 0.051] | 0.049 [−0.004, 0.114] | 0.107 | 0.390 [0.365, 0.413] | 0.425 [0.398, 0.450] | 0.242 [0.219, 0.265] |
| 1 | Pooled | 8,290 | 0.934 / 1.078 / 1.225 | 1.086 / 1.091 / 1.094 | 0.013 [−0.032, 0.072] | −0.010 [−0.031, 0.012] | 0.041 [−0.005, 0.097] | 0.107 | 1.041 [0.924, 1.156] | 1.135 [1.007, 1.261] | −0.082 [−0.161, −0.010] |
| 2 | Before onset | 678 | 1.676 / 1.828 / 1.982 | 1.099 / 1.100 / 1.101 | 0.080 [0.037, 0.126] | 0.076 [0.038, 0.114] | 0.102 [0.049, 0.161] | 0.060 | 1.691 [1.515, 1.872] | 1.860 [1.666, 2.059] | −1.768 [−2.225, −1.349] |
| 2 | Lead braking | 755 | 1.676 / 1.829 / 1.982 | 1.099 / 1.100 / 1.101 | 0.318 [0.274, 0.376] | 0.314 [0.268, 0.373] | 0.242 [0.150, 0.318] | 0.068 | 4.768 [4.386, 5.170] | 5.245 [4.825, 5.688] | −8.320 [−9.024, −7.662] |
| 2 | Lead stopped | 6,857 | 1.676 / 1.829 / 1.982 | 1.099 / 1.100 / 1.101 | 0.047 [−0.010, 0.125] | 0.016 [−0.015, 0.047] | 0.061 [0.005, 0.137] | 0.070 | 0.327 [0.303, 0.350] | 0.360 [0.333, 0.385] | 0.211 [0.186, 0.235] |
| 2 | Pooled | 8,290 | 1.676 / 1.829 / 1.982 | 1.099 / 1.100 / 1.101 | −0.008 [−0.057, 0.064] | −0.037 [−0.061, −0.010] | 0.031 [−0.020, 0.100] | 0.069 | 1.547 [1.360, 1.732] | 1.702 [1.496, 1.905] | −0.728 [−0.933, −0.546] |
| 3 | Before onset | 678 | 2.442 / 2.598 / 2.753 | 1.102 / 1.103 / 1.103 | 0.096 [0.048, 0.144] | 0.091 [0.045, 0.136] | 0.128 [0.068, 0.197] | 0.043 | 3.077 [2.722, 3.439] | 3.393 [3.001, 3.792] | −6.335 [−7.346, −5.429] |
| 3 | Lead braking | 755 | 2.440 / 2.598 / 2.753 | 1.097 / 1.103 / 1.103 | 0.323 [0.272, 0.379] | 0.311 [0.261, 0.369] | 0.178 [0.070, 0.276] | 0.064 | 5.892 [5.470, 6.294] | 6.490 [6.025, 6.934] | −13.575 [−14.784, −12.404] |
| 3 | Lead stopped | 6,857 | 2.433 / 2.598 / 2.754 | 1.089 / 1.103 / 1.103 | 0.094 [−0.021, 0.240] | 0.061 [−0.026, 0.190] | 0.110 [−0.005, 0.255] | 0.062 | 0.307 [0.281, 0.330] | 0.336 [0.308, 0.362] | 0.025 [−0.059, 0.104] |
| 3 | Pooled | 8,290 | 2.438 / 2.598 / 2.754 | 1.091 / 1.103 / 1.103 | 0.049 [−0.047, 0.178] | 0.018 [−0.051, 0.128] | 0.089 [−0.006, 0.215] | 0.061 | 2.004 [1.747, 2.257] | 2.207 [1.925, 2.486] | −1.734 [−2.148, −1.373] |

> **TABLE S15.** Reliability tables: the decisions of each phase and look-ahead split into quintiles of the tracker's deviation σ_N, with the smallest, mean and largest σ_N and the root-mean-square error in each. Points; one program.

| t (s) | Phase | Quintile | n | σ_N min (m) | σ_N mean (m) | σ_N max (m) | RMS e (m) |
|---|---|---|---|---|---|---|---|
| 0 | Before onset | 1 | 136 | 0.400 | 0.400 | 0.400 | 0.194 |
| 0 | Before onset | 2 | 136 | 0.400 | 0.417 | 0.419 | 0.232 |
| 0 | Before onset | 3 | 136 | 0.419 | 0.447 | 0.452 | 0.262 |
| 0 | Before onset | 4 | 135 | 0.452 | 0.488 | 0.495 | 0.304 |
| 0 | Before onset | 5 | 135 | 0.495 | 0.540 | 0.545 | 0.346 |
| 0 | Lead braking | 1 | 151 | 0.400 | 0.400 | 0.419 | 0.217 |
| 0 | Lead braking | 2 | 151 | 0.419 | 0.419 | 0.419 | 0.314 |
| 0 | Lead braking | 3 | 151 | 0.419 | 0.451 | 0.452 | 0.422 |
| 0 | Lead braking | 4 | 151 | 0.452 | 0.494 | 0.495 | 0.555 |
| 0 | Lead braking | 5 | 151 | 0.495 | 0.545 | 0.545 | 0.735 |
| 0 | Lead stopped | 1 | 1,372 | 0.291 | 0.398 | 0.400 | 0.303 |
| 0 | Lead stopped | 2 | 1,372 | 0.400 | 0.418 | 0.419 | 0.305 |
| 0 | Lead stopped | 3 | 1,371 | 0.419 | 0.451 | 0.452 | 0.308 |
| 0 | Lead stopped | 4 | 1,371 | 0.452 | 0.494 | 0.495 | 0.317 |
| 0 | Lead stopped | 5 | 1,371 | 0.495 | 0.546 | 0.888 | 0.328 |
| 1 | Before onset | 1 | 136 | 0.933 | 0.934 | 0.934 | 0.692 |
| 1 | Before onset | 2 | 136 | 0.934 | 0.997 | 1.005 | 0.689 |
| 1 | Before onset | 3 | 136 | 1.005 | 1.067 | 1.078 | 0.721 |
| 1 | Before onset | 4 | 135 | 1.078 | 1.140 | 1.151 | 0.788 |
| 1 | Before onset | 5 | 135 | 1.151 | 1.217 | 1.225 | 0.840 |
| 1 | Lead braking | 1 | 151 | 0.933 | 0.934 | 1.005 | 2.671 |
| 1 | Lead braking | 2 | 151 | 1.005 | 1.005 | 1.005 | 3.050 |
| 1 | Lead braking | 3 | 151 | 1.005 | 1.076 | 1.078 | 3.410 |
| 1 | Lead braking | 4 | 151 | 1.078 | 1.149 | 1.151 | 3.793 |
| 1 | Lead braking | 5 | 151 | 1.151 | 1.224 | 1.225 | 4.245 |
| 1 | Lead stopped | 1 | 1,372 | 0.611 | 0.927 | 0.934 | 0.324 |
| 1 | Lead stopped | 2 | 1,372 | 0.934 | 1.002 | 1.005 | 0.347 |
| 1 | Lead stopped | 3 | 1,371 | 1.005 | 1.075 | 1.078 | 0.405 |
| 1 | Lead stopped | 4 | 1,371 | 1.078 | 1.149 | 1.151 | 0.486 |
| 1 | Lead stopped | 5 | 1,371 | 1.151 | 1.224 | 1.405 | 0.545 |
| 2 | Before onset | 1 | 136 | 1.674 | 1.676 | 1.676 | 2.922 |
| 2 | Before onset | 2 | 136 | 1.676 | 1.744 | 1.752 | 2.968 |
| 2 | Before onset | 3 | 136 | 1.752 | 1.817 | 1.829 | 3.112 |
| 2 | Before onset | 4 | 135 | 1.829 | 1.893 | 1.905 | 3.083 |
| 2 | Before onset | 5 | 135 | 1.905 | 1.974 | 1.982 | 3.281 |
| 2 | Lead braking | 1 | 151 | 1.670 | 1.676 | 1.749 | 7.498 |
| 2 | Lead braking | 2 | 151 | 1.749 | 1.752 | 1.752 | 8.109 |
| 2 | Lead braking | 3 | 151 | 1.752 | 1.827 | 1.829 | 8.741 |
| 2 | Lead braking | 4 | 151 | 1.829 | 1.903 | 1.905 | 9.351 |
| 2 | Lead braking | 5 | 151 | 1.905 | 1.981 | 1.982 | 9.948 |
| 2 | Lead stopped | 1 | 1,372 | 1.049 | 1.659 | 1.676 | 0.377 |
| 2 | Lead stopped | 2 | 1,372 | 1.676 | 1.747 | 1.752 | 0.434 |
| 2 | Lead stopped | 3 | 1,371 | 1.752 | 1.825 | 1.829 | 0.573 |
| 2 | Lead stopped | 4 | 1,371 | 1.829 | 1.903 | 1.905 | 0.730 |
| 2 | Lead stopped | 5 | 1,371 | 1.905 | 1.981 | 2.093 | 0.835 |
| 3 | Before onset | 1 | 136 | 2.436 | 2.443 | 2.444 | 7.631 |
| 3 | Before onset | 2 | 136 | 2.444 | 2.512 | 2.521 | 7.664 |
| 3 | Before onset | 3 | 136 | 2.521 | 2.586 | 2.599 | 8.061 |
| 3 | Before onset | 4 | 135 | 2.599 | 2.663 | 2.676 | 7.989 |
| 3 | Before onset | 5 | 135 | 2.676 | 2.745 | 2.754 | 8.472 |
| 3 | Lead braking | 1 | 151 | 0.625 | 2.366 | 2.444 | 13.004 |
| 3 | Lead braking | 2 | 151 | 2.444 | 2.511 | 2.521 | 14.559 |
| 3 | Lead braking | 3 | 151 | 2.521 | 2.588 | 2.599 | 15.478 |
| 3 | Lead braking | 4 | 151 | 2.599 | 2.669 | 2.676 | 16.247 |
| 3 | Lead braking | 5 | 151 | 2.676 | 2.749 | 2.754 | 17.012 |
| 3 | Lead stopped | 1 | 1,372 | 0.695 | 2.363 | 2.444 | 0.465 |
| 3 | Lead stopped | 2 | 1,372 | 2.444 | 2.505 | 2.521 | 0.496 |
| 3 | Lead stopped | 3 | 1,371 | 2.521 | 2.586 | 2.599 | 0.813 |
| 3 | Lead stopped | 4 | 1,371 | 2.599 | 2.666 | 2.676 | 0.993 |
| 3 | Lead stopped | 5 | 1,371 | 2.676 | 2.747 | 2.832 | 1.064 |

> **TABLE S16.** Validity of the run-bootstrap intervals (3 s commitment, all evaluated decisions, step frontier). Point; the 95% percentile and basic intervals of the draw of record (20,000 run resamples); their coverage estimated by a double bootstrap (2000 outer × 1000 inner resamples; the full-sample value plays the truth; Monte Carlo standard error about 0.005); the smallest nominal level at which the percentile interval reaches 95% estimated coverage, and the percentile interval of the draw of record at that level (the calibrated interval).

| Statistic | Point | 95% percentile interval | Estimated coverage | 95% basic interval | Estimated coverage | Calibrated nominal level | Calibrated interval |
|---|---|---|---|---|---|---|---|
| $R$ (pp) | 5.56 | [4.50, 6.60] | 0.934 | [4.51, 6.61] | 0.921 | 0.964 | [4.43, 6.68] |
| RR(N) | 0.0012 | [−0.0011, 0.0012] | 0.528 | [0.0012, 0.0035] | 0.523 | 0.996 | [−0.0016, 0.0017] |
| RR(NA) | 0.017 | [0.007, 0.025] | 0.922 | [0.008, 0.026] | 0.873 | 0.972 | [0.006, 0.027] |
| RR(AM) | 0.376 | [0.316, 0.425] | 0.933 | [0.326, 0.436] | 0.951 | 0.962 | [0.312, 0.428] |
| RR(CK3) | 0.831 | [0.753, 0.903] | 0.932 | [0.760, 0.910] | 0.956 | 0.97 | [0.745, 0.912] |
| RR(Q) | −0.0018 | [−0.0065, 0.0012] | 0.925 | [−0.0048, 0.0029] | 0.910 | 0.968 | [−0.0069, 0.0015] |
| RR₀(CK3) | 0.771 | [0.695, 0.835] | 0.948 | [0.706, 0.846] | 0.945 | 0.952 | [0.694, 0.835] |
| RR(NA) − RR(N) | 0.015 | [0.007, 0.025] | 0.935 | [0.006, 0.024] | 0.893 | 0.962 | [0.007, 0.026] |

> **TABLE S17.** Sensitivities of the intervals of Table S16: run resampling stratified by the recording setting α (10, 12, 13 runs; 20,000 resamples); the 30 full-length runs alone (the five short runs left out; point and percentile interval); subsampling 15, 20 and 25 of the 35 runs without replacement (5,000 subsamples each; interval from the root √m(θ*−θ) with the finite-population factor); and the range over leaving one run out.

| Statistic | Stratified by α | 30 full-length runs | Subsampling, m = 15 | Subsampling, m = 20 | Subsampling, m = 25 | Leave one run out (min, max) |
|---|---|---|---|---|---|---|
| $R$ (pp) | [4.56, 6.54] | 5.46 [4.33, 6.57] | [4.52, 6.64] | [4.51, 6.64] | [4.50, 6.65] | 5.36, 5.80 |
| RR(N) | [−0.0010, 0.0012] | −0.0001 [−0.0011, 0.0012] | [0.0011, 0.0033] | [0.0013, 0.0038] | [0.0014, 0.0047] | −0.0009, 0.0012 |
| RR(NA) | [0.007, 0.025] | 0.016 [0.007, 0.027] | [0.007, 0.027] | [0.008, 0.027] | [0.008, 0.027] | 0.014, 0.018 |
| RR(AM) | [0.321, 0.421] | 0.388 [0.328, 0.443] | [0.325, 0.441] | [0.323, 0.438] | [0.324, 0.432] | 0.363, 0.386 |
| RR(CK3) | [0.759, 0.901] | 0.852 [0.775, 0.925] | [0.758, 0.915] | [0.761, 0.913] | [0.765, 0.915] | 0.809, 0.842 |
| RR(Q) | [−0.0065, 0.0012] | −0.0033 [−0.0070, 0.0013] | [−0.0052, 0.0027] | [−0.0051, 0.0027] | [−0.0051, 0.0030] | −0.0038, −0.0016 |
| RR₀(CK3) | [0.700, 0.832] | 0.789 [0.714, 0.853] | [0.703, 0.850] | [0.705, 0.846] | [0.704, 0.845] | 0.757, 0.781 |
| RR(NA) − RR(N) | [0.007, 0.025] | 0.016 [0.007, 0.027] | [0.005, 0.024] | [0.006, 0.025] | [0.006, 0.025] | 0.014, 0.017 |

> **TABLE S18.** Plans judged until their stop ends. For each reaction-and-stop setting: the decision–row pairs that the scoring of record judges safe although their stop ends after the 3 s window (the pairs of count (ii)); those among them whose recording ends before the stop (count (i)); how many of the former are unsafe when the same trajectory is followed against the logged truth until the stop ends; and the unsafe pairs as scored and in the estimate. 140,930 pairs of evaluated decisions and rows; 24,902 are unsafe under the 3 s commitment.

| τ (s) | $A$ (m/s²) | Safe as scored, stop after 3 s | Recording ends before the stop | Unsafe when judged to the stop | Unsafe pairs, as scored | Unsafe pairs, estimate |
|---|---|---|---|---|---|---|
| 0.5 | 6 | 2,897 | 94 | 8 | 1,417 | 1,425 |
| 0.75 | 6 | 5,356 | 153 | 28 | 3,334 | 3,362 |
| 1 | 6 | 5,301 | 230 | 126 | 5,631 | 5,757 |
| 1.25 | 6 | 7,048 | 296 | 215 | 8,530 | 8,745 |
| 1.5 | 6 | 8,583 | 372 | 374 | 12,714 | 13,088 |
| 1.8 | 6 | 9,900 | 487 | 651 | 15,824 | 16,475 |
| 0.75 | 4 | 8,905 | 773 | 440 | 4,373 | 4,813 |
| 0.75 | 5 | 6,781 | 365 | 161 | 3,740 | 3,901 |
| 0.75 | 7.6 | 2,431 | 37 | 0 | 2,802 | 2,802 |

> **TABLE S19.** The reaction-and-stop scoring with plans judged until their stop ends (the estimate), beside the scoring of record. The 3 s oracle's advantage relative to its 3 s value: as scored (the 3 s window's flags kept), the estimate with its 95% interval, the estimate with the pairs whose recording ends before the stop counted unsafe, and count (ii) of record (every pair whose stop ends after 3 s counted unsafe). den₀: the class average's avoidable wrong-go against the perfect oracle of the estimate, in percentage points and relative to its 3 s value. 35 evaluation runs, all evaluated decisions, step frontier, zero standstill gap. Points only at 4, 5 and 7.6 m/s².

| τ (s) | $A$ (m/s²) | As scored | Estimate [95%] | Recording-end pairs unsafe | Count (ii) | den₀, estimate (pp) [95%] | den₀ relative to 3 s [95%] |
|---|---|---|---|---|---|---|---|
| 0.5 | 6 | 0.019 | 0.019 [0.000, 0.052] | 0.029 | 0.447 | 0.11 [0.00, 0.33] | 0.019 [0.000, 0.052] |
| 0.75 | 6 | 0.121 | 0.122 [0.052, 0.188] | 0.144 | 0.531 | 0.71 [0.26, 1.23] | 0.118 [0.050, 0.182] |
| 1 | 6 | 0.234 | 0.241 [0.136, 0.331] | 0.275 | 0.636 | 1.41 [0.68, 2.19] | 0.235 [0.133, 0.322] |
| 1.25 | 6 | 0.364 | 0.384 [0.259, 0.488] | 0.426 | 1.295 | 2.27 [1.29, 3.26] | 0.378 [0.255, 0.478] |
| 1.5 | 6 | 0.490 | 0.537 [0.405, 0.643] | 0.586 | 1.360 | 3.20 [2.04, 4.36] | 0.533 [0.401, 0.638] |
| 1.8 | 6 | 0.644 | 0.732 [0.601, 0.829] | 0.776 | 1.146 | 4.37 [3.03, 5.64] | 0.729 [0.598, 0.825] |
| 0.75 | 4 | 0.253 | 0.293 | n/a | n/a | 1.72 | 0.286 |
| 0.75 | 5 | 0.162 | 0.179 | n/a | n/a | 1.04 | 0.173 |
| 0.75 | 7.6 | 0.064 | 0.064 | n/a | n/a | 0.37 | 0.062 |

> **TABLE S20a.** τ = 0.75 s, stop at 6 m/s², zero gap, the estimate (plans judged until their stop ends): den₀ in decision-equivalents and each source's share RR₀ of it with its 95% interval and the branch of Section S8.1 without the hull clause (1 not evaluable; 2 below the class average; 3 not distinguishable from zero; 4 most; 5 distinguishable from zero), by population, each on its own frontier.

| Population | n | den₀, dec.-eq. [95%] | RR₀(E) | RR₀(N) | RR₀(NA) | RR₀(CK3) | RR₀(AM) | RR₀(Q) |
|---|---|---|---|---|---|---|---|---|
| All | 8,290 | 58.8 [20.9, 103.2] | 0.958 [0.920, 0.988] | 0.000 [−0.006, 0.005] (3) | 0.012 [−0.004, 0.039] (3) | 0.936 [0.908, 0.959] (4) | 0.570 [0.472, 0.664] (5) | −0.031 [−0.074, 0.013] (3) |
| Ego moving | 1,863 | 12.2 [4.3, 21.1] | 0.951 [0.940, 1.000] | −0.013 [−0.031, 0.006] (3) | −0.021 [−0.057, 0.020] (3) | 0.038 [−0.460, 0.381] (3) | 0.257 [0.167, 0.337] (5) | −0.044 [−0.093, 0.022] (3) |
| Lead braking | 755 | 1.5 [0.3, 3.0] | 1.000 [1.000, 1.000] | −0.003 [−0.056, 0.073] (1) | −0.153 [−0.365, 0.025] (1) | −1.109 [−4.636, 0.510] (1) | −0.677 [−1.589, −0.187] (1) | −0.048 [−0.205, 0.216] (1) |
| Lead stopped | 6,857 | 2.2 [0.1, 6.3] | 0.811 [0.652, 0.982] | 0.000 [−0.032, 0.047] (1) | 0.042 [−0.024, 0.250] (1) | 0.788 [0.662, 1.000] (1) | 0.350 [−0.364, 0.647] (1) | −0.252 [−0.502, 0.065] (1) |
| Phase-weighted | 8,290 | 3.7 [0.8, 8.7] | 0.886 [0.778, 0.996] | −0.001 [−0.029, 0.038] (1) | −0.035 [−0.130, 0.078] (1) | 0.038 [−2.164, 0.704] (1) | −0.057 [−0.693, 0.208] (1) | −0.171 [−0.303, 0.111] (1) |

> **TABLE S20b.** τ = 0.75 s, stop at 6 m/s², zero gap, the estimate with the pairs whose recording ends before the stop counted unsafe: den₀ in decision-equivalents and each source's share RR₀ of it with its 95% interval and the branch of Section S8.1 without the hull clause (1 not evaluable; 2 below the class average; 3 not distinguishable from zero; 4 most; 5 distinguishable from zero), by population, each on its own frontier.

| Population | n | den₀, dec.-eq. [95%] | RR₀(E) | RR₀(N) | RR₀(NA) | RR₀(CK3) | RR₀(AM) | RR₀(Q) |
|---|---|---|---|---|---|---|---|---|
| All | 8,290 | 69.5 [31.0, 113.2] | 0.956 [0.917, 0.986] | 0.000 [−0.005, 0.004] (3) | 0.012 [−0.002, 0.033] (3) | 0.829 [0.623, 0.946] (4) | 0.492 [0.341, 0.613] (5) | −0.026 [−0.063, 0.011] (3) |
| Ego moving | 1,863 | 19.3 [8.4, 30.2] | 0.958 [0.948, 1.014] | −0.008 [−0.022, 0.005] (3) | −0.009 [−0.040, 0.016] (3) | 0.087 [−0.255, 0.324] (3) | 0.178 [0.084, 0.285] (5) | −0.026 [−0.070, 0.013] (3) |
| Lead braking | 755 | 6.7 [0.9, 14.8] | 1.041 [0.980, 1.213] | 0.002 [−0.024, 0.032] (1) | −0.023 [−0.228, 0.018] (1) | −0.083 [−2.396, 0.323] (1) | −0.282 [−1.065, −0.087] (1) | −0.004 [−0.080, 0.092] (1) |
| Lead stopped | 6,857 | 2.2 [0.1, 6.3] | 0.811 [0.652, 0.982] | 0.000 [−0.032, 0.047] (1) | 0.042 [−0.024, 0.250] (1) | 0.788 [0.662, 1.000] (1) | 0.350 [−0.364, 0.647] (1) | −0.252 [−0.502, 0.065] (1) |
| Phase-weighted | 8,290 | 9.4 [1.8, 18.6] | 0.984 [0.851, 1.103] | 0.001 [−0.014, 0.018] (1) | −0.007 [−0.073, 0.031] (1) | 0.137 [−0.793, 0.524] (1) | −0.104 [−0.427, 0.088] (1) | −0.069 [−0.216, 0.030] (1) |

> **TABLE S20c.** As Table S20a, with caution counted at every decision's signed speed difference to the 3 s oracle's row (compare Table S13).

| Population | n | den₀, dec.-eq. [95%] | RR₀(E) | RR₀(N) | RR₀(NA) | RR₀(CK3) | RR₀(AM) |
|---|---|---|---|---|---|---|---|
| All | 8,290 | 53.7 [19.4, 92.8] | 0.930 [0.883, 0.965] | −0.001 [−0.006, 0.006] (3) | 0.007 [−0.007, 0.035] (3) | 0.803 [0.724, 0.851] (4) | 0.532 [0.437, 0.625] (5) |
| Ego moving | 1,863 | 13.7 [4.8, 24.7] | 0.675 [0.535, 0.809] | −0.013 [−0.020, 0.007] (3) | −0.033 [−0.059, 0.003] (3) | −0.895 [−1.437, −0.484] (2) | 0.070 [−0.026, 0.177] (3) |
| Lead braking | 755 | 9.4 [2.5, 16.4] | 0.301 [0.210, 0.484] | 0.001 [−0.015, 0.018] (1) | −0.037 [−0.089, −0.010] (1) | −2.350 [−3.972, −1.913] (1) | −0.120 [−0.309, 0.002] (1) |
| Lead stopped | 6,857 | 2.2 [0.1, 6.3] | 0.786 [0.627, 0.961] | 0.004 [−0.032, 0.046] (1) | 0.042 [−0.028, 0.247] (1) | 0.706 [0.576, 0.940] (1) | 0.314 [−0.514, 0.600] (1) |
| Phase-weighted | 8,290 | 11.6 [3.1, 20.9] | 0.395 [0.305, 0.570] | 0.001 [−0.013, 0.016] (3) | −0.022 [−0.060, 0.008] (3) | −1.763 [−3.231, −1.122] (2) | −0.036 [−0.223, 0.100] (3) |

> **TABLE S20d.** The estimate at the other delays (stop at 6 m/s², zero gap): den₀ in decision-equivalents and the shares of the tracker covariance, the braking prediction and the acceleration margin, pooled and phase-weighted.

| τ (s) | den₀ all, dec.-eq. [95%] | RR₀(N) all | RR₀(CK3) all | RR₀(AM) all | den₀ phase-weighted, dec.-eq. [95%] | RR₀(N) phase-weighted | RR₀(CK3) phase-weighted | RR₀(AM) phase-weighted |
|---|---|---|---|---|---|---|---|---|
| 0.5 | 9.3 [0.0, 27.2] | −0.003 [−0.010, 0.021] (1) | 0.879 [0.840, 0.945] (1) | 0.573 [0.449, 0.715] (1) | 1.6 [0.0, 5.5] | −0.016 [−0.020, 0.000] (1) | 0.338 [−19.000, 0.683] (1) | 0.369 [0.000, 0.609] (1) |
| 0.75 | 58.8 [20.9, 103.2] | 0.000 [−0.006, 0.005] (3) | 0.936 [0.908, 0.959] (4) | 0.570 [0.472, 0.664] (5) | 3.7 [0.8, 8.7] | −0.001 [−0.029, 0.038] (1) | 0.038 [−2.164, 0.704] (1) | −0.057 [−0.693, 0.208] (1) |
| 1 | 116.8 [55.0, 184.6] | 0.001 [−0.005, 0.004] (3) | 0.943 [0.919, 0.962] (4) | 0.536 [0.458, 0.618] (5) | 13.6 [4.7, 24.8] | −0.015 [−0.042, 0.021] (3) | 0.569 [−0.031, 0.870] (3) | 0.027 [−0.328, 0.261] (3) |
| 1.25 | 187.9 [105.5, 274.5] | 0.001 [−0.003, 0.002] (3) | 0.943 [0.918, 0.962] (4) | 0.506 [0.431, 0.581] (5) | 31.9 [15.3, 51.7] | −0.004 [−0.014, 0.009] (3) | 0.718 [0.415, 0.894] (5) | 0.083 [−0.140, 0.265] (3) |
| 1.5 | 265.1 [166.0, 366.2] | 0.001 [−0.002, 0.001] (3) | 0.933 [0.905, 0.954] (4) | 0.452 [0.384, 0.516] (5) | 61.4 [34.8, 91.7] | −0.001 [−0.006, 0.007] (3) | 0.786 [0.590, 0.908] (4) | 0.104 [−0.066, 0.250] (3) |
| 1.8 | 362.4 [248.4, 473.0] | 0.001 [−0.001, 0.001] (3) | 0.845 [0.791, 0.887] (4) | 0.386 [0.321, 0.443] (5) | 109.9 [76.2, 141.7] | −0.001 [−0.005, 0.005] (3) | 0.760 [0.628, 0.865] (4) | 0.137 [−0.005, 0.269] (3) |

> **TABLE S21.** Caution counted at its signed value under the 3 s commitment, beside the values of record. Signed: caution is averaged over every evaluated decision (each has a truly safe row), at its signed speed difference to the first truly safe row; of record: over truly safe selections only. Room $R$ and share recovered RR with 95% run-bootstrap percentile intervals; step frontier; each population on its own frontier. The last three columns give the partial oracles (the oracle's margin on a random 25%, 50% and 75% of decisions, the class average's elsewhere) under signed caution.

| Population | Caution | $R$ (pp) | RR(N) | RR(NA) | RR(AM) | RR(CK3) | RR(Q) | Partial oracle 25% | 50% | 75% |
|---|---|---|---|---|---|---|---|---|---|---|
| All | of record | 5.56 [4.50, 6.60] | 0.0012 [−0.0011, 0.0012] | 0.017 [0.007, 0.025] | 0.376 [0.316, 0.425] | 0.831 [0.753, 0.903] | −0.0018 [−0.0065, 0.0012] | 0.27 [0.22, 0.31] | 0.54 [0.47, 0.58] | 0.78 [0.73, 0.81] |
| All | signed | 4.86 [4.05, 5.61] | −0.0002 [−0.0011, 0.0012] | 0.016 [0.008, 0.026] | 0.378 [0.322, 0.430] | 0.817 [0.735, 0.891] | −0.0030 [−0.0073, 0.0010] | 0.27 [0.23, 0.31] | 0.54 [0.48, 0.59] | 0.78 [0.74, 0.82] |
| Ego moving | of record | 10.16 [7.96, 12.39] | −0.0001 [−0.0058, 0.0016] | 0.016 [0.002, 0.028] | 0.293 [0.207, 0.350] | 0.472 [0.353, 0.570] | 0.0018 [−0.0067, 0.0050] | −0.11 [−0.23, −0.04] | 0.05 [−0.12, 0.16] | 0.44 [0.31, 0.53] |
| Ego moving | signed | 6.32 [4.83, 7.42] | −0.0031 [−0.0070, 0.0023] | 0.020 [0.005, 0.035] | 0.346 [0.249, 0.425] | 0.299 [0.127, 0.432] | −0.0014 [−0.0135, 0.0042] | −0.12 [−0.27, −0.04] | 0.01 [−0.22, 0.14] | 0.39 [0.21, 0.49] |
| Lead braking | of record | 15.59 [11.45, 20.04] | −0.0025 [−0.0048, 0.0052] | −0.006 [−0.031, 0.023] | −0.044 [−0.193, 0.062] | 0.606 [0.468, 0.711] | −0.0003 [−0.0076, 0.0106] | −0.68 [−0.93, −0.49] | −0.63 [−0.91, −0.38] | 0.05 [−0.19, 0.23] |
| Lead braking | signed | 5.64 [3.68, 7.57] | 0.0000 [−0.0118, 0.0102] | 0.007 [−0.027, 0.046] | 0.061 [−0.156, 0.237] | 0.347 [0.012, 0.549] | −0.0161 [−0.0430, 0.0046] | −0.71 [−1.19, −0.44] | −0.87 [−1.52, −0.50] | −0.23 [−0.70, 0.05] |
| Lead stopped | of record | 0.82 [0.66, 0.99] | 0.0019 [−0.0045, 0.0043] | 0.079 [0.034, 0.123] | 0.702 [0.636, 0.769] | 0.993 [0.914, 1.108] | −0.0143 [−0.0339, 0.0049] | 0.28 [0.21, 0.35] | 0.54 [0.48, 0.61] | 0.78 [0.73, 0.83] |
| Lead stopped | signed | 0.79 [0.64, 0.95] | 0.0007 [−0.0047, 0.0044] | 0.079 [0.034, 0.125] | 0.703 [0.630, 0.765] | 0.982 [0.903, 1.094] | −0.0146 [−0.0352, 0.0042] | 0.28 [0.21, 0.35] | 0.54 [0.48, 0.61] | 0.78 [0.73, 0.83] |
| Phase-weighted | of record | 2.13 [1.70, 2.56] | −0.0010 [−0.0035, 0.0038] | 0.021 [0.002, 0.045] | 0.192 [0.093, 0.275] | 0.711 [0.614, 0.793] | −0.0048 [−0.0129, 0.0059] | −0.38 [−0.54, −0.24] | −0.27 [−0.45, −0.09] | 0.27 [0.12, 0.39] |
| Phase-weighted | signed | 1.20 [1.03, 1.35] | 0.0004 [−0.0056, 0.0051] | 0.046 [0.019, 0.076] | 0.405 [0.310, 0.487] | 0.666 [0.519, 0.783] | −0.0148 [−0.0340, 0.0008] | −0.18 [−0.33, −0.07] | −0.11 [−0.31, 0.04] | 0.31 [0.15, 0.43] |

> **TABLE S12b.** The partial oracles over 50 further random draws (3 s commitment, step frontier, points): for each share of decisions that take the oracle's margin, the value of the draw of record (Table S12) and the mean and range over the draws.

| Population | 25%: of record; mean [min, max] | 50%: of record; mean [min, max] | 75%: of record; mean [min, max] |
|---|---|---|---|
| All | 0.27; 0.28 [0.26, 0.31] | 0.54; 0.54 [0.50, 0.58] | 0.78; 0.78 [0.75, 0.81] |
| Ego moving | −0.11; −0.08 [−0.14, −0.01] | 0.05; 0.09 [0.00, 0.19] | 0.44; 0.46 [0.34, 0.55] |
| Lead braking | −0.68; −0.64 [−0.76, −0.52] | −0.63; −0.54 [−0.72, −0.40] | 0.05; 0.05 [−0.16, 0.20] |
| Lead stopped | 0.28; 0.28 [0.23, 0.33] | 0.54; 0.55 [0.50, 0.60] | 0.78; 0.79 [0.76, 0.82] |
| Phase-weighted | −0.38; −0.35 [−0.45, −0.26] | −0.27; −0.20 [−0.33, −0.09] | 0.27; 0.28 [0.14, 0.38] |

> **TABLE S22.** The length of the after-stop segment. Each population keeps every evaluated decision before the lead's stop and those taken less than $T$ after it; 3 s commitment, step frontier, each population on its own frontier and levels; 95% run-bootstrap percentile intervals. In the 30 full-length runs the after-stop segment lasts 18.9–24.9 s.

| $T$ (s) | Decisions | $R$ (pp) [95%] | RR(N) | RR(NA) | RR(AM) | RR(CK3) | RR₀(CK3) | D(CK3), dec.-eq. |
|---|---|---|---|---|---|---|---|---|
| 0 (none) | 1,433 | 8.58 [6.16, 11.08] | −0.0002 [−0.0046, 0.0036] | 0.018 [0.000, 0.041] | 0.434 [0.300, 0.523] | 0.289 [0.170, 0.390] | 0.287 [0.169, 0.387] | 35.5 |
| 1 | 1,733 | 10.00 [7.73, 12.26] | 0.0004 [−0.0039, 0.0021] | 0.016 [0.002, 0.031] | 0.282 [0.186, 0.350] | 0.412 [0.299, 0.519] | 0.406 [0.294, 0.510] | 71.4 |
| 2 | 2,033 | 10.65 [8.48, 12.83] | −0.0041 [−0.0054, 0.0013] | 0.014 [0.003, 0.027] | 0.305 [0.234, 0.356] | 0.537 [0.440, 0.621] | 0.522 [0.429, 0.606] | 116.2 |
| 5 | 2,933 | 10.15 [8.31, 11.87] | −0.0009 [−0.0030, 0.0011] | 0.015 [0.006, 0.025] | 0.341 [0.285, 0.383] | 0.684 [0.605, 0.755] | 0.656 [0.581, 0.724] | 203.7 |
| 10 | 4,433 | 8.39 [6.95, 9.74] | 0.0003 [−0.0018, 0.0010] | 0.015 [0.007, 0.025] | 0.359 [0.303, 0.404] | 0.766 [0.692, 0.837] | 0.721 [0.650, 0.787] | 285.1 |
| 20 | 7,422 | 6.00 [4.92, 7.01] | −0.0002 [−0.0012, 0.0012] | 0.015 [0.007, 0.025] | 0.370 [0.311, 0.420] | 0.818 [0.744, 0.893] | 0.761 [0.687, 0.826] | 364.4 |
| all | 8,290 | 5.56 [4.50, 6.60] | 0.0012 [−0.0011, 0.0012] | 0.017 [0.007, 0.025] | 0.376 [0.316, 0.425] | 0.831 [0.753, 0.903] | 0.771 [0.695, 0.835] | 383.0 |

> **TABLE S23.** One margin scale per phase of the lead's motion (before the onset, lead braking, lead stopped), 3 s commitment, all evaluated decisions, pooled caution levels of record. (a) The pooled room of record and its parts; (b) each source against a class average that also chooses one scale per phase. Intervals: 400 run resamples of the draw of record.

| Quantity | Percentage points [95%] | Decision-equivalents [95%] | Share of the pooled room [95%] |
|---|---|---|---|
| The pooled room of record, one scale: class average minus oracle | 5.56 [4.49, 6.56] | 460.7 [365.6, 552.5] | 1 |
| What the class average gains from one scale per phase | 4.96 [4.01, 5.92] | 411.3 [319.9, 497.2] | 0.893 [0.836, 0.968] |
| The room that remains when both choose a scale per phase | 0.95 [0.76, 1.08] | 78.4 [59.7, 92.5] | 0.170 [0.138, 0.203] |
| What the oracle gains from one scale per phase | 0.35 [0.09, 0.72] | 29.0 [7.2, 63.2] | n/a |
| The class average with per-phase scales against the perfect oracle | 1.04 [0.81, 1.20] | 85.8 [66.1, 100.8] | n/a |

| Source | RR of record (one scale) | Share of the remaining room, per-phase scales [95%] | Against the perfect oracle, per-phase scales | Gain over the class average: one scale → per-phase scales (dec.-eq.) [95%] |
|---|---|---|---|---|
| N | 0.0012 | −0.0013 [−0.0041, 0.0068] | −0.0012 [−0.0037, 0.0061] | 0.6 → −0.1 [−0.3, 0.5] |
| NA | 0.017 | 0.041 [0.019, 0.065] | 0.038 [0.018, 0.060] | 7.7 → 3.2 [1.4, 5.4] |
| AM | 0.376 | 0.388 [0.270, 0.478] | 0.354 [0.239, 0.446] | 173.1 → 30.4 [19.9, 39.6] |
| CK3 | 0.831 | 0.633 [0.490, 0.763] | 0.579 [0.454, 0.668] | 383.0 → 49.7 [34.2, 61.1] |
| Q | −0.0018 | −0.0054 [−0.0193, 0.0095] | −0.0049 [−0.0184, 0.0087] | −0.8 → −0.4 [−1.5, 0.7] |

> **TABLE S24.** A standstill gap of 2 m: a decision–row pair is unsafe when its true clearance is at most 2 m, for the wrong go and for the caution's truly safe rows alike. den₀ against the perfect oracle for the 2 m requirement, and each source's share RR₀ [95%]; RR₀(E) is the 3 s oracle, which is built for contact and is not an oracle for this requirement. Step frontier; each population on its own frontier; for the 3 s commitment the lead-braking and lead-stopped phases are also given. Points only at 4, 5 and 7.6 m/s².

| Scoring | Population | Decisions without a row keeping 2 m | den₀ (pp) | den₀, dec.-eq. [95%] | RR₀(E) | RR₀(N) | RR₀(NA) | RR₀(CK3) | RR₀(AM) |
|---|---|---|---|---|---|---|---|---|---|
| 3 s commitment | All | 633 | 7.38 | 612.0 [499.9, 719.1] | −1.532 [−2.909, −0.548] | −0.0087 [−0.0163, 0.0024] | 0.010 [−0.002, 0.029] | 0.307 [−0.004, 0.515] | 0.341 [0.270, 0.398] |
| 3 s commitment | Ego moving |  | 13.10 | 244.0 [190.7, 294.8] | 0.064 [−0.380, 0.364] | 0.0000 [−0.0055, 0.0045] | 0.023 [0.011, 0.038] | 0.129 [−0.057, 0.298] | 0.297 [0.209, 0.364] |
| 3 s commitment | Lead braking |  | 20.81 | 157.1 [115.7, 198.2] | 0.880 [0.837, 0.919] | 0.0076 [0.0010, 0.0132] | 0.011 [−0.016, 0.038] | 0.554 [0.415, 0.669] | −0.111 [−0.284, 0.003] |
| 3 s commitment | Lead stopped |  | 1.57 | 107.7 [71.3, 162.1] | −1.464 [−2.894, −0.537] | −0.0535 [−0.1025, 0.0102] | 0.049 [−0.037, 0.180] | 0.661 [0.455, 0.857] | 0.258 [−0.117, 0.575] |
| 3 s commitment | Phase-weighted |  | 3.28 | 272.2 [211.9, 340.7] | −0.046 [−0.566, 0.321] | −0.0171 [−0.0393, 0.0088] | 0.025 [−0.008, 0.071] | 0.571 [0.468, 0.668] | 0.034 [−0.128, 0.148] |
| Stop 0.75 s, 6 m/s² | All | 631 | 1.12 | 93.1 [38.2, 154.0] | −0.087 [−2.182, 0.871] | −0.0006 [−0.0107, 0.0050] | 0.022 [−0.003, 0.061] | 0.571 [−0.285, 0.854] | 0.801 [0.739, 0.870] |
| Stop 0.75 s, 6 m/s² | Ego moving |  | 1.08 | 20.1 [7.6, 35.0] | −1.619 [−7.306, 0.182] | −0.0217 [−0.0547, 0.0055] | −0.009 [−0.044, 0.039] | −0.974 [−2.846, −0.227] | 0.407 [0.255, 0.502] |
| Stop 0.75 s, 6 m/s² | Phase-weighted |  | 0.14 | 11.8 [2.9, 21.4] | −0.292 [−3.369, 0.713] | −0.0198 [−0.0659, 0.0131] | 0.086 [−0.165, 0.232] | 0.549 [−0.230, 0.926] | 0.232 [−0.628, 0.585] |
| Stop 1.8 s, 6 m/s² | All | 633 | 4.85 | 402.4 [309.4, 491.4] | 0.523 [0.039, 0.893] | −0.0030 [−0.0058, 0.0016] | 0.022 [0.011, 0.039] | 0.700 [0.502, 0.826] | 0.506 [0.444, 0.569] |
| Stop 1.8 s, 6 m/s² | Ego moving |  | 7.80 | 145.4 [107.4, 183.4] | 0.344 [−0.105, 0.650] | −0.0043 [−0.0103, 0.0017] | 0.021 [0.006, 0.040] | 0.206 [−0.042, 0.418] | 0.364 [0.265, 0.441] |
| Stop 1.8 s, 6 m/s² | Phase-weighted |  | 1.60 | 132.6 [94.8, 175.6] | 0.717 [0.553, 0.873] | −0.0118 [−0.0168, 0.0054] | 0.031 [0.009, 0.073] | 0.751 [0.615, 0.849] | 0.150 [0.015, 0.274] |
| Stop 0.75 s, 4 m/s² | All | 642 | 1.96 | 162.1 | 0.367 | 0.0014 | 0.045 | 0.720 | 0.726 |
| Stop 0.75 s, 4 m/s² | Ego moving |  | 2.31 | 43.0 | −0.283 | −0.0079 | 0.033 | −0.178 | 0.432 |
| Stop 0.75 s, 4 m/s² | Phase-weighted |  | 0.38 | 31.6 | 0.496 | 0.0016 | 0.102 | 0.759 | 0.265 |
| Stop 0.75 s, 5 m/s² | All | 633 | 1.54 | 127.3 | 0.204 | 0.0005 | 0.028 | 0.669 | 0.767 |
| Stop 0.75 s, 5 m/s² | Ego moving |  | 1.63 | 30.5 | −0.737 | −0.0131 | 0.015 | −0.454 | 0.424 |
| Stop 0.75 s, 5 m/s² | Phase-weighted |  | 0.21 | 17.2 | 0.104 | −0.0058 | 0.057 | 0.642 | 0.148 |
| Stop 0.75 s, 7.6 m/s² | All | 629 | 0.84 | 69.3 | −0.460 | −0.0020 | 0.020 | 0.449 | 0.837 |
| Stop 0.75 s, 7.6 m/s² | Ego moving |  | 0.74 | 13.7 | −2.839 | −0.0326 | −0.025 | −1.634 | 0.400 |
| Stop 0.75 s, 7.6 m/s² | Phase-weighted |  | 0.12 | 9.6 | −0.583 | −0.0201 | 0.120 | 0.515 | 0.420 |

> **TABLE S24b.** As Table S24 at τ = 0.75 s and 6 m/s², with plans judged until their stop ends (the estimate of Table S19) and the 2 m gap applied to the wrong go and to the caution's truly safe rows alike. 631 evaluated decisions have no row that keeps 2 m until its stop ends.

| Population | den₀ (pp) | den₀, dec.-eq. [95%] | RR₀(E) | RR₀(N) | RR₀(NA) | RR₀(CK3) | RR₀(AM) |
|---|---|---|---|---|---|---|---|
| All | 1.14 | 94.7 [39.1, 156.2] | −0.070 [−2.138, 0.873] | −0.0008 [−0.0111, 0.0048] | 0.021 [−0.004, 0.059] | 0.576 [−0.260, 0.856] | 0.801 [0.738, 0.870] |
| Ego moving | 1.10 | 20.4 [7.8, 35.3] | −1.580 [−7.144, 0.196] | −0.0219 [−0.0548, 0.0051] | −0.009 [−0.045, 0.038] | −0.956 [−2.768, −0.216] | 0.407 [0.255, 0.501] |
| Phase-weighted | 0.14 | 11.9 [3.0, 21.5] | −0.287 [−3.325, 0.714] | −0.0193 [−0.0656, 0.0131] | 0.086 [−0.168, 0.230] | 0.547 [−0.231, 0.927] | 0.225 [−0.642, 0.574] |

> **TABLE S25.** The braking prediction at other decelerations. (a) The 35 evaluation runs, 3 s commitment: share of the room RR [95%] by population, and the zero-margin point; computed in the revision, the 3 m/s² row being the value of record. (b) The 20 tuning runs (of record, 13 November 2026), on which 3 m/s² was chosen: pooled RR [95%]; the eighth value tried there, 0.5 m/s², gave 0.085 [0.026, 0.160] and was not run on the evaluation runs.

| Deceleration (m/s²) | All | Ego moving | Lead braking | Lead stopped | Phase-weighted | Zero-margin caution (%) | Zero-margin wrong go (%) | Tuning runs, all |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.276 [0.214, 0.354] | 0.129 [0.094, 0.175] | 0.029 [0.019, 0.044] | 0.795 [0.708, 0.899] | 0.273 [0.220, 0.348] | 1.13 | 8.17 | 0.201 [0.055, 0.380] |
| 2 | 0.565 [0.474, 0.667] | 0.283 [0.208, 0.361] | 0.280 [0.237, 0.338] | 0.953 [0.868, 1.062] | 0.485 [0.433, 0.561] | 1.41 | 6.67 | 0.350 [0.001, 0.697] |
| 3 | 0.831 [0.753, 0.903] | 0.472 [0.353, 0.570] | 0.606 [0.468, 0.711] | 0.993 [0.914, 1.108] | 0.711 [0.614, 0.793] | 1.72 | 4.84 | 0.377 [−0.204, 0.840] |
| 4 | 0.930 [0.869, 0.995] | 0.386 [0.229, 0.501] | 0.531 [0.313, 0.697] | 1.010 [0.932, 1.133] | 0.652 [0.489, 0.783] | 2.27 | 2.76 | 0.274 [−0.464, 0.831] |
| 5 | 0.929 [0.868, 1.001] | 0.182 [−0.068, 0.366] | 0.304 [−0.044, 0.578] | 1.019 [0.941, 1.145] | 0.490 [0.220, 0.699] | 2.86 | 2.00 | 0.119 [−0.757, 0.744] |
| 6 | 0.917 [0.840, 0.993] | 0.022 [−0.324, 0.252] | 0.100 [−0.343, 0.468] | 1.023 [0.945, 1.148] | 0.345 [0.004, 0.623] | 3.31 | 1.59 | −0.055 [−1.016, 0.662] |
| 7 | 0.898 [0.813, 0.980] | −0.127 [−0.537, 0.148] | −0.070 [−0.610, 0.345] | 1.025 [0.946, 1.151] | 0.223 [−0.190, 0.537] | 3.67 | 1.39 | −0.237 [−1.307, 0.536] |

> **TABLE S26.** The margin-ratio check of Fig. 2(b) by scenario family: on every evaluated decision row with a finite positive critical scale under both the tracker covariance and the class average, the tracker's margin over the class average's, $1/\sqrt{g^{\ast}_N/g^{\ast}_{F0}}$. Runs, rows, the median ratio and the share of rows within 5% of that median. Stored arrays of all runs of the project (tuning runs of all six families; evaluation runs where they exist).

| Scenario family | Runs | Decision rows | Median ratio | Rows within 5% of the median (%) | Tuning runs alone: median; within 5% (%) |
|---|---|---|---|---|---|
| Lead braking | 55 | 152,264 | 1.103 | 99.26 | 1.103; 99.57 |
| Stopped vehicle | 55 | 121,685 | 1.103 | 98.73 | 1.103; 98.28 |
| Cut-in | 20 | 90,227 | 1.102 | 99.86 | 1.102; 99.86 |
| Benign driving | 20 | 40,120 | 1.093 | 60.45 | 1.093; 60.45 |
| Pedestrian crossing | 51 | 157,972 | 0.883 | 8.51 | 0.868; 8.42 |
| Vehicle crossing | 22 | 42,122 | 0.915 | 4.09 | 0.923; 4.92 |

> **TABLE S27.** The age of the lead's track. Evaluated decisions of the 35 evaluation runs by track age, and the margin ratio on the decision rows of all 55 lead-braking runs by track age (rows; share more than 5% from the family median 1.103; median ratio).

| Track age (s) | Evaluated decisions (35 runs) | Decision rows (55 runs) | Rows more than 5% from the median | Median ratio |
|---|---|---|---|---|
| [0, 0.5) | 5 | 80 | 0 | 1.137 |
| [0.5, 1) | 5 | 84 | 84 | 1.682 |
| [1, 2) | 0 | 0 | 0 | n/a |
| [2, 4) | 0 | 0 | 0 | n/a |
| ≥ 4 | 8,280 | 152,100 | 1,043 | 1.103 |

> **TABLE S30.** The grid placebo and the gridless frontier (3 s commitment, step frontier). Grid: the 202 swept scales of record. P: the class average with its critical scales divided by 1.1029², which selects at every scale as the class average does at a scale 1.1029² larger and so carries no information beyond it. RR(N) − RR(P): the tracker covariance against that placebo. Gridless: every margin scale in [0, 10³] at which a selection changes. Grid columns: the draw of record (20,000 run resamples); gridless intervals: its first 2,000 resamples; 95% percentile intervals, basic intervals in parentheses for the pooled tracker covariance. D: frontier distance in decision-equivalents (positive: below the class average).

| Population | Decisions | Grid: RR(N) | Grid: RR(P) | Grid: RR(N) − RR(P) | Grid: D(N) − D(P) | Gridless: RR(N) | Gridless: D(N) |
|---|---|---|---|---|---|---|---|
| All | 8,290 | 0.0012 [−0.0011, 0.0012] (basic [0.0012, 0.0035]) | 0.0015 [−0.0007, 0.0015] | −0.0003 [−0.0009, 0.0001] | −0.12 [−0.43, 0.04] | −0.0004 [−0.0008, 0.0001] (basic [−0.0009, −0.0001]) | −0.19 [−0.34, 0.02] |
| Ego moving | 1,863 | −0.0001 [−0.0058, 0.0016] | 0.0022 [−0.0029, 0.0023] | −0.0023 [−0.0050, 0.0006] | −0.44 [−0.93, 0.11] | −0.0023 | −0.43 |
| Before onset | 678 | 0.0051 [−0.029, 0.021] | 0.0051 [−0.030, 0.020] | 0.0000 [−0.0020, 0.0065] | 0.00 [0.00, 0.02] | 0.0017 | 0.00 |
| Lead braking | 755 | −0.0025 [−0.0048, 0.0052] | −0.0014 [−0.0047, 0.0053] | −0.0010 [−0.0016, 0.0015] | −0.12 [−0.19, 0.18] | 0.0002 | 0.02 |
| Lead stopped | 6,857 | 0.0019 [−0.0045, 0.0043] | 0.0028 [−0.0031, 0.0054] | −0.0010 [−0.0033, −0.0001] | −0.05 [−0.18, 0.00] | −0.0009 | −0.05 |

> **TABLE S30b.** Other sources on the gridless frontier (3 s commitment, all evaluated decisions; first 2,000 resamples of the draw of record), beside the grid values of record.

| Quantity | Grid (of record) | Gridless |
|---|---|---|
| Room $R$ (pp) | 5.56 | 5.51 [4.45, 6.54] |
| RR(NA), NIS-inflated | 0.017 | 0.015 [0.0069, 0.024] |
| RR(AM), acceleration margin | 0.376 | 0.382 [0.324, 0.434] |
| RR(CK3), braking prediction | 0.831 | 0.837 [0.756, 0.909] |
| RR(Q), planner allowance | −0.0018 | −0.0024 [−0.0059, 0.0010] |
| RR(P), placebo | 0.0015 | 0.0000 [0.0000, 0.0000] |

> **TABLE S30c.** Grid jitter: the class average with its critical scales divided by 10^(0.025 u), a fraction u of one grid step, scored as a source (3 s commitment, all evaluated decisions, points). Such a source carries no information beyond the class average.

| u | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.45 | 0.50 |
|---|---|---|---|---|---|---|---|---|---|---|
| RR | 0.0002 | 0.0005 | 0.0006 | 0.0010 | 0.0010 | 0.0010 | 0.0012 | 0.0015 | 0.0017 | 0.0011 |
| u | 0.55 | 0.60 | 0.65 | 0.70 | 0.75 | 0.80 | 0.85 | 0.90 | 0.95 | 1.00 |
| RR | 0.0015 | 0.0017 | 0.0011 | 0.0014 | 0.0013 | 0.0011 | 0.0009 | 0.0006 | 0.0000 | 0.0000 |

> **TABLE S31.** Monte Carlo error of the calibrated levels of Table S16 (3 s commitment, all evaluated decisions, step frontier, grid). Calibrated level: the smallest nominal level at which the percentile interval covers the full-sample value in at least 95% of the 2,000 outer samples. Inner seed 20261121 repeats Table S16; 20261126 repeats the double bootstrap with new inner resamples. Monte Carlo spread: 2,000 resamples of the outer samples (2.5%, 50% and 97.5% points; standard deviation).

| Statistic | Calibrated level, inner seed 20261121 | Spread [2.5%, 50%, 97.5%]; SD | Calibrated level, inner seed 20261126 | Spread [2.5%, 50%, 97.5%]; SD |
|---|---|---|---|---|
| Room $R$ | 0.9640 | [0.9560, 0.9640, 0.9700]; 0.0043 | 0.9640 | [0.9580, 0.9640, 0.9720]; 0.0044 |
| RR(N) | 0.9960 | [0.9960, 0.9960, 0.9980]; 0.0005 | 0.9960 | [0.9960, 0.9960, 0.9960]; 0.0002 |

> **TABLE S31b.** Subsampling with an estimated rate (Bertail, Politis and Romano [S1]): m = 10, 15, 20, 25 of the 35 runs without replacement, 2,000 subsamples each. β: the rate estimated from the interquartile range of the subsample values against m. Intervals at m = 20 with the finite-population factor, the same with β = 1/2 beside them, and both in decision-equivalents (converted at the full-sample room). Amendment 09 also named D(N) in decision-equivalents; that statistic is a total that grows with the number of runs in a subsample, so its subsampling root is not centred, and it is not reported (a deviation).

| Statistic | β estimated | Interval, estimated β | Interval, β = 1/2 | Decision-equivalents, estimated β | Decision-equivalents, β = 1/2 |
|---|---|---|---|---|---|
| RR(N), grid | 0.33 | [0.0013, 0.0040] | [0.0013, 0.0038] | [0.60, 1.86] | [0.59, 1.74] |
| RR(N), gridless | 0.69 | [−0.0009, −0.0002] | [−0.0010, −0.0002] | [−0.42, −0.10] | [−0.44, −0.09] |

> **TABLE S31c.** The bound of Section V-A: every 95% interval of the tracker covariance's frontier distance from the class average, in decision-equivalents of the 8,290 evaluated decisions (intervals of RR(N) converted at the full-sample room of 460.7 decision-equivalents). The bound is the largest absolute end, rounded up to one decimal.

| Interval | Decision-equivalents |
|---|---|
| Table S16: percentile | [−0.50, 0.55] |
| Table S16: basic | [0.57, 1.62] |
| Table S16: calibrated (99.6%) | [−0.74, 0.76] |
| Table S17: stratified by recording setting | [−0.48, 0.55] |
| Table S17: five short runs left out | [−0.51, 0.56] |
| Table S17: subsampling m = 15 | [0.52, 1.51] |
| Table S17: subsampling m = 20 | [0.60, 1.76] |
| Table S17: subsampling m = 25 | [0.63, 2.16] |
| Table S30: grid, D(N) percentile | [−0.51, 0.54] |
| Table S30: gridless, D(N) percentile | [−0.34, 0.02] |
| Table S31b: grid, estimated rate | [0.60, 1.86] |
| Table S31b: grid, rate 1/2 | [0.59, 1.74] |
| Table S31b: gridless, estimated rate | [−0.42, −0.10] |
| Table S31b: gridless, rate 1/2 | [−0.44, −0.09] |
| **Largest absolute end** | **2.16** (Table S17: subsampling m = 25) |

> **TABLE S32.** One class-average margin scale per phase of the lead's motion, in sample and out of sample (3 s commitment, all evaluated decisions; shares of the room of record, 5.56 points). In sample: the frontier over all scale triples (Table S23). Held out: per caution level, the triple (or the single scale) with the lowest wrong-go on the training runs, applied to the left-out runs (a level at which some fold has no qualifying choice gives no point); like for like: against a single scale chosen the same way; against the single-scale frontier of record. Five-fold: 5-fold cross-validation on the full sample; interval from 200 resamples of the draw of record, each cross-validated over its own runs. Estimated phase: from the lead track's own speed and acceleration estimate (stopped at most 0.5 m/s; braking above it with an acceleration estimate at most the threshold).

| Phase labels | In sample | Held out, like for like (leave one run out) | Held out, like for like (five-fold) | Held out against the single scale of record (leave one run out) | Agreement with the truth phase |
|---|---|---|---|---|---|
| Logged truth | 0.893 | 0.903 | 0.885 [0.81, 1.00] | 0.868 | — |
| Tracker estimate, threshold −1.0 m/s² | 0.984 | 0.999 | — | 0.964 | 95.6% |
| Tracker estimate, threshold −0.5 m/s² | 0.980 | 0.996 | — | 0.960 | 96.1% |
| Tracker estimate, threshold −2.0 m/s² | 0.968 | 0.980 | — | 0.944 | 94.2% |

> **TABLE S33.** Where the room and the sources' gains lie (3 s commitment, step frontier, grid): the frontier difference against the class average split exactly into per-decision contributions (at each caution level, the frontier points' wrong-go flags), in decision-equivalents, by time since the lead's stop. "All": the pooled population; "Lead stopped": decisions after the stop, on their own frontier. Decisions: the number in each bin.

| Population | Source | Total | before stop | 0-1 s | 1-2 s | 2-5 s | 5-10 s | >=10 s |
|---|---|---|---|---|---|---|---|---|
| All | Decisions | 8,290 | 1,433 | 300 | 300 | 900 | 1,500 | 3,857 |
| All | E, oracle (the room) | 460.7 | 419.1 | 41.7 | −0.14 | 0.00 | 0.00 | 0.00 |
| All | CK3, braking prediction | 383.0 | 345.9 | 37.4 | −0.27 | 0.00 | 0.00 | 0.00 |
| All | AM, acceleration margin | 173.1 | 143.2 | 30.0 | −0.10 | 0.00 | 0.00 | 0.00 |
| All | N, tracker covariance | 0.56 | 0.42 | 0.14 | 0.00 | 0.00 | 0.00 | 0.00 |
| Lead stopped | Decisions | 6,857 | 0 | 300 | 300 | 900 | 1,500 | 3,857 |
| Lead stopped | E, oracle (the room) | 56.3 | 0.00 | 56.1 | 0.15 | 0.00 | 0.00 | 0.00 |
| Lead stopped | CK3, braking prediction | 55.9 | 0.00 | 55.9 | 0.00 | 0.00 | 0.00 | 0.00 |
| Lead stopped | AM, acceleration margin | 39.5 | 0.00 | 39.7 | −0.16 | 0.00 | 0.00 | 0.00 |
| Lead stopped | N, tracker covariance | 0.10 | 0.00 | 0.10 | 0.00 | 0.00 | 0.00 | 0.00 |

> **TABLE S33b.** The after-stop frontier differences of Table S33 by the tracker's estimate of the lead's speed at the decision (the true speed is zero in this phase), in decision-equivalents.

| Source | <=0.5 m/s | 0.5-1 m/s | 1-2 m/s | >2 m/s |
|---|---|---|---|---|
| Decisions | 6,725 | 53 | 43 | 36 |
| E (the room) | 4.1 | 6.7 | 18.6 | 26.9 |
| CK3 | 0.01 | 8.3 | 20.8 | 26.8 |
| AM | 1.7 | 4.8 | 14.1 | 18.9 |
| N | 0.03 | −0.01 | 0.01 | 0.08 |

> **TABLE S34.** The lead track's estimated state at the decision (evaluated decisions; median [25%, 75%]): the tracker's lead speed and the true one; the track's acceleration estimate along its velocity; the constant-velocity-predicted minus the true longitudinal position of the lead centre 1 s and 3 s after the decision (positive: the lead is predicted further ahead than it is); the ego's speed.

| Decisions | n | Tracker speed (m/s) | True speed (m/s) | Acceleration estimate (m/s²) | Predicted − true at 1 s (m) | at 3 s (m) | Ego speed (m/s) |
|---|---|---|---|---|---|---|---|
| Before onset | 678 | 9.63 [4.77, 12.95] | 9.75 [4.93, 13.36] | 0.06 [−0.17, 0.24] | −0.23 [−0.62, 0.39] | 6.21 [2.56, 9.21] | 10.00 [4.78, 13.42] |
| Lead braking, since onset 0–1 s | 334 | 8.81 [4.36, 10.04] | 6.52 [3.53, 9.70] | −0.61 [−1.46, −0.05] | 2.70 [2.00, 3.61] | 13.74 [10.78, 19.29] | 9.10 [3.89, 10.00] |
| Lead braking, since onset 1–2 s | 189 | 7.39 [5.23, 10.73] | 5.30 [2.68, 9.61] | −3.05 [−3.81, −2.39] | 3.78 [2.92, 5.00] | 16.86 [14.03, 19.20] | 10.00 [8.67, 13.70] |
| Lead braking, since onset ≥ 2 s | 232 | 5.31 [3.33, 7.75] | 3.97 [2.10, 6.21] | −2.91 [−3.72, −2.41] | 2.98 [2.36, 3.66] | 13.54 [9.24, 16.52] | 9.02 [6.54, 11.89] |
| After the stop, 0–1 s | 300 | 0.45 [0.18, 1.05] | 0.00 [0.00, 0.00] | −2.91 [−3.87, −1.50] | 0.58 [0.16, 1.30] | 1.49 [0.54, 3.51] | 3.13 [1.86, 4.56] |
| After the stop, 1–2 s | 300 | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | −0.12 [−0.34, 0.01] | −0.15 [−0.22, −0.07] | −0.14 [−0.22, −0.03] | 0.01 [0.00, 1.87] |
| After the stop, 2–5 s | 900 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | −0.28 [−0.35, −0.23] | −0.28 [−0.36, −0.23] | 0.00 [0.00, 0.00] |
| After the stop, 5–10 s | 1,500 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | −0.30 [−0.38, −0.24] | −0.30 [−0.38, −0.24] | 0.00 [0.00, 0.00] |
| After the stop, ≥ 10 s | 3,857 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | −0.30 [−0.38, −0.25] | −0.30 [−0.38, −0.25] | 0.00 [0.00, 0.00] |

> **TABLE S34b.** Consistency of the lead track by phase: mean normalised innovation squared of the position block over the track's distinct updates (2 degrees of freedom; a consistent filter averages 2), and the mean and median normalised error of the velocity that the planner uses at the decision, against the true velocity, with the logged velocity block (2 degrees of freedom).

| Phase | Updates | Mean NIS | Decisions | Mean velocity NEES | Median velocity NEES |
|---|---|---|---|---|---|
| Before onset | 151 | 0.50 | 678 | 2.06 | 1.28 |
| Lead braking | 150 | 1.47 | 755 | 5.08 | 3.70 |
| Lead braking, first 1 s | 66 | 0.68 | 334 | 4.34 | 3.05 |
| After stop | 1,383 | 0.10 | 6,857 | 0.09 | 0.00 |
| After stop, first 2 s | 120 | 0.77 | 600 | 0.99 | 0.01 |

> **TABLE S35.** The tuning runs beside the evaluation runs (3 s commitment, step frontier, points; each population on its own frontier). Tuning runs were recorded with a fixed recording margin (α = 0.105, a unit variance in place of the tracker's covariance); evaluation runs with the tracker's covariance (α = β = 1.642–7.550). Per-phase gain: in sample, as a share of the pooled room (Table S23's definition).

| Quantity | Tuning runs | Evaluation runs |
|---|---|---|
| Runs; evaluated decisions | 20; 3,018 | 35; 8,290 |
| Decisions before onset / lead braking / lead stopped | 378 / 279 / 2,361 | 678 / 755 / 6,857 |
| Share after the stop; share with the ego at or below 0.5 m/s | 78.2%; 70.3% | 82.7%; 77.5% |
| Room $R$, all (pp; decision-equivalents) | 1.18; 35.6 | 5.56; 460.7 |
| Room $R$, ego moving (pp; decision-equivalents) | 4.05; 36.4 | 10.16; 189.4 |
| Room $R$, before onset (pp; decision-equivalents) | 0.07; 0.27 | 0.43; 2.9 |
| Room $R$, lead braking (pp; decision-equivalents) | 10.14; 28.3 | 15.59; 117.7 |
| Room $R$, lead stopped (pp; decision-equivalents) | 1.20; 28.3 | 0.82; 56.3 |
| Pooled room over the decision-weighted phase rooms | 0.63 | 2.60 |
| Per-phase gain, in sample (share of the pooled room) | 0.632 | 0.893 |
| RR(CK3): all / lead braking / lead stopped | 0.377 / 0.301 / 0.937 | 0.831 / 0.606 / 0.993 |
| RR(AM): all / lead braking / lead stopped | 0.245 / 0.063 / 0.063 | 0.376 / −0.044 / 0.702 |
| RR(NA): all / lead braking / lead stopped | 0.063 / 0.080 / −0.0016 | 0.017 / −0.0064 / 0.079 |
| RR(N): all / lead braking / lead stopped | 0.0022 / 0.0035 / −0.0011 | 0.0012 / −0.0025 / 0.0019 |

> **TABLE S36.** Reliance on the stop (reaction-and-stop scoring: τ = 0.75 s, 6 m/s², plans judged until their stop ends). At each caution level, each source's frontier point under this scoring; the share of the population's decisions whose selected row is unsafe if followed for 3 s but safe with the stop, averaged over the levels. O: the scoring's perfect oracle (its one selection).

| Population | Decisions | F0 | N | NA | AM | CK3 | E | O |
|---|---|---|---|---|---|---|---|---|
| All | 8,290 | 5.8% | 5.8% | 5.7% | 4.7% | 3.3% | 0.6% | 72.3% |
| Ego moving | 1,863 | 19.0% | 19.2% | 18.7% | 17.8% | 15.3% | 0.9% | 51.6% |
| Before onset | 678 | 5.0% | 5.0% | 5.0% | 5.0% | 5.0% | 5.0% | 5.0% |
| Lead braking | 755 | 41.7% | 42.2% | 41.0% | 37.9% | 40.5% | 65.7% | 70.2% |
| Lead stopped | 6,857 | 1.2% | 1.2% | 1.2% | 0.7% | 0.4% | 0.3% | 79.1% |

> **TABLE S36b.** Caution counted under the reaction-and-stop scoring (τ = 0.75 s, 6 m/s², judged until the stop ends): the oracle row and the truly safe set of the caution measure taken from this scoring instead of the 3 s commitment. den₀ in decision-equivalents and RR₀ with 95% intervals (draw of record), beside the values of record (Table IV).

| Quantity | All | Ego moving |
|---|---|---|
| den₀ (decision-equivalents) | 53.8 [19.4, 92.9] | 12.8 [4.7, 22.0] |
| RR₀(N) | −0.0006 [−0.0061, 0.0056] | −0.013 [−0.022, 0.0071] |
| RR₀(NA) | 0.0078 [−0.0069, 0.036] | −0.041 [−0.067, 0.0023] |
| RR₀(AM) | 0.545 [0.447, 0.636] | 0.095 [−0.018, 0.193] |
| RR₀(CK3) | 0.829 [0.769, 0.868] | −0.867 [−1.474, −0.444] |

> **TABLE S37.** A constant time-gap margin scored like every source: along every constraint, $s = (r_0 + v_e)^2$ with $v_e$ the row's speed at the constraint's time, so that at $g = h^2$ a row is feasible when every clearance is at least $h(r_0 + v_e)$: a time gap $h$ and a standstill distance $h r_0$. $r_0$ = 2 m/s (1 and 4 m/s beside it). 3 s commitment: RR with 95% intervals (draw of record); reaction-and-stop (τ = 0.75 s, 6 m/s², judged until the stop ends): RR₀. The braking prediction and the acceleration margin, scored in the same program, beside them.

| Quantity | TG, $r_0$ = 2 | TG, $r_0$ = 1 | TG, $r_0$ = 4 | CK3 | AM |
|---|---|---|---|---|---|
| RR, all | 0.314 [0.219, 0.389] | 0.387 | 0.213 | 0.831 | 0.376 |
| RR, ego moving | 0.168 [−0.032, 0.308] | 0.185 | 0.116 | 0.472 | 0.293 |
| RR, before onset | −0.481 [−3.114, 0.253] | −0.726 | −0.259 | −0.536 | −0.128 |
| RR, lead braking | 0.088 [−0.236, 0.357] | 0.053 | 0.093 | 0.606 | −0.044 |
| RR, lead stopped | 0.161 [0.056, 0.268] | 0.185 | 0.066 | 0.993 | 0.702 |
| RR₀ at τ = 0.75 s, all | 0.442 [0.342, 0.547] | 0.487 | 0.354 | 0.936 | 0.570 |
| RR₀ at τ = 0.75 s, ego moving | 0.542 [0.474, 0.589] | 0.595 | 0.452 | 0.038 | 0.257 |

> **TABLE S38.** The grading check in the population before the lead's stop (Table S22, T = 0: before onset and while the lead brakes; 3 s commitment, step frontier, points; Addendum 01 to Amendment 09). Partial oracles: the oracle's critical values on a random share of the decisions and the class average's elsewhere, for the draw of record and over 50 further draws (mean [min, max]). Below: the braking prediction's and the acceleration margin's shares and frontier distances in decision-equivalents.

| Quantity | 25% | 50% | 75% |
|---|---|---|---|
| Partial oracle, draw of record | −0.365 | −0.258 | 0.232 |
| Partial oracle, 50 draws: mean [min, max] | −0.326 [−0.423, −0.228] | −0.221 [−0.364, −0.088] | 0.243 [0.081, 0.374] |

| Source | Share | Frontier distance (decision-equivalents of 1,433) |
|---|---|---|
| CK3, braking prediction | 0.289 | 35.5 |
| AM, acceleration margin | 0.434 | 53.4 |

