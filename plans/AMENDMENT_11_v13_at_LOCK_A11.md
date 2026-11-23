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

## 6c. DR: detection dropouts on the fresh lead-braking runs (open loop) — locked separately by LOCK_A11b

Proposed by "Paper work summary" and approved in scope by the author (§0). Owner: session F. F's full specification replaces this section's design notes before LOCK_A11b. The name is DR, with hypotheses DR0–DR2, because A10 already has a package D. Nothing of DR is computed on fresh runs before LOCK_A11b.
- **Why.** Lead braking has room but a near-constant covariance; crossing has a varying covariance but little room. Under detection dropouts the covariance grows with the time since the last update. That plausibly tracks the real error, giving room and variation in one scenario.
- **Coordinator's proposed design, for F to confirm or amend before LOCK_A11b:**
  - Frame-level masks, independent of truth, at the 2 Hz update ticks. Each tick not already in a window starts one with probability 0.10, of length 1, 2 or 3 ticks (uniform), seeded per run from its id.
  - The online tracker of record, re-run with the masks through session B's frozen replay; empty-mask identity first.
  - F0_D: the class average under the same masks on the 120 tuning runs.
  - Sequence D0 room, D1 detection by E5_N, D2 N's class by the H3 rule, as X (§3.5), calibrated per A10 §2.6.
  - Descriptive: the in-dropout population, the margin-ratio check, the masked share of ticks.
- **Closed loop with dropouts:** session E judged it feasible (note `E_DROPOUT_FEASIBILITY_v01.md`, shared notes). It is pre-registered in §6d, written by E and locked in LOCK_A11b before any dropout run is captured.
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

## 6d. E-D: closed loop with detection dropouts — TEXT FROM SESSION E PENDING (due about 15:15), locked in LOCK_A11b

- **Coordinator's decisions, about 14:00 EST:**
  - Arms F0, N, F0_IMM and N_IMM at LOCK_A10_2b's lo and hi settings, unchanged, on the 60 E3 cases (480 runs). No CK3.
  - Capture order: all lo runs first (the primary comparison), then hi. Hi is reported only if captured and recounted by §4's cut-off; otherwise the text says hi was not completed.
  - Under dropouts the arms are not caution-matched; N's margin grows during dropouts by design. Outcomes are each arm's safety and progress at the locked settings, classified by E's rules (contact ±0.10, time lost ±0.5 s), with the open-loop caution difference reported. No equal-caution claim is made for this set.
  - Every check of E is kept.
  - No pod until the coordinator confirms the budget.

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
