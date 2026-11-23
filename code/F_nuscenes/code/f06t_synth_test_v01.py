"""Package F (revision v13): end-to-end test of f06_score_v01 (horizon and heldout modes) on SYNTHETIC arrays only. New file,
19 Nov 2026 (Claude Opus 5.5); 20 Nov 2026: adapted to the clearance departure (f06 reads cache\\clear_v02 by default).
Reads recount\\synth\\arrays_<tracker>\\<split>\\ (written by the recount's fr_synth_v01.py; no nuScenes data), copies them into
<scratch>\\cache (adding a `sweep` key) and writes synthetic clear_v02 files there; outputs go to the scratch folder given as
argv[1]. The split gate is replaced in this process only, because the synthetic scenes are not nuScenes scenes; the bootstrap
sizes are reduced. Nothing here reads a cache, track or val file of F.
Checks: (1) with clear_v02 equal to the arrays' clearances, the v02 horizon output equals the v01 one exactly; (2) with clear_v02
changed (every unsafe row of an even-numbered decision made safe), the horizon and held-out modes run end to end and the horizon
values differ from (1).
Usage: venv\\Scripts\\python.exe -I f06t_synth_test_v01.py <scratch out dir>
"""
import pathlib, sys, shutil
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json                                  # noqa: E402
import numpy as np                           # noqa: E402

SYN = FC.F / 'recount' / 'synth'
OUTD = pathlib.Path(sys.argv[1]); OUTD.mkdir(parents=True, exist_ok=True)
CA = OUTD / 'cache'
if CA.exists():
    shutil.rmtree(CA)
for p in OUTD.glob('F_*'):
    p.unlink()
names = {s: sorted(p.stem for p in (SYN / 'arrays_T1' / s).glob('*.npz')) for s in ('train', 'val')}
for tr in ('T1', 'IMM'):
    for s in ('train', 'val'):
        (CA / ('arrays_' + tr) / s).mkdir(parents=True)
        for nm in names[s]:
            z = dict(np.load(SYN / ('arrays_' + tr) / s / (nm + '.npz'), allow_pickle=False))
            z['sweep'] = np.arange(z['clear'].shape[0])
            np.savez(CA / ('arrays_' + tr) / s / (nm + '.npz'), **z)


def write_clear(modify):
    for s in ('train', 'val'):
        d = CA / 'clear_v02' / s
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        for nm in names[s]:
            z = np.load(CA / 'arrays_T1' / s / (nm + '.npz'), allow_pickle=False)
            out = {}
            for k in ('clear', 'clear2'):
                c = z[k].astype(float).copy()
                if modify:
                    even = (np.arange(c.shape[0]) % 2 == 0)[:, None]
                    c = np.where(even & np.isfinite(c) & (c <= 0), 1.0, c)
                out[k] = c
            np.savez(d / (nm + '.npz'), sweep=z['sweep'], **out)


FC.CACHE = CA
FC.OUT = OUTD
FC.splits = lambda: names
FC.require_split = lambda split: None

import f06_score_v01 as S                    # noqa: E402
S.FC.CACHE = CA; S.FC.OUT = OUTD; S.FC.splits = FC.splits; S.FC.require_split = FC.require_split
S.NBOOT = 400; S.B_OUT = 40; S.B_IN = 60

# (1) identity: v01 path vs v02 path with equal clearances
S.CLEAR = 'v01'; S.horizon(1)
write_clear(False)
S.CLEAR = 'v02'; S.horizon(1)
a = json.loads((OUTD / 'F_HORIZON_RULE_v01.json').read_text(encoding='utf-8'))
b = json.loads((OUTD / 'F_HORIZON_RULE_v02.json').read_text(encoding='utf-8'))
same = all(a['horizons'][h]['R_gl_pp'] == b['horizons'][h]['R_gl_pp'] and a['horizons'][h]['D_gl_E_F0'] == b['horizons'][h]['D_gl_E_F0']
           for h in a['horizons'])
print('(1) v02 with equal clearances reproduces v01 exactly:', same)
# (2) changed clearances, end to end
(OUTD / 'F_HORIZON_RULE_v02.json').unlink()
write_clear(True)
S.horizon(1)
c = json.loads((OUTD / 'F_HORIZON_RULE_v02.json').read_text(encoding='utf-8'))
differ = any(a['horizons'][h]['D_gl_E_F0'] != c['horizons'][h]['D_gl_E_F0'] for h in a['horizons'])
print('(2) changed clearances change the horizon values:', differ, '| primary', c['primary_horizon_s'], '| clearance', c['clearance']['version'])
if c['primary_horizon_s'] is None:
    c['primary_horizon_s'] = 3
    (OUTD / 'F_HORIZON_RULE_v02.json').write_text(json.dumps(c), encoding='utf-8')
S.heldout(1)
d = json.loads((OUTD / 'F_HELDOUT_v02.json').read_text(encoding='utf-8'))
print('verify', [round(v['max_rel'], 17) for v in d['verify']])
print('clearance', d['clearance']['version'])
print('descriptive all', {k: (round(v['point'], 4) if v['point'] == v['point'] else None) for k, v in d['populations']['all']['descriptive'].items()})
print('calibration', {k: (v['level'], v['reason'][:40]) for k, v in d['calibration'].items()})
print('hypotheses', d['hypotheses'])
print('TEST', 'PASS' if (same and differ) else 'FAIL')
