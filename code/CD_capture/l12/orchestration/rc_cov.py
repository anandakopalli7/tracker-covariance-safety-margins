"""Seed-1 coverage at nominal 95% from a recount's chunk files (p_lt, p_le per outer sample and statistic), with A10 sec. 2.6's rule
(cover_two, as cd_common_v13): tells whether the recount will need the second inner seed. Usage: python rc_cov.py CHUNKDIR LABEL"""
import sys, pathlib, re, json
import numpy as np
cd, lab = pathlib.Path(sys.argv[1]), sys.argv[2]
pat = re.compile(rf'^{re.escape(lab)}_20261913_o(\d+)_(\d+)\.npz$')
ch = sorted((int(m.group(1)), int(m.group(2)), p) for p in cd.iterdir() if (m := pat.match(p.name)))
pos = 0; lt = []; le = []
for lo, hi, p in ch:
    assert lo == pos, (lo, pos); z = np.load(p); lt.append(z['p_lt']); le.append(z['p_le']); pos = hi
assert pos == 2000, pos
lt = np.concatenate(lt); le = np.concatenate(le)
for j in range(lt.shape[1]):
    a = 0.05; ok = np.isfinite(lt[:, j]); ind = (le[ok, j] >= a / 2 - 1e-12) & (lt[ok, j] <= 1 - a / 2 + 1e-12)
    c = float(ind.mean()) if ind.size else float('nan')
    print(json.dumps(dict(label=lab, stat_index=j, n_outer_valid=int(ok.sum()), coverage95=c, second_seed_needed=bool(np.isfinite(c) and c < 0.94))))
