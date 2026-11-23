"""Package F (revision v13): end-to-end test of the pod path of the held-out double bootstrap on SYNTHETIC arrays only. New file,
20 Nov 2026 (Claude Opus 5.5). Same set-up as f06t_synth_test_v01.py (copies of recount\\synth arrays in <scratch>\\cache, clear_v02
equal to the arrays' clearances, reduced bootstrap sizes). Runs f06 heldout three ways and compares:
  (1) local: heldout() with the double bootstrap in process;
  (2) export -> f16_calib_remote_v01.run on the exported job (both inner seeds) -> import_job();
the calibration (every statistic: level, coverages, calibrated levels, MC SD, interval) and the hypotheses must be equal exactly.
Usage: venv\\Scripts\\python.exe -I f06t2_calib_path_test_v01.py <scratch out dir>
"""
import pathlib, sys, shutil
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json                                  # noqa: E402
import numpy as np                           # noqa: E402

SYN = FC.F / 'recount' / 'synth'
OUTD = pathlib.Path(sys.argv[1])
if OUTD.exists():
    shutil.rmtree(OUTD)
OUTD.mkdir(parents=True)
CA = OUTD / 'cache'
names = {s: sorted(p.stem for p in (SYN / 'arrays_T1' / s).glob('*.npz')) for s in ('train', 'val')}
for tr in ('T1', 'IMM'):
    for s in ('train', 'val'):
        (CA / ('arrays_' + tr) / s).mkdir(parents=True)
        for nm in names[s]:
            z = dict(np.load(SYN / ('arrays_' + tr) / s / (nm + '.npz'), allow_pickle=False))
            z['sweep'] = np.arange(z['clear'].shape[0])
            np.savez(CA / ('arrays_' + tr) / s / (nm + '.npz'), **z)
for s in ('train', 'val'):
    (CA / 'clear_v02' / s).mkdir(parents=True)
    for nm in names[s]:
        z = np.load(CA / 'arrays_T1' / s / (nm + '.npz'), allow_pickle=False)
        np.savez(CA / 'clear_v02' / s / (nm + '.npz'), sweep=z['sweep'], clear=z['clear'], clear2=z['clear2'])

FC.CACHE = CA; FC.OUT = OUTD; FC.splits = lambda: names; FC.require_split = lambda split: None
import f06_score_v01 as S                    # noqa: E402
S.FC.CACHE = CA; S.FC.OUT = OUTD; S.FC.splits = FC.splits; S.FC.require_split = FC.require_split
S.CALIB_DIR = OUTD / 'calib'
S.NBOOT = 400; S.B_OUT = 40; S.B_IN = 60
S.horizon(1)
hz = json.loads((OUTD / 'F_HORIZON_RULE_v02.json').read_text(encoding='utf-8'))
if hz['primary_horizon_s'] is None:
    hz['primary_horizon_s'] = 3
    (OUTD / 'F_HORIZON_RULE_v02.json').write_text(json.dumps(hz), encoding='utf-8')
# (1) local
S.CALIB = 'local'; S.heldout(1)
loc = json.loads((OUTD / 'F_HELDOUT_v02.json').read_text(encoding='utf-8'))
(OUTD / 'F_HELDOUT_v02.json').rename(OUTD / 'F_HELDOUT_v02_local.json')
# (2) export -> remote -> import
S.CALIB = 'export'; S.heldout(1)
import f16_calib_remote_v01 as R            # noqa: E402
R.run(OUTD / 'calib', 'heldout_all', [S.SEED_IN, S.SEED_IN2], None, OUTD / 'calib')
S.CALIB = 'import'; S.import_job(1)
imp = json.loads((OUTD / 'F_HELDOUT_v02.json').read_text(encoding='utf-8'))
same_cal = loc['calibration'] == imp['calibration']
same_hyp = loc['hypotheses'] == imp['hypotheses']
same_pop = loc['populations'] == imp['populations']
print('calibration equal:', same_cal, '| hypotheses equal:', same_hyp, '| populations equal:', same_pop)
print('second seed: local', loc['second_inner_seed_run'], '| import', imp['second_inner_seed_run'])
print('levels', {k: v['level'] for k, v in imp['calibration'].items()})
print('TEST', 'PASS' if (same_cal and same_hyp and same_pop) else 'FAIL')
