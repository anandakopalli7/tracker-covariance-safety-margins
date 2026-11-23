"""v13 package B: TU, the 20 lead-braking tuning runs (A10 section 5.6, "Tuning-run intervals": default_rng(20261918), 20,000 resamples
of the 20 tuning runs, for R and R_gl, the shares of N, NA, AM, CK3 (and TG), grid and gridless, and the per-phase rooms).
New file, 20 Nov 2026 (Claude Opus 5.5). Descriptive. Online tracker of record; old (stored) data only, so no lock gate applies.
Inputs (read-only): the stored arrays of record (gateR_rt_v01: cF0 with the P-bar of record, cE, cN, clearances, rows), v12's A4 tuning
extraction (11_ojits/A4/dryrun/extract: cNA, cA1 (AM), cCK3, cQ, truth phase) — the inputs of revision_v12 a9_5_tuning_runs_v01 — and,
for the tracker-estimated phase only, the lead keys (vhat, ahat_long, lead_found) of B's CV0 replay (B_retrack\\out\\retrack\\CV0\\,
identical to the logs, B0), matched on k.
Gridless step frontier primary (A10 section 2.3); grid points beside, with an identity check against v12's A9_5_TUNING_RUNS_v01.json.
Intervals: optA_lib_v02.boot_counts(20, 20000, 20261918), runs in name order; engine CD's gl_fast_v13 (read-only). TG (supplement)
is not computed here (its tuning-run arrays would need the A9-7 rebuild); TU.RR_TG stays absent.
Writes out\\tu\\TU_v02.json and out\\tu\\boot_tu.npz.
Usage: B_retrack\\.venv\\Scripts\\python.exe -I -B -X utf8 b_tu_v02.py [--threads 2]
"""
import os, sys, argparse
_ap = argparse.ArgumentParser(); _ap.add_argument('--threads', type=int, default=2)
ARGS = _ap.parse_args()
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell'); os.environ['NUMBA_NUM_THREADS'] = str(ARGS.threads)
import json, pathlib, time, hashlib
HERE = pathlib.Path(__file__).resolve().parents[1]
WORK = HERE.parent
sys.path.insert(0, str(WORK / 'shared' / 'trackers'))
import numpy as np
import trk_score_v01 as S
L = S.L; C = S.A9.C
sys.path.insert(0, str(WORK / 'CD_capture' / 'analysis'))
import gl_fast_v13 as GF                          # package CD's engine, read-only

TX = C.OJ / 'A4' / 'dryrun' / 'extract'
A95 = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis\out\A9_5_TUNING_RUNS_v01.json')
RT = HERE / 'out' / 'retrack' / 'CV0'
OUTD = HERE / 'out' / 'tu'
SEED, NBOOT = 20261918, 20000
POPN = ['all', 'moving', 'est_before', 'est_braking', 'est_stopped', 'tru_before', 'tru_braking', 'tru_stopped']
SRC = ['N', 'NA', 'AM', 'CK3', 'Q']


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def load():
    runs = []; ident = []
    for run in sorted(p.stem for p in TX.glob('*.npz')):
        z = np.load(C.STORED / (run + '.npz'), allow_pickle=False); m = json.loads(str(z['meta']))
        if m.get('family') != 'lead_braking':
            raise SystemExit('REFUSED: %s is not a lead-braking run' % run)
        x = np.load(TX / (run + '.npz'), allow_pickle=False); y = np.load(RT / (run + '_arrays.npz'), allow_pickle=False)
        if not (np.array_equal(x['k'], z['k']) and np.array_equal(y['k'], z['k'])):
            raise SystemExit('REFUSED: decision ticks differ for %s' % run)
        ident.append(dict(run=run, cN_equal=bool(np.array_equal(y['cN'], z['cN'], equal_nan=True)),
                          cE_equal=bool(np.array_equal(y['cE'], z['cE'], equal_nan=True)),
                          evaluated_equal=bool(np.array_equal(y['evaluated'], z['evaluated']))))
        ev = z['evaluated'].astype(bool); v0 = z['v0']; ph = x['phase'].astype(np.int64)
        eph = S.est_phase(y['vhat'], y['ahat_long'], y['lead_found'], -1.0)
        masks = (ev, ev & (v0 > 0.5), ev & (eph == 0), ev & (eph == 1), ev & (eph == 2), ev & (ph == 0), ev & (ph == 1), ev & (ph == 2))
        runs.append(dict(run=run, desired=float(m['desired']), k=z['k'], ev=ev, v0=v0, vbar=z['vbar'], idx55=z['idx55'].astype(np.int64),
                         clear1=L.clean_clear(z['clear']), masks=masks, n_dec=len(z['k']), sel={}, late={},
                         crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float),
                               'NA': np.asarray(x['cNA'], float), 'AM': np.asarray(x['cA1'], float), 'CK3': np.asarray(x['cCK3'], float),
                               'Q': np.asarray(x['cQ'], float)}))
    return runs, ident


def main():
    t00 = time.time(); OUTD.mkdir(parents=True, exist_ok=True)
    runs, ident = load()
    if len(runs) != 20:
        raise SystemExit('REFUSED: %d tuning runs, expected 20' % len(runs))
    doc = dict(code='b_tu_v02.py', status='descriptive (A10 section 5.6), old tuning runs', runs=[r['run'] for r in runs], populations=POPN,
               draw='optA_lib_v02.boot_counts(20, 20000, 20261918), runs in name order', nboot=NBOOT,
               engine='CD_capture/analysis/gl_fast_v13.py sha256 ' + sha(WORK / 'CD_capture' / 'analysis' / 'gl_fast_v13.py'),
               lead_keys_source_identity=dict(runs=len(ident), all_equal=all(i['cN_equal'] and i['cE_equal'] and i['evaluated_equal'] for i in ident),
                                              detail=[i for i in ident if not (i['cN_equal'] and i['cE_equal'] and i['evaluated_equal'])]))
    # grid (secondary) and its identity with v12 A9-5
    X = C.tables(runs, ('W1',), ['F0', 'E'] + SRC)
    gp = C.points(X, ['E'] + SRC, pops=range(len(POPN)))
    doc['grid_points'] = {POPN[pi]: dict(n=gp[pi]['n'], R_pp=gp[pi]['denE'] / L.NLEV, R_deceq=L.dec_eq(gp[pi]['denE'], gp[pi]['n']),
                                         RR={a: L.ratio(gp[pi]['D'][a], gp[pi]['denE']) for a in SRC}) for pi in range(len(POPN))}
    rec = json.loads(A95.read_text(encoding='utf-8'))['tuning']; cmp = []
    for mine, theirs in (('all', 'all'), ('moving', 'moving'), ('tru_before', 'phase0'), ('tru_braking', 'phase1'), ('tru_stopped', 'phase2')):
        g = doc['grid_points'][mine]; t = rec[theirs]
        cmp += [(mine + '.n', g['n'], t['n']), (mine + '.R_pp', g['R_pp'], t['R_pp'])]
        cmp += [(mine + '.RR_' + a, g['RR'][a], t['RR_' + ('A1' if a == 'AM' else a)]) for a in SRC]
    doc['grid_identity_vs_v12_A9_5'] = dict(compared=len(cmp), identical=sum(1 for c in cmp if c[1] == c[2]), differing=[c for c in cmp if c[1] != c[2]])
    # gridless (primary)
    G = S.gridless(runs, ['F0', 'E'] + SRC)
    doc['points'] = {pn: S.rr_gl(G, 'F0', 'E', SRC, pop=pi) for pi, pn in enumerate(POPN)}
    CNT = L.boot_counts(len(runs), NBOOT, SEED)
    P = GF.Prepared(G, ['F0', 'E'] + SRC, 0)
    parts = [GF.evaluate(P, CNT[s:s + 500]) for s in range(0, NBOOT, 500)]
    b = dict(denE=np.concatenate([x['denE'] for x in parts]), n=np.concatenate([x['n'] for x in parts]),
             D={a: np.concatenate([x['D'][a] for x in parts]) for a in SRC})
    pt = doc['points']['all']
    e = dict(R_pp=L.summ(b['denE'] / L.NLEV, pt['R_pp']), R_deceq=dict(point=pt['R_deceq'], ci=L.pct(L.dec_eq(b['denE'], b['n']))))
    for a in SRC:
        e['RR_' + a] = S.rr_summary(pt, b, a)
    doc['intervals'] = {'all': e}
    np.savez_compressed(OUTD / 'boot_tu.npz', denE=b['denE'], n=b['n'], **{'D_' + a: b['D'][a] for a in SRC})
    doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    (OUTD / 'TU_v02.json').write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    print(json.dumps(dict(grid_identity=doc['grid_identity_vs_v12_A9_5']['identical'], of=doc['grid_identity_vs_v12_A9_5']['compared'],
                          lead_identity=doc['lead_keys_source_identity']['all_equal'], seconds=round(doc['seconds'])), default=float), flush=True)


if __name__ == '__main__':
    main()
