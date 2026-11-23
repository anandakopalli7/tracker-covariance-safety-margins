"""Recount (second program), probe of the stored arrays. Read-only on the data project."""
import json, pathlib, sys
import numpy as np

P = pathlib.Path(r'<library folder>')
STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
EXTRACT = P / '11_ojits' / 'A4' / 'fit' / 'extract'
CACHE = P / '11_ojits' / 'review' / 'optionA_recount_v01' / 'cache'
A4 = P / '11_ojits' / 'A4' / 'fit' / 'analysis' / 'A4_RESULTS_FIT_v01.json'

files = sorted(STORED.glob('*.npz'))
print('stored files', len(files))
run = 'p1b_fit_finite_0005'
for name, folder, fn in (('stored', STORED, run + '.npz'), ('extract', EXTRACT, run + '.npz'), ('cache', CACHE, run + '_pack.npz')):
    z = np.load(folder / fn, allow_pickle=False)
    print('==', name)
    for k in z.files:
        a = z[k]
        if a.ndim == 0:
            s = str(a)
            print('  ', k, a.dtype, 'scalar', s[:600])
        else:
            extra = ''
            if a.dtype.kind in 'fiub':
                af = a.astype(float)
                extra = 'nan=%d min=%s max=%s' % (int(np.isnan(af).sum()), np.nanmin(af) if af.size else None, np.nanmax(af) if af.size else None)
            print('  ', k, a.dtype, a.shape, extra)
j = json.loads(A4.read_text(encoding='utf-8'))
print('A4 keys', list(j.keys())[:40])
sp = j['splits']
print('splits keys', list(sp.keys()))
al = sp['alpha']
print('alpha keys', list(al.keys()))
for a, v in al.items():
    print(a, type(v), list(v.keys()) if isinstance(v, dict) else v)
    if isinstance(v, dict) and 'runs' in v:
        print('   runs', len(v['runs']), v['runs'])
fam = {}
for f in files:
    with np.load(f, allow_pickle=False) as z:
        m = json.loads(str(z['meta']))
    fam.setdefault((m.get('family'), m.get('set')), []).append(f.stem)
for k, v in sorted(fam.items(), key=lambda t: str(t[0])):
    print(k, len(v), v[0], v[-1])
