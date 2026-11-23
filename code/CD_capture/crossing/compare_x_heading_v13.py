"""Compare the first program (crossing/out/X_HEADING_v13.json) with the second (recount/out/RC_X_HEADING_v13.json, Claude Sonnet 5.5) value by
value (A10 sec. 10.1 practice: equal within 1e-9 absolute or relative), and summarise the second program's independent per-tick
recomputation from the logs. EXPLORATORY task. New file, 22 Nov 2026 (Claude Opus 5.5, session CD). Writes crossing/out/COMPARE_X_HEADING_v13.json.
"""
import hashlib, json, math, pathlib
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
A = HERE / 'out' / 'X_HEADING_v13.json'; B = CD / 'recount' / 'out' / 'RC_X_HEADING_v13.json'
NM = {'cos_phi2': 'cos_phi^2', 'te': 'te', 'miss': 'miss', 'ln1p_age_upd': 'ln(1+age_upd)', 'abs_e_n': '|e_n|'}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    a = json.loads(A.read_text(encoding='utf-8')); b = json.loads(B.read_text(encoding='utf-8')); p1 = b['part1']; c = p1['counts']
    pairs = []
    def add(name, x, y): pairs.append((name, x, y))
    t = a['ticks']
    for k1, k2 in (('all', 'ticks_all'), ('evaluated', 'ticks_evaluated_status0'), ('primary', 'ticks_primary_status0_finite_prim'),
                   ('binding', 'ticks_binding_status0_bind_ok1'), ('analysed', 'ticks_analysed')):
        add('ticks.' + k1, t[k1], c[k2])
    add('y_bind.median', a['y_bind']['median'], c['y_bind']['median']); add('y_bind.sd', a['y_bind']['sd'], c['y_bind']['sd_ddof0'])
    add('y_bind.q25', a['y_bind']['iqr'][0], c['y_bind']['q25']); add('y_bind.q75', a['y_bind']['iqr'][1], c['y_bind']['q75'])
    for key, sp in (('y_bind', 'spearman_y_bind'), ('y_dec', 'spearman_y_dec')):
        for n, m in NM.items(): add('%s.spearman.%s' % (key, n), a[sp][n], p1[key]['spearman_rho'][m])
    for key, dk in (('y_bind', 'decomposition_y_bind'), ('y_dec', 'decomposition_y_dec')):
        d, e = a[dk], p1[key]
        add(key + '.n_ticks', d['n_ticks'], e['n_ticks']); add(key + '.n_runs', d['n_runs'], e['n_runs'])
        add(key + '.r2_full', d['r2_full'], e['r2_full'])
        for i in (0, 1): add('%s.r2_full_ci95[%d]' % (key, i), d['r2_full_ci95'][i], e['r2_full_ci95'][i])
        for g in ('geometry', 'schedule', 'error'):
            add('%s.shapley_r2.%s' % (key, g), d['shapley_r2'][g], e['shapley_r2'][g])
            add('%s.shapley_share.%s' % (key, g), d['shapley_share_of_r2'][g], e['shapley_share_of_r2'][g])
            add('%s.r2_single_group.%s' % (key, g), d['r2_single_group'][g], e['r2_single_group'][g])
            for i in (0, 1): add('%s.shapley_r2_ci95.%s[%d]' % (key, g, i), d['shapley_r2_ci95'][g][i], e['shapley_r2_ci95'][g][i])
        add(key + '.coef.intercept', d['coef']['intercept'], e['coef_full']['intercept'])
        for n, m in NM.items(): add('%s.coef.%s' % (key, n), d['coef'][n], e['coef_full'][m])
    o, q = a['object_frame_check'], p1['object_frame']
    for k1, k2 in (('abs_sin_major_vs_heading', 'abs_sin_angle'), ('axis_ratio', 'axis_ratio')):
        add(k1 + '.median', o[k1]['median'], q[k2]['median'])
        add(k1 + '.p25', o[k1]['iqr'][0], q[k2]['p25']); add(k1 + '.p75', o[k1]['iqr'][1], q[k2]['p75'])
        add(k1 + '.p05', o[k1]['p05_p95'][0], q[k2]['p5']); add(k1 + '.p95', o[k1]['p05_p95'][1], q[k2]['p95'])
    add('share_aligned_within_10deg', o['share_aligned_within_10deg'], q['abs_sin_angle']['share_aligned_lt_sin10'])
    add('share_across_within_10deg', o['share_across_within_10deg'], q['abs_sin_angle']['share_across_gt_cos10'])
    rows = []
    for n, x, y in pairs:
        ok = (x == y) or (isinstance(x, float) and isinstance(y, float) and math.isfinite(x) and math.isfinite(y)
                          and abs(x - y) <= 1e-9 * max(1., abs(x), abs(y)))
        rows.append(dict(value=n, first=x, second=y, agree=bool(ok)))
    # the second program's per-tick recomputation from the logs (three runs)
    ptc = b.get('per_tick_check') or {}
    def leaves(x):
        if isinstance(x, dict):
            if 'max_abs_diff' in x: yield x
            for v in x.values(): yield from leaves(v)
    per = {}
    for run, r in ptc.items():
        if not isinstance(r, dict): continue
        L = list(leaves(r))
        per[run] = dict(n_comparisons=len(L), all_nan_patterns_equal=all(l.get('nan_pattern_equal', True) for l in L),
                        max_abs_diff=max((l['max_abs_diff'] for l in L if l['max_abs_diff'] is not None), default=None),
                        n_with_nothing_to_compare=sum(l['max_abs_diff'] is None for l in L), k_equal=r.get('k_equal'), status_equal=r.get('status_equal'))
    out = dict(first=dict(file=str(A.name), sha256=sha(A)), second=dict(file=str(B.name), sha256=sha(B), program_sha256=b.get('program_sha256')),
               rule='equal, or within 1e-9 absolute or relative', n_values=len(rows), n_agree=sum(r['agree'] for r in rows),
               disagree=[r for r in rows if not r['agree']], per_tick_recomputation_from_logs=per, values=rows)
    (HERE / 'out' / 'COMPARE_X_HEADING_v13.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
    print('values agree %d/%d' % (out['n_agree'], out['n_values']), '| per-tick check:', json.dumps(per))


if __name__ == '__main__':
    main()
