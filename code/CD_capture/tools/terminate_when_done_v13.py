"""Terminate each listed pod once everything on it is safe on the laptop: every run folder with a receipt under
/opt/claude_v13_local/results and /opt/claude_v13_resim/results has archives/<rid>/DOWNLOAD_OK.json locally, the B7/sealing outputs
were fetched (pod_outputs/<pod>/small_out.tgz exists), and no worker or b7 process runs. Checks every 5 minutes; logs to
pods/terminate.log; each deletion writes a spend-log row (pods_v13.delete). Usage: python -I terminate_when_done_v13.py POD [POD ...]
"""
import datetime, json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(HERE))
import pods_v13 as pv

LOG = CD / 'pods' / 'terminate.log'


def log(m):
    line = f'{datetime.datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z} {m}'
    print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f: f.write(line + '\n')


def remote_rids(pod):
    cmd = ("for R in /opt/claude_v13_local/results /opt/claude_v13_resim/results; do [ -d $R ] && for d in $R/*/; do d=${d%/}; "
           "ls $d/*.receipt.json >/dev/null 2>&1 && basename $d; done; done; echo BUSY=$(pgrep -fc '[w]orker_main_v01.py|[b]7_redetect')")
    r = pv.ssh(pod, cmd, timeout=300)
    lines = r.stdout.split()
    busy = next((l for l in lines if l.startswith('BUSY=')), 'BUSY=?')
    return [l for l in lines if not l.startswith('BUSY=')], busy, r.returncode


pods = sys.argv[1:]
while pods:
    for pod in list(pods):
        try:
            rids, busy, rc = remote_rids(pod)
        except Exception as e:
            log(f'{pod}: check failed {type(e).__name__}'); continue
        if rc != 0 or busy != 'BUSY=0' or not rids:
            log(f'{pod}: not yet ({busy}, {len(rids)} runs listed)'); continue
        missing = [r for r in rids if not (CD / 'archives' / r / 'DOWNLOAD_OK.json').is_file()]
        fetched = (CD / 'pod_outputs' / pod / 'small_out.tgz').is_file()
        if missing or not fetched:
            log(f'{pod}: {len(missing)} of {len(rids)} archives not yet verified locally; small outputs fetched: {fetched}'); continue
        log(f'{pod}: all {len(rids)} archives verified locally; terminating')
        pv.delete(pod, f'all {len(rids)} archives verified on the laptop; B7 and sealing outputs fetched')
        pods.remove(pod)
    if pods: time.sleep(300)
log('terminator done')
