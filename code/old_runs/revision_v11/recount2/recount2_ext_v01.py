"""Second program (recount2): the "extended truth" of the reaction-and-stop scoring, recomputed from the specification.

Written without reading the first program (revision_v11\\analysis). Reads the data project read-only; writes only into this folder.

Per fit lead-braking run (p1b_fit_finite_0005 .. 0039), per evaluated decision, per row (17), per setting (tau, A):
  1. s_R = oxsb_replan_v03.replan_s(row, j_react, A, 'r157') for frames 0..60; beyond frame 60 the same brake profile is continued:
     s[j] = s[j_react] + pos((j - j_react) * 0.05), pos from oxsb_replan_v03.brake_profile(v0, a0, A) (holds after standstill).
     t_stop_abs = j_react * 0.05 + t_stop.
  2. J = max(60, ceil(t_stop_abs / 0.05 - 1e-9)); late = t_stop_abs > 3.0 + 1e-9.
  3. True actors: rx.load_run('fit', run, sb.YAW) -> T, kmax. As ol_extract_v01.window_truth does with allow_extrap False: the actors
     present at the decision frame k, each over its contiguous true frames from k (stops at the first frame without it); here up to
     frame k + J instead of k + 60, as far as the recording goes. Ego rectangle along the straight direction tr['ego'][2] from
     tr['ego'][:2] (ol_extract_v01.clearance: oc.rect_corners, oc.poly_dist).
  4. Extended clearance = min rectangle distance to any true actor over frames 0..min(J, last available frame).
     censored = late and J > kmax - k.
  5. Anchors: (a) own computation on frames 0..60 against the stored clearR_<key>; (b) t_stop_abs against tstopR_<key>;
     (c) counts at (0.75, 6).
Output: out\\<run>.npz (clearX_, clear61_, late_, cens_, tstop_, J_ per key; k, evaluated) and RECOUNT2_RESULTS_v01.json.
Usage: python -B -X utf8 recount2_ext_v01.py
"""
import json, math, pathlib, sys, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
P = pathlib.Path(r'<library folder>')
sys.path.insert(0, str(P / '11_ojits' / 'A5' / 'code'))
import oxsb_replan_v03 as rp                       # noqa: E402  (code of record: replan_s, brake_profile, j_of, vkey)
from oxsb_replan_v03 import c3, sb, gc, rx, oc, consumer, finite_primitive   # noqa: E402

H = 0.05
SETTINGS = [(0.5, 6.0), (0.75, 6.0), (1.0, 6.0), (1.25, 6.0), (1.5, 6.0), (1.8, 6.0), (0.75, 4.0), (0.75, 5.0), (0.75, 7.6)]
KEYS = [rp.vkey(t, a) for t, a in SETTINGS]
RUNS = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
STORED = P / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
EXTRACT = P / '11_ojits' / 'A5' / 'fit' / 'main' / 'extract'
PACK = P / '11_ojits' / 'review' / 'optionA_recount_v01' / 'cache'
OUT = HERE / 'out'
LOG = HERE / 'recount2_ext_v01.log'


def log(msg):
    line = '%s  %s' % (time.strftime('%H:%M:%S'), msg)
    print(line, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def truth_arrays(T, kmax):
    """Per true actor: presence per frame, (cx, cy, heading, half length, half width) per frame, and end[k] = the first frame >= k
    without the actor (kmax + 1 if present to the end). Frames missing from T count as 'actor absent'."""
    n = kmax + 1
    ids = []
    for k in sorted(T):
        for aid in T[k]['actors']:
            if aid not in ids:
                ids.append(aid)
    out = {}
    for aid in ids:
        pres = np.zeros(n, bool); arr = np.full((n, 5), np.nan)
        for k, fr in T.items():
            a = fr['actors'].get(aid)
            if a is not None:
                pres[k] = True; arr[k] = a[:5]
        end = np.empty(n + 1, np.int64); end[n] = n
        for k in range(n - 1, -1, -1):
            end[k] = end[k + 1] if pres[k] else k
        out[aid] = (pres, arr, end)
    return out


def do_run(run):
    c0 = time.process_time()
    L = rx.load_run('fit', run, sb.YAW); T = L['T']; cap = L['cap']; kmax = int(L['kmax'])
    if min(T) < 0:
        raise RuntimeError('negative truth frame index')
    z = np.load(STORED / (run + '.npz'), allow_pickle=False)
    q = np.load(EXTRACT / (run + '.npz'), allow_pickle=False)
    pk = np.load(PACK / (run + '_pack.npz'), allow_pickle=False)
    decs = list(gc.decisions(cap))
    ks = np.array([k for k, _ in decs], dtype=np.int64)
    if not (ks.shape == z['k'].shape and (ks == z['k']).all()):
        raise RuntimeError('%s: decisions differ from the stored k' % run)
    ev = z['evaluated'].astype(bool)
    nd = len(decs)
    TA = truth_arrays(T, kmax)
    truth_contiguous = (sorted(T) == list(range(0, kmax + 1)))
    ext_const = all(len({(float(a[3]), float(a[4])) for a in arr[pres]}) == 1 for pres, arr, end in TA.values())
    arr = {}
    for kk in KEYS:
        arr['clearX_' + kk] = np.full((nd, 17), np.nan); arr['clear61_' + kk] = np.full((nd, 17), np.nan)
        arr['tstop_' + kk] = np.full((nd, 17), np.nan); arr['J_' + kk] = np.full((nd, 17), -1, np.int64)
        arr['late_' + kk] = np.zeros((nd, 17), bool); arr['cens_' + kk] = np.zeros((nd, 17), bool)
    n_ev_mismatch = 0; n_actor_ends_early = 0; n_prefix_differs = 0; n_tstop_differs_fn = 0
    ar = np.arange(17)
    for di, (k, dec) in enumerate(decs):
        tr = T.get(k)
        prim = tr['target_id'] if tr else None
        my_ev = (tr is not None and prim is not None and prim in tr['actors'] and k + 60 <= kmax)
        n_ev_mismatch += int(my_ev != bool(ev[di]))
        if not ev[di]:
            continue
        ms = dec['model_state']; actors = dec['actors']; now = dec['now']
        Lg, Wd = dec['ego_length'], dec['ego_width']
        rows = finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'], actors, Lg, Wd,
                                              now, consumer.Diagnostics())
        if len(rows) != 17:
            raise RuntimeError('%s k %d: %d rows' % (run, k, len(rows)))
        ego = tr['ego']
        ux, uy = math.cos(ego[2]), math.sin(ego[2])
        left = kmax - k
        for (tau, A), kk in zip(SETTINGS, KEYS):
            jr = rp.j_of(tau)
            sR = []; poss = []; tsa = np.empty(17); Jr = np.empty(17, np.int64); sjr = np.empty(17)
            for ri, x in enumerate(rows):
                s61, info = rp.replan_s(x, jr, A, 'r157')
                pos, t_stop, v_max = rp.brake_profile(float(x['v'][jr]), float(x['a'][jr - 1]), A)
                n_tstop_differs_fn += int(t_stop != info['t_stop'])
                sR.append(s61); poss.append(pos); sjr[ri] = float(np.asarray(x['s'], float)[jr])
                tsa[ri] = jr * H + t_stop
                Jr[ri] = max(60, int(math.ceil(tsa[ri] / H - 1e-9)))
            Jmax = int(Jr.max())
            S = np.empty((17, Jmax + 1))
            for ri in range(17):
                S[ri, :61] = sR[ri]
                # the same expression for j_react < j <= 60 must reproduce replan_s
                for j in (jr + 1, 60):
                    n_prefix_differs += int(sjr[ri] + poss[ri]((j - jr) * H) != sR[ri][j])
                for j in range(61, Jmax + 1):
                    S[ri, j] = sjr[ri] + poss[ri]((j - jr) * H)
            n_av = min(Jmax, left) + 1                               # frames 0..n_av-1 exist in the recording
            E = oc.rect_corners(ego[0] + S[:, :n_av] * ux, ego[1] + S[:, :n_av] * uy, ego[2], Lg / 2, Wd / 2)   # (17, n_av, 4, 2)
            clX = np.full(17, np.inf); cl61 = np.full(17, np.inf)
            for aid in tr['actors']:
                pres, ta, end = TA[aid]
                n_a = int(min(end[k], k + n_av) - k)                 # contiguous true frames of this actor from k
                if n_a <= 0:
                    continue
                n_actor_ends_early += int(n_a < n_av)
                a = ta[k:k + n_a]
                Ac = oc.rect_corners(a[:, 0], a[:, 1], a[:, 2], a[:, 3], a[:, 4])            # (n_a, 4, 2)
                D = oc.poly_dist(E[:, :n_a], Ac[None])                                       # (17, n_a)
                cum = np.minimum.accumulate(D, axis=1)
                clX = np.minimum(clX, cum[ar, np.minimum(Jr, n_a - 1)])
                cl61 = np.minimum(cl61, cum[:, min(60, n_a - 1)])
            late = tsa > 3.0 + 1e-9
            arr['clearX_' + kk][di] = clX; arr['clear61_' + kk][di] = cl61; arr['tstop_' + kk][di] = tsa; arr['J_' + kk][di] = Jr
            arr['late_' + kk][di] = late; arr['cens_' + kk][di] = late & (Jr > left)
    # ---- anchors and counts of this run
    res = dict(run=run, n_dec=nd, n_evaluated=int(ev.sum()), kmax=kmax, truth_frames_contiguous=bool(truth_contiguous),
               actor_extents_constant=bool(ext_const), n_true_actors=len(TA), n_evaluated_flag_mismatch=n_ev_mismatch,
               n_actor_ends_before_window=n_actor_ends_early, n_prefix_differs=n_prefix_differs, n_tstop_differs_fn=n_tstop_differs_fn,
               settings={})
    E2 = ev[:, None] & np.ones((1, 17), bool)
    for kk in KEYS:
        cX = arr['clearX_' + kk]; c61 = arr['clear61_' + kk]; late = arr['late_' + kk]; cens = arr['cens_' + kk]
        sc_ = q['clearR_' + kk]; st = q['tstopR_' + kk]; sp = pk[kk]
        safe61 = (c61 > 0) & E2; safeS = (sc_ > 0) & E2
        d = np.abs(c61[E2] - sc_[E2]); dp = np.abs(c61[E2] - sp[E2]); dt = np.abs(arr['tstop_' + kk][E2] - st[E2])
        ls = late & safe61
        res['settings'][kk] = dict(
            n_pairs=int(E2.sum()),
            anchor_a_flags_differ=int((safe61 != safeS).sum()), anchor_a_max_abs_diff=float(np.nanmax(d)) if d.size else 0.,
            anchor_a_n_nonfinite=int((~np.isfinite(d)).sum()),
            anchor_a_pack_max_abs_diff=float(np.nanmax(dp)) if dp.size else 0., anchor_a_pack_flags_differ=int((((sp > 0) & E2) != safe61).sum()),
            anchor_b_max_abs_diff=float(np.nanmax(dt)) if dt.size else 0., anchor_b_n_not_equal=int((arr['tstop_' + kk][E2] != st[E2]).sum()),
            stored_tstop_nonfinite_in_evaluated=int((~np.isfinite(st[E2])).sum()),
            n_late=int((late & E2).sum()), n_late_safe61=int(ls.sum()), n_cens_safe61=int((ls & cens).sum()),
            n_cens_all=int((cens & E2).sum()),
            n_late_safe61_unsafeX=int((ls & ~(cX > 0)).sum()),
            n_late_safe61_unsafeX_censored=int((ls & cens & ~(cX > 0)).sum()),
            n_late_safe61_unsafeX_not_censored=int((ls & ~cens & ~(cX > 0)).sum()),
            n_unsafe61=int((~(c61 > 0) & E2).sum()), n_unsafeX=int((~(cX > 0) & E2).sum()),
            n_notlate_clearX_differs_from_61=int(((cX != c61) & ~late & E2).sum()),
            n_clearX_above_61=int(((cX > c61) & E2).sum()),
            J_max=int(arr['J_' + kk][E2].max()) if E2.any() else -1,
            tstop_max=float(np.nanmax(arr['tstop_' + kk][E2])) if E2.any() else float('nan'))
    OUT.mkdir(exist_ok=True)
    np.savez_compressed(OUT / (run + '.npz'), k=ks, evaluated=ev, kmax=np.int64(kmax), **arr)
    res['cpu_s'] = time.process_time() - c0
    return res


def main():
    t0 = time.time()
    if c3.RUNS['fit'] != RUNS:
        raise RuntimeError('run list differs from the code of record')
    log('recount2_ext_v01 started: %d runs, %d settings %s' % (len(RUNS), len(SETTINGS), KEYS))
    per_run = []
    for i, run in enumerate(RUNS):
        r = do_run(run)
        per_run.append(r)
        s = r['settings'][rp.vkey(0.75, 6.0)]
        log('%d/%d %s ev %d cpu %.1f s | a: flags %d maxdiff %.2e | b: maxdiff %.2e | t0p75_a6p0 late&safe61 %d cens %d flips %d' % (
            i + 1, len(RUNS), run, r['n_evaluated'], r['cpu_s'], sum(v['anchor_a_flags_differ'] for v in r['settings'].values()),
            max(v['anchor_a_max_abs_diff'] for v in r['settings'].values()), max(v['anchor_b_max_abs_diff'] for v in r['settings'].values()),
            s['n_late_safe61'], s['n_cens_safe61'], s['n_late_safe61_unsafeX']))
    tot = {}
    SUM = ('n_pairs', 'anchor_a_flags_differ', 'anchor_a_n_nonfinite', 'anchor_a_pack_flags_differ', 'anchor_b_n_not_equal',
           'stored_tstop_nonfinite_in_evaluated', 'n_late', 'n_late_safe61', 'n_cens_safe61', 'n_cens_all', 'n_late_safe61_unsafeX',
           'n_late_safe61_unsafeX_censored', 'n_late_safe61_unsafeX_not_censored', 'n_unsafe61', 'n_unsafeX',
           'n_notlate_clearX_differs_from_61', 'n_clearX_above_61')
    MAX = ('anchor_a_max_abs_diff', 'anchor_a_pack_max_abs_diff', 'anchor_b_max_abs_diff', 'J_max', 'tstop_max')
    for (tau, A), kk in zip(SETTINGS, KEYS):
        t = dict(tau=tau, A=A, key=kk)
        for f in SUM:
            t[f] = int(sum(r['settings'][kk][f] for r in per_run))
        for f in MAX:
            t[f] = max(r['settings'][kk][f] for r in per_run)
        tot[kk] = t
    m = tot[rp.vkey(0.75, 6.0)]
    anchors = dict(
        a_flags_identical_all_settings=bool(all(t['anchor_a_flags_differ'] == 0 for t in tot.values())),
        a_max_abs_diff_all_settings=max(t['anchor_a_max_abs_diff'] for t in tot.values()),
        a_within_1e9=bool(all(t['anchor_a_max_abs_diff'] <= 1e-9 and t['anchor_a_n_nonfinite'] == 0 for t in tot.values())),
        a_pack_max_abs_diff=max(t['anchor_a_pack_max_abs_diff'] for t in tot.values()),
        a_pack_flags_differ=int(sum(t['anchor_a_pack_flags_differ'] for t in tot.values())),
        b_tstop_max_abs_diff=max(t['anchor_b_max_abs_diff'] for t in tot.values()),
        b_tstop_n_not_bitwise_equal=int(sum(t['anchor_b_n_not_equal'] for t in tot.values())),
        c_t0p75_a6p0=dict(n_pairs=m['n_pairs'], expected_pairs=140930, n_late_safe61=m['n_late_safe61'], expected_late_safe61=5356,
                          n_cens_safe61=m['n_cens_safe61'], expected_cens_safe61=153,
                          holds=bool(m['n_pairs'] == 140930 and m['n_late_safe61'] == 5356 and m['n_cens_safe61'] == 153)),
        decisions_k_equal_stored='checked per run (the program stops otherwise)',
        n_evaluated_flag_mismatch=int(sum(r['n_evaluated_flag_mismatch'] for r in per_run)),
        n_prefix_differs=int(sum(r['n_prefix_differs'] for r in per_run)),
        n_tstop_differs_between_replan_s_and_brake_profile=int(sum(r['n_tstop_differs_fn'] for r in per_run)),
        truth_frames_contiguous_all_runs=bool(all(r['truth_frames_contiguous'] for r in per_run)),
        actor_extents_constant_all_runs=bool(all(r['actor_extents_constant'] for r in per_run)),
        n_actor_ends_before_window=int(sum(r['n_actor_ends_before_window'] for r in per_run)),
        max_true_actors_per_run=max(r['n_true_actors'] for r in per_run))
    doc = dict(program='recount2_ext_v01.py (second program; written from the specification, first program not read)',
               written=time.strftime('%Y-%m-%d %H:%M:%S'), n_runs=len(RUNS), runs=RUNS, settings=[[t, a] for t, a in SETTINGS], keys=KEYS,
               n_decisions=int(sum(r['n_dec'] for r in per_run)), n_evaluated_decisions=int(sum(r['n_evaluated'] for r in per_run)),
               anchors=anchors, totals=tot, per_run=per_run, seconds=time.time() - t0)
    (HERE / 'RECOUNT2_RESULTS_v01.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')
    log('done in %.0f s; anchors: %s' % (time.time() - t0, json.dumps(anchors)))
    for kk in KEYS:
        t = tot[kk]
        log('%s: late&safe61 %d, censored %d, flips %d (censored %d), unsafe61 %d, unsafeX %d' % (
            kk, t['n_late_safe61'], t['n_cens_safe61'], t['n_late_safe61_unsafeX'], t['n_late_safe61_unsafeX_censored'], t['n_unsafe61'], t['n_unsafeX']))


if __name__ == '__main__':
    main()
