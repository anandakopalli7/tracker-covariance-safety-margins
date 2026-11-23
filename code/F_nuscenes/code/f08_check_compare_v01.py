"""Package F (revision v13): comparison of the adapter (first program) with the independent second program on the 20
design-split decisions (A10 section 10.1(b)). New file, 19 Nov 2026 (Claude Opus 5.5).
For each decision of notes\\ADAPTER_CHECK_DECISIONS_v01.json the first program's adapter (f03) gives v_raw, a_raw, v0, desired,
s_e, l_e, the number of truth actors, the 17 rows' targets and the 3 s truth clearance of every row; these are compared with
check2\\ADAPTER_CHECK2_v01.json (Claude Sonnet 5.5): clearances within 1e-6 m (all rows; +inf patterns equal), targets equal,
counts equal, kinematics within 1e-9. The selected row of A10's wording (F0's selection at g = 1) is one of the 17 rows; it is
named in a later addendum once F0's critical scales exist. Writes out\\F_ADAPTER_CHECK_v01.json.
Usage: python -I f08_check_compare_v01.py
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json                                  # noqa: E402
import numpy as np                           # noqa: E402
import f03_adapter_v01 as AD                 # noqa: E402
import f05_arrays_v01 as F5                  # noqa: E402

OUTF = FC.OUT / 'F_ADAPTER_CHECK_v01.json'
TOL = 1e-6


def num(x):
    return np.inf if x in ('inf', 'Infinity') else (-np.inf if x in ('-inf', '-Infinity') else float(x))


def main():
    FC.require_split('train')
    consumer, finite_primitive = F5.planner_mods()
    sel = json.loads((FC.F / 'notes' / 'ADAPTER_CHECK_DECISIONS_v01.json').read_text(encoding='utf-8'))['decisions']
    two = json.loads((FC.F / 'check2' / 'ADAPTER_CHECK2_v01.json').read_text(encoding='utf-8'))
    recs2 = two['records'] if isinstance(two, dict) and 'records' in two else (two['decisions'] if isinstance(two, dict) else two)
    by = {(r['scene'], int(r.get('sweep_timestamp_us', 0))): r for r in recs2}
    out = []; worst = 0.; ok_all = True
    for d in sel:
        z = np.load(FC.CACHE / 'train' / (d['scene'] + '.npz'), allow_pickle=False)
        sc = AD.Scene(z)
        j = d['sweep_index']; now = float(sc.sw_t[j])
        v_raw = float(sc.v[j]); a_raw = float(sc.a[j]); v0 = max(0., v_raw)
        s_e, l_e, th_e = (x[0] for x in sc.project(sc.ego_c[j:j + 1]))
        rows = finite_primitive.build_library(v0, a_raw, sc.desired, [], AD.EGO_L, AD.EGO_W, now, consumer.Diagnostics())
        ids, tc, ty, hl, hw = F5.truth_planner(sc, now, s_e, 61)
        cl = AD.clearance_rows(np.stack([r['s'] for r in rows]), tc, ty, hl, hw, 61)
        r2 = by.get((d['scene'], d['sweep_timestamp_us']))
        rec = dict(scene=d['scene'], sweep_index=j, first=dict(v_raw=v_raw, a_raw=a_raw, v0=v0, desired=sc.desired, s_e=s_e, l_e=l_e,
                                                             n_truth=int(ids.size), targets=[list(r['targets']) for r in rows],
                                                             clearance_3s=[float(x) for x in cl]))
        if r2 is None:
            rec['second'] = None; rec['agree'] = False; ok_all = False
            out.append(rec); continue
        c2 = np.array([num(x) for x in r2['clearance_3s']])
        same_inf = bool(np.array_equal(np.isinf(c2), np.isinf(cl)))
        fin = np.isfinite(c2) & np.isfinite(cl)
        dmax = float(np.abs(c2[fin] - cl[fin]).max()) if fin.any() else 0.
        tg2 = np.array([list(map(float, t)) for t in r2['targets']]); tg1 = np.array(rec['first']['targets'], float)
        tdiff = float(np.abs(tg2 - tg1).max()) if tg2.shape == tg1.shape else np.inf
        kin = max(abs(float(r2['v_raw']) - v_raw), abs(float(r2['a_raw']) - a_raw), abs(float(r2['desired']) - sc.desired))
        agree = bool(same_inf and dmax <= TOL and tdiff <= 1e-9 and int(r2['n_truth_actors']) == int(ids.size))
        rec.update(second=dict(v_raw=r2['v_raw'], a_raw=r2['a_raw'], desired=r2['desired'], n_truth=r2['n_truth_actors']),
                   clearance_max_abs_diff=dmax, inf_pattern_equal=same_inf, targets_max_abs_diff=tdiff, targets_equal=bool(tdiff <= 1e-9),
                   kinematics_max_abs_diff=kin, s_e_diff=abs(float(r2.get('s_e', np.nan)) - s_e), agree=agree)
        worst = max(worst, dmax); ok_all &= agree
        out.append(rec)
    doc = dict(code='f08_check_compare_v01.py', rule='A10 10.1(b): truth clearance within 1e-6 m', tolerance_m=TOL,
               second_program=str(FC.F / 'check2' / 'ADAPTER_CHECK2_v01.json'), second_model='Claude Sonnet 5.5 (check2\\README_CHECK2.md)',
               all_agree=bool(ok_all), worst_clearance_diff_m=worst, decisions=out, written=FC.clock())
    OUTF.write_text(FC.jdump(doc), encoding='utf-8')
    print('all agree:', ok_all, 'worst clearance diff', worst)
    for r in out:
        print(r['scene'], r.get('agree'), r.get('clearance_max_abs_diff'), r.get('kinematics_max_abs_diff'), r.get('targets_equal'),
              r['first']['n_truth'], (r.get('second') or {}).get('n_truth'))


if __name__ == '__main__':
    main()
