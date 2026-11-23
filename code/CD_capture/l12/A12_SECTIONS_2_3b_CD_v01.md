## 2. New lead-braking runs (session CD)

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
- **Capture settings.** C's settings, made by `l12\make_jobs_l12_v13.py` (`jobs_l12\JOBS_PL12_claude-v13cd-l<k>_v01.json`):
  - RTX 4090 pods, with L4 as a fallback;
  - per pod, 3 A1 admission runs and a crash control first, then one after every 50 study jobs;
  - every control must be identical to its reference (S equal, T bit-identical), or the pod's runs are not study runs.
- **Logs.** keep_raw is false: sweep frames are not archived, though FILE_HASHES.json lists them. Every log that the re-tracking (session B) and the dropout replay (session F) read is kept: detections, filter events and algebra, frames, scenario frames, evaluation truth, contract.
- **Archives.** They go to the pod-local disk and are downloaded to the laptop, each checked against its receipt, before any pod is deleted.

**2.3 Sealing.**
- Capture may start before LOCK_A12a. Until the lock, only receipts and pass/fail counts are read (A10 §5.2; `x_pods_v13.py seal` checks each archive against its receipt, status and keep_raw).
- CD's CV0 extraction runs only after LOCK_A12a exists. It uses the online tracker of record with the P̄ of record, by package B's frozen `trk_arrays_v01.extract(lead=True, a4=True)` as in C (`analysis\c_extract_v13.py`), and its program is frozen in a FREEZE_CD addendum before its first run.
- Nothing else of a new run is computed or read before the lock.

**2.4 Failures and the analysed set.**
- A10 §5.1 applies: one retry in a fresh process; a second failure is replaced by the next unused reserve of the same speed, with the failed case's α. Each replacement goes in `l12\REPLACEMENTS_L12_v13.json` (append-only) and is reported.
- A run captured on an allowed retry carries the worker's suffixed run id. Its arrays are aliased to the job id with no numeric change, as for X (A11 departure X-6).
- **Capture deadline: 22 Nov 04:30 EST.** The analysed set is the 150 listed cases, with replacements, that are CAPTURED_AND_REVIEWED by then. With fewer than 128 runs (85%), every A12 test on the new runs is reported as descriptive (under-run).

### 3b. Y replication (session B re-tracks, session CD scores)

A11 §6b applies unchanged to the new runs. Its definitions are `ycheck\CD_DEFINITIONS_Y_v13.md` (frozen in FREEZE_CD_add4), including the twin draw (K = 20, `default_rng(20261931)`, k outer, runs inner).
- **Data.** These are the 150 new runs of §2.4, in ascending run id: package B's B2 re-track of them (frozen as data in a FREEZE_B addendum, with per-file SHA-256), and CD's CV0 arrays of the same runs for the online-N reference.
- **Program.** The same first and second programs are used (`ycheck\y_twin_v13.py`, `recount\rc_y_twin_v13.py`). Only the run list, the B2 array folder, its manifest and the CV0 folder change, as arguments; that change is frozen in a FREEZE_CD addendum before the first new-run value. Both are run on the same pod with identical draws.
- **Resamples.** There are 20,000 run resamples, `optA_lib_v02.boot_counts(n_runs, 20000, 20261911)`.
- **Intervals.** The A10 §2.6 calibration for Δ uses seeds 20261912/13, the second inner seed 20261914 only where needed, and the Monte Carlo check 20261920. The emergency rule is that of A11 §3.7, with A12's cut-off.
- **Y1 (replication).** Δ = RR_gl(N_B2) − RR_gl(B2p) passes if its lower end is > 0.
- **One-sided bootstrap p-value (§4).** p_Y1 = #{b : Δ_b ≤ 0} / #{b : Δ_b finite} over the 20,000 resamples of Y's draw. Both programs export it; it enters A12's Holm adjustment.
- **Descriptive, unchanged.** Also reported: B2s and Δs, RR_gl(B2p), and the online-N reference.
- **Labels.** Y on the new runs is labelled "passed (amendment), replicated under rules fixed before the data" (§1).
