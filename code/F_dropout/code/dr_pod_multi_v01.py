"""Revision v13, AMENDMENT_12 sec. 3a: create ONE RunPod pod with several GPUs (for its larger CPU quota; the recount's double bootstrap
is CPU-bound and cannot be split over pods). New file, 22 Nov 2026 (Claude Opus 5.5, session F). Same arguments as
F_nuscenes\\code\\fpods_v01.create (image, volume, data centre, 40 GB disk, SSH port; spend log and watchdog record through
fpods_v01.adopt) plus --gpu-count. fpods_v01.py itself is not edited. Moves no data and computes no value.
Usage: python -I -B dr_pod_multi_v01.py NAME COUNT [--gpu "NVIDIA GeForce RTX 4090"] [--deadline-h H]
"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'F_nuscenes' / 'code'))
import fpods_v01 as pv                                  # noqa: E402


def main():
    name, count = sys.argv[1], int(sys.argv[2])
    gpu = sys.argv[sys.argv.index('--gpu') + 1] if '--gpu' in sys.argv else 'NVIDIA GeForce RTX 4090'
    dl = float(sys.argv[sys.argv.index('--deadline-h') + 1]) if '--deadline-h' in sys.argv else 3.0
    assert name.startswith(pv.PREFIX) and 1 <= count <= 8
    d = pv.PODS / name
    assert not (d / 'pod.json').exists(), 'pod record exists; use a new name'
    d.mkdir(parents=True, exist_ok=True)
    env = json.dumps({'NVIDIA_DRIVER_CAPABILITIES': 'all'})
    r = pv.rp('pod', 'create', '--name', name, '--image', pv.IMAGE, '--gpu-id', gpu, '--gpu-count', str(count), '--cloud-type', 'SECURE',
              '--container-disk-in-gb', '40', '--network-volume-id', pv.VOLUME, '--data-center-ids', pv.DC,
              '--ports', '22/tcp', '--env', env, check=False, timeout=300)
    (d / 'create_stdout.txt').write_text(r.stdout + '\n--stderr--\n' + r.stderr, encoding='utf-8')
    if r.returncode != 0:
        print('CREATE FAILED', name, (r.stdout + r.stderr)[-600:]); raise SystemExit(2)
    p = json.loads(r.stdout)
    pv.adopt(name, p['id'], '%s x%d' % (gpu, count), dl, 'AMENDMENT_12 sec. 3a DR recount (CPU quota of %d GPUs)' % count, p)


if __name__ == '__main__':
    main()
