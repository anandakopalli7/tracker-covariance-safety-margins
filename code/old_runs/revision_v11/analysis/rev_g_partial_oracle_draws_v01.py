"""Revision v11, post hoc check S19 (ARS review of draft v10): the partial oracles over 50 random draws. New file, 18 Nov 2026.
Descriptive; AMENDMENT_08 (smaller checks). Of record, the partial oracles use one draw (default_rng(20261118)).
Here: for draw i = 0..49, u = default_rng(20261200 + i).random(9307), one uniform per stored decision in (run name, k) order;
the partial oracle with share p takes the oracle's critical values where u < p and the class average's elsewhere, p in
{0.25, 0.5, 0.75}. 3 s commitment, step frontier, points: RR by population (each on its own frontier) and phase-weighted.
Reported: mean, minimum, maximum and the 5th-95th percentiles over the 50 draws, beside the value of the draw of record.
Usage: python -B -X utf8 rev_g_partial_oracle_draws_v01.py
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rev_common_v01 as C                   # noqa: E402
L = C.L

OUT = HERE / 'out' / 'REV_G_PARTIAL_DRAWS_v01.json'
if OUT.exists():
    sys.exit('REFUSED: %s exists' % OUT)
t00 = time.time()
runs = C.load_runs()
PS = [0.25, 0.5, 0.75]; NM = ['P25', 'P50', 'P75']
POPS = ['all', 'moving', 'phase0', 'phase1', 'phase2', 'strat']
base = C.tables(runs, ('W1',), ['F0', 'E'])


def one(seed):
    U = np.random.default_rng(seed).random(9307)
    pos = 0
    for r in runs:
        u = U[pos:pos + r['n_dec']]; pos += r['n_dec']
        for p, nm in zip(PS, NM):
            r['crit'][nm] = np.where((u < p)[:, None], r['crit']['E'], r['crit']['F0'])
            r['sel'].pop(nm, None)
    X = dict(base); X.update(C.tables(runs, ('W1',), NM))
    pts = C.points(X, ['E'] + NM, pops=range(5))
    sp = C.strat_point(pts, ['E'] + NM)
    out = {}
    for pi, pop in enumerate(POPS[:5]):
        out[pop] = [L.ratio(pts[pi]['D'][nm], pts[pi]['denE']) for nm in NM]
    out['strat'] = [L.ratio(sp['D'][nm], sp['denE']) for nm in NM]
    return out


rec = one(20261118)
draws = [one(20261200 + i) for i in range(50)]
doc = dict(code='rev_g_partial_oracle_draws_v01.py', status='post hoc, descriptive; AMENDMENT_08', n_draws=50,
           seeds='default_rng(20261200 + i), i = 0..49', pops={})
for pop in POPS:
    A = np.array([dr[pop] for dr in draws])
    doc['pops'][pop] = {nm: dict(of_record=float(rec[pop][j]), mean=float(np.nanmean(A[:, j])), min=float(np.nanmin(A[:, j])),
                                 max=float(np.nanmax(A[:, j])), p5=float(np.nanpercentile(A[:, j], 5)), p95=float(np.nanpercentile(A[:, j], 95)),
                                 share_below_zero=float(np.mean(A[:, j] < 0))) for j, nm in enumerate(NM)}
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
OUT.write_text(C.jdump(doc), encoding='utf-8')
for pop in POPS:
    print(pop, {nm: 'rec %.3f mean %.3f [%.3f, %.3f]' % (v['of_record'], v['mean'], v['min'], v['max']) for nm, v in doc['pops'][pop].items()})
print('written (%.0f s)' % (time.time() - t00))
