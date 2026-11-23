"""B9 recount: cut-in event detector, window sizes, track-age strata, RR_gl(N) and room in window and young-track population."""
import sys, json, csv, time
import numpy as np
from rc_core import *
import b_variants as bv

IDX = PA + r'\09_redesign\m4_perception_model\run_index_m4_v02.csv'
THR = 1.75
WIN = (-1.0, 4.0)


def cutin_runs():
    rows = list(csv.DictReader(open(IDX)))
    return [(r['run_id'], r['cap']) for r in rows if r['set'] == 'tune' and r['family'] == 'cutin' and r['use'] == '1']


def read_jsonl(p):
    return [json.loads(l) for l in open(p)]


def event_tick(T, thr=THR, inst=False):
    """first truth tick with the primary actor (target) ahead (along-route centre distance > 0) and its centre within thr laterally of
    the ego lane centre (median ego lateral route coordinate over the run, spec D-B9-1)."""
    ego = np.array([t['ego']['derived']['center_rh'][:2] for t in T]); psi = np.array([t['ego']['derived']['route_yaw_rh'] for t in T])
    tg = np.array([t['target']['derived']['center_rh'][:2] for t in T])
    c, s = np.cos(psi), np.sin(psi)
    d = tg - ego
    along = c * d[:, 0] + s * d[:, 1]
    lat_e = -s * ego[:, 0] + c * ego[:, 1]; lat_t = -s * tg[:, 0] + c * tg[:, 1]
    lane = lat_e if inst else np.median(lat_e)
    ok = (along > 0) & (np.abs(lat_t - lane) <= thr)
    if not ok.any():
        return None
    k = int(np.argmax(ok))
    return dict(k=k, t=float(T[k]['time']), idx=int(T[k]['k']))


def births(D):
    b = {}
    for fr in D:
        for tr in fr['tracks']:
            b.setdefault(int(tr['id']), float(fr['time']))
    return b


def ages_for(run, cap, ks):
    """per assessment decision (in order of the stored k): track age of the youngest track matched to the primary actor, NaN if
    untracked. matching: planner-frame actor position predicted to `now`; true primary actor in the planner frame (ego centre and
    route yaw at the decision tick); nearest within 4 m."""
    T = read_jsonl(cap + r'\evaluation_truth.jsonl'); F = read_jsonl(cap + r'\frames.jsonl'); D = read_jsonl(cap + r'\detections.jsonl')
    bt = births(D)
    ass = {f['k']: f['execution']['new_decision'] for f in F if f.get('execution', {}).get('new_decision', {}).get('mode') == 'assessment'}
    age = np.full(len(ks), np.nan); nmatch = np.zeros(len(ks), int); now = np.full(len(ks), np.nan)
    for i, k in enumerate(ks):
        d = ass[int(k)]; t = T[int(k)]
        now[i] = d['now']
        e = np.array(t['ego']['derived']['center_rh'][:2]); psi = t['ego']['derived']['route_yaw_rh']
        a = np.array(t['target']['derived']['center_rh'][:2]); dx, dy = a - e
        p = np.array([np.cos(psi) * dx + np.sin(psi) * dy, -np.sin(psi) * dx + np.cos(psi) * dy])
        best = []
        for ac in d['actors']:
            dt = d['now'] - ac['state_time']
            pp = np.array([ac['x'] + ac['vx'] * dt, ac['y'] + ac['vy'] * dt])
            if np.hypot(*(pp - p)) <= 4.0:
                best.append(d['now'] - bt[int(ac['track_id'])])
        nmatch[i] = len(best)
        if best:
            age[i] = min(best)
    return age, nmatch, now, T


def main(nboot=2000):
    runs = cutin_runs()
    names = [r for r, _ in runs]
    data = {}; info = {}
    for r, cap in runs:
        g = np.load(r'%s\%s.npz' % (REC_G, r), allow_pickle=True)
        q = {k: g[k] for k in ['k', 'evaluated', 'v0', 'des', 'clear', 'vbar', 'idx55', 'cF0', 'cE', 'cN']}
        q['prim_age_stored'] = g['prim_age']
        age, nm, now, T = ages_for(r, cap, q['k'])
        q['age'] = age; q['nmatch'] = nm; q['now'] = now
        ev_ = event_tick(T); ev25 = event_tick(T, 2.5); evi = event_tick(T, THR, inst=True)
        info[r] = dict(event=ev_, event_thr2p5=ev25, event_inst_lane=evi)
        q['t_c'] = ev_['t'] if ev_ else np.nan; q['k_c'] = ev_['idx'] if ev_ else None
        data[r] = q
    rs = RunSet(data, names)
    res = dict(n_runs=len(names), runs_with_event=int(sum(1 for r in names if info[r]['event'])),
               runs_without_event=[r for r in names if not info[r]['event']],
               events_same_with_instant_lane=int(sum(1 for r in names if info[r]['event'] == info[r]['event_inst_lane'] or
                                                     (info[r]['event'] and info[r]['event_inst_lane'] and info[r]['event']['k'] == info[r]['event_inst_lane']['k']))),
               events_with_thr_2p5=int(sum(1 for r in names if info[r]['event_thr2p5'])))
    per = {}
    pops = {'window': [], 'young': [], 's_lt1': [], 's_1_4': [], 's_ge4': [], 'untracked': []}
    for r, q in zip(names, rs.d):
        n_all_ev = len(q['k'])
        dt = (q['k'] - q['k_c']) * 0.05 if q['k_c'] is not None else np.full(len(q['k']), np.nan)
        with np.errstate(invalid='ignore'):
            win = (np.round(dt / 0.05) * 0.05 >= WIN[0] - 1e-9) & (np.round(dt / 0.05) * 0.05 <= WIN[1] + 1e-9)
        a = q['age']; tr = np.isfinite(a)
        m = {'window': win, 'young': win & tr & (a < 1.0), 's_lt1': win & tr & (a < 1.0), 's_1_4': win & tr & (a >= 1.0) & (a < 4.0),
             's_ge4': win & tr & (a >= 4.0), 'untracked': win & ~tr}
        for k in pops:
            pops[k].append(m[k])
        stored = q['prim_age_stored']
        cmpd = np.isfinite(a) & np.isfinite(stored)
        per[r] = dict(event=info[r]['event'], n_evaluated=n_all_ev, window=int(m['window'].sum()), young=int(m['young'].sum()),
                      lt1=int(m['s_lt1'].sum()), s1_4=int(m['s_1_4'].sum()), ge4=int(m['s_ge4'].sum()), untracked=int(m['untracked'].sum()),
                      age_max_abs_diff_vs_stored_prim_age=float(np.max(np.abs(a[cmpd] - stored[cmpd]))) if cmpd.any() else None,
                      n_age_nan_but_stored_finite=int((~np.isfinite(a) & np.isfinite(stored)).sum()))
    res['per_run'] = per
    res['window_total'] = int(sum(v['window'] for v in per.values()))
    res['strata_totals'] = {k: int(sum(m.sum() for m in pops[k])) for k in pops}
    # intervals
    idx = np.random.default_rng(20261113).integers(0, 20, (20000, 20))[:nboot]
    cnt = np.zeros((nboot, 20))
    for b in range(nboot):
        cnt[b] = np.bincount(idx[b], minlength=20)
    res['populations'] = {}
    for pn in ['window', 'young', 's_lt1', 's_1_4', 's_ge4', 'untracked']:
        pm = pops[pn]
        if sum(m.sum() for m in pm) == 0:
            res['populations'][pn] = dict(n=0); continue
        ms = margin_stats(margin_ratio_rows(rs, pm)) if True else None
        u = ranks_u(rs, masks=pm)
        Cs = {'F0': [q['cF0'] for q in rs.d], 'E': [q['cE'] for q in rs.d], 'N': [q['cN'] for q in rs.d], 'E5N': oracle_C(rs, u, ms['median'], ms['A'])}
        S = {}
        for nm, Cl in Cs.items():
            G = breakpoints(Cl)
            Tr = []
            for q, C, m in zip(rs.d, Cl, pm):
                c1, sx = scoring_3s(q)
                Tr.append(stats_curve(C, G, c1, sx, q['vbar'], q['des'], q['idx55'], [m])[:, 0, :])
            Tr = np.stack(Tr)
            S[nm] = dict(G=G, Trun=Tr, Tsum=Tr.sum(axis=0)[:, None, :])
        To = 0
        for q, m in zip(rs.d, pm):
            c1, sx = scoring_3s(q)
            To = To + L.stats_scored(L.select_first_safe(sx, q['idx55']), c1, sx, q['vbar'], q['des'], [m])
        S['O'] = dict(G=np.array([0.]), Tsum=To, Trun=None)
        pt = bv.pop_eval(S, 0, ['N', 'E5N', 'O'])
        entry = dict(n=pt['n'], R_pp=pt['R_pp'], room_deceq=pt['room_deceq'], RR_N=pt['RR_N'], D_deceq_N=pt['D_deceq_N'],
                     ceiling_RR_E5N=pt['RR_E5N'], den0_deceq=pt['D_deceq_O'], margin=ms, evaluable_room_ge10=bool(pt['room_deceq'] >= 10.))
        if pn in ('window', 'young'):
            B = bv.boot(S, ['N', 'E5N'], cnt)
            for k, v in B.items():
                entry['ci_' + k] = L.pct(v); entry['invalid_' + k] = float(1 - np.isfinite(v).mean())
            entry['H3_style'] = bv.classify(entry['ci_RR_N'], entry['ci_RR_E5N'], ms['share_within5'] >= 0.95)
            entry['H3_style']['note'] = 'young: not evaluable if room < 10 dec-eq (K2); window: K0 needs den0 >= 10'
        res['populations'][pn] = entry
        print(pn, entry['n'], entry['room_deceq'], entry['RR_N'], flush=True)
    return res


if __name__ == '__main__':
    r = main(int(sys.argv[1]) if len(sys.argv) > 1 else 2000)
    json.dump(r, open(OUT + r'\parts\b9.json', 'w'), indent=1, default=float)
    print({k: r[k] for k in ['runs_with_event', 'runs_without_event', 'window_total', 'strata_totals', 'events_with_thr_2p5', 'events_same_with_instant_lane']})
