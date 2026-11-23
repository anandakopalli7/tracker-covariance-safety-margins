"""Correctly rounded sin / cos / atan2 for doubles, and a run-time switch that makes the tracker path use them.

Why: the paid runs were computed on Linux pods (glibc math library); this laptop's Windows math library returns a
cos/sin that is one unit in the last place off the correctly rounded value for about 3 % of arguments
(diag_trig_v02.py). That alone makes the offline tracker replay differ from the logs by ~1e-15 in runs whose objects
have a yaw far from zero (diag_trig_v01.py: replacing cos by the correctly rounded value reproduces the logged P bit
for bit). Here sin/cos/atan2 are computed in 80-digit decimal arithmetic and rounded once to the nearest double.

install() rebinds module-global NAMES at run time (no file of the tracker code is changed):
    canmot.motion_module.motion_model.np   -> proxy of numpy with cos, sin replaced
    canmot.geometry.nusc_utils.np          -> proxy of numpy with cos replaced
    canmot.geometry.nusc_distance.np       -> proxy of numpy with arctan2 replaced
    tracker_audit.math                     -> proxy of math with cos, sin replaced (the audit's "expected" values)
    pyquaternion (local stand-in) sin, cos, atan2
"""
import functools
import math
from decimal import Decimal, localcontext

import numpy as _np

_PREC = 80
_CALLS = dict(sin=0, cos=0, atan2=0, fallback=0)


def _dec_sin_cos(X):
    """sin, cos of the Decimal X by Taylor series (call inside a localcontext with prec = _PREC; |X| < 8)."""
    s = Decimal(0)
    c = Decimal(0)
    term = Decimal(1)
    n = 0
    tiny = Decimal(10) ** -(_PREC + 2)
    while n < 4 or abs(term) > tiny:
        if n % 2 == 0:
            c += term if (n // 2) % 2 == 0 else -term
        else:
            s += term if (n // 2) % 2 == 0 else -term
        n += 1
        term = term * X / n
    return s, c


@functools.lru_cache(maxsize=400000)
def _sin_cos(x):
    with localcontext() as ctx:
        ctx.prec = _PREC
        s, c = _dec_sin_cos(Decimal(x))
        return float(s), float(c)


def cr_sin(x):
    x = float(x)
    _CALLS['sin'] += 1
    if x == 0.0 or not math.isfinite(x) or abs(x) > 8.0:
        _CALLS['fallback'] += (x != 0.0)
        return math.sin(x)
    return _sin_cos(x)[0]


def cr_cos(x):
    x = float(x)
    _CALLS['cos'] += 1
    if x == 0.0 or not math.isfinite(x) or abs(x) > 8.0:
        _CALLS['fallback'] += (x != 0.0)
        return math.cos(x)
    return _sin_cos(x)[1]


@functools.lru_cache(maxsize=400000)
def _atan2(y, x):
    with localcontext() as ctx:
        ctx.prec = _PREC
        Y = Decimal(y)
        X = Decimal(x)
        t = Decimal(math.atan2(y, x))
        for _ in range(3):                       # Newton on X sin t - Y cos t = 0 (error e -> about e^3 / 3)
            s, c = _dec_sin_cos(t)
            t = t - (X * s - Y * c) / (X * c + Y * s)
        return float(t)


def cr_atan2(y, x):
    y = float(y)
    x = float(x)
    _CALLS['atan2'] += 1
    if y == 0.0 or x == 0.0 or not (math.isfinite(x) and math.isfinite(y)):
        return math.atan2(y, x)                  # exact special values
    return _atan2(y, x)


def _vec1(fun, np_fun):
    def f(x, *a, **k):
        if a or k:
            return np_fun(x, *a, **k)
        if _np.ndim(x) == 0:
            return _np.float64(fun(float(x)))
        arr = _np.asarray(x, dtype=float)
        return _np.array([fun(float(v)) for v in arr.ravel()], dtype=float).reshape(arr.shape)
    return f


def _vec2(fun, np_fun):
    def f(y, x, *a, **k):
        if a or k:
            return np_fun(y, x, *a, **k)
        if _np.ndim(y) == 0 and _np.ndim(x) == 0:
            return _np.float64(fun(float(y), float(x)))
        ya, xa = _np.broadcast_arrays(_np.asarray(y, dtype=float), _np.asarray(x, dtype=float))
        return _np.array([fun(float(p), float(q)) for p, q in zip(ya.ravel(), xa.ravel())], dtype=float).reshape(ya.shape)
    return f


class _Proxy:
    """Stands for a module; every attribute comes from the real module except the overridden ones."""

    def __init__(self, real, **over):
        object.__setattr__(self, '_real', real)
        for k, v in over.items():
            object.__setattr__(self, k, v)

    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, '_real'), name)


_installed = ()


def install(parts=('mm', 'nu', 'nd', 'ta', 'pq')):
    """Switch the named parts of the tracker path to correctly rounded trig. Call after m4_common.setup_codex()."""
    global _installed
    np_cos = _vec1(cr_cos, _np.cos)
    np_sin = _vec1(cr_sin, _np.sin)
    np_atan2 = _vec2(cr_atan2, _np.arctan2)
    if 'mm' in parts:
        import canmot.motion_module.motion_model as mm
        mm.np = _Proxy(_np, cos=np_cos, sin=np_sin)
    if 'nu' in parts:
        import canmot.geometry.nusc_utils as nu
        nu.np = _Proxy(_np, cos=np_cos, sin=np_sin)
    if 'nd' in parts:
        import canmot.geometry.nusc_distance as nd
        nd.np = _Proxy(_np, arctan2=np_atan2)
    if 'ta' in parts:
        import tracker_audit as ta
        ta.math = _Proxy(math, cos=cr_cos, sin=cr_sin)
    if 'pq' in parts:
        import pyquaternion as pq
        if 'shims_v01' not in str(pq.__file__):
            raise RuntimeError('pyquaternion is not the local stand-in: %s' % pq.__file__)
        pq.sin = cr_sin
        pq.cos = cr_cos
        pq.atan2 = cr_atan2
    _installed = tuple(parts)
    return _installed


def calls():
    return dict(_CALLS, installed=','.join(_installed))


if __name__ == '__main__':
    import random
    rnd = random.Random(7)
    bad = dict(sin=0, cos=0, atan2=0)
    N = 5000
    for _ in range(N):
        x = rnd.uniform(-math.pi, math.pi)
        bad['sin'] += cr_sin(x) != math.sin(x)
        bad['cos'] += cr_cos(x) != math.cos(x)
        y = rnd.uniform(-2, 2)
        z = rnd.uniform(-2, 2)
        bad['atan2'] += cr_atan2(y, z) != math.atan2(y, z)
    print('this platform math library differs from the correctly rounded value in', bad, 'of', N)
    print('cr_cos(-0.15210536931985597) =', repr(cr_cos(-0.15210536931985597)), '(logged pod value 0.9884542643065177)')
    print('max |cr - math|: sin %.3g cos %.3g' % (max(abs(cr_sin(x) - math.sin(x)) for x in [i * 0.001 for i in range(-3141, 3142)]),
                                                 max(abs(cr_cos(x) - math.cos(x)) for x in [i * 0.001 for i in range(-3141, 3142)])))
