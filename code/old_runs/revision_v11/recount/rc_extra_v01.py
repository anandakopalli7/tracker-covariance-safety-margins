"""Recount (second program), comparison stage: per-resample arrays for the comparison, and the quantities that the first
program's output files contain beyond the brief's list.

WRITTEN AFTER the recount's own results (RECOUNT_RESULTS_v01.json, RECOUNT_REPORT_v01.md) were written and after the first
program's OUTPUT files (revision_v11\\analysis\\out\\*.json) were opened. The first program's code was not read. Nothing
here changes a number of RECOUNT_RESULTS_v01.json: the scoring is rc_lib_v01, unchanged; this script only (a) stores the
per-resample n and D arrays, so that every derived number of the first program's tables (decision-equivalent intervals,
basic intervals, shares of non-positive denominators) can be formed from the recount's own resamples, and (b) adds arms
and scorings that the first program printed and the brief did not list. Their definitions are taken from the project's
second-program library (optA2_lib_v02.py / optA2_main_v02.py, allowed by the brief):
  CK3r   CK3 with F0's zero-margin point in place of CK3's own zero-margin point ('CK3repl').
  P25, P50, P75  partial oracles: critical scale = cE where u < p, else cF0; u = default_rng(20261118).random(9307), one
         draw per stored decision of the 35 runs in (run name, k) order, evaluated decisions keeping their own entries.
  (ii)   reaction-and-stop safe AND the stop ends within the 3 s window: tau + t_stop(v0, a0, A) <= 3 + 1e-9, t_stop as in
         optA2_lib_v02 (jerk 12.65 m/s3), copied below.
  other reaction-and-stop settings: the cache keys t1p80_a6p0, t0p75_a4p0, t0p75_a5p0, t0p75_a7p6.

Usage: python -B -X utf8 rc_extra_v01.py"""
import json, math, time
import numpy as np
import rc_lib_v01 as L

LOG = L.HERE / 'rc_extra_v01_log.txt'
BASE = L.ARMS
EXTRA = ('CK3r', 'P25', 'P50', 'P75')
JERK = 12.65
RS_KEYS = {'t0p75_a6p0': (0.75, 6.), 't1p80_a6p0': (1.8, 6.), 't0p75_a4p0': (0.75, 4.), 't0p75_a5p0': (0.75, 5.), 't0p75_a7p6': (0.75, 7.6)}
T_LIST = (0, 1, 2, 5, 10, 20)


def first_stop(v0, a0, jr, t1, A):
    if v0 <= 0. and a0 <= 0.:
        return 0.
    qa, qb, qc = .5 * jr, a0, v0
    disc = qb * qb - 4. * qa * qc
    if disc >= 0.:
        sq = math.sqrt(disc)
        q = -.5 * (qb + math.copysign(sq, qb)) if qb != 0. else -.5 * (qb + sq)
        roots = [q / qa, qc / q] if q != 0. else [0.]
        roots = sorted(r for r in roots if 1e-12 < r <= t1)
        if roots:
            return roots[0]
    v1 = v0 + a0 * t1 + .5 * jr * t1 * t1
    return t1 + max(v1, 0.) / A


def t_stop(v0, a0, A):
    jr = -JERK if a0 > -A else JERK
    return first_stop(v0, a0, jr, abs(-A - a0) / JERK, A)


T_STOP = np.vectorize(t_stop)


def prepare(ds):
    ntot = sum(d['n_stored'] for d in ds)
    if ntot != 9307:
        raise RuntimeError('stored decisions %d, expected 9307' % ntot)
    u = np.random.default_rng(20261118).random(ntot)
    p = 0
    for d in ds:
        m = d['n_stored']
        if not np.all(np.diff(d['k_all']) > 0):
            raise RuntimeError('k not increasing in %s' % d['run'])
        uu = u[p:p + m][d['ev_all']]; p += m
        s = d['sel']['CK3'].copy(); s[0] = d['sel']['F0'][0]; d['sel']['CK3r'] = s
        for pp, nm in ((0.25, 'P25'), (0.5, 'P50'), (0.75, 'P75')):
            d['sel'][nm] = L.select(np.where((uu < pp)[:, None], d['crit']['E'], d['crit']['F0']), d['idx55'])
        zc = np.load(L.CACHE / (d['run'] + '_pack.npz'), allow_pickle=False)
        ev = d['ev_all']
        d['cache'] = {}
        for key in RS_KEYS:
            c = np.asarray(zc[key], float)[ev]
            d['cache'][key] = np.where(np.isnan(c), -1., c)
        tau, A = RS_KEYS['t0p75_a6p0']
        d['late'] = (tau + T_STOP(np.asarray(zc['v0_t0p75_a6p0'], float)[ev], np.asarray(zc['a0_t0p75_a6p0'], float)[ev], A)) > 3. + 1e-9


def build(ds, mask_fn, safe_w_fn, gap, signed):
    rows = []
    for d in ds:
        safe_c = d['clear'] > gap
        rows.append(L.run_row(d, mask_fn(d), safe_w_fn(d, safe_c, gap), safe_c, signed))
    return np.stack(rows)


def sw_w1(d, safe_c, gap):
    return safe_c


def sw_rs(key):
    return lambda d, safe_c, gap: d['cache'][key] > gap


def sw_ii(d, safe_c, gap):
    return (d['cache']['t0p75_a6p0'] > gap) & ~d['late']


def masks_trunc(d):
    if d['k_stop'] is None:
        return [np.ones(d['n'], bool) for _ in T_LIST]
    return [((d['k'] - d['k_stop']) * L.H) < T for T in T_LIST]


def masks_age(d):
    return [d['prim_age'] < 4., d['prim_age'] >= 4.]


def main():
    t0 = time.time()
    L.log('rc_extra_v01 start', file=LOG)
    ds = L.load_all()                      # loaded with the seven base arms
    L.ARMS = BASE + EXTRA                  # run_row / unpack / evaluate read this module global at call time
    prepare(ds)
    idx = L.draw_of_record()
    configs = [('W1_g0', L.masks_std, 5, sw_w1, 0., False, True), ('W1_g0_signed', L.masks_std, 5, sw_w1, 0., True, True),
               ('W1_g2', L.masks_std, 5, sw_w1, 2., False, True), ('WR_t0p75_a6p0_g2', L.masks_std, 5, sw_rs('t0p75_a6p0'), 2., False, True),
               ('ii_t0p75_a6p0_g2', L.masks_std, 5, sw_ii, 2., False, True), ('WR_t1p80_a6p0_g2', L.masks_std, 5, sw_rs('t1p80_a6p0'), 2., False, True),
               ('WR_t0p75_a4p0_g2', L.masks_std, 5, sw_rs('t0p75_a4p0'), 2., False, True), ('WR_t0p75_a5p0_g2', L.masks_std, 5, sw_rs('t0p75_a5p0'), 2., False, True),
               ('WR_t0p75_a7p6_g2', L.masks_std, 5, sw_rs('t0p75_a7p6'), 2., False, True),
               ('W1_g0_trunc', masks_trunc, len(T_LIST), sw_w1, 0., False, True), ('W1_g0_age', masks_age, 2, sw_w1, 0., False, False)]
    counts = dict(arms=list(L.ARMS) + ['O'], no_safe_row={})
    for name, mf, Pm, sw, gap, signed, do_boot in configs:
        M = build(ds, mf, sw, gap, signed)
        n0, D0, nl0 = L.evaluate(M.sum(0), Pm)
        out = dict(n0=n0[0], D0=D0[0])
        if do_boot:
            nb, Db, nlb = L.boot(M, idx, Pm, logfile=LOG, tag=name)
            out.update(nb=nb, Db=Db)
            counts.setdefault('resamples_with_undefined_frontier', {})[name] = int((nlb > 0).any(1).sum())
        np.savez(L.HERE / ('rc_arr_%s_v01.npz' % name), **out)
        counts['no_safe_row'][name] = sum(int((~sw(d, d['clear'] > gap, gap).any(1)).sum()) for d in ds)
        L.log('%s done, %.0f s' % (name, time.time() - t0), file=LOG)
    # counts printed by the first program
    counts['pairs'] = sum(int(d['clear'].size) for d in ds)
    counts['unsafe_W1_gap0'] = sum(int((~(d['clear'] > 0)).sum()) for d in ds)
    counts['unsafe_WR075_gap0'] = sum(int((~(d['cache']['t0p75_a6p0'] > 0)).sum()) for d in ds)
    counts['unsafe_WR075_gap2'] = sum(int((~(d['cache']['t0p75_a6p0'] > 2)).sum()) for d in ds)
    counts['late_pairs_t0p75_a6p0_among_WR_safe_gap0'] = sum(int((d['late'] & (d['cache']['t0p75_a6p0'] > 0)).sum()) for d in ds)
    counts['n_evaluated_without_W1_safe_row'] = sum(int((~(d['clear'] > 0).any(1)).sum()) for d in ds)
    # zero-margin points, all evaluated decisions
    zm = {}
    for signed, lab in ((False, 'unsigned'), (True, 'signed')):
        M = build(ds, L.masks_all, sw_w1, 0., signed)
        n, S, O = L.unpack(np.atleast_2d(M.sum(0)), 1)
        for a in ('F0', 'CK3'):
            ai = L.ARMS.index(a)
            zm['%s_%s' % (a, lab)] = dict(caution_pct=float(100. * S[0, 0, ai, 0, 1] / S[0, 0, ai, 0, 2]), wrong_go_pct=float(100. * S[0, 0, ai, 0, 0] / n[0, 0]))
    counts['zero_margin_points_all'] = zm
    # post-stop segment per run
    seg = []
    for d in ds:
        after = d['k'] >= d['k_stop']
        seg.append(dict(run=d['run'], k_stop=d['k_stop'], n_after_stop_evaluated=int(after.sum()),
                        last_after_stop_s=(float(((d['k'][after] - d['k_stop']) * L.H).max()) if after.any() else None)))
    counts['post_stop_segment'] = seg
    # track age over the 35 evaluation runs
    age_ev = np.concatenate([d['prim_age'] for d in ds]); miss_ev = np.concatenate([d['prim_miss'] for d in ds])
    drops = []; young_stored = 0
    for d in ds:
        zg = np.load(L.STORED / (d['run'] + '.npz'), allow_pickle=False)
        age_all = np.asarray(zg['prim_age'], float)
        nd = int((np.diff(age_all) < 0).sum())
        if nd:
            drops.append(dict(run=d['run'], n=nd))
        young_stored += int((age_all < 4.).sum())
    counts['track'] = dict(n=int(age_ev.size), by_misses={str(v): int((miss_ev == v).sum()) for v in sorted(set(miss_ev.tolist()))},
                           min_track_age_s=float(age_ev.min()), age_drops_in_stored_decisions=drops,
                           stored_decisions_with_track_younger_than_4s=young_stored,
                           stored_not_evaluated=sum(d['n_stored'] - d['n'] for d in ds))
    # margin ratio per family and set: percentiles, rows of evaluated decisions; the rows outside the band by set, run, phase
    files = sorted(L.STORED.glob('*.npz'))
    fam = {}
    for f in files:
        with np.load(f, allow_pickle=False) as z:
            m = json.loads(str(z['meta'])); ev = z['evaluated'].astype(bool)
            cN = np.asarray(z['cN'], float)[ev]; cF = np.asarray(z['cF0'], float)[ev]; k = np.asarray(z['k'])
        ok = np.isfinite(cN) & np.isfinite(cF) & (cN > 0) & (cF > 0)
        with np.errstate(invalid='ignore', divide='ignore'):
            mm = 1. / np.sqrt(cN / cF)
        ph = None
        if m['family'] == 'lead_braking' and m['set'] == 'fit':
            with np.load(L.EXTRACT / (f.stem + '.npz'), allow_pickle=False) as ze:
                ph = np.broadcast_to(np.asarray(ze['phase'])[ev][:, None], ok.shape)[ok]
        fam.setdefault(m['family'], []).append(dict(run=f.stem, set=m['set'], m=mm[ok], rows_evaluated=int(ok.size), phase=ph))
    ratio = {}
    for fk, recs in fam.items():
        for st in ['all'] + sorted(set(r['set'] for r in recs)):
            rr = [r for r in recs if st == 'all' or r['set'] == st]
            m = np.concatenate([r['m'] for r in rr]); med = float(np.median(m)); off = np.abs(m / med - 1.) > 0.05
            ratio['%s|%s' % (fk, st)] = dict(runs=len(rr), rows=int(m.size), rows_evaluated=int(sum(r['rows_evaluated'] for r in rr)),
                                             median_margin_ratio=med, off5_share=float(off.mean()), off5_n=int(off.sum()),
                                             within5_share=float((~off).mean()), pct_1_5_25_50_75_95_99=np.percentile(m, [1, 5, 25, 50, 75, 95, 99]).tolist())
    counts['ratio'] = ratio
    recs = fam['lead_braking']
    med = float(np.median(np.concatenate([r['m'] for r in recs])))
    s9 = dict(n_off=0, by_set={}, n_runs_with_off_rows=0, by_phase_fit_only={'phase0': 0, 'phase1': 0, 'phase2': 0})
    for r in recs:
        off = np.abs(r['m'] / med - 1.) > 0.05
        k = int(off.sum()); s9['n_off'] += k; s9['by_set'][r['set']] = s9['by_set'].get(r['set'], 0) + k; s9['n_runs_with_off_rows'] += int(k > 0)
        if r['phase'] is not None:
            for p in range(3):
                s9['by_phase_fit_only']['phase%d' % p] += int((off & (r['phase'] == p)).sum())
    counts['S9'] = s9
    counts['seconds'] = time.time() - t0
    L.jdump(counts, L.HERE / 'rc_extra_counts_v01.json')
    L.log('rc_extra_v01 end, %.0f s' % (time.time() - t0), file=LOG)


if __name__ == '__main__':
    main()
