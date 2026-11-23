"""Revision v13, AMENDMENT_12 sec. 5 (v02): the export of the real-sensor mechanism check for package A, prefix M. New file, 22 Nov 2026
(Claude Opus 5.5, session F). A pure renaming of the two trackers' `values`, applied the same way to both programs' files; it computes
nothing.
  first : F_nuscenes\\out\\mech_val\\MECH_val_{T1,IMM}_v02.json          -> F_nuscenes\\out\\A_EXPORT_M.json
  second: F_nuscenes\\out\\mech_val\\MECH_RECOUNT_val_{T1,IMM}_v02.json  -> F_nuscenes\\out\\A_RECOUNT_M.json
Names: CANMOT (T1, primary) keeps its M.* names (M.tau, M.ci, M.level, M.passes, M.p = the primary over the miss pairs; M.all.* = the
original all-row statistic, descriptive; M.s.<stratum>.*; M.n_rows.*; M.tau_pooled; M.twin_mean; M.n_scenes). The IMM (secondary) gets
the same names under M.IMM. (e.g. M.IMM.tau). M.status = "ran".
Usage: python -I f21_export_m_v01.py first|second   (refuses to overwrite)
"""
import hashlib, json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent
F = HERE.parent
V13 = F.parent.parent
SRC = {'first': ('MECH_val_T1_v02.json', 'MECH_val_IMM_v02.json'),
       'second': ('MECH_RECOUNT_val_T1_v02.json', 'MECH_RECOUNT_val_IMM_v02.json')}
DST = {'first': F / 'out' / 'A_EXPORT_M.json', 'second': F / 'out' / 'A_RECOUNT_M.json'}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    which = sys.argv[1]
    dst = DST[which]
    if dst.exists(): raise SystemExit('REFUSED: %s exists' % dst)
    ft, fi = (F / 'out' / 'mech_val' / n for n in SRC[which])
    vt = json.loads(ft.read_text(encoding='utf-8'))['values']
    vi = json.loads(fi.read_text(encoding='utf-8'))['values']
    out = {'M.status': 'ran'}
    for k, x in vt.items():
        if not k.startswith('M.'): raise SystemExit('REFUSED: key %s' % k)
        out[k] = x
    for k, x in vi.items():
        if not k.startswith('M.'): raise SystemExit('REFUSED: key %s' % k)
        out['M.IMM.' + k[2:]] = x
    lock = V13 / 'LOCK_A12c.txt'
    doc = dict(package='F (real-sensor mechanism check, AMENDMENT_12 sec. 5 v02)', written=time.strftime('%Y-%m-%d %H:%M:%S'),
               programs={ft.name: sha(ft), fi.name: sha(fi)}, renamer='f21_export_m_v01.py', renamer_sha256=sha(__file__),
               lock_sha256=sha(lock) if lock.is_file() else None,
               note='CANMOT (primary) under M.*, the IMM (secondary) under M.IMM.*; M.tau / M.ci / M.passes = the miss-pair primary', values=out)
    dst.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('WROTE', dst, len(out), 'values', sha(dst))


if __name__ == '__main__':
    main()
