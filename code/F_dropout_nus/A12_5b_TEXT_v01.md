# AMENDMENT_12 §5b. Decision test under injected detection dropouts on the nuScenes val logs (package F worker) — [F's text]

Status: written 22 Nov 2026, 01:07 EST by the laptop clock, by a worker of package F (Claude Opus 5.5). It was written before `LOCK_A12c.txt` and before any value of the masked val run. The design is the coordinator's; this section words it. The acceptance runs (masks off) came before this text; their results are in §5b.7.

## 5b.1 Question
On real sensor logs, under injected whole-frame detection dropouts, does the masked tracker's own covariance N rank decisions better than the unmasked class average F0? This is A11 §6c's DR test (DR0–DR2) carried to the nuScenes val logs of package F.

## 5b.2 Data and tracker
- **Data:** the 150 nuScenes val scenes of package F (`work\F_nuscenes\cache\val\<scene>.npz`): keyframes (2 Hz), truth annotations and CenterPoint detections, read only.
- **Tracker:** T1 only. This is CANMOT through the project's OnlineTracker, built exactly as `f02_track_v01.py` does (`OnlineTracker(tracker_config)`, F's `lib\`). It is fed each keyframe's detections in file order, with state_time = the keyframe's time.
- **Output rule:** `output.punish_num = 3` (record: 1). Every other entry of CANMOT's configuration of record is unchanged.

## 5b.3 Masks
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

## 5b.4 Arrays and sources
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

## 5b.5 Statistics and sequence (one-sided 0.025)
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

## 5b.6 Descriptive (not tested)
- the evaluated decisions in dropout and their share;
- the masked share of keyframes;
- in population 1 (evaluated decisions in dropout): R, RR(N) and c, with 95 % percentile intervals;
- the N/F0 ratio summary in dropout;
- the decision-equivalents of R and D(N).

## 5b.7 Acceptance before any masked value: results
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

## 5b.8 Limits
- **F0 does not see the dropouts.** It is the unmasked class average P̄_T1 from the train scenes (punish_num = 1). The test asks whether N beats a fixed class average under dropouts, not one re-estimated under dropouts (DR used F0_DR from masked tuning runs).
- **Masks and output rule are confounded.** Both change against F's held-out arrays, and no unmasked punish_num = 3 reference run is made, so a difference from F's held-out result mixes the two.
- **The masks are synthetic.** Whole keyframes of detections are removed (0.5–1.5 s windows at 2 Hz); these are not real sensor failures.
- **One tracker.** The IMM is not run under masks.
- **The val scenes are not new.** F scored them unmasked. There F-H0 did not pass (R_gl = −0.0052 pp, 95 % [−0.127, 0.134]), so room under masks is not assured; if room fails, the later steps are reported as not confirmatory.
- **Platform.** The masked run is on Linux, F's reference on Windows. The differences are at the last-bit level and change no scored unmasked value (§5b.7).

## 5b.9 Programs (SHA-256 at this text)
See §5b.11 (the table at the end of this file).

## 5b.10 Run after LOCK_A12c (once)
1. **Upload and start the run.** Upload `LOCK_A12c.txt` to the pod, then run `code\fn_run_masked_v01.sh` once there:
   - fn02 masked → fn05 masked → fn06 prep → calib (seed 20261913) → finish;
   - calib with seed 20261914 only if finish asks for it.
2. **Fetch.** Fetch `out\masked_val\` (results, `FN5B_RESULTS_v01.json`), `cache\tracks_masked\val\` and `cache\arrays_masked\val\` (for a recount), every file SHA-256 checked.
3. **Delete the pod.** It counts as deleted only if rc = 0 and its id is gone from the list.
4. **Report.** The DR-style values go to `out\FN5B_VALUES_v01.json`.

A10 §10.1's recount by a second program on another model (A12 §7) is the coordinator's to assign. It may read the masked arrays, the mask table and the draws.

## 5b.11 SHA-256 of the programs and inputs
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
