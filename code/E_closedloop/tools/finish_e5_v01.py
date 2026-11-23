"""Package E, set E5: watch a set of one-list pods; when a pod's worker is FINISHED (total = its list), fetch its exact job ids
(fetch_e_v01.py, S3; on an S3 failure, SFTP through that pod), check that EVERY job of its list has a verified run on the laptop,
then delete it with terminate_e_v01.py (rc=0 and absent from the pod list). Reads statuses only. Prints one line per event.

python -I finish_e5_v01.py --stage E5C --pods 21,22,23,24     (lists jobs\\JOBS_<stage>_claude-v13e-<nn>_v01.json)
Stop: pods\\STOP_FINISH_E5.
"""
import argparse, datetime, json, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
E = HERE.parent
sys.path.insert(0, str(HERE))
import pods_e_v01 as pv   # noqa: E402


def say(m):
    print(f'{datetime.datetime.now():%H:%M:%S} {m}', flush=True)


def verified(jobs):
    return [j for j in jobs if not [d for d in (E / 'runs').glob(j + '*') if (d.name == j or d.name.startswith(j + '__')) and (d / 'FETCH_OK.json').exists()]]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--stage', required=True); ap.add_argument('--pods', required=True); ap.add_argument('--sleep', type=float, default=90)
    a = ap.parse_args()
    names = [f'claude-v13e-{n}' for n in a.pods.split(',')]
    lists = {n: [j['id'] for j in json.loads((E / 'jobs' / f'JOBS_{a.stage}_{n}_v01.json').read_text(encoding='utf-8'))['jobs']] for n in names}
    prev = None
    while not (pv.PODS / 'STOP_FINISH_E5').exists():
        line = []; left = 0
        for n in names:
            d = pv.PODS / n
            if (d / 'TERMINATED').exists(): line.append(n[-2:] + ':deleted'); continue
            left += 1
            if not (d / 'ssh_config').exists(): line.append(n[-2:] + ':creating'); continue
            try:
                r = pv.ssh(n, 'cat /opt/claude_main/worker_status.json 2>/dev/null || echo NOSTATUS', timeout=60)
                s = json.loads(r.stdout.strip().splitlines()[0])
            except Exception:
                line.append(n[-2:] + ':booting'); continue
            st, tot, dn, ff = s.get('status'), s.get('total') or 0, s.get('done_ok') or 0, s.get('failed_final') or []
            ctl = (s.get('last_control') or {}).get('identical')
            line.append(f'{n[-2:]}:{st}:{dn}/{tot}:f{len(ff)}:ctl{ctl}')
            if st and st.startswith('HALTED'): say(f'ERROR {n} worker {st}')
            if st == 'FINISHED' and tot == len(lists[n]):
                say(f'READY {n} done_ok {dn}/{tot} failed_final {len(ff)}')
                jobs = lists[n]; miss = verified(jobs)
                for via in (None, None, n):          # S3 twice, then SFTP through the pod
                    if not miss: break
                    cmd = [sys.executable, '-I', str(HERE / 'fetch_e_v01.py'), *miss, '--threads', '6'] + (['--sftp', via] if via else [])
                    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(HERE))
                    say(f'fetch {n} via {"sftp" if via else "s3"} rc={p.returncode} {(p.stdout + p.stderr).strip()[-160:]!r}')
                    miss = verified(jobs)
                if miss: say(f'KEPT {n}: {len(miss)} of {len(jobs)} jobs missing {miss[:5]}'); continue
                t = subprocess.run([sys.executable, '-I', str(HERE / 'terminate_e_v01.py'), n, '--note', f'E5 {a.stage} list done; all {len(jobs)} runs fetched and receipt-verified'],
                                   capture_output=True, text=True, cwd=str(HERE))
                say(f'{"DELETED" if t.returncode == 0 else "DELETE NOT CONFIRMED"} {n} rc={t.returncode}')
        s = ' '.join(line)
        if s != prev: say('STATUS ' + s); prev = s
        if left == 0: say('all pods deleted'); break
        time.sleep(a.sleep)


if __name__ == '__main__':
    main()
