"""Recount (second program) of test Y (AMENDMENT_11_v13.md section 6b), revision v13: the adaptive filter's covariance (tracker B2)
against its own permuted twin, on the 105 fresh lead-braking runs. New file, 21 Nov 2026 (Claude Sonnet 5.5).

Written from A11 section 6b / 3.7, ycheck\\CD_DEFINITIONS_Y_v13.md, CD_DEFINITIONS_v13.md and the earlier recounts' code (rc_core_v13,
rc_kern_v13, imported unchanged). The first program (y_twin_v13.py) and ycheck\\out were NOT opened.

Modes (--intervals is required: calibrated | nominal95 | nominal99):
  --test-old --intervals nominal95 [--nboot 2000]
        the 35 old evaluation runs as the online-N REFERENCE only (crit F0, E, N of record; the earlier recounts' loader), same
        construction (factor, scaled twin, 20 permuted twins, default_rng(20261931)). -> out\\TESTOLD_RC_Y_TWIN_v13[_b<nboot>].json
        (reads no fresh run).  With --intervals calibrated the A10 2.6 calibration is run on the reference's Delta_N (plumbing test).
  fresh (no --test-old): needs revision_v13\\LOCK_A11.txt; verifies the 105 B2 files against work\\locks\\FREEZE_B_add7.json before any
        value is read; -> out\\RC_Y_TWIN_v13.json.
  calibrated: A10 2.6 double bootstrap on Delta only (seeds 20261912/13, 20261914, 20261920; twins fixed, not redrawn per resample).
        --calib inproc (default) | export (writes the pod job out\\calib\\<label>.job.npz ... and a PENDING output) | import --calib-chunks DIR.
Outputs are never overwritten.
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('NUMBA_NUM_THREADS', '2')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import argparse, hashlib, json, pathlib, sys, time, warnings
import numpy as np

if os.name == 'nt':                                   # BelowNormal priority (shared laptop)
    try:
        import ctypes
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
    except Exception:
        pass

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))      # python -I: the script folder is not on sys.path
import rc_core_v13 as K                                              # noqa: E402
import rc_y_kern_v13 as YK                                           # noqa: E402

L = K.L
CD = K.CD
LOCK_A11 = K.ROOT13 / 'LOCK_A11.txt'
FREEZE = K.ROOT13 / 'work' / 'locks' / 'FREEZE_B_add7.json'
FREEZE_SHA = 'd06cc48bbe89ec87b3927c962c041b31b5e7aab1dccbe570188a331e0a7b0c12'
B2_DIR = K.ROOT13 / 'work' / 'B_retrack' / 'out' / 'retrack_fresh' / 'B2'
REPL = CD / 'REPLACEMENTS_C_v13.json'
SEED_TWIN = 20261931
NPERM = YK.NPERM
FAMILY = 'lead_braking'
K.RUNNER_FILES = ['rc_y_calib_remote_v13.py', 'rc_y_kern_v13.py', 'rc_kern_v13.py']
PN = YK.twin_names(NPERM)                                   # p01 ... p20


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


# ---------------------------------------------------------------------------------------------- twins
def decision_factor(crit):
    """f_i: median over the 17 rows with finite positive cF0 and cN of sqrt(cF0 / cN); NaN (no factor) where no such row."""
    cf = np.asarray(crit['F0'], float); cn = np.asarray(crit['N'], float)
    with np.errstate(invalid='ignore', divide='ignore'):
        ok = np.isfinite(cf) & np.isfinite(cn) & (cf > 0) & (cn > 0)
        ratio = np.where(ok, np.sqrt(np.where(ok, cf, 1.) / np.where(ok, cn, 1.)), np.nan)
    f = np.full(cf.shape[0], np.nan)
    for i in np.flatnonzero(ok.any(axis=1)):
        f[i] = float(np.median(ratio[i][ok[i]]))
    return f, ok.any(axis=1)


def scaled_crit(crit, f, use):
    """cF0 / f^2 on the decisions flagged in `use`, N's own cN elsewhere."""
    cf = np.asarray(crit['F0'], float); cn = np.asarray(crit['N'], float)
    with np.errstate(invalid='ignore', divide='ignore'):
        sc = cf / (f * f)[:, None]
    return np.where(use[:, None], sc, cn)


def add_twins(runs, seed=SEED_TWIN, nperm=NPERM):
    """Adds r['f'], r['hasf'], r['crit']['S'] (scaled twin) and r['crit']['p01'..'p20'] (permuted twins). One generator
    default_rng(seed); for k = 1..nperm (outer) and runs in the given (ascending run id) order (inner): J = evaluated decisions with a
    factor in ascending index; perm = rng.permutation(len(J)); decision J[j] gets the factor f[J[perm[j]]]. Others keep cN."""
    for r in runs:
        r['f'], r['hasf'] = decision_factor(r['crit'])
        r['crit']['S'] = scaled_crit(r['crit'], r['f'], r['hasf'])
    rng = np.random.default_rng(seed)
    for k in range(nperm):
        for r in runs:
            J = np.flatnonzero(r['ev'] & r['hasf'])
            perm = rng.permutation(J.size)
            fp = r['f'].copy()
            fp[J] = r['f'][J][perm]
            use = np.zeros(r['ev'].size, bool); use[J] = True
            r['crit'][PN[k]] = scaled_crit(r['crit'], fp, use)
    return dict(n_factor=int(sum(int((r['ev'] & r['hasf']).sum()) for r in runs)),
                n_factor_all_decisions=int(sum(int(r['hasf'].sum()) for r in runs)))


# ---------------------------------------------------------------------------------------------- loaders
def old_runs():
    """The 35 old evaluation runs (the earlier recounts' loader; crit F0, E, N of record)."""
    runs = K.load_old_eval_runs()
    for r in runs:
        r['crit'] = {k_: r['crit'][k_] for k_ in ('F0', 'E', 'N')}
        r.pop('vhat', None); r.pop('ahat_long', None); r.pop('lead_found', None); r.pop('ph', None)
    return runs


def check_replacements():
    d = json.loads(REPL.read_text(encoding='utf-8'))
    if d.get('replacements'):
        raise SystemExit('REFUSED: REPLACEMENTS_C_v13.json is not empty (the definitions assume no replacement)')


def verify_b2(rids):
    """FREEZE_B_add7.json's SHA-256 and each B2 file's SHA-256 (nothing is read as a value)."""
    if sha256_file(FREEZE) != FREEZE_SHA:
        raise SystemExit('REFUSED: %s does not have SHA-256 %s' % (FREEZE, FREEZE_SHA))
    man = json.loads(FREEZE.read_text(encoding='utf-8'))
    ent = {pathlib.PureWindowsPath(e['path']).name: e for e in man['arrays_B2_fresh']}
    want = {rid + '_arrays.npz' for rid in rids}
    if set(ent) != want or len(man['arrays_B2_fresh']) != len(want):
        raise SystemExit('REFUSED: the manifest lists %d files, which differ from the %d run ids' % (len(ent), len(want)))
    n_ok = 0
    for rid in rids:
        f = K.check_path(B2_DIR / (rid + '_arrays.npz'))
        if not f.is_file():
            raise SystemExit('REFUSED: missing B2 file %s' % f)
        e = ent[rid + '_arrays.npz']
        if f.stat().st_size != e['bytes'] or sha256_file(f) != e['sha256']:
            raise SystemExit('REFUSED: %s does not match its entry in %s' % (f, FREEZE.name))
        n_ok += 1
    return dict(manifest=str(FREEZE), manifest_sha256=FREEZE_SHA, n_files_verified=n_ok)


def _run_of(z, rid, des):
    return dict(run=rid, desired=float(des), ev=np.asarray(z['evaluated']).astype(bool), clear1=K.clean_clear(z['clear']),
                vbar=np.asarray(z['vbar'], float), idx55=np.asarray(z['idx55']).astype(np.int64),
                crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float)})


def fresh_runs():
    """-> (B2 runs, reference runs, info). Gate, hash verification, then values."""
    if not LOCK_A11.is_file():
        raise SystemExit('REFUSED: fresh values are sealed until %s exists (A11 section 9)' % LOCK_A11)
    check_replacements()
    rids = K.fresh_run_ids(FAMILY)
    if len(rids) != 105:
        raise SystemExit('REFUSED: %d lead-braking run ids, not 105' % len(rids))
    info = verify_b2(rids)
    b2 = []; ref = []
    for rid in rids:
        zr = np.load(K.check_path(K.ARRAYS / 'CV0' / (rid + '.npz')), allow_pickle=False)
        meta = json.loads(str(zr['meta']))
        if meta.get('family') != FAMILY or meta.get('lead_variant'):
            raise SystemExit('REFUSED: %s is not a plain %s run (meta %s)' % (rid, FAMILY, meta))
        des = np.asarray(zr['des'], float)
        if des.size and not np.all(des == des[0]):
            raise SystemExit('REFUSED: %s has more than one desired speed' % rid)
        rr = _run_of(zr, rid, des[0])
        zb = np.load(K.check_path(B2_DIR / (rid + '_arrays.npz')), allow_pickle=False)
        db = np.asarray(zb['des'], float)
        if db.shape != des.shape or not np.array_equal(db, des):
            raise SystemExit('REFUSED: %s: B2 and CV0 desired speeds differ' % rid)
        rb = _run_of(zb, rid, des[0])
        if not np.array_equal(rb['ev'], rr['ev']) or rb['crit']['F0'].shape != rr['crit']['F0'].shape:
            raise SystemExit('REFUSED: %s: B2 and CV0 evaluated sets or shapes differ' % rid)
        b2.append(rb); ref.append(rr)
    info['run_ids'] = rids
    return b2, ref, info


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


def make_problem(runs, names, preps):
    ev_masks = lambda k: [runs[k]['ev']]                                 # noqa: E731
    curves = [K.build_curves(runs, preps, nm, ev_masks)[0] for nm in names]
    return K.Problem(names, curves), curves


def nz(x):
    if x is None:
        return None
    x = float(x)
    return x if np.isfinite(x) else None


def ci_json(ci):
    return None if ci is None or not (np.isfinite(ci[0]) and np.isfinite(ci[1])) else [float(ci[0]), float(ci[1])]


def summarize(runs, tag, P, full_only_names=()):
    """Full-sample points of one problem (F0, E, N, S, p01..p20)."""
    n = len(runs)
    e0 = P.evaluate(np.ones((1, n)))
    den = float(e0['denE'][0]); n_dec = float(e0['n'][0])
    D = {x: float(e0['D'][x][0]) for x in e0['D']}
    RR = {x: L.ratio(D[x], den) for x in D}
    rrp = float(YK.twin_mean([np.array([RR[nm]]) for nm in PN])[0]) if np.isfinite(den) and den > 0 else float('nan')
    return dict(n=n_dec, denE=den, R_pp=den / K.NLEV, D=D, RR=RR, RR_p=rrp, RR_N=RR['N'], RR_S=RR['S'],
                delta=RR['N'] - rrp, delta_s=RR['S'] - rrp)


def boot_series(B):
    """Per-resample series from run_chunks output."""
    den = B['denE']
    rr = {x: K.ratio_arr(B['D'][x], den) for x in B['D']}
    rrp = YK.twin_mean([rr[nm] for nm in PN])
    return dict(den=den, RR_N=rr['N'], RR_S=rr['S'], RR_p=rrp, delta=rr['N'] - rrp, delta_s=rr['S'] - rrp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--intervals', required=True, choices=['nominal95', 'nominal99', 'calibrated'])
    ap.add_argument('--nboot', '--boot', dest='nboot', type=int, default=K.NBOOT)
    ap.add_argument('--outer', type=int, default=K.B_OUTER)
    ap.add_argument('--inner', type=int, default=K.B_INNER)
    ap.add_argument('--mc', type=int, default=K.B_MC)
    ap.add_argument('--second-seed', default='auto', choices=['auto', 'always', 'never'])
    ap.add_argument('--calib', default='inproc', choices=['inproc', 'export', 'import'])
    ap.add_argument('--calib-chunks', default=None)
    ap.add_argument('--calib-label', default='rc_y')
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--no-library', action='store_true')
    ap.add_argument('--tag', default='')
    a = ap.parse_args()
    full_size = (a.nboot == K.NBOOT and a.outer == K.B_OUTER and a.inner == K.B_INNER and a.mc == K.B_MC)
    if a.calib != 'inproc' and a.intervals != 'calibrated':
        raise SystemExit('REFUSED: --calib export / import goes with --intervals calibrated')
    if (a.calib == 'import') != (a.calib_chunks is not None):
        raise SystemExit('REFUSED: --calib-chunks DIR goes with --calib import, and only with it')
    K.check_label(a.calib_label)
    name = '%sRC_Y_TWIN_v13' % ('TESTOLD_' if a.test_old else '')
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
            raise SystemExit('REFUSED: fresh values are sealed until %s exists (A11 section 9)' % LOCK_A11)
        if not full_size:
            raise SystemExit('REFUSED: fresh runs use the full sizes (20,000 / 2,000 / 1,000 / 2,000)')
    cdir = K.calib_dir(a.test_old)
    t00 = time.time()
    nthreads = K.set_workers(a.workers)

    # ---------------- data
    if a.test_old:
        ref = old_runs(); b2 = None
        runinfo = dict(run_ids=[r['run'] for r in ref], source='rev_common_v01.load_runs (35 old evaluation runs), crit F0, E, N of record')
    else:
        b2, ref, runinfo = fresh_runs()
    n = len(ref)
    if n < 2:
        raise SystemExit('REFUSED: fewer than 2 runs')
    ev_count = [int(r['ev'].sum()) for r in ref]
    doc = dict(code='rc_y_twin_v13.py', role='second program (recount), test Y (A11 6b)', model='claude-sonnet-5-5',
               mode='test-old' if a.test_old else 'fresh', intervals=a.intervals, calib_mode=a.calib, started=K.clock(), threads=nthreads,
               sizes=dict(nboot=a.nboot, outer=a.outer, inner=a.inner, mc=a.mc), seeds=dict(
                   boot=K.SEED_BOOT, outer=K.SEED_OUTER, inner=K.SEED_INNER, inner2=K.SEED_INNER2, mc=K.SEED_MC, twin=SEED_TWIN, n_twins=NPERM),
               runs=runinfo, n_evaluated_per_run=ev_count)
    print('%d runs, %d evaluated decisions (%s)' % (n, sum(ev_count), 'old reference only' if a.test_old else 'fresh'), flush=True)

    # ---------------- twins (reference always; B2 in fresh mode); every set has its own generator default_rng(20261931)
    tw_ref = add_twins(ref)
    names = ['F0', 'E', 'N', 'S'] + PN
    prep_ref = [K.Prep(r) for r in ref]
    P_ref, _ = make_problem(ref, names, prep_ref)
    doc['n_factor_ref'] = tw_ref
    pts_ref = summarize(ref, 'ref', P_ref)
    if pts_ref['n'] != sum(ev_count):
        raise SystemExit('REFUSED: curve decision count %s differs from the evaluated count %d' % (pts_ref['n'], sum(ev_count)))
    P_b2 = pts_b2 = None
    if b2 is not None:
        tw_b2 = add_twins(b2)
        doc['n_factor_b2'] = tw_b2
        prep_b2 = [K.Prep(r) for r in b2]
        P_b2, _ = make_problem(b2, names, prep_b2)
        pts_b2 = summarize(b2, 'b2', P_b2)
        if pts_b2['n'] != sum(ev_count):
            raise SystemExit('REFUSED: B2 decision count differs from the reference')
    print('curves built (%.0f s)' % (time.time() - t00), flush=True)
    doc['points_ref'] = pts_ref
    if pts_b2 is not None:
        doc['points_b2'] = pts_b2

    # ---------------- the statistic of the double bootstrap: Delta of B2 (fresh) or Delta_N of the reference (old-run plumbing test)
    cal_runs, cal_P, cal_pts = (b2, P_b2, pts_b2) if b2 is not None else (ref, P_ref, pts_ref)
    cnames = ['F0', 'E', 'N'] + PN
    prep_c = prep_b2 if b2 is not None else prep_ref
    P_cal, _ = make_problem(cal_runs, cnames, prep_c)
    stat = YK.YStat(P_cal)
    full = stat(np.ones((1, n)))[0]
    if abs(full[0] - cal_pts['delta']) > 1e-15:
        raise SystemExit('REFUSED: the calibration problem and the full problem disagree on Delta (%r vs %r)' % (full[0], cal_pts['delta']))

    # ---------------- library cross-check of the full-sample points (shared library; never the source of a value)
    if not a.no_library:
        A9 = K.try_a9()
        if A9 is not None:
            libs = {}
            for tag, rs_, pts_ in [('ref', ref, pts_ref)] + ([('b2', b2, pts_b2)] if b2 is not None else []):
                try:
                    e, _ = K.library_point(A9, rs_, names, lambda k, rs_=rs_: [rs_[k]['ev']], 0, 'F0', 'E')
                    lib = dict(denE=float(e['denE']), n=float(e['n']), D={x: float(e['D'][x]) for x in e['D']})
                    lib['max_abs_diff_vs_own'] = max([abs(lib['denE'] - pts_['denE'])] + [abs(lib['D'][x] - pts_['D'][x]) for x in lib['D']])
                    lib['identical'] = bool(lib['max_abs_diff_vs_own'] == 0.)
                except Exception as ex:                                  # pragma: no cover
                    lib = dict(error=repr(ex))
                libs[tag] = lib
                print('library point %s: %s (%.0f s)' % (tag, {k_: lib.get(k_) for k_ in ('identical', 'max_abs_diff_vs_own', 'error')},
                                                       time.time() - t00), flush=True)
            doc['library_point'] = libs

    # ---------------- main bootstrap (run resamples of optA_lib_v02.boot_counts(n, 20000, 20261911); smaller = first rows)
    CNT = L.boot_counts(n, a.nboot, K.SEED_BOOT)
    Bref = run_chunks(P_ref, CNT)
    Bb2 = run_chunks(P_b2, CNT) if P_b2 is not None else None
    del CNT
    sref = boot_series(Bref)
    sb2 = boot_series(Bb2) if Bb2 is not None else None
    den_main = (sb2 or sref)['den']
    share_pos = float(np.mean(np.isfinite(den_main) & (den_main > 0)))
    print('main bootstrap done (%.0f s); share D(E)>0: %.4f' % (time.time() - t00, share_pos), flush=True)

    # ---------------- level of the main statistic Delta (B2 in fresh mode; the reference's Delta_N in the old-run plumbing test)
    level = {'nominal95': 0.95, 'nominal99': 0.99}.get(a.intervals, 0.95)
    if a.intervals == 'calibrated':
        if a.calib == 'export':
            state = dict(n_boot=np.int64(a.nboot))
            info = K.calib_export(stat, full, n, a.outer, a.inner, a.calib_label, cdir, doc['mode'], doc['code'], state)
            doc['PENDING'] = ('PENDING: the double bootstrap (A10 section 2.6) has not run. No calibrated level, interval or '
                              'hypothesis is in this file. Finish with --calib import --calib-chunks DIR.')
            doc['calibration'] = dict(status='pending', job=info, runner='rc_y_calib_remote_v13.py JOBDIR %s --seeds SEED --outer LO:HI --threads 1' % a.calib_label)
            doc['written'] = K.clock(); doc['seconds'] = time.time() - t00
            print('job written: %s (SHA-256 %s)' % (info['job'], info['job_sha256']), flush=True)
            print('written %s (PENDING; %.0f s)' % (K.write_new(outf, doc), time.time() - t00))
            return
        if a.calib == 'import':
            imp = K.CalibImport(stat, full, n, a.outer, a.inner, a.calib_label, cdir, a.calib_chunks)
            db1 = imp.db(K.SEED_INNER)
        else:
            ck = K.OUT / 'ckpt'; ck.mkdir(parents=True, exist_ok=True)
            db1 = K.DoubleBoot(stat, full, n, K.SEED_INNER, a.outer, a.inner, ckpt=ck / (name + '_inner1.npz'), label='y').run()
        need = K.needs_second_seed(db1, YK.STATS)
        db2 = None
        if a.second_seed == 'always' or (a.second_seed == 'auto' and need):
            if a.calib == 'import':
                db2 = imp.db(K.SEED_INNER2)
            else:
                db2 = K.DoubleBoot(stat, full, n, K.SEED_INNER2, a.outer, a.inner, ckpt=ck / (name + '_inner2.npz'), label='y2').run()
        c = K.calibrate_stat(db1, 0, db2, n_mc=a.mc)
        lv = c.get('level_used')
        if lv is None:
            raise SystemExit('REFUSED: calibration of Delta undecided (second inner seed not run); use --second-seed always')
        level = float(lv)
        doc['calibration'] = dict(stats=YK.STATS, second_seed_run=db2 is not None, needs_second_seed=need, per_stat={'delta': c},
                                  seconds_inner1=db1.seconds, seconds_inner2=(db2.seconds if db2 is not None else None),
                                  outer_den_le0=int((~(db1.outer_est[:, 0] > 0)).sum()))
        if a.calib == 'import':
            doc['calib_import'] = imp.info
    main_s = sb2 if sb2 is not None else sref
    ci_delta = K.pct_interval(main_s['delta'], level)
    doc['levels'] = dict(delta=level)
    doc['intervals_nominal95_all'] = dict(delta=K.pct_interval(main_s['delta'], 0.95), delta_nominal99=K.pct_interval(main_s['delta'], 0.99))
    doc['resamples'] = {k_: dict(n=int(x.size), n_finite=int(np.isfinite(x).sum())) for k_, x in main_s.items()}

    # ---------------- values (definitions section 5)
    v = {}
    pre = 'Y.'
    v[pre + 'n_runs'] = int(n)
    v[pre + 'n_dec'] = int(pts_ref['n'])
    v[pre + 'n_factor'] = int(tw_b2['n_factor']) if b2 is not None else None
    v[pre + 'n_factor_ref'] = int(tw_ref['n_factor'])
    v[pre + 'share_pos'] = share_pos
    if b2 is not None:
        v[pre + 'delta'] = nz(pts_b2['delta']); v[pre + 'delta.ci'] = ci_json(ci_delta); v[pre + 'delta.level'] = level
        v[pre + 'Y1'] = bool(np.isfinite(ci_delta[0]) and ci_delta[0] > 0)
        for key, pt, ser in [('RR_NB2', pts_b2['RR_N'], sb2['RR_N']), ('RR_B2s', pts_b2['RR_S'], sb2['RR_S']), ('RR_B2p', pts_b2['RR_p'], sb2['RR_p']),
                             ('delta_s', pts_b2['delta_s'], sb2['delta_s'])]:
            v[pre + key] = nz(pt); v[pre + key + '.ci'] = ci_json(K.pct_interval(ser, 0.95)); v[pre + key + '.level'] = 0.95
        v[pre + 'R'] = nz(pts_b2['R_pp'])
    for key, pt, ser in [('RR_N', pts_ref['RR_N'], sref['RR_N']), ('RR_Ns', pts_ref['RR_S'], sref['RR_S']), ('RR_Np', pts_ref['RR_p'], sref['RR_p']),
                         ('delta', pts_ref['delta'], sref['delta']), ('delta_s', pts_ref['delta_s'], sref['delta_s'])]:
        v[pre + 'ref.' + key] = nz(pt)
        # in the old-run plumbing test with calibrated intervals the reference's Delta_N is the calibrated statistic
        lvl = level if (a.test_old and key == 'delta') else 0.95
        v[pre + 'ref.' + key + '.ci'] = ci_json(K.pct_interval(ser, lvl)); v[pre + 'ref.' + key + '.level'] = lvl
    v[pre + 'ref.R'] = nz(pts_ref['R_pp'])
    doc['values'] = v
    doc['written'] = K.clock(); doc['seconds'] = time.time() - t00
    print('written %s' % K.write_new(outf, doc), flush=True)
    for k_, x in v.items():
        print('  %-26s %s' % (k_, x))


if __name__ == '__main__':
    main()
