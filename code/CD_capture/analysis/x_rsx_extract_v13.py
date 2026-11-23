"""Revision v13, packages C and D: the reaction-and-stop clearances "judged until the stop ends" (A10 sec. 1) of the fresh lead-braking
runs, a faithful port of revision_v11\\analysis\\rev_e1_extended_truth_extract_v01.py (RSX arrays, SHARED: c_s57b_v13.py, package B's
LB.RS075.rel / terciles / stop reliance, D2's reaction-and-stop column, the second programs). New file, 20 Nov 2026 (Claude Opus 5.5),
requested by the CD lead. Format: CD_capture\\CD_DEFINITIONS_S57B_v13.md sec. 7.

For every evaluated decision (from arrays\\CV0\\<rid>.npz) and planner row, and rev_e1's nine VARIANTS (tau 0.5, 0.75, 1.0, 1.25, 1.5,
1.8 s at 6 m/s^2; A = 4, 5, 7.6 m/s^2 at 0.75 s), with rev_e1's expressions:
  * the row until tau, then oxsb_replan_v03.replan_s(x, jr, A, 'r157') with brake_profile (optA_lib_v02's copy, same expressions:
    v0 = row v[jr], a0 = row a[jr - 1], jerk 12.65 m/s^3, position held after standstill), continued after frame 60 until the stop
    ends (J = max(60, ceil(t_stop / 0.05 - 1e-9)));
  * truth: true frames only (no extrapolation), up to frame min(max J, max(kmax - k, 60)); smallest rectangle distance to any true
    actor over frames 0..J (clearX) and over 0..60 (clear61 = the cached clearance of record); late = t_stop > 3 s; censored = late
    and the recording ends before J.
Loader: package B's trk_arrays_v01.load_capture(rd, cap) (rx.load_run's expressions with an explicit run folder; the --test-old run
checks that its truth T, kmax and decisions equal rev_e1's loader's, ol_gateR_rt_extract_v01.load_run('fit', run, YAW)).
Writes arrays\\RSX\\<rid>.npz (keys: meta, k, evaluated, and per vkey: clearX_, clear61_, tstop_, jend_, late_, cens_, jmin_).
Gate: stage 2 of the two-stage Lock 2, cd_common_v13.require_lock2c (both LOCK_A10_2.txt and LOCK_A10_2c.txt), unless --test-old,
which runs on OLD evaluation runs only (archives of record in P\\07_fit_runs), writes analysis\\out\\rsx_testold_arrays\\ and compares
with revision_v11\\analysis\\out\\ext (of record, all keys) and with the cache packs of record (clear61).
Usage (from CD_capture): .venv\\Scripts\\python.exe -I -B -X utf8 analysis\\x_rsx_extract_v13.py [--workers 2] [--test-old [--runs a,b]]
"""
import argparse, json, math, os, pathlib, sys, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
os.environ.setdefault('NUMBA_NUM_THREADS', '2')
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cd_common_v13 as CC          # noqa: E402
import numpy as np                  # noqa: E402

H = 0.05
VARIANTS = [(t, 6.0) for t in (0.5, 0.75, 1.0, 1.25, 1.5, 1.8)] + [(0.75, a) for a in (4.0, 5.0, 7.6)]
P = pathlib.Path(r'<library folder>')
OLD_ARCH = P / '07_fit_runs' / 'archives'
OLD_STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
V11_EXT = pathlib.Path(r'ARS_TRIAL\revision_v11\analysis\out\ext')
CACHE = P / '11_ojits' / 'review' / 'optionA_recount_v01' / 'cache'
OUT_TEST = CC.OUT / 'rsx_testold_arrays'
OUT_FRESH = CC.ARR / 'RSX'
FIELDS = ('clearX_', 'clear61_', 'tstop_', 'jend_', 'late_', 'cens_', 'jmin_')


def j_of(tau):
    j = int(round(tau / H))
    if abs(j * H - tau) > 1e-9 or j < 1:
        raise RuntimeError('tau %r is not a positive multiple of %g s' % (tau, H))
    return j


def replan_s(L, row, jr, A):
    """oxsb_replan_v03.replan_s(row, jr, A, 'r157') (same expressions; brake_profile = optA_lib_v02's copy of oxsb_replan_v03's)."""
    s = np.asarray(row['s'], float)
    out = s.copy()
    v0 = float(row['v'][jr]); a0 = float(row['a'][jr - 1])
    pos, t_stop, v_max = L.brake_profile(v0, a0, A, hold=False)
    for j in range(jr + 1, 61):
        out[j] = s[jr] + pos((j - jr) * H)
    return out, dict(v0=v0, a0=a0, t_stop=t_stop, v_max=v_max)


def window_truth_ext(np, T, k, kmax, nfr):
    """rev_e1.window_truth_ext: ol_extract_v01.window_truth with nfr frames and no extrapolation (true frames only)."""
    out = {}
    nreal = min(nfr - 1, kmax - k) + 1
    for aid in list(T[k]['actors']):
        c = np.full((nfr, 2), np.nan); hd = np.full(nfr, np.nan); hl = hw = None; last = None
        for j in range(nreal):
            a = T[k + j]['actors'].get(aid)
            if a is None:
                break
            c[j] = a[0], a[1]; hd[j] = a[2]; hl, hw = a[3], a[4]; last = j
        if last is None:
            continue
        out[aid] = (c, hd, hl, hw)
    return out


def dist_frames(np, oc, S, ego, Lg, Wd, wt):
    """rev_e1.dist_frames: (17, nfr) smallest rectangle distance to any true actor per frame (inf where none)."""
    nfr = S.shape[1]
    u = np.array([math.cos(ego[2]), math.sin(ego[2])])
    cx = ego[0] + S * u[0]; cy = ego[1] + S * u[1]
    E = oc.rect_corners(cx, cy, ego[2], Lg / 2, Wd / 2)
    Dall = np.full((17, nfr), np.inf)
    for aid, (c, hd, hl, hw) in wt.items():
        ok = np.isfinite(c[:, 0])
        if not ok.any():
            continue
        A = oc.rect_corners(c[:, 0][ok], c[:, 1][ok], hd[ok], hl, hw)
        D = oc.poly_dist(E[:, ok], A[None])
        Dall[:, ok] = np.minimum(Dall[:, ok], D)
    return Dall


def extract_run(rd, cap, k_ref, ev):
    """rev_e1.run_one on a run folder rd (SUMMARY.json) and capture folder cap; k_ref / ev: the decision ticks and evaluated flags of
    the run's CV0 arrays. Returns (checks, arrays)."""
    import numpy as np
    import trk_env_v01 as env; env.setup()
    import trk_arrays_v01 as TA
    L = CC.L
    Lr = TA.load_capture(rd, cap); T = Lr['T']; kmax = Lr['kmax']
    decs = list(TA.gc.decisions(Lr['cap']))
    ks = np.array([k for k, _ in decs], dtype=np.int64)
    if not (ks.shape == k_ref.shape and (ks == k_ref).all()):
        raise RuntimeError('decisions differ from the CV0 arrays\' k')
    nd = len(decs)
    arr = {}
    for (tau, A) in VARIANTS:
        kk = L.vkey(tau, A)
        arr['clearX_' + kk] = np.full((nd, 17), np.nan); arr['clear61_' + kk] = np.full((nd, 17), np.nan)
        arr['tstop_' + kk] = np.full((nd, 17), np.nan); arr['jend_' + kk] = np.full((nd, 17), -1, np.int64)
        arr['cens_' + kk] = np.zeros((nd, 17), bool); arr['late_' + kk] = np.zeros((nd, 17), bool)
        arr['jmin_' + kk] = np.full((nd, 17), -1, np.int64)
    for di, (k, dec) in enumerate(decs):
        if not ev[di]:
            continue
        ms = dec['model_state']; actors = dec['actors']; now = dec['now']
        Lg, Wd = dec['ego_length'], dec['ego_width']
        rows = TA.finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'], actors,
                                                 Lg, Wd, now, TA.consumer.Diagnostics())
        assert len(rows) == 17
        tr = T.get(k)
        left = int(kmax - k)
        for (tau, A) in VARIANTS:
            kk = L.vkey(tau, A); jr = j_of(tau)
            info = []; base = []
            for x in rows:
                sR, inf_ = replan_s(L, x, jr, A)
                pos, t_stop, _ = L.brake_profile(inf_['v0'], inf_['a0'], A)
                info.append((float(np.asarray(x['s'], float)[jr]), pos, jr * H + t_stop)); base.append(sR)
            tst = np.array([i[2] for i in info])
            jend = np.maximum(60, np.ceil(tst / H - 1e-9).astype(np.int64))
            late = tst > 3.0 + 1e-9
            nfr = int(min(jend.max(), max(left, 60))) + 1
            S = np.empty((17, nfr))
            for ri in range(17):
                S[ri, :61] = base[ri]
                s0, pos, _ = info[ri]
                for j in range(61, nfr):
                    S[ri, j] = s0 + pos((j - jr) * H)
            wt = window_truth_ext(np, T, k, kmax, nfr)
            Dall = dist_frames(np, TA.oc, S, tr['ego'], Lg, Wd, wt)
            arr['clear61_' + kk][di] = Dall[:, :61].min(axis=1)
            for ri in range(17):
                je = int(min(jend[ri], nfr - 1))
                seg = Dall[ri, :je + 1]
                arr['clearX_' + kk][di, ri] = seg.min(); arr['jmin_' + kk][di, ri] = int(seg.argmin())
            arr['tstop_' + kk][di] = tst; arr['jend_' + kk][di] = jend
            arr['late_' + kk][di] = late
            arr['cens_' + kk][di] = late & (jend > left)
    chk = {}
    for (tau, A) in VARIANTS:
        kk = L.vkey(tau, A)
        c61 = arr['clear61_' + kk][ev]; cx = arr['clearX_' + kk][ev]
        chk[kk] = dict(n_pairs=int(ev.sum()) * 17, n_late=int(arr['late_' + kk][ev].sum()),
                       n_late_safe61=int((arr['late_' + kk][ev] & (c61 > 0)).sum()),
                       n_cens_safe61=int((arr['cens_' + kk][ev] & (c61 > 0)).sum()),
                       n_flag_changed_by_extension=int(((c61 > 0) & ~(cx > 0)).sum()),
                       n_nonlate_changed=int((~arr['late_' + kk][ev] & (cx != c61)).sum()),
                       jend_max=int(arr['jend_' + kk][ev].max()) if ev.any() else -1)
    return dict(n_dec=nd, n_evaluated=int(ev.sum()), kmax=int(kmax), checks=chk), arr


def one(job):
    rid, rd, cap, kpath, outf, mode = job
    import numpy as np
    t0 = time.time()
    if outf.is_file():
        return rid, dict(status='exists')
    z = np.load(kpath, allow_pickle=False)
    k_ref = np.asarray(z['k'], np.int64); ev = z['evaluated'].astype(bool)
    meta, arr = extract_run(rd, cap, k_ref, ev)
    if mode == 'fresh' and 'clearR075' in z.files:          # identity with c_extract's 3 s-window clearance at 0.75 s, 6 m/s^2
        a = arr['clear61_t0p75_a6p0'][ev]; b = z['clearR075'][ev]
        both = np.isfinite(a) & np.isfinite(b)
        meta['identity_clear61_vs_CV0_clearR075'] = dict(
            max_abs=float(np.max(np.abs(a[both] - b[both]))) if both.any() else 0.,
            finite_pattern_equal=bool(np.array_equal(np.isfinite(a), np.isfinite(b))), flags_differ=int(((a > 0) != (b > 0)).sum()))
    contract = json.loads((pathlib.Path(cap) / 'contract.json').read_text(encoding='utf-8'))
    meta.update(run_id=rid, case=contract['case']['id'], code='x_rsx_extract_v13.py', variants=[[t, a] for t, a in VARIANTS],
                seconds=time.time() - t0, mode=mode)
    if mode == 'test_old':
        meta['loader_check'] = loader_check(rid, rd, cap)
        meta['cache_check'] = cache_check(rid, arr, ev)
    outf.parent.mkdir(parents=True, exist_ok=True)
    tmp = outf.with_name(outf.stem + '.partial.npz')
    np.savez_compressed(tmp, meta=json.dumps(meta, default=float), k=k_ref, evaluated=ev, **arr)
    os.replace(tmp, outf)
    return rid, dict(status='ok', seconds=meta['seconds'], n_evaluated=meta['n_evaluated'],
                     identity=meta.get('identity_clear61_vs_CV0_clearR075'), loader_check=meta.get('loader_check'),
                     cache_check=meta.get('cache_check'))


def deep_equal(a, b):
    """Exact structural equality (dict keys, sequence lengths, numbers bit for bit, NaN equal to NaN)."""
    if isinstance(a, dict):
        return isinstance(b, dict) and set(a) == set(b) and all(deep_equal(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)):
        return isinstance(b, (list, tuple)) and len(a) == len(b) and all(deep_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return np.array_equal(np.asarray(a), np.asarray(b), equal_nan=np.asarray(a).dtype.kind == 'f')
    if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b):
        return True
    return type(a) == type(b) and a == b


def loader_check(rid, rd, cap):
    """Old runs: trk_arrays_v01.load_capture(rd, cap) against rev_e1's loader, ol_gateR_rt_extract_v01.load_run('fit', run, YAW)
    (rev_e1: rx.load_run('fit', run, sb.YAW), rx and sb those of oxsb_core_v01)."""
    import trk_arrays_v01 as TA
    A = TA.load_capture(rd, cap); B = TA.sb.rx.load_run('fit', rid, TA.sb.YAW)
    return dict(T_equal=bool(deep_equal(A['T'], B['T'])), kmax_equal=bool(A['kmax'] == B['kmax']), n_frames=len(A['T']),
                cap_equal=bool(pathlib.Path(A['cap']).resolve() == pathlib.Path(B['cap']).resolve()),
                draw_equal=bool(deep_equal(A['draw'], B['draw'])), contact_k_equal=bool(A['contact_k'] == B['contact_k']),
                decisions_k_equal=bool([k for k, _ in TA.gc.decisions(A['cap'])] == [k for k, _ in TA.gc.decisions(B['cap'])]))


def cache_check(rid, arr, ev):
    """Old runs: clear61 against the cache pack of record (11_ojits\\review\\optionA_recount_v01\\cache), evaluated decisions."""
    pk = np.load(CACHE / (rid + '_pack.npz'), allow_pickle=False)
    out = {}
    for (tau, A) in VARIANTS:
        kk = CC.L.vkey(tau, A)
        c61 = arr['clear61_' + kk][ev]; cc = pk[kk][ev]
        both = np.isfinite(c61) & np.isfinite(cc)
        out[kk] = dict(max_abs=float(np.max(np.abs(c61[both] - cc[both]))) if both.any() else 0.,
                       inf_pattern_equal=bool(np.array_equal(np.isfinite(c61), np.isfinite(cc))),
                       flags_differ=int(((c61 > 0) != (cc > 0)).sum()), flags2_differ=int(((c61 > 2) != (cc > 2)).sum()))
    return out


def compare_with_record(rid, outf):
    """Old runs: this extraction against revision_v11\\analysis\\out\\ext\\<run>.npz (rev_e1, of record)."""
    import numpy as np
    a = np.load(outf, allow_pickle=False); b = np.load(V11_EXT / (rid + '.npz'), allow_pickle=False)
    res = dict(k_equal=bool(np.array_equal(a['k'], b['k'])))
    for (tau, A) in VARIANTS:
        kk = CC.L.vkey(tau, A); r = {}
        for f in FIELDS:
            x = a[f + kk]; y = b[f + kk]
            if x.dtype.kind == 'f':
                both = np.isfinite(x) & np.isfinite(y)
                r[f + 'max_abs'] = float(np.max(np.abs(x[both] - y[both]))) if both.any() else 0.
                r[f + 'pattern_equal'] = bool(np.array_equal(np.isfinite(x), np.isfinite(y)) and np.array_equal(np.isinf(x), np.isinf(y)))
                if f in ('clearX_', 'clear61_'):
                    r[f + 'flags_differ'] = int(((x > 0) != (y > 0)).sum()); r[f + 'flags2_differ'] = int(((x > 2) != (y > 2)).sum())
            else:
                r[f + 'equal'] = bool(np.array_equal(x, y))
        res[kk] = r
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=2); ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--runs', default='', help='--test-old only: comma-separated old run ids (default: all 35)')
    ap.add_argument('--not-laptop', action='store_true', help='allow more than 2 workers (only on a machine that is not the shared laptop)')
    a = ap.parse_args()
    gate = CC.require_lock2c(a.test_old)       # stage 2 of the two-stage Lock 2 (coordinator, 20 Nov)
    if a.workers > 2 and not a.not_laptop:
        raise SystemExit('REFUSED: at most 2 worker processes on the shared laptop (--not-laptop elsewhere)')
    jobs = []
    if a.test_old:
        rids = [r for r in a.runs.split(',') if r] or ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
        for rid in rids:
            assert rid.startswith('p1b_fit_finite_'), 'test mode reads old runs only'
            rd = OLD_ARCH / rid; cap = next(p for p in (rd / 'x' / rid / 'capture').iterdir() if p.is_dir())
            jobs.append((rid, rd, cap, OLD_STORED / (rid + '.npz'), OUT_TEST / (rid + '.npz'), 'test_old'))
    else:
        import c_extract_v13 as CX
        rids = CC.c_run_ids('lead_braking')
        missing = [r for r in rids if not (CC.ARR / 'CV0' / (r + '.npz')).is_file()]
        if missing:
            raise SystemExit('REFUSED: CV0 arrays missing for %d runs (run c_extract_v13.py --set c_lead first): %s' % (len(missing), missing[:5]))
        for rid in rids:
            dest = CC.CD / 'runs' / rid
            if not (dest / 'LOGS_OK').is_file():
                CX.extract_logs(rid, CC.CD / 'runs')                       # verified archive -> logs (c_extract_v13, unchanged)
            rd, cap = CX.run_paths(dest, rid)
            jobs.append((rid, rd, cap, CC.ARR / 'CV0' / (rid + '.npz'), OUT_FRESH / (rid + '.npz'), 'fresh'))
    t0 = time.time(); log = []
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(a.workers) as ex:
        for rid, res in ex.map(one, jobs):
            log.append(dict(run=rid, **res)); print('[%6.0f s] %s %s' % (time.time() - t0, rid, res), flush=True)
    doc = dict(code='x_rsx_extract_v13.py', gate=gate, mode='test_old' if a.test_old else 'fresh', workers=a.workers, runs=log,
               seconds=time.time() - t0, written=time.strftime('%Y-%m-%d %H:%M:%S'))
    secs = [x['seconds'] for x in log if x.get('status') == 'ok']
    if secs:
        doc['cost'] = dict(n_runs=len(secs), seconds_per_run_mean=float(sum(secs) / len(secs)), seconds_per_run_max=float(max(secs)),
                           wall_seconds=doc['seconds'], estimate_105_runs_wall_h=float(105 * sum(secs) / len(secs) / a.workers / 3600.))
    if a.test_old:
        cmp_ = {rid: compare_with_record(rid, OUT_TEST / (rid + '.npz')) for rid, *_ in jobs}
        worst = {}
        for rid, r in cmp_.items():
            for kk, v in r.items():
                if not isinstance(v, dict):
                    continue
                for f, x in v.items():
                    if isinstance(x, bool):
                        worst[f] = worst.get(f, True) and x
                    else:
                        worst[f] = max(worst.get(f, 0), x)
        doc['comparison_with_v11_ext'] = dict(per_run=cmp_, worst=worst)
        lc = [x['loader_check'] for x in log if x.get('loader_check')]
        doc['loader_check_all'] = {f: all(c[f] for c in lc) for f in ('T_equal', 'kmax_equal', 'cap_equal', 'draw_equal', 'contact_k_equal',
                                                                     'decisions_k_equal')} if lc else None
        cw = {}
        for x in log:
            for kk, c in (x.get('cache_check') or {}).items():
                w = cw.setdefault(kk, dict(max_abs=0., inf_pattern_equal=True, flags_differ=0, flags2_differ=0))
                w['max_abs'] = max(w['max_abs'], c['max_abs']); w['inf_pattern_equal'] &= c['inf_pattern_equal']
                w['flags_differ'] += c['flags_differ']; w['flags2_differ'] += c['flags2_differ']
        doc['cache_check_worst'] = cw
        out = CC.OUT / ('TEST_S57B_v13_rsx_extract_%s.json' % time.strftime('%Y%m%dT%H%M%S'))
    else:
        out = CC.OUT / ('EXTRACT_RSX_%s.json' % time.strftime('%Y%m%dT%H%M%S'))
    CC.write_once(out, doc)
    print('written %s' % out)


if __name__ == '__main__':
    main()
