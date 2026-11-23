"""Recount (second program): item 5 of RECOUNT_BRIEF_v01.md (R9), the double bootstrap.

  outer = default_rng(20261120).integers(0, 35, (2000, 35))
  rng   = default_rng(20261121)                       one inner stream
  for b = 0, 1, ...: ii = rng.integers(0, 35, (1000, 35)); inner samples = outer[b][ii]
Truth = the full-sample value. Per outer sample and statistic: number of valid inner values (positive denominator), number
below the truth and number at or below it. Coverage of the two-sided percentile interval at nominal level 1 - a = share of
outer samples with share(inner <= truth) >= a/2 and share(inner < truth) <= 1 - a/2.
The two inequalities are evaluated in exact integer arithmetic (the levels are decimal fractions); the same rule evaluated
in floating point is reported beside it, because at a = 0.05 the float (1 - 0.95)/2 is slightly above 0.025 = 25/1000.

Usage: python -B -X utf8 rc_double_v01.py [n_outer]     (default 2000; checkpoints every 100 outer samples, resumes)"""
import json, sys, time
from fractions import Fraction
import numpy as np
import rc_lib_v01 as L
from rc_items_v01 import STATS, stat_values

LOG = L.HERE / 'rc_double_v01_log.txt'
CKPT = L.HERE / 'rc_double_ckpt_v01.npz'
N_OUTER = 2000; N_INNER = 1000
QS = (0.05, 0.5, 2.5, 5., 50., 95., 97.5, 99.5, 99.95)
GRID_LEVELS = ['0.%03d' % i for i in range(900, 1000)] + ['0.9995', '0.9999', '1.0']
REPORT_LEVELS = ['0.900', '0.950', '0.990', '0.999', '1.0']


def run(n_outer):
    t0 = time.time()
    ds = L.load_all()
    M = L.build_M(ds, L.masks_all, 'W1', 0., False)
    _, D0, _ = L.evaluate(M.sum(0), 1)
    truth = {k: float(v[0]) for k, v in stat_values(D0[:, 0]).items()}
    outer = np.random.default_rng(20261120).integers(0, 35, (N_OUTER, 35))
    rng = np.random.default_rng(20261121)
    ns = len(STATS)
    cnts = np.zeros((N_OUTER, ns, 5), np.int64)        # n_valid, n_lt, n_le, n_lt_reflected, n_le_reflected
    oval = np.full((N_OUTER, ns), np.nan)              # the outer sample's own value
    iq = np.full((N_OUTER, ns, len(QS)), np.nan)       # inner percentiles QS (diagnostic)
    start = 0
    if CKPT.exists():
        z = np.load(CKPT, allow_pickle=False)
        if int(z['n_inner']) == N_INNER and np.array_equal(z['outer'], outer):
            start = int(z['done']); cnts = z['cnts']; oval = z['oval']; iq = z['iq']
            rng.bit_generator.state = json.loads(str(z['state']))
            L.log('resumed at outer sample %d' % start, file=LOG)
    for b in range(start, n_outer):
        ii = rng.integers(0, 35, (N_INNER, 35))
        samp = outer[b][ii]
        _, D, _ = L.evaluate(L.counts_from_idx(samp, 35) @ M, 1)
        sv = stat_values(D[:, 0])
        _, Do, _ = L.evaluate(L.counts_from_idx(outer[b][None, :], 35) @ M, 1)
        so = stat_values(Do[:, 0])
        for si, s in enumerate(STATS):
            v = sv[s]; v = v[np.isfinite(v)]
            oval[b, si] = so[s][0]
            refl = 2. * so[s][0] - truth[s]
            cnts[b, si] = (v.size, int((v < truth[s]).sum()), int((v <= truth[s]).sum()),
                           int((v < refl).sum()) if np.isfinite(refl) else -1, int((v <= refl).sum()) if np.isfinite(refl) else -1)
            if v.size:
                iq[b, si] = np.percentile(v, QS)
        if (b + 1) % 100 == 0 or b + 1 == n_outer:
            np.savez(CKPT, done=b + 1, n_inner=N_INNER, outer=outer, cnts=cnts, oval=oval, iq=iq,
                     state=json.dumps(rng.bit_generator.state))
            L.log('  outer %d / %d, %.0f s' % (b + 1, n_outer, time.time() - t0), file=LOG)
    return truth, cnts[:n_outer], oval[:n_outer], iq[:n_outer]


def covered_exact(nv, nlt, nle, level):
    """share(<= truth) >= a/2 and share(< truth) <= 1 - a/2, a = 1 - level, in exact arithmetic. Arrays over outer samples."""
    f = Fraction(level); p, q = f.numerator, f.denominator
    return (2 * q * nle >= (q - p) * nv) & (2 * q * nlt <= (q + p) * nv)


def covered_float(nv, nlt, nle, level):
    a = 1. - float(level)
    return (nle / nv >= a / 2) & (nlt / nv <= 1 - a / 2)


def summarise(truth, cnts, oval, iq):
    rec = np.load(L.HERE / 'rc_record_stats_v01.npz')
    out = dict(item='R9 double bootstrap', n_outer=int(cnts.shape[0]), n_inner=N_INNER, grid_levels=GRID_LEVELS, stats={})
    for si, s in enumerate(STATS):
        nv = cnts[:, si, 0]; use = nv > 0
        nvu = nv[use]; nlt = cnts[use, si, 1]; nle = cnts[use, si, 2]; nltr = cnts[use, si, 3]; nler = cnts[use, si, 4]
        nout = int(use.sum())
        e = dict(truth=truth[s], outer_samples_used=nout, inner_values_left_out_total=int((N_INNER - nv).sum()),
                 inner_equal_to_truth_total=int((nle - nlt).sum()), coverage={}, coverage_float_rule={}, coverage_grid={})
        cal = None
        for lv in GRID_LEVELS:
            c = int(covered_exact(nvu, nlt, nle, lv).sum())
            e['coverage_grid'][lv] = c / nout
            if cal is None and 100 * c >= 95 * nout:
                cal = lv
        for lv in REPORT_LEVELS:
            e['coverage'][lv] = int(covered_exact(nvu, nlt, nle, lv).sum()) / nout
            e['coverage_float_rule'][lv] = int(covered_float(nvu, nlt, nle, lv).sum()) / nout
        e['coverage_basic_95'] = int(covered_exact(nvu, nltr, nler, '0.950').sum()) / nout
        e['calibrated_level'] = None if cal is None else float(cal)
        v = rec[s]; v = v[np.isfinite(v)]
        if cal is not None:
            f = Fraction(cal); a = 1 - f
            lo, hi = np.percentile(v, [float(100 * a / 2), float(100 * (1 - a / 2))])
            e['record_interval_at_calibrated_level'] = [float(lo), float(hi)]
        e['record_interval_95'] = L.pct(v)
        e['record_min_max'] = [float(v.min()), float(v.max())]
        # the same search with the float rule, to show whether the two rules ever disagree
        calf = None
        for lv in GRID_LEVELS:
            if covered_float(nvu, nlt, nle, lv).sum() / nout >= 0.95:
                calf = lv; break
        e['calibrated_level_float_rule'] = None if calf is None else float(calf)
        e['miss_below_95'] = int((2 * 1000 * nle < 50 * nvu).sum()) / nout       # truth below the inner 2.5% point
        e['miss_above_95'] = int((2 * 1000 * nlt > 1950 * nvu).sum()) / nout     # truth above the inner 97.5% point
        e['outer_value_mean'] = float(np.nanmean(oval[:, si])); e['outer_value_sd'] = float(np.nanstd(oval[:, si], ddof=1))
        out['stats'][s] = e
    return out


def main():
    n_outer = int(sys.argv[1]) if len(sys.argv) > 1 else N_OUTER
    L.log('rc_double_v01 start, %d outer x %d inner' % (n_outer, N_INNER), file=LOG)
    truth, cnts, oval, iq = run(n_outer)
    out = summarise(truth, cnts, oval, iq)
    L.jdump(out, L.HERE / ('RECOUNT_item5_double_v01%s.json' % ('' if n_outer == N_OUTER else '_partial%d' % n_outer)))
    L.log('rc_double_v01 end', file=LOG)


if __name__ == '__main__':
    main()
