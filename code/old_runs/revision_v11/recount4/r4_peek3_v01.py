"""Recount4 helper (after the own results were written): arms, bootstrap flags and oracle diagnostics per scoring of the first program's file."""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
F = HERE.parent / 'analysis' / 'out' / 'REV_E2_EXTENDED_TRUTH_v01.json'
d = json.loads(F.read_text(encoding='utf-8'))
for name, sc in d['scorings'].items():
    print('==', name, '| signed_caution', sc['signed_caution'], '| bootstrap', json.dumps(sc['bootstrap']), '| arms', {pn: list(pe['arms'].keys()) for pn, pe in sc['pops'].items()}['all'],
          '| arms equal over pops', len(set(tuple(pe['arms'].keys()) for pe in sc['pops'].values())) == 1)
print(json.dumps(d['scorings']['est_t0p75_a6p0']['oracle_diag'], indent=1))
print(json.dumps(d['scorings']['est_t0p50_a6p0']['pops']['all']['den0'], indent=1))
print(json.dumps(d['scorings']['est_t0p75_a6p0']['pops']['phase0'], indent=1)[:3000])
for k, v in d['pair_counts'].items():
    print(k, v)
