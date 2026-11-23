# Brief: claim audit of the final v13 text (A10 §10.3)

For a fresh agent on a model other than the writer's (writer: Claude Opus 5.5; run this on Claude Fable 5.2 or Claude Sonnet 5.5). Prepared 20 Nov 2026 by session A; it starts at the text freeze (target 21 Nov 02:00 EST).

## Read
- `revision_v13\AMENDMENT_10_v13.md`: §0 (overrides everything else), §2 (definitions), §5.3–§5.4, §6, §7.5, §8.5 (hypotheses and pass rules), §9 (what the abstract, contributions and conclusion may say for each outcome), §10.
- `revision_v13\work\A_text\out\MANUSCRIPT_v13.md` (the frozen text), `out\OUTCOMES_v13.json` (statuses), `out\DERIVED_v13.json` (each printed value with its export key, source file and recount).
- The package exports named in DERIVED (`work\<pkg>\out\A_EXPORT_<pkg>.json`), and `work\A_text\RESULTS_INTERFACE_v13.md` §4 for what each key means.
- Coordinator decisions that change the wording of A10 (they are recorded in `work\A_text\STATUS.md`): "amplitude-matched ranking oracle", never "ceiling" or a bound; CK3 and AM not computed on the real logs; PS not caution-matched in closed loop; F's clearance departure (if `F.clearance` = "departure").
- Do **not** read the generator code in `work\A_text\gen\` or `build\`: judge the text against the amendment and the data.

## Audit
Every sentence of the Abstract, Sections I and V–VII, and every main-table and figure caption. For each, check:
1. **Numbers match their source:** the value printed equals the export value at the printed rounding, and the interval is the one the caption says.
2. **Wording follows §9** for the outcome in OUTCOMES (and the coordinator's wording decisions above).
3. **Labels:** "confirmed" only for a hypothesis that passed with every earlier one in its sequence; old and tuning runs, Section V-D and the post hoc E5q check are exploratory or post hoc.
4. **No claim exceeds its rule:** e.g. no equivalence where H2/K1/F-H1 failed; nothing tested in a data set whose room test failed; no bound language for the amplitude-matched oracle; no transfer of magnitudes; the stop wording replaced only if the closed loop ran.

## Output
`revision_v13\work\A_text\notes\CLAIM_AUDIT_v13_v02.md`: a table with one row per finding (location, quoted sentence, check 1–4, the rule or value it breaks, the fix), then a list of sentences checked without findings, by section. Say which model you are. Do not edit the text.

## After the fixes (v03)
Session A fixes every finding through the generators, rebuilds, and gives a fresh agent (again not the writer's model) the changed sentences only, with the v02 findings: `notes\CLAIM_AUDIT_v13_v03.md` (delta audit).
