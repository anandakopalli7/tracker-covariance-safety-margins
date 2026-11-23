"""Second program (recount) of the step-0 descriptive values, A11 s2 / A10 s2.1-2.3. Written 21 Nov 2026 (Claude Sonnet 5.5).
Run: python -I -B -X utf8 step0_recount_v01.py   (NUMBA_NUM_THREADS=2). Reads stored arrays only. Does not read the first program.
Shared with the first program (allowed): trk_score_v01 (make_run, gridless), optA_lib_v02 (boot_counts, dec_eq, clean_clear), gl_fast_v13
(frontier kernel), the stored arrays and the resample draw. Own code: loading, margin ratio, ranks u, E5/E5_N scales, shares, intervals,
unsafe / unbound shares, lead-braking reference."""
import sys, json, glob, os, time
import numpy as np


def rankdata(x, method='average'):
    # mid-ranks (average of the 1-based positions of tied values)
    x = np.asarray(x, float)
    u, inv, cnt = np.unique(x, return_inverse=True, return_counts=True)
    last = np.cumsum(cnt); first = last - cnt + 1
    return ((first + last) / 2.0)[inv]

W = r'ARS_TRIAL\revision_v13\work'
sys.path.insert(0, W + r'\shared\trackers')
sys.path.insert(0, W + r'\CD_capture\analysis')
import trk_score_v01 as TS
import optA_lib_v02 as L
import gl_fast_v13 as GF

ARR = r'<library folder>\gateR_rt_v01'
OUT = W + r'\shared\checks\step0_recount'
K, SEED = 20000, 20261121
CHUNK = 1000


def load_all():
    out = []
    for f in sorted(glob.glob(ARR + r'\*.npz')):
        d = dict(np.load(f, allow_pickle=True))
        m = json.loads(str(d['meta']))
        out.append((os.path.basename(f)[:-4], m['family'], m['set'], d))
    return out


def q(a, p):
    return [float(x) for x in np.percentile(a, p)]


def ci(a):
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    return dict(ci95=q(a, [2.5, 97.5]), ci90=q(a, [5, 95]), n_finite=int(a.size))


def analyse(items):
    names = [n for n, *_ in items]
    ds = [d for *_, d in items]
    nr = len(ds)
    ev = [d['evaluated'].astype(bool) for d in ds]
    res = dict(n_runs=nr, runs_with_eval=int(sum(e.any() for e in ev)), n_eval_decisions=int(sum(e.sum() for e in ev)))
    # margin ratio at binding rows (evaluated decisions, finite positive cF0 and cN): sqrt(cF0 / cN)
    rat = []
    for d, e in zip(ds, ev):
        a = d['cF0'][e]; b = d['cN'][e]
        ok = np.isfinite(a) & np.isfinite(b) & (a > 0) & (b > 0)
        rat.append(np.sqrt(a[ok] / b[ok]))
    rat = np.concatenate(rat)
    m = float(np.median(rat)); q05, q95 = (float(x) for x in np.quantile(rat, [0.05, 0.95]))
    A = (q95 - q05) / (2 * m)
    res['margin'] = dict(n_rows=int(rat.size), median=m, q05=q05, q95=q95, A=A, share_within5=float(np.mean(np.abs(rat - m) <= 0.05 * m)))
    # ranks u_i over the run set's evaluated decisions (rho = sqrt(cF0/cE), median over rows, mid-ranks)
    ridx = []; rv = []
    for i, (d, e) in enumerate(zip(ds, ev)):
        for t in np.flatnonzero(e):
            a = d['cF0'][t]; b = d['cE'][t]
            ok = np.isfinite(a) & np.isfinite(b) & (a > 0) & (b > 0)
            ridx.append((i, t)); rv.append(np.median(np.sqrt(a[ok] / b[ok])) if ok.any() else np.nan)
    rv = np.array(rv); have = np.isfinite(rv)
    uu = np.full(rv.size, 0.5)
    uu[have] = (rankdata(rv[have], method='average') - 0.5) / have.sum()
    U = [np.full(e.size, 0.5) for e in ev]
    for (i, t), v in zip(ridx, uu):
        U[i][t] = v
    res['n_dec_with_rho'] = int(have.sum())
    runs = []
    for nme, d, e in zip(names, ds, ev):
        runs.append(TS.make_run(d, (e,), dict(F0='cF0', E='cE', N='cN'), desired=float(d['des'][0]), name=nme))
    for r, u in zip(runs, U):
        for nm, mm, AA in (('E5N', m, A), ('E5', 1.1029, 0.05)):
            f = mm * (1. + AA * (2. * u - 1.))
            r['crit'][nm] = r['crit']['F0'] / (f * f)[:, None]
    G = TS.gridless(runs, ['F0', 'E', 'N', 'E5N', 'E5'])
    prep = GF.Prepared(G, ['F0', 'E', 'N', 'E5N', 'E5'], 0)
    one = GF.evaluate(prep, np.ones((1, nr)))
    den = float(one['denE'][0]); n = float(one['n'][0])
    lib = TS.rr_gl(G, 'F0', 'E', ['N', 'E5N', 'E5'])
    res['crosscheck_lib'] = dict(denE_diff=abs(lib['denE'] - den), D_diff={a: abs(lib['D'][a] - float(one['D'][a][0])) for a in ('N', 'E5N', 'E5')})
    res['R_pp'] = den / 201.; res['R_deceq'] = L.dec_eq(den, n); res['den_sum'] = den; res['n_for_deceq'] = n
    pt = {a: (float(one['D'][a][0]) / den if den > 0 else float('nan')) for a in ('N', 'E5N', 'E5')}
    CNT = L.boot_counts(nr, K, SEED)
    dE = np.empty(K); nn = np.empty(K); D = {a: np.empty(K) for a in ('N', 'E5N', 'E5')}
    for b0 in range(0, K, CHUNK):
        o = GF.evaluate(prep, CNT[b0:b0 + CHUNK])
        dE[b0:b0 + CHUNK] = o['denE']; nn[b0:b0 + CHUNK] = o['n']
        for a in D:
            D[a][b0:b0 + CHUNK] = o['D'][a]
        del o
    pos = dE > 0
    res['share_resamples_room_pos'] = float(np.mean(pos))
    res['R_pp_ci'] = ci(dE / 201.)
    res['R_deceq_ci'] = ci(L.dec_eq(dE, nn))
    for a in D:
        rr = np.where(pos, D[a] / np.where(pos, dE, 1.), np.nan)
        res['RR_' + a] = dict(point=pt[a], D_point=float(one['D'][a][0]), **ci(rr), n_resamples_used=int(pos.sum()))
    nb = 0; nu = 0; ns = 0; tot = 0
    for d, e in zip(ds, ev):
        a = d['cF0'][e]
        has = np.any(np.isfinite(a) & (a > 0), axis=1)
        c1 = L.clean_clear(d['clear'][e])
        nb += int((~has).sum()); nu += int(np.any(c1 <= 0, axis=1).sum()); ns += int((~np.any(c1 > 0, axis=1)).sum()); tot += int(e.sum())
    res['share_no_binding_F0'] = nb / tot; res['n_no_binding_F0'] = nb
    res['share_some_row_unsafe_3s'] = nu / tot; res['n_some_row_unsafe_3s'] = nu
    res['share_no_safe_row_3s'] = ns / tot
    return res


def main():
    t0 = time.time()
    allr = load_all()
    out = {}
    for fam in ('vehicle_crossing', 'pedestrian_crossing'):
        sets = {'all': [x for x in allr if x[1] == fam and x[2] in ('tuning', 'fit')],
                'tuning': [x for x in allr if x[1] == fam and x[2] == 'tuning']}
        for sn, items in sets.items():
            out['%s|%s' % (fam, sn)] = analyse(items)
            print(fam, sn, len(items), 'done %.0fs' % (time.time() - t0), flush=True)
    items = [x for x in allr if x[1] == 'lead_braking' and x[2] == 'tuning']
    runs = [TS.make_run(d, (d['evaluated'].astype(bool),), dict(F0='cF0', E='cE'), desired=float(d['des'][0]), name=n) for n, _, _, d in items]
    G = TS.gridless(runs, ['F0', 'E'])
    prep = GF.Prepared(G, ['F0', 'E'], 0)
    o = GF.evaluate(prep, np.ones((1, len(runs))))
    den = float(o['denE'][0]); n = float(o['n'][0])
    out['lead_braking|tuning'] = dict(n_runs=len(runs), n_eval_decisions=int(n), R_pp=den / 201., R_deceq=L.dec_eq(den, n))
    json.dump(out, open(OUT + r'\STEP0_RECOUNT_v01.json', 'w'), indent=1, default=float)
    print('written %.0fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
