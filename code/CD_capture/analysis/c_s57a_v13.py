"""Revision v13, package C: A10 sec. 5.7 keys that c_lead_v13.py and c_cutin_v13.py do not compute ("S57A"). New file, 20 Nov 2026
(Claude Opus 5.5). Every definition: CD_capture\\CD_DEFINITIONS_S57A_v13.md (written before any fresh value). Scope of 20 Nov 02:40 EST
(coordinator): RS075, B6 terciles, delayed stop, stop reliance and TU.* moved to package B; the earlier version is kept as
analysis\\superseded_c_s57a_v13_before_scope_change.txt.

  1. decision-equivalents (.dec, .dec.ci) of the printed shares: LB.R, LB.RR_N / E5 / E5mP / CK3, LB.IMM.r / c, LB.PS.rec, CI.RR_N, CI.Y.R
  2. partial oracles PO25/50/75 (gridless; masks default_rng(20261919) per family) and <prefix>.grading_ok, LB.<pop> and CI (window)
  3. cut-in window shares CI.RR_CK3, CI.RR_E5, CI.RR_E5mP (E5 ranks over all evaluated cut-in decisions)
Fresh intervals: boot_counts(n, 20000, 20261911), nominal 95% percentile (descriptive: .cal "nominal95", .level 0.95).
Inputs (fresh): arrays/CV0, arrays/B1 (c_extract_v13.py), arrays/S57A (x_s57a_extract_v13.py, cut-in). Refuses unless
revision_v13/LOCK_A10_2.txt and LOCK_A10_2c.txt both exist (cd_common_v13.require_lock2c); opens no fresh file before that. --test-old: the 35 old evaluation runs (LB) and the 20 cut-in tuning runs (CI),
with the draws of record where a value of record is compared; writes out/TESTOLD_S57A_v13*.json and out/TEST_S57A_v13*.json.
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\c_s57a_v13.py [--test-old] [--nboot N] [--tag T]
"""
import argparse, csv, json, os, pathlib, re, sys, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('NUMBA_NUM_THREADS', '2')                       # shared laptop: at most 2 threads
import numpy as np
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cd_common_v13 as CC               # noqa: E402
import trk_env_v01 as env                # noqa: E402
env.setup()
import trk_score_v01 as TS               # noqa: E402
from c_lead_choice_v13 import single_choice, triple_choice   # noqa: E402  (v12 functions, verbatim)
L = CC.L; C11 = CC.C11; A9 = CC.A9

ap = argparse.ArgumentParser()
ap.add_argument('--test-old', action='store_true'); ap.add_argument('--nboot', type=int, default=CC.NBOOT)
ap.add_argument('--tag', default='')
args = ap.parse_args()
gate = CC.require_lock2c(args.test_old)  # stage-2 gate: LOCK_A10_2.txt AND LOCK_A10_2c.txt; nothing fresh is opened before it
TEST = args.test_old
t00 = time.time()
log = lambda s: print('[%6.0f s] %s' % (time.time() - t00, s), flush=True)   # noqa: E731
SUF = ('_' + args.tag) if args.tag else ''
OUTF = CC.OUT / (('TESTOLD_S57A_v13' if TEST else 'C_S57A_v13') + SUF + '.json')
TESTF = CC.OUT / ('TEST_S57A_v13' + SUF + '.json')
for f in ([OUTF, TESTF] if TEST else [OUTF]):
    if f.exists(): raise SystemExit('REFUSED: %s exists' % f)

P = pathlib.Path(r'<library folder>')
STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
M4 = P / '09_redesign' / 'm4_perception_model'
BRET = CC.WORK / 'B_retrack' / 'out'
OLDOUT = CC.OUT / 's57a_old'
NB = args.nboot
PS_ = [0.25, 0.5, 0.75]; PO = ['PO25', 'PO50', 'PO75']
POPS = ['all', 'mov', 'pre', 'brk', 'stop']
SEED_PO_RECORD = 20261118          # partial-oracle draw of record (rev_g_partial_oracle_draws_v01, a9_8)
SEED_BOOT_RECORD = 20261113        # bootstrap draw of record (old runs)

V = {}                             # A keys
DET = dict(gate=gate, nboot=NB, definitions='CD_DEFINITIONS_S57A_v13.md')
CHK = {}                           # old-run comparisons


def fin(x):
    return x is not None and np.isfinite(x)


def num(x):
    return float(x) if fin(x) else None


def ci95(b):
    b = np.asarray(b, float); f = np.isfinite(b)
    return [float(v) for v in np.percentile(b[f], [2.5, 97.5])] if f.any() else [None, None]


def put_ci(key, b, tgt=None, lv=None):
    """Interval key: nominal 95% ([2.5, 97.5], L.pct) by default; with lv = (level, cal) from the core output, the percentile interval
    at that level exactly as cd_common_v13.interval forms the share's own interval (a = 100 (1 - level) / 2)."""
    tgt = V if tgt is None else tgt
    if lv is None:
        tgt[key + '.ci'] = ci95(b); tgt[key + '.level'] = 0.95; tgt[key + '.cal'] = 'nominal95'
        return
    level, cal = lv[0], lv[1]
    x = np.asarray(b, float); f = np.isfinite(x); a = 100. * (1. - level) / 2.
    tgt[key + '.ci'] = [float(v) for v in np.percentile(x[f], [a, 100. - a])] if f.any() else [None, None]
    tgt[key + '.level'] = level; tgt[key + '.cal'] = cal


def rr_b(D, den):
    return C11.rat(D, den)


def ratio_b(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(np.isfinite(b) & (b > 0) & np.isfinite(a), a / b, np.nan)


def cmp(name, mine, ref, tol=0.):
    """Record a comparison with a value of record (exact unless tol > 0)."""
    def one_d(a, b):                       # None and NaN are 'undefined'; two undefined values agree
        a = np.nan if a is None else float(a); b = np.nan if b is None else float(b)
        if not np.isfinite(a) or not np.isfinite(b):
            return 0. if (np.isnan(a) and np.isnan(b)) or a == b else float('inf')
        return abs(a - b)
    if isinstance(mine, (list, tuple)):
        d = max(one_d(a, b) for a, b in zip(mine, ref)) if len(mine) == len(ref) else float('inf')
    else:
        d = one_d(mine, ref)
    CHK[name] = dict(mine=mine, record=ref, abs_diff=d, ok=bool(d <= tol))
    return d


def ref_file(name):
    """The existing first program's old-run output: analysis/out/<name>, else its last copy kept in out/old_tests/before_final2_20261120."""
    for f in (CC.OUT / name, CC.OUT / 'old_tests' / 'before_final2_20261120' / name):
        if f.is_file(): return f
    raise SystemExit('REFUSED: no old-run output %s to compare with' % name)


def cal_of(ent):
    """(level, cal) of one statistic's calibration entry of the core output (cd_common_v13.calibrated_levels)."""
    rule = str(ent.get('rule', '')); level = float(ent['level'])
    if 'PENDING' in rule or ent.get('pending'):
        return None
    if rule.startswith('calibrated'):
        return (level, 'calibrated')
    if abs(level - 0.99) < 1e-12:
        return (level, 'nominal99')
    if abs(level - 0.95) < 1e-12:
        return (level, 'nominal95')
    return None


# the .dec.ci of a calibrated statistic is at that statistic's own level (coordinator, 20 Nov; A's interface sec. 1)
LEVEL_SRC = {'LB.RR_N': ('lead', ('calibration_main', 'RR_N')), 'LB.RR_E5': ('lead', ('calibration_main', 'RR_E5')),
             'LB.RR_E5mP': ('lead', ('calibration_main', 'RR_E5_minus_E5p')), 'LB.RR_CK3': ('lead', ('calibration_main', 'RR_CK3')),
             'LB.IMM.r': ('lead', ('H3', 'calibration', 'r')), 'LB.IMM.c': ('lead', ('H3', 'calibration', 'c')),
             'LB.PS.rec': ('lead', ('H4', 'calibration', 'share_record')), 'CI.RR_N': ('cutin', ('K0', 'calibration', 'RR_N'))}


def core_levels():
    if TEST:
        files = dict(lead=ref_file('TESTOLD_C_LEAD_H0_H5_v13.json'), cutin=ref_file('TESTOLD_C_CUTIN_K0_K2_v13.json'))
    else:
        files = dict(lead=CC.OUT / 'C_LEAD_H0_H5_v13.json', cutin=CC.OUT / 'C_CUTIN_K0_K2_v13.json')
        for f in files.values():
            if not f.is_file():
                raise SystemExit('REFUSED: %s missing: run after the core import (c_lead_v13 / c_cutin_v13 --calib import)' % f.name)
    docs = {k: json.loads(f.read_text(encoding='utf-8')) for k, f in files.items()}
    out = {}; info = {k: dict(path=str(f), written=docs[k].get('written'), calib_mode=docs[k].get('calib_mode')) for k, f in files.items()}
    for key, (fam, path) in LEVEL_SRC.items():
        ent = docs[fam]
        for p in path:
            ent = ent.get(p) if isinstance(ent, dict) else None
        lv = cal_of(ent) if isinstance(ent, dict) and 'level' in ent else None
        if lv is None:
            if not TEST:
                raise SystemExit('REFUSED: no final calibrated level for %s in %s (%s)' % (key, files[fam].name, '.'.join(path)))
            out[key] = (0.95, 'nominal95'); info[key] = 'not in the old-run core output (%s); nominal95 in this test' % '.'.join(path)
        else:
            out[key] = lv; info[key] = dict(level=lv[0], cal=lv[1], source='%s: %s' % (files[fam].name, '.'.join(path)), rule=ent.get('rule'))
    return out, info


LV, DET['dec_ci_levels'] = core_levels()


def add_partial(runs, seed):
    """Partial oracles of record: one uniform per stored decision, runs in the given order, decisions in k order."""
    N = int(sum(len(r['k']) for r in runs))
    U = np.random.default_rng(seed).random(N); pos = 0
    for r in runs:
        n = len(r['k']); u = U[pos:pos + n]; pos += n
        for p, nm in zip(PS_, PO):
            r['crit'][nm] = np.where((u < p)[:, None], r['crit']['E'], r['crit']['F0'])
            r['sel'].pop(nm, None)
    return N


def grading(po):
    return bool(all(fin(x) for x in po) and po[0] > 0 and po[0] < po[1] < po[2])


NAMES_W1 = ['F0', 'E', 'N', 'E5', 'E5p', 'CK3'] + PO

# ================================================================================================ LEAD BRAKING
if TEST:
    runs = CC.load_old_lead()
    for r in runs: r['masks'] = r['masks_est']
    run_ids = [r['run'] for r in runs]
else:
    run_ids = CC.c_run_ids('lead_braking')
    runs = CC.load_variant(run_ids, 'CV0')
    assert all(r['meta'].get('family') == 'lead_braking' for r in runs)
for r in runs: r['n_dec'] = len(r['k'])
NR = len(runs)
log('lead runs %d (%s)' % (NR, 'TEST: old evaluation runs' if TEST else 'fresh'))
DET['LB.runs'] = run_ids

u, uinfo = TS.e5_u(runs, 'F0', 'E')
TS.add_oracle(runs, 'E5', 'F0', CC.RATIO, 0.05, u)
TS.add_oracle(runs, 'E5p', 'F0', CC.RATIO, 0.05, TS.permute_u(runs, u))
SEED_PO_LB = SEED_PO_RECORD if TEST else CC.SEED_PARTIAL
N_PO_LB = add_partial(runs, SEED_PO_LB)
DET['LB.partial_oracle_draw'] = dict(seed=SEED_PO_LB, n_uniforms=N_PO_LB)
if TEST: assert N_PO_LB == 9307
SEED_W = SEED_BOOT_RECORD if TEST else CC.SEED_BOOT
W = CC.counts(NR, NB, SEED_W)
DET['LB.draw'] = 'boot_counts(%d, %d, %d)' % (NR, NB, SEED_W)

# ------------------------------------------------------------------------------------------------ W1 sources: .dec and partial oracles
G = TS.gridless(runs, NAMES_W1)
log('W1 gridless events built')
PT = {pi: TS.rr_gl(G, 'F0', 'E', NAMES_W1[2:], pop=pi) for pi in range(5)}
P1 = CC.prep(G, ['F0', 'E', 'N', 'E5', 'E5p', 'CK3'], 0)
chk = CC.evaluate(P1, np.ones((1, NR)))
assert chk['denE'][0] == PT[0]['denE'] and all(chk['D'][a][0] == PT[0]['D'][a] for a in ('N', 'E5', 'E5p', 'CK3')), 'gl_fast differs'
B1 = CC.evaluate(P1, W)
log('W1 resamples done (%d)' % W.shape[0])
p0 = PT[0]; n0 = p0['n']
V['LB.R.dec'] = float(p0['R_deceq'])
DET['LB.R'] = dict(R_pp=p0['R_pp'], n=n0, R_pp_ci=ci95(B1['denE'] / L.NLEV), R_dec_ci=ci95(L.dec_eq(B1['denE'], B1['n'])))
for a, key in (('N', 'LB.RR_N'), ('E5', 'LB.RR_E5'), ('CK3', 'LB.RR_CK3')):
    V[key + '.dec'] = float(p0['D_deceq'][a]); put_ci(key + '.dec', L.dec_eq(B1['D'][a], B1['n']), lv=LV[key])
    DET[key] = dict(point=p0['RR'][a], ci=ci95(rr_b(B1['D'][a], B1['denE'])))
V['LB.RR_E5mP.dec'] = float(L.dec_eq(p0['D']['E5'] - p0['D']['E5p'], n0))
put_ci('LB.RR_E5mP.dec', L.dec_eq(B1['D']['E5'] - B1['D']['E5p'], B1['n']), lv=LV['LB.RR_E5mP'])
DET['LB.RR_E5mP'] = dict(point=p0['RR']['E5'] - p0['RR']['E5p'],
                         ci=ci95(rr_b(B1['D']['E5'], B1['denE']) - rr_b(B1['D']['E5p'], B1['denE'])))
for pi, pop in enumerate(POPS):
    po = [PT[pi]['RR'][nm] for nm in PO]
    for nm, x in zip(PO, po): V['LB.%s.%s' % (pop, nm)] = num(x)
    V['LB.%s.grading_ok' % pop] = grading(po)
    DET['LB.%s' % pop] = dict(n=PT[pi]['n'], R_pp=PT[pi]['R_pp'], R_deceq=PT[pi]['R_deceq'],
                              PO_D_deceq={nm: PT[pi]['D_deceq'][nm] for nm in PO})
for nm in PO: V['LB.' + nm] = V['LB.all.' + nm]
V['LB.grading_ok'] = V['LB.all.grading_ok']
DET['LB.e5_u'] = uinfo
log('LB .dec and partial oracles (gridless) done')

# grid version of the partial oracles (details); test: the values of record (truth phase, draw 20261118)
Xg = C11.tables(runs, ('W1',), ['F0', 'E'] + PO)
pg = C11.points(Xg, ['E'] + PO, pops=range(5))
DET['LB.grid_PO'] = {pop: [L.ratio(pg[pi]['D'][nm], pg[pi]['denE']) for nm in PO] for pi, pop in enumerate(POPS)}
if TEST:
    REVG = json.loads(pathlib.Path(r'ARS_TRIAL\revision_v11\analysis\out\REV_G_PARTIAL_DRAWS_v01.json').read_text(encoding='utf-8'))
    A98 = json.loads((CC.V12A / 'out' / 'A9_8_GRADING_BEFORE_STOP_v01.json').read_text(encoding='utf-8'))
    for r in runs:
        r['masks_truth'] = C11.masks_of(r['ev'], r['v0'], r['ph']) + (r['ev'] & (r['ph'] <= 1),)
    Xt = C11.tables(runs, ('W1',), ['F0', 'E'] + PO, masks_key='masks_truth')
    pt_ = C11.points(Xt, ['E'] + PO, pops=range(7))
    for pi, pop in enumerate(['all', 'moving', 'phase0', 'phase1', 'phase2']):
        cmp('PO grid truth-phase %s (rev_g of record, draw 20261118)' % pop, [L.ratio(pt_[pi]['D'][nm], pt_[pi]['denE']) for nm in PO],
            [REVG['pops'][pop]['P%s' % nm[2:]]['of_record'] for nm in PO])
    gb = [L.ratio(pt_[6]['D'][nm], pt_[6]['denE']) for nm in PO]
    cmp('PO grid before stop (A9-8 of record)', gb, [A98['of_record']['P%s' % nm[2:]] for nm in PO])
    cmp('grading rule before stop = A9-8 grades_by_rule', float(grading(gb)), float(A98['grades_by_rule']))
    DET['LB.grid_PO_truth_phase_of_record'] = {pop: [L.ratio(pt_[pi]['D'][nm], pt_[pi]['denE']) for nm in PO]
                                               for pi, pop in enumerate(['all', 'moving', 'phase0', 'phase1', 'phase2', 'phase3', 'before_stop'])}
log('grid partial oracles done')

# ------------------------------------------------------------------------------------------------ IMM (.dec)
if TEST:
    ri = []
    for rid in run_ids:
        z = np.load(BRET / 'retrack' / 'B1' / (rid + '_arrays.npz'), allow_pickle=False)
        ev = z['evaluated'].astype(bool)
        ri.append(dict(run=rid, desired=float(z['des'][0]), idx55=z['idx55'].astype(np.int64), clear1=L.clean_clear(z['clear']),
                       vbar=z['vbar'], ev=ev, masks=(ev,), crit={'F0': z['cF0'], 'E': z['cE'], 'N': z['cN']}, sel={}, late={}, k=z['k']))
else:
    ri = CC.load_variant(run_ids, 'B1')
rs = TS.ratio_summary(TS.margin_ratios(ri, 'N', 'F0'))
ui, uii = TS.e5_u(ri, 'F0', 'E')
TS.add_oracle(ri, 'E5x', 'F0', rs['median'], rs['A'], ui)
Gi = TS.gridless(ri, ['F0', 'E', 'N', 'E5x'])
pti = TS.rr_gl(Gi, 'F0', 'E', ['N', 'E5x'], pop=0)
Pi = CC.prep(Gi, ['F0', 'E', 'N', 'E5x'], 0)
assert CC.evaluate(Pi, np.ones((1, NR)))['D']['N'][0] == pti['D']['N']
Bi = CC.evaluate(Pi, W)
V['LB.IMM.r.dec'] = float(pti['D_deceq']['N']); put_ci('LB.IMM.r.dec', L.dec_eq(Bi['D']['N'], Bi['n']), lv=LV['LB.IMM.r'])
V['LB.IMM.c.dec'] = float(pti['D_deceq']['E5x']); put_ci('LB.IMM.c.dec', L.dec_eq(Bi['D']['E5x'], Bi['n']), lv=LV['LB.IMM.c'])
DET['LB.IMM'] = dict(r=pti['RR']['N'], c=pti['RR']['E5x'], R_pp=pti['R_pp'], R_deceq=pti['R_deceq'], ratio=rs, e5_u=uii,
                     r_ci=ci95(rr_b(Bi['D']['N'], Bi['denE'])), c_ci=ci95(rr_b(Bi['D']['E5x'], Bi['denE'])))
if TEST:
    BB1 = json.loads((BRET / 'banalysis' / 'B_B1_v01.json').read_text(encoding='utf-8'))['points']['all']
    cmp('IMM r (B_B1_v01 all)', pti['RR']['N'], BB1['RR']['N'], 1e-12)
    cmp('IMM c (B_B1_v01 all, E5x)', pti['RR']['E5x'], BB1['RR']['E5x'], 1e-12)
    cmp('LB.IMM.r.dec (B_B1_v01 D_deceq N)', pti['D_deceq']['N'], BB1['D_deceq']['N'], 1e-12)
    cmp('LB.IMM.c.dec (B_B1_v01 D_deceq E5x)', pti['D_deceq']['E5x'], BB1['D_deceq']['E5x'], 1e-12)
    cmp('IMM room R_deceq (B_B1_v01)', pti['R_deceq'], BB1['R_deceq'], 1e-12)
log('IMM done')

# ------------------------------------------------------------------------------------------------ H4 numerator (.dec), c_lead_v13 design
PHPOP = [2, 3, 4]


def phase_tables(rs_, masks_fn):
    for r in rs_: r['masks_h4'] = masks_fn(r)
    X = C11.tables(rs_, ('W1',), ['F0', 'E'], masks_key='masks_h4')
    return X['F0'], X['E']


def est_masks(thr):
    def f(r):
        eph = TS.est_phase(r['lead']['vhat'], r['lead']['ahat_long'], r['lead']['lead_found'], thr) if 'lead' in r else \
            TS.est_phase(r['z']['vhat'], r['z']['ahat_long'], r['z']['lead_found'], thr)
        return CC.masks_tracker_phase(r['ev'], r['v0'], eph)
    return f


def h4_parts(st, w):
    """cd_common_v13.H4Stat.share (same lines), returning the sums: num_rec = sum(F_F0 - F_ps), num_like = sum(F_1 - F_ps),
    den = sum(F_F0 - F_E), and n (decisions)."""
    fF0, fE, tri, one = st.fF0, st.fE, st.tri, st.one
    Ta = np.tensordot(w, fF0[:, :, 0, :], axes=(0, 0)); TE = np.tensordot(w, fE[:, :, 0, :], axes=(0, 0))
    c = L.curves_w({'F0': Ta, 'E': TE}, 0); cF0, wF0 = c['F0']; cE, wE = c['E']
    lev_ = L.levels_of(cF0, cE, cF0[0])
    f0 = L.frontier(cF0, wF0, lev_); fe = L.frontier(cE, wE, lev_)
    Tph = [np.tensordot(w, fF0[:, :, pi, :], axes=(0, 0)) for pi in (2, 3, 4)]
    nl = tri.shape[0]; Wv = np.zeros(nl); Sv = np.zeros(nl); Kv = np.zeros(nl)
    for q in range(3):
        g = tri[:, q]; okg = g >= 0
        Wv[okg] += Tph[q][g[okg], 1]; Sv[okg] += Tph[q][g[okg], 2]; Kv[okg] += Tph[q][g[okg], 3]
    n = float(Ta[0, 0])
    with np.errstate(divide='ignore', invalid='ignore'):
        cp = np.where(tri[:, 0] >= 0, 100. * Sv / Kv, np.nan); wp = np.where(tri[:, 0] >= 0, 100. * Wv / n, np.nan)
        ok1 = one >= 0; g1 = np.clip(one, 0, None)
        c1 = np.where(ok1, 100. * Ta[g1, 2] / Ta[g1, 3], np.nan); w1 = np.where(ok1, 100. * Ta[g1, 1] / n, np.nan)
    fps = L.frontier(np.concatenate([[cF0[0]], cp]), np.concatenate([[wF0[0]], wp]), lev_)
    f1 = L.frontier(np.concatenate([[cF0[0]], c1]), np.concatenate([[wF0[0]], w1]), lev_)
    return float(np.sum(f0 - fps)), float(np.sum(f1 - fps)), float(np.sum(f0 - fe)), n


design = CC.load_old_lead()
mfn = est_masks(-1.0)
dF0, dE = phase_tables(design, mfn)
wd = np.ones(len(design))
Tall = np.tensordot(wd, dF0[:, :, 0, :], axes=(0, 0)); TEd = np.tensordot(wd, dE[:, :, 0, :], axes=(0, 0))
cur = L.curves_w({'F0': Tall, 'E': TEd}, 0)
levd = L.levels_of(cur['F0'][0], cur['E'][0], cur['F0'][0][0])
tri = triple_choice([np.tensordot(wd, dF0[:, :, pi, :], axes=(0, 0)) for pi in PHPOP], levd)
one = single_choice(Tall, levd)
fF0, fE = phase_tables(runs, mfn)
st4 = CC.H4Stat(fF0, fE, tri, one)
nr, nl_, dn, nn = h4_parts(st4, np.ones(NR))
sh_full = st4.share(np.ones(NR))
assert nr / dn == sh_full[0] and nl_ / dn == sh_full[1]
H4B = np.array([h4_parts(st4, W[b]) for b in range(W.shape[0])])          # (B, 4): num_rec, num_like, den, n
for b in range(min(50, W.shape[0])):
    sb = st4.share(W[b])
    assert (H4B[b, 0] / H4B[b, 2] == sb[0]) or not (H4B[b, 2] > 0)
V['LB.PS.rec.dec'] = float(L.dec_eq(nr, nn)); put_ci('LB.PS.rec.dec', L.dec_eq(H4B[:, 0], H4B[:, 3]), lv=LV['LB.PS.rec'])
DET['LB.PS.rec'] = dict(point=sh_full[0], like=sh_full[1], ci=ci95(ratio_b(H4B[:, 0], H4B[:, 2])), num_rec_sum=nr, den_sum=dn, n=nn,
                        grid_room_dec=float(L.dec_eq(dn, nn)))
log('H4 numerator done')

if TEST:     # consistency with the existing first program's old-run output (its draw: boot_counts(35, 200, 20261911))
    TLf = ref_file('TESTOLD_C_LEAD_H0_H5_v13.json'); TL = json.loads(TLf.read_text(encoding='utf-8'))
    nbx = int(re.match(r'default_rng\(20261911\), (\d+) run resamples', TL['draw']).group(1))
    DET['reference_c_lead'] = dict(path=str(TLf), draw=TL['draw'], written=TL.get('written'))
    Bx = CC.evaluate(P1, CC.counts(NR, nbx, CC.SEED_BOOT))
    cmp('LB.R.dec = c_lead room R_deceq', V['LB.R.dec'], TL['room']['R_deceq'])
    cmp('LB.R.dec ci (c_lead draw 20261911) = c_lead R_deceq_ci', L.pct(L.dec_eq(Bx['denE'], Bx['n'])), TL['room']['R_deceq_ci'])
    for a in ('N', 'E5', 'E5p', 'CK3'):
        cmp('D_deceq %s point = c_lead descriptive_D_deceq' % a, float(PT[0]['D_deceq'][a]), TL['descriptive_D_deceq'][a]['point'])
        cmp('D_deceq %s ci (c_lead draw 20261911) = c_lead' % a, L.pct(L.dec_eq(Bx['D'][a], Bx['n'])), TL['descriptive_D_deceq'][a]['ci'])
    cmp('LB.RR_E5mP.dec = D_deceq(E5) - D_deceq(E5p) of c_lead', V['LB.RR_E5mP.dec'],
        TL['descriptive_D_deceq']['E5']['point'] - TL['descriptive_D_deceq']['E5p']['point'], 1e-9)
    cmp('RR_E5 - RR_E5p point = c_lead main RR_E5_minus_E5p', DET['LB.RR_E5mP']['point'], TL['main']['RR_E5_minus_E5p']['point'])
    for a, nm in (('N', 'RR_N'), ('E5', 'RR_E5'), ('CK3', 'RR_CK3')):
        cmp('share %s point = c_lead main' % a, PT[0]['RR'][a], TL['main'][nm]['point'])
        cmp('share %s = LB.%s.dec / LB.R.dec' % (a, nm), PT[0]['RR'][a], V['LB.%s.dec' % nm] / V['LB.R.dec'], 1e-12)
        cmp('share %s ci (c_lead draw 20261911) = c_lead main ci (nominal)' % a, L.pct(rr_b(Bx['D'][a], Bx['denE'])), TL['main'][nm]['ci'])
        tmp = {}; put_ci('x', rr_b(Bx['D'][a], Bx['denE']), tmp, lv=LV['LB.' + nm])     # the level formula = cd_common_v13.interval
        cmp('share %s ci at its core level %.4f = c_lead main ci_level' % (a, LV['LB.' + nm][0]), tmp['x.ci'], TL['main'][nm]['ci_level'])
    tmp = {}; put_ci('x', rr_b(Bx['D']['E5'], Bx['denE']) - rr_b(Bx['D']['E5p'], Bx['denE']), tmp, lv=LV['LB.RR_E5mP'])
    cmp('share E5 - E5p ci at its core level = c_lead main ci_level', tmp['x.ci'], TL['main']['RR_E5_minus_E5p']['ci_level'])
    cmp('LB.PS.rec share = c_lead H4 record basis', DET['LB.PS.rec']['point'], TL['H4']['record_basis']['point'])
    cmp('LB.PS.rec like-for-like = c_lead H4 like_for_like', DET['LB.PS.rec']['like'], TL['H4']['like_for_like']['point'])
    cmp('LB.PS.rec.dec / grid room dec = share', V['LB.PS.rec.dec'] / DET['LB.PS.rec']['grid_room_dec'], DET['LB.PS.rec']['point'], 1e-12)
    log('consistency with TESTOLD_C_LEAD done')

# ================================================================================================ CUT-IN
if TEST:
    rows = [r for r in csv.DictReader(open(M4 / 'run_index_m4_v02.csv', encoding='utf-8'))
            if r['use'] == '1' and r['set'] == 'tune' and r['family'] == 'cutin']
    ci_ids = sorted(r['archive'] for r in rows); assert len(ci_ids) == 20
else:
    ci_ids = CC.c_run_ids('cutin')
cruns = []
for rid in ci_ids:
    if TEST:
        z = np.load(STORED / (rid + '.npz'), allow_pickle=False)
        b = np.load(BRET / 'retrack' / 'CV0' / (rid + '_arrays.npz'), allow_pickle=False)
        assert np.array_equal(b['k'], z['k'])
        for kk in ('cF0', 'cE', 'cN'):
            assert np.array_equal(np.isfinite(b[kk]), np.isfinite(z[kk])) and \
                np.nanmax(np.abs(np.where(np.isfinite(z[kk]), (b[kk] - z[kk]) / np.maximum(1., np.abs(z[kk])), 0.))) <= 1e-12, (rid, kk)
        ck3 = b['cCK3']
        s = np.load(OLDOUT / 'x' / (rid + '.npz'), allow_pickle=False)
    else:
        z = np.load(CC.ARR / 'CV0' / (rid + '.npz'), allow_pickle=False)
        assert json.loads(str(z['meta']))['family'] == 'cutin', rid
        ck3 = z['cCK3']
        s = np.load(CC.ARR / 'S57A' / (rid + '.npz'), allow_pickle=False)
    assert np.array_equal(s['k'], z['k']), rid
    ev = z['evaluated'].astype(bool); rel_ = s['rel']; strat = s['stratum']
    win = ev & np.isfinite(rel_) & (rel_ >= -1.0) & (rel_ <= 4.0)
    cruns.append(dict(run=rid, desired=float(z['des'][0]), idx55=z['idx55'].astype(np.int64), clear1=L.clean_clear(z['clear']),
                      vbar=z['vbar'], ev=ev, sel={}, late={}, k=z['k'], n_dec=len(z['k']),
                      masks=(win, win & (strat == '<1s'), ev),
                      crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float),
                            'CK3': np.asarray(ck3, float)},
                      kc=int(s['kc']), n_window=int(win.sum()), n_young=int((win & (strat == '<1s')).sum())))
NC = len(cruns)


def cut_block(cr, seed_po, seed_w, lv_rrn):
    """Sec. 3-5 cut-in keys on run dicts cr (masks: window, young, all evaluated). Returns (values, details, rr_gl window point)."""
    out = {}; det = {}
    u_, uinf = TS.e5_u(cr, 'F0', 'E')
    TS.add_oracle(cr, 'E5', 'F0', CC.RATIO, 0.05, u_)
    TS.add_oracle(cr, 'E5p', 'F0', CC.RATIO, 0.05, TS.permute_u(cr, u_))
    npo = add_partial(cr, seed_po)
    g = TS.gridless(cr, NAMES_W1)
    pw = TS.rr_gl(g, 'F0', 'E', NAMES_W1[2:], pop=0)
    py = TS.rr_gl(g, 'F0', 'E', ['N'], pop=1)
    Wx = CC.counts(len(cr), NB, seed_w)
    Px = CC.prep(g, ['F0', 'E', 'N', 'E5', 'E5p', 'CK3'], 0)
    ch = CC.evaluate(Px, np.ones((1, len(cr))))
    assert ch['denE'][0] == pw['denE'] and all(ch['D'][a][0] == pw['D'][a] for a in ('N', 'E5', 'E5p', 'CK3')), 'gl_fast differs'
    Bx_ = CC.evaluate(Px, Wx)
    for a, key in (('CK3', 'CI.RR_CK3'), ('E5', 'CI.RR_E5')):
        out[key] = num(pw['RR'][a]); put_ci(key, rr_b(Bx_['D'][a], Bx_['denE']), out)
    out['CI.RR_E5mP'] = num(pw['RR']['E5'] - pw['RR']['E5p']) if fin(pw['RR']['E5']) and fin(pw['RR']['E5p']) else None
    put_ci('CI.RR_E5mP', rr_b(Bx_['D']['E5'], Bx_['denE']) - rr_b(Bx_['D']['E5p'], Bx_['denE']), out)
    out['CI.RR_N.dec'] = float(pw['D_deceq']['N']); put_ci('CI.RR_N.dec', L.dec_eq(Bx_['D']['N'], Bx_['n']), out, lv=lv_rrn)
    out['CI.Y.R.dec'] = float(py['R_deceq']) if fin(py['R_deceq']) else 0.        # empty young-track population: no room
    po_ = [pw['RR'][nm] for nm in PO]
    for nm, x in zip(PO, po_): out['CI.' + nm] = num(x)
    out['CI.grading_ok'] = grading(po_)
    det['CI.partial_oracle_draw'] = dict(seed=seed_po, n_uniforms=npo)
    det['CI.e5_u'] = uinf
    det['CI.draw'] = 'boot_counts(%d, %d, %d)' % (len(cr), NB, seed_w)
    det['CI.window'] = dict(n=pw['n'], R_pp=pw['R_pp'], R_deceq=pw['R_deceq'], RR={a: pw['RR'][a] for a in NAMES_W1[2:]},
                            D_deceq={a: pw['D_deceq'][a] for a in NAMES_W1[2:]}, R_pp_ci=ci95(Bx_['denE'] / L.NLEV),
                            RR_N_ci=ci95(rr_b(Bx_['D']['N'], Bx_['denE'])))
    det['CI.young'] = dict(n=py['n'], R_pp=py['R_pp'], R_deceq=py['R_deceq'])
    return out, det, pw, py


Vc, Dc, ptc, pty = cut_block(cruns, CC.SEED_PARTIAL, SEED_BOOT_RECORD if TEST else CC.SEED_BOOT, LV['CI.RR_N'])
V.update(Vc); DET.update(Dc)
ucinfo = Dc['CI.e5_u']
DET['CI.runs'] = [dict(run=r['run'], event_tick=(None if r['kc'] < 0 else r['kc']), n_window=r['n_window'], n_young=r['n_young']) for r in cruns]
if TEST:
    TCf = ref_file('TESTOLD_C_CUTIN_K0_K2_v13.json'); TC = json.loads(TCf.read_text(encoding='utf-8'))
    DET['reference_c_cutin'] = dict(path=str(TCf), draw=TC['draw'], written=TC.get('written'))
    cmp('cut-in event ticks (20 runs) = c_cutin', float(all(f['event_tick'] == r['event_tick'] for f, r in zip(TC['runs'], DET['CI.runs']))), 1.)
    cmp('cut-in window sizes (20 runs) = c_cutin', float(all(f['n_window'] == r['n_window'] for f, r in zip(TC['runs'], DET['CI.runs']))), 1.)
    cmp('cut-in young sizes (20 runs) = c_cutin window_strata <1s',
        float(all(f['window_strata']['<1s'] == r['n_young'] for f, r in zip(TC['runs'], DET['CI.runs']))), 1.)
    cmp('cut-in window room R_deceq = c_cutin descriptive.window', ptc['R_deceq'], TC['descriptive']['window']['R_deceq']['point'])
    cmp('cut-in window n = c_cutin descriptive.window', ptc['n'], TC['descriptive']['window']['n'])
    cmp('cut-in window RR_N point = c_cutin K1', ptc['RR']['N'], TC['K1']['RR_N']['point'])
    cmp('CI young R_deceq = c_cutin descriptive.young (NaN: no young-track decision)', num(pty['R_deceq']),
        TC['descriptive']['young']['R_deceq']['point'])
    cmp('cut-in e5_u n_evaluated = c_cutin', ucinfo['n_evaluated'], TC['e5_u']['n_evaluated'])
    log('consistency with TESTOLD_C_CUTIN done')
log('cut-in done (%d runs)' % NC)

if TEST:     # the cut-in code path on data with room: the 35 old lead runs with window = all evaluated must give the LB values
    lr = [dict(run=r['run'], desired=r['desired'], idx55=r['idx55'], clear1=r['clear1'], vbar=r['vbar'], ev=r['ev'], sel={}, late={},
               k=r['k'], n_dec=r['n_dec'], masks=(r['ev'], np.zeros_like(r['ev']), r['ev']),
               crit={a: r['crit'][a] for a in ('F0', 'E', 'N', 'CK3')}) for r in runs]
    Vs, Ds, _, _ = cut_block(lr, SEED_PO_LB, SEED_W, LV['LB.RR_N'])          # same level as LB.RR_N.dec
    for k_ci, k_lb in (('CI.RR_E5', 'LB.RR_E5'), ('CI.RR_CK3', 'LB.RR_CK3')):
        cmp('CI path on LB runs: %s point = %s' % (k_ci, k_lb), Vs[k_ci], DET[k_lb]['point'])
        cmp('CI path on LB runs: %s ci = %s' % (k_ci, k_lb), Vs[k_ci + '.ci'], DET[k_lb]['ci'])
    cmp('CI path on LB runs: CI.RR_E5mP point = LB', Vs['CI.RR_E5mP'], DET['LB.RR_E5mP']['point'])
    cmp('CI path on LB runs: CI.RR_E5mP ci = LB', Vs['CI.RR_E5mP.ci'], DET['LB.RR_E5mP']['ci'])
    cmp('CI path on LB runs: CI.RR_N.dec = LB.RR_N.dec', Vs['CI.RR_N.dec'], V['LB.RR_N.dec'])
    cmp('CI path on LB runs: CI.RR_N.dec.ci = LB.RR_N.dec.ci', Vs['CI.RR_N.dec.ci'], V['LB.RR_N.dec.ci'])
    for nm in PO:
        cmp('CI path on LB runs: CI.%s = LB.all.%s' % (nm, nm), Vs['CI.' + nm], V['LB.all.' + nm])
    cmp('CI path on LB runs: grading_ok', float(Vs['CI.grading_ok']), float(V['LB.all.grading_ok']))
    DET['CI_path_on_old_lead_runs'] = Vs
    log('cut-in code path checked on the old lead runs')

# ================================================================================================ write
DET['seconds'] = time.time() - t00; DET['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
DET['code_sha256'] = {f: CC.sha(CC.HERE / f) for f in ('c_s57a_v13.py', 'x_s57a_extract_v13.py', 'cd_common_v13.py', 'gl_fast_v13.py',
                                                       'c_lead_choice_v13.py')}
DET['moved_to_package_B'] = ['LB.RS075.rel', 'LB.T*', 'LB.DS.*', 'LB.REL_*', 'TU.*']
doc = dict(family='C_S57A', program='c_s57a_v13.py', test_old=TEST, values=V, details=DET)
if TEST: doc['checks'] = CHK


def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.bool_, bool)): return bool(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (float, np.floating)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o


CC.write_once(OUTF, clean(doc))
if TEST:
    bad = {k: v for k, v in CHK.items() if not v.get('ok', False)}
    CC.write_once(TESTF, clean(dict(family='C_S57A', program='c_s57a_v13.py', test_old=True, written=DET['written'], nboot=NB,
                                    n_checks=len(CHK), n_ok=len(CHK) - len(bad), failed=bad, seconds=DET['seconds'])))
log('written %s (%d keys)%s' % (OUTF.name, len(V), '; checks %d, failed %d' % (len(CHK), sum(not v.get('ok') for v in CHK.values())) if TEST else ''))
