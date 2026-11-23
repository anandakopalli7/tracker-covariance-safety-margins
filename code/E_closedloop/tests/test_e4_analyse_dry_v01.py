"""Dry run of analysis/e4_analyse_v01.py before any E4 run: E3's lo/hi runs of the four E4 arms relabelled as E4 (masked_share
0.2), the lock gate pointed at a stand-in in tests/out. Expected: N-vs-F0 and NIMM-vs-F0IMM classes equal E3's; degradation and
difference-in-differences exactly 0 (every 'E4' run is its own E3 twin)."""
import json, pathlib, sys
E = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(E / 'analysis'))
import e4_analyse_v01 as A
OUT = E / 'tests' / 'out' / 'e4_dry'; OUT.mkdir(parents=True, exist_ok=True)
for f in OUT.glob('*.json'): f.unlink()
stand = OUT / 'LOCK_STAND_IN.txt'; stand.write_text('stand-in: dry run on relabelled E3 values\n'); A.LOCK = stand
e3 = [r for r in json.load(open(E / 'out' / 'OUTCOMES_E3_v01.json'))['runs'] if r['arm'] in A.ARM]
A.collect = lambda punish: [dict(r, job=r['job'].replace('e3_', 'e4_'), masked_share=0.2) for r in e3]
A.jobs_expected = lambda: {lv: [r['job'].replace('e3_', 'e4_') for r in e3 if r['level'] == lv] for lv in ('lo', 'hi')}
sys.argv = ['x', '--punish-num', '7', '--out-dir', str(OUT)]
A.main()
x = json.load(open(OUT / 'A_EXPORT_E4.json'))['values']
print('keys', len(x), 'E4H1', x.get('E4H1'), 'E4H2', x.get('E4H2'))
print('deg nonzero', [k for k in x if k.startswith('E4.deg') and k.endswith('.dc') and x[k] not in (0, 0.0)])
print('did nonzero', [k for k in x if k.startswith('E4.did') and k.endswith('.dc') and x[k] not in (0, 0.0)])
r3 = {(c['arm'], c['level_arm']): c['classification'] for c in json.load(open(E / 'out' / 'E3_RESULTS_v01.json'))['comparisons']}
print('classes equal E3:', x['E4.N.lo.class'] == r3[('E_N', 'lo')], x['E4.NIMM.lo.class'] == r3[('E_N_IMM', 'lo')], x['E4.N.hi.class'] == r3[('E_N', 'hi')], x['E4.NIMM.hi.class'] == r3[('E_N_IMM', 'hi')])
