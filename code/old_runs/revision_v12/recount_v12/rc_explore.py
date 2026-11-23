import sys, json, numpy as np
sys.path.insert(0, r'ARS_TRIAL\revision_v11\analysis')
import rev_common_v01 as C
runs = C.load_runs()
r = runs[0]
print(r.keys())
print({k: v.shape for k, v in r['crit'].items()}, r['clear1'].shape, r['vbar'].shape, r['idx55'].shape)
tot = np.zeros(6, int)
for r in runs:
    tot += np.array([m.sum() for m in r['masks']])
print('pop sizes', tot)
print('ph values', np.unique(np.concatenate([r['ph'] for r in runs]), return_counts=True))
print('ph on ev', np.unique(np.concatenate([r['ph'][r['ev']] for r in runs]), return_counts=True))
z = np.load(r'ARS_TRIAL\revision_v12\analysis\out\lead\p1b_fit_finite_0005.npz', allow_pickle=False)
for k in z.files: print('lead', k, z[k].shape, z[k].dtype, z[k][:5] if z[k].ndim==1 else '')
z = np.load(r'ARS_TRIAL\revision_v12\analysis\out\tg\p1b_fit_finite_0005.npz', allow_pickle=False)
for k in z.files: print('tg', k, z[k].shape, z[k].dtype)
z = np.load(r'ARS_TRIAL\revision_v11\analysis\out\ext\p1b_fit_finite_0005.npz', allow_pickle=False)
for k in z.files: print('ext', k, z[k].shape, z[k].dtype)
z = np.load(r'<library folder>\p2_c1109_tune_0000_fixed_c1.npz', allow_pickle=False)
for k in z.files: print('a4dry', k, z[k].shape, z[k].dtype)
print(str(z['meta'])[:2000])
