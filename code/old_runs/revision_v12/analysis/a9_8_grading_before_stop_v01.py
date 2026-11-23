"""Revision v12, AMENDMENT_09 ADDENDUM_01, A9-8: the partial oracles in the population before the lead's stop. New file,
19 Nov 2026. Construction as revision_v11/analysis/rev_g_partial_oracle_draws_v01.py (same draws): the partial oracle with share
p takes the oracle's critical values where u < p and the class average's elsewhere; 3 s commitment, step frontier, points.
Population: evaluated decisions before the lead's stop (truth phase 0 or 1; Table S22, T = 0), on its own frontier.
Also the braking prediction's and the acceleration margin's shares and frontier distances there (identity: Table S22's 0.289).
Usage: python -B -X utf8 a9_8_grading_before_stop_v01.py
"""
import time
import numpy as np
import a9_common_v01 as A
C = A.C; L = A.L

OUTF = A.OUT / 'A9_8_GRADING_BEFORE_STOP_v01.json'
if OUTF.exists():
    raise SystemExit('REFUSED: %s exists' % OUTF)
t00 = time.time()
runs = C.load_runs()
for r in runs:
    ev = r['ev']; ph = r['ph']
    r['masks_bs'] = (ev & (ph <= 1),)
PS = [0.25, 0.5, 0.75]; NM = ['P25', 'P50', 'P75']
base = C.tables(runs, ('W1',), ['F0', 'E', 'CK3', 'A1'], masks_key='masks_bs')


def one(seed):
    U = np.random.default_rng(seed).random(9307)
    pos = 0
    for r in runs:
        u = U[pos:pos + r['n_dec']]; pos += r['n_dec']
        for p, nm in zip(PS, NM):
            r['crit'][nm] = np.where((u < p)[:, None], r['crit']['E'], r['crit']['F0'])
            r['sel'].pop(nm, None)
    X = dict(base); X.update(C.tables(runs, ('W1',), NM, masks_key='masks_bs'))
    pt = C.points(X, ['E', 'CK3', 'A1'] + NM, pops=[0])[0]
    return pt


rec = one(20261118)
draws = [one(20261200 + i) for i in range(50)]
sh = lambda pt, nm: L.ratio(pt['D'][nm], pt['denE'])
doc = dict(code='a9_8_grading_before_stop_v01.py', status='post hoc, descriptive; AMENDMENT_09 ADDENDUM_01 (A9-8)',
           n=rec['n'], R_pp=rec['denE'] / L.NLEV,
           of_record={nm: sh(rec, nm) for nm in NM},
           draws={nm: dict(mean=float(np.mean([sh(d, nm) for d in draws])), min=float(np.min([sh(d, nm) for d in draws])),
                           max=float(np.max([sh(d, nm) for d in draws]))) for nm in NM},
           RR_CK3=sh(rec, 'CK3'), RR_A1=sh(rec, 'A1'),
           D_CK3_deceq=L.dec_eq(rec['D']['CK3'], rec['n']), D_A1_deceq=L.dec_eq(rec['D']['A1'], rec['n']),
           R_deceq=L.dec_eq(rec['denE'], rec['n']))
o = doc['of_record']
doc['grades_by_rule'] = bool(o['P25'] < o['P50'] < o['P75'] and o['P25'] > 0)
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
A.write_out(OUTF, doc)
print({k: doc[k] for k in ('n', 'R_pp', 'of_record', 'draws', 'RR_CK3', 'RR_A1', 'D_CK3_deceq', 'D_A1_deceq', 'grades_by_rule')})
