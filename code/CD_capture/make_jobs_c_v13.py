"""Package C job lists (revision v13, A10 sec. 5.1): fresh evaluation runs in two families.

A variant of P\\03_runbook\\main_sources_v01\\make_main_jobs_v01.py (imported read-only for its control/admission
job builder, so the control jobs are built by the same code as every earlier list). The generator is unchanged:
packet_main_v03, native recording arm.

Cases (A10 5.1): the never-run evaluation cases of DEVELOPMENT_PROTOCOL_MAIN_v01.json (SHA-256 32d683a0...).
For each family (lead_braking, cutin) and desired speed (5, 10, 15 m/s), the first 35 cases in ascending id order:
105 lead-braking + 105 cut-in = 210 study jobs.
Recording arm: native, alpha = beta, assigned within family and speed in id order by the cycle
1.642374415149816, 5.411894431054339, 7.550302542198003 (the old evaluation runs' values).
Jobs: pc13_<case>_native, keep_raw = true for every study job.

Per pod: A1 admission (crash, benign, learned references, as make_main_jobs_v02.py) on every pod, one crash control
first, then one after every 50 study jobs (make_main_jobs_v01.py L89-94). Study jobs are dealt to pods in turn from a
list that alternates the two families and cycles the speeds, so every pod gets a balanced mix.
Volume folder: claude_v13_cd_v01 (new, so no id can collide with earlier results).

Usage: python -I make_jobs_c_v13.py --pods claude-v13cd-01,claude-v13cd-02,... [--tag v01]
       python -I make_jobs_c_v13.py --cases-only      (writes only the case manifest)
Outputs (never overwritten): jobs\\JOBS_PC13_<pod>_<tag>.json and CASES_C_v13.json.
"""
import argparse, hashlib, importlib.util, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
P = pathlib.Path(r'<library folder>')
MAIN_SOURCES = P / '03_runbook' / 'main_sources_v01'
PROTOCOL = P / '06_phase0' / 'scenarios' / 'DEVELOPMENT_PROTOCOL_MAIN_v01.json'
PROTOCOL_SHA256 = '32d683a0a8ca2e91ff0245759ad78b43e7953c33bd12847c5193cafcdaa5735d'
ALPHA_CYCLE = (1.642374415149816, 5.411894431054339, 7.550302542198003)
FAMILIES = ('lead_braking', 'cutin')
SPEEDS = (5, 10, 15)
N_PER_SPEED = 35
PHASE = 'PC13'
VOLUME_FOLDER = 'claude_v13_cd_v01'
CTL_EVERY = 50

spec = importlib.util.spec_from_file_location('mmj1', MAIN_SOURCES / 'make_main_jobs_v01.py')
v1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def select_cases():
    raw = PROTOCOL.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PROTOCOL_SHA256, 'protocol differs from A10 5.1'
    cases = json.loads(raw)['cases']
    chosen = {}
    for fam in FAMILIES:
        for v in SPEEDS:
            pool = sorted((c for c in cases if c.get('role') == 'eval' and c['draw']['family'] == fam and c['desired_mps'] == v),
                          key=lambda c: c['id'])
            assert all(len(c['id']) == len('c1109_eval_0000') and c['id'].startswith('c1109_eval_') for c in pool)
            assert all(c.get('main_study_eligible') is True for c in pool)
            assert len(pool) >= N_PER_SPEED
            sel = pool[:N_PER_SPEED]
            chosen[(fam, v)] = [dict(case=c['id'], family=fam, desired_mps=v, rank=i, alpha=ALPHA_CYCLE[i % 3],
                                     seed=c['seed'], noise_episode=c['noise_episode']) for i, c in enumerate(sel)]
            chosen[(fam, v, 'next_unused')] = [c['id'] for c in pool[N_PER_SPEED:N_PER_SPEED + 5]]
    return chosen


def study_jobs(chosen):
    """Interleave: for rank i, speed v, family f -> a balanced order (lead/cut-in alternating, speeds cycling)."""
    order = []
    for i in range(N_PER_SPEED):
        for v in SPEEDS:
            for fam in FAMILIES:
                order.append(chosen[(fam, v)][i])
    jobs = []
    for c in order:
        jid = f"pc13_{c['case']}_native"
        jobs.append(dict(id=jid, case=c['case'], arm='native', alpha=c['alpha'], beta=c['alpha'], phase=PHASE, role='eval',
                         scenario=c['case'], keep_raw=True))
    assert len(jobs) == len({j['id'] for j in jobs}) == 2 * 3 * N_PER_SPEED
    return jobs


def pod_lists(jobs, pods, tag):
    out = {}
    # Deal: job g (rank i = g // 6, stratum m = g % 6) goes to pod (m + i) % n, so every pod gets a mix of strata.
    deal = [((g % 6) + (g // 6)) % len(pods) for g in range(len(jobs))]
    for k, pod in enumerate(pods):
        sfx = pod[-2:]
        mine = [j for g, j in enumerate(jobs) if deal[g] == k]
        lst = [dict(v1.p1.job('x', 'crash', 'A1'), id=f'a1v13_{sfx}_crash'),
               dict(v1.p1.job('x', 'benign', 'A1'), id=f'a1v13_{sfx}_benign'),
               dict(v1.p1.job('x', 'learnedw0', 'A1'), id=f'a1v13_{sfx}_learned')]
        n = 0
        lst.append(dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_{PHASE.lower()}_{sfx}_{tag}_{n:03d}'))
        for i, j in enumerate(mine):
            lst.append(j)
            if (i + 1) % CTL_EVERY == 0:
                n += 1; lst.append(dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_{PHASE.lower()}_{sfx}_{tag}_{n:03d}'))
        cfg = dict(schema='CLAUDE_MAIN_JOBS_V01', protocol='DEVELOPMENT_PROTOCOL_SMOKE_v01.json', volume_folder=VOLUME_FOLDER,
                   capture_timeout_s=600, review_timeout_s=600, actor_review_timeout_s=180, server_ready_timeout_s=120,
                   concurrent_start_stagger_s=15, max_attempts=2, protocol_main_sha256=PROTOCOL_SHA256,
                   note=(f'Revision v13 package C (A10 5.1), pod {pod} ({k + 1} of {len(pods)}); {len(mine)} of 210 study jobs; '
                         'packet_main_v03 unchanged; native arm alpha = beta by the A10 cycle; keep_raw true on every study job.'),
                   made_by=dict(script='make_jobs_c_v13.py', sha256=sha(__file__), imports_read_only='make_main_jobs_v01.py ' + sha(MAIN_SOURCES / 'make_main_jobs_v01.py')),
                   jobs=lst)
        out[pod] = (cfg, mine)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pods', default=''); ap.add_argument('--tag', default='v01'); ap.add_argument('--cases-only', action='store_true')
    a = ap.parse_args()
    chosen = select_cases()
    manifest = HERE / 'CASES_C_v13.json'
    rows = [c for key, val in chosen.items() if len(key) == 2 for c in val]
    body = dict(schema='CASES_C_V13', amendment='AMENDMENT_10_v13.md sec. 5.1', protocol=str(PROTOCOL), protocol_sha256=PROTOCOL_SHA256,
                alpha_cycle=ALPHA_CYCLE, n_per_family_speed=N_PER_SPEED, cases=rows,
                next_unused_for_replacements={f'{k[0]}_{k[1]}': v for k, v in chosen.items() if len(k) == 3})
    text = json.dumps(body, indent=1) + '\n'
    if manifest.exists():
        assert manifest.read_text(encoding='utf-8') == text, 'case manifest exists with different content'
    else:
        manifest.write_text(text, encoding='utf-8', newline='\n')
    print('cases', len(rows), 'manifest sha256', sha(manifest))
    if a.cases_only:
        return
    pods = [p for p in a.pods.split(',') if p]
    assert pods, '--pods required'
    jobs = study_jobs(chosen)
    outdir = HERE / 'jobs'; outdir.mkdir(exist_ok=True)
    summary = {}
    for pod, (cfg, mine) in pod_lists(jobs, pods, a.tag).items():
        path = outdir / f'JOBS_{PHASE}_{pod}_{a.tag}.json'
        with open(path, 'x', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(cfg, indent=1) + '\n')
        summary[pod] = dict(file=path.name, sha256=sha(path), study=len(mine), total=len(cfg['jobs']))
    print(json.dumps(dict(phase=PHASE, study_jobs=len(jobs), pods=summary), indent=1))


if __name__ == '__main__':
    main()
