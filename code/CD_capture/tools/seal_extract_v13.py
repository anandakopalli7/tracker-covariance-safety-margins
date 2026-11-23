"""Sealing check (AMENDMENT_10_v13.md sec. 5.2) and logs-only extraction for the fresh C/D runs. Runs on a pod.

For every archive under /workspace/<folder>/results/<run_id>/ whose run id starts with one of the given prefixes:
  1. archive SHA-256 and byte count equal its receipt; receipt status CAPTURED_AND_REVIEWED; frames_dropped == 0; keep_raw true;
  2. kept sweeps: the number of raw/*.npy equals the number of clean/*.npy and the number of noise-receipt lines;
  3. each kept noisy sweep (raw/kkkk.npy): file SHA-256 equals FILE_HASHES.json, and the array hash (range_noise.array_hash)
     equals noisy_sha256 of its noise receipt (line k).
It writes, per run, sealing/<run_id>.json with booleans and counts of failures only, and logs/<run_id>_logs.tar.gz: the
archive without the .npy sweep files (every log, receipt and review file), plus its SHA-256 in sealing/<run_id>.json.
Nothing of a run's outcome is read: frames.jsonl, truth, decisions, SUMMARY outcomes and assessment files are copied
into the logs archive as bytes, never parsed. Printed output: pass/fail counts only.

Usage (pod venv python): python -I seal_extract_v13.py --folder claude_v13_cd_v01 --prefixes pc13_,pd13_ [--workers 8]
"""
import argparse, hashlib, io, json, os, pathlib, sys, tarfile
from concurrent.futures import ProcessPoolExecutor
import numpy as np


def array_hash(array):                       # 149 code/range_noise.py array_hash, verbatim logic
    header = json.dumps({'shape': list(array.shape), 'dtype': array.dtype.str}, sort_keys=True, separators=(',', ':')).encode('ascii')
    return hashlib.sha256(header + b'\n' + array.tobytes(order='C')).hexdigest()


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()


def one(args):
    results, root, rid = args
    d = results / rid; outj = root / 'sealing' / f'{rid}.json'
    if outj.exists(): return json.loads(outj.read_text())
    res = dict(run_id=rid, checks={}, failures={})
    arch = d / f'claude_main_{rid}.tar.gz'; rec = json.loads((d / f'claude_main_{rid}.tar.gz.receipt.json').read_text())
    c = res['checks']
    c['receipt_sha256'] = sha_file(arch) == rec['sha256'] and arch.stat().st_size == rec['bytes']
    c['receipt_status'] = rec['status'] == 'CAPTURED_AND_REVIEWED'
    c['receipt_frames_dropped_zero'] = rec['frames_dropped'] == 0
    c['receipt_keep_raw'] = rec['keep_raw'] is True
    raw_file_sha, raw_arr_sha, clean_n, file_hashes, noise = {}, {}, 0, None, None
    logs_tmp = root / 'logs' / f'{rid}_logs.tar.gz.partial'; logs = root / 'logs' / f'{rid}_logs.tar.gz'
    with tarfile.open(arch, 'r:gz') as tin, tarfile.open(logs_tmp, 'w:gz', compresslevel=6) as tout:
        for m in tin:
            parts = m.name.split('/')
            is_frame = m.isfile() and m.name.endswith('.npy') and len(parts) >= 2 and parts[-2] in ('raw', 'clean')
            if not m.isfile():
                continue
            data = tin.extractfile(m).read()
            if is_frame:
                if parts[-2] == 'clean': clean_n += 1
                else:
                    k = int(parts[-1][:-4]); raw_file_sha[k] = hashlib.sha256(data).hexdigest()
                    raw_arr_sha[k] = array_hash(np.load(io.BytesIO(data), allow_pickle=False))
                continue
            if parts[-1] == 'FILE_HASHES.json' and len(parts) == 2: file_hashes = json.loads(data)
            if parts[-1] == 'noise_receipts.jsonl' and len(parts) >= 3 and parts[1] == 'capture':
                noise = [json.loads(l)['noisy_sha256'] for l in data.decode().splitlines() if l.strip()]
            tout.addfile(m, io.BytesIO(data))
    n = len(raw_file_sha)
    c['sweeps_present'] = n > 0
    c['sweep_counts_consistent'] = noise is not None and n == clean_n == len(noise) and sorted(raw_file_sha) == list(range(n))
    fh = {}
    if file_hashes:
        for f in file_hashes['files']:
            p = f['path'].split('/')
            if len(p) == 2 and p[0] == 'raw' and p[1].endswith('.npy'): fh[int(p[1][:-4])] = f['sha256']
    bad_file = [k for k in raw_file_sha if fh.get(k) != raw_file_sha[k]]
    bad_noise = [k for k in raw_arr_sha if noise is None or k >= len(noise) or noise[k] != raw_arr_sha[k]]
    c['noisy_sweep_file_sha256_equals_file_hashes'] = not bad_file and len(fh) == n
    c['noisy_sweep_array_hash_equals_noise_receipt'] = not bad_noise
    res['failures'] = dict(file_sha=len(bad_file), noise_receipt=len(bad_noise))
    os.replace(logs_tmp, logs)
    res['logs_archive'] = logs.name; res['logs_sha256'] = sha_file(logs); res['logs_bytes'] = logs.stat().st_size
    res['archive_sha256'] = rec['sha256']; res['pass'] = all(c.values())
    tmp = outj.with_suffix('.partial'); tmp.write_text(json.dumps(res, indent=1)); os.replace(tmp, outj)
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--folder', default='claude_v13_cd_v01'); ap.add_argument('--prefixes', default='pc13_,pd13_')
    ap.add_argument('--workers', type=int, default=8); ap.add_argument('--only', default='')
    ap.add_argument('--results', default=''); ap.add_argument('--out', default='')   # test overrides
    a = ap.parse_args(); root = pathlib.Path(a.out) if a.out else pathlib.Path('/workspace') / a.folder
    results = pathlib.Path(a.results) if a.results else root / 'results'
    (root / 'sealing').mkdir(exist_ok=True); (root / 'logs').mkdir(exist_ok=True)
    pre = tuple(a.prefixes.split(','))
    rids = sorted(p.name for p in results.iterdir() if p.is_dir() and p.name.startswith(pre)
                  and (p / f'claude_main_{p.name}.tar.gz.receipt.json').is_file())
    if a.only: rids = [r for r in rids if r in set(a.only.split(','))]
    with ProcessPoolExecutor(a.workers) as ex:
        out = list(ex.map(one, [(results, root, r) for r in rids]))
    agg = {}
    for r in out:
        for k, v in r['checks'].items(): agg.setdefault(k, [0, 0])[0 if v else 1] += 1
    print(json.dumps(dict(archives=len(out), passed=sum(r['pass'] for r in out), failed=[r['run_id'] for r in out if not r['pass']],
                          checks_pass_fail=agg), indent=1))


if __name__ == '__main__':
    main()
