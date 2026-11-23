"""Compact printer of the revision result files (reads out/*.json; writes nothing). Usage: python -B rev_print_v01.py A|B|D|E|F"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
O = HERE / 'out'


def ci(s, nd=3):
    if 'ci' not in s:
        return ('%.' + str(nd) + 'f') % s['point']
    f = '%.' + str(nd) + 'f'
    return (f + ' [' + f + ', ' + f + ']') % (s['point'], s['ci'][0], s['ci'][1])


def show_A():
    d = json.loads((O / 'REV_A_SIGNED_GAP_v01.json').read_text())
    for key in ('W1_unsigned_of_record', 'W1_signed'):
        print('=== R11', key)
        for pop, e in d['R11'][key].items():
            print(' %-7s n %5d  R(E) %.3f pp [%s]  den0 %.3f pp (%.1f dec-eq)  E_rr0 %s' % (
                pop, e['n'], e['denE']['R_pp'], ', '.join('%.3f' % (x / 201) for x in e['denE'].get('ci', [float('nan')] * 2)),
                e['den0']['R_pp'], e['den0']['dec_eq'], ci(e['E_rr0'])))
            for a, ent in e['arms'].items():
                print('     %-5s rrE %-28s rr0 %-28s D %.2f dec-eq' % (a, ci(ent['rrE'], 4), ci(ent['rr0'], 4), ent['D_dec_eq']))
    print('zero-margin points', json.dumps(d['R11']['zero_margin_points_all']))
    print('n evaluated without W1-safe row', d['R11']['n_evaluated_without_W1_safe_row'])
    print('=== R17 pair counts', d['R17']['pair_counts'])
    for key, sc in d['R17'].items():
        if not key.endswith('_gap2'):
            continue
        print('=== R17', key, 'decisions without a safe row:', sc['n_evaluated_without_safe_row'])
        for pop, e in sc.items():
            if not isinstance(e, dict) or 'arms' not in e:
                continue
            dq = e['den0'].get('dec_eq_ci')
            print(' %-7s n %5d  den0 %.4f pp, %.2f dec-eq %s  denE %.4f pp (%.2f)  E_rr0 %s' % (
                pop, e['n'], e['den0']['R_pp'], e['den0']['dec_eq'], ('[%.2f, %.2f]' % tuple(dq)) if dq else '',
                e['denE']['R_pp'], e['denE']['dec_eq'], ci(e['E_rr0'])))
            for a, ent in e['arms'].items():
                print('     %-5s rr0 %-28s rrE %-28s D %.2f dec-eq' % (a, ci(ent['rr0'], 4), ci(ent['rrE'], 4), ent['D_dec_eq']))


def show_B():
    d = json.loads((O / 'REV_B_TRUNC_PHASESCALE_v01.json').read_text())
    print('=== R12a truncation')
    for key, e in d['R12a'].items():
        if key == 'post_stop_segment':
            import statistics
            ls = [x['last_after_stop_s'] for x in e if x['last_after_stop_s'] is not None]
            print(' after-stop segment length (s): min %.1f median %.1f max %.1f over %d runs' % (min(ls), statistics.median(ls), max(ls), len(ls)))
            continue
        print(' %-5s n %5d  R %.3f pp [%.3f, %.3f]  den0 %.3f pp' % (key, e['n'], e['R_pp'], e['denE']['R_pp_ci'][0], e['denE']['R_pp_ci'][1], e['den0']['R_pp']))
        for a, ent in e['arms'].items():
            print('     %-4s rrE %-30s rr0 %-30s D %.1f dec-eq' % (a, ci(ent['rrE'], 4), ci(ent['rr0'], 4), ent['D_dec_eq']))
    s = d['R12b']['summary']; p = d['R12b']['point']
    print('=== R12b per-phase scale; nboot', s['nboot'], 'frontier check', d['R12b']['front_bins_vs_frontier_max_abs_diff'])
    for k in ('den1', 'den0_1', 'gain_F0', 'gain_E', 'den_ps', 'den0_ps'):
        print(' %-8s %.4f pp [%.4f, %.4f]  %.1f dec-eq' % (k, s[k]['pp'], s[k]['pp_ci'][0], s[k]['pp_ci'][1], s[k]['dec_eq']))
    for k in ('gain_F0_over_den1', 'den_ps_over_den1', 'gain_F0_over_den0_1'):
        print(' %-22s %s' % (k, ci(s[k], 4)))
    for a, e in s['arms'].items():
        print('  %-4s rr_single %-26s rr_ps %-26s rr0_ps %-26s Dps/den1 %-26s Dps %.1f [%.1f, %.1f] dec-eq (single %.1f)' % (
            a, ci(e['rr_single'], 4), ci(e['rr_ps'], 4), ci(e['rr0_ps'], 4), ci(e['Dps_over_den1'], 4), e['Dps_dec_eq']['point'],
            e['Dps_dec_eq']['ci'][0], e['Dps_dec_eq']['ci'][1], e['D1_dec_eq']['point']))


def show_D():
    d = json.loads((O / 'REV_D_BOOTSTRAP_v01.json').read_text())
    print('full sample', {k: round(v, 5) for k, v in d['full_sample'].items()})
    print('=== D1 draw of record')
    for s, e in d['D1_draw_of_record'].items():
        q = e['q_0_0p05_0p5_2p5_5_25_50_75_95_97p5_99p5_99p95_100']
        print(' %-10s point %.5f  pct95 [%.5f, %.5f] basic95 [%.5f, %.5f]  min %.5f med %.5f max %.5f  share<point %.4f  share<=0 %.4f distinct %d' % (
            s, e['point'], e['percentile_95'][0], e['percentile_95'][1], e['basic_95'][0], e['basic_95'][1], q[0], q[6], q[12],
            e['share_below_point'], e['share_le_zero'], e['n_distinct']))
    print('=== D2 double bootstrap', d['D2_double_bootstrap']['B_outer'], 'x', d['D2_double_bootstrap']['B_inner'])
    for s, e in d['D2_double_bootstrap']['stats'].items():
        cp = e['coverage_percentile']; cb = e['coverage_basic']; cu = e['coverage_upper_bound']
        print(' %-10s cov pct: 90 %.3f 95 %.3f 99 %.3f 99.9 %.3f 100 %.3f | basic: 95 %.3f 99 %.3f 100 %.3f | upper bound: 95 %.3f 97.5 %.3f 99 %.3f' % (
            s, cp['0.9000'], cp['0.9500'], cp['0.9900'], cp['0.9990'], cp['1.0000'], cb['0.9500'], cb['0.9900'], cb['1.0000'],
            cu['0.9500'], cu['0.9750'], cu['0.9900']))
        print('            calibrated nominal pct %s -> %s ; basic %s -> %s ; upper %s -> %s' % (
            e['calibrated_nominal_percentile'], e.get('calibrated_percentile_interval'), e['calibrated_nominal_basic'],
            e.get('calibrated_basic_interval'), e['calibrated_nominal_upper_bound'], e.get('calibrated_upper_bound')))
    s3 = d['D3_sensitivities']
    print('=== D3 stratified by alpha', s3.get('stratified_by_alpha', {}).get('groups'))
    for s, v in s3.get('stratified_by_alpha', {}).get('ci', {}).items():
        print('   %-10s [%.5f, %.5f]' % (s, v[0], v[1]))
    e = s3['short_runs_left_out']
    print('=== D3 short runs left out', e['n_runs'], e['evaluated_in_short_runs'])
    for s in e['point']:
        print('   %-10s %.5f [%.5f, %.5f]' % (s, e['point'][s], e['ci'][s][0], e['ci'][s][1]))
    for m, ent in s3['m_out_of_n'].items():
        print('=== D3 m-out-of-n m =', m)
        for s, v in ent.items():
            print('   %-10s raw [%.5f, %.5f]  fpc [%.5f, %.5f]' % (s, v['interval_raw'][0], v['interval_raw'][1], v['interval_fpc'][0], v['interval_fpc'][1]))
    print('=== leave one run out', {k: (round(v['min'], 5), round(v['max'], 5)) for k, v in s3['leave_one_run_out'].items()})


def show_E():
    f = O / 'REV_E2_EXTENDED_TRUTH_v01.json'
    if not f.exists():
        f = O / 'REV_E2_EXTENDED_TRUTH_v01.partial.json'
    d = json.loads(f.read_text())
    for kk, c in d['pair_counts'].items():
        print('pairs', kk, c)
    for name, sc in d['scorings'].items():
        print('===', name, 'signed' if sc.get('signed_caution') else '', '(boot)' if sc.get('bootstrap') else '(points)')
        od = sc['oracle_diag']['all']
        print('   O: caution %.3f pp vs F0 zero-margin %.3f pp; unavoidable wrong go %.4f pp' % (od['O_caution_pp'], od['F0_g0_caution_pp'], od['no_safe_row_wrong_go_pp']))
        for pop, e in sc['pops'].items():
            dq = e['den0'].get('dec_eq_ci')
            print(' %-7s n %5d den0 %.4f pp, %.2f dec-eq %s | denE %.4f pp | denE/3s %s | den0/3s %s | E_rr0 %s' % (
                pop, e['n'], e['den0']['R_pp'], e['den0']['dec_eq'], ('[%.2f, %.2f]' % tuple(dq)) if dq else '', e['denE']['R_pp'],
                ci(e['denE_over_3s']), ci(e['den0_over_3s']), ci(e['E_rr0'])))
            for a, ent in e['arms'].items():
                print('     %-4s rr0 %-28s (b%s) rrE %-28s D %.2f dec-eq' % (a, ci(ent['rr0'], 4), ent.get('branch', '-'), ci(ent['rrE'], 4), ent['D_dec_eq']))


def show_F():
    d = json.loads((O / 'REV_F2_BRAKING_PRIOR_v01.json').read_text())
    print('cCK3 entries differing from the record:', d['S20']['cCK3_entries_differing_from_record'])
    for pop in ('all', 'moving', 'phase0', 'phase1', 'phase2', 'strat'):
        e = d['S20'][pop]
        print('=== S20', pop, 'n', e['n'], 'denE %.1f den0 %.1f dec-eq' % (e['denE_dec_eq'], e['den0_dec_eq']))
        for k, ent in e['arms'].items():
            print('   a0 %-4s rrE %-28s rr0 %-28s D %.1f dec-eq' % (k, ci(ent['rrE'], 4), ci(ent['rr0'], 4), ent['D_dec_eq']))
    print('zero margin', json.dumps(d['S20']['zero_margin_points_all']))
    print('tuning of record', json.dumps(d['S20']['tuning_runs_of_record']['rr_all']))
    print('=== S18 benign', d['S18'].get('n_runs'), d['S18'].get('selection_changed'))
    for pop in ('all', 'moving'):
        if pop in d['S18']:
            print(pop, json.dumps(d['S18'][pop])[:1800])


{'A': show_A, 'B': show_B, 'D': show_D, 'E': show_E, 'F': show_F}[sys.argv[1]]()
