"""v13 package B on the FRESH lead-braking runs: re-track with the tracker variants B3 (CV2), B4 (CA), B2 (AQ), B1_d090, B1_d098 and
rebuild the decision arrays (A10 section 5.7; B_FRESH_DEFINITIONS_v02.md section 2). New file, 20 Nov 2026 (Claude Opus 5.5).
The frozen v01 code and the library are not edited: this script imports b_retrack_v01 (tracker_record, save) and the library
(trk_tracker_v01.retrack_capture, trk_arrays_v01.overlay / extract) unchanged, so a fresh arrays file is made exactly as an old one.

Inputs (read-only): CD's extracted logs CD_capture\\runs\\<rid>\\<rid>\\capture\\<case>\\ (only once runs\\<rid>\\LOGS_OK exists);
P-bar_x = B_retrack\\out\\pbar\\PBAR_<x>_v01.json (of record, tuning runs). Run ids: CASES_C_v13.json lead-braking cases with
REPLACEMENTS_C_v13.json applied, as pc13_<case>_native, sorted ascending.
Output: B_retrack\\out\\retrack_fresh\\<x>\\<rid>_arrays.npz (keys of extract + the tracker record; meta JSON) and a log per call.
Lock gate: refuses unless revision_v13\\LOCK_A10_2.txt exists, except --test-old, which re-tracks OLD runs (default p1b_fit_finite_0012)
into out\\retrack_fresh_testold\\ and checks every array against the stored v01 file (B_retrack\\out\\retrack\\<x>\\<run>_arrays.npz).
Usage: python -I -B -X utf8 b_fresh_retrack_v02.py [--variants B3,B4,B2,B1_d090,B1_d098] [--workers 3] [--test-old [--runs a,b]]
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, pathlib, time, argparse, hashlib, traceback
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import b_retrack_v01 as R1                      # frozen v01: env.setup(), library imports, tracker_record, save
import numpy as np
T = R1.T; A = R1.A

HERE = pathlib.Path(__file__).resolve().parents[1]
WORK = HERE.parent
V13 = WORK.parent
LOCK2 = V13 / 'LOCK_A10_2.txt'
CD = WORK / 'CD_capture'
RUNS = CD / 'runs'
OUT = HERE / 'out' / 'retrack_fresh'
OUT_TEST = HERE / 'out' / 'retrack_fresh_testold'
VARIANTS = ['B3', 'B4', 'B2', 'B1_d090', 'B1_d098']


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def fresh_ids():
    cases = json.loads((CD / 'CASES_C_v13.json').read_text(encoding='utf-8'))['cases']
    rp = CD / 'REPLACEMENTS_C_v13.json'
    rep = json.loads(rp.read_text(encoding='utf-8'))['replacements'] if rp.is_file() else {}
    return sorted('pc13_%s_native' % rep.get(c['case'], c['case']) for c in cases if c['family'] == 'lead_braking')


def fresh_paths(rid):
    rd = RUNS / rid / rid
    caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
    if len(caps) != 1:
        raise RuntimeError('%s: %d capture folders' % (rid, len(caps)))
    return rd, caps[0]


def one(job):
    rid, variant, test = job
    outd = (OUT_TEST if test else OUT) / variant
    f = outd / ('%s_arrays.npz' % rid)
    if f.exists():
        return rid, variant, 'exists'
    t0 = time.time()
    try:
        if test:
            row = next(r for r in R1.index() if r['archive'] == rid)
            rd, cap = row['rd'], row['cap']
        else:
            if not (RUNS / rid / 'LOGS_OK').is_file():
                return rid, variant, 'waiting (no LOGS_OK)'
            rd, cap = fresh_paths(rid)
        PB = json.loads((R1.PBAR_DIR / ('PBAR_%s_v01.json' % variant)).read_text(encoding='utf-8'))['Pbar']
        ov, rec = T.retrack_capture(cap, variant)
        trk = R1.tracker_record(ov, rec)
        with A.overlay(cap, ov):
            meta, ax = A.extract(rd, cap, PB, lead=True, a4=True)
        meta.update(run=rid, set='fresh_c_lead' if not test else 'testold', variant=variant, pbar=PB, code='b_fresh_retrack_v02.py',
                    seconds=time.time() - t0)
        outd.mkdir(parents=True, exist_ok=True)
        R1.save(f, meta, dict(ax, **trk))
        return rid, variant, 'ok %.1fs' % (time.time() - t0)
    except Exception as e:
        outd.mkdir(parents=True, exist_ok=True)
        (outd / ('%s.err.json' % rid)).write_text(json.dumps(dict(error=repr(e)[:500], tb=traceback.format_exc()[-2500:])), encoding='utf-8')
        return rid, variant, 'ERROR %s' % repr(e)[:200]


def compare_old(rid, variant):
    a = np.load(OUT_TEST / variant / ('%s_arrays.npz' % rid), allow_pickle=False)
    b = np.load(HERE / 'out' / 'retrack' / variant / ('%s_arrays.npz' % rid), allow_pickle=False)
    keys = sorted(set(a.files) - {'meta'}); diff = []
    if set(a.files) != set(b.files):
        diff.append('key sets differ: %s' % sorted(set(a.files) ^ set(b.files)))
    for k in keys:
        if k in b.files and not (a[k].shape == b[k].shape and a[k].dtype == b[k].dtype
                                 and (np.array_equal(a[k], b[k], equal_nan=a[k].dtype.kind == 'f'))):
            diff.append(k)
    return dict(run=rid, variant=variant, keys=len(keys), identical=not diff, differing=diff)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--variants', default=','.join(VARIANTS)); ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--test-old', action='store_true'); ap.add_argument('--runs', default='p1b_fit_finite_0012')
    a = ap.parse_args()
    variants = a.variants.split(',')
    for v in variants:
        if v not in VARIANTS:
            raise SystemExit('REFUSED: variant %s is not re-tracked here (CV0 and B1 come from CD_capture\\arrays)' % v)
    if a.test_old:
        gate = 'TEST_OLD: old runs only; no fresh value'; rids = a.runs.split(',')
    else:
        if not LOCK2.is_file():
            raise SystemExit('REFUSED: LOCK_A10_2.txt does not exist; no fresh run is read before Lock 2 (A10 sections 4, 5.2)')
        gate = 'LOCK_A10_2 sha256 ' + sha(LOCK2); rids = fresh_ids()
        if len(rids) != 105:
            raise SystemExit('REFUSED: %d lead-braking run ids, expected 105' % len(rids))
    jobs = [(r, v, a.test_old) for r in rids for v in variants]     # run-major: a run's variants follow its LOGS_OK
    t0 = time.time(); log = []
    logf = (OUT_TEST if a.test_old else OUT) / ('retrack_%s.log' % time.strftime('%Y%m%dT%H%M%S'))
    logf.parent.mkdir(parents=True, exist_ok=True)
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(a.workers) as ex:
        for rid, v, res in ex.map(one, jobs):
            line = '[%6.0f s] %s %s %s' % (time.time() - t0, rid, v, res); print(line, flush=True); log.append(dict(run=rid, variant=v, res=res))
            with open(logf, 'a', encoding='utf-8') as fh:
                fh.write(line + '\n')
    doc = dict(code='b_fresh_retrack_v02.py', gate=gate, variants=variants, runs=len(rids), jobs=log, seconds=time.time() - t0,
               written=time.strftime('%Y-%m-%d %H:%M:%S'),
               counts={k: sum(1 for x in log if x['res'].startswith(k)) for k in ('ok', 'exists', 'waiting', 'ERROR')})
    if a.test_old:
        doc['identity_vs_v01'] = [compare_old(r, v) for r in rids for v in variants]
        doc['all_identical'] = all(x['identical'] for x in doc['identity_vs_v01'])
    p = (OUT_TEST if a.test_old else OUT) / ('RETRACK_%s_%s.json' % ('TESTOLD' if a.test_old else 'FRESH', time.strftime('%Y%m%dT%H%M%S')))
    p.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(json.dumps({k: doc[k] for k in ('counts', 'seconds') if k in doc}), 'all_identical', doc.get('all_identical'), flush=True)


if __name__ == '__main__':
    main()
