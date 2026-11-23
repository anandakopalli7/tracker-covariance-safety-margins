"""Package C: the remaining study jobs after the volume quota failure (19 Nov ~14:55 EST), as lists *_v02.

From each pod's v01 list, drop the study jobs already published on the volume (status CAPTURED_AND_REVIEWED in their
receipt) and those salvaged on the pod (tools/salvage_local_v13.py); keep the rest in the same order, unchanged (same ids,
case, arm, alpha, beta, keep_raw). One crash control first (and after every 50 study jobs). volume_folder is the absolute
path /opt/claude_v13_local: worker_main_v01.volume_root joins '/workspace' with it, which pathlib resolves to the
pod-local folder, so archives, receipts and status go to the pod's own disk (the packet is unchanged). A1 admission is not
repeated: each pod passed it at the start of v01.
Input: pods/<name>/SURVEY_quota.txt and SALVAGE_v13.json. Usage: python -I make_jobs_c_v13_remaining.py
"""
import hashlib, importlib.util, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('mjc', HERE / 'make_jobs_c_v13.py'); mjc = importlib.util.module_from_spec(spec); spec.loader.exec_module(mjc)
v1 = mjc.v1


def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    survey = {}
    for l in (HERE / 'pods' / 'claude-v13cd-01' / 'SURVEY_quota.txt').read_text().splitlines():
        k, v = l.split(' ', 1); survey[k] = json.loads(v)
    published = {r for r, s in survey['VOLUME_PUBLISHED'] if s == 'CAPTURED_AND_REVIEWED'}
    salvaged = set()
    for n in range(1, 7):
        salvaged |= {x['run'] for x in json.loads((HERE / 'pods' / f'claude-v13cd-0{n}' / 'SALVAGE_v13.json').read_text().strip().splitlines()[-1])['salvaged']}
    total_rem = 0; out = {}
    for n in range(1, 7):
        name = f'claude-v13cd-0{n}'; sfx = name[-2:]
        src = HERE / 'jobs' / f'JOBS_PC13_{name}_v01.json'; cfg = json.loads(src.read_text(encoding='utf-8'))
        rem = [j for j in cfg['jobs'] if j['role'] == 'eval' and j['id'] not in published and j['id'] not in salvaged]
        lst = [dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_pc13_{sfx}_v02_000')]
        for i, j in enumerate(rem):
            lst.append(j)
            if (i + 1) % 50 == 0: lst.append(dict(v1.p1.job('x', 'crash', 'CTL'), id=f'ctl_pc13_{sfx}_v02_{(i + 1) // 50:03d}'))
        new = dict(cfg); new['volume_folder'] = '/opt/claude_v13_local'; new['jobs'] = lst
        new['note'] = (f'Revision v13 package C, pod {name}: the {len(rem)} study jobs of {src.name} not yet captured when the network volume '
                       'hit its quota (19 Nov ~14:55 EST); archives to the pod-local disk /opt/claude_v13_local; packet_main_v03 unchanged.')
        new['made_by'] = dict(script='make_jobs_c_v13_remaining.py', sha256=sha(__file__), from_list=src.name, from_list_sha256=sha(src))
        path = HERE / 'jobs' / f'JOBS_PC13_{name}_v02.json'
        with open(path, 'x', encoding='utf-8', newline='\n') as f: f.write(json.dumps(new, indent=1) + '\n')
        out[name] = dict(remaining=len(rem), file=path.name, sha256=sha(path)); total_rem += len(rem)
    assert total_rem + len({r for r in published if r.startswith('pc13_')}) + len(salvaged) == 210, total_rem
    print(json.dumps(dict(published_study=len({r for r in published if r.startswith('pc13_')}), salvaged=len(salvaged), remaining=total_rem, lists=out), indent=1))


if __name__ == '__main__':
    main()
