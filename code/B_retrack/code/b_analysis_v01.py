"""v13 package B: analyses B1-B5 and B8(b) on the 35 old evaluation lead-braking runs, one tracker variant per call (exploratory).
New file, 19 Nov 2026 (Claude Opus 5.5). Definitions: B_retrack\\B_ANALYSIS_DEFINITIONS_v01.md; library choices: shared\\trackers\\
IMM_AND_VARIANTS_SPEC_v01.md sections 7-8. Writes out\\banalysis\\B_<variant>_v01.json.

Usage: python -I -B -X utf8 b_analysis_v01.py <variant> [nboot] [populations to bootstrap, comma list; default all,tru_stopped,est_stopped]
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, pathlib, time
LIB = pathlib.Path(r'ARS_TRIAL\revision_v13\work\shared\trackers')
sys.path.insert(0, str(LIB))
import trk_env_v01 as env
env.setup()
import numpy as np
import trk_score_v01 as S
C = S.A9.C; L = S.L

HERE = pathlib.Path(__file__).resolve().parents[1]
RT = HERE / 'out' / 'retrack'
OUTD = HERE / 'out' / 'banalysis'
DELTA = 0.05
POPN = ['all', 'moving', 'est_before', 'est_braking', 'est_stopped', 'tru_before', 'tru_braking', 'tru_stopped',
        'est05_braking', 'est20_braking']
SRC = ['N', 'NA', 'AM', 'CK3', 'Q']


def load(variant):
    rec = C.load_runs()                     # record: cache, truth phase, record arrays
    runs = []
    for r in rec:
        z = np.load(RT / variant / (r['run'] + '_arrays.npz'), allow_pickle=False)
        for key, rk in (('k', 'k'), ('idx55', 'idx55')):
            if not np.array_equal(z[key], r[rk]):
                raise SystemExit('REFUSED: %s %s differs from the record' % (r['run'], key))
        ev = z['evaluated'].astype(bool)
        if not np.array_equal(ev, r['ev'].astype(bool)) or not np.array_equal(L.clean_clear(z['clear']), r['clear1']):
            raise SystemExit('REFUSED: %s evaluated / clearance differ from the record' % r['run'])
        ph_t = r['ph']
        ph_e = S.est_phase(z['vhat'], z['ahat_long'], z['lead_found'], -1.0)
        ph_e05 = S.est_phase(z['vhat'], z['ahat_long'], z['lead_found'], -0.5)
        ph_e20 = S.est_phase(z['vhat'], z['ahat_long'], z['lead_found'], -2.0)
        v0 = z['v0']
        masks = (ev, ev & (v0 > 0.5), ev & (ph_e == 0), ev & (ph_e == 1), ev & (ph_e == 2),
                 ev & (ph_t == 0), ev & (ph_t == 1), ev & (ph_t == 2), ev & (ph_e05 == 1), ev & (ph_e20 == 1))
        now = z['now']; i2 = np.flatnonzero(ph_t == 2)
        t_stop = now - now[i2[0]] if i2.size else np.full(now.size, np.nan)
        runs.append(dict(run=r['run'], desired=r['desired'], idx55=r['idx55'].astype(np.int64), clear1=r['clear1'], vbar=r['vbar'], ev=ev,
                         masks=masks, sel={}, late={}, cache=r['cache'],
                         crit={'F0': z['cF0'], 'E': z['cE'], 'N': z['cN'], 'NA': z['cNA'], 'AM': z['cA1'], 'CK3': z['cCK3'], 'Q': z['cQ']},
                         lead={k: z[k] for k in ('vhat', 'ahat_long', 'lead_found', 'track_id', 'nis_last', 'nees_v', 'dx_pred3', 'age', 'now')},
                         ph_t=ph_t, ph_e=ph_e, t_stop=t_stop))
    return runs


def classify(r_s, c_s, barely):
    lo_r = r_s['ci'][0]; c_lo, c_hi = c_s['ci']
    if lo_r > 0:
        cls = 'recovers'
    elif c_lo > DELTA:
        cls = 'uninformative variation'
    elif c_lo > -DELTA and c_hi < DELTA:
        cls = 'amplitude-limited'
    else:
        cls = 'inconclusive'
    return dict(classification=cls, barely_varies=bool(barely), rule='A10 H3 wording applied to old runs; exploratory print only')


def per_update(runs, mask_fn, key):
    vals = []; keys = set(); run_of = []
    for ri, r in enumerate(runs):
        z = r['lead']; m = mask_fn(r) & z['lead_found'].astype(bool)
        st = np.round(z['now'] - z['age'], 3)
        for i in np.flatnonzero(m):
            kk = (r['run'], int(z['track_id'][i]), float(st[i]))
            if kk in keys or not np.isfinite(z[key][i]):
                continue
            keys.add(kk); vals.append(float(z[key][i])); run_of.append(ri)
    return np.array(vals), np.array(run_of, int)


def run_boot_mean(vals, run_of, nrun, CNT):
    if vals.size == 0:
        return None
    s = np.bincount(run_of, weights=vals, minlength=nrun); c = np.bincount(run_of, minlength=nrun).astype(float)
    with np.errstate(invalid='ignore', divide='ignore'):
        b = (CNT @ s) / (CNT @ c)
    return dict(n=int(vals.size), mean=float(vals.mean()), median=float(np.median(vals)), mean_ci=L.pct(b))


def main():
    variant = sys.argv[1]; NB = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    BOOT_POPS = sys.argv[3].split(',') if len(sys.argv) > 3 else ['all', 'tru_stopped', 'est_stopped']   # sensitivities: 'all' only
    OUTD.mkdir(parents=True, exist_ok=True)
    t00 = time.time()
    runs = load(variant)
    doc = dict(code='b_analysis_v01.py', variant=variant, status='exploratory (A10 section 3); old evaluation runs', populations=POPN,
               definitions='B_retrack/B_ANALYSIS_DEFINITIONS_v01.md', nboot=NB,
               draw='first %d rows of default_rng(20261113).integers(0, 35, (20000, 35)), runs in name order' % NB)
    # ---- margin ratio and the E5 family
    rat = S.margin_ratios(runs, 'N', 'F0')
    rs = S.ratio_summary(rat)
    doc['ratio_N_F0'] = rs
    u, uinfo = S.e5_u(runs, 'F0', 'E')
    doc['e5_ranks'] = uinfo
    up = S.permute_u(runs, u)
    S.add_oracle(runs, 'E5', 'F0', S.RATIO, S.E5_AMP, u)
    S.add_oracle(runs, 'E5p', 'F0', S.RATIO, S.E5_AMP, up)
    S.add_oracle(runs, 'E5x', 'F0', rs['median'], rs['A'], u)
    S.add_oracle(runs, 'E5px', 'F0', rs['median'], rs['A'], S.permute_u(runs, u))
    names = SRC + ['E5', 'E5p', 'E5x', 'E5px']
    G = S.gridless(runs, ['F0', 'E'] + names)
    print('gridless built (%.0f s)' % (time.time() - t00), flush=True)
    pts = {}
    for pi, pn in enumerate(POPN):
        p = S.rr_gl(G, 'F0', 'E', names, pop=pi)
        pts[pn] = p
    doc['points'] = pts
    # grid (secondary): RR on the 202-value grid, all decisions
    X = C.tables(runs, ('W1',), ['F0', 'E'] + names)
    gp = C.points(X, ['E'] + names, pops=[0, 7])
    doc['grid_points'] = {POPN[pi]: dict(R_pp=gp[pi]['denE'] / L.NLEV, RR={a: L.ratio(gp[pi]['D'][a], gp[pi]['denE']) for a in names},
                                         R_deceq=L.dec_eq(gp[pi]['denE'], gp[pi]['n'])) for pi in (0, 7)}
    # ---- bootstrap: all decisions and the after-stop population (truth phase 2)
    CNT = C.cnt_of_record()[:NB]
    ci = {}
    for pn in BOOT_POPS:
        pi = POPN.index(pn)
        b = S.boot_gl(G, 'F0', 'E', names, CNT, pop=pi)
        e = dict(R_pp=L.summ(b['denE'] / L.NLEV, pts[pn]['R_pp']),
                 R_deceq=dict(point=pts[pn]['R_deceq'], ci=L.pct(L.dec_eq(b['denE'], b['n']))))
        for a in names:
            e['RR_' + a] = S.rr_summary(pts[pn], b, a)
        with np.errstate(invalid='ignore', divide='ignore'):
            dif = np.where(b['denE'] > 0, (b['D']['E5'] - b['D']['E5p']) / b['denE'], np.nan)
        e['RR_E5_minus_E5p'] = L.summ(dif, pts[pn]['RR']['E5'] - pts[pn]['RR']['E5p'])
        ci[pn] = e
        print('bootstrap %s done (%.0f s)' % (pn, time.time() - t00), flush=True)
    doc['intervals'] = ci
    doc['ceiling'] = dict(c_x=ci['all']['RR_E5x'], m_x=rs['median'], A_x=rs['A'])
    doc['classification_exploratory'] = classify(ci['all']['RR_N'], ci['all']['RR_E5x'], rs['barely_varies'])
    if ci['all']['RR_N']['ci'][0] > 0 and np.isfinite(pts['all']['RR']['E5x']) and pts['all']['RR']['E5x'] != 0:
        doc['efficiency_r_over_c'] = pts['all']['RR']['N'] / pts['all']['RR']['E5x']
    # ---- lag, NIS and NEES by phase
    lag = []
    for r in runs:
        z = r['lead']; m = r['ev'] & (r['ph_t'] == 2) & (r['t_stop'] >= 0) & (r['t_stop'] < 1) & z['lead_found'].astype(bool)
        lag.append(z['dx_pred3'][m])
    lag = np.concatenate(lag); lag = lag[np.isfinite(lag)]
    doc['lag_dx3_first_second_after_stop'] = dict(n=int(lag.size), median=float(np.median(lag)) if lag.size else None,
                                                  q25=float(np.percentile(lag, 25)) if lag.size else None, q75=float(np.percentile(lag, 75)) if lag.size else None)
    nn = {}
    for key, nm in (('nis_last', 'NIS'), ('nees_v', 'NEES_v')):
        for pk, pfn in (('est_before', lambda r: r['ev'] & (r['ph_e'] == 0)), ('est_braking', lambda r: r['ev'] & (r['ph_e'] == 1)),
                        ('est_stopped', lambda r: r['ev'] & (r['ph_e'] == 2)), ('tru_before', lambda r: r['ev'] & (r['ph_t'] == 0)),
                        ('tru_braking', lambda r: r['ev'] & (r['ph_t'] == 1)), ('tru_stopped', lambda r: r['ev'] & (r['ph_t'] == 2)),
                        ('all', lambda r: r['ev'])):
            v, ro = per_update(runs, pfn, key)
            nn['%s_%s' % (nm, pk)] = run_boot_mean(v, ro, len(runs), CNT)
    doc['nis_nees_by_phase'] = nn
    # ---- B8(a): after-stop decisions (truth phase 2) whose lead speed estimate exceeds 0.5 m/s: counts per run and their share of the
    #      after-stop room, by the attribution of record (a9_4b_attribution_v01: grid step frontier, per-level argmin points, source E)
    pi = POPN.index('tru_stopped')
    Tsum = {a: X[a].sum(axis=0)[:, pi, :] for a in ('F0', 'E')}
    cur = L.curves_w(Tsum, 0)
    cF0, wF0 = cur['F0']; cE, wE = cur['E']
    lev = L.levels_of(cF0, cE, cF0[0])
    fF0, aF0 = S.A9.frontier_argmin(cF0, wF0, lev); fE, aE = S.A9.frontier_argmin(cE, wE, lev)
    cntF0 = np.bincount(aF0[aF0 >= 0], minlength=len(C.GRID)).astype(float)
    cntE = np.bincount(aE[aE >= 0], minlength=len(C.GRID)).astype(float)
    tot = 0.; hi = 0.; per_run = []
    for r in runs:
        m = r['masks'][pi]; safe = r['clear1'] > 0.; ar = np.arange(r['ev'].size)
        sF0 = C.sel_of(r, 'F0'); sE = C.sel_of(r, 'E')
        contrib = (cntF0 @ ((~safe[ar[None, :], sF0]) & m[None, :]) - cntE @ ((~safe[ar[None, :], sE]) & m[None, :])) / L.NLEV
        vh = r['lead']['vhat']; fast = m & np.isfinite(vh) & (vh > 0.5)
        tot += contrib[m].sum(); hi += contrib[fast].sum()
        per_run.append(dict(run=r['run'], n_after_stop=int(m.sum()), n_vhat_gt_0p5=int(fast.sum()), contrib_deceq=float(contrib[fast].sum())))
    doc['b8a_after_stop_vhat_gt_0p5'] = dict(grid_after_stop_room_deceq=L.dec_eq(float(np.sum(fF0 - fE)), float(Tsum['F0'][0, 0])),
                                              attributed_total_deceq=float(tot), attributed_vhat_gt_0p5_deceq=float(hi),
                                              n_decisions=int(sum(x['n_vhat_gt_0p5'] for x in per_run)), per_run=per_run,
                                              method='a9_4b attribution of record, source E, grid, truth phase 2')
    doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    (OUTD / ('B_%s_v01.json' % variant)).write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    print(json.dumps(dict(variant=variant, R_pp=pts['all']['R_pp'], RR_N=ci['all']['RR_N'], c_x=ci['all']['RR_E5x'], ratio=rs,
                          cls=doc['classification_exploratory'], lag=doc['lag_dx3_first_second_after_stop']), default=float), flush=True)


if __name__ == '__main__':
    main()
