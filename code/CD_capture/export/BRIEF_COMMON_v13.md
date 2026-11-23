# Common rules for every program written for package CD's A10 §5.6–5.7 export (20 Nov 2026)

Context: revision v13 of an IEEE OJ-ITS paper. Package C scores 105 fresh lead-braking and 105 fresh cut-in CARLA runs once, after
Lock 2; package D scores 105 non-braking-lead runs. The pre-registration is `ARS_TRIAL\revision_v13\AMENDMENT_10_v13.md` (A10;
§0 overrides the rest; §2 definitions; §3 package B methods B1–B9; §5 package C, esp. §5.5–5.8; §10 verification). Session A typesets
the paper from one export per package; its interface is `revision_v13\work\A_text\RESULTS_INTERFACE_v13.md` (§1 format, §2 status keys,
§4 key meanings) and the key list `revision_v13\work\CD_capture\export\A_KEYS_CD_v13.json` (key, printed_as, value_type, where, required).

## Hard rules
- **No fresh-run data.** `revision_v13\LOCK_A10_2.txt` does not exist. Do not open anything under `work\CD_capture\archives\`, `runs\`,
  `arrays\`, `b7\` (except `b7\p1b_fit_finite_0037\`, an old run), `pod_outputs\`, or any `pc13_*` / `pd13_*` file. Fresh code paths must
  refuse to run without the lock (first programs: `cd_common_v13.require_lock2(test_old)`; second programs: their own equivalent gate on
  the same file). Develop and test on OLD runs only (35 old evaluation lead-braking runs `p1b_fit_finite_*`, the 20 lead-braking tuning
  runs, the 20 cut-in tuning runs).
- **Never open** anything named `<excluded folder 1>` or `<excluded folder 2>`, nor `<user folder>`.
- **Read-only:** `<library folder>` (P), `<earlier-phase folder 2>`,
  `<earlier-phase folder 3>`, `<earlier-phase folder 4>`, `revision_v11\`, `revision_v12\`, `review_v12_output\`,
  `revision_v13\work\B_retrack\`, `revision_v13\work\shared\trackers\` (package B's frozen library: import it, never edit).
- Do not edit files you do not own (your brief lists them). In particular never edit `CD_capture\analysis\cd_common_v13.py`,
  `c_extract_v13.py`, `c_lead_v13.py`, `c_cutin_v13.py`, `gl_fast_v13.py`, anything in `recount\` or `recount_d\` you do not own, or
  `CD_DEFINITIONS_v13.md`. You may import them.
- No network, no pods, no package installs, no messages to other sessions.
- Python: `ARS_TRIAL\revision_v13\work\CD_capture\.venv\Scripts\python.exe -I -B -X utf8`, environment
  `OPENBLAS_CORETYPE=Haswell`. The laptop (4 cores) is shared by about eight processes: use at most 2 worker processes or threads;
  run anything longer than about 2 minutes in the background and wait for it. Never overwrite an existing output; use new names.
- `-I` drops the script's folder from sys.path: insert it yourself.

## Output convention (both programs)
- One JSON per program and run set: `{"family": ..., "program": "<script>", "test_old": true|false, "values": {<A key>: <value>}, "details": {...}}`.
- `values` uses A's key names exactly (from the key list). Unrounded numbers; shares as fractions of the room; rooms in percentage
  points; decision-equivalents where the key says `.dec`; intervals `[lo, hi]`; `null` for anything undefined.
- For every interval key `X.ci` also write `X.level` (e.g. 0.95) and `X.cal` = "nominal95" | "calibrated" | "nominal99". Descriptive
  intervals are nominal 95% percentile intervals on the fresh-run bootstrap (`default_rng(20261911)`, 20,000 run resamples, A10 §5.5) unless
  A10 says otherwise (tuning runs: `default_rng(20261918)`, A10 §5.6).
- In old-run tests the same key names are used (prefix `LB.`/`CI.` as for fresh runs) and the file is named `TESTOLD_<family>_v13.json`.
  Old-run tests use the draws of record where you compare against a value of record (A10 §5.8: old-run analyses use 20261113), and say so.
- Record every definitional choice not fixed by A10 or the method of record in your definitions file, BEFORE you see any fresh value.

## Existing first-program pieces you can rely on (package CD, Claude Opus 5.5)
- `CD_capture\analysis\cd_common_v13.py`: constants, Lock 2 gate, run lists (`c_run_ids(family)`, sorted ids), `load_variant(run_ids, variant)`
  (fresh arrays `arrays\<variant>\<rid>.npz` written by `c_extract_v13.py`: CV0 with TG critical scales `cTG1/2/4` and, for lead braking,
  `clearR075` = true clearance under reaction-and-stop τ 0.75 s, 6 m/s²; B1 = the frozen IMM), `load_old_lead()` (old runs),
  `prep/evaluate` (gridless frontier kernel, bit-identical to `a9_common_v01.Gridless` + `optA_lib_v02.eval_scoring`), bootstrap helpers.
- `CD_capture\CD_DEFINITIONS_v13.md`: definitions used by H0–H5, K0–K2, D (gridless, E5/E5p/E5_x, phases, decision-equivalents, cut-in event,
  track age, calibration).
- Run folders after Lock 2: `runs\<rid>\<rid>\capture\<case>\` (logs; same layout as the old archives' `x\<rid>\capture\<case>\`).
