# Recount (second program) of package CD's A10 §5.7 keys ("S57A")

Written 20 Nov 2026 by a subagent on Claude Fable 5.2 (`claude-fable-5-2`), for AMENDMENT_10_v13 §10.1(b). The first program is
written by Claude Opus 5.5. No fresh-run value exists or was read.

## 1. Files

| File | What |
|---|---|
| `rc_s57a_v13.py` | The second program (this scope) |
| `README_RECOUNT_S57A.md` | This file |
| `superseded_rc_s57a_v13_fullscope_20261120_0231.txt` | The earlier full-scope version, kept as text only (§7) |
| `out\SELFTEST_RC_S57A_v13_final.json` | Values of record reproduced on old runs, final code (§4) |
| `out\TESTOLD_RC_S57A_v13.json` | Old-run test under A's keys, draw of record (§5) |
| `out\TESTOLD_RC_S57A_v13_PART_b200_s20261911.json` | The same on the first 200 rows of 20261911 (the draw of `TESTOLD_C_LEAD_H0_H5_v13.json`) |
| `out\TESTOLD_RC_S57A_v13_PART_b200_s20261911_po20261919.json`, `out\DRYRUN_RC_S57A_v13_PART_b200_b200.json` | Dry run of the fresh code path and its old-run twin (§6) |
| `out\testold_rc_s57a*_log.txt`, `out\dryrun_rc_s57a_b200_log.txt` | Logs |

Fresh output, after both locks: `out\RC_S57A_v13.json`
(`{"family": "S57A", "program": "rc_s57a_v13.py", "test_old": false, "values": {...}, "details": {...}}`).

## 2. Independence

- **Not read:** any `.py` under `CD_capture\analysis\` or `CD_capture\tools\`, and no output value of the first program.
- **Read:** A10; `CD_DEFINITIONS_v13.md`; the writer's `CD_DEFINITIONS_S57A_v13.md` (versions of 02:25 and 02:40 EST, re-read
  before finalizing); A's interface and key list; `rev_g_partial_oracle_draws_v01.py`, `a9_8_grading_before_stop_v01.py`,
  `rev_common_v01.py`, `a9_common_v01.py`; package B's `b6_stop_v01.py`, `trk_score_v01.py`, `trk_arrays_v01.py` (headers);
  the earlier recount modules in this folder.
- **Shared, as A10 §10.1(b) allows:** the scoring library of record `optA_lib_v02` (imported unchanged); extracted arrays;
  the resample draws.
- **Reused second-program code:** `rc_core_v13` / `rc_kern_v13` (own gridless kernel, E5 family, phase estimate),
  `rc_c_lead_v13` (H4 design and transfer), `rc_c_cutin_v13` (event tick, track age, populations).
- **Written here:** masks, the partial-oracle draw and critical scales, grid tables, decision-equivalents, intervals,
  the old-run stand-ins, the dry-run mode.
- The gridless values do **not** come from `a9_common_v01.gridless_sources` (which the writer's specification names): they come
  from the recount's own kernel. The selftest shows the two agree bit for bit on old runs.

## 3. Keys produced (54 keys: 47 of A's list and 7 `grading_ok`; plus `.level` and `.cal` for each of the 12 intervals)

| Group | Keys |
|---|---|
| Decision-equivalents, lead braking | `LB.R.dec`; `LB.RR_N.dec`, `LB.RR_E5.dec`, `LB.RR_E5mP.dec`, `LB.RR_CK3.dec`, `LB.IMM.r.dec`, `LB.IMM.c.dec`, `LB.PS.rec.dec`, each with `.ci` |
| Single scale | `LB.PS.single`, `.ci` (record basis, Σ(F_F0 − F_1) / Σ(F_F0 − F_E)) |
| Partial oracles | `LB.PO25/50/75`; `LB.<pop>.PO25/50/75` for pop in all, mov, pre, brk, stop; `CI.PO25/50/75` |
| Grading check | `LB.grading_ok`, `LB.<pop>.grading_ok`, `CI.grading_ok` (bool; not in A's key list, named as the brief and the specification say) |
| Cut-in window | `CI.RR_CK3`, `CI.RR_E5`, `CI.RR_E5mP`, each with `.ci`; `CI.RR_N.dec`, `.ci`; `CI.Y.R.dec` |

Definitions follow the specification §1–§5 and `CD_DEFINITIONS_v13.md` (H4). Every interval is nominal 95% on
`boot_counts(n, 20000, 20261911)` (fresh). Partial-oracle masks: `default_rng(20261919)`, one generator per run set.

## 4. Selftest: values of record on old runs (`--selftest`)

46 checks, 0 failed, largest difference 0 (`out\SELFTEST_RC_S57A_v13_final.json`, final code):
- **v11 `REV_G_PARTIAL_DRAWS_v01.json`** (draw of record `default_rng(20261118).random(9307)`, grid step frontier, truth phases):
  the 15 shares of record (all, moving, phase 0, 1, 2 × 25/50/75%) reproduced exactly.
- **v12 `A9_8_GRADING_BEFORE_STOP_v01.json`:** the three shares, n, the room and `grades_by_rule` reproduced exactly.
- **Gridless kernel against the library of record** (`a9_common_v01.gridless_sources` + `eval_scoring`), tracker-phase
  populations: 15 partial-oracle shares identical.
- **Cut-in section on a window stand-in.** The old cut-in windows hold no room (§5), so the same computation was run on a
  window of the 35 lead-braking runs (evaluated decisions within −20…+80 ticks of the first decision with truth phase ≥ 1;
  1,650 decisions; E5 ranks over all evaluated decisions): n, D(E) and D of N, E5, E5p, CK3, P25, P50, P75 identical to the
  library of record.

Also checked by hand: the points of `LB.R.dec`, `LB.RR_N/E5/CK3.dec`, `LB.PS.rec.dec` and `LB.PS.single` equal those implied by
the earlier H0–H5 recount output `RC_C_LEAD_TESTOLD_b200_o12_i50_inproc.json` (differences 0; `LB.RR_E5mP.dec` 9e-16).

## 5. Old-run test under A's keys (`--test-old`)

Conventions, as the specification §10 states them:
- **LB stand-in:** the 35 old evaluation runs; tracker phase from v12's lead extract; IMM from package B's B1 re-track arrays.
- **CI stand-in:** the 20 cut-in tuning runs; `cCK3` from package B's CV0 re-track arrays; events from the logs.
- **Draws:** run bootstrap `boot_counts(n, 20000, 20261113)`; LB partial oracles `default_rng(20261118).random(9307)`;
  CI partial oracles `default_rng(20261919)`.

`out\TESTOLD_RC_S57A_v13.json` (853 s). Main values:

| Key | Value | 95% interval |
|---|---|---|
| `LB.R.dec` | 456.990 | — |
| `LB.RR_N.dec` | −0.189 | −0.338 to 0.025 |
| `LB.RR_E5.dec` | 6.224 | 3.841 to 8.771 |
| `LB.RR_E5mP.dec` | 4.542 | 2.582 to 6.572 |
| `LB.RR_CK3.dec` | 382.318 | 292.960 to 469.321 |
| `LB.IMM.r.dec` | −0.050 | −0.587 to 0.343 |
| `LB.IMM.c.dec` | 0.338 | 0.219 to 0.557 |
| `LB.PS.rec.dec` | 453.119 | 355.950 to 544.564 |
| `LB.PS.single` | 0.000 | −0.00111 to −0.00021 |
| `LB.PO25/50/75` (all) | 0.268, 0.536, 0.778 | grades |
| mov | −0.119, 0.041, 0.433 | does not grade |
| pre | −0.371, −0.318, 0.175 | does not grade |
| brk | −0.140, 0.029, 0.444 | does not grade |
| stop | −0.375, −0.220, 0.197 | does not grade |

- **`LB.PS.single` is 0 at the point by construction** on old runs: the design set is the test set, so the transferred single
  scale is F0's own frontier. The interval lies just below 0 because resampled levels differ from the design levels.
- **Cut-in keys are untested by data.** In the 20 old cut-in runs D(E, F0) is 0 in the event window and over all evaluated
  decisions. So `CI.RR_CK3`, `CI.RR_E5`, `CI.RR_E5mP`, `CI.PO*` are null, `CI.RR_N.dec` is 0 with interval [0, 0],
  `CI.Y.R.dec` is 0 (no young-track decision) and `CI.grading_ok` is false. The code path ran end to end; its arithmetic is
  tested only on the window stand-in of §4.

## 6. Gate and dry run

- **Gate.** The fresh path refuses unless `revision_v13\LOCK_A10_2.txt` exists **and** `LOCK_A10_2c.txt` exists in
  `revision_v13\` or `revision_v13\work\locks\`. Checked: without stage 1 it refuses; with stage 1 simulated in memory
  (no file written) it refuses for the missing stage 2.
- **No root or gate from the environment.** The program stops if `RC_ARS_TRIAL`, `RC_DRYRUN` or `RC_PROGRAMME_A` is set.
- **Dry run.** `--make-dry DIR` writes the old runs in the fresh-array format into a folder outside the project;
  `--dry-run DIR` runs the fresh code path on it, bypassing the gate by that flag, and writes `DRYRUN_*`. The folder is
  refused if it lies inside the project trees, is named like the fresh arrays or runs, or holds a file named `LOCK_*` or
  `FREEZE_*`. This program wrote no lock-like file anywhere.
- **Result:** see §9.

## 7. Scope change and superseded code

By the coordinator's decision (20 Nov, 01:53 EST) these keys moved to package B and are not produced here:
`LB.RS075.rel`, `LB.T<i>.*`, `LB.T.relmin/relmax`, `LB.DS.*`, `LB.REL_*`, every `TU.*`.

- The code for them is kept only in `superseded_rc_s57a_v13_fullscope_20261120_0231.txt`. It is not a program and is not run.
- Development outputs of that version remain in `out\` (outputs are never deleted): `SELFTEST_RC_S57A_v13_dev1.json`,
  `SELFTEST_RC_S57A_v13_v2.json`, `TESTOLD_RC_S57A_v13_PART_b200_dev1.json`, `_dev3.json`, `_dev4.json`,
  `testold_s57a_dev1/2/3_log.txt`, `s57a_ext_testold\` and `s57a_ext_testold_log.txt`. All are old-run data. None is a result.
- For package B's information, what that version found on old runs before it was dropped:
  - 291 checks against the values of record passed with difference 0: `B6_STOP_v01.json` (realised decelerations, terciles,
    fixed and delayed stop with intervals), v12 A9-6 (all five populations), v12 A9-5 (tuning and evaluation), REV_G, A9-8.
  - An own extended-truth clearance (plans judged until the stop ends) reproduced v11's `out\ext` exactly on the 10 old
    runs tried.
  - **Open point for whoever owns `LB.REL_*`:** the method of record (A9-6) uses the extended-truth safe set, and A10 §1
    says reaction-and-stop plans are "judged until the stop ends". The first version of the writer's specification used
    the 3 s-window clearance instead. The two give different values.

## 8. Disagreements with the writer's specification, and choices of my own

1. **Identity check of package B's CV0 arrays (old-run test only): resolved.** The 02:40 specification accepted them only
   within 1e-12. On 18 of the 20 cut-in tuning runs cF0 differs by up to 8.2e-12 (1.1e-14 relative, on scales of several
   hundred); cE and cN are identical. I accept 1e-12 absolute or relative. The specification of 03:11 now states the same
   rule (|b − z| ≤ 1e-12·max(1, |z|)). It affects no fresh key.
2. **`.dec.ci` level.** The specification uses nominal 95% everywhere (its open choice 1). A's interface §1 says intervals
   are "at the level the hypothesis's calibration selected". A10 does not define `.dec.ci`. I follow the specification by
   default so the two programs compare; `--levels-lead` / `--levels-cutin` can apply calibrated levels if the lead decides so.
3. **Gridless construction.** The specification names `a9_common_v01.gridless_sources`; I use the recount's own kernel (§2).
   Not a disagreement in value.
4. **Run list with replacements.** The specification says the run ids come "with `REPLACEMENTS_C_v13.json` if it exists" but
   not how. If that file exists, I take the ids present in `arrays\CV0` with the family in their meta, require the same
   number as the case list, and record what was dropped and added.
5. **Cut-in event and track age.** The specification reads them from `arrays\S57A` (its own extraction). I compute them
   from the logs with `rc_c_cutin_v13` (or reuse that recount's truth file for the same runs). Same definition
   (`CD_DEFINITIONS_v13.md`, cut-in).
6. **Partial oracles: gridless, not grid.** The method of record (rev_g) scores on the grid step frontier. A10 §2.3 makes the
   gridless frontier primary for every share, and the specification agrees. The grid values are in `details`. On the 35 old
   runs the two differ in the third decimal (all: 0.268 / 0.536 / 0.778 gridless, 0.269 / 0.536 / 0.778 grid).
7. **No disagreement with A10 found** for the keys in scope.

## 9. Dry run result, state of the files, and what is not done

- **Dry run (200 resamples).** `out\DRYRUN_RC_S57A_v13_PART_b200_b200.json` ran the fresh loaders and all four sections on
  the old runs written in the fresh-array format (35 lead with B1, 20 cut-in). Its 78 values equal, one by one and exactly,
  those of `out\TESTOLD_RC_S57A_v13_PART_b200_s20261911_po20261919.json` (the old-run path with the fresh seeds 20261911 and
  20261919). So the fresh path and the tested old-run path compute the same thing.
- **Refusals checked on the final code:** no stage-1 lock; stage 2 missing; `RC_DRYRUN` set; a dry-run folder inside the project.
- **Final code:** SHA-256 `db127f48b6c2a19f863b15d59902bf1131f64a4e3f1cc47cef30355a3f0ae4b0` (20 Nov 2026, 03:23 EST).
  `TESTOLD_RC_S57A_v13.json` (SHA-256 `5a8bf05d…8324`) and the 20261911 variant were written at 02:53–03:07 EST, before the
  dry-run mode was added at 03:09; that change touched the loaders and the gate only, and the final selftest and the dry
  run were made with the final code.
- **Gate location.** This program accepts `LOCK_A10_2c.txt` in `revision_v13\` or `revision_v13\work\locks\` (the
  coordinator confirmed this gate). The specification of 03:11 names `revision_v13\` only.
- **Not done:**
  - no comparison with the first program's old-run output (not read; the lead's comparator does it);
  - the cut-in keys have no non-trivial old-run value (§5);
  - nothing on fresh runs; after both locks: `python -I -B -X utf8 rc_s57a_v13.py --workers 2` (expect roughly 1–1.5 h for
    105 + 105 runs at 20,000 resamples; the old-run test took 14 min for 35 + 20 runs).
