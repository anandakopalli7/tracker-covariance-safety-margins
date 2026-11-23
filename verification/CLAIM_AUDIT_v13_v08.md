# Claim audit v08 (narrow delta audit, A10 §10.3): the two lines changed to fix G1

**Auditor:** Claude Fable 5.2 (`claude-fable-5-2`), a fresh agent. The writer is Claude Opus 5.5. Fable 5.2 also wrote the earlier claim audits (v07 among them), so this audit is independent of the writer but not of the verification chain.

**Written:** 21 Nov 2026 (computer clock). No file other than this one was changed. No web or external service was used. `gen\` and `build\` were not read.

**Scope (stop rule):** only line 9 (abstract) and line 236 (first paragraph of §VII) of `out\audit_v08_input\MANUSCRIPT_v13.md`. Nothing else was re-audited.

## 0. Inputs and method

- **Text:** `work\A_text\out\audit_v08_input\MANUSCRIPT_v13.md` against `work\A_text\out\freeze_v13_0407\MANUSCRIPT_v13.md`.
- **Diff (re-run by me):** exactly two changed lines, 9 and 236. No other difference. Within each line, exactly the three changes the writer describes, and they are the same in both lines:
  1. "The fixed-noise tracker's covariance varies less: at its own spread an oracle recovers only 0.01%" → "The fixed-noise covariance varies less: at its own spread an oracle recovers 0.01%";
  2. "the fixed-noise covariance is equivalent and the prediction" → "the fixed-noise covariance is equivalent (±0.10 contact share) and the prediction";
  3. "at 10 Hz and 0.1 s latency the after-stop room" → "at 10 Hz and 0.1 s the after-stop room".
- **Word count** (whitespace tokens, the project's counter): abstract 220 of 220 (−3 + 3). §VII first paragraph 200 before and after, so the body count is unchanged.
- **G1:** `notes\CLAIM_AUDIT_v13_v07.md`, G1 and its Section 3. The change is v07's "if only G1 is taken" option, except that the writer cut "tracker's" where v07 proposed cutting "caution".
- **Rules:** `AMENDMENT_10_v13.md` §2.7, §7.5 (classification and E-H1 to E-H3), §9.
- **Values:** `A_EXPORT_E.json`, `A_EXPORT_B.json`, `A_EXPORT_C.json`; Table IV and its caption (l. 165 ff.).

**Result in one line:** G1 is resolved; no wrong number; 0 high, 0 medium, 3 low.

## 1. Does the new closed-loop sentence resolve G1?

**Yes.**

> "In closed loop behind braking leads (lower caution level), the fixed-noise covariance is equivalent (±0.10 contact share) and the prediction is safer at no extra cost (0.16 s lost), as is the time gap (descriptive)."

- G1 was that the closed-loop "is equivalent" carried no margin, so the only margin a reader could attach was the open-loop "within 5% of the room" one sentence earlier. The closed-loop claim now carries its own margin in its own unit, so the two cannot be merged.
- **Is "(±0.10 contact share)" correct?** Yes, for the contact part of the rule. A10 §7.5: "'equivalent': contact difference within (−0.10, 0.10), and time lost within (−0.5, 0.5) s". E-H2 is "N against F0 at lo", reported as "its classification". The export: `EH2` = "equivalent"; `E3.N.lo.dc` = −0.0167, `E3.N.lo.dc.ci` = [−0.0763, 0.0397], inside ±0.10; F0's contact share at the lower level is 0.20 (`E3.F0.lo.contact`), N's 0.183. Table IV's row agrees ("−0.02 [−0.08, 0.04] … equivalent").
- **The omitted ±0.5 s bound.** The rule has two conditions and the abstract names one. This does not mislead: the time-lost interval is `E3.N.lo.dt.ci` = [−0.004, 0.037] s, more than ten times inside ±0.5 s, so the classification does not turn on that bound; the contact bound is the binding one (the interval reaches −0.076 of −0.10). The body's own sentence (§V-C, l. 161) uses the same short form ("equivalent to the class average within ±0.10 of contact share") and gives the time lost beside it, and Table IV's caption states both bounds. §9 requires only the classification ("If E-H2 is 'equivalent', the abstract's null extends to closed loop"). Rated L (K1), no change needed.
- **§2.7** (δ = 0.05 of the room) is the open-loop margin only; the abstract keeps it on the open-loop sentence ("within 5% of the room"). The two margins now each sit with their own claim.

## 2. Is every number in the two lines right against its source?

**Yes.** All numbers of both lines (the lines are identical in their numbers):

| In the text | Source | Value | OK |
|---|---|---|---|
| 5.58 [4.99, 6.17] percentage points | `LB.R`, `LB.R.ci` (C) | 5.5792 [4.9889, 6.1673] | yes |
| ±5% band | A10 §2.2 (E5); `LB.H1` = "pass" | — | yes |
| an oracle recovers 0.01% | `B.CV.c` (B) | 0.0000744 = 0.0074% | yes (rounds to 0.01%) |
| [−0.09%, 0.15%] | `LB.RR_N.ci` (C), calibrated, level 0.994 | [−0.000931, 0.001477] | yes |
| within 5% of the room | A10 §2.7; `LB.H2` = "pass" | δ = 0.05 | yes |
| 99.7% of rows within 5% | `LB.IMM.within5` (C) | 0.99693 | yes |
| 4.6% of its room | `B.AQ.RR` (B) | 0.04594 | yes |
| 78% | `LB.RR_CK3` (C) | 0.7828 | yes |
| 92% | `LB.PS.rec` (C) | 0.9157 | yes |
| equivalent | `EH2` (E) | "equivalent" | yes |
| ±0.10 contact share | A10 §7.5; Table IV caption | (−0.10, 0.10) | yes |
| safer at no extra cost | `EH1` (E) | "safer at no extra cost" | yes |
| 0.16 s lost | `E3.CK3.lo.dt` (E) | 0.1632 [0.105, 0.225] | yes |
| as is the time gap (descriptive) | `E3.TG.lo.dc.ci` = [−0.318, −0.099], `E3.TG.lo.dt.ci` = [−0.193, −0.064]; caption: a test only for N, CK3 and the IMM at the lower level | upper ends < 0 and < 0.5 s | yes |
| (lower caution level) | `E3.CK3.hi.dc.ci` = [−0.137, 0.019] (inconclusive at the higher level) | the level is needed and stated | yes |
| 2 Hz, 10 Hz, 0.1 s, 45% | `B7.ratio_10_2` (C) = 0.4488 = `B7.10.0.1.as_room` 77.82 / `B7.2.0.as_room` 173.40 | 10 Hz with 0.1 s latency over 2 Hz without latency | yes |

Table IV's printed row values equal the E export to the printed digits for every lower-level row I compared (N, CK3, TG, PS, IMM).

## 3. Do the cuts change any meaning or break a §9 rule?

**No.**

- **"only" cut.** Removes an evaluative adverb; the value and the claim are unchanged. The "varies less: … recovers 0.01%" construction still carries the amplitude-limited reading (`B.CV.class` = "amplitude-limited", `LB.H3` = "amplitude_limited"). No rule touched.
- **"tracker's" cut.** "The fixed-noise covariance" stays unambiguous in context: the abstract's first sentence sets the subject ("Kalman-tracker covariances"), the next two sentences name the other two trackers by their noise handling ("An interacting-multiple-model tracker as tuned here", "an adaptive-noise filter"), and the 04:07 abstract already used the same short form in the closed-loop sentence ("the fixed-noise covariance is equivalent"), so the term is now uniform within the abstract. §9's requirement that the trackers tested be named (H3 row; "filter tuning (B3/B4 rule)") is still met. One residual reading risk is rated L (K2): on first meeting, "fixed-noise covariance" could be taken for a covariance that is itself fixed, which "varies less" then corrects in the same clause.
- **"latency" dropped.** §9 "Always": "Every magnitude carries its conditions: rate and latency (B7 rule)". The condition is still stated: the sentence reads "Magnitudes are at 2 Hz without latency; at 10 Hz and 0.1 s the after-stop room is 45% of its 2 Hz value", and the parallel "rate + latency" in the first clause makes "0.1 s" the latency in the second. The rule is kept. Residual risk rated L (K3): 0.1 s is also the period of 10 Hz (and the planner's replanning step, §III), so a reader who misses the parallel could take "0.1 s" as a restatement of the rate. The value (45%) is the 0.1 s latency value, so nothing is wrong; it is a clarity point only. This was v07's own proposed cut.

## 4. Anything else high or medium in these two lines?

**No.** No wrong value, no claim the data contradict, no A10 rule broken. Checked specifically:

- §9 "Always": the abstract still ends "Removing covariance margins is not justified." and §VII "The results do not justify removing a covariance margin from a deployed stack." (unchanged; S20 met).
- §9 E-H1 to E-H3 row: classifications stated as exported; the null is extended to closed loop only because `EH2` = "equivalent".
- Conditions carried: lead behaviour ("whose lead brakes to a stop", "behind braking leads", "leads that do not brake hard"), tuning ("as tuned here"), rate and latency (above), level ("lower caution level"), labels ("descriptive" twice).
- "confirmation" is not used; no old-run number is in the abstract.

## 5. Findings

Counts: **0 high, 0 medium, 3 low.** None requires a change before the freeze.

| # | Sev. | Where | Quote | Point | Word-neutral fix (optional) |
|---|---|---|---|---|---|
| K1 | L | Abstract l. 9; §VII l. 236 | "is equivalent (±0.10 contact share)" | The plan's equivalence rule has two bounds (contact difference within ±0.10 and time lost within ±0.5 s); the abstract names the contact bound only. Not misleading: the time-lost interval is [−0.004, 0.037] s, the contact bound is the binding one, and §V-C and Table IV's caption give both. Also, "±0.10 contact share" is an absolute difference in share (F0's share is 0.20, 60 cases); the abstract does not give that baseline, the body does | None needed. If wanted at 0 words: nothing shorter states both bounds; leave as is |
| K2 | L | Abstract l. 9; §VII l. 236 | "The fixed-noise covariance varies less" | First use of the short form without "tracker's"; could be read for an instant as a covariance that is fixed. The same clause ("varies less") and the neighbouring tracker names remove the doubt, and the form now matches the closed-loop sentence | None needed. Alternative at 0 words: restore "tracker's" and cut "caution" instead ("(lower level)"), which v07 offered; but "lower caution level" is the clearer of the two for an abstract reader, so the writer's choice is defensible |
| K3 | L | Abstract l. 9; §VII l. 236 | "at 10 Hz and 0.1 s the after-stop room is 45% of its 2 Hz value" | "0.1 s" reads as latency by parallel with "at 2 Hz without latency;", and §9's rate-and-latency condition is met, but 0.1 s is also the period of 10 Hz, so a hurried reader may take it for the rate restated | None needed. Alternative at 0 words: "at 10 Hz with 0.1 s the after-stop room" does not help; the only clear form costs +1 ("0.1 s latency"), which would need the "caution" cut of K2. Not both K2 and K3 can be taken at 220 words without a further cut |

## 6. Status of G1

**G1 (v07, medium): resolved** in both the abstract and §VII. By the stop rule, no further audit of this text is called for on my findings.
