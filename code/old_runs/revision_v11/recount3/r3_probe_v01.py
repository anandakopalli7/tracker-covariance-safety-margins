"""Recount3: probe of the inputs (keys, shapes, families). Reads only; prints."""
import json, pathlib, sys
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'recount'))
import rc_lib_v01 as L   # noqa: E402

R2 = HERE.parent / 'recount2' / 'out'
CK = HERE.parent / 'analysis' / 'out' / 'ck'

run = L.RUNS[0]
for name, f in (('stored', L.STORED / (run + '.npz')), ('extract', L.EXTRACT / (run + '.npz')), ('pack', L.CACHE / (run + '_pack.npz')),
                ('recount2', R2 / (run + '.npz')), ('ck', CK / (run + '.npz'))):
    z = np.load(f, allow_pickle=False)
    print('==', name, f)
    for k in z.files:
        a = z[k]
        print('   %-22s %-10s %s' % (k, a.dtype, a.shape))

print('ck files:', len(list(CK.glob('*.npz'))))
names = sorted(p.stem for p in CK.glob('*.npz'))
print('ck names not in RUNS:', [n for n in names if n not in L.RUNS])
print('RUNS not in ck:', [n for n in L.RUNS if n not in names])
fam = {}
for f in sorted(L.STORED.glob('*.npz')):
    with np.load(f, allow_pickle=False) as z:
        m = json.loads(str(z['meta']))
    fam.setdefault((m.get('family'), m.get('set')), []).append(f.stem)
for k, v in sorted(fam.items(), key=lambda kv: str(kv[0])):
    print(k, len(v), v[:3], '...')
ben = [s for (fa, st), v in fam.items() if fa == 'benign' for s in v]
print('benign runs:', len(ben), sorted(ben))
print('benign in ck:', sum(b in names for b in ben))
b = sorted(ben)[0]
z = np.load(CK / (b + '.npz'), allow_pickle=False)
print('== ck benign', b)
for k in z.files:
    print('   %-22s %-10s %s' % (k, z[k].dtype, z[k].shape))
z = np.load(L.STORED / (b + '.npz'), allow_pickle=False)
print('meta', str(z['meta'])[:600])
ntot = 0; nev = 0; nph3 = 0
for r in L.RUNS:
    z = np.load(L.STORED / (r + '.npz'), allow_pickle=False); e = np.load(L.EXTRACT / (r + '.npz'), allow_pickle=False)
    ntot += z['evaluated'].size; nev += int(z['evaluated'].sum()); nph3 += int((e['phase'][z['evaluated'].astype(bool)] == 3).sum())
print('stored decisions', ntot, 'evaluated', nev, 'phase 3 among evaluated', nph3)
