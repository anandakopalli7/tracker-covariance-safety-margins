"""Independent recount v12 (second program): shared helpers. Written by the recount agent, 19 Nov 2026.
Does NOT read or import any a9_*.py file. Imports only rev_common_v01 (v11; loader of record) and optA_lib_v02 (library of
record) and numpy. Read-only on every project file.
"""
import sys, json, pathlib
import numpy as np

V11 = pathlib.Path(r'ARS_TRIAL\revision_v11\analysis')
V12 = pathlib.Path(r'ARS_TRIAL\revision_v12')
OUTA = V12 / 'analysis' / 'out'
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(V11))
import rev_common_v01 as C            # noqa: E402
L = C.L
GRID = C.GRID
NLEV = L.NLEV
POPNAMES = ['all', 'moving', 'phase0', 'phase1', 'phase2']   # r['masks'] indices 0..4


# ------------------------------------------------------------------ per-row contributions (my own; W1 caution axis)
def contrib(r, safe_x=None):
    """Per (decision, row) contributions to the five summed statistics, given the scoring's safe set (default W1).
    Returns dict wg (wrong go under the scoring, int), ct (caution term, float), cc (caution count, int), c4 (col 4, int)."""
    clear1 = r['clear1']
    s1 = clear1 > 0.
    n = s1.shape[0]
    ar = np.arange(n)
    orc = s1.argmax(axis=1)
    vorc = r['vbar'][ar, orc]
    with np.errstate(invalid='ignore'):
        ct = np.where(s1, (vorc[:, None] - r['vbar']) / r['desired'], 0.)
    sx = s1 if safe_x is None else safe_x
    anyx = sx.any(axis=1)
    wg = (~sx).astype(np.int64)
    return dict(wg=wg, ct=ct, cc=s1.astype(np.int64), c4=(anyx[:, None] & ~sx).astype(np.int64), s1=s1, sx=sx)


def first_feasible(Cm, g, idx55, strict=False):
    """Selected row: first row with C >= g (C > g if strict), else idx55. g scalar or per-decision vector."""
    g = np.asarray(g, float)
    if g.ndim == 0:
        g = np.full(Cm.shape[0], float(g))
    with np.errstate(invalid='ignore'):
        feas = (Cm > g[:, None]) if strict else (Cm >= g[:, None])
    return np.where(feas.any(axis=1), feas.argmax(axis=1), idx55)


def point_stats(cb, sel, masks):
    """Statistics (len(masks), 5) of one selection vector."""
    ar = np.arange(sel.size)
    out = np.empty((len(masks), 5))
    w = cb['wg'][ar, sel]; s = cb['ct'][ar, sel]; k = cb['cc'][ar, sel]; c4 = cb['c4'][ar, sel]
    for mi, m in enumerate(masks):
        out[mi] = [m.sum(), w[m].sum(), s[m].sum(), k[m].sum(), c4[m].sum()]
    return out


def grid_tables(runs, cname, cbs, masks_key='masks', crit_override=None):
    """(n_runs, 202, n_pop, 5) of a source on the grid, via the library of record (select_grid + stats_scored)."""
    per = []
    for r, cb in zip(runs, cbs):
        Cm = r['crit'][cname] if crit_override is None else crit_override(r)
        sel = L.select_grid(Cm, GRID, r['idx55'])
        per.append(L.stats_scored(sel, r['clear1'], cb['sx'], r['vbar'], r['desired'], r[masks_key]))
    return np.stack(per)


def my_grid_tables(runs, Cfun, cbs, masks_key='masks'):
    """Same as grid_tables, with my own selection and sums (cross-check)."""
    per = []
    for r, cb in zip(runs, cbs):
        Cm = Cfun(r)
        out = np.empty((GRID.size, len(r[masks_key]), 5))
        for gi, g in enumerate(GRID):
            out[gi] = point_stats(cb, first_feasible(Cm, g, r['idx55']), r[masks_key])
        per.append(out)
    return np.stack(per)


# ------------------------------------------------------------------ frontier helpers (my own)
def step_front(c, w, lev):
    """Lowest w among points with c <= level, NaN where none (binning formulation)."""
    c = np.asarray(c, float); w = np.asarray(w, float)
    ok = np.isfinite(c) & np.isfinite(w)
    c = c[ok]; w = w[ok]
    pos = np.searchsorted(lev, c, side='left')
    best = np.full(lev.size + 1, np.inf)
    np.minimum.at(best, pos, w)
    best = np.minimum.accumulate(best[:-1])
    return np.where(np.isfinite(best), best, np.nan)


def front_choice(c, w, lev):
    """Per level: index of the point attaining the step frontier: among points with c <= level, lowest w, then lowest c,
    then lowest index. -1 where no point qualifies."""
    c = np.asarray(c, float); w = np.asarray(w, float)
    idx = np.arange(c.size)
    ok = np.isfinite(c) & np.isfinite(w)
    out = np.full(lev.size, -1, np.int64)
    for li, lv in enumerate(lev):
        q = ok & (c <= lv)
        if not q.any():
            continue
        cand = idx[q]
        o = np.lexsort((cand, c[cand], w[cand]))
        out[li] = cand[o[0]]
    return out


def rates_of(T):
    """T (..., 5) -> (caution %, wrong go %)."""
    with np.errstate(divide='ignore', invalid='ignore'):
        return 100. * T[..., 2] / T[..., 3], 100. * T[..., 1] / T[..., 0]


def curves(Tpop):
    """Points per source of one population, with F0's g = 0 point prepended for every source except F0 and E."""
    cur = {a: rates_of(T) for a, T in Tpop.items()}
    c0, w0 = cur['F0'][0][0], cur['F0'][1][0]
    out = {}
    for a, (c, w) in cur.items():
        if a in ('F0', 'E'):
            out[a] = (c, w)
        else:
            out[a] = (np.concatenate([[c0], c]), np.concatenate([[w0], w]))
    return out


def levels(cur):
    cF0 = cur['F0'][0]; cE = cur['E'][0]
    return np.linspace(cF0[0], min(np.nanmax(cF0), np.nanmax(cE)), NLEV)


def my_eval(Tpop, names):
    """My own step-frontier evaluation (cross-check of L.eval_scoring)."""
    cur = curves(Tpop)
    lev = levels(cur)
    fF0 = step_front(*cur['F0'], lev); fE = step_front(*cur['E'], lev)
    return dict(denE=float(np.sum(fF0 - fE)), n=float(Tpop['F0'][0, 0]), lev=lev,
                D={a: float(np.sum(fF0 - step_front(*cur[a], lev))) for a in names})


# ------------------------------------------------------------------ gridless operating points (my own event algorithm)
def gridless_table(runs, Cfun, cbs, masks_key='masks', gmax=1000.):
    """All distinct operating points of a source over margin scales g in [0, gmax], pooled over runs.
    The selected row of decision i at scale g is the first row with C >= g. It changes only when g passes just above a
    critical value c in [0, gmax): from then on the rows with C == c are infeasible. Per decision, the thresholds are walked
    in increasing order and an event (c, delta of the five statistics per population) is emitted where the selection
    changes. The pooled point at a scale just above threshold c is the g = 0 point plus the cumulative deltas of every
    event with threshold <= c. Returns T (G, n_pop, 5) (row 0 = g = 0) and the threshold of each later row."""
    npop = len(runs[0][masks_key])
    base = np.zeros((npop, 5))
    baseS = [0] * npop                                       # exact caution sums (integers in units of 2**-SC)
    thr_all = []; d_all = []; dS_all = []
    for r, cb in zip(runs, cbs):
        Cm = np.asarray(Cfun(r), float)
        n = Cm.shape[0]
        ar = np.arange(n)
        M = np.stack(r[masks_key]).astype(np.int64)            # (npop, n)
        cur = first_feasible(Cm, 0., r['idx55'])
        base += point_stats(cb, cur, r[masks_key])
        sv = exact_ints(cb['ct'][ar, cur])
        for mi in range(npop):
            baseS[mi] += sum(v for v, mm in zip(sv, M[mi]) if mm)
        srt = np.sort(np.where(np.isnan(Cm), np.inf, Cm), axis=1)
        for t in range(17):
            c = srt[:, t]
            act = np.isfinite(c) & (c >= 0.) & (c < gmax)
            if t > 0:
                act &= c != srt[:, t - 1]
            if not act.any():
                continue
            ii = np.nonzero(act)[0]
            new = first_feasible(Cm[ii], c[ii], r['idx55'][ii], strict=True)
            old = cur[ii]
            ch = new != old
            if ch.any():
                i2 = ii[ch]; o2 = old[ch]; n2 = new[ch]
                d = np.zeros((i2.size, npop, 5))
                for k, key in ((1, 'wg'), (3, 'cc'), (4, 'c4')):
                    dv = cb[key][i2, n2] - cb[key][i2, o2]
                    d[:, :, k] = M[:, i2].T * dv[:, None]
                dS = np.array([a - b for a, b in zip(exact_ints(cb['ct'][i2, n2]), exact_ints(cb['ct'][i2, o2]))],
                              dtype=object)
                dSp = np.empty((i2.size, npop), dtype=object)
                for mi in range(npop):
                    dSp[:, mi] = np.where(M[mi, i2] > 0, dS, 0)
                thr_all.append(c[i2]); d_all.append(d); dS_all.append(dSp)
            cur[ii] = new
    thr = np.concatenate(thr_all); d = np.concatenate(d_all); dS = np.concatenate(dS_all)
    o = np.argsort(thr, kind='stable')
    thr = thr[o]; d = d[o]; dS = dS[o]
    cs = np.cumsum(d, axis=0)                                # integer-valued floats: exact
    csS = np.cumsum(dS, axis=0)                              # Python integers: exact
    last = np.concatenate([thr[1:] != thr[:-1], [True]])
    pts = base[None] + cs[last]
    pts[:, :, 0] = base[None, :, 0]
    T = np.concatenate([base[None], pts], axis=0)
    Sx = np.empty((T.shape[0], npop), dtype=object)
    Sx[0] = baseS
    Sx[1:] = csS[last] + np.array(baseS, dtype=object)[None, :]
    T[:, :, 2] = np.vectorize(lambda v: v / SC2, otypes=[float])(Sx)   # correctly rounded
    return T, thr[last]


SC2 = 2 ** 1100


def exact_ints(x):
    """Floats -> exact integers in units of 2**-1100 (every finite float64 is an integer multiple of 2**-1074)."""
    out = []
    for v in np.asarray(x, float).ravel().tolist():
        num, den = v.as_integer_ratio()
        out.append(num * (SC2 // den))
    return out


def gridless_at(T, thr, g):
    """Point of the gridless table at scale g (for the identity check against the grid)."""
    j = np.searchsorted(thr, g, side='left')          # number of thresholds < g
    return T[j]


# ------------------------------------------------------------------ misc
def jdump(obj):
    return json.dumps(obj, indent=1, default=float, allow_nan=True)
