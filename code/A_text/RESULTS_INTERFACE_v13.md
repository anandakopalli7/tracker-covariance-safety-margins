# RESULTS INTERFACE v13: what package A reads from packages B-F

Written by `work\A_text\build\make_interface_v13.py` (session A) from the text itself: every value the v13 manuscript or supplement can print, under any outcome branch. Regenerated whenever the text changes.

## 1. Files

- Each package writes **one export**, `work\<folder>\out\A_EXPORT_<pkg>.json`, and its second program writes `A_RECOUNT_<pkg>.json` beside it with the same keys (A10 §10.1). Folders: B -> `B_retrack`, C and D -> `CD_capture`, E -> `E_closedloop`, F -> `F_nuscenes`.
- Format: `{"package": "C", "written": "<ISO time>", "program": "<script>", "program_sha256": "...", "lock2_sha256": "...", "values": {<flat key>: <value>, ...}}`.
- Values are **unrounded** numbers (A rounds), `[lo, hi]` lists for intervals (key suffix `.ci`), booleans, or the status strings named below. Shares are fractions of the room (0.831, not 83.1). Rooms are percentage points. Shares printed as percentages (format "%") are fractions in [0, 1].
- For every share `X` that A prints, also export `X.dec` and `X.dec.ci` (decision-equivalents): Table II prints them instead of shares where the partial oracles do not grade (A10 §5.7).
- Intervals are at the level the hypothesis's calibration selected (A10 §2.6); export the level as `X.level` and `X.cal` = "nominal95" | "calibrated" | "nominal99".
- If a package names a value differently or another package computes it, add a line to `work\A_text\gen\rename_v13.json` (`{"B:B.IMM.RR": "C:LB.IMM.r"}`) instead of renaming. Ask session A if unsure.
- A recomputes every hypothesis status from the interval ends (gen\outcomes_v13.py) and stops on a mismatch with a status a package exports.

## 2. Keys read for statuses (not printed, or printed through wording)

- **B**: B.CV.as_room, B.CV2.as_room, B.CA.as_room, B.CV.RR_CK3, B.CV2.RR_CK3, B.CA.RR_CK3 (the B3/B4 rule); B7.2.0.as_room, B7.10.0.1.as_room (the B7 rate rule; "B7.<rate Hz>.<latency s>.<quantity>"); B7.<r>.<L>.RR_N.ci for every rate and latency (the B7 rule on N); B7.identity: "pass" | "fail"; B.tuning, B7.rule_rate, B7.rule_N (optional status); B.ca_window (bool: the CA filter reached the NIS window [1.8, 2.2])
- **C**: LB.R.nonpos_share (share of resamples with D_gl <= 0); LB.IMM.within5; CI.Y.within5; CI.den0.dec; CI.Y.R.dec; LB.T1.evaluable / LB.T2.evaluable / LB.T3.evaluable (bool); TRANSFER.structured (preferred): {"N_inside_delta_all_sets": bool, "orderings": [["CK3", "AM"], ...] with source codes CK3, AM, TG, NA, N, "sets": ["tuning", "old", "fresh", "F"]}; A writes the English (A10 §5.6); LB.H0 ... LB.H5, CI.K0 ... CI.K2 (optional: your own status; A recomputes it from the interval ends and stops on a mismatch)
- **D**: D1.<v>.CK3.dcau.ci, D1.<v>.CK3.dwg.ci, D1.<v>.PS.dcau.ci, D1.<v>.PS.dwg.ci for v in const, mild, stopgo (points); D1.<v>.DH1 / D1.<v>.DH2 (optional status)
- **E**: E.status: "ran" | "stopped_brake" | "stopped_other"; E2.low_power (bool); E3.<arm>.<lev>.dc.ci, E3.<arm>.<lev>.dt.ci for arm in N, CK3, TG, PS, NIMM and lev in lo, hi; E3b.<v>.<arm>.dc.ci, E3b.<v>.<arm>.dt.ci for v in const, mild, stopgo and arm in N, CK3, PS, TG; EH1, EH2, EH3 (optional status); E3.NIMM.dropped (bool: true if the IMM pair was not run in closed loop)
- **F**: F.status: "heldout" | "design_only" | "omitted" | "no_room_design"; F.provenance: "confirmed" | "unconfirmed"; F.R.nonpos_share; F.IMM.within5; F.H0, F.H1, F.H2 (optional status); F.RR_CK3, F.RR_AM and their intervals: not read (coordinator decision of 19 Nov 2026, 19:25 EST; the text prints "not computed" and records the departure; F may still list it in its own deviations)

## 3. Keys printed, by package

### B (89 keys; 66 required by the main text or the response letter)

| Key | Printed as | Value type | Where |
|---|---|---|---|
| `B.AQ.RR` | sh3 | number, share of the room | main (required) |
| `B.AQ.RR.ci` | ci3 | [lo, hi] | main (required) |
| `B.AQ.RR_CK3` | sh3 | number, share of the room | main (required) |
| `B.AQ.c` | sh3 | number, share of the room | main (required) |
| `B.AQ.c.ci` | ci3 | [lo, hi] | main (required) |
| `B.AQ.lag` | f2 | number | main (required) |
| `B.AQ.room_brk` | pp | number, percentage points | main (required) |
| `B.AQ.room_pre` | pp | number, percentage points | main (required) |
| `B.AQ.room_stop` | pp | number, percentage points | main (required) |
| `B.AQ.within5` | pct1 | number in [0, 1], printed as % | main (required) |
| `B.CA.RR` | sh3 | number, share of the room | main (required) |
| `B.CA.RR.ci` | ci3 | [lo, hi] | main (required) |
| `B.CA.RR_CK3` | sh3 | number, share of the room | main (required) |
| `B.CA.as_room` | dec1 | number, decision-equivalents | main (required) |
| `B.CA.c` | sh3 | number, share of the room | main (required) |
| `B.CA.c.ci` | ci3 | [lo, hi] | main (required) |
| `B.CA.lag` | f2 | number | main (required) |
| `B.CA.room_brk` | pp | number, percentage points | main (required) |
| `B.CA.room_pre` | pp | number, percentage points | main (required) |
| `B.CA.room_stop` | pp | number, percentage points | main (required) |
| `B.CA.within5` | pct1 | number in [0, 1], printed as % | main (required) |
| `B.CV.RR` | sh3 | number, share of the room | main (required) |
| `B.CV.RR.ci` | ci3 | [lo, hi] | main (required) |
| `B.CV.RR_CK3` | sh3 | number, share of the room | main (required) |
| `B.CV.as_room` | dec1 | number, decision-equivalents | main (required) |
| `B.CV.c` | sh3 | number, share of the room | main (required) |
| `B.CV.c.ci` | ci3 | [lo, hi] | main (required) |
| `B.CV.lag` | f2 | number | main (required) |
| `B.CV.room_brk` | pp | number, percentage points | main (required) |
| `B.CV.room_pre` | pp | number, percentage points | main (required) |
| `B.CV.room_stop` | pp | number, percentage points | main (required) |
| `B.CV.within5` | pct1 | number in [0, 1], printed as % | main (required) |
| `B.CV2.RR` | sh3 | number, share of the room | main (required) |
| `B.CV2.RR.ci` | ci3 | [lo, hi] | main (required) |
| `B.CV2.RR_CK3` | sh3 | number, share of the room | main (required) |
| `B.CV2.as_room` | dec1 | number, decision-equivalents | main (required) |
| `B.CV2.c` | sh3 | number, share of the room | main (required) |
| `B.CV2.c.ci` | ci3 | [lo, hi] | main (required) |
| `B.CV2.lag` | f2 | number | main (required) |
| `B.CV2.room_brk` | pp | number, percentage points | main (required) |
| `B.CV2.room_pre` | pp | number, percentage points | main (required) |
| `B.CV2.room_stop` | pp | number, percentage points | main (required) |
| `B.CV2.within5` | pct1 | number in [0, 1], printed as % | main (required) |
| `B.IMM.RR` | sh3 | number, share of the room | main (required) |
| `B.IMM.RR.ci` | ci3 | [lo, hi] | main (required) |
| `B.IMM.RR_CK3` | sh3 | number, share of the room | main (required) |
| `B.IMM.c` | sh3 | number, share of the room | main (required) |
| `B.IMM.c.ci` | ci3 | [lo, hi] | main (required) |
| `B.IMM.lag` | f2 | number | main (required) |
| `B.IMM.room_brk` | pp | number, percentage points | main (required) |
| `B.IMM.room_pre` | pp | number, percentage points | main (required) |
| `B.IMM.room_stop` | pp | number, percentage points | main (required) |
| `B.IMM.within5` | pct1 | number in [0, 1], printed as % | main (required) |
| `LB.DS.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.DS.rel` | sh3 | number, share of the room | main (required) |
| `LB.DS.rel.ci` | ci3 | [lo, hi] | main (required) |
| `LB.REL_CK3` | pct0 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `LB.REL_F0` | pct0 | number in [0, 1], printed as % | main (required) |
| `LB.REL_N` | pct0 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `LB.RS075.rel` | sh3 | number, share of the room | main (required) |
| `LB.RS075.rel.ci` | ci3 | [lo, hi] | main (required) |
| `LB.T.relmax` | pct0 | number in [0, 1], printed as % | main (required) |
| `LB.T.relmax` | sh3 | number, share of the room | main (required) |
| `LB.T.relmin` | pct0 | number in [0, 1], printed as % | main (required) |
| `LB.T.relmin` | sh3 | number, share of the room | main (required) |
| `LB.T1.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.T1.range` | str | string or number | supplement (n.c. if absent) |
| `LB.T1.rel` | sh3 | number, share of the room | main (required) |
| `LB.T2.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.T2.range` | str | string or number | supplement (n.c. if absent) |
| `LB.T2.rel` | sh3 | number, share of the room | main (required) |
| `LB.T3.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.T3.range` | str | string or number | supplement (n.c. if absent) |
| `LB.T3.rel` | sh3 | number, share of the room | main (required) |
| `TU.R` | pp | number, percentage points | main (required) |
| `TU.R.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `TU.RR_AM` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `TU.RR_AM.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `TU.RR_CK3` | sh3 | number, share of the room | main (required) |
| `TU.RR_CK3.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `TU.RR_N` | sh4 | number, share of the room | main (required) |
| `TU.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `TU.RR_NA` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `TU.RR_NA.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `TU.RR_TG` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `TU.RR_TG.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `TU.R_brk` | pp | number, percentage points | supplement (n.c. if absent) |
| `TU.R_pre` | pp | number, percentage points | supplement (n.c. if absent) |
| `TU.R_stop` | pp | number, percentage points | supplement (n.c. if absent) |

### C (364 keys; 76 required by the main text or the response letter)

| Key | Printed as | Value type | Where |
|---|---|---|---|
| `B7.10.0.1.R` | pp | number, percentage points | main (required) |
| `B7.10.0.1.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7.10.0.1.RR_N` | sh4 | number, share of the room | main (required) |
| `B7.10.0.1.RR_N.ci` | ci4 | [lo, hi] | main (required) |
| `B7.10.0.1.as_room` | dec1 | number, decision-equivalents | main (required) |
| `B7.10.0.1.lag` | f2 | number | supplement (n.c. if absent) |
| `B7.10.0.2.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7.10.0.2.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7.10.0.2.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7.10.0.2.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7.10.0.2.as_room` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `B7.10.0.2.lag` | f2 | number | supplement (n.c. if absent) |
| `B7.10.0.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7.10.0.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7.10.0.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7.10.0.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7.10.0.as_room` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `B7.10.0.lag` | f2 | number | supplement (n.c. if absent) |
| `B7.2.0.1.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7.2.0.1.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7.2.0.1.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7.2.0.1.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7.2.0.1.as_room` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `B7.2.0.1.lag` | f2 | number | supplement (n.c. if absent) |
| `B7.2.0.R` | pp | number, percentage points | main (required) |
| `B7.2.0.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7.2.0.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7.2.0.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7.2.0.as_room` | dec1 | number, decision-equivalents | main (required) |
| `B7.2.0.lag` | f2 | number | supplement (n.c. if absent) |
| `B7.5.0.1.R` | pp | number, percentage points | main (required) |
| `B7.5.0.1.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7.5.0.1.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7.5.0.1.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7.5.0.1.as_room` | dec1 | number, decision-equivalents | main (required) |
| `B7.5.0.1.lag` | f2 | number | supplement (n.c. if absent) |
| `B7.5.0.2.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7.5.0.2.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7.5.0.2.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7.5.0.2.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7.5.0.2.as_room` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `B7.5.0.2.lag` | f2 | number | supplement (n.c. if absent) |
| `B7.5.0.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7.5.0.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7.5.0.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7.5.0.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7.5.0.as_room` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `B7.5.0.lag` | f2 | number | supplement (n.c. if absent) |
| `B7.identity` | str | string or number | supplement (n.c. if absent) |
| `B7CI.10.0.1.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7CI.10.0.1.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.10.0.1.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.10.0.1.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7CI.10.0.2.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7CI.10.0.2.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.10.0.2.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.10.0.2.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7CI.10.0.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7CI.10.0.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.10.0.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.10.0.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7CI.2.0.1.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7CI.2.0.1.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.2.0.1.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.2.0.1.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7CI.2.0.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7CI.2.0.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.2.0.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.2.0.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7CI.5.0.1.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7CI.5.0.1.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.5.0.1.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.5.0.1.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7CI.5.0.2.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7CI.5.0.2.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.5.0.2.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.5.0.2.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `B7CI.5.0.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `B7CI.5.0.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.5.0.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `B7CI.5.0.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `CI.PO25` | sh3 | number, share of the room | main (required) |
| `CI.PO50` | sh3 | number, share of the room | main (required) |
| `CI.PO75` | sh3 | number, share of the room | main (required) |
| `CI.R` | pp | number, percentage points | main (required) |
| `CI.R.ci` | ci2 | [lo, hi] | main (required) |
| `CI.RR_CK3` | sh3 | number, share of the room | main (required) |
| `CI.RR_CK3.ci` | ci3 | [lo, hi] | main (required) |
| `CI.RR_E5` | sh3 | number, share of the room | main (required) |
| `CI.RR_E5.ci` | ci3 | [lo, hi] | main (required) |
| `CI.RR_E5mP` | sh3 | number, share of the room | main (required) |
| `CI.RR_E5mP.ci` | ci3 | [lo, hi] | main (required) |
| `CI.RR_N` | sh4 | number, share of the room | main (required) |
| `CI.RR_N.ci` | ci4 | [lo, hi] | main (required) |
| `CI.RR_N.dec` | dec1 | number, decision-equivalents | main (required) |
| `CI.RR_N.dec.ci` | ci1 | [lo, hi] | main (required) |
| `CI.Y.R.dec` | dec1 | number, decision-equivalents | main (required) |
| `CI.Y.c` | sh3 | number, share of the room | main (required) |
| `CI.Y.c.ci` | ci3 | [lo, hi] | main (required) |
| `CI.Y.eff` | sh3 | number, share of the room | main (required) |
| `CI.Y.eff.ci` | ci3 | [lo, hi] | main (required) |
| `CI.Y.n_dec` | int | integer count | main (required) |
| `CI.Y.r` | sh3 | number, share of the room | main (required) |
| `CI.Y.r.ci` | ci3 | [lo, hi] | main (required) |
| `CI.Y.within5` | pct1 | number in [0, 1], printed as % | main (required) |
| `CI.age0.R.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `CI.age0.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `CI.age0.n_dec` | int | integer count | supplement (n.c. if absent) |
| `CI.age0.within5` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `CI.age1.R.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `CI.age1.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `CI.age1.n_dec` | int | integer count | supplement (n.c. if absent) |
| `CI.age1.within5` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `CI.age4.R.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `CI.age4.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `CI.age4.n_dec` | int | integer count | supplement (n.c. if absent) |
| `CI.age4.within5` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `CI.den0.dec` | dec1 | number, decision-equivalents | main (required) |
| `CI.n_contact` | int | integer count | supplement (n.c. if absent) |
| `CI.n_dec` | int | integer count | main (required) |
| `CI.n_events` | int | integer count | main (required) |
| `CI.n_replaced` | int | integer count | supplement (n.c. if absent) |
| `CI.n_runs` | int | integer count | main (required) |
| `CI.untr.R.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `CI.untr.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `CI.untr.n_dec` | int | integer count | supplement (n.c. if absent) |
| `CI.untr.within5` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `HAND.status` | str | string or number | supplement (n.c. if absent) |
| `LB.IMM.c` | sh3 | number, share of the room | main (required) |
| `LB.IMM.c.ci` | ci3 | [lo, hi] | main (required) |
| `LB.IMM.c.dec` | dec1 | number, decision-equivalents | main (required) |
| `LB.IMM.c.dec.ci` | ci1 | [lo, hi] | main (required) |
| `LB.IMM.eff` | sh3 | number, share of the room | main (required) |
| `LB.IMM.eff.ci` | ci3 | [lo, hi] | main (required) |
| `LB.IMM.r` | sh3 | number, share of the room | main (required) |
| `LB.IMM.r.ci` | ci3 | [lo, hi] | main (required) |
| `LB.IMM.r.dec` | dec1 | number, decision-equivalents | main (required) |
| `LB.IMM.r.dec.ci` | ci1 | [lo, hi] | main (required) |
| `LB.IMM.within5` | pct1 | number in [0, 1], printed as % | main (required) |
| `LB.PO25` | sh3 | number, share of the room | main (required) |
| `LB.PO50` | sh3 | number, share of the room | main (required) |
| `LB.PO75` | sh3 | number, share of the room | main (required) |
| `LB.PS.like` | sh3 | number, share of the room | main (required) |
| `LB.PS.like.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.PS.rec` | sh3 | number, share of the room | main (required) |
| `LB.PS.rec.ci` | ci3 | [lo, hi] | main (required) |
| `LB.PS.rec.dec` | dec1 | number, decision-equivalents | main (required) |
| `LB.PS.rec.dec.ci` | ci1 | [lo, hi] | main (required) |
| `LB.PS.single` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.PS.single.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.PS.thr05` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.PS.thr05.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.PS.thr20` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.PS.thr20.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.PS.truth` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.PS.truth.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.R` | pp | number, percentage points | main (required) |
| `LB.R.ci` | ci2 | [lo, hi] | main (required) |
| `LB.R.dec` | dec1 | number, decision-equivalents | main (required) |
| `LB.RR_CK3` | sh3 | number, share of the room | main (required) |
| `LB.RR_CK3.ci` | ci3 | [lo, hi] | main (required) |
| `LB.RR_CK3.dec` | dec1 | number, decision-equivalents | main (required) |
| `LB.RR_CK3.dec.ci` | ci1 | [lo, hi] | main (required) |
| `LB.RR_E5` | sh3 | number, share of the room | main (required) |
| `LB.RR_E5.ci` | ci3 | [lo, hi] | main (required) |
| `LB.RR_E5.dec` | dec1 | number, decision-equivalents | main (required) |
| `LB.RR_E5.dec.ci` | ci1 | [lo, hi] | main (required) |
| `LB.RR_E5mP` | sh3 | number, share of the room | main (required) |
| `LB.RR_E5mP.ci` | ci3 | [lo, hi] | main (required) |
| `LB.RR_E5mP.dec` | dec1 | number, decision-equivalents | main (required) |
| `LB.RR_E5mP.dec.ci` | ci1 | [lo, hi] | main (required) |
| `LB.RR_N` | sh4 | number, share of the room | main (required) |
| `LB.RR_N.ci` | ci4 | [lo, hi] | main (required) |
| `LB.RR_N.dec` | dec1 | number, decision-equivalents | main (required) |
| `LB.RR_N.dec.ci` | ci1 | [lo, hi] | main (required) |
| `LB.RS.0.5.6.RR0_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.5.6.RR0_N` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.5.6.RR0_N.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.RS.0.5.6.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.RS.0.5.6.rel` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.5.6.rel.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.RS.0.75.4.RR0_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.75.4.RR0_N` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.75.4.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.RS.0.75.4.rel` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.75.5.RR0_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.75.5.RR0_N` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.75.5.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.RS.0.75.5.rel` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.75.6.RR0_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.75.6.RR0_N` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.75.6.RR0_N.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.RS.0.75.6.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.RS.0.75.7.6.RR0_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.75.7.6.RR0_N` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.0.75.7.6.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.RS.0.75.7.6.rel` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.0.6.RR0_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.0.6.RR0_N` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.0.6.RR0_N.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.RS.1.0.6.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.RS.1.0.6.rel` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.0.6.rel.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.RS.1.25.6.RR0_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.25.6.RR0_N` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.25.6.RR0_N.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.RS.1.25.6.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.RS.1.25.6.rel` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.25.6.rel.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.RS.1.5.6.RR0_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.5.6.RR0_N` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.5.6.RR0_N.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.RS.1.5.6.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.RS.1.5.6.rel` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.5.6.rel.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.RS.1.8.6.RR0_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.8.6.RR0_N` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.8.6.RR0_N.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.RS.1.8.6.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.RS.1.8.6.rel` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.RS.1.8.6.rel.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.T0.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.T0.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.T1.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.T1.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.T10.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.T10.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.T2.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.T2.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.T20.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.T20.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.T5.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.T5.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.all.PO25` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.all.PO50` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.all.PO75` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.all.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.all.R.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `LB.all.RR_AM` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.all.RR_AM.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.all.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.all.RR_CK3.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.all.RR_E5` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.all.RR_E5.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.all.RR_IMM` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.all.RR_IMM.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.all.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.all.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `LB.all.RR_NA` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.all.RR_NA.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.all.RR_Q` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.all.RR_Q.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `LB.all.RR_TG` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.all.RR_TG.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.all.n_dec` | int | integer count | supplement (n.c. if absent) |
| `LB.brk.PO25` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.brk.PO50` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.brk.PO75` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.brk.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.brk.R.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `LB.brk.RR_AM` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.brk.RR_AM.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.brk.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.brk.RR_CK3.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.brk.RR_E5` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.brk.RR_E5.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.brk.RR_IMM` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.brk.RR_IMM.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.brk.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.brk.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `LB.brk.RR_NA` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.brk.RR_NA.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.brk.RR_Q` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.brk.RR_Q.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `LB.brk.RR_TG` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.brk.RR_TG.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.brk.n_dec` | int | integer count | supplement (n.c. if absent) |
| `LB.cap10.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.cap15.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.cap5.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.cut5.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.cut5.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.gap2.RR0_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.gap2.RR0_N` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.gap2.den0.dec` | dec1 | number, decision-equivalents | supplement (n.c. if absent) |
| `LB.grid.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.grid.RR_NmP` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.grid.RR_P` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.hull.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.hull.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.hull.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.mov.PO25` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.mov.PO50` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.mov.PO75` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.mov.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.mov.R.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `LB.mov.RR_AM` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.mov.RR_AM.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.mov.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.mov.RR_CK3.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.mov.RR_E5` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.mov.RR_E5.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.mov.RR_IMM` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.mov.RR_IMM.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.mov.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.mov.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `LB.mov.RR_NA` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.mov.RR_NA.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.mov.RR_Q` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.mov.RR_Q.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `LB.mov.RR_TG` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.mov.RR_TG.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.mov.n_dec` | int | integer count | supplement (n.c. if absent) |
| `LB.n_contact` | int | integer count | supplement (n.c. if absent) |
| `LB.n_dec` | int | integer count | main (required) |
| `LB.n_replaced` | int | integer count | supplement (n.c. if absent) |
| `LB.n_runs` | int | integer count | main (required) |
| `LB.pre.PO25` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.pre.PO50` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.pre.PO75` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.pre.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.pre.R.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `LB.pre.RR_AM` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.pre.RR_AM.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.pre.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.pre.RR_CK3.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.pre.RR_E5` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.pre.RR_E5.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.pre.RR_IMM` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.pre.RR_IMM.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.pre.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.pre.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `LB.pre.RR_NA` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.pre.RR_NA.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.pre.RR_Q` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.pre.RR_Q.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `LB.pre.RR_TG` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.pre.RR_TG.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.pre.n_dec` | int | integer count | supplement (n.c. if absent) |
| `LB.signed.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.signed.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.signed.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.stop.PO25` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.stop.PO50` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.stop.PO75` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.stop.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `LB.stop.R.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `LB.stop.RR_AM` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.stop.RR_AM.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.stop.RR_CK3` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.stop.RR_CK3.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.stop.RR_E5` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.stop.RR_E5.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.stop.RR_IMM` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.stop.RR_IMM.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.stop.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.stop.RR_N.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `LB.stop.RR_NA` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.stop.RR_NA.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.stop.RR_Q` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `LB.stop.RR_Q.ci` | ci4 | [lo, hi] | supplement (n.c. if absent) |
| `LB.stop.RR_TG` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `LB.stop.RR_TG.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `LB.stop.n_dec` | int | integer count | supplement (n.c. if absent) |

### D (84 keys; 13 required by the main text or the response letter)

| Key | Printed as | Value type | Where |
|---|---|---|---|
| `D1.const.CK3.dcau` | f1 | number | main (required) |
| `D1.const.CK3.dcau.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.const.CK3.dwg` | f1 | number | main (required) |
| `D1.const.CK3.dwg.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.const.N.dcau` | f1 | number | supplement (n.c. if absent) |
| `D1.const.N.dcau.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.const.N.dwg` | f1 | number | supplement (n.c. if absent) |
| `D1.const.N.dwg.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.const.PS.dcau` | f1 | number | main (required) |
| `D1.const.PS.dcau.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.const.PS.dwg` | f1 | number | main (required) |
| `D1.const.PS.dwg.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.const.TG.dcau` | f1 | number | supplement (n.c. if absent) |
| `D1.const.TG.dcau.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.const.TG.dwg` | f1 | number | supplement (n.c. if absent) |
| `D1.const.TG.dwg.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.mild.CK3.dcau` | f1 | number | main (required) |
| `D1.mild.CK3.dcau.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.mild.CK3.dwg` | f1 | number | main (required) |
| `D1.mild.CK3.dwg.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.mild.N.dcau` | f1 | number | supplement (n.c. if absent) |
| `D1.mild.N.dcau.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.mild.N.dwg` | f1 | number | supplement (n.c. if absent) |
| `D1.mild.N.dwg.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.mild.PS.dcau` | f1 | number | main (required) |
| `D1.mild.PS.dcau.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.mild.PS.dwg` | f1 | number | main (required) |
| `D1.mild.PS.dwg.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.mild.TG.dcau` | f1 | number | supplement (n.c. if absent) |
| `D1.mild.TG.dcau.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.mild.TG.dwg` | f1 | number | supplement (n.c. if absent) |
| `D1.mild.TG.dwg.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.n_contact` | int | integer count | supplement (n.c. if absent) |
| `D1.n_dec` | int | integer count | supplement (n.c. if absent) |
| `D1.n_replaced` | int | integer count | supplement (n.c. if absent) |
| `D1.n_runs` | int | integer count | main (required) |
| `D1.stopgo.CK3.dcau` | f1 | number | main (required) |
| `D1.stopgo.CK3.dcau.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.stopgo.CK3.dwg` | f1 | number | main (required) |
| `D1.stopgo.CK3.dwg.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.stopgo.N.dcau` | f1 | number | supplement (n.c. if absent) |
| `D1.stopgo.N.dcau.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.stopgo.N.dwg` | f1 | number | supplement (n.c. if absent) |
| `D1.stopgo.N.dwg.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.stopgo.PS.dcau` | f1 | number | main (required) |
| `D1.stopgo.PS.dcau.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.stopgo.PS.dwg` | f1 | number | main (required) |
| `D1.stopgo.PS.dwg.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.stopgo.TG.dcau` | f1 | number | supplement (n.c. if absent) |
| `D1.stopgo.TG.dcau.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D1.stopgo.TG.dwg` | f1 | number | supplement (n.c. if absent) |
| `D1.stopgo.TG.dwg.ci` | ci1 | [lo, hi] | supplement (n.c. if absent) |
| `D2.CK3.c2.rs.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.CK3.c2.rs.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.CK3.c2.w3.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.CK3.c2.w3.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.CK3.c5.rs.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.CK3.c5.rs.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.CK3.c5.w3.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.CK3.c5.w3.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.F0.c2.rs.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.F0.c2.rs.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.F0.c2.w3.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.F0.c2.w3.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.F0.c5.rs.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.F0.c5.rs.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.F0.c5.w3.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.F0.c5.w3.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.N.c2.rs.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.N.c2.rs.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.N.c2.w3.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.N.c2.w3.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.N.c5.rs.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.N.c5.rs.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.N.c5.w3.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.N.c5.w3.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.TG.c2.rs.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.TG.c2.rs.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.TG.c2.w3.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.TG.c2.w3.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.TG.c5.rs.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.TG.c5.rs.vclose` | f1 | number | supplement (n.c. if absent) |
| `D2.TG.c5.w3.runs` | int | integer count | supplement (n.c. if absent) |
| `D2.TG.c5.w3.vclose` | f1 | number | supplement (n.c. if absent) |

### E (431 keys; 80 required by the main text or the response letter)

| Key | Printed as | Value type | Where |
|---|---|---|---|
| `E1.attempts` | int | integer count | supplement (n.c. if absent) |
| `E1.maxerr` | pct0 | number in [0, 1], printed as % | main (required) |
| `E1.v10.dist` | f2 | number | main (required) |
| `E1.v10.err` | pct0 | number in [0, 1], printed as % | main (required) |
| `E1.v10.model` | f2 | number | main (required) |
| `E1.v15.dist` | f2 | number | main (required) |
| `E1.v15.err` | pct0 | number in [0, 1], printed as % | main (required) |
| `E1.v15.model` | f2 | number | main (required) |
| `E1.v5.dist` | f2 | number | main (required) |
| `E1.v5.err` | pct0 | number in [0, 1], printed as % | main (required) |
| `E1.v5.model` | f2 | number | main (required) |
| `E2.g0.contact` | pct0 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E2.g0_25.contact` | pct0 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E2.g1.contact` | pct0 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E2.g16.contact` | pct0 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E2.g4.contact` | pct0 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E2.g64.contact` | pct0 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E2.g_hi` | str | string or number | supplement (n.c. if absent) |
| `E2.g_lo` | str | string or number | supplement (n.c. if absent) |
| `E3.CK3.hi.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.CK3.hi.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3.CK3.hi.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3.CK3.hi.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.hi.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.CK3.hi.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.hi.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.CK3.hi.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.hi.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.CK3.hi.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.hi.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.CK3.hi.dc` | f2 | number | main (required) |
| `E3.CK3.hi.dc.ci` | ci2 | [lo, hi] | main (required) |
| `E3.CK3.hi.dt` | f2 | number | main (required) |
| `E3.CK3.hi.dt.ci` | ci2 | [lo, hi] | main (required) |
| `E3.CK3.hi.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.CK3.hi.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.hi.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.hi.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.hi.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.hi.vimp` | f1 | number | main (required) |
| `E3.CK3.lo.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.CK3.lo.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3.CK3.lo.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3.CK3.lo.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.lo.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.CK3.lo.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.lo.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.CK3.lo.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.lo.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.CK3.lo.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.lo.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.CK3.lo.dc` | f2 | number | main (required) |
| `E3.CK3.lo.dc.ci` | ci2 | [lo, hi] | main (required) |
| `E3.CK3.lo.dt` | f2 | number | main (required) |
| `E3.CK3.lo.dt.ci` | ci2 | [lo, hi] | main (required) |
| `E3.CK3.lo.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.CK3.lo.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.lo.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.lo.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.lo.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.CK3.lo.vimp` | f1 | number | main (required) |
| `E3.F0.hi.caution` | f2 | number | main (required) |
| `E3.F0.hi.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.F0.hi.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.F0.hi.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.F0.hi.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.F0.hi.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.F0.hi.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.F0.hi.vimp` | f1 | number | main (required) |
| `E3.F0.lo.caution` | f2 | number | main (required) |
| `E3.F0.lo.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.F0.lo.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.F0.lo.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.F0.lo.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.F0.lo.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.F0.lo.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.F0.lo.vimp` | f1 | number | main (required) |
| `E3.F0IMM.hi.contact` | pct0 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.F0IMM.hi.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.F0IMM.hi.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.F0IMM.hi.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.F0IMM.hi.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.F0IMM.hi.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.F0IMM.hi.vimp` | f1 | number | supplement (n.c. if absent) |
| `E3.F0IMM.lo.contact` | pct0 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.F0IMM.lo.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.F0IMM.lo.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.F0IMM.lo.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.F0IMM.lo.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.F0IMM.lo.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.F0IMM.lo.vimp` | f1 | number | supplement (n.c. if absent) |
| `E3.N.hi.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.N.hi.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3.N.hi.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3.N.hi.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.N.hi.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.N.hi.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.N.hi.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.N.hi.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.N.hi.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.N.hi.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3.N.hi.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.N.hi.dc` | f2 | number | main (required) |
| `E3.N.hi.dc.ci` | ci2 | [lo, hi] | main (required) |
| `E3.N.hi.dt` | f2 | number | main (required) |
| `E3.N.hi.dt.ci` | ci2 | [lo, hi] | main (required) |
| `E3.N.hi.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.N.hi.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.N.hi.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.N.hi.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.N.hi.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.N.hi.vimp` | f1 | number | main (required) |
| `E3.N.lo.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.N.lo.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3.N.lo.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3.N.lo.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.N.lo.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.N.lo.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.N.lo.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.N.lo.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.N.lo.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.N.lo.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3.N.lo.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.N.lo.dc` | f2 | number | main (required) |
| `E3.N.lo.dc.ci` | ci2 | [lo, hi] | main (required) |
| `E3.N.lo.dt` | f2 | number | main (required) |
| `E3.N.lo.dt.ci` | ci2 | [lo, hi] | main (required) |
| `E3.N.lo.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.N.lo.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.N.lo.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.N.lo.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.N.lo.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.N.lo.vimp` | f1 | number | main (required) |
| `E3.NIMM.hi.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.NIMM.hi.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3.NIMM.hi.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3.NIMM.hi.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.hi.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.NIMM.hi.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.hi.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.NIMM.hi.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.hi.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.NIMM.hi.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.hi.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.NIMM.hi.dc` | f2 | number | main (required) |
| `E3.NIMM.hi.dc.ci` | ci2 | [lo, hi] | main (required) |
| `E3.NIMM.hi.dt` | f2 | number | main (required) |
| `E3.NIMM.hi.dt.ci` | ci2 | [lo, hi] | main (required) |
| `E3.NIMM.hi.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.NIMM.hi.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.hi.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.hi.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.hi.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.hi.vimp` | f1 | number | main (required) |
| `E3.NIMM.lo.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.NIMM.lo.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3.NIMM.lo.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3.NIMM.lo.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.lo.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.NIMM.lo.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.lo.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.NIMM.lo.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.lo.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.NIMM.lo.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.lo.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.NIMM.lo.dc` | f2 | number | main (required) |
| `E3.NIMM.lo.dc.ci` | ci2 | [lo, hi] | main (required) |
| `E3.NIMM.lo.dt` | f2 | number | main (required) |
| `E3.NIMM.lo.dt.ci` | ci2 | [lo, hi] | main (required) |
| `E3.NIMM.lo.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.NIMM.lo.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.lo.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.lo.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.lo.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.NIMM.lo.vimp` | f1 | number | main (required) |
| `E3.PS.hi.caution` | f2 | number | main (required) |
| `E3.PS.hi.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.PS.hi.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3.PS.hi.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3.PS.hi.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.hi.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.PS.hi.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.hi.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.PS.hi.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.hi.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.PS.hi.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.hi.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.PS.hi.dc` | f2 | number | main (required) |
| `E3.PS.hi.dc.ci` | ci2 | [lo, hi] | main (required) |
| `E3.PS.hi.dt` | f2 | number | main (required) |
| `E3.PS.hi.dt.ci` | ci2 | [lo, hi] | main (required) |
| `E3.PS.hi.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.PS.hi.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.hi.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.hi.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.hi.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.hi.vimp` | f1 | number | main (required) |
| `E3.PS.lo.caution` | f2 | number | main (required) |
| `E3.PS.lo.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.PS.lo.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3.PS.lo.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3.PS.lo.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.lo.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.PS.lo.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.lo.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.PS.lo.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.lo.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.PS.lo.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.lo.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.PS.lo.dc` | f2 | number | main (required) |
| `E3.PS.lo.dc.ci` | ci2 | [lo, hi] | main (required) |
| `E3.PS.lo.dt` | f2 | number | main (required) |
| `E3.PS.lo.dt.ci` | ci2 | [lo, hi] | main (required) |
| `E3.PS.lo.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.PS.lo.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.lo.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.lo.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.lo.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.PS.lo.vimp` | f1 | number | main (required) |
| `E3.TG.hi.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.TG.hi.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3.TG.hi.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3.TG.hi.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.hi.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.TG.hi.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.hi.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.TG.hi.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.hi.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.TG.hi.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.hi.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.TG.hi.dc` | f2 | number | main (required) |
| `E3.TG.hi.dc.ci` | ci2 | [lo, hi] | main (required) |
| `E3.TG.hi.dt` | f2 | number | main (required) |
| `E3.TG.hi.dt.ci` | ci2 | [lo, hi] | main (required) |
| `E3.TG.hi.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.TG.hi.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.hi.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.hi.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.hi.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.hi.vimp` | f1 | number | main (required) |
| `E3.TG.lo.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.TG.lo.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3.TG.lo.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3.TG.lo.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.lo.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.TG.lo.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.lo.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.TG.lo.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.lo.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.TG.lo.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.lo.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3.TG.lo.dc` | f2 | number | main (required) |
| `E3.TG.lo.dc.ci` | ci2 | [lo, hi] | main (required) |
| `E3.TG.lo.dt` | f2 | number | main (required) |
| `E3.TG.lo.dt.ci` | ci2 | [lo, hi] | main (required) |
| `E3.TG.lo.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.TG.lo.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.lo.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.lo.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.lo.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.TG.lo.vimp` | f1 | number | main (required) |
| `E3.n_cases` | int | integer count | main (required) |
| `E3b.const.CK3.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3b.const.CK3.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.CK3.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.CK3.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.CK3.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.CK3.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.CK3.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.CK3.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.CK3.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.CK3.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.CK3.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.CK3.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.CK3.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.CK3.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.N.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3b.const.N.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.N.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.N.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.N.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.N.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.N.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.N.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.N.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.N.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.N.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.N.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.N.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.N.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.PS.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3b.const.PS.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.PS.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.PS.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.PS.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.PS.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.PS.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.PS.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.PS.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.PS.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.PS.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.PS.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.PS.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.PS.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.TG.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3b.const.TG.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.TG.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.TG.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.TG.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.TG.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.TG.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.TG.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.TG.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.TG.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.TG.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.TG.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.TG.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.TG.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.CK3.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3b.mild.CK3.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.CK3.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.CK3.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.CK3.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.CK3.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.CK3.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.CK3.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.CK3.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.CK3.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.CK3.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.CK3.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.CK3.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.CK3.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.N.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3b.mild.N.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.N.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.N.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.N.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.N.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.N.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.N.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.N.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.N.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.N.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.N.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.N.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.N.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.PS.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3b.mild.PS.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.PS.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.PS.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.PS.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.PS.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.PS.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.PS.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.PS.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.PS.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.PS.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.PS.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.PS.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.PS.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.TG.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3b.mild.TG.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.TG.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.TG.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.TG.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.TG.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.TG.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.TG.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.TG.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.TG.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.TG.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.TG.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.TG.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.TG.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.n_cases` | int | integer count | main (required) |
| `E3b.stopgo.CK3.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.N.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3b.stopgo.N.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.N.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.N.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.N.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.N.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.N.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.N.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.N.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.N.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.N.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.N.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.N.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.N.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.PS.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3b.stopgo.PS.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.PS.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.PS.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.PS.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.PS.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.PS.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.PS.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.PS.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.PS.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.PS.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.PS.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.PS.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.PS.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.TG.d_fallback` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `E3b.stopgo.TG.d_fallback.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.TG.d_jerk` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.TG.d_jerk.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.TG.d_peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.TG.d_peakdec.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.TG.d_restgap` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.TG.d_restgap.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.TG.d_vimp` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.TG.d_vimp.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.TG.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.TG.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.TG.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.TG.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |

### F (41 keys; 23 required by the main text or the response letter)

| Key | Printed as | Value type | Where |
|---|---|---|---|
| `F.IMM.c` | sh3 | number, share of the room | main (required) |
| `F.IMM.c.ci` | ci3 | [lo, hi] | main (required) |
| `F.IMM.eff` | sh3 | number, share of the room | main (required) |
| `F.IMM.eff.ci` | ci3 | [lo, hi] | main (required) |
| `F.IMM.r` | sh3 | number, share of the room | main (required) |
| `F.IMM.r.ci` | ci3 | [lo, hi] | main (required) |
| `F.IMM.within5` | pct1 | number in [0, 1], printed as % | main (required) |
| `F.PO25` | sh3 | number, share of the room | main (required) |
| `F.PO50` | sh3 | number, share of the room | main (required) |
| `F.PO75` | sh3 | number, share of the room | main (required) |
| `F.R` | pp | number, percentage points | main (required) |
| `F.R.ci` | ci2 | [lo, hi] | main (required) |
| `F.RR_E5` | sh3 | number, share of the room | main (required) |
| `F.RR_E5.ci` | ci3 | [lo, hi] | main (required) |
| `F.RR_E5mP` | sh3 | number, share of the room | main (required) |
| `F.RR_E5mP.ci` | ci3 | [lo, hi] | main (required) |
| `F.RR_N` | sh4 | number, share of the room | main (required) |
| `F.RR_N.ci` | ci4 | [lo, hi] | main (required) |
| `F.RR_N.dec` | dec1 | number, decision-equivalents | main (required) |
| `F.RR_N.dec.ci` | ci1 | [lo, hi] | main (required) |
| `F.RR_TG` | sh3 | number, share of the room | supplement (n.c. if absent) |
| `F.RR_TG.ci` | ci3 | [lo, hi] | supplement (n.c. if absent) |
| `F.design.R2` | pp | number, percentage points | supplement (n.c. if absent) |
| `F.design.R2.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `F.design.R3` | pp | number, percentage points | supplement (n.c. if absent) |
| `F.design.R3.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `F.design.removed2.E` | int | integer count | supplement (n.c. if absent) |
| `F.design.removed2.F0` | int | integer count | supplement (n.c. if absent) |
| `F.design.removed3.E` | int | integer count | supplement (n.c. if absent) |
| `F.design.removed3.F0` | int | integer count | supplement (n.c. if absent) |
| `F.horizon` | str | string or number | main (required) |
| `F.inpath.R` | pp | number, percentage points | supplement (n.c. if absent) |
| `F.inpath.RR_N` | sh4 | number, share of the room | supplement (n.c. if absent) |
| `F.n_dec` | int | integer count | main (required) |
| `F.n_design` | int | integer count | supplement (n.c. if absent) |
| `F.n_heldout` | int | integer count | main (required) |
| `F.prereg.design.R2` | pp | number, percentage points | supplement (n.c. if absent) |
| `F.prereg.design.R2.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `F.prereg.design.R3` | pp | number, percentage points | supplement (n.c. if absent) |
| `F.prereg.design.R3.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `F.provenance` | str | string or number | supplement (n.c. if absent) |

### Read from records (no package action)

- V12: `GL_RRN`, `GL_RR_CK3`, `GL_R` (revision_v12\draft\DERIVED_v12.json).
- LOCK: `A10_1`, `A10_2` (short SHA-256 of the lock files).
- B (old runs only), read from B's own files through `gen\rename_v13.json`: BSUM = `B_retrack\out\B_RESULTS_SUMMARY_v13.json` (`B0a.bit_identical`, `B0a.lead_braking_runs`, `B0a.max_abs_diff_other`, `B0a.runs`, `B0b.all_ok`, `B0b.runs_checked`, `B9.events_found`, `B9.lat_m`, `constants.kappa`, `constants.sigma_a2`, `constants.tuning.kappa.median_lead_nis`, `constants.tuning.sigma_a2.median_lead_nis`, `variants.B2.post_hoc_supplement_only.RR_E5q.ci`, `variants.B2.post_hoc_supplement_only.RR_E5q.point`, `variants.B2.post_hoc_supplement_only.share_rows_outside_E5_band`); B8 = `B_retrack\out\b8\B8_NIS_NEES_v01.json` (60 keys).
- The fresh-run tracker values `B.<x>.*` (section B above) are exported by package B in `A_EXPORT_B.json`; the rate and latency values `B7.*` (under C) by package CD in `A_EXPORT_C.json` (coordinator, 20 Nov). After-stop room `as_room` is in decision-equivalents.

## 4. Meanings of keys whose names are not obvious

- Prefixes: `LB.` fresh lead-braking runs (all evaluated decisions unless a population is named: `LB.<pop>.` with pop in all, mov (ego > 0.5 m/s), pre, brk, stop by the tracker's phase estimate); `CI.` fresh cut-in runs in the event window (`CI.Y.` young tracks < 1 s; `CI.age0/age1/age4/untr.` track-age strata); `TU.` the 20 lead-braking tuning runs; `F.` held-out nuScenes scenes (design split if F.status is design_only); `B.<x>.` tracker variant x on the fresh lead-braking runs (x: CV online, CV2 re-tuned, CA, IMM, AQ adaptive Q); `B7.<rate>.<latency>.` rate and latency variants.
- `R` room in pp (gridless, 3 s); `R.dec` the same in decision-equivalents; `RR_<SRC>` gridless share of SRC; `RR_E5mP` = RR(E5) - RR(E5p); `PO25/PO50/PO75` partial-oracle shares; `IMM.r` = RR_gl(N_IMM) on the IMM's own room; `IMM.c` = its ceiling c_IMM; `IMM.eff` = r/c; `IMM.within5` share of binding rows within 5% of the median N_IMM/F0_IMM ratio.
- `LB.PS.rec`, `LB.PS.like`, `LB.PS.single`, `LB.PS.truth`, `LB.PS.thr05`, `LB.PS.thr20`: the H4 schedule share on the record basis, like-for-like basis, the single scale, and the truth-phase and threshold sensitivities (A10 §5.5).
- `LB.RS.<tau>.<A>.rel`: reaction-and-stop room relative to the 3 s room; `.den0.dec`, `.RR0_N`, `.RR0_CK3` as of record. `LB.RS075.rel` = `LB.RS.0.75.6.rel`. `LB.T<i>.rel` tercile i (1 lowest deceleration) at 0.75 s and 6 m/s^2, `LB.T<i>.range` its realised-deceleration range as a string "a–b", `LB.T<i>.evaluable` den0 >= 10; `LB.T.relmin`/`relmax` the smallest and largest of the evaluable terciles; `LB.DS.rel` delayed stop (A10 B6(b)); `LB.REL_F0/N/CK3` share of decisions safe only because the stop follows, at matched caution; `LB.gap2.` 2 m standstill gap.
- `B.<x>.as_room` after-stop room (decision-equivalents; B also exports `.as_room.pp`); `B.<x>.lag` median CV-predicted minus true lead position at 3 s in the first second after the stop (m); `B.<x>.nis` median over runs of the lead track's mean position NIS; `B.<x>.nis_<phase>`, `B.<x>.nees_<phase>` B8(b). `B7.ratio_10_2` = after-stop room at 10 Hz, 0.1 s over that at 2 Hz, 0 s.
- `TRANSFER.structured`: the A10 §5.6 facts; A turns them into sentences (codes CK3, AM, TG, NA, N; sets tuning, old, fresh, F). `TRANSFER.statements` (plain English, printed verbatim) is still accepted.
prediction recovers more than the acceleration margin"; A prints them verbatim.
- `D1.<v>.<SRC>.dcau`, `.dwg`: caution and wrong-go differences against F0 in points (v: const, mild, stopgo). `D2.<SRC>.<c2|c5>.<w3|rs>.runs`, `.vclose`: the event-level table (A10 §6 D2).
- `E3.<arm>.<lo|hi>.dc` paired contact-share difference vs F0 (Newcombe CI in `.dc.ci`), `.dt` time-lost difference (s), `.contact` contact share, `.vimp` median impact speed, `.tlost`, `.restgap`, `.peakdec`, `.jerk`, `.fallback`; arm NIMM is compared with F0IMM. `E1.v<speed>.dist/.model/.err` brake test (err as a fraction); `E1.maxerr` the largest |err|.
- `deviations` (any package): list of {"item", "planned", "done", "why"} for Table S3; empty list if none.
- `HAND.status` (C), `B0.identity`, `B.IMMCHECK.status` (B; the second-implementation check of the IMM, renamed on 22 Nov so that it cannot be confused with the two-noise IMM of round 2, `B.IMM2N.*` and `B.IMM2C.*`): short strings such as "all 20 within 1e-6 m".

