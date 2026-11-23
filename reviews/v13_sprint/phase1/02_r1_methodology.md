# Phase 1, Seat 2: Peer Reviewer 1 (Methodology)

- **Seat:** Peer Reviewer 1 (Methodology), Card 2
- **Model:** Claude Fable 5.2
- **Freeze folder:** `ARS_TRIAL\revision_v13\work\A_text\out\freeze_v13_2002\`
- **SHA-256 of MANUSCRIPT_v13.md as read:** `93541ff6b1592bbdfc9b5f239fd81e8537fa3f433a3e2a76ba43a242914a4ead`
- **Also read:** SUPPLEMENT_v13.md (S2, S3, S14), AMENDMENT_11_v13.md, the three A11 lock headers, the exports, and the X, DR and Y calibration records.

## Recommendation

**Minor revision** (confidence 4 of 5). The confirmatory sequences are reported as registered: pass rules, levels, labels and locks agree with the plans, and all 30 printed values I checked match their sources. The remaining problems are wording. The dropout result carries two unregistered readings, and the abstract and conclusion disclose post-hoc status unevenly.

## Compliance with the pre-registrations

| Sequence | Pass rule and level as registered? | Label correct? | Post-hoc status disclosed? |
|---|---|---|---|
| Lead braking H0–H5 | Yes. N's share is at its calibrated level 0.994, the IMM's share at nominal 99%, the others at nominal 95% | Yes | n/a |
| Cut-in, real logs | Yes. Room failed; later steps "n.t." | Yes | Clearance change disclosed |
| X0–X2 (crossing) | Yes. Room, share and excess at 95% (estimated coverage 0.956, 0.943, 0.947); the oracle at the 99% fallback (coverage 0.923; calibrated level 0.972 failed the Monte Carlo SD check, 0.0035 > 0.002) | Yes: "uninformative variation" | No-go departure in V-E and Table S5; not in the abstract |
| DR0–DR2 (dropouts) | Yes. All four statistics at 95% (coverage 0.946, 0.9425, 0.950, 0.945) | Yes: "recovers", efficiency reported | In V-E and Table S5; not in the abstract. The output-rule change (punish_num = 3) is disclosed |
| Y1 | Yes. 95%, coverage 0.9485 | Yes | In the abstract, V-E and Table S36 |
| E4 | Yes. Lower level is the hypothesis, higher level secondary | Yes | "Not caution-matched" in the abstract, V-E and VII |
| B1r | Class "recovers" by the H3 rule, flag "barely varies"; the registered IMM result stays confirmatory | Yes | In V-B and Table S5 |

Lock times (LOCK_A11 14:23, LOCK_A11b 14:48, LOCK_A11c 15:09 EST) precede the result files (DR 16:40, Y 17:27, X 19:30 EST).

## Findings

**1. MAJOR. "Inside the equivalence margin" for the dropout share is unregistered and holds by 0.0004.**
*Location:* Abstract ("a confirmed but small 2.8% of the room (inside the equivalence margin)"); Section V-E; Section VII.
*Problem:* DR2 is a classification (A11 §6c.6), and its consequence rule (§6c.11) prints the class, r, c and r/c. No equivalence test was registered for DR. The interval's upper end is 0.04965 against δ = 0.05, at a nominal 95% level whose estimated coverage is 0.945; against the class average of record it is 0.0498. Any widening crosses δ. Next to "confirmed", the parenthesis reads as a confirmed equivalence.
*Fix:* Abstract: "a confirmed but small 2.8% [0.6%, 5.0%] of the room". V-E: "recovers 0.0283 [0.0064, 0.0496] of it (descriptively, the upper end lies just below δ = 0.05; no equivalence test was registered here)". Delete the parenthesis in Section VII.

**2. MAJOR. The main text does not say that the dropout gain is not found inside the dropouts.**
*Location:* Section V-E, "We read the bottleneck in both as the information in the covariance, not its amplitude"; Table S34.
*Problem:* The plan motivated DR by a covariance that grows while the tracker coasts (A11 §6c.1). Table S34 shows that the covariance's share among decisions inside a dropout is −0.003 [−0.020, 0.015]; with the gap row added the export gives 0.030 [−0.003, 0.063]; the output rule alone gives −0.0006. The confirmed 2.8% is therefore a pooled result whose source is not located, while the heading "Where the Covariance Varies" invites the opposite reading. The "bottleneck" sentence is also the registered wording for class (b), which applies to crossing; DR is class (a).
*Fix:* Add to V-E: "Among the 3,644 decisions inside a dropout its share is −0.003 [−0.020, 0.015] (descriptive; Table S34), so the pooled gain is not shown to come from the coasting covariance." Restrict the "bottleneck" sentence to crossing; for dropouts say "its efficiency against its oracle is 0.071".

**3. MINOR. The abstract and conclusion disclose post-hoc status for Y only.**
*Location:* Abstract; Section VII.
*Problem:* DR is called "confirmed" with no note that it was specified after the fresh lead-braking results were seen and that it re-scores those same runs. The crossing test carries no note of the no-go departure. Both are disclosed in V-E and Table S5.
*Fix:* Abstract: "under detection dropouts (specified after the fresh results were seen, on the same runs)". Add "(tested despite a pre-stated no-go)" in Section VII or contribution 2.

**4. MINOR. No statement on multiplicity across sequences.**
*Location:* Section IV-E.
*Problem:* A11 §3.5 says no adjustment is made across families "and this is stated". Neither file states it. There are now eight sequences. The one positive result for the fixed-noise covariance (DR2, lower end 0.0064, roughly z = 2.6) would be borderline under a familywise correction.
*Fix:* Add: "Sequences are not adjusted for one another; each controls its own error rate at 0.025."

**5. MINOR. "Varied without rank information" overstates the crossing class.**
*Location:* Section VII; abstract ("recovers none").
*Problem:* Class (b) means that the share's lower end is not above zero while the oracle's is above δ. The share is −0.067 [−0.221, 0.034], which is not inside ±δ, and no permuted-twin test of N was run in crossing (as Y did for the adaptive filter). Absence of rank information is not shown; an upper bound is.
*Fix:* "it showed no recovery of the room (share −0.07 [−0.22, 0.03]; its oracle: 69%)".

**6. MINOR. "(confirmed)" after a share is ambiguous in V-E.**
*Location:* V-E, "its own share is −0.067 [−0.221, 0.034] (confirmed)".
*Problem:* What is confirmed is the classification, not a value. The second hypothesis of each sequence (detection at the tracker's amplitude: 0.591 [0.382, 0.941] and 0.253 [0.214, 0.296]) is not in the main text, although "confirmed" for the third depends on it.
*Fix:* "(classified as uninformative variation; confirmed)", and add "detection at its amplitude passed (Tables S33, S34)".

**7. MINOR. E4 lower level: the margin is met only before rounding, and the progress cost is not printed.**
*Location:* V-E; Table S35 ("−0.03 [−0.10, 0.03]", "equivalent").
*Problem:* The lower end is −0.0969 against the rule −0.10 < L; printed to two decimals it equals the margin. The time-lost interval, 0.15 [0.08, 0.24] s, excludes zero: the covariance arm is slower, inside ±0.5 s. The main text gives the class with no numbers, and not the contact shares (23% against 27%).
*Fix:* Print the contact interval to three decimals in Table S35, and add to V-E: "(contact difference −0.033 [−0.097, 0.027]; time lost 0.15 [0.08, 0.24] s)".

**8. MINOR. The calibration rule tolerates coverage between 0.94 and 0.95.**
*Location:* Section IV-D; Supplement S2.
*Problem:* Several confirmatory statistics keep nominal 95% with estimated coverage 0.9425 to 0.946, so "one-sided at 0.025" is approximate.
*Fix:* Add the estimated coverage of each nominal 95% interval to Tables S32–S34 and S36, or one sentence in S14.

**9. MINOR. Y's "confirmed" label for a nearly foregone test.**
*Location:* V-E; Table S32.
*Problem:* When Y was written, the filter's share (0.046 [0.039, 0.053]) had been seen, and a permuted twin is expected near zero, so the outcome was largely implied.
*Fix:* "(passed its test, specified post hoc)" in place of "(confirmed)" for Y.

## Values checked against sources

| # | Printed value | Location | Source key | Match |
|---|---|---|---|---|
| 1 | Room 5.58 [4.99, 6.17] | Abstract, Table II | C: LB.R, LB.R.ci | yes |
| 2 | N share [−0.0009, 0.0015] | Abstract, Table II | C: LB.RR_N.ci (level 0.994) | yes |
| 3 | E5 0.013 [0.010, 0.015] | Table II | C: LB.RR_E5 | yes |
| 4 | E5 − E5p 0.008 [0.006, 0.010] | Table II | C: LB.RR_E5mP | yes |
| 5 | CK3 0.783 [0.720, 0.842] | Table II | C: LB.RR_CK3 | yes |
| 6 | PS 0.916 [0.864, 0.965]; like for like 0.918 | Table II, V-A | C: LB.PS.rec, LB.PS.like | yes |
| 7 | Partial oracles 0.261 / 0.514 / 0.754 | Table II | C: LB.PO25/50/75 | yes |
| 8 | IMM r 0.0000 [−0.0018, 0.0012]; c 0.0009 [0.0006, 0.0010] | Table II | C: LB.IMM.r (level 0.99), LB.IMM.c | yes |
| 9 | Room 5.58 / 4.99 / 4.75; 5.31 / 5.07 with latency | V-D, Table V | C: B7.2.0.R, B7.5.0.R, B7.10.0.R, B7.5.0.1.R, B7.10.0.1.R | yes |
| 10 | 21,574 decisions | V-A | C: LB.n_dec | yes |
| 11 | Crossing room 0.16 [0.11, 0.23] | Abstract, V-E | X: X.PC.R (level 0.95) | yes |
| 12 | Crossing oracle 0.695 [0.531, 0.899], nominal 99% | V-E, S33 | X: X.PC.RR_E5N, .level = 0.99 | yes |
| 13 | Crossing N −0.067 [−0.221, 0.034] | V-E | X: X.PC.RR_N | yes |
| 14 | 11.3% within 5%; 390 runs; 105,419 decisions; 170.5 | V-E, S33 | X: within5, n_runs, n_dec, R.dec | yes |
| 15 | Oracle minus twin 0.591 [0.382, 0.941] | S33 | X: X.PC.RR_E5NmP | yes |
| 16 | Dropout room 5.63 [5.03, 6.23] | Abstract, V-E | DR: DR.R | yes |
| 17 | Dropout N 0.0283 [0.0064, 0.0496] | V-E | DR: DR.RR_N | yes |
| 18 | Dropout oracle 0.398 [0.315, 0.473] | V-E | DR: DR.RR_E5N | yes |
| 19 | Efficiency 0.071 [0.016, 0.129] | V-E | DR: DR.eff | yes |
| 20 | 80.5% within 5%; 3,644 in a dropout | V-E, S34 | DR: within5, n_in_dropout | yes |
| 21 | In-dropout N −0.003 [−0.020, 0.015] | S34 | DR: DR.in.RR_N | yes |
| 22 | Output rule alone 5.59; −0.0006 [−0.0019, 0.0006] | S34 | DR: DR.ref3.* | yes |
| 23 | Twin difference 0.0498 [0.0424, 0.0569] | Abstract, V-E | Y: Y.delta | yes |
| 24 | Twin −0.0039 [−0.0089, 0.0016]; reference 0.0003 [−0.0001, 0.0011] | S36 | Y: Y.RR_B2p, Y.ref.delta | yes |
| 25 | E4 N, lower level: −0.03 [−0.10, 0.03]; 0.15 [0.08, 0.24]; equivalent | S35 | E4: E4.N.lo.dc, .dt, E4H1 | yes (see finding 7) |
| 26 | E4 IMM, lower level: −0.02 [−0.07, 0.04]; 0.08 [0.05, 0.12] | S35 | E4: E4.NIMM.lo.* | yes |
| 27 | E4 higher level: contacts 5% against 15%; −0.10 [−0.20, −0.02] | V-E, S35 | E4: E4.N.hi.contact, E4.F0.hi.contact, E4.N.hi.dc | yes |
| 28 | Closed loop N: −0.02 [−0.08, 0.04]; 0.02 [0.00, 0.04] | Table IV | E: E3.N.lo.dc, .dt | yes |
| 29 | Closed loop CK3: −0.20 [−0.32, −0.10]; 0.16 [0.10, 0.22] | Table IV | E: E3.CK3.lo.* | yes |
| 30 | Re-tuned IMM 0.0055 [0.0040, 0.0067]; c 0.0048 [0.0038, 0.0056]; 99.4% | V-B, Table III | B: B.IMMr.RR, .c, .within5 | yes |

30 of 30 match. The three amendment lock hashes printed in Section IV-E equal the `lock_sha256` fields of the X/Y, E4 and DR exports.

## Strengths

- Every sequence's pass rule, order and interval level can be traced from the manuscript to the plan and to a calibration record. The 99% fallback is named where it is used, with its cause in Table S5.
- Table S5 is an unusually complete register of deviations, with what was known at each decision.
- "Recovers" results come with size, interval, oracle and efficiency, and the supplement prints the rows that weaken the paper's own reading (Table S34).

## Score

**7.5 / 10.** Reporting fidelity to the plans is high and the numbers reproduce. It is held down by the two unregistered readings of the dropout result and by uneven post-hoc disclosure in the abstract and conclusion.
