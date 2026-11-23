"""Package F (revision v13): the second-program adapter check of the clearance under the departure of 19 Nov 2026
(notes\\F_DEPARTURE_CLEARANCE_v01.md; A10 section 10.1(b): truth clearance within 1e-6 m on 20 design-split decisions). New file,
20 Nov 2026 (Claude Opus 5.5); f08_check_compare_v01.py with the new rule.
For each decision of notes\\ADAPTER_CHECK_DECISIONS_v01.json, the first program's 3 s clearance of every row under the new rule
(f03 clearance_rows(drop_behind=True), computed here, and the stored cache\\clear_v02 value where the decision is evaluated) is
compared with check2\\ADAPTER_CHECK2_v02.json (`clearance_3s`, the second program, Claude Sonnet 5.5): within 1e-6 m, +inf patterns
equal. The second program's `clearance_3s_v01` is compared with the clearance of record (drop_behind=False) in the same way.
Writes out\\F_ADAPTER_CHECK_v02.json (refuses to overwrite).
Usage: python -I f08_check_compare_v02.py
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json                                  # noqa: E402
import numpy as np                           # noqa: E402
import f03_adapter_v01 as AD                 # noqa: E402
import f05_arrays_v01 as F5                  # noqa: E402

OUTF = FC.OUT / 'F_ADAPTER_CHECK_v02.json'
TOL = 1e-6


def num(x):
    return np.inf if x in ('inf', 'Infinity') else (-np.inf if x in ('-inf', '-Infinity') else float(x))


def cmp(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    same_inf = bool(np.array_equal(np.isinf(a), np.isinf(b)) and np.array_equal(np.isnan(a), np.isnan(b)))
    fin = np.isfinite(a) & np.isfinite(b)
    d = float(np.abs(a[fin] - b[fin]).max()) if fin.any() else 0.
    return d, same_inf


def main():
    if OUTF.exists():
        raise SystemExit('REFUSED: %s exists' % OUTF)
    FC.require_split('train')
    consumer, finite_primitive = F5.planner_mods()
    sel = json.loads((FC.F / 'notes' / 'ADAPTER_CHECK_DECISIONS_v01.json').read_text(encoding='utf-8'))['decisions']
    two = json.loads((FC.F / 'check2' / 'ADAPTER_CHECK2_v02.json').read_text(encoding='utf-8'))
    recs2 = two['records'] if isinstance(two, dict) and 'records' in two else (two['decisions'] if isinstance(two, dict) else two)
    by = {(r['scene'], int(r.get('sweep_timestamp_us', 0))): r for r in recs2}
    out = []; worst = 0.; worst_v01 = 0.; worst_cache = 0.; ok_all = True
    for d in sel:
        sc = AD.Scene(np.load(FC.CACHE / 'train' / (d['scene'] + '.npz'), allow_pickle=False))
        j = d['sweep_index']; now = float(sc.sw_t[j])
        v_raw = float(sc.v[j]); a_raw = float(sc.a[j]); v0 = max(0., v_raw)
        s_e = sc.project(sc.ego_c[j:j + 1])[0][0]
        rows = finite_primitive.build_library(v0, a_raw, sc.desired, [], AD.EGO_L, AD.EGO_W, now, consumer.Diagnostics())
        S = np.stack([r['s'] for r in rows])
        ids, tc, ty, hl, hw = F5.truth_planner(sc, now, s_e, 61)
        new = AD.clearance_rows(S, tc, ty, hl, hw, 61, drop_behind=True)
        old = AD.clearance_rows(S, tc, ty, hl, hw, 61)
        rec = dict(scene=d['scene'], sweep_index=j, first_v02=[float(x) for x in new], first_v01=[float(x) for x in old])
        cz = np.load(FC.CACHE / 'clear_v02' / 'train' / (d['scene'] + '.npz'), allow_pickle=False)
        k = np.nonzero(cz['sweep'] == j)[0]
        if k.size and not np.isnan(cz['clear'][k[0]]).all():
            dc, ic = cmp(cz['clear'][k[0]], new)
            rec.update(cache_v02_max_abs_diff=dc, cache_v02_inf_pattern_equal=ic)
            worst_cache = max(worst_cache, dc); ok_all &= bool(ic and dc == 0.)
        else:
            rec.update(cache_v02_max_abs_diff=None, cache_v02_inf_pattern_equal=None, cache_note='decision not evaluated at 3 s')
        r2 = by.get((d['scene'], d['sweep_timestamp_us']))
        if r2 is None:
            rec['second'] = None; rec['agree'] = False; ok_all = False
            out.append(rec); continue
        c2 = np.array([num(x) for x in r2['clearance_3s']]); c2o = np.array([num(x) for x in r2['clearance_3s_v01']])
        dmax, same_inf = cmp(c2, new); dold, same_old = cmp(c2o, old)
        agree = bool(same_inf and dmax <= TOL and same_old and dold <= TOL)
        rec.update(second_v02=[float(x) for x in c2], clearance_max_abs_diff=dmax, inf_pattern_equal=same_inf,
                   v01_max_abs_diff=dold, v01_inf_pattern_equal=same_old,
                   rows_changed_first=int(np.sum(~((new == old) | (np.isnan(new) & np.isnan(old))))),
                   rows_unsafe_to_safe_first=int(np.sum((old <= 0) & (new > 0))),
                   n_pairs_dropped_second=r2.get('n_pairs_dropped'), agree=agree)
        worst = max(worst, dmax); worst_v01 = max(worst_v01, dold); ok_all &= agree
        out.append(rec)
    doc = dict(code='f08_check_compare_v02.py', rule='A10 10.1(b) under notes\\F_DEPARTURE_CLEARANCE_v01.md: truth clearance within 1e-6 m',
               rule_sha256=FC.sha256_file(FC.F / 'notes' / 'F_DEPARTURE_CLEARANCE_v01.md'), tolerance_m=TOL,
               second_program=str(FC.F / 'check2' / 'ADAPTER_CHECK2_v02.json'),
               second_program_sha256=FC.sha256_file(FC.F / 'check2' / 'ADAPTER_CHECK2_v02.json'),
               second_model='Claude Sonnet 5.5 (check2\\README_CHECK2.md, section v02)', all_agree=bool(ok_all),
               worst_clearance_diff_m=worst, worst_v01_diff_m=worst_v01, worst_cache_diff_m=worst_cache, decisions=out,
               written=FC.clock())
    OUTF.write_text(FC.jdump(doc), encoding='utf-8')
    print('all agree:', ok_all, '| worst v02 diff', worst, '| worst v01 diff', worst_v01, '| worst cache diff', worst_cache)
    for r in out:
        print(r['scene'], r.get('agree'), r.get('clearance_max_abs_diff'), r.get('rows_changed_first'), r.get('rows_unsafe_to_safe_first'),
              r.get('cache_v02_max_abs_diff'))


if __name__ == '__main__':
    main()
