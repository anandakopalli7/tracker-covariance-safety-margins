"""Crossing sprint, X (A11 sec. 3): job lists for the pedestrian-crossing capture. New file, 21 Nov 2026 (Claude Opus 5.5, session CD).

C's job format (make_jobs_c_v13.py: native arm, alpha = beta, the admission and control jobs of P\\03_runbook\\main_sources_v01\\
make_main_jobs_v01.py imported read-only, C's timeouts), with: cases from CASES_X_PC_v13.json (study positions 0-389, or --reserves),
job ids pc13x_<case>_native, phase PX13, keep_raw false, archives on the pod-local disk /opt/claude_v13_xlocal.
--source protocol: the 300 protocol cases, captured with packet_main_v03 unchanged (its protocol is DEVELOPMENT_PROTOCOL_MAIN_v01).
--source extension: the generator-extension cases, captured with packet_x_v13 (= packet_main_v03 with DEVELOPMENT_PROTOCOL_X_v13.json,
the main protocol plus the appended extension cases; no code change).
Jobs of the source in position order are dealt to pods by C's rule (job g, stratum g % 3 = speed, goes to pod (g % 3 + g // 3) % n).
Checks: every job's keys are packet worker fields; every case is in the packet's protocol with role eval and family pedestrian_crossing;
the case file and the extended protocol have the given SHA-256.
Usage: python -I -B make_jobs_x_pc_v13.py --source protocol|extension --cases-sha SHA --pods NAME,... [--reserves POS,POS] [--tag v01] [--dry-run]
Outputs (never overwritten): jobs_x\\JOBS_PX13_<pod>_<tag>.json
"""
import argparse, hashlib, importlib.util, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
P = pathlib.Path(r'<library folder>')
MAIN_SOURCES = P / '03_runbook' / 'main_sources_v01'
MAIN = P / '06_phase0' / 'scenarios' / 'DEVELOPMENT_PROTOCOL_MAIN_v01.json'
MAIN_SHA = '32d683a0a8ca2e91ff0245759ad78b43e7953c33bd12847c5193cafcdaa5735d'
XPROTO = HERE / 'DEVELOPMENT_PROTOCOL_X_v13.json'
JOB_FIELDS = {'id', 'case', 'arm', 'alpha', 'beta', 'kappa', 'phase', 'role', 'scenario', 'keep_raw', 'reference', 'note', 'knob', 'history',
              'history_model', 'history_model_sha256'}            # packet_main_v03/claude_smoke_v01/worker_main_v01.py line 32
PHASE = 'PX13'
VOLUME_FOLDER = '/opt/claude_v13_xlocal'
CTL_EVERY = 50
spec = importlib.util.spec_from_file_location('mmj1', MAIN_SOURCES / 'make_main_jobs_v01.py')
v1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True, choices=('protocol', 'extension')); ap.add_argument('--cases-sha', required=True)
    ap.add_argument('--pods', required=True); ap.add_argument('--reserves', default=''); ap.add_argument('--tag', default='v01')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    cf = HERE / 'CASES_X_PC_v13.json'
    if sha(cf) != a.cases_sha: raise SystemExit('REFUSED: CASES_X_PC_v13.json differs from --cases-sha')
    X = json.loads(cf.read_text(encoding='utf-8'))
    if sha(MAIN) != MAIN_SHA: raise SystemExit('REFUSED: main protocol differs')
    proto_file = MAIN if a.source == 'protocol' else XPROTO
    proto = {c['id']: c for c in json.loads(proto_file.read_text(encoding='utf-8'))['cases']}
    if a.reserves:
        pos = [int(x) for x in a.reserves.split(',')]
        rows = [X['cases'][p] for p in pos]; assert all(r['reserve'] for r in rows)
    else:
        rows = [r for r in X['cases'] if not r['reserve']]
    rows = [r for r in rows if r['source'] == a.source]
    order = []
    for r in rows:
        pc = proto[r['case']]
        assert pc['role'] == 'eval' and pc['draw']['family'] == 'pedestrian_crossing' and pc['desired_mps'] == r['desired_mps'] and pc['seed'] == r['seed']
        order.append(dict(id=r['job'], case=r['case'], arm='native', alpha=r['alpha'], beta=r['alpha'], phase=PHASE, role='eval',
                          scenario=r['case'], keep_raw=False))
    assert all(set(j) <= JOB_FIELDS for j in order) and len({j['id'] for j in order}) == len(order)
    pods = [p for p in a.pods.split(',') if p]
    summary = {}
    for k, pod in enumerate(pods):
        sfx = pod[-2:]
        mine = [j for g, j in enumerate(order) if ((g % 3) + (g // 3)) % len(pods) == k]
        lst = [dict(v1.p1.job('x', 'crash', 'A1'), id=f'a1x13_{sfx}_{a.tag}_crash'), dict(v1.p1.job('x', 'benign', 'A1'), id=f'a1x13_{sfx}_{a.tag}_benign'),
               dict(v1.p1.job('x', 'learnedw0', 'A1'), id=f'a1x13_{sfx}_{a.tag}_learned')]
        n = 0
        lst.append(dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_{PHASE.lower()}_{sfx}_{a.tag}_{n:03d}'))
        for i, j in enumerate(mine):
            lst.append(j)
            if (i + 1) % CTL_EVERY == 0:
                n += 1; lst.append(dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_{PHASE.lower()}_{sfx}_{a.tag}_{n:03d}'))
        cfg = dict(schema='CLAUDE_MAIN_JOBS_V01', protocol='DEVELOPMENT_PROTOCOL_SMOKE_v01.json', volume_folder=VOLUME_FOLDER,
                   capture_timeout_s=600, review_timeout_s=600, actor_review_timeout_s=180, server_ready_timeout_s=120,
                   concurrent_start_stagger_s=15, max_attempts=2, protocol_main_sha256=MAIN_SHA,
                   note=(f'Revision v13 X (A11 sec. 3), pedestrian crossing, {a.source} cases, pod {pod} ({k + 1} of {len(pods)}); {len(mine)} study jobs; '
                         f'CASES_X_PC_v13.json {a.cases_sha[:12]}; packet ' + ('packet_main_v03 unchanged' if a.source == 'protocol' else
                         f'packet_x_v13 (protocol {sha(XPROTO)[:12]})') + '; native arm alpha = beta; keep_raw false.'),
                   made_by=dict(script='make_jobs_x_pc_v13.py', sha256=sha(__file__), imports_read_only='make_main_jobs_v01.py ' + sha(MAIN_SOURCES / 'make_main_jobs_v01.py')),
                   jobs=lst)
        summary[pod] = dict(study=len(mine), total=len(lst), speeds={v: sum(proto[j['case']]['desired_mps'] == v for j in mine) for v in (5, 10, 15)})
        if not a.dry_run:
            d = HERE / 'jobs_x'; d.mkdir(exist_ok=True)
            path = d / f'JOBS_{PHASE}_{pod}_{a.tag}.json'
            with open(path, 'x', encoding='utf-8', newline='\n') as f:
                f.write(json.dumps(cfg, indent=1) + '\n')
            summary[pod].update(file=path.name, sha256=sha(path))
    print(json.dumps(dict(source=a.source, study_jobs=len(order), dry_run=a.dry_run, pods=summary), indent=1))


if __name__ == '__main__':
    main()
