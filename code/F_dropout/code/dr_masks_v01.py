"""Revision v13, AMENDMENT_11 sec. 6c (DR, detection dropouts): the frame masks. New file, 21 Nov 2026 (Claude Opus 5.5, session F).
The rule (sec. 6c.4), independent of truth and of every outcome:
  rng = numpy.random.default_rng(int.from_bytes(hashlib.sha256(("A11/D/" + rid).encode("utf-8")).digest()[:8], "big"))
  frames i = 0 .. n - 1 in logged order (rows of detections.jsonl); frame 0 is never masked. For i = 1 .. n - 1, in order, at each frame
  not already inside a window: u = rng.random(); if u < 0.10: L = rng.integers(1, 4) and frames i .. i + L - 1 are masked (truncated
  at n - 1). Frames inside a window draw nothing.
rid: a fresh run's id (pc13_<case>_native); a tuning run's archive name of record.
Usage: python -I dr_masks_v01.py write      (all 225 runs -> masks\\DR_MASKS_v01.json; refuses to overwrite)
       python -I dr_masks_v01.py check FILE (regenerates every run's mask from the rule and compares)
"""
import csv, hashlib, json, pathlib, sys, time
import numpy as np

P_START = 0.10
L_MAX = 3
PREFIX = 'A11/D/'
HERE = pathlib.Path(__file__).resolve().parent
DR = HERE.parent
WORK = DR.parent
CD = WORK / 'CD_capture'
P = pathlib.Path(r'<library folder>')
RUN_INDEX = P / '09_redesign' / 'm4_perception_model' / 'run_index_m4_v02.csv'
OUTF = DR / 'masks' / 'DR_MASKS_v01.json'


def seed_of(rid):
    return int.from_bytes(hashlib.sha256((PREFIX + rid).encode('utf-8')).digest()[:8], 'big')


def mask(rid, n):
    """Sorted list of masked frame indices of a run with n detector frames."""
    rng = np.random.default_rng(seed_of(rid))
    out = []; i = 1
    while i < n:
        if rng.random() < P_START:
            L = int(rng.integers(1, L_MAX + 1))
            out.extend(range(i, min(i + L, n)))
            i += L
        else:
            i += 1
    return out


def fresh_runs():
    """The 105 fresh lead-braking runs (as b_fresh_retrack_v02.fresh_ids / cd_common_v13.c_run_ids): id -> capture folder."""
    cases = json.loads((CD / 'CASES_C_v13.json').read_text(encoding='utf-8'))['cases']
    rp = CD / 'REPLACEMENTS_C_v13.json'
    rep = json.loads(rp.read_text(encoding='utf-8'))['replacements'] if rp.is_file() else {}
    ids = sorted('pc13_%s_native' % rep.get(c['case'], c['case']) for c in cases if c['family'] == 'lead_braking')
    assert len(ids) == 105, len(ids)
    out = {}
    for rid in ids:
        rd = CD / 'runs' / rid / rid
        caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
        assert len(caps) == 1, rid
        out[rid] = caps[0]
    return out


def tuning_runs():
    """The 120 tuning runs of record (run_index_m4_v02.csv, use == 1, set == tune): archive -> capture folder."""
    rows = [r for r in csv.DictReader(open(RUN_INDEX, encoding='utf-8')) if r['use'] == '1' and r['set'] == 'tune']
    assert len(rows) == 120, len(rows)
    return {r['archive']: pathlib.Path(r['cap']) for r in sorted(rows, key=lambda r: r['archive'])}


def n_frames(cap):
    with open(pathlib.Path(cap) / 'detections.jsonl', encoding='utf-8') as f:
        return sum(1 for line in f if line.strip())


def write():
    if OUTF.exists():
        raise SystemExit('REFUSED: %s exists' % OUTF)
    doc = dict(rule='AMENDMENT_11 sec. 6c.4', code='dr_masks_v01.py', prefix=PREFIX, p_start=P_START, L_values=[1, 2, 3],
               written=time.strftime('%Y-%m-%d %H:%M:%S'), fresh={}, tuning={})
    for key, runs in (('fresh', fresh_runs()), ('tuning', tuning_runs())):
        for rid, cap in runs.items():
            n = n_frames(cap)
            m = mask(rid, n)
            doc[key][rid] = dict(n=n, masked=m)
    tot = {k: (sum(len(v['masked']) for v in doc[k].values()), sum(v['n'] for v in doc[k].values())) for k in ('fresh', 'tuning')}
    doc['totals'] = {k: dict(masked=a, frames=b) for k, (a, b) in tot.items()}
    OUTF.parent.mkdir(parents=True, exist_ok=True)
    OUTF.write_text(json.dumps(doc, indent=0), encoding='utf-8')
    print('wrote', OUTF, json.dumps(doc['totals']), hashlib.sha256(OUTF.read_bytes()).hexdigest())


def check(path):
    doc = json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
    bad = [rid for k in ('fresh', 'tuning') for rid, v in doc[k].items() if mask(rid, v['n']) != v['masked']]
    print('runs', sum(len(doc[k]) for k in ('fresh', 'tuning')), 'mismatches', len(bad), bad[:5])
    return not bad


if __name__ == '__main__':
    if sys.argv[1] == 'write':
        write()
    elif sys.argv[1] == 'check':
        sys.exit(0 if check(sys.argv[2]) else 1)
