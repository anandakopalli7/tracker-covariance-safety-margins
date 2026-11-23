# Round-2 panel: seat brief (common part) — v01, coordinator, 22 Nov 2026 about 05:35 EST

You are one seat of a fresh five-seat ARS pre-submission review panel for the paper's round-2 freeze (v13, after AMENDMENT_12). Your seat, role card and model are named at the end of this brief.

## Hard rules
- Read only. Write only your one output file under `ARS_TRIAL\review_v13_round2_output\phase1\`. Never change anything in `revision_v13\`.
- Never open anything named `<excluded folder 1>` or `<excluded folder 2>`, nor the author's local secrets folder. The folder `<library folder>` may be read but never changed.
- Send no manuscript text to any external service (no web search with manuscript text, no uploads). Install nothing. The laptop is shared and memory is tight: at most one light `python -I` process at a time.
- The author block, repository/DOI and the AI-use confirmation are the author's placeholders: list them as submission gates, not findings. The title is the author's choice: comment only if a sentence of the paper contradicts it.
- Do not read: the response letter, earlier review reports (`review_v13_output\`, `review_v13_sprint_output\`), other seats' files, or session notes. Judge the paper as an editor would.

## What to review (check SHA-256 at start and end; report both)
Folder: `ARS_TRIAL\revision_v13\work\A_text\out\freeze_v13_0623\` (frozen 22 Nov 2026 06:23:03 EST).
- `MANUSCRIPT_v13.md` sha256 893442e4437e01fa6159dd9bbb8ebae21af65508a70064890b17929cf70db958 (read this as the paper; `MANUSCRIPT_v13.tex` for floats and references)
- `SUPPLEMENT_v13.md` sha256 f915fd798bbc9d3c53c56cea74d5b0ea4279463f3f3385b0e93488dba802f426
- `MANUSCRIPT_v13.pdf` sha256 4bd544e9ce3aff7eab8940c1f371ccd709da9910b963d3833e540f560b755da8 (10 typeset pages; no PDF renderer on this machine, so rely on the .md/.tex and BUILD_REPORT_v13.md for layout facts)
- Figures (PNG, viewable): `ARS_TRIAL\revision_v13\work\A_text\out\figures\`
- Do NOT read RESPONSE_TO_REVIEW_v13.md, TEXT_FREEZE_v13.md or RECOUNT_COVERAGE_v13.md in that folder (seat blinding), except where your seat's extra reads allow.
Round-2 sections to re-point your card's focus anchors to: Section V-B (tracker variants, including the two-noise IMM), Section V-E (where the covariance varies: dropouts, the replication on new runs and its dose-response, the 10 Hz configuration, the online-versus-permuted check on new runs, the caution-matched closed loop, the nuScenes mechanism check and the real-log decision test), Sections VI-VII, Supplement S14-S15 (S15 holds the round-2 details and the Holm table) and Table S5 (amendments and departures).

## How
- Use the skill `academic-research-skills:academic-paper-reviewer`, mode `full`, for your one seat only. Your Phase-0 card is in `ARS_TRIAL\review_v13_output\00_phase0_field_analysis_and_cards.md`; re-point its focus anchors to the round-2 sections named at launch. The card-confirmation pause is not held (non-interactive): say so in your header.
- Name your model (not just the family) in your file's header.

## Questions every seat answers (in its own role)
1. Is each result reported at its true size, with its label right? ("confirmed" only for the original plan; "passed (amendment)" or "replicated under rules fixed before the data" for amendment tests; Holm across the six round-2 primaries reported beside them.)
2. Does any sentence claim more than its test allows? In particular: the dropout gain's source; the caution-matched closed loop (its matched caution sits at the bottom of the tested grid); the nuScenes mechanism check (its primary population was chosen on the training split, disclosed); the real-log decision test that found no room.
3. The previous round's main limits were: the headline equivalence could hardly fail (near-constant covariance); thin evidence where the covariance varies; same-day amendments without multiplicity control; one configuration at 2 Hz with no latency; an unfair IMM arm; a closed loop that was not caution-matched. For each: does this version address it, partly address it, or not, and what remains?
4. Readability: bottom line first in the abstract; coined terms defined once; can a reader find each claim's evidence?
5. Your recommendation (accept / minor / major / reject), your score out of 10 and in stars, the most likely editorial outcome at IEEE OJ-ITS, and what single change would raise your score most.

## Output
`phase1\0N_<seat>.md`: header (seat, model, card, files and hashes, pause not held), findings as a table (location, finding, severity CRITICAL / MAJOR / MINOR, evidence, the fix in the fewest words), then the five answers. Final reply under 200 words: recommendation, score, top three findings, your file's SHA-256.
