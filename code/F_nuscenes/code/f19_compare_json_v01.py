"""Package F (revision v13): compares two JSON outputs value by value (platform tests: the same frozen program on the laptop and on
a pod). New file, 20 Nov 2026 (Claude Opus 5.5). Numbers within an absolute tolerance (default 1e-9; NaN = NaN; integers exact),
strings and booleans equal, same structure. Keys whose name is in IGNORE (times, durations, paths, platform) are skipped.
Writes the report to the path given with --out (refuses to overwrite).
Usage: python -I f19_compare_json_v01.py A.json B.json --out REPORT.json [--tol 1e-9] [--ignore k1,k2]
"""
import json, math, pathlib, sys

IGNORE = {'written', 'seconds', 'elapsed', 'elapsed_s', 'runtime_s', 'time', 'lock2', 'platform', 'host', 'python', 'threads'}


def walk(a, b, path, tol, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k in IGNORE:
                continue
            if k not in a or k not in b:
                out['differ'].append(dict(path=path + '/' + k, why='missing in ' + ('first' if k not in a else 'second')))
                continue
            walk(a[k], b[k], path + '/' + k, tol, out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out['differ'].append(dict(path=path, why='length %d vs %d' % (len(a), len(b)))); return
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, '%s[%d]' % (path, i), tol, out)
    elif isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or isinstance(b, str) or a is None or b is None:
        out['n_other'] += 1
        if a != b:
            out['differ'].append(dict(path=path, first=a, second=b))
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
        out['n_numbers'] += 1
        fa, fb = float(a), float(b)
        if math.isnan(fa) and math.isnan(fb):
            return
        if isinstance(a, int) and isinstance(b, int):
            if a != b:
                out['differ'].append(dict(path=path, first=a, second=b))
            return
        d = abs(fa - fb) if not (math.isinf(fa) or math.isinf(fb)) else (0. if fa == fb else math.inf)
        out['max_abs_diff'] = max(out['max_abs_diff'], d)
        if not d <= tol:
            out['differ'].append(dict(path=path, first=a, second=b, abs_diff=d))
    else:
        out['differ'].append(dict(path=path, why='types %s vs %s' % (type(a).__name__, type(b).__name__)))


def main():
    a = sys.argv[1:]
    fa, fb = pathlib.Path(a[0]), pathlib.Path(a[1])
    outp = pathlib.Path(a[a.index('--out') + 1])
    tol = float(a[a.index('--tol') + 1]) if '--tol' in a else 1e-9
    if '--ignore' in a:
        IGNORE.update(x for x in a[a.index('--ignore') + 1].split(',') if x)
    if outp.exists():
        raise SystemExit('REFUSED: %s exists' % outp)
    out = dict(first=str(fa), second=str(fb), tolerance=tol, ignored_keys=sorted(IGNORE), n_numbers=0, n_other=0, max_abs_diff=0.,
               differ=[])
    walk(json.loads(fa.read_text(encoding='utf-8')), json.loads(fb.read_text(encoding='utf-8')), '', tol, out)
    out['agree'] = not out['differ']
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(out, indent=1), encoding='utf-8')
    print('%s vs %s: %d numbers, %d other, max abs diff %.3g, %d differ -> agree %s'
          % (fa.name, fb.name, out['n_numbers'], out['n_other'], out['max_abs_diff'], len(out['differ']), out['agree']))
    for d in out['differ'][:10]:
        print('  ', d)


if __name__ == '__main__':
    main()
