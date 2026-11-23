"""Revision v13, AMENDMENT_12 sec. 3a: FREEZE_DR_A12, the SHA-256 manifest of what DR's replication on the new runs adds to FREEZE_DR
(layered: verify with work\\shared\\tools\\verify_freeze.py --layered FREEZE_DR.json FREEZE_DR_A12.json). New file, 22 Nov 2026 (Claude
Opus 5.5, session F). Entries {group, path, sha256}, paths relative to revision_v13. Refuses to overwrite.
Groups: spec (the sec. 3a text), code (the new and changed F_dropout\\code files), recount (the second program and its test output),
tests (the pre-lock pod test outputs on the 35 old runs and the two programs' comparison), records (DR's records note).
Usage: python -I make_freeze_dr_a12_v01.py   -> work\\locks\\FREEZE_DR_A12.json
"""
import hashlib, json, pathlib, time
HERE = pathlib.Path(__file__).resolve().parent
DRD = HERE.parent
WORK = DRD.parent
V13 = WORK.parent
OUTF = WORK / 'locks' / 'FREEZE_DR_A12.json'
NEW_CODE = ['dr_masks_v03.py', 'dr_masks_v04.py', 'dr_extract_v02.py', 'dr_analysis_v02.py', 'dr_dose_v01.py', 'dr_slope_remote_v01.py',
            'dr_pods_v02.py', 'dr_identity_v02.py', 'dr_pod_a12_test_v01.sh', 'dr_pod_a12_test2_v01.sh', 'dr_pod_a12_postlock_v01.sh', 'make_freeze_dr_a12_v01.py']


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF)
    groups = {
        'spec': [DRD / 'A12_3a_DR_REPLICATION_v02.md', DRD / 'A12_3a_DR_REPLICATION_v01.md'],
        'code': [DRD / 'code' / f for f in NEW_CODE],
        'recount': [DRD / 'recount' / 'dr_recount_a12_v01.py', DRD / 'recount' / 'TESTOLD_DR2_RECOUNT_v01.json'],
        'tests': [DRD / 'out_a12' / 'testold_p010' / 'TESTOLD_DR2_RESULTS_v01.json', DRD / 'out_a12' / 'TESTOLD_DR2_DOSE_v01.json',
                  DRD / 'out_a12' / 'TESTOLD_DR2_FIRST_MERGED_v01.json', DRD / 'out_a12' / 'DR2_COMPARE_TESTOLD_v01.json'],
        'records': [DRD / 'notes' / 'DR_A12_RECORDS_v01.md'],
    }
    entries = []; missing = []
    for g, fs in groups.items():
        for f in fs:
            if pathlib.Path(f).is_file():
                entries.append(dict(group=g, path=str(pathlib.Path(f).resolve().relative_to(V13)), sha256=sha(f)))
            else:
                missing.append(str(f))
    if missing: raise SystemExit('REFUSED: missing %s' % missing)
    doc = dict(name='FREEZE_DR_A12', layered_on='work\\locks\\FREEZE_DR.json', amendment='AMENDMENT_12 sec. 3a',
               written=time.strftime('%Y-%m-%d %H:%M:%S'), writer='session F (Claude Opus 5.5)', n=len(entries), entries=entries)
    OUTF.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('FREEZE_DR_A12', len(entries), 'entries', sha(OUTF))


if __name__ == '__main__':
    main()
