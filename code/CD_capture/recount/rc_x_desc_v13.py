"""Recount (second program) of the fixed descriptive outputs of test X (A11 section 3.6, pedestrian crossing), revision v13.
New file, 21 Nov 2026 (Claude Sonnet 5.5). Written from crossing\\CD_DEFINITIONS_X_DESC_v13.md, A11 section 3 and
crossing\\CD_DEFINITIONS_X_v13.md section 0 only. NOT opened: x_desc_v13.py, x_cross_v13.py, crossing\\out, analysis\\, tools\\.

Imports (unchanged): rc_core_v13 / rc_kern_v13 (own gridless curves, kernel, e5_u, ratio values, percentile interval), rc_x_cross_v13
(run loaders, the A11 gate, case selection) and the scoring library of record optA_lib_v02 (via rc_core_v13.L).

Modes
  --test-old [--nboot N]   the 51 stored old pedestrian runs -> out\\TESTOLD_RC_X_DESC_pedestrian_crossing_v13[_b<N>].json
  --cases-sha SHA          fresh (needs revision_v13\\LOCK_A11.txt; full sizes only) -> out\\RC_X_DESC_pedestrian_crossing_v13.json
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('NUMBA_NUM_THREADS', '2')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import argparse, json, pathlib, sys, time
import numpy as np

if os.name == 'nt':                                   # BelowNormal priority (shared laptop)
    try:
        import ctypes
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
    except Exception:
        pass

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))      # python -I
import rc_core_v13 as K                                              # noqa: E402
import rc_x_cross_v13 as XC                                          # noqa: E402

L = K.L
FAMILY = 'pedestrian_crossing'
PRE = 'X.ped.'
SEED_PO = 20261919
PO_P = (0.25, 0.5, 0.75)


def nz(x):
    if x is None:
        return None
    x = float(x)
    return x if np.isfinite(x) else None


def ci_json(ci):
    return None if ci is None or not (np.isfinite(ci[0]) and np.isfinite(ci[1])) else [float(ci[0]), float(ci[1])]


def ratio(D, den):
    """D / den if den > 0 else NaN (RR undefined when D(E) <= 0)."""
    return float(D) / float(den) if (np.isfinite(den) and den > 0) else float('nan')


def run_chunks(P, CN, chunk=1000):
    parts = [P.evaluate(CN[s:s + chunk]) for s in range(0, CN.shape[0], chunk)]
    return dict(n=np.concatenate([p['n'] for p in parts]), denE=np.concatenate([p['denE'] for p in parts]),
                D={a: np.concatenate([p['D'][a] for p in parts]) for a in parts[0]['D']})


def grid_tables(runs, names):
    """name -> (202, 5) pooled statistics on [0] + logspace(-2, 3, 201): select_grid + stats_scored, 3 s commitment, evaluated mask."""
    out = {}
    for a in names:
        acc = None
        for r in runs:
            sel = L.select_grid(r['crit'][a], K.GRID, r['idx55'])
            t = L.stats_scored(sel, r['clear1'], r['clear1'] > 0., r['vbar'], r['desired'], (r['ev'],))
            acc = t if acc is None else acc + t
        out[a] = acc[:, 0, :]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--cases-sha', default=None)
    ap.add_argument('--n', type=int, default=390)
    ap.add_argument('--nboot', type=int, default=K.NBOOT)
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    if a.test_old == (a.cases_sha is not None):
        raise SystemExit('REFUSED: give exactly one of --test-old and --cases-sha SHA')
    full_size = a.nboot == K.NBOOT
    if not a.test_old:
        if not XC.LOCK_A11.is_file():
            raise SystemExit('REFUSED: fresh crossing arrays are sealed until %s exists' % XC.LOCK_A11)
        if not full_size:
            raise SystemExit('REFUSED: fresh runs use the full number of resamples (20,000)')
    name = '%sRC_X_DESC_%s_v13' % ('TESTOLD_' if a.test_old else '', FAMILY) + ('' if full_size else '_b%d' % a.nboot) + a.tag
    outf = K.OUT / (name + '.json')
    if outf.exists():
        raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % outf)
    t00 = time.time()
    K.set_workers(2)

    # ---- run set
    if a.test_old:
        runs, sets = XC.load_old(FAMILY)
        runinfo = dict(sets=sets, run_ids=[r['run'] for r in runs])
    else:
        runs, runinfo = XC.load_fresh(FAMILY, a.n, a.cases_sha)
    n = len(runs)
    if n < 2:
        raise SystemExit('REFUSED: fewer than 2 runs')
    ev_count = [int(r['ev'].sum()) for r in runs]
    n_dec_ev = int(sum(ev_count))
    n_total = int(sum(r['clear1'].shape[0] for r in runs))                 # every decision in the arrays, evaluated or not
    print('%d runs, %d evaluated decisions, %d decisions in all (%s)' % (n, n_dec_ev, n_total, 'old' if a.test_old else 'fresh'), flush=True)

    # ---- section 2: u, ratios, m_N
    u, _ = K.e5_u(runs, 'F0', 'E')
    ratios = np.concatenate([K.margin_ratio_values(r, 'N', 'F0') for r in runs])
    if ratios.size == 0:
        raise SystemExit('REFUSED: no binding row with finite positive N and F0 scales')
    m_N = float(np.median(ratios))

    # ---- sources
    for r, uu in zip(runs, u):
        f = np.quantile(ratios, uu)                                        # section 3: N's empirical ratio quantile at u_i (linear)
        r['crit']['E5q'] = r['crit']['F0'] / (f * f)[:, None]
        r['crit']['P'] = r['crit']['F0'] / (m_N * m_N)                     # section 4: placebo
        r['crit']['Prec'] = r['crit']['F0'] / (K.RATIO * K.RATIO)
    # section 5: partial oracles; u_po over every decision of the analysed runs (ascending run id, array order)
    U = np.random.default_rng(SEED_PO).random(n_total)
    pos = 0
    for r in runs:
        k = r['clear1'].shape[0]
        up = U[pos:pos + k]; pos += k
        for p in PO_P:
            r['crit']['PO%d' % int(round(100 * p))] = np.where((up < p)[:, None], r['crit']['E'], r['crit']['F0'])
    assert pos == n_total

    # ---- gridless (section 3 and 5)
    preps = [K.Prep(r) for r in runs]
    mk = lambda k: [runs[k]['ev']]                                           # noqa: E731
    names = ['F0', 'E', 'N', 'E5q', 'PO25', 'PO50', 'PO75']
    cur = {nm: K.build_curves(runs, preps, nm, mk)[0] for nm in names}
    P_b = K.Problem(['F0', 'E', 'N', 'E5q'], [cur[x] for x in ['F0', 'E', 'N', 'E5q']])
    P_po = K.Problem(['F0', 'E', 'PO25', 'PO50', 'PO75'], [cur[x] for x in ['F0', 'E', 'PO25', 'PO50', 'PO75']])
    print('curves built (%.0f s)' % (time.time() - t00), flush=True)
    e0 = P_b.evaluate(np.ones((1, n))); den = float(e0['denE'][0]); n_dec = float(e0['n'][0])
    D = {x: float(e0['D'][x][0]) for x in e0['D']}
    if n_dec != n_dec_ev:
        raise SystemExit('REFUSED: curve decision count %s differs from the evaluated count %d' % (n_dec, n_dec_ev))
    RR_N = ratio(D['N'], den); RR_Q = ratio(D['E5q'], den)
    e1 = P_po.evaluate(np.ones((1, n)))
    assert float(e1['denE'][0]) == den and float(e1['n'][0]) == n_dec
    Dpo = {x: float(e1['D'][x][0]) for x in ('PO25', 'PO50', 'PO75')}
    PO = {x: ratio(Dpo[x], den) for x in Dpo}

    # ---- bootstrap (A: first nboot rows of boot_counts(n, 20000, 20261911))
    CNT = L.boot_counts(n, a.nboot, K.SEED_BOOT)
    B = run_chunks(P_b, CNT)
    del CNT
    bden = B['denE']
    rN = K.ratio_arr(B['D']['N'], bden); rQ = K.ratio_arr(B['D']['E5q'], bden)
    ci_Q = K.pct_interval(rQ, 0.95); ci_NmQ = K.pct_interval(rN - rQ, 0.95)
    print('bootstrap done (%.0f s)' % (time.time() - t00), flush=True)

    # ---- grid frontier and placebo (section 4)
    T = grid_tables(runs, ['F0', 'E', 'N', 'P', 'Prec'])
    eg = L.eval_scoring(T, ['N', 'P', 'Prec'])
    gden = eg['denE']; gD = eg['D']
    if eg['n'] != n_dec:
        raise SystemExit('REFUSED: grid decision count %s differs from %s' % (eg['n'], n_dec))

    v = {}
    v[PRE + 'desc.n_runs'] = int(n); v[PRE + 'desc.n_dec'] = int(n_dec)
    v[PRE + 'RR_E5qN'] = nz(RR_Q); v[PRE + 'RR_E5qN.ci'] = ci_json(ci_Q); v[PRE + 'RR_E5qN.level'] = 0.95
    v[PRE + 'RR_NmE5qN'] = nz(RR_N - RR_Q); v[PRE + 'RR_NmE5qN.ci'] = ci_json(ci_NmQ); v[PRE + 'RR_NmE5qN.level'] = 0.95
    v[PRE + 'grid.RR_N'] = nz(ratio(gD['N'], gden)); v[PRE + 'grid.RR_P'] = nz(ratio(gD['P'], gden))
    v[PRE + 'grid.RR_NmP'] = nz(ratio(gD['N'] - gD['P'], gden))
    v[PRE + 'grid.RR_Prec'] = nz(ratio(gD['Prec'], gden)); v[PRE + 'grid.RR_NmPrec'] = nz(ratio(gD['N'] - gD['Prec'], gden))
    v[PRE + 'grid.R'] = nz(gden / K.NLEV)
    v[PRE + 'grid.m_N'] = nz(m_N)
    for x in ('PO25', 'PO50', 'PO75'):
        v[PRE + x] = nz(PO[x]); v[PRE + x + '.dec'] = nz(L.dec_eq(Dpo[x], n_dec))
    p25, p50, p75 = (PO[x] for x in ('PO25', 'PO50', 'PO75'))
    v[PRE + 'grading_ok'] = bool(all(np.isfinite([p25, p50, p75])) and p25 > 0 and p25 < p50 < p75)

    doc = dict(code='rc_x_desc_v13.py', role='second program (recount), X fixed descriptive outputs (A11 3.6)', model='claude-sonnet-5-5',
               mode='test-old' if a.test_old else 'fresh', started=K.clock(), nboot=a.nboot, runs=runinfo, n_evaluated_per_run=ev_count,
               n_decisions_all=n_total,
               gridless=dict(denE=den, R_gl_pp=den / K.NLEV, n=n_dec, D=D, D_po=Dpo, RR_gl_N=RR_N, RR_gl_E5q=RR_Q, RR_gl_N_minus_E5q=RR_N - RR_Q,
                             share_denE_pos=float(np.mean(np.isfinite(bden) & (bden > 0))), n_finite_ratio_resamples=int(np.isfinite(rN).sum())),
               grid=dict(denE=gden, D=gD, n=eg['n']), m_N=m_N, n_ratios=int(ratios.size), values=v,
               written=K.clock(), seconds=time.time() - t00)
    print('written %s' % K.write_new(outf, doc))
    print('RR_gl(N) = %r' % RR_N)
    for k_, x in v.items():
        print('  %-26s %s' % (k_, x))


if __name__ == '__main__':
    main()
