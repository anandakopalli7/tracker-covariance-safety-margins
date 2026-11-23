"""Write or verify FREEZE_CD_add7: the A12 sec. 2 / sec. 3b files of session CD, before LOCK_A12a and before any value of a new run.

The case list, its generator, the L12 packet and its jobs; the L12 CV0 extractor and its pod tool; the Y programs for the new runs (first
and second, copies of the add4 programs with only the run list, folders, gate, output name and the one-sided p-value changed); their
old-run tests; CD's A12 section text. Adds files only. The 'uses' entries are files already frozen (add3/add4 or FREEZE_CD) that these
programs import unchanged; verify re-hashes them too. New file, 22 Nov 2026 (Claude Opus 5.5, session CD). Uses
crossing/make_freeze_x_v13.py's helpers (frozen in add3).
Usage: python -I -B make_freeze_add7_v13.py write "APPROVAL TEXT"   |   python -I -B make_freeze_add7_v13.py verify
"""
import json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(CD / 'crossing'))
import make_freeze_x_v13 as FX           # noqa: E402

ADDS = ['l12/make_cases_l12_v13.py', 'l12/CASES_L12_v13.json', 'l12/DEVELOPMENT_PROTOCOL_L12_v13.json', 'l12/build_packet_l12_v13.py',
        'packets/packet_l12_v13.tar.gz', 'packets/packet_l12_v13_RECEIPT.json', 'l12/make_jobs_l12_v13.py'] + \
       ['l12/jobs_l12/JOBS_PL12_claude-v13cd-l%d_v01.json' % k for k in range(1, 7)] + \
       ['l12/l_extract_v13.py', 'l12/out/TESTOLD_L_EXTRACT_20261122T001127.json', 'l12/l_pods_v13.py',
        'ycheck/y_twin_l12_v13.py', 'ycheck/out/TESTOLD_Y_TWIN_L12_v13_b2000.json',
        'recount/rc_y_twin_l12_v13.py', 'recount/out/TESTOLD_RC_Y_TWIN_L12_v13_b2000.json',
        'l12/A12_SECTIONS_2_3b_CD_v01.md', 'l12/make_freeze_add7_v13.py']
USES = ['crossing/make_cases_x_v13.py', 'crossing/make_cases_x_pc_v13.py', 'crossing/x_extract_v13.py', 'crossing/x_pods_v13.py',
        'ycheck/y_twin_v13.py', 'ycheck/CD_DEFINITIONS_Y_v13.md', 'recount/rc_y_twin_v13.py', 'recount/rc_y_kern_v13.py',
        'recount/rc_y_calib_remote_v13.py']
NAME = 'add7'


def write(approval):
    out = FX.LOCKS / f'FREEZE_CD_{NAME}.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    if (FX.REV / 'LOCK_A12a.txt').exists(): raise SystemExit('REFUSED: LOCK_A12a.txt exists; add7 must precede it')
    doc = dict(schema='FREEZE_V13_ADDENDUM', addendum_to='work/locks/FREEZE_CD.json (sha256 %s)' % FX.sha(FX.LOCKS / 'FREEZE_CD.json'),
               package='C and D (session v13-cd-capture, Claude Opus 5.5); second program by Claude Sonnet 5.5',
               written=time.strftime('%Y-%m-%d %H:%M %Z'), approval=approval,
               kind=('adds files: A12 sec. 2 (new lead-braking runs: cases, packet, jobs, CV0 extractor, pod tool) and sec. 3b (Y on the new runs, '
                     'first and second programs), before LOCK_A12a and before any value of a new run; no frozen file changed'),
               adds=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in ADDS],
               uses=[dict(path=FX.rel(p), sha256=FX.sha(CD / p)) for p in USES], replaces=[])
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(out.name, FX.sha(out), '| adds', len(doc['adds']), '| uses', len(doc['uses']))


if __name__ == '__main__':
    if sys.argv[1] == 'write': write(sys.argv[2])
    else: FX.verify(NAME)
