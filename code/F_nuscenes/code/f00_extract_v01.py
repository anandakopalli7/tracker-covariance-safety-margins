"""Package F (revision v13), step 00: verify and extract the nuScenes downloads. New file, 19 Nov 2026 (Claude Opus 5.5).

Reads revision_v13\\data\\nuscenes\\{v1.0-trainval_meta.tgz, nuScenes-map-expansion-v1.3.zip, can_bus.zip, md5.checksum};
checks each archive's MD5 against md5.checksum where listed; extracts with path-safe filters into the same folder.
Writes logs\\f00_extract_v01.json (sizes, MD5, SHA-256, member counts). Computes no value of any analysis.
Usage: python -I f00_extract_v01.py
"""
import hashlib, json, pathlib, tarfile, time, zipfile

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parents[2] / 'data' / 'nuscenes'
LOG = HERE.parent / 'logs' / 'f00_extract_v01.json'


def digests(p):
    m = hashlib.md5(); s = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 22), b''):
            m.update(blk); s.update(blk)
    return m.hexdigest(), s.hexdigest()


def safe_zip_extract(zp, dest):
    n = 0
    with zipfile.ZipFile(zp) as z:
        for info in z.infolist():
            name = info.filename
            target = (dest / name).resolve()
            if dest.resolve() not in target.parents and target != dest.resolve():
                raise RuntimeError('REFUSED: unsafe member %r in %s' % (name, zp))
            z.extract(info, dest); n += 1
    return n


def main():
    md5 = {}
    for line in (DATA / 'md5.checksum').read_text(encoding='utf-8').splitlines():
        parts = line.split()
        if len(parts) == 2:
            md5[parts[1]] = parts[0]
    rec = dict(started=time.strftime('%Y-%m-%d %H:%M:%S'), archives={})
    for name in ('v1.0-trainval_meta.tgz', 'nuScenes-map-expansion-v1.3.zip', 'can_bus.zip'):
        p = DATA / name
        m, s = digests(p)
        r = dict(bytes=p.stat().st_size, md5=m, sha256=s, md5_listed=md5.get(name), md5_ok=(md5.get(name) == m) if name in md5 else None)
        t0 = time.time()
        if name.endswith('.tgz'):
            with tarfile.open(p, 'r:gz') as t:
                members = t.getmembers()
                t.extractall(DATA, filter='data')
            r['members'] = len(members)
        else:
            dest = DATA / ('map_expansion' if 'map-expansion' in name else '')
            dest.mkdir(exist_ok=True)
            r['members'] = safe_zip_extract(p, dest)
            r['dest'] = str(dest)
        r['seconds'] = round(time.time() - t0, 1)
        rec['archives'][name] = r
        print(name, json.dumps(r), flush=True)
    rec['finished'] = time.strftime('%Y-%m-%d %H:%M:%S')
    LOG.write_text(json.dumps(rec, indent=1), encoding='utf-8')
    print('WROTE', LOG)


if __name__ == '__main__':
    main()
