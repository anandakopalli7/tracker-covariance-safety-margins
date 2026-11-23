"""Revision v11, post hoc re-analyses R11 and R17 (ARS review of draft v10). New file, 18 Nov 2026.
Descriptive analyses added after the results and after a review; declared in AMENDMENT_08 (revision_v11).

R11  Caution counted at its signed value under the 3 s commitment (W1), for every margin source and population.
     Same definition as the tau = 0.75 s sensitivity of record (optA_lib_v02.stats_scored, signed=True): caution is averaged
     over every evaluated decision that has a W1-safe row, each at its signed speed difference to the first W1-safe row.
     Arms F0, E, O, N, NA, CK3, AM ('A1'), Q, CK3r, and the graded oracles P25 / P50 / P75 (draws of record, seed 20261118).
R17  The 2 m standstill gap of UN R157 01 series, performance model 2.
     A decision-row pair is unsafe when its true clearance is <= 2 m: for the wrong go (the scoring's clearance) and for the
     caution's truly safe rows (the 3 s clearance), "applied to W1 and to W_R alike" as in oxsb_replan_v03.stats_R.
     Scorings: W1 at gap 2; W_R(tau, A) at gap 2 for tau in {0.75, 1.8} x A = 6, and tau = 0.75 x A in {4, 5, 7.6}; reading (ii)
     at tau = 0.75 s, 6 m/s^2, gap 2. New quantity: the perfect oracle O for the 2 m requirement (first row whose scoring
     clearance exceeds 2 m), den0 and RR0 of every source, by population and phase-weighted.
     Identity: den, D(N, F0) and RR(N) at gap 2 equal A5_RESULTS_FIT_v01.json where that file has the setting.
Bootstrap: the draw of record (20,000 run resamples, seed 20261113), percentile intervals; basic intervals printed beside.
Usage: python -B -X utf8 rev_a_signed_gap_v01.py
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rev_common_v01 as C                   # noqa: E402
L = C.L

OUT = HERE / 'out' / 'REV_A_SIGNED_GAP_v01.json'
if OUT.exists():
    sys.exit('REFUSED: %s exists' % OUT)
t00 = time.time()
runs = C.load_runs()
CNT = C.cnt_of_record()
ARMS = C.MAIN_ARMS
GRADED = ['P25', 'P50', 'P75']


def add_graded(runs):
    """Copy of optA_main_v02.add_graded (partial oracles only): default_rng(20261118).random(9307) in (run name, k) order."""
    ntot = sum(r['n_dec'] for r in runs)
    assert ntot == 9307
    U = np.random.default_rng(20261118).random(ntot)
    pos = 0
    for r in runs:
        u = U[pos:pos + r['n_dec']]; pos += r['n_dec']
        for p, nm in zip([0.25, 0.5, 0.75], GRADED):
            r['crit'][nm] = np.where((u < p)[:, None], r['crit']['E'], r['crit']['F0'])


def tables_gap(runs, sc, arms, gap, signed=False):
    """C.tables with the gap also applied to the caution's truly safe set: the 3 s clearance minus the gap is passed as clear1."""
    per = {a: [] for a in arms if a != 'CK3r'}
    for r in runs:
        if sc[0] == 'W1':
            sx = r['clear1'] > gap
        else:
            sx = C.safe_set(r, tuple(sc[:3]) + (gap,))
        for a in per:
            sel = L.select_first_safe(sx, r['idx55']) if a == 'O' else C.sel_of(r, a)
            per[a].append(L.stats_scored(sel, r['clear1'] - gap, sx, r['vbar'], r['desired'], r['masks'], signed=signed))
    X = {a: np.stack(v) for a, v in per.items()}
    if 'CK3r' in arms:
        X['CK3r'] = X['CK3']
    return X


def summarise(X, names, do_boot=True):
    pts = C.points(X, names, pops=range(5), repl=('CK3r',))
    R = C.boot(X, names, (), [0, 1, 2, 3, 4], CNT, repl=('CK3r',)) if do_boot else None
    res = {}
    pops = [(C.POPS[pi], pts[pi], R[pi] if R else None) for pi in range(5)]
    pops.append(('strat', C.strat_point(pts, names), C.strat_boot(R, names) if R else None))
    for nm, pe, Rp in pops:
        n = pe['n']; den0 = pe['D']['O']; denE = pe['denE']
        e = dict(n=n, den0=dict(point=den0, R_pp=den0 / L.NLEV, dec_eq=L.dec_eq(den0, n)),
                 denE=dict(point=denE, R_pp=denE / L.NLEV, dec_eq=L.dec_eq(denE, n)), arms={})
        if Rp is not None:
            e['den0'].update(L.summ_den(Rp['D']['O'], den0)); e['denE'].update(L.summ_den(Rp['denE'], denE))
            e['den0']['dec_eq_ci'] = L.pct(L.dec_eq(Rp['D']['O'], Rp['n']))
            e['denE']['dec_eq_ci'] = L.pct(L.dec_eq(Rp['denE'], Rp['n']))
            e['E_rr0'] = L.summ(C.rat(Rp['denE'], Rp['D']['O']), L.ratio(denE, den0))
        else:
            e['E_rr0'] = dict(point=L.ratio(denE, den0))
        for a in names:
            if a in ('E', 'O'):
                continue
            D = pe['D'][a]
            ent = dict(D=D, D_pp=D / L.NLEV, D_dec_eq=L.dec_eq(D, n))
            if Rp is not None:
                ent['D_dec_eq_ci'] = L.pct(L.dec_eq(Rp['D'][a], Rp['n']))
                ent['rr0'] = L.summ(C.rat(Rp['D'][a], Rp['D']['O']), L.ratio(D, den0))
                ent['rrE'] = L.summ(C.rat(Rp['D'][a], Rp['denE']), L.ratio(D, denE))
            else:
                ent['rr0'] = dict(point=L.ratio(D, den0)); ent['rrE'] = dict(point=L.ratio(D, denE))
            e['arms'][a] = ent
        res[nm] = e
    return res


doc = dict(written=None, code='rev_a_signed_gap_v01.py', status='post hoc, descriptive; AMENDMENT_08', R11={}, R17={})

# ------------------------------------------------------------------------------------------------ R11
add_graded(runs)
tab = ['F0', 'E', 'O'] + ARMS + ['CK3r'] + GRADED
names = ['E', 'O'] + ARMS + ['CK3r'] + GRADED
for signed in (False, True):
    key = 'W1_signed' if signed else 'W1_unsigned_of_record'
    X = C.tables(runs, ('W1',), tab, signed=signed)
    doc['R11'][key] = summarise(X, names)
    print('R11 %s done (%.0f s)' % (key, time.time() - t00), flush=True)
doc['R11']['n_evaluated_without_W1_safe_row'] = int(sum(int((r['ev'] & ~(r['clear1'] > 0.).any(axis=1)).sum()) for r in runs))
# zero-margin points (caution %, wrong go %) of F0 and CK3 under both caution conventions
zp = {}
for signed in (False, True):
    X = C.tables(runs, ('W1',), ['F0', 'CK3', 'E'], signed=signed)
    for a in ('F0', 'CK3'):
        T = X[a].sum(axis=0)[0, 0, :]
        zp['%s_%s' % (a, 'signed' if signed else 'unsigned')] = dict(caution_pct=float(100. * T[2] / T[3]),
                                                                    wrong_go_pct=float(100. * T[1] / T[0]))
doc['R11']['zero_margin_points_all'] = zp

# ------------------------------------------------------------------------------------------------ R17
GAP = 2.0
a5 = json.loads((C.OJ / 'A5' / 'fit' / 'main' / 'A5_RESULTS_FIT_v01.json').read_text(encoding='utf-8'))
tab2 = ['F0', 'E', 'O'] + ARMS + ['CK3r']
names2 = ['E', 'O'] + ARMS + ['CK3r']
plan = [(('W1',), True), (('WR', 0.75, 6.0), True), (('ii', 0.75, 6.0), True), (('WR', 1.8, 6.0), True),
        (('WR', 0.75, 4.0), False), (('WR', 0.75, 5.0), False), (('WR', 0.75, 7.6), False)]
for sc, do_boot in plan:
    key = sc[0] if sc[0] == 'W1' else '%s_%s' % (sc[0], L.vkey(sc[1], sc[2]))
    X = tables_gap(runs, sc, tab2, GAP)
    doc['R17'][key + '_gap2'] = summarise(X, names2, do_boot=do_boot)
    # count of evaluated decisions without any row meeting the 2 m requirement under this scoring
    nno = 0
    for r in runs:
        sx = (r['clear1'] > GAP) if sc[0] == 'W1' else C.safe_set(r, tuple(sc[:3]) + (GAP,))
        nno += int((r['ev'] & ~sx.any(axis=1)).sum())
    doc['R17'][key + '_gap2']['n_evaluated_without_safe_row'] = nno
    print('R17 %s done (%.0f s)' % (key, time.time() - t00), flush=True)
# pair counts at the 2 m gap, tau 0.75 s, 6 m/s^2
key = L.vkey(0.75, 6.0)
npair = n1 = nR0 = nR2 = 0
for r in runs:
    ev = r['ev'][:, None]
    npair += int(ev.sum()) * 17
    n1 += int(((r['clear1'] <= 0.) & ev).sum())
    nR0 += int(((L.clean_clear(r['cache'][key]) <= 0.) & ev).sum())
    nR2 += int(((L.clean_clear(r['cache'][key]) <= GAP) & ev).sum())
doc['R17']['pair_counts'] = dict(pairs=npair, unsafe_W1_gap0=n1, unsafe_WR075_gap0=nR0, unsafe_WR075_gap2=nR2)

# identity against A5 at gap 2 (F0, E, N only there): den, D(N, F0), RR(N)
ident = []
try:
    sets = a5.get('settings') or a5.get('results') or {}
    doc['R17']['a5_keys_seen'] = list(a5.keys())[:20]
except Exception as ex:                       # noqa: BLE001
    doc['R17']['a5_identity_error'] = repr(ex)
doc['R17']['identity_note'] = 'see rev_a_identity_a5_v01.py for the comparison with A5_RESULTS_FIT_v01.json at gap 2'
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
doc['common_sha256'] = L.sha256_file(HERE / 'rev_common_v01.py')
OUT.write_text(C.jdump(doc), encoding='utf-8')
print('written %s (%.0f s)' % (OUT, time.time() - t00))
