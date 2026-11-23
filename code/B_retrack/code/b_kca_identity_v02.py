r"""v13 sprint, step 2: identity test of the additive library module shared\trackers\trk_tracker_v02.py (kappa_ca; AMENDMENT_11 §6).
New file, 21 Nov 2026 (Claude Opus 5.5). With trk_tracker_v02 imported and kappa_ca ABSENT, the 20 lead-braking tuning runs are
re-tracked with B4 and B1 and their arrays rebuilt exactly as b_retrack_v01 (P-bar_x of record); every array must equal the stored v01
file B_retrack\out\retrack\<x>\<run>_arrays.npz bit for bit. Also kappa_ca = 1.0 on two runs (B4, B1): identical too (a factor 1.0 is
exact). Writes out\b3\KCA_IDENTITY_v02.json. Usage: python -I -B -X utf8 b_kca_identity_v02.py [--workers 2]
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import b_retrack_v01 as R1                      # frozen: env.setup, library imports, tracker_record
import trk_tracker_v02                           # noqa: F401  (the module under test)
import numpy as np
T = R1.T; A = R1.A
HERE = pathlib.Path(__file__).resolve().parents[1]
CONST = json.loads((pathlib.Path(r'ARS_TRIAL\revision_v13\work\shared\trackers') / 'trk_constants_v01.json').read_text(encoding='utf-8'))


def one(job):
    run, variant, kca = job
    row = next(r for r in R1.index() if r['archive'] == run)
    const = dict(CONST) if kca is None else dict(CONST, kappa_ca=kca)
    PB = json.loads((R1.PBAR_DIR / ('PBAR_%s_v01.json' % variant)).read_text(encoding='utf-8'))['Pbar']
    ov, rec = T.retrack_capture(row['cap'], variant, const=const)
    trk = R1.tracker_record(ov, rec)
    with A.overlay(row['cap'], ov):
        meta, ax = A.extract(row['rd'], row['cap'], PB, lead=True, a4=True)
    arrs = dict(ax, **trk)
    b = np.load(HERE / 'out' / 'retrack' / variant / ('%s_arrays.npz' % run), allow_pickle=False)
    keys = sorted(set(b.files) - {'meta'}); diff = []
    if set(arrs) != set(keys):
        diff.append('key sets differ: %s' % sorted(set(arrs) ^ set(keys)))
    for k in keys:
        a = np.asarray(arrs.get(k)); x = b[k]
        if k not in arrs or a.shape != x.shape or not np.array_equal(a, x, equal_nan=a.dtype.kind == 'f'):
            diff.append(k)
    return dict(run=run, variant=variant, kappa_ca=kca, keys=len(keys), identical=not diff, differing=diff[:10])


def main():
    workers = int(sys.argv[sys.argv.index('--workers') + 1]) if '--workers' in sys.argv else 2
    runs = sorted(r['archive'] for r in R1.index() if r['set'] == 'tune' and r['family'] == 'lead_braking')
    if len(runs) != 20:
        raise SystemExit('REFUSED: %d tuning runs' % len(runs))
    jobs = [(r, v, None) for r in runs for v in ('B4', 'B1')] + [(r, v, 1.0) for r in runs[:2] for v in ('B4', 'B1')]
    t0 = time.time(); res = []
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(workers) as ex:
        for r in ex.map(one, jobs):
            res.append(r); print(r['run'], r['variant'], r['kappa_ca'], 'identical' if r['identical'] else 'DIFF %s' % r['differing'], flush=True)
    doc = dict(code='b_kca_identity_v02.py', module='shared/trackers/trk_tracker_v02.py', jobs=len(res),
               identical=sum(r['identical'] for r in res), all_identical=all(r['identical'] for r in res), results=res,
               seconds=time.time() - t0, written=time.strftime('%Y-%m-%d %H:%M:%S'))
    (HERE / 'out' / 'b3' / 'KCA_IDENTITY_v02.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print('all_identical', doc['all_identical'], doc['identical'], 'of', doc['jobs'])


if __name__ == '__main__':
    main()
