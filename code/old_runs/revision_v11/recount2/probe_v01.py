"""Probe (read-only on the data project): what the stored files hold and how one run looks. Second program, recount2."""
import json, pathlib, sys, time
import numpy as np
P = pathlib.Path(r'<library folder>')
sys.path.insert(0, str(P / '11_ojits' / 'A5' / 'code'))
import oxsb_replan_v03 as rp                       # noqa: E402
from oxsb_replan_v03 import c3, sb, gc, rx, oc, ox, consumer, finite_primitive   # noqa: E402

run = 'p1b_fit_finite_0005'
z = np.load(c3.STORED / (run + '.npz'), allow_pickle=False)
print('stored keys', {k: z[k].shape for k in z.files if k != 'meta'})
q = np.load(P / '11_ojits' / 'A5' / 'fit' / 'main' / 'extract' / (run + '.npz'), allow_pickle=False)
print('extract keys', sorted(q.files))
pk = np.load(P / '11_ojits' / 'review' / 'optionA_recount_v01' / 'cache' / (run + '_pack.npz'), allow_pickle=False)
print('pack keys', sorted(pk.files))
mq = json.loads(str(q['meta']))
print('extract meta cpu_s', mq.get('cpu_s'), 'kmax', mq['kmax'], 'n_dec', mq['n_dec'], 'contact_k', mq['contact_k'])
print('RUNS fit', len(c3.RUNS['fit']), c3.RUNS['fit'][0], c3.RUNS['fit'][-1])
t0 = time.time()
L = rx.load_run('fit', run, sb.YAW)
print('load_run s', time.time() - t0)
T = L['T']; kmax = L['kmax']
ks = sorted(T)
print('truth frames', len(ks), ks[0], ks[-1], 'contiguous', ks == list(range(ks[0], ks[-1] + 1)))
ids = {}
for k in ks:
    for aid, a in T[k]['actors'].items():
        ids.setdefault(aid, []).append((k, a[3], a[4]))
for aid, v in ids.items():
    kk = [x[0] for x in v]
    print('actor', aid, 'frames', kk[0], kk[-1], len(kk), 'contig', kk == list(range(kk[0], kk[-1] + 1)),
          'extents', sorted(set((x[1], x[2]) for x in v)))
print('target ids', sorted(set(str(T[k]['target_id']) for k in ks)))
t0 = time.time()
decs = list(gc.decisions(L['cap']))
print('decisions', len(decs), 'evaluated', int(z['evaluated'].sum()), 's', time.time() - t0)
t0 = time.time()
k, dec = decs[len(decs) // 2]
ms = dec['model_state']
rows = finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'], dec['actors'],
                                      dec['ego_length'], dec['ego_width'], dec['now'], consumer.Diagnostics())
print('build_library s', time.time() - t0, 'row keys', sorted(rows[0].keys()))
print('s len', len(rows[0]['s']), 'v len', len(rows[0]['v']), 'a len', len(rows[0]['a']))
print('ego', T[k]['ego'], 'k', k)
