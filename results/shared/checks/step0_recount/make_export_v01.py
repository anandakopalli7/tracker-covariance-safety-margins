"""Builds A_RECOUNT_S0.json (45 keys) from this recount's own STEP0_RECOUNT_v01.json. Does not read the first program's files."""
import json
D = r'ARS_TRIAL\revision_v13\work\shared\checks\step0_recount'
r = json.load(open(D + r'\STEP0_RECOUNT_v01.json'))
v = {}
for P, fam in (('VC', 'vehicle_crossing'), ('PC', 'pedestrian_crossing')):
    for pre, sn in (('S0', 'all'), ('S0T', 'tuning')):
        x = r['%s|%s' % (fam, sn)]; k = '%s.%s.' % (pre, P)
        v[k + 'n_runs'] = x['n_runs']; v[k + 'n_dec'] = x['n_eval_decisions']
        v[k + 'R'] = x['R_pp']; v[k + 'R.ci'] = x['R_pp_ci']['ci95']; v[k + 'R_deceq'] = x['R_deceq']
        v[k + 'RR_N'] = x['RR_N']['point']; v[k + 'RR_N.ci'] = x['RR_N']['ci95']
        v[k + 'RR_E5N'] = x['RR_E5N']['point']; v[k + 'RR_E5N.ci'] = x['RR_E5N']['ci95']
        v[k + 'nobind'] = x['share_no_binding_F0']; v[k + 'unsafe3s'] = x['share_some_row_unsafe_3s']
v['S0.LB.R'] = r['lead_braking|tuning']['R_pp']
assert len(v) == 45
json.dump(dict(values=v), open(D + r'\A_RECOUNT_S0.json', 'w'), indent=1)
print(len(v))
