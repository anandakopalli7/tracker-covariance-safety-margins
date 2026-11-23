"""AMENDMENT_12 sec. 5b (decision test under injected detection dropouts on the nuScenes val logs): shared paths, gates and the
tracker set-up. New file, 22 Nov 2026 (Claude Opus 5.5, worker of package F). A copy of work\\F_nuscenes\\code\\f_common_v01.py
(frozen; unchanged there) with these changes only:
  - inputs are read from package F's folder SRC = work\\F_nuscenes (read only): its lib\\ (tracker and planner copies, CANMOT's
    configuration of record), cache\\val\\ (keyframes, truth, CenterPoint detections), cache\\clear_v02\\ (clearance under the
    departure), out\\PBAR_T1_train_v01.json (F0) and, for the acceptance test only, cache\\tracks_T1\\ and cache\\arrays_T1\\;
  - outputs go to this folder HOME = work\\F_dropout_nus (cache\\, out\\, logs\\);
  - a second gate: require_masked(split) refuses the val split unless revision_v13\\LOCK_A12c.txt exists (no value of the masked
    val run before the lock); the design split (train) is allowed for code tests;
  - tracker_config(punish_num) returns the configuration of record with output.punish_num replaced (1 = record; 3 = sec. 5b).
The relative layout is the same on a pod (root /root/fn mirrors ...\\Downloads), so every path below is derived from this file.
Import this module BEFORE numpy (it pins OpenBLAS to one Haswell thread, as F's file does).
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
import hashlib, json, pathlib, sys, time

HOME = pathlib.Path(__file__).resolve().parents[1]              # work\F_dropout_nus
WORK = HOME.parent
V13 = WORK.parent                                               # revision_v13
SRC = WORK / 'F_nuscenes'                                       # package F (read only)
LIB = SRC / 'lib'
SRC_CACHE = SRC / 'cache'
PBAR_FILE = SRC / 'out' / 'PBAR_T1_train_v01.json'
LOCK2 = V13 / 'LOCK_A10_2.txt'
LOCK12C = V13 / 'LOCK_A12c.txt'
CACHE = HOME / 'cache'
OUT = HOME / 'out'
LOGS = HOME / 'logs'
for _d in (CACHE, OUT, LOGS):
    _d.mkdir(exist_ok=True)
PUNISH_RECORD = 1
PUNISH_5B = 3


def require_split(split):
    """F's held-out gate, unchanged: 'train' passes; 'val' only after Lock 2."""
    if split == 'train':
        return
    if split == 'val':
        if not LOCK2.exists():
            raise RuntimeError('REFUSED: the val scenes are held out until %s exists (A10 section 8.6)' % LOCK2)
        return
    raise RuntimeError('REFUSED: unknown split %r' % (split,))


def require_masked(split):
    """Sec. 5b gate: no value of the masked val run before LOCK_A12c.txt."""
    require_split(split)
    if split == 'val' and not LOCK12C.exists():
        raise RuntimeError('REFUSED: no masked val value before %s exists (AMENDMENT_12 sec. 5b)' % LOCK12C)


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
    """As f_common_v01.setup_tracker (F's lib, same order, the overlap patch; stand-ins appended last)."""
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


def tracker_config(punish_num=PUNISH_RECORD):
    """CANMOT's nuScenes configuration as bound by the project (F's lib\\tracker_config.json), with output.punish_num set."""
    cfg = ints(json.loads((LIB / 'tracker_config.json').read_text(encoding='utf-8')))
    if cfg['output']['punish_num'] != PUNISH_RECORD:
        raise RuntimeError('the configuration of record no longer has punish_num = 1')
    cfg['output']['punish_num'] = int(punish_num)
    return cfg


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
