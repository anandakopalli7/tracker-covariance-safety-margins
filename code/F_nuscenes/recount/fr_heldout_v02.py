"""Package F recount, held-out quantities under the clearance departure of 19 Nov 2026 (notes\\F_DEPARTURE_CLEARANCE_v01.md).
New file, 20 Nov 2026; a copy of fr_heldout_v01.py with these changes only:
  * `clear` / `clear2` of the val scenes are read from cache\\clear_v02\\val (K.swap_clear_v02), for T1 and IMM alike;
  * the primary horizon comes from recount\\F_RECOUNT_HORIZON_v02.json;
  * the export gains F.clearance, F.prereg.* (the v01 horizon recount), F.design.* from v02 and F.design.removed<h>.<source>;
  * if the v02 horizon rule also stops, only the export is written (F.status = "no_room_design"), and no val file is opened.

The v01 text follows.
Package F recount: the held-out quantities (A10 8.5) on the nuScenes val scenes. New file, 19 Nov 2026.
Writer: Claude Fable 5.2 (independent second program; see fr_core_v01.py). NOT TO BE RUN BEFORE LOCK 2: the loader refuses the
val split until LOCK_A10_2.txt exists (A10 8.6).

At the primary horizon (from recount\\F_RECOUNT_HORIZON_v01.json, or --horizon 3|2, recorded):
  T1 (CANMOT):  R_gl, RR_gl(N); descriptive: RR_gl of TG, E5 (f = 1.1029 (1 + 0.05 (2u - 1))), E5p (u permuted within scenes,
                default_rng(20261915)), RR_gl(E5) - RR_gl(E5p), and the partial oracles PO25/50/75 (default_rng(20261919)).
  IMM (B1):     its own room R_gl,IMM; r = RR_gl(N_IMM); the ceiling c_IMM = RR_gl(E5_IMM) (E5_IMM per A10 2.2 on the val IMM
                arrays); the efficiency r / c; the margin-ratio summary (median m, q05, q95, A, share within 5% of the median).
  Each with the 20,000-resample interval of default_rng(20261923); the hypothesis statistics (R_gl, RR_gl(N), R_gl,IMM, r, c,
  r / c) with the A10 2.6 calibration: double bootstrap, 2,000 outer (20261912) x 1,000 inner (20261913); second inner seed
  20261914 and Monte Carlo SD (20261920) when a calibrated level is needed. Then F-H0, F-H1, F-H2 in sequence.
Populations: all evaluated decisions (primary: hypotheses, calibration); evaluated decisions with `inpath` (secondary:
points and 95% percentile intervals, no calibration, no verdict).
Every share also as D_gl in decision-equivalents (D / 201 / 100 x decisions), with its interval at the share's level.
Also writes work\\F_nuscenes\\out\\A_RECOUNT_F.json (RESULTS_INTERFACE_v13.md section 1); nothing else in out is read or listed.

Usage: python -I fr_heldout_v01.py [--horizon 3|2] [--threads N]
       python -I fr_heldout_v01.py --synth [--quick]     (synthetic arrays; --quick: 200 x 100 double bootstrap, 2,000 primary)
"""
import json, sys, time
sys.dont_write_bytecode = True
import numpy as np
import pathlib as _pl
sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
import numba as nb
import fr_core_v01 as K
import fr_run_v01 as R

L = K.L
SYNTH = '--synth' in sys.argv; QUICK = '--quick' in sys.argv
if QUICK and not SYNTH:
    raise SystemExit('--quick is for synthetic arrays only')
ROOT = (K.HERE / 'synth') if SYNTH else None
OUTD = (K.HERE / 'synth' / 'out') if SYNTH else K.HERE
OUTF = OUTD / ('F_RECOUNT_HELDOUT_synth_v02.json' if SYNTH else 'F_RECOUNT_HELDOUT_v02.json')
AOUT = (OUTD / 'A_RECOUNT_F_synth_v02.json') if SYNTH else (K.HERE.parent / 'out' / 'A_RECOUNT_F.json')
DESC = ['TG', 'E5', 'E5p', 'PO25', 'PO50', 'PO75']          # T1 kernel columns 5.. (after n, c0, C, D_E, D_N)
STATS = ['R_gl_T1', 'RR_gl_N', 'R_gl_IMM', 'r_RR_gl_N_IMM', 'c_RR_gl_E5_IMM', 'efficiency_r_over_c']
SHARED = ['sweep', 'idx55', 'vbar', 'des', 'inpath']
HZ1 = (K.HERE / 'synth' / 'out' / 'F_RECOUNT_HORIZON_synth.json') if SYNTH else (K.HERE / 'F_RECOUNT_HORIZON_v01.json')
HZ2 = (K.HERE / 'synth' / 'out' / 'F_RECOUNT_HORIZON_synth_clear_v02.json') if SYNTH else (K.HERE / 'F_RECOUNT_HORIZON_v02.json')


def export_base(h):
    """The export keys that do not need a val file: both horizon recounts and the removed-contact counts."""
    z1 = json.loads(HZ1.read_text(encoding='utf-8')); z2 = json.loads(HZ2.read_text(encoding='utf-8'))
    V = {'F.clearance': 'departure', 'F.provenance': 'confirmed', 'F.n_design': int(z2['n_scenes']),
         'F.prereg.status': 'no_room_design' if z1['horizon_rule']['primary_horizon_s'] is None else 'room',
         'F.prereg.horizon': K.STOP_SENTENCE if z1['horizon_rule']['primary_horizon_s'] is None
         else z1['horizon_rule']['primary_horizon_s']}
    for hh in (3, 2):
        for pre, z in (('F.prereg.design', z1), ('F.design', z2)):
            V['%s.R%d' % (pre, hh)] = z['horizons']['%ds' % hh]['all']['R_gl_pp']['point']
            V['%s.R%d.ci' % (pre, hh)] = z['horizons']['%ds' % hh]['all']['R_gl_pp']['ci95']
        for x in ('F0', 'E'):
            V['F.design.removed%d.%s' % (hh, x)] = int(z2['horizons']['%ds' % hh]['removed_contacts_g1'][x]['removed'])
    if h is None:
        V['F.status'] = 'no_room_design'; V['F.horizon'] = K.STOP_SENTENCE
    else:
        V['F.status'] = 'heldout'; V['F.horizon'] = h
    return V


def export_doc(V, lock):
    return dict(package='F', written=time.strftime('%Y-%m-%dT%H:%M:%S'), program='recount/fr_heldout_v02.py',
                program_sha256=L.sha256_file(_pl.Path(__file__).resolve()),
                lock2_sha256=L.sha256_file(lock) if lock else None,
                note='second program (Claude Fable 5.2); F.provenance is as given by the coordinator, not determined here; '
                     'F.RR_CK3 and F.RR_AM are not computed on nuScenes (recorded departure); clearances from cache/clear_v02 '
                     '(departure of 19 Nov 2026), the pre-registered horizon result under F.prereg', values=V)


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def stats_of(BT, BI):
    """Kernel outputs of T1 [n, c0, C, D_E, D_N, ...] and IMM [n, c0, C, D_E, D_N, D_E5] -> (B, 6) hypothesis statistics."""
    r = K.rat(BI[:, 4], BI[:, 3]); c = K.rat(BI[:, 5], BI[:, 3])
    with np.errstate(divide='ignore', invalid='ignore'):
        eff = r / c
    eff = np.where(np.isfinite(eff), eff, np.nan)
    return np.stack([BT[:, 3] / K.NLEV, K.rat(BT[:, 4], BT[:, 3]), BI[:, 3] / K.NLEV, r, c, eff], axis=1)


def share_entry(D, den, nn, Dp, denp, npt, level=0.95):
    """A share RR = D / den with its interval, and D in decision-equivalents with its interval at the same level."""
    e = R.summ_ratio(K.rat(D, den), K.rat(Dp, denp), level)
    e['dec'] = float(L.dec_eq(Dp, npt)); e['dec_ci'] = K.pint(L.dec_eq(D, nn), level)
    return e


def double_bootstrap(n, pkT, pkI, theta, seed_inner, n_outer, n_inner, tag):
    """-> cover (n_outer, nstat, nlevels) bool. Outer: default_rng(20261912).integers(0, n, (n_outer, n)); inner: one stream
    default_rng(seed_inner), integers(0, n, (n_inner, n)) for each outer sample in order, indexing that sample's scene list."""
    ck = OUTD / ('_dboot_%s_seed%d.npz' % (tag, seed_inner))
    outer = np.random.default_rng(K.SEED_OUTER).integers(0, n, (n_outer, n))
    rin = np.random.default_rng(seed_inner)
    cover = np.zeros((n_outer, len(STATS), K.LEVELS.size), bool); done = 0
    if ck.exists():
        with np.load(ck) as z:
            if int(z['n_outer']) == n_outer and int(z['n_inner']) == n_inner and int(z['n']) == n \
                    and np.array_equal(z['theta'], theta, equal_nan=True):
                cover = z['cover'].copy(); done = int(z['done'])
                print('  resuming %s at outer sample %d' % (ck.name, done), flush=True)
    t0 = time.time()
    for b in range(n_outer):
        ii = rin.integers(0, n, (n_inner, n))               # drawn for every outer sample, also when resuming
        if b < done:
            continue
        W = K.counts_of(outer[b][ii], n)
        cover[b] = K.cover_rows(stats_of(K.kernel2(W, *pkT), K.kernel2(W, *pkI)), theta)
        if (b + 1) % 50 == 0 or b + 1 == n_outer:
            np.savez(ck, cover=cover, done=b + 1, n_outer=n_outer, n_inner=n_inner, n=n, theta=theta)
            el = time.time() - t0
            print('  double bootstrap (inner seed %d): %d / %d outer (%.0f s; about %.0f s left)'
                  % (seed_inner, b + 1, n_outer, el, el / (b + 1 - done) * (n_outer - b - 1)), flush=True)
    return cover


def classify_h3(r_ci, c_ci, within5):
    lo_r = r_ci[0]; lo_c, hi_c = c_ci
    if lo_r > 0:
        cl = ('a', 'recovers')
    elif lo_c > K.DELTA:
        cl = ('b', 'uninformative variation')
    elif lo_c > -K.DELTA and hi_c < K.DELTA:
        cl = ('c', 'amplitude-limited')
    else:
        cl = ('d', 'inconclusive')
    return dict(branch=cl[0], label=cl[1], passes=cl[0] in 'abc', barely_varies=bool(within5 >= 0.95))


def main():
    if not SYNTH and (OUTF.exists() or AOUT.exists()):
        raise SystemExit('REFUSED: %s or %s exists' % (OUTF, AOUT))
    if arg('--threads'):
        nb.set_num_threads(int(arg('--threads')))
    t0 = time.time()
    lock = None if SYNTH else K.lock2_path()
    if not SYNTH and lock is None:
        raise SystemExit('REFUSED: LOCK_A10_2.txt does not exist (A10 8.6)')
    h = json.loads(HZ2.read_text(encoding='utf-8'))['horizon_rule']['primary_horizon_s']; hsrc = HZ2.name
    if '--force-stop' in sys.argv and SYNTH:
        h = None
    if h is None:                                           # the v02 rule also stops: export only, no val file is opened
        OUTD.mkdir(parents=True, exist_ok=True)
        exp = export_doc(export_base(None), lock)
        if SYNTH:
            (OUTD / 'A_RECOUNT_F_synth_v02_stop.json').write_text(K.jdump(exp), encoding='utf-8')
        else:
            K.write_once(AOUT, exp)
        print('the v02 horizon rule stops: export written with F.status = no_room_design'); return
    if h not in (2, 3):
        raise SystemExit('bad primary horizon %r' % h)
    hk = R.HKEYS[h]; suf = hk['suf']
    nboot = 2000 if QUICK else K.NBOOT; n_outer = 200 if QUICK else K.N_OUTER; n_inner = 100 if QUICK else K.N_INNER
    base = SHARED + [hk['ev'], hk['clear']]
    nT, sT = K.load_split('T1', 'val', base + ['cF0' + suf, 'cN' + suf, 'cE' + suf, 'cTG' + suf], root=ROOT)
    nI, sI = K.load_split('IMM', 'val', base + ['cF0' + suf, 'cN' + suf, 'cE' + suf], root=ROOT)
    sT = K.swap_clear_v02(nT, sT, 'val', root=ROOT); sI = K.swap_clear_v02(nI, sI, 'val', root=ROOT)
    if nT != nI:
        raise SystemExit('STOP: the T1 and IMM scene lists differ')
    for a, b_ in zip(sT, sI):
        for k in base:
            if not np.array_equal(a[k], b_[k], equal_nan=True):
                raise SystemExit('STOP: tracker-independent key %r differs between T1 and IMM' % k)
    n = len(nT)
    print('%d val scenes, horizon %d s (%s) (%.0f s)' % (n, h, hsrc, time.time() - t0), flush=True)
    doc = dict(code='fr_heldout_v02.py', clearance='departure: cache\\clear_v02', writer='Claude Fable 5.2 (claude-fable-5-2), independent second program',
               amendment='AMENDMENT_10_v13.md 2.2, 2.3, 2.6, 8.5', split='val (held out)', synthetic=SYNTH, quick=QUICK,
               lock2=str(lock) if lock else None, horizon_s=h, horizon_source=hsrc, n_scenes=n, first_scene=nT[0],
               last_scene=nT[-1], delta=K.DELTA, counts=R.counts(sT, h),
               draws=dict(primary='default_rng(20261923).integers(0, n, (%d, n))' % nboot, outer=K.SEED_OUTER,
                          inner=K.SEED_INNER, inner2=K.SEED_INNER2, mc=K.SEED_MC, n_outer=n_outer, n_inner=n_inner))

    # ---- E5_IMM (A10 2.2), built once on the val IMM arrays (all evaluated decisions), fixed in every resample
    ev = np.concatenate([z[hk['ev']] for z in sI]).astype(bool)
    cF0 = np.concatenate([z['cF0' + suf] for z in sI]); cE = np.concatenate([z['cE' + suf] for z in sI])
    cN = np.concatenate([z['cN' + suf] for z in sI])
    cut = np.concatenate([[0], np.cumsum([z[hk['ev']].size for z in sI])])
    rsI = K.ratio_summary(cF0, cN, ev)
    c5, u, e5info = K.e5_scales(cF0, cE, ev, rsI['median'], rsI['A'])
    c5v, _, _ = K.e5_scales(cF0, cE, ev, rsI['median'], rsI['A'], n_all=True)
    doc['margin_ratio_IMM'] = rsI
    doc['E5_IMM'] = dict(m=rsI['median'], A=rsI['A'], f_min=rsI['median'] * (1 - rsI['A']), f_max=rsI['median'] * (1 + rsI['A']),
                         u_mean_evaluated=float(u[ev].mean()), **e5info)
    inp = np.concatenate([z['inpath'] for z in sI]).astype(bool)
    doc['margin_ratio_IMM_inpath_descriptive'] = K.ratio_summary(cF0, cN, ev & inp)
    doc['margin_ratio_IMM_all_built_decisions_variant'] = K.ratio_summary(cF0, cN, np.ones(ev.size, bool))
    doc['margin_ratio_T1_descriptive'] = K.ratio_summary(np.concatenate([z['cF0' + suf] for z in sT]),
                                                         np.concatenate([z['cN' + suf] for z in sT]), ev)
    print('margin ratio IMM:', rsI, flush=True)

    # ---- T1's descriptive sources: E5, E5p (A10 2.2) and the partial oracles, built once on the val T1 arrays
    tF0 = np.concatenate([z['cF0' + suf] for z in sT]); tE = np.concatenate([z['cE' + suf] for z in sT])
    t5, tu, t5info = K.e5_scales(tF0, tE, ev, K.E5_M, K.E5_A)
    t5p = K.scales_from_u(tF0, K.permute_u(tu, ev, cut), K.E5_M, K.E5_A)
    tpo = K.po_scales(tF0, tE)
    doc['E5_T1'] = dict(m=K.E5_M, A=K.E5_A, permutation_seed=K.SEED_E5P, partial_oracle_seed=K.SEED_PO,
                        n_built_decisions=int(tF0.shape[0]), **t5info)

    def sl(a):
        return lambda k, z: a[cut[k]:cut[k + 1]]
    fT = [('F0', lambda k, z: z['cF0' + suf]), ('E', lambda k, z: z['cE' + suf]), ('N', lambda k, z: z['cN' + suf]),
          ('TG', lambda k, z: z['cTG' + suf]), ('E5', sl(t5)), ('E5p', sl(t5p)), ('PO25', sl(tpo[0])), ('PO50', sl(tpo[1])),
          ('PO75', sl(tpo[2]))]
    fI = [('F0', lambda k, z: z['cF0' + suf]), ('E', lambda k, z: z['cE' + suf]), ('N', lambda k, z: z['cN' + suf]),
          ('E5', lambda k, z: c5[cut[k]:cut[k + 1]])]
    W = K.counts_of(np.random.default_rng(K.SEED_PRIMARY).integers(0, n, (nboot, n)), n)
    one = np.ones((1, n))
    keep = {}
    for pop in R.POPS:
        pkT, iT = R.build_pack(sT, h, pop, fT); pkI, iI = R.build_pack(sI, h, pop, fI)
        pT = K.kernel2(one, *pkT); pI = K.kernel2(one, *pkI)
        BT = R.run(W, pkT, label='T1 ' + pop); BI = R.run(W, pkI, label='IMM ' + pop)
        th = stats_of(pT, pI)[0]; SB = stats_of(BT, BI)
        ent = dict(T1=dict(n_decisions=float(pT[0, 0]), c0_pp=float(pT[0, 1]), C_pp=float(pT[0, 2]), sources=iT,
                           D_gl=dict(E=float(pT[0, 3]), N=float(pT[0, 4]),
                                     **{x: float(pT[0, 5 + j]) for j, x in enumerate(DESC)}),
                           R_gl_pp=R.summ_room(BT[:, 3], pT[0, 3]),
                           room_decision_equivalents=float(L.dec_eq(pT[0, 3], pT[0, 0])),
                           RR_gl_N=R.summ_ratio(SB[:, 1], th[1]),
                           D_N_decision_equivalents=dict(point=float(L.dec_eq(pT[0, 4], pT[0, 0])),
                                                         ci95=K.pint(L.dec_eq(BT[:, 4], BT[:, 0]), 0.95)),
                           descriptive_95=dict(
                               {x: share_entry(BT[:, 5 + j], BT[:, 3], BT[:, 0], pT[0, 5 + j], pT[0, 3], pT[0, 0])
                                for j, x in enumerate(DESC)},
                               E5mP=share_entry(BT[:, 6] - BT[:, 7], BT[:, 3], BT[:, 0], pT[0, 6] - pT[0, 7], pT[0, 3],
                                                pT[0, 0]),
                               N=share_entry(BT[:, 4], BT[:, 3], BT[:, 0], pT[0, 4], pT[0, 3], pT[0, 0]),
                               R_dec=dict(point=float(L.dec_eq(pT[0, 3], pT[0, 0])),
                                          ci=K.pint(L.dec_eq(BT[:, 3], BT[:, 0]), 0.95)))),
                   IMM=dict(n_decisions=float(pI[0, 0]), c0_pp=float(pI[0, 1]), C_pp=float(pI[0, 2]), sources=iI,
                            D_gl=dict(E=float(pI[0, 3]), N=float(pI[0, 4]), E5=float(pI[0, 5])),
                            R_gl_pp=R.summ_room(BI[:, 3], pI[0, 3]),
                            room_decision_equivalents=float(L.dec_eq(pI[0, 3], pI[0, 0])),
                            r_RR_gl_N_IMM=R.summ_ratio(SB[:, 3], th[3]), c_RR_gl_E5_IMM=R.summ_ratio(SB[:, 4], th[4]),
                            efficiency_r_over_c=R.summ_ratio(SB[:, 5], th[5])))
        if pop == 'all':
            pkV, _ = R.build_pack(sI, h, pop, fI[:3] + [('E5', lambda k, z: c5v[cut[k]:cut[k + 1]])])
            pv = K.kernel2(one, *pkV)[0]
            ent['IMM']['c_variant_rank_divisor_all_evaluated_point'] = float(K.rat(pv[5], pv[3]))
            keep = dict(pkT=(pkT[0][:3],) + tuple(x[:pkT[4][3]] for x in pkT[1:4]) + (pkT[4][:4],), pkI=pkI, th=th, SB=SB,
                        BT=BT, BI=BI, pT=pT[0], pI=pI[0])
        doc[pop] = ent
        print('%s: %s' % (pop, K.jdump({k: (v['point'], v.get('ci', v.get('ci95'))) for d_ in (ent['T1'], ent['IMM'], ent['T1']['descriptive_95'])
                                        for k, v in d_.items() if isinstance(v, dict) and 'point' in v})), flush=True)

    # ---- calibration (A10 2.6), primary population
    th = keep['th']; SB = keep['SB']
    cov1 = double_bootstrap(n, keep['pkT'], keep['pkI'], th, K.SEED_INNER, n_outer, n_inner, 'h%d' % h)
    need2 = bool((cov1.mean(axis=0)[:, 0] < 0.94).any())
    cov2 = double_bootstrap(n, keep['pkT'], keep['pkI'], th, K.SEED_INNER2, n_outer, n_inner, 'h%d' % h) if need2 else None
    cal = {}
    for j, nm in enumerate(STATS):
        d = K.calibrate_decide(cov1[:, j, :], None if cov2 is None else cov2[:, j, :])
        d['point'] = float(th[j]); d['interval'] = K.pint(SB[:, j], d['level'])
        d['interval_nominal95'] = K.pint(SB[:, j], 0.95)
        d['coverage_by_level_first_seed'] = dict(levels=[float(x) for x in K.LEVELS[::10]],
                                                 coverage=[float(x) for x in cov1[:, j, :].mean(axis=0)[::10]])
        cal[nm] = d
    # decision-equivalents of the hypothesis statistics, at the level of the share's calibrated interval
    BT = keep['BT']; BI = keep['BI']; pT = keep['pT']; pI = keep['pI']
    for nm, Bx, px, col in (('R_gl_T1', BT, pT, 3), ('RR_gl_N', BT, pT, 4), ('R_gl_IMM', BI, pI, 3),
                            ('r_RR_gl_N_IMM', BI, pI, 4), ('c_RR_gl_E5_IMM', BI, pI, 5)):
        cal[nm]['dec'] = float(L.dec_eq(px[col], px[0]))
        cal[nm]['dec_interval'] = K.pint(L.dec_eq(Bx[:, col], Bx[:, 0]), cal[nm]['level'])
    doc['calibrated'] = cal
    doc['second_inner_seed_run'] = need2

    # ---- verdicts, in the fixed sequence (A10 8.5)
    a = doc['all']
    share = a['T1']['R_gl_pp']['share_le0']
    h0 = bool(cal['R_gl_T1']['interval'][0] > 0 and share < 0.025)
    ci = cal['RR_gl_N']['interval']
    h1 = bool(ci[0] > -K.DELTA and ci[1] < K.DELTA)
    h2 = classify_h3(cal['r_RR_gl_N_IMM']['interval'], cal['c_RR_gl_E5_IMM']['interval'], rsI['within5_share'])
    doc['verdicts'] = {
        'F-H0': dict(passes=h0, R_gl_lower_end=cal['R_gl_T1']['interval'][0], share_resamples_nonpositive=share,
                     confirmed=h0),
        'F-H1': dict(passes=h1, interval=ci, inside_pm_delta=h1, confirmed=bool(h0 and h1),
                     status='confirmatory' if h0 else 'not confirmatory (F-H0 did not pass)'),
        'F-H2': dict(r_interval=cal['r_RR_gl_N_IMM']['interval'], c_interval=cal['c_RR_gl_E5_IMM']['interval'],
                     R_gl_IMM_interval=cal['R_gl_IMM']['interval'],
                     R_gl_IMM_share_resamples_nonpositive=a['IMM']['R_gl_pp']['share_le0'],
                     efficiency=(cal['efficiency_r_over_c'] if h2['branch'] == 'a' else None),
                     confirmed=bool(h0 and h1 and h2['passes']),
                     status='confirmatory' if (h0 and h1) else 'not confirmatory (an earlier hypothesis did not pass)', **h2)}
    # ---- the export for package A (RESULTS_INTERFACE_v13.md section 1)
    V = export_base(h)
    V['F.n_heldout'] = int(n); V['F.n_dec'] = int(round(a['T1']['n_decisions']))
    for key, nm in (('F.R', 'R_gl_T1'), ('F.RR_N', 'RR_gl_N'), ('F.IMM.r', 'r_RR_gl_N_IMM'), ('F.IMM.c', 'c_RR_gl_E5_IMM'),
                    ('F.IMM.eff', 'efficiency_r_over_c')):
        c_ = cal[nm]
        V[key] = c_['point']; V[key + '.ci'] = c_['interval']; V[key + '.level'] = c_['level']; V[key + '.cal'] = c_['cal']
        if 'dec' in c_:
            V[key + '.dec'] = c_['dec']; V[key + '.dec.ci'] = c_['dec_interval']
    V['F.R.nonpos_share'] = share; V['F.IMM.within5'] = rsI['within5_share']
    dd = a['T1']['descriptive_95']
    for key, nm in (('F.RR_TG', 'TG'), ('F.RR_E5', 'E5'), ('F.RR_E5mP', 'E5mP'), ('F.PO25', 'PO25'), ('F.PO50', 'PO50'),
                    ('F.PO75', 'PO75')):
        V[key] = dd[nm]['point']; V[key + '.ci'] = dd[nm]['ci']; V[key + '.dec'] = dd[nm]['dec']
        V[key + '.dec.ci'] = dd[nm]['dec_ci']
    ip = doc['inpath']['T1']
    V['F.inpath.R'] = ip['R_gl_pp']['point']; V['F.inpath.R.ci'] = ip['R_gl_pp']['ci95']
    V['F.inpath.RR_N'] = ip['descriptive_95']['N']['point']; V['F.inpath.RR_N.ci'] = ip['descriptive_95']['N']['ci']
    V['F.inpath.RR_N.dec'] = ip['descriptive_95']['N']['dec']; V['F.inpath.RR_N.dec.ci'] = ip['descriptive_95']['N']['dec_ci']
    exp = export_doc(V, lock)
    doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t0
    OUTD.mkdir(parents=True, exist_ok=True)
    if SYNTH:
        AOUT.write_text(K.jdump(exp), encoding='utf-8')
    else:
        K.write_once(AOUT, exp)
    if SYNTH:
        OUTF.write_text(K.jdump(doc), encoding='utf-8')
    else:
        K.write_once(OUTF, doc)
    print(K.jdump(doc['verdicts'])); print('written', OUTF, '(%.0f s)' % (time.time() - t0))


if __name__ == '__main__':
    main()
