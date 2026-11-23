"""Compare TESTOLD_A_RECOUNT_B.json with the predecessor's recount\RECOUNT_B_v01.json (every quantity both contain)."""
import json, math
HERE = r'ARS_TRIAL\revision_v13\work\B_retrack'
a = json.load(open(HERE + r'\recount_fresh\out\TESTOLD_A_RECOUNT_B.json'))
p = json.load(open(HERE + r'\recount\RECOUNT_B_v01.json'))['per_variant']
VM = {'CV': 'CV0', 'IMM': 'B1', 'CV2': 'B3', 'CA': 'B4', 'AQ': 'B2', 'IMM090': 'B1_d090', 'IMM098': 'B1_d098'}
PM = {'est_pre': 'estm1.0_before', 'est_brk': 'estm1.0_braking', 'est_stop': 'estm1.0_stopped'}
def get(v):
    r = p[v]; I = r['intervals']; P = r['populations']; mr = r['margin_ratio']
    return {'R': r['room_pp'], 'R.dec': r['room_deceq'], 'RR': r['all']['RR_N'], 'c': r['all']['RR_E5x'], 'RR_CK3': r['all']['RR_CK3'],
            'R.ci': I['R_pp']['ci'], 'RR.ci': I['RR_N']['ci'], 'c.ci': I['RR_E5x']['ci'],
            'm': mr['median'], 'A': mr['A'], 'q05': mr['q05'], 'q95': mr['q95'], 'within5': mr['share_within5'],
            'barely': r['H3']['barely_varies'], 'room_pre': P[PM['est_pre']]['R_pp'], 'room_brk': P[PM['est_brk']]['R_pp'],
            'room_stop': P[PM['est_stop']]['R_pp'], 'as_room': r['after_stop_room_deceq'], 'as_room.pp': P['truth2']['R_pp'],
            'lag': r['lag']['median_dx_pred3'], 'n_dec': r['n_eval_total'],
            'class': {'a_recovers': 'recovers', 'b_uninformative_variation': 'uninformative variation',
                      'c_amplitude_limited': 'amplitude-limited', 'd_inconclusive': 'inconclusive'}[r['H3']['cls']]}
tot = ok = 0; maxd = 0.; bad = []
def eq(x, y):
    if isinstance(x, str) or isinstance(y, str) or isinstance(x, bool): return x == y
    if x is None or y is None: return x == y
    if isinstance(x, float) and math.isnan(x): return isinstance(y, float) and math.isnan(y)
    return abs(x - y) <= 1e-9 * max(1., abs(y))
for n, v in VM.items():
    for k, pv in get(v).items():
        mv = a['B.%s.%s' % (n, k)]
        pairs = list(zip(mv, pv)) if isinstance(pv, list) else [(mv, pv)]
        for x, y in pairs:
            tot += 1
            if eq(x, y):
                ok += 1
                if not isinstance(x, (str, bool)) and x == x: maxd = max(maxd, abs(x - y) / max(1., abs(y)))
            else: bad.append((n, k, x, y))
print('compared', tot, 'agree', ok, 'max rel diff', maxd)
for b in bad: print('DIFF', b)
# rule
for x, v in (('CV2', 'B3'), ('CA', 'B4')):
    pr = p[v]
    print('rule', x, a['B.rule.' + x], 'pred:', pr.get('B3B4_rule'))
