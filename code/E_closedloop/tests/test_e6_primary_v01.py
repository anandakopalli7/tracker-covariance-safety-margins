"""Synthetic tests of e6_analyse_v01.primary (A13 §E6.5): hand-computed full-sample values and a slow per-resample loop.
python -I -B tests/test_e6_primary_v01.py    -> writes tests/out/TEST_E6_PRIMARY_v01.json
"""
import json, pathlib, sys
import numpy as np

E = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(E / 'analysis'))
import e6_analyse_v01 as A6   # noqa: E402

L = A6.LABELS


def make(rows):
    """rows: list of (case, {label: (contact, tlost)})"""
    sel = {a: {} for a in L}
    for case, d in rows:
        for a, (c, t) in d.items():
            sel[a][case] = dict(outcomes=dict(contact=c, time_lost_s=None if c else t))
    return sel


def slow(sel):
    K = sorted(set.intersection(*[set(sel[a]) for a in L])); n = len(K)
    idx = np.random.default_rng(20261922).integers(0, n, (20000, n))
    out = []
    for b in range(20000):
        ks = [K[i] for i in idx[b]]
        c = [sum(sel[a][k]['outcomes']['contact'] for k in ks) / n for a in L]
        tk = [k for k in ks if all(sel[a][k]['outcomes']['contact'] == 0 for a in L)]
        if not tk: out.append(float('nan')); continue
        t = [sum(sel[a][k]['outcomes']['time_lost_s'] for k in tk) / len(tk) for a in L]
        tN, t4, t8, t16 = t
        if not (t4 < t8 < t16) or tN < t4 or tN > t16: out.append(float('nan')); continue
        lo, hi = (1, 2) if tN <= t8 else (2, 3)
        w = (tN - t[lo]) / (t[hi] - t[lo]); out.append(c[0] - (c[lo] + w * (c[hi] - c[lo])))
    D = np.array(out); bad = np.isnan(D)
    p = (1 + int(np.sum(bad | (np.nan_to_num(D, nan=0.) >= 0)))) / 20001
    fin = D[~bad]
    return dict(p=p, fs=fin.size / 20000, ub=float(np.quantile(fin, .95)) if fin.size else None,
                ci=[float(np.quantile(fin, .025)), float(np.quantile(fin, .975))] if fin.size else None)


def check(name, sel, want_status, want_delta=None):
    P = A6.primary(sel); S = slow(sel); r = dict(name=name, status=P['status'], delta=P['delta'], p=P['p_one'], fs=P['finite_share'])
    assert P['status'] == want_status, (name, P['status'])
    if want_delta is None: assert P['delta'] is None, name
    else: assert abs(P['delta'] - want_delta) < 1e-12, (name, P['delta'], want_delta)
    assert abs(P['p_one'] - S['p']) < 1e-12 and abs(P['finite_share'] - S['fs']) < 1e-12, (name, P['p_one'], S['p'])
    if S['ub'] is None: assert P['ub95'] is None
    else: assert abs(P['ub95'] - S['ub']) < 1e-12 and max(abs(x - y) for x, y in zip(P['ci'], S['ci'])) < 1e-12
    return r


res = []
# 1: bracketed 4-8. Cases a-d no contact anywhere: t N=1.5, F0 4/8/16 = 1, 2, 4 (equal per case) -> w = 0.5.
#    contacts on e-h: N 1 of 8, F0D4 4, F0D8 2, F0D16 1 -> c = .125, .5, .25, .125; cF = .5 + .5*(.25-.5) = .375; Delta = -.25
nc = {'N': (0, 1.5), 'F0D4': (0, 1.), 'F0D8': (0, 2.), 'F0D16': (0, 4.)}
def ct(n, f4, f8, f16): return {'N': (n, 9.), 'F0D4': (f4, 9.), 'F0D8': (f8, 9.), 'F0D16': (f16, 9.)}
rows = [(c, nc) for c in 'abcd'] + [('e', ct(1, 1, 1, 1)), ('f', ct(0, 1, 1, 0)), ('g', ct(0, 1, 0, 0)), ('h', ct(0, 1, 0, 0))]
res.append(check('bracketed 4-8', make(rows), 'bracketed 4-8', -0.25))
# 2: bracketed 8-16: N t = 3 -> w = (3-2)/(4-2) = .5; cF = .25 + .5*(.125-.25) = .1875; Delta = .125 - .1875 = -.0625
nc2 = dict(nc, N=(0, 3.)); rows2 = [(c, nc2) for c in 'abcd'] + rows[4:]
res.append(check('bracketed 8-16', make(rows2), 'bracketed 8-16', -0.0625))
# 3: N exactly at t_F0D8 -> pair 4-8 with w = 1 -> cF = c8 = .25; Delta = -.125
nc3 = dict(nc, N=(0, 2.)); rows3 = [(c, nc3) for c in 'abcd'] + rows[4:]
res.append(check('N at t8', make(rows3), 'bracketed 4-8', -0.125))
# 4, 5: not bracketed (below, above)
res.append(check('below', make([(c, dict(nc, N=(0, .5))) for c in 'abcd'] + rows[4:]), 'not bracketed'))
res.append(check('above', make([(c, dict(nc, N=(0, 5.))) for c in 'abcd'] + rows[4:]), 'not bracketed'))
# 6: non-monotone (t8 < t4)
res.append(check('non-monotone', make([(c, dict(nc, F0D8=(0, .8))) for c in 'abcd'] + rows[4:]), 'non-monotone'))
# 7: empty T (every case has a contact in some arm)
res.append(check('empty T', make(rows[4:]), 'no common no-contact case'))
# 8: mixed per-case time lost (multiplicity matters in resamples) and a case missing an arm (excluded from K)
rows8 = [('a', {'N': (0, 1.2), 'F0D4': (0, 1.), 'F0D8': (0, 1.6), 'F0D16': (0, 3.)}), ('b', {'N': (0, 2.6), 'F0D4': (0, 1.4), 'F0D8': (0, 2.9), 'F0D16': (0, 4.1)}),
         ('c', {'N': (0, 0.9), 'F0D4': (0, 0.7), 'F0D8': (0, 1.1), 'F0D16': (0, 1.9)})] + rows[4:] + [('z', {'N': (0, 1.), 'F0D4': (0, 1.)})]
P8 = A6.primary(make(rows8)); assert P8['n'] == 7 and 'z' not in P8['K']
t = [(1.2 + 2.6 + 0.9) / 3, (1 + 1.4 + .7) / 3, (1.6 + 2.9 + 1.1) / 3, (3 + 4.1 + 1.9) / 3]; c = [1 / 7, 4 / 7, 2 / 7, 1 / 7]
w = (t[0] - t[1]) / (t[2] - t[1]); want8 = c[0] - (c[1] + w * (c[2] - c[1]))
res.append(check('mixed', make(rows8), 'bracketed 4-8', want8))
out = E / 'tests' / 'out' / 'TEST_E6_PRIMARY_v01.json'
out.write_text(json.dumps(dict(passed=True, cases=res), indent=1), encoding='utf-8')
print('ALL PASS', len(res))
