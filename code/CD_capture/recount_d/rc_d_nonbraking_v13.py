"""Recount (second program) of D1 / D-H1 / D-H2 (AMENDMENT_10_v13.md sec. 6; CD_DEFINITIONS_v13.md "D1"). Claude Fable 5.2.
Written from the amendment and the definitions, without reading the first programs.

  1. Matched settings on the 35 old evaluation runs (all evaluated decisions, 3 s commitment):
     c* = F0's pooled caution at g = 1; each source (N, NA, AM = A1, CK3, Q, TG): the grid index whose pooled caution is nearest
     c* (ties: smaller g); PS: the per-phase triple of F0 scales (tracker phase, threshold -1.0) with the lowest pooled wrong go
     among triples whose pooled caution is <= c* (ties: lowest caution, then lowest flat index over the unique per-phase
     (wrong go, caution sum, caution count) tuples; each tuple stands for its smallest grid index).
  2. Per D1 variant (35 runs): pooled caution and wrong go of every source at its matched setting and of F0 at g = 1; the
     differences source - F0 with 20,000-resample run-bootstrap 95% percentile intervals (boot_counts(n, 20000, 20261911), the
     same draw for every variant); the D-H1 (CK3) and D-H2 (PS) classifications (computed for every source, for information).

Usage (python -I -B -X utf8):
  rc_d_nonbraking_v13.py --test-old [--tag T]     old runs stand in for each variant (no fresh file is touched)
  rc_d_nonbraking_v13.py [--tag T]                after Lock 2 (refuses unless LOCK_A10_2.txt exists)
Output: out\\RC_D_NONBRAKING_v13[_TESTOLD][_T].json (never overwritten).
"""
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))      # python -I drops the script folder
import numpy as np
import rc_d_common_v13 as K

L = K.L; GRID = K.GRID
SOURCES = ['N', 'NA', 'AM', 'CK3', 'Q', 'TG']          # grid sources; PS is added
ALL = SOURCES + ['PS']
HYP = {'D-H1': 'CK3', 'D-H2': 'PS'}


# ------------------------------------------------------------------------------------------------ matched settings
def pooled(T):
    """(.., NST) summed statistics -> (wrong go %, caution %)."""
    with np.errstate(divide='ignore', invalid='ignore'):
        return 100. * T[..., 1] / T[..., 0], 100. * T[..., 2] / T[..., 3]


def unique_rows(T):
    """Unique (wrong go, caution sum, caution count) rows of a (G, NST) table in lexicographic order, with the smallest grid
    index of each."""
    A = T[:, 1:4]
    o = np.lexsort((np.arange(A.shape[0]), A[:, 2], A[:, 1], A[:, 0]))
    As = A[o]
    first = np.concatenate([[True], np.any(As[1:] != As[:-1], axis=1)])
    return As[first], o[first]


def triple_at(Tph, level):
    """Tph: three (G, NST) tables (phases 0, 1, 2). The triple of grid indices with the lowest pooled wrong go among triples with
    pooled caution <= level; ties: lowest caution, then lowest flat index (C order over the unique tuples). None if no triple."""
    U = []; IX = []
    for T in Tph:
        u, ix = unique_rows(T); U.append(u); IX.append(ix)
    n = float(Tph[0][0, 0] + Tph[1][0, 0] + Tph[2][0, 0])

    def comb(col):
        return (U[0][:, col][:, None, None] + U[1][:, col][None, :, None] + U[2][:, col][None, None, :]).ravel()
    W = comb(0); S = comb(1); Kc = comb(2)
    with np.errstate(divide='ignore', invalid='ignore'):
        c = 100. * S / Kc; w = 100. * W / n
    ok = np.isfinite(c) & np.isfinite(w) & (c <= level)
    if not ok.any():
        return None
    cand = np.nonzero(ok)[0]
    cand = cand[w[cand] == w[cand].min()]
    n_tie_w = int(cand.size)
    cand = cand[c[cand] == c[cand].min()]
    flat = int(cand.min())
    i = np.unravel_index(flat, (U[0].shape[0], U[1].shape[0], U[2].shape[0]))
    idx = [int(IX[q][i[q]]) for q in range(3)]
    # how many grid indices share each chosen tuple (they are indistinguishable on the design set)
    same = [int(np.sum(np.all(Tph[q][:, 1:4] == U[q][i[q]], axis=1))) for q in range(3)]
    return dict(idx=idx, g=[float(GRID[j]) for j in idx], design_wrong_go=float(w[flat]), design_caution=float(c[flat]),
                n_triples=int(c.size), n_tied_on_wrong_go=n_tie_w, n_tied_on_wrong_go_and_caution=int(cand.size),
                n_grid_indices_sharing_each_tuple=same, n_unique=[int(u.shape[0]) for u in U])


def matched_settings(old):
    per = {s: [] for s in ['F0'] + SOURCES}
    ph_tabs = [[], [], []]; conf = np.zeros(3, int)
    for r in old:
        safe = r['clear1'] > 0.
        for s in per:
            sel = K.grid_sel(r, s)
            per[s].append(K.run_table(r, sel, safe))
            if s == 'F0':
                ph = K.est_phase(r['vhat'], r['ahat_long'], r['lead_found'], -1.0)
                for q in range(3):
                    m = r['ev'] & (ph == q); conf[q] += int(m.sum())
                    ph_tabs[q].append(L.stats_scored(sel, r['clear1'], safe, r['vbar'], r['des'], (m,))[:, 0, :])
    T = {s: np.stack(v).sum(axis=0) for s, v in per.items()}                 # (202, NST), runs added in run order
    w0, c0 = pooled(T['F0'])
    cstar = float(c0[K.I_G1])
    ms = {'c_star': cstar, 'F0_g1': dict(idx=K.I_G1, g=1.0, design_caution=cstar, design_wrong_go=float(w0[K.I_G1]),
                                         n=float(T['F0'][K.I_G1, 0])), 'sources': {}}
    for s in SOURCES:
        w, c = pooled(T[s])
        d = np.abs(c - cstar)
        j = int(np.nanargmin(d))                                              # first minimum = smaller g on ties
        ms['sources'][s] = dict(idx=j, g=float(GRID[j]), design_caution=float(c[j]), design_wrong_go=float(w[j]),
                                abs_gap=float(d[j]), n_tied=int(np.sum(d == d[j])))
    Tph = [np.stack(v).sum(axis=0) for v in ph_tabs]
    tri = triple_at(Tph, cstar)
    if tri is None:
        raise RuntimeError('REFUSED: no per-phase triple has design caution <= c*')
    # robustness of the choice to the order of the floating-point run sums (weights of 1 through tensordot)
    Tph2 = [np.tensordot(np.ones(len(old)), np.stack(v), axes=(0, 0)) for v in ph_tabs]
    tri2 = triple_at(Tph2, float(100. * np.tensordot(np.ones(len(old)), np.stack(per['F0']), axes=(0, 0))[K.I_G1, 2]
                                 / np.tensordot(np.ones(len(old)), np.stack(per['F0']), axes=(0, 0))[K.I_G1, 3]))
    tri['same_choice_with_tensordot_sums'] = bool(tri2 is not None and tri2['idx'] == tri['idx'])
    tri['design_phase_counts'] = [int(x) for x in conf]
    ms['PS'] = tri
    return ms, Tph


def validate_v12(old, Tph):
    """Old-run check only: the in-sample per-phase gain over the 201 levels of record against v12's record (A9-3 v02, estimated
    phase, threshold -1.0). Uses triple_at at every level."""
    Tall = {s: np.stack([K.run_table(r, K.grid_sel(r, s), r['clear1'] > 0.) for r in old]).sum(axis=0) for s in ('F0', 'E')} \
        if 'E' in old[0]['crit'] else None
    if Tall is None:
        return None
    cur = L.curves_w(Tall, 0); cF0, wF0 = cur['F0']; cE, wE = cur['E']
    lev = L.levels_of(cF0, cE, cF0[0])
    f1 = L.frontier(cF0, wF0, lev)
    cp = [cF0[0]]; wp = [wF0[0]]
    for lv in lev:
        t = triple_at(Tph, lv)
        if t is not None:
            cp.append(t['design_caution']); wp.append(t['design_wrong_go'])
    fps = L.frontier(np.array(cp), np.array(wp), lev)
    gain = float(np.sum(f1 - fps))
    rec = json.loads((K.V12OUT / 'A9_3_PHASE_SCALE_CV_v02.json').read_text(encoding='utf-8'))
    ref = rec['b_estimated_phase']['-1.0']['insample']['gain_pp']
    return dict(gain_pp_here=gain / L.NLEV, gain_pp_v12=ref, abs_diff=abs(gain / L.NLEV - ref))


# ------------------------------------------------------------------------------------------------ per variant
def source_stats(r, ms):
    """(n, wrong, caution sum, caution count) of F0 at g = 1 and of every source at its matched setting, for one run."""
    safe = r['clear1'] > 0.
    out = {}

    def one(sel):
        return K.run_table(r, sel[None, :], safe)[0, :4]
    out['F0'] = one(L.select_grid(r['crit']['F0'], [1.0], r['idx55'])[0])
    for s in SOURCES:
        out[s] = one(L.select_grid(r['crit'][s], [ms['sources'][s]['g']], r['idx55'])[0])
    ph = K.est_phase(r['vhat'], r['ahat_long'], r['lead_found'], -1.0)
    sel3 = L.select_grid(r['crit']['F0'], ms['PS']['g'], r['idx55'])            # (3, n)
    out['PS'] = one(sel3[ph, np.arange(ph.size)])
    return out


def classify(ci_c, ci_w):
    """A10 D-H1, in the order written: costs progress; costs safety; no measurable cost; inconclusive."""
    if ci_c[0] > 1. and ci_w[1] <= 0.:
        return 'costs progress'
    if ci_w[0] > 0.:
        return 'costs safety'
    if all(-1. <= x <= 1. for x in ci_c + ci_w):
        return 'no measurable cost'
    return 'inconclusive'


def variant_result(runs, ms, CNT):
    per = [source_stats(r, ms) for r in runs]
    X = {s: np.stack([p[s] for p in per]) for s in ['F0'] + ALL}                 # (nrun, 4)
    res = {'n_runs': len(runs), 'runs': [r['run'] for r in runs], 'sources': {}}

    def rates(S):
        with np.errstate(divide='ignore', invalid='ignore'):
            return 100. * S[..., 2] / S[..., 3], 100. * S[..., 1] / S[..., 0]
    tot0 = X['F0'].sum(axis=0); c0, w0 = rates(tot0)
    B0 = CNT @ X['F0']; cb0, wb0 = rates(B0)
    res['F0_g1'] = dict(caution=float(c0), wrong_go=float(w0), n_decisions=int(round(tot0[0])), n_wrong=int(round(tot0[1])),
                        n_caution_count=int(round(tot0[3])), caution_sum=float(tot0[2]))
    for s in ALL:
        tot = X[s].sum(axis=0); c, w = rates(tot)
        B = CNT @ X[s]; cb, wb = rates(B)
        dc = cb - cb0; dw = wb - wb0
        ci_c = K.pct(dc); ci_w = K.pct(dw)
        res['sources'][s] = dict(caution=float(c), wrong_go=float(w), n_decisions=int(round(tot[0])), n_wrong=int(round(tot[1])),
                                 n_caution_count=int(round(tot[3])), caution_sum=float(tot[2]),
                                 d_caution=dict(point=float(c - c0), ci=ci_c, n_nonfinite=int((~np.isfinite(dc)).sum())),
                                 d_wrong_go=dict(point=float(w - w0), ci=ci_w, n_nonfinite=int((~np.isfinite(dw)).sum())),
                                 classification=classify(ci_c, ci_w))
    res['D-H1'] = res['sources'][HYP['D-H1']]['classification']
    res['D-H2'] = res['sources'][HYP['D-H2']]['classification']
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--tag', default='')
    ap.add_argument('--check-v12', action='store_true', help='old-run identity check of the triple rule (slow)')
    ap.add_argument('--nboot', type=int, default=K.NBOOT, help='test only; the recount uses 20000')
    a = ap.parse_args()
    t0 = time.time()
    name = 'RC_D_NONBRAKING_v13' + ('_TESTOLD' if a.test_old else '') + ('_' + a.tag if a.tag else '') + '.json'
    outf = K.OUT / name
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    if not a.test_old:
        K.require_lock()
        if a.nboot != K.NBOOT:
            raise SystemExit('REFUSED: the recount uses 20000 resamples')
    old = K.old_runs()
    if len(old) != 35:
        raise RuntimeError('REFUSED: %d old runs' % len(old))
    ms, Tph = matched_settings(old)
    doc = dict(code='rc_d_nonbraking_v13.py', mode='TEST ON OLD RUNS (exploratory; not a D1 result)' if a.test_old else 'fresh D1 runs',
               spec='AMENDMENT_10_v13.md sec. 6 D1; CD_DEFINITIONS_v13.md D1', nboot=a.nboot, seed=K.SEED_BOOT,
               matched_settings=ms, variants={})
    print('c* = %.6f; matched: %s; PS %s' % (ms['c_star'], {s: v['g'] for s, v in ms['sources'].items()}, ms['PS']['g']), flush=True)
    if a.test_old and a.check_v12:
        # E is in the v11 loader's crit; fetch it for the v12 identity check only
        raw = {r['run']: r for r in K.C.load_runs()}
        for r in old:
            r['crit']['E'] = raw[r['run']]['crit']['E']
        doc['check_v12_insample_gain'] = validate_v12(old, Tph)
        for r in old:
            r['crit'].pop('E')
        print('v12 identity:', doc['check_v12_insample_gain'], flush=True)
    if a.test_old:
        sets = {'old_as_variant': old}
        doc['d1_run_order_file_equals_sorted'] = None
    else:
        ids, order_ok = K.cases_d1()
        doc['d1_run_order_file_equals_sorted'] = bool(order_ok)
        sets = {}
        for kind, rids in ids.items():
            if len(rids) != 35:
                raise RuntimeError('REFUSED: variant %s has %d runs' % (kind, len(rids)))
            sets[kind] = [K.fresh_run(rid, need_tg=True, variant_kind=kind) for rid in rids]
    for kind, runs in sets.items():
        CNT = L.boot_counts(len(runs), a.nboot, K.SEED_BOOT)                    # the same draw for every variant
        doc['variants'][kind] = variant_result(runs, ms, CNT)
        v = doc['variants'][kind]
        print(kind, 'D-H1:', v['D-H1'], '| D-H2:', v['D-H2'], flush=True)
    doc['seconds'] = time.time() - t0; doc['written'] = K.clock()
    K.write_once(outf, doc)
    print('written', outf)


if __name__ == '__main__':
    sys.exit(main())
