"""Compare the first and second programs' exports for A, key by key (A10 sec. 10.1(c)): integers and strings exact; numbers and
interval ends within 1e-9; levels exact; .cal labels exact; null only against null. New file, 20 Nov 2026 (Claude Opus 5.5).

Usage: python -I compare_exports_v13.py [--test-old]  -> out/[TESTOLD_]COMPARE_EXPORTS_v13.json (never overwritten; a numbered name
is used if it exists). Reads out/[TESTOLD_]A_EXPORT_{C,D}.json and out/[TESTOLD_]A_RECOUNT_{C,D}.json.
A key in only one export is listed (not a disagreement by itself); required keys missing in either are listed separately.
"""
import json, math, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
TEST = '--test-old' in sys.argv; PFX = 'TESTOLD_' if TEST else ''
TOL = 1e-9
KEYS = json.loads((HERE / 'A_KEYS_CD_v13.json').read_text(encoding='utf-8'))['keys']


def same(a, b):
    if a is None or b is None: return a is None and b is None
    if isinstance(a, bool) or isinstance(b, bool): return a == b
    if isinstance(a, int) and isinstance(b, int): return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        a, b = float(a), float(b)
        if math.isnan(a) or math.isnan(b): return math.isnan(a) and math.isnan(b)
        return abs(a - b) <= TOL
    if isinstance(a, list) and isinstance(b, list): return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def main():
    rows = []; summary = {}
    for pk in ('C', 'D'):
        fa = CD / 'out' / f'{PFX}A_EXPORT_{pk}.json'; fb = CD / 'out' / f'{PFX}A_RECOUNT_{pk}.json'
        if not (fa.is_file() and fb.is_file()):
            summary[pk] = 'missing export file(s)'; continue
        A = json.loads(fa.read_text(encoding='utf-8'))['values']; B = json.loads(fb.read_text(encoding='utf-8'))['values']
        req = {k['key'] for k in KEYS[pk] if k['required']}
        st = dict(agree=0, disagree=0, only_first=0, only_second=0)
        for k in sorted(set(A) | set(B)):
            if k in A and k in B:
                ok = same(A[k], B[k]); st['agree' if ok else 'disagree'] += 1
                if not ok: rows.append(dict(package=pk, key=k, status='DISAGREE', first=A[k], second=B[k], required=k in req))
            else:
                w = 'only_first' if k in A else 'only_second'; st[w] += 1
                rows.append(dict(package=pk, key=k, status=w, value=A.get(k, B.get(k)), required=k in req))
        st['required_missing_first'] = sorted(k for k in req if k not in A)
        st['required_missing_second'] = sorted(k for k in req if k not in B)
        summary[pk] = st
    out = CD / 'out' / f'{PFX}COMPARE_EXPORTS_v13.json'; i = 1
    while out.exists(): i += 1; out = CD / 'out' / f'{PFX}COMPARE_EXPORTS_v13_{i}.json'
    verdict = 'AGREE' if all(isinstance(s, dict) and not s['disagree'] for s in summary.values()) else 'DISAGREE OR MISSING'
    out.write_text(json.dumps(dict(schema='COMPARE_EXPORTS_V13', test_old=TEST, tolerance=TOL, verdict=verdict, summary=summary, rows=rows),
                              indent=1, default=str), encoding='utf-8')
    print(json.dumps(dict(out=str(out), verdict=verdict, summary={k: ({kk: (len(vv) if isinstance(vv, list) else vv) for kk, vv in v.items()}
                                                                      if isinstance(v, dict) else v) for k, v in summary.items()})))
    for r in rows:
        if r['status'] == 'DISAGREE': print('  DISAGREE', r['package'], r['key'], '| first', str(r['first'])[:70], '| second', str(r['second'])[:70])


if __name__ == '__main__':
    main()
