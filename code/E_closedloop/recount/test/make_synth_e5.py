"""Tiny synthetic E5 sets for testing e_recount_e5_v01.py (not for results).
usage: python -I -B make_synth_e5.py <out_dir> [tie]
Writes <out_dir>/runs (e5c_ calibration runs on tuning cases, e5_ main runs on 20 main cases) and <out_dir>/settings.json.
Case ids are real ids of the locked table out\\E5_MASKS_v01.json; masks are written by the v04 law. Main runs: two corrupted
(mask, punish_num), one with a wrong pbar_sha256, one with the wrong tracker.
With `tie`: only calibration runs on all 30 tuning cases with contacts 5/30 at g=4, 7/30 at g=8, 0 at g=16 and 32 (g_D must be 4)."""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


S4 = load('make_synth_e4', HERE / 'make_synth_e4.py')
M = S4.M
E_DIR = HERE.parents[1]
GN = 14.96235656
PBAR_DR = '4b373f6e3863028049425bed0aa2eb68a4d1e7bdd2ab8269f2edfb6ff2127560'
CONTACTS_CAL = {4: 10, 8: 6, 16: 4, 32: 1}       # of 20 cases: shares 0.50, 0.30, 0.20, 0.05 -> g_D = 16
CONTACTS_TIE = {4: 5, 8: 7, 16: 0, 32: 0}        # of 30 cases: 5/30 and 7/30 are equidistant from 0.20


def patch_method(run_dir, case, tracker='CANMOT', pbar=PBAR_DR):
    f = run_dir / 'x' / run_dir.name / 'capture' / case / 'ARM_METHOD_v01.json'
    am = json.loads(f.read_text())
    am['tracker'] = tracker
    am['pbar_sha256'] = pbar
    f.write_text(json.dumps(am))


def main(out, tie=False):
    out = Path(out)
    runs = out / 'runs'
    tab = json.load(open(E_DIR / 'out' / 'E5_MASKS_v01.json'))
    ncal = 30 if tie else 20
    tune = tab['tuning_cases'][:ncal]
    spec = CONTACTS_TIE if tie else CONTACTS_CAL
    for g, nc in spec.items():
        for i, case in enumerate(tune):
            ex, ev, ea, lx, lv, ck = M.braking_run(15.0, 150, 2.0 if i < nc else 6.0, 160.0)
            rid = 'e5c_%s_e_f0_g%d' % (case, g)
            M.write_run(runs, rid, case, 'E_F0', None, float(g), 15.0, ex, ev, ea, lx, lv, lambda k: False, contact_k=ck)
            S4.write_dropout(runs / rid, case)
            patch_method(runs / rid, case)
    if tie:
        print('written', out)
        return
    main_c = tab['main_cases'][:20]
    for arm, short, g, nc, bk in (('E_F0', 'e_f0', 16.0, 8, 150), ('E_N', 'e_n', GN, 3, 140)):
        for i, case in enumerate(main_c):
            ex, ev, ea, lx, lv, ck = M.braking_run(15.0, bk, 2.0 if i < nc else 6.0, 160.0)
            rid = 'e5_%s_%s' % (case, short)
            M.write_run(runs, rid, case, arm, 'D', g, 15.0, ex, ev, ea, lx, lv, lambda k: k > 160, contact_k=ck)   # level 'D' as in the real runs
            bad = 'mask' if (arm == 'E_N' and i == 5) else ('punish' if (arm == 'E_F0' and i == 7) else None)
            S4.write_dropout(runs / rid, case, bad)
            patch_method(runs / rid, case,
                         tracker='IMM' if (arm == 'E_N' and i == 11) else 'CANMOT',
                         pbar='0' * 64 if (arm == 'E_F0' and i == 9) else PBAR_DR)
    (out / 'settings.json').write_text(json.dumps(dict(g_D=16, g_N=GN)))
    print('written', out)


if __name__ == '__main__':
    main(sys.argv[1], len(sys.argv) > 2 and sys.argv[2] == 'tie')
