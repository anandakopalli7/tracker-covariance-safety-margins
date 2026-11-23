"""A10 sec. 2.6 double bootstrap for an exported statistic group, runnable on any many-core machine (numpy + numba; no project paths).

Input: <label>.job.npz and <label>.meta.json written by cd_common_v13.calibrate_all in --calib export mode (run on the laptop after
Lock 2). Next to this file: gl_fast_v13.py (the identical gridless kernel) and, for H4 jobs, optA_lib_v02.py (the scoring library of
record, copied unchanged). For each inner seed (20261913, 20261914): outer default_rng(20261912).integers(0, n, (2000, n)); inner one
stream of default_rng(seed).integers(0, n, (1000, n)) per outer sample in order, indexing that outer sample's runs (rev_d_bootstrap_v01
D2); per outer sample the inner shares below / at-or-below the full-sample values. Output: <label>_<seed>.npz (p_lt, p_le, full).
Usage: python calib_remote_v13.py JOBDIR LABEL [--seeds 20261913,20261914] [--threads N]
"""
import json, pathlib, sys, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gl_fast_v13 as GF       # noqa: E402

N_OUTER, N_INNER, SEED_OUTER = 2000, 1000, 20261912


class _P:                       # a gl_fast Prepared rebuilt from the job file
    pass


def load(job):
    z = np.load(job, allow_pickle=False)
    kind = str(z['kind'])
    if kind == 'GL':
        P = _P(); P.names = [str(x) for x in z['names']]; P.pop = int(z['pop']); P.T0 = [x for x in z['T0']]
        P.d = np.ascontiguousarray(z['d']); P.ri = z['ri'].astype(np.int64); P.keep = z['keep'].astype(np.int64)
        P.ev_off = z['ev_off'].astype(np.int64); P.keep_off = z['keep_off'].astype(np.int64); P.nrun = P.T0[0].shape[0]
        spec = [tuple(s) for s in json.loads(str(z['spec']))]

        def stat(Wr):
            e = GF.evaluate(P, Wr); den = e['denE']; ok = np.isfinite(den) & (den > 0); cols = []
            with np.errstate(divide='ignore', invalid='ignore'):
                for s in spec:
                    if s[0] == 'R': cols.append(den / 201.)
                    elif s[0] == 'RR': cols.append(np.where(ok, e['D'][s[1]] / den, np.nan))
                    else: cols.append(np.where(ok, e['D'][s[1]] / den, np.nan) - np.where(ok, e['D'][s[2]] / den, np.nan))
            return np.stack(cols, axis=1)
        return stat
    import optA_lib_v02 as L                                   # H4: the library of record, copied unchanged
    fF0, fE, tri, one = z['fF0'], z['fE'], z['tri'], z['one']

    def share(w):
        Ta = np.tensordot(w, fF0[:, :, 0, :], axes=(0, 0)); TE = np.tensordot(w, fE[:, :, 0, :], axes=(0, 0))
        c = L.curves_w({'F0': Ta, 'E': TE}, 0); cF0, wF0 = c['F0']; cE, wE = c['E']
        lev_ = L.levels_of(cF0, cE, cF0[0])
        f0 = L.frontier(cF0, wF0, lev_); fe = L.frontier(cE, wE, lev_)
        Tph = [np.tensordot(w, fF0[:, :, pi, :], axes=(0, 0)) for pi in (2, 3, 4)]
        nl = tri.shape[0]; Wv = np.zeros(nl); Sv = np.zeros(nl); Kv = np.zeros(nl)
        for q in range(3):
            g = tri[:, q]; okg = g >= 0
            Wv[okg] += Tph[q][g[okg], 1]; Sv[okg] += Tph[q][g[okg], 2]; Kv[okg] += Tph[q][g[okg], 3]
        n = float(Ta[0, 0])
        with np.errstate(divide='ignore', invalid='ignore'):
            cp = np.where(tri[:, 0] >= 0, 100. * Sv / Kv, np.nan); wp = np.where(tri[:, 0] >= 0, 100. * Wv / n, np.nan)
        fps = L.frontier(np.concatenate([[cF0[0]], cp]), np.concatenate([[wF0[0]], wp]), lev_)
        den = float(np.sum(f0 - fe))
        return float(np.sum(f0 - fps)) / den if den > 0 else np.nan
    return lambda Wr: np.array([[share(w)] for w in Wr])


def counts_of(idx, n):
    B = idx.shape[0]; flat = (idx + n * np.arange(B)[:, None]).ravel()
    return np.bincount(flat, minlength=B * n).reshape(B, n).astype(float)


def main():
    jobdir = pathlib.Path(sys.argv[1]); label = sys.argv[2]
    seeds = [20261913, 20261914]
    if '--seeds' in sys.argv: seeds = [int(x) for x in sys.argv[sys.argv.index('--seeds') + 1].split(',')]
    if '--threads' in sys.argv:
        import numba; numba.set_num_threads(int(sys.argv[sys.argv.index('--threads') + 1]))
    meta = json.loads((jobdir / f'{label}.meta.json').read_text())
    global N_OUTER
    N_OUTER = int(meta.get('n_outer', N_OUTER))                     # 2000 for every real job; smaller only in --test-old jobs
    n = int(meta['n_run']); full = np.asarray(meta['full'], float); k = full.size
    stat = load(jobdir / f'{label}.job.npz')
    chk = stat(np.ones((1, n)))[0]
    same = [bool(a == b or (np.isnan(a) and np.isnan(b))) for a, b in zip(chk, full)]
    print(json.dumps(dict(label=label, full_sample_reproduced=same)), flush=True)
    for seed in seeds:
        out = jobdir / f'{label}_{seed}.npz'
        if out.exists(): continue
        t0 = time.time()
        rng_o = np.random.default_rng(SEED_OUTER); rng_i = np.random.default_rng(seed)
        IDX_O = rng_o.integers(0, n, (N_OUTER, n))
        p_lt = np.full((N_OUTER, k), np.nan); p_le = np.full((N_OUTER, k), np.nan)
        OE = np.asarray(stat(counts_of(IDX_O, n)), float).reshape(N_OUTER, k)       # outer estimates (v11: skip non-finite ones)
        for b in range(N_OUTER):
            io = IDX_O[b]; ii = rng_i.integers(0, n, (N_INNER, n))
            S = np.asarray(stat(counts_of(io[ii], n)), float).reshape(N_INNER, k)
            for j in range(k):
                v = S[:, j]; v = v[np.isfinite(v)]
                if v.size == 0 or not np.isfinite(full[j]) or not np.isfinite(OE[b, j]): continue
                p_lt[b, j] = (v < full[j]).mean(); p_le[b, j] = (v <= full[j]).mean()
            if (b + 1) % 100 == 0: print('%s seed %d: %d/%d (%.0f s)' % (label, seed, b + 1, N_OUTER, time.time() - t0), flush=True)
        np.savez(out, p_lt=p_lt, p_le=p_le, full=full, seed=seed, label=label, full_sample_reproduced=np.array(same))
        print('written', out.name, '%.0f s' % (time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
