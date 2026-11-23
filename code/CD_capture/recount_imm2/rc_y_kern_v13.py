"""Recount of test Y (A11 section 6b): the statistic group of the double bootstrap as a PURE object (numpy via rc_kern_v13 only), so
that the pod runner can rebuild it from a job file. New file, 21 Nov 2026 (Claude Sonnet 5.5). Importing this module registers the
kind 'ytwin' in rc_kern_v13.STAT_KINDS (rc_kern_v13 itself is unchanged)."""
import numpy as np
import rc_kern_v13 as KN

STATS = ['delta']
NPERM = 20


def twin_names(k=NPERM):
    return ['p%02d' % (i + 1) for i in range(k)]


def twin_mean(rr_list):
    """RR_gl(Bp): the mean over the twins of RR_gl(Bp_k), within the resample (one function for every caller)."""
    return np.mean(np.stack([np.asarray(x, float) for x in rr_list], axis=0), axis=0)


class YStat:
    """Run counts CN (B, nrun) -> (B, 1): Delta = RR_gl(N) - mean_k RR_gl(p_k).
    PY = Problem(F0, E, N, p01 ... p20) (the twins fixed, not redrawn per resample)."""
    kind = 'ytwin'

    def __init__(self, PY, STATS_=None):
        self.PY = PY
        self.STATS = list(STATS_ if STATS_ is not None else STATS)

    def __call__(self, CN):
        CN = np.ascontiguousarray(CN, float)
        if CN.ndim == 1:
            CN = CN[None]
        e = self.PY.evaluate(CN)
        den = e['denE']
        S = np.full((CN.shape[0], len(self.STATS)), np.nan)
        rrN = KN.ratio_arr(e['D']['N'], den)
        rrp = twin_mean([KN.ratio_arr(e['D'][nm], den) for nm in self.PY.names[3:]])
        S[:, 0] = rrN - rrp
        return S

    def to_arrays(self):
        return KN.problem_to_arrays(self.PY, 'PY_')

    @classmethod
    def from_arrays(cls, z, STATS_):
        return cls(KN.problem_from_arrays(z, 'PY_'), STATS_)


KN.STAT_KINDS['ytwin'] = YStat
