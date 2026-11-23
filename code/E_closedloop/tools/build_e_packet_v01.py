"""Build package E's pod packet: packet_main_v03 (read only, in P) plus the files of an overlay folder copied into
claude_smoke_v01/, with the hash bindings recomputed exactly as P\\03_runbook\\main_sources_v01\\build_main_packet_v01.py
does (RUNTIME_SOURCE_BINDING_SMOKE_v01.json for every .py/.json under claude_smoke_v01 except JOBS_*, SMOKE_MANIFEST,
PACKET_MANIFEST), then a tar.gz and a receipt.

Usage: python -I build_e_packet_v01.py --name packet_e_v01 [--overlay DIR ...] [--base DIR] [--dev]
  --overlay   folders whose files (relative paths kept) go into claude_smoke_v01/ (default: ..\\src)
  --base      the base packet folder (default: P\\03_runbook\\packet_main_v03)
  --dev       build into packets\\dev_<name> (replaced if present) and write no tar: for laptop tests only
"""
import argparse, datetime, hashlib, json, pathlib, shutil, tarfile

E = pathlib.Path(__file__).resolve().parents[1]
BASE = pathlib.Path(r'<library folder>\packet_main_v03')
OUT = E / 'packets'


def sha(p):
    h = hashlib.sha256()
    with pathlib.Path(p).open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 ** 2), b''): h.update(block)
    return h.hexdigest()


def dump(path, value): pathlib.Path(path).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--name', required=True); ap.add_argument('--overlay', action='append', default=None)
    ap.add_argument('--base', default=str(BASE)); ap.add_argument('--dev', action='store_true')
    a = ap.parse_args()
    overlays = [pathlib.Path(x).resolve() for x in (a.overlay or [str(E / 'src')])]
    name = ('dev_' + a.name) if a.dev else a.name
    out = OUT / name
    if a.dev and out.exists(): shutil.rmtree(out)
    assert not out.exists(), 'Packet folder exists; never overwrite'
    shutil.copytree(a.base, out, ignore=shutil.ignore_patterns('RELEASE_SMOKE_v01.json', '__pycache__', '*.pyc'))
    C = out / 'claude_smoke_v01'; changes = []
    for ov in overlays:
        for src in sorted(p for p in ov.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'):
            rel = src.relative_to(ov); target = C.joinpath(*rel.parts)
            existed = target.exists(); old = sha(target) if existed else None
            target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, target)
            changes.append(dict(path='claude_smoke_v01/' + rel.as_posix(), source=str(src), old_sha256=old, new_sha256=sha(target), added=not existed))
    bpath = C / 'RUNTIME_SOURCE_BINDING_SMOKE_v01.json'; binding = json.loads(bpath.read_text(encoding='utf-8'))
    smoke_paths = sorted('claude_smoke_v01/' + p.relative_to(C).as_posix() for p in C.rglob('*') if p.is_file() and p.name != 'RUNTIME_SOURCE_BINDING_SMOKE_v01.json'
                         and p.suffix in ('.py', '.json') and not p.name.startswith('JOBS_'))
    base = [f for f in binding['files'] if not f['path'].startswith('claude_smoke_v01/')]
    binding['files'] = base + [dict(path=p, sha256=sha(out / p)) for p in smoke_paths]
    binding['smoke_files'] = len(smoke_paths)
    binding['main_packet'] = dict(name=name, base=str(a.base), utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), changes=changes, package='E')
    dump(bpath, binding)
    dump(out / 'SMOKE_MANIFEST_v01.json', dict(schema='CLAUDE_SMOKE_MANIFEST_V01', files=[dict(path='claude_smoke_v01/' + p.relative_to(C).as_posix(), sha256=sha(p))
         for p in sorted(C.rglob('*')) if p.is_file()]))
    files = [dict(path=p.relative_to(out).as_posix(), bytes=p.stat().st_size, sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'PACKET_MANIFEST_v01.json']
    dump(out / 'PACKET_MANIFEST_v01.json', dict(schema='CLAUDE_MAIN_PACKET_MANIFEST_V01', files=files))
    receipt = dict(packet=name, base=str(a.base), changes=changes, binding_sha256=sha(bpath), protocol_sha256=sha(C / 'DEVELOPMENT_PROTOCOL_SMOKE_v01.json'),
                   smoke_files=len(smoke_paths), utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    if not a.dev:
        tgz = OUT / (name + '.tar.gz'); assert not tgz.exists()
        with tarfile.open(tgz, 'x:gz') as tar:
            for p in sorted(out.rglob('*')):
                if p.is_file(): tar.add(p, arcname=name + '/' + p.relative_to(out).as_posix(), recursive=False)
        receipt.update(tar=tgz.name, tar_sha256=sha(tgz), tar_bytes=tgz.stat().st_size)
        dump(OUT / (name + '_RECEIPT.json'), receipt)
    print(json.dumps({k: v for k, v in receipt.items() if k != 'changes'}, indent=1), '\nchanges:', len(changes))


if __name__ == '__main__':
    main()
