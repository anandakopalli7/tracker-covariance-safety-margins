# ARS review sprint, v13 freeze: panel decision record (v01)

- **Seat:** editor synthesis (Claude Fable 5.2), written 21–22 Nov 2026.
- **Reviewed:** `revision_v13\work\A_text\out\freeze_v13_2002\MANUSCRIPT_v13.md` (SHA-256 `93541ff6…4ead`) and `SUPPLEMENT_v13.md` (`4e6766a4…330c`). Both hashes were recomputed and equal the provenance file.
- **Checked against:** `AMENDMENT_11_v13.md` (A11) and `LOCK_A11.txt`, `LOCK_A11b.txt`, `LOCK_A11c.txt`.
- **Excluded:** the title (being changed tonight) and the submission gates (author block, repository and DOI, AI-use confirmation).
- **Limits of this synthesis:** I checked every kept finding against the frozen text. I did not open the export files; where a point rests on them I say so and rely on the methodology seat.

## 1. Decision

| Seat | Model | Recommendation | Score |
|---|---|---|---|
| Journal fit (EIC) | Sonnet 5.5 | Major revision | 5.5 |
| R1, methodology | Fable 5.2 | Minor revision | 7.5 |
| R2, domain | Opus 5.5 (writer's model) | Major revision | 6.0 |
| R3, practical | Sonnet 5.5 | Minor revision | 6.5 |
| Devil's advocate | Fable 5.2 | Major revision | 6.0 |

| | As frozen | After the required wording fixes |
|---|---|---|
| **Panel decision** | **Major revision** (wording-dominant) | Minor revision by this panel's standard |
| Stars (1–5) | 3 | 3.5 |
| Score (of 10) | **6.3** (seat mean) | **7.0** (range 6.8–7.2) |

**Most likely OJ-ITS outcome.** Sent to review, then **major revision**. A desk rejection is unlikely once the title and abstract are plain, because the journal reviews for soundness and the pre-registration is unusually complete. A rejection after review is a real risk, perhaps one in four: a domain reviewer can say that the main result is the Riccati steady state measured at length, in one simulated configuration, with both external test beds showing no room.

**What keeps the score below 8.5.** None of it can be fixed by wording.

1. The headline equivalence could hardly have failed. The covariance is nearly constant (99.9% of rows within 5% of its median) and its own oracle recovers 0.0001 of the room. The paper says so itself (Section VI).
2. Where the covariance does vary, the evidence is thin. Crossing has 0.16 points of room. The dropout gain of 2.8% has a lower end of 0.0064, is not found inside the dropouts (−0.003), and its source is not identified.
3. The added tests were conceived, locked, run and written on one day, after the fresh lead-braking results were known, with internal locks and no adjustment across sequences. They are honest, but they do not carry the weight of the original plan.
4. One simulator, one road geometry, one detector, one in-house planner, 2 Hz without latency. Real logs and cut-in tested nothing.
5. The IMM arm is not a fair test of a manoeuvre-adaptive covariance.
6. The closed loop runs at contact shares of 20% and 5% with 60 cases per arm, and the dropout closed loop is not caution-matched.

The wording fixes below remove over-claims. They raise trust, not evidence, so their ceiling is about 7.

## 2. Adjudication of disputes

### 2.1 Is "confirmed" earned for X, DR, Y and E4?

**Facts I verified.**

- Lock file times are 14:23:47, 14:48:45 and 15:09:34 EST on 21 Nov, and their SHA-256 values equal the three hashes printed in Section IV-E.
- Each lock records sealing evidence (no fresh result file existed) and names what was already known.
- A11 defines "confirmed" as "it and every earlier one passed" (§3.5, §6c.6), and §3.5 adds that there is no adjustment across families "and this is stated".
- A11 §6b fixes Y's disclosure: it was specified after the adaptive filter's fresh share, oracle and spread had been seen.
- A11 §6c.11 fixes DR's disclosure: specified after the fresh lead-braking results were seen, re-scoring the same runs.
- A11 §0 records the aim of the amendment as raising a review score.
- The methodology seat reports result files at 16:40 (DR), 17:27 (Y) and 19:30 (X). I did not re-check those times.

**Ruling.** Both seats are right about different things.

- By the paper's own definition (Table I: "passed in its locked sequence") the label is formally earned for X0–X2, DR0–DR2 and Y1. The methodology seat's lock-before-results check stands.
- The devil's advocate's objection also stands. A reader takes "confirmed" to mean "planned before related data were seen". That is true of the original plan only. X was run after its own go rule said no-go. DR re-scores runs whose unmasked results were known. Y's pass was close to foreseeable. The locks are self-attested hashes on a laptop clock, and nothing is adjusted across what are now eight sequences. DR's lower end (0.0064) would be borderline under any familywise correction.
- E4 is not labelled "confirmed" anywhere in the frozen text (Table S32 gives its class without "(C)"). No change is needed for E4's label; its problem is the higher-level reading (2.3).
- X is the cleanest of the three (new runs, sealed capture), but a single label for all amendment tests is simpler and safer than a three-way distinction.

**Convention to adopt.**

- **"Confirmed"**: only hypotheses of the original locked plan (lead braking, cut-in, real logs, the closed loop of Section V-C).
- **"Passed (amendment)"**: a hypothesis that passed in a sequence of the later amendment. Mark it "(A)" in tables.
- "Descriptive" and "exploratory" keep their meanings.
- The abstract and the Conclusion use neither "confirmed" nor "(A)" for amendment results; they say "in tests added by a later amendment".
- This is a weaker label than A11 registered. Record it in Table S5 as a wording departure in the conservative direction.

### 2.2 Is DR's "inside the equivalence margin" acceptable?

**No, not in the abstract or the Conclusion.** DR2 is a classification (A11 §6c.6) and its class is "recovers". A11 registered no equivalence test for DR; for X it even says "no equivalence claim beyond what X2 says" (§3.5). The upper end is 0.0496 against δ = 0.05, at a nominal 95% level. Next to "confirmed", the parenthesis reads as a confirmed equivalence, and "recovers" beside "equivalent" confuses the reader (devil's advocate, objection 8). It may stay in Section V-E only as a description, with the words "no equivalence test was registered".

### 2.3 Is E4's "safer at no extra cost" over-read?

**Yes in the prose, no in the table.** It is the registered class name (A11 §6d.5, class 1), so Table S35 may keep it. In Sections V-E and VII it is an over-read:

- the higher level is secondary, and the set is not caution-matched;
- A11 itself expects the direction, "because N's margin grows while the tracker coasts";
- the difference is 5% against 15% of 60 cases (3 against 9);
- the covariance arm loses 0.25 [0.15, 0.36] s more (Table S35), an interval that excludes zero. "No extra cost" means only "upper end below 0.5 s".

**One correction to the devil's advocate.** The missing open-loop caution difference is not an unrecorded departure. A11 §6d.5 says it is reported "if D reports it. Otherwise 'not computed'", and Table S35 prints "not computed". No Table S5 row is required.

### 2.4 Other findings dropped or corrected

- **Devil's advocate 7 (second programs).** Dropped as a required item. Section IV-E already says the second programs "share the scoring library, stored arrays and resample draws".
- **R2 F5 ("no track is reborn").** Not verified, and the devil's advocate reads A11 as allowing re-association as a new track. The fix must not assert either; see R3.
- **R1 finding 1's abstract fix** ("2.8% [0.6%, 5.0%]"). Not adopted: rounding 0.0496 to 5.0% prints the margin itself.
- **R1 finding 7 (three decimals in Table S35)** and **R1 finding 8 (coverage values).** These add printed values, so they are moved to section 4.
- **R2 F3 (crossing test bed not specified).** Valid and important, but it needs parameters that are not in the frozen text. Moved to section 4.
- **EIC 3 ("Removing covariance margins is not justified" reads as policy).** One seat only, and R3 found the sentence well placed. Kept as optional (S8).

## 3. REQUIRED for tonight: wording only, no new values

Every number below is already printed in the frozen manuscript or supplement. The abstract is close to its 250-word limit; R2, R4 and R5 are written to fit if the cuts named in R5 are made.

**R1. One label for amendment tests.** (EIC 2; DA 3; R1 3, 6, 9.)
- *Where:* Table I; Section IV-E; Section V-E; Tables S32–S34 and S36; Table S5; Conclusion.
- *Problem:* "confirmed" is used for tests specified after related results were seen.
- *Do:*
  - Table I row: "*Confirmed*; *passed (amendment)*; *descriptive*; *exploratory*" with meaning "Passed in the original locked sequence; passed in a sequence of the later amendment, locked before its own values but written after the fresh lead-braking results were seen; untested; from runs that shaped the analysis".
  - Section V-E: replace each "(confirmed)" with "(passed; amendment)". For the crossing share write "(classified as uninformative variation; passed, amendment)". For the twin write "(passed; specified post hoc)".
  - Tables S32–S34: "(C)" becomes "(A)"; S32 caption: "(A) passed in its amendment sequence".
  - Table S5: add a row, "Label of the later amendment's tests: the amendment says 'confirmed'; the text says 'passed (amendment)' (a weaker label, decided after the panel review)".

**R2. Remove the dropout "equivalence".** (R1 1; DA 2, 8.)
- *Where:* Abstract; Section V-E; Section VII.
- *Abstract:* replace "it recovers none of a small room (0.16 points) in fresh pedestrian crossing and a confirmed but small 2.8% of the room (inside the equivalence margin) under detection dropouts (room 5.63 points)" with "it shows no recovery of a small room (0.16 points) in fresh pedestrian crossing and recovers a small 2.8% of the room under detection dropouts (the same runs re-scored), a gain not found inside the dropouts".
- Also in the abstract, replace "In open loop, where the fixed-noise covariance varies more," with "In tests added by a later amendment, where the fixed-noise covariance varies more (open loop),".
- *Section V-E:* replace "recovers 0.0283 [0.0064, 0.0496] of it, inside the equivalence margin and against" with "recovers 0.0283 [0.0064, 0.0496] of it (its upper end lies just below δ = 0.05; no equivalence test was registered here), against".
- *Section VII:* delete "(inside the equivalence margin; its oracle: 40%)" and write "(its oracle: 40%)"; delete "confirmed but".

**R3. Say that the dropout gain is not found inside the dropouts, and state the dropout conditions.** (R1 2; DA 2; R2 F5; R3 5.)
- *Where:* Section V-E.
- *Add after the dropout result:* "Among the 3,644 decisions inside a dropout its share is −0.003 [−0.020, 0.015] (descriptive; Table S34), so the pooled gain is not shown to come from the covariance's growth while a track coasts, and its source is not identified."
- *Replace* "We read the bottleneck in both as the information in the covariance, not its amplitude." *with* "In pedestrian crossing we read the bottleneck as the information in the covariance, not its amplitude; under dropouts the covariance recovers 0.071 of what its oracle does."
- *Replace* "every arm keeps unmatched tracks through a window (a pre-registered output-rule change)" *with* "every arm keeps an unmatched track for up to three updates, the longest masked stretch (a pre-registered output-rule change), so track loss after longer gaps was not tested".
- Then delete the now-repeated "(efficiency 0.071 [0.016, 0.129])" or keep it and drop the second half of the replaced sentence; do not print both.

**R4. Rewrite the dropout closed loop at the higher level.** (DA 1; R2 F4f; R3 5; R1 7.)
- *Section V-E:* replace "At the higher level (secondary), the covariance is safer at no extra cost (contacts 5% against 15%) and the IMM's is inconclusive" with "At the higher level (secondary; not caution-matched) the covariance arm had fewer contacts (5% against 15% of 60 cases) and lost 0.25 [0.15, 0.36] s more; without caution matching this cannot be told from a wider margin, which is the expected effect of a covariance that grows while a track coasts. The IMM's is inconclusive".
- *Section VII:* replace "and, at the higher level (secondary), safer at no extra cost" with "and, at the higher level (secondary), had fewer contacts for more time lost, as a wider margin would".
- Table S35 keeps the registered class name.

**R5. Report the braking prediction's closed loop fully.** (EIC 5; R2 F4; R3 2, 3; DA 6.)
- *Abstract:* replace "In closed loop (lower caution level) the prediction is safer at no extra cost (0.16 s lost)." with "In closed loop at the lower caution level, where the class average makes contact in 20% of cases, the prediction removed the contacts for 0.16 s more time lost, as did a plain time gap."
- *To stay within 250 words, cut:* "(by 0.0498 [0.0424, 0.0569]; specified after its share was seen)" to "(specified after its share was seen)"; the second "(±0.10 contact share)"; and "(room 5.63 points)" (already removed by R2).
- *Section V-C:* after "the braking prediction is safer at no extra cost" add "(the plan's class: time lost below 0.5 s)".
- *Section V-C or Limits:* add "These classes refer to the ego's contacts and time only; cost to following traffic and to occupants is not scored here (Supplement S9 gives the braking outcomes)."

**R6. Do not claim absence of rank information in crossing.** (R1 5; R2 F3.)
- *Section VII:* replace "where it varied more it varied without rank information (its oracle: 69%) in fresh pedestrian crossing" with "where it varied more it showed no recovery of a small room in fresh pedestrian crossing (share −0.07 [−0.22, 0.03]; its oracle: 69%)".
- *Contribution 2:* replace "it recovers none of the room in pedestrian crossing" with "it shows no recovery of a small room in pedestrian crossing".
- *Section V-E:* add "(Section IV-C's class name; no permuted-twin test of the covariance was run here)" after the crossing class.

**R7. State multiplicity and the nature of the locks.** (R1 4; DA 3.) A11 §3.5 requires the statement; neither file has it.
- *Section IV-E, after the sentence on fixed sequences, add:* "Sequences are not adjusted for one another; each is tested one-sided at 0.025. The locks are SHA-256 hashes with local file times, not third-party timestamps."
- If a third-party timestamp does exist, name it instead of the second sentence.

**R8. Flag the closed-loop operating points.** (R3 1; R2 F4e; EIC 5; DA 5.)
- *Section V-C, after the sentence giving the full-braking shares, add:* "The two levels were set so that contacts were frequent enough to compare (class-average contact shares of 20% and 5%); neither is an operating point for a deployed system, and with 60 cases per arm the test cannot resolve contact differences much below 0.10. Equivalent here does not mean safe."

**R9. Say plainly that the equivalence was expected, and rename contribution 2.** (DA 4; R2 F1; EIC 6.)
- *Contribution 2:* change the heading "A confirmatory test." to "A confirmatory test and amendment tests." After "(share within [−0.09%, 0.15%]) and in closed loop" add ", as its near-constancy led one to expect; the test adds the bound".
- Mark the crossing and dropout clause "(later amendment; Section V-E)".

**R10. Split Section V-E.** (EIC 4; R3 7.)
- Break the single paragraph into four: how the tests were added; pedestrian crossing; dropouts in open loop; dropouts in closed loop and the permuted twin. End each with one plain sentence of what it shows. Move "(nominal 99%, the plan's fallback)" to a pointer "(interval level: Table S33)". No new numbers.

**R11. Do not let "no room" read as external support.** (R2 F3; R3 6; DA 5.)
- *Section V-A:* after "so nothing is tested there" add "; the cut-in runs are uninformative, not a negative result". After "so nothing is tested on the logs" add "; they neither support nor contradict the simulated results".
- *Section VII:* replace "Cut-in events and held-out nuScenes logs showed no measurable room." with "Cut-in events and held-out nuScenes logs showed no measurable room, so they tested nothing."

**R12. Narrow the scope sentence.** (DA 5; R3 4.)
- *Limits:* replace "One detector, one in-house planner and straight simulated roads were tested" with "One simulated configuration was tested: one detector, one in-house planner and straight roads at desired speeds of 5 to 15 m/s".
- *Section VII:* replace "Magnitudes hold at 2 Hz without latency and under this recording policy." with "Magnitudes hold in this one simulated configuration, at 2 Hz without latency and under this recording policy."

## 4. Needs new evidence or new printed values: not for tonight

List these under future work now, and plan them for the revision stage.

| # | Item | Raised by |
|---|---|---|
| E1 | A registered test in a setting where the covariance varies **and** there is sizeable room, with a third-party timestamp (for example a registry or a signed public commit) and a stated familywise rule | DA 3, 4; R1 4 |
| E2 | The dropout mechanism: print the registered descriptives of A11 §6c.7 (in-dropout plus gap row, re-association counts), and the share by updates since the last detection | R1 2; DA 2; R2 F5 |
| E3 | Dropouts with track loss and re-birth (masks longer than the coasting rule) and occlusion-like, correlated masks | R2 F5 |
| E4 | A baseline that scales the class average by updates since the last detection (no ground truth), and a regression of the crossing margin ratio on heading against the constraint normal and on realised error | R2 F1 |
| E5 | An IMM with two noise levels, mode probabilities around braking onset, and an arm that uses the IMM's mixed mean | R2 F2 |
| E6 | The crossing test bed's specification (walker speed, start rule, distance, occlusion, class noise and class average) and the lead's deceleration range, as a table in Supplement S1 | R2 F3 |
| E7 | A caution-matched closed loop under dropouts, with the open-loop caution difference computed | DA 1; R2 F4 |
| E8 | Closed loop at a realistic operating point with more cases, and full-braking share and peak deceleration per arm in Table IV | R3 1, 3; R2 F4 |
| E9 | A second planner or stack, a second detector, latency, and real-world logs that show room | DA 5; EIC |
| E10 | A permuted-twin test of the fixed-noise covariance in crossing | R1 5 |
| E11 | Estimated coverage beside each nominal 95% interval; the E4 contact interval to three decimals | R1 7, 8 |
| E12 | Detector velocity error by phase, to separate the detector's lag from the tracker's | R2 F7 |
| E13 | Related work on uncertainty in braking and warning decisions, pedestrian switching dynamics and track existence, each reference verified first | R2 F8 |

## 5. Suggested wording items (optional)

- **S1.** Abstract: move the definition of "room" before its first use, or open with a plain sentence such as "In simulation, a fixed-noise tracker's covariance gave a car-following planner no better decisions than one fixed margin per vehicle class, at equal caution." Only if the word limit allows. (EIC 1; R3 7.)
- **S2.** Section V-E, dropout closed loop at the lower level: print the numbers already in Table S35, "(contact difference −0.03 [−0.10, 0.03]; time lost 0.15 [0.08, 0.24] s)". The methodology seat reports that the lower end meets the −0.10 rule only before rounding; if the author confirms it from the export, say so in the Table S35 caption. (R1 7.)
- **S3.** Section IV-C: add "'Recovers' is statistical detection; the margin δ is practical relevance; both are reported." (DA 8.)
- **S4.** Section VI: add, after checking that it holds for this tracker's object-frame noise, "With fixed noise, the covariance depends on when measurements arrive and on the estimated heading, not on the measured values [25]; crossing tests the geometry channel and dropouts the schedule channel." (R2 F1.)
- **S5.** Abstract and Conclusion: describe the IMM as "an IMM whose modes differ only by a small acceleration term", if Supplement S4 supports the wording. (R2 F2.)
- **S6.** Introduction: "Equal caution means each source may slow the car by the same average amount, so none can look safer merely by braking more. It measures the ego's progress, not cost to following traffic." (R3 8.)
- **S7.** Section VII: a short "Reading for designers" of three clauses: the covariance gave no measurable benefit over a class constant here; a braking prediction or a time gap changed outcomes far more; nothing here speaks to other detectors, sensors, speeds or newly born tracks. (R3 2.)
- **S8.** Abstract's last sentence: "These tests do not justify removing a covariance margin; births, other road users and other sensors were not tested." (EIC 3.)
- **S9.** Move "Pre-submission reviews by an AI-based review panel shaped this manuscript…" from Section IV-E to the Acknowledgment. (EIC 8.)
- **S10.** Section III-E: "The margin uses the posterior covariance propagated without the motion model's process noise over the look-ahead; including it is not tested", after checking it against the code. (R2 F6.)

## 6. Panel composition and caveat

From `work\panel_provenance_sprint.json` (panel `ars-review-v13-sprint-round-1`):

- Five seats were dispatched by the coordinating session (Claude Opus 5.5) as separate fresh sub-agents, in parallel. Synthesis is by a separate Claude Fable 5.2 sub-agent (this record).
- Seats: journal fit, Sonnet 5.5; methodology, Fable 5.2 (also read A10, A11, the locks and the exports); domain, Opus 5.5; practical, Sonnet 5.5; devil's advocate, Fable 5.2 (also read A11).
- Blinding: seats did not see each other's reports, earlier reviews or the response letter.
- The cards were the v12 cards the author had accepted; the card-confirmation pause was not held.
- Seats were told not to spend findings on the title.

**Correlated-error caveat.** All seats and the synthesis are Claude models of one family. Using three models reduces correlated error but does not remove it. The domain seat shares the writer's model, and the methodology seat, the devil's advocate and this synthesis share one model. Agreement among seats is therefore weaker evidence than agreement among independent human reviewers. No seat is a human expert in tracking or vehicle safety, and the scores above are this panel's estimate, not a prediction any editor has endorsed.
