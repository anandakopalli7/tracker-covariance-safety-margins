# AMENDMENT 11 to AMENDMENT_10_v13.md: a confirmatory pedestrian-crossing test (X), the IMM re-tune addendum (B1r), the adaptive filter against its permuted twin (Y), and detection dropouts, open loop (DR) and closed loop (E4)

Status: written by the coordinator on 21 Nov 2026 (file created 13:30:44 EST by the laptop clock, before the step-0 file of 13:35:36).
- Locked in two stages (§9):
  - `revision_v13\LOCK_A11.txt` locks everything except §6c and §6d, before any fresh value of X, Y or B1r;
  - `revision_v13\LOCK_A11b.txt` locks §6c (DR) and §6d (E4), before any DR or E4 value or E4 capture.
- Each lock keeps a byte-identical snapshot of this file.

## 0. Approval record

- **Author's approval (21 Nov 2026, relayed by the session "Paper work summary", the session the author talks to):**
  - 13:00: "Tell me what it take to bring it to 8/10 score atleast ... suggest only the things that could concretely increase your confidence score to 8/10."
  - 13:20: "Go ahead, but I cannot give the time you asked me for. Complete the same described work in most effective way. I can give you max 12 hours".
  - The approved plan: step 0 (go/no-go on the crossing tuning runs, $0); a crossing test (if go), open loop only; an IMM re-tune on tuning runs with an open-loop re-score of the fresh lead-braking runs; a readability pass; a fresh mixed-model panel review and one fix round.
- **Why:** Table S28 shows that the margin ratio barely varies in lead braking (99% of rows within 5% of the median) but varies in the crossing families (pedestrian crossing 8.51%, vehicle crossing 4.09%). The paper's one confirmed covariance result is a null in a family where the covariance is close to a class constant. This test asks whether the covariance helps where it does vary. Either answer is reported.
- **Limits as first approved** (superseded below: the cap is now $80, and the cut-off for results is 21:30, §4): $35 of new pod spend for all of it; crossing results recounted by 21:00 EST, 21 Nov, or the text is frozen without them and says so; final package by **01:00 EST, 22 Nov** (unchanged).
- **What needs the author** (through "Paper work summary"): spend above the cap, the title, and any departure from this amendment.
- **Author's decisions after step 0 (relayed by "Paper work summary"):**
  - About 14:05 EST: "change the scenarios how ever you want, I am not particular about braking. The paper has to be strong, for that use whatever scenario is most useful. Don't cut any runs to make it fit within 12 hours. I want all the planned things to be done within 12 hours. That is the task. That way paper stays and aims to be stronger. I want atleast 8.5/10 paper."
    - Relayed as: run pedestrian crossing at full n despite the step-0 no-go (a departure, §2), run Y (§6b), keep the IMM re-tune at full scope (§6), and add the detection-dropout scenario (§6c).
    - Full calibration; no cuts.
  - About 14:15 EST: "Yes, raise to $60". The spend cap for all new pod spend in this sprint is $60.
  - About 14:05 EST by the laptop clock (session times ran ahead): "Yes, I'll top up". This answered "Will you fund the closed-loop test up to $80, topping up RunPod by $25?". **The cap is $80.** The author pays the top-up themselves. E's capture does not start until the balance shows it.

## 1. What does not change

- AMENDMENT_10 and its locks (LOCK_A10_1, LOCK_A10_2, LOCK_A10_2b, LOCK_A10_2c and the erratum), with every rule they fix: definitions (§2), intervals and calibration (§2.6), δ (§2.7), verification (§10), deviations (§11).
- Every v13 value already exported, and every confirmatory reading of A10 (H0–H5, K0–K2, D, E, F). In particular, H3's classification of the IMM, as registered, stays the confirmatory IMM result; the re-tuned IMM (§6) is printed beside it as a disclosed addendum.
- The trackers, constants and scoring library frozen in FREEZE_B and FREEZE_CD (with their addenda) as of this amendment. The crossing test uses them unchanged.
- E's registered results (E1–E3) are unchanged. A new closed-loop set with detection dropouts, E4, is added in §6d.

## 2. Step 0: room on the crossing tuning runs (descriptive design data, $0)

- **Data:** the stored arrays of record of the existing crossing tuning runs: vehicle crossing (22 runs) and pedestrian crossing (51 runs). Online tracker of record; F0 = the P̄ of record; E as of record.
- **Values:** per family, R = D_gl(E, F0) (mean gap and decision-equivalents) with run-bootstrap intervals (`default_rng(20261121)`, 20,000 resamples, runs in name order); RR_gl(N) and, where its inputs exist, RR_gl(E5_N), descriptive; the n needed for a fresh test (plug-in approximation, §2 of the step-0 file).
- **File:** `work\B_retrack\out\step0\STEP0_CROSSING_v01.json` (13:35:36 EST), SHA-256 `1d0322910e072657e5fdaaaa89f2d82a73f028ae879ad2f6baa82b6822e06610`, code `work\B_retrack\code\b_step0_crossing_v01.py`.
- **Run sets.** The stored runs of the two families are 20 tuning runs each (protocol p2, arm "fixed") plus earlier "fit" runs (phase p1b, arm "native"): vehicle crossing 2, pedestrian crossing 31. The go rule was applied to all stored runs (22 and 51), the sets named in the approved plan; tuning-only values are beside it in the file.
- **Outcome under the go rule (coordinator, 21 Nov about 13:45 EST): neither family is go.**
  - Vehicle crossing (22 runs): R_gl = 0.144 pp, 95% interval [0.000, 0.334]; the lower end is 0, not > 0 (D_gl(E, F0) > 0 in 87% of resamples).
  - Pedestrian crossing (51 runs): R_gl = 0.080 pp, 95% interval [−0.055, 0.250].
  - Beside it, not used by the rule: pedestrian tuning runs alone (20), R_gl = 0.185 pp [0.048, 0.342]; vehicle tuning runs alone (20), [0.000, 0.347].
  - So, by §0's plan, no fresh crossing run is captured unless the author decides otherwise. That would be a departure recorded here before any fresh value.
- **Departure, by the author (about 14:05 EST, before any fresh crossing run existed): pedestrian crossing is tested despite the pre-stated no-go.** The text says: "the author chose to test pedestrian crossing despite the pre-stated no-go of step 0". Vehicle crossing is not tested.
- **Go rule (fixed before the step-0 values were read by the coordinator):** a family is **go** if its step-0 R_gl has a 95% interval with a lower end > 0. If neither family is go, X is not run, no fresh crossing run is captured, and the text reports the step-0 room descriptively.
- **Family choice (as first written):** among go families, the one with the smaller n needed for X0 at 80% power is run; both are run if both are go and the larger n needed is ≤ 200 runs per family. With neither go, the author's departure above decides it: pedestrian crossing only, at the full-basis n (§3.2).
- Step-0 values are exploratory (stored runs). Any that are printed are recounted by a second program (§8).
  - **Done:** Claude Sonnet 5.5, `work\shared\checks\step0_recount\` (`STEP0_RECOUNT_v01.json` 548cd81c…4493; `STEP0_COMPARE_v01.json` b321711f…e35a: 156 of 156 agree; `A_RECOUNT_S0.json` 9c23f698…6769, 45 keys: 57 of 57 agree with `A_EXPORT_S0.json` 2e94463c…).

## 3. X: fresh crossing runs, scored once (open loop)

**3.1 Cases.** The never-run evaluation cases of `06_phase0\scenarios\DEVELOPMENT_PROTOCOL_MAIN_v01.json` (SHA-256 `32d683a0…`) for the chosen family or families, by A10 §5.1's rule: per family and desired speed, ascending id, an equal number per speed. Each case keeps its own seed and noise episode. The recording arm is native, with α = β assigned within family and speed in id order by A10 §5.1's cycle. If a family has too few never-run evaluation cases, the protocol's own generator extends it by a documented seed rule, with a no-overlap check against every earlier case.
- **As built (session CD, 21 Nov about 14:14 EST):** `work\CD_capture\crossing\CASES_X_PC_v13.json`, sha256 `58902be5ce022b314148308140cb8fc9373bc7aee401531367d456755409a31e`, made by `make_cases_x_pc_v13.py`.
  - The protocol holds 102 / 101 / 97 never-run pedestrian-crossing evaluation cases at 5 / 10 / 15 m/s (300). None was ever run; this was checked against 526 earlier ids.
  - To reach 135 per speed (130 plus 5 reserves), the protocol's own generator is continued, unchanged, past its last evaluation index 1799: index i, family FAMILIES[i % 6] (pedestrian when i % 6 = 2); `SAMPLER_C1109_v01.draw(i, family, role='eval', consumer='finite')`; seed = int(sha256("C1109/eval/finite/<i>")[:8], 16); id `c1109_eval_<i>`. Pedestrian indices are taken in ascending order, each joining its drawn speed's pool until that speed has 135.
  - That uses 105 extension cases (indices 1802–2534); 18 cases drawn for an already-full speed are listed and unused. The replica reproduces all 1,800 protocol evaluation cases exactly.
  - Order: per speed, protocol cases in ascending id, then extension cases in ascending index. Positions 0–389 are the study runs (130 per speed: 300 protocol, 90 extension); 390–404 are the reserves (all extension).
  - Packets: protocol cases on `packet_main_v03` (unchanged). Extension cases on `packet_x_v13` (tar a949f1e5…), built as D1's was: packet_main_v03 with only the smoke protocol slot replaced by `DEVELOPMENT_PROTOCOL_X_v13.json` (c0e97c1d…), which is the main protocol plus the 105 extension cases appended. No code changed.
  - GPU: RTX 4090 had no stock, so L4 or RTX 4000 Ada pods are used. Their runs count as study runs only if C's admission and control-run identity checks pass bit-identically on that pod.
- **Freezes:**
  - The X core (extractor, X0–X2, record E5 descriptive, counts, ratio check), case file, packet and jobs, in `FREEZE_CD_add3` before LOCK_A11.
  - The §3.6 descriptives and Y's code with their second programs, in `FREEZE_CD_add4`, before their first run.
- **Calibration:** the second inner seed runs only where A10 §2.6 needs it, i.e. where a calibrated level would be used.

**3.2 Run counts.** Pedestrian crossing only: **n = 390** runs (130 per desired speed), **n_min = 332** (85% of n), and 15 reserves. Basis: step 0's plug-in power on all 51 stored runs, about 84% at n = 390 for X0 on a 95% interval (simulation, `STEP0_CROSSING_v01.json`).
- Failures: A10 §5.1's rule (one retry in a fresh process; a second failure is replaced by the next unused case of the same family and speed, same α; each replacement reported). Contact runs are kept.
- **Capture deadline: 18:30 EST, 21 Nov.** The analysed set is the n listed cases (with their replacements) that are CAPTURED_AND_REVIEWED by then. If it holds fewer than n_min runs, X for that family is reported as **descriptive, under-run**, and none of its hypotheses is called confirmatory.
- Job naming as C (`pc13x_<case>_native`). Capture and review settings as C. Sweeps are not kept unless session B needs them for re-tracking (no rate or latency analysis is planned for X).

**3.3 Sealing.** Capture may start before the lock. On download, a script prints only pass/fail counts, as A10 §5.2. Nothing else of a fresh crossing run is computed or read before LOCK_A11.

**3.4 Scoring.** Only the online tracker of record (N, with F0 = the P̄ of record), from session CD's frozen extractor applied to the logged online tracks, as for C's N. No offline tracker variant (B1–B4) is scored on crossing runs: in the library they change only the car-class filter, and pedestrians are tracked by CANMOT's default filter in every variant. Population: all evaluated decisions; 3 s commitment. Definitions: A10 §2 unchanged (N, F0, E; gridless step frontier on 201 caution levels; decision-equivalents as of record).

**3.5 Hypotheses, a fixed sequence per family.** Each is one-sided at 0.025 on A10 §2.6 intervals. "Confirmed" means it and every earlier one passed; later ones are still computed and labelled "not confirmatory". If both families are run, each has its own sequence, with no adjustment across families, and this is stated (as for cut-in, A10 §5.4).

| Ref | Hypothesis | Passes if |
|---|---|---|
| X0 | There is room on fresh crossing runs | R_gl's lower end > 0, and D_gl(E, F0) > 0 in ≥ 97.5% of resamples |
| X1 | The measure detects rank information at the tracker's amplitude in this family | Lower ends of RR_gl(E5_N) and RR_gl(E5_N) − RR_gl(E5p_N) both > 0 |
| X2 | What the covariance does where it varies, against its amplitude-matched oracle | **Classified** by A10 H3's rule, with r = RR_gl(N) and c = c_N = RR_gl(E5_N): (a) "recovers" if r's lower end > 0; else (b) "uninformative variation" if c's lower end > δ; else (c) "amplitude-limited" if c's interval lies inside (−δ, δ); else (d) "inconclusive". Flag "barely varies" if ≥ 95% of binding rows lie within 5% of the median N/F0 ratio. Passes with (a), (b) or (c). Under (a), the efficiency r/c is reported with its interval |

- **E5_N, not E5.** A10's E5 uses ±5% around the lead-braking median ratio of record (1.1029). That band is lead braking's amplitude, not the crossing tracker's. So X1 and X2 use E5_N, the amplitude-matched oracle of A10 §2.2: m_N is the median of N's ratio √(s_N / s_F0) at the binding rows of the family's fresh runs, A_N = (q₉₅ − q₀₅) / (2 m_N), and E5p_N permutes u within runs.
- δ = 0.05 of the room (A10 §2.7), on the gridless frontier.

**3.6 Fixed descriptive outputs (none is a hypothesis).**
- RR_gl(N)'s interval against (−δ, δ), reported as a value (no equivalence claim beyond what X2 says).
- The margin-ratio check (share of binding rows within 5% of the median) on the fresh runs.
- E5q_N, sensitivity: f_i = N's empirical ratio quantile at u_i (the full amplitude distribution with perfect ranking), RR_gl(E5q_N) and RR_gl(N) − RR_gl(E5q_N).
- Grid frontier: RR(N), the grid placebo RR(P), RR(N) − RR(P).
- Grading check (A10 §5.7, C3): partial oracles (25, 50, 75%) strictly increasing, the 25% share above zero; where it fails, decision-equivalents are printed, not shares.
- Counts: runs, evaluated decisions, contact runs, replacements.

**3.7 Intervals and seeds** (all `numpy.random.default_rng`).

| Seed | Use |
|---|---|
| 20261121 | Step-0 stored-run bootstrap |
| 20261911 | X fresh-run bootstrap (20,000), as C |
| 20261912, 20261913 | X double bootstrap, outer (2,000) and inner (1,000), as C |
| 20261914 | X second inner seed, as C |
| 20261915 | X E5p_N permutations, as C |
| 20261919 | X partial-oracle masks, as C |
| 20261920 | X Monte Carlo error of calibrated levels, as C |

(The draft first listed new seeds 20261924–20261930. At about 14:10 EST, before any fresh value, they were changed to C's seeds so that session CD's frozen C code paths are reused unchanged. The data set differs, so the draws are not shared with C's analysis.)

- Calibration: A10 §2.6 exactly, with these seeds, for both programs (the author: no cuts). **Emergency rule only:** if a statistic's calibration has not finished by 21:15 EST, its nominal 99% interval is used, and the text says so.

**3.8 Consequence rules for the text (as A10 §9).**

| Outcome | What the abstract, contributions and conclusion say |
|---|---|
| Neither family is go at step 0 | "On the crossing tuning runs there was no measurable room, so no crossing test was run", with the step-0 values, exploratory |
| X0 fails | No measurable room on fresh crossing runs; nothing is tested there |
| X1 passes / fails | As A10 §9 for H1, naming the crossing family |
| X2 "recovers" | The covariance recovers r of the crossing room (efficiency r/c). The title, abstract and contributions no longer say only that tracker covariances add nothing |
| X2 "uninformative variation" | The covariance varies enough in crossing traffic that perfect ranking at its amplitude would recover c, but it recovers none of it: the bottleneck is the information in the covariance, not its amplitude |
| X2 "amplitude-limited" | Even perfect ranking at the covariance's amplitude recovers little of the crossing room |
| X2 "inconclusive" or "barely varies" | Said, with the values |
| Fewer than n_min runs kept, or not recounted by the cut-off (21:30 EST, §4) | "A crossing test was pre-registered (A11) [and run]; its results [were under-run / were not recounted by the freeze and are not reported]" |
| Always | X is open loop on simulated crossing traffic, with the tracker of record; magnitudes carry the conditions of A10 §9's "Always" row that apply (rate and latency, filter tuning, recording policy) |

- **Title rule.** The title names crossing traffic only if X0 passes in at least one crossing family, i.e. the covariance was tested where there is room. The same rule applies to detection dropouts: they are named only if DR0 passes, or if E4's lo comparison is reported (closed loop needs no room test). This is option 3's principle (name what was tested), applied as for cut-in (K0) and nuScenes (F-H0), which showed no room and are not named. Otherwise the option-3 title of 21 Nov 13:01 stands. With crossing: "Do Fixed-Noise and Interacting-Multiple-Model Tracker Covariances Improve Planning Decisions? An Equal-Caution Test on Simulated Lead Braking and Crossing Traffic, Open and Closed Loop" (session A's proposal, the author's example). The author confirms both the rule and the wording through "Paper work summary".

## 4. Cut-off

- Results of X, Y, B1r and D, each with its second-program recount, are targeted for **21:00 EST** and must be complete by **21:30 EST, 21 Nov** (moved from 21:00 when the scope grew at about 14:15). Otherwise the text is frozen without that result, by §3.8's row or its own section's rule.
- A partial result is not printed: either the family's whole sequence is recounted by the cut-off, or none of it is printed.

## 5. Spend and network

- At most **$80** of new pod spend for everything in this amendment. The author raised it from $35 to $60, then to $80 (§0).
- No pod may run while the RunPod balance would fall below about $15. The coordinator's watchdog alerts below $20. Every pod is logged in `SPEND_LOG_v13.csv` and deleted as soon as its share is verified (a delete counts only when the pod is gone from the list).
- Before a large upload, the coordinator asks "Paper work summary" to lower the OneDrive cap to 1 MiB/s.

## 6. B1r: the IMM re-tune addendum (open loop, lead braking)

- **Why:** B4's acceleration term σ_a² (used by the IMM's CA mode) did not reach its NIS window. On the grid 10^(−3 + 0.05 j), j = 0…120, the median NIS fell monotonically from 1.634 at the grid's low end (σ_a² = 0.001; `B_retrack\out\b3\B3_TUNE_SIGMA_A2_v01.json`, `window_reached: false`), so the nearest value was taken. The IMM's CV mode (B3) reached its window (κ = 0.16788, median 1.994).
- **Window criterion (unchanged, A10 B3 rule (2) as frozen in `b3_nis_tune_v01.py`):** on the 20 lead-braking tuning runs, the median over runs of the CA filter's lead-track mean position NIS lies in [1.8, 2.2]; target 2.
- **Stage 1 (σ_a² widened downward):** σ_a² = 10^(−3 + 0.05 j) for j = −1, −2, …, −120 (down to 1e−9), visited from the old grid's end downward. Take the first sign change of (median − 2), then bisect on log σ_a² until |median − 2| ≤ 0.01. κ stays frozen. The constants go into a new constants file passed to the frozen library; no library change.
- **Stage 2 (only if stage 1 finds no sign change):** σ_a² stays at its frozen value (0.001). A new, additive library constant κ_CA multiplies only the CA filter's position and velocity process-noise terms. When κ_CA is absent the library must reproduce the frozen B4 and B1 outputs bit-identically on the 20 tuning runs (identity test before any search). Search κ_CA = 10^(−0.05 j), j = 0…120, then bisect on log κ_CA as in stage 1. The library addition and its identity test are frozen in a FREEZE_B addendum before the search.
- **If neither stage reaches the window:** the nearest value from stage 2 is used, and the text says that the window was not reachable for this filter class.
- **Outcome (tuning runs only, session B, 21 Nov):**
  - Stage 1: no sign change down to 1e−9; the median plateaus at 1.6663 (`B4_TUNE_STAGE1_v02.json`).
  - κ_CA identity: 44 of 44 bit-identical (`KCA_IDENTITY_v02.json`).
  - Stage 2 reached the window: κ_CA = 0.6401032024709309, median NIS 1.9978.
  - Constants `B_retrack\out\b3\B1R_CONSTANTS_v02.json` (28b2e9da…). Frozen with the B1r code and second programs in `locks\FREEZE_B_add8.json` (9c87f029…b751; layered 220 of 220, 14:07 EST).
  - P̄_B1R is frozen as data addendum add9 before any fresh re-score.
- **F0 for the re-tuned IMM:** its own P̄ on the 120 tuning runs (A10 §2.1).
- The new constants are frozen as a FREEZE_B addendum before any fresh value under them.
- **Cut-off:** as §4. The B1r values and their second program, including the second IMM implementation's check on A10 §10.1(b)'s five runs with the new constants, must be complete by 21:30 EST; otherwise B1r is not printed, and the text says the re-tune was not completed.
- **Re-score:** the fresh lead-braking runs, open loop, with the re-tuned IMM: RR_gl(N_IMMr), its amplitude-matched oracle c_IMMr (the coordinator's wording decision of 19 Nov 20:15: E5-type oracles are not ceilings or bounds) and H3's classification applied to them, on the IMM-r's own room. These are printed beside the old IMM values as a **disclosed addendum**: the re-tune was decided after the fresh results were seen, although it uses tuning runs only. H3's registered classification stays the confirmatory IMM result.
- No closed-loop rerun; E-H3 is unchanged.

## 6b. Y: the adaptive filter against its own permuted twin (fresh lead-braking runs)

Proposed by "Paper work summary" at about 13:55 EST as a $0 substitute, and approved by the author at about 14:05 EST (§0). Nothing in this section is computed before LOCK_A11.

- **Question.** Does the innovation-adaptive filter's covariance (B2) carry rank information, beyond its amplitude distribution? Its share on the fresh lead-braking runs, RR_gl(N_B2), is already exported. The comparison below is not.
- **Disclosure (fixed now).** Y was specified after these fresh B2 values had been exported and seen: RR_gl(N_B2), B2's amplitude-matched oracle, and the pooled spread of B2's margin ratio (B.AQ.*). No permuted or per-decision-factor value of B2 on fresh runs existed when Y was written (session B, 21 Nov about 13:50; on old runs only: E5p_B2 in `B_B2_v01.json`, and E5q_B2, post hoc). The text states this.
- **Who.** Session CD computes Y from session B's frozen B2 arrays (`B_retrack\out\retrack_fresh\B2\<run>_arrays.npz`, 105 files, hashed in `locks\FREEZE_B_add7.json`, sha256 `d06cc48bbe89ec87b3927c962c041b31b5e7aab1dccbe570188a331e0a7b0c12`, verified layered 204 of 204) with CD's frozen gl_fast, on a CPU pod. The second program is by Claude Sonnet 5.5, from this text.
- **Data.** The 105 fresh lead-braking runs; B2's frozen arrays (B's Table III fresh re-tracking, FREEZE_B); all evaluated decisions; 3 s; gridless frontier; on B2's own room (F0_B2, E_B2; A10 §2.1).
- **B2's factor per decision.** f_i = median over rows r with finite positive g\*_F0B2,r and g\*_NB2,r of (g\*_F0B2,r / g\*_NB2,r)^½. Decisions without such rows keep their own scales; no binding row means no selection can change.
- **Permuted twin B2p_k.** For k = 1…K (K = 20; `default_rng(20261931)`, drawn once, before any value), permute f_i among each run's decisions that have a factor. Critical scales are g\*_F0B2,r / f_π(i)². RR_gl(B2p) is the mean of RR_gl(B2p_k) over k, on the same resample.
- **Statistic.** Δ = RR_gl(N_B2) − RR_gl(B2p), on the fresh-run bootstrap (`default_rng(20261911)`, 20,000; the C draw).
- **Y1 (confirmatory, its own sequence).** "B2's covariance carries rank information beyond its amplitude": passes if Δ's lower end > 0.
  - The interval is calibrated by A10 §2.6 (both programs, on CPU pods; session B estimates about 25–30 vCPU-hours), with the twins redrawn identically inside every resample: the permutations are fixed per run, not per resample. Emergency rule as §3.7. (Set to nominal 99% at about 13:46 to save cost; restored at about 14:15 after the author's "no cuts" and the cap raise, before any value.)
- **Beside it (descriptive).**
  - The scaled, unpermuted twin B2s (f_i in place), and Δs = RR_gl(B2s) − RR_gl(B2p): the same comparison without B2's small row-shape differences.
  - RR_gl(B2p) itself.
  - The same twin construction for the online tracker N: it barely varies, so its Δ is expected near 0. This is a reference, not a test.
- **Consequence rules.**
  - Passes: "the adaptive filter's covariance carries rank information on fresh runs (its share exceeds that of the same margins in random order)", with Δ and the interval. The fixed-noise tracker's covariance is a class constant there.
  - Fails: "no rank information beyond its amplitude was shown", with Δ and the interval.
  - In both cases RR_gl(N_B2)'s size is stated (small), and the result is not extended beyond lead braking.
- **Verification.** A Sonnet second program per §8; the comparison before the build.
- **Cut-off.** 21:30 EST, as §4.

## 6c. DR: detection dropouts on the fresh lead-braking runs (open loop) — locked by LOCK_A11b

Proposed by "Paper work summary" and approved in scope by the author (§0); owner session F. The name is DR (hypotheses DR0–DR2), because A10 already has a package D. Nothing of DR is computed on fresh runs before LOCK_A11b.

**Coordinator's decisions binding on DR and E4 (§6d):**
- **Output rule under dropouts (coordinator's decision, about 14:15 EST, on session E's build finding).** The pipeline of record outputs an unmatched track only while time_since_update ≤ punish_num = 1 (CANMOT `nusc_tracker.py`, `output.punish_num`). In a 2–3-tick window the lead would then be absent from the planner's actor list, and no margin could act. For D and §6d, **all arms use punish_num = 3** (the longest window), so the planner receives the tracker's predicted states through every window. This is a pre-registered configuration departure for D and §6d only, and the text states it. Side effect: natural detector misses of up to 3 updates are also coasted, the same in every arm. Checks:
  - the empty-mask identity check runs with punish_num = 1 and must reproduce the stored arrays of record;
  - a descriptive reference, punish_num = 3 with empty masks (room, RR_gl(N)), separates the output rule's effect from the masks'.
  - F0_D's class average is computed under the same configuration (punish_num = 3, masks) on the tuning runs.
- **One mask law for D and §6d (final wording, about 14:00 EST by the laptop clock; F's and E's code must implement exactly this):**
  - Seed per run: `rng = numpy.random.default_rng(int.from_bytes(hashlib.sha256(("A11/D/" + case_id).encode()).digest()[:8], "big"))`. This is the same integer as `int(hexdigest()[:16], 16)`. case_id is the protocol case id string, e.g. `c1109_eval_0480` or `c1109_tune_0000`, never a job or archive name.
  - Rows: the run's 2 Hz detector update ticks, in logged order, i = 0, 1, 2, …. Row 0 is never masked, so tracks start.
  - From row 1 on, at each row not inside a window, draw u = rng.random(). If u < 0.10, draw L = rng.integers(1, 4), uniform on {1, 2, 3}, and mask rows i … i+L−1. A window is cut at the run's end. Rows inside a window draw nothing.
  - **The row right after a window is never masked and draws nothing.** Draws resume at the row after it. So every masked stretch is 1–3 rows (0.5–1.5 s), as designed, and punish_num = 3 covers every stretch.
    - Added at about 14:08 EST by the laptop clock, before any value. Session E found that under the first wording windows could follow back to back: stretches of up to 7 rows in the 60 E3 cases, from the masks alone, which depend on no outcome.
  - On a masked row the detector's output is replaced by an empty detection list at its logged time; the tracker only predicts.
  - The mask depends on the case only, never on any outcome. Mask files for every run used are written and hashed in LOCK_A11b.

**Session F's specification, merged verbatim** from `work\F_dropout\A11_6c_DROPOUT_SPEC_v02.md` (sha256 `446381f221050d6c8689e75a240585ce06705ec013d52fe2d0e405cb9b3cb14f`); headings demoted one level, nothing else changed. Where it and the decisions above differ, the decisions above govern.

**6c.1 Why.** In lead braking the online tracker's covariance is close to a class constant (Table S28: 99% of margin ratios
within 5% of the median), and there is room. In the crossing families it varies, but there is little room (§2). Under detection
dropouts the covariance grows with the time since the last update, which plausibly tracks the real error. DR asks, in one
scenario with room, whether a covariance helps when it carries information. Either answer is reported. The name is DR, with
hypotheses DR0–DR2, because A10 already has a package D and a seed labelled "D1 case draws".

**6c.2 Runs and logs (no new capture).**
- **Fresh runs:** the 105 fresh lead-braking runs of C: `CD_capture\CASES_C_v13.json` lead-braking cases with
  `REPLACEMENTS_C_v13.json` applied, ids `pc13_<case>_native`, ascending. Logs as stored: `CD_capture\runs\<id>\<id>\capture\<case>\`.
- **Tuning runs (for P̄ only):** the 120 tuning runs of record (rows with `set == tune` and `use == 1` in
  `09_redesign\m4_perception_model\run_index_m4_v02.csv` of programme P, read-only), all six families.

**6c.3 The dropout tracker (DR).**
- **Tracker:** the online tracker of record (variant CV0, constants and configuration of record), through the frozen library
  `shared\trackers\trk_tracker_v01.retrack_capture`.
  - It is fed the logged detector frames as `det_rows`: the rows of `detections.jsonl` in logged order and at logged times. dt is 0.5, latency 0.
  - A decision at tick k uses the last frame with k_frame ≤ k, which with the logged rows is the frame of record, kd = 19 + 10⌊(k − 19)/10⌋.
- **A masked frame** keeps its index, time and tick, and its detector output (`model`) is replaced by the empty list. CANMOT's
  loader then flags the frame `no_dets` (`keep_num == 0`), and the tracker predicts every track and updates none, through its own
  empty-frame path (`tras_punish`).
- **Output rule (§6c's "Output rule under dropouts"):** the configuration of record with `output.punish_num = 3` (record: 1,
  `contracts\tracker_config.json` line 104) in every DR source. It is passed to the frozen library as `base_cfg`; no library file
  changes.
  - CANMOT outputs a track that missed its update only while time_since_update ≤ punish_num (`nusc_tracker.py` line 380). With 3,
    the coasting lead is output with its predicted covariance on every masked frame.
  - Tracks are deleted when time_since_update ≥ max_age (`nusc_life_manage.py` line 46). For cars (CANMOT class 2,
    `NUSC_CONSTANT.py` line 15) max_age is 15 frames (7.5 s; `contracts\tracker_config.json` line 78, in the block on lines 75–83), so no
    window of 1–3 frames deletes the lead.
  - Side effect: natural detector misses of up to 3 frames are also coasted, the same in every source.
- **Observed behaviour, recorded before any value:**
  - While coasting, a car track's score is multiplied by the class decay rate 0.2 per missed frame (`tracker_config.json` line 97;
    `nusc_score_manage.py` line 56).
  - On the frame after a window the detection can re-associate as a NEW track id, which starts with a birth covariance.
  - Both are counted descriptively (§6c.7).
- Everything else in the pipeline is unchanged: the planner rows, the decision ticks and the ego's logged motion (open loop).

**6c.4 Masks: the one mask law, shared with §6d (independent of truth and of every outcome).**
- **Seed per run:** `rng = numpy.random.default_rng(int.from_bytes(hashlib.sha256(("A11/D/" + case_id).encode("utf-8")).digest()[:8], "big"))`.
  This is the same integer as `int(hexdigest()[:16], 16)`.
  - case_id is the protocol case id, never a run, job or archive name.
  - Fresh run `pc13_<case>_native` → `<case>`, e.g. `c1109_eval_0012`.
  - Tuning run → the run index's `case_id`, e.g. `p2_c1109_tune_0000_fixed_c1` → `c1109_tune_0000`.
- **Rows:** the run's detector frames, the rows of `detections.jsonl` in logged order, i = 0 … n − 1, the first at k = 19. Row 0 is
  never masked, so tracks start.
- **Draws:** from row 1 on, at each row not inside a window, draw `u = rng.random()`. If u < 0.10, draw `L = rng.integers(1, 4)`
  (1, 2 or 3 rows, 0.5–1.5 s) right after u, and mask rows i … i + L − 1, cut at the run's end.
- **Gap row:** the row right after a window is never masked and draws nothing; draws resume at the row after it (i += L + 1).
  Otherwise i += 1. Every masked stretch is 1–3 rows, which punish_num = 3 covers.
- **Mask file:** `work\F_dropout\masks\DR_MASKS_v02.json` (code `work\F_dropout\code\dr_masks_v02.py`). It gives, for each of the
  225 runs, case_id, n and the masked rows.
  - It is written and hashed before LOCK_A11b.
  - Longest masked stretch: 3 in both the fresh and the tuning runs.
  - It reproduces §6d's mask table `E_closedloop\out\E4_MASKS_v01.json` on all 61 of E's cases (seed and mask).

**6c.5 Sources and arrays.**
- **P̄_DR:** the P̄ rule of record (A10 §2.1; `ol_pbar_v01` as `trk_arrays_v01.pbar_accumulate`, combined as sum over runs / count per
  class) applied to the DR tracker's outputs on the 120 tuning runs under their masks, with punish_num = 3.
- **Arrays per fresh run:** the frozen builder `trk_arrays_v01.overlay` / `extract` (`lead=True, a4=True`) on the DR tracker's overlay,
  with P̄ = P̄_DR. Each run gives:
  - `cF0` → **F0_DR**, `cE` → **E_DR** (the true error of the DR estimate), `cN` → **N_DR**;
  - clearances, the fallback row and the evaluated mask as the builder gives them.
  - A second extract of the same tracker output with the P̄ of record gives **F0rec_DR**, for §6c.7 only.
- **The amplitude-matched ranking oracle and its permuted twin (A10 §2.2, frozen `shared\trackers\trk_score_v01`):**
  - u = `e5_u(runs, 'F0_DR', 'E_DR')` over the 105 runs' evaluated decisions.
  - m_DR and A_DR are the median and (q95 − q05)/(2 · median) of `margin_ratios(runs, 'N_DR', 'F0_DR')`, i.e. of √(g\*_F0 / g\*_N) over
    the evaluated decisions' rows with both finite and positive, pooled.
  - **E5_DR** = `add_oracle(F0_DR, m_DR, A_DR, u)`.
  - **E5p_DR** = the same with `permute_u(runs, u)`: `default_rng(20261915)`, runs ascending, one permutation per run among its evaluated
    decisions.
  - c_DR = RR_gl(E5_DR) is the amplitude-matched oracle's share. E5-type oracles are ranking oracles at a given amplitude, never
    ceilings or bounds (coordinator's wording decision of 19 Nov 20:15).

**6c.6 Hypotheses in their own fixed sequence.**
- **Population and frontier:** fresh runs, all evaluated decisions, 3 s commitment, gridless step frontier on 201 caution levels
  (A10 §2.3), scoring library of record.
- **Test level:** one-sided at 0.025, i.e. the lower end of the two-sided interval at the level A10 §2.6 gives. δ = 0.05 (A10 §2.7).
- **Intervals:** the fresh-run bootstrap of record (`default_rng(20261911)`, 20,000 resamples, `optA_lib_v02.boot_counts`, runs
  ascending: C's draw).
- **Calibration (A10 §2.6) of each hypothesis statistic:** 2,000 × 1,000 (`20261912` / `20261913`), checks `20261914` and `20261920`.
- "Confirmed" means it and every earlier one passed; later ones are still computed and labelled "not confirmatory".

| Ref | Hypothesis | Passes if | Statistics calibrated |
|---|---|---|---|
| DR0 | There is room under dropouts | R_gl = D_gl(E_DR, F0_DR) has a lower end > 0, and D_gl(E_DR, F0_DR) > 0 in ≥ 97.5% of resamples (as H0) | R_gl |
| DR1 | The measure detects rank information at the DR tracker's amplitude | Lower ends of c_DR = RR_gl(E5_DR) and of RR_gl(E5_DR) − RR_gl(E5p_DR) both > 0 | c_DR; the difference |
| DR2 | What the DR covariance does, against its amplitude-matched ranking oracle | **Classified** as H3, with r = RR_gl(N_DR) and c = c_DR on DR's own room: (a) recovers if r's lower end > 0; else (b) uninformative variation if c's lower end > δ; else (c) amplitude-limited if c's interval lies inside (−δ, δ); else (d) inconclusive. Flag "barely varies" if ≥ 95% of binding rows lie within 5% of the median N_DR/F0_DR ratio. Passes with (a), (b) or (c); under (a) r / c with its interval at r's level | r (and c) |

**6c.7 Descriptive (no hypothesis; nominal 95% percentile intervals on the same draw).**
- **In-dropout population:** evaluated decisions whose frame is masked, with its count by age (1, 2, 3 frames), R_gl, RR_gl(N_DR)
  and c_DR there.
- **In-dropout plus gap row:** the same population with the gap row added, with R_gl, RR_gl(N_DR) and c_DR there.
- **Re-association:** among in-dropout decisions and, separately, gap-row decisions:
  - the number with a lead track;
  - the number whose lead track id differs from the lead track id of the last decision before the window (re-associated as a new,
    younger track);
  - the number with no lead before the window.
- **Margin-ratio check** of N_DR / F0_DR (median, q05, q95, A_DR, share within 5% of the median), for all evaluated decisions and
  in-dropout.
- **RR_gl(N_DR) against the record P̄:** D_gl(N_DR, F0rec_DR) / D_gl(E_DR, F0rec_DR).
- **Output rule without masks:** the tracker with punish_num = 3 and empty masks (identity check (ii)'s arrays, P̄ of record), with
  its room R_gl and RR_gl(N). This separates the output rule's effect from the masks'.
- **Masked share:** of frames (fresh runs; tuning runs) and of evaluated decisions.

**6c.8 Identity checks (before LOCK_A11b; they compute no DR value).**
- **(i) Harness:** with an empty mask and the configuration of record (punish_num = 1), the fresh runs' re-run arrays reproduce the
  stored CV0 arrays of record (`CD_capture\arrays\CV0`) to A10 B0(b)'s standard.
  - The standard: every key both builders produce within 1e−12 absolute, with an equal finite/NaN pattern. CD's CV0 arrays come
    from the logged tracks, not a replay, so (b) applies.
  - CD's extra sources (cTG1, cTG2, cTG4, clearR075) are not produced by the frozen builder and are not compared.
  - Platform: the pod that runs DR.
  - Result, before the lock (`work\F_dropout\out\DR_IDENTITY_v01.json`): passed.
    - 104 of 105 runs are bit-identical on every key the analyses read.
    - In one run (c1109_eval_0114), 38 values differ in the last bit (≤ 5.7e−14 absolute, ≤ 4.2e−15 relative).
    - cA1 and cQ, which DR does not read, differ by ≤ 2.8e−14.
- **(ii) Output rule:** with an empty mask and punish_num = 3, the number of fresh-run evaluated decisions whose critical scales (F0, E
  or N) change against (i). Changes can come only from the detector's own consecutive misses. The count is reported. Result
  before the lock: 76 of 21,574 evaluated decisions, in 7 of the 105 runs.
- **(iii) Masks:** the second program's regenerated masks equal `DR_MASKS_v02.json` exactly, and §6d's table agrees (§6c.4).

**6c.9 Order and lock (LOCK_A11b).**
- **Before the lock:** this text; the mask file; the DR code and its second program's code (frozen in `work\locks\FREEZE_DR.json`);
  checks (i)–(iii); a pod test of the whole pipeline on the 35 old lead-braking fit runs (exploratory data of record).
- **LOCK_A11b** records the SHA-256 of each.
- **After it, in this order:** P̄_DR, the fresh DR arrays, the values, the calibration, the second program's recount and the comparison.

**6c.10 Verification.**
- **Second program:** by Claude Sonnet 5.5, written from this section and A10 §2 without reading F's DR code or CD's analysis code.
  It may use the frozen scoring library `optA_lib_v02`.
- **What it does:** it regenerates the masks, and recomputes P̄_DR from the per-run P̄ sums and every DR value and verdict from the DR
  arrays.
- **Agreement (A10 §10.1(c)):** counts exact, points and interval ends within 1e−9 on the same draws, calibrated levels equal.

**6c.11 Consequence rules.**
- **DR0 fails:** "under detection dropouts there is no room to test", and the text stops there for DR.
- **DR1 fails:** the measure does not detect rank information at the DR tracker's amplitude; DR2 is printed as not confirmatory.
- **DR2:** reported in its class, with r, c and, under (a), r / c. Whatever the class, the result is not extended beyond lead braking
  under this mask law and output rule.
- **Disclosure:** the text says that DR was specified on 21 Nov 2026, after C's and B's fresh lead-braking results were exported and
  seen, and that it re-scores those same runs with a pre-registered configuration departure (punish_num = 3).

**6c.12 Spend, pods and cut-off.**
- **Pods:** CPU work on pods (EU-RO-1; workers and numba threads = the pod's cgroup CPU quota).
- **Upload:** about 0.27 GB compressed (five capture files and SUMMARY.json per run, for 225 runs plus the 35 test runs; the codex tree).
- **Spend:** each pod is logged in `SPEND_LOG_v13.csv` and deleted when its output is verified (absent from the list). DR's own cap is
  $10, within the sprint's $80.
- **Cut-off:** recounted DR results by **21:30 EST, 21 Nov**, or DR is not printed, and the text says it was not completed.

## 6d. E4: closed loop with detection dropouts — locked by LOCK_A11b

- **Coordinator's decisions, about 14:00 EST:**
  - Arms F0, N, F0_IMM and N_IMM at LOCK_A10_2b's lo and hi settings, unchanged, on the 60 E3 cases (480 runs). No CK3.
  - Capture order: all lo runs first (the primary comparison), then hi. Hi is reported only if captured and recounted by §4's cut-off; otherwise the text says hi was not completed.
  - Under dropouts the arms are not caution-matched; N's margin grows during dropouts by design. Outcomes are each arm's safety and progress at the locked settings, classified by E's rules (contact ±0.10, time lost ±0.5 s), with the open-loop caution difference reported. No equal-caution claim is made for this set.
  - Every check of E is kept.
  - No pod until the coordinator confirms the budget.

**Session E's specification, merged verbatim** from `E_DROPOUT_A11_6d_v03.md` in the shared session notes (sha256 `51352d7f9b10361e6fa47c042e20fda56b27c14dbe070c6716c6af62ac33cf93`); headings demoted two levels, nothing else changed. Where it and §6c's coordinator decisions differ, those decisions govern.

#### 6d.1 Question
Does the pre-registered closed-loop ordering of E3 survive detection dropouts, at the operating points locked in LOCK_A10_2b?
- The ordering compares N with F0, and N_IMM with F0_IMM.
- The settings are not recalibrated for dropouts. Under dropouts the arms are therefore **not caution-matched**: N's margin grows while the tracker predicts without detections, and F0's class-average margin does not.
- The outcomes are each arm's safety and progress at the locked settings, classified by E's rules (contact ±0.10, time lost ±0.5 s), with the open-loop caution difference reported. No equal-caution claim is made for this set.

#### 6d.2 Unchanged from E3
- CARLA, the ego plant, the Codex planner and its 17-row library, the F2 feed-forward servo, the fallback, the detector, both trackers (CANMOT for F0/N; session B's online IMM B1 for F0_IMM/N_IMM), the A1 admission and the native controls.
- The packet is `packet_e_v04`: `packet_e_v03` plus only the changes of 6d.3. Its diff is `work\E_closedloop\review\E4_V04_DIFF_v02.patch`.
- **Cases:** the same 60 fresh lead-braking cases as E3, `c1109_eval` positions 35–54 at each desired speed (`c1109_eval_0480` … `c1109_eval_1098`), with E3's seeds and noise episodes. Every E4 run has an E3 twin with the same case, arm and level.
- **Settings** (LOCK_A10_2b, SHA-256 81d3a77a…, unchanged):

  | Arm | lo | hi |
  |---|---|---|
  | F0 | g = 4 | g = 16 |
  | N | 3.3497 | 13.335 |
  | F0_IMM | 11.885 | 53.09 |
  | N_IMM | 10.593 | 47.32 |

- **Outcomes per run:** A10 §7.4, from truth at 20 Hz, window k ≥ 99. Contact; impact speed; time lost (runs without contact); rest gap; peak deceleration; RMS jerk; fallback share (decisions in full braking).

#### 6d.3 Changes: the mask and the output rule (A11 §6c)
1. **Rows.** The rows are the run's 2 Hz detector update ticks, in order, i = 0, 1, 2, …. In the closed loop, row i is sim frame k = 19 + 10·i (the probe's detector condition k ≥ 19 and k % 10 == 9). A full run has 69 rows.
2. **The mask law, as A11 §6c, implemented in `e_dropout_v01.py`.**
   - Seed per run: `rng = numpy.random.default_rng(int.from_bytes(hashlib.sha256(("A11/D/" + case_id).encode()).digest()[:8], "big"))`, with case_id the protocol case id, e.g. `c1109_eval_0480`.
   - Row 0 is never masked, so tracks start.
   - From row 1 on, at each row not inside a window, draw u = rng.random(). If u < 0.10, draw L = rng.integers(1, 4), uniform on {1, 2, 3}, and mask rows i … i+L−1. A window is cut at the run's end. Rows inside a window draw nothing.
   - The row right after a window is never masked and draws nothing. Draws resume at the row after it.
   - So every masked stretch is 1–3 rows (0.5–1.5 s).
   - The mask depends on the case only, never on any outcome. All arms of a case see the same mask.
   - Over the 60 E3 cases there are 131 stretches of 1 row, 126 of 2 and 122 of 3, and 18.4 % of assessment-window rows are masked. Under the first wording, windows could follow back to back, giving stretches up to 7 rows; that is why the gap row was added.
3. **On a masked row**, the detector still runs, so compute and timing are unchanged, and its output is logged. The tracker receives an empty detection list at the row's time and only predicts. `detections.jsonl` records `masked` and `tracker_rows` (0 on a masked row). `ARM_METHOD_v01.json → dropout` records, before the run uses them: the law id `A11D2` (§6c final wording), the SHA-256 of the law file, the seed, the mask, the windows as [start, drawn L], and punish_num.
   - The detector rows in `model` are the TRUE detector output, kept so the review can re-run the detector exactly. The tracker's input on a masked row is `[]`. Every consumer must use `masked` / `tracker_rows`.
   - A **locked mask table**, `work\E_closedloop\out\E4_MASKS_v01.json` (61 cases: the 60 E3 cases plus c1109_tune_0000; SHA-256 `c66d91923ae4d87ac7e49ac70fba98828434ae64de0954f15078ff80f2997313`), is the known answer, from outside the law file, that every run is checked against.
4. **Output rule (A11 §6c).**
   - The pipeline of record outputs an unmatched track only while time_since_update ≤ punish_num = 1 (CANMOT `vendor\CANMOT\src\canmot\tracking\nusc_tracker.py`, line 380, `output.punish_num` in `contracts\tracker_config.json`).
   - For §6d all arms use **punish_num = 3**, so the planner receives the tracker's predicted states through every stretch. This is a pre-registered configuration departure for D and §6d only.
   - Side effect: natural detector misses of up to 3 updates are also coasted, the same in every arm.
   - B's IMM wrapper uses the same CANMOT Tracker, and the same punish_num is set on it.
5. **Track deletion is not reached.**
   - Car is CANMOT class 2 (`vendor\CANMOT\src\canmot\data\script\NUSC_CONSTANT.py`, line 15).
   - Its `life_cycle.max_age` is **15 updates = 7.5 s** (`contracts\tracker_config.json`, lines 75–83: `"2": 15`; the block's first entry `"1": 10` is bus).
   - A track dies when time_since_update ≥ max_age (`vendor\CANMOT\src\canmot\tracking\nusc_life_manage.py`, line 46).
   - A 1–3-row stretch never reaches it.
6. **Observed behaviour, recorded, not a rule** (laptop test on E3 case c1109_eval_0480).
   - During a stretch, the coasted lead's score decays ×0.2 per missed update.
   - After a 3-row stretch, the lead's next detection may start a NEW track id at the gap row, with a fresh covariance. The output track lies on the lead's true position.
   - The planner therefore has a lead in its actor list at every row.

#### 6d.4 Order of capture (pre-registered)
- **Stage L:** the 4 arms at **lo**, 240 runs, captured first on every pod, as one list per pod, dealt by case.
- **Stage H:** the 4 arms at **hi**, 240 runs, a second list per pod. A pod starts its H list only when its L list is FINISHED.
- **Lo is primary and complete on its own.** If H is not captured and recounted by §4's cut-off, the text reports L and says that H was not completed. No partial H is reported.
- Each list carries the A1 admission (crash and benign) and native controls. A pod whose controls are not bit-identical halts, and its lists move to another pod.
- Pods are RTX 4090. Another GPU type is used only if its A1 controls are bit-identical at admission; pairs stay on one pod by case.

#### 6d.5 Analysis (as E3, A10 §7.5)
**Comparisons**, paired by case, at each level:
- **E4-H1:** N vs F0.
- **E4-H2:** N_IMM vs F0_IMM.

The lo comparisons are the hypotheses. The hi comparisons use the same statistics and classes and are reported as secondary.

**Statistics:**
- **Contact:** paired difference with the Newcombe hybrid-score 95% interval (method 10, corrected φ) and the exact McNemar test.
- **Time lost:** mean paired difference over pairs without contact, with a 95% case-bootstrap interval. A fresh `default_rng(20261922)` per comparison, 20,000 resamples of all pairs.
- **Other outcomes:** descriptive, with the same bootstrap. No interval is reported below 2 defined pairs.

**Classes**, in order (U and L are the ends of the contact interval):
1. "safer at no extra cost": U < 0 and time-lost upper end < 0.5 s.
2. "safer at a cost": U < 0 and time-lost upper end ≥ 0.5 s.
3. "equivalent": −0.10 < L, U < 0.10, and the time-lost interval within ±0.5 s.
4. "worse": L > 0.
5. Otherwise "inconclusive".

**Expected direction, stated, not a test:** N ≤ F0 in contacts under dropouts, because N's margin grows while the tracker coasts. The classes are reported whatever they are.

**Caution, reported, not matched:**
- Each arm's design caution at the locked point (LOCK_A10_2b, without dropouts).
- The open-loop caution difference under dropouts at the same scales, from D (§6c), if D reports it. Otherwise "not computed".

**Exploratory, labelled exploratory.**
- Each arm's change from its E3 twin: paired contact difference E4 − E3 (Newcombe) and time-lost difference (bootstrap).
- The difference-in-differences of (N − F0) between E4 and E3, by case bootstrap.
- Per-run masked share.
- **Caveat:** these comparisons cross TWO changes, the masks AND the output rule (punish_num 1 in E3, 3 in E4). They do not isolate the masks' effect, and the text says so.

**Validity of a run** (as E3):
- status CAPTURED_AND_REVIEWED;
- no policy failure;
- no contact before the window;
- the realised mask equals the law's mask and the locked mask table, row by row, including `tracker_rows`;
- the law id is `A11D2`, and the law file's SHA-256 is the packet's;
- punish_num = 3, for CANMOT, and for the IMM tracker as recorded in `E_IMM_TRACKER_v01.json`;
- **IMM arms:** no `update` or `birth` event in `imm_filter_events.jsonl` on a masked row (the event's `timestamp` is its detector row). This is independent evidence that the IMM received no detections there. For the CANMOT arms, the perception review's exact replay with `[]` shows the same;
- the run's method carries its job's law and punish_num. Otherwise the worker marks it `E4_METHOD_MISMATCH`, and a phase-E4 job without both knobs is refused;
- the pod's A1 controls are bit-identical.

An invalid run drops its pair.

#### 6d.6 Checks (none of E's is dropped)
1. **Laptop tests, done before the lock** (`work\E_closedloop\tests\out\`).
   - (a) **Mask law** (`E4_LAW_TEST_v02.json`):
     - start rate 0.0991 per draw over 114,110 draws;
     - L shares 0.336 / 0.339 / 0.324;
     - longest stretch 3;
     - row 0 never masked, gap row always unmasked;
     - truncation-consistent.
     - The second program's independent implementation, and session F's `work\F_dropout\code\dr_masks_v02.py`, both give masks and seeds identical to the locked table on all 61 cases (`E4_F_CROSSCHECK_v01.json`: 0 mismatches).
   - (b) **Masked IMM replay identity under punish_num = 3** (`E4_IMM_MASKED_REPLAY_v02.json`):
     - the online IMM of packet v04 equals session B's offline B1 on the same masked stream (69 rows, 17 masked);
     - track and planner-actor maximum difference 0.0;
     - PASS.
   - (c) **CANMOT output rule** (`E4_CANMOT_OUTPUT_TEST_v02.json`):
     - with punish_num 1, the lead is absent from the 2nd masked row of a stretch;
     - with punish_num 3, it is present at every masked row, and at the gap row an output track lies within 3 m of the lead's true position;
     - PASS.
   - (d) The arms' constraint code is unchanged from E3. The diff touches only the probe's detector row, the trackers' punish_num, the worker's knobs and the reviews.
2. **Cross-model build review** of the v04 diff (Claude Fable 5.2) before any pod (`work\E_closedloop\review\REVIEW_E4_BUILD_v01.md`).
   - Result: PASS WITH FIXES.
   - B1 (F's first-wording mask code) is fixed by F, in dr_masks_v02.
   - M1–M4 are fixed as above. M5 is documented in 6d.3(3).
   - The re-review of the fixes is PASS. It caught one IMM check keyed on the wrong field, which was fixed and tested both ways: 0 violations on a masked run; 17 of 17 masked rows flagged on unmasked events.
3. **Smoke, 1 pod.**
   - A1 admission and controls bit-identical.
   - 4 masked runs (F0, N, F0_IMM, N_IMM at lo) on tuning case c1109_tune_0000: masks as logged, and every review passing.
   - **Non-dropout identity:** one E3 case (c1109_eval_0480, F0 lo) run on packet v04 with NO dropout knobs, so punish_num is 1 and nothing is masked, must reproduce E3's record bit-identically: `frames.jsonl`, `detections.jsonl`, `evaluation_truth.jsonl` and `e_decisions.jsonl`. This shows packet v04 changes nothing outside E4.
   - The native A1 controls take no E4 knob, so they run with punish_num 1 as in E3.
4. **Second program** (Claude Sonnet 5.5): `recount\e_recount_v04.py` and `e_recount_export_e4_v01.py`, written from this text and the raw files without reading the first program. It recounts the per-run outcomes, every run's mask against its own implementation of the law, every comparison and class, and the export (179 keys).
5. **Comparison of record:** counts exact, values within 1e-9, classes equal. Any disagreement stops the work until its cause is recorded and fixed (A10 §10.1(c)).
6. **Freeze:** packet v04, the jobs, the first program (`analysis\e4_analyse_v01.py`) and the second program are frozen in a FREEZE_E addendum listed in LOCK_A11b, before any E4 run. The 60 cases' masks are written to a mask file whose hash goes into LOCK_A11b.

#### 6d.7 Export to A
`work\E_closedloop\out\A_EXPORT_E4.json`, and the second program's `A_RECOUNT_E4.json`, with the same 179 keys:
- **Status keys:** `E4.status`, `E4.punish_num`, `E4.n_cases`, `E4.L.completed`, `E4.H.completed`.
- **Per arm and level:** `E4.<F0|N|F0IMM|NIMM>.<lo|hi>.<contact|vimp|tlost|restgap|peakdec|jerk|fallback|masked|caution>`.
- **Comparisons:** `E4.<N|NIMM>.<lev>.dc[.ci]`, `.dt[.ci]`, `.d_<vimp|restgap|peakdec|jerk|fallback>[.ci]`, `.class`.
- **Hypotheses:** `E4H1`, `E4H2` (the lo classes).
- **Exploratory:** `E4.deg.<arm>.<lev>.dc[.ci]/.dt[.ci]` and `E4.did.<N|NIMM>.<lev>.dc[.ci]`.
- An undefined value or interval is null. No value of an incomplete level is exported.

#### 6d.8 Budget and gates
- About 480 runs on 6 RTX 4090 pods (claude-v13e-11…16), about 1.6 h of capture.
- The smoke uses 1 pod (claude-v13e-10).
- About $13 in total, within the coordinator's confirmed cap.
- The smoke is allowed after the build and review pass.
- Capture is allowed only after LOCK_A11b exists AND the coordinator confirms the top-up.
- No pod runs with the balance heading under $15. Every pod is logged in SPEND_LOG_v13.csv and deleted on a confirmed delete.

## 7. Readability pass and review

- Session A's readability pass (abstract bottom line first, plainer introduction, a glossary, the minor points of AUTHOR_ITEMS §5, index terms trimmed to five, abstract cap up to IEEE's 250 words) changes no value, no classification and no rule.
- After the text freeze, a fresh five-seat ARS panel reviews the final freeze, with seats spread over Claude Opus 5.5, Claude Sonnet 5.5 and Claude Fable 5.2, then one fix round, a delta audit of the changed sentences, and the final package.

## 8. Verification

- A10 §10 applies to every new printed value: coverage (a), second programs on a different model from the writer's (b; Claude Sonnet 5.5 by default), agreement (c: counts exact, points and interval ends within 1e−9 on the same draws, calibrated levels equal), order (d).
- The comparison files for X, Y, B1r, DR and E4 are listed in the supplement's verification section with their times and hashes.

## 9. Locks (LOCK_A11.txt, then LOCK_A11b.txt)

Two stages, like A10's Lock 2.
- **LOCK_A11** covers X, Y and B1r. It is written before any fresh crossing value, any Y value and any fresh re-score under B1r.
- **LOCK_A11b** covers DR (§6c) and E4 (§6d), with their final specifications. It is written before any DR value on fresh runs and before any E4 run is captured. It records this file's SHA-256 again, with DR's and E4's code, masks and second programs, and states which sections changed after LOCK_A11.

LOCK_A11 records the SHA-256 of:
- this amendment;
- the step-0 file;
- the X case file(s) and job lists;
- the crossing analysis code and its second program's code, if ready (otherwise frozen in a FREEZE_CD addendum before their first run, with its hash sent to the coordinator and listed in the supplement);
- the B1r rule code (its constants are frozen in a FREEZE_B addendum before the re-score).

## 10. Model record

- This amendment: Claude Opus 5.5 (`claude-opus-5-5`), the coordinating session.
- First programs: Claude Opus 5.5 (sessions B, CD, E and F). Second programs: Claude Sonnet 5.5. Panel: mixed (§7).
