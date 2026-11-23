"""Duplicate-chunk check for Y-L12 seed 1 (coordinator, 04:58: "calib_merge refuses any two copies of the same (label, seed, outer range) that
disagree ... record each duplicate's agreement in the merge log"). For POD: every chunk file on the pod whose name is already on the laptop
(pods/yl12_chunks) is compared with the laptop copy: byte-identical (SHA-256), else downloaded to pods/yl12_chunks_dup/<pod>/ and compared
array by array (same keys, dtype, shape, np.array_equal with NaN equal). Appends one row per duplicate to pods/yl12_chunks/DUPCHECK_L12.jsonl;
exits non-zero if any copy disagrees. Usage: python dupcheck_l12.py POD [POD ...]"""
import sys, pathlib, json, time, hashlib
import numpy as np
CD = pathlib.Path(r'ARS_TRIAL\revision_v13\work\CD_capture')
sys.path[:0] = [str(CD / 'ycheck'), str(CD / 'tools')]
import calib_capture_pods_v13 as CP
DEST = CD / 'pods' / 'yl12_chunks'; LOG = DEST / 'DUPCHECK_L12.jsonl'
PROV = {'seconds', 'seconds_first_outer', 'versions'}     # provenance of the run (time taken, pod kernel string): recorded, not compared
RULE = ('results compared bit for bit: every key but seconds, seconds_first_outer, versions (identity keys label, seed, lo, hi, n_outer, '
        'n_inner, job_sha256, threads and the result arrays p_lt, p_le, p_lt_any, p_le_any, outer_est, n_inner_valid); provenance keys recorded')
bad_any = False
for pod in sys.argv[1:]:
    lst = CP.ssh(pod, 'cd /opt/calib/jobs && for f in *_o*_*.npz; do [ -f "$f" ] && sha256sum "$f"; done; true').strip().splitlines()
    remote = {l.split()[1]: l.split()[0] for l in lst if l.strip()}
    n = dict(pod=pod, remote=len(remote), dup=0, identical_bytes=0, equal_results=0, disagree=0)
    for f, h in sorted(remote.items()):
        loc = DEST / f
        if not loc.exists(): continue
        hl = CP.sha(loc)
        if hl == h:
            row = dict(chunk=f, pod=pod, laptop_sha256=hl, pod_sha256=h, result='identical bytes'); n['identical_bytes'] += 1
        else:
            dd = CD / 'pods' / 'yl12_chunks_dup' / pod; dd.mkdir(parents=True, exist_ok=True)
            r = CP.pv.sftp(pod, ['get "/opt/calib/jobs/%s" "%s"' % (f, dd / f)])
            if r.returncode != 0 or CP.sha(dd / f) != h: raise SystemExit('%s: download of duplicate %s failed' % (pod, f))
            a = np.load(loc, allow_pickle=False); b = np.load(dd / f, allow_pickle=False)
            eq = lambda k: a[k].dtype == b[k].dtype and a[k].shape == b[k].shape and np.array_equal(a[k], b[k], equal_nan=a[k].dtype.kind in 'fc')
            res_keys = sorted(set(a.files) - PROV)
            same = set(a.files) == set(b.files) and all(eq(k) for k in res_keys)
            row = dict(chunk=f, pod=pod, laptop_sha256=hl, pod_sha256=h, result_keys=res_keys, result='equal results' if same else 'DISAGREE',
                       provenance_differs=sorted(k for k in PROV & set(a.files) & set(b.files) if not eq(k)), rule=RULE)
            n['equal_results' if same else 'disagree'] += 1; bad_any |= not same
        n['dup'] += 1; row['at'] = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG, 'a', encoding='utf-8') as fo: fo.write(json.dumps(row) + '\n')
    print(json.dumps(n))
if bad_any: raise SystemExit('DUPLICATE CHUNKS DISAGREE: see ' + str(LOG))
