"""Package F recount: building the sources of a population and running the resamples. New file, 19 Nov 2026 (Claude Fable 5.2).
Used by fr_horizon_v01.py (design split: F0 and E of T1 only) and fr_heldout_v01.py (held-out split, after Lock 2).
"""
import sys
import numpy as np
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import fr_core_v01 as K

L = K.L
HKEYS = {3: dict(clear='clear', ev='evaluated', suf=''), 2: dict(clear='clear2', ev='evaluated2', suf='_2')}
POPS = ('all', 'inpath')


def mask_fn(h, pop):
    ek = HKEYS[h]['ev']
    if pop == 'all':
        return lambda k, z: z[ek].astype(bool)
    return lambda k, z: z[ek].astype(bool) & z['inpath'].astype(bool)


def build_pack(scenes, h, pop, crit_fns):
    """crit_fns: list of (name, fn(k, z) -> (n, 17) critical scales); [0] must be F0 and [1] E."""
    assert crit_fns[0][0] == 'F0' and crit_fns[1][0] == 'E'
    src = [K.Source(scenes, fn, HKEYS[h]['clear'], mask_fn(h, pop)) for _, fn in crit_fns]
    info = {nm: dict(events=s.n_events, points=s.n_points) for (nm, _), s in zip(crit_fns, src)}
    return K.pack(src), info


def run(W, pk, chunk=2000, label=None):
    out = []
    for a in range(0, W.shape[0], chunk):
        out.append(K.kernel2(np.ascontiguousarray(W[a:a + chunk]), *pk))
        if label:
            print('  %s: %d / %d resamples' % (label, min(a + chunk, W.shape[0]), W.shape[0]), flush=True)
    return np.concatenate(out)


def summ_room(Db, Dpt):
    """Room R_gl = D_gl(E, F0) / 201 in percentage points: point, 95% percentile interval over the finite resamples, share of
    resamples with D <= 0 (non-finite resamples counted as not positive, as optA_lib_v02.summ_den)."""
    Rb = Db / K.NLEV
    return dict(point=float(Dpt / K.NLEV), ci95=K.pint(Rb, 0.95), share_le0=float(np.mean(~(Db > 0))),
                n_le0=int((~(Db > 0)).sum()), n_nonfinite=int((~np.isfinite(Db)).sum()), n_resamples=int(Db.size))


def summ_ratio(b, pt, level=0.95):
    b = np.asarray(b, float); f = np.isfinite(b)
    return dict(point=float(pt), ci=K.pint(b, level), level=float(level), invalid_share=float(1. - f.mean()),
                n_invalid=int((~f).sum()))


def counts(scenes, h):
    ek = HKEYS[h]['ev']
    return dict(scenes=len(scenes), decisions_built=int(sum(z[ek].size for z in scenes)),
                evaluated=int(sum(z[ek].sum() for z in scenes)),
                evaluated_inpath=int(sum((z[ek].astype(bool) & z['inpath'].astype(bool)).sum() for z in scenes)))
