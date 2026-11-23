"""Pre-lock §3d test: F's 10 Hz id0 array of old run 0037 (pod) vs CD's accepted B7_10_0.1 test array; A10 B0(b), 1e-12 on common keys."""
import json, pathlib
import numpy as np
W = pathlib.Path(r'ARS_TRIAL\revision_v13\work')
a = np.load(W / 'F_dropout' / 'out_a12' / 'testold_hz10' / 'ID0' / 'p1b_fit_finite_0037.npz', allow_pickle=False)
b = np.load(W / 'CD_capture' / 'analysis' / 'out' / 'testold_b7_arrays_final' / 'B7_10_0.1' / 'p1b_fit_finite_0037.npz', allow_pickle=False)
OWN = {'meta', 'dr_frame', 'dr_masked', 'dr_age', 'dr_gap'}
ka, kb = set(a.files) - OWN, set(b.files) - {'meta'}
common = sorted(ka & kb)
res, ok = {}, True
for k in common:
    x, y = a[k], b[k]
    if x.shape != y.shape:
        res[k] = 'shape %s vs %s' % (x.shape, y.shape); ok = False; continue
    if x.dtype.kind in 'fc' or y.dtype.kind in 'fc':
        xf, yf = x.astype(float), y.astype(float)
        nan_eq = np.array_equal(np.isnan(xf), np.isnan(yf))
        d = float(np.nanmax(np.abs(xf - yf))) if np.isfinite(xf).any() else 0.0
        res[k] = d if nan_eq else 'NaN pattern differs'
        if not nan_eq or d > 1e-12: ok = False
    else:
        eq = np.array_equal(x, y); res[k] = 'equal' if eq else 'DIFFERS'; ok = ok and eq
print(json.dumps(dict(passed=ok, common=len(common), only_F=sorted(ka - kb), only_CD=sorted(kb - ka),
                      worst={k: v for k, v in res.items() if v not in ('equal', 0.0)}), indent=0))
