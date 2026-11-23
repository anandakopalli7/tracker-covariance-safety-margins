# Final v13 panel, seat R1: Peer Reviewer 1 (Methodology)

- **Seat:** R1, Peer Reviewer 1 (Methodology). One seat only; no sub-agents, no other seats, no synthesis.
- **Model:** Claude Fable 5.2 (`claude-fable-5-2`). The launch message says the final text was written by the same model, so this report reads it with deliberate skepticism; agreement between this seat and the text is not independent evidence.
- **Card:** "Card 2: Peer Reviewer 1 (Methodology)" of `review_v13_output\00_phase0_field_analysis_and_cards.md` (identity unchanged: applied statistician and simulation-evaluation methodologist). Focus anchors re-pointed to the sections named in the brief: Section I (contributions, self-containment sentence), IV-E, V-B, V-C, V-D (Table 5, Fig. 4), V-E (Table 6), VI, VII, ACKNOWLEDGMENT, references; the supplement only where a main-text pointer leads.
- **Card-confirmation pause not held** (non-interactive run).
- **Criteria binding:** none supplied (`criteria_binding_unavailable`); no venue-alignment claim beyond the rules stated in the brief. `NOT_CALIBRATED`.
- **Files and SHA-256 at start (22 Nov 2026) and at end: identical, and equal to the brief's values.**
  - `MANUSCRIPT_v13.md` b469bf657af9ddee583b7bda944ca3af639e1ba4b2e61875150d83bafd0f7793
  - `MANUSCRIPT_v13.tex` dd915933edffcebad863c9d1ed02b37ef0a6a493045696b210ff9c94b4dc2eee
  - `SUPPLEMENT_v13.md` d1ea32fa94787a0eb44c441714ac8c9183d3ab9707c25336194673170515f9b8
  - `MANUSCRIPT_v13.pdf` d3fec633f7b5ab7d4d9053c2b9a56e23dbd6d5ef9c90455cd477701c0920bcf5
- **Read:** the manuscript `.md` in full; the `.tex` for front matter, floats and captions; the supplement sections S2, S3 (Tables S4, S5 by row), S5 (Table S9), S6, S8, S9, S12, S14, S15; `BUILD_REPORT_v13.md`; `RECOUNT_COVERAGE_v13.md` (seat extra read); `AMENDMENT_13` in full and `AMENDMENT_12` sections 0, 1, 3a, 4, 5 (head); lock files A11, A12a, A12e, A13a, A13b, A13c (heads) and all lock file times; the export pairs DR2, DR10, M, N5B, DRF, YN, B (and B12X in the same folder for the mode probabilities), E5, E6; both Holm files.
- **Pages viewed (PNG):** 1, 7, 8, 9, 10. Not viewed: 2 to 6, 11, 12 (layout statements below cover the viewed pages only). Figures viewed: Fig. 3, Fig. 4.
- **Not read:** the response letter, earlier reviews, other seats' files, session notes, diff files, `DERIVED`/`OUTCOMES`/`TEXT_FREEZE`, anything named `<excluded folder 1>` or `<excluded folder 2>`. No web access. Nothing in `revision_v13\` was changed.

## Value check against the exports (seat task 3)

**166 printed values checked against first-program exports; 166 match at the printed precision. 0 mismatches.** For every export pair read, the second-program file agrees with the first on every shared key (counts exact, values within 1e-9): DR2 174 keys, DR10 113, M 79, N5B 45, DRF 46, YN 52, B 364, E5 52, E6 70; 0 disagreements.

| Block | Values | Source | Second program |
|---|---|---|---|
| Table 3, all seven rows (within 5%, r and interval, c and interval, three rooms, lag, CK3) | 70 | `A_EXPORT_B` | agrees |
| Table 5 (Section V-D): 0.101 [0.068, 0.134]; terciles 0.072 / 0.168 / 0.055; 0.334 [0.279, 0.383]; 6%; after-stop room 173.4 / 238.1 / 153.0; CK3 0.783 / 0.753 / 0.816; tuning 1.16, 0.379, 0.0000; fresh 5.58 | 18 | `A_EXPORT_B` (LB.*, TU.*, B.*) | agrees |
| Section V-A and Table 2: room 5.58 [4.99, 6.17]; about 1,204; 21,574; CK3 0.783 [0.720, 0.842] | 6 | `A_EXPORT_B` | agrees |
| Dropouts on new runs, dose rows and trend (Table 6, V-E): 5.21 [4.76, 5.66]; 0.0298 [0.0077, 0.0518]; slope 0.152 [0.032, 0.267]; 0.0139 [−0.0017, 0.0306]; 0.0525 [0.0287, 0.0745]; 0.0514 [0.0268, 0.0750]; 0.021 [0.005, 0.036]; 0.009 [−0.008, 0.024]; abstract 3.0% | 17 | `A_EXPORT_DR2` | agrees |
| Coast-count row: −0.0024 [−0.0057, −0.0001] | 2 | `A_EXPORT_DRF` | agrees |
| 10 Hz: 0.0321 [0.0087, 0.0553]; 0.035 [0.014, 0.054] | 4 | `A_EXPORT_DR10` | agrees |
| Two-noise IMM: 4.95 [4.53, 5.33]; 0.0220 [0.0185, 0.0253]; 0.0131 [0.0108, 0.0158]; abstract 2.2%; mode probability 0.18, 0.48 | 9 | `A_EXPORT_B`, `A_EXPORT_B12X` | agrees |
| Adaptive filter on new runs: 0.0508 [0.0449, 0.0567] | 2 | `A_EXPORT_YN` | agrees |
| Closed loop with dropouts: −0.12 [−0.18, −0.05]; 0.18 [0.11, 0.26]; 0.98 [0.60, 1.39]; 18.2% / 18.4%; 21% / 33%; 17% of 30; 135 cases | 12 | `A_EXPORT_E5` | agrees |
| Equal-time-lost rows: −0.05 [−0.12, 0.02]; 20.7%, 25.42; 32.6%, 25.24; 24.4%, 25.45; 11.1%, 25.84 | 10 | `A_EXPORT_E6` | agrees |
| nuScenes mechanism: 0.108 [0.039, 0.172]; −0.038 [−0.070, −0.006]; 5.21 m, 2.45 m; 150; abstract 0.11 [0.04, 0.17] | 8 | `A_EXPORT_M` | agrees |
| nuScenes decision test under dropouts: −0.01 [−0.08, 0.12] | 2 | `A_EXPORT_N5B` | agrees |
| Holm values in Table 6: 0.0079 (two rows), 0.0003 (four rows) | 6 | `A12_HOLM_v01.json` | file records both programs' hashes |

**Values the submission pass moved into the main text, one by one:**

- **Table 5, rows sourced from B** (commitment, filter tuning, tuning-run and fresh-run recording-policy values): match; agreeing second-program recount; none one-program.
- **Table 5, update-rate rows** (5.58 / 5.31 / 5.07; 173.4 / 115.2 / 77.8; 0.0000 [−0.0004, 0.0006]) **and non-braking rows** (twelve values): their exports (C, D) are outside this seat's allowed reads. They match Supplement Tables S16 and S19 exactly (19 of 19), which carry no ‡ mark, and the coverage file states that all main-text values have an agreeing second program. Not verified by me against an export.
- **Table 5, old-evaluation values** (5.51, 0.837, −0.0004): not in my allowed exports; the coverage file says their second program is "the stored-run recount". Not verified by me.
- **Fig. 4:** the points that Table 5 prints agree with the figure by eye. The other plotted points (2 Hz with 0.1 s; 0 s and 0.2 s latencies; reaction times 0.5, 1.0, 1.25, 1.5, 1.8 s) are printed only in Tables S14 and S16, unmarked there (so recounted by the supplement's rule).
- **Fig. 3:** its ten points agree by eye with Table 4. Table 4's export (E) is outside my reads.
- **Dose trend, coast-count row, equal-time-lost rows (V-E and Table 6):** match; agreeing second-program recount (DR2, DRF, E6); none one-program.
- **No value in the main text is marked one-program,** which agrees with Section IV-E.

**Recount-scope sentence (IV-E)** against `RECOUNT_COVERAGE_v13.md`: the file reports 323 of 323 (named passages) and 325 of 325 (whole main text) with an agreeing second program, and 164 supplement result values without one, each marked ‡. The sentence "recount every value printed in the main text and all but the marked (‡) values of the supplement" matches that record. See finding F14 on the record's stale labels.

**Pre-registration claims checked against locks:** every lock's file time precedes its export (A12a 00:47 before B 02:33, DR2 05:11, YN 06:17; A12b 01:44 before E5 03:29; A12c 03:35 before M 03:41; A12d 03:21 before DR10 05:44; A12e 03:37 before N5B 05:20; A13a 06:49 before E6 09:01; A13c 06:48 before DRF 07:04). The six Holm hypotheses were named in A12 section 4 under LOCK_A12a. The mechanism check's primary population was changed on the training split before LOCK_A12c, as the paper says. The coast-count baseline replaced a two-population baseline between LOCK_A13b and LOCK_A13c after code tests on 35 old runs only; the supplement says so. All times are one laptop's clock, as the paper states.

## Findings

| ID | Location | Finding | Severity | Evidence (quoted) | Fix in the fewest words |
|---|---|---|---|---|---|
| F1 | V-E (p. 8); VI "What a varying covariance needs"; Abstract; VII | The coast-count margin is built from the covariance itself: its four factors are the covariance margin's median ratio to the class average per coast count, fitted on the first amendment's 105 runs. The main text does not say this, and says the gain "needs no covariance". With fixed noise and every track kept through every mask, the covariance while coasting is almost a function of the coast count alone, so this control could hardly come out otherwise. What it shows: per-decision covariance adds nothing beyond a coast-count table learned from the covariance. | MAJOR | "a level effect that needs no covariance"; supplement only: "Each factor is the median ratio of the covariance margin's critical scale to the class average's ... fitted on the first amendment's 105 fresh runs" | Add to V-E: "its factors (0.216, 0.107, 0.065; 0.925 after re-acquisition) are the covariance margin's medians per missed-update count, fitted on the 105 earlier runs". Replace "needs no covariance" with "needs no online covariance: a table by missed-update count does as well". |
| F2 | V-E last paragraph; Abstract; VII; Table 6 | The mechanism check reports only the fixed-noise tracker. The registered secondary, the IMM, is positive around misses and positive over all pairs, the opposite sign. It is in Table S45 only. The abstract's "its spread ... slightly inversely over all tracks" reads as a statement about tracker covariances. Leaving out the result that favours a covariance, in a paper whose thesis is that covariances rarely help, is a balance problem. | MAJOR | Main: "over all pairs it is slightly negative". Table S45: IMM "0.210 [0.158, 0.255]" around misses, "0.093 [0.066, 0.116]" all pairs | Add one clause to V-E and one to Table 6: "the IMM (secondary): 0.210 [0.158, 0.255]; all pairs 0.093 [0.066, 0.116]". In the abstract and VII say "the fixed-noise tracker's spread". |
| F3 | V-C; Table 4; VII | Unequal standard. The covariance arm's +0.18 s under dropouts is treated as a possible wider margin and tested at equal time lost. The braking prediction's +0.16 s [0.10, 0.22] is labelled "safer, no extra cost" with no such check. The check exists in the supplement and favours the braking prediction (0% at 24.78 s against the class average's 5% at 24.89 s at the higher level), but a main-text reader cannot see it. | MINOR | "the braking prediction is safer at no extra cost (the plan's class: time lost below 0.5 s)"; Table S23 rows F0 higher 5%, 24.89; CK3 lower 0%, 24.78 | Add to V-C: "the class average at its higher level still made contact in 5% for more time lost (24.89 s against 24.78 s; unpaired, descriptive)". |
| F4 | VII; V-E; Abstract | Size. VII says the dropout and two-noise shares "both lie inside the ±5% margin" and drops "as point values". The replication's interval reaches 0.0518, and at start probabilities 0.20 and 0.30 the point shares are 0.0525 and 0.0514, above the margin (Table 6). "Small by that margin" holds at the registered rate only. | MINOR | VII: "both lie inside the ±5% margin"; Table 6: "0.0525 [0.0287, 0.0745]; 0.0514 [0.0268, 0.0750]" | VII: "both point values lie inside the ±5% margin at the registered dropout rate; at two and three times that rate the share is about 5%". |
| F5 | Abstract; V-E; VII | "Recovers slightly more" is a reverse-direction reading of a one-sided superiority test that failed. Its interval is a plain, uncalibrated 95% percentile interval whose upper end is −0.0001. True of the point values (0.0322 against 0.0298); weak as an inferential claim. | MINOR | "difference −0.0024 [−0.0057, −0.0001]"; A13 3.4: "A10 §2.6 calibration is not applied" | "recovers as much (0.032 against 0.030)". Note in Table 6 that this interval is uncalibrated. |
| F6 | Table 2; Abstract; IV-D | The level of the headline interval is not in the main text. [−0.0009, 0.0015] is a calibrated 99.4% interval and the IMM's a nominal 99% fallback; Table 2's caption sends the reader to the supplement. (The direction is conservative.) | MINOR | Table 2 caption: "shares with intervals at the levels of Supplement S5"; Table S9: "N's share 99.4% calibrated" | Add to Table 2's caption: "95% except N's share (calibrated 99.4%) and the IMM's share (99%)". |
| F7 | V-E (p. 9); Table 6 | The equal-time-lost comparison leaves out three facts a reader needs: linear interpolation between scales 4 and 8; the class average's interpolated contact share (25.7%); time lost over 89 of 135 cases. | MINOR | "read from the class average's frontier at scales 4, 8, and 16"; S15: "read by linear interpolation between the two scales around it (bracketed 4-8): 25.7%" | "by linear interpolation between scales 4 and 8 (25.7% against 20.7%; time lost over the 89 cases without contact in any arm)". |
| F8 | V-E; VI Limits | "This share is a lower bound" is an inference, not a result: no test shows that passing acceleration terms or a constant-acceleration prediction would raise the share. V-E and VI also word it differently ("a lower bound" / "a lower bound for that interface"). | MINOR | "Through the position–velocity interface (Section III-D) this share is a lower bound." | "this share holds for that interface only; a fuller interface was not tested". |
| F9 | V-B; Table 3 | The prose says the re-tuned IMM "still barely varies" and stops. Table 3 shows its share's interval excludes zero and its share exceeds its oracle's: by Section IV-C's rule it would class as "recovers" (the export says so). A reader of the prose alone gets a null. | MINOR | "A re-tuned IMM ... still barely varies"; Table 3: "0.0055 [0.0040, 0.0067]" | Add: "its share is 0.0055 [0.0040, 0.0067], above zero (descriptive)". |
| F10 | V-D; Fig. 4(a) | The update-rate sentence compares 2 Hz without latency with 10 Hz at 0.1 s and attributes the fall to "the 2 Hz update". Fig. 4(a), now in the main text, shows latency moves the after-stop room as much as the rate does (10 Hz: 35.5 at 0 s, 130.5 at 0.2 s; 2 Hz at 0.1 s: 227.1). | MINOR | "so it is largely a consequence of the 2 Hz update" | "a consequence of the age of the track state (update interval plus latency)". |
| F11 | Abstract; VI; VII | "Varies mostly for other reasons" rests on an exploratory regression that explains 47% of the variance; the abstract and VII state it without "exploratory". | MINOR | V-E: "An exploratory decomposition (R² 0.47 ...) attributes 8% of its explained variation" | VII: "where an exploratory decomposition attributes most of its explained variation to other causes". Give the other two shares (54%, 38%) in V-E. |
| F12 | V-C; Table 4; Table 6; VI Limits | Time lost is averaged over pairs or cases without contact, a set chosen by an outcome the arm changes (89 of 135 in the frontier test). The comparison is therefore not between randomized-equivalent sets. Unavoidable in part; not named as a limit. | MINOR | Table 6 caption: "mean time lost over the cases without contact in any of the four" | One sentence in Limits naming the conditioning. |
| F13 | ACKNOWLEDGMENT, AI paragraph | (i) "the second programs that recount every printed value" contradicts IV-E (164 marked supplement values have no agreeing second program). (ii) "(Supplement S12)" is given as the source of the model record, but S12 names no model. (iii) "which Claude Fable 5.2 revised for the second amendment": if the same model also wrote the third amendment's text and the submission pass, as this seat's launch message says, the sentence understates. | MINOR | "wrote the second programs that recount every printed value" against IV-E "all but the marked (‡) values of the supplement" | "recount every value printed in the main text"; "revised for the later amendments and the submission"; drop or correct the S12 pointer. |
| F14 | `RECOUNT_COVERAGE_v13.md` (the record behind IV-E) | The record's passage list is stale: it names "Tables II-V", gives no line for the present Table 5, and lists the amendment table (present Table 6) as "TABLE V". The totals are plausible (Table 5 sits inside Section V's 375 placeholders), but the audit trail for the table just moved into the main text cannot be read off the record. | MINOR | "Named passages: Abstract, Sections I and V-VII, Tables II-V, figure captions" | Regenerate the record with the frozen table numbers and one line per table. |
| F15 | V-E first paragraph; Table 6 | The registered dropout rate is not stated in the main text. A reader cannot tell that the 2.8% and 3.0% belong to start probability 0.10, or that this masks about 16% of updates, except by matching numbers across Table 6 rows. | MINOR | "detections removed for one to three updates by random, truth-independent masks" | Add "(start probability 0.10 per update; 16% to 17% of updates masked)". |
| F16 | Table 6 (p. 10) | Thirteen rows with up to four semicolon-separated values and intervals per cell; the row "slope of that share on the dropout rate" uses another name for the start probability. Hard to audit a claim against. | MINOR | "0.0139 [−0.0017, 0.0306]; 0.0298 [0.0077, 0.0518]; 0.0525 ..." in one cell | One quantity per column for the dose rows; "start probability" throughout. |
| F17 | Table 2 "(C)" on the IMM row; V-B | "Confirmed" is attached to a classification hypothesis that passes unless the class is "inconclusive" (Table S4). The label is formally right, but "(confirmed)" after "inside ±0.05" reads as a confirmed equivalence. | MINOR | V-B: "recovers only 0.0009 [0.0006, 0.0010] of its own room, inside ±0.05 (confirmed)" | "(classification confirmed: amplitude-limited)". |
| F18 | V-A; IV-C | The equivalence margin (5% of the room) is wider than the whole share of the perfect ±5% ranking oracle (1.3%). The data are stronger than the margin: the covariance's interval, upper end 0.0015, lies below that oracle's lower end, 0.010. The paper does not say so. | MINOR | "0.013 [0.010, 0.015]"; "0.0000 [−0.0009, 0.0015]" | Add: "its interval also lies below the ±5% oracle's". |
| F19 | References [26], [39] | [26] has no place of publication; [39] has no year or access date. | MINOR | "[26] ... Wiley, 2001"; "[39] UNECE, ... E/ECE/TRANS/505/Rev.3/Add.151." | Add "Hoboken, NJ, USA:" and a year or "Accessed:" date. |
| F20 | Pages 7 to 10 | Float order: Fig. 3 (p. 7) comes before Table 4 (p. 8), and both a page or more after Section V-C's text; Table 6 lands on p. 10 inside Section VI. | MINOR | Page images 7, 8, 10 | Move Table 4 before Fig. 3; place Table 6 on the page of V-E if the class allows. |

No CRITICAL finding. I found no printed value that disagrees with its export, no label that claims "confirmed" for an amendment test, and no lock later than its data.

## Answers

### 1. Labels and sizes

Labels are right throughout. "Confirmed" appears only for the original plan's sequence. Amendment tests carry "(A)", "replicated", "failed" or "secondary", and the caption of Table 6 defines them. Holm stands beside the labels and changes none: I recomputed both families from the files (six second-amendment primaries: 0.0079, 0.0079, 0.0003 four times; two third-amendment controls: 0.18 and 0.99, both not rejected), and the printed values match.

Sizes are right where printed, with two soft spots: the Conclusion drops "as point values" and is silent that the share is about 5% at higher dropout rates (F4); and "recovers slightly more" turns a failed one-sided test into a claim (F5). The level of the headline interval is in the supplement only (F6). "Confirmed" on a classification that can fail only by being inconclusive is formally right but easy to misread (F17).

### 2. Overreach

- **Dropout gain's source:** mostly sound ("matched by a coasting margin, a level effect"), but "needs no covariance" goes past the test, because the coast-count factors were fitted from the covariance, and the test could hardly fail under fixed noise (F1).
- **Closed loop:** sound. "Matched in open-loop caution", "might come from a wider margin", "at equal time lost fewer contacts were not shown" are each within their test. "Not shown" is not turned into "no difference". The braking prediction is held to a looser standard than the covariance (F3).
- **nuScenes mechanism check:** the training-split choice of the primary population and the level effect are both stated. The overreach is by omission: the IMM's opposite sign is left in the supplement (F2).
- **Real-log decision test:** sound; "no room, so nothing was tested".
- **Two-noise IMM:** the interface limit is stated twice; "lower bound" is an untested inference (F8).
- **Other:** "varies mostly for other reasons" is exploratory and should say so wherever it appears (F11); the update-rate attribution mixes rate and latency (F10).

### 3. Earlier limits

| Limit | Status | What remains |
|---|---|---|
| (a) Closed loop matched only in open-loop caution | Addressed | The equal-time-lost test was run and failed, and the text says so in the abstract, V-E and VII. Remaining: interpolation and the 89-case set are supplement-only (F7); one covariance point; conditioning on no contact (F12). |
| (b) Dropout gain perhaps only a coasting margin | Addressed, with one wording gap | The control was run and the covariance did not beat it. Remaining: how the control was built, and "needs no covariance" (F1). |
| (c) Abstract and conclusion stronger than the body | Mostly addressed | "In these tests", "rarely", "weakly", "not shown" now match the body. Remaining: F2, F4, F5, F11. |
| (d) Two-noise IMM's interface | Addressed as a limit | Stated in III-D, V-E, VI. "Lower bound" should go (F8). |
| (e) Scope of Holm and of the recount | Addressed | Both scopes are stated in IV-E and V-E and match the files. Remaining: the Acknowledgment's wider recount wording (F13); the stale coverage record (F14). |
| (f) Density; round-2 results only in the supplement | Partly addressed | The results are now in the main text (Tables 5, 6; Figs. 3, 4). The cost is Table 6's density (F16) and 898 words in V-E. |
| Confirmed result that could hardly fail | Not addressable by wording; stated honestly | VI says the equivalence "was expected from this constancy". The coast-count control is a second result of the same kind (F1). |
| Small positive effects | Stated | See F4 for the one place the size is under-described. |
| One simulator and configuration | Stated | The 10 Hz dropout check is one secondary configuration. |
| No decision-level real-log evidence | Stated | Two real-log decision tests found no room. |
| Process (amendments after results, local hash locks, AI authorship) | Stated | Lock order holds on the laptop's clock; no third-party timestamp. Six of 21 after-the-fact departures touch a confirmatory result; one changed values (the real-log clearance). |

### 4. Readability

The abstract gives the bottom line first. Coined terms are defined once in Table 1 and Section IV. Each claim's evidence can be found in the main text, with the exceptions listed under Q6. Three things slow a reader: Table 6 (F16); the word "mechanism" in V-D's "The mechanism persists" has no stated referent in the main text; and the registered dropout rate must be inferred (F15).

### 5. Verdict

- **Recommendation (methodology seat): minor revision.** Every fix above is a sentence or a table cell; no analysis needs re-running, and no number is wrong.
- **Score: 6.6 / 10; 3.5 stars of 5.** The inference is careful and honestly labelled, and the record is unusually checkable. The score is held down by what wording cannot fix: the confirmed result and the coast-count control could hardly fail; the positive effects are 2% to 5% of a room and partly level effects; one simulator; amendments chosen after results; locks on one laptop's clock; no real-log decision evidence.
- **Most likely editorial outcome at IEEE OJ-ITS: major revision,** with a real chance of rejection on significance (a null in one simulated configuration) or on the extent of AI authorship, rather than on method.
- **The single change that would raise my score most:** a decision-level test on data with room where the covariance varies (real logs or a second simulator and planner), locked with a third-party timestamp. Within the text alone: F1 and F2 together.

### 6. Self-contained main text

Eight cases where a main-text claim needs a method step, definition or value that is only in the supplement:

| # | Main-text location | Supplement item it rests on | Fact to bring in |
|---|---|---|---|
| 1 | V-E (coast-count margin); Abstract; VI; VII | S15, "A fixed coast-count margin" | The factors (0.216, 0.107, 0.065; 0.925 after re-acquisition) are the covariance margin's median ratios per missed-update count, fitted on the first amendment's 105 runs. |
| 2 | V-E (equal time lost); Table 6; Abstract | S15, "The class average at larger scales"; Table S44 | Linear interpolation between scales 4 and 8; the class average's interpolated contact share 25.7%; time lost over 89 of the 135 cases. |
| 3 | Table 2; Abstract (the interval [−0.09%, 0.15%]) | Table S9 | The interval's level: calibrated 99.4% for the covariance's share; 99% for the IMM's. |
| 4 | V-E (mechanism check); Abstract; VII | Table S45 | The IMM's registered secondary result: 0.210 [0.158, 0.255] around misses and 0.093 [0.066, 0.116] over all pairs. |
| 5 | V-E (pedestrian crossing); Abstract "varies mostly for other reasons" | S15, Table S46 | What the decomposition is (a regression of the log margin ratio on three groups, Shapley shares) and the other two shares: update schedule 54%, geometry 38%. |
| 6 | V-C and Table 4 ("safer, no extra cost" for the braking prediction) | Table S23 | The class average's time lost at each level (24.52 s and 24.89 s) beside the braking prediction's 24.78 s, which makes the equal-time reading possible. |
| 7 | V-B ("By the plan's flag its covariance barely varies") | S2, amplitude-matched oracles | The flag's rule: at least 95% of binding rows within 5% of the median ratio. |
| 8 | V-E (dropouts); Table 6 | S15 (Table S39); Table S34 | The registered start probability (0.10) and the share of updates masked (16% to 17%). |

Not cases (pointers that only offer more detail): the calibration procedure, the phase thresholds, the first amendment's closed loop with dropouts, the post hoc Bonferroni check, the two-noise IMM's r − c interval (Table 6 already shows non-overlapping intervals).

The sentence after Scope, "The main text holds every result on which the claims rest", is nearly true for results; it is not yet true for the method steps in cases 1, 2 and 7 or the values in cases 3, 4 and 8.

### 7. IEEE OJ-ITS format and declarations (from this seat; pages 1, 7 to 10 and the `.md`/`.tex`)

Checked and found in order: headings in capitals; "Fig. N" in text and "FIGURE N." in captions; Arabic table numbers; "Fig. S"/"Table S" in the supplement pointers; American spelling, serial comma, no contractions, one spelling of "preregistered", period inside the closing quotation mark (IV-E); funding in the template's first-page note and no Funding heading; one ACKNOWLEDGMENT in the required order; author, affiliation, ORCID, corresponding author with email; running head with a short title (p. 8, 10); abstract 250 words by the build counter and by a whitespace count, no abbreviations; five index terms; [10] names no journal; arXiv items in the "year, arXiv:ID." form; [4] has "Accessed:".

Misses (3 cases):

1. **Reference [26]:** no place of publication before the publisher (F19).
2. **Reference [39]:** no year and no access date (F19).
3. **Float order, pages 7, 8, 10:** Fig. 3 before Table 4; Table 6 inside Section VI (F20).

A risk, not a miss: the abstract is at exactly 250 words, so a counter that splits "[−0.09%, 0.15%]" or "interacting-multiple-model" differently will read it as over. Two gates remain as placeholders in the ACKNOWLEDGMENT (repository DOI; author confirmation), as the brief says. References on pages 11 and 12 were checked in the `.md` only, not as typeset.

### 8. AI disclosure

**Does (a), as frozen, meet IEEE's rule?** Yes in form: it names the system (Claude, Anthropic, three models; OpenAI Codex), the sections (Abstract, Sections I to VII, the Supplementary Material; the code) and the level (carried out the searches, wrote and ran the code, drafted the text). Its factual problems are in F13: "recount every printed value" is wider than IV-E; the S12 pointer does not hold a model record; "revised for the second amendment" may understate the later revision.

**Would an editor desk-reject on it?** The risk comes from the extent of use, which no honest wording removes: all text and all analysis code are AI-generated, and review was by an AI panel. Version (a) raises that risk a little by opening with "Content generated by artificial intelligence" and listing model-by-model roles before any statement of what the author did.

**Which version lowers the risk without understating the use: (b), with three changes.**

- (b) is accurate where (a) is not: "recounted every value printed in the main text" matches IV-E and the coverage record (325 of 325), and "had not seen the first programs" matches IV-E.
- (b) states the level of use more plainly ("drafted and revised the text of all sections and of the supplementary material") and leads with the author's role.
- Changes I would make to (b):
  1. "wrote **and ran** the analysis, simulation-control, and figure code" ((b) drops "ran", which understates).
  2. Add: "The two sets of programs share the scoring library, the stored data, and the resample draws" or point to IV-E, so "recounted" is not read as an independent replication.
  3. Keep one sentence on the AI panel: "Pre-submission reviews by an AI panel informed the revisions." Dropping it removes a disclosed use of AI.
- (b)'s first sentence ("reviewed and approved all content") is the author's own confirmation and is a gate; it must be true as written before it is used.

---
*End of seat R1. Files re-hashed at the end: unchanged (values above).*
