r"""v13 round 2 (AMENDMENT_12 s3c; coordinator decision 22 Nov ~02:32 EST, option (a)): launcher for the FIRST Y program copy
(CD_capture\ycheck_imm2\y_twin_l12_v13.py, byte-identical to CD's frozen file) on IMM2's new-run arrays. New file, 22 Nov 2026
(Claude Opus 5.5). The program is not changed. On new runs it accepts only "--intervals calibrated"; with "--calib export" it writes
its calibration job to cd_common_v13.CALIB_DIR, which by default is a folder of session CD's under CD's label (y_l12_main). This
launcher imports cd_common_v13 first and sets CALIB_DIR to CD_capture\ycheck_imm2\out\calib (B's copy folder; asserted), then runs the
copy with runpy under its own path. No calibration job is ever run from that export: Delta's interval is the 95 % percentile one
(delta_main at level 0.95, marked PENDING) and the nominal95 block, the descriptive interval of A12 s3c (departure recorded: s3c's flag
wording "--intervals nominal95" is replaced by the calibrated path's export, the program unchanged).
Checks before running: the copy's SHA-256 equals the SHA recorded for CD's source in FREEZE_B_add10 (external_read_only).
Run with CD's venv (numba):  CD_capture\.venv\Scripts\python.exe -I -B -X utf8 b_imm2_twin_first_v01.py
"""
import hashlib, json, pathlib, runpy, sys

W = pathlib.Path(__file__).resolve().parents[2]
CD = W / 'CD_capture'
B = W / 'B_retrack'
COPY = CD / 'ycheck_imm2' / 'y_twin_l12_v13.py'
SRC = CD / 'ycheck' / 'y_twin_l12_v13.py'
CALIB = CD / 'ycheck_imm2' / 'out' / 'calib'
MAN = B / 'out' / 'retrack_new' / 'IMM2_MANIFEST_v01.json'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    fz = {str(W / e['path']): e['sha256'] for e in json.loads((W / 'locks' / 'FREEZE_B_add10.json').read_text(encoding='utf-8'))['external_read_only']}
    if sha(COPY) != fz[str(SRC)]:
        raise SystemExit('REFUSED: the copy differs from the frozen source SHA')
    sys.path.insert(0, str(CD / 'analysis'))
    import cd_common_v13 as CC
    CC.CALIB_DIR = CALIB
    assert CC.CALIB_DIR.resolve().is_relative_to((CD / 'ycheck_imm2').resolve()), 'CALIB_DIR must stay in B\'s copy folder'
    sys.argv = [str(COPY), '--intervals', 'calibrated', '--calib', 'export', '--cases-sha', sha(CD / 'l12' / 'CASES_L12_v13.json'),
                '--b2-dir', str(B / 'out' / 'retrack_new' / 'IMM2'), '--b2-manifest', str(MAN), '--b2-manifest-sha', sha(MAN)]
    print('launcher: CALIB_DIR =', CC.CALIB_DIR, '| argv =', ' '.join(sys.argv[1:]), flush=True)
    runpy.run_path(str(COPY), run_name='__main__')
    assert CC.CALIB_DIR == CALIB, 'CALIB_DIR changed during the run'


if __name__ == '__main__':
    main()
