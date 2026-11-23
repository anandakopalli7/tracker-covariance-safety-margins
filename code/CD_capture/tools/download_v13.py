"""Verified download of run archives from a pod (its local results folder, or the volume folder read through the pod).

For every run folder under REMOTE (default /opt/claude_v13_local/results) that has a receipt and whose id starts with one of
the prefixes: fetch claude_main_<rid>.tar.gz and its .receipt.json into archives/<rid>/, hash the local archive, and write
archives/<rid>/DOWNLOAD_OK.json only if SHA-256 and byte count equal the receipt. Runs already verified are skipped.
Only receipts are read (archive, sha256, bytes, status, keep_raw); no outcome.
Usage: python -I download_v13.py POD [--remote DIR] [--prefixes pc13_,pd13_,a1,ctl] [--max N]
"""
import argparse, datetime, hashlib, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(HERE))
import pods_v13 as pv

DEST = CD / 'archives'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('pod'); ap.add_argument('--remote', default='/opt/claude_v13_local/results')
    ap.add_argument('--prefixes', default='pc13_,pd13_,pd13pilot_,a1,ctl_'); ap.add_argument('--max', type=int, default=10 ** 6)
    ap.add_argument('--shard', default='0/1', help='i/n: this process fetches the runs whose position in the sorted list is i mod n')
    ap.add_argument('--chunk', type=int, default=2)
    a = ap.parse_args()
    lst = pv.ssh(a.pod, f"cd {a.remote} && for d in */; do d=${{d%/}}; r=$(ls $d/*.receipt.json 2>/dev/null | head -1); [ -n \"$r\" ] && echo \"$d $(cat $r | tr -d '\\n')\"; done", timeout=300)
    rows = []
    for line in lst.stdout.splitlines():
        rid, rec = line.split(' ', 1); rec = json.loads(rec)
        if rid.startswith(tuple(a.prefixes.split(','))): rows.append((rid, rec))
    si, sn = map(int, a.shard.split('/')); rows = sorted(rows)[si::sn]
    todo = [(r, c) for r, c in rows if not (DEST / r / 'DOWNLOAD_OK.json').is_file()][:a.max]
    print(f'{a.pod}: {len(rows)} runs with receipts, {len(todo)} to fetch', flush=True)
    ok = bad = 0
    for i in range(0, len(todo), a.chunk):
        chunk = todo[i:i + a.chunk]; lines = []
        for rid, rec in chunk:
            (DEST / rid).mkdir(parents=True, exist_ok=True)
            lines += [f'get "{a.remote}/{rid}/{rec["archive"]}" "{DEST / rid / rec["archive"]}"',
                      f'get "{a.remote}/{rid}/{rec["archive"]}.receipt.json" "{DEST / rid / (rec["archive"] + ".receipt.json")}"']
        r = pv.sftp(a.pod, lines, timeout=7200)
        for rid, rec in chunk:
            f = DEST / rid / rec['archive']
            good = f.is_file() and f.stat().st_size == rec['bytes'] and sha(f) == rec['sha256']
            if good:
                (DEST / rid / 'DOWNLOAD_OK.json').write_text(json.dumps(dict(run_id=rid, archive=rec['archive'], sha256=rec['sha256'], bytes=rec['bytes'],
                    status=rec['status'], keep_raw=rec['keep_raw'], salvaged=rec.get('salvaged', False), source=f'{a.pod}:{a.remote}/{rid}',
                    utc=datetime.datetime.now(datetime.timezone.utc).isoformat()), indent=1), encoding='utf-8'); ok += 1
            else:
                bad += 1; print('MISMATCH or missing', rid, r.returncode, r.stderr[-200:], flush=True)
        print(f'  {min(i + a.chunk, len(todo))}/{len(todo)} ok={ok} bad={bad}', flush=True)
    print(json.dumps(dict(pod=a.pod, remote=a.remote, fetched_ok=ok, failed=bad)))


if __name__ == '__main__':
    main()
