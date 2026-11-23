"""LOCAL STAND-IN for `numba` (not installed on this laptop): njit is the identity decorator, so Codex's
fast_overlap / fast_hull functions run as plain Python with the same IEEE double arithmetic (no fastmath in the
originals). Slower, same formulas. Checked through the bit-level replay comparison (tracker_harness_v0x.py)."""


def njit(*args, **kwargs):
    if len(args) == 1 and callable(args[0]) and not kwargs:
        return args[0]

    def deco(f):
        return f
    return deco


jit = njit
