"""v13 B0 copy (19 Nov 2026): adds mode b0 (155 runs). Otherwise unchanged."""
"""Step 1: exact offline tracker harness (v02: OpenBLAS kernel pinned to Haswell through m4_common_v02; v01 ran with
the laptop's default SkylakeX kernel and differed from the logs in the last bit, max 4.4e-16).

For each run: feed the logged detections (detections.jsonl, field model[], logged order and times) through the real
tracker code (Codex OnlineTracker -> CANMOT, unmodified, third-party packages missing on the laptop replaced by the
stand-ins in shims_v01) and compare with the logged tracks[]; then rebuild the planner actor list for every decision
tick from the replayed tracks and the logged ego centre and compare with frames.jsonl -> execution.new_decision.actors.
Also compares the filter instrumentation streams (events, target covariances, algebra) with the logged files.
All comparisons are exact (==) on the parsed JSON values.

Usage: python -I -B -X utf8 tracker_harness_v02.py <mode> [out_csv]
   mode = 'one:<cap dir>' | 'sel20' | 'all'
Single process. Appends one CSV row per run (resume: runs already in the CSV are skipped).
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import m4_common_v02 as C                      # before numpy: pins the BLAS kernel
import copy, csv, json, math, time
import numpy as np

BLAS = C.require_exact_blas()
C.setup_codex()
from online_tracker import OnlineTracker, planner_actors
from sensor_policy import serial_actors
from tracker_audit import record_history, audited

FIELDS = ['set', 'archive', 'case_id', 'family', 'occluder', 'desired_mps', 'frames', 'contact', 'blas',
          'det_frames', 'model_rows', 'det_frames_exact', 'tracks_logged', 'tracks_exact', 'tracks_max_abs_diff',
          'events_exact', 'targets_exact', 'algebra_exact', 'algebra_max_abs_diff',
          'decisions', 'decisions_exact', 'actors_logged', 'actors_exact', 'actors_max_abs_diff',
          'decisions_with_actors', 'first_actor_k', 'route_yaw', 'det_k_ok', 'time_max_dev', 'seconds', 'note']


def replay(cap):
    det = list(C.jl(cap / 'detections.jsonl'))
    events, targets, algebra, outputs = [], [], [], []
    with record_history(events, targets), audited(algebra):
        tracker = OnlineTracker(C.tracker_config())
        for row in det:
            outputs.append(copy.deepcopy(tracker.step(copy.deepcopy(row['model']), row['time'])))
    return det, outputs, events, targets, algebra


def check_run(r):
    t0 = time.time()
    cap = pathlib.Path(r['cap'])
    det, outputs, events, targets, algebra = replay(cap)
    res = {k: r.get(k) for k in ('set', 'archive', 'case_id', 'family', 'occluder', 'desired_mps', 'frames', 'contact')}
    res['blas'] = BLAS
    note = []
    # --- tracks
    n_exact_frames = 0; n_tracks = 0; n_tracks_exact = 0; worst = 0.0
    for row, out in zip(det, outputs):
        n_tracks += len(row['tracks'])
        if out == row['tracks']:
            n_exact_frames += 1; n_tracks_exact += len(row['tracks'])
        else:
            if len(out) == len(row['tracks']):
                for a, b in zip(out, row['tracks']):
                    if a == b:
                        n_tracks_exact += 1
                    else:
                        worst = max(worst, C.max_abs_diff(a, b))
            else:
                worst = math.inf
    res.update(det_frames=len(det), model_rows=sum(len(d['model']) for d in det), det_frames_exact=n_exact_frames,
               tracks_logged=n_tracks, tracks_exact=n_tracks_exact, tracks_max_abs_diff=worst)
    res['det_k_ok'] = int([d['k'] for d in det] == list(range(19, 19 + 10 * len(det), 10)))
    res['time_max_dev'] = max([abs(d['time'] - (d['k'] + 1) * C.SIM_DT) for d in det] or [0.0])
    # --- instrumentation streams
    for key, name, val in (('events', 'filter_events.jsonl', events), ('targets', 'filter_target_covariances.jsonl', targets),
                           ('algebra', 'filter_algebra.jsonl', algebra)):
        p = cap / name
        if not p.exists():
            res[key + '_exact'] = ''
            continue
        logged = list(C.jl(p))
        res[key + '_exact'] = int(val == logged)
        if key == 'algebra':
            res['algebra_max_abs_diff'] = 0.0 if val == logged else C.max_abs_diff(val, logged)
    # --- planner actors
    truth0 = next(C.jl(cap / 'evaluation_truth.jsonl'))
    route_yaw = float(truth0['ego']['derived']['route_yaw_rh'])
    res['route_yaw'] = route_yaw
    by_k = {d['k']: out for d, out in zip(det, outputs)}
    n_dec = 0; n_dec_exact = 0; n_act = 0; n_act_exact = 0; worst_a = 0.0; n_dec_with = 0; first_actor_k = ''
    for fr in C.jl(cap / 'frames.jsonl'):
        ex = fr.get('execution')
        if not ex or 'new_decision' not in ex or ex['new_decision'] is None:
            continue
        dec = ex['new_decision']
        k = fr['k']
        n_dec += 1
        kd = None if k < 19 else 19 + 10 * ((k - 19) // 10)
        tracks = [] if kd is None else by_k.get(kd)
        if tracks is None:
            note.append('no detector frame for decision k=%d' % k)
            continue
        c = fr['state']['center_lh']
        ego = np.array([c[0], -c[1], c[2]])        # REFLECT @ center_lh
        mine = serial_actors(planner_actors(tracks, ego, route_yaw))
        logged = dec['actors']
        n_act += len(logged)
        if logged:
            n_dec_with += 1
            if first_actor_k == '':
                first_actor_k = k
        if mine == logged:
            n_dec_exact += 1; n_act_exact += len(logged)
        else:
            if len(mine) == len(logged):
                for a, b in zip(mine, logged):
                    if a == b:
                        n_act_exact += 1
                    else:
                        worst_a = max(worst_a, C.max_abs_diff(a, b))
            else:
                worst_a = math.inf
                if len(note) < 3:
                    note.append('k=%d actors mine %d logged %d' % (k, len(mine), len(logged)))
    res.update(decisions=n_dec, decisions_exact=n_dec_exact, actors_logged=n_act, actors_exact=n_act_exact,
               actors_max_abs_diff=worst_a, decisions_with_actors=n_dec_with, first_actor_k=first_actor_k,
               seconds=round(time.time() - t0, 2), note='; '.join(note))
    return res


def select20(rows):
    """10 tuning runs over all six families (both occluder settings in the crossing families) and 10 fit runs over
    the four families present in the fit set. Deterministic: evenly spaced picks from the sorted archive names."""
    plan = [('tune', 'benign', False, 1), ('tune', 'cutin', False, 2), ('tune', 'lead_braking', False, 1),
            ('tune', 'stopped', False, 1), ('tune', 'pedestrian_crossing', False, 1), ('tune', 'pedestrian_crossing', True, 1),
            ('tune', 'vehicle_crossing', False, 1), ('tune', 'vehicle_crossing', True, 2),
            ('fit', 'lead_braking', False, 2), ('fit', 'stopped', False, 2), ('fit', 'pedestrian_crossing', False, 2),
            ('fit', 'pedestrian_crossing', True, 2), ('fit', 'vehicle_crossing', False, 1), ('fit', 'vehicle_crossing', True, 1)]
    out = []
    for s, fam, occ, n in plan:
        g = sorted([r for r in rows if r['set'] == s and r['family'] == fam and r['occluder'] == occ], key=lambda r: r['archive'])
        idx = [int(round((i + 0.5) * len(g) / n - 0.5)) for i in range(n)]
        out += [g[i] for i in idx]
    return out


def main():
    mode = sys.argv[1]
    rows = C.load_index()
    if mode.startswith('one:'):
        cap = mode[4:]
        sel = [r for r in rows if r['cap'] == cap] or [dict(cap=cap)]
        res = check_run(sel[0])
        print(json.dumps(res, indent=1))
        return
    if mode == 'b0':      # v13 B0: the 120 tuning runs and the 35 old evaluation lead-braking runs
        sel = [r for r in rows if r['set'] == 'tune' or (r['set'] == 'fit' and r['family'] == 'lead_braking')]
    else:
        sel = select20(rows) if mode == 'sel20' else rows
    out = C.OUT / (sys.argv[2] if len(sys.argv) > 2 else 'harness_match_%s_v02.csv' % mode)
    done = set()
    if out.exists():
        with open(out, encoding='utf-8', newline='') as f:
            done = {(x['set'], x['archive']) for x in csv.DictReader(f)}
    else:
        with open(out, 'w', encoding='utf-8', newline='') as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()
    for i, r in enumerate(sel):
        if (r['set'], r['archive']) in done:
            continue
        try:
            res = check_run(r)
        except Exception as e:                                   # keep going, record the failure
            res = {k: r.get(k) for k in ('set', 'archive', 'case_id', 'family', 'occluder', 'desired_mps', 'frames', 'contact')}
            res['note'] = 'ERROR ' + repr(e)[:300]
        with open(out, 'a', encoding='utf-8', newline='') as f:
            csv.DictWriter(f, fieldnames=FIELDS).writerow({k: res.get(k, '') for k in FIELDS})
        print(i + 1, len(sel), r['archive'], 'frames', res.get('det_frames_exact'), '/', res.get('det_frames'),
              'tracks', res.get('tracks_exact'), '/', res.get('tracks_logged'), 'dec', res.get('decisions_exact'), '/',
              res.get('decisions'), 'actors', res.get('actors_exact'), '/', res.get('actors_logged'), res.get('note'), flush=True)


if __name__ == '__main__':
    main()
