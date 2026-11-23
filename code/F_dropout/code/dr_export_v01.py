"""Revision v13, AMENDMENT_11 sec. 6c (DR): the export for package A (work\\A_text\\notes\\RESULTS_INTERFACE_SPRINT_v13.md, "X and DR",
prefix DR.). New file, 21 Nov 2026 (Claude Opus 5.5, session F). A pure renaming of the `values` of a DR results file, applied the
same way to the first program's file and to the second program's file; it computes nothing.
  first : F_dropout\\out\\DR_RESULTS_v01.json        -> F_nuscenes\\out\\A_EXPORT_DR.json
  second: F_dropout\\recount\\DR_RECOUNT_v01.json    -> F_nuscenes\\out\\A_RECOUNT_DR.json
A's names <- DR's names (both programs write DR's names; sec. 6c.6-6c.7):
  DR.R, .R.ci, .R.pos_share, .R.dec          <- DR.R_gl, DR.R_gl.ci, DR.R_gl.share_pos, DR.R_deceq
  DR.RR_E5N, .RR_E5N.ci                       <- DR.c, DR.c.ci        (the amplitude-matched ranking oracle's share)
  DR.RR_E5NmP, .RR_E5NmP.ci                   <- DR.cdiff, DR.cdiff.ci
  DR.RR_N, .RR_N.ci, .RR_N.dec, .RR_N.dec.ci  <- DR.r, DR.r.ci, DR.D_N_deceq, DR.D_N_deceq.ci
  DR.within5, DR.eff, DR.eff.ci, DR.masked_share, DR.n_runs, DR.n_dec <- the same names
  every other DR.* key is passed through under its own name (levels, verdicts, descriptive populations, P-bar_DR, identity).
DR.PO25/50/75 are not part of DR's pre-registration (sec. 6c) and are not written (A: pending / not printed).
DR.status = "ran" (both programs agree is checked separately, out\\DR_COMPARE_v01.json; "missed" is the coordinator's).
Usage: python -I dr_export_v01.py first|second   (refuses to overwrite)
"""
import hashlib, json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent
DRD = HERE.parent
WORK = DRD.parent
V13 = WORK.parent
SRC = {'first': DRD / 'out' / 'DR_RESULTS_v01.json', 'second': DRD / 'recount' / 'DR_RECOUNT_v01.json'}
DST = {'first': WORK / 'F_nuscenes' / 'out' / 'A_EXPORT_DR.json', 'second': WORK / 'F_nuscenes' / 'out' / 'A_RECOUNT_DR.json'}  # coordinator, 21 Nov
REN = {'DR.R_gl': 'DR.R', 'DR.R_gl.ci': 'DR.R.ci', 'DR.R_gl.share_pos': 'DR.R.pos_share', 'DR.R_deceq': 'DR.R.dec',
       'DR.R_deceq.ci': 'DR.R.dec.ci', 'DR.R_gl.level': 'DR.R.level',
       'DR.c': 'DR.RR_E5N', 'DR.c.ci': 'DR.RR_E5N.ci', 'DR.c.level': 'DR.RR_E5N.level',
       'DR.cdiff': 'DR.RR_E5NmP', 'DR.cdiff.ci': 'DR.RR_E5NmP.ci', 'DR.cdiff.level': 'DR.RR_E5NmP.level',
       'DR.r': 'DR.RR_N', 'DR.r.ci': 'DR.RR_N.ci', 'DR.r.level': 'DR.RR_N.level',
       'DR.D_N_deceq': 'DR.RR_N.dec', 'DR.D_N_deceq.ci': 'DR.RR_N.dec.ci'}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    which = sys.argv[1]
    src, dst = SRC[which], DST[which]
    if dst.exists(): raise SystemExit('REFUSED: %s exists' % dst)
    d = json.loads(src.read_text(encoding='utf-8'))
    v = d['values']
    out = {'DR.status': 'ran'}
    for k, x in v.items():
        out[REN.get(k, k)] = x
    lock = V13 / 'LOCK_A11c.txt'
    doc = dict(package='F (DR, AMENDMENT_11 sec. 6c)', written=time.strftime('%Y-%m-%d %H:%M:%S'), program=str(src.name),
               program_sha256=sha(src), renamer='dr_export_v01.py', renamer_sha256=sha(__file__),
               lock2_sha256=sha(lock) if lock.is_file() else None,
               note='values renamed to RESULTS_INTERFACE_SPRINT_v13 "X and DR" names; DR.PO25/50/75 are not part of DR (not written)',
               values=out)
    dst.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('WROTE', dst, len(out), 'values', sha(dst))


if __name__ == '__main__':
    main()
