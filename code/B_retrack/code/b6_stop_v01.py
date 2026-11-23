"""v13 package B, B6 (AMENDMENT_10_v13 section 3 row B6) on the 35 old evaluation lead-braking runs, online tracker of record
(record arrays and the reaction-and-stop cache of record). Exploratory. New file, 19 Nov 2026 (Claude Opus 5.5). Writes out\\b6\\.

(a) Terciles of realised lead deceleration (trk_score_v01.realised_decel = rev_h_run_facts_v01 rule; ascending, ties by id, 12/12/11).
    Per tercile, on its own frontier (gridless primary, grid beside): the room under W_R(tau 0.75 s, A 6 m/s^2) (cached stop clearance
    > 0), the room under the 3 s commitment (W1), their ratio, den0 = D(F0, O) under W_R in decision-equivalents (evaluable if >= 10),
    and RR of N, CK3 under W_R. Also all 35 runs.
(b) Delayed, variable stop: tau_i = 0.75 + delta_i, delta_i ~ U(0, 0.75) per evaluated decision (default_rng(20261916); runs in name
    order, decisions in k order), A = 6 m/s^2 (trk_score_v01.delayed_stop_clearance). Room, den0, RR of N, NA, AM, CK3, Q under
    that scoring; intervals from the first 2,000 rows of the draw of record.
Usage: python -I -B -X utf8 b6_stop_v01.py clear <part> <nparts>   (delayed-stop clearances per run, cached in out\\b6\\clear\\)
       python -I -B -X utf8 b6_stop_v01.py score
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

OUTD = pathlib.Path(__file__).resolve().parents[1] / 'out' / 'b6'
ARCH = S.P / '07_fit_runs' / 'archives'
NB = 2000
KEY = 't0p75_a6p0'


def cap_of(run):
    return list((ARCH / run / 'x' / run / 'capture').iterdir())[0]


def delays(runs):
    """One generator, runs in name order, evaluated decisions in k order."""
    d = S.draw_delays(int(sum(r['ev'].sum() for r in runs)))
    out = {}; pos = 0
    for r in runs:
        ev = np.flatnonzero(r['ev'])
        out[r['run']] = {int(i): 0.75 + float(x) for i, x in zip(ev, d[pos:pos + ev.size])}
        pos += ev.size
    return out


def evaluate(runs, safe_fn, names, with_boot=True):
    G = S.gridless(runs, ['F0', 'E'] + names + ['O'], safe_fn)
    p = S.rr_gl(G, 'F0', 'E', names + ['O'])
    out = dict(R_pp=p['R_pp'], R_deceq=p['R_deceq'], den0_deceq=p['D_deceq']['O'], RR={a: p['RR'][a] for a in names}, n=p['n'],
               evaluable_den0=bool(p['D_deceq']['O'] >= 10.))
    if with_boot:
        CNT = L.boot_counts(len(runs), 20000, 20261113)[:NB]
        b = S.boot_gl(G, 'F0', 'E', names + ['O'], CNT)
        out['R_pp_ci'] = L.summ(b['denE'] / L.NLEV, p['R_pp'])['ci']
        out['den0_deceq_ci'] = L.pct(L.dec_eq(b['D']['O'], b['n']))
        out['RR_ci'] = {a: S.rr_summary(p, b, a)['ci'] for a in names}
    return out, G, p


def main():
    OUTD.mkdir(parents=True, exist_ok=True); (OUTD / 'clear').mkdir(exist_ok=True)
    runs = C.load_runs()
    for r in runs:
        r['ev'] = r['ev'].astype(bool)
        r['crit'] = {'F0': r['crit']['F0'], 'E': r['crit']['E'], 'N': r['crit']['N'], 'NA': r['crit']['NA'], 'AM': r['crit']['A1'],
                     'CK3': r['crit']['CK3'], 'Q': r['crit']['Q']}
        r['masks'] = (r['ev'],)
    if sys.argv[1] == 'clear':
        part, nparts = int(sys.argv[2]), int(sys.argv[3])
        D = delays(runs)
        for i, r in enumerate(runs):
            if i % nparts != part:
                continue
            f = OUTD / 'clear' / (r['run'] + '.npz')
            if f.exists():
                continue
            t0 = time.time()
            cl = S.delayed_stop_clearance(ARCH / r['run'], cap_of(r['run']), D[r['run']], A=6.0)
            taus = np.full(r['ev'].size, np.nan)
            for di, t in D[r['run']].items():
                taus[di] = t
            np.savez_compressed(f, clear=cl, tau=taus, k=r['k'])
            print(r['run'], round(time.time() - t0, 1), flush=True)
        return
    t00 = time.time()
    doc = dict(code='b6_stop_v01.py', status='exploratory; A10 B6 on the 35 old evaluation runs (online tracker of record)', nboot=NB)
    # (a) terciles
    ids = [r['run'] for r in runs]
    dec = [S.realised_decel(cap_of(x)) for x in ids]
    T3 = S.terciles(ids, dec)
    doc['realised_decel'] = dict(zip(ids, dec))
    doc['terciles'] = []
    wr = lambda r: L.clean_clear(r['cache'][KEY]) > 0.          # noqa: E731
    for ti, members in enumerate([ids] + T3):
        sub = [r for r in runs if r['run'] in members]
        for r in sub:
            r['sel'] = {}
        a_wr, _, _ = evaluate(sub, wr, ['N', 'CK3'])
        a_3s, _, _ = evaluate(sub, S.safe_w1, ['N', 'CK3'])
        dd = [d for x, d in zip(ids, dec) if x in members and d is not None]
        doc['terciles'].append(dict(name='all' if ti == 0 else 'tercile %d' % ti, runs=members, decel_min_max=[min(dd), max(dd)] if dd else None,
                                    W_R=a_wr, W1=a_3s, room_ratio_WR_over_3s=(a_wr['R_pp'] / a_3s['R_pp'] if a_3s['R_pp'] > 0 else None)))
        print('tercile', ti, round(a_wr['R_pp'], 3), round(a_3s['R_pp'], 3), round(time.time() - t00), flush=True)
    # (b) delayed stop
    D = delays(runs)
    for r in runs:
        z = np.load(OUTD / 'clear' / (r['run'] + '.npz'))
        if not np.array_equal(z['k'], r['k']):
            raise SystemExit('REFUSED: delayed-stop clearances of %s do not match k' % r['run'])
        r['clear_delay'] = z['clear']; r['sel'] = {}
        tz = z['tau']; ev = np.flatnonzero(r['ev'])
        if not np.allclose(tz[ev], [D[r['run']][int(i)] for i in ev]):
            raise SystemExit('REFUSED: tau draw differs')
    dl = lambda r: L.clean_clear(r['clear_delay']) > 0.         # noqa: E731
    b_res, _, _ = evaluate(runs, dl, ['N', 'NA', 'AM', 'CK3', 'Q'])
    doc['delayed_stop'] = dict(rule='tau_i = 0.75 + U(0, 0.75), 6 m/s^2; default_rng(20261916)', **b_res)
    fixed, _, _ = evaluate(runs, wr, ['N', 'NA', 'AM', 'CK3', 'Q'], with_boot=False)
    doc['fixed_tau_0p75_point'] = fixed
    doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    (OUTD / 'B6_STOP_v01.json').write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    print(json.dumps(dict(terciles=[(t['name'], t['decel_min_max'], t['room_ratio_WR_over_3s'], t['W_R']['evaluable_den0']) for t in doc['terciles']],
                          delayed=dict(R_pp=b_res['R_pp'], den0=b_res['den0_deceq'], RR=b_res['RR'])), default=float), flush=True)


if __name__ == '__main__':
    main()
