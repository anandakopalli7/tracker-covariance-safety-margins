# Brief for the third independent recount: the four analyses that so far have one program

Written 18 Nov 2026 (evening) by the revision session. The claim audit of the v11 manuscript (`notes\CLAIM_AUDIT_v11_v01.md`, row 22) found that four supplement tables behind numbers of the main text were produced by one program only: Table S12b, the subsampling columns of Table S17, Table S24b and Table S25 (with the benign-run check). This brief asks for an independent second program for them.

## Rules
- Work only in `ARS_TRIAL\revision_v11\recount3\`. Write nothing anywhere else. Everything under `<library folder>` is read-only.
- Never open anything named `<excluded folder 1>` or `<excluded folder 2>`, nor `<user folder>`.
- No network use. No cloud. Python: `python -B -X utf8 <script>`; scripts insert their own folder in `sys.path`. Run anything likely to exceed two minutes in the background and wait for it.
- **Independence.** Do not open `revision_v11\analysis\*.py`, `revision_v11\analysis\out\*.json` or anything under `revision_v11\draft\` until your own results file is written. The two array folders named below under `analysis\out\` are inputs and may be read from the start.
- You may read and import the second-program lineage: `revision_v11\recount\rc_lib_v01.py` (and the other `rc_*.py` there), `revision_v11\recount2\`, and `P\11_ojits\review\optionA_recount_v01\optA2_lib_v02.py`. Forbidden: `P\11_ojits\A6R\code\`.
- Scoring definitions, the inputs and the bootstrap of record are those of `revision_v11\recount\RECOUNT_BRIEF_v01.md` (sections "Inputs" and "Scoring definitions"). Read that file first. `P` is the project root named there.

## Inputs beyond those of the first brief
- `revision_v11\recount2\out\<run>.npz`: the second program's own clearances with plans judged until their stop ends (it reproduced the first program's bit for bit). Inspect the keys; use the τ = 0.75 s, 6 m/s² setting.
- `revision_v11\analysis\out\ck\<run>.npz`: critical margin scales of the braking prediction at 1–7 m/s² (`cCK1` … `cCK7`, decision × 17 rows) for the 35 evaluation runs, and at 3 m/s² for the 20 benign-driving tuning runs. The extraction itself is not recounted here; check instead that `cCK3` equals the stored `cCK3` of `P\11_ojits\A4\fit\extract\<run>.npz` bit for bit on the 35 evaluation runs, and report the result.

## What to compute

### 1. Table S12b: partial oracles over 50 draws (3 s commitment, step frontier, points)
For draw i = 0 … 49: `u = numpy.random.default_rng(20261200 + i).random(9307)`, one uniform per stored decision of the 35 evaluation runs, runs in sorted-name order, each run's decisions in stored order (9,307 stored decisions in all, evaluated or not). The partial oracle with share p ∈ {0.25, 0.50, 0.75} takes the oracle's critical scales (`cE`) on the decisions with u < p and the class average's (`cF0`) elsewhere. It is an arm other than F0 and E (F0's zero-margin point is prepended). Report RR for: all, ego moving, lead braking (phase 1), lead stopped (phase 2), phase-weighted (Σ_p (n_p/n)·D_p over Σ_p (n_p/n)·denE_p, phases 0–2). For each cell: mean, minimum and maximum over the 50 draws.

### 2. Table S17: subsampling without replacement
`rng = numpy.random.default_rng(20261124)`; for m in (15, 20, 25), in that order and on that one stream: for b in range(5000) the subsample is `rng.permutation(35)[:m]` (run indices in sorted-name order, each run once). Statistics, 3 s commitment, all evaluated decisions, everything recomputed on the subsample: R (pp), RR(N), RR(NA), RR(AM), RR(CK3), RR(Q), RR₀(CK3), RR(NA) − RR(N). With θ the full-sample value and θ* a subsample value: root = √m·(θ* − θ); (ql, qh) = the 2.5 and 97.5 percentiles of the finite roots (NumPy default interpolation); interval with the finite-population factor f = √(1 − m/35): [θ − qh/(f·√35), θ − ql/(f·√35)]. Report the interval for each statistic and m.

### 3. Table S24b: 2 m standstill gap with plans judged until their stop ends (τ = 0.75 s, 6 m/s²)
- Wrong go: the selected row's clearance judged until the stop ends is ≤ 2 m (NaN counts as unsafe).
- Caution: as of record, but a row is "truly safe" when its 3 s-commitment clearance (`clear`) is > 2 m.
- Perfect oracle O: per decision the first row in cost order whose clearance judged until the stop ends is > 2 m; the fallback row if none.
- Report for all / ego moving / phase-weighted: den₀ in percentage points and in decision-equivalents with the 95% interval of record; RR₀ of E, N, NA, CK3 and AM with intervals of record.
- Counts over evaluated decisions: decisions without any row whose clearance judged until the stop ends is > 2 m; decision–row pairs unsafe at 2 m on the 3 s window's reaction-and-stop clearance of record (the pack cache) and when judged until the stop ends.

### 4. Table S25 and the benign-run check
- For a0 = 1 … 7 (arm = `cCK<a0>`), 3 s commitment, step frontier: RR with the 95% interval of record and D in decision-equivalents for all, ego moving, phase 0, phase 1, phase 2 and phase-weighted; the zero-margin point (caution %, wrong go % at g = 0, all evaluated decisions) for each a0 and for F0.
- Benign-driving tuning runs (the 20 runs with `meta.family == 'benign'` in `gateR_rt_v01`; `cCK3` from the `ck` folder, `cF0` from `gateR_rt_v01`): evaluated decisions in all; the number of evaluated decisions whose selected row differs between the braking prediction and the class average at g = 0 and at g = 1; wrong-go decisions at zero margin under each.

## Output
1. `RECOUNT3_RESULTS_v01.json` (one entry per number) and the scripts that made it.
2. Only then open `revision_v11\analysis\out\REV_G_PARTIAL_DRAWS_v01.json`, `REV_D_BOOTSTRAP_v01.json` (its `D3_sensitivities.m_out_of_n`), `REV_E3_EXTENDED_GAP2_v01.json` and `REV_F2_BRAKING_PRIOR_v01.json`, compare every shared number and write `RECOUNT3_COMPARE_v01.md`: per item the count of numbers compared and the count differing by more than 1e-9, and every difference with both values and, if you can find it, its cause. Do not change the first program's files.
3. `RECOUNT3_REPORT_v01.md`: what was computed, how, the identity check of `cCK3`, and anything in this brief that turned out ambiguous and how you resolved it.

Your final message should give, per item: numbers compared, numbers differing, and each difference.
