# ARS review, round 2 of revision v13: panel record (v01)

- **Written by:** the editor-synthesis seat, Claude Sonnet 5.5 (not the round-2 text's writer, Claude Fable 5.2, nor the earlier writer, Claude Opus 5.5). Read-only apart from this folder; no web, no installs.
- **Frozen text reviewed:** `revision_v13\work\A_text\out\freeze_v13_0623\`, `MANUSCRIPT_v13.md` sha256 `893442e4437e01fa6159dd9bbb8ebae21af65508a70064890b17929cf70db958`, `SUPPLEMENT_v13.md` sha256 `f915fd798bbc9d3c53c56cea74d5b0ea4279463f3f3385b0e93488dba802f426`. Both hashes were checked at the start and again at the end; both times equal to the frozen values.
- **Read:** the five seat reports, the provenance file, both frozen files (manuscript in full; supplement S15 and Tables S34, S38-S45 in full), the claim audit (extra check, not a seat), and AMENDMENT_12 for what was fixed before the data (sections 0, 2, 4, 6). Not read: response letter, earlier rounds, anything named <excluded folder 1> or <excluded folder 2>, the secrets folder.
- **Gates, not findings:** author block, repository name and DOI, the author's AI-use confirmation.
- **Seat limits:** all seats are Claude models; two (R1, DA) share the round-2 writer's model and one (R2) the sprint writer's. Correlated error is reduced, not removed. R1 and the claim audit compared printed values with the exports (57 of 57 match, no wrong number found); I did not re-run any export.

## 1. Seat table

| Seat | Model | Recommendation | Score (of 10) | Stars (of 5) |
|---|---|---|---|---|
| EIC, journal fit | Claude Sonnet 5.5 | Major revision | 6.0 | 3.0 |
| R1, methodology | Claude Fable 5.2 | Major revision (light) | 6.5 | 3.5 |
| R2, domain | Claude Opus 5.5 | Major revision | 6.5 | 3.25 |
| R3, practical | Claude Sonnet 5.5 | Major revision | 6.5 | 3.5 |
| DA, devil's advocate | Claude Fable 5.2 | Major revision | 6.0 | 3.0 |
| Claim audit (not a seat) | Claude Sonnet 5.5 | none (1 H, 11 M, 13 L; no wrong number) | n/a | n/a |

## 2. Panel decision and score as frozen

- **Decision: Major Revision.** Unanimous (5 of 5). No seat says reject; none says minor.
- **Seat mean 6.3; median 6.5.** **Score as frozen: 6.5 of 10 (about 3.25 to 3.5 stars).** I use the median, not the mean, because the two seats at 6.0 each priced one problem (the closed-loop wording; the missing coast control) that the other three also price at 6.5 and that is mostly wording. I do not go higher: the five seats agree the paper's honesty and checking are strong and that its positive results are small, simulated and not yet separated from a plain "wider margin while coasting".
- **Why not lower:** every printed number was reproduced by two programs; labels ("confirmed", "passed (amendment)", "replicated under rules fixed before the data") hold up against the amendment record; the body discloses nearly every limit the seats raise. The damage is in the abstract and conclusion, which drop caveats the body states.
- **Why not higher:** the one confirmed covariance result is a near-tautology (the paper says so); the positive results are 2-3% of room, inside the paper's own +/-5% equivalence margin; the strongest alternative explanation (extra margin while coasting; extra closed-loop caution) is untested; no real-data decision test had room.
- **Likely editorial outcome (IEEE OJ-ITS):** major revision, with a real chance of rejection from a referee who weighs the near-tautological confirmed result and the one-day amendments heavily (DA, EIC).

## 3. CRITICAL items

**None.** DA rated the caution-matched closed-loop wording "CRITICAL as worded (a text fix resolves it; the data are not in doubt)". Ruling: **not CRITICAL; it is the top REQUIRED item (R-1).** Facts checked in the frozen text:
- V-E (the closed-loop paragraph) already states, in the same paragraph as the 21% against 33%, that the class average's scale "sat at the bottom of its calibration grid (contact share 17% there), the match is open-loop, and only lead braking at one level was tested". Supplement S15 repeats it and Table S43 prints the 0.18 s and the rest gap.
- What is not stated, and is what turns a major item into the lead one: (a) the abstract and the conclusion carry the bare phrase "caution-matched closed loop" and no qualifier; (b) the main text never gives the closed-loop rest gap (0.98 m [0.60, 1.39], covariance arm farther back), which shows the covariance arm was the more cautious arm where the outcome was measured; (c) the match was made on the older 105 runs' open-loop arrays, but the V-E sentence reads as if it were on the 135 closed-loop cases (the audit's one H; I confirm the sentence: "matched the two arms by open-loop caution (18.2% against 18.4%) on 135 fresh cases"; S15 and A12 6.5-6.11 say the match is on other runs).
- No number is wrong and the body does not hide anything; a reader of the abstract alone is misled in degree. That is a major wording defect, not a critical one.

## 4. Adjudication of disputes between seats

| # | Dispute | Ruling and facts checked |
|---|---|---|
| D1 | Severity of the caution-matched closed loop: DA CRITICAL; EIC, R1, R2, R3 MAJOR | **MAJOR, required first** (see section 3). The result may still stand at equal closed-loop caution (DA says so); it has not been shown. E6 (class average at g = 8 and 16 on the same 135 cases) is the test that decides it. |
| D2 | Did calibration "miss its target twice" (R1: 17% on tuning, then 33% on test; R3 similar)? | **Partly.** The scale rule was fixed before any run (A12 6.4: g_D is the grid value whose contact share is nearest 0.20, with g = 4 if all are lower): shares were 17%, 13%, 7%, 0% at 4, 8, 16, 32 (S15), so g = 4 follows from the rule, not from a choice after the data. The 17% rests on 5 of 30 cases (a wide interval); 33% is on 135 different cases, so the jump is partly sampling and case mix. What is true: the class average's contact level was never bracketed around 20%, and the grid floor is the weakest reference. Print both shares with their n and say "17% on 30 tuning cases". |
| D3 | Is the dropout gain "covariance" or "a coasting flag"? R2, R3, DA, R1 want a coast-count or fixed-increment baseline; EIC wants only the wording changed | **The control is a real gap, not only wording.** V-E itself says "A fixed margin increase during dropouts might give much of this gain; that was not tested". The decomposition (Table S40: 0.0206 [0.0050, 0.0363] of the pooled room inside dropouts; own-room share among dropout decisions 0.009 [-0.008, 0.024]) says the gain is extra margin for dropout decisions. Until the coast baseline is scored, the abstract's "where it tracks the error, it helps" and VI's "A covariance helps a planner where its variation tracks the realised error" are stronger than the data. Wording fix is required either way; the coordinator's flag/coast control is the data fix. |
| D4 | Does "not from ranking" overreach (audit 6)? vs R1/R2/R3 who accept it | **Audit is right on tone.** The interval's upper end is 0.024 and V-E adds "as the covariance grows during a dropout", a mechanism no printed number shows. Soften to "fits extra margin more than ranking (descriptive)". Also print the 10 Hz within-dropout share (R1 reports 0.035 [0.014, 0.054] from the 10 Hz export, which would contradict an unqualified "not ranking"; I did not open the export, so I treat it as R1's checked claim and require it be printed). |
| D5 | "Preregistered" in the title: EIC (MAJOR), R3 (minor), DA (MAJOR) | **The title is the author's choice; not a required item.** Facts: IV-E says "SHA-256 hashes with local file times, not a public registry or third-party timestamps"; Table I says amendment tests were "written after the fresh lead-braking results were seen". The paper discloses the limit itself, so the contradiction is inside the paper's own text, not hidden. Listed as an author decision (section 7). |
| D6 | Is the nuScenes tau "shows ... on real data" overstated? EIC MAJOR, others MINOR | **Required wording fix, MAJOR in effect for the abstract.** Table S44: primary 0.108 [0.039, 0.172] at the 99% fallback level (bare in the abstract); all pairs -0.038 [-0.070, -0.006]; steady tracks -0.075 [-0.109, -0.043] on 40,228 rows; the abstract says "but not over all tracks", which understates an interval below zero; VI says "as the nuScenes check shows on real data". Also the primary pairs need only one member in or after a miss (A12 5.4, per R1 and DA), so tau largely contrasts missed with steady tracks. |
| D7 | Should the two-noise IMM's 2.2% be read as "a manoeuvre mode helps"? R2 MAJOR (interface lower bound); others silent | **R2 is right.** III-D states, for "the IMM as tuned here", that the planner receives only the position-velocity block and predicts at constant velocity. V-E/VI do not carry that limit to the two-noise IMM, and VI sets its gain "small beside the braking prediction's". Table S8 (R2): the acceleration margin recovers 0.369 of the room. Required: "same position-velocity interface; a lower bound". Re-scoring with the full propagated covariance is suggested, not required. |
| D8 | Closed-loop equivalence size in the abstract (R3 MAJOR; audit M) | **Required, one parenthesis.** Abstract: "as it is in closed loop" has no size; Table IV: +/-0.10 contact share on 60 cases at 20% base rate; V-C says "Equivalent here does not mean safe". The dropout closed-loop effect (-0.12) is about the size of that margin. |
| D9 | Shares inside the +/-5% margin (DA 3, MAJOR; no other seat) | **Valid, required as one clause.** IV-C: equivalence is an interval inside (-0.05, 0.05); "recovers" needs only an interval above zero. 0.0283 [0.0064, 0.0496], 0.0298 [0.0077, 0.0518] (upper end slightly above 0.05) and 0.0220 [0.0185, 0.0253] all lie at or inside that margin. This is the plan's rule, not a fork; the defect is that the reader is never told. |
| D10 | Main-text table for the round-2 results (EIC MAJOR) | **Suggested, not required.** The claim is fair (V-E is 774 words with no main-text table), but body is 5,747 of 5,750 words, tables and captions 1,940 words (plan: 1,400), 10 pages (EIC, from BUILD_REPORT). A new table needs an equal cut (EIC: Table III rows). Can be done only if page count allows. |
| D11 | Steady-track margin is lower in the dropout arm (R3 5) | **Plausible, not shown.** Table S40 shows steady-decision substitution share 0.0035 [-0.0054, 0.0125]; no printed number shows the steady-track margin lower. Suggested sentence "closed-loop effect elsewhere untested" (V-E already says one level, lead braking only). |
| D12 | "Real-log result unchanged: no room" | **All seats agree** the no-room statements are correctly worded ("nothing was tested"). No finding. |
| D13 | Multiplicity: Holm covers six second-amendment primaries only | **Disclosed and arithmetically correct** (R1 and audit recomputed by hand; all six reject under both conventions; largest adjusted p about 0.012 even with the failed real-log test added, per R1). Required only: say in V-E which six and that the first amendment and original sequences are outside it. The 188 values marked as one-program include the whole Holm table while IV-E says second programs "recount every printed value" (checked in IV-E): scope the sentence. |

## 5. REQUIRED items

All are wording or one offline print. Each needs a word cut: body 5,747 of 5,750, abstract 250 of 250 (cuts: "simulated" in the abstract; "second amendment" and "fresh" in V-E; duplicate "(descriptive)").

| # | Location | Fix, fewest words | Seats |
|---|---|---|---|
| R-1 | Abstract; V-E closed-loop paragraph; VII; I contribution 2 | Say "open-loop-matched closed loop", not "caution-matched". In V-E add: "in closed loop the covariance arm lost 0.18 s more and stopped about 1 m farther back (rest gap 0.98 m), so it cannot be told from a wider margin"; "17% on 30 tuning cases". Say the match was on the older runs and the 21% against 33% is on 135 new cases. | EIC 2, R1 1-2, R2 W3, R3 1-2, DA 1, audit 1, 2, 13 |
| R-2 | V-E closed loop; Table S43 caption | "safer at no extra cost" to "safer; time cost within the plan's 0.5 s tolerance" (0.18 [0.11, 0.26] excludes zero). | R1 14, R2 W10, DA 1, audit |
| R-3 | Abstract; V-E dropout-source sentence; VI "What a varying covariance needs"; VII | Replace "where it tracks the error, it helps" with "where it grows when detections are missed, it helps a little". V-E: "fits extra margin for dropout decisions more than ranking among them (descriptive); a coast-count margin was not tested [or: was beaten / was not beaten: control result]". Delete "as the covariance grows during a dropout". | EIC 3, R1 3, R2 W2, R3 6, DA 2, audit 6 |
| R-4 | Abstract first sentence; VII first sentence | Universal "only where it varies" to "In these tests, ... only where ...". | R1 5, DA 5, audit 22 |
| R-5 | Abstract; V-E last paragraph; VI "as the nuScenes check shows" | "and slightly inversely over all tracks"; mark the interval "99%"; VI: "is consistent with" for "shows"; one clause: pairs mostly compare missed with steady tracks; print the training value 0.190 beside 0.108. | EIC 4, R1 6-7, R2 W9, DA 6, audit 4, 12 |
| R-6 | Abstract; V-C text | After "as it is in closed loop" add "(within 0.10 contact share)". | R3 4, audit 3 |
| R-7 | V-E opening or dropout paragraph | One clause: "these shares lie inside the +/-5% margin used for equivalence". | DA 3 |
| R-8 | V-E opening; VI Limits | Dropout results hold for random truth-independent masks of one to three updates with tracks kept three updates (an output-rule change), lead braking; no decision-level real-log support (the real-log injected-dropout test had no room). Limits currently never names dropouts. | R3 3, DA 7, EIC 2 |
| R-9 | V-E two-noise IMM paragraph; VI; Limits; Table III row label | Add "same position-velocity interface; a lower bound"; VI: drop "does the same ... small beside the braking prediction's" or recast as a channel comparison; add "its share exceeds its own oracle (0.022 against 0.013), so the gain is a phase-level effect"; Table III row: "(older runs, secondary)" (it prints 0.0250 not the primary 0.0220); pointer "Supplement S4" to "Supplement S15" (S4 has no two-noise text, audit and R2). | R2 W1, W5, W16; R1 13; DA 10; audit 9, 16 |
| R-10 | V-E crossing; VI | "no permuted-twin test of the covariance was run"; "mostly for other reasons" in V-E, abstract and VII, with "(exploratory; R2 0.47)"; VI "Missed detections make it grow when the estimate is worse" narrowed to "under injected lead-braking misses" (the same schedule term is "other reasons" in crossing, Table S45: 54% explained). | R2 W4, W15; R1 16; audit 7, 11 |
| R-11 | S15 dropouts-on-new-runs ("rules fixed before those runs existed") | "before any of those runs was extracted or scored". Facts: capture began 00:37-00:40 (A12 section 2 line 67), LOCK_A12a 00:47:51 (R1). The main text's "fixed before the data" is defensible for scoring; the supplement sentence is not. | R1 8 |
| R-12 | S15 10 Hz paragraph and Table S34 row | Print both within-dropout shares (2 Hz 0.009; 10 Hz 0.035 [0.014, 0.054] per R1) and limit "not ranking" to 2 Hz; state the 10 Hz class average is the 2 Hz one under the 2 Hz masks, and the masks and coast limit in seconds; delete the stale Table S34 parenthesis "(the gain is not concentrated there if this is near zero)" (line 799; contradicts Table S40). | R1 4; R2 W7; audit 8, 10 |
| R-13 | IV-E; V-E last sentence | "recount every value printed in the main text" and mark Table S38 as one program; say Holm is over the second amendment's six, naming them (replications and post hoc tests), and that the first amendment and original sequences are outside it. | R1 10-11, EIC 9, DA 8, audit 18 |
| R-14 | Abstract end | "at 2 Hz, no latency" (Table S5 row and VII say the abstract states it; it does not now); add "mainly at 2 Hz" since a 10 Hz result is reported. | audit 5; R2 W13 |

Held to the word budget: the abstract can take R-1, R-3, R-4, R-5, R-6, R-14 only by cutting about 12 words (list above) and by moving the verdict first (S-1).

## 6. SUGGESTED items

| # | Location | Suggestion | Seats |
|---|---|---|---|
| S-1 | Abstract | Lead with the verdict in plain words, keep three numbers, move the rest to the body (about 14 numbers now; first sentence carries a parenthesis; "caution-matched", "room", "share" used before Table I). | EIC 6, R3 13, DA, R2 |
| S-2 | V-E, new main-text table | One table: claim, test, label, size, Holm p, caveat; pay for it from Table III rows (keep online, IMM, two-noise IMM) and V-D prose. Only if pages allow. | EIC 1, 12, 13 |
| S-3 | VI / VII | Practitioner sentence (use a time gap or braking prediction before tuning a covariance) and a symmetric last sentence: "no support for the covariance in steady tracks; some support in simulated dropouts; none for dropping or keeping it elsewhere". | EIC 7, R3 12 |
| S-4 | Title | The author's choice. "Locked-plan" or "(locally hashed)" would remove the contradiction with IV-E; keeping it is defensible only because IV-E and Table I disclose the limit. | EIC 5, R3 10, DA 4 |
| S-5 | IV-E | Move nine hash prefixes to Table S5; keep "locked before data, local file times". | EIC 10 |
| S-6 | Table I; V-B | Drop NA and AM; expand CANMOT, CARLA, PS; define "two-noise IMM" in Table I; re-tuned IMM's share (0.0055) in one clause. | EIC 11, R2 W6, W13 |
| S-7 | VI | One clause on the NIS-adaptive filter (largest share, 0.046, passed twin test) in "What a varying covariance needs". | R2 W14 |
| S-8 | S15, Table S39; V-E | Attribute the dose-response plateau (0.0525 then 0.0514) to the mask law's caps; tag "levels off" descriptive; define "start probability". | R2 W8, audit 15 |
| S-9 | S15 | Two-noise IMM detail: name the quiet filter; rows for transition diagonals 0.90 and 0.98; score non-braking leads; offline re-score with full propagated covariance. | R2 W1, W5 |
| S-10 | V-E / S15 | Real-log tau: state class handling and static objects; give tau of N/F0 and the IMM's 0.210 in one clause; add Spearman (A12 3a.4 asked for it, audit). | R2 W9 |
| S-11 | VI; Limits | Add two citations (Sinopoli et al. 2004 on Kalman filtering with intermittent observations; Mehra 1970) and name detector-driven measurement noise as an untested source of variation. DOIs not verified by the seat; author to check. | R2 W12 |
| S-12 | Table S43 | Caption: differences are paired case means; peak deceleration over contact-free pairs; explain 18.2% against 16.9% masked (masks fixed per case); state the full-braking share (65.4%) in the main text. | R1 2, 15; R2 W11; R3 7 |
| S-13 | V-E, V-D | Add the closed-loop time-lost range behind non-braking leads (S25) so a designer can weigh it; name who bears the 0.18 s. | R3 8-9 |
| S-14 | V-E crossing; VII | "classed as" not "passed" for null results; drop "its oracle: 69%" from the conclusion (no permuted-twin test for N). | EIC 8 |
| S-15 | AMENDMENT_12 audit trail | Two stated times postdate their locks (bootstrap draw "about 00:55" vs lock A12a 00:47:51; section 5 v02 "about 03:55" vs LOCK_A12c 03:35:07): record both in an erratum. I confirm 00:55 appears at A12 line 35 and 03:55 at line 426; I did not open the lock files. | R1 9 |
| S-16 | Response letter | Add the real-log injected-dropout test, the 10 Hz configuration and Holm; confirm the page count on the typeset file. | audit 21 |

## 7. What was fixed before the data and what after (from AMENDMENT_12)

- **Before its data, holds up:** the six Holm primaries; the replication's mask law, output rule and class; the dose slope; the two-noise IMM's design and tuning rule; the closed loop's scale rule and match table (computed before any calibration run, A12 6.5); the mechanism check's gate, strata and horizon.
- **After related results, disclosed:** dropouts and the twin test (first amendment, after the fresh lead-braking results); the mechanism check's primary population (chosen on the training split); the two-noise IMM's quiet mode; the closed-loop arm's scale (matched on runs whose dropout results were known); the rear-contact rule; pedestrian crossing despite its no-go. The second amendment's approval record states its aim as removing a review panel's blockers inside a 12-hour window: rules were locked before each dataset, but which tests to add was outcome-aware. DA judges the paper's statement that the reviews "shaped this manuscript" sufficient; I agree.
- No label in the manuscript is stronger than the amendment record supports. "Confirmed" is used only for the original plan.

## 8. Forecasts (honest; panel scale; not inflated)

The score now is 6.5. A score moves with what a referee can still object to, not with how many fixes were made.

| Scenario | Score | Reasoning |
|---|---|---|
| **A. Required wording fixes only (R-1 to R-14)** | **7.0** (range 6.8-7.2) | Removes the overreach all five seats priced (abstract and conclusion against the body). The paper stays an equivalence result plus small simulated positives whose best alternatives are untested; seats' own post-fix numbers: EIC about 7 (with a table), DA 7, R1 7.5 only with controls. |
| **E6: N better than the class average at equal time lost** (class average at g = 8 and 16 on the 135 cases; N's contacts below the class average's interpolated at N's time lost) | **7.4** (A + 0.4) | Turns the headline closed-loop result from "cannot be told from a wider margin" into a result at equal closed-loop caution; the thing R1, R2, R3 and DA each named. Still one level, lead braking, random masks, so no more than +0.4. |
| **E6: not shown** (N lies on or inside the class average's contact-versus-time curve) | **6.8** | The lead positive becomes "consistent with extra caution". The wording of R-1 already assumes that, so there is no further damage, but the paper loses its strongest positive: slightly below A. Honest result, and I would count it to the author's credit. |
| **E6: not bracketed** (N's time lost outside the class average's range at g = 4, 8, 16, or contacts do not fall monotonically) | **6.9** | Neither shown nor refuted; the claim is limited to "not separated from a wider margin" and the closed-loop sentence shrinks. About A, minus a little for the unresolved question. |
| **Coast baseline: covariance beats it** (class average times a coast-count factor fitted on disjoint runs, scored on the 150 new runs) | **7.4** (A + 0.4) | Answers the missing control all four of R1, R2, R3, DA named as their top change: the covariance then adds something a track flag does not. Gains stay 2-3% of room, simulated, random masks. |
| **Coast baseline: not shown** (equals or beats the covariance) | **6.8** | The thesis must be restated as "a margin that widens while a track coasts helps". Honest, and a useful practitioner message, but the paper's "where it tracks the error" story would then lose its only open-loop support, and the novelty falls. The paper's honesty keeps it above 6.5. |
| **Both favourable** (E6 shown and coast beaten) | **7.6-7.8** | The two largest outstanding objections are answered. |
| **Both unfavourable** | **6.6-6.8** | Wording-only paper with its positives explained away; it would still read as a careful null study. |

Not additive in the middle: one favourable and one unfavourable lands near 7.0. The forecasts assume the wording fixes are done well and the abstract stays inside 250 words; a wording fix that adds a number-dense clause loses about 0.2.

## 9. What still keeps the score below 8, and whether wording can fix it today

1. **The confirmed result is a near-tautology.** The fixed-noise covariance is near-constant by the Riccati steady state, and the equal-caution sweep removes scale; the paper admits this. Cannot be fixed; wording only frames it (already done).
2. **The positive results are small and inside the paper's own margin.** 2-3% of room, intervals inside +/-5% (D9). Wording can say so (R-7); only new tests with a larger or clearer effect change it.
3. **One simulator, detector, planner, road and update rate; random truth-independent masks.** 10 Hz is secondary and dropout-only. Wording can scope it (R-8, R-14); real-sensor breadth needs data.
4. **No decision-level evidence on real logs.** nuScenes and cut-in showed no room; the tau check is weak and inverse over all tracks. Wording can state it (R-5); only a real-log set with room fixes it. This is probably the single largest barrier to 8.
5. **Process.** The second amendment's tests were chosen after seeing results in a review-driven sprint, locks are local hashes, nearly all authorship acts are AI, second programs share the scoring library and arrays (disclosed), and the author's personal-verification statement is blank (gate). Wording cannot remove it; the author's own confirmation of what was verified would help (gate).
6. **Density.** At the 250-word abstract cap and 5,750-word body cap, with no main-text table of the round-2 results (S-1, S-2). **This one can be mitigated today by restructuring, not adding.**

**Fixable today by wording alone:** R-1 to R-14 and S-1, S-3 to S-8, S-12 to S-16 (items 2, 3, 4 and 6 only in the sense of stating them honestly). **Not fixable by wording:** items 1, 4 (real-log room) and the untested alternatives unless the two controls come back. Even with both controls favourable the paper reaches about 7.6-7.8, not 8; reaching 8 needs a real-data decision test with room or an independent replication of the dropout result on a second simulator or detector.

## 10. Hashes

Manuscript and supplement hashes re-checked at the end of this review: equal to the frozen values at the top.
