"""Revision v11, post hoc re-analyses R10 and R17 combined: the reaction-and-stop scoring at tau = 0.75 s, 6 m/s^2, with a 2 m
standstill gap AND plans judged until their stop ends. New file, 18 Nov 2026. Descriptive; AMENDMENT_08.
Gap convention as in rev_a_signed_gap_v01.py / oxsb_replan_v03.stats_R: a pair is unsafe when its clearance is <= 2 m, for the
wrong go (the extended clearance of rev_e1) and for the caution's truly safe rows (the 3 s clearance) alike.
(rev_e2's 'est_gap2' scoring applied the gap to the wrong go only and is not reported.)
Usage: python -B -X utf8 rev_e3_extended_gap2_v01.py
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rev_common_v01 as C                   # noqa: E402
L = C.L

OUT = HERE / 'out' / 'REV_E3_EXTENDED_GAP2_v01.json'
if OUT.exists():
    sys.exit('REFUSED: %s exists' % OUT)
t00 = time.time()
runs = C.load_runs()
CNT = C.cnt_of_record()
GAP = 2.0; KEY = L.vkey(0.75, 6.0)
ARMS = C.MAIN_ARMS
tab = ['F0', 'E', 'O'] + ARMS; names = ['E', 'O'] + ARMS
per = {a: [] for a in tab}
pairs = dict(unsafe_as_scored_gap2=0, unsafe_est_gap2=0, decisions_without_safe_row=0)
for r in runs:
    x = np.load(HERE / 'out' / 'ext' / (r['run'] + '.npz'), allow_pickle=False)
    assert np.array_equal(x['k'], r['k'])
    sx = L.clean_clear(x['clearX_' + KEY]) > GAP
    ev = r['ev'][:, None]
    pairs['unsafe_as_scored_gap2'] += int((~(L.clean_clear(r['cache'][KEY]) > GAP) & ev).sum())
    pairs['unsafe_est_gap2'] += int((~sx & ev).sum())
    pairs['decisions_without_safe_row'] += int((r['ev'] & ~sx.any(axis=1)).sum())
    for a in tab:
        sel = L.select_first_safe(sx, r['idx55']) if a == 'O' else C.sel_of(r, a)
        per[a].append(L.stats_scored(sel, r['clear1'] - GAP, sx, r['vbar'], r['desired'], r['masks']))
X = {a: np.stack(v) for a, v in per.items()}
pts = C.points(X, names, pops=range(5))
R = C.boot(X, names, (), [0, 1, 2, 3, 4], CNT)
res = {}
for nm, pe, Rp in [(C.POPS[pi], pts[pi], R[pi]) for pi in range(5)] + [('strat', C.strat_point(pts, names), C.strat_boot(R, names))]:
    n = pe['n']; den0 = pe['D']['O']; denE = pe['denE']
    e = dict(n=n, den0=dict(L.summ_den(Rp['D']['O'], den0), R_pp=den0 / L.NLEV, dec_eq=L.dec_eq(den0, n),
                            dec_eq_ci=L.pct(L.dec_eq(Rp['D']['O'], Rp['n']))),
             denE=dict(point=denE, R_pp=denE / L.NLEV, dec_eq=L.dec_eq(denE, n)),
             E_rr0=L.summ(C.rat(Rp['denE'], Rp['D']['O']), L.ratio(denE, den0)), arms={})
    for a in ARMS:
        D = pe['D'][a]
        e['arms'][a] = dict(D_dec_eq=L.dec_eq(D, n), rr0=L.summ(C.rat(Rp['D'][a], Rp['D']['O']), L.ratio(D, den0)))
    res[nm] = e
doc = dict(code='rev_e3_extended_gap2_v01.py', status='post hoc, descriptive; AMENDMENT_08', setting=dict(tau=0.75, A=6.0, gap=GAP),
           pairs=pairs, pops=res, written=time.strftime('%Y-%m-%d %H:%M:%S'), seconds=time.time() - t00)
OUT.write_text(C.jdump(doc), encoding='utf-8')
for nm in ('all', 'moving', 'strat'):
    e = res[nm]
    print(nm, 'den0 %.4f pp %.1f dec-eq' % (e['den0']['R_pp'], e['den0']['dec_eq']), {a: (round(e['arms'][a]['rr0']['point'], 4), [round(v, 4) for v in e['arms'][a]['rr0']['ci']]) for a in ARMS})
print(pairs, 'written (%.0f s)' % (time.time() - t00))
