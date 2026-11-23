# Claim audit v13, delta v11 (panel round)

**Auditor model:** Claude Fable 5.2 (the writer is Claude Opus 5.5). 21 Nov 2026, time-boxed (about 12 minutes).

**Scope:** changed lines only (`DIFF_MANUSCRIPT_v13.txt`, `DIFF_SUPPLEMENT_v13.txt`, `DIFF_RESPONSE_TO_REVIEW_v13.txt`), read against the panel record (`ARS_REVIEW_SPRINT_v01.md` §2 and §3) and, for numbers and pointers, the tables of `MANUSCRIPT_v13.md` and `SUPPLEMENT_v13.md` in `audit_v11_input`.

**Not checked:** the exports (A_EXPORT_*.json) and DERIVED were not opened, so the new numbers were checked against the printed tables only; the count "246 of 246" (Supplement S12) was not recounted; no build was run; word counts are taken from the build report.

**Result:** 0 H, 1 M, 9 L. R1–R9, R11, R12 implemented; R10 partly.

## 1. R1–R12

| Item | Status | Evidence (new text) | Note |
|---|---|---|---|
| R1 one label | yes | Table I: "*Confirmed*; *passed (amendment)*; *descriptive*; *exploratory*" with the panel's meaning verbatim. §V-E: "(passed; amendment)" ×2, "(classified as uninformative variation, Section IV-C's class name; passed, amendment; …)", "(passed; specified post hoc)". S32–S34: "(A)"; S32 caption "(A) passed in its amendment sequence". S36 caption "(passed; specified post hoc)". Table S5 row added. §IV-E: "the later amendment's are marked "passed (amendment)"". | No "confirmed" or "(C)" is left on an amendment test in the manuscript, supplement or letter (grep). The remaining "confirmed" are the original plan's (§V-A, §V-B, Tables II, S4). |
| R2 dropout "equivalence" | yes | Abstract: "it shows no recovery of a small room (0.16 points) in fresh pedestrian crossing and recovers a small 2.8% of the room under detection dropouts (re-scored runs), a gain not found inside the dropouts"; "In tests added by a later amendment, where the fixed-noise covariance varies more (open loop),". §V-E: "(its upper end lies just below δ = 0.05; no equivalence test was registered here), against". §VII: "(its oracle: 40%)", "confirmed but" gone. | "(re-scored runs)" keeps the meaning of "(the same runs re-scored)". |
| R3 not inside the dropouts; conditions | yes | "Among the 3,644 decisions inside a dropout its share is −0.003 [−0.020, 0.015] (descriptive; Table S34), so the pooled gain is not shown to come from the covariance's growth while a track coasts, and its source is not identified." "every arm keeps an unmatched track for up to three updates, the longest masked stretch (a pre-registered output-rule change), so track loss after longer gaps was not tested". "In pedestrian crossing we read the bottleneck as the information in the covariance, not its amplitude." | 3,644 and the share match Table S34. Dropping the second half is the option the record allows ("or keep it and drop the second half"); the efficiency 0.071 [0.016, 0.129] is printed once. |
| R4 higher level | yes | §V-E: "At the higher level (secondary; not caution-matched) the covariance arm had fewer contacts (5% against 15% of 60 cases) and lost 0.25 [0.15, 0.36] s more; without caution matching this cannot be told from a wider margin, which is the expected effect of a covariance that grows while a track coasts. The IMM's is inconclusive". §VII: "had fewer contacts for more time lost, as a wider margin would". | 0.25 [0.15, 0.36] matches Table S35, which keeps the class name. |
| R5 braking prediction's closed loop | yes | Abstract: "In closed loop (lower caution level; class-average contacts 20%), the prediction removed the contacts for 0.16 s more time lost, as did a plain time gap." The three cuts are made. §V-C: "the plan's class: time lost below 0.5 s"; "These classes concern the ego's contacts and time only; cost to following traffic and occupants is not scored (braking outcomes: Supplement S9)." | Compression keeps the meaning (Table IV: F0 20%, CK3 0%). See M1 on "as did a plain time gap". S9 does hold peak deceleration, jerk and full-braking share. |
| R6 crossing | yes | §VII: "it showed no recovery of a small room in fresh pedestrian crossing (share −0.07 [−0.22, 0.03]; its oracle: 69%)". Contribution 2: "it shows no recovery of a small room in pedestrian crossing". §V-E: "Section IV-C's class name; … no permuted-twin test of the covariance was run here". | Rounding of −0.0675 [−0.2210, 0.0339] is right. |
| R7 multiplicity and locks | yes | "Sequences are not adjusted for one another. The locks are SHA-256 hashes with local file times, not third-party timestamps." | "each is tested one-sided at 0.025" is carried by the sentence before ("a fixed sequence, one-sided at 0.025"). |
| R8 operating points | yes | "The two levels were set so that contacts were frequent enough to compare (class-average contact shares of 20% and 5%); neither is a deployed operating point, and with 60 cases per arm contact differences much below 0.10 cannot be resolved. Equivalent here does not mean safe." | Meaning kept. 20% and 5% match Table IV. |
| R9 expected; contribution 2 | yes | "**A confirmatory test and amendment tests.** … and in closed loop, as its near-constancy led one to expect; the test adds the bound; … where the fixed-noise covariance varies more (later amendment; Section V-E), it shows no recovery …" | See L3 (punctuation). |
| R10 split §V-E | partly | Four paragraphs as asked; "(interval level: Table S33)" (Table S33 does print "nominal 99% interval, the plan's fallback"). | "End each with one plain sentence of what it shows" is met by paragraphs 2 and 3 only. Paragraph 1 ends on the output rule and paragraph 4 on the twin's detail. Acceptable under the caps (L4). |
| R11 "no room" | yes | "; the cut-in runs are uninformative, not a negative result"; "; they neither support nor contradict the simulated results"; §VII "showed no measurable room, so they tested nothing." | The letter's quoted Result (line 68) carries the same text. |
| R12 scope | yes | "One simulated configuration was tested: one detector, one in-house planner and straight roads at desired speeds of 5 to 15 m/s"; "Magnitudes hold in this one simulated configuration, at 2 Hz without latency and under this recording policy." | 5, 10 and 15 m/s is in §III-A. |

## 2. Cuts for the caps

Nothing required is missing, and no pointer is wrong.

- §V-D terciles and drawn reaction time: both are in Table V (and the terciles in Supplement S6.1). See L5.
- §V-D per-rate rooms: Table V prints rooms and after-stop rooms for 2 Hz / 5 Hz, 0.1 s / 10 Hz, 0.1 s; the new sentence (173.4 at 2 Hz, 77.8 at 10 Hz with 0.1 s latency, "below half") agrees with it. The no-latency values (4.99, 4.75, 35.5) are now only in the supplement, which the pointer names.
- §V-D non-braking trade-off: "at a cost in caution (Table V)" agrees with Table V ((18.7, −0.9) and (1.7, −4.7)).
- §V-D filter tuning: Table V holds 238.1 / 153.0 and 0.753 / 0.816.
- §V-C non-braking paragraph: Supplement S9 holds the classifications. See L1.
- §V-B S11 sentence cut; §V-E "(Supplement S11; values in Supplement S14)": S11 is the margin-ratio check by scenario family, so the pointer is right.
- §VI, §I, §II cuts: nothing a later sentence depends on, except the weak antecedent in L2.
- S12 models sentence: the Acknowledgment names Opus 5.5, Sonnet 5.5 and Fable 5.2 with their roles and points to Supplement S12, which still holds the claim-audit paragraph.
- Letter: its quoted Results follow the new text; no quote of a cut sentence is left (grep of nine cut phrases: 0 hits).

## 3. Findings

### H
None.

### M

**M1. Abstract, "as did a plain time gap" reads as if the time gap also cost 0.16 s.** Table IV: the time gap removed the contacts with time lost −0.13 [−0.19, −0.06] s, that is, less time lost than the class average. The clause is the panel's own wording (R5), but placed after "for 0.16 s more time lost" it attaches the cost to the time gap as well, and it understates the point the panel wanted (a plain rule did as well, more cheaply).
- Fix (same word count, 250): move the clause before the cost: "the prediction removed the contacts, as did a plain time gap, for 0.16 s more time lost." If the author prefers no reordering, leave it: the reading "removed the contacts" is true for both.
- A reordering still leaves a little ambiguity; a clean version costs one word ("the prediction and a plain time gap removed the contacts, the prediction for 0.16 s more time lost" is +2), so it needs a cut elsewhere in the abstract.

### L (9)

- **L1.** §V-C: "Behind leads that do not brake hard (60 cases, lower level), the arms' classifications are descriptive (Supplement S9)." states no result. The old sentence carried one unfavourable class for the prediction (safer at a cost in time lost behind leads that stop and pull away). If words allow (+3 of the 19 spare): "Behind leads that do not brake hard (60 cases, lower level), the prediction is inconclusive or safer at a cost (Supplement S9; descriptive)."
- **L2.** §V-D filter tuning: "The mechanism persists under both" has a weaker antecedent now that §VI's sentence on the velocity lag is cut and the numbers moved to Table V. Word-neutral fix: "The after-stop room persists under both".
- **L3.** Contribution 2: "…, as its near-constancy led one to expect; the test adds the bound; an interacting-…" chains three semicolons. Word-neutral: "(as its near-constancy led one to expect; the test adds the bound)".
- **L4.** R10: paragraphs 1 and 4 of §V-E do not end with a plain sentence of what they show. No fix proposed under the caps.
- **L5.** §V-D: "(terciles: Supplement S6; a drawn reaction time: Table V)". The terciles are also in Table V, so "(terciles and a drawn reaction time: Table V)" is as accurate and saves one word.
- **L6.** Table S5, crossing placebo row: "The fresh crossing runs' own median ratio" became "The crossing runs' own median ratio"; S14 also has stored crossing runs (step 0), so "fresh" removed a distinction. Restore it if the one spare supplement word is free (see L7).
- **L7.** Table S5, new label row says "decided after the panel review" twice (first and third cell). Dropping one frees words for L6.
- **L8.** Table S5, mid-rank row: "ranks only the decisions with such rows" lost "only" and "as the later amendment states". The meaning survives through "the others take 0.5"; no fix needed.
- **L9.** Abstract: "in closed loop with dropouts (not caution-matched) it is equivalent" names no level; the equivalence is the lower (primary) level's, while the higher level's registered class is "safer at no extra cost" (Table S35). This is unchanged from the freeze apart from the dropped "to the class average", and §V-E and §VII give both levels. No fix possible at 250 words without a cut.

## 4. New problems asked about in the brief

- Wrong number: none found in the changed lines (checked against Tables IV, V, S32–S36).
- Missing label: none.
- Claim beyond its rule: none; the changed lines weaken claims throughout.
- Leftover "confirmed" on an amendment test: none.
