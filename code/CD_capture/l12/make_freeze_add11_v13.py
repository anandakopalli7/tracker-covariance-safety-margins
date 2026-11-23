"""Write or verify FREEZE_CD_add11 (after LOCK_A12a): the XH export pair for Supplement S15 (coordinator 22 Nov about 03:05 EST): the clerical
exporter crossing/make_export_xh_v13.py, its two outputs and their key-by-key comparison (50/50 agree; compare rule of crossing/compare_x_v13.py).
New file, 22 Nov 2026 (Claude Opus 5.5, session CD).
Usage: python -I -B make_freeze_add11_v13.py write "APPROVAL TEXT"   |   python -I -B make_freeze_add11_v13.py verify
"""
import json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(CD / 'crossing'))
import make_freeze_x_v13 as FX           # noqa: E402

ADDS = ['crossing/make_export_xh_v13.py', 'out/A_EXPORT_XH.json', 'out/A_RECOUNT_XH.json', 'ycheck/out/COMPARE_XH_EXPORTS_v13.json',
        'l12/make_freeze_add11_v13.py']
USES = ['crossing/out/X_HEADING_v13.json', 'recount/out/RC_X_HEADING_v13.json', 'ycheck/compare_y_v13.py']
NAME = 'add11'


def write(approval):
    out = FX.LOCKS / f'FREEZE_CD_{NAME}.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    doc = dict(schema='FREEZE_V13_ADDENDUM', addendum_to='work/locks/FREEZE_CD.json (sha256 %s); FREEZE_CD_add9.json (sha256 %s)'
               % (FX.sha(FX.LOCKS / 'FREEZE_CD.json'), FX.sha(FX.LOCKS / 'FREEZE_CD_add9.json')),
               package='C and D (session v13-cd-capture, Claude Opus 5.5)', written=time.strftime('%Y-%m-%d %H:%M %Z'),
               approval=approval, after_lock='LOCK_A12a.txt sha256 %s' % FX.sha(FX.REV / 'LOCK_A12a.txt'),
               kind='the XH export pair (clerical) and its comparison; no analysis program changed',
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
