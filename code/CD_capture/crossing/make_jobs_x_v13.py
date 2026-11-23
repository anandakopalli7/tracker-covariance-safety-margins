"""Crossing sprint (A11): job lists for the fresh crossing capture. New file, 21 Nov 2026 (Claude Opus 5.5, session CD).

A copy of make_jobs_c_v13.py's job format (C's capture settings: packet_main_v03 unchanged, native recording arm, alpha = beta,
the same admission and control jobs from P\\03_runbook\\main_sources_v01\\make_main_jobs_v01.py, imported read-only, the same
timeouts), with four differences: cases from CASES_X_v13.json (first n per family, A11), phase PX13 (job ids px13_<case>_native),
archives on the pod-local disk /opt/claude_v13_xlocal (as C's v02 lists; the network volume is not used), keep_raw false (the capture's sweep frames are not archived; FILE_HASHES.json still lists them; CD's extractor and B's re-tracking
read only the logs). Study jobs alternate the families by position (v0, p0, v1, p1, ...), so job g has stratum g % 6 (family x
speed), and are dealt to pods by C's rule, so every pod gets a mix of strata.
Checks: every study job's keys are fields the packet's worker accepts (worker_main_v01.JOB_FIELDS); every case is in the protocol of
record with role eval and the family of CASES_X; CASES_X_v13.json has the SHA-256 given with --cases-sha.
Usage: python -I -B make_jobs_x_v13.py --n N --cases-sha SHA --pods claude-v13cx-01,... [--tag v01] [--dry-run]
       --dry-run writes nothing (prints the per-pod counts and the checks).
Outputs (never overwritten): jobs_x\\JOBS_PX13_<pod>_<tag>.json.
"""
import argparse, hashlib, importlib.util, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
P = pathlib.Path(r'<library folder>')
MAIN_SOURCES = P / '03_runbook' / 'main_sources_v01'
PROTOCOL = P / '06_phase0' / 'scenarios' / 'DEVELOPMENT_PROTOCOL_MAIN_v01.json'
PROTOCOL_SHA256 = '32d683a0a8ca2e91ff0245759ad78b43e7953c33bd12847c5193cafcdaa5735d'
PACKET = CD / 'packets' / 'packet_main_v03.tar.gz'
PACKET_SHA256 = '6ae57b9f7b096278a3fbbcaa3d6fa19927c4bc326d58c35a4bdcb4ca61d85ec5'
JOB_FIELDS = {'id', 'case', 'arm', 'alpha', 'beta', 'kappa', 'phase', 'role', 'scenario', 'keep_raw', 'reference', 'note', 'knob', 'history',
              'history_model', 'history_model_sha256'}            # packet_main_v03/claude_smoke_v01/worker_main_v01.py line 32
PHASE = 'PX13'
VOLUME_FOLDER = '/opt/claude_v13_xlocal'        # pod-local disk, as C's v02 lists after the volume quota (archives: <it>/results/<rid>/)
CTL_EVERY = 50
FAMILIES = ('vehicle_crossing', 'pedestrian_crossing')

spec = importlib.util.spec_from_file_location('mmj1', MAIN_SOURCES / 'make_main_jobs_v01.py')
v1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, required=True); ap.add_argument('--cases-sha', required=True); ap.add_argument('--pods', required=True)
    ap.add_argument('--tag', default='v01'); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    cf = HERE / 'CASES_X_v13.json'
    if sha(cf) != a.cases_sha: raise SystemExit('REFUSED: CASES_X_v13.json differs from --cases-sha')
    if sha(PACKET) != PACKET_SHA256: raise SystemExit('REFUSED: packet_main_v03.tar.gz differs from C\'s')
    raw = PROTOCOL.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PROTOCOL_SHA256: raise SystemExit('REFUSED: protocol differs')
    proto = {c['id']: c for c in json.loads(raw)['cases']}
    X = json.loads(cf.read_text(encoding='utf-8'))
    if not 0 < a.n <= X['n_study']: raise SystemExit('REFUSED: n must be 1..%d' % X['n_study'])
    order = []
    for i in range(a.n):
        for fam in FAMILIES:
            c = X['families'][fam][i]
            assert c['position'] == i and not c['reserve'] and c['family'] == fam
            pc = proto[c['case']]
            assert pc['role'] == 'eval' and pc['draw']['family'] == fam and pc['desired_mps'] == c['desired_mps'] and pc['seed'] == c['seed']
            order.append(dict(id=c['job'], case=c['case'], arm='native', alpha=c['alpha'], beta=c['alpha'], phase=PHASE, role='eval',
                              scenario=c['case'], keep_raw=False))
    assert all(set(j) <= JOB_FIELDS for j in order)
    assert len({j['id'] for j in order}) == len(order) == 2 * a.n
    pods = [p for p in a.pods.split(',') if p]
    out = {}
    for k, pod in enumerate(pods):
        sfx = pod[-2:]
        # C's deal (make_jobs_c_v13.pod_lists): job g (stratum m = g % 6 = family x speed, rank g // 6) goes to pod (m + g // 6) % n
        mine = [j for g, j in enumerate(order) if ((g % 6) + (g // 6)) % len(pods) == k]
        lst = [dict(v1.p1.job('x', 'crash', 'A1'), id=f'a1x13_{sfx}_crash'), dict(v1.p1.job('x', 'benign', 'A1'), id=f'a1x13_{sfx}_benign'),
               dict(v1.p1.job('x', 'learnedw0', 'A1'), id=f'a1x13_{sfx}_learned')]
        n = 0
        lst.append(dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_{PHASE.lower()}_{sfx}_{a.tag}_{n:03d}'))
        for i, j in enumerate(mine):
            lst.append(j)
            if (i + 1) % CTL_EVERY == 0:
                n += 1; lst.append(dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_{PHASE.lower()}_{sfx}_{a.tag}_{n:03d}'))
        cfg = dict(schema='CLAUDE_MAIN_JOBS_V01', protocol='DEVELOPMENT_PROTOCOL_SMOKE_v01.json', volume_folder=VOLUME_FOLDER,
                   capture_timeout_s=600, review_timeout_s=600, actor_review_timeout_s=180, server_ready_timeout_s=120,
                   concurrent_start_stagger_s=15, max_attempts=2, protocol_main_sha256=PROTOCOL_SHA256,
                   note=(f'Revision v13 crossing sprint (A11), pod {pod} ({k + 1} of {len(pods)}); {len(mine)} of {2 * a.n} study jobs '
                         f'(first {a.n} per family of CASES_X_v13.json {a.cases_sha[:12]}); packet_main_v03 unchanged; native arm alpha = beta; '
                         'keep_raw false.'),
                   made_by=dict(script='make_jobs_x_v13.py', sha256=sha(__file__), imports_read_only='make_main_jobs_v01.py ' + sha(MAIN_SOURCES / 'make_main_jobs_v01.py')),
                   jobs=lst)
        out[pod] = (cfg, mine)
    summary = {}
    for pod, (cfg, mine) in out.items():
        fams = {f: sum(proto[j['case']]['draw']['family'] == f for j in mine) for f in FAMILIES}
        summary[pod] = dict(study=len(mine), total=len(cfg['jobs']), families=fams)
        if not a.dry_run:
            d = HERE / 'jobs_x'; d.mkdir(exist_ok=True)
            path = d / f'JOBS_{PHASE}_{pod}_{a.tag}.json'
            with open(path, 'x', encoding='utf-8', newline='\n') as f:
                f.write(json.dumps(cfg, indent=1) + '\n')
            summary[pod].update(file=path.name, sha256=sha(path))
    print(json.dumps(dict(phase=PHASE, n_per_family=a.n, study_jobs=len(order), dry_run=a.dry_run, pods=summary), indent=1))


if __name__ == '__main__':
    main()
