"""Package F (revision v13): the true clearances under the departure of 19 Nov 2026 (notes\\F_DEPARTURE_CLEARANCE_v01.md: an
(actor, frame) pair is dropped when the actor's centre has a negative longitudinal coordinate in the ego frame at that frame). New
file, 19 Nov 2026 (Claude Opus 5.5). Changes no other quantity: rows, constraints and critical scales stay those of the v01 arrays.
Per scene, for the decisions of cache\\arrays_T1\\<split>\\<scene>.npz (same order; the clearance does not depend on the tracker):
  clear, clear2 (n, 17; 3 s and 2 s, NaN when not evaluated), clear_logged, clear_logged2 (the ego's own logged motion) under the
  new rule -> cache\\clear_v02\\<split>\\<scene>.npz (keys as the arrays, plus sweep).
Checks per scene (meta and log):
  1. the same code with drop_behind=False reproduces the stored v01 clearances exactly (max abs difference, inf pattern);
  2. on decisions whose index is a multiple of ID_EVERY: the pruned minimum equals a brute-force minimum over every kept pair
     (rows 3 s and the logged motion; the drop rule written again in the brute force);
  3. monotonicity: the new clearance is >= the v01 clearance wherever both are finite (dropping pairs cannot lower a minimum).
Descriptive (A10 section 8.6 allows only F0 and E on the design split): at g = 1, per source F0 and E and per horizon, evaluated
decisions whose selected row (first row with critical scale >= 1, else the fallback) is unsafe under v01 and safe under v02 (and
the reverse, which must be 0); (decision, row) pairs of evaluated decisions whose safety changes.
Usage: python -I f15_clear_v02.py <split> <nproc>   (then:  python -I f15_clear_v02.py summary <split>)
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json, multiprocessing as mp, time, traceback   # noqa: E402
import numpy as np                           # noqa: E402
import f03_adapter_v01 as AD                 # noqa: E402
import f05_arrays_v01 as F5                  # noqa: E402

ID_EVERY = 100
G1 = 1.


def brute_v02(S_rows, tc, ty, hl, hw, nframes, ego_y=None, ego_h=None):
    """Every (row, truth actor, frame) pair, no pruning, with the departure's drop rule written out per pair."""
    R = S_rows.shape[0]; out = np.full(R, np.inf)
    ey = np.zeros(nframes) if ego_y is None else ego_y; eh = np.zeros(nframes) if ego_h is None else ego_h
    for r in range(R):
        for j in range(nframes):
            if not np.isfinite(S_rows[r, j]):
                continue
            for a in range(tc.shape[0]):
                if not np.isfinite(tc[a, j, 0]):
                    continue
                dx = tc[a, j, 0] - S_rows[r, j]; dy = tc[a, j, 1] - ey[j]
                if np.cos(eh[j]) * dx + np.sin(eh[j]) * dy < 0.:
                    continue
                E = AD.rect_corners(S_rows[r, j], ey[j], eh[j], AD.EGO_L / 2., AD.EGO_W / 2.)
                A = AD.rect_corners(tc[a, j, 0], tc[a, j, 1], ty[a, j], hl[a], hw[a])
                out[r] = min(out[r], float(AD.poly_dist(E[None], A[None])[0]))
    return out


def select(c, g, idx55):
    feas = c >= g; anyf = feas.any(1)
    return np.where(anyf, feas.argmax(1), idx55)


def run_scene(args):
    split, scene = args
    out = FC.CACHE / 'clear_v02' / split / (scene + '.npz')
    if out.exists():
        return scene, 'exists', None
    try:
        t0 = time.time()
        consumer, finite_primitive = F5.planner_mods()
        FC.require_split(split)
        sc = AD.Scene(np.load(FC.CACHE / split / (scene + '.npz'), allow_pickle=False))
        Z = np.load(FC.CACHE / 'arrays_T1' / split / (scene + '.npz'), allow_pickle=False)
        last = float(sc.kf_t[-1])
        sweeps = []; recs = {k: [] for k in ('clear', 'clear2', 'clear_logged', 'clear_logged2')}
        chk = dict(v01_max_abs=0., v01_inf_differ=0, brute_n=0, brute_max_abs=0., brute_inf_differ=0, monotone_violations=0)
        old = {k: [] for k in recs}
        for di, (j, kf) in enumerate(sc.decision_sweeps()):
            now = float(sc.sw_t[j]); v_raw = float(sc.v[j]); a_raw = float(sc.a[j])
            if v_raw < -0.1 or v_raw > 20.:
                continue
            v0 = max(0., v_raw)
            s_e = sc.project(sc.ego_c[j:j + 1])[0][0]
            rows = finite_primitive.build_library(v0, a_raw, sc.desired, [], AD.EGO_L, AD.EGO_W, now, consumer.Diagnostics())
            Srows = np.stack([r['s'] for r in rows])
            ev3 = now + 3. <= last + 1e-9; ev2 = now + 2. <= last + 1e-9
            ids, tc, ty, hl, hw = F5.truth_planner(sc, now, s_e, 61)
            lc, ly = sc.ego_logged_window(now, 61)
            LX = np.full(61, np.nan); LY = np.full(61, np.nan); LH = np.full(61, np.nan)
            okl = np.isfinite(lc[:, 0])
            if okl.any():
                ls_, ll_, lth = sc.project(lc[okl])
                LX[okl] = ls_ - s_e; LY[okl] = ll_; LH[okl] = ly[okl] - lth
            nan17 = np.full(17, np.nan)
            for tag, db, store in (('new', True, recs), ('old', False, old)):
                store['clear'].append(AD.clearance_rows(Srows, tc, ty, hl, hw, 61, drop_behind=db) if ev3 else nan17)
                store['clear2'].append(AD.clearance_rows(Srows, tc, ty, hl, hw, 41, drop_behind=db) if ev2 else nan17)
                store['clear_logged'].append(float(AD.clearance_rows(LX[None], tc, ty, hl, hw, 61, LY, LH, drop_behind=db)[0])
                                             if ev3 else np.nan)
                store['clear_logged2'].append(float(AD.clearance_rows(LX[None], tc, ty, hl, hw, 41, LY, LH, drop_behind=db)[0])
                                              if ev2 else np.nan)
            sweeps.append(j)
            if di % ID_EVERY == 0 and ev3:
                cb = brute_v02(Srows, tc, ty, hl, hw, 61)
                lb_ = brute_v02(LX[None], tc, ty, hl, hw, 61, LY, LH)
                got = np.concatenate([recs['clear'][-1], [recs['clear_logged'][-1]]]); ref = np.concatenate([cb, lb_])
                fin = np.isfinite(ref) & np.isfinite(got)
                chk['brute_n'] += 1
                chk['brute_inf_differ'] += int((np.isfinite(ref) != np.isfinite(got)).sum())
                if fin.any():
                    chk['brute_max_abs'] = max(chk['brute_max_abs'], float(np.abs(ref[fin] - got[fin]).max()))
        sweeps = np.array(sweeps)
        if not np.array_equal(sweeps, Z['sweep']):
            raise RuntimeError('decision order differs from the v01 arrays')
        A = {k: np.array(v, float) for k, v in recs.items()}
        O = {k: np.array(v, float) for k, v in old.items()}
        for k in A:
            st = Z[k].astype(float)
            same_pat = (np.isnan(st) == np.isnan(O[k])) & (np.isposinf(st) == np.isposinf(O[k]))
            chk['v01_inf_differ'] += int((~same_pat).sum())
            f = np.isfinite(st) & np.isfinite(O[k])
            if f.any():
                chk['v01_max_abs'] = max(chk['v01_max_abs'], float(np.abs(st[f] - O[k][f]).max()))
            both = np.isfinite(A[k]) & np.isfinite(st)
            chk['monotone_violations'] += int((A[k][both] < st[both]).sum()) + int((np.isposinf(st) & np.isfinite(A[k])).sum())
        # descriptive counts at g = 1 (F0 and E only) and safety changes of (decision, row) pairs
        desc = {}
        for hz, ck, sfx, evk in ((3, 'clear', '', 'evaluated'), (2, 'clear2', '_2', 'evaluated2')):
            ev = Z[evk].astype(bool)
            s1 = Z[ck].astype(float) > 0; s2 = A[ck] > 0
            idx55 = Z['idx55'].astype(np.int64); ar = np.arange(ev.size)
            d = dict(n_evaluated=int(ev.sum()), rows_unsafe_to_safe=int((~s1 & s2)[ev].sum()),
                     rows_safe_to_unsafe=int((s1 & ~s2)[ev].sum()), rows_unsafe_v01=int((~s1)[ev].sum()),
                     rows_unsafe_v02=int((~s2)[ev].sum()))
            for src in ('F0', 'E'):
                sel = select(np.asarray(Z['c' + src + sfx], float), G1, idx55)
                u1 = ~s1[ar, sel]; u2 = ~s2[ar, sel]
                d[src] = dict(wrong_go_v01=int((u1 & ev).sum()), wrong_go_v02=int((u2 & ev).sum()),
                              removed=int((u1 & ~u2 & ev).sum()), added=int((~u1 & u2 & ev).sum()))
            desc['%d s' % hz] = d
        meta = dict(scene=scene, split=split, n_dec=int(sweeps.size), checks=chk, g1_counts=desc, seconds=round(time.time() - t0, 1),
                    rule='notes\\F_DEPARTURE_CLEARANCE_v01.md')
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix('.tmp.npz')
        np.savez_compressed(tmp, meta=json.dumps(meta), sweep=sweeps, **A)
        tmp.replace(out)
        return scene, 'ok n=%d checks=%s %.1fs' % (sweeps.size, json.dumps(chk), meta['seconds']), meta
    except Exception as e:
        return scene, 'ERROR %r %s' % (e, traceback.format_exc()[-1500:]), None


def summary(split):
    FC.require_split(split)
    outf = FC.OUT / ('F_CLEAR_V02_%s_v01.json' % split)
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    names = sorted(FC.splits()[split])
    chk = dict(v01_max_abs=0., v01_inf_differ=0, brute_n=0, brute_max_abs=0., brute_inf_differ=0, monotone_violations=0)
    agg = {}
    missing = []
    for nm in names:
        p = FC.CACHE / 'clear_v02' / split / (nm + '.npz')
        if not p.exists():
            missing.append(nm); continue
        m = json.loads(str(np.load(p, allow_pickle=False)['meta']))
        for k, v in m['checks'].items():
            chk[k] = max(chk[k], v) if k.endswith('max_abs') else chk[k] + v
        for hz, d in m['g1_counts'].items():
            a = agg.setdefault(hz, {})
            for k, v in d.items():
                if isinstance(v, dict):
                    b = a.setdefault(k, {})
                    for kk, vv in v.items():
                        b[kk] = b.get(kk, 0) + vv
                else:
                    a[k] = a.get(k, 0) + v
    if missing:
        raise SystemExit('REFUSED: %d scenes missing, e.g. %s' % (len(missing), missing[:3]))
    passed = (chk['v01_max_abs'] == 0. and chk['v01_inf_differ'] == 0 and chk['brute_inf_differ'] == 0 and chk['brute_max_abs'] <= 1e-9
              and chk['monotone_violations'] == 0)
    doc = dict(code='f15_clear_v02.py summary', split=split, written=FC.clock(), rule='notes\\F_DEPARTURE_CLEARANCE_v01.md',
               rule_sha256=FC.sha256_file(FC.F / 'notes' / 'F_DEPARTURE_CLEARANCE_v01.md'), n_scenes=len(names), checks=chk,
               checks_passed=bool(passed), g1_counts=agg,
               note='F0 and E only on the design split (A10 section 8.6); selection at g = 1: first row with critical scale >= 1, '
                    'else the fallback row; "removed" = unsafe under the clearance of record and safe under the new rule')
    outf.write_text(FC.jdump(doc), encoding='utf-8')
    print('WROTE', outf, 'checks passed:', passed)
    print(FC.jdump(dict(checks=chk, g1_counts=agg)))


def main():
    if sys.argv[1] == 'summary':
        return summary(sys.argv[2])
    split, nproc = sys.argv[1], int(sys.argv[2])
    FC.require_split(split)
    scenes = sys.argv[3:] or sorted(FC.splits()[split])
    log = FC.LOGS / ('f15_clear_v02_%s.log' % split)
    with mp.Pool(nproc) as pool:
        for scene, msg, _ in pool.imap_unordered(run_scene, [(split, s) for s in scenes]):
            with open(log, 'a', encoding='utf-8') as f:
                f.write('%s %s %s\n' % (FC.clock(), scene, msg))
    print(FC.clock(), 'finished clear_v02', split, len(scenes), flush=True)


if __name__ == '__main__':
    main()
