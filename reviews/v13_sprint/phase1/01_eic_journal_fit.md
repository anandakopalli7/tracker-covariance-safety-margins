# Seat 01: Journal-Fit Reviewer (internal role EIC)

- Model: Claude Sonnet 5.5
- Freeze folder: ARS_TRIAL\revision_v13\work\A_text\out\freeze_v13_2002\
- SHA-256 of MANUSCRIPT_v13.md read: 93541ff6b1592bbdfc9b5f239fd81e8537fa3f433a3e2a76ba43a242914a4ead
- Angle: fit, significance, contribution, readability, disclosure and overstatement. Methodology was not reviewed in depth. The supplement was not opened beyond the manuscript's own pointers.

## Recommendation

**Major revision** (it would go to review, but not in this form). Confidence 3 of 5.

A rigorous, honestly hedged null result is publishable in OJ-ITS if the reader can find it. At present the paper is hard to read, and a few labels and sentences claim more than the design supports. Most fixes are wording and structure; none needs new experiments.

## Findings

**1. MAJOR. The abstract buries the bottom line and uses undefined coined terms.**
Location: Abstract, first sentence ("Used as a planner's safety margin, a fixed-noise Kalman tracker's covariance is equivalent to one class-average margin...").
- Problem: The 217-word abstract opens with an equivalence interval. It then uses "room", "share", "recovers", "caution-matched" and "rank information" before any definition. Table I is never pointed to. A transportation-engineering reader cannot extract the take-away.
- Fix: Open with plain words: "In simulation, a tracker's covariance gave a car-following planner no better braking decisions than one fixed margin per vehicle class, at equal caution." Then give the numbers. Define "room" in one clause: "the wrong-go reduction a perfect-hindsight margin would achieve". Drop the secondary numbers (0.0498, 2.8%, 0.16 s) from the abstract and keep the three or four that carry the claim.

**2. MAJOR. Post-hoc analyses are labelled "confirmed".**
Location: Section V-E ("Detection dropouts, specified after the fresh lead-braking results"); abstract ("a confirmed but small 2.8%"); Conclusion; Section V-B addendum.
- Problem: The text says the pedestrian-crossing test went ahead "despite the pre-stated no-go". It says the dropout test and the adaptive-filter twin test were specified after results were seen. Yet each carries "(confirmed)", and the abstract and conclusion repeat the word. A "confirmed" reserved for the locked sequences loses meaning when also applied to amendments. An editor will read it as spin.
- Fix: Use a separate label, e.g. "passed (post-hoc amendment, lock after data seen)", in Table I, the text, the abstract and the conclusion. Table I's definition of "confirmed" ("Passed in its locked sequence") should say explicitly that amendments are excluded. State once, in Section IV-E, which amendments were fixed before versus after which data.

**3. MAJOR. The practical conclusion is framed in a way a reader can misread.**
Location: Abstract last sentence ("Removing covariance margins is not justified."); Conclusion; Discussion "Limits".
- Problem: The central finding is that the covariance is equivalent to a class-average margin. Read plainly, that suggests a covariance can be replaced by a constant. The paper then warns against removal, on grounds the data do not test (young tracks, other sensors). The "not justified" sentence reads as a policy claim from a simulation null, and it sits oddly beside the equivalence result.
- Fix: "In these simulated car-following tests the covariance added nothing a class average did not; whether it matters for births, other road users or other sensors was not tested." Move any deployment advice to the Discussion.

**4. MAJOR. Section V-E and the abstract are unreadable at their current density.**
Location: Section V-E (one paragraph of about 350 words); Abstract sentences 5-7.
- Problem: V-E packs seven results, four intervals with different confidence levels ("nominal 99%, the plan's fallback"), an "efficiency" figure, and a closed-loop comparison into a single paragraph. A reader needs Supplement S14 to follow it. About a quarter of the main text points to supplements for essential content.
- Fix: Split V-E into three short subsections (pedestrian; dropouts; adaptive twin) and add a small Table VI. Move "efficiency 0.071" and the 99% fallback to the supplement. Cut V-E's text by roughly 30%.

**5. MAJOR. The closed-loop headline omits what makes it less informative.**
Location: Abstract ("In closed loop (lower caution level) the prediction is safer at no extra cost (0.16 s lost)"); Table IV.
- Problem: In Table IV the time gap, which uses no motion information, gives the identical contact difference (−0.20) at lower time cost. At the higher level the prediction is "inconclusive". F0 at the lower level has 20% contacts. The abstract reports only the favourable arm and level. Section VI concedes that the closed loop "ranks none of them", but the abstract does not.
- Fix: Add to the abstract: "a plain time-gap rule did equally well; closed loop did not separate them, and at the higher caution level the result was inconclusive." State that a 20% baseline contact share is a stress setting, not a deployment rate.

**6. MINOR. The contribution framing is thin and mixed.**
Location: Section I, contributions 2 and 3; Section II, "Novelty, with its limits".
- Problem: The paper itself says the mechanism (Riccati steady state) is not new. Contribution 2 is largely a null on one tracker. Contribution 3 is "largely exploratory". The honest limits paragraph is a strength, but an editor will ask what a reader should do differently.
- Fix: Rewrite contribution 1 as the headline: a protocol for judging an uncertainty signal's decision value, with a sensitivity control. Make 2 and 3 its demonstrations. Add one sentence on who should use the protocol (anyone offline-scoring a tracker, forecaster or perception module).

**7. MINOR. Real-log disclosure and the "not caution-matched" set are present but scattered.**
Location: Section III-C ("contacts with actors behind the ego were no longer counted"); Table II footnote †; Table IV "not caution-matched"; Section V-E closed loop with dropouts.
- Problem: The post-hoc clearance change that turned 6,122 decisions from unsafe to safe is disclosed, but only in III-C and a table footnote. The dropout closed-loop set, which is not caution-matched, still enters the abstract and conclusion as a primary equivalence claim.
- Fix: Add a short "Departures and post-hoc choices" box or paragraph at the end of Section IV-E that lists all five (clearance change, pedestrian test despite no-go, dropouts, adaptive twin, IMM re-tune addendum). Mark the dropout closed-loop sentence in the abstract "descriptive" instead of "equivalent".

**8. MINOR. AI-assistance disclosure and the related manuscript.**
Location: Acknowledgment; Section I Scope ([10] under review at IEEE Access); Section IV-E ("an AI-based review panel").
- Problem: The disclosure is thorough but long, and the author-confirmation placeholder is open. The sentence "Pre-submission reviews by an AI-based review panel shaped this manuscript" sits in a methods section and is easy to miss. [10] is unpublished, so reviewers cannot check the claimed non-overlap.
- Fix: Move the panel sentence to the Acknowledgment. Offer [10] to the editor as a confidential supplement.

## Submission gates (not findings)

- Author block: affiliation, e-mail and ORCID.
- Repository name and DOI.
- Author confirmation in the AI-use statement.
- Title, being revised. A good title must convey: simulation scope, the equal-caution comparison, and that the finding is a null or equivalence for tracker covariance as a planner margin.

## Strengths

- One falsifiable question, a clear sensitivity control (the amplitude-matched oracle) and a locked plan with hashes: unusually honest evaluation design for the field.
- Results are reported at true size. The null is reported as a null, the 2.8% is called small, and the non-braking-lead costs are not hidden.
- The main text carries every headline number in Tables II to V. The limits paragraph and "Novelty, with its limits" are candid and calibrated.
- The abstract does flag "descriptive", "specified after its share was seen" and "not caution-matched". Most papers do not.
- Table I gives one place for the vocabulary, and the length is held to 10 pages.

## Score

**5.5 / 10.** The substance is a 7; clarity, density and the label inflation pull it down. Sending it to review is reasonable once findings 1 to 5 are fixed. The word budget favours cuts, not additions.
