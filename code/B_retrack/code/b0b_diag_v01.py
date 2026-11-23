"""v13 package B, B0(b) diagnosis of the 4 runs outside 1e-12 absolute (19 Nov 2026, 20:40 EST): relative differences of the rebuilt
critical scales against the stored ones, the magnitude of the scales where they differ, and whether those decisions' replayed actor
lists were bit-identical to the logged ones. Writes out\b0\B0B_DIAG_v01.json. Usage: python -I -B -X utf8 b0b_diag_v01.py"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import b0b_arrays_check_v01 as B
import numpy as np
T = B.T; A = B.A; env = B.env
RUNS = ['p2_c1109_tune_0002_fixed_c1', 'p2_c1109_tune_0056_fixed_c1', 'p2_c1109_tune_0110_fixed_c1', 'p2_c1109_tune_0033_fixed_c1']
out = {}
rows = {r['archive']: r for r in B.runs()}
for run in RUNS:
    r = rows[run]; cap = pathlib.Path(r['cap']); rd = cap.parents[3]
    ov, rec = T.retrack_capture(cap, 'CV0')
    with A.overlay(cap, ov):
        meta, arr = A.extract(rd, cap, B.PBAR, lead=False, a4=False)
    z = np.load(B.STORED / (run + '.npz'))
    logged = [f for f in env.jl(cap / 'frames.jsonl') if (f.get('execution') or {}).get('new_decision') is not None]
    mine = [f for f in ov['frames.jsonl'] if (f.get('execution') or {}).get('new_decision') is not None]
    k_act_diff = {f['k'] for f, g in zip(logged, mine) if f['execution']['new_decision']['actors'] != g['execution']['new_decision']['actors']}
    res = {}
    for key in ('cF0', 'cN', 'cE'):
        a = arr[key].astype(float); b = z[key].astype(float)
        fin = np.isfinite(a) & np.isfinite(b) & (a != b)
        rel = np.abs(a[fin] - b[fin]) / np.abs(b[fin]) if fin.any() else np.zeros(0)
        rows_k = arr['k'][np.nonzero(fin)[0]] if fin.any() else np.zeros(0, int)
        res[key] = dict(n_diff=int(fin.sum()), max_abs=float(np.abs(a[fin] - b[fin]).max()) if fin.any() else 0., max_rel=float(rel.max()) if rel.size else 0.,
                        scale_at_max_abs=float(np.abs(b[fin])[np.argmax(np.abs(a[fin] - b[fin]))]) if fin.any() else None,
                        decisions_with_diff=int(np.unique(rows_k).size),
                        decisions_with_diff_and_actor_list_differs=int(sum(1 for k in np.unique(rows_k) if int(k) in k_act_diff)))
    out[run] = dict(family=r['family'], decisions_actor_list_differs=len(k_act_diff), crit=res)
    print(run, json.dumps(out[run]), flush=True)
(pathlib.Path(__file__).resolve().parents[1] / 'out' / 'b0' / 'B0B_DIAG_v01.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
