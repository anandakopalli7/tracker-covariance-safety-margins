"""Revision v13, AMENDMENT_11 sec. 6c.9: FREEZE_DR, the SHA-256 manifest of everything DR fixes before LOCK_A11c. New file, 21 Nov 2026
(Claude Opus 5.5, session F). Entries {group, path, sha256} with paths relative to revision_v13 (as FREEZE_F; checked by
work\\shared\\tools\\verify_freeze.py). Refuses to overwrite.
Groups: spec (the §6c text F drafted), code (F_dropout\\code\\*.py, *.json), masks, recount (the second program and its test output),
identity (DR_IDENTITY_v01.json and the pod record), libraries (the frozen files DR imports: shared trackers, CD's cd_common / gl_fast /
calib_remote / calib_merge, the codex tracker config, P's scoring library and run index), tests (test-old outputs).
Usage: python -I make_freeze_dr_v01.py   -> work\\locks\\FREEZE_DR.json
"""
import hashlib, json, pathlib, time
HERE = pathlib.Path(__file__).resolve().parent
DRD = HERE.parent
WORK = DRD.parent
V13 = WORK.parent
DL = pathlib.Path(r'<user folder>')
P = DL / '<earlier-phase folder 1>'
CODEX = DL / '<earlier-phase folder 2>' / '149_supported_sensor_preparation_20261101'
OUTF = WORK / 'locks' / 'FREEZE_DR.json'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def rel(p):
    p = pathlib.Path(p).resolve()
    try:
        return str(p.relative_to(V13))
    except ValueError:
        return str(p)


def main():
    if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)
    groups = {
        'spec': [DRD / 'A11_6c_DROPOUT_SPEC_v04.md', DRD / 'A11_6c_DROPOUT_SPEC_v03.md', DRD / 'A11_6c_DROPOUT_SPEC_v02.md',
                 DRD / 'A11_6c_DROPOUT_SPEC_v01.md'],          # AMENDMENT_11 itself is hashed by the coordinator's LOCK_A11c
        'notes': [DRD / 'notes' / 'DR_RECORDS_v01.md'],
        'code': sorted(p for p in (DRD / 'code').iterdir() if p.is_file() and p.suffix in ('.py', '.json', '.sh')),
        'masks': [DRD / 'masks' / 'DR_MASKS_v02.json', DRD / 'masks' / 'DR_MASKS_v01.json'],
        'recount': sorted(p for p in (DRD / 'recount').rglob('*') if p.is_file() and p.suffix in ('.py', '.json', '.md')
                          and '__pycache__' not in p.parts),
        'identity': [p for p in [DRD / 'out' / 'DR_IDENTITY_v01.json'] if p.is_file()],
        'libraries': sorted(p for p in (WORK / 'shared' / 'trackers').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
                     + [WORK / 'CD_capture' / 'analysis' / f for f in ('cd_common_v13.py', 'gl_fast_v13.py', 'calib_remote_v13.py')]
                     + [WORK / 'CD_capture' / 'tools' / 'calib_merge_v13.py', WORK / 'CD_capture' / 'CASES_C_v13.json',
                        WORK / 'CD_capture' / 'REPLACEMENTS_C_v13.json', CODEX / 'contracts' / 'tracker_config.json',
                        P / '11_ojits' / 'A6R' / 'code' / 'optA_lib_v02.py', P / '09_redesign' / 'm4_perception_model' / 'run_index_m4_v02.csv',
                        P / '09_redesign' / 'm2_decisions' / 'openloop' / 'pbar_tuning_v01.json'],
        'tests': sorted(DRD.glob('out/TESTOLD_*.json')) + sorted(DRD.glob('out/testold/*.json'))
                 + sorted(DRD.glob('out/DR_COMPARE_TESTOLD*.json')),
    }
    entries = []
    for g, fs in groups.items():
        for f in fs:
            if pathlib.Path(f).is_file():
                entries.append(dict(group=g, path=rel(f), sha256=sha(f)))
    doc = dict(name='FREEZE_DR', amendment='AMENDMENT_11 sec. 6c.9', written=time.strftime('%Y-%m-%d %H:%M:%S'),
               writer='session F (Claude Opus 5.5)', punish_num=json.loads((DRD / 'code' / 'DR_CONFIG_v01.json').read_text(encoding='utf-8'))['punish_num'],
               n=len(entries), entries=entries)
    OUTF.parent.mkdir(parents=True, exist_ok=True)
    OUTF.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('FREEZE_DR', len(entries), 'entries', sha(OUTF))


if __name__ == '__main__':
    main()
