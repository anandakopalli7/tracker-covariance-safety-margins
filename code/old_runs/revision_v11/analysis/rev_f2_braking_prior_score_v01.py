"""Revision v11, post hoc checks S20 and S18 (ARS review of draft v10), step 2: scoring. New file, 18 Nov 2026.
Descriptive; declared in AMENDMENT_08 (smaller checks). Input: out/ck/<run>.npz from rev_f1_braking_prior_extract_v01.py.

S20  The braking prior at 1, 2, 3, 4, 5, 6 and 7 m/s^2 on the 35 evaluation runs, 3 s commitment, step frontier: RR (share of
     the 3 s oracle's room) and RR0 (against the perfect oracle), by population and phase-weighted, with 95% run-bootstrap
     percentile intervals (the draw of record); zero-margin points. The 3 m/s^2 value reproduces the value of record.
     The same sweep on the 20 tuning runs is of record (OXSB_CTL_RESULTS_v02.json) and is copied into the output for reference.
S18  The braking prior (3 m/s^2) on the 20 benign-driving tuning runs, in which no lead brakes: evaluated decisions, the room,
     the prior's distance from the class average in decisions, and the zero-margin points (caution %, wrong go %) of the class
     average and the prior. Bootstrap over the 20 runs (20,000 resamples, seed 20261125).
Usage: python -B -X utf8 rev_f2_braking_prior_score_v01.py
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rev_common_v01 as C                   # noqa: E402
L = C.L

OUT = HERE / 'out' / 'REV_F2_BRAKING_PRIOR_v01.json'
if OUT.exists():
    sys.exit('REFUSED: %s exists' % OUT)
t00 = time.time()
CK = HERE / 'out' / 'ck'
A0 = [1., 2., 3., 4., 5., 6., 7.]


def nm(x):
    return ('%g' % x).replace('.', 'p')


doc = dict(code='rev_f2_braking_prior_score_v01.py', status='post hoc, descriptive; AMENDMENT_08', S20={}, S18={})

# ------------------------------------------------------------------------------------------------ S20 evaluation runs
runs = C.load_runs()
CNT = C.cnt_of_record()
ndiff = 0
for r in runs:
    x = np.load(CK / (r['run'] + '.npz'), allow_pickle=False)
    assert np.array_equal(x['k'], r['k'])
    for a0 in A0:
        r['crit']['CK' + nm(a0) + 'x'] = x['cCK' + nm(a0)]
    ndiff += int((~((x['cCK3'] == r['crit']['CK3']) | (np.isnan(x['cCK3']) & np.isnan(r['crit']['CK3'])))).sum())
doc['S20']['cCK3_entries_differing_from_record'] = ndiff
arms = ['CK' + nm(a0) + 'x' for a0 in A0]
tab = ['F0', 'E', 'O'] + arms
names = ['E', 'O'] + arms
X = C.tables(runs, ('W1',), tab)
pts = C.points(X, names, pops=range(5))
R = C.boot(X, names, (), [0, 1, 2, 3, 4], CNT)
items = [(C.POPS[pi], pts[pi], R[pi]) for pi in range(5)] + [('strat', C.strat_point(pts, names), C.strat_boot(R, names))]
for pop, pe, Rp in items:
    n = pe['n']; den0 = pe['D']['O']; denE = pe['denE']
    e = dict(n=n, denE_dec_eq=L.dec_eq(denE, n), den0_dec_eq=L.dec_eq(den0, n), arms={})
    for a0, a in zip(A0, arms):
        D = pe['D'][a]
        e['arms'][nm(a0)] = dict(a0=a0, D_dec_eq=L.dec_eq(D, n), rrE=L.summ(C.rat(Rp['D'][a], Rp['denE']), L.ratio(D, denE)),
                                 rr0=L.summ(C.rat(Rp['D'][a], Rp['D']['O']), L.ratio(D, den0)))
    doc['S20'][pop] = e
Tsum = {a: X[a].sum(axis=0) for a in X}
doc['S20']['zero_margin_points_all'] = {
    a: dict(caution_pct=float(100. * Tsum[a][0, 0, 2] / Tsum[a][0, 0, 3]), wrong_go_pct=float(100. * Tsum[a][0, 0, 1] / Tsum[a][0, 0, 0]))
    for a in ['F0'] + arms}
ctl = json.loads((C.P / '09_redesign' / 'm2_decisions' / 'openloop' / 'OXSB_CTL_RESULTS_v02.json').read_text(encoding='utf-8'))
doc['S20']['tuning_runs_of_record'] = dict(
    source='OXSB_CTL_RESULTS_v02.json (13 Nov 2026; 20 lead-braking tuning runs)',
    rr_all={k: dict(point=v['point'], ci=[v['lo'], v['hi']]) for k, v in ctl['rr_all'].items() if k.startswith('CK') and 'g' not in k},
    by_population={p: {k: v for k, v in d['rr'].items() if k.startswith('CK') and 'g' not in k}
                   for p, d in ctl['point_by_population'].items()})
print('S20 done (%.0f s)' % (time.time() - t00), flush=True)

# ------------------------------------------------------------------------------------------------ S18 benign tuning runs
bruns = []
for f in sorted(C.STORED.glob('p2_c1109_tune_*.npz')):
    z = np.load(f, allow_pickle=False)
    m = json.loads(str(z['meta']))
    if m['family'] != 'benign':
        continue
    x = np.load(CK / (m['run'] + '.npz'), allow_pickle=False)
    assert np.array_equal(x['k'], z['k'])
    ev = z['evaluated'].astype(bool); v0 = z['v0']
    bruns.append(dict(run=m['run'], desired=float(m['desired']), ev=ev, v0=v0, vbar=z['vbar'], idx55=z['idx55'],
                      clear1=L.clean_clear(z['clear']), masks=(ev, ev & (v0 > C.VMIN)), n_dec=len(z['k']),
                      crit={'F0': z['cF0'], 'E': z['cE'], 'N': z['cN'], 'CK3': x['cCK3']}, sel={}, late={}, cache={}))
doc['S18']['n_runs'] = len(bruns)
if bruns:
    tabb = ['F0', 'E', 'O', 'N', 'CK3']; namesb = ['E', 'O', 'N', 'CK3']
    Xb = C.tables(bruns, ('W1',), tabb)
    ptb = C.points(Xb, namesb, pops=range(2))
    CNTb = L.boot_counts(len(bruns), 20000, 20261125)
    Rb = C.boot(Xb, namesb, (), [0, 1], CNTb)
    Tb = {a: Xb[a].sum(axis=0) for a in Xb}
    for pi, pop in enumerate(['all', 'moving']):
        pe = ptb[pi]; Rp = Rb[pi]; n = pe['n']
        e = dict(n=n, R_pp=pe['denE'] / L.NLEV, denE=L.summ_den(Rp['denE'], pe['denE']), den0=L.summ_den(Rp['D']['O'], pe['D']['O']),
                 denE_dec_eq=L.dec_eq(pe['denE'], n), den0_dec_eq=L.dec_eq(pe['D']['O'], n), arms={}, zero_margin={})
        for a in ('N', 'CK3'):
            D = pe['D'][a]
            e['arms'][a] = dict(D_pp=D / L.NLEV, D_dec_eq=dict(point=L.dec_eq(D, n), ci=L.pct(L.dec_eq(Rp['D'][a], Rp['n']))),
                                rrE=L.summ(C.rat(Rp['D'][a], Rp['denE']), L.ratio(D, pe['denE'])),
                                rr0=L.summ(C.rat(Rp['D'][a], Rp['D']['O']), L.ratio(D, pe['D']['O'])))
        for a in ('F0', 'CK3', 'E'):
            T = Tb[a][0, pi, :]
            e['zero_margin'][a] = dict(caution_pct=float(100. * T[2] / T[3]) if T[3] else None, wrong_go_pct=float(100. * T[1] / T[0]),
                                       wrong_go_n=int(T[1]))
        # caution at the largest scale reached by both (whole-curve cost): mean caution of the prior minus the class average over g
        cF = 100. * Tb['F0'][:, pi, 2] / Tb['F0'][:, pi, 3]; cK = 100. * Tb['CK3'][:, pi, 2] / Tb['CK3'][:, pi, 3]
        wF = 100. * Tb['F0'][:, pi, 1] / Tb['F0'][:, pi, 0]; wK = 100. * Tb['CK3'][:, pi, 1] / Tb['CK3'][:, pi, 0]
        e['over_the_scale_grid'] = dict(mean_caution_diff_pp=float(np.nanmean(cK - cF)), max_caution_diff_pp=float(np.nanmax(cK - cF)),
                                        mean_wrong_go_diff_pp=float(np.nanmean(wK - wF)),
                                        max_wrong_go_F0=float(np.nanmax(wF)), max_wrong_go_CK3=float(np.nanmax(wK)))
        doc['S18'][pop] = e
    # how often the prior changes the selection at zero margin and at g = 1
    nch0 = nch1 = nev = 0
    g1 = int(np.argmin(np.abs(C.GRID - 1.0)))
    for r in bruns:
        s0 = C.sel_of(r, 'F0'); s1 = C.sel_of(r, 'CK3')
        nev += int(r['ev'].sum())
        nch0 += int(((s0[0] != s1[0]) & r['ev']).sum()); nch1 += int(((s0[g1] != s1[g1]) & r['ev']).sum())
    doc['S18']['selection_changed'] = dict(evaluated=nev, at_zero_margin=nch0, at_g_1=nch1)
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
OUT.write_text(C.jdump(doc), encoding='utf-8')
print('written %s (%.0f s)' % (OUT, time.time() - t00))
