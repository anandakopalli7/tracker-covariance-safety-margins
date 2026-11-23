# Letter to the author, round 2 of revision v13

22 November 2026

Dear author,

The five seats met on the frozen text (manuscript 893442e4...db958, supplement f915fd79...2426e). The decision is **Major Revision, 6.5 out of 10** (seat mean 6.3). No seat found a wrong number; the labels hold. Nothing is critical. What costs points is that the abstract and conclusion drop caveats the body states.

**Fix first:**
1. Call the dropout closed loop "open-loop-matched", not "caution-matched". Say in V-E that the covariance arm lost 0.18 s more and stopped about 1 m farther back, so the result cannot yet be told from a wider margin. Say the match was made on the older runs, not on the 135 cases. Replace "no extra cost" with "time cost within 0.5 s".
2. Replace "where it tracks the error" for dropouts: your own decomposition says the gain is extra margin for dropout decisions, not ranking. Say a coasting-count margin was not tested, or give its result.
3. nuScenes: say "slightly inversely over all tracks", mark the 99% level, and change "shows" to "is consistent with".
4. Say the recovered shares lie inside your own plus-or-minus 5% equivalence margin, and give the closed-loop equivalence size (0.10 contact share) beside the word "equivalent".
5. Scope the dropout result (random masks, tracks kept three updates, lead braking) and the two-noise IMM (position-velocity interface, a lower bound). Fix the Table III row label and the S4 pointer.
6. Small items in the supplement: "before any of those runs was extracted or scored"; print the 10 Hz within-dropout share; delete the stale Table S34 parenthesis; scope "recount every printed value".

**What the two running controls can add.** With the wording fixed, I expect about 7.0. If the class average at g = 8 and 16 does not match your covariance arm at equal time lost, +0.4; if the coasting baseline loses to the covariance, +0.4; both, about 7.6-7.8. If either goes the other way the score drops to about 6.8, and an honest result is still worth printing. Nothing planned reaches 8: that needs a real-log decision test with room, or an independent replication on another simulator.

**Yours to decide:** the title word "Preregistered" (three seats note IV-E calls the locks local hashes; "Locked-plan" would remove the tension), and the three submission gates.

Record: ARS_REVIEW_ROUND2_v01.md.

The panel
