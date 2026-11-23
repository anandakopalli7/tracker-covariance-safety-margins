"""Revision v13, AMENDMENT_12 sec. 5b: session F's independent check of the masked val arrays' tracker-independent keys against F's
val arrays of record (22 Nov 2026, about 03:55 EST, Claude Opus 5.5, session F), after fn06_score_v01's gate stopped the run.
Exact keys compared on all decisions; float keys (vbar, v0, des, clear, clear2) within 1e-9 and equal NaN patterns, split by
whether the decision is evaluated. Reads arrays only; computes no scored value. Writes out\\nus5b\\CHECK_INDEP_F_v01.json."""
import pathlib
import numpy as np
W = pathlib.Path(r'ARS_TRIAL\revision_v13\work')
A = W / 'F_dropout_nus' / 'cache' / 'arrays_masked' / 'val'
B = W / 'F_nuscenes' / 'cache' / 'arrays_T1' / 'val'
EXACT = ['sweep', 'kf', 'now', 'age', 'idx55', 'evaluated', 'evaluated2', 'inpath', 'n_truth']
FLOAT = ['vbar', 'v0', 'des', 'clear', 'clear2']
bad_exact, bad_float_eval, bad_float_noneval = [], [], []
files = sorted(A.glob('scene-*.npz'))
for f in files:
    a = np.load(f, allow_pickle=False); b = np.load(B / f.name, allow_pickle=False)
    for k in EXACT:
        if k in a.files and k in b.files and not np.array_equal(a[k], b[k]):
            bad_exact.append((f.stem, k))
    ev = b['evaluated'].astype(bool) if 'evaluated' in b.files else None
    for k in FLOAT:
        if k not in a.files or k not in b.files: continue
        x, y = a[k].astype(float), b[k].astype(float)
        if x.shape != y.shape:
            bad_exact.append((f.stem, k + ' shape')); continue
        nanne = np.isnan(x) != np.isnan(y)
        with np.errstate(invalid='ignore'):
            d = np.abs(x - y); d[np.isnan(d)] = 0.
        off = (d > 1e-9) | nanne
        if off.any():
            rows = np.unique(np.nonzero(off)[0])           # first axis = decision
            for r in rows:
                (bad_float_eval if (ev is not None and r < ev.size and ev[r]) else bad_float_noneval).append((f.stem, k, int(r), float(d[r].max())))
import json
out = dict(scenes=len(files), exact_key_differences=bad_exact, float_differences_evaluated=bad_float_eval,
           float_differences_not_evaluated=bad_float_noneval)
o = pathlib.Path(__file__).resolve().parent.parent / 'out' / 'nus5b' / 'CHECK_INDEP_F_v01.json'
if o.exists(): raise SystemExit('REFUSED: exists')
o.write_text(json.dumps(out, indent=1), encoding='utf-8')
print('scenes', len(files))
print('exact-key differences:', bad_exact)
print('float differences at EVALUATED decisions:', bad_float_eval)
print('float differences at non-evaluated decisions:', bad_float_noneval)
