r"""Revision v13, AMENDMENT_12 sec. 3d: DR at 10 Hz on the NEW runs (second configuration). New file, 22 Nov 2026 (Claude Opus 5.5,
session F): a copy of dr_extract_v02.py (FREEZE_DR_A12) with only these changes:
  * rows: B7's 10 Hz detector rows (CD_capture\b7\<folder id>\b7_detections_v13.jsonl, rows whose rates_hz holds 10; ticks
    19, 21, ...); dt = 0.1, q_scale, latency 0.1 s (CD's chain B7_10_0.1); a decision at tick k uses the last row with
    k_row * 0.05 + 0.1 <= k * 0.05 (+1e-9);
  * masks: dr_masks_v04.mask(case_id, n_rows, p = 1 - 0.9 ** 0.2, Ls = (5, 10, 15), gap = 5);
  * output rule: output.punish_num = 15 (modes id3, dr); id0 keeps the configuration of record;
  * F0: P-bar_DR of A11 (F_dropout\out\PBAR_DR_v01.json, 2 Hz) for dr; the P-bar of record for id0 / id3 and for DRrec;
  * modes id0, id3, dr only (no P-bar pass at 10 Hz); folder F_dropout\out_a12\hz10\ (test: out_a12\testold_hz10\);
  * lock: revision_v13\LOCK_A12d.txt for dr.
  --test-old: old run p1b_fit_finite_0037 (the one old run with B7 rows; CD_capture\b7\p1b_fit_finite_0037\).
Usage: python -I -B -X utf8 dr_extract_v03.py MODE [--workers N] [--part i:n] [--runs a,b] [--test-old] [--logs-root D]
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
import dr_masks_v02 as M            # noqa: E402  (n_frames, tuning_runs)
import dr_masks_v03 as M3           # noqa: E402
import dr_masks_v04 as M4           # noqa: E402  (the one mask law by parameter)

P_WIN = r'<library folder>'
P = pathlib.Path(os.environ.get('V13_P_ROOT', P_WIN))
PBAR_RECORD = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'pbar_tuning_v01.json'
RUN_INDEX = P / '09_redesign' / 'm4_perception_model' / 'run_index_m4_v02.csv'
OLD_ARCH = P / '07_fit_runs' / 'archives'
TEST_RUN = 'p1b_fit_finite_0037'
CD = WORK / 'CD_capture'
MASKS = DR / 'masks' / 'DR_MASKS_v02.json'
CONFIG = DR / 'code' / 'DR_CONFIG_v01.json'
OUT_A12 = DR / 'out_a12'
LOCK = V13 / 'LOCK_A12d.txt'
B7 = CD / 'b7'
DT, LAT, PUNISH10 = 0.1, 0.1, 15
P10, LS10, GAP10 = 1 - 0.9 ** 0.2, (5, 10, 15), 5
L12 = CD / 'l12'
LOCKED_MODES = ('dr',)


def punish():
    return int(json.loads(CONFIG.read_text(encoding='utf-8'))['punish_num'])


def cfg_dr():
    c = copy.deepcopy(env.tracker_config())
    c['output']['punish_num'] = PUNISH10
    return c


def b7_rows(rid, test):
    """B7's 10 Hz rows of a run (k, time, model), file order, ticks checked (19, 21, ...)."""
    fid = rid if test else l12_map().get(rid, rid)
    rows = [x for x in env.jl(B7 / fid / 'b7_detections_v13.jsonl') if 10 in x['rates_hz']]
    ks = [x['k'] for x in rows]
    if any(b <= a for a, b in zip(ks, ks[1:])) or any(k < 19 or k % 2 == 0 for k in ks):
        raise RuntimeError('%s: 10 Hz rows at unexpected ticks' % rid)
    return [dict(k=x['k'], time=x['time'], model=x['model']) for x in rows]


def p_local(win_path):
    """A path string of P's run index (Windows, absolute) -> the path under P (V13_P_ROOT on a pod)."""
    s = str(win_path)
    if not s.startswith(P_WIN):
        raise RuntimeError('not under P: %s' % s)
    return P.joinpath(*[x for x in s[len(P_WIN):].split('\\') if x])


def l12_ids(logs_root):
    """The new runs (A12 sec. 2): study positions 0..149 of CASES_L12_v13.json, REPLACEMENTS_L12_v13.json applied (case -> case), as
    jobs pl12_<case>_native, ascending; only runs whose capture folder exists. Returns (ids, missing)."""
    cases = [c for c in json.loads((L12 / 'CASES_L12_v13.json').read_text(encoding='utf-8'))['cases'] if not c['reserve']]
    assert len(cases) == 150, len(cases)
    rp = L12 / 'REPLACEMENTS_L12_v13.json'
    rep = json.loads(rp.read_text(encoding='utf-8')).get('replacements', {}) if rp.is_file() else {}
    ids = sorted('pl12_%s_native' % rep.get(c['case'], c['case']) for c in cases)
    have = [r for r in ids if cap_of(logs_root, r) is not None]
    if len(have) < 128:
        raise SystemExit('REFUSED: %d of the 150 new runs have logs (fewer than 128: A12 sec. 2.4)' % len(have))
    return have, [r for r in ids if r not in have]


def l12_map():
    """CD's job id -> capture folder id map of the new runs (CD_capture/l12/out/L12_RUNS_v13.json; a run captured on an allowed retry
    has a suffixed folder id, e.g. __p1 / __r1). Values may be a string or a dict with 'rid' / 'run_id' / 'folder' / 'run'. Without the
    file, the folder id is the job id."""
    f = L12 / 'out' / 'L12_RUNS_v13.json'
    if not f.is_file():
        return {}
    d = json.loads(f.read_text(encoding='utf-8'))
    m = d.get('runs', d) if isinstance(d, dict) else {}
    out = {}
    for job, v in (m.items() if isinstance(m, dict) else []):
        if not str(job).startswith('pl12_'):
            continue
        out[str(job)] = v if isinstance(v, str) else (v.get('rid') or v.get('run_id') or v.get('folder') or v.get('run'))
    return out


def case_of(rid):
    assert rid.startswith('pl12_') and rid.endswith('_native'), rid
    return rid[len('pl12_'):-len('_native')]


def cap_of(logs_root, rid):
    fid = l12_map().get(rid, rid) if str(rid).startswith('pl12_') else rid       # job id -> CD's folder id (retry suffixes)
    for rd in (logs_root / fid / fid, logs_root / fid):
        if (rd / 'capture').is_dir():
            caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
            if len(caps) == 1:
                return rd, caps[0]
    return None


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
        rc = cap_of(logs_root, rid)
        if rc is None:
            raise RuntimeError('%s: no capture folder' % rid)
        return rc
    if len(caps) != 1:
        raise RuntimeError('%s: %d capture folders' % (rid, len(caps)))
    return rd, caps[0]


def masked_rows(cap, rid, masked, test=False):
    rows = b7_rows(rid, test)
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
        ok = np.flatnonzero(kr * 0.05 + LAT <= k * 0.05 + 1e-9)
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
        rows = masked_rows(cap, rid, masked if use_mask else [], test)
        base_cfg = None if mode == 'id0' else cfg_dr()
        PBrec = json.loads(PBAR_RECORD.read_text(encoding='utf-8'))['Pbar']
        t0 = time.perf_counter()
        ov, rec = T.retrack_capture(cap, 'CV0', base_cfg=base_cfg, det_rows=rows, dt=DT, q_scale=True, latency=LAT)
        t1 = time.perf_counter()
        meta0 = dict(run_id=rid, case_id=case_id, mode=mode, tracker='CV0', punish_num=(None if base_cfg is None else base_cfg['output']['punish_num']),
                     config=('of record' if base_cfg is None else 'record with output.punish_num = %d' % base_cfg['output']['punish_num']),
                     n_det_rows=len(rows), masked=(list(masked) if use_mask else []), masks_file=('DR_MASKS_<ptag>.json in the base folder' if use_mask else None),
                     code='dr_extract_v03.py', rate_hz=10, dt=DT, latency_s=LAT, test_old=bool(test), seconds_retrack=t1 - t0)
        if mode == 'pbar':
            with A.overlay(cap, ov):
                acc, cnt = A.pbar_accumulate(cap)
            arrs = dict(acc_vehicle=acc['vehicle'], acc_pedestrian=acc['pedestrian'], cnt_vehicle=np.int64(cnt['vehicle']),
                        cnt_pedestrian=np.int64(cnt['pedestrian']))
            meta = dict(meta0, seconds=time.perf_counter() - t0)
        else:
            PB = PBrec
            if mode == 'dr':                                     # A11's P-bar_DR (2 Hz), sec. 3d.4
                PB = json.loads((DR / 'out' / 'PBAR_DR_v01.json').read_text(encoding='utf-8'))['Pbar']
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
    doc = dict(code='dr_extract_v02.py combine', rule='ol_pbar_v01 (trk_arrays_v01.pbar_accumulate) on the DR tracker under the masks, '
               'the 120 tuning runs of record', punish_num=punish(), masks=[str(x) for x in sorted(outroot.glob('DR_MASKS_*.json'))], runs=len(names), counts=cnt, Pbar=Pbar,
               written=time.strftime('%Y-%m-%d %H:%M:%S'), test_old=bool(test))
    f = outroot / 'PBAR_DR_v01.json'
    if f.exists():
        raise SystemExit('REFUSED: %s exists' % f)
    f.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(json.dumps({k: doc[k] for k in doc if k != 'Pbar'}), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=('id0', 'id3', 'dr'))
    ap.add_argument('--workers', type=int, default=2); ap.add_argument('--runs', default='')
    ap.add_argument('--test-old', action='store_true'); ap.add_argument('--part', default='')
    ap.add_argument('--logs-root', default=''); ap.add_argument('--out-root', default='')
    a = ap.parse_args()
    if a.mode in LOCKED_MODES and not a.test_old and not LOCK.is_file():
        raise SystemExit('REFUSED: %s needs LOCK_A12d.txt (AMENDMENT_12 sec. 3d); no 10 Hz DR value before the lock' % a.mode)
    base = OUT_A12 / ('testold_hz10' if a.test_old else 'hz10')
    outroot = pathlib.Path(a.out_root) if a.out_root else (base if a.test_old else base / 'arrays')
    outroot.mkdir(parents=True, exist_ok=True)
    logs_root = pathlib.Path(a.logs_root) if a.logs_root else CD / 'runs'
    if a.test_old:
        rids = [TEST_RUN]; cases = {TEST_RUN: old_fit_rows()[TEST_RUN]['case_id']}; missing = []
    else:
        rids, missing = l12_ids(logs_root); cases = {r: case_of(r) for r in rids}
    masks = {}; rec = {}
    for r in rids:
        n = len(b7_rows(r, a.test_old)); masks[r] = M4.mask(cases[r], n, P10, LS10, GAP10); rec[r] = dict(case_id=cases[r], n=n, masked=masks[r])
    if not a.test_old:
        mf = base / 'DR_MASKS_hz10.json'
        doc = dict(law='AMENDMENT_12 sec. 3d.2 (A11 one mask law at 10 Hz: p_row = 1 - 0.9 ** 0.2, Ls = (5, 10, 15), gap 5)',
                   p_row=P10, Ls=list(LS10), gap=GAP10, code='dr_masks_v04.py', fresh=rec, missing_new_runs=missing)
        if mf.is_file() and json.loads(mf.read_text(encoding='utf-8'))['fresh'] != rec:
            raise SystemExit('REFUSED: %s exists with other masks' % mf)
        mf.write_text(json.dumps(doc, indent=0), encoding='utf-8')
    if a.runs:
        sel = [x for x in a.runs.split(',') if x]
        if not all(x in rids for x in sel): raise SystemExit('REFUSED: run ids outside the set')
        rids = sel
    if a.part:
        i, n = (int(x) for x in a.part.split(':'))
        rids = [rids[j] for j in range(len(rids)) if j * n // len(rids) == i]
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
        mode=a.mode, runs=len(rids), errors=nerr, seconds=time.time() - t0, punish_num=PUNISH10, log=log,
        lock=str(LOCK) if LOCK.is_file() else None, written=time.strftime('%Y-%m-%d %H:%M:%S')), indent=0), encoding='utf-8')
    print('done', a.mode, len(rids), 'errors', nerr, '%.0f s' % (time.time() - t0))


if __name__ == '__main__':
    main()
