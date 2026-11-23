"""Salvage runs whose capture and both reviews finished but whose volume copy failed (Disk quota exceeded, 19 Nov ~14:55 EST).

The worker had already written the complete local archive (/opt/claude_main/archives/claude_main_<rid>.tar.gz, renamed from
.partial only when complete) and the job folder with SUMMARY.json; it failed in shutil.copyfileobj to the volume, before the
receipt. Here, per such run: require the local SUMMARY status CAPTURED_AND_REVIEWED, move the archive into
/opt/claude_v13_local/results/<rid>/, write the receipt in the worker's schema (archive, sha256, bytes, run_id, status,
frames_dropped, keep_raw, utc) plus salvaged=true, and copy SUMMARY.json. Only the status field of SUMMARY is read.
frames_dropped is the worker's own count: 0 when keep_raw is true (every frame kept), recomputed here from the archive members.
Pod system python3. Usage: python3 salvage_local_v13.py
"""
import datetime, hashlib, json, os, pathlib, shutil, tarfile

L = pathlib.Path('/opt/claude_main'); OUT = pathlib.Path('/opt/claude_v13_local/results')
OUT.mkdir(parents=True, exist_ok=True)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()


done = []
for a in sorted((L / 'archives').glob('claude_main_*.tar.gz')):
    rid = a.name[len('claude_main_'):-len('.tar.gz')]
    s = json.loads((L / 'jobs' / rid / 'SUMMARY.json').read_text())
    assert s['status'] == 'CAPTURED_AND_REVIEWED' and s['run_id'] == rid, rid
    fh = json.loads((L / 'jobs' / rid / 'FILE_HASHES.json').read_text())
    frames_total = sum(1 for f in fh['files'] if f['path'].endswith('.npy') and f['path'].split('/')[0] in ('raw', 'clean'))
    with tarfile.open(a, 'r:gz') as t:
        kept = sum(1 for m in t if m.isfile() and m.name.endswith('.npy') and m.name.split('/')[-2] in ('raw', 'clean') and '/capture/' in m.name)
    d = OUT / rid; d.mkdir(exist_ok=False)
    os.replace(a, d / a.name)
    rec = dict(archive=a.name, sha256=sha(d / a.name), bytes=(d / a.name).stat().st_size, run_id=rid, status=s['status'],
               frames_dropped=frames_total - kept, keep_raw=bool(s['keep_raw']), utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               salvaged=True, salvage_note='volume copy failed (Disk quota exceeded); local archive moved; receipt written by salvage_local_v13.py')
    with open(d / (a.name + '.receipt.json'), 'x') as f: json.dump(rec, f, indent=2)
    shutil.copyfile(L / 'jobs' / rid / 'SUMMARY.json', d / 'SUMMARY.json')
    done.append(dict(run=rid, frames_dropped=rec['frames_dropped'], bytes=rec['bytes']))
print(json.dumps(dict(salvaged=done)))
