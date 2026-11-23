"""Revision v12, AMENDMENT_09 A9-1 (review item R9): grid placebo, offset family and gridless frontier. New file, 19 Nov 2026.
(a) Placebo P: F0's critical scales / 1.1029^2. 3 s commitment; populations all, ego moving, phases 0-2; RR(P), RR(N), RR(N) - RR(P),
    D in decision-equivalents; the draw of record (20,000 resamples, seed 20261113); percentile and basic intervals.
(b) Offset family: F0's critical scales / 10^(0.025 u), u = 0.05..1.00; RR points, all decisions.
(c) Gridless: every margin scale in [0, 1e3] at which a selection changes; R, RR of N, P, NA, AM, CK3, Q; D(N, F0), D(N, P);
    intervals from the first 2,000 resamples of the draw of record (levels rebuilt in each).
Identity checks: the gridless curves evaluated at the 202 grid scales equal the grid tables of record (F0, N, E; all populations).
Usage: python -B -X utf8 a9_1_placebo_gridless_v01.py
"""
import time
import numpy as np
import a9_common_v01 as A
C = A.C; L = A.L

OUTF = A.OUT / 'A9_1_PLACEBO_GRIDLESS_v01.json'
if OUTF.exists():
    raise SystemExit('REFUSED: %s exists' % OUTF)
t00 = time.time()
runs = C.load_runs(); NRUN = len(runs)
A.add_placebo(runs, 'P')
U = [round(0.05 * k, 2) for k in range(1, 21)]
for u in U:
    A.add_placebo(runs, 'U%.2f' % u, A.GSTEP ** u)
CNT = C.cnt_of_record()
POPS = [0, 1, 2, 3, 4]
PN = ['all', 'moving', 'phase0', 'phase1', 'phase2']
doc = dict(code='a9_1_placebo_gridless_v01.py', status='post hoc, descriptive; AMENDMENT_09 A9-1', ratio=A.RATIO,
           grid_step=A.GSTEP, populations=PN)

# ------------------------------------------------------------------------------------------------ (a) placebo on the grid
ARMS = ['N', 'P', 'NA', 'A1', 'CK3', 'Q']
X = C.tables(runs, ('W1',), ['F0', 'E'] + ARMS)
pts = C.points(X, ['E'] + ARMS, pops=POPS)
R = C.boot(X, ['E'] + ARMS, (), POPS, CNT)
a = {}
for pi, pn in zip(POPS, PN):
    p = pts[pi]; b = R[pi]; den = p['denE']; n = p['n']
    ent = dict(n=n, R_pp=den / L.NLEV, R=L.summ(b['denE'] / L.NLEV, den / L.NLEV))
    for x in ARMS:
        ent['RR_' + x] = L.summ(C.rat(b['D'][x], b['denE']), L.ratio(p['D'][x], den))
        ent['D_%s_deceq' % x] = dict(point=L.dec_eq(p['D'][x], n), ci=L.pct(L.dec_eq(b['D'][x], b['n'])))
    ent['RR_N_minus_P'] = L.summ(C.rat(b['D']['N'] - b['D']['P'], b['denE']), L.ratio(p['D']['N'] - p['D']['P'], den))
    ent['D_N_minus_P_deceq'] = dict(point=L.dec_eq(p['D']['N'] - p['D']['P'], n),
                                    ci=L.pct(L.dec_eq(b['D']['N'] - b['D']['P'], b['n'])))
    ent['D_N_vs_P_direct_deceq'] = ent['D_N_minus_P_deceq']['point']
    a[pn] = ent
doc['a_placebo_grid'] = a
print('(a) done (%.0f s): all RR(N) %.5f RR(P) %.5f' % (time.time() - t00, a['all']['RR_N']['point'], a['all']['RR_P']['point']),
      flush=True)

# ------------------------------------------------------------------------------------------------ (b) offset family
UN = ['U%.2f' % u for u in U]
XU = C.tables(runs, ('W1',), ['F0', 'E'] + UN)
pu = C.points(XU, ['E'] + UN, pops=[0])[0]
doc['b_offset_family'] = dict(u=U, RR=[L.ratio(pu['D'][x], pu['denE']) for x in UN],
                              D_deceq=[L.dec_eq(pu['D'][x], pu['n']) for x in UN])
rr = np.array(doc['b_offset_family']['RR'])
doc['b_offset_family']['RR_min_max'] = [float(rr.min()), float(rr.max())]
print('(b) done (%.0f s)' % (time.time() - t00), flush=True)

# ------------------------------------------------------------------------------------------------ (c) gridless
GL = ['F0', 'E', 'N', 'P', 'NA', 'A1', 'CK3', 'Q']
G = A.gridless_sources(runs, GL, lambda r: r['clear1'] > 0.)
print('gridless events built (%.0f s): %s' % (time.time() - t00, {k: int(v.b.size) for k, v in G.items()}), flush=True)
# identity: the gridless curve at the grid scales equals the grid tables
idc = {}
for x in ('F0', 'N', 'E'):
    g = G[x]
    full = g.curve()                                         # (1 + nb, npop, NST)
    bk = g.b[g.keep] if g.b.size else np.zeros(0)
    # state at grid scale gk: after every breakpoint b < gk
    j = np.searchsorted(bk, C.GRID, side='left')             # number of breakpoints strictly below gk
    Tg = full[j]                                             # (202, npop, NST)
    Tr = X[x].sum(axis=0) if x in X else None
    idc[x] = float(np.abs(Tg - Tr).max())
doc['c_identity_grid_points_max_abs_diff'] = idc
print('identity: %s' % idc, flush=True)


def ev_gridless(curves, pop=0):
    T = {x: curves[x][:, pop, :] for x in curves}
    return L.eval_scoring(T, ['E', 'N', 'P', 'NA', 'A1', 'CK3', 'Q'])


full_c = {x: G[x].curve() for x in GL}
cp = {}
for pi, pn in zip(POPS, PN):
    e = ev_gridless(full_c, pi); n = e['n']
    ent = dict(n=n, R_pp=e['denE'] / L.NLEV, n_points={x: int(full_c[x].shape[0]) for x in GL})
    for x in ['N', 'P', 'NA', 'A1', 'CK3', 'Q']:
        ent['RR_' + x] = L.ratio(e['D'][x], e['denE']); ent['D_%s_deceq' % x] = L.dec_eq(e['D'][x], n)
    ent['RR_N_minus_P'] = L.ratio(e['D']['N'] - e['D']['P'], e['denE'])
    ent['D_N_minus_P_deceq'] = L.dec_eq(e['D']['N'] - e['D']['P'], n)
    cp[pn] = ent
print('(c) points (%.0f s): all RR(N) %.5f RR(P) %.5f' % (time.time() - t00, cp['all']['RR_N'], cp['all']['RR_P']), flush=True)
NB = 2000
keys = ['denE', 'n'] + ['D_' + x for x in ['N', 'P', 'NA', 'A1', 'CK3', 'Q']]
BB = {k: np.full(NB, np.nan) for k in keys}
for b in range(NB):
    w = CNT[b]
    cb = {x: G[x].curve(w, pops=[0]) for x in GL}
    e = ev_gridless(cb, 0)
    BB['denE'][b] = e['denE']; BB['n'][b] = e['n']
    for x in ['N', 'P', 'NA', 'A1', 'CK3', 'Q']:
        BB['D_' + x][b] = e['D'][x]
    if (b + 1) % 250 == 0:
        print('  gridless bootstrap %d / %d (%.0f s)' % (b + 1, NB, time.time() - t00), flush=True)
p0 = cp['all']; e0 = ev_gridless(full_c, 0)
ci = dict(R=L.summ(BB['denE'] / L.NLEV, e0['denE'] / L.NLEV))
for x in ['N', 'P', 'NA', 'A1', 'CK3', 'Q']:
    ci['RR_' + x] = L.summ(C.rat(BB['D_' + x], BB['denE']), L.ratio(e0['D'][x], e0['denE']))
    ci['D_%s_deceq' % x] = dict(point=L.dec_eq(e0['D'][x], e0['n']), ci=L.pct(L.dec_eq(BB['D_' + x], BB['n'])))
ci['RR_N_minus_P'] = L.summ(C.rat(BB['D_N'] - BB['D_P'], BB['denE']), L.ratio(e0['D']['N'] - e0['D']['P'], e0['denE']))
ci['D_N_minus_P_deceq'] = dict(point=L.dec_eq(e0['D']['N'] - e0['D']['P'], e0['n']),
                               ci=L.pct(L.dec_eq(BB['D_N'] - BB['D_P'], BB['n'])))
cp['all_intervals'] = dict(nboot=NB, draw='first %d rows of the draw of record (seed 20261113)' % NB, **ci)
doc['c_gridless'] = cp
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
doc['common_sha256'] = L.sha256_file(A.HERE / 'a9_common_v01.py')
A.write_out(OUTF, doc)
print('written %s (%.0f s)' % (OUTF, time.time() - t00))
