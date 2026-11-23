# Package F: decision arrays (format), for the recount program

Written 19 Nov 2026 by session F (Claude Opus 5.5). The recount program may read these arrays (A10 §10.1(b): second programs "may share the scoring library, extracted arrays and resample draws") but not F's code.

## Files
- **Location:** `work\F_nuscenes\cache\arrays_<tracker>\<split>\<scene>.npz`, one per scene.
- **Trackers:**
  - `T1`: CANMOT, the tracker of N and its own F0 and E.
  - `IMM`: session B's B1, the tracker of N_IMM and its own F0_IMM and E_IMM.
- **Splits:** `train` (design) and `val` (held out; it exists only after Lock 2).

## Keys
One row per built decision, in time order.

**Decision state**

| Key | Shape | Meaning |
|---|---|---|
| `meta` | JSON string | scene, split, tracker, `desired` (the scene's desired speed, m/s), counts |
| `sweep`, `kf`, `now`, `age` | (n,) | the decision's LIDAR_TOP sweep index, keyframe index, time (s from the scene's first keyframe), age of the track states |
| `v0`, `des` | (n,) | ego speed and desired speed (m/s) |
| `evaluated` | (n,) bool | the 3 s truth window is complete |
| `evaluated2` | (n,) bool | the 2 s truth window is complete |
| `inpath` | (n,) bool | a truth vehicle at `now` with 0 < x ≤ 60 m and \|y\| ≤ 1.75 m in the route frame |

**Rows** (17 per decision, in the planner's cost order)

| Key | Shape | Meaning |
|---|---|---|
| `idx55` | (n,) | the fallback row (targets −5, −5) |
| `vbar` | (n, 17) | each row's mean speed over 3 s (m/s) |
| `clear` | (n, 17) | true clearance of each row over 3 s, in m; NaN when not evaluated |
| `clear2` | (n, 17) | true clearance over 2 s; NaN when not evaluated2 |

**Critical scales** (n, 17), each the largest g with g·s ≤ d² and d ≥ 0 on every constraint (+inf: always feasible; −inf: never)

| Key | Source | Margin variance s |
|---|---|---|
| `cF0` | F0 | the tracker's class average P̄ (from the train scenes) |
| `cN` | N | the track's own covariance |
| `cE` | E | squared true prediction error along the constraint normal |
| `cTG` | TG | (2 + row speed)², a constant time gap |

The keys with suffix `_2` (`cF0_2`, `cN_2`, `cE_2`, `cTG_2`) are the same over constraints at plan times ≤ 2 s.

**Diagnostics**
- `clear_logged`, `clear_logged2`: the ego's own logged motion's clearance (adapter check).
- `l_ego`, `n_act`, `n_truth`, `n_match`, `targets`, `v_raw`, `a_raw`.

## Tracker-independent keys
These are equal between the T1 and IMM files of a scene: `idx55`, `vbar`, `clear`, `clear2`, `evaluated`, `evaluated2`, `inpath`, `v0`, `des`.

## Scoring conventions
These are as of record (optA_lib_v02 and the v12 gridless code).
- **Run unit:** the scene. Scenes are ordered by sorted scene name.
- **Bootstrap draw:**
  - Primary: `numpy.random.default_rng(20261923).integers(0, n_scenes, (20000, n_scenes))`, turned into per-scene counts.
  - Double bootstrap: outer `default_rng(20261912).integers(0, n, (2000, n))`; inner one stream `default_rng(20261913)` drawing `integers(0, n, (1000, n))` for each outer sample in order, indexing that outer sample's scene list. The second inner stream is `default_rng(20261914)`. The Monte Carlo SD uses `default_rng(20261920).integers(0, 2000, (2000, 2000))`.
- **Scoring:** 3 s commitment (W1: a row is safe when its clearance is > 0).
  - Caution: (mean speed of the first safe row in cost order − mean speed of the selected row) / desired, over selections that are safe.
  - Wrong go: the selected row is not safe.
  - Selection at margin scale g: the first row with critical scale ≥ g; the fallback row if none.
- **Populations:**
  - primary: all evaluated decisions;
  - secondary: evaluated decisions with `inpath`.
- **E5_IMM:** built per A10 §2.2 on the IMM files of the scored (val) set: m_x and A_x from √(cF0/cN) at rows with finite positive values of both; u_i from √(cF0/cE).

## Added 20 Nov 2026: clearances under the departure (`notes/F_DEPARTURE_CLEARANCE_v01.md`)
- **Files:** `work\F_nuscenes\cache\clear_v02\<split>\<scene>.npz` (`code\f15_clear_v02.py`), one per scene.
- **Keys:** `sweep`, `clear` (n,17), `clear2` (n,17), `clear_logged`, `clear_logged2`, `meta` (checks and descriptive counts).
- **Same decision order as the arrays:** `sweep` equals the arrays' `sweep`, and the NaN pattern equals the arrays' `clear` / `clear2`.
- **Rule:** an (actor, frame) pair is dropped from the minimum when the actor's centre has a negative longitudinal coordinate in the ego frame at that frame. Everything else is as above.
- **Scoring in force** reads `clear` / `clear2` from these files instead of from the arrays. The arrays' own `clear` / `clear2` are the clearance of record (the pre-registered outcome).
