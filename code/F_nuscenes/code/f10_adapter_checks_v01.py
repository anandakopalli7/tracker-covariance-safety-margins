"""Package F (revision v13): the adapter checks on the design split (A10 section 8.6 allows the train scenes for the adapter checks,
the class averages and the horizon rule only). New file, 19 Nov 2026 (Claude Opus 5.5). Aggregates the train arrays of a tracker;
computes no share, frontier or room.
  * counts: scenes, built decisions, decisions excluded by the planner's speed domain, evaluated (3 s / 2 s), in-path share;
  * identity sample against the planner library (f05 meta): max relative difference of critical scales, +-inf pattern
    differences, max |d| difference, projection (KNN vs all segments), pruned vs brute-force clearance;
  * logged-motion check: the ego's own logged motion along the route must not touch a truth box (the real car did not collide);
    share of evaluated decisions with clear_logged <= 0 (3 s and 2 s), and the scenes where it happens;
  * route fit: |l_ego| (lateral offset of the ego centre from its own route) quantiles;
  * desired speeds and ego speeds (quantiles).
Writes out\\F_ADAPTER_CHECKS_<tracker>_train_v01.json.
Usage: python -I f10_adapter_checks_v01.py <tracker>
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json                                  # noqa: E402
import numpy as np                           # noqa: E402


def q(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    return [float(v) for v in np.quantile(x, [0, .01, .5, .99, 1])] if x.size else None


def main():
    tracker = sys.argv[1]
    FC.require_split('train')
    names = sorted(FC.splits()['train'])
    agg = dict(n_scenes=0, n_dec=0, n_excluded_speed=0, n_eval=0, n_eval2=0, n_inpath_eval=0)
    idc = dict(n=0, crit_pattern_differ=0, crit_max_rel=0., d_max_abs=0., proj_max_abs=0., lib_errors=0, clear_max_abs=0.,
               clear_inf_differ=0)
    bad3 = []; bad2 = []; lego = []; des = []; v0 = []; nlog3 = 0; nlog2 = 0; missing = []
    for nm in names:
        p = FC.CACHE / ('arrays_' + tracker) / 'train' / (nm + '.npz')
        if not p.exists():
            missing.append(nm); continue
        z = np.load(p, allow_pickle=False); m = json.loads(str(z['meta']))
        agg['n_scenes'] += 1; agg['n_dec'] += m['n_dec']; agg['n_excluded_speed'] += m['n_excluded_speed']
        for k in idc:
            if k in m['identity']:
                v = m['identity'][k]
                idc[k] = max(idc[k], v) if k.endswith('max_rel') or k.endswith('max_abs') else idc[k] + v
        if m['n_dec'] == 0:
            continue
        ev = z['evaluated'].astype(bool); ev2 = z['evaluated2'].astype(bool)
        agg['n_eval'] += int(ev.sum()); agg['n_eval2'] += int(ev2.sum()); agg['n_inpath_eval'] += int((ev & z['inpath'].astype(bool)).sum())
        c3 = z['clear_logged'][ev]; c2 = z['clear_logged2'][ev2]
        nlog3 += int((c3 <= 0).sum()); nlog2 += int((c2 <= 0).sum())
        if (c3 <= 0).any():
            bad3.append((nm, int((c3 <= 0).sum()), int(ev.sum()), float(np.min(c3))))
        if (c2 <= 0).any():
            bad2.append((nm, int((c2 <= 0).sum())))
        lego.append(np.abs(z['l_ego'])); des.append(m['desired']); v0.append(z['v0'])
    doc = dict(code='f10_adapter_checks_v01.py', tracker=tracker, split='train', counts=agg, missing_scenes=missing, identity=idc,
               logged_motion=dict(rule='the ego\'s own logged motion has true clearance > 0 (the real car did not collide)',
                                  n_eval_clear_le0_3s=nlog3, share_3s=nlog3 / max(agg['n_eval'], 1),
                                  n_eval2_clear_le0_2s=nlog2, share_2s=nlog2 / max(agg['n_eval2'], 1),
                                  scenes_3s=sorted(bad3, key=lambda x: -x[1])[:40], n_scenes_3s=len(bad3)),
               l_ego_abs_quantiles=q(np.concatenate(lego)) if lego else None, desired_quantiles=q(des),
               v0_quantiles=q(np.concatenate(v0)) if v0 else None, written=FC.clock())
    outf = FC.OUT / ('F_ADAPTER_CHECKS_%s_train_v01.json' % tracker)
    outf.write_text(FC.jdump(doc), encoding='utf-8')
    print(json.dumps({k: doc[k] for k in ('counts', 'identity')}, indent=1))
    print('logged-motion contact share 3 s %.5f (%d decisions, %d scenes)' % (doc['logged_motion']['share_3s'], nlog3, len(bad3)))


if __name__ == '__main__':
    main()
