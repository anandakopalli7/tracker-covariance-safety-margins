"""B6 recount: (a) terciles of realised lead deceleration, reaction-and-stop room vs 3 s room; (b) delayed variable stop.
usage: python b6.py [nboot]   (CV0 / record arrays)"""
import sys, json, glob, time
import numpy as np
from rc_core import *

ARCH = PA + r'\07_fit_runs\archives'
SRC = [('F0', 'cF0'), ('E', 'cE'), ('N', 'cN'), ('NA', 'cNA'), ('AM', 'cA1'), ('CK3', 'cCK3'), ('Q', 'cQ')]
SHARE = ['N', 'NA', 'AM', 'CK3', 'Q']


def capture_dir(run):
    return glob.glob(r'%s\%s\x\%s\capture\*\\' % (ARCH, run, run))[0]


def realised_decel(run):
    """minus the least-squares slope of the true lead (target) speed vs time between 90% and 10% of its pre-brake speed.
    Pre-brake speed: the lead's speed 3 truth ticks before the tick nearest (t_ref + brake_start_s), t_ref = 5.05 s (the time of
    tick k = 100; the braking onset in the truth is at that offset from contract draw.brake_start_s). Fit ticks: from 2 ticks before
    that tick on, speed within [0.1, 0.9] of the pre-brake speed."""
    d = capture_dir(run)
    L_ = [json.loads(l) for l in open(d + 'evaluation_truth.jsonl')]
    c = json.load(open(d + 'contract.json'))['case']['draw']
    t = np.array([x['time'] for x in L_]); v = np.array([np.hypot(*x['target']['velocity_lh'][:2]) for x in L_])
    t_ref = t[99]
    j = int(np.argmin(np.abs(t - (t_ref + c['brake_start_s']))))
    vp = v[max(j - 3, 0)]
    sel = (np.arange(len(t)) >= j - 2) & (v <= 0.9 * vp) & (v >= 0.1 * vp)
    slope = np.polyfit(t[sel], v[sel], 1)[0]
    return -float(slope), dict(vpre=float(vp), j=j, brake_mps2=c['brake_mps2'], n_fit=int(sel.sum()))


def realised_decel_rule(run):
    """Rule of record (B_ANALYSIS_DEFINITIONS 'Realised lead deceleration'): v = |velocity_lh| of target at tick k, t = 0.05 k;
    v_pre = median v over 3 < t < 5 + brake_start_s - 0.2 (else max of first 20 samples); samples 0.1 v_pre < v < 0.9 v_pre and
    t > 5 + brake_start_s - 0.5; if >= 4, contiguous index range first..last such sample, minus polyfit slope; else NaN."""
    d = capture_dir(run)
    L_ = [json.loads(l) for l in open(d + 'evaluation_truth.jsonl')]
    c = json.load(open(d + 'contract.json'))['case']['draw']
    kk = np.array([x['k'] for x in L_]); t = 0.05 * kk
    v = np.array([np.sqrt(x['target']['velocity_lh'][0] ** 2 + x['target']['velocity_lh'][1] ** 2 + x['target']['velocity_lh'][2] ** 2) for x in L_])
    bs = c['brake_start_s']
    m = (t > 3) & (t < 5 + bs - 0.2)
    vp = float(np.median(v[m])) if m.any() else float(np.max(v[:20]))
    sel = np.nonzero((v > 0.1 * vp) & (v < 0.9 * vp) & (t > 5 + bs - 0.5))[0]
    if sel.size < 4:
        return float('nan'), dict(vpre=vp, n=int(sel.size))
    ii = np.arange(sel[0], sel[-1] + 1)
    return -float(np.polyfit(t[ii], v[ii], 1)[0]), dict(vpre=vp, n=int(ii.size))


def score_pop(data, names, clearR, gridless=True, with_O=True):
    """Room and shares of the run subset `names` under the scoring of clearR (dict run -> (n_eval,17) or None for 3 s)."""
    rs = RunSet({n: data[n] for n in names}, names)
    Td = {}
    scoring = (lambda q: scoring_3s(q)) if clearR is None else None
    for nm, k in SRC + ([('O', None)] if with_O else []):
        T = 0
        if nm == 'O':
            G = np.array([0.])
        else:
            Cl = [q[k] for q in rs.d]
            G = breakpoints(Cl) if gridless else GRID
        for q, name in zip(rs.d, rs.names):
            c1 = L.clean_clear(q['clear'])
            sx = (c1 > 0.) if clearR is None else (L.clean_clear(clearR[name]) > 0.)
            masks = [np.ones(len(q['k']), bool)]
            if nm == 'O':
                sel = L.select_first_safe(sx, q['idx55'])
                T = T + L.stats_scored(sel, c1, sx, q['vbar'], q['des'], masks)
            elif gridless:
                T = T + stats_curve(q[k], G, c1, sx, q['vbar'], q['des'], q['idx55'], masks)
            else:
                T = T + stats_grid(q[k], G, c1, sx, q['vbar'], q['des'], q['idx55'], masks)
        Td[nm] = T[:, 0, :]
    ev = L.eval_scoring(Td, SHARE + (['O'] if with_O else []))
    n = ev['n']
    out = dict(n=n, R_pp=ev['denE'] / 201., room_deceq=L.dec_eq(ev['denE'], n))
    if with_O:
        out['den0_deceq'] = L.dec_eq(ev['D']['O'], n)
        out['evaluable_den0_ge10'] = bool(out['den0_deceq'] >= 10.)
    for a in SHARE:
        out['RR_' + a] = L.ratio(ev['D'][a], ev['denE'])
    out['_denE'] = ev['denE']
    return out


def main(nboot=2000):
    t0 = time.time()
    data = {r: load_record(r) for r in RUNS}
    packs = {r: load_pack(r) for r in RUNS}
    clearR = {r: packs[r][data[r]['evaluated'].astype(bool)] for r in RUNS}
    dec = {}; info = {}
    dec_old = {}
    for r in RUNS:
        dec_old[r], info[r] = realised_decel(r)
        dec[r], info[r]['rule'] = realised_decel_rule(r)
    order = sorted(RUNS, key=lambda r: (dec[r] if np.isfinite(dec[r]) else np.inf, r))
    order_old = sorted(RUNS, key=lambda r: (dec_old[r], r))
    terc_old = [sorted(str(s) for s in a) for a in np.array_split(np.array(order_old), 3)]
    terc = [list(a) for a in np.array_split(np.array(order), 3)]
    res = dict(realised_decel={r: dec[r] for r in RUNS}, realised_decel_onset_reading_sensitivity=dec_old, terciles_onset_reading=terc_old, decel_info=info,
               range=[min(dec.values()), max(dec.values())], terciles={})
    for ti, names in enumerate(terc):
        names = [str(s) for s in names]
        decs = [dec[n] for n in names]
        wr = score_pop(data, names, clearR); s3 = score_pop(data, names, None, with_O=False)
        wrg = score_pop(data, names, clearR, gridless=False); s3g = score_pop(data, names, None, gridless=False, with_O=False)
        res['terciles']['T%d' % (ti + 1)] = dict(
            runs=names, decel_range=[min(decs), max(decs)], n_runs=len(names),
            WR=wr, room3s=s3, ratio_WR_to_3s=wr['_denE'] / s3['_denE'], grid_WR=wrg, grid_room3s=s3g,
            grid_ratio=wrg['_denE'] / s3g['_denE'])
    res['all35'] = dict(WR=score_pop(data, RUNS, clearR), room3s=score_pop(data, RUNS, None, with_O=False))
    print('terciles done', time.time() - t0, flush=True)
    # delayed stop
    bdir = os.environ.get('B6DIR', os.path.join(OUT.replace('recount', 'out'), 'b6', 'clear'))
    files = [os.path.exists(r'%s\%s.npz' % (bdir, r)) for r in RUNS]
    res['b6b_files_present'] = int(sum(files))
    rng = np.random.default_rng(20261916)
    tau_my = {}
    for r in RUNS:
        n = int(data[r]['evaluated'].sum())
        tau_my[r] = 0.75 + rng.uniform(0., 0.75, n)
    if all(files):
        cl = {}; chk = {}; mx = 0.
        for r in RUNS:
            z = np.load(r'%s\%s.npz' % (bdir, r), allow_pickle=True)
            ev = data[r]['evaluated'].astype(bool)
            tau_st = z['tau']
            tau_st_ev = tau_st[ev] if tau_st.shape[0] == ev.shape[0] else tau_st
            chk[r] = float(np.max(np.abs(tau_st_ev - tau_my[r])))
            c = z['clear']
            cl[r] = c[ev] if c.shape[0] == ev.shape[0] else c
        res['b6b_tau_max_abs_diff'] = max(chk.values()); res['b6b_tau_diff_per_run'] = chk
        d = score_pop(data, RUNS, cl); dg = score_pop(data, RUNS, cl, gridless=False)
        res['delayed'] = dict(gridless=d, grid=dg)
        # run bootstrap intervals (gridless) for room and RR(N)
    else:
        res['delayed'] = None
    return res


if __name__ == '__main__':
    r = main()
    json.dump(r, open(os.environ.get('B6OUT', OUT + '\\parts\\b6.json'), 'w'), indent=1, default=float)
    for k, v in r['terciles'].items():
        print(k, v['decel_range'], 'WR room dec-eq', v['WR']['room_deceq'], '3s room', v['room3s']['room_deceq'], 'ratio', v['ratio_WR_to_3s'], 'den0', v['WR']['den0_deceq'])
    print(r['range'], r['all35']['WR']['room_deceq'], r['all35']['WR']['den0_deceq'], r['all35']['room3s']['room_deceq'])
