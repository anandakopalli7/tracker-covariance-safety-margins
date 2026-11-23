"""Recount4 (independent second program): the scoring of the reaction-and-stop estimate (Tables III and IV of the manuscript).

Written from revision_v11\\recount4\\RECOUNT4_BRIEF_v01.md and revision_v11\\recount\\RECOUNT_BRIEF_v01.md only.
Imports the second-program lineage: revision_v11\\recount3\\r3_lib_v01.py (which imports revision_v11\\recount\\rc_lib_v01.py):
loader of the 35 evaluation runs, selection on the grid, per-run statistics, batched step frontier, percentile helpers.
Reads the clearances of revision_v11\\recount2\\out\\<run>.npz. Opens nothing of revision_v11\\analysis, draft, package_v11
or P\\11_ojits\\A6R\\code.

Scorings (wrong-go flag; the caution axis always uses the 3 s commitment: truly safe = clear > 0):
  w1                the 3 s commitment (unsafe when clear <= 0); reference for "relative to 3 s"
  w1_signed         the same with signed caution; second reference for est_signed
  est_<setting>     unsafe when clearX <= 0 (NaN = unsafe)                                   9 settings
  cens_<setting>    as est, and every pair with cens true counts as unsafe                    6 settings with 6 m/s2
  est_signed_t0p75_a6p0   est's wrong go, signed caution
  asscored_<setting>      unsafe when clear61 <= 0 (the brief asks for t0p75_a6p0; the others are added)
D columns: F0, E, N, NA, AM, CK3, Q, O.  denE = D[E], den0 = D[O].

Usage: python -B -X utf8 r4_items_v01.py            -> RECOUNT4_RESULTS_v01.json, boot\\<scoring>.npz
       python -B -X utf8 r4_items_v01.py quick      -> first 400 rows of the draw of record, ..._quick.json (test only)
"""
import hashlib, json, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'recount3'))
sys.path.insert(0, str(HERE.parent / 'recount'))
import r3_lib_v01 as R   # noqa: E402
L = R.L

R2_OUT = HERE.parent / 'recount2' / 'out'
R2_SCORING = HERE.parent / 'recount2' / 'RECOUNT2_SCORING_v01.json'
LOG = HERE / 'r4_items_v01_log.txt'
QUICK = 'quick' in sys.argv
NB = 400 if QUICK else L.NBOOT
BOOT_DIR = HERE / ('boot_quick' if QUICK else 'boot')
SETTINGS = ('t0p50_a6p0', 't0p75_a6p0', 't1p00_a6p0', 't1p25_a6p0', 't1p50_a6p0', 't1p80_a6p0', 't0p75_a4p0', 't0p75_a5p0', 't0p75_a7p6')
A6 = tuple(k for k in SETTINGS if k.endswith('_a6p0'))
MAIN = 't0p75_a6p0'
A7 = len(L.ARMS)
AI = {a: i for i, a in enumerate(L.ARMS)}
IO = A7                                   # column of the perfect oracle O
SRC = ('N', 'NA', 'AM', 'CK3', 'Q')
POPS = R.POPS                             # all, moving, phase0, phase1, phase2
NLEV = float(L.NLEV)

SCORINGS = [('w1', 'w1', None, False), ('w1_signed', 'w1', None, True)]
SCORINGS += [('est_' + k, 'est', k, False) for k in SETTINGS]
SCORINGS += [('cens_' + k, 'cens', k, False) for k in A6]
SCORINGS += [('est_signed_' + MAIN, 'est', MAIN, True)]
SCORINGS += [('asscored_' + k, 'asscored', k, False) for k in SETTINGS]
ON_BRIEF = set(['est_' + k for k in SETTINGS] + ['cens_' + k for k in A6] + ['est_signed_' + MAIN, 'asscored_' + MAIN])


def load():
    ds = L.load_all()
    for d in ds:
        ev = d['ev_all']
        with np.load(R2_OUT / (d['run'] + '.npz'), allow_pickle=False) as z:
            if not np.array_equal(z['k'], d['k_all']):
                raise RuntimeError('%s: k of recount2 differs from the stored k' % d['run'])
            if not np.array_equal(z['evaluated'].astype(bool), ev):
                raise RuntimeError('%s: evaluated flags of recount2 differ' % d['run'])
            d['X'] = {k: np.asarray(z['clearX_' + k], float)[ev] for k in SETTINGS}
            d['W'] = {k: np.asarray(z['clear61_' + k], float)[ev] for k in SETTINGS}
            d['late'] = {k: np.asarray(z['late_' + k]).astype(bool)[ev] for k in SETTINGS}
            d['cens'] = {k: np.asarray(z['cens_' + k]).astype(bool)[ev] for k in SETTINGS}
    return ds


def safe_flag(d, variant, key):
    """Rows the scoring judges safe (n, 17). A NaN clearance is never > 0, so it counts as unsafe."""
    if variant == 'w1':
        return d['clear'] > 0.
    if variant == 'est':
        return d['X'][key] > 0.
    if variant == 'cens':
        return (d['X'][key] > 0.) & ~d['cens'][key]
    if variant == 'asscored':
        return d['W'][key] > 0.
    raise ValueError(variant)


def fl(x):
    x = float(x)
    return x if np.isfinite(x) else None


def q_plain(point, boot):
    ci, nbad = R.ci_plain(boot)
    return dict(point=fl(point), ci=ci, n_not_finite=nbad)


def q_ratio(pn, pd, bn, bd):
    """Point = quotient of the full-sample values; interval over the resamples with a positive denominator."""
    ci, nlo = R.ci_ratio(bn, bd)
    with np.errstate(invalid='ignore', divide='ignore'):
        pt = np.float64(pn) / np.float64(pd)
    return dict(point=fl(pt), ci=ci, n_left_out=nlo, point_denominator_positive=bool(pd > 0))


def block(n0, D0p, nbp, Dbp, refs):
    """One population of one scoring. n0 scalar, D0p (8,), nbp (B,), Dbp (B, 8); refs: name -> (D0 (8,), Db (B, 8)) of the
    reference scoring on the same population and the same resamples."""
    e = dict(n=float(n0))
    for name, col in (('den0', IO), ('denE', 1)):
        b = Dbp[:, col]
        e[name] = dict(sum=q_plain(D0p[col], b), pp=q_plain(D0p[col] / NLEV, b / NLEV),
                       deceq=q_plain(D0p[col] / NLEV / 100. * n0, b / NLEV / 100. * nbp))
        e['share_%s_le0' % name] = float((b <= 0).mean())
        e['n_%s_le0' % name] = int((b <= 0).sum())
        e['n_%s_not_finite' % name] = int((~np.isfinite(b)).sum())
    e['rel'] = {}
    for rname, (r0, rb) in refs.items():
        e['rel'][rname] = dict(denE=q_ratio(D0p[1], r0[1], Dbp[:, 1], rb[:, 1]), den0=q_ratio(D0p[IO], r0[IO], Dbp[:, IO], rb[:, IO]))
    e['src'] = {}
    for a in SRC:
        c = AI[a]; b = Dbp[:, c]
        e['src'][a] = dict(D_sum=q_plain(D0p[c], b), D_pp=q_plain(D0p[c] / NLEV, b / NLEV),
                           D_deceq=q_plain(D0p[c] / NLEV / 100. * n0, b / NLEV / 100. * nbp),
                           RR0=q_ratio(D0p[c], D0p[IO], b, Dbp[:, IO]), RR=q_ratio(D0p[c], D0p[1], b, Dbp[:, 1]))
    e['RR0_E'] = q_ratio(D0p[1], D0p[IO], Dbp[:, 1], Dbp[:, IO])
    return e


def pair_counts(ds):
    out = {}
    for key in SETTINGS:
        c = dict(evaluated_decisions=0, pairs=0, pairs_unsafe_window=0, pairs_unsafe_est=0, pairs_late=0, pairs_late_safe_window=0,
                 pairs_late_safe_window_unsafe_est=0, pairs_cens=0, pairs_cens_safe_window=0, pairs_cens_safe_window_safe_est=0,
                 decisions_without_safe_row_est=0, decisions_without_safe_row_window=0, decisions_without_safe_row_cens_unsafe=0,
                 decisions_with_a_cens_pair=0, pairs_safe_window_unsafe_est=0, pairs_unsafe_window_safe_est=0, pairs_cens_not_late=0,
                 nan_clearX=0, nan_clear61=0, pairs_unsafe_3s_commitment=0)
        for d in ds:
            x = d['X'][key]; w = d['W'][key]; la = d['late'][key]; ce = d['cens'][key]
            sx = x > 0.; sw = w > 0.
            c['evaluated_decisions'] += int(d['n']); c['pairs'] += int(x.size)
            c['pairs_unsafe_window'] += int((~sw).sum()); c['pairs_unsafe_est'] += int((~sx).sum())
            c['pairs_late'] += int(la.sum()); c['pairs_late_safe_window'] += int((la & sw).sum())
            c['pairs_late_safe_window_unsafe_est'] += int((la & sw & ~sx).sum())
            c['pairs_cens'] += int(ce.sum()); c['pairs_cens_safe_window'] += int((ce & sw).sum())
            c['pairs_cens_safe_window_safe_est'] += int((ce & sw & sx).sum())
            c['decisions_without_safe_row_est'] += int((~sx.any(1)).sum())
            c['decisions_without_safe_row_window'] += int((~sw.any(1)).sum())
            c['decisions_without_safe_row_cens_unsafe'] += int((~(sx & ~ce).any(1)).sum())
            c['decisions_with_a_cens_pair'] += int(ce.any(1).sum())
            c['pairs_safe_window_unsafe_est'] += int((sw & ~sx).sum()); c['pairs_unsafe_window_safe_est'] += int((~sw & sx).sum())
            c['pairs_cens_not_late'] += int((ce & ~la).sum())
            c['nan_clearX'] += int(np.isnan(x).sum()); c['nan_clear61'] += int(np.isnan(w).sum())
            c['pairs_unsafe_3s_commitment'] += int((~(d['clear'] > 0.)).sum())
        out[key] = c
    return out


def main():
    t0 = time.time()
    L.log('r4_items_v01 start, nboot %d, numpy %s' % (NB, np.__version__), file=LOG)
    BOOT_DIR.mkdir(exist_ok=True)
    ds = load()
    idx = L.draw_of_record()[:NB]
    res = dict(program='recount4: r4_items_v01.py (imports revision_v11\\recount3\\r3_lib_v01.py and revision_v11\\recount\\rc_lib_v01.py)',
               numpy=np.__version__, nboot=int(idx.shape[0]),
               bootstrap_of_record='numpy.random.default_rng(20261113).integers(0, 35, size=(20000, 35))',
               interval='95% percentile (numpy.percentile 2.5, 97.5); ratios over the resamples with a positive denominator',
               columns_of_D=list(L.ARMS) + ['O'], settings=list(SETTINGS), on_brief=sorted(ON_BRIEF))
    res['data'] = dict(runs=len(ds), stored_decisions=int(sum(d['n_stored'] for d in ds)), evaluated_decisions=int(sum(d['n'] for d in ds)),
                       nan_clear_evaluated=int(sum(d['n_nan_clear_eval'] for d in ds)),
                       phase_counts_evaluated={str(p): int(sum((d['phase'] == p).sum() for d in ds)) for p in range(4)},
                       moving_evaluated=int(sum((d['v0'] > 0.5).sum() for d in ds)))
    res['counts'] = pair_counts(ds)
    L.log('pair counts done', file=LOG)

    store = {}
    for name, variant, key, signed in SCORINGS:
        t1 = time.time()
        M = np.stack([L.run_row(d, L.masks_std(d), safe_flag(d, variant, key), d['clear'] > 0., signed) for d in ds])
        nn, S, O = R.split(M.sum(0), 5, A7)
        D0, info0 = R.evaluate_g(nn, S, O, want=True)
        nb, Db, nlb = R.boot_g(M, idx, 5, A7)
        nt0, Dw0 = R.weighted(nn, D0); ntb, Dwb = R.weighted(nb, Db)
        store[name] = dict(nn=nn, D0=D0, nb=nb, Db=Db, nt0=nt0, Dw0=Dw0, ntb=ntb, Dwb=Dwb, info0=info0, nlb=nlb)
        np.savez(BOOT_DIR / (name + '.npz'), nn=nn, D0=D0, nb=nb, Db=Db, nt0=nt0, Dw0=Dw0, ntb=ntb, Dwb=Dwb, nlb=nlb,
                 c0=info0['c0'], w0=info0['w0'], hi=info0['hi'], cO=info0['cO'], wO=info0['wO'])
        L.log('%-26s all: n %d denE %.9f den0 %.9f  (%.0f s)' % (name, nn[0, 0], D0[0, 0, 1], D0[0, 0, IO], time.time() - t1), file=LOG)

    res['scorings'] = {}
    for name, variant, key, signed in SCORINGS:
        s = store[name]
        refnames = {}
        if name not in ('w1', 'w1_signed'):
            refnames['3s_commitment'] = 'w1'
            if signed:
                refnames['3s_commitment_signed'] = 'w1_signed'
            if variant in ('est', 'cens') and not signed:
                refnames['3s_window_same_setting'] = 'asscored_' + key
        e = dict(variant=variant, setting=key, signed_caution=bool(signed), on_brief=bool(name in ON_BRIEF),
                 reference_scorings=refnames, pops={})
        for pi, pn in enumerate(POPS):
            refs = {rn: (store[r]['D0'][0, pi], store[r]['Db'][:, pi]) for rn, r in refnames.items()}
            b = block(s['nn'][0, pi], s['D0'][0, pi], s['nb'][:, pi], s['Db'][:, pi], refs)
            b['undefined_frontier_levels_point'] = bool(s['info0']['nanlev'][0, pi])
            b['resamples_with_undefined_frontier'] = int(s['nlb'][:, pi].sum())
            b['F0_zero_margin'] = dict(caution_pct=fl(s['info0']['c0'][0, pi]), wrong_go_pct=fl(s['info0']['w0'][0, pi]))
            b['O_point'] = dict(caution_pct=fl(s['info0']['cO'][0, pi]), wrong_go_pct=fl(s['info0']['wO'][0, pi]))
            b['last_level'] = fl(s['info0']['hi'][0, pi])
            e['pops'][pn] = b
        refs = {rn: (store[r]['Dw0'][0], store[r]['Dwb']) for rn, r in refnames.items()}
        e['pops']['phase_weighted'] = block(s['nt0'][0], s['Dw0'][0], s['ntb'], s['Dwb'], refs)
        res['scorings'][name] = e

    # anchor inside the second-program lineage (recount2's optional scoring of its own clearances, points only)
    try:
        a = json.loads(R2_SCORING.read_text(encoding='utf-8'))
        anc = {}
        for pn in ('all', 'moving'):
            for theirs, mine in (('W1_3s_commitment', 'w1'), ('RS_61frames_own', 'asscored_' + MAIN), ('RS_extended', 'est_' + MAIN),
                                 ('RS_extended_censored_unsafe', 'cens_' + MAIN)):
                for q in ('denE', 'den0'):
                    v2 = a['pops'][pn][theirs][q]; v4 = res['scorings'][mine]['pops'][pn][q]['sum']['point']
                    anc['%s.%s.%s' % (pn, mine, q)] = dict(recount2=v2, recount4=v4, abs_diff=abs(v2 - v4))
        res['anchor_recount2_scoring'] = dict(values=anc, max_abs_diff=max(v['abs_diff'] for v in anc.values()))
        L.log('anchor against recount2 scoring: max abs diff %.3g' % res['anchor_recount2_scoring']['max_abs_diff'], file=LOG)
    except Exception as ex:   # the anchor is a convenience, not a result
        res['anchor_recount2_scoring'] = dict(error=repr(ex))
    res['seconds'] = time.time() - t0
    out = HERE / ('RECOUNT4_RESULTS_v01%s.json' % ('_quick' if QUICK else ''))
    L.jdump(res, out)
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    stamp = time.strftime('%Y-%m-%d %H:%M:%S')
    L.log('written %s sha256 %s at %s' % (out.name, sha, stamp), file=LOG)
    if not QUICK:
        (HERE / 'RECOUNT4_RESULTS_v01.sha256.txt').write_text('%s  %s  written %s\n' % (sha, out.name, stamp), encoding='utf-8')
    L.log('r4_items_v01 end, %.0f s' % (time.time() - t0), file=LOG)


if __name__ == '__main__':
    main()
