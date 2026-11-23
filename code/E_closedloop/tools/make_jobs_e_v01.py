"""Package E job lists (revision v13, A10 section 7). Control jobs come from P\\03_runbook\\main_sources_v01\\
make_phase1_jobs_v01.py (imported read only), so they are built by the same code as every earlier list.

Stages
  e1s  one pod, first list (E0 pod integration check, before the brake test): A1 admission controls (crash, benign;
       references read from the smoke SUMMARY files), then one engineering smoke run per CANMOT arm on the lead-braking
       tuning case c1109_tune_0000 (design data; only the pipeline and the review status are read, no outcome is analysed).
  e1   same pod, second list, launched only after e1s passed: the brake test (E_BRAKE, forced fallback from decision tick
       199, i.e. 5 s into the assessment, as the stand-in's STOP mode with its wall from k = 199) on the benign tuning
       cases c1109_tune_0023 / 0011 / 0005 (5 / 10 / 15 m/s). A failure of e1s is a build fault (E0), not a brake attempt.
  e2   F0 calibration (A10 7.1): the 30 lead-braking tuning cases (role tune, ascending id: c1109_tune_0000..0174, step 6)
       x g in {0, 0.25, 1, 4, 16, 64} = 180 runs (g = 0 is the zero margin), dealt to --pods in turn; A1 admission
       (crash, benign) and a crash control every 50 study jobs on each pod.
  e3, e3b  written after LOCK_A10_2b / LOCK_A10_2 (separate function, matched settings read from the lock files).

Usage: python -I make_jobs_e_v01.py e1s --pods claude-v13e-01 [--tag v01]   (then e1 with --tag a1, a2 for the attempts)
       python -I make_jobs_e_v01.py e2 --pods claude-v13e-01,claude-v13e-02 [--tag v01]
Outputs (never overwritten): ..\\jobs\\JOBS_<STAGE>_<pod>_<tag>.json
"""
import argparse, hashlib, importlib.util, json, pathlib

E = pathlib.Path(__file__).resolve().parents[1]
P = pathlib.Path(r'<library folder>')
MAIN_SOURCES = P / '03_runbook' / 'main_sources_v01'
PROTOCOL = P / '06_phase0' / 'scenarios' / 'DEVELOPMENT_PROTOCOL_MAIN_v01.json'
PROTOCOL_SHA256 = '32d683a0a8ca2e91ff0245759ad78b43e7953c33bd12847c5193cafcdaa5735d'
VOLUME_FOLDER = 'claude_v13_e_v01'
BRAKE_CASES = {5: 'c1109_tune_0023', 10: 'c1109_tune_0011', 15: 'c1109_tune_0005'}
BRAKE_FROM_K = 199
SMOKE_CASE = 'c1109_tune_0000'
E2_G = (0., 0.25, 1., 4., 16., 64.)
CTL_EVERY = 50

spec = importlib.util.spec_from_file_location('mp1', MAIN_SOURCES / 'make_phase1_jobs_v01.py')
p1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(p1)


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def protocol_cases():
    raw = PROTOCOL.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PROTOCOL_SHA256
    return {c['id']: c for c in json.loads(raw)['cases']}


def gtag(g):
    return ('%g' % g).replace('.', 'p')


def e_job(jid, case, arm, phase, role='e', g=None, triple=None, brake_from_k=None, level=None, tracker='CANMOT', note=None):
    j = dict(id=jid, case=case, arm=arm, phase=phase, role=role, scenario=case, keep_raw=False, tracker=tracker)
    if g is not None: j['g'] = float(g)
    if triple is not None: j['triple'] = [float(x) for x in triple]
    if brake_from_k is not None: j['brake_from_k'] = int(brake_from_k)
    if level is not None: j['level'] = level
    if note: j['note'] = note
    return j


def config(note, jobs, timeout=600, max_attempts=2):
    return dict(schema='CLAUDE_MAIN_JOBS_V01', protocol='DEVELOPMENT_PROTOCOL_SMOKE_v01.json', volume_folder=VOLUME_FOLDER,
                capture_timeout_s=timeout, review_timeout_s=600, actor_review_timeout_s=180, server_ready_timeout_s=120,
                concurrent_start_stagger_s=15, max_attempts=max_attempts, protocol_main_sha256=PROTOCOL_SHA256, note=note,
                made_by=dict(script='make_jobs_e_v01.py', sha256=sha(__file__),
                             imports_read_only='make_phase1_jobs_v01.py ' + sha(MAIN_SOURCES / 'make_phase1_jobs_v01.py')), jobs=jobs)


def admission(stage, sfx, tag):
    return [dict(p1.job('x', 'crash', 'A1'), id=f'a1e13_{stage}_{sfx}_{tag}_crash'), dict(p1.job('x', 'benign', 'A1'), id=f'a1e13_{stage}_{sfx}_{tag}_benign')]


SMOKE = [('E_Z', dict()), ('E_F0', dict(g=1.)), ('E_N', dict(g=1.)), ('E_CK3', dict(g=1.)), ('E_TG', dict(g=1.)),
         ('E_PS', dict(triple=[0.25, 1., 4.]))]


def stage_e1s(pods, tag, cases):
    assert len(pods) == 1
    pod = pods[0]; sfx = pod[-2:]
    assert cases[SMOKE_CASE]['draw']['family'] == 'lead_braking' and cases[SMOKE_CASE]['role'] == 'tune'
    jobs = admission('e1s', sfx, tag)
    for arm, kw in SMOKE:
        jobs.append(e_job(f'e1s_{tag}_{arm.lower()}_{SMOKE_CASE}', SMOKE_CASE, arm, 'E1S', role='smoke', note='E0 pod integration smoke run (design data)', **kw))
    return {pod: config(f'Revision v13 package E, E0 pod integration check on {pod}: A1 admission (crash, benign), '
                        f'{len(SMOKE)} smoke runs; packet_e; volume folder {VOLUME_FOLDER}; one attempt per job (no worker retry).', jobs, max_attempts=1)}


def stage_e1(pods, tag, cases):
    assert len(pods) == 1
    pod = pods[0]
    for v, c in BRAKE_CASES.items():
        assert cases[c]['draw']['family'] == 'benign' and cases[c]['desired_mps'] == v and cases[c]['role'] == 'tune'
    jobs = [e_job(f'e1_{tag}_brake_{v:02d}_{c}', c, 'E_BRAKE', 'E1', brake_from_k=BRAKE_FROM_K, note='brake test (A10 7.1 E1)')
            for v, c in BRAKE_CASES.items()]
    return {pod: config(f'Revision v13 package E stage E1 (brake test, attempt list {tag}) on {pod}: 3 brake runs (5, 10, 15 m/s); '
                        f'packet_e; volume folder {VOLUME_FOLDER}; one attempt per job: a second attempt is a new list after a fault, decided by a person.', jobs, max_attempts=1)}


V03_SMOKE = [('E_F0_IMM', 'c1109_tune_0000', dict(g=1., tracker='IMM')), ('E_N_IMM', 'c1109_tune_0000', dict(g=1., tracker='IMM')),
             ('E_F0', 'd1v13pilot_stop_and_go', dict(g=1.)), ('E_PS', 'd1v13pilot_mild_braking', dict(triple=[0.25, 1., 4.]))]


def stage_v03s(pods, tag, cases):
    """packet_e_v03 smoke (review M4): the two IMM arms on tuning case c1109_tune_0000 and two arms on D1 pilot cases (session
    CD's non-study pilots), after A1 admission; design data / pilots only, no outcome analysed; one attempt per job."""
    assert len(pods) == 1
    pod = pods[0]; sfx = pod[-2:]
    jobs = admission('v03s', sfx, tag)
    for arm, case, kw in V03_SMOKE:
        assert case in cases, case
        jobs.append(e_job(f'v03s_{tag}_{arm.lower()}_{case}', case, arm, 'V03S', role='smoke', note='packet_e_v03 smoke (IMM arms, D1 lead variant)', **kw))
    return {pod: config(f'Revision v13 package E: packet_e_v03 smoke on {pod} (IMM arms, D1 pilots); one attempt per job.', jobs, max_attempts=1)}


def stage_e2(pods, tag, cases):
    tune = sorted((c for c in cases.values() if c.get('role') == 'tune' and c['draw']['family'] == 'lead_braking'), key=lambda c: c['id'])
    assert len(tune) == 30 and tune[0]['id'] == 'c1109_tune_0000' and tune[-1]['id'] == 'c1109_tune_0174'
    assert [int(c['id'][-4:]) for c in tune] == list(range(0, 175, 6))
    study = []
    for c in tune:
        for g in E2_G:
            arm = 'E_F0'
            study.append(e_job(f'e2_{c["id"]}_f0_g{gtag(g)}', c['id'], arm, 'E2', g=g, note='F0 calibration (A10 7.1 E2)'))
    assert len(study) == 180 == len({j['id'] for j in study})
    # Deal so every pod gets every g and a spread of cases: job i -> pod (i + i // 6) % n
    out = {}
    for k, pod in enumerate(pods):
        sfx = pod[-2:]
        mine = [j for i, j in enumerate(study) if (i + i // 6) % len(pods) == k]
        lst = admission('e2', sfx, tag); n = 0
        lst.append(dict(p1.job('x', 'crash', 'CTL'), id=f'ctl_e2_{sfx}_{tag}_{n:03d}'))
        for i, j in enumerate(mine):
            lst.append(j)
            if (i + 1) % CTL_EVERY == 0:
                n += 1; lst.append(dict(p1.job('x', 'crash', 'CTL'), id=f'ctl_e2_{sfx}_{tag}_{n:03d}'))
        out[pod] = config(f'Revision v13 package E stage E2 (F0 calibration, A10 7.1) on {pod} ({k + 1} of {len(pods)}): '
                          f'{len(mine)} of 180 study jobs; packet_e; volume folder {VOLUME_FOLDER}.', lst)
    return out


C_CASES = pathlib.Path(r'ARS_TRIAL\revision_v13\work\CD_capture\CASES_C_v13.json')
D1_CASES = pathlib.Path(r'ARS_TRIAL\revision_v13\work\CD_capture\d1\CASES_D1_v13.json')
E3_ARMS = ('E_F0', 'E_N', 'E_CK3', 'E_TG', 'E_PS', 'E_F0_IMM', 'E_N_IMM')
E3B_ARMS = ('E_F0', 'E_N', 'E_CK3', 'E_PS', 'E_TG')
MATCH_KEY = {'E_N': 'N', 'E_CK3': 'CK3', 'E_TG': 'TG', 'E_PS': 'PS', 'E_F0_IMM': 'F0_IMM', 'E_N_IMM': 'N_IMM'}


def e3_cases(cases, replacements=None):
    """A10 7.1 E3: the next 20 lead-braking evaluation cases per speed after C's, in id order. `replacements`: per speed, the
    replacement cases C used (from CD's note), which E3 must skip."""
    cc = json.loads(C_CASES.read_text(encoding='utf-8'))
    out = []
    for v in (5, 10, 15):
        pool = sorted(c['id'] for c in cases.values() if c.get('role') == 'eval' and c['draw']['family'] == 'lead_braking' and c['desired_mps'] == v)
        used = sorted(x['case'] for x in cc['cases'] if x['family'] == 'lead_braking' and x['desired_mps'] == v)
        repl = list((replacements or {}).get(str(v), []))
        assert pool[:35] == used, 'C case list is not the first 35 in id order'
        last = max(pool.index(c) for c in used + repl)
        out += pool[last + 1:last + 21]
    assert len(out) == 60 and len(set(out)) == 60
    return out


def arm_knobs(arm, level, m):
    st = m['settings'][level]
    if arm == 'E_F0': return dict(g=st['g_F0'])
    if arm == 'E_PS':
        t = st['arms']['PS']['triple']
        assert t is not None, 'PS triple missing'
        return dict(triple=t)
    return dict(g=st['arms'][MATCH_KEY[arm]]['g'])


def deal_by_case(pods, case_ids, per_case, stage, tag):
    """All runs of a case go to one pod (pairs stay together); cases dealt round-robin; A1 admission and a crash control
    first, then one every CTL_EVERY study jobs."""
    out = {}
    for k, pod in enumerate(pods):
        sfx = pod[-2:]
        mine = [j for i, cid in enumerate(case_ids) if i % len(pods) == k for j in per_case[cid]]
        lst = admission(stage, sfx, tag); n = 0
        lst.append(dict(p1.job('x', 'crash', 'CTL'), id=f'ctl_{stage}_{sfx}_{tag}_{n:03d}'))
        for i, j in enumerate(mine):
            lst.append(j)
            if (i + 1) % CTL_EVERY == 0:
                n += 1; lst.append(dict(p1.job('x', 'crash', 'CTL'), id=f'ctl_{stage}_{sfx}_{tag}_{n:03d}'))
        out[pod] = (lst, len(mine))
    return out


def stage_e3(pods, tag, cases, m, replacements=None):
    ids = e3_cases(cases, replacements)
    per_case = {}
    for cid in ids:
        jobs = [e_job(f'e3_{cid}_e_z', cid, 'E_Z', 'E3', note='zero margin, once per case')]
        for lv in ('lo', 'hi'):
            for arm in E3_ARMS:
                jobs.append(e_job(f'e3_{cid}_{arm.lower()}_{lv}', cid, arm, 'E3', level=lv, tracker='IMM' if 'IMM' in arm else 'CANMOT', **arm_knobs(arm, lv, m)))
        per_case[cid] = jobs
    assert sum(len(v) for v in per_case.values()) == 900
    order = [ids[i] for i in sorted(range(60), key=lambda i: (i % 20, i // 20))]      # the three speeds interleaved
    return {pod: config(f'Revision v13 package E stage E3 (A10 7.1) on {pod}: {n} of 900 runs; matched settings sha256 {m["sha256"]}; '
                        f'volume folder {VOLUME_FOLDER}.', lst) for pod, (lst, n) in deal_by_case(pods, order, per_case, 'e3', tag).items()}


def stage_e3b(pods, tag, cases, m, replacements=None):
    d1 = json.loads(D1_CASES.read_text(encoding='utf-8'))
    ids = sorted(c['id'] for c in d1['cases'] if c.get('role') == 'd1_e3b')
    assert len(ids) == 60, len(ids)
    per_case = {cid: [e_job(f'e3b_{cid}_{arm.lower()}_lo', cid, arm, 'E3B', level='lo', **arm_knobs(arm, 'lo', m)) for arm in E3B_ARMS] for cid in ids}
    return {pod: config(f'Revision v13 package E stage E3b (A10 7.1) on {pod}: {n} of 300 runs; matched settings sha256 {m["sha256"]}; '
                        f'volume folder {VOLUME_FOLDER}.', lst) for pod, (lst, n) in deal_by_case(pods, ids, per_case, 'e3b', tag).items()}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('stage', choices=('e1s', 'e1', 'v03s', 'e2', 'e3', 'e3b')); ap.add_argument('--pods', required=True); ap.add_argument('--tag', default='v01')
    ap.add_argument('--matched', help='e3/e3b: the matched-settings JSON whose SHA-256 is recorded in LOCK_A10_2b.txt')
    ap.add_argument('--c-replacements', help='e3: JSON {"5": [...], "10": [...], "15": [...]} of replacement cases C used')
    a = ap.parse_args()
    pods = [p for p in a.pods.split(',') if p]
    cases = protocol_cases()
    if a.stage in ('e3', 'e3b'):
        lock2b = E.parent / 'locks' / 'LOCK_A10_2b.txt'
        assert lock2b.exists(), 'LOCK_A10_2b.txt must exist before the E3 / E3b lists are written'
        m = json.loads(pathlib.Path(a.matched).read_text(encoding='utf-8')); m['sha256'] = sha(a.matched)
        assert m['sha256'] in lock2b.read_text(encoding='utf-8'), 'the matched-settings file is not the one recorded in LOCK_A10_2b'
        repl = json.loads(a.c_replacements) if a.c_replacements else None
        if a.stage == 'e3b':
            cases = {**cases, **{c['id']: c for c in json.loads(D1_CASES.read_text(encoding='utf-8'))['cases']}}
        lists = (stage_e3 if a.stage == 'e3' else stage_e3b)(pods, a.tag, cases, m, repl)
    else:
        if a.stage == 'v03s':
            cases = {**cases, **{c['id']: c for c in json.loads(D1_CASES.read_text(encoding='utf-8'))['cases']}}
        lists = dict(e1s=stage_e1s, e1=stage_e1, v03s=stage_v03s, e2=stage_e2)[a.stage](pods, a.tag, cases)
    outdir = E / 'jobs'; outdir.mkdir(exist_ok=True); summary = {}
    for pod, cfg in lists.items():
        path = outdir / f'JOBS_{a.stage.upper()}_{pod}_{a.tag}.json'
        with open(path, 'x', encoding='utf-8', newline='\n') as f: f.write(json.dumps(cfg, indent=1) + '\n')
        summary[pod] = dict(file=path.name, sha256=sha(path), jobs=len(cfg['jobs']))
    print(json.dumps(summary, indent=1))


if __name__ == '__main__':
    main()
