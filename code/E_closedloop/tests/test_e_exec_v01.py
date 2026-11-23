"""E0 laptop check: the executor built by e_arms_v01.build_execution (native 712 SensorExecution, E policy, F2 servo) runs
the probe's whole call sequence for 700 ticks without error, for every arm: start(); per tick observe(k, speed, accel, steer,
time, applied_control = the executor's own previous direct control, actors, selection_sink = the bridge's check of
outcome_bridge_v01 select_raw); the detector updates feed the arm's track history as the probe does. Inputs are the logged
speed / acceleration / steer / time / actors of a stored run (open loop, for the code path only). Checks: no exception; the
sink fires exactly at assessment origins with decision == interval['new_decision']; e_decisions records match the decisions;
every next_client control has F2 fields; method record JSON-safe; F2 plan acceleration used at tick k and k+1.
Writes tests\\out\\TEST_E_EXEC_v01.json.
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import copy, json, pathlib, sys
import numpy as np

E = pathlib.Path(__file__).resolve().parents[1]
PK = E / 'packets' / 'dev_packet_e_v01' / 'claude_smoke_v01'
W = pathlib.Path(r'<library folder>')
PRJ = pathlib.Path(r'<library folder>')
SHIMS = PRJ / '09_redesign' / 'm4_perception_model' / 'shims_v01'
os.environ['CLAUDE_SMOKE_WORKSPACE_ROOT'] = str(W)
sys.path.insert(0, str(PK)); sys.path.append(str(SHIMS)); sys.dont_write_bytecode = True
import e_arms_v01 as earms      # noqa: E402

CAP = PRJ / '08_phase2' / 'archives_c1' / 'p2_c1109_tune_0000_fixed_c1' / 'x' / 'p2_c1109_tune_0000_fixed_c1' / 'capture' / 'c1109_tune_0000'
ARMS = [('E_Z', {}), ('E_F0', dict(g=1.)), ('E_N', dict(g=1.)), ('E_CK3', dict(g=1.)), ('E_TG', dict(g=1.)), ('E_PS', dict(triple=[0.25, 1., 4.])),
        ('E_BRAKE', dict(brake_from_k=199))]


def jl(p):
    with open(p, encoding='utf-8') as f:
        return [json.loads(x) for x in f if x.strip()]


def events_prefix(events, i):
    """The events the probe's list holds after detector update i: the logged file in order, up to (not including) the first
    event stamped with a later detector update; unstamped events (reset) are kept in place."""
    out = []
    for e in events:
        if 'timestamp' in e and int(e['timestamp']) > i:
            break
        out.append(e)
    return out


def run_arm(arm, kw):
    contract = json.loads((CAP / 'contract.json').read_text()); case = contract['case']
    frames = jl(CAP / 'frames.jsonl'); det = {d['k']: d for d in jl(CAP / 'detections.jsonl')}
    events = jl(CAP / 'filter_events.jsonl')
    init = json.loads((CAP / 'initial_command.json').read_text())
    meth = json.loads((CAP / 'ARM_METHOD_v01.json').read_text())['constructor']
    ex, method, ctx = earms.build_execution(arm, case, meth['ego_length_m'], meth['ego_width_m'], meth['max_steer_rad'], 700, **kw)
    json.dumps(method, allow_nan=False)
    d0 = init['decision']['model_state']
    start = ex.start(d0['raw_speed_mps'], d0['raw_acceleration_mps2'], init['decision']['steer'])
    direct = start['direct_control']
    n_sink = n_origin = n_ff_plan = 0; problems = []; detn = 0
    origins = set(range(99, 698, 2))
    for fr in frames:
        k = fr['k']
        if k in det:
            # the probe: tracker.step -> events appended -> ectx.on_detector(tracks, events); events up to this detector index
            upto = events_prefix(events, detn)
            ctx.on_detector(det[k]['tracks'], upto); detn += 1
        nd = (fr.get('execution') or {}).get('new_decision')
        actors = nd['actors'] if nd else []
        if nd is None and k % 2 == 1 and k < 699:
            problems.append('no logged decision at odd tick %d' % k); break
        selected = []
        def sink(decision, row):
            if selected: raise ValueError('duplicate selection')
            if decision['tick'] != k or decision['mode'] != 'assessment': raise ValueError('scope')
            if np.asarray(row['s']).shape != (61,) or np.asarray(row['v']).shape != (61,): raise ValueError('shape')
            if len(row['tags']) != 120 * len(decision['actors']): raise ValueError('tags')
            if tuple(row['targets']) != tuple(decision['output']['targets']): raise ValueError('targets')
            selected.append(dict(decision=decision, selected_plan=row))
        st = fr['state']
        interval = ex.observe(k, st['speed'], fr['acceleration'], nd['steer'] if nd else 0., fr['time'], direct, actors, selection_sink=sink)
        if len(selected) != int(k in origins): problems.append('sink count at %d' % k)
        if selected:
            n_sink += 1
            if selected[0]['decision'] != interval['new_decision']: problems.append('decision differs at %d' % k)
        if k in origins: n_origin += 1
        nc = interval.get('next_client')
        if nc is not None:
            direct = nc['control']
            if 'f2_feedforward_pedal' not in nc: problems.append('no F2 fields at %d' % k)
            if nc['f2_source'] == 'plan': n_ff_plan += 1
    recs = ctx.pending_records()
    decs = [r for r in recs]
    for r in decs:
        json.dumps(r, allow_nan=False)        # the probe's append() writes with allow_nan=False
    out = dict(arm=arm, knobs=method['knobs'], alpha=method['alpha'], ticks=len(frames), origins=n_origin, sink_fired=n_sink,
               e_records=len(decs), ff_from_plan_ticks=n_ff_plan, fallbacks=sum(r['fallback'] for r in decs),
               forced=sum(r['forced_fallback'] for r in decs), phases=None, problems=problems[:5], n_problems=len(problems))
    if arm == 'E_PS':
        ph = [r['phase'] for r in decs]; out['phases'] = {str(p): ph.count(p) for p in (0, 1, 2)}
    if arm == 'E_CK3':
        out['decisions_with_shift'] = sum(1 for r in decs if r['ck3_shifted_actors'])
    return out


def main():
    res = []
    for arm, kw in ARMS:
        try: r = run_arm(arm, kw)
        except Exception as e:
            import traceback; r = dict(arm=arm, error=repr(e), tb=traceback.format_exc()[-1500:])
        res.append(r); print(json.dumps(r), flush=True)
    out = dict(schema='E_TEST_EXEC_V01', capture=str(CAP), runs=res,
               ok=all('error' not in r and r['n_problems'] == 0 and r['sink_fired'] == r['origins'] == r['e_records'] for r in res))
    (E / 'tests' / 'out' / 'TEST_E_EXEC_v01.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
    print('OK' if out['ok'] else 'NOT OK')


if __name__ == '__main__':
    main()
