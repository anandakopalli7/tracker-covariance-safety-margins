"""Recount (second program): item 4 of RECOUNT_BRIEF_v01.md (R12b), one margin scale per phase of the lead's motion.

For each arm the points are all triples (g0, g1, g2) of the 202-value grid:
  wrong go = 100 * (w0[g0] + w1[g1] + w2[g2]) / n
  caution  = 100 * (cs0[g0] + cs1[g1] + cs2[g2]) / (cn0[g0] + cn1[g1] + cn2[g2])
(w = wrong-go count, cs = sum of caution terms, cn = number of truly safe selections, per phase).
Per-phase-scale step frontier Fps at the pooled single-scale levels; every arm other than F0 and E gets F0's single-scale
zero-margin point prepended.

How the 202^3 triples are handled (no enumeration): for a level L, "caution <= L" is the same as
sum_p a_p <= 0 with a_p = 100 cs_p - L cn_p, so the frontier at L is min sum_p w_p subject to sum_p a_p <= 0. Each phase's
distinct (w, cs, cn) triples are reduced to their (w, a) Pareto set, two phases are paired and the third is searched.
The comparison is made twice, with thresholds -DELTA and +DELTA; if the two answers differ (a triple lies within rounding
of the level) the level is recomputed by enumeration with the caution formula itself. The diagonal triples (g, g, g) are
the single-scale points: they are taken from the single-scale curve (Fps = min(F1, triples)), so that the two frontiers
share their floating-point values on the diagonal.
Check: at the point (and for a few resamples) every arm's Fps is recomputed by full enumeration of the deduplicated triples.

Usage: python -B -X utf8 rc_item4_v01.py [nrows]     (default 400 = the first 400 rows of the draw of record)"""
import sys, time
import numpy as np
import rc_lib_v01 as L

LOG = L.HERE / 'rc_item4_v01_log.txt'
A = len(L.ARMS); AI = {a: i for i, a in enumerate(L.ARMS)}
FIVE = ('N', 'NA', 'AM', 'CK3', 'Q')
DELTA = 1e-6
KEYS = (['den1', 'gain_F0', 'den_ps', 'den0_ps', 'den0_1', 'n'] + ['Dps_' + a for a in FIVE] + ['D1_' + a for a in FIVE])
# the same sums when the per-phase-scale frontier uses the triples' own floating-point values only (no single-scale diagonal)
KEYS_ALT = ['alt_gain_F0', 'alt_den_ps', 'alt_den0_ps'] + ['alt_Dps_' + a for a in FIVE]


def masks4(d):
    return [np.ones(d['n'], bool), d['phase'] == 0, d['phase'] == 1, d['phase'] == 2]


def phase_points(S, ai):
    """Distinct (w, cs, cn) of the arm per phase, sorted by w (then cs, cn)."""
    return [np.unique(S[p, ai], axis=0) for p in (1, 2, 3)]


def tri_exact_level(U, Lv):
    U0, U1, U2 = U
    best = np.inf
    with np.errstate(invalid='ignore', divide='ignore'):
        for i in range(U0.shape[0]):
            cs = (U0[i, 1] + U1[:, 1])[:, None] + U2[None, :, 1]
            cn = (U0[i, 2] + U1[:, 2])[:, None] + U2[None, :, 2]
            ok = (100. * cs / cn) <= Lv
            if ok.any():
                w = (U0[i, 0] + U1[:, 0])[:, None] + U2[None, :, 0]
                best = min(best, float(w[ok].min()))
    return best


def tri_frontier(U, lev):
    """Lowest total wrong-go COUNT over the triples with pooled caution <= level, per level (inf if none)."""
    res = np.full(lev.size, np.inf); nbf = 0
    safe_cn = max(float(X[:, 2].min()) for X in U) > 0          # then the pooled count of truly safe selections is > 0
    for li in range(lev.size):
        Lv = lev[li]
        if not safe_cn:
            res[li] = tri_exact_level(U, Lv); nbf += 1; continue
        fr = []
        for X in U:
            m = np.minimum.accumulate(100. * X[:, 1] - Lv * X[:, 2])
            keep = np.empty(m.size, bool); keep[0] = True; keep[1:] = m[1:] < m[:-1]
            fr.append((X[keep, 0], m[keep]))
        fr.sort(key=lambda t: t[0].size)
        (wA, aA), (wB, aB), (wC, aC) = fr
        th = -(aA[:, None] + aB[None, :]).ravel(); wab = (wA[:, None] + wB[None, :]).ravel()
        rev = aC[::-1]; nC = aC.size
        k1 = np.searchsorted(rev, th - DELTA, side='right'); k2 = np.searchsorted(rev, th + DELTA, side='right')
        o1 = k1 > 0; o2 = k2 > 0
        lo = float((wab[o1] + wC[nC - k1[o1]]).min()) if o1.any() else np.inf
        hi = float((wab[o2] + wC[nC - k2[o2]]).min()) if o2.any() else np.inf
        if lo == hi:
            res[li] = lo
        else:
            res[li] = tri_exact_level(U, Lv); nbf += 1
    return res, nbf


def tri_brute(U, lev):
    """Full enumeration of the deduplicated triples (check only)."""
    U0, U1, U2 = U
    with np.errstate(invalid='ignore', divide='ignore'):
        cs = ((U0[:, 1][:, None] + U1[:, 1][None, :])[:, :, None] + U2[:, 1][None, None, :]).ravel()
        cn = ((U0[:, 2][:, None] + U1[:, 2][None, :])[:, :, None] + U2[:, 2][None, None, :]).ravel()
        c = 100. * cs / cn
    del cs, cn
    w = ((U0[:, 0][:, None] + U1[:, 0][None, :])[:, :, None] + U2[:, 0][None, None, :]).ravel().astype(np.float32)
    c[~np.isfinite(c)] = np.inf
    o = np.argsort(c, kind='stable')
    cso = c[o]; del c
    cm = np.minimum.accumulate(w[o]); del w, o
    j = np.searchsorted(cso, lev, side='right') - 1
    res = np.where(j >= 0, cm[np.maximum(j, 0)].astype(float), np.inf)
    return res, int(cso.size)


def one(agg, brute=False):
    """All item-4 quantities for one pooled statistics vector."""
    n, S, O = L.unpack(np.atleast_2d(agg), 4)
    n = n[0]; S = S[0]; O = O[0]
    if n[0] != n[1] + n[2] + n[3]:
        raise RuntimeError('phases 0-2 do not add up to all evaluated decisions')
    _, D1, _, cur = L.evaluate(np.atleast_2d(agg), 4, want_curves=True)
    lev = cur[0]['lev'][0]; fr1 = {a: f[0] for a, f in cur[0]['fr'].items()}
    out = dict(n=float(n[0]), den1=float(np.sum(fr1['F0'] - fr1['E'])), den0_1=float(np.sum(fr1['F0'] - fr1['O'])))
    for a in FIVE:
        out['D1_' + a] = float(np.sum(fr1['F0'] - fr1[a]))
    fps = {}; alt = {}; info = dict(points={}, n_enumerated_levels=0, brute_max_abs_diff={})
    w0 = cur[0]['W'][0, 0, 0]
    for a in L.ARMS:
        U = phase_points(S, AI[a])
        res, nbf = tri_frontier(U, lev)
        info['points'][a] = [int(X.shape[0]) for X in U]; info['n_enumerated_levels'] += nbf
        with np.errstate(invalid='ignore'):
            tri = np.where(np.isfinite(res), 100. * res / n[0], np.nan)
        fps[a] = np.fmin(fr1[a], tri)
        alt[a] = tri if a in ('F0', 'E') else np.fmin(tri, w0)
        if brute:
            rb, ntri = tri_brute(U, lev)
            trib = np.where(np.isfinite(rb), 100. * rb / n[0], np.nan)
            fb = np.fmin(fr1[a], trib)
            info['brute_max_abs_diff'][a] = float(np.nanmax(np.abs(fb - fps[a]))) if np.array_equal(np.isnan(fb), np.isnan(fps[a])) else float('inf')
            info.setdefault('brute_triples', {})[a] = ntri
    out['gain_F0'] = float(np.sum(fr1['F0'] - fps['F0']))
    out['den_ps'] = float(np.sum(fps['F0'] - fps['E']))
    out['den0_ps'] = float(np.sum(fps['F0'] - fr1['O']))
    for a in FIVE:
        out['Dps_' + a] = float(np.sum(fps['F0'] - fps[a]))
    out['alt_gain_F0'] = float(np.sum(fr1['F0'] - alt['F0']))
    out['alt_den_ps'] = float(np.sum(alt['F0'] - alt['E']))
    out['alt_den0_ps'] = float(np.sum(alt['F0'] - fr1['O']))
    for a in FIVE:
        out['alt_Dps_' + a] = float(np.sum(alt['F0'] - alt[a]))
    info['alt_max_abs_diff_from_primary'] = {a: (float(np.nanmax(np.abs(alt[a] - fps[a]))) if np.array_equal(np.isnan(alt[a]), np.isnan(fps[a])) else float('inf')) for a in L.ARMS}
    info['undefined_levels'] = {a: int(np.isnan(fps[a]).sum()) for a in L.ARMS}
    info['undefined_levels_single'] = {a: int(np.isnan(fr1[a]).sum()) for a in fr1}
    return out, info


def derived(v):
    """Ratios of the reported sums (v: dict of scalars or arrays)."""
    with np.errstate(invalid='ignore', divide='ignore'):
        d = dict(gain_F0_over_den1=(v['gain_F0'] / v['den1'], v['den1']), den_ps_over_den1=(v['den_ps'] / v['den1'], v['den1']),
                 den0_ps_over_den0_1=(v['den0_ps'] / v['den0_1'], v['den0_1']))
        for a in FIVE:
            d['RRps_' + a] = (v['Dps_' + a] / v['den_ps'], v['den_ps'])
            d['RR0ps_' + a] = (v['Dps_' + a] / v['den0_ps'], v['den0_ps'])
            d['RR1_' + a] = (v['D1_' + a] / v['den1'], v['den1'])
            d['RR01_' + a] = (v['D1_' + a] / v['den0_1'], v['den0_1'])
    return d


def main():
    nrows = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    t0 = time.time()
    L.log('rc_item4_v01 start, %d rows' % nrows, file=LOG)
    ds = L.load_all()
    if any((d['phase'] == 3).any() for d in ds):
        raise RuntimeError('an evaluated decision has phase 3')
    M = L.build_M(ds, masks4, 'W1', 0., False)
    pt, info = one(M.sum(0), brute=True)
    L.log('point', pt, file=LOG); L.log('info', info, file=LOG)
    out = dict(item='R12b one margin scale per phase', nrows=nrows, delta=DELTA, point_info=info,
               sums={k: dict(point=pt[k]) for k in KEYS + KEYS_ALT}, ratios={k: dict(point=float(v[0])) for k, v in derived(pt).items()})
    L.jdump(out, L.HERE / 'RECOUNT_item4_v01_point.json')
    idx = L.draw_of_record()[:nrows]
    cnt = L.counts_from_idx(idx, 35)
    vals = {k: np.full(nrows, np.nan) for k in KEYS + KEYS_ALT}
    n_enum = 0; n_undef = 0; n_alt = 0; chk = []
    for b in range(nrows):
        r, inf = one(cnt[b] @ M, brute=(b < 3))
        for k in KEYS + KEYS_ALT:
            vals[k][b] = r[k]
        n_alt += int(max(inf['alt_max_abs_diff_from_primary'].values()) > 0)
        n_enum += inf['n_enumerated_levels']; n_undef += int(sum(inf['undefined_levels'].values()) > 0)
        if b < 3:
            chk.append(inf['brute_max_abs_diff'])
        if b in (0, 2, 9) or (b + 1) % 25 == 0:
            L.log('  resample %d / %d, %.0f s' % (b + 1, nrows, time.time() - t0), file=LOG)
    for k in KEYS + KEYS_ALT:
        out['sums'][k]['ci'] = L.pct(vals[k]); out['sums'][k]['n_left_out'] = int((~np.isfinite(vals[k])).sum())
    for k, (v, den) in derived(vals).items():
        keep = np.isfinite(v) & (den > 0)
        out['ratios'][k]['ci'] = L.pct(v[keep]); out['ratios'][k]['n_left_out'] = int((~keep).sum())
    out['resample_info'] = dict(levels_recomputed_by_enumeration=n_enum, resamples_with_an_undefined_frontier_level=n_undef,
                                resamples_where_alt_differs_from_primary=n_alt,
                                brute_check_first_resamples=chk)
    out['seconds'] = time.time() - t0
    np.savez(L.HERE / 'rc_item4_boot_v01.npz', **vals)
    L.jdump(out, L.HERE / 'RECOUNT_item4_v01.json')
    L.log('item 4 done %.0f s' % (time.time() - t0), file=LOG)


if __name__ == '__main__':
    main()
