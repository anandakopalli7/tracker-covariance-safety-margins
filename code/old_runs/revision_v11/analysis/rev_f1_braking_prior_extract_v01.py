"""Revision v11, post hoc checks S20 and S18 (ARS review of draft v10), step 1: the braking prior at other decelerations on the
35 evaluation runs, and at 3 m/s^2 on the 20 benign-driving tuning runs (no braking lead). New file, 18 Nov 2026.
Descriptive; declared in AMENDMENT_08 (smaller checks).

Construction: exactly that of 11_ojits/A4/code/oxsb_extract_v05.py (lines 73-147, which copy oxsb_ctl_extract_v02.py): support =
tracked actors with a truth frame and a nonzero acceleration estimate (sb.a_hat_vec); gate = logged speed above 0.5 m/s;
shift SH = sh_cols(N, vel, -a0 u, t) with u the unit velocity; critical values gc.crit_rows(D + SH, S-bar), S-bar the
class-average projection. The functions sh_cols and the loop are imported / copied from oxsb_extract_v05 (same expressions);
only the deceleration a0 is a loop variable here. No guard function is called; nothing is written under the project.
Identity: at a0 = 3 the critical values equal the stored cCK3 of the A4 extraction bit for bit (evaluation runs); the
class-average critical values recomputed here equal the stored cF0 (all runs).
Output: out/ck/<run>.npz (cCK<a0> arrays) and out/REV_F1_CK_EXTRACT_SUMMARY_v01.json.
Usage: python -B -X utf8 rev_f1_braking_prior_extract_v01.py
"""
import json, math, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
P = pathlib.Path(r'<library folder>')
OJ = P / '11_ojits'
sys.path.insert(0, str(OJ / 'A4' / 'code'))
import oxsb_extract_v05 as ex                # noqa: E402
c3 = ex.c3; sb = ex.sb; gc = ex.gc; rx = ex.rx; oc = ex.oc; xc = ex.xc
consumer = ex.consumer; finite_primitive = ex.finite_primitive

OUTD = HERE / 'out' / 'ck'
OUTD.mkdir(parents=True, exist_ok=True)
SUMMARY = HERE / 'out' / 'REV_F1_CK_EXTRACT_SUMMARY_v01.json'
if SUMMARY.exists():
    sys.exit('REFUSED: %s exists' % SUMMARY)
STORED = c3.STORED
A4X = OJ / 'A4' / 'fit' / 'extract'
PB = json.loads(gc.PBAR_FILE.read_text(encoding='utf-8'))['Pbar']        # as oxsb_extract_v05.main (line 182)
A0_FIT = (1., 2., 3., 4., 5., 6., 7.)
A0_BENIGN = (3.,)
VMIN = 0.5


def nm(x):
    return ('%g' % x).replace('.', 'p')


def run_one(set_name, run, a0s):
    Lr = rx.load_run(set_name, run, sb.YAW); T = Lr['T']; cap = Lr['cap']; draw = Lr['draw']
    hist = xc.Hist(cap)
    z = np.load(STORED / (run + '.npz'), allow_pickle=False)
    decs = list(gc.decisions(cap))
    ks = np.array([k for k, _ in decs], dtype=np.int64)
    if not (ks.shape == z['k'].shape and (ks == z['k']).all()):
        raise RuntimeError('decisions differ from the stored k')
    nd = len(decs)
    info = {}
    for di, (k, dec) in enumerate(decs):
        tr = T.get(k); ego = tr['ego'] if tr is not None else None
        for oi, a in enumerate(dec['actors']):
            ah = sb.a_hat_vec(hist, int(a['track_id']), a['state_time'])
            if ego is None or not np.any(ah):
                continue
            mu, vel, t = sb.actor_mu(a, dec['now'])
            sp = math.hypot(vel[0], vel[1])
            d = dict(vel=vel, t=t, gate=sp > VMIN)
            if d['gate']:
                d['u'] = np.asarray(vel, float) / sp
            info[(di, oi)] = d
    out = {'cCK' + nm(a0): np.full((nd, 17), np.nan) for a0 in a0s}
    n_f0_diff = 0; n_gate_dec = 0; n_nonfinite = 0
    for di, (k, dec) in enumerate(decs):
        ms = dec['model_state']; actors = dec['actors']; now = dec['now']
        Lg, Wd = dec['ego_length'], dec['ego_width']
        rows = finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'], actors, Lg, Wd,
                                              now, consumer.Diagnostics())
        n = len(rows); assert n == 17
        na = len(actors); M = 120 * na
        if na == 0:
            for a0 in a0s:
                out['cCK' + nm(a0)][di] = z['cF0'][di]
            continue
        D = np.stack([x['d'] for x in rows]).reshape(n, M)
        N, TE, MU = gc.geometry(rows, actors, now)
        Sbar = gc.s_P(N, TE, [np.array(PB[oc.cls_of(a['name'])], float) for a in actors])
        cF0 = gc.crit_rows(D, Sbar)
        n_f0_diff += ex.same(cF0, z['cF0'][di])
        gated = [(oi, info[(di, oi)]) for oi in range(na) if (di, oi) in info and info[(di, oi)]['gate']]
        n_gate_dec += int(bool(gated))
        for a0 in a0s:
            SH = np.zeros((n, M))
            for oi, d in gated:
                blk = slice(120 * oi, 120 * oi + 120)
                SH[:, blk] = ex.sh_cols(N[:, blk], d['vel'], -a0 * d['u'], d['t'])
            n_nonfinite += int((~np.isfinite(SH)).sum())
            out['cCK' + nm(a0)][di] = gc.crit_rows(D + SH, Sbar)
    meta = dict(run=run, set=set_name, family=draw['family'], n_dec=nd, n_eval=int(z['evaluated'].sum()),
                cF0_rows_differ=n_f0_diff, decisions_with_a_gated_actor=n_gate_dec, n_nonfinite_sh=n_nonfinite,
                n_support=len(info), n_gate=int(sum(1 for d in info.values() if d['gate'])))
    return meta, dict(k=ks, **out)


def main():
    t0 = time.time(); metas = []
    fit = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
    benign = []
    for f in sorted(STORED.glob('p2_c1109_tune_*.npz')):
        m = json.loads(str(np.load(f, allow_pickle=False)['meta']))
        if m['family'] == 'benign':
            benign.append(m['run'])
    jobs = [('fit', r, A0_FIT) for r in fit] + [('tuning', r, A0_BENIGN) for r in benign]
    for i, (st, run, a0s) in enumerate(jobs):
        out = OUTD / (run + '.npz')
        if out.exists():
            sys.exit('REFUSED: %s exists' % out)
        meta, arrs = run_one(st, run, a0s)
        if st == 'fit':
            x = np.load(A4X / (run + '.npz'), allow_pickle=False)
            meta['cCK3_differs_from_A4'] = ex.same(arrs['cCK3'], x['cCK3'])
        np.savez_compressed(out, meta=json.dumps(meta), **arrs)
        metas.append(meta)
        print('%s (%d / %d, %.0f s): family %s, cF0 differ %d, cCK3 differ from A4 %s, gated decisions %d' % (
            run, i + 1, len(jobs), time.time() - t0, meta['family'], meta['cF0_rows_differ'], meta.get('cCK3_differs_from_A4'),
            meta['decisions_with_a_gated_actor']), flush=True)
    SUMMARY.write_text(json.dumps(dict(written=time.strftime('%Y-%m-%d %H:%M:%S'), seconds=time.time() - t0, runs=metas,
                                       cF0_rows_differ_total=int(sum(m['cF0_rows_differ'] for m in metas)),
                                       cCK3_differs_from_A4_total=int(sum(m.get('cCK3_differs_from_A4', 0) for m in metas)),
                                       benign_runs=benign), indent=1), encoding='utf-8')
    print('done (%.0f s)' % (time.time() - t0))


if __name__ == '__main__':
    main()
