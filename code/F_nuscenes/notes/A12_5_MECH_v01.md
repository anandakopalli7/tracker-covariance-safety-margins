# Text for AMENDMENT_12 §5: the real-sensor mechanism check on nuScenes, v01

Drafted by session F (Claude Opus 5.5), 22 Nov 2026, about 00:55 EST by this laptop's clock, for the coordinator to merge verbatim into
`revision_v13\AMENDMENT_12_v13.md` §5. The train design's numbers are added in §5.8 before LOCK_A12c. No val value of this check exists
before LOCK_A12c.

---

## 5. Real-sensor mechanism check on nuScenes (session F)

**5.1 Question.** On real sensor data, does the variation of a tracker's covariance follow the realised prediction error, including
around real missed detections? This needs no planner room: it asks whether, at one decision time, the actor the covariance calls more
uncertain is the one whose 3 s prediction turns out worse.

**5.2 Data.** Package F's frozen nuScenes pipeline (A10 §8; FREEZE_F): the 2 Hz keyframes of the design split (700 train scenes) and
the held-out split (150 val scenes).
- Tracks of CANMOT (T1, the online tracker of record) and of the IMM (B1), as tracked for A10 §8 (`F_nuscenes\cache\tracks_T1|tracks_IMM\{train,val}\`).
- The truth annotations and the detector output of record (`F_nuscenes\cache\{train,val}\`).
Nothing is re-tracked.

**5.3 Rows (one per decision instance).**
- **Tracks:** a track of a four-wheel vehicle class (car, truck, bus, trailer; CANMOT classes 2, 6, 1, 5) output at keyframe t.
- **Matching:** one-to-one to a truth annotation of the same class at t, by the Hungarian assignment on the bird's-eye centre distance
  with a gate of 2.0 m (the nuScenes tracking metric's centre-distance threshold).
- **Horizon:** the truth instance must be annotated again at the keyframe u nearest t + 3 s, with |t_u − t − 3 s| ≤ 0.25 s.
- **Per row, with Δ = t_u − (the track's state time):**
  - **e_h**, the realised 3 s CV-prediction error: ‖centre_xy + velocity_xy · Δ − truth_xy(u)‖.
  - **σ_h**, the covariance's 3 s predicted position spread: √trace(P_pp + Δ(P_pv + P_vp) + Δ² P_vv), with P the (x, y, vx, vy) block of
    the track's 9 × 9 covariance (indices 0, 1, 6, 7, as the planner's `covariance4`). The planner's acceleration-noise term (σ_acc = 1
    for every vehicle) adds the same constant to every row's trace, so it cannot change any within-cell rank.
  - **Age:** t minus the keyframe time of the track id's first output in the scene.
- **Real missed detection** of the matched instance at keyframe k: the instance is annotated at k, and no detection of its class with
  score ≥ the tracker's own threshold (`contracts\tracker_config.json` `preprocessing.SF_thre`: car 0.16, truck 0, bus 0, trailer 0.1)
  lies within 2.0 m of its centre. The tracker received no usable detection of the object.
- **Strata:**
  - young: age < 1.0 s;
  - otherwise in-miss: missed at t;
  - otherwise post-miss: missed at t − 1 or t − 2;
  - otherwise steady.
  - With CANMOT's output rule of record (punish_num = 1), a track missed for 2 or more keyframes is not output and returns as a new,
    young track.

**5.4 Statistic.**
- **Primary population:** the rows with age ≥ 1.0 s (steady, in-miss, post-miss).
- **Primary statistic:** Kendall's τ_b within (scene, keyframe) cells, pooled over cells:
  τ = Σ_c (C_c − D_c) / Σ_c √((n0_c − n1_c)(n0_c − n2_c)).
  - C and D are the concordant and discordant pairs of (σ_h, e_h) within cell c; n0 is its number of pairs; n1 and n2 are its pairs tied in
    σ_h and in e_h.
  - Pairs never cross cells, so differences between scenes and times cannot create the association. A within-cell permuted twin has
    expectation exactly 0.
  - Ties in σ_h are frequent for a fixed-noise filter (its covariance depends on the update history only); τ_b accounts for them.
- **Interval:** 20,000 scene resamples, `default_rng(20261951).integers(0, S, (20000, S))`, with the S scenes in ascending name order.
  - A resample's τ is Σ w_s A_s / Σ w_s B_s, with A_s and B_s the scene's summed numerator and denominator terms.
  - Calibration per A10 §2.6: double bootstrap 2,000 × 1,000, seeds 20261912 / 20261913, checks 20261914 / 20261920. The conventions are
    those of `cd_common_v13`: rank p-values, and coverage over the outer samples with a finite statistic.
- **Hypothesis M1 (primary, CANMOT):** the covariance's variation carries rank information about the realised error. It passes if τ's
  lower end > 0 at the calibrated level (one-sided 0.025).
- **Holm (A12 §4):** p_M1 = (1 + #{τ\* ≤ 0}) / (20,000 + 1).

**5.5 Secondary and descriptive (95% percentile intervals on the same draw).**
- The same τ for the IMM (secondary; no Holm entry).
- **Strata, both trackers:**
  - τ over within-cell pairs with at least one member in-miss, post-miss or young (young rows enter only here);
  - τ over pairs of two steady rows;
  - the mean σ_h and e_h per stratum, and the row counts.
- τ_b pooled across all primary rows, not within cells.
- A drawn within-cell permuted twin: K = 20 permutations of σ_h within each cell (`default_rng(20261952)`), its mean τ.

**5.6 Design on train (fixed before val).**
- **What is fixed:** the gate, the classes, the 1.0 s minimum age, the 3 s horizon and its 0.25 s tolerance, the score thresholds, and
  the strata.
  - They were set by rule (the nuScenes metric's gate, the planner's vehicle classes, the tracker's own thresholds) before any τ was
    computed.
  - The train split only provides the design numbers and the power for val (§5.8).
- **Program:** `F_nuscenes\code\f21_mech_v01.py`, frozen in `work\locks\FREEZE_F_A12.json` with its second program before LOCK_A12c.

**5.7 Verification and order.**
- **Second program:** Claude Sonnet 5.5, written from this section without reading F's code. Agreement per A10 §10.1(c) on train first,
  then on val.
- **Order:**
  1. train design (both programs agree);
  2. this text with §5.8 filled;
  3. LOCK_A12c (coordinator);
  4. val scored ONCE by both programs;
  5. comparison;
  6. export `work\F_nuscenes\out\A_EXPORT_M.json` / `A_RECOUNT_M.json`, prefix `M.`.
- **Cost:** $0, on the laptop, one process at BelowNormal.

**5.8 Train design numbers.** [filled from `F_nuscenes\out\mech\MECH_train_T1_v01.json` and `..._IMM_v01.json` before LOCK_A12c:
rows per stratum, τ with its 95% interval, the strata, the power for val at the train τ]
