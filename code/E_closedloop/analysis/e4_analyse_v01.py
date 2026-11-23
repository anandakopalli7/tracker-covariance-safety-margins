"""Package E, set E4 (A11 §6d, closed-loop detection dropout): first program. Collects the E4 runs, checks each run's mask against
the pre-registered law, runs the §6d.5 comparisons with E3's frozen statistics (e3_analyse_v01: Newcombe method 10 with the
corrected phi, exact McNemar, case bootstrap default_rng(20261922) x 20,000, E's classes), the exploratory E3-twin analysis, and
writes the E4 export for A.

Gate: refuses unless revision_v13\\LOCK_A11b.txt exists (§6d locked before any E4 run).
Stages: L (lo) and H (hi) are analysed independently; a level is 'complete' when all 240 of its jobs have a valid-or-invalid
run of record (every job ran). E4.H.completed = H complete (if not, no H value is exported: §6d.4, no partial H).

python -I -B e4_analyse_v01.py --punish-num N --out-dir out [--e3-outcomes out\\OUTCOMES_E3_v01.json]
Writes out\\OUTCOMES_E4_v01.json, out\\E4_RESULTS_v01.json, out\\A_EXPORT_E4.json (never overwrites).

Export keys (values unrounded; intervals [lo, hi] or null when undefined; shares as fractions):
  E4.status ('ran'), E4.punish_num, E4.n_cases, E4.L.completed, E4.H.completed
  E4.<A>.<lev>.<contact|vimp|tlost|restgap|peakdec|jerk|fallback|masked>   A in F0, N, F0IMM, NIMM (E3 export summaries:
        contact share; median impact speed; mean time lost; mean rest gap; median peak decel; median RMS jerk; fallback pooled
        over decisions; masked = mean over runs of the share of the run's detector updates at k >= 99 that were masked)
  E4.<A>.<lev>.caution   design caution % at the locked point (LOCK_A10_2b; no dropouts): F0 = F0_caution_pct; others caution_pct
  E4.<C>.<lev>.dc / .dc.ci / .dt / .dt.ci / .d_<vimp|restgap|peakdec|jerk|fallback> / .d_<..>.ci / .class    C in N (vs F0), NIMM (vs F0IMM)
  E4H1 = E4.N.lo.class, E4H2 = E4.NIMM.lo.class
  exploratory: E4.deg.<A>.<lev>.dc / .dc.ci / .dt / .dt.ci   (E4 run minus its E3 twin, same case / arm / level)
               E4.did.<C>.<lev>.dc / .dc.ci   (mean over cases of [(C - ref) in E4] - [(C - ref) in E3], contact; case bootstrap)
"""
import argparse, datetime, hashlib, json, math, pathlib, statistics, sys

import numpy as np

E = pathlib.Path(__file__).resolve().parents[1]
REV = E.parents[1]
LOCK = REV / 'LOCK_A11b.txt'
MASKS = E / 'out' / 'E4_MASKS_v01.json'     # the locked 60-case mask table (hash in LOCK_A11b): the known answer
sys.path.insert(0, str(E / 'analysis')); sys.path.insert(0, str(E / 'src_v04'))
import e_collect_v01 as EC          # noqa: E402  (frozen; one(run_dir) -> record with validity and outcomes)
import e3_analyse_v01 as EA         # noqa: E402  (frozen statistics)
import e_dropout_v01 as D           # noqa: E402  (the law, packet v04 copy)

ARM = {'E_F0': 'F0', 'E_N': 'N', 'E_F0_IMM': 'F0IMM', 'E_N_IMM': 'NIMM'}
COMP = (('E_N', 'E_F0', 'N'), ('E_N_IMM', 'E_F0_IMM', 'NIMM'))
HYP = {('N', 'lo'): 'E4H1', ('NIMM', 'lo'): 'E4H2'}
MEAN = {'contact': 'contact', 'tlost': 'time_lost_s', 'restgap': 'rest_gap_m'}
MEDIAN = {'vimp': 'impact_speed_mps', 'peakdec': 'peak_decel_mps2', 'jerk': 'rms_jerk_mps3'}
PAIRED = {'vimp': 'impact_speed_mps', 'restgap': 'rest_gap_m', 'peakdec': 'peak_decel_mps2', 'jerk': 'rms_jerk_mps3', 'fallback': 'fallback_share'}
MATCH = {'E_N': 'N', 'E_F0_IMM': 'F0_IMM', 'E_N_IMM': 'N_IMM'}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def jl(p):
    with open(p, encoding='utf-8') as f:
        return [json.loads(x) for x in f if x.strip()]


def defined(xs):
    return [float(x) for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]


def mask_check(run_dir, punish):
    """(ok, reasons, masked_share): ARM_METHOD dropout record = the law for the case; every detector tick's masked flag and
    tracker input follow it; the run's punish_num is the pre-registered one."""
    caps = list((run_dir / 'x' / run_dir.name / 'capture').glob('*'))
    if len(caps) != 1: return False, ['no capture folder'], None
    cap = caps[0]; reasons = []
    m = json.loads((cap / 'ARM_METHOD_v01.json').read_text(encoding='utf-8')).get('dropout')
    cid = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))['case']['id']
    if m is None: return False, ['no dropout record'], None
    mask, windows = D.mask_for_case(cid, m['n_updates'])
    if m['case_id'] != cid or m['mask'] != [int(x) for x in mask] or m['windows'] != [list(w) for w in windows]: reasons.append('mask differs from the law')
    known = json.loads(MASKS.read_text(encoding='utf-8'))
    if m.get('law') != known['law'] or m.get('law_file_sha256') != known['law_file_sha256']: reasons.append('law id or law file differs from the locked mask table')
    kc = known['cases'].get(cid)
    if kc is None or ''.join(str(int(x)) for x in m['mask']) != kc['mask'][:len(m['mask'])] or m['windows'] != kc['windows']: reasons.append('mask differs from the locked mask table')
    if int(m['punish_num']) != int(punish): reasons.append('punish_num %s is not the pre-registered %s' % (m['punish_num'], punish))
    det = jl(cap / 'detections.jsonl'); win = [r for r in det if r['k'] >= 99]
    for r in det:
        i = D.tick_index(r['k'])
        if bool(r.get('masked')) != bool(mask[i]) or r.get('tracker_rows') != (0 if mask[i] else len(r['model'])):
            reasons.append('tick %d does not follow the mask' % r['k']); break
    share = (sum(bool(mask[D.tick_index(r['k'])]) for r in win) / len(win)) if win else None
    return not reasons, reasons, share


def collect(punish):
    runs = sorted(d for d in (E / 'runs').glob('e4_*') if (d / 'SUMMARY.json').exists())
    by_job = {}
    for d in runs: by_job.setdefault(EC.base_id(d.name), []).append(d)
    recs = []
    for job, ds in sorted(by_job.items()):
        d = sorted(ds, key=lambda x: EC.attempt_of(x.name))[-1]
        r = EC.one(d)
        ok, why, share = mask_check(d, punish) if r.get('reasons') != ['no capture folder'] else (False, ['no capture folder'], None)
        if not ok:
            r['valid'] = False; r['reasons'] = list(r.get('reasons') or []) + why
        r['masked_share'] = share; r['attempts'] = len(ds)
        recs.append(r)
    return recs


def jobs_expected():
    out = {}
    for lv, st in (('lo', 'E4L'), ('hi', 'E4H')):
        ids = []
        for f in sorted((E / 'jobs').glob(f'JOBS_{st}_*_v01.json')):
            ids += [j['id'] for j in json.loads(f.read_text(encoding='utf-8'))['jobs'] if j['id'].startswith('e4_')]
        out[lv] = ids
    return out


def boot_mean_cases(vals):
    """Mean over cases and the case-bootstrap 95% interval (fresh default_rng(20261922), 20,000 resamples of the cases)."""
    x = np.asarray(vals, float); n = len(x)
    if n < 2: return dict(n=n, mean=float(x.mean()) if n else None, lo=None, hi=None)
    idx = np.random.default_rng(EA.SEED).integers(0, n, (EA.NBOOT, n))
    bm = x[idx].mean(axis=1)
    return dict(n=n, mean=float(x.mean()), lo=float(np.percentile(bm, 2.5)), hi=float(np.percentile(bm, 97.5)))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--punish-num', type=int, required=True); ap.add_argument('--out-dir', default=str(E / 'out'))
    ap.add_argument('--e3-outcomes', default=str(E / 'out' / 'OUTCOMES_E3_v01.json'))
    a = ap.parse_args()
    if not LOCK.exists(): raise SystemExit('REFUSED: LOCK_A11b.txt does not exist')
    out = pathlib.Path(a.out_dir)
    paths = dict(o=out / 'OUTCOMES_E4_v01.json', r=out / 'E4_RESULTS_v01.json', x=out / 'A_EXPORT_E4.json')
    for p in paths.values(): assert not p.exists(), f'{p.name} exists; never overwrite'
    recs = collect(a.punish_num)
    exp = jobs_expected(); have = {r['job'] for r in recs}
    complete = {lv: bool(exp[lv]) and all(j in have for j in exp[lv]) for lv in ('lo', 'hi')}
    paths['o'].write_text(json.dumps(dict(schema='E4_OUTCOMES_V01', code='e4_analyse_v01.py', punish_num=a.punish_num, complete=complete,
                                          n_jobs=len(recs), n_valid=sum(r['valid'] for r in recs), runs=recs), indent=1, allow_nan=False), encoding='utf-8')
    e3 = [r for r in json.loads(pathlib.Path(a.e3_outcomes).read_text(encoding='utf-8'))['runs'] if r['arm'] in ARM]
    m = json.loads((E / 'out' / 'E2_MATCHED_v01.json').read_text(encoding='utf-8'))
    res = dict(schema='E4_RESULTS_V01', code='e4_analyse_v01.py', punish_num=a.punish_num, complete=complete, comparisons=[], degradation=[], did=[])
    v = {'E4.status': 'ran', 'E4.punish_num': a.punish_num, 'E4.n_cases': len({r['case'] for r in recs}), 'E4.L.completed': complete['lo'], 'E4.H.completed': complete['hi']}
    for lv in ('lo', 'hi'):
        if not complete[lv]: continue
        rows = [r for r in recs if r['level'] == lv]
        for arm, ak in ARM.items():
            sel = [r for r in rows if r['arm'] == arm and r['valid']]
            if not sel: continue
            for k, ok in MEAN.items():
                xs = defined([r['outcomes'][ok] for r in sel]); v[f'E4.{ak}.{lv}.{k}'] = sum(xs) / len(xs) if xs else None
            for k, ok in MEDIAN.items():
                xs = defined([r['outcomes'][ok] for r in sel]); v[f'E4.{ak}.{lv}.{k}'] = float(statistics.median(xs)) if xs else None
            nd = sum(int(r['outcomes']['decisions'] or 0) for r in sel)
            v[f'E4.{ak}.{lv}.fallback'] = sum(int(r['outcomes']['fallback_decisions'] or 0) for r in sel) / nd if nd else None
            ms = defined([r['masked_share'] for r in sel]); v[f'E4.{ak}.{lv}.masked'] = sum(ms) / len(ms) if ms else None
            st = m['settings'][lv]
            v[f'E4.{ak}.{lv}.caution'] = st['F0_caution_pct'] if arm == 'E_F0' else st['arms'][MATCH[arm]]['caution_pct']
        for arm, ref, ck in COMP:
            c = EA.compare(rows, arm, ref, lv, lv); c['class'] = c.pop('classification'); c['hypothesis'] = HYP.get((ck, lv)); c['level'] = lv
            res['comparisons'].append(c)
            pre = f'E4.{ck}.{lv}'
            v[pre + '.dc'] = c['contact'].get('diff'); v[pre + '.dc.ci'] = [c['contact'].get('lo'), c['contact'].get('hi')]
            v[pre + '.dt'] = c['time_lost']['mean']; v[pre + '.dt.ci'] = [c['time_lost']['lo'], c['time_lost']['hi']]
            for k, ok in PAIRED.items():
                pdf = c['descriptive'][ok]['paired_diff']; v[f'{pre}.d_{k}'] = pdf['mean']; v[f'{pre}.d_{k}.ci'] = [pdf['lo'], pdf['hi']]
            v[pre + '.class'] = c['class']
            if c['hypothesis']: v[c['hypothesis']] = c['class']
        # exploratory: E4 run minus its E3 twin (same case, arm, level)
        for arm, ak in ARM.items():
            t = [dict(r, arm='X4') for r in rows if r['arm'] == arm] + [dict(r, arm='X3') for r in e3 if r['arm'] == arm and r['level'] == lv]
            c = EA.compare(t, 'X4', 'X3', lv, lv); c['arm_name'] = ak; c['level'] = lv; res['degradation'].append(c)
            pre = f'E4.deg.{ak}.{lv}'
            v[pre + '.dc'] = c['contact'].get('diff'); v[pre + '.dc.ci'] = [c['contact'].get('lo'), c['contact'].get('hi')]
            v[pre + '.dt'] = c['time_lost']['mean']; v[pre + '.dt.ci'] = [c['time_lost']['lo'], c['time_lost']['hi']]
        for arm, ref, ck in COMP:
            def tab(src, a_):
                return {r['case']: r for r in src if r['arm'] == a_ and r['level'] == lv and r['valid']}
            A4, R4, A3, R3 = tab(rows, arm), tab(rows, ref), tab(e3, arm), tab(e3, ref)
            cases = sorted(set(A4) & set(R4) & set(A3) & set(R3))
            d = [(int(A4[c]['outcomes']['contact']) - int(R4[c]['outcomes']['contact'])) - (int(A3[c]['outcomes']['contact']) - int(R3[c]['outcomes']['contact'])) for c in cases]
            b = boot_mean_cases(d); b.update(comparison=ck, level=lv); res['did'].append(b)
            v[f'E4.did.{ck}.{lv}.dc'] = b['mean']; v[f'E4.did.{ck}.{lv}.dc.ci'] = [b['lo'], b['hi']]
    def clean(x):
        if isinstance(x, list):
            y = [clean(z) for z in x]; return None if all(z is None for z in y) else y
        if isinstance(x, float) and not math.isfinite(x): return None
        return x
    v = {k: clean(x) for k, x in v.items()}
    paths['r'].write_text(json.dumps(res, indent=1, allow_nan=True, default=str), encoding='utf-8')
    doc = dict(package='E', set='E4', written=datetime.datetime.now().astimezone().isoformat(), program='e4_analyse_v01.py', program_sha256=sha(__file__),
               lock_sha256=sha(LOCK), values=v)
    paths['x'].write_text(json.dumps(doc, indent=1, allow_nan=False), encoding='utf-8')
    print(json.dumps(dict(complete=complete, runs=len(recs), valid=sum(r['valid'] for r in recs), keys=len(v),
                          classes={k: v[k] for k in v if k.endswith('.class')})))


if __name__ == '__main__':
    main()
