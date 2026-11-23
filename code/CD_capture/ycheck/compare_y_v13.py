"""Y (A11 sec. 6b): first vs second program, key by key (A10 sec. 10.1(c)), with crossing\\compare_x_v13.py's rule (frozen in
FREEZE_CD_add3, imported unchanged): integers, booleans, strings and levels exact; numbers and interval ends within 1e-9; null only
against null. New file, 21 Nov 2026 (Claude Opus 5.5, session CD).
Usage: python -I -B compare_y_v13.py FIRST.json SECOND.json OUTNAME   -> ycheck/out/OUTNAME (never overwritten)
"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'crossing'))
_argv = sys.argv; sys.argv = sys.argv[:1]
import compare_x_v13 as C               # noqa: E402
sys.argv = _argv


def main():
    fa, fb, name = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
    out = HERE / 'out' / name
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    A = json.loads(fa.read_text(encoding='utf-8'))['values']; B = json.loads(fb.read_text(encoding='utf-8'))['values']
    rows = []; st = dict(agree=0, disagree=0, only_first=0, only_second=0)
    for k in sorted(set(A) | set(B)):
        if k in A and k in B:
            ok = C.same(A[k], B[k], k); st['agree' if ok else 'disagree'] += 1
            if not ok: rows.append(dict(key=k, status='DISAGREE', first=A[k], second=B[k]))
        else:
            w = 'only_first' if k in A else 'only_second'; st[w] += 1; rows.append(dict(key=k, status=w, value=A.get(k, B.get(k))))
    verdict = 'AGREE' if not st['disagree'] else 'DISAGREE'
    out.write_text(json.dumps(dict(schema='COMPARE_Y_V13', first=str(fa), second=str(fb), tolerance=C.TOL, verdict=verdict, summary=st, rows=rows),
                              indent=1, default=str), encoding='utf-8')
    print(json.dumps(dict(out=out.name, verdict=verdict, summary=st)))
    for r in rows: print('  ', r['status'], r['key'], str(r.get('first', r.get('value')))[:60], str(r.get('second', ''))[:60])


if __name__ == '__main__':
    main()
