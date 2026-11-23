# Points the round-2 claim audit must check (session A, 22 Nov 2026, 05:40 EST)

Each item needs an explicit verdict. Items (a)–(i) are the coordinator's (05:36); items (j)–(n) are session A's own interpretive rules and risks. Keys are in `notes\RESULTS_INTERFACE_ROUND2_v13.md`.

**(a) Labels.**
- "Confirmed" appears only for hypotheses of the original plan (A10).
- Tests of A11 and A12 read "passed (amendment)" in running text, "(passed; amendment)" inside brackets and "(A)" in tables.
- The dropout replication reads "replicated under rules fixed before the data" (A12 §1, §3a.3), which requires that its class and passes equal the first dropout test's.
- Secondary results say so: the two-noise IMM on the older fresh runs, the IMM in the mechanism check, the 10 Hz dropouts, the earlier closed loop's higher level.
- Descriptive and exploratory results say so: the mode probabilities, the two-noise IMM's twin, the decomposition, the crossing decomposition.

**(b) The dropout-source sentence (§V-E) and its "not tested" clause.**
- Both numbers must come from the new runs: the substitution share inside a dropout (`DR2.dec.in`, with its interval) and the own-room share among those decisions (`DR2.in.RR_N`).
- "Most of the gain" is session A's rule: printed when the substitution share's lower end is above zero and the share exceeds half of the total (`DR2.RR_N`). Judge it.
- The reading that follows ("the gain comes mostly from the extra margin that dropout decisions get relative to the others … not from ranking them among themselves") is the coordinator's and is descriptive. Judge whether the two numbers support it and whether it overreaches.
- The clause "A fixed margin increase during dropouts might give much of this gain; that was not tested." must be present.

**(c) The caution-matched closed loop (E5) and its caveats.**
- Numbers: contacts per arm, the contact difference with its interval, the time lost with its interval, the matched cautions, the class (`E5.*`).
- The caveats must be in the main text: the class average's scale sat at the bottom of its calibration grid; the match is open-loop; one level; lead braking only. "One simulated configuration" must stand in the abstract and the conclusion.
- "Fewer contacts … for 0.18 s more time lost" must not read as a claim of equal closed-loop caution.
- A12 §6.5's disclosure (the covariance arm's scale was set on runs whose dropout results had been seen; no shared case) must be in S15 or Table S5.

**(d) The real-log mechanism check (M1) and its disclosure.**
- The primary statistic is τ over pairs around real missed detections, at its calibrated level (`M.tau`, `M.ci`, `M.level`); the all-pairs τ is descriptive (`M.all.tau`).
- The disclosure must be printed: the primary population was chosen on the training split, after the all-pairs statistic there was found to be dominated by steady tracks; validation was scored once.
- The text must not turn the check into a decision result. The abstract's "ranks the realised error around real missed detections … but not over all tracks" is the limit.

**(e) The real-log decision test under dropouts (§5b).**
- Its room test failed, so nothing was tested there; the text must say no more than that, and must not report its class.
- It is not in the Holm family.
- The conclusion and contribution 2 say that no real-log decision test was possible. Check that this follows from the logs and is not attributed to the simulated cut-in runs.

**(f) The dose-response wording.**
- "Rises with the dropout rate up to a start probability of 0.20 and then levels off" is session A's rule: printed when the shares rise over the first three probabilities and the fourth is not more than 5% above the third. Check it against `DR2.r_p005` to `DR2.r_p030`.
- The slope keeps "passed (amendment)" (`DR2.slope`, `DR2.slope.ci`). Judge whether "levels off" beside a passed linear trend misleads.
- The four values must be in the supplement table the sentence points to.

**(g) Holm (A12 §4), once the final file is in.**
- The family has six hypotheses; a pair not completed by the cut-off enters as p = 1.
- The main text gives no p-value: it says in words how many of the six stay significant at a family-wise 0.05. Session A counts a hypothesis only if it is rejected under both conventions of the table. Check the count and the names against `work\shared\holm\A12_HOLM_v01.json`.
- The Holm values in S15 are one-program values and must carry the mark.
- Holm changes no label.

**(h) The two-noise IMM (A12 §3c).**
- Numbers on the new runs (primary) and the older fresh runs (secondary): `B.IMM2N.*`, `B.IMM2C.*`.
- The disclosure of the quiet mode's noise must be printed (Table S5 or S15): the rule's window could not be reached on frames before braking, so the filter of record was used; changed on tuning runs only, before any new-run value.
- The older fresh runs' values are secondary and "specified after the IMM's results on those runs had been seen".
- The abstract's "2.2% for a two-noise interacting-multiple-model tracker" stands beside "helps a little"; check that no sentence presents it as large or as an equivalence.

**(i) The crossing decomposition (exploratory).**
- Main text: "an exploratory decomposition attributes 54% of its explained variation to the update schedule, 38% to the geometry and 8% to the realised error". These are shares of the explained variance, not of the variance (`XH.bind.share.*`; the explained share itself is `XH.bind.r2`, in S15).
- "It varies there for other reasons" and the abstract's "varies for other reasons" rest on this exploratory analysis. Judge whether the label and the wording are adequate.

**(j) "Helps a little" and "tracks the error" (the framing).**
- The abstract, contribution 2, §VI and the conclusion say the covariance helps "only where it varies with the real error". The evidence for "tracks the error" is indirect: the decomposition under dropouts, the mode probabilities of the two-noise IMM, and the nuScenes τ. Judge whether the framing claims more than these show.
- The abstract's opening verb is "beats". Judge it against results that are small and, in closed loop, not caution-equal.

**(k) What left the main text.** Check that each is still printed where the text points:
- Fig. 3 as Fig. S2 in Supplement S9;
- the closed loop's per-arm numbers in Table IV;
- the sprint closed loop's higher-level numbers in Supplement S14;
- the dropout efficiency in Table S34;
- the two-noise IMM's twin difference in S15;
- the stop-reliance share in Table S14's caption;
- the dose values in S15's table.

**(l) The sprint panel's required wording (R1–R12) must survive.** In particular:
- R2: no dropout "equivalence";
- R4: the earlier closed loop's higher level "cannot be told from a wider margin";
- R5: the abstract keeps the 20% baseline and the time gap;
- R6: crossing "shows no recovery";
- R7: no adjustment across sequences, and the locks are local hashes;
- R8: the closed-loop levels are not deployed operating points;
- R11: "no room" tests nothing;
- R12: "one simulated configuration".

**(m) The abstract.** At 250 words it no longer names the adaptive filter or the per-arm closed-loop margin. Check that no confirmed result of the original plan lost its size, and that every number in it has a two-program source.

**(n) The model statement.** The Acknowledgment must say that Claude Opus 5.5 wrote the first programs and the text, that Claude Fable 5.2 revised the text for the second amendment, and which models audited the claims; the round-2 audit is by Claude Sonnet 5.5. Supplement S12 describes the audit without naming models.
