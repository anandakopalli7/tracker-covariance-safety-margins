# Type-A options O-1 and O-2: feasibility note, v01

Coordinator (Claude Opus 5.5), 22 Nov 2026, 19:23 EST (Get-Date). For Paper work summary, to put a choice to the author.

**Status:** nothing has been planned, locked or run. Sources:
- the 18:30 package;
- `shared\trackers\trk_arrays_v01.py` lines 144–243;
- the module of record `ol_gateR_core_v01.py`, `s_P` and `crit_rows`, read only;
- CD's and F's definitions and status files.

**Key fact for both options.** Each margin source is stored per decision as a critical scale, `crit_rows(D, S)`. Here D is the clearance along each constraint and S = zᵀPz, with P carried forward at constant velocity and no process noise.
- CK3 is `crit_rows(D + SH, Sbar)`: the braking-shifted path SH with the class-average variance.
- N is `crit_rows(D, Pr)`: the tracker's own covariance on the constant-velocity path.

## O-1: the covariance on top of the braking prediction's path
- **What would be tested.**
  - Add the source CK3N = `crit_rows(D + SH, Pr)` and compare it with CK3 at equal caution. The measure is (D(F0→CK3N) − D(F0→CK3)) / D(F0→E), on the paper's room, with the paper's ±5% margin.
  - **Caution: this is almost a foregone conclusion with the fixed-noise tracker.** Its covariance is a near-constant multiple of F0's, so CK3N's frontier is CK3's frontier rescaled, and no difference is close to certain. That is the same "could hardly fail" objection the panel raised against the confirmed result.
  - The informative arm is therefore **dropouts at start probability 0.10**, with the dropout-estimated class average, where the covariance varies (the 2.8% case). The question is whether it still adds anything once the path is right.
  - Run sets: the fresh lead-braking runs as primary, with the DR masks; the 150 new runs as replication, with the DR2 masks. The fixed-noise arm is a scope check only.
  - A positive control is needed first: the ranking oracle E5 on CK3's path. CK3 already recovers 78% of the room, so only about a fifth of the room is left. If E5 cannot detect a ranking there, the result is another "no room".
- **Inputs, all on this laptop now.**
  - Run logs: `CD_capture\runs\` (pc13_ 210 including cut-in; pl12_ 150) and `archives_l12\`.
  - Arrays of record: `CD_capture\arrays\CV0`, `arrays_l12\CV0`.
  - Dropout masks and code: `F_dropout\masks\DR_MASKS_v01/v02.json`, `F_dropout\code\dr_extract_v03.py`.
  - Library: `shared\trackers\`. Modules of record and P̄ in the ProgrammeA folder, read only.
  - Each extractor needs one added line.
- **Where it would run, how long, and the cost.**
  - **On the laptop:** BelowNormal priority, at most two worker processes. Re-extraction measured about 8 s per run (pod) to 69 s (fresh, with extras). The estimate is 1–2.5 h for the fixed-noise arm and 2–4 h for the dropout arm. The second program runs after the first, so lock to recounted values takes about 8–12 h overnight with nominal 95% intervals, at **$0**.
  - **With A10 §2.6's calibrated intervals:** add about 2 h per seed per population on the laptop, or about 20 min per seed on a pod.
  - **On pods:** about 4–6 h and about $4–8 for two RTX 4090 pods at $0.89/h. The balance was $5.37 at 12:32 and drains about $0.03/h, so it is about $5.2 now (not re-checked). That is below the rule of never running pods under $10, so pods need a top-up by the author.
- **Who does what** (as for A11 to A13):

  | Step | Who |
  |---|---|
  | Write AMENDMENT_14 §O-1 | Coordinator |
  | Approve | Author, via Paper work summary |
  | Lock (LOCK_A14a), before any value | Coordinator |
  | First program, fixed-noise arm | CD |
  | First program, dropout arm | F |
  | Second program, independent recount from the logs plus a scoring recount; Holm within A14 | A different model |
  | Text | A |
  | Review of the result | The same panel |
- **What each outcome lets the paper say.**
  - *No gain, within ±5%:* the dropout gain does not survive a braking prediction. The room is prediction error, and the "constant-velocity prediction" scope note can be narrowed. This answers DA's R-M5, so a null raises the score modestly; my estimate is +0.2 to 0.4.
  - *Gain:* a varying covariance adds even on a better path. This is a new positive, but it invites a coast-count control on CK3's path as well (scope creep).
  - *Harm:* the margin costs decisions on top of a braking prediction. This contradicts the abstract's last sentence ("the results do not justify removing a covariance margin"), which would have to change.
  - *Inconclusive:* likely if the remaining room is too small. It adds length for little.
- **Risks.**
  - A fourth amendment written after AI-panel reports, which strengthens the process objection.
  - About 150–200 words, one Table 6 row and a supplement section, on a paper already 13 pages against a recommended ten.
  - The harm outcome undercuts the last sentence of the abstract.

## O-2: the two-noise IMM and the adaptive filter with process noise over the look-ahead
- **What would be tested.**
  - Replace zᵀPz with zᵀ(P + Q_int(t))z. Q_int is the tracker's process noise integrated to each look-ahead time: mode-weighted for the IMM (projected to position and velocity), and scaled by clip(m, 0.25, 10) for the adaptive filter.
  - Compare each tracker with its own class average, which carries the class-average Q.
  - Hypotheses: each tracker's share against the ±5% margin, and the change from 2.2% and 4.6%.
  - Run sets: fresh lead-braking runs, with the new runs as replication. The fixed-noise tracker is a control.
- **Inputs.**
  - The same run logs, plus re-tracking with the library's IMM2 and B2 code (`shared\trackers\trk_tracker_v02.py`, `trk_filters_v01.py`, `B_retrack\imm2\`).
  - All on the laptop. The per-decision mode probabilities and adaptive scales are not stored, so re-tracking is needed.
  - New code: a variance function with Q, and Q exposed at each decision. The module of record stays read only.
- **Where it would run, how long, and the cost.**
  - Code and tests on old runs: 2–3 h.
  - Re-track and extract: 2 trackers × 255 runs at about 35–60 s each, so 2.5–4 h with two workers.
  - The second program must re-implement the mode-weighted Q: 3–4 h.
  - Laptop total: about 12–20 h, $0.
  - Pods: about 5–8 h and $8–15, after a top-up.
- **Who does what:**

  | Step | Who |
  |---|---|
  | Plan and lock | Coordinator, after author approval |
  | First program | B (owns the trackers), with CD for the adaptive filter's arrays |
  | Second program | A different model |
  | Text | A |
- **What each outcome lets the paper say.**
  - *Same shares:* the interface did not limit these trackers. This closes R2's M2 and N-6, so a null raises the score.
  - *Larger shares:* the varying noise has more decision value than reported. This is a stronger positive, but the abstract's "2% to 5%" changes.
  - *Smaller or no shares:* the 2.2% and 4.6% are interface-specific. That weakens two of the paper's three positive results.
- **Risks.**
  - Many new design choices: how Q is weighted and projected, and the class-average Q. That is a forking-paths exposure.
  - A changed margin definition invites the question "why not every tracker".
  - It can weaken existing claims.
  - It brings the most new code of any option.

## O-3, outside this revision
A decision-level real-log test with room needs a new log source and a new pre-registration, measured in weeks, not hours. The nuScenes decision test found no room, and Argoverse 2 is excluded here and belongs to the companion paper.

## Recommendation: O-1 alone
- **Run it on the laptop overnight, at $0.** The primary is the dropout arm at start probability 0.10, the fixed-noise arm is a scope check, and E5 on CK3's path is a positive control checked first. Use nominal 95% intervals, labeled as such, unless the author tops up for calibrated ones.
- **Why O-1.** It answers the objection that the most seats raised: the room is prediction error, and the covariance was never tested on a better path. Every input is on the laptop, it needs one added line in each extractor, and two of its three likely outcomes strengthen the paper's main message.
- **Why not O-2 now.** It costs about twice as much, adds new design choices, and can take away two of the three positive results.
- **What O-1 does not guarantee.** A 7 is still not assured. The synthesis's 7.2–7.5 with one type-A item is a forecast, and forecasts here have run about 0.5 high, so a realistic range is about 6.8–7.2. The text-only fix round (N-1 to N-20) is needed either way.
