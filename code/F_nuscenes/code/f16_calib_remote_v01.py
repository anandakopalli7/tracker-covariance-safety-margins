"""Package F (revision v13): the A10 section 2.6 double bootstrap of an exported F job, runnable on any many-core machine
(numpy + numba; no project paths). New file, 20 Nov 2026 (Claude Opus 5.5), at the coordinator's request (01:25 EST) to move the
double bootstrap to a pod. The arithmetic is f06_score_v01.double_bootstrap's, unchanged:
  outer IDX_O = default_rng(20261912).integers(0, n, (n_outer, n)); one inner stream default_rng(seed); for each outer sample b in
  order: ii = inner.integers(0, n, (n_inner, n)); counts of IDX_O[b][ii] per resample; the statistics of those weights; per
  statistic the shares of finite inner values below / at-or-below the full-sample value.
Statistics (f06_score_v01.HeldOut.stats, population 0), from f06k_kernel_v01.eval_many (copied next to this file, unchanged):
  kind FULL: two packed inputs a1 (roles F0, E, N of CANMOT) and a2 (roles F0, E, N, E5x of the IMM); columns
    R = denE1 / 201, RR_N = D1_N / denE1, r_IMM = D2_N / denE2, c_IMM = D2_E5x / denE2, eff_IMM = r / c (NaN when c is 0 or NaN);
    a share is NaN unless its denominator is finite and > 0.
  kind R: one packed input a1 (roles F0, E); column R = denE1 / 201 (the pre-Lock-2 platform test on the design split).
Input: JOBDIR/<job>.job.npz and <job>.meta.json (f06 heldout --calib=export, or f16_calib_job_v01.py for tests).
Output: JOBDIR/<job>_<seed>.npz with p_lt, p_le, full (recomputed here), full_reproduced (exact equality with the meta's full
values, NaN = NaN), job_sha256, platform, versions, seconds. Optional --single SEED NBOOT also writes <job>_single.npz with the
statistics of default_rng(SEED).integers(0, n, (NBOOT, n)) (the single bootstrap, for the platform test).
Usage: python f16_calib_remote_v01.py JOBDIR JOB [--seeds 20261913,20261914] [--threads N] [--single 20261923 20000]
"""
import hashlib, json, pathlib, platform, sys, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import f06k_kernel_v01 as K    # noqa: E402

NLEV = 201


def counts_of(idx, n):
    B = idx.shape[0]
    flat = (idx + n * np.arange(B)[:, None]).ravel()
    return np.bincount(flat, minlength=B * n).reshape(B, n).astype(np.float64)


def rr_of(D, den):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(np.isfinite(den) & (den > 0), D / den, np.nan)


def load(jf):
    z = np.load(jf, allow_pickle=False)
    kind = str(z['kind'])
    a1 = tuple(z['a1_%d' % i] for i in range(5))
    if kind == 'R':
        def stat(W):
            o = K.eval_many(np.ascontiguousarray(W, dtype=np.float64), *a1)
            return (o[:, 1] / NLEV)[:, None]
        return kind, stat
    a2 = tuple(z['a2_%d' % i] for i in range(5))

    def stat(W):
        W = np.ascontiguousarray(W, dtype=np.float64)
        o1 = K.eval_many(W, *a1); o2 = K.eval_many(W, *a2)
        r = rr_of(o2[:, 2], o2[:, 1]); c = rr_of(o2[:, 3], o2[:, 1])
        with np.errstate(divide='ignore', invalid='ignore'):
            eff = np.where(np.isfinite(c) & (c != 0), r / c, np.nan)
        return np.column_stack([o1[:, 1] / NLEV, rr_of(o1[:, 2], o1[:, 1]), r, c, eff])
    return kind, stat


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def run(jobdir, job, seeds, single=None, outdir=None):
    jobdir = pathlib.Path(jobdir); outdir = pathlib.Path(outdir or jobdir)
    meta = json.loads((jobdir / (job + '.meta.json')).read_text(encoding='utf-8'))
    jf = jobdir / (job + '.job.npz'); jsha = sha(jf)
    if meta.get('job_sha256') and meta['job_sha256'] != jsha:
        raise SystemExit('job file differs from its meta')
    n = int(meta['n_run']); n_outer = int(meta['n_outer']); n_inner = int(meta['n_inner']); seed_outer = int(meta['seed_outer'])
    full_meta = np.asarray(meta['full'], float)
    kind, stat = load(jf)
    full = stat(np.ones((1, n)))[0]
    reproduced = np.array([bool(a == b or (np.isnan(a) and np.isnan(b))) for a, b in zip(full, full_meta)])
    import numba
    info = dict(platform=platform.platform(), python=platform.python_version(), numpy=np.__version__, numba=numba.__version__,
                threads=int(numba.get_num_threads()))
    print(json.dumps(dict(job=job, kind=kind, n=n, full=full.tolist(), full_reproduced=reproduced.tolist(), **info)), flush=True)
    if single:
        sseed, nb = single
        t0 = time.time()
        S = stat(counts_of(np.random.default_rng(sseed).integers(0, n, (nb, n)), n))
        np.savez(outdir / (job + '_single.npz'), S=S, seed=sseed, nboot=nb, job_sha256=jsha, platform=info['platform'],
                 seconds=time.time() - t0)
        print('single bootstrap written (%.0f s)' % (time.time() - t0), flush=True)
    for seed in seeds:
        out = outdir / ('%s_%d.npz' % (job, seed))
        if out.exists():
            print('exists', out.name); continue
        t0 = time.time()
        IDX_O = np.random.default_rng(seed_outer).integers(0, n, (n_outer, n))
        rng_i = np.random.default_rng(seed)
        k = full.size
        p_lt = np.full((n_outer, k), np.nan); p_le = np.full((n_outer, k), np.nan)
        for b in range(n_outer):
            ii = rng_i.integers(0, n, (n_inner, n))
            S = stat(counts_of(IDX_O[b][ii], n))
            for j in range(k):
                v = S[:, j]; v = v[np.isfinite(v)]
                if v.size and np.isfinite(full[j]):
                    p_lt[b, j] = (v < full[j]).mean(); p_le[b, j] = (v <= full[j]).mean()
            if (b + 1) % 100 == 0:
                print('%s seed %d: outer %d / %d (%.0f s)' % (job, seed, b + 1, n_outer, time.time() - t0), flush=True)
        np.savez(out, p_lt=p_lt, p_le=p_le, full=full, full_reproduced=reproduced, seed=seed, job_sha256=jsha,
                 platform=info['platform'], versions=json.dumps(info), seconds=time.time() - t0)
        print('written', out.name, '%.0f s' % (time.time() - t0), flush=True)


def main():
    a = sys.argv[1:]
    jobdir, job = a[0], a[1]
    seeds = [20261913, 20261914]
    if '--seeds' in a:
        seeds = [int(x) for x in a[a.index('--seeds') + 1].split(',') if x]
    if '--threads' in a:
        import numba
        numba.set_num_threads(int(a[a.index('--threads') + 1]))
    single = None
    if '--single' in a:
        i = a.index('--single'); single = (int(a[i + 1]), int(a[i + 2]))
    outdir = a[a.index('--out') + 1] if '--out' in a else None
    run(jobdir, job, seeds, single, outdir)


if __name__ == '__main__':
    main()
