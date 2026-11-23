# Seat 5: Devil's Advocate

- **Seat:** Devil's Advocate (pre-submission panel, IEEE OJ-ITS)
- **Model:** Claude Fable 5.2
- **Freeze folder:** `revision_v13\work\A_text\out\freeze_v13_2002\`
- **SHA-256 of MANUSCRIPT_v13.md as read:** `93541ff6b1592bbdfc9b5f239fd81e8537fa3f433a3e2a76ba43a242914a4ead`
- **Also read:** SUPPLEMENT_v13.md (S3, S12, S14), AMENDMENT_11_v13.md. No earlier review report or response letter was read. Title, author block, DOI and AI-confirmation gates are excluded.

## Objections

### 1. MAJOR. The closed-loop dropout "safer at no extra cost" breaks the paper's own premise
**Where:** Section V-E; Section VII; Table S35.
**Argument:** The paper's founding rule (Section I) is that sources must be compared at equal caution, "because any wider margin avoids risky decisions by giving up progress". The dropout closed loop is declared not caution-matched, and the amendment says N's margin "grows during dropouts by design". At the higher level N has 5% contacts against 15% (3 against 9 of 60 cases) and loses 0.25 [0.15, 0.36] s more. That is exactly what a wider margin does. The comparison is secondary, has no multiplicity control, and the IMM's twin comparison is inconclusive. Yet the Conclusion prints "safer at no extra cost" without the time cost. In addition, amendment §6d.1 promised "the open-loop caution difference reported"; Table S35 says "not computed", and I found no row for this in Table S5.
**Repairable by wording**, plus one disclosure. Fix: in V-E and VII write "at the higher level (secondary, not caution-matched) the covariance arm had fewer contacts (3 against 9 of 60) and lost 0.25 s more; without caution matching this cannot be told from a wider margin". Remove "safer at no extra cost" from the Conclusion. Add the uncomputed caution difference to Table S5 as a departure.

### 2. MAJOR. The "confirmed 2.8%" under dropouts does not come from the dropouts
**Where:** Abstract; Section V-E; Table S34.
**Argument:** The stated motive is that the covariance grows with time since update and so tracks the real error. Table S34 reports N's share in the decisions inside a dropout alone as −0.003 [−0.020, 0.015]. So the 2.8% arises outside the windows. The amendment records a candidate cause: after a window the lead can re-associate as a new track with a birth covariance. The main text never says this. It also adds "inside the equivalence margin" on an upper end of 0.0496 against 0.05, though equivalence was not a registered DR hypothesis (DR2's registered class is "recovers"). Finally, "we read the bottleneck in both as the information in the covariance" sits badly with that registered class.
**Wording suffices for the claim; evidence is needed for the mechanism.** Fix: state in V-E that the share inside dropout windows is −0.003 and that the source of the gain (gap rows, re-born tracks) is not identified; drop "inside the equivalence margin" for dropouts or call it descriptive; restrict the "bottleneck" sentence to pedestrian crossing. The amendment's planned gap-row and re-association descriptives (§6c.7) would settle the mechanism if they exist.

### 3. MAJOR. Forking paths in a one-day sprint; "confirmed" is stretched
**Where:** Sections IV-E, V-E; Table S5; amendment §0, §2, §6b, §6c.
**Argument:** All added results were conceived, locked, run and written on 21 Nov, the day of the freeze. The amendment's approval record states the aim: to raise a review score. Crossing was run after its own go rule said no-go. The twin test was specified after the adaptive filter's share (0.046), oracle (0.048) and spread were seen, so its pass was close to foreseeable. Dropouts re-score runs whose results were known, under a configuration change (three-update coasting), after the pipeline had been exercised on old runs. The disclosures are honest, and the amendment supports that no fresh value preceded each lock. But the locks are self-attested laptop-clock hashes ("session times ran ahead") with no external timestamp, and each sequence is tested at 0.025 with no adjustment across what are now seven sequences. Table I defines "confirmed" as "passed in its locked sequence"; a reader will take it as "pre-registered before related data were seen".
**Repairable by wording.** Fix: use a separate label (for example "passed, post hoc sequence") for the crossing, twin and dropout tests in the Abstract, V-E and Table S32; state in IV-E that there is no adjustment across sequences and that locks are internal hashes; remove "confirmed" from the Abstract's 2.8% and from the twin result.

### 4. MAJOR. The headline equivalence could not have failed
**Where:** Sections IV-C, V-A, VI.
**Argument:** The perfect ranking oracle in a ±5% band recovers 1.3% of the room. The equivalence margin is 5% of the room. The tracker's margin lies within 5% of its median in 99.9% of rows, and its own oracle recovers 0.0001. So no ordering of this covariance could leave the margin. The paper admits the result "was expected" and that "detection at its spread is not shown". A reviewer will say that contribution 2 is the Riccati steady state measured at length, and that the informative results are the post hoc ones of objection 3.
**Partly wording, partly evidence.** Fix: say plainly in the Abstract and contribution 2 that the equivalence follows from constancy and that the test adds the protocol and the bound. A stronger paper needs a registered test where the covariance varies and there is room.

### 5. MAJOR. Simulation only, one configuration, and both external test beds returned nothing
**Where:** Sections III, V-A, V-D, VI.
**Argument:** One straight CARLA road, one detector, one in-house planner, a 2 Hz detector without latency. The baseline brakes fully in 52.7% of decisions and makes contact in 20% of closed-loop cases, far from any deployed operating point. The room moves from 1.16 to 5.58 points with the recording policy, and the after-stop room is "largely a consequence of the 2 Hz update". nuScenes showed no room even after the clearance rule was changed post hoc; cut-in showed none. Pedestrian crossing has 0.16 points of room and one contact run in 390. All open-loop shares are off-policy.
**Needs evidence** (a second planner or stack, or real logs with room). Wording can only narrow: put "in one simulated configuration" in the Abstract's first sentence.

### 6. MINOR. The Abstract over-reads the braking prediction in closed loop
**Where:** Abstract ("safer at no extra cost (0.16 s lost)"); Section V-C; Table IV.
**Argument:** A time gap that uses no information about the lead gives the same contact result and loses less time, and Section VI concedes the closed loop "ranks none of them". "No extra cost" is a pre-set 0.5 s threshold on leads that all brake to a stop; behind leads that stop and pull away the same arm is safer at a cost, and at the higher level it is inconclusive.
**Repairable by wording.** Fix: "In closed loop at the lower level the prediction removed the contacts (12 of 60 to none), as did a plain time gap; behind leads that do not brake hard it costs time."

### 7. MINOR. Verification is less independent than "recount every printed value" suggests
**Where:** Section IV-E; S12; Acknowledgment.
**Argument:** The second programs share the scoring library, arrays and resample draws, and are written by models of the same family as the first. A shared cache already hid one error (Table S5). An AI panel "shaped" the text. Sweeps are "on request" and no archive exists yet.
**Repairable by wording.** Fix: describe the second programs in the main text as "a recount of the analysis layer, not of the scoring library".

### 8. MINOR. "Recovers" and "equivalent" apply to the same result
**Where:** Sections IV-C, V-B, V-E.
**Argument:** By IV-C a share whose interval is above zero "recovers" room, so the re-tuned IMM (0.0055) and dropouts (0.028) both "recover" while being "inside the equivalence margin". The reader cannot tell which label governs. The adaptive filter's 4.6% straddles the margin.
**Repairable by wording.** Fix: one sentence in IV-C saying that "recovers" is statistical detection, the margin is practical relevance, and both are reported.

## The strongest counter-argument to my case

The paper is unusually candid. Every fork listed above is disclosed in the text or in Table S5. The post hoc tests cut both ways (a null in crossing, positives under dropouts and for the adaptive filter), and the paper reports the ones that weaken its original thesis. Its closing sentence refuses the convenient conclusion. The amplitude-matched oracle with a permuted twin is a real methodological contribution: it tells a reader what a null means. A bounded, carefully hedged negative result on a question whose answer practitioners assume has value for an open journal that reviews for soundness.

## Recommendation and score

**Major revision.** Objections 1, 2, 3 and 6 can be closed by wording within a day. Objections 4 and 5 limit the ceiling and need evidence the sprint cannot supply.

**Score: 6 / 10** (about 6.5 if objections 1–3 and 6 are fixed in the text).
