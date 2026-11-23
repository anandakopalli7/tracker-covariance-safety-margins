# Letter to the author: result of the author-round review, v01

Written 22 Nov 2026, after the panel on your 18:30 package (13 pages). Full record: `ARS_REVIEW_AUTHOR_ROUND_v01.md`. Codes such as N-1 are the items in that file.

**The decision: major revision.** Four of the five reviewers said major; one said minor. No reviewer found a fatal problem.

**The score as it stands: about 6.1 out of 10** (the five reviewers' mean is 6.0; range 5.5 to 6.6). The earlier panel scored the 12:01 text at 6.3. That is no real change. Almost everything the earlier panel asked for is done (16 of 19 resolved, 3 partly, none open), but the new text opened new gaps of about the same size. The score is held down by things editing cannot change: the main confirmed result was expected from the start, the gains are small, it is one simulator and one planner, and the real-log tests found no room to test.

**Does anything need new analysis? No.** All 20 required items are wording (9), a value moved in from the supplement (6), or text you write from records you already have (5). Three extra analyses would raise the score but are not required: the covariance on top of a braking prediction, a rerun with process noise in the predicted covariance, and a real-log test with room. A forecast after one fix round on the required items is about 6.6 (range 6.2 to 7.0). A 7 is possible but not likely, and an 8 needs new evidence.

## The required items, in order of effort

**Minutes (words only)**
1. N-20, format: put the AI disclosure third in the ACKNOWLEDGMENT (after data and code); add (a) and (b) to Fig. 2; write "multiobject" and "midrank"; use letters for table footnotes; remove the comma after "?" in reference [21].
2. N-19: define NIS where Table 1 first uses it.
3. N-9, N-10, N-11, N-17: one sentence each (the crossing scenario was added by an amendment, "fixed before any run was scored", define "level effect", and the wording of reference [27]).
4. N-1: change "made every scientific decision" to "made or approved every scientific decision" (see below).

**An hour or two (existing records)**
5. N-3: the abstract and the summary sentences. Tag each number as confirmed, amendment or descriptive; call 4.6% descriptive; say each share is against its tracker's own class average; "slightly more" for the coast-count margin and say its factors come from the covariance's own growth; add the 78% range and the progress cost; name the planner, speed range and interface; lead with the answer. Stay at 250 words or fewer.
6. N-2: two sentences defining the tracker's "permuted twin" (the plan is in AMENDMENT_11 section 6b).
7. N-6, N-8, N-12, N-14, N-15: move short facts from the supplement (IMM specification, recount scope, a Table 6 row for the earlier closed loop, NA/AM/TG or delete them, braking-phase NIS).
8. N-13, N-7, N-16, N-18: closed-loop cost columns; name the AI panel's model and who audited what in S12; classes in the nuScenes pairs; the third slip in Table S5.

**A day or more (your own work)**
9. N-4: the sentence "The main text holds every result on which the claims rest" is not true as written. Bring in about 11 short facts from the supplement (list in section 7 of the record), or soften the sentence. This adds length; trim V-E to pay for it.
10. N-5: read in full the papers the text characterises ([13], [15], [19], [35], [36] and the closest others). Then state how many references you read in full and that you checked each against its publisher or Crossref record. Today the text says an AI system ran the search and the supplement says no full text was opened.

## What is yours to decide or confirm

- **The first sentence of the ACKNOWLEDGMENT (N-1).** The deposited amendment files record some design choices as "the coordinator's" (the output rule under dropouts, the nuScenes primary population, the third amendment's choices). A reader of the deposit will see that against "made every scientific decision". The smallest fix keeps your sentences: "made or approved every scientific decision". Only you can confirm that you approved each such choice, at least in scope, before its data were scored. The files support this for the first and second amendments; the third ran under your standing approval from the second. If that is the true size of it, a fallback is "made or approved every scientific decision, or delegated it within an approved scope". I have not decided this for you.
- **Model names and the Codex sentence.** Nobody on the panel could check the model names or the Codex statement. Confirm them.
- **The AI panel.** Name its model or models, and confirm that the reviews and responses will be in the deposit (the paragraph promises it).
- **The surname form** in the byline, the running head and reference [10] (one form, so the self-citation is recognisable).
- **Reference facts.** Check [27] and the references added in round 2; the panel could not check them offline.
- **"et al."** in [9], [13], [15], [21], [34]: count the authors (IEEE allows "et al." above six).
- **Length.** The paper is 13 pages; the journal recommends ten. Decide whether you accept that.
- **The title.** "Preregistered" is defined in IV-E as internal locks. It is your choice; nobody on the panel treated it as an error.
- **The repository name and DOI** are a gate, not a finding.

## A caution

All five reviewers and the editor are Claude models of one family, and the same family wrote the text and ran the earlier panels. They can share blind spots. Treat the score as a guide to what to fix, not as a prediction of a journal's decision. A real editor would most likely send this out and return major revision; a desk rejection is possible (about 10% by my rough judgement) and the Acknowledgment sentence is the part most under your control.
