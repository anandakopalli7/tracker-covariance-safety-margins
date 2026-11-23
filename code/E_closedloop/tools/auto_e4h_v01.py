"""Package E, set E4 (A11 §6d): the H list starts on a pod only after its L list is FINISHED (pre-registered order).
Copy of auto_e3b_v01.py with E4L -> E4H in place of E3 -> E3b. Original text follows: follow-on lists for the E3 pods (19 Nov 2026). Reads worker statuses only (no outcome values; Lock 2 gate).

Every --sleep seconds, for each pod claude-v13e-04..09 that has a pod record and an SSH config and is not TERMINATED:
- Read /opt/claude_main/worker_status.json.
- If the status is FINISHED, the total equals the pod's E3 list length, and there is no E3B_LAUNCHED.json: start the pod's
  E3b list with next_list_e_v01.py (packet_e_v03, 2 slots) and write E3B_LAUNCHED.json (the next_list output).
- If the status is FINISHED, the total equals the pod's E3b list length, and E3B_LAUNCHED.json exists: write
  READY_FOR_FETCH.json once (status, done_ok, failed_final).
- Print one line when the joint status line changes, and one line per action (E4H_START, READY_FOR_FETCH, ERROR).
Stop: create pods/STOP_AUTO_E3B. Runs runpodctl-free (SSH only), so the API's DNS trouble does not affect it.

python -I auto_e3b_v01.py [--sleep 150]
"""
import argparse, datetime, json, os, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
E = HERE.parent
sys.path.insert(0, str(HERE))
import pods_e_v01 as pv   # noqa: E402


def now():
    return datetime.datetime.now().astimezone().strftime('%H:%M:%S')


def say(msg):
    print(f'{now()} {msg}', flush=True)


def njobs(p):
    return len(json.loads(pathlib.Path(p).read_text(encoding='utf-8'))['jobs'])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--sleep', type=float, default=150)
    a = ap.parse_args()
    prev = None; halted_said = set()
    while not (pv.PODS / 'STOP_AUTO_E4H').exists():
        parts = []
        for d in sorted(pv.PODS.glob('claude-v13e-1[1-6]')):
            n = d.name
            if not (d / 'pod.json').exists(): continue
            if (d / 'TERMINATED').exists(): parts.append(n[-2:] + ':terminated'); continue
            if not (d / 'ssh_config').exists(): parts.append(n[-2:] + ':creating'); continue
            j3 = E / 'jobs' / f'JOBS_E4L_{n}_v01.json'; j3b = E / 'jobs' / f'JOBS_E4H_{n}_v01.json'
            try:
                r = pv.ssh(n, 'cat /opt/claude_main/worker_status.json 2>/dev/null || echo NOSTATUS', timeout=60)
                s = json.loads(r.stdout.strip().splitlines()[0])
            except Exception:
                parts.append(n[-2:] + ':booting'); continue
            st, tot, dn = s.get('status'), s.get('total') or 0, s.get('done_ok') or 0
            ff = s.get('failed_final') or []
            phase = 'E4H' if (d / 'E4H_LAUNCHED.json').exists() else 'E4L'
            shown = (dn // 25) * 25 if st == 'RUNNING' else dn
            parts.append(f'{n[-2:]}:{phase}:{st}:{shown}/{tot}:f{len(ff)}:ctl{(s.get("last_control") or {}).get("identical")}')
            if st == 'FINISHED' and phase == 'E4L' and tot == njobs(j3):
                say(f'E4H_START {n} (E4L finished: done_ok {dn}/{tot}, failed_final {len(ff)})')
                env = dict(os.environ); env.pop('RUNPOD_API_KEY', None)
                p = subprocess.run([sys.executable, '-I', str(HERE / 'next_list_e_v01.py'), n, str(j3b), '--packet', 'packet_e_v04', '--slots', '2'],
                                   capture_output=True, text=True, timeout=900, env=env)
                ok = p.returncode == 0 and 'REFUSED' not in p.stdout + p.stderr
                rec = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), rc=p.returncode, ok=ok, e4l_status=s,
                           stdout=p.stdout[-3000:], stderr=p.stderr[-2000:])
                if ok:
                    (d / 'E4H_LAUNCHED.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
                    say(f'E4H_STARTED {n}')
                else:
                    (d / f'E4H_LAUNCH_FAIL_{int(time.time())}.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
                    say(f'ERROR E4H launch {n} rc={p.returncode}: {(p.stderr or p.stdout).strip()[-200:]!r}')
            elif st == 'FINISHED' and phase == 'E4H' and tot == njobs(j3b) and not (d / 'READY_FOR_FETCH.json').exists():
                (d / 'READY_FOR_FETCH.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), e4h_status=s), indent=1), encoding='utf-8')
                say(f'READY_FOR_FETCH {n} (E4H done_ok {dn}/{tot}, failed_final {len(ff)})')
            elif st and st.startswith('HALTED') and (n, st) not in halted_said:
                halted_said.add((n, st)); say(f'ERROR {n} worker {st}')
        line = ' '.join(parts) or 'no E3 pod yet'
        if line != prev:
            say('STATUS ' + line); prev = line
        time.sleep(a.sleep)
    say('stopped')


if __name__ == '__main__':
    main()
