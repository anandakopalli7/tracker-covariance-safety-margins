"""Download package E's run archives from the volume (S3 API, read only), verify each against its receipt, keep the logs the
analyses need, delete the tarball. Secrets are read by work\\shared\\tools\\rp_s3.py and never printed.

python -I fetch_e_v01.py <run-id prefix> [<prefix> ...] [--threads 8] [--summaries-only] [--list]
  Remote: /workspace/claude_v13_e_v01/results/<run_id>/{claude_main_<run_id>.tar.gz, .receipt.json, SUMMARY.json}
  Local:  work\\E_closedloop\\runs\\<run_id>\\ with SUMMARY.json, RECEIPT.json, FETCH_OK.json and x\\<run_id>\\... (kept members)
Kept members: everything except capture\\<case>\\inventory\\, capture\\<case>\\ordered_capture\\, raw\\/clean\\ frames, gpu samples
(the archive's SHA-256 is verified first and recorded, so the full archive stays identifiable on the volume).
--summaries-only: SUMMARY.json only (status, outcome bookkeeping for counts; no truth logs).
"""
import argparse, concurrent.futures as cf, hashlib, io, json, pathlib, sys, tarfile, time

E = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(E.parent / 'shared' / 'tools'))
from rp_s3 import client   # noqa: E402

ROOT = 'claude_v13_e_v01/results/'
RUNS = E / 'runs'
SKIP_PARTS = ('inventory', 'ordered_capture', 'raw', 'clean', 'review_copy')
SKIP_FILES = ('gpu_samples.jsonl', 'scenario_frames.jsonl', 'raw_observations.jsonl', 'noise_receipts.jsonl', 'batch_receipts.jsonl',
              'canonical_field_receipts.jsonl', 'filter_algebra.jsonl', 'filter_target_covariances.jsonl', 'imm_filter_algebra.jsonl',
              'actor_review_copy.json')
MIN_FREE_GB = 65          # coordination rule: keep at least 60 GB free on C:


def keep(name):
    """Kept: truth, frames, contacts, outcomes, method/context/E records, detections, filter events, IMM events/modes, the run's
    SUMMARY/JOB/review/actor-review records. Dropped (still in the verified archive on the volume): sweeps, inventories, ordered
    capture, scenario frames, raw observations, receipts of noise/batches/fields, filter algebra, target covariances, copies."""
    parts = pathlib.PurePosixPath(name).parts
    if any(p in SKIP_PARTS for p in parts[1:]):
        return False
    return parts[-1] not in SKIP_FILES


def list_runs(s3, bucket, prefixes):
    """RunPod's S3 returns folder prefixes only for a prefix that ends in '/', so the results folder is listed whole and
    filtered here."""
    out = []; tok = None
    while True:
        kw = dict(Bucket=bucket, Prefix=ROOT, Delimiter='/', MaxKeys=1000)
        if tok: kw['ContinuationToken'] = tok
        r = s3.list_objects_v2(**kw)
        out += [p['Prefix'][len(ROOT):].rstrip('/') for p in r.get('CommonPrefixes', [])]
        if not r.get('IsTruncated'): break
        tok = r['NextContinuationToken']
    return sorted(n for n in set(out) if any(n.startswith(pre) for pre in prefixes))


def fetch(s3, bucket, rid, summaries_only):
    d = RUNS / rid
    if (d / 'FETCH_OK.json').exists() or (summaries_only and (d / 'SUMMARY.json').exists()):
        return rid, 'present'
    d.mkdir(parents=True, exist_ok=True)
    summ = s3.get_object(Bucket=bucket, Key=f'{ROOT}{rid}/SUMMARY.json')['Body'].read()
    (d / 'SUMMARY.json').write_bytes(summ)
    if summaries_only:
        return rid, 'summary'
    arch = f'claude_main_{rid}.tar.gz'
    rec = json.loads(s3.get_object(Bucket=bucket, Key=f'{ROOT}{rid}/{arch}.receipt.json')['Body'].read())
    (d / 'RECEIPT.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    raw = s3.get_object(Bucket=bucket, Key=f'{ROOT}{rid}/{arch}')['Body'].read()
    h = hashlib.sha256(raw).hexdigest()
    if h != rec['sha256'] or len(raw) != rec['bytes']:
        return rid, 'SHA_MISMATCH'
    n = 0
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as tar:
        for m in tar.getmembers():
            if not m.isfile() or not keep(m.name): continue
            target = (d / 'x' / m.name).resolve()
            if not str(target).startswith(str((d / 'x').resolve())): raise RuntimeError('unsafe member ' + m.name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(tar.extractfile(m).read()); n += 1
    (d / 'FETCH_OK.json').write_text(json.dumps(dict(archive=arch, sha256=h, bytes=len(raw), members_kept=n,
                                                     utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())), indent=1), encoding='utf-8')
    return rid, 'ok'


class SftpStore:
    """The same reads through a running E pod (the volume is mounted at /workspace): ssh listing, sftp downloads."""
    def __init__(self, pod):
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import pods_e_v01 as pv
        self.pv = pv; self.pod = pod; self.tmp = E / 'runs' / '_sftp_tmp'; self.tmp.mkdir(parents=True, exist_ok=True)

    def list_object_dirs(self, prefixes):
        r = self.pv.ssh(self.pod, 'ls /workspace/' + ROOT, timeout=120)
        names = r.stdout.split()
        return sorted(n for n in names if any(n.startswith(p) for p in prefixes))

    def read(self, key):
        local = self.tmp / key.replace('/', '__')
        for attempt in range(5):
            r = self.pv.sftp(self.pod, [f'get "/workspace/{key}" "{local}"'], timeout=1800)
            if r.returncode == 0 and local.exists(): break
            time.sleep(10 * (attempt + 1))
        else:
            raise RuntimeError('sftp get failed: ' + key)
        b = local.read_bytes(); local.unlink(); return b


class S3Store:
    def __init__(self):
        self.s3, self.bucket = client()

    def list_object_dirs(self, prefixes):
        return list_runs(self.s3, self.bucket, prefixes)

    def read(self, key):
        return self.s3.get_object(Bucket=self.bucket, Key=key)['Body'].read()


def fetch_store(st, rid, summaries_only):
    d = RUNS / rid
    if (d / 'FETCH_OK.json').exists() or (summaries_only and (d / 'SUMMARY.json').exists()):
        return rid, 'present'
    d.mkdir(parents=True, exist_ok=True)
    (d / 'SUMMARY.json').write_bytes(st.read(f'{ROOT}{rid}/SUMMARY.json'))
    if summaries_only:
        return rid, 'summary'
    arch = f'claude_main_{rid}.tar.gz'
    rec = json.loads(st.read(f'{ROOT}{rid}/{arch}.receipt.json'))
    (d / 'RECEIPT.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')
    raw = st.read(f'{ROOT}{rid}/{arch}')
    h = hashlib.sha256(raw).hexdigest()
    if h != rec['sha256'] or len(raw) != rec['bytes']:
        return rid, 'SHA_MISMATCH'
    n = 0
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as tar:
        for m in tar.getmembers():
            if not m.isfile() or not keep(m.name): continue
            target = (d / 'x' / m.name).resolve()
            if not str(target).startswith(str((d / 'x').resolve())): raise RuntimeError('unsafe member ' + m.name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(tar.extractfile(m).read()); n += 1
    (d / 'FETCH_OK.json').write_text(json.dumps(dict(archive=arch, sha256=h, bytes=len(raw), members_kept=n, via=type(st).__name__,
                                                     utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())), indent=1), encoding='utf-8')
    return rid, 'ok'


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('prefixes', nargs='+'); ap.add_argument('--threads', type=int, default=8)
    ap.add_argument('--summaries-only', action='store_true'); ap.add_argument('--list', action='store_true'); ap.add_argument('--sftp', help='pod name')
    a = ap.parse_args()
    if a.sftp:
        st = SftpStore(a.sftp); rids = st.list_object_dirs(a.prefixes)
        print(len(rids), 'runs via', a.sftp, flush=True)
        if a.list:
            for r in rids: print(r)
            return
        counts = {}
        for rid in rids:
            try:
                r, s_ = fetch_store(st, rid, a.summaries_only)
            except Exception as e:
                s_ = 'ERROR'; print(rid, 'ERROR', repr(e)[:200], flush=True)
            counts[s_] = counts.get(s_, 0) + 1
            if s_ not in ('ok', 'present', 'summary'): print(rid, s_, flush=True)
        print(json.dumps(counts)); return
    s3, bucket = client()
    rids = list_runs(s3, bucket, a.prefixes)
    print(len(rids), 'runs on the volume for', a.prefixes, flush=True)
    if a.list:
        for r in rids: print(r)
        return
    RUNS.mkdir(exist_ok=True)
    import shutil
    free = shutil.disk_usage(str(RUNS)).free / 1e9
    if free < MIN_FREE_GB + 0.012 * len(rids):
        raise SystemExit('REFUSED: %.0f GB free on the laptop; keep >= %d GB free' % (free, MIN_FREE_GB))
    counts = {}
    with cf.ThreadPoolExecutor(a.threads) as ex:
        futs = [ex.submit(fetch, s3, bucket, r, a.summaries_only) for r in rids]
        for f in cf.as_completed(futs):
            rid, st = f.result(); counts[st] = counts.get(st, 0) + 1
            if st not in ('ok', 'present', 'summary'): print(rid, st, flush=True)
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
