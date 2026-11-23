"""Package F (revision v13): adapter check of the horizon rule's outcome on the design split (A10 section 8.6: adapter checks). New
file, 19 Nov 2026 (Claude Opus 5.5), written after the horizon rule found no room at 3 s or 2 s (out\\F_HORIZON_RULE_v01.json) to
find why. Uses the T1 train arrays (F0 and E only; no N, TG or IMM array) and the train truth geometry; computes no share, frontier
or room.
  Part 1, from the stored arrays, 3 s, all evaluated decisions: rows and decisions with critical scale -inf; for margin scales g in
    G_LIST, selections of F0 and E by the library's rule (first row with critical scale >= g, else the fallback row idx55): fallback
    share, wrong-go share (selected row's true clearance <= 0), wrong go among fallback and non-fallback selections, mean speed.
  Part 2, geometry: on a sample of 300 of F0's unsafe fallback selections at g = 1 (default_rng(1), a diagnostic draw, not a seed of
    record), the truth actor that first touches the fallback row (first frame with box distance 0; at that frame the closest actor):
    its class, whether it is behind the ego at the decision time and at contact (planner frame), the contact frame.
Writes out\\F_ROOM_MECHANISM_T1_train_v01.json (refuses to overwrite).
Usage: python -I f14_room_mechanism_v01.py
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json                                  # noqa: E402
from collections import Counter              # noqa: E402
import numpy as np                           # noqa: E402
import f03_adapter_v01 as AD                 # noqa: E402
import f05_arrays_v01 as F5                  # noqa: E402

G_LIST = (0., 0.1, 0.5, 1., 2., 5., 20., 1e3)
OUTF = FC.OUT / 'F_ROOM_MECHANISM_T1_train_v01.json'


def main():
    if OUTF.exists():
        raise SystemExit('REFUSED: %s exists' % OUTF)
    FC.require_split('train')
    names = sorted(FC.splits()['train'])
    keys = ('cF0', 'cE', 'clear', 'idx55', 'vbar', 'sweep', 'clear_logged')
    cols = {k: [] for k in keys}; scene = []
    for nm in names:
        z = np.load(FC.CACHE / 'arrays_T1' / 'train' / (nm + '.npz'), allow_pickle=False)
        ev = z['evaluated'].astype(bool)
        for k in keys:
            cols[k].append(z[k][ev])
        scene += [nm] * int(ev.sum())
    C = {k: np.concatenate(v) for k, v in cols.items()}
    scene = np.array(scene)
    n = C['clear'].shape[0]; ar = np.arange(n)
    safe = C['clear'] > 0
    doc = dict(code='f14_room_mechanism_v01.py', split='train (design)', tracker='T1', horizon_s=3, n_evaluated=int(n),
               share_any_safe_row=float(safe.any(1).mean()), share_row0_safe=float(safe[:, 0].mean()),
               share_fallback_row_safe=float(safe[ar, C['idx55']].mean()), share_logged_motion_safe=float((C['clear_logged'] > 0).mean()),
               share_rows_neginf=dict(F0=float(np.isneginf(C['cF0']).mean()), E=float(np.isneginf(C['cE']).mean())),
               share_decisions_all_rows_neginf=dict(F0=float(np.isneginf(C['cF0']).all(1).mean()),
                                                     E=float(np.isneginf(C['cE']).all(1).mean())),
               by_scale=[])
    for g in G_LIST:
        for src in ('F0', 'E'):
            feas = C['c' + src] >= g; anyf = feas.any(1)
            sel = np.where(anyf, feas.argmax(1), C['idx55'])
            fb = sel == C['idx55']; wg = ~safe[ar, sel]
            doc['by_scale'].append(dict(g=g, source=src, share_fallback=float(fb.mean()), share_wrong_go=float(wg.mean()),
                                        wrong_go_among_fallback=float(wg[fb].mean()) if fb.any() else None,
                                        wrong_go_among_other=float(wg[~fb].mean()) if (~fb).any() else None,
                                        mean_vbar_selected=float(C['vbar'][ar, sel].mean())))
    # Part 2
    feas = C['cF0'] >= 1.; anyf = feas.any(1)
    sel = np.where(anyf, feas.argmax(1), C['idx55'])
    cand = np.nonzero((sel == C['idx55']) & ~safe[ar, sel])[0]
    pick = np.sort(np.random.default_rng(1).choice(cand, size=min(300, cand.size), replace=False))
    consumer, finite_primitive = F5.planner_mods()
    res = []; cur = None; sc = None
    for i in pick:
        if scene[i] != cur:
            cur = scene[i]; sc = AD.Scene(np.load(FC.CACHE / 'train' / (cur + '.npz'), allow_pickle=False))
        j = int(C['sweep'][i]); now = float(sc.sw_t[j])
        s_e = sc.project(sc.ego_c[j:j + 1])[0][0]
        ids, tc, ty, hl, hw = F5.truth_planner(sc, now, s_e, 61)
        rows = finite_primitive.build_library(max(0., float(sc.v[j])), float(sc.a[j]), sc.desired, [], AD.EGO_L, AD.EGO_W, now,
                                              consumer.Diagnostics())
        S = np.stack([r['s'] for r in rows])[int(C['idx55'][i])]
        first = None
        for f in range(61):
            ok = np.isfinite(tc[:, f, 0])
            if not ok.any():
                continue
            E = AD.rect_corners(S[f], 0., 0., AD.EGO_L / 2., AD.EGO_W / 2.)
            A = AD.rect_corners(tc[ok, f, 0], tc[ok, f, 1], ty[ok, f], hl[ok], hw[ok])
            d = AD.poly_dist(np.broadcast_to(E, A.shape), A)
            if (d <= 0).any():
                k = np.nonzero(ok)[0][int(np.argmin(d))]
                first = dict(scene=str(cur), sweep=j, frame=f, cls=str(sc.t_cls[ids[k]]), x0=float(tc[k, 0, 0]),
                             x_rel_contact=float(tc[k, f, 0] - S[f]), y_rel_contact=float(tc[k, f, 1]), ego_v=float(sc.v[j]))
                break
        res.append(first)
    ok = [r for r in res if r]
    doc['fallback_contacts'] = dict(
        rule="F0 at g = 1: selections equal to the fallback row with true clearance <= 0", n_candidates=int(cand.size),
        n_sampled=int(pick.size), sample_draw='default_rng(1).choice(candidates, 300, replace=False) (diagnostic draw)',
        n_contact_found=len(ok), share_actor_behind_at_now=float(np.mean([r['x0'] < 0 for r in ok])),
        share_actor_behind_at_contact=float(np.mean([r['x_rel_contact'] < 0 for r in ok])),
        share_lateral_beyond_ego_half_width=float(np.mean([abs(r['y_rel_contact']) > AD.EGO_W / 2. for r in ok])),
        classes=Counter(r['cls'] for r in ok).most_common(),
        contact_frame_quantiles=[float(x) for x in np.quantile([r['frame'] for r in ok], [0, .25, .5, .75, 1])],
        logged_ego_speed_quantiles=[float(x) for x in np.quantile([r['ego_v'] for r in ok], [0, .25, .5, .75, 1])],
        cases=ok)
    doc['written'] = FC.clock()
    OUTF.write_text(FC.jdump(doc), encoding='utf-8')
    print('WROTE', OUTF)


if __name__ == '__main__':
    main()
