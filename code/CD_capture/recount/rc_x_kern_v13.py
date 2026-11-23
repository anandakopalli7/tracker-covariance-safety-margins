"""Recount of the crossing sprint X (A11): the statistic group of the double bootstrap as a PURE object (numpy via rc_kern_v13
only), so that the pod runner can rebuild it from a job file. New file, 21 Nov 2026 (Claude Sonnet 5.5). Importing this module
registers the kind 'cross' in rc_kern_v13.STAT_KINDS (rc_kern_v13 itself is unchanged)."""
import numpy as np
import rc_kern_v13 as KN

STATS = ['R_gl_pp', 'RR_E5N', 'RR_E5NmP', 'RR_N']


class XStat:
    """Run counts CN (B, nrun) -> (B, 4): R_gl (pp), RR_gl(E5_N), RR_gl(E5_N) - RR_gl(E5p_N), RR_gl(N).
    PX = Problem(F0, E, N, E5N, E5pN)."""
    kind = 'cross'

    def __init__(self, PX, STATS_=None):
        self.PX = PX
        self.STATS = list(STATS_ if STATS_ is not None else STATS)

    def __call__(self, CN):
        CN = np.ascontiguousarray(CN, float)
        if CN.ndim == 1:
            CN = CN[None]
        e = self.PX.evaluate(CN)
        den = e['denE']
        S = np.full((CN.shape[0], len(self.STATS)), np.nan)
        S[:, 0] = den / KN.NLEV
        c = KN.ratio_arr(e['D']['E5N'], den); cp = KN.ratio_arr(e['D']['E5pN'], den)
        S[:, 1] = c; S[:, 2] = c - cp; S[:, 3] = KN.ratio_arr(e['D']['N'], den)
        return S

    def to_arrays(self):
        return KN.problem_to_arrays(self.PX, 'PX_')

    @classmethod
    def from_arrays(cls, z, STATS_):
        return cls(KN.problem_from_arrays(z, 'PX_'), STATS_)


KN.STAT_KINDS['cross'] = XStat
