# Recount report (independent second program), revision v11

Written 2026-11-18 17:20:26 by the second program. Code: `rc_lib_v01.py`, `rc_anchor_v01.py`, `rc_items_v01.py`, `rc_item4_v01.py`, `rc_double_v01.py`, `rc_report_v01.py` (this folder). All numbers below are in `RECOUNT_RESULTS_v01.json` (4232 numeric entries; per-item files listed in its `index`).

## 0. Independence
The code was written from `RECOUNT_BRIEF_v01.md` and `AMENDMENT_08_ARS_REVISION_v01.md`. It reads the stored arrays with numpy and imports nothing from the data project. `optA2_lib_v02.py` and `optA2_main_v02.py` (the project's own second-program lineage, allowed by the brief) were read for the definitions; nothing was imported from them. Nothing under `revision_v11\analysis\` or `11_ojits\A6R\code\` was opened before this report and the results file were written. One file outside the listed inputs was consulted: `11_ojits\review\optionA_recount_v01\OPTIONA_SECOND_REPORT_v02.txt` and `..._RESULTS_v02.json` (the earlier second program's outputs), for one value only, the reaction-and-stop den0 (see the anchor).

## 1. Anchor check (3 s commitment, all evaluated decisions, step frontier, 35 runs)

| quantity | published | recount | reproduces to the printed digits |
|---|---|---|---|
| evaluated decisions | 8,290 | 8290 | yes |
| phase decision counts | 678 / 755 / 6,857 | 678 / 755 / 6857 (phase 3: 0) | yes |
| room R (pp) | 5.5568 [4.4986, 6.6038] | 5.556776 [4.498589, 6.603840] | yes |
| RR(N) | 0.00122 [-0.00108, 0.00119] | 0.0012204 [-0.0010755, 0.0011933] | yes |
| RR(NA) | 0.0167 [0.0073, 0.0252] | 0.016665 [0.007295, 0.025186] | yes |
| RR(CK3) | 0.8315 [0.7528, 0.9033] | 0.831476 [0.752807, 0.903326] | yes |
| RR(AM) | 0.3758 [0.3156, 0.4254] | 0.375799 [0.315577, 0.425361] | yes |
| den0 (sum over 201 levels) | 1205.2352 | 1205.235223 | yes |
| reaction-and-stop tau 0.75 s, 6 m/s2: den0 (sum) | 141.0132 | 141.01326900 | NO |
| reaction-and-stop: RR0(CK3) | 0.9357 | 0.935672 | yes |

Result: 9 of 10 anchor values reproduce to the printed digits. The one that does not is the reaction-and-stop den0: the recount gives 141.01326900, which rounds to 141.0133, while the task statement prints 141.0132. The project's earlier second program records 141.01326899879373 (printed there as 141.0133), identical to the recount to every digit, so the printed 141.0132 is the same number truncated instead of rounded; it is a 1e-4 presentation difference and not a scoring difference. The run was continued.

Other checks made at the anchor: no NaN clearance inside the evaluated set (3 s: 0, cache: 0), so the "NaN = -1" rule is never used; the levels equal `numpy.linspace` bit for bit (True); no frontier is undefined at any level in the point or in any of the 20,000 resamples (0 resamples with an undefined level); stored decisions 9307; moving decisions 1863; of the truly safe rows, 2752 of 116028 are faster than the first truly safe row (negative caution terms exist).

## 2. Interpretations made (where the brief leaves a choice)
- Runs: the 35 names `p1b_fit_finite_0005` to `_0039`; each file's metadata was checked (family lead_braking, set fit). Desired speed: the stored per-decision `des`, checked equal to `meta.desired`.
- Wrong go under the reaction-and-stop scoring: the selected row's cache clearance is <= G, counted for every evaluated decision (the brief's wording). The earlier second-program library counts it only where some row is safe; the two differ by the same count for every arm and scale, so D, den and RR are unchanged.
- Caution axis: always the 3 s clearance (truly safe = `clear` > G), also when the wrong go is scored by reaction-and-stop. With G = 2 m both the wrong go and the truly safe rows use the 2 m requirement (Amendment R17).
- Signed caution (item 1): sum of the signed differences over the population's decisions that have a truly safe row, divided by their number; the wrong-go share is over all evaluated decisions of the population. Levels are built from the signed cautions. The oracle O has signed caution 0 and gets F0's zero-margin point; because F0's zero-margin signed caution is negative, the levels below 0 see only that prepended point, so den0 can be smaller than denE (it is in: moving, phase0, phase1, phase_weighted). Reported as computed.
- Undefined frontier (no point of the arm with caution <= level): kept as NaN and counted; it never occurred in any analysis here.
- Phase-weighted aggregate: sum over phases 0-2 of (n_p / n) D_p with n = n_0 + n_1 + n_2, recomputed in every resample, an empty phase contributing 0. RR = aggregated D / aggregated denE; RR0 = aggregated D / aggregated den0; R = aggregated denE / 201; decision-equivalents = aggregated den0 / 201 / 100 * n.
- Intervals: numpy percentiles (linear interpolation) at 2.5 and 97.5 over the resamples; ratios over the resamples whose own denominator is positive (denE for RR, den0 for RR0), the others counted as "left out". Decision-equivalent intervals scale each resample by its own n.
- Item 2: E stays the stored oracle margin source (`cE`); it is not re-derived for the 2 m requirement, so denE can be negative there. O is the first row whose scoring clearance is > 2 m, else the fallback.
- Item 3: k_stop is taken from the stored decisions (evaluated or not), as the brief says. The condition (k - k_stop) * 0.05 < T was evaluated in floating point and as the integer condition k - k_stop < 20 T; the two agree for every decision. Every run has a phase-2 decision, and no phase-0 or phase-1 decision lies after k_stop. In 5 runs the first stored phase-2 decision is not an evaluated one; the reading "first evaluated phase-2 decision" was also computed (points only) and gives the same populations.
- Item 4: n = all evaluated decisions (no evaluated decision has phase 3, so phases 0-2 are the whole population). Levels, F1 and F_O are the pooled single-scale ones. The 202^3 triples are not enumerated in the bootstrap: for each level the minimum pooled wrong-go count subject to "pooled caution <= level" is found from each phase's distinct (count, caution sum, safe count) triples (method in the header of `rc_item4_v01.py`), with enumeration as a fallback when a triple lies within rounding of a level (never needed). At the point and for the first three resamples every arm's frontier was also computed by full enumeration of the deduplicated triples: identical (largest difference 0). The diagonal triples (g, g, g) are the single-scale points; taking them from the single-scale curve or from the triple sums changed nothing in the point or in any of the 400 resamples. Intervals of ratios: resamples with a positive denominator.
- Item 5, coverage rule: shares are over the inner values with a positive denominator (all 1,000 in every outer sample). The two inequalities of the brief are evaluated in exact integer arithmetic. The same rule in floating point is printed beside it: at a = 0.05 the float (1 - 0.95)/2 is 0.025000000000000022, just above 25/1000, so an outer sample with exactly 25 inner values at or below the truth is covered under exact arithmetic and not covered under the float rule. Coverage at nominal 1.0 is 1 by the formula (a = 0 makes both inequalities always true).
- Item 5, calibrated interval: the smallest grid level whose coverage is >= 0.95 (covered count * 100 >= 95 * outer samples); the interval is numpy.percentile of the draw of record at 100 a/2 and 100 (1 - a/2).
- Item 5, stratified draw: groups in increasing alpha (1.642, 5.412, 7.55), the runs of a group in sorted-name order (as listed in the A4 JSON), one generator used for the three groups in turn. Long runs: the 30 runs with >= 100 evaluated decisions, in sorted-name order.
- Item 6: m = 1/sqrt(cN/cF0) on the rows of evaluated decisions where cN and cF0 are both finite and positive; "per family (all runs)" pools the fit and tuning files of a family (the per-set split is also given). The median is over rows. Track-age bands: [0, 0.5), [0.5, 1), [1, 2), [2, 4), [4, inf) s.
- Not computed (not in the brief's list, or no draw specified): the m-out-of-n subsampling of Amendment R9; R10 (extended truth); the smaller checks S13-S20; the convex-hull frontier.

## 3. Item 1 (R11): 3 s commitment with signed caution
Draw of record, 20000 resamples. Sums are over the 201 levels; R = denE / 201 in pp.

| population | n | R (pp) | denE | den0 | den0 (dec.-eq.) |
|---|---|---|---|---|---|
| all | 8290 | 4.8625 [4.0488, 5.6104] | 977.358 [813.806, 1127.694] | 1092.654 [909.710, 1252.426] | 450.65 [360.58, 531.36] |
| moving | 1863 | 6.3160 [4.8342, 7.4243] | 1269.512 [971.679, 1492.293] | 975.255 [684.331, 1197.136] | 90.39 [66.30, 108.90] |
| phase0 | 678 | 0.4102 [0.0509, 1.0654] | 82.448 [10.241, 214.146] | 77.729 [8.695, 204.344] | 2.62 [0.30, 6.69] |
| phase1 | 755 | 5.6361 [3.6810, 7.5692] | 1132.848 [739.878, 1521.418] | 383.444 [-15.581, 857.958] | 14.40 [-0.70, 27.37] |
| phase2 | 6857 | 0.7922 [0.6414, 0.9514] | 159.224 [128.924, 191.237] | 195.756 [153.489, 241.151] | 66.78 [49.89, 84.48] |
| phase_weighted | 8290 | 1.2021 [1.0290, 1.3520] | 241.616 [206.827, 271.742] | 203.197 [155.608, 249.500] | 83.81 [62.85, 104.37] |

RR (share of denE):

| population | N | NA | AM | CK3 | Q |
|---|---|---|---|---|---|
| all | -0.0002 [-0.0011, 0.0012] | 0.0157 [0.0075, 0.0258] | 0.3784 [0.3221, 0.4302] | 0.8166 [0.7351, 0.8908] | -0.0030 [-0.0073, 0.0010] |
| moving | -0.0031 [-0.0070, 0.0023] | 0.0197 [0.0046, 0.0355] | 0.3462 [0.2487, 0.4252] | 0.2993 [0.1270, 0.4321] | -0.0014 [-0.0135, 0.0042] |
| phase0 | -0.0000 [-0.0313, 0.0274] (2 left out) | -0.0000 [-0.0323, 0.0272] (2 left out) | -0.1270 [-0.4441, 0.1732] (2 left out) | -0.6261 [-4.5583, 0.1381] (2 left out) | 0.0018 [-0.1589, 0.0490] (2 left out) |
| phase1 | -0.0000 [-0.0118, 0.0102] | 0.0065 [-0.0265, 0.0456] | 0.0607 [-0.1556, 0.2371] | 0.3472 [0.0123, 0.5494] | -0.0161 [-0.0430, 0.0046] |
| phase2 | 0.0007 [-0.0047, 0.0044] | 0.0793 [0.0343, 0.1246] | 0.7027 [0.6300, 0.7651] | 0.9821 [0.9028, 1.0942] | -0.0146 [-0.0352, 0.0042] |
| phase_weighted | 0.0004 [-0.0056, 0.0051] | 0.0460 [0.0195, 0.0764] | 0.4054 [0.3098, 0.4871] | 0.6662 [0.5187, 0.7832] | -0.0148 [-0.0340, 0.0008] |

RR0 (share of den0):

| population | N | NA | AM | CK3 | Q |
|---|---|---|---|---|---|
| all | -0.0002 [-0.0010, 0.0011] | 0.0141 [0.0068, 0.0231] | 0.3384 [0.2854, 0.3902] | 0.7305 [0.6488, 0.8086] | -0.0027 [-0.0066, 0.0009] |
| moving | -0.0040 [-0.0090, 0.0031] | 0.0257 [0.0059, 0.0457] | 0.4507 [0.3200, 0.5640] | 0.3896 [0.1719, 0.5475] | -0.0018 [-0.0187, 0.0052] |
| phase0 | -0.0000 [-0.0342, 0.0311] (2 left out) | -0.0000 [-0.0347, 0.0311] (2 left out) | -0.1347 [-0.4790, 0.1825] (2 left out) | -0.6641 [-5.4176, 0.1417] (2 left out) | 0.0019 [-0.1685, 0.0513] (2 left out) |
| phase1 | -0.0000 [-0.0687, 0.0480] (598 left out) | 0.0193 [-0.1620, 0.1753] (598 left out) | 0.1793 [-0.7406, 1.2206] (598 left out) | 1.0259 [0.1761, 3.3365] (598 left out) | -0.0477 [-0.4282, 0.0111] (598 left out) |
| phase2 | 0.0006 [-0.0038, 0.0036] | 0.0645 [0.0280, 0.1044] | 0.5716 [0.4546, 0.6776] | 0.7989 [0.7170, 0.8802] | -0.0118 [-0.0292, 0.0033] |
| phase_weighted | 0.0005 [-0.0068, 0.0059] | 0.0547 [0.0235, 0.0903] | 0.4820 [0.3516, 0.6158] | 0.7921 [0.6439, 0.9099] | -0.0176 [-0.0428, 0.0010] |

Signed-caution axis: F0's zero-margin signed caution (= the first level) is all -0.972%, moving -8.700%, phase0 -0.728%, phase1 -17.541%, phase2 0.828%. Every evaluated decision has a truly safe row (the signed mean is over all of them).

## 4. Item 2 (R17): standstill gap 2 m
### (a) 3 s commitment
Unsafe pairs under the scoring: 43684; pairs not truly safe (3 s clearance <= 2 m): 43684; evaluated decisions with no safe row under the scoring: 633; with no truly safe row: 633.

| population | n | den0 (sum) | den0 (pp) | den0 (dec.-eq.) | denE (sum) | share of resamples with denE <= 0 |
|---|---|---|---|---|---|---|
| all | 8290 | 1483.969 [1270.148, 1690.376] | 7.3829 [6.3191, 8.4098] | 612.04 [499.95, 719.12] | -2273.703 [-4136.301, -798.110] | 0.9996 |
| moving | 1863 | 2632.904 [2036.273, 3190.214] | 13.0990 [10.1307, 15.8717] | 244.03 [190.71, 294.84] | 168.975 [-840.227, 1087.042] | 0.3799 |
| phase0 | 678 | 218.289 [66.573, 461.601] | 1.0860 [0.3312, 2.2965] | 7.36 [2.27, 15.09] | 199.853 [56.779, 429.405] | 0.0000 |
| phase1 | 755 | 4183.444 [3015.734, 5462.229] | 20.8132 [15.0036, 27.1753] | 157.14 [115.65, 198.19] | 3681.060 [2593.575, 4917.682] | 0.0000 |
| phase2 | 6857 | 315.604 [217.029, 474.242] | 1.5702 [1.0797, 2.3594] | 107.67 [71.28, 162.12] | -461.966 [-842.975, -184.211] | 0.9996 |
| phase_weighted | 8290 | 659.903 [529.350, 813.660] | 3.2831 [2.6336, 4.0481] | 272.17 [211.95, 340.68] | -30.519 [-358.451, 217.727] | 0.5793 |

RR0 (share of den0):

| population | N | NA | AM | CK3 | Q | E |
|---|---|---|---|---|---|---|
| all | -0.0087 [-0.0163, 0.0024] | 0.0100 [-0.0016, 0.0286] | 0.3406 [0.2705, 0.3978] | 0.3075 [-0.0035, 0.5153] | -0.0140 [-0.0390, -0.0004] | -1.5322 [-2.9091, -0.5480] |
| moving | 0.0000 [-0.0055, 0.0045] | 0.0225 [0.0112, 0.0380] | 0.2975 [0.2088, 0.3642] | 0.1295 [-0.0574, 0.2977] | 0.0042 [-0.0016, 0.0098] | 0.0642 [-0.3804, 0.3644] |
| phase0 | -0.0128 [-0.0269, 0.0026] | -0.0128 [-0.0270, 0.0025] | -0.1419 [-0.3602, 0.0248] | -0.3608 [-1.4755, 0.1252] | -0.0122 [-0.0882, 0.0185] | 0.9155 [0.8175, 0.9664] |
| phase1 | 0.0076 [0.0010, 0.0132] | 0.0110 [-0.0157, 0.0375] | -0.1108 [-0.2839, 0.0030] | 0.5537 [0.4149, 0.6690] | 0.0046 [-0.0077, 0.0128] | 0.8799 [0.8365, 0.9192] |
| phase2 | -0.0535 [-0.1025, 0.0102] | 0.0485 [-0.0366, 0.1801] | 0.2585 [-0.1165, 0.5750] | 0.6609 [0.4547, 0.8573] | -0.1238 [-0.2967, -0.0166] | -1.4637 [-2.8938, -0.5365] |
| phase_weighted | -0.0171 [-0.0393, 0.0088] | 0.0252 [-0.0076, 0.0712] | 0.0344 [-0.1277, 0.1481] | 0.5714 [0.4684, 0.6683] | -0.0467 [-0.1311, -0.0031] | -0.0462 [-0.5657, 0.3213] |

### (b) reaction-and-stop, tau 0.75 s, 6 m/s2 (`t0p75_a6p0`)
Unsafe pairs under the scoring: 19900; pairs not truly safe (3 s clearance <= 2 m): 43684; evaluated decisions with no safe row under the scoring: 631; with no truly safe row: 633.

| population | n | den0 (sum) | den0 (pp) | den0 (dec.-eq.) | denE (sum) | share of resamples with denE <= 0 |
|---|---|---|---|---|---|---|
| all | 8290 | 225.742 [94.716, 366.887] | 1.1231 [0.4712, 1.8253] | 93.10 [38.21, 154.03] | -19.747 [-379.931, 259.716] | 0.4481 |
| moving | 1863 | 217.230 [85.937, 369.255] | 1.0807 [0.4275, 1.8371] | 20.13 [7.62, 34.95] | -351.798 [-827.773, 52.746] | 0.9499 |
| phase0 | 678 | 0.000 [0.000, 0.000] | 0.0000 [0.0000, 0.0000] | 0.00 [0.00, 0.00] | 0.000 [0.000, 0.000] | 1.0000 |
| phase1 | 755 | 122.649 [29.667, 236.249] | 0.6102 [0.1476, 1.1754] | 4.61 [1.05, 9.20] | 108.344 [28.410, 209.511] | 0.0000 |
| phase2 | 6857 | 21.161 [3.026, 41.774] | 0.1053 [0.0151, 0.2078] | 7.22 [1.02, 14.18] | -22.050 [-72.502, 16.828] | 0.7777 |
| phase_weighted | 8290 | 28.673 [7.309, 51.341] | 0.1427 [0.0364, 0.2554] | 11.83 [2.95, 21.43] | -8.372 [-49.607, 27.037] | 0.5818 |

RR0 (share of den0):

| population | N | NA | AM | CK3 | Q | E |
|---|---|---|---|---|---|---|
| all | -0.0006 [-0.0107, 0.0050] | 0.0216 [-0.0027, 0.0613] | 0.8008 [0.7388, 0.8705] | 0.5705 [-0.2851, 0.8544] | -0.0063 [-0.0170, 0.0193] | -0.0875 [-2.1818, 0.8707] |
| moving | -0.0217 [-0.0547, 0.0055] | -0.0091 [-0.0438, 0.0393] | 0.4070 [0.2551, 0.5016] | -0.9736 [-2.8460, -0.2274] | -0.0267 [-0.0439, 0.0212] | -1.6195 [-7.3061, 0.1823] |
| phase0 | n/a n/a (20000 left out) | n/a n/a (20000 left out) | n/a n/a (20000 left out) | n/a n/a (20000 left out) | n/a n/a (20000 left out) | n/a n/a (20000 left out) |
| phase1 | 0.0216 [-0.0485, 0.0626] | -0.1048 [-0.3862, 0.0180] | -0.6739 [-1.5077, -0.2774] | 0.1695 [-1.5432, 0.9486] | -0.0130 [-0.1198, 0.1129] | 0.8834 [0.7114, 1.0000] |
| phase2 | -0.0462 [-0.1377, 0.0200] | 0.2081 [-0.1205, 0.3624] | 0.8105 [-0.0518, 0.9469] | 0.7912 [0.5409, 0.9842] | -0.0145 [-0.2066, 0.0671] | -1.0420 [-10.1104, 0.6020] |
| phase_weighted | -0.0198 [-0.0659, 0.0131] | 0.0862 [-0.1650, 0.2321] | 0.2322 [-0.6277, 0.5850] | 0.5490 [-0.2297, 0.9264] | -0.0139 [-0.1154, 0.0478] | -0.2920 [-3.3686, 0.7131] |

The brief asks for intervals for "all" and phase-weighted; the other rows carry them too (same draw). Phase 0 under (b) has den0 = 0 (no ratio).

## 5. Item 3 (R12a): the first T s after the lead's stop
Draw of record, 20000 resamples. n by phase shows what each population keeps.

| T (s) | n (phase 0 / 1 / 2) | R (pp) | den0 (sum) |
|---|---|---|---|
| 0 | 1433 (678 / 755 / 0) | 8.5841 [6.1592, 11.0841] | 1738.521 [1249.781, 2244.697] |
| 1 | 1733 (678 / 755 / 300) | 10.0036 [7.7272, 12.2588] | 2041.085 [1577.377, 2504.375] |
| 2 | 2033 (678 / 755 / 600) | 10.6450 [8.4850, 12.8289] | 2200.738 [1753.253, 2634.267] |
| 5 | 2933 (678 / 755 / 1500) | 10.1453 [8.3103, 11.8686] | 2127.446 [1756.108, 2471.124] |
| 10 | 4433 (678 / 755 / 3000) | 8.3932 [6.9540, 9.7423] | 1791.924 [1498.836, 2055.750] |
| 20 | 7422 (678 / 755 / 5989) | 6.0033 [4.9242, 7.0066] | 1297.063 [1077.229, 1496.108] |

RR:

| T (s) | N | NA | AM | CK3 |
|---|---|---|---|---|
| 0 | -0.0002 [-0.0046, 0.0036] | 0.0180 [0.0000, 0.0406] | 0.4338 [0.3004, 0.5235] | 0.2887 [0.1703, 0.3905] |
| 1 | 0.0004 [-0.0039, 0.0021] | 0.0163 [0.0021, 0.0313] | 0.2820 [0.1860, 0.3503] | 0.4117 [0.2985, 0.5185] |
| 2 | -0.0041 [-0.0054, 0.0013] | 0.0138 [0.0032, 0.0270] | 0.3045 [0.2336, 0.3562] | 0.5372 [0.4403, 0.6208] |
| 5 | -0.0009 [-0.0030, 0.0011] | 0.0149 [0.0059, 0.0250] | 0.3407 [0.2848, 0.3834] | 0.6844 [0.6055, 0.7554] |
| 10 | 0.0003 [-0.0018, 0.0010] | 0.0153 [0.0068, 0.0248] | 0.3593 [0.3034, 0.4044] | 0.7662 [0.6916, 0.8371] |
| 20 | -0.0002 [-0.0012, 0.0012] | 0.0154 [0.0072, 0.0249] | 0.3697 [0.3115, 0.4196] | 0.8179 [0.7439, 0.8925] |

RR0:

| T (s) | N | NA | AM | CK3 |
|---|---|---|---|---|
| 0 | -0.0002 [-0.0046, 0.0036] | 0.0179 [0.0000, 0.0402] | 0.4305 [0.2975, 0.5192] | 0.2866 [0.1690, 0.3870] |
| 1 | 0.0004 [-0.0039, 0.0021] | 0.0161 [0.0021, 0.0308] | 0.2778 [0.1830, 0.3454] | 0.4055 [0.2945, 0.5096] |
| 2 | -0.0040 [-0.0053, 0.0013] | 0.0134 [0.0031, 0.0264] | 0.2961 [0.2276, 0.3476] | 0.5223 [0.4288, 0.6055] |
| 5 | -0.0009 [-0.0029, 0.0010] | 0.0143 [0.0057, 0.0240] | 0.3266 [0.2722, 0.3685] | 0.6560 [0.5808, 0.7243] |
| 10 | 0.0003 [-0.0017, 0.0010] | 0.0144 [0.0065, 0.0233] | 0.3383 [0.2837, 0.3815] | 0.7214 [0.6496, 0.7868] |
| 20 | -0.0002 [-0.0011, 0.0011] | 0.0143 [0.0067, 0.0230] | 0.3439 [0.2868, 0.3906] | 0.7609 [0.6869, 0.8262] |

Sensitivity (points only), k_stop from the first evaluated phase-2 decision: n = 1433, 1733, 2033, 2933, 4433, 7422; R = 8.5841, 10.0036, 10.6450, 10.1453, 8.3932, 6.0033; RR(CK3) = 0.2887, 0.4117, 0.5372, 0.6844, 0.7662, 0.8179. Largest difference from the main reading over every point of the table: 0 (in the 5 runs concerned no evaluated decision lies at or after the stop, so the two readings keep the same decisions).

## 6. Item 4 (R12b): one margin scale per phase
Points on the full sample; intervals over the first 400 rows of the draw of record. Sums over the 201 pooled single-scale levels.

| quantity | point | 95% interval |
|---|---|---|
| den1 = sum(F1_F0 - F1_E), single scale | 1116.9119 | [903.0345, 1318.3053] |
| gain_F0 = sum(F1_F0 - Fps_F0) | 997.1411 | [805.5026, 1189.8993] |
| den_ps = sum(Fps_F0 - Fps_E) | 190.1689 | [152.8767, 216.4515] |
| den0_ps = sum(Fps_F0 - F_O) | 208.0941 | [163.0993, 241.6513] |
| den0, single scale (for reference) | 1205.2352 | [989.9239, 1401.3287] |
| Dps(N) = sum(Fps_F0 - Fps_N) | -0.2413 | [-0.7294, 1.2454] |
| Dps(NA) = sum(Fps_F0 - Fps_NA) | 7.8046 | [3.3589, 12.5634] |
| Dps(AM) = sum(Fps_F0 - Fps_AM) | 73.7153 | [49.7985, 91.5458] |
| Dps(CK3) = sum(Fps_F0 - Fps_CK3) | 120.4704 | [88.2460, 141.8993] |
| Dps(Q) = sum(Fps_F0 - Fps_Q) | -1.0253 | [-3.8713, 1.6798] |
| D1(N), single scale (for reference) | 1.3631 | [-1.2246, 1.3676] |
| D1(NA), single scale (for reference) | 18.6128 | [9.1880, 25.4219] |
| D1(AM), single scale (for reference) | 419.7346 | [345.3861, 481.9253] |
| D1(CK3), single scale (for reference) | 928.6852 | [753.4294, 1104.9842] |
| D1(Q), single scale (for reference) | -2.0145 | [-8.0575, 0.9379] |

Ratios of these sums (derived; intervals over the same 400 rows):

| ratio | point | 95% interval |
|---|---|---|
| gain_F0 / den1 | 0.8928 | [0.8365, 0.9682] |
| den_ps / den1 | 0.1703 | [0.1378, 0.2027] |
| den0_ps / den0 (single scale) | 0.1727 | [0.1400, 0.2078] |
| Dps(N) / den_ps | -0.0013 | [-0.0041, 0.0068] |
| Dps(NA) / den_ps | 0.0410 | [0.0193, 0.0653] |
| Dps(AM) / den_ps | 0.3876 | [0.2704, 0.4779] |
| Dps(CK3) / den_ps | 0.6335 | [0.4903, 0.7634] |
| Dps(Q) / den_ps | -0.0054 | [-0.0193, 0.0095] |
| Dps(N) / den0_ps | -0.0012 | [-0.0037, 0.0061] |
| Dps(NA) / den0_ps | 0.0375 | [0.0178, 0.0601] |
| Dps(AM) / den0_ps | 0.3542 | [0.2392, 0.4455] |
| Dps(CK3) / den0_ps | 0.5789 | [0.4539, 0.6679] |
| Dps(Q) / den0_ps | -0.0049 | [-0.0184, 0.0087] |

Distinct (count, caution sum, safe count) triples per phase (0, 1, 2): F0 [97, 103, 156]; E [131, 80, 191]; N [97, 105, 153]; NA [97, 108, 153]; AM [97, 139, 117]; CK3 [179, 178, 141]; Q [101, 107, 128]. Full enumeration at the point: largest difference from the fast method 0.0. Levels recomputed by enumeration in the 400 resamples: 0; resamples with an undefined frontier level: 0; resamples where the no-diagonal variant differs: 0.

## 7. Item 5 (R9): validity of the run-bootstrap intervals (3 s commitment, all evaluated decisions)
### 7.1 The draw of record (20,000 resamples)

| statistic | point | 95% percentile | 95% basic | range over resamples |
|---|---|---|---|---|
| R | 5.5568 | [4.4986, 6.6038] | [4.5097, 6.6150] | [3.2508, 7.9224] |
| RR_N | 0.00122 | [-0.00108, 0.00119] | [0.00125, 0.00352] | [-0.00237, 0.00247] |
| RR_NA | 0.01666 | [0.00729, 0.02519] | [0.00814, 0.02603] | [0.00158, 0.03666] |
| RR_AM | 0.37580 | [0.31558, 0.42536] | [0.32624, 0.43602] | [0.21944, 0.48322] |
| RR_CK3 | 0.83148 | [0.75281, 0.90333] | [0.75963, 0.91014] | [0.67411, 0.97880] |
| RR_Q | -0.00180 | [-0.00655, 0.00116] | [-0.00476, 0.00294] | [-0.01100, 0.00496] |
| RR0_CK3 | 0.77054 | [0.69460, 0.83487] | [0.70621, 0.84648] | [0.59354, 0.90145] |
| RR_NA_minus_RR_N | 0.01544 | [0.00729, 0.02509] | [0.00579, 0.02359] | [0.00121, 0.03561] |

### 7.2 Double bootstrap (2000 outer x 1000 inner)
Coverage of the two-sided percentile interval at each nominal level (exact-arithmetic rule); in brackets the float rule where it differs.

| statistic | 0.90 | 0.95 | 0.99 | 0.999 | 1.0 | basic, 0.95 | smallest level with coverage >= 0.95 | interval of record at that level |
|---|---|---|---|---|---|---|---|---|
| R | 0.8935 | 0.9345 | 0.9835 (0.9820) | 0.9955 | 1.0000 | 0.9210 | 0.964 | [4.4287, 6.6816] |
| RR_N | 0.2975 | 0.5280 | 0.8860 | 0.9820 | 1.0000 | 0.5235 | 0.996 | [-0.00161, 0.00166] |
| RR_NA | 0.8630 | 0.9220 (0.9215) | 0.9785 | 0.9935 | 1.0000 | 0.8730 | 0.972 | [0.00645, 0.02660] |
| RR_AM | 0.8805 | 0.9330 (0.9325) | 0.9820 (0.9810) | 0.9940 | 1.0000 | 0.9510 | 0.962 (float rule: 0.963) | [0.31178, 0.42838] |
| RR_CK3 | 0.8885 | 0.9320 (0.9315) | 0.9800 (0.9790) | 0.9930 | 1.0000 | 0.9555 | 0.97 | [0.74462, 0.91204] |
| RR_Q | 0.8605 | 0.9250 (0.9245) | 0.9790 (0.9780) | 0.9950 | 1.0000 | 0.9105 | 0.968 (float rule: 0.969) | [-0.00691, 0.00147] |
| RR0_CK3 | 0.8975 | 0.9480 | 0.9850 (0.9840) | 0.9955 | 1.0000 | 0.9450 | 0.952 (float rule: 0.953) | [0.69404, 0.83540] |
| RR_NA_minus_RR_N | 0.8805 | 0.9355 (0.9340) | 0.9840 (0.9835) | 0.9955 | 1.0000 | 0.8930 | 0.962 | [0.00687, 0.02571] |

Misses at nominal 0.95, by side (truth below the inner 2.5% point / above the inner 97.5% point): R 0.0225 / 0.0430; RR_N 0.0000 / 0.4720; RR_NA 0.0065 / 0.0715; RR_AM 0.0220 / 0.0450; RR_CK3 0.0190 / 0.0490; RR_Q 0.0280 / 0.0470; RR0_CK3 0.0225 / 0.0295; RR_NA_minus_RR_N 0.0170 / 0.0475.
Inner values left out for a non-positive denominator: 0 in total; inner values exactly equal to the truth: 0 in total.

### 7.3 Resampling stratified by the recording setting alpha (seed 20261122) and the 30 long runs (seed 20261123)

| statistic | stratified: 95% percentile | 30 long runs: point | 30 long runs: 95% percentile |
|---|---|---|---|
| R | [4.5616, 6.5409] | 5.4615 | [4.3298, 6.5677] |
| RR_N | [-0.00105, 0.00119] | -0.00012 | [-0.00111, 0.00121] |
| RR_NA | [0.00742, 0.02529] | 0.01582 | [0.00749, 0.02705] |
| RR_AM | [0.32094, 0.42097] | 0.38785 | [0.32828, 0.44280] |
| RR_CK3 | [0.75929, 0.90077] | 0.85158 | [0.77470, 0.92469] |
| RR_Q | [-0.00652, 0.00121] | -0.00329 | [-0.00698, 0.00126] |
| RR0_CK3 | [0.70045, 0.83181] | 0.78943 | [0.71351, 0.85264] |
| RR_NA_minus_RR_N | [0.00734, 0.02519] | 0.01594 | [0.00738, 0.02693] |

Long runs: 30 runs, 8130 evaluated decisions; the five short runs and their evaluated decisions: 0008 (27), 0025 (18), 0031 (53), 0033 (25), 0034 (37).

## 8. Item 6 (R19 / R20)
Margin ratio m = 1/sqrt(cN/cF0), rows of evaluated decisions with finite positive cN and cF0, 223 stored files.

| family (all runs) | runs | evaluated decisions | rows | median m | share with abs(m/median - 1) > 0.05 | rows outside |
|---|---|---|---|---|---|---|
| benign | 20 | 5420 | 40120 | 1.092739 | 0.395513 | 15868 |
| cutin | 20 | 5420 | 90227 | 1.102484 | 0.001419 | 128 |
| lead_braking | 55 | 11308 | 152264 | 1.102870 | 0.007402 | 1127 |
| pedestrian_crossing | 51 | 13821 | 157972 | 0.882621 | 0.914947 | 144536 |
| stopped | 55 | 10054 | 121685 | 1.102733 | 0.012672 | 1542 |
| vehicle_crossing | 22 | 5691 | 42122 | 0.914599 | 0.959071 | 40398 |

| family, set | runs | evaluated decisions | rows | median m | share outside 5% | rows outside |
|---|---|---|---|---|---|---|
| benign, tuning | 20 | 5420 | 40120 | 1.092739 | 0.395513 | 15868 |
| cutin, tuning | 20 | 5420 | 90227 | 1.102484 | 0.001419 | 128 |
| lead_braking, fit | 35 | 8290 | 120522 | 1.102877 | 0.008231 | 992 |
| lead_braking, tuning | 20 | 3018 | 31742 | 1.102807 | 0.004253 | 135 |
| pedestrian_crossing, fit | 31 | 8401 | 113537 | 0.892142 | 0.907149 | 102995 |
| pedestrian_crossing, tuning | 20 | 5420 | 44435 | 0.868290 | 0.915832 | 40695 |
| stopped, fit | 35 | 6260 | 87860 | 1.102734 | 0.010938 | 961 |
| stopped, tuning | 20 | 3794 | 33825 | 1.102732 | 0.017177 | 581 |
| vehicle_crossing, fit | 2 | 542 | 4671 | 0.507381 | 0.989510 | 4622 |
| vehicle_crossing, tuning | 20 | 5149 | 37451 | 0.922879 | 0.950842 | 35610 |

Lead braking, the 35 evaluation runs, evaluated decisions by the age of the lead's track (`prim_age`): <0.5 s: 5; 0.5-1 s: 5; 1-2 s: 0; 2-4 s: 0; >=4 s: 8280 (n = 8290).

Extra (Amendment R19, not in the brief's list), all 55 stored lead-braking runs: 152264 rows, median m 1.102870, 1127 rows outside the 5% band. By track age (rows / rows outside): <0.5 s: 80 / 0; 0.5-1 s: 84 / 84; 1-2 s: 0 / 0; 2-4 s: 0 / 0; >=4 s: 152100 / 1043. By `prim_miss`: miss 0: 152180 / 1043; miss 2: 84 / 84.

Extra (Amendment R19, not in the brief's list), the 35 evaluation runs: 120522 rows, median m 1.102877, 992 rows outside the 5% band. By track age (rows / rows outside): <0.5 s: 80 / 0; 0.5-1 s: 84 / 84; 1-2 s: 0 / 0; 2-4 s: 0 / 0; >=4 s: 120358 / 908. By `prim_miss`: miss 0: 120438 / 908; miss 2: 84 / 84.


## 9. Addendum, added 18 Nov 2026 17:40 after the comparison (nothing above this line was changed)
Everything above, and `RECOUNT_RESULTS_v01.json`, was written at 17:20, before any file of the first program was opened. Afterwards only `revision_v11\analysis\out\*.json` was read, for the comparison in `RECOUNT_COMPARE_v01.md`. For that comparison `rc_extra_v01.py` stored the per-resample arrays of the analyses above and added quantities that the first program prints beyond the brief (CK3 with the zero-margin point of F0, the partial oracles P25 / P50 / P75, the published unsigned table for every population, four more reaction-and-stop settings and count (ii) under the 2 m gap, the two track-age populations, leave-one-run-out). Their definitions come from the brief and from the allowed second-program library; they were computed after the first program's outputs had been seen, so they are a weaker check than the numbers of sections 3 to 8, and `RECOUNT_COMPARE_v01.md` labels them "extra". The stored arrays reproduce the numbers of sections 3 to 5 exactly (988 values re-formed, largest difference 0).
