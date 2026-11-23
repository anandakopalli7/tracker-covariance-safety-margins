"""Package E, set E6 (A13 §E6): first program. Closed-loop caution frontier under dropouts.

  main  (refuses unless revision_v13\\LOCK_A13a.txt exists; checks the E5 settings, mask table and P-bar_DR hashes):
        collects E5's e5_ runs (N at g_N, F0D4 at g = 4) and E6's e6_ runs (F0D8, F0D16), latest attempt per job; validity as
        E5 (e5_analyse_v01.mask_check) plus the locked g of each arm label; the primary (A13 §E6.5): sets K and T, frontier
        points, Delta = c_N - c_F0(t_N) by linear interpolation between the bracketing F0 scales, case bootstrap
        default_rng(20261922) x 20,000 with NaN resamples, one-sided p = (1 + #{D* >= 0 or NaN}) / 20,001, ub95 and the 95 %
        interval over the finite resamples; the secondary (§E6.6): E's compare for N vs F0D8 and N vs F0D16, per-arm summaries.
        Writes out\\OUTCOMES_E6_v01.json, out\\E6_RESULTS_v01.json, out\\A_EXPORT_E6.json (the 65 keys of §E6.8). Never overwrites.

python -I -B e6_analyse_v01.py main
"""
import datetime, hashlib, json, math, pathlib, statistics, sys

import numpy as np

E = pathlib.Path(__file__).resolve().parents[1]
REV = E.parents[1]
LOCK = REV / 'LOCK_A13a.txt'
OUT = E / 'out'
KEYS = E / 'tests' / 'out' / 'E6_EXPORT_KEYS_v01.json'
sys.path.insert(0, str(E / 'analysis')); sys.path.insert(0, str(E / 'src_v05'))
import e5_analyse_v01 as E5A        # noqa: E402  (mask_check, collect, PBAR_V05, MASKS, SETTINGS, summaries' definitions)
import e3_analyse_v01 as EA         # noqa: E402  (compare, SEED, NBOOT)

LABELS = ('N', 'F0D4', 'F0D8', 'F0D16')
SEED, NBOOT = 20261922, 20000
assert SEED == EA.SEED and NBOOT == EA.NBOOT


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def label_of(r, g_N):
    """Arm label and its locked g from (prefix, arm, job suffix); None if the job is not an E6 study job."""
    j, arm = r['job'], r['arm']
    if j.startswith('e5_') and arm == 'E_N' and j.endswith('_e_n'): return 'N', g_N
    if j.startswith('e5_') and arm == 'E_F0' and j.endswith('_e_f0'): return 'F0D4', 4.
    if j.startswith('e6_') and arm == 'E_F0' and j.endswith('_e_f0_g8'): return 'F0D8', 8.
    if j.startswith('e6_') and arm == 'E_F0' and j.endswith('_e_f0_g16'): return 'F0D16', 16.
    return None, None


def delta_of(c, t):
    """c, t: arrays (4, ...) in LABELS order. Returns (Delta, ok, lo_is_4, w, cF). NaN where undefined (§E6.5 steps 1-3)."""
    cN, c4, c8, c16 = c; tN, t4, t8, t16 = t
    with np.errstate(invalid='ignore', divide='ignore'):
        fin = np.isfinite(tN) & np.isfinite(t4) & np.isfinite(t8) & np.isfinite(t16)
        mono = fin & (t4 < t8) & (t8 < t16)
        ok = mono & (tN >= t4) & (tN <= t16)
        lo4 = tN <= t8
        tlo = np.where(lo4, t4, t8); thi = np.where(lo4, t8, t16); clo = np.where(lo4, c4, c8); chi = np.where(lo4, c8, c16)
        w = (tN - tlo) / (thi - tlo); cF = clo + w * (chi - clo); D = cN - cF
    D = np.where(ok, D, np.nan)
    return D, ok, lo4, w, cF


def status_of(c, t, nT):
    tN, t4, t8, t16 = t
    if nT == 0: return 'no common no-contact case'
    if not (t4 < t8 < t16): return 'non-monotone'
    if tN < t4 or tN > t16: return 'not bracketed'
    return 'bracketed 4-8' if tN <= t8 else 'bracketed 8-16'


def primary(sel):
    """sel: {label: {case: record}} of valid runs. Implements §E6.5 exactly."""
    K = sorted(set.intersection(*[set(sel[a]) for a in LABELS]))
    n = len(K)
    C = np.array([[float(int(sel[a][k]['outcomes']['contact'])) for k in K] for a in LABELS], float).reshape(4, n)
    inT = np.array([all(int(sel[a][k]['outcomes']['contact']) == 0 for a in LABELS) for k in K], bool)
    TL = np.array([[float(sel[a][k]['outcomes']['time_lost_s']) if inT[i] else 0. for i, k in enumerate(K)] for a in LABELS], float).reshape(4, n)
    nT = int(inT.sum())
    res = dict(K=K, n=n, nT=nT)
    if n == 0:
        # §E6.5: K empty -> every resample is NaN: p = 20,001 / 20,001 = 1, finite share 0, ub95 and the interval null
        res.update(status='no common no-contact case', c=[None] * 4, t=[None] * 4, delta=None, cF=None, p_one=1.0, ub95=None, ci=None, finite_share=0.0, pass_alone=False)
        return res
    c = C.mean(axis=1)
    t = TL[:, inT].mean(axis=1) if nT else np.full(4, np.nan)
    st = status_of(c, t, nT)
    D, ok, lo4, w, cF = delta_of(c, t)
    full_ok = bool(ok) and st.startswith('bracketed')
    idx = np.random.default_rng(SEED).integers(0, n, (NBOOT, n))
    Cb = C[:, idx].mean(axis=2)                                   # (4, B)
    W = inT[idx]                                                  # (B, n)
    cnt = W.sum(axis=1)                                           # (B,)
    with np.errstate(invalid='ignore', divide='ignore'):
        Tb = (TL[:, idx] * W[None, :, :]).sum(axis=2) / np.where(cnt > 0, cnt, np.nan)[None, :]
    Db, _, _, _, _ = delta_of(Cb, Tb)
    bad = ~np.isfinite(Db)
    p_one = float((1 + int(np.sum(bad | (np.where(bad, 0., Db) >= 0.)))) / (NBOOT + 1))
    fin = Db[~bad]
    ub95 = float(np.quantile(fin, 0.95)) if fin.size else None
    ci = [float(np.quantile(fin, 0.025)), float(np.quantile(fin, 0.975))] if fin.size else None
    res.update(status=st, c=[float(x) for x in c], t=[float(x) if np.isfinite(x) else None for x in t],
               delta=float(D) if full_ok else None, cF=float(cF) if full_ok else None, w=float(w) if full_ok else None,
               p_one=p_one, ub95=ub95, ci=ci, finite_share=float(fin.size / NBOOT),
               pass_alone=bool(full_ok and ub95 is not None and ub95 < 0.))
    return res


def summaries(sel_runs):
    v = {}
    for k, ok in E5A.MEAN.items():
        xs = [float(r['outcomes'][ok]) for r in sel_runs if r['outcomes'][ok] is not None]; v[k] = sum(xs) / len(xs) if xs else None
    for k, ok in E5A.MEDIAN.items():
        xs = [float(r['outcomes'][ok]) for r in sel_runs if r['outcomes'][ok] is not None]; v[k] = float(statistics.median(xs)) if xs else None
    nd = sum(int(r['outcomes']['decisions'] or 0) for r in sel_runs)
    v['fallback'] = sum(int(r['outcomes']['fallback_decisions'] or 0) for r in sel_runs) / nd if nd else None
    ms = [r['masked_share'] for r in sel_runs if r['masked_share'] is not None]; v['masked'] = sum(ms) / len(ms) if ms else None
    return v


def clean(x):
    if isinstance(x, list):
        y = [clean(z) for z in x]; return None if all(z is None for z in y) else y
    if isinstance(x, float) and not math.isfinite(x): return None
    return x


def main_stage():
    if not LOCK.exists(): raise SystemExit('REFUSED: LOCK_A13a.txt does not exist')
    paths = dict(o=OUT / 'OUTCOMES_E6_v01.json', r=OUT / 'E6_RESULTS_v01.json', x=OUT / 'A_EXPORT_E6.json')
    for p in paths.values(): assert not p.exists(), f'{p.name} exists; never overwrite'
    s = json.loads(E5A.SETTINGS.read_text(encoding='utf-8')); m = json.loads(E5A.MASKS.read_text(encoding='utf-8'))
    if s['masks_sha256'] != sha(E5A.MASKS) or s.get('pbar_dr_sha256') != sha(E5A.PBAR_V05):
        raise SystemExit('REFUSED: the mask table or P-bar_DR differs from the hashes in E5_SETTINGS_v01.json')
    g_N = float(s['g_N'])
    recs = E5A.collect('e5_', expect={'E_F0': 4., 'E_N': g_N}) + E5A.collect('e6_')     # e6_: g checked against the label below
    main_cases = set(m['main_cases'])
    for r in recs:
        lab, g = label_of(r, g_N)
        r['label'] = lab; r['level'] = lab
        if lab is None or r['case'] not in main_cases:
            r['valid'] = False; r['reasons'] = list(r.get('reasons') or []) + ['not an E6 study job']
        elif r.get('g') is None or float(r['g']) != g:
            r['valid'] = False; r['reasons'] = list(r.get('reasons') or []) + [f'g differs from the locked g of {lab}']
    want = {f'e5_{c}_e_f0' for c in main_cases} | {f'e5_{c}_e_n' for c in main_cases} | {f'e6_{c}_e_f0_g8' for c in main_cases} | {f'e6_{c}_e_f0_g16' for c in main_cases}
    have = {r['job'] for r in recs}
    paths['o'].write_text(json.dumps(dict(schema='E6_OUTCOMES_V01', code='e6_analyse_v01.py', n_jobs=len(recs), n_valid=sum(bool(r['valid']) for r in recs),
                                          missing=sorted(want - have), runs=recs), indent=1, allow_nan=False), encoding='utf-8')
    sel = {a: {r['case']: r for r in recs if r['label'] == a and r['valid']} for a in LABELS}
    P = primary(sel)
    v = {'E6.status': 'ran', 'E6.n_cases': P['n'], 'E6.n_nocontact_all': P['nT']}
    for i, a in enumerate(LABELS):
        v[f'E6.pt.{a}.c'] = P['c'][i]; v[f'E6.pt.{a}.t'] = P['t'][i]
    v.update({'E6.bracket': P['status'], 'E6.c_F0_at_tN': P['cF'], 'E6.delta': P['delta'], 'E6.delta.ub95': P['ub95'], 'E6.delta.ci': P['ci'],
              'E6.finite_share': P['finite_share'], 'E6.p_one': P['p_one'], 'E6.pass_alone': P['pass_alone']})
    for a in LABELS:
        sm = summaries([r for r in recs if r['label'] == a and r['valid']])
        for k in ('contact', 'vimp', 'tlost', 'restgap', 'peakdec', 'jerk', 'fallback', 'masked'): v[f'E6.{a}.{k}'] = sm[k]
    comps = {}
    for sc, lab in (('8', 'F0D8'), ('16', 'F0D16')):
        c = EA.compare(recs, 'E_N', 'E_F0', 'N', lab); comps[sc] = c
        v[f'E6.s{sc}.dc'] = c['contact'].get('diff'); v[f'E6.s{sc}.dc.ci'] = [c['contact'].get('lo'), c['contact'].get('hi')]
        v[f'E6.s{sc}.mcnemar_p'] = c['contact'].get('mcnemar_exact_p') if c['pairs'] else None; v[f'E6.s{sc}.dt'] = c['time_lost']['mean']   # §E6.6: no pairs -> null
        v[f'E6.s{sc}.dt.ci'] = [c['time_lost']['lo'], c['time_lost']['hi']]; v[f'E6.s{sc}.class'] = c['classification']; v[f'E6.s{sc}.pairs'] = c['pairs']
    v = {k: clean(x) for k, x in v.items()}
    keys = json.loads(KEYS.read_text(encoding='utf-8'))['keys']
    assert sorted(v) == sorted(keys) and len(v) == 65, sorted(set(v) ^ set(keys))
    v = {k: v[k] for k in keys}
    paths['r'].write_text(json.dumps(dict(schema='E6_RESULTS_V01', primary={k: x for k, x in P.items()}, secondary=comps), indent=1, allow_nan=True, default=str), encoding='utf-8')
    doc = dict(package='E', set='E6', written=datetime.datetime.now().astimezone().isoformat(), program='e6_analyse_v01.py', program_sha256=sha(__file__),
               lock_sha256=sha(LOCK), values=v)
    paths['x'].write_text(json.dumps(doc, indent=1, allow_nan=False), encoding='utf-8')
    print(json.dumps(dict(runs=len(recs), valid=sum(bool(r['valid']) for r in recs), missing=len(want - have), K=P['n'], T=P['nT'], bracket=P['status'],
                          delta=v['E6.delta'], ub95=v['E6.delta.ub95'], p_one=v['E6.p_one'], pass_alone=v['E6.pass_alone'], keys=len(v))))


if __name__ == '__main__':
    {'main': main_stage}[sys.argv[1]]()
