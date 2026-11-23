"""Package F (revision v13): moves F's double-bootstrap jobs to a RunPod pod and back (no numerics here; the statistic code is
f16_calib_remote_v01.py with f06k_kernel_v01.py, both uploaded unchanged and SHA-256 checked). New file, 20 Nov 2026 (Claude Opus
5.5), at the coordinator's request (01:25 EST). Pods via fpods_v01 (copy of CD's helper: spend-log rows, local deadline watchdog).
On the pod: /opt/fcal/{code,jobs,out,logs}; Python 3.12 venv /opt/fv with numpy and numba pinned to F's laptop venv.
  up NAME [--deadline-h H]          create the pod (RTX 4090 image of CD), set up the venv, upload the code (hash-checked)
  push NAME JOBDIR JOB              upload JOB.job.npz and JOB.meta.json (hash-checked)
  run NAME JOB [remote options]     start f16_calib_remote_v01.py on the pod in the background (log /opt/fcal/logs/JOB.log)
  status NAME [JOB]                 log tail and output list
  fetch NAME JOB DEST               download every output file of JOB, SHA-256 checked against the pod's sha256sum
  down NAME NOTE                    delete the pod (spend-log row)
Usage: python -I f17_calib_pod_v01.py <cmd> ...
"""
import hashlib, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fpods_v01 as pv           # noqa: E402

GPU = 'NVIDIA GeForce RTX 4090'
CODE = [HERE / 'f16_calib_remote_v01.py', HERE / 'f06k_kernel_v01.py']
PINS = 'numpy==2.5.5 numba==0.68.1'          # = work\F_nuscenes\venv (numba 0.68.1, numpy 2.5.5)
R = '/opt/fcal'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def ssh(name, cmd, timeout=600):
    r = pv.ssh(name, cmd, timeout=timeout)
    if r.returncode != 0:
        raise SystemExit(f'{name}: ssh rc={r.returncode}: {r.stderr[-600:]} {r.stdout[-600:]}')
    return r.stdout


def put_checked(name, files, remote_dir):
    r = pv.sftp(name, [f'put "{f}" "{remote_dir}/{pathlib.Path(f).name}"' for f in files])
    if r.returncode != 0:
        raise SystemExit(f'{name}: upload failed {r.stderr[-400:]}')
    got = {pathlib.PurePosixPath(l.split()[1]).name: l.split()[0]
           for l in ssh(name, f'cd {remote_dir} && sha256sum ' + ' '.join(pathlib.Path(f).name for f in files)).splitlines() if l.strip()}
    bad = [pathlib.Path(f).name for f in files if got.get(pathlib.Path(f).name) != sha(f)]
    if bad:
        raise SystemExit(f'{name}: uploaded files differ: {bad}')
    print(name, 'uploaded and checked:', [pathlib.Path(f).name for f in files])


def up(name, deadline_h, gpu=GPU, note='package F double bootstrap (A10 sec. 2.6)'):
    if not (pv.PODS / name / 'pod.json').is_file():
        pv.create(name, gpu, deadline_h, note)
    setup = (f'mkdir -p {R}/code {R}/jobs {R}/out {R}/logs && cd {R} && '
             f'( python3 -m pip install -q uv && uv venv -q --clear -p 3.12 /opt/fv && uv pip install -q --python /opt/fv/bin/python {PINS} ) '
             '> setup.log 2>&1; /opt/fv/bin/python -c "import sys, numpy, numba; print(sys.version.split()[0], numpy.__version__, numba.__version__)"; nproc')
    print(name, 'python numpy numba / nproc:', ssh(name, setup, timeout=1800).strip().replace('\n', ' / '))
    put_checked(name, CODE, f'{R}/code')
    (pv.PODS / name / 'FCAL_UP').write_text(json.dumps({f.name: sha(f) for f in CODE}), encoding='utf-8')


def push(name, jobdir, job):
    jd = pathlib.Path(jobdir)
    put_checked(name, [jd / f'{job}.job.npz', jd / f'{job}.meta.json'], f'{R}/jobs')


def run(name, job, opts):
    cmd = (f'cd {R} && setsid nohup /opt/fv/bin/python code/f16_calib_remote_v01.py jobs {job} --out out {" ".join(opts)} '
           f'> logs/{job}.log 2>&1 < /dev/null & sleep 3; cat {R}/logs/{job}.log')
    print(ssh(name, cmd))


def status(name, job=None):
    tail = f'tail -n 5 {R}/logs/{job}.log; ' if job else f'tail -n 3 {R}/logs/*.log; '
    print(ssh(name, tail + f'ls -la {R}/out; uptime'))


def fetch(name, job, dest):
    dest = pathlib.Path(dest); dest.mkdir(parents=True, exist_ok=True)
    lines = [l for l in ssh(name, f'cd {R}/out && sha256sum {job}_*.npz').splitlines() if l.strip()]
    sums = {l.split()[1]: l.split()[0] for l in lines}
    r = pv.sftp(name, [f'get "{R}/out/{f}" "{dest / f}"' for f in sums])
    if r.returncode != 0:
        raise SystemExit(f'{name}: download failed {r.stderr[-400:]}')
    bad = [f for f, s in sums.items() if sha(dest / f) != s]
    if bad:
        raise SystemExit(f'{name}: downloaded files differ: {bad}')
    print(name, 'fetched and checked:', sorted(sums))


def main():
    a = sys.argv[1:]
    c = a[0]
    if c == 'up':
        up(a[1], float(a[a.index('--deadline-h') + 1]) if '--deadline-h' in a else 3.0, a[a.index('--gpu') + 1] if '--gpu' in a else GPU)
    elif c == 'push':
        push(a[1], a[2], a[3])
    elif c == 'run':
        run(a[1], a[2], a[3:])
    elif c == 'status':
        status(a[1], a[2] if len(a) > 2 else None)
    elif c == 'fetch':
        fetch(a[1], a[2], a[3])
    elif c == 'down':
        pv.delete(a[1], a[2] if len(a) > 2 else '')
    else:
        raise SystemExit('unknown command')


if __name__ == '__main__':
    main()
