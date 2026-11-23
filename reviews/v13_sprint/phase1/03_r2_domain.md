# Seat 3: Peer Reviewer 2 (Domain: tracking, motion planning, AV safety margins)

- **Model:** Claude Opus 5.5 (the same model drafted the paper, so I read it skeptically)
- **Freeze folder:** `ARS_TRIAL\revision_v13\work\A_text\out\freeze_v13_2002\`
- **SHA-256 of MANUSCRIPT_v13.md:** `93541FF6B1592BBDFC9B5F239FD81E8537FA3F433A3E2A76BA43A242914A4EAD`
- **Read:** full manuscript; Supplement S1–S4, S6.1, S7, S9, S11, S13, S14. No earlier reviews or response letter.

## Recommendation

**Major Revision**, confidence 4/5. The equal-caution protocol is sound and the lead-braking null is worded correctly. But the textbook account that predicts the new results is unused, the IMM arm is not a fair test of a manoeuvre-adaptive covariance, the pedestrian-crossing test bed is never specified, and "no extra cost" overstates the closed loop.

## Findings

**F1. MAJOR: the paper explains the result with weaker Kalman theory than the literature offers.** (Sec. VI, first paragraph; Sec. V-E, "We read the bottleneck…"; S11)
- **Problem.** Section VI relies only on convergence to the Riccati steady state. The stronger textbook fact [25]: with fixed Q and R, P depends only on *when* measurements arrive and, through object-frame noise, on the estimated heading, never on the measured values. That predicts every outcome in advance (constant on lead braking, heading-driven in crossing, as S11 says, schedule-driven under dropouts) and why only the adaptive filter, whose P follows its innovations, beats its twin. Section V-E presents these as discoveries.
- **Fix.** Add to VI: "For a fixed-noise Kalman filter, P depends on when measurements arrive and on the estimated heading, not on the measured values [25]. Its variation can therefore encode the update schedule and geometry, not the manoeuvre. Crossing tests the geometry channel and dropouts the schedule channel. Only the adaptive filter, whose noise follows its innovations, carried rank information." Then show the mechanism rather than assert it. For crossing, regress the log margin ratio on the angle between the estimated heading and the constraint normal, and separately on the realised error. For dropouts, compare N with F0 scaled by the number of updates since the last detection, a baseline that uses no ground truth.

**F2. MAJOR: the IMM is not a fair test of a covariance that varies.** (Sec. III-D; V-B; Table III; S4; Table S7)
- **Problem.** Both modes share the position–velocity noise; the CA mode adds only σ_a² = 0.001, whereas a standard manoeuvring-target IMM [21], [22] pairs low- and high-noise models. During braking its NIS is 9.24, against 9.58 for CV and an expected 2 (Table S7): it did not switch modes, and mode probabilities are not reported. The planner also discards the IMM's acceleration and mode-conditioned means, yet CK3, which recovers 78%, is exactly such a mean shift. The re-tuned IMM still barely varies (99.4%).
- **Fix.** Report mode probabilities around the onset of braking. Add, at least descriptively, an IMM with two noise levels and one arm that predicts with the IMM's mixed mean. In the abstract and conclusion write: "an IMM whose modes differ only by a small acceleration term, and whose acceleration estimate the planner does not use, did not switch modes during braking (NIS 9.2 against 2) and barely varies."

**F3. MAJOR: the pedestrian-crossing test bed and other scenario parameters are not given.** (Sec. III-A; S1, Tables S1–S2; V-E; Table S33)
- **Problem.** Pedestrian crossing is in the title, but neither III-A nor S1 describes it. Missing details:
  - the walker's speed, start rule, distance ahead, direction, hesitation and occlusion;
  - the ego's speeds;
  - which decisions are evaluated when no vehicle is ahead (Section IV-D defines its population by a vehicle ahead);
  - the pedestrian-class noise and class average.

  Only 1 of 390 runs had a contact (room 0.16 pp). If CARLA walkers follow scripted constant-speed paths, constant-velocity prediction is nearly exact, which explains the small room and narrows "uninformative variation". The lead's braking range (S1.3 implies 2–6 m/s²) is missing beside the ego's 5 m/s² fallback, so some contacts may be unavoidable. In cut-in, nothing was a wrong go at any caution, and 5,292 of 5,293 decisions came from tracks at least 4 s old.
- **Fix.** Add a paragraph to III-A and a table to S1. Give the lead's deceleration range beside the ego's braking limit. In V-A write: "the cut-in generator produced no wrong go and no young track; it is uninformative, not a negative result."

**F4. MAJOR: the closed-loop "safer at no extra cost" findings are over-read.** (Abstract, "In closed loop (lower caution level)…"; V-C; V-E, higher level; VII; Tables IV, S23, S25, S35)
- **Problem.**
  - (a) Behind stopped leads every arm loses about 24.5 s, counted only over pairs without contact, so the measure can hardly detect a progress cost.
  - (b) CK3's 0.16 [0.10, 0.22] s and N-under-dropouts' 0.25 [0.15, 0.36] s both exclude zero; "no extra cost" is the plan's label (upper end below 0.5 s), not plain English.
  - (c) The time gap does as well (−0.13 s); the abstract omits it.
  - (d) Behind leads that do not brake hard, CK3 costs 0.52–0.82 s.
  - (e) At the lower level F0 contacts in 20% of runs and brakes fully on 52.7% of decisions, not a deployed-ACC point; at 5%, CK3 is inconclusive.
  - (f) The dropout comparison is not caution-matched; a margin that widens while coasting is expected to be safer.
- **Fix.** Abstract: "In closed loop behind leads that brake to a stop, at a level where the class average makes contact in 20% of runs, the prediction removed every contact for 0.16 [0.10, 0.22] s more time lost (within the plan's 0.5 s allowance), as did a constant time gap; behind leads that do not brake hard it cost 0.5–0.8 s." Section VII: "at the higher level (secondary; not caution-matched), contacts were 5% against 15% at 0.25 s more time lost, as expected of a margin that widens while a track coasts."

**F5. MINOR: the dropout test holds coasting tracks long enough that none is lost.** (V-E; Table S5, output-rule row; Table S34)
- **Problem.** Coasting for 3 updates (1.5 s) is a defensible stack choice, close to nuScenes-era trackers' maximum ages. But it equals the longest mask, so no track is reborn and the birth covariance (where S11 found the ratio departs) is never tested. The masks are i.i.d., unlike occlusion, and the masked objects are not named. N's share inside dropouts is −0.003 (Table S34), so the confirmed 2.8% lies outside the windows, and the paper does not say where.
- **Fix.** Report N's share by updates since the last detection. State: "tracks coasted through every window; track loss and re-initialisation were not tested." Name which objects were masked.

**F6. MINOR: the margin omits the motion model's process noise over the look-ahead.** (III-E; S1.1)
- **Problem.** s = zᵀPz propagates the posterior without the process noise a predicted covariance normally adds (FPFᵀ + Q(t)).
- **Fix.** "The margin s uses the posterior covariance propagated without the motion model's process noise over the look-ahead; including it is not tested."

**F7. MINOR: the lag is not separated from the detector, and consistency by phase is buried in the supplement.** (VI, "What a varying covariance needs"; Table III; Table S7)
- **Problem.** CenterPoint accumulates 0.5 s of sweeps, so part of the 1.42 m lag may be the detector's. The online filter's NIS (0.49 before braking, 1.87 braking, 0.07 stopped), the usual sign of fixed noise meeting a manoeuvre, appears only in the supplement.
- **Fix.** Report the detector's velocity error by phase; put the NIS-by-phase sentence in VI; give CK3's trigger threshold and persistence.

**F8. MINOR: related work misses the closest automotive literature, much of it found by the author's own search.** (II, "Threat assessment…"; S13, queries 2, 15–17, 25–26, 36–39, 49)
- **Problem.** Missing: uncertainty in braking and warning decisions (Stellet et al., IV 2015/2016; Stöckle et al., ITSC 2018; Berthelot et al.; Eidehall and Petersson; Houénou et al., ITSC 2014; Lefèvre et al., 2014; Pak, Sensors 2022); pedestrian switching dynamics (Schneider and Gavrila, GCPR 2013; Kooij et al., IJCV 2019); track existence under misses (Mušicki et al., TAC 1994); propagated obstacle uncertainty (Du Toit and Burdick, T-RO 2012; Althoff et al., T-ITS 2009).
- **Fix.** One sentence per group, each checked against Crossref, and: "Our frontier is the decision-level analogue of the operating characteristics used to evaluate warning and braking functions."

## Strengths

- Equal caution removes the trivial "a wider margin is safer" effect.
- The amplitude-matched oracle and permuted twin are a good sensitivity control.
- The wording is narrow, and the paper admits the mechanism is not new.
- NIS and NEES are given by phase; the closed loop has a brake test; costs behind leads that do not brake hard are reported.
- The adaptive filter beats its twin, as theory expects, and the test is disclosed as chosen after the data were seen.

## Score

**6/10.** Careful and transparent, but theory predicts the central result. The new scenarios need specifying, and the mechanism must be shown.
