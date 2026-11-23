"""Write or verify FREEZE_CD_add5: X's A11 sec. 3.6 descriptive programs (first and second) and the orchestration tools written after
add3/add4 (they move files and start frozen programs; no value is computed in them). Adds files only. New file, 21 Nov 2026 (Claude
Opus 5.5, session CD). Uses crossing\\make_freeze_x_v13.py's helpers (frozen in add3, imported unchanged).
Usage: python -I -B make_freeze_add5_v13.py write "APPROVAL TEXT"   |   python -I -B make_freeze_add5_v13.py verify
"""
import json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(HERE))
import make_freeze_x_v13 as FX           # noqa: E402

ADDS = ['crossing/CD_DEFINITIONS_X_DESC_v13.md', 'crossing/x_desc_v13.py', 'recount/rc_x_desc_v13.py', 'recount/README_RECOUNT_X_DESC.md',
        'crossing/x_extract_loop_v13.py', 'ycheck/y_pods_v13.py', 'ycheck/calib_capture_pods_v13.py', 'crossing/make_freeze_add5_v13.py']
USES = ['analysis/cd_common_v13.py', 'analysis/gl_fast_v13.py', 'recount/rc_core_v13.py', 'recount/rc_kern_v13.py', 'recount/rc_x_cross_v13.py',
        'recount/rc_s57a_v13.py', 'recount/rc_s57b_v13.py', 'tools/calib_worker_v13.sh', 'tools/b7_pods_v13.py', 'tools/pods_v13.py',
        '../shared/trackers/trk_score_v01.py', '../shared/trackers/trk_env_v01.py']
NAME = 'add5'


def write(approval):
    out = FX.LOCKS / f'FREEZE_CD_{NAME}.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    doc = dict(schema='FREEZE_V13_ADDENDUM', addendum_to='work/locks/FREEZE_CD.json (sha256 %s)' % FX.sha(FX.LOCKS / 'FREEZE_CD.json'),
               package='C and D (session v13-cd-capture, Claude Opus 5.5)', written=time.strftime('%Y-%m-%d %H:%M %Z'), approval=approval,
               kind='adds files: X sec. 3.6 descriptives (A11), after LOCK_A11 and before their first fresh run; orchestration tools; no frozen file changed',
               adds=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in ADDS],
               uses=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in USES], replaces=[])
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(out.name, FX.sha(out), '| adds', len(doc['adds']), '| uses', len(doc['uses']))


if __name__ == '__main__':
    if sys.argv[1] == 'write': write(sys.argv[2])
    else: FX.verify(NAME)
