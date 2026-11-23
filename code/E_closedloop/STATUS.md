# Package E (closed loop in CARLA): status

Owner: session E (Claude Opus 5.5, `claude-opus-5-5`). Spec: `..\..\AMENDMENT_10_v13.md` §0, §2, §7, §9 (§0 overrides; E cap $100, brake-test cap $3 per attempt, at most two attempts).

## Now (19 Nov 2026, 16:35 EST)
- **Build review done: PASS WITH FIXES** (Claude Fable 5.2, `review\REVIEW_E_BUILD_v01.md`): 1 blocking, 6 major, 11 minor. Fixes below; all applied except M4 (an IMM pod smoke, scheduled after `FREEZE_B`).
- **Packet for E1S/E1/E2: `packets\packet_e_v02.tar.gz`, SHA-256 `451a317df87ceaefb047041c0b92c45ad588e281f054b4838053344bbf7cadf3`** (receipt `packets\packet_e_v02_RECEIPT.json`; 31 bound files in claude_smoke_v01). F2 and every arm are frozen in it; nothing in it changes because of anything E1S or E1 shows. `packet_e_v01` is withdrawn (stale, review B1); it never went to a pod.
- Tests rerun on v02 content (running): executor, F2, and the full arms check over all 55 stored lead-braking runs.
- No pod created, nothing spent.

## Review findings and what was done
| Finding | Done |
|---|---|
| B1 packet_e_v01 stale (NaN crash in E_PS records; old tracker files) | `_json_safe` records; `packet_e_v02` built from `src\`; tests rerun on identical content |
| M1 $3 cap not enforced | E1 pod created with a 3 h deadline watchdog (≤ $2.67 at $0.89/h) and terminated as soon as E1 is read; E1S and the brake list of attempt a1 share that cap |
| M2 E1S not recorded | departure 3 below, recorded now (before any pod) |
| M3 worker could retry a brake run | E1S and E1 lists have `max_attempts: 1`; a second brake attempt is a new list after a fault, decided here |
| M4 IMM arms never smoked on a pod | two-job IMM smoke (E_F0_IMM, E_N_IMM on c1109_tune_0000) on the E3 packet after `FREEZE_B`, before E3 |
| M5 contact rule longitudinal | every E lead is in lane: D1 changes only the lead's speed law (`CD_capture\d1\src\actor_policy_d1_v01.py`), so the directional gap is the right test |
| M6 Newcombe φ | corrected: if ad − bc > 0 it is reduced by n/2, floored at 0 (Newcombe 1998 method 10 as statsmodels' `confint_proportions_paired(method='newcomb')`; reproduces its documented example [[10,5],[2,20]] → (−0.0643926050711, 0.2211160178958) to 12 digits) |
| Minor 1 natural fallback before the forced one | the brake run then fails as a fault (`e1_brake_v01.py`) |
| Minor 3, 4, 5, 6 | 2b lock path fixed; g_lo = g_hi or a zero level stops and asks the author; E2 rows must carry `valid`; matched scales at a grid end are flagged |
| Minor 7, 8 (readings) | impact speed from the last tick before the first contact; "full braking" = the (−5, −5) plan, as fallback or as a feasible row |
| Minor 2, 9, 11 | C1 of `test_e_arms` compares with the stored truth phase (the valid check is `test_ps_phase`); stage name noted; L4 allowed only with the A1 controls bit-identical (E1 uses RTX 4090 only) |
| Minor 10 | `test_e_arms` on all 55 runs: running |

**Disclosure from the reviewer (rule 2 of the coordination README):** a recursive text search the reviewer started in `<earlier-phase folder 2>` ran about two minutes before it stopped it; that tree contains `<excluded folder 1>` and `<excluded folder 2>`, and it cannot tell whether the search reached them. It printed nothing from them and used nothing from them. Nothing of E depends on that search.

## Freeze and E3 start (19 Nov, 21:00–21:10 EST)
- **`work\locks\FREEZE_E.json` written ~21:00 EST** (82 files, SHA-256 `0a613b6471dfd293a51d1a3e0557e6a830e519759cc65186c033186f4c27da98`), before any E3/E3b run: src (= packet_e_v03's claude_smoke_v01, file for file), packets v02 and v03 (tars + receipts), tools, analysis, tests and their outputs, E1/E2 outputs, recount program and outputs, LOCK_A10_2b and its note, STATUS.
- **`work\locks\FREEZE_E_ADDENDUM_v01.json`** (SHA-256 `49d37ef5…`): the 12 E3/E3b job lists (pods claude-v13e-04 … 09; E3 156 jobs each incl. A1 admission and controls, E3b 54 each), written by the frozen builder from the locked matched settings. E3 = 900 runs (Z once + 7 arms × 2 levels on 60 cases: c1109_eval positions 35–54 per speed; C used no replacement); E3b = 300 runs (F0, N, CK3, PS, TG at lo on the 60 `d1_e3b` cases).
- **`work\locks\FREEZE_E_ADDENDUM_v02.json`**: the full laptop arms check (review Minor 10) on all 55 stored lead-braking runs: 12,907 decisions, 219,419 rows, zero differences (constraint copy; F0, N, CK3, TG critical scales; E policy decisions at five scales; F2 plan).
- **Capture starts now** (coordinator, 20:58: capture may run after Lock 1; values stay sealed until LOCK_A10_2). Until `LOCK_A10_2.txt` exists, only receipts, job statuses and control-versus-reference flags of E3/E3b are read; e_collect / e3_analyse refuse to run.
- Pods: acquisition loop for claude-v13e-04 … 09 (RTX 4090, EU-RO-1, packet_e_v03; E3 list first, E3b list after it on the same pod); one session watchdog deletes any of them at creation + 7 h (`pods\E3_WATCHDOG.log`).

## E6 FINAL RESULT (A13 §2; 22 Nov 2026, 09:04 EST): bracketed 4-8, FAILED (amendment), recounted, 0 disagreements
- **Run:** `run_e6_v01.py main`, 09:00–09:03. 540 runs (E5 270 + E6 270), 540 valid, 0 missing.
- **Comparison of record:** per-run outcomes 540 compared, 0 disagreements; export 65 keys, 0 disagreements.
- **Exports:** `out/A_EXPORT_E6.json` (72a520cf…) and `out/A_RECOUNT_E6.json` (87c32b32…); hashes in `out/e6/SHAS_main.json`.
- **Primary:**
  - K = 135, T = 89.
  - c: N 0.207, F0D4 0.326, F0D8 0.244, F0D16 0.111.
  - t over T: N 25.417, F0D4 25.235, F0D8 25.451, F0D16 25.841 s.
  - Bracketed 4-8 (w 0.84). c_F0(t_N) 0.257.
  - **Δ = −0.050, 95% [−0.121, +0.022]**; ub95 +0.010; p_one 0.088; finite share 1.0.
  - **Label "failed (amendment)":** the two-sided upper end is not below 0. Holm does not reject.
- **Secondary:**
  - N vs F0D8: dc −0.037 [−0.109, 0.034], dt −0.03 s; inconclusive.
  - N vs F0D16: dc +0.096 [0.030, 0.166], McNemar 0.007, dt −0.37 s; class "worse" (F0D16 has fewer contacts, at about 0.37 s more time lost).
- **Pods:** all 6 deleted, each confirmed; about 7.9 pod-h, about $7.0; balance $5.48.
- **Reported:** to the coordinator, A and Paper work summary.

## E6 (A13 §E6; 22 Nov 2026, 06:45 EST): closed-loop caution frontier, frozen, then captured
- **Approval:** coordinator GO (stamped 06:52 on the coordinator's clock) for the recommended design:
  - F0_D (E_F0, P̄_DR) at g ∈ {8, 16} on the 135 E5 main cases, 270 new runs;
  - E5's N@g_N and F0_D@4 reused, with their public status disclosed;
  - primary Δ = c_N − c_F0(t_N), linear in time lost between bracketing F0 scales, case bootstrap, NaN counted against H1;
  - amendment test, entering A13's Holm.
- **Text:** shared notes `E_A13_E6_v01.md` (f60b92c9…).
- **Freeze:** `work\locks\FREEZE_E_ADDENDUM_v09.json` (16d6fdc9…, 34 files), written before any E6 run or value.
- **New files:**
  - `tools\make_jobs_e6_v01.py` and `jobs\JOBS_E6_claude-v13e-4{1..6}_v01.json` (g = 8 first);
  - `tools\balance_watch_e6_v01.py` (floor $3.5);
  - `analysis\e6_analyse_v01.py` and `analysis\run_e6_v01.py`; `tests\test_e6_primary_v01.py` (8 pass);
  - `recount\e_recount_e6_v01.py` (Sonnet; 15 tests pass).
- **Dry run of both programs** on the E5 runs only (K = 0): outcomes 270/270 agree; export 65 keys, 0 disagreements.
- **FREEZE_E_ADDENDUM_v10** (a2383dbb…): re-freezes `recount/test/make_synth_e5.py`, changed at 03:30:54 by the E5 recount pairing fix.
- **LOCK_A13a** written 06:49:05 (4428e5dc…). The label rule is amended by the coordinator: bracketed AND the two-sided `E6.delta.ci` upper end < 0; Holm reported beside it.
- **Capture:** pods 41–46 created 06:50–06:54; lists launched rc 0 (packet and list hashes verified on each pod).
  - The S3 gateway failed again and the laptop disk guard refused S3, so fetches went over SFTP through each pod, with per-pod finishers.
  - Confirmed deletes: 46 at 07:49, 45 and 44 at 08:00, 42 at 08:01, 41 at 08:18.
  - At 08:43: pod 43 at 45/49 (slow, about 27 runs/h; 0 failures; controls identical); 224/270 E6 runs on the laptop.
  - Balance $5.79.
- **Next:** pod 43 done, fetched and deleted; then `run_e6_v01.py main` (both programs and the comparison of record); then report to the coordinator. ETA about 09:15.

## E5 FINAL RESULT (A12 §6; 22 Nov 2026, 03:37 EST): caution-matched closed-loop dropout test, recounted, 0 disagreements
- **Design:** F0_D (P-bar_DR) vs N; A11 masks; punish_num 3; packet v05; 135 never-run lead-braking cases; 270 runs.
- **Calibration:**
  - F0_D contact shares on the 30 tuning cases: g=4 5/30, g=8 4/30, g=16 2/30, g=32 0/30.
  - g_D = 4, at the bottom of the grid; the 0.20 point lies below it.
  - Matched g_N = 5.957; open-loop caution 18.22 % vs 18.39 %.
  - Both programs agree; LOCK_A12b (8fe33669…) records the settings (73cc480c…).
- **Capture:**
  - 270/270 valid; 0 final failures; controls identical.
  - All 10 E5 pods deleted, each confirmed.
  - The S3 gateway was down, so all fetches went over SFTP; the last five ran in parallel.
- **Primary result:**

  | Measure | Value |
  |---|---|
  | Contacts | N 28/135 vs F0_D 44/135 (discordant 2 vs 18) |
  | dc | −0.1185 [−0.1827, −0.0550] |
  | McNemar p | 0.0004 |
  | dt | +0.181 s [0.111, 0.258] |
  | Class | **safer at no extra cost** |
  | p_one | 5e-05 |

- **Exports:** `out/A_EXPORT_E5.json` (20ecda6a…) and `out/A_RECOUNT_E5.json` (63b6be84…), 45 keys each.
- **Comparison of record:**
  - Before the fix, the second program had a pairing bug (level None vs 'D'; recorded in `out/e5/E5_COMPARE_NOTE_v01.md`). It was fixed in the second program only.
  - After the fix: 270 runs and 45 keys, 0 disagreements.
- **Reported** to the coordinator.

## E4 FINAL RESULT (21 Nov 2026, 17:33 EST): L and H analysed and recounted, 0 disagreements, published
- **Capture:**
  - 480 of 480 study runs: L 240 and H 240.
  - 0 final failures and 0 replaced runs.
  - A1 admission and controls identical on every pod; no halts.
- **Pods:** all 7 E4 pods (10 smoke, 11–16) deleted, each confirmed. E4 cost about $9.60; balance $69.42.
- **Fetch:** the RunPod S3 gateway failed twice ("failed to fetch user keys"). Pods 15 and 13 were fetched over SFTP through the pod; every run was receipt-verified.
- **Driver** `analysis/run_e4_v01.py --tag LH --publish` (log `out/RUN_E4_v01_LH.log`, outputs `out/e4_LH/`, hashes `out/e4_LH/SHAS.json`):
  - 480/480 valid.
  - Per-run outcomes: 480 runs, 0 disagreements. Export: 179 keys, 0 disagreements.
  - Published `out/A_EXPORT_E4.json` and `out/A_RECOUNT_E4.json`.
  - The lo keys equal the L-only run, 92 of 92.
- **Results:**

  | Comparison | Level | Contacts | Contact difference [95% CI] | Time-lost difference, s [95% CI] | Class |
  |---|---|---|---|---|---|
  | E4H1: N vs F0 | lo | 14/60 vs 16/60 | −0.033 [−0.097, 0.027] | +0.148 [0.078, 0.235] | **equivalent** |
  | E4H2: N_IMM vs F0_IMM | lo | 15/60 vs 16/60 | −0.017 [−0.071, 0.036] | +0.082 [0.045, 0.123] | **equivalent** |
  | N vs F0 (secondary) | hi | 3/60 vs 9/60 | −0.100 [−0.201, −0.016] | +0.248 [0.148, 0.362] | **safer at no extra cost** |
  | N_IMM vs F0_IMM (secondary) | hi | 6/60 vs 10/60 | −0.067 [−0.154, 0.009] | +0.229 [0.124, 0.361] | inconclusive |

- **Exploratory** (crosses the masks and punish_num 1→3):
  - At hi, F0 went from 3/60 in E3 to 9/60 (+0.100 [0.016, 0.201]); N stayed at 3/60.
  - Difference-in-differences of N − F0: −0.100 [−0.183, −0.033] at hi; −0.017 [−0.050, 0.000] at lo.
- **Reported** to the coordinator. A reads the published files.

## E4 stage L RESULT (21 Nov 2026, 16:14 EST): analysed and recounted, 0 disagreements
- **Stage L complete.** All 6 pods finished L with 43/43 each, 0 final failures, and controls identical. All 258 L jobs are fetched and receipt-verified.
  - The S3 gateway was unavailable for about 20 min ("failed to fetch user keys"). The fetch then ran briefly over SFTP and finished over S3.
- **Driver** `analysis\run_e4_v01.py --tag L` (log `out\RUN_E4_v01_L.log`, outputs `out\e4_L\`):
  - 240/240 runs valid in both programs.
  - Per-run outcomes: 240 runs, 0 disagreements. Export: 93 keys, 0 disagreements.
  - The second program's own law matches the mask table on 61 of 61 cases.
- **Hypotheses (lo):**

  | Hypothesis | Comparison | Contacts | Contact difference [95% CI] | Time-lost difference, s [95% CI] | Class |
  |---|---|---|---|---|---|
  | E4-H1 | N vs F0 | 14/60 vs 16/60 | −0.033 [−0.097, 0.027] | +0.148 [0.078, 0.235] | **equivalent** |
  | E4-H2 | N_IMM vs F0_IMM | 15/60 vs 16/60 | −0.017 [−0.071, 0.036] | +0.082 [0.045, 0.123] | **equivalent** |

  - About 19 % of detector rows in the window were masked.
- **Exploratory** (crosses the masks AND punish_num 1→3):

  | Arm | E3 contacts (no dropouts) | E4 contacts | Difference [95% CI] |
  |---|---|---|---|
  | F0 | 12/60 | 16/60 | +0.067 [−0.007, 0.145] |
  | N | 11/60 | 14/60 | +0.050 [−0.018, 0.124] |

  - The difference-in-differences of (N − F0) is −0.017 [−0.050, 0.000] (the same for NIMM).
- **H** is running on all 6 pods. A finisher fetches, verifies and confirm-deletes each pod as its H finishes. The LH run follows.

## E4 capture (21 Nov 2026, from 14:51 EST)
- **Smoke PASS** (`out\E4S_CHECK_v01.json`). The smoke pod was deleted at 14:45, confirmed, about $0.25.
- **FREEZE_E_ADDENDUM_v07** (SHA-256 `deb7e27a…`, 58 files).
- **LOCK_A11b** written 14:48:44 (SHA-256 `d3a11b4c…`): E layered 186 of 188, with 2 allowed.
- **Coordinator GO** at 14:49: start without waiting for the top-up; the balance was $63.28.
- **Pods**, all RTX 4090, with L lists launched 14:51–14:55; on every pod the packet hash is `b8d3fd15…` and the list hash equals the frozen list:

  | Pod | Id |
|---|---|
  | 11 | c4y0s96emadf1s |
  | 12 | 2wujdr043zxa1k |
  | 13 | e5cvaf4afrga12 |
  | 14 | z9rvqs1xl3kmui |
  | 15 | wq06iwltd5hqhi |
  | 16 | iveisp5d6befw9 |

- **Tools running:**
  - `tools\auto_e4h_v01.py` starts each pod's H list after its L list finishes.
  - Session watchdog: creation + 6 h.
  - Balance guard (`pods\E4_BALANCE.log`): alerts under $20; flags a stop on new pods under $15.

## E4 update (21 Nov 2026, about 14:35 EST): decisions, review, packet, smoke
- **Coordinator's decisions:**
  - punish_num = **3** for all arms (A11 §6c "Output rule under dropouts").
  - The mask law is A11 §6c final: seed by `int.from_bytes(sha256(...).digest()[:8], 'big')`; row 0 never masked; a gap row (unmasked, no draw) after every window. Every stretch is therefore 1–3 rows. Over the 60 cases the stretch counts are 131 / 126 / 122 (lengths 1 / 2 / 3), and 18.4 % of window rows are masked.
  - Budget: cap $80 (shared), confirmed. The smoke is allowed after review; capture waits for LOCK_A11b plus the coordinator's top-up confirmation.
- **§6d v02** is in the shared notes as `E_DROPOUT_A11_6d_v02.md`, aligned to §6c, and will be merged verbatim into A11 for LOCK_A11b. The car max_age is settled with citations: class 2, 15 updates.
- **Cross-model build review (Fable 5.2)**, `review\REVIEW_E4_BUILD_v01.md`: PASS WITH FIXES.
  - B1 is F's mask code (old wording); sent to F and the coordinator.
  - M1: law `A11D2`, `law_file_sha256`, and the locked **mask table `out\E4_MASKS_v01.json`** (61 cases, SHA-256 `c66d9192…`).
  - M2: punish_num pinned to 3.
  - M3: IMM no-update-on-masked-row check, keyed on the event `timestamp`. The reviewer caught a first version keyed on `index`. Tested: 0 violations on a masked run; 17 of 17 masked rows flagged on unmasked E3 events.
  - M4: the worker requires the E4 knobs; new status `E4_METHOD_MISMATCH`.
  - M5: documented.
  - **Re-review: PASS.**
- **Laptop tests, all PASS:**
  - law v02;
  - CANMOT output (punish 1 drops the lead from the 2nd masked row; punish 3 keeps it; the lead is present at the gap row, sometimes under a new id);
  - **masked IMM replay identity under punish 3: max difference 0.0**.
- **Second program (Sonnet) is final for E4:**
  - `recount\e_recount_v04.py`, SHA-256 `2b528c0b…`.
  - `e_recount_export_e4_v01.py`, `b0254d6a…`.
  - Its own law matches the mask table in 61 of 61 cases.
- **Packet:** `packets\packet_e_v04.tar.gz`, SHA-256 `b8d3fd1587da32ee3f5f15f8fdf46dbcec933d04819aa229db6e4dc59da13820` (35 smoke files).
- **Job lists:**
  - `JOBS_E4S_claude-v13e-10_v01.json` (8 jobs).
  - `JOBS_E4L_claude-v13e-1[1-6]_v01.json` and `JOBS_E4H_…`: 240 + 240 study runs; dealt by case; law A11D2, punish 3.
- **Smoke:** pod claude-v13e-10 (RTX 4090), created 14:29:38 and launched 14:30. The E4 session watchdog deletes the smoke pod at creation + 2 h and capture pods at + 6 h (`pods\E4_WATCHDOG.log`).
- **Driver after capture:** `analysis\run_e4_v01.py --tag L|LH` (first program, second program, comparison of record).
- **Next:** smoke check (`tools\e4s_check_v01.py`) → delete the smoke pod → FREEZE_E_ADDENDUM_v07 → LOCK_A11b and the top-up → capture L then H on pods 11–16.

## E4: closed-loop detection dropout (A11 §6d). BUILD in progress, 21 Nov 2026 from about 14:00 EST, $0, no pod
- **Coordinator's GO for the build**, about 14:00: 480 runs = F0, N, F0_IMM and N_IMM at lo, then at hi, on the 60 E3 cases.
  - The locked LOCK_A10_2b points are kept; no recalibration.
  - Lo is primary and is captured first.
  - **No pod** is created until the coordinator confirms the budget.
- **Pre-registration text**: `E_DROPOUT_A11_6d_v01.md` in the shared notes, sent about 14:10. Two items are open: punish_num, and F's exact draw order.
- **Build checks so far:**
  - Car deletion age: 15 updates = 7.5 s (`contracts\tracker_config.json`, class 2), as B7 recorded.
  - **Output rule `punish_num` = 1** in the pipeline of record, and in B's IMM wrapper: an unmatched track is output only for 1 missed update.
  - Laptop test (`tests\out\E4_CANMOT_OUTPUT_TEST_v01.json`, case c1109_eval_0480):
    - punish 1: the lead is absent from the 2nd masked tick on.
    - punish 3: the lead is present through 3 masked ticks, and the same id continues.
  - Windows can follow back-to-back. Exact stretch counts over the 60 cases (69 ticks each):

    | Stretch (ticks) | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
    |---|---|---|---|---|---|---|---|
    | Count | 116 | 117 | 112 | 7 | 11 | 7 | 1 |

    - 23 cases have a stretch over 3.
    - About 19.7 % of window ticks are masked.
  - Options sent to the coordinator: (A) 1, (B) 3, or **(B′) 7, recommended**: the longest stretch, below the deletion age. **Awaiting the decision.** The code takes any value from 1 to 14.
- **Packet v04 overlay `src_v04\`.** The frozen `src\` is untouched. The diff is `review\E4_V04_DIFF_v01.patch` (262 lines).
  - `e_dropout_v01.py`: the law.
  - Probe: on a masked tick the detector runs, the tracker gets `[]`, and `detections.jsonl` logs `masked` and `tracker_rows`.
  - `punish_num` is set for CANMOT and the IMM; the ARM_METHOD `dropout` record is written before the run.
  - Worker: knobs `dropout` and `punish_num`.
  - Review: perception replay with the mask and the run's punish_num; a mask-law check in the E record.
  - The dev packet is built (`packets\dev_packet_e_v04`, 35 smoke files).
- **Laptop tests, light and single process:**
  - Mask law: start rate 0.0992 over 125,879 eligible ticks; L shares 0.337 / 0.336 / 0.327; 69 updates per run. **PASS.**
  - **Masked IMM replay identity:** online OnlineIMM(punish 7) equals B's offline B1 on the same masked stream (20 masked ticks): tracks and actors max difference 0.0. **PASS.**
  - Analysis dry run on relabelled E3 values: 179 export keys; degradation and DiD exactly 0; classes as E3.
- **Running:**
  - Cross-model build review (Fable) → `review\REVIEW_E4_BUILD_v01.md`.
  - Second program E4 extension (Sonnet) → `recount\e_recount_v04.py`, `e_recount_export_e4_v01.py`.
- **Written:**
  - `tools\make_jobs_e4_v01.py`: e4s smoke (4 masked runs plus one unmasked E3 reproduction), e4l, e4h.
  - `tools\auto_e4h_v01.py`: H starts only after L, per pod.
  - `tools\finish_pod_e4_v01.py`: narrow fetch prefixes.
  - `analysis\e4_analyse_v01.py`: gated on `LOCK_A11b.txt`.
  - Pods for E4 will be named claude-v13e-10 (smoke) and 11–16.

## RESULT (20 Nov 2026, 04:59 EST): E3 / E3b analysed and recounted, 0 disagreements
- **Driver run.** `analysis\run_e_after_lock2_v01.py` ran from 03:42 to 04:59 and exited 0 (log `out\RUN_AFTER_LOCK2_v01.log`).
  - Lock 2 SHA-256 is `02048a43…`, and the matched file `dee03e7d…` is the one in LOCK_A10_2b.
  - Coverage: 1,200/1,200 arm jobs. All 900 E3 runs and all 300 E3b runs are valid in both programs.
- **First vs second program (A10 §10.1(c)), 0 disagreements in every comparison.** The output SHA-256s are in `out\RUN_AFTER_LOCK2_v01_SHAS.json`.

  | Comparison | Checked |
  |---|---|
  | E3 per-run outcomes | 900 runs |
  | E3b per-run outcomes | 300 runs |
  | Comparisons | 24, plus the recount's 2 labelled extras |
  | Exports (`A_EXPORT_E.json` vs `A_RECOUNT_E.json`) | 438 keys |

- **Hypotheses, at lo (g = 4, F0 contact 12/60 = 0.20 on the fresh cases):**

  | Hypothesis | Arm vs reference | Contacts | Contact difference [95% CI] | Time-lost difference [95% CI] | Result |
  |---|---|---|---|---|---|
  | E-H1 | CK3 vs F0 | 0/60 vs 12/60 | −0.200 [−0.318, −0.099], McNemar p < 0.001 | +0.163 s [0.105, 0.225] | **safer at no extra cost** |
  | E-H2 | N vs F0 | 11/60 vs 12/60 | −0.017 [−0.076, 0.040] | +0.016 s [−0.004, 0.037] | **equivalent** |
  | E-H3 | N_IMM vs F0_IMM | 12/60 vs 12/60 | 0.000 [−0.048, 0.048] | +0.019 s [0.001, 0.040] | **equivalent** |

- **Descriptive comparisons.**
  - **TG and PS at lo:** 0/60 contacts each, contact difference −0.200, and they lose less time than F0 (TG −0.128 s, PS −0.165 s). PS is NOT caution-matched (design caution 11.88 % against F0's 14.10 %); see `LOCK_A10_2b_NOTE_v01.txt`.
  - **At hi (F0 3/60):**
    - CK3, TG and PS: 0/60 each, inconclusive, with contact CI [−0.137, 0.019].
    - N: equivalent.
    - N_IMM: equivalent.
  - **Z (no uncertainty) vs F0:** 25/60 contacts, worse at both levels.
  - **E3b, constant and mild braking leads:** no contacts in any arm, so every comparison is inconclusive. CK3 and PS cost time; for example, PS mild braking +2.30 s.
  - **E3b, stop-and-go:** F0 5/20 contacts.

    | Arm | Contacts | Contact difference [95% CI] | Time lost | Result |
    |---|---|---|---|---|
    | CK3 | 0/20 | −0.25 [−0.469, −0.038] | +0.80 s | safer at a cost |
    | PS | 0/20 | −0.25 [−0.469, −0.038] | +2.35 s | safer at a cost |
    | TG | 1/20 | – | – | inconclusive |
    | N | 5/20 | – | – | inconclusive |

- **Files for A.** `out\A_EXPORT_E.json` (SHA-256 `4f21b5e9…`) and `out\A_RECOUNT_E.json` (`6b02c2d7…`) each hold 438 keys, with `lock2_sha256` set to Lock 2's hash.
- **Resources.**
  - Volume: E uses 10.77 GB of its 40 GB under `/workspace/claude_v13_e_v01/`.
  - Spend: about $28.81 for E in total.
  - Pods: none running.
- **Not done here.** Package A places the values into the text. Session E has typed no number into the text.

## Now (20 Nov 2026, 03:45 EST): capture done, all pods deleted, Lock 2 present, driver running
- **E3 900/900 and E3b 300/300 arm runs captured**, with no final failure on any pod and A1 controls bit-identical throughout.
- **All 1,200 arm runs**, plus every pod's A1 admission and control runs (60), are fetched and receipt-verified on the laptop.
- **All E3 pods are deleted**, each by `tools\finish_pod_e_v01.py` (all 210 jobs verified, then `terminate_e_v01.py`):

  | Pod | Deleted (EST) |
  |---|---|
  | 04 | 01:38 |
  | 08 | 03:02 |
  | 07 | 03:11 |
  | 09 | 03:17 |
  | 06 | 03:40 |
  | 05 | 03:41 |

  - Every delete was confirmed: rc=0 and the id absent from the pod list.
  - The account listed 0 pods at 03:41.
- **Pods 05 and 06 were first kept, correctly.** The fetch guard in `fetch_e_v01.py` sizes its free-space margin by every run on the volume under the prefixes (1,211 runs), not by the runs still to fetch. So it asked for about 80 GB free while 73 GB was available, refused, and the finish script kept both pods. The 40 missing runs were then fetched by exact job id (a 0.5 GB margin), and the finish re-run deleted both pods.
- **E spend** from the spend log, create to terminate for all 9 E pods: about **$28.81**.
  - E3 pods: $3.53–$4.21 each.
  - Balance: $106.14.
  - Cap: $100.
- **LOCK_A10_2.txt written 03:41:21** by the coordinator, SHA-256 `02048a43…`.
  - E is layered over 7 manifests: 132 of 133 files match; only STATUS.md is excluded, as the living file.
  - LOCK_A10_2b and its note are listed.
- **03:42: `analysis\run_e_after_lock2_v01.py` started**: first program, second program, comparison of record. The log is `out\RUN_AFTER_LOCK2_v01.log`.

## E3 / E3b capture and second-program checks (19 Nov, 21:30–23:20 EST)
- **Pods.** All six E3 pods are up, RTX 4090, EU-RO-1, packet_e_v03.

  | Pod | Name | Created (EST) |
  |---|---|---|
  | 04 | lfvzd6ibydzxxg | 21:33 |
  | 05 | txppklspeev235 | 22:57 |
  | 06 | e685tenbrfj8fh | 22:59 |
  | 07 | 89mjik2pz71884 | 23:02 |
  | 08 | 15ryb1qjm9jsxg | 23:04 |
  | 09 | miizhfdjw8ps1l | 23:06 |

  - Each pod runs its E3 list (156 jobs) first. `tools\auto_e3b_v01.py`, which reads statuses only (log `pods\AUTO_E3B.log`), starts the pod's E3b list (54) when E3 is FINISHED, and writes `READY_FOR_FETCH.json` when E3b is FINISHED.
  - Rate is about one run a minute per pod, so each pod needs about 3.5 h for its 210 runs.
  - The session watchdog deletes any E3 pod at creation + 7 h (`pods\E3_WATCHDOG.log`). Controls are bit-identical so far on every pod (ctlTrue).
- **DNS fault and fix.** Pods 05–09 failed 28 of 28 creates from 21:38 to 22:27. These were network errors, not lack of stock: the laptop's resolver took 5–40 s per lookup of api.runpod.io, longer than runpodctl's timeout.
  - `tools\acquire_e_v02.py` is a wrapper; frozen `pods_e_v01.py` and `acquire_e_v01.py` are not edited. It runs runpodctl with `GODEBUG=netdns=go`, which measured 2 of 2 successes against 0 of 2 for the default and cgo resolvers. It retries DNS failures, and before every create it lists pods and adopts any pod of the same name, so an uncertain create cannot duplicate a pod.
  - The session watchdog was restarted with the same setting.
- **Second program: fallback share (E2), recorded and fixed.** See `out\E2_COMPARE_NOTE_v01.md`.
  - The recount had counted only the fallback flag. A10 §7.4 says "decisions in full braking", which includes the (−5, −5) row chosen as a feasible row. 31 of 180 runs differed.
  - Recount v02 (Sonnet) fixed it. The E2 comparison is now 180 runs, 0 disagreements (`out\E_COMPARE_OUTCOMES_E2_v02.json`).
- **Second program: dict lead variant (E3b), found before any E3b data.** Real D1 contracts store the lead variant as a dict. v02 would crash when keying on it. The fix is going into recount v03 (Sonnet, running).
- **Plumbing test of the result path** (`tests\test_e_compare_e2relabel_v01.py`):
  - Method: the E2 values (design data) are relabelled into an E3/E3b-shaped design. Then `e3_analyse_v01` and the recount's `compare` run on identical inputs, and `analysis\e_compare_v01.py` compares them.
  - Agreed over 24 comparisons: pairs, a, b, c, d, Newcombe interval, McNemar p, time-lost bootstrap, classification, hypothesis labels.
  - One convention gap, which A10 §7.5 does not settle: for an outcome defined on exactly one pair, the recount reported a degenerate bootstrap interval (lo = hi). The first program reports none for fewer than 2 pairs. v03 adopts "undefined below 2 pairs", and the gap is recorded here.
- **Recount v03 is done** (Sonnet, `recount\e_recount_v03.py` SHA-256 `fb1a810e…`). It fixes the dict lead variant and adopts "no interval below 2 pairs".
  - E2 first vs v03: 180 runs, 0 disagreements.
  - Plumbing test first vs v03: 24 comparisons, 0 disagreements. The recount's two labelled extras (F0_IMM vs F0) are listed apart.
  - **`work\locks\FREEZE_E_ADDENDUM_v03.json`** (SHA-256 `5c33a8c8…`, 21 files) freezes these additions before any E3 value; LOCK_A10_2 does not exist yet.
- **Export checked against the interface (20 Nov ~01:25).** The coordinator's target is E3/E3b results with the recount by 20 Nov 20:00, with Lock 2 aimed at about 10:30.
  - `analysis\e_export_v01.py` did not match RESULTS_INTERFACE_v13 and the text's captions (Table IV, Table S9).
  - `analysis\e_export_v02.py` is now the export of record:
    - Per-arm summaries: contact share, MEDIAN impact speed, mean time lost, mean rest gap, MEDIAN peak deceleration, MEDIAN RMS jerk, and fallback pooled over decisions.
    - Caution keys `E3.<F0|PS>.<lev>.caution` (%), and `E3.NIMM.dropped`.
    - The PS caveat key is kept.
  - The second program writes `A_RECOUNT_E.json` (`recount\e_recount_export_v01.py`, Sonnet).
  - Dry run on the relabelled E2 values: 218 keys each, 0 disagreements (`e_compare_v01.py export`).
  - **`work\locks\FREEZE_E_ADDENDUM_v04.json`** (SHA-256 `3da15871…`) freezes these files. The coordinator was asked to layer it into LOCK_A10_2.
  - Possible definitional gap: E3.n_cases is all cases of record (first program) against cases with a valid run (second). They differ only if every run of a case is invalid.
- **Interpretation recorded under A10 §11 (20 Nov 2026, about 01:25 EST, before any E3 or E3b value; LOCK_A10_2 does not exist).**
  1. A10 §7.4 defines the outcomes per run, but names no summary statistic for the per-arm levels.
     - The per-arm levels follow the text's captions (Table IV, Table S9):
       - contact share;
       - median impact speed (over runs with contact);
       - mean time lost (runs without contact);
       - mean rest gap;
       - median peak deceleration;
       - median RMS jerk;
       - fallback as the share of decisions in full braking, pooled over the arm's decisions.
     - These medians and means were chosen to match the captions. They are presentation summaries and feed no test.
  2. The A10 §7.5 analyses are reported as pre-registered:
     - contact: paired difference with the Newcombe interval and exact McNemar;
     - time lost: paired mean difference over pairs without contact, with the case bootstrap `default_rng(20261922)`, 20,000;
     - "Other outcomes: descriptive, with the same bootstrap": paired mean differences of impact speed, rest gap, peak deceleration, RMS jerk and per-run fallback share, each over the pairs where the outcome is defined for both runs, with the same case bootstrap.
     - New export keys: `E3.<arm>.<lev>.d_<vimp|restgap|peakdec|jerk|fallback>` and `E3b.<v>.<arm>.d_<…>`, each with `.ci`.
     - No interval is reported for an outcome defined on fewer than 2 pairs; A10 is silent on this.
  3. Classifications and E-H1 to E-H3 use contact and time lost only, as in A10 §7.5. Nothing here changes them.
  - **Export of record: `analysis\e_export_v03.py`** (v02 plus the §7.5 paired differences; an undefined interval is written as None, which A prints as n.c.).
  - The second program's exporter is `recount\e_recount_export_v02.py` (Sonnet).
  - Dry run on the relabelled E2 values: 438 keys each, 0 disagreements.
  - **`work\locks\FREEZE_E_ADDENDUM_v05.json`** (SHA-256 `fe5bc4dc…`) freezes these files. The coordinator has the SHA, and A has the key names (`E_EXPORT_KEYS_FOR_A_v01.md` in the shared notes).
  - In the run sequence below, use e_export_v03 and e_recount_export_v02.
- **Run sequence after `LOCK_A10_2.txt` exists** (all from `work\E_closedloop`):
  1. Final fetch: `tools\fetch_e_v01.py e3_ e3b_`.
  2. First program:
     - `analysis\e_collect_v01.py e3 --out out\OUTCOMES_E3_v01.json`, and the same for e3b.
     - `analysis\e3_analyse_v01.py --e3 … --e3b … --lock2b out\E2_MATCHED_v01.json --out out\E3_RESULTS_v01.json`. First check that this file's SHA matches the one in LOCK_A10_2b.
     - `analysis\e_export_v03.py --status ran --e1 out\E1_VERDICT_a1_v01.json --matched out\E2_MATCHED_v01.json --e3-outcomes … --e3b-outcomes … --results …`, which writes `out\A_EXPORT_E.json`.
  3. Second program:
     - `recount\e_recount_v03.py outcomes runs e3_` and `… e3b_`.
     - `compare … --e3b … --low-power false`.
     - `recount\e_recount_export_v02.py`, which writes `out\A_RECOUNT_E.json`.
  4. `analysis\e_compare_v01.py`, in three modes: `outcomes` (E3, E3b), `compare` (results) and `export` (A_EXPORT_E vs A_RECOUNT_E). Any disagreement stops the work until its cause is recorded and fixed.
- **Pod 04 done and deleted (01:38).**
  - E3 finished 156/156 and E3b 54/54, with no final failures and controls bit-identical.
  - All 210 jobs are fetched and receipt-verified on the laptop: 200 arm runs plus 10 admission and control runs.
  - `terminate_e_v01.py` confirmed the delete: rc=0, and the id is absent from the pod list. Spend row logged; balance $115.97.
  - E3 driver frozen in `FREEZE_E_ADDENDUM_v06.json` (SHA-256 `507f920e…`). A watcher waits for `LOCK_A10_2.txt`.
- **Confirmed termination (23:50).** CD reported that `runpodctl pod delete` can return rc=1 with the pod still running.
  - `pods_e_v01.delete` already required rc=0.
  - `tools\terminate_e_v01.py` adds a second condition: the pod id must be absent from the pod list before TERMINATED or the spend row is written. Otherwise it re-sends the delete, for at most 12 rounds, and writes nothing.
  - The session watchdog now uses it. Every manual E3 termination uses it too.
- **Fetch, incremental:**

  | Pass | Time (EST) | Runs on volume | Fetched and receipt-verified | Values computed | C: free |
  |---|---|---|---|---|---|
  | 1 | ~23:40 | 147 | 147 (`pods\fetch_e3_inc1.out`) | none | 91 GB |
  | 2 | 00:50 | 526 | 379 new, 147 already present (`pods\fetch_e3_inc2.out`) | none | 87 GB |

  Pod 04 finished E3 with 156/156 at 00:12. Its E3b list was launched with hashes verified (jobs `c0ef8767…`, packet `f3eb32c9…`).

  Further passes run as pods finish.
- **Not done yet.** Fetching E3/E3b archives as pods finish. After `LOCK_A10_2.txt`: e_collect → e3_analyse → e_export, plus the recount and e_compare.

## Deadlines (A10 §0.5)
| When (EST) | What |
|---|---|
| 20 Nov 06:00 | E build reviewed (cross-model) |
| 20 Nov 16:00 | `work\locks\FREEZE_E.json` |
| 21 Nov 06:00 | E1 brake test passed, or E stops |
| 21 Nov 18:00 | E results and recount complete |

## Plan of the ladder
1. Review passes → one pod `claude-v13e-01`: list `JOBS_E1S` (A1 admission crash + benign, 6 integration smoke runs of the CANMOT arms on tuning case c1109_tune_0000; a failure there is a build fault, not a brake attempt) → if clean, list `JOBS_E1_…_a1` (3 brake runs) on the same pod → `analysis\e1_brake_v01.py`.
2. E1 passed → E2 on 2–3 pods (`JOBS_E2_*`, 180 F0 runs + controls) → `e_collect_v01.py e2` → `e2_matched_v01.py` (needs B's IMM arrays) → `work\locks\LOCK_A10_2b.txt`.
3. Before the freeze: `packet_e_v03` (= v02 + CD's final D1 files and probe scene-class line + B's frozen tracker library, constants, P̄_IMM); IMM pod smoke (review M4) → `FREEZE_E.json`. After `LOCK_A10_2.txt`: E3 (900) and E3b (300) on as many pods as stock allows → `e_collect_v01.py` → `e3_analyse_v01.py` → second program (different model) recount.

## Build (E0): files and checks
| File | What |
|---|---|
| `src\e_sources_v01.py` | Online sources: line-for-line copy of the consumer's constraint builder (plus normals), F0 (P̄ of record), N, CK3 (3 m/s², a-hat gate, path shift), TG (r0 = 2), PS (phase from the online lead), online track history |
| `src\e_arms_v01.py` | Arms E_Z, E_F0, E_N, E_CK3, E_TG, E_PS, E_F0_IMM, E_N_IMM, E_BRAKE on the native 712 executor; g·s_A ≤ d², d ≥ 0, no q term; F2 servo |
| `src\probe_e_v01.py` | Copy of `probe_arms_v01.py`: E arms, F2, track-history feed, online IMM for the IMM arms (CANMOT audit hooks off there; B's recorder logged), `e_decisions.jsonl` |
| `src\worker_main_v01.py`, `src\cuda_entry_smoke_v01.py`, `src\review\review_case_e_v01.py` | Worker with E fields and `capture_e`/`review_e`; review = outcome accounting + perception prefix (CANMOT arms) + E-record check |
| `src\e_imm_v01.py`, `src\trackers_b\` | Online IMM adapter around B's `V13Tracker('B1')`; B's library files (to be replaced by the frozen copies) |
| `src\E_PBAR_CANMOT_v01.json`, `src\E_F2_PLANT_v01.json` | P̄ of record; F2 car model |
| `tools\build_e_packet_v01.py`, `make_jobs_e_v01.py`, `pods_e_v01.py`, `acquire_e_v01.py`, `fetch_e_v01.py`, `remote_chain_v01.sh` | Packet, job lists (E1S, E1, E2 written; E3/E3b builders read the matched settings and refuse without LOCK_A10_2b), pods (CD's helper, prefix `claude-v13e-`), archive fetch |
| `analysis\e_outcomes_v01.py`, `e_collect_v01.py`, `e1_brake_v01.py`, `e2_matched_v01.py`, `e3_analyse_v01.py` | §7.4 outcomes, collection with validity, E1 rule, §7.3 matched settings, §7.5 tests (Newcombe hybrid score, exact McNemar, case bootstrap 20261922) and classification. E3/E3b collection and analysis refuse to run without `LOCK_A10_2.txt` |

| Laptop check (`tests\`) | Result |
|---|---|
| A1 constraint copy = consumer, every row (d, p, q, tags, s, v, a, cost, targets) | 0 of 33,000+ rows differ (tuning 0000/0006/0012, old 0005/0006/0007) |
| A2 online critical scales = stored open-loop arrays: F0, N (gateR_rt_v01), CK3 (A4 extract), TG (v12 cTG2) | 0 rows differ, max relative difference 0 |
| B1 the E policy, fed the logged inputs, selects the open-loop row: E_F0, E_N, E_CK3, E_TG at g ∈ {0, 0.25, 1, 4, 16} | all decisions agree (e.g. 300/300 per arm and scale) |
| B2 F2 plan acceleration = trajectory(targets, model state)['a'][:2] | 0 mismatches |
| PS phase online vs stored tracker-estimated phase (35 old runs; thresholds −1.0, −0.5, −2.0) | 9,307/9,307 at each threshold; same lead track in 9,306 |
| F2Servo vs stand-in FixServo (F2 on, F3 off), 461 ticks × 3 speeds | equal term for term; stand-in car stops 3.95 / 12.68 / 26.24 m vs model 3.86 / 12.80 / 26.74 (= stand-in record) |
| Executor end-to-end (712 SensorExecution + E policy + F2), 700 ticks, every CANMOT arm | no error; selection sink at all 300 origins; records = decisions |
| IMM replay identity (A10 E0): online adapter + ObservationStream vs B's offline `retrack_capture('B1')` | bit-identical tracks and actors on 3 runs with B's constants (`tests\out\IMM_REPLAY_*_v01.json`) |
| Job lists validated by the E worker (`load_jobs`, knob args, stage dispatch) | pass |
| Matched-settings dry run on a synthetic E2 input (code test only) | runs; N's matched g ≈ F0's/1.1² as the recorded N/F0 ratio implies |

## Departures and interpretations (A10 §11; recorded before any closed-loop value exists)
1. **PS lead track online.** The open-loop phase (a9_4a) used the logged actor matched to the *true* primary. Truth is not available to a closed-loop planner, so E_PS takes as lead the actor whose predicted centre at the decision time is ahead of the ego centre (x > 0, planner frame) within 1.75 m of the route line (the lane rule of A10 §2.5), nearest in x. Speed and acceleration estimates as A10 §2.4 / a9_4a. On the 35 old runs this gives the stored phase in 9,307/9,307 decisions (`tests\out\TEST_PS_PHASE_v01.json`).
2. **Brake test operationalised** as the stand-in's STOP mode: zero margin until decision tick 199 (5 s into the assessment), then the fallback at every decision; benign tuning cases c1109_tune_0023 / 0011 / 0005 (5 / 10 / 15 m/s; parked vehicle 7–9 m to the side). Distance from the first fallback decision to standstill (measured speed < 0.05 m/s), against `trajectory(-5,-5,v0,a0,desired,H=12)`.
3. **Departure: a paid pod integration step (E1S) before the brake test.** A10 §7.1 lists E0 as free and E1 as the first paid step. E1 runs as two lists on one pod: E1S (A1 admission controls crash + benign, and one smoke run per CANMOT arm on the lead-braking tuning case c1109_tune_0000; 8 jobs) and, only if E1S finished with every job CAPTURED_AND_REVIEWED and both controls bit-identical, the brake list. Rules: (a) F2, the arms and the packet are hash-frozen before E1S (`packet_e_v02`, SHA-256 above); (b) no E1S outcome (contact, distance, time) is read — only job status, review status, policy-failure flags and control identity; (c) a failure in E1S is an E0 build fault: the pod is terminated, the cause repaired, and the brake attempt count is unchanged; (d) E1S and brake attempt a1 run in one pod session under the $3 cap (3 h watchdog). Reason: a pipeline fault (import, packet, F2 wiring) must not consume one of the two brake attempts.
4. **Reviews on the pod.** The native-ego replay of `review_case_v01` rebuilds an old-arm executor and cannot replay an E arm; E captures run outcome accounting (unchanged), the perception prefix (CANMOT arms) and an E-record check; the decision replay is checked on the laptop.
5. **E2 g = 0** is run as E_F0 with g = 0, which is the zero margin by definition.
6. **E3 cases.** "The next 20 per speed after C's, in id order": positions 35–54 of each speed's sorted evaluation lead-braking list (first cases c1109_eval_0726 / 0672 / 0480 at 5 / 10 / 15 m/s), shifted past any replacement case C uses (CD flags these).
9. **PS is not caution-matched (recorded 19 Nov 20:55 EST, after the coordinator's question; `work\locks\LOCK_A10_2b_NOTE_v01.txt`).** A10 7.3's "its H4 triple at that caution level" is read as A10 5.5's rule at l = F0's open-loop caution at g_L (lowest wrong-go among triples with design caution ≤ l; ties to the lowest caution). It bounds caution, it does not target it: the zero-wrong-go triple of design caution 11.88 % is chosen at both levels (F0: 14.10 % lo, 22.30 % hi). No other rule is substituted. PS's E3/E3b comparisons with F0 are descriptive with the caveat "PS is not caution-matched (11.88 % against 14.10 % / 22.30 %)", which session A must print.
8. **First-program readings revised on 19 Nov, 16:20–16:45, before any E data existed** (after the build review and the second program's README; no closed-loop or fresh value had been computed): contact by truth gap requires the two truth boxes to overlap in the ground plane (separating-axis test; the gap alone is negative for an actor beside or behind the ego; on the 120 stored tuning runs this gives the logged contact accounting in 119, the 120th being a 2 cm truth-box overlap without a sensor event, which the amendment's truth-gap clause counts); rest gap only to a stopped (≤ 0.5 m/s), in-path lead ahead; deceleration and jerk from the ego speed (velocity norm); the time-lost and descriptive intervals resample all valid pairs (cases) and recompute the statistic on the defined pairs; a contact in a brake run is reported, not a criterion (A10 7.1).
7. **PS triple at a level** (§7.3 + §5.5): the H4 rule applied at ℓ = F0's open-loop caution at g_L (`triple_choice` of a9_3 v02, verbatim), phases by the tracker estimate with threshold −1.0.

## Pods and spend
- **claude-v13e-01** = `t6uh20ixg2ii1b`, RTX 4090, EU-RO-1, $0.89/h, created 16:27 EST for E1S + brake attempt a1 (cap $3). The create call succeeded but the following status calls timed out (RunPod API DNS timeouts), so the acquisition loop recorded "no pod"; found with `runpodctl pod list` at 16:31, adopted by hand: record, SSH config, watchdog to 19:27 EST (creation + 3 h), spend row at 16:34 (balance 175.91). The loop was stopped; no other E pod exists. `tools\pods_e_v01.py` now writes record, watchdog and spend row before any status call. Chain started 16:34 EST (packet hash on the pod = `451a317d…`).
- **E1S passed (17:07 EST)**, `out\E1S_CHECK_v01.json` (status fields only): 8/8 CAPTURED_AND_REVIEWED; both A1 controls (crash, benign) bit-identical to their references; all six E arms passed outcome accounting, the perception prefix (detector re-executed, CANMOT replay exact) and the E-record check; no policy failure; captures 72–79 s. No E1S outcome was read.
- **Brake attempt a1 started 17:08 EST** on the same pod (`JOBS_E1_claude-v13e-01_a1.json`, 3 runs, one attempt each).
- **E1 PASSED at the first attempt (17:20 EST).** `out\E1_VERDICT_a1_v01.json` (first program), `out\E1_RECOUNT_a1_v01.json` (second program, Sonnet): identical to the last digit. Stopping distance from the first fallback decision (tick 199) against the planner's model: 5 m/s 3.830 vs 3.858 m (ratio 0.993); 10 m/s 12.606 vs 12.790 m (0.986); 15 m/s 26.224 vs 26.704 m (0.982); no policy failure, no contact, every run CAPTURED_AND_REVIEWED. E1 cost about $0.9 of the $3 cap (pod 16:27–17:20). Runs: `runs\e1_a1_brake_*` (fetched over SFTP, SHA-256 verified against the receipts).
- **Watchdogs.** The detached laptop watchdogs started by the pod helper do not survive their launching command (none running at 17:25; CD's also absent — told the coordinator). An in-pod self-delete guard with the pod's own key was refused by the permission classifier and is not used. E pods now get a session-tracked background watchdog (deadline 3 h) and are deleted by hand when their list finishes.
- **E2 running since 17:25 EST** on three RTX 4090 pods, packet `packet_e_v02`, one share (64 jobs incl. A1 admission and crash controls) each:
  - claude-v13e-01 `t6uh20ixg2ii1b` (E1 pod, reused; session watchdog to 20:23 EST);
  - claude-v13e-02 `455rs4aeq4z3mk`, created 17:37 (watchdog 20:40);
  - claude-v13e-03 `8b3x68wmppdkm2`, created 17:52 (watchdog 20:52; its SSH endpoint was completed by hand after the acquisition loop was stopped at 17:55, launched 18:00).
  Throughput about 36–47 jobs per pod-hour; controls bit-identical so far. **Pod 01 finished its share at 18:30 (64/64, no failure).**
- **packet_e_v03 smoke PASSED on pod 01 (18:50 EST; review M4 closed)**, `out\V03S_CHECK_v01.txt` (status fields only): the packet update verified all 1,936 bound files and passed the CPU self-check; A1 controls bit-identical on the D1-based packet; E_F0_IMM and E_N_IMM ran B's B1 tracker online (method tracker IMM, `E_PBAR_IMM_v01.json`; perception stage skipped by design) and E_F0 / E_PS ran the D1 pilot cases; all CAPTURED_AND_REVIEWED, E records pass, no policy failure.
- **Pod IMM replay (cross-platform A10 E0 check)**, `out\IMM_POD_REPLAY_v01.json`, `tests\test_imm_pod_replay_v01.py`: B's offline B1 on the laptop, fed the detections logged on the pod, reproduces the pod's online IMM tracks and planner actors within 5.7e-14 m (one unit in the last place at ~250 m; 69 detector updates, 340 decisions, both IMM runs), inside A10's 1e-12. The same-platform replay is bit-identical (`tests\out\IMM_REPLAY_*`). B's tracker files in the packet equal `work\shared\trackers\` as of 18:55, and equal the hashes session B sent at 19:30 (no change since its 15:44 fix D-B4-3, none planned before FREEZE_B); `E_PBAR_IMM_v01.json`'s source equals B's final `PBAR_B1_v01.json`. **packet_e_v03 stands as the E3/E3b packet**: checked at 20:45 EST against `work\locks\FREEZE_B.json` (written 20:38, SHA-256 `1fc9bb7c…`): all five tracker files in `trackers_b\` and the source of `E_PBAR_IMM_v01.json` equal B's frozen files.
- Pods 01 and 02 terminated 19:29 / 19:30 EST; pod 03 finished share 3 at 19:37 and was deleted at about 19:44 after API timeouts (its 19:38:59 terminate row was premature; correction row logged at 19:46; helper now logs only confirmed deletes). **No E pod is running.** E pod time so far ≈ 6.8 pod-h ≈ $6.0 (E1 ≈ $0.9).
- **E2 DONE (19:37 EST)**: 180/180 study runs CAPTURED_AND_REVIEWED and valid; every A1 admission and crash control bit-identical on all three pods. All 180 archives downloaded over S3 and verified against their receipts (`runs\e2_*`). Outcomes: `out\OUTCOMES_E2_v01.json` (first program), `out\E2_RECOUNT_OUTCOMES_v01.json` + `out\E2_RECOUNT_CALIB_v01.json` (second program): **identical** (contact and validity of all 180 runs; shares; levels).
  - F0 contact share on the 30 tuning cases: g = 0: 12/30; 0.25: 11/30; 1: 8/30; 4: 5/30; 16: 2/30; 64: 0/30.
  - **g_lo = 4** (share 0.167, nearest 0.20), **g_hi = 16** (0.067, nearest 0.05); not low-power.
  - Matched settings (`out\E2_MATCHED_v01.json`, design data): lo (F0 caution 14.10 %): N 3.350, CK3 2.661, TG 1.059, F0_IMM 11.885, N_IMM 10.593, PS triple (125.9, 105.9, 0.447); hi (22.30 %): N 13.335, CK3 8.414, TG 2.985, F0_IMM 53.09, N_IMM 47.32, PS the same triple (the zero-wrong-go triple of design caution 11.88 % is the H4 choice at both levels). The second program (Sonnet, `recount\e_recount_v01.py matched`, from the amendment text with the shared scoring library) gives **identical** grid indices, g values, PS triple and cautions (`out\E2_RECOUNT_MATCHED_v01.json`).
- **`work\locks\LOCK_A10_2b.txt` written 20:33 EST** (SHA-256 `81d3a77ada225718987d745e7ee2faaa4ef49c3c5e50b7a2ab81ade76cd5e867`): matched-settings file `out\E2_MATCHED_v01.json` (SHA-256 `dee03e7d…`), its inputs and code hashes, and the settings above. The E3/E3b job builder refuses any other matched-settings file.
- Note for the text: E-H3 compares N_IMM against F0_IMM, each matched to F0's open-loop caution; on the old runs the IMM pair needs much larger scales (F0_IMM 11.9 / 53.1, N_IMM 10.6 / 47.3) than CANMOT's F0 (4 / 16) for the same caution, because the IMM's covariances are smaller (P̄_IMM vehicle position variance about a third of the CANMOT P̄). Each pod is terminated as soon as its share is finished and its archives are verified (author's approval relayed by the coordinator, 17:40).
- **packet_e_v03** (for the IMM smoke, E3 and E3b) built at 17:45 on session CD's final `packet_d1_v13` (tar 90647c83…, folder verified against its manifest): tar SHA-256 `f3eb32c9546b21e7b3d28451b3bba4609726d6fd8341031c93bf19f7b7a20c74`, protocol `1a832864…` (the main protocol plus D1's cases), 34 bound files; adds CD's scene-class line to `probe_e_v01.py`, `E_PBAR_IMM_v01.json` (= B's `PBAR_B1_v01.json`, which equals the P̄ in B's B1 arrays) and B's tracker files as of 17:30 (to be compared with `FREEZE_B`; rebuilt and re-smoked if they differ). Smoke list `JOBS_V03S_claude-v13e-01_v01.json` (A1 admission, E_F0_IMM and E_N_IMM on c1109_tune_0000, E_F0 and E_PS on D1 pilot cases; one attempt each) runs on a pod after its E2 share.
- E cap $100. CD has six RTX 4090 pods running since 14:23–14:37 EST (5.47 USD/h); RunPod balance 180.05 at 15:40 EST.
- **Volume budget (coordinator, 19 Nov 15:15):** E at most 40 GB under `/workspace/claude_v13_e_v01/`. E's archives keep no sweeps (about 7.5 MB each), so all of E (about 1,400 runs incl. controls) is about 11 GB there; usage is checked by S3 listing before each stage. Copy path: the worker writes the archive to the volume only after a SHA-256-verified copy and its receipt; `tools\fetch_e_v01.py` downloads it, verifies it against the receipt again, keeps only the logs the analyses read (about 7–8 MB per run, about 11 GB in all) and refuses if fewer than 65 GB would stay free on C: (227 GB free at 15:50).

## Waiting on
- Build review (running).
- B: P̄_IMM (`B_retrack\out\pbar\PBAR_B1_v01.json`, "within the hour" at 15:25), the IMM pair's arrays on the 35 old runs (asked in the notes), frozen library (`FREEZE_B.json`).
- CD: final D1 packet (review passed with fixes) for `packet_e_v02`.
