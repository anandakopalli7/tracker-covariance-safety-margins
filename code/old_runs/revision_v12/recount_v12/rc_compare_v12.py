"""Compare the recount values (RECOUNT_VALUES_v12.json, saved before any first-program JSON was opened) with the first program's
outputs in revision_v12/analysis/out. Writes RECOUNT_COMPARE_TABLE_v12.json (rows) and prints a markdown table body.
Usage: python -B -X utf8 rc_compare_v12.py
"""
import json, pathlib, math
HERE = pathlib.Path(__file__).resolve().parent
OUTA = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis\out')
V = json.loads((HERE / 'RECOUNT_VALUES_v12.json').read_text(encoding='utf-8'))
F = {k: json.loads((OUTA / f).read_text(encoding='utf-8')) for k, f in (
    ('1', 'A9_1_PLACEBO_GRIDLESS_v01.json'), ('3', 'A9_3_PHASE_SCALE_CV_v01.json'), ('4b', 'A9_4B_ATTRIBUTION_v01.json'),
    ('5', 'A9_5_TUNING_RUNS_v01.json'), ('6', 'A9_6_STOP_RELIANCE_v01.json'), ('7b', 'A9_7B_TIMEGAP_SCORE_v01.json'))}
TOL = 1e-9
rows = []


def add(sec, name, mine, first, integer=False):
    if isinstance(mine, (list, tuple)):
        for i, (a, b) in enumerate(zip(mine, first)):
            add(sec, '%s[%d]' % (name, i), a, b, integer)
        return
    a = float(mine); b = float(first)
    d = abs(a - b) if (math.isfinite(a) and math.isfinite(b)) else (0. if (a == b or (math.isnan(a) and math.isnan(b))) else float('inf'))
    flag = (d != 0) if integer else (d > TOL)
    rows.append(dict(section=sec, name=name, recount=a, first=b, abs_diff=d, flag=bool(flag)))


POPS = ['all', 'moving', 'phase0', 'phase1', 'phase2']
# ---------------------------------------------------------------- A9-1 (a)
for p in POPS:
    m = V['A9_1a'][p]; f = F['1']['a_placebo_grid'][p]
    add('A9-1a', '%s n' % p, m['n'], f['n'], True)
    add('A9-1a', '%s R (pp)' % p, m['R_pp'], f['R']['point'])
    add('A9-1a', '%s RR(N)' % p, m['RR_N'], f['RR_N']['point'])
    add('A9-1a', '%s RR(P)' % p, m['RR_P'], f['RR_P']['point'])
    add('A9-1a', '%s RR(N)-RR(P)' % p, m['RR_N_minus_RR_P'], f['RR_N_minus_P']['point'])
    add('A9-1a', '%s D(N,F0) dec-eq' % p, m['D_N_F0_dec_eq'], f['D_N_deceq']['point'])
    add('A9-1a', '%s D(P,F0) dec-eq' % p, m['D_P_F0_dec_eq'], f['D_P_deceq']['point'])
# ---------------------------------------------------------------- A9-1 (b)
fb = F['1']['b_offset_family']
for u, rr in zip(fb['u'], fb['RR']):
    add('A9-1b', 'RR offset u=%.2f' % u, V['A9_1b']['RR_by_u']['%.2f' % u], rr)
add('A9-1b', 'RR offset min', V['A9_1b']['min'], fb['RR_min_max'][0])
add('A9-1b', 'RR offset max', V['A9_1b']['max'], fb['RR_min_max'][1])
# ---------------------------------------------------------------- A9-1 (c)
for p in POPS:
    m = V['A9_1c'][p]; f = F['1']['c_gridless'][p]
    add('A9-1c', '%s R (pp)' % p, m['R_pp'], f['R_pp'])
    for a in ['N', 'P', 'NA', 'A1', 'CK3', 'Q']:
        add('A9-1c', '%s RR(%s)' % (p, a), m['RR_' + a], f['RR_' + a])
    add('A9-1c', '%s D(N,F0) dec-eq' % p, m['D_N_F0_dec_eq'], f['D_N_deceq'])
    add('A9-1c', '%s D(P,F0) dec-eq' % p, m['D_P_F0_dec_eq'], f['D_P_deceq'])
    add('A9-1c', '%s D(N,P) dec-eq' % p, m['D_N_P_dec_eq'], f['D_N_minus_P_deceq'])
for a in ['F0', 'E', 'N', 'P', 'NA', 'A1', 'CK3', 'Q']:
    add('A9-1c', 'number of gridless points %s' % a, V['A9_1c']['all']['n_points'][a], F['1']['c_gridless']['all']['n_points'][a], True)
# ---------------------------------------------------------------- A9-3
m3 = V['A9_3']; f3 = F['3']
add('A9-3', 'R (pp), pooled', m3['R_pp'], f3['a_truth_phase']['insample']['R_pp'])
for tag, ft in (('a_truth_phase', f3['a_truth_phase']), ('b_estimated_phase', f3['b_estimated_phase']['-1.0'])):
    m = m3[tag]; lab = 'truth phase' if tag.startswith('a') else 'estimated phase'
    add('A9-3', '%s in-sample gain (pp)' % lab, m['gain_in_pp'], ft['insample']['gain_pp'])
    add('A9-3', '%s in-sample gain share of R' % lab, m['gain_in_share'], ft['insample']['share'])
    add('A9-3', '%s LORO G_cv share' % lab, m['G_cv_share'], ft['loro']['G_cv_share'])
    add('A9-3', '%s LORO G_cv (pp)' % lab, m['G_cv_pp'], ft['loro']['G_cv_pp'])
    add('A9-3', '%s LORO G_cv_vs_in share' % lab, m['G_cv_vs_in_share'], ft['loro']['G_cv_vs_in_share'])
    add('A9-3', '%s LORO G_cv_vs_in (pp)' % lab, m['G_cv_vs_in_pp'], ft['loro']['G_cv_vs_in_pp'])
    add('A9-3', '%s LORO sum(F1_cv - F1_in)' % lab, -m['single_cv_vs_in_sum'], ft['loro']['raw']['F1cv_minus_F1'])
    add('A9-3', '%s LORO run-level pairs without a qualifying triple' % lab, m['run_level_pairs_without_choice_ps'],
        ft['loro']['raw']['none_ps'], True)
    add('A9-3', '%s LORO run-level pairs without a qualifying single scale' % lab, m['run_level_pairs_without_choice_single'],
        ft['loro']['raw']['none_1'], True)
add('A9-3', 'estimated phase agreement with truth', m3['b_agreement'], f3['b_estimated_phase']['-1.0']['agreement'])
cmm = m3['b_confusion_truth_rows_est_cols']; cmf = f3['b_estimated_phase']['-1.0']['confusion_truth_rows_estimate_cols']
for t in range(3):
    for e in range(3):
        add('A9-3', 'confusion truth %d / estimated %d' % (t, e), cmm[t][e], cmf[t][e], True)
# ---------------------------------------------------------------- A9-4 (b)
tb_m = ['before the stop', '[0,1)', '[1,2)', '[2,5)', '[5,10)', '>=10']
tb_f = F['4b']['ts_bins']
vb_m = ['vhat<=0.5', '(0.5,1]', '(1,2]', '>2']
vb_f = F['4b']['vh_bins']
for pm, pf in (('all', 'all'), ('after_stop_phase2', 'after_stop')):
    for a in ['E', 'CK3', 'A1', 'N']:
        m = V['A9_4b'][pm][a]; f = F['4b']['b_attribution'][pf][a]
        add('A9-4b', '%s %s total (dec-eq)' % (pf, a), m['total_dec_eq'], f['attributed_total'])
        add('A9-4b', '%s %s D dec-eq of record' % (pf, a), m['dec_eq_of_record'], f['D_deceq'])
        for bm, bf in zip(tb_m, tb_f):
            add('A9-4b', '%s %s time since stop %s' % (pf, a, bf), m['by_time_since_stop'][bm], f['by_time_since_stop'][bf])
        for bm, bf in zip(vb_m, vb_f):
            add('A9-4b', '%s %s lead speed estimate %s' % (pf, a, bf), m['by_vhat'][bm], f['by_vhat'][bf])
# ---------------------------------------------------------------- A9-5
m5 = V['A9_5']; f5 = F['5']['tuning']
add('A9-5', 'number of tuning runs', m5['n_runs'], f5['n_runs'], True)
for p in POPS:
    m = m5['pops'][p]; f = f5[p]
    add('A9-5', '%s n' % p, m['n'], f['n'], True)
    add('A9-5', '%s R (pp)' % p, m['R_pp'], f['R_pp'])
    for a in ['N', 'NA', 'A1', 'CK3', 'Q']:
        add('A9-5', '%s RR(%s)' % (p, a), m['RR_' + a], f['RR_' + a])
add('A9-5', 'decision-weighted mean phase room (pp)', m5['phase_room_decision_weighted_mean_pp'], f5['phase_weighted_room_pp'])
add('A9-5', 'pooled room / weighted phase room', m5['ratio_pooled_room_to_weighted_phase_mean'], f5['pooled_over_phase_weighted'])
# ---------------------------------------------------------------- A9-6
for p in POPS:
    for a in ['F0', 'E', 'N', 'NA', 'A1', 'CK3', 'O']:
        add('A9-6', '%s %s share W1-unsafe but stop-safe' % (p, a), V['A9_6']['pops'][p][a],
            F['6']['reliance'][p][a]['share_safe_only_with_stop'])
# ---------------------------------------------------------------- A9-7
for p in POPS:
    m = V['A9_7'][p]; f = F['7b']['w1'][p]
    add('A9-7', '%s R (pp)' % p, m['R_pp'], f['R_pp'])
    for a in ['TG2', 'TG1', 'TG4']:
        add('A9-7', '%s RR(%s)' % (p, a), m['RR_' + a], f['RR_' + a]['point'])
    add('A9-7', '%s D(TG2,F0) dec-eq' % p, m['D_TG2_dec_eq'], f['D_TG2_deceq'])

(HERE / 'RECOUNT_COMPARE_TABLE_v12.json').write_text(json.dumps(rows, indent=1), encoding='utf-8')
n = len(rows); nf = sum(r['flag'] for r in rows)
print('compared %d, agree %d, flagged %d' % (n, n - nf, nf))
lines = []
cur = None
for r in rows:
    if r['section'] != cur:
        cur = r['section']
        lines.append('\n### %s\n\n| Value | Recount | First program | Abs. difference | Flag |\n|---|---|---|---|---|' % cur)
    lines.append('| %s | %.17g | %.17g | %.3g | %s |' % (r['name'], r['recount'], r['first'], r['abs_diff'],
                                                       '**DIFFERS**' if r['flag'] else ''))
(HERE / 'rc_compare_rows_v12.md.txt').write_text('\n'.join(lines), encoding='utf-8')
for r in rows:
    if r['flag']:
        print('FLAG', r['section'], r['name'], r['recount'], r['first'], r['abs_diff'])
