r"""v13 sprint (AMENDMENT_11 s6): per-resample check for IMMr (B1r), the one variant the frozen comparator b_fresh_compare_v02.py does
not list in its per-resample loop (its key comparison covers the B.IMMr.* keys). New file, 21 Nov 2026 (Claude Opus 5.5); additive,
no frozen file changed. Same rule as b_fresh_compare_v02.py: arrays denE, n, D_N, D_E5x, D_CK3 of out\fresh\boot_B1R.npz (first program)
against recount_fresh\out\boot_IMMr.npz (second program), relative difference <= 1e-9 with max(1, |a|, |b|) scaling, NaN = NaN.
Writes out\compare\B_IMMR_ROWS_v01.json and prints a one-line verdict.
Usage: python -I -B -X utf8 b_immr_rows_check_v01.py
"""
import json, pathlib, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parents[1]
OUT = HERE / 'out'
PA = OUT / 'fresh' / 'boot_B1R.npz'
PB = HERE / 'recount_fresh' / 'out' / 'boot_IMMr.npz'
KEYS = ('denE', 'n', 'D_N', 'D_E5x', 'D_CK3')
TOL = 1e-9


def main():
    a = np.load(PA); b = np.load(PB); ent = {}
    for k in KEYS:
        m = min(a[k].size, b[k].size); x = a[k][:m].astype(float); y = b[k][:m].astype(float)
        both_nan = np.isnan(x) & np.isnan(y)
        err = np.where(both_nan, 0., np.abs(x - y) / np.maximum(1., np.maximum(np.abs(x), np.abs(y))))
        ent[k] = dict(rows=int(m), rows_first=int(a[k].size), rows_second=int(b[k].size),
                      max_rel=float(np.nanmax(err)) if m else None, agree=bool(m and np.all(np.isfinite(err) & (err <= TOL))))
    doc = dict(code='b_immr_rows_check_v01.py', first=str(PA.relative_to(HERE)), second=str(PB.relative_to(HERE)), tol=TOL,
               arrays=ent, all_agree=all(e['agree'] for e in ent.values()), written=time.strftime('%Y-%m-%d %H:%M:%S'))
    od = OUT / 'compare'; od.mkdir(parents=True, exist_ok=True)
    (od / 'B_IMMR_ROWS_v01.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('IMMr per-resample rows: %s; %s' % ('ALL AGREE' if doc['all_agree'] else 'DIFFER',
          '; '.join('%s %d/%d max_rel %.2g' % (k, e['rows'], e['rows_first'], e['max_rel']) for k, e in ent.items())))


if __name__ == '__main__':
    main()
