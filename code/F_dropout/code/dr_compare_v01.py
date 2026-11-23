"""Revision v13, AMENDMENT_11 sec. 6c.10: compares the first program's DR values with the second program's (A10 sec. 10.1(c): counts
exact, points and interval ends within 1e-9 on the same draws, calibrated levels equal; verdicts and classes equal). New file, 21 Nov
2026 (Claude Opus 5.5, session F). Compares the `values` dicts key by key (DR's own names); integers and booleans and strings exact;
floats within the tolerance (NaN = NaN, None = None); lists element by element. Keys present in only one file are listed and make the
comparison fail unless they are named in --allow-missing.
Usage: python -I dr_compare_v01.py FIRST.json SECOND.json --out REPORT.json [--tol 1e-9] [--allow-missing k1,k2]
"""
import json, math, pathlib, sys, time


def eq(a, b, tol, path, out):
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(dict(key=path, why='length %d vs %d' % (len(a), len(b)))); return
        for i, (x, y) in enumerate(zip(a, b)):
            eq(x, y, tol, '%s[%d]' % (path, i), out)
        return
    if a is None or b is None or isinstance(a, (bool, str)) or isinstance(b, (bool, str)):
        if a != b: out.append(dict(key=path, first=a, second=b))
        return
    if isinstance(a, int) and isinstance(b, int):
        if a != b: out.append(dict(key=path, first=a, second=b, why='count differs'))
        return
    fa, fb = float(a), float(b)
    if math.isnan(fa) and math.isnan(fb): return
    d = abs(fa - fb) if not (math.isinf(fa) or math.isinf(fb)) else (0. if fa == fb else math.inf)
    out.append(dict(key=path, abs_diff=d, ok=d <= tol)) if d > 0 else None


def main():
    a = sys.argv[1:]
    fa, fb = pathlib.Path(a[0]), pathlib.Path(a[1])
    outp = pathlib.Path(a[a.index('--out') + 1]); tol = float(a[a.index('--tol') + 1]) if '--tol' in a else 1e-9
    allow = set(a[a.index('--allow-missing') + 1].split(',')) if '--allow-missing' in a else set()
    if outp.exists(): raise SystemExit('REFUSED: %s exists' % outp)
    va = json.loads(fa.read_text(encoding='utf-8'))['values']; vb = json.loads(fb.read_text(encoding='utf-8'))['values']
    only_a = sorted(set(va) - set(vb)); only_b = sorted(set(vb) - set(va))
    diffs = []
    for k in sorted(set(va) & set(vb)):
        eq(va[k], vb[k], tol, k, diffs)
    bad = [d for d in diffs if not d.get('ok', False)]
    maxd = max([d['abs_diff'] for d in diffs if 'abs_diff' in d] + [0.])
    agree = not bad and not [k for k in only_a + only_b if k not in allow]
    doc = dict(code='dr_compare_v01.py', rule='A10 sec. 10.1(c): counts exact, values within %g, levels and verdicts equal' % tol,
               first=str(fa), second=str(fb), n_keys_compared=len(set(va) & set(vb)), only_first=only_a, only_second=only_b,
               allowed_missing=sorted(allow), max_abs_diff=maxd, n_float_diffs_within_tol=sum(1 for d in diffs if d.get('ok')),
               differ=bad, agree=agree, written=time.strftime('%Y-%m-%d %H:%M:%S'))
    outp.write_text(json.dumps(doc, indent=1, default=str), encoding='utf-8')
    print('%d keys compared; only first %s; only second %s; max abs diff %.3g; %d differ -> agree %s'
          % (doc['n_keys_compared'], only_a, only_b, maxd, len(bad), agree))
    for d in bad[:15]: print('  ', d)


if __name__ == '__main__':
    main()
