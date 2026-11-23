"""Package F (revision v13), step 01: per-scene caches of the nuScenes v1.0-trainval metadata and the CenterPoint results.
New file, 19 Nov 2026 (Claude Opus 5.5). Read-only on the data; writes cache\\<split>\\<scene>.npz and
logs\\f01_prepare_<split>_v01.json. Computes no analysis value: it copies fields, keeps LIDAR_TOP sample_data and their ego
poses, links annotations to keyframes, and checks token coverage.

Gate: require_split(split) first (val is refused until LOCK_A10_2.txt exists).
Per scene (arrays; times in s relative to the scene's first keyframe; global frame as in nuScenes):
  sw_t, sw_key, sw_kf (keyframe index of a keyframe sweep, else -1), ego_xyz (n,3), ego_q (n,4 wxyz)    LIDAR_TOP, 20 Hz
  kf_t, kf_token                                                                                         keyframes, 2 Hz
  ann_kf, ann_inst (instance index in the scene), ann_cat (nuScenes category name), ann_xyz, ann_wlh, ann_q, ann_nlidar,
  ann_nradar, ann_vis, ann_next (row of the instance's next annotation, -1 if none)                      all annotations
  det_kf, det_xyz, det_wlh, det_q, det_vel, det_score, det_name, det_attr                               results, file order
Usage: python -I f01_prepare_v01.py train|val
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402  (before numpy)
import json, time                            # noqa: E402
import numpy as np                           # noqa: E402


def stream_array(path, keep=None):
    """Elements of a top-level JSON array, decoded one at a time (the text is read once); keep(rec) -> rec or None."""
    s = pathlib.Path(path).read_text(encoding='utf-8')
    dec = json.JSONDecoder(); i = s.index('[') + 1; n = len(s); out = []
    while True:
        while i < n and s[i] in ' \t\r\n,':
            i += 1
        if i >= n or s[i] == ']':
            break
        rec, i = dec.raw_decode(s, i)
        r = keep(rec) if keep else rec
        if r is not None:
            out.append(r)
    del s
    return out


def stream_results(path, wanted):
    """{sample_token: list of detection dicts} for the tokens in `wanted`; also returns all tokens seen and the meta block."""
    s = pathlib.Path(path).read_text(encoding='utf-8')
    dec = json.JSONDecoder()
    i = s.index('{', s.index('"results"') + 9) + 1; n = len(s)
    out = {}; seen = []
    while True:
        while i < n and s[i] in ' \t\r\n,':
            i += 1
        if s[i] == '}':
            i += 1; break
        key, i = dec.raw_decode(s, i)
        while s[i] in ' \t\r\n:':
            i += 1
        lst, i = dec.raw_decode(s, i)
        seen.append(key)
        if key in wanted:
            out[key] = lst
    j = s.index('"meta"', i)
    while s[j] != '{':
        j += 1
    meta, _ = dec.raw_decode(s, j)
    del s
    return out, seen, meta


def main():
    split = sys.argv[1]
    FC.require_split(split)
    t00 = time.time()
    names = FC.splits()[split]
    outdir = FC.CACHE / split
    outdir.mkdir(parents=True, exist_ok=True)
    M = FC.META
    scenes = {r['name']: r for r in json.loads((M / 'scene.json').read_text(encoding='utf-8'))}
    logs = {r['token']: r for r in json.loads((M / 'log.json').read_text(encoding='utf-8'))}
    samples = {r['token']: r for r in json.loads((M / 'sample.json').read_text(encoding='utf-8'))}
    sensors = {r['token']: r for r in json.loads((M / 'sensor.json').read_text(encoding='utf-8'))}
    calib = {r['token']: r for r in json.loads((M / 'calibrated_sensor.json').read_text(encoding='utf-8'))}
    lidar_cs = {t for t, r in calib.items() if sensors[r['sensor_token']]['channel'] == 'LIDAR_TOP'}
    want_scenes = {scenes[nm]['token'] for nm in names}
    want_samples = {t for t, r in samples.items() if r['scene_token'] in want_scenes}
    print(FC.clock(), split, len(names), 'scenes', len(want_samples), 'samples', flush=True)

    sd = stream_array(M / 'sample_data.json',
                      lambda r: (r['token'], r['sample_token'], r['ego_pose_token'], r['timestamp'], r['is_key_frame'])
                      if (r['calibrated_sensor_token'] in lidar_cs and r['sample_token'] in want_samples) else None)
    print(FC.clock(), 'LIDAR_TOP sample_data', len(sd), flush=True)
    need_pose = {x[2] for x in sd}
    poses = {r[0]: r[1:] for r in stream_array(M / 'ego_pose.json',
                                               lambda r: (r['token'], r['timestamp'], r['translation'], r['rotation'])
                                               if r['token'] in need_pose else None)}
    print(FC.clock(), 'ego poses', len(poses), flush=True)
    cats = {r['token']: r['name'] for r in json.loads((M / 'category.json').read_text(encoding='utf-8'))}
    inst_cat = {r['token']: cats[r['category_token']] for r in json.loads((M / 'instance.json').read_text(encoding='utf-8'))}
    ann = stream_array(M / 'sample_annotation.json',
                       lambda r: (r['token'], r['sample_token'], r['instance_token'], r['translation'], r['size'], r['rotation'],
                                  r['num_lidar_pts'], r['num_radar_pts'], int(r['visibility_token'] or 0), r['next'])
                       if r['sample_token'] in want_samples else None)
    print(FC.clock(), 'annotations', len(ann), flush=True)
    dets, seen, rmeta = stream_results(FC.RESULT_FILES[split], want_samples)
    print(FC.clock(), 'result tokens', len(seen), 'wanted found', len(dets), flush=True)

    sd_by_sample = {}
    for x in sd:
        sd_by_sample.setdefault(x[1], []).append(x)
    ann_by_sample = {}
    for a in ann:
        ann_by_sample.setdefault(a[1], []).append(a)
    rec = dict(split=split, n_scenes=len(names), started=time.strftime('%Y-%m-%d %H:%M:%S'),
               results_file=str(FC.RESULT_FILES[split]), results_meta=rmeta, results_tokens=len(seen),
               results_tokens_not_in_split=len(set(seen) - want_samples), split_samples_without_results=len(want_samples - set(dets)),
               results_duplicate_tokens=len(seen) - len(set(seen)), scenes={})
    for nm in names:
        sc = scenes[nm]
        kf_tokens = []; t = sc['first_sample_token']
        while t:
            kf_tokens.append(t); t = samples[t]['next']
        if len(kf_tokens) != sc['nbr_samples'] or kf_tokens[-1] != sc['last_sample_token']:
            raise RuntimeError('keyframe chain of %s is broken' % nm)
        t0 = samples[kf_tokens[0]]['timestamp']
        kf_t = np.array([(samples[t]['timestamp'] - t0) * 1e-6 for t in kf_tokens])
        kf_index = {t: i for i, t in enumerate(kf_tokens)}
        sws = sorted((x for t in kf_tokens for x in sd_by_sample.get(t, [])), key=lambda x: x[3])
        sw_t = np.array([(x[3] - t0) * 1e-6 for x in sws])
        sw_key = np.array([bool(x[4]) for x in sws])
        sw_kf = np.array([kf_index[x[1]] if x[4] else -1 for x in sws], int)
        ego_xyz = np.array([poses[x[2]][1] for x in sws], float); ego_q = np.array([poses[x[2]][2] for x in sws], float)
        pose_dt = max(abs(poses[x[2]][0] - x[3]) for x in sws)
        kfs = sw_kf[sw_kf >= 0]
        if not np.array_equal(kfs, np.arange(len(kf_tokens))):
            raise RuntimeError('%s: keyframe sweeps %s do not match the keyframes' % (nm, kfs[:5]))
        # annotations
        A = [a for t in kf_tokens for a in ann_by_sample.get(t, [])]
        tok_row = {a[0]: i for i, a in enumerate(A)}
        inst_ids = {}
        ann_inst = np.array([inst_ids.setdefault(a[2], len(inst_ids)) for a in A], int)
        arr = dict(
            sw_t=sw_t, sw_key=sw_key, sw_kf=sw_kf, ego_xyz=ego_xyz, ego_q=ego_q, kf_t=kf_t, kf_token=np.array(kf_tokens, dtype='U32'),
            ann_kf=np.array([kf_index[a[1]] for a in A], int), ann_inst=ann_inst,
            ann_inst_token=np.array(list(inst_ids), dtype='U32'), ann_cat=np.array([inst_cat[a[2]] for a in A], dtype='U48'),
            ann_xyz=np.array([a[3] for a in A], float).reshape(-1, 3), ann_wlh=np.array([a[4] for a in A], float).reshape(-1, 3),
            ann_q=np.array([a[5] for a in A], float).reshape(-1, 4), ann_nlidar=np.array([a[6] for a in A], int),
            ann_nradar=np.array([a[7] for a in A], int), ann_vis=np.array([a[8] for a in A], int),
            ann_next=np.array([tok_row.get(a[9], -1) if a[9] else -1 for a in A], int))
        D = [(kf_index[t], d) for t in kf_tokens for d in dets.get(t, [])]
        for _, d in D:
            if d['sample_token'] not in kf_index:
                raise RuntimeError('detection with a foreign sample token in %s' % nm)
        arr.update(det_kf=np.array([k for k, _ in D], int), det_xyz=np.array([d['translation'] for _, d in D], float).reshape(-1, 3),
                   det_wlh=np.array([d['size'] for _, d in D], float).reshape(-1, 3), det_q=np.array([d['rotation'] for _, d in D], float).reshape(-1, 4),
                   det_vel=np.array([d['velocity'] for _, d in D], float).reshape(-1, 2), det_score=np.array([d['detection_score'] for _, d in D], float),
                   det_name=np.array([d['detection_name'] for _, d in D], dtype='U24'), det_attr=np.array([d['attribute_name'] for _, d in D], dtype='U32'))
        meta = dict(scene=nm, token=sc['token'], split=split, location=logs[sc['log_token']]['location'], logfile=logs[sc['log_token']]['logfile'],
                    description=sc['description'], t0_us=t0, n_kf=len(kf_tokens), n_sweeps=len(sws), n_ann=len(A), n_det=len(D),
                    max_pose_minus_sweep_us=int(pose_dt), kf_without_dets=int(sum(1 for t in kf_tokens if t not in dets)))
        np.savez_compressed(outdir / (nm + '.npz'), meta=json.dumps(meta), **arr)
        rec['scenes'][nm] = meta
    rec['finished'] = time.strftime('%Y-%m-%d %H:%M:%S'); rec['seconds'] = round(time.time() - t00, 1)
    (FC.LOGS / ('f01_prepare_%s_v01.json' % split)).write_text(FC.jdump(rec), encoding='utf-8')
    print(FC.clock(), 'done', split, rec['seconds'], 's; tokens not in split', rec['results_tokens_not_in_split'],
          'split samples without results', rec['split_samples_without_results'], flush=True)


if __name__ == '__main__':
    main()
