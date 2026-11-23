# Text for AMENDMENT_11 §6c: DR, detection dropouts on the fresh lead-braking runs (open loop), v03

Drafted by session F (Claude Opus 5.5), 21 Nov 2026, about 14:55 EST by this laptop's clock, for the coordinator to merge verbatim into
`revision_v13\AMENDMENT_11_v13.md` §6c. Changes from v02 (`A11_6c_DROPOUT_SPEC_v02.md`, SHA-256 `446381f2…b14f`):
- DR's lock is its own third stage, `LOCK_A11c.txt` (coordinator, 14:49; `LOCK_A11b` covers §6d only). Every "LOCK_A11b" in v02 now
  reads "LOCK_A11c".
- §6c.9 records the pre-lock pod test of the whole pipeline (35 old lead-braking fit runs).
Nothing else changed.

Nothing under DR is computed on fresh runs before LOCK_A11c, except the identity checks of §6c.8, which compute no DR value.

---

## 6c. DR: detection dropouts on the fresh lead-braking runs (open loop)

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
  - It is written and hashed before LOCK_A11c.
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

**6c.8 Identity checks (before LOCK_A11c; they compute no DR value).**
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

**6c.9 Order and lock (LOCK_A11c).**
- **Before the lock:** this text; the mask file; the DR code and its second program's code (frozen in `work\locks\FREEZE_DR.json`);
  checks (i)–(iii); a pod test of the whole pipeline on the 35 old lead-braking fit runs (exploratory data of record).
- **Pod test, done:** on pod `claude-v13f-d01`, the whole pipeline ran end to end on the 35 old lead-braking fit runs:
  masked P̄, masked arrays, the record-P̄ extract, the empty-mask reference, the analysis, the calibration export,
  `calib_remote_v13` with 100 outer × 1,000 inner, and the import. These are exploratory data of record; the outputs are
  `work\F_dropout\out\TESTOLD_DR_RESULTS_v01.json` and `out\testold\`.
- **LOCK_A11c** records the SHA-256 of each.
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
