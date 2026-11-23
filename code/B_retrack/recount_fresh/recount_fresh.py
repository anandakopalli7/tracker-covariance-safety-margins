"""Package B, independent second program for the fresh lead-braking runs (v13).  Spec: B_FRESH_DEFINITIONS_v02.md.
Usage (run with: python -I -B -X utf8 recount_fresh.py ...):
  --test-old [--variants CV IMM ...] [--K 2000]   35 old runs, draw of record (first K rows), writes out\\TESTOLD_*
  --fresh    [--variants ...] [--K 20000]         105 fresh runs; REFUSES unless revision_v13\\LOCK_A10_2.txt exists
  --combine  (with --test-old or --fresh)         merge per-variant parts into the flat JSON (+ B.rule.*)
"""
import sys, os, json, time, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

V13 = r'ARS_TRIAL\revision_v13'
LOCK = V13 + r'\LOCK_A10_2.txt'
LOCK_C = V13 + r'\LOCK_A10_2c.txt'
LOCKS = [LOCK, LOCK_C]
BR = V13 + r'\work\B_retrack'
CD = V13 + r'\work\CD_capture'
OUTD = HERE + r'\out'
FINAL_FRESH = BR + r'\out\A_RECOUNT_B.json'

# key name -> (variant folder, fresh path template, old folder)
VARS = {
    'CV': 'CV0', 'IMM': 'B1', 'CV2': 'B3', 'CA': 'B4', 'AQ': 'B2', 'IMM090': 'B1_d090', 'IMM098': 'B1_d098',
}
ORDER = ['CV', 'IMM', 'CV2', 'CA', 'AQ', 'IMM090', 'IMM098']
DELTA = 0.05


def check_locks():
    """Every fresh path (variants, --b6, fresh --combine) needs BOTH lock files; returns their SHA-256."""
    import hashlib
    miss = [p for p in LOCKS if not os.path.exists(p)]
    if miss:
        raise SystemExit('REFUSED: fresh runs are sealed; missing ' + ', '.join(miss))
    return {os.path.basename(p): hashlib.sha256(open(p, 'rb').read()).hexdigest() for p in LOCKS}


def fresh_path(name, rid):
    v = VARS[name]
    if name in ('CV', 'IMM'):
        return r'%s\arrays\%s\%s.npz' % (CD, v, rid)
    return r'%s\out\retrack_fresh\%s\%s_arrays.npz' % (BR, v, rid)


def old_path(name, run):
    return r'%s\out\retrack\%s\%s_arrays.npz' % (BR, VARS[name], run)


def fresh_run_ids():
    """lead_braking cases of CASES_C_v13.json, replaced via REPLACEMENTS_C_v13.json if listed, as pc13_<case>_native, sorted."""
    cases = json.load(open(CD + r'\CASES_C_v13.json'))['cases']
    lb = [c['case'] for c in cases if c['family'] == 'lead_braking']
    rep = {}
    rp = CD + r'\REPLACEMENTS_C_v13.json'
    if os.path.exists(rp):
        d = json.load(open(rp))
        if isinstance(d, dict) and 'replacements' in d:
            d = d['replacements']
        if isinstance(d, dict):
            rep = {k: (v if isinstance(v, str) else v.get('replacement', v.get('case'))) for k, v in d.items()}
        elif isinstance(d, list):
            for e in d:
                o = e.get('case', e.get('original', e.get('replaced')))
                n = e.get('replacement', e.get('replaced_by', e.get('new')))
                if o is not None and n is not None:
                    rep[o] = n
        else:
            raise SystemExit('REPLACEMENTS_C_v13.json: unrecognised structure')
        print('replacements used:', {k: v for k, v in rep.items() if k in lb}, flush=True)
    else:
        print('WARNING: no REPLACEMENTS_C_v13.json found; no replacements applied', flush=True)
    ids = sorted('pc13_%s_native' % rep.get(c, c) for c in lb)
    return ids


def setup(mode):
    """returns (run names, path function, n_runs, seed)"""
    if mode == 'fresh':
        check_locks()
        ids = fresh_run_ids()
        assert len(ids) == 105 and len(set(ids)) == 105, len(ids)
        return ids, fresh_path, 105, 20261911
    runs = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
    return runs, old_path, 35, 20261113


# ---------------------------------------------------------------------------------------------------------------- compute
def est_phase_masks(q, thr=-1.0):
    lf = q['lead_found'].astype(bool); v = q['vhat']; a = q['ahat_long']
    with np.errstate(invalid='ignore'):
        st = lf & (v <= 0.5)
        br = lf & (v > 0.5) & (a <= thr)
    return [~(st | br), br, st]       # pre, brk, stop


def mask_list(q):
    n = len(q['k'])
    e = est_phase_masks(q)
    return [np.ones(n, bool), e[0], e[1], e[2], q['phase'] == 2]


MN = ['all', 'pre', 'brk', 'stop', 'truth2']
NAMES = ['N', 'E5x', 'CK3']


def classify(r_ci, c_ci):
    """H3 wording applied to (RR, c), delta = 0.05"""
    if r_ci[0] > 0:
        return 'recovers'
    if c_ci[0] > DELTA:
        return 'uninformative variation'
    if c_ci[0] > -DELTA and c_ci[1] < DELTA:   # c's interval inside (-delta, delta)
        return 'amplitude-limited'
    return 'inconclusive'


def lag_of(data, names, use_now=True, first_eval=False):
    vals = []
    for nm in names:
        r = data[nm]; ph = r['phase']; ev = r['evaluated'].astype(bool)
        pool = (ph == 2) & (ev if first_eval else True)
        i2 = np.nonzero(pool)[0]
        if not i2.size:
            continue
        if use_now:
            dt = r['now'] - r['now'][i2[0]]
            ok = (dt >= 0) & (dt < 1.0)
        else:
            dt = (r['k'] - r['k'][i2[0]]) * 0.05
            ok = (dt >= -1e-9) & (dt < 1.0 - 1e-9)
        sel = ev & (ph == 2) & ok & np.isfinite(r['dx_pred3']) & r['lead_found'].astype(bool)
        vals.append(r['dx_pred3'][sel])
    v = np.concatenate(vals) if vals else np.array([])
    return (float(np.median(v)) if v.size else float('nan')), int(v.size)


def per_variant(name, mode, K, log=print):
    from rf_core import (np, L, NS, RunSet, breakpoints, stats_curve, margin_ratio_rows, margin_stats, ranks_u, oracle_C,
                         M_REC, A_REC)
    t0 = time.time()
    names, pathf, nr, seed = setup(mode)
    data = {r: dict(np.load(pathf(name, r), allow_pickle=True)) for r in names}
    rs = RunSet(data, names)
    n_ev = int(sum(rs.n_eval))
    ms = margin_stats(margin_ratio_rows(rs))
    u = ranks_u(rs)
    Cs = {'F0': [q['cF0'] for q in rs.d], 'E': [q['cE'] for q in rs.d], 'N': [q['cN'] for q in rs.d],
          'CK3': [q['cCK3'] for q in rs.d], 'E5x': oracle_C(rs, u, ms['median'], ms['A'])}
    S = {}
    for nm, Cl in Cs.items():
        G = breakpoints(Cl)
        Tsum = None; Trun = []
        for q, C in zip(rs.d, Cl):
            c1 = L.clean_clear(q['clear'])
            T = stats_curve(C, G, c1, c1 > 0., q['vbar'], q['des'], q['idx55'], mask_list(q))
            Tsum = T.copy() if Tsum is None else Tsum + T
            Trun.append(T[:, 0, :].copy())
        S[nm] = dict(G=G, Tsum=Tsum, Trun=np.stack(Trun))
    log(name, 'stats done %.1fs' % (time.time() - t0), {k: len(v['G']) for k, v in S.items()}, flush=True)

    def pop(mi, nms):
        Td = {k: S[k]['Tsum'][:, mi, :] for k in ['F0', 'E'] + nms}
        return L.eval_scoring(Td, nms)

    ev = pop(0, NAMES)
    n = ev['n']
    res = {}
    res['R'] = ev['denE'] / 201.
    res['R.dec'] = L.dec_eq(ev['denE'], n)
    res['RR'] = L.ratio(ev['D']['N'], ev['denE'])
    res['c'] = L.ratio(ev['D']['E5x'], ev['denE'])
    res['RR_CK3'] = L.ratio(ev['D']['CK3'], ev['denE'])
    res['RR_minus_c'] = res['RR'] - res['c']
    res.update(m=ms['median'], A=ms['A'], q05=ms['q05'], q95=ms['q95'], within5=ms['share_within5'],
               barely=bool(ms['share_within5'] >= 0.95))
    for key, mi in (('room_pre', 1), ('room_brk', 2), ('room_stop', 3)):
        e = pop(mi, [])
        res[key] = e['denE'] / 201. if e['n'] else float('nan')
    e2 = pop(4, [])
    res['as_room'] = L.dec_eq(e2['denE'], e2['n']) if e2['n'] else float('nan')
    res['as_room.pp'] = e2['denE'] / 201. if e2['n'] else float('nan')
    res['lag'], lag_n = lag_of(data, names)
    res['n_dec'] = n_ev
    res['n_runs'] = nr
    sens = dict(n_eval_check=n, lag_n=lag_n,
                lag_tickclock=lag_of(data, names, use_now=False)[0],
                lag_first_evaluated_stop=lag_of(data, names, first_eval=True)[0],
                n_pop=[float(pop(i, [])['n']) for i in range(5)])

    # ---- bootstrap
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, nr, (20000, nr))[:K]
    cnt = np.zeros((K, nr))
    for b in range(K):
        cnt[b] = np.bincount(idx[b], minlength=nr)
    del idx
    out = {k: np.full(K, np.nan) for k in ['denE', 'n', 'D_N', 'D_E5x', 'D_CK3']}
    Gtot = max(len(S[k]['G']) for k in S)
    chunk = max(1, min(20, int(4e6 // (Gtot * NS))))
    srcs = ['F0', 'E', 'N', 'E5x', 'CK3']
    flat = {k: S[k]['Trun'].reshape(nr, -1) for k in srcs}
    tb = time.time()
    for b0 in range(0, K, chunk):
        c = cnt[b0:b0 + chunk]
        Tb = {k: (c @ flat[k]).reshape(len(c), -1, NS) for k in srcs}
        for j in range(len(c)):
            e = L.eval_scoring({k: Tb[k][j] for k in srcs}, NAMES)
            i = b0 + j
            out['denE'][i] = e['denE']; out['n'][i] = e['n']
            out['D_N'][i] = e['D']['N']; out['D_E5x'][i] = e['D']['E5x']; out['D_CK3'][i] = e['D']['CK3']
        if (b0 // chunk) % 25 == 0:
            log(name, 'boot %d/%d  %.1fs' % (b0, K, time.time() - tb), flush=True)
    boot_s = time.time() - tb
    den = out['denE']
    with np.errstate(divide='ignore', invalid='ignore'):
        pos = den > 0
        rr = np.where(pos, out['D_N'] / den, np.nan)
        cc = np.where(pos, out['D_E5x'] / den, np.nan)
        ck = np.where(pos, out['D_CK3'] / den, np.nan)
    res['R.ci'] = L.pct(den / 201.)
    res['RR.ci'] = L.pct(rr)
    res['c.ci'] = L.pct(cc)
    res['RR_minus_c.ci'] = L.pct(rr - cc)
    res['RR_CK3.ci'] = L.pct(ck)
    res['class'] = classify(res['RR.ci'], res['c.ci'])
    sens.update(K=K, boot_seconds=boot_s, boot_ms_per_resample=1000 * boot_s / K, total_seconds=time.time() - t0,
                n_G={k: len(S[k]['G']) for k in S}, share_den_pos=float(pos.mean()))
    return res, out, sens


def finite_equal_json(o):
    return json.loads(json.dumps(o, default=float))


def run_variant(name, mode, K):
    pre = 'testold' if mode == 'old' else 'fresh'
    res, out, sens = per_variant(name, mode, K)
    if mode == 'fresh':
        sens['lock_sha256'] = check_locks()
    os.makedirs(OUTD, exist_ok=True)
    npzname = (OUTD + r'\testold_boot_%s.npz' if mode == 'old' else OUTD + r'\boot_%s.npz') % name
    np.savez(npzname, **out)
    json.dump(dict(res=res, sens=sens), open(OUTD + r'\part_%s_%s.json' % (pre, name), 'w'), indent=1, default=float)
    print(name, 'written; total %.1fs' % sens['total_seconds'], flush=True)


def combine(mode):
    pre = 'testold' if mode == 'old' else 'fresh'
    flat = {}; sens = {}
    for name in ORDER:
        p = OUTD + r'\part_%s_%s.json' % (pre, name)
        if not os.path.exists(p):
            raise SystemExit('missing part ' + p)
        d = json.load(open(p))
        for k, v in d['res'].items():
            flat['B.%s.%s' % (name, k)] = v
        sens[name] = d['sens']
    rule = {}
    for x in ('CV2', 'CA'):
        rule['B.rule.' + x] = dict(
            as_room_below_half=bool(flat['B.%s.as_room' % x] < 0.5 * flat['B.CV.as_room']),
            ck3_differs=bool(abs(flat['B.%s.RR_CK3' % x] - flat['B.CV.RR_CK3']) > 0.10))
    anyt = any(v['as_room_below_half'] or v['ck3_differs'] for v in rule.values())
    rule['B.rule.outcome'] = 'depends on filter tuning' if anyt else 'mechanism persists'
    flat.update(rule)
    if mode == 'fresh':
        flat['B.lock_sha256'] = check_locks()
    for part in (pre + '_b6', 'tu'):
        p = OUTD + r'\part_%s.json' % part
        if os.path.exists(p):
            d = json.load(open(p)); flat.update(d['res']); sens[part] = d['sens']
        else:
            print('WARNING: no', p, '(LB/TU keys missing)')
    target = OUTD + r'\TESTOLD_A_RECOUNT_B.json' if mode == 'old' else FINAL_FRESH
    json.dump(flat, open(target, 'w'), indent=1, default=float)
    json.dump(sens, open(OUTD + r'\%s_sensitivities.json' % pre, 'w'), indent=1, default=float)
    print('combined ->', target)


def run_b6(mode, K):
    import b6tu
    res, out, sens = b6tu.b6_compute('fresh' if mode == 'fresh' else 'old', K)
    if mode == 'fresh':
        sens['lock_sha256'] = check_locks()
    os.makedirs(OUTD, exist_ok=True)
    np.savez(os.path.join(OUTD, 'boot_b6.npz' if mode == 'fresh' else 'testold_boot_b6.npz'), **out)
    json.dump(dict(res=res, sens=sens), open(OUTD + r'\part_%s_b6.json' % ('fresh' if mode == 'fresh' else 'testold'), 'w'), indent=1, default=float)
    print('b6 written', flush=True)


def run_tu(K):
    import b6tu
    res, out, sens = b6tu.tu_compute(K)
    np.savez(os.path.join(OUTD, 'boot_tu.npz'), **out)
    json.dump(dict(res=res, sens=sens), open(OUTD + r'\part_tu.json', 'w'), indent=1, default=float)
    print('tu written', flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--test-old', action='store_true')
    g.add_argument('--fresh', action='store_true')
    ap.add_argument('--variants', nargs='*', default=None)
    ap.add_argument('--K', type=int, default=None)
    ap.add_argument('--b6', action='store_true', help='B6 / stop reliance (LB.*) only')
    ap.add_argument('--tu', action='store_true', help='tuning runs (TU.*) only (same in both modes)')
    ap.add_argument('--combine', action='store_true', help='only merge existing parts')
    a = ap.parse_args()
    mode = 'fresh' if a.fresh else 'old'
    lock_sha = check_locks() if mode == 'fresh' else None
    if lock_sha:
        print('locks:', lock_sha, flush=True)
    import numpy as np
    K = a.K or (20000 if mode == 'fresh' else 2000)
    if a.b6 or a.tu:
        if a.b6:
            run_b6(mode, a.K or (20000 if mode == 'fresh' else 2000))
        if a.tu:
            run_tu(a.K or 2000)
        sys.exit(0)
    if not a.combine:
        for v in (a.variants or ORDER):
            run_variant(v, mode, K)
    if a.combine or a.variants is None:
        combine(mode)
