# Tables of the manuscript of draft v12 (tables only)

> **TABLE I.** Margin sources. Each supplies the variance *s* along every constraint of the planner's 17 rows; the braking prediction CK3 instead shifts the predicted path and keeps the class-average *s*.

| Source | Margin variance $s$ | Role |
|---|---|---|
| F0, class average | $\bar P$, the mean of the tracker's reported route-frame covariances (120 tuning runs, six families, 20,611 vehicle states), projected as the tracker covariance | Baseline |
| N, tracker covariance | The tracker's own logged covariance $P$, projected | Tested |
| NA, NIS-inflated | $\lambda P$; $\lambda=\max(1,\overline{\mathrm{NIS}}/2)$ over the track's last ($\le 3$) position innovations (2 dof); inflate-only | Tested on runs not used to design it |
| E, oracle | Squared realised prediction error along the constraint normal (matched true actor; unmatched: 0) | Positive control; a reference, not a bound |
| CK3, braking prediction | F0's $s$; the path of each tracked actor with $\hat a \ne 0$ moving faster than 0.5 m/s shifted as if braking at 3 m/s² (stop-clipped) | Simple prediction |
| AM, acceleration margin | $t^4(\sigma_a^2+\hat a^2)/4$, $\hat a$ from the track's two latest update states, $t$ the look-ahead | Simple margin |
| Q, planner allowance | $t^4\sigma_a^2/4$ ($\sigma_a$ a class constant) | Shape only |
| TG, time gap | $(r_0 + v_e)^2$ with $v_e$ the row's speed at the constraint's time and $r_0$ = 2 m/s: at $g = h^2$ a time gap $h$ with a standstill distance $h r_0$ | Spacing-policy baseline (added in revision) |

> **TABLE II.** The 3 s commitment: room *R* (percentage points) and share recovered, RR, with nominal 95% run-bootstrap percentile intervals; step frontier; each population on its own frontier, so values do not add. Shares are printed to 3 decimals, and to 4 for the tracker covariance and the planner allowance. For the tracker covariance the nominal intervals are not valid (Section V-A). Partial oracle: the oracle's margin on a random share of the decisions, the class average's elsewhere; with the ego moving and while the lead brakes it does not grade, so shares there are read as frontier distances in decisions (Section IV-B). Calibrated intervals, the convex hull, signed caution, the other phases and the phase-weighted aggregate: Tables S5, S16 and S21.

| Quantity | All | Ego moving | Lead braking |
|---|---|---|---|
| Evaluated decisions | 8,290 | 1,863 | 755 |
| Room $R$ (pp) | 5.56 [4.50, 6.60] | 10.16 [7.96, 12.39] | 15.59 [11.45, 20.04] |
| RR(N), tracker covariance | 0.0012 [−0.0011, 0.0012] | −0.0001 [−0.0058, 0.0016] | −0.0025 [−0.0048, 0.0052] |
| RR(NA), NIS-inflated | 0.017 [0.007, 0.025] | 0.016 [0.002, 0.028] | −0.006 [−0.031, 0.023] |
| RR(AM), acceleration margin | 0.376 [0.316, 0.425] | 0.293 [0.207, 0.350] | −0.044 [−0.193, 0.062] |
| RR(CK3), braking prediction | 0.831 [0.753, 0.903] | 0.472 [0.353, 0.570] | 0.606 [0.468, 0.711] |
| RR(TG), time gap | 0.314 [0.219, 0.389] | 0.168 [−0.032, 0.308] | 0.088 [−0.236, 0.357] |
| Partial oracle, 25% | 0.269 [0.222, 0.305] | −0.109 [−0.227, −0.039] | −0.682 [−0.933, −0.486] |
| Partial oracle, 50% | 0.536 [0.473, 0.582] | 0.051 [−0.120, 0.161] | −0.630 [−0.915, −0.383] |
| Partial oracle, 75% | 0.778 [0.731, 0.811] | 0.440 [0.307, 0.526] | 0.046 [−0.187, 0.227] |

> **TABLE III.** The reaction-and-stop scoring: the ego follows its row for τ, then stops at *A* with zero standstill gap; plans are judged until their stop ends. *R*: the 3 s oracle's advantage; its ratio to the 3 s room (5.56 points), and the same ratio with clearance read on the 3 s window only; den₀: the class average's avoidable wrong-go against the scoring's perfect oracle; RR₀(N): the tracker covariance's share of it. Nominal 95% intervals, not valid at their level for the tracker covariance's share (Section V-A). The ratio at other stop decelerations: Table S19; other populations and sources at τ = 0.75 s: Tables S20a–S20c; three sources at the other delays: Table S20d.

| τ (s) | $A$ (m/s²) | $R$ (pp) [95%] | Relative to 3 s [95%] | On the 3 s window only | den₀ (pp) [95%] | RR₀(N) [95%] |
|---|---|---|---|---|---|---|
| 0.5 | 6 | 0.10 [0.00, 0.30] | 0.019 [0.000, 0.052] | 0.019 | 0.11 [0.00, 0.33] | not evaluable |
| 0.75 | 6 | 0.68 [0.25, 1.17] | 0.122 [0.052, 0.188] | 0.121 | 0.71 [0.26, 1.23] | 0.000 [−0.006, 0.005] |
| 1.0 | 6 | 1.34 [0.65, 2.09] | 0.241 [0.136, 0.331] | 0.234 | 1.41 [0.68, 2.19] | 0.001 [−0.005, 0.004] |
| 1.25 | 6 | 2.14 [1.23, 3.08] | 0.384 [0.259, 0.488] | 0.364 | 2.27 [1.29, 3.26] | 0.001 [−0.003, 0.002] |
| 1.5 | 6 | 2.98 [1.90, 4.09] | 0.537 [0.405, 0.643] | 0.490 | 3.20 [2.04, 4.36] | 0.001 [−0.002, 0.001] |
| 1.8 | 6 | 4.07 [2.82, 5.29] | 0.732 [0.601, 0.829] | 0.644 | 4.37 [3.03, 5.64] | 0.001 [−0.001, 0.001] |

> **TABLE IV.** The reaction-and-stop scoring at τ = 0.75 s (stop at 6 m/s², plans judged until their stop ends) against the perfect oracle for that scoring: the class average's avoidable wrong-go den₀ and each source's share of it, RR₀, with nominal 95% intervals. Nominal intervals are not valid at their level for the tracker covariance's share (Section V-A). A share is not evaluable (n.e.) where den₀ is below 10 decision-equivalents; the point is then given in brackets. Last column: a 2 m standstill gap. The phases, the other sources and the other delays: Tables S20a–S20d; the 2 m gap by population: Table S24b.

| Quantity | All | Ego moving | Phase-weighted | All, 2 m gap |
|---|---|---|---|---|
| den₀ (pp); decision-equivalents [95%] | 0.71; 58.8 [20.9, 103.2] | 0.65; 12.2 [4.3, 21.1] | 0.045; 3.7 [0.8, 8.7] | 1.14; 94.7 [39.1, 156.2] |
| RR₀(N), tracker covariance | 0.000 [−0.006, 0.005] | −0.013 [−0.031, 0.006] | n.e. (−0.001) | −0.0008 [−0.0111, 0.0048] |
| RR₀(NA), NIS-inflated | 0.012 [−0.004, 0.039] | −0.021 [−0.057, 0.020] | n.e. (−0.035) | 0.021 [−0.004, 0.059] |
| RR₀(CK3), braking prediction | 0.936 [0.908, 0.959] | 0.038 [−0.460, 0.381] | n.e. (0.038) | 0.576 [−0.260, 0.856] |
| RR₀(AM), acceleration margin | 0.570 [0.472, 0.664] | 0.257 [0.167, 0.337] | n.e. (−0.057) | 0.801 [0.738, 0.870] |
| RR₀(TG), time gap | 0.442 [0.342, 0.547] | 0.542 [0.474, 0.589] | — | — |

> **TABLE V.** The margin-ratio check by scenario family: the tracker's margin over the class average's on every evaluated decision row where a margin binds under both; median ratio and share of rows within 5% of that median (Table S26).

| Scenario family | Runs | Decision rows | Median ratio | Rows within 5% of the median (%) |
|---|---|---|---|---|
| Lead braking | 55 | 152,264 | 1.103 | 99.26 |
| Stopped vehicle | 55 | 121,685 | 1.103 | 98.73 |
| Cut-in | 20 | 90,227 | 1.102 | 99.86 |
| Benign driving | 20 | 40,120 | 1.093 | 60.45 |
| Pedestrian crossing | 51 | 157,972 | 0.883 | 8.51 |
| Vehicle crossing | 22 | 42,122 | 0.915 | 4.09 |

