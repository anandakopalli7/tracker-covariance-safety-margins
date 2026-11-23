"""Per-variant recount (room, shares, margin ratio, E5 family, phases, lag, NIS/NEES). usage: python b_variants.py <variant|REC> [nboot]"""
import sys, json, time
import numpy as np
from rc_core import *

DELTA = 0.05
SRC = [('F0', 'cF0'), ('E', 'cE'), ('N', 'cN'), ('NA', 'cNA'), ('AM', 'cA1'), ('CK3', 'cCK3'), ('Q', 'cQ')]


def est_phase_masks(q, thr):
    lf = q['lead_found'].astype(bool); v = q['vhat']; a = q['ahat_long']
    with np.errstate(invalid='ignore'):
        st = lf & (v <= 0.5); br = lf & (v > 0.5) & (a <= thr)
    return [~(st | br), br, st]          # before braking, braking, stopped


def mask_list(q):
    n = len(q['k']); ph = q['phase']
    m = [np.ones(n, bool)]
    m += [ph == p for p in range(4)]
    for thr in (-1.0, -0.5, -2.0):
        m += est_phase_masks(q, thr)
    return m


MNAMES = ['all', 'truth0', 'truth1', 'truth2', 'truth3'] + ['est%s_%s' % (t, p) for t in ('m1.0', 'm0.5', 'm2.0') for p in ('before', 'braking', 'stopped')]


def sources_stats(rs, Cs, keep, masks_fn=mask_list):
    """Cs name -> list of C arrays. returns name -> dict(G, Tsum (G,M,5), Trun (nr,G,5) or None)."""
    out = {}
    for nm, Cl in Cs.items():
        G = breakpoints(Cl)
        Tsum = None; Trun = []
        for q, C in zip(rs.d, Cl):
            c1, sx = scoring_3s(q)
            T = stats_curve(C, G, c1, sx, q['vbar'], q['des'], q['idx55'], masks_fn(q))
            Tsum = T.copy() if Tsum is None else Tsum + T
            if nm in keep:
                Trun.append(T[:, 0, :].copy())
        out[nm] = dict(G=G, Tsum=Tsum, Trun=np.stack(Trun) if Trun else None)
    return out


def pop_eval(S, mi, names):
    Td = {nm: S[nm]['Tsum'][:, mi, :] for nm in ['F0', 'E'] + names}
    ev = L.eval_scoring(Td, names)
    n = ev['n']
    res = dict(n=n, R_pp=ev['denE'] / 201., room_deceq=L.dec_eq(ev['denE'], n) if n else float('nan'))
    for a in names:
        res['RR_' + a] = L.ratio(ev['D'][a], ev['denE']); res['D_deceq_' + a] = L.dec_eq(ev['D'][a], n) if n else float('nan')
    return res


def boot(S, names, cnt, chunk=20):
    B = cnt.shape[0]; nm_all = ['F0', 'E'] + names
    res = {k: np.full(B, np.nan) for k in ['R_pp', 'room_deceq'] + ['RR_' + a for a in names]}
    for b0 in range(0, B, chunk):
        c = cnt[b0:b0 + chunk]
        Tb = {nm: (c @ S[nm]['Trun'].reshape(S[nm]['Trun'].shape[0], -1)).reshape(len(c), -1, NS) for nm in nm_all}
        for j in range(len(c)):
            ev = L.eval_scoring({nm: Tb[nm][j] for nm in nm_all}, names)
            res['R_pp'][b0 + j] = ev['denE'] / 201.; res['room_deceq'][b0 + j] = L.dec_eq(ev['denE'], ev['n'])
            for a in names:
                res['RR_' + a][b0 + j] = L.ratio(ev['D'][a], ev['denE'])
    return res


def classify(r_ci, c_ci, barely):
    if r_ci[0] > 0:
        k = 'a_recovers'
    elif c_ci[0] > DELTA:
        k = 'b_uninformative_variation'
    elif c_ci[0] > -DELTA and c_ci[1] < DELTA:
        k = 'c_amplitude_limited'
    else:
        k = 'd_inconclusive'
    return dict(cls=k, barely_varies=bool(barely))


def nis_nees(rs, cnt):
    """one value per distinct (run, track_id, state time = now-age rounded 1 ms) at evaluated decisions with a lead track
    (first such decision in k order carries the value and the phase)."""
    keys = ['truth0', 'truth1', 'truth2', 'truth3', 'est_before', 'est_braking', 'est_stopped']
    per = {m: {k: [] for k in keys} for m in ('nis', 'nees')}
    out = {}
    for q in rs.d:
        lf = q['lead_found'].astype(bool)
        st = np.round(q['now'] - q['age'], 3)
        seen = set(); first = np.zeros(len(q['k']), bool)
        for i in range(len(first)):
            if not lf[i]:
                continue
            key = (int(q['track_id'][i]), float(st[i]))
            if key not in seen:
                seen.add(key); first[i] = True
        em = est_phase_masks(q, -1.0)
        grp = {'truth%d' % p: first & (q['phase'] == p) for p in range(4)}
        grp.update({'est_before': first & em[0], 'est_braking': first & em[1], 'est_stopped': first & em[2]})
        for m, key in (('nis', 'nis_last'), ('nees', 'nees_v')):
            x = q[key]
            for g, mk in grp.items():
                sel = mk & np.isfinite(x)
                per[m][g].append((x[sel].sum(), int(sel.sum()), x[sel].copy()))
    for m in ('nis', 'nees'):
        out[m] = {}
        for g in keys:
            s = np.array([p[0] for p in per[m][g]]); c = np.array([p[1] for p in per[m][g]], float)
            allv = np.concatenate([p[2] for p in per[m][g]])
            mean = s.sum() / c.sum() if c.sum() else float('nan')
            with np.errstate(divide='ignore', invalid='ignore'):
                bm = (cnt @ s) / (cnt @ c)
            out[m][g] = dict(n=int(c.sum()), mean=float(mean), median=float(np.median(allv)) if allv.size else float('nan'),
                             ci=L.pct(bm), runs_with=int((c > 0).sum()))
    return out


def lag_of(data):
    vals = []
    for nm in RUNS:
        r = data[nm]; ph = r['phase']
        i2 = np.nonzero(ph == 2)[0]
        if not i2.size:
            continue
        kstop = r['k'][i2[0]]
        ev = r['evaluated'].astype(bool)
        sel = ev & (ph == 2) & ((r['k'] - kstop) * 0.05 >= -1e-9) & ((r['k'] - kstop) * 0.05 < 1.0 - 1e-9) & np.isfinite(r['dx_pred3'])
        vals.append(r['dx_pred3'][sel])
    vv = np.concatenate(vals) if vals else np.array([])
    return dict(median_dx_pred3=float(np.median(vv)) if vv.size else float('nan'), n=int(vv.size))


def run(x, nboot):
    t0 = time.time()
    data = {r: load_variant(x, r) for r in RUNS}
    rs = RunSet(data, RUNS)
    cnt = np.zeros((nboot, 35))
    idx = np.random.default_rng(20261113).integers(0, 35, (20000, 35))[:nboot]
    for b in range(nboot):
        cnt[b] = np.bincount(idx[b], minlength=35)
    res = dict(variant=x, n_eval_per_run=dict(zip(RUNS, rs.n_eval)), n_eval_total=int(sum(rs.n_eval)))
    ms = margin_stats(margin_ratio_rows(rs)); res['margin_ratio'] = ms
    u = ranks_u(rs); up = permute_u(u)
    Cs = {nm: [q[k] for q in rs.d] for nm, k in SRC}
    Cs['E5'] = oracle_C(rs, u, M_REC, A_REC); Cs['E5p'] = oracle_C(rs, up, M_REC, A_REC)
    Cs['E5x'] = oracle_C(rs, u, ms['median'], ms['A']); Cs['E5px'] = oracle_C(rs, up, ms['median'], ms['A'])
    S = sources_stats(rs, Cs, keep={'F0', 'E', 'N', 'E5', 'E5x'})
    print(x, 'stats done', time.time() - t0, flush=True)
    names5 = ['N', 'NA', 'AM', 'CK3', 'Q', 'E5', 'E5p', 'E5x', 'E5px']
    allp = pop_eval(S, 0, names5)
    res['all'] = allp
    res['room_pp'] = allp['R_pp']; res['room_deceq'] = allp['room_deceq']
    res['populations'] = {}
    for mi, nm in enumerate(MNAMES):
        e = pop_eval(S, mi, ['N'])
        res['populations'][nm] = dict(n=e['n'], R_pp=e['R_pp'], room_deceq=e['room_deceq'], RR_N=e['RR_N'])
    res['after_stop_room_deceq'] = res['populations']['truth2']['room_deceq']
    Tg = {}
    for nm, k in [('F0', 'cF0'), ('E', 'cE'), ('N', 'cN'), ('NA', 'cNA'), ('AM', 'cA1'), ('CK3', 'cCK3'), ('Q', 'cQ')]:
        T = 0
        for q in rs.d:
            c1, sx = scoring_3s(q)
            T = T + stats_grid(q[k], GRID, c1, sx, q['vbar'], q['des'], q['idx55'], [np.ones(len(q['k']), bool)])
        Tg[nm] = T[:, 0, :]
    eg = L.eval_scoring(Tg, ['N', 'NA', 'AM', 'CK3', 'Q'])
    res['grid'] = dict(R_pp=eg['denE'] / 201., n=eg['n'], **{'RR_' + a: L.ratio(eg['D'][a], eg['denE']) for a in ['N', 'NA', 'AM', 'CK3', 'Q']})
    B = boot(S, ['N', 'E5', 'E5x'], cnt)
    print(x, 'boot done', time.time() - t0, flush=True)
    pts = {'R_pp': allp['R_pp'], 'room_deceq': allp['room_deceq'], 'RR_N': allp['RR_N'], 'RR_E5': allp['RR_E5'], 'RR_E5x': allp['RR_E5x']}
    res['intervals'] = {k: dict(point=pts[k], ci=L.pct(v), invalid_share=float(1 - np.isfinite(v).mean())) for k, v in B.items()}
    r_ci = res['intervals']['RR_N']['ci']; c_ci = res['intervals']['RR_E5x']['ci']
    res['ceiling_c'] = allp['RR_E5x']
    res['H3'] = classify(r_ci, c_ci, ms['share_within5'] >= 0.95)
    if r_ci[0] > 0:
        eff = B['RR_N'] / B['RR_E5x']
        res['H3']['efficiency'] = dict(point=allp['RR_N'] / allp['RR_E5x'], ci=L.pct(eff))
    res['nis_nees'] = nis_nees(rs, cnt)
    res['lag'] = lag_of(data)
    res['seconds'] = time.time() - t0
    return res


if __name__ == '__main__':
    x = sys.argv[1]; nb = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    os.makedirs(OUT + r'\parts', exist_ok=True)
    r = run(x, nb)
    json.dump(r, open(OUT + r'\parts\%s.json' % x, 'w'), indent=1, default=float)
    print(json.dumps({k: r[k] for k in ['room_pp', 'room_deceq', 'ceiling_c', 'H3', 'after_stop_room_deceq', 'lag', 'margin_ratio', 'intervals', 'grid']}, indent=1, default=float))
    print(r['all'])
