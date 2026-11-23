"""B0 support: the library's CV0 replay (trk_tracker_v01.retrack_capture, recording subclass) against the logs of one run:
tracks, planner actors, filter events (kind, track, timestamp) and update algebra (prior state, prior P, measurement,
rotated_R). Usage: python -I -B -X utf8 b0_recorder_check_v01.py <cap dir> [variant]"""
import sys, pathlib, json, time
sys.path.insert(0, r'ARS_TRIAL\revision_v13\work\shared\trackers')
import trk_env_v01 as env
env.setup()
import trk_tracker_v01 as T
cap = pathlib.Path(sys.argv[1]); variant = sys.argv[2] if len(sys.argv) > 2 else 'CV0'
t0 = time.time()
ov, rec = T.retrack_capture(cap, variant)
t1 = time.time()
res = dict(variant=variant, seconds=round(t1 - t0, 2))
det = list(env.jl(cap / 'detections.jsonl'))
res['tracks_equal'] = all(a['tracks'] == b['tracks'] for a, b in zip(ov['detections.jsonl'], det))
fr = [f for f in env.jl(cap / 'frames.jsonl') if (f.get('execution') or {}).get('new_decision') is not None]
fo = [f for f in ov['frames.jsonl'] if (f.get('execution') or {}).get('new_decision') is not None]
res['n_dec'] = len(fr)
res['actors_equal'] = all(a['execution']['new_decision']['actors'] == b['execution']['new_decision']['actors'] for a, b in zip(fo, fr))
ev = list(env.jl(cap / 'filter_events.jsonl'))
key = lambda e: (e['kind'], e.get('track'), e.get('timestamp'))
res['events_n'] = (len(ov['filter_events.jsonl']), len(ev))
res['events_equal_kind_track_ts'] = [key(e) for e in ov['filter_events.jsonl']] == [key(e) for e in ev]
alg = [a for a in env.jl(cap / 'filter_algebra.jsonl') if a.get('kind') == 'update']
mine = [a for a in ov['filter_algebra.jsonl'] if a.get('kind') == 'update']
res['algebra_update_n'] = (len(mine), len(alg))
ok = len(mine) == len(alg)
bad = 0
for a, b in zip(mine, alg):
    for f in ('track', 'timestamp'):
        bad += a[f] != b[f]
    bad += a['prior']['state'] != b['prior']['state']
    bad += a['prior']['P'] != b['prior']['P']
    bad += a['measurement'] != b['measurement']
    bad += a['rotated_R'] != b['rotated_R']
res['algebra_fields_differ'] = bad
print(json.dumps(res))
