"""Package F (revision v13), step 02: re-track the CenterPoint results of each scene, keyframe by keyframe (2 Hz). New
file, 19 Nov 2026 (Claude Opus 5.5).

Trackers:
  T1   CANMOT through the project's OnlineTracker (code149\\online_tracker.py, unchanged copy) with CANMOT's nuScenes
       configuration as bound by the project (lib\\tracker_config.json = 149\\contracts\\tracker_config.json, unchanged).
       One OnlineTracker per scene; detections fed in file order with state_time = the keyframe time (s from the scene's
       first keyframe). The tracker's own output (top 500 by score) is stored unchanged.
  IMM  session B's frozen B1 tracker (work\\shared\\trackers\\trk_tracker_v01.V13Tracker('B1'), its default base configuration,
       which is the same file as T1's, and its frozen constants), fed exactly as T1.
Gate: require_split per scene list (val refused until Lock 2).
Writes cache\\tracks_<tracker>\\<split>\\<scene>.npz: trk_kf, trk_id, trk_name, trk_center (n,3), trk_size (n,3; w, l, h),
trk_yaw, trk_vel (n,2), trk_P (n,9,9) global frame, trk_state_time, trk_score; meta (counts, seconds).
Usage: python -I f02_track_v01.py <tracker> <split> <nproc> [scene ...]
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402  (before numpy)
import json, multiprocessing as mp, time, traceback   # noqa: E402
import numpy as np                           # noqa: E402


def det_dicts(z, kf, token):
    m = z['det_kf'] == kf
    out = []
    for xyz, wlh, q, v, sc, nm, at in zip(z['det_xyz'][m], z['det_wlh'][m], z['det_q'][m], z['det_vel'][m], z['det_score'][m],
                                          z['det_name'][m], z['det_attr'][m]):
        out.append(dict(sample_token=token, translation=[float(x) for x in xyz], size=[float(x) for x in wlh],
                        rotation=[float(x) for x in q], velocity=[float(x) for x in v], detection_name=str(nm),
                        detection_score=float(sc), attribute_name=str(at)))
    return out


SHARED = FC.F.parent / 'shared' / 'trackers'
_LOADED = {}   # per worker process: the shared library's hashes at the moment it was imported


def shared_hashes():
    """SHA-256 of every file of session B's library that the IMM path can load (trk_*.py, the constants, the shims).
    Added 19 Nov 2026, 18:50 EST: B patched trk_filters_v01.py (fix D-B4-3) at 15:44:47 while the first IMM run's workers
    (started 15:42:22) held the old module; the meta then recorded the new file's hash. The run now records the hashes as
    imported and refuses to write a scene if any file differs from them or from the hashes at the start of the run."""
    fs = sorted(SHARED.glob('trk_*.py')) + [SHARED / 'trk_constants_v01.json'] + sorted((SHARED / 'shims_v01').rglob('*.py'))
    return {f.relative_to(SHARED).as_posix(): FC.sha256_file(f) for f in fs}


def make_tracker(name):
    if name == 'T1':
        FC.setup_tracker()
        from online_tracker import OnlineTracker
        return OnlineTracker(FC.tracker_config())
    if name == 'IMM':
        # session B's frozen B1 (work\shared\trackers, API README section 2), in its own environment (env.setup: the
        # project's 149 tree and stand-ins), default base configuration (= lib\tracker_config.json, the same file) and the
        # frozen constants trk_constants_v01.json; one tracker library per process (this process never loads the T1 path).
        # exact_trig=False: the correctly rounded sin/cos/atan2 exist only to reproduce Linux pod logs bit for bit on Windows;
        # nuScenes has no such log, and they triple the run time (measured on scene-0001: 132 s against 42 s).
        if str(SHARED) not in sys.path:
            sys.path.insert(0, str(SHARED))
        if 'IMM' not in _LOADED:
            before = shared_hashes()
        import trk_env_v01 as env
        env.setup(exact_trig=False)
        import trk_tracker_v01 as T
        if 'IMM' not in _LOADED:
            if shared_hashes() != before:
                raise RuntimeError('shared library changed while it was being imported')
            _LOADED['IMM'] = before
        return T.V13Tracker('B1', record=False)
    raise RuntimeError('unknown tracker %r' % name)


def run_scene(args):
    tracker, split, scene, start_hashes = args
    FC.require_split(split)
    out = FC.CACHE / ('tracks_' + tracker) / split / (scene + '.npz')
    if out.exists():
        return scene, 'exists'
    try:
        t0 = time.time()
        z = np.load(FC.CACHE / split / (scene + '.npz'), allow_pickle=False)
        trk = make_tracker(tracker)
        rows = []
        for kf, (tok, t) in enumerate(zip(z['kf_token'], z['kf_t'])):
            for r in trk.step(det_dicts(z, kf, str(tok)), float(t)):
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
        meta = dict(scene=scene, split=split, tracker=tracker, n_kf=int(len(z['kf_t'])), n_rows=n, seconds=round(time.time() - t0, 2))
        if tracker == 'IMM':
            now = shared_hashes()
            if not (_LOADED['IMM'] == now == start_hashes):
                raise RuntimeError('REFUSED: the shared library differs from the one imported or the one at the start of the run')
            meta['shared_sha256'] = _LOADED['IMM']
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix('.tmp.npz')
        np.savez_compressed(tmp, meta=json.dumps(meta), **arr)
        tmp.replace(out)
        return scene, 'ok %d rows %.1fs' % (n, meta['seconds'])
    except Exception as e:
        return scene, 'ERROR %r %s' % (e, traceback.format_exc()[-800:])


def main():
    tracker, split, nproc = sys.argv[1], sys.argv[2], int(sys.argv[3])
    FC.require_split(split)
    scenes = sys.argv[4:] or FC.splits()[split]
    log = FC.LOGS / ('f02_track_%s_%s_v01.log' % (tracker, split))
    start_hashes = shared_hashes() if tracker == 'IMM' else None
    if start_hashes is not None:
        with open(log, 'a', encoding='utf-8') as f:
            f.write('%s start IMM run, shared library %s\n' % (FC.clock(), json.dumps(start_hashes, sort_keys=True)))
    jobs = [(tracker, split, s, start_hashes) for s in scenes]
    with mp.Pool(nproc) as pool:
        for scene, msg in pool.imap_unordered(run_scene, jobs):
            with open(log, 'a', encoding='utf-8') as f:
                f.write('%s %s %s\n' % (FC.clock(), scene, msg))
    print(FC.clock(), 'finished', tracker, split, len(jobs), 'scenes', flush=True)


if __name__ == '__main__':
    main()
