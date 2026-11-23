> **TABLE S16.** Validity of the run-bootstrap intervals (3 s commitment, all evaluated decisions, step frontier). Point; the 95% percentile and basic intervals of the draw of record (20,000 run resamples); their coverage estimated by a double bootstrap (2000 outer × 1000 inner resamples; the full-sample value plays the truth; Monte Carlo standard error about 0.005); the smallest nominal level at which the percentile interval reaches 95% estimated coverage, and the percentile interval of the draw of record at that level (the calibrated interval).

| Statistic | Point | 95% percentile interval | Estimated coverage | 95% basic interval | Estimated coverage | Calibrated nominal level | Calibrated interval |
|---|---|---|---|---|---|---|---|
| $R$ (pp) | 5.56 | [4.50, 6.60] | 0.934 | [4.51, 6.61] | 0.921 | 0.964 | [4.43, 6.68] |
| RR(N) | 0.0012 | [−0.0011, 0.0012] | 0.528 | [0.0012, 0.0035] | 0.523 | 0.996 | [−0.0016, 0.0017] |
| RR(NA) | 0.017 | [0.007, 0.025] | 0.922 | [0.008, 0.026] | 0.873 | 0.972 | [0.006, 0.027] |
| RR(AM) | 0.376 | [0.316, 0.425] | 0.933 | [0.326, 0.436] | 0.951 | 0.962 | [0.312, 0.428] |
| RR(CK3) | 0.831 | [0.753, 0.903] | 0.932 | [0.760, 0.910] | 0.956 | 0.97 | [0.745, 0.912] |
| RR(Q) | −0.0018 | [−0.0065, 0.0012] | 0.925 | [−0.0048, 0.0029] | 0.910 | 0.968 | [−0.0069, 0.0015] |
| RR₀(CK3) | 0.771 | [0.695, 0.835] | 0.948 | [0.706, 0.846] | 0.945 | 0.952 | [0.694, 0.835] |
| RR(NA) − RR(N) | 0.015 | [0.007, 0.025] | 0.935 | [0.006, 0.024] | 0.893 | 0.962 | [0.007, 0.026] |

> **TABLE S17.** Sensitivities of the intervals of Table S16: run resampling stratified by the recording setting α (10, 12, 13 runs; 20,000 resamples); the 30 full-length runs alone (the five short runs left out; point and percentile interval); subsampling 15, 20 and 25 of the 35 runs without replacement (5,000 subsamples each; interval from the root √m(θ*−θ) with the finite-population factor); and the range over leaving one run out.

| Statistic | Stratified by α | 30 full-length runs | Subsampling, m = 15 | Subsampling, m = 20 | Subsampling, m = 25 | Leave one run out (min, max) |
|---|---|---|---|---|---|---|
| $R$ (pp) | [4.56, 6.54] | 5.46 [4.33, 6.57] | [4.52, 6.64] | [4.51, 6.64] | [4.50, 6.65] | 5.36, 5.80 |
| RR(N) | [−0.0010, 0.0012] | −0.0001 [−0.0011, 0.0012] | [0.0011, 0.0033] | [0.0013, 0.0038] | [0.0014, 0.0047] | −0.0009, 0.0012 |
| RR(NA) | [0.007, 0.025] | 0.016 [0.007, 0.027] | [0.007, 0.027] | [0.008, 0.027] | [0.008, 0.027] | 0.014, 0.018 |
| RR(AM) | [0.321, 0.421] | 0.388 [0.328, 0.443] | [0.325, 0.441] | [0.323, 0.438] | [0.324, 0.432] | 0.363, 0.386 |
| RR(CK3) | [0.759, 0.901] | 0.852 [0.775, 0.925] | [0.758, 0.915] | [0.761, 0.913] | [0.765, 0.915] | 0.809, 0.842 |
| RR(Q) | [−0.0065, 0.0012] | −0.0033 [−0.0070, 0.0013] | [−0.0052, 0.0027] | [−0.0051, 0.0027] | [−0.0051, 0.0030] | −0.0038, −0.0016 |
| RR₀(CK3) | [0.700, 0.832] | 0.789 [0.714, 0.853] | [0.703, 0.850] | [0.705, 0.846] | [0.704, 0.845] | 0.757, 0.781 |
| RR(NA) − RR(N) | [0.007, 0.025] | 0.016 [0.007, 0.027] | [0.005, 0.024] | [0.006, 0.025] | [0.006, 0.025] | 0.014, 0.017 |

> **TABLE S18.** Plans judged until their stop ends. For each reaction-and-stop setting: the decision–row pairs that the scoring of record judges safe although their stop ends after the 3 s window (the pairs of count (ii)); those among them whose recording ends before the stop (count (i)); how many of the former are unsafe when the same trajectory is followed against the logged truth until the stop ends; and the unsafe pairs as scored and in the estimate. 140,930 pairs of evaluated decisions and rows; 24,902 are unsafe under the 3 s commitment.

| τ (s) | $A$ (m/s²) | Safe as scored, stop after 3 s | Recording ends before the stop | Unsafe when judged to the stop | Unsafe pairs, as scored | Unsafe pairs, estimate |
|---|---|---|---|---|---|---|
| 0.5 | 6 | 2,897 | 94 | 8 | 1,417 | 1,425 |
| 0.75 | 6 | 5,356 | 153 | 28 | 3,334 | 3,362 |
| 1 | 6 | 5,301 | 230 | 126 | 5,631 | 5,757 |
| 1.25 | 6 | 7,048 | 296 | 215 | 8,530 | 8,745 |
| 1.5 | 6 | 8,583 | 372 | 374 | 12,714 | 13,088 |
| 1.8 | 6 | 9,900 | 487 | 651 | 15,824 | 16,475 |
| 0.75 | 4 | 8,905 | 773 | 440 | 4,373 | 4,813 |
| 0.75 | 5 | 6,781 | 365 | 161 | 3,740 | 3,901 |
| 0.75 | 7.6 | 2,431 | 37 | 0 | 2,802 | 2,802 |

> **TABLE S19.** The reaction-and-stop scoring with plans judged until their stop ends (the estimate), beside the scoring of record. The 3 s oracle's advantage relative to its 3 s value: as scored (the 3 s window's flags kept), the estimate with its 95% interval, the estimate with the pairs whose recording ends before the stop counted unsafe, and count (ii) of record (every pair whose stop ends after 3 s counted unsafe). den₀: the class average's avoidable wrong-go against the perfect oracle of the estimate, in percentage points and relative to its 3 s value. 35 evaluation runs, all evaluated decisions, step frontier, zero standstill gap. Points only at 4, 5 and 7.6 m/s².

| τ (s) | $A$ (m/s²) | As scored | Estimate [95%] | Recording-end pairs unsafe | Count (ii) | den₀, estimate (pp) [95%] | den₀ relative to 3 s [95%] |
|---|---|---|---|---|---|---|---|
| 0.5 | 6 | 0.019 | 0.019 [0.000, 0.052] | 0.029 | 0.447 | 0.11 [0.00, 0.33] | 0.019 [0.000, 0.052] |
| 0.75 | 6 | 0.121 | 0.122 [0.052, 0.188] | 0.144 | 0.531 | 0.71 [0.26, 1.23] | 0.118 [0.050, 0.182] |
| 1 | 6 | 0.234 | 0.241 [0.136, 0.331] | 0.275 | 0.636 | 1.41 [0.68, 2.19] | 0.235 [0.133, 0.322] |
| 1.25 | 6 | 0.364 | 0.384 [0.259, 0.488] | 0.426 | 1.295 | 2.27 [1.29, 3.26] | 0.378 [0.255, 0.478] |
| 1.5 | 6 | 0.490 | 0.537 [0.405, 0.643] | 0.586 | 1.360 | 3.20 [2.04, 4.36] | 0.533 [0.401, 0.638] |
| 1.8 | 6 | 0.644 | 0.732 [0.601, 0.829] | 0.776 | 1.146 | 4.37 [3.03, 5.64] | 0.729 [0.598, 0.825] |
| 0.75 | 4 | 0.253 | 0.293 | n/a | n/a | 1.72 | 0.286 |
| 0.75 | 5 | 0.162 | 0.179 | n/a | n/a | 1.04 | 0.173 |
| 0.75 | 7.6 | 0.064 | 0.064 | n/a | n/a | 0.37 | 0.062 |

> **TABLE S20a.** τ = 0.75 s, stop at 6 m/s², zero gap, the estimate (plans judged until their stop ends): den₀ in decision-equivalents and each source's share RR₀ of it with its 95% interval and the branch of Section S8.1 without the hull clause (1 not evaluable; 2 below the class average; 3 not distinguishable from zero; 4 most; 5 distinguishable from zero), by population, each on its own frontier.

| Population | n | den₀, dec.-eq. [95%] | RR₀(E) | RR₀(N) | RR₀(NA) | RR₀(CK3) | RR₀(AM) | RR₀(Q) |
|---|---|---|---|---|---|---|---|---|
| All | 8,290 | 58.8 [20.9, 103.2] | 0.958 [0.920, 0.988] | 0.000 [−0.006, 0.005] (3) | 0.012 [−0.004, 0.039] (3) | 0.936 [0.908, 0.959] (4) | 0.570 [0.472, 0.664] (5) | −0.031 [−0.074, 0.013] (3) |
| Ego moving | 1,863 | 12.2 [4.3, 21.1] | 0.951 [0.940, 1.000] | −0.013 [−0.031, 0.006] (3) | −0.021 [−0.057, 0.020] (3) | 0.038 [−0.460, 0.381] (3) | 0.257 [0.167, 0.337] (5) | −0.044 [−0.093, 0.022] (3) |
| Lead braking | 755 | 1.5 [0.3, 3.0] | 1.000 [1.000, 1.000] | −0.003 [−0.056, 0.073] (1) | −0.153 [−0.365, 0.025] (1) | −1.109 [−4.636, 0.510] (1) | −0.677 [−1.589, −0.187] (1) | −0.048 [−0.205, 0.216] (1) |
| Lead stopped | 6,857 | 2.2 [0.1, 6.3] | 0.811 [0.652, 0.982] | 0.000 [−0.032, 0.047] (1) | 0.042 [−0.024, 0.250] (1) | 0.788 [0.662, 1.000] (1) | 0.350 [−0.364, 0.647] (1) | −0.252 [−0.502, 0.065] (1) |
| Phase-weighted | 8,290 | 3.7 [0.8, 8.7] | 0.886 [0.778, 0.996] | −0.001 [−0.029, 0.038] (1) | −0.035 [−0.130, 0.078] (1) | 0.038 [−2.164, 0.704] (1) | −0.057 [−0.693, 0.208] (1) | −0.171 [−0.303, 0.111] (1) |

> **TABLE S20b.** τ = 0.75 s, stop at 6 m/s², zero gap, the estimate with the pairs whose recording ends before the stop counted unsafe: den₀ in decision-equivalents and each source's share RR₀ of it with its 95% interval and the branch of Section S8.1 without the hull clause (1 not evaluable; 2 below the class average; 3 not distinguishable from zero; 4 most; 5 distinguishable from zero), by population, each on its own frontier.

| Population | n | den₀, dec.-eq. [95%] | RR₀(E) | RR₀(N) | RR₀(NA) | RR₀(CK3) | RR₀(AM) | RR₀(Q) |
|---|---|---|---|---|---|---|---|---|
| All | 8,290 | 69.5 [31.0, 113.2] | 0.956 [0.917, 0.986] | 0.000 [−0.005, 0.004] (3) | 0.012 [−0.002, 0.033] (3) | 0.829 [0.623, 0.946] (4) | 0.492 [0.341, 0.613] (5) | −0.026 [−0.063, 0.011] (3) |
| Ego moving | 1,863 | 19.3 [8.4, 30.2] | 0.958 [0.948, 1.014] | −0.008 [−0.022, 0.005] (3) | −0.009 [−0.040, 0.016] (3) | 0.087 [−0.255, 0.324] (3) | 0.178 [0.084, 0.285] (5) | −0.026 [−0.070, 0.013] (3) |
| Lead braking | 755 | 6.7 [0.9, 14.8] | 1.041 [0.980, 1.213] | 0.002 [−0.024, 0.032] (1) | −0.023 [−0.228, 0.018] (1) | −0.083 [−2.396, 0.323] (1) | −0.282 [−1.065, −0.087] (1) | −0.004 [−0.080, 0.092] (1) |
| Lead stopped | 6,857 | 2.2 [0.1, 6.3] | 0.811 [0.652, 0.982] | 0.000 [−0.032, 0.047] (1) | 0.042 [−0.024, 0.250] (1) | 0.788 [0.662, 1.000] (1) | 0.350 [−0.364, 0.647] (1) | −0.252 [−0.502, 0.065] (1) |
| Phase-weighted | 8,290 | 9.4 [1.8, 18.6] | 0.984 [0.851, 1.103] | 0.001 [−0.014, 0.018] (1) | −0.007 [−0.073, 0.031] (1) | 0.137 [−0.793, 0.524] (1) | −0.104 [−0.427, 0.088] (1) | −0.069 [−0.216, 0.030] (1) |

> **TABLE S20c.** As Table S20a, with caution counted at every decision's signed speed difference to the 3 s oracle's row (compare Table S13).

| Population | n | den₀, dec.-eq. [95%] | RR₀(E) | RR₀(N) | RR₀(NA) | RR₀(CK3) | RR₀(AM) |
|---|---|---|---|---|---|---|---|
| All | 8,290 | 53.7 [19.4, 92.8] | 0.930 [0.883, 0.965] | −0.001 [−0.006, 0.006] (3) | 0.007 [−0.007, 0.035] (3) | 0.803 [0.724, 0.851] (4) | 0.532 [0.437, 0.625] (5) |
| Ego moving | 1,863 | 13.7 [4.8, 24.7] | 0.675 [0.535, 0.809] | −0.013 [−0.020, 0.007] (3) | −0.033 [−0.059, 0.003] (3) | −0.895 [−1.437, −0.484] (2) | 0.070 [−0.026, 0.177] (3) |
| Lead braking | 755 | 9.4 [2.5, 16.4] | 0.301 [0.210, 0.484] | 0.001 [−0.015, 0.018] (1) | −0.037 [−0.089, −0.010] (1) | −2.350 [−3.972, −1.913] (1) | −0.120 [−0.309, 0.002] (1) |
| Lead stopped | 6,857 | 2.2 [0.1, 6.3] | 0.786 [0.627, 0.961] | 0.004 [−0.032, 0.046] (1) | 0.042 [−0.028, 0.247] (1) | 0.706 [0.576, 0.940] (1) | 0.314 [−0.514, 0.600] (1) |
| Phase-weighted | 8,290 | 11.6 [3.1, 20.9] | 0.395 [0.305, 0.570] | 0.001 [−0.013, 0.016] (3) | −0.022 [−0.060, 0.008] (3) | −1.763 [−3.231, −1.122] (2) | −0.036 [−0.223, 0.100] (3) |

> **TABLE S20d.** The estimate at the other delays (stop at 6 m/s², zero gap): den₀ in decision-equivalents and the shares of the tracker covariance, the braking prediction and the acceleration margin, pooled and phase-weighted.

| τ (s) | den₀ all, dec.-eq. [95%] | RR₀(N) all | RR₀(CK3) all | RR₀(AM) all | den₀ phase-weighted, dec.-eq. [95%] | RR₀(N) phase-weighted | RR₀(CK3) phase-weighted | RR₀(AM) phase-weighted |
|---|---|---|---|---|---|---|---|---|
| 0.5 | 9.3 [0.0, 27.2] | −0.003 [−0.010, 0.021] (1) | 0.879 [0.840, 0.945] (1) | 0.573 [0.449, 0.715] (1) | 1.6 [0.0, 5.5] | −0.016 [−0.020, 0.000] (1) | 0.338 [−19.000, 0.683] (1) | 0.369 [0.000, 0.609] (1) |
| 0.75 | 58.8 [20.9, 103.2] | 0.000 [−0.006, 0.005] (3) | 0.936 [0.908, 0.959] (4) | 0.570 [0.472, 0.664] (5) | 3.7 [0.8, 8.7] | −0.001 [−0.029, 0.038] (1) | 0.038 [−2.164, 0.704] (1) | −0.057 [−0.693, 0.208] (1) |
| 1 | 116.8 [55.0, 184.6] | 0.001 [−0.005, 0.004] (3) | 0.943 [0.919, 0.962] (4) | 0.536 [0.458, 0.618] (5) | 13.6 [4.7, 24.8] | −0.015 [−0.042, 0.021] (3) | 0.569 [−0.031, 0.870] (3) | 0.027 [−0.328, 0.261] (3) |
| 1.25 | 187.9 [105.5, 274.5] | 0.001 [−0.003, 0.002] (3) | 0.943 [0.918, 0.962] (4) | 0.506 [0.431, 0.581] (5) | 31.9 [15.3, 51.7] | −0.004 [−0.014, 0.009] (3) | 0.718 [0.415, 0.894] (5) | 0.083 [−0.140, 0.265] (3) |
| 1.5 | 265.1 [166.0, 366.2] | 0.001 [−0.002, 0.001] (3) | 0.933 [0.905, 0.954] (4) | 0.452 [0.384, 0.516] (5) | 61.4 [34.8, 91.7] | −0.001 [−0.006, 0.007] (3) | 0.786 [0.590, 0.908] (4) | 0.104 [−0.066, 0.250] (3) |
| 1.8 | 362.4 [248.4, 473.0] | 0.001 [−0.001, 0.001] (3) | 0.845 [0.791, 0.887] (4) | 0.386 [0.321, 0.443] (5) | 109.9 [76.2, 141.7] | −0.001 [−0.005, 0.005] (3) | 0.760 [0.628, 0.865] (4) | 0.137 [−0.005, 0.269] (3) |

> **TABLE S21.** Caution counted at its signed value under the 3 s commitment, beside the values of record. Signed: caution is averaged over every evaluated decision (each has a truly safe row), at its signed speed difference to the first truly safe row; of record: over truly safe selections only. Room $R$ and share recovered RR with 95% run-bootstrap percentile intervals; step frontier; each population on its own frontier. The last three columns give the partial oracles (the oracle's margin on a random 25%, 50% and 75% of decisions, the class average's elsewhere) under signed caution.

| Population | Caution | $R$ (pp) | RR(N) | RR(NA) | RR(AM) | RR(CK3) | RR(Q) | Partial oracle 25% | 50% | 75% |
|---|---|---|---|---|---|---|---|---|---|---|
| All | of record | 5.56 [4.50, 6.60] | 0.0012 [−0.0011, 0.0012] | 0.017 [0.007, 0.025] | 0.376 [0.316, 0.425] | 0.831 [0.753, 0.903] | −0.0018 [−0.0065, 0.0012] | 0.27 [0.22, 0.31] | 0.54 [0.47, 0.58] | 0.78 [0.73, 0.81] |
| All | signed | 4.86 [4.05, 5.61] | −0.0002 [−0.0011, 0.0012] | 0.016 [0.008, 0.026] | 0.378 [0.322, 0.430] | 0.817 [0.735, 0.891] | −0.0030 [−0.0073, 0.0010] | 0.27 [0.23, 0.31] | 0.54 [0.48, 0.59] | 0.78 [0.74, 0.82] |
| Ego moving | of record | 10.16 [7.96, 12.39] | −0.0001 [−0.0058, 0.0016] | 0.016 [0.002, 0.028] | 0.293 [0.207, 0.350] | 0.472 [0.353, 0.570] | 0.0018 [−0.0067, 0.0050] | −0.11 [−0.23, −0.04] | 0.05 [−0.12, 0.16] | 0.44 [0.31, 0.53] |
| Ego moving | signed | 6.32 [4.83, 7.42] | −0.0031 [−0.0070, 0.0023] | 0.020 [0.005, 0.035] | 0.346 [0.249, 0.425] | 0.299 [0.127, 0.432] | −0.0014 [−0.0135, 0.0042] | −0.12 [−0.27, −0.04] | 0.01 [−0.22, 0.14] | 0.39 [0.21, 0.49] |
| Lead braking | of record | 15.59 [11.45, 20.04] | −0.0025 [−0.0048, 0.0052] | −0.006 [−0.031, 0.023] | −0.044 [−0.193, 0.062] | 0.606 [0.468, 0.711] | −0.0003 [−0.0076, 0.0106] | −0.68 [−0.93, −0.49] | −0.63 [−0.91, −0.38] | 0.05 [−0.19, 0.23] |
| Lead braking | signed | 5.64 [3.68, 7.57] | 0.0000 [−0.0118, 0.0102] | 0.007 [−0.027, 0.046] | 0.061 [−0.156, 0.237] | 0.347 [0.012, 0.549] | −0.0161 [−0.0430, 0.0046] | −0.71 [−1.19, −0.44] | −0.87 [−1.52, −0.50] | −0.23 [−0.70, 0.05] |
| Lead stopped | of record | 0.82 [0.66, 0.99] | 0.0019 [−0.0045, 0.0043] | 0.079 [0.034, 0.123] | 0.702 [0.636, 0.769] | 0.993 [0.914, 1.108] | −0.0143 [−0.0339, 0.0049] | 0.28 [0.21, 0.35] | 0.54 [0.48, 0.61] | 0.78 [0.73, 0.83] |
| Lead stopped | signed | 0.79 [0.64, 0.95] | 0.0007 [−0.0047, 0.0044] | 0.079 [0.034, 0.125] | 0.703 [0.630, 0.765] | 0.982 [0.903, 1.094] | −0.0146 [−0.0352, 0.0042] | 0.28 [0.21, 0.35] | 0.54 [0.48, 0.61] | 0.78 [0.73, 0.83] |
| Phase-weighted | of record | 2.13 [1.70, 2.56] | −0.0010 [−0.0035, 0.0038] | 0.021 [0.002, 0.045] | 0.192 [0.093, 0.275] | 0.711 [0.614, 0.793] | −0.0048 [−0.0129, 0.0059] | −0.38 [−0.54, −0.24] | −0.27 [−0.45, −0.09] | 0.27 [0.12, 0.39] |
| Phase-weighted | signed | 1.20 [1.03, 1.35] | 0.0004 [−0.0056, 0.0051] | 0.046 [0.019, 0.076] | 0.405 [0.310, 0.487] | 0.666 [0.519, 0.783] | −0.0148 [−0.0340, 0.0008] | −0.18 [−0.33, −0.07] | −0.11 [−0.31, 0.04] | 0.31 [0.15, 0.43] |

> **TABLE S22.** The length of the after-stop segment. Each population keeps every evaluated decision before the lead's stop and those taken less than $T$ after it; 3 s commitment, step frontier, each population on its own frontier and levels; 95% run-bootstrap percentile intervals. In the 30 full-length runs the after-stop segment lasts 18.9–24.9 s.

| $T$ (s) | Decisions | $R$ (pp) [95%] | RR(N) | RR(NA) | RR(AM) | RR(CK3) | RR₀(CK3) | D(CK3), dec.-eq. |
|---|---|---|---|---|---|---|---|---|
| 0 (none) | 1,433 | 8.58 [6.16, 11.08] | −0.0002 [−0.0046, 0.0036] | 0.018 [0.000, 0.041] | 0.434 [0.300, 0.523] | 0.289 [0.170, 0.390] | 0.287 [0.169, 0.387] | 35.5 |
| 1 | 1,733 | 10.00 [7.73, 12.26] | 0.0004 [−0.0039, 0.0021] | 0.016 [0.002, 0.031] | 0.282 [0.186, 0.350] | 0.412 [0.299, 0.519] | 0.406 [0.294, 0.510] | 71.4 |
| 2 | 2,033 | 10.65 [8.48, 12.83] | −0.0041 [−0.0054, 0.0013] | 0.014 [0.003, 0.027] | 0.305 [0.234, 0.356] | 0.537 [0.440, 0.621] | 0.522 [0.429, 0.606] | 116.2 |
| 5 | 2,933 | 10.15 [8.31, 11.87] | −0.0009 [−0.0030, 0.0011] | 0.015 [0.006, 0.025] | 0.341 [0.285, 0.383] | 0.684 [0.605, 0.755] | 0.656 [0.581, 0.724] | 203.7 |
| 10 | 4,433 | 8.39 [6.95, 9.74] | 0.0003 [−0.0018, 0.0010] | 0.015 [0.007, 0.025] | 0.359 [0.303, 0.404] | 0.766 [0.692, 0.837] | 0.721 [0.650, 0.787] | 285.1 |
| 20 | 7,422 | 6.00 [4.92, 7.01] | −0.0002 [−0.0012, 0.0012] | 0.015 [0.007, 0.025] | 0.370 [0.311, 0.420] | 0.818 [0.744, 0.893] | 0.761 [0.687, 0.826] | 364.4 |
| all | 8,290 | 5.56 [4.50, 6.60] | 0.0012 [−0.0011, 0.0012] | 0.017 [0.007, 0.025] | 0.376 [0.316, 0.425] | 0.831 [0.753, 0.903] | 0.771 [0.695, 0.835] | 383.0 |

> **TABLE S23.** One margin scale per phase of the lead's motion (before the onset, lead braking, lead stopped), 3 s commitment, all evaluated decisions, pooled caution levels of record. (a) The pooled room of record and its parts; (b) each source against a class average that also chooses one scale per phase. Intervals: 400 run resamples of the draw of record.

| Quantity | Percentage points [95%] | Decision-equivalents [95%] | Share of the pooled room [95%] |
|---|---|---|---|
| The pooled room of record, one scale: class average minus oracle | 5.56 [4.49, 6.56] | 460.7 [365.6, 552.5] | 1 |
| What the class average gains from one scale per phase | 4.96 [4.01, 5.92] | 411.3 [319.9, 497.2] | 0.893 [0.836, 0.968] |
| The room that remains when both choose a scale per phase | 0.95 [0.76, 1.08] | 78.4 [59.7, 92.5] | 0.170 [0.138, 0.203] |
| What the oracle gains from one scale per phase | 0.35 [0.09, 0.72] | 29.0 [7.2, 63.2] | n/a |
| The class average with per-phase scales against the perfect oracle | 1.04 [0.81, 1.20] | 85.8 [66.1, 100.8] | n/a |

| Source | RR of record (one scale) | Share of the remaining room, per-phase scales [95%] | Against the perfect oracle, per-phase scales | Gain over the class average: one scale → per-phase scales (dec.-eq.) [95%] |
|---|---|---|---|---|
| N | 0.0012 | −0.0013 [−0.0041, 0.0068] | −0.0012 [−0.0037, 0.0061] | 0.6 → −0.1 [−0.3, 0.5] |
| NA | 0.017 | 0.041 [0.019, 0.065] | 0.038 [0.018, 0.060] | 7.7 → 3.2 [1.4, 5.4] |
| AM | 0.376 | 0.388 [0.270, 0.478] | 0.354 [0.239, 0.446] | 173.1 → 30.4 [19.9, 39.6] |
| CK3 | 0.831 | 0.633 [0.490, 0.763] | 0.579 [0.454, 0.668] | 383.0 → 49.7 [34.2, 61.1] |
| Q | −0.0018 | −0.0054 [−0.0193, 0.0095] | −0.0049 [−0.0184, 0.0087] | −0.8 → −0.4 [−1.5, 0.7] |

> **TABLE S24.** A standstill gap of 2 m: a decision–row pair is unsafe when its true clearance is at most 2 m, for the wrong go and for the caution's truly safe rows alike. den₀ against the perfect oracle for the 2 m requirement, and each source's share RR₀ [95%]; RR₀(E) is the 3 s oracle, which is built for contact and is not an oracle for this requirement. Step frontier; each population on its own frontier; for the 3 s commitment the lead-braking and lead-stopped phases are also given. Points only at 4, 5 and 7.6 m/s².

| Scoring | Population | Decisions without a row keeping 2 m | den₀ (pp) | den₀, dec.-eq. [95%] | RR₀(E) | RR₀(N) | RR₀(NA) | RR₀(CK3) | RR₀(AM) |
|---|---|---|---|---|---|---|---|---|---|
| 3 s commitment | All | 633 | 7.38 | 612.0 [499.9, 719.1] | −1.532 [−2.909, −0.548] | −0.0087 [−0.0163, 0.0024] | 0.010 [−0.002, 0.029] | 0.307 [−0.004, 0.515] | 0.341 [0.270, 0.398] |
| 3 s commitment | Ego moving |  | 13.10 | 244.0 [190.7, 294.8] | 0.064 [−0.380, 0.364] | 0.0000 [−0.0055, 0.0045] | 0.023 [0.011, 0.038] | 0.129 [−0.057, 0.298] | 0.297 [0.209, 0.364] |
| 3 s commitment | Lead braking |  | 20.81 | 157.1 [115.7, 198.2] | 0.880 [0.837, 0.919] | 0.0076 [0.0010, 0.0132] | 0.011 [−0.016, 0.038] | 0.554 [0.415, 0.669] | −0.111 [−0.284, 0.003] |
| 3 s commitment | Lead stopped |  | 1.57 | 107.7 [71.3, 162.1] | −1.464 [−2.894, −0.537] | −0.0535 [−0.1025, 0.0102] | 0.049 [−0.037, 0.180] | 0.661 [0.455, 0.857] | 0.258 [−0.117, 0.575] |
| 3 s commitment | Phase-weighted |  | 3.28 | 272.2 [211.9, 340.7] | −0.046 [−0.566, 0.321] | −0.0171 [−0.0393, 0.0088] | 0.025 [−0.008, 0.071] | 0.571 [0.468, 0.668] | 0.034 [−0.128, 0.148] |
| Stop 0.75 s, 6 m/s² | All | 631 | 1.12 | 93.1 [38.2, 154.0] | −0.087 [−2.182, 0.871] | −0.0006 [−0.0107, 0.0050] | 0.022 [−0.003, 0.061] | 0.571 [−0.285, 0.854] | 0.801 [0.739, 0.870] |
| Stop 0.75 s, 6 m/s² | Ego moving |  | 1.08 | 20.1 [7.6, 35.0] | −1.619 [−7.306, 0.182] | −0.0217 [−0.0547, 0.0055] | −0.009 [−0.044, 0.039] | −0.974 [−2.846, −0.227] | 0.407 [0.255, 0.502] |
| Stop 0.75 s, 6 m/s² | Phase-weighted |  | 0.14 | 11.8 [2.9, 21.4] | −0.292 [−3.369, 0.713] | −0.0198 [−0.0659, 0.0131] | 0.086 [−0.165, 0.232] | 0.549 [−0.230, 0.926] | 0.232 [−0.628, 0.585] |
| Stop 1.8 s, 6 m/s² | All | 633 | 4.85 | 402.4 [309.4, 491.4] | 0.523 [0.039, 0.893] | −0.0030 [−0.0058, 0.0016] | 0.022 [0.011, 0.039] | 0.700 [0.502, 0.826] | 0.506 [0.444, 0.569] |
| Stop 1.8 s, 6 m/s² | Ego moving |  | 7.80 | 145.4 [107.4, 183.4] | 0.344 [−0.105, 0.650] | −0.0043 [−0.0103, 0.0017] | 0.021 [0.006, 0.040] | 0.206 [−0.042, 0.418] | 0.364 [0.265, 0.441] |
| Stop 1.8 s, 6 m/s² | Phase-weighted |  | 1.60 | 132.6 [94.8, 175.6] | 0.717 [0.553, 0.873] | −0.0118 [−0.0168, 0.0054] | 0.031 [0.009, 0.073] | 0.751 [0.615, 0.849] | 0.150 [0.015, 0.274] |
| Stop 0.75 s, 4 m/s² | All | 642 | 1.96 | 162.1 | 0.367 | 0.0014 | 0.045 | 0.720 | 0.726 |
| Stop 0.75 s, 4 m/s² | Ego moving |  | 2.31 | 43.0 | −0.283 | −0.0079 | 0.033 | −0.178 | 0.432 |
| Stop 0.75 s, 4 m/s² | Phase-weighted |  | 0.38 | 31.6 | 0.496 | 0.0016 | 0.102 | 0.759 | 0.265 |
| Stop 0.75 s, 5 m/s² | All | 633 | 1.54 | 127.3 | 0.204 | 0.0005 | 0.028 | 0.669 | 0.767 |
| Stop 0.75 s, 5 m/s² | Ego moving |  | 1.63 | 30.5 | −0.737 | −0.0131 | 0.015 | −0.454 | 0.424 |
| Stop 0.75 s, 5 m/s² | Phase-weighted |  | 0.21 | 17.2 | 0.104 | −0.0058 | 0.057 | 0.642 | 0.148 |
| Stop 0.75 s, 7.6 m/s² | All | 629 | 0.84 | 69.3 | −0.460 | −0.0020 | 0.020 | 0.449 | 0.837 |
| Stop 0.75 s, 7.6 m/s² | Ego moving |  | 0.74 | 13.7 | −2.839 | −0.0326 | −0.025 | −1.634 | 0.400 |
| Stop 0.75 s, 7.6 m/s² | Phase-weighted |  | 0.12 | 9.6 | −0.583 | −0.0201 | 0.120 | 0.515 | 0.420 |

> **TABLE S24b.** As Table S24 at τ = 0.75 s and 6 m/s², with plans judged until their stop ends (the estimate of Table S19) and the 2 m gap applied to the wrong go and to the caution's truly safe rows alike. 631 evaluated decisions have no row that keeps 2 m until its stop ends.

| Population | den₀ (pp) | den₀, dec.-eq. [95%] | RR₀(E) | RR₀(N) | RR₀(NA) | RR₀(CK3) | RR₀(AM) |
|---|---|---|---|---|---|---|---|
| All | 1.14 | 94.7 [39.1, 156.2] | −0.070 [−2.138, 0.873] | −0.0008 [−0.0111, 0.0048] | 0.021 [−0.004, 0.059] | 0.576 [−0.260, 0.856] | 0.801 [0.738, 0.870] |
| Ego moving | 1.10 | 20.4 [7.8, 35.3] | −1.580 [−7.144, 0.196] | −0.0219 [−0.0548, 0.0051] | −0.009 [−0.045, 0.038] | −0.956 [−2.768, −0.216] | 0.407 [0.255, 0.501] |
| Phase-weighted | 0.14 | 11.9 [3.0, 21.5] | −0.287 [−3.325, 0.714] | −0.0193 [−0.0656, 0.0131] | 0.086 [−0.168, 0.230] | 0.547 [−0.231, 0.927] | 0.225 [−0.642, 0.574] |

> **TABLE S25.** The braking prediction at other decelerations. (a) The 35 evaluation runs, 3 s commitment: share of the room RR [95%] by population, and the zero-margin point; computed in the revision, the 3 m/s² row being the value of record. (b) The 20 tuning runs (of record, 13 November 2026), on which 3 m/s² was chosen: pooled RR [95%]; the eighth value tried there, 0.5 m/s², gave 0.085 [0.026, 0.160] and was not run on the evaluation runs.

| Deceleration (m/s²) | All | Ego moving | Lead braking | Lead stopped | Phase-weighted | Zero-margin caution (%) | Zero-margin wrong go (%) | Tuning runs, all |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.276 [0.214, 0.354] | 0.129 [0.094, 0.175] | 0.029 [0.019, 0.044] | 0.795 [0.708, 0.899] | 0.273 [0.220, 0.348] | 1.13 | 8.17 | 0.201 [0.055, 0.380] |
| 2 | 0.565 [0.474, 0.667] | 0.283 [0.208, 0.361] | 0.280 [0.237, 0.338] | 0.953 [0.868, 1.062] | 0.485 [0.433, 0.561] | 1.41 | 6.67 | 0.350 [0.001, 0.697] |
| 3 | 0.831 [0.753, 0.903] | 0.472 [0.353, 0.570] | 0.606 [0.468, 0.711] | 0.993 [0.914, 1.108] | 0.711 [0.614, 0.793] | 1.72 | 4.84 | 0.377 [−0.204, 0.840] |
| 4 | 0.930 [0.869, 0.995] | 0.386 [0.229, 0.501] | 0.531 [0.313, 0.697] | 1.010 [0.932, 1.133] | 0.652 [0.489, 0.783] | 2.27 | 2.76 | 0.274 [−0.464, 0.831] |
| 5 | 0.929 [0.868, 1.001] | 0.182 [−0.068, 0.366] | 0.304 [−0.044, 0.578] | 1.019 [0.941, 1.145] | 0.490 [0.220, 0.699] | 2.86 | 2.00 | 0.119 [−0.757, 0.744] |
| 6 | 0.917 [0.840, 0.993] | 0.022 [−0.324, 0.252] | 0.100 [−0.343, 0.468] | 1.023 [0.945, 1.148] | 0.345 [0.004, 0.623] | 3.31 | 1.59 | −0.055 [−1.016, 0.662] |
| 7 | 0.898 [0.813, 0.980] | −0.127 [−0.537, 0.148] | −0.070 [−0.610, 0.345] | 1.025 [0.946, 1.151] | 0.223 [−0.190, 0.537] | 3.67 | 1.39 | −0.237 [−1.307, 0.536] |

> **TABLE S26.** The margin-ratio check of Fig. 2(b) by scenario family: on every evaluated decision row with a finite positive critical scale under both the tracker covariance and the class average, the tracker's margin over the class average's, $1/\sqrt{g^{\ast}_N/g^{\ast}_{F0}}$. Runs, rows, the median ratio and the share of rows within 5% of that median. Stored arrays of all runs of the project (tuning runs of all six families; evaluation runs where they exist).

| Scenario family | Runs | Decision rows | Median ratio | Rows within 5% of the median (%) | Tuning runs alone: median; within 5% (%) |
|---|---|---|---|---|---|
| Lead braking | 55 | 152,264 | 1.103 | 99.26 | 1.103; 99.57 |
| Stopped vehicle | 55 | 121,685 | 1.103 | 98.73 | 1.103; 98.28 |
| Cut-in | 20 | 90,227 | 1.102 | 99.86 | 1.102; 99.86 |
| Benign driving | 20 | 40,120 | 1.093 | 60.45 | 1.093; 60.45 |
| Pedestrian crossing | 51 | 157,972 | 0.883 | 8.51 | 0.868; 8.42 |
| Vehicle crossing | 22 | 42,122 | 0.915 | 4.09 | 0.923; 4.92 |

> **TABLE S27.** The age of the lead's track. Evaluated decisions of the 35 evaluation runs by track age, and the margin ratio on the decision rows of all 55 lead-braking runs by track age (rows; share more than 5% from the family median 1.103; median ratio).

| Track age (s) | Evaluated decisions (35 runs) | Decision rows (55 runs) | Rows more than 5% from the median | Median ratio |
|---|---|---|---|---|
| [0, 0.5) | 5 | 80 | 0 | 1.137 |
| [0.5, 1) | 5 | 84 | 84 | 1.682 |
| [1, 2) | 0 | 0 | 0 | n/a |
| [2, 4) | 0 | 0 | 0 | n/a |
| ≥ 4 | 8,280 | 152,100 | 1,043 | 1.103 |

> **TABLE S12b.** The partial oracles over 50 further random draws (3 s commitment, step frontier, points): for each share of decisions that take the oracle's margin, the value of the draw of record (Table S12) and the mean and range over the draws.

| Population | 25%: of record; mean [min, max] | 50%: of record; mean [min, max] | 75%: of record; mean [min, max] |
|---|---|---|---|
| All | 0.27; 0.28 [0.26, 0.31] | 0.54; 0.54 [0.50, 0.58] | 0.78; 0.78 [0.75, 0.81] |
| Ego moving | −0.11; −0.08 [−0.14, −0.01] | 0.05; 0.09 [0.00, 0.19] | 0.44; 0.46 [0.34, 0.55] |
| Lead braking | −0.68; −0.64 [−0.76, −0.52] | −0.63; −0.54 [−0.72, −0.40] | 0.05; 0.05 [−0.16, 0.20] |
| Lead stopped | 0.28; 0.28 [0.23, 0.33] | 0.54; 0.55 [0.50, 0.60] | 0.78; 0.79 [0.76, 0.82] |
| Phase-weighted | −0.38; −0.35 [−0.45, −0.26] | −0.27; −0.20 [−0.33, −0.09] | 0.27; 0.28 [0.14, 0.38] |

