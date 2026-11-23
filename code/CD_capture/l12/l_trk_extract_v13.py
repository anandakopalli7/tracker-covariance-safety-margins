"""L12 copy (A12 sec. 2.5, the 10 Hz option; coordinator 22 Nov 2026 about 00:55 EST) of analysis/x_trk_extract_v13.py (frozen in
FREEZE_CD_2), 22 Nov 2026 (Claude Opus 5.5, session CD). Changed: the run list (the 150 L12 capture run ids of l12/out/L12_RUNS_v13.json),
the gate (LOCK_A12a; the old-run test unchanged), the default output root (arrays_l12) and the log names. Nothing else.
Original text follows. Revision v13, package C: decision arrays of the B7 rate x latency chains on the fresh lead-braking and cut-in runs (AMENDMENT_10_v13
sec. 3 B7 "both families", sec. 5.7 "B7 at every rate x latency"). New file, 20 Nov 2026 (Claude Opus 5.5); B7 only since the
coordinator's scope change of 20 Nov 01:53 EST (Table III is package B's); cut-in family added 20 Nov 03:35 EST.
Definitions: CD_capture\\CD_DEFINITIONS_TRK_v13.md sec. 2 (lead braking) and sec. 8 (cut-in).

Per run (105 fresh runs of the family, cd_common_v13.c_run_ids(family); logs from c_extract_v13.py, runs\\<rid>\\LOGS_OK) and per
(r Hz, L s) in (2, 0), (2, 0.1), (5, 0), (5, 0.1), (5, 0.2), (10, 0), (10, 0.1), (10, 0.2):
  rows = the rows of b7\\<rid>\\b7_detections_v13.jsonl whose rates_hz holds r (file order; ticks checked);
  ov, rec = trk_tracker_v01.retrack_capture(cap, 'CV0', det_rows=rows, dt={2: 0.5, 5: 0.2, 10: 0.1}[r], q_scale=True, latency=L);
  with trk_arrays_v01.overlay(cap, ov): extract(run_dir, cap, P-bar of record, lead=True, a4=True)
  -> arrays\\B7_<r>_<L>\\<rid>.npz (lead braking) or arrays\\B7CI_<r>_<L>\\<rid>.npz (cut-in)
An existing output is never rewritten (the job is skipped). The package-B library is imported read-only (work\\shared\\trackers).
Each file holds extract's arrays and `meta` (JSON) with the timing of the re-tracking and of the extract.

Lock gate: cd_common_v13.require_lock2c (BOTH revision_v13\\LOCK_A10_2.txt and LOCK_A10_2c.txt; stage-2 code), except --test-old:
  lead braking: OLD run p1b_fit_finite_0037 only (the one old run with B7 detection rows) -> analysis\\out\\testold_b7_arrays\\;
  cut-in: the 20 OLD cut-in tuning runs (no sweeps were kept): rate 2 only, with the LOGGED detection rows (detections.jsonl: k, time,
          model) in place of the B7 file -> analysis\\out\\testold_b7ci_arrays\\B7CI_2_<L>\\.
  Per-job cost: analysis\\out\\TESTOLD_B7_v13[_ci]_extract_<stamp>.json.
Pods: --logs-root, --b7-root, --out-root, --runs and --part i:n make the same jobs runnable elsewhere (tools\\trk_pod_plan_v13.md); the
P-bar of record is found under V13_P_ROOT (default the laptop path of record).
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\x_trk_extract_v13.py [--family lead_braking|cutin] [--workers 2]
         [--combos 2_0,10_0.1,...] [--test-old] [--runs a,b] [--part i:n] [--logs-root DIR] [--b7-root DIR] [--out-root DIR]
"""
import argparse, csv, json, os, pathlib, sys, time, traceback
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('NUMBA_NUM_THREADS', '2')
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
SHARED = HERE.parents[1] / 'shared' / 'trackers'
for _p in (str(HERE.parent / 'analysis'), str(SHARED)):      # L12 copy: cd_common_v13 lives in analysis/ (was HERE)
    if _p not in sys.path: sys.path.insert(0, _p)
import trk_env_v01 as env           # noqa: E402  (first: environment of record, as package B's programs)
env.setup()
import cd_common_v13 as CC          # noqa: E402

P = pathlib.Path(os.environ.get('V13_P_ROOT', r'<library folder>'))
PBAR_RECORD = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'pbar_tuning_v01.json'
OLD_ARCH = P / '07_fit_runs' / 'archives'
RUN_INDEX = P / '09_redesign' / 'm4_perception_model' / 'run_index_m4_v02.csv'
FAM = {'lead_braking': dict(prefix='B7', test_out=CC.OUT / 'testold_b7_arrays', test_tag=''),
       'cutin': dict(prefix='B7CI', test_out=CC.OUT / 'testold_b7ci_arrays', test_tag='_ci')}
TEST_RUN = 'p1b_fit_finite_0037'
B7 = [(2, 0.0), (2, 0.1), (5, 0.0), (5, 0.1), (5, 0.2), (10, 0.0), (10, 0.1), (10, 0.2)]
DT = {2: 0.5, 5: 0.2, 10: 0.1}


def lstr(L):
    return '0' if L == 0 else ('%g' % L)


def b7name(r, L, prefix='B7'):
    return '%s_%d_%s' % (prefix, r, lstr(L))


def old_cutin_tuning():
    """The 20 cut-in tuning runs of record (as c_cutin_v13.py --test-old): run id -> (run_dir, cap), sorted by id."""
    rows = [r for r in csv.DictReader(open(RUN_INDEX, encoding='utf-8')) if r['use'] == '1' and r['set'] == 'tune' and r['family'] == 'cutin']
    rows.sort(key=lambda r: r['archive'])
    assert len(rows) == 20
    return {r['archive']: (pathlib.Path(r['cap']).parents[3], pathlib.Path(r['cap'])) for r in rows}


def run_paths(rid, test, logs_root, family):
    if test and family == 'cutin':
        return old_cutin_tuning()[rid]
    if test:
        rd = OLD_ARCH / rid
        caps = [p for p in (rd / 'x' / rid / 'capture').iterdir() if p.is_dir()]
    else:
        if not (logs_root / rid / 'LOGS_OK').is_file():
            return None, None
        rd = logs_root / rid / rid
        caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
    if len(caps) != 1:
        raise RuntimeError('%s: %d capture folders' % (rid, len(caps)))
    return rd, caps[0]


def b7_rows(b7_root, rid, r):
    if not (b7_root / rid / 'B7_MANIFEST_v13.json').is_file():
        raise RuntimeError('%s: no B7_MANIFEST_v13.json' % rid)
    rows = [x for x in env.jl(b7_root / rid / 'b7_detections_v13.jsonl') if r in x['rates_hz']]
    check_ticks(rows, rid, r)
    return rows


def check_ticks(rows, rid, r):
    ks = [x['k'] for x in rows]
    if any(b <= a for a, b in zip(ks, ks[1:])):
        raise RuntimeError('%s: B7 rows of %d Hz are not in ascending k' % (rid, r))
    bad = [k for k in ks if k < 19 or k % 2 == 0 or (r == 2 and k % 10 != 9) or (r == 5 and (k - 19) % 4 != 0)]
    if bad:
        raise RuntimeError('%s: %d Hz rows at unexpected ticks %s' % (rid, r, bad[:5]))


def logged_rows(cap, rid, r):
    """Test of the cut-in path on old runs (no sweeps kept): the logged online 2 Hz rows, as logged (the tracker reads k, time, model;
    the logged 'tracks' are replaced by the re-tracked ones), stand in for the B7 rows."""
    if r != 2:
        raise RuntimeError('%s: only 2 Hz exists in the logged detections' % rid)
    rows = list(env.jl(cap / 'detections.jsonl'))
    check_ticks(rows, rid, r)
    return rows


def one(job):
    rid, r, L, test, family, logs_root, b7_root, outroot = job
    name = b7name(r, L, FAM[family]['prefix'])
    outf = outroot / name / (rid + '.npz')
    if outf.is_file():
        return rid, name, dict(status='exists')
    try:
        import numpy as np
        import trk_tracker_v01 as T, trk_arrays_v01 as A
        rd, cap = run_paths(rid, test, logs_root, family)
        if rd is None:
            return rid, name, dict(status='waiting (no LOGS_OK)')
        contract = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))
        PB = json.loads(PBAR_RECORD.read_text(encoding='utf-8'))['Pbar']
        t0 = time.perf_counter()
        if test and family == 'cutin':
            rows = logged_rows(cap, rid, r); src = 'logged detections.jsonl rows: old-run test of the cut-in path'
        else:
            rows = b7_rows(b7_root, rid, r); src = 'b7_detections_v13.jsonl rows whose rates_hz holds %d' % r
        ov, rec = T.retrack_capture(cap, 'CV0', det_rows=rows, dt=DT[r], q_scale=True, latency=L)
        t1 = time.perf_counter()
        with A.overlay(cap, ov):
            meta, arrs = A.extract(rd, cap, PB, lead=True, a4=True)
        t2 = time.perf_counter()
        meta = dict(meta, run_id=rid, variant=name, family_set=family, case=contract['case']['id'], lead_variant=contract['case'].get('lead_variant'),
                    tracker='CV0', rate_hz=r, latency_s=L, dt=DT[r], q_scale=True, n_det_rows=len(rows), b7_ks=[rows[0]['k'], rows[-1]['k']] if rows else None,
                    det_rows=src, pbar_file=str(PBAR_RECORD), code='x_trk_extract_v13.py',
                    seconds_retrack=t1 - t0, seconds_extract=t2 - t1, seconds=t2 - t0, test_old=bool(test))
        outf.parent.mkdir(parents=True, exist_ok=True)
        tmp = outf.with_name(rid + '.partial.npz')
        np.savez_compressed(tmp, meta=json.dumps(meta, default=float), **{k: np.asarray(x) for k, x in arrs.items()})
        os.replace(tmp, outf)
        return rid, name, dict(status='ok', seconds_retrack=t1 - t0, seconds_extract=t2 - t1, n_dec=len(arrs['k']), n_det_rows=len(rows))
    except Exception as e:
        try:
            outf.parent.mkdir(parents=True, exist_ok=True)
            (outf.parent / (rid + '.err.json')).write_text(json.dumps(dict(error=repr(e)[:500], tb=traceback.format_exc()[-3000:])), encoding='utf-8')
        except Exception:
            pass
        return rid, name, dict(status='ERROR %s' % repr(e)[:300])


def l12_gate():
    """A12 sec. 2.3: no value of a new run before LOCK_A12a."""
    lk = CC.V13 / 'LOCK_A12a.txt'
    if not lk.is_file(): raise SystemExit('REFUSED: LOCK_A12a.txt does not exist; no new L12 run may be read (A12 sec. 2.3)')
    return 'LOCK_A12a sha256 %s' % CC.sha(lk)


def l12_rids():
    """The capture run ids (folders under runs/ and b7/) of the 150 analysed L12 jobs: l12/out/L12_RUNS_v13.json "runs" {job: rid}."""
    m = json.loads((CC.CD / 'l12' / 'out' / 'L12_RUNS_v13.json').read_text(encoding='utf-8'))
    if m.get('missing') or len(m['runs']) != 150: raise SystemExit('REFUSED: L12_RUNS_v13.json is not complete (%d runs)' % len(m['runs']))
    return sorted(m['runs'].values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--family', default='lead_braking', choices=('lead_braking', 'cutin'))
    ap.add_argument('--workers', type=int, default=2); ap.add_argument('--combos', default='')
    ap.add_argument('--test-old', action='store_true'); ap.add_argument('--runs', default='')
    ap.add_argument('--part', default='', help='i:n, the i-th of n contiguous slices of the run list (0-based)')
    ap.add_argument('--logs-root', default=''); ap.add_argument('--b7-root', default=''); ap.add_argument('--out-root', default='')
    a = ap.parse_args()
    gate = CC.require_lock2c(True) if a.test_old else l12_gate()   # L12: LOCK_A12a (A12 sec. 2.3); the old-run test is unchanged
    fam = FAM[a.family]
    combos = B7 if not a.combos else [c for c in B7 if '%d_%s' % (c[0], lstr(c[1])) in a.combos.split(',')]
    if a.combos and len(combos) != len(a.combos.split(',')):
        raise SystemExit('unknown combination in --combos (use r_L, e.g. 2_0,10_0.1)')
    if a.test_old:
        if a.family == 'lead_braking':
            rids = [x for x in a.runs.split(',') if x] or [TEST_RUN]
            if rids != [TEST_RUN]:
                raise SystemExit('REFUSED: --test-old (lead braking) runs on %s only (the one old run with B7 detection rows)' % TEST_RUN)
        else:
            allr = sorted(old_cutin_tuning())
            rids = [x for x in a.runs.split(',') if x] or allr
            if any(x not in allr for x in rids):
                raise SystemExit('REFUSED: --test-old (cut-in) takes the 20 old cut-in tuning runs only')
            if any(r != 2 for r, _ in combos):
                if a.combos: raise SystemExit('REFUSED: the cut-in old-run test has logged 2 Hz rows only')
                combos = [c for c in combos if c[0] == 2]
        outroot = pathlib.Path(a.out_root) if a.out_root else fam['test_out']
    else:
        if a.family != 'lead_braking': raise SystemExit('REFUSED: the L12 runs are lead braking')
        rids = l12_rids()
        if a.runs:
            sel = [x for x in a.runs.split(',') if x]
            if not all(x in rids for x in sel): raise SystemExit('REFUSED: run ids outside the L12 set')
            rids = sel
        outroot = pathlib.Path(a.out_root) if a.out_root else CC.CD / 'arrays_l12'
    if a.part:
        i, n = (int(x) for x in a.part.split(':'))
        rids = [rids[j] for j in range(len(rids)) if j * n // len(rids) == i]
    logs_root = pathlib.Path(a.logs_root) if a.logs_root else CC.CD / 'runs'
    b7_root = pathlib.Path(a.b7_root) if a.b7_root else CC.CD / 'b7'
    # run-major: all chains of a run, then the next run (each run's 10 Hz chains are the slow ones)
    jobs = [(rid, r, L, a.test_old, a.family, logs_root, b7_root, outroot) for rid in rids for r, L in combos]
    stamp = time.strftime('%Y%m%dT%H%M%S')
    logdir = CC.OUT if (a.test_old and not a.out_root) else outroot
    logdir.mkdir(parents=True, exist_ok=True)
    base = ('TESTOLD_LB7_v13%s_extract_%s' % (fam['test_tag'], stamp)) if a.test_old else ('LB7_EXTRACT_%s_%s' % (a.family, stamp))
    logf = logdir / (base + '.log')
    t0 = time.time(); log = []
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(a.workers) as ex:
        for rid, name, res in ex.map(one, jobs):
            line = '[%6.0f s] %s %s %s' % (time.time() - t0, rid, name, json.dumps(res))
            print(line, flush=True); log.append(dict(run=rid, name=name, **res))
            with open(logf, 'a', encoding='utf-8') as fh: fh.write(line + '\n')
    doc = dict(program='x_trk_extract_v13.py', gate=gate, family=a.family, test_old=a.test_old, combos=[b7name(r, L, fam['prefix']) for r, L in combos],
               runs=rids, out_root=str(outroot), workers=a.workers, jobs=log, seconds=time.time() - t0, written=time.strftime('%Y-%m-%d %H:%M:%S'),
               counts={k: sum(1 for x in log if x['status'].startswith(k)) for k in ('ok', 'exists', 'waiting', 'ERROR')})
    cost = {}
    for x in log:
        if x['status'] == 'ok':
            c = cost.setdefault(x['name'], dict(n=0, retrack=0., extract=0.))
            c['n'] += 1; c['retrack'] += x['seconds_retrack']; c['extract'] += x['seconds_extract']
    doc['cost_seconds_per_run'] = {k: dict(n=v['n'], retrack_mean=v['retrack'] / v['n'], extract_mean=v['extract'] / v['n'],
                                           total_mean=(v['retrack'] + v['extract']) / v['n']) for k, v in cost.items()}
    CC.write_once(logdir / (base + '.json'), doc)
    print(json.dumps(dict(counts=doc['counts'], seconds=doc['seconds'], cost=doc['cost_seconds_per_run']), default=float), flush=True)


if __name__ == '__main__':
    main()
