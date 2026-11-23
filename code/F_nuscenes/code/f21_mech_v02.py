"""Revision v13, AMENDMENT_12 sec. 5: the real-sensor mechanism check on nuScenes. Does the covariance's variation follow the realised
v02 (22 Nov 2026, about 03:40 EST, before LOCK_A12c and before any val value): a copy of v01 with the TRAIN-INFORMED primary
declared by the coordinator at 03:27 and agreed by the author ("Yes, keep it"). PRIMARY (the only Holm entry, M.tau / M.ci /
M.level / M.passes / M.p): CANMOT's within-(scene, keyframe) tau_b over the pairs of primary-population rows (age >= 1.0 s) with
at least one member in-miss or post-miss, i.e. every within-cell pair except steady-steady pairs. The v01 all-row statistic is
descriptive (M.all.tau, M.all.tau.ci95, M.all.p). Rows, strata, pooled tau and the permuted twin (all-row population) as v01.
prediction error? New file, 22 Nov 2026 (Claude Opus 5.5, session F).

Rows (one per decision instance): a track of a primary class (car, truck, bus, trailer: CANMOT classes 2, 6, 1, 5) output at keyframe t,
matched one-to-one to a truth annotation of the same class at t (Hungarian assignment on the BEV centre distance, gate 2.0 m, the
nuScenes tracking metric's centre-distance threshold), whose instance is annotated again at the keyframe u nearest t + 3 s
(|kf_t[u] - kf_t[t] - 3| <= 0.25 s).
  dt   = kf_t[u] - trk_state_time
  e_h  = || centre_xy + vel_xy * dt - truth_xy(u) ||                                         (the realised 3 s CV-prediction error)
  s_h  = sqrt(trace(P_pp + dt (P_pv + P_vp) + dt^2 P_vv)), P = trk_P[[0,1,6,7]][:, [0,1,6,7]] (x, y, vx, vy; consumer.covariance4)
         (the covariance's 3 s propagated position spread; the planner's acceleration-noise term, sigma_acc = 1 for every vehicle,
         adds the same constant to every row's trace and so cannot change any within-cell rank)
  age  = kf_t[t] - kf_t[first keyframe of the track id in the scene]
  miss(k) for the matched instance at keyframe k: the instance is annotated at k and no detection of its class with score >= the
         tracker's own score threshold (contracts\\tracker_config.json preprocessing.SF_thre: car 0.16, truck 0, bus 0, trailer 0.1)
         lies within 2.0 m of its centre (a real missed detection: the tracker received no usable detection of the object)
  stratum: young if age < 1.0 s; else in-miss if miss(t); else post-miss if miss(t-1) or miss(t-2); else steady.
Primary population: rows with age >= 1.0 s. Statistic: Kendall tau_b WITHIN (scene, keyframe) cells, pooled:
  tau = sum_c (C_c - D_c) / sum_c sqrt((n0_c - n1_c)(n0_c - n2_c))   (n0 pairs, n1 / n2 tied pairs in s_h / e_h, per cell c)
Per scene A_s = sum over its cells of (C - D), B_s = sum of the denominators: a scene resample's tau = sum w A / sum w B (exact).
Strata (descriptive): tau over within-cell pairs with at least one member in the stratum (in-miss, post-miss, young: young rows
included for this only), and over pairs of two steady rows; mean s_h and e_h per stratum. Pooled tau_b across all rows (not within
cells) and a drawn within-cell permuted twin (K = 20, default_rng(20261952): for k = 1..20, scenes ascending, cells by ascending
keyframe, one rng.permutation of the cell's primary rows' s_h, rows in ascending track id) beside it.
Intervals: 20,000 scene resamples (default_rng(20261951).integers(0, n, (20000, n)), scenes ascending); one-sided lower end at the
A10 sec. 2.6 level (double bootstrap 2,000 x 1,000, seeds 20261912 / 20261913, checks 20261914 / 20261920). Holm p-value (A12 sec. 4):
p = (1 + #{tau* <= 0}) / (20,000 + 1).
Modes: design SPLIT TRACKER (train only: the design numbers and the power for val) | score TRACKER (val; refuses without
revision_v13\\LOCK_A12c.txt). Writes out\\mech\\MECH_<split>_<tracker>_v01.json and the rows npz. Refuses to overwrite.
Usage: python -I f21_mech_v01.py design train T1|IMM [--scenes N] | score T1|IMM [--no-calib]
"""
import json, math, pathlib, sys, time
import numpy as np
from scipy.optimize import linear_sum_assignment

HERE = pathlib.Path(__file__).resolve().parent
F = HERE.parent
V13 = F.parent.parent
CACHE = F / 'cache'
OUT = F / 'out' / 'mech'
LOCK = V13 / 'LOCK_A12c.txt'
GATE = 2.0
H = 3.0
H_TOL = 0.25
MIN_AGE = 1.0
CLASSES = {'car': 'car', 'truck': 'truck', 'bus': 'bus', 'trailer': 'trailer'}
ANN_MAP = {'vehicle.car': 'car', 'vehicle.truck': 'truck', 'vehicle.bus.rigid': 'bus', 'vehicle.bus.bendy': 'bus',
           'vehicle.trailer': 'trailer'}
SF = {'car': 0.16, 'truck': 0.0, 'bus': 0.0, 'trailer': 0.1}
IDX = [0, 1, 6, 7]
SEED_BOOT, SEED_PERM, K_PERM, NBOOT = 20261951, 20261952, 20, 20000


def scene_rows(scene, split, tracker):
    c = np.load(CACHE / split / (scene + '.npz'), allow_pickle=False)
    t = np.load(CACHE / ('tracks_' + tracker) / split / (scene + '.npz'), allow_pickle=False)
    kf_t = c['kf_t']; nkf = kf_t.size
    acls = np.array([ANN_MAP.get(str(x), '') for x in c['ann_cat']])
    tn = np.array([str(x) for x in t['trk_name']])
    first = {}
    for kf, tid in zip(t['trk_kf'], t['trk_id']):
        first.setdefault(int(tid), int(kf))
    first_kf = {k: min(int(kf) for kf, i in zip(t['trk_kf'], t['trk_id']) if int(i) == k) for k in first}
    dk = c['det_kf']; dn = np.array([str(x) for x in c['det_name']]); ds = c['det_score']; dx = c['det_xyz'][:, :2]

    def miss(inst, k):
        if k < 0: return False
        a = np.flatnonzero((c['ann_kf'] == k) & (c['ann_inst'] == inst))
        if a.size == 0: return False
        cl = acls[a[0]]; p = c['ann_xyz'][a[0], :2]
        m = (dk == k) & (dn == cl) & (ds >= SF[cl])
        return not bool(m.any() and (np.hypot(*(dx[m] - p).T) <= GATE).any())

    rows = []
    for k in range(nkf):
        u = int(np.argmin(np.abs(kf_t - kf_t[k] - H)))
        if abs(kf_t[u] - kf_t[k] - H) > H_TOL or u <= k:
            continue
        ti = np.flatnonzero((t['trk_kf'] == k) & np.isin(tn, list(CLASSES)))
        ai = np.flatnonzero((c['ann_kf'] == k) & (acls != ''))
        if ti.size == 0 or ai.size == 0:
            continue
        D = np.hypot(t['trk_center'][ti, 0][:, None] - c['ann_xyz'][ai, 0][None, :], t['trk_center'][ti, 1][:, None] - c['ann_xyz'][ai, 1][None, :])
        same = tn[ti][:, None] == acls[ai][None, :]
        cost = np.where(same & (D <= GATE), D, 1e6)
        r, q = linear_sum_assignment(cost)
        for a_, b_ in zip(r, q):
            if cost[a_, b_] >= 1e6: continue
            j = ti[a_]; i = ai[b_]; inst = int(c['ann_inst'][i])
            au = np.flatnonzero((c['ann_kf'] == u) & (c['ann_inst'] == inst))
            if au.size == 0: continue
            dt = float(kf_t[u] - t['trk_state_time'][j])
            pred = t['trk_center'][j, :2] + t['trk_vel'][j] * dt
            e = float(np.hypot(*(pred - c['ann_xyz'][au[0], :2])))
            P = t['trk_P'][j][np.ix_(IDX, IDX)]
            S = P[:2, :2] + dt * (P[:2, 2:] + P[2:, :2]) + dt * dt * P[2:, 2:]
            s = float(math.sqrt(max(np.trace(S), 0.)))
            age = float(kf_t[k] - kf_t[first_kf[int(t['trk_id'][j])]])
            m0, m1, m2 = miss(inst, k), miss(inst, k - 1), miss(inst, k - 2)
            st = 'young' if age < MIN_AGE else ('in_miss' if m0 else ('post_miss' if (m1 or m2) else 'steady'))
            rows.append((k, int(t['trk_id'][j]), inst, tn[j], s, e, age, dt, st))
    rows.sort(key=lambda r: (r[0], r[1]))          # within each cell, rows in ascending track id (the twin's permutation order)
    return rows


def cell_terms(s, e, sel_pair=None):
    """Kendall tau_b terms of one cell: (C - D, sqrt((n0 - n1)(n0 - n2))). sel_pair(i, j) restricts the pairs counted."""
    n = s.size
    if n < 2: return 0., 0.
    i, j = np.triu_indices(n, 1)
    if sel_pair is not None:
        keep = sel_pair(i, j); i, j = i[keep], j[keep]
    if i.size == 0: return 0., 0.
    ds_ = np.sign(s[i] - s[j]); de = np.sign(e[i] - e[j])
    n0 = i.size; n1 = int((ds_ == 0).sum()); n2 = int((de == 0).sum())
    return float((ds_ * de).sum()), math.sqrt(max(n0 - n1, 0) * max(n0 - n2, 0))


def scene_terms(rows, which='primary', perm_rng=None):
    if not rows: return 0., 0.
    a = np.array([r[0] for r in rows]); s = np.array([r[4] for r in rows]); e = np.array([r[5] for r in rows])
    st = np.array([r[8] for r in rows])
    A = B = 0.
    for k in np.unique(a):
        m = a == k
        if which == 'primary':
            mm = m & (st != 'young'); ss = s[mm]
            if perm_rng is not None: ss = ss[perm_rng.permutation(ss.size)]
            x, y = cell_terms(ss, e[mm])
        elif which == 'miss':                       # v02 primary: pairs with >= 1 member in-miss or post-miss (age >= 1.0 s rows)
            mm = m & (st != 'young'); sts = st[mm]; ms_ = (sts == 'in_miss') | (sts == 'post_miss')
            x, y = cell_terms(s[mm], e[mm], lambda i, j: ms_[i] | ms_[j])
        elif which == 'steady':
            mm = m & (st == 'steady'); x, y = cell_terms(s[mm], e[mm])
        else:                                     # pairs with >= 1 member in stratum `which` (young included only here)
            mm = m & ((st != 'young') | (st == which)) if which == 'young' else m & (st != 'young')
            if which == 'young': mm = m
            sts = st[mm]
            x, y = cell_terms(s[mm], e[mm], lambda i, j: (sts[i] == which) | (sts[j] == which))
        A += x; B += y
    return A, B


def boot(A, B, nboot=NBOOT, seed=SEED_BOOT):
    n = A.size
    idx = np.random.default_rng(seed).integers(0, n, (nboot, n))
    W = np.zeros((nboot, n))
    np.add.at(W, (np.repeat(np.arange(nboot), n), idx.ravel()), 1.)
    with np.errstate(invalid='ignore', divide='ignore'):
        return (W @ A) / (W @ B)


def double_boot(A, B, full):
    """A10 sec. 2.6 for the primary tau (cd_common_v13 conventions: rank p-values, coverage over finite outer samples)."""
    n = A.size
    res = {}
    for seed_in in (20261913, 20261914):
        IDX_O = np.random.default_rng(20261912).integers(0, n, (2000, n)); rng_i = np.random.default_rng(seed_in)
        lt = np.full(2000, np.nan); le = np.full(2000, np.nan)
        for b in range(2000):
            io = IDX_O[b]; ii = io[rng_i.integers(0, n, (1000, n))]
            W = np.zeros((1000, n)); np.add.at(W, (np.repeat(np.arange(1000), n), ii.ravel()), 1.)
            with np.errstate(invalid='ignore', divide='ignore'):
                v = (W @ A) / (W @ B)
            v = v[np.isfinite(v)]
            if v.size: lt[b] = (v < full).mean(); le[b] = (v <= full).mean()
        res[seed_in] = (lt, le)
    levels = np.round(np.arange(0.95, 0.99951, 0.0005), 4)

    def cover(lt, le, nom):
        a = 1. - nom; ok = np.isfinite(lt)
        return ((le[ok] >= a / 2. - 1e-12) & (lt[ok] <= 1. - a / 2. + 1e-12))
    lt1, le1 = res[20261913]
    c95 = float(cover(lt1, le1, 0.95).mean())
    if c95 >= 0.94:
        return dict(level=0.95, coverage_nominal95=c95, rule='nominal 95% (coverage >= 0.94)')
    cov = np.array([cover(lt1, le1, l).mean() for l in levels])
    ok = np.flatnonzero(cov >= 0.95)
    cand = float(levels[ok[0]]) if ok.size else None
    if cand is None:
        return dict(level=0.99, coverage_nominal95=c95, rule='nominal 99% (no level reaches 0.95)')
    # Monte Carlo SD of the chosen level, as cd_common_v13.calibrated_levels (the A10 sec. 2.6 practice of record): ONE index draw
    # default_rng(20261920).integers(0, 2000, (2000, 2000)); in each resample, the outer samples with a finite p-value among the drawn
    # ones; the smallest level whose coverage is >= 0.95, or 1.0 when none is; SD with ddof = 1. Second seed: the same choice (1.0 if none).
    mc = np.random.default_rng(20261920).integers(0, 2000, (2000, 2000))
    aa = 1. - levels
    valid = np.isfinite(lt1)
    IND = np.zeros((2000, levels.size), bool)
    IND[valid] = (le1[valid][:, None] >= aa / 2. - 1e-12) & (lt1[valid][:, None] <= 1. - aa / 2. + 1e-12)
    lv = np.empty(2000)
    for q, r in enumerate(mc):
        rows = r[valid[r]]
        cv = IND[rows].mean(axis=0) if rows.size else np.full(levels.size, np.nan)
        hit = np.flatnonzero(cv >= 0.95)
        lv[q] = levels[hit[0]] if hit.size else 1.0
    sd = float(np.std(lv, ddof=1))
    lt2, le2 = res[20261914]
    cov2 = np.array([cover(lt2, le2, l).mean() for l in levels]); ok2 = np.flatnonzero(cov2 >= 0.95)
    cand2 = float(levels[ok2[0]]) if ok2.size else 1.0
    if sd <= 0.002 and abs(cand2 - cand) <= 0.002:
        return dict(level=cand, coverage_nominal95=c95, mc_sd=sd, second=cand2, rule='calibrated')
    return dict(level=0.99, coverage_nominal95=c95, mc_sd=sd, second=cand2, rule='nominal 99% (calibrated level failed a check)')


def run(split, tracker, calib, first=None):
    OUT.mkdir(parents=True, exist_ok=True)
    outf = OUT / ('MECH_%s_%s_v02%s.json' % (split, tracker, '_first%d' % first if first else ''))
    if outf.exists(): raise SystemExit('REFUSED: %s exists' % outf)
    scenes = sorted(p.stem for p in (CACHE / ('tracks_' + tracker) / split).glob('scene-*.npz'))
    if first:                                   # the second program's agreement check on the first N train scenes (design split only)
        if split != 'train': raise SystemExit('REFUSED: --scenes is for the design split only')
        scenes = scenes[:first]
    t0 = time.time(); allrows = {}
    for n_, sc in enumerate(scenes):
        allrows[sc] = scene_rows(sc, split, tracker)
        if (n_ + 1) % 100 == 0: print('%d/%d scenes (%.0f s)' % (n_ + 1, len(scenes), time.time() - t0), flush=True)
    AB = {w: np.array([scene_terms(allrows[sc], w) for sc in scenes]) for w in ('miss', 'primary', 'steady', 'in_miss', 'post_miss', 'young')}
    A, B = AB['miss'][:, 0], AB['miss'][:, 1]           # v02: the primary is the miss-pair statistic
    tau = float(A.sum() / B.sum())
    bt = boot(A, B)
    doc = dict(code='f21_mech_v02.py', amendment='AMENDMENT_12 sec. 5', split=split, tracker=tracker, n_scenes=len(scenes),
               rules=dict(gate_m=GATE, horizon_s=H, horizon_tol_s=H_TOL, min_age_s=MIN_AGE, classes=sorted(CLASSES), sf_thre=SF,
                          seeds=dict(boot=SEED_BOOT, perm=SEED_PERM, calib=[20261912, 20261913, 20261914, 20261920])))
    st_all = [r[8] for sc in scenes for r in allrows[sc]]
    doc['n_rows'] = {s: st_all.count(s) for s in ('steady', 'in_miss', 'post_miss', 'young')}
    doc['n_rows_primary'] = sum(v for k, v in doc['n_rows'].items() if k != 'young')
    doc['n_cells_primary_with_pairs'] = int(sum(1 for sc in scenes for k in set(r[0] for r in allrows[sc])
                                              if sum(1 for r in allrows[sc] if r[0] == k and r[8] != 'young') >= 2))
    doc['tau'] = tau
    doc['tau_ci95'] = [float(x) for x in np.nanpercentile(bt, [2.5, 97.5])]
    doc['tau_boot_sd'] = float(np.nanstd(bt, ddof=1))
    doc['p_one_sided'] = float((1 + np.sum(bt <= 0)) / (bt.size + 1))
    doc['primary'] = 'within-cell tau_b over pairs with >= 1 member in-miss or post-miss (age >= 1.0 s rows); v02, train-informed'
    A0, B0 = AB['primary'][:, 0], AB['primary'][:, 1]     # v01's all-row statistic, descriptive in v02
    bt0 = boot(A0, B0)
    doc['all_rows'] = dict(tau=float(A0.sum() / B0.sum()), ci95=[float(x) for x in np.nanpercentile(bt0, [2.5, 97.5])],
                           boot_sd=float(np.nanstd(bt0, ddof=1)), p_one_sided=float((1 + np.sum(bt0 <= 0)) / (bt0.size + 1)))
    if calib:
        cal = double_boot(A, B, tau)
        a = 100. * (1. - cal['level']) / 2.
        cal['ci'] = [float(x) for x in np.nanpercentile(bt, [a, 100. - a])]
        doc['calibration'] = cal
        doc['passes'] = bool(cal['ci'][0] > 0)
    doc['strata'] = {}
    for w in ('steady', 'in_miss', 'post_miss', 'young'):
        a_, b_ = AB[w][:, 0], AB[w][:, 1]
        if b_.sum() > 0:
            bw = boot(a_, b_)
            doc['strata'][w] = dict(tau=float(a_.sum() / b_.sum()), ci95=[float(x) for x in np.nanpercentile(bw, [2.5, 97.5])],
                                    pairs_note='pairs with >= 1 member in the stratum' if w != 'steady' else 'pairs of two steady rows')
        rr = [r for sc in scenes for r in allrows[sc] if r[8] == w]
        doc['strata'].setdefault(w, {})['mean_s'] = float(np.mean([r[4] for r in rr])) if rr else None
        doc['strata'][w]['mean_e'] = float(np.mean([r[5] for r in rr])) if rr else None
        doc['strata'][w]['n_rows'] = len(rr)
    # descriptive: pooled tau_b across all primary rows (not within cells); drawn within-cell permuted twin
    from scipy.stats import kendalltau
    sp = np.array([r[4] for sc in scenes for r in allrows[sc] if r[8] != 'young'])
    ep = np.array([r[5] for sc in scenes for r in allrows[sc] if r[8] != 'young'])
    doc['tau_pooled_across_cells'] = float(kendalltau(sp, ep).statistic) if sp.size > 1 else None
    rng = np.random.default_rng(SEED_PERM)
    tw = []
    for _ in range(K_PERM):
        AP = np.array([scene_terms(allrows[sc], 'primary', perm_rng=rng) for sc in scenes])
        tw.append(float(AP[:, 0].sum() / AP[:, 1].sum()))
    doc['permuted_twin'] = dict(K=K_PERM, mean=float(np.mean(tw)), values=tw)
    if split == 'train':
        se_val = doc['tau_boot_sd'] * math.sqrt(len(scenes) / 150.)
        from math import erf
        z = tau / se_val - 1.959964
        doc['power_for_val_150'] = dict(assumed_tau=tau, se_val=se_val, power_one_sided_95=float(0.5 * (1 + erf(z / math.sqrt(2)))))
    # the keys the second program writes (A10 sec. 10.1(c) comparison)
    v = {'M.n_scenes': len(scenes), 'M.tau': tau, 'M.tau.ci95': doc['tau_ci95'], 'M.p': doc['p_one_sided'],
         'M.tau_pooled': doc['tau_pooled_across_cells'], 'M.twin_mean': doc['permuted_twin']['mean'],
         'M.all.tau': doc['all_rows']['tau'], 'M.all.tau.ci95': doc['all_rows']['ci95'], 'M.all.p': doc['all_rows']['p_one_sided']}
    for s_ in ('steady', 'in_miss', 'post_miss', 'young'):
        v['M.n_rows.' + s_] = doc['n_rows'][s_]
        d_ = doc['strata'][s_]
        v['M.s.%s.tau' % s_] = d_.get('tau'); v['M.s.%s.ci95' % s_] = d_.get('ci95')
        v['M.s.%s.mean_s' % s_] = d_.get('mean_s'); v['M.s.%s.mean_e' % s_] = d_.get('mean_e')
    if 'calibration' in doc:
        v.update({'M.level': doc['calibration']['level'], 'M.ci': doc['calibration']['ci'], 'M.passes': doc['passes']})
    doc['values'] = v
    doc['seconds'] = time.time() - t0; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    outf.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    np.savez_compressed(OUT / ('MECH_ROWS_%s_%s_v02%s.npz' % (split, tracker, '_first%d' % first if first else '')),
                        scene=np.array([sc for sc in scenes for r in allrows[sc]]),
                        **{nm: np.array([r[ix] for sc in scenes for r in allrows[sc]]) for ix, nm in
                           enumerate(['kf', 'track_id', 'inst', 'cls', 's_h', 'e_h', 'age', 'dt', 'stratum'])})
    print(json.dumps({k: doc[k] for k in ('split', 'tracker', 'n_rows', 'tau', 'tau_ci95', 'p_one_sided', 'all_rows') if k in doc}), flush=True)
    print('strata', json.dumps({k: (v.get('tau'), v.get('n_rows')) for k, v in doc['strata'].items()}), flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'design':
        if a[1] != 'train': raise SystemExit('REFUSED: design uses the train split only')
        run('train', a[2], calib='--no-calib' not in a, first=int(a[a.index('--scenes') + 1]) if '--scenes' in a else None)
    elif a[0] == 'score':
        if not LOCK.is_file(): raise SystemExit('REFUSED: no LOCK_A12c.txt; no val value of the mechanism check before the lock')
        run('val', a[1], calib='--no-calib' not in a)
