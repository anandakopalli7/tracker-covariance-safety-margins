# Package F departure (A10 §11): the true clearance does not count actors behind the ego

Written by session F (Claude Opus 5.5), 19 Nov 2026. F's clock read 23:52:08 EST just before writing. **No value under this rule has been computed.** This file is pinned before any such value exists. Its SHA-256 goes into `LOCK_A10_2.txt` with `FREEZE_F.json`.

## 1. Decision and record
- **Decision:** option (b) of `F_HORIZON_STOP_v01.md` (shared notes), chosen by the coordinating session (message timed 19 Nov 23:58 EST, received by F at about 23:52 on F's clock). The author has been told and may veto it until the text freeze. If they do, package A prints the pre-registered outcome (a).
- **The pre-registered outcome stays in the record:** horizon rule of A10 §8.3 under the clearance of record.
  - D(E, F0) = 0 at 3 s and at 2 s; F stops ("no measurable room on design data at 2 or 3 s").
  - `out\F_HORIZON_RULE_v01.json`: written 2026-11-19 23:40:04 EST, SHA-256 `b431314755deabc29439ec8f340f7905586641dbcb044e3dae202cb8d76340e2`.
  - Independent recount `recount\F_RECOUNT_HORIZON_v01.json`: 23:26:43 EST, `fe844ea15bfeb81900a81c7043a2ad6985ea3baa47e9811a001994823a57dbd3`.
  - Comparison `out\F_HORIZON_COMPARE_v01.json`: 23:46:41 EST, `c76ab34dda36e01556cbf774f2e494548c82a75e443ac2ec7814520c179f8d3b`; all agree.
- **Reason:** the mechanism check (`code\f14_room_mechanism_v01.py`, design split). Wrong go rises with the margin scale because the hard-brake fallback is struck from behind by replayed traffic, which does not react to the counterfactual brake.
- **The rule was chosen after seeing the design-split stop.** This is disclosed.
- **Val was unread when the choice was made.** At 23:52:08 EST `revision_v13\LOCK_A10_2.txt` did not exist, and F's cache had no `val` directory. Every F script refuses `val` until Lock 2 exists (`f_common_v01.require_split`).

## 2. Definition
The clearance of record is the minimum rectangle distance between the ego box and every truth box over frames 0..60 (3 s) or 0..40 (2 s), in the planner (route) frame; a row is safe when it is > 0 (W1). It changes in one respect only.

**Rule:** an (actor, frame) pair is dropped from the minimum when the actor's centre has a **negative longitudinal coordinate in the ego frame** at that frame. The clearance is the minimum rectangle distance over the remaining pairs, or +inf if none remain.

**Ego frame at frame f:** origin at the ego box's centre at f, x along the ego's heading at f, in the same planner frame as the clearance.
- **Rows** (the planner's 17 candidate motions; ego centre (S_r[f], 0), heading 0):
  x_rel = c_x(f) − S_r[f].
- **The ego's logged motion** (adapter check; ego centre (LX[f], LY[f]), heading LH[f] relative to the route):
  x_rel = cos(LH[f]) · (c_x(f) − LX[f]) + sin(LH[f]) · (c_y(f) − LY[f]).
- Here c(f) is the truth actor's centre at f in the planner frame.
- **Drop the pair when x_rel < 0** (strictly). A pair with x_rel = 0 is kept.

**Contact and distance readings coincide.** F's scoring uses the clearance only through "safe ⇔ clearance > 0": wrong go, the oracle row, and the safe set of caution.
- The rectangle distance is exactly 0 for touching or overlapping boxes (separating-axis test; `poly_dist`).
- So a row is unsafe under this rule exactly when some kept pair is in contact.
- This is the same classification as the contact-only reading: count a contact unless the actor's centre is behind the ego at that frame. The two readings differ only in the stored value of rows that are safe under both.

## 3. Scope
- **Applies to every clearance F computes:**
  - `clear` and `clear2` (rows) and `clear_logged` and `clear_logged2` (adapter check);
  - every split (train now; val after Lock 2);
  - so to every source (F0, E, E5, E5p, E5_x, N, N_IMM, TG and the partial oracles), every margin scale and both populations. The clearance does not depend on the source.
- **Unchanged:**
  - the planner library and its 17 rows;
  - the constraints and every source's critical scales (all actors, behind or not, as of record);
  - the selection rule and the fallback row;
  - the truth boxes and frames, W1, the 3 s / 2 s windows and the in-path rule;
  - δ = 0.05, every seed and draw (scene bootstrap default_rng(20261923), §2.6 seeds), the populations, the hypotheses and the horizon rule.

## 4. Implementation and checks
- **Code:**
  - `f03_adapter_v01.clearance_rows` gains a keyword `drop_behind` (default False = the rule of record, so nothing built before changes).
  - `code\f15_clear_v02.py` writes `cache\clear_v02\<split>\<scene>.npz` with the keys `clear`, `clear2`, `clear_logged`, `clear_logged2` (same shapes as the arrays).
  - Scoring reads its clearances from there; new outputs carry `_v02`.
  - The v01 arrays and outputs are kept unchanged as the pre-registered record.
- **Checks:**
  1. With `drop_behind=False` the new script reproduces the stored v01 clearances exactly (all train scenes).
  2. The pruned minimum equals the brute-force minimum over all kept pairs (sample).
  3. **Second-program adapter check of the clearance under this rule**, A10 §10.1(b): the same 20 design-split decisions as v01 (`notes\ADAPTER_CHECK_DECISIONS_v01.json`), all 17 rows' 3 s clearances within 1e-6 m. It is written by a different model from this text and the raw data.
  4. **Horizon rule (A10 §8.3) applied once** under this rule (`out\F_HORIZON_RULE_v02.json`), recounted by the independent second program, and compared (counts equal, values within 1e-9).
  5. **Descriptive (design split):** for F0 and E at g = 1, the number of evaluated decisions whose selected row is unsafe under the clearance of record and safe under this rule; also the number of (decision, row) pairs whose safety changes. N, N_IMM, TG and E5 are not evaluated on the design split (A10 §8.6).
- **Stop rule:** if the horizon rule finds no room at 3 s or 2 s under this rule, F stops with no further variant. The export then reports both outcomes.
- **Deadline:** if this rule's horizon result is not recounted by 20 Nov 14:00 EST, F freezes outcome (a): F.status = "no_room_design" with the stop sentence. `FREEZE_F.json` is written by 16:00 EST either way.

## 5. Disclosure (for package A: Table S4 and the response letter)
- The rule was chosen after the design-split stop was seen.
- The pre-registered result is printed beside the new one: D(E, F0) = 0 at 3 s and 2 s, with its intervals, from `F_HORIZON_RULE_v01.json`.
- The mechanism is the reason (`out\F_ROOM_MECHANISM_T1_train_v01.json`).
- Val was unread when the choice was made (§1 file times).
- **nuPlan:** its at-fault collision convention may be cited as comparable only after its exact rule has been checked in the nuplan-devkit source. F records that check in a separate note and does not describe the rule from memory.
- **CARLA:** whether the CARLA scenarios place actors behind the ego has not been checked from the scenario definitions. No statement about it is made here.
