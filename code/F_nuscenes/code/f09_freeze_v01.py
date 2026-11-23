"""Package F (revision v13): the freeze manifest work\\locks\\FREEZE_F.json (README_COORDINATION rule 3; A10 section 4). New file,
19 Nov 2026 (Claude Opus 5.5). Lists every code, library, configuration, specification and design-split output file of package F
with its SHA-256, the shared files F imports (package B's library: their hashes as F used them), the Python and package versions,
and the settings F fixes for Lock 2: route, split, primary horizon (from out\\F_HORIZON_RULE_v01.json), delta, seeds, the P-bar
files and the departures. Refuses to overwrite. Reads no val scene.
20 Nov 2026: the clearance departure (notes\\F_DEPARTURE_CLEARANCE_v01.md) is in force: the primary horizon comes from
out\\F_HORIZON_RULE_v02.json, which must carry the pinned departure file's SHA-256; the v02 adapter check and horizon comparison
must agree; the pre-registered outcome (F_HORIZON_RULE_v01.json) is recorded beside it. `--outcome-a` freezes outcome (a)
instead (the coordinator's fallback if the departure is not recounted by 20 Nov 14:00 EST).
Usage: python -I f09_freeze_v01.py [--outcome-a]
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json, platform, subprocess            # noqa: E402

OUTF = FC.F.parent / 'locks' / 'FREEZE_F.json'
SHARED = FC.F.parent / 'shared' / 'trackers'


def files_under(root, patterns=('*',)):
    out = []
    for pat in patterns:
        out += [p for p in root.rglob(pat) if p.is_file() and '__pycache__' not in p.parts]
    return sorted(set(out))


OUTCOME_A = '--outcome-a' in sys.argv
V02_ONLY = {'F_HORIZON_RULE_v02.json', 'F_HORIZON_COMPARE_v02.json', 'F_CLEAR_V02_train_v01.json', 'F_ADAPTER_CHECK_v02.json',
            'F_RECOUNT_HORIZON_v02.json', 'F_CALIB_PLATFORM_TEST_design_R_v01.json', 'F_CALIB_PLATFORM_TEST_synth_full_v01.json'}


def main():
    if OUTF.exists():
        raise SystemExit('REFUSED: %s exists' % OUTF)
    FC.require_split('train')
    groups = {
        'code': files_under(FC.F / 'code', ('*.py', '*.sh')),
        'lib': files_under(FC.LIB),
        'notes': [FC.F / 'notes' / 'ADAPTER_SPEC_F_v01.md', FC.F / 'notes' / 'ADAPTER_CHECK_DECISIONS_v01.json',
                  FC.F / 'notes' / 'ARRAYS_FORMAT_F_v01.md', FC.F / 'notes' / 'F_DEPARTURE_CLEARANCE_v01.md',
                  FC.F / 'notes' / 'F_NUPLAN_ATFAULT_CHECK_v01.md'],
        'design_outputs': [FC.OUT / 'PBAR_T1_train_v01.json', FC.OUT / 'PBAR_IMM_train_v01.json', FC.OUT / 'F_HORIZON_RULE_v01.json',
                           FC.OUT / 'F_HORIZON_COMPARE_v01.json', FC.OUT / 'F_ROOM_MECHANISM_T1_train_v01.json',
                           FC.OUT / 'F_HORIZON_RULE_v02.json', FC.OUT / 'F_HORIZON_COMPARE_v02.json', FC.OUT / 'F_CLEAR_V02_train_v01.json',
                           FC.OUT / 'F_ADAPTER_CHECK_v01.json', FC.OUT / 'F_ADAPTER_CHECK_v02.json',
                           FC.OUT / 'F_ADAPTER_CHECKS_T1_train_v01.json'],
        'second_program_adapter_check': files_under(FC.F / 'check2'),
        'second_program_recount': files_under(FC.F / 'recount', ('*.py', '*.md')),
        'second_program_recount_outputs': [FC.F / 'recount' / 'F_RECOUNT_HORIZON_v01.json', FC.F / 'recount' / 'F_RECOUNT_HORIZON_v02.json'],
        'pod_double_bootstrap_platform_test': [FC.OUT / 'calib' / 'test' / 'F_CALIB_PLATFORM_TEST_design_R_v01.json',
                                              FC.OUT / 'calib' / 'test' / 'F_CALIB_PLATFORM_TEST_synth_full_v01.json'],
        'shared_imported': sorted(SHARED.glob('trk_*.py')) + [SHARED / 'trk_constants_v01.json'] + sorted((SHARED / 'shims_v01').rglob('*.py')),
        'data_logs': [FC.LOGS / 'f00_extract_v01.json', FC.LOGS / 'f01_prepare_train_v01.json'],
    }
    man = {}
    missing = []
    h2 = FC.OUT / 'F_HORIZON_RULE_v02.json'
    v02_stops = h2.exists() and json.loads(h2.read_text(encoding='utf-8'))['primary_horizon_s'] is None
    for g, fs in groups.items():
        man[g] = {}
        for f in fs:
            if OUTCOME_A and f.name in V02_ONLY and not f.exists():
                continue
            if v02_stops and g == 'pod_double_bootstrap_platform_test' and not f.exists():
                continue                                  # no held-out run, so no pod double bootstrap
            if not f.exists():
                missing.append(str(f)); continue
            man[g][str(f.relative_to(FC.F.parent.parent))] = FC.sha256_file(f)
    if missing:
        raise SystemExit('REFUSED: missing %s' % missing)
    # every IMM train track file must carry one and the same library hash set (as imported; f02 since 19 Nov 18:50 EST), equal to
    # the files now; and to B's freeze manifest where it lists the same files
    sys.path.insert(0, str(FC.F / 'code'))
    import f02_track_v01 as F02
    now = F02.shared_hashes()
    seen = set(); n_imm = 0
    import numpy as np
    for p in sorted((FC.CACHE / 'tracks_IMM' / 'train').glob('scene-*.npz')):
        if '.tmp' in p.name:
            continue
        m = json.loads(str(np.load(p, allow_pickle=False)['meta'])); n_imm += 1
        seen.add(json.dumps(m.get('shared_sha256'), sort_keys=True))
    if n_imm != 700 or len(seen) != 1 or json.loads(next(iter(seen))) != now:
        raise SystemExit('REFUSED: IMM train tracks: %d files, %d library versions, equal to the files now: %s'
                         % (n_imm, len(seen), bool(seen) and json.loads(next(iter(seen))) == now))
    imm_lib = dict(n_track_files=n_imm, hashes=now)
    fb = FC.F.parent / 'locks' / 'FREEZE_B.json'
    if fb.exists():
        txt = fb.read_text(encoding='utf-8')
        imm_lib['FREEZE_B_sha256'] = FC.sha256_file(fb)
        imm_lib['hashes_not_found_in_FREEZE_B'] = sorted(k for k, h in now.items() if h not in txt)
    else:
        imm_lib['FREEZE_B_sha256'] = None
    hz1 = json.loads((FC.OUT / 'F_HORIZON_RULE_v01.json').read_text(encoding='utf-8'))
    dep = FC.F / 'notes' / 'F_DEPARTURE_CLEARANCE_v01.md'
    if OUTCOME_A:
        # fallback (coordinator's condition 6): the departure was not recounted by 20 Nov 14:00 EST; outcome (a) is frozen
        hz = hz1
        clearance = dict(in_force='of record (outcome (a): the departure was not recounted by 20 Nov 14:00 EST)',
                         departure_file='work\\F_nuscenes\\notes\\F_DEPARTURE_CLEARANCE_v01.md', departure_sha256=FC.sha256_file(dep))
    else:
        hz = json.loads((FC.OUT / 'F_HORIZON_RULE_v02.json').read_text(encoding='utf-8'))
        if hz['clearance'].get('sha256') != FC.sha256_file(dep):
            raise SystemExit('REFUSED: the v02 horizon output does not carry the pinned departure file')
        for f in ('F_HORIZON_COMPARE_v02.json', 'F_ADAPTER_CHECK_v02.json'):
            if not json.loads((FC.OUT / f).read_text(encoding='utf-8'))['all_agree']:
                raise SystemExit('REFUSED: %s does not agree' % f)
        if not json.loads((FC.OUT / 'F_CLEAR_V02_train_v01.json').read_text(encoding='utf-8'))['checks_passed']:
            raise SystemExit('REFUSED: clear_v02 train checks did not pass')
        if hz['primary_horizon_s'] is not None:
            for t in ('design_R', 'synth_full'):
                if not json.loads((FC.OUT / 'calib' / 'test' / ('F_CALIB_PLATFORM_TEST_%s_v01.json' % t)).read_text(encoding='utf-8'))['ok']:
                    raise SystemExit('REFUSED: pod platform test %s did not pass' % t)
        import hashlib
        cv = sorted((FC.CACHE / 'clear_v02' / 'train').glob('scene-*.npz'))
        cv = [p for p in cv if '.tmp' not in p.name]
        if len(cv) != 700:
            raise SystemExit('REFUSED: clear_v02 train has %d files' % len(cv))
        dg = hashlib.sha256(''.join('%s %s\n' % (p.name, FC.sha256_file(p)) for p in cv).encode()).hexdigest()
        clearance = dict(in_force='departure (v02)', file='work\\F_nuscenes\\notes\\F_DEPARTURE_CLEARANCE_v01.md', sha256=FC.sha256_file(dep),
                         decided='coordinator, 19 Nov 2026 23:58 EST, after the design-split stop; author may veto until the text freeze',
                         clear_v02_train=dict(n_files=len(cv), digest_sha256_of_name_and_sha_lines=dg),
                         preregistered_outcome=dict(file='work\\F_nuscenes\\out\\F_HORIZON_RULE_v01.json',
                                                    primary_horizon_s=hz1['primary_horizon_s'], stop=hz1.get('stop')))
    venv_py = FC.F / 'venv' / 'Scripts' / 'python.exe'
    vers = subprocess.run([str(venv_py), '-I', '-c', 'import numba, numpy, llvmlite; print(numba.__version__, numpy.__version__, llvmlite.__version__)'],
                          capture_output=True, text=True).stdout.split()
    import numpy, scipy
    doc = dict(
        package='F', route='F-B, nuScenes (A10 section 0.3)', written=FC.clock(), writer='session F, Claude Opus 5.5',
        split=dict(design='nuScenes v1.0-trainval train (700 scenes; devkit splits.py)', held_out='val (150 scenes)',
                   gate='every F script calls f_common_v01.require_split: val refused until revision_v13\\LOCK_A10_2.txt exists'),
        primary_horizon_s=hz['primary_horizon_s'],
        horizon_rule_output='work\\F_nuscenes\\out\\F_HORIZON_RULE_%s.json' % ('v01' if OUTCOME_A else 'v02'),
        stop=hz.get('stop'), clearance=clearance,
        delta=0.05, seeds=dict(scene_bootstrap=20261923, double_outer=20261912, double_inner=20261913, double_inner_2=20261914,
                               calibration_mc=20261920, e5_permutation=20261915, partial_oracle_mask=20261919,
                               adapter_check_subset=20261917),
        nboot=20000, double_bootstrap=dict(outer=2000, inner=1000),
        trackers=dict(T1='CANMOT via OnlineTracker, lib\\tracker_config.json (= 149\\contracts\\tracker_config.json)',
                      IMM="session B's B1 (trk_tracker_v01.V13Tracker('B1'), default base configuration, trk_constants_v01.json), "
                          'env.setup(exact_trig=False)'),
        pbar_files=['work\\F_nuscenes\\out\\PBAR_T1_train_v01.json', 'work\\F_nuscenes\\out\\PBAR_IMM_train_v01.json'],
        sources=dict(computed=['F0', 'N', 'E', 'F0_IMM', 'N_IMM', 'E_IMM', 'E5_IMM (ceiling c_IMM)'],
                     descriptive=['TG', 'E5', 'E5p', 'RR(E5) - RR(E5p)', 'PO25', 'PO50', 'PO75 (mask default_rng(20261919))'],
                     not_computed=['CK3', 'AM', 'NA'], departure='STATUS.md, "Design decisions fixed on the design split"'),
        imm_library=imm_lib,
        export=dict(program='code\\f12_export_v01.py', file='work\\F_nuscenes\\out\\A_EXPORT_F.json',
                    recount_file='work\\F_nuscenes\\out\\A_RECOUNT_F.json'),
        hypotheses='F-H0, F-H1, F-H2 as A10 section 8.5, population all evaluated decisions; secondary population in-path lead (descriptive)',
        detector_provenance=('the publicly released CenterPoint nuScenes predictions with flip augmentation, as confirmed by the author '
                             '("Official CenterPoint", 19 Nov 2026); file evidence and the post-Lock-2 val NDS check against 68.5 in '
                             'STATUS.md; the test file and the second val file in Downloads are not used'),
        versions=dict(python=platform.python_version(), numpy=numpy.__version__, scipy=scipy.__version__,
                      venv_numba_numpy_llvmlite=vers),
        files=man,
        # the same files as entries {path, sha256} (shared\tools\verify_freeze.py counts only such dicts; paths relative to
        # revision_v13\, which that tool resolves)
        entries=[dict(group=g, path=p, sha256=h) for g, fs in man.items() for p, h in fs.items()])
    OUTF.write_text(FC.jdump(doc), encoding='utf-8')
    print('WROTE', OUTF, sum(len(v) for v in man.values()), 'files')


if __name__ == '__main__':
    main()
