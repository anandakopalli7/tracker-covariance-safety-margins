"""Write work\\locks\\FREEZE_CD.json: SHA-256 of every job list, case file, protocol, packet, actor-policy source, capture tool and
analysis script of packages C and D (A10 sec. 4; README_COORDINATION rule 3). Never overwrites. Usage: python -I make_freeze_cd_v13.py [--stage 1|2] [--verify]
Two-stage Lock 2 (coordinator 20 Nov 01:53 EST): stage 1 (core) -> locks\\FREEZE_CD.json; stage 2 (A10 sec. 5.7 additions, every
code/definition/test file not in stage 1, and a check that no stage-1 file changed) -> locks\\FREEZE_CD_2.json.
"""
import datetime, hashlib, json, pathlib, platform, sys
HERE = pathlib.Path(__file__).resolve().parent
STAGE = 2 if '--stage' in sys.argv and sys.argv[sys.argv.index('--stage') + 1] == '2' else 1
OUT1 = HERE.parent / 'locks' / 'FREEZE_CD.json'                     # stage 1 (core): LOCK_A10_2
OUT = OUT1 if STAGE == 1 else HERE.parent / 'locks' / 'FREEZE_CD_2.json'   # stage 2 (A10 sec. 5.7 additions): LOCK_A10_2c
STAGE1_TOOLS = ('acquire_v13.py', 'b7_identity_old0037.py', 'b7_redetect_v13.py', 'calib_merge_v13.py', 'calib_pods_v13.py', 'calib_worker_v13.sh',
                'check_resim_v13.py', 'download_v13.py', 'fetch_small_v13.py', 'next_list_v13.py', 'pilot_check_d1.py', 'pods_v13.py',
                'remote_b7_and_seal.sh', 'remote_chain_v01.sh', 'remote_status_cd.sh', 'remote_survey_cd.sh', 'remote_update_and_work_v01.sh',
                'republish_salvaged_v13.py', 'salvage_local_v13.py', 'seal_extract_v13.py', 'status_all.sh', 'terminate_when_done_v13.py',
                'volume_cleanup_v13.py', 'wait_b7_then_resim.sh')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()


def entry(p):
    p = pathlib.Path(p)
    return dict(path=str(p.relative_to(HERE.parent.parent)) if p.is_relative_to(HERE.parent.parent) else str(p), sha256=sha(p), bytes=p.stat().st_size)


def norm(x):                                          # path key: the parts after 'revision_v13', lower-case
    parts = [q.lower() for q in pathlib.PureWindowsPath(x).parts]
    return '/'.join(parts[parts.index('revision_v13') + 1:] if 'revision_v13' in parts else parts)


def verify_manifest(path):
    """Every file of a freeze manifest still has its SHA-256; addenda (<manifest>_add<N>.json, coordinator's naming) replace an entry's
    SHA-256 when the frozen sha equals the addendum's sha256_before. Returns (n_files, changed_or_missing, addenda_applied)."""
    d = json.loads(path.read_text(encoding='utf-8')); bad = []; sup = {}; applied = []
    for af in sorted(path.parent.glob(path.stem + '_add*.json')):
        for r in json.loads(af.read_text(encoding='utf-8')).get('replaces', []):
            sup[norm(r['path'])] = (r['sha256_before'], r['sha256_after'], af.name)
    for g, es in d['groups'].items():
        for e in es:
            p = pathlib.Path(e['path']); p = p if p.is_absolute() else HERE.parent.parent / p
            want = e['sha256']; key = norm(e['path']) if pathlib.PureWindowsPath(e['path']).is_absolute() else norm('revision_v13/' + e['path'])
            if key in sup and sup[key][0] == want: want = sup[key][1]; applied.append((e['path'], sup[key][2]))
            if not p.is_file() or sha(p) != want: bad.append(e['path'])
    return sum(len(v) for v in d['groups'].values()), bad, applied


def main():
    if '--verify' in sys.argv:                        # after Lock 2: every frozen file still has its SHA-256
        n, bad, applied = verify_manifest(OUT)
        if applied: print(json.dumps(dict(addenda_applied=applied)))
        print(json.dumps(dict(verified=n, changed_or_missing=bad))); return
    if OUT.exists(): raise SystemExit('REFUSED: %s exists' % OUT)
    A, R, RD, O = HERE / 'analysis', HERE / 'recount', HERE / 'recount_d', HERE / 'analysis' / 'out'
    core = {
        'case_files_and_protocols': [HERE / 'CASES_C_v13.json', HERE / 'd1' / 'CASES_D1_v13.json', HERE / 'd1' / 'DEVELOPMENT_PROTOCOL_D1_v13.json',
                                     HERE / 'REPLACEMENTS_C_v13.json',
                                     pathlib.Path(r'<library folder>\DEVELOPMENT_PROTOCOL_MAIN_v01.json')],
        'job_lists_used': sorted((HERE / 'jobs').glob('JOBS_*.json')),
        'job_list_builders': [HERE / 'make_jobs_c_v13.py', HERE / 'make_jobs_c_v13_remaining.py', HERE / 'd1' / 'make_jobs_d1_v13.py',
                              HERE / 'd1' / 'make_cases_d1_v13.py', HERE / 'd1' / 'build_packet_d1_v13.py'],
        'packets': [HERE / 'packets' / 'packet_main_v03.tar.gz', HERE / 'packets' / 'packet_d1_v13.tar.gz', HERE / 'packets' / 'packet_d1_v13_RECEIPT.json'],
        'd1_actor_policy_version': sorted((HERE / 'd1' / 'src').rglob('*.py')),
        'd1_review_and_tests': [HERE / 'd1' / 'REVIEW_D1_PACKET_v01.md', HERE / 'd1' / 'test_d1_policy_v13.py', HERE / 'd1' / 'TEST_D1_POLICY_v13.json'],
        'capture_sealing_pod_and_calibration_tools': [HERE / 'tools' / n for n in STAGE1_TOOLS],
        'analysis_scripts': [A / n for n in ('cd_common_v13.py', 'c_extract_v13.py', 'c_lead_v13.py', 'c_lead_choice_v13.py', 'c_cutin_v13.py',
                                             'gl_fast_v13.py', 'calib_remote_v13.py', 'd_nonbraking_v13.py', 'd2_event_table_v13.py',
                                             'test_gl_fast_v13.py', 'prof_gl_fast_v13.py', 'prof2_gl_fast_v13.py')],
        'analysis_tests': [O / n for n in ('TEST_GL_FAST_v13.json', 'TESTOLD_C_LEAD_H0_H5_v13.json', 'TESTOLD_C_CUTIN_K0_K2_v13.json',
                                           'TESTOLD_D_NONBRAKING_DH1_DH2_v13.json', 'TESTOLD_D2_EVENT_TABLE_v13.json', 'VENV_FREEZE.txt')]
                          + [R / 'out' / n for n in ('TEST_RC_KERNEL_v13_dev2.json', 'TEST_RC_KERNEL_v13_podpath.json', 'TEST_RC_CALIBRATION_v13.json',
                                                     'TEST_RC_CALIBRATION_v13_podpath.json', 'TEST_RC_CALIB_CHUNKS_v13.json',
                                                     'RC_C_LEAD_TESTOLD_b200_o4_i1000_matched.json', 'RC_C_CUTIN_TESTOLD_b200_o4_i1000_matched.json',
                                                     'RC_C_CUTIN_TESTOLD_TRUTH_v13.json')]
                          + [RD / 'out' / n for n in ('RC_D_NONBRAKING_v13_TESTOLD_t2.json', 'RC_D2_EVENT_TABLE_v13_TESTOLD_t1.json')]
                          + [HERE / 'out' / n for n in ('COMPARE_C_v13_TESTOLD_matched_final.json', 'COMPARE_D_v13_TESTOLD.json')],
        'definitions_and_runbook': [HERE / 'CD_DEFINITIONS_v13.md', HERE / 'RUN_AFTER_LOCK2.md', HERE / 'compare_c_v13.py', HERE / 'compare_d_v13.py',
                                    HERE / 'make_jobs_resim_v13.py'],
        'second_programs_C_recount': [R / n for n in ('rc_core_v13.py', 'rc_kern_v13.py', 'rc_c_lead_v13.py', 'rc_c_cutin_v13.py',
                                                      'rc_calib_remote_v13.py', 'test_rc_kernel_v13.py', 'test_rc_calibration_v13.py',
                                                      'test_rc_calib_chunks_v13.py', 'dryrun_fresh_path_v13.py', 'README_RECOUNT_C.md')],
        'second_programs_D_recount_d': [RD / n for n in ('rc_d_common_v13.py', 'rc_d_nonbraking_v13.py', 'rc_d2_event_table_v13.py', 'README_RECOUNT_D.md')],
        'shared_tracker_library_imported_read_only': sorted(p for p in (HERE.parent / 'shared' / 'trackers').rglob('*') if p.suffix in ('.py', '.json', '.md') and '__pycache__' not in p.parts),
        'capture_records': [HERE / 'SEALING_SUMMARY_v13.json', HERE / 'RESIM_SUMMARY_v13.json', HERE / 'volume_cleanup_receipts.json'],
    }
    if STAGE == 1:
        groups = core
    else:                                             # stage 2: every code, definition and test file not frozen in stage 1
        f1 = json.loads(OUT1.read_text(encoding='utf-8')); frozen1 = set()
        for es in f1['groups'].values():
            for e in es:
                q = pathlib.Path(e['path']); q = q if q.is_absolute() else HERE.parent.parent / q; frozen1.add(q.resolve())
        _, changed, _ = verify_manifest(OUT1)         # stage 1 with its addenda (FREEZE_CD_add1: REPLACEMENTS_C_v13.json)
        if changed: raise SystemExit('REFUSED: stage-1 files changed since FREEZE_CD: %s' % changed)
        cand = lambda d, pats: sorted({x for pat in pats for x in d.glob(pat)})
        pools = {
            'stage2_analysis_scripts': cand(A, ('*.py',)),
            'stage2_tools': cand(HERE / 'tools', ('*.py', '*.sh', '*.md')),
            'stage2_second_programs_C': cand(R, ('*.py', '*.md')),
            'stage2_second_programs_D': cand(RD, ('*.py', '*.md')),
            'stage2_export': cand(HERE / 'export', ('*.py', '*.json', '*.md')),
            'stage2_definitions_and_runbook': cand(HERE, ('CD_DEFINITIONS_*.md', 'RUN_AFTER_LOCK2*.md', 'compare_*.py', 'make_freeze_cd_v13.py')),
            'stage2_tests': cand(O, ('TEST*.json',)) + cand(R / 'out', ('TEST*.json', 'TESTOLD*.json')) + cand(RD / 'out', ('*TESTOLD*.json',))
                            + cand(HERE / 'out', ('*TESTOLD*.json',)),
        }
        groups = {g: [x for x in ps if x.resolve() not in frozen1 and '__pycache__' not in x.parts] for g, ps in pools.items()}
        groups['stage1_reference'] = [OUT1]
    missing = [str(x) for ps in groups.values() for x in ps if not pathlib.Path(x).is_file()]
    if missing: raise SystemExit('REFUSED: listed files missing: %s' % missing)
    doc = dict(schema='FREEZE_V13', stage=STAGE, package='C and D (session v13-cd-capture, Claude Opus 5.5)', amendment='AMENDMENT_10_v13.md',
               lock=('LOCK_A10_2 (stage 1, core)' if STAGE == 1 else 'LOCK_A10_2c (stage 2, A10 sec. 5.7 additions; two-stage Lock 2, coordinator 20 Nov 01:53 EST)'),
               written_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), python=sys.version, platform=platform.platform(),
               groups={g: [entry(p) for p in ps] for g, ps in groups.items()},
               imported_read_only=dict(shared_trackers='work/shared/trackers (frozen by FREEZE_B.json)',
                                       v12_gridless='revision_v12/analysis/a9_common_v01.py ' + sha(r'ARS_TRIAL\revision_v12\analysis\a9_common_v01.py'),
                                       v11_loader='revision_v11/analysis/rev_common_v01.py ' + sha(r'ARS_TRIAL\revision_v11\analysis\rev_common_v01.py'),
                                       scoring_library='P/11_ojits/A6R/code/optA_lib_v02.py ' + sha(r'<library folder>\optA_lib_v02.py')),
               venv='work/CD_capture/.venv: numba and llvmlite added (see analysis/out/VENV_FREEZE.txt)')
    fb = HERE.parent / 'locks' / 'FREEZE_B.json'     # cross-check: shared-library hashes equal package B's freeze
    if fb.is_file():
        seen = {}
        def walk(o):
            if isinstance(o, dict):
                p, h = o.get('path') or o.get('file'), o.get('sha256')
                q = p.replace('\\', '/') if isinstance(p, str) else ''
                if isinstance(h, str) and 'shared/trackers/' in q: seen[q.split('shared/trackers/', 1)[1]] = h
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)
        walk(json.loads(fb.read_text(encoding='utf-8')))
        mine = {e['path'].replace('\\', '/').split('shared/trackers/', 1)[1]: e['sha256'] for e in doc['groups'].get('shared_tracker_library_imported_read_only', [])}
        diff = sorted(n for n in mine if n in seen and seen[n] != mine[n])
        doc['freeze_b_crosscheck'] = dict(freeze_b_sha256=sha(fb), compared=sorted(n for n in mine if n in seen), not_in_freeze_b=sorted(n for n in mine if n not in seen), different=diff)
        if diff: raise SystemExit('REFUSED: shared-library files differ from FREEZE_B: %s' % diff)
    else:
        doc['freeze_b_crosscheck'] = 'FREEZE_B.json not present when FREEZE_CD was written'
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(OUT, sha(OUT), sum(len(v) for v in doc['groups'].values()), 'files')


if __name__ == '__main__':
    main()
