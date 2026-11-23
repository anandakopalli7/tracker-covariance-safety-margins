"""Seed-1 merge of a first-program calibration job (the frozen tools/calib_merge_v13.merge with SEEDS = (20261913,)) and A10 sec. 2.6's
first test: coverage at the nominal 95% (cd_common_v13.cover_two, frozen), deciding whether the second inner seed is needed (< 0.94).
Usage: python -I -B merge1_cov.py CHUNKDIR OUTDIR LABEL"""
import sys, pathlib, json, os
CD = pathlib.Path(r'ARS_TRIAL\revision_v13\work\CD_capture')
sys.dont_write_bytecode = True
sys.path[:0] = [str(CD / 'tools'), str(CD / 'analysis')]
import numpy as np
import calib_merge_v13 as M
M.SEEDS = (20261913,)
cd, od, lab = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
M.merge(cd, od, lab)
import importlib.util
spec = importlib.util.spec_from_file_location('cdc', CD / 'analysis' / 'cd_common_v13.py')
z = np.load(od / f'{lab}_20261913.npz')
# cover_two copied from cd_common_v13 (importing cd_common pulls the whole library; the function is three lines)
def cover_two(lt, le, nom):
    a = 1. - nom; ok = np.isfinite(lt)
    return ((le[ok] >= a / 2. - 1e-12) & (lt[ok] <= 1. - a / 2. + 1e-12))
meta = json.loads((od / f'{lab}.meta.json').read_text(encoding='utf-8'))
for j, nm in enumerate(meta['names']):
    lt, le = z['p_lt'][:, j], z['p_le'][:, j]; ind = cover_two(lt, le, 0.95)
    c95 = float(ind.mean()) if ind.size else float('nan')
    print(json.dumps(dict(label=lab, stat=nm, n_outer_valid=int(np.isfinite(lt).sum()), coverage95=c95, second_seed_needed=bool(np.isfinite(c95) and c95 < 0.94))))
