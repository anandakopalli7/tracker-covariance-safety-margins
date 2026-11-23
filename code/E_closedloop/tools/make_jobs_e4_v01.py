"""Package E, set E4 (A11 §6d, closed-loop detection dropout): job lists for packet_e_v04. Reuses the frozen builder
make_jobs_e_v01.py (admission, controls, dealing by case, matched settings from LOCK_A10_2b) and adds the dropout knobs.

  e4s  smoke, one pod: A1 admission + a control; 4 masked runs (E_F0, E_N, E_F0_IMM, E_N_IMM at lo) on c1109_tune_0000;
       1 UNMASKED E_F0-lo run of E3 case c1109_eval_0480 (no dropout knobs) that must reproduce E3's record bit-identically.
  e4l  stage L (pre-registered first): the 4 arms at lo on the 60 E3 cases, 240 runs, dealt by case over the pods.
  e4h  stage H: the same at hi, 240 runs, same dealing; a pod starts its H list only after its L list is finished.
Every E4 study job carries dropout='A11D2' and punish_num=3 (A11 §6c) (all arms alike).

python -I make_jobs_e4_v01.py <e4s|e4l|e4h> --pods claude-v13e-11,... --matched out\\E2_MATCHED_v01.json --punish-num N [--tag v01]
"""
import argparse, importlib.util, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
E = HERE.parent
spec = importlib.util.spec_from_file_location('mj', HERE / 'make_jobs_e_v01.py')
mj = importlib.util.module_from_spec(spec); spec.loader.exec_module(mj)

E4_ARMS = ('E_F0', 'E_N', 'E_F0_IMM', 'E_N_IMM')
REPRO = ('c1109_eval_0480', 'E_F0', 'lo')


def e3_case_ids():
    """The 60 E3 cases, read from the frozen E3 lists (FREEZE_E_ADDENDUM_v01), in E3's dealing order."""
    ids = []
    for n in '456789':
        for j in json.loads((E / 'jobs' / f'JOBS_E3_claude-v13e-0{n}_v01.json').read_text(encoding='utf-8'))['jobs']:
            if j['arm'].startswith('E_') and j['case'] not in ids: ids.append(j['case'])
    assert len(ids) == 60
    return ids


def e4_job(cid, arm, lv, m, punish):
    j = mj.e_job(f'e4_{cid}_{arm.lower()}_{lv}', cid, arm, 'E4', level=lv, tracker='IMM' if 'IMM' in arm else 'CANMOT', **mj.arm_knobs(arm, lv, m))
    j.update(dropout='A11D2', punish_num=int(punish))
    return j


def stage_main(pods, tag, m, punish, lv):
    ids = e3_case_ids()
    per_case = {cid: [e4_job(cid, arm, lv, m, punish) for arm in E4_ARMS] for cid in ids}
    stage = 'e4' + lv[0]
    return {pod: mj.config(f'Revision v13 package E set E4 stage {lv.upper()} (A11 §6d) on {pod}: {n} of 240 runs; dropout A11D2, punish_num {punish}; '
                           f'matched settings sha256 {m["sha256"]}; volume folder {mj.VOLUME_FOLDER}.', lst)
            for pod, (lst, n) in mj.deal_by_case(pods, ids, per_case, stage, tag).items()}


def stage_smoke(pods, tag, m, punish):
    assert len(pods) == 1
    sfx = pods[0][-2:]
    jobs = mj.admission('e4s', sfx, tag) + [dict(mj.p1.job('x', 'crash', 'CTL'), id=f'ctl_e4s_{sfx}_{tag}_000')]
    jobs += [dict(e4_job(mj.SMOKE_CASE, arm, 'lo', m, punish), id=f'e4s_{tag}_{arm.lower()}_lo') for arm in E4_ARMS]
    cid, arm, lv = REPRO
    rj = mj.e_job(f'e4s_{tag}_repro_e3_{cid}_{arm.lower()}_{lv}', cid, arm, 'E4S', level=lv, tracker='CANMOT', **mj.arm_knobs(arm, lv, m),
                  note=f'unmasked; must reproduce e3_{cid}_{arm.lower()}_{lv} bit-identically')
    jobs.append(rj)
    return {pods[0]: mj.config(f'Revision v13 package E set E4 smoke (A11 §6d) on {pods[0]}: 4 masked runs + 1 E3 reproduction; punish_num {punish}.',
                               jobs, max_attempts=1)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('stage', choices=('e4s', 'e4l', 'e4h')); ap.add_argument('--pods', required=True)
    ap.add_argument('--matched', required=True); ap.add_argument('--punish-num', type=int, required=True); ap.add_argument('--tag', default='v01')
    a = ap.parse_args()
    assert a.punish_num == 3, 'A11 §6c: punish_num is 3 for every arm (pinned)'
    lock2b = E.parent / 'locks' / 'LOCK_A10_2b.txt'
    m = json.loads(pathlib.Path(a.matched).read_text(encoding='utf-8')); m['sha256'] = mj.sha(a.matched)
    assert m['sha256'] in lock2b.read_text(encoding='utf-8'), 'the matched-settings file is not the one recorded in LOCK_A10_2b'
    pods = a.pods.split(',')
    lists = stage_smoke(pods, a.tag, m, a.punish_num) if a.stage == 'e4s' else stage_main(pods, a.tag, m, a.punish_num, 'lo' if a.stage == 'e4l' else 'hi')
    outdir = E / 'jobs'; summary = {}
    for pod, cfg in lists.items():
        cfg['made_by_e4'] = dict(script='make_jobs_e4_v01.py', sha256=mj.sha(__file__))
        path = outdir / f'JOBS_{a.stage.upper()}_{pod}_{a.tag}.json'
        with open(path, 'x', encoding='utf-8', newline='\n') as f: f.write(json.dumps(cfg, indent=1) + '\n')
        summary[pod] = dict(file=path.name, sha256=mj.sha(path), jobs=len(cfg['jobs']), study=sum(1 for j in cfg['jobs'] if j['id'].startswith(('e4_', 'e4s_'))))
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
