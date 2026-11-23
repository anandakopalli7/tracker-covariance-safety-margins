"""Read-only check: run package A's own outcome rules (A_text/gen/outcomes_v13.py classify, compare_reported) on CD's exports, in
memory, and list A's recomputed statuses for C and D next to the statuses CD exports. Writes nothing into A's folder (run with -B so
no bytecode is written); writes out/[TESTOLD_]CHECK_A_OUTCOMES_v13.json here. New file, 21 Nov 2026 (Claude Opus 5.5).
Usage: python -I -B check_a_outcomes_v13.py [EXPORT_C.json EXPORT_D.json] [--out NAME]
"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
GEN = CD.parent / 'A_text' / 'gen'
sys.dont_write_bytecode = True
sys.path.insert(0, str(GEN))
import outcomes_v13 as AO  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith('--')]
fc = pathlib.Path(args[0]) if args else CD / 'out' / 'A_EXPORT_C.json'
fd = pathlib.Path(args[1]) if len(args) > 1 else CD / 'out' / 'A_EXPORT_D.json'
outn = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else 'CHECK_A_OUTCOMES_v13.json'
C = json.loads(fc.read_text(encoding='utf-8'))['values']; D = json.loads(fd.read_text(encoding='utf-8'))['values']
v = AO.Values(fixture={'C': C, 'D': D})
o = AO.classify(v)
bad = AO.compare_reported(o, v)
keys = ['H0', 'H1', 'H2', 'H3', 'H3.barely', 'H4', 'H5', 'K0', 'K1', 'K2', 'K2.barely'] + [k for k in o if k.startswith(('DH1', 'DH2'))]
names = {'H3.barely': 'LB.IMM.barely', 'K2.barely': 'CI.Y.barely'}
rep = {}
for h in keys:
    k = names.get(h) or (('LB.' if h.startswith('H') else 'CI.') + h if h[0] in 'HK' else 'D1.%s.%s' % (h.split('.')[1], h.split('.')[0]))
    rep[k] = (C if h[0] in 'HK' else D).get(k, '(not exported)')
res = dict(export_C=str(fc), export_D=str(fd), a_recomputed={k: o.get(k) for k in keys},
           a_confirmation={k: o.get(k) for k in o if k.startswith('conf.') and k[5:] in keys},
           cd_reported=rep, mismatches_by_a_rule=bad, verdict='AGREE' if not bad else 'MISMATCH')
(CD / 'out' / outn).write_text(json.dumps(res, indent=1, default=str), encoding='utf-8')
print(json.dumps(res, indent=1, default=str))
