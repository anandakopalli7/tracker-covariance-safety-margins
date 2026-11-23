"""Package F (revision v13): runs the FROZEN independent recount (recount\\fr_heldout_v02.py, Claude Fable 5.2; in FREEZE_F) on a
RunPod pod, unchanged. New file, 20 Nov 2026 (Claude Opus 5.5), at the coordinator's offer of 09:28 EST (budget up to $10). Only
moves files; no numerics. The recount resolves every path from its own folder (fr_core_v01: V13 = recount/../../..; arrays in
F_nuscenes/cache; output A_RECOUNT_F.json in F_nuscenes/out), so the pod gets a mirror of that tree:
  /opt/frc/rv13/LOCK_A10_2.txt
  /opt/frc/rv13/work/F_nuscenes/recount/   the recount's .py and .json files, optA_lib_v02.py (the scoring library of record,
                                           copied unchanged from P; found because the recount puts its own folder on sys.path),
                                           and synth/ (its synthetic arrays and outputs) for the platform test
  /opt/frc/rv13/work/F_nuscenes/cache/{arrays_T1,arrays_IMM,clear_v02}/val/
  /opt/frc/rv13/work/F_nuscenes/out/
Every upload and download is SHA-256 checked. Python 3.12 venv /opt/fv with numpy 2.5.5 and numba 0.68.1 (= the laptop venv the
recount was tested with), set up by f17_calib_pod_v01.up.
  up NAME [--deadline-h H]     create the pod and the venv (f17 up)
  push_code NAME               the recount files, optA_lib_v02.py and synth/
  push_val NAME                Lock 2 and the val arrays and clearances (150 scenes each)
  run NAME [recount args]      python fr_heldout_v02.py [args] in the mirrored recount folder (blocking; log on the pod)
  fetch NAME synth|val DEST    the outputs (synth: synth/out/*synth_v02*.json; val: out/A_RECOUNT_F.json and
                               recount/F_RECOUNT_HELDOUT_v02.json), SHA-256 checked
  down NAME NOTE               delete the pod
Usage: python -I f18_recount_pod_v01.py <cmd> ...
"""
import hashlib, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fpods_v01 as pv           # noqa: E402
import f17_calib_pod_v01 as P17  # noqa: E402

F = HERE.parent
RC = F / 'recount'
LIB = pathlib.Path(r'<library folder>\optA_lib_v02.py')
LOCK2 = F.parent.parent / 'LOCK_A10_2.txt'
B = '/opt/frc/rv13'
RR = B + '/work/F_nuscenes/recount'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def put_tree(name, pairs):
    """pairs: (local file, remote path). mkdir -p every remote folder, upload, then compare sha256sum."""
    dirs = sorted({str(pathlib.PurePosixPath(r).parent) for _, r in pairs})
    P17.ssh(name, 'mkdir -p ' + ' '.join(dirs))
    r = pv.sftp(name, [f'put "{l}" "{rm}"' for l, rm in pairs], timeout=7200)
    if r.returncode != 0:
        raise SystemExit(f'{name}: upload failed {r.stderr[-400:]}')
    bad = []
    for i in range(0, len(pairs), 200):
        chunk = pairs[i:i + 200]
        out = P17.ssh(name, 'sha256sum ' + ' '.join(f'"{rm}"' for _, rm in chunk), timeout=600)
        got = {l.split(None, 1)[1].strip(): l.split()[0] for l in out.splitlines() if l.strip()}
        bad += [rm for l, rm in chunk if got.get(rm) != sha(l)]
    if bad:
        raise SystemExit(f'{name}: {len(bad)} uploaded files differ, e.g. {bad[:3]}')
    print(name, 'uploaded and checked:', len(pairs), 'files')


def push_code(name):
    pairs = [(p, f'{RR}/{p.name}') for p in sorted(RC.glob('*.py')) + sorted(RC.glob('F_RECOUNT_HORIZON_v0*.json'))]
    pairs.append((LIB, f'{RR}/optA_lib_v02.py'))
    for p in sorted((RC / 'synth').rglob('*')):
        # no checkpoints (_dboot_*: the recount resumes from them) and no earlier synthetic outputs: the platform test computes afresh
        if p.is_file() and not p.name.startswith('_dboot') and 'synth_v02' not in p.name:
            pairs.append((p, f'{RR}/synth/' + p.relative_to(RC / 'synth').as_posix()))
    put_tree(name, pairs)


def push_val(name):
    if not LOCK2.exists():
        raise SystemExit('REFUSED: no Lock 2')
    pairs = [(LOCK2, f'{B}/LOCK_A10_2.txt')]
    for sub in ('arrays_T1', 'arrays_IMM', 'clear_v02'):
        fs = sorted(p for p in (F / 'cache' / sub / 'val').glob('scene-*.npz') if '.tmp' not in p.name)
        if len(fs) != 150:
            raise SystemExit(f'{sub}/val has {len(fs)} files, not 150')
        pairs += [(p, f'{B}/work/F_nuscenes/cache/{sub}/val/{p.name}') for p in fs]
    P17.ssh(name, f'mkdir -p {B}/work/F_nuscenes/out {B}/logs')
    put_tree(name, pairs)


def run(name, args):
    tag = 'synth' if '--synth' in args else 'val'
    cmd = (f'mkdir -p {B}/logs && cd {RR} && /opt/fv/bin/python fr_heldout_v02.py {" ".join(args)} > {B}/logs/recount_{tag}.log 2>&1; '
           f'echo rc=$?; tail -n 8 {B}/logs/recount_{tag}.log')
    print(P17.ssh(name, cmd, timeout=6 * 3600))


def fetch(name, which, dest):
    dest = pathlib.Path(dest); dest.mkdir(parents=True, exist_ok=True)
    if which == 'synth':
        files = P17.ssh(name, f'cd {RR}/synth/out && ls *synth_v02*.json').split()
        remote = [f'{RR}/synth/out/{f}' for f in files]
    else:
        remote = [f'{B}/work/F_nuscenes/out/A_RECOUNT_F.json', f'{RR}/F_RECOUNT_HELDOUT_v02.json']
    remote.append(f'{B}/logs/recount_{which}.log')
    sums = {l.split(None, 1)[1].strip(): l.split()[0] for l in P17.ssh(name, 'sha256sum ' + ' '.join(remote)).splitlines() if l.strip()}
    r = pv.sftp(name, [f'get "{rm}" "{dest / pathlib.PurePosixPath(rm).name}"' for rm in remote])
    if r.returncode != 0:
        raise SystemExit(f'{name}: download failed {r.stderr[-400:]}')
    bad = [rm for rm in remote if sha(dest / pathlib.PurePosixPath(rm).name) != sums[rm]]
    if bad:
        raise SystemExit(f'{name}: downloaded files differ: {bad}')
    print(name, 'fetched and checked:', [pathlib.PurePosixPath(x).name for x in remote])


def main():
    a = sys.argv[1:]
    c = a[0]
    if c == 'up':
        P17.up(a[1], float(a[a.index('--deadline-h') + 1]) if '--deadline-h' in a else 4.0,
               a[a.index('--gpu') + 1] if '--gpu' in a else P17.GPU, 'package F recount (frozen fr_heldout_v02) on a pod')
    elif c == 'push_code':
        push_code(a[1])
    elif c == 'push_val':
        push_val(a[1])
    elif c == 'run':
        run(a[1], a[2:])
    elif c == 'fetch':
        fetch(a[1], a[2], a[3])
    elif c == 'down':
        pv.delete(a[1], a[2] if len(a) > 2 else '')
    else:
        raise SystemExit('unknown command')


if __name__ == '__main__':
    main()
