"""Package E: compare the first program (session E, Opus) with the second (recount, Sonnet) under A10 10.1(c):
counts exact; points and interval ends on the same draws within 1e-9; classifications equal. A disagreement is listed with both
values; it stops the work until its cause is recorded and fixed (A10 10.1(c)).

python -I -B e_compare_v01.py outcomes <mine OUTCOMES_*.json> <theirs recount outcomes .json> --out X.json
python -I -B e_compare_v01.py compare  <mine E3_RESULTS.json> <theirs recount compare .json> --out X.json
"""
import argparse, json, math, pathlib

TOL = 1e-9
CONT = ('impact_speed_mps', 'time_lost_s', 'rest_gap_m', 'peak_decel_mps2', 'rms_jerk_mps3', 'fallback_share')
VAR = {'constant': 'constant', 'mild_braking': 'mild_braking', 'stop_and_go': 'stop_and_go'}


def num_eq(a, b):
    if a is None or b is None:
        return (a is None or (isinstance(a, float) and math.isnan(a))) and (b is None or (isinstance(b, float) and math.isnan(b)))
    if isinstance(a, float) and math.isnan(a): return isinstance(b, float) and math.isnan(b)
    return abs(float(a) - float(b)) <= TOL


def outcomes(mine, theirs):
    M = {r['job']: r for r in json.loads(pathlib.Path(mine).read_text(encoding='utf-8'))['runs']}
    T = {r['job']: r for r in json.loads(pathlib.Path(theirs).read_text(encoding='utf-8'))['runs']}
    diffs = []; n = 0
    for job in sorted(set(M) | set(T)):
        if job not in M or job not in T:
            diffs.append(dict(job=job, field='presence', mine=job in M, theirs=job in T)); continue
        m, t = M[job], T[job]; n += 1
        if bool(m['valid']) != bool(t['valid']):
            diffs.append(dict(job=job, field='valid', mine=m['valid'], theirs=t['valid'])); continue
        if not m['valid']: continue
        mo = m['outcomes']
        for f in ('contact', 'first_contact_k'):
            if (mo.get(f) if mo.get(f) is not None else None) != (t.get(f) if t.get(f) is not None else None):
                diffs.append(dict(job=job, field=f, mine=mo.get(f), theirs=t.get(f)))
        for f in CONT:
            if not num_eq(mo.get(f), t.get(f)):
                diffs.append(dict(job=job, field=f, mine=mo.get(f), theirs=t.get(f)))
    return dict(schema='E_COMPARE_OUTCOMES_V01', runs_compared=n, disagreements=len(diffs), by_field={f: sum(d['field'] == f for d in diffs) for f in sorted({d['field'] for d in diffs})}, list=diffs)


def comparisons(mine, theirs):
    M = json.loads(pathlib.Path(mine).read_text(encoding='utf-8'))['comparisons']
    T = json.loads(pathlib.Path(theirs).read_text(encoding='utf-8'))['comparisons']
    def key_m(c): return (c['stage'].upper(), c['arm'], c['ref'], c['level_ref'], c.get('lead_variant') or None)

    def lv_t(c):   # the recount names the D1 variant in a field (v03 on) or only in its label (v01/v02)
        if c.get('lead_variant'): return c['lead_variant']
        lab = c.get('label') or ''
        return lab.split('lead variant ', 1)[1].strip() if 'lead variant ' in lab else None
    def key_t(c): return (str(c.get('set', '')).upper(), c['arm'], c['reference'], c.get('level'), lv_t(c))
    Mi = {key_m(c): c for c in M if c.get('classification') != 'no pairs' or True}
    Ti = {key_t(c): c for c in T}
    extras = [dict(key=k, label=Ti[k].get('label')) for k in Ti if k not in Mi and '(extra)' in (Ti[k].get('label') or '')]
    diffs = []; n = 0
    for k in sorted(set(Mi) | set(Ti), key=str):
        if k in Ti and k not in Mi and '(extra)' in (Ti[k].get('label') or ''):
            continue   # the recount's labelled extra (F0_IMM vs F0) has no first-program counterpart; listed under 'extras'
        if k not in Mi or k not in Ti:
            diffs.append(dict(key=k, field='presence', mine=k in Mi, theirs=k in Ti)); continue
        m, t = Mi[k], Ti[k]; n += 1
        ct = m['contact']
        for fm, ft in (('pairs', 'pairs'),):
            if m[fm] != t[ft]: diffs.append(dict(key=k, field=fm, mine=m[fm], theirs=t[ft]))
        for f in ('a', 'b', 'c', 'd'):
            if ct.get(f) != t.get(f): diffs.append(dict(key=k, field=f, mine=ct.get(f), theirs=t.get(f)))
        for fm, ft in (('diff', 'contact_diff'), ('lo', 'contact_diff_lo'), ('hi', 'contact_diff_hi'), ('mcnemar_exact_p', 'mcnemar_p')):
            if not num_eq(ct.get(fm), t.get(ft)): diffs.append(dict(key=k, field=ft, mine=ct.get(fm), theirs=t.get(ft)))
        tl = m['time_lost']
        for fm, ft in (('mean', 'time_lost_diff'), ('lo', 'time_lost_lo'), ('hi', 'time_lost_hi')):
            if not num_eq(tl.get(fm), t.get(ft)): diffs.append(dict(key=k, field=ft, mine=tl.get(fm), theirs=t.get(ft)))
        if m['classification'] != t['classification']:
            diffs.append(dict(key=k, field='classification', mine=m['classification'], theirs=t['classification']))
        if (m.get('hypothesis') or None) != (t.get('hypothesis') or None):
            diffs.append(dict(key=k, field='hypothesis', mine=m.get('hypothesis'), theirs=t.get('hypothesis')))
        # descriptive outcomes (A10 7.5 'Other outcomes'): paired mean difference and its bootstrap interval, same draws
        for o, dm in (m.get('descriptive') or {}).items():
            to = (t.get('outcomes') or {}).get(o)
            if to is None:
                diffs.append(dict(key=k, field=f'{o}.presence', mine=True, theirs=False)); continue
            pd = dm['paired_diff']
            if pd.get('m') != to.get('n_pairs_used'): diffs.append(dict(key=k, field=f'{o}.pairs', mine=pd.get('m'), theirs=to.get('n_pairs_used')))
            if pd.get('resamples') != to.get('n_boot_defined'): diffs.append(dict(key=k, field=f'{o}.resamples', mine=pd.get('resamples'), theirs=to.get('n_boot_defined')))
            for fm, ft in (('mean', 'mean_diff'), ('lo', 'ci_lo'), ('hi', 'ci_hi')):
                if not num_eq(pd.get(fm), to.get(ft)): diffs.append(dict(key=k, field=f'{o}.{ft}', mine=pd.get(fm), theirs=to.get(ft)))
    return dict(schema='E_COMPARE_RESULTS_V01', comparisons_compared=n, disagreements=len(diffs), extras_in_recount=extras, list=diffs)


def exports(mine, theirs):
    """A_EXPORT_E.json vs A_RECOUNT_E.json (RESULTS_INTERFACE_v13 section 1: 'the same keys'): key sets equal; numbers and
    interval ends within 1e-9 (None = undefined on both sides); strings and booleans equal."""
    M = json.loads(pathlib.Path(mine).read_text(encoding='utf-8'))['values']
    T = json.loads(pathlib.Path(theirs).read_text(encoding='utf-8'))['values']
    diffs = []
    for k in sorted(set(M) | set(T)):
        if k not in M or k not in T:
            diffs.append(dict(key=k, field='presence', mine=k in M, theirs=k in T)); continue
        m, t = M[k], T[k]
        if isinstance(m, list) or isinstance(t, list):
            ok = isinstance(m, list) and isinstance(t, list) and len(m) == len(t) and all(num_eq(x, y) for x, y in zip(m, t))
        elif isinstance(m, (bool, str)) or isinstance(t, (bool, str)):
            ok = m == t
        else:
            ok = num_eq(m, t)
        if not ok: diffs.append(dict(key=k, field='value', mine=m, theirs=t))
    return dict(schema='E_COMPARE_EXPORT_V01', keys_mine=len(M), keys_theirs=len(T), disagreements=len(diffs), list=diffs)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('what', choices=('outcomes', 'compare', 'export')); ap.add_argument('mine'); ap.add_argument('theirs'); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    res = {'outcomes': outcomes, 'compare': comparisons, 'export': exports}[a.what](a.mine, a.theirs)
    pathlib.Path(a.out).write_text(json.dumps(res, indent=1, default=str), encoding='utf-8')
    print(json.dumps({k: v for k, v in res.items() if k != 'list'}), 'first:', res['list'][:3])


if __name__ == '__main__':
    main()
