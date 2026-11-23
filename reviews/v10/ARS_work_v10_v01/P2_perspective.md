contract_role: perspective
## Dimension Scores

### D1: methodology_rigor
score: not_assessed

### D2: domain_accuracy
score: not_assessed

### D3: argumentative_coherence
score: not_assessed

### D4: cross_disciplinary_relevance
score: warn
trigger: "The adjacent-field framing is incomplete but not misleading"

### D5: writing_and_structure
score: not_assessed

### D6: venue_fit_and_contribution
score: not_assessed

## Review Body

I read this manuscript as an automotive safety-assurance engineer who builds scenario-based safety arguments (SOTIF-style argumentation, UN R157 performance models, RSS). Statistics and tracker theory are outside my competence, and I leave them to the other seats. My question throughout was whether a team that builds or validates an automated-driving stack, or an assessor, could act on these conclusions without misapplying them.

The main claim is scoped with unusual care, and the paper never presents simulation results as deployment-ready safety evidence, so nothing here reaches my block trigger. The adjacent-field framing is still incomplete. The paper does not say what its null does not license for a deployed stack (W1). It anchors its 0.75 s conclusion on a regulatory performance model whose standstill parameter it drops (W2). The costs and the parties who bear them are named only in part (W4, W6). The headline results are hard for readers outside tracking to use (W7). I therefore score D4 warn. W1 and W2 are Major; the rest are Minor. Each fix is given in its finding.

### Focus-item checks (Configuration Card #4)

1. R157 and RSS values. The derivations and clause-level citations agree with my reading of the regulation (S2). Performance model 2 is adopted only in part (W2). The recorded lead braking is milder than the regulation's test values (W3). The operating domain behind the borrowed values is not stated (W9). The "RSS-style" label is loose (W5).
2. Practical take-aways. "State the commitment assumption" is actionable (S4). The ratio check is portable (S5) but lacks a decision rule and guidance for other planner types (W8).
3. Costs beside wrong-go. Caution is reported, and the case where braking never comes is admitted to be untested. Comfort is not measured (W6). The closed-loop fallback share appears only deep in S3.4 (W4).
4. Stakeholders. The conclusions are framed for tracker developers, planner designers and open-loop evaluators; regulators appear only as a source of parameters. Occupants' lost progress is measured but their comfort is not. Following traffic is never mentioned. Vulnerable road users, cut-in and newly detected actors, and lead braking above 5.5 m/s² lie outside the scope but are mostly not named (W1, W3, W6).
5. The closed-loop check. §VI states its role and two of its limits correctly. The fallback share is missing wherever readers meet its sizing figures (W4).

### W1: The covariance null is not fenced against removing covariance margins from a deployed stack
**Problem**: The headline practical reading is scoped to lead braking and this tracker (§I Scope, §VI). The paper never says what that scope excludes for the step a practitioner is most likely to take from it: dropping or freezing the covariance margin. Two features of the evidence leave that step unsupported. First, the evaluated decisions barely contain the regimes a covariance margin exists for. Every lead-braking decision has a mature track (S9). The lead's track is initialised 45 times in 35 runs (§V-A). The 0.74% of binding rows whose tracker margin departs from 1.10 times the class average (Fig. 2(b), including a cluster near 1.7) are not characterised. Newly detected, cut-in, re-acquired or occluded actors are where a covariance should widen, and they are essentially absent. Second, a deployed stack tunes one margin scale across its whole operating domain. The paper itself finds that one scale spends caution differently across phases (§IV-B, §VI). The same mechanism across scenario families could give value to a covariance whose level differs by family, and a single-family, per-population test at equal caution cannot see that.
**Why it matters**: A planner team reading §VII could replace the covariance term with a class constant and lose protection exactly where this study has no data. The paper does not claim this implication, which is why I do not score block, but nothing in the text stops a reader from drawing it.
**Suggested fix**:
1. Add to §I Scope and §VI a sentence such as: "These results do not support removing or freezing the covariance margin of a deployed stack; the evaluated decisions contain almost no track births, re-acquisitions or newly detected actors."
2. From the stored data, count the evaluated decisions within about two tracker updates (1 s) of one of the 45 initialisations, and report D(N, F0) on them or state that they are too few to evaluate. Characterise the 1,127 rows outside the 5% band in Fig. 2(b) by track age.
3. Apply the paper's own ground-truth-free ratio check (Fig. 2(b)) to the tuning runs of the other five scenario families, and report the median N/F0 ratio for each family. If the level differs between families, state that a single tuned scale could reallocate caution across them and that this is untested.
4. Name newly detected and cut-in actors as untested in §VI Limits. If a deployment reading is intended, place the scenario family within a scenario-coverage argument (Riedmaier et al., below).

**Severity**: Major
**Evidence Anchor**: text: Supplement S9 "Every lead-braking decision has a track in the oldest age band, so the planned split by track age is empty."; §VI "a class average does as well as the tracker's covariance"
**Confidence**: 4 — core expertise: safety-case scoping and misuse analysis; the cross-family mechanism is my inference, not a result of the paper

### W2: UN R157 performance model 2 is adopted only for its ego parameters, yet the 0.75 s conclusion is said to rest on it
**Problem**: §IV-C takes τ = 0.75 s, A = 6 m/s² and the 12.65 m/s³ jerk from performance model 2 of the 01 series [39]. §V-C then says the 0.75 s conclusion rests on the performance-model values, and §VI Limits says it uses them. By the manuscript's own account (S3.1), the same model also fixes a 2 m safety distance at complete stop and a 7 m/s² deceleration for the other vehicle. The closed-loop rule uses both values, but the primary open-loop scoring sets the standstill gap to zero. At the model's 2 m gap, the 3 s oracle's advantage at τ = 0.75 s is −0.10 [−1.89, 1.29] points and no share is evaluable (Table S6). No perfect oracle O is reported for that setting; Tables S9–S13 cover only the zero gap. Under the model's full parameter set, the paper therefore has no measure of the room at all.
**Why it matters**: An assessor who reads that the conclusion "rests on the performance-model values" will take the 0.75 s headline, the Abstract's last sentence, as holding under R157 model 2. It holds only under a modified version of the model, and the unmodified case cannot be evaluated. The paper also parameterises the same model in two different ways without explaining why.
**Suggested fix**:
1. In §IV-C, state that model 2 also specifies the 2 m stop distance and the other vehicle's 7 m/s², that the primary scoring uses a 0 m gap, and why: a wrong go is defined as contact.
2. Score the perfect oracle O under the 2 m-gap reaction-and-stop scoring (the safe-row flags behind Table S6 already exist) and report den₀. If den₀ falls below the 10-decision-equivalent rule, say that no share can be evaluated under the full model-2 parameter set.
3. In §V-C, replace "rests on the performance-model values of the 01 series" with "uses two ego parameters of performance model 2 (0.75 s, 6 m/s²) with a zero standstill gap". In §VI Limits, add "with a zero standstill gap" after "(0.75 s, 6 m/s²)".

**Severity**: Major
**Evidence Anchor**: text: §V-C "The as-scored conclusion at τ = 0.75 s therefore rests on the performance-model values of the 01 series"; Table S6 caption "No ratio is printed at a 2 m gap, where the 3 s oracle is not an oracle"
**Confidence**: 3 — adjacent expertise: R157 performance models; I could not open the 01-series Annex 3 and rely on the manuscript's own statement of the model's parameters in S3.1

### W3: The recorded lead braking is milder than the assumed stop and the regulation's test, and the 12% headline does not say so
**Problem**: Recorded leads brake at 2.0–5.5 m/s² and none brakes harder (S2). The reaction-and-stop scoring assumes the ego stops at 6 m/s². The paper reports that R157's following test uses at least 6 m/s² for the lead (S3.2), and model 2 assumes 7 m/s² for the other vehicle. The commitment sensitivity is therefore measured only where the ego's assumed stop is at least as hard as anything the lead does. The paper's own sweep over stop decelerations (0.253 at 4 m/s² down to 0.064 at 7.6 m/s², §V-C) shows that the room is sensitive to this relation. The main text gives the lead's deceleration only as bins of the stopping-point error (§III-A), never as a condition on the scope.
**Why it matters**: Benchmark designers and assessors may read the Abstract's "with a perfect 6 m/s² stop 0.75 s after committing, it falls to 12%" as a general property of open-loop decision scores. The case in which a lead brakes harder than the ego's assumed stop, which both the regulation's test and model 2 include, is absent from the recordings.
**Suggested fix**:
1. State the 2.0–5.5 m/s² range in §III-A and §I Scope.
2. Qualify the 12% and the 53% in §V-C, §VI and, if space allows, the Abstract with "for leads braking at up to 5.5 m/s²".
3. Add to §VI Limits that the closed-loop check (leads at 6–7 m/s²) and the open-loop runs cover different braking severities.
4. Name harder lead braking as future work; it needs new recordings.

**Severity**: Minor
**Evidence Anchor**: text: Supplement S2 "No recording brakes above 5.5 m/s²."; Supplement S3.2 "the regulation's following test uses at least 6 m/s²"
**Confidence**: 3 — adjacent expertise: scenario-based validation; the link between lead and ego decelerations is my reading, not something the paper shows

### W4: The closed-loop check's fallback share is missing where readers meet its sizing figures
**Problem**: The opening paragraph of S3 summarises the check as information-free planners needing about 0.31–0.35 s of starting gap beyond the legal following distance. Only the third paragraph of S3.4 reports two further facts. At the selected commitment times the planner was in its full-braking fallback in 0.70–0.72 of decisions, against 0.06 for Td. One scan step below those times there were 13 low-speed contacts. The Fig. S3 caption gives the contact counts but not the fallback share. §VI, where most readers meet the check, states its role and two of its limits correctly but gives neither fact.
**Why it matters**: Read alone, the opening paragraph looks like sizing guidance for a planner without covariance margins. A planner that sits in emergency fallback for most of a hard-braking episode is not a deployable design. A reader could therefore take away a much cheaper result than the check supports.
**Suggested fix**:
1. Add the fallback share and the contact count to the opening paragraph of S3, and the fallback share to the Fig. S3 caption.
2. Add one clause to the §VI sentence, for example "and its planners reach these gaps while in full-braking fallback in about 70% of decisions".
3. State explicitly that the gap figures are not design guidance.
4. S3 itself says the check does not test the paper's question; if it is not needed, consider removing it.

**Severity**: Minor
**Evidence Anchor**: text: Supplement S3 "at about 0.31–0.35 s of extra starting gap over the legal following distance"; S3.4 "The cost in starting gap therefore leaves out a large cost in comfort and progress."
**Confidence**: 4 — core expertise: interpreting closed-loop safety evidence

### W5: "RSS-style" overstates how closely the braking prior resembles RSS
**Problem**: §II and §VI call CK3 an RSS-style assumption. RSS [37] applies a worst-case bound on the front vehicle's braking to every lead. It combines that bound with a response time and a minimum ego braking to derive a safe distance, which comes with a formal guarantee under those bounds. CK3 is different in kind. It is a mild expectation: 3 m/s², while recorded leads brake at up to 5.5 m/s². It applies only to actors moving faster than 0.5 m/s with a nonzero acceleration estimate, and it shifts a constant-velocity prediction. It carries no RSS guarantee. In this paper the RSS-form construction is the closed-loop rule WC(T_c) of S3.1, which assumes 7 m/s² for the other vehicle.
**Why it matters**: Safety-assurance readers associate RSS with provable bounds. The label invites them to read the 83% as evidence for an RSS-compliant design, when it is evidence for a heuristic prediction.
**Suggested fix**:
1. Call CK3 "a constant-deceleration braking prediction (3 m/s²)" throughout.
2. Add one sentence contrasting it with RSS's worst-case bound on the front vehicle's braking, and point to S3.1 for an RSS-form rule.

**Severity**: Minor
**Evidence Anchor**: text: §VI "a fixed 3 m/s² braking prediction, an RSS-style assumption [37]"
**Confidence**: 4 — core expertise: RSS and safe-distance models

### W6: Who bears the braking prior's costs is only partly named; comfort and following traffic are unmeasured
**Problem**: The "prior has costs" paragraph of §VI reports three things: lost progress (zero-margin caution of 1.72% against 1.10%), a scenario selection that favours the prior, and the untested case where braking never comes. It does not name two parties that pay for a planner that predicts braking for every moving lead with a nonzero acceleration estimate. Occupants pay through harder or more frequent early deceleration; caution measures how much speed is given up, not how. Vehicles behind the ego pay through rear-end exposure and car-following disturbances, which commercial adaptive cruise controllers already amplify (Gunter et al., below); the paper never mentions following traffic. The scope sentence of §I excludes other road users and scenarios but does not name them: pedestrians and cyclists, crossing and cut-in actors, vehicles behind the ego, and real sensor data.
**Why it matters**: §VII locates the measurable decision value in anticipating braking. A reader who weighs that value against its costs sees only the occupants' lost progress.
**Suggested fix**:
1. Name occupants' comfort and following traffic as unmeasured costs in the "prior has costs" paragraph and in §VI Limits.
2. As a comfort proxy that needs no new data, report for each arm, at matched caution, the distribution of the selected row's first target acceleration (the row labels of Table S7) or of its peak jerk.
3. In §I Scope, list the road users and scenarios left out.

**Severity**: Minor
**Evidence Anchor**: text: §VI "The prior has costs: its zero-margin caution is 1.72% against 1.10%" and "its cost where braking never comes is untested here"
**Confidence**: 4 — core expertise: how safety cases allocate residual risk

### W7: The headline results are hard for adjacent-field readers to use
**Problem**: The Abstract, contribution 3 and §VII state their results in the paper's own constructs: room, share, commitment, phase-weighted, counts (i) and (ii), and as scored. None of these comes with a plain statement of what it means in practice or a link to vocabulary that ITS and safety-assurance readers already use. The Notation table of §IV-C defines the terms but does not relate them to established ones:
- a wrong go is a binary criticality indicator: the plan would collide under an assumed ego response (Westhofen et al., below);
- the reaction-and-stop scoring resembles a proper-response check, made against the lead's actual motion rather than a worst case;
- caution is a progress, or over-conservatism, cost;
- the room is a value of perfect information [43].

"Commitment" is used in the Abstract without a definition.
**Why it matters**: The readers of this venue who would act on the result work outside tracking: planner integrators, safety engineers and assessors. If the last sentences of the Abstract cannot be parsed without the Notation table, the practical contribution reaches only specialists.
**Suggested fix**:
1. Add a summary of two or three plain sentences at the end of §I or the start of §VI. For example: for this tracker in lead braking, a fixed per-class margin works as well as the tracker's covariance; a simple braking prediction captures most of the achievable gain if each plan is followed for 3 s; and how much gain exists at all depends on what the evaluation assumes the car does after committing.
2. Add a column to the Notation table that maps each term to its nearest established counterpart, citing a review of criticality metrics.
3. Define "commitment" at its first use in the Abstract.
4. Optionally, add one sentence that places the study in the vocabulary of ISO 21448 (SOTIF): evidence on one mitigation of a perception insufficiency in one scenario class.

**Severity**: Minor
**Evidence Anchor**: text: Abstract "With that stop, unless those plans count as unsafe, too little room remains, phase by phase, for the braking prior's share to be measured."
**Confidence**: 4 — core expertise: communicating validation evidence to integrators and assessors

### W8: The transferable ratio check lacks a decision rule and guidance beyond this planner
**Problem**: §VI offers the ratio of the tracker's margin to the class-average margin on binding rows as a check other teams can run. Three things limit its use. "Nearly constant" is given no threshold; the paper's own case has 99.26% of rows within 5% of the median. "Binding rows" are defined only through this planner's critical scale (§III-B). The check's validity depends on the scenario mix it is run over (W1).
**Why it matters**: Without a rule and a recipe, a team with an optimisation-based or sampling-based planner cannot apply the check. Nor can it know when a result would license dropping the covariance margin.
**Suggested fix**:
1. State the criterion used here as a worked heuristic, for example a ratio within ±5% of its median in at least 99% of binding rows, and say that the threshold is not validated.
2. Say how to identify binding constraints in other planner types, for example the active constraints of an optimisation-based planner, or the constraint that sets each candidate's critical scale.
3. Require the check to be run over the full scenario mix, including track births and re-acquisitions.
4. Note that the second check, the graded oracles, needs logged ground truth.

**Severity**: Minor
**Evidence Anchor**: text: §VI "where it is nearly constant, the covariance can change few decisions once the margin's scale is tuned, whatever its calibration"
**Confidence**: 3 — adjacent expertise: planner integration; I am not a planning specialist

### W9: The operating domain of the recordings, and of the borrowed R157 values, is not stated
**Problem**: UN R157 and its 01 series [38], [39] apply to ALKS on roads where pedestrians and cyclists are prohibited and opposing traffic is physically separated, and their performance models were set for that domain. The manuscript states neither the road type or setting of the CARLA recordings (desired speeds 5–15 m/s, most decisions at standstill behind a stopped lead) nor that it borrows the regulation's values as reference parameters outside the regulation's scope.
**Why it matters**: Before giving the τ = 0.75 s results any weight, an assessor will want to know whether the regulatory parameters are applied inside or outside the domain they were set for.
**Suggested fix**:
1. In §III-A, give the road type and setting of the recordings.
2. In §IV-C, add that the R157 values serve as reference parameters, not as a claim about ALKS or about compliance.

**Severity**: Minor
**Evidence Anchor**: absence: §III-A and §IV-C — expected the road type and operating domain of the CARLA recordings and a statement that the R157 values are borrowed outside the regulation's motorway scope; checked §I Scope, §III-A, §IV-C, §VI Limits, Supplement S3.1, S3.2 and S8.1
**Confidence**: 3 — adjacent expertise: R157 scope; I am confident of the regulation's road-type scope but cannot tell from the text where the runs were recorded

### S1: An oracle positive control turns a null result into evidence
The design compares margins at equal caution against an oracle margin set from the realised error. Graded oracles then show where the measure can and cannot grade partial information (Table S12). Safety-validation teams could borrow this design for any question of the form "does this signal add value?". It separates "no value" from "a blunt measure", which most simulation studies in my field cannot do.
**Evidence Anchor**: text: §I "a positive control showing that better per-decision information could help on the same decisions at all"

### S2: Regulatory parameters are cited to clause level and used with explicit caveats
§IV-C and S8.1 cite the regulation down to annex and table, and they keep the planner's reaction time separate from τ. The derived values agree with my own reading of the regulation. 12.65 m/s³ is 0.774 g over 0.6 s, and 7.6 m/s² is about 0.774 g. The minimum following distances of S3.2 (10.30, 13.60 and 17.18 m at 8, 10 and 12 m/s) match the regulation's interpolated time-gap table. I could not consult the 01-series Annex 3 to confirm which of its tables lists the 12.65 m/s³ jerk for model 2.
**Evidence Anchor**: text: §IV-C "This is not a replanning model and τ is not the planner's own reaction time."

### S3: The main claim is fenced against the obvious overreach
The paper says repeatedly that it tests one raw covariance of a fixed-noise filter, in one scenario family, with simulated sensor data. It also gives the NIS evidence (median 0.24) that the simulated data make the covariance too wide, the opposite of what CANMOT's authors report on nuScenes. A reader cannot honestly cite this paper as showing that uncertainty does not help planners.
**Evidence Anchor**: text: §VI "the claim concerns this covariance, not uncertainty in planning in general"

### S4: An actionable lesson for open-loop evaluators
The paper shows that the room falls to 12%, or to 53% under count (ii), depending on what is assumed after the commitment. It then recommends that every open-loop decision score state its commitment assumption. That is a concrete reporting rule for designers of benchmarks and virtual tests, and it ties into the open-loop and closed-loop literature the paper cites [26]–[29].
**Evidence Anchor**: text: §VI "an open-loop decision score should state its commitment assumption and show how its conclusions move with it"

### S5: A cheap diagnostic that needs no ground truth
Any team can compute, from its own logs and without labels, the ratio of the tracker's margin to a class-average margin on binding rows. The ratio shows immediately whether a covariance can change decisions once the margin's scale is tuned. W8 asks for a rule that would make the check usable.
**Evidence Anchor**: figure: Fig. 2(b) — tracker margin over class-average margin on 152,264 binding rows, 99.26% within 5% of the median 1.10

### Cross-Disciplinary Reading Recommendations
- Westhofen et al. (2022), a review of criticality metrics for automated driving: for mapping the wrong go and the reaction-and-stop scoring onto established criticality metrics (W7).
- Riedmaier et al. (2020), a survey of scenario-based safety assessment: for placing a single-family evaluation within a scenario-coverage argument and naming what the scenario set leaves out (W1, W6).
- Gunter et al. (2021), on the string stability of commercial adaptive cruise control: evidence that the braking behaviour of car-following controllers reaches following traffic (W6).
- ISO 21448:2022 (SOTIF): vocabulary for perception insufficiencies and their mitigations (W7).

~~~yaml suggested-references
- title: "Criticality Metrics for Automated Driving: A Review and Suitability Analysis of the State of the Art"
  authors: ["Westhofen, L.", "Neurohr, C.", "Koopmann, T.", "Butz, M.", "Schütt, B.", "Utesch, F.", "Neurohr, B.", "Gutenkunst, C.", "Böde, E."]
  year: "2022"
  doi: "10.1007/s11831-022-09788-7"
  arxiv_id: "2108.02403"
- title: "Survey on Scenario-Based Safety Assessment of Automated Vehicles"
  authors: ["Riedmaier, S.", "Ponn, T.", "Ludwig, D.", "Schick, B.", "Diermeyer, F."]
  year: "2020"
  doi: "10.1109/ACCESS.2020.2993730"
  arxiv_id: null
- title: "Are Commercially Implemented Adaptive Cruise Control Systems String Stable?"
  authors: ["Gunter, G.", "Gloudemans, D.", "Stern, R. E.", "McQuade, S.", "Bhadani, R.", "Bunting, M.", "Delle Monache, M. L.", "Lysecky, R.", "Seibold, B.", "Sprinkle, J.", "Piccoli, B.", "Work, D. B."]
  year: "2021"
  doi: "10.1109/TITS.2020.3000682"
  arxiv_id: "1905.02108"
- title: "ISO 21448:2022 Road vehicles — Safety of the intended functionality"
  authors: ["International Organization for Standardization"]
  year: "2022"
  doi: null
  arxiv_id: null
~~~
