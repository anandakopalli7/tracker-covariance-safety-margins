"""A12 sec. 2: the new lead-braking case list, n = 150 (50 per speed) + 15 reserves (5 per speed). New file, 22 Nov 2026 (Claude Opus 5.5,
session CD), written before any new run exists. Pattern of crossing\\make_cases_x_pc_v13.py (frozen in FREEZE_CD_add3).

Rule (A10 sec. 5.1, A11 sec. 3.1):
  1. The never-run evaluation cases of DEVELOPMENT_PROTOCOL_MAIN_v01.json (SHA-256 32d683a0...) of family lead_braking: per speed in ascending
     id, skipping every case already used (C: ranks 0-34; E3/E4: ranks 35-54; checked against every run name and case list). The
     protocol has 51 / 33 / 51 of them at 5 / 10 / 15 m/s.
  2. Extension with the protocol's own generator, unchanged, where a speed is short of 55: make_main_protocol_v01.new_case's rule continued
     past index 1799 (i = 1800, 1801, ...; family FAMILIES[i % 6], lead braking when i % 6 == 0; SAMPLER_C1109_v01.draw(i, family,
     role='eval', consumer='finite'); seed = int(sha256('C1109/eval/finite/<i>')[:8], 16); id c1109_eval_<i>). Lead-braking indices in
     ascending order; each joins its drawn speed's pool until every speed has 55; a case for a full speed is not used (listed).
     The replica must reproduce all 1,800 protocol evaluation cases exactly.
  3. Per speed: never-run protocol cases (ascending id), then extension cases (ascending index). Speeds interleaved: position p has speed
     (5, 10, 15)[p % 3], rank p // 3. Positions 0-149 are the study runs (50 per speed); 150-164 the reserves (5 per speed, used in order).
     alpha = beta = C's cycle [rank % 3]. Job pl12_<case>_native.
Checks: extension ids, seeds, seed digests and noise episodes new against the protocol, D1, X's case file and extended protocol; all draws
unique; no selected id in any earlier run or case list (crossing\\make_cases_x_v13.earlier_ids plus CASES_X_PC_v13.json).
Writes (never overwritten): l12\\CASES_L12_v13.json; l12\\DEVELOPMENT_PROTOCOL_L12_v13.json (the main protocol + the appended extension
cases, for packet_l12; the protocol's own cases unchanged).
"""
import hashlib, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(CD / 'crossing'))
import make_cases_x_v13 as MX                    # noqa: E402  (frozen in add3: earlier_ids, draw_key, PROTOCOL)
import make_cases_x_pc_v13 as XP                 # noqa: E402  (frozen in add3: sampler, new_case, actor)
FAM = 'lead_braking'
SPEEDS = (5, 10, 15)
N_PER_SPEED, R_PER_SPEED = 50, 5


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    raw = MX.PROTOCOL.read_bytes()
    if sha(raw) != MX.PROTOCOL_SHA256: raise SystemExit('REFUSED: protocol differs')
    cases = json.loads(raw)['cases']; draw = XP.sampler()
    ev = [c for c in cases if c['role'] == 'eval']
    if sum(XP.new_case(draw, int(c['id'].rsplit('_', 1)[1])) == c for c in ev) != 1800: raise SystemExit('REFUSED: replica differs')
    seen, src = MX.earlier_ids()
    X = json.loads((CD / 'crossing' / 'CASES_X_PC_v13.json').read_text(encoding='utf-8'))
    xext = json.loads((CD / 'crossing' / 'DEVELOPMENT_PROTOCOL_X_v13.json').read_text(encoding='utf-8'))['cases'][len(cases):]
    seen |= {r['case'] for r in X['cases']}
    need = N_PER_SPEED + R_PER_SPEED
    pools = {v: sorted((c for c in ev if c['draw']['family'] == FAM and c['desired_mps'] == v and c['id'] not in seen), key=lambda c: c['id'])
             for v in SPEEDS}
    n_protocol = {v: len(pools[v]) for v in SPEEDS}
    pools = {v: p[:need] for v, p in pools.items()}
    ext, unused = [], []; i = 1800
    while any(len(pools[v]) < need for v in SPEEDS):
        if XP.actor.FAMILIES[i % 6] == FAM:
            c = XP.new_case(draw, i)
            if len(pools[c['desired_mps']]) < need: pools[c['desired_mps']].append(c); ext.append(c)
            else: unused.append(c['id'])
        i += 1; assert i < 10000
    d1 = json.loads((CD / 'd1' / 'CASES_D1_v13.json').read_text(encoding='utf-8'))['cases']
    old = cases + d1 + xext
    assert not {c['id'] for c in ext} & ({c['id'] for c in old} | seen)
    assert not {c['seed'] for c in ext} & {c['seed'] for c in old} and len({c['seed'] for c in ext}) == len(ext)
    assert not {c['draw']['seed_hex'] for c in ext} & {c['draw']['seed_hex'] for c in old}
    assert not {c['noise_episode'] for c in ext} & {c['noise_episode'] for c in old}
    keys = [MX.draw_key(c) for c in cases + xext + ext]; assert len(set(keys)) == len(keys), 'two cases share a draw'
    pids = {c['id'] for c in cases}
    rows = []
    for p in range(3 * need):
        v = SPEEDS[p % 3]; r = p // 3; c = pools[v][r]; d = c['draw']
        assert c['id'] not in seen
        rows.append(dict(position=p, reserve=p >= 3 * N_PER_SPEED, case=c['id'], job=f"pl12_{c['id']}_native", family=FAM, desired_mps=v,
                         rank_in_speed=r, alpha=MX.ALPHA_CYCLE[r % 3], source='protocol' if c['id'] in pids else 'extension', seed=c['seed'],
                         seed_hex=d['seed_hex'], noise_episode=c['noise_episode'], side=d['side'], brake_mps2=d['brake_mps2'],
                         brake_start_s=d['brake_start_s'], tau_s=d['tau_s']))
    body = dict(schema='CASES_L12_V13', amendment='A12 sec. 2 (new lead-braking runs)', protocol=str(MX.PROTOCOL), protocol_sha256=MX.PROTOCOL_SHA256,
                sampler_sha256=sha(MX.SAMPLER.read_bytes()), rule=__doc__.split('Rule')[1].split('Checks')[0].strip(),
                n_per_speed=N_PER_SPEED, reserves_per_speed=R_PER_SPEED, never_run_protocol_cases_per_speed={str(v): n_protocol[v] for v in SPEEDS},
                extension=dict(first_index=1800, last_index_examined=i - 1, used=len(ext), used_per_speed={str(v): sum(c['desired_mps'] == v for c in ext) for v in SPEEDS},
                               not_used_speed_full=unused, cases=ext),
                checks=dict(replica_reproduces_protocol_eval_cases=1800, earlier_id_sources=dict(src, CASES_X_PC_v13=len(X['cases'])),
                            earlier_ids_total=len(seen), overlaps=0, draws_unique=True),
                study_by_source={s: sum(x['source'] == s for x in rows if not x['reserve']) for s in ('protocol', 'extension')}, cases=rows)
    proto = json.loads(raw); proto2 = dict(proto); proto2['cases'] = cases + ext
    proto2['claude_v13_l12_derivation'] = dict(base='DEVELOPMENT_PROTOCOL_MAIN_v01.json', base_sha256=MX.PROTOCOL_SHA256, appended_cases=len(ext),
                                              case_file='CASES_L12_v13.json', note='A12 sec. 2: the main protocol unchanged, with the lead-braking evaluation cases of the generator extension appended.')
    for path, obj in ((HERE / 'CASES_L12_v13.json', body), (HERE / 'DEVELOPMENT_PROTOCOL_L12_v13.json', proto2)):
        text = json.dumps(obj, indent=1, allow_nan=False) + '\n'
        if path.exists():
            if path.read_text(encoding='utf-8') != text: raise SystemExit('REFUSED: %s exists with different content' % path.name)
        else: path.write_text(text, encoding='utf-8', newline='\n')
        print(path.name, sha(path.read_bytes()))
    print('never-run protocol per speed', n_protocol, '| extension', len(ext), body['extension']['used_per_speed'], 'not used', len(unused),
          '| last index', i - 1, '| study by source', body['study_by_source'])


if __name__ == '__main__':
    main()
