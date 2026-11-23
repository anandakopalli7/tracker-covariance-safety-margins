"""Revision v13, packages C and D: decision arrays of the fresh runs (after Lock 2). New file, 19 Nov 2026 (Claude Opus 5.5).

Per run (C: 105 lead braking + 105 cut-in; D1: 105), from its verified archive archives/<rid>/claude_main_<rid>.tar.gz:
  1. logs: every member except the 20 Hz sweep files (raw/, clean/ .npy) is extracted to runs/<rid>/ (layout of the archive:
     runs/<rid>/<rid>/SUMMARY.json and runs/<rid>/<rid>/capture/<case>/...);
  2. CV0 (online tracker of record, logged files) with the P-bar of record (P\\09_redesign\\m2_decisions\\openloop\\pbar_tuning_v01.json):
     trk_arrays_v01.extract(run_dir, cap_dir, PB, lead=True, a4=True) (package B's frozen library; read-only);
     plus TG critical scales cTG1, cTG2, cTG4 (revision_v12 a9_7a_timegap_extract_v01 construction: s = (r0 + v_e)^2 with v_e the row's
     speed at the constraint's sample; gc.crit_rows), with the identity check that cF0 recomputed here equals extract's cF0;
     plus (set c_lead only) clearR075: per decision and row the true clearance under reaction-and-stop at tau = 0.75 s, 6 m/s^2 (trk_score_v01.
     delayed_stop_clearance with every tau_i = 0.75; equal to the cached stop of record within 5.7e-14, README sec. 4);
  3. B1 (the frozen IMM): trk_tracker_v01.retrack_capture(cap_dir, 'B1'), overlay, extract with P-bar_IMM
     (work\\B_retrack\\out\\pbar\\PBAR_B1_v01.json) -> arrays/B1/<rid>.npz (lead-braking C runs and cut-in C runs).
Writes arrays/<variant>/<rid>.npz (keys of extract, + cTG*, clearR075 for CV0; meta JSON with the case's lead_variant).
Refuses before Lock 2 (A10 sec. 5.2) unless --test-old (then it runs on old run p1b_fit_finite_0012 only, into arrays_testold/).
Usage: .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\c_extract_v13.py --set c_lead|c_cutin|d1 [--workers 4] [--variants CV0,B1]
"""
import argparse, json, os, pathlib, sys, tarfile, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cd_common_v13 as CC          # noqa: E402

PBAR_RECORD = pathlib.Path(r'<library folder>\pbar_tuning_v01.json')
PBAR_DIR = CC.WORK / 'B_retrack' / 'out' / 'pbar'
R0S = (1., 2., 4.)


def extract_logs(rid, dest_root):
    arch = CC.CD / 'archives' / rid / f'claude_main_{rid}.tar.gz'
    ok = json.loads((CC.CD / 'archives' / rid / 'DOWNLOAD_OK.json').read_text(encoding='utf-8'))
    assert ok['sha256'] == CC.sha(arch), rid
    dest = dest_root / rid
    if (dest / 'LOGS_OK').is_file(): return dest
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(arch, 'r:gz') as t:
        for m in t:
            parts = m.name.split('/')
            if m.isfile() and m.name.endswith('.npy') and len(parts) >= 2 and parts[-2] in ('raw', 'clean'): continue
            if '..' in parts or m.name.startswith('/'): raise RuntimeError('unsafe member ' + m.name)
            if m.isfile(): t.extract(m, dest, filter='data')
    (dest / 'LOGS_OK').write_text(ok['sha256'] + '\n')
    return dest


def run_paths(dest, rid):
    rd = dest / rid
    caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
    assert len(caps) == 1, rid
    return rd, caps[0]


def tg_arrays(A, cap, PB, cF0_ref):
    import numpy as np
    gc = A.gc; oc = A.oc; consumer = A.consumer; fp = A.finite_primitive
    JIDX = np.concatenate([np.arange(60), np.arange(1, 61)])
    decs = list(gc.decisions(cap)); nd = len(decs)
    out = {'cTG%d' % r0: np.full((nd, 17), np.nan) for r0 in R0S}; ndiff = 0
    for di, (k, dec) in enumerate(decs):
        ms = dec['model_state']; actors = dec['actors']; now = dec['now']
        rows = fp.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'], actors,
                                dec['ego_length'], dec['ego_width'], now, consumer.Diagnostics())
        n = len(rows); na = len(actors); M = 120 * na
        if na == 0:
            for r0 in R0S: out['cTG%d' % r0][di] = cF0_ref[di]
            continue
        D = np.stack([x['d'] for x in rows]).reshape(n, M)
        N, TE, MU = gc.geometry(rows, actors, now)
        Sbar = gc.s_P(N, TE, [np.array(PB[oc.cls_of(a['name'])], float) for a in actors])
        c = gc.crit_rows(D, Sbar); ndiff += int((~((c == cF0_ref[di]) | (np.isnan(c) & np.isnan(cF0_ref[di])))).sum())
        V = np.stack([np.asarray(x['v'], float) for x in rows]); VE = np.tile(V[:, JIDX], (1, na))
        for r0 in R0S: out['cTG%d' % r0][di] = gc.crit_rows(D, (r0 + VE) ** 2)
    return out, ndiff


def one(job):
    rid, variants, dest_root, outroot, setname = job
    import numpy as np
    import trk_env_v01 as env; env.setup()
    import trk_tracker_v01 as T, trk_arrays_v01 as A, trk_score_v01 as TS
    dest = extract_logs(rid, dest_root) if not rid.startswith('p1b_') else dest_root / rid
    rd, cap = run_paths(dest, rid)
    contract = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))
    res = {}
    for v in variants:
        outf = outroot / v / (rid + '.npz')
        if outf.is_file(): res[v] = 'exists'; continue
        t0 = time.time()
        if v == 'CV0':
            PB = json.loads(PBAR_RECORD.read_text(encoding='utf-8'))['Pbar']
            meta, arrs = A.extract(rd, cap, PB, lead=True, a4=True)
            tg, nd = tg_arrays(A, cap, PB, arrs['cF0'])
            arrs.update(tg); meta['tg_cF0_rows_differ'] = nd
            n = len(arrs['k'])
            if setname == 'c_lead':                                   # D2 (lead braking) only
                arrs['clearR075'] = TS.delayed_stop_clearance(rd, cap, {di: 0.75 for di in range(n)}, A=6.0)   # taus: {decision index: tau}
        else:
            PB = json.loads((PBAR_DIR / f'PBAR_{v}_v01.json').read_text(encoding='utf-8'))['Pbar']
            ov, rec = T.retrack_capture(cap, v)
            with A.overlay(cap, ov):
                meta, arrs = A.extract(rd, cap, PB, lead=True, a4=True)
        meta = dict(meta, run_id=rid, variant=v, case=contract['case']['id'], lead_variant=contract['case'].get('lead_variant'),
                    code='c_extract_v13.py', seconds=time.time() - t0)
        outf.parent.mkdir(parents=True, exist_ok=True)
        tmp = outf.with_suffix('.partial.npz')
        np.savez_compressed(tmp, meta=json.dumps(meta, default=float), **{k: np.asarray(x) for k, x in arrs.items()})
        os.replace(tmp, outf); res[v] = 'ok %.0f s' % (time.time() - t0)
    return rid, res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--set', required=True, choices=('c_lead', 'c_cutin', 'd1', 'test'))
    ap.add_argument('--workers', type=int, default=4); ap.add_argument('--variants', default='CV0,B1'); ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--logs-only', action='store_true', help='step 1 only: extract every run\'s logs (writes runs/<rid>/LOGS_OK), no arrays')
    a = ap.parse_args()
    gate = CC.require_lock2(a.test_old or a.set == 'test')
    variants = a.variants.split(',')
    if a.set == 'test':
        rids = ['p1b_fit_finite_0012']; dest_root = pathlib.Path(r'<library folder>\archives')
        outroot = CC.CD / 'arrays_testold'
        # old layout: archives/<rid>/SUMMARY.json and archives/<rid>/x/<rid>/capture/<case>
        import trk_env_v01 as env; env.setup()
        import numpy as np, trk_arrays_v01 as A, trk_score_v01 as TS
        rd = dest_root / rids[0]; cap = next(p for p in (rd / 'x' / rids[0] / 'capture').iterdir() if p.is_dir())
        PB = json.loads(PBAR_RECORD.read_text(encoding='utf-8'))['Pbar']
        meta, arrs = A.extract(rd, cap, PB, lead=True, a4=True)
        tg, nd = tg_arrays(A, cap, PB, arrs['cF0'])
        old = np.load(pathlib.Path(r'ARS_TRIAL\revision_v12\analysis\out\tg') / (rids[0] + '.npz'))
        same = all(np.array_equal(tg[k], old[k], equal_nan=True) for k in ('cTG1', 'cTG2', 'cTG4'))
        cR = TS.delayed_stop_clearance(rd, cap, {di: 0.75 for di in range(len(arrs['k']))}, A=6.0)
        pk = np.load(pathlib.Path(r'<library folder>\cache') / (rids[0] + '_pack.npz'))
        ref = pk[CC.L.vkey(0.75, 6.0)]; ev = arrs['evaluated'].astype(bool)
        dmax = float(np.nanmax(np.abs(np.where(np.isfinite(ref[ev]) & np.isfinite(cR[ev]), cR[ev] - ref[ev], 0.))))
        same_inf = bool(np.array_equal(np.isfinite(ref[ev]), np.isfinite(cR[ev])))
        print(json.dumps(dict(test='p1b_fit_finite_0012 (old run)', tg_identical_to_v12=same, tg_cF0_rows_differ=nd,
                              clearR075_vs_pack_of_record_max_abs_diff_evaluated=dmax, clearR075_same_finite_pattern=same_inf,
                              n_dec=len(arrs['k']))))
        return
    if a.set == 'c_lead': rids = CC.c_run_ids('lead_braking')
    elif a.set == 'c_cutin': rids = CC.c_run_ids('cutin')
    else: rids = [x for k in ('constant', 'mild_braking', 'stop_and_go') for x in CC.d1_run_ids(k)]
    dest_root = CC.CD / 'runs'; outroot = CC.ARR
    from concurrent.futures import ProcessPoolExecutor
    t0 = time.time(); log = []
    if a.logs_only:                                                   # logs first, so package B can read its runs (A10 sec. 10.1(b))
        # package B's five second-IMM runs (default_rng(20261917) over the sorted 105 lead-braking ids: positions 48, 54, 64, 75, 92)
        # go first, so B can start minutes after Lock 2
        B5 = [r for r in rids if r in ('pc13_c1109_eval_0288_native', 'pc13_c1109_eval_0324_native', 'pc13_c1109_eval_0384_native',
                                       'pc13_c1109_eval_0450_native', 'pc13_c1109_eval_0582_native')]
        rids = B5 + [r for r in rids if r not in B5]
        with ProcessPoolExecutor(a.workers) as ex:
            for rid, d in zip(rids, ex.map(extract_logs, rids, [dest_root] * len(rids))):
                log.append(dict(run=rid, logs_ok=(d / 'LOGS_OK').is_file())); print('[%5.0f s] %s logs' % (time.time() - t0, rid), flush=True)
        (CC.OUT).mkdir(exist_ok=True)
        (CC.OUT / f'EXTRACT_{a.set}_LOGS_{time.strftime("%Y%m%dT%H%M%S")}.json').write_text(
            json.dumps(dict(gate=gate, set=a.set, logs_only=True, runs=log, seconds=time.time() - t0), indent=1), encoding='utf-8')
        return
    with ProcessPoolExecutor(a.workers) as ex:
        for rid, res in ex.map(one, [(r, variants, dest_root, outroot, a.set) for r in rids]):
            log.append(dict(run=rid, res=res)); print('[%5.0f s] %s %s' % (time.time() - t0, rid, res), flush=True)
    (CC.OUT).mkdir(exist_ok=True)
    (CC.OUT / f'EXTRACT_{a.set}_{"_".join(variants)}_{time.strftime("%Y%m%dT%H%M%S")}.json').write_text(
        json.dumps(dict(gate=gate, set=a.set, variants=variants, runs=log, seconds=time.time() - t0), indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
