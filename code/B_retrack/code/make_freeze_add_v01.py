"""v13 package B: addendum to the freeze manifest (coordinator request 19 Nov 2026, 20:50 EST). New file, 19 Nov 2026 (Claude Opus 5.5).
Re-hashes every file listed in work\\locks\\FREEZE_B.json and every file now in the folders it covers (B_retrack\\code, B_retrack\\imm2,
B_retrack\\out\\pbar, B_retrack\\out\\b3, shared\\trackers), and writes work\\locks\\FREEZE_B_add<n>.json with every file that CHANGED or is
NEW since FREEZE_B.json (path, old SHA-256 if any, new SHA-256, size, mtime) and the reason given on the command line. FREEZE_B.json is not
touched. Refuses if any library file (shared\\trackers) changed (a library change after the freeze needs the coordinator's OK first).
Usage: python -I -B -X utf8 make_freeze_add_v01.py <n> "<reason>"
"""
import hashlib, json, pathlib, sys, time

W = pathlib.Path(r'ARS_TRIAL\revision_v13\work')
B = W / 'B_retrack'
MAN = W / 'locks' / 'FREEZE_B.json'
FOLDERS = [(B / 'code', '*.py'), (B / 'code', '*.sh'), (B / 'imm2', '*'), (B / 'out' / 'pbar', 'PBAR_*_v01.json'), (B / 'out' / 'b3', '*.json')]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    n = int(sys.argv[1]); reason = sys.argv[2]
    out = W / 'locks' / ('FREEZE_B_add%d.json' % n)
    if out.exists():
        raise SystemExit('REFUSED: %s exists' % out)
    man = json.loads(MAN.read_text(encoding='utf-8'))
    listed = {}
    for key in ('library', 'pbar', 'b3_tuning', 'package_b_code', 'second_imm', 'definitions'):
        for e in man[key]:
            listed[str(W / e['path'])] = e['sha256']
    for e in man['record_modules_read_only']:
        listed[e['path']] = e['sha256']
    current = {}
    for p in sorted((W / 'shared' / 'trackers').rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            current[str(p)] = p
    for folder, pat in FOLDERS:
        for p in sorted(folder.glob(pat)):
            if p.is_file():
                current[str(p)] = p
    for path in listed:
        current.setdefault(path, pathlib.Path(path))
    changed = []; new = []; missing = []
    for path, p in sorted(current.items()):
        if not p.exists():
            missing.append(path); continue
        h = sha(p)
        st = p.stat()
        ent = dict(path=str(p.relative_to(W)) if str(p).startswith(str(W)) else str(p), sha256=h, bytes=st.st_size,
                   mtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime)))
        if path in listed:
            if listed[path] != h:
                ent['old_sha256'] = listed[path]; changed.append(ent)
        else:
            new.append(ent)
    lib_changed = [e for e in changed if e['path'].startswith('shared')]
    if lib_changed or any(m.startswith(str(W / 'shared')) for m in missing):
        raise SystemExit('REFUSED: library file changed or missing: %s %s' % ([e['path'] for e in lib_changed], missing))
    doc = dict(addendum=n, to='work\\locks\\FREEZE_B.json', freeze_b_sha256=sha(MAN), written=time.strftime('%Y-%m-%d %H:%M:%S %Z'),
               writer='package-B session, Claude Opus 5.5 (claude-opus-5-5)', reason=reason,
               library_unchanged=True, changed=changed, new=new, missing=missing,
               note='FREEZE_B.json is kept as written; this addendum lists every covered file that changed or is new since it.')
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('wrote', out, 'changed', [e['path'] for e in changed], 'new', [e['path'] for e in new], 'missing', missing)


if __name__ == '__main__':
    main()
