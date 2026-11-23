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
20:- **E**: E.status: "ran" | "stopped_brake" | "stopped_other"; E2.low_power (bool); E3.<arm>.<lev>.dc.ci, E3.<arm>.<lev>.dt.ci for arm in N, CK3, TG, PS, NIMM and lev in lo, hi; E3b.<v>.<arm>.dc.ci, E3b.<v>.<arm>.dt.ci for v in const, mild, stopgo and arm in N, CK3, PS, TG; EH1, EH2, EH3 (optional status)
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
| `E3.F0.hi.contact` | pct0 | number in [0, 1], printed as % | main (required) |
| `E3.F0.hi.fallback` | pct1 | number in [0, 1], printed as % | supplement (n.c. if absent) |
| `E3.F0.hi.jerk` | f2 | number | supplement (n.c. if absent) |
| `E3.F0.hi.peakdec` | f2 | number | supplement (n.c. if absent) |
| `E3.F0.hi.restgap` | f2 | number | supplement (n.c. if absent) |
| `E3.F0.hi.tlost` | f2 | number | supplement (n.c. if absent) |
| `E3.F0.hi.vimp` | f1 | number | main (required) |
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
| `E3.PS.hi.contact` | pct0 | number in [0, 1], printed as % | main (required) |
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
| `E3.PS.lo.contact` | pct0 | number in [0, 1], printed as % | main (required) |
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
| `E3b.const.CK3.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.CK3.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.CK3.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.CK3.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.N.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.N.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.N.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.N.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.PS.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.PS.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.PS.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.PS.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.TG.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.TG.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.const.TG.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.const.TG.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.CK3.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.CK3.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.CK3.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.CK3.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.N.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.N.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.N.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.N.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.PS.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.PS.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.PS.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.PS.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.TG.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.TG.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.mild.TG.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.mild.TG.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.n_cases` | int | integer count | main (required) |
| `E3b.stopgo.CK3.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.CK3.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.N.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.N.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.N.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.N.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.PS.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.PS.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.PS.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.PS.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.TG.dc` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.TG.dc.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
| `E3b.stopgo.TG.dt` | f2 | number | supplement (n.c. if absent) |
| `E3b.stopgo.TG.dt.ci` | ci2 | [lo, hi] | supplement (n.c. if absent) |
