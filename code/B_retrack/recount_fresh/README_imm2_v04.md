# IMM2 second programs (A12 s3c), written from A12_3c_IMM2_v02.md and the raw inputs; first-program IMM2 code not read

## imm2_v04.py (python -I -B -X utf8)
Imports the frozen recount_fresh.py / rf_core.py; same scoring (RF.per_variant), same draw (default_rng(20261911), first K rows = optA_lib boot_counts truncated).
- `--test-old-as IMM [--K 2000]`: 35 old runs, old B1 arrays, compared with B.IMM.* of out\TESTOLD_A_RECOUNT_B.json and testold_boot_IMM.npz. Outputs part_testold_IMM2_as_IMM.json, testold_boot_IMM2_as_IMM.npz. Ungated.
- `--fresh [--K 20000]`: 105 C runs (RF.fresh_run_ids), arrays B_retrack\out\retrack_fresh\IMM2\<rid>_arrays.npz; keys B.IMM2C.*; out part_fresh_IMM2C.json, boot_IMM2C.npz.
- `--new --runs-root R [--K 20000]`: ids = 150 rows reserve == False of CD_capture\l12\CASES_L12_v13.json, mapped by REPLACEMENTS_L12_v13.json (key `replacements`, case -> case; none applied with a printed NOTE if the file is absent), `pl12_<case>_native`, ascending, kept if R\<rid>\LOGS_OK exists; arrays B_retrack\out\retrack_new\IMM2\; keys B.IMM2N.*; out part_new_IMM2N.json, boot_IMM2N.npz.
- `--combine`: adds only B.IMM2C.* / B.IMM2N.* keys to B_retrack\out\A_RECOUNT_B.json; refuses if an existing key would change; backup A_RECOUNT_B_v04_before_IMM2[_n].json.
- Gate: LOCK_A10_2, LOCK_A10_2c, LOCK_A11, LOCK_A12a must all exist; checked before any fresh/new file or case list is opened.
- Extra keys: `p_one_sided` = #{b: RR_b <= 0} / #{b: RR_b finite} with RR_b = D_N/denE (finite iff denE > 0), `p_n_finite`.

## modeprob2_v01.py
`modeprob2_v01.py <label> <arrays dir> old | fresh | new <runs root>`; output out\MODEPROB2_<label>_<set>_v01.json (refuses to overwrite).
Decisions: evaluated, lead_found, phase in {0,1,2}; frame index (k-19)//10; mu_CA = mode_mu[:,1] of the record with mode_track == track_id and the largest mode_frame <= index (last in file order on ties); none -> skipped.
Per phase: n, mean, median, share(mu > 0.5), pooled; run-level bootstrap percentile intervals (2.5, 97.5; np.percentile linear), multiplicity weights from boot_counts(n_runs, 20000, 20261911). The weighted median is the numpy median of the expanded sample (checked against brute force).

## Choices
- Interval keys at K < 2000 differ from TESTOLD by construction; point values and per-resample arrays are compared.
- p_one_sided: ties at RR_b == 0 count toward the numerator (<= 0).
- A resample with an empty phase sample (cannot happen at these sizes) would be dropped by nanpercentile.
