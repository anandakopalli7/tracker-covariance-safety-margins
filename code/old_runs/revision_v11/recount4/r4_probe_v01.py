"""Recount4 probe (read-only): what recount2\\out\\<run>.npz holds and basic checks on it. Opens nothing of revision_v11\\analysis."""
import pathlib, sys
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'recount'))
import rc_lib_v01 as L   # noqa: E402

R2 = HERE.parent / 'recount2' / 'out'
KEYS = ['t0p50_a6p0', 't0p75_a6p0', 't1p00_a6p0', 't1p25_a6p0', 't1p50_a6p0', 't1p80_a6p0', 't0p75_a4p0', 't0p75_a5p0', 't0p75_a7p6']

z = np.load(R2 / (L.RUNS[0] + '.npz'), allow_pickle=False)
for k in z.files:
    print(k, z[k].shape, z[k].dtype)
ds = L.load_all()
print('runs', len(ds), 'evaluated', sum(d['n'] for d in ds), 'stored', sum(d['n_stored'] for d in ds))
print('phase counts', {p: int(sum((d['phase'] == p).sum() for d in ds)) for p in range(4)})
print('nan clear eval', sum(d['n_nan_clear_eval'] for d in ds))
tot = {k: dict(nanX=0, nan61=0, late=0, cens=0, cens_notlate=0, x_gt_61=0, safe61_unsafe3=0, unsafe61_safe3=0, cens_unsafe61_safeX=0,
               notlate_diff=0, pairs=0) for k in KEYS}
for d in ds:
    with np.load(R2 / (d['run'] + '.npz'), allow_pickle=False) as z:
        assert np.array_equal(z['k'], d['k_all']) and np.array_equal(z['evaluated'].astype(bool), d['ev_all'])
        ev = d['ev_all']
        for k in KEYS:
            cx = np.asarray(z['clearX_' + k], float)[ev]; c6 = np.asarray(z['clear61_' + k], float)[ev]
            la = np.asarray(z['late_' + k])[ev].astype(bool); ce = np.asarray(z['cens_' + k])[ev].astype(bool)
            t = tot[k]
            t['pairs'] += cx.size
            t['nanX'] += int(np.isnan(cx).sum()); t['nan61'] += int(np.isnan(c6).sum())
            t['late'] += int(la.sum()); t['cens'] += int(ce.sum()); t['cens_notlate'] += int((ce & ~la).sum())
            t['x_gt_61'] += int((cx > c6).sum())
            t['notlate_diff'] += int(((cx != c6) & ~la).sum())
            t['cens_unsafe61_safeX'] += int((ce & ~(c6 > 0) & (cx > 0)).sum())
            if k == 't0p75_a6p0':
                t['safe61_unsafe3'] += int(((c6 > 0) & ~(d['clear'] > 0)).sum()); t['unsafe61_safe3'] += int((~(c6 > 0) & (d['clear'] > 0)).sum())
                t.setdefault('cache_flag_differs', 0)
                t['cache_flag_differs'] += int(((c6 > 0) != (d['rs'] > 0)).sum())
for k in KEYS:
    print(k, tot[k])
