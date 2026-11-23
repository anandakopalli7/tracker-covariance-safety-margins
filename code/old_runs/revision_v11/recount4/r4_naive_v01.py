"""Recount4 self-check by a second, plain route. Shares only the data loader (r4_items_v01.load -> rc_lib_v01.load_all) and the grid.

Part 1 (scoring): decisions concatenated (no per-run statistics); selection recomputed from the critical scales by a loop over
rows; unsafe flags written out again (x <= 0 or NaN); levels by numpy.linspace; step frontier by a loop over levels. Compared
with the points of RECOUNT4_RESULTS_v01.json for every scoring and population, and with three resamples of boot\\<scoring>.npz.
Part 2 (summaries): every interval, share and ratio of the results file recomputed from boot\\<scoring>.npz with a hand-written
percentile and name-based column lookup.
Part 3 (pair counts): recounted on the concatenated arrays with other expressions.
Usage: python -B -X utf8 r4_naive_v01.py   -> r4_naive_v01_out.json
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import r4_items_v01 as I   # noqa: E402  (loader, list of scorings; none of its scoring functions is used here)
L = I.L
GRID = L.GRID
COLS = ['F0', 'E', 'N', 'NA', 'AM', 'CK3', 'Q', 'O']
RES = json.loads((HERE / 'RECOUNT4_RESULTS_v01.json').read_text(encoding='utf-8'))
CHECK_ROWS = (0, 7, 19999)
t00 = time.time()

ds = I.load()
off = np.concatenate([[0], np.cumsum([d['n'] for d in ds])])
N = int(off[-1])
cat = lambda key: np.concatenate([d[key] for d in ds])
clear = cat('clear'); vbar = cat('vbar'); des = cat('des'); idx55 = cat('idx55'); v0 = cat('v0'); phase = cat('phase')
crit = {a: np.concatenate([d['crit'][a] for d in ds]) for a in L.ARMS}
X = {k: np.concatenate([d['X'][k] for d in ds]) for k in I.SETTINGS}
W = {k: np.concatenate([d['W'][k] for d in ds]) for k in I.SETTINGS}
LATE = {k: np.concatenate([d['late'][k] for d in ds]) for k in I.SETTINGS}
CENS = {k: np.concatenate([d['cens'][k] for d in ds]) for k in I.SETTINGS}
ROWS = np.arange(17)

# selection per arm and scale: go through the rows from the last to the first, so the first feasible row wins
SEL = {}
for a in L.ARMS:
    s = np.empty((GRID.size, N), np.int64)
    for gi, g in enumerate(GRID):
        cur = idx55.copy()
        for r in range(16, -1, -1):
            cur = np.where(crit[a][:, r] >= g, r, cur)
        s[gi] = cur
    SEL[a] = s
safe_c = clear > 0.
has_safe = safe_c.any(1)
first_safe = np.array([int(np.flatnonzero(safe_c[i])[0]) if has_safe[i] else 0 for i in range(N)])


def unsafe_of(variant, key):
    if variant == 'w1':
        return ~(clear > 0.)
    if variant == 'est':
        return (X[key] <= 0.) | np.isnan(X[key])
    if variant == 'cens':
        return (X[key] <= 0.) | np.isnan(X[key]) | CENS[key]
    if variant == 'asscored':
        return (W[key] <= 0.) | np.isnan(W[key])
    raise ValueError(variant)


def point(sel_row, unsafe_w, ii, signed):
    """(caution %, wrong go %) of one selection (one row per decision of the full set) on the decisions ii."""
    s = sel_row[ii]
    w = 100. * unsafe_w[ii, s].sum() / ii.size
    diff = (vbar[ii, first_safe[ii]] - vbar[ii, s]) / des[ii]
    m = has_safe[ii] if signed else safe_c[ii, s]
    c = 100. * diff[m].sum() / m.sum() if m.any() else np.nan
    return c, w


def frontier(c, w, lev):
    out = np.full(lev.size, np.nan)
    for i, x in enumerate(lev):
        m = c <= x
        if m.any():
            out[i] = w[m].min()
    return out


def oracle_rows(unsafe_w):
    """Per decision the first row (cost order) the scoring judges safe, the fallback row if none."""
    sw = ~unsafe_w
    return np.array([int(np.flatnonzero(sw[i])[0]) if sw[i].any() else int(idx55[i]) for i in range(N)])


def pop_eval(unsafe_w, ii, signed, selO):
    if ii.size == 0:
        return None
    pts = {}
    for a in L.ARMS:
        cw = np.array([point(SEL[a][gi], unsafe_w, ii, signed) for gi in range(GRID.size)])
        pts[a] = (cw[:, 0], cw[:, 1])
    cF, wF = pts['F0']; cE, wE = pts['E']
    lev = np.linspace(cF[0], min(np.nanmax(cF), np.nanmax(cE)), 201)
    fF = frontier(cF, wF, lev)
    D = {'F0': 0.0, 'E': float(np.sum(fF - frontier(cE, wE, lev)))}
    for a in ('N', 'NA', 'AM', 'CK3', 'Q'):
        c, w = pts[a]
        D[a] = float(np.sum(fF - frontier(np.concatenate([[cF[0]], c]), np.concatenate([[wF[0]], w]), lev)))
    cO, wO = point(selO, unsafe_w, ii, signed)
    D['O'] = float(np.sum(fF - frontier(np.array([cF[0], cO]), np.array([wF[0], wO]), lev)))
    return dict(n=int(ii.size), D=D)


def all_pops(unsafe_w, ii, signed, selO):
    out = {'all': pop_eval(unsafe_w, ii, signed, selO), 'moving': pop_eval(unsafe_w, ii[v0[ii] > 0.5], signed, selO)}
    for p in (0, 1, 2):
        out['phase%d' % p] = pop_eval(unsafe_w, ii[phase[ii] == p], signed, selO)
    ph = [out['phase%d' % p] for p in (0, 1, 2)]
    nt = sum(e['n'] for e in ph if e is not None)
    out['phase_weighted'] = dict(n=nt, D={c: sum(e['n'] / nt * e['D'][c] for e in ph if e is not None) for c in COLS})
    return out


cmp1 = dict(points=dict(n=0, max_abs=0.0, nan_mismatch=0), resamples=dict(n=0, max_abs=0.0, nan_mismatch=0), worst=[])


def note(kind, tag, a, b):
    c = cmp1[kind]; c['n'] += 1
    an = a is None or not np.isfinite(a); bn = b is None or not np.isfinite(b)
    if an or bn:
        if an != bn:
            c['nan_mismatch'] += 1; cmp1['worst'].append([tag, a, b])
        return
    dlt = abs(a - b)
    if dlt > c['max_abs']:
        c['max_abs'] = float(dlt)
    if dlt > 1e-9:
        cmp1['worst'].append([tag, float(a), float(b)])


draw = L.draw_of_record()
full = np.arange(N)
naive_points = {}
for name, variant, key, signed in I.SCORINGS:
    uw = unsafe_of(variant, key)
    selO = oracle_rows(uw)
    ev = all_pops(uw, full, signed, selO)
    naive_points[name] = {pn: dict(n=e['n'], D=e['D']) for pn, e in ev.items()}
    rs = RES['scorings'][name]['pops']
    for pn, e in ev.items():
        note('points', '%s.%s.n' % (name, pn), float(e['n']), rs[pn]['n'])
        note('points', '%s.%s.denE' % (name, pn), e['D']['E'], rs[pn]['denE']['sum']['point'])
        note('points', '%s.%s.den0' % (name, pn), e['D']['O'], rs[pn]['den0']['sum']['point'])
        for a in I.SRC:
            note('points', '%s.%s.D_%s' % (name, pn, a), e['D'][a], rs[pn]['src'][a]['D_sum']['point'])
    z = np.load(I.BOOT_DIR / (name + '.npz'))
    for b in CHECK_ROWS:
        ii = np.concatenate([np.arange(off[r], off[r + 1]) for r in draw[b]])
        ev = all_pops(uw, ii, signed, selO)
        for pi, pn in enumerate(I.POPS):
            note('resamples', '%s.%s.row%d.n' % (name, pn, b), float(ev[pn]['n']), float(z['nb'][b, pi]))
            for ci, c in enumerate(COLS):
                note('resamples', '%s.%s.row%d.D_%s' % (name, pn, b, c), ev[pn]['D'][c], float(z['Db'][b, pi, ci]))
        note('resamples', '%s.phase_weighted.row%d.n' % (name, b), float(ev['phase_weighted']['n']), float(z['ntb'][b]))
        for ci, c in enumerate(COLS):
            note('resamples', '%s.phase_weighted.row%d.D_%s' % (name, b, c), ev['phase_weighted']['D'][c], float(z['Dwb'][b, ci]))
    print('%-26s part 1 done, %.0f s' % (name, time.time() - t00), flush=True)


# ------------------------------------------------------------------------------------------------ part 2: summaries
def pctl(v):
    v = np.asarray(v, float); v = np.sort(v[np.isfinite(v)])
    m = v.size
    if m == 0:
        return None
    out = []
    for q in (0.025, 0.975):
        pos = (m - 1) * q; lo = int(np.floor(pos)); hi = min(lo + 1, m - 1)
        out.append(float(v[lo] + (v[hi] - v[lo]) * (pos - lo)))
    return out


def ratio_ci(num, den):
    keep = np.isfinite(num) & np.isfinite(den) & (den > 0)
    return pctl(num[keep] / den[keep]), int((~keep).sum())


cmp2 = dict(n=0, max_abs=0.0, mismatch=[])


def same(tag, a, b):
    cmp2['n'] += 1
    if a is None or b is None:
        if not (a is None and b is None):
            cmp2['mismatch'].append([tag, a, b])
        return
    dlt = abs(float(a) - float(b))
    cmp2['max_abs'] = max(cmp2['max_abs'], dlt)
    if dlt > 1e-9:
        cmp2['mismatch'].append([tag, a, b])


def fin(x):
    return float(x) if np.isfinite(x) else None


def pop_arrays(z, pn):
    """n point, D point (dict), n per resample, D per resample (dict), for one population; the weighted one rebuilt here."""
    if pn != 'phase_weighted':
        pi = I.POPS.index(pn)
        return float(z['nn'][0, pi]), {c: float(z['D0'][0, pi, ci]) for ci, c in enumerate(COLS)}, z['nb'][:, pi], {c: z['Db'][:, pi, ci] for ci, c in enumerate(COLS)}
    ph = [I.POPS.index('phase%d' % p) for p in (0, 1, 2)]
    n0 = sum(float(z['nn'][0, pi]) for pi in ph)
    D0 = {c: sum(float(z['nn'][0, pi]) / n0 * float(z['D0'][0, pi, ci]) for pi in ph) for ci, c in enumerate(COLS)}
    nb = sum(z['nb'][:, pi] for pi in ph)
    Db = {c: sum(z['nb'][:, pi] / nb * z['Db'][:, pi, ci] for pi in ph) for ci, c in enumerate(COLS)}
    return n0, D0, nb, Db


Z = {name: np.load(I.BOOT_DIR / (name + '.npz')) for name, _, _, _ in I.SCORINGS}
for name, variant, key, signed in I.SCORINGS:
    sc = RES['scorings'][name]
    for pn in list(I.POPS) + ['phase_weighted']:
        e = sc['pops'][pn]; tag = name + '.' + pn
        n0, D0, nb, Db = pop_arrays(Z[name], pn)
        same(tag + '.n', n0, e['n'])
        for q, c in (('den0', 'O'), ('denE', 'E')):
            for form, f0, fb in (('sum', D0[c], Db[c]), ('pp', D0[c] / 201., Db[c] / 201.), ('deceq', D0[c] / 201. / 100. * n0, Db[c] / 201. / 100. * nb)):
                same('%s.%s.%s.point' % (tag, q, form), fin(f0), e[q][form]['point'])
                ci = pctl(fb)
                for j in (0, 1):
                    same('%s.%s.%s.ci%d' % (tag, q, form, j), None if ci is None else ci[j], None if e[q][form]['ci'] is None else e[q][form]['ci'][j])
            same('%s.share_%s_le0' % (tag, q), float(np.sum(Db[c] <= 0)) / Db[c].size, e['share_%s_le0' % q])
        for rn, r in sc['reference_scorings'].items():
            _, R0, _, Rb = pop_arrays(Z[r], pn)
            for q, c in (('denE', 'E'), ('den0', 'O')):
                with np.errstate(invalid='ignore', divide='ignore'):
                    pt = np.float64(D0[c]) / np.float64(R0[c])
                same('%s.rel.%s.%s.point' % (tag, rn, q), fin(pt), e['rel'][rn][q]['point'])
                ci, nlo = ratio_ci(Db[c], Rb[c])
                for j in (0, 1):
                    same('%s.rel.%s.%s.ci%d' % (tag, rn, q, j), None if ci is None else ci[j], None if e['rel'][rn][q]['ci'] is None else e['rel'][rn][q]['ci'][j])
                same('%s.rel.%s.%s.n_left_out' % (tag, rn, q), nlo, e['rel'][rn][q]['n_left_out'])
        for a in I.SRC:
            s = e['src'][a]
            for form, f0, fb in (('D_sum', D0[a], Db[a]), ('D_pp', D0[a] / 201., Db[a] / 201.), ('D_deceq', D0[a] / 201. / 100. * n0, Db[a] / 201. / 100. * nb)):
                same('%s.%s.%s.point' % (tag, a, form), fin(f0), s[form]['point'])
                ci = pctl(fb)
                for j in (0, 1):
                    same('%s.%s.%s.ci%d' % (tag, a, form, j), None if ci is None else ci[j], None if s[form]['ci'] is None else s[form]['ci'][j])
            for q, c in (('RR0', 'O'), ('RR', 'E')):
                with np.errstate(invalid='ignore', divide='ignore'):
                    pt = np.float64(D0[a]) / np.float64(D0[c])
                same('%s.%s.%s.point' % (tag, a, q), fin(pt), s[q]['point'])
                ci, nlo = ratio_ci(Db[a], Db[c])
                for j in (0, 1):
                    same('%s.%s.%s.ci%d' % (tag, a, q, j), None if ci is None else ci[j], None if s[q]['ci'] is None else s[q]['ci'][j])
                same('%s.%s.%s.n_left_out' % (tag, a, q), nlo, s[q]['n_left_out'])
        with np.errstate(invalid='ignore', divide='ignore'):
            pt = np.float64(D0['E']) / np.float64(D0['O'])
        same(tag + '.RR0_E.point', fin(pt), e['RR0_E']['point'])
        ci, nlo = ratio_ci(Db['E'], Db['O'])
        for j in (0, 1):
            same('%s.RR0_E.ci%d' % (tag, j), None if ci is None else ci[j], None if e['RR0_E']['ci'] is None else e['RR0_E']['ci'][j])
        same(tag + '.RR0_E.n_left_out', nlo, e['RR0_E']['n_left_out'])
print('part 2 done, %.0f s' % (time.time() - t00), flush=True)

# ------------------------------------------------------------------------------------------------ part 3: pair counts
cmp3 = dict(n=0, differ=[])
for key in I.SETTINGS:
    x = X[key]; w = W[key]; la = LATE[key]; ce = CENS[key]
    ux = (x <= 0.) | np.isnan(x); uw = (w <= 0.) | np.isnan(w)
    mine = dict(evaluated_decisions=N, pairs=N * 17, pairs_unsafe_window=int(np.count_nonzero(uw)), pairs_unsafe_est=int(np.count_nonzero(ux)),
                pairs_late=int(np.count_nonzero(la)), pairs_late_safe_window=int(np.count_nonzero(la[~uw])),
                pairs_late_safe_window_unsafe_est=int(np.count_nonzero(ux[la & ~uw])), pairs_cens=int(np.count_nonzero(ce)),
                pairs_cens_safe_window=int(np.count_nonzero(ce[~uw])), pairs_cens_safe_window_safe_est=int(np.count_nonzero(~ux[ce & ~uw])),
                decisions_without_safe_row_est=int(np.count_nonzero(ux.sum(1) == 17)),
                decisions_without_safe_row_window=int(np.count_nonzero(uw.sum(1) == 17)),
                decisions_without_safe_row_cens_unsafe=int(np.count_nonzero((ux | ce).sum(1) == 17)),
                decisions_with_a_cens_pair=int(np.count_nonzero(ce.sum(1) > 0)))
    for k, v in mine.items():
        cmp3['n'] += 1
        if v != RES['counts'][key][k]:
            cmp3['differ'].append([key, k, v, RES['counts'][key][k]])

out = dict(what='self-check of recount4 by a second route', check_rows=list(CHECK_ROWS), part1=cmp1, part2=cmp2, part3=cmp3,
           naive_points=naive_points, seconds=time.time() - t00)
L.jdump(out, HERE / 'r4_naive_v01_out.json')
print('part 1 points: %d compared, max abs %.3g, nan mismatches %d' % (cmp1['points']['n'], cmp1['points']['max_abs'], cmp1['points']['nan_mismatch']))
print('part 1 resamples: %d compared, max abs %.3g, nan mismatches %d' % (cmp1['resamples']['n'], cmp1['resamples']['max_abs'], cmp1['resamples']['nan_mismatch']))
print('part 1 entries above 1e-9 or NaN mismatch:', len(cmp1['worst']))
print('part 2: %d compared, max abs %.3g, mismatches %d' % (cmp2['n'], cmp2['max_abs'], len(cmp2['mismatch'])))
print('part 3: %d counts compared, differ %d' % (cmp3['n'], len(cmp3['differ'])))
