"""D1 pilot check (review finding 2): does the actor PID realise each lead profile? Reads ONLY the three d1_pilot runs
(pd13pilot_*; not study runs) from the volume; prints the lead's measured speed against its request. Pod system python3.

Per pilot run: assessment-window RMSE and max |speed - request|; for stop_and_go the measured standstill (speed < 0.1 m/s)
duration and the final speed; for mild_braking the final speed against v/2; for constant the min/max speed; the actor
review status and its summary fields; the run's capture status. Usage: python3 pilot_check_d1.py [folder]
"""
import json, math, sys, tarfile, pathlib

root = pathlib.Path('/workspace') / (sys.argv[1] if len(sys.argv) > 1 else 'claude_v13_cd_v01') / 'results'
for d in sorted(root.glob('pd13pilot_*')):
    rid = d.name; arch = d / f'claude_main_{rid}.tar.gz'
    if not arch.is_file(): print(rid, 'no archive'); continue
    rows, review, summ = [], None, json.loads((d / 'SUMMARY.json').read_text())
    with tarfile.open(arch, 'r:gz') as t:
        for m in t:
            if m.name.endswith('/scenario_frames.jsonl'):
                rows = [json.loads(l) for l in t.extractfile(m).read().decode().splitlines() if l.strip()]
            elif m.name.endswith('/actor_review.json') and m.name.count('/') == 1:
                review = json.loads(t.extractfile(m).read())
    pts = []
    for r in rows:
        q = r['request']; t_ = q['assessment_time_s']; v = r['measured'][0]['center_velocity_route_rh']
        if v is None: continue
        pts.append((t_, math.hypot(v[0], v[1]), q['requested_speed_mps'], q['reason']))
    win = [p for p in pts if p[0] >= 0]
    err = [p[1] - p[2] for p in win]
    out = dict(run=rid, status=summ['status'], frames=len(rows), reasons=sorted({p[3] for p in win}),
               rmse=math.sqrt(sum(e * e for e in err) / len(err)) if err else None, max_abs_err=max((abs(e) for e in err), default=None),
               speed_min=min((p[1] for p in win), default=None), speed_max=max((p[1] for p in win), default=None),
               final_speed=win[-1][1] if win else None, final_request=win[-1][2] if win else None,
               standstill_s=0.05 * sum(1 for p in win if p[1] < 0.1),
               request_zero_s=0.05 * sum(1 for p in win if p[2] == 0.0),
               actor_review=review and review.get('status'),
               review_summary=review and {k: review.get('summary', {}).get(k) for k in ('speed_vs_current_request_rmse', 'reasons')})
    print(json.dumps(out))
