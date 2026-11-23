# FEASIBILITY of revision v13 (accept-ready scope): inputs, compute and time per package, and what only the author can do

Written 19 Nov 2026 by the v13 planning session (Claude Opus 5.5, `claude-opus-5-5`).
- First version: about 11:55 EST.
- **This version: about 12:10 EST.** It adds packages D (now required), E (closed loop) and F (real sensors), and the cut-in family, after the requesting session's scope change.

**How the check was done**
- **Read-only:** file listings and counts; reading code, configuration, receipts, design notes and reports; the first records of logs and result files; one `tar -t` listing; SHA-256 of the detector checkpoint; file attributes; hardware queries.
- **Not done:** no analysis, simulation, tracking, detection or scoring. Nothing was written outside `revision_v13\` and the shared notes folder.
- **Folders read only:**
  - `<earlier-phase folder 1>` (**P** below);
  - one file hashed in `<earlier-phase folder 2>\`;
  - companion manuscript [9]'s archive (`<user folder>\<companion manuscript archive>\`, **R** below): directory names, five file names, sizes and attributes only. No data file was opened.
- **Not opened:** nothing named `<excluded folder 1>` or `<excluded folder 2>` (they exist only in `<earlier-phase folder 2>\`, and the one search there skipped them), and `<excluded folder 3>`.
- **No external traffic:** no network access was used, and no manuscript text left the machine.

## 1. Verdict per package

| Package | Feasible? | Runs where | Main dependency or risk |
|---|---|---|---|
| A (text) | Yes | Laptop | A TeX toolchain for the typeset count (the IEEE open-journal template is already in Downloads); access to paywalled standards |
| B (offline re-tracking) | Yes | Laptop (B7 on a pod) | New code: IMM, adaptive Q, re-tuning, the adapter. The exact offline tracker replay exists. B7 runs on fresh runs only: the old runs' sweeps are gone (§3) |
| C (fresh runs, two families) | Yes | RunPod RTX 4090 pods, as before | The author's account; the network volume with the CARLA runtime must still exist (unverified) |
| D1 (non-braking leads) | Yes, with a generator change | Pod | A new, reviewed, hash-pinned actor-policy version and packet |
| D2 (event-level table) | Yes | Laptop | — |
| E (closed loop) | **Possible, uncertain** | Pod | The braking fix F2 has never run in CARLA. Four of the arms do not exist in the simulator code. The project's lead put the brake test's first-attempt pass at 1 in 3 to 1 in 2, and a clean end-to-end confirmation below 1 in 2 (`P\09_redesign\DESIGN_NOTES_v01.md` §6.4n). The ladder stops cheaply if it fails |
| F (real sensors) | **Yes, on this laptop, by either of two routes**; the author must choose (§6) | Laptop | F-A reuses [9]'s data (author consent; the paper's statement changes). F-B needs nuScenes metadata under the author's account and terms |
| CARLA on this machine | **No** | — | Intel Iris Xe, no NVIDIA GPU, no WSL, no Docker, no CARLA (§2 row 7) |

## 2. Inputs, checked one by one

| # | Input | Status | Evidence | Implication |
|---|---|---|---|---|
| 1 | Stored 2 Hz detections | Present | `detections.jsonl` in all 35 old evaluation runs (`P\07_fit_runs\archives\p1b_fit_finite_0005…0039`) and all 120 tuning runs at c = 1 (`P\08_phase2\archives_c1`), including 20 lead-braking and 20 cut-in runs. 69 detector updates per 700-frame run | B re-tracks every stored run at 2 Hz |
| 2 | Tracker logs and truth | Present | `filter_algebra`, `filter_events`, `filter_target_covariances`, `frames`, `evaluation_truth`, `raw_observations`, `noise_receipts`, `scenario_frames` per run. Stored arrays `P\09_redesign\m2_decisions\openloop\gateR_rt_v01\*.npz`: fit lead braking 35, stopped 35, pedestrian 31, vehicle crossing 2; tuning 20 for each of the six families | Everything for B. **Cut-in has stored arrays for its 20 tuning runs only**: the carry-over claim needs fresh cut-in runs (C) |
| 3 | 20 Hz lidar sweeps | **Not retained**, except one evaluation run | The capture saves every sweep (`P\03_runbook\packet_main_v03\claude_smoke_v01\probe_arms_v01.py` L243); the archive drops them unless `keep_raw`, which a hash rule sets for 1% of jobs (`P\03_runbook\main_sources_v01\make_main_jobs_v01.py`). Receipts: `"keep_raw": false` in 116 of 117 fit and 117 of 120 tuning archives, `"frames_dropped": 1400`. Kept: evaluation run **p1b_fit_finite_0037** (700 clean + 700 noisy, 263 MB each folder, on disk) and three tuning runs that are not lead braking. Each frame's sweep SHA-256 is logged | R13 is done on the fresh runs (all sweeps kept), with run 0037 as a link. **The v12 Data Availability statement, which offers the sweeps, is wrong** and must be corrected |
| 4 | CenterPoint checkpoint | Present, hash verified | `Downloads\epoch_20.pth` and `<earlier-phase folder 2>\149_…\legacy86\weights\epoch_20.pth`: 107,553,302 bytes, SHA-256 `59936925…e8ca32` = Table S28 = pod cache manifest | Detection runs on pods (CUDA, spconv). Median logged inference 0.061 s per detection on an RTX 4090 |
| 5 | CANMOT configuration and code | Present | `149_…\contracts\tracker_config.json`: CV with `ExtendedKalmanFilterRotate`, all classes (L55–71). Vendored CANMOT has CA, CV and CTRA models (`motion_model.py` L166, L325, L506); no IMM | B3 and B4 are configuration plus tuning; B1 and B2 are new code |
| 6 | Offline tracker replay | Present (not re-run here) | `P\09_redesign\m4_perception_model\tracker_harness_v03.py`: lead braking 55/55 exact, about 1 s per run; stand-ins for missing packages in `shims_v01\` | Base of B; B0 re-checks exactness in today's Python 3.12.2 / numpy 2.5.4 |
| 7 | CARLA 0.9.15 here | **No** | Intel Iris Xe (integrated), no NVIDIA GPU, i7-1165G7 (4 cores / 8 threads), 15.7 GB RAM, 240 GB free; no WSL, Docker or CARLA. The runs were made on Linux RTX 4090 pods from a network-volume runtime (CARLA assets 8.5 GB) | C, D1, E and B7 run on pods. A Windows CARLA would not be "the same generator" |
| 8 | Local Python | Partly | Python 3.12.2 with numpy, scipy, pandas, matplotlib. Missing: torch, spconv, filterpy, numba, shapely, lap, pyquaternion, hydra, omegaconf, carla | B and F work through the harness's stand-ins; no local detection |
| 9 | Fresh cases | Present, never run | `P\06_phase0\scenarios\DEVELOPMENT_PROTOCOL_MAIN_v01.json` (SHA-256 `32d683a0…`, the hash in every run's `contract.json`). Lead braking: 300 evaluation cases (106 / 88 / 106 at 5 / 10 / 15 m/s), plus 10 never-run tuning cases. Cut-in: 300 evaluation cases (106 / 101 / 93) | C uses 35 per speed per family; E3 the next 20 per speed in lead braking; E2 the 30 lead-braking tuning cases |
| 10 | Same generator? | Draw law and arm yes; sampler key differs | The draw keys are identical, with U(2, 6) m/s², U(1, 3) s, U(1, 3) s ranges in both sets. The old evaluation cases come from sampler key A85 with α = β ∈ {1.642374415149816, 5.411894431054339, 7.550302542198003}; the C1109 cases carry no α, so A10 §5.1 assigns those values in a fixed cycle | Disclosed in §III; the author confirms (§10) |
| 11 | Pod pipeline and costs | Records only | `packet_main_v03`, worker and job builder in `P\03_runbook\`. `P\04_spend\SPEND_LOG.csv`: RTX 4090 about $0.89/h; main-results spend $29.70 for 210 fit episodes, 720 fixed-sweep runs, admission runs and about 15 min of native sweep; balance **$189.34 on 13 Nov 2026**. Records: 44–51 runs per hour per pod, about $0.028 per run all-in, about $0.50 per pod session. Run 0037's capture took 111 s | Costs in §8. **Not verified:** that the network volume still exists (needs the account) |
| 12 | Closed-loop building blocks (E) | **Partly** | The simulator code has zero margin, the tracker covariance, a constant margin and two learned arms; it lacks the class-average, true-state and oracle arms, a brake-test script and the controller fix F2 (`P\02_design\PROPOSAL_CARLA_CONFIRMATION_v02.md` §3, citing `P\09_redesign\impl_map\REPORT_v01.md` L16–60). F2 is specified and tested only on the laptop stand-in, where it brings stopping distance within 2.4% of the planner's model (`DESIGN_NOTES_v01.md` §6.4e). Stand-in Gate C (§6.4m): the oracle had room in closed loop; the tracker covariance behaved as the class average in 120 of 120 episode-settings | E is a build plus a staged ladder (A10 §7). If E1 fails, Gate C remains as a stand-in result with its limits |
| 13 | Real-sensor route F-A (Argoverse 2, [9]'s archive) | Present, local | **R** `\30_DATA\`: own-CenterPoint detections, CANMOT (T1) and Poly-MOT (T3) tracks with covariances, caches with matched truth, 2 Hz ground truth, 10 Hz ego pose; 375 logs; files stored locally (attributes `Archive`, no online-only flag). Inventory: `P\02_design\INVENTORY_AV2_C1_ARCHIVE_v01.md`. Existing pilot code `P\10_av2\av2_*.py` and report `REPORT_AV2_PILOT_v01.md` (folds 0–1 only; about 7 CPU-min; room at the 2 s horizon, none at 3 s; held-out folds 2–4 never read). Licence CC BY-NC-SA 4.0 | Cheapest real-sensor route, laptop only. **It reuses [9]'s data and its replay planner**: needs the author's consent, and the paper's sentence "none of its data, results or figures is used here" must change |
| 14 | Real-sensor route F-B (nuScenes) | Partly present | `Downloads\nusc_results_flip\`: CenterPoint detection results in nuScenes submission format for train, val and test (2.4 GB; provenance to be confirmed by the author); `Downloads\infos_val_10sweeps_withvelo_filter_True.json`; nuScenes devkit in `<earlier-phase folder 2>\86_implementation_20261030\vendor\`. **Missing:** the nuScenes annotations and ego poses (`v1.0-trainval` metadata) | Independent of [9]. Needs the author to register with nuScenes, accept its terms and download the metadata, plus a new adapter (about 500 lines). No GPU needed |
| 15 | LaTeX and Pandoc | Not installed; template present | No `pandoc`, `pdflatex`, `xelatex`, `lualatex` or `latexmk`. `Downloads\IEEE-open-journal-template.zip` holds `ieeetj.cls` and a template | The typeset count needs a TeX install (author's approval) or the author's own build |
| 16 | Regulation texts (S21) | Present | `Downloads\ECE_TRANS_WP.29_2022_59_Rev.1e.pdf` and `R157am4e.pdf` | S21 can be answered from local copies; ISO and IEEE standards (S25) are paywalled |

## 3. The lost sweeps, and what follows

Every old run except p1b_fit_finite_0037 lost its 20 Hz sweeps at archiving. Three things follow:
1. **R13 runs on the fresh runs**, recorded with all sweeps (A10 B7), with run 0037 as a one-run link to the old set.
2. **The v12 Data Availability statement** ("lidar sweeps … available from the author on request") must be corrected in v13. The deposit manifest must say the same.
3. **Re-simulating the old runs** to recover their sweeps is possible only if CARLA reproduces each frame exactly; the logged per-frame SHA-256 makes that checkable. It is an option, not part of the default plan.

## 4. Compute and time per package

Rates used:
- **Tracker replay:** about 1 s per run (M4 report).
- **Array rebuild:** about 10 s per lead-braking run (`STATUS_GATE_R_v01.txt`: 2,344 CPU-s for 223 runs; `a9_7a` about 7 s per run).
- **Capture:** 44–51 runs per pod-hour at about $0.028 per run.
- **Detection:** about 0.06 s per inference.
- **Bootstrap scoring:** minutes per 20,000-resample analysis on 35 runs, scaling roughly with the number of runs.

| Package | Code to write (estimate) | Compute | Money | Wall clock (with gates) |
|---|---|---|---|---|
| **B** | Adapter 250 lines; re-tuning 200; CA 80; IMM 300–400 (+ second implementation); adaptive Q 80; E5 and ceilings, terciles, delayed stop 300; diagnostics 150; cut-in event and track age 150 | Laptop 3–5 h (five trackers × 175 runs replay and rebuild; scoring); B7 detection on the pod: about 35 s per run × 210 fresh runs ≈ 2 GPU-h | ≈ $2 (B7) | 2–3 days (mostly coding) |
| **C** | Job builder (two families, `keep_raw`), sealing check, offline detector script | Pods: 210 runs ≈ 4.5 pod-h (about 45 min on six pods, plus start-up). Laptop after Lock 2: extraction ≈ 3 h (five trackers × 210 runs), rate variants ≈ 2 h, scoring and double bootstrap ≈ 4–7 h; recount the same again | ≈ $6–8 capture + storage (≈ 0.5 GB per run with sweeps, ≈ 100 GB in all; a monthly volume cost the author can end after deposit) | 2–3 days after Lock 2 |
| **D** | D1 actor-policy variants 100–150 lines, independent review, new packet; D2 extraction 100 | Pods: 105 D1 runs ≈ 2.3 pod-h. Laptop: 2–3 h | ≈ $3 | 1–2 days (review included) |
| **E** | F2 feed-forward about 110 lines; brake-test script 120–150; arms F0 80, CK3 60, TG 40, PS 80, online IMM integration about 150 plus a replay-identity test; packet changes; outcome extraction and its second program about 200 | Pods: E1 3–6 runs; E2 180 runs; E3 900 runs; E3b 300 runs ≈ 30 pod-h (about 5 h on six pods). Laptop 2–3 h | ≈ $42 expected (E1 ≤ $3; E2 ≈ $5; E3 ≈ $25; E3b ≈ $9); cap $50 | 4–6 days: build and review 2–3, brake test, then calibration and main runs. Stops after E1 if the brake test fails |
| **F-A** (Argoverse 2) | Extend the pilot code: E5 and ceilings, the gridless frontier, IMM on the archive's detections, the held-out gate | Laptop ≈ 2–4 h (pilot: about 7 CPU-min for 150 logs × 3 trackers; the IMM re-tracking and calibrated intervals dominate) | $0 | 1–2 days after consent |
| **F-B** (nuScenes) | Adapter about 500 lines (route from the ego path, keyframe interpolation, planner rows); class average on the train split; checks | Laptop ≈ 4–8 h (850 scenes; CANMOT and IMM re-tracking; array build; scoring) | $0 (download ≈ 0.4–0.5 GB of metadata by the author) | 2–3 days after the download |
| **A** | Parts and generators; response letter; claim audits | Laptop | $0 | 2–3 days |

**Totals.** About $55–65 of pod time plus storage, against $189 on record (13 Nov). About 20–30 hours of laptop compute, plus the same for recounts. **Calendar: about 2–3 weeks**, set by coding, independent reviews and the author's gates rather than by compute. C, D and F can proceed while E is built; E's ladder can stop early without holding the rest.

## 5. What C, D and E need on the pod side

- **Network volume and runtime.** The CARLA runtime and assets on the network volume (CACHE_EXPECTED lists 1,693 runtime files and an 8.5 GB asset archive). If the volume is gone, the runtime must be rebuilt first: the bootstrap scripts are in `packet_main_v03\bootstrap\`; the asset archive is not on this laptop. That would be planned and costed separately.
- **Jobs.** New job lists (C: two families; D1: the new case file; E: arms × levels × cases), each with `keep_raw` set as A10 requires.
- **Packets.** For E and D1, a new packet version. Packet updates accept only `claude_smoke_v01` paths and auto-bind new files there (sibling notes). Stored references cannot be reproduced once F2 is in, so "references reproduce" means "a new run repeats itself" (proposal v02 §3).
- **Pod rules.** Pods are terminated whenever a repair is needed. E1 has a $3 cap with at most two attempts.

## 6. Package F: the two routes compared

| | F-A: Argoverse 2 ([9]'s archive) | F-B: nuScenes |
|---|---|---|
| Data on this machine | All (detections, tracks with covariances, truth, ego pose) | Detections only; annotations and ego poses need a download |
| Trackers | CANMOT (T1) and Poly-MOT (T3, CTRA: a covariance about half state-dependent per the pilot's §5) exist; B1 IMM can be run on the archive's detections | CANMOT with its released nuScenes configuration; B1 IMM |
| Held-out data | Folds 2–4 (225 logs), never read for this question | The val split (150 scenes); train as the design split (detector in-sample there) |
| Planner | The archive's replay planner (k8), as in the pilot: magnitudes not comparable with CARLA | The CARLA study's planner library through a new adapter: comparable |
| Known so far | The pilot's design folds: small room at 2 s, none at 3 s, RR(N) undecided | Nothing |
| Separation from [9] | **Breaks it**: [9]'s data, detector and replay code. The paper and cover letter must say so; the editor may see it as overlap | Kept |
| Author actions | Consent; decide how to describe the overlap | Register with nuScenes, accept its terms (non-commercial), download the metadata; confirm the provenance of the local detection results |
| Cost | $0, 1–2 days | $0, 2–3 days |

**My reading.** F-A is faster and already validated by the pilot. F-B keeps the two papers apart and uses the same planner as the CARLA study, so its results line up with the rest of the paper. If the author wants both independence and speed, F-B with F-A as a later robustness check is possible. **The choice is the author's**, as the requesting session asked.

**Other real-data routes.** Waymo Open and KITTI tracking would need GPU detection or have no covariance tracker output here: not feasible on this machine.

## 7. What package A needs

- **Typeset page count.** Pandoc plus a TeX distribution, with the IEEE open-journal class from the local template. Two ways, neither of which this session should take on its own:
  - (a) install TeX Live or MiKTeX and Pandoc from official sources, with the author's approval;
  - (b) the author builds the PDF themselves. On Overleaf, the manuscript would leave the machine; that is the author's choice, not this session's.
- **Standards.** R157 texts are local. ISO 15622, ISO 22179 and IEEE 2846 are paywalled, and UN R152 is public. Any check against them is by identifier, and no manuscript text is sent anywhere.

## 8. Money in detail

| Item | Expected | Cap or note |
|---|---|---|
| C capture (210 runs) | ≈ $6 | — |
| B7 detection (≈ 2 GPU-h) | ≈ $2 | — |
| D1 (105 runs) | ≈ $3 | — |
| E1 brake test | ≤ $3 | Cap $3 |
| E2 (180 runs) | ≈ $5 | — |
| E3 (900 runs) | ≈ $25 | E total cap $50 |
| E3b (300 runs) | ≈ $9 | — |
| Pod start-ups and idle time | ≈ $3–5 | About $0.50 per session |
| Storage (sweeps, ≈ 100 GB) | A monthly charge | The author can delete after deposit |
| **Total** | **≈ $55–65 + storage** | Balance on record $189.34 (13 Nov) |

## 9. Risks and unknowns

| Risk | Effect | Handling |
|---|---|---|
| The network volume is gone | C, D and E need a runtime rebuild first | The author checks the account first |
| E1 brake test fails (project estimate: passes at first attempt with 1 in 3 to 1 in 2) | No closed-loop result in CARLA | E stops at ≤ $3. Reported as attempted, with the reason. Gate C (stand-in) is reported with its limits (A10 §9) |
| Zero-margin closed-loop contacts are rare | E's contact comparisons have low power | Rule in A10 §7.3; time lost, rest gap and deceleration remain |
| The online IMM differs from the offline B1 | E-H3 tests a different tracker | E0 replay-identity test before any pod |
| Offline 2 Hz re-detection is not identical to the online one | The B7 reference changes | A10 B7(i): use the offline 2 Hz as the reference, and say so |
| Tracker replay no longer exact in today's numpy | B0 fails | B stops until the cause is found |
| CANMOT's rotated EKF does not take CA | B4 uses the linear KF | Code check, recorded in Lock 2 |
| Too few young-track cut-in decisions with room | K2 not evaluable | Reported as such (A10 §5.4) |
| The fresh room is small or absent | H0 or K0 fails | Rules fixed; the author is consulted if H0 fails |
| F-A: the editor sees overlap with [9] | Desk risk | The author's choice of route; full disclosure if F-A |
| F-B: the local nuScenes detections have unclear provenance | Real-log results rest on unknown detections | The author confirms provenance; otherwise detection is re-run on a pod with the nuScenes lidar data (a much larger download) |
| Length grows with E and F | R3 not met | The build fails above the word budget (A10 §10.4); detail goes to the supplement (PLAN §6) |
| Correlated error between writer, recount and audit | Errors pass unseen | Different models by default (A10 §10) |

## 10. What only the author can do

**Decisions before Lock 1**
1. Approve `PLAN_v13.md` and `AMENDMENT_10_v13_DRAFT.md`, with any default changed (A10 §12: δ; runs per family; latency; IMM transition; D1 variants; E go-ahead and cap; models for the second programs and audits; re-simulating old runs).
2. **Choose F's route**, F-A (Argoverse 2 via [9]'s archive) or F-B (nuScenes), knowing that F-A changes the paper's statement about [9].
3. Triage each R and S item (`AUTHOR_TRIAGE_v13.md`).
4. Confirm that the C1109 cases with the old runs' three recording margins count as "same generator".
5. Choose the title.

**Account, spend and downloads**
6. Check that the RunPod network volume and its runtime still exist. Create the pods, or authorise a session to use the account; its credentials are in `<excluded folder 3>`, which this session must not open. Top up if needed.
7. For F-B: register with nuScenes, accept its terms, download the `v1.0-trainval` metadata, and confirm where the local CenterPoint results came from.
8. Approve installs: a TeX distribution and Pandoc. Approve any local copy of the fresh sweeps.

**Submission gates (unchanged from v12)**
9. Author block (affiliation, e-mail, ORCID).
10. Repository and DOI. The deposit list must say that the old runs' sweeps were not retained and the fresh runs' are.
11. The "[AUTHOR CONFIRMATION: …]" sentence and the model names per step in the AI-use statement.

**Housekeeping and the next review**
12. Copy Amendments 08, 09 and 10 into `P\11_ojits\`. This session must not change the project folder.
13. Access to paywalled standards, and to full texts for the novelty statement (S2).
14. The cover letter: [9] as a related manuscript, and the shared data if F-A; the AI-use disclosure; which results are confirmatory.
15. Which models run the next ARS review: seats and synthesis on a model other than the writer's, preferably with a cross-family check.
