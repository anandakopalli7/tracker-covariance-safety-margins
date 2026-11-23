"""Package E, first program: the analysis of A10 7.5 on E3 (and E3b), from e_collect_v01 outputs.

Writer: session E (Claude Opus 5.5). The independent second program (different model, from the amendment text and the truth
logs) recounts every value this program prints (A10 10.1(b)).

Paired by case, each arm against F0 at the same level (the IMM pair: N_IMM against F0_IMM); Z against F0 at each level.
A pair enters a comparison iff both runs are valid (e_collect_v01 rule).
  Contact share   difference d = p_arm - p_ref with counts a (both contact), b (arm only), c (ref only), n pairs:
                  d = (b - c) / n; Newcombe's hybrid score 95% interval for paired proportions (Newcombe 1998, method 10;
                  Fagerland, Lydersen & Laake 2014): Wilson 95% intervals (l1, u1) of p_arm = (a + b)/n and (l2, u2) of
                  p_ref = (a + c)/n; phi = cov / sqrt((a+b)(c+d0)(a+c)(b+d0)) with cov = a d0 - b c, corrected as Newcombe
                  (1998): if cov > 0, cov := max(cov - n/2, 0) (d0 = pairs with neither contact; phi = 0 if the denominator is
                  0); this is statsmodels' confint_proportions_paired(method='newcomb') and reproduces its documented example
                  [[10, 5], [2, 20]] -> (-0.0643926050711, 0.2211160178958) (corrected after the build review, M6);
                  L = d - sqrt((p_arm-l1)^2 - 2 phi (p_arm-l1)(u2-p_ref) + (u2-p_ref)^2),
                  U = d + sqrt((u1-p_arm)^2 - 2 phi (u1-p_arm)(p_ref-l2) + (p_ref-l2)^2). Exact McNemar: two-sided
                  p = min(1, 2 P(X <= min(b, c))), X ~ Binomial(b + c, 1/2); p = 1 if b + c = 0.
  Time lost       mean paired difference (arm - ref) over pairs in which neither run has a contact; 95% percentile interval
                  from a case bootstrap: the n valid pairs (cases) are resampled, default_rng(20261922).integers(0, n,
                  (20000, n)) (one fresh generator of record per comparison, one index matrix for all its outcomes), and the
                  mean is recomputed over the resampled pairs without contact; resamples with no such pair are dropped
                  (revised 19 Nov before any E data: the earlier draft resampled only the pairs without contact).
  Other outcomes  descriptive: per arm means; paired mean differences with the same bootstrap over the pairs in which the
                  outcome is defined for both runs (impact speed: both in contact; rest gap: neither in contact; peak
                  deceleration, RMS jerk, fallback share: all pairs).
  Classification  in this order: "safer at no extra cost" if U < 0 and the time-lost upper end < 0.5 s; "safer at a cost" if
                  U < 0 and that upper end >= 0.5 s; "equivalent" if (L, U) lies inside (-0.10, 0.10) and the time-lost
                  interval inside (-0.5, 0.5) s; "worse" if L > 0; otherwise "inconclusive". If the time-lost interval does not
                  exist (fewer than 2 pairs without contact) only "worse" and "inconclusive" can be reached.
  Hypotheses      E-H1: CK3 vs F0 at lo; E-H2: N vs F0 at lo; E-H3: N_IMM vs F0_IMM at lo. Everything else descriptive.
  Low power       carried from LOCK_A10_2b (all F0 contact shares in E2 below 0.05).
Usage: python -I -B e3_analyse_v01.py --e3 OUTCOMES_E3.json [--e3b OUTCOMES_E3B.json] --lock2b MATCHED.json --out E3_RESULTS.json
"""
import argparse, json, math, pathlib
import numpy as np

SEED = 20261922
NBOOT = 20000
Z = 1.959963984540054
EQ_CONTACT = 0.10
EQ_TIME = 0.5
OUTS = ('impact_speed_mps', 'rest_gap_m', 'peak_decel_mps2', 'rms_jerk_mps3', 'fallback_share', 'time_lost_s')
HYP = {('E_CK3', 'lo'): 'E-H1', ('E_N', 'lo'): 'E-H2', ('E_N_IMM', 'lo'): 'E-H3'}
LOCK2 = pathlib.Path(__file__).resolve().parents[3] / 'LOCK_A10_2.txt'


def wilson(k, n):
    if n == 0: return (float('nan'), float('nan'))
    p = k / n; den = 1 + Z * Z / n; cen = p + Z * Z / (2 * n)
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n))
    return ((cen - half) / den, (cen + half) / den)


def newcombe_paired(a, b, c, d0):
    n = a + b + c + d0
    if n == 0: return dict(n=0)
    p1 = (a + b) / n; p2 = (a + c) / n; diff = (b - c) / n
    l1, u1 = wilson(a + b, n); l2, u2 = wilson(a + c, n)
    den = (a + b) * (c + d0) * (a + c) * (b + d0)
    cov = a * d0 - b * c
    if cov > 0:
        cov = max(cov - n / 2, 0.)                 # Newcombe's correction of the correlation estimate
    phi = 0. if den == 0 else cov / math.sqrt(den)
    dl = math.sqrt(max(0., (p1 - l1) ** 2 - 2 * phi * (p1 - l1) * (u2 - p2) + (u2 - p2) ** 2))
    du = math.sqrt(max(0., (u1 - p1) ** 2 - 2 * phi * (u1 - p1) * (p2 - l2) + (p2 - l2) ** 2))
    return dict(n=n, a=a, b=b, c=c, d=d0, p_arm=p1, p_ref=p2, diff=diff, lo=diff - dl, hi=diff + du, phi=phi)


def mcnemar_exact(b, c):
    m = b + c
    if m == 0: return 1.
    k = min(b, c)
    tail = sum(math.comb(m, i) for i in range(k + 1)) / 2 ** m
    return min(1., 2 * tail)


def boot_mean(diffs, idx=None):
    """diffs: one value per pair, NaN where the outcome is undefined for that pair. idx: the comparison's (NBOOT, n) case
    resample matrix. Point = mean over defined pairs; interval = percentiles of the resampled means over defined pairs."""
    x = np.asarray(diffs, float); ok = np.isfinite(x); m = int(ok.sum())
    point = float(x[ok].mean()) if m else float('nan')
    if m < 2 or idx is None: return dict(m=m, mean=point, lo=float('nan'), hi=float('nan'), resamples=0)
    xs = x[idx]; okk = np.isfinite(xs); cnt = okk.sum(axis=1)
    keep = cnt > 0
    bm = np.where(okk, xs, 0.).sum(axis=1)[keep] / cnt[keep]
    return dict(m=m, mean=point, lo=float(np.percentile(bm, 2.5)), hi=float(np.percentile(bm, 97.5)), resamples=int(keep.sum()))


def classify(ct, tl):
    U, L = ct['hi'], ct['lo']
    has_tl = tl is not None and math.isfinite(tl.get('hi', float('nan')))
    if U < 0 and has_tl and tl['hi'] < EQ_TIME: return 'safer at no extra cost'
    if U < 0 and has_tl and tl['hi'] >= EQ_TIME: return 'safer at a cost'
    if has_tl and -EQ_CONTACT < L and U < EQ_CONTACT and -EQ_TIME < tl['lo'] and tl['hi'] < EQ_TIME: return 'equivalent'
    if L > 0: return 'worse'
    return 'inconclusive'


def compare(table, arm, ref, level_arm, level_ref):
    A = {r['case']: r for r in table if r['arm'] == arm and (level_arm is None or r['level'] == level_arm)}
    R = {r['case']: r for r in table if r['arm'] == ref and (level_ref is None or r['level'] == level_ref)}
    cases = sorted(set(A) & set(R))
    pairs = [(A[c], R[c]) for c in cases if A[c]['valid'] and R[c]['valid']]
    dropped = [c for c in cases if not (A[c]['valid'] and R[c]['valid'])]
    a = b = c_ = d0 = 0
    for x, y in pairs:
        cx, cy = x['outcomes']['contact'], y['outcomes']['contact']
        if cx and cy: a += 1
        elif cx: b += 1
        elif cy: c_ += 1
        else: d0 += 1
    ct = newcombe_paired(a, b, c_, d0)
    ct['mcnemar_exact_p'] = mcnemar_exact(b, c_)
    out = dict(arm=arm, ref=ref, level_arm=level_arm, level_ref=level_ref, cases=len(cases), pairs=len(pairs), dropped_pairs=dropped, contact=ct)
    desc = {}
    n = len(pairs)
    idx = np.random.default_rng(SEED).integers(0, n, (NBOOT, n)) if n else None
    for k in OUTS:
        if k in ('time_lost_s', 'rest_gap_m'):
            sel = [(x, y) for x, y in pairs if not x['outcomes']['contact'] and not y['outcomes']['contact']]
        elif k == 'impact_speed_mps':
            sel = [(x, y) for x, y in pairs if x['outcomes']['contact'] and y['outcomes']['contact']]
        else:
            sel = pairs
        sel_ids = {id(x) for x, _ in sel}
        diffs = [(x['outcomes'][k] - y['outcomes'][k]) if (id(x) in sel_ids and x['outcomes'][k] is not None and y['outcomes'][k] is not None)
                 else float('nan') for x, y in pairs]
        desc[k] = dict(paired_diff=boot_mean(diffs, idx),
                       mean_arm=float(np.mean([x['outcomes'][k] for x, _ in pairs if x['outcomes'][k] is not None])) if pairs else None,
                       mean_ref=float(np.mean([y['outcomes'][k] for _, y in pairs if y['outcomes'][k] is not None])) if pairs else None)
    out['time_lost'] = desc['time_lost_s']['paired_diff']
    out['descriptive'] = desc
    out['classification'] = classify(ct, out['time_lost']) if ct['n'] else 'no pairs'
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--e3', required=True); ap.add_argument('--e3b'); ap.add_argument('--lock2b', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    if not LOCK2.exists(): raise SystemExit('REFUSED: LOCK_A10_2.txt does not exist')
    lock = json.loads(pathlib.Path(a.lock2b).read_text(encoding='utf-8'))
    low_power = bool(lock['levels']['low_power'])
    e3 = json.loads(pathlib.Path(a.e3).read_text(encoding='utf-8'))['runs']
    res = dict(schema='E3_RESULTS_V01', code='e3_analyse_v01.py', low_power=low_power, comparisons=[])
    for lv in ('lo', 'hi'):
        for arm in ('E_N', 'E_CK3', 'E_TG', 'E_PS'):
            res['comparisons'].append(dict(compare(e3, arm, 'E_F0', lv, lv), stage='E3', hypothesis=HYP.get((arm, lv))))
        res['comparisons'].append(dict(compare(e3, 'E_N_IMM', 'E_F0_IMM', lv, lv), stage='E3', hypothesis=HYP.get(('E_N_IMM', lv))))
        res['comparisons'].append(dict(compare(e3, 'E_Z', 'E_F0', None, lv), stage='E3', hypothesis=None))
    if a.e3b:
        e3b = json.loads(pathlib.Path(a.e3b).read_text(encoding='utf-8'))['runs']
        for kind in sorted({r['lead_variant'] for r in e3b}):
            sub = [r for r in e3b if r['lead_variant'] == kind]
            for arm in ('E_N', 'E_CK3', 'E_TG', 'E_PS'):
                res['comparisons'].append(dict(compare(sub, arm, 'E_F0', 'lo', 'lo'), stage='E3b', lead_variant=kind, hypothesis=None))
    pathlib.Path(a.out).write_text(json.dumps(res, indent=1, allow_nan=True), encoding='utf-8')
    for c in res['comparisons']:
        print(c['stage'], c.get('lead_variant', ''), c['arm'], 'vs', c['ref'], c['level_arm'], c.get('hypothesis') or '', c['pairs'], c['classification'])


if __name__ == '__main__':
    main()
