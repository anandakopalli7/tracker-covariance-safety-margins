"""Revision v13, AMENDMENT_12 sec. 3a: decides whether the A10 sec. 2.6 second inner seed (20261914) must be run BEFORE the import.
New file, 22 Nov 2026 (Claude Opus 5.5, session F). In import mode cd_common_v13.calibrate_all / dr_dose_v01 use the first seed's
shares as the second when the second seed's file is absent, which is right only when no statistic needs the checks. This script reads
a remote result (p_lt, p_le per outer sample and statistic) and prints, per statistic, the coverage of the nominal 95% interval with
cd_common_v13.cover_two's rule (copied: share(inner <= value) >= a/2 - 1e-12 and share(inner < value) <= 1 - a/2 + 1e-12, over the
outer samples with a finite share), and NEEDS_SECOND_SEED when any coverage is below 0.94 (cd_common_v13.calibrate_all's rule).
It computes no reported value.
Usage: python -I dr_calib_cover_v01.py RESULT.npz NAME[,NAME...]
"""
import sys
import numpy as np


def cover_two(lt, le, nom):
    a = 1. - nom; ok = np.isfinite(lt)
    return ((le[ok] >= a / 2. - 1e-12) & (lt[ok] <= 1. - a / 2. + 1e-12))


def main():
    z = np.load(sys.argv[1], allow_pickle=False)
    names = sys.argv[2].split(',')
    lt, le = np.atleast_2d(z['p_lt']), np.atleast_2d(z['p_le'])
    if lt.shape[0] != 2000 and lt.shape[1] == 2000: lt, le = lt.T, le.T
    assert lt.shape[1] == len(names), (lt.shape, names)
    need = False
    for j, nm in enumerate(names):
        ind = cover_two(lt[:, j], le[:, j], 0.95)
        c95 = float(ind.mean()) if ind.size else float('nan')
        flag = (np.isfinite(c95) and c95 < 0.94)
        need = need or flag
        print('%-16s coverage95 %.4f  outer valid %d  %s' % (nm, c95, int(np.isfinite(lt[:, j]).sum()), 'BELOW 0.94' if flag else 'ok'))
    print('NEEDS_SECOND_SEED' if need else 'SEED_1_SUFFICES')


if __name__ == '__main__':
    main()
