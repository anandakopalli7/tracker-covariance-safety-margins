"""Y (AMENDMENT_11_v13.md sec. 6b): the adaptive filter (B2) against its own permuted twin, on the 105 fresh lead-braking runs. First
program. New file, 21 Nov 2026 (Claude Opus 5.5, session CD), written before LOCK_A11 and before any Y value. Specification: A11 sec. 6b
and ycheck\\CD_DEFINITIONS_Y_v13.md (factor, twins, draw order, outputs).

Engine: package B's frozen trk_score_v01 (gridless events, rr_gl) and CD's frozen gl_fast_v13 (checked equal at the full sample).
Delta = RR_gl(N_B2) - mean_k RR_gl(B2p_k) on B2's own room; 20,000 run resamples (default_rng(20261911)); A10 sec. 2.6 level for Delta
(group y_main; --calib local|export|import; export writes a kind-'Y' job for ycheck\\y_calib_remote_v13.py). Descriptive at 95%.
Y1 passes if Delta's lower end > 0.
Gate: refuses unless revision_v13/LOCK_A11.txt exists. --test-old: the 35 old evaluation runs as the online-N reference only.
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 ycheck\\y_twin_v13.py [--test-old] --intervals calibrated|nominal95|nominal99
         [--calib local|export|import] [--nboot N] [--outer N]
Writes ycheck/out/[TESTOLD_]Y_TWIN_v13[_PENDING_CALIB].json (never overwritten).
"""
import argparse, hashlib, json, os, pathlib, sys, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
if os.name == 'nt':                                      # laptop rule: BelowNormal priority (no effect on any value)
    import ctypes; ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
import numpy as np
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(CD / 'analysis'))
import cd_common_v13 as CC               # noqa: E402
import trk_env_v01 as env                # noqa: E402
env.setup()
import trk_score_v01 as TS               # noqa: E402
GF = CC.GF; L = CC.L
K = 20
SEED_TWIN = 20261931
LOCK_A11 = CC.V13 / 'LOCK_A11.txt'
B2DIR = CC.WORK / 'B_retrack' / 'out' / 'retrack_fresh' / 'B2'
MANIFEST = CC.WORK / 'locks' / 'FREEZE_B_add7.json'
MANIFEST_SHA = 'd06cc48bbe89ec87b3927c962c041b31b5e7aab1dccbe570188a331e0a7b0c12'
OUTD = HERE / 'out'

ap = argparse.ArgumentParser()
ap.add_argument('--test-old', action='store_true'); ap.add_argument('--intervals', required=True, choices=('calibrated', 'nominal95', 'nominal99'))
ap.add_argument('--calib', choices=('local', 'export', 'import'), default='export'); ap.add_argument('--nboot', type=int, default=CC.NBOOT)
ap.add_argument('--outer', type=int, default=CC.N_OUTER)
args = ap.parse_args()
CC.N_OUTER = args.outer; CC.CALIB_MODE = args.calib
if args.test_old:
    CC.CALIB_DIR = OUTD / 'calib_testold'; gate = 'TEST_OLD: old evaluation runs only; no fresh value'
else:
    if not LOCK_A11.is_file(): raise SystemExit('REFUSED: LOCK_A11.txt does not exist; no Y value may be computed (A11 sec. 6b)')
    gate = 'LOCK_A11 sha256 ' + CC.sha(LOCK_A11)
    if args.nboot != CC.NBOOT or args.outer != CC.N_OUTER or args.intervals == 'nominal95':
        raise SystemExit('REFUSED: --nboot, --outer and nominal95 are test options (--test-old only)')
t00 = time.time()
log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)
PEND = args.intervals == 'calibrated' and args.calib == 'export'
OUTF = OUTD / (('TESTOLD_' if args.test_old else '') + 'Y_TWIN_v13' + (f'_b{args.nboot}' if args.nboot != CC.NBOOT else '') + ('_PENDING_CALIB' if PEND else '') + '.json')
if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)


def run_dict(rid, z):
    ev = z['evaluated'].astype(bool)
    return dict(run=rid, desired=float(json.loads(str(z['meta']))['desired']), idx55=z['idx55'].astype(np.int64), clear1=L.clean_clear(z['clear']),
                vbar=z['vbar'], ev=ev, masks=(ev,), sel={}, late={},
                crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float)})


def load_b2(rids):
    if CC.sha(MANIFEST) != MANIFEST_SHA: raise SystemExit('REFUSED: FREEZE_B_add7.json differs')
    man = {pathlib.PureWindowsPath(e['path']).name: e['sha256'] for e in json.loads(MANIFEST.read_text(encoding='utf-8'))['arrays_B2_fresh']}
    runs = []
    for rid in rids:
        f = B2DIR / (rid + '_arrays.npz')
        if CC.sha(f) != man[f.name]: raise SystemExit('REFUSED: %s differs from FREEZE_B_add7' % f.name)
        runs.append(run_dict(rid, np.load(f, allow_pickle=False)))
    return runs


def load_cv0(rids):
    return [run_dict(rid, np.load(CC.ARR / 'CV0' / (rid + '.npz'), allow_pickle=False)) for rid in rids]


def factors(r):
    cF, cN = r['crit']['F0'], r['crit']['N']
    with np.errstate(divide='ignore', invalid='ignore'):
        ok = np.isfinite(cF) & np.isfinite(cN) & (cF > 0) & (cN > 0)
        rat = np.where(ok, np.sqrt(np.where(ok, cF, 1.) / np.where(ok, cN, 1.)), np.nan)
    has = ok.any(axis=1)
    f = np.full(cF.shape[0], np.nan)
    if has.any(): f[has] = np.nanmedian(rat[has], axis=1)
    return f, has


def twin_crit(r, fa, mask):
    c = r['crit']['N'].copy()
    c[mask] = r['crit']['F0'][mask] / (fa[mask] ** 2)[:, None]
    return c


def build(runs):
    """Adds 'Ts' (scaled twin) and 'Tp1'..'TpK' (permuted twins) to every run's crit; returns the names and the factor count."""
    rng = np.random.default_rng(SEED_TWIN)
    fs = [factors(r) for r in runs]
    for r, (f, has) in zip(runs, fs): r['crit']['Ts'] = twin_crit(r, f, has)
    for k in range(1, K + 1):
        for r, (f, has) in zip(runs, fs):
            J = np.flatnonzero(r['ev'] & has)
            perm = rng.permutation(J.size)
            fk = f.copy(); fk[J] = f[J][perm]
            m = np.zeros(f.size, bool); m[J] = True
            r['crit']['Tp%d' % k] = twin_crit(r, fk, m)
    return ['F0', 'E', 'N', 'Ts'] + ['Tp%d' % k for k in range(1, K + 1)], int(sum((r['ev'] & h).sum() for r, (f, h) in zip(runs, fs)))


class YStat:
    """Delta = RR_gl(N) - mean_k RR_gl(Tp_k) (NaN where D_gl(E) <= 0). save() writes a kind-'Y' job for y_calib_remote_v13.py."""

    def __init__(self, P):
        self.P = P; self.tw = [a for a in P.names if a.startswith('Tp')]

    def __call__(self, Wr):
        e = GF.evaluate(self.P, Wr); den = e['denE']; ok = np.isfinite(den) & (den > 0)
        with np.errstate(divide='ignore', invalid='ignore'):
            rn = np.where(ok, e['D']['N'] / den, np.nan)
            rp = np.mean(np.stack([np.where(ok, e['D'][a] / den, np.nan) for a in self.tw]), axis=0)
        return (rn - rp)[:, None]

    def save(self, path):
        P = self.P
        np.savez_compressed(path, kind='Y', names=np.array(P.names), pop=P.pop, T0=np.stack(P.T0), d=P.d, ri=P.ri, keep=P.keep,
                            ev_off=P.ev_off, keep_off=P.keep_off, twins=json.dumps(self.tw))


def analyse(runs, W, label, calibrate):
    names, nfac = build(runs)
    G = TS.gridless(runs, names)
    pt = TS.rr_gl(G, 'F0', 'E', names[2:], pop=0)
    P = CC.prep(G, names, 0)
    NR = len(runs); Wfull = np.ones((1, NR))
    chk = CC.evaluate(P, Wfull)
    assert chk['denE'][0] == pt['denE'] and all(chk['D'][a][0] == pt['D'][a] for a in names[2:]), 'gl_fast differs from the library'
    B = CC.evaluate(P, W)
    den = B['denE']; ok = den > 0; tw = names[4:]
    with np.errstate(divide='ignore', invalid='ignore'):
        rr = {a: np.where(ok, B['D'][a] / den, np.nan) for a in names[2:]}
        rp = np.mean(np.stack([rr[a] for a in tw]), axis=0)
    ptrr = {a: pt['RR'][a] for a in names[2:]}; ptp = float(np.mean([ptrr[a] for a in tw]))
    d95 = dict(RR_N=CC.interval(rr['N'], ptrr['N'], 0.95), RR_s=CC.interval(rr['Ts'], ptrr['Ts'], 0.95), RR_p=CC.interval(rp, ptp, 0.95),
               delta_s=CC.interval(rr['Ts'] - rp, ptrr['Ts'] - ptp, 0.95), delta=CC.interval(rr['N'] - rp, ptrr['N'] - ptp, 0.95))
    out = dict(label=label, n_runs=NR, n_dec=int(pt['n']), n_factor=nfac, R_pp=pt['R_pp'], R_deceq=pt['R_deceq'], share_pos=float(np.mean(ok)),
               points=dict(RR_N=ptrr['N'], RR_s=ptrr['Ts'], RR_p=ptp, RR_p_each=[ptrr[a] for a in tw], delta=ptrr['N'] - ptp, delta_s=ptrr['Ts'] - ptp),
               nominal95=d95)
    if calibrate:
        st = YStat(P); full = st(Wfull)[0]; boot = st(W)[:, 0]
        assert full[0] == out['points']['delta'] or (np.isnan(full[0]) and np.isnan(out['points']['delta']))
        if args.intervals == 'calibrated':
            cal = CC.calibrate_all(st, NR, full, ['delta'], log=log, label='y_main' if not args.test_old else 'y_main_testold')
        else:
            cal = {'delta': dict(level=0.95 if args.intervals == 'nominal95' else 0.99, rule=args.intervals + ' (no double bootstrap)')}
        out['delta_main'] = CC.interval(boot, float(full[0]), cal['delta']['level']); out['calibration'] = cal
    return out


if args.test_old:
    old = CC.load_old_lead()
    runs = [dict(run=r['run'], desired=r['desired'], idx55=r['idx55'], clear1=r['clear1'], vbar=r['vbar'], ev=r['ev'], masks=(r['ev'],), sel={}, late={},
                 crit={a: r['crit'][a] for a in ('F0', 'E', 'N')}) for r in old]
    W = CC.counts(len(runs), args.nboot, CC.SEED_BOOT)
    b2 = None; ref = analyse(runs, W, 'reference (online N; old evaluation runs)', calibrate=True)
    run_ids = [r['run'] for r in runs]
else:
    run_ids = CC.c_run_ids('lead_braking'); assert len(run_ids) == 105
    W = CC.counts(len(run_ids), args.nboot, CC.SEED_BOOT)
    b2 = analyse(load_b2(run_ids), W, 'B2 (adaptive filter)', calibrate=True)
    log('B2 done')
    ref = analyse(load_cv0(run_ids), W, 'reference (online N of record)', calibrate=False)
log('reference done')


def _f(x):
    return None if x is None or not np.isfinite(x) else float(x)


def _ci(s):
    c = s['ci_level']; return None if not (np.isfinite(c[0]) and np.isfinite(c[1])) else [float(c[0]), float(c[1])]


V = {}
if b2 is not None:
    V['Y.n_runs'] = b2['n_runs']; V['Y.n_dec'] = b2['n_dec']; V['Y.n_factor'] = b2['n_factor']; V['Y.share_pos'] = b2['share_pos']; V['Y.R'] = _f(b2['R_pp'])
    V['Y.delta'] = _f(b2['points']['delta']); V['Y.delta.ci'] = _ci(b2['delta_main']); V['Y.delta.level'] = float(b2['delta_main']['level'])
    V['Y.Y1'] = bool(b2['delta_main']['ci_level'][0] > 0)
    for k, s in (('RR_NB2', 'RR_N'), ('RR_B2s', 'RR_s'), ('RR_B2p', 'RR_p'), ('delta_s', 'delta_s')):
        V['Y.' + k] = _f(b2['nominal95'][s]['point']); V['Y.%s.ci' % k] = _ci(b2['nominal95'][s]); V['Y.%s.level' % k] = 0.95
V['Y.n_factor_ref'] = ref['n_factor']; V['Y.ref.R'] = _f(ref['R_pp'])
for k, s in (('RR_N', 'RR_N'), ('RR_Ns', 'RR_s'), ('RR_Np', 'RR_p'), ('delta', 'delta'), ('delta_s', 'delta_s')):
    V['Y.ref.' + k] = _f(ref['nominal95'][s]['point']); V['Y.ref.%s.ci' % k] = _ci(ref['nominal95'][s]); V['Y.ref.%s.level' % k] = 0.95
doc = dict(code='y_twin_v13.py', amendment='AMENDMENT_11_v13.md sec. 6b (Y)', gate=gate, runs=run_ids, test_old=args.test_old, K=K, seed_twins=SEED_TWIN,
           draw='default_rng(%d), %d run resamples' % (CC.SEED_BOOT, args.nboot), intervals=args.intervals, pending_calibration=PEND,
           B2=b2, reference=ref, values=V, seconds=time.time() - t00, written=time.strftime('%Y-%m-%d %H:%M:%S'),
           code_sha256={str(f.relative_to(CD)): CC.sha(f) for f in (HERE / 'y_twin_v13.py', CD / 'analysis' / 'cd_common_v13.py', CD / 'analysis' / 'gl_fast_v13.py')})
OUTD.mkdir(exist_ok=True)
CC.write_once(OUTF, doc)
log('written %s; %s' % (OUTF.name, {k: V[k] for k in ('Y.Y1', 'Y.delta', 'Y.ref.delta') if k in V}))
