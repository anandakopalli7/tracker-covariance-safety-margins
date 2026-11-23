"""Revision v13, AMENDMENT_11 sec. 6c (DR, detection dropouts): re-track with frame masks and build the decision arrays. New file,
21 Nov 2026 (Claude Opus 5.5, session F); adapted from CD_capture\\analysis\\x_trk_extract_v13.py (the B7 extractor, accepted
bit-identical on Linux pods). The package-B library is imported read-only (work\\shared\\trackers); no library file is edited.

Per run: rows = the logged detector frames (detections.jsonl: k, time, model; logged order). A masked frame (masks\\DR_MASKS_v02.json,
dr_masks_v02.py: the one mask law, seeded by the protocol case id, with the gap row) keeps k and time; its model becomes [] (CANMOT: no_dets -> predict all, update none). Then
  ov, rec = trk_tracker_v01.retrack_capture(cap, 'CV0', base_cfg=CFG, det_rows=rows, dt=0.5, q_scale=True, latency=0.0)
  CFG = None (configuration of record) or the record with output.punish_num = PUNISH (DR_CONFIG_v01.json, sec. 6c.3)
  with trk_arrays_v01.overlay(cap, ov): extract(run_dir, cap, P-bar, lead=True, a4=True)
Per decision it also stores dr_frame (index of the detector frame the decision uses: the last row with k_row <= k, as the library's
det_rows path), dr_masked (that frame is masked), dr_age (consecutive masked frames up to and including it; 0 if not masked) and
dr_gap (the frame is the gap row right after a window).

Modes:
  id0    fresh runs, no mask, configuration of record, P-bar of record   -> out\\arrays\\ID0\\<rid>.npz   (identity check (i))
  id3    fresh runs, no mask, punish_num = PUNISH, P-bar of record       -> out\\arrays\\ID3\\<rid>.npz   (identity check (ii))
  pbar   tuning runs, masks, punish_num = PUNISH: pbar_accumulate        -> out\\pbar\\<archive>_pbar.npz   [LOCK_A11c]
  combine                                                                 -> out\\PBAR_DR_v01.json          [LOCK_A11c]
  dr     fresh runs, masks, punish_num = PUNISH, P-bar_DR (and the record) -> out\\arrays\\DR\\ and DRrec\\  [LOCK_A11c]
  --test-old: old run p1b_fit_finite_0037 (exploratory; CD's acceptance run) with its own mask, every mode's code path; writes
              out\\testold\\<mode>\\.
An existing output is never rewritten. Pods: --logs-root (fresh runs: <root>\\<rid>\\LOGS_OK, <root>\\<rid>\\<rid>\\...), V13_P_ROOT (P, for
the tuning runs, the run index and the P-bar of record), --out-root, --part i:n, --workers.
Usage: python -I -B -X utf8 dr_extract_v01.py MODE [--workers 2] [--part i:n] [--runs a,b] [--test-old] [--logs-root D] [--out-root D]
"""
import argparse, copy, csv, json, os, pathlib, sys, time, traceback
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('NUMBA_NUM_THREADS', '1')
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
DR = HERE.parent
WORK = DR.parent
V13 = WORK.parent
SHARED = WORK / 'shared' / 'trackers'
for _p in (str(HERE), str(SHARED)):
    if _p not in sys.path: sys.path.insert(0, _p)
import trk_env_v01 as env           # noqa: E402
env.setup()
import dr_masks_v02 as M            # noqa: E402  (the one mask law, A11 sec. 6c)

P_WIN = r'<library folder>'
P = pathlib.Path(os.environ.get('V13_P_ROOT', P_WIN))
PBAR_RECORD = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'pbar_tuning_v01.json'
RUN_INDEX = P / '09_redesign' / 'm4_perception_model' / 'run_index_m4_v02.csv'
OLD_ARCH = P / '07_fit_runs' / 'archives'
TEST_RUN = 'p1b_fit_finite_0037'
CD = WORK / 'CD_capture'
MASKS = DR / 'masks' / 'DR_MASKS_v02.json'
CONFIG = DR / 'code' / 'DR_CONFIG_v01.json'
OUT = DR / 'out'
LOCK = V13 / 'LOCK_A11c.txt'
LOCKED_MODES = ('pbar', 'combine', 'dr')


def punish():
    return int(json.loads(CONFIG.read_text(encoding='utf-8'))['punish_num'])


def cfg_dr():
    c = copy.deepcopy(env.tracker_config())
    c['output']['punish_num'] = punish()
    return c


def p_local(win_path):
    """A path string of P's run index (Windows, absolute) -> the path under P (V13_P_ROOT on a pod)."""
    s = str(win_path)
    if not s.startswith(P_WIN):
        raise RuntimeError('not under P: %s' % s)
    return P.joinpath(*[x for x in s[len(P_WIN):].split('\\') if x])


def fresh_ids():
    cases = json.loads((CD / 'CASES_C_v13.json').read_text(encoding='utf-8'))['cases']
    rp = CD / 'REPLACEMENTS_C_v13.json'
    rep = json.loads(rp.read_text(encoding='utf-8'))['replacements'] if rp.is_file() else {}
    ids = sorted('pc13_%s_native' % rep.get(c['case'], c['case']) for c in cases if c['family'] == 'lead_braking')
    if len(ids) != 105:
        raise SystemExit('REFUSED: %d lead-braking run ids, expected 105' % len(ids))
    return ids


def tuning_rows():
    rows = [r for r in csv.DictReader(open(RUN_INDEX, encoding='utf-8')) if r['use'] == '1' and r['set'] == 'tune']
    assert len(rows) == 120
    return {r['archive']: r for r in sorted(rows, key=lambda r: r['archive'])}


def old_fit_rows():
    """The 35 OLD lead-braking fit runs of record (exploratory; run_index_m4_v02.csv, use == 1, set == fit): the --test-old set."""
    rows = [r for r in csv.DictReader(open(RUN_INDEX, encoding='utf-8'))
            if r['use'] == '1' and r['set'] == 'fit' and r['family'] == 'lead_braking']
    assert len(rows) == 35
    return {r['archive']: r for r in sorted(rows, key=lambda r: r['archive'])}


def run_paths(rid, mode, test, logs_root):
    if test:
        cap = p_local(old_fit_rows()[rid]['cap'])
        return cap.parents[3], cap
    elif mode == 'pbar':
        cap = p_local(tuning_rows()[rid]['cap'])
        return cap.parents[3], cap
    else:
        if not (logs_root / rid / 'LOGS_OK').is_file():
            raise RuntimeError('%s: no LOGS_OK' % rid)
        rd = logs_root / rid / rid
        caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
    if len(caps) != 1:
        raise RuntimeError('%s: %d capture folders' % (rid, len(caps)))
    return rd, caps[0]


def masked_rows(cap, rid, masked):
    rows = list(env.jl(cap / 'detections.jsonl'))
    ks = [r['k'] for r in rows]
    if any(b <= a for a, b in zip(ks, ks[1:])):
        raise RuntimeError('%s: detector rows not in ascending k' % rid)
    ms = set(masked)
    if ms and max(ms) >= len(rows):
        raise RuntimeError('%s: mask index beyond the %d rows' % (rid, len(rows)))
    out = []
    for i, r in enumerate(rows):
        r2 = dict(k=r['k'], time=r['time'], model=([] if i in ms else r['model']))
        out.append(r2)
    return out


def frame_info(rows, ks_dec, masked):
    """Per decision tick k: the frame used (last row with k_row * 0.05 <= k * 0.05 + 1e-9, as trk_tracker_v01's det_rows path with
    latency 0), whether it is masked, and its age (consecutive masked frames up to and including it)."""
    import numpy as np
    kr = np.array([r['k'] for r in rows], dtype=np.int64)
    ms = np.zeros(len(rows), bool); ms[list(masked)] = True
    age = np.zeros(len(rows), np.int64)
    for i in range(len(rows)):
        age[i] = (age[i - 1] + 1 if i > 0 else 1) if ms[i] else 0
    gap = np.zeros(len(rows), bool)
    gap[1:] = ms[:-1] & ~ms[1:]
    fr = np.full(len(ks_dec), -1, np.int64)
    for j, k in enumerate(np.asarray(ks_dec, dtype=np.int64)):
        ok = np.flatnonzero(kr * 0.05 <= k * 0.05 + 1e-9)
        fr[j] = ok[-1] if ok.size else -1
    m = np.where(fr >= 0, ms[np.clip(fr, 0, None)], False)
    a = np.where(fr >= 0, age[np.clip(fr, 0, None)], 0)
    g = np.where(fr >= 0, gap[np.clip(fr, 0, None)], False)
    return fr, m, a, g


def one(job):
    rid, mode, test, logs_root, outroot, masked, case_id = job
    sub = {'id0': 'ID0', 'id3': 'ID3', 'pbar': 'pbar', 'dr': 'DR'}[mode]
    outf = outroot / sub / (rid + ('_pbar.npz' if mode == 'pbar' else '.npz'))
    if outf.is_file():
        return rid, mode, dict(status='exists')
    try:
        import numpy as np
        import trk_tracker_v01 as T, trk_arrays_v01 as A
        rd, cap = run_paths(rid, mode, test, logs_root)
        use_mask = mode in ('pbar', 'dr')
        rows = masked_rows(cap, rid, masked if use_mask else [])
        base_cfg = None if mode == 'id0' else cfg_dr()
        PBrec = json.loads(PBAR_RECORD.read_text(encoding='utf-8'))['Pbar']
        t0 = time.perf_counter()
        ov, rec = T.retrack_capture(cap, 'CV0', base_cfg=base_cfg, det_rows=rows, dt=0.5, q_scale=True, latency=0.0)
        t1 = time.perf_counter()
        meta0 = dict(run_id=rid, case_id=case_id, mode=mode, tracker='CV0', punish_num=(None if base_cfg is None else base_cfg['output']['punish_num']),
                     config=('of record' if base_cfg is None else 'record with output.punish_num = %d' % base_cfg['output']['punish_num']),
                     n_det_rows=len(rows), masked=(list(masked) if use_mask else []), masks_file=str(MASKS) if use_mask else None,
                     code='dr_extract_v01.py', test_old=bool(test), seconds_retrack=t1 - t0)
        if mode == 'pbar':
            with A.overlay(cap, ov):
                acc, cnt = A.pbar_accumulate(cap)
            arrs = dict(acc_vehicle=acc['vehicle'], acc_pedestrian=acc['pedestrian'], cnt_vehicle=np.int64(cnt['vehicle']),
                        cnt_pedestrian=np.int64(cnt['pedestrian']))
            meta = dict(meta0, seconds=time.perf_counter() - t0)
        else:
            PB = PBrec
            if mode == 'dr' and not test:
                PB = json.loads((OUT / 'PBAR_DR_v01.json').read_text(encoding='utf-8'))['Pbar']
            elif mode == 'dr' and test:
                PB = json.loads((outroot / 'PBAR_DR_v01.json').read_text(encoding='utf-8'))['Pbar']
            with A.overlay(cap, ov):
                meta, arrs = A.extract(rd, cap, PB, lead=True, a4=True)
            t2 = time.perf_counter()
            fr, m, a, g = frame_info(rows, arrs['k'], masked if use_mask else [])
            arrs = dict({k: np.asarray(x) for k, x in arrs.items()}, dr_frame=fr, dr_masked=m, dr_age=a, dr_gap=g)
            meta = dict(meta, **meta0, pbar=('P-bar_DR (PBAR_DR_v01.json)' if mode == 'dr' else 'P-bar of record'), seconds_extract=t2 - t1)
            if mode == 'dr':
                # the same tracker output with the P-bar of record: F0rec_DR (sec. 6c.5; descriptive only)
                with A.overlay(cap, ov):
                    meta_r, arrs_r = A.extract(rd, cap, PBrec, lead=True, a4=True)
                arrs_r = dict({k: np.asarray(x) for k, x in arrs_r.items()}, dr_frame=fr, dr_masked=m, dr_age=a, dr_gap=g)
                fr2 = outroot / 'DRrec' / (rid + '.npz'); fr2.parent.mkdir(parents=True, exist_ok=True)
                tmp2 = fr2.with_name(rid + '.partial.npz')
                np.savez_compressed(tmp2, meta=json.dumps(dict(meta_r, **meta0, pbar='P-bar of record'), default=float), **arrs_r)
                os.replace(tmp2, fr2)
            meta['seconds'] = time.perf_counter() - t0
        outf.parent.mkdir(parents=True, exist_ok=True)
        tmp = outf.with_name(outf.name[:-4] + '.partial.npz')
        np.savez_compressed(tmp, meta=json.dumps(meta, default=float), **arrs)
        os.replace(tmp, outf)
        return rid, mode, dict(status='ok', seconds=meta['seconds'], n_rows=len(rows), n_masked=len(meta0['masked']))
    except Exception as e:
        try:
            outf.parent.mkdir(parents=True, exist_ok=True)
            (outf.parent / (rid + '.err.json')).write_text(json.dumps(dict(error=repr(e)[:500], tb=traceback.format_exc()[-3000:])), encoding='utf-8')
        except Exception:
            pass
        return rid, mode, dict(status='ERROR %s' % repr(e)[:300])


def combine(outroot, test):
    import numpy as np
    names = sorted(p.name[:-len('_pbar.npz')] for p in (outroot / 'pbar').glob('*_pbar.npz')) if test else list(tuning_rows())
    acc = {c: np.zeros((4, 4)) for c in ('vehicle', 'pedestrian')}; cnt = {c: 0 for c in acc}
    for rid in names:
        z = np.load(outroot / 'pbar' / (rid + '_pbar.npz'), allow_pickle=False)
        for c in acc:
            acc[c] += z['acc_' + c]; cnt[c] += int(z['cnt_' + c])
    Pbar = {c: (acc[c] / max(cnt[c], 1)).tolist() for c in acc}
    doc = dict(code='dr_extract_v01.py combine', rule='ol_pbar_v01 (trk_arrays_v01.pbar_accumulate) on the DR tracker under the masks, '
               'the 120 tuning runs of record', punish_num=punish(), masks=str(MASKS), runs=len(names), counts=cnt, Pbar=Pbar,
               written=time.strftime('%Y-%m-%d %H:%M:%S'), test_old=bool(test))
    f = outroot / 'PBAR_DR_v01.json'
    if f.exists():
        raise SystemExit('REFUSED: %s exists' % f)
    f.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(json.dumps({k: doc[k] for k in doc if k != 'Pbar'}), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=('id0', 'id3', 'pbar', 'combine', 'dr'))
    ap.add_argument('--workers', type=int, default=2); ap.add_argument('--runs', default='')
    ap.add_argument('--test-old', action='store_true'); ap.add_argument('--part', default='')
    ap.add_argument('--logs-root', default=''); ap.add_argument('--out-root', default='')
    a = ap.parse_args()
    if a.mode in LOCKED_MODES and not a.test_old and not LOCK.is_file():
        raise SystemExit('REFUSED: %s needs LOCK_A11c.txt (AMENDMENT_11 sec. 6c.9); no DR value before the lock' % a.mode)
    # arrays: out\arrays\<ID0|ID3|DR|DRrec>; P-bar: out\pbar\ and out\PBAR_DR_v01.json; test: everything under out\testold
    outroot = pathlib.Path(a.out_root) if a.out_root else (
        OUT / 'testold' if a.test_old else (OUT if a.mode in ('pbar', 'combine') else OUT / 'arrays'))
    outroot.mkdir(parents=True, exist_ok=True)
    if a.mode == 'combine':
        combine(outroot, a.test_old); return
    mk = json.loads(MASKS.read_text(encoding='utf-8'))
    if a.test_old:
        allr = list(old_fit_rows())
        rids = [x for x in a.runs.split(',') if x] or [TEST_RUN]
        if rids == ['all']: rids = allr
        if any(x not in allr for x in rids): raise SystemExit('REFUSED: --test-old takes the 35 old lead-braking fit runs only')
        ofr = old_fit_rows()
        cases = {r: ofr[r]['case_id'] for r in rids}
        masks = {r: M.mask(cases[r], M.n_frames(run_paths(r, a.mode, True, None)[1])) for r in rids}
        a.runs = ''
    elif a.mode == 'pbar':
        rids = list(tuning_rows()); masks = {r: mk['tuning'][r]['masked'] for r in rids}
        cases = {r: mk['tuning'][r]['case_id'] for r in rids}
    else:
        rids = fresh_ids(); masks = {r: mk['fresh'][r]['masked'] for r in rids}
        cases = {r: mk['fresh'][r]['case_id'] for r in rids}
    if a.runs:
        sel = [x for x in a.runs.split(',') if x]
        if not all(x in rids for x in sel): raise SystemExit('REFUSED: run ids outside the set')
        rids = sel
    if a.part:
        i, n = (int(x) for x in a.part.split(':'))
        rids = [rids[j] for j in range(len(rids)) if j * n // len(rids) == i]
    logs_root = pathlib.Path(a.logs_root) if a.logs_root else CD / 'runs'
    jobs = [(rid, a.mode, a.test_old, logs_root, outroot, masks[rid], cases[rid]) for rid in rids]
    stamp = time.strftime('%Y%m%dT%H%M%S')
    logf = outroot / ('DR_EXTRACT_%s_%s.log' % (a.mode, stamp))
    t0 = time.time(); log = []
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(a.workers) as ex:
        for rid, mode, res in ex.map(one, jobs):
            line = '[%6.0f s] %s %s %s' % (time.time() - t0, rid, mode, json.dumps(res))
            print(line, flush=True); log.append(dict(run=rid, **res))
            with open(logf, 'a', encoding='utf-8') as fh:
                fh.write(line + '\n')
    nerr = sum(1 for x in log if x['status'].startswith('ERROR'))
    (outroot / ('DR_EXTRACT_%s_%s.json' % (a.mode, stamp))).write_text(json.dumps(dict(
        mode=a.mode, runs=len(rids), errors=nerr, seconds=time.time() - t0, punish_num=punish(), masks=str(MASKS), log=log,
        lock=str(LOCK) if LOCK.is_file() else None, written=time.strftime('%Y-%m-%d %H:%M:%S')), indent=0), encoding='utf-8')
    print('done', a.mode, len(rids), 'errors', nerr, '%.0f s' % (time.time() - t0))


if __name__ == '__main__':
    main()
