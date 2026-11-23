"""Revision v13, package C, lead braking: the supplement sensitivities of AMENDMENT_10_v13 sec. 5.7 (S57B keys). New file,
20 Nov 2026 (Claude Opus 5.5). Definitions: CD_capture\\CD_DEFINITIONS_S57B_v13.md (every choice and array format).

Groups (keys of export\\A_KEYS_CD_v13.json; descriptive, nominal 95% percentile intervals, fresh bootstrap default_rng(20261911), 20,000):
  1  populations all / mov / pre / brk / stop (CV0's phase estimate, -1.0 m/s^2): n_dec, R, RR of AM, CK3, E5, N, NA, Q, TG and IMM
     (N_IMM on the IMM's own room, B1 arrays), with intervals;
  2  reaction and stop, judged until the stop ends (scoring 'est' on the RSX arrays of x_rsx_extract_v13.py; rev_e2 / rev_e3 /
     rev_e4): rel, den0.dec, RR0_N, RR0_CK3 for tau 0.5-1.8 s at 6 m/s^2 (rel and RR0_N with intervals) and A = 4, 5, 7.6 at 0.75 s;
     the 2 m standstill gap;
  3  after-stop truncation T = 0, 1, 2, 5, 10, 20 s (rev_b R12a) and the recordings cut 5 s after the stop: R, RR_CK3;
  4  caution capped at 5, 10, 15 %: R; signed caution (rev_a R11): R, RR_N, RR_CK3;
  5  grid frontier and placebo (A9-1(a)): RR_N, RR_P, RR_N - RR_P; convex hull on the grid points: R, RR_N, RR_CK3.
Frontier: gridless step frontier (A10 sec. 2.3) for groups 1-4; grid for group 5. Resamples with gl_fast (cd_common_v13.prep/evaluate,
identical to the library; checked at the full sample here).
Gate: stage 2 of the two-stage Lock 2 (cd_common_v13.require_lock2c). --test-old runs every group on the 35 OLD evaluation runs
(exploratory data of record) with the draw of record (default_rng(20261113)), never reads a fresh run, and compares with the values
of record (v11 rev_a / rev_b / rev_e2 / rev_e3 / rev_e4, v12 A9-1 / A9-7B, Option A main, package B's old-run B_CV0 / B_B1).
  --frontier grid|gridless and --phase est|truth (test only) select the frontier and the phase of the populations, so that each
  value of record can be reproduced by its own construction.
Usage (from CD_capture): .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\c_s57b_v13.py [--test-old [--frontier grid] [--phase truth]
  [--ext record|mine] [--tag T]] [--nboot N] [--groups 12345]
"""
import argparse, json, math, os, pathlib, sys, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('NUMBA_NUM_THREADS', '2')
import numpy as np
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cd_common_v13 as CC               # noqa: E402
import trk_score_v01 as TS               # noqa: E402  (e5_u, add_oracle, est_phase; no tracker set-up needed)
L = CC.L; C11 = CC.C11; A9 = CC.A9

ap = argparse.ArgumentParser()
ap.add_argument('--test-old', action='store_true'); ap.add_argument('--nboot', type=int, default=CC.NBOOT)
ap.add_argument('--frontier', choices=('gridless', 'grid'), default='gridless'); ap.add_argument('--phase', choices=('est', 'truth'), default='est')
ap.add_argument('--ext', choices=('record', 'mine'), default='mine'); ap.add_argument('--tag', default='')
ap.add_argument('--groups', default='12345')
ap.add_argument('--summarize', default='', help='write analysis\\out\\TEST_S57B_v13<suffix>.json from the TESTOLD files and the RSX test record')
args = ap.parse_args()
if args.summarize:
    outs = sorted(f for f in CC.OUT.glob('TESTOLD_S57B_v13*.json') if '_smoke' not in f.name)      # smoke runs (100 resamples) are development only
    rec = dict(family='S57B', program='c_s57b_v13.py', written=time.strftime('%Y-%m-%d %H:%M:%S'), testold_files={}, rsx_extract_tests={})
    for f in outs:
        d = json.loads(f.read_text(encoding='utf-8')); c = d['details'].get('comparison_with_record', {})
        rec['testold_files'][f.name] = dict(frontier=d['details']['frontier'], phase=d['details']['phase'], draw=d['details']['draw'],
                                            ext=d['details'].get('ext_dir'), n_values=d['details']['keys']['n_values'],
                                            seconds=d['details']['seconds'], compared=c.get('n'), agree=c.get('n_ok'),
                                            max_absdiff=c.get('max_absdiff'), failures=c.get('failures'))
    for f in sorted(CC.OUT.glob('TEST_S57B_v13_rsx_extract_*.json')):
        d = json.loads(f.read_text(encoding='utf-8'))
        rec['rsx_extract_tests'][f.name] = dict(runs=len(d['runs']), cost=d.get('cost'), worst_vs_v11_ext=d['comparison_with_v11_ext']['worst'],
                                                loader_check_all=d.get('loader_check_all'), cache_check_worst=d.get('cache_check_worst'))
    out = CC.OUT / ('TEST_S57B_v13%s.json' % args.summarize.strip('_').join(['_', '']) if args.summarize != 'main' else 'TEST_S57B_v13.json')
    CC.write_once(out, rec); print('written', out); raise SystemExit(0)
if not args.test_old and (args.frontier != 'gridless' or args.phase != 'est' or args.tag or args.nboot != CC.NBOOT or args.groups != '12345'):
    raise SystemExit('REFUSED: --frontier / --phase / --tag / --nboot / --groups are test options (--test-old only)')
gate = CC.require_lock2c(args.test_old)
t00 = time.time()
log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)


def mem():
    try:
        import psutil
        m = psutil.Process().memory_info()
        return 'rss %.0f MB, peak %.0f MB' % (m.rss / 2 ** 20, getattr(m, 'peak_wset', m.rss) / 2 ** 20)
    except Exception:                          # noqa: BLE001
        return 'memory not measured'


OUTF = CC.OUT / (('TESTOLD_S57B_v13%s.json' % args.tag) if args.test_old else 'S57B_v13.json')
if OUTF.exists():
    raise SystemExit('REFUSED: %s exists' % OUTF)
GL = args.frontier == 'gridless'

POPS = ['all', 'mov', 'pre', 'brk', 'stop']
SRC1 = [('AM', 'A1'), ('CK3', 'CK3'), ('E5', 'E5'), ('N', 'N'), ('NA', 'NA'), ('Q', 'Q'), ('TG', 'TG')]
TAUS = [0.5, 0.75, 1.0, 1.25, 1.5, 1.8]
AS = [4.0, 5.0, 7.6]
VARIANTS = [(t, 6.0) for t in TAUS] + [(0.75, a) for a in AS]
TSTR = {0.5: '0.5', 0.75: '0.75', 1.0: '1.0', 1.25: '1.25', 1.5: '1.5', 1.8: '1.8'}
ASTR = {4.0: '4', 5.0: '5', 6.0: '6', 7.6: '7.6'}
TRUNC = [0., 1., 2., 5., 10., 20.]
CAPS = [5., 10., 15.]
GAP = 2.0
V11 = pathlib.Path(r'ARS_TRIAL\revision_v11\analysis')
V12 = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis')
BRT = CC.WORK / 'B_retrack' / 'out'
OPTA = pathlib.Path(r'<library folder>\OPTIONA_MAIN_RESULTS_v02.json')


# ------------------------------------------------------------------------------------------------ runs
def truth5(r):
    return CC.masks_tracker_phase(r['ev'], r['v0'], np.where(r['ph'] <= 2, r['ph'], 9))


def make_imm(cv, z):
    """IMM run (B1 arrays) on the CV0 run's populations (CD_DEFINITIONS_S57B sec. 3)."""
    chk = dict(k=bool(np.array_equal(np.asarray(z['k'], np.int64), np.asarray(cv['k'], np.int64))),
               v0=bool(np.array_equal(z['v0'], cv['v0'])), clear=bool(np.array_equal(z['clear'], cv['clear_raw'], equal_nan=True)),
               vbar=bool(np.array_equal(z['vbar'], cv['vbar'], equal_nan=True)),
               idx55=bool(np.array_equal(np.asarray(z['idx55'], np.int64), np.asarray(cv['idx55'], np.int64))))
    assert chk['k'], ('B1 decisions differ from CV0', cv['run'], chk)     # the masks index decisions; the rest is recorded
    evb = z['evaluated'].astype(bool)
    chk['n_evaluated_differ'] = int((evb != cv['ev']).sum())
    eph_own = TS.est_phase(z['vhat'], z['ahat_long'], z['lead_found'], -1.0)
    return dict(run=cv['run'], desired=cv['desired'], idx55=np.asarray(z['idx55'], np.int64), clear1=L.clean_clear(z['clear']),
                vbar=z['vbar'], ev=cv['ev'] & evb, v0=z['v0'], masks=tuple(m & evb for m in cv['masks']),
                masks_own=CC.masks_tracker_phase(evb, z['v0'], eph_own),
                crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float)},
                sel={}, late={}, chk=chk)


if args.test_old:
    runs = CC.load_old_lead()
    for r in runs:
        r['masks'] = r['masks_est'] if args.phase == 'est' else truth5(r)
    run_ids = [r['run'] for r in runs]
    imm = [make_imm(r, np.load(BRT / 'retrack' / 'B1' / (r['run'] + '_arrays.npz'), allow_pickle=False)) for r in runs]
    EXTDIR = (V11 / 'out' / 'ext') if args.ext == 'record' else (CC.OUT / 'rsx_testold_arrays')
    CNT = C11.cnt_of_record()[:args.nboot]
    draw = 'default_rng(20261113).integers(0, 35, (20000, 35)) (the draw of record), first %d rows' % args.nboot
else:
    run_ids = CC.c_run_ids('lead_braking')
    runs = CC.load_variant(run_ids, 'CV0')
    assert all(r['meta'].get('family') == 'lead_braking' for r in runs)
    assert all('TG' in r['crit'] for r in runs), 'cTG2 missing in CV0 arrays'
    imm = [make_imm(r, np.load(CC.ARR / 'B1' / (r['run'] + '.npz'), allow_pickle=False)) for r in runs]
    EXTDIR = CC.ARR / 'RSX'
    CNT = CC.counts(len(runs), CC.NBOOT, CC.SEED_BOOT)
    draw = 'default_rng(20261911).integers(0, 105, (20000, 105)) over the runs in ascending id (fresh-run bootstrap)'
NR = len(runs)
for r in runs:
    r['masks_all'] = (r['ev'],)
ONES = np.ones((1, NR))
log('runs %d (%s); frontier %s; phase %s; %d resamples' % (NR, 'TEST: old evaluation runs' if args.test_old else 'fresh C lead braking',
                                                        args.frontier, args.phase, CNT.shape[0]))
u, uinfo = TS.e5_u(runs, 'F0', 'E')
TS.add_oracle(runs, 'E5', 'F0', CC.RATIO, 0.05, u)
A9.add_placebo(runs, 'P')


# ------------------------------------------------------------------------------------------------ scorers
def safe_w1(r):
    return r['clear1'] > 0.


def row_stats_signed(r, safe_x, masks):
    """A9.row_stats with caution counted at its signed value (L.stats_scored signed=True per row): column 2 = (vbar[W1 oracle row] -
    vbar[row]) / desired for every decision with a W1-safe row, column 3 = that decision has a W1-safe row (whatever the row)."""
    clear1 = r['clear1']; vbar = r['vbar']; des = r['desired']
    n = clear1.shape[0]; ar = np.arange(n)
    safe = clear1 > 0.
    anys1 = safe.any(axis=1)
    orc = safe.argmax(axis=1)
    ct = np.where(anys1[:, None], (vbar[ar, orc][:, None] - vbar) / des, 0.)
    anysX = safe_x.any(axis=1)
    out = np.zeros((n, 17, len(masks), L.NST))
    for mi, m in enumerate(masks):
        mm = m[:, None].astype(float)
        out[:, :, mi, 0] = mm
        out[:, :, mi, 1] = (~safe_x) * mm
        out[:, :, mi, 2] = ct * mm
        out[:, :, mi, 3] = anys1[:, None] * mm
        out[:, :, mi, 4] = (anysX[:, None] & ~safe_x) * mm
    return out


def paths_of(r, a):
    """A9.sel_path per decision of source a (cached per run and source; crit is not changed after the first call)."""
    pc = r.setdefault('_paths', {})
    if a not in pc:
        c = r['crit'][a]; idx = r['idx55']
        pc[a] = [A9.sel_path(c[i], idx[i]) for i in range(c.shape[0])]
    return pc[a]


def build_gridless(rs, names, safe_fn, masks_fn, rs_fn=A9.row_stats, shift=0.):
    """{name: A9.Gridless}: A9.gridless_sources(rs, names, safe_fn) with the row statistics computed once per run and scoring, the
    selection paths cached, an optional row-statistics function (signed caution) and a shift of the caution's clearance (gap)."""
    per = {a: [] for a in names}
    for r in rs:
        sx = safe_fn(r); masks = masks_fn(r)
        rr = r if shift == 0. else dict(r, clear1=r['clear1'] - shift)
        RS = rs_fn(rr, sx, masks); npop = len(masks)
        for a in names:
            if a == 'O':
                sel = L.select_first_safe(sx, r['idx55'])[0]
                per[a].append((RS[np.arange(sel.size), sel].sum(axis=0), np.zeros(0), np.zeros((0, npop, L.NST))))
                continue
            T0 = np.zeros((npop, L.NST)); bs = []; ds = []
            for i, (s0, ev) in enumerate(paths_of(r, a)):
                T0 += RS[i, s0]
                cur = s0
                for b, nxt in ev:
                    if nxt != cur:
                        bs.append(b); ds.append(RS[i, nxt] - RS[i, cur])
                    cur = nxt
            per[a].append((T0, np.array(bs), np.stack(ds)) if bs else (T0, np.zeros(0), np.zeros((0, npop, L.NST))))
    return {a: A9.Gridless(per[a]) for a in names}


NCHK_FILTER = 200
FILTER_LOG = []


def prep_filtered(P, G, names):
    """The gl_fast Prepared object P without the events whose statistics (columns 0-3) are all zero in P's population (decisions
    outside the population or not evaluated): such an event adds exactly 0.0 to the running sums, so the curve's distinct points, and
    hence every frontier value, are unchanged; the last retained event of each breakpoint is kept as the curve point (A9's rule)."""
    import copy
    Q = copy.copy(P)
    d_l, ri_l, keep_l, nev, nkeep = [], [], [], [0], [0]
    for s, a in enumerate(names):
        e0, e1 = int(P.ev_off[s]), int(P.ev_off[s + 1])
        d = P.d[e0:e1]; ri = P.ri[e0:e1]
        idx = np.flatnonzero(np.any(d[:, :4] != 0., axis=1)) if e1 > e0 else np.zeros(0, np.int64)
        bb = G[a].b[idx] if idx.size else np.zeros(0)
        keep = np.flatnonzero(np.concatenate([bb[1:] != bb[:-1], [True]])) if idx.size else np.zeros(0, np.int64)
        d_l.append(d[idx]); ri_l.append(ri[idx]); keep_l.append(keep.astype(np.int64))
        nev.append(nev[-1] + idx.size); nkeep.append(nkeep[-1] + keep.size)
    Q.d = np.ascontiguousarray(np.concatenate(d_l, axis=0)); Q.ri = np.concatenate(ri_l).astype(np.int64)
    Q.keep = np.concatenate(keep_l).astype(np.int64)
    Q.ev_off = np.array(nev, np.int64); Q.keep_off = np.array(nkeep, np.int64)
    return Q


class Scorer:
    """One scoring of a run set: tables of every source (names[0] = F0, names[1] = E) by population, on the gridless (GL) or the grid
    frontier. point(pop) -> dict(denE, n, D, c0, C); boot(pop, W, names) -> dict(denE, n, D) over the rows of W; curves(pop)."""

    def __init__(self, rs, names, safe_fn, masks_fn, gridless=True, rs_fn=A9.row_stats, shift=0., signed=False):
        self.names = list(names); self.gl = gridless; self.nrun = len(rs)
        if gridless:
            self.G = build_gridless(rs, names, safe_fn, masks_fn, rs_fn, shift)
        else:
            per = {a: [] for a in names}
            for r in rs:
                sx = safe_fn(r); masks = masks_fn(r)
                for a in names:
                    sel = L.select_first_safe(sx, r['idx55']) if a == 'O' else C11.sel_of(r, a)
                    per[a].append(L.stats_scored(sel, r['clear1'] - shift, sx, r['vbar'], r['desired'], masks, signed=signed))
            self.X = {a: np.stack(v) for a, v in per.items()}

    def curves(self, pop):
        if self.gl:
            return {a: self.G[a].curve(None, pops=[pop])[:, 0, :] for a in self.names}
        return {a: self.X[a].sum(axis=0)[:, pop, :] for a in self.names}

    def point(self, pop, hull=()):
        e = L.eval_scoring(self.curves(pop), self.names[2:], hull_names=hull)
        return e

    def boot(self, pop, W, names=None):
        nm = list(names) if names else self.names
        if self.gl:
            P = CC.prep(self.G, nm, pop)
            chk = CC.evaluate(P, ONES); pt = self.point(pop)
            assert chk['denE'][0] == pt['denE'] and all(chk['D'][a][0] == pt['D'][a] for a in nm[2:]), 'gl_fast differs from the library'
            Pf = prep_filtered(P, self.G, nm)
            nchk = min(NCHK_FILTER, W.shape[0])                      # the filtered events give the same numbers, bit for bit
            a_, b_ = CC.evaluate(P, W[:nchk]), CC.evaluate(Pf, W[:nchk])
            assert np.array_equal(a_['denE'], b_['denE']) and all(np.array_equal(a_['D'][a], b_['D'][a], equal_nan=True) for a in nm[2:]), \
                'filtered events differ'
            FILTER_LOG.append(dict(pop=pop, names=nm, events=int(P.d.shape[0]), events_kept=int(Pf.d.shape[0]), checked_rows=int(nchk)))
            return CC.evaluate(Pf, W)
        R = C11.boot({a: self.X[a] for a in nm}, nm[2:], (), [pop], W)[pop]
        return dict(denE=R['denE'], n=R['n'], D=R['D'])


def ratio(a, b):
    return L.ratio(a, b)


def pct(x):
    x = np.asarray(x, float)
    return L.pct(x)


def invalid(x):
    return float(np.mean(~np.isfinite(np.asarray(x, float))))


V = {}            # values (A's keys)
DT = dict(definitions='CD_capture\\CD_DEFINITIONS_S57B_v13.md', draw=draw, frontier=args.frontier + ' (groups 1-4); grid (group 5)',
          phase=args.phase, e5_u=uinfo, runs=run_ids, n_runs=NR, ext_dir=str(EXTDIR))


def put_ci(key, ci):
    V[key] = ci; V[key[:-3] + '.level'] = 0.95; V[key[:-3] + '.cal'] = 'nominal95'


# ------------------------------------------------------------------------------------------------ group 1: populations
B_ALL_W1 = None
if '1' in args.groups:
    names1 = ['F0', 'E'] + [c for _, c in SRC1]
    d1 = dict(imm_checks=dict(n_evaluated_differ=int(sum(r['chk']['n_evaluated_differ'] for r in imm)),
                              runs_differing_from_CV0={f: [r['run'] for r in imm if not r['chk'][f]] for f in ('v0', 'clear', 'vbar', 'idx55')}),
              pops={})
    for pi, pn in enumerate(POPS):                    # one population at a time (memory); the same numbers as one table set
        S1 = Scorer(runs, names1, safe_w1, lambda r, pi=pi: (r['masks'][pi],), GL)
        SI = Scorer(imm, ['F0', 'E', 'N'], safe_w1, lambda r, pi=pi: (r['masks'][pi],), GL)
        p = S1.point(0); b = S1.boot(0, CNT)
        if pi == 0:
            B_ALL_W1 = b; P_ALL_W1 = p
        V['LB.%s.n_dec' % pn] = int(round(p['n']))
        V['LB.%s.R' % pn] = p['denE'] / L.NLEV
        put_ci('LB.%s.R.ci' % pn, pct(b['denE'] / L.NLEV))
        dd = dict(n=p['n'], R_dec=L.dec_eq(p['denE'], p['n']), R_dec_ci=pct(L.dec_eq(b['denE'], b['n'])),
                  share_resamples_denE_le0=float(np.mean(~(b['denE'] > 0))), src={})
        for key, c in SRC1:
            rr = C11.rat(b['D'][c], b['denE'])
            V['LB.%s.RR_%s' % (pn, key)] = ratio(p['D'][c], p['denE'])
            put_ci('LB.%s.RR_%s.ci' % (pn, key), pct(rr))
            dd['src'][key] = dict(D_dec=L.dec_eq(p['D'][c], p['n']), invalid_share=invalid(rr))
        q = SI.point(0); bi = SI.boot(0, CNT)
        rr = C11.rat(bi['D']['N'], bi['denE'])
        V['LB.%s.RR_IMM' % pn] = ratio(q['D']['N'], q['denE'])
        put_ci('LB.%s.RR_IMM.ci' % pn, pct(rr))
        dd['IMM'] = dict(n=q['n'], R_IMM_pp=q['denE'] / L.NLEV, R_IMM_ci=pct(bi['denE'] / L.NLEV), D_N_dec=L.dec_eq(q['D']['N'], q['n']),
                         invalid_share=invalid(rr))
        d1['pops'][pn] = dd
        del S1, SI
        log('group 1: %s done (%s)' % (pn, mem()))
    if args.phase == 'est':                                   # sensitivity: the IMM's own phase estimate (points)
        SIo = Scorer(imm, ['F0', 'E', 'N'], safe_w1, lambda r: r['masks_own'], GL)
        d1['imm_own_phase_points'] = {pn: dict(n=e['n'], R_pp=e['denE'] / L.NLEV, RR_N=ratio(e['D']['N'], e['denE']))
                                      for pn, e in ((pn, SIo.point(pi)) for pi, pn in enumerate(POPS))}
        del SIo
    DT['group1'] = d1
    log('group 1 done (%s)' % mem())


# ------------------------------------------------------------------------------------------------ group 2: reaction and stop
def load_ext(rid):
    return np.load(EXTDIR / (rid + '.npz'), allow_pickle=False)


if '2' in args.groups:
    if B_ALL_W1 is None:
        S1a = Scorer(runs, ['F0', 'E'], safe_w1, lambda r: r['masks_all'], GL)
        P_ALL_W1 = S1a.point(0); B_ALL_W1 = S1a.boot(0, CNT)
    ext = {}
    for r in runs:
        x = load_ext(r['run'])
        assert np.array_equal(np.asarray(x['k'], np.int64), np.asarray(r['k'], np.int64)), r['run']
        if 'evaluated' in x.files:
            assert np.array_equal(x['evaluated'].astype(bool), r['ev']), r['run']
        ext[r['run']] = {f + L.vkey(t, a): x[f + L.vkey(t, a)] for t, a in VARIANTS for f in ('clearX_', 'clear61_', 'cens_')}
    NM2 = ['F0', 'E', 'O', 'N', 'CK3', 'NA', 'A1', 'Q']
    d2 = dict(three_s=dict(denE=P_ALL_W1['denE'], R_pp=P_ALL_W1['denE'] / L.NLEV), est={}, as_scored_points={})
    for (tau, A) in VARIANTS:
        kk = L.vkey(tau, A); base = 'LB.RS.%s.%s' % (TSTR[tau], ASTR[A])
        S2 = Scorer(runs, NM2, lambda r, kk=kk: L.clean_clear(ext[r['run']]['clearX_' + kk]) > 0., lambda r: r['masks_all'], GL)
        p = S2.point(0); den0 = p['D']['O']; n = p['n']
        V[base + '.rel'] = ratio(p['denE'], P_ALL_W1['denE'])
        V[base + '.den0.dec'] = L.dec_eq(den0, n)
        V[base + '.RR0_N'] = ratio(p['D']['N'], den0)
        V[base + '.RR0_CK3'] = ratio(p['D']['CK3'], den0)
        ent = dict(n=n, denE=p['denE'], den0=den0, den0_pp=den0 / L.NLEV, E_rr0=ratio(p['denE'], den0),
                   RR0={a: ratio(p['D'][a], den0) for a in NM2[3:]}, D_dec={a: L.dec_eq(p['D'][a], n) for a in NM2[3:]})
        if A == 6.0:
            b = S2.boot(0, CNT, ['F0', 'E', 'O', 'N', 'CK3'])
            rel = C11.rat(b['denE'], B_ALL_W1['denE']); r0 = C11.rat(b['D']['N'], b['D']['O'])
            put_ci(base + '.rel.ci', pct(rel)); put_ci(base + '.RR0_N.ci', pct(r0))
            ent.update(rel_invalid_share=invalid(rel), RR0_N_invalid_share=invalid(r0), share_resamples_den0_le0=float(np.mean(~(b['D']['O'] > 0))),
                       den0_dec_ci=pct(L.dec_eq(b['D']['O'], b['n'])), RR0_CK3_ci=pct(C11.rat(b['D']['CK3'], b['D']['O'])))
        d2['est'][kk] = ent
        Sa = Scorer(runs, ['F0', 'E', 'O', 'N', 'CK3'], lambda r, kk=kk: L.clean_clear(ext[r['run']]['clear61_' + kk]) > 0.,
                    lambda r: r['masks_all'], GL)
        q = Sa.point(0)
        d2['as_scored_points'][kk] = dict(rel=ratio(q['denE'], P_ALL_W1['denE']), den0_dec=L.dec_eq(q['D']['O'], q['n']),
                                          RR0_N=ratio(q['D']['N'], q['D']['O']), RR0_CK3=ratio(q['D']['CK3'], q['D']['O']))
        log('group 2: %s done' % kk)
    kk = L.vkey(0.75, 6.0)
    for lab, sfn in (('gap2', lambda r: L.clean_clear(ext[r['run']]['clearX_' + kk]) > GAP),
                     ('gap2_censored_unsafe', lambda r: (L.clean_clear(ext[r['run']]['clearX_' + kk]) > GAP)
                      & ~(ext[r['run']]['cens_' + kk].astype(bool) & r['ev'][:, None]))):
        Sg = Scorer(runs, NM2, sfn, lambda r: r['masks_all'], GL, shift=GAP)
        p = Sg.point(0); den0 = p['D']['O']; n = p['n']
        e = dict(n=n, den0_pp=den0 / L.NLEV, den0_dec=L.dec_eq(den0, n), E_rr0=ratio(p['denE'], den0),
                 RR0={a: ratio(p['D'][a], den0) for a in NM2[3:]},
                 decisions_without_safe_row=int(sum(int((r['ev'] & ~sfn(r).any(axis=1)).sum()) for r in runs)))
        d2[lab] = e
        if lab == 'gap2':
            V['LB.gap2.den0.dec'] = e['den0_dec']; V['LB.gap2.RR0_N'] = e['RR0']['N']; V['LB.gap2.RR0_CK3'] = e['RR0']['CK3']
    DT['group2'] = d2
    del S2, Sa, Sg, ext
    log('group 2 done (%s)' % mem())


# ------------------------------------------------------------------------------------------------ group 3: truncation
def trunc_masks(r):
    """rev_b R12a masks (T = 0 .. 20 s, all) and cut5 (CD_DEFINITIONS_S57B sec. 5)."""
    ph = r['ph']; k = np.asarray(r['k'], np.int64); ev = r['ev']
    i2 = np.nonzero(ph == 2)[0]
    kstop = int(k[i2[0]]) if i2.size else None
    since = (k - kstop) * L.H if kstop is not None else np.full(k.shape, np.nan)
    ms = [ev & ((ph != 2) | (since < T - 1e-9)) for T in TRUNC] + [ev.copy()]
    ms.append(ev.copy() if kstop is None else ev & (since + 3.0 <= 5.0 + 1e-9))
    r['_kstop'] = kstop
    return tuple(ms)


if '3' in args.groups:
    NM3 = ['F0', 'E', 'CK3', 'N', 'NA', 'A1', 'Q', 'O']
    for r in runs:
        r['masks_trunc'] = trunc_masks(r)
    d3 = dict(runs_without_stop=[r['run'] for r in runs if r['_kstop'] is None])
    labs = ['T%d' % T for T in TRUNC] + ['Tall', 'cut5']
    for pi, lab in enumerate(labs):                  # one population at a time (memory)
        S3 = Scorer(runs, NM3, safe_w1, lambda r, pi=pi: (r['masks_trunc'][pi],), GL)
        p = S3.point(0)
        d3[lab] = dict(n=p['n'], R_pp=p['denE'] / L.NLEV, R_dec=L.dec_eq(p['denE'], p['n']), den0_pp=p['D']['O'] / L.NLEV,
                       RR={a: ratio(p['D'][a], p['denE']) for a in NM3[2:]})
        if lab != 'Tall':
            V['LB.%s.R' % lab] = p['denE'] / L.NLEV; V['LB.%s.RR_CK3' % lab] = ratio(p['D']['CK3'], p['denE'])
    DT['group3'] = d3
    del S3
    log('group 3 done (%s)' % mem())


# ------------------------------------------------------------------------------------------------ group 4: caution caps, signed caution
def eval_capped(T, names, cap):
    """L.eval_scoring's step frontier on the levels linspace(c0, min(C, cap), 201) (CD_DEFINITIONS_S57B sec. 6); None if empty."""
    cur = L.curves_w(T, 0)
    cF0, wF0 = cur['F0']; cE, wE = cur['E']
    c0 = cF0[0]; C = min(np.nanmax(cF0), np.nanmax(cE)); top = min(C, cap)
    if not (top > c0):
        return dict(c0=float(c0), C=float(C), top=float(top), empty=True)
    lev = np.linspace(c0, top, L.NLEV)
    fF0 = L.frontier(cF0, wF0, lev); fE = L.frontier(cE, wE, lev)
    return dict(c0=float(c0), C=float(C), top=float(top), empty=False, denE=float(np.sum(fF0 - fE)),
                D={a: float(np.sum(fF0 - L.frontier(cur[a][0], cur[a][1], lev))) for a in names})


if '4' in args.groups:
    NM4 = ['F0', 'E', 'N', 'CK3', 'NA', 'A1', 'Q']
    S4 = Scorer(runs, NM4, safe_w1, lambda r: r['masks_all'], GL)
    T4 = S4.curves(0)
    d4 = dict(uncapped=dict(R_pp=S4.point(0)['denE'] / L.NLEV), caps={})
    for cap in CAPS:
        e = eval_capped(T4, NM4[2:], cap)
        V['LB.cap%d.R' % cap] = None if e['empty'] else e['denE'] / L.NLEV
        if not e['empty']:
            e['RR'] = {a: ratio(e['D'][a], e['denE']) for a in NM4[2:]}; e['R_pp'] = e['denE'] / L.NLEV
        d4['caps']['cap%d' % cap] = e
    e = eval_capped(T4, NM4[2:], 1e9)
    d4['check_cap_above_C_equals_uncapped'] = bool(e['denE'] == S4.point(0)['denE'])
    Ss = Scorer(runs, NM4 + ['O'], safe_w1, lambda r: r['masks_all'], GL, rs_fn=row_stats_signed, signed=True)
    p = Ss.point(0)
    V['LB.signed.R'] = p['denE'] / L.NLEV; V['LB.signed.RR_N'] = ratio(p['D']['N'], p['denE']); V['LB.signed.RR_CK3'] = ratio(p['D']['CK3'], p['denE'])
    d4['signed'] = dict(n=p['n'], denE=p['denE'], R_pp=p['denE'] / L.NLEV, den0=p['D']['O'], RR={a: ratio(p['D'][a], p['denE']) for a in NM4[2:]},
                        RR0={a: ratio(p['D'][a], p['D']['O']) for a in NM4[2:]}, n_evaluated_without_W1_safe_row=int(sum(
                            int((r['ev'] & ~(r['clear1'] > 0.).any(axis=1)).sum()) for r in runs)))
    DT['group4'] = d4
    del S4, Ss
    log('group 4 done (%s)' % mem())


# ------------------------------------------------------------------------------------------------ group 5: grid frontier, placebo, hull
if '5' in args.groups:
    NM5 = ['F0', 'E', 'N', 'P', 'CK3', 'NA', 'A1', 'Q']
    S5 = Scorer(runs, NM5, safe_w1, lambda r: r['masks_all'], gridless=False)
    p = S5.point(0, hull=('N', 'CK3'))
    V['LB.grid.RR_N'] = ratio(p['D']['N'], p['denE']); V['LB.grid.RR_P'] = ratio(p['D']['P'], p['denE'])
    V['LB.grid.RR_NmP'] = ratio(p['D']['N'] - p['D']['P'], p['denE'])
    V['LB.hull.R'] = p['hdenE'] / L.NLEV; V['LB.hull.RR_N'] = ratio(p['hD']['N'], p['hdenE']); V['LB.hull.RR_CK3'] = ratio(p['hD']['CK3'], p['hdenE'])
    d5 = dict(grid=dict(n=p['n'], R_pp=p['denE'] / L.NLEV, RR={a: ratio(p['D'][a], p['denE']) for a in NM5[2:]},
                        D_dec={a: L.dec_eq(p['D'][a], p['n']) for a in NM5[2:]}),
              hull_grid=dict(hdenE=p['hdenE'], hD=p['hD']))
    if GL:
        Sh = Scorer(runs, ['F0', 'E', 'N', 'CK3'], safe_w1, lambda r: r['masks_all'], True)
        h = Sh.point(0, hull=('N', 'CK3'))
        d5['hull_gridless_points'] = dict(R_pp=h['hdenE'] / L.NLEV, RR_N=ratio(h['hD']['N'], h['hdenE']), RR_CK3=ratio(h['hD']['CK3'], h['hdenE']))
    DT['group5'] = d5
    log('group 5 done')


# ------------------------------------------------------------------------------------------------ comparisons with the values of record (test)
def jl(p):
    return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))


def compare():
    rows = []

    def add(name, mine, rec, tol=1e-9):
        if mine is None or rec is None:
            rows.append(dict(name=name, mine=mine, record=rec, absdiff=None, ok=(mine is None and rec is None))); return
        if isinstance(mine, (list, tuple)):
            for i, (a, b) in enumerate(zip(mine, rec)):
                add('%s[%d]' % (name, i), a, b, tol)
            return
        a, b = float(mine), float(rec)
        d = 0. if (math.isnan(a) and math.isnan(b)) else abs(a - b)
        rows.append(dict(name=name, mine=a, record=b, absdiff=d, ok=bool(d <= tol)))
    PMAP = {'all': 'all', 'mov': 'moving', 'pre': 'phase0', 'brk': 'phase1', 'stop': 'phase2'}
    if args.frontier == 'grid' and args.phase == 'truth':
        a9 = jl(V12 / 'out' / 'A9_1_PLACEBO_GRIDLESS_v01.json')['a_placebo_grid']
        tg = jl(V12 / 'out' / 'A9_7B_TIMEGAP_SCORE_v01.json')['w1']
        if '1' in args.groups:
            for pn, rn in PMAP.items():
                e = a9[rn]
                add('A9-1(a) %s n' % rn, V['LB.%s.n_dec' % pn], e['n'], 0)
                add('A9-1(a) %s R' % rn, V['LB.%s.R' % pn], e['R']['point']); add('A9-1(a) %s R.ci' % rn, V['LB.%s.R.ci' % pn], e['R']['ci'])
                for key, rec in (('N', 'N'), ('NA', 'NA'), ('AM', 'A1'), ('CK3', 'CK3'), ('Q', 'Q')):
                    add('A9-1(a) %s RR_%s' % (rn, key), V['LB.%s.RR_%s' % (pn, key)], e['RR_' + rec]['point'])
                    add('A9-1(a) %s RR_%s.ci' % (rn, key), V['LB.%s.RR_%s.ci' % (pn, key)], e['RR_' + rec]['ci'])
                add('A9-7B %s RR_TG2' % rn, V['LB.%s.RR_TG' % pn], tg[rn]['RR_TG2']['point'])
                add('A9-7B %s RR_TG2.ci' % rn, V['LB.%s.RR_TG.ci' % pn], tg[rn]['RR_TG2']['ci'])
        if '2' in args.groups:
            e2 = jl(V11 / 'out' / 'REV_E2_EXTENDED_TRUTH_v01.json')['scorings']
            for (tau, A) in VARIANTS:
                kk = L.vkey(tau, A); base = 'LB.RS.%s.%s' % (TSTR[tau], ASTR[A]); e = e2['est_' + kk]['pops']['all']
                add('rev_e2 est_%s rel' % kk, V[base + '.rel'], e['denE_over_3s']['point'])
                add('rev_e2 est_%s den0.dec' % kk, V[base + '.den0.dec'], e['den0']['dec_eq'])
                add('rev_e2 est_%s RR0_N' % kk, V[base + '.RR0_N'], e['arms']['N']['rr0']['point'])
                add('rev_e2 est_%s RR0_CK3' % kk, V[base + '.RR0_CK3'], e['arms']['CK3']['rr0']['point'])
                if A == 6.0:
                    add('rev_e2 est_%s rel.ci' % kk, V[base + '.rel.ci'], e['denE_over_3s']['ci'])
                    add('rev_e2 est_%s RR0_N.ci' % kk, V[base + '.RR0_N.ci'], e['arms']['N']['rr0']['ci'])
            ea = e2['asscored_t0p75_a6p0']['pops']['all']; m = DT['group2']['as_scored_points']['t0p75_a6p0']
            add('rev_e2 asscored_t0p75_a6p0 rel', m['rel'], ea['denE_over_3s']['point'])
            add('rev_e2 asscored_t0p75_a6p0 RR0_N', m['RR0_N'], ea['arms']['N']['rr0']['point'])
            op = jl(OPTA)['part1']['scorings']
            for tau in TAUS:
                kk = L.vkey(tau, 6.0); m = DT['group2']['as_scored_points'][kk]
                o = op['WR_' + kk]['pops']['all']; w = op['W1']['pops']['all']
                add('OptionA WR_%s rel (denE/denE_W1)' % kk, m['rel'], o['denE']['point'] / w['denE']['point'])
                add('OptionA WR_%s den0.dec' % kk, m['den0_dec'], o['den0']['dec_eq'])
                add('OptionA WR_%s RR0_N' % kk, m['RR0_N'], o['arms']['N']['rr0']['point'])
                add('OptionA WR_%s RR0_CK3' % kk, m['RR0_CK3'], o['arms']['CK3']['rr0']['point'])
            e3 = jl(V11 / 'out' / 'REV_E3_EXTENDED_GAP2_v01.json')['pops']['all']
            add('rev_e3 den0.dec', V['LB.gap2.den0.dec'], e3['den0']['dec_eq'])
            add('rev_e3 RR0_N', V['LB.gap2.RR0_N'], e3['arms']['N']['rr0']['point'])
            add('rev_e3 RR0_CK3', V['LB.gap2.RR0_CK3'], e3['arms']['CK3']['rr0']['point'])
            e4 = jl(V11 / 'out' / 'REV_E4_GAP2_CENS_UNSAFE_v01.json')['pops']['all']; m = DT['group2']['gap2_censored_unsafe']
            add('rev_e4 den0.dec', m['den0_dec'], e4['den0_dec_eq'])
            add('rev_e4 RR0_N', m['RR0']['N'], e4['arms']['N']['rr0']); add('rev_e4 RR0_CK3', m['RR0']['CK3'], e4['arms']['CK3']['rr0'])
        if '3' in args.groups:
            eb = jl(V11 / 'out' / 'REV_B_TRUNC_PHASESCALE_v01.json')['R12a']
            for T in TRUNC + [None]:
                lab = 'Tall' if T is None else 'T%d' % T; m = DT['group3'][lab]
                add('rev_b %s n' % lab, m['n'], eb[lab]['n'], 0)
                add('rev_b %s R' % lab, m['R_pp'], eb[lab]['R_pp'])
                add('rev_b %s RR_CK3' % lab, m['RR']['CK3'], eb[lab]['arms']['CK3']['rrE']['point'])
                add('rev_b %s RR_N' % lab, m['RR']['N'], eb[lab]['arms']['N']['rrE']['point'])
        if '4' in args.groups:
            ea = jl(V11 / 'out' / 'REV_A_SIGNED_GAP_v01.json')['R11']['W1_signed']['all']
            add('rev_a R11 signed R', V['LB.signed.R'], ea['denE']['R_pp'])
            add('rev_a R11 signed RR_N', V['LB.signed.RR_N'], ea['arms']['N']['rrE']['point'])
            add('rev_a R11 signed RR_CK3', V['LB.signed.RR_CK3'], ea['arms']['CK3']['rrE']['point'])
            add('rev_a R11 signed RR0_N', DT['group4']['signed']['RR0']['N'], ea['arms']['N']['rr0']['point'])
    if '5' in args.groups:
        e = jl(V12 / 'out' / 'A9_1_PLACEBO_GRIDLESS_v01.json')['a_placebo_grid']['all']
        add('A9-1(a) all RR_N', V['LB.grid.RR_N'], e['RR_N']['point']); add('A9-1(a) all RR_P', V['LB.grid.RR_P'], e['RR_P']['point'])
        add('A9-1(a) all RR_NmP', V['LB.grid.RR_NmP'], e['RR_N_minus_P']['point'])
        o = jl(OPTA)['part1']['scorings']['W1']['pops']['all']
        add('OptionA W1 hull R (hdenE/201)', V['LB.hull.R'], o['hdenE'] / L.NLEV)
        add('OptionA W1 hull RR_N (hrr0 hden0 / hdenE)', V['LB.hull.RR_N'], o['arms']['N']['hrr0']['point'] * o['hden0'] / o['hdenE'])
        add('OptionA W1 hull RR_CK3', V['LB.hull.RR_CK3'], o['arms']['CK3']['hrr0']['point'] * o['hden0'] / o['hdenE'])
    if args.frontier == 'gridless' and args.phase == 'truth' and '1' in args.groups:
        c = jl(V12 / 'out' / 'A9_1_PLACEBO_GRIDLESS_v01.json')['c_gridless']
        for pn, rn in PMAP.items():
            add('A9-1(c) %s n' % rn, V['LB.%s.n_dec' % pn], c[rn]['n'], 0)
            add('A9-1(c) %s R' % rn, V['LB.%s.R' % pn], c[rn]['R_pp'])
            for key, rec in (('N', 'N'), ('NA', 'NA'), ('AM', 'A1'), ('CK3', 'CK3'), ('Q', 'Q')):
                add('A9-1(c) %s RR_%s' % (rn, key), V['LB.%s.RR_%s' % (pn, key)], c[rn]['RR_' + rec])
        if CNT.shape[0] == c['all_intervals']['nboot']:
            ci = c['all_intervals']
            add('A9-1(c) all R.ci', V['LB.all.R.ci'], ci['R']['ci'])
            for key, rec in (('N', 'N'), ('NA', 'NA'), ('AM', 'A1'), ('CK3', 'CK3'), ('Q', 'Q')):
                add('A9-1(c) all RR_%s.ci' % key, V['LB.all.RR_%s.ci' % key], ci['RR_' + rec]['ci'])
    if args.frontier == 'gridless' and args.phase == 'est' and '1' in args.groups:
        bc = jl(BRT / 'banalysis' / 'B_CV0_v01.json'); bi = jl(BRT / 'banalysis' / 'B_B1_v01.json')
        BMAP = {'all': 'all', 'mov': 'moving', 'pre': 'est_before', 'brk': 'est_braking', 'stop': 'est_stopped'}
        for pn, rn in BMAP.items():
            e = bc['points'][rn]
            add('B_CV0 %s n' % rn, V['LB.%s.n_dec' % pn], e['n'], 0); add('B_CV0 %s R' % rn, V['LB.%s.R' % pn], e['R_pp'])
            for key in ('N', 'NA', 'AM', 'CK3', 'Q', 'E5'):
                add('B_CV0 %s RR_%s' % (rn, key), V['LB.%s.RR_%s' % (pn, key)], e['RR'][key])
            own = DT['group1'].get('imm_own_phase_points', {}).get(pn)
            if own:
                add('B_B1 %s RR_N (IMM own phase)' % rn, own['RR_N'], bi['points'][rn]['RR']['N'])
                add('B_B1 %s R (IMM own phase)' % rn, own['R_pp'], bi['points'][rn]['R_pp'])
        add('B_B1 all RR_N = LB.all.RR_IMM', V['LB.all.RR_IMM'], bi['points']['all']['RR']['N'])
        if CNT.shape[0] == bc['nboot']:
            ia = bc['intervals']['all']
            add('B_CV0 all R.ci', V['LB.all.R.ci'], ia['R_pp']['ci'])
            for key in ('N', 'NA', 'AM', 'CK3', 'Q', 'E5'):
                add('B_CV0 all RR_%s.ci' % key, V['LB.all.RR_%s.ci' % key], ia['RR_' + key]['ci'])
            add('B_B1 all RR_N.ci = LB.all.RR_IMM.ci', V['LB.all.RR_IMM.ci'], bi['intervals']['all']['RR_N']['ci'])
    return dict(n=len(rows), n_ok=sum(r['ok'] for r in rows), max_absdiff=max([r['absdiff'] for r in rows if r['absdiff'] is not None] or [0.]),
                failures=[r for r in rows if not r['ok']], rows=rows)


if args.test_old:
    DT['comparison_with_record'] = compare()
    c = DT['comparison_with_record']
    log('comparison with the values of record: %d of %d agree within tolerance; largest difference %.3g' % (c['n_ok'], c['n'], c['max_absdiff']))


# ------------------------------------------------------------------------------------------------ write
def clean(x):
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        return float(x) if math.isfinite(float(x)) else None
    return x


KL = CC.CD / 'export' / 'A_KEYS_CD_v13.json'
keys = set(k['key'] for k in jl(KL)['keys']['C'])
base_of = lambda k: k[:-6] + '.ci' if k.endswith('.level') else (k[:-4] + '.ci' if k.endswith('.cal') else k)
mine = [k for k in V if not (k.endswith('.level') or k.endswith('.cal'))]
extra = sorted(k for k in mine if k not in keys)
# keys that A no longer reads from package C (e.g. LB.RS.0.75.6.rel(.ci), mapped to B:LB.RS075.rel by A's rename_v13.json since
# 20 Nov 03:29) stay out of `values` and are kept in details as cross-checks
DT['values_not_in_key_list'] = clean({k: V[k] for k in V if base_of(k) in extra})
V = {k: v for k, v in V.items() if base_of(k) not in extra}
DT['keys'] = dict(key_list=str(KL), key_list_sha256=CC.sha(KL), n_values=len(mine) - len(extra), not_in_key_list=extra)
DT['peak_memory'] = mem()
DT['gl_fast_event_filter'] = dict(note='prep_filtered: zero-statistics events dropped; checked equal on the first %d resamples of every bootstrap' % NCHK_FILTER, calls=FILTER_LOG)
DT['gate'] = gate; DT['seconds'] = time.time() - t00; DT['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
DT['code_sha256'] = {f: CC.sha(CC.HERE / f) for f in ('c_s57b_v13.py', 'cd_common_v13.py', 'gl_fast_v13.py', 'x_rsx_extract_v13.py')}
doc = dict(family='S57B', program='c_s57b_v13.py', test_old=bool(args.test_old), values=clean(V), details=clean(DT))
OUTF.parent.mkdir(parents=True, exist_ok=True)
with open(OUTF, 'x', encoding='utf-8') as f:
    f.write(json.dumps(doc, indent=1, allow_nan=False))
log('written %s (%d values)' % (OUTF.name, len(mine) - len(extra)))
