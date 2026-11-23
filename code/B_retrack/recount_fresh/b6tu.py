"""Second program, spec sections 6b (B6 / stop reliance, LB.*) and 6c (tuning runs, TU.*).  Lineage: ..\\recount\\b6.py (terciles, delayed stop)
and rc_core.py (gridless engine); REL (A9-6 (1)) and TU are written here from the definitions."""
import os, sys, glob, json, time
import numpy as np
from rf_core import L, NS, RunSet, breakpoints, stats_curve, stats_grid

PA = r'<library folder>'
REC_G = PA + r'\09_redesign\m2_decisions\openloop\gateR_rt_v01'
REC_X = PA + r'\11_ojits\A4\fit\extract'
REC_L = r'ARS_TRIAL\revision_v12\analysis\out\lead'
CACHE = PA + r'\11_ojits\review\optionA_recount_v01\cache'
ARCH = PA + r'\07_fit_runs\archives'
TUNE_X = PA + r'\11_ojits\A4\dryrun\extract'
V13 = r'ARS_TRIAL\revision_v13'
BR = V13 + r'\work\B_retrack'
CD = V13 + r'\work\CD_capture'
EXT = r'ARS_TRIAL\revision_v11\analysis\out\ext'
GRID = np.concatenate([[0.], np.logspace(-2, 3, 201)])
SEED_DS = 20261916


# ------------------------------------------------------------------------------------------------------ loading
def load_record(run):
    g = np.load(r'%s\%s.npz' % (REC_G, run), allow_pickle=True)
    x = np.load(r'%s\%s.npz' % (REC_X, run), allow_pickle=True)
    l = np.load(r'%s\%s.npz' % (REC_L, run), allow_pickle=True)
    d = {k: g[k] for k in ['k', 'evaluated', 'v0', 'des', 'clear', 'vbar', 'idx55', 'cF0', 'cE', 'cN']}
    for k in ['cNA', 'cQ', 'cA1', 'cCK3']:
        d[k] = x[k]
    for k in ['phase', 'now', 'lead_found']:
        d[k] = l[k]
    return d


def ev_slice(a, ev):
    return a[ev] if a.shape[0] == ev.shape[0] else a


def capture_dir_old(run):
    return glob.glob(r'%s\%s\x\%s\capture\*\\' % (ARCH, run, run))[0]


def capture_dir_fresh(rid):
    return glob.glob(r'%s\work\CD_capture\runs\%s\%s\capture\*\\' % (V13, rid, rid))[0]


def realised_decel_rule(d):
    """Rule of record (B_ANALYSIS_DEFINITIONS 'Realised lead deceleration'): v = |velocity_lh| (3-D norm) of target at tick k, t = 0.05 k;
    v_pre = median v over 3 < t < 5 + brake_start_s - 0.2 (else max of first 20); samples 0.1 v_pre < v < 0.9 v_pre and
    t > 5 + brake_start_s - 0.5; if >= 4, contiguous index range first..last, minus polyfit slope; else NaN."""
    L_ = [json.loads(l) for l in open(d + 'evaluation_truth.jsonl')]
    c = json.load(open(d + 'contract.json'))['case']['draw']
    kk = np.array([x['k'] for x in L_]); t = 0.05 * kk
    v = np.array([np.sqrt(sum(float(a) ** 2 for a in x['target']['velocity_lh'][:3])) for x in L_])
    bs = c['brake_start_s']
    m = (t > 3) & (t < 5 + bs - 0.2)
    vp = float(np.median(v[m])) if m.any() else float(np.max(v[:20]))
    sel = np.nonzero((v > 0.1 * vp) & (v < 0.9 * vp) & (t > 5 + bs - 0.5))[0]
    if sel.size < 4:
        return float('nan')
    ii = np.arange(sel[0], sel[-1] + 1)
    return -float(np.polyfit(t[ii], v[ii], 1)[0])


def load_b6_inputs(mode):
    """returns names, data (run -> dict), clearR, clearDS, tau_stored (evaluated-only), decel, cache61 (test mode only, else None).
    Primary scorings (spec 6b, changed 20 Nov before any fresh value): judged until the stop ends."""
    cache = None
    if mode == 'fresh':
        import recount_fresh as RF
        names = RF.fresh_run_ids()
        data = {r: dict(np.load(r'%s\arrays\CV0\%s.npz' % (CD, r), allow_pickle=True)) for r in names}
        clearR = {}
        for r in names:
            z = np.load(r'%s\arrays\RSX\%s.npz' % (CD, r), allow_pickle=True)
            assert z['k'].shape == data[r]['k'].shape and (z['k'] == data[r]['k']).all(), 'RSX k differs from CV0 k: ' + r
            assert (z['evaluated'].astype(bool) == data[r]['evaluated'].astype(bool)).all(), 'RSX evaluated differs: ' + r
            clearR[r] = ev_slice(z['clearX_t0p75_a6p0'], data[r]['evaluated'].astype(bool))
        dsd = r'%s\out\fresh_b6\clear\%%s.npz' % BR
        capd = capture_dir_fresh
    else:
        names = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
        data = {r: load_record(r) for r in names}
        ev = {r: data[r]['evaluated'].astype(bool) for r in names}
        clearR = {r: ev_slice(np.load(r'%s\%s.npz' % (EXT, r), allow_pickle=True)['clearX_t0p75_a6p0'], ev[r]) for r in names}
        cache = {r: ev_slice(np.load(r'%s\%s_pack.npz' % (CACHE, r), allow_pickle=True)['t0p75_a6p0'], ev[r]) for r in names}
        dsd = r'%s\out\fresh_testold\b6_clear_ext\%%s.npz' % BR
        capd = capture_dir_old
    clearDS = {}; tau_st = {}
    for r in names:
        z = np.load(dsd % r, allow_pickle=True); ev = data[r]['evaluated'].astype(bool)
        clearDS[r] = ev_slice(z['clear'], ev); tau_st[r] = ev_slice(z['tau'], ev)
    decel = {r: realised_decel_rule(capd(r)) for r in names}
    return names, data, clearR, clearDS, tau_st, decel, cache


# ------------------------------------------------------------------------------------------------------ REL (A9-6 (1))
def frontier_points(c, w):
    """Operating point index (in the input order) of the step frontier at each caution level; mirrors optA_lib.frontier:
    among finite points sorted (stable) by caution, the running minimum of w; the point attaining it is the first (lowest caution)
    point that reached the current running-minimum value."""
    ok = np.nonzero(np.isfinite(c) & np.isfinite(w))[0]
    o = ok[np.argsort(c[ok], kind='stable')]
    best = np.inf; att = []
    for i in o:
        if w[i] < best:
            best = w[i]; att.append(i)
        else:
            att.append(att[-1])
    return o, np.array(att)


def rel_shares(rs, safeR, srcs=('F0', 'N', 'CK3')):
    """For x in srcs: mean over the 201 levels of the share of evaluated decisions whose selected row at x's frontier operating point
    under W_R (grid frontier, 202-value grid) is unsafe under W1 but safe under W_R."""
    keymap = {'F0': 'cF0', 'E': 'cE', 'N': 'cN', 'CK3': 'cCK3'}
    T = {}; X = {}
    for nm in ['F0', 'E'] + [s for s in srcs if s != 'F0']:
        t = 0; xs = 0
        for q, sR in zip(rs.d, safeR):
            c1 = L.clean_clear(q['clear']); s1 = c1 > 0.
            sel = L.select_grid(q[keymap[nm]], GRID, q['idx55'])
            masks = [np.ones(len(q['k']), bool)]
            t = t + L.stats_scored(sel, c1, sR, q['vbar'], q['des'], masks)
            ar = np.arange(len(q['k']))
            xs = xs + (~s1[ar[None, :], sel] & sR[ar[None, :], sel]).sum(axis=1)
        T[nm] = t[:, 0, :]; X[nm] = xs.astype(float)
    n = T['F0'][0, 0]
    cur = L.curves_w(T, 0)
    cF0 = cur['F0'][0]; cE = cur['E'][0]
    lev = L.levels_of(cF0, cE, cF0[0])
    out = {}
    for nm in srcs:
        c, w = cur[nm]
        x = X[nm] if nm in ('F0', 'E') else np.concatenate([[X['F0'][0]], X[nm]])
        o, att = frontier_points(c, w)
        cs = c[o]
        idx = np.searchsorted(cs, lev, side='right') - 1
        pts = att[idx]
        out[nm] = float(np.mean(x[pts] / n))
    return out


# ------------------------------------------------------------------------------------------------------ gridless tables
def run_tables(rs, clears, which=('F0', 'E')):
    """clears: dict scoring -> list (per run) of clearance arrays (evaluated rows) or None for W1. Returns scoring -> src -> Trun."""
    keymap = {'F0': 'cF0', 'E': 'cE'}
    G = {s: breakpoints([q[keymap[s]] for q in rs.d]) for s in which}
    out = {}
    for sc, cl in clears.items():
        out[sc] = {}
        for s in which:
            Tr = []
            for i, q in enumerate(rs.d):
                c1 = L.clean_clear(q['clear'])
                sx = (c1 > 0.) if cl is None else (L.clean_clear(cl[i]) > 0.)
                Tr.append(stats_curve(q[keymap[s]], G[s], c1, sx, q['vbar'], q['des'], q['idx55'], [np.ones(len(q['k']), bool)])[:, 0, :])
            out[sc][s] = np.stack(Tr)
    return out


def room_of(Tr, sel):
    Td = {s: Tr[s][sel].sum(axis=0) for s in ('F0', 'E')}
    ev = L.eval_scoring(Td, [])
    return ev['denE'], ev['n']


def den0_of(rs, cl, sel, Tr):
    """D_gl(F0, O) under scoring cl (decision-equivalents) on the runs `sel`."""
    Td = {s: Tr[s][sel].sum(axis=0) for s in ('F0', 'E')}
    To = 0
    for i in sel:
        q = rs.d[i]
        c1 = L.clean_clear(q['clear']); sx = L.clean_clear(cl[i]) > 0.
        o = L.select_first_safe(sx, q['idx55'])
        To = To + L.stats_scored(o, c1, sx, q['vbar'], q['des'], [np.ones(len(q['k']), bool)])
    Td['O'] = To[:, 0, :]
    ev = L.eval_scoring(Td, ['O'])
    return L.dec_eq(ev['D']['O'], ev['n'])


def b6_compute(mode, K, log=print):
    t0 = time.time()
    names, data, clearR, clearDS, tau_st, decel, cache = load_b6_inputs(mode)
    nr = len(names)
    rs = RunSet(data, names)
    cR = [clearR[r] for r in names]; cD = [clearDS[r] for r in names]
    # delayed-stop tau draw check (spec 6b): one draw over all evaluated decisions, runs in order, k order
    rng = np.random.default_rng(SEED_DS)
    tau_diff = 0.
    for r in names:
        n = int(data[r]['evaluated'].sum())
        tm = 0.75 + rng.uniform(0., 0.75, n)
        tau_diff = max(tau_diff, float(np.max(np.abs(tau_st[r] - tm))))
    tabs = run_tables(rs, {'W1': None, 'WR': cR, 'DS': cD})
    log('b6 tables %.1fs' % (time.time() - t0), flush=True)
    allr = np.arange(nr)
    res = {}; extra = {}
    dW1, n = room_of(tabs['W1'], allr); dWR, _ = room_of(tabs['WR'], allr); dDS, _ = room_of(tabs['DS'], allr)
    res['LB.RS075.rel'] = dWR / dW1 if dW1 > 0 else float('nan')
    res['LB.DS.rel'] = dDS / dW1 if dW1 > 0 else float('nan')
    res['LB.DS.den0.dec'] = den0_of(rs, cD, allr, tabs['DS'])
    extra.update(R_pp_W1=dW1 / 201., R_pp_WR=dWR / 201., R_pp_DS=dDS / 201., room_dec_WR=L.dec_eq(dWR, n), room_dec_DS=L.dec_eq(dDS, n),
                 den0_dec_WR_all=den0_of(rs, cR, allr, tabs['WR']), tau_max_abs_diff=tau_diff, n=float(n))
    # terciles
    dv = np.array([decel[r] for r in names])
    order = sorted(range(nr), key=lambda i: (dv[i] if np.isfinite(dv[i]) else np.inf, names[i]))
    terc = [list(a) for a in np.array_split(np.array(order), 3)]
    rels = []
    for ti, sel in enumerate(terc):
        sel = [int(i) for i in sel]
        a, nn = room_of(tabs['WR'], sel); b, _ = room_of(tabs['W1'], sel)
        rel = a / b if b > 0 else float('nan')
        d0 = den0_of(rs, cR, sel, tabs['WR'])
        k = 'LB.T%d.' % (ti + 1)
        res[k + 'rel'] = rel; res[k + 'den0.dec'] = d0; res[k + 'evaluable'] = bool(d0 >= 10.)
        res[k + 'range'] = '%.2f\u2013%.2f' % (dv[sel].min(), dv[sel].max())
        extra['T%d' % (ti + 1)] = dict(R_pp_WR=a / 201., R_pp_W1=b / 201., room_dec_WR=L.dec_eq(a, nn), room_dec_W1=L.dec_eq(b, nn), n_runs=len(sel),
                                       n=float(nn), decel_min=float(dv[sel].min()), decel_max=float(dv[sel].max()))
        if d0 >= 10. and np.isfinite(rel):
            rels.append(rel)
    if rels:
        res['LB.T.relmin'] = min(rels); res['LB.T.relmax'] = max(rels)
    extra['decel_range'] = [float(np.nanmin(dv)), float(np.nanmax(dv))]
    # REL
    safeR = [L.clean_clear(c) > 0. for c in cR]
    rl = rel_shares(rs, safeR)
    res['LB.REL_F0'] = rl['F0']; res['LB.REL_N'] = rl['N']; res['LB.REL_CK3'] = rl['CK3']
    if cache is not None:     # test-mode sensitivity: the 61-frame stop cache as W_R
        cc = [cache[r] for r in names]
        rx = rel_shares(rs, [L.clean_clear(c) > 0. for c in cc])
        extra['REL_stopcache61'] = rx
        tc = run_tables(rs, {'WR': cc}, which=('F0', 'E'))['WR']
        dc, _ = room_of(tc, allr)
        d61 = [ev_slice(np.load(os.path.join(BR, 'out', 'fresh_testold', 'b6_clear_ext', r + '.npz'), allow_pickle=True)['clear61'],
                        data[r]['evaluated'].astype(bool)) for r in names]
        td = run_tables(rs, {'DS': d61}, which=('F0', 'E'))['DS']
        dd, _ = room_of(td, allr)
        extra['ds61'] = dict(R_pp=dd / 201., rel=dd / dW1, den0_dec=den0_of(rs, d61, allr, td))
        extra['stopcache61'] = dict(R_pp_WR=dc / 201., rel=dc / dW1, den0_dec=den0_of(rs, cc, allr, tc))
    log('b6 points done %.1fs' % (time.time() - t0), flush=True)
    # bootstrap (all runs): per-resample D_gl(E,F0) under WR, W1, DS
    seed, nn_ = (20261911, 105) if mode == 'fresh' else (20261113, 35)
    idx = np.random.default_rng(seed).integers(0, nr, (20000, nr))[:K]
    cnt = np.zeros((K, nr))
    for b in range(K):
        cnt[b] = np.bincount(idx[b], minlength=nr)
    out = {k: np.full(K, np.nan) for k in ['WR', 'W1', 'DS']}
    flat = {sc: {s: tabs[sc][s].reshape(nr, -1) for s in ('F0', 'E')} for sc in tabs}
    Gt = max(tabs['W1'][s].shape[1] for s in ('F0', 'E'))
    chunk = max(1, min(20, int(4e6 // (Gt * NS))))
    tb = time.time()
    for b0 in range(0, K, chunk):
        c = cnt[b0:b0 + chunk]
        Tb = {sc: {s: (c @ flat[sc][s]).reshape(len(c), -1, NS) for s in ('F0', 'E')} for sc in flat}
        for j in range(len(c)):
            for sc in ('WR', 'W1', 'DS'):
                out[sc][b0 + j] = L.eval_scoring({s: Tb[sc][s][j] for s in ('F0', 'E')}, [])['denE']
        if (b0 // chunk) % 50 == 0:
            log('b6 boot %d/%d %.1fs' % (b0, K, time.time() - tb), flush=True)
    boot_s = time.time() - tb
    pos = out['W1'] > 0
    with np.errstate(divide='ignore', invalid='ignore'):
        res['LB.RS075.rel.ci'] = L.pct(np.where(pos, out['WR'] / out['W1'], np.nan))
        res['LB.DS.rel.ci'] = L.pct(np.where(pos, out['DS'] / out['W1'], np.nan))
    extra.update(K=K, boot_seconds=boot_s, boot_ms_per_resample=1000 * boot_s / K, total_seconds=time.time() - t0)
    return res, out, extra


# ------------------------------------------------------------------------------------------------------ TU
def tu_load():
    fs = sorted(glob.glob(TUNE_X + r'\*.npz'))
    names = [os.path.basename(f)[:-4] for f in fs]
    data = {}
    for r in names:
        g = np.load(r'%s\%s.npz' % (REC_G, r), allow_pickle=True)
        x = np.load(r'%s\%s.npz' % (TUNE_X, r), allow_pickle=True)
        c = np.load(r'%s\out\retrack\CV0\%s_arrays.npz' % (BR, r), allow_pickle=True)
        d = {k: g[k] for k in ['k', 'evaluated', 'des', 'clear', 'vbar', 'idx55', 'cF0', 'cE', 'cN']}
        for k in ['cNA', 'cQ', 'cA1', 'cCK3', 'phase']:
            d[k] = x[k]
        assert (x['k'] == g['k']).all()
        pos = {int(k): i for i, k in enumerate(c['k'])}
        ii = np.array([pos[int(k)] for k in g['k']])
        for k in ['lead_found', 'vhat', 'ahat_long']:
            d[k] = c[k][ii]
        data[r] = d
    return names, data


def tu_masks(q):
    lf = q['lead_found'].astype(bool); v = q['vhat']; a = q['ahat_long']
    with np.errstate(invalid='ignore'):
        st = lf & (v <= 0.5); br = lf & (v > 0.5) & (a <= -1.0)
    ph = q['phase']
    return [np.ones(len(ph), bool), ~(st | br), br, st, ph == 0, ph == 1, ph == 2]


TSRC = [('N', 'cN'), ('NA', 'cNA'), ('AM', 'cA1'), ('CK3', 'cCK3'), ('Q', 'cQ')]


def tu_compute(K, log=print):
    t0 = time.time()
    names, data = tu_load()
    rs = RunSet(data, names)
    nr = len(names)
    srcs = [('F0', 'cF0'), ('E', 'cE')] + TSRC
    S = {}; Sg = {}
    for nm, k in srcs:
        Cl = [q[k] for q in rs.d]
        G = breakpoints(Cl)
        Tsum = 0; Tr = []; Tg = 0
        for q, C in zip(rs.d, Cl):
            c1 = L.clean_clear(q['clear']); sx = c1 > 0.; m = tu_masks(q)
            T = stats_curve(C, G, c1, sx, q['vbar'], q['des'], q['idx55'], m)
            Tsum = Tsum + T; Tr.append(T[:, 0, :].copy())
            Tg = Tg + stats_grid(C, GRID, c1, sx, q['vbar'], q['des'], q['idx55'], m)
        S[nm] = dict(Tsum=Tsum, Trun=np.stack(Tr), Tg=Tg)
    nms = [s for s, _ in TSRC]
    res = {}; extra = {}

    def pop(mi, grid=False):
        Td = {nm: (S[nm]['Tg'] if grid else S[nm]['Tsum'])[:, mi, :] for nm in ['F0', 'E'] + nms}
        return L.eval_scoring(Td, nms)
    ev = pop(0)
    res['TU.R'] = ev['denE'] / 201.
    for a in ['N', 'NA', 'AM', 'CK3']:
        res['TU.RR_' + a] = L.ratio(ev['D'][a], ev['denE'])
    extra['RR_Q'] = L.ratio(ev['D']['Q'], ev['denE']); extra['n'] = ev['n']
    for key, mi in (('TU.R_pre', 1), ('TU.R_brk', 2), ('TU.R_stop', 3)):
        e = pop(mi)
        res[key] = e['denE'] / 201. if e['n'] else float('nan')
    # grid points beside (compare with A9-5)
    grid = {}
    for lab, mi in (('all', 0), ('phase0', 4), ('phase1', 5), ('phase2', 6)):
        e = pop(mi, grid=True)
        grid[lab] = dict(n=e['n'], R_pp=e['denE'] / 201., **{'RR_' + a: L.ratio(e['D'][a], e['denE']) for a in nms})
    extra['grid'] = grid
    log('tu points %.1fs' % (time.time() - t0), flush=True)
    idx = np.random.default_rng(20261918).integers(0, nr, (20000, nr))[:K]
    cnt = np.zeros((K, nr))
    for b in range(K):
        cnt[b] = np.bincount(idx[b], minlength=nr)
    bs = ['F0', 'E', 'N', 'NA', 'AM', 'CK3']
    out = {k: np.full(K, np.nan) for k in ['denE', 'n', 'D_N', 'D_NA', 'D_AM', 'D_CK3']}
    flat = {s: S[s]['Trun'].reshape(nr, -1) for s in bs}
    Gt = max(S[s]['Trun'].shape[1] for s in bs)
    chunk = max(1, min(40, int(4e6 // (Gt * NS))))
    tb = time.time()
    for b0 in range(0, K, chunk):
        c = cnt[b0:b0 + chunk]
        Tb = {s: (c @ flat[s]).reshape(len(c), -1, NS) for s in bs}
        for j in range(len(c)):
            e = L.eval_scoring({s: Tb[s][j] for s in bs}, ['N', 'NA', 'AM', 'CK3'])
            i = b0 + j
            out['denE'][i] = e['denE']; out['n'][i] = e['n']
            for a in ['N', 'NA', 'AM', 'CK3']:
                out['D_' + a][i] = e['D'][a]
        if (b0 // chunk) % 100 == 0:
            log('tu boot %d/%d %.1fs' % (b0, K, time.time() - tb), flush=True)
    boot_s = time.time() - tb
    den = out['denE']; pos = den > 0
    res['TU.R.ci'] = L.pct(den / 201.)
    with np.errstate(divide='ignore', invalid='ignore'):
        for a in ['N', 'NA', 'AM', 'CK3']:
            res['TU.RR_%s.ci' % a] = L.pct(np.where(pos, out['D_' + a] / den, np.nan))
    extra.update(K=K, boot_seconds=boot_s, boot_ms_per_resample=1000 * boot_s / K, total_seconds=time.time() - t0)
    return res, out, extra
