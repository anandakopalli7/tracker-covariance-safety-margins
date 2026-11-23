# Review of package E's build (A10 §7.1 step E0), v01

Reviewer: Claude Fable 5.2 (independent of the writer, Claude Opus 5.5). 19 Nov 2026, 15:55 EST. Code reviewed: `src\` as of 15:47 EST (including the `_json_safe` change to `e_arms_v01.py`), tools, analysis, tests, and `packets\packet_e_v01`.

## Verdict: PASS WITH FIXES

The arms, the F2 servo, the track history and the brake-test rule are correct against their sources of record. **`packet_e_v01` as built must not be sent to a pod** (B1). After B1 and M1–M3, the CANMOT stages (E1S, E1, E2) may start. The IMM arms and E3/E3b need M4–M6 first.

## Findings

### Blocking

**B1. `packet_e_v01` is stale and holds a crash in E_PS.**
- `packets\packet_e_v01\claude_smoke_v01\e_arms_v01.py:238` writes records with `allow_nan=True`; `probe_e_v01.py:101-104` appends with `allow_nan=False`. A NaN `ahat_long` in `phase_info` (`e_sources_v01.py:236`) then raises outside `policy_call`, so the capture dies with `exception.json`, and the deterministic retry dies again.
- I measured how often: 4 of 12,907 decisions in the 55 stored lead-braking runs carry a NaN (`review\scratch\out\CHK_PS_NAN.json`). That is roughly one E_PS run in 14 lost, and its pair dropped.
- `src\e_arms_v01.py:181-189, 248` fixes it. The packet does not have the fix.
- The packet's `trackers_b\trk_tracker_v01.py` (17d519…) is older than `src\` and session B's copy (5cf4ad…), and `trk_constants_v01.json` and `E_PBAR_IMM_v01.json` are absent, so both IMM arms fail at start.
- Fix: build `packet_e_v02` from `src\`; rerun `test_e_exec` and `test_f2_servo` against it; record the new tar hash.

### Major

**M1. Nothing enforces the $3 brake-test cap.** `tools\acquire_e_v01.py:51` defaults `--deadline-h 10` (about $8.90 on an RTX 4090 at $0.89/h). I did not read the watchdog itself. Fix: launch the E1 pod with `--deadline-h 3` or less, and state whether E1S's cost counts inside the $3.

**M2. E1S is a paid step that A10 does not contain, and it is not recorded.** A10 §7.1 lists E0 as free. `make_jobs_e_v01.py:78-86` runs 8 paid jobs with F2 on a lead-braking case before the brake test. The split is defensible (a build fault is not a brake attempt), but `STATUS.md` departures 1–5 omit it. Fix: record it as departure 6 before the pod starts, with the rule that no E1S outcome is read and that F2 and the packet are hash-frozen before E1S, so E1S cannot inform a change to F2.

**M3. `max_attempts: 2` lets the worker rerun a brake run by itself.** `make_jobs_e_v01.py:65` applies it to the E1 list; `worker_main_v01.py:410` retries any launched job whose status is not `CAPTURED_AND_REVIEWED`. With lists `a1` and `a2` that allows four runs per speed. Fix: `max_attempts=1` for E1 lists, so each attempt is explicit and the "fault, not a result" judgement is made by a person.

**M4. The IMM arms are never run on a pod before the 900-run E3.** `make_jobs_e_v01.py:74` smokes the six CANMOT arms only. `e_imm_v01.py:30-34` calls `trk_env.setup`, which calls `fast_overlap_array.install()` a second time (the probe already does at line 92) and rebinds CANMOT's filter factory; none of this has run on Linux. Fix: a two-job IMM smoke list before E3, after `FREEZE_B`.

**M5. The contact rule "truth gap ≤ 0" has no lateral test.** `e_outcomes_v01.py:72` uses `directional_gap_m`, which `evaluation_geometry.py:53` labels "not a collision test" (longitudinal only). For in-lane leads this is right. If any D1 variant of E3b lets the lead leave the ego's lane, passing it counts as a contact. Fix: check D1's variants before E3b; if any is off-lane, record the lateral condition as a departure.

**M6. Newcombe's interval is not the published method 10.** `e3_analyse_v01.py:55` uses the plain φ. Newcombe (1998) and Fagerland et al. (2014) correct the numerator (ad − bc − n/2 if above n/2; 0 if between 0 and n/2; unchanged if negative). The plain form gives narrower intervals under positive correlation, which is the expected case for paired runs, and E-H1 to E-H3 are decided by the interval ends. I state this from memory of the papers, not from a copy. Fix: verify against the source and correct before Lock 2b.

### Minor

1. `e1_brake_v01.py:53` reports `fallback_before_forced` but does not fail on it. A natural fallback before tick 199 would move `kf` and void the distance.
2. `tests\test_e_arms_v01.py:203` (C1) compares the online phase with `zl['phase']`, which is not the estimated phase; hence 288/300. `test_ps_phase_v01.py` is the valid check (9,307/9,307). `STATUS.md` departure 1 cites the wrong test.
3. `make_jobs_e_v01.py:208` looks for `revision_v13\locks\LOCK_A10_2b.txt`; the folder is `work\locks\`. It fails loudly.
4. `e2_matched_v01.py:121-122`: g_lo and g_hi can be the same grid value, or g_lo can be 0. A10 is silent; stop and ask (§11) rather than run duplicate levels.
5. `e2_matched_v01.py:112` defaults a row without `valid` to valid. `e_collect_v01.py` always sets it; make it required.
6. `e2_matched_v01.py:148`: if an arm's curve cannot reach F0's caution, the nearest end is taken silently; `abs_diff` is stored but not checked.
7. `e_outcomes_v01.py:81-83`: impact speed uses velocities at the contact tick (possibly after the impulse) and always against the primary actor.
8. `e_outcomes_v01.py:122`: fallback share counts the `fallback` flag only; a (−5, −5) row chosen as a feasible candidate is not counted.
9. A failure in `e_track_history` is not a stage `prefix_contract_v01.py:6-7` knows; the review then fails and the run is marked failed, which is the right result by accident.
10. `test_e_arms` has been run on 6 of 65 runs. Run `--all` before the freeze.
11. `acquire_e_v01.py:50` allows an L4 beside the RTX 4090. The admission controls protect bit-identity, but E2's cases are dealt across pods.

## Answers to the ten questions

**1. Arms: yes.** `e_arms_v01.py:203-213` rebinds the constraint builder in both `consumer.build_library` (16 rows) and `finite_primitive.build_library` (the local primitive), as the packet's `fixed` arm does, so no row keeps the native p or d. `consumer.feasible` (`consumer.py:42-59`) then tests d ≥ 0 and α·p ≤ d² with β = 0. Sources match line for line: F0 = `ol_gateR_core_v01.s_P` (lines 206-216), CK3 = `oxsb_extract_v05.py:74-86, 132-147` (shifted d, F0's s), TG = (2 + v_e)², PS = scale × s_F0 with α = 1. Sorting, cost and fallback are untouched. Evidence: critical scales bit-equal to the stored arrays on 26,571 rows (six runs), and the real policy picks the open-loop row in every decision at five scales (`TEST_E_ARMS_s*`). P̄ and the car model equal the files of record by value.

**2. History: yes.** `OnlineHist` (`e_sources_v01.py:140-211`) keys events by (track, timestamp) and tracks by detector index, as `ox12_core_v01.Hist:86-110`; `a_hat_vec` is identical to `oxsb_core_v01.py:104-114`. The feed (`probe_e_v01.py:281-284`) runs after `tracker.step` and before the same tick's decision; detector ticks are odd, so the decision sees the update, as in the open-loop logs.

**3. PS lead: acceptable.** The online rule gives the same track in 9,306 of 9,307 decisions and the same phase in all, at all three thresholds. It is untested on non-braking leads. The triple rule in `e2_matched_v01.py:37-63` is a verbatim copy of `a9_3_phase_scale_cv_v02.triple_choice`, on §5.5's design set. Reading the level as F0's caution at g_L is faithful.

**4. F2: yes, term for term** (`e_arms_v01.py:116-160` against `surrogate_v01.py` FixServo and `feedforward`), including the feed-forward inside the anti-windup test, stop-hold and the warm-up rule. Index 0 at tick k and 1 at k+1 follow from `sensor_execution.py:53-58`. The two-tick reference and the applied/direct check are inherited. My rerun: 0 mismatches in 1,383 ticks.

**5. Brake test: yes.** Forced fallback from tick 199 copies the stand-in's STOP mode (`eval_fixes_v01.py:104-131`) and its `model_stop`. Benign cases are defensible. See M1–M3 and Minor 1.

**6. Probe and worker.** Every diff is intended and documented. A policy failure still ends as `CAPTURED_AND_REVIEWED`, exactly as in the original (`audit_physical_outcomes_v01.py` passes such runs). The protection is downstream: `e_collect_v01.py:52` and `e1_brake_v01.py:72` mark them invalid. A crashed review gives exit 2 and `INCOMPLETE_OR_FAILED`. Crash paths: B1 and M4.

**7. Outcomes and matched settings** follow the text. My different readings: M5, M6, Minor 4–8; also contact is restricted to the assessment window, with warm-up contact invalid.

**8. Packet.** For `packet_e_v01`: 337 files; the 11 added and 5 changed files are the intended ones; all other files are byte-identical to `packet_main_v03`; every `.py`/`.json` under `claude_smoke_v01` is bound except the two `JOBS_*` files and the binding itself; tar, manifest and receipt agree. Both bootstrap scripts walk `SMOKE_MANIFEST` and accept subfolders. But see B1.

**9. Tests.** A2, B1, the F2 test and the PS phase test are real tests against independent references. Weak: C1 (Minor 2); the IMM replay compares the library with itself through two call paths, on an unfrozen library; `test_e_exec` checks the call sequence only. Untested: E_PS's decisions against the schedule rule, the review's E-record stage, the worker's job validation.

**10. Other.** Nothing further found that would silently invalidate a run.

## What I ran, and what I did not check

Ran (outputs in `review\scratch\`):
- `chk_packet.py`: packet against base, tar, binding, manifest, receipt.
- A copy of `test_f2_servo_v01.py`: all equal; ratios 1.024, 0.991, 0.981.
- A copy of `test_e_exec_v01.py` (the pre-15:47 test file, against the current dev packet): OK for all seven arms (0 problems; 300 records each; E_BRAKE 250 forced fallbacks).
- `chk_ps_nan.py`: 155 stored runs, 40,952 decisions.

Not run or not checked:
- `test_e_arms`, `test_ps_phase` and `test_imm_replay`; I read their code and stored outputs only.
- Anything on Linux, in CARLA or on a pod.
- `pods_e_v01.py` beyond its first 80 lines; `fetch_e_v01.py`; session B's tracker arithmetic; `rev_common_v01` and `optA_lib_v02` internals.

Two things to disclose:
- A recursive text search I started in `<earlier-phase folder 2>` ran about two minutes before I stopped it. That tree contains `<excluded folder 1>` and `<excluded folder 2>`. I cannot tell whether the search reached them. It printed nothing from them and I used nothing from them.
- A syntax check wrote `__pycache__` folders into `src\` and `src\review\`. I removed them within a minute; `src\` again holds its 14 files.
