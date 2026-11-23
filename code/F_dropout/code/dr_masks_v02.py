"""Revision v13, AMENDMENT_11 sec. 6c (DR, detection dropouts): the frame masks under the ONE mask law shared with E's closed loop
(A11 sec. 6c "One mask law", final). New file, 21 Nov 2026 (Claude Opus 5.5, session F); replaces dr_masks_v01.py (first wording:
run-id seeds, no gap row), which is kept unchanged for the record and is not used.
The law, independent of truth and of every outcome:
  rng = numpy.random.default_rng(int.from_bytes(hashlib.sha256(("A11/D/" + case_id).encode("utf-8")).digest()[:8], "big"))
  case_id: the PROTOCOL case id (fresh run pc13_<case>_native -> <case>, e.g. c1109_eval_0012; tuning and old runs: the run index's
  case_id column, e.g. c1109_tune_0000); never a run, job or archive name.
  Frames i = 0 .. n - 1 in logged order (rows of detections.jsonl). Frame 0 is never masked. From i = 1, at each frame not inside a
  window: u = rng.random(); if u < 0.10: L = rng.integers(1, 4) and frames i .. i + L - 1 are masked (cut at n - 1); the frame right
  after a window is never masked and draws nothing; draws resume at the frame after it (i += L + 1). Otherwise i += 1.
Usage: python -I dr_masks_v02.py write       (225 runs -> masks\\DR_MASKS_v02.json; refuses to overwrite)
       python -I dr_masks_v02.py check FILE  (regenerates every run's mask and compares)
       python -I dr_masks_v02.py e4 FILE     (compares with E's mask table, e.g. E_closedloop\\out\\E4_MASKS_v01.json)
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
OUTF = DR / 'masks' / 'DR_MASKS_v02.json'


def seed_of(case_id):
    return int.from_bytes(hashlib.sha256((PREFIX + case_id).encode('utf-8')).digest()[:8], 'big')


def mask(case_id, n):
    """Sorted list of masked frame indices of a run of protocol case `case_id` with n detector frames."""
    rng = np.random.default_rng(seed_of(case_id))
    out = []; i = 1
    while i < n:
        if rng.random() < P_START:
            L = int(rng.integers(1, L_MAX + 1))
            out.extend(range(i, min(i + L, n)))
            i += L + 1
        else:
            i += 1
    return out


def case_of_fresh(rid):
    assert rid.startswith('pc13_') and rid.endswith('_native'), rid
    return rid[len('pc13_'):-len('_native')]


def fresh_runs():
    """The 105 fresh lead-braking runs: run id -> (case id, capture folder)."""
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
        out[rid] = (case_of_fresh(rid), caps[0])
    return out


def index_runs(set_, family=None, n_expected=None):
    rows = [r for r in csv.DictReader(open(RUN_INDEX, encoding='utf-8'))
            if r['use'] == '1' and r['set'] == set_ and (family is None or r['family'] == family)]
    if n_expected is not None:
        assert len(rows) == n_expected, len(rows)
    return {r['archive']: (r['case_id'], pathlib.Path(r['cap'])) for r in sorted(rows, key=lambda r: r['archive'])}


def tuning_runs():
    """The 120 tuning runs of record: archive -> (case id, capture folder)."""
    return index_runs('tune', None, 120)


def n_frames(cap):
    with open(pathlib.Path(cap) / 'detections.jsonl', encoding='utf-8') as f:
        return sum(1 for line in f if line.strip())


def stretches(m):
    """Lengths of the maximal runs of consecutive masked frames."""
    out = []; prev = None
    for i in m:
        if prev is not None and i == prev + 1: out[-1] += 1
        else: out.append(1)
        prev = i
    return out


def write():
    if OUTF.exists():
        raise SystemExit('REFUSED: %s exists' % OUTF)
    doc = dict(rule='AMENDMENT_11 sec. 6c "One mask law" (gap row; protocol case id)', code='dr_masks_v02.py', prefix=PREFIX,
               p_start=P_START, L_values=[1, 2, 3], written=time.strftime('%Y-%m-%d %H:%M:%S'), fresh={}, tuning={})
    for key, runs in (('fresh', fresh_runs()), ('tuning', tuning_runs())):
        for rid, (case, cap) in runs.items():
            n = n_frames(cap)
            doc[key][rid] = dict(case_id=case, n=n, masked=mask(case, n))
    tot = {}
    for k in ('fresh', 'tuning'):
        st = [s for v in doc[k].values() for s in stretches(v['masked'])]
        tot[k] = dict(masked=sum(len(v['masked']) for v in doc[k].values()), frames=sum(v['n'] for v in doc[k].values()),
                      windows=len(st), max_stretch=max(st) if st else 0)
    doc['totals'] = tot
    OUTF.parent.mkdir(parents=True, exist_ok=True)
    OUTF.write_text(json.dumps(doc, indent=0), encoding='utf-8')
    print('wrote', OUTF, json.dumps(tot), hashlib.sha256(OUTF.read_bytes()).hexdigest())


def check(path):
    doc = json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
    bad = [rid for k in ('fresh', 'tuning') for rid, v in doc[k].items() if mask(v['case_id'], v['n']) != v['masked']]
    print('runs', sum(len(doc[k]) for k in ('fresh', 'tuning')), 'mismatches', len(bad), bad[:5])
    return not bad


def bits(case_id, n):
    m = set(mask(case_id, n))
    return ''.join('1' if i in m else '0' for i in range(n))


if __name__ == '__main__':
    if sys.argv[1] == 'write':
        write()
    elif sys.argv[1] == 'check':
        sys.exit(0 if check(sys.argv[2]) else 1)
    elif sys.argv[1] == 'bits':
        print(bits(sys.argv[2], int(sys.argv[3])))
