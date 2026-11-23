# PLAN for revision v13 of the OJ-ITS paper (accept-ready scope)

Written 19 Nov 2026 by a planning session started from the v12 review session (Claude Opus 5.5, model id `claude-opus-5-5`, in `ARS_TRIAL`).
- First version: 11:47 EST.
- **This version: 12:01 EST.** It follows the requesting session's scope change: the user chose "Push for 5 stars".
  - Package D (non-braking leads; event-level table) is now required.
  - Packages E (closed loop in CARLA) and F (real-sensor replication) are added.
  - Cut-in is added as a second scenario family.
  - Both outcomes of the varying-covariance arm must be publishable.
  - The length is planned now.

**Status.** A plan for the author's approval. Nothing has been run, rewritten or computed. `revision_v12\`, `review_v12_output\` and the project folder were read only.

Companion files:
- `AMENDMENT_10_v13_DRAFT.md`: pre-registration of B, C, D, E and F.
- `FEASIBILITY_v13.md`: what exists, compute and cost per package, what only the author can do.

## 1. Aim and the one take-away (R1)

The v12 review (about 3.5 stars) says rewording no longer moves the score. An accept-ready paper needs evidence that the panel could not get from the same 35 runs. The plan supplies it on four fronts:
1. **Fresh runs** under a plan locked in advance (C), in two scenario families: lead braking and cut-in.
2. **A tracker whose covariance varies** (B1, an IMM), scored with a ceiling that makes either outcome interpretable.
3. **A closed-loop test** in CARLA with the margin sources driving the car (E).
4. **A real-sensor replication** of the open-loop test (F).

Non-braking leads (D1) test the conditions under which the braking prediction and the phase schedule are quoted.

**Proposed take-away.** Final wording follows the outcome branches fixed in Amendment 10 §9:

> A perception output earns decision value only under a score that can detect better information at the output's own amplitude and that states its commitment, population and recording policy. Under such a score, on fresh simulated runs, in closed loop and on real driving logs, [a fixed-noise Kalman tracker's covariance is equivalent to a class-average margin] and [a covariance-varying (IMM) tracker's covariance recovers k% of what perfect ranking at its own amplitude would recover].

**Why either IMM outcome is publishable.** The paper reports the IMM's share beside a ceiling: an oracle that varies by exactly the IMM's own amplitude but ranks decisions by the realised error (E5_IMM). This turns the result into one of four findings:
- **IMM recovers room:** a covariance that varies with the manoeuvre has decision value, and the paper sizes it against its ceiling.
- **IMM recovers nothing, ceiling large:** the IMM varies enough to matter but not in step with the error. The bottleneck is the information in the covariance, not its amplitude.
- **IMM recovers nothing, ceiling also small:** even perfect ranking at that amplitude recovers little. The amplitude limits it, and a covariance margin cannot carry this room.
- **IMM's covariance barely varies:** the stated reason, measured.

Each is a result a reader can use. The same structure applies on real logs (F), where Poly-MOT's CTRA covariance also varies.

**What becomes confirmatory.** Only the pre-registered hypotheses on data not used for any design choice:
- C: lead-braking H0–H5 and cut-in K0–K2;
- D1: hypothesis D-H1;
- E: the closed-loop classifications E-H1 to E-H3;
- F: real-log hypotheses F-H0 to F-H2.

Everything on the 35 old evaluation runs and the 20 tuning runs stays exploratory.

## 2. Order of work and gates

| Step | What | Where | Gate |
|---|---|---|---|
| 0 | Author reads plan, amendment and feasibility; confirms defaults (A10 §12); decides F's route (FEASIBILITY §6: Argoverse 2 via [9]'s archive, or nuScenes); triages each item | — | Author's written approval |
| 1 | **Lock 1:** approved amendment and defaults hashed in `LOCK_A10_1.txt` | `revision_v13\` | Before any value |
| 2 | **B** on the laptop: identity; IMM, adaptive Q, re-tuned CV, CA; E5 and the amplitude-matched ceilings; terciles; cut-in event and track-age development on the 20 cut-in tuning runs | Laptop | Lock 1 |
| 3 | **E build** (free): controller fix F2, brake-test script, closed-loop arms (F0, CK3, TG, phase schedule, online IMM), new packet; laptop checks; independent code review | Laptop | Lock 1 |
| 4 | **D1 build** (free): three non-braking lead variants in a new, reviewed actor-policy version | Laptop | Lock 1 |
| 5 | **F build** (free): adapter for the chosen real-log route; design-split checks only | Laptop | Lock 1; author's F decision (and nuScenes terms, if that route) |
| 6 | **Lock 2:** freeze all trackers, arms, variants and adapters (hashes, tuned constants, matched closed-loop settings) | `revision_v13\` | After 2–5; before any fresh or held-out value |
| 7 | **Pods** (author starts them): C (210 runs, sweeps kept), B7 offline detection, D1 (105 runs), E1 brake test (cap $3), then, only if it passes, E2 calibration (F0 only) and E3 main runs | RunPod | Lock 2; E2/E3 also need the E1 pass |
| 8 | **Scoring once:** C, D1, E and F held-out, by the locked scripts | Laptop | Archives sealed until then |
| 9 | **Recount** by independent second programs (A10 §10.1), hand-check subset, second IMM implementation | Laptop | After the last first-program output |
| 10 | **A:** rewrite and cut, from generators only | `revision_v13\draft\` | After 9 |
| 11 | **Claim audits:** the final text by a model other than the writer; fixes; delta audit; package build | `notes\`, `package_v13\` | — |
| 12 | Next ARS review on a model different from the writer's | New folder | Author's choice |

E is a staged ladder with its own stop rules (A10 §7). If its brake test fails, E is reported as attempted and stopped, with the reason; the rest of the plan does not wait for it.

## 3. Every roadmap item, mapped

Package key:
- **A**: text.
- **B**: offline, stored data.
- **C**: fresh runs, locked.
- **D**: non-braking leads and event-level table (required).
- **E**: closed loop.
- **F**: real logs.

"Triage" is my proposal; the author's call is final.

### Required items R1–R13

| Item | Packages | What is done | Lands in | Triage |
|---|---|---|---|---|
| R1 One take-away | A (after all) | Re-centre on the protocol; the null as the worked example; three contributions; exploratory results in one labelled table | Title, Abstract, §I, §VII | Address |
| R2 A covariance that varies | B + C + E + F + A | B1 IMM (and B2 adaptive Q) frozen and scored on fresh runs (H3) with its amplitude-matched ceiling; online IMM as a closed-loop arm (E); Poly-MOT on real logs (F). NA renamed "output-scalar NIS inflation" | §III, Table I, §V-B, Abstract | Address |
| R3 Length | A | 10-page budget (§5); supplement to what the main text needs (§6); typeset count from the IEEE open-journal template already in Downloads (FEASIBILITY §7) | Whole paper | Address |
| R4 Abstract numbers in main tables | A | Every abstract, §I and §VII number traces to Tables II–V, enforced by the number-source check | Tables II–V | Address |
| R5 The control's scope | B + C + A | E5 (±5%, rank-matched) and E5p; criterion fixed before computing (H1); "not a blunt measure" limited | §IV-B, §V-A | Address |
| R6 One estimand | C + A | Gridless share primary; one calibrated interval; δ fixed (H2); 2.2 retired | §IV-B, §V-A | Address |
| R7 Held-out per-phase figures | C + A | Schedule chosen on the old runs, the tracker's own phase estimate, applied once to fresh runs; record basis primary (H4) | §V-D, Table II | Address |
| R8 Confirmatory status | C + D + E + F + A | Fresh runs, held-out real logs, closed loop; "confirmatory" only for hypotheses that passed | Abstract, §I, §IV | Address |
| R9 Transfer sentence | C + F + A | Tuning-run intervals; the Limits sentence lists only orderings that hold in all run sets (tuning, old, fresh, and real logs where defined) | §VI | Address |
| R10 Filter tuning | B + A | B3 (NIS near 2) and B4 (CA); lag, room by phase, CK3 share | Table III, Limits | Address |
| R11 The 83% condition | D + A | D1 measures the braking prediction's cost behind leads that do not brake hard (D-H1); the abstract states the condition with that result | Abstract, §I, Table V | Address |
| R12 The 12% assumptions | B + C + E + A | Terciles of lead deceleration; a delayed, variable stop; E replaces the perfect stop with the car's own closed-loop braking | Abstract, Tables IV–V | Address |
| R13 Rate and latency | B (pod) + A | 2, 5 and 10 Hz with stated latency on the fresh runs' kept sweeps (old sweeps were not kept) | Table V, Abstract | Address |

### Suggested items S1–S25

| Item | Packages | What is done | Triage |
|---|---|---|---|
| S1 Pooled vs after-stop length | A + C | Clause in the abstract; per-phase columns in the supplement table | Address |
| S2 Queries; full texts; references | A | Queries and engines listed; abstract-level novelty statement; suggested references checked by identifier | Address |
| S3 Readable abstract; title | A | Three results, one defining sentence; title options (§5) | Address |
| S4 Fewer labels | A | Notation table to the supplement; each fence once in Scope and once in Limits | Address |
| S5 One interval type | A + C | Calibrated intervals where the plan requires them; basis labels | Address |
| S6 Provenance paragraph | A | One paragraph; "AI-based review panel", "AI session" | Address |
| S7 Internal identifiers | A | Removed; a build check | Address |
| S8 Same claims, same order | A | One claims list feeds the Abstract, §I and §VII | Address |
| S9 2.2 wording | A | Retired (H2 replaces it) | Address |
| S10 Hand-check; second program for N's intervals | C | A10 §10.2 and §10.1 | Address |
| S11 Caution windows | C | Fixed sensitivities | Address |
| S12 Decision-equivalents where shares do not grade | A + C | Grading check per printed population | Address |
| S13 Run-level after-stop breakdown; staleness vs smoothing | B | B8 and B7 | Address |
| S14 Ratio spread vs heading and age; benign | B (cut-in part) + A | Track-age and event analysis in cut-in (K-family); §V-E shortened, the ratio table moved to the supplement | Address |
| S15 Cut-in carry-over | C (K-family) | Cut-in tested on fresh runs at the event and by track age | Address |
| S16 NIS and NEES per phase | B | B8 | Address |
| S17 The 435.2 row | A | From the generator or cut | Address |
| S18 Non-braking leads | **D1 (required)** | Constant speed, mild braking, stop and pull away; open loop (D-H1) and closed loop (E3b) | Address |
| S19 Event-level table | **D2 (required)** | Runs with contact and impact speed by source at two matched cautions; plus E's closed-loop contacts and impact speeds | Address |
| S20 Do not remove margins | A | Abstract and §VII | Address |
| S21 R157 status; 6 m/s² vs AEB/ACC | A | Adopted text and amendment status from the R157 PDFs already in Downloads; relation stated | Address |
| S22 TG+N, TG+F0 | D3 (optional) | Combined arms | Consider |
| S23 Fallback share / R157 unit | A | Dropped with S3 | Address |
| S24 Phase schedule is a diagnostic | D1 + E + A | Tested behind non-braking leads (D1) and in closed loop (E); wording by rule | Address |
| S25 Standards | A | ISO 15622, ISO 22179, UN R152, IEEE 2846 | Address |

### Other open points

| Point | Package | What is done |
|---|---|---|
| DA C1 | B–F + A | All three repairs, plus closed loop and real logs |
| Recount gap; no second claim audit | A10 §10 | Recount covers every printed value; nothing computed after it; audit of the final text by another model |
| **Data Availability statement wrong** (found here) | A | The old runs' sweeps were not kept, except run 0037 (FEASIBILITY §3). Corrected; the fresh runs keep theirs |
| Contribution 4's carry-over claim | C (K-family) | Cut-in tested, not assumed |
| Companion [9] separation | F (author decision) | If F uses [9]'s Argoverse 2 archive, §I and the cover letter state the shared data. The v12 sentence "none of its data, results or figures is used here" is then changed. Otherwise F uses nuScenes |

## 4. The packages in brief

Definitions, seeds and rules: Amendment 10. Time and cost: FEASIBILITY §4 and §8.

**A (text).** v12 build pipeline (parts and generators; no number typed into the text).
- **Response letter** on the ARS template.
- **Author triage** recorded in `AUTHOR_TRIAGE_v13.md` before writing.
- **Revision method.** The ARS revision-mode patch protocol suits targeted revisions. v13 restructures nearly every block, so the response letter says why the build pipeline is used instead.

**B (offline, stored data; exploratory).** All at 2 Hz on the laptop, except B7 (5 and 10 Hz, on the fresh runs' kept sweeps, on a pod).
- **B0:** identity check.
- **B1:** IMM (CV/CA).
- **B2:** innovation-adaptive Q.
- **B3:** CV re-tuned to NIS near 2.
- **B4:** CA.
- **B5:** E5 and the amplitude-matched ceilings.
- **B6:** deceleration terciles and a delayed stop.
- **B7:** update rate and latency.
- **B8:** diagnostics.
- **B9:** cut-in event and track-age development on the 20 cut-in tuning runs.

**C (fresh runs; confirmatory).**
- **Runs:** 105 lead-braking and 105 cut-in runs from the never-run evaluation cases (35 per desired speed in each family), recorded exactly as the old evaluation runs were; all sweeps kept.
- **Plan:** one locked plan, scored once.
- **Lead braking:** H0 room; H1 grading at the tracker's amplitude; H2 N equivalent; H3 IMM classified against its ceiling; H4 per-phase schedule transfers; H5 braking prediction.
- **Cut-in:** K0 room at the event; K1 N equivalent at the event; K2 young tracks (where the covariance does vary) classified.

**D (required, plus optional parts).**
- **D1:** non-braking leads, 105 fresh runs:
  - constant speed;
  - mild braking;
  - stop and pull away.
  - Open-loop wrong goes and caution of the braking prediction, the phase schedule and TG against F0.
  - Also driven in closed loop in E3b.
- **D2:** event-level table, required.
- **D3 and D4** stay optional.

**E (closed loop in CARLA; staged).**
- **E0:** build: the controller fix F2, without which the car does not brake as the planner assumes; the arms.
- **E1:** brake test, cap $3, with a pass rule pre-set on 10 November.
- **E2:** F0-only calibration on tuning cases, to place two matched levels.
- **E3:** main runs. Arms: zero margin, F0, N, CK3, TG, the phase schedule on the tracker's own phase estimate, and the online IMM with its own class average. 60 fresh lead-braking cases at two matched levels; E3b runs the D1 variants.
- **Outcomes:** contacts, impact speed, time lost, peak deceleration, jerk and fallback share.
- **Settings:** matched by a rule fixed now (open-loop caution on the design runs).
- **Classifications per arm:** "safer at no cost", "trade-off", "equivalent", "worse" or "inconclusive".

**F (real sensors; author chooses the route).**
- **F-A, Argoverse 2:**
  - Uses companion [9]'s archive: CANMOT and Poly-MOT tracks with covariances on 375 real logs; 225 held-out logs never read for this question; laptop only; code largely exists.
  - It reuses [9]'s data, so it needs the author's consent and a changed statement in the paper.
- **F-B, nuScenes:**
  - Independent of [9]. CenterPoint nuScenes detections are already in Downloads; CANMOT runs on nuScenes natively; laptop only.
  - Needs the nuScenes metadata (the author's account and terms) and a new adapter.
- **Common plan:** the same equal-caution test, with design data and held-out data separated, and the hypotheses F-H0 to F-H2.

## 5. Length plan: the main text (R3, R4)

**Budget.** About 10 IEEE two-column pages:
- whole manuscript ≤ 8,500 words (v12: 12,451);
- body without tables, captions and references ≤ 5,300 (v12: 8,926);
- tables and captions ≤ 1,400;
- references ≤ about 40;
- abstract ≤ 220.

The typeset count comes from the IEEE open-journal template (`Downloads\IEEE-open-journal-template.zip`, `ieeetj.cls`) once a TeX toolchain exists (FEASIBILITY §7).

**Title options** (author's choice):
1. "Do Tracker Covariances Improve Planning Decisions? An Equal-Caution Test on Fresh Simulation Runs, in Closed Loop and on Real Driving Logs"
2. "What an Open-Loop Decision Score Must State: Tracker-Covariance Safety Margins at Equal Caution"

| Section | Words | Content |
|---|---|---|
| Abstract | ≤ 220 | Take-away; protocol in one sentence; confirmatory results by name (fresh runs, cut-in, closed loop, real logs); one exploratory sentence with its conditions; "does not justify removing a margin" |
| I. Introduction | 600 | Problem; three requirements; three contributions: (1) the protocol with an amplitude-matched control; (2) the confirmatory test across fresh runs, closed loop and real logs, including a varying covariance; (3) what the score depends on (exploratory) |
| II. Related work | 600 | Decision-level perception metrics; uncertainty into planning; adaptive covariances (IMM, adaptive Q, fading factors); ACC/AEB standards and RSS |
| III. Test beds and sources | 900 | CARLA lead braking, cut-in and non-braking leads (three run sets); real logs; closed loop with the braking fix; trackers (online CV, IMM, adaptive Q, re-tuned CV, CA; Poly-MOT on real logs); planner; Table I (sources) |
| IV. Scoring and plan | 750 | Wrong go, caution, gridless frontier, room, share; the grading criterion and the amplitude-matched ceiling; populations (incl. cut-in event window, track age); intervals; the locked plans; one provenance paragraph |
| V-A. Confirmatory open-loop results | 600 | **Table II**: columns lead braking (fresh), cut-in (fresh, event window), real logs (held out); rows: room, grading, N, IMM with its ceiling, schedule, CK3. **Fig. 2**: frontiers |
| V-B. Trackers whose covariance varies | 400 | **Table III**: per tracker variant: NIS, ratio spread, share, ceiling, room by phase, lag |
| V-C. Closed loop | 450 | **Table IV**: per arm at two matched levels: contacts, impact speed, time lost, deceleration, jerk; the D1 variants. **Fig. 3**: contacts against time lost |
| V-D. What the score depends on (exploratory) | 450 | **Table V**: commitment, stop deceleration terciles, delayed stop, rate and latency, filter tuning, non-braking leads (open loop), recording policy across run sets. **Fig. 4** |
| VI. Discussion and limits | 500 | Why the null; what an adaptive covariance needs; which reading of the commitment applies (now measured in closed loop); limits stated once |
| VII. Conclusion | 150 | Findings, then next steps |

Five tables and four figures. Old Table V (margin ratio by family) and the old Fig. 2(b) move to the supplement, with one sentence each in §V-B.

## 6. What the supplement keeps, moves in, and drops

**Target:** ≤ 15,000 words (v12: 34,240). It keeps only what the main text cites.

| Supplement section | Content | Why |
|---|---|---|
| S1 Configuration | Table S28 (recording, detector, tracker), the three run sets, the fresh cases, the D1 variants, the closed-loop build (F2, arms), the real-log route | Reproducibility |
| S2 Definitions | Notation table, interval mechanics, calibration, resolution rules, the gridless frontier, E5 and the ceilings, the matched-setting rule | Moved from §IV |
| S3 The locked plans | Amendment 10 in brief; locks and hashes; deviations table (Table S4, deviations only) | Required by R8 |
| S4 Tracker variants | IMM, adaptive Q, re-tuned CV, CA: tuning, NIS and NEES per phase, ratio spread, B0 identity | R2, R10, S16 |
| S5 Lead braking, full tables | Per-phase and populations, grid and hull, caution windows, signed caution, after-stop truncation, the per-phase schedule both bases and thresholds, tuning-run intervals, the old-run (v12) values marked exploratory | R6, R7, R9, S1, S5, S11, S12 |
| S6 Commitment and rate | Reaction-and-stop grid, terciles, delayed stop, 2 m gap, stop reliance, B7 full grid | R12, R13 |
| S7 Cut-in | Event definition, track-age strata, ratio around the event, K-family details | S14, S15 |
| S8 Non-braking leads | D1 variants, open-loop and closed-loop tables; D2 event-level table | S18, S19 |
| S9 Closed loop | Brake test, calibration runs, all outcomes per arm and level, per-case table | E |
| S10 Real logs | Route, adapter checks, design and held-out split, all outcomes | F |
| S11 Ratio check by family | Old Table V and the ratio figure | Contribution 4's reach, one sentence in the main text |
| S12 Verification | Recount coverage and agreement, file-time order, hand-check subset, second IMM implementation, claim audits, the models that ran each step | R8, S10 |
| S13 Literature search | Queries and engines | S2 |

**Dropped:**
- The v12 S3 closed-loop check on the simplified simulator, superseded by E. If E stops at the brake test, a short note on that check returns, with its limits.
- The v12 S9.
- The draft history.
- Figs. S2–S4 unless cited.
- Every "added in revision" label and internal identifier.

## 7. How the headline changes with the outcomes

Each branch, with its wording, is fixed in Amendment 10 §9. The principle: every hypothesis has a reportable result in each direction. Two kinds of outcome remove a claim:
- an outcome that removes a claim also removes its numbers from the abstract;
- an outcome that cannot be evaluated is reported as such, never filled in.

## 8. Model record

- **This plan and its companions:** Claude Opus 5.5 (`claude-opus-5-5`).
- **Planned writer of v13's first programs and text:** Claude Opus 5.5, unless the author chooses otherwise.
- **Second programs, the second IMM implementation and the claim audit of the final text:** by default a different model (for example Claude Sonnet 5.5 or Claude Fable 5.2).
- **Next ARS review:** every seat and the synthesis on a model other than the writer's. The requesting session confirms it will not write v13. A cross-family check is recommended.
- **Record keeping:** v13's README and AI-use statement name the model per step.

## 9. What the author decides before Lock 1

All items, with defaults, are in Amendment 10 §12 and FEASIBILITY §10.
- **Margins and runs:**
  - δ (default 0.05 of the room);
  - fresh runs per family (default 105);
  - latency (default 0.1 s).
- **Closed loop (E):** whether to start it, accepting a brake-test pass chance that the project's own lead put at one in three to one in two.
- **Real logs (F):** the route, Argoverse 2 via [9]'s archive or nuScenes; for nuScenes, registering and accepting its terms.
- **Title.**
