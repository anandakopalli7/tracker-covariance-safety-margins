import os, sys, json, pathlib, math
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
sys.path.insert(0, r'ARS_TRIAL\revision_v13\work\shared\trackers')
import trk_env_v01 as env
env.setup()
import trk_tracker_v01 as T
def jl(p): return [json.loads(x) for x in open(p, encoding='utf-8') if x.strip()]
def maxdiff(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys(): return math.inf
        return max([maxdiff(a[k], b[k]) for k in a] or [0.])
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): return math.inf
        return max([maxdiff(x, y) for x, y in zip(a, b)] or [0.])
    if isinstance(a, (str, bool)) or a is None: return 0. if a == b else math.inf
    return abs(float(a) - float(b))
out = {}
for rid in sys.argv[1:]:
    cap = next((pathlib.Path(r'ARS_TRIAL\revision_v13\work\E_closedloop\runs') / rid / 'x' / rid / 'capture').iterdir())
    ov, rec = T.retrack_capture(cap, 'B1')
    det = jl(cap / 'detections.jsonl')
    t_exact = sum(int(a['tracks'] == b['tracks']) for a, b in zip(det, ov['detections.jsonl']))
    t_max = max(maxdiff(a['tracks'], b['tracks']) for a, b in zip(det, ov['detections.jsonl']))
    fr = jl(cap / 'frames.jsonl'); fo = ov['frames.jsonl']
    pairs = [(a['execution']['new_decision']['actors'], b['execution']['new_decision']['actors']) for a, b in zip(fr, fo)
             if a.get('execution') and a['execution'].get('new_decision') and a['k'] >= 19]
    a_exact = sum(int(x == y) for x, y in pairs); a_max = max([maxdiff(x, y) for x, y in pairs] or [0.])
    ev = jl(cap / 'imm_filter_events.jsonl') if (cap / 'imm_filter_events.jsonl').exists() else []
    out[rid] = dict(detector_updates=len(det), tracks_exact=t_exact, tracks_max_abs_diff=t_max, decisions=len(pairs), actors_exact=a_exact,
                    actors_max_abs_diff=a_max, events_equal=(ev == rec.events), n_events=len(ev))
print(json.dumps(out, indent=1))
