"""Revision v13, package C, A10 sec. 5.7 additions ("S57A"): per-run cut-in inputs that c_extract_v13.py does not produce. New file,
20 Nov 2026 (Claude Opus 5.5). Definitions: CD_capture\\CD_DEFINITIONS_S57A_v13.md sec. 2. Scope of 20 Nov 02:40 EST (coordinator):
the lead-braking extraction (delayed stop, realised deceleration) and the tuning-run TG moved to package B; the earlier version is kept as
analysis\\superseded_x_s57a_extract_v13_before_scope_change.txt.

Sets:
  c_cutin    (fresh, after both locks) per cut-in run: kc, rel, stratum, spread (event and track age as c_cutin_v13 / b9_cutin_v01, same
             expressions, copied below).  -> arrays/S57A/<rid>.npz
  test_cutin (old runs only) the same on the 20 cut-in tuning runs, into analysis/out/s57a_old/x/<run>.npz.
The fresh set refuses unless revision_v13/LOCK_A10_2.txt AND revision_v13/LOCK_A10_2c.txt exist (cd_common_v13.require_lock2c, the
two-stage Lock 2), and it opens no fresh array or log before that check. Nothing is overwritten: an existing output file is skipped.
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\x_s57a_extract_v13.py --set c_cutin|test_cutin [--workers 2] [--runs id1,...]
"""
import argparse, csv, json, math, os, pathlib, sys, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np                  # noqa: E402
import cd_common_v13 as CC          # noqa: E402

P = pathlib.Path(r'<library folder>')
STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
M4 = P / '09_redesign' / 'm4_perception_model'
OLDOUT = CC.OUT / 's57a_old'
DT = 0.05
LAT = 1.75            # Lock 2 cut-in threshold (B9: events in 20 of 20 tuning runs at 1.75 m)
CODE = 'x_s57a_extract_v13.py'
require_locks = CC.require_lock2c      # stage-2 gate: LOCK_A10_2.txt AND LOCK_A10_2c.txt (coordinator, 20 Nov)


# ------------------------------------------------------------------------------------------------ cut-in event (b9 / c_cutin, same lines)
def event_tick(T):
    ks = sorted(T); kc = None
    lat_e = np.array([-math.sin(T[k]['ego'][2]) * T[k]['ego'][0] + math.cos(T[k]['ego'][2]) * T[k]['ego'][1] for k in ks])
    lane = float(np.median(lat_e))
    for k in ks:
        tr = T[k]; tid = tr['target_id']
        ex, ey, yaw = tr['ego']
        if tid is None or tid not in tr['actors']: continue
        a = tr['actors'][tid]
        along = math.cos(yaw) * (a[0] - ex) + math.sin(yaw) * (a[1] - ey)
        across = -math.sin(yaw) * a[0] + math.cos(yaw) * a[1] - lane
        if along > 0 and abs(across) <= LAT:
            kc = k; break
    return kc, float(np.ptp(lat_e)) if lat_e.size else float('nan')


def event_info(TA, rd, cap, ks_ref):
    Lr = TA.load_capture(rd, cap); T = Lr['T']; book = Lr['book']
    kc, spread = event_tick(T)
    decs = list(TA.gc.decisions(cap)); ks = np.array([k for k, _ in decs])
    assert np.array_equal(ks, ks_ref)
    rel = (ks - kc) * DT if kc is not None else np.full(ks.size, np.nan)
    age = np.full(ks.size, np.nan)
    for di, (k, dec) in enumerate(decs):
        tr = T.get(k)
        m, prim, order = TA.gc.match_many(dec['actors'], dec['now'], tr)
        if prim is None: continue
        best = None
        for a, aid in zip(dec['actors'], m):
            if aid == prim:
                b = book.birth.get(int(a['track_id']))
                if b is None: continue
                ag = dec['now'] - book.det_time[b]
                best = ag if best is None else min(best, ag)
        if best is not None: age[di] = best
    stratum = np.full(ks.size, 'untracked', dtype='U9')
    stratum[np.isfinite(age) & (age < 1.)] = '<1s'; stratum[np.isfinite(age) & (age >= 1.) & (age < 4.)] = '1-4s'
    stratum[np.isfinite(age) & (age >= 4.)] = '>=4s'
    return kc, spread, rel, stratum


# ------------------------------------------------------------------------------------------------ run locations
def fresh_paths(rid):
    if not (CC.CD / 'runs' / rid / 'LOGS_OK').is_file():
        raise SystemExit('REFUSED: runs/%s/LOGS_OK missing (run c_extract_v13.py --logs-only first)' % rid)
    rd = CC.CD / 'runs' / rid / rid
    caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
    assert len(caps) == 1, rid
    return rd, caps[0]


def tune_rows(family):
    rows = [r for r in csv.DictReader(open(M4 / 'run_index_m4_v02.csv', encoding='utf-8'))
            if r['use'] == '1' and r['set'] == 'tune' and r['family'] == family]
    rows.sort(key=lambda r: r['archive']); assert len(rows) == 20
    return {r['archive']: (pathlib.Path(r['cap']).parents[3], pathlib.Path(r['cap'])) for r in rows}


# ------------------------------------------------------------------------------------------------ worker
def one(job):
    rid, rd, cap, k_ref, outf = job
    rd = pathlib.Path(rd); cap = pathlib.Path(cap); outf = pathlib.Path(outf)
    if outf.is_file():
        return rid, 'exists', 0.
    import trk_env_v01 as env; env.setup()
    import trk_arrays_v01 as TA
    t0 = time.time()
    contract = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))
    kc, spread, rel, stratum = event_info(TA, rd, cap, np.asarray(k_ref))
    meta = dict(run_id=rid, kind='cutin', family='cutin', case=contract['case']['id'], code=CODE, event=kc is not None,
                seconds=time.time() - t0)
    outf.parent.mkdir(parents=True, exist_ok=True)
    tmp = outf.with_name(outf.stem + '.partial.npz')
    np.savez_compressed(tmp, meta=json.dumps(meta, default=float), k=np.asarray(k_ref), kc=np.int64(-1 if kc is None else kc), rel=rel,
                        stratum=stratum, spread=np.float64(spread))
    os.replace(tmp, outf)
    return rid, 'ok', meta['seconds']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--set', required=True, choices=('c_cutin', 'test_cutin'))
    ap.add_argument('--workers', type=int, default=2); ap.add_argument('--runs', default='')
    a = ap.parse_args()
    if a.workers > 2: raise SystemExit('REFUSED: at most 2 workers on the shared laptop')
    gate = require_locks(a.set == 'test_cutin')
    jobs = []
    if a.set == 'c_cutin':
        for rid in CC.c_run_ids('cutin'):
            z = np.load(CC.ARR / 'CV0' / (rid + '.npz'), allow_pickle=False)
            assert json.loads(str(z['meta']))['family'] == 'cutin', rid
            rd, cap = fresh_paths(rid)
            jobs.append((rid, str(rd), str(cap), z['k'], str(CC.ARR / 'S57A' / (rid + '.npz'))))
    else:
        loc = tune_rows('cutin')
        sel = [x for x in a.runs.split(',') if x] or sorted(loc)
        for rid in sel:
            z = np.load(STORED / (rid + '.npz'), allow_pickle=False)
            jobs.append((rid, str(loc[rid][0]), str(loc[rid][1]), z['k'], str(OLDOUT / 'x' / (rid + '.npz'))))
    t0 = time.time(); log = []
    if a.workers <= 1:
        res = map(one, jobs)
    else:
        from concurrent.futures import ProcessPoolExecutor
        ex = ProcessPoolExecutor(a.workers); res = ex.map(one, jobs)
    for rid, st, sec in res:
        log.append(dict(run=rid, status=st, seconds=sec)); print('[%5.0f s] %s %s %.1f s' % (time.time() - t0, rid, st, sec), flush=True)
    CC.OUT.mkdir(exist_ok=True)
    (CC.OUT / f'S57A_EXTRACT_{a.set}_{time.strftime("%Y%m%dT%H%M%S")}.json').write_text(
        json.dumps(dict(gate=gate, set=a.set, workers=a.workers, runs=log, seconds=time.time() - t0), indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
