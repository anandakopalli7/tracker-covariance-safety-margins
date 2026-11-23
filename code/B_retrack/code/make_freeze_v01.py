"""v13 package B: write work\\locks\\FREEZE_B.json (A10 section 4; README_COORDINATION rule 3). New file, 19 Nov 2026 (Claude Opus 5.5).
Lists, with SHA-256 and size: every file of the shared tracker library (shared\\trackers\\, shims included; __pycache__ excluded), the
tuned constants and their sources, the P-bar files of every variant, package B's code, the definitions, and the read-only modules
of record the library imports (P and revision_v12 / v11 paths), so Lock 2 can pin them. Refuses to overwrite an existing manifest
unless 'force' is given (a re-freeze before the deadline is recorded with its reason in STATUS.md).
Usage: python -I -B -X utf8 make_freeze_v01.py [force]
"""
import hashlib, json, pathlib, sys, time

W = pathlib.Path(r'ARS_TRIAL\revision_v13\work')
LIB = W / 'shared' / 'trackers'
B = W / 'B_retrack'
OUT = W / 'locks' / 'FREEZE_B.json'
P = pathlib.Path(r'<library folder>')
CODEX = pathlib.Path(r'<library folder>\149_supported_sensor_preparation_20261101')
RECORD_MODULES = [
    P / '09_redesign' / 'm2_decisions' / 'openloop' / n for n in
    ('olcore_v01.py', 'olcore_rt_v01.py', 'ol_gateR_core_v01.py', 'ol_extract_v01.py', 'ox12_core_v01.py', 'oxsb_core_v01.py',
     'ol_gateR_rt_extract_v01.py', 'pbar_tuning_v01.json')] + [
    P / '11_ojits' / 'A6R' / 'code' / 'optA_lib_v02.py',
    pathlib.Path(r'ARS_TRIAL\revision_v12\analysis\a9_common_v01.py'),
    pathlib.Path(r'ARS_TRIAL\revision_v11\analysis\rev_common_v01.py'),
    CODEX / 'contracts' / 'tracker_config.json', CODEX / 'code' / 'online_tracker.py', CODEX / 'code' / 'consumer.py',
    CODEX / 'code' / 'finite_primitive.py', CODEX / 'code' / 'sensor_policy.py', CODEX / 'vendor' / 'fast_overlap_array.py',
    CODEX / 'vendor' / 'CANMOT' / 'src' / 'canmot' / 'motion_module' / 'kalman_filter.py',
    CODEX / 'vendor' / 'CANMOT' / 'src' / 'canmot' / 'motion_module' / 'motion_model.py',
    CODEX / 'vendor' / 'CANMOT' / 'src' / 'canmot' / 'tracking' / 'nusc_trajectory.py',
    CODEX / 'vendor' / 'CANMOT' / 'src' / 'canmot' / 'tracking' / 'nusc_tracker.py']


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def entry(p, root=None):
    st = p.stat()
    return dict(path=str(p.relative_to(root)) if root else str(p), sha256=sha(p), bytes=st.st_size,
                mtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.st_mtime)))


def main():
    if OUT.exists() and not (len(sys.argv) > 1 and sys.argv[1] == 'force'):
        raise SystemExit('REFUSED: %s exists' % OUT)
    lib = [entry(p, W) for p in sorted(LIB.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
    pbar = [entry(p, W) for p in sorted((B / 'out' / 'pbar').glob('PBAR_*_v01.json'))]
    b3 = [entry(p, W) for p in sorted((B / 'out' / 'b3').glob('*.json'))]
    code = [entry(p, W) for p in sorted((B / 'code').glob('*.py'))] + [entry(p, W) for p in sorted((B / 'code').glob('*.sh'))]
    imm2 = [entry(p, W) for p in sorted((B / 'imm2').glob('*')) if p.is_file()]
    defs = [entry(B / 'B_ANALYSIS_DEFINITIONS_v01.md', W)]
    rec = [entry(p) for p in RECORD_MODULES]
    const = json.loads((LIB / 'trk_constants_v01.json').read_text(encoding='utf-8'))
    doc = dict(package='B (offline re-tracking) and the shared tracker library', written=time.strftime('%Y-%m-%d %H:%M:%S %Z'),
               writer='package-B session, Claude Opus 5.5 (claude-opus-5-5)',
               rule='After this manifest the library does not change (README_COORDINATION rule 3; A10 section 4 change rules).',
               tuned_constants=dict(R_car_diag=const['R_car_diag'], kappa=const['kappa'], sigma_a2=const['sigma_a2'],
                                    ca_acc_init_var=const['ca_acc_init_var'], tuning=const['tuning']),
               b4_filter_class=const['b4_filter_class'], cut_in_lateral_threshold_m=1.75,
               cut_in_threshold_basis='events found in 20 of 20 cut-in tuning runs (out/b9/B9_EVENT_COUNT_lat1p75_v01.json)',
               imm=dict(transition_diag_per_0p5s=0.95, sensitivities=[0.90, 0.98], mu0=[0.9, 0.1]),
               library=lib, pbar=pbar, b3_tuning=b3, package_b_code=code, second_imm=imm2, definitions=defs, record_modules_read_only=rec)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('wrote', OUT, 'library files', len(lib), 'pbar', len(pbar))


if __name__ == '__main__':
    main()
