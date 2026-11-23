"""Compares the recount (STEP0_RECOUNT_v01.json, A_RECOUNT_S0.json) with the first program's outputs. Run after the recount is written."""
import json, math
D = r'ARS_TRIAL\revision_v13\work'
C = D + r'\shared\checks\step0_recount'
me = json.load(open(C + r'\STEP0_RECOUNT_v01.json'))
fp = json.load(open(D + r'\B_retrack\out\step0\STEP0_CROSSING_v01.json'))
rows = []
TOL = 1e-9


def add(key, mine, theirs, exact=False):
    mine = mine if mine is not None else float('nan'); theirs = theirs if theirs is not None else float('nan')
    if isinstance(mine, bool) or isinstance(theirs, bool):
        diff = 0.0 if mine == theirs else 1.0
    else:
        both_nan = isinstance(mine, float) and isinstance(theirs, float) and math.isnan(mine) and math.isnan(theirs)
        diff = 0.0 if both_nan else abs(float(mine) - float(theirs))
    ok = (diff == 0.0) if exact else (diff <= TOL)
    rows.append(dict(key=key, recount=mine, first=theirs, abs_diff=diff, tol=0 if exact else TOL, result='pass' if ok else 'FAIL'))


for fam in ('vehicle_crossing', 'pedestrian_crossing'):
    for sn, sect in (('all', fp['families']), ('tuning', fp['tuning_only'])):
        a = me['%s|%s' % (fam, sn)]; b = sect[fam]; k = '%s|%s|' % (fam, sn)
        add(k + 'n_runs', a['n_runs'], b['n_runs'], True)
        add(k + 'runs_with_eval', a['runs_with_eval'], b['runs_with_evaluated'], True)
        add(k + 'n_eval_decisions', a['n_eval_decisions'], b['evaluated_decisions'], True)
        add(k + 'R_pp', a['R_pp'], b['points']['R_pp']); add(k + 'R_deceq', a['R_deceq'], b['points']['R_deceq'])
        for lv, key in (('ci95', '0.95'), ('ci90', '0.9')):
            for e, f in ((0, 'lo'), (1, 'hi')):
                add(k + 'R_pp.%s.%s' % (lv, f), a['R_pp_ci'][lv][e], b['intervals']['R_pp'][key][e])
                add(k + 'R_deceq.%s.%s' % (lv, f), a['R_deceq_ci'][lv][e], b['intervals']['R_deceq'][key][e])
        for nm, fn in (('N', 'N'), ('E5N', 'E5N'), ('E5', 'E5rec')):
            add(k + 'RR_%s.point' % nm, a['RR_' + nm]['point'], b['points']['RR'][fn])
            for lv, key in (('ci95', '0.95'), ('ci90', '0.9')):
                for e, f in ((0, 'lo'), (1, 'hi')):
                    add(k + 'RR_%s.%s.%s' % (nm, lv, f), a['RR_' + nm][lv][e], b['intervals']['RR'][fn][key][e])
        add(k + 'share_resamples_room_pos', a['share_resamples_room_pos'], b['intervals']['share_resamples_room_positive'])
        add(k + 'n_resamples_valid_for_shares', a['RR_N']['n_resamples_used'], b['intervals']['resamples_valid_for_shares'], True)
        for f in ('median', 'q05', 'q95', 'A', 'share_within5'):
            add(k + 'margin.' + f, a['margin'][f], b['margin_ratio']['share_within_5pct' if f == 'share_within5' else f])
        add(k + 'margin.n_rows', a['margin']['n_rows'], b['margin_ratio']['n'], True)
        add(k + 'share_no_binding_F0', a['share_no_binding_F0'], b['flags']['share_no_binding_constraint_F0'])
        add(k + 'share_some_row_unsafe_3s', a['share_some_row_unsafe_3s'], b['flags']['share_with_some_row_unsafe_3s'])
lb = fp['reference_lead_braking_tuning']; m = me['lead_braking|tuning']
add('lead_braking|tuning|n_runs', m['n_runs'], lb['n_runs'], True)
add('lead_braking|tuning|n_eval_decisions', m['n_eval_decisions'], lb['evaluated_decisions'], True)
add('lead_braking|tuning|R_pp', m['R_pp'], lb['points']['R_pp']); add('lead_braking|tuning|R_deceq', m['R_deceq'], lb['points']['R_deceq'])

# the 45-key export
ex_me = json.load(open(C + r'\A_RECOUNT_S0.json'))['values']
ex_fp = json.load(open(D + r'\B_retrack\out\step0\A_EXPORT_S0.json'))
ex_fp = ex_fp.get('values', ex_fp)
exrows = []
for k, v in ex_me.items():
    t = ex_fp.get(k)
    exact = k.endswith('n_runs') or k.endswith('n_dec')
    if isinstance(v, list):
        for i, x in enumerate(v):
            exrows.append((k + '[%d]' % i, x, None if t is None else t[i], False))
    else:
        exrows.append((k, v, t, exact))
export_rows = []
for k, v, t, exact in exrows:
    n0 = len(rows)
    if t is None:
        export_rows.append(dict(key=k, recount=v, first=None, abs_diff=None, result='FAIL (missing in first)')); continue
    add('A_EXPORT_S0|' + k, v, t, exact)
    export_rows.append(rows.pop())
extra_keys = sorted(set(ex_fp) - set(ex_me))
out = dict(tolerances='counts exact; others abs diff <= 1e-9', main=rows, export45=export_rows, export_keys_only_in_first=extra_keys,
           summary=dict(main_compared=len(rows), main_pass=sum(r['result'] == 'pass' for r in rows), main_fail=sum(r['result'] != 'pass' for r in rows),
                        export_compared=len(export_rows), export_pass=sum(r['result'] == 'pass' for r in export_rows),
                        export_fail=sum(r['result'] != 'pass' for r in export_rows)))
json.dump(out, open(C + r'\STEP0_COMPARE_v01.json', 'w'), indent=1, default=float)
print(out['summary'], extra_keys)
for r in rows + export_rows:
    if r['result'] != 'pass':
        print(r)
