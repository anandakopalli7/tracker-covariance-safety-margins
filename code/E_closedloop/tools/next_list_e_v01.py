"""Start the next job list on a running, bootstrapped E pod whose worker has finished (P\\03_runbook\\pod_tools\\
Update-MainPod_v01.ps1 + Wait-ThenUpdate_v02.ps1 pattern): upload the packet (if newer), remote_update_and_work_v01.sh and the list
as /root/cmp/JOBS_NEXT.json, then run the update script detached. Refuses if the pod's worker status is RUNNING or HALTED_*.

python -I next_list_e_v01.py <pod name> <jobs json> [--packet packet_e_v01] [--slots 2]
python -I next_list_e_v01.py <pod name> --status        (prints /opt/claude_main/worker_status.json and the chain log tails)
"""
import argparse, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
E = HERE.parent
sys.path.insert(0, str(HERE))
import pods_e_v01 as pv   # noqa: E402


def status(name):
    r = pv.ssh(name, 'cat /opt/claude_main/worker_status.json 2>/dev/null; echo; tail -n 5 /root/main_chain*.log 2>/dev/null; '
                     'ls /opt/claude_smoke/BOOTSTRAP_OK.json 2>/dev/null', timeout=120)
    return r.stdout


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('name'); ap.add_argument('jobs', nargs='?'); ap.add_argument('--packet', default='packet_e_v01')
    ap.add_argument('--slots', type=int, default=2); ap.add_argument('--status', action='store_true')
    a = ap.parse_args()
    if a.status or not a.jobs:
        print(status(a.name)); return
    st = status(a.name)
    first = st.strip().splitlines()[0] if st.strip() else ''
    try: ws = json.loads(first)
    except Exception: ws = {}
    if ws.get('status') != 'FINISHED':
        raise SystemExit('REFUSED: worker status is %r, not FINISHED' % ws.get('status'))
    tar = E / 'packets' / f'{a.packet}.tar.gz'
    lines = ['-mkdir /root/cmp', f'put "{tar}" /root/cmp/{a.packet}.tar.gz', f'put "{HERE / "remote_update_and_work_v01.sh"}" /root/cmp/remote_update_and_work_v01.sh',
             f'put "{pathlib.Path(a.jobs).resolve()}" /root/cmp/JOBS_NEXT.json']
    r = pv.sftp(a.name, lines)
    if r.returncode != 0: raise SystemExit('upload failed: ' + (r.stderr or r.stdout)[-500:])
    cmd = (f"sed -i 's/\\r$//' /root/cmp/remote_update_and_work_v01.sh; sha256sum /root/cmp/JOBS_NEXT.json /root/cmp/{a.packet}.tar.gz; "
           f"S=$(date --utc +%Y%m%dT%H%M%SZ); setsid nohup bash /root/cmp/remote_update_and_work_v01.sh {a.packet} {a.slots} > /root/main_chain_$S.log 2>&1 < /dev/null & "
           f"sleep 5; tail -n 5 /root/main_chain_*.log")
    r = pv.ssh(a.name, cmd, timeout=180)
    print(r.stdout[-2000:], r.stderr[-1000:])


if __name__ == '__main__':
    main()
