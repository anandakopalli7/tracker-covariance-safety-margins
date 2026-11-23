"""X (A11 sec. 3.2): runs CAPTURED_AND_REVIEWED on a retry (A10 sec. 5.1) carry the worker's attempt suffix in their run id
(pc13x_<case>_native__p1 after a pre-launch failure, __r1 for the second attempt). The X programs read arrays_x\\CV0\\<job id>.npz with
meta.run_id == job id. This tool writes, for each analysed job id without arrays, an alias arrays_x\\CV0\\<job id>.npz from the unique
suffixed run of that job whose archive receipt is CAPTURED_AND_REVIEWED: every array byte-identical (np.array_equal, dtype and shape
equal); only meta changes (run_id := job id, capture_run_id := the suffixed run id, alias_of := its SHA-256). Data step, no value computed.
New file, 21 Nov 2026 (Claude Opus 5.5, session CD). Record: crossing\\out\\ALIAS_RETRIES_X_v13.json (never overwritten).
Usage: python -I -B alias_retries_x_v13.py --cases-sha SHA [--dry-run]
"""
import argparse, hashlib, json, pathlib
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
ARR = CD / 'arrays_x' / 'CV0'


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--cases-sha', required=True); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    cf = HERE / 'CASES_X_PC_v13.json'
    if sha(cf) != a.cases_sha: raise SystemExit('REFUSED: CASES_X_PC_v13.json differs')
    X = json.loads(cf.read_text(encoding='utf-8'))
    rep = json.loads((HERE / 'REPLACEMENTS_X_v13.json').read_text(encoding='utf-8'))['replacements']
    jobs = ['pc13x_%s_native' % rep.get(r['case'], r['case']) for r in X['cases'] if not r['reserve']]
    out = HERE / 'out' / 'ALIAS_RETRIES_X_v13.json'
    if out.exists() and not a.dry_run: raise SystemExit('REFUSED: %s exists' % out.name)
    rec = []
    for j in jobs:
        if (ARR / (j + '.npz')).is_file(): continue
        cands = []
        for p in sorted(ARR.glob(j + '__*.npz')):
            rid = p.stem
            rc = CD / 'archives' / rid / f'claude_main_{rid}.tar.gz.receipt.json'
            ok = CD / 'archives' / rid / 'DOWNLOAD_OK.json'
            if rc.is_file() and ok.is_file() and json.loads(rc.read_text(encoding='utf-8')).get('status') == 'CAPTURED_AND_REVIEWED':
                cands.append((p, rid, rc))
        if len(cands) != 1: raise SystemExit('REFUSED: %s has %d captured retried runs' % (j, len(cands)))
        p, rid, rc = cands[0]
        z = np.load(p, allow_pickle=False); meta = json.loads(str(z['meta']))
        assert meta['run_id'] == rid and meta['family'] == 'pedestrian_crossing'
        arrs = {k: z[k] for k in z.files if k != 'meta'}
        meta2 = dict(meta, run_id=j, capture_run_id=rid, alias_of=sha(p), alias_tool='alias_retries_x_v13.py')
        dst = ARR / (j + '.npz')
        if not a.dry_run:
            tmp = dst.with_suffix('.partial.npz')
            np.savez_compressed(tmp, meta=json.dumps(meta2, default=float), **arrs); tmp.replace(dst)
            z2 = np.load(dst, allow_pickle=False)
            assert set(z2.files) == set(z.files)
            for k in arrs:
                assert z2[k].dtype == arrs[k].dtype and z2[k].shape == arrs[k].shape and np.array_equal(z2[k], arrs[k], equal_nan=arrs[k].dtype.kind == 'f'), k
        rec.append(dict(job=j, capture_run_id=rid, source=p.name, source_sha256=sha(p), receipt_sha256=sha(rc),
                        alias=dst.name, alias_sha256=(sha(dst) if not a.dry_run else None), arrays_identical=True, n_keys=len(arrs)))
        print(j, '<-', rid)
    if not a.dry_run:
        out.write_text(json.dumps(dict(schema='ALIAS_RETRIES_X_V13', tool_sha256=sha(__file__), cases_sha256=a.cases_sha,
                                       statement=('Three study runs CAPTURED_AND_REVIEWED on an allowed retry (A10 sec. 5.1) carry the worker\'s '
                                                  'suffixed run id (__p1 after a pre-launch failure, __r1 for the second attempt). Their arrays '
                                                  'were aliased to the job id: every numeric array is byte-identical (np.array_equal, dtype and '
                                                  'shape checked on every key); only meta changed (run_id := job id; capture_run_id := the '
                                                  'suffixed id; alias_of := the source file SHA-256), so both frozen programs read all 390 runs. '
                                                  'Approved by the coordinator, 21 Nov 2026 about 17:05 EST.'),
                                       replacements_sha256=sha(HERE / 'REPLACEMENTS_X_v13.json'), aliases=rec), indent=1), encoding='utf-8')
        print(out.name, sha(out))
    print('analysed jobs', len(jobs), 'aliases', len(rec))


if __name__ == '__main__':
    main()
