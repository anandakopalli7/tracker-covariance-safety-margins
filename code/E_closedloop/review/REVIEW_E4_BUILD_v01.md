# REVIEW_E4_BUILD_v01: cross-model build review of packet v04 (set E4, detection dropout)

Reviewer: Fable 5.2 (independent of the author). 21 Nov 2026, about 14:50 EST. No source file was edited.
This version includes the coordinator's update (final law of A11 §6c, punish_num = 3, `E4_V04_DIFF_v02.patch`, the v02 test outputs).

## Verdict: PASS WITH FIXES, and one blocking finding outside E's code (B1)

- E's code in `src_v04` implements the final law and the dropout effect correctly.
- No E4 run may be captured until B1 is closed: F's mask function is still the first wording and does not equal E's.
- Four major findings should be fixed in the packet before the freeze (M1–M4). M5 is a note for the analysis.

## State reviewed

- `review\E4_V04_DIFF_v02.patch` (14:22:15). Its `e_dropout_v01.py` equals `src_v04\e_dropout_v01.py` (SHA-256 7f738134…). Its other hunks equal those of the v01 patch.
- `packets\dev_packet_e_v04\claude_smoke_v01\e_dropout_v01.py` now has the same hash (rebuilt 14:22:10). At 14:35 it still held the first-wording law (861c40dd…); that was my first blocking finding and it is closed. The other five changed files are byte-identical between `src_v04` and the dev packet.

## Blocking

**B1. F's mask function does not equal E's; check 6d.6(a) cannot pass.**
- Where: `work\F_dropout\code\dr_masks_v01.py:33–40` (14:06, unchanged at 14:50) advances with `i += L`: no gap row. `F_dropout\A11_6c_DROPOUT_SPEC_v01.md:44–46` has the same wording. `F_dropout\masks\DR_MASKS_v01.json` (14:06) was written under it.
- Measured: I transcribed F's function and compared it with E's on the 60 E3 case ids and `c1109_tune_0000`. The masks differ on 60 of 61. F's rule still gives stretches of up to 7 rows on the 60 cases, which punish_num = 3 does not cover.
- F also seeds with a run id or archive name (`dr_masks_v01.py:7`). The amendment says the protocol case id, "never a job or archive name".
- `tests\out\E4_LAW_TEST_v02.json` has no field that compares E's masks with F's function, although 6d.6(a) requires it.
- Fix: F brings its function, spec and mask file to the amendment's wording. E's law test then imports F's function and asserts equal masks on the three fixed ids and the 60 cases.

## Major

**M1. The law id is not versioned, and the review checks the law against itself.**
- Where: `e_dropout_v01.py:19` (`LAW = 'A11D'` under both wordings); `review_case_e_v01.py:36–40` imports the packet's own `e_dropout_v01.py`.
- Failure: a packet with a stale or altered law file passes every mask check, and its records look the same. This nearly happened today: the dev packet held the first wording for 12 minutes after the source changed.
- Fix: record the SHA-256 of `e_dropout_v01.py` in the `dropout` block, or bump the id. Give the review a known answer from outside the file: the hash of the 60-case mask table locked in LOCK_A11b.

**M2. punish_num = 3 is decided but not pinned.**
- Where: `probe_e_v01.py:79`, `worker_main_v01.py:98`, `review_case_e_v01.py:38` and `tools\make_jobs_e4_v01.py` accept 1..14.
- Failure: a list built with another value runs and passes every review.
- Fix: assert punish_num == 3 in `make_jobs_e4_v01.py` and in the review. Rewrite `E_DROPOUT_A11_6d_v01.md` §6d.3 items 1–3 and 5 to the final wording; they still say "walk i = 0, 1, 2…" with no gap row.

**M3. IMM arms: nothing independent shows the tracker received an empty list.**
- Where: `review_case_e_v01.py:82–83` skips the perception stage for IMM. Lines 43–44 check only `masked` and `tracker_rows`, which the probe writes itself (`probe_e_v01.py:292`).
- For CANMOT arms the replay with `[]` and the run's punish_num does prove it.
- Fix: require `E_IMM_TRACKER_v01.json` punish_num to equal the dropout record's. Require no `update` or `birth` event in `imm_filter_events.jsonl` at a masked tick's time. Have the recount run the offline masked B1 identity (test (b)) on the IMM runs.

**M4. An E4 job can run without masks and still be CAPTURED_AND_REVIEWED.**
- Where: `review_case_e_v01.py:33` checks the dropout block only if ARM_METHOD has one. `worker_main_v01.py:286–296` stores `e_job` and `method` and never compares them. `load_jobs` (97–98) does not require the knobs for phase E4.
- Fix: in `summarize`, if the job has `dropout`, require the method's law and punish_num to equal the job's and the review's `dropout` block to be present; otherwise another status. In `load_jobs`, require the knobs when phase is E4. The analysis and the second program apply the same filter.

**M5. `detections.jsonl` `model` no longer means "what the tracker saw".**
- Where: `probe_e_v01.py:290`. On masked rows `model` holds the true detector rows.
- Failure: a consumer that re-tracks from `row['model']` silently gives the unmasked result on E4 captures: `trackers_b\trk_tracker_v01.py:155–159` (`retrack_capture` with logged rows), `replay_tracker` called directly, and any recount of the actor list.
- Fix: state it in the E4 interface note. The recount builds the tracker input as `[] if masked else model`.

## The new track id after a window: is it a problem for N vs F0?

No, not for the validity of the pre-registered comparison. Three points should go into the text and the statistics.

- **The cause is the lead's braking, not the score.** In `E4_IMM_online_v02.json` (`c1109_eval_0480`), at the window of rows 16–18 the track coasts at 14.7 m/s while the lead slows to 9.2 m/s. The prediction overshoots and the detection at row 19 does not associate. At rows 36–38 the score also falls to 0.004, the lead is at rest, and the same id continues. The test's note ("score decays ×0.2…") should be corrected.
- **The new track's covariance is small.** Position variance along the route, in m²:

  | Row | State | Position variance | Velocity variance |
  |---|---|---|---|
  | 15 | steady | 0.035 | 0.18 |
  | 18 | third coasted row | 1.13 | 1.31 |
  | 19 | new id | 0.047 | 0.27 |
  | 39 | same id re-associated | 0.046 | 0.21 |

  N's extra caution therefore comes from the coasted rows, as §6d.5 says, and hardly from the new track. The new track's mean state is the same for F0 and N.
- **The arms do not use track ids.** `e_arms_v01.py` has no reference to a track id or to emission age. The mask and the tracker are the same within each pair.
- **What to report.**
  - The switch happens when the lead brakes inside a window, which is the moment that matters. During such a window both arms plan against a lead predicted too fast and too far ahead. That is the effect under test, and it should be said in the text.
  - After a 1–2-row window with a failed association, the old track is still within punish_num and is output beside the new one, with an inflated covariance. Only N responds to that covariance. I saw no such row in the one case tested. Add to the exploratory per-run statistics: the number of lead id switches, and the number of decision ticks with two in-path cars.

## Minor

- **m1.** `probe_e_v01.py:117`: RUN_CONTEXT does not record the dropout knobs. With dropout off the outputs equal E3's, with two exceptions: `RUN_CONTEXT_v01.json` (`probe_sha256`) and, for IMM arms, `E_IMM_TRACKER_v01.json`, which gains a `punish_num` key (`e_imm_v01.py:62`). The F0 smoke reproduction is unaffected; state which files it compares.
- **m2.** `review_case_e_v01.py:38–40` does not check `n_updates` (69), `first_k`, `period_k`, `p_start` or `length_ticks`. For IMM arms no stage checks that the two copies of `detections.jsonl` are equal.
- **m3.** `review_perception_prefix_v01.py:128` reads ARM_METHOD outside the dual-copy `Inputs` reader.
- **m4.** §6d.3 item 6 says "the number of rows discarded"; the code logs the rows fed (`tracker_rows`).
- **m5.** Smoke case `c1109_tune_0000` masks only rows 36, 37, 49 and 57 (first at k = 379). A run that ends earlier exercises no mask. Require at least 38 detector updates in the smoke acceptance, or add a case with an early window.
- **m6.** `E4_CANMOT_OUTPUT_TEST_v02.json` (14:21:53) now passes, with the criterion changed from "same id after" to "a lead at the gap row". Record that change of criterion in the check list.

## Checked and found correct

**`mask_for_case` against A11 §6c, line by line:**

| §6c wording | Code (`e_dropout_v01.py`) | Result |
|---|---|---|
| Seed `int.from_bytes(sha256("A11/D/" + case_id).digest()[:8], "big")` | line 27 | equal |
| Row 0 never masked | line 35, `i = 1`; no draw at row 0 | equal |
| From row 1, at a row not in a window, draw u | line 37 | equal |
| If u < 0.10, draw L = `rng.integers(1, 4)` | lines 38–39; L drawn only when a window starts | equal |
| Mask rows i … i+L−1, cut at the run's end | lines 40–41 | equal |
| Rows inside a window draw nothing | line 42 | equal |
| The row after a window is unmasked and draws nothing | line 42, `i += L + 1` | equal |
| Depends on the case only | no other input | equal |

- On the 60 E3 cases I recounted 131, 126 and 122 stretches of 1, 2 and 3 rows, none longer, and no masked row 0. This agrees with `E4_LAW_TEST_v02.json`.
- **Probe:** the mask is applied at every detector tick with the law's index (lines 281, 286). Only the tracker input changes. Emissions, ObservationStream and `e_track_history` receive tracks; `model_rows` is used only for logging. ARM_METHOD is saved at line 190, before the loop at line 243. With dropout off, the `detections.jsonl` rows have E3's keys and order.
- **IMM override:** effective. `Tracker.punish_num` is read only at `nusc_tracker.py:380`; `e_imm_v01.py:40` sets it. `trackers_b` does not read punish_num. `E4_IMM_MASKED_REPLAY_v02.json` passes with punish_num 3.
- **CANMOT empty frame:** takes `tras_punish`. Class deletion ages are 10–20 updates, above 3.
- **Perception review (CANMOT):** the detector check compares the true rows; the replay gets `[]` and the run's punish_num; tracks, events, targets and algebra are compared. `prefix_contract_v01.derive` does not constrain the new keys. Runs that end early by contact or policy failure replay as a prefix.
- **Worker:** both knobs or neither, E4 arms only, passed together. A v03 probe would reject `--dropout` and not run unmasked. E4 job ids do not collide with E3 ids on the volume.
- **Not verified:** `Store.put` (711 `ordered_capture_v02.py`) with a 64-bit seed integer; I could not read its encoder. The smoke shows it at the first ARM_METHOD save.
