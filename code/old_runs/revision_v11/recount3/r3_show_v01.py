"""Recount3: print the main numbers of RECOUNT3_RESULTS_v01.json (own results only)."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
name = 'RECOUNT3_RESULTS_v01%s.json' % ('_quick' if 'quick' in sys.argv else '')
r = json.loads((HERE / name).read_text(encoding='utf-8'))


def f(x, d=4):
    return 'None' if x is None else ('%.*f' % (d, x))


def ci(c, d=4):
    return 'None' if c is None else '[%s, %s]' % (f(c[0], d), f(c[1], d))


print('data', r['data'])
print('identity', r['cck3_identity']['total'], r['cck3_identity']['holds'])
i1 = r['item1_S12b']
print('\nITEM 1  n', i1['n'], 'undefined', i1['undefined_frontier_levels'])
for p, e in i1['share'].items():
    print(' share', p, 'mean decisions on oracle', e['evaluated_decisions_on_the_oracle_mean'])
    for pn, v in e['pops'].items():
        print('   %-15s mean %s  min %s  max %s' % (pn, f(v['RR_mean']), f(v['RR_min']), f(v['RR_max'])))
i2 = r['item2_S17']
print('\nITEM 2 theta', {k: round(v, 6) for k, v in i2['theta'].items()})
for m, e in i2['m'].items():
    print(' m', m, 'f', f(e['f']), 'denE<=0', e['n_denE_not_positive'], 'den0<=0', e['n_den0_not_positive'], 'undef', e['n_undefined_frontier'])
    for s, v in e['stats'].items():
        print('   %-18s [%s, %s]   pos-den reading [%s, %s]  n finite %d / %d' % (s, f(v['lo']), f(v['hi']), f(v['lo_positive_denominator_only']),
                                                                              f(v['hi_positive_denominator_only']), v['n_finite'], v['n_finite_positive_denominator_only']))
i3 = r['item3_S24b']
print('\nITEM 3 nboot', i3['nboot'], 'lib same', i3['evaluate_g_equals_rc_lib_evaluate'])
for pn, e in i3['pops'].items():
    print(' %-15s n %d den0 pp %s %s  deceq %s %s  denE pp %s  share den0<=0 %s' % (
        pn, e['n'], f(e['den0_pp']['point']), ci(e['den0_pp']['ci']), f(e['den0_deceq']['point'], 2), ci(e['den0_deceq']['ci'], 2),
        f(e['denE_pp']['point']), f(e['share_den0_not_positive'])))
    print('     ' + '  '.join('RR0_%s %s %s (out %d)' % (a, f(e['RR0_' + a]['point']), ci(e['RR0_' + a]['ci']), e['RR0_' + a]['n_left_out'])
                              for a in ('E', 'N', 'NA', 'CK3', 'AM')))
    if 'F0_zero_margin' in e:
        print('     F0 zero', e['F0_zero_margin'], 'O', e['O_point'], 'undef', e['undefined_frontier_levels_point'], e['resamples_with_undefined_frontier'])
print(' counts', i3['counts'])
i4 = r['item4_S25']
print('\nITEM 4 n', i4['n'], 'nan', i4['nan_critical_scales_evaluated'], 'ck3 same sel', i4['ck3_selection_equals_extract_ck3'])
print(' R_pp', {k: round(v, 4) for k, v in i4['R_pp'].items()}, 'undef', i4['resamples_with_undefined_frontier'])
for a0, e in i4['a0'].items():
    print(' a0', a0)
    for pn, v in e.items():
        print('   %-15s RR %s %s (out %d)  D deceq %s %s' % (pn, f(v['RR']), ci(v['RR_ci']), v['n_left_out'], f(v['D_deceq'], 2), ci(v['D_deceq_ci'], 2)))
for a, v in i4['zero_margin'].items():
    print(' zero margin %-4s caution %s  wrong go %s  (%d wrong-go decisions)' % (a, f(v['caution_pct']), f(v['wrong_go_pct']), v['wrong_go_decisions']))
b = r['item4_benign']
print('\nBENIGN', b['n_runs'], b['sets'], 'g1 grid', b['g1_grid_value'], b['g1_grid_value_is_exactly_1'])
print(' ', b['total'])
