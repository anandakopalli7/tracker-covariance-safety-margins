"""Tiny synthetic E4 run set (and E3 twins) for testing e_recount_v04.py compare_e4 and the E4 exporter. Not for results.
usage: python -I -B make_synth_e4.py <out_dir>      (writes <out_dir>/runs, <out_dir>/jobs, <out_dir>/jobs_incomplete)
Masks are written by the v04 law; three runs are corrupted on purpose (see CORRUPT)."""
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


M = load('make_synth', HERE / 'make_synth.py')
R = load('rv4', HERE.parent / 'e_recount_v04.py')

N_UPD = 69
NCASE = 20
ARMS = ['E_F0', 'E_N', 'E_F0_IMM', 'E_N_IMM']
SHORT = {'E_F0': 'e_f0', 'E_N': 'e_n', 'E_F0_IMM': 'e_f0_imm', 'E_N_IMM': 'e_n_imm'}
# contact cases (first n) per arm and level, E3 and E4
SPEC3 = {('E_F0', 'lo'): 8, ('E_N', 'lo'): 8, ('E_F0_IMM', 'lo'): 8, ('E_N_IMM', 'lo'): 9,
         ('E_F0', 'hi'): 2, ('E_N', 'hi'): 2, ('E_F0_IMM', 'hi'): 2, ('E_N_IMM', 'hi'): 2}
SPEC4 = {('E_F0', 'lo'): 10, ('E_N', 'lo'): 5, ('E_F0_IMM', 'lo'): 10, ('E_N_IMM', 'lo'): 6,
         ('E_F0', 'hi'): 3, ('E_N', 'hi'): 1, ('E_F0_IMM', 'hi'): 3, ('E_N_IMM', 'hi'): 1}
CORRUPT = {('E_N', 'lo', 3): 'mask', ('E_N', 'hi', 4): 'tracker_rows', ('E_F0', 'hi', 5): 'punish'}


def case_id(i):
    return 'c1109_eval_%04d' % (480 + i)


def write_dropout(run_dir, case, corrupt=None):
    cap = run_dir / 'x' / run_dir.name / 'capture' / case
    mask, wins, _, _ = R.dropout_mask(case, N_UPD)
    logged_mask = list(mask)
    punish = 3
    if corrupt == 'mask':
        logged_mask[10] = 1 - logged_mask[10]
    if corrupt == 'punish':
        punish = 1
    am = json.loads((cap / 'ARM_METHOD_v01.json').read_text())
    am['dropout'] = dict(schema='DROPOUT_V01', law='A11D2', law_file_sha256='0'*64, seed=case, case_id=case, n_updates=N_UPD, mask=logged_mask,
                         windows=[list(w) for w in wins], punish_num=punish)
    (cap / 'ARM_METHOD_v01.json').write_text(json.dumps(am))
    rows = []
    for i in range(N_UPD):
        k = 19 + 10 * i
        model = [dict(detection_score=0.7)] * (1 + i % 2)
        masked = bool(mask[i])
        tr = 0 if masked else len(model)
        if corrupt == 'tracker_rows' and i == 12:
            tr = len(model) + 1
        rows.append(dict(k=k, frame=1000 + k, model=model, tracks=[], masked=masked, tracker_rows=tr))
    with open(cap / 'detections.jsonl', 'w') as f:
        f.writelines(json.dumps(r) + '\n' for r in rows)


def main(out):
    out = Path(out)
    runs = out / 'runs'
    jl, jh = [], []
    for (arm, lev), nc in SPEC3.items():
        for i in range(NCASE):
            ex, ev, ea, lx, lv, ck = M.braking_run(15.0, 150, 2.0 if i < nc else 6.0, 160.0)
            M.write_run(runs, 'e3_%s_%s_%s' % (case_id(i), SHORT[arm], lev), case_id(i), arm, lev, 1.0, 15.0, ex, ev, ea, lx, lv,
                        lambda k: False, contact_k=ck)
    for (arm, lev), nc in SPEC4.items():
        for i in range(NCASE):
            decel = 2.0 if i < nc else 6.0
            bk = 150 if arm in ('E_F0', 'E_F0_IMM') else 140
            ex, ev, ea, lx, lv, ck = M.braking_run(15.0, bk, decel, 160.0)
            rid = 'e4_%s_%s_%s' % (case_id(i), SHORT[arm], lev)
            M.write_run(runs, rid, case_id(i), arm, lev, 1.0, 15.0, ex, ev, ea, lx, lv, lambda k: k > 160 and decel > 3, contact_k=ck)
            write_dropout(runs / rid, case_id(i), CORRUPT.get((arm, lev, i)))
            (jl if lev == 'lo' else jh).append(dict(id=rid, case=case_id(i), arm=arm))
    for name, extra in (('jobs', []), ('jobs_incomplete', [dict(id='e4_c1109_eval_9999_e_n_hi', case='c1109_eval_9999', arm='E_N')])):
        d = out / name
        d.mkdir(parents=True, exist_ok=True)
        (d / 'JOBS_E4L_pod1_v01.json').write_text(json.dumps(dict(jobs=[dict(id='ctl_x', phase='A1')] + jl)))
        (d / 'JOBS_E4H_pod1_v01.json').write_text(json.dumps(dict(jobs=jh + extra)))
    print('written', out)


if __name__ == '__main__':
    main(sys.argv[1])
