"""Build packet_d1_v13 from packet_main_v03 (read-only source in P\\03_runbook), as build_main_packet_v01.py builds a
main packet: copy the packet, replace or add files inside claude_smoke_v01/ (file names kept, so the worker, entry
point and release logic are unchanged), recompute the hash bindings (RUNTIME_SOURCE_BINDING_SMOKE_v01.json,
SMOKE_MANIFEST_v01.json, PACKET_MANIFEST_v01.json), write a tar.gz and a receipt.

Changes for revision v13 D1 (AMENDMENT_10_v13.md sec. 6):
  claude_smoke_v01/DEVELOPMENT_PROTOCOL_SMOKE_v01.json  <- d1/DEVELOPMENT_PROTOCOL_D1_v13.json (main protocol + 165 D1 cases)
  claude_smoke_v01/actor_policy_d1_v01.py              <- d1/src (added: the lead-variant actor-request version)
  claude_smoke_v01/scene_actors_d1_v01.py              <- d1/src (added: ScenarioActors with that policy)
  claude_smoke_v01/probe_arms_v01.py                   <- d1/src (2 lines: import, scene class)
  claude_smoke_v01/review/review_actor_records_v04.py  <- d1/src (2 lines: the replayed policy object)
Usage: python -I build_packet_d1_v13.py   (never overwrites)
"""
import datetime, hashlib, json, pathlib, shutil, tarfile

HERE = pathlib.Path(__file__).resolve().parent
OUTROOT = HERE.parent / 'packets'
SRC = pathlib.Path(r'<library folder>\packet_main_v03')
NAME = 'packet_d1_v13'
NL = chr(10)
SETS = {'DEVELOPMENT_PROTOCOL_SMOKE_v01.json': HERE / 'DEVELOPMENT_PROTOCOL_D1_v13.json',
        'actor_policy_d1_v01.py': HERE / 'src' / 'actor_policy_d1_v01.py',
        'scene_actors_d1_v01.py': HERE / 'src' / 'scene_actors_d1_v01.py',
        'probe_arms_v01.py': HERE / 'src' / 'probe_arms_v01.py',
        'review/review_actor_records_v04.py': HERE / 'src' / 'review' / 'review_actor_records_v04.py'}


def sha(p):
    h = hashlib.sha256()
    with pathlib.Path(p).open('rb') as f:
        for block in iter(lambda: f.read(8 * 1024 ** 2), b''): h.update(block)
    return h.hexdigest()


def dump(path, value): pathlib.Path(path).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    out = OUTROOT / NAME; assert not out.exists(), 'Packet folder exists; never overwrite'
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
    # Review finding 8: regenerate the two stale diffs and add a change note (not bound; documentation only).
    import difflib
    for rel, dname in (('probe_arms_v01.py', 'probe_arms_v01.diff'), ('review/review_actor_records_v04.py', 'review_review_actor_records_v04.diff')):
        a = (SRC / 'claude_smoke_v01' / rel).read_text(encoding='utf-8').splitlines(keepends=True)
        b = (C / rel).read_text(encoding='utf-8').splitlines(keepends=True)
        (out / 'diffs' / dname).write_text(''.join(difflib.unified_diff(a, b, 'packet_main_v03/claude_smoke_v01/' + rel, NAME + '/claude_smoke_v01/' + rel)), encoding='utf-8', newline=NL)
    (out / 'D1_CHANGES.md').write_text('# packet_d1_v13: changes from packet_main_v03' + NL + NL + 'Revision v13 package D1 (AMENDMENT_10_v13.md sec. 6). '
        'CHECK_REPORT_v01.md and the other files under diffs/ describe packet_main_v03 and are unchanged; diffs/probe_arms_v01.diff and '
        'diffs/review_review_actor_records_v04.diff are regenerated against packet_main_v03. Changed or added (all bound): '
        + ', '.join(c['path'] for c in changes) + '. Independent review: work/CD_capture/d1/REVIEW_D1_PACKET_v01.md (Claude Fable 5.2).' + NL,
        encoding='utf-8', newline=NL)
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
                   made_by=dict(script='build_packet_d1_v13.py', sha256=sha(__file__)))
    dump(OUTROOT / (NAME + '_RECEIPT.json'), receipt); print(json.dumps(receipt, indent=1))


if __name__ == '__main__':
    main()
