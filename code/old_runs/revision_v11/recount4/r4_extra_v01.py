"""Recount4 supplementary checks, written after the comparison (not part of the results file):
  1. the "as scored" flag: the pack cache clearance (the first program's source) against recount2's own clear61, all 9 settings;
  2. the two readings of "censored pairs unsafe" (every censored pair unsafe / only censored pairs that are safe on the 3 s
     window): pairs on which they differ;
  3. how far the estimate moves the first safe row and the perfect oracle's selection against the 3 s window, per setting.
Reads the stored inputs and recount2\\out only. Usage: python -B -X utf8 r4_extra_v01.py -> r4_extra_v01_out.json"""
import json, pathlib, sys
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import r4_items_v01 as I   # noqa: E402
L = I.L

ds = I.load()
out = {}
for key in I.SETTINGS:
    c = dict(pairs=0, cache_flag_differs_from_clear61=0, cache_value_differs_from_clear61_by_more_than_1e9=0, nan_cache=0,
             cens_readings_differ=0, cens_not_late=0, clearX_above_clear61=0, not_late_but_clearX_differs=0,
             decisions_first_safe_row_moves=0, decisions_with_a_pair_changing=0, decisions_with_a_cens_pair_safe_under_est=0,
             runs_with_a_cens_pair=0)
    for d in ds:
        with np.load(L.CACHE / (d['run'] + '_pack.npz'), allow_pickle=False) as z:
            ca = np.asarray(z[key], float)[d['ev_all']]
        x = d['X'][key]; w = d['W'][key]; la = d['late'][key]; ce = d['cens'][key]
        c['pairs'] += int(x.size); c['nan_cache'] += int(np.isnan(ca).sum())
        c['cache_flag_differs_from_clear61'] += int(((ca > 0.) != (w > 0.)).sum())
        with np.errstate(invalid='ignore'):
            c['cache_value_differs_from_clear61_by_more_than_1e9'] += int((~(np.abs(ca - w) <= 1e-9)).sum())
        r1 = ~(x > 0.) | ce                      # every censored pair unsafe (the brief)
        r2 = ~(x > 0.) | (ce & (w > 0.))         # only censored pairs safe on the 3 s window (recount2's optional scoring)
        c['cens_readings_differ'] += int((r1 != r2).sum())
        c['cens_not_late'] += int((ce & ~la).sum()); c['clearX_above_clear61'] += int((x > w).sum())
        c['not_late_but_clearX_differs'] += int((~la & (x != w)).sum())
        sx = x > 0.; sw = w > 0.
        fx = np.where(sx.any(1), sx.argmax(1), -1); fw = np.where(sw.any(1), sw.argmax(1), -1)
        c['decisions_first_safe_row_moves'] += int((fx != fw).sum())
        c['decisions_with_a_pair_changing'] += int((sx != sw).any(1).sum())
        c['decisions_with_a_cens_pair_safe_under_est'] += int((ce & sx).any(1).sum())
        c['runs_with_a_cens_pair'] += int(ce.any())
    out[key] = c
    print(key, c)
(HERE / 'r4_extra_v01_out.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
