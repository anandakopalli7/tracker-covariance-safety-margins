> **TABLE S30.** The grid placebo and the gridless frontier (3 s commitment, step frontier). Grid: the 202 swept scales of record. P: the class average with its critical scales divided by 1.1029², which selects at every scale as the class average does at a scale 1.1029² larger and so carries no information beyond it. RR(N) − RR(P): the tracker covariance against that placebo. Gridless: every margin scale in [0, 10³] at which a selection changes. Grid columns: the draw of record (20,000 run resamples); gridless intervals: its first 2,000 resamples; 95% percentile intervals, basic intervals in parentheses for the pooled tracker covariance. D: frontier distance in decision-equivalents (positive: below the class average).

| Population | Decisions | Grid: RR(N) | Grid: RR(P) | Grid: RR(N) − RR(P) | Grid: D(N) − D(P) | Gridless: RR(N) | Gridless: D(N) |
|---|---|---|---|---|---|---|---|
| All | 8,290 | 0.0012 [−0.0011, 0.0012] (basic [0.0012, 0.0035]) | 0.0015 [−0.0007, 0.0015] | −0.0003 [−0.0009, 0.0001] | −0.12 [−0.43, 0.04] | −0.0004 [−0.0008, 0.0001] (basic [−0.0009, −0.0001]) | −0.19 [−0.34, 0.02] |
| Ego moving | 1,863 | −0.0001 [−0.0058, 0.0016] | 0.0022 [−0.0029, 0.0023] | −0.0023 [−0.0050, 0.0006] | −0.44 [−0.93, 0.11] | −0.0023 | −0.43 |
| Before onset | 678 | 0.0051 [−0.029, 0.021] | 0.0051 [−0.030, 0.020] | 0.0000 [−0.0020, 0.0065] | 0.00 [0.00, 0.02] | 0.0017 | 0.00 |
| Lead braking | 755 | −0.0025 [−0.0048, 0.0052] | −0.0014 [−0.0047, 0.0053] | −0.0010 [−0.0016, 0.0015] | −0.12 [−0.19, 0.18] | 0.0002 | 0.02 |
| Lead stopped | 6,857 | 0.0019 [−0.0045, 0.0043] | 0.0028 [−0.0031, 0.0054] | −0.0010 [−0.0033, −0.0001] | −0.05 [−0.18, 0.00] | −0.0009 | −0.05 |

> **TABLE S30b.** Other sources on the gridless frontier (3 s commitment, all evaluated decisions; first 2,000 resamples of the draw of record), beside the grid values of record.

| Quantity | Grid (of record) | Gridless |
|---|---|---|
| Room $R$ (pp) | 5.56 | 5.51 [4.45, 6.54] |
| RR(NA), NIS-inflated | 0.017 | 0.015 [0.0069, 0.024] |
| RR(AM), acceleration margin | 0.376 | 0.382 [0.324, 0.434] |
| RR(CK3), braking prediction | 0.831 | 0.837 [0.756, 0.909] |
| RR(Q), planner allowance | −0.0018 | −0.0024 [−0.0059, 0.0010] |
| RR(P), placebo | 0.0015 | 0.0000 [0.0000, 0.0000] |

> **TABLE S30c.** Grid jitter: the class average with its critical scales divided by 10^(0.025 u), a fraction u of one grid step, scored as a source (3 s commitment, all evaluated decisions, points). Such a source carries no information beyond the class average.

| u | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.45 | 0.50 |
|---|---|---|---|---|---|---|---|---|---|---|
| RR | 0.0002 | 0.0005 | 0.0006 | 0.0010 | 0.0010 | 0.0010 | 0.0012 | 0.0015 | 0.0017 | 0.0011 |
| u | 0.55 | 0.60 | 0.65 | 0.70 | 0.75 | 0.80 | 0.85 | 0.90 | 0.95 | 1.00 |
| RR | 0.0015 | 0.0017 | 0.0011 | 0.0014 | 0.0013 | 0.0011 | 0.0009 | 0.0006 | 0.0000 | 0.0000 |

> **TABLE S31.** Monte Carlo error of the calibrated levels of Table S16 (3 s commitment, all evaluated decisions, step frontier, grid). Calibrated level: the smallest nominal level at which the percentile interval covers the full-sample value in at least 95% of the 2,000 outer samples. Inner seed 20261121 repeats Table S16; 20261126 repeats the double bootstrap with new inner resamples. Monte Carlo spread: 2,000 resamples of the outer samples (2.5%, 50% and 97.5% points; standard deviation).

| Statistic | Calibrated level, inner seed 20261121 | Spread [2.5%, 50%, 97.5%]; SD | Calibrated level, inner seed 20261126 | Spread [2.5%, 50%, 97.5%]; SD |
|---|---|---|---|---|
| Room $R$ | 0.9640 | [0.9560, 0.9640, 0.9700]; 0.0043 | 0.9640 | [0.9580, 0.9640, 0.9720]; 0.0044 |
| RR(N) | 0.9960 | [0.9960, 0.9960, 0.9980]; 0.0005 | 0.9960 | [0.9960, 0.9960, 0.9960]; 0.0002 |

> **TABLE S31b.** Subsampling with an estimated rate (Bertail, Politis and Romano [S1]): m = 10, 15, 20, 25 of the 35 runs without replacement, 2,000 subsamples each. β: the rate estimated from the interquartile range of the subsample values against m. Intervals at m = 20 with the finite-population factor, the same with β = 1/2 beside them, and both in decision-equivalents (converted at the full-sample room). Amendment 09 also named D(N) in decision-equivalents; that statistic is a total that grows with the number of runs in a subsample, so its subsampling root is not centred, and it is not reported (a deviation).

| Statistic | β estimated | Interval, estimated β | Interval, β = 1/2 | Decision-equivalents, estimated β | Decision-equivalents, β = 1/2 |
|---|---|---|---|---|---|
| RR(N), grid | 0.33 | [0.0013, 0.0040] | [0.0013, 0.0038] | [0.60, 1.86] | [0.59, 1.74] |
| RR(N), gridless | 0.69 | [−0.0009, −0.0002] | [−0.0010, −0.0002] | [−0.42, −0.10] | [−0.44, −0.09] |

> **TABLE S31c.** The bound of Section V-A: every 95% interval of the tracker covariance's frontier distance from the class average, in decision-equivalents of the 8,290 evaluated decisions (intervals of RR(N) converted at the full-sample room of 460.7 decision-equivalents). The bound is the largest absolute end, rounded up to one decimal.

| Interval | Decision-equivalents |
|---|---|
| Table S16: percentile | [−0.50, 0.55] |
| Table S16: basic | [0.57, 1.62] |
| Table S16: calibrated (99.6%) | [−0.74, 0.76] |
| Table S17: stratified by recording setting | [−0.48, 0.55] |
| Table S17: five short runs left out | [−0.51, 0.56] |
| Table S17: subsampling m = 15 | [0.52, 1.51] |
| Table S17: subsampling m = 20 | [0.60, 1.76] |
| Table S17: subsampling m = 25 | [0.63, 2.16] |
| Table S30: grid, D(N) percentile | [−0.51, 0.54] |
| Table S30: gridless, D(N) percentile | [−0.34, 0.02] |
| Table S31b: grid, estimated rate | [0.60, 1.86] |
| Table S31b: grid, rate 1/2 | [0.59, 1.74] |
| Table S31b: gridless, estimated rate | [−0.42, −0.10] |
| Table S31b: gridless, rate 1/2 | [−0.44, −0.09] |
| **Largest absolute end** | **2.16** (Table S17: subsampling m = 25) |

> **TABLE S32.** One class-average margin scale per phase of the lead's motion, in sample and out of sample (3 s commitment, all evaluated decisions; shares of the room of record, 5.56 points). In sample: the frontier over all scale triples (Table S23). Held out: per caution level, the triple (or the single scale) with the lowest wrong-go on the training runs, applied to the left-out runs (a level at which some fold has no qualifying choice gives no point); like for like: against a single scale chosen the same way; against the single-scale frontier of record. Five-fold: 5-fold cross-validation on the full sample; interval from 200 resamples of the draw of record, each cross-validated over its own runs. Estimated phase: from the lead track's own speed and acceleration estimate (stopped at most 0.5 m/s; braking above it with an acceleration estimate at most the threshold).

| Phase labels | In sample | Held out, like for like (leave one run out) | Held out, like for like (five-fold) | Held out against the single scale of record (leave one run out) | Agreement with the truth phase |
|---|---|---|---|---|---|
| Logged truth | 0.893 | 0.903 | 0.885 [0.81, 1.00] | 0.868 | — |
| Tracker estimate, threshold −1.0 m/s² | 0.984 | 0.999 | — | 0.964 | 95.6% |
| Tracker estimate, threshold −0.5 m/s² | 0.980 | 0.996 | — | 0.960 | 96.1% |
| Tracker estimate, threshold −2.0 m/s² | 0.968 | 0.980 | — | 0.944 | 94.2% |

> **TABLE S33.** Where the room and the sources' gains lie (3 s commitment, step frontier, grid): the frontier difference against the class average split exactly into per-decision contributions (at each caution level, the frontier points' wrong-go flags), in decision-equivalents, by time since the lead's stop. "All": the pooled population; "Lead stopped": decisions after the stop, on their own frontier. Decisions: the number in each bin.

| Population | Source | Total | before stop | 0-1 s | 1-2 s | 2-5 s | 5-10 s | >=10 s |
|---|---|---|---|---|---|---|---|---|
| All | Decisions | 8,290 | 1,433 | 300 | 300 | 900 | 1,500 | 3,857 |
| All | E, oracle (the room) | 460.7 | 419.1 | 41.7 | −0.14 | 0.00 | 0.00 | 0.00 |
| All | CK3, braking prediction | 383.0 | 345.9 | 37.4 | −0.27 | 0.00 | 0.00 | 0.00 |
| All | AM, acceleration margin | 173.1 | 143.2 | 30.0 | −0.10 | 0.00 | 0.00 | 0.00 |
| All | N, tracker covariance | 0.56 | 0.42 | 0.14 | 0.00 | 0.00 | 0.00 | 0.00 |
| Lead stopped | Decisions | 6,857 | 0 | 300 | 300 | 900 | 1,500 | 3,857 |
| Lead stopped | E, oracle (the room) | 56.3 | 0.00 | 56.1 | 0.15 | 0.00 | 0.00 | 0.00 |
| Lead stopped | CK3, braking prediction | 55.9 | 0.00 | 55.9 | 0.00 | 0.00 | 0.00 | 0.00 |
| Lead stopped | AM, acceleration margin | 39.5 | 0.00 | 39.7 | −0.16 | 0.00 | 0.00 | 0.00 |
| Lead stopped | N, tracker covariance | 0.10 | 0.00 | 0.10 | 0.00 | 0.00 | 0.00 | 0.00 |

> **TABLE S33b.** The after-stop frontier differences of Table S33 by the tracker's estimate of the lead's speed at the decision (the true speed is zero in this phase), in decision-equivalents.

| Source | <=0.5 m/s | 0.5-1 m/s | 1-2 m/s | >2 m/s |
|---|---|---|---|---|
| Decisions | 6,725 | 53 | 43 | 36 |
| E (the room) | 4.1 | 6.7 | 18.6 | 26.9 |
| CK3 | 0.01 | 8.3 | 20.8 | 26.8 |
| AM | 1.7 | 4.8 | 14.1 | 18.9 |
| N | 0.03 | −0.01 | 0.01 | 0.08 |

> **TABLE S34.** The lead track's estimated state at the decision (evaluated decisions; median [25%, 75%]): the tracker's lead speed and the true one; the track's acceleration estimate along its velocity; the constant-velocity-predicted minus the true longitudinal position of the lead centre 1 s and 3 s after the decision (positive: the lead is predicted further ahead than it is); the ego's speed.

| Decisions | n | Tracker speed (m/s) | True speed (m/s) | Acceleration estimate (m/s²) | Predicted − true at 1 s (m) | at 3 s (m) | Ego speed (m/s) |
|---|---|---|---|---|---|---|---|
| Before onset | 678 | 9.63 [4.77, 12.95] | 9.75 [4.93, 13.36] | 0.06 [−0.17, 0.24] | −0.23 [−0.62, 0.39] | 6.21 [2.56, 9.21] | 10.00 [4.78, 13.42] |
| Lead braking, since onset 0–1 s | 334 | 8.81 [4.36, 10.04] | 6.52 [3.53, 9.70] | −0.61 [−1.46, −0.05] | 2.70 [2.00, 3.61] | 13.74 [10.78, 19.29] | 9.10 [3.89, 10.00] |
| Lead braking, since onset 1–2 s | 189 | 7.39 [5.23, 10.73] | 5.30 [2.68, 9.61] | −3.05 [−3.81, −2.39] | 3.78 [2.92, 5.00] | 16.86 [14.03, 19.20] | 10.00 [8.67, 13.70] |
| Lead braking, since onset ≥ 2 s | 232 | 5.31 [3.33, 7.75] | 3.97 [2.10, 6.21] | −2.91 [−3.72, −2.41] | 2.98 [2.36, 3.66] | 13.54 [9.24, 16.52] | 9.02 [6.54, 11.89] |
| After the stop, 0–1 s | 300 | 0.45 [0.18, 1.05] | 0.00 [0.00, 0.00] | −2.91 [−3.87, −1.50] | 0.58 [0.16, 1.30] | 1.49 [0.54, 3.51] | 3.13 [1.86, 4.56] |
| After the stop, 1–2 s | 300 | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | −0.12 [−0.34, 0.01] | −0.15 [−0.22, −0.07] | −0.14 [−0.22, −0.03] | 0.01 [0.00, 1.87] |
| After the stop, 2–5 s | 900 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | −0.28 [−0.35, −0.23] | −0.28 [−0.36, −0.23] | 0.00 [0.00, 0.00] |
| After the stop, 5–10 s | 1,500 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | −0.30 [−0.38, −0.24] | −0.30 [−0.38, −0.24] | 0.00 [0.00, 0.00] |
| After the stop, ≥ 10 s | 3,857 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | −0.30 [−0.38, −0.25] | −0.30 [−0.38, −0.25] | 0.00 [0.00, 0.00] |

> **TABLE S34b.** Consistency of the lead track by phase: mean normalised innovation squared of the position block over the track's distinct updates (2 degrees of freedom; a consistent filter averages 2), and the mean and median normalised error of the velocity that the planner uses at the decision, against the true velocity, with the logged velocity block (2 degrees of freedom).

| Phase | Updates | Mean NIS | Decisions | Mean velocity NEES | Median velocity NEES |
|---|---|---|---|---|---|
| Before onset | 151 | 0.50 | 678 | 2.06 | 1.28 |
| Lead braking | 150 | 1.47 | 755 | 5.08 | 3.70 |
| Lead braking, first 1 s | 66 | 0.68 | 334 | 4.34 | 3.05 |
| After stop | 1,383 | 0.10 | 6,857 | 0.09 | 0.00 |
| After stop, first 2 s | 120 | 0.77 | 600 | 0.99 | 0.01 |

> **TABLE S35.** The tuning runs beside the evaluation runs (3 s commitment, step frontier, points; each population on its own frontier). Tuning runs were recorded with a fixed recording margin (α = 0.105, a unit variance in place of the tracker's covariance); evaluation runs with the tracker's covariance (α = β = 1.642–7.550). Per-phase gain: in sample, as a share of the pooled room (Table S23's definition).

| Quantity | Tuning runs | Evaluation runs |
|---|---|---|
| Runs; evaluated decisions | 20; 3,018 | 35; 8,290 |
| Decisions before onset / lead braking / lead stopped | 378 / 279 / 2,361 | 678 / 755 / 6,857 |
| Share after the stop; share with the ego at or below 0.5 m/s | 78.2%; 70.3% | 82.7%; 77.5% |
| Room $R$, all (pp; decision-equivalents) | 1.18; 35.6 | 5.56; 460.7 |
| Room $R$, ego moving (pp; decision-equivalents) | 4.05; 36.4 | 10.16; 189.4 |
| Room $R$, before onset (pp; decision-equivalents) | 0.07; 0.27 | 0.43; 2.9 |
| Room $R$, lead braking (pp; decision-equivalents) | 10.14; 28.3 | 15.59; 117.7 |
| Room $R$, lead stopped (pp; decision-equivalents) | 1.20; 28.3 | 0.82; 56.3 |
| Pooled room over the decision-weighted phase rooms | 0.63 | 2.60 |
| Per-phase gain, in sample (share of the pooled room) | 0.632 | 0.893 |
| RR(CK3): all / lead braking / lead stopped | 0.377 / 0.301 / 0.937 | 0.831 / 0.606 / 0.993 |
| RR(AM): all / lead braking / lead stopped | 0.245 / 0.063 / 0.063 | 0.376 / −0.044 / 0.702 |
| RR(NA): all / lead braking / lead stopped | 0.063 / 0.080 / −0.0016 | 0.017 / −0.0064 / 0.079 |
| RR(N): all / lead braking / lead stopped | 0.0022 / 0.0035 / −0.0011 | 0.0012 / −0.0025 / 0.0019 |

> **TABLE S36.** Reliance on the stop (reaction-and-stop scoring: τ = 0.75 s, 6 m/s², plans judged until their stop ends). At each caution level, each source's frontier point under this scoring; the share of the population's decisions whose selected row is unsafe if followed for 3 s but safe with the stop, averaged over the levels. O: the scoring's perfect oracle (its one selection).

| Population | Decisions | F0 | N | NA | AM | CK3 | E | O |
|---|---|---|---|---|---|---|---|---|
| All | 8,290 | 5.8% | 5.8% | 5.7% | 4.7% | 3.3% | 0.6% | 72.3% |
| Ego moving | 1,863 | 19.0% | 19.2% | 18.7% | 17.8% | 15.3% | 0.9% | 51.6% |
| Before onset | 678 | 5.0% | 5.0% | 5.0% | 5.0% | 5.0% | 5.0% | 5.0% |
| Lead braking | 755 | 41.7% | 42.2% | 41.0% | 37.9% | 40.5% | 65.7% | 70.2% |
| Lead stopped | 6,857 | 1.2% | 1.2% | 1.2% | 0.7% | 0.4% | 0.3% | 79.1% |

> **TABLE S36b.** Caution counted under the reaction-and-stop scoring (τ = 0.75 s, 6 m/s², judged until the stop ends): the oracle row and the truly safe set of the caution measure taken from this scoring instead of the 3 s commitment. den₀ in decision-equivalents and RR₀ with 95% intervals (draw of record), beside the values of record (Table IV).

| Quantity | All | Ego moving |
|---|---|---|
| den₀ (decision-equivalents) | 53.8 [19.4, 92.9] | 12.8 [4.7, 22.0] |
| RR₀(N) | −0.0006 [−0.0061, 0.0056] | −0.013 [−0.022, 0.0071] |
| RR₀(NA) | 0.0078 [−0.0069, 0.036] | −0.041 [−0.067, 0.0023] |
| RR₀(AM) | 0.545 [0.447, 0.636] | 0.095 [−0.018, 0.193] |
| RR₀(CK3) | 0.829 [0.769, 0.868] | −0.867 [−1.474, −0.444] |

> **TABLE S37.** A constant time-gap margin scored like every source: along every constraint, $s = (r_0 + v_e)^2$ with $v_e$ the row's speed at the constraint's time, so that at $g = h^2$ a row is feasible when every clearance is at least $h(r_0 + v_e)$: a time gap $h$ and a standstill distance $h r_0$. $r_0$ = 2 m/s (1 and 4 m/s beside it). 3 s commitment: RR with 95% intervals (draw of record); reaction-and-stop (τ = 0.75 s, 6 m/s², judged until the stop ends): RR₀. The braking prediction and the acceleration margin, scored in the same program, beside them.

| Quantity | TG, $r_0$ = 2 | TG, $r_0$ = 1 | TG, $r_0$ = 4 | CK3 | AM |
|---|---|---|---|---|---|
| RR, all | 0.314 [0.219, 0.389] | 0.387 | 0.213 | 0.831 | 0.376 |
| RR, ego moving | 0.168 [−0.032, 0.308] | 0.185 | 0.116 | 0.472 | 0.293 |
| RR, before onset | −0.481 [−3.114, 0.253] | −0.726 | −0.259 | −0.536 | −0.128 |
| RR, lead braking | 0.088 [−0.236, 0.357] | 0.053 | 0.093 | 0.606 | −0.044 |
| RR, lead stopped | 0.161 [0.056, 0.268] | 0.185 | 0.066 | 0.993 | 0.702 |
| RR₀ at τ = 0.75 s, all | 0.442 [0.342, 0.547] | 0.487 | 0.354 | 0.936 | 0.570 |
| RR₀ at τ = 0.75 s, ego moving | 0.542 [0.474, 0.589] | 0.595 | 0.452 | 0.038 | 0.257 |

> **TABLE S38.** The grading check in the population before the lead's stop (Table S22, T = 0: before onset and while the lead brakes; 3 s commitment, step frontier, points; Addendum 01 to Amendment 09). Partial oracles: the oracle's critical values on a random share of the decisions and the class average's elsewhere, for the draw of record and over 50 further draws (mean [min, max]). Below: the braking prediction's and the acceleration margin's shares and frontier distances in decision-equivalents.

| Quantity | 25% | 50% | 75% |
|---|---|---|---|
| Partial oracle, draw of record | −0.365 | −0.258 | 0.232 |
| Partial oracle, 50 draws: mean [min, max] | −0.326 [−0.423, −0.228] | −0.221 [−0.364, −0.088] | 0.243 [0.081, 0.374] |

| Source | Share | Frontier distance (decision-equivalents of 1,433) |
|---|---|---|
| CK3, braking prediction | 0.289 | 35.5 |
| AM, acceleration margin | 0.434 | 53.4 |

