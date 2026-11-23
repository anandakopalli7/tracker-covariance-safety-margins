"""Write or verify FREEZE_CD_add9 (after LOCK_A12a, before any value of a new run is computed or any new-run file is moved by these tools):
the 10 Hz option's L12 tools (coordinator's GO, 22 Nov about 00:55 EST) and the job-to-folder map shape B and F read.
Adds: l12/remote_l12_after_capture.sh (C's frozen sealer then C's frozen B7 re-detector on each pod after capture); l12/l_trk_extract_v13.py
(copy of C's analysis/x_trk_extract_v13.py: L12 run list, LOCK_A12a gate, output root arrays_l12; its old-run test equals C's accepted
arrays on all 45 keys); that test's output. Replaces: l12/l_logs_v13.py (map "runs" = {job: rid} as B and F asked; new fetch-b7 command).
New file, 22 Nov 2026 (Claude Opus 5.5, session CD).
Usage: python -I -B make_freeze_add9_v13.py write "APPROVAL TEXT"   |   python -I -B make_freeze_add9_v13.py verify
"""
import json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(CD / 'crossing'))
import make_freeze_x_v13 as FX           # noqa: E402

ADDS = ['l12/remote_l12_after_capture.sh', 'l12/l_trk_extract_v13.py', 'l12/out/testold_lb7/TESTOLD_LB7_v13_extract_20261122T005230.json',
        'l12/out/testold_lb7/p1b_fit_finite_0037.npz', 'l12/make_freeze_add9_v13.py']
REPLACES = {
    'l12/l_logs_v13.py': ('runs_map(): "runs" is now {job id: rid} (was a list of rows), plus "missing" and "detail" (the rows); new command '
                          'fetch-b7 (download finished B7 re-detections into b7/<rid>/, checked against their manifests and the laptop '
                          'receipts). seal and fetch unchanged.'),
}
USES = ['analysis/x_trk_extract_v13.py', 'tools/b7_redetect_v13.py', 'tools/seal_extract_v13.py', 'tools/remote_b7_and_seal.sh',
        'analysis/out/testold_b7_arrays_final/B7_10_0.1/p1b_fit_finite_0037.npz']
NAME = 'add9'


def write(approval):
    out = FX.LOCKS / f'FREEZE_CD_{NAME}.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    a8 = json.loads((FX.LOCKS / 'FREEZE_CD_add8.json').read_text(encoding='utf-8'))
    before = {e['path']: e['sha256'] for e in a8['adds']}
    rep = [dict(path=FX.rel(p), sha256_before=before[FX.rel(p)], sha256_after=FX.sha(CD / p), change=c,
                why='B and F read the map as {"runs": {job: rid}} (their messages of 22 Nov about 00:45); the 10 Hz option (coordinator GO).')
           for p, c in REPLACES.items()]
    lock = FX.REV / 'LOCK_A12a.txt'
    doc = dict(schema='FREEZE_V13_ADDENDUM', addendum_to='work/locks/FREEZE_CD.json (sha256 %s); FREEZE_CD_add8.json (sha256 %s)'
               % (FX.sha(FX.LOCKS / 'FREEZE_CD.json'), FX.sha(FX.LOCKS / 'FREEZE_CD_add8.json')),
               package='C and D (session v13-cd-capture, Claude Opus 5.5)', written=time.strftime('%Y-%m-%d %H:%M %Z'), approval=approval,
               after_lock='LOCK_A12a.txt sha256 %s exists; no value of a new run has been computed and no new-run file has been moved by these tools'
               % FX.sha(lock),
               kind='adds the 10 Hz option tools (A12 sec. 2.2/2.5) and changes the map shape; no analysis program changed',
               adds=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in ADDS],
               uses=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in USES], replaces=rep)
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(out.name, FX.sha(out), '| adds', len(doc['adds']), '| uses', len(doc['uses']), '| replaces', len(rep))


def verify():
    d = json.loads((FX.LOCKS / f'FREEZE_CD_{NAME}.json').read_text(encoding='utf-8'))
    bad = [e['path'] for e in d['adds'] + d['uses'] if FX.sha(FX.REV.parent / e['path']) != e['sha256']]
    bad += [e['path'] for e in d['replaces'] if FX.sha(FX.REV.parent / e['path']) != e['sha256_after']]
    print(json.dumps(dict(addendum=NAME, adds=len(d['adds']), uses=len(d['uses']), replaces=len(d['replaces']), changed=bad)))


if __name__ == '__main__':
    if sys.argv[1] == 'write': write(sys.argv[2])
    else: verify()
