"""Write work\\locks\\FREEZE_E.json: the SHA-256 of every file of package E's frozen build (README_COORDINATION rule 3; A10 4:
'the E packet and arms'). Never overwrites.

python -I freeze_e_v01.py --packet packet_e_v02 [--note TEXT]
Lists: src\\** (the packet overlay), the packet tar and receipt, tools\\*.py|*.sh, analysis\\*.py, tests\\*.py and tests\\out\\*.json,
jobs\\*.json, review\\*.md, recount\\*.py|*.md, STATUS.md. Excludes __pycache__, runs\\, packets\\dev_*.
"""
import argparse, datetime, hashlib, json, pathlib

E = pathlib.Path(__file__).resolve().parents[1]
LOCKS = E.parent / 'locks'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 * 1024 ** 2), b''): h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--packet', required=True, action='append'); ap.add_argument('--note', default='')
    a = ap.parse_args()
    out = LOCKS / 'FREEZE_E.json'
    assert not out.exists(), 'FREEZE_E.json exists; never overwrite (write a new version by hand-named file if a fix is needed)'
    groups = {
        'src': [p for p in (E / 'src').rglob('*') if p.is_file()],
        'packet': [f for pk in a.packet for f in (E / 'packets' / f'{pk}.tar.gz', E / 'packets' / f'{pk}_RECEIPT.json')],
        'out': [p for p in (E / 'out').glob('*') if p.suffix in ('.json', '.txt', '.md')],
        'tools': [p for p in (E / 'tools').glob('*') if p.suffix in ('.py', '.sh') or p.name == 'runpodctl.exe'],
        'analysis': list((E / 'analysis').glob('*.py')),
        'tests': list((E / 'tests').glob('*.py')) + list((E / 'tests' / 'out').glob('*.json')),
        'jobs': list((E / 'jobs').glob('*.json')),
        'review': list((E / 'review').glob('*.md')),
        'recount': ([p for p in (E / 'recount').glob('*') if p.suffix in ('.py', '.md')] + list((E / 'recount' / 'out').glob('*.json'))) if (E / 'recount').exists() else [],
        'lock': [E.parent / 'locks' / 'LOCK_A10_2b.txt', E.parent / 'locks' / 'LOCK_A10_2b_NOTE_v01.txt'],
        'status': [E / 'STATUS.md'],
    }
    files = []
    for g, ps in groups.items():
        for p in sorted(ps):
            if '__pycache__' in p.parts: continue
            assert p.exists(), p
            files.append(dict(group=g, path=str(p.relative_to(E.parent)).replace('\\', '/'), bytes=p.stat().st_size, sha256=sha(p)))
    doc = dict(schema='FREEZE_V13', package='E', session='E (Claude Opus 5.5)', written=datetime.datetime.now().astimezone().isoformat(),
               packet=a.packet, note=a.note, files=files)
    LOCKS.mkdir(exist_ok=True)
    with open(out, 'x', encoding='utf-8', newline='\n') as f: f.write(json.dumps(doc, indent=1) + '\n')
    print(out, len(files), 'files; sha256', sha(out))


if __name__ == '__main__':
    main()
