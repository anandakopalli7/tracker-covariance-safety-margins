"""Revision v13, AMENDMENT_12 sec. 5 v02: the train design numbers of the v02 primary from the rows f21_mech_v01 already built on all
700 train scenes (CANMOT), without re-tracking or re-matching. New file, 22 Nov 2026 (Claude Opus 5.5, session F).
It reads out\\mech\\MECH_ROWS_train_T1_v01.npz (one row per decision instance, in f21's own order: scenes ascending, rows by keyframe then
track id), rebuilds each scene's row tuples and calls f21_mech_v02's own scene_terms / boot. Check: the v01 all-row tau recomputed from
the rows must equal MECH_train_T1_v01.json's tau exactly, else it refuses. Output out\\mech\\MECH_train_T1_v02_fromrows.json: the v02
primary (point, 95% percentile interval, bootstrap SD, one-sided p, power for val at the train value as f21), the all-row statistic,
and the strata. No calibration (train).
Usage: python -I f21_design_from_rows_v02.py
"""
import json, math, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import f21_mech_v02 as M          # noqa: E402

OUT = HERE.parent / 'out' / 'mech'


def main():
    outf = OUT / 'MECH_train_T1_v02_fromrows.json'
    if outf.exists(): raise SystemExit('REFUSED: %s exists' % outf)
    z = np.load(OUT / 'MECH_ROWS_train_T1_v01.npz', allow_pickle=False)
    v01 = json.loads((OUT / 'MECH_train_T1_v01.json').read_text(encoding='utf-8'))
    sc = z['scene']; scenes = sorted(set(sc.tolist()))
    assert len(scenes) == v01['n_scenes']
    cols = [z[k] for k in ('kf', 'track_id', 'inst', 'cls', 's_h', 'e_h', 'age', 'dt', 'stratum')]
    rows = {s: [] for s in scenes}
    for i in range(sc.size):
        rows[sc[i]].append(tuple(c[i].item() if hasattr(c[i], 'item') else c[i] for c in cols))
    AB = {w: np.array([M.scene_terms(rows[s], w) for s in scenes]) for w in ('miss', 'primary', 'steady', 'in_miss', 'post_miss', 'young')}
    A0, B0 = AB['primary'][:, 0], AB['primary'][:, 1]
    tau0 = float(A0.sum() / B0.sum())
    if tau0 != v01['tau']: raise SystemExit('REFUSED: the all-row tau from the rows %r differs from v01 %r' % (tau0, v01['tau']))
    A, B = AB['miss'][:, 0], AB['miss'][:, 1]
    tau = float(A.sum() / B.sum()); bt = M.boot(A, B); bt0 = M.boot(A0, B0)
    sd = float(np.nanstd(bt, ddof=1)); se_val = sd * math.sqrt(len(scenes) / 150.)
    z_ = tau / se_val - 1.959964
    doc = dict(code='f21_design_from_rows_v02.py (f21_mech_v02 scene_terms / boot)', source='out\\mech\\MECH_ROWS_train_T1_v01.npz',
               split='train', tracker='T1', n_scenes=len(scenes), n_rows=v01['n_rows'],
               primary='v02: within-cell tau_b over pairs with >= 1 member in-miss or post-miss (age >= 1.0 s rows)',
               tau=tau, tau_ci95=[float(x) for x in np.nanpercentile(bt, [2.5, 97.5])], tau_boot_sd=sd,
               p_one_sided=float((1 + np.sum(bt <= 0)) / (bt.size + 1)),
               power_for_val_150=dict(assumed_tau=tau, se_val=se_val, power_one_sided_95=float(0.5 * (1 + math.erf(z_ / math.sqrt(2))))),
               all_rows=dict(tau=tau0, ci95=[float(x) for x in np.nanpercentile(bt0, [2.5, 97.5])],
                             p_one_sided=float((1 + np.sum(bt0 <= 0)) / (bt0.size + 1)), equals_v01=True),
               strata={w: float(AB[w][:, 0].sum() / AB[w][:, 1].sum()) for w in ('steady', 'in_miss', 'post_miss', 'young')},
               share_of_primary_pairs_weight=float(B.sum() / B0.sum()),
               written=time.strftime('%Y-%m-%d %H:%M:%S'))
    outf.write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(json.dumps({k: doc[k] for k in ('tau', 'tau_ci95', 'tau_boot_sd', 'p_one_sided', 'power_for_val_150', 'all_rows', 'strata',
                                         'share_of_primary_pairs_weight')}, indent=0))


if __name__ == '__main__':
    main()
