# AMENDMENT 10 to BRIEF_EVIDENCE_v03.md: offline re-tracking (B), fresh runs in two scenario families (C), non-braking leads and an event-level table (D), a closed-loop test (E) and a real-sensor replication (F), after the ARS review of draft v12 — DRAFT

Written 19 Nov 2026 by the v13 planning session (Claude Opus 5.5, `claude-opus-5-5`, in `ARS_TRIAL`):
- first version: clock read 11:51 EST;
- **this version: clock read 12:04 EST.** It follows the requesting session's scope change: the user chose "Push for 5 stars". D became required; E, F and the cut-in family were added; both outcomes of the varying-covariance arm were made reportable.

**Where it sits.** This file is in `revision_v13\`, not in `11_ojits\`. If the author adopts the revision, the lead copies it into `11_ojits\` under the next free number, with Amendments 08 and 09, which are not there yet. It follows Amendment 09 (SHA-256 `7c5d6285…915a`) and its Addendum 01 (`ed9720c2…eab9`), and changes neither.

**Status: DRAFT, not in force.** It becomes the plan of record when all of the following hold:
1. The author approves it, with any default of §12 changed.
2. The approved text is saved as `AMENDMENT_10_v13.md`.
3. Its SHA-256 and the confirmed defaults are written to `LOCK_A10_1.txt`.
4. Steps 1–3 happen before any value of B, C, D, E or F is computed.

`LOCK_A10_2.txt` (§4) freezes every tracker, arm, variant and adapter before any value of fresh, held-out or closed-loop data is computed.

**Authority**
- The author's goal is an accept-ready paper (their words: "Push for 5 stars").
- The requesting session asked for B–F to be pre-registered and for nothing to run until the user approves.
- The researcher's standing instruction from revisions v11 and v12 applies: re-measured numbers are reported even if a headline figure drops.

**Trigger.** `review_v12_output\ARS_REVIEW_v12_v01.md` and `ARS_DECISION_PACKAGE_v12_v01.md`:
- Major Revision;
- R1–R13, S1–S25;
- the Devil's Advocate's C1 validated;
- two verification gaps.

**State when written.** No value of any analysis below has been computed. The fresh, closed-loop and non-braking-lead runs do not exist. Known:
- every number of drafts v11 and v12 and of `revision_v11\analysis\out\` and `revision_v12\analysis\out\`;
- the v12 review.

To plan, I read the following:
- **Code and configuration:** the loaders, the capture probe, the job builder, CANMOT's configuration and motion models, and the M4 tracker-replay report.
- **Project design notes:** `09_redesign\DESIGN_NOTES_v01.md` §6.4e, §6.4m and §6.4n, which give the braking fix F2, Gate C on the stand-in, and the costing of a CARLA confirmation; and `02_design\PROPOSAL_CARLA_CONFIRMATION_v02.md`.
- **The Argoverse 2 inventory and pilot report:** `02_design\INVENTORY_AV2_C1_ARCHIVE_v01.md`, `10_av2\REPORT_AV2_PILOT_v01.md`. These contain exploratory results on design folds 0–1. **That knowledge informs the horizon rule of §8, which is why that rule is stated as using the design folds.**
- **Files examined without computing anything:**
  - the first record of several capture logs of run p1b_fit_finite_0005;
  - the detector inference times of run p1b_fit_finite_0037;
  - the first records of the nuScenes CenterPoint result files in `Downloads\nusc_results_flip\`.
- **Counts:** files, receipts, draw ranges and recording knobs of the protocol's cases.
- **Hashes:** the detector checkpoint.

No frontier, room, share, NIS, ratio, contact count or other quantity named below was computed by this session, on any data.

## 1. What does not change

**Scoring and sources**
- The scoring library `optA_lib_v02.py` and the loader `rev_common_v01.py`, imported unchanged.
- The 3 s commitment scoring.
- The reaction-and-stop scoring, with plans judged until the stop ends.
- The caution definition and the 202-value grid.
- The evaluated-decision rule.
- F0's P̄ of record.
- The sources NA, E, CK3 (3 m/s²), AM, Q and TG (r₀ = 2 m/s) as in v12.
- The planner and its 17 rows.

**Earlier results.** Every number of v12 stays as recorded and keeps its exploratory status. Analyses of old runs that reuse v12 quantities use the draw of record (20,000 run resamples, `default_rng(20261113)`).

**The generator of the fresh open-loop runs (C and D1), identical to the 35 old evaluation runs**
- `03_runbook\packet_main_v03`, CARLA 0.9.15 synchronous at 0.05 s.
- The 32-channel 20 Hz lidar with σ = 0.02 m range noise seeded per sweep.
- CenterPoint `epoch_20.pth` (SHA-256 `59936925…e8ca32`) on ten sweeps at 2 Hz online.
- CANMOT (commit `515d0792…` with its recorded local change), CV EKF at 0.5 s steps.
- The native recording arm with α = β per case.

Exceptions:
- D1 changes the lead's behaviour, through a new and reviewed actor-policy version (§6).
- E changes the ego's controller (fix F2) and its margin arm (§7).

## 2. Definitions

**2.1 Tracker variants and their sources.** For a tracker variant x:
- **N_x**: x's 4 × 4 route-frame position–velocity covariance, projected as N.
- **F0_x**: x's class average P̄_x, the rule of record applied to x's covariances on the 120 tuning runs, used with x's states.
  - For the rate variants of B7, F0_x = P̄ of record.
  - For real logs (§8), P̄_x comes from the design split.
- **E_x, CK3_x, AM_x, NA_x, TG_x**: as of record, on x's tracks.
- **Room and share**: R_x = D(E_x, F0_x) and RR(A_x) = D(A_x, F0_x) / R_x.

For the online tracker of record, x is omitted.

**2.2 E5: rank-matched, amplitude-limited oracles.** For decision i, take the rows r with finite positive g\*_F0,r and g\*_E,r, and form:
- ρ_i,r = (g\*_F0,r / g\*_E,r)^½;
- r_i = median_r ρ_i,r;
- u_i = (rank of r_i − 0.5) / n over the run set's evaluated decisions, with mid-ranks for ties. A decision without such rows gets u_i = 0.5.

Each oracle's critical scales are g\*_F0,r / f_i², with f_i defined per oracle:

| Oracle | Factor f_i | Use |
|---|---|---|
| **E5** | 1.1029 · (1 + 0.05 (2u_i − 1)) | ±5% around the median N/F0 ratio of record (H1, K1) |
| **E5_x**, the amplitude-matched ceiling of variant x | m_x · (1 + A_x (2u_i − 1)) | Ceiling for x's share |
| **E5p, E5p_x** | as E5 or E5_x, with u_i permuted within runs (`default_rng(20261915)`) | Same amplitude, no information |

For E5_x:
- m_x is the median of x's ratio √(s_Nx / s_F0x) at the binding rows of the scored run set;
- A_x = (q₉₅ − q₀₅) / (2 m_x), from the 5% and 95% quantiles of that ratio.

The **ceiling share** is c_x = RR_gl(E5_x) on x's own room. **P** (grid placebo) and the **partial oracles** (25, 50 and 75%; fresh masks `default_rng(20261919)`) are as of record.

**2.3 Frontiers and estimands.** The gridless step frontier (A9-1(c)) is primary for every share; grid and hull are secondary.
- D_gl(A, B) is the summed frontier distance on 201 caution levels; RR_gl(A) = D_gl(A, F0) / D_gl(E, F0); decision-equivalents as of record.
- The per-phase schedule (H4) is on the grid frontier, because its scales are grid values.

**2.4 Phase.** Primary: the tracker's own estimate, as A9-3(b):
- "stopped" if the lead track's speed is ≤ 0.5 m/s;
- "braking" if it is above that and its acceleration along its velocity is ≤ −1.0 m/s²;
- otherwise, or with no lead track, "before braking".

Sensitivities: thresholds −0.5 and −2.0 m/s², and the truth phase.

**2.5 Cut-in event and track age.**
- **Event time t_c:** in each cut-in run, the first truth tick at which the cutting vehicle (the scenario's primary actor) is ahead of the ego and its centre lies within 1.75 m laterally of the ego's lane centre (route frame).
- **Runs without an event:** listed and left out of the event population.
- **Event window:** evaluated decisions with t − t_c ∈ [−1, +4] s.
- **Track age:** decision time minus the birth time of the track matched to the cutting vehicle (matching rule of record). Strata: < 1 s, 1–4 s, ≥ 4 s; "untracked" is counted separately.
- **Young-track population:** decisions in the event window in the < 1 s stratum.

**2.6 Intervals and calibration.** Run (or log, or case) bootstrap; 95% percentile intervals unless calibrated.

**Calibration** of each hypothesis statistic of C and F: a double bootstrap with 2,000 outer resamples (`default_rng(20261912)`) and 1,000 inner (`default_rng(20261913)`).
- If the estimated coverage of the nominal 95% interval is below 0.94, use the smallest nominal level in 0.950–0.9995 (step 0.0005) whose coverage is at least 0.95.
- A calibrated level is used only if two checks hold: its Monte Carlo SD, from 2,000 resamples of the outer samples (`default_rng(20261920)`), is ≤ 0.002; and a repeat with a second inner seed (`default_rng(20261914)`) agrees within 0.002.
- Otherwise use the nominal 99% interval, and say so.

**2.7 Equivalence margin.** δ = 0.05 of the room (author default, §12), on the gridless frontier.
- **Stakes.** At the old room of 5.56 percentage points, 5% is about 0.28 points of decisions.
- **Calibration against known sources.** The NIS-inflated covariance (0.017 on the old runs) lies inside it; the braking prediction (0.83) far outside.
- It is fixed at Lock 1.

## 3. Package B: offline re-tracking and re-analysis on stored data (exploratory)

**Scope.** Package B uses the stored detections, logs, truth and arrays of:
- the 55 lead-braking runs (20 tuning, 35 old evaluation);
- the 120 tuning runs of all six families, which include 20 cut-in runs.

The trackers B1–B4 are tuned on tuning runs only, frozen by Lock 2, and then scored on fresh, closed-loop and real-log data. Code: `revision_v13\analysis\b*_*.py`.

| Ref | Item | Analysis | Consequence rule, fixed now |
|---|---|---|---|
| B0 | Pre-condition | **Identity.** (a) The offline replay of the online tracker (method of `m4_perception_model\tracker_harness_v03.py`) reproduces the logged tracks and actor lists of the 175 runs. (b) Arrays rebuilt from the replayed actor lists reproduce the stored ones (critical scales of F0, N, E, NA, CK3, AM, Q; clearances; selections) | (a) Exact, or within 1e-14 where the pod's math library differs. (b) Within 1e-12. Otherwise B stops until the cause is found and recorded |
| B1 | R2 | **IMM (CV/CA).** Models: B3's CV filter and B4's CA filter; the CV state embedded with zero acceleration and zero acceleration variance. Standard IMM interaction with the spread-of-means term in the combined covariance. Transition matrix per 0.5 s step: diagonal 0.95; initial mode probabilities (0.9, 0.1). CANMOT association and life cycle on the combined prediction. The planner receives the combined 4 × 4 block. Sensitivities: diagonal 0.90 and 0.98 | Old runs, exploratory: print RR_gl(N_IMM), its ceiling c_IMM, the ratio spread, and NIS and NEES by phase. The confirmatory reading comes from H3, K2, E-H3 and F-H2 only |
| B2 | R2 | **Innovation-adaptive Q.** The B3 CV filter with velocity-block process noise Q_v · clip(m, 0.25, 10). m is the mean of NIS/2 (position, 2 dof) over the track's last (at most three) updates. It adapts both ways | Printed beside B1. On fresh runs it is descriptive |
| B3 | R10 | **CV re-tuned so that position NIS is near 2.** (1) The car-class position and velocity terms of R are set to the mean squared detection errors (object frame), from car boxes matched to the nearest true vehicle within 5 m on the same tick, clear view, range ≤ 54 m, **on the 120 tuning runs only**. (2) One scalar κ on all car-class process-noise terms, chosen **on the 20 lead-braking tuning runs** so that the median over runs of the lead track's mean position NIS lies in [1.8, 2.2]: search 10^(−3 + 0.05 j), then bisection on log κ to within 0.01 of 2. If the window cannot be reached, take the nearest κ and report it | For the online CV, B3 and B4, on old (exploratory) and fresh (descriptive) runs: the lag (median of CV-predicted minus true lead position at 3 s in the first second after the stop), room by phase, after-stop room, and RR(CK3) pooled. If under B3 or B4 the after-stop room is below half its online-CV value, or RR(CK3) differs by more than 0.10, the text says these depend on filter tuning and gives both, and the abstract's conditions include filter tuning. Otherwise it says the mechanism persists with NIS near 2 and with a CA filter |
| B4 | R10 | **CA.** CANMOT's CA model for the car class: R from B3 (1); position and velocity process noise from B3; one acceleration term σ_a² chosen by B3's rule (2). Filter class: CANMOT's rotated-noise EKF if it takes the CA model unchanged, otherwise its linear KF (world-frame noise), decided by a code check and recorded in Lock 2 | As B3 |
| B5 | R5, R2 | **E5, E5p and the ceilings E5_x and E5p_x** on the old runs, for N and B1–B4 | Exploratory. The confirmatory readings come from H1 and H3 |
| B6 | R12 | (a) **Terciles** of realised lead deceleration (definition of Table S28, `rev_h_run_facts_v01.py`): runs split into thirds, ties by id. Per tercile, on its own frontier: the reaction-and-stop room at τ = 0.75 s and 6 m/s² relative to its 3 s room. (b) **Delayed, variable stop**: τ_i = 0.75 + δ_i, δ_i ~ U(0, 0.75) s per decision (`default_rng(20261916)`), 6 m/s² | The abstract uses the fresh-run values (§5.7) with the range across terciles and the words "a perfect, free stop independent of perception", unless E's closed-loop braking supersedes that wording (§9). A non-evaluable tercile (den₀ < 10 decision-equivalents) restricts the statement to the evaluable terciles' deceleration range |
| B7 | R13 | **Rate and latency** (pod; fresh runs' kept sweeps, both families). (i) Identity: offline 2 Hz detection at the online ticks reproduces the logged combined-cloud hash and boxes (boxes within 1e-6 m). (ii) Detection at 5 Hz (every 4th frame from k = 19) and 10 Hz (every 2nd), each on the last ten sweeps. (iii) CANMOT at dt = 0.2 or 0.1 s: process noise scaled by dt/0.5 elementwise (sensitivity: unscaled), R unchanged, deletion age in seconds (car 7.5 s). (iv) Latency L: the state from the sweep at time t reaches the planner at t + L; primary 0.1 s, sensitivities 0 and 0.2 s; 2 Hz reference at 0 and 0.1 s. Run p1b_fit_finite_0037 (the one old run with sweeps): descriptive lag statistics only | Fresh runs, each rate × latency: R, after-stop room, RR(CK3), RR_gl(N), lag. If (i) fails, the offline 2 Hz detection is the reference, and the text says so. If at 10 Hz with L = 0.1 s the after-stop room is below half its 2 Hz value, the text says it is largely a consequence of the 2 Hz update, and the abstract gives magnitudes "at 2 Hz without latency" with the 10 Hz value. If RR_gl(N) leaves (−δ, δ) at any rate, H2's statement is qualified to 2 Hz |
| B8 | S13, S16 | **Diagnostics.** (a) After-stop decisions with tracker speed > 0.5 m/s: run-level counts and contributions with intervals. (b) NIS and NEES per phase at update time, truth at the state time, run-level intervals, every tracker variant | Supplement |
| B9 | S14, S15 | **Cut-in development** on the 20 cut-in tuning runs: the event detector of §2.5 (events found, window sizes), track-age strata counts, the ratio N/F0 by stratum and around the event, RR_gl(N) in the event window (exploratory) | If events are found in fewer than 18 of the 20 runs, the lateral threshold may be changed **once**, to 2.5 m, before Lock 2. The decision uses only the event counts, not any score, and is recorded. No other part of §2.5 may change |

## 4. Freeze (Lock 2)

**When.** After B0–B5 and B9, and the builds of D1 (§6), E (§7, through E0) and F (§8, design split only), and before any value of fresh, closed-loop or held-out data.

**What `LOCK_A10_2.txt` records**
- The SHA-256 of every code file and configuration of B1–B4, B7, the D1 actor-policy version and its case file, the E packet and arms, and the F adapter.
- The tuned constants: R terms, κ, σ_a².
- B4's filter class.
- The cut-in threshold.
- The E matched settings (§7.3).
- F's route, split and primary horizon (§8.3).

**Change rules.** No design or constant changes after any value it could be tuned to has been seen. The only exception is a bug fix that meets all of these:
- found by an identity or unit test;
- recorded with before and after values in Table S4;
- made before Lock 2.

## 5. Package C: fresh runs in two families, scored once

**5.1 Runs**
- **Cases.** The never-run evaluation cases of `06_phase0\scenarios\DEVELOPMENT_PROTOCOL_MAIN_v01.json` (SHA-256 `32d683a0…`). For each family (lead braking; cut-in) and each desired speed (5, 10, 15 m/s), take the first 35 cases in ascending id order: 105 lead-braking and 105 cut-in runs. Each case keeps its own seed and noise episode.
- **Recording arm.** Native, α = β, assigned within family and speed in id order by the cycle 1.642374415149816, 5.411894431054339, 7.550302542198003 (the old evaluation runs' values).
- **Jobs.** `pc13_<case>_native`, with `keep_raw = true` for every job.
- **Failures.** A failed job (status not CAPTURED_AND_REVIEWED, a policy failure or a server crash) runs once more in a fresh process. A second failure is replaced by the next unused case of the same family and speed, with the same α; every replacement is reported.
- **Contact runs.** Runs ending at first contact are kept.
- **Job lists.** Built by a variant of `make_main_jobs_v01.py`; the generator is unchanged.

**5.2 Sealing.** On download, a script prints only pass/fail counts, checking:
- each archive's receipt SHA-256, status, frames and keep_raw;
- the number of kept sweeps;
- that each kept noisy sweep's SHA-256 equals its receipt.

Nothing else of a fresh run is computed before Lock 2. B7's detection writes files on the pod and computes nothing else.

**5.3 Lead braking: hypotheses in a fixed sequence**
- Each is one-sided at 0.025, on §2.6 intervals.
- "Confirmed" means it and every earlier one passed.
- Later ones are still computed and labelled "not confirmatory".
- Population: all evaluated decisions; 3 s commitment.

| Ref | Item | Hypothesis | Passes if |
|---|---|---|---|
| H0 | R8 | There is room | R_gl's lower end > 0, and D_gl(E, F0) > 0 in ≥ 97.5% of resamples |
| H1 | R5 | The measure detects rank information at the tracker's amplitude | Lower ends of RR_gl(E5) and RR_gl(E5) − RR_gl(E5p) both > 0 |
| H2 | R6, R8 | N is equivalent to F0 | RR_gl(N)'s interval lies inside (−δ, δ) |
| H3 | R2 | What the IMM's covariance does, against its ceiling | **Classified.** With r = RR_gl(N_IMM) and c = c_IMM (§2.2), each on IMM's own room: (a) "recovers" if r's lower end > 0; else (b) "uninformative variation" if c's lower end > δ (the IMM varies enough for perfect ranking to matter, and does not use it); else (c) "amplitude-limited" if c's interval lies inside (−δ, δ); else (d) "inconclusive". Flag "barely varies" if ≥ 95% of binding rows lie within 5% of the median N_IMM/F0_IMM ratio. Passes with (a), (b) or (c). Under (a) the efficiency r/c is reported with its interval |
| H4 | R7 | The per-phase schedule transfers (§5.5) | The transferred per-phase share on the record basis has a lower end > 0.5 |
| H5 | R11 | The braking prediction recovers most of the room | RR_gl(CK3)'s lower end > 0.5 |

**5.4 Cut-in: hypotheses in their own fixed sequence**
- Population: the event window (§2.5); 3 s commitment.
- The cut-in family supports separate claims, so it has its own sequence, with no adjustment across families. This is stated.

| Ref | Item | Hypothesis | Passes if |
|---|---|---|---|
| K0 | S15 | There is room at the cut-in event | Lower end of R_gl in the event window > 0, and den₀ ≥ 10 decision-equivalents |
| K1 | Contribution 4 | N is equivalent to F0 at the event | RR_gl(N)'s interval inside (−δ, δ) |
| K2 | R2, S14 | What the covariance does on young tracks, where it is not a class constant | In the young-track population, classified as H3 with N and its ceiling E5_N (amplitude A_N measured in that population). Not evaluable if R_gl there is below 10 decision-equivalents: then the text says too few young-track decisions carry room to test it |

Per stratum of track age and per second relative to t_c, RR_gl(N), the ratio spread and the room are descriptive.

**5.5 The per-phase schedule (H4).**
- **Design set:** the 35 old evaluation runs, phases by the tracker's estimate, the 201 caution levels of record.
- **Choice on the design set.** At each level ℓ, the scale triple with the lowest wrong-go among triples whose design caution is at most ℓ. Ties go to the lowest caution, then the lowest index. A single scale is chosen the same way.
- **Transfer.** Both are applied once to the fresh lead-braking runs. With F0's zero-margin point added, they give step frontiers on the fresh runs' own 201 levels.
- **Record basis (primary):** Σ_ℓ (F_F0 − F_ps→C) / Σ_ℓ (F_F0 − F_E), with F_F0 the class average's own grid frontier on the fresh runs.
- **Like-for-like basis:** beside it.
- **Intervals:** fresh-run bootstrap (`default_rng(20261911)`, 20,000), with no re-selection.
- **Sensitivities:** the truth phase; thresholds −0.5 and −2.0 m/s².

**5.6 What may be said to transfer (R9; C9).**
- **Tuning-run intervals.** `default_rng(20261918)`, 20,000 resamples of the 20 tuning runs, for:
  - R and R_gl;
  - the shares of N, NA, AM, CK3 and TG, grid and gridless (TG's tuning-run arrays rebuilt by the A9-7 method with its identity check);
  - the per-phase rooms.
- **The Limits sentence** lists only statements that hold in every run set where they are defined (tuning, old evaluation, fresh, and the held-out real logs of F):
  - RR_gl(N) inside (−δ, δ) at its point estimate;
  - pairwise orderings RR_gl(A) > RR_gl(B) among CK3, AM, TG, NA and N whose point difference is positive in all of those sets.
- Magnitudes are never said to transfer.

**5.7 Fixed sensitivities and descriptive outputs (none is a hypothesis)**
- Grid frontier and placebo: RR(N), RR(P), RR(N) − RR(P), and the convex hull.
- Caution capped at 5, 10 and 15%, and signed caution (S11).
- The reaction-and-stop grid: τ 0.5–1.8 s at 6 m/s²; A = 4, 5 and 7.6 m/s²; 2 m gap; den₀ and RR₀ for every source; B6(a) terciles; B6(b) delayed stop; stop reliance (A9-6).
- After-stop truncation T = 0, 1, 2, 5, 10 and 20 s, and a cut 5 s after the stop (S1).
- **Grading check in every printed population (C3).** The partial oracles must be strictly increasing, with the 25% share above zero. Where it fails, Table II prints decision-equivalents, not shares (S12).
- RR_gl of NA, AM, CK3, TG and Q.
- Variants B2–B4; B1's transition sensitivities; the ceilings E5_x.
- B7 at every rate × latency.
- The margin-ratio check for every variant.
- Cut-in by track-age stratum and relative time.

**5.8 Seeds** (all `numpy.random.default_rng`)

| Seed | Use |
|---|---|
| 20261911 | Fresh-run bootstrap |
| 20261912, 20261913 | Double bootstrap, outer and inner |
| 20261914 | Second inner seed |
| 20261915 | E5 permutations |
| 20261916 | Delayed stop |
| 20261917 | Hand-check subset and the five runs of the second IMM check |
| 20261918 | Tuning-run bootstrap |
| 20261919 | Fresh partial-oracle masks |
| 20261920 | Monte Carlo error of calibrated levels |
| 20261921 | D1 case draws |
| 20261922 | E case bootstrap |
| 20261923 | F log/scene bootstrap |

Old-run analyses use the draw of record, 20261113. Fresh runs use their protocol seeds.

## 6. Package D: non-braking leads and an event-level table

D1 and D2 are **required**; D3 and D4 are optional.

**D1. Leads that do not brake hard (S18, R11, S24).**
- **Variants.** A new actor-policy version (reviewed independently before Lock 2, hash-pinned in a new packet) adds three lead variants. Everything else is the lead-braking generator.
  - (a) **Constant speed:** the lead keeps its initial speed.
  - (b) **Mild braking:** from a start time U(1, 3) s, the lead decelerates at U(0.5, 1.5) m/s² to half its speed, then holds it.
  - (c) **Stop and pull away:** the lead brakes at U(2, 6) m/s² from U(1, 3) s to a stop, holds 3 s, then accelerates at 1.5 m/s² to its initial speed.
- **Cases.** 55 new cases per variant, drawn by `default_rng(20261921)` from the lead-braking draw law for desired speed (cycling 5/10/15), gap and τ. The case file is hashed at Lock 2.
  - The first 35 per variant are recorded as in §5.1 (native arm, α cycle, keep_raw true): 105 runs.
  - The next 20 are E3b's (§7).
- **Scoring.** All sources at their **matched settings from lead braking**: each source's grid scale whose open-loop caution on the old evaluation runs is nearest F0's caution at g = 1 (ties: smaller g). For the phase schedule, its H4 triple at that caution level.

Per variant, the comparisons against F0 at those settings are:
- the difference in caution (percentage points of desired speed);
- the difference in wrong-go share (3 s commitment);
- with run-bootstrap intervals (`default_rng(20261911)`).

| Ref | Hypothesis | Classified as |
|---|---|---|
| D-H1 | The braking prediction's cost behind each variant | "Costs progress" if the caution difference's lower end > 1 point and the wrong-go difference's upper end ≤ 0; "costs safety" if the wrong-go difference's lower end > 0; "no measurable cost" if both intervals lie within ±1 point; otherwise "inconclusive" |
| D-H2 | The phase schedule's cost behind each variant | As D-H1 |

Each variant's two classifications are reported as they fall. No pooling across variants is claimed.

**D2. Event-level table (S19).** On the fresh lead-braking runs, for F0, N, CK3 and TG, at the operating points whose caution is nearest 2% and 5% of the desired speed (each source on its own step frontier), under the 3 s commitment and under reaction-and-stop at τ = 0.75 s:
- the number of runs with at least one wrong go;
- per run, the median closing speed at the first loss of clearance of its wrong-go decisions;
- across runs, the median of those medians.

The table goes in the supplement, with one sentence in Limits.

**D3 (optional; S22).** TG+N and TG+F0 (variances added), RR_gl on fresh runs.

**D4 (optional; S14).** Ratio spread against heading offset and track age in the crossing and benign families, from stored arrays.

## 7. Package E: closed loop in CARLA, staged

**7.1 Ladder and stop rules.** The ladder follows the project's costing (`02_design\PROPOSAL_CARLA_CONFIRMATION_v02.md`). Pods are terminated whenever a repair is needed. The total cap is **$50** unless the author raises it.

| Step | What | Paid | Passes if | Otherwise |
|---|---|---|---|---|
| E0 | Build (free). The controller fix F2 (plant-inverse feed-forward on the acceleration servo, `DESIGN_NOTES_v01.md` §6.4e). A brake-test script. Closed-loop arms F0, CK3, TG, PS and the online IMM pair (zero margin and N exist). A new packet. Laptop checks. An independent code review. A replay identity: the online IMM fed a logged detection stream reproduces B1's offline output within 1e-12 | No | Checks and review pass | Repair; no pod until they pass |
| E1 | **Brake test**: stops from 5, 10 and 15 m/s with F2 | Cap $3; at most two attempts, the second only after a fault, not a result | Stopping distance from the first fallback decision within 10% of the planner's model at all three speeds, **and** no policy failure or halted job (rule pre-set on 10 Nov 2026, §6.4e) | **E stops.** The paper reports that the braking fix did not meet the planner's model in CARLA. The closed-loop statement is then limited to that, and to the simplified-simulator check with its stated limits |
| E2 | **Calibration** (F0 only) on the 30 lead-braking tuning cases (`c1109_tune_0000…0174`, step 6; design data): g ∈ {0, 0.25, 1, 4, 16, 64}, 180 runs | About $5 | — | Sets the levels (§7.3) |
| E3 | **Main runs** on 60 never-run lead-braking evaluation cases: the next 20 per speed after C's, in id order. Arms: Z (zero margin) once, and F0, N, CK3, TG, PS, F0_IMM and N_IMM at levels lo and hi: 900 runs | About $25 | — | — |
| E3b | **Non-braking leads**: the 60 E3b cases of D1. Arms F0, N, CK3, PS and TG at level lo: 300 runs | About $9 | — | — |

**7.2 Arms.**
- **Feasibility rule:** g · s_A ≤ d², d ≥ 0 on every constraint, as in the open-loop sources; the 17 rows and the fallback as the planner; no acceleration-allowance term.
- **CK3:** shifts the predicted path as in v12.
- **PS:** uses the online phase estimate (§2.4) and its triple.
- **The IMM pair:** runs the frozen B1 tracker online; F0_IMM uses P̄_IMM.
- **The controller:** F2 in every arm. Fix F5 (a planner-side stopping check) is **not** applied: the planner's late reaction to a braking lead is part of what is tested.

**7.3 Matched settings, fixed before any closed-loop run.**
- **Levels.** From E2: g_lo is the grid value whose F0 contact share on the tuning cases is nearest 0.20, and g_hi the value nearest 0.05 (ties: smaller g). If every share is below 0.05, g_lo = 0.25 and g_hi = 1, and the contact comparisons are labelled low-power.
- **Other arms.** For every other arm A and level L, g_A,L is the grid scale whose **open-loop** caution on the old evaluation runs (B arrays for the IMM pair) is nearest F0's open-loop caution at g_L. For PS, its H4 triple at that caution level.
- **When fixed.** These values are computed from design data and written into an addendum lock (`LOCK_A10_2b.txt`) after E2 and before E3.

**7.4 Outcomes per run** (from truth, 20 Hz)
- **Contact:** any contact event, or a truth gap ≤ 0.
- **Impact speed:** closing speed along the route at the first contact.
- **Time lost:** run length minus distance travelled divided by desired speed, for runs without contact.
- **Rest gap:** the gap to the stopped lead at the end of the run.
- **Peak deceleration:** the maximum of −dv/dt over a 0.25 s moving average.
- **RMS jerk:** over the run, from the same smoothed speed.
- **Fallback share:** the share of decisions in full braking.

**7.5 Analysis, paired by case, each arm against F0 at the same level** (the IMM pair: N_IMM against F0_IMM)
- **Contact share:** paired difference with a Newcombe hybrid-score 95% interval for paired proportions, plus the exact McNemar test.
- **Time lost:** mean paired difference over pairs without contact, with a 95% case-bootstrap interval (`default_rng(20261922)`, 20,000).
- **Other outcomes:** descriptive, with the same bootstrap.
- **Classification per arm and level:**
  - "safer at no extra cost": contact difference's upper end < 0, and time lost's upper end < 0.5 s;
  - "safer at a cost": contact difference's upper end < 0, and time lost's upper end ≥ 0.5 s;
  - "equivalent": contact difference within (−0.10, 0.10), and time lost within (−0.5, 0.5) s;
  - "worse": contact difference's lower end > 0;
  - otherwise "inconclusive".

| Ref | Hypothesis | Reported as |
|---|---|---|
| E-H1 | CK3 against F0 at lo | Its classification |
| E-H2 | N against F0 at lo | Its classification (expected "equivalent") |
| E-H3 | N_IMM against F0_IMM at lo | Its classification. With either outcome the text states what the IMM's covariance did in closed loop |

Every other arm, level and the E3b variants are reported in the same terms, as descriptive.

## 8. Package F: real-sensor replication (open-loop log replay)

**8.1 Routes.** The author chooses one before Lock 1; this session must not choose for them.
- **F-A, Argoverse 2.** Uses the archive of companion manuscript [9] (`OneDrive\…\<companion manuscript archive>\30_DATA\`, read only):
  - CANMOT (T1) and Poly-MOT (T3, CTRA) tracks with full covariances;
  - detections from the archive's own CenterPoint;
  - 2 Hz truth and 10 Hz ego pose; 375 logs.
  - **Design split:** folds 0–1 (150 logs), already used by the project's exploratory Argoverse 2 pilot.
  - **Held out:** folds 2–4 (225 logs), never read for this question.
  - **Planner:** the archive's speed-only replay planner, as used by the pilot. Magnitudes are therefore not comparable with CARLA; directions and the null are.
  - **Paper change required:** the paper must state the shared data with [9] and drop v12's sentence that none of [9]'s data is used.
- **F-B, nuScenes.** Independent of [9]:
  - CenterPoint detections in `Downloads\nusc_results_flip\` (provenance to be confirmed by the author);
  - annotations and ego poses from the nuScenes v1.0-trainval metadata (downloaded by the author under the nuScenes terms);
  - CANMOT with its released nuScenes configuration, through the offline harness;
  - the CARLA study's planner library through a new adapter: the route is the ego's logged path; truth boxes are interpolated between keyframes.
  - **Design split:** the train scenes; the detector is in-sample there, which is stated.
  - **Held out:** the val scenes.

**8.2 Sources.**
- F0 is the class average of each tracker's covariances on the design split.
- N is CANMOT (T1).
- N_IMM is the frozen B1 tracker run on the route's detections.
- For F-A only, N_T3 (Poly-MOT, existing tracks) is reported as descriptive.
- E, E5, E5_x, CK3, AM and TG are as in §2.

**8.3 Horizon rule** (on the design split only, before Lock 2):
- **3 s** is primary if D(E, F0) at 3 s has a lower 95% end > 0 on the design split.
- Otherwise **2 s**, if that holds there.
- Otherwise F stops and reports "no measurable room on design data at 2 or 3 s".

For F-A, the pilot's design-fold results are already known (room at 2 s, none at 3 s), and the rule is applied to them as recorded. This is disclosed.

**8.4 Population.** All evaluated decisions. Secondary: decisions with an in-path lead vehicle (in-path rule of the route).

**8.5 Hypotheses on held-out data, in a fixed sequence**

| Ref | Hypothesis | Passes if |
|---|---|---|
| F-H0 | There is room on real logs | R_gl's lower end > 0, with fewer than 2.5% of log or scene resamples non-positive |
| F-H1 | N (CANMOT) is equivalent to F0 | RR_gl(N)'s interval inside (−δ, δ) |
| F-H2 | What N_IMM does, against its ceiling | Classified as H3 |

Intervals come from a log or scene bootstrap (`default_rng(20261923)`), calibrated by §2.6.

**8.6 Gating.** Scripts refuse held-out logs or scenes until Lock 2 exists. The design split may be used for the adapter checks, the class averages and the horizon rule only.

## 9. Consequence rules for the text, fixed now

| Outcome | What the abstract, contributions and conclusion say |
|---|---|
| H0 / K0 / F-H0 fails | No measurable room in that data set. Nothing is tested there. If H0 fails, the author is consulted before writing |
| H1 passes / fails | "The measure detects rank information at the tracker's amplitude" / "was not shown to detect information at the tracker's amplitude". In the second case every null is worded "under a measure not shown to detect information at that amplitude" |
| H2, K1, F-H1 pass | "Equivalent to a class-average margin within 5% of the room" in that data set, confirmatory, with decision-equivalents. "Confirmation" is used only for hypotheses that passed in their sequence |
| H2, K1, F-H1 fail | The estimate and interval are given; "equivalent" is dropped; if the lower end exceeds δ, the share recovered is stated |
| H3, K2, F-H2: "recovers" | The covariance-varying tracker recovers r of the room (efficiency r/c of its ceiling). The title and abstract no longer say only that tracker covariances add nothing |
| H3, K2, F-H2: "uninformative variation" | The varying covariance changes enough that perfect ranking at its amplitude would recover c, but it recovers none of it: the bottleneck is the information in the covariance |
| H3, K2, F-H2: "amplitude-limited" | Even perfect ranking at the covariance's amplitude recovers little: this room cannot be carried by a covariance margin of that size |
| H3, K2, F-H2: "inconclusive" or "barely varies" | Said, with the values; the title and contributions name the trackers tested (R2's narrow framing). NA is "output-scalar NIS inflation" in every case |
| H4 passes / fails | Schedule result as a diagnostic of where the room lies, with D1's and E's results on its cost / the value, "not confirmed" |
| H5 passes / fails | The braking prediction recovers most of the room, open loop, on runs where every lead brakes to a stop; its cost behind other leads is D-H1's classification / the value only |
| D-H1, D-H2 | Their classifications are stated beside H5 and H4 in the abstract if any is "costs safety" or "costs progress"; otherwise in §V-D |
| E1 fails | "A closed-loop test was attempted; the braking fix did not meet the planner's model in CARLA", with the brake-test numbers |
| E-H1 to E-H3 | Their classifications. If E-H2 is "equivalent", the abstract's null extends to closed loop. If E-H1 is "safer at no extra cost" or "safer at a cost", the commitment discussion says which open-loop reading closed loop supports. The "perfect, free stop" wording is replaced by the measured closed-loop outcome |
| Always | Old-run numbers appear in the abstract only if labelled exploratory. Every magnitude carries its conditions: rate and latency (B7 rule), filter tuning (B3/B4 rule), lead behaviour (D1), stop assumption (B6, E), recording policy (C9). The abstract and §VII say the result does not justify removing a covariance margin from a deployed stack (S20). The Data Availability statement says the old runs' sweeps were not retained (except p1b_fit_finite_0037) and the fresh runs' are. If F-A is used, the shared data with [9] are stated in §I and the cover letter |

## 10. Verification

**10.1 Recount rule.**
- **(a) Coverage.**
  - Every numeric token in the following passages maps to a generator source key (`DERIVED_v13.json`) with an independent second-program value:
    - the Abstract, §I, §V–VII;
    - the main tables and figure captions;
    - every supplement value those passages cite.
  - Otherwise the value is not printed there; in the supplement it is marked "one program".
  - The comparison file shows 100% coverage or names the gaps.
- **(b) Second programs.** Written in separate sessions from this amendment and the paper's definitions, without reading the first programs, by default on a different model from the writer's. They may share the scoring library, extracted arrays and resample draws; this is stated.
  - **Second IMM implementation.** The IMM (B1) gets a second, separately written implementation. On five fresh lead-braking runs (`default_rng(20261917)`), the combined covariances must agree within 1e-9 relative.
  - **Closed-loop outcomes.** E's outcome extraction gets a second program working from the truth logs.
  - **Real logs.** F's adapter is checked by a second program on 20 design-split decisions: truth clearance of the selected row within 1e-6 m.
- **(c) Agreement.** Counts must be exact; points and interval ends on the same draws within 1e-9; calibrated levels equal. A disagreement stops the work; both versions, the cause and the fix are recorded, and the corrected value is recounted.
- **(d) Order.** The comparison runs after the last first-program output. No value may be computed later unless the recount is extended to it before the build. File times of plans, locks, outputs and comparisons are listed in the supplement. This closes the v12 Table S38 gap.

**10.2 Hand-check subset (S10).**
- **Selection:** 20 evaluated fresh lead-braking decisions (`default_rng(20261917)`), stratified 7/7/6 by truth phase.
- **Check:** the true clearance of F0's selection at g = 1 is computed by a new routine without the scoring library.
- **Tolerance:** within 1e-6 m. The cases are tabulated.

**10.3 Second claim audit of the final text.**
- **Who and when:** after the package is built, a fresh agent audits it against this amendment, by default on a model other than the writer's.
- **What:** every sentence of the Abstract, §I, §V–VII and the main captions, for four things:
  - the number matches its table;
  - the wording follows §9;
  - the confirmatory and exploratory labels are right;
  - no claim exceeds its rule.
- **Output and fixes:** `notes\CLAIM_AUDIT_v13_v02.md`. Every finding is fixed, and every changed sentence gets a delta audit (`v03`).
- **Reporting:** the supplement states that the final text was audited, and by which model.

**10.4 Build checks.**
- The number-source check: zero tokens without a source.
- The identifier check (S7).
- The ARS acronym check.
- The word budget: the build fails if the body exceeds 5,300 words or the supplement 15,000.
- The package manifest records the hash and time of every verification file.

## 11. Deviations

- A departure from this amendment is recorded, with its reason, before its values are computed (Table S4 and the response letter).
- A rule that cannot be applied as written stops the work, and the author is asked.
- A deviation found afterwards is reported as such, with the planned and actual analyses where both can be computed.

## 12. Defaults the author confirms or changes before Lock 1

| Setting | Default | Alternatives |
|---|---|---|
| δ | 0.05 of the room | 0.02; 0.10 |
| Fresh runs per family (C) | 105 (35 per speed) | 70; 150 |
| Latency L; rates | 0.1 s (0, 0.2 s sensitivities); 5 and 10 Hz | 0.15 s; 10 Hz only |
| Process noise with rate | dt/0.5 elementwise | Continuous white-noise-acceleration form |
| IMM transition diagonal | 0.95 per 0.5 s | 0.90; 0.98 |
| H4, H5 thresholds | 0.5 | — |
| Cut-in lateral threshold; window; young-track limit | 1.75 m; [−1, +4] s; < 1 s | — |
| D1 variants and runs | Three variants, 35 + 20 runs each | Two variants |
| D-H thresholds | ±1 point of caution | — |
| E | Run the ladder; cap $50 | Brake test only (E0–E1, cap $3); not run |
| E thresholds | Contact ±0.10; time lost ±0.5 s; F0 contact targets 0.20 and 0.05 | — |
| F route | **Author's choice**: F-A (Argoverse 2 via [9]'s archive) or F-B (nuScenes) | Both; neither (then the paper states the limit) |
| Models for second programs and audits | Different from the writer's | Same, disclosed |
| D3, D4 | Not run | Run |
| Re-simulating the 55 old runs for their sweeps | Not done | Done, accepted only on per-frame SHA-256 identity |

## 13. Model record

- This draft: Claude Opus 5.5 (`claude-opus-5-5`).
- Planned v13 first programs and text: Claude Opus 5.5.
- Second programs, the second IMM implementation, the claim audits and the next ARS review: by default a different model.
- v13's README and AI-use statement name the model for each step.
