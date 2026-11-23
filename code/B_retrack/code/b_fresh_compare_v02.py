"""v13 package B: first program (A_EXPORT_B.json, out\\fresh\\boot_<x>.npz) against the independent second program (A_RECOUNT_B.json,
recount_fresh\\out\\boot_<x>.npz) on the fresh runs (B_FRESH_DEFINITIONS_v02.md section 7). New file, 20 Nov 2026 (Claude Opus 5.5).
Rules: key sets equal; integers and strings and booleans equal; numbers within 1e-9 * max(1, |value|) (NaN equals NaN); intervals
element-wise, compared where both programs have them; per-resample values (denE, n, D_N, D_E5x, D_CK3) row by row on the rows both have.
Writes out\\compare\\B_FRESH_COMPARE_v02.json and .md (--test-old: the TESTOLD files, out\\compare\\B_FRESH_COMPARE_TESTOLD_v02.*).
Usage: python -I -B -X utf8 b_fresh_compare_v02.py [--test-old]
"""
import sys, json, math, pathlib, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parents[1]
OUT = HERE / 'out'
RC = HERE / 'recount_fresh' / 'out'
VARS = ['CV0', 'B3', 'B4', 'B1', 'B2', 'B1_d090', 'B1_d098']
NAME = {'CV0': 'CV', 'B3': 'CV2', 'B4': 'CA', 'B1': 'IMM', 'B2': 'AQ', 'B1_d090': 'IMM090', 'B1_d098': 'IMM098'}
TOL = 1e-9


def same(a, b):
    if isinstance(a, dict) or isinstance(b, dict):
        return isinstance(a, dict) and isinstance(b, dict) and set(a) == set(b) and all(same(a[k], b[k]) for k in a)
    if isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or isinstance(b, str):
        return a == b
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, list) or isinstance(b, list):
        return isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    a = float(a); b = float(b)
    if math.isnan(a) or math.isnan(b):
        return math.isnan(a) and math.isnan(b)
    return abs(a - b) <= TOL * max(1., abs(a), abs(b))


def main():
    test = '--test-old' in sys.argv
    fa = (OUT / 'fresh_testold' / 'TESTOLD_A_EXPORT_B.json') if test else (OUT / 'A_EXPORT_B.json')
    fb = (RC / 'TESTOLD_A_RECOUNT_B.json') if test else (OUT / 'A_RECOUNT_B.json')
    A = json.loads(fa.read_text(encoding='utf-8')); B = json.loads(fb.read_text(encoding='utf-8'))
    prov = sorted(k for k in set(A) | set(B) if k.endswith('lock_sha256'))     # provenance (lock-file hashes), not values
    A = {k: v for k, v in A.items() if k not in prov}; B = {k: v for k, v in B.items() if k not in prov}
    only_a = sorted(set(A) - set(B)); only_b = sorted(set(B) - set(A))
    ci_only_a = [k for k in only_a if k.endswith('.ci')]
    rows = []
    for k in sorted(set(A) & set(B)):
        rows.append(dict(key=k, first=A[k], second=B[k], agree=same(A[k], B[k])))
    boots = []
    for v in VARS:
        pa = OUT / ('fresh_testold' if test else 'fresh') / ('boot_%s.npz' % v)
        pb = RC / (('testold_boot_%s.npz' if test else 'boot_%s.npz') % NAME[v])     # the second program names files by key name
        if not (pa.exists() and pb.exists()):
            boots.append(dict(variant=v, missing=[str(p) for p in (pa, pb) if not p.exists()])); continue
        a = np.load(pa); b = np.load(pb); ent = dict(variant=v)
        for k in ('denE', 'n', 'D_N', 'D_E5x', 'D_CK3'):
            m = min(a[k].size, b[k].size); x = a[k][:m]; y = b[k][:m]
            both_nan = np.isnan(x) & np.isnan(y)
            err = np.where(both_nan, 0., np.abs(x - y) / np.maximum(1., np.maximum(np.abs(x), np.abs(y))))
            ent[k] = dict(rows=int(m), rows_first=int(a[k].size), rows_second=int(b[k].size),
                          max_rel=float(np.nanmax(err)) if m else None, agree=bool(m and np.all(np.isfinite(err) & (err <= TOL))))
        ent['agree'] = all(ent[k]['agree'] for k in ('denE', 'n', 'D_N', 'D_E5x', 'D_CK3'))
        boots.append(ent)
    extra = [('B6', OUT / ('fresh_testold/boot_b6_testold.npz' if test else 'fresh_b6/boot_b6.npz'),
              RC / ('testold_boot_b6.npz' if test else 'boot_b6.npz'), ('WR', 'W1', 'DS')),
             ('TU', OUT / 'tu' / 'boot_tu.npz', RC / 'boot_tu.npz', ('denE', 'n', 'D_N', 'D_NA', 'D_AM', 'D_CK3'))]
    for v, pa, pb, keys in extra:
        if not (pa.exists() and pb.exists()):
            boots.append(dict(variant=v, missing=[str(p) for p in (pa, pb) if not p.exists()])); continue
        a = np.load(pa); b = np.load(pb); ent = dict(variant=v)
        for k in keys:
            m = min(a[k].size, b[k].size); x = a[k][:m]; y = b[k][:m]
            both_nan = np.isnan(x) & np.isnan(y)
            err = np.where(both_nan, 0., np.abs(x - y) / np.maximum(1., np.maximum(np.abs(x), np.abs(y))))
            ent[k] = dict(rows=int(m), rows_first=int(a[k].size), rows_second=int(b[k].size),
                          max_rel=float(np.nanmax(err)) if m else None, agree=bool(m and np.all(np.isfinite(err) & (err <= TOL))))
        ent['agree'] = all(ent[k]['agree'] for k in keys)
        boots.append(ent)
    n_ag = sum(r['agree'] for r in rows)
    doc = dict(code='b_fresh_compare_v02.py', test_old=test, first=str(fa.relative_to(HERE)), second=str(fb.relative_to(HERE)),
               keys_compared=len(rows), keys_agree=n_ag, keys_disagree=[r for r in rows if not r['agree']],
               keys_only_first=only_a, keys_only_second=only_b,
               note_ci_only_first='interval keys the second program did not compute (it then checks the per-resample rows)' if ci_only_a else None,
               per_resample=boots, all_agree=bool(n_ag == len(rows) and not only_b and set(only_a) <= set(ci_only_a)
                                                    and all(x.get('agree') for x in boots)),
               written=time.strftime('%Y-%m-%d %H:%M:%S'))
    od = OUT / 'compare'; od.mkdir(parents=True, exist_ok=True)
    stem = 'B_FRESH_COMPARE_TESTOLD_v02' if test else 'B_FRESH_COMPARE_v02'
    (od / (stem + '.json')).write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    L = ['# Package B fresh-run values: first vs second program%s — %s' % (' (TEST on old runs)' if test else '', doc['written']), '',
         'Keys compared: %d; agree: %d; disagree: %d; only in first: %d (of which interval keys: %d); only in second: %d.' % (
             len(rows), n_ag, len(rows) - n_ag, len(only_a), len(ci_only_a), len(only_b)), '',
         '| Variant | rows compared (first / second) | denE | n | D_N | D_E5x | D_CK3 |', '|---|---|---|---|---|---|---|']
    for x in boots:
        if 'missing' in x:
            L.append('| %s | missing | | | | | |' % x['variant']); continue
        if x['variant'] in ('B6', 'TU'):
            ks = [k for k in x if k not in ('variant', 'agree')]
            L.append('| %s | %d (%d / %d) | %s |  |  |  |  |' % (x['variant'], x[ks[0]]['rows'], x[ks[0]]['rows_first'], x[ks[0]]['rows_second'],
                     '; '.join('%s %s' % (k, 'agree' if x[k]['agree'] else 'DIFFER %.2g' % x[k]['max_rel']) for k in ks)))
            continue
        L.append('| %s | %d (%d / %d) | %s | %s | %s | %s | %s |' % (x['variant'], x['denE']['rows'], x['denE']['rows_first'], x['denE']['rows_second'],
                 *[('agree' if x[k]['agree'] else 'DIFFER %.2g' % x[k]['max_rel']) for k in ('denE', 'n', 'D_N', 'D_E5x', 'D_CK3')]))
    L += ['', '**All agree: %s**' % doc['all_agree']]
    for r in doc['keys_disagree']:
        L.append('- %s: first %r, second %r' % (r['key'], r['first'], r['second']))
    (od / (stem + '.md')).write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('\n'.join(L), flush=True)


if __name__ == '__main__':
    main()
