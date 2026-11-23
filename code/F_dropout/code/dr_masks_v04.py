"""Revision v13, AMENDMENT_12 sec. 3a: the one mask law (A11 sec. 6c) with the window start probability p, the set of window lengths
and the gap length as parameters, for a possible 10 Hz configuration. New file, 22 Nov 2026 (Claude Opus 5.5, session F).
  rng = numpy.random.default_rng(int.from_bytes(hashlib.sha256(("A11/D/" + case_id).encode("utf-8")).digest()[:8], "big"))
  rows i = 0 .. n - 1 (the detector rows at the configuration's rate, logged order); row 0 is never masked. From i = 1, at each row not
  inside a window: u = rng.random(); if u < p: j = rng.integers(0, len(Ls)) and L = Ls[j]; rows i .. i + L - 1 are masked (cut at
  n - 1); the `gap` rows right after a window are never masked and draw nothing; draws resume after them (i += L + gap).
  Otherwise i += 1.
Defaults p = 0.10, Ls = (1, 2, 3), gap = 1 are A11 sec. 6c's law exactly: rng.integers(0, 3) consumes the same draw as
rng.integers(1, 4) and gives the value minus one (checked: `check`, equal to dr_masks_v03 and to DR_MASKS_v02.json on all 225 runs).
A 10 Hz configuration would be, for example, mask(case_id, n, p=0.02, Ls=(5, 10, 15), gap=5).
Usage: python -I dr_masks_v04.py check
"""
import hashlib, json, pathlib, sys
import numpy as np

PREFIX = 'A11/D/'
HERE = pathlib.Path(__file__).resolve().parent


def seed_of(case_id):
    return int.from_bytes(hashlib.sha256((PREFIX + case_id).encode('utf-8')).digest()[:8], 'big')


def mask(case_id, n, p=0.10, Ls=(1, 2, 3), gap=1):
    Ls = tuple(int(x) for x in Ls)
    rng = np.random.default_rng(seed_of(case_id))
    out = []; i = 1
    while i < n:
        if rng.random() < p:
            L = Ls[int(rng.integers(0, len(Ls)))]
            out.extend(range(i, min(i + L, n)))
            i += L + gap
        else:
            i += 1
    return out


def check():
    sys.path.insert(0, str(HERE))
    import dr_masks_v02 as M2, dr_masks_v03 as M3
    d = json.loads((HERE.parent / 'masks' / 'DR_MASKS_v02.json').read_text(encoding='utf-8'))
    bad = []
    for k in ('fresh', 'tuning'):
        for rid, v in d[k].items():
            m4 = mask(v['case_id'], v['n'])
            if m4 != v['masked'] or m4 != M2.mask(v['case_id'], v['n']):
                bad.append(rid)
            for p in M3.P_VALUES:
                if mask(v['case_id'], v['n'], p) != M3.mask(v['case_id'], v['n'], p):
                    bad.append((rid, p))
    print('defaults vs DR_MASKS_v02.json / dr_masks_v02, and p in %s vs dr_masks_v03: %d runs, mismatches %d'
          % (M3.P_VALUES, sum(len(d[k]) for k in ('fresh', 'tuning')), len(bad)))
    return not bad


if __name__ == '__main__':
    if sys.argv[1] == 'check':
        sys.exit(0 if check() else 1)
