"""Crossing sprint (A11): keep the frozen extractor running on the capture pods as runs land (orchestration only; no value computed or
read here). New file, 21 Nov 2026 (Claude Opus 5.5, session CD). Every SLEEP seconds, for each pod: if its capture worker is no longer
RUNNING, or the pod is an RTX 4090 pod (spare cores), and no x_extract process runs there, upload the lock once (x_pods lock) and start
x_pods run on the CAPTURED_AND_REVIEWED archives (finished arrays are skipped). Stops when every pod's capture is finished and all its
receipted runs have arrays, or after HOURS.
Usage: python -I -B x_extract_loop_v13.py POD,POD,... [--hours 4] [--sleep 300] [--workers-4090 4] [--workers-l4 4]
"""
import json, pathlib, sys, time, datetime
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path[:0] = [str(HERE), str(CD / 'tools')]
import x_pods_v13 as XP                  # noqa: E402
import pods_v13 as pv                    # noqa: E402

ARGS = sys.argv[1:]; PODS = ARGS[0].split(',')
opt = lambda n, d: type(d)(ARGS[ARGS.index(n) + 1]) if n in ARGS else d
HOURS, SLEEP = opt('--hours', 4.0), opt('--sleep', 300)
W4090, WL4 = opt('--workers-4090', 4), opt('--workers-l4', 4)
LOG = CD / 'pods' / 'x_extract_loop.log'


def log(m):
    line = f'{datetime.datetime.now():%H:%M:%S} {m}'; print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f: f.write(line + '\n')


def probe(name):
    cmd = ("python3 -c \"import json;print(json.load(open('/opt/claude_main/worker_status.json')).get('status'))\"; "
           "ls %s/pc13x_*/*.receipt.json 2>/dev/null | xargs -r grep -l CAPTURED_AND_REVIEWED | wc -l; "
           "ls %s/CV0/*.npz 2>/dev/null | grep -vc partial; pgrep -f '[x]_extract_v13.py --archive-root' | wc -l" % (XP.RESULTS, XP.OUTR))
    r = pv.ssh(name, cmd, timeout=120)
    if r.returncode != 0: return None
    lines = r.stdout.strip().splitlines()
    return dict(status=lines[-4].strip(), receipts=int(lines[-3]), arrays=int(lines[-2]), running=int(lines[-1]))


def main():
    until = time.time() + HOURS * 3600
    gpu = {n: json.loads((CD / 'pods' / n / 'pod.json').read_text(encoding='utf-8')).get('gpu', '') for n in PODS}
    while time.time() < until:
        done = 0
        for n in PODS:
            try:
                p = probe(n)
                if p is None: log(f'{n} probe failed'); continue
                big = '4090' in gpu[n]
                log(f'{n} {gpu[n][-8:]} capture={p["status"]} receipts={p["receipts"]} arrays={p["arrays"]} extracting={p["running"]}')
                if p['status'] != 'RUNNING' and p['receipts'] == p['arrays'] and p['running'] == 0:
                    done += 1; continue
                if p['running'] == 0 and p['receipts'] > p['arrays'] and (big or p['status'] != 'RUNNING'):
                    if not (CD / 'pods' / n / 'X_LOCK.json').is_file(): XP.lock(n)
                    XP.run(n, W4090 if big else WL4); log(f'{n} extraction started')
            except SystemExit as e:
                log(f'{n} error: {str(e)[:300]}')
            except Exception as e:
                log(f'{n} error {type(e).__name__}: {str(e)[:300]}')
        if done == len(PODS): log('all pods: capture finished and every receipted run extracted'); return
        time.sleep(SLEEP)
    log('loop end (time limit)')


if __name__ == '__main__':
    main()
