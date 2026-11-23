Phase 1 file SHA-256 (`phase1\01_eic_journal_fit.md`): cc695cdf347f6e94a05aa5185208b2aed8527e3cfcf2f888c3c759c13a2f6eb6

# Phase 2: check of the earlier panel's required items R-1 to R-19 and Q7-1 to Q7-19, seat EIC (Journal-Fit Reviewer)

## Header

- **Seat and card:** EIC, Journal-Fit Reviewer, "Card 1: Journal-Fit Reviewer (internal role EIC)". **Model:** Claude Sonnet 5.5 (`claude-sonnet-5-5`).
- **Card-confirmation pause not held** (non-interactive run).
- **Order of work:** Phase 1 was written and hashed first (hash on line 1, re-checked at the end of this phase: unchanged). The earlier-items file `work\earlier_required_R1_R19_and_Q7.md` (SHA-256 13f24cd5ee3dae2eeddda3472e0bda371d0e3ed565185f71534a2f5e6fa211ce) was opened only afterwards. Phase 1 was not changed after that.
- **Package files, hashes at start and end (identical both times, and equal to the brief):**
  - `MANUSCRIPT_v13.md` 29125167b108bc27833c16e3b639cbb07af5f4c105c49d375deff3d5b4a951d0
  - `MANUSCRIPT_v13.tex` bd4d08d954d3595de2b5ac2653c18476c7bb3281e1c264604f995f018da01345
  - `SUPPLEMENT_v13.md` fab98c1fe24c8c5b95f86da8b1e664662401055232409a236d963938f5b99a09
  - `MANUSCRIPT_v13.pdf` 4fabfd9f611013fd4e7f60b8a59fcdcc2d782dbd3192a77c2efe54e77beb8299
  - `SUPPLEMENT_v13.pdf` a8ad36027dee70c8c48cf2b998cb2512b55ca568c400eb1ecd340923ddeb8b16
- **Pages viewed (all in Phase 1):** manuscript `page01.png` to `page13.png`; template `tpl01.png` to `tpl09.png`; supplement `sup01.png` to `sup03.png`.
- **Time:** 22 Nov 2026 18:49 (Get-Date).
- **Method note:** locations in the earlier file refer to a 12-page text; each item was found again in the 18:30 text (13 pages). The earlier file cites template line numbers from a different numbering (it cites 226, 424, 473); the correct lines in the 938-line official template are 195-197 (prefixes), 393-396 (sub-figure labels) and 463-467 (conclusion). I could not check reference existence or author counts (no web, by rule); those judgements rest on the text.

## Table A: R-1 to R-19

| ID | Verdict | Evidence from the 18:30 text (location) | What remains |
|---|---|---|---|
| R-1 | Resolved | V-E dropouts: "its factors (0.216, 0.107, and 0.065 for the first, second, and third missed update; 0.925 after reacquisition) are the median ratios of the covariance margin's critical scale to the class average's, relative to steady decisions, fitted on the 105 earlier runs"; "a level effect that needs no per-decision covariance"; "A second configuration, 10 Hz with 0.1 s latency (secondary), gave the same class and was not compared with a coast-count margin". VI repeats the factors. | Nothing. |
| R-2 | Resolved | V-E nuScenes paragraph: "For the IMM (secondary) ... 0.210 [0.158, 0.255] (99% interval) around misses and 0.093 [0.066, 0.116] over all pairs"; Table 6 last row; abstract: "the fixed-noise tracker's spread ranks the realized error weakly around missed detections and slightly inversely over all tracks". | Nothing. |
| R-3 | Partly resolved | V-E last dropout-share paragraph: "The dropout shares at start probability 0.10 and the two-noise share (2.8%, 3.0%, and 2.2%) are, as point values, inside the paper's ±5% equivalence margin ... At start probabilities 0.20 and 0.30 the dropout share is about 5% (Table 6)". Abstract: "(replicated; about 5% at higher rates)". VII: "it recovered a few percent of the room". | The "inside the ±5% margin as point values" statement is only in V-E; the abstract and VII do not carry it. At 0.20 and 0.30 the Table 6 point values (0.0525, 0.0514) sit on the margin, which "about 5%" covers. One clause in VII would close it. |
| R-4 | Resolved | V-E: "This share holds for the position–velocity interface (Section III-D) only; a wider interface was not tested." VI Limits: "so the two-noise IMM's share holds for that interface only (a wider interface was not tested) and is no verdict on maneuver-adaptive covariances." | Not in the abstract (my Phase 1 m11); the earlier item did not ask for it. |
| R-5 | Resolved | Abstract: "at equal caution against the realized future, with a constant-velocity prediction"; VI: "The room itself lies almost wholly in braking (Table 3: 1.63, 23.62, and 0.08 points before braking, during it, and after the stop)"; VI Limits: "whether a covariance adds anything on top of the braking prediction's path was not tested"; VII next steps: "a covariance added to a braking prediction's path". | Nothing. |
| R-6 | Resolved | IV-E: "The original lead-braking sequence, which is not Holm-adjusted, is room; detection in a ±5% band; ..." and "Within the second amendment, six primary hypotheses are Holm-adjusted (the H rows of Table 6): the dropout replication, the slope of the dropout share on the start probability, the two-noise IMM's class, the adaptive filter's twin replication, the closed loop with dropouts, and the nuScenes mechanism check". | Nothing. |
| R-7 | Resolved | Table 6: "new runs, share minus a fixed coast-count margin's ... failed, Holm 0.99"; "same cases, contacts at equal time lost ... failed, Holm 0.18"; caption: "Holm: Holm-adjusted one-sided p within the third amendment's two tests." V-E: "the third amendment's two fail under their own Holm adjustment as well (adjusted p 0.99 and 0.18; Table 6)". | Nothing. |
| R-8 | Resolved | Abstract: "Where it is nearly constant it adds nothing ... In three lead-braking tests where it varies, it recovers 2% to 5% of the room: 2.8% under random detection dropouts (replicated; about 5% at higher rates), 2.2% for a two-noise interacting-multiple-model tracker, and 4.6% for a noise-adaptive filter. A margin that only counts missed updates reproduces the dropout gain"; 245 words (whitespace count). VII is reorganised as "For a designer, three things follow" with a list of next steps rather than the abstract's sequence. | Two points from Phase 1 stay: 4.6% is a descriptive value among tests (J1), and VII still carries the same facts in other words (acceptable under template 463-467, which allows elaboration). |
| R-9 | Resolved | Abstract: "Plans were hash-locked internally; amendment tests followed the first results." Title unchanged. | Nothing. |
| R-10 | Resolved | V-E: "An exploratory decomposition (R² 0.47; decision-level R² 0.06; Supplement S15) attributes 54% of its explained variation to the update schedule, 38% to the geometry, and 8% to the realized error: by this exploratory reading it varies there mostly for other reasons." Abstract and VII no longer say "mostly for other reasons". | The method is still only in S15 (Phase 1 case C3). |
| R-11 | Resolved | ACKNOWLEDGMENT: "Generative AI was used and is disclosed here under IEEE policy."; "Claude (Anthropic; models Opus 5.5, Fable 5.2, and Sonnet 5.5) wrote the analysis ... and drafted and revised the text of all sections and of the supplementary material"; "the two sets share the scoring library, stored arrays, and resample draws (Section IV-E)"; "the presubmission review by an AI panel". | Provenance of "Fable 5.2 wrote the round-2 text" cannot be checked from the paper; the paragraph now says Claude models "drafted and revised the text of all sections", which does not understate. Recount scope still differs from S12 (Phase 1 m12). |
| R-12 | Partly resolved | IV-E: "The three amendments were written and locked on Nov. 21 and 22, 2026 (file times in Table S29), each after a report of an artificial intelligence (AI) review panel on the text before it, and the third's two controls were asked for by that panel (Table S5)." Ack: "The author conceived the study, set its questions and plans, made every scientific decision ... where the amendment files record a design choice as an AI session's, it was made within the author's approval." | IV-E part done. The Ack still says "made every scientific decision", the claim the earlier item asked to change to what the deposit supports (for example "approved its plans and design decisions"); the added qualifier softens it but does not replace it. Author must confirm which is true. |
| R-13 | Resolved | III-A: "In pedestrian crossing (first amendment; Section V-E), a pedestrian walks across the ego's lane from a drawn side at a drawn speed of 1 to 3 m/s, starting so that it would reach the ego's path together with an ego that keeps its desired speed, after a drawn 1 to 4 s; each case also carries an occluder flag ... The planner treats the pedestrian like any other actor, predicted at constant velocity. The study recorded 390 runs, 130 per desired speed, after a check on 51 stored runs (step 0) had shown little room". | Nothing. |
| R-14 | Resolved | III-B: "Time lost is the run's duration minus the distance traveled divided by the desired speed, for runs without contact; the rest gap is the gap to the stopped lead at the end of the run." | Nothing. |
| R-15 | Resolved | V-E: "a window starts with probability 0.10 (the primary start probability; on the new runs it masks 16.2% of updates)"; "the class average is computed under the same masks and output rule on the tuning runs (the dropout-estimated class average)". | Nothing. |
| R-16 | Resolved | V-E: "read by linear interpolation between scales 4 and 8 of its frontier at scales 4, 8, and 16 on the same cases, is 25.7% against the covariance arm's 20.7%; time lost is taken over the 89 of 135 cases without contact in any arm and lies between 25.24 and 25.84 s for the four arms (Table 6)". | Nothing. |
| R-17 | Resolved | Table 2 caption: "shares with 95% intervals, except N's share (99.4%, calibrated) and the IMM's share (99%, nominal)". | Nothing. |
| R-18 | Resolved | II: "With fixed noise and under regular updates, a Kalman filter's covariance settles to a steady state [26]. With intermittent observations it follows the arrival sequence instead ... [27]; the coast-count result of Section V-E is consistent with that dependence"; "Filters that account for data-association uncertainty [28] have a covariance that depends on the data"; "Collision-avoidance decisions have long been computed from uncertain state estimates [33] ... [35] ... [36]". | I cannot verify the added references offline; S13 says they were checked against Crossref by identifier and their abstracts read. Author gate. |
| R-19 | Partly resolved | See Table B: 11 of 19 Q7 items resolved, 4 partly, 4 not. | Open items: Q7-1 (multi-object, mid-rank), Q7-6 (conference locations), Q7-7 (et al.), Q7-13 (NIS, CANMOT), Q7-16, Q7-17, Q7-18, Q7-19 (advisory). Phase 1 adds the ACKNOWLEDGMENT order, Fig. 2 labels, "while", table footnote letters, as new misses. |

## Table B: Q7-1 to Q7-19 (the list R-19 refers to)

| ID | Verdict | Evidence from the 18:30 text or page image | What remains |
|---|---|---|---|
| Q7-1 | Partly resolved | Fixed: "nonbraking", "retuned", "Redetected" (V-D), "prestated" (V-E), "rescore", "presubmission". Still present: "multi-object" (abstract p.1; I p.1; II p.3), and "mid-rank" (IV-E p.5). Template 195-197. | Join "multiobject" and "midrank". |
| Q7-2 | Resolved | VII opens "For a designer, three things follow." and ends with next steps; it is not the abstract's sequence. Template 463-467 asks for elaboration, not a replica. | Nothing. |
| Q7-3 | Resolved | [26] "New York, NY, USA: Wiley, 2001, doi: ..."; [37] and [38] are now journal articles with volume, number, pages, month, year, DOI. | Nothing. |
| Q7-4 | Resolved | [39] "*Physica A*, vol. 360, no. 1, pp. 71–88, Jan. 2006, doi: 10.1016/j.physa.2005.05.001." | Nothing. |
| Q7-5 | Resolved | [40] has authors and "2018, arXiv:1708.06374v6."; [41] "IEEE Std 2846-2022, 2022, doi: ..."; [43] "Oct. 30, 2020."; [44] "Mar. 9, 2021." Month-first; no free-text tails. | Nothing. |
| Q7-6 | Partly resolved | Conference references are now uniform (no city and no month in any), e.g. "in *Proc. IEEE Intell. Veh. Symp. (IV)*, 2018, pp. 1171–1178". Template 722-723 includes City, State, Country. | Locations are absent for 15 conference references (Phase 1 o3); consistency fixed, template form not followed. Optional if DOIs stand. |
| Q7-7 | Not resolved (author check) | "et al." remains in [9], [13], [15], [21], [34] ([31] now lists all authors). Template 495. | Author must count authors (IEEE allows "et al." above six). I cannot check this offline. Phase 1 o2. |
| Q7-8 | Resolved | II: "IMM estimators [7], [8], [22]". | Nothing. |
| Q7-9 | Resolved | Fig. 4 (page 9): "(a)" and "(b)" are centered below each panel, plain type. | Nothing. |
| Q7-10 | Resolved | Fig. 2 right panel (page 7): both axes labeled ("Wrong goes (% of decisions)", "Caution (% of desired speed)") and the text "No wrong goes at any caution". | Fig. 2 still lacks (a) and (b) labels (Phase 1 m2, new). |
| Q7-11 | Resolved | Caption: "The IMM's share is measured against its own class average, F0 (IMM), drawn dashed." Legend: "F0 (IMM)" dashed, "IMM" solid. | Nothing. |
| Q7-12 | Resolved | "Generative AI was used and is disclosed here under IEEE policy." has a verb. | Nothing. |
| Q7-13 | Partly resolved | SHA-256: "hashes of the 256-bit Secure Hash Algorithm (SHA-256)". CARLA: "CARLA (Car Learning to Act) simulator" in I. Table 1 now stands on page 2 right after the Section I pointer, before F0, N, E are used. | CANMOT is not expanded in the body (it is a published name, [5]; I would not insist). New case: NIS is used in Table 1 (p.2) before III-D defines it (Phase 1 m6). |
| Q7-14 | Resolved | Page 11, Limits: "came from a track younger than / 1 s." breaks after "than"; "1 s" stays together. | Nothing. |
| Q7-15 | Resolved | V-E: "(lead braking, this mask law, and this output rule only)". | Nothing. |
| Q7-16 | Not resolved | Page 1: "Independent Researcher, Troy, MI, USA (ORCID: 0009-0002-5241-9922)". Template 24-27: "City, ST ZIP USA". | Form only: ZIP and the comma before USA. I would not press an independent researcher to print a home ZIP; the author may choose. |
| Q7-17 | Not resolved | Bold sentence-case run-in heads remain: II (p.3) "Perception judged by its effect on decisions." and three more; VI (pp.10-11) "Which commitment applies." and three more. | Phase 1 m4: title case or plain paragraphs. |
| Q7-18 | Not resolved (conditional; unnecessary) | Supplement headings in title case: "S1. Configuration", "S1.1. Planner Rows and Margin Projection" (sup01). | The supplement is not typeset in the journal template; I would not ask for capitals there. The earlier item was conditional and I judge it unnecessary. |
| Q7-19 | Partly resolved (advisory) | Drop cap present on page 1 ("A MULTI-OBJECT tracker"). No author biography. | Biography is optional at submission (brief); advisory only. |

## Counts

- **R-1 to R-19:** resolved 16, partly resolved 3 (R-3, R-12, R-19), not resolved 0.
- **Q7-1 to Q7-19 (inside R-19):** resolved 11, partly resolved 4 (Q7-1, Q7-6, Q7-13, Q7-19), not resolved 4 (Q7-7, Q7-16, Q7-17, Q7-18).

## Where an earlier item asked for something wrong or unnecessary

- Q7-18 (supplement headings in capitals): unnecessary; the supplement is a separate document.
- Q7-16 (ZIP in the affiliation): form-only; do not require a private address.
- Q7-13 (expand CANMOT): unnecessary; it is a name, expanded in [5].
- Q7-7 ("et al."): cannot be decided without author counts; IEEE allows it beyond six authors, so it may not be a miss at all.
- R-8 and Q7-2 cite "template line 473" for the conclusion rule; that line is not the conclusion text in the 938-line official template (463-467 is). The rule is a mild preference ("do not replicate the abstract as the conclusion"), met here.
- R-18 asked the author to add references the earlier panel itself called unverified; adding references that the author has checked is right, and S13 says that was done.

## Noted after Phase 1 (Phase 1 left unchanged)

1. **Affiliation form** (Q7-16): ZIP and comma form differ from template 24-27; my Phase 1 Q7 answer called the first page fine. It is a form-only advisory, not a REQUIRED item.
2. **Supplement headings** (Q7-18): title case; advisory, conditional.
3. **R-12 and my m13:** the earlier panel and I flagged the same Ack sentence ("made every scientific decision") from different directions; no new fact.
4. **R-3:** the earlier panel wanted the "inside the ±5% margin as point values" clause in the abstract and VII; Phase 1 asked for status tags in the abstract (J1) but did not name this clause. Not a new finding, a refinement of J1.
5. No earlier item changes my recommendation (major revision) or score (5.8 / 10; 2.9 stars).

## Phase 1 hash at end of Phase 2

`phase1\01_eic_journal_fit.md` SHA-256 re-computed after writing this file: cc695cdf347f6e94a05aa5185208b2aed8527e3cfcf2f888c3c759c13a2f6eb6 (unchanged).
