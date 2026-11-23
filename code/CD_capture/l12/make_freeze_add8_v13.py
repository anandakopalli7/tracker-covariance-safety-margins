"""Write or verify FREEZE_CD_add8: the keep_raw-true change of the L12 capture (coordinator, 22 Nov about 00:35 EST, the 10 Hz hedge),
before LOCK_A12a and before any value of a new run; plus the exploratory crossing heading programs (A12 task 4).
Adds: the v02 job lists and their derivation, the logs tool, CD's A12 text v02, the re-run old-run test; the crossing heading programs and
the second program's spec. Replaces (one value each): l_extract_v13.py and l_pods_v13.py now require keep_raw true. Uses (unchanged,
already frozen): C's sealer, re-detector and B7 extractor, the v01 lists. New file, 22 Nov 2026 (Claude Opus 5.5, session CD).
Usage: python -I -B make_freeze_add8_v13.py write "APPROVAL TEXT"   |   python -I -B make_freeze_add8_v13.py verify
"""
import json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(CD / 'crossing'))
import make_freeze_x_v13 as FX           # noqa: E402

ADDS = ['l12/make_jobs_l12_raw_v13.py'] + ['l12/jobs_l12/JOBS_PL12_claude-v13cd-l%d_v02.json' % k for k in range(1, 7)] + \
       ['l12/l_logs_v13.py', 'l12/A12_SECTIONS_2_3b_CD_v02.md', 'l12/out/TESTOLD_L_EXTRACT_20261122T004340.json',
        'crossing/x_heading_v13.py', 'crossing/x_heading_analyse_v13.py', 'recount/SPEC_RC_X_HEADING_v13.md', 'l12/make_freeze_add8_v13.py']
REPLACES = {
    'l12/l_extract_v13.py': ('extract_logs(): the receipt must have keep_raw true (was false); docstring lines 6-10 say so. No other byte changed. '
                             'Old-run test re-run: bit-identical (l12/out/TESTOLD_L_EXTRACT_20261122T004340.json).'),
    'l12/l_pods_v13.py': ('SEAL_PY: the keep_raw check requires true (was false); the seal() docstring says so. No other byte changed. '
                          'Sealing of record is now C\'s tools/seal_extract_v13.py via l12/l_logs_v13.py.'),
}
USES = ['tools/seal_extract_v13.py', 'tools/b7_redetect_v13.py', 'analysis/x_trk_extract_v13.py'] + \
       ['l12/jobs_l12/JOBS_PL12_claude-v13cd-l%d_v01.json' % k for k in range(1, 7)]
NAME = 'add8'
WHY = ('Coordinator 22 Nov about 00:35-00:40 EST: capture the new runs with keep_raw = TRUE, sweeps on pod-local disk only, logs and receipts '
       'downloaded as planned (a second configuration, 10 Hz with 0.1 s latency, may be assessed). The add7 programs required keep_raw false.')


def write(approval):
    out = FX.LOCKS / f'FREEZE_CD_{NAME}.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    if (FX.REV / 'LOCK_A12a.txt').exists(): raise SystemExit('REFUSED: LOCK_A12a.txt exists; add8 must precede it')
    a7 = json.loads((FX.LOCKS / 'FREEZE_CD_add7.json').read_text(encoding='utf-8'))
    before = {e['path']: e['sha256'] for e in a7['adds']}
    rep = [dict(path=FX.rel(p), sha256_before=before[FX.rel(p)], sha256_after=FX.sha(CD / p), change=c, why=WHY) for p, c in REPLACES.items()]
    doc = dict(schema='FREEZE_V13_ADDENDUM', addendum_to='work/locks/FREEZE_CD.json (sha256 %s); FREEZE_CD_add7.json (sha256 %s)'
               % (FX.sha(FX.LOCKS / 'FREEZE_CD.json'), FX.sha(FX.LOCKS / 'FREEZE_CD_add7.json')),
               package='C and D (session v13-cd-capture, Claude Opus 5.5)', written=time.strftime('%Y-%m-%d %H:%M %Z'), approval=approval,
               kind=('keep_raw-true change of the L12 capture (A12 sec. 2.2), before LOCK_A12a and before any value of a new run; and the '
                     'exploratory crossing heading programs (A12 task 4; their test on two X runs, pc13x 0002/0008, was seen)'),
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
