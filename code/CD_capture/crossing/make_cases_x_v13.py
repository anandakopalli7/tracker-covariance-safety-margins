"""Crossing sprint (amendment A11, 21 Nov 2026): fresh never-run cases for vehicle crossing and pedestrian crossing. New file,
21 Nov 2026 (Claude Opus 5.5, session CD). No pod, no run, no outcome is read here.

Generator (the same as the old crossing tuning runs p2_c1109_tune_*, and as package C): the C1109 sampler
(P\\06_phase0\\scenarios\\SAMPLER_C1109_v01.py, draw(index, family, role, consumer)), whose cases are pre-drawn in
DEVELOPMENT_PROTOCOL_MAIN_v01.json (SHA-256 32d683a0...). Tuning cases are role 'tune'; these are role 'eval', consumer 'finite'
(seed = the case's own, noise episode C1109/eval/finite/<index>), so packet_main_v03 runs them unchanged.
Rule (as CASES_C_v13, A10 sec. 5.1): per family and desired speed (5, 10, 15 m/s), the evaluation cases in ascending id order;
the ordered list interleaves the speeds: position p has speed (5, 10, 15)[p % 3] and rank p // 3 within its speed, so the first
3m positions hold m cases per speed. Positions 0-199 are the study order (A11 takes the first n); 200-209 are reserves, used in
order. alpha = beta = (1.642374415149816, 5.411894431054339, 7.550302542198003)[rank % 3] (C's cycle). Job id px13_<case>_native.
Checks (refuse on any failure): every selected case is role eval, main_study_eligible, of its family, and the protocol SHA-256 is
the one of record; no selected id appears in any earlier case list or run name (sources and counts written to the file); no
selected case equals any other protocol case in its Draw (family, speed, every drawn number) or its seed; D1 and E3b cases are
lead-braking draws (CASES_D1_v13.json), so none can equal a crossing case (checked: no family match).
Usage: python -I -B make_cases_x_v13.py  -> CASES_X_v13.json beside this file (never overwritten with different content)
"""
import hashlib, json, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent; WORK = CD.parent
P = pathlib.Path(r'<library folder>')
PROTOCOL = P / '06_phase0' / 'scenarios' / 'DEVELOPMENT_PROTOCOL_MAIN_v01.json'
PROTOCOL_SHA256 = '32d683a0a8ca2e91ff0245759ad78b43e7953c33bd12847c5193cafcdaa5735d'
SAMPLER = P / '06_phase0' / 'scenarios' / 'SAMPLER_C1109_v01.py'
ALPHA_CYCLE = (1.642374415149816, 5.411894431054339, 7.550302542198003)
FAMILIES = ('vehicle_crossing', 'pedestrian_crossing')
SPEEDS = (5, 10, 15)
N_STUDY, N_RESERVE = 200, 10
ID = re.compile(r'(?:c1109_(?:eval|tune)_\d{4}|fit_finite_\d{4}|canonical_[a-z_]+_v\d+_r\d+_finite)')
# earlier run names (directory or file names) and earlier case lists (file contents)
RUN_DIRS = [CD / 'runs', CD / 'archives', WORK / 'E_closedloop' / 'runs', P / '08_phase2' / 'archives_c1', P / '08_phase2' / 'summaries',
            P / '07_phase1_archives', P / '07_fit_runs' / 'archives', P / '05_smoke_results' / 'archives']
LISTS = [CD / 'CASES_C_v13.json', CD / 'd1' / 'CASES_D1_v13.json', CD / 'REPLACEMENTS_C_v13.json'] + sorted((CD / 'jobs').glob('*.json')) \
    + sorted((WORK / 'E_closedloop' / 'jobs').glob('*.json')) + sorted((WORK / 'B_retrack' / 'out' / 'b0').glob('*.csv'))


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def earlier_ids():
    seen, src = set(), {}
    for d in RUN_DIRS:
        if not d.is_dir(): src[str(d)] = 'missing'; continue
        ids = {m.group(0) for n in (x.name for x in d.iterdir()) for m in ID.finditer(n)}
        src[str(d)] = len(ids); seen |= ids
    for f in LISTS:
        if not f.is_file(): src[str(f)] = 'missing'; continue
        ids = set(ID.findall(f.read_text(encoding='utf-8', errors='replace')))
        src[str(f)] = len(ids); seen |= ids
    return seen, src


def draw_key(c):
    d = c['draw']
    return (d['family'], float(d['desired_mps'])) + tuple(sorted((k, d[k]) for k in d if k not in ('family', 'desired_mps', 'seed_hex')))


def main():
    raw = PROTOCOL.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PROTOCOL_SHA256: raise SystemExit('REFUSED: protocol differs from the one of record')
    cases = json.loads(raw)['cases']
    keys = [draw_key(c) for c in cases]
    if len(set(keys)) != len(keys) or len({c['seed'] for c in cases}) != len(cases) or len({c['draw']['seed_hex'] for c in cases}) != len(cases):
        raise SystemExit('REFUSED: two protocol cases share a draw or a seed')
    seen, src = earlier_ids()
    out = {}
    for fam in FAMILIES:
        pools = {}
        for v in SPEEDS:
            pool = sorted((c for c in cases if c.get('role') == 'eval' and c['draw']['family'] == fam and c['desired_mps'] == v), key=lambda c: c['id'])
            assert all(c['id'].startswith('c1109_eval_') and c.get('main_study_eligible') is True and c['consumer'] == 'finite' for c in pool)
            pools[v] = pool
        rows = []
        for p in range(N_STUDY + N_RESERVE):
            v = SPEEDS[p % 3]; r = p // 3
            if r >= len(pools[v]): raise SystemExit(f'REFUSED: {fam} has only {len(pools[v])} evaluation cases at {v} m/s')
            c = pools[v][r]; d = c['draw']
            rows.append(dict(position=p, reserve=p >= N_STUDY, case=c['id'], job=f"px13_{c['id']}_native", family=fam, desired_mps=v,
                             rank_in_speed=r, alpha=ALPHA_CYCLE[r % 3], seed=c['seed'], seed_hex=d['seed_hex'],
                             noise_episode=c['noise_episode'], side=d['side'], occluder=d['occluder'], crossing_mps=d['crossing_mps'],
                             ttc_s=d['ttc_s'], tau_s=d['tau_s']))
        clash = sorted(x['case'] for x in rows if x['case'] in seen)
        if clash: raise SystemExit(f'REFUSED: {fam} cases already used earlier: {clash[:10]}')
        out[fam] = rows
    d1 = json.loads((CD / 'd1' / 'CASES_D1_v13.json').read_text(encoding='utf-8'))
    d1_fams = sorted({(c.get('draw') or {}).get('family', 'lead_braking') for c in d1.get('cases', [])})
    if set(d1_fams) & set(FAMILIES): raise SystemExit('REFUSED: a D1 case has a crossing family')
    allx = [x['case'] for f in FAMILIES for x in out[f]]
    assert len(allx) == len(set(allx)) == len(FAMILIES) * (N_STUDY + N_RESERVE)
    body = dict(schema='CASES_X_V13', amendment='A11 (crossing sprint, 21 Nov 2026)', protocol=str(PROTOCOL), protocol_sha256=PROTOCOL_SHA256,
                sampler=str(SAMPLER), sampler_sha256=sha(SAMPLER), generator='C1109 sampler, role eval, consumer finite (pre-drawn in the protocol)',
                rule=('per family and speed: evaluation cases in ascending id order; positions interleave speeds 5, 10, 15 (position p: speed '
                      '(5,10,15)[p % 3], rank p // 3); positions 0-199 study order (A11 takes the first n), 200-209 reserves in order; '
                      'alpha = beta = C cycle [rank % 3]; job px13_<case>_native'),
                alpha_cycle=ALPHA_CYCLE, n_study=N_STUDY, n_reserve=N_RESERVE,
                checks=dict(protocol_draws_and_seeds_unique=True, earlier_id_sources=src, earlier_ids_total=len(seen), overlaps=0,
                            d1_families=d1_fams, note='E3/E3b used lead-braking cases only (c1109_eval positions 35-54 and D1-law draws).'),
                families={f: out[f] for f in FAMILIES})
    text = json.dumps(body, indent=1) + '\n'
    path = HERE / 'CASES_X_v13.json'
    if path.exists():
        if path.read_text(encoding='utf-8') != text: raise SystemExit('REFUSED: CASES_X_v13.json exists with different content')
    else:
        path.write_text(text, encoding='utf-8', newline='\n')
    for f in FAMILIES:
        rs = out[f]
        print(f, 'study', sum(not x['reserve'] for x in rs), 'reserve', sum(x['reserve'] for x in rs), 'first', rs[0]['case'], 'last study', rs[N_STUDY - 1]['case'],
              'occluder share (first 200) %.2f' % (sum(x['occluder'] for x in rs[:N_STUDY]) / N_STUDY))
    print('earlier ids', len(seen), {pathlib.Path(k).name: v for k, v in src.items()})
    print('CASES_X_v13.json sha256', sha(path))


if __name__ == '__main__':
    main()
