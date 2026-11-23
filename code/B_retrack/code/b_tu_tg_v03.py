"""v13 package B: TG's tuning-run arrays (A10 section 5.6: "TG's tuning-run arrays rebuilt by the A9-7 method with its identity check").
New file, 21 Nov 2026 (Claude Opus 5.5); coordinator request 21 Nov ~02:25 EST. Old (stored) data only; no lock gate applies.
For each of the 20 lead-braking tuning runs (P\\11_ojits\\A4\\dryrun\\extract\\*.npz, name order, as b_tu_v02.py): package CD's frozen
c_extract_v13.tg_arrays(A, cap, PB, cF0_ref) (FREEZE_CD; the A9-7 construction of revision_v12 a9_7a_timegap_extract_v01: for every
constraint of every rebuilt planner row, s = (r0 + v_e)^2 with v_e the row's speed at the constraint's sample; critical scale
gc.crit_rows(D, s); r0 = 1, 2, 4 m/s) with the P-bar of record. Identity (A9-7's own rule): the class-average critical scales recomputed
there from the same rows and geometry equal the stored cF0 of record (gateR_rt_v01) in every cell — tg_arrays returns the count of
differing cells, which must be 0 for every run, else the run is refused.
Writes out\\tu\\tg\\<run>.npz (k, cTG1, cTG2, cTG4) and out\\tu\\tg\\TU_TG_EXTRACT_v03.json.
--test-old: old evaluation run p1b_fit_finite_0012 only (out\\tu\\tg_testold\\): its cTG arrays must equal revision_v12 out\\tg exactly.
Run with package CD's frozen interpreter (importing c_extract_v13 loads cd_common_v13 / gl_fast_v13, which need numba):
  ..\\CD_capture\\.venv\\Scripts\\python.exe -I -B -X utf8 code\\b_tu_tg_v03.py [--test-old]
"""
import os, sys, json, pathlib, time, csv, hashlib
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
HERE = pathlib.Path(__file__).resolve().parents[1]
WORK = HERE.parent
sys.path.insert(0, str(WORK / 'shared' / 'trackers'))
sys.path.insert(0, str(WORK / 'CD_capture' / 'analysis'))
import trk_env_v01 as env
env.setup()
import numpy as np
import trk_arrays_v01 as A
import c_extract_v13 as CE                          # package CD's frozen file (tg_arrays), read-only

P = pathlib.Path(r'<library folder>')
TX = P / '11_ojits' / 'A4' / 'dryrun' / 'extract'
STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
INDEX = P / '09_redesign' / 'm4_perception_model' / 'run_index_m4_v02.csv'
PBAR_RECORD = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'pbar_tuning_v01.json'
V12TG = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis\out\tg')
ARCH = P / '07_fit_runs' / 'archives'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def caps():
    rows = {r['archive']: r for r in csv.DictReader(open(INDEX, encoding='utf-8')) if r['use'] == '1'}
    out = []
    for run in sorted(p.stem for p in TX.glob('*.npz')):
        cap = pathlib.Path(rows[run]['cap']); out.append((run, cap.parents[3], cap))
    return out


def one(run, rd, cap, PB, outd):
    t0 = time.time()
    z = np.load(STORED / (run + '.npz'), allow_pickle=False)
    nd = len(list(A.gc.decisions(cap)))
    if nd != len(z['k']):
        raise SystemExit('REFUSED: %s: %d logged decisions vs %d stored' % (run, nd, len(z['k'])))
    tg, ndiff = CE.tg_arrays(A, cap, PB, z['cF0'])
    np.savez_compressed(outd / (run + '.npz'), k=z['k'], **tg)
    return dict(run=run, n_dec=nd, cF0_cells_differ=int(ndiff), identity=bool(ndiff == 0), seconds=round(time.time() - t0, 1))


def main():
    test = '--test-old' in sys.argv
    PB = json.loads(PBAR_RECORD.read_text(encoding='utf-8'))['Pbar']
    t00 = time.time()
    if test:
        outd = HERE / 'out' / 'tu' / 'tg_testold'; outd.mkdir(parents=True, exist_ok=True)
        run = 'p1b_fit_finite_0012'; rd = ARCH / run; cap = next(p for p in (rd / 'x' / run / 'capture').iterdir() if p.is_dir())
        r = one(run, rd, cap, PB, outd)
        a = np.load(outd / (run + '.npz')); b = np.load(V12TG / (run + '.npz'))
        same = {k: bool(np.array_equal(a[k], b[k], equal_nan=True)) for k in ('cTG1', 'cTG2', 'cTG4')}
        doc = dict(code='b_tu_tg_v03.py --test-old', run=r, identical_to_v12_out_tg=same, k_equal=bool(np.array_equal(a['k'], b['k'])),
                   written=time.strftime('%Y-%m-%d %H:%M:%S'))
        (outd / 'TU_TG_TESTOLD_v03.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')
        print(json.dumps(doc)); return
    outd = HERE / 'out' / 'tu' / 'tg'; outd.mkdir(parents=True, exist_ok=True)
    res = []
    for run, rd, cap in caps():
        r = one(run, rd, cap, PB, outd); res.append(r); print(json.dumps(r), flush=True)
        if not r['identity']:
            raise SystemExit('REFUSED: identity failed for %s (%d cells)' % (run, r['cF0_cells_differ']))
    doc = dict(code='b_tu_tg_v03.py', status='old tuning runs (A10 section 5.6)', runs=res, n_runs=len(res),
               identity_all=all(r['identity'] for r in res), c_extract_v13_sha256=sha(WORK / 'CD_capture' / 'analysis' / 'c_extract_v13.py'),
               pbar_of_record_sha256=sha(PBAR_RECORD), seconds=time.time() - t00, written=time.strftime('%Y-%m-%d %H:%M:%S'))
    if len(res) != 20:
        raise SystemExit('REFUSED: %d tuning runs' % len(res))
    (outd / 'TU_TG_EXTRACT_v03.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('identity_all', doc['identity_all'], 'runs', len(res))


if __name__ == '__main__':
    main()
