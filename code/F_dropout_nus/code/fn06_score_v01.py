"""AMENDMENT_12 sec. 5b: the decision test under injected detection dropouts on the nuScenes val logs (T1 = CANMOT through the
project's OnlineTracker, masks by the AMENDMENT_11 sec. 6c law with the scene name as case id, punish_num = 3). New file,
22 Nov 2026 (Claude Opus 5.5, worker of package F). Machinery copied from work\\F_nuscenes\\code\\f06_score_v01.py (frozen;
unchanged there): load_runs (with F's clearance under the departure, cache\\clear_v02, and its decision-tick check), boot_counts,
Evaluator / verify (f06k_kernel_v01, unchanged copy, checked against trk_score_v01.rr_gl on the first 25 resamples, relative 1e-9),
cover_two, calibrate, the double bootstrap and the level rule of finish() (A10 sec. 2.6), all with F's seeds.

Run unit = scene (the 150 val scenes, sorted names). Horizon 3 s (F's frozen horizon). Population 0 = all evaluated decisions
(primary); population 1 = evaluated decisions whose keyframe is masked ("in dropout", descriptive).
Sources: F0 = cF0 of the masked arrays, i.e. the T1 class average P-bar of record from the train scenes, UNMASKED tracks
(F_nuscenes\\out\\PBAR_T1_train_v01.json); E = cE (true error); N = cN (the masked tracker's own covariance);
E5_N (A10 sec. 2.2, amplitude-matched ranking oracle with N's own amplitude): m and A from trk_score_v01.ratio_summary of the
N/F0 margin ratios sqrt(cF0 / cN) of the evaluated decisions; u from trk_score_v01.e5_u(F0, E); E5x = add_oracle(F0, m, A, u);
E5xp = the same with u permuted within scenes (trk_score_v01.permute_u, default_rng(20261915)).
Statistics (population 0): R = R_gl = denE / 201; c = RR_gl(E5x); cdiff = RR_gl(E5x) - RR_gl(E5xp); r = RR_gl(N).
Scene bootstrap: default_rng(20261923).integers(0, 150, (20000, 150)) as counts. Calibration (A10 sec. 2.6, F's f06 heldout):
outer default_rng(20261912) 2,000; inner one stream default_rng(20261913) 1,000 per outer sample in order; the second inner stream
default_rng(20261914) only when some statistic's nominal-95% coverage is below 0.94; Monte Carlo SD from default_rng(20261920).
Sequence (one-sided 0.025 = the lower end of the calibrated two-sided interval):
  1. room: R's lower end > 0;
  2. E5_N: the lower ends of c and of cdiff > 0;
  3. N's class by A10 H3's rule (delta = 0.05): r's lower end > 0 -> recovers; else c's lower end > delta -> uninformative
     variation; else c's interval inside (-delta, delta) -> amplitude-limited; else inconclusive.
  A step is confirmatory only when every earlier step passed. Holm p-value of r: (1 + #{r* <= 0, NaN counted}) / 20,001.
Descriptive: decisions in dropout and their share; the masked share of keyframes; R, RR(N), c in population 1 (95% percentile
intervals); the N/F0 ratio summary in dropout.
Modes (the val split of the masked set is refused until LOCK_A12c.txt exists):
  prep SET SPLIT [--threads N] [--nboot N]   loads, checks, single bootstrap, descriptives; writes OUTDIR\\partial.json / .npz and
                                             the calibration job OUTDIR\\calib_job.npz (+ .meta.json)
  calib SET SPLIT --seed S [--threads N] [--outer N --inner N]   the double bootstrap of one inner seed -> OUTDIR\\calib_<S>.npz
  finish SET SPLIT                           calibration, sequence, p-value -> OUTDIR\\FN5B_RESULTS_v01.json
OUTDIR = out\\<set>_<split>. Sizes other than F's (20,000 / 2,000 / 1,000) are allowed only on the design split (code tests).
Usage: python -I fn06_score_v01.py prep|calib|finish masked val|train [options]
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fn_common_v01 as FC                   # noqa: E402  (before numpy)
import json, time                            # noqa: E402
import numpy as np                           # noqa: E402

SHARED = FC.WORK / 'shared' / 'trackers'
sys.path.insert(0, str(SHARED))
import trk_score_v01 as TS                   # noqa: E402
import f06k_kernel_v01 as K                  # noqa: E402  (numba)
import dr_masks_v02 as M                     # noqa: E402
L = TS.L

NLEV = L.NLEV
SEED_F = 20261923
DELTA = 0.05
SEED_OUT, SEED_IN, SEED_IN2, SEED_MC = 20261912, 20261913, 20261914, 20261920
NOMINALS = np.round(np.arange(0.950, 0.99951, 0.0005), 4)
STATS = ('R', 'c', 'cdiff', 'r')
ROLES = ['F0', 'E', 'N', 'E5x', 'E5xp']
ROLES1 = ['F0', 'E', 'N', 'E5x']
HZ = 3
INDEP_EXACT = ('sweep', 'kf', 'now', 'age', 'idx55', 'evaluated', 'evaluated2', 'inpath', 'n_truth')
INDEP_FLOAT = ('vbar', 'v0', 'des', 'clear', 'clear2')   # last-bit platform differences (acceptance 2): equal NaN pattern, |d| <= 1e-9
TOL_INDEP = 1e-9

argv = sys.argv[1:]
MODE, SET, SPLIT = argv[0], argv[1], argv[2]


def opt(name, default, typ=int):
    return typ(argv[argv.index(name) + 1]) if name in argv else default


NBOOT = opt('--nboot', 20000)
B_OUT = opt('--outer', 2000)
B_IN = opt('--inner', 1000)
THREADS = opt('--threads', 0)
if SET not in ('masked', 'accept'):
    raise SystemExit('set?')
if SET == 'masked':
    FC.require_masked(SPLIT)
else:
    FC.require_split(SPLIT)
if SPLIT == 'val' and (NBOOT, B_OUT, B_IN) != (20000, 2000, 1000):
    raise SystemExit('REFUSED: the val run uses F\'s sizes (20,000 / 2,000 / 1,000)')
OUTDIR = FC.OUT / ('%s_%s' % (SET, SPLIT))
OUTDIR.mkdir(parents=True, exist_ok=True)
if THREADS:
    import numba
    numba.set_num_threads(THREADS)
T00 = time.time()


def log(s):
    print('[%6.0f s] %s' % (time.time() - T00, s), flush=True)


# ------------------------------------------------------------------------------------------------ runs (f06 load_runs + masks)
def scene_list():
    if SPLIT == 'val':
        return sorted(FC.splits()['val'])
    have = sorted(p.stem for p in (FC.CACHE / ('arrays_' + SET) / SPLIT).glob('scene-*.npz') if '.tmp' not in p.name)
    if not have:
        raise SystemExit('no arrays')
    return have


def load_runs():
    runs = []; chk = dict(indep_keys_equal_F=0, indep_checked=0, masks_identical=True, ticks_match=True, indep_float_max_abs={})
    for nm in scene_list():
        z = np.load(FC.CACHE / ('arrays_' + SET) / SPLIT / (nm + '.npz'), allow_pickle=False)
        meta = json.loads(str(z['meta']))
        ev = z['evaluated'].astype(bool)
        clear = z['clear']
        c2 = np.load(FC.SRC_CACHE / 'clear_v02' / SPLIT / (nm + '.npz'), allow_pickle=False)
        if not np.array_equal(c2['sweep'], z['sweep']) or not np.array_equal(np.isnan(c2['clear']), np.isnan(clear)):
            chk['ticks_match'] = False
            raise RuntimeError('clear_v02 does not match the arrays of %s' % nm)
        tr = np.load(FC.CACHE / ('tracks_' + SET) / SPLIT / (nm + '.npz'), allow_pickle=False)
        tm = json.loads(str(tr['meta']))
        n_kf = int(len(np.load(FC.SRC_CACHE / SPLIT / (nm + '.npz'), allow_pickle=False)['kf_t']))
        masked = M.mask(nm, n_kf) if SET == 'masked' else []
        if tm['n_kf'] != n_kf or list(tm['masked_kf']) != masked or tm['punish_num'] != (FC.PUNISH_5B if SET == 'masked' else 1):
            chk['masks_identical'] = False
            raise RuntimeError('masks or punish_num of %s differ from the law' % nm)
        fa = FC.SRC_CACHE / 'arrays_T1' / SPLIT / (nm + '.npz')
        if fa.is_file():
            fz = np.load(fa, allow_pickle=False)
            chk['indep_checked'] += 1
            ok = all(np.array_equal(fz[k], z[k], equal_nan=(fz[k].dtype.kind == 'f')) for k in INDEP_EXACT)
            for k in INDEP_FLOAT:
                x, y = np.asarray(fz[k], float), np.asarray(z[k], float)
                if x.shape != y.shape or not np.array_equal(np.isnan(x), np.isnan(y)):
                    ok = False; continue
                d = float(np.nanmax(np.abs(x - y))) if np.isfinite(x).any() else 0.
                chk['indep_float_max_abs'][k] = max(chk['indep_float_max_abs'].get(k, 0.), d)
                ok = ok and d <= TOL_INDEP
            if ok:
                chk['indep_keys_equal_F'] += 1
            else:
                raise RuntimeError('tracker-independent keys of %s differ from F\'s arrays' % nm)
        dr = np.isin(z['kf'], masked)
        runs.append(dict(run=nm, desired=float(meta['desired']), idx55=z['idx55'].astype(np.int64), clear1=L.clean_clear(c2['clear']),
                         vbar=z['vbar'], masks=(ev, ev & dr), ev=ev, n_dec=int(ev.size), dr=dr, n_kf=n_kf, n_masked=len(masked),
                         crit={k: np.asarray(z['c' + k], float) for k in ('F0', 'E', 'N')}, sel={}, late={}))
    return runs, chk


def boot_counts(n, nboot, seed):
    return counts_of(np.random.default_rng(seed).integers(0, n, (nboot, n)), n)


def counts_of(idx, n):
    """Per-resample scene counts (float64); the same values as f06's row-by-row bincount."""
    B = idx.shape[0]
    flat = (idx + n * np.arange(B)[:, None]).ravel()
    return np.bincount(flat, minlength=B * n).reshape(B, n).astype(np.float64)


class Evaluator:
    def __init__(self, G, roles, pop):
        self.roles = list(roles); self.pop = pop
        self.args = K.pack([G[k] for k in self.roles], pop)

    def run(self, W):
        o = K.eval_many(np.ascontiguousarray(W, dtype=np.float64), *self.args)
        return dict(n=o[:, 0], denE=o[:, 1], D={a: o[:, i] for i, a in enumerate(self.roles) if i >= 2})


def verify(G, ev, W):
    worst = 0.; names = ev.roles[2:]
    fb = ev.run(W)
    for b in range(W.shape[0]):
        ref = TS.rr_gl(G, ev.roles[0], ev.roles[1], names, ev.pop, W[b])
        pairs = [(ref['denE'], fb['denE'][b]), (ref['n'], fb['n'][b])] + [(ref['D'][a], fb['D'][a][b]) for a in names]
        for x, y in pairs:
            if np.isnan(x) and np.isnan(y):
                continue
            worst = max(worst, abs(x - y) / max(abs(x), abs(y), 1e-12))
    return dict(max_rel=float(worst), n=int(W.shape[0]), roles=ev.roles, pop=ev.pop)


def rr_of(D, den):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(np.isfinite(den) & (den > 0), D / den, np.nan)


def stats_of(o):
    """Columns R, c, cdiff, r from an Evaluator output of ROLES (population 0)."""
    den = o['denE']
    c = rr_of(o['D']['E5x'], den); cp = rr_of(o['D']['E5xp'], den)
    return np.column_stack([den / NLEV, c, c - cp, rr_of(o['D']['N'], den)])


def stats_from_args(args):
    def f(W):
        o = K.eval_many(np.ascontiguousarray(W, dtype=np.float64), *args)
        return stats_of(dict(n=o[:, 0], denE=o[:, 1], D={a: o[:, i] for i, a in enumerate(ROLES) if i >= 2}))
    return f


def pct_level(b, level):
    b = np.asarray(b, float); f = np.isfinite(b)
    a = (1. - level) / 2.
    return [float(x) for x in np.percentile(b[f], [100. * a, 100. * (1. - a)])] if f.any() else [np.nan, np.nan]


def summ(b, pt):
    b = np.asarray(b, float)
    return dict(point=float(pt), ci95=pct_level(b, 0.95), ci99=pct_level(b, 0.99), n_finite=int(np.isfinite(b).sum()))


# ------------------------------------------------------------------------------------------------ prep
def prep():
    outj = OUTDIR / 'partial.json'
    if outj.exists():
        raise SystemExit('REFUSED: %s exists' % outj)
    runs, chk = load_runs()
    n = len(runs)
    log('runs %d (%s %s); checks %s' % (n, SET, SPLIT, chk))
    rs = TS.ratio_summary(TS.margin_ratios(runs, 'N', 'F0'))
    u, uinfo = TS.e5_u(runs, 'F0', 'E')
    TS.add_oracle(runs, 'E5x', 'F0', rs['median'], rs['A'], u)
    TS.add_oracle(runs, 'E5xp', 'F0', rs['median'], rs['A'], TS.permute_u(runs, u, seed=TS.SEED_PERM))
    G = TS.gridless(runs, ROLES)
    log('gridless events built')
    CNT = boot_counts(n, NBOOT, SEED_F)
    E0 = Evaluator(G, ROLES, 0)
    vers = [verify(G, E0, CNT[:25])]
    n_in = int(sum((r['ev'] & r['dr']).sum() for r in runs))
    E1 = Evaluator(G, ROLES1, 1) if n_in else None
    if E1 is not None:
        vers.append(verify(G, E1, CNT[:25]))
    if max(v['max_rel'] for v in vers) > 1e-9:
        raise RuntimeError('fast evaluator differs from the reference: %s' % vers)
    log('fast evaluator verified %s' % [v['max_rel'] for v in vers])
    pt = TS.rr_gl(G, 'F0', 'E', ROLES[2:], 0)
    o0 = E0.run(np.ones((1, n))); S0 = stats_of(o0)[0]
    ref = [pt['R_pp'], pt['RR']['E5x'], pt['RR']['E5x'] - pt['RR']['E5xp'], pt['RR']['N']]
    for x, y in zip(S0, ref):
        if not ((np.isnan(x) and np.isnan(y)) or abs(x - y) <= 1e-12 * max(abs(x), abs(y), 1.)):
            raise RuntimeError('full-sample values differ from the library: %s %s' % (S0, ref))
    ob = E0.run(CNT); S = stats_of(ob)
    log('single bootstrap done')
    doc = dict(code='fn06_score_v01.py', amendment='AMENDMENT_12 sec. 5b', set=SET, split=SPLIT, horizon_s=HZ, n_scenes=n,
               scenes=[r['run'] for r in runs], checks=chk, verify=vers, nboot=NBOOT, n_outer=B_OUT, n_inner=B_IN,
               draw='default_rng(%d).integers(0, %d, (%d, %d)) as counts' % (SEED_F, n, NBOOT, n), delta=DELTA,
               punish_num=FC.PUNISH_5B if SET == 'masked' else 1, mask_law='AMENDMENT_11 sec. 6c, dr_masks_v02.mask(scene name, n keyframes)',
               F0=dict(file='work\\F_nuscenes\\out\\PBAR_T1_train_v01.json', sha256=FC.sha256_file(FC.PBAR_FILE),
                       note='class average of record from the train scenes, UNMASKED tracks'),
               clearance='F departure (cache\\clear_v02), decision ticks checked equal',
               ratio_summary_N_F0=rs, E5x=dict(m=rs.get('median'), A=rs.get('A')), e5_u=uinfo, perm_seed=TS.SEED_PERM)
    doc['full'] = dict(zip(STATS, [float(x) for x in S0]))
    doc['library_point'] = dict(R_pp=pt['R_pp'], R_deceq=pt['R_deceq'], n=pt['n'], RR=pt['RR'], D_deceq=pt['D_deceq'])
    doc['boot95'] = {s: summ(S[:, j], S0[j]) for j, s in enumerate(STATS)}
    doc['share_R_nonpositive'] = float(np.mean(~(S[:, 0] > 0)))
    doc['p_r'] = float((1 + np.sum(~(S[:, 3] > 0))) / (S.shape[0] + 1))
    doc['R_deceq_ci95'] = L.pct(L.dec_eq(ob['denE'], ob['n']))
    doc['D_N_deceq'] = dict(point=pt['D_deceq']['N'], ci95=L.pct(L.dec_eq(ob['D']['N'], ob['n'])))
    # ---- descriptive
    ev_all = np.concatenate([r['ev'] for r in runs]); dr_all = np.concatenate([r['dr'] for r in runs])
    desc = dict(n_evaluated=int(ev_all.sum()), n_in_dropout=n_in, share_evaluated_in_dropout=float(n_in / max(ev_all.sum(), 1)),
                n_decisions_built=int(ev_all.size), n_built_in_dropout=int(dr_all.sum()),
                keyframes=int(sum(r['n_kf'] for r in runs)), keyframes_masked=int(sum(r['n_masked'] for r in runs)))
    desc['masked_share_keyframes'] = desc['keyframes_masked'] / max(desc['keyframes'], 1)
    if E1 is not None:
        p1 = TS.rr_gl(G, 'F0', 'E', ROLES1[2:], 1)
        o1 = E1.run(CNT); f1 = E1.run(np.ones((1, n)))
        b1 = dict(R=o1['denE'] / NLEV, RR_N=rr_of(o1['D']['N'], o1['denE']), c=rr_of(o1['D']['E5x'], o1['denE']))
        fp = dict(R=float(f1['denE'][0] / NLEV), RR_N=float(rr_of(f1['D']['N'], f1['denE'])[0]), c=float(rr_of(f1['D']['E5x'], f1['denE'])[0]))
        desc['in_dropout'] = dict(n=p1['n'], R_pp=p1['R_pp'], R_deceq=p1['R_deceq'], RR=p1['RR'],
                                  **{k: summ(b1[k], fp[k]) for k in ('R', 'RR_N', 'c')})
        mr = []
        for r in runs:
            sel = r['ev'] & r['dr']
            ca = r['crit']['N'][sel]; cb = r['crit']['F0'][sel]
            ok = np.isfinite(ca) & np.isfinite(cb) & (ca > 0) & (cb > 0); mr.append(np.sqrt(cb[ok] / ca[ok]))
        desc['ratio_summary_in_dropout'] = TS.ratio_summary(np.concatenate(mr) if mr else np.zeros(0))
    doc['descriptive'] = desc
    # ---- calibration job (the packed inputs of E0, as f06 export_job)
    jf = OUTDIR / 'calib_job.npz'
    np.savez(jf, kind='FN5B', **{'a_%d' % i: x for i, x in enumerate(E0.args)})
    meta = dict(n_run=n, full=[float(x) for x in S0], stats=list(STATS), n_outer=B_OUT, n_inner=B_IN, seed_outer=SEED_OUT,
                seeds_inner=[SEED_IN, SEED_IN2], nlev=NLEV, roles=ROLES, job_sha256=FC.sha256_file(jf), written=FC.clock())
    (OUTDIR / 'calib_job.meta.json').write_text(FC.jdump(meta), encoding='utf-8')
    np.savez(OUTDIR / 'partial.npz', S=S, S0=S0)
    doc['seconds_prep'] = round(time.time() - T00, 1); doc['written_prep'] = FC.clock()
    outj.write_text(FC.jdump(doc), encoding='utf-8')
    log('WROTE %s full %s' % (outj, doc['full']))


# ------------------------------------------------------------------------------------------------ calib (one inner seed)
def calib():
    seed = opt('--seed', SEED_IN)
    outf = OUTDIR / ('calib_%d.npz' % seed)
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    meta = json.loads((OUTDIR / 'calib_job.meta.json').read_text(encoding='utf-8'))
    jf = OUTDIR / 'calib_job.npz'
    if FC.sha256_file(jf) != meta['job_sha256']:
        raise RuntimeError('job file changed')
    z = np.load(jf, allow_pickle=False)
    args = tuple(z['a_%d' % i] for i in range(5))
    stat = stats_from_args(args)
    n = int(meta['n_run']); full_meta = np.asarray(meta['full'], float)
    full = stat(np.ones((1, n)))[0]
    reproduced = np.array([bool(a == b or (np.isnan(a) and np.isnan(b))) for a, b in zip(full, full_meta)])
    IDX_O = np.random.default_rng(SEED_OUT).integers(0, n, (B_OUT, n))
    rng_i = np.random.default_rng(seed)
    k = full.size
    p_lt = np.full((B_OUT, k), np.nan); p_le = np.full((B_OUT, k), np.nan)
    for b in range(B_OUT):
        ii = rng_i.integers(0, n, (B_IN, n))
        Sb = stat(counts_of(IDX_O[b][ii], n))
        for j in range(k):
            v = Sb[:, j]; v = v[np.isfinite(v)]
            if v.size and np.isfinite(full[j]):
                p_lt[b, j] = (v < full[j]).mean(); p_le[b, j] = (v <= full[j]).mean()
        if (b + 1) % 100 == 0:
            log('seed %d: outer %d / %d' % (seed, b + 1, B_OUT))
    import numba, platform
    np.savez(outf, p_lt=p_lt, p_le=p_le, full=full, full_reproduced=reproduced, seed=seed, job_sha256=meta['job_sha256'],
             platform=platform.platform(), threads=numba.get_num_threads(), seconds=time.time() - T00)
    log('WROTE %s' % outf)


# ------------------------------------------------------------------------------------------------ finish (f06 finish's rule)
def cover_two(lt, le, nom):
    a = 1. - nom
    ok = np.isfinite(lt)
    return float(((le[ok] >= a / 2. - 1e-12) & (lt[ok] <= 1. - a / 2. + 1e-12)).mean())


def calibrate(lt, le):
    if cover_two(lt, le, 0.95) >= 0.94:
        return 0.95
    for nm in NOMINALS:
        if cover_two(lt, le, nm) >= 0.95:
            return float(nm)
    return None


def finish():
    outf = OUTDIR / 'FN5B_RESULTS_v01.json'
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    doc = json.loads((OUTDIR / 'partial.json').read_text(encoding='utf-8'))
    zp = np.load(OUTDIR / 'partial.npz', allow_pickle=False); S = zp['S']; S0 = zp['S0']
    meta = json.loads((OUTDIR / 'calib_job.meta.json').read_text(encoding='utf-8'))
    runs_db = {}; pods = {}
    for seed in (SEED_IN, SEED_IN2):
        p = OUTDIR / ('calib_%d.npz' % seed)
        if not p.exists():
            continue
        r = np.load(p, allow_pickle=False)
        if str(r['job_sha256']) != meta['job_sha256'] or not bool(np.all(r['full_reproduced'])) or not np.array_equal(r['full'], S0, equal_nan=True):
            raise RuntimeError('calibration result %s: wrong job or full-sample values not reproduced exactly' % p.name)
        runs_db[seed] = (r['p_lt'], r['p_le'])
        pods[seed] = dict(file=p.name, sha256=FC.sha256_file(p), platform=str(r['platform']), seconds=float(r['seconds']),
                          threads=int(r['threads']))
    if SEED_IN not in runs_db:
        raise RuntimeError('the first inner seed result is missing')
    need2 = [s for j, s in enumerate(STATS) if cover_two(runs_db[SEED_IN][0][:, j], runs_db[SEED_IN][1][:, j], 0.95) < 0.94]
    doc['second_inner_seed'] = dict(needed=need2, present=SEED_IN2 in runs_db)
    if need2 and SEED_IN2 not in runs_db:
        raise SystemExit('NEED_SECOND_SEED %s' % need2)
    if not need2:
        runs_db.pop(SEED_IN2, None)
    doc['calib_runs'] = pods
    IDX_MC = np.random.default_rng(SEED_MC).integers(0, B_OUT, (2000, B_OUT))
    cal = {}
    for j, s in enumerate(STATS):
        lt, le = runs_db[SEED_IN]
        c1 = calibrate(lt[:, j], le[:, j])
        c2 = calibrate(*[x[:, j] for x in runs_db[SEED_IN2]]) if SEED_IN2 in runs_db else None
        mc = np.array([np.nan if (x := calibrate(lt[ix, j], le[ix, j])) is None else x for ix in IDX_MC])
        sd = float(np.nanstd(mc, ddof=1)) if np.isfinite(mc).sum() > 1 else np.nan
        cov95 = cover_two(lt[:, j], le[:, j], 0.95)
        if c1 is not None and c1 == 0.95:
            level, why = 0.95, 'coverage of the nominal 95%% interval %.4f >= 0.94' % cov95
        elif c1 is not None and c2 is not None and np.isfinite(sd) and sd <= 0.002 and abs(c1 - c2) <= 0.002 + 1e-12:
            level, why = c1, 'calibrated (MC SD %.4f, second inner seed %.4f)' % (sd, c2)
        else:
            level, why = 0.99, 'nominal 99%% (calibration checks failed: level %s, second %s, MC SD %s)' % (c1, c2, sd)
        cal[s] = dict(level=level, reason=why, coverage_nominal95=cov95, calibrated_seed1=c1, calibrated_seed2=c2, mc_sd=sd,
                      ci=pct_level(S[:, j], level), point=float(S0[j]))
    doc['calibration'] = cal
    lo = lambda s: cal[s]['ci'][0]
    room = dict(passes=bool(lo('R') > 0), R_gl_pp=cal['R']['point'], R_lower=lo('R'), level=cal['R']['level'],
                share_resamples_R_nonpositive=doc['share_R_nonpositive'], rule="R_gl's lower end > 0")
    e5 = dict(passes=bool(lo('c') > 0 and lo('cdiff') > 0), c=cal['c']['point'], c_ci=cal['c']['ci'], cdiff=cal['cdiff']['point'],
              cdiff_ci=cal['cdiff']['ci'], rule='lower ends of RR_gl(E5_N) and RR_gl(E5_N) - RR_gl(E5p_N) > 0')
    clo, chi = cal['c']['ci']
    if lo('r') > 0: cls = 'recovers'
    elif clo > DELTA: cls = 'uninformative variation'
    elif clo > -DELTA and chi < DELTA: cls = 'amplitude-limited'
    else: cls = 'inconclusive'
    eff = None
    if cls == 'recovers':
        with np.errstate(divide='ignore', invalid='ignore'):
            eff = dict(point=float(S0[3] / S0[1]), ci=pct_level(S[:, 3] / S[:, 1], cal['r']['level']))
    klass = dict(classification=cls, passes=cls in ('recovers', 'uninformative variation', 'amplitude-limited'), r=cal['r']['point'],
                 r_ci=cal['r']['ci'], c_ci=cal['c']['ci'], delta=DELTA, barely_varies=doc['ratio_summary_N_F0'].get('barely_varies'),
                 efficiency_r_over_c=eff)
    conf = True
    for h in (room, e5, klass):
        h['confirmatory'] = bool(conf)
        h['status'] = 'confirmatory' if conf else 'not confirmatory (an earlier step did not pass)'
        conf = conf and h['passes']
    doc['sequence'] = dict(room=room, E5_N=e5, N_class=klass)
    doc['p_r_holm_input'] = dict(p=doc['p_r'], rule='(1 + #{r* <= 0, NaN counted}) / (20,000 + 1)')
    d = doc['descriptive']
    vals = {'N5b.n_scenes': doc['n_scenes'], 'N5b.n_dec': d['n_evaluated'], 'N5b.n_in_dropout': d['n_in_dropout'],
            'N5b.dec_in_share': d['share_evaluated_in_dropout'], 'N5b.masked_share': d['masked_share_keyframes'],
            'N5b.R_gl': cal['R']['point'], 'N5b.R_gl.ci': cal['R']['ci'], 'N5b.R_gl.level': cal['R']['level'],
            'N5b.R_gl.share_nonpos': doc['share_R_nonpositive'],
            'N5b.c': cal['c']['point'], 'N5b.c.ci': cal['c']['ci'], 'N5b.c.level': cal['c']['level'],
            'N5b.cdiff': cal['cdiff']['point'], 'N5b.cdiff.ci': cal['cdiff']['ci'], 'N5b.cdiff.level': cal['cdiff']['level'],
            'N5b.r': cal['r']['point'], 'N5b.r.ci': cal['r']['ci'], 'N5b.r.level': cal['r']['level'], 'N5b.p_r': doc['p_r'],
            'N5b.m': doc['E5x']['m'], 'N5b.A': doc['E5x']['A'], 'N5b.within5': doc['ratio_summary_N_F0'].get('share_within_5pct'),
            'N5b.room.passes': room['passes'], 'N5b.E5N.passes': e5['passes'], 'N5b.class': cls, 'N5b.class.passes': klass['passes'],
            'N5b.eff': eff['point'] if eff else None, 'N5b.eff.ci': eff['ci'] if eff else None,
            'N5b.R_deceq': doc['library_point']['R_deceq'], 'N5b.D_N_deceq': doc['D_N_deceq']['point']}
    if 'in_dropout' in d:
        di = d['in_dropout']
        vals.update({'N5b.in.R_gl': di['R']['point'], 'N5b.in.R_gl.ci': di['R']['ci95'], 'N5b.in.RR_N': di['RR_N']['point'],
                     'N5b.in.RR_N.ci': di['RR_N']['ci95'], 'N5b.in.c': di['c']['point'], 'N5b.in.c.ci': di['c']['ci95'],
                     'N5b.in.within5': d['ratio_summary_in_dropout'].get('share_within_5pct')})
    doc['values'] = vals
    doc['written'] = FC.clock(); doc['seconds_finish'] = round(time.time() - T00, 1)
    doc['code_sha256'] = FC.sha256_file(pathlib.Path(__file__))
    outf.write_text(FC.jdump(doc), encoding='utf-8')
    log('WROTE %s %s' % (outf, json.dumps(dict(room=room['passes'], E5_N=e5['passes'], cls=cls, p_r=doc['p_r']))))


if __name__ == '__main__':
    {'prep': prep, 'calib': calib, 'finish': finish}[MODE]()
