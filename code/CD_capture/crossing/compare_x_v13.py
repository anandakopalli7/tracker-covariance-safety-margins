"""Crossing sprint (A11): first vs second program, key by key (A10 sec. 10.1(c)). New file, 21 Nov 2026 (Claude Opus 5.5, session CD).
Compares the flat 'values' of crossing/out/[TESTOLD_]X_CROSS_<family>_v13.json (first) and recount/out/[TESTOLD_]RC_X_CROSS_<family>_v13.json
(second): integers, booleans, strings and levels exact; numbers and interval ends within 1e-9; null only against null.
Usage: python -I -B compare_x_v13.py [--test-old] [--second-dir DIR] [--second-suffix S]  -> crossing/out/[TESTOLD_]COMPARE_X_v13[_<i>].json (never overwritten)
"""
import json, math, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
TEST = '--test-old' in sys.argv; PFX = 'TESTOLD_' if TEST else ''
SEC = pathlib.Path(sys.argv[sys.argv.index('--second-dir') + 1]) if '--second-dir' in sys.argv else CD / 'recount' / 'out'
TOL = 1e-9
SFX = sys.argv[sys.argv.index('--second-suffix') + 1] if '--second-suffix' in sys.argv else ''   # e.g. _b2000 (old-run test)


def same(a, b, key):
    if a is None or b is None: return a is None and b is None
    if isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or isinstance(b, str): return a == b
    if isinstance(a, int) and isinstance(b, int): return a == b
    if key.endswith('.level'): return float(a) == float(b)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        a, b = float(a), float(b)
        if math.isnan(a) or math.isnan(b): return math.isnan(a) and math.isnan(b)
        return abs(a - b) <= TOL
    if isinstance(a, list) and isinstance(b, list): return len(a) == len(b) and all(same(x, y, key) for x, y in zip(a, b))
    return a == b


def main():
    rows = []; summary = {}
    for fam in ('pedestrian_crossing',):                                  # A11 sec. 3: pedestrian crossing only
        fa = HERE / 'out' / f'{PFX}X_CROSS_{fam}_v13.json'; fb = SEC / f'{PFX}RC_X_CROSS_{fam}_v13{SFX}.json'
        if not (fa.is_file() and fb.is_file()): summary[fam] = 'missing file(s): %s' % [str(f) for f in (fa, fb) if not f.is_file()]; continue
        A = json.loads(fa.read_text(encoding='utf-8'))['values']; B = json.loads(fb.read_text(encoding='utf-8'))['values']
        st = dict(agree=0, disagree=0, only_first=0, only_second=0)
        for k in sorted(set(A) | set(B)):
            if k in A and k in B:
                ok = same(A[k], B[k], k); st['agree' if ok else 'disagree'] += 1
                if not ok: rows.append(dict(family=fam, key=k, status='DISAGREE', first=A[k], second=B[k]))
            else:
                w = 'only_first' if k in A else 'only_second'; st[w] += 1; rows.append(dict(family=fam, key=k, status=w, value=A.get(k, B.get(k))))
        summary[fam] = st
    ok = all(isinstance(s, dict) and not s['disagree'] and not s['only_first'] and not s['only_second'] for s in summary.values())
    out = HERE / 'out' / f'{PFX}COMPARE_X_v13.json'; i = 1
    while out.exists(): i += 1; out = HERE / 'out' / f'{PFX}COMPARE_X_v13_{i}.json'
    out.write_text(json.dumps(dict(schema='COMPARE_X_V13', test_old=TEST, tolerance=TOL, verdict='AGREE' if ok else 'DISAGREE OR MISSING',
                                   summary=summary, rows=rows), indent=1, default=str), encoding='utf-8')
    print(json.dumps(dict(out=out.name, verdict='AGREE' if ok else 'DISAGREE OR MISSING', summary=summary)))
    for r in rows: print('  ', r['family'], r['status'], r['key'], str(r.get('first', r.get('value')))[:60], str(r.get('second', ''))[:60])


if __name__ == '__main__':
    main()
