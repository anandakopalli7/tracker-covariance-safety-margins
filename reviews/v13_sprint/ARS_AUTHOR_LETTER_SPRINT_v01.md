# Letter to the author: v13 sprint review

Dear author,

**The verdict.** The panel's decision on the frozen text is **major revision**, 3 stars, **6.3 out of 10**. With tonight's wording fixes it becomes about **7.0** (3.5 stars). It does not reach 8.5, and no wording can take it there. At OJ-ITS, review followed by a major revision is most likely; rejection is possible.

**What is good.** The numbers reproduce (30 of 30 checked), and the plans, locks and deviations are recorded unusually completely.

**What is wrong, in plain words.** Yesterday's added tests are honest, but the text calls them "confirmed" in the same voice as the original plan, although they were written after the main results were known. Three phrases claim more than the tests show:

- The dropout result is called "inside the equivalence margin". No such test was registered.
- The 2.8% gain under dropouts is not found inside the dropouts themselves (−0.003 there).
- "Safer at no extra cost" in the dropout closed loop describes an arm that was not caution-matched and lost 0.25 s more.

**What changes tonight (12 wording items, no new numbers).**

- Amendment tests are labelled "passed (amendment)", not "confirmed".
- The dropout "equivalence" is removed, and the text says where the gain is not found.
- The dropout closed loop becomes "fewer contacts for more time lost".
- The abstract says a plain time gap did as well as the braking prediction.
- Crossing becomes "no recovery shown"; "no room" in cut-in and nuScenes is said to test nothing.
- The text states that sequences are not adjusted for one another, that the locks are internal, that the closed-loop contact levels are not deployable, and that the headline equivalence was expected.
- Section V-E is split, and scope becomes "one simulated configuration".

**What would raise the score later.** New evidence only:

- a pre-registered test, with an outside timestamp, where the covariance varies and there is real room;
- the dropout mechanism shown (gap rows, re-born tracks, longer masks);
- a fair IMM with two noise levels;
- a caution-matched closed loop under dropouts;
- a second planner or detector, or real logs with room.

One caution: every reviewer here is a Claude model, so their agreement is weaker than that of independent human reviewers.

The full record is `ARS_REVIEW_SPRINT_v01.md`.

The editor-synthesis seat (Claude Fable 5.2)
