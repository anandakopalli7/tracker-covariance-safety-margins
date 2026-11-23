"""Revision v12, AMENDMENT_09 A9-6 (review items R19, S15): reliance on the stop, and caution counted under the stop scoring.
New file, 19 Nov 2026. Reaction-and-stop scoring of record: tau = 0.75 s, A = 6 m/s^2, plans judged until their stop ends
(revision_v11/analysis/out/ext, the safe set 'est' of rev_e2_extended_truth_score_v01.py: extended clearance > 0).

(1) Reliance: at each of the 201 levels of a population, each source's frontier operating point under this scoring (the point
    attaining the step frontier; point 0 of a source other than F0 and E is F0's zero-margin point); the share of the population's
    decisions whose selected row is unsafe under the 3 s commitment but safe with the stop, averaged over the levels; also the
    share whose selected row is unsafe under the 3 s commitment at all. The scoring's perfect oracle O: its one selection.
(2) S15 variant: caution's oracle row and truly safe set taken from this scoring instead of the 3 s commitment
    (optA_lib_v02.stats_scored with safe = the scoring's safe set); den0 and RR0 of every source; draw of record.
Usage: python -B -X utf8 a9_6_stop_reliance_v01.py
"""
import time
import numpy as np
import a9_common_v01 as A
C = A.C; L = A.L

OUTF = A.OUT / 'A9_6_STOP_RELIANCE_v01.json'
if OUTF.exists():
    raise SystemExit('REFUSED: %s exists' % OUTF)
t00 = time.time()
runs = C.load_runs()
KEY = L.vkey(0.75, 6.0)
EXT = A.V11 / 'out' / 'ext'
for r in runs:
    x = np.load(EXT / (r['run'] + '.npz'), allow_pickle=False)
    if not np.array_equal(x['k'], r['k']):
        raise SystemExit('REFUSED: decision ticks differ for %s' % r['run'])
    r['safe_x'] = {'est': L.clean_clear(x['clearX_' + KEY]) > 0.}
SC = ('X', 'est')
ARMS = ['N', 'NA', 'A1', 'CK3']
POPS = {'all': 0, 'moving': 1, 'phase0': 2, 'phase1': 3, 'phase2': 4}
doc = dict(code='a9_6_stop_reliance_v01.py', status='post hoc, descriptive; AMENDMENT_09 A9-6', scoring=KEY + ', judged until the stop ends')

# ------------------------------------------------------------------------------------------------ (1) reliance on the stop
X = C.tables(runs, SC, ['F0', 'E', 'O'] + ARMS)
rel = {}
for pn, pi in POPS.items():
    Tsum = {a: X[a].sum(axis=0)[:, pi, :] for a in X}
    cur = L.curves_w({a: Tsum[a] for a in Tsum if a != 'O'}, 0)
    cF0, wF0 = cur['F0']; cE, wE = cur['E']
    lev = L.levels_of(cF0, cE, cF0[0])
    n = float(Tsum['F0'][0, 0])
    ent = dict(n=n)
    for a in ['F0', 'E'] + ARMS + ['O']:
        only_stop = 0.; unsafe3 = 0.; unsafe_stop = 0.
        if a == 'O':
            for r in runs:
                m = r['masks'][pi]; sx = r['safe_x']['est']; s1 = r['clear1'] > 0.
                sel = L.select_first_safe(sx, r['idx55'])[0]; ar = np.arange(sel.size)
                only_stop += float((m & ~s1[ar, sel] & sx[ar, sel]).sum()); unsafe3 += float((m & ~s1[ar, sel]).sum())
                unsafe_stop += float((m & ~sx[ar, sel]).sum())
            ent[a] = dict(share_safe_only_with_stop=only_stop / n, share_unsafe_3s=unsafe3 / n, share_unsafe_with_stop=unsafe_stop / n)
            continue
        f, ix = A.frontier_argmin(cur[a][0], cur[a][1], lev)
        if a in ('F0', 'E'):
            cnt = np.bincount(ix[ix >= 0], minlength=len(C.GRID)).astype(float); cnt0 = 0.; base = a
        else:
            cnt0 = float((ix == 0).sum()); cnt = np.bincount(ix[ix >= 1] - 1, minlength=len(C.GRID)).astype(float); base = a
        for r in runs:
            m = r['masks'][pi]; sx = r['safe_x']['est']; s1 = r['clear1'] > 0.; ar = np.arange(r['n_dec'])
            sA = C.sel_of(r, base); sF = C.sel_of(r, 'F0')
            os_ = (~s1[ar[None, :], sA] & sx[ar[None, :], sA]) & m[None, :]
            u3 = (~s1[ar[None, :], sA]) & m[None, :]
            us = (~sx[ar[None, :], sA]) & m[None, :]
            only_stop += float(cnt @ os_.sum(axis=1)); unsafe3 += float(cnt @ u3.sum(axis=1)); unsafe_stop += float(cnt @ us.sum(axis=1))
            if cnt0:
                os0 = (~s1[ar, sF[0]] & sx[ar, sF[0]]) & m; u30 = (~s1[ar, sF[0]]) & m; us0 = (~sx[ar, sF[0]]) & m
                only_stop += cnt0 * float(os0.sum()); unsafe3 += cnt0 * float(u30.sum()); unsafe_stop += cnt0 * float(us0.sum())
        ent[a] = dict(share_safe_only_with_stop=only_stop / L.NLEV / n, share_unsafe_3s=unsafe3 / L.NLEV / n,
                      share_unsafe_with_stop=unsafe_stop / L.NLEV / n)
    rel[pn] = ent
    print('%s: %s (%.0f s)' % (pn, {a: round(100 * ent[a]['share_safe_only_with_stop'], 2) for a in ent if a != 'n'},
                                time.time() - t00), flush=True)
doc['reliance'] = rel


# ------------------------------------------------------------------------------------------------ (2) S15: caution under the stop
def stats_stop(sel, sx, vbar, des, masks):
    """optA_lib_v02.stats_scored with the caution's oracle row and truly safe set taken from sx (the scoring's safe set)."""
    G, n = sel.shape; ar = np.arange(n)
    anys = sx.any(axis=1); orc = sx.argmax(axis=1)
    ssel = sx[ar[None, :], sel]
    ct = np.where(ssel, (vbar[ar, orc][None, :] - vbar[ar[None, :], sel]) / des, 0.)
    out = np.empty((G, len(masks), L.NST))
    for mi, m in enumerate(masks):
        out[:, mi, 0] = m.sum(); out[:, mi, 1] = (~ssel & m).sum(axis=1); out[:, mi, 2] = (ct * m).sum(axis=1)
        out[:, mi, 3] = (ssel & m).sum(axis=1); out[:, mi, 4] = (anys[None, :] & ~ssel & m).sum(axis=1)
    return out


per = {a: [] for a in ['F0', 'E', 'O'] + ARMS}
for r in runs:
    sx = r['safe_x']['est']
    for a in per:
        sel = L.select_first_safe(sx, r['idx55']) if a == 'O' else C.sel_of(r, a)
        per[a].append(stats_stop(sel, sx, r['vbar'], r['desired'], r['masks']))
XS = {a: np.stack(v) for a, v in per.items()}
CNT = C.cnt_of_record()
pts = C.points(XS, ['E', 'O'] + ARMS, pops=[0, 1])
Rb = C.boot(XS, ['E', 'O'] + ARMS, (), [0, 1], CNT)
s15 = {}
for pn, pi in (('all', 0), ('moving', 1)):
    p = pts[pi]; b = Rb[pi]; n = p['n']
    ent = dict(n=n, R_pp=p['denE'] / L.NLEV, den0_pp=p['D']['O'] / L.NLEV, den0_deceq=L.dec_eq(p['D']['O'], n),
               den0_deceq_ci=L.pct(L.dec_eq(b['D']['O'], b['n'])))
    for a in ARMS:
        ent['RR0_' + a] = L.summ(C.rat(b['D'][a], b['D']['O']), L.ratio(p['D'][a], p['D']['O']))
    s15[pn] = ent
doc['s15_caution_under_stop'] = s15
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
A.write_out(OUTF, doc)
print('written %s (%.0f s)' % (OUTF, time.time() - t00))
