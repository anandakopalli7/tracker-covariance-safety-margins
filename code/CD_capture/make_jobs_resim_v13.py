"""Task 5 (A10 sec. 0.2, FEASIBILITY sec. 3): re-simulate the 55 old lead-braking runs to recover their 20 Hz sweeps.

Runs: the 35 old evaluation runs (P\\07_fit_runs\\archives\\p1b_fit_finite_0005..0039) and the 20 lead-braking tuning runs
(P\\08_phase2\\archives_c1\\p2_c1109_tune_<i>_fixed_c1 with case family lead_braking). Each job repeats the old job exactly: same case,
arm and knobs (alpha, beta, kappa) read from the old run's own SUMMARY.json; keep_raw true; packet_main_v03. Job id 'rs13_<old job id>'.
Acceptance (A10 sec. 0.2): a re-simulated run replaces nothing and is accepted only if every frame's noisy-sweep SHA-256
(frames.jsonl raw_sha256) equals the old run's logged value, with the same number of frames (check_resim_v13.py).
Usage: python -I make_jobs_resim_v13.py --lists claude-v13cd-01,...   (never overwrites)
"""
import argparse, hashlib, importlib.util, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
P = pathlib.Path(r'<library folder>')
spec = importlib.util.spec_from_file_location('mjc', HERE / 'make_jobs_c_v13.py'); mjc = importlib.util.module_from_spec(spec); spec.loader.exec_module(mjc)
v1 = mjc.v1


def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def old_runs():
    proto = {c['id']: c for c in json.loads((P / '06_phase0' / 'scenarios' / 'DEVELOPMENT_PROTOCOL_MAIN_v01.json').read_text(encoding='utf-8'))['cases']}
    rows = []
    for i in range(5, 40):
        rows.append(P / '07_fit_runs' / 'archives' / f'p1b_fit_finite_{i:04d}')
    for d in sorted((P / '08_phase2' / 'archives_c1').glob('p2_c1109_tune_*_fixed_c1')):
        s = json.loads((d / 'SUMMARY.json').read_text(encoding='utf-8'))
        if proto[s['case']]['draw']['family'] == 'lead_braking': rows.append(d)
    out = []
    for d in rows:
        s = json.loads((d / 'SUMMARY.json').read_text(encoding='utf-8'))
        assert s['status'] == 'CAPTURED_AND_REVIEWED' and proto[s['case']]['draw']['family'] == 'lead_braking'
        j = dict(id=f"rs13_{s['job']}", case=s['case'], arm=s['arm'], phase='RS13', role='resim', scenario=s['case'], keep_raw=True)
        for k in ('alpha', 'beta', 'kappa'):
            if s['knobs'].get(k) is not None: j[k] = s['knobs'][k]
        out.append((j, d))
    assert len(out) == 55, len(out)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--lists', required=True); ap.add_argument('--tag', default='v01')
    a = ap.parse_args(); lists = a.lists.split(',')
    jobs = old_runs()
    (HERE / 'RESIM_SOURCES_v13.json').write_text(json.dumps([dict(job=j['id'], old_run=str(d)) for j, d in jobs], indent=1), encoding='utf-8')
    for k, name in enumerate(lists):
        mine = [j for i, (j, d) in enumerate(jobs) if i % len(lists) == k]
        lst = [dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_rs13_{name[-2:]}_{a.tag}_000')] + mine
        cfg = dict(schema='CLAUDE_MAIN_JOBS_V01', protocol='DEVELOPMENT_PROTOCOL_SMOKE_v01.json', volume_folder='/opt/claude_v13_resim',
                   capture_timeout_s=600, review_timeout_s=600, actor_review_timeout_s=180, server_ready_timeout_s=120,
                   concurrent_start_stagger_s=15, max_attempts=1, note=f'Task 5 re-simulation of old lead-braking runs, list {name}; packet_main_v03.',
                   made_by=dict(script='make_jobs_resim_v13.py', sha256=sha(__file__)), jobs=lst)
        path = HERE / 'jobs' / f'JOBS_RS13_{name}_{a.tag}.json'
        with open(path, 'x', encoding='utf-8', newline='\n') as f: f.write(json.dumps(cfg, indent=1) + '\n')
        print(path.name, len(mine))


if __name__ == '__main__':
    main()
