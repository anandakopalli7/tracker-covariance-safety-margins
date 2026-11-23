"""Recount of package C: test of the calibration plumbing (rc_core_v13.DoubleBoot, cover_two, smallest_level, mc_levels) on TOY
data (no run is read). New file, 19 Nov 2026 (Claude Fable 5.2).

A plain transcription of the method of revision_v11\\analysis\\rev_d_bootstrap_v01.py (D2) and revision_v12\\analysis\\
a9_2a_double_bootstrap_mc_v01.py, with A10's seeds and level grid, is run beside rc_core_v13 on a toy statistic (a ratio of
weighted sums of 35 fixed toy values, NaN when its denominator is not positive). The inner shares, the coverage at every level,
the calibrated level and the Monte Carlo SD must be equal.
Usage: python -I -B -X utf8 test_rc_calibration_v13.py      Output: out\\TEST_RC_CALIBRATION_v13<tag>.json
"""
import argparse, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rc_core_v13 as K


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--tag', default=''); a = ap.parse_args()
    outf = K.OUT / ('TEST_RC_CALIBRATION_v13%s.json' % a.tag)
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    n = 35
    g = np.random.default_rng(7)                              # toy data only
    x = g.lognormal(0., 1.2, n); y = g.normal(0.6, 1.0, n)

    def stat_fn(CN):
        CN = np.atleast_2d(np.asarray(CN, float))
        num = CN @ x; den = CN @ y
        with np.errstate(divide='ignore', invalid='ignore'):
            r = np.where(den > 0, num / den, np.nan)
        return np.column_stack([num / n, r])

    full = stat_fn(np.ones(n))[0]
    B1, B2 = 300, 200
    db = K.DoubleBoot(stat_fn, full, n, K.SEED_INNER, B1, B2, label='toy').run()
    # ---- plain transcription
    rng_o = np.random.default_rng(K.SEED_OUTER); rng_i = np.random.default_rng(K.SEED_INNER)
    IDX_O = rng_o.integers(0, n, (K.B_OUTER, n))
    p_lt = np.full((B1, 2), np.nan); p_le = np.full((B1, 2), np.nan)
    for b in range(B1):
        io = IDX_O[b]
        co = np.bincount(io, minlength=n).astype(float)
        oe = stat_fn(co)[0]
        ii = rng_i.integers(0, n, (K.B_INNER, n))[:B2]
        cn = np.zeros((B2, n))
        for q in range(B2):
            cn[q] = np.bincount(io[ii[q]], minlength=n)
        S = stat_fn(cn)
        for j in range(2):
            v = S[:, j]; v = v[np.isfinite(v)]
            if v.size == 0 or not np.isfinite(oe[j]):
                continue
            p_lt[b, j] = (v < full[j]).mean(); p_le[b, j] = (v <= full[j]).mean()

    def cover_two(lt, le, nom):
        al = 1. - nom
        ok = np.isfinite(lt)
        return float(((le[ok] >= al / 2. - 1e-12) & (lt[ok] <= 1. - al / 2. + 1e-12)).mean())

    def calibrate(lt, le):
        for nm in K.CAL_LEVELS:
            if cover_two(lt, le, float(nm)) >= 0.95:
                return float(nm)
        return None
    doc = dict(code='test_rc_calibration_v13.py', toy=True, n=n, outer=B1, inner=B2, stats=['mean', 'ratio'], checks={})
    ok_all = True
    IDX_MC = np.random.default_rng(K.SEED_MC).integers(0, B1, (K.B_MC, B1))[:300]
    for j, s in enumerate(doc['stats']):
        eq_sh = bool(np.array_equal(p_lt[:, j], db.p_lt[:, j], equal_nan=True) and np.array_equal(p_le[:, j], db.p_le[:, j], equal_nan=True))
        cov_a = [cover_two(p_lt[:, j], p_le[:, j], float(nm)) for nm in K.CAL_LEVELS]
        cov_b = [K.cover_two(db.p_lt[:, j], db.p_le[:, j], float(nm)) for nm in K.CAL_LEVELS]
        lv_a = calibrate(p_lt[:, j], p_le[:, j]); lv_b = K.smallest_level(db.p_lt[:, j], db.p_le[:, j])
        mc = []
        for q in range(IDX_MC.shape[0]):
            ix = IDX_MC[q]
            mc.append(calibrate(p_lt[ix, j], p_le[ix, j]))
        mc = np.array([1.0 if v is None else v for v in mc], float)        # 1.0 when none reaches 0.95 (CD_DEFINITIONS)
        sd_a = float(np.nanstd(mc, ddof=1))
        mcb = K.mc_levels(db.p_lt[:, j], db.p_le[:, j], 300)
        c = dict(inner_shares_equal=eq_sh, coverage_equal=bool(cov_a == cov_b), level_plain=lv_a, level_recount=lv_b,
                 level_equal=bool(lv_a == lv_b), mc_sd_plain=sd_a, mc_sd_recount=mcb['sd'],
                 mc_sd_equal=bool(sd_a == mcb['sd'] or abs(sd_a - mcb['sd']) < 1e-15), coverage_95=cov_b[0],
                 n_outer_valid=int(np.isfinite(db.p_lt[:, j]).sum()), rule=K.calibrate_stat(db, j, None, 300))
        ok_all = ok_all and eq_sh and c['coverage_equal'] and c['level_equal'] and c['mc_sd_equal']
        doc['checks'][s] = c
        print(s, {k: v for k, v in c.items() if k != 'rule'}, flush=True)
    doc['all_equal'] = bool(ok_all)
    print('ALL EQUAL' if ok_all else 'DIFFERENCES FOUND')
    print('written %s' % K.write_new(outf, doc))


if __name__ == '__main__':
    main()
