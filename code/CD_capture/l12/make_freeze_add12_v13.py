"""Write or verify FREEZE_CD_add12 (after LOCK_A12a): Y on the L12 runs (A12 sec. 3b), done. The A10 sec. 2.6 calibration (seed 1 only: coverage
0.9445 >= 0.94 for both programs), its merged table and chunk manifest, the duplicate-chunk log, both programs' final outputs and their key-by-key
comparison, the YN exports and their comparison, and the round-2 orchestration helpers (l12/orchestration: they move files and start the frozen
programs; no value is computed in them). Replaces: l12/make_export_yn_v13.py (adds YN.p_count_le0 and YN.p_count_finite, coordinator about 03:00).
Note (coordinator 04:58): FREEZE_CD_add11's addendum_to text names add9 where it should name add10; add11 is left unchanged.
New file, 22 Nov 2026 (Claude Opus 5.5, session CD).
Usage: python -I -B make_freeze_add12_v13.py write "APPROVAL TEXT"   |   python -I -B make_freeze_add12_v13.py verify
"""
import json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(CD / 'crossing'))
import make_freeze_x_v13 as FX           # noqa: E402

ORCH = sorted('l12/orchestration/' + p.name for p in (HERE / 'orchestration').glob('*.py'))
ADDS = ORCH + ['analysis/out/calib/y_l12_main.job.npz', 'analysis/out/calib/y_l12_main.meta.json', 'analysis/out/calib/y_l12_main_20261913.npz',
               'analysis/out/calib/MERGE_y_l12_main.json', 'pods/yl12_chunks/CHUNKS_MANIFEST_L12.json', 'pods/yl12_chunks/DUPCHECK_L12.jsonl',
               'ycheck/out/Y_TWIN_L12_v13.json', 'recount/out/RC_Y_TWIN_L12_v13.json', 'ycheck/out/COMPARE_Y_L12_v13.json',
               'out/A_EXPORT_YN.json', 'out/A_RECOUNT_YN.json', 'ycheck/out/COMPARE_YN_EXPORTS_v13.json', 'l12/make_freeze_add12_v13.py']
REPLACES = {'l12/make_export_yn_v13.py': 'adds YN.p_count_le0 and YN.p_count_finite (#finite from each program\'s own output; #{Delta_b <= 0} = '
                                         'p * #finite, integer-checked); the docstring says so. Nothing else changed.'}
USES = ['ycheck/compare_y_v13.py', 'tools/calib_merge_v13.py', 'ycheck/y_twin_l12_v13.py', 'recount/rc_y_twin_l12_v13.py']
NAME = 'add12'


def write(approval):
    out = FX.LOCKS / f'FREEZE_CD_{NAME}.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    a10 = json.loads((FX.LOCKS / 'FREEZE_CD_add10.json').read_text(encoding='utf-8'))
    before = {e['path']: e['sha256'] for e in a10['adds']}
    rep = [dict(path=FX.rel(p), sha256_before=before[FX.rel(p)], sha256_after=FX.sha(CD / p), change=c,
                why='coordinator: "export #{Delta_b <= 0} and #{finite} as keys too (YN.p_count_le0, YN.p_count_finite)"') for p, c in REPLACES.items()]
    doc = dict(schema='FREEZE_V13_ADDENDUM', addendum_to='work/locks/FREEZE_CD.json (sha256 %s); FREEZE_CD_add11.json (sha256 %s)'
               % (FX.sha(FX.LOCKS / 'FREEZE_CD.json'), FX.sha(FX.LOCKS / 'FREEZE_CD_add11.json')),
               package='C and D (session v13-cd-capture, Claude Opus 5.5)', written=time.strftime('%Y-%m-%d %H:%M %Z'), approval=approval,
               after_lock='LOCK_A12a.txt sha256 %s' % FX.sha(FX.REV / 'LOCK_A12a.txt'),
               note_add11='FREEZE_CD_add11 addendum_to names FREEZE_CD_add9; it should name FREEZE_CD_add10 (clerical; left unchanged, coordinator 04:58)',
               kind='Y-L12 results and records; one clerical exporter change; no analysis program changed',
               adds=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in ADDS], uses=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in USES],
               replaces=rep)
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
