"""Revision v13, package C: B7 rate x latency on the fresh lead-braking runs (AMENDMENT_10_v13 sec. 3 B7, sec. 5.7 "B7 at every rate x
latency"). Descriptive: nominal 95% percentile intervals over 20,000 run resamples (default_rng(20261911)). New file, 20 Nov 2026
(Claude Opus 5.5). Definitions: CD_capture\\CD_DEFINITIONS_TRK_v13.md (sec. 2, 3, 6, 7, 8).

Chains (arrays\\B7_<r>_<L>\\<rid>.npz from x_trk_extract_v13.py: CV0 re-tracked on the offline detections of rate r with latency L,
F0 with the P-bar of record), (r, L) in (2, 0), (2, 0.1), (5, 0), (5, 0.1), (5, 0.2), (10, 0), (10, 0.1), (10, 0.2):
  B7.<r>.<L>.R              R_gl (pp), all evaluated decisions, on the chain's own room
  B7.<r>.<L>.as_room(.pp)   after-stop room: R_gl in truth phase 2 (the run's CV0 truth phase), decision-equivalents (and pp)
  B7.<r>.<L>.RR_N(.ci)      RR_gl(N) of the chain
  B7.<r>.<L>.RR_CK3         RR_gl(CK3) of the chain
  B7.<r>.<L>.lag            median dx_pred3 over evaluated truth-phase-2 decisions in the first second after the run's first one
  B7.identity               "pass" | "fail": the offline 2 Hz detection reproduces every logged online tick (combined-cloud SHA-256
                            equal, same box count, translation and size within 1e-6 m)
  B7.ratio_10_2             as_room(10, 0.1) / as_room(2, 0);  B7.rule_rate "consequence" | "holds";  B7.rule_N "qualified" | "holds"
Lock gate: refuses unless BOTH revision_v13\\LOCK_A10_2.txt and LOCK_A10_2c.txt exist (stage-2 code), except --test-old: then it runs
on OLD run p1b_fit_finite_0037 (its B7 file b7\\p1b_fit_finite_0037\\, its capture in the old archive; arrays from
x_trk_extract_v13.py --test-old), checks that the 2 Hz chain at L = 0 equals the logged arrays exactly (an extract of the logged files,
and package B's stored CV0 array), and reports the lag statistics of every chain (descriptive only, A10 B7)
-> out\\TESTOLD_B7_v13[_<tag>].json. Fresh output: out\\C_B7_v13.json. Never overwrites. No B.<x>.* key is written (package B's).
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\c_b7_v13.py [--test-old [--arrays DIR]] [--nboot N] [--tag S]
"""
import argparse, json, os, pathlib, sys, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('NUMBA_NUM_THREADS', '2')
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cd_common_v13 as CC               # noqa: E402
import trk_env_v01 as env                # noqa: E402
env.setup()
import numpy as np                       # noqa: E402
import trk_score_v01 as TS               # noqa: E402
L = CC.L

B7 = [(2, 0.0), (2, 0.1), (5, 0.0), (5, 0.1), (5, 0.2), (10, 0.0), (10, 0.1), (10, 0.2)]
NAMES = ['N', 'CK3']
P = pathlib.Path(os.environ.get('V13_P_ROOT', r'<library folder>'))
OLD_ARCH = P / '07_fit_runs' / 'archives'
PBAR_RECORD = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'pbar_tuning_v01.json'
B_CV0 = CC.WORK / 'B_retrack' / 'out' / 'retrack' / 'CV0'
TEST_ARR = CC.OUT / 'testold_b7_arrays'
TEST_RUN = 'p1b_fit_finite_0037'
BOX_TOL = 1e-6
LEVEL, CAL = 0.95, 'nominal95'


def fin(x):
    return float(x) if x is not None and np.isfinite(x) else None


def lag_of(runs):
    """CD_DEFINITIONS_TRK_v13.md sec. 6 (b_analysis_v01's lag): per run t_stop = now of its first decision with truth phase 2; evaluated
    truth-phase-2 decisions with 0 <= now - t_stop < 1 s and lead_found; dx_pred3 pooled over runs (finite); median, n, q25, q75."""
    vals = []
    for r in runs:
        ph = r['ph_t']; now = r['lead']['now']; i2 = np.flatnonzero(ph == 2)
        if not i2.size:
            continue
        t = now - now[i2[0]]
        m = r['ev'] & (ph == 2) & (t >= 0) & (t < 1) & r['lead']['lead_found']
        vals.append(r['lead']['dx_pred3'][m])
    v = np.concatenate(vals) if vals else np.zeros(0)
    v = v[np.isfinite(v)]
    return dict(n=int(v.size), median=float(np.median(v)) if v.size else None, q25=float(np.percentile(v, 25)) if v.size else None,
                q75=float(np.percentile(v, 75)) if v.size else None)


def lstr(Lt):
    return '0' if Lt == 0 else ('%g' % Lt)


def folder(r, Lt):
    return 'B7_%d_%s' % (r, lstr(Lt))


def keypre(r, Lt):
    return 'B7.%d.%s.' % (r, lstr(Lt))


def paths(rid, test):
    if test:
        rd = OLD_ARCH / rid; caps = [p for p in (rd / 'x' / rid / 'capture').iterdir() if p.is_dir()]
    else:
        if not (CC.CD / 'runs' / rid / 'LOGS_OK').is_file():
            raise SystemExit('REFUSED: %s has no LOGS_OK' % rid)
        rd = CC.CD / 'runs' / rid / rid; caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
    assert len(caps) == 1, rid
    return rd, caps[0]


def identity_run(rid, test):
    """A10 B7 (i) for one run: logged online ticks (capture detections.jsonl) vs the offline B7 rows (b7\\<rid>\\b7_detections_v13.jsonl)."""
    rd, cap = paths(rid, test)
    logged = list(env.jl(cap / 'detections.jsonl'))
    off = {x['k']: x for x in env.jl(CC.CD / 'b7' / rid / 'b7_detections_v13.jsonl')}
    dec_k = [fr['k'] for fr in env.jl(cap / 'frames.jsonl') if (fr.get('execution') or {}).get('new_decision') is not None]
    kmax_dec = max(dec_k) if dec_k else -1
    res = dict(run=rid, online_ticks=len(logged), matched=0, hash_equal=0, count_equal=0, max_abs=dict(translation=0., size=0., velocity=0., rotation=0., score=0.),
               name_mismatch=0)
    for a in logged:
        b = off.get(a['k'])
        if b is None: continue
        res['matched'] += 1; res['hash_equal'] += int(a.get('combined_hash') == b.get('combined_hash'))
        if len(a['model']) != len(b['model']): continue
        res['count_equal'] += 1
        for x, y in zip(a['model'], b['model']):
            for fld, key in (('translation', 'translation'), ('size', 'size'), ('velocity', 'velocity'), ('rotation', 'rotation')):
                d = max(abs(p - q) for p, q in zip(x[key], y[key]))
                res['max_abs'][fld] = max(res['max_abs'][fld], d)
            res['max_abs']['score'] = max(res['max_abs']['score'], abs(x['detection_score'] - y['detection_score']))
            res['name_mismatch'] += int(x['detection_name'] != y['detection_name'])
    lk = {a['k'] for a in logged}
    res['offline_2hz_rows_not_online_before_last_decision'] = sum(1 for k, x in off.items() if 2 in x['rates_hz'] and k not in lk and k <= kmax_dec)
    n = res['online_ticks']
    res['pass'] = bool(n > 0 and res['matched'] == n and res['hash_equal'] == n and res['count_equal'] == n
                       and res['max_abs']['translation'] <= BOX_TOL and res['max_abs']['size'] <= BOX_TOL)
    return res


def compare_arrays(a, b, keys=None):
    keys = keys or sorted(set(a.files) - {'meta'})
    out = {}; same = True
    for k in keys:
        if k not in b.files:
            out[k] = 'missing in reference'; same = False; continue
        x, y = a[k], b[k]
        eq = x.shape == y.shape and np.array_equal(x, y, equal_nan=x.dtype.kind == 'f')
        if not eq:
            same = False
            if x.shape == y.shape and x.dtype.kind in 'fiub':
                xx = x.astype(float); yy = y.astype(float); m = np.isfinite(xx) & np.isfinite(yy)
                out[k] = dict(max_abs=float(np.max(np.abs(xx[m] - yy[m]))) if m.any() else None,
                              finite_pattern_equal=bool(np.array_equal(np.isfinite(xx), np.isfinite(yy))))
            else:
                out[k] = 'differs (shape %s vs %s)' % (x.shape, y.shape)
    return same, out


def one_chain(r, Lt, rids, ref, W, arr_root, log):
    t0 = time.time()
    fold = folder(r, Lt)
    # runs as b_analysis_v01.load (consistency with the CV0 array; truth phase from the CV0 array); crit F0, E, N, CK3
    runs = []; nphase = 0; ages = []
    for rid, rf in zip(rids, ref):
        z = np.load(arr_root / fold / (rid + '.npz'), allow_pickle=False)
        for key in ('k', 'idx55'):
            if not np.array_equal(z[key], rf[key]):
                raise SystemExit('REFUSED: %s %s: %s differs from the CV0 array' % (fold, rid, key))
        ev = z['evaluated'].astype(bool); clear1 = L.clean_clear(z['clear'])
        if not np.array_equal(ev, rf['ev']) or not np.array_equal(clear1, rf['clear1']):
            raise SystemExit('REFUSED: %s %s: evaluated / clearance differ from the CV0 array' % (fold, rid))
        ph_t = rf['phase']; nphase += int((z['phase'].astype(int) != ph_t).sum())
        ages.append(np.asarray(z['age'], float)[ev & z['lead_found'].astype(bool)])
        masks = (ev, ev & (ph_t == 2))
        runs.append(dict(run=rid, desired=float(z['des'][0]), idx55=z['idx55'].astype(np.int64), clear1=clear1, vbar=z['vbar'], ev=ev, masks=masks,
                         crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float),
                               'CK3': np.asarray(z['cCK3'], float)}, sel={}, late={}, ph_t=ph_t,
                         lead=dict(lead_found=z['lead_found'].astype(bool), dx_pred3=np.asarray(z['dx_pred3'], float), now=np.asarray(rf['now'], float))))
    NR = len(runs)
    rs = TS.ratio_summary(TS.margin_ratios(runs, 'N', 'F0'))
    G = TS.gridless(runs, ['F0', 'E'] + NAMES)
    with np.errstate(divide='ignore', invalid='ignore'):
        pts = [TS.rr_gl(G, 'F0', 'E', NAMES, pop=p) for p in (0, 1)]
    Pp = CC.prep(G, ['F0', 'E'] + NAMES, 0)
    one = CC.evaluate(Pp, np.ones((1, NR)))
    if not (one['denE'][0] == pts[0]['denE'] and all(one['D'][a][0] == pts[0]['D'][a] for a in NAMES)):
        raise SystemExit('REFUSED: gl_fast differs from the library at the full sample (%s)' % fold)
    B = CC.evaluate(Pp, W)
    ok = np.isfinite(B['denE']) & (B['denE'] > 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        rr = {a: np.where(ok, B['D'][a] / B['denE'], np.nan) for a in NAMES}
    S = dict(RR_N=L.summ(rr['N'], pts[0]['RR']['N']), RR_CK3=L.summ(rr['CK3'], pts[0]['RR']['CK3']),
             R=L.summ(B['denE'] / L.NLEV, pts[0]['R_pp']), R_deceq=dict(point=pts[0]['R_deceq'], ci=L.pct(L.dec_eq(B['denE'], B['n']))))
    lg = lag_of(runs)
    ag = np.concatenate(ages) if ages else np.zeros(0); ag = ag[np.isfinite(ag)]
    pre = keypre(r, Lt); V = {}
    V[pre + 'R'] = fin(pts[0]['R_pp'])
    V[pre + 'as_room'] = fin(pts[1]['R_deceq']); V[pre + 'as_room.pp'] = fin(pts[1]['R_pp'])
    V[pre + 'RR_N'] = fin(S['RR_N']['point']); V[pre + 'RR_N.ci'] = [fin(S['RR_N']['ci'][0]), fin(S['RR_N']['ci'][1])]
    V[pre + 'RR_N.level'] = LEVEL; V[pre + 'RR_N.cal'] = CAL
    V[pre + 'RR_CK3'] = fin(pts[0]['RR']['CK3'])
    V[pre + 'lag'] = lg['median']
    det = dict(folder=fold, rate_hz=r, latency_s=Lt, n_runs=NR, ratio_summary=rs, intervals=S, lag=lg,
               lead_state_age_s=dict(n=int(ag.size), median=float(np.median(ag)) if ag.size else None, max=float(ag.max()) if ag.size else None,
                                     q90=float(np.percentile(ag, 90)) if ag.size else None),
               populations={pn: dict(n=fin(pts[p]['n']), denE=fin(pts[p]['denE']), R_pp=fin(pts[p]['R_pp']), R_deceq=fin(pts[p]['R_deceq']),
                                     RR={a: fin(pts[p]['RR'][a]) for a in NAMES}) for p, pn in enumerate(('all', 'after_stop'))},
               decisions_where_chain_phase_differs_from_CV0=nphase, resamples=int(W.shape[0]), resamples_without_room=int((~ok).sum()),
               seconds=time.time() - t0)
    log('%s: R %s pp, as_room %s dec-eq, RR_N %s %s, RR_CK3 %s, lag %s (%.0f s)' % (fold, V[pre + 'R'], V[pre + 'as_room'], V[pre + 'RR_N'],
                                                                                      V[pre + 'RR_N.ci'], V[pre + 'RR_CK3'], lg['median'], time.time() - t0))
    return V, det


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true'); ap.add_argument('--arrays', default=''); ap.add_argument('--nboot', type=int, default=None)
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    gate = CC.require_lock2c(a.test_old)            # stage-2 gate: LOCK_A10_2.txt AND LOCK_A10_2c.txt
    t00 = time.time()
    log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)
    outf = CC.OUT / (('TESTOLD_B7_v13%s.json' if a.test_old else 'C_B7_v13%s.json') % (('_' + a.tag) if a.tag else ''))
    if outf.exists(): raise SystemExit('REFUSED: %s exists' % outf)
    if a.test_old:
        rids = [TEST_RUN]
        arr_root = pathlib.Path(a.arrays) if a.arrays else TEST_ARR; ref_arr = lambda rid: B_CV0 / (rid + '_arrays.npz')
        nb = a.nboot or 2000
        draw = 'default_rng(%d), %d resamples of %d run(s) (test: one run, every resample is the run itself)' % (CC.SEED_BOOT, nb, len(rids))
    else:
        rids = CC.c_run_ids('lead_braking')
        if len(rids) != 105: raise SystemExit('REFUSED: %d lead-braking run ids, expected 105' % len(rids))
        arr_root = CC.ARR; ref_arr = lambda rid: CC.ARR / 'CV0' / (rid + '.npz')
        nb = a.nboot or CC.NBOOT
        draw = 'default_rng(%d), %d run resamples (optA_lib_v02.boot_counts), runs in ascending id order' % (CC.SEED_BOOT, nb)
    W = CC.counts(len(rids), nb, CC.SEED_BOOT)
    for r, Lt in B7:
        miss = [rid for rid in rids if not (arr_root / folder(r, Lt) / (rid + '.npz')).is_file()]
        if miss: raise SystemExit('REFUSED: %s: %d of %d runs have no arrays' % (folder(r, Lt), len(miss), len(rids)))
    ref = []
    for rid in rids:
        z = np.load(ref_arr(rid), allow_pickle=False)
        ref.append(dict(k=z['k'], idx55=z['idx55'], ev=z['evaluated'].astype(bool), clear1=L.clean_clear(z['clear']), phase=z['phase'].astype(int), now=z['now']))
    V = {}; DET = {}
    # ---- B7 (i) identity
    idn = [identity_run(rid, a.test_old) for rid in rids]
    V['B7.identity'] = 'pass' if all(x['pass'] for x in idn) else 'fail'
    log('B7 identity: %s (%d of %d runs pass)' % (V['B7.identity'], sum(x['pass'] for x in idn), len(idn)))
    # ---- chains
    for r, Lt in B7:
        v, d = one_chain(r, Lt, rids, ref, W, arr_root, log)
        V.update(v); DET[folder(r, Lt)] = d
    a2, a10 = V['B7.2.0.as_room'], V['B7.10.0.1.as_room']
    V['B7.ratio_10_2'] = (a10 / a2) if (a2 is not None and a10 is not None and a2 > 0) else None
    V['B7.rule_rate'] = None if None in (a2, a10) else ('consequence' if a10 < 0.5 * a2 else 'holds')
    cis = [V[keypre(r, Lt) + 'RR_N.ci'] for r, Lt in B7]
    V['B7.rule_N'] = None if any(None in c for c in cis) else ('qualified' if any(not (c[0] > -CC.DELTA and c[1] < CC.DELTA) for c in cis) else 'holds')
    # ---- the 2 Hz chain at L = 0 against the logged chain (array level)
    two = {}
    for rid, rf in zip(rids, ref):
        za = np.load(arr_root / folder(2, 0.0) / (rid + '.npz'), allow_pickle=False)
        same, dif = compare_arrays(za, np.load(ref_arr(rid), allow_pickle=False))
        two[rid] = dict(identical_to_CV0_array=same, differing=dif)
    DET_2HZ = dict(reference='CV0 array of the run (%s)' % ('package B\'s stored CV0 array' if a.test_old else 'arrays\\CV0, c_extract_v13.py'),
                   all_identical=all(x['identical_to_CV0_array'] for x in two.values()), n_runs=len(two),
                   n_identical=sum(1 for x in two.values() if x['identical_to_CV0_array']),
                   runs={k: v for k, v in two.items() if not v['identical_to_CV0_array']})
    test_extra = {}
    if a.test_old:
        # the logged arrays computed here from the logged capture files (no overlay), with the P-bar of record
        import trk_arrays_v01 as A
        PB = json.loads(PBAR_RECORD.read_text(encoding='utf-8'))['Pbar']
        for rid in rids:
            rd, cap = paths(rid, True)
            meta, arrs = A.extract(rd, cap, PB, lead=True, a4=True)
            za = np.load(arr_root / folder(2, 0.0) / (rid + '.npz'), allow_pickle=False)
            same = True; dif = {}
            for k in arrs:
                x, y = za[k], np.asarray(arrs[k])
                eq = x.shape == y.shape and np.array_equal(x, y, equal_nan=x.dtype.kind == 'f')
                if not eq:
                    same = False; dif[k] = 'differs'
            test_extra[rid] = dict(b7_2hz_L0_equals_logged_extract=same, keys_compared=len(arrs), differing=dif)
        test_extra['lag_statistics'] = {f: dict(rate_hz=d['rate_hz'], latency_s=d['latency_s'], lag=d['lag'], lead_state_age_s=d['lead_state_age_s'])
                                         for f, d in DET.items()}
        test_extra['note'] = ('One old run: every value under B7.* is a single-run pipeline exercise, not a result; A10 B7 asks for the lag '
                              'statistics only on this run (descriptive).')
    doc = dict(family='B7', program='c_b7_v13.py', test_old=a.test_old, values=V,
               details=dict(gate=gate, definitions='CD_capture/CD_DEFINITIONS_TRK_v13.md', amendment='AMENDMENT_10_v13 sec. 3 B7, 5.7',
                            status='descriptive (A10 sec. 5.7); nominal 95% percentile intervals', runs=rids, n_runs=len(rids), draw=draw,
                            identity=dict(rule='every logged online tick: B7 row with the same k, combined_hash equal, same box count, translation and '
                                               'size within %g m' % BOX_TOL, n_pass=sum(x['pass'] for x in idn), per_run=idn),
                            chains=DET, two_hz_L0_vs_logged=DET_2HZ, test_old=test_extra,
                            units=dict(as_room='decision-equivalents (key list); as_room.pp in percentage points', R='pp', shares='fractions of the room', lag='m')))
    doc['details']['seconds'] = time.time() - t00; doc['details']['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    doc['details']['code_sha256'] = {f: CC.sha(CC.HERE / f) for f in ('c_b7_v13.py', 'x_trk_extract_v13.py', 'cd_common_v13.py', 'gl_fast_v13.py')}
    CC.write_once(outf, doc)
    log('written %s; identity %s, rule_rate %s, rule_N %s, ratio_10_2 %s' % (outf.name, V['B7.identity'], V['B7.rule_rate'], V['B7.rule_N'], V['B7.ratio_10_2']))


if __name__ == '__main__':
    main()
