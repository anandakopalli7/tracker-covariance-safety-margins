"""Join the chunk outputs of analysis/calib_remote_v13.py --outer A:B into the per-seed share tables that
cd_common_v13 --calib import reads (<label>_<seed>.npz with p_lt, p_le, full). New file, 20 Nov 2026 (Claude Opus 5.5).

Checks before writing: the chunks of each (label, seed) tile 0..n_outer exactly (no gap, no overlap), every chunk has the
same full-sample values as the exported job's meta, and every chunk reproduced the full-sample values (full_sample_reproduced
all true). Never overwrites a different existing table. Writes MERGE_<label>.json (chunk list with SHA-256).
Usage: python -I calib_merge_v13.py CHUNKDIR OUTDIR LABEL [LABEL ...]
"""
import hashlib, json, pathlib, re, sys
import numpy as np

SEEDS = (20261913, 20261914)


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def merge(chunkdir, outdir, label):
    meta = json.loads((outdir / f'{label}.meta.json').read_text(encoding='utf-8'))
    n_outer = int(meta['n_outer']); full = np.asarray(meta['full'], float)
    rec = dict(label=label, n_outer=n_outer, seeds={})
    for seed in SEEDS:
        pat = re.compile(rf'^{re.escape(label)}_{seed}_o(\d+)_(\d+)\.npz$')
        ch = sorted((int(m.group(1)), int(m.group(2)), p) for p in chunkdir.iterdir() if (m := pat.match(p.name)))
        pos = 0; lt = []; le = []; used = []
        for lo, hi, p in ch:
            if lo != pos: raise SystemExit(f'{label} seed {seed}: chunks do not tile 0..{n_outer} (expected start {pos}, got {lo}:{hi})')
            z = np.load(p)
            assert int(z['seed']) == seed and str(z['label']) == label and list(z['outer']) == [lo, hi] and int(z['n_outer']) == n_outer, p.name
            assert np.array_equal(z['full'], full, equal_nan=True), f'{p.name}: full-sample values differ from the job meta'
            assert bool(np.all(z['full_sample_reproduced'])), f'{p.name}: the pod did not reproduce the full-sample values'
            assert z['p_lt'].shape == (hi - lo, full.size) and z['p_le'].shape == (hi - lo, full.size), p.name
            lt.append(z['p_lt']); le.append(z['p_le']); used.append(dict(file=p.name, outer=[lo, hi], sha256=sha(p))); pos = hi
        if pos != n_outer: raise SystemExit(f'{label} seed {seed}: chunks end at {pos}, not {n_outer}')
        p_lt = np.concatenate(lt); p_le = np.concatenate(le)
        out = outdir / f'{label}_{seed}.npz'
        if out.exists():
            z = np.load(out)
            if not (np.array_equal(z['p_lt'], p_lt, equal_nan=True) and np.array_equal(z['p_le'], p_le, equal_nan=True)):
                raise SystemExit(f'REFUSED: {out.name} exists with different content')
        else:
            tmp = outdir / f'{label}_{seed}.partial.npz'
            np.savez(tmp, p_lt=p_lt, p_le=p_le, full=full, seed=seed, label=label, full_sample_reproduced=np.array([True] * full.size))
            tmp.replace(out)
        rec['seeds'][str(seed)] = dict(table=out.name, sha256=sha(out), chunks=used)
        print(f'{label} seed {seed}: {len(used)} chunks -> {out.name}', flush=True)
    (outdir / f'MERGE_{label}.json').write_text(json.dumps(rec, indent=1), encoding='utf-8')


if __name__ == '__main__':
    cd, od = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    for lab in sys.argv[3:]:
        merge(cd, od, lab)
