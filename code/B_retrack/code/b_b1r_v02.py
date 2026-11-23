r"""v13 sprint, step 2: B1r = the IMM (B1, transition diagonal 0.95) with the re-tuned CA constants of out\b3\B1R_CONSTANTS_v02.json
(AMENDMENT_11_v13 §6). New file, 21 Nov 2026 (Claude Opus 5.5). Library: frozen trk_tracker_v01 plus the additive trk_tracker_v02
(kappa_ca); the frozen b_retrack_v01 functions (tracker_record, save, run index) are reused unchanged.
  pbar     the 120 tuning runs: re-track with B1r, then the P-bar rule of record (trk_arrays_v01.pbar_accumulate) -> per-run sums in
           out\retrack_b1r\pbar\<run>_pbar.npz (A10 §2.1: F0_x = x's own P-bar on the tuning runs).
  combine  out\pbar\PBAR_B1R_v02.json = sum / count per class (and the constants' SHA-256).
  fresh    the 105 fresh lead-braking runs (CASES_C_v13.json, ascending): re-track with B1r and extract with P-bar_B1r, exactly as
           b_fresh_retrack_v02.py -> out\retrack_fresh\B1R\<rid>_arrays.npz. REFUSES unless revision_v13\LOCK_A10_2.txt, LOCK_A10_2c.txt
           and LOCK_A11.txt exist (no fresh run before the A11 lock).
Workers: --workers N (default 1); with --adaptive a second worker is used only while the commit headroom (Win32 FreeVirtualMemory) is
>= 3.0 GB, and work pauses for the extra worker below 1.5 GB (coordinator rule, 21 Nov).
Usage: python -I -B -X utf8 b_b1r_v02.py pbar|combine|fresh [--workers 1]
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, pathlib, time, hashlib, traceback
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import b_retrack_v01 as R1                       # frozen: env.setup, library imports, tracker_record, save, run_list
import trk_tracker_v02                           # noqa: F401  (kappa_ca)
import numpy as np
T = R1.T; A = R1.A
HERE = pathlib.Path(__file__).resolve().parents[1]
WORK = HERE.parent; V13 = WORK.parent; CD = WORK / 'CD_capture'
CONSTF = HERE / 'out' / 'b3' / 'B1R_CONSTANTS_v02.json'
PBARF = HERE / 'out' / 'pbar' / 'PBAR_B1R_v02.json'
OUTP = HERE / 'out' / 'retrack_b1r' / 'pbar'
OUTF = HERE / 'out' / 'retrack_fresh' / 'B1R'
LOCKS = [V13 / 'LOCK_A10_2.txt', V13 / 'LOCK_A10_2c.txt', V13 / 'LOCK_A11.txt']


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def const():
    c = json.loads(CONSTF.read_text(encoding='utf-8'))
    return {k: v for k, v in c.items() if k != 'b1r'}


def fresh_ids():
    cases = json.loads((CD / 'CASES_C_v13.json').read_text(encoding='utf-8'))['cases']
    rep = json.loads((CD / 'REPLACEMENTS_C_v13.json').read_text(encoding='utf-8'))['replacements']
    return sorted('pc13_%s_native' % rep.get(c['case'], c['case']) for c in cases if c['family'] == 'lead_braking')


def job_pbar(row):
    f = OUTP / ('%s_pbar.npz' % row['archive'])
    if f.exists():
        return row['archive'], 'exists'
    t0 = time.time()
    try:
        ov, rec = T.retrack_capture(row['cap'], 'B1', const=const())
        trk = R1.tracker_record(ov, rec)
        with A.overlay(row['cap'], ov):
            acc, cnt = A.pbar_accumulate(row['cap'])
        R1.save(f, dict(run=row['archive'], set=row['set'], family=row['family'], variant='B1R', constants_sha256=sha(CONSTF)),
                dict(acc_vehicle=acc['vehicle'], acc_pedestrian=acc['pedestrian'], cnt_vehicle=cnt['vehicle'], cnt_pedestrian=cnt['pedestrian'], **trk))
        return row['archive'], 'ok %.0fs' % (time.time() - t0)
    except Exception as e:
        (OUTP / ('%s.err.json' % row['archive'])).write_text(json.dumps(dict(error=repr(e)[:500], tb=traceback.format_exc()[-2000:])), encoding='utf-8')
        return row['archive'], 'ERROR %s' % repr(e)[:200]


def job_fresh(rid):
    f = OUTF / ('%s_arrays.npz' % rid)
    if f.exists():
        return rid, 'exists'
    t0 = time.time()
    try:
        rd = CD / 'runs' / rid / rid
        cap = [p for p in (rd / 'capture').iterdir() if p.is_dir()][0]
        PB = json.loads(PBARF.read_text(encoding='utf-8'))['Pbar']
        ov, rec = T.retrack_capture(cap, 'B1', const=const())
        trk = R1.tracker_record(ov, rec)
        with A.overlay(cap, ov):
            meta, ax = A.extract(rd, cap, PB, lead=True, a4=True)
        meta.update(run=rid, set='fresh_c_lead', variant='B1R', pbar=PB, code='b_b1r_v02.py', constants_sha256=sha(CONSTF), seconds=time.time() - t0)
        R1.save(f, meta, dict(ax, **trk))
        return rid, 'ok %.0fs' % (time.time() - t0)
    except Exception as e:
        (OUTF / ('%s.err.json' % rid)).write_text(json.dumps(dict(error=repr(e)[:500], tb=traceback.format_exc()[-2000:])), encoding='utf-8')
        return rid, 'ERROR %s' % repr(e)[:200]


def headroom_gb():
    try:
        import subprocess
        r = subprocess.run(['powershell', '-NoProfile', '-Command', '(Get-CimInstance Win32_OperatingSystem).FreeVirtualMemory'],
                           capture_output=True, text=True, timeout=60)
        return float(r.stdout.strip()) / 1024 / 1024
    except Exception:
        return 0.


def run_jobs(fn, items, workers, log):
    from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
    pending = list(items); running = {}; t0 = time.time()
    with ProcessPoolExecutor(max(1, workers)) as ex:
        while pending or running:
            allow = 1 if workers <= 1 else (2 if headroom_gb() >= 3.0 else 1)
            while pending and len(running) < allow:
                it = pending.pop(0); running[ex.submit(fn, it)] = it
            done, _ = wait(list(running), timeout=60, return_when=FIRST_COMPLETED)
            for d in done:
                running.pop(d); name, res = d.result()
                line = '[%6.0f s] %s %s (allow %d)' % (time.time() - t0, name, res, allow); print(line, flush=True)
                with open(log, 'a', encoding='utf-8') as fh:
                    fh.write(line + '\n')


def main():
    mode = sys.argv[1]
    workers = int(sys.argv[sys.argv.index('--workers') + 1]) if '--workers' in sys.argv else 1
    if not CONSTF.exists():
        raise SystemExit('REFUSED: %s missing (tune first)' % CONSTF)
    if mode == 'pbar':
        OUTP.mkdir(parents=True, exist_ok=True)
        rows = R1.run_list('pbar')
        run_jobs(job_pbar, rows, workers, OUTP / ('pbar_%s.log' % time.strftime('%Y%m%dT%H%M%S')))
    elif mode == 'combine':
        acc = {c: np.zeros((4, 4)) for c in ('vehicle', 'pedestrian')}; cnt = {c: 0 for c in acc}; runs = []
        for r in R1.run_list('pbar'):
            z = np.load(OUTP / ('%s_pbar.npz' % r['archive']), allow_pickle=False)
            for c in acc:
                acc[c] += z['acc_' + c]; cnt[c] += int(z['cnt_' + c])
            runs.append(r['archive'])
        doc = dict(code='b_b1r_v02.py combine', variant='B1R', rule='ol_pbar_v01 on the re-tracked actors of the 120 tuning runs',
                   runs=len(runs), counts=cnt, Pbar={c: (acc[c] / max(cnt[c], 1)).tolist() for c in acc}, constants=str(CONSTF.relative_to(HERE)),
                   constants_sha256=sha(CONSTF), written=time.strftime('%Y-%m-%d %H:%M:%S'))
        PBARF.write_text(json.dumps(doc, indent=1), encoding='utf-8')
        print(json.dumps({k: doc[k] for k in ('runs', 'counts', 'constants_sha256')}))
    elif mode == 'fresh':
        miss = [str(p) for p in LOCKS if not p.is_file()]
        if miss:
            raise SystemExit('REFUSED: lock files missing: %s (no fresh run before the A11 lock)' % miss)
        if not PBARF.exists():
            raise SystemExit('REFUSED: %s missing' % PBARF)
        ids = fresh_ids()
        if len(ids) != 105:
            raise SystemExit('REFUSED: %d ids' % len(ids))
        OUTF.mkdir(parents=True, exist_ok=True)
        run_jobs(job_fresh, ids, workers, OUTF / ('fresh_%s.log' % time.strftime('%Y%m%dT%H%M%S')))
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
