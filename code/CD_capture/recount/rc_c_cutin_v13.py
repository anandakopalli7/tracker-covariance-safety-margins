"""Recount (second program) of package C, cut-in: K0-K2 of AMENDMENT_10_v13 section 5.4. New file, 19 Nov 2026
(Claude Fable 5.2). Written from A10 (sections 0, 2.5, 2.6, 5.4, 5.8, 10.1) and CD_DEFINITIONS_v13.md; no first program was read.

Per cut-in run, from the truth and the capture logs:
  event tick k_c   the first truth tick at which the scenario's primary actor (the truth record's target) is ahead of the ego
                   (centre distance along the route > 0) and its lateral route coordinate lies within 1.75 m of the lane centre
                   (the median over the run of the ego's lateral route coordinate); runs without an event are listed;
  event window     evaluated decisions with -20 <= k - k_c <= 80 ticks (t - t_c in [-1, +4] s at 0.05 s per tick);
  track age        decision time 'now' minus the detector time of the first detector frame whose output holds the track matched
                   to the primary actor (ol_gateR_core_v01.match_many: nearest true actor within 4 m; several tracks -> the
                   youngest); strata < 1 s, 1-4 s, >= 4 s, untracked.
Statistics (gridless step frontier, 3 s commitment):
  K0  R_gl in the event window (lower end > 0) and den0 = D_gl(O, F0) in decision-equivalents (>= 10);
  K1  RR_gl(N) in the event window against (-delta, delta);
  K2  young-track population: r = RR_gl(N), c = RR_gl(E5_N) (m_N, A_N from that population's margin ratios; u over all
      evaluated decisions of the cut-in runs), classified as H3; not evaluable if R_gl there is below 10 decision-equivalents;
  the A10 section 2.6 calibrated levels; the fixed sequence; RR_gl(N), room, den0 and the ratio spread per track-age stratum and
  per second relative to t_c.

Usage (python -I -B -X utf8):
  rc_c_cutin_v13.py --test-old [--boot 200 --outer 10 --inner 50 --mc 200 --workers 2]     the 20 cut-in tuning runs of record
  rc_c_cutin_v13.py --stage truth                                                           event ticks and track ages only
  rc_c_cutin_v13.py [--truth-file out\\RC_C_CUTIN_TRUTH_v13.json] [--workers N]              fresh runs; refuses before Lock 2
  ... --calib export                    everything except the double bootstrap; writes the job out\\calib\\rc_cutin.job.npz
                                        (+ .meta.json, .state.npz) and a pending output <name>.PENDING.json
  ... --calib import --calib-chunks DIR reads the chunks rc_cutin_<SEED>_o<LO>_<HI>.npz that rc_calib_remote_v13.py computed,
                                        checks them and finishes the run (output as an in-process run)
Output: out\\RC_C_CUTIN_v13<tag>.json (never overwritten).
"""
import argparse, json, math, pathlib, sys, time
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))      # python -I: the script folder is not on sys.path
import rc_core_v13 as K

L = K.L
LAT_M = 1.75
WIN = (-20, 80)                      # ticks: [-1, +4] s
POPS = ['all', 'window', 'young', 'age_1_4', 'age_ge4', 'untracked', 'sec_-1_0', 'sec_0_1', 'sec_1_2', 'sec_2_3', 'sec_3_4']
SEC_BINS = [(-20, 0), (0, 20), (20, 40), (40, 60), (60, 81)]      # [-1,0) [0,1) [1,2) [2,3) [3,4] (closed)


def truth_of_run(r):
    """Event tick, lane centre and per-decision track age of one run (truth through package B's trk_arrays_v01.load_capture)."""
    if str(K.SHARED) not in sys.path:
        sys.path.insert(0, str(K.SHARED))
    import trk_arrays_v01 as TA
    Lr = TA.load_capture(r['rd'], r['cap'])
    T = Lr['T']; book = Lr['book']
    ks = sorted(T)
    lat = []
    for k in ks:
        x, y, psi = T[k]['ego']
        lat.append(-math.sin(psi) * x + math.cos(psi) * y)
    lane = float(np.median(lat))
    k_c = None
    for k in ks:
        tr = T[k]; prim = tr['target_id']
        if prim is None or prim not in tr['actors']:
            continue
        x, y, psi = tr['ego']; ta = tr['actors'][prim]
        along = math.cos(psi) * (ta[0] - x) + math.sin(psi) * (ta[1] - y)
        across = -math.sin(psi) * ta[0] + math.cos(psi) * ta[1]
        if along > 0 and abs(across - lane) <= LAT_M:
            k_c = int(k); break
    decs = list(TA.gc.decisions(Lr['cap']))
    kd = np.array([k for k, _ in decs], dtype=np.int64)
    if not np.array_equal(kd, np.asarray(r['k'])):
        raise SystemExit('REFUSED: the decisions of %s in frames.jsonl do not match its arrays' % r['run'])
    age = np.full(len(decs), np.nan); now = np.full(len(decs), np.nan); n_nobirth = 0
    for di, (k, dec) in enumerate(decs):
        now[di] = dec['now']
        tr = T.get(k)
        m, prim, order = TA.gc.match_many(dec['actors'], dec['now'], tr)
        if prim is None:
            continue
        best = None
        for oi, aid in enumerate(m):
            if aid is not None and aid == prim:
                tid = int(dec['actors'][oi]['track_id'])
                kb = book.birth.get(tid)
                if kb is None:
                    n_nobirth += 1                 # no birth record: the track is skipped (CD_DEFINITIONS 'Cut-in details')
                    continue
                ag = float(dec['now'] - book.det_time[kb])
                if best is None or ag < best:
                    best = ag
        if best is not None:
            age[di] = best
    return dict(run=r['run'], event_tick=k_c, lane_centre_m=lane, ego_lateral_spread_m=float(max(lat) - min(lat)),
                k=kd.tolist(), now=now.tolist(), age=[None if np.isnan(x) else float(x) for x in age],
                n_matched_tracks_without_birth=n_nobirth)


def masks_of(r, tr):
    """The 11 populations of POPS for one run."""
    ev = r['ev']; n = ev.size
    k = np.asarray(r['k']).astype(np.int64)
    age = np.array([np.nan if x is None else x for x in tr['age']], float)
    if tr['event_tick'] is None:
        win = np.zeros(n, bool); dk = np.zeros(n, np.int64)
    else:
        dk = k - int(tr['event_tick'])
        win = ev & (dk >= WIN[0]) & (dk <= WIN[1])
    tracked = np.isfinite(age)
    with np.errstate(invalid='ignore'):
        out = [ev, win, win & tracked & (age < 1.), win & tracked & (age >= 1.) & (age < 4.), win & tracked & (age >= 4.), win & ~tracked]
    for lo, hi in SEC_BINS:
        out.append(win & (dk >= lo) & (dk < hi))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--stage', default='all', choices=['all', 'truth'])
    ap.add_argument('--truth-file', default=None)
    ap.add_argument('--boot', type=int, default=K.NBOOT)
    ap.add_argument('--outer', type=int, default=K.B_OUTER)
    ap.add_argument('--inner', type=int, default=K.B_INNER)
    ap.add_argument('--mc', type=int, default=K.B_MC)
    ap.add_argument('--workers', type=int, default=0)
    ap.add_argument('--second-seed', default='auto', choices=['auto', 'always', 'never'])
    ap.add_argument('--no-calibration', action='store_true')
    ap.add_argument('--no-library', action='store_true')
    ap.add_argument('--tag', default='')
    ap.add_argument('--calib', default='inproc', choices=['inproc', 'export', 'import'])
    ap.add_argument('--calib-chunks', default=None)
    ap.add_argument('--calib-label', default='rc_cutin')
    a = ap.parse_args()
    if a.calib != 'inproc' and (a.no_calibration or a.stage != 'all'):
        raise SystemExit('REFUSED: --calib export / import needs the calibration and --stage all')
    if (a.calib == 'import') != (a.calib_chunks is not None):
        raise SystemExit('REFUSED: --calib-chunks DIR goes with --calib import, and only with it')
    K.check_label(a.calib_label)
    cdir = K.calib_dir(a.test_old)
    t00 = time.time()
    nthreads = K.set_workers(a.workers)
    full_size = (a.boot == K.NBOOT and a.outer == K.B_OUTER and a.inner == K.B_INNER and a.mc == K.B_MC)
    pre = 'RC_C_CUTIN_TESTOLD' if a.test_old else 'RC_C_CUTIN'
    if a.stage == 'truth':
        name = '%s_TRUTH_v13%s.json' % (pre, a.tag)
    elif a.test_old:
        name = '%s_b%d_o%d_i%d%s.json' % (pre, a.boot, a.outer, a.inner, a.tag)
    else:
        name = '%s_v13%s%s.json' % (pre, '' if full_size else '_b%d_o%d_i%d' % (a.boot, a.outer, a.inner), a.tag)
    if K.DRYRUN:
        name = 'DRYRUN_' + name
    outf = K.OUT / name
    if a.calib == 'export':
        outf = K.OUT / (name[:-5] + '.PENDING.json')
    if outf.exists():
        raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % outf)

    # ---------------- run set
    if a.test_old:
        runs = K.load_old_cutin_runs()
    else:
        K.require_lock2('fresh cut-in arrays and truth')
        runs = K.load_fresh_runs('cutin', 'CV0')
        for r in runs:
            rd = K.check_path(K.RUNS_DIR / r['run'] / r['run'])
            caps = [d for d in (rd / 'capture').iterdir() if d.is_dir()] if a.truth_file is None else [None]
            if len(caps) != 1:
                raise SystemExit('REFUSED: expected one capture folder in %s' % (rd / 'capture'))
            r['rd'] = rd; r['cap'] = caps[0]
    n = len(runs)
    doc = dict(code='rc_c_cutin_v13.py', role='second program (recount), AMENDMENT_10_v13 section 10.1(b)', model='claude-fable-5-2',
               mode='test-old' if a.test_old else 'fresh', started=K.clock(), calib_mode=a.calib,
               dryrun=('OLD runs relabelled as fresh in a scratch tree; NOT fresh data' if K.DRYRUN else False), threads=nthreads, lat_m=LAT_M, window_ticks=list(WIN),
               sizes=dict(boot=a.boot, outer=a.outer, inner=a.inner, mc=a.mc), delta=K.DELTA, populations=POPS,
               seeds=dict(boot=K.SEED_BOOT, outer=K.SEED_OUTER, inner=K.SEED_INNER, inner2=K.SEED_INNER2, mc=K.SEED_MC),
               runs=[r['run'] for r in runs])

    # ---------------- truth: event tick and track age
    if a.truth_file is not None:
        tdoc = json.loads(pathlib.Path(a.truth_file).read_text(encoding='utf-8'))
        if tdoc.get('mode') != doc['mode'] or [t['run'] for t in tdoc['truth']] != doc['runs']:
            raise SystemExit('REFUSED: the truth file does not describe this run set')
        truth = tdoc['truth']
        for r, t in zip(runs, truth):
            if not np.array_equal(np.asarray(t['k']), np.asarray(r['k'])):
                raise SystemExit('REFUSED: the truth file decisions of %s do not match its arrays' % r['run'])
        doc['truth_source'] = str(a.truth_file)
    else:
        truth = []
        for r in runs:
            truth.append(truth_of_run(r))
        doc['truth_source'] = 'computed here (trk_arrays_v01.load_capture, ol_gateR_core_v01.match_many / Book)'
    print('truth done (%.0f s): events in %d of %d runs' % (time.time() - t00, sum(t['event_tick'] is not None for t in truth), n),
          flush=True)
    if a.stage == 'truth':
        doc['truth'] = truth; doc['written'] = K.clock(); doc['seconds'] = time.time() - t00
        print('written %s' % K.write_new(outf, doc)); return

    M = [masks_of(r, t) for r, t in zip(runs, truth)]
    per_run = []
    for r, t, m in zip(runs, truth, M):
        per_run.append(dict(run=r['run'], event_tick=t['event_tick'], lane_centre_m=t['lane_centre_m'],
                            ego_lateral_spread_m=t['ego_lateral_spread_m'], n_decisions=int(r['ev'].size), n_evaluated=int(r['ev'].sum()),
                            n_matched_tracks_without_birth=t['n_matched_tracks_without_birth'],
                            counts={p: int(m[pi].sum()) for pi, p in enumerate(POPS)}))
    doc['per_run'] = per_run
    doc['events'] = dict(found=int(sum(t['event_tick'] is not None for t in truth)), of=n,
                         runs_without_event=[t['run'] for t in truth if t['event_tick'] is None])
    doc['counts'] = {p: int(sum(m[pi].sum() for m in M)) for pi, p in enumerate(POPS)}
    doc['counts']['runs_with_young_decisions'] = int(sum(bool(m[2].any()) for m in M))
    print('counts: %s' % doc['counts'], flush=True)

    # ---------------- E5_N of the young-track population (K2)
    u, uinfo = K.e5_u(runs, 'F0', 'E')
    ratios = {p: np.concatenate([K.margin_ratio_values(r, 'N', 'F0', m[pi]) for r, m in zip(runs, M)]) for pi, p in enumerate(POPS)}
    doc['margin_ratio'] = {p: K.ratio_summary(ratios[p]) for p in POPS}
    rsy = doc['margin_ratio']['young']
    have_e5n = bool(rsy['n'] > 0 and np.isfinite(rsy['median']) and np.isfinite(rsy['A']))
    if have_e5n:
        for r, uu in zip(runs, u):
            r['crit']['E5N'] = K.oracle_crit(r['crit']['F0'], rsy['median'], rsy['A'], uu)
    doc['E5_N'] = dict(uinfo, m_N=rsy['median'], A_N=rsy['A'], defined=have_e5n, barely_varies=rsy['barely_varies'])

    # ---------------- curves and problems
    preps = [K.Prep(r) for r in runs]
    mfn = lambda k: M[k]                                       # noqa: E731
    names = ['F0', 'E', 'N', 'O'] + (['E5N'] if have_e5n else [])
    cur = {nm: K.build_curves(runs, preps, nm, mfn, oracle=(nm == 'O')) for nm in names}
    PB = {}
    for pi, p in enumerate(POPS):
        nmp = names if p == 'young' else ['F0', 'E', 'N', 'O']
        PB[p] = K.Problem(nmp, [cur[x][pi] for x in nmp])
    doc['gridless_sizes'] = {p: {nm: cur[nm][pi].npts for nm in names} for pi, p in enumerate(POPS)}
    print('curves built (%.0f s)' % (time.time() - t00), flush=True)

    def pop_eval(p, CN):
        e = PB[p].evaluate(CN)
        den = e['denE']; nn = e['n']
        o = dict(n=nn, denE=den, R_pp=den / K.NLEV, R_deceq=den / K.NLEV / 100. * nn, RR_N=K.ratio_arr(e['D']['N'], den),
                 D_N_deceq=e['D']['N'] / K.NLEV / 100. * nn, den0_deceq=e['D']['O'] / K.NLEV / 100. * nn, D_O=e['D']['O'], D_N=e['D']['N'])
        if 'E5N' in e['D']:
            c = K.ratio_arr(e['D']['E5N'], den)
            o['c'] = c; o['D_E5N'] = e['D']['E5N']
            with np.errstate(divide='ignore', invalid='ignore'):
                o['r_over_c'] = np.where(np.isfinite(c) & (c != 0), o['RR_N'] / c, np.nan)
        return o

    STATS = ['W_R_gl_pp', 'W_RR_N', 'Y_R_gl_pp', 'Y_r', 'Y_c', 'Y_r_over_c']

    # the statistics of a batch of run counts (rc_kern_v13.CutinStat: the window and the young-track population)
    stat_fn = K.KN.CutinStat(PB['window'], PB['young'], STATS)

    # ---------------- points (kernel) and the library of record
    one = np.ones((1, n))
    PT = {p: {k: float(v[0]) for k, v in pop_eval(p, one).items()} for p in POPS}
    full = stat_fn(one)[0]
    doc['point'] = dict(populations=PT, stats={s: float(v) for s, v in zip(STATS, full)})
    A9 = None if a.no_library else K.try_a9()
    if A9 is not None:
        for k, r in enumerate(runs):
            r['_masks'] = tuple(M[k])
        G = A9.gridless_sources(runs, names, lambda r: r['clear1'] > 0., masks_key='_masks')
        lib = {}; ident = True
        for pi, p in enumerate(POPS):
            nmp = names if p == 'young' else ['F0', 'E', 'N', 'O']
            T = {nm: G[nm].curve(None, pops=[pi])[:, 0, :] for nm in nmp}
            el = L.eval_scoring(T, nmp[1:])
            lib[p] = dict(denE=el['denE'], n=el['n'], D=el['D'], RR_N=L.ratio(el['D']['N'], el['denE']),
                          R_deceq=L.dec_eq(el['denE'], el['n']), den0_deceq=L.dec_eq(el['D']['O'], el['n']))

            def same(x, y):
                return bool(x == y or (np.isnan(x) and np.isnan(y)))
            okp = same(el['denE'], PT[p]['denE']) and same(el['n'], PT[p]['n']) and same(el['D']['N'], PT[p]['D_N']) \
                and same(el['D']['O'], PT[p]['D_O']) and ('E5N' not in el['D'] or same(el['D']['E5N'], PT[p]['D_E5N']))
            lib[p]['identical_to_recount_kernel'] = bool(okp); ident = ident and okp
        doc['point']['library_of_record'] = dict(populations=lib, all_identical=bool(ident))
        for r in runs:
            r.pop('_masks', None)
        print('library of record vs kernel (full sample, %d populations): identical = %s' % (len(POPS), ident), flush=True)

    # ---------------- main bootstrap (all populations)
    t1 = time.time()
    st = K.calib_state(cdir, a.calib_label, full, a.boot) if a.calib == 'import' else None
    if st is not None:
        # the main bootstrap of the export run (the same arrays; it is not computed twice)
        BO = {p: {} for p in POPS}
        for key in st:
            if key.startswith('BO|'):
                _, p, kx = key.split('|')
                BO[p][kx] = st[key]
        print('main bootstrap: taken from the export run (%s.state.npz)' % a.calib_label, flush=True)
    else:
        CNT = K.boot_counts(n, K.NBOOT, K.SEED_BOOT)[:a.boot]
        BO = {p: pop_eval(p, CNT) for p in POPS}
    BS = np.full((a.boot, len(STATS)), np.nan)
    BS[:, 0] = BO['window']['R_pp']; BS[:, 1] = BO['window']['RR_N']; BS[:, 2] = BO['young']['R_pp']; BS[:, 3] = BO['young']['RR_N']
    if 'c' in BO['young']:
        BS[:, 4] = BO['young']['c']; BS[:, 5] = BO['young']['r_over_c']
    doc['bootstrap'] = dict(n_resamples=int(a.boot), seconds=time.time() - t1,
                            share_den_gt0={p: float(np.mean(BO[p]['denE'] > 0)) for p in POPS})
    print('main bootstrap done: %d resamples in %.0f s' % (a.boot, time.time() - t1), flush=True)
    doc['descriptive'] = {p: dict(n=PT[p]['n'], R_gl_pp=K.summ(BO[p]['R_pp'], PT[p]['R_pp']), R_gl_deceq=K.summ(BO[p]['R_deceq'], PT[p]['R_deceq']),
                                  RR_gl_N=K.summ(BO[p]['RR_N'], PT[p]['RR_N']), den0_deceq=K.summ(BO[p]['den0_deceq'], PT[p]['den0_deceq']),
                                  D_N_deceq=PT[p]['D_N_deceq'], margin_ratio=doc['margin_ratio'][p]) for p in POPS}

    # ---------------- calibration (A10 2.6)
    cal = {}
    if not a.no_calibration:
        base = name[:-5]
        if a.calib == 'export':
            state = dict(n_boot=np.int64(a.boot))
            state.update({'BO|%s|%s' % (p, kx): BO[p][kx] for p in POPS for kx in BO[p]})
            info = K.calib_export(stat_fn, full, n, a.outer, a.inner, a.calib_label, cdir, doc['mode'], doc['code'], state)
            doc['PENDING'] = ('PENDING: the double bootstrap (A10 section 2.6) has not run. No calibrated level, interval or '
                              'hypothesis is in this file. Finish with --calib import --calib-chunks DIR.')
            doc['calibration'] = dict(status='pending', job=info)
            doc['written'] = K.clock(); doc['seconds'] = time.time() - t00
            print('job written: %s (SHA-256 %s)' % (info['job'], info['job_sha256']), flush=True)
            print('written %s (PENDING; %.0f s)' % (K.write_new(outf, doc), time.time() - t00))
            return
        if a.calib == 'import':
            imp = K.CalibImport(stat_fn, full, n, a.outer, a.inner, a.calib_label, cdir, a.calib_chunks)
            db1 = imp.db(K.SEED_INNER)
        else:
            ck = K.OUT / 'ckpt'; ck.mkdir(parents=True, exist_ok=True)
            db1 = K.DoubleBoot(stat_fn, full, n, K.SEED_INNER, a.outer, a.inner, ckpt=ck / (base + '_inner1.npz'), label='calibration').run()
        need = K.needs_second_seed(db1, STATS)
        db2 = None
        if a.second_seed == 'always' or (a.second_seed == 'auto' and need):
            if a.calib == 'import':
                db2 = imp.db(K.SEED_INNER2)
            else:
                db2 = K.DoubleBoot(stat_fn, full, n, K.SEED_INNER2, a.outer, a.inner, ckpt=ck / (base + '_inner2.npz'),
                                   label='calibration (second inner seed)').run()
        for j, s in enumerate(STATS):
            cal[s] = K.calibrate_stat(db1, j, db2, a.mc)
        doc['calibration'] = dict(stats=cal, needed_second_seed=need, second_seed_run=db2 is not None,
                                  seconds_inner1=db1.seconds, seconds_inner2=(db2.seconds if db2 is not None else None))
        if a.calib == 'import':
            doc['calib_import'] = imp.info
    else:
        doc['calibration'] = 'not run (--no-calibration): every interval below is the nominal 95% interval'

    def level_of(s):
        lv = cal.get(s, {}).get('level_used') if cal else 0.95
        return 0.95 if lv is None else lv

    iv = {s: K.summ(BS[:, j], full[j], level_of(s)) for j, s in enumerate(STATS)}
    for s in iv:
        if cal and cal[s].get('level_used') is None:
            iv[s]['level_note'] = 'calibration undecided (second inner seed not run): nominal 95% shown'
    doc['intervals'] = iv

    # ---------------- K0-K2 in the fixed sequence
    d = K.DELTA
    Hy = {}
    den0 = PT['window']['den0_deceq']
    Hy['K0'] = dict(R_gl_pp=iv['W_R_gl_pp'], den0_deceq=den0, R_gl_deceq=PT['window']['R_deceq'],
                    passes=bool(np.isfinite(iv['W_R_gl_pp']['ci'][0]) and iv['W_R_gl_pp']['ci'][0] > 0 and np.isfinite(den0) and den0 >= 10.))
    Hy['K1'] = dict(RR_gl_N=iv['W_RR_N'], delta=d, passes=K.inside(iv['W_RR_N']['ci'], d))
    ry = PT['young']['R_deceq']
    if not (np.isfinite(ry) and ry >= 10.):
        Hy['K2'] = dict(passes=None, evaluable=False, R_gl_deceq_young=ry, n_young=PT['young']['n'],
                        note='not evaluable: R_gl in the young-track population is below 10 decision-equivalents')
    else:
        code, word = K.classify_h3(iv['Y_r']['ci'], iv['Y_c']['ci'], d)
        Hy['K2'] = dict(evaluable=True, R_gl_deceq_young=ry, n_young=PT['young']['n'], r=iv['Y_r'], c=iv['Y_c'], classification=word,
                        branch=code, barely_varies=rsy['barely_varies'], passes=code in ('a', 'b', 'c'))
        if code == 'a':
            Hy['K2']['efficiency_r_over_c'] = iv['Y_r_over_c']
    ok = True
    for hk in ('K0', 'K1', 'K2'):
        p = Hy[hk]['passes']
        Hy[hk]['earlier_all_passed'] = ok
        Hy[hk]['confirmed'] = bool(p and ok) if p is not None else None
        Hy[hk]['label'] = ('confirmed' if (p and ok) else ('not confirmed' if ok else 'not confirmatory')) if p is not None else 'not evaluable'
        if p is not None:
            ok = ok and bool(p)
    doc['hypotheses'] = Hy
    doc['written'] = K.clock(); doc['seconds'] = time.time() - t00
    print('written %s (%.0f s)' % (K.write_new(outf, doc), time.time() - t00))


if __name__ == '__main__':
    main()
