"""Revision v11 (ARS review of draft v10): shared loader and scoring helpers for the post hoc re-analyses.
New file, 18 Nov 2026. Read-only on every project file; writes nothing itself.

What is reused and how:
  * optA_lib_v02.py (11_ojits/A6R/code; numpy + standard library only) is IMPORTED unchanged: stats_scored, eval_scoring,
    frontier, hull_frontier, select_grid, select_first_safe, boot_counts, summ, summ_den, dec_eq, brake_profile, tstop_array,
    late_of, vkey, clean_clear.
  * load_runs, masks_of, sel_of, safe_set, tables, points, boot, strat_point, strat_boot are COPIES (same expressions) of the
    functions of the same names in 11_ojits/A6R/code/optA_main_v02.py, without the planner-library import (optA_logs_v01),
    which these analyses do not need. Additions are marked "new".
  * GRID = [0] + logspace(-2, 3, 201): the assertion of optA_main_v02.py on ox12_score_v01.G_DENSE, rebuilt here.
Identity: rev_identity_v01.py checks this module against OPTIONA_MAIN_RESULTS_v02.json before any new quantity is computed.
"""
import json, pathlib, sys
import numpy as np

P = pathlib.Path(r'<library folder>')
OJ = P / '11_ojits'
sys.path.insert(0, str(OJ / 'A6R' / 'code'))
import optA_lib_v02 as L                     # noqa: E402

STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
A4X = OJ / 'A4' / 'fit' / 'extract'
CACHE = OJ / 'review' / 'optionA_recount_v01' / 'cache'
A4_JSON = OJ / 'A4' / 'fit' / 'analysis' / 'A4_RESULTS_FIT_v01.json'
OPTA_JSON = OJ / 'A6R' / 'run' / 'OPTIONA_MAIN_RESULTS_v02.json'

GRID = np.concatenate([[0.], np.logspace(-2, 3, 201)])
FIT_RUNS = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
NBOOT = 20000
SEED = 20261113
CHUNK = 250
VMIN = 0.5
TAUS = [0.5, 0.75, 1.0, 1.25, 1.5, 1.8]
A_MAIN = 6.0
TAU_KEY = 0.75
M8_A = [4.0, 5.0, 7.6]
CACHE_SETTINGS = [(t, A_MAIN) for t in TAUS] + [(TAU_KEY, a) for a in M8_A]
CACHE_KEYS = [L.vkey(t, a) for t, a in CACHE_SETTINGS]
MAIN_ARMS = ['N', 'NA', 'CK3', 'A1', 'Q']
POPS = ['all', 'moving', 'phase0', 'phase1', 'phase2', 'phase3']
PHASE_POPS = [2, 3, 4]


def masks_of(ev, v0, ph):
    return (ev, ev & (v0 > VMIN), ev & (ph == 0), ev & (ph == 1), ev & (ph == 2), ev & (ph == 3))


def load_runs():
    a4 = json.loads(A4_JSON.read_text(encoding='utf-8'))
    if a4.get('runs') != FIT_RUNS:
        raise RuntimeError('REFUSED: the A4 JSON run list differs from p1b_fit_finite_0005..0039')
    runs = []
    for run in FIT_RUNS:
        z = np.load(STORED / (run + '.npz'), allow_pickle=False)
        m = json.loads(str(z['meta']))
        if m.get('set') != 'fit' or m.get('run') != run or m.get('family') != 'lead_braking':
            raise RuntimeError('REFUSED: stored file of %s is not a fit lead-braking run' % run)
        x = np.load(A4X / (run + '.npz'), allow_pickle=False); mx = json.loads(str(x['meta'])); c = mx['checks']
        bad = [c['cF0_rows_differ'] != 0, c['cN_rows_differ'] != 0, c['idx55_differs'] != 0, c['n_nonfinite_sh'] != 0,
               mx['set'] != 'fit', mx['run'] != run, mx['code'] != 'oxsb_extract_v05.py', not np.array_equal(x['k'], z['k'])]
        if any(bad):
            raise RuntimeError('REFUSED %s: a check of record of the A4 extraction failed' % run)
        cz = np.load(CACHE / (run + '_pack.npz'), allow_pickle=False)
        tag = json.loads(str(cz['tag']))
        if tag.get('keys') != CACHE_KEYS or tag.get('jerk') != L.JERK or tag.get('h') != L.H:
            raise RuntimeError('REFUSED %s: the cache tag differs from the settings of record' % run)
        nd = len(z['k'])
        cache = {}
        for kk in ['own'] + CACHE_KEYS + ['v0_' + q for q in CACHE_KEYS] + ['a0_' + q for q in CACHE_KEYS]:
            a = cz[kk]
            if a.shape != (nd, 17):
                raise RuntimeError('REFUSED %s: cache array %s has shape %s' % (run, kk, a.shape))
            cache[kk] = a
        ev = z['evaluated'].astype(bool); v0 = z['v0']; ph = x['phase'].astype(np.int64)
        runs.append(dict(run=run, desired=float(m['desired']), meta=m, k=z['k'], ev=ev, v0=v0, ph=ph, vbar=z['vbar'],
                         idx55=z['idx55'], clear_raw=z['clear'], clear1=L.clean_clear(z['clear']), masks=masks_of(ev, v0, ph),
                         n_dec=nd,
                         crit={'F0': z['cF0'], 'E': z['cE'], 'N': z['cN'], 'NA': x['cNA'], 'A1': x['cA1'], 'CK3': x['cCK3'],
                               'Q': x['cQ']},
                         cache=cache, prim_idx=z['prim_idx'], prim_age=z['prim_age'], prim_track=z['prim_track'],
                         prim_miss=z['prim_miss'], sel={}, late={}))
    return runs


def sel_of(r, a):
    base = 'CK3' if a == 'CK3r' else a
    if base not in r['sel']:
        r['sel'][base] = L.select_grid(r['crit'][base], GRID, r['idx55']).astype(np.int16)
    return r['sel'][base]


def safe_set(r, sc):
    """Copy of optA_main_v02.safe_set, plus (new) an optional 4th element of sc, the standstill gap in m (default 0), and the
    scoring 'X' (new): a caller-supplied boolean safe set stored in r['safe_x'][sc[1]]."""
    if sc[0] == 'W1':
        return r['clear1'] > 0.
    if sc[0] == 'X':
        return r['safe_x'][sc[1]]
    tau, A = sc[1], sc[2]; key = L.vkey(tau, A)
    gap = sc[3] if len(sc) > 3 else 0.
    sR = L.clean_clear(r['cache'][key]) > gap
    if sc[0] in ('WR', 'WRs'):
        return sR
    if sc[0] == 'ii':
        if key not in r['late']:
            r['late'][key] = L.late_of(L.tstop_array(r['cache']['v0_' + key], r['cache']['a0_' + key], tau, A))
        return sR & ~(r['late'][key] & r['ev'][:, None])
    raise RuntimeError('unknown scoring %r' % (sc,))


def tables(runs, sc, arms, signed=False, masks_key='masks'):
    """Copy of optA_main_v02.tables; masks_key (new) selects an alternative tuple of population masks per run."""
    per = {a: [] for a in arms if a != 'CK3r'}
    for r in runs:
        sx = safe_set(r, sc)
        for a in per:
            sel = L.select_first_safe(sx, r['idx55']) if a == 'O' else sel_of(r, a)
            per[a].append(L.stats_scored(sel, r['clear1'], sx, r['vbar'], r['desired'], r[masks_key], signed=signed))
    X = {a: np.stack(v) for a, v in per.items()}
    if 'CK3r' in arms:
        X['CK3r'] = X['CK3']
    return X


def points(X, names, hull_names=(), pops=range(6), repl=()):
    Tsum = {a: X[a].sum(axis=0) for a in X}
    return {pi: L.eval_scoring({a: Tsum[a][:, pi, :] for a in X}, names, hull_names, repl) for pi in pops}


def boot(X, names, hull_names, pops, CNT, repl=(), hull_pops=None):
    B = CNT.shape[0]
    hull_pops = list(pops) if hull_pops is None else list(hull_pops)
    R = {}
    for pi in pops:
        hn = hull_names if pi in hull_pops else ()
        R[pi] = dict(denE=np.full(B, np.nan), n=np.full(B, np.nan), D={a: np.full(B, np.nan) for a in names},
                     hdenE=np.full(B, np.nan), hD={a: np.full(B, np.nan) for a in hn}, hull_names=list(hn))
    for s0 in range(0, B, CHUNK):
        cn = CNT[s0:s0 + CHUNK]
        for pi in pops:
            TB = {a: np.tensordot(cn, X[a][:, :, pi, :], axes=(1, 0)) for a in X}
            hn = R[pi]['hull_names']
            for b in range(cn.shape[0]):
                e = L.eval_scoring({a: TB[a][b] for a in X}, names, hn, repl)
                i = s0 + b
                R[pi]['denE'][i] = e['denE']; R[pi]['n'][i] = e['n']
                for a in names:
                    R[pi]['D'][a][i] = e['D'][a]
                if hn:
                    R[pi]['hdenE'][i] = e['hdenE']
                    for a in hn:
                        R[pi]['hD'][a][i] = e['hD'][a]
    return R


def rat(D, den):
    """Copy of optA_main_v02.rat: D / den where den is finite and > 0, else NaN (arrays)."""
    D = np.asarray(D, float); den = np.asarray(den, float)
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(np.isfinite(den) & (den > 0), D / den, np.nan)


def strat_point(pts, names, hnames=()):
    ns = {pi: pts[pi]['n'] for pi in PHASE_POPS}
    tot = sum(v for v in ns.values() if v > 0)
    w = {pi: (ns[pi] / tot if ns[pi] > 0 else 0.) for pi in PHASE_POPS}

    def f(key, a=None):
        return float(sum(w[pi] * (pts[pi][key] if a is None else pts[pi][key][a]) for pi in PHASE_POPS if ns[pi] > 0))
    out = dict(n=float(tot), denE=f('denE'), D={a: f('D', a) for a in names})
    if hnames:
        out['hdenE'] = f('hdenE'); out['hD'] = {a: f('hD', a) for a in hnames}
    return out


def strat_boot(R, names, hnames=()):
    ns = np.stack([R[pi]['n'] for pi in PHASE_POPS])
    tot = np.where(ns > 0, ns, 0.).sum(axis=0)
    with np.errstate(divide='ignore', invalid='ignore'):
        w = np.where(ns > 0, ns / tot, 0.)

    def comb(get):
        acc = np.zeros(ns.shape[1])
        for j, pi in enumerate(PHASE_POPS):
            acc = acc + np.where(ns[j] > 0, w[j] * get(pi), 0.)
        return acc
    out = dict(n=tot, denE=comb(lambda pi: R[pi]['denE']), D={a: comb(lambda pi, a=a: R[pi]['D'][a]) for a in names},
               hull_names=list(hnames))
    out['hdenE'] = comb(lambda pi: R[pi]['hdenE']) if hnames else None
    out['hD'] = {a: comb(lambda pi, a=a: R[pi]['hD'][a]) for a in hnames}
    return out


def cnt_of_record():
    """The bootstrap draw of record: default_rng(20261113).integers(0, 35, (20000, 35)) as counts per run."""
    return L.boot_counts(len(FIT_RUNS), NBOOT, SEED)


def jdump(obj):
    return json.dumps(obj, indent=1, default=float, allow_nan=True)
