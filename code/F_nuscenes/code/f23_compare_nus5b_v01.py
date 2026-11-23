"""Revision v13, AMENDMENT_12 sec. 5b: the side-by-side of the two programs' masked val values (A10 sec. 10.1(c)). New file, 22 Nov 2026
(Claude Opus 5.5, session F). Computes nothing: it renames the first program's keys (N5b.*, out\\FN5B_VALUES_v01.json) to the second
program's names (DR.*, recount\\FN5B_RECOUNT_masked_v02.json) and compares them with dr_compare_v01's rule (counts exact, values within
1e-9, levels / verdicts / classes equal). Name map: N5b.room.passes -> DR.DR0.passes, N5b.E5N.passes -> DR.DR1.passes, N5b.class ->
DR.DR2.class, N5b.class.passes -> DR.DR2.passes, N5b.n_scenes -> DR.n_runs; every other N5b.X -> DR.X. Keys written by one program only
are listed (descriptive extras). Output out\\nus5b\\NUS5B_COMPARE_v01.json (refuses to overwrite).
Usage: python -I f23_compare_nus5b_v01.py
"""
import hashlib, json, math, pathlib, time
V13 = pathlib.Path(__file__).resolve().parents[3]
FIRST = V13 / 'work' / 'F_dropout_nus' / 'out' / 'FN5B_VALUES_v01.json'
SECOND = V13 / 'work' / 'F_dropout_nus' / 'recount' / 'FN5B_RECOUNT_masked_v02.json'
OUT = V13 / 'work' / 'F_nuscenes' / 'out' / 'nus5b' / 'NUS5B_COMPARE_v01.json'
MAP = {'N5b.room.passes': 'DR.DR0.passes', 'N5b.E5N.passes': 'DR.DR1.passes', 'N5b.class': 'DR.DR2.class',
       'N5b.class.passes': 'DR.DR2.passes', 'N5b.n_scenes': 'DR.n_runs'}
TOL = 1e-9


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def eq(a, b, path, out, diffs):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b: out.append(dict(key=path + '.' + k, why='only in one')); continue
            eq(a[k], b[k], path + '.' + k, out, diffs)
        return
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): out.append(dict(key=path, why='length')); return
        for i, (x, y) in enumerate(zip(a, b)): eq(x, y, '%s[%d]' % (path, i), out, diffs)
        return
    if a is None or b is None or isinstance(a, (bool, str)) or isinstance(b, (bool, str)):
        if a != b: out.append(dict(key=path, first=a, second=b))
        return
    if isinstance(a, int) and isinstance(b, int):
        if a != b: out.append(dict(key=path, first=a, second=b, why='count'))
        return
    fa, fb = float(a), float(b)
    if math.isnan(fa) and math.isnan(fb): return
    d = abs(fa - fb)
    diffs.append(d)
    if not (d <= TOL): out.append(dict(key=path, first=fa, second=fb, diff=d))


def main():
    if OUT.exists(): raise SystemExit('REFUSED: %s exists' % OUT)
    v1 = json.loads(FIRST.read_text(encoding='utf-8'))['values']
    v2 = json.loads(SECOND.read_text(encoding='utf-8'))['values']
    mapped = {MAP.get(k, 'DR.' + k[len('N5b.'):]): (k, x) for k, x in v1.items()}
    common = sorted(k for k in mapped if k in v2)
    bad, diffs = [], []
    for k in common:
        x1 = mapped[k][1]; x2 = v2[k]
        if isinstance(x1, (int, float)) and not isinstance(x1, bool) and isinstance(x2, (int, float)) and not isinstance(x2, bool):
            if isinstance(x1, int) != isinstance(x2, int) and float(x1) == float(x2):   # 18987 vs 18987.0: a count written as float
                continue
        eq(x1, x2, k, bad, diffs)
    only_first = sorted(mapped[k][0] for k in mapped if k not in v2)
    only_second = sorted(k for k in v2 if k not in mapped)
    doc = dict(code='f23_compare_nus5b_v01.py', rule='A10 sec. 10.1(c): counts exact, values within 1e-9, levels and verdicts equal',
               first=str(FIRST.relative_to(V13)), first_sha256=sha(FIRST), second=str(SECOND.relative_to(V13)), second_sha256=sha(SECOND),
               name_map=MAP, n_keys_compared=len(common), max_abs_diff=max(diffs) if diffs else 0.0, differ=bad,
               only_first=only_first, only_second=only_second, agree=not bad, written=time.strftime('%Y-%m-%d %H:%M:%S'))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1, default=str), encoding='utf-8')
    print('%d keys compared; max abs diff %.3g; %d differ -> agree %s' % (len(common), doc['max_abs_diff'], len(bad), doc['agree']))
    print('only first:', only_first); print('only second:', only_second)
    for x in bad[:20]: print('  ', x)
    print('WROTE', OUT, sha(OUT))


if __name__ == '__main__':
    main()
