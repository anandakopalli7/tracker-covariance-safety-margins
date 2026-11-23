"""Recount (second program) of the crossing sprint X (amendment A11, pedestrian crossing only), revision v13.
New file, 21 Nov 2026 (Claude Sonnet 5.5). Revised 21 Nov ~14:30 EST for the coordinator's changes (A11 section 3 as built: X0, X1, X2;
E5_N in X1; CASES_X_PC_v13.json; calibrated intervals with pod export / import).

Written from crossing\\CD_DEFINITIONS_X_v13.md, A11 section 3, CD_DEFINITIONS_v13.md and the earlier recount's code (rc_core_v13,
rc_kern_v13, imported unchanged). The first program (x_cross_v13.py), the extractor and crossing\\out were NOT opened.

Modes (--family pedestrian_crossing only):
  --test-old --intervals nominal95 [--nboot 2000]     the 51 stored arrays of record (gateR_rt_v01), name order.
        -> out\\TESTOLD_RC_X_CROSS_pedestrian_crossing_v13[_b<nboot>].json   (reads no fresh run)
  --n 390 --cases-sha 58902be5... --intervals calibrated --calib inproc|export|import      fresh arrays; needs LOCK_A11.txt
        -> out\\RC_X_CROSS_pedestrian_crossing_v13.json
  calibrated: A10 2.6 double bootstrap on R_gl, RR_E5N, RR_E5N - RR_E5pN, RR_N (seeds 20261912/13, 20261914, 20261920).
  --calib export writes the pod job out\\calib\\<label>.job.npz (+ .meta.json, .state.npz) and a PENDING output; run
  rc_x_calib_remote_v13.py on pods; --calib import --calib-chunks DIR finishes the run.  Outputs are never overwritten.
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('NUMBA_NUM_THREADS', '2')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import argparse, hashlib, json, pathlib, sys, time
import numpy as np

if os.name == 'nt':                                   # BelowNormal priority (shared laptop)
    try:
        import ctypes
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
    except Exception:
        pass

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))      # python -I: the script folder is not on sys.path
import rc_core_v13 as K                                              # noqa: E402
import rc_x_kern_v13 as XK                                           # noqa: E402

L = K.L
CD = K.CD
LOCK_A11 = K.ROOT13 / 'LOCK_A11.txt'
CASES_X = CD / 'crossing' / 'CASES_X_PC_v13.json'
CASES_X_SHA = '58902be5ce022b314148308140cb8fc9373bc7aee401531367d456755409a31e'
REPL_FILES = [CD / 'crossing' / 'REPLACEMENTS_X_v13.json']
ARRAYS_X = CD / 'arrays_x' / 'CV0'
STEP0 = K.ROOT13 / 'work' / 'B_retrack' / 'out' / 'step0' / 'STEP0_CROSSING_v01.json'
FAMILY = 'pedestrian_crossing'
STATS = XK.STATS                                    # calibrated statistics
K.RUNNER_FILES = ['rc_x_calib_remote_v13.py', 'rc_x_kern_v13.py', 'rc_kern_v13.py']
CLASSNAME = dict(a='recovers', b='uninformative variation', c='amplitude-limited', d='inconclusive')


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------------------------------------- loaders
def run_from_npz(z, rid, family):
    meta = json.loads(str(z['meta']))
    if meta.get('family') != family:
        raise SystemExit('REFUSED: %s has meta.family %r, not %r' % (rid, meta.get('family'), family))
    return dict(run=rid, desired=float(meta['desired']), ev=np.asarray(z['evaluated']).astype(bool),
                clear1=K.clean_clear(z['clear']), vbar=np.asarray(z['vbar'], float),
                idx55=np.asarray(z['idx55']).astype(np.int64),
                crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float)},
                contact=bool(meta.get('contact_k') is not None and meta.get('contact_k') >= 0)), meta


def load_old(family):
    runs = []; sets = {}
    for f in sorted(K.STORED_OLD.glob('*.npz'), key=lambda p: p.name):
        with np.load(f, allow_pickle=False) as z:
            meta = json.loads(str(z['meta']))
            if meta.get('family') != family:
                continue
            r, meta = run_from_npz(z, meta.get('run', f.stem), family)
        r['file'] = f.name
        runs.append(r)
        sets[meta.get('set')] = sets.get(meta.get('set'), 0) + 1
    return runs, sets


def load_fresh(family, n, cases_sha):
    if not LOCK_A11.is_file():
        raise SystemExit('REFUSED: fresh crossing arrays are sealed until %s exists (A11 section 9)' % LOCK_A11)
    raw = CASES_X.read_bytes()
    if sha256_bytes(raw) != cases_sha:
        raise SystemExit('REFUSED: SHA-256 of CASES_X_PC_v13.json is %s, not --cases-sha %s' % (sha256_bytes(raw), cases_sha))
    d = json.loads(raw.decode('utf-8'))
    cs = [c for c in d['cases'] if c['family'] == family]
    study = sorted([c for c in cs if not c['reserve']], key=lambda c: c['position'])
    if [c['position'] for c in study] != list(range(len(study))):
        raise SystemExit('REFUSED: study positions are not 0..%d' % (len(study) - 1))
    if not (1 <= n <= len(study)):
        raise SystemExit('REFUSED: --n %d is outside 1..%d' % (n, len(study)))
    first = study[:n]
    repl = {}; repl_file = None
    for rf in REPL_FILES:
        if rf.is_file():
            repl = json.loads(rf.read_text(encoding='utf-8')).get('replacements', {}); repl_file = str(rf); break
    byid = {c['case']: c for c in cs}
    reserves = {c['case'] for c in cs if c['reserve']}
    for k_, v_ in repl.items():
        if v_ not in reserves:
            raise SystemExit('REFUSED: replacement %s -> %s is not a reserve case' % (k_, v_))
    jobs = []
    for c in first:
        c2 = byid[repl[c['case']]] if c['case'] in repl else c
        if c2['desired_mps'] != c['desired_mps']:
            raise SystemExit('REFUSED: replacement of %s is not of the same speed' % c['case'])
        if c2['family'] != family:
            raise SystemExit('REFUSED: replacement of %s is not of family %s' % (c['case'], family))
        jobs.append(c2['job'])
    if len(set(jobs)) != len(jobs):
        raise SystemExit('REFUSED: a job occurs twice after replacements')
    rids = sorted(jobs)
    runs = []
    for rid in rids:
        f = K.check_path(ARRAYS_X / (rid + '.npz'))
        if not f.is_file():
            raise SystemExit('REFUSED: missing array %s' % f)
        with np.load(f, allow_pickle=False) as z:
            r, meta = run_from_npz(z, rid, family)
            if meta.get('run_id') not in (None, rid):
                raise SystemExit('REFUSED: %s has meta.run_id %r' % (f.name, meta.get('run_id')))
        runs.append(r)
    return runs, dict(cases=[c['case'] for c in first], run_ids=rids, replacements={k_: v_ for k_, v_ in repl.items() if k_ in {c['case'] for c in first}},
                      replacements_file=repl_file, cases_sha256=sha256_bytes(raw))


# ---------------------------------------------------------------------------------------------- helpers
def run_chunks(P, CN, chunk=1000):
    out = None
    for s0 in range(0, CN.shape[0], chunk):
        e = P.evaluate(CN[s0:s0 + chunk])
        if out is None:
            out = dict(n=[e['n']], denE=[e['denE']], D={a: [e['D'][a]] for a in e['D']})
        else:
            out['n'].append(e['n']); out['denE'].append(e['denE'])
            for a in e['D']:
                out['D'][a].append(e['D'][a])
    return dict(n=np.concatenate(out['n']), denE=np.concatenate(out['denE']), D={a: np.concatenate(v) for a, v in out['D'].items()})


def nz(x):
    if x is None:
        return None
    x = float(x)
    return x if np.isfinite(x) else None


def ci_json(ci):
    return None if ci is None or not (np.isfinite(ci[0]) and np.isfinite(ci[1])) else [float(ci[0]), float(ci[1])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--family', required=True, choices=['pedestrian_crossing', 'vehicle_crossing'])
    ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--n', type=int, default=None)
    ap.add_argument('--cases-sha', default=None)
    ap.add_argument('--intervals', required=True, choices=['nominal95', 'calibrated'])
    ap.add_argument('--nboot', '--boot', dest='nboot', type=int, default=K.NBOOT)
    ap.add_argument('--outer', type=int, default=K.B_OUTER)
    ap.add_argument('--inner', type=int, default=K.B_INNER)
    ap.add_argument('--mc', type=int, default=K.B_MC)
    ap.add_argument('--second-seed', default='auto', choices=['auto', 'always', 'never'])
    ap.add_argument('--calib', default='inproc', choices=['inproc', 'export', 'import'])
    ap.add_argument('--calib-chunks', default=None)
    ap.add_argument('--calib-label', default='rc_x')
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--no-library', action='store_true')
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    if a.family != FAMILY:
        raise SystemExit('REFUSED: A11 runs pedestrian crossing only (vehicle crossing is not tested)')
    family = a.family; pre = 'X.ped.'
    full_size = (a.nboot == K.NBOOT and a.outer == K.B_OUTER and a.inner == K.B_INNER and a.mc == K.B_MC)
    if a.test_old == (a.n is not None):
        raise SystemExit('REFUSED: give exactly one of --test-old and --n N (with --cases-sha)')
    if not a.test_old and not a.cases_sha:
        raise SystemExit('REFUSED: fresh mode needs --cases-sha')
    if a.calib != 'inproc' and a.intervals != 'calibrated':
        raise SystemExit('REFUSED: --calib export / import goes with --intervals calibrated')
    if (a.calib == 'import') != (a.calib_chunks is not None):
        raise SystemExit('REFUSED: --calib-chunks DIR goes with --calib import, and only with it')
    K.check_label(a.calib_label)
    name = '%sRC_X_CROSS_%s_v13' % ('TESTOLD_' if a.test_old else '', family)
    if not full_size:
        name += '_b%d' % a.nboot + ('_o%d_i%d' % (a.outer, a.inner) if a.intervals == 'calibrated' else '')
    if a.intervals == 'calibrated' and a.test_old:
        name += '_calibrated'
    name += a.tag
    outf = K.OUT / (name + '.json')
    if a.calib == 'export':
        outf = K.OUT / (name + '.PENDING.json')
    if outf.exists():
        raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % outf)
    if not a.test_old:
        if not LOCK_A11.is_file():                                     # the gate comes before anything is opened
            raise SystemExit('REFUSED: fresh crossing arrays are sealed until %s exists (A11 section 9)' % LOCK_A11)
        if not full_size:
            raise SystemExit('REFUSED: fresh runs use the full sizes (20,000 / 2,000 / 1,000 / 2,000)')
    cdir = K.calib_dir(a.test_old)
    t00 = time.time()
    nthreads = K.set_workers(a.workers)

    # ---------------- run set
    if a.test_old:
        runs, sets = load_old(family)
        runinfo = dict(sets=sets, run_ids=[r['run'] for r in runs], files=[r['file'] for r in runs])
    else:
        runs, runinfo = load_fresh(family, a.n, a.cases_sha)
    n = len(runs)
    if n < 2:
        raise SystemExit('REFUSED: fewer than 2 runs')
    ev_count = [int(r['ev'].sum()) for r in runs]
    doc = dict(code='rc_x_cross_v13.py', role='second program (recount), crossing sprint X (A11)', model='claude-sonnet-5-5',
               family=family, mode='test-old' if a.test_old else 'fresh', intervals=a.intervals, calib_mode=a.calib,
               started=K.clock(), threads=nthreads,
               sizes=dict(nboot=a.nboot, outer=a.outer, inner=a.inner, mc=a.mc), delta=K.DELTA,
               seeds=dict(boot=K.SEED_BOOT, outer=K.SEED_OUTER, inner=K.SEED_INNER, inner2=K.SEED_INNER2, perm=K.SEED_PERM, mc=K.SEED_MC),
               runs=runinfo, n_evaluated_per_run=ev_count)
    print('%s: %d runs, %d evaluated decisions (%s)' % (family, n, sum(ev_count), 'old' if a.test_old else 'fresh'), flush=True)

    # ---------------- sources: E5_N (own amplitude), E5p_N, and descriptive E5 / E5p (record amplitude)
    u, uinfo = K.e5_u(runs, 'F0', 'E')
    up = K.permute_u(runs, u)
    rs = K.ratio_summary(np.concatenate([K.margin_ratio_values(r, 'N', 'F0') for r in runs]))
    have_n = rs['n'] > 0 and np.isfinite(rs['median']) and rs['median'] > 0
    if not have_n:
        raise SystemExit('REFUSED: no binding row with finite positive N and F0 scales: E5_N is undefined')
    for r, uu, pp in zip(runs, u, up):
        r['crit']['E5'] = K.oracle_crit(r['crit']['F0'], K.RATIO, K.E5_AMP, uu)
        r['crit']['E5p'] = K.oracle_crit(r['crit']['F0'], K.RATIO, K.E5_AMP, pp)
        r['crit']['E5N'] = K.oracle_crit(r['crit']['F0'], rs['median'], rs['A'], uu)
        r['crit']['E5pN'] = K.oracle_crit(r['crit']['F0'], rs['median'], rs['A'], pp)
    names = ['F0', 'E', 'N', 'E5N', 'E5pN', 'E5', 'E5p']
    doc['E5'] = dict(uinfo, m_record=K.RATIO, A_record=K.E5_AMP, m_N=rs['median'], A_N=rs['A'])
    doc['margin_ratio_N_F0'] = rs
    preps = [K.Prep(r) for r in runs]
    ev_masks = lambda k: [runs[k]['ev']]                                 # noqa: E731
    curves = {nm: K.build_curves(runs, preps, nm, ev_masks)[0] for nm in names}
    P = K.Problem(names, [curves[x] for x in names])
    x_names = ['F0', 'E', 'N', 'E5N', 'E5pN']
    stat = XK.XStat(K.Problem(x_names, [curves[x] for x in x_names]))
    print('curves built (%.0f s): %s' % (time.time() - t00, {k: c.npts for k, c in curves.items()}), flush=True)

    # ---------------- full-sample points
    e0 = P.evaluate(np.ones((1, n)))
    n_dec = float(e0['n'][0]); den = float(e0['denE'][0])
    pts = dict(n=n_dec, denE=den, R_pp=den / K.NLEV, R_deceq=L.dec_eq(den, n_dec),
               D={x: float(e0['D'][x][0]) for x in e0['D']}, RR={x: L.ratio(float(e0['D'][x][0]), den) for x in e0['D']})
    pts['RR_E5NmP'] = pts['RR']['E5N'] - pts['RR']['E5pN']
    pts['RR_E5recmP'] = pts['RR']['E5'] - pts['RR']['E5p']
    doc['points'] = pts
    if n_dec != sum(ev_count):
        raise SystemExit('REFUSED: curve decision count %s differs from the evaluated count %d' % (n_dec, sum(ev_count)))
    full = stat(np.ones((1, n)))[0]
    assert abs(full[1] - pts['RR']['E5N']) == 0 and abs(full[3] - pts['RR']['N']) == 0

    # ---------------- library cross-check of the full-sample points (shared library; never the source of a value)
    if not a.no_library:
        A9 = K.try_a9()
        if A9 is not None:
            try:
                e, _ = K.library_point(A9, runs, names, lambda k: [runs[k]['ev']], 0, 'F0', 'E')
                lib = dict(denE=float(e['denE']), n=float(e['n']), RR={x: L.ratio(float(e['D'][x]), float(e['denE'])) for x in e['D']},
                           D={x: float(e['D'][x]) for x in e['D']})
                lib['max_abs_diff_vs_own'] = max([abs(lib['denE'] - den)] + [abs(lib['D'][x] - pts['D'][x]) for x in lib['D']])
                lib['identical'] = bool(lib['max_abs_diff_vs_own'] == 0.)
            except Exception as ex:                                      # pragma: no cover
                lib = dict(error=repr(ex))
            doc['library_point'] = lib
            print('library point: %s (%.0f s)' % ({k: lib.get(k) for k in ('identical', 'max_abs_diff_vs_own', 'error')}, time.time() - t00), flush=True)

    # ---------------- main bootstrap (run resamples of optA_lib_v02.boot_counts(n, 20000, 20261911); smaller = first rows)
    st = K.calib_state(cdir, a.calib_label, full, a.nboot) if a.calib == 'import' else None
    if st is not None and 'bden' in st:
        B = dict(denE=st['bden'], D={x: st['bD_' + x] for x in names[2:]})
        print('main bootstrap: taken from the export run', flush=True)
    else:
        CNT = L.boot_counts(n, a.nboot, K.SEED_BOOT)
        B = run_chunks(P, CNT)
        del CNT
    bden = B['denE']
    brr = {x: K.ratio_arr(B['D'][x], bden) for x in B['D']}
    bs = dict(R_gl_pp=bden / K.NLEV, RR_E5N=brr['E5N'], RR_E5NmP=brr['E5N'] - brr['E5pN'], RR_N=brr['N'],
              RR_E5rec=brr['E5'], RR_E5recmP=brr['E5'] - brr['E5p'])
    share_pos = float(np.mean(np.isfinite(bden) & (bden > 0)))
    print('main bootstrap done (%.0f s); share D(E)>0: %.4f' % (time.time() - t00, share_pos), flush=True)

    # ---------------- levels: nominal 95% or A10 2.6 calibration
    levels = {s: 0.95 for s in list(STATS) + ['RR_E5rec', 'RR_E5recmP']}
    if a.intervals == 'calibrated':
        if a.calib == 'export':
            state = dict(n_boot=np.int64(a.nboot), bden=bden, **{'bD_' + x: B['D'][x] for x in names[2:]})
            info = K.calib_export(stat, full, n, a.outer, a.inner, a.calib_label, cdir, doc['mode'], doc['code'], state)
            doc['PENDING'] = ('PENDING: the double bootstrap (A10 section 2.6) has not run. No calibrated level, interval or '
                              'hypothesis is in this file. Finish with --calib import --calib-chunks DIR.')
            doc['calibration'] = dict(status='pending', job=info, runner='rc_x_calib_remote_v13.py JOBDIR %s --seeds SEED --outer LO:HI --threads 1' % a.calib_label)
            doc['points'] = pts
            doc['written'] = K.clock(); doc['seconds'] = time.time() - t00
            print('job written: %s (SHA-256 %s)' % (info['job'], info['job_sha256']), flush=True)
            print('written %s (PENDING; %.0f s)' % (K.write_new(outf, doc), time.time() - t00))
            return
        if a.calib == 'import':
            imp = K.CalibImport(stat, full, n, a.outer, a.inner, a.calib_label, cdir, a.calib_chunks)
            db1 = imp.db(K.SEED_INNER)
        else:
            ck = K.OUT / 'ckpt'; ck.mkdir(parents=True, exist_ok=True)
            db1 = K.DoubleBoot(stat, full, n, K.SEED_INNER, a.outer, a.inner, ckpt=ck / (name + '_inner1.npz'), label='x').run()
        need = K.needs_second_seed(db1, STATS)
        db2 = None
        if a.second_seed == 'always' or (a.second_seed == 'auto' and need):
            if a.calib == 'import':
                db2 = imp.db(K.SEED_INNER2)
            else:
                db2 = K.DoubleBoot(stat, full, n, K.SEED_INNER2, a.outer, a.inner, ckpt=ck / (name + '_inner2.npz'), label='x2').run()
        calib = {}
        for j, s in enumerate(STATS):
            c = K.calibrate_stat(db1, j, db2, n_mc=a.mc)
            calib[s] = c
            lv = c.get('level_used')
            if lv is None:
                raise SystemExit('REFUSED: calibration of %s undecided (second inner seed not run); use --second-seed always' % s)
            levels[s] = float(lv)
        doc['calibration'] = dict(stats=STATS, second_seed_run=db2 is not None, needs_second_seed=need, per_stat=calib,
                                  seconds_inner1=db1.seconds, seconds_inner2=(db2.seconds if db2 is not None else None),
                                  outer_den_le0=int((~(db1.outer_est[:, 0] > 0)).sum()))
        if a.calib == 'import':
            doc['calib_import'] = imp.info
    doc['levels'] = levels

    ci = {s: K.pct_interval(bs[s], levels[s]) for s in bs}
    ciR, ciE5N, ciE5NmP, ciN = ci['R_gl_pp'], ci['RR_E5N'], ci['RR_E5NmP'], ci['RR_N']
    doc['intervals_nominal95_all'] = {k: K.pct_interval(x, 0.95) for k, x in bs.items()}
    doc['resamples'] = {k: dict(n=int(x.size), n_finite=int(np.isfinite(x).sum())) for k, x in bs.items()}

    # ---------------- sequence X0, X1, X2
    X0 = bool(np.isfinite(ciR[0]) and ciR[0] > 0 and share_pos >= 0.975)
    X1 = bool(np.isfinite(ciE5N[0]) and ciE5N[0] > 0 and np.isfinite(ciE5NmP[0]) and ciE5NmP[0] > 0)
    r_pt = pts['RR']['N']; c_pt = pts['RR']['E5N']
    cl, _ = K.classify_h3(ciN, ciE5N)
    X2 = cl in ('a', 'b', 'c')
    eff = eff_ci = None
    if cl == 'a':
        with np.errstate(divide='ignore', invalid='ignore'):
            eff = r_pt / c_pt if (np.isfinite(c_pt) and c_pt != 0 and np.isfinite(r_pt)) else float('nan')
            rb, cb = bs['RR_N'], brr['E5N']
            ok = np.isfinite(rb) & np.isfinite(cb) & (cb != 0)
            effb = np.where(ok, rb / np.where(cb != 0, cb, 1.), np.nan)
        eff_ci = K.pct_interval(effb, levels['RR_N'])
    doc['detail'] = dict(class_letter=cl, RR_N_ci_inside_delta=bool(K.inside(ciN)), RR_E5p=pts['RR']['E5p'], RR_E5pN=pts['RR']['E5pN'])

    v = {}
    v[pre + 'n_runs'] = int(n); v[pre + 'n_dec'] = int(n_dec)
    v[pre + 'R'] = nz(pts['R_pp']); v[pre + 'R.dec'] = nz(pts['R_deceq']); v[pre + 'R.share_pos'] = share_pos
    v[pre + 'R.ci'] = ci_json(ciR); v[pre + 'R.level'] = levels['R_gl_pp']
    for s, pt in [('RR_E5N', c_pt), ('RR_E5NmP', pts['RR_E5NmP']), ('RR_N', r_pt), ('RR_E5rec', pts['RR']['E5']),
                  ('RR_E5recmP', pts['RR_E5recmP'])]:
        v[pre + s] = nz(pt); v[pre + s + '.ci'] = ci_json(ci[s]); v[pre + s + '.level'] = levels[s]
    v[pre + 'ratio.median'] = nz(rs['median']); v[pre + 'ratio.A'] = nz(rs['A'])
    v[pre + 'ratio.within5'] = nz(rs['share_within_5pct']); v[pre + 'ratio.barely'] = bool(rs['barely_varies'])
    v[pre + 'X2.class'] = CLASSNAME[cl]
    v[pre + 'X2.eff'] = nz(eff) if cl == 'a' else None
    v[pre + 'X2.eff.ci'] = ci_json(eff_ci) if cl == 'a' else None
    v[pre + 'X0'] = X0; v[pre + 'X1'] = X1; v[pre + 'X2'] = X2
    v[pre + 'X0.confirmed'] = X0; v[pre + 'X1.confirmed'] = bool(X0 and X1); v[pre + 'X2.confirmed'] = bool(X0 and X1 and X2)
    v[pre + 'tested'] = X0
    v[pre + 'n_contact'] = int(sum(r['contact'] for r in runs))
    v[pre + 'n_replaced'] = int(len(runinfo.get('replacements', {}))) if not a.test_old else 0
    v[pre + 'under_run'] = bool(n < 332) if not a.test_old else False
    v[pre + 'RR_N.inside_delta'] = bool(K.inside(ciN))
    doc['values'] = v

    # ---------------- test-old: compare the points with package B's step 0
    if a.test_old:
        try:
            s0 = json.loads(STEP0.read_text(encoding='utf-8'))['families'][family]['points']
            mine = {'R_pp': pts['R_pp'], 'R_deceq': pts['R_deceq'], 'RR.N': pts['RR']['N'], 'RR.E5N': pts['RR']['E5N'],
                    'RR.E5rec': pts['RR']['E5']}
            theirs = {'R_pp': s0['R_pp'], 'R_deceq': s0['R_deceq'], 'RR.N': s0['RR']['N'], 'RR.E5N': s0['RR']['E5N'],
                      'RR.E5rec': s0['RR']['E5rec']}
            diffs = {k_: abs(mine[k_] - theirs[k_]) for k_ in mine}
            doc['compare_step0'] = dict(file=str(STEP0), mine=mine, step0=theirs, abs_diff=diffs, max_abs_diff=max(diffs.values()),
                                        n_equal_step0=(s0['n'] == n_dec))
            print('vs step0: max abs diff %.3g' % doc['compare_step0']['max_abs_diff'], flush=True)
        except Exception as ex:
            doc['compare_step0'] = 'not available: %r' % ex
    doc['written'] = K.clock(); doc['seconds'] = time.time() - t00
    print('written %s' % K.write_new(outf, doc), flush=True)
    for k_, x in v.items():
        print('  %-26s %s' % (k_, x))


if __name__ == '__main__':
    main()
