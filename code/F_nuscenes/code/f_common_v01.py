"""Package F (revision v13): shared paths, the Lock 2 gate, the nuScenes splits and the tracker set-up. New file,
19 Nov 2026 (Claude Opus 5.5). Import this module BEFORE numpy (it pins OpenBLAS to one Haswell thread, as the
project's tracker harness does, so that tracker runs are reproducible and processes do not oversubscribe the CPU).

Gate (A10 section 8.6; README_COORDINATION rule 3): require_split('val') raises RuntimeError('REFUSED ...') unless
revision_v13\\LOCK_A10_2.txt exists. Every F script that reads detections, annotations or poses calls it per scene.
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
import hashlib, json, pathlib, sys, time

F = pathlib.Path(__file__).resolve().parents[1]                 # work\F_nuscenes
V13 = F.parents[1]                                              # revision_v13
LIB = F / 'lib'
DATA = V13 / 'data' / 'nuscenes'
META = DATA / 'v1.0-trainval'
RESULTS = pathlib.Path(r'<library folder>\nusc_results_flip')
RESULT_FILES = {'train': RESULTS / 'infos_train_10sweeps_withvelo_filter_True.json',
                'val': RESULTS / 'infos_val_10sweeps_withvelo_filter_True.json'}
LOCK2 = V13 / 'LOCK_A10_2.txt'
CACHE = F / 'cache'
OUT = F / 'out'
LOGS = F / 'logs'
for _d in (CACHE, OUT, LOGS):
    _d.mkdir(exist_ok=True)


def lock2_exists():
    return LOCK2.exists()


def require_split(split):
    """The held-out gate. 'train' (design split) passes; 'val' only after Lock 2; anything else is refused."""
    if split == 'train':
        return
    if split == 'val':
        if not LOCK2.exists():
            raise RuntimeError('REFUSED: the val scenes are held out until %s exists (A10 section 8.6)' % LOCK2)
        return
    raise RuntimeError('REFUSED: unknown split %r' % (split,))


def splits():
    """{'train': [scene names], 'val': [...]} from the devkit's nuscenes/utils/splits.py (lists only; no devkit import)."""
    src = (LIB / 'devkit' / 'python-sdk' / 'nuscenes' / 'utils' / 'splits.py').read_text(encoding='utf-8')
    src = src.replace('from nuscenes import NuScenes', 'NuScenes = None')
    ns = {'__name__': 'nusc_splits'}
    exec(compile(src, 'splits.py', 'exec'), ns)
    tr, va = list(ns['train']), list(ns['val'])
    if len(tr) != 700 or len(va) != 150 or set(tr) & set(va):
        raise RuntimeError('unexpected nuScenes split sizes %d / %d' % (len(tr), len(va)))
    return {'train': tr, 'val': va}


def setup_tracker():
    """Put the copied planner library, CANMOT and the stand-ins on sys.path (the order of m4_common_v02.setup_codex) and
    install the overlap patch of the paid driver. Real installed packages win over the stand-ins (appended last)."""
    paths = [LIB / 'code149', LIB / 'vendor149', LIB / 'vendor149' / 'CANMOT' / 'src', LIB / 'devkit' / 'python-sdk']
    for p in reversed(paths):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    if str(LIB / 'shims_v01') not in sys.path:
        sys.path.append(str(LIB / 'shims_v01'))
    sys.dont_write_bytecode = True
    from fast_overlap_array import install
    install()


def setup_planner():
    for p in (LIB / 'code149', LIB / 'vendor149'):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    sys.dont_write_bytecode = True


def ints(x):
    if isinstance(x, dict):
        return {(int(k) if isinstance(k, str) and k.isdigit() else k): ints(v) for k, v in x.items()}
    if isinstance(x, list):
        return [ints(v) for v in x]
    return x


def tracker_config():
    """CANMOT's nuScenes configuration as bound by the project (149\\contracts\\tracker_config.json, copied unchanged)."""
    return ints(json.loads((LIB / 'tracker_config.json').read_text(encoding='utf-8')))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 22), b''):
            h.update(blk)
    return h.hexdigest()


def clock():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def jdump(obj):
    return json.dumps(obj, indent=1, default=float, allow_nan=True)
