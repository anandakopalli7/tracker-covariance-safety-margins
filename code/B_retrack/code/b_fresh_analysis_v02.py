"""v13 package B on the FRESH lead-braking runs: per tracker variant, the descriptive values of B_FRESH_DEFINITIONS_v02.md (A10 section
5.7: variants B2-B4, B1's transition sensitivities, the ceilings E5_x, the margin-ratio check; A10 section 3 B3/B4 rule inputs on fresh
runs). New file, 20 Nov 2026 (Claude Opus 5.5). Status: descriptive. The frozen v01 code and the library are not edited.

Same computations as b_analysis_v01.py (loader masks, margin ratio, E5_x, gridless step frontier, lag), restricted to the sources the
keys need (F0_x, E_x, N_x, CK3_x, E5_x). Resampling: package CD's gl_fast_v13 (read-only import; identical to a9_common_v01.Gridless +
optA_lib_v02.eval_scoring, CD's test_gl_fast_v13.py) over optA_lib_v02.boot_counts(105, 20000, 20261911), runs in ascending id order.
Inputs (read-only): CV0 and B1 from CD_capture\\arrays\\<CV0|B1>\\<rid>.npz; B3, B4, B2, B1_d090, B1_d098 from
B_retrack\\out\\retrack_fresh\\<x>\\<rid>_arrays.npz (b_fresh_retrack_v02.py).
Outputs: out\\fresh\\B_FRESH_<x>_v02.json and out\\fresh\\boot_<x>.npz (per-resample denE, n, D_N, D_E5x, D_CK3).
Lock gate: refuses unless revision_v13\\LOCK_A10_2.txt exists, except --test-old: the 35 old evaluation runs (B_retrack\\out\\retrack\\<x>\\),
the first 2,000 rows of the draw of record (default_rng(20261113)), outputs in out\\fresh_testold\\, and a check against
out\\banalysis\\B_<x>_v01.json (every shared value must be identical).
Run with B's venv (numba): B_retrack\\.venv\\Scripts\\python.exe -I -B -X utf8 b_fresh_analysis_v02.py <variant> [--test-old] [--threads 2]
"""
import os, sys, argparse
_ap = argparse.ArgumentParser()
_ap.add_argument('variant'); _ap.add_argument('--test-old', action='store_true'); _ap.add_argument('--threads', type=int, default=2)
_ap.add_argument('--nboot', type=int, default=None)
ARGS = _ap.parse_args()
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ['NUMBA_NUM_THREADS'] = str(ARGS.threads)
import json, pathlib, time, hashlib
HERE = pathlib.Path(__file__).resolve().parents[1]
WORK = HERE.parent
LIB = WORK / 'shared' / 'trackers'
CDA = WORK / 'CD_capture' / 'analysis'
sys.path.insert(0, str(LIB))
import trk_env_v01 as env                       # noqa: F401  (OPENBLAS setting only; env.setup() is not needed for scoring:
import numpy as np                              # it loads CANMOT, which this venv does not have; --test-old checks the identity)
import trk_score_v01 as S
sys.path.insert(0, str(CDA))
import gl_fast_v13 as GF                        # package CD's engine, read-only
L = S.L; C = S.A9.C

V13 = WORK.parent
LOCK2 = V13 / 'LOCK_A10_2.txt'
LOCK2C = V13 / 'LOCK_A10_2c.txt'                # coordinator, 20 Nov: no fresh value of B before LOCK_A10_2c
CD = WORK / 'CD_capture'
NAME = {'CV0': 'CV', 'B1': 'IMM', 'B3': 'CV2', 'B4': 'CA', 'B2': 'AQ', 'B1_d090': 'IMM090', 'B1_d098': 'IMM098'}
DELTA = 0.05
POPN = ['all', 'moving', 'est_before', 'est_braking', 'est_stopped', 'tru_before', 'tru_braking', 'tru_stopped',
        'est05_braking', 'est20_braking']
SRC = ['N', 'CK3', 'E5x']
SEED_FRESH, NBOOT_FRESH = 20261911, 20000
OLD_RUNS = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def fresh_ids():
    cases = json.loads((CD / 'CASES_C_v13.json').read_text(encoding='utf-8'))['cases']
    rp = CD / 'REPLACEMENTS_C_v13.json'
    rep = json.loads(rp.read_text(encoding='utf-8'))['replacements'] if rp.is_file() else {}
    return sorted('pc13_%s_native' % rep.get(c['case'], c['case']) for c in cases if c['family'] == 'lead_braking')


def arrays_path(variant, rid, test_old):
    if test_old:
        return HERE / 'out' / 'retrack' / variant / (rid + '_arrays.npz')
    if variant in ('CV0', 'B1'):
        return CD / 'arrays' / variant / (rid + '.npz')
    return HERE / 'out' / 'retrack_fresh' / variant / (rid + '_arrays.npz')


def load(variant, ids, test_old):
    runs = []
    for rid in ids:
        z = np.load(arrays_path(variant, rid, test_old), allow_pickle=False)
        ev = z['evaluated'].astype(bool)
        ph_t = np.asarray(z['phase']).astype(np.int64)
        ph_e = S.est_phase(z['vhat'], z['ahat_long'], z['lead_found'], -1.0)
        ph_e05 = S.est_phase(z['vhat'], z['ahat_long'], z['lead_found'], -0.5)
        ph_e20 = S.est_phase(z['vhat'], z['ahat_long'], z['lead_found'], -2.0)
        v0 = z['v0']
        masks = (ev, ev & (v0 > 0.5), ev & (ph_e == 0), ev & (ph_e == 1), ev & (ph_e == 2),
                 ev & (ph_t == 0), ev & (ph_t == 1), ev & (ph_t == 2), ev & (ph_e05 == 1), ev & (ph_e20 == 1))
        now = z['now']; i2 = np.flatnonzero(ph_t == 2)
        t_stop = now - now[i2[0]] if i2.size else np.full(now.size, np.nan)
        runs.append(dict(run=rid, desired=float(z['des'][0]), idx55=z['idx55'].astype(np.int64), clear1=L.clean_clear(z['clear']),
                         vbar=z['vbar'], ev=ev, masks=masks, sel={}, late={},
                         crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float),
                               'CK3': np.asarray(z['cCK3'], float)},
                         lead={k: z[k] for k in ('lead_found', 'dx_pred3')}, ph_t=ph_t, ph_e=ph_e, t_stop=t_stop))
    return runs


def classify(r_s, c_s, barely):
    lo_r = r_s['ci'][0]; c_lo, c_hi = c_s['ci']
    if lo_r > 0:
        cls = 'recovers'
    elif c_lo > DELTA:
        cls = 'uninformative variation'
    elif c_lo > -DELTA and c_hi < DELTA:
        cls = 'amplitude-limited'
    else:
        cls = 'inconclusive'
    return dict(classification=cls, barely_varies=bool(barely), rule='A10 H3 wording applied descriptively (A10 section 5.7)')


def evaluate(P, W, chunk=500):
    out = dict(denE=[], n=[], D={a: [] for a in P.names[2:]})
    for s in range(0, W.shape[0], chunk):
        e = GF.evaluate(P, W[s:s + chunk])
        out['denE'].append(e['denE']); out['n'].append(e['n'])
        for a in P.names[2:]:
            out['D'][a].append(e['D'][a])
    return dict(denE=np.concatenate(out['denE']), n=np.concatenate(out['n']), D={a: np.concatenate(v) for a, v in out['D'].items()})


def check_v01(variant, doc):
    """--test-old: every value shared with out\\banalysis\\B_<variant>_v01.json must be identical."""
    v1 = json.loads((HERE / 'out' / 'banalysis' / ('B_%s_v01.json' % variant)).read_text(encoding='utf-8'))
    pairs = []
    for k in ('median', 'q05', 'q95', 'A', 'share_within_5pct', 'barely_varies', 'n'):
        pairs.append(('ratio.' + k, doc['ratio_N_F0'][k], v1['ratio_N_F0'][k]))
    for pn in POPN:
        for k in ('R_pp', 'R_deceq', 'denE', 'n'):
            pairs.append(('points.%s.%s' % (pn, k), doc['points'][pn][k], v1['points'][pn][k]))
        for a, a1 in (('N', 'N'), ('CK3', 'CK3'), ('E5x', 'E5x')):
            pairs.append(('points.%s.RR.%s' % (pn, a), doc['points'][pn]['RR'][a], v1['points'][pn]['RR'][a1]))
    I1 = v1['intervals']['all']
    for k, k1 in (('R_pp', 'R_pp'), ('RR_N', 'RR_N'), ('RR_CK3', 'RR_CK3'), ('RR_E5x', 'RR_E5x')):
        pairs.append(('intervals.all.%s.point' % k, doc['intervals']['all'][k]['point'], I1[k1]['point']))
        pairs.append(('intervals.all.%s.ci' % k, doc['intervals']['all'][k]['ci'], I1[k1]['ci']))
    pairs.append(('intervals.all.R_deceq.ci', doc['intervals']['all']['R_deceq']['ci'], I1['R_deceq']['ci']))
    pairs.append(('lag.median', doc['lag_dx3_first_second_after_stop']['median'], v1['lag_dx3_first_second_after_stop']['median']))
    pairs.append(('lag.n', doc['lag_dx3_first_second_after_stop']['n'], v1['lag_dx3_first_second_after_stop']['n']))
    pairs.append(('classification', doc['classification']['classification'], v1['classification_exploratory']['classification']))
    same = lambda a, b: (a == b) or (isinstance(a, float) and isinstance(b, float) and np.isnan(a) and np.isnan(b))  # noqa: E731
    bad = [(k, a, b) for k, a, b in pairs if not (same(a, b) if not isinstance(a, list) else all(same(x, y) for x, y in zip(a, b)))]
    return dict(compared=len(pairs), identical=len(pairs) - len(bad), differing=bad)


def main():
    variant = ARGS.variant
    if variant not in NAME:
        raise SystemExit('unknown variant %s' % variant)
    t00 = time.time()
    if ARGS.test_old:
        gate = 'TEST_OLD: old runs only; no fresh value'; ids = OLD_RUNS
        CNT = C.cnt_of_record()[:(ARGS.nboot or 2000)]
        draw = 'first %d rows of default_rng(20261113).integers(0, 35, (20000, 35)) (draw of record), runs in name order' % CNT.shape[0]
        outd = HERE / 'out' / 'fresh_testold'
    else:
        if not LOCK2.is_file():
            raise SystemExit('REFUSED: LOCK_A10_2.txt does not exist; no fresh value is computed before Lock 2 (A10 sections 4, 5.2)')
        if not LOCK2C.is_file():
            raise SystemExit('REFUSED: LOCK_A10_2c.txt does not exist; no fresh value of B before it (coordinator, 20 Nov)')
        gate = 'LOCK_A10_2 sha256 %s; LOCK_A10_2c sha256 %s' % (sha(LOCK2), sha(LOCK2C)); ids = fresh_ids()
        if len(ids) != 105:
            raise SystemExit('REFUSED: %d lead-braking run ids, expected 105' % len(ids))
        missing = [r for r in ids if not arrays_path(variant, r, False).is_file()]
        if missing:
            raise SystemExit('REFUSED: %d arrays files missing for %s, e.g. %s' % (len(missing), variant, missing[:3]))
        nb = ARGS.nboot or NBOOT_FRESH
        CNT = L.boot_counts(len(ids), NBOOT_FRESH, SEED_FRESH)[:nb]
        draw = 'optA_lib_v02.boot_counts(105, 20000, 20261911)%s, runs in ascending id order' % ('' if nb == NBOOT_FRESH else ' first %d rows' % nb)
        outd = HERE / 'out' / 'fresh'
    outd.mkdir(parents=True, exist_ok=True)
    runs = load(variant, ids, ARGS.test_old)
    doc = dict(code='b_fresh_analysis_v02.py', variant=variant, name=NAME[variant], gate=gate, n_runs=len(runs),
               status='descriptive (A10 section 5.7)' if not ARGS.test_old else 'TEST on old runs (exploratory data of record)',
               definitions='B_retrack/B_FRESH_DEFINITIONS_v02.md', populations=POPN, nboot=int(CNT.shape[0]), draw=draw,
               engine='CD_capture/analysis/gl_fast_v13.py sha256 ' + sha(CDA / 'gl_fast_v13.py'))
    rat = S.margin_ratios(runs, 'N', 'F0'); rs = S.ratio_summary(rat)
    doc['ratio_N_F0'] = rs
    u, uinfo = S.e5_u(runs, 'F0', 'E'); doc['e5_ranks'] = uinfo
    S.add_oracle(runs, 'E5x', 'F0', rs['median'], rs['A'], u)
    G = S.gridless(runs, ['F0', 'E'] + SRC)
    print('gridless built (%.0f s)' % (time.time() - t00), flush=True)
    doc['points'] = {pn: S.rr_gl(G, 'F0', 'E', SRC, pop=pi) for pi, pn in enumerate(POPN)}
    P = GF.Prepared(G, ['F0', 'E'] + SRC, 0)
    b = evaluate(P, CNT)
    print('resamples done (%.0f s)' % (time.time() - t00), flush=True)
    pt = doc['points']['all']
    e = dict(R_pp=L.summ(b['denE'] / L.NLEV, pt['R_pp']), R_deceq=dict(point=pt['R_deceq'], ci=L.pct(L.dec_eq(b['denE'], b['n']))))
    for a in SRC:
        e['RR_' + a] = S.rr_summary(pt, b, a)
    with np.errstate(invalid='ignore', divide='ignore'):
        ok = np.isfinite(b['denE']) & (b['denE'] > 0)
        rrN = np.where(ok, b['D']['N'] / b['denE'], np.nan); rrX = np.where(ok, b['D']['E5x'] / b['denE'], np.nan)
    e['RR_N_minus_E5x'] = L.summ(rrN - rrX, pt['RR']['N'] - pt['RR']['E5x'])
    doc['intervals'] = {'all': e}
    doc['classification'] = classify(e['RR_N'], e['RR_E5x'], rs['barely_varies'])
    lag = []
    for r in runs:
        z = r['lead']; m = r['ev'] & (r['ph_t'] == 2) & (r['t_stop'] >= 0) & (r['t_stop'] < 1) & z['lead_found'].astype(bool)
        lag.append(z['dx_pred3'][m])
    lag = np.concatenate(lag); lag = lag[np.isfinite(lag)]
    doc['lag_dx3_first_second_after_stop'] = dict(n=int(lag.size), median=float(np.median(lag)) if lag.size else None,
                                                  q25=float(np.percentile(lag, 25)) if lag.size else None,
                                                  q75=float(np.percentile(lag, 75)) if lag.size else None)
    doc['n_dec'] = int(sum(int(r['ev'].sum()) for r in runs))
    np.savez_compressed(outd / ('boot_%s.npz' % variant), denE=b['denE'], n=b['n'], D_N=b['D']['N'], D_E5x=b['D']['E5x'], D_CK3=b['D']['CK3'])
    if ARGS.test_old:
        doc['identity_vs_v01'] = check_v01(variant, doc)
    doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    (outd / ('B_FRESH_%s_v02.json' % variant)).write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    print(json.dumps(dict(variant=variant, R_pp=e['R_pp'], RR_N=e['RR_N'], c=e['RR_E5x'], within5=rs['share_within_5pct'],
                          lag=doc['lag_dx3_first_second_after_stop']['median'], cls=doc['classification']['classification'],
                          identity=doc.get('identity_vs_v01', {}).get('identical'), compared=doc.get('identity_vs_v01', {}).get('compared'),
                          seconds=round(doc['seconds'])), default=float), flush=True)


if __name__ == '__main__':
    main()
