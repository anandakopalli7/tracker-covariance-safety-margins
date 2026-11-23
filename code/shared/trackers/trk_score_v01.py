"""v13 shared tracker library: scoring add-ons of AMENDMENT_10_v13 sections 2-3. New file, 19 Nov 2026 (Claude Opus 5.5).

Reuses, imported unchanged and read-only: the scoring library of record optA_lib_v02 (as L) and the v12 gridless code
(revision_v12\\analysis\\a9_common_v01: Gridless, gridless_sources, row_stats). A "run" is a dict with at least
  desired (float), idx55 (n,), clear1 (n, 17) = L.clean_clear(clear), vbar (n, 17), masks (tuple of (n,) bool), crit {name: (n, 17)},
  ev (n,) evaluated flags.
(make_run builds one from trk_arrays_v01.extract output.)

A10 section 2.2  E5 family
  margin_ratios(runs, a, b): per evaluated decision and row with finite positive critical scales of both a and b, the ratio
      sqrt(c_b / c_a) (= sqrt(s_a / s_b) at the binding constraint: "the margin ratio"). Returns the pooled array.
      A10's m_x (ratio sqrt(s_Nx / s_F0x)) = median of margin_ratios(runs, 'N_x', 'F0_x'); of record 1.1029 for N.
  ratio_summary(m): median m_x, q05, q95, A_x = (q95 - q05) / (2 m_x), share within 5% of the median, barely_varies (>= 0.95).
  e5_u(runs, f0, e): u_i = (mid-rank of r_i - 0.5) / n over the run set's evaluated decisions; r_i = median over rows with finite
      positive c_f0 and c_e of sqrt(c_f0 / c_e); evaluated decisions without such rows get 0.5. Non-evaluated decisions: 0.5.
  permute_u(runs, u, seed=20261915): u permuted within each run among its evaluated decisions (fresh default_rng(seed); runs in the
      given order; one permutation per run).
  add_oracle(runs, name, f0, m, A, u): crit[name] = c_f0 / f_i^2, f_i = m (1 + A (2 u_i - 1)).   E5: m = 1.1029, A = 0.05.
A10 section 2.3  gridless frontier (A9-1(c)): gridless(runs, names, safe_fn) -> {name: a9 Gridless}; rr_gl(G, refF0, refE, names,
  pop) -> point dict (denE, D, RR, n, dec-eq); boot_gl(...) -> resample arrays over run-count weights (the draw of record or another).
  The F0 / E roles are passed explicitly (F0_x, E_x for a variant's own room).
A10 section 2.4  est_phase(vhat, ahat_long, lead_found, thr=-1.0): 2 stopped (vhat <= 0.5), 1 braking (vhat > 0.5 and ahat_long <= thr),
  0 before braking (else, or no lead track). Same codes as the truth phase of record (0 before onset, 1 lead moving, 2 stopped).
A10 B6(a)  realised_decel(cap) (rev_h_run_facts_v01 rule) and terciles(ids, decel): ascending realised deceleration, ties by id,
  numpy.array_split into three.
A10 B6(b)  delayed_stop_clearance(rd, cap, taus, A=6.0): per evaluated decision i and row, the true clearance of "follow the row until
  tau_i, then brake (jerk 12.65 m/s^3 to -A, hold to the first stop)" over frames 0..60, minimum over true actors; tau_i any real
  >= 0.05 s. Generalises the stop of record (recount_A5_pack_v01.stop_profile, tau on the 0.05 s grid) to a tau inside a step:
  the row's piecewise-constant acceleration a[j] of step j gives v(tau), s(tau) exactly (speed floor 0 as the row generator), the
  initial acceleration of the stop is a[j] (the record's a[j0 - 1] when tau is on the grid). draw_delays(n, seed=20261916).
"""
import json, math, pathlib, sys
import numpy as np
import trk_env_v01 as env

P = pathlib.Path(r'<library folder>')
V12 = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis')
for p in (str(P / '11_ojits' / 'A6R' / 'code'), str(V12)):
    if p not in sys.path:
        sys.path.insert(0, p)
import optA_lib_v02 as L                    # noqa: E402
import a9_common_v01 as A9                  # noqa: E402

RATIO = 1.1029
E5_AMP = 0.05
SEED_PERM = 20261915
SEED_DELAY = 20261916
H = 0.05
JERK = 12.65
GRID = np.concatenate([[0.], np.logspace(-2, 3, 201)])


def make_run(arrs, masks, crit_map, desired=None, name=None):
    """crit_map: {name: array key in arrs}. masks: tuple of (n,) bool arrays (population masks; evaluated decisions only)."""
    return dict(run=name, desired=float(desired if desired is not None else arrs['des'][0]), idx55=np.asarray(arrs['idx55']).astype(np.int64),
                clear1=L.clean_clear(arrs['clear']), vbar=arrs['vbar'], masks=tuple(masks), ev=np.asarray(arrs['evaluated']).astype(bool),
                crit={nm: np.asarray(arrs[key], float) for nm, key in crit_map.items()}, sel={}, late={})


# ------------------------------------------------------------------------------------------------ 2.2
def margin_ratios(runs, a, b):
    out = []
    for r in runs:
        ca = r['crit'][a][r['ev']]; cb = r['crit'][b][r['ev']]
        ok = np.isfinite(ca) & np.isfinite(cb) & (ca > 0) & (cb > 0)
        out.append(np.sqrt(cb[ok] / ca[ok]))
    return np.concatenate(out) if out else np.zeros(0)


def ratio_summary(m):
    m = np.asarray(m, float)
    if m.size == 0:
        return dict(n=0)
    med = float(np.median(m)); q05, q95 = (float(x) for x in np.quantile(m, [0.05, 0.95]))
    within = float(np.mean(np.abs(m / med - 1.) <= 0.05))
    return dict(n=int(m.size), median=med, q05=q05, q95=q95, A=(q95 - q05) / (2. * med), share_within_5pct=within,
                barely_varies=bool(within >= 0.95), q25=float(np.quantile(m, 0.25)), q75=float(np.quantile(m, 0.75)))


def _midrank(x):
    o = np.argsort(x, kind='stable'); xs = x[o]
    ranks = np.empty(x.size, float)
    i = 0
    while i < xs.size:
        j = i
        while j + 1 < xs.size and xs[j + 1] == xs[i]:
            j += 1
        ranks[o[i:j + 1]] = 0.5 * (i + j) + 1.
        i = j + 1
    return ranks


def e5_u(runs, f0='F0', e='E'):
    rs = []; idx = []
    for ri, r in enumerate(runs):
        cf = r['crit'][f0]; ce = r['crit'][e]
        for i in np.flatnonzero(r['ev']):
            ok = np.isfinite(cf[i]) & np.isfinite(ce[i]) & (cf[i] > 0) & (ce[i] > 0)
            rs.append(float(np.median(np.sqrt(cf[i][ok] / ce[i][ok]))) if ok.any() else np.nan)
            idx.append((ri, i))
    rs = np.array(rs)
    u_all = np.full(rs.size, 0.5)
    have = np.isfinite(rs)
    n = int(rs.size)                                   # n = the run set's evaluated decisions
    if have.any():
        # mid-ranks among decisions with a ratio; decisions without one take 0.5 and do not enter the ranking
        rk = _midrank(rs[have])
        u_all[have] = (rk - 0.5) / have.sum()
    u = [np.full(r['ev'].size, 0.5) for r in runs]
    for (ri, i), val in zip(idx, u_all):
        u[ri][i] = val
    return u, dict(n_evaluated=n, n_with_ratio=int(have.sum()))


def permute_u(runs, u, seed=SEED_PERM):
    rng = np.random.default_rng(seed)
    out = []
    for r, uu in zip(runs, u):
        uu = uu.copy(); ev = np.flatnonzero(r['ev'])
        uu[ev] = uu[ev][rng.permutation(ev.size)]
        out.append(uu)
    return out


def add_oracle(runs, name, f0, m, A, u):
    for r, uu in zip(runs, u):
        f = m * (1. + A * (2. * uu - 1.))
        r['crit'][name] = r['crit'][f0] / (f * f)[:, None]
        r['sel'].pop(name, None)


# ------------------------------------------------------------------------------------------------ 2.3
def safe_w1(r):
    return r['clear1'] > 0.


def gridless(runs, names, safe_fn=safe_w1, masks_key='masks'):
    """{name: A9.Gridless} over the runs (A9-1(c) events: every scale in [0, 1e3] where a selection changes)."""
    return A9.gridless_sources(runs, names, safe_fn, masks_key=masks_key)


def rr_gl(G, f0, e, names, pop=0, w=None):
    """Point (or one resample with run weights w) on the gridless step frontier: the roles F0 := f0, E := e."""
    T = {'F0': G[f0].curve(w, pops=[pop])[:, 0, :], 'E': G[e].curve(w, pops=[pop])[:, 0, :]}
    for a in names:
        T[a] = G[a].curve(w, pops=[pop])[:, 0, :]
    ev = L.eval_scoring(T, list(names))
    out = dict(denE=ev['denE'], n=ev['n'], R_pp=ev['denE'] / L.NLEV, R_deceq=L.dec_eq(ev['denE'], ev['n']), D={}, RR={}, D_deceq={})
    for a in names:
        out['D'][a] = ev['D'][a]; out['RR'][a] = L.ratio(ev['D'][a], ev['denE']); out['D_deceq'][a] = L.dec_eq(ev['D'][a], ev['n'])
    return out


def boot_gl(G, f0, e, names, CNT, pop=0):
    B = CNT.shape[0]
    res = dict(denE=np.full(B, np.nan), n=np.full(B, np.nan), D={a: np.full(B, np.nan) for a in names})
    for b in range(B):
        p = rr_gl(G, f0, e, names, pop, CNT[b])
        res['denE'][b] = p['denE']; res['n'][b] = p['n']
        for a in names:
            res['D'][a][b] = p['D'][a]
    return res


def rr_summary(point, boot, a):
    """Percentile interval of RR_gl(a) (resamples with den > 0) and of the room, as L.summ / summ_den."""
    with np.errstate(divide='ignore', invalid='ignore'):
        rr = np.where(np.isfinite(boot['denE']) & (boot['denE'] > 0), boot['D'][a] / boot['denE'], np.nan)
    return L.summ(rr, point['RR'][a])


# ------------------------------------------------------------------------------------------------ 2.4
def est_phase(vhat, ahat_long, lead_found, thr=-1.0):
    vhat = np.asarray(vhat, float); ah = np.asarray(ahat_long, float); fd = np.asarray(lead_found, bool)
    ph = np.zeros(vhat.shape, np.int8)
    stp = fd & (vhat <= 0.5)
    brk = fd & (vhat > 0.5) & np.isfinite(ah) & (ah <= thr)
    ph[brk] = 1; ph[stp] = 2
    return ph


# ------------------------------------------------------------------------------------------------ B6(a)
def realised_decel(cap):
    """rev_h_run_facts_v01 rule: minus the least-squares slope of the true lead speed against time between 90% and 10% of its speed
    before the brake onset (onset 5 s + brake_start_s after the episode clock starts; time = k * 0.05 s). None if < 4 samples."""
    cap = pathlib.Path(cap)
    draw = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))['case']['draw']
    ks = []; vs = []
    for r in env.jl(cap / 'evaluation_truth.jsonl'):
        tg = r.get('target')
        if not tg:
            continue
        a = [x for x in (r.get('scenario_actors') or []) if x['actor_id'] == tg['actor_id']]
        if not a:
            continue
        v = a[0]['velocity_lh']; ks.append(r['k']); vs.append(math.hypot(v[0], v[1]))
    ks = np.array(ks); vs = np.array(vs); t = ks * 0.05
    pre = (t > 3) & (t < 5 + draw['brake_start_s'] - 0.2)
    v0 = float(np.median(vs[pre])) if pre.any() else float(vs[:20].max())
    sel = (vs < 0.9 * v0) & (vs > 0.1 * v0) & (t > 5 + draw['brake_start_s'] - 0.5)
    if sel.sum() >= 4:
        i = np.nonzero(sel)[0]; i = np.arange(i[0], i[-1] + 1)
        return float(-np.polyfit(t[i], vs[i], 1)[0])
    return None


def terciles(ids, decel):
    """Ascending realised deceleration, ties by id; None (no realised value) sorts last. Returns three lists of ids."""
    key = sorted(zip(ids, decel), key=lambda x: ((x[1] is None), x[1] if x[1] is not None else 0., x[0]))
    order = [k for k, _ in key]
    return [list(map(str, s)) for s in np.array_split(np.array(order, dtype=object), 3)]


# ------------------------------------------------------------------------------------------------ B6(b)
def draw_delays(n, seed=SEED_DELAY):
    return np.random.default_rng(seed).uniform(0., 0.75, size=n)


def _first_stop(v0, a0, jr, t1, A):
    """recount_A5_pack_v01.first_stop (same lines)."""
    if v0 <= 0. and a0 <= 0.:
        return 0.
    qa, qb, qc = .5 * jr, a0, v0
    disc = qb * qb - 4. * qa * qc
    if disc >= 0.:
        sq = math.sqrt(disc)
        q = -.5 * (qb + math.copysign(sq, qb)) if qb != 0. else -.5 * (qb + sq)
        roots = []
        if q != 0.:
            roots += [q / qa, qc / q]
        else:
            roots += [0.]
        roots = sorted(r for r in roots if 1e-12 < r <= t1)
        if roots:
            return roots[0]
    v1 = v0 + a0 * t1 + .5 * jr * t1 * t1
    return t1 + max(v1, 0.) / A


def row_state_at(s_row, v_row, a_row, tau):
    """Position, speed and acceleration of a planner row at time tau (row generator: constant acceleration a[j] in step j,
    speed floored at 0 / capped at 20 inside the step)."""
    j = int(math.floor(tau / H + 1e-9))
    dt = tau - j * H
    if abs(dt) <= 1e-9:
        jj = int(round(tau / H))
        return float(s_row[jj]), float(v_row[jj]), float(a_row[jj - 1])
    v = float(v_row[j]); a = float(a_row[j]); s = float(s_row[j])
    vn = v + a * dt
    if vn < 0. or vn > 20.:
        bound = 0. if vn < 0. else 20.
        ts = (bound - v) / a
        return s + v * ts + .5 * a * ts * ts + bound * (dt - ts), bound, a
    return s + v * dt + .5 * a * dt * dt, vn, a


def stop_profile_cont(s_row, v_row, a_row, tau, A):
    """The row until tau, then the stop of record from (s, v, a) at tau; positions at the 61 ticks."""
    s = np.array(s_row, float)
    x0, v0, a0 = row_state_at(s_row, v_row, a_row, tau)
    jr = -JERK if a0 > -A else JERK
    t1 = abs(-A - a0) / JERK
    ts = _first_stop(v0, a0, jr, t1, A)
    jj = np.arange(61)
    after = jj * H > tau + 1e-9
    t = np.minimum(jj[after] * H - tau, ts)
    x1 = x0 + v0 * t1 + .5 * a0 * t1 ** 2 + jr * t1 ** 3 / 6.
    v1 = v0 + a0 * t1 + .5 * jr * t1 ** 2
    tr = np.minimum(t, t1); th = np.maximum(t - t1, 0.)
    ramp = x0 + v0 * tr + .5 * a0 * tr ** 2 + jr * tr ** 3 / 6.
    hold = x1 + v1 * th - .5 * A * th ** 2
    s[after] = np.where(t <= t1, ramp, hold)
    return s


def delayed_stop_clearance(rd, cap, taus, A=6.0, only=None):
    """taus: {decision index: tau_i}. Returns (n_dec, 17) clearances (NaN where not computed). Uses the logged decisions (the rows
    depend on the ego state only, not on the tracker)."""
    import trk_arrays_v01 as TA
    Lr = TA.load_capture(rd, cap)
    T = Lr['T']; kmax = Lr['kmax']; draw = Lr['draw']
    decs = list(TA.gc.decisions(Lr['cap']))
    out = np.full((len(decs), 17), np.nan)
    for di, (k, dec) in enumerate(decs):
        if di not in taus:
            continue
        ms = dec['model_state']; Lg, Wd = dec['ego_length'], dec['ego_width']
        rows = TA.finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'],
                                                 dec['actors'], Lg, Wd, dec['now'], TA.consumer.Diagnostics())
        sv = [stop_profile_cont(r['s'], r['v'], r['a'], float(taus[di]), A) for r in rows]
        wt = TA.ox.window_truth(T, k, kmax, draw, False)[0]
        res = TA.ox.clearance([{'s': x} for x in sv], T[k]['ego'], Lg, Wd, wt, 61)
        cm = np.full(17, np.inf)
        for aid, (mn, d0) in res.items():
            cm = np.minimum(cm, mn)
        out[di] = cm
    return out
