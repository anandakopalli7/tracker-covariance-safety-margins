"""Revision v13, package D1 (AMENDMENT_10_v13 sec. 6): D-H1 and D-H2 on the three non-braking lead variants (35 open-loop runs each).

Matched settings, from lead braking (the 35 old evaluation runs of record, all evaluated decisions, 3 s commitment, grid of record
GRID = [0] + logspace(-2, 3, 201)): c* = F0's caution at g = 1; every source's grid scale whose caution is nearest c* (ties: smaller g);
the phase schedule PS: its H4 triple at caution level c* (v12 triple_choice on the design set, tracker-estimated phase, threshold
-1.0 m/s^2: the triple with the lowest design wrong-go among triples whose design caution <= c*).
Per variant, at those settings against F0 at g = 1 (pooled over the variant's runs): the difference in caution (percentage points of the
desired speed, 100 * sum caution / sum count) and in wrong-go share (100 * sum wrong go / decisions), 3 s commitment, all evaluated
decisions, with 95% run-bootstrap percentile intervals (default_rng(20261911), 20,000).
  D-H1  CK3 (braking prediction); D-H2  PS (phase schedule on the online phase estimate of the D1 runs).
  Classification: 'costs progress' if the caution difference's lower end > 1 point and the wrong-go difference's upper end <= 0;
  'costs safety' if the wrong-go difference's lower end > 0; 'no measurable cost' if both intervals lie within +-1 point; else
  'inconclusive'. Every other source at its matched setting is reported in the same terms, descriptive. No pooling across variants.
Decisions used: evaluated decisions only (full 3 s truth windows); contact-truncated windows, where the extractor extrapolates the
lead, are not evaluated, so the D1 lead law never enters these values (review finding 1).
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\d_nonbraking_v13.py [--test-old] [--nboot N]
--test-old: the old evaluation runs stand in for each variant (code test only).
"""
import argparse, json, pathlib, sys, time
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cd_common_v13 as CC               # noqa: E402
import trk_env_v01 as env                # noqa: E402
env.setup()
import trk_score_v01 as TS               # noqa: E402
import c_lead_choice_v13 as CH           # noqa: E402  (v12 triple_choice / single_choice, verbatim)
L = CC.L; C11 = CC.C11

ap = argparse.ArgumentParser(); ap.add_argument('--test-old', action='store_true'); ap.add_argument('--nboot', type=int, default=CC.NBOOT)
args = ap.parse_args()
gate = CC.require_lock2(args.test_old)
t00 = time.time(); log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)
OUTF = CC.OUT / (('TESTOLD_' if args.test_old else '') + 'D_NONBRAKING_DH1_DH2_v13.json')
if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)
SRC = ['N', 'NA', 'A1', 'CK3', 'Q', 'TG']
GRID = C11.GRID
g1 = int(np.argmin(np.abs(GRID - 1.0))); assert abs(GRID[g1] - 1.0) < 1e-12

# ------------------------------------------------------------------------------------------------ matched settings (old runs)
design = CC.load_old_lead()
for r in design: r['masks_d'] = r['masks_est']
Xd = C11.tables(design, ('W1',), ['F0'] + SRC, masks_key='masks_d')            # (35, 202, 5, NST)
Td = {a: X.sum(axis=0) for a, X in Xd.items()}
rt = lambda T: (100. * T[..., 2] / T[..., 3], 100. * T[..., 1] / T[..., 0])     # caution, wrong go (optA_lib_v02.rates)
cstar = float(rt(Td['F0'][g1, 0])[0])
match = {}
for a in SRC:
    c = rt(Td[a][:, 0])[0]
    dist = np.where(np.isfinite(c), np.abs(c - cstar), np.inf)
    match[a] = int(np.flatnonzero(dist == dist.min())[0])                        # ties: smaller g (GRID ascending)
tri = CH.triple_choice([Td['F0'][:, pi] for pi in (2, 3, 4)], np.array([cstar]))[0]
doc = dict(code='d_nonbraking_v13.py', amendment='AMENDMENT_10_v13 sec. 6 D1', gate=gate, test_old=args.test_old,
           matched=dict(F0_g=float(GRID[g1]), caution_F0_g1_pp=cstar, scales={a: dict(index=match[a], g=float(GRID[match[a]]),
           design_caution_pp=float(rt(Td[a][match[a], 0])[0])) for a in SRC},
           PS_triple=dict(indices=[int(x) for x in tri], g=[float(GRID[x]) if x >= 0 else None for x in tri])),
           draw='default_rng(%d), %d run resamples per variant' % (CC.SEED_BOOT, args.nboot))
assert all(x >= 0 for x in tri), 'no PS triple qualifies at c*'
log('matched settings: c* = %.4f pp; %s; PS %s' % (cstar, {a: match[a] for a in SRC}, list(tri)))


def classify(dc, dw):
    if dc['ci'][0] > 1. and dw['ci'][1] <= 0.: return 'costs progress'
    if dw['ci'][0] > 0.: return 'costs safety'
    if -1. <= dc['ci'][0] and dc['ci'][1] <= 1. and -1. <= dw['ci'][0] and dw['ci'][1] <= 1.: return 'no measurable cost'
    return 'inconclusive'


# ------------------------------------------------------------------------------------------------ per variant
res = {}
for kind in ('constant', 'mild_braking', 'stop_and_go'):
    if args.test_old:
        runs = CC.load_old_lead()
        for r in runs: r['masks'] = r['masks_est']
    else:
        runs = CC.load_variant(CC.d1_run_ids(kind), 'CV0')
        assert all(r['meta'].get('lead_variant', {}).get('kind') == kind for r in runs)
    X = C11.tables(runs, ('W1',), ['F0'] + SRC)                                  # (nrun, 202, 5, NST); masks: ev, moving, est phases
    NR = len(runs); W = CC.counts(NR, args.nboot, CC.SEED_BOOT)
    per = {'F0': X['F0'][:, g1, 0, :]}
    for a in SRC: per[a] = X[a][:, match[a], 0, :]
    per['PS'] = sum(X['F0'][:, tri[q], pi, :] for q, pi in enumerate((2, 3, 4)))  # phases partition the evaluated decisions
    assert np.allclose(per['PS'][:, 0], per['F0'][:, 0])
    def diffs(Wr, a):
        TA = Wr @ per[a]; TF = Wr @ per['F0']
        cA, wA = rt(TA); cF, wF = rt(TF)
        return cA - cF, wA - wF
    ent = {}
    one = np.ones((1, NR))
    for a in SRC + ['PS']:
        dc0, dw0 = diffs(one, a); dcb, dwb = diffs(W, a)
        dc = L.summ(dcb, float(dc0[0])); dw = L.summ(dwb, float(dw0[0]))
        ent[a] = dict(caution_diff_pp=dc, wrong_go_diff_pp=dw, classification=classify(dc, dw),
                      caution_pp=float(rt(per[a].sum(axis=0))[0]), wrong_go_pp=float(rt(per[a].sum(axis=0))[1]))
    ent['F0'] = dict(caution_pp=float(rt(per['F0'].sum(axis=0))[0]), wrong_go_pp=float(rt(per['F0'].sum(axis=0))[1]),
                     decisions=float(per['F0'][:, 0].sum()))
    res[kind] = dict(runs=[r['run'] for r in runs], n_runs=NR, D_H1=ent['CK3']['classification'], D_H2=ent['PS']['classification'], sources=ent)
    log('%s: D-H1 %s, D-H2 %s' % (kind, res[kind]['D_H1'], res[kind]['D_H2']))
doc['variants'] = res
doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
doc['code_sha256'] = {f: CC.sha(CC.HERE / f) for f in ('d_nonbraking_v13.py', 'cd_common_v13.py', 'c_lead_choice_v13.py')}
CC.write_once(OUTF, doc)
log('written ' + OUTF.name)
