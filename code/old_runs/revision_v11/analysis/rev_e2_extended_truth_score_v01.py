"""Revision v11, post hoc re-analysis R10, step 2 (ARS review of draft v10): the reaction-and-stop scoring with every plan
judged against the logged truth until its stop ends. New file, 18 Nov 2026. Descriptive; declared in AMENDMENT_08.

Input: out/ext/<run>.npz from rev_e1_extended_truth_extract_v01.py (extended clearance clearX_, censored and late flags).
Scorings (wrong go only; the caution axis keeps the 3 s scoring's first truly safe row and truly safe selections, as of record):
  est    a pair is unsafe when its extended clearance is <= 0. Pairs whose stop is unfinished at the end of the recording
         ("censored", the pairs of count (i)) are judged on the frames that exist.
  cens   as est, and the censored pairs that est judges safe count as unsafe (sensitivity).
  For reference, recomputed here from the cache: as scored (WR) and count (ii) (ii).
Quantities as of record (optA_main_v02.summarise_pop): den0 against the scoring's perfect oracle O, denE (the 3 s oracle's
advantage), each source's D, RR0 and RR_E, by population and phase-weighted, with 95% run-bootstrap percentile intervals
(the draw of record). New ratios, per resample: denE / denE(3 s) and den0 / den0(3 s).
Usage: python -B -X utf8 rev_e2_extended_truth_score_v01.py
"""
import json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rev_common_v01 as C                   # noqa: E402
L = C.L

OUT = HERE / 'out' / 'REV_E2_EXTENDED_TRUTH_v01.json'
if OUT.exists():
    sys.exit('REFUSED: %s exists' % OUT)
t00 = time.time()
runs = C.load_runs()
CNT = C.cnt_of_record()
EXT = HERE / 'out' / 'ext'
ARMS = C.MAIN_ARMS
VARIANTS = [(t, 6.0) for t in C.TAUS] + [(0.75, a) for a in C.M8_A]
for r in runs:
    x = np.load(EXT / (r['run'] + '.npz'), allow_pickle=False)
    if not np.array_equal(x['k'], r['k']):
        raise RuntimeError('decision ticks differ for %s' % r['run'])
    r['ext'] = x; r['safe_x'] = {}
    for (tau, A) in VARIANTS:
        kk = L.vkey(tau, A)
        cx = L.clean_clear(x['clearX_' + kk])
        est = cx > 0.
        r['safe_x']['est_' + kk] = est
        r['safe_x']['cens_' + kk] = est & ~(x['cens_' + kk] & r['ev'][:, None])
        r['safe_x']['est2_' + kk] = cx > 2.0


def branch_num(s_rr, den_dec_eq):
    """Branch number of optA_lib_v02.branch_rr0 without the hull clause (1 not evaluable, 2 below the class average, 3 not
    distinguishable from zero, 4 most, 5 distinguishable from zero; 0 non-finite interval)."""
    inv = s_rr['invalid_share']; lo, hi = s_rr['ci']
    if inv > L.MAX_INVALID or not (np.isfinite(den_dec_eq) and den_dec_eq >= L.MIN_DEC_EQ):
        return 1
    if not (np.isfinite(lo) and np.isfinite(hi)):
        return 0
    if hi < 0:
        return 2
    if lo <= 0 <= hi:
        return 3
    return 4 if lo > 0.5 else 5


# the 3 s scoring, for the ratios (points and resamples)
XW = C.tables(runs, ('W1',), ['F0', 'E', 'O'])
ptW = C.points(XW, ['E', 'O'], pops=range(5))
RW = C.boot(XW, ['E', 'O'], (), [0, 1, 2, 3, 4], CNT)
spW = C.strat_point(ptW, ['E', 'O']); sbW = C.strat_boot(RW, ['E', 'O'])
print('3 s reference done (%.0f s)' % (time.time() - t00), flush=True)


def score(sc, arms, signed=False, do_boot=True):
    tab = ['F0', 'E', 'O'] + list(arms)
    names = ['E', 'O'] + list(arms)
    X = C.tables(runs, sc, tab, signed=signed)
    pts = C.points(X, names, pops=range(5))
    R = C.boot(X, names, (), [0, 1, 2, 3, 4], CNT) if do_boot else None
    Tsum = {a: X[a].sum(axis=0) for a in X}
    res = dict(pops={}, oracle_diag={C.POPS[pi]: L.oracle_frontier_diag({a: Tsum[a][:, pi, :] for a in X}) for pi in range(5)})
    items = [(C.POPS[pi], pts[pi], R[pi] if R else None, ptW[pi], RW[pi]) for pi in range(5)]
    items.append(('strat', C.strat_point(pts, names), C.strat_boot(R, names) if R else None, spW, sbW))
    for nm, pe, Rp, pw, Rw in items:
        n = pe['n']; den0 = pe['D']['O']; denE = pe['denE']
        e = dict(n=n, den0=dict(point=den0, R_pp=den0 / L.NLEV, dec_eq=L.dec_eq(den0, n)),
                 denE=dict(point=denE, R_pp=denE / L.NLEV, dec_eq=L.dec_eq(denE, n)),
                 denE_over_3s=dict(point=L.ratio(denE, pw['denE'])), den0_over_3s=dict(point=L.ratio(den0, pw['D']['O'])),
                 E_rr0=dict(point=L.ratio(denE, den0)), arms={})
        if Rp is not None:
            e['den0'].update(L.summ_den(Rp['D']['O'], den0)); e['denE'].update(L.summ_den(Rp['denE'], denE))
            e['den0']['dec_eq_ci'] = L.pct(L.dec_eq(Rp['D']['O'], Rp['n'])); e['denE']['dec_eq_ci'] = L.pct(L.dec_eq(Rp['denE'], Rp['n']))
            e['den0']['R_pp_ci'] = [v / L.NLEV for v in L.pct(Rp['D']['O'])]; e['denE']['R_pp_ci'] = [v / L.NLEV for v in L.pct(Rp['denE'])]
            if not signed:
                e['denE_over_3s'] = L.summ(C.rat(Rp['denE'], Rw['denE']), L.ratio(denE, pw['denE']))
                e['den0_over_3s'] = L.summ(C.rat(Rp['D']['O'], Rw['D']['O']), L.ratio(den0, pw['D']['O']))
            e['E_rr0'] = L.summ(C.rat(Rp['denE'], Rp['D']['O']), L.ratio(denE, den0))
        for a in arms:
            D = pe['D'][a]
            ent = dict(D=D, D_pp=D / L.NLEV, D_dec_eq=L.dec_eq(D, n), rr0=dict(point=L.ratio(D, den0)), rrE=dict(point=L.ratio(D, denE)))
            if Rp is not None:
                ent['D_dec_eq_ci'] = L.pct(L.dec_eq(Rp['D'][a], Rp['n']))
                ent['rr0'] = L.summ(C.rat(Rp['D'][a], Rp['D']['O']), L.ratio(D, den0))
                ent['rrE'] = L.summ(C.rat(Rp['D'][a], Rp['denE']), L.ratio(D, denE))
                ent['branch'] = branch_num(ent['rr0'], L.dec_eq(den0, n))
            e['arms'][a] = ent
        res['pops'][nm] = e
    return res


doc = dict(code='rev_e2_extended_truth_score_v01.py', status='post hoc, descriptive; AMENDMENT_08', scorings={}, pair_counts={})
# pair counts per variant
for (tau, A) in VARIANTS:
    kk = L.vkey(tau, A); c = dict(pairs=0, unsafe_as_scored=0, unsafe_est=0, late_safe_as_scored=0, late_safe_now_unsafe=0,
                                  censored_safe_as_scored=0, censored_safe_est=0, unsafe_W1=0, decisions_no_safe_row_est=0)
    for r in runs:
        ev = r['ev'][:, None]; x = r['ext']
        sR = L.clean_clear(r['cache'][kk]) > 0.; est = r['safe_x']['est_' + kk]
        late = x['late_' + kk]; cens = x['cens_' + kk]
        c['pairs'] += int(ev.sum()) * 17
        c['unsafe_as_scored'] += int((~sR & ev).sum()); c['unsafe_est'] += int((~est & ev).sum())
        c['late_safe_as_scored'] += int((sR & late & ev).sum()); c['late_safe_now_unsafe'] += int((sR & late & ~est & ev).sum())
        c['censored_safe_as_scored'] += int((sR & cens & ev).sum()); c['censored_safe_est'] += int((est & cens & ev).sum())
        c['unsafe_W1'] += int((~(r['clear1'] > 0.) & ev).sum())
        c['decisions_no_safe_row_est'] += int((r['ev'] & ~est.any(axis=1)).sum())
    doc['pair_counts'][kk] = c
print(json.dumps(doc['pair_counts']['t0p75_a6p0']), flush=True)

KEY = L.vkey(0.75, 6.0)
plan = [('est_' + KEY, ('X', 'est_' + KEY), ARMS, False, True),
        ('cens_' + KEY, ('X', 'cens_' + KEY), ARMS, False, True),
        ('asscored_' + KEY, ('WR', 0.75, 6.0), ARMS, False, False),
        ('ii_' + KEY, ('ii', 0.75, 6.0), ARMS, False, False),
        ('est_signed_' + KEY, ('X', 'est_' + KEY), ['N', 'NA', 'CK3', 'A1'], True, True),
        ('est_gap2_' + KEY, ('X', 'est2_' + KEY), ARMS, False, False)]
for t in C.TAUS:
    if t != 0.75:
        kk = L.vkey(t, 6.0)
        plan.append(('est_' + kk, ('X', 'est_' + kk), ['N', 'NA', 'CK3', 'A1'], False, True))
        plan.append(('cens_' + kk, ('X', 'cens_' + kk), ['N', 'CK3'], False, False))
for a in C.M8_A:
    kk = L.vkey(0.75, a)
    plan.append(('est_' + kk, ('X', 'est_' + kk), ['N', 'NA', 'CK3', 'A1'], False, False))
for name, sc, arms, signed, do_boot in plan:
    doc['scorings'][name] = score(sc, arms, signed=signed, do_boot=do_boot)
    doc['scorings'][name]['signed_caution'] = signed; doc['scorings'][name]['bootstrap'] = do_boot
    e = doc['scorings'][name]['pops']['all']
    print('%s done (%.0f s): den0 %.4f pp, denE/3s %.4f' % (name, time.time() - t00, e['den0']['R_pp'], e['denE_over_3s']['point']),
          flush=True)
    OUT.with_suffix('.partial.json').write_text(C.jdump(doc), encoding='utf-8')
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
doc['common_sha256'] = L.sha256_file(HERE / 'rev_common_v01.py')
OUT.write_text(C.jdump(doc), encoding='utf-8')
OUT.with_suffix('.partial.json').unlink()
print('written %s (%.0f s)' % (OUT, time.time() - t00))
