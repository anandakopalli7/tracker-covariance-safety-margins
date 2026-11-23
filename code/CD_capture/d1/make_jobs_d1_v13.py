"""Package D1 job lists (revision v13, A10 sec. 6 D1): the first 35 cases of each lead variant, recorded as in sec. 5.1.

Cases: CASES_D1_v13.json, role d1_openloop (35 per variant; 105 jobs). Native arm, alpha = beta, assigned within variant
and desired speed in id order by the cycle 1.642374415149816, 5.411894431054339, 7.550302542198003 (as sec. 5.1 within
family and speed). keep_raw = true. Job ids pd13_<case>_native. Packet: packet_d1_v13.
Per list: A1 references again (crash, benign, learned; ids a1d13_<sfx>_*) so each pod shows that the D1 packet still
reproduces the reference runs bit-identically, one crash control first and after every 50 study jobs.
Deal: job g (rank i = g // 9 over the 9 variant x speed strata, stratum m = g % 9) to list (m + i) % n.
Pilot (--pilot NAME): one list with the A1 references (ids a1d13p_<sfx>_*), a crash control and the three d1_pilot cases
(pd13pilot_<kind>_native, alpha = beta = 5.411894431054339, keep_raw false); run before the study lists (review finding 2).
Usage: python -I make_jobs_d1_v13.py --lists claude-v13cd-01,...  |  --pilot claude-v13cd-01   (never overwrites)
"""
import argparse, hashlib, importlib.util, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
CD = HERE.parent
P = pathlib.Path(r'<library folder>')
MAIN_SOURCES = P / '03_runbook' / 'main_sources_v01'
ALPHA_CYCLE = (1.642374415149816, 5.411894431054339, 7.550302542198003)
KINDS = ('constant', 'mild_braking', 'stop_and_go')
PHASE = 'PD13'

spec = importlib.util.spec_from_file_location('mmj1', MAIN_SOURCES / 'make_main_jobs_v01.py')
v1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)


def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--lists', default=''); ap.add_argument('--pilot', default=''); ap.add_argument('--tag', default='v01')
    a = ap.parse_args(); lists = [x for x in a.lists.split(',') if x]
    cf = HERE / 'CASES_D1_v13.json'; cases = json.loads(cf.read_text(encoding='utf-8'))['cases']
    proto_sha = sha(HERE / 'DEVELOPMENT_PROTOCOL_D1_v13.json')
    role = {c['id']: c['role'] for c in cases}
    if a.pilot:
        sfx = a.pilot[-2:]
        lst = [dict(v1.p1.job('x', 'crash', 'A1'), id=f'a1d13p_{sfx}_crash'), dict(v1.p1.job('x', 'benign', 'A1'), id=f'a1d13p_{sfx}_benign'),
               dict(v1.p1.job('x', 'learnedw0', 'A1'), id=f'a1d13p_{sfx}_learned'), dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_pd13p_{sfx}_{a.tag}_000')]
        for c in cases:
            if c['role'] == 'd1_pilot':
                lst.append(dict(id=f"pd13pilot_{c['lead_variant']['kind']}_native", case=c['id'], arm='native', alpha=ALPHA_CYCLE[1], beta=ALPHA_CYCLE[1],
                                phase='PD13PILOT', role='pilot', scenario=c['id'], keep_raw=False))
        assert sum(j['phase'] == 'PD13PILOT' for j in lst) == 3
        cfg = dict(schema='CLAUDE_MAIN_JOBS_V01', protocol='DEVELOPMENT_PROTOCOL_SMOKE_v01.json', volume_folder='/opt/claude_v13_local',
                   capture_timeout_s=600, review_timeout_s=600, actor_review_timeout_s=180, server_ready_timeout_s=120,
                   concurrent_start_stagger_s=15, max_attempts=2, protocol_d1_sha256=proto_sha,
                   note='Revision v13 package D1 pilot (review finding 2): A1 references on packet_d1_v13 and the three d1_pilot cases (not study runs).',
                   made_by=dict(script='make_jobs_d1_v13.py', sha256=sha(__file__), case_file_sha256=sha(cf)), jobs=lst)
        path = CD / 'jobs' / f'JOBS_PD13PILOT_{a.pilot}_{a.tag}.json'
        with open(path, 'x', encoding='utf-8', newline=chr(10)) as f: f.write(json.dumps(cfg, indent=1) + chr(10))
        print(path.name, sha(path)); return
    strata = {}
    for kind in KINDS:
        for v in (5, 10, 15):
            sel = sorted((c for c in cases if c['role'] == 'd1_openloop' and c['lead_variant']['kind'] == kind and c['desired_mps'] == v), key=lambda c: c['id'])
            strata[(kind, v)] = [dict(id=f"pd13_{c['id']}_native", case=c['id'], arm='native', alpha=ALPHA_CYCLE[i % 3], beta=ALPHA_CYCLE[i % 3],
                                      phase=PHASE, role='eval', scenario=c['id'], keep_raw=True) for i, c in enumerate(sel)]
    assert sum(len(s) for s in strata.values()) == 105
    assert all(role[j['case']] == 'd1_openloop' for s in strata.values() for j in s)   # review finding 6
    order = []
    for i in range(max(len(s) for s in strata.values())):
        for key in strata:
            if i < len(strata[key]): order.append(strata[key][i])
    deal = [((g % 9) + (g // 9)) % len(lists) for g in range(len(order))]
    out = CD / 'jobs'; summary = {}
    for k, name in enumerate(lists):
        sfx = name[-2:]; mine = [j for g, j in enumerate(order) if deal[g] == k]
        lst = [dict(v1.p1.job('x', 'crash', 'A1'), id=f'a1d13_{sfx}_crash'), dict(v1.p1.job('x', 'benign', 'A1'), id=f'a1d13_{sfx}_benign'),
               dict(v1.p1.job('x', 'learnedw0', 'A1'), id=f'a1d13_{sfx}_learned')]
        n = 0; lst.append(dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_{PHASE.lower()}_{sfx}_{a.tag}_{n:03d}'))
        for i, j in enumerate(mine):
            lst.append(j)
            if (i + 1) % 50 == 0:
                n += 1; lst.append(dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_{PHASE.lower()}_{sfx}_{a.tag}_{n:03d}'))
        cfg = dict(schema='CLAUDE_MAIN_JOBS_V01', protocol='DEVELOPMENT_PROTOCOL_SMOKE_v01.json', volume_folder='/opt/claude_v13_local',
                   capture_timeout_s=600, review_timeout_s=600, actor_review_timeout_s=180, server_ready_timeout_s=120,
                   concurrent_start_stagger_s=15, max_attempts=2, protocol_d1_sha256=proto_sha,
                   note=f'Revision v13 package D1 (A10 sec. 6), list {name} ({k + 1} of {len(lists)}); {len(mine)} of 105 study jobs; packet_d1_v13; native arm alpha = beta by the A10 cycle; keep_raw true.',
                   made_by=dict(script='make_jobs_d1_v13.py', sha256=sha(__file__), case_file_sha256=sha(cf)), jobs=lst)
        path = out / f'JOBS_{PHASE}_{name}_{a.tag}.json'
        with open(path, 'x', encoding='utf-8', newline='\n') as f: f.write(json.dumps(cfg, indent=1) + '\n')
        summary[name] = dict(file=path.name, sha256=sha(path), study=len(mine), total=len(lst))
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
