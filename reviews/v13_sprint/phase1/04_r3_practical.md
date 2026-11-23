# Seat 04: Peer Reviewer 3 (Cross-disciplinary / Practical)

- Model: Claude Sonnet 5.5
- Freeze folder: ARS_TRIAL\revision_v13\work\A_text\out\freeze_v13_2002\
- MANUSCRIPT_v13.md SHA-256: 93541ff6b1592bbdfc9b5f239fd81e8537fa3f433a3e2a76ba43a242914a4ead
- Read: manuscript in full (all 344 lines). The supplement was not opened, so findings on Supplement content are limited to what the manuscript itself reports. Title, author block, repository/DOI and AI-confirmation not assessed (gates).

## Recommendation

Minor revision (text-only; no new experiments needed from my angle), confidence 4/5. Score 6.5/10.

The work is careful and, on conditions, unusually honest for this field. The closing sentence ("does not justify removing a covariance margin") is correctly cautious. But the paper never tells an engineer what to do with its result, buries the most actionable closed-loop finding, and reports closed-loop operating points a safety practitioner would regard as unusable without saying so.

## Findings

**1. MAJOR. Closed-loop operating points are not flagged as non-deployable.** Location: Abstract ("in closed loop (±0.10 contact share)"); Section III-B; Section V-C; Table IV. The baseline F0 hits contact in 20% of cases at the lower level and 5% at the higher level, with 60 cases per arm. A 5% to 20% contact rate in a lead-braking scenario is far from any assurance target, and an equivalence margin of ±0.10 contact share is half the lower-level baseline. A practitioner will read "equivalent" as "equally safe" when it means "indistinguishable at a very coarse resolution". The abstract's "(lower caution level)" does not say what contact rate that means. Fix: add to V-C and Limits: "The closed-loop levels were chosen so that contacts were frequent enough to compare (F0 contact share 20% and 5%); neither is an acceptable operating point for a deployed system, and with 60 cases per arm the test cannot resolve contact differences much below 0.10. Equivalence here does not mean safe." In the abstract replace "(±0.10 contact share)" with "(F0 contact share 20%; equivalence band ±0.10)".

**2. MAJOR. No explicit practitioner takeaway; the most actionable closed-loop result is buried.** Location: Abstract; Section VII; Table IV (TG rows); Section VI "Which commitment applies". The conclusion is a list of recoveries and a prohibition. Missing is what a designer should take away. Table IV shows the plain time gap (no lead-motion information) removes all contacts at the lower level with a time saving (−0.13 s [−0.19, −0.06]) and the same contact difference as the braking prediction, and Section VI says the closed loop ranks none of the three. That is the practical headline, yet it appears only mid-paragraph in V-C, not in the abstract or conclusion. Fix: add a short Section VII paragraph, "Reading for designers": "(i) In these tests a fixed-noise tracker covariance used as a margin gave no measurable benefit over one constant margin per vehicle class; (ii) a braking prediction or a time-gap rule changed outcomes far more, and in closed loop a plain time gap did as well as the prediction at lower time cost; (iii) this is not evidence about other detectors, sensors, speeds, update rates, newly born or coasting tracks." Frame it as a reading of these tests, not a design recommendation.

**3. MAJOR. Cost to traffic behind and to occupants is invisible in the main text, though the baseline brakes fully in over half of its decisions.** Location: Section V-C ("brakes fully in 52.7% ... 78.6%"); Section I Scope; Section VI Limits; Table IV. Section III-B lists peak deceleration, jerk and full-braking share as outcomes, but Table IV reports only contacts, time lost and impact speed; the rest is in Supplement S9. "Safer at no extra cost" (Abstract; Table IV; V-C) therefore holds for the ego's contacts and time only; the arm that removes contacts plausibly brakes earlier or harder, which is the cost passed to followers and occupants. Fix: add full-braking share and peak deceleration per arm to Table IV, and relabel the classification "safer for the ego, no extra time cost" with: "Cost to following traffic and occupant comfort is not scored; these labels refer to the ego's contacts and time only." Same qualifier in the abstract ("safer at no extra cost (0.16 s lost)").

**4. MINOR. Test-bed conditions a practitioner needs are missing from the abstract and Limits.** Location: Abstract; Section III-A; Section VI Limits. Lead desired speeds are 5, 10 and 15 m/s (18 to 54 km/h), on a straight flat road, simulated 32-channel lidar, one in-house planner. The abstract says "simulated" and "2 Hz without latency" but not the speed range; Limits list "straight simulated roads" but not speeds, and do not note that the stop parameters borrowed from UN R157 (a highway function) are used in an urban-speed range. Fix: put "5 to 15 m/s" in the abstract and add to Limits: "desired speeds 5 to 15 m/s only; the R157-derived stop parameters are nominal values borrowed for this range."

**5. MINOR. The coasting rule and dropout conditions are not stated where needed.** Location: Section V-E; Section VI Limits ("young and coasting tracks"); Section VII. V-E says only that "every arm keeps unmatched tracks through a window" and that masks are "truth-independent". The window length, whether the covariance grows while coasting, and the mask law are not in the main text, yet the dropouts are the only test where the covariance varies, and the Limits mention "coasting tracks" without defining them. Fix: in V-E state: "Dropouts remove 1 to 3 consecutive detections (0.5 to 1.5 s at 2 Hz); during a dropout the tracker coasts for up to [N] updates with its covariance propagated by the filter, then the track is dropped." In the Conclusion attach "so not a controlled comparison" to the clause "safer at no extra cost" for the not-caution-matched dropout closed loop (contacts 5% against 15%).

**6. MINOR. The real-log result can be over-read as external validation.** Location: Abstract ("held-out nuScenes logs showed no measurable room"); Section III-C; Table II. Contacts with actors behind the ego were dropped after the design-split result, replay traffic does not react to counterfactual brakes, and the outcome is "no room, so nothing is tested". Fix in the abstract: "nuScenes logs showed no measurable room, so they neither support nor contradict the simulated results; traffic behind the ego could not be scored in replay."

**7. MINOR. Readability: the abstract and Section V-E are not usable by a non-specialist.** Location: Abstract; V-E (one paragraph of about 400 words); Table I placement. The abstract opens with "share", "room" and "equivalence margin" before any definition and uses "recovers", "efficiency 0.071", "nominal 99%, the plan's fallback" and "(confirmed)" with no gloss; the plain bottom line is never stated first. Fix: open the abstract with: "In these simulated tests, using a fixed-noise tracker's own uncertainty as a safety margin gave no measurable benefit over one constant margin per vehicle class; a braking prediction and a simple time gap did." Then keep the numbers. Split V-E into three short paragraphs (pedestrian crossing; dropouts in open loop; dropouts in closed loop and the permuted twin), each ending with a one-line takeaway; move "efficiency" and "nominal 99%" to Supplement S14.

**8. MINOR. "Equal caution" is the key idea but is explained only as a score.** Location: Introduction; Section IV-A; Table I. Caution is "speed given up against the first truly safe profile". A designer will translate that into comfort or follower cost, which the paper does not measure. Fix: in the Introduction add: "Equal caution means each margin source may slow the car by the same average amount, so a source cannot look safer merely by braking more. It measures progress given up by the ego, not cost to following traffic."

## Conditions check

- Simulation, 2 Hz, no latency, open versus closed loop, off-policy open-loop shares: stated, mostly clearly (Abstract, III-A, Limits).
- "Does not justify removing a covariance margin": stated three times and well placed (Abstract end, VI, VII).
- Regulation wording: "with no claim of compliance" is clear; the borrowed 0.75 s and 6 m/s² are labelled nominal.
- Missing or buried: speed range (4), coasting and dropout law (5), closed-loop contact levels (1), follower cost (3).

## Strengths

- Pre-registration, locking and recounts make the null credible; the amplitude-matched oracle lets a reader see that a null is not just a blunt metric.
- Honest labelling of confirmed, descriptive and exploratory results, and of the non-caution-matched dropout closed loop.
- Limits and the final sentence refuse the obvious over-reading and name young tracks, coasting, other road users and other sensors as untested.
- Table I is a real help; Fig. 3 (contact difference against time lost) is the right picture for a safety-versus-progress trade.
- The progress cost of the braking prediction behind non-braking leads is reported, not hidden.

## Score

6.5/10. Sound and carefully hedged; practical value reduced by a missing designer-facing reading, unflagged unusable closed-loop operating points, an incompletely framed "no extra cost", and a dense abstract.
