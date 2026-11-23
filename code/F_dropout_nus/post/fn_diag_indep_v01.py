"""AMENDMENT_12 sec. 5b: diagnosis of the stop "tracker-independent keys of <scene> differ from F's arrays" (fn06 prep, 22 Nov
03:49 EST). NEW helper (Claude Opus 5.5, worker of package F), read only; it reads ONLY the tracker-independent keys that fn06's check
reads (no critical scale, no outcome) and reports, per scene and key, what differs. Usage: python -I -B fn_diag_indep_v01.py ROOT
(ROOT = .../revision_v13/work)."""
import json, pathlib, sys
import numpy as np
W = pathlib.Path(sys.argv[1])
EX = ('sweep', 'kf', 'now', 'age', 'idx55', 'evaluated', 'evaluated2', 'inpath', 'n_truth')
FL = ('vbar', 'v0', 'des', 'clear', 'clear2')
rep = {}
for f in sorted((W / 'F_nuscenes' / 'cache' / 'arrays_T1' / 'val').glob('scene-*.npz')):
    m = W / 'F_dropout_nus' / 'cache' / 'arrays_masked' / 'val' / f.name
    a = np.load(f, allow_pickle=False); b = np.load(m, allow_pickle=False)
    bad = {}
    for k in EX:
        if a[k].shape != b[k].shape or not np.array_equal(a[k], b[k], equal_nan=(a[k].dtype.kind == 'f')):
            bad[k] = dict(shape=[list(a[k].shape), list(b[k].shape)])
    for k in FL:
        x = np.asarray(a[k], float); y = np.asarray(b[k], float)
        if x.shape != y.shape:
            bad[k] = dict(shape=[list(x.shape), list(y.shape)]); continue
        nan_d = int((np.isnan(x) != np.isnan(y)).sum())
        inf_d = int((np.isinf(x) != np.isinf(y)).sum()) + int((np.isinf(x) & np.isinf(y) & (np.sign(x) != np.sign(y))).sum())
        fin = np.isfinite(x) & np.isfinite(y)
        mx = float(np.abs(x[fin] - y[fin]).max()) if fin.any() else 0.
        if nan_d or inf_d or mx > 1e-9:
            e = dict(nan_pattern_differ=nan_d, inf_pattern_differ=inf_d, finite_max_abs=mx)
            where = np.argwhere((np.isinf(x) != np.isinf(y)) | (fin & (np.abs(np.where(fin, x - y, 0.)) > 1e-9)))[:5]
            e['examples'] = [dict(index=[int(i) for i in w], F=float(x[tuple(w)]), masked=float(y[tuple(w)])) for w in where]
            bad[k] = e
    if bad:
        rep[f.stem] = bad
print(json.dumps(dict(n_scenes_differing=len(rep), scenes=rep), indent=1, default=float)[:6000])
