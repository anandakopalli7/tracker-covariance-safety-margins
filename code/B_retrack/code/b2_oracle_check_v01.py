"""v13 package B: why RR_gl(N_B2) exceeds RR_gl(E5_B2) on the old runs (coordinator question, 19 Nov 2026 ~20:20 EST). POST HOC,
descriptive diagnostics; nothing here is pre-registered. New file, 19 Nov 2026 (Claude Opus 5.5). Writes out\\banalysis\\B2_ORACLE_CHECK_v01.json.

(1) Rebuilds E5_B2 exactly as b_analysis_v01.py does (B2's own arrays: F0_B2 with P-bar_B2, E_B2, N_B2; m_x, A_x from B2's margin ratio
    sqrt(c_F0 / c_N) at binding rows; ranks u_i from F0_B2 / E_B2; same population (all evaluated decisions), 3 s commitment, gridless
    step frontier) and checks its point against out\\banalysis\\B_B2_v01.json.
(2) Interval of RR_gl(N_B2) - RR_gl(E5_B2) on the same resamples (first 2,000 rows of the draw of record).
(3) What E5 does not contain, measured on B2's rows:
    - amplitude band: share of binding rows whose ratio lies outside [m (1 - A), m (1 + A)] (A from q05 / q95: about 10% by construction);
    - shape: E5 multiplies every row and constraint of a decision by ONE factor; N_B2's ratio varies across the rows of a decision. Per
      evaluated decision with >= 2 binding rows: (max - min) / median of the row ratios; median, q90, share above 5%.
(4) A post-hoc reference E5q: the same ranks, but f_i = the B2 ratio distribution's own quantile at u_i (full amplitude, no band);
    RR_gl(E5q) and RR_gl(N_B2) - RR_gl(E5q) with intervals.
Usage: python -I -B -X utf8 b2_oracle_check_v01.py [variant=B2] [nboot=2000]
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numpy as np
import b_analysis_v01 as BA
S = BA.S; L = BA.L; C = BA.C


def main():
    x = sys.argv[1] if len(sys.argv) > 1 else 'B2'; NB = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    t00 = time.time()
    runs = BA.load(x)
    rat = S.margin_ratios(runs, 'N', 'F0'); rs = S.ratio_summary(rat)
    u, _ = S.e5_u(runs, 'F0', 'E')
    S.add_oracle(runs, 'E5x', 'F0', rs['median'], rs['A'], u)
    q = [np.quantile(rat, uu) for uu in u]                     # f_i = empirical ratio quantile at u_i
    for r, f in zip(runs, q):
        r['crit']['E5q'] = r['crit']['F0'] / (f * f)[:, None]
    G = S.gridless(runs, ['F0', 'E', 'N', 'E5x', 'E5q'])
    p = S.rr_gl(G, 'F0', 'E', ['N', 'E5x', 'E5q'], pop=0)
    rec = json.loads((BA.OUTD / ('B_%s_v01.json' % x)).read_text(encoding='utf-8'))
    doc = dict(code='b2_oracle_check_v01.py', status='POST HOC diagnostic (not pre-registered)', variant=x, nboot=NB,
               check_1=dict(RR_N=p['RR']['N'], RR_N_record=rec['points']['all']['RR']['N'], RR_E5x=p['RR']['E5x'],
                            RR_E5x_record=rec['points']['all']['RR']['E5x'], m_x=rs['median'], A_x=rs['A'],
                            same=bool(abs(p['RR']['N'] - rec['points']['all']['RR']['N']) < 1e-12 and abs(p['RR']['E5x'] - rec['points']['all']['RR']['E5x']) < 1e-12),
                            construction='E5_x = c_F0x / f_i^2, f_i = m_x (1 + A_x (2 u_i - 1)); m_x, A_x from x\'s own ratio sqrt(c_F0x / c_Nx) at binding rows; '
                                         'u_i from x\'s own F0_x / E_x; population all evaluated decisions; 3 s commitment; gridless step frontier; '
                                         'the same run dicts, gridless events and resamples as N_x'))
    lo, hi = rs['median'] * (1 - rs['A']), rs['median'] * (1 + rs['A'])
    within_dec = []
    for r in runs:
        cN = r['crit']['N']; cF = r['crit']['F0']
        for i in np.flatnonzero(r['ev']):
            ok = np.isfinite(cN[i]) & np.isfinite(cF[i]) & (cN[i] > 0) & (cF[i] > 0)
            if ok.sum() >= 2:
                v = np.sqrt(cF[i][ok] / cN[i][ok])
                within_dec.append((v.max() - v.min()) / np.median(v))
    wd = np.array(within_dec)
    doc['diagnostics'] = dict(share_rows_outside_band=float(np.mean((rat < lo) | (rat > hi))), band=[lo, hi],
                              ratio_q01_q99=[float(np.quantile(rat, 0.01)), float(np.quantile(rat, 0.99))],
                              within_decision_spread=dict(n_decisions=int(wd.size), median=float(np.median(wd)), q90=float(np.quantile(wd, 0.9)),
                                                          share_above_5pct=float(np.mean(wd > 0.05))))
    doc['points'] = dict(RR_N=p['RR']['N'], RR_E5x=p['RR']['E5x'], RR_E5q=p['RR']['E5q'],
                         diff_N_minus_E5x=p['RR']['N'] - p['RR']['E5x'], diff_N_minus_E5q=p['RR']['N'] - p['RR']['E5q'])
    CNT = C.cnt_of_record()[:NB]
    b = S.boot_gl(G, 'F0', 'E', ['N', 'E5x', 'E5q'], CNT, pop=0)
    with np.errstate(invalid='ignore', divide='ignore'):
        ok = np.isfinite(b['denE']) & (b['denE'] > 0)
        rr = {a: np.where(ok, b['D'][a] / b['denE'], np.nan) for a in ('N', 'E5x', 'E5q')}
    doc['intervals'] = dict(RR_N=L.summ(rr['N'], p['RR']['N']), RR_E5x=L.summ(rr['E5x'], p['RR']['E5x']), RR_E5q=L.summ(rr['E5q'], p['RR']['E5q']),
                            diff_N_minus_E5x=L.summ(rr['N'] - rr['E5x'], doc['points']['diff_N_minus_E5x']),
                            diff_N_minus_E5q=L.summ(rr['N'] - rr['E5q'], doc['points']['diff_N_minus_E5q']))
    doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    (BA.OUTD / ('%s_ORACLE_CHECK_v01.json' % x)).write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    print(json.dumps(dict(check=doc['check_1'], diag=doc['diagnostics'], points=doc['points'],
                          diff_ci=doc['intervals']['diff_N_minus_E5x']['ci'], diffq_ci=doc['intervals']['diff_N_minus_E5q']['ci']), default=float))


if __name__ == '__main__':
    main()
