"""E1 brake test (A10 7.1): does the car with F2 stop within 10% of the planner's own model at 5, 10 and 15 m/s?

Writer: session E (Claude Opus 5.5). Rule pre-set on 10 Nov 2026 (P\\09_redesign\\DESIGN_NOTES_v01.md 6.4e item 1):
stopping distance from the first fallback decision within 10% of the planner's model at all three speeds, and no policy
failure or halted job.

Per brake run (an E_BRAKE capture: E_Z until decision tick 199, then the fallback at every decision):
  kf       the first assessment decision whose output is the fallback (e_decisions.jsonl / frames.jsonl)
  v0, a0   that decision's model speed and acceleration (the planner's own state at kf)
  d_model  design_core_v85.trajectory(-5, -5, v0, a0, desired, h=.05, H=12)['s'][-1]  (the stand-in's model_stop,
           m3_plant_surrogate\\eval_fixes_v01.py L86-91)
  ks       the first tick >= kf whose measured speed (frames.jsonl state.speed, the speed the servo sees) is < 0.05 m/s
  d_real   route projection of the truth ego centre at ks minus that at kf (evaluation_truth.jsonl)
  ratio    d_real / d_model; a speed passes iff |ratio - 1| <= 0.10
Descriptive: time to stop, delay from kf to the first measured acceleration <= -3 m/s^2, peak deceleration and peak
jerk of the measured acceleration between kf and ks, the F2 feed-forward share of the pedal.
The test passes iff all three speeds pass, no run has a policy-failure file (a contact is reported but is not part of the rule), and every run's status is
CAPTURED_AND_REVIEWED (the job-level halts are read from the worker status by the caller).

Usage: python -I e1_brake_v01.py <run_dir> [<run_dir> ...]   (run_dir = extracted archive folder x/<run_id>)
"""
import json, math, pathlib, sys

DESIGN_CORE = pathlib.Path(r'<library folder>\vendor')
sys.path.insert(0, str(DESIGN_CORE))
from design_core_v85 import trajectory   # noqa: E402

TOL = 0.10


def jl(p):
    with open(p, encoding='utf-8') as f:
        return [json.loads(x) for x in f if x.strip()]


def one(run_dir):
    run_dir = pathlib.Path(run_dir)
    summ = json.loads((run_dir / 'SUMMARY.json').read_text(encoding='utf-8'))
    cap = next((run_dir / 'capture').iterdir())
    method = json.loads((cap / 'ARM_METHOD_v01.json').read_text(encoding='utf-8'))
    assert method['arm'] == 'E_BRAKE', 'not a brake run'
    desired = float(method['constructor']['desired_mps'])
    frames = jl(cap / 'frames.jsonl'); truth = {t['k']: t for t in jl(cap / 'evaluation_truth.jsonl')}
    decs = [(fr['k'], fr['execution']['new_decision']) for fr in frames
            if fr.get('execution') and fr['execution'].get('new_decision') and fr['execution']['new_decision']['mode'] == 'assessment']
    fb = [(k, d) for k, d in decs if d['output']['fallback']]
    out = dict(run=run_dir.name, case=summ['case'], desired_mps=desired, status=summ['status'],
               policy_failure=(cap / 'policy_failure.json').exists(), contact=(cap / 'contacts.jsonl').exists(),
               brake_from_k=method['knobs']['brake_from_k'])
    if not fb:
        out.update(passed=False, reason='no fallback decision'); return out
    kf, d0 = fb[0]
    out['first_fallback_k'] = kf; out['fallback_before_forced'] = kf < method['knobs']['brake_from_k']
    v0 = float(d0['model_state']['model_speed_mps']); a0 = float(d0['model_state']['model_acceleration_mps2'])
    d_model = float(trajectory(-5., -5., v0, a0, desired, h=.05, H=12.)['s'][-1])
    speed = {fr['k']: float(fr['state']['speed']) for fr in frames}
    acc = {fr['k']: float(fr['acceleration']) for fr in frames}
    ks = next((k for k in sorted(speed) if k >= kf and speed[k] < .05), None)
    yaw = float(truth[kf]['ego']['derived']['route_yaw_rh']); ux, uy = math.cos(yaw), math.sin(yaw)
    proj = lambda k: float(truth[k]['ego']['derived']['center_rh'][0]) * ux + float(truth[k]['ego']['derived']['center_rh'][1]) * uy
    out.update(v_at_fallback=v0, a_at_fallback=a0, model_dist_m=d_model)
    if ks is None or ks not in truth:
        out.update(passed=False, reason='no standstill within the run'); return out
    d_real = proj(ks) - proj(kf)
    seg = [acc[k] for k in range(kf, ks + 1)]
    k3 = next((k for k in range(kf, ks + 1) if acc[k] <= -3.), None)
    jerk = [abs(seg[i + 1] - seg[i]) / .05 for i in range(len(seg) - 1)]
    ratio = d_real / d_model
    out.update(standstill_k=ks, stop_dist_m=d_real, ratio_real_to_model=ratio, stop_time_s=(ks - kf) * .05,
               delay_to_3_s=None if k3 is None else (k3 - kf) * .05, peak_decel_mps2=-min(seg), peak_jerk_mps3=max(jerk) if jerk else None,
               within_tolerance=abs(ratio - 1.) <= TOL)
    # A natural fallback before the forced one (tick brake_from_k) means the stop did not start from steady cruise as designed:
    # the run is not a valid brake test (a fault to inspect, not a result) - review finding Minor 1.
    out['passed'] = bool(out['within_tolerance'] and not out['policy_failure'] and out['status'] == 'CAPTURED_AND_REVIEWED'   # a contact is reported, not a criterion (A10 7.1)
                         and not out['fallback_before_forced'])
    return out


def main():
    rows = [one(p) for p in sys.argv[1:]]
    speeds = sorted(r['desired_mps'] for r in rows)
    verdict = dict(schema='E1_BRAKE_TEST_V01', tolerance=TOL, runs=rows,
                   speeds_covered=speeds, all_three_speeds=speeds == [5., 10., 15.],
                   passed=bool(speeds == [5., 10., 15.] and all(r.get('passed') for r in rows)))
    print(json.dumps(verdict, indent=1))


if __name__ == '__main__':
    main()
