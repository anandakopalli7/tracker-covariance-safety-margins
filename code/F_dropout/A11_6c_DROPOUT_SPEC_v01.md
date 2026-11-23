# Proposed text for AMENDMENT_11 §6c: DR, detection dropouts on the fresh lead-braking runs (open loop)

Drafted by session F (Claude Opus 5.5), 21 Nov 2026, 14:05–14:35 EST (this laptop's clock), for the coordinator to place into
`revision_v13\AMENDMENT_11_v13.md`. Nothing under DR is computed before LOCK_A11b, except the items §6c.9 names. The scenario is
called **DR** (not D) because A10 already has a package D and a seed labelled "D1 case draws"; its hypotheses are DR0–DR2.

**One open choice, marked [PUNISH] below, is the coordinator's:** the D-only tracker output rule (§6c.3). Option 1 (recommended)
is `punish_num = 3`; option 2 is the value of record, 1.

---

## 6c. DR: detection dropouts on the fresh lead-braking runs (open loop)

**6c.1 Why.** In lead braking the online tracker's covariance is close to a class constant (Table S28: 99% of margin ratios
within 5% of the median), and there is room. In the crossing families it varies, but there is little room (§2). Under detection
dropouts the covariance grows with the time since the last update, which plausibly tracks the real error. DR asks, in one
scenario with room, whether a covariance helps when it carries information. Either answer is reported.

**6c.2 Runs and logs (no new capture).**
- **Fresh runs:** the 105 fresh lead-braking runs of C: `CD_capture\CASES_C_v13.json` lead-braking cases with
  `REPLACEMENTS_C_v13.json` applied, ids `pc13_<case>_native`, ascending. Logs as stored: `CD_capture\runs\<id>\<id>\capture\<case>\`.
- **Tuning runs (for P̄ only):** the 120 tuning runs of record (rows with `set == tune` in
  `09_redesign\m4_perception_model\run_index_m4_v02.csv` of programme P, read-only), all six families.

**6c.3 The dropout tracker (DR).**
- **Tracker:** the online tracker of record (variant CV0, constants and configuration of record), through the frozen library
  `shared\trackers\trk_tracker_v01.retrack_capture`, fed the logged detector frames (rows of `detections.jsonl`, logged order and
  times; dt 0.5; latency 0; the decision at tick k uses frame kd = 19 + 10⌊(k − 19)/10⌋, as of record).
- **A masked frame** keeps its index, time and tick, and its detector output (`model`) is replaced by the empty list. CANMOT's
  loader then flags the frame `no_dets` (`keep_num == 0`), and the tracker predicts every track and updates none (its own
  empty-frame path, `tras_punish`).
- **Output rule [PUNISH].** The tracker of record outputs a track that missed its update only while its time since update is at
  most `output.punish_num` = 1 (`contracts\tracker_config.json`); tracks stay alive up to `life_cycle.max_age` (cars: 10 frames).
  - **Option 1 (recommended):** DR uses the configuration of record with `output.punish_num = 3` (the longest window). A coasting
    lead is then output with its predicted covariance on every masked frame. This is a configuration value passed to the frozen
    library (`base_cfg`); no library file changes.
  - **Option 2:** the value of record (1). On the second and third frames of a window the lead is then not output; F0, E and N
    all see no actor there. The lead-absent share (§6c.7) is then reported beside every DR value.
- Everything else in the pipeline is unchanged: the planner rows, the decision ticks and the ego's logged motion (open loop).

**6c.4 Masks (independent of truth and of every outcome).**
- For a run with id `rid` (fresh: the run id; tuning: the archive name of record):
  `rng = numpy.random.default_rng(int.from_bytes(hashlib.sha256(("A11/D/" + rid).encode("utf-8")).digest()[:8], "big"))`.
- Frames i = 0 … n − 1 in logged order. Frame 0 is never masked, so tracks can start. For i = 1 … n − 1, in order, at each frame
  not already inside a window: draw `u = rng.random()`; if `u < 0.10`, draw `L = rng.integers(1, 4)` (1, 2 or 3 frames, i.e.
  0.5–1.5 s) and mask frames i … i + L − 1 (truncated at n − 1). Frames inside a window draw nothing.
- **Mask file:** `work\F_dropout\masks\DR_MASKS_v01.json`: for each of the 225 runs, n and the masked frame indices. It is written
  and hashed before LOCK_A11b (the masks depend on no value), and the second program regenerates it exactly.

**6c.5 Sources and arrays.**
- **P̄_DR:** the P̄ rule of record (A10 §2.1; `ol_pbar_v01` through `B_retrack\code\b_retrack_v01.py` pass `pbar` and `combine`)
  applied to the DR tracker's outputs on the 120 tuning runs under their masks.
- **Arrays per fresh run:** the frozen builder `trk_arrays_v01.overlay` / `extract` (`lead=True, a4=True`) on the DR tracker's
  overlay, with P̄ = P̄_DR: `cF0` → **F0_DR**, `cE` → **E_DR** (true error of the DR estimate), `cN` → **N_DR**; clearances, the
  fallback row and the evaluated mask as the builder gives them. A second extract with the P̄ of record gives **F0rec_DR** (for
  §6c.7 only).
- **Ceiling and twin (A10 §2.2, frozen `shared\trackers\trk_score_v01`):** u = `e5_u(runs, 'F0_DR', 'E_DR')` over the 105 runs'
  evaluated decisions; m_DR and A_DR are the median and (q95 − q05)/(2 · median) of `margin_ratios(runs, 'F0_DR', 'N_DR')`;
  **E5_DR** = `add_oracle(F0_DR, m_DR, A_DR, u)`; **E5p_DR** = the same with `permute_u(runs, u)` (`default_rng(20261915)`, runs
  ascending, one permutation per run among its evaluated decisions).

**6c.6 Hypotheses in their own fixed sequence.**
- Fresh runs, all evaluated decisions, 3 s commitment, gridless step frontier on 201 caution levels (A10 §2.3), scoring library
  of record. One-sided at 0.025: the lower end of the two-sided interval at the level A10 §2.6 gives. δ = 0.05 (A10 §2.7).
- **Intervals:** the fresh-run bootstrap of record (`default_rng(20261911)`, 20,000 resamples, `optA_lib_v02.boot_counts`,
  runs ascending: C's draw). **Calibration** (A10 §2.6) of each hypothesis statistic: 2,000 × 1,000 (`20261912` / `20261913`),
  checks `20261914` and `20261920`.
- "Confirmed" means it and every earlier one passed; later ones are still computed and labelled "not confirmatory".

| Ref | Hypothesis | Passes if | Statistics calibrated |
|---|---|---|---|
| DR0 | There is room under dropouts | R_gl = D_gl(E_DR, F0_DR) has a lower end > 0, and D_gl(E_DR, F0_DR) > 0 in ≥ 97.5% of resamples (as H0) | R_gl |
| DR1 | The measure detects rank information at the DR tracker's amplitude | Lower ends of c_DR = RR_gl(E5_DR) and of RR_gl(E5_DR) − RR_gl(E5p_DR) both > 0 | c_DR; the difference |
| DR2 | What the DR covariance does, against its ceiling | **Classified** as H3, with r = RR_gl(N_DR) and c = c_DR on DR's own room: (a) recovers if r's lower end > 0; else (b) uninformative variation if c's lower end > δ; else (c) amplitude-limited if c's interval lies inside (−δ, δ); else (d) inconclusive. Flag "barely varies" if ≥ 95% of binding rows lie within 5% of the median N_DR/F0_DR ratio. Passes with (a), (b) or (c); under (a) r / c with its interval | r (and c) |

**6c.7 Descriptive (no hypothesis; nominal 95% percentile intervals on the same draw).**
- **In-dropout population:** evaluated decisions whose frame kd is masked; with its count, R_gl, RR_gl(N_DR) and c_DR there.
- **Margin-ratio check** of N_DR / F0_DR (median, q05, q95, A_DR, share within 5% of the median), for all evaluated decisions and
  in-dropout.
- **RR_gl(N_DR) against the record P̄:** D_gl(N_DR, F0rec_DR) / D_gl(E_DR, F0rec_DR).
- **Masked share:** of frames (fresh runs; tuning runs) and of evaluated decisions.
- Under option 2 of §6c.3 only: the share of evaluated decisions whose frame kd outputs no lead track.

**6c.8 Identity checks (before LOCK_A11b; they compute no DR value).**
- **(i) Harness:** with an empty mask and the configuration of record, the fresh runs' re-run arrays reproduce the stored CV0 arrays of
  record (`CD_capture\arrays\CV0`) to A10 B0's standard (bit-identical, or B0's stated tolerance). Platform: the pods that run DR.
- **(ii) Output rule (option 1 only):** with an empty mask and `punish_num = 3`, the number of fresh-run evaluated decisions whose
  actor list changes against (i). Changes can come only from the detector's own consecutive misses. The count is reported.
- **(iii) Masks:** the second program's regenerated masks equal `DR_MASKS_v01.json` exactly.

**6c.9 Order and lock (LOCK_A11b).** Before the lock: this text; the mask file; the DR code and its second program's code (frozen
in a FREEZE addendum); (i)–(iii); pod platform tests on synthetic data. LOCK_A11b records the SHA-256 of each. After it: P̄_DR,
the fresh DR arrays, the values, the calibration, the second program's recount and the comparison, in that order.

**6c.10 Verification.** A second program by Claude Sonnet 5.5, written from this section and A10 §2 without reading F's DR code
(it may use the frozen shared libraries `trk_score_v01` and `optA_lib_v02`): it regenerates the masks, and recomputes every DR
value and verdict from the DR arrays and P̄_DR's inputs. Agreement as A10 §10.1(c): counts exact, points and interval ends within
1e−9 on the same draws, calibrated levels equal.

**6c.11 Consequence rules.**
- DR0 fails: "under detection dropouts there is no room to test", and the text stops there for DR.
- DR1 fails: the measure does not detect rank information at the DR tracker's amplitude; DR2 is printed as not confirmatory.
- DR2 is reported in its class, with r, c and, under (a), r / c. Whatever the class, the result is not extended beyond lead braking
  under this mask rule.
- The text says that DR was specified on 21 Nov 2026, after C's and B's fresh lead-braking results were exported and seen, and
  that it re-scores those same runs.

**6c.12 Spend, pods and cut-off.**
- CPU work on pods (EU-RO-1; numba threads = the pod's cgroup CPU quota). Upload: about 0.3 GB compressed (seven log files per
  run, 225 runs; the CANMOT codex tree).
- Each pod is logged in `SPEND_LOG_v13.csv` and deleted when its output is verified (absent from the list). DR's own cap is $10,
  within the sprint's $60.
- Cut-off: recounted DR results by **21:30 EST, 21 Nov**, or DR is not printed, and the text says it was not completed.
