"""Recount of package C: identity test of the recount's gridless kernel against the library of record, on OLD runs only.
New file, 19 Nov 2026 (Claude Fable 5.2).

For the 35 old evaluation runs (and, with --cutin, the 20 cut-in tuning runs), several populations and several run resamples:
  reference = a9_common_v01.gridless_sources(...).curve(weights) fed to optA_lib_v02.eval_scoring (the library of record);
  recount   = rc_core_v13.Problem.evaluate(weights) (own events, numba kernel).
Every denE, n and D[a] must be EQUAL (==, bit for bit; NaN matches NaN). Also checked: the recount's E5 family (e5_u, permute_u,
oracle critical scales, margin-ratio summary) against the shared tracker library trk_score_v01, value for value.
Usage: python -I -B -X utf8 test_rc_kernel_v13.py [--resamples 40] [--cutin] [--workers 2]
Output: out\\TEST_RC_KERNEL_v13<tag>.json (never overwritten).
"""
import argparse, pathlib, sys, time
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))      # python -I: the script folder is not on sys.path
import rc_core_v13 as K

L = K.L


def same(x, y):
    return bool(x == y or (np.isnan(x) and np.isnan(y)))


def compare(A9, runs, names, masks_fn, npop, W, label, doc):
    preps = [K.Prep(r) for r in runs]
    cur = {nm: K.build_curves(runs, preps, nm, masks_fn, oracle=(nm == 'O')) for nm in names}
    for k, r in enumerate(runs):
        r['_masks'] = tuple(masks_fn(k))
    G = A9.gridless_sources(runs, names, lambda r: r['clear1'] > 0., masks_key='_masks')
    ndiff = 0; ncmp = 0; maxd = 0.; t_lib = 0.; t_rc = 0.
    for pi in range(npop):
        Pb = K.Problem(names, [cur[nm][pi] for nm in names])
        t0 = time.time()
        e = Pb.evaluate(W)
        t_rc += time.time() - t0
        for b in range(W.shape[0]):
            t0 = time.time()
            T = {nm: G[nm].curve(W[b], pops=[pi])[:, 0, :] for nm in names}
            el = L.eval_scoring(T, names[1:])
            t_lib += time.time() - t0
            pairs = [(el['denE'], e['denE'][b]), (el['n'], e['n'][b])] + [(el['D'][x], e['D'][x][b]) for x in names[2:]]
            pairs.append((el['D']['E'], e['denE'][b]))
            for x, y in pairs:
                ncmp += 1
                if not same(x, y):
                    ndiff += 1
                    if np.isfinite(x) and np.isfinite(y):
                        maxd = max(maxd, abs(x - y))
                    else:
                        maxd = float('inf')
    doc[label] = dict(populations=npop, resamples=int(W.shape[0]), sources=names, values_compared=ncmp, values_differing=ndiff,
                      max_abs_diff=maxd, seconds_library=t_lib, seconds_recount=t_rc,
                      points_per_source={nm: [int(c.npts) for c in cur[nm]] for nm in names})
    print('%s: %d values compared, %d differ (max |diff| %.3g); library %.1f s, recount %.2f s'
          % (label, ncmp, ndiff, maxd, t_lib, t_rc), flush=True)
    for r in runs:
        r.pop('_masks', None)
    return ndiff


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--resamples', type=int, default=40)
    ap.add_argument('--cutin', action='store_true')
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    outf = K.OUT / ('TEST_RC_KERNEL_v13%s.json' % a.tag)
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    K.set_workers(a.workers)
    A9 = K.try_a9()
    if A9 is None:
        raise SystemExit('the library of record is not importable here')
    doc = dict(code='test_rc_kernel_v13.py', started=K.clock(), numpy=np.__version__, numba=K.numba.__version__)
    bad = 0
    runs = K.load_old_eval_runs()
    n = len(runs)
    # ---- E5 family against the shared tracker library
    sys.path.insert(0, str(K.SHARED))
    import trk_score_v01 as TS
    u, info = K.e5_u(runs); u_l, info_l = TS.e5_u(runs)
    up = K.permute_u(runs, u); up_l = TS.permute_u(runs, u_l)
    for r, uu, pp in zip(runs, u, up):
        r['crit']['E5'] = K.oracle_crit(r['crit']['F0'], K.RATIO, K.E5_AMP, uu)
        r['crit']['E5p'] = K.oracle_crit(r['crit']['F0'], K.RATIO, K.E5_AMP, pp)
    lib_runs = [dict(r, crit=dict(r['crit']), sel={}) for r in runs]
    TS.add_oracle(lib_runs, 'E5', 'F0', K.RATIO, K.E5_AMP, u_l); TS.add_oracle(lib_runs, 'E5p', 'F0', K.RATIO, K.E5_AMP, up_l)
    rs = K.ratio_summary(np.concatenate([K.margin_ratio_values(r) for r in runs]))
    rs_l = TS.ratio_summary(TS.margin_ratios(runs, 'N', 'F0'))
    e5 = dict(u_equal=all(np.array_equal(x, y) for x, y in zip(u, u_l)), info_equal=(info == info_l),
              u_permuted_equal=all(np.array_equal(x, y) for x, y in zip(up, up_l)),
              crit_E5_equal=all(np.array_equal(x['crit']['E5'], y['crit']['E5'], equal_nan=True) for x, y in zip(runs, lib_runs)),
              crit_E5p_equal=all(np.array_equal(x['crit']['E5p'], y['crit']['E5p'], equal_nan=True) for x, y in zip(runs, lib_runs)),
              ratio_summary_equal=all(rs[k] == rs_l[k] for k in rs), ratio_summary=rs, e5_info=info)
    ph_l = [TS.est_phase(r['vhat'], r['ahat_long'], r['lead_found'], t) for r in runs for t in (-1.0, -0.5, -2.0)]
    ph_m = [K.est_phase(r['vhat'], r['ahat_long'], r['lead_found'], t) for r in runs for t in (-1.0, -0.5, -2.0)]
    e5['est_phase_equal'] = all(np.array_equal(x, y) for x, y in zip(ph_l, ph_m))
    doc['E5_family_vs_trk_score_v01'] = e5
    print('E5 family / phase vs trk_score_v01: %s' % {k: v for k, v in e5.items() if k.endswith('equal')}, flush=True)
    bad += sum(1 for k, v in e5.items() if k.endswith('equal') and not v)
    # ---- gridless kernel against the library of record
    rng = np.random.default_rng(424242)                           # test-only draw (not a seed of A10)
    W = np.concatenate([np.ones((1, n)), K.counts_of(rng.integers(0, n, (a.resamples, n)), n)])
    # a degenerate weight vector as well: a single run repeated
    W = np.concatenate([W, np.eye(n)[:2] * n])

    def masks(k):
        r = runs[k]; ev = r['ev']; ph = K.est_phase(r['vhat'], r['ahat_long'], r['lead_found'])
        return [ev, ev & (ph == 0), ev & (ph == 1), ev & (ph == 2), ev & (r['ph'] == 2), ev & (r['k'] % 20 == 0)]
    bad += compare(A9, runs, ['F0', 'E', 'N', 'CK3', 'E5', 'E5p', 'NA', 'A1', 'Q', 'TG', 'O'], masks, 6, W, 'old_evaluation_runs', doc)
    if a.cutin:
        cr = K.load_old_cutin_runs()
        nc = len(cr)
        Wc = np.concatenate([np.ones((1, nc)), K.counts_of(rng.integers(0, nc, (a.resamples, nc)), nc)])

        def cmasks(k):
            r = cr[k]; ev = r['ev']
            return [ev, ev & (r['k'] >= 120) & (r['k'] <= 220), ev & (r['k'] < 60)]
        bad += compare(A9, cr, ['F0', 'E', 'N', 'O'], cmasks, 3, Wc, 'old_cutin_tuning_runs', doc)
    doc['all_identical'] = bool(bad == 0)
    doc['written'] = K.clock()
    print('ALL IDENTICAL' if bad == 0 else 'DIFFERENCES FOUND: %d' % bad)
    print('written %s' % K.write_new(outf, doc))


if __name__ == '__main__':
    main()
