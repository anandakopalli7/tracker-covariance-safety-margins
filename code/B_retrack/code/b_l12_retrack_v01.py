r"""v13 round 2 (AMENDMENT_12 s3b, s3c): the new lead-braking runs of A12 s2.4. New file, 22 Nov 2026 (Claude Opus 5.5).
  retrack  re-track with a fixed-constant variant of the library (B2 for Y, A12 s3b; any of B3, B4, B2, B1_d090, B1_d098) and rebuild
           the decision arrays exactly as b_fresh_retrack_v02.one does for the C runs: trk_tracker_v01.retrack_capture(cap, variant)
           with the constants of record, b_retrack_v01.tracker_record, trk_arrays_v01.overlay + extract(rd, cap, P-bar_x of record,
           lead=True, a4=True), b_retrack_v01.save -> out\retrack_new\<x>\<rid>_arrays.npz. IMM2 is re-tracked by b_imm2_v01.py new.
  manifest write out\retrack_new\<X>_MANIFEST_v01.json: one list `arrays_<X>_l12` of {path, sha256, bytes} for every run id of A12 s2.4
           with LOGS_OK, in ascending order (the form CD's y_twin_l12_v13 / rc_y_twin_l12_v13 read); REFUSES if an arrays file is
           missing or an .err.json exists.
Run ids: b_l12_ids_v02.l12_run_ids (CD's rule), those whose run folder (job id -> run id map) has LOGS_OK. REFUSES unless revision_v13\LOCK_A12a.txt exists.
Workers: --workers N (default 2); the second worker only while the commit headroom is >= 3.0 GB (coordinator rule); BelowNormal.
Usage: python -I -B -X utf8 b_l12_retrack_v01.py retrack <runs root> --variant B2 [--workers 2]
       python -I -B -X utf8 b_l12_retrack_v01.py manifest <runs root> --variant B2|IMM2
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, pathlib, time, hashlib, traceback
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
if os.name == 'nt':
    import ctypes; ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
import b_l12_ids_v02 as L12          # 22 Nov 00:46: CD layout (job id -> run id map), b_l12_ids_v02

HERE = pathlib.Path(__file__).resolve().parents[1]
V13 = HERE.parents[1]
LOCK = V13 / 'LOCK_A12a.txt'
OUT = HERE / 'out' / 'retrack_new'
FIXED = ['B3', 'B4', 'B2', 'B1_d090', 'B1_d098']


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def one(job):
    rid, variant, root = job
    import b_retrack_v01 as R1                  # frozen v01 (env.setup, library); imported in the worker only
    T = R1.T; A = R1.A
    outd = OUT / variant
    f = outd / ('%s_arrays.npz' % rid)
    if f.exists():
        return rid, 'exists'
    t0 = time.time()
    try:
        rd, cap = L12.capture_dir(root, rid)
        PB = json.loads((R1.PBAR_DIR / ('PBAR_%s_v01.json' % variant)).read_text(encoding='utf-8'))['Pbar']
        ov, rec = T.retrack_capture(cap, variant)
        trk = R1.tracker_record(ov, rec)
        with A.overlay(cap, ov):
            meta, ax = A.extract(rd, cap, PB, lead=True, a4=True)
        meta.update(run=rid, set='new_a12', variant=variant, pbar=PB, code='b_l12_retrack_v01.py', seconds=time.time() - t0)
        outd.mkdir(parents=True, exist_ok=True)
        R1.save(f, meta, dict(ax, **trk))
        return rid, 'ok %.0fs' % (time.time() - t0)
    except Exception as e:
        outd.mkdir(parents=True, exist_ok=True)
        (outd / ('%s.err.json' % rid)).write_text(json.dumps(dict(error=repr(e)[:500], tb=traceback.format_exc()[-2500:])), encoding='utf-8')
        return rid, 'ERROR %s' % repr(e)[:200]


def headroom_gb():
    try:
        import subprocess
        r = subprocess.run(['powershell', '-NoProfile', '-Command', '(Get-CimInstance Win32_OperatingSystem).FreeVirtualMemory'],
                           capture_output=True, text=True, timeout=60)
        return float(r.stdout.strip()) / 1024 / 1024
    except Exception:
        return 0.


def main():
    mode, root = sys.argv[1], pathlib.Path(sys.argv[2]).resolve()
    variant = sys.argv[sys.argv.index('--variant') + 1]
    workers = int(sys.argv[sys.argv.index('--workers') + 1]) if '--workers' in sys.argv else 2
    if not LOCK.is_file():
        raise SystemExit('REFUSED: LOCK_A12a.txt does not exist (no new-run value before the A12a lock)')
    ids = [r for r in L12.l12_run_ids() if L12.logs_ok(root, r)]
    if mode == 'retrack':
        if variant not in FIXED:
            raise SystemExit('REFUSED: variant %s (IMM2 is re-tracked by b_imm2_v01.py new)' % variant)
        (OUT / variant).mkdir(parents=True, exist_ok=True)
        log = OUT / variant / ('new_%s.log' % time.strftime('%Y%m%dT%H%M%S'))
        from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
        pending = [(r, variant, root) for r in ids]; running = {}; t0 = time.time()
        print('runs with LOGS_OK: %d' % len(ids), flush=True)
        with ProcessPoolExecutor(max(1, workers)) as ex:
            while pending or running:
                allow = 1 if workers <= 1 else (2 if headroom_gb() >= 3.0 else 1)
                while pending and len(running) < allow:
                    it = pending.pop(0); running[ex.submit(one, it)] = it
                done, _ = wait(list(running), timeout=60, return_when=FIRST_COMPLETED)
                for d in done:
                    running.pop(d); name, res = d.result()
                    line = '[%6.0f s] %s %s (allow %d)' % (time.time() - t0, name, res, allow); print(line, flush=True)
                    with open(log, 'a', encoding='utf-8') as fh:
                        fh.write(line + '\n')
    elif mode == 'manifest':
        d = OUT / variant
        errs = sorted(p.name for p in d.glob('*.err.json'))
        miss = [r for r in ids if not (d / ('%s_arrays.npz' % r)).is_file()]
        if errs or miss:
            raise SystemExit('REFUSED: %d error files %s, %d arrays missing %s' % (len(errs), errs[:3], len(miss), miss[:3]))
        lst = [dict(path=str((d / ('%s_arrays.npz' % r)).relative_to(HERE.parent)), sha256=sha(d / ('%s_arrays.npz' % r)),
                    bytes=(d / ('%s_arrays.npz' % r)).stat().st_size) for r in ids]
        doc = {'code': 'b_l12_retrack_v01.py manifest', 'variant': variant, 'runs_root': str(root), 'n': len(lst),
               'lock_A12a_sha256': sha(LOCK), 'written': time.strftime('%Y-%m-%d %H:%M:%S'), 'arrays_%s_l12' % variant: lst}
        mf = OUT / ('%s_MANIFEST_v01.json' % variant)
        if mf.exists():
            raise SystemExit('REFUSED: %s exists' % mf)
        mf.write_text(json.dumps(doc, indent=1), encoding='utf-8')
        print('manifest %s: %d files, sha256 %s' % (mf.name, len(lst), sha(mf)), flush=True)
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
