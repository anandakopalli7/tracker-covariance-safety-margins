"""Fetch the small per-pod outputs: B7 detection files (/opt/claude_v13_local/b7/), sealing results (/opt/claude_v13_local/sealing/),
re-simulation identity results if present. Packs them on the pod (tar.gz + SHA-256), downloads, verifies, extracts into
work/CD_capture/pod_outputs/<pod>/. Usage: python -I fetch_small_v13.py POD [POD ...]
"""
import hashlib, json, pathlib, sys, tarfile
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(HERE))
import pods_v13 as pv


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()


for pod in sys.argv[1:]:
    r = pv.ssh(pod, "cd /opt/claude_v13_local && tar czf /root/small_out.tgz b7 sealing $( [ -d /opt/claude_v13_resim/resim_check ] && echo ../claude_v13_resim/resim_check ) 2>/dev/null; sha256sum /root/small_out.tgz | cut -d' ' -f1", timeout=600)
    h = r.stdout.strip().split()[-1]
    dest = CD / 'pod_outputs' / pod; dest.mkdir(parents=True, exist_ok=True)
    loc = dest / 'small_out.tgz'
    r2 = pv.sftp(pod, [f'get /root/small_out.tgz "{loc}"'])
    ok = loc.is_file() and sha(loc) == h
    if ok:
        with tarfile.open(loc, 'r:gz') as t: t.extractall(dest, filter='data')
    nb7 = len(list((dest / 'b7').glob('*/B7_MANIFEST_v13.json'))) if (dest / 'b7').is_dir() else 0
    nseal = len(list((dest / 'sealing').glob('*.json'))) if (dest / 'sealing').is_dir() else 0
    print(json.dumps(dict(pod=pod, sha256_ok=ok, b7_manifests=nb7, sealing_files=nseal)))
