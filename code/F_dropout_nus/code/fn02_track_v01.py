"""AMENDMENT_12 sec. 5b: re-track the CenterPoint results of each nuScenes scene with T1, keyframe by keyframe (2 Hz), with or
without the injected dropouts. New file, 22 Nov 2026 (Claude Opus 5.5, worker of package F). A copy of
work\\F_nuscenes\\code\\f02_track_v01.py (frozen; unchanged there), T1 path only, with these changes only:
  mode accept  masks OFF, output.punish_num = 1 (record): must reproduce F's cache\\tracks_T1\\<split>\\<scene>.npz (acceptance 1);
               writes HOME\\cache\\tracks_accept\\<split>\\<scene>.npz.
  mode masked  the one mask law of AMENDMENT_11 sec. 6c (dr_masks_v02.mask, unchanged copy) with case id = the scene name and
               n = the scene's number of keyframes; on a masked keyframe the tracker is fed an EMPTY detection list at that keyframe's
               time (it predicts only); output.punish_num = 3. Val refused until LOCK_A12c.txt exists (fn_common.require_masked).
               Writes HOME\\cache\\tracks_masked\\<split>\\<scene>.npz with the extra key trk_masked_kf (the masked keyframes).
T1 = OnlineTracker(tracker_config) exactly as F (code149\\online_tracker.py, F's lib); detections in file order; state_time = the
keyframe time. Every array key and its construction are F's.
Usage: python -I fn02_track_v01.py accept|masked <split> <nproc> [scene ...]
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fn_common_v01 as FC                   # noqa: E402  (before numpy)
import json, multiprocessing as mp, time, traceback   # noqa: E402
import numpy as np                           # noqa: E402
import dr_masks_v02 as M                     # noqa: E402  (unchanged copy of F_dropout\code\dr_masks_v02.py)

MODES = {'accept': dict(punish=FC.PUNISH_RECORD, masks=False), 'masked': dict(punish=FC.PUNISH_5B, masks=True)}


def det_dicts(z, kf, token):
    m = z['det_kf'] == kf
    out = []
    for xyz, wlh, q, v, sc, nm, at in zip(z['det_xyz'][m], z['det_wlh'][m], z['det_q'][m], z['det_vel'][m], z['det_score'][m],
                                          z['det_name'][m], z['det_attr'][m]):
        out.append(dict(sample_token=token, translation=[float(x) for x in xyz], size=[float(x) for x in wlh],
                        rotation=[float(x) for x in q], velocity=[float(x) for x in v], detection_name=str(nm),
                        detection_score=float(sc), attribute_name=str(at)))
    return out


def make_tracker(punish):
    FC.setup_tracker()
    from online_tracker import OnlineTracker
    return OnlineTracker(FC.tracker_config(punish))


def gate(mode, split):
    if mode == 'masked':
        FC.require_masked(split)
    else:
        FC.require_split(split)


def run_scene(args):
    mode, split, scene = args
    gate(mode, split)
    cfg = MODES[mode]
    out = FC.CACHE / ('tracks_' + mode) / split / (scene + '.npz')
    if out.exists():
        return scene, 'exists'
    try:
        t0 = time.time()
        z = np.load(FC.SRC_CACHE / split / (scene + '.npz'), allow_pickle=False)
        n_kf = int(len(z['kf_t']))
        masked = M.mask(scene, n_kf) if cfg['masks'] else []
        mset = set(masked)
        trk = make_tracker(cfg['punish'])
        rows = []
        for kf, (tok, t) in enumerate(zip(z['kf_token'], z['kf_t'])):
            dets = [] if kf in mset else det_dicts(z, kf, str(tok))
            for r in trk.step(dets, float(t)):
                rows.append((kf, r))
        n = len(rows)
        arr = dict(trk_kf=np.array([k for k, _ in rows], int), trk_id=np.array([r['id'] for _, r in rows], int),
                   trk_name=np.array([r['name'] for _, r in rows], dtype='U24'),
                   trk_center=np.array([r['center'] for _, r in rows], float).reshape(n, 3),
                   trk_size=np.array([r['size'] for _, r in rows], float).reshape(n, 3),
                   trk_yaw=np.array([r['yaw'] for _, r in rows], float),
                   trk_vel=np.array([r['velocity'] for _, r in rows], float).reshape(n, 2),
                   trk_P=np.array([r['P9'] for _, r in rows], float).reshape(n, 9, 9),
                   trk_state_time=np.array([r['state_time'] for _, r in rows], float),
                   trk_score=np.array([r['score'] for _, r in rows], float))
        meta = dict(scene=scene, split=split, tracker='T1', mode=mode, punish_num=cfg['punish'], n_kf=n_kf, n_rows=n,
                    masked_kf=masked, n_masked=len(masked), seconds=round(time.time() - t0, 2))
        if cfg['masks']:
            arr['trk_masked_kf'] = np.array(masked, int)
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix('.tmp.npz')
        np.savez_compressed(tmp, meta=json.dumps(meta), **arr)
        tmp.replace(out)
        return scene, 'ok %d rows %d masked %.1fs' % (n, len(masked), meta['seconds'])
    except Exception as e:
        return scene, 'ERROR %r %s' % (e, traceback.format_exc()[-800:])


def main():
    mode, split, nproc = sys.argv[1], sys.argv[2], int(sys.argv[3])
    if mode not in MODES:
        raise SystemExit('mode?')
    gate(mode, split)
    scenes = sys.argv[4:] or FC.splits()[split]
    log = FC.LOGS / ('fn02_track_%s_%s_v01.log' % (mode, split))
    jobs = [(mode, split, s) for s in scenes]
    with mp.Pool(nproc) as pool:
        for scene, msg in pool.imap_unordered(run_scene, jobs):
            with open(log, 'a', encoding='utf-8') as f:
                f.write('%s %s %s\n' % (FC.clock(), scene, msg))
    print(FC.clock(), 'finished', mode, split, len(jobs), 'scenes', flush=True)


if __name__ == '__main__':
    main()
