"""Re-publish salvaged runs (complete on this pod's local disk) to the volume folder claude_v13_cd_v01 (coordinator's request,
19 Nov; volume grown to 300 GB, CD budget <= 50 GB). Per run: copy the archive to <dst>/<name>.partial, require its SHA-256 = the
receipt, then replace the failed partial copy; copy the receipt and SUMMARY.json. Pod system python3. Usage: python3 - RID [RID ...]"""
import hashlib, json, os, pathlib, shutil, sys
SRC = pathlib.Path('/opt/claude_v13_local/results'); DST = pathlib.Path('/workspace/claude_v13_cd_v01/results')
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()
res = []
for rid in sys.argv[1:]:
    s = SRC / rid; rec = json.loads(next(s.glob('*.receipt.json')).read_text()); d = DST / rid; d.mkdir(parents=True, exist_ok=True)
    tmp = d / (rec['archive'] + '.partial'); shutil.copyfile(s / rec['archive'], tmp)
    if sha(tmp) != rec['sha256']: tmp.unlink(); res.append((rid, 'HASH MISMATCH, not published')); continue
    os.replace(tmp, d / rec['archive'])
    shutil.copyfile(next(s.glob('*.receipt.json')), d / (rec['archive'] + '.receipt.json')); shutil.copyfile(s / 'SUMMARY.json', d / 'SUMMARY.json')
    res.append((rid, 'published', rec['bytes']))
print(json.dumps(res))
