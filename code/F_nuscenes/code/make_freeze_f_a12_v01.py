"""Revision v13, AMENDMENT_12 sec. 5: FREEZE_F_A12, the SHA-256 manifest of the real-sensor mechanism check before LOCK_A12c. New file,
22 Nov 2026 (Claude Opus 5.5, session F). Entries {group, path, sha256}, paths relative to revision_v13 (verify_freeze.py). Refuses to
overwrite. Groups: spec (the sec. 5 text), code (f21_mech_v01.py, this script), recount (the second program fm_recount_v01.py and its
train-subset outputs), design (the train design outputs and the agreement check on the first 50 train scenes).
Usage: python -I make_freeze_f_a12_v01.py   -> work\\locks\\FREEZE_F_A12.json
"""
import hashlib, json, pathlib, time
HERE = pathlib.Path(__file__).resolve().parent
F = HERE.parent
V13 = F.parent.parent
OUTF = V13 / 'work' / 'locks' / 'FREEZE_F_A12.json'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)
    groups = {
        'spec': sorted((F / 'notes').glob('A12_5_MECH_v0*.md')),
        'code': [HERE / 'f21_mech_v01.py', HERE / 'f21_mech_v02.py', HERE / 'f21_design_from_rows_v02.py', HERE / 'make_freeze_f_a12_v01.py'],
        'recount': sorted(p for p in (F / 'recount_mech').glob('*') if p.is_file() and p.suffix in ('.py', '.json')),
        'design': sorted(p for p in (F / 'out' / 'mech').glob('*') if p.is_file()),
        'design_v02': sorted(p for p in (F / 'out' / 'mech_v02').glob('*') if p.is_file()),
        'rehearsal': sorted(p for p in (F / 'out' / 'mech_rehearsal_train50').glob('*') if p.is_file())
                     + sorted(p for p in (F / 'out' / 'mech_rehearsal_train50_v02').glob('*') if p.is_file()),
        'pod': [HERE / 'f21_pod_run_v01.sh', HERE / 'f21_pod_run_v02.sh'],
    }
    entries = [dict(group=g, path=str(pathlib.Path(f).resolve().relative_to(V13)), sha256=sha(f)) for g, fs in groups.items() for f in fs]
    doc = dict(name='FREEZE_F_A12', amendment='AMENDMENT_12 sec. 5', written=time.strftime('%Y-%m-%d %H:%M:%S'),
               writer='session F (Claude Opus 5.5)', n=len(entries), entries=entries)
    OUTF.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('FREEZE_F_A12', len(entries), 'entries', sha(OUTF))


if __name__ == '__main__':
    main()
