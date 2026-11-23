"""Write or verify FREEZE_CD_add4 for Y (AMENDMENT_11_v13.md sec. 6b): adds files only (no frozen file changed), with the SHA-256 of
the already-frozen files Y uses unchanged. New file, 21 Nov 2026 (Claude Opus 5.5, session CD). Uses crossing\\make_freeze_x_v13.py's
helpers (frozen in FREEZE_CD_add3, imported unchanged).
Usage: python -I -B make_freeze_y_v13.py write "APPROVAL TEXT"   |   python -I -B make_freeze_y_v13.py verify
"""
import json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(CD / 'crossing'))
import make_freeze_x_v13 as FX           # noqa: E402

OWN = ['ycheck/CD_DEFINITIONS_Y_v13.md', 'ycheck/y_twin_v13.py', 'ycheck/y_calib_remote_v13.py', 'ycheck/compare_y_v13.py', 'ycheck/make_freeze_y_v13.py']
SECOND = sorted(str(p.relative_to(CD)).replace('\\', '/') for p in (CD / 'recount').glob('rc_y_*.py')) + ['recount/README_RECOUNT_Y.md']
USES = ['analysis/cd_common_v13.py', 'analysis/gl_fast_v13.py', 'analysis/calib_remote_v13.py', 'tools/calib_pods_v13.py', 'tools/calib_merge_v13.py',
        'tools/calib_worker_v13.sh', 'recount/rc_core_v13.py', 'recount/rc_kern_v13.py', 'recount/rc_calib_remote_v13.py',
        '../shared/trackers/trk_score_v01.py', '../shared/trackers/trk_env_v01.py', '../locks/FREEZE_B_add7.json']
NAME = 'add4'


def write(approval):
    out = FX.LOCKS / f'FREEZE_CD_{NAME}.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    doc = dict(schema='FREEZE_V13_ADDENDUM', addendum_to='work/locks/FREEZE_CD.json (sha256 %s)' % FX.sha(FX.LOCKS / 'FREEZE_CD.json'),
               package='C and D (session v13-cd-capture, Claude Opus 5.5)', written=time.strftime('%Y-%m-%d %H:%M %Z'), approval=approval,
               kind='adds files for Y (AMENDMENT_11_v13.md sec. 6b), before LOCK_A11 and before any Y value; no frozen file changed',
               adds=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in OWN + SECOND],
               uses=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in USES], replaces=[])
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(out.name, FX.sha(out), '| adds', len(doc['adds']), [a['path'].split('\\')[-1] for a in doc['adds']], '| uses', len(doc['uses']))


if __name__ == '__main__':
    if sys.argv[1] == 'write': write(sys.argv[2])
    else: FX.verify(NAME)
