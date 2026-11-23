"""Build packet_x_v13 from packet_main_v03 (read-only source in P\\03_runbook), exactly as d1\\build_packet_d1_v13.py built
packet_d1_v13, with ONE file replaced: claude_smoke_v01/DEVELOPMENT_PROTOCOL_SMOKE_v01.json <- crossing/DEVELOPMENT_PROTOCOL_X_v13.json
(the main protocol unchanged, with the pedestrian-crossing evaluation cases of the generator extension appended; A11 sec. 3, X).
No code file changes. The hash bindings (RUNTIME_SOURCE_BINDING_SMOKE_v01.json, SMOKE_MANIFEST_v01.json, PACKET_MANIFEST_v01.json) are
recomputed; a tar.gz and a receipt are written. New file, 21 Nov 2026 (Claude Opus 5.5, session CD).
Usage: python -I -B build_packet_x_v13.py   (never overwrites)
"""
import datetime, hashlib, json, pathlib, shutil, tarfile

HERE = pathlib.Path(__file__).resolve().parent
OUTROOT = HERE.parent / 'packets'
SRC = pathlib.Path(r'<library folder>\packet_main_v03')
NAME = 'packet_x_v13'
NL = chr(10)
SETS = {'DEVELOPMENT_PROTOCOL_SMOKE_v01.json': HERE / 'DEVELOPMENT_PROTOCOL_X_v13.json'}


def sha(p):
    h = hashlib.sha256()
    with pathlib.Path(p).open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 ** 2), b''): h.update(block)
    return h.hexdigest()


def dump(path, value): pathlib.Path(path).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    out = OUTROOT / NAME; assert not out.exists(), 'Packet folder exists; never overwrite'
    old_proto = json.loads((SRC / 'claude_smoke_v01' / 'DEVELOPMENT_PROTOCOL_SMOKE_v01.json').read_text(encoding='utf-8'))
    new_proto = json.loads(SETS['DEVELOPMENT_PROTOCOL_SMOKE_v01.json'].read_text(encoding='utf-8'))
    assert new_proto['cases'][:len(old_proto['cases'])] == old_proto['cases'], 'the packet protocol\'s own cases must be unchanged'
    assert {k: v for k, v in new_proto.items() if k not in ('cases', 'claude_v13_x_derivation')} == {k: v for k, v in old_proto.items() if k != 'cases'}
    shutil.copytree(SRC, out, ignore=shutil.ignore_patterns('RELEASE_SMOKE_v01.json', '__pycache__'))
    C = out / 'claude_smoke_v01'; changes = []
    for rel, source in SETS.items():
        rel = pathlib.PurePosixPath(rel); target = C.joinpath(*rel.parts); existed = target.exists(); old = sha(target) if existed else None
        target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, target)
        changes.append(dict(path='claude_smoke_v01/' + rel.as_posix(), source=str(source), old_sha256=old, new_sha256=sha(target), added=not existed))
    bpath = C / 'RUNTIME_SOURCE_BINDING_SMOKE_v01.json'; binding = json.loads(bpath.read_text(encoding='utf-8'))
    smoke_paths = sorted('claude_smoke_v01/' + p.relative_to(C).as_posix() for p in C.rglob('*') if p.is_file() and p.name != 'RUNTIME_SOURCE_BINDING_SMOKE_v01.json'
                         and p.suffix in ('.py', '.json') and not p.name.startswith('JOBS_'))
    base = [f for f in binding['files'] if not f['path'].startswith('claude_smoke_v01/')]
    binding['files'] = base + [dict(path=p, sha256=sha(out / p)) for p in smoke_paths]
    binding['smoke_files'] = len(smoke_paths)
    binding['main_packet'] = dict(name=NAME, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), derived_from='packet_main_v03', changes=changes,
                                  parent=binding.get('main_packet'))
    (out / 'X_CHANGES.md').write_text('# packet_x_v13: changes from packet_main_v03' + NL + NL + 'Revision v13 X (AMENDMENT_11_v13.md sec. 3). Only '
        'claude_smoke_v01/DEVELOPMENT_PROTOCOL_SMOKE_v01.json is replaced: the main protocol (32d683a0...) with its cases unchanged and the '
        'pedestrian-crossing evaluation cases of the generator extension appended (crossing/make_cases_x_pc_v13.py). No code file changed. '
        'CHECK_REPORT_v01.md and diffs/ describe packet_main_v03 and are unchanged.' + NL, encoding='utf-8', newline=NL)
    dump(bpath, binding)
    dump(out / 'SMOKE_MANIFEST_v01.json', dict(schema='CLAUDE_SMOKE_MANIFEST_V01', files=[dict(path='claude_smoke_v01/' + p.relative_to(C).as_posix(), sha256=sha(p))
         for p in sorted(C.rglob('*')) if p.is_file()]))
    files = [dict(path=p.relative_to(out).as_posix(), bytes=p.stat().st_size, sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'PACKET_MANIFEST_v01.json']
    dump(out / 'PACKET_MANIFEST_v01.json', dict(schema='CLAUDE_MAIN_PACKET_MANIFEST_V01', files=files))
    tgz = OUTROOT / (NAME + '.tar.gz'); assert not tgz.exists()
    with tarfile.open(tgz, 'x:gz') as tar:
        for p in sorted(out.rglob('*')):
            if p.is_file(): tar.add(p, arcname=NAME + '/' + p.relative_to(out).as_posix(), recursive=False)
    receipt = dict(packet=NAME, tar=tgz.name, tar_sha256=sha(tgz), tar_bytes=tgz.stat().st_size, changes=changes, binding_sha256=sha(bpath),
                   protocol_sha256=sha(C / 'DEVELOPMENT_PROTOCOL_SMOKE_v01.json'), smoke_files=len(smoke_paths), source_packet=str(SRC),
                   made_by=dict(script='build_packet_x_v13.py', sha256=sha(__file__)))
    dump(OUTROOT / (NAME + '_RECEIPT.json'), receipt); print(json.dumps(receipt, indent=1))


if __name__ == '__main__':
    main()
