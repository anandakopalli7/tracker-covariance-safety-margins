# E5 main: first vs second program, disagreement record (A10 §10.1(c))

Session E, 22 Nov 2026, 03:31 EST.

**Run:** `analysis\run_e5_v01.py main` (log `out\RUN_E5_v01_main.log`).

**Before the fix**

| Check | Result |
|---|---|
| Per-run outcomes (`e_compare_v01 outcomes`) | 270 runs compared, **0 disagreements** |
| Validity | 270 of 270 valid in both programs |
| Export (`e_compare_v01 export`) | **17 of 45 keys disagree** |

The 17 export keys:
- every comparison key: `E5.dc`, `.ci`, `.dt`, `.ci`, `.d_*`, `E5.class`, `E5.p_one`, `E5.mcnemar_p`;
- the second program's comparison has `pairs: 0` and `classification: 'no pairs'`.

**Cause.** The second program's comparison record is built with `level: None`, and its pairing filters runs on that level. Every real E5 run carries the job's level label `'D'` (`make_jobs_e5_v01.py`; SUMMARY `e_job.level`). The second program's synthetic test runs had no level, so the filter matched there but matches nothing on real data. The outcomes are read correctly; the bug is in pairing only.

**Fix.** The second program pairs E_N with E_F0 over all valid e5_ runs by case, without filtering on the level label (§6.6 has one level). The fix is made by the Sonnet subagent in `recount\e_recount_e5_v01.py`, v01 edited in place, with its SHA recorded below. Then the second program's `main` and the two comparisons are rerun.

**After the fix (03:36 EST).**
- The second program is `recount/e_recount_e5_v01.py`, SHA-256 `126dea37b18ba74bcd5fa69d8e216abfb26b77b1f3d890323bab7575e0b30fd6`.
  - It pairs over all valid e5_ runs by case.
  - It fails loudly on any level label other than D or None.
  - A synthetic test with level D is added.
- Its main step and the comparisons were rerun:

  | Check | File | SHA-256 | Result |
  |---|---|---|---|
  | Per-run outcomes | `out/e5/E_COMPARE_OUTCOMES_E5_v02.json` | `3d51d82664b469d2e10846105f663c80784eaba1e4910694172de5b915e7ef30` | 270 runs, **0 disagreements** |
  | Export | `out/e5/E_COMPARE_EXPORT_E5_v02.json` | `f9bac3f128e5bc01f15a0010001cab91bb1e0d667757ef83e2f4f6ab29cc45df` | 45 keys, **0 disagreements** |

- **Exports:**
  - `out/A_EXPORT_E5.json`, SHA-256 `20ecda6a122de2c2d976ee6bf8c84bd229f801a453425162ca25ae40d6655e28`;
  - `out/A_RECOUNT_E5.json`, SHA-256 `63b6be84c2baa669db0dc00b7262c2eb87e8df3fc5515f089ebd75866b2e3c88`.
- **Disclosure:** the fix was made after both programs had run on the main data. It changes only the second program's pairing filter. It changes no rule and no first-program value, and the first program's results were not altered.
