"""Crossing sprint, X (A11 sec. 3): the ordered pedestrian-crossing case list, n = 390 (130 per speed) + 15 reserves (5 per speed).
New file, 21 Nov 2026 (Claude Opus 5.5, session CD). Supersedes CASES_X_v13.json (two families, 200 + 10) for X.

Rule (A10 sec. 5.1, as package C; coordinator 13:36 and 14:12 EST):
  1. The never-run evaluation cases of DEVELOPMENT_PROTOCOL_MAIN_v01.json (SHA-256 32d683a0...) of family pedestrian_crossing: per speed
     (5, 10, 15 m/s) in ascending id. Each keeps its own seed and noise episode. The protocol has 102 / 101 / 97 of them.
  2. Extension with the protocol's own generator, unchanged, because 135 per speed are needed: make_main_protocol_v01.new_case's rule
     continued past the protocol's last evaluation index 1799, i.e. index i = 1800, 1801, ... with family FAMILIES[i % 6] (pedestrian
     crossing when i % 6 == 2), draw = SAMPLER_C1109_v01.draw(i, family, role='eval', consumer='finite') (the 746 actor policy's Draw;
     digest sha256('C1109/eval/finite/<i>'), seed = int(digest[:8], 16)), id c1109_eval_<i>. Pedestrian indices are taken in ascending
     order; each case joins the pool of the speed the sampler draws, until every speed has 135 cases; a case whose speed is already
     full is not used (listed). The replica is checked first: it reproduces all 1,800 protocol evaluation cases byte for byte.
  3. Per speed the pool is ordered: protocol cases (ascending id), then extension cases (ascending index). The list interleaves the
     speeds: position p has speed (5, 10, 15)[p % 3] and rank p // 3. Positions 0-389 are the study runs (130 per speed), 390-404
     the reserves (5 per speed, used in order by A11's replacement rule). alpha = beta = C's cycle [rank % 3]. Job pc13x_<case>_native.
Checks (refuse on failure): protocol SHA-256; replica identity; extension ids, seeds, seed digests and noise episodes are new (not in the
protocol, D1's case file or any earlier list); no case equals another in its Draw; no selected id appears in an earlier run or case list.
Writes (never overwritten): CASES_X_PC_v13.json; DEVELOPMENT_PROTOCOL_X_v13.json = the main protocol with the extension cases appended
(for packet_x_v13; the protocol's own cases unchanged).
Usage: python -I -B make_cases_x_pc_v13.py
"""
import dataclasses, hashlib, json, pathlib, sys
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import make_cases_x_v13 as MX                                                 # noqa: E402  (earlier-id sources and draw_key only)
P = MX.P
W = pathlib.Path(r'<library folder>')
sys.path[:0] = [str(W / '746_actual_actor_policy_development_20261103')]
import actor_policy_v01 as actor                                             # noqa: E402  (read-only import of the 746 policy)
FAM = 'pedestrian_crossing'
SPEEDS = (5, 10, 15)
N_PER_SPEED, R_PER_SPEED = 130, 5
ALPHA_CYCLE = MX.ALPHA_CYCLE


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sdict(d):
    return {k: (sdict(v) if isinstance(v, dict) else v) for k, v in sorted(d.items())}


def sampler():
    src = (P / '06_phase0' / 'scenarios' / 'SAMPLER_C1109_v01.py').read_text(encoding='utf-8')
    scope = dict(actor.__dict__); exec(compile(src, 'SAMPLER_C1109_v01.py', 'exec'), scope)
    return scope['draw']


def new_case(draw, i, role='eval'):                                          # make_main_protocol_v01.new_case, verbatim logic
    family = actor.FAMILIES[i % 6]
    d = draw(i, family=family, role=role, consumer='finite')
    identity = f'C1109/{role}/finite/{i}'
    assert d.seed_hex == sha(identity.encode()) and d.family == family
    v = int(d.desired_mps); assert float(v) == d.desired_mps
    return sdict(dict(consumer='finite', desired_mps=v, draw=sdict(dataclasses.asdict(d)), fresh_process_required=True,
                      id=f'c1109_{role}_{i:04d}', main_study_eligible=True, noise_episode=identity, paired_condition=identity,
                      reactive=True, repeat=0, repeat_group=identity, role=role, seed=int(d.seed_hex[:8], 16)))


def main():
    raw = MX.PROTOCOL.read_bytes()
    if sha(raw) != MX.PROTOCOL_SHA256: raise SystemExit('REFUSED: protocol differs from the one of record')
    proto = json.loads(raw); cases = proto['cases']
    draw = sampler()
    ev = [c for c in cases if c['role'] == 'eval']
    idx = [int(c['id'].rsplit('_', 1)[1]) for c in ev]
    assert idx == list(range(1800))
    rep = sum(new_case(draw, i) == c for i, c in zip(idx, ev))
    if rep != 1800: raise SystemExit('REFUSED: the replica reproduces only %d of 1800 protocol evaluation cases' % rep)
    pools = {v: sorted((c for c in ev if c['draw']['family'] == FAM and c['desired_mps'] == v), key=lambda c: c['id']) for v in SPEEDS}
    n_protocol = {v: len(pools[v]) for v in SPEEDS}
    need = N_PER_SPEED + R_PER_SPEED
    ext, unused = [], []
    i = 1800
    while any(len(pools[v]) < need for v in SPEEDS):
        if actor.FAMILIES[i % 6] == FAM:
            c = new_case(draw, i)
            if len(pools[c['desired_mps']]) < need: pools[c['desired_mps']].append(c); ext.append(c)
            else: unused.append(c['id'])
        i += 1
        assert i < 10000
    # checks: new identities; unique draws; no earlier use
    pids = {c['id'] for c in cases}; pseeds = {c['seed'] for c in cases}; phex = {c['draw']['seed_hex'] for c in cases}
    peps = {c['noise_episode'] for c in cases} | {c['paired_condition'] for c in cases} | {c['repeat_group'] for c in cases}
    d1 = json.loads((MX.CD / 'd1' / 'CASES_D1_v13.json').read_text(encoding='utf-8'))['cases']
    d1seeds = {c['seed'] for c in d1}; d1hex = {c['draw']['seed_hex'] for c in d1}; d1eps = {c['noise_episode'] for c in d1}
    assert not {c['id'] for c in ext} & pids
    assert not {c['seed'] for c in ext} & (pseeds | d1seeds) and len({c['seed'] for c in ext}) == len(ext)
    assert not {c['draw']['seed_hex'] for c in ext} & (phex | d1hex)
    assert not {c['noise_episode'] for c in ext} & (peps | d1eps)
    keys = [MX.draw_key(c) for c in cases + ext]
    assert len(set(keys)) == len(keys), 'two cases share a draw'
    seen, src = MX.earlier_ids()
    rows = []
    for p in range(3 * need):
        v = SPEEDS[p % 3]; r = p // 3; c = pools[v][r]; d = c['draw']
        rows.append(dict(position=p, reserve=p >= 3 * N_PER_SPEED, case=c['id'], job=f"pc13x_{c['id']}_native", family=FAM, desired_mps=v,
                         rank_in_speed=r, alpha=ALPHA_CYCLE[r % 3], source='protocol' if c['id'] in pids else 'extension', seed=c['seed'],
                         seed_hex=d['seed_hex'], noise_episode=c['noise_episode'], side=d['side'], occluder=d['occluder'],
                         crossing_mps=d['crossing_mps'], ttc_s=d['ttc_s'], tau_s=d['tau_s']))
    clash = sorted(x['case'] for x in rows if x['case'] in seen)
    if clash: raise SystemExit('REFUSED: cases already used earlier: %s' % clash[:10])
    ext_ids = {c['id'] for c in ext}
    body = dict(schema='CASES_X_PC_V13', amendment='A11 sec. 3 (X, pedestrian crossing)', protocol=str(MX.PROTOCOL), protocol_sha256=MX.PROTOCOL_SHA256,
                sampler=str(MX.SAMPLER), sampler_sha256=sha(MX.SAMPLER.read_bytes()),
                actor_policy=str(W / '746_actual_actor_policy_development_20261103' / 'actor_policy_v01.py'),
                actor_policy_sha256=sha((W / '746_actual_actor_policy_development_20261103' / 'actor_policy_v01.py').read_bytes()),
                rule=__doc__.split('Rule')[1].split('Checks')[0].strip(), n_per_speed=N_PER_SPEED, reserves_per_speed=R_PER_SPEED,
                never_run_protocol_cases_per_speed={str(v): n_protocol[v] for v in SPEEDS},
                extension=dict(first_index=1800, last_index_examined=i - 1, used=len(ext), used_per_speed={str(v): sum(c['desired_mps'] == v for c in ext) for v in SPEEDS},
                               not_used_speed_full=unused, cases=ext),
                checks=dict(replica_reproduces_protocol_eval_cases=rep, extension_ids_seeds_digests_episodes_new=True, draws_unique=True,
                            earlier_id_sources=src, earlier_ids_total=len(seen), overlaps=0),
                study_by_source={s: sum(x['source'] == s for x in rows if not x['reserve']) for s in ('protocol', 'extension')},
                cases=rows)
    out1 = HERE / 'CASES_X_PC_v13.json'
    proto2 = dict(proto); proto2['cases'] = cases + ext
    proto2['claude_v13_x_derivation'] = dict(base='DEVELOPMENT_PROTOCOL_MAIN_v01.json', base_sha256=MX.PROTOCOL_SHA256, appended_cases=len(ext),
                                            case_file='CASES_X_PC_v13.json', note='Revision v13 X (A11 sec. 3): the main protocol unchanged, with the pedestrian-crossing '
                                            'evaluation cases of the generator extension (indices >= 1800) appended.')
    out2 = HERE / 'DEVELOPMENT_PROTOCOL_X_v13.json'
    for path, obj in ((out1, body), (out2, proto2)):
        text = json.dumps(obj, indent=1, allow_nan=False) + '\n'
        if path.exists():
            if path.read_text(encoding='utf-8') != text: raise SystemExit('REFUSED: %s exists with different content' % path.name)
        else:
            path.write_text(text, encoding='utf-8', newline='\n')
        print(path.name, sha(path.read_bytes()))
    assert json.loads(out2.read_bytes())['cases'][:len(cases)] == cases
    print('protocol never-run per speed', n_protocol, '| extension used', len(ext), body['extension']['used_per_speed'], 'not used', len(unused),
          '| last index', i - 1, '| study by source', body['study_by_source'], ext_ids and sorted(ext_ids)[:3])


if __name__ == '__main__':
    main()
