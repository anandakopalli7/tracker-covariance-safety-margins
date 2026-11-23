# Brief for the fourth independent recount: the scoring of the reaction-and-stop estimate

Written 18 Nov 2026 (evening) by the revision session. The re-check of the claim audit (`notes\CLAIM_AUDIT_v11_v02_delta.md`, item N2) found that the scoring behind Tables III and IV of the manuscript (the "estimate": plans judged against the recording until their stop ends) has a second program only for its points at one setting. The clearances themselves have two programs (`recount2`, identical for every decision–row pair). This brief asks for an independent second program for the scoring: every setting, every population, the intervals, and the two variants.

## Rules
- Work only in `ARS_TRIAL\revision_v11\recount4\`. Write nothing anywhere else. Everything under `<library folder>` (called `P`) is read-only.
- Never open anything named `<excluded folder 1>` or `<excluded folder 2>`, nor `<user folder>`. No network use.
- Python: `python -B -X utf8 <script>`; scripts insert their own folder in `sys.path`; write scripts with the Write tool. Run anything likely to exceed two minutes in the background and wait for it.
- **Independence.** Do not open `revision_v11\analysis\*.py`, `revision_v11\analysis\out\*.json`, anything under `revision_v11\draft\` or `revision_v11\package_v11\`, or `P\11_ojits\A6R\code\`, until your own results file is written and its SHA-256 recorded. You may read and import the second-program lineage: `revision_v11\recount\rc_lib_v01.py`, `revision_v11\recount3\r3_lib_v01.py`, `revision_v11\recount2\` and `P\11_ojits\review\optionA_recount_v01\optA2_lib_v02.py`.
- Scoring definitions, inputs and the bootstrap of record are those of `revision_v11\recount\RECOUNT_BRIEF_v01.md` (sections "Inputs" and "Scoring definitions"). Read that file first.

## Input beyond the first brief
`revision_v11\recount2\out\<run>.npz` (35 evaluation runs): for each of nine settings `t0p50_a6p0`, `t0p75_a6p0`, `t1p00_a6p0`, `t1p25_a6p0`, `t1p50_a6p0`, `t1p80_a6p0`, `t0p75_a4p0`, `t0p75_a5p0`, `t0p75_a7p6` (τ in s, stop deceleration in m/s²): `clearX_<setting>` (decision × 17 rows: the clearance when the row is followed for τ and the stop is then followed until it ends; where the recording ends first, the minimum over the frames that exist), `clear61_<setting>` (the same clearance read on the 3 s window only), `late_<setting>` (the stop ends after the 3 s window), `cens_<setting>` (the recording ends before the stop does).

## Definitions
- **The estimate** (`est`): reaction-and-stop scoring in which a decision–row pair is unsafe when `clearX` ≤ 0 (NaN counts as unsafe). Only the wrong-go flag changes: caution keeps the 3 s commitment's definition (truly safe rows and the first truly safe row from `clear` > 0).
- **Censored pairs unsafe** (`cens`): as the estimate, and every pair with `cens` true that the estimate judges safe counts as unsafe.
- **Signed caution** (`est_signed`, τ = 0.75 s, 6 m/s² only): the estimate's wrong go, with caution averaged over every evaluated decision at its signed difference (definition in the first brief).
- **3 s window only** (`asscored`, τ = 0.75 s, 6 m/s² only, for reference): unsafe when `clear61` ≤ 0.
- Perfect oracle O of a scoring: per decision the first row in cost order that the scoring judges safe; the fallback row if none. den₀ = D(O); RR₀(A) = D(A)/den₀.
- denE = D(E) with E the 3 s oracle's critical scales `cE` scored under the scoring; R = denE/201 in percentage points.
- **Relative to 3 s**: denE under the scoring divided by denE under the 3 s commitment, and likewise den₀ over den₀ of the 3 s commitment, each computed per resample (numerator and denominator from the same resample) for the interval.
- Decision-equivalents use each resample's own number of decisions.
- Populations: all, ego moving, phases 0, 1, 2, and phase-weighted, as in the first brief.

## What to compute (points and 95% percentile intervals of the draw of record)
1. For `est` at all nine settings, and `cens` at the six settings with 6 m/s², for every population: n; den₀ (sum, percentage points, decision-equivalents); denE (same forms); denE relative to 3 s and den₀ relative to 3 s (population "all"; other populations if cheap); the share of resamples with den₀ ≤ 0 and with denE ≤ 0; and for each source N, NA, AM (`cA1`), CK3 and Q: D (sum, percentage points, decision-equivalents with interval), RR₀ and D/denE; RR₀ of E.
2. The same for `est_signed` and `asscored` at τ = 0.75 s, 6 m/s².
3. Pair counts over evaluated decisions per setting: pairs; pairs unsafe on the 3 s window; pairs unsafe under the estimate; pairs with `late` true that are safe on the 3 s window; how many of those are unsafe under the estimate; pairs with `cens` true that are safe on the 3 s window, and how many of those are safe under the estimate; decisions without any row the estimate judges safe.

## Output
1. `RECOUNT4_RESULTS_v01.json` (one entry per number) and the scripts that made it; record its SHA-256 and time in `RECOUNT4_REPORT_v01.md` before the next step.
2. Then open `revision_v11\analysis\out\REV_E2_EXTENDED_TRUTH_v01.json` (scorings `est_*`, `cens_*`, `est_signed_*`, `asscored_*`; ignore `ii_*` and `est_gap2_*`) and compare every shared number. Write `RECOUNT4_COMPARE_v01.md` and `RECOUNT4_COMPARE_v01.json`: per scoring the count of numbers compared and the count differing by more than 1e-9, every difference with both values and its cause if you can find it, and which numeric entries of the first program's file you did not compare and why. Keep apart the numbers on this brief's list and any you add after opening the first program's file.
3. `RECOUNT4_REPORT_v01.md`: what was computed and how, and anything in this brief that was ambiguous and how you resolved it.

Do not tune your program to match: an earlier recount of this kind found a real error in the first program. Your final message: numbers compared, numbers differing, each difference, and the ambiguities.
