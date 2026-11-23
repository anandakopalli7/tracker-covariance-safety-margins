"""Option A, main program (A5 engineer lineage): scoring and statistics library, v02. New file, 18 Nov 2026.
v02 = optA_lib_v01.py (unchanged, kept) with ONE change, required by 11_ojits\\BRIEF_OPTION_A_v02_CLARIFICATIONS_01.md point 7:
  in branch_rr0, the v01 l. 52-57 sentences say "of the class-average margin's avoidable wrong-go under this scoring" where v01 said
  "of the remaining room" (branches 2 and 4; review B1 Fix: RR0 is never called a share of a room). Numbers are unaffected.
Specification: 11_ojits\\BRIEF_OPTION_A_v02.md with the replacement texts it adopts verbatim from
11_ojits\\review\\REVIEW_BRIEF_OPTION_A_v01.md (B1-B4 Fix, M1, M3, M5, M6, M7, M8, m2-m7, m10, m11), and Clarifications 01.

No oxsb_* module is imported. Every function below that is not marked "new" is a COPY (same expressions) of the named function:
  clean_clear, select_grid, rates, frontier, levels_of, boot_counts
      <- 09_redesign\\m2_decisions\\openloop\\ox12_score_v01.py (same names)
  stats_scored(sel, clear1, safe_x, ...)
      <- ox12_score_v01.stats_grid (W1: safe_x = clear1 > 0) and 11_ojits\\A5\\code\\oxsb_replan_v03.py stats_R (W_R: safe_x =
         clearR > gap), written as one function: caution (columns 2, 3) from the W1 clearance (oracle row = first W1-safe row,
         true-safe set = W1 clear > 0), wrong go (columns 1, 4) from the scoring's safe set (column 4 = anysX & not selected-safe).
         signed=True is new (review M5 sensitivity).
  curves_w (+ the 'repl' option, new: review m2's CK3 sensitivity), hull_frontier, rr_hull
      <- 09_redesign\\m2_decisions\\openloop\\oxsb_analyse_v05.py (same names)
  brake_profile, vkey, j_of
      <- 11_ojits\\A5\\code\\oxsb_replan_v03.py (same names; A as a parameter)
  sha256_file, write_once, json_dump, clock, root_rel
      <- 11_ojits\\A4\\code\\oxsb_core_v03.py (same names)
New: select_first_safe (the perfect oracle O_X, review B1), eval_scoring (step and hull frontier quantities of one population),
  summ (percentile / basic intervals), branch_rr0 (v01 l. 52-57 with review M1), weighted-rank Spearman for the run bootstrap
  (review M6: each run's decisions repeated by its count, ranks recomputed with average ties; computed exactly with weights).
Imports: numpy and the standard library only.
"""
import hashlib, json, math, pathlib, time
import numpy as np

NLEV = 201
NST = 5      # decisions, wrong go (selected unsafe under the scoring), caution sum, caution count, wrong go if a scoring-safe row exists
H = 0.05
JERK = 12.65
MAX_INVALID = 0.025
MIN_DEC_EQ = 10.0          # review M1 resolution rule (JUDGEMENT, resolution-based)


# ------------------------------------------------------------------------------------------------ ox12_score_v01 copies
def clean_clear(clear):
    """ox12_score_v01.clean_clear: NaN clearance (only outside the evaluated set) -> -1."""
    return np.where(np.isfinite(clear) | (clear == np.inf), clear, -1.)


def select_grid(C, grid, idx55):
    """ox12_score_v01.select_grid: C (n, 17) critical values -> selected row (len(grid), n)."""
    feas = C[None, :, :] >= np.asarray(grid, float)[:, None, None]
    anyf = feas.any(axis=2)
    return np.where(anyf, feas.argmax(axis=2), idx55[None, :])


def select_first_safe(safe_x, idx55):
    """New (review B1): the perfect oracle O_X selects the first X-safe row in cost order, or the fallback row idx55 if there is
    none. One selection per decision, independent of the knob: returned as (1, n)."""
    anyf = safe_x.any(axis=1)
    return np.where(anyf, safe_x.argmax(axis=1), idx55)[None, :]


def stats_scored(sel, clear1, safe_x, vbar, des, masks, signed=False):
    """sel (G, n) -> (G, len(masks), NST) summed statistics of one run.
    Caution axis (review M5, verbatim from oxsb_replan_v03.stats_R): oracle row and true-safe set by W1 (clear > 0); wrong go by
    the scoring X (safe_x), column 4 with anysX. With safe_x = clear1 > 0 this is ox12_score_v01.stats_grid exactly.
    signed=True (new; review M5 sensitivity): caution averaged over every decision that has a W1-safe row, each counted at its own
    signed speed difference to the W1 oracle row (column 2 = sum of the signed differences, column 3 = number of such decisions)."""
    G, n = sel.shape; ar = np.arange(n)
    safe = clear1 > 0.
    anys1 = safe.any(axis=1)
    orc = safe.argmax(axis=1)
    ssel = safe[ar[None, :], sel]
    if signed:
        ct = np.where(anys1[None, :], (vbar[ar, orc][None, :] - vbar[ar[None, :], sel]) / des, 0.)
        cnt = np.broadcast_to(anys1[None, :], (G, n))
    else:
        ct = np.where(ssel, (vbar[ar, orc][None, :] - vbar[ar[None, :], sel]) / des, 0.)
        cnt = ssel
    anysX = safe_x.any(axis=1)
    sselX = safe_x[ar[None, :], sel]
    out = np.empty((G, len(masks), NST))
    for mi, m in enumerate(masks):
        out[:, mi, 0] = m.sum(); out[:, mi, 1] = (~sselX & m).sum(axis=1); out[:, mi, 2] = (ct * m).sum(axis=1)
        out[:, mi, 3] = (cnt & m).sum(axis=1); out[:, mi, 4] = (anysX[None, :] & ~sselX & m).sum(axis=1)
    return out


def rates(T):
    """ox12_score_v01.rates: (..., NST) -> wrong go %, caution %, wrong go if a safe row exists %."""
    with np.errstate(divide='ignore', invalid='ignore'):
        return 100. * T[..., 1] / T[..., 0], 100. * T[..., 2] / T[..., 3], 100. * T[..., 4] / T[..., 0]


def frontier(c, w, levels):
    """ox12_score_v01.frontier: lowest w among points with caution <= level; NaN where no point qualifies."""
    ok = np.isfinite(c) & np.isfinite(w)
    if not ok.any():
        return np.full(len(levels), np.nan)
    o = np.argsort(c[ok], kind='stable'); cs = c[ok][o]; ws = np.minimum.accumulate(w[ok][o])
    idx = np.searchsorted(cs, levels, side='right') - 1
    return np.where(idx >= 0, ws[np.clip(idx, 0, None)], np.nan)


def levels_of(cF0, cE, c0):
    """ox12_score_v01.levels_of."""
    C = min(np.nanmax(cF0), np.nanmax(cE))
    return np.linspace(c0, C, NLEV)


def boot_counts(n_run, nboot, seed):
    """ox12_score_v01.boot_counts = review M1's draw: default_rng(seed).integers(0, n_run, (nboot, n_run)), counts per run."""
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n_run, (nboot, n_run))
    cnt = np.zeros((nboot, n_run))
    for b in range(nboot):
        cnt[b] = np.bincount(idx[b], minlength=n_run)
    return cnt


# ------------------------------------------------------------------------------------------------ oxsb_analyse_v05 copies
def curves_w(Tsum, wi, repl=()):
    """oxsb_analyse_v05.curves_w: every name except F0 and E gets F0's g = 0 point prepended.
    repl (new; review m2's CK3 sensitivity 'repl'): for the names listed, F0's g = 0 point REPLACES the name's own first (g = 0)
    point instead of being placed in front of it."""
    out = {}
    for nm, T in Tsum.items():
        rt = rates(T)
        out[nm] = (rt[1], rt[wi])
    c0, w0 = out['F0'][0][0], out['F0'][1][0]
    for nm in out:
        if nm not in ('F0', 'E'):
            if nm in repl:
                out[nm] = (np.concatenate([[c0], out[nm][0][1:]]), np.concatenate([[w0], out[nm][1][1:]]))
            else:
                out[nm] = (np.concatenate([[c0], out[nm][0]]), np.concatenate([[w0], out[nm][1]]))
    return out


def hull_frontier(c, w, levels):
    """oxsb_analyse_v05.hull_frontier: lower convex envelope of the points (c, w), made non-increasing; NaN below the smallest
    caution."""
    ok = np.isfinite(c) & np.isfinite(w)
    if not ok.any():
        return np.full(len(levels), np.nan)
    cu, inv = np.unique(c[ok], return_inverse=True)
    wu = np.full(cu.size, np.inf); np.minimum.at(wu, inv, w[ok])
    ws = np.minimum.accumulate(wu)
    keep = np.concatenate([[True], ws[1:] < ws[:-1]])
    hx = []; hy = []
    for x, y in zip(cu[keep], ws[keep]):
        while len(hx) >= 2 and (hx[-1] - hx[-2]) * (y - hy[-2]) - (hy[-1] - hy[-2]) * (x - hx[-2]) <= 0:
            hx.pop(); hy.pop()
        hx.append(x); hy.append(y)
    hx = np.array(hx); hy = np.array(hy)
    f = np.interp(levels, hx, hy)
    f = np.where(levels < hx[0], np.nan, f)
    fin = np.isfinite(f)
    if fin.any():
        i0 = int(np.argmax(fin))
        f[i0:] = np.minimum.accumulate(f[i0:])
    return f


def eval_scoring(Tpop, names, hull_names=(), repl=()):
    """New. Tpop: arm -> (G, NST) of one population (F0 and E required). Step frontier (primary; ox12_score_v01.rr_point's levels
    and sums) and, for hull_names, the convex hull (oxsb_analyse_v05.rr_hull's levels and sums):
      denE = sum over the 201 levels of (F0 - E);  D[a] = sum of (F0 - a) for every a in names (O included when given: den0 = D['O']).
    Levels: 201 equally spaced from F0's g = 0 caution to min(F0's, E's largest caution) (ox12_score_v01.levels_of).
    Returns dict(denE, D={a: ...}, n=decisions, c0, C, hdenE, hD={...}). RR is formed by the caller as D / den where den > 0."""
    cur = curves_w(Tpop, 0, repl=repl)
    cF0, wF0 = cur['F0']; cE, wE = cur['E']
    c0 = cF0[0]
    lev = levels_of(cF0, cE, c0)
    fF0 = frontier(cF0, wF0, lev); fE = frontier(cE, wE, lev)
    out = dict(denE=float(np.sum(fF0 - fE)), D={}, n=float(Tpop['F0'][0, 0]), c0=float(c0), C=float(lev[-1]))
    for a in names:
        out['D'][a] = float(np.sum(fF0 - frontier(cur[a][0], cur[a][1], lev)))
    if hull_names:
        hF0 = hull_frontier(cF0, wF0, lev); hE = hull_frontier(cE, wE, lev)
        out['hdenE'] = float(np.sum(hF0 - hE))
        out['hD'] = {a: float(np.sum(hF0 - hull_frontier(cur[a][0], cur[a][1], lev))) for a in hull_names}
    return out


def oracle_frontier_diag(Tpop, repl=()):
    """New diagnostic (point only): the perfect oracle O's step frontier on the 201 levels (min, max) and the wrong-go share of
    decisions without any scoring-safe row (O's unavoidable wrong go), in percentage points. Review B1: under W_R at 6 m/s^2 O's
    frontier is expected to be that constant at every level (zero avoidable wrong go)."""
    cur = curves_w(Tpop, 0, repl=repl)
    cF0 = cur['F0'][0]; cE = cur['E'][0]
    lev = levels_of(cF0, cE, cF0[0])
    fO = frontier(cur['O'][0], cur['O'][1], lev)
    T = Tpop['O'][0]
    with np.errstate(divide='ignore', invalid='ignore'):
        no_safe = 100. * (T[1] - T[4]) / T[0]
        cO = 100. * T[2] / T[3]
    return dict(O_front_min=float(np.nanmin(fO)) if np.isfinite(fO).any() else float('nan'),
                O_front_max=float(np.nanmax(fO)) if np.isfinite(fO).any() else float('nan'),
                O_front_n_nan=int((~np.isfinite(fO)).sum()), no_safe_row_wrong_go_pp=float(no_safe), O_caution_pp=float(cO),
                F0_g0_caution_pp=float(cF0[0]))


def ratio(D, den):
    """D / den where den is finite and > 0 (the A4 / A5 convention), else NaN."""
    return float(D / den) if (np.isfinite(den) and den > 0) else float('nan')


# ------------------------------------------------------------------------------------------------ A5 copies (oxsb_replan_v03)
def vkey(tau, A):
    return 't%s_a%s' % (('%.2f' % tau).replace('.', 'p'), ('%.1f' % A).replace('.', 'p'))


def j_of(tau):
    j = int(round(tau / H))
    if abs(j * H - tau) > 1e-9 or j < 1:
        raise RuntimeError('tau %r is not a positive multiple of %g s' % (tau, H))
    return j


def brake_profile(v0, a0, A, hold=False):
    """oxsb_replan_v03.brake_profile (= oxsb_replan_v02.brake_profile with A_MAX = A; same expressions)."""
    J = JERK
    if hold and a0 < -A:
        sJ = 0.; tau1 = 0.; aB = a0
    else:
        sJ = -J if a0 > -A else J
        tau1 = abs(a0 + A) / J
        aB = -A
    s1_ = v0 * tau1 + a0 * tau1 ** 2 / 2. + sJ * tau1 ** 3 / 6.
    v1 = v0 + a0 * tau1 + sJ * tau1 ** 2 / 2.
    if v0 <= 0. and a0 <= 0.:
        t_stop = 0.
    else:
        t_root = None
        if sJ < 0:
            t_root = (a0 + math.sqrt(a0 * a0 + 2. * J * v0)) / J
        elif sJ > 0:
            disc = a0 * a0 - 2. * J * v0
            if disc >= 0.:
                t_root = (-a0 - math.sqrt(disc)) / J
        t_stop = t_root if (t_root is not None and t_root <= tau1) else tau1 + v1 / (-aB)
    v_max = v0 + (a0 * a0 / (2. * J) if a0 > 0 else 0.)

    def pos(tau):
        t = min(tau, t_stop)
        if t <= tau1:
            return v0 * t + a0 * t * t / 2. + sJ * t ** 3 / 6.
        dt = t - tau1
        return s1_ + v1 * dt + aB * dt * dt / 2.
    return pos, t_stop, v_max


def tstop_array(v0, a0, tau, A):
    """New wrapper: per (decision, row) the end time of the W_R stop, jr * H + t_stop (oxsb_replan_v03.run_one's tstopR_), from the
    row's speed v0 at j = tau / H and acceleration a0 in the step ending there (the cache's v0_ / a0_ arrays); NaN where v0 is NaN."""
    jr = j_of(tau)
    out = np.full(v0.shape, np.nan)
    for idx in zip(*np.nonzero(np.isfinite(v0) & np.isfinite(a0))):
        out[idx] = jr * H + brake_profile(float(v0[idx]), float(a0[idx]), A)[1]
    return out


def late_of(tstop):
    """oxsb_replan_v03.setting_result: a W_R stop that ends after 3 s (isfinite and > 3.0 + 1e-9)."""
    return np.isfinite(tstop) & (tstop > 3.0 + 1e-9)


# ------------------------------------------------------------------------------------------------ summaries and branches (new)
def pct(b):
    f = np.isfinite(b)
    return [float(x) for x in np.percentile(b[f], [2.5, 97.5])] if f.any() else [float('nan'), float('nan')]


def summ(b, pt):
    """Point, 95% percentile interval over the finite resamples, invalid share (non-finite resamples: den <= 0 or undefined),
    and the basic interval [2 pt - q97.5, 2 pt - q2.5] (printed beside; never decides; review M1)."""
    b = np.asarray(b, float)
    valid = np.isfinite(b)
    s = dict(point=float(pt), ci=pct(b), invalid_share=float(1. - valid.mean()) if b.size else float('nan'),
             n_invalid=int((~valid).sum()))
    s['outside'] = bool(np.isfinite(pt) and np.isfinite(s['ci'][0]) and not (s['ci'][0] <= pt <= s['ci'][1]))
    s['basic'] = [2. * float(pt) - s['ci'][1], 2. * float(pt) - s['ci'][0]]
    return s


def summ_den(b, pt):
    """den: point, share of resamples with den <= 0 (non-finite counted), 95% interval over the finite resamples."""
    b = np.asarray(b, float)
    fin = np.isfinite(b)
    return dict(point=float(pt), share_le0=float(np.mean(~(b > 0))), n_le0=int((~(b > 0)).sum()),
                ci=[float(x) for x in np.percentile(b[fin], [2.5, 97.5])] if fin.any() else [float('nan'), float('nan')])


def dec_eq(D, n):
    """Decision-equivalents of a sum over the 201 levels (review B1 a): D / 201 / 100 * n."""
    return D / NLEV / 100. * n


def branch_rr0(arm, s_rr, den_pt_dec_eq, s_hull):
    """BRIEF_OPTION_A_v01 l. 52-57 (claim sentences; "of the remaining room" replaced by "of the class-average margin's avoidable
    wrong-go under this scoring", Clarifications 01 point 7) with review M1: the percentile interval decides; not evaluable when more than
    2.5% of resamples have den0 <= 0 OR den0 is below 10 decision-equivalents (JUDGEMENT, resolution-based); A4's hull clause on
    branches 4 and 5 ("; not robust to the convex-hull frontier" unless the hull RR0 is evaluable with l_h above the branch's line).
    Returns (branch, wording, hull_robust or None)."""
    inv = s_rr['invalid_share']; l, u = s_rr['ci']
    if inv > MAX_INVALID:
        return 1, '%s: not evaluable (%.1f%% of resamples without room)' % (arm, 100. * inv), None
    if not (np.isfinite(den_pt_dec_eq) and den_pt_dec_eq >= MIN_DEC_EQ):
        return 1, ('%s: not evaluable (the denominator is %.2f decision-equivalents, below %d; resolution rule)'
                   % (arm, den_pt_dec_eq, MIN_DEC_EQ)), None
    if not (np.isfinite(l) and np.isfinite(u)):
        return 0, '%s: no branch applies (non-finite interval)' % arm, None
    h_ok = s_hull is not None and s_hull['invalid_share'] <= MAX_INVALID and np.isfinite(s_hull['ci'][0])
    if u < 0:
        return 2, ('%s recovers less of the class-average margin\'s avoidable wrong-go under this scoring than the class-average '
                   'covariance' % arm), None
    if l <= 0 <= u:
        return 3, '%s recovers no share distinguishable from zero; the data allow at most %.3f' % (arm, u), None
    if l > 0.5:
        rob = bool(h_ok and s_hull['ci'][0] > 0.5)
        return 4, ('%s recovers most of the class-average margin\'s avoidable wrong-go under this scoring, between %.3f and %.3f%s'
                   % (arm, l, u, '' if rob else '; not robust to the convex-hull frontier')), rob
    rob = bool(h_ok and s_hull['ci'][0] > 0)
    return 5, ('%s recovers a share distinguishable from zero, between %.3f and %.3f%s'
               % (arm, l, u, '' if rob else '; not robust to the convex-hull frontier')), rob


WEAK_ORDER = {1: 0, 2: 1, 3: 2, 5: 3, 4: 4}       # review B2: weakest first, in the order 1 < 2 < 3 < 5 < 4


# ------------------------------------------------------------------------------------------------ Spearman (new; Part 2)
class RankPrep:
    """Average-tie ranks of x under integer weights w (each item repeated w times), for many weight vectors at once.
    Sorting and tie groups are fixed once (x as given); ranks of a weighted resample: group rank = weight before the group +
    (group weight + 1) / 2 (the average of the positions the group occupies when its items are repeated)."""

    def __init__(self, x):
        x = np.asarray(x, float)
        self.n = x.size
        self.order = np.argsort(x, kind='stable')
        xs = x[self.order]
        new = np.concatenate([[True], xs[1:] != xs[:-1]]) if self.n else np.zeros(0, bool)
        self.starts = np.nonzero(new)[0]
        self.sizes = np.diff(np.concatenate([self.starts, [self.n]]))

    def ranks(self, W):
        """W (B, n) weights -> (B, n) average-tie ranks of the repeated sample, in the original item order."""
        Ws = W[:, self.order]
        Wg = np.add.reduceat(Ws, self.starts, axis=1)
        before = np.cumsum(Wg, axis=1) - Wg
        rg = before + (Wg + 1.) / 2.
        rs = np.repeat(rg, self.sizes, axis=1)
        out = np.empty_like(rs)
        out[:, self.order] = rs
        return out


def wpearson(rx, ry, W):
    """Pearson correlation of rx, ry with weights W (rows = resamples); NaN where undefined."""
    sw = W.sum(axis=1)
    with np.errstate(divide='ignore', invalid='ignore'):
        mx = (W * rx).sum(axis=1) / sw; my = (W * ry).sum(axis=1) / sw
        dx = rx - mx[:, None]; dy = ry - my[:, None]
        cov = (W * dx * dy).sum(axis=1); vx = (W * dx * dx).sum(axis=1); vy = (W * dy * dy).sum(axis=1)
        r = cov / np.sqrt(vx * vy)
    return np.where(np.isfinite(r), r, np.nan)


def spearman_w(x, y, W):
    """Spearman's rho (Pearson of average-tie ranks) of x and y for each weight row of W (B, n)."""
    W = np.atleast_2d(np.asarray(W, float))
    return wpearson(RankPrep(x).ranks(W), RankPrep(y).ranks(W), W)


def spearman(x, y):
    return float(spearman_w(x, y, np.ones((1, len(x))))[0])


# ------------------------------------------------------------------------------------------------ files (oxsb_core_v03 copies)
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def root_rel(path, roots):
    """(root name, relative path with '/') of a file under one of roots {name: path}; None otherwise."""
    p = pathlib.Path(path).resolve()
    for name, root in roots.items():
        r = pathlib.Path(root).resolve()
        if r == p or r in p.parents:
            return name, p.relative_to(r).as_posix()
    return None


def write_once(path, text):
    try:
        with open(path, 'x', encoding='utf-8') as f:
            f.write(text)
    except FileExistsError:
        raise RuntimeError('REFUSED: %s exists (write once)' % path)


def clock():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def json_dump(obj):
    return json.dumps(obj, indent=1, default=float, allow_nan=True)
