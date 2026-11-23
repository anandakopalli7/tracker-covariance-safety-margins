# Journal-Fit Review (seat 1 of 5)

- Seat: Journal-Fit Reviewer (internal id EIC). Senior associate editor perspective for IEEE Open Journal of Intelligent Transportation Systems, regular paper. One recommendation among five; no decision authority.
- Model: Claude Fable 5.2 (model id claude-fable-5-2).
- Date: 21 November 2026.
- Material read: MANUSCRIPT_v13.md (whole), SUPPLEMENT_v13.md (whole), Figs. 1-4 (PNG). Judged offline from the text alone; no web, no citation service, no other seat's report, reference [10] not consulted. The PDF was not rendered; the page count (10) and word counts (abstract 218, body 5,191, supplement 11,950, 42 references) are taken as given.
- Calibration status: NOT_CALIBRATED.

## 1. Recommendation

**Major Revision.** Confidence 4 of 5 (novelty, fit, clarity and editorial handling are within this seat's competence; the statistics were not reviewed in depth and I could not check any reference against a database).

Reason. The topic fits the journal and the work is unusually candid about what it did not show, but the one result that is confirmatory (a fixed-noise covariance equals a class-average margin behind a braking lead) is one the paper itself says follows from known filter theory, while two of the three confirmatory test beds returned nothing to test and the cases where a covariance does vary are left to future work. The title, abstract and closed-loop sentence promise more than the tables carry, and the abstract cannot be read without the paper's private vocabulary. Almost all of the needed changes are wording and restructuring; one (a test where the covariance actually varies) would need new analysis, and without it the paper must be reframed as a protocol-and-measurement paper.

**Desk-rejection risk: moderate.** Scope and length are fine. The risk comes from three things an editor sees in the first five minutes: (a) an abstract whose second sentence ("The oracle's room is 5.58...") is unintelligible to a reader who has not yet met the paper's terms; (b) an Acknowledgment stating that an AI system drafted every section, wrote and ran all code, wrote the checking programs and audited the claims, with the author's own verification statement still a placeholder; (c) a headline null that the paper calls "not new" in mechanism. If the three author-only placeholders are still open at submission the risk is high, but those are gates, listed in Section 7, not findings.

## 2. Strengths

S1. **Scope stated honestly, including what was not tested.** Abstract and Section I contribution 2 say that cut-in events and held-out nuScenes logs "showed no measurable room, so nothing was tested there"; Section VI "Limits" repeats that one detector, one in-house planner and straight simulated roads were used and that removing a covariance margin is not justified. A reader is not misled about external validity by the body text. (Abstract; Section I; Section VI.)

S2. **The abstract, contribution 2 and the conclusion state the same claims in the same words.** The sentences on room, equivalence, the IMM and the braking prediction are identical across Abstract, Section I and Section VII; I found no number that differs between them. (Abstract; Section I item 2; Section VII.)

S3. **Every number in the abstract is carried by a main-text table** (trace in Section 6 below). None rests on the supplement alone. (Tables II-V.)

S4. **A clear, reusable methodological idea.** Comparing margin sources at equal caution against a positive control (oracle) and a same-amplitude permuted control is a clean design that readers evaluating perception outputs by their downstream effect can reuse. (Section IV-B, IV-C; Table I.)

S5. **The dependence of an open-loop score on its assumptions is shown with numbers, not asserted.** Table V and Fig. 4 show the room falling to 0.101 of its value under a reaction-and-stop assumption, the after-stop room falling from 173.4 to 77.8 decision-equivalents with update rate, and the braking prediction's share moving from 0.379 to 0.837 across run sets. For the journal's readers this is the most useful content of the paper. (Section V-D; Table V; Fig. 4.)

S6. **Negative side of the positive result is reported.** The braking prediction's cost behind leads that do not brake hard is in the abstract and in Table V, and the pooled 0.783 is qualified in Section V-A (0.411 while the ego moves; 0.244 to 0.774 by how long after-stop decisions are kept). (Section V-A; Table V; Table S10.)

S7. **Length and reference count suit a regular paper.** Ten typeset pages, 42 references, four figures, five tables. (Given facts.)

S8. **AI use is disclosed, with model names and the sections affected,** in the Acknowledgment as IEEE asks, and the limits of the literature search are disclosed rather than hidden (Supplement S13). The disclosure itself is a strength; what it discloses is weakness W8 and W9.

## 3. Weaknesses

### W1. The confirmatory result is narrow and, by the paper's own account, expected; the interesting case is not tested
- Severity: MAJOR
- Location: Section II "Novelty, with its limits"; Section I paragraph 4; Table III; Table S28; Section VII last paragraph.
- Evidence: "The mechanism of the null is not new" (Section II).
- What is wrong: The single confirmed equivalence concerns a covariance of which 99.9% of binding rows lie within 5% of its median ratio (Table III). Section VI explains that the equal-caution sweep removes any global scale, so such a covariance cannot change decisions; the introduction says "a null is expected". Of the three confirmatory test beds, two (cut-in, nuScenes) had no room, so nothing was tested. The one tested variant meant to vary (the IMM) also turned out nearly constant (99.7%). The only covariance that does vary (adaptive process noise, 21.5% within 5%) is reported as descriptive, with a share of 0.0459. The supplement's own check (Table S28) shows where a covariance does vary (pedestrian crossing 8.51%, vehicle crossing 4.09% of rows within 5%), and those families are excluded and named as "next steps". For a regular paper, the take-away "a nearly constant margin behaves like a constant margin behind a braking lead in one simulator" is thin; the question in the title is not answered for the cases where the answer is open.
- Fix: Either (a) add a decision-level test in at least one family where the margin ratio varies (crossing traffic or track births), under the same protocol, or (b) reframe the paper around contributions 1 and 3 (the protocol with its controls, and what an open-loop decision score depends on), present the lead-braking null as the worked example, and change the title accordingly (see W2). Option (b) is feasible within the present data.
- Needs: (a) NEW analysis; (b) WORDING ONLY (restructuring of title, abstract, contribution order).

### W2. The title promises a test "on Real Driving Logs" and a result about IMM covariances that the paper does not deliver
- Severity: MAJOR
- Location: Title; Table II column "Real logs, held out"; Section V-A.
- Evidence: "so nothing is tested on the logs" (Section V-A).
- What is wrong: The title lists three test settings as if each produced a test. On nuScenes the room is −0.01 [−0.13, 0.13] and every other row is "n.t."; that outcome was reached after a change to the clearance definition made after the design-split result (Section III-C, Table S5). The title also uses "Fresh", a term private to this project, and at 24 words it is long. A reader searching for evidence on real logs will open the paper and find none.
- Fix: Remove the real logs from the title or name them as what they are (for example "... An Equal-Caution Protocol and a Simulation Test Behind Braking Leads"); drop "Fresh"; keep the nuScenes outcome in the body as a reported non-test.
- Needs: WORDING ONLY.

### W3. The abstract is not readable on its own
- Severity: MAJOR
- Location: Abstract, sentences 1-2 and 5.
- Evidence: "The oracle's room is 5.58 [4.99, 6.17] percentage points" (Abstract).
- What is wrong: "Room", "equal caution", "oracle controls", "locked plan", "fresh", "rank information at the tracker's amplitude" and "amplitude-matched ranking oracle" are used in the abstract before any definition; they are defined only in Section I paragraph 3 and Section IV. The first sentence has 44 words and five nested qualifiers, including the parenthesis "(contacts from behind excluded)", which a reader cannot place. The abstract does not say that the 5.58 points refer to lead braking in simulation until two sentences later, nor what the points are points of. Shares are given as bare decimals ("0.0009", "0.783", "0.916") without saying they are fractions of the room. An indexing-service reader, and an editor screening the submission, will not understand the main result.
- Fix: Rewrite in plain terms: state the question; state the measure once in words ("the reduction in unsafe go-decisions that a perfect margin would give at the same loss of progress"); give the lead-braking result; say plainly that the cut-in and real-log data offered nothing to test; give the braking-prediction result with its cost; end with the recommendation. Move "contacts from behind excluded" to the body. If the plan fixed the wording of outcome sentences (Supplement S3), state outcomes in the fixed wording but define the terms first, or record the rewording as a departure.
- Needs: WORDING ONLY.

### W4. "Detection at the tracker's amplitude" is not what Table III shows for the tracker of record
- Severity: MAJOR
- Location: Abstract sentence 2; Section I contribution 1; Section IV-C; Table II row E5; Table III row "CV filter, online".
- Evidence: "the score detects rank information at the tracker's amplitude" (Abstract).
- What is wrong: This is a claim-consistency finding, not a statistical one. The confirmed detection (E5 share 0.013 [0.010, 0.015]) uses a fixed ±5% band (Table I: "varied by ±5%"). Table III shows that the tracker of record varies far less than that (99.9% of binding rows within 5% of the median) and that the oracle at its own amplitude recovers 0.0001 [0.0000, 0.0002]. So the paper's first contribution, "a control at the tested output's own amplitude", is carried for the tested tracker by a control at a larger amplitude, while the control at its actual amplitude recovers essentially nothing. A reader comparing the abstract with Table III will conclude either that the phrase is wrong or that the equivalence could not have come out otherwise. The paper applies the label "amplitude-limited" to the IMM but not to the tracker of record, to which the same numbers apply more strongly.
- Fix: Say in the abstract, Section I and Section IV-C that the detection control is at a ±5% band and that the tracker's own variation is smaller; report the tracker of record's own-amplitude oracle (already in Table III) beside E5 in Table II; state plainly that at its own amplitude the tracker of record, like the IMM, has almost no room to recover, so the equivalence is expected. This also strengthens the case for reframing under W1(b).
- Needs: WORDING ONLY (the values exist in Table III).

### W5. The closed-loop sentence in the abstract is stronger than Table IV
- Severity: MAJOR
- Location: Abstract penultimate result sentence; Section VII; Table IV; Table S25; Table S4.
- Evidence: "the braking prediction is safer at no extra cost" (Abstract).
- What is wrong: Four qualifications in the tables are missing from the abstract. (1) Table IV gives the braking prediction a time-lost difference of 0.16 [0.10, 0.22] s at the lower level: a cost whose interval excludes zero. "No extra cost" is a label from the plan's rule (upper end below 0.5 s), not a plain-language fact; the conclusion adds "by the plan's rule", the abstract does not. (2) The result holds at the lower of two levels only; at the higher level Table IV classifies the same arm "inconclusive". (3) It rests on 60 cases, 12 contacts against 0. (4) In closed loop behind stop-and-go leads the same arm is "safer at a cost" (Table S25), and the plain time-gap baseline TG obtains the same contact difference with less time lost (−0.13 s, Table IV), which the abstract and conclusion do not mention. In addition, the status of the closed-loop results is unclear: contribution 2 is headed "A confirmatory test" and includes the closed-loop equivalence, but Table S4 leaves the Status column empty for the closed-loop rows and Section V-D speaks of results "outside the confirmatory sequences".
- Fix: Reword to, for example, "in closed loop at the lower of two caution levels, the braking prediction had no contacts against 20% for the class average, for 0.16 s more time lost; a time-gap rule did as well". State in one sentence whether the closed-loop classifications are confirmatory, and fill the Status column of Table S4.
- Needs: WORDING ONLY.

### W6. Private vocabulary and table density exceed what a 10-page paper can carry
- Severity: MAJOR
- Location: Section I paragraph 3; Table I; captions of Tables II, III, IV; Sections III-A, V.
- Evidence: "Five terms carry the paper." (Section I).
- What is wrong: The five announced terms are only the start. The reader must also hold: twelve source codes (F0, N, N_x, E, E5, E5p, E5_x, NA, CK3, AM, TG, PS); "rows"; "decision-equivalents"; "fresh", "old evaluation" and "tuning" runs; "record basis" and "like for like"; "matched setting" and "design caution"; "lower" and "higher level"; "amplitude-limited", "uninformative variation", "recovers", "inconclusive"; the status marks (C), (P), (F), n.t., n.c.; and three evidential grades ("confirmed", "descriptive", "exploratory", used 8, 13 and 11 times). Captions run to 146 words (Table II), 113 (Table III) and 191 (Table IV). Table III prints different intervals from Table II for the same two quantities (N: [−0.0009, 0.0015] against [−0.0007, 0.0010]; IMM: [−0.0018, 0.0012] against [−0.0013, 0.0009]) because of different interval levels, which a reader discovers only in the caption. NA and AM are defined in Table I but have no result in any main-text table. "Wrong go" and "caution" have established names, which the supplement's own Table S3 lists (collision under the assumed manoeuvre; conservatism or lost progress).
- Fix: Use the established terms of Table S3 in the main text. Cut Table I to the sources that have a main-text result. Print one interval per quantity in the main text. Move rule definitions out of captions into one short "Classification rules" paragraph. Replace codes by words where a code is used fewer than three times (PS, TG, NA, AM). Decide whether three evidential grades are needed; two (planned test; other) would do.
- Needs: WORDING ONLY.

### W7. The main text is not self-contained; a reader needs the supplement to understand claims made in the abstract
- Severity: MAJOR
- Location: Section IV-B, IV-D, IV-E; Table V; Supplement S2, S3 (Tables S4, S5), S8.
- Evidence: "fixed and hashed before any of their values was computed" (Section IV-E).
- What is wrong: The supplement is 2.3 times the length of the body and is cited 26 times from it. Items needed to read main-text claims exist only there: the rule that turns numbers into "costs progress" (Supplement S8), used in the abstract; the definition of "matched setting"; the list of hypotheses with pass rules (Table S4); the interval calibration. More seriously for an editor, the main text presents the locked plan without qualification, while Table S5 lists 25 departures and readings, among them a second lock written in two stages, four code fixes after the second lock, a figure exporter written after the lock, and a clearance change on the real logs after a design-split result. The main text mentions the last and one other. The departures may all be harmless, but the reader of the paper alone is given a cleaner picture than the record.
- Fix: Add to Section IV-E one sentence giving the number of recorded departures and naming those made after the second lock, with a pointer to Table S5. Bring the "costs progress" rule and the hypothesis list (a six-line table) into the main text; space can come from W6 and from the triple repetition noted in W10.
- Needs: WORDING ONLY.

### W8. Extent of AI assistance, and who approved what, for a single-author journal submission
- Severity: MAJOR
- Location: Acknowledgment; Section IV-E; Supplement S12; Table S5.
- Evidence: "drafted the Abstract, Sections I–VII and the Supplementary Material" (Acknowledgment).
- What is wrong: The disclosure is in the right place and names systems and sections, which meets the form of IEEE's rule on AI-generated content. What it discloses will still concern an editor. (1) One AI system family did the literature search, wrote and ran all analysis code, wrote all text, wrote the second programs that check the first, and audited the claims; the supplement says the two programs "share the scoring library, the stored arrays and the resample draws". The checks are therefore role-separated, not independent, and the paper should say so in those words in the main text. Section IV-E describes the second programs without saying that both writers were AI models; a reader learns it only from the Acknowledgment. (2) The sentence that should carry the human accountability, the author's statement of what was verified personally, is a placeholder. (3) Table S5 records post-lock changes "approved by the coordinator" and rules "set by the coordinator"; the coordinator is never identified. If the coordinator is an AI session, departures from a pre-registered plan were approved without the author, which bears directly on the claim that the plan was locked. (4) Section IV-E says AI-panel reviews "shaped this revision": a fresh submission has no revision, and pre-submission AI reviews are not verification; the sentence sits in a section headed "Verification". (5) The supplement states that values marked n.c. were "not computed by the plan's deadline"; all dated steps (search 17-18 Nov, locks 20 Nov, fixes 20-21 Nov 2026) fall within a few days. An editor will ask whether the author had time to check what is being signed.
- Fix: Identify the coordinator and state for each post-lock approval whether the author made it. State in Section IV-E that the first and second programs were written by AI models of one vendor and are not independent. Move the AI-panel sentence to the Acknowledgment and reword it ("pre-submission reviews by an AI-based panel were used"). Complete the author's verification statement with concrete acts (which tables recomputed or inspected by hand, which references read). Check the journal's current author guidelines on AI-generated text before submission; I could not verify them offline.
- Needs: WORDING ONLY, plus author-only verification acts; no new value.

### W9. The literature basis of the novelty claim and of several citations is weak by the paper's own account
- Severity: MAJOR
- Location: Section II "Novelty, with its limits"; Supplement S13; References.
- Evidence: "no full text was opened" (Supplement S13).
- What is wrong: The novelty claim ("we found no study that tests...") rests on a search that was English-only, in which one engine blocked queries and one service was not accessible, in which "publisher full texts were not searched", and whose first round did not search the IMM and adaptive-filtering literature for a planner-side test, although the IMM is now in the title. The supplement states that "the related-work statements about intelligent-vehicle threat assessment therefore rest on abstracts" and that the four standards are cited with "their full texts were not read". Six references were added because an AI review panel suggested them and were checked "against their Crossref records by identifier", which confirms that they exist, not that they say what the sentence citing them says. The reference list contains no article from IEEE Transactions on Intelligent Transportation Systems, IEEE OJ-ITS or the ITSC conference, although the query list (Table S29) shows that directly relevant intelligent-vehicle work was found (uncertainty propagation in criticality measures; probabilistic time-to-collision; worst-case analysis of collision-avoidance systems with measurement errors; robust emergency-braking design under sensor errors) and none of it is cited or discussed. For this journal's readership, that is the nearest prior literature.
- Fix: The author should read, in full, every source that carries a claim in Sections I-II and VI, and say so in the verification statement. Add and discuss the threat-assessment-under-measurement-uncertainty literature found by queries 15-17, 25-26, 36-38 and 42, and state how the present question differs. Soften the novelty sentence to the scope actually searched, in the main text and not only in the supplement.
- Needs: WORDING ONLY and added references, after author reading; no new value.

### W10. The same four sentences appear three times
- Severity: MINOR
- Location: Abstract; Section I contribution 2; Section VII.
- Evidence: "so nothing was tested there" (Abstract, Section I, Section VII).
- What is wrong: The outcome sentences are repeated verbatim (about 90 words each time), apparently because the plan fixed their wording (Supplement S3). Consistency is good (S2), but the repetition costs about a fifth of a page and makes the contribution list read as a results list.
- Fix: Keep the fixed wording in the conclusion; state contribution 2 in one sentence; write the abstract for a general reader (W3).
- Needs: WORDING ONLY.

### W11. "The room" in the abstract's IMM sentence is not the room of the preceding sentences
- Severity: MINOR
- Location: Abstract; Section V-B.
- Evidence: "recovers only 0.0009 [0.0006, 0.0010] of its own room" (Section V-B).
- What is wrong: The abstract and conclusion say the IMM's oracle "recovers little of the room (0.0009)", which reads as the 5.58-point room. Section V-B and Table III say the share is of the IMM's own room, against its own class average; that room is not printed anywhere in the main text (Table III gives it only by phase).
- Fix: Write "of its own room" in abstract and conclusion and print the IMM's pooled room in Table III.
- Needs: WORDING ONLY for the phrase; the pooled room of each variant is a NEW VALUE to print (presumably already computed).

### W12. "Costs progress" hides a safety gain in one of the three cases
- Severity: MINOR
- Location: Abstract; Table V rows "Non-braking leads"; Section V-D.
- Evidence: "costs progress (1.7, −4.7)" (Table V).
- What is wrong: Behind leads that stop and pull away, the braking prediction gives up 1.7 points of caution and removes 4.7 points of wrong goes. The rule labels this "costs progress"; the abstract lists it with the two cases where the cost is large and the gain is nil or small. The body states the numbers, so nothing is concealed, but the abstract's summary is one-sided.
- Fix: In the abstract, separate "costs progress with little or no gain behind constant-speed and mildly braking leads" from the stop-and-go case.
- Needs: WORDING ONLY.

### W13. Supplement: unfinished and inconsistent entries
- Severity: MINOR
- Location: Supplement header; Tables S8, S13, S17, S27; Section S12.
- Evidence: "not computed by the plan's deadline" (Supplement header).
- What is wrong: (1) Table S17 consists of eight rows of "0.00 | n.c. n.c. | n.c."; it reports nothing. (2) Table S27 prints "n.c. [−0.023, 2.813]" and "n.c. [−36.424, 0.404]": intervals without estimates, and it is unclear whether these are undefined (room near zero) or unfinished. (3) "n.c." means "no contact" in Table IV, "not computed by the deadline" in the supplement header and "not definable" in Table S24. (4) Table S8 has a row "Q" that is defined nowhere in either file. (5) Table S13 gives N's share as 0.00122 with interval [−0.00108, 0.00119], an estimate outside its own interval, and its row label "Room $R$ (pp" lacks a bracket. (6) Section S12 ends with a sentence that cites "(Supplement S12)" from inside S12, and the hand-check sentence says the same thing twice ("all agreed within 1e−6 m (all 20 within 1e-6 m)"). (7) A submission should not tell the reader that values are missing because of a deadline.
- Fix: Remove Table S17 or state its content in one sentence; print estimates or the word "undefined" in Table S27; use distinct marks for the three meanings; define Q; check the S13 entry; delete the duplicated phrases; either compute the missing descriptive values or drop them without reference to a deadline.
- Needs: WORDING ONLY, except any descriptive value the author chooses to complete (NEW VALUE) and the check of the Table S13 entry.

### W14. The supplement reads in places as a process log
- Severity: MINOR
- Location: Table S5; Section S4 "Identity".
- Evidence: "a draft of stage 2 written a minute earlier misstated" (Table S5).
- What is wrong: Clock times to the minute, "the laptop", "rented machines", "the coordinator" and one-line code-fix narratives belong in the deposit's manifest, not in supplementary material of a journal article. They lengthen the supplement and obscure the departures that matter (the real-log clearance, the non-caution-matched schedule, the sources not computed on real logs).
- Fix: Split Table S5 into (a) departures that affect what a result means, kept in the supplement, and (b) operational records, moved to the deposit.
- Needs: WORDING ONLY.

### W15. Figures
- Severity: MINOR
- Location: Figs. 1-4 and captions.
- Evidence: "Curves that coincide at this scale are drawn over each other." (Fig. 2 caption).
- What is wrong: Fig. 1 is a six-box pipeline whose boxes list source codes; it conveys little that Section III does not, and it does not show the scoring idea (frontier, room), which is what a new reader needs a picture of. In Fig. 2 the baseline F0 is invisible under N, the caption calls the right-hand panel an "Inset" although it is a separate panel, and that panel shows an empty plot. In Fig. 3 the axes say "against F0" although the IMM points are against the IMM's own class average, and the filled/open coding is explained only in the caption. Fig. 4(a) puts six series on two differently coloured axes; the caption does not say which latency belongs to the values quoted in the text (the text compares 2 Hz without latency with 5 and 10 Hz at 0.1 s latency, which the figure shows are not like for like: at 2 Hz and 0.1 s the room is 5.89, Table S16).
- Fix: Replace Fig. 1 by a schematic of the frontier, the room and a share. Draw F0 dashed above N in Fig. 2 and replace the empty panel by one sentence. Relabel Fig. 3's axes "against its baseline". In Section V-D and Table V compare update rates at equal latency, or say why not.
- Needs: WORDING ONLY and redrawing; the equal-latency values already exist in Table S16.

### W16. Reference list (judged offline, from the text alone)
- Severity: MINOR
- Location: References [3], [5], [10], [15], [27], [28], [36]-[40]; Section II.
- Evidence: "the nearest published analogue of our null" (Section II, citing [15]).
- What is wrong: (1) [15] is called "published" in Section II but is listed as an arXiv preprint (v1, 2026); its title concerns "class uncertainty propagation", which does not obviously match the description "a constant-velocity baseline with a fixed covariance". (2) [5], the tracker of record, is an arXiv preprint marked "accepted to IROS 2026"; if the proceedings have appeared, cite them. (3) [27] has no DOI although Table S29 query 48 shows one was found. (4) [38] has no date or revision. (5) [40] is cited as a "Proposal" document for a regulation text in force; cite the consolidated regulation. (6) [36] and [37] are cited together as current adaptive-cruise-control standards; to my recollection ISO 22179:2009 was withdrawn when ISO 15622:2018 absorbed full-speed-range systems. I could not verify this offline and the paper says the standards' texts were not read; the author should check. (7) [3] has no access date. (8) Five of 42 entries are preprints or unpublished ([5], [10], [15], [28], [34]); [10] is the author's own manuscript under review. (9) No entry from the target journal's own community (see W9). Format is otherwise consistent IEEE style.
- Fix: Correct "published"; verify [15] against its full text; update [5]; add identifiers and dates; verify the status of [37].
- Needs: WORDING ONLY (bibliographic corrections after checking).

### W17. Run counts are stated in two ways
- Severity: MINOR
- Location: Section III-A; Data and Code Availability.
- Evidence: "For the 55 earlier lead-braking runs they were regenerated" (Data and Code Availability).
- What is wrong: Section III-A speaks of "35 lead-braking runs" (old evaluation runs); the availability statement speaks of 55 earlier lead-braking runs. The difference (20 tuning runs) can be worked out from the supplement but is not stated in the main text.
- Fix: Write "the 55 earlier lead-braking runs (35 old evaluation and 20 tuning runs)".
- Needs: WORDING ONLY.

### W18. Relation to the author's manuscript under review
- Severity: MINOR
- Location: Section I "Scope"; Section VI "Limits"; Reference [10].
- Evidence: "shares this paper's detector architecture, tracker configuration and margin form" (Section I).
- What is wrong: The statement of separation is clear and properly placed. An editor will nevertheless need to check overlap with a concurrent submission that shares detector, tracker and margin form, and cannot do so from an uncited-in-full, unpublished item. This seat did not consult [10], as instructed.
- Fix: Supply [10] to the editor as a related manuscript at submission and say so in the cover letter; keep the scope statement.
- Needs: WORDING ONLY (cover letter); an author action.

## 4. Questions for the author

Q1. What should a reader of this journal do differently after reading the paper? If the answer is "state the commitment of an open-loop score and show detection at the output's amplitude", why is that contribution third and labelled "largely exploratory", and the expected null first?

Q2. For the tracker of record, the oracle at its own amplitude recovers 0.0001 [0.0000, 0.0002] (Table III). Was any outcome other than equivalence possible for hypothesis 3? If not, in what sense is the test confirmatory rather than a check of the scoring code?

Q3. Why were the families in which the margin ratio varies (Table S28: pedestrian crossing, vehicle crossing, benign driving) not included in the confirmatory plan, given that the earlier runs already showed where the ratio is constant?

Q4. Who is "the coordinator" in Table S5? For each approval dated 20 or 21 November 2026, did the author make the decision?

Q5. What did the author verify personally? Which of the 42 references has the author read in full?

Q6. Are the closed-loop classifications of Table IV (N, CK3, IMM at the lower level) part of a confirmatory sequence? Table S4 gives them no status.

Q7. The time-gap rule TG gives the same contact reduction as the braking prediction in closed loop, with less time lost (Table IV). Why does the abstract report the braking prediction and not the simpler baseline?

Q8. Does reference [15] contain the constant-velocity, fixed-covariance baseline that Section II attributes to it? Its listed title suggests a different subject.

Q9. In Table S27, are the entries "n.c. [−0.023, 2.813]" undefined because the room is near zero, or unfinished?

Q10. Did the plan fix the wording of the abstract's outcome sentences (Supplement S3)? If so, can the abstract be rewritten for readability without a recorded departure, and will the author record one?

Q11. The Acknowledgment says pre-submission AI-panel reviews and the author's responses are deposited. Does the author intend reviewers to read them, and under what status?

## 5. Submission gates (author-only; not scientific findings)

G1. Author block: affiliation, e-mail and ORCID are a placeholder.
G2. Repository name and DOI are a placeholder in "Data and Code Availability"; the plan hashes in Section IV-E are truncated and can be checked only against the deposit.
G3. "[AUTHOR CONFIRMATION: ...]" in the Acknowledgment is a placeholder; see W8 for what it should contain.
G4. Reference [10] is under review elsewhere; supply it to the editor (W18).
G5. Confirm the journal's current rules on AI-generated content, on supplementary material length and on data availability ("sweeps are available from the author on request") before submission; none could be checked offline.

## 6. Claim trace: numbers in the Abstract

| Abstract item | Carried by | Remark |
|---|---|---|
| Room 5.58 [4.99, 6.17] percentage points | Table II, row "Room R", lead-braking column; also Table V (5.58, no interval) | Abstract does not say "lead braking" in that sentence |
| "detects rank information at the tracker's amplitude" (no number) | Table II, rows E5 (0.013 [0.010, 0.015]) and E5 minus E5p (0.008 [0.006, 0.010]) | The ±5% band is wider than the tracker's own variation (Table III); see W4 |
| "no measurable room" in cut-in and nuScenes (no number) | Table II, 0.00 [0.00, 0.00] and −0.01 [−0.13, 0.13] | Consistent |
| "within 5% of the room" (equivalence margin) | Table II, row N: 0.0000 [−0.0009, 0.0015] lies inside ±0.05 | The margin 0.05 itself is defined in Section IV-C, not in a table; Table II's caption does not state it |
| "also equivalent in closed loop" (no number) | Table IV, row N at both levels | A planned test at the lower level only (Table IV caption) |
| 99.7% of rows within 5% of its median | Table III, row IMM, column "Within 5%" | Consistent |
| 0.0009 (IMM's amplitude-matched oracle) | Table II, row "Varying covariance", and Table III, row IMM | Share of the IMM's own room, not of the 5.58-point room (W11) |
| 0.783 (braking prediction) | Table II, row CK3: 0.783 [0.720, 0.842]; also Tables III and V | "Pooled" is in the abstract; the dependence on after-stop decisions is in Section V-A and Table S10 only |
| "costs progress behind constant-speed, mildly braking and stop-and-go leads" (no number) | Table V, rows "Non-braking leads" | The rule defining "costs progress" is only in Supplement S8 (W7, W12) |
| 0.916 (per-phase schedule) | Table II, row PS: 0.916 [0.864, 0.965] | Grid frontier, not the gridless frontier of the other rows (Table II caption) |
| "safer at no extra cost" in closed loop (no number) | Table IV, row CK3, lower level: −0.20 [−0.32, −0.10]; time lost 0.16 [0.10, 0.22] s | Lower level only; higher level "inconclusive"; the cost is non-zero (W5) |
| 2 Hz updates | Table V, rows "Update rate" (5.58 / 5.31 / 5.07; 173.4 / 115.2 / 77.8) | The 2 Hz value is without latency, the others with 0.1 s (W15) |
| "recording policy" (no number) | Table V, rows "Recording policy" | Consistent |

No number in the abstract lacks a main-text table. The two items whose table support is weaker than the abstract's wording are the amplitude sentence (W4) and the closed-loop sentence (W5).
