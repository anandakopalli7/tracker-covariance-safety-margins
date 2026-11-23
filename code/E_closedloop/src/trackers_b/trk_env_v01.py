"""v13 shared tracker library (package B, revision v13): environment set-up. New file, 19 Nov 2026 (Claude Opus 5.5).

IMPORT THIS MODULE BEFORE numpy when bit-exact replay of the logged pod output is wanted on this laptop: it pins the OpenBLAS
kernel to Haswell (see P\\09_redesign\\m4_perception_model\\m4_common_v02.py, whose set-up this copies).

setup(codex_root=None, exact_trig=None)
    Puts Codex's tracker and planner code (the packet's 149_supported_sensor_preparation tree, or the same tree inside a pod
    packet) on sys.path exactly as the paid driver does, installs its overlap patch, and appends this library's stand-ins
    (shims\\) for third-party packages that are missing (pyquaternion, numba, shapely, lap, hydra, omegaconf). A real installed
    package always wins over a stand-in (they are at the END of sys.path).
    codex_root: path of the tree that holds code\\, vendor\\CANMOT\\src, legacy86\\...; default: env V13_CODEX_ROOT, else the
    laptop path of record.
    exact_trig: True installs correctly rounded sin/cos/atan2 on the tracker path (needed for bit-identity with the Linux pods on
    Windows); None = True on Windows, False elsewhere.
tracker_config(): the online tracker configuration of record (contracts\\tracker_config.json), class keys as int.
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import copy, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_CODEX = pathlib.Path(r'<library folder>\149_supported_sensor_preparation_20261101')
SHIMS = HERE / 'shims_v01'
STATE = dict(ready=False, codex=None, exact_trig=False, blas=None)


def blas_architecture():
    try:
        import threadpoolctl
        for lib in threadpoolctl.threadpool_info():
            if lib.get('internal_api') == 'openblas' and 'numpy' in str(lib.get('filepath', '')).lower():
                return lib.get('architecture')
    except Exception:
        return None
    return None


def setup(codex_root=None, exact_trig=None):
    if STATE['ready']:
        return STATE
    root = pathlib.Path(codex_root or os.environ.get('V13_CODEX_ROOT') or DEFAULT_CODEX)
    sys.path[:0] = [str(root / 'code'), str(root / 'sources'), str(root / 'vendor'), str(root / 'vendor' / 'CANMOT' / 'src'),
                    str(root / 'legacy86' / 'vendor' / 'nuscenes-devkit' / 'python-sdk')]
    sys.path.append(str(SHIMS))
    sys.dont_write_bytecode = True
    from fast_overlap_array import install
    install()
    if exact_trig is None:
        exact_trig = (os.name == 'nt')
    if exact_trig:
        sys.path.insert(0, str(HERE))
        import trk_exact_math_v01 as X
        X.install()
    STATE.update(ready=True, codex=str(root), exact_trig=bool(exact_trig), blas=blas_architecture())
    return STATE


def _ints(x):
    if isinstance(x, dict):
        return {(int(k) if isinstance(k, str) and k.isdigit() else k): _ints(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_ints(v) for v in x]
    return x


def tracker_config(codex_root=None):
    root = pathlib.Path(codex_root or STATE['codex'] or os.environ.get('V13_CODEX_ROOT') or DEFAULT_CODEX)
    return _ints(json.loads((root / 'contracts' / 'tracker_config.json').read_text(encoding='utf-8')))


def jl(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def deep(x):
    return copy.deepcopy(x)
