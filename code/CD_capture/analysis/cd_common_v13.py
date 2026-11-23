"""Revision v13, packages C and D: shared helpers for the analyses of AMENDMENT_10_v13 sec. 2, 5 and 6 (Claude Opus 5.5).

Reuses, imported read-only: the scoring library of record optA_lib_v02 (L), the v12 gridless code (a9_common_v01), the v11
loader rev_common_v01 (old evaluation runs: the H4 design set and the D1 matched settings), package B's frozen library
(work/shared/trackers: trk_score_v01, est_phase), and gl_fast_v13 (identical to the library; test_gl_fast_v13.py).

Lock gate: functions that read fresh-run arrays refuse unless revision_v13/LOCK_A10_2.txt exists (A10 sec. 4, 5.2), except in
--test-old mode, where every script runs on OLD runs (exploratory data of record) only to exercise the code.
"""
import hashlib, json, pathlib, sys, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
CD = HERE.parent
WORK = CD.parent
V13 = WORK.parent
LOCK2 = V13 / 'LOCK_A10_2.txt'
OUT = HERE / 'out'
ARR = CD / 'arrays'                 # arrays/<variant>/<run_id>.npz (c_extract_v13.py)
SHARED = WORK / 'shared' / 'trackers'
V12A = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis')
sys.dont_write_bytecode = True
for p in (str(HERE), str(V12A), str(SHARED)):
    if p not in sys.path: sys.path.insert(0, p)
import a9_common_v01 as A9           # noqa: E402
import gl_fast_v13 as GF             # noqa: E402
C11 = A9.C; L = A9.L

DELTA = 0.05                        # A10 sec. 2.7 / 0.2
RATIO = 1.1029                      # median N/F0 margin ratio of record (E5)
NBOOT = 20000
SEED_BOOT = 20261911                # fresh-run bootstrap
SEED_OUTER, SEED_INNER, SEED_INNER2, SEED_MC = 20261912, 20261913, 20261914, 20261920
N_OUTER, N_INNER, N_MC = 2000, 1000, 2000
SEED_PERM = 20261915
SEED_PARTIAL = 20261919
LEVEL_STEPS = np.round(np.arange(0.950, 0.99951, 0.0005), 4)
VMIN = 0.5


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()


def require_lock2(test_old):
    if test_old:
        return 'TEST_OLD: old runs only; no fresh value'
    if not LOCK2.is_file():
        raise SystemExit('REFUSED: LOCK_A10_2.txt does not exist; no value of a fresh run may be computed (A10 sec. 4, 5.2)')
    return 'LOCK_A10_2 sha256 ' + sha(LOCK2)


LOCK2C = V13 / 'LOCK_A10_2c.txt'       # second stage of the two-stage Lock 2 (coordinator, 20 Nov 01:53 EST; A10 sec. 11 departure)


def require_lock2c(test_old):
    """Gate for stage-2 programs (A10 sec. 5.7 additions, frozen in FREEZE_CD_2): no fresh C or D value before LOCK_A10_2c."""
    if test_old:
        return 'TEST_OLD: old runs only; no fresh value'
    if not (LOCK2.is_file() and LOCK2C.is_file()):
        raise SystemExit('REFUSED: LOCK_A10_2.txt and LOCK_A10_2c.txt must both exist before a stage-2 program reads a fresh run '
                         '(two-stage Lock 2, coordinator 20 Nov 01:53 EST)')
    return 'LOCK_A10_2 sha256 %s; LOCK_A10_2c sha256 %s' % (sha(LOCK2), sha(LOCK2C))


def write_once(path, doc):
    path = pathlib.Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists(): raise SystemExit('REFUSED: %s exists' % path)
    path.write_text(json.dumps(doc, indent=1, default=float, allow_nan=True), encoding='utf-8')


# ------------------------------------------------------------------------------------------------ run sets
def c_cases():
    d = json.loads((CD / 'CASES_C_v13.json').read_text(encoding='utf-8'))
    return d['cases']


def c_run_ids(family):
    """Run ids of package C for 'lead_braking' or 'cutin' (A10 5.1), with any reported replacement applied (REPLACEMENTS_C_v13.json)."""
    rep = {}
    rp = CD / 'REPLACEMENTS_C_v13.json'
    if rp.is_file(): rep = json.loads(rp.read_text(encoding='utf-8'))['replacements']
    ids = []
    for c in c_cases():
        if c['family'] == family:
            case = rep.get(c['case'], c['case'])
            ids.append(f'pc13_{case}_native')
    return sorted(ids)                    # run order of every resampling: ascending run id (CD_DEFINITIONS_v13.md)


def d1_run_ids(kind):
    d = json.loads((CD / 'd1' / 'CASES_D1_v13.json').read_text(encoding='utf-8'))
    rep = {}
    rp = CD / 'REPLACEMENTS_D1_v13.json'
    if rp.is_file(): rep = json.loads(rp.read_text(encoding='utf-8'))['replacements']
    return sorted(f"pd13_{rep.get(c['id'], c['id'])}_native" for c in d['cases'] if c['role'] == 'd1_openloop' and c['lead_variant']['kind'] == kind)


# ------------------------------------------------------------------------------------------------ runs from arrays
def masks_tracker_phase(ev, v0, eph):
    """Populations: all evaluated, ego moving, estimated phase 0 / 1 / 2 (A10 sec. 2.4: before braking, braking, stopped)."""
    return (ev, ev & (v0 > VMIN), ev & (eph == 0), ev & (eph == 1), ev & (eph == 2))


def load_variant(run_ids, variant, test_old=False, extra=None, thr=-1.0):
    """Runs (rev_common / trk_score format) from arrays/<variant>/<rid>.npz written by c_extract_v13.py.
    crit: F0, E, N, NA, A1 (AM), CK3, Q; TG (cTG2) when present. Masks by the tracker-estimated phase (thr = -1.0 primary)."""
    import trk_score_v01 as TS
    runs = []
    for rid in run_ids:
        z = np.load(ARR / variant / (rid + '.npz'), allow_pickle=False)
        meta = json.loads(str(z['meta']))
        if not test_old:
            assert meta.get('lead_variant') is None or rid.startswith('pd13_'), rid
        ev = z['evaluated'].astype(bool); v0 = z['v0']
        eph = TS.est_phase(z['vhat'], z['ahat_long'], z['lead_found'], thr)
        crit = {'F0': z['cF0'], 'E': z['cE'], 'N': z['cN'], 'NA': z['cNA'], 'A1': z['cA1'], 'CK3': z['cCK3'], 'Q': z['cQ']}
        if 'cTG2' in z.files: crit['TG'] = z['cTG2']
        r = dict(run=rid, desired=float(z['des'][0]), meta=meta, k=z['k'], ev=ev, v0=v0, eph=eph, ph=z['phase'], vbar=z['vbar'],
                 idx55=z['idx55'].astype(np.int64), clear_raw=z['clear'], clear1=L.clean_clear(z['clear']), masks=masks_tracker_phase(ev, v0, eph),
                 crit={a: np.asarray(v, float) for a, v in crit.items()}, sel={}, late={}, z=z)
        if 'clearR075' in z.files: r['clearR075'] = z['clearR075']
        runs.append(r)
    return runs


def load_old_lead():
    """The 35 old evaluation runs of record (rev_common_v01.load_runs) with the tracker-estimated phase from v12's lead-state
    extract (revision_v12/analysis/out/lead/<run>.npz) and TG (out/tg/<run>.npz, cTG2) attached."""
    import trk_score_v01 as TS
    runs = C11.load_runs()
    for r in runs:
        ld = np.load(V12A / 'out' / 'lead' / (r['run'] + '.npz'), allow_pickle=False)
        assert np.array_equal(ld['k'], r['k'])
        r['eph'] = TS.est_phase(ld['vhat'], ld['ahat_long'], ld['lead_found'], -1.0)
        r['lead'] = {k: ld[k] for k in ld.files}
        tg = np.load(V12A / 'out' / 'tg' / (r['run'] + '.npz'), allow_pickle=False)
        assert np.array_equal(tg['k'], r['k'])
        r['crit']['TG'] = np.asarray(tg['cTG2'], float)
        r['masks_est'] = masks_tracker_phase(r['ev'], r['v0'], r['eph'])
    return runs


# ------------------------------------------------------------------------------------------------ resampling
def counts(n_run, nboot, seed):
    return L.boot_counts(n_run, nboot, seed)


def prep(G, names, pop):
    return GF.Prepared(G, names, pop)


def evaluate(P, W, chunk=500):
    """gl_fast evaluate in chunks: dict(denE, n, D{a}) over the rows of W."""
    out = dict(denE=[], n=[], D={a: [] for a in P.names[2:]})
    for s in range(0, W.shape[0], chunk):
        e = GF.evaluate(P, W[s:s + chunk])
        out['denE'].append(e['denE']); out['n'].append(e['n'])
        for a in P.names[2:]: out['D'][a].append(e['D'][a])
    return dict(denE=np.concatenate(out['denE']), n=np.concatenate(out['n']), D={a: np.concatenate(v) for a, v in out['D'].items()})


def rat(D, den):
    return C11.rat(D, den)


# ------------------------------------------------------------------------------------------------ calibration (A10 sec. 2.6)
def percentile_ci(x, level):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if x.size == 0: return [np.nan, np.nan]
    a = (1. - level) / 2.
    return [float(np.quantile(x, a)), float(np.quantile(x, 1. - a))]


def counts_of(idx, n):
    """(B, n) run indices -> (B, n) counts per run (rev_d_bootstrap_v01.counts_of, vectorised)."""
    B = idx.shape[0]
    flat = (idx + n * np.arange(B)[:, None]).ravel()
    return np.bincount(flat, minlength=B * n).reshape(B, n).astype(float)


def cover_two(lt, le, nom):
    """rev_d_bootstrap_v01.cover_two: share of outer samples whose inner two-sided percentile interval at level nom contains the
    full-sample value: share(inner <= value) >= a/2 and share(inner < value) <= 1 - a/2."""
    a = 1. - nom; ok = np.isfinite(lt)
    return ((le[ok] >= a / 2. - 1e-12) & (lt[ok] <= 1. - a / 2. + 1e-12))


def double_bootstrap_shares(stat_fn, n_run, full, seed_inner, log=print, label=''):
    """Per outer sample (default_rng(20261912).integers(0, n, (2000, n))), the inner (default_rng(seed_inner), one stream,
    1,000 resamples of the outer sample's runs, as rev_d_bootstrap_v01 D2) shares below / at-or-below the full-sample values.
    stat_fn(W) -> (B, k) for count rows W; full (k,). Returns p_lt, p_le (2000, k)."""
    t0 = time.time()
    rng_o = np.random.default_rng(SEED_OUTER); rng_i = np.random.default_rng(seed_inner)
    IDX_O = rng_o.integers(0, n_run, (N_OUTER, n_run))
    full = np.atleast_1d(np.asarray(full, float)); k = full.size
    p_lt = np.full((N_OUTER, k), np.nan); p_le = np.full((N_OUTER, k), np.nan)
    OE = np.asarray(stat_fn(counts_of(IDX_O, n_run)), float).reshape(N_OUTER, k)      # outer estimates (v11: skip non-finite ones)
    for b in range(N_OUTER):
        io = IDX_O[b]; ii = rng_i.integers(0, n_run, (N_INNER, n_run))
        S = np.asarray(stat_fn(counts_of(io[ii], n_run)), float).reshape(N_INNER, k)
        for j in range(k):
            v = S[:, j]; v = v[np.isfinite(v)]
            if v.size == 0 or not np.isfinite(full[j]) or not np.isfinite(OE[b, j]): continue
            p_lt[b, j] = (v < full[j]).mean(); p_le[b, j] = (v <= full[j]).mean()
        if (b + 1) % 200 == 0: log('  double bootstrap %s (inner seed %d): outer %d/%d (%.0f s)' % (label, seed_inner, b + 1, N_OUTER, time.time() - t0))
    return p_lt, p_le


def calibrated_levels(sh1, sh2, names):
    """A10 sec. 2.6 rule per statistic from the share tables of the two inner seeds (sh = (p_lt, p_le))."""
    out = {}
    levels = LEVEL_STEPS
    for j, nm in enumerate(names):
        lt, le = sh1[0][:, j], sh1[1][:, j]
        ind95 = cover_two(lt, le, 0.95); c95 = float(ind95.mean()) if ind95.size else float('nan')
        res = dict(coverage95=c95, n_outer_valid=int(np.isfinite(lt).sum()))
        if not np.isfinite(c95):
            res.update(level=0.99, rule='coverage not defined (no valid outer sample); nominal 99%'); out[nm] = res; continue
        if not (c95 < 0.94):
            res.update(level=0.95, rule='nominal 95% (estimated coverage >= 0.94)'); out[nm] = res; continue
        IND = np.stack([cover_two(lt, le, lv) for lv in levels], axis=1)          # (n_valid, nlev)
        cov = IND.mean(axis=0); ok = np.flatnonzero(cov >= 0.95)
        if ok.size == 0:
            res.update(level=0.99, rule='nominal 99%: no level in 0.950-0.9995 reaches coverage 0.95'); out[nm] = res; continue
        lev = float(levels[ok[0]])
        # Monte Carlo SD: ONE index draw over all outer samples, default_rng(20261920).integers(0, N_OUTER, (2000, N_OUTER)), the same
        # for every statistic; validity applied inside each resample (CD_DEFINITIONS_v13.md "Calibration details").
        valid = np.isfinite(lt)
        INDF = np.zeros((lt.size, levels.size), bool); INDF[valid] = IND
        MCI = np.random.default_rng(SEED_MC).integers(0, lt.size, (N_MC, lt.size))
        boots = np.empty(N_MC)
        for i in range(N_MC):
            rows = MCI[i][valid[MCI[i]]]
            s = INDF[rows].mean(axis=0) if rows.size else np.full(levels.size, np.nan); kk = np.flatnonzero(s >= 0.95)
            boots[i] = levels[kk[0]] if kk.size else 1.0
        mcsd = float(np.std(boots, ddof=1))
        lt2, le2 = sh2[0][:, j], sh2[1][:, j]
        cov2 = np.array([cover_two(lt2, le2, lv).mean() for lv in levels]); k2 = np.flatnonzero(cov2 >= 0.95)
        lev2 = float(levels[k2[0]]) if k2.size else 1.0
        res.update(calibrated_level=lev, mc_sd=mcsd, second_seed_level=lev2)
        if mcsd <= 0.002 and abs(lev2 - lev) <= 0.002:
            res.update(level=lev, rule='calibrated (MC SD <= 0.002; second inner seed within 0.002)')
        else:
            res.update(level=0.99, rule='nominal 99%: the calibrated level failed its Monte Carlo checks')
        out[nm] = res
    return out


# ------------------------------------------------------------------------------------------------ statistic objects (exportable)
class GLStat:
    """Statistics of the gridless frontier from a gl_fast Prepared object: spec is a list of ('R',) | ('RR', a) | ('RRdiff', a, b)."""

    def __init__(self, P, spec):
        self.P = P; self.spec = [tuple(s) for s in spec]

    def __call__(self, Wr):
        e = GF.evaluate(self.P, Wr); den = e['denE']
        ok = np.isfinite(den) & (den > 0)
        cols = []
        with np.errstate(divide='ignore', invalid='ignore'):
            for s in self.spec:
                if s[0] == 'R': cols.append(den / L.NLEV)
                elif s[0] == 'RR': cols.append(np.where(ok, e['D'][s[1]] / den, np.nan))
                else: cols.append(np.where(ok, e['D'][s[1]] / den, np.nan) - np.where(ok, e['D'][s[2]] / den, np.nan))
        return np.stack(cols, axis=1)

    def save(self, path):
        P = self.P
        np.savez_compressed(path, kind='GL', names=np.array(P.names), pop=P.pop, T0=np.stack(P.T0), d=P.d, ri=P.ri, keep=P.keep,
                            ev_off=P.ev_off, keep_off=P.keep_off, spec=json.dumps(self.spec))


class H4Stat:
    """H4 record-basis share (sec. 5.5) on grid tables with the design choices fixed (no re-selection)."""

    def __init__(self, fF0, fE, tri, one):
        self.fF0, self.fE, self.tri, self.one = fF0, fE, tri, one

    def share(self, w):
        fF0, fE, tri, one = self.fF0, self.fE, self.tri, self.one
        Ta = np.tensordot(w, fF0[:, :, 0, :], axes=(0, 0)); TE = np.tensordot(w, fE[:, :, 0, :], axes=(0, 0))
        c = L.curves_w({'F0': Ta, 'E': TE}, 0); cF0, wF0 = c['F0']; cE, wE = c['E']
        lev_ = L.levels_of(cF0, cE, cF0[0])
        f0 = L.frontier(cF0, wF0, lev_); fe = L.frontier(cE, wE, lev_)
        Tph = [np.tensordot(w, fF0[:, :, pi, :], axes=(0, 0)) for pi in (2, 3, 4)]
        nl = tri.shape[0]; Wv = np.zeros(nl); Sv = np.zeros(nl); Kv = np.zeros(nl)
        for q in range(3):
            g = tri[:, q]; okg = g >= 0
            Wv[okg] += Tph[q][g[okg], 1]; Sv[okg] += Tph[q][g[okg], 2]; Kv[okg] += Tph[q][g[okg], 3]
        n = float(Ta[0, 0])
        with np.errstate(divide='ignore', invalid='ignore'):
            cp = np.where(tri[:, 0] >= 0, 100. * Sv / Kv, np.nan); wp = np.where(tri[:, 0] >= 0, 100. * Wv / n, np.nan)
            ok1 = one >= 0; g1 = np.clip(one, 0, None)
            c1 = np.where(ok1, 100. * Ta[g1, 2] / Ta[g1, 3], np.nan); w1 = np.where(ok1, 100. * Ta[g1, 1] / n, np.nan)
        fps = L.frontier(np.concatenate([[cF0[0]], cp]), np.concatenate([[wF0[0]], wp]), lev_)
        f1 = L.frontier(np.concatenate([[cF0[0]], c1]), np.concatenate([[wF0[0]], w1]), lev_)
        den = float(np.sum(f0 - fe))
        # [record basis, like-for-like basis, single scale (A10 sec. 5.5 "A single scale is chosen the same way"; added 20 Nov 2026)]
        return np.array([float(np.sum(f0 - fps)) / den if den > 0 else np.nan, float(np.sum(f1 - fps)) / den if den > 0 else np.nan,
                         float(np.sum(f0 - f1)) / den if den > 0 else np.nan])

    def __call__(self, Wr):
        return np.array([self.share(w)[:1] for w in Wr])

    def save(self, path):
        np.savez_compressed(path, kind='H4', fF0=self.fF0, fE=self.fE, tri=self.tri, one=self.one)


CALIB_MODE = 'local'                   # 'local' | 'export' | 'import' (set by the scripts from --calib)
CALIB_DIR = OUT / 'calib'


def calibrate_all(stat_obj, n_run, full, names, log=print, label='', need_second=True):
    """A10 sec. 2.6 for one statistic group. local: run both seeds here (second only if needed). export: write the job
    (calib/<label>.job.npz) for calib_remote_v13.py and return pending levels. import: read calib/<label>_<seed>.npz."""
    full = np.atleast_1d(np.asarray(full, float))
    if CALIB_MODE == 'export':
        CALIB_DIR.mkdir(parents=True, exist_ok=True)
        jp = CALIB_DIR / f'{label}.job.npz'
        stat_obj.save(jp)
        (CALIB_DIR / f'{label}.meta.json').write_text(json.dumps(dict(label=label, n_run=n_run, full=full.tolist(), names=list(names),
            seeds=[SEED_OUTER, SEED_INNER, SEED_INNER2], n_outer=N_OUTER, n_inner=N_INNER, job_sha256=sha(jp))), encoding='utf-8')
        return {nm: dict(level=0.95, rule='PENDING: exported for calib_remote_v13.py', pending=True) for nm in names}
    if CALIB_MODE == 'import':
        res = {}
        for seed in (SEED_INNER, SEED_INNER2):
            f = CALIB_DIR / f'{label}_{seed}.npz'
            if f.is_file():
                z = np.load(f); assert np.array_equal(z['full'], full, equal_nan=True), 'full-sample values differ from the exported job: ' + label
                res[seed] = (z['p_lt'], z['p_le'])
        assert SEED_INNER in res, 'no remote result for ' + label
        sh2 = res.get(SEED_INNER2, res[SEED_INNER])
        out = calibrated_levels(res[SEED_INNER], sh2, names)
        for nm in out: out[nm]['source'] = 'calib_remote_v13.py results ' + ', '.join(str(s) for s in res)
        return out
    sh1 = double_bootstrap_shares(stat_obj, n_run, full, SEED_INNER, log, label)
    need = any(np.isfinite(sh1[0][:, j]).any() and cover_two(sh1[0][:, j], sh1[1][:, j], 0.95).mean() < 0.94 for j in range(len(names)))
    sh2 = double_bootstrap_shares(stat_obj, n_run, full, SEED_INNER2, log, label) if (need and need_second) else sh1
    return calibrated_levels(sh1, sh2, names)


def interval(boot, point, level):
    """Percentile interval at the (calibrated) level over the finite resamples (np.percentile, as L.pct), plus L.summ fields."""
    b = np.asarray(boot, float); f = np.isfinite(b); a = 100. * (1. - level) / 2.
    ci = [float(x) for x in np.percentile(b[f], [a, 100. - a])] if f.any() else [float('nan'), float('nan')]
    s = L.summ(b, point); s['level'] = level; s['ci_level'] = ci
    return s
