"""Revision v12, AMENDMENT_09 A9-5 (review item R11): the 3 s scoring of record on the 20 lead-braking tuning runs, beside the
35 evaluation runs. New file, 19 Nov 2026. Stored arrays (gateR_rt_v01) and the A4 tuning extraction (11_ojits/A4/dryrun/extract:
phases and the NA, AM, CK3, Q critical scales), read-only. Points only (the tuning runs had no intervals of record).
Identity: the tuning room's summed F0 - E frontier difference equals Table S2 (237.24).
Per set: decisions, phase mix, share with the ego moving, the room of each population, the in-sample per-phase gain of F0 (the
rev_b2 definition) and the shares of N, NA, AM, CK3 pooled and by population.
Usage: python -B -X utf8 a9_5_tuning_runs_v01.py
"""
import json, time
import numpy as np
import a9_common_v01 as A
C = A.C; L = A.L

OUTF = A.OUT / 'A9_5_TUNING_RUNS_v01.json'
if OUTF.exists():
    raise SystemExit('REFUSED: %s exists' % OUTF)
t00 = time.time()
TX = C.OJ / 'A4' / 'dryrun' / 'extract'
TUNE = sorted(p.stem for p in TX.glob('*.npz'))


def load_tuning():
    runs = []
    for run in TUNE:
        z = np.load(C.STORED / (run + '.npz'), allow_pickle=False)
        m = json.loads(str(z['meta']))
        if m.get('family') != 'lead_braking':
            raise SystemExit('REFUSED: %s is not a lead-braking run' % run)
        x = np.load(TX / (run + '.npz'), allow_pickle=False)
        if not np.array_equal(x['k'], z['k']):
            raise SystemExit('REFUSED: decision ticks differ for %s' % run)
        ev = z['evaluated'].astype(bool); v0 = z['v0']; ph = x['phase'].astype(np.int64)
        runs.append(dict(run=run, desired=float(m['desired']), k=z['k'], ev=ev, v0=v0, ph=ph, vbar=z['vbar'], idx55=z['idx55'],
                         clear1=L.clean_clear(z['clear']), masks=C.masks_of(ev, v0, ph), n_dec=len(z['k']),
                         crit={'F0': z['cF0'], 'E': z['cE'], 'N': z['cN'], 'NA': x['cNA'], 'A1': x['cA1'], 'CK3': x['cCK3'],
                               'Q': x['cQ']}, sel={}, late={}))
    return runs


ARMS = ['N', 'NA', 'A1', 'CK3', 'Q']
PN = ['all', 'moving', 'phase0', 'phase1', 'phase2']


def describe(runs):
    X = C.tables(runs, ('W1',), ['F0', 'E'] + ARMS)
    pts = C.points(X, ['E'] + ARMS, pops=range(5))
    out = dict(n_runs=len(runs))
    ev_all = np.concatenate([r['ev'] for r in runs]); ph = np.concatenate([r['ph'][r['ev']] for r in runs])
    v0 = np.concatenate([r['v0'][r['ev']] for r in runs])
    out['n_evaluated'] = int(ev_all.sum())
    out['phase_counts'] = {str(p): int((ph == p).sum()) for p in range(4)}
    out['share_after_stop'] = float((ph == 2).mean()); out['share_ego_le_0p5'] = float((v0 <= 0.5).mean())
    for pi, pn in enumerate(PN):
        p = pts[pi]
        ent = dict(n=p['n'], R_pp=p['denE'] / L.NLEV, R_summed=p['denE'], R_deceq=L.dec_eq(p['denE'], p['n']))
        for a in ARMS:
            ent['RR_' + a] = L.ratio(p['D'][a], p['denE'])
        out[pn] = ent
    # decision-weighted mean of the phase rooms and the in-sample per-phase gain of F0 (rev_b2 definition)
    ns = [out['phase%d' % q]['n'] for q in range(3)]; rs = [out['phase%d' % q]['R_pp'] for q in range(3)]
    out['phase_weighted_room_pp'] = float(sum(n * r for n, r in zip(ns, rs)) / sum(ns))
    out['pooled_over_phase_weighted'] = out['all']['R_pp'] / out['phase_weighted_room_pp']
    Tsum = {a: X[a].sum(axis=0) for a in ('F0', 'E')}
    Tall = Tsum['F0'][:, 0, :]; TE = Tsum['E'][:, 0, :]
    cur = L.curves_w({'F0': Tall, 'E': TE}, 0); cF0, wF0 = cur['F0']; cE, wE = cur['E']
    lev = L.levels_of(cF0, cE, cF0[0]); f1 = L.frontier(cF0, wF0, lev)
    U = [np.unique(np.stack([Tsum['F0'][:, pi, 1], Tsum['F0'][:, pi, 2], Tsum['F0'][:, pi, 3]], axis=1), axis=0) for pi in (2, 3, 4)]
    n = float(Tall[0, 0])
    W = (U[0][:, 0][:, None, None] + U[1][:, 0][None, :, None] + U[2][:, 0][None, None, :]).ravel()
    S = (U[0][:, 1][:, None, None] + U[1][:, 1][None, :, None] + U[2][:, 1][None, None, :]).ravel()
    K = (U[0][:, 2][:, None, None] + U[1][:, 2][None, :, None] + U[2][:, 2][None, None, :]).ravel()
    with np.errstate(divide='ignore', invalid='ignore'):
        fps = L.frontier(100. * S / K, 100. * W / n, lev)
    out['per_phase_gain_pp'] = float(np.sum(f1 - fps)) / L.NLEV
    out['per_phase_gain_share'] = float(np.sum(f1 - fps)) / (out['all']['R_summed'])
    return out


doc = dict(code='a9_5_tuning_runs_v01.py', status='post hoc, descriptive; AMENDMENT_09 A9-5', tuning_runs=TUNE)
tr = load_tuning()
doc['tuning'] = describe(tr)
doc['identity_tuning_room_vs_table_S2'] = dict(here=doc['tuning']['all']['R_summed'], table_S2=237.24,
                                               abs_diff=abs(doc['tuning']['all']['R_summed'] - 237.24))
doc['evaluation'] = describe(C.load_runs())
doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S'); doc['seconds'] = time.time() - t00
A.write_out(OUTF, doc)
print(json.dumps({k: doc[k] for k in ('identity_tuning_room_vs_table_S2',)}, indent=1))
print('written %s (%.0f s)' % (OUTF, time.time() - t00))
