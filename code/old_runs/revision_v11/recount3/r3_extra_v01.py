"""Recount3, supplementary numbers (class C of the comparison). Written AFTER RECOUNT3_RESULTS_v01.json was written and the first
program's four result files had been opened: these are numbers of the first program's files that the brief does not list, recomputed
with the same library (r3_lib_v01.py, unchanged). Their definitions were taken from the first program's two scripts
(rev_g_partial_oracle_draws_v01.py, rev_f2_braking_prior_score_v01.py), which were read at that point; the A6R code was not opened.

  item 1  phase 0 of Table S12b (mean, min, max, 5th and 95th percentile, share below zero over the 50 draws) and the value
          "of record" = the same construction with u = default_rng(20261118).random(9307), for all six populations
  item 4  RR0 (against the perfect oracle of the 3 s commitment) of the braking prediction at a0 = 1..7 with the interval of
          record, and den0 in decision-equivalents
  benign  the 20 benign-driving tuning runs scored as the first program does (arms F0, E, N, CK3, perfect oracle; populations all
          and ego moving): room, D, RR, RR0, zero-margin points, differences over the scale grid. Run bootstrap of the 20 runs:
          default_rng(20261125).integers(0, 20, size=(20000, 20)) (the form of the draw of record; the first program's own draw
          function sits in the A6R code, which was not opened - every resample gives 0, so the interval does not depend on it)
Usage: python -B -X utf8 r3_extra_v01.py  ->  r3_extra_v01_out.json"""
import json, time
import numpy as np
import r3_lib_v01 as R
L = R.L
SHARES = (0.25, 0.50, 0.75)
POPS6 = R.POPS + ('phase_weighted',)


def partial_rr(ds, seeds):
    """RR of the partial oracles for each seed: array (len(seeds), 3 shares, 6 populations)."""
    n_st = [d['n_stored'] for d in ds]; off = np.concatenate([[0], np.cumsum(n_st)])
    U = np.stack([np.random.default_rng(s).random(int(off[-1])) for s in seeds])
    NA = len(seeds) * len(SHARES)
    n = np.zeros(5); SF = np.zeros((5, R.NG, 3)); SE = np.zeros((5, R.NG, 3)); SP = np.zeros((NA, 5, R.NG, 3))
    for ri, d in enumerate(ds):
        safe = d['clear'] > 0.; masks = L.masks_std(d)
        bF, tF, cF = R.dec_stats(d, d['sel']['F0'], safe, safe); bE, tE, cE = R.dec_stats(d, d['sel']['E'], safe, safe)
        n += np.array([float(m.sum()) for m in masks])
        SF += R.sums(bF, tF, cF, masks); SE += R.sums(bE, tE, cE, masks)
        ue = U[:, off[ri]:off[ri + 1]][:, d['ev_all']]
        for i in range(len(seeds)):
            for si, p in enumerate(SHARES):
                m = (ue[i] < p)[None, :]
                SP[i * len(SHARES) + si] += R.sums(np.where(m, bE, bF), np.where(m, tE, tF), np.where(m, cE, cF), masks)
    S = np.concatenate([SF[:, None], SE[:, None], np.moveaxis(SP, 0, 1)], axis=1)[None]
    D, _ = R.evaluate_g(n[None], S)
    _, Dw = R.weighted(n[None], D)
    out = np.zeros((len(seeds), len(SHARES), 6))
    for i in range(len(seeds)):
        for si in range(len(SHARES)):
            col = 2 + i * len(SHARES) + si
            out[i, si, :5] = D[0, :, col] / D[0, :, 1]
            out[i, si, 5] = Dw[0, col] / Dw[0, 1]
    return out


def item1(ds):
    rr = partial_rr(ds, [20261200 + i for i in range(50)])
    rec = partial_rr(ds, [20261118])
    out = dict(phase0={}, of_record={}, check_against_results={})
    main = json.loads((R.HERE / 'RECOUNT3_RESULTS_v01.json').read_text(encoding='utf-8'))['item1_S12b']['share']
    worst = 0.
    for si, p in enumerate(SHARES):
        key = '%.2f' % p
        v = rr[:, si, 2]
        out['phase0'][key] = dict(mean=float(np.mean(v)), min=float(np.min(v)), max=float(np.max(v)), p5=float(np.percentile(v, 5)),
                                  p95=float(np.percentile(v, 95)), share_below_zero=float((v < 0).mean()), draws=[float(x) for x in v])
        out['of_record'][key] = {pn: float(rec[0, si, pi]) for pi, pn in enumerate(POPS6)}
        for pn, pi in (('all', 0), ('moving', 1), ('phase1', 3), ('phase2', 4), ('phase_weighted', 5)):
            worst = max(worst, float(np.max(np.abs(rr[:, si, pi] - np.array(main[key]['pops'][pn]['RR_draws'])))))
    out['check_against_results'] = dict(what='largest absolute difference of the 750 draw values recomputed here from those of RECOUNT3_RESULTS_v01.json',
                                        max_abs_diff=worst)
    return out


def item4(ds):
    arms = ('F0', 'E') + R.CK_ARMS; A = len(arms)
    rows = []
    for d in ds:
        safe = d['clear'] > 0.
        sels = [d['sel']['F0'], d['sel']['E']] + [L.select(d['ck'][a], d['idx55']) for a in R.CK_ARMS]
        rows.append(R.run_vector(d, sels, L.masks_std(d), safe, safe, with_oracle=True))
    M = np.stack(rows)
    nn, S, O = R.split(M.sum(0), 5, A)
    D0, _ = R.evaluate_g(nn, S, O)
    idx = L.draw_of_record()
    nb, Db, _ = R.boot_g(M, idx, 5, A)
    nt0, Dw0 = R.weighted(nn, D0); ntb, Dwb = R.weighted(nb, Db)
    out = dict(nboot=int(idx.shape[0]), den0_deceq={}, a0={})
    for pi, pn in enumerate(R.POPS):
        out['den0_deceq'][pn] = float(D0[0, pi, A] / 201. / 100. * nn[0, pi])
    out['den0_deceq']['phase_weighted'] = float(Dw0[0, A] / 201. / 100. * nt0[0])
    for a0 in range(1, 8):
        ai = 1 + a0; e = {}
        for pi, pn in enumerate(R.POPS):
            ci, lo = R.ci_ratio(Db[:, pi, ai], Db[:, pi, A])
            e[pn] = dict(RR0=float(D0[0, pi, ai] / D0[0, pi, A]), RR0_ci=ci, n_left_out=lo)
        ci, lo = R.ci_ratio(Dwb[:, ai], Dwb[:, A])
        e['phase_weighted'] = dict(RR0=float(Dw0[0, ai] / Dw0[0, A]), RR0_ci=ci, n_left_out=lo)
        out['a0'][str(a0)] = e
    return out


def benign():
    runs = []
    for f in sorted(L.STORED.glob('*.npz')):
        with np.load(f, allow_pickle=False) as z:
            m = json.loads(str(z['meta']))
            if m.get('family') != 'benign':
                continue
            ev = np.array(z['evaluated']).astype(bool)
            clear = np.asarray(z['clear'], float)[ev]
            d = dict(run=f.stem, n=int(ev.sum()), clear=np.where(np.isnan(clear), -1., clear), vbar=np.asarray(z['vbar'], float)[ev],
                     idx55=np.asarray(z['idx55'])[ev].astype(np.int64), des=np.asarray(z['des'], float)[ev], v0=np.asarray(z['v0'], float)[ev],
                     crit=dict(F0=np.asarray(z['cF0'], float)[ev], E=np.asarray(z['cE'], float)[ev], N=np.asarray(z['cN'], float)[ev]))
            if not np.all(d['des'] == float(m['desired'])):
                raise RuntimeError('%s: des differs from meta.desired' % f.stem)
            k = np.array(z['k'])
        with np.load(R.CK_DIR / (f.stem + '.npz'), allow_pickle=False) as z:
            if not np.array_equal(z['k'], k):
                raise RuntimeError('%s: k differs' % f.stem)
            d['crit']['CK3'] = np.asarray(z['cCK3'], float)[ev]
        runs.append(d)
    arms = ('F0', 'E', 'N', 'CK3'); A = len(arms)
    rows = []
    for d in runs:
        safe = d['clear'] > 0.
        masks = [np.ones(d['n'], bool), d['v0'] > 0.5]
        rows.append(R.run_vector(d, [L.select(d['crit'][a], d['idx55']) for a in arms], masks, safe, safe, with_oracle=True))
    M = np.stack(rows)
    nn, S, O = R.split(M.sum(0), 2, A)
    D0, info = R.evaluate_g(nn, S, O, want=True)
    idx = np.random.default_rng(20261125).integers(0, len(runs), size=(20000, len(runs)))
    nb, Db, _ = R.boot_g(M, idx, 2, A)
    out = dict(n_runs=len(runs), nboot=int(idx.shape[0]))

    def den(point, b):
        b = np.asarray(b, float)
        return dict(point=float(point), ci=L.pct(b), n_le0=int((~(b > 0)).sum()))

    def val(x):
        return float(x) if np.isfinite(x) else None

    for pi, pop in enumerate(('all', 'moving')):
        n = nn[0, pi]; dE = D0[0, pi, 1]; d0 = D0[0, pi, A]
        e = dict(n=float(n), R_pp=float(dE / 201.), denE=den(dE, Db[:, pi, 1]), den0=den(d0, Db[:, pi, A]),
                 denE_deceq=float(dE / 201. / 100. * n), den0_deceq=float(d0 / 201. / 100. * n), arms={}, zero_margin={})
        for a in ('N', 'CK3'):
            ai = arms.index(a); Da = D0[0, pi, ai]
            ciE, loE = R.ci_ratio(Db[:, pi, ai], Db[:, pi, 1]); ci0, lo0 = R.ci_ratio(Db[:, pi, ai], Db[:, pi, A])
            with np.errstate(invalid='ignore', divide='ignore'):
                rrE = val(Da / dE) if dE > 0 else None; rr0 = val(Da / d0) if d0 > 0 else None
            e['arms'][a] = dict(D_pp=float(Da / 201.), D_deceq=float(Da / 201. / 100. * n), D_deceq_ci=L.pct(Db[:, pi, ai] / 201. / 100. * nb[:, pi]),
                                RR=rrE, RR_ci=ciE, RR_left_out=loE, RR0=rr0, RR0_ci=ci0, RR0_left_out=lo0)
        for a in ('F0', 'CK3', 'E'):
            ai = arms.index(a)
            e['zero_margin'][a] = dict(caution_pct=val(info['C'][0, pi, ai, 0]), wrong_go_pct=val(info['W'][0, pi, ai, 0]),
                                       wrong_go_n=int(S[0, pi, ai, 0, 0]))
        cF = info['C'][0, pi, 0]; cK = info['C'][0, pi, 3]; wF = info['W'][0, pi, 0]; wK = info['W'][0, pi, 3]
        e['over_the_scale_grid'] = dict(mean_caution_diff_pp=float(np.nanmean(cK - cF)), max_caution_diff_pp=float(np.nanmax(cK - cF)),
                                        mean_wrong_go_diff_pp=float(np.nanmean(wK - wF)), max_wrong_go_F0=float(np.nanmax(wF)),
                                        max_wrong_go_CK3=float(np.nanmax(wK)))
        out[pop] = e
    return out


def item3_diag(ds):
    """Counts behind Table S24b that the brief does not ask for (diagnostics for the report, not compared with the first program):
    pairs whose stop ends after the 3 s window (late), pairs whose recording ends before the stop (censored), and the pairs that
    change their 2 m verdict between the 3 s window and the judgement until the stop ends."""
    c = dict(pairs=0, late=0, censored=0, censored_and_counted_safe_at_2m=0, safe_window_cache_unsafe_until_stop=0,
             unsafe_window_cache_safe_until_stop=0, clearX_above_own61=0, decisions_whose_first_safe_row_changes=0,
             decisions_with_a_censored_pair=0, own61_differs_from_cache_at_2m=0)
    for d in ds:
        with np.load(R.R2_OUT / (d['run'] + '.npz'), allow_pickle=False) as z:
            late = np.asarray(z['late_' + R.KEY])[d['ev_all']].astype(bool); cens = np.asarray(z['cens_' + R.KEY])[d['ev_all']].astype(bool)
        sx = d['clearX'] > 2.0; sr = d['rs'] > 2.0; s6 = d['clear61'] > 2.0
        c['pairs'] += int(sx.size); c['late'] += int(late.sum()); c['censored'] += int(cens.sum())
        c['censored_and_counted_safe_at_2m'] += int((cens & sx).sum())
        c['safe_window_cache_unsafe_until_stop'] += int((sr & ~sx).sum()); c['unsafe_window_cache_safe_until_stop'] += int((~sr & sx).sum())
        c['clearX_above_own61'] += int((d['clearX'] > d['clear61']).sum())
        c['own61_differs_from_cache_at_2m'] += int((s6 != sr).sum())
        fx = np.where(sx.any(1), sx.argmax(1), d['idx55']); fr = np.where(sr.any(1), sr.argmax(1), d['idx55'])
        c['decisions_whose_first_safe_row_changes'] += int((fx != fr).sum())
        c['decisions_with_a_censored_pair'] += int(cens.any(1).sum())
        d['clearXw'] = np.where(cens & sx, -1., d['clearX'])              # worst case: a censored pair counted safe becomes unsafe
    # sensitivity (points only): Table S24b with every censored pair that was counted safe at 2 m counted unsafe instead
    A7 = len(L.ARMS); AI = {a: i for i, a in enumerate(L.ARMS)}
    sens = {}
    for name, field in (('as_computed', 'clearX'), ('censored_pairs_unsafe', 'clearXw')):
        M = np.stack([R.run_vector(d, [d['sel'][a] for a in L.ARMS], L.masks_std(d), d[field] > 2.0, d['clear'] > 2.0) for d in ds])
        nn, S, O = R.split(M.sum(0), 5, A7)
        D0, _ = R.evaluate_g(nn, S, O)
        nt, Dw = R.weighted(nn, D0)
        e = {}
        for pn, n_, D_ in (('all', nn[0, 0], D0[0, 0]), ('moving', nn[0, 1], D0[0, 1]), ('phase_weighted', nt[0], Dw[0])):
            e[pn] = dict(den0_pp=float(D_[A7] / 201.), den0_deceq=float(D_[A7] / 201. / 100. * n_),
                         **{'RR0_' + a: float(D_[AI[a]] / D_[A7]) for a in ('E', 'N', 'NA', 'CK3', 'AM')})
        sens[name] = e
    c['sensitivity_points'] = sens
    return c


def main():
    t0 = time.time()
    ds = R.load_eval_runs()
    res = dict(program='recount3 supplementary: r3_extra_v01.py (written after the first program\'s files were opened)',
               written=time.strftime('%Y-%m-%d %H:%M:%S'))
    res['item1'] = item1(ds)
    res['item4'] = item4(ds)
    res['benign'] = benign()
    res['item3_diagnostics'] = item3_diag(ds)
    res['seconds'] = time.time() - t0
    L.jdump(res, R.HERE / 'r3_extra_v01_out.json')
    print('r3_extra_v01 done, %.0f s; item 1 draws against the results file: max abs diff %.3e' % (
        time.time() - t0, res['item1']['check_against_results']['max_abs_diff']))


if __name__ == '__main__':
    main()
