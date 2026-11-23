"""Revision v12, AMENDMENT_09 A9-4(b, c) (review items R18, S18): where the room lies, and the lead's estimated state.
New file, 19 Nov 2026. 3 s commitment, step frontier, grid of record.

(b) Attribution: for a population, at each of its 201 caution levels the frontier point of F0 and of source A (the point that
    attains the step frontier, first in caution order among equal minima; for A other than F0 and E, point 0 is F0's zero-margin
    point, as in optA_lib_v02.curves_w). Per decision, contribution = sum over levels of (F0's selected row is a wrong go) minus
    (A's selected row is a wrong go), divided by 201: decision-equivalents that sum exactly to dec_eq(D(F0, A), n).
    Summed by time since the lead's stop and by the tracker's lead speed estimate; A = E, CK3, A1 (AM), N; populations all,
    lead braking, after the stop. The rows selected in F0's after-stop wrong goes: fallback row, speeding up, holding, slowing.
(c) Medians of the lead's estimated state by time since the stop and since the onset; mean NIS and normalised velocity error by
    phase (one value per distinct update), with the first second after the onset separately.
Usage: python -B -X utf8 a9_4b_attribution_v01.py
"""
import time
import numpy as np
import a9_common_v01 as A
C = A.C; L = A.L

OUTF = A.OUT / 'A9_4B_ATTRIBUTION_v01.json'
if OUTF.exists():
    raise SystemExit('REFUSED: %s exists' % OUTF)
t00 = time.time()
runs = C.load_runs()
LEAD = A.HERE / 'out' / 'lead'
for r in runs:
    z = np.load(LEAD / (r['run'] + '.npz'), allow_pickle=False)
    if not np.array_equal(z['k'], r['k']) or not np.array_equal(z['phase'], r['ph']):
        raise SystemExit('REFUSED: lead arrays of %s do not match' % r['run'])
    r['lead'] = {k: z[k] for k in z.files}
    ph = r['ph']; now = z['now']
    i1 = np.nonzero(ph >= 1)[0]; i2 = np.nonzero(ph == 2)[0]
    r['t_onset'] = now - now[i1[0]] if i1.size else np.full(now.size, np.nan)
    r['t_stop'] = now - now[i2[0]] if i2.size else np.full(now.size, np.nan)
ARMS = ['E', 'CK3', 'A1', 'N']
X = C.tables(runs, ('W1',), ['F0'] + ARMS)
POPS = {'all': 0, 'lead_braking': 3, 'after_stop': 4}
TS_EDGES = [0., 1., 2., 5., 10., np.inf]
TS_NAMES = ['before stop', '0-1 s', '1-2 s', '2-5 s', '5-10 s', '>=10 s']
VH_EDGES = [-np.inf, 0.5, 1., 2., np.inf]
VH_NAMES = ['<=0.5', '0.5-1', '1-2', '>2']


def ts_bin(r):
    ts = r['t_stop']; b = np.zeros(ts.size, int)
    after = r['ph'] == 2
    b[after] = 1 + np.clip(np.searchsorted(TS_EDGES, ts[after], side='right') - 1, 0, len(TS_EDGES) - 2)
    return b


def vh_bin(r):
    v = r['lead']['vhat']
    return np.clip(np.searchsorted(VH_EDGES, v, side='right') - 1, 0, len(VH_EDGES) - 2)


doc = dict(code='a9_4b_attribution_v01.py', status='post hoc, descriptive; AMENDMENT_09 A9-4(b, c)', ts_bins=TS_NAMES, vh_bins=VH_NAMES)
att = {}
for pn, pi in POPS.items():
    Tsum = {a: X[a].sum(axis=0)[:, pi, :] for a in X}
    cur = L.curves_w(Tsum, 0)
    cF0, wF0 = cur['F0']; cE, wE = cur['E']
    lev = L.levels_of(cF0, cE, cF0[0])
    n = float(Tsum['F0'][0, 0])
    fF0, aF0 = A.frontier_argmin(cF0, wF0, lev)
    cntF0 = np.bincount(aF0[aF0 >= 0], minlength=len(C.GRID)).astype(float)
    ent = dict(n=n)
    for a in ARMS:
        fA, aA = A.frontier_argmin(cur[a][0], cur[a][1], lev)
        D = float(np.sum(fF0 - fA))
        if a == 'E':
            cntA = np.bincount(aA[aA >= 0], minlength=len(C.GRID)).astype(float); cnt0 = 0.
        else:                                  # point 0 = F0's g = 0 point; point k = A's grid index k - 1
            cnt0 = float((aA == 0).sum()); cntA = np.bincount(aA[aA >= 1] - 1, minlength=len(C.GRID)).astype(float)
        ts_sum = np.zeros(len(TS_NAMES)); vh_sum = np.zeros(len(VH_NAMES)); ts_n = np.zeros(len(TS_NAMES)); vh_n = np.zeros(len(VH_NAMES))
        tot = 0.
        rows_f0 = dict(fallback=0., faster=0., hold=0., slower=0.)
        for r in runs:
            m = r['masks'][pi]
            safe = r['clear1'] > 0.
            ar = np.arange(r['n_dec'])
            sF0 = C.sel_of(r, 'F0'); sA = C.sel_of(r, a)          # (G, n)
            wgF0 = (~safe[ar[None, :], sF0]) & m[None, :]
            wgA = (~safe[ar[None, :], sA]) & m[None, :]
            contrib = cntF0 @ wgF0 - cntA @ wgA
            if a != 'E':
                contrib = contrib - cnt0 * wgF0[0]
            contrib = contrib / L.NLEV
            tot += contrib.sum()
            tb = ts_bin(r); vb = vh_bin(r)
            ts_sum += np.bincount(tb[m], weights=contrib[m], minlength=len(TS_NAMES))
            vh_sum += np.bincount(vb[m], weights=contrib[m], minlength=len(VH_NAMES))
            ts_n += np.bincount(tb[m], minlength=len(TS_NAMES)); vh_n += np.bincount(vb[m], minlength=len(VH_NAMES))
            if a == 'E':                           # rows of F0's wrong goes at its frontier points, level-weighted
                for g in np.nonzero(cntF0)[0]:
                    sel = sF0[g]; wgm = wgF0[g]
                    vsel = r['vbar'][ar, sel]
                    fb = sel == r['idx55']
                    rows_f0['fallback'] += cntF0[g] * float((wgm & fb).sum())
                    rows_f0['faster'] += cntF0[g] * float((wgm & ~fb & (vsel > r['v0'] + 0.1)).sum())
                    rows_f0['hold'] += cntF0[g] * float((wgm & ~fb & (np.abs(vsel - r['v0']) <= 0.1)).sum())
                    rows_f0['slower'] += cntF0[g] * float((wgm & ~fb & (vsel < r['v0'] - 0.1)).sum())
        ent[a] = dict(D_deceq=L.dec_eq(D, n), attributed_total=tot, check_abs_diff=abs(tot - L.dec_eq(D, n)),
                      by_time_since_stop=dict(zip(TS_NAMES, ts_sum.tolist())), n_by_time_since_stop=dict(zip(TS_NAMES, ts_n.tolist())),
                      by_vhat=dict(zip(VH_NAMES, vh_sum.tolist())), n_by_vhat=dict(zip(VH_NAMES, vh_n.tolist())))
        if a == 'E':
            totw = sum(rows_f0.values())
            ent['F0_wrong_go_rows_level_weighted_share'] = {k: (v / totw if totw else float('nan')) for k, v in rows_f0.items()}
    att[pn] = ent
    print('%s: %s (%.0f s)' % (pn, {a: round(ent[a]['D_deceq'], 2) for a in ARMS}, time.time() - t00), flush=True)
doc['b_attribution'] = att

# ------------------------------------------------------------------------------------------------ (c) the lead's estimated state
def med(v):
    v = v[np.isfinite(v)]
    return [float(np.median(v)), float(np.percentile(v, 25)), float(np.percentile(v, 75)), int(v.size)] if v.size else None


cat = {k: [] for k in ('ph', 't_stop', 't_onset', 'vhat', 'v_true', 'ahat_long', 'dx_pred1', 'dx_pred3', 'age', 'nis', 'nees',
                       'key', 'v0')}
for r in runs:
    ev = r['ev']; z = r['lead']
    cat['ph'].append(r['ph'][ev]); cat['t_stop'].append(r['t_stop'][ev]); cat['t_onset'].append(r['t_onset'][ev])
    for k1, k2 in (('vhat', 'vhat'), ('v_true', 'v_true'), ('ahat_long', 'ahat_long'), ('dx_pred1', 'dx_pred1'),
                   ('dx_pred3', 'dx_pred3'), ('age', 'age'), ('nis', 'nis_last'), ('nees', 'nees_v')):
        cat[k1].append(z[k2][ev])
    cat['v0'].append(r['v0'][ev])
    st = np.round(z['now'][ev] - z['age'][ev], 3)
    cat['key'].append(np.array(['%s|%d|%.3f' % (r['run'], t, s) for t, s in zip(z['track_id'][ev], st)]))
cat = {k: np.concatenate(v) for k, v in cat.items()}
tab = {}
after = cat['ph'] == 2
for lo, hi, nm in ((0, 1, '0-1 s'), (1, 2, '1-2 s'), (2, 5, '2-5 s'), (5, 10, '5-10 s'), (10, np.inf, '>=10 s')):
    s = after & (cat['t_stop'] >= lo) & (cat['t_stop'] < hi)
    tab['after stop ' + nm] = {k: med(cat[k][s]) for k in ('vhat', 'v_true', 'ahat_long', 'dx_pred1', 'dx_pred3', 'age', 'v0')}
    tab['after stop ' + nm]['share_vhat_gt_0p5'] = float((cat['vhat'][s] > 0.5).mean()) if s.any() else None
brk = cat['ph'] == 1
for lo, hi, nm in ((0, 1, '0-1 s'), (1, 2, '1-2 s'), (2, np.inf, '>=2 s')):
    s = brk & (cat['t_onset'] >= lo) & (cat['t_onset'] < hi)
    tab['lead braking ' + nm] = {k: med(cat[k][s]) for k in ('vhat', 'v_true', 'ahat_long', 'dx_pred1', 'dx_pred3', 'age', 'v0')}
s = cat['ph'] == 0
tab['before onset'] = {k: med(cat[k][s]) for k in ('vhat', 'v_true', 'ahat_long', 'dx_pred1', 'dx_pred3', 'age', 'v0')}
doc['c_lead_state_medians_q25_q75_n'] = tab
# NIS and NEES by phase over distinct updates
cons = {}
_, first = np.unique(cat['key'], return_index=True)
for nm, s in (('before onset', cat['ph'] == 0), ('lead braking', cat['ph'] == 1),
              ('lead braking, first 1 s', (cat['ph'] == 1) & (cat['t_onset'] < 1.)), ('after stop', cat['ph'] == 2),
              ('after stop, first 2 s', (cat['ph'] == 2) & (cat['t_stop'] < 2.))):
    sel = np.zeros(cat['ph'].size, bool); sel[first] = True; sel &= s
    v = cat['nis'][sel]; v = v[np.isfinite(v)]
    cons[nm] = dict(n_updates=int(v.size), mean_nis=float(v.mean()) if v.size else None,
                    median_nis=float(np.median(v)) if v.size else None,
                    mean_nees_v_decisions=float(np.nanmean(cat['nees'][s])) if s.any() else None,
                    median_nees_v_decisions=float(np.nanmedian(cat['nees'][s])) if s.any() else None, n_decisions=int(s.sum()))
doc['c_consistency_by_phase'] = cons
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
doc['common_sha256'] = L.sha256_file(A.HERE / 'a9_common_v01.py')
A.write_out(OUTF, doc)
print('written %s (%.0f s)' % (OUTF, time.time() - t00))
