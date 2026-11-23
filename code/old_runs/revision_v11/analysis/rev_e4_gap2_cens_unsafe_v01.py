"""Revision v11, sensitivity to rev_e3_extended_gap2_v01.py: the reaction-and-stop scoring at tau = 0.75 s, 6 m/s^2, with a
2 m standstill gap and plans judged until their stop ends, where the pairs whose recording ends before the stop ("censored")
count as unsafe instead of being judged on the frames that exist. New file, 18 Nov 2026 (evening). Descriptive; points only.
Why: the third recount (recount3/r3_extra_v01.py) computed this sensitivity with one program; this is the first program's
value. It was written after the recount's numbers had been seen, so it is a second implementation that shares no code with
the recount, not a blind one (the comparison is printed at the end and stored in the output).
Convention as rev_e3: a pair is unsafe when its clearance is <= 2 m, for the wrong go (extended clearance) and for the
caution's truly safe rows (3 s clearance) alike. Only the wrong-go flag of the censored pairs changes here.
Usage: python -B -X utf8 rev_e4_gap2_cens_unsafe_v01.py
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rev_common_v01 as C                   # noqa: E402
L = C.L

OUT = HERE / 'out' / 'REV_E4_GAP2_CENS_UNSAFE_v01.json'
if OUT.exists():
    sys.exit('REFUSED: %s exists' % OUT)
t00 = time.time()
runs = C.load_runs()
GAP = 2.0; KEY = L.vkey(0.75, 6.0)
ARMS = C.MAIN_ARMS
tab = ['F0', 'E', 'O'] + ARMS; names = ['E', 'O'] + ARMS
per = {a: [] for a in tab}
pairs = dict(censored=0, censored_safe_at_2m_on_existing_frames=0, decisions_with_a_censored_pair=0, decisions_without_safe_row=0)
for r in runs:
    x = np.load(HERE / 'out' / 'ext' / (r['run'] + '.npz'), allow_pickle=False)
    assert np.array_equal(x['k'], r['k'])
    cens = x['cens_' + KEY].astype(bool)
    sx0 = L.clean_clear(x['clearX_' + KEY]) > GAP
    sx = sx0 & ~cens
    ev = r['ev'][:, None]
    pairs['censored'] += int((cens & ev).sum())
    pairs['censored_safe_at_2m_on_existing_frames'] += int((cens & sx0 & ev).sum())
    pairs['decisions_with_a_censored_pair'] += int((r['ev'] & cens.any(axis=1)).sum())
    pairs['decisions_without_safe_row'] += int((r['ev'] & ~sx.any(axis=1)).sum())
    for a in tab:
        sel = L.select_first_safe(sx, r['idx55']) if a == 'O' else C.sel_of(r, a)
        per[a].append(L.stats_scored(sel, r['clear1'] - GAP, sx, r['vbar'], r['desired'], r['masks']))
X = {a: np.stack(v) for a, v in per.items()}
pts = C.points(X, names, pops=range(5))
res = {}
for nm, pe in [(C.POPS[pi], pts[pi]) for pi in range(5)] + [('strat', C.strat_point(pts, names))]:
    n = pe['n']; den0 = pe['D']['O']; denE = pe['denE']
    e = dict(n=n, den0_pp=den0 / L.NLEV, den0_dec_eq=L.dec_eq(den0, n), RR0_E=L.ratio(denE, den0), arms={})
    for a in ARMS:
        e['arms'][a] = dict(D_dec_eq=L.dec_eq(pe['D'][a], n), rr0=L.ratio(pe['D'][a], den0))
    res[nm] = e
doc = dict(code='rev_e4_gap2_cens_unsafe_v01.py', status='post hoc, descriptive, points only; sensitivity to rev_e3',
           setting=dict(tau=0.75, A=6.0, gap=GAP, censored_pairs='unsafe'), pairs=pairs, pops=res)
# comparison with the third recount's supplementary script (opened only now)
R3 = json.loads((HERE.parent / 'recount3' / 'r3_extra_v01_out.json').read_text(encoding='utf-8'))['item3_diagnostics']
cmp_ = []
for mine, theirs in (('all', 'all'), ('moving', 'moving'), ('strat', 'phase_weighted')):
    t = R3['sensitivity_points']['censored_pairs_unsafe'][theirs]; e = res[mine]
    for lab, a, b in [('den0_pp', e['den0_pp'], t['den0_pp']), ('den0_dec_eq', e['den0_dec_eq'], t['den0_deceq']), ('RR0_E', e['RR0_E'], t['RR0_E']),
                      ('RR0_N', e['arms']['N']['rr0'], t['RR0_N']), ('RR0_NA', e['arms']['NA']['rr0'], t['RR0_NA']),
                      ('RR0_CK3', e['arms']['CK3']['rr0'], t['RR0_CK3']), ('RR0_AM', e['arms']['A1']['rr0'], t['RR0_AM'])]:
        cmp_.append(dict(pop=mine, name=lab, first=float(a), recount3=float(b), absdiff=abs(float(a) - float(b))))
for lab, a, b in [('censored pairs', pairs['censored'], R3['censored']), ('censored and safe at 2 m', pairs['censored_safe_at_2m_on_existing_frames'], R3['censored_and_counted_safe_at_2m']),
                  ('decisions with a censored pair', pairs['decisions_with_a_censored_pair'], R3['decisions_with_a_censored_pair'])]:
    cmp_.append(dict(pop='counts', name=lab, first=float(a), recount3=float(b), absdiff=abs(float(a) - float(b))))
doc['comparison_with_recount3'] = dict(n=len(cmp_), n_differ_1e9=sum(c['absdiff'] > 1e-9 for c in cmp_), max_absdiff=max(c['absdiff'] for c in cmp_), rows=cmp_)
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
OUT.write_text(C.jdump(doc), encoding='utf-8')
print(pairs)
for nm in ('all', 'moving', 'strat'):
    e = res[nm]
    print(nm, 'den0 %.4f pp %.2f dec-eq' % (e['den0_pp'], e['den0_dec_eq']), {a: round(e['arms'][a]['rr0'], 4) for a in ARMS})
print('comparison with recount3: %d numbers, %d differ by more than 1e-9, largest %.3g' % (
    doc['comparison_with_recount3']['n'], doc['comparison_with_recount3']['n_differ_1e9'], doc['comparison_with_recount3']['max_absdiff']))
