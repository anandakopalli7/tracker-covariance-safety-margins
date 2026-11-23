"""v13 sprint, step 0 (coordinator 21 Nov 13:27 EST, author-approved): room and descriptive shares in the two crossing families on the
STORED runs of record, as design data for a locked confirmatory crossing test. New file, 21 Nov 2026 (Claude Opus 5.5). Old data only.
Inputs (read-only): the stored arrays of record (P\\09_redesign\\m2_decisions\\openloop\\gateR_rt_v01\\<run>.npz: cF0 with the P-bar of
record, cE, cN, clear, vbar, idx55, evaluated, des; online tracker of record) of every stored run whose meta family is vehicle_crossing
(22: 20 tuning + 2 fit) or pedestrian_crossing (51: 20 tuning + 31 fit); runs in name order. Tuning-only (20 + 20) beside.
Per family: gridless step frontier at 201 caution levels, 3 s commitment, all evaluated decisions (as TU, b_tu_v02.py):
  R = D_gl(E, F0) as mean gap (pp) and decision-equivalents; RR_gl(N); RR_gl(E5_N) with m, A from the family's own margin ratio
  sqrt(c_F0 / c_N) at binding rows and ranks from F0 / E (A10 section 2.2, as K2's E5_N); RR_gl(E5) with the record amplitude
  (1.1029, 0.05) beside. Intervals: optA_lib_v02.boot_counts(n_runs, 20000, 20261121), percentile 95% and 90% (shares over resamples
  with D_gl(E, F0) > 0). Engine: package CD's gl_fast_v13 (read-only).
n needed (plug-in): SE(n) = SE_tune * sqrt(n_tune / n), SE_tune = bootstrap SD; the lower end of a two-sided (1 - a) interval exceeds 0 with
power p when theta / SE(n) >= z_{1 - a/2} + z_p, so n = n_tune * (SE_tune * (z_{1 - a/2} + z_p) / theta)^2. Check by simulation for one n:
synthetic studies of n runs drawn with replacement from the stored runs (default_rng(20261122)); power = share with
theta_hat - z * SE(n) > 0.
Writes out\\step0\\STEP0_CROSSING_v01.json. Usage: B_retrack\\.venv\\Scripts\\python.exe -I -B -X utf8 b_step0_crossing_v01.py [--threads 2]
"""
import os, sys, argparse
_ap = argparse.ArgumentParser(); _ap.add_argument('--threads', type=int, default=2); ARGS = _ap.parse_args()
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell'); os.environ['NUMBA_NUM_THREADS'] = str(ARGS.threads)
import json, pathlib, time, hashlib, math
HERE = pathlib.Path(__file__).resolve().parents[1]
WORK = HERE.parent
sys.path.insert(0, str(WORK / 'shared' / 'trackers'))
import numpy as np
import trk_score_v01 as S
L = S.L
sys.path.insert(0, str(WORK / 'CD_capture' / 'analysis'))
import gl_fast_v13 as GF

P = pathlib.Path(r'<library folder>')
STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
SEED, NB, SEED_SIM = 20261121, 20000, 20261122
FAMS = ['vehicle_crossing', 'pedestrian_crossing']
Z = {0.95: 1.959963984540054, 0.90: 1.6448536269514722}
ZP = {0.80: 0.8416212335729143, 0.90: 1.2815515655446004}


def load(family, tuning_only=False):
    runs = []
    for f in sorted(STORED.glob('*.npz')):
        z = np.load(f, allow_pickle=False); m = json.loads(str(z['meta']))
        if m.get('family') != family or (tuning_only and m.get('set') != 'tuning'):
            continue
        ev = z['evaluated'].astype(bool)
        runs.append(dict(run=f.stem, set=m.get('set'), desired=float(m['desired']), idx55=z['idx55'].astype(np.int64),
                         clear1=L.clean_clear(z['clear']), vbar=z['vbar'], ev=ev, masks=(ev,), sel={}, late={},
                         crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float)}))
    return runs


def pct(x, level):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    a = (1. - level) / 2. * 100.
    return [float(np.percentile(x, a)), float(np.percentile(x, 100. - a))] if x.size else [None, None]


def evaluate(G, names, W):
    P_ = GF.Prepared(G, ['F0', 'E'] + names, 0)
    parts = [GF.evaluate(P_, W[s:s + 500]) for s in range(0, W.shape[0], 500)]
    return dict(denE=np.concatenate([x['denE'] for x in parts]), n=np.concatenate([x['n'] for x in parts]),
                D={a: np.concatenate([x['D'][a] for x in parts]) for a in names})


def n_needed(theta, se, n_tune):
    out = {}
    for lev, za in Z.items():
        for pw, zp in ZP.items():
            out['interval%d_power%d' % (round(lev * 100), round(pw * 100))] = (
                None if not (theta and se and theta > 0) else int(math.ceil(n_tune * (se * (za + zp) / theta) ** 2)))
    return out


def flags(runs):
    """Item 5: what the scoring sees in these families (all evaluated decisions)."""
    nd = sum(int(r['ev'].sum()) for r in runs); no_bind = 0; any_unsafe = 0; idx55_unsafe = 0; all_unsafe = 0; nonfin = 0; cells = 0
    for r in runs:
        ev = r['ev']; c = r['crit']['F0'][ev]; s1 = r['clear1'][ev] > 0.
        fin = np.isfinite(c) & (c > 0)
        no_bind += int((~fin.any(axis=1)).sum()); nonfin += int((~np.isfinite(c)).sum()); cells += c.size
        any_unsafe += int((~s1).any(axis=1).sum()); all_unsafe += int((~s1).all(axis=1).sum())
        idx55_unsafe += int((~s1[np.arange(s1.shape[0]), r['idx55'][ev]]).sum())
    return dict(evaluated=nd, share_no_binding_constraint_F0=no_bind / nd if nd else None,
                share_F0_cells_nonfinite=nonfin / cells if cells else None,
                share_with_some_row_unsafe_3s=any_unsafe / nd if nd else None, share_all_rows_unsafe_3s=all_unsafe / nd if nd else None,
                share_fallback_row_unsafe_3s=idx55_unsafe / nd if nd else None)


def family(fam, tuning_only=False):
    t0 = time.time()
    runs = load(fam, tuning_only)
    if fam == 'lead_braking':                       # reference only: points and flags of the 20 lead-braking tuning runs
        nr = len(runs); G = S.gridless(runs, ['F0', 'E', 'N']); p = S.rr_gl(G, 'F0', 'E', ['N'], pop=0)
        return dict(family=fam, set='tuning only (reference)', n_runs=nr, evaluated_decisions=int(sum(int(r['ev'].sum()) for r in runs)),
                    points=dict(R_pp=p['R_pp'], R_deceq=p['R_deceq'], RR_N=p['RR']['N']), margin_ratio=S.ratio_summary(S.margin_ratios(runs, 'N', 'F0')),
                    flags=flags(runs))
    nr = len(runs)
    out = dict(family=fam, set='tuning only' if tuning_only else 'all stored runs (tuning + fit)', n_runs=nr,
               runs_by_set={s: sum(1 for r in runs if r['set'] == s) for s in sorted({r['set'] for r in runs})},
               runs_with_evaluated=sum(1 for r in runs if r['ev'].any()), evaluated_decisions=int(sum(int(r['ev'].sum()) for r in runs)))
    rat = S.margin_ratios(runs, 'N', 'F0'); rs = S.ratio_summary(rat); out['margin_ratio'] = rs
    u, uinfo = S.e5_u(runs, 'F0', 'E')
    S.add_oracle(runs, 'E5N', 'F0', rs['median'], rs['A'], u)
    S.add_oracle(runs, 'E5rec', 'F0', S.RATIO, S.E5_AMP, u)
    names = ['N', 'E5N', 'E5rec']
    G = S.gridless(runs, ['F0', 'E'] + names)
    p = S.rr_gl(G, 'F0', 'E', names, pop=0)
    out['points'] = dict(R_pp=p['R_pp'], R_deceq=p['R_deceq'], denE=p['denE'], n=p['n'], RR={a: p['RR'][a] for a in names})
    W = L.boot_counts(nr, NB, SEED)
    b = evaluate(G, names, W)
    rpp = b['denE'] / L.NLEV
    with np.errstate(invalid='ignore', divide='ignore'):
        ok = np.isfinite(b['denE']) & (b['denE'] > 0)
        rr = {a: np.where(ok, b['D'][a] / b['denE'], np.nan) for a in names}
    out['intervals'] = dict(R_pp={str(lv): pct(rpp, lv) for lv in (0.95, 0.90)},
                            R_deceq={str(lv): pct(L.dec_eq(b['denE'], b['n']), lv) for lv in (0.95, 0.90)},
                            RR={a: {str(lv): pct(rr[a], lv) for lv in (0.95, 0.90)} for a in names},
                            share_resamples_room_positive=float(np.mean(b['denE'] > 0)), resamples_valid_for_shares=int(ok.sum()))
    se_r = float(np.std(rpp, ddof=1)); se_e5 = float(np.nanstd(rr['E5N'], ddof=1)); se_e5r = float(np.nanstd(rr['E5rec'], ddof=1))
    rob = lambda x: ((lambda c: (c[1] - c[0]) / (2 * Z[0.95]) if c[0] is not None else None)(pct(x, 0.95)))   # noqa: E731
    se_r_rob = rob(rpp); se_e5_rob = rob(rr['E5N']); se_e5r_rob = rob(rr['E5rec'])
    out['n_needed_robust'] = dict(formula='as n_needed, with SE_tune = (95% percentile width) / (2 * 1.96): robust to resamples with a near-zero room',
                                  R=dict(theta=p['R_pp'], se_tune=se_r_rob, **n_needed(p['R_pp'], se_r_rob, nr)),
                                  E5N=dict(theta=p['RR']['E5N'], se_tune=se_e5_rob, **n_needed(p['RR']['E5N'], se_e5_rob, nr)),
                                  E5rec=dict(theta=p['RR']['E5rec'], se_tune=se_e5r_rob, **n_needed(p['RR']['E5rec'], se_e5r_rob, nr)))
    out['n_needed'] = dict(formula='n = n_tune * (SE_tune * (z_{1-a/2} + z_power) / theta)^2, SE_tune = bootstrap SD, theta = point',
                           n_tune=nr, R=dict(theta=p['R_pp'], se_tune=se_r, **n_needed(p['R_pp'], se_r, nr)),
                           E5N=dict(theta=p['RR']['E5N'], se_tune=se_e5, **n_needed(p['RR']['E5N'], se_e5, nr)),
                           E5rec=dict(theta=p['RR']['E5rec'], se_tune=se_e5r, **n_needed(p['RR']['E5rec'], se_e5r, nr)))
    # simulation check of the plug-in for R at its 80%-power n (95% interval), capped at 400 runs
    n80 = out['n_needed']['R']['interval95_power80']
    if n80:
        n_sim = int(min(max(n80, 5), 400))
        rng = np.random.default_rng(SEED_SIM)
        idx = rng.integers(0, nr, (2000, n_sim)); Wsim = np.zeros((2000, nr))
        for i in range(2000):
            Wsim[i] = np.bincount(idx[i], minlength=nr)
        bs = evaluate(G, [], Wsim)
        th = bs['denE'] / L.NLEV; se_n = se_r * math.sqrt(nr / n_sim)
        out['simulation_check_R'] = dict(n=n_sim, studies=2000, se_plugin=se_n,
                                         power_95=float(np.mean(th - Z[0.95] * se_n > 0)), power_90=float(np.mean(th - Z[0.90] * se_n > 0)),
                                         note='studies of n runs drawn with replacement from the stored runs; power = share with theta_hat - z SE(n) > 0')
    out['flags'] = flags(runs)
    out['seconds'] = time.time() - t0
    return out


def main():
    t00 = time.time()
    doc = dict(code='b_step0_crossing_v01.py', status='descriptive design data on stored runs (needs a second-program recount before print)',
               coordinator='21 Nov 2026 13:27 EST, step 0', draw='optA_lib_v02.boot_counts(n_runs, 20000, 20261121), runs in name order',
               engine='CD_capture/analysis/gl_fast_v13.py sha256 ' + hashlib.sha256((WORK / 'CD_capture' / 'analysis' / 'gl_fast_v13.py').read_bytes()).hexdigest(),
               scoring_notes=['wrong go = the selected row\'s 3 s true clearance to any true actor <= 0 (same rule as lead braking)',
                              'F0 = class-average P-bar of record per actor class (vehicle / pedestrian), N = the online tracker of record',
                              'binding constraint = minimum over all actors and samples (crit_rows); a row with no binding constraint has an infinite critical scale',
                              'no lead-specific quantity is used (no lag, no phase)'],
               families={}, tuning_only={})
    for fam in FAMS:
        doc['families'][fam] = family(fam); print(fam, 'all done', round(time.time() - t00), flush=True)
        doc['tuning_only'][fam] = family(fam, tuning_only=True); print(fam, 'tuning-only done', round(time.time() - t00), flush=True)
    doc['reference_lead_braking_tuning'] = family('lead_braking', tuning_only=True)
    doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    od = HERE / 'out' / 'step0'; od.mkdir(parents=True, exist_ok=True)
    (od / 'STEP0_CROSSING_v01.json').write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    print('written', round(doc['seconds']))


if __name__ == '__main__':
    main()
