# AMENDMENT 12 to AMENDMENT_10_v13.md and AMENDMENT_11_v13.md: replication on new runs, a fair two-noise IMM, a real-sensor mechanism check and a caution-matched closed-loop dropout test (round 2)

Status: coordinator's frame, 22 Nov 2026, about 00:25 EST by the laptop clock. Each package writes its own section text, merged verbatim as in A11. Three staged locks:
- `LOCK_A12a.txt`: §§2–4 and §7, before any value of a new run;
- `LOCK_A12b.txt`: §6, E's matched setting, before E's main capture;
- `LOCK_A12c.txt`: §5, before any nuScenes val value of the mechanism check.

## 0. Approval record

- Author, 21 Nov about 23:50 EST, relayed by "Paper work summary" (verbatim): "I like option 3 for the title. Also regarding the paper itself, based what you've told me so far, I don't think it would get even 7 out of 10. My own confidence on the paper is even lesser. Bring the confidence to 8 by fixing all weaknesses of the paper. I approve 12 more hours from now. Download whatever you want and run whatever the experiment you want. But paper should meet minimum 8 out of 10 confidence."
- Limits:
  - round 2 ends 22 Nov 11:45 EST;
  - at most $50 of new pod spend, with the balance kept above $10 while pods run;
  - official downloads only, needing no new account or licence; not Argoverse 2.
- Aimed at the sprint panel's blockers (`ARS_TRIAL\review_v13_sprint_output\ARS_REVIEW_SPRINT_v01.md` §1, §4):
  - amendment evidence specified after related results were seen;
  - an unfair IMM arm;
  - one simulated configuration;
  - the source of the dropout gain not identified;
  - the closed-loop dropout set not caution-matched;
  - no multiplicity adjustment.

## 1. What does not change

- AMENDMENT_10, AMENDMENT_11 and all their locks and results. Every v13 value already exported stays as it is.
- The labels convention adopted after the sprint panel: "confirmed" for A10's original plan; "passed (amendment)" for amendment tests. A12's replications of A11 tests run under rules fixed before their data. The text may call them "replicated under rules fixed before the data", and still labels them as amendment tests.

## 2. New lead-braking runs (session CD)

Cases, packet, capture, sealing and failures as A10 §5.1 and A11 §3.1–3.3:
- never-run lead-braking evaluation cases of the main protocol;
- the protocol's own generator extension where a speed is short;
- n per speed and reserves fixed here.

**Bootstrap draw for every §3 analysis on the new runs (fixed by the coordinator, about 00:55 EST):**
- `optA_lib_v02.boot_counts(n_new, 20000, 20261911)`, runs in ascending id, the same draw for §3a, §3b and §3c;
- A10 §2.6's calibration seeds as A11 §3.7.
The data set differs from C's, so no draw is shared with C's analysis.

<!--MERGE:CD-->

**Merged verbatim** from `A12_SECTIONS_2_3b_CD_v02.md` (sha256 `10d5691cdfe232c79498bbb96a60fdfe0d6fff7c178e544875ce2ce2139a652e`); headings demoted two levels, nothing else changed. Where it and the coordinator's fixed choices above differ, the fixed choices govern.

#### 2. New lead-braking runs (session CD)

**2.1 Cases.** The file is `work\CD_capture\l12\CASES_L12_v13.json` (SHA-256 `ae494eb27637139132df1e258da489038087fd81452952ded73c6c842d4075eb`), made by `l12\make_cases_l12_v13.py`. The rule is A10 §5.1, as for X (A11 §3.1):
- **Protocol cases first.** These are the never-run lead-braking evaluation cases of `06_phase0\scenarios\DEVELOPMENT_PROTOCOL_MAIN_v01.json` (`32d683a0…`), per desired speed in ascending id. Every case already used is skipped: C took ranks 0–34 and E3/E4 took 35–54, checked against every run name and case list, X's included. The protocol holds 51 / 33 / 51 such cases at 5 / 10 / 15 m/s.
- **Generator extension where a speed is short of 55.** This is the protocol's own generator, unchanged: `make_main_protocol_v01.new_case` continued at indices i ≥ 1800 with i % 6 == 0 (lead braking), via `SAMPLER_C1109_v01.draw(i, 'lead_braking', role='eval', consumer='finite')`.
  - The seed is int(sha256("C1109/eval/finite/<i>")[:8], 16), and the id is `c1109_eval_<i>`.
  - Indices are taken in ascending order; each case joins the pool of its drawn speed until that pool is full.
  - It supplies 30 cases (4 / 22 / 4), indices up to 2220. The 41 cases drawn for an already-full speed are not used, and are listed in the file.
- **Checks before use.** The replica reproduces all 1,800 protocol evaluation cases exactly. The extension's ids, seeds, seed digests and noise episodes are new against the protocol, D1, X's case list and X's extended protocol, and all draws are unique.
- **Order.** Per speed, protocol cases come first, then extension cases. Speeds are interleaved: position p has speed (5, 10, 15)[p % 3].
  - Positions 0–149 are the study runs (**n = 150, 50 per speed**: 133 protocol, 17 extension, all at 10 m/s).
  - Positions 150–164 are the reserves (5 per speed), used in order.
  - Recording arm: native, α = β by C's cycle on the rank within speed. Jobs are `pl12_<case>_native`.

**2.2 Packets and capture.**
- **Packets.** Protocol cases run on packet_main_v03, unchanged. Extension cases run on `packets\packet_l12_v13.tar.gz` (`451f776d…`): packet_main_v03 with only `claude_smoke_v01/DEVELOPMENT_PROTOCOL_SMOKE_v01.json` replaced by the main protocol plus the appended extension cases (`DEVELOPMENT_PROTOCOL_L12_v13.json`, `0b35dbd6…`). It is built as packet_d1_v13 and packet_x_v13 were, with no code change.
- **Capture settings.** C's settings, made by `l12\make_jobs_l12_v13.py`:
  - RTX 4090 pods, with L4 as a fallback;
  - per pod, 3 A1 admission runs and a crash control first, then one after every 50 study jobs;
  - every control must be identical to its reference (S equal, T bit-identical), or the pod's runs are not study runs.
- **keep_raw true (change before capture).** The coordinator's change of 22 Nov, about 00:35 EST, keeps a second configuration (10 Hz, 0.1 s latency) open:
  - Every study job has keep_raw = true, as C's study jobs had. Controls keep false, as in C.
  - The lists actually run are `jobs_l12\JOBS_PL12_claude-v13cd-l<k>_v02.json`, made from the frozen `_v01` lists by `l12\make_jobs_l12_raw_v13.py`, which asserts that nothing else differs. They are frozen in FREEZE_CD_add8.
  - Capture started at 00:37–00:40 EST on these lists.
- **Logs.** Every log that the re-tracking (session B) and the dropout replay (session F) read is kept: detections, filter events and algebra, frames, scenario frames, evaluation truth, contract.
- **Archives and sweeps.**
  - Archives, including the noisy sweeps, stay on each pod's local disk.
  - On the pod, C's frozen `tools\seal_extract_v13.py` makes a logs-only copy of each archive (every member but the sweep .npy files, copied as bytes).
  - Only these copies, the sealing records and the receipts are downloaded to the laptop (`l12\l_logs_v13.py`), each checked against its sealing record and receipt.
  - The sweeps stay on the pods until the coordinator decides on 10 Hz. If 10 Hz is adopted, re-detection uses C's frozen `tools\b7_redetect_v13.py` (10 Hz rows, every 2nd frame), and re-tracking uses chain B7_10_0.1 of C's frozen `analysis\x_trk_extract_v13.py`. That configuration is specified in the section that adopts it.

**2.3 Sealing.**
- Capture may start before LOCK_A12a. Until the lock, only receipts and pass/fail counts are read (A10 §5.2). C's `seal_extract_v13.py` checks each archive against its receipt (SHA-256, bytes, status, frames_dropped 0, keep_raw true) and checks every kept sweep against FILE_HASHES.json and its noise receipt. It prints pass/fail counts only.
- CD's CV0 extraction runs only after LOCK_A12a exists. It uses the online tracker of record with the P̄ of record, by package B's frozen `trk_arrays_v01.extract(lead=True, a4=True)` as in C (`analysis\c_extract_v13.py`), and its program is frozen in a FREEZE_CD addendum before its first run.
- Nothing else of a new run is computed or read before the lock.

**2.4 Failures and the analysed set.**
- A10 §5.1 applies: one retry in a fresh process; a second failure is replaced by the next unused reserve of the same speed, with the failed case's α. Each replacement goes in `l12\REPLACEMENTS_L12_v13.json` (append-only) and is reported.
- A run captured on an allowed retry carries the worker's suffixed run id. Its arrays are aliased to the job id with no numeric change, as for X (A11 departure X-6).
- **Capture deadline: 22 Nov 04:30 EST.** The analysed set is the 150 listed cases, with replacements, that are CAPTURED_AND_REVIEWED by then. With fewer than 128 runs (85%), every A12 test on the new runs is reported as descriptive (under-run).

**2.5 Where the files are** (laptop, under `work\CD_capture\`; the same layout as C).
- **Logs.**
  - `runs\<rid>\LOGS_OK` holds the archive's SHA-256, which equals its receipt.
  - `runs\<rid>\<rid>\` holds SUMMARY.json, FILE_HASHES.json, JOB.json, review\ and `capture\<case>\`: contract.json, detections.jsonl, filter_events.jsonl, filter_algebra.jsonl, filter_target_covariances.jsonl, frames.jsonl, scenario_frames.jsonl, evaluation_truth.jsonl, raw_observations.jsonl, noise_receipts.jsonl, assessment_outcomes.json and the other capture records.
  - <rid> is the capture run id: the job id, or the worker's suffixed id after an allowed retry.
- **Receipts, logs-only copies and sealing records:** `archives_l12\<rid>\`.
- **Job id to run folder:** `l12\out\L12_RUNS_v13.json`, for the 150 analysed job ids after replacements.
- **CV0 arrays:** `arrays_l12\CV0\<job id>.npz`, written after LOCK_A12a.
- **If 10 Hz is adopted:** `b7\<rid>\b7_detections_v13.jsonl` with its `B7_MANIFEST_v13.json`, and `arrays_l12\B7_10_0.1\<job id>.npz`.

##### 3b. Y replication (session B re-tracks, session CD scores)

A11 §6b applies unchanged to the new runs. Its definitions are `ycheck\CD_DEFINITIONS_Y_v13.md` (frozen in FREEZE_CD_add4), including the twin draw (K = 20, `default_rng(20261931)`, k outer, runs inner).
- **Data.** These are the 150 new runs of §2.4, in ascending run id: package B's B2 re-track of them (frozen as data in a FREEZE_B addendum, with per-file SHA-256), and CD's CV0 arrays of the same runs for the online-N reference.
- **Program.** The same first and second programs are used (`ycheck\y_twin_v13.py`, `recount\rc_y_twin_v13.py`). Only the run list, the B2 array folder, its manifest and the CV0 folder change, as arguments; that change is frozen in a FREEZE_CD addendum before the first new-run value. Both are run on the same pod with identical draws.
- **Resamples.** There are 20,000 run resamples, `optA_lib_v02.boot_counts(n_runs, 20000, 20261911)`.
- **Intervals.** The A10 §2.6 calibration for Δ uses seeds 20261912/13, the second inner seed 20261914 only where needed, and the Monte Carlo check 20261920. The emergency rule is that of A11 §3.7, with A12's cut-off.
- **Y1 (replication).** Δ = RR_gl(N_B2) − RR_gl(B2p) passes if its lower end is > 0.
- **One-sided bootstrap p-value (§4).** p_Y1 = #{b : Δ_b ≤ 0} / #{b : Δ_b finite} over the 20,000 resamples of Y's draw. Both programs export it; it enters A12's Holm adjustment.
- **Descriptive, unchanged.** Also reported: B2s and Δs, RR_gl(B2p), and the online-N reference.
- **Labels.** Y on the new runs is labelled "passed (amendment), replicated under rules fixed before the data" (§1).


## 3. On the new runs

### 3a. DR replication and dose-response (session F)
- DR0–DR2 at p = 0.10 under A11 §6c unchanged (masks by case id, punish_num = 3, F0_DR from the 120 tuning runs).
- Dose-response at p ∈ {0.05, 0.10, 0.20, 0.30}, with a pre-registered trend test.
- Decomposition of the gain (in-dropout / the ticks after re-acquisition / steady) as substitution shares, descriptive.

<!--MERGE:F3a-->

**Merged verbatim** from `A12_3a_DR_REPLICATION_v02.md` (sha256 `ca5f058c54250f06b72355675810b664f818ef86d05a630ed230358ca8dbbfa0`); headings demoted two levels, nothing else changed. Where it and the coordinator's fixed choices above differ, the fixed choices govern.

### Text for AMENDMENT_12 §3a: DR replication and dose-response on the new lead-braking runs, v02

Drafted by session F (Claude Opus 5.5), 22 Nov 2026, about 00:25 EST by this laptop's clock, for the coordinator to merge verbatim into
`revision_v13\AMENDMENT_12_v13.md` §3a. Nothing below is computed on a new run before LOCK_A12a.

Changes from v01 (`26ca6298…291c`):
- §3a.4 now says the masks at different p are not nested (v01 wrongly said they differ only through u < p).
- §3a.2 names the new program files.

---

##### 3a. DR replication and dose-response (session F)

**3a.1 Runs.** The new lead-braking runs of §2 (session CD), in ascending run id. Their number n is fixed by §2. Each run's protocol
case id is its seed id. Logs and CV0 arrays of record as CD stores them for C (`CD_capture\runs\`, `CD_capture\arrays\CV0\`).
The 120 tuning runs of record give F0 (A10 §2.1), as in A11 §6c.

**3a.2 What is unchanged from A11 §6c (v04, locked by LOCK_A11c).**
- The tracker: CV0 through the frozen library, `punish_num = 3`.
- The one mask law with its gap row.
- The decision-frame mapping, the frozen array builder, the scoring library, the gridless frontier on 201 levels and the 3 s commitment.
- The amplitude-matched ranking oracle E5_DR and its permuted twin, including u_i's divisor n_r (A11 §6c.5).
- δ = 0.05, A10 §2.6's calibration, and the identity checks (i) and (ii).
- The code is FREEZE_DR's, unchanged in substance. The new files are frozen in `work\locks\FREEZE_DR_A12.json` before LOCK_A12a:
  - `dr_masks_v03.py`: the law with p;
  - `dr_extract_v02.py` and `dr_analysis_v02.py`: copies of the frozen v01 files with only the run set, folders, lock and p changed;
  - `dr_dose_v01.py`: the dose-response and the decomposition;
  - `dr_slope_remote_v01.py`: the slope's double bootstrap on pods;
  - `dr_pods_v02.py`: the pod tool.

**3a.3 DR0–DR2 at p = 0.10 (the replication).** A11 §6c.6's sequence, unchanged, on the new runs.
- **Masks:** the one mask law with p = 0.10.
- **F0:** P̄_DR is the existing file `work\F_dropout\out\PBAR_DR_v01.json`. Same tuning runs, same law, same configuration, so it is the
  same P̄; it is recomputed and must be identical.
- **Draw:** run resamples `optA_lib_v02.boot_counts(n, 20000, 20261911)` (A10 §5.8's fresh-run bootstrap seed, runs ascending).
- **Calibration:** A10 §2.6 with its seeds.
- **Labels:** "replicated under rules fixed before the data" if the class and passes equal A11's; it is an amendment test (A12 §1).
- **Holm (A12 §4):** DR2's one-sided bootstrap p-value is p_r = (1 + #{r\* ≤ 0}) / (20,000 + 1). Here r\* = RR_gl(N_DR) in each of the
  20,000 resamples, and a resample whose D_gl(E_DR, F0_DR) ≤ 0 counts as r\* ≤ 0. "Recovers" requires r's lower end > 0.

**3a.4 Dose-response.**
- **Masks:** for each p ∈ {0.05, 0.10, 0.20, 0.30}, the one mask law with the start probability p in place of 0.10. The seed string,
  the draw order, L ∈ {1, 2, 3} and the gap row are unchanged. Masks at different p are not nested: once one p starts a window where
  another does not, their draw sequences diverge. At p = 0.10 the law is exactly A11 §6c's (checked on all 225 runs of DR_MASKS_v02).
- **Per p:** P̄_DR(p) is recomputed on the 120 tuning runs under that p's masks. Then the arrays, F0_DR(p), E_DR(p) and N_DR(p), and
  r(p) = RR_gl(N_DR(p)) on that p's own room.
- **Trend statistic (primary):** the ordinary least-squares slope of r on p over the four values,
  b = Σ_p (p − p̄)(r(p) − r̄) / Σ_p (p − p̄)², with p̄ = 0.1625.
  - It is computed on each run resample with the SAME resample of runs at every p (the 20,000 draws of §3a.3).
  - A resample where any p has D_gl(E, F0) ≤ 0 gives b\* = NaN; NaN counts as b\* ≤ 0 for the p-value.
- **Test:** the trend passes if b's lower end > 0 at the level of A10 §2.6. Its double bootstrap recomputes all four r(p) in every inner
  resample.
- **Holm:** p_b = (1 + #{b\* ≤ 0}) / (20,000 + 1).
- **Descriptive:**
  - each r(p) and R_gl(p) with 95% percentile intervals;
  - the masked share of frames at each p;
  - Spearman's ρ between p and r(p) on the full sample.

**3a.5 Decomposition of the gain (p = 0.10, descriptive).**
- **Populations of evaluated decisions, by the frame each uses:**
  - in-dropout: the frame is masked;
  - re-acquisition: the frame is not masked and one of the two frames before it is (the gap row and the frame after it);
  - steady: all others.
- **Substitution share** of population S: RR_gl(N_S), where N_S takes N_DR's critical scales on S and F0_DR's elsewhere, on DR's own room.
- **Interaction remainder:** RR_gl(N_DR) − Σ_S RR_gl(N_S). The gridless frontier is not additive across decisions, so the remainder is
  reported, not apportioned.
- **Intervals:** 95% percentile on the same draw. Each share is also given in decision-equivalents.

**3a.6 Verification.**
- **Second program:** the second program of A11 §6c (Claude Sonnet 5.5, `dr_recount_v02.py`), extended by the same model from this text,
  without reading F's code. It recomputes the masks at every p, P̄_DR(p) from the per-run P̄ sums, and every value, verdict and p-value.
- **Agreement:** A10 §10.1(c).
- **Identity checks (i) and (ii) of A11 §6c.8 on the new runs.** They are computed before LOCK_A12a only if CD's CV0 arrays for the new
  runs exist then (they compute no DR value); otherwise right after it, before any DR array.

**3a.7 Spend and order.**
- **Pods:** CPU pods as in A11 §6c (logged; deleted when verified). About $6, within A12's $50. The balance is checked before each pod.
- **Order after LOCK_A12a:**
  1. masks;
  2. P̄_DR(p);
  3. arrays at all four p;
  4. §3a.3's values with calibration;
  5. the trend with calibration;
  6. the decomposition;
  7. the second program;
  8. the comparison;
  9. the export.
- **Export:** `work\F_nuscenes\out\A_EXPORT_DR2.json` and `A_RECOUNT_DR2.json`. The keys are A11's DR keys with the prefix `DR2.`, plus:
  - `DR2.p_r` and `DR2.slope.p` (Holm);
  - `DR2.slope`, `.ci`, `.level`;
  - `DR2.r_p005`, `DR2.r_p010`, `DR2.r_p020`, `DR2.r_p030` (each with `.ci`);
  - `DR2.dec.in`, `DR2.dec.reacq`, `DR2.dec.steady`, `DR2.dec.rest` (each with `.ci`).


### 3b. Y replication (session B re-tracks, session CD scores)
A11 §6b unchanged on the new runs. Session CD's text for §3b is merged in §2.

### 3c. A fair two-noise IMM, "IMM2" (session B)
- **Coordinator's fixed choices:**
  - The quiet CV mode uses κ_q = the κ of record, 0.16788: B3's CV filter, already tuned by A10 B3 rule (2) on whole tuning runs, median NIS 1.994.
    - Changed at about 00:20 EST, on tuning runs only and before any new-run value, from "κ_q by rule (2) on pre-onset frames".
    - Session B found that window unreachable on pre-onset frames. The median stays between 0.91 and 1.11 for j = 0…48, then falls (0.63 at j = 60, 0.0014 at j = 120); its maximum is 1.108 at j = 30, with no sign change. The cause: the lead cruises, and the innovation is limited by R. The rule's "nearest value" would pick an unstable peak. All 121 medians are in `B_retrack\out\imm2t\IMM2_TUNE_KQ_v01.json`.
    - The adopted design is the classic one: a nominal CV mode plus a manoeuvre mode tuned to the manoeuvre.
  - The high-noise CA mode's σ_a² is tuned by the same rule on frames from the truth braking onset to the lead's stop.
    - Search 10^(−3 + 0.05 j), j = 0…160 (up to 10^5), with κ_CA = 1 (library default). First sign change, then bisection to |median − 2| ≤ 0.01.
    - If no sign change, take the nearest value and say so.
  - Transition diagonal 0.95; initial mode probabilities (0.9, 0.1); its own P̄ on the 120 tuning runs (A10 §2.1).
  - Locked before any new-run value.
- **Scored on:**
  - the new runs (primary);
  - the 105 fresh C runs (secondary);
  - with RR_gl, its amplitude-matched oracle, H3's class, its permuted twin (A11 §6b's construction) and mode probabilities by truth phase.

<!--MERGE:B3c-->

**Merged verbatim** from `A12_3c_IMM2_v02.md` (sha256 `02484ab7adacecd38f8fbfa4d2dcfcc3ff4c992fe033193fd5f7351ba7b11de2`); headings demoted two levels, nothing else changed. Where it and the coordinator's fixed choices above differ, the fixed choices govern.

##### 3c. A fair two-noise IMM, "IMM2" (session B)

**Design.**
- IMM2 is the library's IMM, variant B1, with its own constants file. The frozen library is unchanged; κ_CA is not used.
  - It mixes two modes: the B3 CV filter and the B4 CA filter, with CANMOT arithmetic as frozen.
  - Transition diagonal 0.95 per 0.5 s; initial mode probabilities (CV, CA) = (0.9, 0.1).
- **Quiet mode (CV):** car Q = κ_q · Q of record, with κ_q = the κ of record, 0.16788040181225605.
  - That κ is B3's, tuned by A10 B3 rule (2) on whole tuning runs (median 1.994); it is also the first IMM's CV mode.
- **High mode (CA):** acceleration noise σ_a² = σ²_hi, tuned on braking frames below.
  - Its position and velocity terms come from the same CV diagonal (library rule), so the two modes differ in noise through the CA mode's acceleration states.
- R, ca_acc_init_var = 10 and every other class are the constants of record (`shared\trackers\trk_constants_v01.json`).
- The constants file is `B_retrack\out\imm2t\IMM2_CONSTANTS_REC_v01.json`.

**Why κ_q is the κ of record (decided 22 Nov about 00:18 EST, tuning runs only, before any new-run value).**
- The frame first fixed κ_q by rule (2) on pre-onset frames.
- On the 20 tuning runs, the CV filter's pre-onset median NIS stays between 0.91 and 1.11 for κ = 10^(−3 + 0.05 j), j = 0…48, and falls below that for larger κ (0.63 at j = 60, 0.0014 at j = 120). There is no sign change, so the window [1.8, 2.2] is unreachable: while the lead cruises, the innovation is limited by R.
- Rule (2)'s "nearest value" would take the peak of this flat curve (j = 30, κ = 10^(−1.5), median 1.108), an unstable choice.
- The coordinator therefore kept the CV mode of record; the search is kept as a note (`IMM2_TUNE_KQ_v01.json`, its 121 grid medians copied from the search's log `kq_run1_killed.out` by `b_imm2_kq_note_v01.py`; the run was stopped at its final evaluation when the decision came).

**Tuning of σ²_hi: 20 lead-braking tuning runs only (`run_index_m4_v02.csv`: set = tune, family = lead_braking, use = 1).**
- **Statistic: A10 B3 rule (2), as frozen in `b3_nis_tune_v01.run_stat`, restricted to braking frames.** Per run:
  - The lead track is the re-tracked planner actor matched to the true lead at each decision of record. On these runs it is always the scenario target: 20 of 20 runs, every decision.
  - Its updates are those with frame index ≤ the largest state frame at which it was matched.
  - Keep the updates whose detector frame is a braking frame; take their mean position NIS, ν′S⁻¹ν (ν = z[0:2] − x_prior[0:2], S = P_prior[0:2,0:2] + R_rot[0:2,0:2]).
  - Take the median over the runs with at least one such update; that number of runs is reported.
- **Identity check, before any search:** with all frames kept, the restricted statistic reproduces the frozen one bit for bit on the 20 runs at the constants of record (median 1.99443; `IMM2_TUNE_CHECK_v01.json`).
- **Truth phases of a detector frame at simulation tick k:**
  - k_on = the first tick whose scenario request time (assessment_time_s, `scenario_frames.jsonl`) is ≥ the case's brake_start_s (`contract.json`, case.draw);
  - k_stop = the first tick ≥ k_on at which the true lead (the `evaluation_truth` target) has speed ≤ 0.5 m/s (VMIN of record);
  - braking frames: k_on ≤ k < k_stop (pre: k < k_on; stopped: k ≥ k_stop).
  - This matches the truth phase of record (`trk_arrays_v01`, oxsb_extract_v05) at every tick whose request time is logged.
- **Search:**
  - Variant B4, the CA filter alone, built on the CV diagonal of the κ of record.
  - σ_a² = 10^(−3 + 0.05 j), j = 0…160, κ_CA = 1. Evaluate in grid order.
  - Take the first sign change of (median − 2), then bisect on log10 σ_a² until |median − 2| ≤ 0.01.
  - With no sign change, take the grid value nearest 2; the text then says the window was not reached.
  - At σ_a² = 0.001 the braking-frame median is 3.67.
- **Outcome (22 Nov 00:23 EST, tuning runs only).**
  - The first sign change is between j = 59 (median 2.010) and j = 60 (1.957).
  - Bisection gives σ²_hi = 0.9172759353897799, median 1.9969, with all 20 runs used; the window is reached (`IMM2_TUNE_SA2REC_v01.json`).
  - Constants: `IMM2_CONSTANTS_REC_v01.json`.
- **Code:**
  - `B_retrack\code\b_imm2_tune_v01.py`, modes check, sa2rec (this search) and kq (the note);
  - outputs `B_retrack\out\imm2t\IMM2_TUNE_{CHECK,SA2REC,KQ}_v01.json`.
- **F0 for IMM2:** its own P̄ on the 120 tuning runs (A10 §2.1; the rule of record `trk_arrays_v01.pbar_accumulate`, as for B1r).
- **Lock:** before LOCK_A12a, and before any IMM2 value on any evaluation run (new or C), the following are frozen in FREEZE_B addenda:
  - the constants, the tuning outputs and all IMM2 code: re-track `b_imm2_v01.py`, analysis `b_fresh_analysis_v04.py`, mode probabilities `b_modeprob_v01.py`, export;
  - the Sonnet second programs;
  - then P̄_IMM2, as a data addendum.
- **Second IMM implementation (A10 §10.1(b)):** the five fresh runs of record (0288, 0324, 0384, 0450, 0582) with IMM2's constants. The library and `imm2\imm2_v02.py` must match: ids identical, P9 within 1e-9 relative.

**Scoring.** Open loop, 3 s, gridless frontier, all evaluated decisions, on IMM2's own room (F0 = P̄_IMM2; A10 §2.1). The keys are those of the IMM's row of Table III, as for IMMr.
- **Run sets:**
  - the 150 new lead-braking runs of §2.4 (**primary**): ids `pl12_<case>_native` with `l12\REPLACEMENTS_L12_v13.json`, ascending; the analysed set is §2.4's;
  - the 105 fresh C runs (**secondary**). IMM2 was specified after the C results of B1 and B1r were seen; the new runs are unseen.
- **Arrays:**
  - Re-track every run with IMM2 (`retrack_capture(cap, 'B1', const = IMM2's constants)`); extract with P̄_IMM2 exactly as for B1r.
  - Then a data manifest with per-file SHA-256, written before scoring.
- **Values per run set:**
  - RR_gl(N_IMM2) and its interval;
  - IMM2's amplitude-matched ranking oracle c (E5 at IMM2's own median ratio and spread; not a bound);
  - RR − c, R, RR_CK3, within5, room by estimated phase, lag;
  - H3's class with δ = 0.05.
- **Bootstrap:** run-level, 20,000 resamples, `optA_lib_v02.boot_counts(n, 20000, 20261911)`, runs ascending.
  - n = 105 for C; n = the analysed new runs for the new set, the draw shared by all §3 analyses.
- **Primary statistic, for §4's Holm.** The hypothesis "IMM2's covariance recovers part of its own room on the new runs" is tested by RR_gl(N_IMM2) > 0.
  - One-sided bootstrap p = #{b : RR*_b ≤ 0} / #{b : RR*_b finite} over the 20,000 resamples of the new-run draw (the convention of §3b).
  - The class is printed as H3 assigns it; Holm applies to this p.
- **Permuted twin (descriptive).** A11 §6b's construction, computed by session B with session CD's frozen Y programs, unchanged (`ycheck\y_twin_l12_v13.py`, `recount\rc_y_twin_l12_v13.py`).
  - Their B2 inputs are given IMM2's arrays as path arguments: the array folder, its manifest and the manifest's SHA-256.
  - The copies are byte-identical, kept in their own folders so that no output of CD's is touched.
  - Δ = RR_gl(N_IMM2) − mean over k of RR_gl(IMM2p_k), with K = 20 and `default_rng(20261931)`; on the new runs only (the programs' run list).
  - Percentile interval (`--intervals nominal95`) without A10 §2.6 calibration. IMM2's test is its class, not Δ.
- **Mode probabilities by truth phase (descriptive).**
  - Which decisions: every evaluated decision whose lead is matched to a re-tracked track.
  - μ_CA = that track's CA-mode probability after its last update or miss at or before the decision's detector frame (the tracker's mode record in the arrays).
  - Grouped by the decision's truth phase of record: pre, braking, stopped.
  - Printed per phase: the mean of μ_CA, its median, and the share of decisions with μ_CA > 0.5, with run-level percentile intervals on the run set's draw.
  - Printed for IMM2 on both run sets; for B1r on the C runs, as a reference.

**What is printed.**
- IMM2's row beside the IMM as first tuned and IMMr. Their values stand.
- RR, c, their intervals and the class; Δ to the twin; μ_CA by phase.
- The tuning outcome: σ²_hi, its median, and whether the window was reached; why κ_q is the κ of record.
- p, and its Holm-adjusted value in §4's table.
- The C-run values, labelled secondary and disclosed as specified after the IMM's C results were seen.

**Verification (A10 §10.1; A12 §7).** Second programs by Claude Sonnet 5.5, from this text and the raw inputs, not from B's code:
- the scoring recount of both run sets at K = 20,000, including p;
- the twin's second program (CD's `rc_y_twin_l12_v13.py`, above);
- the mode-probability summary from the capture files and the arrays' mode records;
- the A10 §10.1(b) five-run check (`imm2_v02`).

A result not recounted by 08:45 EST is not printed (§7).


## 4. Multiplicity

Holm across A12's primary hypotheses is reported beside the unadjusted results. Each analysis exports a one-sided bootstrap p-value for its primary statistic, defined in its section. A12's primary hypotheses are:
- DR2's class on the new runs;
- the dose-response trend;
- Y1 on the new runs;
- IMM2's class;
- §5's τ for CANMOT;
- §6's primary comparison.

## 5. Real-sensor mechanism check on nuScenes (session F)

Kendall τ within (scene, keyframe), between the covariance's 3 s predicted position spread and the realised 3 s CV-prediction error:
- for CANMOT and the IMM;
- with strata by real missed detections;
- designed on train, val scored once.

<!--MERGE:F5-->

## 5b. Real-log decision test under injected dropouts (a parallel worker under session F)

Asked for by the author's side at about 00:25 as the one item aimed at "simulation-only decisions". Agreed by session F at about 00:30 under these conditions:
- **Isolation:** a background Opus subagent started by F works on copies of F's real-log chain in `work\F_dropout_nus\`, never on F's frozen files.
- **Acceptance before any value:** with masks off and punish_num = 1, the copy must reproduce F's val T1 tracks bit for bit (or within A10 B0(a)'s 1e-14, platform stated), then F's val arrays within 1e-12.
- **Design, pre-registered straight on val:**
  - A11 §6c's mask law with the scene name as case id; T1 only; punish_num = 3.
  - F0 = the real-log class average of record (P̄_T1 from train, without masks). This is a stated limit.
  - F's adapter and its clearance rule (the rear-contact departure); 3 s horizon.
  - Sequence: room → E5_N → N's class (as X0–X2).
- **Limits:** its own pod, at most $6. Hard stop: if acceptance has not passed by 05:00 EST, it is dropped and the text says the attempt was made.
- **Lock:** LOCK_A12c locks this section with §5, before any masked val value.

<!--MERGE:F5b-->

## 6. Caution-matched closed-loop dropout test (session E)

F0 vs N under the A11 mask law and punish_num = 3:
- at one level calibrated under dropouts;
- N's scale matched to F0's open-loop caution under dropouts;
- on the never-run lead-braking cases;
- with one primary comparison.

<!--MERGE:E6-->

**Merged verbatim** from `E_A12_6_v02.md` (sha256 `81bd271870b95735d18a2ad0b32debcd7912dff2cd9b6105132bde4b6f821b43`); headings demoted two levels, nothing else changed. Where it and the coordinator's fixed choices above differ, the fixed choices govern.

### A12 §6: Caution-matched closed-loop dropout test (set E5, session E). Text v02

Written 22 Nov 2026, about 00:35 EST by the laptop clock, by session E. This is the draft for LOCK_A12a's snapshot; LOCK_A12b locks it, with g_D and g_N, before any main E5 run is captured. v02 supersedes v01. It records the coordinator's approval (00:30) of the two adjustments below, P̄_DR's SHA-256, the disclosure of (b), and the hashes of the artefacts already built.

**Approved adjustments, forced by the data that exist:**
- **(a) F0 is F0_D.**
  - It uses F's masked class average **P̄_DR**: `work\F_dropout\out\PBAR_DR_v01.json`, SHA-256 `a50b3a1df23107efdb2e76c1c6a318a24de7813fbb88eb396b28f667edafa685`. F computed it under the A11 masks with punish_num 3 on the 120 tuning runs; vehicle and pedestrian 4×4, counts 21,002 and 2,233.
  - FREEZE_DR lists only the test-old P̄ (`5355d1e4…`), so this file's hash is recorded here and in LOCK_A12b.
  - Reason: masked open-loop caution can only be computed for F0 with the P̄ that F's arrays were built with. Their per-row F0 threshold uses P̄_DR, and the row vectors needed to rescale it are not stored. F0_D is also the fair class average under dropouts.
  - Packet **`packet_e_v05`** = `packet_e_v04` with only `E_PBAR_CANMOT_v01.json` replaced by P̄_DR (tar SHA-256 `4eda7c41f734440a8522f109aa78e7709e4d6a695f4cef05c0e32d10293ab83d`).
- **(b) Design data for the matching.**
  - F's masked open-loop DR arrays of the **105 fresh lead-braking runs** of A11, in `work\F_dropout\out\arrays\DR\` (A11 masks, punish_num 3; cF0 with P̄_DR, cN from the tracker).
  - **Disclosure:** F's DR results on these 105 runs were already computed and seen (A11 D). Here they set only N's scale. They contain no outcome of the new test, and their cases are disjoint from E5's 135.
  - F has no per-row masked arrays of the tuning runs, only P̄ accumulators.

#### 6.1 Question
At equal open-loop caution under detection dropouts, does the tracker's own covariance (N), which grows while the tracker coasts, give fewer closed-loop contacts than the class average estimated under the same dropouts (F0_D)? This is tested on never-run lead-braking cases.

#### 6.2 Unchanged
- E4's closed loop and checks (A11 §6d):
  - CARLA, plant, the Codex planner, F2, fallback, detector, CANMOT;
  - the A11 §6c mask law (`A11D2`) and `output.punish_num = 3` for both arms;
  - A1 admission and native controls on every pod;
  - the reviews, including the mask-law, locked-table and method-equals-job checks.
- Statistics and classes as E (A10 §7.5): Newcombe hybrid-score interval (method 10, corrected φ); exact McNemar; time-lost case bootstrap `default_rng(20261922)` × 20,000; classes with contact ±0.10 and time lost ±0.5 s.

#### 6.3 Arms and packet
- **F0_D** (`E_F0`) with P̄_DR, and **N** (`E_N`), both CANMOT, both with the mask law and punish_num 3.
- **Packet `packet_e_v05`:** v04 plus only the P̄ file. The run's method records the P̄ file's SHA-256.

#### 6.4 Level, calibrated under dropouts (stage E5C)
- **Runs:** F0_D at g ∈ {4, 8, 16, 32} on the 30 lead-braking tuning cases of E2, with masks: 120 runs, dealt by case on pods claude-v13e-21…24.
- **g_D** is the g whose contact share (valid runs) is nearest 0.20. Ties go to the smaller g. If every share is below 0.05, g_D = 4 and the comparison is labelled low-power.
- The shares and g_D are recounted by the second program before LOCK_A12b.
- The E5C lists carry the A1 admission and controls on every pod. They are packet v05's smoke.

#### 6.5 N's scale, matched by open-loop caution under dropouts
- **g_N** is the scale on the 202-value grid of record (`[0] + logspace(−2, 3, 201)`) whose pooled open-loop caution on F's masked DR arrays (`cN`) is nearest F0_D's open-loop caution (`cF0`) at g_D. Ties go to the smaller g.
- The caution is as of record: W1, population "all", `optA_lib_v02.stats_scored`, as in E2's matching.
- **The mapping was computed BEFORE any calibration run, from the design data alone:** `work\E_closedloop\out\E5_MATCH_TABLE_v01.json`, SHA-256 `7fdb4e36d0514928d6c52d7a62c1022f12a901464a3513d0596cb14bd2531e3a`.

  | g_D | F0_D caution | g_N | N caution | Difference |
  |---|---|---|---|---|
  | 4 | 18.389 % | 5.957 | 18.219 % | −0.170 pp |
  | 8 | 21.340 % | 10.593 | 21.383 % | +0.043 pp |
  | 16 | 22.333 % | 14.962 | 22.328 % | −0.005 pp |
  | 32 | 24.566 % | 44.668 | 24.585 % | +0.019 pp |

- The row of the calibrated g_D is used. The second program recomputes the table independently, and LOCK_A12b records it.

#### 6.6 Main runs (stage E5)
- **Cases:** the **135 never-run lead-braking evaluation cases**, c1109_eval positions 55+ at each speed: 51 at 5 m/s, 33 at 10 m/s, 51 at 15 m/s. They are the same case ids CD captures open loop in A12 §2.
- **Runs:** F0_D at g_D and N at g_N, 270 runs, dealt by case so pairs stay on one pod, on pods claude-v13e-31…36.
- **Masks:** the locked table `work\E_closedloop\out\E5_MASKS_v01.json` (the 30 tuning plus 135 main cases; SHA-256 `010595907805f7434ad4fc04f963439fa3756e57406de983053e66910822d770`) is hashed in LOCK_A12b. Every run is checked against it.

#### 6.7 Analysis: one primary comparison
- **Primary:** N vs F0_D, paired by case over valid runs.
  - **Contact share:** the difference (N − F0_D) with the Newcombe 95% interval, and the exact McNemar test.
  - **Time lost:** the mean paired difference over pairs without contact, with the case bootstrap.
  - **Class:** E's rules.
- **One-sided bootstrap p-value** (A12 §4, used in its Holm step):
  - p = the share of the 20,000 case-bootstrap resamples whose mean paired contact difference (N − F0_D) is ≥ 0.
  - The resamples come from a fresh `default_rng(20261922)`, `integers(0, n, (20000, n))` over the n valid pairs, the same draw as the time-lost bootstrap.
  - H1: N has fewer contacts.
- **Descriptive:**
  - the other outcomes' paired differences, with the same bootstrap;
  - each arm's per-arm summaries as E;
  - the masked share;
  - the open-loop design cautions at g_D and g_N.
- **Validity** as E4: status CAPTURED_AND_REVIEWED, no policy failure, no contact before the window, mask = law = locked table, law `A11D2`, law-file hash, punish_num 3, method = job, controls identical.

#### 6.8 Second program and comparison of record
- A Sonnet 5.5 subagent writes it from this text and the raw files, not from the first program. It recounts:
  - the calibration shares and g_D;
  - the match table from F's arrays;
  - every main outcome, comparison, class and p-value;
  - the export.
- Comparison of record as A10 §10.1(c): counts exact, values within 1e-9, classes equal.

#### 6.9 Export
`work\E_closedloop\out\A_EXPORT_E5.json` and `A_RECOUNT_E5.json`, with the same 45 keys (`work\E_closedloop\tests\out\E5_EXPORT_KEYS_v01.json`):
- **Calibration:** `E5.cal.g<4|8|16|32>.contact`, `E5.g_D`, `E5.low_power`.
- **Matching:** `E5.g_N`, `E5.caution_F0D`, `E5.caution_N`, `E5.caution_diff`.
- **Cases and status:** `E5.n_cases`, `E5.status`.
- **Per arm:** `E5.<F0D|N>.<contact|vimp|tlost|restgap|peakdec|jerk|fallback|masked>`.
- **Primary comparison:** `E5.dc`, `E5.dc.ci`, `E5.dt`, `E5.dt.ci`, `E5.d_<vimp|restgap|peakdec|jerk|fallback>[.ci]`, `E5.class`, `E5.p_one`, `E5.mcnemar_p`.
- An undefined value or interval is null.

#### 6.10 Order, gates, budget
1. Packet v05 is built, then cross-model reviewed (Fable 5.2).
2. **E5C calibration capture**, from about 03:00. It is the v05 smoke, with A1 admission and controls.
3. Fetch; g_D; the settings file `E5_SETTINGS_v01.json` (g_D, g_N); the second program's recount.
4. **LOCK_A12b**, by the coordinator. It records the settings file, the match table, the mask table and P̄_DR.
5. **E5 main capture.**
6. Fetch; both programs; comparison of record.

- Results must be recounted by 08:45; otherwise they are not printed (A12 §7).
- Spend is about $10. Every pod is logged, the balance floor is $10, and deletes are confirmed.

#### 6.11 What it can and cannot show
- **It can show** whether N's coasting-grown covariance lowers contacts against a dropout-estimated class average at equal open-loop caution, on fresh cases. It is a confirmatory test of E4's hi signal.
- **It cannot show:**
  - the masks' effect apart from punish_num 3;
  - more than one level;
  - other scenarios;
  - closed-loop caution equality (the match is open-loop, on other runs);
  - the IMM pair.


## 7. Verification, cut-off and text

- A10 §10.1 applies to every printed value. Second programs are on Claude Sonnet 5.5 (or Fable 5.2), not the writer's model.
- Results recounted by 08:45 EST, or the result is not printed and the text says so.
- Text freeze about 09:15. Then a Fable claim audit, the same five seat cards on the same models as the sprint panel, one fix round, and the package by 11:45.

## 8. Model record

Coordinator and first programs: Claude Opus 5.5. Second programs: Claude Sonnet 5.5 or Fable 5.2.
