# Peer Review Report: Reviewer 3 (Cross-disciplinary / Practical)

- Seat: Peer Reviewer 3 (R3), cross-disciplinary / practical perspective. Identity: automated-driving safety-assurance practitioner (adaptive cruise control and emergency braking, scenario-based testing, regulation and responsibility-sensitive models).
- Model: Claude Fable 5.2 (model id claude-fable-5-2).
- Date: 21 November 2026.
- Manuscript: "Do Fixed-Noise and Interacting-Multiple-Model Tracker Covariances Improve Planning Decisions? An Equal-Caution Test on Fresh Simulation Runs, in Closed Loop and on Real Driving Logs" (MANUSCRIPT_v13, SUPPLEMENT_v13, Figs. 1-4), read as a fresh submission to IEEE OJ-ITS.
- Materials read: the manuscript, the supplement and the four figures, in full. Nothing else. No reference was looked up; anything I say about a standard or regulation is from memory and marked "to verify".
- Calibration status: NOT_CALIBRATED.

## 1. Recommendation

**Major Revision.** Confidence 4 of 5 (core expertise for closed-loop reading, operating points, standards use and stakeholder scope; I did not assess the bootstrap calibration or the tracker tuning).

The open-loop null for the fixed-noise covariance is carefully scoped and a safety engineer can use it as stated. The closed-loop part, which is what a designer or assessor will act on, is weaker than its wording: the baseline operates in full braking for more than half of its decisions and still makes contact in one case in five, the cost side of "safer at no extra cost" is a time-lost measure that can hardly differ when every lead stops, and nothing in any test bed stands behind the ego. The Discussion then draws an inference from closed loop ("supports the 3 s reading") that the paper's own time-gap arm contradicts. Most fixes are wording and moving existing supplement values into the main text; one new closed-loop operating point would settle the largest issue.

## 2. Strengths

S1. **The paper refuses to turn a null into a design recommendation.** "None of this justifies removing a covariance margin from a deployed stack" (Section VI, Limits), repeated in the Abstract and the Conclusion, with the reason given in Section VI that the equal-caution sweep "removes any global scale". From a safety-assurance view this is the correct reading: the test isolates per-decision variation and says nothing about the protective value of the margin's absolute size.

S2. **The costs behind non-braking leads were measured and are printed, in open loop and closed loop.** Section V-D, Table V and Supplement Tables S19, S25, S26. Many papers that find a braking prediction helpful behind braking leads never run the leads that do not brake. The abstract carries the cost.

S3. **Regulation-derived numbers are used as nominal parameters with an explicit disclaimer and a sensitivity sweep.** Section II ("claiming no compliance"), Section IV-A ("as nominal parameters"), Supplement Table S14 (reaction time 0.5 to 1.8 s; deceleration 4, 5, 6 and 7.6 m/s²; a 2 m standstill gap). The braking prediction is also correctly distinguished from a Responsibility-Sensitive Safety bound (Section II: "a nominal prediction, not such a bound").

S4. **Dependence of the open-loop room on update rate, latency and commitment is quantified, not just listed.** Section V-D, Table V, Fig. 4, Supplement Tables S14 and S16. The statement that the after-stop room is "largely a consequence of the 2 Hz update" is exactly what a practitioner needs to avoid over-reading the 0.783 share.

S5. **The real-log failure is reported as a failure, with the planned outcome printed beside the changed one.** Section III-C, Table II dagger note, Supplement Table S27 (planned clearance: room 0.00 at 3 s). The paper does not present the nuScenes result as a replication.

S6. **The ground-truth-free margin-ratio check is a usable field diagnostic.** Supplement S11, Table S28. An engineer can run it on fleet logs without labels to see whether a tracker's covariance can change any decision at all. It also shows honestly where the null's mechanism stops holding (pedestrian crossing 8.51%, vehicle crossing 4.09% of rows within 5%).

## 3. Weaknesses

### W1. No road user behind the ego in any test bed, and the one place they appeared they were taken out of the score

- **Severity:** MAJOR
- **Location:** Section III-C; Table II dagger note; Section VI Limits; Supplement Table S1 (Vehicles row), Table S5 (Real logs: true clearance), Table S27; Section I Scope.
- **Evidence (quotation):** "contacts with actors behind the ego were no longer counted" (Section III-C). Also Supplement Table S1: "Ego and lead (or cutting vehicle): the same car model".
- **What is wrong:** Every CARLA run has two vehicles, so braking is free for everyone except the ego's own progress. The only test bed with following traffic is nuScenes, and there the planned score found that more margin made things worse for every source because the hard-brake fallback was struck from behind; after seeing that, rear contacts were removed from the outcome. The paper is transparent about the sequence, but the consequence for the reader is not stated: the whole evaluation assumes that the beneficiary of a margin is the ego and its lead, and that the cost of braking is ego time. Two core statements depend on that premise: (a) the real-log "no measurable room" result exists only under it, and (b) "safer at no extra cost" in closed loop counts no cost to anyone behind. The replay artefact is real (logged followers cannot react), but the planned result is also the paper's only empirical signal that hard braking has a third-party cost, and Supplement Table S27 shows how large the excluded set is (6,122 design-split decisions for F0 "unsafe as planned and safe as changed"). Section I Scope lists pedestrians, cyclists and crossing vehicles as outside, and does not list traffic behind the ego.
- **Fix:** (1) Add to Section I Scope and Section VI Limits one sentence that no test bed contains a reacting follower, so no result prices braking for traffic behind. (2) In Table II or its note, print the planned-clearance real-log room beside the changed one (it is already in Table S27), and say in the text that the planned score was dominated by rear contacts with non-reacting replayed traffic. (3) In the main closed-loop table, add the two columns the supplement already has that bear on a follower: share of decisions in full braking and peak deceleration (Table S23). For the braking-lead runs these favour CK3, TG and PS (1.6%, 8.6%, 2.4% full braking against F0's 52.7%), which strengthens the paper; behind non-braking leads they go the other way for CK3 and PS (Table S26: peak deceleration +0.76 and +2.13 m/s² behind constant-speed leads). (4) Optional and stronger: a closed-loop run set with a simple reacting follower (a fixed time gap and reaction delay) so that a rear-contact share can be reported per arm.
- **Needs:** WORDING ONLY for (1)-(3), using values already in the supplement. NEW VALUE/analysis for (4).

### W2. The closed-loop baseline is at an operating point no speed controller would be released at, so "equivalent" and "safer" are statements about a degenerate regime

- **Severity:** MAJOR
- **Location:** Section III-B; Section V-C; Table IV; Supplement Tables S22 and S23.
- **Evidence (quotation):** "set two levels at which F0's contact share was near 0.20 and 0.05" (Section III-B). Table S23: F0 fallback share 52.7% (lower level) and 78.6% (higher level); F0 median peak deceleration 6.17 and 6.26 m/s².
- **What is wrong:** At the lower level the class-average planner hits the lead in 20% of cases while spending 52.7% of its decisions in the full-braking fallback; at the higher level it still hits in 5% of cases and is in full braking for 78.6% of decisions. Raising the margin scale makes the controller brake fully more often, not follow at a larger gap. This is a bang-bang emergency-braking regime, not car following. Two readings in the paper are affected. First, the closed-loop equivalence of the tracker covariance and of the IMM covariance (N 52.9%, IMM 53.8% full braking) is measured where, for most decisions, no candidate row is feasible under either source, so a covariance has little opportunity to change the selected row; the closed loop therefore adds less independent support to the open-loop null than "it is also equivalent in closed loop" (Abstract) suggests. Second, every arm that is not a scaled covariance margin (CK3, TG, PS) reaches 0% contacts at both levels with 1.6% to 8.6% full braking. That pattern says the class-average margin at these scales is a poor spacing rule in closed loop; it does not single out the braking prediction. The fallback share is among the planned outcomes (Section III-B lists it) but appears only in the supplement. Supplement Table S22 shows a calibration scale (g = 64) at which F0 has 0% contacts on the tuning cases; no arm was compared there.
- **Fix:** (1) Report F0's full-braking share and peak deceleration at both levels in Table IV and state in Section V-C that at these levels the baseline is in full braking for more than half of its decisions. (2) Qualify the closed-loop equivalence accordingly in the Abstract, contribution 2 and the Conclusion (for example "equivalent in closed loop at two levels where the baseline brakes fully in over half of its decisions"). (3) Stronger: add a third level at which F0 makes no contact (g = 64 or the scale the calibration supports) and compare arms there on time lost, rest gap, peak deceleration and full-braking share; that is the operating region a deployed function lives in, and it is where a designer needs to know whether any source differs.
- **Needs:** WORDING ONLY for (1)-(2), with values already in Table S23. NEW VALUE/analysis for (3).

### W3. "At no extra cost" rests on a time-lost measure that can barely differ when every lead stops for the rest of the run, and on a 0.5 s threshold with no stated basis

- **Severity:** MAJOR
- **Location:** Abstract; Section V-C; Table IV caption; Section VII; Supplement Tables S23, S24, S25, S26.
- **Evidence (quotation):** "the braking prediction is safer at no extra cost" (Section V-C; the Abstract has "is safer at no extra cost"). Table S23: mean time lost 24.52 s (F0) and 24.78 s (CK3), lower level.
- **What is wrong:** In the lead-braking cases the lead brakes to a stop and stays stopped, so every arm ends the run stationary behind it; mean time lost is about 24.5 to 25.2 s for every arm at both levels, and the arms differ by tenths of a second. A threshold of 0.5 s on a quantity that is 24.5 s for everyone will classify almost any arm as "no extra cost" in this scenario. The costs that can differ here are not in the rule: where the car stops (CK3 rests 1.41 [0.94, 1.90] m further back at the lower level and 1.98 m at the higher; Table S24) and occupant comfort (which here favours CK3, TG and PS). Where a time cost can actually appear, behind leads that do not stop for good, it does: the braking prediction's time-lost difference is 0.52 [0.25, 0.81], 0.82 [0.79, 0.86] and 0.80 [0.68, 0.92] s (Table S25), all with point estimates above the plan's own 0.5 s threshold, with higher peak deceleration and jerk behind constant-speed leads (Table S26: +0.76 m/s², +0.71 m/s³). The Conclusion adds "by the plan's rule"; the Abstract and Section V-C do not. The plan does not say why 0.5 s is the cost that matters, nor relative to what exposure.
- **Fix:** (1) In the Abstract and Section V-C write "at no extra cost in time lost by the plan's rule" and state in Section V-C that time lost is near 24.5 s for every arm because the lead remains stopped, so this outcome discriminates little on these cases. (2) Bring Table S25's time-lost differences for CK3 into the main text or Table IV, next to the braking-lead result, so the cost is read in the same table as the benefit. (3) State the origin of the ±0.5 s threshold. (4) Report rest gap in the main table as the cost that does differ behind stopping leads.
- **Needs:** WORDING ONLY (all values exist in the supplement).

### W4. The Discussion's inference from closed loop to "the 3 s reading" is contradicted by the time-gap arm

- **Severity:** MAJOR
- **Location:** Section VI, "Which commitment applies"; Table IV (TG rows); Supplement Table S8 (TG row), Table S23.
- **Evidence (quotation):** "which supports the 3 s reading" (Section VI). Table IV, lower level: "TG, time gap | matched | 0% | −0.20 [−0.32, −0.10] | −0.13 [−0.19, −0.06]".
- **What is wrong:** The sentence argues that because the braking prediction reduces contacts in closed loop, "information about the lead's motion is worth room when the car cannot revise in time", and that this supports the 3 s open-loop commitment over the reaction-and-stop one. The time gap's margin, $(r_0 + v_e)^2$, depends only on the ego row's speed; it carries no information about the lead's motion. In closed loop it achieves the same contact reduction as the braking prediction at both levels and loses less time than F0 (−0.13 and −0.23 s), while the braking prediction loses more (0.16 and 0.20 s). In open loop under the 3 s commitment the same two sources are far apart (CK3 0.783, TG 0.287 of the room; negative shares for TG before braking and after the stop, Table S8). So the closed loop does not reproduce the 3 s score's ordering of sources, and the closed-loop benefit is obtainable without lead-motion information. What the closed loop supports is narrower: at these levels the class-average margin shape is a poor spacing rule, and several alternatives fix it. For a designer the practical headline is arguably that the plain constant time gap of adaptive cruise control practice [31], [32] is at least as good as the braking prediction in closed loop and cheaper behind non-braking leads (Table S25: 0.07 and 0.18 s against 0.52 and 0.82 s), and this is left to "reported in the same terms in Table IV (descriptive)".
- **Fix:** Either remove the inference or restate it as what the data show: closed loop confirms that the baseline's late reaction costs contacts, and three different arms remove them, one of which uses no lead-motion information; the closed loop therefore does not adjudicate between the open-loop commitments. Add one sentence in Section V-C and the Abstract (or at least the Conclusion) reporting the time-gap arm's closed-loop result alongside the braking prediction's, marked descriptive.
- **Needs:** WORDING ONLY.

### W5. "Equivalent" in closed loop means within ten percentage points of contact share; the Abstract and Conclusion do not say so

- **Severity:** MINOR (the margin is pre-registered and printed in the Table IV caption; the fix is one clause, but the unqualified word invites over-reading by an assessor)
- **Location:** Abstract; Section I contribution 2; Section VII; Table IV caption.
- **Evidence (quotation):** "equivalent if the contact difference lies within ±0.10" (Table IV caption).
- **What is wrong:** For the open-loop result the Abstract gives the margin ("within 5% of the room"). For closed loop it says only "it is also equivalent in closed loop". A ten-point difference in the share of runs ending in contact is not a quantity any safety case would call negligible; the observed interval for N at the lower level, [−0.08, 0.04], is consistent with four more contacts per hundred cases.
- **Fix:** State the closed-loop margin wherever the word is used: "equivalent in closed loop within ±10 points of contact share and ±0.5 s of time lost (60 cases)".
- **Needs:** WORDING ONLY.

### W6. Classification labels flatten trade-offs a designer would read very differently

- **Severity:** MINOR
- **Location:** Section V-C second paragraph; Section V-D; Table V; Abstract; Supplement Tables S19, S25.
- **Evidence (quotation):** "the braking prediction is inconclusive behind leads that keep their speed or brake mildly" (Section V-C).
- **What is wrong:** Two labels mislead in opposite directions. (a) "Inconclusive" in closed loop behind constant-speed and mildly braking leads: with 20 cases and no contact in either arm the Newcombe interval is [−0.16, 0.16], which can never fit inside ±0.10, so "equivalent" was unreachable by design; meanwhile the time-lost difference is clearly positive (0.52 [0.25, 0.81] and 0.82 [0.79, 0.86] s). A reader takes "inconclusive" as "no evidence of cost". (b) "Costs progress" in open loop behind stop-and-go leads: the braking prediction removes 4.7 [3.4, 6.3] points of wrong goes for 1.7 points of caution, and in closed loop it cuts contacts by 0.25 [0.04, 0.47]. The Abstract's "costs progress behind constant-speed, mildly braking and stop-and-go leads" gives this the same label as 5.3 points of caution for no safety change behind constant-speed leads.
- **Fix:** In Section V-C say "no contact in either arm (20 cases each; the contact interval cannot reach the equivalence margin at this size), with time lost higher by 0.52 and 0.82 s". In the Abstract and Conclusion separate stop-and-go leads: "costs progress behind constant-speed and mildly braking leads; behind stop-and-go leads it trades a small cost for fewer wrong goes".
- **Needs:** WORDING ONLY.

### W7. The function under test is not named, and the test bed's speed range and sensor are missing from the stated limits

- **Severity:** MINOR
- **Location:** Index Terms; Section I Scope; Section III-A; Section VI Limits; Supplement S6.1, Table S1.
- **Evidence (quotation):** "35 per desired speed of 5, 10 and 15 m/s" (Section III-A); "stands for a separate emergency-braking function" (Supplement S6.1); "other sensors can make a covariance vary" (Section VI).
- **What is wrong:** (a) The paper is indexed under adaptive cruise control and cites the comfort limits of [36], [37], but its planner falls back to −5 m/s², reaches a median peak deceleration above 6 m/s² in closed loop and is scored in open loop with a 6 m/s² stop. It is one controller doing both the following and the emergency braking, with no driver in the loop. A reader from either community needs to be told which function class the results speak to. (b) All runs are at 18 to 54 km/h on one straight flat road, with one car model for both vehicles and default weather. Section VI Limits lists "straight simulated roads" but not the speed range; motorway following, which is where the borrowed UN R157 parameters live, is outside. (c) The room is created by a velocity estimate differenced from lidar boxes at 2 Hz that lags the lead's stop (Table III lag 1.42 m). Production longitudinal functions typically have a direct range-rate measurement from radar at a much higher rate; that would be expected to shrink the lag and with it the room the braking prediction recovers. Limits mentions other sensors only as a reason a covariance might vary, not as a reason the room might vanish.
- **Fix:** One sentence in Scope naming the function (a single longitudinal planner with a full-braking fallback, no separate emergency-braking function and no driver), the speed range, and the single vehicle model. One sentence in Limits that with a range-rate sensor the velocity lag, and therefore the room and the braking prediction's share, may be much smaller; the 5 and 10 Hz results (Table S16) already point that way for the after-stop part.
- **Needs:** WORDING ONLY.

### W8. A content claim about standards whose texts the supplement says were not read

- **Severity:** MINOR
- **Location:** Section II last paragraph; Supplement S6.1; Supplement S13.
- **Evidence (quotation):** "their full texts were not read" (Supplement S13), against "limit automatic deceleration to comfort levels" (Section II).
- **What is wrong:** S13 says the paper takes from [36]-[38] and [35] "only their scope", but Section II and S6.1 state what the adaptive cruise control standards limit. From memory the statement is right in substance (to verify), but it is a requirement-level claim made without the source in hand, in a paragraph whose purpose is to show careful use of standards. Separately, and to verify: I recall ISO 22179:2009 [37] as withdrawn, with full-speed-range systems folded into ISO 15622:2018 [36]; if so, citing both as current is inaccurate. Also to verify by the author against the primary text: that the 0.75 s, 6 m/s² and 12.65 m/s³ values belong together in "performance model 2" of [40]; my recollection is that the regulation's two performance models share the reaction time and jerk and differ in deceleration (the 7.6 m/s² sensitivity in Table S14 looks like the other model's value), and that in both the reaction time starts at a defined risk-perception point, not at every planner decision. The paper's "nominal parameters" wording covers the last point, but one sentence saying the trigger logic of the model was not used would prevent a compliance reading.
- **Fix:** Either read the clauses and cite them, or soften to what was verified ("standards for adaptive cruise control [36], [37] address comfort-level automatic deceleration"). Check the status of [37]. Add "the model's risk-perception trigger is not used; the reaction time is applied after every decision" to Section IV-A.
- **Needs:** WORDING ONLY (plus the author's own check of the sources).

### W9. The braking prediction is matched to the scenario generator, and no exposure weighting connects the two sides of its trade

- **Severity:** MINOR
- **Location:** Table I (CK3 row); Section III-A; Section V-D; Supplement S1.3, Table S14 (terciles).
- **Evidence (quotation):** "predicted to brake at 3 m/s² to a stop" (Table I).
- **What is wrong:** The fresh leads brake at realised rates of 2.00 to 5.71 m/s² (Table S14 terciles), so a 3 m/s² assumption sits inside the generator's range, and the source was designed on tuning runs of the same generator. Its benefit is measured on run sets where every lead brakes to a stop and its cost on run sets where none does. In traffic, leads that keep speed or brake mildly outnumber leads that brake to a stop by orders of magnitude, so a designer cannot combine the 0.783 share with the 5.3 and 18.7 points of caution without an exposure assumption the paper does not offer. The paper does not claim CK3 is deployable, and it prints both sides; the gap is that it never says the two sides cannot be netted.
- **Fix:** One sentence in Section VI: the benefit and the cost come from disjoint scenario sets with no exposure weighting, the 3 m/s² value lies inside the generator's braking range, and the braking prediction is a diagnostic of where the room lies, not a proposed policy.
- **Needs:** WORDING ONLY.

### W10. The title promises real driving logs; the paper tested nothing on them

- **Severity:** MINOR
- **Location:** Title; Abstract; Table II.
- **Evidence (quotation):** "so nothing was tested there" (Abstract).
- **What is wrong:** The Abstract is honest, but the title ("...in Closed Loop and on Real Driving Logs") reads as a three-way confirmation. On the logs no hypothesis after "room" was run, the braking prediction was not computed, and the outcome definition was changed after the design-split result. A log-replay adapter that follows the ego's logged path will also, by construction, see few wrong goes, since the human driver's path was safe.
- **Fix:** Drop "and on Real Driving Logs" from the title or change it to reflect the outcome (for example "...with a Log-Replay Check That Found No Room").
- **Needs:** WORDING ONLY.

### W11. Vulnerable road users are outside the tests, which is stated in Scope but not where the conclusions are read

- **Severity:** MINOR
- **Location:** Section I Scope; Abstract; Section VII; Supplement Table S28.
- **Evidence (quotation):** "Pedestrians, cyclists and crossing vehicles are outside the confirmatory tests." (Section I).
- **What is wrong:** The Scope sentence is clear. The Abstract and Conclusion, which are what most readers take away, never name pedestrians or cyclists; the "not justified" sentence in the Abstract gives no reason. The paper's own margin-ratio check shows that in pedestrian-crossing and vehicle-crossing runs the covariance is not a constant multiple of the class average (8.51% and 4.09% of rows within 5%; Table S28), that is, the null's mechanism is absent precisely for the road users with the most to lose. The stored arrays for those families exist (51 and 22 runs) but were not scored at decision level.
- **Fix:** In the Abstract, replace or extend "removing covariance margins is not justified" with the scope ("the tests cover car following only; pedestrians, cyclists and crossing traffic, where the covariance does vary, were not tested"). In Section VI cite Table S28's numbers, not only "crossing traffic".
- **Needs:** WORDING ONLY. (A decision-level score on the stored crossing runs would be a NEW analysis and is optional; it would be exploratory.)

### W12. Minor presentation points that affect the practical reading

- **Severity:** MINOR
- **Location:** Table IV (PS rows); Fig. 3.
- **Evidence (quotation):** "its design caution (11.88% at both levels)" (Section V-C).
- **What is wrong:** (a) The per-phase schedule is the same policy at both "levels" (identical outcomes in Table S23: 24.49 s, 2.67 m, 5.15 m/s², 2.4%); Table IV prints it twice with two different classifications ("safer" and "inconclusive") that differ only because the baseline changed. A reader may take them as two experiments. (b) Fig. 3 does not draw the plan's classification bounds (±0.10 contact share, ±0.5 s), so the figure cannot be read against the rule that produces the labels.
- **Fix:** Say in the Table IV note that PS is one arm compared with two baselines. Add the classification bounds to Fig. 3.
- **Needs:** WORDING ONLY (and a figure edit).

## 4. Stakeholder check

**Who the evaluation assumes benefits from a margin source.** The ego vehicle and the single vehicle ahead of it. A margin source is "better" if it removes wrong goes (open loop) or contacts with the lead (closed loop).

**Who bears the cost, as the paper counts it.** Only the ego's progress: "caution" is speed given up, and the closed-loop cost rule is time lost. Occupant comfort (peak deceleration, jerk) and where the car comes to rest are measured but sit in the supplement and enter no classification.

**Who bears a cost the paper does not count.**
- Traffic behind the ego. There is none in CARLA (two vehicles per run), and on nuScenes contacts from behind were removed from the outcome after the planned score showed the hard-brake fallback being struck by replayed followers. The paper discloses the change and prints the planned result (Section III-C, Table S27). It does not say, in Scope or Limits, that consequently no result prices braking for anyone behind. This is W1 (MAJOR) because the real-log result and the "no extra cost" wording both depend on it.
- Occupants, where the cost rule is concerned: W3 (MAJOR). In the braking-lead runs the uncounted comfort outcomes favour the non-covariance arms; behind non-braking leads they go against the braking prediction and the per-phase schedule.
- Traffic flow generally: the baseline's 52.7% to 78.6% share of decisions in full braking (W2) is a property a traffic engineer would care about and is not in the main text.

**Who is outside the tests.**
- Pedestrians, cyclists and crossing vehicles: stated in Section I Scope; not carried into the Abstract or Conclusion (W11). The paper's own Table S28 shows the null's mechanism does not hold for them.
- Motorway-speed following, other vehicle classes (trucks, motorcycles), curved or graded roads, adverse weather, radar-equipped vehicles: partly stated ("One detector, one in-house planner and straight simulated roads"), speed range and sensor consequence not stated (W7).
- A human driver or a separate emergency-braking function supervising the planner: not stated (W7).

**Does the paper say so?** For vulnerable road users and crossing traffic: yes, in Scope. For traffic behind the ego: the facts are disclosed, the scope consequence is not. For occupants and the cost definition: the rule is printed in the Table IV caption, but the Abstract's "at no extra cost" carries no qualifier. No stakeholder premise rises to CRITICAL: the central open-loop null for the fixed-noise covariance does not depend on any of them.

## 5. Questions for the author

1. At a closed-loop level where F0 makes no contact (Table S22 suggests g = 64 on the tuning cases), what are F0's full-braking share, time lost and rest gap, and do N, CK3 and TG differ from it there? If F0 is still in full braking for most decisions at that scale, is the class-average margin in this planner a usable baseline for closed loop at all?
2. Why does raising the margin scale from the lower to the higher level increase F0's full-braking share from 52.7% to 78.6%? Is it that no candidate row is feasible once the margin exceeds the standing gap, so the planner alternates between fallback and release? If so, does the open-loop "caution" measure capture that behaviour?
3. What is the basis for ±0.5 s of time lost as the cost threshold, given that mean time lost is about 24.5 s in every arm of the lead-braking cases? Was the threshold chosen with that magnitude in view?
4. The time gap carries no information about the lead's motion and matches the braking prediction on contacts in closed loop with less time lost. How do you reconcile that with "information about the lead's motion is worth room when the car cannot revise in time"?
5. On the nuScenes design split under the planned clearance, how many of the wrong goes were rear contacts with replayed followers, by source and margin scale? Reported as its own outcome (not as a wrong go), would it show that larger margins raise rear exposure in replay, and is that worth one sentence as a caution about log replay for margin studies?
6. Did you verify against the primary text of [40] that 0.75 s, 6 m/s² and 12.65 m/s³ are the parameters of the same performance model, and at what event that model starts its reaction time?
7. With a range-rate measurement on the lead (radar), would the 1.42 m lag that locates the room survive? Can the existing runs answer this by feeding the tracker a noisy true range rate at 10 Hz or more, as an exploratory sensitivity?
8. The 51 pedestrian-crossing and 22 vehicle-crossing runs have stored arrays and a varying margin ratio. Is there a reason the decision-level score was not run on them, even as an exploratory result, given that they are named as the first next step?
