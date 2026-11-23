"""Package E, set E5 (A12 §6): first program.

  cal   (A12 §6.4–6.5; design data): collects the e5c_ runs; validity as E4 (status, policy failure, no early contact) plus the
        mask = law = locked table E5_MASKS_v01.json, law A11D2, law file, punish_num 3; contact share per g over valid runs;
        g_D = the g nearest 0.20 (ties: smaller; all shares < 0.05 -> g_D = 4, low_power); g_N, cautions = the row of g_D in
        out\\E5_MATCH_TABLE_v01.json. Writes out\\E5_CAL_v01.json and out\\E5_SETTINGS_v01.json (the file LOCK_A12b records).
  main  (A12 §6.7; refuses unless revision_v13\\LOCK_A12b.txt exists and records E5_SETTINGS_v01.json's SHA-256): collects the
        e5_ runs (same validity); the primary comparison N vs F0_D paired by case (e3_analyse_v01.compare: Newcombe, exact McNemar,
        case bootstrap default_rng(20261922) x 20,000, E's classes); the one-sided bootstrap p (share of resamples with mean paired
        contact difference N - F0_D >= 0, same index matrix); writes out\\OUTCOMES_E5_v01.json, out\\E5_RESULTS_v01.json,
        out\\A_EXPORT_E5.json (keys of A12 §6.9). Never overwrites.

python -I -B e5_analyse_v01.py cal   |   python -I -B e5_analyse_v01.py main
"""
import datetime, fractions, hashlib, json, math, pathlib, statistics, sys

import numpy as np

E = pathlib.Path(__file__).resolve().parents[1]
REV = E.parents[1]
LOCK_B = REV / 'LOCK_A12b.txt'
OUT = E / 'out'
MASKS = OUT / 'E5_MASKS_v01.json'
TABLE = OUT / 'E5_MATCH_TABLE_v01.json'
SETTINGS = OUT / 'E5_SETTINGS_v01.json'
sys.path.insert(0, str(E / 'analysis')); sys.path.insert(0, str(E / 'src_v05'))
import e_collect_v01 as EC          # noqa: E402
import e3_analyse_v01 as EA         # noqa: E402
import e_dropout_v01 as D           # noqa: E402
CAL_G = (4., 8., 16., 32.)
PBAR_V05 = E / 'src_v05' / 'E_PBAR_CANMOT_v01.json'      # P-bar_DR (F0_D); review M1: every F0_D run must carry its hash
MEAN = {'contact': 'contact', 'tlost': 'time_lost_s', 'restgap': 'rest_gap_m'}
MEDIAN = {'vimp': 'impact_speed_mps', 'peakdec': 'peak_decel_mps2', 'jerk': 'rms_jerk_mps3'}
PAIRED = {'vimp': 'impact_speed_mps', 'restgap': 'rest_gap_m', 'peakdec': 'peak_decel_mps2', 'jerk': 'rms_jerk_mps3', 'fallback': 'fallback_share'}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def jl(p):
    with open(p, encoding='utf-8') as f:
        return [json.loads(x) for x in f if x.strip()]


def mask_check(run_dir, known, expect=None):
    caps = list((run_dir / 'x' / run_dir.name / 'capture').glob('*'))
    if len(caps) != 1: return False, ['no capture folder'], None
    cap = caps[0]; reasons = []
    if not (cap / 'ARM_METHOD_v01.json').exists(): return False, ['no method record'], None
    meth = json.loads((cap / 'ARM_METHOD_v01.json').read_text(encoding='utf-8'))
    # review M1: the run's arm, tracker, g and (F0_D) P-bar must be the job's and the packet v05 P-bar_DR
    summ = json.loads((run_dir / 'SUMMARY.json').read_text(encoding='utf-8')); ej = summ.get('e_job') or {}
    if meth.get('tracker') != 'CANMOT' or meth.get('arm') != summ.get('arm') or meth.get('arm') not in ('E_F0', 'E_N'): reasons.append('arm or tracker differs from the job')
    if ej.get('g') is None or float((meth.get('knobs') or {}).get('g')) != float(ej['g']): reasons.append('method g differs from the job g')
    if meth.get('arm') == 'E_F0' and meth.get('pbar_sha256') != sha(PBAR_V05): reasons.append('F0 P-bar is not P-bar_DR (packet v05)')
    if expect is not None and float((meth.get('knobs') or {}).get('g')) != float(expect.get(meth.get('arm'), float('nan'))): reasons.append('method g differs from the locked setting')
    m = meth.get('dropout')
    cid = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))['case']['id']
    if m is None: return False, ['no dropout record'], None
    mask, windows = D.mask_for_case(cid, m['n_updates'])
    if m['case_id'] != cid or m['mask'] != [int(x) for x in mask] or m['windows'] != [list(w) for w in windows]: reasons.append('mask differs from the law')
    if m.get('law') != known['law'] or m.get('law_file_sha256') != known['law_file_sha256'] or int(m['punish_num']) != 3: reasons.append('law, law file or punish_num differs')
    kc = known['cases'].get(cid)
    if kc is None or ''.join(str(int(x)) for x in m['mask']) != kc['mask'][:len(m['mask'])] or m['windows'] != kc['windows']: reasons.append('mask differs from the locked table')
    det = jl(cap / 'detections.jsonl')
    for r in det:
        i = D.tick_index(r['k'])
        if bool(r.get('masked')) != bool(mask[i]) or r.get('tracker_rows') != (0 if mask[i] else len(r['model'])): reasons.append('tick %d does not follow the mask' % r['k']); break
    win = [r for r in det if r['k'] >= 99]
    return not reasons, reasons, ((sum(bool(mask[D.tick_index(r['k'])]) for r in win) / len(win)) if win else None)


def collect(prefix, expect=None):
    known = json.loads(MASKS.read_text(encoding='utf-8'))
    by = {}
    for d in sorted(x for x in (E / 'runs').glob(prefix + '*') if (x / 'SUMMARY.json').exists()):
        by.setdefault(EC.base_id(d.name), []).append(d)
    recs = []
    for job, ds in sorted(by.items()):
        d = sorted(ds, key=lambda x: EC.attempt_of(x.name))[-1]; r = EC.one(d)
        ok, why, share = mask_check(d, known, expect)
        if not ok: r['valid'] = False; r['reasons'] = list(r.get('reasons') or []) + why
        r['masked_share'] = share; recs.append(r)
    return recs


def cal():
    for p in (OUT / 'E5_CAL_v01.json', SETTINGS): assert not p.exists(), f'{p.name} exists; never overwrite'
    recs = collect('e5c_')
    shares = {}
    for g in CAL_G:
        v = [r for r in recs if r['valid'] and abs(float(r['g']) - g) < 1e-12]
        shares[g] = dict(n_valid=len(v), contacts=sum(int(r['outcomes']['contact']) for r in v), share=(sum(int(r['outcomes']['contact']) for r in v) / len(v)) if v else None)
    sh = [shares[g]['share'] for g in CAL_G]
    low = all(s is not None and s < 0.05 for s in sh)
    if low: gD = 4.
    else:
        # review M2: exact distance |contacts/n - 1/5| = |5 contacts - n| / (5 n) as a Fraction; first minimum = smaller g
        dist = [fractions.Fraction(abs(5 * shares[g]['contacts'] - shares[g]['n_valid']), 5 * shares[g]['n_valid']) if shares[g]['n_valid'] else None for g in CAL_G]
        best = min(x for x in dist if x is not None); gD = CAL_G[dist.index(best)]
    t = json.loads(TABLE.read_text(encoding='utf-8')); row = [x for x in t['candidates'] if x['g_D'] == gD][0]
    doc = dict(schema='E5_CAL_V01', code='e5_analyse_v01.py cal', code_sha256=sha(__file__), runs=len(recs), valid=sum(r['valid'] for r in recs),
               invalid=[(r['job'], r['reasons']) for r in recs if not r['valid']], shares={str(g): v for g, v in shares.items()}, g_D=gD, low_power=low,
               match_row=row, match_table_sha256=sha(TABLE), masks_sha256=sha(MASKS), runs_detail=recs)
    (OUT / 'E5_CAL_v01.json').write_text(json.dumps(doc, indent=1, allow_nan=False), encoding='utf-8')
    s = dict(schema='E5_SETTINGS_V01', g_D=gD, g_N=row['g_N'], g_N_index=row['g_N_index'], caution_F0D_pct=row['caution_F0D_pct'], caution_N_pct=row['caution_N_pct'],
             caution_diff_pp=row['caution_diff_pp'], low_power=low, shares={str(g): shares[g]['share'] for g in CAL_G}, cal_sha256=sha(OUT / 'E5_CAL_v01.json'),
             match_table_sha256=sha(TABLE), masks_sha256=sha(MASKS), pbar_dr_sha256=sha(PBAR_V05))
    with open(SETTINGS, 'x', encoding='utf-8', newline='\n') as f: f.write(json.dumps(s, indent=1) + '\n')
    print(json.dumps(dict(runs=len(recs), valid=doc['valid'], shares={str(g): shares[g]['share'] for g in CAL_G}, g_D=gD, g_N=row['g_N'], low_power=low, settings_sha256=sha(SETTINGS))))


def main_stage():
    if not LOCK_B.exists(): raise SystemExit('REFUSED: LOCK_A12b.txt does not exist')
    if sha(SETTINGS) not in LOCK_B.read_text(encoding='utf-8'): raise SystemExit('REFUSED: E5_SETTINGS_v01.json is not the one in LOCK_A12b')
    paths = dict(o=OUT / 'OUTCOMES_E5_v01.json', r=OUT / 'E5_RESULTS_v01.json', x=OUT / 'A_EXPORT_E5.json')
    for p in paths.values(): assert not p.exists(), f'{p.name} exists; never overwrite'
    s = json.loads(SETTINGS.read_text(encoding='utf-8')); m = json.loads(MASKS.read_text(encoding='utf-8'))
    if s['masks_sha256'] != sha(MASKS) or s['match_table_sha256'] != sha(TABLE) or s.get('pbar_dr_sha256') != sha(PBAR_V05):
        raise SystemExit('REFUSED: the mask table, match table or P-bar_DR differs from the hashes in the settings')
    recs = collect('e5_', expect={'E_F0': s['g_D'], 'E_N': s['g_N']})
    want = {f'e5_{c}_{a}' for c in m['main_cases'] for a in ('e_f0', 'e_n')}
    have = {r['job'] for r in recs}
    paths['o'].write_text(json.dumps(dict(schema='E5_OUTCOMES_V01', code='e5_analyse_v01.py', n_jobs=len(recs), n_valid=sum(r['valid'] for r in recs),
                                          missing=sorted(want - have), runs=recs), indent=1, allow_nan=False), encoding='utf-8')
    rows = [dict(r, level='D') for r in recs]
    c = EA.compare(rows, 'E_N', 'E_F0', 'D', 'D')
    # one-sided bootstrap p (A12 §4, §6.7): same pairs and index matrix as compare() (fresh default_rng(20261922), 20,000)
    A = {r['case']: r for r in rows if r['arm'] == 'E_N'}; R = {r['case']: r for r in rows if r['arm'] == 'E_F0'}
    cases = sorted(set(A) & set(R)); pairs = [(A[k], R[k]) for k in cases if A[k]['valid'] and R[k]['valid']]
    d = np.array([int(x['outcomes']['contact']) - int(y['outcomes']['contact']) for x, y in pairs], float); n = len(d)
    p_one = None
    if n:
        idx = np.random.default_rng(EA.SEED).integers(0, n, (EA.NBOOT, n)); p_one = float(np.mean(d[idx].mean(axis=1) >= 0.))
    v = {'E5.status': 'ran', 'E5.n_cases': len({r['case'] for r in recs}), 'E5.g_D': s['g_D'], 'E5.g_N': s['g_N'], 'E5.low_power': s['low_power'],
         'E5.caution_F0D': s['caution_F0D_pct'], 'E5.caution_N': s['caution_N_pct'], 'E5.caution_diff': s['caution_diff_pp']}
    for g in CAL_G: v[f'E5.cal.g{mj_tag(g)}.contact'] = s['shares'][str(g)]
    for arm, ak in (('E_F0', 'F0D'), ('E_N', 'N')):
        sel = [r for r in recs if r['arm'] == arm and r['valid']]
        for k, ok in MEAN.items():
            xs = [float(r['outcomes'][ok]) for r in sel if r['outcomes'][ok] is not None]; v[f'E5.{ak}.{k}'] = sum(xs) / len(xs) if xs else None
        for k, ok in MEDIAN.items():
            xs = [float(r['outcomes'][ok]) for r in sel if r['outcomes'][ok] is not None]; v[f'E5.{ak}.{k}'] = float(statistics.median(xs)) if xs else None
        nd = sum(int(r['outcomes']['decisions'] or 0) for r in sel)
        v[f'E5.{ak}.fallback'] = sum(int(r['outcomes']['fallback_decisions'] or 0) for r in sel) / nd if nd else None
        ms = [r['masked_share'] for r in sel if r['masked_share'] is not None]; v[f'E5.{ak}.masked'] = sum(ms) / len(ms) if ms else None
    v['E5.dc'] = c['contact'].get('diff'); v['E5.dc.ci'] = [c['contact'].get('lo'), c['contact'].get('hi')]; v['E5.mcnemar_p'] = c['contact'].get('mcnemar_exact_p')
    v['E5.dt'] = c['time_lost']['mean']; v['E5.dt.ci'] = [c['time_lost']['lo'], c['time_lost']['hi']]
    for k, ok in PAIRED.items():
        pdf = c['descriptive'][ok]['paired_diff']; v[f'E5.d_{k}'] = pdf['mean']; v[f'E5.d_{k}.ci'] = [pdf['lo'], pdf['hi']]
    v['E5.class'] = c['classification']; v['E5.p_one'] = p_one
    def clean(x):
        if isinstance(x, list):
            y = [clean(z) for z in x]; return None if all(z is None for z in y) else y
        if isinstance(x, float) and not math.isfinite(x): return None
        return x
    v = {k: clean(x) for k, x in v.items()}
    paths['r'].write_text(json.dumps(dict(schema='E5_RESULTS_V01', comparison=c, p_one=p_one, pairs=n), indent=1, allow_nan=True, default=str), encoding='utf-8')
    doc = dict(package='E', set='E5', written=datetime.datetime.now().astimezone().isoformat(), program='e5_analyse_v01.py', program_sha256=sha(__file__),
               lock_sha256=sha(LOCK_B), values=v)
    paths['x'].write_text(json.dumps(doc, indent=1, allow_nan=False), encoding='utf-8')
    print(json.dumps(dict(runs=len(recs), valid=sum(r['valid'] for r in recs), missing=len(want - have), pairs=n, dc=v['E5.dc'], ci=v['E5.dc.ci'],
                          cls=v['E5.class'], p_one=p_one, keys=len(v))))


def mj_tag(g):
    return ('%g' % g).replace('.', 'p')


if __name__ == '__main__':
    {'cal': cal, 'main': main_stage}[sys.argv[1]]()
