r"""v13 round 2: a data-only FREEZE_B addendum from a manifest written by b_l12_retrack_v01.py (one list arrays_<X>_l12 of {path,
sha256, bytes}), in the form of FREEZE_B_add7 (data-only layer read by make_freeze_add_v03/v04). New file, 22 Nov 2026 (Claude Opus 5.5).
Every file is re-hashed here before writing; REFUSED on any mismatch or if the addendum exists.
Usage: python -I -B -X utf8 make_freeze_data_v01.py <n> <manifest json> "<reason>"
"""
import hashlib, json, pathlib, sys, time

W = pathlib.Path(r'ARS_TRIAL\revision_v13\work')
LOCKS = W / 'locks'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    n = int(sys.argv[1]); mf = pathlib.Path(sys.argv[2]); reason = sys.argv[3]
    out = LOCKS / ('FREEZE_B_add%d.json' % n)
    if out.exists():
        raise SystemExit('REFUSED: %s exists' % out)
    for i in range(1, n):
        if not (LOCKS / ('FREEZE_B_add%d.json' % i)).exists():
            raise SystemExit('REFUSED: add%d missing' % i)
    m = json.loads(mf.read_text(encoding='utf-8'))
    keys = [k for k, v in m.items() if k.startswith('arrays_') and isinstance(v, list)]
    if len(keys) != 1:
        raise SystemExit('REFUSED: the manifest must hold exactly one arrays_* list')
    lst = m[keys[0]]
    bad = [e['path'] for e in lst if sha(W / e['path']) != e['sha256']]
    if bad:
        raise SystemExit('REFUSED: %d files differ from the manifest: %s' % (len(bad), bad[:3]))
    layers = [dict(file='FREEZE_B.json', sha256=sha(LOCKS / 'FREEZE_B.json'))] + [
        dict(file='FREEZE_B_add%d.json' % i, sha256=sha(LOCKS / ('FREEZE_B_add%d.json' % i))) for i in range(1, n)]
    doc = {'addendum': n, 'to': 'work\\locks\\FREEZE_B.json', 'layers': layers, 'kind': 'data-only',
           'written': time.strftime('%Y-%m-%d %H:%M:%S %Z'), 'writer': 'package-B session, Claude Opus 5.5 (claude-opus-5-5)',
           'code': 'make_freeze_data_v01.py', 'reason': reason, 'manifest': str(mf.relative_to(W)), 'manifest_sha256': sha(mf),
           'n_files': len(lst), keys[0]: lst}
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('wrote', out.name, 'sha256', sha(out), '|', len(lst), 'files re-hashed OK')


if __name__ == '__main__':
    main()
