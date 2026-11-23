"""v13 package B: comparison of the first program's outputs with the independent second program's (A10 section 10.1(c)).
New file, 19 Nov 2026 (Claude Opus 5.5). Runs after the last first-program output (10.1(d)).
First program: out\\banalysis\\B_<x>_v01.json, out\\b6\\B6_STOP_v01.json, out\\b9\\B9_CUTIN_lat1p75_v01.json.
Second program (Claude Sonnet subagent, written from the amendment and the definitions only): recount\\RECOUNT_B_v01.json.
Rule: counts exact; points and interval ends within 1e-9 (absolute for shares and pp; relative 1e-9 for values above 1); NaN = NaN;
classifications equal. Every compared item is listed with both values. Writes out\\compare\\B_COMPARE_RECOUNT_v01.json and .md.
Usage: python -I -B -X utf8 b_compare_recount_v01.py
"""
import json, math, pathlib, time
HERE = pathlib.Path(__file__).resolve().parents[1]
OUT = HERE / 'out'
RC = json.loads((HERE / 'recount' / 'RECOUNT_B_v01.json').read_text(encoding='utf-8'))
VARS = ['CV0', 'B3', 'B2', 'B4', 'B1', 'B1_d090', 'B1_d098']
CLS = {'recovers': 'a_recovers', 'uninformative variation': 'b_uninformative_variation', 'amplitude-limited': 'c_amplitude_limited',
       'inconclusive': 'd_inconclusive'}
rows = []


def num(a, b, item, count=False):
    if a is None or b is None:
        ok = a is None and b is None
    else:
        a = float(a); b = float(b)
        if math.isnan(a) or math.isnan(b):
            ok = math.isnan(a) and math.isnan(b)
        elif count:
            ok = a == b
        else:
            ok = abs(a - b) <= 1e-9 * max(1.0, abs(b))
    rows.append(dict(item=item, first=a, second=b, ok=bool(ok), kind='count' if count else 'value'))


def same(a, b, item):
    rows.append(dict(item=item, first=a, second=b, ok=bool(a == b), kind='label'))


def main():
    for x in VARS:
        p = OUT / 'banalysis' / ('B_%s_v01.json' % x)
        if not p.exists():
            rows.append(dict(item='%s: first-program file missing' % x, ok=False, kind='missing')); continue
        m = json.loads(p.read_text(encoding='utf-8')); r = RC['per_variant'][x]
        pa = m['points']['all']
        num(pa['n'], r['populations']['all']['n'], '%s n evaluated' % x, True)
        num(pa['R_pp'], r['populations']['all']['R_pp'], '%s room pp' % x)
        num(pa['R_deceq'], r['room_deceq'], '%s room dec-eq' % x)
        for a in ('N', 'NA', 'AM', 'CK3', 'Q', 'E5', 'E5p'):
            num(pa['RR'][a], r['all']['RR_' + a], '%s RR_gl(%s)' % (x, a))
        num(pa['RR']['E5x'], r['all']['RR_E5x'], '%s RR_gl(E5_x) = ceiling' % x)
        num(pa['RR']['E5px'], r['all']['RR_E5px'], '%s RR_gl(E5p_x)' % x)
        rs = m['ratio_N_F0']; rr = r['margin_ratio']
        num(rs['n'], rr['n'], '%s margin-ratio rows' % x, True)
        for k1, k2 in (('median', 'median'), ('q05', 'q05'), ('q95', 'q95'), ('A', 'A'), ('share_within_5pct', 'share_within5')):
            num(rs[k1], rr[k2], '%s margin ratio %s' % (x, k1))
        iv = m['intervals']['all']; ri = r['intervals']
        for i in (0, 1):
            num(iv['R_pp']['ci'][i], ri['R_pp']['ci'][i], '%s room pp CI[%d]' % (x, i))
            num(iv['R_deceq']['ci'][i], ri['room_deceq']['ci'][i], '%s room dec-eq CI[%d]' % (x, i))
            num(iv['RR_N']['ci'][i], ri['RR_N']['ci'][i], '%s RR_gl(N) CI[%d]' % (x, i))
            num(iv['RR_E5']['ci'][i], ri['RR_E5']['ci'][i], '%s RR_gl(E5) CI[%d]' % (x, i))
            num(iv['RR_E5x']['ci'][i], ri['RR_E5x']['ci'][i], '%s ceiling CI[%d]' % (x, i))
        num(m['points']['tru_stopped']['R_deceq'], r['after_stop_room_deceq'], '%s after-stop room dec-eq' % x)
        for mine, theirs in (('tru_before', 'truth0'), ('tru_braking', 'truth1'), ('tru_stopped', 'truth2'), ('est_before', 'estm1.0_before'),
                             ('est_braking', 'estm1.0_braking'), ('est_stopped', 'estm1.0_stopped'), ('est05_braking', 'estm0.5_braking'),
                             ('est20_braking', 'estm2.0_braking')):
            pm = m['points'][mine]; pr = r['populations'][theirs]
            num(pm['n'], pr['n'], '%s %s n' % (x, mine), True)
            num(pm['R_deceq'], pr['room_deceq'], '%s %s room dec-eq' % (x, mine))
            num(pm['RR']['N'], pr['RR_N'], '%s %s RR_gl(N)' % (x, mine))
        g = m['grid_points']['all']; gr = r['grid']
        num(g['R_pp'], gr['R_pp'], '%s grid room pp' % x)
        for a in ('N', 'NA', 'AM', 'CK3', 'Q'):
            num(g['RR'][a], gr['RR_' + a], '%s grid RR(%s)' % (x, a))
        num(m['lag_dx3_first_second_after_stop']['n'], r['lag']['n'], '%s lag n' % x, True)
        num(m['lag_dx3_first_second_after_stop']['median'], r['lag']['median_dx_pred3'], '%s lag median' % x)
        same(CLS[m['classification_exploratory']['classification']], r['H3']['cls'], '%s H3-style class' % x)
        same(bool(m['classification_exploratory']['barely_varies']), bool(r['H3']['barely_varies']), '%s barely varies' % x)
    # NIS / NEES by phase: B_ANALYSIS_DEFINITIONS Amendment 1 (first program out\b8\B8_NIS_NEES_v01.json; second: nis_nees_amend1)
    p8 = OUT / 'b8' / 'B8_NIS_NEES_v01.json'
    if p8.exists():
        m8 = json.loads(p8.read_text(encoding='utf-8'))
        for x in VARS:
            r = RC['per_variant'][x].get('nis_nees_amend1')
            if r is None:
                rows.append(dict(item='%s NIS/NEES amendment 1: second program missing' % x, ok=False, kind='missing')); continue
            for mine, theirs in (('tru_phase0', 'truth0'), ('tru_phase1', 'truth1'), ('tru_phase2', 'truth2'), ('est_phase0', 'est_before'),
                                 ('est_phase1', 'est_braking'), ('est_phase2', 'est_stopped')):
                for key, rk in (('NIS', 'nis'), ('NEES_v', 'nees')):
                    a = m8['variants'][x][mine][key]; b = r[rk][theirs]
                    num(a['n'], b['n'], '%s %s %s n' % (x, key, mine), True)
                    num(a['mean'], b['mean'], '%s %s %s mean' % (x, key, mine))
                    for i in (0, 1):
                        num(a['mean_ci'][i], b['ci'][i], '%s %s %s mean CI[%d]' % (x, key, mine, i))
    # B2 oracle check (post hoc)
    pb2 = OUT / 'banalysis' / 'B2_ORACLE_CHECK_v01.json'
    if pb2.exists() and 'B2_oracle_check' in RC:
        m = json.loads(pb2.read_text(encoding='utf-8')); r = RC['B2_oracle_check']
        num(m['diagnostics']['share_rows_outside_band'], r['b_outside_share'], 'B2 oracle: share of rows outside the band')
        for i in (0, 1):
            num(m['diagnostics']['ratio_q01_q99'][i], r['b_ratio_q01_q99'][i], 'B2 oracle: ratio q01/q99 [%d]' % i)
        num(m['diagnostics']['within_decision_spread']['n_decisions'], r['c']['n_decisions'], 'B2 oracle: decisions with >= 2 rows', True)
        num(m['diagnostics']['within_decision_spread']['median'], r['c']['median'], 'B2 oracle: within-decision spread median')
        num(m['diagnostics']['within_decision_spread']['q90'], r['c']['p90'], 'B2 oracle: within-decision spread q90')
        num(m['diagnostics']['within_decision_spread']['share_above_5pct'], r['c']['share_gt_0p05'], 'B2 oracle: share above 5%')
        for mk, rk in (('diff_N_minus_E5x', 'a_RRN_minus_RRE5x'), ('RR_E5q', 'd_RR_E5q'), ('diff_N_minus_E5q', 'd_RRN_minus_RRE5q')):
            num(m['intervals'][mk]['point'], r[rk]['point'], 'B2 oracle: %s point' % mk)
            for i in (0, 1):
                num(m['intervals'][mk]['ci'][i], r[rk]['ci'][i], 'B2 oracle: %s CI[%d]' % (mk, i))
    # oracle checks for every tracker (N - E5_x; post hoc E5q)
    if 'oracle_check' in RC:
        for x in VARS:
            po = OUT / 'banalysis' / ('%s_ORACLE_CHECK_v01.json' % x)
            r = RC['oracle_check'].get(x)
            if not po.exists() or r is None:
                rows.append(dict(item='%s oracle check missing (first %s, second %s)' % (x, po.exists(), r is not None), ok=False, kind='missing')); continue
            m = json.loads(po.read_text(encoding='utf-8'))
            num(m['diagnostics']['share_rows_outside_band'], r['b_outside_share'], '%s oracle: share outside band' % x)
            for mk, rk in (('diff_N_minus_E5x', 'a_RRN_minus_RRE5x'), ('RR_E5q', 'd_RR_E5q'), ('diff_N_minus_E5q', 'd_RRN_minus_RRE5q')):
                num(m['intervals'][mk]['point'], r[rk]['point'], '%s oracle: %s point' % (x, mk))
                for i in (0, 1):
                    num(m['intervals'][mk]['ci'][i], r[rk]['ci'][i], '%s oracle: %s CI[%d]' % (x, mk, i))
    # B6
    p6 = OUT / 'b6' / 'B6_STOP_v01.json'
    if p6.exists():
        m = json.loads(p6.read_text(encoding='utf-8')); r6 = RC['B6']
        names = {'tercile 1': 'T1', 'tercile 2': 'T2', 'tercile 3': 'T3'}
        for t in m['terciles']:
            if t['name'] == 'all':
                rt = r6['all35']
            else:
                rt = r6['terciles'][names[t['name']]]
                same(sorted(t['runs']), sorted(rt['runs']), 'B6 %s membership' % t['name'])
            num(t['W_R']['R_deceq'], rt['WR']['room_deceq'], 'B6 %s W_R room dec-eq' % t['name'])
            num(t['W1']['R_deceq'], rt['room3s']['room_deceq'], 'B6 %s 3 s room dec-eq' % t['name'])
            num(t['W_R']['den0_deceq'], rt['WR']['den0_deceq'], 'B6 %s den0 dec-eq' % t['name'])
            same(bool(t['W_R']['evaluable_den0']), bool(rt['WR']['evaluable_den0_ge10']), 'B6 %s evaluable' % t['name'])
            for a in ('N', 'CK3'):
                num(t['W_R']['RR'][a], rt['WR']['RR_' + a], 'B6 %s W_R RR_gl(%s)' % (t['name'], a))
        d = m['delayed_stop']; rd = r6['delayed']['gridless']
        num(d['R_pp'], rd['R_pp'], 'B6(b) delayed-stop room pp')
        num(d['R_deceq'], rd['room_deceq'], 'B6(b) delayed-stop room dec-eq')
        num(d['den0_deceq'], rd['den0_deceq'], 'B6(b) delayed-stop den0 dec-eq')
        for a in ('N', 'NA', 'AM', 'CK3', 'Q'):
            num(d['RR'][a], rd['RR_' + a], 'B6(b) delayed-stop RR_gl(%s)' % a)
        num(r6['b6b_tau_max_abs_diff'], 0.0, 'B6(b) tau draw: second program vs stored (max abs diff)')
    # B9
    p9 = OUT / 'b9' / 'B9_CUTIN_lat1p75_v01.json'
    if p9.exists():
        m = json.loads(p9.read_text(encoding='utf-8')); r9 = RC['B9']
        num(m['events_found'], r9['runs_with_event'], 'B9 events found', True)
        num(sum(x['n_window'] for x in m['runs']), r9['window_total'], 'B9 window decisions', True)
        for mine, theirs in (('<1s', 's_lt1'), ('1-4s', 's_1_4'), ('>=4s', 's_ge4'), ('untracked', 'untracked')):
            num(sum(x['window_strata'][mine] for x in m['runs']), r9['strata_totals'][theirs], 'B9 window stratum %s' % mine, True)
        num(m['gridless']['window']['R_pp'], r9['populations']['window']['R_pp'], 'B9 window room pp')
        num(m['ratio_window_all']['median'], r9['populations']['window']['margin']['median'], 'B9 window margin ratio median')
        num(m['ratio_window_all']['n'], r9['populations']['window']['margin']['n'], 'B9 window margin-ratio rows', True)
    bad = [x for x in rows if not x['ok']]
    doc = dict(code='b_compare_recount_v01.py', written=time.strftime('%Y-%m-%d %H:%M:%S'), second_program='recount\\RECOUNT_B_v01.json (written %s)' % RC['written'],
               n_items=len(rows), n_agree=len(rows) - len(bad), disagreements=bad, items=rows)
    od = OUT / 'compare'; od.mkdir(parents=True, exist_ok=True)
    (od / 'B_COMPARE_RECOUNT_v01.json').write_text(json.dumps(doc, indent=1, default=str), encoding='utf-8')
    L = ['# Package B: first program vs independent second program — %s' % doc['written'], '',
         'Items compared: %d; agree: %d; disagree: %d.' % (len(rows), len(rows) - len(bad), len(bad)), '']
    if bad:
        L += ['| Item | First | Second |', '|---|---|---|'] + ['| %s | %s | %s |' % (b['item'], b.get('first'), b.get('second')) for b in bad]
    (od / 'B_COMPARE_RECOUNT_v01.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('\n'.join(L[:60]))


if __name__ == '__main__':
    main()
