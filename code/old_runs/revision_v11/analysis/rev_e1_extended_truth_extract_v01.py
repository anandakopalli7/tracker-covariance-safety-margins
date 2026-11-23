"""Revision v11, post hoc re-analysis R10, step 1 (ARS review of draft v10): the reaction-and-stop clearance judged against the
logged truth until the stop ends. New file, 18 Nov 2026. Descriptive; declared in AMENDMENT_08 (revision_v11).

Of record (11_ojits/A5/code/oxsb_replan_v03.py), the reaction-and-stop clearance of a decision-row pair is the smallest
rectangle-to-rectangle distance to the true actors over the 61 frames (3 s) after the decision. A pair whose stop ends after
3 s ("late") therefore keeps a flag that the window cannot confirm. Here the same trajectory is continued: after frame 60 the
ego keeps the same jerk-limited stop (oxsb_replan_v03.brake_profile; position held after standstill) along the same straight
route direction, and the truth is read from the same log (true frames only, no extrapolation) up to the frame at which the stop
ends, J = ceil(t_stop / 0.05). The extended clearance is the smallest distance over frames 0..J. If the recording ends before
frame J (the pairs of count (i)), the pair is "censored": its extended clearance covers the frames that exist.
Imports (read-only): oxsb_replan_v03 (and through it oxsb_core_v03, the Stage 1 open-loop modules and the planner library).
No guard function of oxsb_core_v03 is called; nothing is written under the project. Output: out/ext/<run>.npz and a summary.
Identity anchors (per run): the 61-frame clearance recomputed here equals the cache (review/optionA_recount_v01/cache) and the
A5 extraction's clearR_; the stop end equals the A5 extraction's tstopR_; counts of late and censored pairs.
Usage: python -B -X utf8 rev_e1_extended_truth_extract_v01.py
"""
import json, math, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
P = pathlib.Path(r'<library folder>')
OJ = P / '11_ojits'
sys.path.insert(0, str(OJ / 'A5' / 'code'))
import oxsb_replan_v03 as rp                 # noqa: E402
c3 = rp.c3; sb = rp.sb; gc = rp.gc; rx = rp.rx; oc = rp.oc; ox = rp.ox
consumer = rp.consumer; finite_primitive = rp.finite_primitive
H = rp.H

EXT = HERE / 'out' / 'ext'
EXT.mkdir(parents=True, exist_ok=True)
SUMMARY = HERE / 'out' / 'REV_E1_EXTRACT_SUMMARY_v01.json'
if SUMMARY.exists():
    sys.exit('REFUSED: %s exists' % SUMMARY)
STORED = c3.STORED
CACHE = OJ / 'review' / 'optionA_recount_v01' / 'cache'
A5X = OJ / 'A5' / 'fit' / 'main' / 'extract'
FIT_RUNS = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
VARIANTS = [(t, 6.0) for t in (0.5, 0.75, 1.0, 1.25, 1.5, 1.8)] + [(0.75, a) for a in (4.0, 5.0, 7.6)]


def window_truth_ext(T, k, kmax, nfr):
    """ol_extract_v01.window_truth with nfr frames instead of 61 and no extrapolation (true frames only)."""
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


def dist_frames(S, ego, Lg, Wd, wt):
    """S (17, nfr) positions along the route -> (17, nfr) smallest rectangle distance to any true actor per frame (inf where no
    true actor has a frame). Same geometry as ol_extract_v01.clearance (oc.rect_corners, oc.poly_dist)."""
    nfr = S.shape[1]
    u = np.array([math.cos(ego[2]), math.sin(ego[2])])
    cx = ego[0] + S * u[0]; cy = ego[1] + S * u[1]
    E = oc.rect_corners(cx, cy, ego[2], Lg / 2, Wd / 2)          # (17, nfr, 4, 2)
    Dall = np.full((17, nfr), np.inf)
    for aid, (c, hd, hl, hw) in wt.items():
        ok = np.isfinite(c[:, 0])
        if not ok.any():
            continue
        A = oc.rect_corners(c[:, 0][ok], c[:, 1][ok], hd[ok], hl, hw)
        D = oc.poly_dist(E[:, ok], A[None])
        Dall[:, ok] = np.minimum(Dall[:, ok], D)
    return Dall


def run_one(run):
    Lr = rx.load_run('fit', run, sb.YAW); T = Lr['T']; cap = Lr['cap']; kmax = Lr['kmax']
    z = np.load(STORED / (run + '.npz'), allow_pickle=False)
    cz = np.load(CACHE / (run + '_pack.npz'), allow_pickle=False)
    q = np.load(A5X / (run + '.npz'), allow_pickle=False)
    decs = list(gc.decisions(cap))
    ks = np.array([k for k, _ in decs], dtype=np.int64)
    if not (ks.shape == z['k'].shape and (ks == z['k']).all()):
        raise RuntimeError('decisions differ from the stored k')
    nd = len(decs); ev = z['evaluated'].astype(bool)
    arr = {}
    for (tau, A) in VARIANTS:
        kk = rp.vkey(tau, A)
        arr['clearX_' + kk] = np.full((nd, 17), np.nan); arr['clear61_' + kk] = np.full((nd, 17), np.nan)
        arr['tstop_' + kk] = np.full((nd, 17), np.nan); arr['jend_' + kk] = np.full((nd, 17), -1, np.int64)
        arr['cens_' + kk] = np.zeros((nd, 17), bool); arr['late_' + kk] = np.zeros((nd, 17), bool)
        arr['jmin_' + kk] = np.full((nd, 17), -1, np.int64)
    for di, (k, dec) in enumerate(decs):
        if not ev[di]:
            continue
        ms = dec['model_state']; actors = dec['actors']; now = dec['now']
        Lg, Wd = dec['ego_length'], dec['ego_width']
        rows = finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'], actors, Lg, Wd,
                                              now, consumer.Diagnostics())
        assert len(rows) == 17
        tr = T.get(k)
        left = int(kmax - k)
        for (tau, A) in VARIANTS:
            kk = rp.vkey(tau, A); jr = rp.j_of(tau)
            info = []; base = []
            for x in rows:
                sR, inf_ = rp.replan_s(x, jr, A, 'r157')
                pos, t_stop, _ = rp.brake_profile(inf_['v0'], inf_['a0'], A)
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
            wt = window_truth_ext(T, k, kmax, nfr)
            Dall = dist_frames(S, tr['ego'], Lg, Wd, wt)
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
        kk = rp.vkey(tau, A)
        c61 = arr['clear61_' + kk][ev]; cc = cz[kk][ev]; cq = q['clearR_' + kk][ev]
        chk[kk] = dict(
            clear61_vs_cache_max_abs=float(np.nanmax(np.abs(np.where(np.isfinite(c61) & np.isfinite(cc), c61 - cc, 0.)))),
            clear61_vs_cache_inf_pattern_equal=bool(np.array_equal(np.isfinite(c61), np.isfinite(cc))),
            clear61_flags_differ_cache=int(((c61 > 0) != (cc > 0)).sum()),
            clear61_flags_differ_a5=int(((c61 > 0) != (cq > 0)).sum()),
            tstop_vs_a5_max_abs=float(np.nanmax(np.abs(arr['tstop_' + kk][ev] - q['tstopR_' + kk][ev]))),
            n_pairs=int(ev.sum()) * 17, n_late=int(arr['late_' + kk][ev].sum()),
            n_late_safe61=int((arr['late_' + kk][ev] & (c61 > 0)).sum()),
            n_cens_safe61=int((arr['cens_' + kk][ev] & (c61 > 0)).sum()),
            n_flag_changed_by_extension=int(((c61 > 0) & ~(arr['clearX_' + kk][ev] > 0)).sum()),
            n_nonlate_changed=int((~arr['late_' + kk][ev] & (arr['clearX_' + kk][ev] != c61)).sum()),
            jend_max=int(arr['jend_' + kk][ev].max()))
    meta = dict(run=run, n_dec=nd, n_evaluated=int(ev.sum()), kmax=int(kmax), checks=chk, code='rev_e1_extended_truth_extract_v01.py')
    return meta, dict(k=ks, **arr)


def main():
    t0 = time.time(); metas = []
    for i, run in enumerate(FIT_RUNS):
        out = EXT / (run + '.npz')
        if out.exists():
            sys.exit('REFUSED: %s exists' % out)
        c1 = time.time()
        meta, arrs = run_one(run)
        meta['seconds'] = time.time() - c1
        np.savez_compressed(out, meta=json.dumps(meta), **arrs)
        metas.append(meta)
        c = meta['checks']['t0p75_a6p0']
        print('%s (%d / 35, %.0f s): 0.75 s: late-safe %d, censored-safe %d, changed %d; max |clear61 - cache| %.2e; flags differ %d'
              % (run, i + 1, time.time() - t0, c['n_late_safe61'], c['n_cens_safe61'], c['n_flag_changed_by_extension'],
                 c['clear61_vs_cache_max_abs'], c['clear61_flags_differ_cache']), flush=True)
    tot = {}
    for m in metas:
        for kk, c in m['checks'].items():
            t = tot.setdefault(kk, {})
            for k2, v in c.items():
                if isinstance(v, bool):
                    t[k2] = t.get(k2, True) and v
                elif k2.endswith('max_abs') or k2 == 'jend_max':
                    t[k2] = max(t.get(k2, 0), v)
                else:
                    t[k2] = t.get(k2, 0) + v
    SUMMARY.write_text(json.dumps(dict(written=time.strftime('%Y-%m-%d %H:%M:%S'), seconds=time.time() - t0, totals=tot,
                                       runs=[m['run'] for m in metas], variants=VARIANTS,
                                       expected=dict(t0p75_a6p0=dict(n_pairs=140930, count_ii_pairs=5356, count_i_pairs=153))),
                                  indent=1), encoding='utf-8')
    print(json.dumps(tot, indent=1))


if __name__ == '__main__':
    main()
