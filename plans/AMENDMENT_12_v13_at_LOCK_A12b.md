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


### 3d. DR at 10 Hz, a second configuration (session F) — locked separately by LOCK_A12d

Added at about 00:45 EST at the author's side's request, at lower priority than every 2 Hz analysis. Dropped, and the text says so, if its 10 Hz arrays are not on the laptop by 05:00 EST or if it would push any 2 Hz result past 07:30. It is secondary and not part of §4's Holm family. Nothing of it is computed before LOCK_A12d.

<!--MERGE:F3d-->

**Merged verbatim** from `A12_3d_DR_10HZ_v01.md` (sha256 `0f268a93152b2cb25ca9a2bd5d11c8b7f41b24f8d0d2bcb67e6b9e825f28a6c0`); headings demoted two levels, nothing else changed. Where it and the coordinator's fixed choices above differ, the fixed choices govern.

### Text for AMENDMENT_12 §3d: DR at 10 Hz, a second configuration on the new runs, v01

Drafted by session F (Claude Opus 5.5), 22 Nov 2026, about 00:55 EST by this laptop's clock, for the coordinator to merge verbatim into
`revision_v13\AMENDMENT_12_v13.md` §3d. Nothing below is computed before LOCK_A12d. Priority is below §3a and §5: if §3d would delay
their recounted results past 07:30 EST, it is dropped, and the text says so.

---

##### 3d. DR at 10 Hz (second configuration; session F)

**3d.1 Runs and rows.**
- **Runs:** the new runs of §3a, the same analysed set.
- **Rows:** B7's 10 Hz detector rows of each run, re-detected by session CD (`CD_capture\b7\<rid>\b7_detections_v13.jsonl`, the rows whose `rates_hz` holds 10;
  ticks k = 19, 21, 23, …). Row 0 is the first.
- **Re-tracking:** the online tracker of record through the frozen library, with B7's 10 Hz configuration (A10 B7; CD's chain
  `B7_10_0.1`): dt = 0.1 s, the process noise scaled by dt / 0.5 (q_scale), and latency 0.1 s. A decision at tick k uses the last row
  with k_row · 0.05 + 0.1 ≤ k · 0.05.

**3d.2 Masks: the one mask law in its 10 Hz form (`dr_masks_v04.mask` by parameter; the seed rule unchanged).**
- **Seed:** `rng = default_rng(int.from_bytes(sha256(("A11/D/" + case_id).encode()).digest()[:8], "big"))`, where case_id is the
  protocol case id.
- **Draws:** from row 1, at each row not inside a window, u = rng.random(). If u < p_row, with p_row = 1 − 0.9^(1/5), computed as the double `1 - 0.9 ** 0.2` = 0.0208516376390232
  (exactly a 0.10 chance per 0.5 s), then L = (5, 10, 15)[rng.integers(0, 3)] rows (0.5, 1.0 or 1.5 s, as at 2 Hz), and rows i … i + L − 1
  are masked, cut at the run's end.
- **Gap:** the 5 rows after a window (0.5 s, as at 2 Hz) are never masked and draw nothing.
- **Masked rows:** a masked row keeps its tick and time, and its detector output is the empty list.

**3d.3 Output rule.** `output.punish_num = 15`, the longest window in rows. This is A11 §6c's "longest window" rule at the 10 Hz row
rate, so the coasting lead is output through every window. The frozen library rescales `life_cycle.max_age` to the row rate
(`make_config`: cars 15 → 75 rows = 7.5 s), so no window deletes the lead.

**3d.4 F0.** F0 = P̄_DR, the 2 Hz class average under the 2 Hz masks on the 120 tuning runs (`F_dropout\out\PBAR_DR_v01.json`).
- A 10 Hz P̄ cannot be made: the tuning runs have no kept sweeps. P̄ of record would mix the dropout effect into F0.
- This is stated as a limit. RR_gl(N) against the P̄ of record is reported beside it, as A11 §6c.7 does.

**3d.5 Identity check (before any DR value).** With masks off and the configuration of record (punish_num = 1), the re-run arrays
reproduce CD's 10 Hz arrays of the new runs (`CD_capture\arrays_l12\B7_10_0.1\<job id>.npz`) to A10 B0(b)'s standard (1e−12 on
every key both builders produce). Check (ii), punish_num = 15 with no mask, reports the number of changed evaluated decisions.

**3d.6 Hypotheses (their own sequence; secondary, not in A12 §4's Holm list).**
- DR0–DR2 as A11 §6c.6, at the 10 Hz configuration: E5_DR, E5p_DR and the H3 classification on DR's own room.
- Draw: `optA_lib_v02.boot_counts(n, 20000, 20261911)`. Calibration per A10 §2.6. δ = 0.05.
- Reported beside the 2 Hz results of §3a as a second configuration. A one-sided p-value for r is exported but does not enter Holm.
- **Descriptive:** the in-dropout population and the masked share of rows.

**3d.7 Verification.** The second program of §3a (Claude Sonnet 5.5) extended by its own model from this text, without reading F's
code. Agreement per A10 §10.1(c).

**3d.8 Code, lock and export.**
- **Code:** `dr_extract_v03.py`, a copy of `dr_extract_v02.py` with only the 10 Hz rows, dt, latency, mask parameters and punish_num
  changed. It is frozen in a FREEZE_DR_A12 addendum before LOCK_A12d.
- **Export:** `work\F_nuscenes\out\A_EXPORT_DR10.json` and `A_RECOUNT_DR10.json`, with prefix `DR10.` and the keys of A11 §6c.


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
- **Departure from the acceptance rule above (coordinator, about 01:05 EST, before any masked val value):** the copy on the pod did not meet the literal float tolerances (tracks up to 4.55e-13 absolute, 1 ulp at about 2.5 km; critical scales up to 3.7e-9 absolute, at most 7.7e-11 relative). It was accepted on this record:
  - every discrete key was identical on all 150 val scenes;
  - every scored value of F's unmasked T1 chain was bit-identical from both array sets, all 20,000 resamples included, and equal to F's export;
  - the cause is the Windows math library, shown by reproducing the pod bit for bit with correctly rounded trigonometry;
  - A10 B0's record accepted last-bit replay differences of the same order.
  The worker's text below states the same.

<!--MERGE:F5b-->

**Merged verbatim** from `A12_5b_TEXT_v01.md` (sha256 `4732c9cfad2440a88d4586417ec443ce8187ac8e30df1bd77bc54a21fa10365b`); headings demoted two levels, nothing else changed. Where it and the coordinator's fixed choices above differ, the fixed choices govern.

### AMENDMENT_12 §5b. Decision test under injected detection dropouts on the nuScenes val logs (package F worker) — [F's text]

Status: written 22 Nov 2026, 01:07 EST by the laptop clock, by a worker of package F (Claude Opus 5.5). It was written before `LOCK_A12c.txt` and before any value of the masked val run. The design is the coordinator's; this section words it. The acceptance runs (masks off) came before this text; their results are in §5b.7.

#### 5b.1 Question
On real sensor logs, under injected whole-frame detection dropouts, does the masked tracker's own covariance N rank decisions better than the unmasked class average F0? This is A11 §6c's DR test (DR0–DR2) carried to the nuScenes val logs of package F.

#### 5b.2 Data and tracker
- **Data:** the 150 nuScenes val scenes of package F (`work\F_nuscenes\cache\val\<scene>.npz`): keyframes (2 Hz), truth annotations and CenterPoint detections, read only.
- **Tracker:** T1 only. This is CANMOT through the project's OnlineTracker, built exactly as `f02_track_v01.py` does (`OnlineTracker(tracker_config)`, F's `lib\`). It is fed each keyframe's detections in file order, with state_time = the keyframe's time.
- **Output rule:** `output.punish_num = 3` (record: 1). Every other entry of CANMOT's configuration of record is unchanged.

#### 5b.3 Masks
- **Law:** the one mask law of A11 §6c, through `dr_masks_v02.mask(case_id, n)` (an unchanged copy, same SHA-256 as F_dropout's).
  - case_id = the scene name, e.g. `scene-0003`; n = the scene's number of keyframes.
  - Seed: the first 8 bytes of SHA-256("A11/D/" + scene name).
  - Keyframe 0 is never masked. A window starts with probability 0.10, with length L uniform on {1, 2, 3}, and the keyframe right after a window is never masked.
- **On a masked keyframe:** the tracker gets an EMPTY detection list at that keyframe's time. It predicts only: CANMOT's no-detection branch (`tras_predict`, then `tras_punish`). A track missed for up to punish_num = 3 keyframes is still output.
- **The masks are fixed inputs.** They depend only on the scene name and the keyframe count, not on truth or outcomes.
  - Table: `masks\FN5B_MASKS_v01.json`, SHA-256 `0c433e37b49124d4de21fb9b6e5959b9b9e7f132e4b700324704039f1ad7d315`, written before the lock.
  - Totals: 981 of 6,019 keyframes masked (16.3 %), in 494 windows (169 of length 1, 163 of length 2, 162 of length 3); 2 scenes have no masked keyframe.
  - The run checks every scene's mask against the law.
- **"In dropout":** a decision is in dropout when its keyframe is masked (the latest keyframe at or before `now`, the arrays' `kf`).

#### 5b.4 Arrays and sources
- **Builder:** F's array builder, `f05_arrays_v01.py run_arrays` with its adapter `f03_adapter_v01.py` (an unchanged copy). It runs on the masked T1 tracks at the 3 s horizon, with F's decisions: every second sweep from each keyframe from keyframe 8 on, and −0.1 ≤ v0 ≤ 20.
- **Sources:**
  - F0 = the critical scales under P̄_T1, the T1 class average of record from the train scenes with UNMASKED tracks (`work\F_nuscenes\out\PBAR_T1_train_v01.json`, as used for F's val arrays). This is a limit (§5b.8).
  - N = the masked tracker's own covariance.
  - E = the squared true prediction error.
- **Clearance:** F's clearance under the departure, `work\F_nuscenes\cache\clear_v02\val\<scene>.npz`. It depends on truth and ego only, so it is reused.
  - The decision ticks are checked: the `sweep` and the NaN pattern of `clear` equal the masked arrays'.
  - These keys must equal F's val arrays exactly: `sweep`, `kf`, `now`, `age`, `idx55`, `evaluated`, `evaluated2`, `inpath` and `n_truth`.
  - `vbar`, `v0`, `des`, `clear` and `clear2` must have equal NaN patterns and lie within 1e-9 of F's. The pod's math library differs from the laptop's in the last bits (§5b.7).
  - Any failure stops the run.

#### 5b.5 Statistics and sequence (one-sided 0.025)
**Population and scoring.** The run unit is the scene (150, sorted names). Population 0 is every evaluated decision. Scoring is F's: 3 s commitment, the gridless step frontier, optA_lib_v02 and the v12 gridless code, reached through `trk_score_v01`.

**E5_N.** This is the amplitude-matched ranking oracle with N's own amplitude (A10 §2.2):
- m and A come from `ratio_summary` of the N/F0 margin ratios √(cF0/cN) over the evaluated decisions;
- u comes from `e5_u(F0, E)`;
- E5_N = `add_oracle(F0, m, A, u)`;
- E5p_N is the same with u permuted within scenes (`permute_u`, `default_rng(20261915)`).

**Statistics:**
- R = R_gl = D_gl(E, F0)/201;
- c = RR_gl(E5_N);
- c − c_p = RR_gl(E5_N) − RR_gl(E5p_N);
- r = RR_gl(N).

**Bootstrap and calibration:**
- The scene bootstrap is F's held-out draw: `default_rng(20261923).integers(0, 150, (20000, 150))`, as counts.
- Intervals are calibrated by A10 §2.6 exactly as F's `f06_score_v01.py heldout`:
  - outer `default_rng(20261912)`, 2,000 samples;
  - inner one stream `default_rng(20261913)`, 1,000 per outer sample in order;
  - the second inner stream `default_rng(20261914)` only when some statistic's nominal-95 % coverage is below 0.94;
  - the Monte Carlo SD from `default_rng(20261920)`;
  - F's level rule: 95 %, or the calibrated level, or 99 %.
- The fast evaluator (`f06k_kernel_v01`, an unchanged copy) is checked against `trk_score_v01.rr_gl` on the first 25 resamples (relative 1e-9), and the full-sample values against the library (1e-12).

**Sequence.** A step is confirmatory only when every earlier step passed.
1. **Room:** R's lower end > 0. Because the level is at least 95 %, this also implies that at most 2.5 % of resamples are non-positive; that share is reported.
2. **E5_N:** the lower ends of c and of c − c_p are both > 0.
3. **N's class by A10 H3's rule, δ = 0.05:**
   - r's lower end > 0: "recovers", with efficiency r/c;
   - else c's lower end > δ: "uninformative variation";
   - else c's interval inside (−δ, δ): "amplitude-limited";
   - else "inconclusive".

**Holm input (A12 §4).** p_r = (1 + #{r* ≤ 0, NaN counted}) / 20,001, over the 20,000 scene resamples.

#### 5b.6 Descriptive (not tested)
- the evaluated decisions in dropout and their share;
- the masked share of keyframes;
- in population 1 (evaluated decisions in dropout): R, RR(N) and c, with 95 % percentile intervals;
- the N/F0 ratio summary in dropout;
- the decision-equivalents of R and D(N).

#### 5b.7 Acceptance before any masked value: results
All of these ran on pod `claude-v13f-n01` (Linux, Python 3.12.16) between 00:44 and 00:57 EST, masks OFF and punish_num = 1.

**Environments on the pod:**
- **Tracking and arrays:** the laptop interpreter's exact versions of every third-party package the T1 tracker and planner path imports, traced on the laptop: numpy 2.5.4, scipy 1.18.1, pandas 2.2.2, opencv-python-headless 4.14.0.94, scikit-learn 1.9.1 and the rest of `fn_pods_v01.PINS_T`. Numba, shapely, lap and pyquaternion are absent, so F's stand-ins are used, as on the laptop.
- **Scoring:** F's venv (numpy 2.5.5, numba 0.68.1).

**1. Tracks (`out\ACCEPT1_TRACKS_v01.json`).** All 150 scenes; every non-float array is identical.
- Identical: `trk_kf`, `trk_id`, `trk_name`, `trk_score` and `trk_state_time` (381,280 rows), the row counts, the meta, and every NaN/±inf pattern.
- The float arrays differ in the last bits:

| Key | Largest absolute difference | Median ulp | Share of differing elements within 4 ulp |
|---|---|---|---|
| `trk_center` | 4.55e-13 (global coordinates up to ~2,500 m) | 1 | 96 % |
| `trk_vel` | 8.6e-14 | 7 | 43 % |
| `trk_size` | 1.07e-14 | 1 | 98 % |
| `trk_yaw` | 9.8e-15 | 4 | 82 % |
| `trk_P` | 8.2e-15 | 1 | 87 % |

- **Verdict:** not bit for bit. The literal standard "within 1e-14 absolute on every array" is **NOT met**: met for `trk_P` and `trk_yaw`; missed for `trk_center`, `trk_vel` and `trk_size`. One ulp of a nuScenes global coordinate (512–4,096 m) is 1.1e-13 to 4.5e-13; the largest centre difference, 4.55e-13, is one ulp of a coordinate between 2,048 and 4,096 m. No absolute bound of 1e-14 can hold on centres once any last bit differs.

**Cause (`code\fn08_trig_check_v01.py`; keyframes 0–2 of the worst scene, scene-0332, a check on the laptop of a few keyframes only):**
- The copied code on the laptop's own math library reproduces F's file bit for bit.
- With session B's correctly rounded sin/cos/atan2 switched on (`trk_exact_math_v01`, the project's switch for reproducing Linux pod logs on Windows):
  - keyframe 0 equals the pod's file bit for bit;
  - through keyframe 2, centre, size and yaw equal the pod's, and only 1 velocity element (1.1e-16) and 38 covariance elements of one row (≤ 6.9e-18) still differ.
- So the differences come from the Windows math library (mainly its trig), not from the copied code.

**2. Arrays (`out\ACCEPT2_ARRAYS_v01.json`, the pod's builder on the pod's accept tracks, against F's val arrays).** All 150 scenes. Every array key has the same shape and dtype, and every NaN/±inf pattern is equal.
- **Equal bit for bit:** `sweep`, `kf`, `now`, `age`, `idx55`, `evaluated`, `evaluated2`, `inpath`, `n_act`, `n_truth`, `n_match`; the meta's counts and identity flags.
- **Float keys differ in the last bits.** This includes the tracker-independent ones (`v_raw`, `v0`, `des`, `vbar`, `clear`): the ego's own pose arithmetic goes through the same math library.
- **Largest absolute differences:**
  - cE 3.7e-9 and cE_2 4.8e-9 (relative ≤ 7.1e-11);
  - cF0 7.0e-12, cN 5.9e-12, cF0_2 1.2e-11 (relative ≤ 7.7e-11);
  - cTG 7.1e-13;
  - clear 8.8e-13, vbar 9.0e-13, targets 2.2e-13, v0 1.7e-13, a_raw 1.1e-12.
- **Verdict:** the literal standard "within 1e-12 on every key" is **NOT met** in absolute terms for the critical scales (cE, cE_2, cF0, cF0_2, cN, cN_2). It holds in relative terms (≤ 7.7e-11 relative, from cancellation in small distances).

**3. Scored values (supplement, `out\ACCEPT3_SCORED_v01.json`, `code\fn09_accept_scored_v01.py`).** Do the differences change any scored value? F's unmasked T1 values were recomputed from both array sets with F's machinery: the departure clearance, both populations, and the 20,000 scene resamples. Every one is **identical bit for bit**:
- R_pp = −0.0052405586749980256 (all) and −0.03444999866817025 (in-path);
- R_deceq, n, D(N) and RR(N) (NaN);
- each of the 20,000 resample values of R, D(N) and n;
- the 95 % interval of R, [−0.12711, 0.13371].

Both equal F's exported values (`F_HELDOUT_v02.json`). In these data the last-bit differences leave every scored sum unchanged.

**Decision needed from the coordinator.** Acceptance 1 and 2 fail the literal absolute tolerances and pass:
- structurally (every discrete key identical);
- in relative terms;
- in every scored value (bit for bit).

The cause is identified. Two options:
- **(a)** Accept on the record above: structure identical, differences ≤ 4.6e-13 absolute on tracks and ≤ 7.7e-11 relative on critical scales, scored values identical, cause shown. The masked run then goes on the pod as designed.
- **(b)** Run the masked tracking and arrays on the laptop, where the copy reproduces F bit for bit, against the load rule.

The worker recommends (a).

**Code test of the masked chain (design split only, no val value).** The masked tracking, arrays and scoring ran end to end on train scenes with the same programs. A test on 12 scenes ran with reduced sizes. A dress rehearsal on 150 train scenes ran with the full single bootstrap and 200 outer samples. The rehearsal exercised every branch the val run can take, including the second inner seed (finish asked for it, and the rerun completed). It also gave the timing: about 2 min of tracking, 2 min of arrays, and about 19 min per inner seed at 2,000 outer samples on one pod. Results in `out\masked_train12\` and `out\masked_train\`; they are code tests on the design split, not evidence.

#### 5b.8 Limits
- **F0 does not see the dropouts.** It is the unmasked class average P̄_T1 from the train scenes (punish_num = 1). The test asks whether N beats a fixed class average under dropouts, not one re-estimated under dropouts (DR used F0_DR from masked tuning runs).
- **Masks and output rule are confounded.** Both change against F's held-out arrays, and no unmasked punish_num = 3 reference run is made, so a difference from F's held-out result mixes the two.
- **The masks are synthetic.** Whole keyframes of detections are removed (0.5–1.5 s windows at 2 Hz); these are not real sensor failures.
- **One tracker.** The IMM is not run under masks.
- **The val scenes are not new.** F scored them unmasked. There F-H0 did not pass (R_gl = −0.0052 pp, 95 % [−0.127, 0.134]), so room under masks is not assured; if room fails, the later steps are reported as not confirmatory.
- **Platform.** The masked run is on Linux, F's reference on Windows. The differences are at the last-bit level and change no scored unmasked value (§5b.7).

#### 5b.9 Programs (SHA-256 at this text)
See §5b.11 (the table at the end of this file).

#### 5b.10 Run after LOCK_A12c (once)
1. **Upload and start the run.** Upload `LOCK_A12c.txt` to the pod, then run `code\fn_run_masked_v01.sh` once there:
   - fn02 masked → fn05 masked → fn06 prep → calib (seed 20261913) → finish;
   - calib with seed 20261914 only if finish asks for it.
2. **Fetch.** Fetch `out\masked_val\` (results, `FN5B_RESULTS_v01.json`), `cache\tracks_masked\val\` and `cache\arrays_masked\val\` (for a recount), every file SHA-256 checked.
3. **Delete the pod.** It counts as deleted only if rc = 0 and its id is gone from the list.
4. **Report.** The DR-style values go to `out\FN5B_VALUES_v01.json`.

A10 §10.1's recount by a second program on another model (A12 §7) is the coordinator's to assign. It may read the masked arrays, the mask table and the draws.

#### 5b.11 SHA-256 of the programs and inputs
Computed at 01:07 EST from the files themselves. The pod's code is the bundle whose manifest is listed; every file was SHA-256 checked on the pod.

| Group | File | SHA-256 | Note |
|---|---|---|---|
| new (this folder) | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\fn_common_v01.py` | `13ab9266243272f650c86ca3096781dde3d7b8c2ad99f7329bcd65506fe4c6f1` |  |
| new (this folder) | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\fn02_track_v01.py` | `213b424307ed8d27b09871f3fde655e2e0b812f0dd839ecc5119d19933adae09` |  |
| new (this folder) | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\fn05_arrays_v01.py` | `34c1cac137f7887b5ff2ea8948b4a5e0a6098ad6154a92f6b496cc9733c07bb0` |  |
| new (this folder) | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\fn06_score_v01.py` | `ae8e7e28b40c71c81aa0be26e260176eea3a3dd658c20acfbdd19c13aa6b3359` |  |
| new (this folder) | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\fn_run_masked_v01.sh` | `b24b6734bddd89268ada1149e063de34a8c7689f2367b893c0a0783a75e66cf9` |  |
| new (this folder) | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\val_order_v01.txt` | `c48dcba5db06539b001f5d9bcb1a8cd9debf487ac853109bbac729f5f0d41dbb` |  |
| new (this folder) | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\fn07_accept_v01.py` | `afc112655704f7c5c49a70d02e6e77b83d305dadc0f27e4a8d5d75ddf9bfeff8` |  |
| new (this folder) | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\fn08_trig_check_v01.py` | `be297705f98db0da74cd4bf23d16d1df4a38e3af05947a413f68495fb3075af7` |  |
| new (this folder) | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\fn09_accept_scored_v01.py` | `9000741f608bd0b63f34846ee286c1e3cbbaea8bc207e501540e29647894413f` |  |
| new (this folder) | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\fn_pods_v01.py` | `5f87f050457b8ceeacaf8471d11d4a474327c43f4f12b356e043d92dce5bb0c3` |  |
| new (this folder) | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\fpods_n_v01.py` | `00f85a9d9f24da85a7643105121c9db458ddecccf3135b7cec76ced4de0c5b57` |  |
| unchanged copy | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\f03_adapter_v01.py` | `0b8871a40e54a1f928571c616958dab575ecd3a5af81d012eb4163f08aa86b88` | equal to ARS_TRIAL\revision_v13\work\F_nuscenes\code\f03_adapter_v01.py |
| unchanged copy | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\f06k_kernel_v01.py` | `8d32d5bfb246610059279e508f7c21bf91594fe5b19be6310d9700829a646a99` | equal to ARS_TRIAL\revision_v13\work\F_nuscenes\code\f06k_kernel_v01.py |
| unchanged copy | `ARS_TRIAL\revision_v13\work\F_dropout_nus\code\dr_masks_v02.py` | `63f786c540f41aa87c41047daf0f327c68e850c1f76757682c7d3ce02c11d953` | equal to ARS_TRIAL\revision_v13\work\F_dropout\code\dr_masks_v02.py |
| read only | `ARS_TRIAL\revision_v13\work\shared\trackers\trk_score_v01.py` | `1cab6f300ad85fc6007d9b46dae75f41202f010c2080c5987ef06a79921417b4` |  |
| read only | `ARS_TRIAL\revision_v13\work\shared\trackers\trk_env_v01.py` | `0219dd2ed6517109a3c913430a2f30ca756fc01f4f003c1347c4ddd4a9628cad` |  |
| read only | `<earlier-phase folder 1>\11_ojits\A6R\code\optA_lib_v02.py` | `b32a619a07f494e919f8d0bf112c8df4bed0957f051412c73819982a9a3f9898` |  |
| read only | `ARS_TRIAL\revision_v12\analysis\a9_common_v01.py` | `6ee4998074b00dfc678b2eb6e1ea349b951ad2569c6f4a13ec7376aaadc11edc` |  |
| read only | `ARS_TRIAL\revision_v11\analysis\rev_common_v01.py` | `872f3559198dcfcddf4ac01d8b0389b00db0855456fc0835973e4c651782cf6c` |  |
| read only | `ARS_TRIAL\revision_v13\work\F_nuscenes\lib\code149\online_tracker.py` | `69edbc02b6653889b4fb8b12d6ad23dd95ae0b7f932b7c93f76749ce4b22508f` |  |
| read only | `ARS_TRIAL\revision_v13\work\F_nuscenes\lib\tracker_config.json` | `a3bfe2f344e15b96392d5b372366ae95450211446f1781eed4afacb21d8dd586` |  |
| read only | `ARS_TRIAL\revision_v13\work\shared\trackers\trk_exact_math_v01.py` | `6a42ece0b2255e4c2ec15a5651ee8ac65671e63cce01895e1ff4227ead86f541` |  |
| read only | `ARS_TRIAL\revision_v13\work\F_dropout_nus\pods\code_bundle.json` | `a46db8b1ceb170c91edab4a27d9afd9f945de8e5fbe4097c404d6b3db86e36f2` | manifest: SHA-256 of every file uploaded (F lib: code149, vendor149, devkit, shims; the modules above) |
| input | `ARS_TRIAL\revision_v13\work\F_nuscenes\out\PBAR_T1_train_v01.json` | `01b3708895f58fa21beb48d34f8efbf030259cdcd77254e13e18c398e7fbf9ba` |  |
| input | `ARS_TRIAL\revision_v13\work\F_dropout_nus\masks\FN5B_MASKS_v01.json` | `0c433e37b49124d4de21fb9b6e5959b9b9e7f132e4b700324704039f1ad7d315` |  |
| input | `ARS_TRIAL\revision_v13\LOCK_A10_2.txt` | `02048a431e41c6310202328545ac8d91e71f5c1bba78c3906fc0a672c6c5a4df` |  |
| input | `ARS_TRIAL\revision_v13\work\F_dropout_nus\pods\val_bundle.json` | `1debc8715422d84ac028e96b3644e30ea5515e339ee437ee4aa9fd09eabceaad` |  |
| acceptance output | `ARS_TRIAL\revision_v13\work\F_dropout_nus\out\ACCEPT1_TRACKS_v01.json` | `01a9ceff13e4bbb406b8eacd2d713a692a42026120b89d56a6a4e773027ee265` |  |
| acceptance output | `ARS_TRIAL\revision_v13\work\F_dropout_nus\out\ACCEPT2_ARRAYS_v01.json` | `70a07e03745bbaefb903ed97e7c14a0a86688865a1d44126aa4923a76f070221` |  |
| acceptance output | `ARS_TRIAL\revision_v13\work\F_dropout_nus\out\ACCEPT3_SCORED_v01.json` | `562b93e3a94b1429004446907760a449f6fc5a3c9577b7046a3161b7d9637b2e` |  |
| acceptance output | `ARS_TRIAL\revision_v13\work\F_dropout_nus\out\HASH_F_tracks_T1_val.json` | `0e51c73a1aed9700e1507ccc7182318ed32fd1ec515ec7044408acdb1c8992a3` |  |
| acceptance output | `ARS_TRIAL\revision_v13\work\F_dropout_nus\out\HASH_POD_tracks_accept_val.json` | `e44a6d19317d3f9f524b7038b3ff4f8d91ccfec8508880d24a10f46da5ca86c6` |  |


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
