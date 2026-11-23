"""Package E, set E4: finish one E4 pod (copy of finish_pod_e_v01.py with the E4 lists and NARROW fetch prefixes, so the
fetch guard sizes its margin by this pod's runs only). Original text follows: finish one E3 pod (20 Nov 2026). Fetch its archives from the volume (receipt-verified, fetch_e_v01.py), check that
EVERY job of its two frozen lists (E3 156 + E3b 54, incl. A1 admission and controls) has a verified run on the laptop, and only
then terminate it with terminate_e_v01.py (rc=0 and absent from the pod list). Reads no outcome. Writes pods/<name>/FINISH.json.

python -I finish_pod_e_v01.py <pod name>
Exit 0: pod complete and deleted. Exit 2: something missing (pod kept; the list is in FINISH.json). Exit 3: delete not confirmed.
"""
import datetime, json, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
E = HERE.parent


def main():
    name = sys.argv[1]; nn = name[-2:]
    assert name.startswith('claude-v13e-1') and nn in ('11', '12', '13', '14', '15', '16'), name
    jobs = [j['id'] for f in (E / 'jobs' / f'JOBS_E4L_{name}_v01.json', E / 'jobs' / f'JOBS_E4H_{name}_v01.json') if f.exists()
            for j in json.loads(f.read_text(encoding='utf-8'))['jobs']]
    pre = sorted(jobs)                     # exact job ids as prefixes (the guard then counts this pod's runs only)
    log = []
    for attempt in range(3):
        r = subprocess.run([sys.executable, '-I', str(HERE / 'fetch_e_v01.py'), *pre, '--threads', '8'], capture_output=True, text=True, cwd=str(HERE))
        log.append(dict(attempt=attempt + 1, rc=r.returncode, tail=(r.stdout + r.stderr).strip()[-400:]))
        jobs = [j['id'] for f in (E / 'jobs' / f'JOBS_E4L_{name}_v01.json', E / 'jobs' / f'JOBS_E4H_{name}_v01.json') if f.exists()
                for j in json.loads(f.read_text(encoding='utf-8'))['jobs']]
        missing = [j for j in jobs if not [d for d in (E / 'runs').glob(j + '*') if (d.name == j or d.name.startswith(j + '__')) and (d / 'FETCH_OK.json').exists()]]
        if not missing: break
    rec = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), pod=name, jobs=len(jobs), missing=missing, fetch=log)
    if missing:
        rec['decision'] = 'kept: runs missing'
        (E / 'pods' / name / 'FINISH.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
        print(f'FINISH {name}: {len(missing)} of {len(jobs)} jobs missing; pod kept: {missing[:8]}'); sys.exit(2)
    t = subprocess.run([sys.executable, '-I', str(HERE / 'terminate_e_v01.py'), name, '--note',
                        f'E4 L and H done; all {len(jobs)} runs fetched and receipt-verified on the laptop'],
                       capture_output=True, text=True, cwd=str(HERE))
    rec.update(decision='terminate', terminate_rc=t.returncode, terminate_tail=(t.stdout + t.stderr).strip()[-600:])
    (E / 'pods' / name / 'FINISH.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    if t.returncode != 0:
        print(f'FINISH {name}: all {len(jobs)} jobs verified, but DELETE NOT CONFIRMED rc={t.returncode}'); sys.exit(3)
    print(f'FINISH {name}: all {len(jobs)} jobs verified; pod deleted (confirmed)'); sys.exit(0)


if __name__ == '__main__':
    main()
