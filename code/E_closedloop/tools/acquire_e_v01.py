"""Package E: copy of CD_capture/tools/acquire_v13.py (E paths, E pod helper, E packets folder). Acquire pods and launch a job list on each (background loop).

python -I acquire_v13.py --names claude-v13e-01 --jobs-glob "jobs/JOBS_E1_{name}_v01.json" --packet packet_e_v01
       [--gpus "NVIDIA GeForce RTX 4090,NVIDIA L4"] [--hours 6] [--sleep 45] [--deadline-h 10]

For each name without a pod record: try each GPU type in order (EU-RO-1, volume <cloud volume id>). On success, upload the
packet tarball, remote_chain_v01.sh and the name's job list, then launch the chain detached (simulate rehearsal ->
bootstrap -> worker), exactly as P\\03_runbook\\pod_tools\\Start-MainPod_v01.ps1 did. A failed create costs nothing.
Writes a log line per attempt to pods/acquire.log.
"""
import argparse, datetime, json, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
CD = HERE.parent   # = work/E_closedloop (name kept from the copied code)
sys.path.insert(0, str(HERE))
import pods_e_v01 as pv

LOG = CD / 'pods' / 'acquire.log'


def log(msg):
    line = f'{datetime.datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z} {msg}'
    print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f: f.write(line + '\n')


def launch(name, jobs, packet, slots):
    tar = CD / 'packets' / f'{packet}.tar.gz'
    chain = HERE / 'remote_chain_v01.sh'
    ok = False
    for i in range(8):
        r = pv.sftp(name, ['-mkdir /root/cmp', f'put "{tar}" /root/cmp/{packet}.tar.gz', f'put "{chain}" /root/cmp/remote_chain_v01.sh',
                           f'put "{jobs}" /root/cmp/JOBS.json'])
        if r.returncode == 0: ok = True; break
        log(f'{name} upload attempt {i + 1} failed: {(r.stderr or r.stdout)[-300:]!r}')
        time.sleep(20)
    if not ok: log(f'{name} UPLOAD FAILED'); return False
    cmd = (f"sed -i 's/\\r$//' /root/cmp/remote_chain_v01.sh; sha256sum /root/cmp/{packet}.tar.gz /root/cmp/JOBS.json; "
           f"setsid nohup bash /root/cmp/remote_chain_v01.sh {packet} {slots} > /root/main_chain.log 2>&1 < /dev/null & sleep 3; cat /root/main_chain.log")
    r = pv.ssh(name, cmd, timeout=120)
    log(f'{name} launch rc={r.returncode} out={r.stdout.strip()[-400:]!r}')
    (CD / 'pods' / name / 'LAUNCHED.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), jobs=str(jobs),
        packet=packet, slots=slots, stdout=r.stdout[-2000:]), indent=1), encoding='utf-8')
    return r.returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--names', required=True); ap.add_argument('--jobs-glob', required=True); ap.add_argument('--packet', default='packet_main_v03')
    ap.add_argument('--gpus', default='NVIDIA GeForce RTX 4090,NVIDIA L4'); ap.add_argument('--hours', type=float, default=6)
    ap.add_argument('--sleep', type=float, default=45); ap.add_argument('--deadline-h', type=float, default=10); ap.add_argument('--slots', type=int, default=2)
    ap.add_argument('--note', default='package E')
    a = ap.parse_args()
    names = a.names.split(','); gpus = a.gpus.split(','); until = time.time() + a.hours * 3600
    log(f'acquire start names={names} gpus={gpus}')
    while time.time() < until:
        missing = [n for n in names if not (CD / 'pods' / n / 'pod.json').exists()]
        if not missing: break
        for n in missing:
            got = False
            for g in gpus:
                try:
                    pv.create(n, g, a.deadline_h, a.note)
                    got = True
                except SystemExit as e:
                    log(f'{n} {g}: no pod ({e})')
                    import shutil
                    rec = CD / 'pods' / n
                    if rec.is_dir() and not (rec / 'pod.json').exists():
                        (rec / 'create_stdout.txt').unlink(missing_ok=True)
                    continue
                except Exception as e:
                    log(f'{n} {g}: error {type(e).__name__}: {e}')
                    continue
                log(f'{n} CREATED on {g}')
                jobs = CD / a.jobs_glob.format(name=n)
                launch(n, jobs, a.packet, a.slots)
                break
            if not got: break       # no stock now: wait before trying the next name
        time.sleep(a.sleep)
    log('acquire end; missing=' + ','.join(n for n in names if not (CD / 'pods' / n / 'pod.json').exists()))


if __name__ == '__main__':
    main()
