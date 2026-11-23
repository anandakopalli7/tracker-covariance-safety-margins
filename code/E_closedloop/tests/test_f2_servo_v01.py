"""E0 laptop check of F2: e_arms_v01.F2Servo equals the stand-in's FixServo with F2 on and F3 off
(P\\09_redesign\\m3_plant_surrogate\\surrogate_v01.py L274-306, RunState.feedforward L257-265), term for term, on a
closed-loop sequence: warm-up at the desired speed, cruise plans from tick 99, the (-5, -5) fallback from tick 199
(the stand-in's STOP mode), the stand-in's car model (plant_v01.Plant) as the plant. Both servos see the same measured
speed and acceleration (those produced by the stand-in servo's pedal). Also reports the stopping distance on the
stand-in car against the planner's model, as a plausibility figure (the stand-in's own result was 3.95 / 12.68 / 26.24 m).
Writes tests\\out\\TEST_F2_SERVO_v01.json.
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import json, pathlib, sys, types
import numpy as np

E = pathlib.Path(__file__).resolve().parents[1]
PK = E / 'packets' / 'dev_packet_e_v01' / 'claude_smoke_v01'
W = pathlib.Path(r'<library folder>')
M3 = pathlib.Path(r'<library folder>\m3_plant_surrogate')
SHIMS = pathlib.Path(r'<library folder>\shims_v01')
os.environ['CLAUDE_SMOKE_WORKSPACE_ROOT'] = str(W)
sys.path.insert(0, str(PK)); sys.path.append(str(SHIMS)); sys.dont_write_bytecode = True
import e_arms_v01 as earms           # noqa: E402
sys.path.insert(0, str(M3))
import surrogate_v01 as S            # noqa: E402
import plant_v01 as PL               # noqa: E402
from consumer import command_bytes   # noqa: E402
from design_core_v85 import trajectory   # noqa: E402

MAX_STEER = 1.2217303432379762
KEYS = ('control', 'pedal', 'unclamped_pedal', 'integral_state', 'integral_trial', 'integration_blocked', 'stop_hold',
        'acceleration_reference_mps2', 'acceleration_error_mps2')


def run(desired, brake_k=199, K=460):
    st = S.RunState(fixes=('F2',), margin='fixed')
    ref = S.FixServo(MAX_STEER, st)
    ctx = types.SimpleNamespace(f2_plan=None)
    mine = earms.F2Servo(MAX_STEER, ctx, earms.PlantInverse(json.loads((PK / 'E_F2_PLANT_v01.json').read_text())['params']))
    car = PL.Plant(v0=desired)
    v, a = float(desired), 0.
    mism = 0; n = 0; first = {}
    xs = [0.]; vs = [v]; kf = None; d_model = None
    for k in range(-1, K):
        if k == -1 or k % 2 == 1:
            if k < 99:
                wire = command_bytes(float(desired)); st.plan = None; ctx.f2_plan = None
            else:
                tg = (-5., -5.) if k >= brake_k else (0., 0.)
                tr = trajectory(tg[0], tg[1], max(v, 0.), a, float(desired))
                wire = command_bytes(tr['command_speed'])
                st.plan = dict(k=k, a_cmd=np.asarray(tr['a'], float), v=tr['v'], fallback=tg == (-5., -5.))
                ctx.f2_plan = dict(k=k, a_cmd=np.asarray(tr['a'][:2], float))
                if k >= brake_k and kf is None:
                    kf = k; d_model = float(trajectory(-5., -5., max(v, 0.), a, float(desired), h=.05, H=12.)['s'][-1]); x_f = car.x
            ref.receive(wire, k, v); mine.receive(wire, k, v)
        r1 = ref.step(k, v, a); r2 = mine.step(k, v, a)
        n += 1
        same = all(r1[key] == r2[key] for key in KEYS) and r1['feedforward'] == r2['f2_feedforward_pedal']
        if not same:
            mism += 1
            if not first: first = dict(k=k, ref={key: r1[key] for key in KEYS}, mine={key: r2[key] for key in KEYS})
        c = r1['control']
        v, a = car.step(c['throttle'], c['brake'])
        xs.append(car.x); vs.append(v)
        if kf is not None and v < .05 and 'ks' not in locals():
            ks = k; d_real = car.x - x_f
    out = dict(desired=desired, ticks=n, mismatches=mism, first_mismatch=first or None, brake_k=brake_k, first_fallback_k=kf,
               model_dist_m=d_model)
    if 'ks' in locals():
        out.update(standstill_k=ks, standin_car_dist_m=d_real, ratio=d_real / d_model)
    return out


def main():
    res = [run(v) for v in (5., 10., 15.)]
    out = dict(schema='E_TEST_F2_SERVO_V01', runs=res, all_equal=all(r['mismatches'] == 0 for r in res))
    (E / 'tests' / 'out').mkdir(exist_ok=True)
    (E / 'tests' / 'out' / 'TEST_F2_SERVO_v01.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
