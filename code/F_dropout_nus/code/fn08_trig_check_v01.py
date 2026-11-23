"""AMENDMENT_12 sec. 5b, acceptance 1, cause of the last-bit differences between the pod's accept tracks and F's laptop tracks.
New file, 22 Nov 2026 (Claude Opus 5.5, worker of package F). A few keyframes only (a check, not a re-tracking): the first K
keyframes of one scene through fn02's T1 path on this laptop,
  plain   (the laptop's own math library, as F ran it): the rows of keyframes < K must equal F's tracks bit for bit;
  exact   (session B's trk_exact_math_v01.install(): correctly rounded sin / cos / atan2 on the tracker path, the switch the
          project uses to reproduce Linux pod logs on Windows): the rows must equal the pod's accept tracks bit for bit.
If both hold, the differences come from the Windows math library's trig, not from the copied code.
Usage: python -I -B fn08_trig_check_v01.py plain|exact SCENE K
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fn_common_v01 as FC                   # noqa: E402  (before numpy)
import json                                  # noqa: E402
import numpy as np                           # noqa: E402
import fn02_track_v01 as T                   # noqa: E402

KEYS = ('trk_kf', 'trk_id', 'trk_name', 'trk_center', 'trk_size', 'trk_yaw', 'trk_vel', 'trk_P', 'trk_state_time', 'trk_score')


def main():
    how, scene, K = sys.argv[1], sys.argv[2], int(sys.argv[3])
    FC.require_split('val')
    z = np.load(FC.SRC_CACHE / 'val' / (scene + '.npz'), allow_pickle=False)
    trk = T.make_tracker(FC.PUNISH_RECORD)
    if how == 'exact':
        sys.path.insert(0, str(FC.WORK / 'shared' / 'trackers'))
        import trk_exact_math_v01 as X
        X.install()
    rows = []
    for kf in range(K):
        for r in trk.step(T.det_dicts(z, kf, str(z['kf_token'][kf])), float(z['kf_t'][kf])):
            rows.append((kf, r))
    n = len(rows)
    mine = dict(trk_kf=np.array([k for k, _ in rows], int), trk_id=np.array([r['id'] for _, r in rows], int),
                trk_name=np.array([r['name'] for _, r in rows], dtype='U24'),
                trk_center=np.array([r['center'] for _, r in rows], float).reshape(n, 3),
                trk_size=np.array([r['size'] for _, r in rows], float).reshape(n, 3),
                trk_yaw=np.array([r['yaw'] for _, r in rows], float),
                trk_vel=np.array([r['velocity'] for _, r in rows], float).reshape(n, 2),
                trk_P=np.array([r['P9'] for _, r in rows], float).reshape(n, 9, 9),
                trk_state_time=np.array([r['state_time'] for _, r in rows], float),
                trk_score=np.array([r['score'] for _, r in rows], float))
    res = dict(scene=scene, K=K, how=how, n_rows=n)
    for label, path in (('F_laptop', FC.SRC_CACHE / 'tracks_T1' / 'val' / (scene + '.npz')),
                        ('pod_accept', FC.CACHE / 'tracks_accept' / 'val' / (scene + '.npz'))):
        ref = np.load(path, allow_pickle=False)
        m = ref['trk_kf'] < K
        same = {k: bool(np.array_equal(ref[k][m], mine[k])) for k in KEYS}
        dif = {}
        for k in KEYS:
            if not same[k] and ref[k].dtype.kind == 'f' and ref[k][m].shape == mine[k].shape:
                x, y = ref[k][m], mine[k]
                dif[k] = dict(elements_differ=int((x != y).sum()), of=int(x.size), max_abs=float(np.abs(x - y).max()),
                              rows_differ=int(np.any((x != y).reshape(x.shape[0], -1), axis=1).sum()))
        res[label] = dict(bit_identical=all(same.values()), differing_keys=[k for k, v in same.items() if not v], differences=dif)
    if how == 'exact':
        res['trig_calls'] = X.calls()
    print(json.dumps(res))


if __name__ == '__main__':
    main()
