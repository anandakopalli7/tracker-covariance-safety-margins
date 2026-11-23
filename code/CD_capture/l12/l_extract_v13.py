"""A12 sec. 2.3: decision arrays of the new lead-braking runs (online tracker of record, CV0). Copy of crossing/x_extract_v13.py (frozen
in FREEZE_CD_add3) with C's lead-braking call (lead=True, a4=True, as analysis/c_extract_v13.py), job ids pl12_, gate LOCK_A12a. Copied 22 Nov
2026 from the file written 21 Nov 2026 (Claude Opus 5.5, session CD). Runs on the laptop or on a capture pod (paths are arguments; no project path is needed on a pod except the
shared tracker library and the openloop modules of record, which trk_env_v01 locates).

Per run, from its verified archive <archive_root>/<rid>/claude_main_<rid>.tar.gz (keep_raw true since the A12 sec. 2.2 change of
22 Nov about 00:35 EST, the 10 Hz hedge: sweep frames inside, never extracted):
  1. logs: the archive must equal its receipt (claude_main_<rid>.tar.gz.receipt.json: sha256, bytes; status CAPTURED_AND_REVIEWED,
     keep_raw true); every member but the raw/clean sweep .npy is extracted to <runs_root>/<rid>/ (as c_extract_v13.extract_logs;
     unsafe members refused). FREEZE_CD_add8 changed only the keep_raw value required here (was false).
  2. CV0 with the P-bar of record (P\\09_redesign\\m2_decisions\\openloop\\pbar_tuning_v01.json): package B's frozen
     trk_arrays_v01.extract(run_dir, cap_dir, PB, lead=True, a4=True), C's lead-braking call (analysis/c_extract_v13.py, without the
     TG and clearR075 extras); it rebuilds, with the expressions of record, k, evaluated, v0, des, clear, vbar, idx55, cF0, cN, cE,
     the bookkeeping arrays, the A4 arrays (cNA, cQ, cA1, cCK3, phase, prebrake, lam_max) and the lead-state arrays.
Writes <out_root>/CV0/<rid>.npz (meta JSON: run, case, family and desired speed from the run's contract, code SHA-256).
Gate: refuses unless LOCK_A12a.txt exists in revision_v13 (or --lock PATH on a pod, whose SHA-256 must equal --lock-sha), except
--test-old, which runs on OLD lead-braking tuning runs only (P\\08_phase2\\archives_c1, already extracted) and compares the common keys
with the stored arrays of record; it never reads a new run.
Usage: python -I -B l_extract_v13.py --test-old [--runs p2_c1109_tune_0000_fixed_c1,...]
       python -I -B l_extract_v13.py --archive-root A --runs-root R --out-root O --ids FILE [--workers 2] [--lock PATH --lock-sha SHA]
"""
import argparse, hashlib, json, os, pathlib, sys, tarfile, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
V13 = HERE.parents[2] if HERE.parent.name == 'CD_capture' else None
SHARED = (HERE.parents[1] / 'shared' / 'trackers') if V13 else HERE / 'trackers'
if str(SHARED) not in sys.path: sys.path.insert(0, str(SHARED))
P = pathlib.Path(r'<library folder>')
PBAR_RECORD = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'pbar_tuning_v01.json'
STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
OLD_ARCH = P / '08_phase2' / 'archives_c1'
KEYS_CHECK = ('k', 'evaluated', 'v0', 'des', 'clear', 'vbar', 'idx55', 'cF0', 'cN', 'cE')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()


def below_normal():
    if os.name == 'nt':
        import ctypes
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)


def extract_logs(arch_dir, rid, runs_root):
    arch = arch_dir / rid / f'claude_main_{rid}.tar.gz'
    dest = runs_root / rid
    if (dest / 'LOGS_OK').is_file(): return dest
    rec = json.loads((arch_dir / rid / f'claude_main_{rid}.tar.gz.receipt.json').read_text(encoding='utf-8'))
    if rec.get('sha256') != sha(arch) or rec.get('bytes') != arch.stat().st_size:
        raise RuntimeError('archive differs from its receipt: ' + rid)
    if rec.get('status') != 'CAPTURED_AND_REVIEWED' or rec.get('keep_raw') is not True:
        raise RuntimeError('receipt status %s keep_raw %s: %s' % (rec.get('status'), rec.get('keep_raw'), rid))
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(arch, 'r:gz') as t:
        for m in t:
            parts = m.name.split('/')
            if '..' in parts or m.name.startswith('/'): raise RuntimeError('unsafe member ' + m.name)
            if m.isfile() and m.name.endswith('.npy') and len(parts) >= 2 and parts[-2] in ('raw', 'clean'): continue
            if m.isfile(): t.extract(m, dest, filter='data')
    (dest / 'LOGS_OK').write_text(sha(arch) + '\n')
    return dest


def run_paths(dest, rid):
    rd = dest / rid
    caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
    assert len(caps) == 1, rid
    return rd, caps[0]


def arrays(rd, cap, PB):
    import numpy as np
    import trk_env_v01 as env; env.setup()
    import trk_arrays_v01 as A
    meta, arrs = A.extract(rd, cap, PB, lead=True, a4=True)
    return meta, {k: np.asarray(x) for k, x in arrs.items()}


def one(job):
    rid, arch_dir, runs_root, out_root = job
    below_normal()
    import numpy as np
    outf = out_root / 'CV0' / (rid + '.npz')
    if outf.is_file(): return rid, 'exists'
    t0 = time.time()
    dest = extract_logs(arch_dir, rid, runs_root)
    rd, cap = run_paths(dest, rid)
    contract = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))
    PB = json.loads(PBAR_RECORD.read_text(encoding='utf-8'))['Pbar']
    meta, arrs = arrays(rd, cap, PB)
    case = contract['case']
    meta = dict(meta, run_id=rid, variant='CV0', case=case['id'], family=case['draw']['family'], desired=float(case['desired_mps']),
                code='l_extract_v13.py', code_sha256=sha(__file__), seconds=time.time() - t0)
    outf.parent.mkdir(parents=True, exist_ok=True)
    tmp = outf.with_suffix('.partial.npz')
    np.savez_compressed(tmp, meta=json.dumps(meta, default=float), **arrs)
    os.replace(tmp, outf)
    return rid, 'ok %.0f s' % (time.time() - t0)


def test_old(rids):
    import numpy as np
    below_normal()
    PB = json.loads(PBAR_RECORD.read_text(encoding='utf-8'))['Pbar']
    rows = []
    for rid in rids:
        t0 = time.time()
        rd = OLD_ARCH / rid / 'x' / rid
        cap = next(p for p in (rd / 'capture').iterdir() if p.is_dir())
        meta, arrs = arrays(rd, cap, PB)
        st = np.load(STORED / (rid + '.npz'), allow_pickle=False); sm = json.loads(str(st['meta']))
        cmp = {}
        for k in KEYS_CHECK:
            a, b = np.asarray(arrs[k], float), np.asarray(st[k], float)
            if a.shape != b.shape: cmp[k] = dict(shape=[list(a.shape), list(b.shape)]); continue
            fin = np.isfinite(a) & np.isfinite(b)
            cmp[k] = dict(same_nan=bool(np.array_equal(np.isnan(a), np.isnan(b))), n_diff=int((fin & (a != b)).sum()),
                          max_abs=float(np.max(np.abs(a[fin] - b[fin]))) if fin.any() else 0.0)
        rows.append(dict(run=rid, family=sm.get('family'), seconds=round(time.time() - t0, 1), compare=cmp))
        print(json.dumps(rows[-1]), flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true'); ap.add_argument('--runs', default='p2_c1109_tune_0000_fixed_c1,p2_c1109_tune_0006_fixed_c1')
    ap.add_argument('--archive-root'); ap.add_argument('--runs-root'); ap.add_argument('--out-root'); ap.add_argument('--ids')
    ap.add_argument('--workers', type=int, default=2); ap.add_argument('--lock'); ap.add_argument('--lock-sha')
    a = ap.parse_args()
    if a.test_old:
        rids = a.runs.split(',')
        assert all(r.startswith('p2_c1109_tune_') for r in rids), 'test mode reads old tuning runs only'
        rows = test_old(rids)
        out = HERE / 'out' / f'TESTOLD_L_EXTRACT_{time.strftime("%Y%m%dT%H%M%S")}.json'
        out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(dict(code_sha256=sha(__file__), runs=rows), indent=1), encoding='utf-8')
        print('written', out.name); return
    lock = pathlib.Path(a.lock) if a.lock else (V13 / 'LOCK_A12a.txt' if V13 else None)
    if lock is None or not lock.is_file(): raise SystemExit('REFUSED: LOCK_A12a.txt does not exist; no new lead-braking run may be read (A12 sec. 2.3)')
    if a.lock_sha and sha(lock) != a.lock_sha: raise SystemExit('REFUSED: the lock file differs from --lock-sha')
    ids = [x.strip() for x in pathlib.Path(a.ids).read_text(encoding='utf-8').split() if x.strip()]
    assert all(r.startswith('pl12_c1109_eval_') for r in ids)
    arch, runs_root, out_root = pathlib.Path(a.archive_root), pathlib.Path(a.runs_root), pathlib.Path(a.out_root)
    from concurrent.futures import ProcessPoolExecutor
    t0 = time.time(); log = []
    with ProcessPoolExecutor(a.workers) as ex:
        for rid, res in ex.map(one, [(r, arch, runs_root, out_root) for r in ids]):
            log.append(dict(run=rid, res=res)); print('[%5.0f s] %s %s' % (time.time() - t0, rid, res), flush=True)
    (out_root / f'L_EXTRACT_{time.strftime("%Y%m%dT%H%M%S")}.json').write_text(
        json.dumps(dict(lock_sha256=sha(lock), code_sha256=sha(__file__), runs=log, seconds=time.time() - t0), indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
