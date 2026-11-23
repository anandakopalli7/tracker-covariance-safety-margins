"""Package E, set E6 (A13 §E6): job lists for packet_e_v05 (F0_D = E_F0 with P-bar_DR; A11 law A11D2; punish_num 3).
Reuses the frozen builder make_jobs_e_v01.py (e_job, admission, config, the crash control job).

  e6   E_F0 at g = 8 (level D8) and g = 16 (level D16) on the 135 E5 main cases (out\\E5_MASKS_v01.json 'main_cases'),
       270 runs, phase E6. Cases are dealt round-robin over E5's speed-interleaved order, so all of a case's runs are on one pod.
       Each list: A1 admission (crash, benign), a crash control, ALL its g = 8 jobs, then ALL its g = 16 jobs, with a crash
       control every 50 study jobs (A13 §E6.3: a balance stop still leaves the g = 8 arm).

python -I make_jobs_e6_v01.py --pods claude-v13e-41,claude-v13e-42,claude-v13e-43,claude-v13e-44,claude-v13e-45,claude-v13e-46
"""
import argparse, importlib.util, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
E = HERE.parent
spec = importlib.util.spec_from_file_location('mj', HERE / 'make_jobs_e_v01.py')
mj = importlib.util.module_from_spec(spec); spec.loader.exec_module(mj)
MASKS = E / 'out' / 'E5_MASKS_v01.json'
MASKS_SHA = '010595907805f7434ad4fc04f963439fa3756e57406de983053e66910822d770'
SCALES = ((8., 'D8'), (16., 'D16'))
KNOBS = dict(dropout='A11D2', punish_num=3)


def job(cid, g, level):
    j = mj.e_job(f'e6_{cid}_e_f0_g{mj.gtag(g)}', cid, 'E_F0', 'E6', g=g, level=level, tracker='CANMOT'); j.update(KNOBS); return j


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--pods', required=True); ap.add_argument('--tag', default='v01')
    a = ap.parse_args(); pods = a.pods.split(',')
    assert mj.sha(MASKS) == MASKS_SHA, 'mask table differs from the locked E5_MASKS_v01.json'
    ids = json.loads(MASKS.read_text(encoding='utf-8'))['main_cases']; assert len(ids) == 135 and len(set(ids)) == 135
    order = [ids[i] for i in sorted(range(len(ids)), key=lambda i: (i % 3, i))]          # as E5's lists
    summary = {}
    for k, pod in enumerate(pods):
        sfx = pod[-2:]
        mine = [cid for i, cid in enumerate(order) if i % len(pods) == k]
        study = [job(cid, g, lv) for g, lv in SCALES for cid in mine]                     # all g = 8 first, then g = 16
        lst = mj.admission('e6', sfx, a.tag); n = 0
        lst.append(dict(mj.p1.job('x', 'crash', 'CTL'), id=f'ctl_e6_{sfx}_{a.tag}_{n:03d}'))
        for i, j in enumerate(study):
            lst.append(j)
            if (i + 1) % mj.CTL_EVERY == 0:
                n += 1; lst.append(dict(mj.p1.job('x', 'crash', 'CTL'), id=f'ctl_e6_{sfx}_{a.tag}_{n:03d}'))
        cfg = mj.config(f'Revision v13 package E set E6 (A13 §E6) on {pod}: {len(study)} runs ({len(mine)} cases x g in {{8, 16}}, '
                        f'all g = 8 first); E_F0 (F0_D, P-bar_DR), A11D2, punish_num 3; packet_e_v05; masks table sha256 {MASKS_SHA}.', lst)
        cfg['made_by_e6'] = dict(script='make_jobs_e6_v01.py', sha256=mj.sha(__file__))
        path = E / 'jobs' / f'JOBS_E6_{pod}_{a.tag}.json'
        with open(path, 'x', encoding='utf-8', newline='\n') as f: f.write(json.dumps(cfg, indent=1) + '\n')
        summary[pod] = dict(file=path.name, sha256=mj.sha(path), jobs=len(lst), study=len(study), cases=len(mine))
    assert sum(v['study'] for v in summary.values()) == 270
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
