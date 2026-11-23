"""Recount3 (second program): the cCK3 identity check and items 1-4 of RECOUNT3_BRIEF_v01.md.
Usage: python -B -X utf8 r3_items_v01.py            (writes RECOUNT3_RESULTS_v01.json)
       python -B -X utf8 r3_items_v01.py quick      (first 400 rows of the draw of record; writes ..._quick.json; test only)
Does not open revision_v11\\analysis except the input folder analysis\\out\\ck."""
import json, sys, time
import numpy as np
import r3_lib_v01 as R
L = R.L

LOG = R.HERE / 'r3_items_v01_log.txt'
QUICK = 'quick' in sys.argv
NB = 400 if QUICK else L.NBOOT
A7 = len(L.ARMS)
AI = {a: i for i, a in enumerate(L.ARMS)}


def ratio(num, den):
    with np.errstate(invalid='ignore', divide='ignore'):
        return np.asarray(num, float) / np.asarray(den, float)


# ------------------------------------------------------------------------------------------------ identity check of cCK3
def identity_check():
    out = dict(what='ck\\<run>.npz cCK3 against A4\\fit\\extract\\<run>.npz cCK3, the 35 evaluation runs', runs={})
    tot = dict(runs=0, runs_bit_identical=0, elements=0, elements_differing_bits=0, elements_evaluated=0,
               elements_evaluated_differing_bits=0, nan_in_ck=0, nan_in_extract=0, max_abs_diff=0.)
    for run in L.RUNS:
        with np.load(R.CK_DIR / (run + '.npz'), allow_pickle=False) as z:
            a = np.array(z['cCK3']); ka = np.array(z['k'])
        with np.load(L.EXTRACT / (run + '.npz'), allow_pickle=False) as z:
            b = np.array(z['cCK3']); kb = np.array(z['k'])
        with np.load(L.STORED / (run + '.npz'), allow_pickle=False) as z:
            ev = np.array(z['evaluated']).astype(bool)
        same_form = (a.shape == b.shape) and (a.dtype == b.dtype)
        bit = bool(same_form and a.tobytes() == b.tobytes())
        e = dict(shape_ck=list(a.shape), shape_extract=list(b.shape), dtype_ck=str(a.dtype), dtype_extract=str(b.dtype),
                 k_equal=bool(np.array_equal(ka, kb)), bit_identical=bit)
        if same_form and a.dtype == np.float64:
            ne = np.ascontiguousarray(a).view(np.uint64) != np.ascontiguousarray(b).view(np.uint64)
            e['elements'] = int(ne.size); e['elements_differing_bits'] = int(ne.sum())
            e['elements_evaluated'] = int(ne[ev].size); e['elements_evaluated_differing_bits'] = int(ne[ev].sum())
            e['nan_in_ck'] = int(np.isnan(a).sum()); e['nan_in_extract'] = int(np.isnan(b).sum())
            with np.errstate(invalid='ignore'):
                dd = np.abs(a - b)
            e['max_abs_diff'] = float(np.nanmax(dd)) if np.isfinite(dd).any() else 0.
            for kk in ('elements', 'elements_differing_bits', 'elements_evaluated', 'elements_evaluated_differing_bits', 'nan_in_ck', 'nan_in_extract'):
                tot[kk] += e[kk]
            tot['max_abs_diff'] = max(tot['max_abs_diff'], e['max_abs_diff'])
        tot['runs'] += 1; tot['runs_bit_identical'] += int(bit)
        out['runs'][run] = e
    out['total'] = tot
    out['holds'] = bool(tot['runs'] == 35 and tot['runs_bit_identical'] == 35)
    L.log('identity check cCK3: %d / %d runs bit-identical; elements differing %d of %d' % (
        tot['runs_bit_identical'], tot['runs'], tot['elements_differing_bits'], tot['elements']), file=LOG)
    return out


# ------------------------------------------------------------------------------------------------ item 1 (Table S12b)
SHARES = (0.25, 0.50, 0.75)
NDRAW = 50
POPS1 = ('all', 'moving', 'phase1', 'phase2', 'phase_weighted')


def item1(ds):
    t0 = time.time()
    n_stored = [d['n_stored'] for d in ds]
    tot = int(sum(n_stored))
    if tot != 9307:
        raise RuntimeError('stored decisions: %d, the brief says 9307' % tot)
    off = np.concatenate([[0], np.cumsum(n_stored)])
    U = np.stack([np.random.default_rng(20261200 + i).random(tot) for i in range(NDRAW)])        # (50, 9307)
    Pm = 5; NA = NDRAW * len(SHARES)
    n = np.zeros(Pm); SF = np.zeros((Pm, R.NG, 3)); SE = np.zeros((Pm, R.NG, 3)); SP = np.zeros((NA, Pm, R.NG, 3))
    took = np.zeros((NDRAW, len(SHARES)))
    for ri, d in enumerate(ds):
        safe = d['clear'] > 0.
        masks = L.masks_std(d)
        bF, tF, cF = R.dec_stats(d, d['sel']['F0'], safe, safe)
        bE, tE, cE = R.dec_stats(d, d['sel']['E'], safe, safe)
        n += np.array([float(m.sum()) for m in masks])
        SF += R.sums(bF, tF, cF, masks); SE += R.sums(bE, tE, cE, masks)
        ue = U[:, off[ri]:off[ri + 1]][:, d['ev_all']]                                           # (50, n evaluated)
        # check: the partial arm built from critical scales (cE where u < p, cF0 elsewhere) selects the same rows
        for i in range(NDRAW):
            for si, p in enumerate(SHARES):
                m = ue[i] < p
                took[i, si] += m.sum()
                SP[i * len(SHARES) + si] += R.sums(np.where(m[None, :], bE, bF), np.where(m[None, :], tE, tF), np.where(m[None, :], cE, cF), masks)
        if ri == 0:
            m = ue[0] < 0.5
            crit = np.where(m[:, None], d['crit']['E'], d['crit']['F0'])
            sel = L.select(crit, d['idx55'])
            if not np.array_equal(sel, np.where(m[None, :], d['sel']['E'], d['sel']['F0'])):
                raise RuntimeError('partial-oracle selection: the two constructions differ')
    S = np.concatenate([SF[:, None], SE[:, None], np.moveaxis(SP, 0, 1)], axis=1)[None]             # (1, P, 2 + 150, G, 3)
    D, info = R.evaluate_g(n[None], S)
    nt, Dw = R.weighted(n[None], D)
    out = dict(item='Table S12b: partial oracles over 50 draws (3 s commitment, step frontier, points)',
               seeds='20261200 + i, i = 0..49', n_stored=tot, n_evaluated=int(n[0]),
               n={pn: float(n[pi]) for pi, pn in enumerate(R.POPS)}, share={})
    out['n']['phase_weighted'] = float(nt[0])
    out['denE'] = {pn: float(D[0, pi, 1]) for pi, pn in enumerate(R.POPS)}
    out['denE']['phase_weighted'] = float(Dw[0, 1])
    out['undefined_frontier_levels'] = {pn: bool(info['nanlev'][0, pi]) for pi, pn in enumerate(R.POPS)}
    pidx = dict(all=0, moving=1, phase1=3, phase2=4)
    for si, p in enumerate(SHARES):
        cols = 2 + np.arange(NDRAW) * len(SHARES) + si
        e = dict(evaluated_decisions_on_the_oracle_mean=float(took[:, si].mean()), pops={})
        for pn in POPS1:
            if pn == 'phase_weighted':
                rr = Dw[0, cols] / Dw[0, 1]; dd = Dw[0, cols]
            else:
                rr = D[0, pidx[pn], cols] / D[0, pidx[pn], 1]; dd = D[0, pidx[pn], cols]
            e['pops'][pn] = dict(RR_mean=float(np.mean(rr)), RR_min=float(np.min(rr)), RR_max=float(np.max(rr)),
                                 RR_draws=[float(x) for x in rr], D_draws=[float(x) for x in dd])
        out['share']['%.2f' % p] = e
    out['seconds'] = time.time() - t0
    L.log('item 1 done %.0f s' % (time.time() - t0), file=LOG)
    return out


# ------------------------------------------------------------------------------------------------ item 2 (Table S17, subsampling)
STATS = ('R', 'RR_N', 'RR_NA', 'RR_AM', 'RR_CK3', 'RR_Q', 'RR0_CK3', 'RR_NA_minus_RR_N')


def stat_values(D, strict):
    """D (B, 8): columns ARMS then O. strict=False: plain quotients (non-finite only at a zero or undefined denominator);
    strict=True: NaN wherever the statistic's denominator is not positive."""
    D = np.atleast_2d(D)
    dE = D[:, 1]; d0 = D[:, A7]
    out = dict(R=dE / 201.)
    for a in ('N', 'NA', 'AM', 'CK3', 'Q'):
        out['RR_' + a] = ratio(D[:, AI[a]], dE)
    out['RR0_CK3'] = ratio(D[:, AI['CK3']], d0)
    out['RR_NA_minus_RR_N'] = ratio(D[:, AI['NA']], dE) - ratio(D[:, AI['N']], dE)
    if strict:
        okE = dE > 0; ok0 = d0 > 0
        for k in out:
            if k == 'R':
                continue
            out[k] = np.where(ok0 if k == 'RR0_CK3' else okE, out[k], np.nan)
    return out


def item2(ds):
    t0 = time.time()
    M = np.stack([R.run_vector(d, [d['sel'][a] for a in L.ARMS], L.masks_all(d), d['clear'] > 0., d['clear'] > 0.) for d in ds])
    nn, S, O = R.split(M.sum(0), 1, A7)
    D0, info0 = R.evaluate_g(nn, S, O)
    theta = {k: float(v[0]) for k, v in stat_values(D0[:, 0], False).items()}
    out = dict(item='Table S17: subsampling without replacement (m of 35 runs, 5000 subsamples each, one stream 20261124)',
               theta=theta, n_full=float(nn[0, 0]), denE_full=float(D0[0, 0, 1]), den0_full=float(D0[0, 0, A7]), m={})
    rng = np.random.default_rng(20261124)
    for m in (15, 20, 25):
        idx = np.stack([rng.permutation(35)[:m] for _ in range(5000)])
        if not all(len(set(r.tolist())) == m for r in idx[:50]):
            raise RuntimeError('subsample with a repeated run')
        nb, Db, nl = R.boot_g(M, idx, 1, A7, logfile=LOG, tag='S17 m=%d' % m)
        sv = stat_values(Db[:, 0], False); svs = stat_values(Db[:, 0], True)
        f = np.sqrt(1. - m / 35.)
        e = dict(f=float(f), n_subsamples=int(idx.shape[0]), n_denE_not_positive=int((~(Db[:, 0, 1] > 0)).sum()),
                 n_den0_not_positive=int((~(Db[:, 0, A7] > 0)).sum()), n_undefined_frontier=int(nl[:, 0].sum()),
                 first_subsample=[int(x) for x in idx[0]], stats={})
        for s in STATS:
            root = np.sqrt(m) * (sv[s] - theta[s])
            fin = np.isfinite(root)
            ql, qh = np.percentile(root[fin], [2.5, 97.5])
            lo = theta[s] - qh / (f * np.sqrt(35.)); hi = theta[s] - ql / (f * np.sqrt(35.))
            roots = np.sqrt(m) * (svs[s] - theta[s]); fs = np.isfinite(roots)
            qls, qhs = np.percentile(roots[fs], [2.5, 97.5])
            e['stats'][s] = dict(theta=theta[s], ql=float(ql), qh=float(qh), lo=float(lo), hi=float(hi), n_finite=int(fin.sum()),
                                 lo_positive_denominator_only=float(theta[s] - qhs / (f * np.sqrt(35.))),
                                 hi_positive_denominator_only=float(theta[s] - qls / (f * np.sqrt(35.))), n_finite_positive_denominator_only=int(fs.sum()))
        out['m'][str(m)] = e
    out['seconds'] = time.time() - t0
    L.log('item 2 done %.0f s' % (time.time() - t0), file=LOG)
    return out


# ------------------------------------------------------------------------------------------------ item 3 (Table S24b)
GAP = 2.0
ARMS3 = ('E', 'N', 'NA', 'CK3', 'AM', 'Q')


def item3(ds):
    t0 = time.time()
    M = np.stack([R.run_vector(d, [d['sel'][a] for a in L.ARMS], L.masks_std(d), d['clearX'] > GAP, d['clear'] > GAP) for d in ds])
    nn, S, O = R.split(M.sum(0), 5, A7)
    D0, info0 = R.evaluate_g(nn, S, O, want=True)
    # cross-check of evaluate_g against the imported library's own evaluation (same arms, same statistics)
    ML = np.stack([L.run_row(d, L.masks_std(d), d['clearX'] > GAP, d['clear'] > GAP, False) for d in ds])
    nL, DL, _ = L.evaluate(ML.sum(0), 5)
    lib_same = bool(np.array_equal(ML, M) and np.array_equal(DL, D0, equal_nan=True))
    idx = L.draw_of_record()[:NB]
    nb, Db, nlb = R.boot_g(M, idx, 5, A7, logfile=LOG, tag='S24b bootstrap')
    nt0, Dw0 = R.weighted(nn, D0); ntb, Dwb = R.weighted(nb, Db)
    out = dict(item='Table S24b: 2 m standstill gap, wrong go by the clearance judged until the stop ends (tau 0.75 s, 6 m/s2)',
               nboot=int(idx.shape[0]), gap_m=GAP, evaluate_g_equals_rc_lib_evaluate=lib_same, pops={})

    def table(n0, D0p, nbp, Dbp):
        den0 = D0p[A7]; b0 = Dbp[:, A7]; denE = D0p[1]; bE = Dbp[:, 1]
        e = dict(n=float(n0))
        ci, lo = R.ci_plain(b0 / 201.)
        e['den0_pp'] = dict(point=float(den0 / 201.), ci=ci, n_left_out=lo)
        ci, lo = R.ci_plain(b0 / 201. / 100. * nbp)
        e['den0_deceq'] = dict(point=float(den0 / 201. / 100. * n0), ci=ci, n_left_out=lo)
        ci, lo = R.ci_plain(bE / 201.)
        e['denE_pp'] = dict(point=float(denE / 201.), ci=ci, n_left_out=lo)
        e['den0_sum'] = float(den0); e['denE_sum'] = float(denE)
        e['share_den0_not_positive'] = float((~(b0 > 0)).mean())
        for a in ARMS3:
            ci, lo = R.ci_ratio(Dbp[:, AI[a]], b0)
            e['RR0_' + a] = dict(point=float(D0p[AI[a]] / den0) if den0 != 0 else None, ci=ci, n_left_out=lo)
            e['D_' + a] = float(D0p[AI[a]])
        return e

    for pi, pn in enumerate(R.POPS):
        e = table(nn[0, pi], D0[0, pi], nb[:, pi], Db[:, pi])
        e['undefined_frontier_levels_point'] = bool(info0['nanlev'][0, pi]); e['resamples_with_undefined_frontier'] = int(nlb[:, pi].sum())
        e['F0_zero_margin'] = dict(caution_pct=float(info0['c0'][0, pi]), wrong_go_pct=float(info0['w0'][0, pi]))
        e['O_point'] = dict(caution_pct=float(info0['cO'][0, pi]), wrong_go_pct=float(info0['wO'][0, pi]))
        e['last_level'] = float(info0['hi'][0, pi])
        out['pops'][pn] = e
    out['pops']['phase_weighted'] = table(nt0[0], Dw0[0], ntb, Dwb)
    # counts over evaluated decisions
    c = dict(evaluated_decisions=0, decision_row_pairs=0, decisions_without_row_safe_until_stop=0, pairs_unsafe_window_cache=0,
             pairs_unsafe_until_stop=0, pairs_unsafe_window_own61=0, decisions_without_row_safe_window_cache=0,
             decisions_without_truly_safe_row_3s=0, pairs_not_truly_safe_3s=0, nan_clearX=0, nan_cache=0, pairs_late=0)
    for d in ds:
        sx = d['clearX'] > GAP; sr = d['rs'] > GAP; s6 = d['clear61'] > GAP; s3 = d['clear'] > GAP
        c['evaluated_decisions'] += d['n']; c['decision_row_pairs'] += int(sx.size)
        c['decisions_without_row_safe_until_stop'] += int((~sx.any(1)).sum())
        c['pairs_unsafe_window_cache'] += int((~sr).sum()); c['pairs_unsafe_until_stop'] += int((~sx).sum())
        c['pairs_unsafe_window_own61'] += int((~s6).sum())
        c['decisions_without_row_safe_window_cache'] += int((~sr.any(1)).sum())
        c['decisions_without_truly_safe_row_3s'] += int((~s3.any(1)).sum()); c['pairs_not_truly_safe_3s'] += int((~s3).sum())
        c['nan_clearX'] += d['clearX_nan_eval']; c['nan_cache'] += d['n_nan_rs_eval']
    out['counts'] = c
    out['seconds'] = time.time() - t0
    L.log('item 3 done %.0f s' % (time.time() - t0), file=LOG)
    return out


# ------------------------------------------------------------------------------------------------ item 4 (Table S25, benign check)
def item4(ds):
    t0 = time.time()
    arms = ('F0', 'E') + R.CK_ARMS
    A = len(arms)
    rows = []
    for d in ds:
        safe = d['clear'] > 0.
        sels = [d['sel']['F0'], d['sel']['E']] + [L.select(d['ck'][a], d['idx55']) for a in R.CK_ARMS]
        rows.append(R.run_vector(d, sels, L.masks_std(d), safe, safe, with_oracle=False))
    M = np.stack(rows)
    nn, S, _ = R.split(M.sum(0), 5, A, with_oracle=False)
    D0, info0 = R.evaluate_g(nn, S, None, want=True)
    idx = L.draw_of_record()[:NB]
    nb, Db, nlb = R.boot_g(M, idx, 5, A, with_oracle=False, logfile=LOG, tag='S25 bootstrap')
    nt0, Dw0 = R.weighted(nn, D0); ntb, Dwb = R.weighted(nb, Db)
    out = dict(item='Table S25: braking prediction at a0 = 1..7 m/s2 (3 s commitment, step frontier)', nboot=int(idx.shape[0]),
               nan_critical_scales_evaluated={a: int(sum(d['ck_nan_eval'][a] for d in ds)) for a in R.CK_ARMS},
               n={pn: float(nn[0, pi]) for pi, pn in enumerate(R.POPS)}, a0={}, zero_margin={})
    out['n']['phase_weighted'] = float(nt0[0])
    out['denE'] = {pn: float(D0[0, pi, 1]) for pi, pn in enumerate(R.POPS)}; out['denE']['phase_weighted'] = float(Dw0[0, 1])
    out['R_pp'] = {k: v / 201. for k, v in out['denE'].items()}
    out['resamples_with_undefined_frontier'] = {pn: int(nlb[:, pi].sum()) for pi, pn in enumerate(R.POPS)}
    for a0 in range(1, 8):
        ai = 1 + a0
        e = {}
        for pi, pn in enumerate(R.POPS):
            ci, lo = R.ci_ratio(Db[:, pi, ai], Db[:, pi, 1])
            cid, _ = R.ci_plain(Db[:, pi, ai] / 201. / 100. * nb[:, pi])
            e[pn] = dict(RR=float(D0[0, pi, ai] / D0[0, pi, 1]), RR_ci=ci, n_left_out=lo, D_sum=float(D0[0, pi, ai]),
                         D_deceq=float(D0[0, pi, ai] / 201. / 100. * nn[0, pi]), D_deceq_ci=cid)
        ci, lo = R.ci_ratio(Dwb[:, ai], Dwb[:, 1])
        cid, _ = R.ci_plain(Dwb[:, ai] / 201. / 100. * ntb)
        e['phase_weighted'] = dict(RR=float(Dw0[0, ai] / Dw0[0, 1]), RR_ci=ci, n_left_out=lo, D_sum=float(Dw0[0, ai]),
                                   D_deceq=float(Dw0[0, ai] / 201. / 100. * nt0[0]), D_deceq_ci=cid)
        out['a0'][str(a0)] = e
    for ai, a in enumerate(arms):
        if a == 'E':
            continue
        out['zero_margin'][a] = dict(caution_pct=float(info0['C'][0, 0, ai, 0]), wrong_go_pct=float(info0['W'][0, 0, ai, 0]),
                                     wrong_go_decisions=float(S[0, 0, ai, 0, 0]), truly_safe_selections=float(S[0, 0, ai, 0, 2]))
    # the CK3 arm of the ck folder against the CK3 arm of the extraction (the arm of record)
    same = all(np.array_equal(L.select(d['ck']['CK3'], d['idx55']), d['sel']['CK3']) for d in ds)
    out['ck3_selection_equals_extract_ck3'] = bool(same)
    out['seconds'] = time.time() - t0
    L.log('item 4 (Table S25) done %.0f s' % (time.time() - t0), file=LOG)
    return out


def benign_check():
    t0 = time.time()
    runs = []
    for f in sorted(L.STORED.glob('*.npz')):
        with np.load(f, allow_pickle=False) as z:
            m = json.loads(str(z['meta']))
        if m.get('family') == 'benign':
            runs.append((f.stem, m.get('set')))
    g1_grid = float(L.GRID[np.argmin(np.abs(L.GRID - 1.))])
    tot = dict(evaluated_decisions=0, stored_decisions=0, differ_g0=0, differ_g1=0, differ_g1_gridvalue=0, wrong_go_g0_CK3=0, wrong_go_g0_F0=0,
               wrong_go_g1_CK3=0, wrong_go_g1_F0=0, nan_cCK3_evaluated=0, nan_cF0_evaluated=0, nan_clear_evaluated=0,
               fallback_selected_g1_CK3=0, fallback_selected_g1_F0=0)
    per = {}
    for run, st in runs:
        with np.load(L.STORED / (run + '.npz'), allow_pickle=False) as z:
            ev = np.array(z['evaluated']).astype(bool); k = np.array(z['k'])
            clear = np.asarray(z['clear'], float)[ev]; idx55 = np.asarray(z['idx55'])[ev].astype(np.int64)
            cF = np.asarray(z['cF0'], float)[ev]
        with np.load(R.CK_DIR / (run + '.npz'), allow_pickle=False) as z:
            if not np.array_equal(z['k'], k):
                raise RuntimeError('%s: k of the ck folder differs from the stored k' % run)
            cK = np.asarray(z['cCK3'], float)[ev]
        n = int(ev.sum()); ar = np.arange(n)
        nan_clear = int(np.isnan(clear).sum())
        clear = np.where(np.isnan(clear), -1., clear)
        e = dict(set=st, evaluated_decisions=n, stored_decisions=int(ev.size), nan_cCK3_evaluated=int(np.isnan(cK).sum()),
                 nan_cF0_evaluated=int(np.isnan(cF).sum()), nan_clear_evaluated=nan_clear)
        sK0 = R.select_at(cK, idx55, 0.); sF0 = R.select_at(cF, idx55, 0.)
        sK1 = R.select_at(cK, idx55, 1.); sF1 = R.select_at(cF, idx55, 1.)
        sK1g = R.select_at(cK, idx55, g1_grid); sF1g = R.select_at(cF, idx55, g1_grid)
        e['differ_g0'] = int((sK0 != sF0).sum()); e['differ_g1'] = int((sK1 != sF1).sum()); e['differ_g1_gridvalue'] = int((sK1g != sF1g).sum())
        e['wrong_go_g0_CK3'] = int((clear[ar, sK0] <= 0).sum()); e['wrong_go_g0_F0'] = int((clear[ar, sF0] <= 0).sum())
        e['wrong_go_g1_CK3'] = int((clear[ar, sK1] <= 0).sum()); e['wrong_go_g1_F0'] = int((clear[ar, sF1] <= 0).sum())
        e['fallback_selected_g1_CK3'] = int((~(cK >= 1.).any(1)).sum()); e['fallback_selected_g1_F0'] = int((~(cF >= 1.).any(1)).sum())
        for kk in tot:
            tot[kk] += e[kk]
        per[run] = e
    out = dict(item='benign-driving tuning runs: braking prediction (cCK3, ck folder) against the class average (cF0)',
               n_runs=len(runs), sets=sorted(set(s for _, s in runs)), g1_grid_value=g1_grid, g1_grid_value_is_exactly_1=bool(g1_grid == 1.0),
               total=tot, per_run=per, seconds=time.time() - t0)
    L.log('benign check done: %d runs, %d evaluated decisions, differ g0 %d, g1 %d, wrong go g0 CK3 %d F0 %d' % (
        len(runs), tot['evaluated_decisions'], tot['differ_g0'], tot['differ_g1'], tot['wrong_go_g0_CK3'], tot['wrong_go_g0_F0']), file=LOG)
    return out


def main():
    t0 = time.time()
    L.log('r3_items_v01 start, nboot %d, numpy %s' % (NB, np.__version__), file=LOG)
    res = dict(program='recount3: r3_items_v01.py + r3_lib_v01.py (imports revision_v11\\recount\\rc_lib_v01.py)',
               written=time.strftime('%Y-%m-%d %H:%M:%S'), numpy=np.__version__, nboot=NB,
               bootstrap_of_record='numpy.random.default_rng(20261113).integers(0, 35, size=(20000, 35))')
    res['cck3_identity'] = identity_check()
    ds = R.load_eval_runs()
    res['data'] = dict(runs=len(ds), stored_decisions=int(sum(d['n_stored'] for d in ds)), evaluated_decisions=int(sum(d['n'] for d in ds)),
                       nan_clear_evaluated=int(sum(d['n_nan_clear_eval'] for d in ds)), nan_cache_evaluated=int(sum(d['n_nan_rs_eval'] for d in ds)),
                       nan_clearX_evaluated=int(sum(d['clearX_nan_eval'] for d in ds)),
                       phase_counts_evaluated={str(p): int(sum((d['phase'] == p).sum() for d in ds)) for p in range(4)})
    res['item1_S12b'] = item1(ds)
    res['item2_S17'] = item2(ds)
    res['item3_S24b'] = item3(ds)
    res['item4_S25'] = item4(ds)
    res['item4_benign'] = benign_check()
    res['seconds'] = time.time() - t0
    L.jdump(res, R.HERE / ('RECOUNT3_RESULTS_v01%s.json' % ('_quick' if QUICK else '')))
    L.log('r3_items_v01 end, %.0f s' % (time.time() - t0), file=LOG)


if __name__ == '__main__':
    main()
