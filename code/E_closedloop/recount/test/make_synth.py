"""Synthetic closed-loop runs in the truth/frames format, for testing e_recount_v01.py (not for results).
usage: python -I -B make_synth.py <out_runs_dir>"""
import json, math, sys
from pathlib import Path
import numpy as np

DT = 0.05
N = 700
KS = 99          # assessment start tick
BASE = 1000


def box(cx, cy):
    return dict(center_rh=[cx, cy, 0.8], route_yaw_rh=0.0, forward_support_m=2.4, backward_support_m=2.4,
                left_support_m=1.0, right_support_m=1.0)


def write_run(root, rid, case, arm, level, g, desired, ego_x, ego_v, ego_a, lead_x, lead_v, fallback, contact_k=None,
              lead_variant=None, status='CAPTURED_AND_REVIEWED', policy_failure=False, model_state=None, lat=0.0):
    run = root / rid
    cap = run / 'x' / rid / 'capture' / case
    cap.mkdir(parents=True, exist_ok=True)
    n = len(ego_x) if contact_k is None else contact_k + 1
    truth = []
    for k in range(n):
        gap = lead_x[k] - ego_x[k] - 4.8
        if contact_k is not None and k == contact_k:
            gap = -0.01
        ev = ego_v[k] if not (contact_k is not None and k == contact_k) else 0.0   # post-impulse speed at the contact tick
        truth.append(dict(k=k, frame=BASE + 1 + k, ego=dict(derived=box(ego_x[k], 0.0), velocity_lh=[ev, 0.0, 0.0]),
                          target=dict(derived=box(lead_x[k], lat), velocity_lh=[lead_v[k], 0.0, 0.0]), directional_gap_m=gap))
    frames = []
    for k in range(n):
        fr = dict(k=k, state=dict(speed=float(ego_v[k])), acceleration=float(ego_a[k]), execution={})
        if k % 2 == 1:
            ms = model_state(k) if model_state else dict(model_speed_mps=float(ego_v[k]), model_acceleration_mps2=float(ego_a[k]))
            fr['execution'] = dict(new_decision=dict(tick=k, mode='warmup' if k < KS else 'assessment',
                                                     model_state=ms, output=dict(fallback=bool(fallback(k)))))
        frames.append(fr)
    with open(cap / 'evaluation_truth.jsonl', 'w') as f:
        f.writelines(json.dumps(t) + '\n' for t in truth)
    with open(cap / 'frames.jsonl', 'w') as f:
        f.writelines(json.dumps(t) + '\n' for t in frames)
    if contact_k is not None:
        with open(cap / 'contacts.jsonl', 'w') as f:
            f.write(json.dumps(dict(frame=BASE + 1 + contact_k, other_id=2)) + '\n')
    c = ego_x[n - 1] - ego_x[KS]
    out = dict(base_frame=BASE, assessment_start_frame=BASE + 1 + KS, assessment_end_frame=BASE + 1 + N - 1,
               first_contact_frame=None if contact_k is None else BASE + 1 + contact_k, first_policy_failure_frame=None,
               forward_displacement_m=float(c), invalid_reasons=[], instrument_failures=[],
               termination='FULL_ASSESSMENT' if contact_k is None else 'FIRST_PHYSICAL_CONTACT')
    (cap / 'assessment_outcomes.json').write_text(json.dumps(out))
    cd = dict(case=dict(desired_mps=desired, draw=dict(family='lead_braking'), id=case))
    if lead_variant:
        cd['case']['lead_variant'] = lead_variant
    (cap / 'contract.json').write_text(json.dumps(cd))
    (cap / 'ARM_METHOD_v01.json').write_text(json.dumps(dict(arm=arm, knobs=dict(g=g, triple=None, brake_from_k=None))))
    if policy_failure:
        (cap / 'policy_failure.json').write_text('{}')
    summ = dict(status=status, job=rid.split('__r')[0], case=case, arm=arm, attempt=1,
                e_job=dict(g=g, triple=None, level=level, tracker=None))
    (run / 'SUMMARY.json').write_text(json.dumps(summ))


def braking_run(v0, brake_k, decel, lead_gap0, desired=None):
    """Ego cruises at v0, brakes at constant decel from tick brake_k (speed to zero), lead stopped lead_gap0 ahead."""
    ego_x = np.zeros(N); ego_v = np.zeros(N); ego_a = np.zeros(N)
    v = v0; x = 0.0
    for k in range(N):
        ego_x[k] = x; ego_v[k] = v
        a = -decel if (k >= brake_k and v > 0) else 0.0
        ego_a[k] = a
        vn = max(v + a * DT, 0.0)
        x += 0.5 * (v + vn) * DT
        v = vn
    lead_x = np.full(N, 4.8 + lead_gap0 + 0.0)
    lead_v = np.zeros(N)
    # first tick with gap <= 0
    gaps = lead_x - ego_x - 4.8
    ck = next((int(i) for i in np.flatnonzero(gaps <= 0)), None)
    return ego_x, ego_v, ego_a, lead_x, lead_v, ck


def main(out):
    root = Path(out)
    # ---- E1 brake runs: plant = exact planner-like stop (constant -5, jerk ramp), "weak" plant at -3.5
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    import e_recount_v01 as R
    for tag, speeds, scale in (('good', (5, 10, 15), 1.0), ('weak', (5, 10, 15), 0.7)):
        for sp in speeds:
            ego_x = np.zeros(N); ego_v = np.zeros(N); ego_a = np.zeros(N)
            v = float(sp); x = 0.0; a = 0.0; kf = 199
            for k in range(N):
                ego_x[k] = x; ego_v[k] = v; ego_a[k] = a
                tgt = -5.0 * scale if k >= kf else 0.0
                a += float(np.clip(tgt - a, -8 * DT, 8 * DT))
                vn = max(v + a * DT, 0.0)
                x += 0.5 * (v + vn) * DT; v = vn
            rid = 'e1_%s_v%d' % (tag, sp)
            if tag == 'weak' and sp != 15:
                continue
            write_run(root / ('brake_' + tag), rid, 'c_brake_%d' % sp, 'E_BRAKE', None, None, float(sp), ego_x, ego_v, ego_a,
                      np.full(N, 1e4), np.zeros(N), lambda k: k >= kf, lat=9.0)
    # weak set also needs good 5 and 10 so the pass rule fails only on the 15 m/s run
    for sp in (5, 10):
        ego_x = np.zeros(N); ego_v = np.zeros(N); ego_a = np.zeros(N)
        v = float(sp); x = 0.0; a = 0.0; kf = 199
        for k in range(N):
            ego_x[k] = x; ego_v[k] = v; ego_a[k] = a
            a += float(np.clip((-5.0 if k >= kf else 0.0) - a, -8 * DT, 8 * DT))
            vn = max(v + a * DT, 0.0); x += 0.5 * (v + vn) * DT; v = vn
        write_run(root / 'brake_weak', 'e1_weak_v%d' % sp, 'c_brake_%d' % sp, 'E_BRAKE', None, None, float(sp), ego_x, ego_v, ego_a,
                  np.full(N, 1e4), np.zeros(N), lambda k: k >= kf, lat=9.0)

    # ---- outcome runs: lead stopped 60 m ahead, speed 15 -> contact depends on braking decel
    # (arm, level, case) -> decel; E2 runs: E_F0 at g in grid over 20 cases
    grid = [0, 0.25, 1, 4, 16, 64]
    contact_share = {0: 0.5, 0.25: 0.35, 1: 0.2, 4: 0.1, 16: 0.05, 64: 0.0}    # of 20 cases
    e2 = root / 'e2'
    for g in grid:
        nc = int(round(contact_share[g] * 20))
        for i in range(20):
            decel = 2.0 if i < nc else 6.0
            ego_x, ego_v, ego_a, lead_x, lead_v, ck = braking_run(15.0, 150, decel, 160.0)
            write_run(e2, 'e2_F0_g%s_c%02d' % (str(g).replace('.', 'p'), i), 'case%02d' % i, 'E_F0', None, g, 15.0, ego_x, ego_v, ego_a,
                      lead_x, lead_v, lambda k: k > 150 and decel > 3, contact_k=ck)
    # one retried job (last attempt of record): first attempt invalid, __r1 valid
    ego_x, ego_v, ego_a, lead_x, lead_v, ck = braking_run(15.0, 150, 6.0, 160.0)
    write_run(e2, 'e2_F0_g64_c00__r1', 'case00', 'E_F0', None, 64, 15.0, ego_x, ego_v, ego_a, lead_x, lead_v, lambda k: False, contact_k=ck)
    write_run(e2, 'e2_F0_g64_c00', 'case00', 'E_F0', None, 64, 15.0, ego_x, ego_v, ego_a, lead_x, lead_v, lambda k: False, contact_k=ck,
              status='FAILED')

    # ---- e3: 20 cases; F0 contact in cases 0..7 at lo (decel 2), arm N contact in 0..3 (4 of F0's), CK3 in 0..9, etc.
    e3 = root / 'e3'
    spec = {  # arm: {level: number of contact cases (first n cases), extra shift}
        ('E_F0', 'lo'): 8, ('E_N', 'lo'): 8, ('E_CK3', 'lo'): 2, ('E_TG', 'lo'): 6, ('E_PS', 'lo'): 8,
        ('E_F0_IMM', 'lo'): 8, ('E_N_IMM', 'lo'): 9,
        ('E_F0', 'hi'): 2, ('E_N', 'hi'): 2, ('E_CK3', 'hi'): 0, ('E_TG', 'hi'): 1, ('E_PS', 'hi'): 2,
        ('E_F0_IMM', 'hi'): 2, ('E_N_IMM', 'hi'): 2}
    for (arm, lv), nc in spec.items():
        for i in range(20):
            decel = 2.0 if i < nc else 6.0
            # no-contact runs: arm CK3 brakes earlier -> some time lost
            bk = 150 if arm != "E_CK3" else 140
            ego_x, ego_v, ego_a, lead_x, lead_v, ck = braking_run(15.0, bk, decel, 160.0)
            write_run(e3, 'e3_%s_%s_c%02d' % (arm, lv, i), 'case%02d' % i, arm, lv, 1.0, 15.0, ego_x, ego_v, ego_a, lead_x, lead_v,
                      lambda k: False, contact_k=ck)
    for i in range(20):
        ego_x, ego_v, ego_a, lead_x, lead_v, ck = braking_run(15.0, 150, 2.0 if i < 12 else 6.0, 160.0)
        write_run(e3, 'e3_E_Z_c%02d' % i, 'case%02d' % i, 'E_Z', None, 0, 15.0, ego_x, ego_v, ego_a, lead_x, lead_v, lambda k: False, contact_k=ck)
    # ---- e3b: two lead variants
    e3b = root / 'e3b'
    for lv, ncs in (('slow', {'E_F0': 4, 'E_N': 4, 'E_CK3': 1, 'E_PS': 4, 'E_TG': 4}), ('cruise', {'E_F0': 0, 'E_N': 0, 'E_CK3': 0, 'E_PS': 0, 'E_TG': 0})):
        for arm, nc in ncs.items():
            for i in range(10):
                ego_x, ego_v, ego_a, lead_x, lead_v, ck = braking_run(15.0, 150, 2.0 if i < nc else 6.0, 160.0)
                write_run(e3b, 'e3b_%s_%s_c%02d' % (arm, lv, i), 'b%s%02d' % (lv, i), arm, 'lo', 1.0, 15.0, ego_x, ego_v, ego_a, lead_x, lead_v,
                          lambda k: False, contact_k=ck, lead_variant=lv)
    print('synthetic runs written to', root)


if __name__ == '__main__':
    main(sys.argv[1])
