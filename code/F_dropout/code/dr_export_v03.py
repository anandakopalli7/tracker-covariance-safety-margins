"""Revision v13, AMENDMENT_12 sec. 3d (DR at 10 Hz on the new runs): the export for package A, prefix DR10 (sec. 3d.8). New file,
22 Nov 2026 (Claude Opus 5.5, session F): a copy of dr_export_v02.py with only the sources, destinations, lock and prefix changed.
A pure renaming of `values`, applied the same way to both programs' files; it computes nothing.
  first : F_dropout\\out_a12\\hz10\\DR10_RESULTS_v01.json -> F_nuscenes\\out\\A_EXPORT_DR10.json
  second: F_dropout\\recount\\DR10_RECOUNT_v01.json       -> F_nuscenes\\out\\A_RECOUNT_DR10.json
Names: dr_export_v01's renames (R, RR_E5N, RR_E5NmP, RR_N, ...), then the prefix DR. -> DR10.; every other key keeps its name under DR10.
DR10.status = "ran" (agreement is checked separately, out_a12\\DR10_COMPARE_v01.json).
Usage: python -I dr_export_v03.py first|second   (refuses to overwrite)
"""
import hashlib, json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent
DRD = HERE.parent
WORK = DRD.parent
V13 = WORK.parent
SRC = {'first': DRD / 'out_a12' / 'hz10' / 'DR10_RESULTS_v01.json', 'second': DRD / 'recount' / 'DR10_RECOUNT_v01.json'}
DST = {'first': WORK / 'F_nuscenes' / 'out' / 'A_EXPORT_DR10.json', 'second': WORK / 'F_nuscenes' / 'out' / 'A_RECOUNT_DR10.json'}
REN = {'DR.R_gl': 'DR.R', 'DR.R_gl.ci': 'DR.R.ci', 'DR.R_gl.share_pos': 'DR.R.pos_share', 'DR.R_deceq': 'DR.R.dec',
       'DR.R_deceq.ci': 'DR.R.dec.ci', 'DR.R_gl.level': 'DR.R.level',
       'DR.c': 'DR.RR_E5N', 'DR.c.ci': 'DR.RR_E5N.ci', 'DR.c.level': 'DR.RR_E5N.level',
       'DR.cdiff': 'DR.RR_E5NmP', 'DR.cdiff.ci': 'DR.RR_E5NmP.ci', 'DR.cdiff.level': 'DR.RR_E5NmP.level',
       'DR.r': 'DR.RR_N', 'DR.r.ci': 'DR.RR_N.ci', 'DR.r.level': 'DR.RR_N.level',
       'DR.D_N_deceq': 'DR.RR_N.dec', 'DR.D_N_deceq.ci': 'DR.RR_N.dec.ci'}         # = dr_export_v01.REN


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    which = sys.argv[1]
    src, dst = SRC[which], DST[which]
    if dst.exists(): raise SystemExit('REFUSED: %s exists' % dst)
    v = json.loads(src.read_text(encoding='utf-8'))['values']
    out = {'DR10.status': 'ran'}
    for k, x in v.items():
        k2 = REN.get(k, k)
        if not k2.startswith('DR.'): raise SystemExit('REFUSED: key without the DR. prefix: %s' % k)
        out['DR10.' + k2[len('DR.'):]] = x
    lock = V13 / 'LOCK_A12d.txt'
    doc = dict(package='F (DR at 10 Hz on the new runs, AMENDMENT_12 sec. 3d)', written=time.strftime('%Y-%m-%d %H:%M:%S'),
               program=str(src.name), program_sha256=sha(src), renamer='dr_export_v03.py', renamer_sha256=sha(__file__),
               lock_sha256=sha(lock) if lock.is_file() else None, note='values renamed as dr_export_v01 (A names), prefix DR10', values=out)
    dst.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('WROTE', dst, len(out), 'values', sha(dst))


if __name__ == '__main__':
    main()
