"""Write or verify a FREEZE_CD addendum that ADDS files (no frozen file is changed), for X (AMENDMENT_11_v13.md sec. 3). New file,
21 Nov 2026 (Claude Opus 5.5, session CD). The addendum records each added file's SHA-256 and, for the record, the SHA-256 of every
already-frozen file the X programs use unchanged ('uses'); verify re-hashes both lists.
Usage: python -I -B make_freeze_x_v13.py write ADDENDUM_NAME "APPROVAL TEXT"     (refuses if the addendum exists)
       python -I -B make_freeze_x_v13.py verify ADDENDUM_NAME
"""
import hashlib, json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent; WORK = CD.parent; REV = WORK.parent
LOCKS = WORK / 'locks'
ADDS = {
    'add3': ['crossing/make_cases_x_v13.py', 'crossing/make_cases_x_pc_v13.py', 'crossing/CASES_X_PC_v13.json', 'crossing/DEVELOPMENT_PROTOCOL_X_v13.json',
             'crossing/build_packet_x_v13.py', 'packets/packet_x_v13.tar.gz', 'packets/packet_x_v13_RECEIPT.json', 'crossing/make_jobs_x_pc_v13.py',
             'crossing/jobs_x/JOBS_PX13_claude-v13cd-x1_v01.json', 'crossing/jobs_x/JOBS_PX13_claude-v13cd-x2_v01.json',
             'crossing/jobs_x/JOBS_PX13_claude-v13cd-x3_v01.json', 'crossing/jobs_x/JOBS_PX13_claude-v13cd-x4_v01.json',
             'crossing/jobs_x/JOBS_PX13_claude-v13cd-x5_v01.json', 'crossing/jobs_x/JOBS_PX13_claude-v13cd-x6_v01.json',
             'crossing/x_extract_v13.py', 'crossing/x_pods_v13.py', 'crossing/x_cross_v13.py', 'crossing/compare_x_v13.py',
             'crossing/make_freeze_x_v13.py', 'crossing/CD_DEFINITIONS_X_v13.md',
             'recount/rc_x_cross_v13.py', 'recount/rc_x_kern_v13.py', 'recount/rc_x_calib_remote_v13.py', 'recount/README_RECOUNT_X.md'],
}
USES = ['analysis/cd_common_v13.py', 'analysis/gl_fast_v13.py', 'analysis/calib_remote_v13.py', 'tools/pods_v13.py', 'tools/acquire_v13.py',
        'tools/remote_chain_v01.sh', 'tools/b7_pods_v13.py', 'tools/calib_pods_v13.py', 'tools/calib_merge_v13.py', 'tools/download_v13.py',
        'packets/packet_main_v03.tar.gz', 'recount/rc_core_v13.py', 'recount/rc_kern_v13.py', 'recount/rc_calib_remote_v13.py',
        '../shared/trackers/trk_arrays_v01.py', '../shared/trackers/trk_score_v01.py', '../shared/trackers/trk_env_v01.py']


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def rel(p):
    return str((CD / p).resolve().relative_to(REV.parent)).replace('/', '\\')


def write(name, approval):
    out = LOCKS / f'FREEZE_CD_{name}.json'
    if out.exists(): raise SystemExit('REFUSED: %s exists' % out.name)
    fz = LOCKS / 'FREEZE_CD.json'
    doc = dict(schema='FREEZE_V13_ADDENDUM', addendum_to='work/locks/FREEZE_CD.json (sha256 %s)' % sha(fz),
               package='C and D (session v13-cd-capture, Claude Opus 5.5)', written=time.strftime('%Y-%m-%d %H:%M %Z'), approval=approval,
               kind='adds files for X (AMENDMENT_11_v13.md sec. 3), before LOCK_A11 and before any fresh crossing value; no frozen file changed',
               adds=[dict(path=rel(p), sha256=sha(CD / p)) for p in ADDS[name]],
               uses=[dict(path=rel(p), sha256=sha(CD / p)) for p in USES], replaces=[])
    out.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(out.name, sha(out), '| adds', len(doc['adds']), '| uses', len(doc['uses']))


def verify(name):
    d = json.loads((LOCKS / f'FREEZE_CD_{name}.json').read_text(encoding='utf-8'))
    bad = [e['path'] for e in d['adds'] + d['uses'] if sha(REV.parent / e['path']) != e['sha256']]
    print(json.dumps(dict(addendum=name, adds=len(d['adds']), uses=len(d['uses']), changed=bad)))


if __name__ == '__main__':
    if sys.argv[1] == 'write': write(sys.argv[2], sys.argv[3])
    else: verify(sys.argv[2])
