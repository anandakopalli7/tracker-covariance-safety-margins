# Letter to the author: final review of v13 (22 Nov 2026, 12:30 EST)

**Decision: major revision, a light one. Score as frozen: 6.3 out of 10 (about 3 stars of 5).** Five reviewers scored 6.0, 6.6, 6.5, 6.8 and 5.5. Nobody found a wrong number or a wrong label, and nobody found a blocking problem. Every value they traced matched its source. What they found is wording that claims a little more, or a little less, than a test shows, and some facts that live only in the supplement.

**What to expect.** After the fixes below I expect about 6.7 (range 6.5 to 6.9). It stays below 8 because of things wording cannot change: the confirmed result is a near-constancy null that could hardly fail; the gains are 2% to 5% of the room and both last controls failed; one simulator at 2 Hz; no real-log decision test; amendments written after results; all text and code written by AI under one author. The one thing that would lift it most is new work (a decision test on real logs or a second simulator, with a third-party timestamp), which is not part of a fix round.

## The 19 required items, easiest first

None needs a new run. Details, locations and exact wording are in `ARS_REVIEW_FINAL_v01.md`, section 4.

**A few words each (wording only)**
1. R-4: replace "a lower bound" for the two-noise IMM with "holds for that interface only" (V-E and Limits). Nothing in the paper shows the sign.
2. R-6: split the Holm sentence in IV-E, because "they" reads as if the original lead-braking list were Holm-adjusted. It is not; the six Holm tests are the H rows of Table 6.
3. R-3: say the "inside the ±5% margin" holds as point values at dropout start probability 0.10, and about 5% at 0.20 and 0.30. The Conclusion dropped both qualifiers.
4. R-9: put "internal hash-locked plan; amendments written after the fresh results" in the abstract. The title stays your choice; the body already says this, the abstract does not.
5. R-10: add "exploratory" to "varies mostly for other reasons" (abstract, Section I, Conclusion).
6. R-5: add "with a constant-velocity prediction" to the first sentence and to Scope, and one sentence in the Discussion: the room is almost all braking onset, which a fixed-noise covariance cannot track.
7. R-1: the coast-count factors are the covariance's own median ratios. Say so, and change "needs no covariance" to "needs no per-decision covariance".

**A sentence or two, plus a value that already exists in the supplement**
8. R-7: put the third amendment's Holm values (0.18 and 0.99, Table S38) beside the two failed labels in Table 6.
9. R-15: say the primary dropout start probability is 0.10 and masks 16.2% of updates (Table S39).
10. R-17: say the headline interval is 99.4% (Table S9), not 95%, in the Table 2 caption.
11. R-2: add the IMM's nuScenes numbers (0.210 around misses; +0.093 over all pairs; Table S45) and say "the fixed-noise tracker's spread" in the abstract and Conclusion. The reviewers' main complaint: the one tracker that can vary has the opposite sign, and the main text leaves it out.
12. R-16: add how the equal-time-lost test was read (linear interpolation between scales 4 and 8: 25.7% against 20.7%; 89 of 135 cases; Table S44).

**Text you write from your own records (no new analysis)**
13. R-13: describe the pedestrian-crossing scenario in two sentences. It is described nowhere in the paper or the supplement.
14. R-14: define "time lost" and "rest gap" in one clause each (also found nowhere).
15. R-12: one sentence in IV-E saying the three amendments were written and locked 21 to 22 Nov 2026, after AI-panel reports, and that the panel asked for the third's two controls. Then check "the author ... made the scientific decisions": the amendment files record some design choices as the coordinator's (an AI session). Use words you can stand behind, for example "approved its plans and design decisions".
16. R-8: rewrite the abstract's first sentence, the Conclusion's first sentence and contribution 2 so they are two-sided: nothing where the covariance is near-constant; 2% to 5% of the room where it varies (include the noise-adaptive filter's 4.6%, replicated); a coast-count margin matches the dropout gain. Make the Conclusion not repeat the abstract. Keep the abstract at 245 words or fewer (it is exactly 250 now).
17. R-11: fix the AI paragraph (see below).

**Needs a literature check by you**
18. R-18: add "under regular updates" to the steady-state sentence, and place intermittent-observation Kalman filtering, data-dependent covariances and ITS threat-assessment work in Section II. One reviewer suggested references from memory; none was verified, so check every one before use.

**Format**
19. R-19: the format list (section 7 of the record): reference [26], [37], [38] places; [39] year; [40], [41] dates; Fig. 4 labels below the panels; Fig. 2 caption versus legend and the unlabelled right axis; the AI paragraph's first sentence; "[7], [22], [8]"; prefix hyphens; "1 s" line break.

## The AI paragraph (R-11 and Q8)

Both versions meet IEEE's rule in form. The frozen one says the second programs recount "every printed value", but Section IV-E says every main-text value and all but the marked (‡) supplement values; and it says Fable 5.2 revised the text "for the second amendment", while the record shows Fable 5.2 wrote the round-2 text and the submission pass. Your shorter version is better organized but understates in four places: it drops the AI panel, says you "made every scientific decision" (the amendment files do not support "every"), says "wrote" without "ran", and does not name the Abstract. I recommend the shorter one with those four put back; the full text is in section 8 of the record. No wording hides the extent of AI use and none should try; the risk that remains is the fact itself.

## The gates that are yours

- The repository name and DOI in the ACKNOWLEDGMENT.
- Your AI-use confirmation sentence. Write acts, not adjectives (what you read, what you checked, what you approved), and make sure each statement is literally true before signing. The same goes for "approved its plans and design decisions" and the sentence about AI sessions' design choices in the recommended paragraph.
- Whether to keep the title word "Preregistered". The body already qualifies it; the abstract should too.
- Checking any new reference, and the "et al." lists ([9], [13], [15], [21], [31]) against author counts. None of this was checked online.

Files: `ARS_REVIEW_FINAL_v01.md` (the full record) and this letter, in `review_v13_final_output\`.
