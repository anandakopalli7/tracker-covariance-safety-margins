"""Revision v13, AMENDMENT_12 sec. 3a.4: the A10 sec. 2.6 double bootstrap of the dose-response slope b, runnable on a many-core pod.
New file, 22 Nov 2026 (Claude Opus 5.5, session F). The four per-p statistics r(p) = RR_gl(N_DR(p)) are CD's exported GLStat jobs
(dose_<ptag>.job.npz, spec [('RR', 'N')]), evaluated by CD_capture\\analysis\\calib_remote_v13.load (gl_fast, unchanged). The draws are
calib_remote_v13's: outer default_rng(20261912).integers(0, n, (2000, n)); for each inner seed one stream default_rng(seed).integers(0, n,
(1000, n)) per outer sample in order, indexing that outer sample's runs; the inner statistics' shares below / at-or-below the full-sample
b (b of a resample: OLS slope of the four r over p, NaN if any r is NaN); outer samples whose own b is not finite are skipped.
--outer A:B computes outer samples A..B-1 only (the inner draws of 0..A-1 are generated and discarded), output dose_slope_<seed>_oA_B.npz;
merge with `merge`.
Usage: python dr_slope_remote_v01.py JOBDIR [--seeds 20261913,20261914] [--threads N] [--outer A:B]
       python dr_slope_remote_v01.py JOBDIR merge
"""
import json, pathlib, sys, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
for cand in (HERE.parents[1] / 'CD_capture' / 'analysis', HERE):
    if (cand / 'calib_remote_v13.py').is_file():
        sys.path.insert(0, str(cand)); break
import calib_remote_v13 as CR            # noqa: E402

N_OUTER, N_INNER, SEED_OUTER = 2000, 1000, 20261912
PS = (0.05, 0.10, 0.20, 0.30)


def slope_of(R):
    x = np.array(PS) - np.mean(PS)
    b = (R - R.mean(axis=1, keepdims=True)) @ x / (x @ x)
    b[~np.isfinite(R).all(axis=1)] = np.nan
    return b


def main():
    jobdir = pathlib.Path(sys.argv[1])
    meta = json.loads((jobdir / 'dose_slope.meta.json').read_text())
    if len(sys.argv) > 2 and sys.argv[2] == 'merge':
        return merge(jobdir, meta)
    seeds = [20261913, 20261914]
    if '--seeds' in sys.argv: seeds = [int(x) for x in sys.argv[sys.argv.index('--seeds') + 1].split(',')]
    if '--threads' in sys.argv:
        import numba; numba.set_num_threads(int(sys.argv[sys.argv.index('--threads') + 1]))
    n_outer = int(meta.get('n_outer', N_OUTER)); n = int(meta['n_run']); full = float(meta['full'][0])
    lo, hi = 0, n_outer
    if '--outer' in sys.argv:
        lo, hi = (int(x) for x in sys.argv[sys.argv.index('--outer') + 1].split(':'))
    chunk = (lo, hi) != (0, n_outer)
    stats = [CR.load(jobdir / ('dose_p%03d.job.npz' % int(round(p * 100)))) for p in PS]
    stat = lambda Wr: slope_of(np.stack([s(Wr)[:, 0] for s in stats], axis=1))
    chk = float(stat(np.ones((1, n)))[0])
    same = bool(chk == full)
    print(json.dumps(dict(full=full, reproduced=chk, full_sample_reproduced=same)), flush=True)
    for seed in seeds:
        out = jobdir / (('dose_slope_%d_o%d_%d.npz' % (seed, lo, hi)) if chunk else ('dose_slope_%d.npz' % seed))
        if out.exists(): continue
        t0 = time.time()
        IDX_O = np.random.default_rng(SEED_OUTER).integers(0, n, (n_outer, n)); rng_i = np.random.default_rng(seed)
        OE = stat(CR.counts_of(IDX_O[lo:hi], n))
        p_lt = np.full((hi - lo, 1), np.nan); p_le = np.full((hi - lo, 1), np.nan)
        for b in range(lo):
            rng_i.integers(0, n, (N_INNER, n))
        for b in range(lo, hi):
            io = IDX_O[b]; ii = rng_i.integers(0, n, (N_INNER, n))
            v = stat(CR.counts_of(io[ii], n)); v = v[np.isfinite(v)]
            if v.size == 0 or not np.isfinite(full) or not np.isfinite(OE[b - lo]): continue
            p_lt[b - lo, 0] = (v < full).mean(); p_le[b - lo, 0] = (v <= full).mean()
            if (b + 1) % 100 == 0: print('seed %d: %d/%d (%.0f s)' % (seed, b + 1, n_outer, time.time() - t0), flush=True)
        tmp = out.with_name(out.stem + '.partial.npz')
        np.savez(tmp, p_lt=p_lt, p_le=p_le, full=np.array([full]), seed=seed, full_sample_reproduced=same, outer=np.array([lo, hi]))
        tmp.replace(out)
        print('written', out.name, '%.0f s' % (time.time() - t0), flush=True)


def merge(jobdir, meta):
    n_outer = int(meta.get('n_outer', N_OUTER))
    for seed in (20261913, 20261914):
        parts = sorted(jobdir.glob('dose_slope_%d_o*_*.npz' % seed), key=lambda q: int(q.stem.split('_o')[1].split('_')[0]))
        if not parts: continue
        z = [np.load(q) for q in parts]
        rng = [tuple(int(x) for x in q['outer']) for q in z]
        assert rng[0][0] == 0 and rng[-1][1] == n_outer and all(a[1] == b[0] for a, b in zip(rng, rng[1:])), rng
        assert all(bool(q['full_sample_reproduced']) for q in z)
        out = jobdir / ('dose_slope_%d.npz' % seed)
        if out.exists(): raise SystemExit('REFUSED: %s exists' % out)
        np.savez(out, p_lt=np.concatenate([q['p_lt'] for q in z]), p_le=np.concatenate([q['p_le'] for q in z]), full=z[0]['full'], seed=seed,
                 full_sample_reproduced=True, outer=np.array([0, n_outer]), chunks=np.array(rng))
        print('merged', out.name, len(parts), 'chunks')


if __name__ == '__main__':
    main()
