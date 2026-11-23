"""Package F recount: the v02 scripts on synthetic arrays against the v01 outputs. New file, 20 Nov 2026 (Claude Fable 5.2).
With synth\\clear_v02 equal to the arrays' clearance, fr_horizon_v02.py must reproduce fr_horizon_v01.py's numbers exactly, and
fr_heldout_v02.py every value of fr_heldout_v01.py's export; the removed-contact counts must be 0.
Run first (each with python -I): fr_synth_v01.py; fr_horizon_v01.py --synth; fr_horizon_v02.py --synth;
fr_heldout_v01.py --synth --quick; fr_heldout_v02.py --synth --quick; fr_heldout_v02.py --synth --force-stop.
"""
import json, pathlib
O = pathlib.Path(__file__).resolve().parent / 'synth' / 'out'
J = lambda n: json.loads((O / n).read_text(encoding='utf-8'))
h1 = J('F_RECOUNT_HORIZON_synth.json'); h2 = J('F_RECOUNT_HORIZON_synth_clear_v02.json')
for h in ('3s', '2s'):
    for pop in ('all', 'inpath'):
        assert h1['horizons'][h][pop] == h2['horizons'][h][pop], (h, pop)
    assert h1['horizons'][h]['counts'] == h2['horizons'][h]['counts']
    for x in ('F0', 'E'):
        r = h2['horizons'][h]['removed_contacts_g1'][x]
        assert r['removed'] == 0 and r['added'] == 0 and r['pairs_unsafe_to_safe'] == 0 and r['pairs_safe_to_unsafe'] == 0
assert h1['horizon_rule']['primary_horizon_s'] == h2['horizon_rule']['primary_horizon_s']
print('horizon v02 = v01 exactly; removed counts 0')
a1 = J('A_RECOUNT_F_synth.json')['values']; a2 = J('A_RECOUNT_F_synth_v02.json')['values']
for k, v in a1.items():
    assert a2[k] == v, (k, v, a2[k])
new = sorted(set(a2) - set(a1))
print('held-out export v02 = v01 on all %d shared keys; new keys: %s' % (len(a1), new))
for k in ('F.prereg.design.R3', 'F.prereg.design.R3.ci', 'F.prereg.design.R2', 'F.prereg.design.R2.ci'):
    assert a2[k] == a2[k.replace('.prereg', '')]
s = J('A_RECOUNT_F_synth_v02_stop.json')['values']
assert s['F.status'] == 'no_room_design' and 'F.R' not in s and 'F.n_dec' not in s and s['F.clearance'] == 'departure'
print('stop export keys:', sorted(s))
print('ALL v02 SCRIPT CHECKS PASSED')
