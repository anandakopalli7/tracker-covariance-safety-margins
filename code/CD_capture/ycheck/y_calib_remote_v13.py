"""Y (A11 sec. 6b): A10 sec. 2.6 double-bootstrap runner for a kind-'Y' job (y_twin_v13.YStat.save). New file, 21 Nov 2026 (Claude
Opus 5.5, session CD). It is the frozen analysis\\calib_remote_v13.py (imported unchanged from the same folder) with one addition: a
kind-'Y' job's statistic, Delta = RR_gl(N) - mean over the twins of RR_gl(Tp_k), NaN where D_gl(E) <= 0, computed by the frozen
gl_fast_v13.evaluate. Every other kind is passed to calib_remote_v13's own loader; seeds, chunking and outputs are calib_remote_v13's.
Usage (as calib_remote_v13.py): python y_calib_remote_v13.py JOBDIR LABEL [--seeds 20261913,20261914] [--threads N] [--outer A:B]
"""
import json, pathlib, sys
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import calib_remote_v13 as CR            # noqa: E402  (frozen, unchanged)
import gl_fast_v13 as GF                 # noqa: E402

_load = CR.load


def load(job):
    z = np.load(job, allow_pickle=False)
    if str(z['kind']) != 'Y': return _load(job)
    P = CR._P(); P.names = [str(x) for x in z['names']]; P.pop = int(z['pop']); P.T0 = [x for x in z['T0']]
    P.d = np.ascontiguousarray(z['d']); P.ri = z['ri'].astype(np.int64); P.keep = z['keep'].astype(np.int64)
    P.ev_off = z['ev_off'].astype(np.int64); P.keep_off = z['keep_off'].astype(np.int64); P.nrun = P.T0[0].shape[0]
    tw = json.loads(str(z['twins']))

    def stat(Wr):
        e = GF.evaluate(P, Wr); den = e['denE']; ok = np.isfinite(den) & (den > 0)
        with np.errstate(divide='ignore', invalid='ignore'):
            rn = np.where(ok, e['D']['N'] / den, np.nan)
            rp = np.mean(np.stack([np.where(ok, e['D'][a] / den, np.nan) for a in tw]), axis=0)
        return (rn - rp)[:, None]
    return stat


CR.load = load

if __name__ == '__main__':
    CR.main()
