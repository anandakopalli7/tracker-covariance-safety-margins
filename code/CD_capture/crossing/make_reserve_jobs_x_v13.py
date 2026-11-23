"""X (A11 sec. 3.2): replacements of study runs that failed twice, and the job list that captures them. New file, 21 Nov 2026 (Claude Opus
5.5, session CD). Rule (A11 sec. 3.2, A10 sec. 5.1): "a second failure is replaced by the next unused case of the same family and speed,
same alpha; each replacement reported". The reserve is the lowest-position unused reserve of the failed case's speed in CASES_X_PC_v13.json;
the job keeps the FAILED case's alpha = beta (not the reserve's own cycle value). REPLACEMENTS_X_v13.json is append-only:
{"replacements": {failed case: reserve case}, "records": [...]}; an existing entry is never changed.
Job list: C's format (make_jobs_x_pc_v13.py): a crash control first, the replacement jobs, a crash control last; phase PX13, keep_raw
false, archives on the pod-local disk. Reserves are extension cases, so the list runs with packet_x_v13.
Usage: python -I -B make_reserve_jobs_x_v13.py --cases-sha SHA --failed CASE[,CASE] --why TEXT --pod NAME --tag v02 [--dry-run]
"""
import argparse, hashlib, importlib.util, json, pathlib, time
HERE = pathlib.Path(__file__).resolve().parent
P = pathlib.Path(r'<library folder>')
spec = importlib.util.spec_from_file_location('mmj1', P / '03_runbook' / 'main_sources_v01' / 'make_main_jobs_v01.py')
v1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v1)
MAIN_SHA = '32d683a0a8ca2e91ff0245759ad78b43e7953c33bd12847c5193cafcdaa5735d'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cases-sha', required=True); ap.add_argument('--failed', required=True); ap.add_argument('--why', required=True)
    ap.add_argument('--pod', required=True); ap.add_argument('--tag', required=True); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    cf = HERE / 'CASES_X_PC_v13.json'
    if sha(cf) != a.cases_sha: raise SystemExit('REFUSED: CASES_X_PC_v13.json differs')
    X = json.loads(cf.read_text(encoding='utf-8')); rows = {r['case']: r for r in X['cases']}
    xproto = {c['id'] for c in json.loads((HERE / 'DEVELOPMENT_PROTOCOL_X_v13.json').read_text(encoding='utf-8'))['cases']}
    rp = HERE / 'REPLACEMENTS_X_v13.json'
    doc = json.loads(rp.read_text(encoding='utf-8')) if rp.is_file() else dict(schema='REPLACEMENTS_X_V13', rule=__doc__.split('Rule')[1].split('Job list')[0].strip(),
                                                                                    replacements={}, records=[])
    used = set(doc['replacements'].values())
    jobs = []
    for fc in a.failed.split(','):
        f = rows[fc]; assert not f['reserve'], 'the failed case must be a study case'
        if fc in doc['replacements']: raise SystemExit('REFUSED: %s already replaced by %s' % (fc, doc['replacements'][fc]))
        cand = [r for r in X['cases'] if r['reserve'] and r['desired_mps'] == f['desired_mps'] and r['case'] not in used]
        if not cand: raise SystemExit('REFUSED: no unused reserve of speed %s' % f['desired_mps'])
        r = min(cand, key=lambda x: x['position']); used.add(r['case'])
        assert r['case'] in xproto
        doc['replacements'][fc] = r['case']
        doc['records'].append(dict(failed=fc, failed_position=f['position'], reserve=r['case'], reserve_position=r['position'], desired_mps=f['desired_mps'],
                                   alpha=f['alpha'], why=a.why, written=time.strftime('%Y-%m-%d %H:%M %Z')))
        jobs.append(dict(id=f"pc13x_{r['case']}_native", case=r['case'], arm='native', alpha=f['alpha'], beta=f['alpha'], phase='PX13', role='eval',
                         scenario=r['case'], keep_raw=False))
    sfx = a.pod[-2:]
    lst = [dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_px13_{sfx}_{a.tag}_000')] + jobs + [dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_px13_{sfx}_{a.tag}_001')]
    cfg = dict(schema='CLAUDE_MAIN_JOBS_V01', protocol='DEVELOPMENT_PROTOCOL_SMOKE_v01.json', volume_folder='/opt/claude_v13_xlocal',
               capture_timeout_s=600, review_timeout_s=600, actor_review_timeout_s=180, server_ready_timeout_s=120, concurrent_start_stagger_s=15,
               max_attempts=2, protocol_main_sha256=MAIN_SHA,
               note=f'Revision v13 X (A11 sec. 3.2) replacements on {a.pod}: ' + ', '.join(f"{k}->{v}" for k, v in doc['replacements'].items() if f"pc13x_{v}_native" in [j['id'] for j in jobs])
                    + '; packet_x_v13; alpha = beta of the failed case; keep_raw false.',
               made_by=dict(script='make_reserve_jobs_x_v13.py', sha256=sha(__file__)), jobs=lst)
    print(json.dumps(dict(replacements=doc['replacements'], jobs=[j['id'] for j in lst]), indent=1))
    if a.dry_run: return
    d = HERE / 'jobs_x'; path = d / f'JOBS_PX13_{a.pod}_{a.tag}.json'
    with open(path, 'x', encoding='utf-8', newline='\n') as f: f.write(json.dumps(cfg, indent=1) + '\n')
    rp.write_text(json.dumps(doc, indent=1) + '\n', encoding='utf-8', newline='\n')
    print(path.name, sha(path), '| REPLACEMENTS_X_v13.json', sha(rp))


if __name__ == '__main__':
    main()
