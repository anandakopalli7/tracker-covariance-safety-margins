"""Revision v13, AMENDMENT_12 sec. 3a.4: the one mask law (A11 sec. 6c "One mask law"; dr_masks_v02.py, frozen in FREEZE_DR) with the
window start probability p as a parameter. New file, 22 Nov 2026 (Claude Opus 5.5, session F). With p = 0.10 it is dr_masks_v02.mask
exactly (checked by `check02`). Seed string, draw order, L in {1, 2, 3} and the gap row are unchanged; masks differ across p only
through u < p.
Usage: python -I dr_masks_v03.py check02          (p = 0.10 equals dr_masks_v02 on all 225 runs of DR_MASKS_v02.json)
"""
import hashlib, json, pathlib, sys
import numpy as np

PREFIX = 'A11/D/'
L_MAX = 3
P_VALUES = (0.05, 0.10, 0.20, 0.30)
HERE = pathlib.Path(__file__).resolve().parent


def seed_of(case_id):
    return int.from_bytes(hashlib.sha256((PREFIX + case_id).encode('utf-8')).digest()[:8], 'big')


def mask(case_id, n, p=0.10):
    rng = np.random.default_rng(seed_of(case_id))
    out = []; i = 1
    while i < n:
        if rng.random() < p:
            L = int(rng.integers(1, L_MAX + 1))
            out.extend(range(i, min(i + L, n)))
            i += L + 1
        else:
            i += 1
    return out


def ptag(p):
    return 'p%03d' % int(round(p * 100))


def check02():
    sys.path.insert(0, str(HERE))
    import dr_masks_v02 as M2
    d = json.loads((HERE.parent / 'masks' / 'DR_MASKS_v02.json').read_text(encoding='utf-8'))
    bad = [rid for k in ('fresh', 'tuning') for rid, v in d[k].items()
           if mask(v['case_id'], v['n'], 0.10) != v['masked'] or mask(v['case_id'], v['n'], 0.10) != M2.mask(v['case_id'], v['n'])]
    print('p = 0.10 against dr_masks_v02 / DR_MASKS_v02.json:', sum(len(d[k]) for k in ('fresh', 'tuning')), 'runs, mismatches', len(bad))
    return not bad


if __name__ == '__main__':
    if sys.argv[1] == 'check02':
        sys.exit(0 if check02() else 1)
