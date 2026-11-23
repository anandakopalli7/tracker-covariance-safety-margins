"""Revision v13, AMENDMENT_13 sec. 3 (N_DR against a fixed dropout-flag margin): the export pair for package A, prefix DRF. New file,
22 Nov 2026 (Claude Opus 5.5, session F). Both programs write the DRF.* names of sec. 3.8 directly, so this is a pure copy of `values`
(no renaming); it computes nothing.
  first : F_dropout\\out_a13\\DRF_RESULTS_v01.json        -> F_nuscenes\\out\\A_EXPORT_DRF.json
  second: F_dropout\\recount\\DRF_RECOUNT_v01.json        -> F_nuscenes\\out\\A_RECOUNT_DRF.json
Usage: python -I dr_export_v04.py first|second   (refuses to overwrite; refuses a key without the DRF. prefix)
"""
import hashlib, json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent
DRD = HERE.parent
WORK = DRD.parent
V13 = WORK.parent
SRC = {'first': DRD / 'out_a13' / 'DRF_RESULTS_v01.json', 'second': DRD / 'recount' / 'DRF_RECOUNT_v01.json'}
DST = {'first': WORK / 'F_nuscenes' / 'out' / 'A_EXPORT_DRF.json', 'second': WORK / 'F_nuscenes' / 'out' / 'A_RECOUNT_DRF.json'}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    which = sys.argv[1]
    src, dst = SRC[which], DST[which]
    if dst.exists(): raise SystemExit('REFUSED: %s exists' % dst)
    v = json.loads(src.read_text(encoding='utf-8'))['values']
    bad = [k for k in v if not k.startswith('DRF.')]
    if bad: raise SystemExit('REFUSED: keys without the DRF. prefix: %s' % bad)
    lock = V13 / 'LOCK_A13b.txt'
    doc = dict(package='F (N_DR against a fixed dropout-flag margin, AMENDMENT_13 sec. 3)', written=time.strftime('%Y-%m-%d %H:%M:%S'),
               program=str(src.name), program_sha256=sha(src), renamer='dr_export_v04.py', renamer_sha256=sha(__file__),
               lock_sha256=sha(lock) if lock.is_file() else None, note='values copied unchanged (DRF.* names of sec. 3.8)', values=dict(v))
    dst.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('WROTE', dst, len(v), 'values', sha(dst))


if __name__ == '__main__':
    main()
