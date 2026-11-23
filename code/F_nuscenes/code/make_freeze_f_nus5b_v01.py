"""Revision v13, AMENDMENT_12 sec. 5b: FREEZE_F_NUS5B, the SHA-256 manifest of the real-log dropout decision test (package F's worker,
work\\F_dropout_nus) before LOCK_A12e. New file, 22 Nov 2026 (Claude Opus 5.5, session F). Entries {group, path, sha256}, paths relative
to revision_v13. Refuses to overwrite. Groups:
  spec       A12_5b_TEXT_v01.md (the sec. 5b text, with the coordinator's decision paragraph)
  code       every file in F_dropout_nus\\code (programs, the masked-run script, the pod tools, the val order), no __pycache__
  masks      masks\\FN5B_MASKS_v01.json
  acceptance out\\ACCEPT1_TRACKS_v01.json, ACCEPT2_ARRAYS_v01.json, ACCEPT3_SCORED_v01.json, HASH_*.json (masks off; F's unmasked val
             values of record reproduced; no masked value)
  codetest   out\\masked_train\\*, out\\masked_train12\\* (the masked chain on TRAIN scenes only: code tests, not evidence)
It also checks every SHA-256 that the text's own table lists against the file, and prints any difference.
Usage: python -I make_freeze_f_nus5b_v01.py   -> work\\locks\\FREEZE_F_NUS5B.json
"""
import hashlib, json, pathlib, re, time
V13 = pathlib.Path(__file__).resolve().parents[3]
N = V13 / 'work' / 'F_dropout_nus'
OUTF = V13 / 'work' / 'locks' / 'FREEZE_F_NUS5B.json'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)
    groups = {
        'spec': [N / 'A12_5b_TEXT_v01.md'],
        'code': sorted(p for p in (N / 'code').iterdir() if p.is_file()),
        'masks': [N / 'masks' / 'FN5B_MASKS_v01.json'],
        'acceptance': sorted(p for p in (N / 'out').iterdir() if p.is_file()),
        'codetest': sorted(p for d in ('masked_train', 'masked_train12') for p in (N / 'out' / d).iterdir() if p.is_file()),
    }
    entries = [dict(group=g, path=str(f.resolve().relative_to(V13)), sha256=sha(f)) for g, fs in groups.items() for f in fs]
    # the text's own table: rows "| ... | `ARS_TRIAL\revision_v13\<path>` | `<sha>` |"
    txt = (N / 'A12_5b_TEXT_v01.md').read_text(encoding='utf-8')
    have = {e['path']: e['sha256'] for e in entries}
    diffs = []
    for m in re.finditer(r'`ARS_TRIAL\\revision_v13\\([^`]+)`\s*\|\s*`([0-9a-f]{64})`', txt):
        p, h = m.group(1), m.group(2)
        f = V13 / p
        cur = sha(f) if f.is_file() else None
        if cur != h: diffs.append(dict(path=p, text=h, now=cur))
    doc = dict(name='FREEZE_F_NUS5B', amendment='AMENDMENT_12 sec. 5b', written=time.strftime('%Y-%m-%d %H:%M:%S'),
               writer='session F (Claude Opus 5.5)', n=len(entries), text_table_differences=diffs, entries=entries)
    OUTF.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('groups', {g: len(fs) for g, fs in groups.items()})
    print('text table differences:', json.dumps(diffs, indent=0) if diffs else 'none')
    print('FREEZE_F_NUS5B', len(entries), 'entries', sha(OUTF))


if __name__ == '__main__':
    main()
