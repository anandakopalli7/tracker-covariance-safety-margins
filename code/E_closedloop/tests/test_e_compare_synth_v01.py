"""Test of the E3/E3b result path on the SYNTHETIC set the second program built (recount/test/synth, from make_synth.py),
before any real E3 value exists: first program (e_collect_v01 -> e3_analyse_v01) vs the second program's stored compare
(recount/test/cmp.json, low_power False), through e_compare_v01.

The Lock 2 guard of e_collect / e3_analyse protects real E3 / E3b runs; here the RUNS folder points at the synthetic set and the
guard's path at a stand-in file inside tests/out, so no real run is read. Outputs: tests/out/SYNTH_*.json.

python -I -B tests/test_e_compare_synth_v01.py
"""
import json, pathlib, sys, tempfile

E = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(E / 'analysis'))
import e_collect_v01 as EC, e3_analyse_v01 as EA, e_compare_v01 as CMP   # noqa: E402

OUT = E / 'tests' / 'out'; OUT.mkdir(exist_ok=True)
SYN = E / 'recount' / 'test' / 'synth'
stand_in = OUT / 'SYNTH_LOCK2_STAND_IN.txt'
stand_in.write_text('stand-in for the Lock 2 guard: synthetic test data only\n', encoding='utf-8')
EC.LOCK2 = stand_in; EA.LOCK2 = stand_in
assert 'synth' in str(SYN)


def collect(stage, folder):
    EC.RUNS = SYN / folder
    out = OUT / f'SYNTH_OUTCOMES_{stage.upper()}.json'
    sys.argv = ['e_collect_v01.py', stage, '--out', str(out)]
    EC.main(); return out


o3 = collect('e3', 'e3'); o3b = collect('e3b', 'e3b')
# low_power False, as the stored recount compare was made with --low-power false
lp = OUT / 'SYNTH_LOCK2B_STAND_IN.json'
lp.write_text(json.dumps({'levels': {'low_power': False}}), encoding='utf-8')
res = OUT / 'SYNTH_E3_RESULTS.json'
sys.argv = ['e3_analyse_v01.py', '--e3', str(o3), '--e3b', str(o3b), '--lock2b', str(lp), '--out', str(res)]
EA.main()
r = CMP.comparisons(res, E / 'recount' / 'test' / 'cmp.json')
(OUT / 'SYNTH_COMPARE_RESULTS.json').write_text(json.dumps(r, indent=1, default=str), encoding='utf-8')
print('RESULTS compared', r['comparisons_compared'], 'disagreements', r['disagreements'], 'extras', [x['label'] for x in r['extras_in_recount']])
for d in r['list'][:15]: print('  ', d)
for st, f, theirs in (('e3', o3, 'o_e3.json'), ('e3b', o3b, 'o_e3b.json')):
    ro = CMP.outcomes(f, E / 'recount' / 'test' / theirs)
    print('OUTCOMES', st, 'runs', ro['runs_compared'], 'disagreements', ro['disagreements'], ro['by_field'])
    for d in ro['list'][:5]: print('  ', d)
