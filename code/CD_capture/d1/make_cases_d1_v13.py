"""Package D1 case file and protocol (revision v13, AMENDMENT_10_v13.md sec. 6, D1).

55 new cases per variant (constant, mild_braking, stop_and_go), drawn by numpy default_rng(20261921) from the
lead-braking draw law (C1109 sampler, P\\06_phase0\\scenarios\\SAMPLER_C1109_v01.py) for the Draw fields, with the
desired speed cycling 5/10/15 by index and one extra draw for the mild-braking deceleration:
  per case, in this order: side = choice([-1, 1]); tau, brake_start, braking, ttc, duration, forward, lateral =
  uniform over (1,3), (1,3), (2,6), (1,4), (1,3), (10,60), (5,10); crossing = uniform(3, 10); mild_decel = uniform(0.5, 1.5).
  Variants are drawn in the order constant (55), mild_braking (55), stop_and_go (55); every case consumes the same draws.
Identity (as C1109's new_case): identity = 'D1V13/<kind>/finite/<i>'; seed_hex = sha256(identity); seed = int(seed_hex[:8], 16);
noise_episode = paired_condition = repeat_group = identity; family lead_braking; reactive true; occluder false.
Cases 0-34 of each variant: role d1_openloop (D1, 105 runs). Cases 35-54: role d1_e3b (E3b's closed-loop cases).
Reserves (added 19 Nov 15:00 EST, before any D1 run, after the independent review): cases 55-59 of each variant, role
d1_reserve, drawn by CONTINUING the same generator after all 165 cases above (same per-case draw order, variants in the same
order), so the 165 cases are unchanged; used only by the sec. 5.1 failure rule (next unused case of the same variant and speed).
Pilots (role d1_pilot, not study runs): ids d1v13pilot_<kind>, the canonical lead-braking draw of the main protocol
(canonical_lead_braking_v10_r0_finite: 10 m/s, tau 2, brake start 2 s, 4 m/s^2) with identity 'D1V13/pilot/<kind>', mild
deceleration 1.0; run first to check that the actor PID realises each profile (restart after the hold, ramps).
lead_variant (actor_policy_d1_v01.py): constant (no parameters); mild_braking (start_s = brake_start, decel = mild_decel,
floor 0.5); stop_and_go (start_s = brake_start, decel = braking, hold 3 s, resume 1.5 m/s^2).

Writes (never overwrites): CASES_D1_v13.json and DEVELOPMENT_PROTOCOL_D1_v13.json (= the main protocol with the 165
cases (165 study + 15 reserve + 3 pilot) appended and a 'claude_v13_d1_derivation' record). Usage: python -I -B make_cases_d1_v13.py
"""
import dataclasses, hashlib, json, pathlib, sys
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
P = pathlib.Path(r'<library folder>')
W = pathlib.Path(r'<library folder>')
MAIN = P / '06_phase0' / 'scenarios' / 'DEVELOPMENT_PROTOCOL_MAIN_v01.json'
MAIN_SHA = '32d683a0a8ca2e91ff0245759ad78b43e7953c33bd12847c5193cafcdaa5735d'
sys.dont_write_bytecode = True
sys.path[:0] = [str(HERE / 'src'), str(W / '746_actual_actor_policy_development_20261103')]
from actor_policy_v01 import Draw                      # noqa: E402  (read-only import of the 746 policy)
import actor_policy_d1_v01 as d1                        # noqa: E402

SEED = 20261921
KINDS = ('constant', 'mild_braking', 'stop_and_go')
N = 55
N_OPEN = 35
N_RESERVE = 5


def sha(b): return hashlib.sha256(b).hexdigest()
def sdict(d): return {k: (sdict(v) if isinstance(v, dict) else v) for k, v in sorted(d.items())}


def variant_record(kind, brake_start, braking, mild_decel):
    if kind == 'constant':
        v = dict(start_s=None, decel_mps2=None, floor_fraction=None, hold_s=None, resume_mps2=None)
    elif kind == 'mild_braking':
        v = dict(start_s=brake_start, decel_mps2=mild_decel, floor_fraction=0.5, hold_s=None, resume_mps2=None)
    else:
        v = dict(start_s=brake_start, decel_mps2=braking, floor_fraction=None, hold_s=3.0, resume_mps2=1.5)
    return sdict(dict(schema=d1.SCHEMA, kind=kind, **v))


def role_of(i):
    return 'd1_openloop' if i < N_OPEN else ('d1_e3b' if i < N else 'd1_reserve')


def build():
    rng = np.random.default_rng(SEED)
    cases = []
    for kind, i in [(k, i) for k in KINDS for i in range(N)] + [(k, i) for k in KINDS for i in range(N, N + N_RESERVE)]:
        if True:
            v = (5, 10, 15)[i % 3]
            side = int(rng.choice([-1, 1]))
            tau, brake_start, braking, ttc, duration, forward, lateral = [float(rng.uniform(a, b)) for a, b in
                                                                          ((1, 3), (1, 3), (2, 6), (1, 4), (1, 3), (10, 60), (5, 10))]
            crossing = float(rng.uniform(3, 10))
            mild_decel = float(rng.uniform(0.5, 1.5))
            identity = f'D1V13/{kind}/finite/{i}'
            seed_hex = sha(identity.encode())
            d = Draw('lead_braking', float(v), side, tau, brake_start, braking, ttc, crossing, duration, forward, lateral, False, seed_hex)
            draw = sdict(dataclasses.asdict(d))
            variant = variant_record(kind, brake_start, braking, mild_decel)
            d1.check_variant(variant, draw)
            cases.append(sdict(dict(consumer='finite', desired_mps=v, draw=draw, fresh_process_required=True, id=f'd1v13_{kind}_{i:04d}',
                                    lead_variant=variant, main_study_eligible=True, noise_episode=identity, paired_condition=identity,
                                    reactive=True, repeat=0, repeat_group=identity, role=role_of(i),
                                    seed=int(seed_hex[:8], 16))))
    return cases


def pilots(main_protocol):
    canon = next(c for c in main_protocol['cases'] if c['id'] == 'canonical_lead_braking_v10_r0_finite')
    out = []
    for kind in KINDS:
        identity = f'D1V13/pilot/{kind}'; seed_hex = sha(identity.encode())
        draw = dict(canon['draw'], seed_hex=seed_hex); d = Draw(**draw); draw = sdict(dataclasses.asdict(d))
        variant = variant_record(kind, d.brake_start_s, d.brake_mps2, 1.0); d1.check_variant(variant, draw)
        out.append(sdict(dict(consumer='finite', desired_mps=int(d.desired_mps), draw=draw, fresh_process_required=True, id=f'd1v13pilot_{kind}',
                              lead_variant=variant, main_study_eligible=False, noise_episode=identity, paired_condition=identity,
                              reactive=True, repeat=0, repeat_group=identity, role='d1_pilot', seed=int(seed_hex[:8], 16))))
    return out


def main():
    raw = MAIN.read_bytes(); assert sha(raw) == MAIN_SHA
    main_protocol = json.loads(raw)
    cases = build() + pilots(main_protocol)
    old = HERE / 'superseded' / 'CASES_D1_v13_v01_reviewed.json'
    if old.exists():   # the 165 reviewed study cases must be unchanged
        assert json.loads(old.read_text(encoding='utf-8'))['cases'] == cases[:3 * N], 'study cases changed'
    ids = {c['id'] for c in main_protocol['cases']}
    seeds = {c['seed'] for c in main_protocol['cases']}; eps = {c['noise_episode'] for c in main_protocol['cases']}
    assert len({c['id'] for c in cases}) == len(cases) == 3 * (N + N_RESERVE) + 3 and not ids & {c['id'] for c in cases}
    assert len({c['seed'] for c in cases}) == len(cases) and not seeds & {c['seed'] for c in cases}, 'seed collision'
    assert not eps & {c['noise_episode'] for c in cases}
    case_file = dict(schema='CASES_D1_V13', amendment='AMENDMENT_10_v13.md sec. 6 D1', rng='numpy.random.default_rng(20261921)',
                     draw_order=__doc__.split('\n')[3:8],
                     additions=[l for l in __doc__.split('\n') if l.startswith(('Reserves', 'd1_reserve', 'order), so', 'Pilots', '(canonical_lead', 'deceleration 1.0'))],
                     variants=KINDS, per_variant=N, open_loop_per_variant=N_OPEN, reserves_per_variant=N_RESERVE, pilots=3,
                     main_protocol_sha256=MAIN_SHA, actor_policy='actor_policy_d1_v01.py', actor_policy_sha256=sha((HERE / 'src' / 'actor_policy_d1_v01.py').read_bytes()),
                     made_by=dict(script='make_cases_d1_v13.py', sha256=sha(pathlib.Path(__file__).read_bytes())), cases=cases)
    proto = dict(main_protocol)
    proto['cases'] = main_protocol['cases'] + cases
    proto['claude_v13_d1_derivation'] = dict(base='DEVELOPMENT_PROTOCOL_MAIN_v01.json', base_sha256=MAIN_SHA, appended_cases=len(cases),
                                             case_file='CASES_D1_v13.json', note='Revision v13 package D1: the main protocol unchanged, with 165 lead-variant cases appended.')
    out1 = HERE / 'CASES_D1_v13.json'; out2 = HERE / 'DEVELOPMENT_PROTOCOL_D1_v13.json'
    for path, obj in ((out1, case_file), (out2, proto)):
        with open(path, 'x', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(obj, indent=1, allow_nan=False) + '\n')
        print(path.name, sha(path.read_bytes()))
    assert json.loads(out2.read_bytes())['cases'][:len(main_protocol['cases'])] == main_protocol['cases']


if __name__ == '__main__':
    main()
