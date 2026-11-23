"""Recount (second program) of package C, lead braking: H0-H5 of AMENDMENT_10_v13 section 5.3. New file, 19 Nov 2026
(Claude Fable 5.2). Written from A10 (sections 0, 2, 5.1-5.5, 5.8, 10.1) and CD_DEFINITIONS_v13.md; no first program was read.

Computes, on the lead-braking run set (all evaluated decisions, 3 s commitment):
  H0  R_gl = D_gl(E, F0) / 201 and the share of resamples with D_gl(E, F0) > 0;
  H1  RR_gl(E5), RR_gl(E5p), RR_gl(E5) - RR_gl(E5p);
  H2  RR_gl(N) against (-delta, delta), delta = 0.05;
  H3  (B1 arrays) r = RR_gl(N_IMM), c = RR_gl(E5_IMM) on the IMM's own room, the classification, 'barely varies', r / c;
  H4  the per-phase schedule chosen on the 35 old runs and transferred once: record basis and like-for-like basis, with the
      truth phase and the thresholds -0.5 and -2.0 as sensitivities (grid frontier);
  H5  RR_gl(CK3);
  the A10 section 2.6 calibrated level of every hypothesis statistic; the fixed sequence; descriptive RR_gl of NA, AM, Q, TG.
Intervals: run bootstrap boot_counts(n, 20000, 20261911), percentile, at the level the calibration gives.

Usage (python -I -B -X utf8):
  rc_c_lead_v13.py --test-old [--boot 200 --outer 10 --inner 50 --mc 200 --workers 2]     old runs as stand-in (IMM skipped)
  rc_c_lead_v13.py --stage design                                                          H4 design choices only (old runs)
  rc_c_lead_v13.py [--workers N]                                                           fresh runs; refuses before Lock 2
  ... --calib export                    everything except the double bootstrap; writes the job out\\calib\\rc_lead.job.npz
                                        (+ .meta.json, .state.npz) and a pending output <name>.PENDING.json
  ... --calib import --calib-chunks DIR reads the chunks rc_lead_<SEED>_o<LO>_<HI>.npz that rc_calib_remote_v13.py computed,
                                        checks them and finishes the run (output as an in-process run)
Output: out\\RC_C_LEAD_v13<tag>.json (never overwritten).
"""
import argparse, json, pathlib, sys, time
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))      # python -I: the script folder is not on sys.path
import rc_core_v13 as K

L = K.L
VARIANTS = [('est_-1.0', 'est', -1.0), ('truth', 'truth', None), ('est_-0.5', 'est', -0.5), ('est_-2.0', 'est', -2.0)]


# ------------------------------------------------------------------------------------------------ H4 (grid)
def phase_of(r, kind, thr):
    if kind == 'truth':
        return np.asarray(r['ph']).astype(np.int64)
    return K.est_phase(r['vhat'], r['ahat_long'], r['lead_found'], thr)


def grid_tables(r, ph):
    """(202, 4, 5) F0 statistics on the grid of record for the populations (evaluated, phase 0, 1, 2) and (202, 5) for E."""
    ev = r['ev']
    masks = (ev, ev & (ph == 0), ev & (ph == 1), ev & (ph == 2))
    safe = r['clear1'] > 0.
    tf = L.stats_scored(L.select_grid(r['crit']['F0'], K.GRID, r['idx55']), r['clear1'], safe, r['vbar'], r['desired'], masks)
    te = L.stats_scored(L.select_grid(r['crit']['E'], K.GRID, r['idx55']), r['clear1'], safe, r['vbar'], r['desired'], (ev,))
    return tf, te[:, 0, :]


def uniq_rows(T):
    """Distinct (wrong go, caution sum, caution count) rows of a (G, 5) table in lexicographic order, with the first grid index."""
    A = T[:, 1:4]
    o = np.lexsort((np.arange(A.shape[0]), A[:, 2], A[:, 1], A[:, 0]))
    As = A[o]
    new = np.concatenate([[True], (As[1:] != As[:-1]).any(axis=1)])
    return As[new], o[new]


def choose_running_min(c, w, lev):
    """Per level: the index of the point with the lowest w among points with c <= level; ties: lowest c, then lowest index.
    -1 where no point qualifies."""
    ok = np.isfinite(c) & np.isfinite(w)
    idx = np.nonzero(ok)[0]
    if idx.size == 0:
        return np.full(lev.size, -1, np.int64)
    o = np.argsort(c[ok], kind='stable')
    cs = c[ok][o]; ws = w[ok][o]; src = idx[o]
    cm = np.minimum.accumulate(ws)
    newmin = np.concatenate([[True], cm[1:] < cm[:-1]])
    holder = np.maximum.accumulate(np.where(newmin, np.arange(ws.size), 0))
    j = np.searchsorted(cs, lev, side='right') - 1
    return np.where(j >= 0, src[holder[np.clip(j, 0, None)]], -1).astype(np.int64)


def h4_design(runs, kind, thr):
    """Design-set choice: levels of the design set's F0 / E grid curves (all evaluated decisions); per level the scale triple
    (one grid index per phase) with the lowest pooled wrong go among triples with pooled caution <= level, and a single scale
    chosen the same way."""
    tabs = [grid_tables(r, phase_of(r, kind, thr)) for r in runs]
    XF = np.stack([t[0] for t in tabs]); XE = np.stack([t[1] for t in tabs])
    w1 = np.ones(len(runs))
    Tall = np.tensordot(w1, XF[:, :, 0, :], axes=(0, 0)); TE = np.tensordot(w1, XE, axes=(0, 0))
    cur = L.curves_w({'F0': Tall, 'E': TE}, 0)
    cF0, wF0 = cur['F0']; cE, wE = cur['E']
    lev = L.levels_of(cF0, cE, cF0[0])
    single = choose_running_min(cF0, wF0, lev)
    Tph = [np.tensordot(w1, XF[:, :, q, :], axes=(0, 0)) for q in (1, 2, 3)]
    U = []; IX = []
    for T in Tph:
        u, ix = uniq_rows(T); U.append(u); IX.append(ix)
    n = float(Tph[0][0, 0] + Tph[1][0, 0] + Tph[2][0, 0])
    W = (U[0][:, 0][:, None, None] + U[1][:, 0][None, :, None] + U[2][:, 0][None, None, :]).ravel()
    S = (U[0][:, 1][:, None, None] + U[1][:, 1][None, :, None] + U[2][:, 1][None, None, :]).ravel()
    Kc = (U[0][:, 2][:, None, None] + U[1][:, 2][None, :, None] + U[2][:, 2][None, None, :]).ravel()
    with np.errstate(divide='ignore', invalid='ignore'):
        c = 100. * S / Kc; w = 100. * W / n
    flat = choose_running_min(c, w, lev)
    triple = np.full((lev.size, 3), -1, np.int64)
    okl = flat >= 0
    i0, i1, i2 = np.unravel_index(flat[okl], (U[0].shape[0], U[1].shape[0], U[2].shape[0]))
    triple[okl, 0] = IX[0][i0]; triple[okl, 1] = IX[1][i1]; triple[okl, 2] = IX[2][i2]
    # in-sample value of the design set (cross-check with v12's A9-3 on the old runs)
    Wd = np.zeros(lev.size); Sd = np.zeros(lev.size); Kd = np.zeros(lev.size)
    for q in range(3):
        g = triple[:, q]
        Wd[okl] += Tph[q][g[okl], 1]; Sd[okl] += Tph[q][g[okl], 2]; Kd[okl] += Tph[q][g[okl], 3]
    with np.errstate(divide='ignore', invalid='ignore'):
        cp = np.where(okl, 100. * Sd / Kd, np.nan); wp = np.where(okl, 100. * Wd / float(Tall[0, 0]), np.nan)
    f1 = L.frontier(cF0, wF0, lev); fE = L.frontier(cE, wE, lev)
    fps = L.frontier(np.concatenate([[cF0[0]], cp]), np.concatenate([[wF0[0]], wp]), lev)
    return dict(levels=lev, triple=triple, single=single, n_unique=[int(u.shape[0]) for u in U],
                n_levels_without_triple=int((~okl).sum()), n_levels_without_single=int((single < 0).sum()),
                n_design=float(Tall[0, 0]), n_design_in_phases=n,
                insample_share=float(np.sum(f1 - fps) / np.sum(f1 - fE)), insample_gain_pp=float(np.sum(f1 - fps) / K.NLEV),
                design_room_grid_pp=float(np.sum(f1 - fE) / K.NLEV))


# _h4_kernel and the evaluation part of H4 (frontiers, evaluate) were moved, text unchanged, to rc_kern_v13.py (20 Nov 2026),
# where the remote runner of the double bootstrap can import them.
_h4_kernel = K.KN._h4_kernel


class H4(K.KN.H4Eval):
    """Transfer of the design choices to a run set; evaluate(CN) (rc_kern_v13.H4Eval) -> per variant the record-basis and
    like-for-like shares."""

    def __init__(self, fresh, designs):
        self.names = [v[0] for v in VARIANTS]
        nrun = len(fresh); nv = len(VARIANTS)
        self.NEV = np.zeros(nrun); self.GF = None; self.GE = None
        self.ONE = np.zeros((nrun, 201, 3)); self.PS = np.zeros((nrun, nv, 201, 3))
        self.v1 = None; self.vp = np.zeros((nv, 201), np.uint8)
        self.phase3 = {}
        for vi, (nm, kind, thr) in enumerate(VARIANTS):
            d = designs[nm]
            tri = np.asarray(d['triple'], np.int64); sg = np.asarray(d['single'], np.int64)
            okl = tri[:, 0] >= 0
            self.vp[vi] = okl
            n_out = 0
            GF = []; GE = []
            for k, r in enumerate(fresh):
                ph = phase_of(r, kind, thr)
                n_out += int((r['ev'] & ~np.isin(ph, (0, 1, 2))).sum())
                tf, te = grid_tables(r, ph)
                if vi == 0:
                    GF.append(tf[:, 0, 1:4]); GE.append(te[:, 1:4]); self.NEV[k] = tf[0, 0, 0]
                for q in range(3):
                    self.PS[k, vi, okl] += tf[tri[okl, q], q + 1, 1:4]
                if vi == 0:
                    ok1 = sg >= 0
                    self.v1 = ok1.astype(np.uint8)
                    self.ONE[k, ok1] = tf[sg[ok1], 0, 1:4]
            if vi == 0:
                self.GF = np.stack(GF); self.GE = np.stack(GE)
                self.single = sg
            elif not np.array_equal(sg, self.single):
                raise SystemExit('REFUSED: the single-scale choice differs between phase variants (it must not depend on the phase)')
            self.phase3[nm] = n_out
        self.nrun = nrun; self.G = self.GF.shape[1]

    def library_point(self):
        """The full-sample value with the library's frontier and levels (Python path), for comparison with the kernel."""
        TF = self.GF.sum(axis=0); TE = self.GE.sum(axis=0); n = self.NEV.sum()
        with np.errstate(divide='ignore', invalid='ignore'):
            cF = 100. * TF[:, 1] / TF[:, 2]; wF = 100. * TF[:, 0] / n
            cE = 100. * TE[:, 1] / TE[:, 2]; wE = 100. * TE[:, 0] / n
            lev = L.levels_of(cF, cE, cF[0])
            fF = L.frontier(cF, wF, lev); fE = L.frontier(cE, wE, lev)
            T1 = self.ONE.sum(axis=0); ok1 = self.v1.astype(bool)
            f1 = L.frontier(np.concatenate([[cF[0]], 100. * T1[ok1, 1] / T1[ok1, 2]]),
                            np.concatenate([[wF[0]], 100. * T1[ok1, 0] / n]), lev)
            den = float(np.sum(fF - fE)); res = {}
            for vi, nm in enumerate(self.names):
                TP = self.PS[:, vi].sum(axis=0); okp = self.vp[vi].astype(bool)
                fp = L.frontier(np.concatenate([[cF[0]], 100. * TP[okp, 1] / TP[okp, 2]]),
                                np.concatenate([[wF[0]], 100. * TP[okp, 0] / n]), lev)
                res[nm] = dict(record_basis=L.ratio(float(np.sum(fF - fp)), den), like_for_like=L.ratio(float(np.sum(f1 - fp)), den))
        return dict(den=den, room_grid_pp=den / K.NLEV, n=float(n), variants=res)


classify_h3 = K.classify_h3
inside = K.inside


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--stage', default='all', choices=['all', 'design'])
    ap.add_argument('--boot', type=int, default=K.NBOOT)
    ap.add_argument('--outer', type=int, default=K.B_OUTER)
    ap.add_argument('--inner', type=int, default=K.B_INNER)
    ap.add_argument('--mc', type=int, default=K.B_MC)
    ap.add_argument('--workers', type=int, default=0)
    ap.add_argument('--second-seed', default='auto', choices=['auto', 'always', 'never'])
    ap.add_argument('--no-calibration', action='store_true')
    ap.add_argument('--no-library', action='store_true')
    ap.add_argument('--no-descriptive', action='store_true')
    ap.add_argument('--tag', default='')
    ap.add_argument('--calib', default='inproc', choices=['inproc', 'export', 'import'])
    ap.add_argument('--calib-chunks', default=None)
    ap.add_argument('--calib-label', default='rc_lead')
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
    if a.stage == 'design':
        name = 'RC_C_LEAD_H4_DESIGN_v13%s.json' % a.tag
    elif a.test_old:
        name = 'RC_C_LEAD_TESTOLD_b%d_o%d_i%d%s.json' % (a.boot, a.outer, a.inner, a.tag)
    else:
        name = 'RC_C_LEAD_v13%s%s.json' % ('' if full_size else '_b%d_o%d_i%d' % (a.boot, a.outer, a.inner), a.tag)
    if K.DRYRUN:
        name = 'DRYRUN_' + name
    outf = K.OUT / name
    if a.calib == 'export':
        outf = K.OUT / (name[:-5] + '.PENDING.json')
    if outf.exists():
        raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % outf)
    if not a.test_old and a.stage == 'all':
        K.require_lock2('fresh lead-braking arrays')           # before anything else: nothing of a fresh run is opened

    doc = dict(code='rc_c_lead_v13.py', role='second program (recount), AMENDMENT_10_v13 section 10.1(b)', model='claude-fable-5-2',
               mode='test-old' if a.test_old else 'fresh', started=K.clock(), calib_mode=a.calib,
               dryrun=('OLD runs relabelled as fresh in a scratch tree; NOT fresh data' if K.DRYRUN else False), threads=nthreads,
               sizes=dict(boot=a.boot, outer=a.outer, inner=a.inner, mc=a.mc), delta=K.DELTA,
               seeds=dict(boot=K.SEED_BOOT, outer=K.SEED_OUTER, inner=K.SEED_INNER, inner2=K.SEED_INNER2, perm=K.SEED_PERM, mc=K.SEED_MC))

    # ---------------- H4 design on the old runs (exploratory data of record; allowed before Lock 2)
    design_runs = K.load_old_eval_runs()
    designs = {}
    for nm, kind, thr in VARIANTS:
        designs[nm] = h4_design(design_runs, kind, thr)
        print('H4 design %s: in-sample share on the design set %.12f (%.0f s)' % (nm, designs[nm]['insample_share'], time.time() - t00),
              flush=True)
    doc['H4_design'] = {nm: dict(d, levels=d['levels'].tolist(), triple=d['triple'].tolist(), single=d['single'].tolist())
                        for nm, d in designs.items()}
    doc['H4_design']['design_runs'] = [r['run'] for r in design_runs]
    try:
        v12 = json.loads((K.V12 / 'out' / 'A9_3_PHASE_SCALE_CV_v02.json').read_text(encoding='utf-8'))
        ref = {'est_-1.0': v12['b_estimated_phase']['-1.0']['insample']['share'], 'truth': v12['a_truth_phase']['insample']['share'],
               'est_-0.5': v12['b_estimated_phase']['-0.5']['insample']['share'], 'est_-2.0': v12['b_estimated_phase']['-2.0']['insample']['share']}
        doc['H4_design']['check_vs_v12_A9_3_insample_share'] = {nm: dict(here=designs[nm]['insample_share'], v12=ref[nm],
                                                                        abs_diff=abs(designs[nm]['insample_share'] - ref[nm])) for nm in ref}
        print('H4 design vs v12 A9-3 in-sample shares: max |diff| %.3g'
              % max(x['abs_diff'] for x in doc['H4_design']['check_vs_v12_A9_3_insample_share'].values()), flush=True)
    except Exception as e:
        doc['H4_design']['check_vs_v12_A9_3_insample_share'] = 'not available: %s' % e
    if a.stage == 'design':
        doc['written'] = K.clock(); doc['seconds'] = time.time() - t00
        print('written %s' % K.write_new(outf, doc)); return

    # ---------------- run set
    if a.test_old:
        runs = K.load_old_eval_runs(); imm = None
    else:
        K.require_lock2('fresh lead-braking arrays')
        runs = K.load_fresh_runs('lead_braking', 'CV0')
        imm = K.load_fresh_runs('lead_braking', 'B1')
        for r, q in zip(runs, imm):
            if not (r['run'] == q['run'] and np.array_equal(r['k'], q['k']) and np.array_equal(r['ev'], q['ev'])):
                raise SystemExit('REFUSED: CV0 and B1 arrays of %s do not describe the same decisions' % r['run'])
    n = len(runs)
    doc['runs'] = [r['run'] for r in runs]
    doc['counts'] = dict(n_runs=n, n_decisions=int(sum(r['ev'].size for r in runs)), n_evaluated=int(sum(r['ev'].sum() for r in runs)),
                         evaluated_per_run=[int(r['ev'].sum()) for r in runs])
    A9 = None if a.no_library else K.try_a9()

    # ---------------- E5 family on the online tracker
    u, uinfo = K.e5_u(runs, 'F0', 'E')
    up = K.permute_u(runs, u)
    for r, uu, pp in zip(runs, u, up):
        r['crit']['E5'] = K.oracle_crit(r['crit']['F0'], K.RATIO, K.E5_AMP, uu)
        r['crit']['E5p'] = K.oracle_crit(r['crit']['F0'], K.RATIO, K.E5_AMP, pp)
    doc['E5'] = dict(uinfo, m=K.RATIO, A=K.E5_AMP)
    rs = K.ratio_summary(np.concatenate([K.margin_ratio_values(r) for r in runs]))
    doc['margin_ratio_N'] = rs
    preps = [K.Prep(r) for r in runs]
    ev_masks = lambda k: [runs[k]['ev']]                       # noqa: E731
    hyp_names = ['F0', 'E', 'N', 'E5', 'E5p', 'CK3']
    desc_names = [] if a.no_descriptive else [x for x in ('NA', 'A1', 'Q', 'TG') if all(x in r['crit'] for r in runs)]
    curves = {nm: K.build_curves(runs, preps, nm, ev_masks)[0] for nm in hyp_names + desc_names}
    PA = K.Problem(hyp_names, [curves[x] for x in hyp_names])
    PD = K.Problem(['F0', 'E'] + desc_names, [curves[x] for x in ['F0', 'E'] + desc_names]) if desc_names else None
    doc['gridless_sizes'] = {nm: dict(events=curves[nm].n_events_all, events_kept=int(curves[nm].ri.size), points=curves[nm].npts)
                             for nm in curves}
    print('curves built (%.0f s): %s' % (time.time() - t00, {k: v['points'] for k, v in doc['gridless_sizes'].items()}), flush=True)

    # ---------------- IMM (H3)
    PI = None
    if imm is not None:
        ui, uiinfo = K.e5_u(imm, 'F0', 'E')
        rsi = K.ratio_summary(np.concatenate([K.margin_ratio_values(r) for r in imm]))
        for r, uu in zip(imm, ui):
            r['crit']['E5x'] = K.oracle_crit(r['crit']['F0'], rsi['median'], rsi['A'], uu)
        preps_i = [K.Prep(r) for r in imm]
        im_masks = lambda k: [imm[k]['ev']]                    # noqa: E731
        inames = ['F0', 'E', 'N', 'E5x']
        icurves = {nm: K.build_curves(imm, preps_i, nm, im_masks)[0] for nm in inames}
        PI = K.Problem(inames, [icurves[x] for x in inames])
        doc['IMM'] = dict(e5_u=uiinfo, margin_ratio=rsi, m=rsi['median'], A=rsi['A'], barely_varies=rsi['barely_varies'])
    hx = H4(runs, designs)
    doc['H4_phase_outside_0_1_2_evaluated'] = hx.phase3

    # ---------------- statistics of a batch of run counts
    STATS = ['R_gl_pp', 'RR_E5', 'RR_E5_minus_E5p', 'RR_N', 'RR_CK3', 'RR_E5p']
    if PI is not None:
        STATS += ['IMM_R_gl_pp', 'IMM_r', 'IMM_c', 'IMM_r_over_c']
    for nm in hx.names:
        STATS += ['H4_rec_' + nm, 'H4_lfl_' + nm]
    SI = {s: i for i, s in enumerate(STATS)}
    stat_fn = K.KN.LeadStat(PA, PI, hx, STATS)          # the statistics of a batch of run counts (rc_kern_v13)

    # ---------------- points
    kp = {}
    full = stat_fn(np.ones((1, n)), kp)[0]
    e = kp['e']; nn = float(e['n'][0]); den = float(e['denE'][0])
    pts = dict(n=nn, denE=den, R_gl_pp=den / K.NLEV, R_gl_deceq=L.dec_eq(den, nn),
               D={x: float(e['D'][x][0]) for x in e['D']}, RR={x: L.ratio(float(e['D'][x][0]), den) for x in e['D']},
               D_deceq={x: L.dec_eq(float(e['D'][x][0]), nn) for x in e['D']})
    doc['point'] = dict(gridless=pts, stats={s: float(v) for s, v in zip(STATS, full)})
    if PI is not None:
        ei = kp['ei']; di = float(ei['denE'][0]); ni = float(ei['n'][0])
        doc['point']['IMM'] = dict(n=ni, denE=di, R_gl_pp=di / K.NLEV, R_gl_deceq=L.dec_eq(di, ni),
                                   r=L.ratio(float(ei['D']['N'][0]), di), c=L.ratio(float(ei['D']['E5x'][0]), di),
                                   D_deceq={x: L.dec_eq(float(ei['D'][x][0]), ni) for x in ei['D']})
    h = kp['h']
    doc['point']['H4'] = dict(den=float(h['den'][0]), room_grid_pp=float(h['den'][0]) / K.NLEV, n=float(h['n'][0]),
                              variants={nm: dict(record_basis=float(h['rec'][0, vi]), like_for_like=float(h['lfl'][0, vi]))
                                        for vi, nm in enumerate(hx.names)},
                              library_path=hx.library_point())
    lp = doc['point']['H4']['library_path']
    doc['point']['H4']['max_abs_diff_kernel_vs_library_path'] = float(max(
        [abs(lp['den'] - float(h['den'][0]))] + [abs(lp['variants'][nm][b] - doc['point']['H4']['variants'][nm][b])
                                                  for nm in hx.names for b in ('record_basis', 'like_for_like')]))
    if PD is not None:
        ed = PD.evaluate(np.ones((1, n)))
        doc['point']['descriptive'] = {x: dict(RR_gl=L.ratio(float(ed['D'][x][0]), float(ed['denE'][0])),
                                               D_deceq=L.dec_eq(float(ed['D'][x][0]), nn)) for x in desc_names}
    # library of record: a9 gridless curves + eval_scoring (must be identical, bit for bit)
    if A9 is not None:
        allm = lambda k: (runs[k]['ev'],)                      # noqa: E731
        el, _ = K.library_point(A9, runs, hyp_names + desc_names, allm, 0, 'F0', 'E')
        lib = dict(denE=el['denE'], n=el['n'], D=el['D'])
        mine = dict(pts['D'])
        if PD is not None:
            mine.update({x: float(ed['D'][x][0]) for x in desc_names})
        ident = bool(el['denE'] == den and el['n'] == nn and all(el['D'][x] == mine[x] for x in mine))
        doc['point']['library_of_record'] = dict(lib, RR={x: L.ratio(el['D'][x], el['denE']) for x in el['D'] if x != 'E'},
                                                 identical_to_recount_kernel=ident,
                                                 max_abs_diff=float(max([abs(el['denE'] - den)] + [abs(el['D'][x] - mine[x]) for x in mine])))
        print('library of record vs kernel (full sample, CV0): identical = %s' % ident, flush=True)
        if PI is not None:
            im = lambda k: (imm[k]['ev'],)                     # noqa: E731
            eli, _ = K.library_point(A9, imm, ['F0', 'E', 'N', 'E5x'], im, 0, 'F0', 'E')
            identi = bool(eli['denE'] == di and all(eli['D'][x] == float(ei['D'][x][0]) for x in ei['D']))
            doc['point']['IMM']['library_of_record'] = dict(denE=eli['denE'], D=eli['D'], identical_to_recount_kernel=identi)
            print('library of record vs kernel (full sample, B1): identical = %s' % identi, flush=True)
    print('points done (%.0f s)' % (time.time() - t00), flush=True)

    # ---------------- main bootstrap
    t1 = time.time()
    st = K.calib_state(cdir, a.calib_label, full, a.boot) if a.calib == 'import' else None
    if st is not None and all(('DESC_' + x) in st for x in desc_names):
        # the main bootstrap of the export run (the same arrays; it is not computed twice)
        BS = st['BS']; DEN = st['DEN']; DENI = st['DENI']
        DESC = {x: st['DESC_' + x] for x in desc_names} if PD is not None else None
        print('main bootstrap: taken from the export run (%s.state.npz)' % a.calib_label, flush=True)
    else:
        CNT = K.boot_counts(n, K.NBOOT, K.SEED_BOOT)[:a.boot]
        BS = np.empty((a.boot, len(STATS)))
        DEN = np.empty(a.boot); DENI = np.full(a.boot, np.nan)
        for s0 in range(0, a.boot, 1000):
            kk = {}
            BS[s0:s0 + 1000] = stat_fn(CNT[s0:s0 + 1000], kk)
            DEN[s0:s0 + 1000] = kk['e']['denE']
            if PI is not None:
                DENI[s0:s0 + 1000] = kk['ei']['denE']
        DESC = None
        if PD is not None:
            ed = PD.evaluate(CNT)
            DESC = {x: K.ratio_arr(ed['D'][x], ed['denE']) for x in desc_names}
    doc['bootstrap'] = dict(n_resamples=int(a.boot), seconds=time.time() - t1,
                            share_den_gt0=float(np.mean(DEN > 0)), n_den_le0_or_nonfinite=int((~(DEN > 0)).sum()))
    print('main bootstrap done: %d resamples in %.0f s' % (a.boot, time.time() - t1), flush=True)

    # ---------------- calibration (A10 2.6)
    cal = {}
    if not a.no_calibration:
        base = name[:-5]
        if a.calib == 'export':
            state = dict(n_boot=np.int64(a.boot), BS=BS, DEN=DEN, DENI=DENI)
            if DESC is not None:
                state.update({'DESC_' + x: DESC[x] for x in desc_names})
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
                                  seconds_inner1=db1.seconds, seconds_inner2=(db2.seconds if db2 is not None else None),
                                  outer_den_le0=int((~(db1.outer_est[:, SI['R_gl_pp']] > 0)).sum()))
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
    if DESC is not None:
        doc['descriptive'] = {x: K.summ(DESC[x], doc['point']['descriptive'][x]['RR_gl'], 0.95) for x in desc_names}

    # ---------------- hypotheses in the fixed sequence
    d = K.DELTA
    H = {}
    ci = iv['R_gl_pp']['ci']
    H['H0'] = dict(statistic='R_gl_pp', lower=ci[0], share_den_gt0=doc['bootstrap']['share_den_gt0'],
                   passes=bool(np.isfinite(ci[0]) and ci[0] > 0 and doc['bootstrap']['share_den_gt0'] >= 0.975))
    H['H1'] = dict(lower_RR_E5=iv['RR_E5']['ci'][0], lower_diff=iv['RR_E5_minus_E5p']['ci'][0],
                   passes=bool(iv['RR_E5']['ci'][0] > 0 and iv['RR_E5_minus_E5p']['ci'][0] > 0))
    H['H2'] = dict(ci=iv['RR_N']['ci'], delta=d, passes=inside(iv['RR_N']['ci'], d))
    if PI is not None:
        code, word = classify_h3(iv['IMM_r']['ci'], iv['IMM_c']['ci'], d)
        H['H3'] = dict(r=iv['IMM_r'], c=iv['IMM_c'], classification=word, branch=code, barely_varies=doc['IMM']['barely_varies'],
                       passes=code in ('a', 'b', 'c'))
        if code == 'a':
            H['H3']['efficiency_r_over_c'] = iv['IMM_r_over_c']
    else:
        H['H3'] = dict(passes=None, note='skipped: no B1 arrays for the old runs (test mode)')
    k4 = 'H4_rec_' + hx.names[0]
    H['H4'] = dict(statistic=k4, lower=iv[k4]['ci'][0], passes=bool(iv[k4]['ci'][0] > 0.5),
                   like_for_like=iv['H4_lfl_' + hx.names[0]],
                   sensitivities={nm: dict(record_basis=iv['H4_rec_' + nm], like_for_like=iv['H4_lfl_' + nm]) for nm in hx.names[1:]})
    H['H5'] = dict(lower=iv['RR_CK3']['ci'][0], passes=bool(iv['RR_CK3']['ci'][0] > 0.5))
    ok = True
    for hk in ('H0', 'H1', 'H2', 'H3', 'H4', 'H5'):
        p = H[hk]['passes']
        H[hk]['earlier_all_passed'] = ok
        H[hk]['confirmed'] = bool(p and ok) if p is not None else None
        H[hk]['label'] = ('confirmed' if (p and ok) else ('not confirmed' if ok else 'not confirmatory')) if p is not None else 'skipped'
        if p is not None:
            ok = ok and bool(p)
    doc['hypotheses'] = H
    doc['written'] = K.clock(); doc['seconds'] = time.time() - t00
    print('written %s (%.0f s)' % (K.write_new(outf, doc), time.time() - t00))


if __name__ == '__main__':
    main()
