"""Give the network volume back its space: delete my own v13 run ARCHIVES from /workspace/claude_v13_cd_v01/results/ once each has a
verified laptop copy (coordinator's approval, 19 Nov 2026 ~15:10 EST; rules: only files under /workspace/claude_v13_cd_v01/; a file only
after its laptop copy's SHA-256 matches; the receipt list is written before anything is deleted; nothing else is touched).

Only the .tar.gz archives are deleted (they hold the space); receipts and SUMMARY.json stay on the volume (a few kB each).
Steps: (1) for every run whose archives/<rid>/DOWNLOAD_OK.json names the volume as its source, re-hash the laptop archive and require
equality with the receipt; (2) write volume_cleanup_receipts.json (never overwritten); (3) on the pod, for each listed path, re-hash the
volume file and delete it only if it equals the receipt; print counts. Usage: python -I volume_cleanup_v13.py POD [--dry-run]
"""
import datetime, hashlib, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(HERE))
import pods_v13 as pv

ROOT = '/workspace/claude_v13_cd_v01/results'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()


def main():
    pod = sys.argv[1]; dry = '--dry-run' in sys.argv
    out = CD / 'volume_cleanup_receipts.json'
    if out.exists() and not dry: raise SystemExit('REFUSED: receipts exist')
    rows = []
    for ok in sorted((CD / 'archives').glob('*/DOWNLOAD_OK.json')):
        d = json.loads(ok.read_text(encoding='utf-8'))
        if not d['source'].endswith(f"{ROOT}/{d['run_id']}"): continue
        local = ok.parent / d['archive']
        h = sha(local)
        assert h == d['sha256'], d['run_id']
        rec = json.loads((ok.parent / (d['archive'] + '.receipt.json')).read_text(encoding='utf-8'))
        assert rec['sha256'] == h and rec['bytes'] == local.stat().st_size, d['run_id']
        rows.append(dict(run_id=d['run_id'], volume_path=f"{ROOT}/{d['run_id']}/{d['archive']}", sha256=h, bytes=rec['bytes'],
                         laptop_path=str(local), laptop_sha256=h))
    doc = dict(schema='VOLUME_CLEANUP_RECEIPTS_V13', approval='coordinator session, 19 Nov 2026 ~15:10 EST (option 1)',
               rule='delete only these archive files, each re-hashed on the pod and equal to sha256 below; receipts and SUMMARY.json stay',
               utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), files=rows, total_bytes=sum(r['bytes'] for r in rows))
    print(f'{len(rows)} archives, {doc["total_bytes"] / 1e9:.2f} GB verified on the laptop')
    if dry: return
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    script = 'import hashlib,json,os,sys\nrows=json.loads(sys.stdin.read())\nok=bad=0\nfor r in rows:\n    p=r["volume_path"]\n' \
             '    assert p.startswith("/workspace/claude_v13_cd_v01/results/") and p.endswith(".tar.gz")\n' \
             '    h=hashlib.sha256()\n    with open(p,"rb") as f:\n        for b in iter(lambda:f.read(8<<20),b""):h.update(b)\n' \
             '    if h.hexdigest()==r["sha256"]:\n        os.remove(p);ok+=1\n    else:bad+=1\nprint(json.dumps(dict(deleted=ok,hash_mismatch_kept=bad)))\n'
    tmp = CD / 'pods' / pod / 'cleanup_rows.json'
    tmp.write_text(json.dumps([dict(volume_path=r['volume_path'], sha256=r['sha256']) for r in rows]), encoding='utf-8')
    (CD / 'pods' / pod / 'cleanup_remote.py').write_text(script, encoding='utf-8')
    r = pv.sftp(pod, [f'put "{CD / "pods" / pod / "cleanup_remote.py"}" /root/cmp/cleanup_remote.py', f'put "{tmp}" /root/cmp/cleanup_rows.json'])
    assert r.returncode == 0, r.stderr
    r = pv.ssh(pod, 'python3 /root/cmp/cleanup_remote.py < /root/cmp/cleanup_rows.json', timeout=3600)
    print(r.stdout, r.stderr[-500:])
    doc['result'] = r.stdout.strip(); out.write_text(json.dumps(doc, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
