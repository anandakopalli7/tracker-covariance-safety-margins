r"""v13 round 2 (AMENDMENT_12 s3c): IMM2's permuted twin (descriptive) with session CD's frozen Y programs for the new runs, unchanged
(coordinator, 22 Nov 00:18 EST). New file, 22 Nov 2026 (Claude Opus 5.5). Tooling only: nothing is computed here.
  prepare   copy, byte for byte, CD_capture\ycheck\y_twin_l12_v13.py to CD_capture\ycheck_imm2\ and CD_capture\recount\
            {rc_y_twin_l12_v13, rc_core_v13, rc_kern_v13, rc_y_kern_v13}.py to CD_capture\recount_imm2\ (outputs then go to those
            folders' out\, never to CD's; CD = HERE.parent and the library paths stay the same). Each copy must have the SHA-256 recorded
            for its source in work\locks\FREEZE_B_add10.json (external_read_only), else REFUSED.
  first     run the first program copy: --intervals nominal95 --cases-sha <sha of CD_capture\l12\CASES_L12_v13.json>
            --b2-dir B_retrack\out\retrack_new\IMM2 --b2-manifest B_retrack\out\retrack_new\IMM2_MANIFEST_v01.json --b2-manifest-sha <its sha>
  second    run the second program copy (CD's Sonnet recount) with the same inputs (--intervals nominal95, --workers 2).
Both refuse by themselves unless revision_v13\LOCK_A12a.txt exists (their gate). Python: CD's venv (numba), BelowNormal (the programs set it).
Usage: python -I -B -X utf8 b_imm2_twin_v01.py prepare | first | second
"""
import hashlib, json, pathlib, shutil, subprocess, sys

W = pathlib.Path(__file__).resolve().parents[2]
CD = W / 'CD_capture'
B = W / 'B_retrack'
FREEZE = W / 'locks' / 'FREEZE_B_add10.json'
COPIES = [(CD / 'ycheck' / 'y_twin_l12_v13.py', CD / 'ycheck_imm2' / 'y_twin_l12_v13.py')] + [
    (CD / 'recount' / n, CD / 'recount_imm2' / n) for n in ('rc_y_twin_l12_v13.py', 'rc_core_v13.py', 'rc_kern_v13.py', 'rc_y_kern_v13.py')]
PY = CD / '.venv' / 'Scripts' / 'python.exe'
B2DIR = B / 'out' / 'retrack_new' / 'IMM2'
MAN = B / 'out' / 'retrack_new' / 'IMM2_MANIFEST_v01.json'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def frozen():
    d = json.loads(FREEZE.read_text(encoding='utf-8'))
    return {str(W / e['path']): e['sha256'] for e in d['external_read_only']}


def prepare():
    fz = frozen()
    for src, dst in COPIES:
        want = fz.get(str(src))
        if want is None or sha(src) != want:
            raise SystemExit('REFUSED: %s differs from its SHA-256 in FREEZE_B_add10 (%s)' % (src, want))
        dst.parent.mkdir(exist_ok=True)
        if dst.exists():
            if sha(dst) != want:
                raise SystemExit('REFUSED: %s exists and differs' % dst)
            continue
        shutil.copyfile(src, dst)
        assert sha(dst) == want
        print('copied', dst.relative_to(W), want[:12])


def args_common():
    if not MAN.is_file():
        raise SystemExit('REFUSED: %s missing (write it with b_l12_retrack_v01.py manifest <root> --variant IMM2)' % MAN)
    return ['--intervals', 'nominal95', '--cases-sha', sha(CD / 'l12' / 'CASES_L12_v13.json'), '--b2-dir', str(B2DIR),
            '--b2-manifest', str(MAN), '--b2-manifest-sha', sha(MAN)]


def run(which):
    prepare()
    if which == 'first':
        cmd = [str(PY), '-I', '-B', '-X', 'utf8', str(CD / 'ycheck_imm2' / 'y_twin_l12_v13.py')] + args_common()
    else:
        cmd = [str(PY), '-I', '-B', '-X', 'utf8', str(CD / 'recount_imm2' / 'rc_y_twin_l12_v13.py')] + args_common() + ['--workers', '2']
    print(' '.join(cmd), flush=True)
    sys.exit(subprocess.call(cmd, cwd=str(CD)))


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'prepare':
        prepare()
    elif c in ('first', 'second'):
        run(c)
    else:
        raise SystemExit(__doc__)
