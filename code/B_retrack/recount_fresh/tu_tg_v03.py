r"""Second program, TU.RR_TG (spec B_FRESH_DEFINITIONS_v02 s6e).  New file; imports the frozen b6tu / rf_core.
Usage (python -I -B -X utf8 tu_tg_v03.py ...):
  --test-old [--K n]   35 old evaluation runs, v12 out\tg cTG2; gridless + grid RR(TG) points (+ optional K-row bootstrap over the
                       35-run draw of record); writes out\TESTOLD_TU_TG_v03.json
  --tuning [--K 20000] 20 tuning runs, B_retrack\out\tu\tg\<run>.npz cTG2 (NOT to be run before the freeze); writes
                       out\part_tu_tg_v03.json (flat TU.RR_TG, TU.RR_TG.ci) and out\boot_tu_tg_v03.npz (D_TG, denE)
  --combine-tg         adds the two keys to B_retrack\out\A_RECOUNT_B.json (refuses if any existing key would change;
                       old file kept as A_RECOUNT_B_v02_220keys.json)"""
import os, sys, json, time, shutil, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from rf_core import L, NS, RunSet, breakpoints, stats_curve, stats_grid
import b6tu as B

OUTD = HERE + r'\out'
V12TG = r'ARS_TRIAL\revision_v12\analysis\out\tg'
TUTG = B.BR + r'\out\tu\tg'
FINAL = B.BR + r'\out\A_RECOUNT_B.json'
KEEP = B.BR + r'\out\A_RECOUNT_B_v02_220keys.json'


def load(mode):
    if mode == 'old':
        names = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
        data = {r: B.load_record(r) for r in names}; tgd = V12TG
    else:
        names, data = B.tu_load(); tgd = TUTG
    for r in names:
        z = np.load(r'%s\%s.npz' % (tgd, r), allow_pickle=True)
        assert z['k'].shape == data[r]['k'].shape and (z['k'] == data[r]['k']).all(), 'TG k differs: ' + r
        data[r]['cTG'] = np.asarray(z['cTG2'], float)       # r0 = 2 m/s
    return names, data


def compute(mode, K, log=print):
    t0 = time.time()
    names, data = load(mode)
    rs = RunSet(data, names); nr = len(names)
    srcs = [('F0', 'cF0'), ('E', 'cE'), ('TG', 'cTG')]
    Trun = {}; Tg = {}
    for nm, k in srcs:
        Cl = [q[k] for q in rs.d]; G = breakpoints(Cl)
        Tr = []; tg = 0
        for q, C in zip(rs.d, Cl):
            c1 = L.clean_clear(q['clear']); sx = c1 > 0.; m = [np.ones(len(q['k']), bool)]
            Tr.append(stats_curve(C, G, c1, sx, q['vbar'], q['des'], q['idx55'], m)[:, 0, :].copy())
            tg = tg + stats_grid(C, B.GRID, c1, sx, q['vbar'], q['des'], q['idx55'], m)
        Trun[nm] = np.stack(Tr); Tg[nm] = tg[:, 0, :]
    def ev(T):
        return L.eval_scoring(T, ['TG'])
    eg = ev({s: Trun[s].sum(axis=0) for s in Trun})
    egr = ev(Tg)
    res = {'TU.RR_TG': L.ratio(eg['D']['TG'], eg['denE'])}
    extra = dict(n=eg['n'], denE_gl=eg['denE'], D_TG_gl=eg['D']['TG'], R_pp_gl=eg['denE'] / 201.,
                 D_TG_gl_deceq=L.dec_eq(eg['D']['TG'], eg['n']),
                 RR_TG_grid=L.ratio(egr['D']['TG'], egr['denE']), D_TG_grid=egr['D']['TG'], denE_grid=egr['denE'],
                 D_TG_grid_deceq=L.dec_eq(egr['D']['TG'], egr['n']), R_pp_grid=egr['denE'] / 201., n_runs=nr)
    log('points %.1fs' % (time.time() - t0), flush=True)
    out = None
    if K:
        seed = 20261918 if mode == 'tu' else 20261113
        cnt = L.boot_counts(nr, 20000, seed)[:K]
        flat = {s: Trun[s].reshape(nr, -1) for s in Trun}
        out = {k: np.full(K, np.nan) for k in ['denE', 'D_TG']}
        Gt = max(Trun[s].shape[1] for s in Trun); chunk = max(1, min(40, int(4e6 // (Gt * NS)))); tb = time.time()
        for b0 in range(0, K, chunk):
            c = cnt[b0:b0 + chunk]
            Tb = {s: (c @ flat[s]).reshape(len(c), -1, NS) for s in flat}
            for j in range(len(c)):
                e = ev({s: Tb[s][j] for s in Tb})
                out['denE'][b0 + j] = e['denE']; out['D_TG'][b0 + j] = e['D']['TG']
            if (b0 // chunk) % 100 == 0:
                log('boot %d/%d %.1fs' % (b0, K, time.time() - tb), flush=True)
        pos = out['denE'] > 0
        with np.errstate(divide='ignore', invalid='ignore'):
            res['TU.RR_TG.ci'] = L.pct(np.where(pos, out['D_TG'] / out['denE'], np.nan))
        extra.update(K=K, boot_seconds=time.time() - tb, boot_ms_per_resample=1000 * (time.time() - tb) / K, n_valid=int(pos.sum()))
    extra['total_seconds'] = time.time() - t0
    return res, out, extra


def combine():
    new = json.load(open(OUTD + r'\part_tu_tg_v03.json'))['res']
    assert set(new) == {'TU.RR_TG', 'TU.RR_TG.ci'}
    old = json.load(open(FINAL))
    for k in new:
        if k in old:
            raise SystemExit('REFUSED: key already present: ' + k)
    if not os.path.exists(KEEP):
        shutil.copy2(FINAL, KEEP)
    merged = dict(old); merged.update(new)
    assert all(merged[k] == old[k] for k in old) and len(merged) == len(old) + 2
    json.dump(merged, open(FINAL, 'w'), indent=1)
    print('combined: %d keys -> %d; old kept at %s' % (len(old), len(merged), KEEP))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true'); ap.add_argument('--tuning', action='store_true')
    ap.add_argument('--combine-tg', action='store_true'); ap.add_argument('--K', type=int, default=None)
    a = ap.parse_args()
    os.makedirs(OUTD, exist_ok=True)
    if a.combine_tg:
        combine()
    elif a.test_old:
        K = 0 if a.K is None else a.K
        res, out, ex = compute('old', K)
        json.dump(dict(res=res, extra=ex), open(OUTD + r'\TESTOLD_TU_TG_v03.json', 'w'), indent=1)
        print(res, ex)
    elif a.tuning:
        K = 20000 if a.K is None else a.K
        res, out, ex = compute('tu', K)
        json.dump(dict(res=res, extra=ex), open(OUTD + r'\part_tu_tg_v03.json', 'w'), indent=1)
        np.savez(OUTD + r'\boot_tu_tg_v03.npz', **out)
        print(res)
