"""Collect package E's per-run outcomes (first program) from the fetched runs: one record per job with its design fields
(stage, case, arm, level, g / triple, tracker, desired speed, D1 variant) from SUMMARY.json / ARM_METHOD_v01.json, its validity,
and the A10 7.4 outcomes from e_outcomes_v01.outcomes().

Validity of a run: SUMMARY status CAPTURED_AND_REVIEWED (capture, review and actor review all exited 0, readers agree), no
policy_failure.json, no contact event before the assessment window. An invalid run is listed with its reason and enters no
comparison (its pair is dropped). Only the run of record of each job is used: the worker's last attempt with a SUMMARY
(retries carry '__r<k>' in the run id); duplicates are listed.

Gate: for stages e3 and e3b the program refuses to run unless revision_v13\\LOCK_A10_2.txt exists (A10 4, README rule 3).

Usage: python -I -B e_collect_v01.py <stage: e1s|e1|e2|e3|e3b> --out <OUTCOMES.json>
"""
import argparse, json, math, pathlib, sys

E = pathlib.Path(__file__).resolve().parents[1]
RUNS = E / 'runs'
LOCK2 = E.parents[1] / 'LOCK_A10_2.txt'
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import e_outcomes_v01 as EO     # noqa: E402

PREFIX = {'e1s': 'e1s_', 'e1': 'e1_', 'e2': 'e2_', 'e3': 'e3_', 'e3b': 'e3b_'}


def base_id(rid):
    return rid.split('__')[0]


def attempt_of(rid):
    for part in rid.split('__')[1:]:
        if part.startswith('r') and part[1:].isdigit(): return int(part[1:]) + 1
    return 1


def one(d):
    summ = json.loads((d / 'SUMMARY.json').read_text(encoding='utf-8'))
    rec = dict(run_id=d.name, job=summ['job'], attempt=summ.get('attempt'), status=summ['status'], case=summ['case'], arm=summ['arm'],
               e_job=summ.get('e_job'), pod_id=summ.get('pod_id'))
    reasons = []
    if summ['status'] != 'CAPTURED_AND_REVIEWED': reasons.append('status ' + summ['status'])
    caps = list((d / 'x' / d.name / 'capture').glob('*')) if (d / 'x' / d.name / 'capture').exists() else []
    if len(caps) != 1:
        reasons.append('no capture folder'); rec.update(valid=False, reasons=reasons); return rec
    cap = caps[0]
    method = json.loads((cap / 'ARM_METHOD_v01.json').read_text(encoding='utf-8')) if (cap / 'ARM_METHOD_v01.json').exists() else None
    if method is None: reasons.append('no method record')
    contract = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))
    case = contract['case']
    rec.update(desired_mps=float(case['desired_mps']), family=case['draw']['family'], lead_variant=(case.get('lead_variant') or {}).get('kind'),
               g=None if method is None else method['knobs'].get('g'), triple=None if method is None else method['knobs'].get('triple'),
               tracker=None if method is None else method.get('tracker'), level=(summ.get('e_job') or {}).get('level'))
    if (cap / 'policy_failure.json').exists(): reasons.append('policy failure')
    try:
        out = EO.outcomes(cap, case['desired_mps'])
    except Exception as e:
        reasons.append('outcomes error: ' + repr(e)[:200]); out = None
    if out is not None:
        if out['warmup_contact_event']: reasons.append('contact before the assessment window')
        rec['outcomes'] = {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in out.items() if k != 'capture'}
    rec['valid'] = not reasons; rec['reasons'] = reasons
    return rec


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('stage', choices=list(PREFIX)); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    if a.stage in ('e3', 'e3b') and not LOCK2.exists():
        raise SystemExit('REFUSED: LOCK_A10_2.txt does not exist; no closed-loop main-run value is computed before Lock 2')
    dirs = sorted(d for d in RUNS.glob(PREFIX[a.stage] + '*') if (d / 'SUMMARY.json').exists())
    if a.stage == 'e1':
        dirs = [d for d in dirs if not d.name.startswith('e1s_')]
    by_job = {}
    for d in dirs:
        by_job.setdefault(base_id(d.name), []).append(d)
    records = []; dup = []
    for job, ds in sorted(by_job.items()):
        ds = sorted(ds, key=lambda x: attempt_of(x.name))
        if len(ds) > 1: dup.append(dict(job=job, runs=[x.name for x in ds]))
        records.append(one(ds[-1]))
    doc = dict(schema='E_OUTCOMES_V01', stage=a.stage, code='e_collect_v01.py', n_jobs=len(records), n_valid=sum(r['valid'] for r in records),
               multiple_attempts=dup, runs=records)
    pathlib.Path(a.out).write_text(json.dumps(doc, indent=1, allow_nan=False), encoding='utf-8')
    print(json.dumps(dict(stage=a.stage, jobs=len(records), valid=doc['n_valid'], invalid=[(r['job'], r['reasons']) for r in records if not r['valid']][:20])))


if __name__ == '__main__':
    main()
