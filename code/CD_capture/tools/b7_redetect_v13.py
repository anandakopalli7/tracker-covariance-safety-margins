"""B7 pod part (AMENDMENT_10_v13.md sec. 3, B7 (i)-(ii)): offline CenterPoint re-detection on a fresh run's kept noisy sweeps.

The online capture (probe_arms_v01.py) pushes each frame's noisy sweep into a SweepBuffer (10 sweeps) and detects at
k >= 19, k % 10 == 9 (2 Hz) on buffer.combined(reference_world(ego T, reference sensor), 1,
keyed_seed('integration', case seed, 'lidar', 'driving_binding92:' + str(k))). This script replays that with the same
code (sensor_adapter, CenterPointBackend, detector_to_world from the staged workspace) at EVERY odd k >= 19, which covers
  2 Hz  : k = 19, 29, 39, ...           (the online ticks; B7 (i) identity is checked after Lock 2, not here)
  5 Hz  : k = 19, 23, 27, ...           (every 4th frame from 19)
  10 Hz : k = 19, 21, 23, ...           (every 2nd frame)
because the combined cloud at tick k depends only on k (last ten sweeps, keyed seed of k). Each output row is tagged with
the rates it belongs to. Sweeps are pushed for every saved frame (also after an online policy failure or at the contact
frame, where the online loop stopped detecting); the row records whether the online loop detected at that tick.
Nothing else is computed: no tracking, no comparison, no score (A10 sec. 5.2). Output per run:
  <out-root>/b7/<run_id>/b7_detections_v13.jsonl and B7_MANIFEST_v13.json (input/code hashes; never overwritten); archives are
  read from /workspace/<src-folder or folder>/results/<run_id>/ (an absolute folder path overrides /workspace).

Run on a bootstrapped pod with the capture environment:
  bash run_with_container_env_v01.sh /opt/programme_a_gpu750/.venv/bin/python -B b7_redetect_v13.py --runs RID[,RID...] [--folder claude_v13_cd_v01]
"""
import argparse, hashlib, io, json, os, pathlib, sys, tarfile, time
os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'; os.environ['OPENBLAS_CORETYPE'] = 'HASWELL'
for _k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'): os.environ[_k] = '1'
os.environ.pop('RUNPOD_API_KEY', None)
import numpy as np
import torch

ROOT = pathlib.Path('/opt/programme_a_gpu750/workspace')
P = ROOT / '149_supported_sensor_preparation_20261101'
MODEL = ROOT / '410_fixed_kernel_sensor_qualification_20261102/package'
sys.path[:0] = [str(P / 'code'), str(P / 'sources'), str(P / 'vendor'), str(P / 'vendor/CANMOT/src'), str(P / 'legacy86/vendor/nuscenes-devkit/python-sdk')]
from sensor_adapter import Sweep, SweepBuffer, reference_world, keyed_seed      # noqa: E402
from online_tracker import detector_to_world                                     # noqa: E402


def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p): return sha_bytes(pathlib.Path(p).read_bytes())


def load_model():
    torch.cuda.init(); assert torch.cuda.is_initialized()
    import importlib.util
    sys.path.insert(0, str(MODEL / 'code'))
    spec = importlib.util.spec_from_file_location('programme_a733_fixed_backend', MODEL / 'code/centerpoint_backend.py')
    backend = importlib.util.module_from_spec(spec); spec.loader.exec_module(backend)
    lock = json.loads((MODEL / 'legacy86/40_remote/input_lock.json').read_text())
    model = backend.CenterPointBackend(MODEL / 'legacy86/vendor/CenterPoint', MODEL / 'legacy86/weights/epoch_20.pth', lock['checkpoint_sha256'])
    return model, lock['checkpoint_sha256']


def read_inputs(archive):
    """Noisy sweeps, raw observations and the contract from the run archive (local extraction into memory)."""
    sweeps, raw_obs, contract, online_ks = {}, None, None, None
    with tarfile.open(archive, 'r:gz') as t:
        for m in t:
            if not m.isfile(): continue
            parts = m.name.split('/')
            if len(parts) < 4 or parts[1] != 'capture': continue
            name = '/'.join(parts[3:])
            if len(parts) == 5 and parts[3] == 'raw' and parts[4].endswith('.npy'):
                sweeps[int(parts[4][:-4])] = np.load(io.BytesIO(t.extractfile(m).read()), allow_pickle=False)
            elif name == 'raw_observations.jsonl':
                raw_obs = [json.loads(l) for l in t.extractfile(m).read().decode().splitlines() if l.strip()]
            elif name == 'contract.json':
                contract = json.loads(t.extractfile(m).read())
            elif name == 'detections.jsonl':
                online_ks = [json.loads(l)['k'] for l in t.extractfile(m).read().decode().splitlines() if l.strip()]
    return sweeps, raw_obs, contract, online_ks


def run_one(model, ckpt, folder, rid, src=None):
    res = (src or folder) / 'results' / rid; out = folder / 'b7' / rid
    done = out / 'B7_MANIFEST_v13.json'
    if done.exists(): return 'skip'
    out.mkdir(parents=True, exist_ok=True)
    arch = res / f'claude_main_{rid}.tar.gz'
    t0 = time.time()
    sweeps, raw_obs, contract, online_ks = read_inputs(arch)
    case = contract['case']; seed = case['seed']
    ref_sensor = np.eye(4); ref_sensor[:3, :3] = [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]; ref_sensor[:3, 3] = [1, 0, 2]   # probe_arms_v01.py L181
    buf = SweepBuffer(); rows = 0; online = set(online_ks or [])
    tmp = out / 'b7_detections_v13.jsonl.partial'
    with open(tmp, 'w') as f:
        for r in raw_obs:
            k = r['k']
            if k not in sweeps: break                      # frames after the last saved sweep are not observable
            buf.push(Sweep(r['frame'], float(r['time']), sweeps[k], np.asarray(r['sensor_world'])))
            if k >= 19 and k % 2 == 1:
                sref = reference_world(np.asarray(r['state']['world']), ref_sensor)
                cloud = buf.combined(sref, 1, keyed_seed('integration', seed, 'lidar', 'driving_binding92:' + str(k)))
                pred = model.predict(cloud, 'binding_' + str(k))
                mrows = detector_to_world(pred, sref)
                rates = [hz for hz, ok in ((2, k % 10 == 9), (5, (k - 19) % 4 == 0), (10, True)) if ok]
                f.write(json.dumps(dict(k=k, frame=r['frame'], time=r['time'], rates_hz=rates, online_tick=k in online,
                                        model=mrows, combined_hash=sha_bytes(cloud.tobytes()), inference_s=pred['inference_s']), allow_nan=False) + '\n')
                rows += 1
    os.replace(tmp, out / 'b7_detections_v13.jsonl')
    man = dict(schema='B7_REDETECT_V13', run_id=rid, archive=arch.name, archive_sha256=sha_file(arch), rows=rows, sweeps=len(sweeps),
               case=case['id'], seed=seed, checkpoint_sha256=ckpt, script_sha256=sha_file(__file__),
               sensor_adapter_sha256=sha_file(P / 'code/sensor_adapter.py'), online_tracker_sha256=sha_file(P / 'code/online_tracker.py'),
               backend_sha256=sha_file(MODEL / 'code/centerpoint_backend.py'), output_sha256=sha_file(out / 'b7_detections_v13.jsonl'),
               gpu=torch.cuda.get_device_name(0), pod_id=os.environ.get('RUNPOD_POD_ID'), seconds=time.time() - t0,
               utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    with open(done, 'x') as f: json.dump(man, f, indent=1)
    return 'ok'


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--runs', required=True); ap.add_argument('--folder', default='claude_v13_cd_v01')
    ap.add_argument('--src-folder', default='', help='read archives from /workspace/<this>/results (e.g. claude_main_v01 for run 0037); outputs always go to --folder')
    ap.add_argument('--out-root', default='/opt/claude_v13_local', help='outputs go to <out-root>/b7/<run_id> (pod-local disk; the volume is full)')
    a = ap.parse_args(); folder = pathlib.Path(a.out_root)
    src = pathlib.Path('/workspace') / a.src_folder if a.src_folder else pathlib.Path('/workspace') / a.folder   # absolute paths override /workspace
    rids = [x for x in a.runs.split(',') if x]
    model, ckpt = load_model()
    counts = {}
    for rid in rids:
        try: s = run_one(model, ckpt, folder, rid, src)
        except Exception as e:
            s = 'error'; (folder / 'b7').mkdir(exist_ok=True)
            (folder / 'b7' / f'{rid}.ERROR.txt').write_text(f'{type(e).__name__}: {e}\n')
        counts[s] = counts.get(s, 0) + 1
        print(json.dumps(dict(run=rid, status=s)), flush=True)
    print(json.dumps(dict(done=counts)), flush=True)


if __name__ == '__main__':
    main()
