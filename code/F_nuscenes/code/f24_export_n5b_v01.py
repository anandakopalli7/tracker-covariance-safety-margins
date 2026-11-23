"""Revision v13, AMENDMENT_12 sec. 5b: the clerical export pair for package A, prefix N5b (coordinator, 05:22). New file, 22 Nov 2026
(Claude Opus 5.5, session F). A pure renaming; it computes nothing.
  first : work\\F_dropout_nus\\out\\FN5B_VALUES_v01.json (values N5b.*, as they are)          -> work\\F_nuscenes\\out\\A_EXPORT_N5B.json
  second: work\\F_dropout_nus\\recount\\FN5B_RECOUNT_masked_v02.json (values DR.*), renamed  -> work\\F_nuscenes\\out\\A_RECOUNT_N5B.json
          by the inverse of f23_compare_nus5b_v01.py's name map: DR.DR0.passes -> N5b.room.passes, DR.DR1.passes -> N5b.E5N.passes,
          DR.DR2.class -> N5b.class, DR.DR2.passes -> N5b.class.passes, DR.n_runs -> N5b.n_scenes; every other DR.X -> N5b.X (the
          second program's descriptive extras keep their own names under N5b.).
N5b.status = "ran" in both. Usage: python -I f24_export_n5b_v01.py first|second   (refuses to overwrite)
"""
import hashlib, json, pathlib, sys, time
V13 = pathlib.Path(__file__).resolve().parents[3]
SRC = {'first': V13 / 'work' / 'F_dropout_nus' / 'out' / 'FN5B_VALUES_v01.json',
       'second': V13 / 'work' / 'F_dropout_nus' / 'recount' / 'FN5B_RECOUNT_masked_v02.json'}
DST = {'first': V13 / 'work' / 'F_nuscenes' / 'out' / 'A_EXPORT_N5B.json', 'second': V13 / 'work' / 'F_nuscenes' / 'out' / 'A_RECOUNT_N5B.json'}
INV = {'DR.DR0.passes': 'N5b.room.passes', 'DR.DR1.passes': 'N5b.E5N.passes', 'DR.DR2.class': 'N5b.class',
       'DR.DR2.passes': 'N5b.class.passes', 'DR.n_runs': 'N5b.n_scenes'}      # inverse of f23_compare_nus5b_v01.MAP


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    which = sys.argv[1]
    src, dst = SRC[which], DST[which]
    if dst.exists(): raise SystemExit('REFUSED: %s exists' % dst)
    v = json.loads(src.read_text(encoding='utf-8'))['values']
    out = {'N5b.status': 'ran'}
    for k, x in v.items():
        if which == 'first':
            if not k.startswith('N5b.'): raise SystemExit('REFUSED: key %s' % k)
            out[k] = x
        else:
            if not k.startswith('DR.'): raise SystemExit('REFUSED: key %s' % k)
            out[INV.get(k, 'N5b.' + k[len('DR.'):])] = x
    lock = V13 / 'LOCK_A12e.txt'
    doc = dict(package='F worker (real-log dropout decision test, AMENDMENT_12 sec. 5b)', written=time.strftime('%Y-%m-%d %H:%M:%S'),
               program=str(src.relative_to(V13)), program_sha256=sha(src), renamer='f24_export_n5b_v01.py', renamer_sha256=sha(__file__),
               lock_sha256=sha(lock) if lock.is_file() else None, note='pure renaming; second program mapped by the inverse of f23 name map',
               values=out)
    dst.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('WROTE', dst, len(out), 'values', sha(dst))


if __name__ == '__main__':
    main()
