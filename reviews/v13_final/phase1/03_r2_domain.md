# Final v13 panel, Phase 1, seat R2: Peer Reviewer 2 (Domain)

- **Seat:** R2, Peer Reviewer 2 (Domain). This one seat only: no sub-agents, no other seat, no synthesis.
- **Model:** Claude Opus 5.5 (`claude-opus-5-5`). Much of the earlier text was written by this same model, so I read it with deliberate skepticism and checked claims against the tables and the supplement rather than the prose.
- **Card:** "Card 3: Peer Reviewer 2 (Domain)" in `review_v13_output\00_phase0_field_analysis_and_cards.md` (I read only the card and the field analysis). Identity unchanged: researcher in multi-object tracking and Kalman estimation for road vehicles (NIS/NEES consistency, adaptive and multiple-model filtering, uncertainty passed to prediction and planning). Focus anchors re-pointed to the brief: (1) the near-constant covariance and its mechanism, now Sections V-B and VI, Table 3, Supplement S11; (2) the tracker variants, their tuning and consistency, and whether the IMM arms test "a covariance that varies", now Sections III-D, V-B, V-E, Tables 3 and 6, Supplements S4 and S15; (3) the literature, now Section II, Section VI, the references and Supplement S13; (4) lag, update rate, latency and tuning, now Section V-D, Table 5, Fig. 4, Supplement S6. Added weight, as the launch message asks: what the failed coast-count control leaves; the closed loop after the failed equal-time-lost comparison; the two-noise IMM as a "lower bound"; placement against misdetection-aware planning and intermittent-observation filtering.
- **Card-confirmation pause not held.** This is a non-interactive sub-agent, and the brief says so.
- **Criteria binding:** none supplied (`criteria_binding_unavailable`). Format is judged only against the brief's stated rules and the template's `.tex`.
- **Skill:** `academic-research-skills:academic-paper-reviewer`, mode `full`, standards used for this seat only.
- **Clock (from `date` and Get-Date):** started 2026-11-22 12:09:39 EST; hashes checked again at 12:20:07 EST; written 12:21 EST.

**Files and SHA-256, at start (12:09) and at end (12:20). All match the brief, and nothing changed.**

| File (`revision_v13\work\A_text\out\freeze_v13_1201\`) | Start | End |
|---|---|---|
| `MANUSCRIPT_v13.md` | b469bf657af9ddee583b7bda944ca3af639e1ba4b2e61875150d83bafd0f7793 | same |
| `MANUSCRIPT_v13.tex` | dd915933edffcebad863c9d1ed02b37ef0a6a493045696b210ff9c94b4dc2eee | same |
| `SUPPLEMENT_v13.md` | d1ea32fa94787a0eb44c441714ac8c9183d3ab9707c25336194673170515f9b8 | same |
| `MANUSCRIPT_v13.pdf` (not opened; hashed only) | d3fec633f7b5ab7d4d9053c2b9a56e23dbd6d5ef9c90455cd477701c0920bcf5 | same |

- **Pages viewed:** `page01.png` to `page12.png` (all 12), plus `figures\fig2_frontiers_v13.png` at full size to check the legend.
- **Other reads:** `BUILD_REPORT_v13.md` (word counts); the template `tj-template-s1.tex` (front matter, headings, acknowledgment and reference examples); the main-text `.tex` (headings, captions, front matter, bibliography). In the supplement I read only the sections a main-text pointer sends the reader to: S1 (S1.1, S1.2, S1.4), S2, S4, S9, S10, S11, the opening of S12, S13, S14, and S15.
- **Not read:** the response letter, `TEXT_FREEZE_v13.md`, `RECOUNT_COVERAGE_v13.md`, `DERIVED_v13.json`, `OUTCOMES_v13.json`, earlier reports, other seats' files, and notes. I had no web access, so no reference was checked online. The suggested references at the end are given from memory and marked unverified.

## Summary from the domain seat

This is a careful, candid study. The confirmatory result is right and is explained correctly: a fixed-noise extended Kalman filter followed on a straight road at a regular update rate sits at its Riccati steady state, and an equal-caution sweep removes a constant scale, so nothing is left to rank. The margin-ratio check (Table 3, Supplement S11) is a good diagnostic that needs no ground truth. The amplitude-matched oracle gives each tracker a fair reference at its own spread. The limits are mostly stated.

From an estimation point of view, four things keep the paper from saying exactly what it shows.

1. **The room is mostly mean-model error.** Most of the room is the constant-velocity mean's lag at braking onset. That is a bias, which a covariance (a second moment) cannot track. The null is therefore scoped to a constant-velocity mean, and this is not said (R2-01).
2. **"Lower bound" is unsupported.** The paper calls the two-noise IMM's share a "lower bound". Nothing in the paper fixes the sign of the interface's effect (R2-02).
3. **The literature that predicts the amendment results is not placed.** Intermittent-observation Kalman theory predicts the coast-count result, and trackers whose covariance depends on the data are the natural candidates for an informative covariance. Neither literature is cited (R2-03).
4. **The adaptive filter is missing from the summaries.** The adaptive-process-noise filter gives the largest covariance gain in the paper, replicated against its own permuted twin, yet it does not appear in the abstract, the conclusion, or the Discussion (R2-04).

All four can be fixed in the text. The failed coast-count control and the failed equal-time-lost comparison are reported honestly; only smaller wording residues remain (R2-05, R2-06).

## Findings

| ID | Location | Finding | Severity | Evidence quoted from the text | Fix (fewest words) |
|---|---|---|---|---|---|
| R2-01 | Sections III-E, V-B (Table 3), VI, VII; Scope in Section I | **The null is a property of a covariance used with a constant-velocity mean, and the text does not say so.** The room is concentrated in the braking phase (room by phase 1.63 / 23.62 / 0.08 pp for the tracker of record), and the braking prediction, a mean-path fix, recovers 0.783 of it. The error a margin must cover is therefore mainly a bias: the constant-velocity prediction's lag once the lead brakes. A covariance is a second moment. A fixed-noise filter's covariance cannot grow when that bias appears, and the re-tuned variants are strongly overconfident in the braking phase (Supplement S4, Table S7, on the 35 old evaluation runs, which are exploratory: braking-phase NIS 7.9 to 9.6 against an expected 2). So the confirmatory equivalence mainly shows that a covariance cannot stand in for a maneuver-aware mean. Whether a covariance adds anything once the mean is fixed (N with CK3's predicted path, on the roughly 22% of the room CK3 leaves) is untested, while VII states the null generally. | MAJOR | "with actors predicted at constant velocity" (III-E); "The braking prediction acts through another channel, the predicted path, and recovers far more." (VI); "In these tests a tracker's covariance rarely improved a planner's decisions over a class-average margin, and then by little." (VII) | Add to VI: room mostly constant-velocity bias at braking onset (cite braking-phase NIS); scope abstract and VII "with a constant-velocity prediction"; list N-with-CK3 as untested (or run it). |
| R2-02 | Section V-E (two-noise IMM paragraph); Section VI, Limits | **"Lower bound" is not supported.** The share is the value for the position–velocity interface, not a bound for other interfaces. The direction is unknown either way. Passing the acceleration block with a constant-velocity mean would add margin that rises with the maneuver-mode probability, including the mode's 13% of before-braking decisions above 0.5 (Supplement S15, Table S42). A constant-acceleration or mixture mean would shrink the room the covariance competes for, as CK3 shows. No argument or test in the paper fixes the sign. This turns the previous panel's limit (d) into a favorable directional claim. | MAJOR | "Through the position–velocity interface (Section III-D) this share is a lower bound." (V-E); "so the two-noise IMM's share is a lower bound for that interface, not a verdict on maneuver-adaptive covariances." (VI) | "This share is measured through the position–velocity interface; a full-state interface was not tested and could give more or less." |
| R2-03 | Section II; Section VI; references; novelty paragraph | **The literature that predicts or bounds the amendment results is not placed.** (i) *Intermittent-observation Kalman filtering* (e.g., Sinopoli et al., 2004): with fixed noise, the error covariance is a function of the measurement-arrival sequence only. This predicts the coast-count result (the covariance carries nothing beyond the miss count) and the detection-rate threshold the paper quotes from [19]. Section II's steady-state sentence omits its condition, a regular update schedule. (ii) *Trackers whose covariance depends on the data*: probabilistic data association filters (PDA, IPDA, JIPDA), whose covariance carries an association-uncertainty term, and per-detection (heteroscedastic) measurement noise from probabilistic detectors. These are the obvious candidates for "a covariance that varies with information", which the next steps point toward. (iii) *ITS threat assessment and automatic emergency braking under sensor uncertainty* (Stellet et al.; Berthelot et al.; Stöckle et al.; Nilsson et al.) and *IMM evaluations for ACC and forward collision warning* (e.g., Pak 2022; Moon and Yi 2005). Supplement S13 lists these as queries, but the paper neither cites nor places them, and its novelty paragraph should say how the equal-caution test differs from them. The heading "What a varying covariance needs" makes claims about exactly this literature. | MAJOR | "With fixed noise, a Kalman filter's covariance settles to a steady state [26]" (II); "Lidar trackers use fixed-noise Kalman filters [28] or covariances set from training data [29]." (II); "Collision-avoidance decisions have long been computed from uncertain state estimates [30], with criticality metrics for their outcomes [31]." (II) | Add "under regular updates"; add three or four sentences placing (i) to (iii); add four to six references. |
| R2-04 | Abstract; Section VII; Section VI ("What a varying covariance needs") | **The adaptive filter is left out of the summaries.** The adaptive-process-noise filter is the textbook engineering response to maneuvers. It gives the paper's largest covariance share (0.0459 [0.0390, 0.0533]) and the only replicated test against its own permuted twin (difference 0.0498 on the fresh runs and 0.0508 on the new runs; H 0.0003). It is absent from the abstract, from VII, and from VI's list of varying-covariance cases, which ends "These are level-type effects." Its share interval also crosses δ, which the "inside the ±5% margin" sentences do not cover. VI could add that its gain is plausibly timed by phase (the per-phase schedule recovers 0.916). | MAJOR | "under dropouts it recovers 2.8% of the room (replication: 3.0%), but a fixed coast-count margin recovers slightly more, and a two-noise interacting-multiple-model tracker's recovers 2.2%; these point values lie inside the ±5% margin." (Abstract); "These are level-type effects." (VI) | Add "a noise-adaptive filter's 4.6%, replicated against its permuted twin" to the abstract (shorten "(replication: 3.0%)" to "(replicated)"), to VII and to VI. |
| R2-05 | Section V-E, dropouts paragraph | **What the failed coast-count control leaves, worded slightly off in three places.** (a) "Needs no covariance" is not quite what was shown. The coast-count factors (0.216, 0.107, 0.065; 0.925 after re-acquisition) were fitted as the covariance margin's own median growth per missed update (Supplement S15). The control shows that the covariance adds nothing beyond its deterministic growth with the miss count, which Kalman theory predicts. (b) The replication and the dose trend do not separate the covariance from a coast count: a coast-count margin would also gain more as dropouts become more frequent. (c) The 10 Hz value placed right after "not shown at 2 Hz" invites reading it as ranking shown at 10 Hz. At 10 Hz a 0.5 to 1.5 s mask spans 5 to 15 missed updates, so the ordering within a dropout is still the miss count, no coast-count control was run there, and its class average is the 2 Hz one (Supplement S15). | MINOR | "The dropout gain is thus matched by a coasting margin, a level effect that needs no covariance; ranking among dropout decisions is not shown at 2 Hz. A second configuration, 10 Hz with 0.1 s latency (secondary), gave the same class; there the share among dropout decisions alone is 0.035 [0.014, 0.054] (descriptive)." | "needs no per-decision covariance: one factor per missed-update count, fitted from the covariance's growth, does as well"; add "(not compared with a coast-count margin)" after 0.035; one clause on (b). |
| R2-06 | Section V-E, closed loop with dropouts; Table 6 | The closed loop is stated as what it is in the abstract, Section I, V-E and VII. That is good. Residues: (a) The Table 6 row "(A), H 0.0003" can be quoted without the next row; put "not at equal time lost" into its label cell. (b) The nearest direct comparison is not cited in the main text. The class average at scale 8 sits at nearly the same time lost (25.45 s against 25.42 s) with 24.4% contacts against 20.7%, a paired difference of −0.04 [−0.11, 0.03] (Supplement S15, Table S44). (c) The covariance arm spent less time in full braking (58.9% against 65.4%, Table S43) while losing more time. That is consistent with earlier, gentler braking from a wider margin during dropouts, the same level effect. | MINOR | "On 135 new cases the covariance arm made contact in 21% against 33% for the dropout-estimated class average (passed; amendment). But in closed loop that arm was the more cautious one" | Add "not at equal time lost" to the row label; cite the scale-8 pair; one clause on full-braking share. |
| R2-07 | Section II; Section VI on [19] | **Fairness to [19], which is in the target journal.** [19] reports over 66% lower collision risk from misdetection-aware chance constraints. Here the open-loop gain is about 3% of the room, and the closed-loop drop from 33% to 21% contacts cannot be told from a wider margin. The paper aligns the two mechanisms well in VI but does not reconcile the magnitudes. It should say whether [19]'s comparison held caution equal; the paper describes it only as being "against a noise-only controller". | MINOR | "a model predictive controller whose chance constraints account for misdetections as well as measurement noise cut collision risk by over 66% against a noise-only controller [19]" | One sentence in VI: the equal-caution lens and the failed equal-time-lost comparison bear on gains like [19]'s if caution was not held equal. |
| R2-08 | Section V-E, nuScenes mechanism check; Abstract | (a) The pairs "around real missed detections" mostly compare missed with steady tracks, and the spread there grows deterministically with misses: the coast-count effect again. A missed-update count would likely rank the same pairs; say so, or compute its τ. (b) The IMM's τ is positive over all pairs (0.093 [0.066, 0.116]) and on steady tracks (0.064). This is in Supplement S15, Table S45, not the main text, and it shows that "slightly inversely over all tracks" is a property of the fixed-noise tracker. (c) Explain the negative τ on steady tracks: state whether pairs mix classes (class-level noise against speed-driven constant-velocity error), and stratify. | MINOR | "Around real missed detections Kendall's τ is positive but weak (passed; amendment); over all pairs it is slightly negative: on steady tracks the spread ranks the error the wrong way" | Add the IMM's all-pairs τ; one clause on (a); state the class mix. |
| R2-09 | Section IV-E | **The Holm sentence has a misleading antecedent.** "They" reads as the six Holm-adjusted hypotheses, but the list that follows is the original lead-braking sequence, which also has six. This misstates Holm's scope (earlier limit (e)). | MINOR | "within the second amendment, six primary hypotheses are Holm-adjusted (Table 6). In lead braking they are room; detection in a ±5% band;" | "In lead braking the sequence is: …", with the Holm sentence after the family lists. |
| R2-10 | Table 6; Section V-E | The third amendment's Holm values (0.18 and 0.99, Supplement S15, Table S38) are not beside their labels. The main text says only "fail regardless". | MINOR | "and the third's two fail regardless (Supplement S15)." Table 6: "new runs, share minus a fixed coast-count margin's \| −0.0024 [−0.0057, −0.0001] \| failed" | Add "H 0.99" and "H 0.18" to the two failed rows and note "Holm within the third amendment's two tests". |
| R2-11 | Table 4; Section V-C | The label "safer, no extra cost" sits beside a positive time-lost difference with an interval above zero. Read by an outsider, the label contradicts its own numbers; the supplement already words it better. The status of N's closed-loop equivalence (confirmed, or a plan test outside the sequences) is also not labeled. | MINOR | "\| CK3, braking prediction \| matched \| 0% \| −0.20 [−0.32, −0.10] \| 0.16 [0.10, 0.22] \| n.c. \| safer, no extra cost \|"; "the tracker covariance is equivalent to the class average within ±0.10 of contact share" | "safer, time cost within tolerance"; state N's label. |
| R2-12 | Fig. 2 caption (page 6) | The caption contradicts the legend. In the figure the IMM is solid pink and its class average, "F0 (IMM)", is dashed. F0 is hidden under N. | MINOR | "The IMM (dashed) is drawn with its own class average, against which its share is measured." | "The IMM (solid) against its own class average (dashed); F0 lies under N." |
| R2-13 | Table 3; Section V-E; Section III-A | Run-set names drift: "fresh", "new", "older fresh", "older runs", "old evaluation", "tuning". Table 3's title says "fresh lead-braking runs", but its two-noise row says "older runs", which is easily read as the 35 old evaluation runs. | MINOR | "IMM, two-noise (older runs, secondary)" (Table 3); "matched in open-loop caution on the older fresh runs (18.2% against 18.4%)" (V-E) | Name the 105 and 150 lead-braking sets once (for example "fresh set A" and "fresh set B") and use only those names. |
| R2-14 | Section III-E | The margin projection propagates the current state covariance only. Process noise accumulated over the look-ahead (the integral of Q over t_e) is not included, or at least not stated. With fixed noise it would add a term that is the same for every decision and would dilute the variation further. Say which. | MINOR | "for a position–velocity covariance $P$, $s = z^{\top} P z$ with $z = (n, t_e n)$ and $t_e$ the look-ahead" | One clause: "without process noise over the look-ahead (a decision-constant term with fixed noise)". |
| R2-15 | Section V-C | **The closed-loop regime.** F0 and N brake fully in about 53% (lower level) to 80% (higher level) of decisions, against 2% to 9% for CK3, TG and PS (Supplement S9, Table S23). In this regime the margin mainly sets when the fallback fires, which limits what "equivalent in closed loop" says about an ACC-like planner. The main text gives F0's share but not the contrast. | MINOR | "the class average brakes fully in 52.7% of its decisions at the lower level and 78.6% at the higher" | Add "(braking prediction, time gap, schedule: 2–9%)". |
| R2-16 | Section I, contribution 2 | The cross-reference misses V-E, where the no-room result for nuScenes under dropouts is reported. | MINOR | "The nuScenes logs and cut-in events showed no room, so no real-log decision test was possible (Sections V-A to V-C)." | "(Sections V-A and V-E)". |
| R2-17 | ACKNOWLEDGMENT, AI paragraph (a) | The recount scope is overstated against Section IV-E, which excludes the supplement's ‡ values. The paragraph's first sentence also has no verb. | MINOR | "Claude Sonnet 5.5 and Claude Fable 5.2 wrote the second programs that recount every printed value" against IV-E: "recount every value printed in the main text and all but the marked (‡) values of the supplement" | "… that recount every value printed in the main text"; use version (b) (see answer 8). |
| R2-18 | Q6; Section V-E (coast-count control) | **Self-containment.** How the coast-count margin was built is only in Supplement S15: one factor per missed-update count, fitted as the covariance's median ratio on the 105 earlier runs, which share no run with the test. The main text's reading ("needs no covariance") depends on that fact. | MINOR | "a class-average margin that knows only the dropout state and the number of consecutive missed updates recovered slightly more of the room" | Add "its factors fitted from the covariance's median growth per missed update on the 105 earlier runs". |
| R2-19 | Q6; Section V-E (equal-time-lost comparison) | **Self-containment.** How the failed test reads the frontier (linear interpolation between scales 4 and 8, giving 25.7% against 20.7%, with bracketing required) is only in Supplement S15. The main text gives the difference but not the statistic. | MINOR | "At equal closed-loop time lost, read from the class average's frontier at scales 4, 8, and 16 on the same cases, its contacts were not shown to be fewer (difference −0.05 [−0.12, 0.02]" | Add "(linear interpolation between scales 4 and 8: 25.7% against 20.7%)". |
| R2-20 | Q6; Section V-C (behind non-braking leads) | **Self-containment.** The plan's classes are stated, but the contact differences they rest on are only in Supplement S9, Table S25. The only non-null one is −0.25 [−0.47, −0.04] behind leads that stop and pull away, for both CK3 and PS. | MINOR | "By the plan's classes the braking prediction is inconclusive behind leads that keep their speed or brake mildly and is safer at a cost in time lost behind leads that stop and pull away; the per-phase schedule has the same classes (Supplement S9)." | Add "(contacts −0.25 [−0.47, −0.04]; no difference behind the others)". |
| R2-21 | Q7; first page (page 1; `.tex` line 50) | The affiliation is not in the template's form, which is "City, ST ZIP USA" with no comma before USA. This concerns form only, not the content of the author block. | MINOR | "Independent Researcher, Troy, MI, USA (ORCID: 0009-0002-5241-9922)"; template: "Boulder, CO 80305 USA" | "Troy, MI [ZIP] USA". |
| R2-22 | Q7; references (pages 11–12) | IEEE style misses: [26] has no place of publication; [39] has no year; [40] and [41] write dates day first ("9 Mar. 2021", "4 Jan. 2023"), while [4] writes "Nov. 22, 2026". Low priority, outside the brief's list: months are missing in [2], [19], [24] and [31]. | MINOR | "Wiley, 2001, doi: 10.1002/0471221279." [26]; "E/ECE/TRANS/505/Rev.3/Add.151." [39]; "9 Mar. 2021" [40]; "in force from 4 Jan. 2023" [41] | Add "New York, NY, USA:" (or the city on the title page) to [26] and the year to [39]; use "Mar. 9, 2021" and "Jan. 4, 2023". |
| R2-23 | Q7; Section IV-E | An abbreviation is not defined at first use in the body. | MINOR | "SHA-256 hashes with local file times" | "Secure Hash Algorithm (SHA-256) hashes". |
| R2-24 | Q7; Section V-E, dropouts paragraph (page 7) | The serial comma is probably missing, if this is a list of three items (low confidence; it may be a pair). | MINOR | "(lead braking, this mask law and output rule only)" | "(lead braking, this mask law, and this output rule only)". |

**Checked and sound in my area.**

- The Riccati explanation of the null (Section VI) is correct.
- The two limits of the first IMM are disclosed: its constant-acceleration filter missed the NIS window, and the planner uses only the position–velocity block with a constant-velocity prediction.
- All variants were tuned on tuning runs only and frozen before scoring. The offline replay reproduced the logged tracks bit for bit in 151 of 155 runs (Supplement S4).
- The re-tuned IMM and the two-noise IMM are reported beside the registered classification without replacing it.
- The pedestrian-crossing decomposition rightly attributes most variation to the update schedule and the geometry. In CANMOT the object-frame noise is rotated by a noisy pedestrian heading (Supplement S11); naming that would make "geometry" concrete.
- The update-rate and latency analysis (Section V-D, Fig. 4(a)) correctly treats the after-stop room as a 2 Hz artifact.
- The real-log decision test is reported as uninformative, not as support.

## Answers to the eight questions

### 1. Labels and sizes

Mostly right.

- "Confirmed" is used only for the original sequences (Table 2; Sections V-A and V-B).
- Amendment results carry "(A)", "replicated" or "failed" (Table 6). "Failed" stands without "(amendment)", but Table 6 holds only amendment tests, so it reads correctly.
- Holm for the six second-amendment primaries sits beside the labels (the H column), and the text says it changes none.
- Misses:
  - The third amendment's two Holm values are not beside their labels in the main text (R2-10).
  - IV-E's "In lead braking they are …" lets a reader take the original lead-braking sequence for the Holm family (R2-09).
  - "Safer, no extra cost" contradicts a positive time-lost interval (R2-11).
  - The closed-loop equivalence of N has no status label (R2-11).
- Sizes are reported with intervals. One exception: the "inside the ±5% margin" sentences cover 2.8%, 3.0% and 2.2% but not the adaptive filter's 4.6%, whose interval crosses δ (R2-04).

### 2. Overreach

- **Dropout gain's source.** Mostly correct now. The text says the gain "is thus matched by a coasting margin". Residues: "needs no covariance" against factors fitted from the covariance; the replication and dose trend do not separate the two; and the 10 Hz within-dropout value invites a ranking reading that no coast-count control was run to support (R2-05).
- **Closed loop.** Stated as what it is everywhere: fewer contacts matched in open-loop caution, not shown at equal time lost, "cannot be told from a wider margin". Only label-cell and mechanism residues remain (R2-06).
- **nuScenes mechanism check.** The training-split choice and the all-pairs inverse are disclosed. The positive τ around misses is again the miss-count effect, and the IMM's positive all-pairs τ is omitted (R2-08).
- **Real-log decision test.** No overreach: "they neither support nor contradict".
- **Two-noise IMM.** "Lower bound" is an overreach (R2-02).
- **New, in my area.** The general wording of Section VII and the abstract's first sentence are broader than the test, which used a constant-velocity mean (R2-01).

### 3. Earlier limits

| Limit | Status | What remains |
|---|---|---|
| (a) Closed loop matched only in open-loop caution | **Addressed as far as data allow.** The equal-time-lost comparison was run, failed, and is reported in the abstract, Section I, V-E and VII. | The benefit is not shown. It covers one level and lead braking only, in a regime with 53–80% full braking (R2-15). The scale-8 near-equal-time pair should be cited (R2-06). |
| (b) Dropout gain may be only a coasting margin | **Addressed: it is.** The coast-count margin recovered slightly more. | Wording residues (R2-05). The link to intermittent-observation theory, which predicts this result, is missing (R2-03). |
| (c) Abstract and conclusion stronger than the body | **Largely addressed.** "Rarely beat … and then by little" matches the body. | The opposite bias now: the adaptive filter, the strongest positive result, is missing from the abstract and conclusion (R2-04). The general claim is not scoped to a constant-velocity mean (R2-01). |
| (d) Two-noise IMM interface | **Partly.** It was tested, and the interface is disclosed. | "Lower bound" is unsupported (R2-02). |
| (e) Scope of Holm and of the second-program recount | **Partly.** The second-amendment Holm is clear in Table 6 and V-E; the recount scope is clear in IV-E. | IV-E antecedent (R2-09); third-amendment Holm values not in the main text (R2-10); the AI paragraph overstates the recount scope (R2-17). |
| (f) Density; round-2 results only in the supplement | **Addressed on placement.** Table 6 and Sections V-D and V-E are in the main text. | Still dense: drifting run-set names (R2-13), many coined labels, three Q6 gaps (R2-18 to R2-20). |
| Structural: near-constant covariance makes the confirmation hard to fail | Acknowledged ("expected from its near-constancy"). | Unchanged. R2-01 sharpens it: the room is mostly mean bias. |
| Structural: small positive effects | Acknowledged. | Unchanged. |
| Structural: one simulator and configuration | Acknowledged (Limits; VII). | Unchanged. |
| Structural: no decision-level real-log evidence | Acknowledged. | Unchanged. |
| Structural: process (amendments after results, local hash locks, AI authorship) | Disclosed (IV-E; Table S5; Acknowledgment). | Unchanged by wording. |

### 4. Readability

- **Bottom line first:** yes. The abstract's first sentence carries the result and the caveat.
- **Coined terms:** defined once, in Table 1 and Section IV. There are many of them (room, share, wrong go, caution, decision-equivalent, amplitude-limited, uninformative variation), and the run-set names drift (R2-13).
- **Finding the evidence:** a reader can find nearly every claim's evidence in Tables 2–6 and Figs. 2–4. The exceptions are the coast-count construction, the equal-time-lost reading, and the non-braking closed-loop contact differences (Q6).
- **Error to fix:** the Fig. 2 caption contradicts the legend (R2-12).
- **Section V-E** carries about ten results in 898 words. One sentence of road map at its start would help, for example: "three amendments: pedestrian crossing; dropouts in open and closed loop, each with a control; the two-noise IMM; the adaptive filter; the real-log mechanism and decision tests".

### 5. Verdict

- **Recommendation:** major revision.
- **Score:** 6.5/10, which is 3.25 stars and rounds to 3.5 of 5 (★★★½).
- **Most likely outcome at IEEE OJ-ITS:** major revision. The rejection risk comes mainly from the predicted null, the small effects, and the density, not from errors.
- **The single change that would raise my score most:** fix R2-01. Scope the null to a covariance used with a constant-velocity mean, and add Section VI's bias-versus-variance sentence with the braking-phase NIS. If new runs are possible, scoring N on top of CK3's predicted path would raise the score further: it would turn "a covariance cannot replace a maneuver-aware mean" into a test of whether a covariance adds anything once the mean is right.

### 6. Self-contained main text

The sentence after Scope ("The main text holds every result on which the claims rest") is nearly true. There are three cases (R2-18, R2-19, R2-20):

| Main-text location | Supplement item it rests on | Fact to bring in |
|---|---|---|
| Section V-E, coast-count control ("a level effect that needs no covariance") | Supplement S15, "A fixed coast-count margin" paragraph | Its factors are the covariance margin's median growth per missed update, fitted on the 105 earlier runs (no shared run). |
| Section V-E, equal-time-lost comparison | Supplement S15, "The class average at larger scales" paragraph | Linear interpolation between scales 4 and 8, giving 25.7% against the covariance arm's 20.7%, with bracketing required. |
| Section V-C, closed-loop classes behind non-braking leads | Supplement S9, Table S25 | CK3 and PS: contacts −0.25 [−0.47, −0.04] behind leads that stop and pull away; zero difference behind the others. |

Pointers that only add detail (S2, S4, S5, S6, S10, S13, S14) are not cases.

### 7. IEEE OJ-ITS format and declarations

**Passed:**

- Section and subsection headings are in capitals, as in the template; there are no subsubsections.
- "Fig. N" in running text and "FIGURE N." in captions; "Table N" and "TABLE N." in Arabic; supplement items are "Table S…".
- American spelling, with no British forms found by a scan.
- Periods and commas sit inside closing quotation marks; there are no contractions.
- "Preregistered" has one spelling throughout.
- Funding is in the first-page author note (page 1), with no Funding heading.
- One ACKNOWLEDGMENT in the required order: responsibility, data and code, AI, then competing interests with no human or animal subjects.
- The first page has the author, affiliation, ORCID, and corresponding author with email. The running head on even pages reads "Kopalli: Tracker Covariances as Safety Margins in Motion Planning".
- Web source [4] carries "Accessed:"; arXiv entries are in "year, arXiv:ID." form; [10] is "submitted for publication" with no journal named.
- The abstract has 250 words (`wc`), with no abbreviations.
- Five index terms, in alphabetical order.
- References are numbered in the order of first citation.

**Misses (6; the last is low confidence):**

1. Affiliation form (R2-21).
2. [26] has no place of publication (R2-22).
3. [39] has no year (R2-22).
4. [40] and [41] use day-first dates (R2-22).
5. "SHA-256" is not defined at first use (R2-23).
6. Possible serial-comma miss in V-E (R2-24).

**Not counted:** months missing in some journal entries.

**Title:** no sentence contradicts it. Section IV-E qualifies "preregistered" as internal locks; the word is the author's choice.

### 8. AI disclosure

**(a) As frozen.** It meets IEEE's three elements:

- systems: Claude, with each model named, and OpenAI Codex;
- sections: the Abstract, Sections I–VII, the supplement, and the code;
- level of use: literature searches and summaries, code written and run, text drafted and revised, recounts, audits.

Its problems:

- One factual overstatement: "recount every printed value". Section IV-E and Supplement S12 exclude the ‡ supplement values (R2-17).
- A verbless first sentence.
- A long model-by-model narrative, which invites an editor to ask what the author did.

Desk-rejection risk from the disclosure itself is low to moderate once the author's confirmation (a gate) is filled.

**(b) The shorter candidate lowers the risk without understating the use, with three edits.** Its facts check out against the paper:

- "Separate Claude sessions that had not seen the first programs" matches IV-E ("separate sessions … without reading the first programs").
- "recounted every value printed in the main text" matches IV-E and S12 exactly.
- The models and Codex match (a).
- "drafted and revised the text of all sections and of the supplementary material" states the level clearly.

The three edits:

1. Restore "and summaries" after "literature searches". The related-work statements rest on summarized abstracts (S13), which is AI-generated content.
2. Write "wrote and ran the analysis, simulation-control, and figure code". Running the analyses is part of the level of use.
3. Change "made every scientific decision" to "made or approved every scientific decision". The amendments were written after results, and the paper does not show who proposed each; "made every" is the one claim in (b) that could later be contested.

Two further notes:

- "Reviewed and approved all content" is the author's own attestation, a gate. It must be literally true for 20,860 words of supplement and all code, or be narrowed to what the author verified.
- Keep the ACKNOWLEDGMENT order. (b)'s first sentence stays as paragraph 1 and the rest becomes paragraph 3. The AI-panel sentence of (a) is optional, since "drafted and revised" covers its effect, but keeping it costs only a few words and adds transparency.

## Suggested references (from memory; unverified, because there was no web access)

```yaml suggested-references
- key: sinopoli2004intermittent
  why: "Intermittent-observation Kalman filtering; covariance depends only on the arrival sequence; predicts the coast-count result and the detection-rate threshold in [19]"
  authors: "B. Sinopoli, L. Schenato, M. Franceschetti, K. Poolla, M. I. Jordan, S. S. Sastry"
  title: "Kalman filtering with intermittent observations"
  venue: "IEEE Transactions on Automatic Control, vol. 49, no. 9, pp. 1453-1464"
  year: 2004
  doi: "10.1109/TAC.2004.834121"
  verified: false
- key: musicki1994ipda
  why: "Integrated probabilistic data association: a tracker whose covariance depends on the data (association uncertainty) and on detection probability"
  authors: "D. Musicki, R. Evans, S. Stankovic"
  title: "Integrated probabilistic data association"
  venue: "IEEE Transactions on Automatic Control, vol. 39, no. 6, pp. 1237-1241"
  year: 1994
  doi: "10.1109/9.293185"
  verified: false
- key: stellet2015criticality
  why: "Propagation of sensor and state uncertainty into criticality measures for driver assistance (ITS threat-assessment lineage; S13 query 15)"
  authors: "J. E. Stellet, J. Schumacher, W. Branz, J. M. Zoellner"
  title: "Uncertainty propagation in criticality measures for driver assistance"
  venue: "Proc. IEEE Intelligent Vehicles Symposium (IV)"
  year: 2015
  verified: false
- key: stoeckle2018aeb
  why: "Automatic emergency braking design under sensor measurement errors (decision-level effect of estimate uncertainty; S13 query 43)"
  authors: "C. Stöckle, W. Utschick, S. Herrmann, T. Dirndorfer"
  title: "Robust design of an automatic emergency braking system considering sensor measurement errors"
  venue: "Proc. IEEE Int. Conf. Intelligent Transportation Systems (ITSC)"
  year: 2018
  doi: "10.1109/ITSC.2018.8569495"
  verified: false
- key: pak2022himm
  why: "IMM filtering evaluated by its effect on forward collision warning decisions (maneuver-adaptive tracking judged downstream; S13 query 49)"
  authors: "J. M. Pak"
  title: "Hybrid interacting multiple model filtering for improving the reliability of radar-based forward collision warning systems"
  venue: "Sensors, vol. 22, no. 3, art. 875"
  year: 2022
  doi: "10.3390/s22030875"
  verified: false
- key: meyer2019lasernet
  why: "Lidar detector with per-detection (heteroscedastic) uncertainty, a route to a measurement-noise term that varies with information"
  authors: "G. P. Meyer, A. Laddha, E. Kee, C. Vallespi-Gonzalez, C. K. Wellington"
  title: "LaserNet: An efficient probabilistic 3D object detector for autonomous driving"
  venue: "Proc. IEEE/CVF Conf. Computer Vision and Pattern Recognition (CVPR)"
  year: 2019
  verified: false
```
