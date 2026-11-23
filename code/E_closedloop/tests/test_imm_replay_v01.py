"""E0 replay identity (A10 7.1 E0): the online IMM, fed a logged detection stream the way the probe feeds it, reproduces
session B's offline B1 output on the same detections within 1e-12 (tracks per detector update and planner actors per
decision tick).

Two processes (session B's rule: one tracker library per process):
  python -I -B test_imm_replay_v01.py online  <cap> <out.json> [--const FILE]
      E's path: e_imm_v01.OnlineIMM (the packet copy of B's library) -> per detector update tracker.step(model, time) ->
      the probe's ObservationStream (807 shared_policy_v01, unchanged) update/actors at every decision tick
  python -I -B test_imm_replay_v01.py offline <cap> <out.json> [--const FILE]
      B's path: trk_tracker_v01.retrack_capture(cap, 'B1') from work\\shared\\trackers (tracks and frames overlays)
  python -I -B test_imm_replay_v01.py compare <online.json> <offline.json> <report.json>
--const: a constants JSON for both (until B's trk_constants_v01.json is frozen; the report records which was used).
Run with OPENBLAS_CORETYPE=Haswell in the environment.
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import copy, hashlib, json, math, pathlib, sys

E = pathlib.Path(__file__).resolve().parents[1]
PK = E / 'packets' / 'dev_packet_e_v01' / 'claude_smoke_v01'
SHARED = E.parent / 'shared' / 'trackers'
W = pathlib.Path(r'<library folder>')
CODEX149 = W / '149_supported_sensor_preparation_20261101'
SIM_DT = 0.05


def jl(p):
    with open(p, encoding='utf-8') as f:
        for line in f:
            if line.strip(): yield json.loads(line)


def load_const(path):
    return None if path is None else json.loads(pathlib.Path(path).read_text(encoding='utf-8'))


def online(cap, out, const):
    os.environ['CLAUDE_SMOKE_WORKSPACE_ROOT'] = str(W)
    sys.path.insert(0, str(PK))
    sys.dont_write_bytecode = True
    sys.path.append(str(SHARED / 'shims_v01'))               # laptop stand-ins for packages that exist on the pod
    import e_imm_v01
    trk = e_imm_v01.OnlineIMM(codex_root=str(CODEX149), const=const)
    import arms_adapter_v02 as arms                          # the probe's import chain (807 ObservationStream)
    stream = arms.live.ObservationStream()
    det = list(jl(cap / 'detections.jsonl'))
    truth0 = next(jl(cap / 'evaluation_truth.jsonl')); route_yaw = float(truth0['ego']['derived']['route_yaw_rh'])
    tracks_out = []; actors_out = {}; rec_json_ok = True
    di = 0; last = None
    frames = list(jl(cap / 'frames.jsonl'))
    for fr in frames:
        k = fr['k']
        while di < len(det) and det[di]['k'] == k:
            row = det[di]
            tracks = trk.step(copy.deepcopy(row['model']), row['time'])
            stream.update(k, int(row['frame']), row['time'], tracks)
            tracks_out.append(copy.deepcopy(tracks)); di += 1
            for items in trk.new_records():
                try: json.dumps(items, allow_nan=False)
                except Exception: rec_json_ok = False
        ex = fr.get('execution')
        if ex and ex.get('new_decision') is not None and k >= 19:
            c = fr['state']['center_lh']
            import numpy as np
            center = np.array([c[0], -c[1], c[2]])
            actors_out[str(k)] = stream.actors(k, fr['time'], center, route_yaw)
    pathlib.Path(out).write_text(json.dumps(dict(tracks=tracks_out, actors=actors_out, describe=trk.describe(), recorder_json_ok=rec_json_ok,
                                                 index=trk.index)), encoding='utf-8')


def offline(cap, out, const):
    sys.path.insert(0, str(SHARED))
    import trk_env_v01 as env
    env.setup(codex_root=str(CODEX149))
    import trk_tracker_v01 as T
    ov, rec = T.retrack_capture(cap, 'B1', const=const)
    tracks = [r['tracks'] for r in ov['detections.jsonl']]
    actors = {str(fr['k']): fr['execution']['new_decision']['actors'] for fr in ov['frames.jsonl']
              if fr.get('execution') and fr['execution'].get('new_decision') is not None and fr['k'] >= 19}
    pathlib.Path(out).write_text(json.dumps(dict(tracks=tracks, actors=actors)), encoding='utf-8')


def maxdiff(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys(): return math.inf
        return max([maxdiff(a[k], b[k]) for k in a] or [0.])
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): return math.inf
        return max([maxdiff(x, y) for x, y in zip(a, b)] or [0.])
    if isinstance(a, (bool, str)) or a is None or isinstance(b, (bool, str)) or b is None:
        return 0. if a == b else math.inf
    return abs(float(a) - float(b))


def compare(on, off, rep):
    A = json.loads(pathlib.Path(on).read_text(encoding='utf-8')); B = json.loads(pathlib.Path(off).read_text(encoding='utf-8'))
    t_exact = sum(int(x == y) for x, y in zip(A['tracks'], B['tracks']))
    a_keys = sorted(set(A['actors']) & set(B['actors']), key=int)
    a_exact = sum(int(A['actors'][k] == B['actors'][k]) for k in a_keys)
    r = dict(schema='E_IMM_REPLAY_IDENTITY_V01', detector_updates=[len(A['tracks']), len(B['tracks'])], tracks_exact_updates=t_exact,
             tracks_max_abs_diff=maxdiff(A['tracks'], B['tracks']), decision_ticks=[len(A['actors']), len(B['actors'])],
             actors_exact_ticks=a_exact, actors_max_abs_diff=maxdiff({k: A['actors'][k] for k in a_keys}, {k: B['actors'][k] for k in a_keys}),
             recorder_json_ok=A['recorder_json_ok'], online_describe=A['describe'])
    r['pass'] = bool(r['detector_updates'][0] == r['detector_updates'][1] and r['decision_ticks'][0] == r['decision_ticks'][1]
                     and r['tracks_max_abs_diff'] <= 1e-12 and r['actors_max_abs_diff'] <= 1e-12 and r['recorder_json_ok'])
    pathlib.Path(rep).write_text(json.dumps(r, indent=1), encoding='utf-8')
    print(json.dumps({k: v for k, v in r.items() if k != 'online_describe'}))


if __name__ == '__main__':
    mode = sys.argv[1]
    cst = None
    if '--const' in sys.argv:
        i = sys.argv.index('--const'); cst = load_const(sys.argv[i + 1]); del sys.argv[i:i + 2]
    if mode == 'online': online(pathlib.Path(sys.argv[2]), sys.argv[3], cst)
    elif mode == 'offline': offline(pathlib.Path(sys.argv[2]), sys.argv[3], cst)
    elif mode == 'compare': compare(sys.argv[2], sys.argv[3], sys.argv[4])
