"""Synthetic E3b set with dict lead variants (as in real D1 contracts). usage: python -I -B make_synth_dict.py <out_runs_dir>
Run from this folder (imports make_synth)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_synth as M

SPEC = {'constant': dict(schema='LEAD_VARIANT_D1V13_V01', kind='constant'),
        'mild_braking': dict(schema='LEAD_VARIANT_D1V13_V01', kind='mild_braking', decel_mps2=2.0),
        'stop_and_go': dict(schema='LEAD_VARIANT_D1V13_V01', kind='stop_and_go', start_s=2.0, decel_mps2=4.0, hold_s=3.0, resume_mps2=1.5, floor_fraction=None)}
# contact cases among 10, per kind and arm
NC = {'constant': {'E_F0': 0, 'E_N': 0, 'E_CK3': 0, 'E_PS': 0, 'E_TG': 0},
      'mild_braking': {'E_F0': 4, 'E_N': 4, 'E_CK3': 1, 'E_PS': 4, 'E_TG': 4},
      'stop_and_go': {'E_F0': 6, 'E_N': 2, 'E_CK3': 6, 'E_PS': 6, 'E_TG': 6}}

def main(out):
    root = Path(out); root.mkdir(parents=True, exist_ok=True)
    e3b = root / 'e3b'
    for lv, ncs in NC.items():
        for arm, nc in ncs.items():
            for i in range(10):
                ego_x, ego_v, ego_a, lead_x, lead_v, ck = M.braking_run(15.0, 150, 2.0 if i < nc else 6.0, 160.0)
                M.write_run(e3b, 'e3b_%s_%s_c%02d' % (arm, lv, i), 'b%s%02d' % (lv, i), arm, 'lo', 1.0, 15.0, ego_x, ego_v, ego_a,
                            lead_x, lead_v, lambda k: False, contact_k=ck, lead_variant=dict(SPEC[lv]))
    print('written', root)

if __name__ == '__main__':
    main(sys.argv[1])
