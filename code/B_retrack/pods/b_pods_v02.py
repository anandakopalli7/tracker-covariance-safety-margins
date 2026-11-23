r"""RunPod helper for package B (revision v13): a copy of CD_capture\tools\pods_v13.py (SHA-256 in B's STATUS) adapted for B on
20 Nov 2026 (Claude Opus 5.5): pods named claude-v13b-*, records in B_retrack\pods\, spend rows labelled B, CD's runpodctl.exe used
read-only. Used only to run B's frozen second program (recount_fresh) on Linux (coordinator decision 20 Nov 09:28).
Original docstring: Uses runpodctl (key from ~/.runpod/config.toml; never printed).

Subcommands (python -I pods_v13.py <cmd> ...):
  balance                         print the account balance
  stock                           print GPU stock in EU-RO-1
  list                            list pods (id, name, status, $/h)
  create NAME [--gpu G] [--deadline-h H] [--note TEXT]
                                  create one pod on volume <cloud volume id> in EU-RO-1 with the packet_main_v03 image,
                                  NVIDIA_DRIVER_CAPABILITIES=all, 120 GB disk, port 22; wait for SSH; write
                                  pods/NAME/{pod.json,ssh_config,known_hosts}; arm a local deadline watchdog
                                  (deletes the pod at the deadline); append a row to SPEND_LOG_v13.csv
  delete NAME [--note TEXT]       delete the pod, append a spend-log row, mark pods/NAME/TERMINATED
  ssh NAME CMD...                 run a command over SSH (Windows OpenSSH)
  put NAME LOCAL REMOTE [...]     sftp upload (pairs of LOCAL REMOTE)
  get NAME REMOTE LOCAL           sftp download
Only pods named claude-v13b-* are touched.
"""
import datetime, json, os, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent          # B_retrack\pods
PODS = HERE
SPEND = HERE.parents[1] / 'SPEND_LOG_v13.csv'
RPCTL = str(HERE.parents[1] / 'CD_capture' / 'tools' / 'runpodctl.exe')     # read-only use
SSH = r'C:\Windows\System32\OpenSSH\ssh.exe'
SFTP = r'C:\Windows\System32\OpenSSH\sftp.exe'
KEY = str(pathlib.Path(os.environ['USERPROFILE']) / '.ssh' / 'programme_a_runpod_20261030_ed25519')
IMAGE = 'runpod/pytorch@sha256:2594f25beeef751aeebcc207ba4c45a382ba174655f01e15cbbfad0e2bdb5ef8'
VOLUME = '<cloud volume id>'
DC = 'EU-RO-1'
PREFIX = 'claude-v13b-'


def rp(*args, check=True, timeout=1200):
    env = {k: v for k, v in os.environ.items() if k != 'RUNPOD_API_KEY'}
    r = subprocess.run([RPCTL, *args], capture_output=True, text=True, timeout=timeout, env=env)
    if check and r.returncode != 0:
        raise SystemExit(f'runpodctl {args[0]} {args[1] if len(args) > 1 else ""} failed rc={r.returncode}: {r.stdout[-2000:]} {r.stderr[-2000:]}')
    return r


def balance():
    d = json.loads(rp('user').stdout)
    return float(d['clientBalance']), float(d.get('currentSpendPerHr') or 0)


def est():
    return datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')


def spend_row(action, pod_id, gpu, usd_h, note):
    try: bal, rate = balance()
    except BaseException: bal, rate = float('nan'), float('nan')
    line = f'{est()},B,{action},{pod_id},{gpu},{DC},{usd_h},{bal:.4f},"{note} (account spend now {rate:.3f}/h)"\n'
    with open(SPEND, 'a', encoding='utf-8', newline='') as f:
        f.write(line)
    print('spend log:', line.strip())


def ssh_config(name, ip, port):
    d = PODS / name
    text = (f'Host {name}\n  HostName {ip}\n  Port {port}\n  User root\n  IdentityFile {KEY}\n  IdentitiesOnly yes\n'
            f'  StrictHostKeyChecking accept-new\n  UserKnownHostsFile {d / "known_hosts"}\n  ServerAliveInterval 30\n'
            f'  ServerAliveCountMax 6\n  ConnectTimeout 20\n')
    (d / 'ssh_config').write_text(text, encoding='ascii')


def pod_get(pid):
    # 20 Nov 02:00: a transient RunPod API timeout here left a created pod untracked; retry before giving up
    for attempt in range(6):
        r = rp('pod', 'get', pid, check=False)
        if r.returncode == 0: return json.loads(r.stdout)
        time.sleep(20)
    raise SystemExit(f'runpodctl pod get {pid} failed 6 times: {r.stdout[-300:]} {r.stderr[-300:]}')


def ssh_endpoint(p):
    s = p.get('ssh')
    if isinstance(s, dict) and s.get('ip') and s.get('port'):
        return s['ip'], int(s['port'])
    ip = p.get('publicIp'); port = None
    if isinstance(p.get('ports'), list) and all(isinstance(x, str) for x in p['ports']):
        return ip, None
    ports = p.get('portMappings') or p.get('ports') or {}
    if isinstance(ports, str):
        try: ports = json.loads(ports)
        except Exception: ports = {}
    if isinstance(ports, dict):
        port = ports.get('22') or ports.get(22)
    elif isinstance(ports, list):
        for m in ports:
            if str(m.get('privatePort')) == '22' and m.get('isIpPublic', True):
                port = m.get('publicPort'); ip = m.get('ip') or ip
    ssh = p.get('ssh') or {}
    if isinstance(ssh, dict) and not port:
        ip = ssh.get('ip') or ssh.get('host') or ip; port = ssh.get('port') or port
    return ip, port


def create(name, gpu, deadline_h, note):
    assert name.startswith(PREFIX)
    d = PODS / name
    assert not (d / 'pod.json').exists(), 'pod record exists; use a new name'
    d.mkdir(parents=True, exist_ok=True)
    env = json.dumps({'NVIDIA_DRIVER_CAPABILITIES': 'all'})
    # No --wait: its banner check never saw our pods' SSH (19 Nov); we poll 'pod get' and test SSH ourselves.
    r = rp('pod', 'create', '--name', name, '--image', IMAGE, '--gpu-id', gpu, '--cloud-type', 'SECURE',
           '--container-disk-in-gb', '120', '--network-volume-id', VOLUME, '--data-center-ids', DC,
           '--ports', '22/tcp', '--env', env, check=False, timeout=300)
    (d / 'create_stdout.txt').write_text(r.stdout + '\n--stderr--\n' + r.stderr, encoding='utf-8')
    if r.returncode != 0:
        txt = (r.stdout + r.stderr)
        pid = None
        for tok in txt.replace('"', ' ').split():
            if len(tok) == 14 and tok.isalnum() and tok.islower():
                pid = tok
        print('CREATE FAILED', name, txt[-600:])
        if pid:
            print('a pod id appears in the error; check it with list:', pid)
        raise SystemExit(2)
    p = json.loads(r.stdout)
    adopt(name, p['id'], gpu, deadline_h, note, p)


def adopt(name, pid, gpu, deadline_h, note, p=None):
    """Record a pod (created now or earlier), wait for SSH, arm the watchdog and log the creation."""
    d = PODS / name; d.mkdir(parents=True, exist_ok=True)
    assert not (d / 'pod.json').exists(), 'pod record exists'
    p = p or pod_get(pid); ip, port = ssh_endpoint(p)
    for _ in range(90):
        if ip and port: break
        time.sleep(10); p = pod_get(pid); ip, port = ssh_endpoint(p)
    cost = p.get('costPerHr') or p.get('adjustedCostPerHr')
    deadline = datetime.datetime.now().astimezone() + datetime.timedelta(hours=deadline_h)
    rec = dict(id=pid, name=name, gpu=gpu, costPerHr=cost, ip=ip, port=port, created=datetime.datetime.now().astimezone().isoformat(),
               deadline=deadline.isoformat(), image=IMAGE, volume=VOLUME, dc=DC, raw=p)
    (d / 'pod.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    if ip and port: ssh_config(name, ip, port)
    # Local watchdog: delete this pod at the deadline even if this session stops.
    wd = (f"Start-Sleep -Seconds {int(deadline_h * 3600)}; & '{RPCTL}' pod delete {pid} *>&1 | "
          f"Out-File -Encoding utf8 '{d / 'watchdog_terminate.log'}'")
    subprocess.Popen(['powershell', '-NoProfile', '-WindowStyle', 'Hidden', '-Command', wd],
                     creationflags=0x00000008 | 0x00000200, close_fds=True)
    (d / 'watchdog.txt').write_text(f'watchdog armed: delete {pid} at {deadline.isoformat()}\n', encoding='utf-8')
    print(json.dumps(dict(created=name, id=pid, gpu=gpu, cost=cost, ip=ip, port=port, deadline=deadline.isoformat())))
    spend_row('create', pid, gpu, cost, f'{name}; deadline watchdog {deadline_h} h; {note}')
    ok = False
    for _ in range(60):                       # up to 10 min for sshd
        try:
            r = ssh(name, 'echo ok', timeout=40)
            if r.returncode == 0 and 'ok' in r.stdout: ok = True; break
        except Exception: pass
        time.sleep(10)
    (d / 'SSH_OK' if ok else d / 'SSH_NOT_READY').write_text(est() + '\n', encoding='utf-8')
    print('ssh', 'ready' if ok else 'NOT READY', name)


def delete(name, note):
    assert name.startswith(PREFIX)
    d = PODS / name; rec = json.loads((d / 'pod.json').read_text(encoding='utf-8'))
    import time
    for attempt in range(1, 6):                       # 19 Nov 23:45 fix: rc=1 deletes were logged as terminations (pods 01, 03, 06)
        r = rp('pod', 'delete', rec['id'], check=False)
        print(r.stdout[-500:], r.stderr[-500:])
        if r.returncode == 0: break
        with open(d / 'DELETE_FAILED.log', 'a', encoding='utf-8') as f: f.write(f'{est()} attempt {attempt} rc={r.returncode}\n')
        time.sleep(30)
    else:
        raise SystemExit(f'{name}: pod delete failed 5 times; TERMINATED not written')
    (d / 'TERMINATED').write_text(f'{est()} rc={r.returncode}\n', encoding='utf-8')
    spend_row('terminate', rec['id'], rec['gpu'], rec['costPerHr'], f'{name}; {note}')


def ssh(name, cmd, timeout=600, stdin=None):
    cfg = str(PODS / name / 'ssh_config')
    r = subprocess.run([SSH, '-F', cfg, name, cmd], capture_output=True, text=True, timeout=timeout, input=stdin)
    return r


def sftp(name, lines, timeout=3600):
    cfg = str(PODS / name / 'ssh_config')
    import os, uuid
    batch = PODS / name / f'sftp_batch_{os.getpid()}_{uuid.uuid4().hex[:8]}.txt'
    batch.write_text('\n'.join(lines) + '\n', encoding='ascii')
    return subprocess.run([SFTP, '-F', cfg, '-b', str(batch), name], capture_output=True, text=True, timeout=timeout)


def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return
    c = a[0]
    if c == 'balance': print(balance())
    elif c == 'stock':
        for x in json.loads(rp('datacenter', 'list').stdout):
            if x['id'] == DC: print(x.get('gpuAvailability'))
    elif c == 'list':
        for p in json.loads(rp('pod', 'list').stdout):
            print(p.get('id'), p.get('name'), p.get('desiredStatus'), p.get('costPerHr'), p.get('gpu') or p.get('machine', {}).get('gpuDisplayName'))
    elif c == 'create':
        name = a[1]; gpu = 'NVIDIA GeForce RTX 4090'; dl = 10.0; note = ''
        i = 2
        while i < len(a):
            if a[i] == '--gpu': gpu = a[i + 1]; i += 2
            elif a[i] == '--deadline-h': dl = float(a[i + 1]); i += 2
            elif a[i] == '--note': note = a[i + 1]; i += 2
            else: raise SystemExit('unknown arg ' + a[i])
        create(name, gpu, dl, note)
    elif c == 'adopt':                        # adopt NAME POD_ID GPU DEADLINE_H NOTE
        adopt(a[1], a[2], a[3], float(a[4]), a[5] if len(a) > 5 else '')
    elif c == 'delete':
        note = a[3] if len(a) > 3 and a[2] == '--note' else ''
        delete(a[1], note)
    elif c == 'ssh':
        r = ssh(a[1], ' '.join(a[2:])); print(r.stdout, end=''); print(r.stderr[-3000:], end='', file=sys.stderr); sys.exit(r.returncode)
    elif c == 'put':
        pairs = a[2:]; lines = ['-mkdir /root/cmp']
        for i in range(0, len(pairs), 2): lines.append(f'put "{pairs[i]}" "{pairs[i + 1]}"')
        r = sftp(a[1], lines); print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(r.returncode)
    elif c == 'get':
        r = sftp(a[1], [f'get "{a[2]}" "{a[3]}"']); print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(r.returncode)
    else: raise SystemExit('unknown command')


if __name__ == '__main__':
    main()
