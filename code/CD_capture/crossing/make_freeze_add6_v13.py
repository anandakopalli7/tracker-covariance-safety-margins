"""Write or verify FREEZE_CD_add6: X's replacement record and job lists, and the tools written after add5 (reserve jobs, the X run on a pod,
the exporter for A). Adds files only; no value is computed in them (the exporter maps outputs; RR_N.dec = RR_N * R.dec for the second
program). New file, 21 Nov 2026 (Claude Opus 5.5, session CD). Uses crossing\\make_freeze_x_v13.py's helpers (frozen in add3).
Usage: python -I -B make_freeze_add6_v13.py write "APPROVAL TEXT"   |   python -I -B make_freeze_add6_v13.py verify
"""
import json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(HERE))
import make_freeze_x_v13 as FX           # noqa: E402

ADDS = ['crossing/REPLACEMENTS_X_v13.json', 'crossing/make_reserve_jobs_x_v13.py', 'crossing/jobs_x/JOBS_PX13_claude-v13cd-x6_v02.json',
        'crossing/jobs_x/JOBS_PX13_claude-v13cd-x6_v03.json', 'crossing/x_run_pods_v13.py', 'crossing/make_export_xy_v13.py',
        'crossing/alias_retries_x_v13.py', 'crossing/out/ALIAS_RETRIES_X_v13.json', 'crossing/DEVIATIONS_X_v13.json',
        'crossing/make_freeze_add6_v13.py']
NAME = 'add6'


def write(approval):
    out = FX.LOCKS / f'FREEZE_CD_{NAME}.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    doc = dict(schema='FREEZE_V13_ADDENDUM', addendum_to='work/locks/FREEZE_CD.json (sha256 %s)' % FX.sha(FX.LOCKS / 'FREEZE_CD.json'),
               package='C and D (session v13-cd-capture, Claude Opus 5.5)', written=time.strftime('%Y-%m-%d %H:%M %Z'), approval=approval,
               kind='adds files: X replacements (A11 sec. 3.2) and orchestration/export tools, before the X analysis of record; no frozen file changed',
               adds=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in ADDS], uses=[], replaces=[])
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(out.name, FX.sha(out), '| adds', len(doc['adds']))


if __name__ == '__main__':
    if sys.argv[1] == 'write': write(sys.argv[2])
    else: FX.verify(NAME)
