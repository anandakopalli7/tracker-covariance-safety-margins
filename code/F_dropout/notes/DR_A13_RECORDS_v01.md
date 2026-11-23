# AMENDMENT_13 §3 (N_DR against a fixed dropout-flag margin): records before LOCK_A13b

Session F (Claude Opus 5.5), 22 Nov 2026.

## R1. Design (frozen in FREEZE_DR_A13, 6155b023…, about 07:30 EST)

- **Text:** `A13_3_DRFLAG_v01.md`, with the coordinator's changes of 07:12: an amendment label with Holm alongside E6 (m = 2), a plain
  95% percentile interval, and the failure wording.
- **Arm:** the two-population flag (k_in on in-dropout decisions, k_re on re-acquisition decisions, 1 on steady decisions), fitted on
  A11's 105 runs.
- **First program:** `code\dr_flag_v01.py`.

## R2. Coast-count refinement not adopted

- **What the coordinator asked:** at 07:16 and again at 07:25, a coast-count arm (k_1, k_2, k_3 by consecutive masked frame, k_re, a
  pooled fallback below 50 rows, named F0_coast).
- **Why it is not in the design:** both messages reached F only after the freeze and the code test (about 07:35). By the
  coordinator's own rules (07:16: keep the two-population flag if already frozen; 07:25: change no choice after seeing the code test),
  the frozen two-population flag stands.

## R3. Pre-lock code test: design data, no choice changed after it

- **Set:** the 35 OLD test runs (A11's pre-lock test arrays, `out\testold\DR\`, p = 0.10 masks). k was fitted on, and the test scored
  on, these same runs. No A11 run and no new run was used.
- **Values** (`out_a13\TESTOLD_DRF_RESULTS_v01.json`):
  - M_in 0.2268, M_re 1.9603, M_st 2.1219 (rows 19,322 / 17,255 / 84,200);
  - k_in 0.1069, k_re 0.9239;
  - RR_N 0.0116, RR_flag 0.0173;
  - Δ −0.0058, 95% [−0.0135, 0.0008];
  - status "failed (amendment)".
- **Run:** 56 s on the laptop, BelowNormal.
- **No choice** in the text or the code was changed after these values were seen.

## R4. Design change to the coast count (v02), the coordinator's decision

- **The decision:** made by the coordinator on the domain seat's report, before any value on A11's or the new runs. It was taken
  after FREEZE_DR_A13. The coordinator had not seen R3's old-run values, and they did not inform it.
- **Primary arm F0_coast:**
  - k_1, k_2, k_3 by the consecutive-masked-frame count of the decision's frame;
  - k_re for re-acquisition, 1 for steady;
  - medians relative to steady, fitted on A11's 105 runs;
  - a coast-count population with fewer than 50 rows falls back to the pooled k_in.
- **Secondary:** v01's two-population flag stays as a descriptive arm (F0_flag2), not in Holm.
- **Files:** text `A13_3_DRFLAG_v02.md`, code `code\dr_flag_v02.py`, export `code\dr_export_v05.py`.

## R5. v02 pre-lock code test on the 35 old runs (design data; no choice changed after it)

- **Values** (`out_a13\TESTOLD_DRF_RESULTS_v02.json`, 87 s):
  - M_1 0.4593, M_2 0.2260, M_3 0.1373, M_in 0.2268, M_re 1.9603, M_st 2.1219 (rows 9,352 / 6,305 / 3,665 / 19,322 / 17,255 /
    84,200; no fallback);
  - k_1 0.2165, k_2 0.1065, k_3 0.0647, k_re 0.9239, k_in 0.1069;
  - RR_N 0.0116, RR_coast 0.0128;
  - Δ −0.0012, 95% [−0.0028, −0.00002], "failed (amendment)";
  - RR_flag2 0.0173 (equal to v01's RR_flag, as it must be).
- **Set:** these are the 35 old test runs only, not A11's 105 runs or the new runs.

## R6. Tie rule for the count p, added before the v02 freeze (found by the pre-lock agreement test)

- **What was found:** both programs' v02 code tests (35 old runs) agreed on every key except DRF.delta.p. That differed by exactly
  1/20,001 (counts 19,570 vs 19,571).
- **Cause:** 8 resamples have Δ\* = 0 exactly and 27 have |Δ\*| < 1e-12 (resamples where N and F0_coast give the same D). Round-off gave
  one of them opposite signs in the two programs.
- **Rule** (text v02 §3.4, both programs, before any freeze or real value): p_F = (1 + #{Δ\* ≤ 1e-12, NaN counted}) / 20,001. Ties
  count against the test. The interval and the pass rule (Δ's lower end > 0) are unchanged.
- **Records:** the first code-test outputs are kept as `out_a13\superseded\*_pretie.json`. The rerun of the first program gives 19,582
  resamples ≤ 1e-12 or NaN, of which 27 are ties (|Δ\*| ≤ 1e-12); the other values are unchanged.
