"""Second program (recount) of the exploratory crossing analysis: margin ratio y against heading, schedule and realised error.
Written 22 Nov 2026 (Claude Sonnet 5.5) from recount\\SPEC_RC_X_HEADING_v13.md only. The first programs (x_heading_v13.py,
x_heading_analyse_v13.py) were NOT opened. Everything reported is descriptive; nothing is tested.

Part 1: from the per-run npz files (pc13x_*.npz in --in-dir): selection, OLS R^2 over all regressor subsets, exact Shapley (LMG) by
        group (geometry {cos_phi^2, te}, schedule {miss, ln(1+age_upd)}, error {|e_n|}), run-clustered bootstrap (sufficient statistics
        per run; equivalent to stacking c copies of each run), Spearman, object-frame check, counts. Same for y_dec.
Part 2: per-tick recomputation of y_bind, cos_phi, e_n, te, y_dec for three runs from the logs (modules of record via trk_arrays_v01)
        and comparison with the npz values.

Run (one process, BelowNormal): .venv\\Scripts\\python.exe -I -B recount\\rc_x_heading_v13.py [--in-dir D] [--out F] [options]
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import argparse, ctypes, hashlib, itertools, json, math, pathlib, shutil, sys, tarfile, time
import numpy as np
from scipy.stats import rankdata

HERE = pathlib.Path(__file__).resolve().parent
CD = HERE.parent
TRACKERS = CD.parent / 'shared' / 'trackers'
PBAR_JSON = pathlib.Path(r'<library folder>\pbar_tuning_v01.json')
SEED = 20261951
B_BOOT = 2000
XNAMES = ['cos_phi^2', 'te', 'miss', 'ln(1+age_upd)', '|e_n|']
GROUPS = {'geometry': [0, 1], 'schedule': [2, 3], 'error': [4]}
GNAMES = list(GROUPS)
KEYS_REQ = ['k', 'status', 'prim', 'bind_ok', 'y_bind', 'cos_phi', 'speed', 'e_n', 'te', 'offset', 'age_s', 'age_upd', 'miss',
            'y_dec', 'chkF0', 'chkN', 'P', 'Pbar']


def lower_priority():
    try:
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
    except Exception:
        pass


def jnum(x):
    """JSON-safe: NaN / inf -> None (with a string for inf), numpy scalars -> python."""
    if isinstance(x, dict):
        return {str(k): jnum(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jnum(v) for v in x]
    if isinstance(x, np.ndarray):
        return jnum(x.tolist())
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    if isinstance(x, (np.integer, int)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        x = float(x)
        if math.isnan(x):
            return None
        if math.isinf(x):
            return 'inf' if x > 0 else '-inf'
        return x
    return x


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------------------------------------ loading and selection
def load_runs(in_dir, synth_v):
    files = sorted(pathlib.Path(in_dir).glob('pc13x_*.npz'), key=lambda p: p.name)
    if not files:
        raise SystemExit('no pc13x_*.npz in %s' % in_dir)
    runs = []; synth_used = False
    rng_v = np.random.default_rng(1234)
    for f in files:
        with np.load(f, allow_pickle=False) as z:
            d = {k: z[k] for k in z.files}
        miss = [k for k in KEYS_REQ if k not in d]
        if miss:
            raise SystemExit('%s lacks keys %s' % (f.name, miss))
        if 'vx' not in d or 'vy' not in d:
            if not synth_v:
                raise SystemExit('%s lacks vx/vy (use --synth-v only for a test)' % f.name)
            th = rng_v.uniform(0, 2 * np.pi, len(d['k']))
            d['vx'] = np.cos(th); d['vy'] = np.sin(th); synth_used = True
        n = len(d['k'])
        for k in KEYS_REQ + ['vx', 'vy']:
            if d[k].shape[0] != n:
                raise SystemExit('%s: key %s has length %d != %d' % (f.name, k, d[k].shape[0], n))
        d['_name'] = f.name; d['_stem'] = f.stem; d['_path'] = f
        runs.append(d)
    return runs, synth_used


def select(d):
    """Boolean mask of analysed ticks of one run (spec: Selection)."""
    with np.errstate(invalid='ignore'):
        m = (d['status'] == 0) & (d['bind_ok'] == 1) & np.isfinite(d['cos_phi'])
    for k in ('y_bind', 'cos_phi', 'te', 'miss', 'age_upd', 'e_n'):
        m &= np.isfinite(d[k])
    return m


def design(d, m):
    x = np.column_stack([d['cos_phi'][m] ** 2, d['te'][m], d['miss'][m], np.log1p(d['age_upd'][m]), np.abs(d['e_n'][m])])
    return x


# ------------------------------------------------------------------------------------------------ OLS, Shapley, bootstrap
def r2_direct(X, y, cols):
    """R^2 = 1 - SSR/SST of y on an intercept and X[:, cols] (least squares)."""
    if not cols:
        return 0.0
    A = np.column_stack([np.ones(len(y)), X[:, cols]])
    beta = np.linalg.lstsq(A, y, rcond=None)[0]
    r = y - A @ beta
    sst = float(((y - y.mean()) ** 2).sum())
    return 1.0 - float(r @ r) / sst


def all_subset_r2(X, y):
    out = {}
    for r in range(0, 6):
        for cols in itertools.combinations(range(5), r):
            out[cols] = r2_direct(X, y, list(cols))
    return out


def group_subsets():
    """Each subset of groups (frozenset of names) -> sorted regressor column list."""
    out = {}
    for r in range(0, 4):
        for gs in itertools.combinations(GNAMES, r):
            cols = sorted(c for g in gs for c in GROUPS[g])
            out[frozenset(gs)] = cols
    return out


GSUB = group_subsets()


def shapley(r2_of_groups):
    """Exact Shapley over the 3 groups. r2_of_groups: frozenset of group names -> R^2 (empty set -> 0)."""
    out = {}
    for g in GNAMES:
        others = [h for h in GNAMES if h != g]
        s = 0.0
        for r in range(0, len(others) + 1):
            w = math.factorial(r) * math.factorial(3 - r - 1) / math.factorial(3)
            for S in itertools.combinations(others, r):
                S = frozenset(S)
                s += w * (r2_of_groups[S | {g}] - r2_of_groups[S])
        out[g] = s
    return out


def group_r2_direct(X, y):
    return {gs: (0.0 if not cols else r2_direct(X, y, cols)) for gs, cols in GSUB.items()}


def run_stats(X, y, mu, sd, ymu, ysd):
    """Per-run sufficient statistics Z'Z, Z = [1, standardised X, standardised y] (7 x 7)."""
    Z = np.column_stack([np.ones(len(y)), (X - mu) / sd, ((y - ymu) / ysd)])
    return Z.T @ Z


def r2_from_G(G, cols):
    """R^2 of y on intercept + cols from the (weighted) Z'Z; Z columns: 0 = 1, 1..5 = x, 6 = y."""
    if not cols:
        return 0.0
    n = G[0, 0]
    idx = [1 + c for c in cols]
    sxx = G[np.ix_(idx, idx)] - np.outer(G[idx, 0], G[idx, 0]) / n
    sxy = G[idx, 6] - G[idx, 0] * G[0, 6] / n
    syy = G[6, 6] - G[0, 6] ** 2 / n
    try:
        b = np.linalg.solve(sxx, sxy)
    except np.linalg.LinAlgError:
        b = np.linalg.lstsq(sxx, sxy, rcond=None)[0]
    return float(b @ sxy / syy)


def groupr2_from_G(G):
    return {gs: r2_from_G(G, cols) for gs, cols in GSUB.items()}


def analyse_block(runs_xy, label):
    """runs_xy: list (file order) of (name, X (n_i x 5), y (n_i,)) with n_i >= 1. Returns the result dict."""
    X = np.vstack([r[1] for r in runs_xy]); y = np.concatenate([r[2] for r in runs_xy])
    nr = len(runs_xy)
    res = dict(label=label, n_runs=nr, n_ticks=int(len(y)))
    if len(y) < 8 or np.ptp(y) == 0:
        res['error'] = 'too few ticks or constant y'
        return res
    # point estimates (direct least squares)
    sub = all_subset_r2(X, y)
    res['r2_all_subsets'] = {'+'.join(XNAMES[c] for c in cols) if cols else '(intercept only)': v for cols, v in sub.items()}
    res['r2_full'] = sub[(0, 1, 2, 3, 4)]
    A = np.column_stack([np.ones(len(y)), X])
    beta = np.linalg.lstsq(A, y, rcond=None)[0]
    res['coef_full'] = dict(zip(['intercept'] + XNAMES, beta.tolist()))
    g2 = group_r2_direct(X, y)
    sh = shapley(g2)
    res['shapley_r2'] = sh
    res['shapley_sum_minus_r2_full'] = float(sum(sh.values()) - res['r2_full'])
    res['shapley_share_of_r2'] = {g: sh[g] / res['r2_full'] for g in GNAMES}
    res['r2_single_group'] = {g: g2[frozenset([g])] for g in GNAMES}
    # bootstrap
    mu = X.mean(0); sd = X.std(0); sd = np.where(sd > 0, sd, 1.0); ymu = y.mean(); ysd = y.std()
    Gs = np.stack([run_stats(r[1], r[2], mu, sd, ymu, ysd) for r in runs_xy])        # (nr, 7, 7)
    Gtot = Gs.sum(0)
    gchk = groupr2_from_G(Gtot)
    res['bootstrap_point_check_max_abs_diff'] = float(max(abs(gchk[s] - g2[s]) for s in g2))
    rng = np.random.default_rng(SEED)
    full = np.full(B_BOOT, np.nan); shb = {g: np.full(B_BOOT, np.nan) for g in GNAMES}
    for b in range(B_BOOT):
        idx = rng.integers(0, nr, nr)
        c = np.bincount(idx, minlength=nr).astype(float)
        G = np.tensordot(c, Gs, axes=(0, 0))
        gr = groupr2_from_G(G)
        full[b] = gr[frozenset(GNAMES)]
        s = shapley(gr)
        for g in GNAMES:
            shb[g][b] = s[g]
    res['bootstrap'] = dict(B=B_BOOT, seed=SEED, n_nonfinite_r2_full=int((~np.isfinite(full)).sum()))
    res['r2_full_ci95'] = np.percentile(full, [2.5, 97.5]).tolist()
    res['shapley_r2_ci95'] = {g: np.percentile(shb[g], [2.5, 97.5]).tolist() for g in GNAMES}
    # Spearman (average ranks, pooled)
    ry = rankdata(y)
    sp = {}
    for j, nm in enumerate(XNAMES):
        rx = rankdata(X[:, j])
        if np.std(rx) == 0 or np.std(ry) == 0:
            sp[nm] = None
        else:
            sp[nm] = float(np.corrcoef(ry, rx)[0, 1])
    res['spearman_rho'] = sp
    return res


# ------------------------------------------------------------------------------------------------ object-frame check
def q5(v):
    p = np.percentile(v, [5, 25, 50, 75, 95])
    return dict(p5=p[0], p25=p[1], median=p[2], p75=p[3], p95=p[4], iqr=p[3] - p[1])


def object_frame(runs, masks):
    sines = []; ratios = []; nbad = 0
    for d, m in zip(runs, masks):
        if not m.any():
            continue
        P = d['P'][m][:, :2, :2]; vx = d['vx'][m]; vy = d['vy'][m]
        for i in range(len(P)):
            if not (np.isfinite(P[i]).all() and np.isfinite(vx[i]) and np.isfinite(vy[i])):
                nbad += 1; continue
            sp = math.hypot(vx[i], vy[i])
            if sp <= 0:
                nbad += 1; continue
            w, V = np.linalg.eigh(P[i])
            mx, my = V[0, 1], V[1, 1]                 # eigenvector of the larger eigenvalue (eigh: ascending)
            ux, uy = vx[i] / sp, vy[i] / sp
            sines.append(abs(mx * uy - my * ux))
            ratios.append(math.sqrt(w[1] / w[0]) if w[0] > 0 else float('inf'))
    sines = np.array(sines); ratios = np.array(ratios)
    out = dict(n_ticks=int(len(sines)), n_dropped_nonfinite=nbad)
    if len(sines) == 0:
        return out
    s10 = math.sin(math.radians(10)); c10 = math.cos(math.radians(10))
    out['abs_sin_angle'] = dict(**q5(sines), share_aligned_lt_sin10=float((sines < s10).mean()),
                                share_across_gt_cos10=float((sines > c10).mean()))
    fin = np.isfinite(ratios)
    out['axis_ratio'] = dict(**q5(ratios[fin]), n_infinite=int((~fin).sum()),
                             note='shares of the aligned / across criterion refer to |sin| of the same tick; axis ratio is reported by those classes below',
                             share_aligned_lt_sin10=float((sines < s10).mean()), share_across_gt_cos10=float((sines > c10).mean()))
    for nm, mk in (('aligned', sines < s10), ('across', sines > c10)):
        mk = mk & fin
        out['axis_ratio']['median_axis_ratio_' + nm] = float(np.median(ratios[mk])) if mk.any() else None
    return out


# ------------------------------------------------------------------------------------------------ Part 1
def part1(runs):
    masks = [select(d) for d in runs]
    n_all = sum(len(d['k']) for d in runs)
    with np.errstate(invalid='ignore'):
        n_eval = sum(int((d['status'] == 0).sum()) for d in runs)
        n_prim = sum(int(((d['status'] == 0) & np.isfinite(d['prim'])).sum()) for d in runs)
        n_bind = sum(int(((d['status'] == 0) & (d['bind_ok'] == 1)).sum()) for d in runs)
    n_an = sum(int(m.sum()) for m in masks)
    res = dict(counts=dict(n_files=len(runs), n_runs_with_analysed_ticks=int(sum(1 for m in masks if m.any())),
                           ticks_all=n_all, ticks_evaluated_status0=n_eval, ticks_primary_status0_finite_prim=n_prim,
                           ticks_binding_status0_bind_ok1=n_bind, ticks_analysed=n_an))
    # y_bind block
    blk = []
    for d, m in zip(runs, masks):
        if m.any():
            blk.append((d['_name'], design(d, m), d['y_bind'][m]))
    yb = np.concatenate([b[2] for b in blk]) if blk else np.array([])
    if len(yb):
        p = np.percentile(yb, [25, 50, 75])
        res['counts']['y_bind'] = dict(median=p[1], q25=p[0], q75=p[2], iqr=p[2] - p[0], sd_ddof0=float(np.std(yb)))
    res['y_bind'] = analyse_block(blk, 'y_bind') if blk else dict(error='no analysed ticks')
    # y_dec block (subset with finite y_dec)
    blk2 = []
    for d, m in zip(runs, masks):
        m2 = m & np.isfinite(d['y_dec'])
        if m2.any():
            blk2.append((d['_name'], design(d, m2), d['y_dec'][m2]))
    res['counts']['ticks_analysed_with_finite_y_dec'] = int(sum(len(b[2]) for b in blk2))
    res['counts']['n_runs_with_finite_y_dec_ticks'] = len(blk2)
    if blk2:
        yd = np.concatenate([b[2] for b in blk2]); p = np.percentile(yd, [25, 50, 75])
        res['counts']['y_dec'] = dict(median=p[1], q25=p[0], q75=p[2], iqr=p[2] - p[0], sd_ddof0=float(np.std(yd)))
    res['y_dec'] = analyse_block(blk2, 'y_dec') if blk2 else dict(error='no ticks')
    res['object_frame'] = object_frame(runs, masks)
    return res


# ------------------------------------------------------------------------------------------------ Part 2
def extract_archive(rid, scratch):
    arch = CD / 'archives' / rid / ('claude_main_%s.tar.gz' % rid)
    if not arch.exists():
        raise SystemExit('archive missing: %s' % arch)
    dest = pathlib.Path(scratch) / ('x_' + rid)
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    n = 0
    with tarfile.open(arch, 'r:gz') as t:
        for mem in t:
            nm = mem.name.replace('\\', '/')
            if nm.endswith('.npy') and ('/raw/' in nm or '/clean/' in nm):
                continue
            if mem.isdir() or not mem.isfile():
                continue
            tgt = (dest / nm).resolve()
            if dest.resolve() not in tgt.parents:
                raise SystemExit('unsafe tar member %s' % nm)
            tgt.parent.mkdir(parents=True, exist_ok=True)
            with t.extractfile(mem) as src, open(tgt, 'wb') as dst:
                shutil.copyfileobj(src, dst)
            n += 1
    rd = dest / rid
    caps = [p for p in (rd / 'capture').iterdir() if p.is_dir()]
    if len(caps) != 1:
        raise SystemExit('expected exactly one capture folder in %s' % (rd / 'capture'))
    return dest, rd, caps[0], n


def recompute_run(rid, scratch, A, PB):
    gc, oc, ox, consumer, finite_primitive = A.gc, A.oc, A.ox, A.consumer, A.finite_primitive
    dest, rd, cap, nfiles = extract_archive(rid, scratch)
    try:
        Lr = A.load_capture(rd, cap)
        T = Lr['T']; draw = Lr['draw']; kmax = Lr['kmax']; contact_k = Lr['contact_k']
        decs = list(gc.decisions(cap))
        nd = len(decs)
        out = {k: np.full(nd, np.nan) for k in ('k', 'status', 'prim', 'bind_ok', 'y_bind', 'cos_phi', 'e_n', 'te', 'y_dec', 'chkF0', 'chkN')}
        for di, (k, dec) in enumerate(decs):
            ms = dec['model_state']; actors = dec['actors']; now = dec['now']
            Lg, Wd = dec['ego_length'], dec['ego_width']; desired = dec['desired_mps']
            diag = consumer.Diagnostics()
            rows = finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], desired, actors, Lg, Wd, now, diag)
            n = len(rows); assert n == 17
            idx55 = next(i for i, x in enumerate(rows) if x['targets'] == (-5., -5.))
            na = len(actors); M = 120 * na
            D = np.stack([x['d'] for x in rows]).reshape(n, M); Pr = np.stack([x['p'] for x in rows]).reshape(n, M)
            # geometry and s_P act row by row; the single row idx55 gives the identical numbers (rows are independent)
            N, TE, MU = gc.geometry([rows[idx55]], actors, now)
            Sbar = gc.s_P(N, TE, [np.array(PB[oc.cls_of(a['name'])], float) for a in actors])
            D1 = D[idx55:idx55 + 1]; Pr1 = Pr[idx55:idx55 + 1]
            cF0 = gc.crit_rows(D1, Sbar)[0]; cN = gc.crit_rows(D1, Pr1)[0]
            out['k'][di] = k; out['chkF0'][di] = cF0; out['chkN'][di] = cN
            with np.errstate(divide='ignore', invalid='ignore'):
                out['y_dec'][di] = 0.5 * np.log(cF0 / cN)
            tr = T.get(k)
            m, prim_t, order = gc.match_many(actors, now, tr)
            status = 3; prim = -1; wt = {}
            if prim_t is not None:
                one, (prim, pd) = oc.match_actors(actors, now, tr, order)
                full = (k + 60 <= kmax)
                trunc_c = (not full) and contact_k >= 0
                status = 0 if full else (1 if trunc_c else 2)
            out['status'][di] = status
            if prim_t is None or prim < 0 or m[prim] is None:
                continue                              # no primary actor: prim, bind_ok and the rest stay NaN
            out['prim'][di] = prim
            blk = slice(120 * prim, 120 * prim + 120)
            Db = D1[0, blk]; Sb = Sbar[0, blk]; Pb = Pr1[0, blk]
            if (Db < 0).any():
                out['bind_ok'][di] = 0; continue
            with np.errstate(divide='ignore', invalid='ignore'):
                ratio = np.where(Sb > 0, Db * Db / np.where(Sb > 0, Sb, 1.0), np.inf)
            j = int(np.argmin(ratio))
            if not np.isfinite(ratio[j]):
                out['bind_ok'][di] = 0; continue
            out['bind_ok'][di] = 1
            with np.errstate(divide='ignore', invalid='ignore'):
                out['y_bind'][di] = 0.5 * np.log(Pb[j] / Sb[j])
            nrm = N[0, 120 * prim + j]
            out['te'][di] = TE[120 * prim + j]
            offset = j // 60; p = offset + (j % 60)
            v = consumer.finite_array([actors[prim][kk] for kk in gc.ACTOR_KEYS])[2:4]
            sp = math.hypot(v[0], v[1])
            out['cos_phi'][di] = (v[0] * nrm[0] + v[1] * nrm[1]) / sp if sp > A.VMIN else np.nan
            wtE = ox.window_truth(T, k, kmax, draw, False)[0]
            cen = gc.planner_centres(tr['ego'], wtE[m[prim]][0])
            e = cen[p] - MU[prim][p]
            out['e_n'][di] = (nrm[0] * e[0] + nrm[1] * e[1]) / math.sqrt(Sb[j])
        out['n_files_extracted'] = nfiles
        return out
    finally:
        shutil.rmtree(dest, ignore_errors=True)


def compare_vec(a, b, mask=None):
    """NaN-pattern and max-abs-difference comparison of recomputed a with stored b (inf compared by sign)."""
    if mask is not None:
        a = a[mask]; b = b[mask]
    na, nb = np.isnan(a), np.isnan(b)
    ia, ib = np.isinf(a), np.isinf(b)
    inf_ok = bool((np.where(ia, np.sign(a), 0) == np.where(ib, np.sign(b), 0)).all())
    both = np.isfinite(a) & np.isfinite(b)
    diff = np.abs(a[both] - b[both])
    return dict(n=int(len(a)), nan_pattern_equal=bool((na == nb).all()), n_nan_pattern_mismatch=int((na != nb).sum()),
                inf_pattern_equal=inf_ok, n_nan_recomputed=int(na.sum()), n_nan_stored=int(nb.sum()), n_compared=int(both.sum()),
                max_abs_diff=float(diff.max()) if diff.size else None, n_exact_equal=int((diff == 0).sum()) if diff.size else 0)


def part2(runs, names, scratch):
    sys.path.insert(0, str(TRACKERS))
    import trk_env_v01
    trk_env_v01.setup()
    import trk_arrays_v01 as A
    pb = json.loads(PBAR_JSON.read_text(encoding='utf-8'))['Pbar']
    PB = {c: np.array(v, float) for c, v in pb.items()}
    byname = {d['_stem']: d for d in runs}
    res = {}
    for rid, roles in names.items():
        t0 = time.time()
        if rid not in byname:
            res[rid] = dict(roles=roles, error='npz not available in in-dir; per-tick check not done')
            continue
        d = byname[rid]
        o = recompute_run(rid, scratch, A, PB)
        r = dict(roles=roles, seconds=time.time() - t0, n_dec_recomputed=int(len(o['k'])), n_dec_npz=int(len(d['k'])),
                 n_files_extracted=o['n_files_extracted'])
        if len(o['k']) != len(d['k']):
            r['error'] = 'tick count differs'; res[rid] = r; continue
        r['k_equal'] = bool(np.array_equal(o['k'], d['k']))
        with np.errstate(invalid='ignore'):
            ev = (d['status'] == 0)
            an = select(d)
        r['status_equal'] = bool(np.array_equal(np.nan_to_num(o['status'], nan=-9), np.nan_to_num(d['status'], nan=-9)))
        r['n_status_mismatch'] = int((np.nan_to_num(o['status'], nan=-9) != np.nan_to_num(d['status'], nan=-9)).sum())
        r['prim'] = compare_vec(o['prim'], d['prim'])
        r['bind_ok'] = compare_vec(o['bind_ok'], d['bind_ok'])
        for key in ('y_bind', 'cos_phi', 'e_n', 'te', 'y_dec', 'chkF0', 'chkN'):
            r[key] = dict(all_ticks=compare_vec(o[key], d[key]),
                          status0_ticks=compare_vec(o[key], d[key], ev),
                          npz_analysed_ticks=compare_vec(o[key], d[key], an))
        # recomputed selection vs stored selection
        o2 = dict(o); o2['_name'] = rid
        with np.errstate(invalid='ignore'):
            mo = (o['status'] == 0) & (o['bind_ok'] == 1) & np.isfinite(o['cos_phi'])
        for key in ('y_bind', 'cos_phi', 'te', 'e_n'):
            mo &= np.isfinite(o[key])
        r['n_analysed_recomputed_partial'] = int(mo.sum()); r['n_analysed_npz_partial'] = int((an & np.isfinite(d['y_bind'])).sum())
        r['recomputed_values_head'] = {key: [None if not np.isfinite(v) else float(v) for v in o[key][:3]] for key in ('y_bind', 'cos_phi', 'e_n', 'te', 'y_dec')}
        res[rid] = r
    return res


# ------------------------------------------------------------------------------------------------ main
def main():
    global B_BOOT
    ap = argparse.ArgumentParser()
    ap.add_argument('--in-dir', default=str(CD / 'crossing' / 'heading'))
    ap.add_argument('--out', default=str(HERE / 'out' / 'RC_X_HEADING_v13.json'))
    ap.add_argument('--scratch', default=str(HERE / 'scratch_rc_x_heading'))
    ap.add_argument('--part2', choices=('auto', 'off'), default='auto')
    ap.add_argument('--part2-runs', default=None, help='comma-separated run stems instead of 0002 / median / last')
    ap.add_argument('--synth-v', action='store_true', help='TEST ONLY: files lack vx/vy; synthesise vx=cos(theta), vy=sin(theta)')
    ap.add_argument('--boot', type=int, default=B_BOOT, help='TEST ONLY: change B')
    a = ap.parse_args()
    B_BOOT = a.boot
    lower_priority()
    out = pathlib.Path(a.out)
    if out.exists():
        raise SystemExit('refusing to overwrite %s' % out)
    out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    runs, synth = load_runs(a.in_dir, a.synth_v)
    stems = [d['_stem'] for d in runs]
    h = hashlib.sha256()
    for d in runs:
        h.update(d['_name'].encode()); h.update(sha256_file(d['_path']).encode())
    res = dict(program='rc_x_heading_v13.py', program_sha256=sha256_file(__file__), spec='recount\\SPEC_RC_X_HEADING_v13.md',
               written_by='Claude Sonnet 5.5, independent second program', exploratory=True,
               in_dir=str(a.in_dir), n_input_files=len(runs), inputs_digest_sha256=h.hexdigest(),
               first_file=stems[0], last_file=stems[-1], synthetic_vx_vy_TEST_ONLY=synth,
               python=sys.version.split()[0], numpy=np.__version__, B=B_BOOT, seed=SEED)
    res['part1'] = part1(runs)
    res['part1_seconds'] = time.time() - t0
    if a.part2 == 'auto':
        if a.part2_runs:
            sel = a.part2_runs.split(',')
            names = {s: ['explicit'] for s in sel}
        else:
            first = 'pc13x_c1109_eval_0002_native'
            med = stems[len(stems) // 2]          # n even: the upper median (0-based index n // 2)
            names = {}
            for role, s in (('first_0002', first), ('median_numbered_index_n//2', med), ('last', stems[-1])):
                names.setdefault(s, []).append(role)
        res['part2_selection'] = dict(runs=names, n_sorted=len(stems), median_rule='sorted list, 0-based index n//2 (upper median for even n); lower median would be index (n-1)//2 = %s' % stems[(len(stems) - 1) // 2])
        res['per_tick_check'] = part2(runs, names, a.scratch)
    res['total_seconds'] = time.time() - t0
    with open(out, 'x', encoding='utf-8') as f:
        json.dump(jnum(res), f, indent=1)
    print('wrote', out)


if __name__ == '__main__':
    main()
