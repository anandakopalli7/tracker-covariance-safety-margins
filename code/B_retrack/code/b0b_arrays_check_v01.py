"""v13 package B, B0(b) (AMENDMENT_10_v13 section 3, row B0 (b)): arrays rebuilt from the REPLAYED actor lists reproduce the stored
ones. New file, 19 Nov 2026 (Claude Opus 5.5). Read-only on P and revision_v12; writes only B_retrack\\out\\b0\\.

Per run: the library's CV0 replay (trk_tracker_v01.retrack_capture: logged detections -> tracker of record -> planner actors;
filter events and algebra from the library's recorder) is served to the extractors of record through trk_arrays_v01.overlay; the
arrays are rebuilt with P-bar of record (openloop\\pbar_tuning_v01.json) and compared with
  gateR_rt_v01\\<run>.npz (critical scales F0, N, E; clearances; selections; basics),
  A4 extract (fit: 11_ojits\\A4\\fit\\extract; lead-braking tuning: 11_ojits\\A4\\dryrun\\extract): NA, CK3, AM (cA1), Q, phase,
  revision_v12\\analysis\\out\\lead (fit only): the lead-track state.
Selections: optA_lib_v02.select_grid(crit, GRID of record, idx55) for F0, N, E, NA, CK3, AM, Q, compared exactly.
Tolerance A10 B0(b): 1e-12 (absolute; NaN = NaN, inf = inf).
Usage: python -I -B -X utf8 b0b_arrays_check_v01.py <part> <nparts>   (runs: 35 fit lead braking + 120 tuning)
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, pathlib, time, csv
LIB = pathlib.Path(r'ARS_TRIAL\revision_v13\work\shared\trackers')
sys.path.insert(0, str(LIB))
import trk_env_v01 as env
env.setup()
import numpy as np
import trk_tracker_v01 as T
import trk_arrays_v01 as A
P = pathlib.Path(r'<library folder>')
sys.path.insert(0, str(P / '11_ojits' / 'A6R' / 'code'))
import optA_lib_v02 as L                     # noqa: E402  (read-only scoring library of record)

STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
A4 = {'fit': P / '11_ojits' / 'A4' / 'fit' / 'extract', 'tune': P / '11_ojits' / 'A4' / 'dryrun' / 'extract'}
LEAD = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis\out\lead')
PBAR = json.loads((P / '09_redesign' / 'm2_decisions' / 'openloop' / 'pbar_tuning_v01.json').read_text(encoding='utf-8'))['Pbar']
GRID = np.concatenate([[0.], np.logspace(-2, 3, 201)])
OUT = pathlib.Path(__file__).resolve().parents[1] / 'out' / 'b0'
TOL = 1e-12
G_KEYS = [('k', 'k'), ('evaluated', 'evaluated'), ('v0', 'v0'), ('des', 'des'), ('clear', 'clear'), ('vbar', 'vbar'), ('idx55', 'idx55'),
          ('cF0', 'cF0'), ('cN', 'cN'), ('cE', 'cE'), ('cl', 'cl'), ('clx', 'clx'), ('status', 'status'), ('prim_idx', 'prim_idx'),
          ('n_act', 'n_act'), ('n_match', 'n_match'), ('prim_track', 'prim_track'), ('prim_age', 'prim_age'), ('prim_miss', 'prim_miss'),
          ('ego_speed', 'ego_speed'), ('flag_task', 'flag_task'), ('flag_strict', 'flag_strict')]
A4_KEYS = [('cNA', 'cNA'), ('cQ', 'cQ'), ('cA1', 'cA1'), ('cCK3', 'cCK3'), ('phase', 'phase'), ('prebrake', 'prebrake'), ('lam_max', 'lam_max'), ('k', 'k')]
LEAD_KEYS = ['lead_found', 'track_id', 'vhat', 'vhat_x', 'ahat_long', 'ahat_mag', 'age', 'v_true', 'nis_last', 'nees_v', 'gap_true',
             'dx_pred0', 'dx_pred1', 'dx_pred2', 'dx_pred3']


def cmp(a, b):
    a = np.asarray(a); b = np.asarray(b)
    if a.shape != b.shape:
        return dict(shape=[list(a.shape), list(b.shape)], ok=False)
    a = a.astype(float); b = b.astype(float)
    same = (a == b) | (np.isnan(a) & np.isnan(b))
    fin = np.isfinite(a) & np.isfinite(b)
    mad = float(np.abs(a[fin] - b[fin]).max()) if fin.any() else 0.
    nonfin_diff = int((~same & ~fin).sum())
    return dict(n=int(a.size), n_diff=int((~same).sum()), max_abs=mad, ok=bool(nonfin_diff == 0 and mad <= TOL))


def runs():
    M4 = P / '09_redesign' / 'm4_perception_model'
    rows = [r for r in csv.DictReader(open(M4 / 'run_index_m4_v02.csv', encoding='utf-8')) if r['use'] == '1'
            and (r['set'] == 'tune' or (r['set'] == 'fit' and r['family'] == 'lead_braking'))]
    rows.sort(key=lambda r: (r['set'], r['archive']))
    return rows


def main():
    part, nparts = int(sys.argv[1]), int(sys.argv[2])
    rr = runs()
    assert len(rr) == 155
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / ('B0B_ARRAYS_part%d_v01.jsonl' % part)
    done = set()
    if out.exists():
        done = {json.loads(l)['run'] for l in open(out, encoding='utf-8') if l.strip()}
    for i, r in enumerate(rr):
        if i % nparts != part or r['archive'] in done:
            continue
        t0 = time.time()
        cap = pathlib.Path(r['cap']); rd = cap.parents[3]
        res = dict(run=r['archive'], set=r['set'], family=r['family'])
        try:
            ov, rec = T.retrack_capture(cap, 'CV0')
            lb = r['family'] == 'lead_braking'
            with A.overlay(cap, ov):
                meta, arr = A.extract(rd, cap, PBAR, lead=(r['set'] == 'fit'), a4=lb)
            z = np.load(STORED / (r['archive'] + '.npz'))
            c = {new: cmp(arr[new], z[old]) for new, old in G_KEYS}
            if lb:
                x = np.load(A4['fit' if r['set'] == 'fit' else 'tune'] / (r['archive'] + '.npz'))
                c.update({'A4.' + new: cmp(arr[new], x[old]) for new, old in A4_KEYS})
            if r['set'] == 'fit':
                l = np.load(LEAD / (r['archive'] + '.npz'))
                c.update({'lead.' + key: cmp(arr[key], l[key]) for key in LEAD_KEYS})
            sel = {}
            crits = [('F0', 'cF0', z['cF0']), ('N', 'cN', z['cN']), ('E', 'cE', z['cE'])]
            if lb:
                crits += [('NA', 'cNA', x['cNA']), ('CK3', 'cCK3', x['cCK3']), ('AM', 'cA1', x['cA1']), ('Q', 'cQ', x['cQ'])]
            for nm, key, stored in crits:
                s1 = L.select_grid(arr[key], GRID, arr['idx55']); s0 = L.select_grid(stored, GRID, z['idx55'])
                sel[nm] = int((s1 != s0).sum())
            res.update(checks=c, selections_differ=sel, all_ok=bool(all(v['ok'] for v in c.values()) and not any(sel.values())),
                       worst=max(v.get('max_abs', 0.) for v in c.values()), seconds=round(time.time() - t0, 1))
        except Exception as e:
            import traceback
            res.update(error=repr(e)[:400], tb=traceback.format_exc()[-1500:], all_ok=False)
        with open(out, 'a', encoding='utf-8') as f:
            f.write(json.dumps(res) + '\n')
        print(r['archive'], res.get('all_ok'), res.get('worst'), res.get('seconds'), res.get('error', ''), flush=True)


if __name__ == '__main__':
    main()
