"""Run the next job list on a bootstrapped pod whose worker has finished (as P\\03_runbook\\pod_tools\\Update-MainPod_v01.ps1).
Uploads the packet tarball, remote_update_and_work_v01.sh and the list as /root/cmp/JOBS_NEXT.json, then launches the
update script detached: it switches the staged claude_smoke_v01 to the packet (update_main_packet_v01.py: manifest check,
superseded copies, new release, CPU self-check) when the binding differs, and runs the worker on the list.
Refuses if the pod's worker status is RUNNING.
Usage: python -I next_list_v13.py NAME PACKET JOBS_FILE [SLOTS]
"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(HERE))
import pods_v13 as pv

name, packet, jobs = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]).resolve()
slots = int(sys.argv[4]) if len(sys.argv) > 4 else 2
r = pv.ssh(name, "python3 -c \"import json;print(json.load(open('/opt/claude_main/worker_status.json'))['status'])\"", timeout=150)
st = r.stdout.strip()
alive = pv.ssh(name, "pgrep -f '[w]orker_main_v01.py' >/dev/null && echo ALIVE || echo NONE", timeout=60).stdout.strip()
assert alive == 'NONE' and (st in ('FINISHED', 'HALTED_ALL_SLOTS_PAUSED') or st == 'RUNNING'), f'worker status {st!r}, process {alive}; refusing'
print(name, 'worker status', st, 'process', alive)
tar = CD / 'packets' / f'{packet}.tar.gz'
r = pv.sftp(name, ['-mkdir /root/cmp', f'put "{tar}" /root/cmp/{packet}.tar.gz', f'put "{HERE / "remote_update_and_work_v01.sh"}" /root/cmp/remote_update_and_work_v01.sh',
                   f'put "{jobs}" /root/cmp/JOBS_NEXT.json'])
assert r.returncode == 0, r.stderr[-500:]
cmd = (f"sed -i 's/\\r$//' /root/cmp/remote_update_and_work_v01.sh; sha256sum /root/cmp/{packet}.tar.gz /root/cmp/JOBS_NEXT.json; "
       f"S=$(date --utc +%Y%m%dT%H%M%SZ); setsid nohup bash /root/cmp/remote_update_and_work_v01.sh {packet} {slots} > /root/main_chain_$S.log 2>&1 < /dev/null & "
       f"sleep 4; tail -3 /root/main_chain_*.log")
r = pv.ssh(name, cmd, timeout=120)
print(r.stdout[-800:], r.stderr[-300:])
(CD / 'pods' / name / f'NEXT_{jobs.stem}.json').write_text(json.dumps(dict(packet=packet, jobs=str(jobs), stdout=r.stdout[-2000:]), indent=1), encoding='utf-8')
