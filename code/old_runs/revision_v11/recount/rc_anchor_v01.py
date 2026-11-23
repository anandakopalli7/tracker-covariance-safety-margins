"""Recount: the sanity anchor. Reproduce the published 3 s values (and the two reaction-and-stop values) before anything new.
Usage: python -B -X utf8 rc_anchor_v01.py [nboot]   (default 20000 = the draw of record)"""
import sys, time
import numpy as np
import rc_lib_v01 as L

LOG = L.HERE / 'rc_anchor_v01_log.txt'
A = len(L.ARMS); ai = {a: i for i, a in enumerate(L.ARMS)}; ai['O'] = A


def main():
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else L.NBOOT
    t0 = time.time()
    ds = L.load_all()
    out = dict(n_runs=len(ds), n_eval=sum(d['n'] for d in ds), n_stored=sum(d['n_stored'] for d in ds),
               nan_clear_in_evaluated=sum(d['n_nan_clear_eval'] for d in ds), nan_cache_in_evaluated=sum(d['n_nan_rs_eval'] for d in ds),
               phase_counts={str(p): sum(int((d['phase'] == p).sum()) for d in ds) for p in range(4)},
               moving=sum(int((d['v0'] > 0.5).sum()) for d in ds))
    L.log('loaded', out, file=LOG)
    # caution terms: is the first truly safe row always at least as fast as every later truly safe row?
    neg = 0; tot = 0
    for d in ds:
        s = d['clear'] > 0; first = s.argmax(1)
        diff = d['vbar'][np.arange(d['n']), first][:, None] - d['vbar']
        neg += int(((diff < 0) & s).sum()); tot += int(s.sum())
    out['negative_caution_terms_among_safe_rows'] = [neg, tot]
    M = L.build_M(ds, L.masks_std, 'W1', 0., False)
    n, D, nl = L.evaluate(M.sum(0), 5)
    n, D, nl = n[0], D[0], nl[0]
    # check of the level emulation against numpy.linspace at the point
    _, _, _, cur = L.evaluate(M.sum(0), 5, want_curves=True)
    C = cur[0]['C'][0]
    ref = np.linspace(C[0, 0], min(np.nanmax(C[0]), np.nanmax(C[1])), 201)
    out['levels_equal_numpy_linspace'] = bool(np.array_equal(ref, cur[0]['lev'][0]))
    pt = dict(n=n.tolist(), R_pp=float(D[0, 1] / 201), denE=float(D[0, 1]), den0=float(D[0, A]), nan_levels=nl.tolist())
    for a in ('N', 'NA', 'CK3', 'AM', 'Q'):
        pt['RR_' + a] = float(D[0, ai[a]] / D[0, 1]); pt['RR0_' + a] = float(D[0, ai[a]] / D[0, A])
    out['W1_point_all'] = pt
    L.log('W1 point', pt, file=LOG)
    Mr = L.build_M(ds, L.masks_std, 'RS', 0., False)
    nr, Dr, nlr = L.evaluate(Mr.sum(0), 5)
    out['RS_point_all'] = dict(den0=float(Dr[0, 0, A]), denE=float(Dr[0, 0, 1]), RR0_CK3=float(Dr[0, 0, ai['CK3']] / Dr[0, 0, A]),
                               nan_levels=nlr[0].tolist())
    L.log('RS point', out['RS_point_all'], file=LOG)
    idx = L.draw_of_record()[:nb]
    nB, DB, nlB = L.boot(M, idx, 5, logfile=LOG, tag='W1')
    ci = dict(nboot=nb, R_pp=L.pct(DB[:, 0, 1] / 201), n_nan_resamples=int((nlB[:, 0] > 0).sum()),
              share_denE_le0=float((DB[:, 0, 1] <= 0).mean()))
    for a in ('N', 'NA', 'CK3', 'AM', 'Q'):
        ci['RR_' + a], _ = L.ratio_ci(DB[:, 0, ai[a]], DB[:, 0, 1])
    out['W1_ci_all'] = ci
    L.log('W1 intervals', ci, file=LOG)
    out['seconds'] = time.time() - t0
    L.jdump(out, L.HERE / 'rc_anchor_v01_out.json')
    L.log('done %.0f s' % (time.time() - t0), file=LOG)


if __name__ == '__main__':
    main()
