"""v13 package B: B6 and the stop reliance on the FRESH lead-braking runs, online tracker of record (A10 section 3 row B6 and section 5.7:
"the reaction-and-stop grid ... B6(a) terciles; B6(b) delayed stop; stop reliance (A9-6)"). Port of b6_stop_v01.py (B6) and of
revision_v12 a9_6_stop_reliance_v01.py part (1) (reliance). New file, 20 Nov 2026 (Claude Opus 5.5). Descriptive.

Scorings (A10 section 1: the reaction-and-stop scoring with plans judged until the stop ends; package CD, 20 Nov ~03:15):
W1 = 3 s commitment (clean clearance > 0); W_R = reaction and stop, tau 0.75 s, 6 m/s^2, judged until the stop ends = clean
clearX_t0p75_a6p0 > 0 (fresh: CD's CD_capture\\arrays\\RSX\\<rid>.npz, its port of revision_v11 rev_e1; test: revision_v11 out\\ext);
DS = delayed variable stop, tau_i = 0.75 + U(0, 0.75) per evaluated decision (default_rng(20261916); runs in the run order, evaluated
decisions in k order), 6 m/s^2, judged until the stop ends (b_stop_ext_v02.delayed_stop_clearance_ext; mode 'clear').
--stop horizon (test only) uses the 61-frame clearances instead (stop cache of record, v01's delayed clearances); it reproduces
B6_STOP_v01.json, the exploratory B6 of record. --stop ext is the scoring of A10 section 1 and the only one allowed on fresh runs.
(a) all runs: room under W_R and under W1, RS075.rel = R(W_R) / R(W1) with an interval from the same resamples; terciles of realised
    lead deceleration (trk_score_v01.realised_decel, terciles): per tercile R(W_R), R(W1), rel, den0 = D(F0, O) under W_R in
    decision-equivalents, evaluable if den0 >= 10, and RR of N, CK3 under W_R; relmin / relmax over the evaluable terciles.
(b) DS: room, den0, RR of N, NA, AM, CK3, Q under DS; DS.rel = R(DS) / R(W1) with an interval from the same resamples.
(c) reliance (A9-6 (1), population all): at each of the 201 levels, each source's grid-frontier operating point under W_R; the share of
    decisions whose selected row is unsafe under W1 but safe under W_R, averaged over the levels (F0, E, N, NA, AM, CK3; O its one
    selection). REL_<src> = that share.
Intervals: fresh optA_lib_v02.boot_counts(105, 20000, 20261911); test: first 2,000 rows of the draw of record. Engine: CD's gl_fast_v13
(read-only). Lock gate: refuses unless revision_v13\\LOCK_A10_2.txt exists, except --test-old (35 old runs: record arrays and stop cache,
v01's delayed-stop clearances out\\b6\\clear\\; must reproduce out\\b6\\B6_STOP_v01.json; reliance also with v11's extended clearance,
which must reproduce revision_v12 A9_6_STOP_RELIANCE_v01.json).
Usage: python -I -B -X utf8 b_fresh_b6_v02.py clear [--workers 3]                         (system python: needs the tracker stack)
       B_retrack\\.venv\\Scripts\\python.exe -I -B -X utf8 b_fresh_b6_v02.py score [--test-old [--stop ext|horizon]] [--threads 2]  (venv)
       Test outputs: --stop ext -> out\\fresh_testold\\B6_TESTOLD_v02.json (the dry run of the fresh path; DS clearances from
       b_stop_ext_v02.py --test-old in out\\fresh_testold\\b6_clear_ext\\); --stop horizon -> B6_TESTOLD_HORIZON_v02.json (identity with v01).
"""
import os, sys, argparse
_ap = argparse.ArgumentParser()
_ap.add_argument('mode', choices=('clear', 'score')); _ap.add_argument('--test-old', action='store_true')
_ap.add_argument('--threads', type=int, default=2); _ap.add_argument('--workers', type=int, default=3)
_ap.add_argument('--stop', choices=('ext', 'horizon'), default='ext')
ARGS = _ap.parse_args() if __name__ == '__main__' else None
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
if ARGS is not None:
    os.environ['NUMBA_NUM_THREADS'] = str(ARGS.threads)
import json, pathlib, time, hashlib
HERE = pathlib.Path(__file__).resolve().parents[1]
WORK = HERE.parent
LIB = WORK / 'shared' / 'trackers'
CDA = WORK / 'CD_capture' / 'analysis'
sys.path.insert(0, str(LIB))
import trk_env_v01 as env
if ARGS is not None and ARGS.mode == 'clear':
    env.setup()                                  # the clearance needs the tracker stack (system python)
import numpy as np
import trk_score_v01 as S
L = S.L; A9 = S.A9; C = A9.C

V13 = WORK.parent
LOCK2 = V13 / 'LOCK_A10_2.txt'
LOCK2C = V13 / 'LOCK_A10_2c.txt'                # coordinator, 20 Nov: no fresh value of B before LOCK_A10_2c
CD = WORK / 'CD_capture'
OUTF = HERE / 'out' / 'fresh_b6'
OUTT = HERE / 'out' / 'fresh_testold'
KEY = 't0p75_a6p0'
EXT = pathlib.Path(r'ARS_TRIAL\revision_v11\analysis\out\ext')
A96 = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis\out\A9_6_STOP_RELIANCE_v01.json')
ARCH = S.P / '07_fit_runs' / 'archives'
SEED_FRESH, NBOOT_FRESH = 20261911, 20000


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def fresh_ids():
    cases = json.loads((CD / 'CASES_C_v13.json').read_text(encoding='utf-8'))['cases']
    rp = CD / 'REPLACEMENTS_C_v13.json'
    rep = json.loads(rp.read_text(encoding='utf-8'))['replacements'] if rp.is_file() else {}
    return sorted('pc13_%s_native' % rep.get(c['case'], c['case']) for c in cases if c['family'] == 'lead_braking')


def fresh_paths(rid):
    rd = CD / 'runs' / rid / rid
    caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
    assert len(caps) == 1, rid
    return rd, caps[0]


def old_cap(run):
    return list((ARCH / run / 'x' / run / 'capture').iterdir())[0]


def load_fresh(with_rsx=True):
    """with_rsx=False for mode 'clear' (arrays only; CD's stage-2 RSX arrays are not needed and may not exist yet)."""
    runs = []
    for rid in fresh_ids():
        z = np.load(CD / 'arrays' / 'CV0' / (rid + '.npz'), allow_pickle=False)
        ev = z['evaluated'].astype(bool)
        runs.append(dict(run=rid, desired=float(z['des'][0]), k=z['k'], ev=ev, v0=z['v0'], vbar=z['vbar'], idx55=z['idx55'].astype(np.int64),
                         clear1=L.clean_clear(z['clear']), n_dec=int(ev.size), masks=(ev,), sel={}, late={},
                         crit={'F0': np.asarray(z['cF0'], float), 'E': np.asarray(z['cE'], float), 'N': np.asarray(z['cN'], float),
                               'NA': np.asarray(z['cNA'], float), 'AM': np.asarray(z['cA1'], float), 'CK3': np.asarray(z['cCK3'], float),
                               'Q': np.asarray(z['cQ'], float)}))
        if not with_rsx:
            continue
        x = np.load(CD / 'arrays' / 'RSX' / (rid + '.npz'), allow_pickle=False)     # CD's port of rev_e1 (judged until the stop ends)
        if not np.array_equal(x['k'], z['k']):
            raise SystemExit('REFUSED: RSX and CV0 decision ticks differ for %s' % rid)
        runs[-1]['wr'] = L.clean_clear(x['clearX_' + KEY]) > 0.
    return runs


def load_old(stop):
    runs = C.load_runs()
    for r in runs:
        r['ev'] = r['ev'].astype(bool)
        r['crit'] = {'F0': r['crit']['F0'], 'E': r['crit']['E'], 'N': r['crit']['N'], 'NA': r['crit']['NA'], 'AM': r['crit']['A1'],
                     'CK3': r['crit']['CK3'], 'Q': r['crit']['Q']}
        r['masks'] = (r['ev'],)
        if stop == 'horizon':
            r['wr'] = L.clean_clear(r['cache'][KEY]) > 0.
        else:
            x = np.load(EXT / (r['run'] + '.npz'), allow_pickle=False)
            assert np.array_equal(x['k'], r['k'])
            r['wr'] = L.clean_clear(x['clearX_' + KEY]) > 0.
    return runs


def delays(runs):
    """One generator (default_rng(20261916)), runs in the run order, evaluated decisions in k order (as b6_stop_v01)."""
    d = S.draw_delays(int(sum(r['ev'].sum() for r in runs)))
    out = {}; pos = 0
    for r in runs:
        ev = np.flatnonzero(r['ev'])
        out[r['run']] = {int(i): 0.75 + float(x) for i, x in zip(ev, d[pos:pos + ev.size])}
        pos += ev.size
    return out


_SETUP = []


def clear_one(job):
    if not _SETUP:                               # worker processes import this module without __main__: set the stack up once
        env.setup(); _SETUP.append(1)
    rid, taus = job
    f = OUTF / 'clear' / (rid + '.npz')
    if f.exists():
        return rid, 'exists'
    t0 = time.time()
    z = np.load(CD / 'arrays' / 'CV0' / (rid + '.npz'), allow_pickle=False)
    rd, cap = fresh_paths(rid)
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import b_stop_ext_v02 as X                   # judged until the stop ends (A10 section 1)
    c = X.delayed_stop_clearance_ext(rd, cap, {int(k): v for k, v in taus.items()}, A=6.0)
    t = np.full(z['k'].size, np.nan)
    for di, v in taus.items():
        t[int(di)] = v
    f.parent.mkdir(parents=True, exist_ok=True)
    tmp = f.with_name(f.stem + '.partial.npz')
    np.savez_compressed(tmp, clear=c['clearX'], clear61=c['clear61'], tstop=c['tstop'], jend=c['jend'], late=c['late'], cens=c['cens'],
                        tau=t, k=z['k'])
    os.replace(tmp, f)
    return rid, 'ok %.1fs' % (time.time() - t0)


# ------------------------------------------------------------------------------------------------ scoring
def make_eval(GF, seed, nrows):
    """As b6_stop_v01.evaluate: the draw is boot_counts(len(runs), 20000, seed)[:nrows] for the run set evaluated (all runs, or a
    tercile's runs), so a tercile has its own draw over its own runs."""
    def evaluate(runs, safe_fn, names, with_boot=True):
        CNT = L.boot_counts(len(runs), 20000, seed)[:nrows]
        G = S.gridless(runs, ['F0', 'E'] + names + ['O'], safe_fn)
        p = S.rr_gl(G, 'F0', 'E', names + ['O'])
        out = dict(R_pp=p['R_pp'], R_deceq=p['R_deceq'], den0_deceq=p['D_deceq']['O'], RR={a: p['RR'][a] for a in names}, n=p['n'],
                   evaluable_den0=bool(p['D_deceq']['O'] >= 10.))
        b = None
        if with_boot:
            P = GF.Prepared(G, ['F0', 'E'] + names + ['O'], 0)
            parts = [GF.evaluate(P, CNT[s:s + 500]) for s in range(0, CNT.shape[0], 500)]
            b = dict(denE=np.concatenate([x['denE'] for x in parts]), n=np.concatenate([x['n'] for x in parts]),
                     D={a: np.concatenate([x['D'][a] for x in parts]) for a in names + ['O']})
            out['R_pp_ci'] = L.summ(b['denE'] / L.NLEV, p['R_pp'])['ci']
            out['den0_deceq_ci'] = L.pct(L.dec_eq(b['D']['O'], b['n']))
            out['RR_ci'] = {a: S.rr_summary(p, b, a)['ci'] for a in names}
        return out, b
    return evaluate


def reliance(runs, safe_key, arms=('N', 'NA', 'AM', 'CK3')):
    """revision_v12 a9_6_stop_reliance_v01 part (1), population all, with the stop scoring's safe set r[safe_key] (grid frontier)."""
    for r in runs:
        r['safe_x'] = {'est': r[safe_key]}; r['sel'] = {}
        r.setdefault('n_dec', int(r['ev'].size))
    X = C.tables(runs, ('X', 'est'), ['F0', 'E', 'O'] + list(arms))
    Tsum = {a: X[a].sum(axis=0)[:, 0, :] for a in X}
    cur = L.curves_w({a: Tsum[a] for a in Tsum if a != 'O'}, 0)
    cF0, wF0 = cur['F0']; cE, wE = cur['E']
    lev = L.levels_of(cF0, cE, cF0[0])
    n = float(Tsum['F0'][0, 0]); ent = dict(n=n)
    for a in ['F0', 'E'] + list(arms) + ['O']:
        only_stop = 0.; unsafe3 = 0.; unsafe_stop = 0.
        if a == 'O':
            for r in runs:
                m = r['masks'][0]; sx = r['safe_x']['est']; s1 = r['clear1'] > 0.
                sel = L.select_first_safe(sx, r['idx55'])[0]; ar = np.arange(sel.size)
                only_stop += float((m & ~s1[ar, sel] & sx[ar, sel]).sum()); unsafe3 += float((m & ~s1[ar, sel]).sum())
                unsafe_stop += float((m & ~sx[ar, sel]).sum())
            ent[a] = dict(share_safe_only_with_stop=only_stop / n, share_unsafe_3s=unsafe3 / n, share_unsafe_with_stop=unsafe_stop / n)
            continue
        f, ix = A9.frontier_argmin(cur[a][0], cur[a][1], lev)
        if a in ('F0', 'E'):
            cnt = np.bincount(ix[ix >= 0], minlength=len(C.GRID)).astype(float); cnt0 = 0.
        else:
            cnt0 = float((ix == 0).sum()); cnt = np.bincount(ix[ix >= 1] - 1, minlength=len(C.GRID)).astype(float)
        for r in runs:
            m = r['masks'][0]; sx = r['safe_x']['est']; s1 = r['clear1'] > 0.; ar = np.arange(r['n_dec'])
            sA = C.sel_of(r, a); sF = C.sel_of(r, 'F0')
            os_ = (~s1[ar[None, :], sA] & sx[ar[None, :], sA]) & m[None, :]
            u3 = (~s1[ar[None, :], sA]) & m[None, :]
            us = (~sx[ar[None, :], sA]) & m[None, :]
            only_stop += float(cnt @ os_.sum(axis=1)); unsafe3 += float(cnt @ u3.sum(axis=1)); unsafe_stop += float(cnt @ us.sum(axis=1))
            if cnt0:
                os0 = (~s1[ar, sF[0]] & sx[ar, sF[0]]) & m; u30 = (~s1[ar, sF[0]]) & m; us0 = (~sx[ar, sF[0]]) & m
                only_stop += cnt0 * float(os0.sum()); unsafe3 += cnt0 * float(u30.sum()); unsafe_stop += cnt0 * float(us0.sum())
        ent[a] = dict(share_safe_only_with_stop=only_stop / L.NLEV / n, share_unsafe_3s=unsafe3 / L.NLEV / n,
                      share_unsafe_with_stop=unsafe_stop / L.NLEV / n)
    for r in runs:
        r['sel'] = {}
    return ent


def score(test, stop):
    sys.path.insert(0, str(CDA))
    import gl_fast_v13 as GF
    t00 = time.time()
    if test:
        gate = 'TEST_OLD: old runs only; no fresh value'; runs = load_old(stop); capf = lambda x: old_cap(x)  # noqa: E731
        seed, nrows = 20261113, 2000; draw = 'first 2,000 rows of boot_counts(n, 20000, 20261113) per run set (as b6_stop_v01)'
        cdir = (HERE / 'out' / 'b6' / 'clear') if stop == 'horizon' else (OUTT / 'b6_clear_ext'); outd = OUTT
    else:
        if not LOCK2.is_file():
            raise SystemExit('REFUSED: LOCK_A10_2.txt does not exist (A10 sections 4, 5.2)')
        if stop != 'ext':
            raise SystemExit('REFUSED: fresh runs use the scoring of A10 section 1 (--stop ext) only')
        if not LOCK2C.is_file():
            raise SystemExit('REFUSED: LOCK_A10_2c.txt does not exist; no fresh value of B before it (coordinator, 20 Nov)')
        gate = 'LOCK_A10_2 sha256 %s; LOCK_A10_2c sha256 %s' % (sha(LOCK2), sha(LOCK2C)); runs = load_fresh(); capf = lambda x: fresh_paths(x)[1]  # noqa: E731
        if len(runs) != 105:
            raise SystemExit('REFUSED: %d runs' % len(runs))
        seed, nrows = SEED_FRESH, NBOOT_FRESH; draw = 'optA_lib_v02.boot_counts(n, 20000, 20261911) per run set (all 105, or a tercile), runs ascending'
        cdir = OUTF / 'clear'; outd = OUTF
    outd.mkdir(parents=True, exist_ok=True)
    evaluate = make_eval(GF, seed, nrows)
    doc = dict(code='b_fresh_b6_v02.py', gate=gate, status='descriptive (A10 section 5.7)' if not test else 'TEST on old runs', stop=stop,
               stop_scoring=('judged until the stop ends (A10 section 1; clearX)' if stop == 'ext' else '61 frames (B6 v01; test only)'),
               nboot=int(nrows), draw=draw, engine='CD_capture/analysis/gl_fast_v13.py sha256 ' + sha(CDA / 'gl_fast_v13.py'))
    ids = [r['run'] for r in runs]
    dec = [S.realised_decel(capf(x)) for x in ids]
    T3 = S.terciles(ids, dec)
    doc['realised_decel'] = dict(zip(ids, dec)); doc['terciles'] = []
    wr = lambda r: r['wr']                                          # noqa: E731
    boots = {}
    for ti, members in enumerate([ids] + T3):
        sub = [r for r in runs if r['run'] in members]
        for r in sub:
            r['sel'] = {}
        a_wr, b_wr = evaluate(sub, wr, ['N', 'CK3'])
        a_3s, b_3s = evaluate(sub, S.safe_w1, ['N', 'CK3'])
        dd = [d for x, d in zip(ids, dec) if x in members and d is not None]
        doc['terciles'].append(dict(name='all' if ti == 0 else 'tercile %d' % ti, runs=members, decel_min_max=[min(dd), max(dd)] if dd else None,
                                    W_R=a_wr, W1=a_3s, room_ratio_WR_over_3s=(a_wr['R_pp'] / a_3s['R_pp'] if a_3s['R_pp'] > 0 else None)))
        if ti == 0:
            boots['WR'] = b_wr; boots['W1'] = b_3s
        print('tercile', ti, round(a_wr['R_pp'], 4), round(a_3s['R_pp'], 4), round(time.time() - t00), flush=True)
    D = delays(runs)
    for r in runs:
        z = np.load(cdir / (r['run'] + '.npz'))
        if not np.array_equal(z['k'], r['k']):
            raise SystemExit('REFUSED: delayed-stop clearances of %s do not match k' % r['run'])
        ev = np.flatnonzero(r['ev'])
        if not np.allclose(z['tau'][ev], [D[r['run']][int(i)] for i in ev], rtol=0, atol=0):
            raise SystemExit('REFUSED: tau draw differs for %s' % r['run'])
        r['clear_delay'] = z['clear']; r['sel'] = {}
    dl = lambda r: L.clean_clear(r['clear_delay']) > 0.             # noqa: E731
    b_res, b_ds = evaluate(runs, dl, ['N', 'NA', 'AM', 'CK3', 'Q'])
    doc['delayed_stop'] = dict(rule='tau_i = 0.75 + U(0, 0.75), 6 m/s^2; default_rng(20261916)', **b_res)
    fixed, _ = evaluate(runs, wr, ['N', 'NA', 'AM', 'CK3', 'Q'], with_boot=False)
    doc['fixed_tau_0p75_point'] = fixed
    with np.errstate(invalid='ignore', divide='ignore'):
        ok = boots['W1']['denE'] > 0
        rs = np.where(ok, boots['WR']['denE'] / boots['W1']['denE'], np.nan); ds = np.where(ok, b_ds['denE'] / boots['W1']['denE'], np.nan)
    allw = doc['terciles'][0]
    doc['RS075_rel'] = L.summ(rs, allw['room_ratio_WR_over_3s'])
    doc['DS_rel'] = L.summ(ds, b_res['R_pp'] / allw['W1']['R_pp'] if allw['W1']['R_pp'] > 0 else np.nan)
    ev3 = [t for t in doc['terciles'][1:] if t['W_R']['evaluable_den0']]
    doc['tercile_rel_range'] = dict(evaluable=[t['name'] for t in ev3], relmin=min(t['room_ratio_WR_over_3s'] for t in ev3) if ev3 else None,
                                    relmax=max(t['room_ratio_WR_over_3s'] for t in ev3) if ev3 else None)
    doc['reliance'] = dict(scoring='W_R (the same safe set as RS075)', all=reliance(runs, 'wr'))
    tag = ('_testold' + ('' if stop == 'ext' else '_horizon')) if test else ''
    np.savez_compressed(outd / ('boot_b6%s.npz' % tag), WR=boots['WR']['denE'], W1=boots['W1']['denE'], DS=b_ds['denE'])
    if test and stop == 'horizon':
        doc['identity_vs_v01'] = check_v01(doc)
    if test:
        ext_runs = []
        for r in runs:
            x = np.load(EXT / (r['run'] + '.npz'), allow_pickle=False)
            assert np.array_equal(x['k'], r['k'])
            r['wr_ext'] = L.clean_clear(x['clearX_' + KEY]) > 0.
        rel_ext = reliance(runs, 'wr_ext', arms=('N', 'NA', 'AM', 'CK3'))
        rec = json.loads(A96.read_text(encoding='utf-8'))['reliance']['all']
        cmp = []
        for a, ra in (('F0', 'F0'), ('E', 'E'), ('N', 'N'), ('NA', 'NA'), ('AM', 'A1'), ('CK3', 'CK3'), ('O', 'O')):
            for k in ('share_safe_only_with_stop', 'share_unsafe_3s', 'share_unsafe_with_stop'):
                cmp.append((a, k, rel_ext[a][k], rec[ra][k]))
        doc['reliance_port_check_vs_v12_A9_6'] = dict(scoring='v11 extended clearance (as v12 A9-6)', compared=len(cmp),
                                                      identical=sum(1 for c in cmp if c[2] == c[3]),
                                                      differing=[c for c in cmp if c[2] != c[3]])
    doc['seconds'] = time.time() - t00; doc['written'] = time.strftime('%Y-%m-%d %H:%M:%S')
    (outd / ('B6_%s_v02.json' % (('TESTOLD' + ('' if stop == 'ext' else '_HORIZON')) if test else 'FRESH'))).write_text(json.dumps(doc, indent=1, default=float), encoding='utf-8')
    print(json.dumps(dict(RS075_rel=doc['RS075_rel'], DS_rel=doc['DS_rel'], terciles=[(t['name'], t['room_ratio_WR_over_3s'], t['W_R']['evaluable_den0'])
                                                                                     for t in doc['terciles']],
                          REL_F0=doc['reliance']['all']['F0']['share_safe_only_with_stop'],
                          identity=doc.get('identity_vs_v01'), rel_port=doc.get('reliance_port_check_vs_v12_A9_6', {}).get('identical'),
                          seconds=round(doc['seconds'])), default=float), flush=True)


def check_v01(doc):
    v1 = json.loads((HERE / 'out' / 'b6' / 'B6_STOP_v01.json').read_text(encoding='utf-8'))
    pairs = []
    for t, t1 in zip(doc['terciles'], v1['terciles']):
        pairs.append((t['name'] + '.runs', t['runs'], t1['runs'])); pairs.append((t['name'] + '.decel', t['decel_min_max'], t1['decel_min_max']))
        pairs.append((t['name'] + '.ratio', t['room_ratio_WR_over_3s'], t1['room_ratio_WR_over_3s']))
        for sc in ('W_R', 'W1'):
            for k in ('R_pp', 'R_deceq', 'den0_deceq', 'n', 'evaluable_den0', 'R_pp_ci', 'den0_deceq_ci', 'RR', 'RR_ci'):
                pairs.append(('%s.%s.%s' % (t['name'], sc, k), t[sc][k], t1[sc][k]))
    for k in ('R_pp', 'R_deceq', 'den0_deceq', 'n', 'evaluable_den0', 'R_pp_ci', 'den0_deceq_ci', 'RR', 'RR_ci'):
        pairs.append(('delayed_stop.' + k, doc['delayed_stop'][k], v1['delayed_stop'][k]))
        if k in v1['fixed_tau_0p75_point']:
            pairs.append(('fixed.' + k, doc['fixed_tau_0p75_point'][k], v1['fixed_tau_0p75_point'][k]))
    pairs.append(('realised_decel', doc['realised_decel'], v1['realised_decel']))
    bad = [(k, a, b) for k, a, b in pairs if json.dumps(a, default=float) != json.dumps(b, default=float)]
    return dict(compared=len(pairs), identical=len(pairs) - len(bad), differing=bad[:10])


def main():
    if ARGS.mode == 'clear':
        if ARGS.test_old:
            raise SystemExit('clear --test-old is not needed: the test reuses v01\'s clearances (out\\b6\\clear\\)')
        if not LOCK2.is_file():
            raise SystemExit('REFUSED: LOCK_A10_2.txt does not exist (A10 sections 4, 5.2)')
        runs = load_fresh(with_rsx=False)
        if len(runs) != 105:
            raise SystemExit('REFUSED: %d runs' % len(runs))
        D = delays(runs)
        from concurrent.futures import ProcessPoolExecutor
        t0 = time.time()
        with ProcessPoolExecutor(ARGS.workers) as ex:
            for rid, res in ex.map(clear_one, [(r['run'], D[r['run']]) for r in runs]):
                print('[%5.0f s] %s %s' % (time.time() - t0, rid, res), flush=True)
        return
    score(ARGS.test_old, ARGS.stop)


if __name__ == '__main__':
    main()
