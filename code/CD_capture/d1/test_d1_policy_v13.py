"""Laptop checks of the D1 actor-policy version (no CARLA). python -I -B test_d1_policy_v13.py

1. Every D1 case validates; every main-protocol case gets the unchanged 746 ActorRequests from make_requests.
2. LeadVariantRequests.step returns the 746 step's record except requested_speed_mps / reason, for a synthetic
   frame sequence (inputs that 746 accepts), and its request follows the A10 sec. 6 law at every frame.
3. Profile checks per variant: constant = v; mild reaches and holds v/2 with slope -a; stop-and-go stops, holds 3 s,
   ramps at 1.5 m/s^2 back to v; requests are continuous (max step <= max(a, 1.5) * 0.05 + 1e-12).
4. A non-variant lead_braking case: make_requests and the 746 class give identical records frame by frame.
5. scene_actors_d1_v01.VariantScenarioActors.start is, token for token, scene_actors_v03.ScenarioActors.start with
   ActorRequests(self.draw,frame,reactive=reactive) replaced by LeadVariantRequests(..., variant=variant).
6. The two edited packet files differ from packet_main_v03 only in the documented lines.
Writes TEST_D1_POLICY_v13.json.
"""
import ast, json, math, pathlib, sys, difflib, tokenize, io

HERE = pathlib.Path(__file__).resolve().parent
P = pathlib.Path(r'<library folder>')
W = pathlib.Path(r'<library folder>')
V3 = P / '03_runbook' / 'packet_main_v03'
sys.dont_write_bytecode = True
sys.path[:0] = [str(HERE / 'src'), str(W / '746_actual_actor_policy_development_20261103')]
from actor_policy_v01 import ActorRequests, Draw, DT          # noqa: E402
import actor_policy_d1_v01 as d1                              # noqa: E402

results = {}


def frames_run(policy, first, n, v_of_frame=None):
    out = []
    for k in range(n):
        f = first + k
        x = 20.0 + 0.5 * k
        vel = [5.0, 0.0] if v_of_frame is None else [v_of_frame(k), 0.0]
        rec = policy.step(f, actor_center=[x, 0.0], actor_velocity=vel, rear_position=[x - 1.4, 0.0], rear_velocity=vel,
                          ego_center=[0.0, 0.0], ego_velocity=[5.0, 0.0], actor_half_diagonal=2.6, ego_half_diagonal=2.6)
        out.append((rec, policy.snapshot()))
    return out


def law(variant, v, t):
    k = variant['kind']
    if k == 'constant': return v
    a, t0 = variant['decel_mps2'], variant['start_s']
    if k == 'mild_braking': return max(0.5 * v, v - a * max(0.0, t - t0))
    ts = t0 + v / a
    if t < ts + 3.0: return max(0.0, v - a * max(0.0, t - t0))
    return min(v, 1.5 * (t - ts - 3.0))


def main():
    cases = json.loads((HERE / 'CASES_D1_v13.json').read_text(encoding='utf-8'))['cases']
    proto = json.loads((HERE / 'DEVELOPMENT_PROTOCOL_D1_v13.json').read_text(encoding='utf-8'))
    # 1
    n_variant = n_plain = 0
    for c in proto['cases']:
        if c['draw']['family'] not in ('lead_braking', 'stopped', 'pedestrian_crossing', 'vehicle_crossing', 'cutin', 'benign'): continue
        d = Draw(**c['draw'])
        p = d1.make_requests(c, d, 1000)
        if 'lead_variant' in c: assert type(p) is d1.LeadVariantRequests; n_variant += 1
        else: assert type(p) is ActorRequests; n_plain += 1
    results['1_make_requests'] = dict(variant_cases=n_variant, plain_cases=n_plain)
    # 2 + 3
    worst = {}
    for c in cases:
        d = Draw(**c['draw']); var = c['lead_variant']; v = d.desired_mps
        p = d1.make_requests(c, d, 500); base = ActorRequests(d, 500, reactive=True)
        recs = frames_run(p, 500, 700); brecs = frames_run(base, 500, 700)
        prev = None; maxstep = 0.0
        for (r, s), (br, bs) in zip(recs, brecs):
            t = r['assessment_time_s']; want = law(var, v, t)
            assert abs(r['requested_speed_mps'] - want) <= 1e-12, (c['id'], t)
            assert r['reason'] == 'lead_variant_' + var['kind']
            assert {k: r[k] for k in r if k not in ('requested_speed_mps', 'reason')} == {k: br[k] for k in br if k not in ('requested_speed_mps', 'reason')}
            assert s['lead_variant'] == var and s['schema'] == 'ACTOR_REQUESTS746_D1V13_V01' and s['request'] == r['requested_speed_mps']
            json.dumps(s, allow_nan=False); json.dumps(r, allow_nan=False)
            if prev is not None: maxstep = max(maxstep, abs(r['requested_speed_mps'] - prev))
            prev = r['requested_speed_mps']
        lim = (max(var['decel_mps2'] or 0, 1.5) if var['kind'] != 'constant' else 0) * DT + 1e-12
        assert maxstep <= lim, (c['id'], maxstep, lim)
        req = [r['requested_speed_mps'] for r, _ in recs]; ts = [r['assessment_time_s'] for r, _ in recs]
        if var['kind'] == 'constant': assert all(x == v for x in req)
        elif var['kind'] == 'mild_braking':
            assert min(req) == 0.5 * v and req[-1] == 0.5 * v and req[0] == v
        else:
            assert min(req) == 0.0 and req[-1] == v
            zero = [t for t, x in zip(ts, req) if x == 0.0]
            assert abs((zero[-1] - zero[0]) - 3.0) <= 2 * DT, (c['id'], zero[0], zero[-1])
        worst[var['kind']] = max(worst.get(var['kind'], 0.0), maxstep)
    results['2_3_profiles'] = dict(cases=len(cases), max_request_step_per_frame=worst)
    # 4
    plain = next(c for c in proto['cases'] if c['draw']['family'] == 'lead_braking' and c['role'] == 'eval')
    d = Draw(**plain['draw']); a = frames_run(d1.make_requests(plain, d, 77), 77, 700); b = frames_run(ActorRequests(d, 77, reactive=True), 77, 700)
    assert a == b
    results['4_plain_case_identical'] = dict(case=plain['id'], frames=700)
    # 5
    src = (V3 / 'overlay' / '747_full_scenario_binding_20261103' / 'scene_actors_v03.py').read_text(encoding='utf-8')
    base_start = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == 'start')
    mine = (HERE / 'src' / 'scene_actors_d1_v01.py').read_text(encoding='utf-8')
    var_start = next(n for n in ast.walk(ast.parse(mine)) if isinstance(n, ast.FunctionDef) and n.name == 'start')
    a = ast.dump(base_start).replace("Call(func=Name(id='ActorRequests', ctx=Load()), args=[Attribute(value=Name(id='self', ctx=Load()), attr='draw', ctx=Load()), Name(id='frame', ctx=Load())], keywords=[keyword(arg='reactive', value=Name(id='reactive', ctx=Load()))])",
                                     "Call(func=Name(id='LeadVariantRequests', ctx=Load()), args=[Attribute(value=Name(id='self', ctx=Load()), attr='draw', ctx=Load()), Name(id='frame', ctx=Load())], keywords=[keyword(arg='reactive', value=Name(id='reactive', ctx=Load())), keyword(arg='variant', value=Name(id='variant', ctx=Load()))])")
    assert a == ast.dump(var_start), 'start() bodies differ beyond the policy class'
    results['5_start_ast_identical_but_policy'] = True
    # 6
    diffs = {}
    for rel in ('probe_arms_v01.py', 'review/review_actor_records_v04.py'):
        old = (V3 / 'claude_smoke_v01' / rel).read_text(encoding='utf-8').splitlines(); new = (HERE / 'src' / rel).read_text(encoding='utf-8').splitlines()
        diffs[rel] = [l for l in difflib.unified_diff(old, new, lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
    assert len(diffs['probe_arms_v01.py']) == 7 and len(diffs['review/review_actor_records_v04.py']) == 3, diffs
    results['6_diffs'] = diffs
    results['status'] = 'PASS'
    (HERE / 'TEST_D1_POLICY_v13.json').write_text(json.dumps(results, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in results.items() if k != '6_diffs'}, indent=1))


if __name__ == '__main__':
    main()
