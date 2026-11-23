"""v13 package B: freeze addendum n (n >= 3) layered on work\\locks\\FREEZE_B.json and every earlier addendum. New file, 20 Nov 2026
(Claude Opus 5.5); make_freeze_add_v01.py is kept unchanged. Differences from v01:
  * the reference state is FREEZE_B.json with add1 .. add<n-1> applied in order (each addendum's changed/new entries replace or add),
    so the new addendum lists only what changed or is new since the last one;
  * it also covers the fresh-run task of 20 Nov 2026 (coordinator): B_retrack\\recount_fresh\\ (the second program: *.py, *.md),
    B_retrack\\B_FRESH_DEFINITIONS_v02.md, B_retrack\\B_ANALYSIS_DEFINITIONS_v01.md, B_retrack\\VENV_FREEZE_B.txt (B's venv packages),
    B_retrack\\RUN_AFTER_LOCK2_B.md (the run sheet),
    and records the SHA-256 of package CD's engine CD_capture\\analysis\\gl_fast_v13.py, which the fresh analysis imports read-only.
Refuses if a library file (shared\\trackers) changed or is missing.
Usage: python -I -B -X utf8 make_freeze_add_v02.py <n> "<reason>"
"""
import hashlib, json, pathlib, sys, time

W = pathlib.Path(r'ARS_TRIAL\revision_v13\work')
B = W / 'B_retrack'
LOCKS = W / 'locks'
MAN = LOCKS / 'FREEZE_B.json'
FOLDERS = [(B / 'code', '*.py'), (B / 'code', '*.sh'), (B / 'imm2', '*'), (B / 'out' / 'pbar', 'PBAR_*_v01.json'), (B / 'out' / 'b3', '*.json'),
           (B / 'recount_fresh', '*.py'), (B / 'recount_fresh', '*.md')]
FILES = [B / 'B_FRESH_DEFINITIONS_v02.md', B / 'B_ANALYSIS_DEFINITIONS_v01.md', B / 'VENV_FREEZE_B.txt', B / 'RUN_AFTER_LOCK2_B.md']
EXTERNAL = [W / 'CD_capture' / 'analysis' / 'gl_fast_v13.py']


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def key(path):
    p = pathlib.Path(path)
    return str(p if p.is_absolute() else W / p)


def main():
    n = int(sys.argv[1]); reason = sys.argv[2]
    out = LOCKS / ('FREEZE_B_add%d.json' % n)
    if out.exists():
        raise SystemExit('REFUSED: %s exists' % out)
    man = json.loads(MAN.read_text(encoding='utf-8'))
    listed = {}
    for k in ('library', 'pbar', 'b3_tuning', 'package_b_code', 'second_imm', 'definitions'):
        for e in man[k]:
            listed[key(e['path'])] = e['sha256']
    for e in man['record_modules_read_only']:
        listed[key(e['path'])] = e['sha256']
    layers = [dict(file=MAN.name, sha256=sha(MAN))]
    for i in range(1, n):
        a = LOCKS / ('FREEZE_B_add%d.json' % i)
        if not a.exists():
            raise SystemExit('REFUSED: %s missing (layers must be complete)' % a)
        d = json.loads(a.read_text(encoding='utf-8'))
        for e in d['changed'] + d['new']:
            listed[key(e['path'])] = e['sha256']
        layers.append(dict(file=a.name, sha256=sha(a)))
    current = {}
    for p in sorted((W / 'shared' / 'trackers').rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            current[str(p)] = p
    for folder, pat in FOLDERS:
        if folder.exists():
            for p in sorted(folder.glob(pat)):
                if p.is_file():
                    current[str(p)] = p
    for p in FILES:
        current[str(p)] = p
    for path in listed:
        current.setdefault(path, pathlib.Path(path))
    changed = []; new = []; missing = []
    for path, p in sorted(current.items()):
        if not p.exists():
            missing.append(path); continue
        h = sha(p); st = p.stat()
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
    ext = [dict(path=str(p.relative_to(W)), sha256=sha(p), note='package CD file imported read-only by b_fresh_analysis_v02.py')
           for p in EXTERNAL]
    doc = dict(addendum=n, to='work\\locks\\FREEZE_B.json', layers=layers, written=time.strftime('%Y-%m-%d %H:%M:%S %Z'),
               writer='package-B session, Claude Opus 5.5 (claude-opus-5-5)', code='make_freeze_add_v02.py', reason=reason,
               library_unchanged=True, changed=changed, new=new, missing=missing, external_read_only=ext,
               note='Reference = FREEZE_B.json with add1..add%d applied in order; this addendum lists every covered file that changed or is new '
                    'since that state. Earlier manifests are kept as written.' % (n - 1))
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('wrote', out, 'sha256', sha(out))
    print('changed', [e['path'] for e in changed]); print('new', [e['path'] for e in new]); print('missing', missing)


if __name__ == '__main__':
    main()
