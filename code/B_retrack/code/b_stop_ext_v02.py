"""v13 package B: the reaction-and-stop clearance judged until the stop ends (A10 section 1: "The reaction-and-stop scoring, with plans
judged until the stop ends"), for a reaction time tau_i per decision (B6(b) delayed stop). New file, 20 Nov 2026 (Claude Opus 5.5).

It joins two pieces of record, unchanged in substance:
  * revision_v11 rev_e1_extended_truth_extract_v01 (the extension: after frame 60 the same jerk-limited stop continues along the same
    straight route direction, position held after standstill; truth read from the log, true frames only, up to the frame J at which
    the stop ends, J = max(60, ceil(t_stop / 0.05)); the extended clearance clearX is the smallest distance over frames 0..J; a pair
    whose recording ends before J is "censored" and covers the frames that exist; window_truth_ext and dist_frames copied);
  * trk_score_v01.stop_profile_cont / row_state_at / _first_stop (the stop from the row's state at any tau, also inside a step),
    evaluated here at every frame up to J instead of the 61 frames.
Test (--test-old, old runs, read-only): (a) tau = 0.75 for every evaluated decision must reproduce revision_v11 out\\ext
clearX_t0p75_a6p0 (and clear61 the stop cache of record); (b) with the delayed taus of b6_stop_v01 (out\\b6\\clear\\<run>.npz), the
61-frame part must reproduce v01's delayed-stop clearances. Writes out\\fresh_testold\\STOP_EXT_TEST_v02.json.
Usage: python -I -B -X utf8 b_stop_ext_v02.py --test-old [--workers 3] [--runs a,b]   (system python: the tracker stack)
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import sys, json, math, pathlib, time, argparse
HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parent / 'shared' / 'trackers'))
import trk_env_v01 as env
env.setup()
import numpy as np
import trk_score_v01 as S
import trk_arrays_v01 as TA
H = S.H; JERK = S.JERK


def window_truth_ext(T, k, kmax, nfr):
    """rev_e1_extended_truth_extract_v01.window_truth_ext (same lines): nfr frames, true frames only."""
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


def dist_frames(Sx, ego, Lg, Wd, wt):
    """rev_e1_extended_truth_extract_v01.dist_frames (same lines)."""
    nfr = Sx.shape[1]
    u = np.array([math.cos(ego[2]), math.sin(ego[2])])
    cx = ego[0] + Sx * u[0]; cy = ego[1] + Sx * u[1]
    E = TA.oc.rect_corners(cx, cy, ego[2], Lg / 2, Wd / 2)
    Dall = np.full((17, nfr), np.inf)
    for aid, (c, hd, hl, hw) in wt.items():
        ok = np.isfinite(c[:, 0])
        if not ok.any():
            continue
        A = TA.oc.rect_corners(c[:, 0][ok], c[:, 1][ok], hd[ok], hl, hw)
        D = TA.oc.poly_dist(E[:, ok], A[None])
        Dall[:, ok] = np.minimum(Dall[:, ok], D)
    return Dall


def stop_ext(s_row, v_row, a_row, tau, A):
    """trk_score_v01.stop_profile_cont's stop, as a function of frame: returns (pos(j) for any frame j >= 0, t_end = tau + stop time)."""
    s_row = np.asarray(s_row, float)
    x0, v0, a0 = S.row_state_at(s_row, v_row, a_row, tau)
    jr = -JERK if a0 > -A else JERK
    t1 = abs(-A - a0) / JERK
    ts = S._first_stop(v0, a0, jr, t1, A)
    x1 = x0 + v0 * t1 + .5 * a0 * t1 ** 2 + jr * t1 ** 3 / 6.
    v1 = v0 + a0 * t1 + .5 * jr * t1 ** 2

    def pos(jj):
        jj = np.asarray(jj); out = np.empty(jj.shape, float)
        before = ~(jj * H > tau + 1e-9)
        out[before] = s_row[jj[before]]
        t = np.minimum(jj[~before] * H - tau, ts)
        tr = np.minimum(t, t1); th = np.maximum(t - t1, 0.)
        ramp = x0 + v0 * tr + .5 * a0 * tr ** 2 + jr * tr ** 3 / 6.
        hold = x1 + v1 * th - .5 * A * th ** 2
        out[~before] = np.where(t <= t1, ramp, hold)
        return out
    return pos, tau + ts


def delayed_stop_clearance_ext(rd, cap, taus, A=6.0):
    """taus: {decision index: tau_i}. Returns dict of (n_dec, 17) arrays: clearX (until the stop ends), clear61 (61 frames),
    tstop (stop end, s after the decision), jend, late (tstop > 3 s), cens (late and the recording ends before jend)."""
    Lr = TA.load_capture(rd, cap)
    T = Lr['T']; kmax = Lr['kmax']
    decs = list(TA.gc.decisions(Lr['cap'])); nd = len(decs)
    out = dict(clearX=np.full((nd, 17), np.nan), clear61=np.full((nd, 17), np.nan), tstop=np.full((nd, 17), np.nan),
               jend=np.full((nd, 17), -1, np.int64), late=np.zeros((nd, 17), bool), cens=np.zeros((nd, 17), bool))
    for di, (k, dec) in enumerate(decs):
        if di not in taus:
            continue
        ms = dec['model_state']; Lg, Wd = dec['ego_length'], dec['ego_width']
        rows = TA.finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'],
                                                 dec['actors'], Lg, Wd, dec['now'], TA.consumer.Diagnostics())
        assert len(rows) == 17
        prof = [stop_ext(r['s'], r['v'], r['a'], float(taus[di]), A) for r in rows]
        tst = np.array([p[1] for p in prof])
        jend = np.maximum(60, np.ceil(tst / H - 1e-9).astype(np.int64))
        late = tst > 3.0 + 1e-9
        left = int(kmax - k)
        nfr = int(min(jend.max(), max(left, 60))) + 1
        jj = np.arange(nfr)
        Sx = np.stack([p[0](jj) for p in prof])
        wt = window_truth_ext(T, k, kmax, nfr)
        Dall = dist_frames(Sx, T[k]['ego'], Lg, Wd, wt)
        out['clear61'][di] = Dall[:, :61].min(axis=1)
        for ri in range(17):
            je = int(min(jend[ri], nfr - 1))
            out['clearX'][di, ri] = Dall[ri, :je + 1].min()
        out['tstop'][di] = tst; out['jend'][di] = jend; out['late'][di] = late; out['cens'][di] = late & (jend > left)
    return out


# ------------------------------------------------------------------------------------------------ test on old runs
EXT = pathlib.Path(r'ARS_TRIAL\revision_v11\analysis\out\ext')
CACHE = S.P / '11_ojits' / 'review' / 'optionA_recount_v01' / 'cache'
ARCH = S.P / '07_fit_runs' / 'archives'
STORED = S.P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
V01CLEAR = HERE / 'out' / 'b6' / 'clear'


def diff(a, b, ev):
    a = a[ev]; b = b[ev]
    fin = np.isfinite(a) & np.isfinite(b)
    return dict(max_abs=float(np.max(np.abs(a[fin] - b[fin]))) if fin.any() else 0., finite_pattern_equal=bool(np.array_equal(np.isfinite(a), np.isfinite(b))),
                safe_flags_differ=int(((np.nan_to_num(a, nan=-1.) > 0) != (np.nan_to_num(b, nan=-1.) > 0)).sum()), cells=int(a.size))


def test_one(run):
    t0 = time.time()
    z = np.load(STORED / (run + '.npz'), allow_pickle=False); ev = z['evaluated'].astype(bool)
    cap = list((ARCH / run / 'x' / run / 'capture').iterdir())[0]; rd = ARCH / run
    x = np.load(EXT / (run + '.npz'), allow_pickle=False); cz = np.load(CACHE / (run + '_pack.npz'), allow_pickle=False)
    a = delayed_stop_clearance_ext(rd, cap, {int(i): 0.75 for i in np.flatnonzero(ev)}, A=6.0)
    res = dict(run=run, a_clearX_vs_v11_ext=diff(a['clearX'], x['clearX_t0p75_a6p0'], ev), a_clear61_vs_cache=diff(a['clear61'], cz['t0p75_a6p0'], ev),
               a_tstop_max_abs=float(np.nanmax(np.abs(a['tstop'][ev] - x['tstop_t0p75_a6p0'][ev]))),
               a_jend_equal=bool(np.array_equal(a['jend'][ev], x['jend_t0p75_a6p0'][ev])),
               a_cens_equal=bool(np.array_equal(a['cens'][ev], x['cens_t0p75_a6p0'][ev])),
               a_late_equal=bool(np.array_equal(a['late'][ev], x['late_t0p75_a6p0'][ev])))
    v = np.load(V01CLEAR / (run + '.npz'))
    taus = {int(i): float(v['tau'][i]) for i in np.flatnonzero(ev)}
    b = delayed_stop_clearance_ext(rd, cap, taus, A=6.0)
    od = HERE / 'out' / 'fresh_testold' / 'b6_clear_ext'; od.mkdir(parents=True, exist_ok=True)   # for the B6 dry run on old runs
    tz = np.full(z['k'].size, np.nan)
    for i, t in taus.items():
        tz[i] = t
    np.savez_compressed(od / (run + '.npz'), clear=b['clearX'], clear61=b['clear61'], tstop=b['tstop'], jend=b['jend'], late=b['late'],
                        cens=b['cens'], tau=tz, k=z['k'])
    res['b_clear61_vs_v01_delayed'] = diff(b['clear61'], v['clear'], ev)
    res['b_n_flag_changed_by_extension'] = int(((b['clear61'][ev] > 0) & ~(b['clearX'][ev] > 0)).sum())
    res['seconds'] = round(time.time() - t0, 1)
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--test-old', action='store_true'); ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--runs', default=None)
    a = ap.parse_args()
    if not a.test_old:
        raise SystemExit('only --test-old here; the fresh clearances are computed by b_fresh_b6_v02.py clear')
    runs = a.runs.split(',') if a.runs else ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
    from concurrent.futures import ProcessPoolExecutor
    t0 = time.time(); res = []
    with ProcessPoolExecutor(a.workers) as ex:
        for r in ex.map(test_one, runs):
            res.append(r)
            print(r['run'], r['a_clearX_vs_v11_ext']['max_abs'], r['a_clearX_vs_v11_ext']['safe_flags_differ'],
                  r['b_clear61_vs_v01_delayed']['max_abs'], r['b_clear61_vs_v01_delayed']['safe_flags_differ'], r['seconds'], flush=True)
    keys = ('a_clearX_vs_v11_ext', 'a_clear61_vs_cache', 'b_clear61_vs_v01_delayed')
    tot = {k: dict(max_abs=max(r[k]['max_abs'] for r in res), safe_flags_differ=sum(r[k]['safe_flags_differ'] for r in res),
                   finite_pattern_equal=all(r[k]['finite_pattern_equal'] for r in res), cells=sum(r[k]['cells'] for r in res)) for k in keys}
    tot.update(a_tstop_max_abs=max(r['a_tstop_max_abs'] for r in res), a_jend_equal=all(r['a_jend_equal'] for r in res),
               a_cens_equal=all(r['a_cens_equal'] for r in res), a_late_equal=all(r['a_late_equal'] for r in res),
               b_n_flag_changed_by_extension=sum(r['b_n_flag_changed_by_extension'] for r in res))
    doc = dict(code='b_stop_ext_v02.py --test-old', runs=len(res), totals=tot, per_run=res, seconds=time.time() - t0,
               written=time.strftime('%Y-%m-%d %H:%M:%S'))
    od = HERE / 'out' / 'fresh_testold'; od.mkdir(parents=True, exist_ok=True)
    (od / ('STOP_EXT_TEST_v02.json' if not a.runs else 'STOP_EXT_TEST_partial_v02.json')).write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(json.dumps(tot, indent=1))


if __name__ == '__main__':
    main()
