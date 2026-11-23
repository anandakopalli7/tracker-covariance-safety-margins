"""One-off: tabulate the A10 2.6 calibration of both programs side by side (reads the two output files; computes nothing new)."""
import json, hashlib, pathlib, datetime
F = pathlib.Path(r'ARS_TRIAL\revision_v13\work\F_nuscenes')
fa, fb = F / 'out' / 'F_HELDOUT_v02.json', F / 'recount' / 'F_RECOUNT_HELDOUT_v02.json'
outp = F / 'out' / 'F_RECOUNT_COMPARE_CALIBRATION_v01.json'
assert not outp.exists()
a = json.loads(fa.read_text(encoding='utf-8')); b = json.loads(fb.read_text(encoding='utf-8'))
ca, cb = a['calibration'], b['calibrated']
m = {'R': 'R_gl_T1', 'RR_N': 'RR_gl_N', 'r_IMM': 'r_RR_gl_N_IMM', 'c_IMM': 'c_RR_gl_E5_IMM', 'eff_IMM': 'efficiency_r_over_c'}
rows = {}
for k, kb in m.items():
    x, y = ca[k], cb[kb]
    rows[k] = dict(first_level=x['level'], recount_level=y['level'], level_equal=x['level'] == y['level'],
                   first_coverage_nominal95=x['coverage_nominal95'], recount_coverage_nominal95=y['coverage_nominal95'],
                   same_side_of_0_94=(x['coverage_nominal95'] >= 0.94) == (y['coverage_nominal95'] >= 0.94)
                   if x['coverage_nominal95'] == x['coverage_nominal95'] else (y['coverage_nominal95'] < 0.94),
                   first_ci=x['ci'], recount_interval=y['interval'])
ha, hb = a['hypotheses'], b['verdicts']
verd = dict(F_H0=[ha['F_H0']['passes'], hb['F-H0']['passes']], F_H1=[ha['F_H1']['passes'], hb['F-H1']['passes']],
            F_H2=[ha['F_H2']['classification'], hb['F-H2']['branch'] + ': ' + hb['F-H2']['label']])
doc = dict(written=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
           first=str(fa), first_sha256=hashlib.sha256(fa.read_bytes()).hexdigest(),
           recount=str(fb), recount_sha256=hashlib.sha256(fb.read_bytes()).hexdigest(),
           levels_all_equal=all(r['level_equal'] for r in rows.values()),
           coverage_all_same_side=all(r['same_side_of_0_94'] for r in rows.values()),
           verdicts_first_recount=verd,
           verdicts_equal=verd['F_H0'][0] == verd['F_H0'][1] and verd['F_H1'][0] == verd['F_H1'][1] and verd['F_H2'][0] == verd['F_H2'][1],
           statistics=rows,
           convention_note=('The estimated coverage of the nominal 95% interval is an intermediate quantity (not in the export). '
                            'First program (f06, the expressions of a9_2a_double_bootstrap_mc_v01.cover_two): rank p-values of the '
                            'full-sample point among the inner statistics, covered if p_le >= a/2 and p_lt <= 1 - a/2 (tolerance '
                            '1e-12), mean over the outer resamples with a finite p-value. Recount (fr_core_v01.cover_rows, written from '
                            'the amendment text): linearly interpolated percentiles (np.percentile) of the finite inner statistics, '
                            'covered if lo <= point <= hi; an outer resample with no finite inner statistic or a non-finite point '
                            'counts as not covered (mean over all 2,000). The two readings differ by a few outer resamples where '
                            'inner statistics tie with the point; every statistic is on the same side of the 0.94 threshold in both, '
                            'so the calibrated levels (A10 2.6) are equal.'))
outp.write_text(json.dumps(doc, indent=1), encoding='utf-8')
print(json.dumps({k: doc[k] for k in ('levels_all_equal', 'coverage_all_same_side', 'verdicts_equal', 'verdicts_first_recount')}))
