"""Write or verify FREEZE_CD_add10 (after LOCK_A12a): files written since add9, before the Y-L12 exports and before any heading value is printed.
Adds: ycheck/y_pods_l12_v13.py (copy of ycheck/y_pods_v13.py for Y on the L12 runs: run list, B2 folder and manifest, CV0 folder, LOCK_A12a,
the L12 programs; orchestration only); l12/make_export_yn_v13.py (clerical YN.* export for A); recount/rc_x_heading_v13.py (Claude Sonnet 5.5's
second program for the exploratory crossing heading analysis, written from recount/SPEC_RC_X_HEADING_v13.md before any heading value existed)
and crossing/compare_x_heading_v13.py; the heading outputs and their comparison (83/83 agree). No analysis program of record changed.
New file, 22 Nov 2026 (Claude Opus 5.5, session CD).
Usage: python -I -B make_freeze_add10_v13.py write "APPROVAL TEXT"   |   python -I -B make_freeze_add10_v13.py verify
"""
import json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(CD / 'crossing'))
import make_freeze_x_v13 as FX           # noqa: E402

ADDS = ['ycheck/y_pods_l12_v13.py', 'l12/make_export_yn_v13.py', 'recount/rc_x_heading_v13.py', 'crossing/compare_x_heading_v13.py',
        'crossing/out/X_HEADING_v13.json', 'recount/out/RC_X_HEADING_v13.json', 'crossing/out/COMPARE_X_HEADING_v13.json',
        'l12/out/L12_RUNS_v13.json', 'l12/make_freeze_add10_v13.py']
USES = ['ycheck/y_pods_v13.py', 'crossing/make_export_xy_v13.py', 'ycheck/calib_capture_pods_v13.py', 'tools/calib_merge_v13.py',
        'tools/calib_worker_v13.sh', 'ycheck/y_calib_remote_v13.py', 'recount/rc_y_calib_remote_v13.py']
NAME = 'add10'


def write(approval):
    out = FX.LOCKS / f'FREEZE_CD_{NAME}.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    doc = dict(schema='FREEZE_V13_ADDENDUM', addendum_to='work/locks/FREEZE_CD.json (sha256 %s); FREEZE_CD_add9.json (sha256 %s)'
               % (FX.sha(FX.LOCKS / 'FREEZE_CD.json'), FX.sha(FX.LOCKS / 'FREEZE_CD_add9.json')),
               package='C and D (session v13-cd-capture, Claude Opus 5.5); rc_x_heading by Claude Sonnet 5.5', written=time.strftime('%Y-%m-%d %H:%M %Z'),
               approval=approval, after_lock='LOCK_A12a.txt sha256 %s' % FX.sha(FX.REV / 'LOCK_A12a.txt'),
               kind='orchestration (Y-L12 on a pod), a clerical exporter, the exploratory heading second program and its outputs; no analysis program of record changed',
               adds=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in ADDS], uses=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in USES], replaces=[])
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(out.name, FX.sha(out), '| adds', len(doc['adds']), '| uses', len(doc['uses']))


def verify():
    d = json.loads((FX.LOCKS / f'FREEZE_CD_{NAME}.json').read_text(encoding='utf-8'))
    bad = [e['path'] for e in d['adds'] + d['uses'] if FX.sha(FX.REV.parent / e['path']) != e['sha256']]
    print(json.dumps(dict(addendum=NAME, adds=len(d['adds']), uses=len(d['uses']), changed=bad)))


if __name__ == '__main__':
    if sys.argv[1] == 'write': write(sys.argv[2])
    else: verify()
