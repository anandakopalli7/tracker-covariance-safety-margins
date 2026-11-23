"""First pass (read-only on the archives): class-mean logged covariance of the primary actor, and the checksum values.

For every assessment decision of every run, the logged actor nearest to the true primary centre (planner frame, at `now`,
gate 4 m) is taken as the primary's track. Its logged 4x4 P is accumulated by track-name class (pedestrian / vehicle).

Usage: python -I -B -X utf8 ol_pbar_v01.py <archives_root> <out_json> [checksum_run_folder] [max_runs]
"""
import json, math, pathlib, sys, collections
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import olcore_v01 as oc

root = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2])
chk = sys.argv[3] if len(sys.argv) > 3 else ''
maxn = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9

acc = {c: np.zeros((4, 4)) for c in ('vehicle', 'pedestrian')}; cnt = collections.Counter()
acc_fam = collections.defaultdict(lambda: np.zeros((4, 4))); cnt_fam = collections.Counter()
xtab = collections.Counter(); nodec = collections.Counter(); ndec = collections.Counter(); ages = []
nrun = 0
for rd in sorted(root.iterdir()):
    if not rd.is_dir():
        continue
    try:
        cap = oc.cap_dir(rd)
        fam = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))['case']['draw']['family']
        T = oc.load_truth(cap)
    except Exception as e:  # incomplete run
        print('SKIP', rd.name, repr(e)[:120], flush=True); continue
    nrun += 1
    if nrun > maxn:
        break
    first = True; n_ass = 0
    for r in oc.jl(cap / 'frames.jsonl'):
        dec = (r.get('execution') or {}).get('new_decision')
        if not dec or dec['mode'] != 'assessment':
            continue
        n_ass += 1; k = r['k']; tr = T.get(k)
        if tr is None or tr['target_id'] is None or tr['target_id'] not in tr['actors']:
            nodec[fam] += 1; continue
        ndec[fam] += 1
        now = dec['now']; actors = dec['actors']
        _, (j, dist) = oc.match_actors(actors, now, tr, [tr['target_id']])
        # ungated nearest (for the checksum statement)
        t = tr['actors'][tr['target_id']]; rx, ry = oc.to_planner(tr['ego'], t[0], t[1])
        if j < 0:
            xtab[(fam, 'unmatched')] += 1
            if rd.name == chk and first and actors:
                ds = [math.hypot(a['x'] + (now - a['state_time']) * a['vx'] - rx, a['y'] + (now - a['state_time']) * a['vy'] - ry) for a in actors]
                print('CHECKSUM note: k=%d has %d logged actors, nearest at %.3f m (outside the 4 m gate)' % (k, len(actors), min(ds)))
            continue
        a = actors[j]; P = np.asarray(a['P'], float); c = oc.cls_of(a['name'])
        acc[c] += P; cnt[c] += 1; acc_fam[(fam, c)] += P; cnt_fam[(fam, c)] += 1
        xtab[(fam, a['name'])] += 1; ages.append(now - a['state_time'])
        if rd.name == chk and first:
            first = False; age = now - a['state_time']
            print('CHECKSUM first matched assessment decision of %s' % rd.name)
            print(json.dumps(dict(k=k, n_logged_actors=len(actors), matched_index=j, name=a['name'], x=a['x'], y=a['y'], vx=a['vx'], vy=a['vy'],
                                  age=age, now=now, state_time=a['state_time'], P00=P[0, 0], P11=P[1, 1], P22=P[2, 2], P33=P[3, 3],
                                  true_x_at_now=rx, true_y_at_now=ry, match_distance_m=dist), indent=1))
    if rd.name == chk:
        print('CHECKSUM assessment decisions in %s: %d' % (rd.name, n_ass))
    print('%-36s %-20s assess=%d' % (rd.name, fam, n_ass), flush=True)

res = dict(root=str(root), runs=nrun, gate_m=oc.GATE_M, counts=dict(cnt), Pbar={c: (acc[c] / max(cnt[c], 1)).tolist() for c in acc},
           Pbar_by_family_class={'%s|%s' % k: (acc_fam[k] / cnt_fam[k]).tolist() for k in acc_fam}, counts_by_family_class={'%s|%s' % k: v for k, v in cnt_fam.items()},
           name_by_family={'%s|%s' % k: v for k, v in sorted(xtab.items())}, decisions_with_truth=dict(ndec), decisions_without_truth=dict(nodec),
           age_quantiles=dict(zip(('min', 'q10', 'q50', 'q90', 'max'), np.quantile(ages, [0, .1, .5, .9, 1]).tolist())) if ages else None)
out.write_text(json.dumps(res, indent=1), encoding='utf-8')
np.set_printoptions(precision=5, suppress=True, linewidth=160)
for c in acc:
    print('Pbar', c, 'n=%d' % cnt[c]); print(acc[c] / max(cnt[c], 1))
print('track name of the matched primary, by family:'); [print('  ', k, v) for k, v in sorted(xtab.items())]
print('age quantiles', res['age_quantiles'])
print('WROTE', out)
