"""Crossing: what moves the covariance margin relative to the class margin (EXPLORATORY; coordinator's A12 task 4; sprint panel E4, S4;
R2 F1). First program. New file, 22 Nov 2026 (Claude Opus 5.5, session CD). Reads crossing/heading/<run>.npz (x_heading_v13.py); tests
nothing; every value is descriptive.

Ticks: evaluated (status 0), a primary actor, a binding constraint for it at row idx55 (bind_ok), |v_hat| > 0.5 m/s, all of y, cos_phi,
te, e_n, age_upd, miss finite.
  y        = y_bind = 0.5 ln(Pr/Sbar) at the constraint that binds the class margin (the covariance margin relative to the class margin)
  geometry = {cos_phi^2 (estimated heading against the constraint normal), te (look-ahead of that constraint)}
  schedule = {miss (updates since the last detection), ln(1 + age_upd)}
  error    = {|e_n|} (realised error along the normal, class-margin units)
OLS of y on the three groups (with intercept); R^2 of every subset; Shapley (LMG) shares of R^2 by group (exact, 3 groups);
run-clustered bootstrap (B = 2000, default_rng(20261951), runs resampled with replacement) for the shares and the full R^2 (percentile
95%). The same for y_dec = 0.5 ln(cF0/cN) at row idx55 (decision level). Spearman rho (average ranks) of y with each regressor. Object-frame check: the
angle between the major axis of the actor's 2x2 position covariance and its velocity estimate (|sin| median, IQR), and the axis ratio.
Writes crossing/out/X_HEADING_v13.json (never overwritten).
Usage: python -I -B x_heading_analyse_v13.py
"""
import hashlib, itertools, json, math, os, pathlib, sys
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
IN = HERE / 'heading'; OUTF = HERE / 'out' / 'X_HEADING_v13.json'
GROUPS = dict(geometry=[0, 1], schedule=[2, 3], error=[4])
NAMES = ['cos_phi2', 'te', 'miss', 'ln1p_age_upd', 'abs_e_n']
B, SEED = 2000, 20261951


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def load():
    runs = []
    for f in sorted(IN.glob('pc13x_*.npz')):
        z = np.load(f, allow_pickle=False)
        ok = (z['status'] == 0) & (z['bind_ok'] == 1) & np.isfinite(z['cos_phi'])
        X = np.column_stack([z['cos_phi'] ** 2, z['te'], z['miss'], np.log1p(z['age_upd']), np.abs(z['e_n'])])
        ok &= np.isfinite(X).all(axis=1) & np.isfinite(z['y_bind'])
        P = z['P'][ok]; V = np.column_stack([z['vx'], z['vy']])[ok]
        runs.append(dict(run=f.stem, X=X[ok], y=z['y_bind'][ok], ydec=z['y_dec'][ok], V=V, P=P,
                         n_all=int(len(z['k'])), n_eval=int((z['status'] == 0).sum()), n_prim=int(((z['status'] == 0) & np.isfinite(z['prim'])).sum()),
                         n_bind=int(((z['status'] == 0) & (z['bind_ok'] == 1)).sum())))
    return runs


def suff(X, y):
    A = np.column_stack([np.ones(len(y)), X])
    return A.T @ A, A.T @ y, float(y @ y), len(y), float(y.sum())


def r2_all(AtA, Aty, yty, n, sy):
    sst = yty - sy * sy / n; out = {}
    k = AtA.shape[0] - 1
    for r in range(k + 1):
        for S in itertools.combinations(range(k), r):
            idx = [0] + [s + 1 for s in S]
            beta = np.linalg.lstsq(AtA[np.ix_(idx, idx)], Aty[idx], rcond=None)[0]
            ssr = yty - 2 * beta @ Aty[idx] + beta @ AtA[np.ix_(idx, idx)] @ beta
            out[S] = 1. - ssr / sst
    return out


def shapley(R2):
    G = list(GROUPS); res = {}
    for g in G:
        others = [h for h in G if h != g]; tot = 0.
        for r in range(len(others) + 1):
            for S in itertools.combinations(others, r):
                w = math.factorial(r) * math.factorial(len(G) - r - 1) / math.factorial(len(G))
                cols = tuple(sorted(c for h in S for c in GROUPS[h])); cols_g = tuple(sorted(cols + tuple(GROUPS[g])))
                tot += w * (R2[cols_g] - R2[cols])
        res[g] = tot
    return res


def decompose(runs, key):
    S = [suff(r['X'], r[key]) for r in runs if len(r[key])]
    def agg(c):
        return (sum(ci * s[0] for ci, s in zip(c, S)), sum(ci * s[1] for ci, s in zip(c, S)), sum(ci * s[2] for ci, s in zip(c, S)),
                sum(ci * s[3] for ci, s in zip(c, S)), sum(ci * s[4] for ci, s in zip(c, S)))
    one = np.ones(len(S))
    R2 = r2_all(*agg(one)); full = R2[tuple(range(5))]; sh = shapley(R2)
    AtA, Aty = agg(one)[:2]
    beta = np.linalg.solve(AtA, Aty)
    rng = np.random.default_rng(SEED); bs = []
    for _ in range(B):
        c = np.bincount(rng.integers(0, len(S), len(S)), minlength=len(S)).astype(float)
        Rb = r2_all(*agg(c)); sb = shapley(Rb); bs.append([Rb[tuple(range(5))]] + [sb[g] for g in GROUPS])
    bs = np.array(bs)
    ci = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
    return dict(n_ticks=int(sum(s[3] for s in S)), n_runs=len(S), r2_full=float(full), r2_full_ci95=ci(bs[:, 0]),
                shapley_r2={g: float(sh[g]) for g in GROUPS}, shapley_r2_ci95={g: ci(bs[:, i + 1]) for i, g in enumerate(GROUPS)},
                shapley_share_of_r2={g: float(sh[g] / full) for g in GROUPS},
                r2_single_group={g: float(R2[tuple(GROUPS[g])]) for g in GROUPS},
                coef=dict(zip(['intercept'] + NAMES, map(float, beta))))


def spearman(a, b):
    from scipy.stats import rankdata                 # average ranks for ties (miss and age_upd are integers)
    return float(np.corrcoef(rankdata(a), rankdata(b))[0, 1])


def main():
    if OUTF.exists(): raise SystemExit('REFUSED: %s exists' % OUTF.name)
    runs = load()
    X = np.concatenate([r['X'] for r in runs]); y = np.concatenate([r['y'] for r in runs]); yd = np.concatenate([r['ydec'] for r in runs])
    fin = np.isfinite(yd)
    P = np.concatenate([r['P'] for r in runs]); Vh = np.concatenate([r['V'] for r in runs])
    # object-frame check on the 2x2 position block (planner frame) against the velocity estimate's direction
    w, E = np.linalg.eigh(P[:, :2, :2])
    major = E[:, :, 1]; u = Vh / np.linalg.norm(Vh, axis=1)[:, None]
    sin_major = np.abs(major[:, 0] * u[:, 1] - major[:, 1] * u[:, 0])
    ratio = np.sqrt(w[:, 1] / np.maximum(w[:, 0], 1e-300))
    out = dict(code='x_heading_analyse_v13.py', code_sha256=sha(__file__), status='EXPLORATORY (A12 task 4; sprint E4, S4); no test',
               n_runs=len(runs), ticks=dict(all=sum(r['n_all'] for r in runs), evaluated=sum(r['n_eval'] for r in runs),
                                            primary=sum(r['n_prim'] for r in runs), binding=sum(r['n_bind'] for r in runs), analysed=int(len(y))),
               y_bind=dict(median=float(np.median(y)), iqr=[float(np.percentile(y, 25)), float(np.percentile(y, 75))], sd=float(np.std(y))),
               spearman_y_bind={n: spearman(y, X[:, i]) for i, n in enumerate(NAMES)},
               decomposition_y_bind=decompose(runs, 'y'))
    rd = [dict(r, X=r['X'][np.isfinite(r['ydec'])], ydec=r['ydec'][np.isfinite(r['ydec'])]) for r in runs]
    out['decomposition_y_dec'] = decompose(rd, 'ydec'); out['y_dec_finite_ticks'] = int(fin.sum())
    out['spearman_y_dec'] = {n: spearman(yd[fin], X[fin, i]) for i, n in enumerate(NAMES)}
    q = lambda a: dict(median=float(np.median(a)), iqr=[float(np.percentile(a, 25)), float(np.percentile(a, 75))],
                       p05_p95=[float(np.percentile(a, 5)), float(np.percentile(a, 95))])
    out['object_frame_check'] = dict(note='|sin| of the angle between the major axis of the 2x2 position covariance (planner frame) and the '
                                     'velocity estimate: 0 = aligned with the heading, 1 = across it; axis ratio = sqrt(major/minor eigenvalue)',
                                     abs_sin_major_vs_heading=q(sin_major), axis_ratio=q(ratio),
                                     share_aligned_within_10deg=float(np.mean(sin_major < math.sin(math.radians(10)))),
                                     share_across_within_10deg=float(np.mean(sin_major > math.cos(math.radians(10)))))
    out['inputs'] = {f.name: sha(f) for f in sorted(IN.glob('pc13x_*.npz'))}
    OUTF.parent.mkdir(exist_ok=True)
    OUTF.write_text(json.dumps(out, indent=1), encoding='utf-8')
    print(json.dumps({k: out[k] for k in ('n_runs', 'ticks', 'decomposition_y_bind')}, indent=1)[:3000])


if __name__ == '__main__':
    main()
