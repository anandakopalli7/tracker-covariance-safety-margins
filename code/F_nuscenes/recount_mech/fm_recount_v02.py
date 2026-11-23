"""Independent recount of the A12 section 5 real-sensor mechanism check (written from the text of the rule only).

Usage: python -I fm_recount_v02.py train|val T1|IMM [--scenes N] [--no-calib]

v02 changes v01 only in the primary statistic (M.tau, M.tau.ci95, M.p, M.level, M.ci, M.passes): the within-cell tau_b is now taken
over the selected pairs only, i.e. pairs of age>=1.0 s rows with at least one member in-miss or post-miss (no steady-steady pairs;
n0, n1, n2 count selected pairs). This is a train-informed primary declared before any val value. The old all-row primary is kept as
M.all.tau, M.all.tau.ci95, M.all.p. M.tau_pooled and M.twin_mean remain all-row.
"""
import sys
import os
import json
import glob
import time
import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.stats import kendalltau

ROOT = r"ARS_TRIAL\revision_v13"
CACHE = os.path.join(ROOT, "work", "F_nuscenes", "cache")
OUTDIR = os.path.join(ROOT, "work", "F_nuscenes", "recount_mech")
LOCK = os.path.join(ROOT, "LOCK_A12c.txt")

CAT2CLS = {"vehicle.car": "car", "vehicle.truck": "truck", "vehicle.bus.rigid": "bus",
           "vehicle.bus.bendy": "bus", "vehicle.trailer": "trailer"}
SF_THRE = {"car": 0.16, "truck": 0.0, "bus": 0.0, "trailer": 0.1}
GATE = 2.0
MIN_AGE = 1.0
HORIZON = 3.0
HTOL = 0.25
STEADY, IN_MISS, POST_MISS, YOUNG = 0, 1, 2, 3
SNAMES = {"steady": STEADY, "in_miss": IN_MISS, "post_miss": POST_MISS, "young": YOUNG}
# stat columns: 0 primary, then the four strata
COLS = ["primary", "steady", "in_miss", "post_miss", "young"]
NBOOT = 20000


def set_priority():
    try:
        import ctypes
        h = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.kernel32.SetPriorityClass(h, 0x4000)  # BELOW_NORMAL
    except Exception:
        pass


def pair_terms(sig, e, sel=None):
    """Kendall tau_b terms over the pairs i<j (restricted to sel, an m x m boolean) of one cell.
    Returns (numerator C-D, denominator sqrt((n0-n1)(n0-n2)))."""
    m = len(sig)
    if m < 2:
        return 0.0, 0.0
    iu = np.triu_indices(m, 1)
    ds = np.sign(sig[iu[0]] - sig[iu[1]])
    de = np.sign(e[iu[0]] - e[iu[1]])
    if sel is not None:
        k = sel[iu]
        ds = ds[k]
        de = de[k]
    n0 = len(ds)
    if n0 == 0:
        return 0.0, 0.0
    num = float(np.sum(ds * de))
    n1 = int(np.sum(ds == 0))
    n2 = int(np.sum(de == 0))
    den = float(np.sqrt(float(n0 - n1) * float(n0 - n2)))
    return num, den


def load_scene(split, name, tracker):
    d = np.load(os.path.join(CACHE, split, name + ".npz"), allow_pickle=True)
    t = np.load(os.path.join(CACHE, "tracks_" + tracker, split, name + ".npz"), allow_pickle=True)
    return d, t


def scene_rows(d, t):
    """Build the rows of one scene. Returns dict of arrays (sorted by keyframe then track id)."""
    kf_t = d["kf_t"]
    ann_kf = d["ann_kf"]
    ann_inst = d["ann_inst"]
    ann_xyz = d["ann_xyz"]
    ann_cls = np.array([CAT2CLS.get(c, "") for c in d["ann_cat"]])
    det_kf = d["det_kf"]
    det_xy = d["det_xyz"][:, :2]
    det_name = d["det_name"]
    det_score = d["det_score"]

    # annotation lookups
    ann_by_kf = {}
    inst_at = {}
    for i in range(len(ann_kf)):
        if ann_cls[i] == "":
            continue
        ann_by_kf.setdefault(int(ann_kf[i]), []).append(i)
        inst_at[(int(ann_inst[i]), int(ann_kf[i]))] = i
    det_by_kf = {}
    for k in np.unique(det_kf):
        det_by_kf[int(k)] = np.nonzero(det_kf == k)[0]

    miss_cache = {}

    def missed(inst, k):
        key = (inst, k)
        if key in miss_cache:
            return miss_cache[key]
        ai = inst_at.get(key)
        if ai is None:
            r = False  # not annotated at k: not a real missed detection
        else:
            cls = ann_cls[ai]
            r = True
            di = det_by_kf.get(k)
            if di is not None and len(di):
                ok = (det_name[di] == cls) & (det_score[di] >= SF_THRE[cls])
                if ok.any():
                    dd = np.hypot(det_xy[di[ok], 0] - ann_xyz[ai, 0], det_xy[di[ok], 1] - ann_xyz[ai, 1])
                    if (dd <= GATE).any():
                        r = False
        miss_cache[key] = r
        return r

    trk_kf = t["trk_kf"]
    trk_id = t["trk_id"]
    trk_name = t["trk_name"]
    trk_center = t["trk_center"]
    trk_vel = t["trk_vel"]
    trk_P = t["trk_P"]
    trk_st = t["trk_state_time"]

    # first output keyframe time per track id
    first_t = {}
    for i in range(len(trk_id)):
        tid = int(trk_id[i])
        tt = kf_t[int(trk_kf[i])]
        if tid not in first_t or tt < first_t[tid]:
            first_t[tid] = tt

    out = {"kf": [], "tid": [], "sigma": [], "e": [], "age": [], "stratum": []}
    veh = np.isin(trk_name, list(SF_THRE.keys()))
    nneg = 0
    for k in np.unique(trk_kf):
        k = int(k)
        tk = kf_t[k]
        # horizon keyframe
        u = int(np.argmin(np.abs(kf_t - (tk + HORIZON))))
        if abs(kf_t[u] - tk - HORIZON) > HTOL:
            continue
        ridx = np.nonzero((trk_kf == k) & veh)[0]
        aidx_all = ann_by_kf.get(k, [])
        if len(ridx) == 0 or len(aidx_all) == 0:
            continue
        for cls in SF_THRE:
            r = ridx[trk_name[ridx] == cls]
            a = np.array([i for i in aidx_all if ann_cls[i] == cls], dtype=int)
            if len(r) == 0 or len(a) == 0:
                continue
            dist = np.hypot(trk_center[r, 0][:, None] - ann_xyz[a, 0][None, :],
                            trk_center[r, 1][:, None] - ann_xyz[a, 1][None, :])
            cost = np.where(dist <= GATE, dist, 1e6)
            ri, ci = linear_sum_assignment(cost)
            for x, y in zip(ri, ci):
                if dist[x, y] > GATE:
                    continue
                row = r[x]
                ai = a[y]
                inst = int(ann_inst[ai])
                ui = inst_at.get((inst, u))
                if ui is None:
                    continue
                delta = kf_t[u] - trk_st[row]
                e = float(np.hypot(*(trk_center[row, :2] + trk_vel[row] * delta - ann_xyz[ui, :2])))
                P = trk_P[row]
                idx = [0, 1, 6, 7]
                Pb = P[np.ix_(idx, idx)]
                Ppp = Pb[:2, :2]
                Ppv = Pb[:2, 2:]
                Pvp = Pb[2:, :2]
                Pvv = Pb[2:, 2:]
                M = Ppp + delta * (Ppv + Pvp) + delta * delta * Pvv
                v = float(np.trace(M))
                if v < 0:
                    nneg += 1
                sigma = float(np.sqrt(v)) if v >= 0 else float("nan")
                age = tk - first_t[int(trk_id[row])]
                if age < MIN_AGE:
                    s = YOUNG
                elif missed(inst, k):
                    s = IN_MISS
                elif missed(inst, k - 1) or missed(inst, k - 2):
                    s = POST_MISS
                else:
                    s = STEADY
                out["kf"].append(k)
                out["tid"].append(int(trk_id[row]))
                out["sigma"].append(sigma)
                out["e"].append(e)
                out["age"].append(age)
                out["stratum"].append(s)
    arr = {kk: np.array(v) for kk, v in out.items()}
    if len(arr["kf"]):
        o = np.lexsort((arr["tid"], arr["kf"]))
        arr = {kk: v[o] for kk, v in arr.items()}
    arr["n_neg_var"] = nneg
    return arr


def scene_terms(rows):
    """Per-scene numerators and denominators for the 5 stat columns, plus cells for later use."""
    num = np.zeros(6)
    den = np.zeros(6)
    kf = rows["kf"]
    cells = []  # primary-row cells for the twin: (sigma, e)
    if len(kf) == 0:
        return num, den, cells
    for k in np.unique(kf):
        c = kf == k
        sig = rows["sigma"][c]
        e = rows["e"][c]
        st = rows["stratum"][c]
        age = rows["age"][c]
        prim = age >= MIN_AGE
        # primary rows are those not young (age >= 1.0 s)
        sp, ep, stp = sig[prim], e[prim], st[prim]
        if len(sp) >= 1:
            cells.append((sp.copy(), ep.copy()))
        n_, d_ = pair_terms(sp, ep)
        num[5] += n_
        den[5] += d_
        mnp = stp != STEADY
        n_, d_ = pair_terms(sp, ep, mnp[:, None] | mnp[None, :])
        num[0] += n_
        den[0] += d_
        # steady: pairs of two steady rows
        ms = stp == STEADY
        n_, d_ = pair_terms(sp, ep, np.outer(ms, ms))
        num[1] += n_
        den[1] += d_
        for col, code in ((2, IN_MISS), (3, POST_MISS)):
            mm = stp == code
            sel = mm[:, None] | mm[None, :]
            n_, d_ = pair_terms(sp, ep, sel)
            num[col] += n_
            den[col] += d_
        # young: all rows of the cell, pairs with at least one young member
        my = st == YOUNG
        sel = my[:, None] | my[None, :]
        n_, d_ = pair_terms(sig, e, sel)
        num[4] += n_
        den[4] += d_
    return num, den, cells


def boot_weights_tau(A, B, idx_chunk_rows=1000):
    """tau*_b = sum_s w_s A_s / sum_s w_s B_s for the 20000 scene resamples."""
    S = A.shape[0]
    idx = np.random.default_rng(20261951).integers(0, S, (NBOOT, S))
    AB = np.concatenate([A, B], axis=1)
    ncol = A.shape[1]
    res = np.empty((NBOOT, ncol))
    for s0 in range(0, NBOOT, idx_chunk_rows):
        ch = idx[s0:s0 + idx_chunk_rows]
        n = len(ch)
        flat = (ch + (np.arange(n) * S)[:, None]).ravel()
        w = np.bincount(flat, minlength=n * S).reshape(n, S).astype(float)
        sums = w @ AB
        with np.errstate(invalid="ignore", divide="ignore"):
            r = sums[:, :ncol] / sums[:, ncol:]
        r[sums[:, ncol:] == 0] = np.nan
        res[s0:s0 + n] = r
    del idx
    return res


LEVELS = np.round(0.95 + 0.0005 * np.arange(100), 4)


def calibrate(A, B, tau_full, tag=""):
    """Double bootstrap on the primary statistic; returns (level, info)."""
    S = A.shape[0]
    a = A[:, 0]
    b = B[:, 0]
    outer = np.random.default_rng(20261912).integers(0, S, (2000, S))
    res = {}
    for s_in in (20261913, 20261914):
        g = np.random.default_rng(s_in)
        p_lt = np.full(2000, np.nan)
        p_le = np.full(2000, np.nan)
        for bi in range(2000):
            o = outer[bi]
            j = g.integers(0, S, (1000, S))
            sc = o[j]
            flat = (sc + (np.arange(1000) * S)[:, None]).ravel()
            w = np.bincount(flat, minlength=1000 * S).reshape(1000, S).astype(float)
            sa = w @ a
            sb = w @ b
            with np.errstate(invalid="ignore", divide="ignore"):
                v = sa / sb
            v = v[(sb != 0) & np.isfinite(v)]
            if len(v):
                p_lt[bi] = np.mean(v < tau_full)
                p_le[bi] = np.mean(v <= tau_full)
        res[s_in] = (p_lt, p_le)
        print("calibration inner seed", s_in, "done", flush=True)

    def cover_matrix(p_lt, p_le):
        fin = np.isfinite(p_lt)
        C = np.zeros((2000, len(LEVELS)), dtype=bool)
        for li, lev in enumerate(LEVELS):
            al = 1.0 - lev
            with np.errstate(invalid="ignore"):
                C[:, li] = (p_le >= al / 2 - 1e-12) & (p_lt <= 1 - al / 2 + 1e-12)
        C &= fin[:, None]
        return C, fin

    C1, F1 = cover_matrix(*res[20261913])
    C2, F2 = cover_matrix(*res[20261914])
    cov1 = C1.sum(0) / F1.sum()
    cov2 = C2.sum(0) / F2.sum()

    def smallest(cov):
        ok = np.nonzero(cov >= 0.95)[0]
        return float(LEVELS[ok[0]]) if len(ok) else 1.0

    lev1 = smallest(cov1)
    lev2 = smallest(cov2)
    info = {"cov1_at_0.95": float(cov1[0]), "lev1": lev1, "lev2": lev2}
    if cov1[0] >= 0.94:
        level = 0.95
        info["branch"] = "nominal"
    else:
        # Monte Carlo SD: validity (finite p_lt) applied inside each resample; no nominal branch
        ridx = np.random.default_rng(20261920).integers(0, 2000, (2000, 2000))
        flat = (ridx + (np.arange(2000) * 2000)[:, None]).ravel()
        W = np.bincount(flat, minlength=2000 * 2000).reshape(2000, 2000).astype(float)
        num = W @ C1.astype(float)
        dn = W @ F1.astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            covr = num / dn[:, None]
        levs = np.array([smallest(covr[r]) for r in range(2000)])
        sd = float(np.std(levs, ddof=1))
        info["mc_sd"] = sd
        has = bool(np.any(cov1 >= 0.95))
        if has and sd <= 0.002 and abs(lev2 - lev1) <= 0.002 + 1e-12:
            level = lev1
            info["branch"] = "chosen"
        else:
            level = 0.99
            info["branch"] = "fallback_0.99"
    return level, info


def main():
    args = sys.argv[1:]
    if len(args) < 2 or args[0] not in ("train", "val") or args[1] not in ("T1", "IMM"):
        print(__doc__)
        sys.exit(2)
    split, tracker = args[0], args[1]
    nscenes = None
    if "--scenes" in args:
        nscenes = int(args[args.index("--scenes") + 1])
    no_calib = "--no-calib" in args
    if split == "val" and not os.path.exists(LOCK):
        print("refusing: LOCK_A12c.txt does not exist")
        sys.exit(3)
    name = "MECH_RECOUNT_%s_%s_v02%s.json" % (split, tracker, ("_first%d" % nscenes) if nscenes else "")
    outp = os.path.join(OUTDIR, name)
    if os.path.exists(outp):
        print("refusing to overwrite", outp)
        sys.exit(4)
    set_priority()
    t0 = time.time()
    scenes = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(CACHE, split, "*.npz")))
    if nscenes:
        scenes = scenes[:nscenes]
    S = len(scenes)
    A = np.zeros((S, 6))
    B = np.zeros((S, 6))
    all_cells = []  # per scene list of cells
    sums = {c: 0.0 for c in SNAMES}
    sig_sum = {c: 0.0 for c in SNAMES}
    e_sum = {c: 0.0 for c in SNAMES}
    cnt = {c: 0 for c in SNAMES}
    prim_sig, prim_e = [], []
    nneg = 0
    nnan = 0
    for si, sc in enumerate(scenes):
        d, t = load_scene(split, sc, tracker)
        rows = scene_rows(d, t)
        nneg += rows["n_neg_var"]
        if len(rows["kf"]):
            nnan += int(np.sum(~np.isfinite(rows["sigma"]) | ~np.isfinite(rows["e"])))
            for nm, code in SNAMES.items():
                m = rows["stratum"] == code
                cnt[nm] += int(m.sum())
                sig_sum[nm] += float(np.sum(rows["sigma"][m]))
                e_sum[nm] += float(np.sum(rows["e"][m]))
            pm = rows["age"] >= MIN_AGE
            prim_sig.append(rows["sigma"][pm])
            prim_e.append(rows["e"][pm])
        num, den, cells = scene_terms(rows)
        A[si] = num
        B[si] = den
        all_cells.append(cells)
        if (si + 1) % 50 == 0:
            print("scene", si + 1, "/", S, "%.0fs" % (time.time() - t0), flush=True)

    # point estimates
    with np.errstate(invalid="ignore", divide="ignore"):
        tau_all = A.sum(0) / B.sum(0)
    tau_boot = boot_weights_tau(A, B)
    ci = np.nanpercentile(tau_boot, [2.5, 97.5], axis=0)
    p_m1 = (1 + int(np.sum(tau_boot[:, 0] <= 0))) / (NBOOT + 1)
    ps = np.concatenate(prim_sig) if prim_sig else np.array([])
    pe = np.concatenate(prim_e) if prim_e else np.array([])
    tau_pooled = float(kendalltau(ps, pe).statistic)

    # twin
    rng = np.random.default_rng(20261952)
    twin = []
    iu_cache = {}
    sgn_e = []
    # precompute per-scene, per-cell e sign vectors
    pre = []
    for cells in all_cells:
        pc = []
        for sp, ep in cells:
            m = len(sp)
            if m not in iu_cache:
                iu_cache[m] = np.triu_indices(m, 1)
            iu = iu_cache[m]
            de = np.sign(ep[iu[0]] - ep[iu[1]])
            pc.append((m, iu, de, int(np.sum(de == 0))))
        pre.append(pc)
    for k in range(20):
        nn = 0.0
        dd = 0.0
        for si in range(S):
            for (sp, ep), (m, iu, de, n2) in zip(all_cells[si], pre[si]):
                perm = rng.permutation(m)
                if m < 2:
                    continue
                sq = sp[perm]
                ds = np.sign(sq[iu[0]] - sq[iu[1]])
                n0 = len(ds)
                n1 = int(np.sum(ds == 0))
                nn += float(np.sum(ds * de))
                dd += float(np.sqrt(float(n0 - n1) * float(n0 - n2)))
        twin.append(nn / dd if dd > 0 else float("nan"))
    twin_mean = float(np.nanmean(twin))

    def f(x):
        x = float(x)
        return x if np.isfinite(x) else None

    vals = {}
    vals["M.n_scenes"] = S
    vals["M.tau"] = f(tau_all[0])
    vals["M.tau.ci95"] = [f(ci[0, 0]), f(ci[1, 0])]
    vals["M.p"] = p_m1
    vals["M.all.tau"] = f(tau_all[5])
    vals["M.all.tau.ci95"] = [f(ci[0, 5]), f(ci[1, 5])]
    vals["M.all.p"] = (1 + int(np.sum(tau_boot[:, 5] <= 0))) / (NBOOT + 1)
    vals["M.tau_pooled"] = f(tau_pooled)
    vals["M.twin_mean"] = f(twin_mean)
    for ci_, nm in enumerate(["steady", "in_miss", "post_miss", "young"], start=1):
        vals["M.n_rows.%s" % nm] = cnt[nm]
        vals["M.s.%s.tau" % nm] = f(tau_all[ci_])
        vals["M.s.%s.ci95" % nm] = [f(ci[0, ci_]), f(ci[1, ci_])]
        vals["M.s.%s.mean_s" % nm] = f(sig_sum[nm] / cnt[nm]) if cnt[nm] else None
        vals["M.s.%s.mean_e" % nm] = f(e_sum[nm] / cnt[nm]) if cnt[nm] else None
    extra = {"n_negative_variance_rows": nneg, "n_nonfinite_rows": nnan,
             "twin_taus": [f(x) for x in twin]}
    if split == "val" and not no_calib:
        level, info = calibrate(A, B, float(tau_all[0]))
        lo, hi = np.nanpercentile(tau_boot[:, 0], [100 * (1 - level) / 2, 100 - 100 * (1 - level) / 2])
        vals["M.level"] = level
        vals["M.ci"] = [f(lo), f(hi)]
        vals["M.passes"] = bool(lo > 0)
        extra["calibration"] = info
    elif split == "train":
        print("note: calibration is val only; not run on train")
    out = {"program": "fm_recount_v02.py", "split": split, "tracker": tracker, "scenes_used": nscenes,
           "values": vals, "diagnostics": extra, "seconds": time.time() - t0}
    with open(outp, "x") as fh:
        json.dump(out, fh, indent=1)
    for k_, v_ in vals.items():
        print(k_, v_)
    print("diagnostics", extra["n_negative_variance_rows"], extra["n_nonfinite_rows"])
    print("wrote", outp)


if __name__ == "__main__":
    main()
