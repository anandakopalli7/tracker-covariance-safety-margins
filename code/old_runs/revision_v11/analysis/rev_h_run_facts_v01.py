"""Revision v11: facts about the recordings that the v11 text states (requested and realised lead deceleration, run length,
runs that ended at a contact). New file, 18 Nov 2026. Reads the stored Gate R meta and, per lead-braking run, contract.json and
evaluation_truth.jsonl of its capture folder (read-only). Realised deceleration = minus the least-squares slope of the true
lead's speed against time between 90% and 10% of its speed before the brake onset (the lead's speed from the target actor's
velocity in evaluation_truth.jsonl; time = k * 0.05 s; the onset is 5 s + brake_start_s after the episode clock starts).
Output: out/REV_H_RUN_FACTS_v01.json.  Usage: python -B -X utf8 rev_h_run_facts_v01.py
"""
import json, math, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
P = pathlib.Path(r'<library folder>')
S = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
OUT = HERE / 'out' / 'REV_H_RUN_FACTS_v01.json'
if OUT.exists():
    sys.exit('REFUSED: %s exists' % OUT)
rows = []
for st, arch, pat in (('fit', P / '07_fit_runs' / 'archives', 'p1b_fit_finite_*.npz'), ('tuning', P / '08_phase2' / 'archives_c1', 'p2_c1109_tune_*.npz')):
    for f in sorted(S.glob(pat)):
        z = np.load(f, allow_pickle=False); m = json.loads(str(z['meta']))
        if m['family'] != 'lead_braking':
            continue
        run = m['run']; capd = list((arch / run / 'x' / run / 'capture').iterdir())[0]
        draw = json.loads((capd / 'contract.json').read_text(encoding='utf-8'))['case']['draw']
        ks = []; vs = []
        for line in open(capd / 'evaluation_truth.jsonl', encoding='utf-8'):
            if not line.strip():
                continue
            r = json.loads(line); tg = r.get('target')
            if not tg:
                continue
            a = [x for x in (r.get('scenario_actors') or []) if x['actor_id'] == tg['actor_id']]
            if not a:
                continue
            v = a[0]['velocity_lh']; ks.append(r['k']); vs.append(math.hypot(v[0], v[1]))
        ks = np.array(ks); vs = np.array(vs); t = ks * 0.05
        pre = (t > 3) & (t < 5 + draw['brake_start_s'] - 0.2)
        v0 = float(np.median(vs[pre])) if pre.any() else float(vs[:20].max())
        sel = (vs < 0.9 * v0) & (vs > 0.1 * v0) & (t > 5 + draw['brake_start_s'] - 0.5)
        dec = None
        if sel.sum() >= 4:
            i = np.nonzero(sel)[0]; i = np.arange(i[0], i[-1] + 1)
            dec = float(-np.polyfit(t[i], vs[i], 1)[0])
        rows.append(dict(set=st, run=run, desired=draw['desired_mps'], brake_requested=draw['brake_mps2'], brake_realised=dec,
                         brake_start_s=draw['brake_start_s'], tau_s=draw['tau_s'], lead_speed_before=v0,
                         evaluated=int(z['evaluated'].sum()), contact_k=m.get('contact_k'), kmax=m.get('kmax'),
                         ended_at_contact=bool(m.get('contact_k') is not None and m.get('contact_k') >= 0)))
doc = dict(code='rev_h_run_facts_v01.py', written=time.strftime('%Y-%m-%d %H:%M:%S'), runs=rows, summary={})
for st in ('fit', 'tuning'):
    R = [r for r in rows if r['set'] == st]
    rq = np.array([r['brake_requested'] for r in R]); rl = np.array([r['brake_realised'] for r in R], float)
    doc['summary'][st] = dict(
        n=len(R), requested_min_med_max=[float(rq.min()), float(np.median(rq)), float(rq.max())],
        realised_min_med_max=[float(np.nanmin(rl)), float(np.nanmedian(rl)), float(np.nanmax(rl))],
        n_requested_above_5p5=int((rq > 5.5).sum()), n_realised_above_5p5=int((rl > 5.5).sum()),
        tau_s_min_max=[float(min(r['tau_s'] for r in R)), float(max(r['tau_s'] for r in R))],
        ended_at_contact=[dict(run=r['run'], evaluated=r['evaluated']) for r in R if r['ended_at_contact']],
        n_full_length=int(sum(1 for r in R if r['kmax'] == 699)), full_length_s=700 * 0.05,
        evaluated_in_full_length=sorted({r['evaluated'] for r in R if r['kmax'] == 699}),
        lead_speed_over_desired_min_max=[float(min(r['lead_speed_before'] / r['desired'] for r in R)),
                                         float(max(r['lead_speed_before'] / r['desired'] for r in R))])
OUT.write_text(json.dumps(doc, indent=1), encoding='utf-8')
print(json.dumps(doc['summary'], indent=1))
