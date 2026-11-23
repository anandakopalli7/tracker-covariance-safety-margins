"""Recount3 self-check: the same quantities by a plain, slow route that shares no evaluation code with r3_lib_v01 / rc_lib_v01.
Decisions of the population are concatenated (no per-run sufficient statistics); the selection is recomputed from the critical
scales per scale; levels by numpy.linspace; the step frontier by a loop over levels (min wrong go among points with caution <=
level). Only the data loader (R.load_eval_runs) and the grid are shared.
Compares with RECOUNT3_RESULTS_v01.json (own results) and, for a few resamples and subsamples, with R.boot_g.
Usage: python -B -X utf8 r3_naive_v01.py        -> r3_naive_v01_out.json"""
import json
import numpy as np
import r3_lib_v01 as R
L = R.L
GRID = L.GRID
res = json.loads((R.HERE / 'RECOUNT3_RESULTS_v01.json').read_text(encoding='utf-8'))


def cat(ds, runs, key, sub=None):
    return np.concatenate([(ds[i][key] if sub is None else ds[i][key][sub]) for i in runs])


def points(crit, idx55, unsafe_w, safe_c, vbar, des):
    """Points (caution %, wrong go %) of one arm at every scale of the grid."""
    n = crit.shape[0]; ar = np.arange(n)
    first = np.array([np.flatnonzero(safe_c[i])[0] if safe_c[i].any() else 0 for i in range(n)])
    c = np.full(GRID.size, np.nan); w = np.full(GRID.size, np.nan)
    for gi, g in enumerate(GRID):
        feas = crit >= g
        sel = np.where(feas.any(1), feas.argmax(1), idx55)
        w[gi] = 100. * unsafe_w[ar, sel].sum() / n
        ok = safe_c[ar, sel]
        if ok.any():
            c[gi] = 100. * (((vbar[ar, first] - vbar[ar, sel]) / des)[ok]).sum() / ok.sum()
    return c, w


def frontier(c, w, lev):
    out = np.full(lev.size, np.nan)
    for i, x in enumerate(lev):
        m = c <= x
        if m.any():
            out[i] = w[m].min()
    return out


def pop_eval(P, arms, oracle):
    """P: dict of concatenated arrays of one population. arms: dict name -> crit array (must hold 'F0' and 'E').
    Returns D per arm (sum over levels of F_F0 - F_arm), den0 if oracle, and the zero-margin points."""
    n = P['idx55'].size
    if n == 0:
        return None
    pts = {a: points(c, P['idx55'], P['unsafe_w'], P['safe_c'], P['vbar'], P['des']) for a, c in arms.items()}
    cF, wF = pts['F0']; cE, wE = pts['E']
    lev = np.linspace(cF[0], min(np.nanmax(cF), np.nanmax(cE)), 201)
    fF = frontier(cF, wF, lev)
    D = {}; zero = {}
    for a, (c, w) in pts.items():
        zero[a] = (float(c[0]), float(w[0]))
        if a == 'F0':
            continue
        if a != 'E':
            c = np.concatenate([[cF[0]], c]); w = np.concatenate([[wF[0]], w])
        D[a] = float(np.sum(fF - frontier(c, w, lev)))
    if oracle:
        ar = np.arange(n)
        sw = ~P['unsafe_w']
        sel = np.where(sw.any(1), sw.argmax(1), P['idx55'])
        first = np.array([np.flatnonzero(P['safe_c'][i])[0] if P['safe_c'][i].any() else 0 for i in range(n)])
        ok = P['safe_c'][ar, sel]
        cO = 100. * (((P['vbar'][ar, first] - P['vbar'][ar, sel]) / P['des'])[ok]).sum() / ok.sum() if ok.any() else np.nan
        wO = 100. * P['unsafe_w'][ar, sel].sum() / n
        D['O'] = float(np.sum(fF - frontier(np.array([cF[0], cO]), np.array([wF[0], wO]), lev)))
    return dict(n=n, D=D, zero=zero)


def build(ds, runs, unsafe_key, gap, arm_crit):
    """Concatenate the runs (list of indices, repeats allowed). unsafe_key: 'clear' or 'clearX'. arm_crit: name -> fn(d) -> crit."""
    full = dict(idx55=cat(ds, runs, 'idx55'), vbar=cat(ds, runs, 'vbar'), des=cat(ds, runs, 'des'), v0=cat(ds, runs, 'v0'),
                phase=cat(ds, runs, 'phase'))
    full['unsafe_w'] = ~(cat(ds, runs, unsafe_key) > gap)
    full['safe_c'] = cat(ds, runs, 'clear') > gap
    arms = {a: np.concatenate([fn(ds[i]) for i in runs]) for a, fn in arm_crit.items()}
    return full, arms


def pops_eval(full, arms, oracle):
    masks = dict(all=np.ones(full['idx55'].size, bool), moving=full['v0'] > 0.5, phase0=full['phase'] == 0, phase1=full['phase'] == 1,
                 phase2=full['phase'] == 2)
    out = {}
    for pn, m in masks.items():
        P = {k: v[m] for k, v in full.items()}
        out[pn] = pop_eval(P, {a: c[m] for a, c in arms.items()}, oracle)
    # phase-weighted: sum_p (n_p / n) D_p over phases 0-2
    nt = sum(out[p]['n'] for p in ('phase0', 'phase1', 'phase2') if out[p] is not None)
    keys = out['all']['D'].keys()
    out['phase_weighted'] = dict(n=nt, D={a: sum(out[p]['n'] / nt * out[p]['D'][a] for p in ('phase0', 'phase1', 'phase2') if out[p] is not None)
                                          for a in keys})
    return out


worst = dict(v=0.)
log = []


def cmp(tag, mine, ref):
    if ref is None or mine is None:
        d = 0. if (ref is None and (mine is None or not np.isfinite(mine))) else float('inf')
    elif not np.isfinite(mine) or not np.isfinite(ref):
        d = 0. if (not np.isfinite(mine) and not np.isfinite(ref)) else float('inf')
    else:
        d = abs(mine - ref)
    worst['v'] = max(worst['v'], d)
    log.append(dict(tag=tag, naive=mine, program=ref, absdiff=d))


def main():
    ds = R.load_eval_runs()
    allruns = list(range(35))
    std = {a: (lambda d, a=a: d['crit'][a]) for a in L.ARMS}
    # ---- item 4 points (and item 2 theta)
    armfn = dict(F0=std['F0'], E=std['E'])
    for a in R.CK_ARMS:
        armfn[a] = (lambda d, a=a: d['ck'][a])
    full, arms = build(ds, allruns, 'clear', 0., armfn)
    ev = pops_eval(full, arms, False)
    i4 = res['item4_S25']
    for a0 in range(1, 8):
        for pn in ('all', 'moving', 'phase0', 'phase1', 'phase2', 'phase_weighted'):
            e = ev[pn]; r = i4['a0'][str(a0)][pn]
            cmp('S25 a0=%d %s RR' % (a0, pn), e['D']['CK%d' % a0] / e['D']['E'], r['RR'])
            cmp('S25 a0=%d %s D deceq' % (a0, pn), e['D']['CK%d' % a0] / 201. / 100. * e['n'], r['D_deceq'])
    for a in ('F0',) + R.CK_ARMS:
        cmp('S25 zero margin %s caution' % a, ev['all']['zero'][a][0], i4['zero_margin'][a]['caution_pct'])
        cmp('S25 zero margin %s wrong go' % a, ev['all']['zero'][a][1], i4['zero_margin'][a]['wrong_go_pct'])
    full, arms = build(ds, allruns, 'clear', 0., std)
    e = pop_eval(full, arms, True)
    th = res['item2_S17']['theta']
    naive_theta = dict(R=e['D']['E'] / 201., RR_N=e['D']['N'] / e['D']['E'], RR_NA=e['D']['NA'] / e['D']['E'], RR_AM=e['D']['AM'] / e['D']['E'],
                       RR_CK3=e['D']['CK3'] / e['D']['E'], RR_Q=e['D']['Q'] / e['D']['E'], RR0_CK3=e['D']['CK3'] / e['D']['O'],
                       RR_NA_minus_RR_N=e['D']['NA'] / e['D']['E'] - e['D']['N'] / e['D']['E'])
    for k, v in naive_theta.items():
        cmp('S17 theta %s' % k, v, th[k])
    # ---- item 2: the first two subsamples of each m, naive on the concatenated subsample
    Mfull = np.stack([R.run_vector(d, [d['sel'][a] for a in L.ARMS], L.masks_all(d), d['clear'] > 0., d['clear'] > 0.) for d in ds])
    rng = np.random.default_rng(20261124)
    for m in (15, 20, 25):
        idx = np.stack([rng.permutation(35)[:m] for _ in range(5000)])
        if [int(x) for x in idx[0]] != res['item2_S17']['m'][str(m)]['first_subsample']:
            raise RuntimeError('subsample stream differs from the program')
        nb, Db, _ = R.boot_g(Mfull, idx[:2], 1, 7)
        for b in range(2):
            full, arms = build(ds, [int(x) for x in idx[b]], 'clear', 0., std)
            e = pop_eval(full, arms, True)
            cmp('S17 m=%d subsample %d denE' % (m, b), e['D']['E'], float(Db[b, 0, 1]))
            cmp('S17 m=%d subsample %d D CK3' % (m, b), e['D']['CK3'], float(Db[b, 0, 4 + 1]))
            cmp('S17 m=%d subsample %d den0' % (m, b), e['D']['O'], float(Db[b, 0, 7]))
            cmp('S17 m=%d subsample %d D NA' % (m, b), e['D']['NA'], float(Db[b, 0, 3]))
    # ---- item 3 points
    full, arms = build(ds, allruns, 'clearX', 2.0, std)
    ev = pops_eval(full, arms, True)
    i3 = res['item3_S24b']['pops']
    for pn in ('all', 'moving', 'phase0', 'phase1', 'phase2', 'phase_weighted'):
        e = ev[pn]; r = i3[pn]
        cmp('S24b %s den0 pp' % pn, e['D']['O'] / 201., r['den0_pp']['point'])
        cmp('S24b %s den0 deceq' % pn, e['D']['O'] / 201. / 100. * e['n'], r['den0_deceq']['point'])
        for a in ('E', 'N', 'NA', 'CK3', 'AM', 'Q'):
            cmp('S24b %s RR0 %s' % (pn, a), (e['D'][a] / e['D']['O']) if e['D']['O'] != 0 else None, r['RR0_' + a]['point'])
    # ---- items 3 and 4: the first two resamples of the draw of record, naive on the concatenated resample
    idx = L.draw_of_record()[:2]
    M3 = np.stack([R.run_vector(d, [d['sel'][a] for a in L.ARMS], L.masks_std(d), d['clearX'] > 2.0, d['clear'] > 2.0) for d in ds])
    nb, Db, _ = R.boot_g(M3, idx, 5, 7)
    for b in range(2):
        full, arms = build(ds, [int(x) for x in idx[b]], 'clearX', 2.0, std)
        ev = pops_eval(full, arms, True)
        for pi, pn in enumerate(R.POPS):
            cmp('S24b resample %d %s den0' % (b, pn), ev[pn]['D']['O'], float(Db[b, pi, 7]))
            cmp('S24b resample %d %s D CK3' % (b, pn), ev[pn]['D']['CK3'], float(Db[b, pi, 5]))
            cmp('S24b resample %d %s D AM' % (b, pn), ev[pn]['D']['AM'], float(Db[b, pi, 4]))
            cmp('S24b resample %d %s denE' % (b, pn), ev[pn]['D']['E'], float(Db[b, pi, 1]))
    rows = []
    for d in ds:
        safe = d['clear'] > 0.
        sels = [d['sel']['F0'], d['sel']['E']] + [L.select(d['ck'][a], d['idx55']) for a in R.CK_ARMS]
        rows.append(R.run_vector(d, sels, L.masks_std(d), safe, safe, with_oracle=False))
    M4 = np.stack(rows)
    nb, Db, _ = R.boot_g(M4, idx, 5, 9, with_oracle=False)
    for b in range(2):
        full, arms = build(ds, [int(x) for x in idx[b]], 'clear', 0., armfn)
        ev = pops_eval(full, arms, False)
        for pi, pn in enumerate(R.POPS):
            cmp('S25 resample %d %s denE' % (b, pn), ev[pn]['D']['E'], float(Db[b, pi, 1]))
            for a0 in (1, 3, 7):
                cmp('S25 resample %d %s D CK%d' % (b, pn, a0), ev[pn]['D']['CK%d' % a0], float(Db[b, pi, 1 + a0]))
    # ---- item 1: draws 0, 1 and 49, the partial arm built from the critical scales
    i1 = res['item1_S12b']['share']
    n_st = [d['n_stored'] for d in ds]; off = np.concatenate([[0], np.cumsum(n_st)])
    for i in (0, 1, 49):
        u = np.random.default_rng(20261200 + i).random(int(off[-1]))
        for p in (0.25, 0.50, 0.75):
            def part(d, p=p, u=u):
                ri = L.RUNS.index(d['run'])
                m = u[off[ri]:off[ri + 1]][d['ev_all']] < p
                return np.where(m[:, None], d['crit']['E'], d['crit']['F0'])
            full, arms = build(ds, allruns, 'clear', 0., dict(F0=std['F0'], E=std['E'], PART=part))
            ev = pops_eval(full, arms, False)
            for pn in ('all', 'moving', 'phase1', 'phase2', 'phase_weighted'):
                cmp('S12b draw %d p=%.2f %s RR' % (i, p, pn), ev[pn]['D']['PART'] / ev[pn]['D']['E'], i1['%.2f' % p]['pops'][pn]['RR_draws'][i])
    out = dict(what='naive recomputation against the program (own results)', n_compared=len(log), max_abs_diff=worst['v'],
               n_above_1e9=int(sum(1 for x in log if x['absdiff'] > 1e-9)), entries=log)
    L.jdump(out, R.HERE / 'r3_naive_v01_out.json')
    print('naive check: %d numbers, max abs diff %.3e, above 1e-9: %d' % (len(log), worst['v'], out['n_above_1e9']))
    for x in log:
        if x['absdiff'] > 1e-9:
            print('  ', x)


if __name__ == '__main__':
    main()
