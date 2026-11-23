# ARS Pre-Submission Review — MANUSCRIPT v10 (target: IEEE OJ-ITS, regular paper)

**Time stamp:** 2026-11-18 14:47 −05:00 (local clock, read before writing)
**Manuscript:** "Does a Kalman Tracker's Covariance Improve Car-Following Decisions? A Decision-Level Evaluation in CARLA Lead-Braking Scenarios" (`review_v10_input\MANUSCRIPT_v10.md`, `SUPPLEMENT_v10.md`, `SUPPLEMENT_FULL_CAPTIONS_v10.md`, 7 figures). Input SHA-256 prefixes as read: manuscript 0e69dc2a624eae8e, supplement 3ad7ab8fa7faa6af, captions fa73b82e0bcd458a. Inputs were not modified.

## 1. Skill used and how the review ran

- **Skill:** `academic-research-skills:academic-paper-reviewer` v1.11.1 (ARS plugin 3.24.3, enabled in this folder), mode **`full`**: the plugin's most thorough review mode. It runs a five-seat referee panel (Journal-Fit Reviewer + three peer reviewers + Devil's Advocate) and an editorial synthesizer, under the sprint contract `reviewer/reviewer_full/v2`.
- **Phase 0 (field analysis):** coverage check (every supplied part read; nothing unreadable; no text aimed at reviewers) and four reviewer cards. These are in `ARS_PHASE0_FIELD_ANALYSIS_v10_v01.md`. The cards were shown and the user accepted them without edits ("Do a full ARS review").
- **Panel:**
  - Journal-Fit Reviewer: OJ-ITS associate editor.
  - Peer Reviewer 1, Methodology: cluster-bootstrap and off-policy evaluation statistician.
  - Peer Reviewer 2, Domain: chance-constrained planning and tracking.
  - Peer Reviewer 3, Practical: automated-driving safety assurance, UN R157/RSS.
  - Devil's Advocate.
- **Seat runs:** each seat ran a paper-blind Phase 1 (scoring plan) and a paper-visible Phase 2 (review) in separate fresh contexts. No seat saw another seat's output.
- **Checks:** all ten seat outputs passed `check_phase_conformance.py`, and the panel passed `check_panel_synthesis.py --layer1-only`. The synthesis passed `check_panel_synthesis.py` (exit 0). The panel provenance artifact passed `review_panel_provenance.py validate`.
- **Decision rule:** under the contract, the decision is mechanical: dimension scores feed fixed failure conditions.
- **Disclosures that bound this review:**
  - All five seats ran on one model family (Claude Opus 5.5). Role separation does not remove correlated-error risk.
  - `calibration_status: NOT_CALIBRATED`: the panel is not calibrated against human referees.
  - Cross-model verification was not run.
  - No formal venue-criteria manifest was supplied. Venue judgements use only the stated constraints (abstract ≤ 250 words; no page limit, 10 pages recommended).
- **Deviations from the plugin's literal protocol (all in `ARS_work_v10_v01\`):**
  1. The provenance builder was run through a small wrapper (`run_provenance_lf.py`), because this Windows install's `full.json` has CRLF line endings. Its raw SHA-256 differs from the pinned LF digest. Plugin files were not modified.
  2. Phase 2 seats used the conformance checkers as their pre-send structural preflight. All passed on the first run, with no structural fixes needed.
  3. The claim-check judge read its 270 KB prompt with the Read tool (the prompt says "no tools").
  4. A helper agent drafted the author letter, which the plugin's checker then checked (see §7).
- **External traffic:**
  - The Domain and Practical seats ran a few short generic keyword web searches, no manuscript text.
  - The suggested-reference check sent only the reviewers' suggested reference titles and identifiers to bibliographic indexes, anonymously.
  - No manuscript text left the machine.

## 2. Verdict

| Question | Answer |
|---|---|
| **Desk-rejection risk** | **Moderate as v10 stands; low once four gating items are fixed** (Journal-Fit seat; no other seat assessed it): (1) unfilled author block, repository/DOI line and AI-use disclosure → administrative return before screening; (2) title and headline lead with a null the paper itself calls expected; (3) abstract not parseable by a general ITS reader; (4) main text an estimated 12–14 IEEE pages vs 10 recommended (an estimate from word and display-item counts, not a typeset count). None needs new experiments. |
| **Most likely referee decision** | **Major Revision.** Mechanical result: `dimension_verdicts: [D1=block, D2=warn, D3=block, D4=warn, D5=warn, D6=warn]`, `fired_conditions: [F2, F3, F5]`, `editorial_decision=major_revision`. F2 fired because two mandatory dimensions were blocked: D1 (methodology rigor) by Reviewer 1, and D3 (argument coherence) by the Devil's Advocate. **Both blocks are declared repairable; no seat declared a fatal block; the Devil's Advocate's CRITICAL table is empty.** No sub-claim reached 3- or 4-seat consensus. Nine severity splits were arbitrated by the synthesizer. |
| **Core result** | **Every seat that addressed it finds the covariance null robust.** Reviewer 1: "None of these overturns the covariance null". Reviewer 2: neither Major finding "touches the covariance null". Reviewer 3: the main claim is "scoped with unusual care". DA: "The covariance null survives all six". The required work concerns the inferential support and scope of the **secondary** headline numbers (the 83%, the 12%/53% commitment bracket, "at most about 0.4%", the location claim), plus framing, abstract, length, scope fences and reproducibility. |
| **Volume** | 20 required revisions (R1–R20) and 38 suggested (S1–S38; 4 of them optional "consider" items). Of the required items, seven ask for **re-analysis of stored data**: R9–R12, R17, R19, R20. None asks for new CARLA recordings. The rest are wording, structure or documentation. |

## 3. Blocking issues (the three the decision rests on)

Numbers B1–B3. The roadmap refs (R/S) point into `ARS_DECISION_PACKAGE_v10_v01.md` Part 2.

**B1. The bootstrap intervals behind two abstract claims are not validated (Reviewer 1; D1 block). Resolved by R9 + R8.**
- **Location:** §IV-B para. 4; §V-A para. 2; Abstract; §I contribution 2; §VII; Table II; Table S5 footnote.
- **Evidence:**
  - Percentile intervals on the non-smooth step-frontier statistic have coverage stated as "not verified".
  - RR(N)'s point (0.00122) lies above its own percentile interval [−0.00108, 0.00119].
  - "At most about 0.4%" comes from the upper end of a basic interval "chosen after the results".
  - That basic interval is 2·0.00122 − [0.00119, −0.00108] = **[0.00125, 0.0035]**, and its lower end excludes zero (I verified this arithmetic). So the two interval types disagree on whether RR(N) differs from zero.
  - The same intervals decide the NIS-inflated wording ("distinguishable from zero, 0.7–2.5%"). That effect comes from 217 decisions in 14 of 35 unequal runs, with no stratification.
- **Fix:**
  - State whether the 201 caution levels are rebuilt in each resample.
  - Estimate actual coverage on the stored arrays: a run-level double bootstrap, or m-out-of-n run subsampling (m ≈ 15–25).
  - Report intervals from the method that passes, with a sensitivity analysis stratified by recording setting α.
  - Re-apply the five fixed NIS-inflated wording rules to the new interval.
  - Replace "at most about 0.4%" with the validated bound or a descriptive statement (0.6 of 8,290 decisions). If the basic interval is kept, print both ends.

**B2. The headline location claim ("the decision value we could measure lies in anticipating braking") rests on unsupported premises (Devil's Advocate D3 block; Reviewer 1 D3 warn). Resolved by R10–R13 with R3 (and S18, S32, S37, S38).**
- **Location:** §I contribution 3; §IV-B para. 2; §VI "Where the decision value lies"; §VII.
- **Evidence:**
  - Only about 127 of the braking prior's ~383 pooled decision gains appear on the phases' own frontiers. The rest is attributed to "how one margin scale spends caution across phases … a mechanism that no analysis here isolates" (§IV-B).
  - The pooled room is 2.6× the decision-weighted phase rooms, so it scales with how long recordings ran after the stop (82.7% of decisions come after the stop).
  - Caution averages only truly safe selections, so it conditions on the outcome. Where signed caution was tried (τ = 0.75 s), the prior's ego-moving and phase-weighted shares turn negative (Table S13). The 3 s shares, including the 83%, were never rerun this way (§VI Limits says so).
  - The prior's cost where braking never comes is untested.
  - Its value is open-loop and off-policy.
- **Fix:**
  - **R10:** judge censored reaction-and-stop pairs against the logged truth beyond 3 s (see major finding 10).
  - **R11:** rerun the 3 s scoring with signed caution for every arm.
  - **R12:** run a post-stop truncation sensitivity and a per-phase-scale frontier.
  - **R13:** print the ego-moving and/or phase-weighted share beside the 83% and name the population.
  - **R3:** word §VII conditionally on the commitment.
  - **S18:** add "on runs in which the lead always brakes", or score CK3 on non-braking runs.
  - **S38:** call the 83% an open-loop, off-policy share.

**B3. The room and every commitment ratio are defined for contact (0 m gap), although the regulatory model the paper adopts specifies a 2 m standstill gap (Reviewers 2 and 3; basis of the D2 warn). Resolved by R17 + R18.**
- **Location:** §IV-C; §V-C ("The as-scored conclusion at τ = 0.75 s therefore rests on the performance-model values of the 01 series"); Table S6 and its footnote; Supplement S3.1.
- **Evidence:**
  - S3.1 uses d_stop = 2 m and b_o = 7 m/s² from performance model 2. The open-loop scoring borrows only 0.75 s and 6 m/s², with zero gap.
  - At 2 m, Table S6 prints the 3 s oracle's advantage and RR(N) but no ratio, "where the 3 s oracle is not an oracle".
  - The perfect oracle O and den₀ are not computed at 2 m. *Precision note:* the 2 m gap is scored for R and RR(N) (Tables S6, S1); what is missing is an evaluable room or share there.
- **Fix:**
  - State in §IV-C that a wrong go means contact, that model 2's 2 m gap and 7 m/s² are not used, and why.
  - Score O at the 2 m gap and report den₀ (and shares where evaluable).
  - Reword the "rests on the performance-model values" sentence and the matching Limits clause: two ego parameters of model 2, used as a nominal parameterisation with zero gap.

## 4. Major findings (required revisions, R1–R20)

Each entry: ref · location · problem (evidence) · fix. Severity as transported from the reviewer cards; "split" = seats disagreed on Major vs Minor and the synthesizer arbitrated to required. B1–B3 above are R8/R9, R10–R13 and R17/R18.

**Framing, abstract, length and submission readiness**

1. **R1 — Title asks a question theory already answers** (Journal-Fit major / Domain minor; split).
   - **Location:** Title; Abstract sentence 1; §I para. 4.
   - **Problem:** §I says "For a fixed-noise Kalman filter the covariance's null is expected", but the title asks generically about "a Kalman Tracker's Covariance".
   - **Fix:** qualify or retitle around the question actually answered (a decision-level, equal-caution evaluation of tracker-covariance margins, with the fixed-noise tracker as the case). Say in §I that the null is the steady-state expectation.
   - *Advisory:* the claim check found that the abstract's first sentence already names CANMOT as "a fixed-noise Kalman tracker", so the fix mainly concerns the title.
2. **R2 — The contribution list leads with confirming an expected steady state** (Journal-Fit major).
   - **Location:** §I contribution list.
   - **Fix:**
     - Put the evaluation design (equal caution, oracle positive control, graded oracles) and the commitment dependence first.
     - Present the covariance diagnostic as a confirmatory test.
     - Add one sentence on why the expected null still needed measuring (the covariance also depends on detections, misses and track age; §VI).
3. **R3 — The practical take-away under the realistic commitment is unstated** (Journal-Fit major).
   - **Location:** §IV-C ("The 3 s commitment scoring is a stress scoring."); §VI; §VII last sentence.
   - **Problem:** the positive result (83%) comes from the scoring the paper calls a stress case.
   - **Fix:**
     - Add a §VI paragraph: which commitment model is representative of the planner's replanning and why; the practical reading under each; and the closed-loop test that would settle it.
     - Word the Conclusion conditionally.
4. **R4 — Main text an estimated 20–40% over the recommended 10 pages** (Journal-Fit major).
   - **Location:** Table IV (16 rows × 5 populations); §III-A stopping-point paragraph; §V-C signed-caution and stop-deceleration paragraphs; §V-D; inline provenance markers; repeated numbers (83% six times in the main text).
   - **Fix:**
     - Replace Table IV with a five-row table (den₀; RR₀ of N, NA, CK3, AM) and move the rest to S8.
     - Move §V-D to S9, keeping a two-sentence summary.
     - Move the stopping-point paragraph to S2.
     - Cut the signed-caution and stop-deceleration paragraphs to one sentence each.
     - Replace inline provenance markers with one sentence in §IV-D.
     - State each headline number once.
5. **R5 — Abstract not self-contained** (Journal-Fit major / Practical minor; split).
   - **Location:** Abstract.
   - **Problem:** it uses step and convex-hull frontiers, phase shares and "those plans" without definition, carries about twenty numbers, and ends on what cannot be measured. It is at 249/250 words, so the required wording changes elsewhere cannot be absorbed without a rewrite.
   - **Fix:** rewrite to about 200–230 words in plain terms: question; method in one sentence; three results; one implication. If the plan's consequence rules bind the abstract's wording, keep the claims, word them plainly, and log the mapping in Table S4.
6. **R6 — Author block and AI-use disclosure are placeholders** (Journal-Fit minor; required as a submission gate).
   - **Location:** Author block; Acknowledgment.
   - **Fix:** complete the author block. Finalise the IEEE AI disclosure: delete the approval note; name the tool and version; state the sections with AI-generated text, the extent of AI involvement in code and literature summaries, and what the author verified.
7. **R7 — Pre-specification cannot be checked without a deposit** (Journal-Fit minor / Methodology major; split).
   - **Location:** Data and Code Availability; §IV-D ("The plan, its SHA-256 and every amendment are released with the code").
   - **Fix:**
     - Deposit both plans (with amendments and lock manifests), the code and the per-decision arrays under an archived DOI that referees can access.
     - Fill in the statement, and say which raw recordings can be shared.

**Statistics and inference (B1, B2)**

8. **R8** — see B1: replace "at most about 0.4%" (Abstract, contribution 2, §V-A, §VII) (Journal-Fit minor / Methodology major; split).
9. **R9** — see B1: validate the step-frontier bootstrap (Methodology major).
10. **R10 — The reaction-and-stop results rest on single imputations of censored plans** (Methodology major; corroborated by the DA).
    - **Location:** §IV-C para. 2; §V-C para. 2; Table III; Tables S6 and S10.
    - **Problem:** at τ = 0.75 s, 5,356 decision–row pairs have a stop unfinished within the 3 s window, against 3,334 judged unsafe. The bracket in the abstract (12% or 53%) depends on how they are counted. Only 153 pairs are unfinished at the end of the recording, so the logged truth after 3 s can presumably judge most of the rest.
    - **Fix:** judge them against the logged truth until the stop finishes (or explain why that truth cannot be used). Report this as the estimate, and keep counts (i) and (ii) as sensitivity analyses. Update the Abstract's 12%/53% sentence.
11. **R11 — Caution conditions on the outcome** (Methodology major; corroborated by the DA).
    - **Location:** §IV-A ("Decisions whose selected row is unsafe do not enter this average"); §VI Limits; Table II.
    - **Fix:** rerun the 3 s scoring with signed caution over all evaluated decisions, for every arm and population (the code exists for τ = 0.75 s). Print the results beside Table II, and revise the 83% sentence and the Conclusion if a sign or wording branch changes.
12. **R12 — The pooled estimand is set by post-stop recording length; the cross-phase mechanism is not isolated** (Methodology major; corroborated by the DA).
    - **Location:** §IV-B para. 2 (2.6×); §V-A; §VI; §VII.
    - **Fix:** run a truncation sensitivity on the post-stop segment (for example, cap it at a fixed duration). Isolate the mechanism with a per-phase-scale frontier.
13. **R13 — The 83% is printed only as a pooled figure** (Methodology major / Domain minor; split).
    - **Location:** Abstract; §VII.
    - **Fix:** print the ego-moving share (0.47 [0.35, 0.57]) and/or the phase-weighted share against a perfect oracle (0.665) beside it, and name the population that defines the room.
14. **R14 — The data cannot be regenerated from the paper** (Methodology major).
    - **Location:** §III-A; Supplement S1–S2. Confirmed absent by a full-text search: CARLA version, map, weather and sensor settings; CenterPoint checkpoint and training data; CANMOT per-class noise matrices and gating; per-run scenario parameters; recording-planner settings.
    - **Fix:** add a configuration table with software versions.

**Domain accuracy and regulatory use (B3)**

15. **R15 — "RSS-style" mislabels the braking prior** (Domain major / Practical minor; split).
    - **Location:** §II; §VI ("a fixed 3 m/s² braking prediction, an RSS-style assumption [37]").
    - **Problem:** RSS is a worst-case envelope; CK3 is a nominal constant-deceleration prediction.
    - **Fix:** call CK3 a constant-deceleration braking prediction, contrast it with RSS's worst-case bound in one sentence, and keep the RSS label for the S3.1 rule only.
16. **R16 — The 3 m/s² value sits inside the recorded leads' braking range and its choice is unstated** (Domain major).
    - **Location:** §III-C; §VI Limits.
    - **Fix:** state how 3 m/s² was chosen on the tuning runs, and add to Limits that it lies inside the evaluation runs' 2.0–5.5 m/s² range. A deceleration sweep is optional (S20).
17. **R17** — see B3: state the zero-gap definition; score O at 2 m (Domain major; Practical major).
18. **R18** — see B3: reword "rests on the performance-model values" (Domain minor / Practical major; split).

**Scope fences**

19. **R19 — The null is not fenced against removing a deployed stack's covariance margin** (Practical major).
    - **Location:** §I Scope; §VI ("a class average does as well as the tracker's covariance"); Supplement S9: every lead-braking decision is in the oldest track-age band, so the planned split by track age is empty.
    - **Problem:** the tested decisions contain almost no track births, re-acquisitions or new actors.
    - **Fix:**
      - Say the result does not justify removing or freezing covariance margins in a deployed stack.
      - Report D(N, F0) near the 45 track initialisations, or state that they are too few.
      - Name new and cut-in actors as untested.
20. **R20 — Cross-family reallocation of one tuned margin scale is untested** (Practical major).
    - **Location:** §VI; §III-C (F0 built from six families).
    - **Fix:** apply the ratio check to the tuning runs of the other five scenario families and report the median N/F0 ratio per family. If the levels differ, state that cross-family reallocation of caution is untested.

## 5. Minor findings (suggested revisions, S1–S38)

Each: ref · location · fix. All are Minor unless marked; "optional" = a stronger or costlier option a seat offered, which the package classes as consider.

**Positioning, disclosure and presentation (Journal-Fit)**
- S1 (optional, from a Major finding) · §I, §II · Apply the evaluation to one source whose covariance varies per decision (the calibrated covariance of [9], or an IMM tracker).
- S2 (Journal-Fit + Domain) · §II; Supplement S6 (IMM/adaptive literature "not searched for a planner-side test"; few T-ITS/ITSC/OJ-ITS references) · Extend the novelty search to ITS venues, threat assessment and collision probability, and IMM/adaptive trackers in ACC and collision warning; add a §II paragraph; narrow the novelty sentence if needed.
- S3 · §I Scope; refs [8], [9], [14], [17], [19] · Upload [9] as a confidential related manuscript, state shared and new content in the cover letter, and cite published versions of the preprints where available.
- S4 (Journal-Fit + Practical) · §I; contribution 3; Notation table placement · Give plain one-sentence definitions of room, caution and the two commitment models in §I, move the Notation table to the start of §IV, and add a 2–3 sentence plain summary.
- S5 · Table III, Table S6, Fig. 4(b); arm names · Use one name per arm after §III-C, and relabel the R/RR(N) columns under reaction-and-stop as RR_E(N), with a distinct symbol for the 3 s oracle's advantage there.
- S6 · Table S12 (cited from §IV-B, V-B, V-C, VI) · Bring a compact graded-oracle table (p = 0.25/0.5/0.75; all, ego moving, lead braking, phase-weighted) into §IV-B or beside Fig. 3.
- S7 · §IV-C ("Two further checks follow review requests"); §IV-D; §V-C · Describe post hoc analyses neutrally, drop references to reviews and to rules governing the abstract, keep the audit trail in S4, and declare any previous venue in the cover letter.
- S8 · Figs. 1–4 and Tables I–IV (two caption files) · Give each one self-contained in-paper caption and drop the supplementary duplicate.
- S9 (Journal-Fit + Domain minor / Practical major; split) · Fig. 2(b) · Characterise the 1,127 rows outside the 5% band (including the group near 1.7) by track age or re-initialisation.
- S10 · Table II; Abstract · Adopt one number-format convention (for example, percentages to two significant figures in prose and decimals to three in tables).
- S11 (Journal-Fit + Methodology) · Abstract ("On 35 runs not used to design the margins") · Add that the room and the tracker covariance had been examined on these runs earlier in an exploratory analysis (a transfer, not a replication).
- S12 · Index Terms · Add car following, adaptive cruise control, safety evaluation and simulation-based testing.

**Methodology (Reviewer 1)**
- S13 · Supplement S1 ("The replay identity was checked on the tuning runs only") · Reproduce the logged selections on the evaluation runs, and state that lead braking is scripted and independent of the ego.
- S14 · §III-A (five short runs, 18–53 decisions; their NIS is 1.02–2.41) · Explain why they are short, count the NA-changed decisions in them, and recompute R, RR(N) and RR(NA) without them.
- S15 · §IV-C ("a resolution rule of our choosing") · Report the wording branch at thresholds of 5 and 20 decision-equivalents and on den₀'s lower limit.
- S16 · Table S10 (count (ii), τ = 0.75 s, lead braking: 0.266 [0.098, 1.237]) · Use joint or Fieller-type intervals where den₀ approaches zero, and flag those cells.
- S17 · Abstract; §VII · Mark the commitment analyses as descriptive analyses added after the first results.
- S18 (Methodology minor; DA major) · §VI ("its cost where braking never comes is untested here") · Score CK3 on non-braking runs, or add "on runs in which the lead always brakes" to the 83% sentence.
- S19 · Supplement S8.1 (one random draw) · Repeat the graded oracles over about 50 draws and report the spread.

**Domain (Reviewer 2)**
- S20 (optional, from a Major finding) · §VI · Sweep the braking prior's deceleration (2, 4, 6, 7 m/s²).
- S21 (optional) · Contribution 2 · Compute the steady-state covariance and the margin ratio it implies; show how common fixed-noise trackers are.
- S22 · §III-B; Table I · State that the margin is propagated without process noise, and why.
- S23 · §V-B heading; §II; §VI · State that NA tests only the output-covariance channel, not the gain or state effect of adaptive filtering.
- S24 (split on existence) · §V-D; §VI; §VII · Present §V-D as a consistency check of the ratio result (ranking located in the state's age), not as independent evidence.
- S25 · §III-A (~2 Hz updates) · Justify the update rate, add it to Limits, and scope §V-D to it.
- S26 · §VII; Table I · Phrase the location claim as a ranking among the tested sources, and name a time-gap margin as untested.
- S27 (optional) · Table I · Add a constant time-gap arm.
- S28 (Domain + Practical) · §IV-C; §III-A · Call the 01-series values nominal reference parameters borrowed from an ALKS (motorway) performance model, with no compliance claim.
- S29 · §V-C; Table III · Present the τ and A sweeps as the result, with 0.75 s and 6 m/s² as one point on them.

**Practical (Reviewer 3)**
- S30 · Supplement S2 ("No recording brakes above 5.5 m/s²."); §III-A; §I Scope · State the 2.0–5.5 m/s² range and qualify the 12% and 53% "for leads braking at up to 5.5 m/s²".
- S31 · Supplement S3 opening; Fig. S3 caption; §VI · Add the full-braking fallback share (0.70–0.72) and the contact count, and say the gap figures are not design guidance.
- S32 (Practical minor; DA major) · §VI ("The prior has costs") · Name occupants' comfort and following traffic as unmeasured costs; report a jerk or first-target-acceleration proxy at matched caution.
- S33 · §I Scope · List the road users and scenarios left out (pedestrians, cyclists, crossing and cut-in actors, vehicles behind, real sensor data).
- S34 · Notation table · Map each term to established ITS and safety vocabulary (criticality metric, proper response, over-conservatism, value of perfect information).
- S35 · §VI "What carries over" · Give the ratio check a worked threshold and guidance for other planner types.
- S36 · §III-A · State the road type and setting of the CARLA recordings.

**Devil's Advocate only** (Major in the DA card; outside the four-seat count; should-fix)
- S37 · Table S12 (a noisy oracle with σ = 2 still recovers 0.820 at 3 s) · The room is not one a covariance-shaped margin can use, so "0.4% of the room" against the prior's 83% is not like for like. Add a positive control in the covariance's own form, or rephrase the contrast as mean-path correction versus variance margins.
- S38 · §III-B ("for the other margin sources they are off-policy"); Supplement S3.1 · Run CK3 (and NA) in the existing simplified closed loop, or call the 83% an open-loop, off-policy share in the Abstract and §VII.

## 6. What the paper does well

These strengths are confirmed across seats (counts are of the four non-DA seats):
- **A cheap, portable diagnostic (all 4 seats, and the DA):** the ratio of the tracker's margin to a class-average margin on binding rows (Fig. 2(b)) needs no ground truth and is the most reusable idea.
- **An actionable evaluation lesson (all 4):** open-loop decision scores must state their commitment assumption, and Fig. 4(a) shows how strongly the room moves with it.
- **A working positive control (3 of 4):** the oracle margin, plus graded oracles that test whether the measure grades partial information (Table S12). The pooled null is therefore not a blunt-measure artefact, and the room is correctly framed as the value of perfect information.
- **Unusual transparency (Journal-Fit, Methodology):**
  - pre-specification with hashed plans;
  - Table S4 setting every post-results wording change beside the fixed wording;
  - per-value verification status (one or two programs);
  - a candid Limits paragraph.
- **The null is explained, not only reported (Methodology, Domain):** steady-state Riccati reasoning, the 1.10 ratio, and §V-D locating the error ranking in the state's age.
- **Covariance consistency is measured, not assumed (Domain):** NIS (Fig. S1) and RMS z.
- **Regulatory anchoring (Journal-Fit, Practical):** UN R157 values cited to clause level, with explicit caveats.
- **Internal consistency:** the Journal-Fit seat's spot checks reconcile (2.6× phase ratio, 383 and 127 decisions, phase counts summing to 8,290). Reviewer 1 checked every number in the Abstract, the contributions and the Conclusion against its table and fixed rule and **found no inconsistency**. Five consistency (GRIM) receipts were all consistent. **No seat reported an arithmetic error.**
- **Scope:** claims are fenced to this tracker, this planner and lead braking (§I Scope; §VI).

## 7. Advisory checks (script output; they do not change the decision or any finding)

- **Reviewer claim check (#1002):** of 55 findings, 52 were judged consistent with the manuscript text and 2 cannot be checked from the text alone (an image detail of Fig. 2(b); the page estimate). One was marked contradicted: Reviewer 2's statement that the abstract's first sentence poses the question for a generic Kalman tracker. That sentence already says "a fixed-noise Kalman tracker". R1's fix therefore concerns mainly the title.
- **Suggested-reference check (#1001):** 8 of the 9 references suggested by Reviewers 2 and 3 were found in a bibliographic index. ISO 21448:2022 was not matched (it has no DOI to check). "Found" does not show relevance.
- **Acronym check (#849):** CANMOT, CARLA, RR, RMS and SHA are used without expansion (CANMOT and CARLA also in the abstract), and NIS is defined twice. The tool also flags placeholder words (AUTHOR, BLOCK, TO), the word TABLE and the numeral IV, which are tool artefacts.
- **Author letter (#1078):** `ARS_AUTHOR_LETTER_v10_v01.md` restates all 58 changes for the author, without internal ids (items 1–20 = R1–R20, 21–58 = S1–S38; item map in its appendix). A helper agent drafted it from the package. `check_author_letter.py` → `AUTHOR-LETTER: PASS` (exit 0, first run; re-run by this session, same result). No corrected copy was needed.

## 8. Files (all in `review_v10_output\`)

- `ARS_REVIEW_v10_v01.md`: this summary for the lead session.
- `ARS_DECISION_PACKAGE_v10_v01.md`: the record. It contains:
  - provenance;
  - the mechanical decision record;
  - consensus and the nine arbitrations;
  - the full roadmap (R1–R20, S1–S38) with transported severities, anchors and confidences;
  - the reviewer summaries;
  - the three advisory attachments.
- `ARS_AUTHOR_LETTER_v10_v01.md`: the author-facing letter (checker PASS).
- `ARS_PHASE0_FIELD_ANALYSIS_v10_v01.md`: coverage and reviewer cards.
- `ARS_work_v10_v01\`:
  - the contract;
  - the metadata;
  - the five Phase 1 plans (`P1_*.md`) and Phase 2 reviews (`P2_*.md`);
  - the synthesis;
  - the provenance input and artifact, and the wrapper;
  - the claim-check prompt, key and reply;
  - the reference and acronym check outputs.
