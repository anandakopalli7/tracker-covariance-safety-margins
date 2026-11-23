"""Recount (second program): items 1, 2, 3, 5 (all but the double bootstrap) and 6 of RECOUNT_BRIEF_v01.md.
Usage: python -B -X utf8 rc_items_v01.py 1 2 3 5 6      (each item writes RECOUNT_item<k>_v01.json when it finishes)
       add 'quick' to use the first 400 rows of each draw (test only; the files then carry nboot = 400)."""
import json, sys, time
import numpy as np
import rc_lib_v01 as L

LOG = L.HERE / 'rc_items_v01_log.txt'
A = len(L.ARMS); AI = {a: i for i, a in enumerate(L.ARMS)}; AI['O'] = A
FIVE = ('N', 'NA', 'AM', 'CK3', 'Q')
QUICK = 'quick' in sys.argv
NB = 400 if QUICK else L.NBOOT


def entry(point, boot=None, den=None):
    """point and, if boot values are given, the 95% percentile interval (resamples with den <= 0 left out and counted)."""
    e = dict(point=None if point is None else float(point))
    if boot is not None:
        boot = np.asarray(boot, float)
        keep = np.isfinite(boot)
        if den is not None:
            keep &= np.isfinite(den) & (np.asarray(den, float) > 0)
        e['ci'] = L.pct(boot[keep]); e['n_left_out'] = int((~keep).sum())
    return e


def ratio(num, den):
    with np.errstate(invalid='ignore', divide='ignore'):
        return np.asarray(num, float) / np.asarray(den, float)


def table_one(n0, D0, nb=None, Db=None, arms=FIVE):
    """One population: n0 scalar, D0 (A+1,) point; nb (B,), Db (B, A+1) resamples."""
    hb = Db is not None
    e = dict(n=entry(n0, nb if hb else None))
    denE = D0[1]; den0 = D0[A]
    bE = Db[:, 1] if hb else None; b0 = Db[:, A] if hb else None
    e['denE'] = entry(denE, bE)
    e['R_pp'] = entry(denE / 201, bE / 201 if hb else None)
    e['denE_deceq'] = entry(denE / 201 / 100 * n0, bE / 201 / 100 * nb if hb else None)
    e['den0'] = entry(den0, b0)
    e['den0_pp'] = entry(den0 / 201, b0 / 201 if hb else None)
    e['den0_deceq'] = entry(den0 / 201 / 100 * n0, b0 / 201 / 100 * nb if hb else None)
    e['RR0_E'] = entry(denE / den0, ratio(bE, b0) if hb else None, b0)
    if hb:
        e['share_denE_le0'] = float((~(bE > 0)).mean()); e['share_den0_le0'] = float((~(b0 > 0)).mean())
    for a in arms:
        Da = D0[AI[a]]; ba = Db[:, AI[a]] if hb else None
        e['D_' + a] = entry(Da, ba)
        e['RR_' + a] = entry(Da / denE, ratio(ba, bE) if hb else None, bE)
        e['RR0_' + a] = entry(Da / den0, ratio(ba, b0) if hb else None, b0)
    return e


def run_config(ds, mask_fn, Pm, scoring, gap, signed, tag, idx=None):
    M = L.build_M(ds, mask_fn, scoring, gap, signed)
    n0, D0, nl0 = L.evaluate(M.sum(0), Pm)
    if idx is None:
        idx = L.draw_of_record()[:NB]
    nb, Db, nlb = L.boot(M, idx, Pm, logfile=LOG, tag=tag)
    return M, n0[0], D0[0], nl0[0], nb, Db, nlb


# ------------------------------------------------------------------------------------------------ item 1 (R11)
def item1(ds):
    t0 = time.time()
    M, n0, D0, nl0, nb, Db, nlb = run_config(ds, L.masks_std, 5, 'W1', 0., True, 'R11 signed')
    out = dict(item='R11 signed caution, 3 s commitment', nboot=int(nb.shape[0]), pops={})
    for pi, pn in enumerate(L.POPS_STD):
        out['pops'][pn] = table_one(n0[pi], D0[pi], nb[:, pi], Db[:, pi])
        out['pops'][pn]['levels_with_undefined_frontier_point'] = int(nl0[pi])
        out['pops'][pn]['resamples_with_undefined_frontier'] = int((nlb[:, pi] > 0).sum())
    nt0, Dw0 = L.weighted(n0[None], D0[None]); ntb, Dwb = L.weighted(nb, Db)
    out['pops']['phase_weighted'] = table_one(nt0[0], Dw0[0], ntb, Dwb)
    # diagnostics of the signed caution axis
    _, _, _, cur = L.evaluate(M.sum(0), 5, want_curves=True)
    n_, S_, O_ = L.unpack(np.atleast_2d(M.sum(0)), 5)
    diag = {}
    for pi, pn in enumerate(L.POPS_STD):
        diag[pn] = dict(decisions_with_a_truly_safe_row=float(S_[0, pi, 0, 0, 2]), n=float(n_[0, pi]),
                        F0_zero_margin_signed_caution_pct=float(cur[pi]['C'][0, 0, 0]), level_first=float(cur[pi]['lev'][0, 0]),
                        level_last=float(cur[pi]['lev'][0, -1]), oracle_caution_pct=float(cur[pi]['cO'][0]),
                        oracle_wrong_go_pct=float(cur[pi]['wO'][0]))
    out['diagnostics'] = diag
    out['seconds'] = time.time() - t0
    L.jdump(out, L.HERE / ('RECOUNT_item1_v01%s.json' % ('_quick' if QUICK else '')))
    L.log('item 1 done %.0f s' % (time.time() - t0), file=LOG)


# ------------------------------------------------------------------------------------------------ item 2 (R17)
def item2(ds):
    t0 = time.time()
    out = dict(item='R17 standstill gap 2 m', nboot=NB, gap_m=2.0, scorings={})
    for sc, name in (('W1', 'a_3s_commitment'), ('RS', 'b_reaction_and_stop_t0p75_a6p0')):
        M, n0, D0, nl0, nb, Db, nlb = run_config(ds, L.masks_std, 5, sc, 2.0, False, 'R17 ' + sc)
        o = dict(pops={})
        for pi, pn in enumerate(L.POPS_STD):
            o['pops'][pn] = table_one(n0[pi], D0[pi], nb[:, pi], Db[:, pi], arms=FIVE)
            o['pops'][pn]['levels_with_undefined_frontier_point'] = int(nl0[pi])
            o['pops'][pn]['resamples_with_undefined_frontier'] = int((nlb[:, pi] > 0).sum())
        nt0, Dw0 = L.weighted(n0[None], D0[None]); ntb, Dwb = L.weighted(nb, Db)
        o['pops']['phase_weighted'] = table_one(nt0[0], Dw0[0], ntb, Dwb)
        # counts behind the scoring
        o['counts'] = dict(
            pairs_unsafe_wrong_go=sum(int((~((d['clear'] if sc == 'W1' else d['rs']) > 2.0)).sum()) for d in ds),
            pairs_not_truly_safe_3s=sum(int((~(d['clear'] > 2.0)).sum()) for d in ds),
            decisions_without_safe_row_scoring=sum(int((~((d['clear'] if sc == 'W1' else d['rs']) > 2.0).any(1)).sum()) for d in ds),
            decisions_without_truly_safe_row_3s=sum(int((~(d['clear'] > 2.0).any(1)).sum()) for d in ds))
        out['scorings'][name] = o
    out['seconds'] = time.time() - t0
    L.jdump(out, L.HERE / ('RECOUNT_item2_v01%s.json' % ('_quick' if QUICK else '')))
    L.log('item 2 done %.0f s' % (time.time() - t0), file=LOG)


# ------------------------------------------------------------------------------------------------ item 3 (R12a)
T_LIST = (0, 1, 2, 5, 10, 20)


def masks_trunc(d):
    """Keep every evaluated decision before the lead's stop and those after it with (k - k_stop) * 0.05 s < T.
    k_stop = tick of the run's first stored decision with phase 2; a run without one keeps everything."""
    out = []
    for T in T_LIST:
        if d['k_stop'] is None:
            out.append(np.ones(d['n'], bool)); continue
        dk = d['k'] - d['k_stop']
        m_int = dk < int(round(T / L.H))                 # integer form
        m_flt = (dk * L.H) < T                           # the brief's form
        if not np.array_equal(m_int, m_flt):
            raise RuntimeError('%s: float and integer forms of the truncation differ at T = %s' % (d['run'], T))
        out.append(m_flt)
    return out


def item3(ds):
    t0 = time.time()
    M, n0, D0, nl0, nb, Db, nlb = run_config(ds, masks_trunc, len(T_LIST), 'W1', 0., False, 'R12a truncation')
    out = dict(item='R12a post-stop truncation', nboot=int(nb.shape[0]), T={},
               runs_without_phase2=[d['run'] for d in ds if d['k_stop'] is None],
               k_stop={d['run']: d['k_stop'] for d in ds},
               first_phase2_decision_is_evaluated={d['run']: (None if d['k_stop'] is None else bool(d['ev_all'][np.flatnonzero(d['phase_all'] == 2)[0]])) for d in ds})
    for ti, T in enumerate(T_LIST):
        e = table_one(n0[ti], D0[ti], nb[:, ti], Db[:, ti], arms=FIVE)
        e['levels_with_undefined_frontier_point'] = int(nl0[ti]); e['resamples_with_undefined_frontier'] = int((nlb[:, ti] > 0).sum())
        e['n_by_phase'] = {str(p): sum(int((m & (d['phase'] == p)).sum()) for d in ds for m in [masks_trunc(d)[ti]]) for p in range(4)}
        out['T'][str(T)] = e
    # sensitivity to one reading (points only): k_stop taken from the run's first EVALUATED decision with phase 2
    def masks_alt(d):
        ph2 = np.flatnonzero(d['phase'] == 2)
        if ph2.size == 0:
            return [np.ones(d['n'], bool) for _ in T_LIST]
        ks = int(d['k'][ph2[0]])
        return [(d['k'] - ks) < int(round(T / L.H)) for T in T_LIST]
    Ma = L.build_M(ds, masks_alt, 'W1', 0., False)
    na, Da, _ = L.evaluate(Ma.sum(0), len(T_LIST))
    out['alt_k_stop_first_evaluated_phase2_decision'] = {str(T): table_one(na[0, ti], Da[0, ti]) for ti, T in enumerate(T_LIST)}
    out['seconds'] = time.time() - t0
    L.jdump(out, L.HERE / ('RECOUNT_item3_v01%s.json' % ('_quick' if QUICK else '')))
    L.log('item 3 done %.0f s' % (time.time() - t0), file=LOG)


# ------------------------------------------------------------------------------------------------ item 5 (R9, single bootstraps)
STATS = ('R', 'RR_N', 'RR_NA', 'RR_AM', 'RR_CK3', 'RR_Q', 'RR0_CK3', 'RR_NA_minus_RR_N')


def stat_values(D):
    """D (B, A+1) -> dict of the eight statistics (B,), NaN where the statistic's denominator is not positive."""
    D = np.atleast_2d(D)
    dE = D[:, 1]; d0 = D[:, A]
    with np.errstate(invalid='ignore', divide='ignore'):
        okE = dE > 0; ok0 = d0 > 0
        out = dict(R=dE / 201.)
        for a in ('N', 'NA', 'AM', 'CK3', 'Q'):
            out['RR_' + a] = np.where(okE, D[:, AI[a]] / dE, np.nan)
        out['RR0_CK3'] = np.where(ok0, D[:, AI['CK3']] / d0, np.nan)
        out['RR_NA_minus_RR_N'] = np.where(okE, D[:, AI['NA']] / dE - D[:, AI['N']] / dE, np.nan)
    return out


def alpha_groups():
    j = json.loads(L.A4_JSON.read_text(encoding='utf-8'))
    al = j['splits']['alpha']
    groups = []
    for key in sorted(al.keys(), key=float):
        runs = al[key]['runs']
        groups.append((key, np.array([L.RUNS.index(r) for r in runs], np.int64)))
    allr = np.concatenate([g for _, g in groups])
    if sorted(allr.tolist()) != list(range(35)):
        raise RuntimeError('alpha groups do not partition the 35 runs')
    return groups


def item5(ds):
    t0 = time.time()
    out = dict(item='R9 intervals (single bootstraps)', nboot=NB)
    M = L.build_M(ds, L.masks_all, 'W1', 0., False)
    n0, D0, _ = L.evaluate(M.sum(0), 1)
    truth = {k: float(v[0]) for k, v in stat_values(D0[:, 0]).items()}
    out['truth'] = truth
    # (a) the draw of record
    idx = L.draw_of_record()[:NB]
    nb, Db, _ = L.boot(M, idx, 1, logfile=LOG, tag='R9 record')
    sv = stat_values(Db[:, 0])
    rec = {}
    for s in STATS:
        v = sv[s]; ci = L.pct(v)
        rec[s] = dict(point=truth[s], percentile=ci, basic=[2 * truth[s] - ci[1], 2 * truth[s] - ci[0]],
                      n_left_out=int((~np.isfinite(v)).sum()), min=float(np.nanmin(v)), max=float(np.nanmax(v)))
    out['draw_of_record'] = rec
    if not QUICK:
        np.savez(L.HERE / 'rc_record_stats_v01.npz', **sv)
    # (c) stratified by the recording setting alpha
    groups = alpha_groups()
    rng = np.random.default_rng(20261122)
    parts = [g[rng.integers(0, g.size, (20000, g.size))] for _, g in groups]
    idx_s = np.concatenate(parts, axis=1)[:NB]
    nb, Db, _ = L.boot(M, idx_s, 1, logfile=LOG, tag='R9 stratified')
    sv = stat_values(Db[:, 0])
    out['stratified_by_alpha'] = dict(groups={k: [L.RUNS[i] for i in g] for k, g in groups},
                                      stats={s: dict(point=truth[s], percentile=L.pct(sv[s]), n_left_out=int((~np.isfinite(sv[s])).sum())) for s in STATS})
    # (d) the runs with at least 100 evaluated decisions
    nrun = np.array([d['n'] for d in ds])
    long = np.flatnonzero(nrun >= 100)
    out['long_runs'] = dict(n_runs=int(long.size), runs=[L.RUNS[i] for i in long], short_runs={L.RUNS[i]: int(nrun[i]) for i in np.flatnonzero(nrun < 100)})
    if long.size == 30:
        nL, DL, _ = L.evaluate(M[long].sum(0), 1)
        tl = {k: float(v[0]) for k, v in stat_values(DL[:, 0]).items()}
        rng = np.random.default_rng(20261123)
        idx_l = long[rng.integers(0, 30, (20000, 30))][:NB]
        nb, Db, _ = L.boot(M, idx_l, 1, logfile=LOG, tag='R9 long runs')
        sv = stat_values(Db[:, 0])
        out['long_runs']['n_eval'] = float(nL[0, 0])
        out['long_runs']['den0'] = float(DL[0, 0, A]); out['long_runs']['denE'] = float(DL[0, 0, 1])
        out['long_runs']['stats'] = {s: dict(point=tl[s], percentile=L.pct(sv[s]), n_left_out=int((~np.isfinite(sv[s])).sum())) for s in STATS}
    else:
        out['long_runs']['error'] = 'expected 30 long runs'
    out['seconds'] = time.time() - t0
    L.jdump(out, L.HERE / ('RECOUNT_item5_single_v01%s.json' % ('_quick' if QUICK else '')))
    L.log('item 5 (single bootstraps) done %.0f s' % (time.time() - t0), file=LOG)


# ------------------------------------------------------------------------------------------------ item 6 (R19 / R20)
AGE_BANDS = (('<0.5', 0., 0.5), ('0.5-1', 0.5, 1.), ('1-2', 1., 2.), ('2-4', 2., 4.), ('>=4', 4., np.inf))


def item6(ds):
    t0 = time.time()
    files = sorted(L.STORED.glob('*.npz'))
    fam = {}
    for f in files:
        with np.load(f, allow_pickle=False) as z:
            m = json.loads(str(z['meta']))
            ev = z['evaluated'].astype(bool)
            cN = np.asarray(z['cN'], float)[ev]; cF = np.asarray(z['cF0'], float)[ev]
            age = np.asarray(z['prim_age'], float)[ev]; miss = np.asarray(z['prim_miss'])[ev]
        ok = np.isfinite(cN) & np.isfinite(cF) & (cN > 0) & (cF > 0)
        with np.errstate(invalid='ignore', divide='ignore'):
            mm = 1. / np.sqrt(cN / cF)
        rec = dict(run=f.stem, set=m.get('set'), n_eval=int(ev.sum()), m=mm[ok], age=np.broadcast_to(age[:, None], ok.shape)[ok],
                   miss=np.broadcast_to(miss[:, None], ok.shape)[ok], rows_all=int(ok.size), rows_nonpos_or_nonfinite=int((~ok).sum()))
        fam.setdefault(m.get('family'), []).append(rec)
    out = dict(item='R19 / R20', n_files=len(files), families={}, families_by_set={})

    def summ(recs):
        m = np.concatenate([r['m'] for r in recs]) if recs else np.zeros(0)
        if m.size == 0:
            return dict(runs=len(recs), evaluated_decisions=int(sum(r['n_eval'] for r in recs)), rows=0)
        med = float(np.median(m))
        outside = np.abs(m / med - 1.) > 0.05
        return dict(runs=len(recs), evaluated_decisions=int(sum(r['n_eval'] for r in recs)), rows=int(m.size), median_m=med,
                    share_outside_5pct=float(outside.mean()), rows_outside_5pct=int(outside.sum()), min_m=float(m.min()), max_m=float(m.max()),
                    rows_excluded_nonpositive_or_nonfinite=int(sum(r['rows_nonpos_or_nonfinite'] for r in recs)))

    for fk in sorted(fam):
        out['families'][fk] = summ(fam[fk])
        for st in sorted(set(r['set'] for r in fam[fk])):
            out['families_by_set']['%s|%s' % (fk, st)] = summ([r for r in fam[fk] if r['set'] == st])
    # lead braking, the 35 evaluation runs: evaluated decisions by track age
    age = np.concatenate([d['prim_age'] for d in ds]); n = age.size
    bands = {}
    for name, lo, hi in AGE_BANDS:
        k = int(((age >= lo) & (age < hi)).sum())
        bands[name] = dict(decisions=k, share=k / n)
    out['lead_braking_eval_prim_age'] = dict(n=int(n), bands=bands, n_nan=int(np.isnan(age).sum()), min_age=float(np.nanmin(age)))
    # extra (Amendment R19, not in the brief's list): margin ratio of the 35 evaluation runs by track-age band
    recs = [r for r in fam['lead_braking'] if r['set'] == 'fit']
    m = np.concatenate([r['m'] for r in recs]); ag = np.concatenate([r['age'] for r in recs]); ms = np.concatenate([r['miss'] for r in recs])
    med = float(np.median(m)); outside = np.abs(m / med - 1.) > 0.05
    ex = dict(rows=int(m.size), median_m=med, rows_outside_5pct=int(outside.sum()), by_age={}, outside_by_prim_miss={})
    for name, lo, hi in AGE_BANDS:
        b = (ag >= lo) & (ag < hi)
        ex['by_age'][name] = dict(rows=int(b.sum()), rows_outside_5pct=int((outside & b).sum()),
                                  median_m=(float(np.median(m[b])) if b.any() else None))
    for v in sorted(set(ms.tolist())):
        ex['outside_by_prim_miss'][str(v)] = dict(rows=int((ms == v).sum()), rows_outside_5pct=int((outside & (ms == v)).sum()))
    out['extra_lead_braking_eval_margin_ratio'] = ex
    # extra: the same for every stored lead-braking run (fit and tuning), the family whose count outside the band is 1,127
    recs = fam['lead_braking']
    m = np.concatenate([r['m'] for r in recs]); ag = np.concatenate([r['age'] for r in recs]); ms = np.concatenate([r['miss'] for r in recs])
    med = float(np.median(m)); outside = np.abs(m / med - 1.) > 0.05
    ex = dict(rows=int(m.size), median_m=med, rows_outside_5pct=int(outside.sum()), by_age={}, outside_by_prim_miss={})
    for name, lo, hi in AGE_BANDS:
        b = (ag >= lo) & (ag < hi)
        ex['by_age'][name] = dict(rows=int(b.sum()), rows_outside_5pct=int((outside & b).sum()),
                                  median_m=(float(np.median(m[b])) if b.any() else None))
    for v in sorted(set(ms.tolist())):
        ex['outside_by_prim_miss'][str(v)] = dict(rows=int((ms == v).sum()), rows_outside_5pct=int((outside & (ms == v)).sum()))
    out['extra_lead_braking_all_runs_margin_ratio'] = ex
    out['seconds'] = time.time() - t0
    L.jdump(out, L.HERE / 'RECOUNT_item6_v01.json')
    L.log('item 6 done %.0f s' % (time.time() - t0), file=LOG)


def main():
    which = [a for a in sys.argv[1:] if a.isdigit()]
    L.log('rc_items_v01 start, items %s, nboot %d' % (which, NB), file=LOG)
    ds = L.load_all()
    for w in which:
        dict(zip('12356', (item1, item2, item3, item5, item6)))[w](ds)
    L.log('rc_items_v01 end', file=LOG)


if __name__ == '__main__':
    main()
