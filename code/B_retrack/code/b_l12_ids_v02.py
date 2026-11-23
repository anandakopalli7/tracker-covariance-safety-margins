r"""v02 (22 Nov 2026 00:45 EST, Claude Opus 5.5): b_l12_ids_v01.py plus session CD's layout of the new runs (CD, 00:44): the logs of a
job sit in CD_capture\runs\<rid>\ where <rid> is the capture run id, which differs from the job id for a run captured on an allowed
retry (suffix __p1 / __r1); CD_capture\l12\out\L12_RUNS_v13.json maps each of the 150 analysed job ids to its <rid>. Arrays stay named
by job id. Everything that touches a new run's folder resolves the job id through that map (REFUSED while the map does not exist).
  markers <out folder>   writes <out folder>\<job id>\LOGS_OK (a copy of the run's LOGS_OK) for every analysed job id whose run has
                         LOGS_OK, so that the frozen second programs (recount_fresh\imm2_v04.py, modeprob2_v01.py), which test
                         <runs root>\<job id>\LOGS_OK, see exactly the same set when given <out folder> as their runs root.
Run ids: l12_run_ids() exactly as v01 (CD's rule: the 150 non-reserve rows of CASES_L12_v13.json with REPLACEMENTS_L12_v13.json).
Usage: python -I -B -X utf8 b_l12_ids_v02.py markers <out folder> [<runs root, default CD_capture\runs>]
"""
import json, pathlib, sys

WORK = pathlib.Path(__file__).resolve().parents[2]
CDL = WORK / 'CD_capture'
L12 = CDL / 'l12'
MAPF = L12 / 'out' / 'L12_RUNS_v13.json'
RUNS = CDL / 'runs'


def l12_run_ids():
    X = json.loads((L12 / 'CASES_L12_v13.json').read_text(encoding='utf-8'))
    rp = L12 / 'REPLACEMENTS_L12_v13.json'
    rep = json.loads(rp.read_text(encoding='utf-8'))['replacements'] if rp.is_file() else {}
    rows = [r for r in X['cases'] if not r['reserve']]
    assert len(rows) == 150, len(rows)
    res = {r['case']: r for r in X['cases'] if r['reserve']}
    for r in rows:
        if r['case'] in rep:
            assert res[rep[r['case']]]['desired_mps'] == r['desired_mps']
    return sorted('pl12_%s_native' % rep.get(r['case'], r['case']) for r in rows)


def job_map():
    """job id -> capture run id folder, from CD's L12_RUNS_v13.json (several plausible shapes accepted; anything else is REFUSED)."""
    if not MAPF.is_file():
        raise SystemExit('REFUSED: %s does not exist yet (CD writes it when the new runs are down)' % MAPF)
    d = json.loads(MAPF.read_text(encoding='utf-8'))
    cand = None
    if isinstance(d, dict):
        for k in ('runs', 'map', 'job_to_rid', 'jobs'):
            if isinstance(d.get(k), (dict, list)):
                cand = d[k]; break
        if cand is None and d and all(isinstance(k, str) and k.startswith('pl12_') for k in d):
            cand = d
    elif isinstance(d, list):
        cand = d
    m = {}
    if isinstance(cand, dict):
        for job, v in cand.items():
            m[job] = v if isinstance(v, str) else (v.get('rid') or v.get('run') or v.get('run_id') or v.get('folder'))
    elif isinstance(cand, list):
        for e in cand:
            job = e.get('job') or e.get('job_id'); rid = e.get('rid') or e.get('run') or e.get('run_id') or e.get('folder')
            m[job] = rid
    if not m or any(not isinstance(k, str) or not isinstance(v, str) for k, v in m.items()):
        raise SystemExit('REFUSED: cannot read %s as a job id -> run id map' % MAPF)
    return m


def rid_of(job):
    m = job_map()
    if job not in m:
        raise SystemExit('REFUSED: job %s not in %s' % (job, MAPF.name))
    return m[job]


def capture_dir(runs_root, job):
    rid = rid_of(job)
    rd = pathlib.Path(runs_root) / rid / rid
    caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
    assert len(caps) == 1, job
    return rd, caps[0]


def logs_ok(runs_root, job):
    m = job_map()
    return job in m and (pathlib.Path(runs_root) / m[job] / 'LOGS_OK').is_file()


def markers(out, runs_root=RUNS):
    out = pathlib.Path(out); m = job_map(); n = 0
    for job in l12_run_ids():
        src = pathlib.Path(runs_root) / m.get(job, '\0') / 'LOGS_OK'
        if job in m and src.is_file():
            (out / job).mkdir(parents=True, exist_ok=True)
            (out / job / 'LOGS_OK').write_bytes(src.read_bytes()); n += 1
    print('markers written: %d of 150 under %s' % (n, out))


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'markers':
        markers(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else RUNS)
    else:
        raise SystemExit(__doc__)
