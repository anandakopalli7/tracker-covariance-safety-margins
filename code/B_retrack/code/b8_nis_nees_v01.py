"""v13 package B, B8(b) and B1's "NIS and NEES by phase" (AMENDMENT_10_v13 section 3), definition of B_ANALYSIS_DEFINITIONS_v01.md
Amendment 1 (19 Nov 18:40 EST). New file, 19 Nov 2026 (Claude Opus 5.5). Exploratory. Writes out\\b8\\B8_NIS_NEES_v01.json.
For every tracker variant x and the 35 old evaluation runs: distinct lead-track updates (first evaluated decision assigns the phase),
NIS = nis_last; NEES_v at the update with the true lead velocity at the state time; means by truth and estimated phase with run-level
intervals (first 2,000 rows of default_rng(20261113).integers(0, 35, (20000, 35))).
Usage: python -I -B -X utf8 b8_nis_nees_v01.py
"""
import sys, json, pathlib, time, math
import numpy as np
HERE = pathlib.Path(__file__).resolve().parents[1]
RT = HERE / 'out' / 'retrack'
P = pathlib.Path(r'<library folder>')
ARCH = P / '07_fit_runs' / 'archives'
VARS = ['CV0', 'B3', 'B2', 'B4', 'B1', 'B1_d090', 'B1_d098']
RUNS = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
NB = 2000


def truth(run):
    cap = next((ARCH / run / 'x' / run / 'capture').iterdir())
    T = {}; route_yaw = None
    for line in open(cap / 'evaluation_truth.jsonl', encoding='utf-8'):
        if not line.strip():
            continue
        r = json.loads(line)
        if route_yaw is None:
            route_yaw = float(r['ego']['derived']['route_yaw_rh'])
        tg = r.get('target'); v = None
        if tg:
            a = [x for x in (r.get('scenario_actors') or []) if x['actor_id'] == tg['actor_id']]
            if a:
                v = (a[0]['velocity_lh'][0], -a[0]['velocity_lh'][1])
        T[r['k']] = (float(r['time']), v)
    ks = np.array(sorted(T)); times = np.array([T[k][0] for k in ks])
    return T, ks, times, route_yaw


def est_phase(vhat, ah, fd, thr=-1.0):
    ph = np.zeros(vhat.shape, np.int8)
    ph[fd & (vhat > 0.5) & np.isfinite(ah) & (ah <= thr)] = 1
    ph[fd & (vhat <= 0.5)] = 2
    return ph


def main():
    t00 = time.time()
    rng = np.random.default_rng(20261113)
    CNT = np.zeros((20000, 35))
    idx = rng.integers(0, 35, (20000, 35))
    for b in range(20000):
        CNT[b] = np.bincount(idx[b], minlength=35)
    CNT = CNT[:NB]
    TR = {run: truth(run) for run in RUNS}
    doc = dict(code='b8_nis_nees_v01.py', definition='B_ANALYSIS_DEFINITIONS_v01.md, Amendment 1', nboot=NB, variants={})
    for x in VARS:
        rec = {('tru', p): [] for p in (0, 1, 2, 3)}
        rec.update({('est', p): [] for p in (0, 1, 2)})
        miss_trk = 0
        for ri, run in enumerate(RUNS):
            z = np.load(RT / x / (run + '_arrays.npz'), allow_pickle=False)
            T, ks, times, ryaw = TR[run]
            c, s = math.cos(ryaw), math.sin(ryaw)
            ev = z['evaluated'].astype(bool); fd = z['lead_found'].astype(bool)
            ph_t = z['phase']; ph_e = est_phase(z['vhat'], z['ahat_long'], fd)
            st = np.round(z['now'] - z['age'], 3)
            trk = {(int(i), round(float(t), 3)): j for j, (i, t) in enumerate(zip(z['trk_id'], z['trk_state_time']))}
            seen = set()
            for di in np.flatnonzero(ev & fd):
                key = (int(z['track_id'][di]), float(st[di]))
                if key in seen:
                    continue
                seen.add(key)
                if not np.isfinite(z['nis_last'][di]):
                    continue                                   # not an update (birth or a coasted state)
                j = trk.get(key)
                nees = np.nan
                if j is None:
                    miss_trk += 1
                else:
                    vw = np.array([z['trk_vx'][j], z['trk_vy'][j]]); P4 = z['trk_P4'][j]
                    R = np.array([[c, s], [-s, c]])
                    v_trk = R @ vw; Pvv = R @ P4[2:4, 2:4] @ R.T
                    kt = int(ks[np.argmin(np.abs(times - key[1]))])
                    vt = T[kt][1]
                    if vt is not None:
                        e = v_trk - R @ np.array(vt)
                        nees = float(e @ np.linalg.solve(Pvv, e))
                rec[('tru', int(ph_t[di]))].append((ri, float(z['nis_last'][di]), nees))
                rec[('est', int(ph_e[di]))].append((ri, float(z['nis_last'][di]), nees))
        out = dict(updates_without_tracker_record=miss_trk)
        for (kind, p), L in rec.items():
            name = '%s_phase%d' % (kind, p)
            if not L:
                out[name] = dict(n=0); continue
            ro = np.array([a for a, _, _ in L]); nis = np.array([b for _, b, _ in L]); nees = np.array([cc for _, _, cc in L])
            ent = {}
            for nm, v in (('NIS', nis), ('NEES_v', nees)):
                ok = np.isfinite(v)
                sm = np.bincount(ro[ok], weights=v[ok], minlength=35); cn = np.bincount(ro[ok], minlength=35).astype(float)
                with np.errstate(invalid='ignore', divide='ignore'):
                    b = (CNT @ sm) / (CNT @ cn)
                f = np.isfinite(b)
                ent[nm] = dict(n=int(ok.sum()), mean=float(v[ok].mean()) if ok.any() else None, median=float(np.median(v[ok])) if ok.any() else None,
                               mean_ci=[float(q) for q in np.percentile(b[f], [2.5, 97.5])] if f.any() else [None, None])
            out[name] = ent
        doc['variants'][x] = out
        print(x, {k: (v.get('NIS', {}).get('n'), round(v['NIS']['mean'], 3) if v.get('NIS', {}).get('mean') is not None else None,
                      round(v['NEES_v']['mean'], 3) if v.get('NEES_v', {}).get('mean') is not None else None)
                  for k, v in out.items() if isinstance(v, dict) and 'NIS' in v}, flush=True)
    doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    od = HERE / 'out' / 'b8'; od.mkdir(parents=True, exist_ok=True)
    (od / 'B8_NIS_NEES_v01.json').write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')


if __name__ == '__main__':
    main()
