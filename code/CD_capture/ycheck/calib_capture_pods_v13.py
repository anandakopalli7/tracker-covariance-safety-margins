"""A10 sec. 2.6 calibration chunks on pods that already exist (e.g. the X capture pods' spare cores), with the frozen worker
tools\\calib_worker_v13.sh and the frozen runners (analysis\\calib_remote_v13.py; ycheck\\y_calib_remote_v13.py; the recount's runners).
Orchestration only: it moves files and task lines; every number comes from the frozen runners; tools\\calib_merge_v13.py joins the chunks.
New file, 21 Nov 2026 (Claude Opus 5.5, session CD). Workers run at nice 19 so capture keeps priority (coordinator, 14:43).
Usage (.venv\\Scripts\\python.exe -I -B -X utf8 ycheck\\calib_capture_pods_v13.py CMD ...):
  prep POD N JOBFILES...        create /opt/calib (todo, jobs, ...), PY=/opt/b7py/bin/python, upload the runners + gl_fast + the job files
                                (.job.npz and .meta.json), start N workers at nice 19
  tasks POD LABEL SEED LO HI CHUNK RUNNER   queue tasks "LABEL SEED lo hi RUNNER" for lo = LO, LO+CHUNK, ... < HI
  status POD                    counts of todo / running / done / failed
  fetch POD DEST                download every finished chunk file (*_o*_*.npz) not yet in DEST, SHA-256 checked
  stop POD                      kill the workers (pkill -f calib_worker)
"""
import hashlib, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(CD / 'tools'))
import pods_v13 as pv                    # noqa: E402

CODE = [CD / 'analysis' / 'calib_remote_v13.py', CD / 'analysis' / 'gl_fast_v13.py', HERE / 'y_calib_remote_v13.py',
        CD / 'recount' / 'rc_kern_v13.py', CD / 'recount' / 'rc_calib_remote_v13.py', CD / 'recount' / 'rc_y_kern_v13.py',
        CD / 'recount' / 'rc_y_calib_remote_v13.py', CD / 'recount' / 'rc_x_kern_v13.py', CD / 'recount' / 'rc_x_calib_remote_v13.py',
        pathlib.Path(r'<library folder>\optA_lib_v02.py')]
WORKER = CD / 'tools' / 'calib_worker_v13.sh'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def ssh(pod, cmd, timeout=600):
    r = pv.ssh(pod, cmd, timeout=timeout)
    if r.returncode != 0: raise SystemExit('%s: %s -> rc=%d %s' % (pod, cmd[:120], r.returncode, (r.stdout + r.stderr)[-600:]))
    return r.stdout


def put(pod, files, remote_dir):
    r = pv.sftp(pod, ['put "%s" "%s/%s"' % (f, remote_dir, pathlib.Path(f).name) for f in files])
    if r.returncode != 0: raise SystemExit('%s: upload failed: %s' % (pod, r.stderr[-500:]))
    got = ssh(pod, 'cd %s && sha256sum %s' % (remote_dir, ' '.join(pathlib.Path(f).name for f in files)))
    have = {l.split()[1]: l.split()[0] for l in got.strip().splitlines()}
    bad = [pathlib.Path(f).name for f in files if have.get(pathlib.Path(f).name) != sha(f)]
    if bad: raise SystemExit('%s: uploaded files differ: %s' % (pod, bad))


def prep(pod, n, jobfiles):
    ssh(pod, 'mkdir -p /opt/calib/jobs /opt/calib/todo /opt/calib/running /opt/calib/done /opt/calib/failed /opt/calib/stolen /opt/calib/logs '
             '&& echo /opt/b7py/bin/python > /opt/calib/PY')
    put(pod, [str(p) for p in CODE if p.is_file()] + list(jobfiles), '/opt/calib/jobs')
    put(pod, [str(WORKER)], '/opt/calib')
    print(ssh(pod, "sed -i 's/\\r$//' /opt/calib/calib_worker_v13.sh; cd /opt/calib && (setsid nohup nice -n 19 bash calib_worker_v13.sh %d > /opt/calib/workers.log 2>&1 < /dev/null &) ; "
                   'sleep 2; cat /opt/calib/workers.log' % int(n)).strip())


def tasks(pod, label, seed, lo, hi, chunk, runner):
    lines = []
    for a in range(int(lo), int(hi), int(chunk)):
        b = min(a + int(chunk), int(hi))
        lines.append("printf '%s %s %d %d %s\\n' > /opt/calib/todo/%s__%s__%04d_%04d.task" % (label, seed, a, b, runner, label, seed, a, b))
    for i in range(0, len(lines), 40):
        ssh(pod, ' && '.join(lines[i:i + 40]))
    print(pod, 'queued', len(lines), 'tasks', label, seed, lo, hi)


def status(pod):
    print(pod, ssh(pod, 'cd /opt/calib && echo todo=$(ls todo | wc -l) running=$(ls running | wc -l) done=$(ls done | wc -l) failed=$(ls failed | wc -l) '
                        "workers=$(pgrep -fc '[c]alib_worker_v13.sh') load=$(cut -d' ' -f1 /proc/loadavg)").strip())


def fetch(pod, dest):
    dest = pathlib.Path(dest); dest.mkdir(parents=True, exist_ok=True)
    lst = ssh(pod, 'cd /opt/calib/jobs && for f in *_o*_*.npz; do [ -f "$f" ] && sha256sum "$f"; done; true').strip().splitlines()
    want = [(l.split()[1], l.split()[0]) for l in lst if l.strip() and not (dest / l.split()[1]).exists()]
    for i in range(0, len(want), 50):
        r = pv.sftp(pod, ['get "/opt/calib/jobs/%s" "%s"' % (f, dest / f) for f, _ in want[i:i + 50]])
        if r.returncode != 0: raise SystemExit('%s: download failed: %s' % (pod, r.stderr[-500:]))
    bad = [f for f, h in want if sha(dest / f) != h]
    if bad:
        for f in bad: (dest / f).unlink()
        raise SystemExit('%s: %d chunk files differ after download (removed): %s' % (pod, len(bad), bad[:3]))
    print(pod, 'fetched', len(want), 'chunk files into', dest)


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'prep': prep(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif c == 'tasks': tasks(*sys.argv[2:9])
    elif c == 'status': status(sys.argv[2])
    elif c == 'fetch': fetch(sys.argv[2], sys.argv[3])
    elif c == 'stop': print(ssh(sys.argv[2], "pkill -f '[c]alib_worker_v13.sh'; pkill -f '[c]alib_remote'; echo stopped"))
    else: raise SystemExit(__doc__)
