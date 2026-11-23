import json, os, numpy as np
from rc_core import *
from b6 import capture_dir
import b_variants as bv
CACHE_T = OUT + r'\parts\truth_vel_cache.npz'
if not os.path.exists(CACHE_T):
    tv = {}
    for r in RUNS:
        Lr = [json.loads(l) for l in open(capture_dir(r) + 'evaluation_truth.jsonl')]
        tv[r + '_t'] = np.array([x['time'] for x in Lr])
        tv[r + '_v'] = np.array([[x['target']['velocity_lh'][0], -x['target']['velocity_lh'][1]] for x in Lr])
        tv[r + '_psi'] = np.array([x['ego']['derived']['route_yaw_rh'] for x in Lr])
    np.savez(CACHE_T, **tv)
TV = np.load(CACHE_T)
idx = np.random.default_rng(20261113).integers(0, 35, (20000, 35))[:2000]
cnt = np.stack([np.bincount(i, minlength=35) for i in idx]).astype(float)
KEYS = ['truth0', 'truth1', 'truth2', 'truth3', 'est_before', 'est_braking', 'est_stopped']

def one(x):
    per = {m: {k: [] for k in KEYS} for m in ('nis', 'nees')}
    unmatched = 0
    for r in RUNS:
        z = load_variant(x, r); ev = z['evaluated'].astype(bool)
        sel = np.nonzero(ev & z['lead_found'].astype(bool))[0]
        st = np.round(z['now'] - z['age'], 3)
        tid = z['trk_id']; tst = np.round(z['trk_state_time'], 3)
        lut = {(int(a), float(b)): i for i, (a, b) in enumerate(zip(tid, tst))}
        keys = [(int(z['track_id'][i]), float(st[i])) for i in sel]
        first = {}
        for j, kk in enumerate(keys):
            if np.isfinite(z['nis_last'][sel[j]]) and kk not in first:
                first[kk] = sel[j]
        em = bv.est_phase_masks({'lead_found': z['lead_found'], 'vhat': z['vhat'], 'ahat_long': z['ahat_long']}, -1.0)
        ph = z['phase']; tt = TV[r + '_t']; tvv = TV[r + '_v']; psi = TV[r + '_psi']
        vals = {k: ([], []) for k in KEYS}
        for kk, i in first.items():
            nis = float(z['nis_last'][i])
            nees = np.nan
            if kk in lut:
                m = lut[kk]
                kt = int(np.argmin(np.abs(tt - kk[1])))
                c, s = np.cos(psi[kt]), np.sin(psi[kt])
                R = np.array([[c, s], [-s, c]])   # world -> route
                e = R @ (np.array([z['trk_vx'][m], z['trk_vy'][m]]) - tvv[kt])
                P = R @ z['trk_P4'][m][2:4, 2:4] @ R.T
                nees = float(e @ np.linalg.solve(P, e))
            else:
                unmatched += 1
            grp = ['truth%d' % int(ph[i])]
            grp.append('est_before' if em[0][i] else 'est_braking' if em[1][i] else 'est_stopped')
            for g in grp:
                vals[g][0].append(nis); vals[g][1].append(nees)
        for g in KEYS:
            a = np.array(vals[g][0]); b = np.array(vals[g][1])
            per['nis'][g].append((a.sum(), len(a), a))
            bf = b[np.isfinite(b)]
            per['nees'][g].append((bf.sum(), len(bf), bf))
    out = {'unmatched_updates': unmatched}
    for m in ('nis', 'nees'):
        out[m] = {}
        for g in KEYS:
            s = np.array([p[0] for p in per[m][g]]); c = np.array([p[1] for p in per[m][g]], float)
            allv = np.concatenate([p[2] for p in per[m][g]])
            with np.errstate(divide='ignore', invalid='ignore'):
                bm = (cnt @ s) / (cnt @ c)
            out[m][g] = dict(n=int(c.sum()), mean=float(s.sum() / c.sum()) if c.sum() else float('nan'),
                             median=float(np.median(allv)) if allv.size else float('nan'), ci=L.pct(bm))
    return out

res = {x: one(x) for x in VARIANTS}
json.dump(res, open(OUT + r'\parts\nis_amend1.json', 'w'), indent=1, default=float)
for x in ('CV0', 'B1'):
    for m in ('nis', 'nees'):
        print(x, m, {g: (v['n'], round(v['mean'], 3), round(v['median'], 3), [round(a, 3) for a in v['ci']]) for g, v in res[x][m].items()})
print({x: res[x]['unmatched_updates'] for x in res})
