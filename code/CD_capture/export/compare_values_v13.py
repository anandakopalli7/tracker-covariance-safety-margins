"""Compare two family outputs ("values" dicts under A's key names) key by key, A10 sec. 10.1(c): ints and strings exact; numbers and
interval ends within 1e-9; null only against null. New file, 20 Nov 2026 (Claude Opus 5.5).
Usage: python -I compare_values_v13.py FIRST.json SECOND.json OUT.json [--ignore-prefix P,...]
Writes OUT.json (never overwritten) with every disagreement and every key present on one side only.
"""
import json, math, pathlib, sys


def same(a, b, tol=1e-9):
    if a is None or b is None: return a is None and b is None
    if isinstance(a, bool) or isinstance(b, bool): return a == b
    if isinstance(a, int) and isinstance(b, int): return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        a, b = float(a), float(b)
        if math.isnan(a) or math.isnan(b): return math.isnan(a) and math.isnan(b)
        if math.isinf(a) or math.isinf(b): return a == b
        return abs(a - b) <= tol
    if isinstance(a, list) and isinstance(b, list): return len(a) == len(b) and all(same(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict): return a.keys() == b.keys() and all(same(a[k], b[k], tol) for k in a)
    return a == b


def main():
    fa, fb, fo = (pathlib.Path(x) for x in sys.argv[1:4])
    ign = tuple(sys.argv[sys.argv.index('--ignore-prefix') + 1].split(',')) if '--ignore-prefix' in sys.argv else ()
    if fo.exists(): raise SystemExit('REFUSED: %s exists' % fo)
    A = json.loads(fa.read_text(encoding='utf-8'))['values']; B = json.loads(fb.read_text(encoding='utf-8'))['values']
    rows = []; st = dict(agree=0, disagree=0, only_first=0, only_second=0, ignored=0)
    for k in sorted(set(A) | set(B)):
        if ign and k.startswith(ign): st['ignored'] += 1; continue
        if k in A and k in B:
            if same(A[k], B[k]): st['agree'] += 1
            else: st['disagree'] += 1; rows.append(dict(key=k, status='DISAGREE', first=A[k], second=B[k]))
        else:
            w = 'only_first' if k in A else 'only_second'; st[w] += 1; rows.append(dict(key=k, status=w, value=A.get(k, B.get(k))))
    doc = dict(first=str(fa), second=str(fb), tolerance=1e-9, summary=st, verdict='AGREE' if not st['disagree'] else 'DISAGREE', rows=rows)
    fo.write_text(json.dumps(doc, indent=1, default=str), encoding='utf-8')
    print(json.dumps(dict(out=str(fo), summary=st, verdict=doc['verdict'])))
    for r in rows[:40]:
        print(' ', r['status'], r['key'], '|', str(r.get('first', r.get('value')))[:70], '|', str(r.get('second', ''))[:70])


if __name__ == '__main__':
    main()
