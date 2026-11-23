"""Write or verify FREEZE_CD_add13: the A11 Bonferroni check (coordinator's task 5, optional). POST HOC: the rule file and the result were
written seconds apart, after every A11 interval was known; "rule written first" means only that the rule was not changed after the result.
The p-values are normal approximations from the exported intervals (the coordinator asks F for DR2's resample-count p).
New file, 22 Nov 2026 (Claude Opus 5.5, session CD).
Usage: python -I -B make_freeze_add13_v13.py write "APPROVAL TEXT"   |   python -I -B make_freeze_add13_v13.py verify
"""
import json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(CD / 'crossing'))
import make_freeze_x_v13 as FX           # noqa: E402

ADDS = ['a11_bonferroni/BONFERRONI_A11_RULE_v13.md', 'a11_bonferroni/bonferroni_a11_v13.py', 'a11_bonferroni/BONFERRONI_A11_v13.json',
        'l12/make_freeze_add13_v13.py']
USES = ['out/A_EXPORT_X.json', 'out/A_EXPORT_Y.json', '../F_dropout/out/DR_RESULTS_v01.json']
NAME = 'add13'


def write(approval):
    out = FX.LOCKS / f'FREEZE_CD_{NAME}.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    doc = dict(schema='FREEZE_V13_ADDENDUM', addendum_to='work/locks/FREEZE_CD.json (sha256 %s); FREEZE_CD_add12.json (sha256 %s)'
               % (FX.sha(FX.LOCKS / 'FREEZE_CD.json'), FX.sha(FX.LOCKS / 'FREEZE_CD_add12.json')),
               package='C and D (session v13-cd-capture, Claude Opus 5.5)', written=time.strftime('%Y-%m-%d %H:%M %Z'), approval=approval,
               status='POST HOC sensitivity check: rule and result written seconds apart, after every A11 interval was known; p-values are normal '
                      'approximations from the exported intervals; no A11 result changes',
               kind='the A11 Bonferroni check (rule, program, result); no analysis program changed',
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
