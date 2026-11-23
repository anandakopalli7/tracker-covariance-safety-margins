# Text for AMENDMENT_12 §3a: DR replication and dose-response on the new lead-braking runs, v01

Drafted by session F (Claude Opus 5.5), 22 Nov 2026, about 00:45 EST by this laptop's clock, for the coordinator to merge verbatim into
`revision_v13\AMENDMENT_12_v13.md` §3a. Nothing below is computed on a new run before LOCK_A12a.

---

### 3a. DR replication and dose-response (session F)

**3a.1 Runs.** The new lead-braking runs of §2 (session CD), in ascending run id. Their number n is fixed by §2. Each run's protocol
case id is its seed id. Logs and CV0 arrays of record as CD stores them for C (`CD_capture\runs\`, `CD_capture\arrays\CV0\`).
The 120 tuning runs of record give F0 (A10 §2.1), as in A11 §6c.

**3a.2 What is unchanged from A11 §6c (v04, locked by LOCK_A11c).**
- The tracker: CV0 through the frozen library, `punish_num = 3`.
- The one mask law with its gap row.
- The decision-frame mapping, the frozen array builder, the scoring library, the gridless frontier on 201 levels and the 3 s commitment.
- The amplitude-matched ranking oracle E5_DR and its permuted twin, including u_i's divisor n_r (A11 §6c.5).
- δ = 0.05, A10 §2.6's calibration, and the identity checks (i) and (ii).
- The code is FREEZE_DR's, unchanged. New code (the dose-response and the decomposition) is frozen in `work\locks\FREEZE_DR_A12.json`
  before LOCK_A12a.

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
  the draw order, L ∈ {1, 2, 3} and the gap row are unchanged, so masks differ across p only through u < p.
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
