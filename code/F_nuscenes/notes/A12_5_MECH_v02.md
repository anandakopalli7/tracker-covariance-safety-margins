# Text for AMENDMENT_12 §5: the real-sensor mechanism check on nuScenes, v02

Drafted by session F (Claude Opus 5.5), 22 Nov 2026, for the coordinator to merge verbatim into `revision_v13\AMENDMENT_12_v13.md` §5.
v01 was drafted about 00:55 EST. v02 was written about 03:55 EST, before LOCK_A12c and before any val value. It adds:
- **The primary, chosen on the training split** (coordinator's decision of 03:27; the author agreed: "Yes, keep it"). The primary is
  CANMOT's within-cell τ over the pairs around real missed detections. It is the only Holm entry.
- **The original all-row statistic becomes descriptive.** Train showed it dominated by steady pairs and expected to fail.
- **The IMM is secondary.** Its design numbers come from the first 50 train scenes.
- **§5.8** holds the train design numbers.

---

## 5. Real-sensor mechanism check on nuScenes (session F)

**5.1 Question.** On real sensor data, does the variation of a tracker's covariance follow the realised prediction error around real
missed detections? This needs no planner room: it asks whether, at one decision time, the actor the covariance calls more uncertain is
the one whose 3 s prediction turns out worse.

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

**5.4 Primary statistic (train-informed, v02).**
- **Population:** the rows with age ≥ 1.0 s (steady, in-miss, post-miss).
- **Pairs:** within each (scene, keyframe) cell, the pairs of that population with AT LEAST ONE member in-miss or post-miss. That is
  every within-cell pair except the pairs of two steady rows.
- **Statistic:** Kendall's τ_b over those pairs, pooled over cells:
  τ = Σ_c (C_c − D_c) / Σ_c √((n0_c − n1_c)(n0_c − n2_c)).
  - C and D are the concordant and discordant selected pairs of (σ_h, e_h) in cell c; n0 is the number of selected pairs; n1 and n2
    are the selected pairs tied in σ_h and in e_h.
  - Pairs never cross cells, so differences between scenes and times cannot create the association.
- **Interval:** 20,000 scene resamples, `default_rng(20261951).integers(0, S, (20000, S))`, with the S scenes in ascending name order.
  - A resample's τ is Σ w_s A_s / Σ w_s B_s, with A_s and B_s the scene's summed numerator and denominator terms.
  - Calibration per A10 §2.6: double bootstrap 2,000 × 1,000, seeds 20261912 / 20261913, checks 20261914 / 20261920. The conventions are
    those of `cd_common_v13`: rank p-values, and coverage over the outer samples with a finite statistic.
- **Hypothesis M1 (primary, CANMOT):** around real missed detections, the covariance's variation carries rank information about the
  realised error. It passes if τ's lower end > 0 at the calibrated level (one-sided 0.025).
- **Holm (A12 §4):** p_M1 = (1 + #{τ\* ≤ 0}) / (20,000 + 1). This is §5's only primary statistic and its only Holm entry.
- **Why this population (disclosure, for the text):** "the primary population was chosen on the training split, after the all-row
  statistic there was found to be dominated by steady tracks; validation was scored once". The train numbers that motivated it are
  in §5.8.

**5.5 Secondary and descriptive (95% percentile intervals on the same draw; all reported on val, nothing hidden).**
- **Secondary, the IMM** (no Holm entry, no threshold or power decision):
  - its τ over the same miss pairs;
  - its all-row τ.
  - Its design numbers come from the first 50 train scenes (§5.8).
- **Descriptive, both trackers:**
  - **The original all-row statistic (v01's M1):** τ over all within-cell pairs of the age ≥ 1.0 s rows. For CANMOT it is reported
    with the statement that train showed it dominated by steady pairs and expected to fail.
  - **The strata, separately:**
    - steady: pairs of two steady rows;
    - in-miss, post-miss and young: pairs with at least one member in the stratum (young rows enter only here);
    - each with its τ, the mean σ_h and e_h, and the row counts.
  - **τ_b pooled across all age ≥ 1.0 s rows** (not within cells).
  - **A drawn within-cell permuted twin** over the same all-row population: K = 20 permutations of σ_h within each cell
    (`default_rng(20261952)`), its mean τ.
- **Keys:**
  - primary: M.tau, M.tau.ci95, M.p, M.level, M.ci, M.passes;
  - original all-row statistic: M.all.tau, M.all.tau.ci95, M.all.p;
  - strata: M.s.<stratum>.*;
  - M.n_rows.*, M.tau_pooled, M.twin_mean.
  - The IMM uses the same keys (export prefix to be set with A).

**5.6 Design on train (fixed before val).**
- **Fixed by rule before any τ was computed:** the gate, the classes, the 1.0 s minimum age, the 3 s horizon and its 0.25 s tolerance,
  the score thresholds, and the strata. They come from the nuScenes metric's gate, the planner's vehicle classes and the tracker's own
  thresholds.
- **Chosen on train after the design numbers (v02):** the primary pair set. This is declared in §5.4 and above.
- **Programs:** `F_nuscenes\code\f21_mech_v02.py` (first) and `F_nuscenes\recount_mech\fm_recount_v02.py` (second, Claude Sonnet 5.5,
  written from the text without reading F's code). Both are copies of their v01 with only the primary pair set changed and the all-row
  statistic kept under M.all.*. Frozen in `work\locks\FREEZE_F_A12.json` before LOCK_A12c.

**5.7 Verification and order.**
- **Agreement per A10 §10.1(c):**
  - on the first 50 train scenes, both trackers: v01 26 keys, v02 29 keys, max abs diff 8.9e-16;
  - a rehearsal of the val code path with the calibration, on the same 50 train scenes in a pod sandbox (§5.8);
  - then on val.
- **Order:**
  1. train design;
  2. this text;
  3. LOCK_A12c (coordinator);
  4. val scored ONCE by both programs on pod m1 (`code\f21_pod_run_v02.sh val`, refusing without LOCK_A12c);
  5. comparison;
  6. export `work\F_nuscenes\out\A_EXPORT_M.json` / `A_RECOUNT_M.json`, prefix `M.`.
- **Where:** the full-train CANMOT rows were built on the laptop. The 50-scene checks, the rehearsals and the val scoring run on pod
  `claude-v13f-m1` (RTX 4090, $0.89/h). The val inputs were uploaded and SHA-256 verified before the lock (450 files).

**5.8 Train design numbers** (22 Nov, before LOCK_A12c; no val value exists).
- **CANMOT, all 700 train scenes.** Rows: steady 217,089; in-miss 8,589; post-miss 12,886 (age ≥ 1.0 s: 238,564); young 41,804.
  Cells with pairs: 19,883.
  - **v02 primary, miss pairs** (`out\mech\MECH_train_T1_v02_fromrows.json`, from v01's rows with v02's own functions; the all-row τ
    recomputed from those rows equals v01's exactly):
    - τ = **+0.190**, 95% interval [0.167, 0.212], one-sided p ≈ 5e-5;
    - power for val (150 scenes, se 0.025 scaled from train) at the train value: ≈ 1.0;
    - the miss pairs carry 19% of the all-row pairs' denominator weight;
    - the second program's own full-train run (`recount_mech\MECH_RECOUNT_train_T1_v02.json`, `fm_recount_v02.py` on all 700 scenes,
      `--no-calib`) gives the same primary, interval, p, all-row statistic, strata, pooled τ and twin (equal to about 1e-16).
  - **Original all-row statistic** (`MECH_train_T1_v01.json`): τ = −0.0108, 95% [−0.0216, −0.0001], one-sided p = 0.976. Power for val
    at that value: about 0.002, so it would fail.
  - **Strata (95%):**
    - steady pairs −0.057 [−0.068, −0.047] (mean σ_h 2.44 m, mean e_h 1.19 m);
    - in-miss +0.242 [0.219, 0.265] (5.27 m, 1.37 m);
    - post-miss +0.143 [0.118, 0.169] (2.52 m, 1.25 m);
    - young +0.169 [0.154, 0.184] (2.74 m, 2.28 m).
  - **Other descriptives:** within-cell permuted twin, mean τ +0.0003; τ_b pooled across cells +0.019.
- **First 50 train scenes, both programs (v02):**
  - CANMOT: primary +0.244 [0.147, 0.287]; all-row +0.055 [−0.025, 0.107].
  - IMM (secondary): primary +0.301 [0.143, 0.337]; all-row +0.159 [0.049, 0.187].
  - IMM strata: steady +0.119, in-miss +0.385, post-miss +0.234, young +0.147.
- **Rehearsals of the val code path** (pod sandbox whose "val" folders pointed to the first 50 train scenes, with a placeholder lock
  file inside the sandbox only):
  - v01: both trackers, 29 keys agree; calibrated levels, intervals and verdicts equal (`out\mech_rehearsal_train50\`);
  - v02: both trackers, 32 keys agree (max 8.9e-16), the calibrated levels, intervals and verdicts included
    (`out\mech_rehearsal_train50_v02\`).
- **Reading:** CANMOT's covariance ranks the realised error around real missed detections and for young tracks. Among steady tracks it
  carries no rank information (slightly inverse), and steady rows are 91% of the age ≥ 1.0 s rows. The primary therefore asks §5.1's
  question where the covariance is meant to carry it.
