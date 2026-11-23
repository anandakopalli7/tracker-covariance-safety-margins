"""Recount3 (independent second program) for Table S12b, the subsampling columns of Table S17, Table S24b and Table S25
with the benign-run check. Library v01, 18 Nov 2026.

Written from revision_v11\\recount3\\RECOUNT3_BRIEF_v01.md and revision_v11\\recount\\RECOUNT_BRIEF_v01.md only.
Imports the second-program library revision_v11\\recount\\rc_lib_v01.py (loader of the 35 evaluation runs, selection, per-run
statistics, batched step frontier, percentile helper). The evaluation for an arbitrary list of arms (evaluate_g) is written here.
Nothing of revision_v11\\analysis is opened except the two array folders the brief names as inputs (analysis\\out\\ck here).

Conventions (as in the brief):
  arms        index 0 is always F0 (class average) and index 1 always E (oracle); every further arm gets F0's zero-margin
              point prepended; the perfect oracle O (one point) gets it too.
  D           D[..., a] = sum over the 201 levels of F_F0 - F_arm; D[..., 1] = denE; the last column (if O is given) = den0.
"""
import json, pathlib, sys, warnings
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'recount'))
import rc_lib_v01 as L   # noqa: E402

R2_OUT = HERE.parent / 'recount2' / 'out'
CK_DIR = HERE.parent / 'analysis' / 'out' / 'ck'
KEY = 't0p75_a6p0'
NLEV = L.NLEV
NG = L.NG
POPS = ('all', 'moving', 'phase0', 'phase1', 'phase2')
CK_ARMS = tuple('CK%d' % a for a in range(1, 8))


# ------------------------------------------------------------------------------------------------ data
def load_eval_runs():
    """The 35 evaluation runs through rc_lib_v01.load_run, plus: the stored-decision count, the clearances judged until the
    stop ends (recount2, tau 0.75 s, 6 m/s2) and the critical scales cCK1..cCK7 of the ck folder (evaluated decisions)."""
    ds = L.load_all()
    for d in ds:
        run = d['run']
        with np.load(R2_OUT / (run + '.npz'), allow_pickle=False) as z:
            if not np.array_equal(z['k'], d['k_all']):
                raise RuntimeError('%s: k of recount2 differs from the stored k' % run)
            if not np.array_equal(z['evaluated'].astype(bool), d['ev_all']):
                raise RuntimeError('%s: evaluated flags of recount2 differ' % run)
            cx = np.asarray(z['clearX_' + KEY], float)[d['ev_all']]
            c61 = np.asarray(z['clear61_' + KEY], float)[d['ev_all']]
        d['clearX_nan_eval'] = int(np.isnan(cx).sum())
        d['clearX'] = cx                                   # NaN stays NaN: (NaN > G) is False = unsafe
        d['clear61'] = c61
        with np.load(CK_DIR / (run + '.npz'), allow_pickle=False) as z:
            if not np.array_equal(z['k'], d['k_all']):
                raise RuntimeError('%s: k of the ck folder differs from the stored k' % run)
            d['ck'] = {}
            d['ck_nan_eval'] = {}
            for a in range(1, 8):
                c = np.asarray(z['cCK%d' % a], float)[d['ev_all']]
                d['ck_nan_eval']['CK%d' % a] = int(np.isnan(c).sum())
                d['ck']['CK%d' % a] = c
    return ds


def select_at(C, idx55, g):
    """(n,): first row (index order) whose critical scale is >= g, else the fallback row. NaN scales are never >= g."""
    feas = C >= g
    return np.where(feas.any(1), feas.argmax(1), idx55)


def dec_stats(d, sel, safe_w, safe_c):
    """Per decision and scale, for the selection sel (G, n): wrong go (bool), caution term, caution count (bool).
    Wrong go: the selected row is not safe under the scoring (safe_w). Caution term: (vbar[first truly safe row] -
    vbar[selected row]) / desired, counted when the selected row is truly safe (safe_c)."""
    n = d['n']; ar = np.arange(n)
    bad = ~safe_w[ar[None, :], sel]
    first = safe_c.argmax(1)
    ok = safe_c[ar[None, :], sel]
    diff = (d['vbar'][ar, first][None, :] - d['vbar'][ar[None, :], sel]) / d['des'][None, :]
    return bad, np.where(ok, diff, 0.), ok


def sums(bad, term, cnt, masks):
    """(P, G, 3): wrong-go count, caution sum, caution count per population mask."""
    out = np.zeros((len(masks), bad.shape[0], 3))
    for mi, m in enumerate(masks):
        out[mi, :, 0] = bad[:, m].sum(1); out[mi, :, 1] = term[:, m].sum(1); out[mi, :, 2] = cnt[:, m].sum(1)
    return out


def run_vector(d, arm_sels, masks, safe_w, safe_c, with_oracle=True):
    """One run's statistics, flat: [n per mask (P) | arms (P, A, G, 3) | oracle (P, 3)]. arm_sels: list of (G, n) selections."""
    Pm = len(masks)
    nm = np.array([float(m.sum()) for m in masks])
    S = np.zeros((Pm, len(arm_sels), NG, 3))
    for ai, sel in enumerate(arm_sels):
        S[:, ai] = sums(*dec_stats(d, sel, safe_w, safe_c), masks)
    parts = [nm, S.ravel()]
    if with_oracle:
        selO = np.where(safe_w.any(1), safe_w.argmax(1), d['idx55'])[None, :]
        parts.append(sums(*dec_stats(d, selO, safe_w, safe_c), masks)[:, 0, :].ravel())
    return np.concatenate(parts)


def split(agg, Pm, A, with_oracle=True):
    agg = np.atleast_2d(agg)
    B = agg.shape[0]
    n = agg[:, :Pm]
    S = agg[:, Pm:Pm + Pm * A * NG * 3].reshape(B, Pm, A, NG, 3)
    O = agg[:, Pm + Pm * A * NG * 3:].reshape(B, Pm, 3) if with_oracle else None
    return n, S, O


# ------------------------------------------------------------------------------------------------ evaluation
def evaluate_g(n, S, O=None, want=False):
    """n (B, P); S (B, P, A, G, 3); O (B, P, 3) or None.
    Returns D (B, P, A [+1]) and info: c0, w0 (F0's zero-margin point), hi (last level), nanlev (B, P) = True where the
    frontier of F0 or E is undefined at some level; with want=True also C, W (B, P, A, G) and cO, wO."""
    B, Pm, A = S.shape[:3]
    D = np.full((B, Pm, A + (0 if O is None else 1)), np.nan)
    info = dict(c0=np.full((B, Pm), np.nan), w0=np.full((B, Pm), np.nan), hi=np.full((B, Pm), np.nan), nanlev=np.zeros((B, Pm), bool))
    if want:
        info['C'] = np.full((B, Pm, A, NG), np.nan); info['W'] = np.full((B, Pm, A, NG), np.nan)
        info['cO'] = np.full((B, Pm), np.nan); info['wO'] = np.full((B, Pm), np.nan)
    with np.errstate(invalid='ignore', divide='ignore'), warnings.catch_warnings():
        warnings.simplefilter('ignore', RuntimeWarning)
        for p in range(Pm):
            npop = n[:, p]
            W = 100. * S[:, p, :, :, 0] / npop[:, None, None]                 # wrong go %, over the population's decisions
            C = 100. * S[:, p, :, :, 1] / S[:, p, :, :, 2]                    # caution %, over truly safe selections
            c0 = C[:, 0, 0]; w0 = W[:, 0, 0]
            hi = np.minimum(np.nanmax(C[:, 0], axis=1), np.nanmax(C[:, 1], axis=1))
            lev = L.linspace_rows(c0, hi)
            fF = L.step_frontier(C[:, 0], W[:, 0], lev)
            fE = L.step_frontier(C[:, 1], W[:, 1], lev)
            D[:, p, 0] = 0.
            D[:, p, 1] = np.sum(fF - fE, axis=1)
            for ai in range(2, A):
                fA = L.step_frontier(np.concatenate([c0[:, None], C[:, ai]], 1), np.concatenate([w0[:, None], W[:, ai]], 1), lev)
                D[:, p, ai] = np.sum(fF - fA, axis=1)
            if O is not None:
                cO = 100. * O[:, p, 1] / O[:, p, 2]; wO = 100. * O[:, p, 0] / npop
                fO = L.step_frontier(np.stack([c0, cO], 1), np.stack([w0, wO], 1), lev)
                D[:, p, A] = np.sum(fF - fO, axis=1)
                if want:
                    info['cO'][:, p] = cO; info['wO'][:, p] = wO
            info['c0'][:, p] = c0; info['w0'][:, p] = w0; info['hi'][:, p] = hi
            info['nanlev'][:, p] = np.isnan(fF).any(1) | np.isnan(fE).any(1)
            if want:
                info['C'][:, p] = C; info['W'][:, p] = W
    return D, info


def boot_g(M, idx, Pm, A, with_oracle=True, chunk=400, logfile=None, tag=''):
    """Evaluate every resample; idx (B, m) run indices into the rows of M (any m)."""
    import time
    B = idx.shape[0]
    n = np.zeros((B, Pm)); D = np.full((B, Pm, A + (1 if with_oracle else 0)), np.nan); nl = np.zeros((B, Pm), bool)
    t0 = time.time()
    for s in range(0, B, chunk):
        cnt = L.counts_from_idx(idx[s:s + chunk], M.shape[0])
        nn, S, O = split(cnt @ M, Pm, A, with_oracle)
        n[s:s + chunk] = nn
        D[s:s + chunk], info = evaluate_g(nn, S, O)
        nl[s:s + chunk] = info['nanlev']
        if logfile is not None and ((s // chunk) % 10 == 0 or s + chunk >= B):
            L.log('  %s %d / %d, %.0f s' % (tag, min(s + chunk, B), B, time.time() - t0), file=logfile)
    return n, D, nl


def weighted(n, D, cols=(2, 3, 4)):
    """Phase-weighted aggregate: sum over phases 0-2 of (n_p / n) D_p, n = n_0 + n_1 + n_2 (an empty phase contributes 0).
    n (B, P), D (B, P, X) -> ntot (B,), Dw (B, X)."""
    cols = list(cols)
    nn = n[:, cols]; ntot = nn.sum(1)
    Dp = np.where(nn[:, :, None] > 0, D[:, cols, :], 0.)
    with np.errstate(invalid='ignore', divide='ignore'):
        Dw = np.sum((nn / ntot[:, None])[:, :, None] * Dp, axis=1)
    Dw[ntot <= 0] = np.nan
    return ntot, Dw


def ci_ratio(num, den):
    """95% percentile interval of num / den over the resamples with a positive denominator (and a finite ratio).
    Returns [lo, hi], number of resamples left out."""
    num = np.asarray(num, float); den = np.asarray(den, float)
    with np.errstate(invalid='ignore', divide='ignore'):
        r = num / den
    keep = np.isfinite(den) & (den > 0) & np.isfinite(r)
    return L.pct(r[keep]), int((~keep).sum())


def ci_plain(v):
    v = np.asarray(v, float)
    return L.pct(v), int((~np.isfinite(v)).sum())
