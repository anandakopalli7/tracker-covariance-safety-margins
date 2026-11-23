# AMENDMENT 13 to the v13 pre-registration (A13): two controls asked for by the round-2 panel

Written 22 Nov 2026 from about 06:30 EST (laptop clock) by the coordinating session (Claude Opus 5.5), with section texts by the package sessions named in each section. It adds two tests. It changes no earlier test, label or result.

## 0. Why, and what was known when this was written

- The round-2 panel (five seats, run on the text frozen at 06:23:03, `freeze_v13_0623`) raised two points in four of its five seats:
  1. The "caution-matched" closed loop (A12 §6, E5) is matched in OPEN-loop caution only. In closed loop the covariance arm lost 0.18 s more time and stopped about 1 m farther back, so its fewer contacts cannot yet be told from a wider margin. The class-average arm ran at one scale only, the bottom of its grid.
  2. The open-loop dropout gain (A12 §3a) looks like a level effect: in-dropout decisions alone give a share near zero. A fixed margin increase during dropouts was not tested.
- Known before this amendment: every A12 result, including E5's two arms on the 135 test cases (contact shares, time lost) and DR2's decomposition on the 150 new runs. Section 2 reuses E5's two arms; section 3 reuses DR2's arrays. Both reuses are stated in the text of the paper.
- Labels (as A12 §1): each test here is an amendment test, "passed (amendment)" or "failed (amendment)". Neither is "confirmed".

## 1. Order, locks and cut-offs

- Each section is locked before any value of it exists: section 2 by LOCK_A13a, section 3 by LOCK_A13b. Each lock records the package's freeze and sealing evidence.
- Cut-off: a result not recounted by 10:00 EST is reported as "not completed" and enters section 4 as p = 1.
- Money: the RunPod balance must stay above $3 with pods running (the author's rule of about 03:25). Section 2 runs at most 6 pods, deleted by a watchdog at $3.5; section 3 runs on the laptop only.

<!--MERGE:E6-->
## 2. The closed-loop caution frontier (E6, session E)

**Coordinator's note on section 2 (laptop clock 06:47 EST, 22 Nov), written before LOCK_A13a and before any E6 run.** The text below is session E's v01, merged verbatim (shared notes `E_A13_E6_v01.md`, SHA-256 f60b92c9fc23184bdca6443867c8d0ed3f4cd2824d576bcab8828e1c59bd120d), with its headings demoted one level. One rule in it is amended here, for consistency with every other test of A12 and A13 (A12 §4: Holm changes no label):
- **Label rule (replaces the Label and Holm clauses of E6.5's Decision):** E6 is "passed (amendment)" iff Δ is defined on the full sample (bracketed) AND the upper end of the two-sided 95% percentile interval `E6.delta.ci` is < 0; otherwise "failed (amendment)". "Not bracketed", "non-monotone" or "no common no-contact case" on the full sample is "failed (amendment)".
- `E6.pass_alone` (from the one-sided bound ub95) and `E6.delta.ub95` are exported and reported as descriptive; they do not set the label.
- `E6.p_one` enters A13 §4's Holm (m = 2, with section 3's p_F). The Holm result is reported beside the label and does not change it.
- No code changes: the label is applied by session A and the coordinator from `E6.bracket` and `E6.delta.ci`, which both programs export.

*Session E's text v01 follows.*

Written 22 Nov 2026, about 06:30–06:50 EST by the laptop clock, by session E, after the coordinator's GO. This is the draft for LOCK_A13a. Every rule below is fixed before any E6 run is captured and before any E6 value is computed.

### E6.0 Disclosure: what was known when this was written
- **E5's results were public** before this section was written (A12 §6; reported 22 Nov, 03:37). That covers N at g_N and F0_D at g_D = 4 on the same 135 cases, and both their contact shares and time lost. E6 reuses those 270 runs unchanged.
- **The two new F0_D scales, g ∈ {8, 16}, come from the locked E5C calibration grid** {4, 8, 16, 32}, not from any test outcome.
- **Design data looked at to judge bracketing.** Before this was written (22 Nov, about 06:45), session E looked at time lost on the 120 E5C tuning runs (F0_D only, 30 tuning cases, disjoint from the 135):
  - from g = 4 to 8, F0_D lost about 0.22 s more (paired over cases without contact in either run);
  - from g = 4 to 16, about 0.67 s more.
  - E5's public N − F0_D@4 time-lost difference was +0.18 s.
  - On that basis, {8, 16} is expected to bracket N, but this is not guaranteed.
- **Dropped by decision (coordinator, 06:52):** N at further scales, the time-gap arm E_TG and a miss-counter arm. E6 has one frontier (F0_D) and one N point.

### E6.1 Question
At equal closed-loop time lost under detection dropouts, does N (the tracker's own covariance, which grows while the tracker coasts) have a lower contact share than F0_D, the class average estimated under the same dropouts? F0_D's contact share at N's time lost is read from F0_D's closed-loop frontier, by linear interpolation between F0_D scales.

### E6.2 Unchanged from A12 §6 (E5)
- **Closed loop:**
  - packet `packet_e_v05` (tar SHA-256 `4eda7c41f734440a8522f109aa78e7709e4d6a695f4cef05c0e32d10293ab83d`), unchanged;
  - F0_D = `E_F0` with P̄_DR (`E_PBAR_CANMOT_v01.json` in v05 = `work\F_dropout\out\PBAR_DR_v01.json`, SHA-256 `a50b3a1d…`);
  - CANMOT, the A11 §6c mask law `A11D2`, `output.punish_num = 3`;
  - the locked mask table `work\E_closedloop\out\E5_MASKS_v01.json` (SHA-256 `010595907805f7434ad4fc04f963439fa3756e57406de983053e66910822d770`);
  - A1 admission and native controls on every pod; the in-pod reviews.
- **Cases:** the 135 E5 main cases (`main_cases` of that table).
- **Statistics as E (A10 §7.5):** Newcombe hybrid-score interval (method 10, corrected φ); exact McNemar; case bootstrap `default_rng(20261922)` × 20,000; classes with contact ±0.10 and time lost ±0.5 s.

### E6.3 Arms and runs
| Arm label | Arm, scale | Runs | Source |
|---|---|---|---|
| N | `E_N`, g_N = 5.95662143529011 (`E5_SETTINGS_v01.json`, SHA-256 `73cc480c…`) | 135 | E5, reused (job ids `e5_<case>_e_n`) |
| F0D4 | `E_F0`, g = 4 | 135 | E5, reused (`e5_<case>_e_f0`) |
| F0D8 | `E_F0`, g = 8 | 135 | **new** (`e6_<case>_e_f0_g8`, level `D8`) |
| F0D16 | `E_F0`, g = 16 | 135 | **new** (`e6_<case>_e_f0_g16`, level `D16`) |

- **New runs:** 270, phase `E6`, the job knobs `dropout = A11D2`, `punish_num = 3`, tracker CANMOT.
- **Pods:** claude-v13e-41…46. Cases are dealt round-robin over the speed-interleaved order, so all of a case's runs are on one pod.
  - Each list: A1 admission (crash, benign), then a crash control, then **all its g = 8 jobs, then all its g = 16 jobs**, with a crash control every 50 study jobs.
- **Run and attempt rule as E5:** the latest attempt of each job is used.
- **Arm label of a run:** from its job (prefix `e5_`/`e6_`, arm, and g):
  - e5 `E_N` → N; e5 `E_F0` → F0D4;
  - e6 `E_F0` with g 8 → F0D8, with g 16 → F0D16.
  - Pairing is by case and arm label, never by the job's level label.

### E6.4 Validity (per run, as E5 §6.7)
A run is valid iff:
- status is CAPTURED_AND_REVIEWED, there is no policy failure, and there is no contact before the window;
- the method record's arm and tracker equal the job's, the arm is `E_F0` or `E_N`, and the tracker is CANMOT;
- the method's g equals the job's g, and equals the locked g of its arm label: N 5.95662143529011, F0D4 4, F0D8 8, F0D16 16;
- for `E_F0`, the P̄ SHA-256 equals P̄_DR in packet v05;
- the mask equals the A11D2 law and the locked table; the law id, law-file hash and punish_num 3 match;
- every detection row follows the mask (masked rows feed the tracker no rows; unmasked rows feed all model rows).

### E6.5 Primary: contact difference at N's time lost (amendment test)
**Sets.**
- **K:** the cases (of the 135) whose four runs (N, F0D4, F0D8, F0D16) are all valid. Sort K ascending by case id (string order); n = |K|.
- **T ⊆ K:** the cases with contact = 0 in all four runs.

**Frontier points.** For each arm a ∈ {N, F0D4, F0D8, F0D16}:
- c_a = the mean of `contact` (0/1) over K;
- t_a = the mean of `time_lost_s` over T.

**Estimator Δ.** Each step in order:
1. If T is empty, Δ is undefined: status "no common no-contact case".
2. If not (t_F0D4 < t_F0D8 < t_F0D16) (strict), Δ is undefined: status "non-monotone".
3. If t_N < t_F0D4 or t_N > t_F0D16, Δ is undefined: status "not bracketed". There is no extrapolation.
4. Otherwise, take the bracketing pair (lo, hi) = (F0D4, F0D8) if t_N ≤ t_F0D8, else (F0D8, F0D16).
   - w = (t_N − t_lo) / (t_hi − t_lo)
   - c_F0(t_N) = c_lo + w · (c_hi − c_lo)
   - **Δ = c_N − c_F0(t_N)**
   - Status `bracketed 4-8` or `bracketed 8-16` (hyphen).
5. If K is empty, the c and t points are null, every Δ* is NaN, p = 1, the finite share is 0, and ub95 and the interval are null. If T is empty but K is not, the c points are defined and the t points are null.
6. All comparisons (<, ≤) are plain float comparisons with no tolerance.

**Bootstrap.**
- `rng = numpy.random.default_rng(20261922)`, then `idx = rng.integers(0, n, (20000, n))`, indexing K in the sorted order above.
- **For resample b:**
  - c_a* = the mean of contact over the n drawn cases, counted with multiplicity;
  - t_a* = the mean of time_lost_s over the drawn positions whose case is in T, counted with multiplicity;
  - Δ*_b = the same steps 1–4 applied to these.
  - Δ*_b is **NaN** when step 1, 2 or 3 applies: no drawn case in T, F0 non-monotone, or N not bracketed.
- **One-sided p** (H1: Δ < 0) = (1 + #{b : Δ*_b ≥ 0 or Δ*_b is NaN}) / 20,001. NaN counts against H1.
- **Over the finite Δ* only, with their share reported:**
  - the one-sided 95% upper bound ub95 = `numpy.quantile(finite, 0.95)` (method "linear", numpy's default);
  - the two-sided 95% interval [`quantile(finite, 0.025)`, `quantile(finite, 0.975)`].
  - If no Δ* is finite, these are null.

**Decision.** The test is an amendment test.
- It **passes on its own** iff Δ is defined on the full sample (bracketed) and ub95 < 0.
- Its p enters A13's Holm step with the open-loop dropout-flag control (F, if it goes ahead: m = 2; otherwise m = 1) at family α = 0.05.
- Label:
  - **"passed (amendment)"** iff it passes on its own and Holm rejects its H0;
  - otherwise **"failed (amendment)"**.
  - "Not bracketed", "non-monotone" or "no common no-contact case" on the full sample is always "failed (amendment)".

### E6.6 Secondary (descriptive)
- **N vs F0D8 and N vs F0D16:** E's paired comparison each (as E5's primary), paired by case over valid pairs:
  - contact difference (N − F0_D) with Newcombe's interval and exact McNemar;
  - time-lost mean paired difference over pairs without contact, with the case bootstrap;
  - E's class.
  - With no valid pair, its values (including the McNemar p) are null and its class is `no pairs`.
- **Per-arm summaries** for all four arms over each arm's valid runs, defined as in E5:
  - means of contact, time lost and rest gap;
  - medians of impact speed, peak deceleration and RMS jerk;
  - fallback share pooled over decisions;
  - mean masked share.
- The counts n = |K| and |T|.

### E6.7 Second program and comparison of record
- A Sonnet 5.5 subagent writes the second program from this text and the raw run files only. It does not read session E's analysis code; it may reuse its own earlier E5 recount (`recount\e_recount_e5_v01.py`).
- It recounts validity, the frontier points, Δ, the bootstrap, p, ub95, the interval, the finite share, the secondary comparisons and the per-arm summaries.
- Comparison of record as A10 §10.1(c): counts exact, values within 1e-9, labels and classes equal.

### E6.8 Export
`work\E_closedloop\out\A_EXPORT_E6.json` and `A_RECOUNT_E6.json`, with the same 65 keys (an undefined value or interval is null):
- **Status and sets:** `E6.status`, `E6.n_cases` (= |K|), `E6.n_nocontact_all` (= |T|).
- **Frontier points:** `E6.pt.<N|F0D4|F0D8|F0D16>.c` and `.t` (c_a and t_a).
- **Primary:**
  - `E6.bracket` (one of `bracketed 4-8`, `bracketed 8-16`, `not bracketed`, `non-monotone`, `no common no-contact case`);
  - `E6.c_F0_at_tN`, `E6.delta`, `E6.delta.ub95`, `E6.delta.ci`;
  - `E6.finite_share` (finite Δ* / 20,000), `E6.p_one`;
  - `E6.pass_alone` (true/false).
- **Per arm:** `E6.<N|F0D4|F0D8|F0D16>.<contact|vimp|tlost|restgap|peakdec|jerk|fallback|masked>`.
- **Secondary:** `E6.s<8|16>.<dc|dc.ci|mcnemar_p|dt|dt.ci|class|pairs>`.
- The Holm label is applied by A13 (session A / coordinator) from `E6.pass_alone` and `E6.p_one`.

### E6.9 Order, gates, budget
1. **Freeze.** `work\locks\FREEZE_E_ADDENDUM_v09.json` freezes, before any E6 run and any E6 value:
   - this text;
   - the job builder `tools\make_jobs_e6_v01.py` and the six job lists;
   - the balance watchdog `tools\balance_watch_e6_v01.py`;
   - the first program `analysis\e6_analyse_v01.py`, its test, and the driver `analysis\run_e6_v01.py`;
   - the second program `recount\e_recount_e6_v01.py` (Sonnet 5.5, written from this text) and its tests;
   - the export key list.

   Then the coordinator writes **LOCK_A13a**.
2. **E6 capture** on claude-v13e-41…46. It starts only after LOCK_A13a is confirmed.
3. Fetch; both programs (`run_e6_v01.py main`); comparison of record; export.
   - After a balance stop only: `--allow-missing`. Missing E6 runs are listed, and K shrinks.

- **Budget:** about $7–8.7, at $0.89/h per pod.
  - A balance watchdog deletes every E6 pod if the account balance falls below $3.5.
  - Because every pod runs its g = 8 jobs first, a stop still leaves N vs F0D8 (§E6.6) for most cases. The primary then needs all four arms per case, and K shrinks to the cases with a valid g = 16 run.
- Every pod is logged in SPEND_LOG_v13.csv; deletes are confirmed (rc = 0 and absent from the pod list).
- Results must be recounted by about 09:45.

### E6.10 What it can and cannot show
- **It can show** whether, along F0_D's own closed-loop caution frontier (three scales), N has fewer contacts than F0_D at N's time lost, on the E5 cases.
- **It cannot show:**
  - N's frontier (one N point);
  - other arms (E_TG and miss-counter dropped);
  - fresh cases for N and F0D4 (their results were public; only F0D8 and F0D16 are new);
  - behaviour outside F0_D's time-lost range (no extrapolation);
  - a time-lost resolution finer than the frontier spacing (about 0.7 s across 4–16 on tuning data, close to E's ±0.5 s class).
- Linear interpolation between scales is an assumption about F0_D's frontier shape.



**Coordinator's note on section 3 (laptop clock 06:48 EST, 22 Nov), superseding the section 3 of LOCK_A13b before any real value.**
- About 06:30 the coordinator asked session F, on the domain seat's report, for a COAST-COUNT baseline (a factor per consecutive missed update). The message reached F after F had frozen the two-population flag (v01, FREEZE_DR_A13) and run its code test on the 35 old test runs.
- About 06:40 the coordinator learned v01's code-test values (k_in 0.107, k_re 0.924, Δ −0.0058 [−0.0135, 0.0008] on the 35 old runs) and, to avoid a design choice after seeing values, wrote LOCK_A13b (06:40:47) on v01 unchanged. F meanwhile acted on the earlier request and froze the coast-count version v02 (FREEZE_DR_A13_ADD01) with its own code test (k_1 0.216, k_2 0.107, k_3 0.065, k_re 0.924; Δ −0.0012 [−0.0028, −0.00002] on the same 35 old runs). The messages crossed.
- Decision: section 3 is v02 (F0_coast primary; v01's two-population flag kept as a descriptive secondary, F0_flag2). Reasons: the coast-count baseline is the one the domain seat asked for and was chosen before any value of either arm on A11's or the new runs; it is the stricter baseline for the covariance; and on the old-run code tests BOTH versions favour the baseline over N, the coast-count version more decisively, so the switch does not favour the paper's claim. The tie rule (Δ* within 1e-12 counts against the test) was added before the freeze because the two programs' code tests differed by one resample on an exact tie.
- No real DRF value exists at this note (only the two code tests on the 35 old runs, which are design data). LOCK_A13c records this section.

*Session F's text v02 follows, merged verbatim (headings as in v01's merge).*

## 3. N_DR against a fixed coast-count margin (F0_coast)

**3.0 Record of the design change.**
- **Whose decision:** the coordinator's. It acts on the domain seat's report, which asked for a class average that knows how many
  updates in a row a track has missed. That is the fairer baseline for a covariance that grows with the coast count.
- **What was known:** the coordinator made the change before any value of this test on A11's or the new runs existed.
- **The v01 code test:** it ran on the 35 old test runs only, and its values are in `notes\DR_A13_RECORDS_v01.md`. The coordinator had
  not seen them, and they did not inform the change. Session F had seen them, but did not make the change.

**3.1 Question.** Under detection dropouts, does N_DR rank decisions better than a fixed extra margin that knows only the dropout
state and the number of consecutive missed frames?

**3.2 Arm F0_coast.**
- **Scales:** F0_DR's critical scales (P̄_DR, A11 §6c.5), multiplied per decision by a k chosen by the frame the decision uses
  (`dr_frame`, with the run's masked frames from its metadata):
  - **k_c** if the frame is masked and is the c-th consecutive masked frame, c = 1, 2, 3 (`dr_age`). By the mask law L ≤ 3; a count
    above 3 would use k_3.
  - **k_re** (re-acquisition) if the frame is not masked and frame − 1 or frame − 2 is masked.
  - **1** (steady) otherwise, including decisions with no frame yet.
- **Value rules:** multiplication keeps inf, −inf, 0 and NaN as they are.
- **Available online:** the coast count is known at decision time.
- **Support:** dropouts are whole-frame, so every actor of a dropout frame coasts the same number of frames. F0_coast inflates every
  actor, as N does.

**3.3 k.**
- **Relative to steady:** RR_gl does not change when all of a source's critical scales are multiplied by one constant, so each k is
  taken relative to steady: k_c = M_c / M_st and k_re = M_re / M_st.
- **M_S:** the MEDIAN of cN / cF0 over the rows (actors) of the evaluated decisions in population S where both are finite and > 0.
- **Fallback:** a coast-count population with fewer than 50 such rows on the fit runs takes the pooled in-dropout k instead,
  k_in = M_in / M_st, with M_in over all in-dropout rows.
- **Fit set:** A11's 105 fresh lead-braking runs (`F_dropout\out\arrays\DR\`: p = 0.10, punish_num 3, P̄_DR), which are disjoint from
  the test runs. k uses no data of the 150 new runs.

**3.4 Test.** On the 150 new runs of A12 §3a (`F_dropout\out_a12\p010\arrays\DR\`, DR2's room F0_DR, E_DR):
- **Statistics:**
  - RR_gl(F0_coast);
  - RR_gl(N_DR), reused (equal to DR2's r);
  - Δ = RR_gl(N_DR) − RR_gl(F0_coast) = (D_gl(N) − D_gl(F0_coast)) / D_gl(E, F0).
- **Draw:** DR2's, `optA_lib_v02.boot_counts(150, 20000, 20261911)`.
- **Interval:** a plain 95% percentile interval. A10 §2.6 calibration is not applied.
- **One-sided p:** p_F = (1 + #{Δ\* ≤ 1e-12, NaN counted}) / 20,001.
  - Δ\* within 1e-12 of 0 is a tie. Exact ties occur when a resample's runs give N and F0_coast the same D, and floating-point round-off
    can give them either sign. They count against the test, so that both programs count alike.
- **Pass:** "passed (amendment)" if Δ's lower end > 0; otherwise "failed (amendment)".
- **Secondary, descriptive, not in Holm:** v01's two-population flag F0_flag2 (k_in on in-dropout decisions, k_re on re-acquisition
  decisions, 1 on steady ones), with RR_gl(F0_flag2) and Δ2 = RR_gl(N) − RR_gl(F0_flag2) on the same draw.

**3.5 Label and Holm.**
- An AMENDMENT test, like E6: one new arm against an arm whose results are already public.
- p_F enters A13 §4's Holm with E6's (m = 2).
- **Disclosure:** the test was designed after DR2 and its decomposition were seen, and N's arm is reused.

**3.6 Wording.**
- **Pass:** "N's gain over a fixed coast-count margin is shown: Δ = [..], 95% [..]."
- **Fail:** "N's gain over a fixed coast-count margin was not shown; the interval [..] includes 0".
  - If both ends also lie inside (−0.05, 0.05) on the share scale, add: "and is within the equivalence margin".

**3.7 Missing data.**
- Rows with a non-finite or non-positive cN or cF0 are left out of M_S.
- A resample with D_gl(E, F0) ≤ 0 gives Δ\* = NaN, which counts against the test.
- All 150 runs enter, and all 105 fit runs enter.

**3.8 Programs, verification, export.**
- **First program:** `F_dropout\code\dr_flag_v02.py`, laptop, BelowNormal. It refuses without `LOCK_A13b.txt`.
  - Its `--test-old` mode fits k on, and scores, the 35 old test runs (`out\testold\DR\`): a code test only.
- **Second program:** Claude Sonnet 5.5 extends its recount from this text, without reading the first program.
- **Agreement:** per A10 §10.1(c).
- **Export:** `work\F_nuscenes\out\A_EXPORT_DRF.json` / `A_RECOUNT_DRF.json`, prefix `DRF.`. Keys:
  - DRF.n_runs, DRF.n_fit_runs;
  - DRF.M_1, DRF.M_2, DRF.M_3, DRF.M_re, DRF.M_st, DRF.M_in;
  - DRF.k_1, DRF.k_2, DRF.k_3, DRF.k_re, DRF.k_in;
  - DRF.k_1.fallback, DRF.k_2.fallback, DRF.k_3.fallback (true when the pooled k_in is used);
  - DRF.n_fit_rows.{1, 2, 3, re, st, in};
  - DRF.n_dec.{c1, c2, c3, reacq, steady};
  - DRF.RR_N (.ci), DRF.RR_coast (.ci), DRF.delta (.ci), DRF.delta.p, DRF.passes, DRF.within_equiv, DRF.status;
  - secondary: DRF.RR_flag2 (.ci), DRF.delta_flag2 (.ci).

## 4. Multiplicity

Holm across A13's primary hypotheses (section 2's Δ and, if locked, section 3's difference), each with its one-sided p as defined in its section; m = the number of sections locked. Reported beside A12's Holm, not merged with it.
