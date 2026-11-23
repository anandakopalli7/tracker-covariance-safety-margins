"""Revision v13, package C: B7 rate x latency on the fresh CUT-IN runs, in the cut-in event window (AMENDMENT_10_v13 sec. 3 B7 "both
families", sec. 2.5, 5.4, 5.7). Descriptive: nominal 95% percentile intervals over 20,000 run resamples of the 105 cut-in runs
(default_rng(20261911)). New file, 20 Nov 2026 (Claude Opus 5.5). Definitions: CD_capture\\CD_DEFINITIONS_TRK_v13.md sec. 8 (and 1-7).

Chains: arrays\\B7CI_<r>_<L>\\<rid>.npz from x_trk_extract_v13.py --family cutin (CV0 re-tracked on the offline detections of rate r with
latency L; F0 with the P-bar of record), (r, L) in (2, 0), (2, 0.1), (5, 0), (5, 0.1), (5, 0.2), (10, 0), (10, 0.1), (10, 0.2).
Population: evaluated decisions in the cut-in event window, from TRUTH and so the same for every chain: t_c = the first truth tick with
the primary actor ahead (along > 0) and within 1.75 m of the ego's lane centre (median lateral route coordinate of the ego); window
(k - k_c) * 0.05 s in [-1, +4] (package B's b9_cutin_v01.event_tick, as c_cutin_v13.py); runs without an event stay in the resampled
set with an empty window. 3 s commitment (as K0/K1); gridless step frontier.
  B7CI.<r>.<L>.R              R_gl (pp) in the window, on the chain's own room
  B7CI.<r>.<L>.RR_N(.ci)      RR_gl(N) in the window (+ .level 0.95, .cal "nominal95")
  B7CI.<r>.<L>.RR_CK3         RR_gl(CK3) in the window
  B7CI.<r>.<L>.as_room, .lag  "not applicable" (no lead stop in a cut-in run)
  B7CI.identity               A10 B7 (i) on the cut-in runs (as B7.identity)
Lock gate: cd_common_v13.require_lock2c (LOCK_A10_2.txt AND LOCK_A10_2c.txt), except --test-old: the 20 OLD cut-in tuning runs (no
sweeps were kept), chain (2, 0) built by x_trk_extract_v13.py --family cutin --test-old from the LOGGED detection rows; the program checks
its window, R and RR_N against out\\TESTOLD_C_CUTIN_K0_K2_v13.json (same draw size), its arrays against the stored arrays of record
(gateR_rt_v01) and, for the first run, against an extract of the logged files -> out\\TESTOLD_B7_v13_ci[_<tag>].json.
Fresh output: out\\C_B7CI_v13.json. Never overwrites.
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\c_b7ci_v13.py [--test-old [--arrays DIR]] [--nboot N] [--tag S]
"""
import argparse, json, math, os, pathlib, sys, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('NUMBA_NUM_THREADS', '2')
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cd_common_v13 as CC               # noqa: E402
import trk_env_v01 as env                # noqa: E402
env.setup()
import numpy as np                       # noqa: E402
import trk_score_v01 as TS               # noqa: E402
import trk_arrays_v01 as TA              # noqa: E402
import c_b7_v13 as B7M                   # noqa: E402  (helpers of the lead-braking B7 program: identity_run, compare_arrays, fin, lstr)
import x_trk_extract_v13 as XT           # noqa: E402  (old cut-in tuning run list and paths)
L = CC.L

B7 = B7M.B7
NAMES = ['N', 'CK3']
LAT = 1.75; WIN = (-1.0, 4.0); DT = 0.05
STORED = XT.P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
TEST_ARR = CC.OUT / 'testold_b7ci_arrays'
NA = 'not applicable'


def folder(r, Lt):
    return 'B7CI_%d_%s' % (r, B7M.lstr(Lt))


def keypre(r, Lt):
    return 'B7CI.%d.%s.' % (r, B7M.lstr(Lt))


def event_tick(T):
    """b9_cutin_v01.event_tick (same lines; also c_cutin_v13.event_tick)."""
    ks = sorted(T); kc = None
    lat_e = np.array([-math.sin(T[k]['ego'][2]) * T[k]['ego'][0] + math.cos(T[k]['ego'][2]) * T[k]['ego'][1] for k in ks])
    lane = float(np.median(lat_e))
    for k in ks:
        tr = T[k]; tid = tr['target_id']
        ex, ey, yaw = tr['ego']
        if tid is None or tid not in tr['actors']: continue
        a = tr['actors'][tid]
        along = math.cos(yaw) * (a[0] - ex) + math.sin(yaw) * (a[1] - ey)
        across = -math.sin(yaw) * a[0] + math.cos(yaw) * a[1] - lane
        if along > 0 and abs(across) <= LAT:
            kc = k; break
    return kc


def window_of(rd, cap, k_ref, ev):
    T = TA.load_capture(rd, cap)['T']
    kc = event_tick(T)
    ks = np.array([k for k, _ in TA.gc.decisions(cap)])
    if not np.array_equal(ks, k_ref):
        raise SystemExit('REFUSED: decision ticks of %s differ from the reference array' % cap)
    rel = (ks - kc) * DT if kc is not None else np.full(ks.size, np.nan)
    win = ev & np.isfinite(rel) & (rel >= WIN[0]) & (rel <= WIN[1])
    return kc, win


def one_chain(r, Lt, rids, ref, W, arr_root, log):
    t0 = time.time(); fold = folder(r, Lt)
    runs = []; nphase = 0
    for rid, rf in zip(rids, ref):
        z = np.load(arr_root / fold / (rid + '.npz'), allow_pickle=False)
        for key in ('k', 'idx55'):
            if not np.array_equal(z[key], rf[key]):
                raise SystemExit('REFUSED: %s %s: %s differs from the reference array' % (fold, rid, key))
        ev = z['evaluated'].astype(bool); clear1 = L.clean_clear(z['clear'])
        if not np.array_equal(ev, rf['ev']) or not np.array_equal(clear1, rf['clear1']):
            raise SystemExit('REFUSED: %s %s: evaluated / clearance differ from the reference array' % (fold, rid))
        runs.append(dict(run=rid, desired=float(z['des'][0]), idx55=z['idx55'].astype(np.int64), clear1=clear1, vbar=z['vbar'], ev=ev,
                         masks=(rf['win'], ev), crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float),
                                                       'N': np.asarray(z['cN'], float), 'CK3': np.asarray(z['cCK3'], float)}, sel={}, late={}))
    NR = len(runs)
    rat = []
    for rr in runs:
        m = rr['masks'][0]; cN = rr['crit']['N'][m]; cF = rr['crit']['F0'][m]
        ok = np.isfinite(cN) & np.isfinite(cF) & (cN > 0) & (cF > 0); rat.append(np.sqrt(cF[ok] / cN[ok]))
    rs = TS.ratio_summary(np.concatenate(rat) if rat else np.zeros(0))
    G = TS.gridless(runs, ['F0', 'E'] + NAMES)
    with np.errstate(divide='ignore', invalid='ignore'):
        pts = [TS.rr_gl(G, 'F0', 'E', NAMES, pop=p) for p in (0, 1)]
    Pp = CC.prep(G, ['F0', 'E'] + NAMES, 0)
    one = CC.evaluate(Pp, np.ones((1, NR)))
    if not (one['denE'][0] == pts[0]['denE'] and all((one['D'][a][0] == pts[0]['D'][a]) or (np.isnan(one['D'][a][0]) and np.isnan(pts[0]['D'][a]))
                                                      for a in NAMES)):
        raise SystemExit('REFUSED: gl_fast differs from the library at the full sample (%s)' % fold)
    B = CC.evaluate(Pp, W)
    ok = np.isfinite(B['denE']) & (B['denE'] > 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        rr = {a: np.where(ok, B['D'][a] / B['denE'], np.nan) for a in NAMES}
    S = dict(RR_N=L.summ(rr['N'], pts[0]['RR']['N']), RR_CK3=L.summ(rr['CK3'], pts[0]['RR']['CK3']),
             R=L.summ(B['denE'] / L.NLEV, pts[0]['R_pp']), R_deceq=dict(point=pts[0]['R_deceq'], ci=L.pct(L.dec_eq(B['denE'], B['n']))))
    pre = keypre(r, Lt); fin = B7M.fin; V = {}
    V[pre + 'R'] = fin(pts[0]['R_pp'])
    V[pre + 'RR_N'] = fin(S['RR_N']['point']); V[pre + 'RR_N.ci'] = [fin(S['RR_N']['ci'][0]), fin(S['RR_N']['ci'][1])]
    V[pre + 'RR_N.level'] = B7M.LEVEL; V[pre + 'RR_N.cal'] = B7M.CAL
    V[pre + 'RR_CK3'] = fin(pts[0]['RR']['CK3'])
    V[pre + 'as_room'] = NA; V[pre + 'lag'] = NA
    det = dict(folder=fold, rate_hz=r, latency_s=Lt, n_runs=NR, ratio_summary_window=rs, intervals=S,
               populations={pn: dict(n=fin(pts[p]['n']), denE=fin(pts[p]['denE']), R_pp=fin(pts[p]['R_pp']), R_deceq=fin(pts[p]['R_deceq']),
                                     RR={a: fin(pts[p]['RR'][a]) for a in NAMES}) for p, pn in enumerate(('window', 'all_evaluated'))},
               resamples=int(W.shape[0]), resamples_without_room=int((~ok).sum()), seconds=time.time() - t0)
    log('%s: R %s pp, RR_N %s %s, RR_CK3 %s, n window %s (%.0f s)' % (fold, V[pre + 'R'], V[pre + 'RR_N'], V[pre + 'RR_N.ci'], V[pre + 'RR_CK3'],
                                                                    det['populations']['window']['n'], time.time() - t0))
    return V, det, S, pts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true'); ap.add_argument('--arrays', default=''); ap.add_argument('--nboot', type=int, default=None)
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    gate = CC.require_lock2c(a.test_old)            # stage-2 gate: LOCK_A10_2.txt AND LOCK_A10_2c.txt
    t00 = time.time()
    log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)
    outf = CC.OUT / (('TESTOLD_B7_v13_ci%s.json' if a.test_old else 'C_B7CI_v13%s.json') % (('_' + a.tag) if a.tag else ''))
    if outf.exists(): raise SystemExit('REFUSED: %s exists' % outf)
    if a.test_old:
        old = XT.old_cutin_tuning(); rids = sorted(old)
        paths = lambda rid: old[rid]
        ref_arr = lambda rid: STORED / (rid + '.npz')                       # the stored arrays of record (as c_cutin_v13.py --test-old)
        arr_root = pathlib.Path(a.arrays) if a.arrays else TEST_ARR
        combos = [(2, 0.0)]
        rec = json.loads((CC.OUT / 'TESTOLD_C_CUTIN_K0_K2_v13.json').read_text(encoding='utf-8'))
        nb = a.nboot or int(rec['draw'].split(',')[1].split()[0])            # the record's resample count (200)
        draw = 'default_rng(%d), %d resamples of the 20 cut-in tuning runs (as TESTOLD_C_CUTIN_K0_K2_v13.json)' % (CC.SEED_BOOT, nb)
    else:
        rids = CC.c_run_ids('cutin')
        if len(rids) != 105: raise SystemExit('REFUSED: %d cut-in run ids, expected 105' % len(rids))
        def paths(rid):
            if not (CC.CD / 'runs' / rid / 'LOGS_OK').is_file(): raise SystemExit('REFUSED: %s has no LOGS_OK' % rid)
            rd = CC.CD / 'runs' / rid / rid; caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
            assert len(caps) == 1, rid
            return rd, caps[0]
        ref_arr = lambda rid: CC.ARR / 'CV0' / (rid + '.npz')
        arr_root = CC.ARR; combos = B7
        nb = a.nboot or CC.NBOOT
        draw = 'default_rng(%d), %d run resamples of the 105 cut-in runs (optA_lib_v02.boot_counts), ascending id order' % (CC.SEED_BOOT, nb)
    W = CC.counts(len(rids), nb, CC.SEED_BOOT)
    for r, Lt in combos:
        miss = [rid for rid in rids if not (arr_root / folder(r, Lt) / (rid + '.npz')).is_file()]
        if miss: raise SystemExit('REFUSED: %s: %d of %d runs have no arrays' % (folder(r, Lt), len(miss), len(rids)))
    # ---- reference arrays and the event window (truth; once per run)
    ref = []; facts = []
    for rid in rids:
        z = np.load(ref_arr(rid), allow_pickle=False)
        if not a.test_old: assert json.loads(str(z['meta']))['family'] == 'cutin', rid
        ev = z['evaluated'].astype(bool)
        rd, cap = paths(rid)
        kc, win = window_of(rd, cap, z['k'], ev)
        ref.append(dict(k=z['k'], idx55=z['idx55'], ev=ev, clear1=L.clean_clear(z['clear']), win=win))
        facts.append(dict(run=rid, event_tick=kc, n_eval=int(ev.sum()), n_window=int(win.sum())))
    log('runs %d; events %d; window decisions %d' % (len(rids), sum(f['event_tick'] is not None for f in facts), sum(f['n_window'] for f in facts)))
    V = {}; DET = {}; SS = {}
    if a.test_old:
        V['B7CI.identity'] = None; idn = 'not run: no old cut-in run has B7 detection rows'
    else:
        idr = [B7M.identity_run(rid, False) for rid in rids]
        V['B7CI.identity'] = 'pass' if all(x['pass'] for x in idr) else 'fail'
        idn = dict(rule='as B7.identity (CD_DEFINITIONS_TRK_v13.md sec. 5)', n_pass=sum(x['pass'] for x in idr), per_run=idr)
        log('B7 identity (cut-in): %s' % V['B7CI.identity'])
    for r, Lt in combos:
        v, d, S, pts = one_chain(r, Lt, rids, ref, W, arr_root, log)
        V.update(v); DET[folder(r, Lt)] = d; SS[folder(r, Lt)] = (S, pts)
    # ---- the 2 Hz chain at L = 0 against the reference arrays (array level)
    two = {}
    for rid in rids:
        za = np.load(arr_root / folder(2, 0.0) / (rid + '.npz'), allow_pickle=False); zr = np.load(ref_arr(rid), allow_pickle=False)
        keys = sorted((set(za.files) & set(zr.files)) - {'meta'}) if a.test_old else None   # test: the keys the stored arrays hold
        same, dif = B7M.compare_arrays(za, zr, keys=keys)
        two[rid] = dict(identical=same, differing=dif, keys_compared=len(keys) if keys else len(set(za.files) - {'meta'}))
    doc_two = dict(reference=('stored arrays of record (gateR_rt_v01; the keys they hold)' if a.test_old else 'arrays\\CV0 (c_extract_v13.py)'),
                   n_identical=sum(1 for x in two.values() if x['identical']), n_runs=len(two),
                   keys_compared=sorted({x['keys_compared'] for x in two.values()}),
                   differing={k: v['differing'] for k, v in two.items() if not v['identical']})
    test = {}
    if a.test_old:
        # (1) the extractor's cut-in path at 2 Hz / L = 0 with logged rows vs an extract of the logged files (first run)
        PB = json.loads(XT.PBAR_RECORD.read_text(encoding='utf-8'))['Pbar']
        rid0 = rids[0]; rd, cap = paths(rid0)
        meta, arrs = TA.extract(rd, cap, PB, lead=True, a4=True)
        za = np.load(arr_root / folder(2, 0.0) / (rid0 + '.npz'), allow_pickle=False)
        dif = [k for k in arrs if not (za[k].shape == np.asarray(arrs[k]).shape and np.array_equal(za[k], np.asarray(arrs[k]), equal_nan=za[k].dtype.kind == 'f'))]
        test['b7ci_2_0_vs_logged_extract'] = dict(run=rid0, keys_compared=len(arrs), identical=not dif, differing=dif)
        # (2) window and values against TESTOLD_C_CUTIN_K0_K2_v13.json
        S, pts = SS[folder(2, 0.0)]
        comp = []
        def add(name, ours, theirs):
            eq = (ours == theirs) or (isinstance(ours, float) and isinstance(theirs, float) and math.isnan(ours) and math.isnan(theirs))
            if isinstance(theirs, list):
                eq = len(ours) == len(theirs) and all((x == y) or (isinstance(x, float) and isinstance(y, float) and math.isnan(x) and math.isnan(y))
                                                      for x, y in zip(ours, theirs))
            comp.append(dict(item=name, ours=ours, record=theirs, equal=bool(eq)))
        recf = {f['run']: f for f in rec['runs']}
        for f in facts:
            add('event_tick %s' % f['run'], f['event_tick'], recf[f['run']]['event_tick'])
            add('n_window %s' % f['run'], f['n_window'], recf[f['run']]['n_window'])
        add('K0 R_gl point', float(S['R']['point']), rec['K0']['R_gl']['point'])
        add('K0 R_gl ci (nominal 95%)', [float(x) for x in S['R']['ci']], rec['K0']['R_gl']['ci'])
        add('K1 RR_N point', float(S['RR_N']['point']), rec['K1']['RR_N']['point'])
        add('K1 RR_N ci (nominal 95%)', [float(x) for x in S['RR_N']['ci']], rec['K1']['RR_N']['ci'])
        add('K1 RR_N invalid share', float(S['RR_N']['invalid_share']), rec['K1']['RR_N']['invalid_share'])
        dw = rec['descriptive']['window']; da = rec['descriptive']['all_evaluated']
        add('window n', float(pts[0]['n']), dw['n']); add('window R_deceq point', float(pts[0]['R_deceq']), dw['R_deceq']['point'])
        add('all_evaluated n', float(pts[1]['n']), da['n']); add('all_evaluated R_pp point', float(pts[1]['R_pp']), da['R_pp']['point'])
        add('all_evaluated RR_N point', float(pts[1]['RR']['N']), da['RR_N']['point'])
        test['vs_TESTOLD_C_CUTIN_K0_K2'] = dict(n_items=len(comp), n_equal=sum(c['equal'] for c in comp), all_equal=all(c['equal'] for c in comp),
                                                differing=[c for c in comp if not c['equal']], items=comp)
        test['note'] = ('The 20 cut-in tuning runs have no room at all (R = 0 in the window and over all evaluated decisions), so RR is '
                        'undefined there; the equality of R, the window sizes and event ticks, and the array identities carry the test.')
        log('test: logged-extract identity %s; %d of %d items equal TESTOLD_C_CUTIN' % (test['b7ci_2_0_vs_logged_extract']['identical'],
                                                                                   test['vs_TESTOLD_C_CUTIN_K0_K2']['n_equal'], len(comp)))
    doc = dict(family='B7CI', program='c_b7ci_v13.py', test_old=a.test_old, values=V,
               details=dict(gate=gate, definitions='CD_capture/CD_DEFINITIONS_TRK_v13.md sec. 8', amendment='AMENDMENT_10_v13 sec. 3 B7, 2.5, 5.4, 5.7',
                            status='descriptive (A10 sec. 5.7); nominal 95% percentile intervals', runs=facts, n_runs=len(rids), draw=draw,
                            lat_m=LAT, window_s=WIN, runs_without_event=[f['run'] for f in facts if f['event_tick'] is None],
                            identity=idn, chains=DET, two_hz_L0_vs_reference=doc_two, test_old=test,
                            units=dict(R='pp', shares='fractions of the room', as_room=NA, lag=NA)))
    doc['details']['seconds'] = time.time() - t00; doc['details']['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    doc['details']['code_sha256'] = {f: CC.sha(CC.HERE / f) for f in ('c_b7ci_v13.py', 'c_b7_v13.py', 'x_trk_extract_v13.py', 'cd_common_v13.py', 'gl_fast_v13.py')}
    CC.write_once(outf, doc)
    log('written %s' % outf.name)


if __name__ == '__main__':
    main()
