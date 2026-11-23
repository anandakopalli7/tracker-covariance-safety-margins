import json, math
B = r'ARS_TRIAL\revision_v13\work\B_retrack'
V12 = r'ARS_TRIAL\revision_v12\analysis\out'
b6 = json.load(open(B + r'\recount_fresh\out\part_testold_b6.json')); tu = json.load(open(B + r'\recount_fresh\out\part_tu.json'))
r, x = b6['res'], b6['sens']
pre = json.load(open(B + r'\recount\RECOUNT_B_v01.json'))['B6']
st = json.load(open(B + r'\out\b6\B6_STOP_v01.json'))
v12 = json.load(open(V12 + r'\A9_6_STOP_RELIANCE_v01.json'))['reliance']['all']
v95 = json.load(open(V12 + r'\A9_5_TUNING_RUNS_v01.json'))['tuning']
tot = ok = 0; bad = []; mx = 0.
def chk(lab, a, b, tol=1e-9):
    global tot, ok, mx
    tot += 1
    if isinstance(a, (str, bool)) or isinstance(b, (str, bool)): good = (a == b)
    else:
        good = (a != a and b != b) or abs(a - b) <= tol * max(1., abs(b))
        if a == a and b == b: mx = max(mx, abs(a - b) / max(1., abs(b)))
    ok += good
    if not good: bad.append((lab, a, b))
d = pre['delayed']['gridless']; pt = pre['all35']['WR']
sc = x['stopcache61']; d61 = x['ds61']
chk('cache61 R_pp vs pred', sc['R_pp_WR'], pt['R_pp']); chk('cache61 den0 vs pred', sc['den0_dec'], pt['den0_deceq'])
chk('cache61 R_pp vs STOP', sc['R_pp_WR'], st['fixed_tau_0p75_point']['R_pp'])
chk('DS61 R_pp vs pred', d61['R_pp'], d['R_pp']); chk('DS61 den0 vs pred', d61['den0_dec'], d['den0_deceq'])
chk('DS61 R_pp vs STOP', d61['R_pp'], st['delayed_stop']['R_pp'])
chk('tau diff', x['tau_max_abs_diff'], 0.0)
for i in (1, 2, 3):
    t = pre['terciles']['T%d' % i]; k = 'LB.T%d.' % i; e = x['T%d' % i]
    chk(k + 'range', r[k + 'range'], '%.2f–%.2f' % tuple(t['decel_range'])); chk(k + 'n', e['n'], t['WR']['n'])
chk('range lo vs STOP', x['decel_range'][0], st['terciles'][0]['decel_min_max'][0]); chk('range hi', x['decel_range'][1], st['terciles'][0]['decel_min_max'][1])
print('B6 compared', tot, 'agree', ok, 'maxrel', mx)
for b in bad: print('DIFF', b)
print('REL stop-cache sensitivity:', x['REL_stopcache61'])
print('REL ext vs v12:')
t2 = ok2 = 0
for k in ('F0', 'N', 'CK3'):
    a = r['LB.REL_' + k]; b = v12[k]['share_safe_only_with_stop']; t2 += 1; ok2 += abs(a - b) <= 1e-9; print(' ', k, a, b, a - b)
print('REL ext compared', t2, 'agree', ok2)
# TU grid
t3 = ok3 = 0; g = tu['sens']['grid']
for lab in ('all', 'phase0', 'phase1', 'phase2'):
    for key in ('n', 'R_pp', 'RR_N', 'RR_NA', 'RR_AM', 'RR_CK3', 'RR_Q'):
        a = g[lab][key]; b = v95[lab][key.replace('AM', 'A1')] if key != 'n' else v95[lab]['n']
        t3 += 1; good = abs(a - b) <= 1e-9 * max(1., abs(b)); ok3 += good
        if not good: print(' TU DIFF', lab, key, a, b)
print('TU grid compared', t3, 'agree', ok3)
print({k: v for k, v in tu['res'].items()})
