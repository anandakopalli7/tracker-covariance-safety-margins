"""Package F (revision v13): scoring. New file, 19 Nov 2026 (Claude Opus 5.5).

Run unit = scene. Scoring library of record (optA_lib_v02) and the v12 gridless code reach this file through package B's frozen
shared module trk_score_v01 (imported unchanged: make_run conventions, margin_ratios, ratio_summary, e5_u, add_oracle, gridless,
rr_gl). Populations: 0 = all evaluated decisions (primary), 1 = evaluated decisions with an in-path lead vehicle (secondary).
3 s commitment scoring (W1: true clearance > 0 over the 3 s window); the 2 s horizon uses the 2 s arrays (clear2, *_2, evaluated2).

mode horizon  (design split, A10 section 8.3): D_gl(E, F0) of CANMOT (T1) at 3 s and at 2 s; point and 95% percentile interval
              from 20,000 scene resamples, default_rng(20261923).integers(0, 700, (20000, 700)) (the F seed, A10 section 5.8).
              Rule: 3 s if its lower end > 0; otherwise 2 s if its lower end > 0; otherwise F stops. Nothing else is computed on
              the design split (A10 section 8.6). Writes out\\F_HORIZON_RULE_v01.json.
mode heldout  (val; refused until LOCK_A10_2.txt exists): at the frozen horizon, F-H0, F-H1, F-H2 (A10 section 8.5) on the gridless
              step frontier, scene bootstrap default_rng(20261923) (20,000), intervals calibrated by A10 section 2.6 (double
              bootstrap: outer default_rng(20261912) 2,000, inner default_rng(20261913) 1,000, second inner default_rng(20261914)
              run only when some statistic's nominal-95% coverage is below 0.94 (the only case in which A10 2.6 uses it),
              Monte Carlo SD from default_rng(20261920) 2,000 resamples of the outer samples). Descriptive sources of CANMOT's
              run set: TG, E5, E5p, RR(E5) - RR(E5p), partial oracles 25/50/75 (95% percentile intervals). Writes
              out\\F_HELDOUT_v01.json and every resample array (shares and decision-equivalents) in out\\F_HELDOUT_BOOT_v01.npz.
Fast evaluation: f06k_kernel_v01 (numba, venv) evaluates the gridless curves and step frontiers of many resamples at once
(same arithmetic; the frontier by exact binary search of each point among the levels instead of sorting). Every run checks it against trk_score_v01.rr_gl on the first 25 resamples
(relative 1e-9) before any interval is formed.
Clearance (20 Nov 2026, departure notes\\F_DEPARTURE_CLEARANCE_v01.md, pinned 19 Nov 23:52 EST before any value under it): the
true clearances come from cache\\clear_v02\\<split>\\<scene>.npz (f15_clear_v02.py: (actor, frame) pairs whose actor centre is
behind the ego are dropped); everything else (critical scales, selection, fallback, seeds, levels) is unchanged. Outputs carry
_v02. `--clear=v01` reads the arrays' own clearances (the rule of record) and is only for reproducing the pre-registered horizon
output out\\F_HORIZON_RULE_v01.json; the held-out mode refuses it.
Double bootstrap on a pod (20 Nov 2026): `heldout --calib=export` stops after the single bootstrap and writes the job for
f16_calib_remote_v01.py; `heldout --calib=import` finishes from the pod's results (see the section "double bootstrap on a pod").
Usage: python -I f06_score_v01.py horizon | heldout [nproc] [--clear=v01] [--calib=export|import]
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402  (before numpy)
import json, multiprocessing as mp, time     # noqa: E402
import numpy as np                           # noqa: E402

SHARED = FC.F.parent / 'shared' / 'trackers'
sys.path.insert(0, str(SHARED))
import trk_score_v01 as TS                   # noqa: E402
L = TS.L

NLEV = L.NLEV
SEED_F = 20261923
NBOOT = 20000
DELTA = 0.05
B_OUT, B_IN = 2000, 1000
SEED_OUT, SEED_IN, SEED_IN2, SEED_MC = 20261912, 20261913, 20261914, 20261920
NOMINALS = np.round(np.arange(0.950, 0.99951, 0.0005), 4)
POPS = ('all', 'inpath')
CLEAR = 'v01' if '--clear=v01' in sys.argv else 'v02'
DEPARTURE = FC.F / 'notes' / 'F_DEPARTURE_CLEARANCE_v01.md'


def clearance_info():
    if CLEAR == 'v01':
        return dict(version='v01', rule='of record (all truth actors), the arrays\' own clear / clear2')
    return dict(version='v02', rule="departure: (actor, frame) pairs with the actor's centre behind the ego dropped",
                file='notes\\F_DEPARTURE_CLEARANCE_v01.md', sha256=FC.sha256_file(DEPARTURE),
                arrays='cache\\clear_v02\\<split>\\<scene>.npz (f15_clear_v02.py)')


# ------------------------------------------------------------------------------------------------ runs
def load_runs(tracker, split, horizon):
    FC.require_split(split)
    names = sorted(FC.splits()[split])
    sfx = '' if horizon == 3 else '_2'
    ck = 'clear' if horizon == 3 else 'clear2'
    runs = []
    for nm in names:
        z = np.load(FC.CACHE / ('arrays_' + tracker) / split / (nm + '.npz'), allow_pickle=False)
        meta = json.loads(str(z['meta']))
        ev = z['evaluated' if horizon == 3 else 'evaluated2'].astype(bool)
        clear = z[ck]
        if CLEAR == 'v02':
            c2 = np.load(FC.CACHE / 'clear_v02' / split / (nm + '.npz'), allow_pickle=False)
            if not np.array_equal(c2['sweep'], z['sweep']) or not np.array_equal(np.isnan(c2[ck]), np.isnan(clear)):
                raise RuntimeError('clear_v02 does not match the arrays of %s' % nm)
            clear = c2[ck]
        inpath = z['inpath'].astype(bool)
        runs.append(dict(run=nm, desired=float(meta['desired']), idx55=z['idx55'].astype(np.int64), clear1=L.clean_clear(clear),
                         vbar=z['vbar'], masks=(ev, ev & inpath), ev=ev, n_dec=int(ev.size),
                         crit={k: np.asarray(z['c' + k + sfx], float) for k in ('F0', 'E', 'N', 'TG')}, sel={}, late={}))
    return runs


def boot_counts(n, nboot, seed):
    idx = np.random.default_rng(seed).integers(0, n, (nboot, n))
    return counts_of(idx, n)


def counts_of(idx, n):
    cn = np.zeros((idx.shape[0], n))
    for b in range(idx.shape[0]):
        cn[b] = np.bincount(idx[b], minlength=n)
    return cn


# ------------------------------------------------------------------------------------------------ fast gridless evaluation
import f06k_kernel_v01 as K                  # noqa: E402  (numba; run this file with work\F_nuscenes\venv)


class Evaluator:
    """Compiled evaluation (f06k_kernel_v01.eval_many) of one population for the sources in `roles` = [F0 role, E role, others]."""

    def __init__(self, G, roles, pop):
        self.roles = list(roles); self.pop = pop
        self.args = K.pack([G[k] for k in self.roles], pop)

    def run(self, W):
        o = K.eval_many(np.ascontiguousarray(W, dtype=np.float64), *self.args)
        return dict(n=o[:, 0], denE=o[:, 1], D={a: o[:, i] for i, a in enumerate(self.roles) if i >= 2})


def verify(G, ev, W):
    """The Evaluator against trk_score_v01.rr_gl (the reference path through optA_lib_v02.eval_scoring) on the rows of W."""
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


# ------------------------------------------------------------------------------------------------ helpers
def summ(b, pt):
    return L.summ(np.asarray(b, float), pt)


def pct_level(b, level):
    b = np.asarray(b, float); f = np.isfinite(b)
    a = (1. - level) / 2.
    return [float(x) for x in np.percentile(b[f], [100. * a, 100. * (1. - a)])] if f.any() else [np.nan, np.nan]


def rr_of(D, den):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(np.isfinite(den) & (den > 0), D / den, np.nan)


# ------------------------------------------------------------------------------------------------ horizon rule (design split)
def horizon(nproc):
    FC.require_split('train')
    outf = FC.OUT / ('F_HORIZON_RULE_%s.json' % CLEAR)
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    t00 = time.time()
    doc = dict(code='f06_score_v01.py horizon', rule='A10 section 8.3', split='train (design split)', nboot=NBOOT,
               draw='default_rng(%d).integers(0, n_scenes, (%d, n_scenes))' % (SEED_F, NBOOT), clearance=clearance_info(),
               horizons={})
    for hz in (3, 2):
        runs = load_runs('T1', 'train', hz)
        n = len(runs)
        G = TS.gridless(runs, ['F0', 'E'])
        ev = Evaluator(G, ['F0', 'E'], 0)
        CNT = boot_counts(n, NBOOT, SEED_F)
        ver = verify(G, ev, CNT[:25])
        if ver['max_rel'] > 1e-9:
            raise RuntimeError('fast evaluator differs from the reference: %s' % ver)
        pt = TS.rr_gl(G, 'F0', 'E', [], 0)
        den = ev.run(CNT)['denE']
        R = den / NLEV
        ent = dict(n_scenes=n, n_evaluated=int(sum(r['ev'].sum() for r in runs)), verify=ver,
                   R_gl_pp=L.summ(R, pt['R_pp']), D_gl_E_F0=dict(point=pt['denE'], ci=L.pct(den)),
                   R_deceq=pt['R_deceq'], share_resamples_nonpositive=float(np.mean(~(den > 0))),
                   lower_end_positive=bool(L.pct(den)[0] > 0))
        doc['horizons']['%d s' % hz] = ent
        print('horizon %d s: R_gl %.5f pp, 95%% %s, nonpositive %.4f (%.0f s)' % (hz, pt['R_pp'], ent['R_gl_pp']['ci'],
              ent['share_resamples_nonpositive'], time.time() - t00), flush=True)
    if doc['horizons']['3 s']['lower_end_positive']:
        doc['primary_horizon_s'] = 3
    elif doc['horizons']['2 s']['lower_end_positive']:
        doc['primary_horizon_s'] = 2
    else:
        doc['primary_horizon_s'] = None
        doc['stop'] = 'no measurable room on design data at 2 or 3 s'
    doc['written'] = FC.clock(); doc['seconds'] = round(time.time() - t00, 1)
    doc['code_sha256'] = FC.sha256_file(pathlib.Path(__file__))
    outf.write_text(FC.jdump(doc), encoding='utf-8')
    print('WROTE', outf, 'primary horizon', doc['primary_horizon_s'])


# ------------------------------------------------------------------------------------------------ held-out (after Lock 2)
STATS = ('R', 'RR_N', 'r_IMM', 'c_IMM', 'eff_IMM')
# Descriptive sources of CANMOT's run set (A10 sections 8.2 and 2.2; added 19 Nov 2026, 19:20 EST, before Lock 2 and before any
# val value): E5 (f_i = 1.1029 (1 + 0.05 (2 u_i - 1)), u_i from T1's own F0/E ratios), E5p (u_i permuted within scenes,
# default_rng(20261915), trk_score_v01.permute_u), and the partial oracles of record (rev_g_partial_oracle_draws_v01 rule: one
# uniform per stored decision in (scene name, decision) order, E's critical scales where u < p and F0's elsewhere) with the fresh
# mask draw default_rng(20261919).random(total stored decisions).
E5_M, E5_A = 1.1029, 0.05
SEED_PO = 20261919
PO = (('PO25', 0.25), ('PO50', 0.5), ('PO75', 0.75))
DESC = ['TG', 'E5', 'E5p'] + [nm for nm, _ in PO]


class HeldOut:
    """Both trackers' run sets on the val scenes at the frozen horizon, with E5_IMM added (A10 section 2.2), and CANMOT's
    descriptive sources TG, E5, E5p and the partial oracles."""

    def __init__(self, hz):
        self.hz = hz
        self.T1 = load_runs('T1', 'val', hz)
        self.IM = load_runs('IMM', 'val', hz)
        u1, self.u1_info = TS.e5_u(self.T1, 'F0', 'E')
        TS.add_oracle(self.T1, 'E5', 'F0', E5_M, E5_A, u1)
        TS.add_oracle(self.T1, 'E5p', 'F0', E5_M, E5_A, TS.permute_u(self.T1, u1, seed=TS.SEED_PERM))
        U = np.random.default_rng(SEED_PO).random(sum(r['n_dec'] for r in self.T1))
        pos = 0
        for r in self.T1:
            uu = U[pos:pos + r['n_dec']]; pos += r['n_dec']
            for nm, p in PO:
                r['crit'][nm] = np.where((uu < p)[:, None], r['crit']['E'], r['crit']['F0'])
        self.po_draw = dict(seed=SEED_PO, n_stored=int(U.size))
        if [r['run'] for r in self.T1] != [r['run'] for r in self.IM]:
            raise RuntimeError('scene lists differ')
        for a, b in zip(self.T1, self.IM):
            for k in ('idx55', 'vbar', 'clear1', 'ev'):
                if not np.array_equal(a[k], b[k]):
                    raise RuntimeError('tracker-independent array %s differs in %s' % (k, a['run']))
        self.n = len(self.T1)
        ms = TS.margin_ratios(self.IM, 'N', 'F0')                  # sqrt(c_F0 / c_N) = sqrt(s_N / s_F0) at the binding rows
        self.ratio = TS.ratio_summary(ms)
        u, self.u_info = TS.e5_u(self.IM, 'F0', 'E')
        TS.add_oracle(self.IM, 'E5x', 'F0', self.ratio['median'], self.ratio['A'], u)
        self.G1 = TS.gridless(self.T1, ['F0', 'E', 'N'] + DESC)
        self.G2 = TS.gridless(self.IM, ['F0', 'E', 'N', 'E5x'])
        self.E1 = {pi: Evaluator(self.G1, ['F0', 'E', 'N'], pi) for pi in (0, 1)}
        self.E1desc = {pi: Evaluator(self.G1, ['F0', 'E'] + DESC, pi) for pi in (0, 1)}
        self.E2 = {pi: Evaluator(self.G2, ['F0', 'E', 'N', 'E5x'], pi) for pi in (0, 1)}

    def stats(self, W, pop=0):
        a = self.E1[pop].run(W)
        b = self.E2[pop].run(W)
        r = rr_of(b['D']['N'], b['denE']); c = rr_of(b['D']['E5x'], b['denE'])
        with np.errstate(divide='ignore', invalid='ignore'):
            eff = np.where(np.isfinite(c) & (c != 0), r / c, np.nan)
        return np.column_stack([a['denE'] / NLEV, rr_of(a['D']['N'], a['denE']), r, c, eff]), a, b


def cover_two(lt, le, nom):
    """a9_2a_double_bootstrap_mc_v01.cover_two (same expressions)."""
    a = 1. - nom
    ok = np.isfinite(lt)
    return float(((le[ok] >= a / 2. - 1e-12) & (lt[ok] <= 1. - a / 2. + 1e-12)).mean())


def calibrate(lt, le):
    """A10 section 2.6: nominal 95% if its coverage is >= 0.94; otherwise the smallest nominal in 0.950..0.9995 (0.0005) with
    coverage >= 0.95; None if there is none."""
    if cover_two(lt, le, 0.95) >= 0.94:
        return 0.95
    for nm in NOMINALS:
        if cover_two(lt, le, nm) >= 0.95:
            return float(nm)
    return None


def double_bootstrap(H, full, seed_inner):
    """a9_2a_double_bootstrap_mc_v01.double with A10's seeds: outer default_rng(20261912).integers(0, n, (2000, n)); inner one
    stream default_rng(seed_inner), 1,000 resamples of each outer sample's scenes in outer order; per outer sample the shares
    of inner values below / at-or-below the full-sample value of each statistic."""
    n = H.n
    IDX_O = np.random.default_rng(SEED_OUT).integers(0, n, (B_OUT, n))
    rng_i = np.random.default_rng(seed_inner)
    p_lt = np.full((B_OUT, len(STATS)), np.nan); p_le = np.full((B_OUT, len(STATS)), np.nan)
    t0 = time.time()
    for b in range(B_OUT):
        ii = rng_i.integers(0, n, (B_IN, n))
        S = H.stats(counts_of(IDX_O[b][ii], n))[0]
        for j in range(len(STATS)):
            v = S[:, j]; v = v[np.isfinite(v)]
            if v.size and np.isfinite(full[j]):
                p_lt[b, j] = (v < full[j]).mean(); p_le[b, j] = (v <= full[j]).mean()
        if (b + 1) % 100 == 0:
            print('  inner seed %d: outer %d / %d (%.0f s)' % (seed_inner, b + 1, B_OUT, time.time() - t0), flush=True)
    return p_lt, p_le


def heldout(nproc):
    FC.require_split('val')
    if CLEAR != 'v02':
        raise SystemExit('REFUSED: the held-out run uses the clearance in force (v02)')
    outf = FC.OUT / 'F_HELDOUT_v02.json'
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    frz = json.loads((FC.OUT / 'F_HORIZON_RULE_v02.json').read_text(encoding='utf-8'))
    hz = frz['primary_horizon_s']
    if hz is None:
        raise SystemExit('F stopped at the horizon rule: %s' % frz.get('stop'))
    t00 = time.time()
    H = HeldOut(hz)
    n = H.n
    CNT = boot_counts(n, NBOOT, SEED_F)
    vers = [verify(H.G1, H.E1[0], CNT[:25]), verify(H.G2, H.E2[0], CNT[:25]), verify(H.G1, H.E1desc[0], CNT[:25]),
            verify(H.G1, H.E1desc[1], CNT[:25])]
    if max(v['max_rel'] for v in vers) > 1e-9:
        raise RuntimeError('fast evaluator differs from the reference: %s' % vers)
    doc = dict(code='f06_score_v01.py heldout', horizon_s=hz, n_scenes=n, nboot=NBOOT, delta=DELTA, verify=vers, clearance=clearance_info(),
               ratio_IMM=H.ratio, e5_u=H.u_info, e5_u_T1=H.u1_info, partial_oracle_draw=H.po_draw,
               ratio_T1=TS.ratio_summary(TS.margin_ratios(H.T1, 'N', 'F0')), populations={})
    full = {}
    BOOT = {}     # every resample array (20,000 scene resamples) by population, saved to out\F_HELDOUT_BOOT_v02.npz for the export
    for pi, pn in enumerate(POPS):
        W1 = np.ones((1, n))
        S0, a0, b0 = H.stats(W1, pi)
        p1 = TS.rr_gl(H.G1, 'F0', 'E', ['N'], pi); p2 = TS.rr_gl(H.G2, 'F0', 'E', ['N', 'E5x'], pi)
        S, ab, bb = H.stats(CNT, pi)
        bt = {'R': S[:, 0], 'RR_N': S[:, 1], 'IMM.r': S[:, 2], 'IMM.c': S[:, 3], 'IMM.eff': S[:, 4],
              'R.dec': L.dec_eq(ab['denE'], ab['n']), 'RR_N.dec': L.dec_eq(ab['D']['N'], ab['n']),
              'IMM.R': bb['denE'] / NLEV, 'IMM.R.dec': L.dec_eq(bb['denE'], bb['n']),
              'IMM.r.dec': L.dec_eq(bb['D']['N'], bb['n']), 'IMM.c.dec': L.dec_eq(bb['D']['E5x'], bb['n']), 'n': ab['n']}
        ent = dict(n=p1['n'], T1=dict(R_pp=p1['R_pp'], R_deceq=p1['R_deceq'], RR_N=p1['RR']['N'], D_N_deceq=p1['D_deceq']['N']),
                   IMM=dict(R_pp=p2['R_pp'], R_deceq=p2['R_deceq'], RR_N_IMM=p2['RR']['N'], c_IMM=p2['RR']['E5x'],
                            D_N_IMM_deceq=p2['D_deceq']['N'], D_E5x_deceq=p2['D_deceq']['E5x']),
                   fast_point=S0[0].tolist(), boot={}, share_R_nonpositive=float(np.mean(~(S[:, 0] > 0))))
        for j, s in enumerate(STATS):
            ent['boot'][s] = L.summ(S[:, j], float(S0[0, j]))
            ent['boot'][s]['ci99'] = pct_level(S[:, j], 0.99)
        # descriptive (not hypotheses): RR_gl of TG, E5, E5p and the partial oracles in CANMOT's run set, and RR(E5) - RR(E5p);
        # 95% percentile intervals only
        db = H.E1desc[pi].run(CNT)
        pd = TS.rr_gl(H.G1, 'F0', 'E', DESC, pi)
        ent['descriptive'] = {}
        for a in DESC:
            bt['RR_' + a] = rr_of(db['D'][a], db['denE']); bt['RR_' + a + '.dec'] = L.dec_eq(db['D'][a], db['n'])
            ent['descriptive']['RR_' + a] = L.summ(bt['RR_' + a], pd['RR'][a])
            ent['descriptive']['RR_' + a]['D_deceq'] = pd['D_deceq'][a]
            ent['descriptive']['RR_' + a]['D_deceq_ci'] = L.pct(bt['RR_' + a + '.dec'])
        bt['RR_E5mP'] = bt['RR_E5'] - bt['RR_E5p']; bt['RR_E5mP.dec'] = L.dec_eq(db['D']['E5'] - db['D']['E5p'], db['n'])
        ent['descriptive']['RR_E5mP'] = L.summ(bt['RR_E5mP'], pd['RR']['E5'] - pd['RR']['E5p'])
        ent['descriptive']['RR_E5mP']['D_deceq'] = pd['D_deceq']['E5'] - pd['D_deceq']['E5p']
        ent['descriptive']['RR_E5mP']['D_deceq_ci'] = L.pct(bt['RR_E5mP.dec'])
        for k in ('R.dec', 'RR_N.dec', 'IMM.R', 'IMM.R.dec', 'IMM.r.dec', 'IMM.c.dec'):
            ent['boot'][k] = dict(ci=L.pct(bt[k]), ci99=pct_level(bt[k], 0.99))
        for k, v in bt.items():
            BOOT[pn + '|' + k] = np.asarray(v, float)
        doc['populations'][pn] = ent
        full[pn] = S0[0]
        if pi == 0:
            S_all = S
        print('%s: %s (%.0f s)' % (pn, {s: round(float(x), 5) for s, x in zip(STATS, S0[0])}, time.time() - t00), flush=True)
    # ---- calibration (A10 section 2.6), primary population
    np.savez_compressed(FC.OUT / 'F_HELDOUT_BOOT_v02.npz', **{k.replace('|', '__'): v for k, v in BOOT.items()})
    if CALIB == 'export':
        export_job(H, doc, S_all, full['all'], t00)
        return
    runs_db = {SEED_IN: double_bootstrap(H, full['all'], SEED_IN)}
    # the repeat with the second inner seed is needed only for a statistic whose nominal-95% coverage is below 0.94 (A10 2.6)
    need2 = [s for j, s in enumerate(STATS) if cover_two(runs_db[SEED_IN][0][:, j], runs_db[SEED_IN][1][:, j], 0.95) < 0.94]
    doc['second_inner_seed_run'] = dict(run=bool(need2), because=need2)
    if need2:
        runs_db[SEED_IN2] = double_bootstrap(H, full['all'], SEED_IN2)
    finish(doc, S_all, full['all'], runs_db, H.ratio, outf, t00)


# ------------------------------------------------------------------------------------------------ double bootstrap on a pod
# (20 Nov 2026, the coordinator's request of 01:25 EST: the A10 section 2.6 double bootstrap may run on a many-core pod.)
# --calib=export: after the single bootstrap, writes out\calib\heldout_all.job.npz (the packed gridless inputs of the two
#   Evaluators of the primary population, exactly as H.stats uses them) and heldout_all.meta.json (n, full-sample values, seeds,
#   sizes), and the partial result out\F_HELDOUT_PARTIAL_v02.json / .npz; then stops.
# f16_calib_remote_v01.py runs the double bootstrap of that job on the pod (same kernel file, same draws, same arithmetic) and
#   writes heldout_all_<seed>.npz (p_lt, p_le, the full-sample values it recomputed).
# --calib=import: reads the partial result and the pod's files (each must have reproduced the full-sample values exactly) and
#   finishes exactly as the local path does (finish()).
CALIB = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--calib=')), 'local')
CALIB_DIR = FC.OUT / 'calib'
JOB = 'heldout_all'


def export_job(H, doc, S_all, full_all, t00):
    CALIB_DIR.mkdir(parents=True, exist_ok=True)
    jf = CALIB_DIR / (JOB + '.job.npz')
    if jf.exists():
        raise SystemExit('REFUSED: %s exists' % jf)
    a1 = H.E1[0].args; a2 = H.E2[0].args
    np.savez(jf, kind='FULL', **{'a1_%d' % i: x for i, x in enumerate(a1)}, **{'a2_%d' % i: x for i, x in enumerate(a2)})
    meta = dict(job=JOB, kind='FULL', n_run=H.n, full=[float(x) for x in full_all], stats=list(STATS), n_outer=B_OUT, n_inner=B_IN,
                seed_outer=SEED_OUT, seeds_inner=[SEED_IN, SEED_IN2], nlev=NLEV, roles1=H.E1[0].roles, roles2=H.E2[0].roles,
                job_sha256=FC.sha256_file(jf), written=FC.clock())
    (CALIB_DIR / (JOB + '.meta.json')).write_text(FC.jdump(meta), encoding='utf-8')
    doc['calib_export'] = dict(job=str(jf.relative_to(FC.F)) if jf.is_relative_to(FC.F) else str(jf), job_sha256=meta['job_sha256'],
                               seconds=round(time.time() - t00, 1))
    doc['ratio_IMM_for_finish'] = H.ratio
    (FC.OUT / 'F_HELDOUT_PARTIAL_v02.json').write_text(FC.jdump(doc), encoding='utf-8')
    np.savez(FC.OUT / 'F_HELDOUT_PARTIAL_v02.npz', S_all=S_all, full_all=np.asarray(full_all, float))
    print('EXPORTED', jf, 'n', H.n, 'full', meta['full'])


def import_job(nproc):
    FC.require_split('val')
    outf = FC.OUT / 'F_HELDOUT_v02.json'
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    t00 = time.time()
    doc = json.loads((FC.OUT / 'F_HELDOUT_PARTIAL_v02.json').read_text(encoding='utf-8'))
    z = np.load(FC.OUT / 'F_HELDOUT_PARTIAL_v02.npz', allow_pickle=False)
    S_all = z['S_all']; full_all = z['full_all']
    meta = json.loads((CALIB_DIR / (JOB + '.meta.json')).read_text(encoding='utf-8'))
    if FC.sha256_file(CALIB_DIR / (JOB + '.job.npz')) != meta['job_sha256']:
        raise RuntimeError('job file changed since export')
    runs_db = {}; pods = {}
    for seed in (SEED_IN, SEED_IN2):
        p = CALIB_DIR / ('%s_%d.npz' % (JOB, seed))
        if not p.exists():
            continue
        r = np.load(p, allow_pickle=False)
        if str(r['job_sha256']) != meta['job_sha256'] or not bool(np.all(r['full_reproduced'])):
            raise RuntimeError('pod result %s: wrong job or full-sample values not reproduced exactly' % p.name)
        if not np.array_equal(r['full'], full_all, equal_nan=True):
            raise RuntimeError('pod result %s: full-sample values differ' % p.name)
        runs_db[seed] = (r['p_lt'], r['p_le'])
        pods[seed] = dict(file=p.name, sha256=FC.sha256_file(p), platform=str(r['platform']), seconds=float(r['seconds']))
    if SEED_IN not in runs_db:
        raise RuntimeError('the first inner seed result is missing')
    need2 = [s for j, s in enumerate(STATS) if cover_two(runs_db[SEED_IN][0][:, j], runs_db[SEED_IN][1][:, j], 0.95) < 0.94]
    doc['second_inner_seed_run'] = dict(run=bool(need2), because=need2,
                                        note='computed on the pod in parallel with the first seed; used only if needed')
    if not need2:
        runs_db.pop(SEED_IN2, None)
    elif SEED_IN2 not in runs_db:
        raise RuntimeError('the second inner seed is needed but its pod result is missing')
    doc['calib_import'] = dict(pod_results=pods, meta=meta)
    finish(doc, S_all, full_all, runs_db, doc.pop('ratio_IMM_for_finish'), outf, t00)


def finish(doc, S_all, full_all, runs_db, ratio, outf, t00):
    """Calibration (A10 section 2.6) from the double-bootstrap shares, the hypotheses (A10 section 8.5), the output file."""
    cal = {}
    IDX_MC = np.random.default_rng(SEED_MC).integers(0, B_OUT, (2000, B_OUT))
    full = {'all': full_all}
    for j, s in enumerate(STATS):
        lt, le = runs_db[SEED_IN]
        c1 = calibrate(lt[:, j], le[:, j])
        if SEED_IN2 in runs_db:
            lt2, le2 = runs_db[SEED_IN2]; c2 = calibrate(lt2[:, j], le2[:, j])
        else:
            c2 = None
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
                      coverage_at_levels={('%.4f' % nm): cover_two(lt[:, j], le[:, j], nm) for nm in NOMINALS[::10]},
                      ci=pct_level(S_all[:, j], level), point=float(full['all'][j]))
    doc['calibration'] = cal
    # ---- hypotheses (A10 section 8.5)
    R = cal['R']; rn = cal['RR_N']; r = cal['r_IMM']; c = cal['c_IMM']
    h0 = bool(R['ci'][0] > 0 and doc['populations']['all']['share_R_nonpositive'] < 0.025)
    h1 = bool(rn['ci'][0] > -DELTA and rn['ci'][1] < DELTA)
    if r['ci'][0] > 0:
        cls = 'a: recovers'
    elif c['ci'][0] > DELTA:
        cls = 'b: uninformative variation'
    elif c['ci'][0] > -DELTA and c['ci'][1] < DELTA:
        cls = 'c: amplitude-limited'
    else:
        cls = 'd: inconclusive'
    doc['hypotheses'] = dict(
        F_H0=dict(passes=h0, rule="R_gl's lower end > 0 and fewer than 2.5% of scene resamples non-positive"),
        F_H1=dict(passes=h1, rule='RR_gl(N) interval inside (-0.05, 0.05)', confirmed=bool(h0 and h1)),
        F_H2=dict(classification=cls, passes=cls[0] in 'abc', barely_varies=ratio.get('barely_varies'),
                  efficiency=cal['eff_IMM'] if cls[0] == 'a' else None, confirmed=bool(h0 and h1 and cls[0] in 'abc')))
    doc['written'] = FC.clock(); doc['seconds'] = round(time.time() - t00, 1)
    doc['code_sha256'] = FC.sha256_file(pathlib.Path(__file__))
    outf.write_text(FC.jdump(doc), encoding='utf-8')
    print('WROTE', outf, json.dumps(doc['hypotheses'], default=str))


if __name__ == '__main__':
    mode = sys.argv[1]
    args = [a for a in sys.argv[2:] if not a.startswith('--')]
    nproc = int(args[0]) if args else 6
    if mode == 'horizon':
        horizon(nproc)
    elif mode == 'heldout':
        if CALIB == 'import':
            import_job(nproc)
        else:
            heldout(nproc)
    else:
        raise SystemExit('mode?')
