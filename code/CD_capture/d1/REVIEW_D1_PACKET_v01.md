# Independent review of packet_d1_v13 (A10 §6, D1)

**Verdict: PASS WITH FIXES.** No blocking defect was found in the packet. The capture code, case file and hash bindings are correct and can run as built. Two major items sit outside the packet (scoring of contact-truncated D1 runs; no physical check of the new lead profiles) and should be settled before Lock 2 or before the 105 runs are launched. The rest are minor.

Reviewer: Claude (Fable 5.2), 19 Nov 2026. Nothing was run on the network; no file was changed except this one.

## Checks run

| Check | Result |
|---|---|
| `python -I -B test_d1_policy_v13.py` | PASS; `TEST_D1_POLICY_v13.json` rewritten byte-identical (SHA-256 `f6be715c…`) |
| `make_cases_d1_v13.build()` re-run twice against `CASES_D1_v13.json` | identical (deterministic) |
| Protocol: first 2,223 cases equal the main protocol (SHA `32d683a0…`), last 165 equal the case file, all other top-level keys equal, one key added | pass |
| Ids, seeds, noise episodes over all 2,388 cases | all unique; no D1 seed collides with a main seed |
| Split and speed cycle | per variant 35 `d1_openloop` (12/12/11 at 5/10/15) and 20 `d1_e3b` (7/6/7); the first 35 in id order are the open-loop ones |
| Parameter supports | τ, start in [1, 3]; mild decel in [0.502, 1.468]; stop-and-go decel in [2.118, 5.955] |
| Speed law against my own independent piecewise implementation, 165 cases × 700 frames | max difference 0 |
| Profile completion time | latest 22.0 s (run ends at 29.9 s assessment time), so every profile finishes inside the run |
| Capture → JSON → review replay (my own driver, numpy inputs on the capture side, lists on the review side, `strip_wall` compare), 24 cases × 699 frames | 24/24 equal |
| Negative: capture with plain 746 `ActorRequests`, review with `make_requests` | 24/24 detected at the first frame |
| `check_variant` tamper cases (decel, start, hold, kind, floor, resume) | 12/12 rejected |
| Pod-layout import (scratch `workspace/746…`, `workspace/claude_smoke_v01`), in the review's import order | `ActorRequests` and `Draw` are the same objects; path inserted once |
| Packet: every entry of the binding (smoke part), `SMOKE_MANIFEST` and `PACKET_MANIFEST` re-hashed; file sets compared with packet_main_v03; tar members compared with the folder | all match; only the 3 manifests/binding and the 5 intended files differ from v03; 2 files added; no `__pycache__`; tar SHA equals the receipt |
| Diff of `probe_arms_v01.py` and `review_actor_records_v04.py` against v03 | only the documented lines (docstring, one import, the scene class; one import and the policy constructor) |

Not checked: anything on a pod (CARLA, the PID's physical response), and the D1 analysis scripts, which do not exist yet.

## Answers to the seven questions

1. **Speed laws.** All three match the specification. Constant: `v`. Mild: `max(0.5 v, v − a·max(0, t − t0))`. Stop and pull away: 746 braking law until `t_stop + 3 s`, then `min(v, 1.5·(t − t_stop − 3))`, with `t_stop = t0 + v/b`. Time is the 746 assessment time. Reusing `brake_start_s` (U(1, 3)) for the start in (b) and (c), and `brake_mps2` (U(2, 6)) for (c), is a faithful reading; the mild deceleration has its own U(0.5, 1.5) draw.
2. **Everything else unchanged.** Yes. The D1 subclass overrides only `start()`, whose AST equals the original except for the policy class. Placement, gap, aim, PID, sensors, detector, tracker and planner take the same code path. For a case without `lead_variant` the probe gets `ScenarioActors` itself and the review gets a plain `ActorRequests`.
3. **Actor review.** It passes on a correct D1 capture and fails on a capture made with another policy (requested speed, `reason` and snapshot schema all differ).
4. **Pitfalls.** None found: module identity holds, `None` and floats survive JSON, the frozen `Draw` has a `__dict__`, keyword-only `step` arguments pass through `**kw`, and `strip_wall` handles the added `lead_variant` dict.
5. **Case file.** Deterministic, unique, correctly split. No consumer in the packet reads the case `role`; `lead_variant` is carried in `contract.json` and compared as a whole dict.
6. **Packet build.** Correct; `update_main_packet_v01.py` and `make_release_smoke_v01.py` will accept it. All five changed or added files are bound.
7. **Other risks.** See findings 1–4.

## Findings

### 1. MAJOR (analysis, not the packet): the scoring extractor extrapolates a D1 lead with the hard-braking law
- **File:** `revision_v13\work\F_nuscenes\lib\scoring\ol_extract_v01.py`, lines 40–55 (called at line 180 with `allow_extrap = truncated_by_contact`). I assume the D1 analysis will use this extractor or a copy; I could not confirm which copy.
- **Failure:** in a run that ends at contact, the true lead trajectory after the last recorded frame is rebuilt as `sp − brake_mps2·H` whenever `family == 'lead_braking'` and `t ≥ brake_start_s`. D1 cases keep `family = 'lead_braking'` and a valid `brake_mps2`, so a constant or mildly braking lead, or one that is holding or pulling away, is extrapolated as braking at 2–6 m/s². Clearances for decisions in the last 3 s before contact are then wrong, which shifts the wrong-go shares that D-H1 and D-H2 compare.
- **Size:** only contact-truncated D1 runs, and only their last 3 s of decisions. Probably few runs, but the direction is not neutral between sources.
- **Fix:** before Lock 2, make the D1 extraction use `actor_policy_d1_v01.requested_speed` for cases with `lead_variant` (a wrapper is enough), or record a deviation that excludes extrapolated decisions for D1. `revision_v11\analysis\rev_h_run_facts_v01.py` (lines 36–44) reads the same draw fields and should not be applied to D1 runs.

### 2. MAJOR (operational): the new profiles have never been driven by the actor PID
- **File:** `src\actor_policy_d1_v01.py`, lines 62–72; `737…\actor_pid_v01.py` `ActorPID.step`.
- **Failure:** the request is correct, but the lead's realised motion is untested in two regimes that lead braking never entered: (i) restarting from a standstill after a 3 s `brake = 1` hold, with a request that starts near 0 m/s; (ii) tracking a 0.5–1.5 m/s² ramp with a proportional gain of 1 per km/h, which may brake in pulses. The actor review replays requests and PID outputs, so it passes even if the lead never pulls away. 105 paid runs could then record leads that do not do what §6 describes.
- **Fix:** run the first study job of each variant first (3 jobs) and, before launching the rest, read only the lead-side field `summary.speed_vs_current_request_rmse` and `summary.reasons` from `actor_review.json`. These describe the lead, not the ego's outcomes; the author should confirm that reading them is compatible with §5.2 sealing, or have the status script print a pass/fail on a fixed threshold.

### 3. MAJOR (process): D1 has no reserve cases for the §5.1 failure rule
- **File:** `make_cases_d1_v13.py` lines 29–31; `make_jobs_d1_v13.py` (added while I reviewed).
- **Failure:** §5.1 replaces a twice-failed job with "the next unused case of the same family and speed". Each variant has exactly 35 open-loop cases and the next 20 belong to E3b. A second failure leaves either a short cell or an undeclared draw from E3b's cases.
- **Fix:** decide now and write it down: either report the cell short, or take the replacement from the end of the E3b block (case 54 downwards, same speed) and tell the E session. A new amendment line is needed in both cases.

### 4. MINOR: D1 runs can be mistaken for fresh lead-braking runs
- **File:** `make_jobs_d1_v13.py` lines 39–40 and 56.
- **Failure:** D1 jobs carry job `role = 'eval'`, draw family `lead_braking`, and land in the same volume folder as package C (`claude_v13_cd_v01`). An analysis that selects C's lead-braking runs by family or role would pool 105 D1 runs into H0–H5 and D2.
- **Fix:** select C runs by the id list in `CASES_C_v13.json` (or by `phase == 'PC13'`), and assert in the loader that no selected case has `lead_variant`. A separate volume folder for D1 would also do.

### 5. MINOR: the 3 s hold is a hold of the request, not of the vehicle
- **File:** `src\actor_policy_d1_v01.py` lines 69–72.
- **Failure:** `t_stop = t0 + v/b` is when the request reaches zero. If the lead cannot realise `b` (up to 6 m/s²), it stops later and stands for less than 3 s.
- **Fix:** none needed in code; state in the methods text that the hold is of the commanded speed, and report the realised standstill duration.

### 6. MINOR: E3b's cases are authorised for open-loop capture
- **File:** `DEVELOPMENT_PROTOCOL_D1_v13.json`; `make_release_smoke_v01.py` line 28 (unchanged).
- **Failure:** the release authorises all 2,388 cases, so a job-list slip could record a `d1_e3b` case open-loop. `make_jobs_d1_v13.py` filters on `role == 'd1_openloop'`, which is the only guard.
- **Fix:** keep that filter and add an assert that no job case has role `d1_e3b`.

### 7. MINOR: package C jobs run after the switch carry the D1 packet's hashes
- **File:** `tools\remote_update_and_work_v01.sh`; `build_packet_d1_v13.py`.
- **Failure:** once a pod is switched, a C retry or replacement records protocol SHA `8822ae4d…` and the D1 binding, while §5.1 and §1 name the main protocol `32d683a0…` and packet_main_v03. Behaviour is identical for those cases, but a sealing or loader check on the protocol hash would reject them.
- **Fix:** finish all C jobs, including replacements, before switching a pod; or record the equivalence (the first 2,223 cases are equal and the code path is unchanged) as a deviation.

### 8. MINOR: stale documentation and provenance inside the packet
- **File:** `build_packet_d1_v13.py` lines 39 and 50.
- **Failure:** `CHECK_REPORT_v01.md`, `diffs\probe_arms_v01.diff` and `diffs\review_review_actor_records_v04.diff` are copied from v03 and no longer describe the probe and review in this packet. `binding['main_packet']` is overwritten, so the v03 change list is lost from the binding.
- **Fix:** optional. Add a `D1_CHANGES.md` or regenerate the two diffs, and keep the old record under `main_packet['parent']`.

### 9. MINOR: the laptop test's reference law is a copy of the implementation
- **File:** `test_d1_policy_v13.py` lines 39–46.
- **Failure:** check 2 would pass if both copies shared an error. My independent implementation agrees exactly, so there is no error now.
- **Fix:** optional; write the reference as explicit phases.

### 10. MINOR: the case file embeds the policy's hash
- **File:** `make_cases_d1_v13.py` line 81.
- **Failure:** any edit to `actor_policy_d1_v01.py` (even a comment) makes `CASES_D1_v13.json` state a stale `actor_policy_sha256`. The protocol itself is unaffected.
- **Fix:** if the policy file changes, rebuild the case file and the packet before hashing at Lock 2.

### 11. MINOR: longer runs and storage
- **File:** `make_jobs_d1_v13.py` line 56 (`capture_timeout_s = 600`, `keep_raw = true`).
- **Failure:** constant and mild leads rarely end in contact, so most D1 runs are full 700-frame runs, with both `clean/` and `raw/` sweeps kept. That is the upper end of capture time and archive size per run.
- **Fix:** check a full-length C run's wall time against the 600 s timeout and the volume's free space before launching.
