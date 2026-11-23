"""Revision v12 (ARS review of draft v11): shared helpers for the analyses of AMENDMENT_09. New file, 19 Nov 2026.
Read-only on every project file and on revision_v11; writes nothing itself.

Reuses revision_v11/analysis/rev_common_v01.py (imported unchanged; its loader passed the identity check of record for v11) and,
through it, the scoring library of record optA_lib_v02.py. New here:
  * gridless curves: a source's operating points at every margin scale in [0, GMAX] at which some decision's selected row
    changes (A9-1(c)); returned as (n_points, NST) tables that optA_lib_v02.eval_scoring accepts unchanged;
  * frontier_argmin: the step frontier of record with the index of the point that attains it (A9-3, A9-4);
  * a placebo source (A9-1(a)) and offset sources (A9-1(b)).
"""
import json, pathlib, sys
import numpy as np

V11 = pathlib.Path(r'ARS_TRIAL\revision_v11\analysis')
sys.path.insert(0, str(V11))
import rev_common_v01 as C                   # noqa: E402
L = C.L
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'out'
OUT.mkdir(exist_ok=True)

RATIO = 1.1029                  # median margin ratio of record (Table V; rev_c_ratio_tracks_v01)
GMAX = 1e3                      # the largest swept scale
GSTEP = 10. ** 0.025            # one grid step (201 log-spaced values over 5 decades)


def add_placebo(runs, name='P', factor=RATIO ** 2):
    """Critical scales of F0 divided by factor: at scale g the source selects as F0 does at g * factor."""
    for r in runs:
        r['crit'][name] = r['crit']['F0'] / factor
        r['sel'].pop(name, None)


# ------------------------------------------------------------------------------------------------ gridless curves
def row_stats(r, safe_x, masks):
    """Per decision, per row, per population: the 5 statistics of stats_scored for that row selected
    (columns: decisions, wrong go, caution sum, caution count, wrong go with a scoring-safe row). (n, 17, npop, 5)."""
    clear1 = r['clear1']; vbar = r['vbar']; des = r['desired']
    n = clear1.shape[0]; ar = np.arange(n)
    safe = clear1 > 0.
    orc = safe.argmax(axis=1)
    ct = np.where(safe, (vbar[ar, orc][:, None] - vbar) / des, 0.)
    anysX = safe_x.any(axis=1)
    out = np.zeros((n, 17, len(masks), L.NST))
    for mi, m in enumerate(masks):
        mm = m[:, None].astype(float)
        out[:, :, mi, 0] = mm
        out[:, :, mi, 1] = (~safe_x) * mm
        out[:, :, mi, 2] = ct * mm
        out[:, :, mi, 3] = safe * mm
        out[:, :, mi, 4] = (anysX[:, None] & ~safe_x) * mm
    return out


def sel_path(c, idx55, gmax=GMAX):
    """One decision's selected rows as g rises from 0 to gmax: (row at g = 0, [(breakpoint b, row selected just above b)])."""
    recs = []; m = -np.inf
    for j in range(17):
        v = c[j]
        if np.isnan(v):
            continue
        if v > m:
            recs.append((v, j)); m = v
    t0 = next((t for t, (v, _) in enumerate(recs) if v >= 0.), None)
    if t0 is None:
        return int(idx55), []
    s0 = recs[t0][1]; ev = []
    for t in range(t0, len(recs)):
        b = recs[t][0]
        if not (b < gmax):
            break
        nxt = recs[t + 1][1] if t + 1 < len(recs) else int(idx55)
        ev.append((float(b), int(nxt)))
    return int(s0), ev


def run_events(r, crit, safe_x, masks, gmax=GMAX):
    """Per run: initial totals (npop, NST) at g = 0 and the events (b, delta (npop, NST)) of one source."""
    RS = row_stats(r, safe_x, masks)
    T0 = np.zeros((len(masks), L.NST)); bs = []; ds = []
    for i in range(crit.shape[0]):
        s0, ev = sel_path(crit[i], r['idx55'][i], gmax)
        T0 += RS[i, s0]
        cur = s0
        for b, nxt in ev:
            if nxt != cur:
                bs.append(b); ds.append(RS[i, nxt] - RS[i, cur])
            cur = nxt
    if bs:
        return T0, np.array(bs), np.stack(ds)
    return T0, np.zeros(0), np.zeros((0, len(masks), L.NST))


class Gridless:
    """Events of one source over all runs, sorted once; curve(weights) -> (n_points, npop, NST) tables."""

    def __init__(self, per_run):
        self.T0 = np.stack([p[0] for p in per_run])                         # (nrun, npop, NST)
        b = np.concatenate([p[1] for p in per_run]); d = np.concatenate([p[2] for p in per_run])
        ri = np.concatenate([np.full(p[1].size, k) for k, p in enumerate(per_run)])
        o = np.argsort(b, kind='stable')
        self.b = b[o]; self.d = d[o]; self.ri = ri[o]
        last = np.concatenate([self.b[1:] != self.b[:-1], [True]]) if self.b.size else np.zeros(0, bool)
        self.keep = np.nonzero(last)[0]                                      # last event of each distinct breakpoint

    def curve(self, w=None, pops=None):
        """w: run weights (nrun,) or None (all 1); pops: population indices to keep (default all).
        Returns (1 + n_breakpoints, npop, NST)."""
        if w is None:
            w = np.ones(self.T0.shape[0])
        T0a = self.T0 if pops is None else self.T0[:, pops, :]
        da = self.d if pops is None else self.d[:, pops, :]
        T0 = np.tensordot(w, T0a, axes=(0, 0))
        if self.b.size == 0:
            return T0[None]
        cs = np.cumsum(da * w[self.ri][:, None, None], axis=0)[self.keep] + T0[None]
        return np.concatenate([T0[None], cs], axis=0)

    def curves(self, W):
        """W (B, nrun) -> list of (1 + nb, npop, NST)."""
        return [self.curve(W[b]) for b in range(W.shape[0])]


def gridless_sources(runs, names, safe_fn, masks_key='masks', gmax=GMAX):
    out = {}
    for a in names:
        per = []
        for r in runs:
            sx = safe_fn(r)
            if a == 'O':
                sel = L.select_first_safe(sx, r['idx55'])[0]
                RS = row_stats(r, sx, r[masks_key])
                T0 = RS[np.arange(sel.size), sel].sum(axis=0)
                per.append((T0, np.zeros(0), np.zeros((0, len(r[masks_key]), L.NST))))
            else:
                per.append(run_events(r, r['crit'][a], sx, r[masks_key], gmax))
        out[a] = Gridless(per)
    return out


# ------------------------------------------------------------------------------------------------ frontier with argmin
def frontier_argmin(c, w, levels):
    """optA_lib_v02.frontier (lowest w among points with caution <= level) and, per level, the index of the point attaining it
    (the first in caution order among equal minima). -1 where no point qualifies."""
    ok = np.isfinite(c) & np.isfinite(w)
    idx_ok = np.nonzero(ok)[0]
    if idx_ok.size == 0:
        return np.full(len(levels), np.nan), np.full(len(levels), -1)
    o = np.argsort(c[ok], kind='stable'); cs = c[ok][o]; ws = w[ok][o]; src = idx_ok[o]
    best = np.empty(ws.size); arg = np.empty(ws.size, int)
    bv = np.inf; ba = -1
    for k in range(ws.size):
        if ws[k] < bv:
            bv = ws[k]; ba = src[k]
        best[k] = bv; arg[k] = ba
    j = np.searchsorted(cs, levels, side='right') - 1
    f = np.where(j >= 0, best[np.clip(j, 0, None)], np.nan)
    a = np.where(j >= 0, arg[np.clip(j, 0, None)], -1)
    return f, a


def jdump(obj):
    return json.dumps(obj, indent=1, default=float, allow_nan=True)


def write_out(path, doc):
    path = pathlib.Path(path)
    if path.exists():
        raise SystemExit('REFUSED: %s exists' % path)
    path.write_text(jdump(doc), encoding='utf-8')
