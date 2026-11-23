"""Package E, set E5 (A12 §6): job lists for packet_e_v05 (F0_D = E_F0 with P-bar_DR; N = E_N; A11 law A11D2; punish_num 3).
Reuses the frozen builder make_jobs_e_v01.py (admission, controls, dealing by case).

  e5c  calibration (A12 §6.4): E_F0 at g in {4, 8, 16, 32} on the 30 lead-braking tuning cases of E2 (out\\E5_MASKS_v01.json
       'tuning_cases'), 120 runs, dealt by case. Also the smoke of packet v05 (A1 admission and controls on every pod).
  e5   main (A12 §6.6): E_F0 at g_D and E_N at g_N on the 135 never-run cases ('main_cases'), 270 runs, dealt by case.
       --settings out\\E5_SETTINGS_v01.json (g_D, g_N); refused unless its SHA-256 is recorded in revision_v13\\LOCK_A12b.txt.

python -I make_jobs_e5_v01.py e5c --pods claude-v13e-21,...      |   e5 --pods claude-v13e-31,... --settings ..\\out\\E5_SETTINGS_v01.json
"""
import argparse, importlib.util, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
E = HERE.parent
spec = importlib.util.spec_from_file_location('mj', HERE / 'make_jobs_e_v01.py')
mj = importlib.util.module_from_spec(spec); spec.loader.exec_module(mj)
MASKS = E / 'out' / 'E5_MASKS_v01.json'
LOCK_B = E.parents[1] / 'LOCK_A12b.txt'
CAL_G = (4., 8., 16., 32.)
KNOBS = dict(dropout='A11D2', punish_num=3)


def job(jid, cid, arm, phase, g, level):
    j = mj.e_job(jid, cid, arm, phase, g=g, level=level, tracker='CANMOT'); j.update(KNOBS); return j


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('stage', choices=('e5c', 'e5')); ap.add_argument('--pods', required=True)
    ap.add_argument('--settings'); ap.add_argument('--tag', default='v01')
    a = ap.parse_args(); pods = a.pods.split(',')
    m = json.loads(MASKS.read_text(encoding='utf-8'))
    if a.stage == 'e5c':
        ids = m['tuning_cases']; assert len(ids) == 30
        per_case = {cid: [job(f'e5c_{cid}_e_f0_g{mj.gtag(g)}', cid, 'E_F0', 'E5C', g, 'cal') for g in CAL_G] for cid in ids}
        note = 'calibration (A12 §6.4): E_F0 (F0_D, P-bar_DR) at g in {4, 8, 16, 32}, 120 runs'
    else:
        assert a.settings, 'e5 needs --settings'
        s = json.loads(pathlib.Path(a.settings).read_text(encoding='utf-8')); s_sha = mj.sha(a.settings)
        assert LOCK_B.exists() and s_sha in LOCK_B.read_text(encoding='utf-8'), 'the settings file is not recorded in LOCK_A12b.txt'
        ids = m['main_cases']; assert len(ids) == 135
        per_case = {cid: [job(f'e5_{cid}_e_f0', cid, 'E_F0', 'E5', s['g_D'], 'D'), job(f'e5_{cid}_e_n', cid, 'E_N', 'E5', s['g_N'], 'D')] for cid in ids}
        note = f'main (A12 §6.6): E_F0 at g_D {s["g_D"]} and E_N at g_N {s["g_N"]!r}, 270 runs; settings sha256 {s_sha}'
    order = [ids[i] for i in sorted(range(len(ids)), key=lambda i: (i % 3, i))]
    lists = {pod: mj.config(f'Revision v13 package E set E5 {a.stage} on {pod}: {n} runs; {note}; packet_e_v05; masks table sha256 {mj.sha(MASKS)}.', lst)
             for pod, (lst, n) in mj.deal_by_case(pods, order, per_case, a.stage, a.tag).items()}
    summary = {}
    for pod, cfg in lists.items():
        cfg['made_by_e5'] = dict(script='make_jobs_e5_v01.py', sha256=mj.sha(__file__))
        path = E / 'jobs' / f'JOBS_{a.stage.upper()}_{pod}_{a.tag}.json'
        with open(path, 'x', encoding='utf-8', newline='\n') as f: f.write(json.dumps(cfg, indent=1) + '\n')
        summary[pod] = dict(file=path.name, sha256=mj.sha(path), jobs=len(cfg['jobs']), study=sum(1 for j in cfg['jobs'] if j['id'].startswith(('e5c_', 'e5_'))))
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
