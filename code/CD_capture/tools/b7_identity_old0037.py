"""B7 (i) identity on OLD run p1b_fit_finite_0037 only (exploratory, allowed): offline 2 Hz ticks vs the logged online detections."""
import json, tarfile, math
arch = '/workspace/claude_main_v01/results/p1b_fit_finite_0037/claude_main_p1b_fit_finite_0037.tar.gz'
logged = {}
with tarfile.open(arch, 'r:gz') as t:
    for m in t:
        if m.name.endswith('/detections.jsonl') and '/capture/' in m.name:
            for l in t.extractfile(m).read().decode().splitlines():
                if l.strip():
                    d = json.loads(l); logged[d['k']] = d
off = {}
for l in open('/opt/claude_v13_local/b7/p1b_fit_finite_0037/b7_detections_v13.jsonl'):
    d = json.loads(l); off[d['k']] = d
ticks = sorted(logged); hash_eq = 0; nbox_eq = 0; maxd = 0.0; score_maxd = 0.0
for k in ticks:
    a = logged[k]; b = off.get(k)
    if b is None: continue
    hash_eq += a['combined_hash'] == b['combined_hash']
    if len(a['model']) == len(b['model']):
        nbox_eq += 1
        for x, y in zip(a['model'], b['model']):
            maxd = max(maxd, max(abs(p - q) for p, q in zip(x['translation'] + x['size'] + x['velocity'], y['translation'] + y['size'] + y['velocity'])))
            score_maxd = max(score_maxd, abs(x['detection_score'] - y['detection_score']))
print(json.dumps(dict(online_ticks=len(ticks), offline_rows=len(off), ticks_matched=sum(k in off for k in ticks), combined_hash_equal=hash_eq,
                      box_count_equal=nbox_eq, max_abs_box_diff_m=maxd, max_abs_score_diff=score_maxd, online_tick_flags=sum(off[k]['online_tick'] for k in off))))
