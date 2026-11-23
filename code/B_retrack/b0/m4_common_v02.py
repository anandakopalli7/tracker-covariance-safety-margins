"""v13 B0 copy (19 Nov 2026): OUT redirected to B_retrack/out/b0; index and shims read from P (read only). Otherwise unchanged.
"""
"""Shared helpers for the m4 perception-model work. Imports Codex's tracker code READ-ONLY (run python with -I -B).

IMPORT THIS MODULE BEFORE numpy. It pins the OpenBLAS kernel to 'Haswell' (AVX2): with the laptop's default kernel
('SkylakeX', AVX-512) the tracker's 10x10 matrix products round differently in the last bit and the replay differs
from the logged pod output by up to 4.4e-16; with the Haswell (or Zen) kernel the replay is bit-identical
(measured with tracker_harness_v01.py / v02 on p2_c1109_tune_0000_fixed_c1).

Chain reproduced here (driver: 03_runbook/packet_main_v03/claude_smoke_v01/probe_arms_v01.py):
  detector tick k (k >= 19 and k % 10 == 9): tracks = OnlineTracker.step(model_rows, now), now = simulation time
  every tick k: actors = serial_actors(planner_actors(tracks_of_last_detector_tick, REFLECT @ state.center_lh(k), route_yaw))
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import csv, json, math, pathlib, sys
import numpy as np

ROOT = pathlib.Path(r'<library folder>')
M4 = ROOT / '09_redesign' / 'm4_perception_model'          # read only: run index and shims
OUT = pathlib.Path(__file__).resolve().parent.parent / 'out' / 'b0'   # v13 B0: outputs here
CODEX = pathlib.Path(r'<library folder>\149_supported_sensor_preparation_20261101')
SIM_DT = 0.05
_ready = False


def blas_architecture():
    """Kernel type the loaded OpenBLAS really uses (None if it cannot be read)."""
    try:
        import threadpoolctl
        for lib in threadpoolctl.threadpool_info():
            if lib.get('internal_api') == 'openblas' and 'numpy' in str(lib.get('filepath', '')).lower():
                return lib.get('architecture')
    except Exception:
        return None
    return None


def require_exact_blas():
    arch = blas_architecture()
    if arch not in ('Haswell', 'Zen'):
        raise RuntimeError('OpenBLAS kernel is %r, not Haswell/Zen: the tracker replay would not be bit-identical. '
                           'Set OPENBLAS_CORETYPE=Haswell in the environment before starting python.' % (arch,))
    return arch


def setup_codex():
    """Put Codex's code on sys.path (read-only use) and install its overlap patch, exactly as the paid driver does."""
    global _ready
    if _ready:
        return
    P = CODEX
    sys.path[:0] = [str(P / 'code'), str(P / 'sources'), str(P / 'vendor'), str(P / 'vendor' / 'CANMOT' / 'src'),
                    str(P / 'legacy86' / 'vendor' / 'nuscenes-devkit' / 'python-sdk')]
    # Third-party packages missing on this laptop (pyquaternion, numba, shapely, lap, hydra, omegaconf) resolve to the
    # local stand-ins in shims_v01 (END of sys.path: a real installed package would always win).
    sys.path.append(str(M4 / 'shims_v01'))
    sys.dont_write_bytecode = True
    from fast_overlap_array import install
    install()
    _ready = True


def ints(x):
    if isinstance(x, dict):
        return {(int(k) if k.isdigit() else k): ints(v) for k, v in x.items()}
    if isinstance(x, list):
        return [ints(v) for v in x]
    return x


_cfg = None


def tracker_config():
    global _cfg
    if _cfg is None:
        _cfg = (CODEX / 'contracts' / 'tracker_config.json').read_text(encoding='utf-8')
    return ints(json.loads(_cfg))


def jl(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def load_index(name='run_index_m4_v02.csv', only_use=True):
    rows = []
    with open(M4 / name, encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f):
            r['use'] = int(r['use'])
            r['frames'] = int(r['frames'])
            r['occluder'] = r['occluder'] == 'True'
            r['contact'] = r['contact'] == 'True'
            r['desired_mps'] = float(r['desired_mps'])
            if only_use and not r['use']:
                continue
            rows.append(r)
    return rows


def max_abs_diff(a, b):
    """Largest absolute difference between two nested JSON-like values; inf if the structure differs."""
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            return math.inf
        return max([max_abs_diff(a[k], b[k]) for k in a] or [0.0])
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return math.inf
        return max([max_abs_diff(x, y) for x, y in zip(a, b)] or [0.0])
    if isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or isinstance(b, str) or a is None or b is None:
        return 0.0 if a == b else math.inf
    return abs(float(a) - float(b))
