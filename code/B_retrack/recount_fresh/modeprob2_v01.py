"""IMM mode probabilities by truth phase (descriptive), second program.  Spec: A12_3c_IMM2_v02.md, "Mode probabilities by truth phase".
Usage (python -I -B -X utf8 modeprob2_v01.py <label> <arrays dir> old | fresh | new <runs root>):
  old    TEST mode: 35 runs p1b_fit_finite_0005..0039, files <arrays dir>\\<run>_arrays.npz; ungated
  fresh  105 fresh C runs (ids RF.fresh_run_ids()); gated (LOCK_A10_2, LOCK_A10_2c, LOCK_A11, LOCK_A12a)
  new    new runs (ids as in imm2_v04.new_run_ids with <runs root>); gated
Output out\\MODEPROB2_<label>_<set>_v01.json: per phase (pre, braking, stopped): n, mean, median, share_gt05, *_ci (run-level percentile
[2.5, 97.5], draw optA_lib_v02.boot_counts(n_runs, 20000, 20261911), a resampled run contributing its decisions with its multiplicity).
Decision: evaluated, lead_found, phase in {0,1,2}; detector frame index (k-19)//10; mu_CA = mode_mu[:,1] of the last-in-file record with
mode_track == track_id and the largest mode_frame <= that index; decisions with no such record are skipped.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
if sys.platform == 'win32':
    import ctypes
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
import numpy as np
import recount_fresh as RF
import imm2_v04 as I2
import rf_core
L = rf_core.L

PH = ['pre', 'braking', 'stopped']
SEED, NB = 20261911, 20000


def decisions(path):
    q = np.load(path, allow_pickle=True)
    k = q['k']; ev = q['evaluated'].astype(bool); ph = q['phase']; lf = q['lead_found'].astype(bool)
    tid = q['track_id']; mt = q['mode_track']; mf = q['mode_frame']; mu = q['mode_mu']
    sel = ev & lf & np.isin(ph, [0, 1, 2])
    out_mu, out_ph = [], []
    for i in np.nonzero(sel)[0]:
        fi = (int(k[i]) - 19) // 10
        ok = np.nonzero((mt == tid[i]) & (mf <= fi))[0]
        if not ok.size:
            continue
        fm = mf[ok].max()
        j = ok[mf[ok] == fm][-1]          # last in file order among records of the largest frame
        out_mu.append(float(mu[j, 1])); out_ph.append(int(ph[i]))
    return np.array(out_mu), np.array(out_ph, dtype=int)


def wmedian(mu_sorted, cs):
    """median of the expanded sample (numpy convention: mean of elements at 0-based positions (W-1)//2 and W//2); cs = cumulative weights."""
    W = cs[:, -1]
    lo = (W - 1) // 2; hi = W // 2
    ilo = (cs > lo[:, None]).argmax(axis=1); ihi = (cs > hi[:, None]).argmax(axis=1)
    m = 0.5 * (mu_sorted[ilo] + mu_sorted[ihi])
    return np.where(W > 0, m, np.nan)


def summarize(mus, phs, runids, cnt):
    res = {}
    nrun = cnt.shape[1]
    for p, name in enumerate(PH):
        parts = [(r, mus[r][phs[r] == p]) for r in range(nrun)]
        mu = np.concatenate([x for _, x in parts]) if parts else np.array([])
        run_of = np.concatenate([np.full(len(x), r) for r, x in parts])
        n = int(mu.size)
        if n == 0:
            res[name] = dict(n=0, mean=None, median=None, share_gt05=None, mean_ci=None, median_ci=None, share_gt05_ci=None)
            continue
        o = np.argsort(mu, kind='stable')
        mus_ = mu[o]; ro = run_of[o]
        gt = (mus_ > 0.5).astype(float)
        M, Md, S = [], [], []
        for b0 in range(0, cnt.shape[0], 500):
            w = cnt[b0:b0 + 500][:, ro]                 # (chunk, n) multiplicities, in sorted order
            W = w.sum(axis=1)
            with np.errstate(invalid='ignore', divide='ignore'):
                M.append((w @ mus_) / W)
                S.append((w @ gt) / W)
            Md.append(wmedian(mus_, np.cumsum(w, axis=1)))
        ci = lambda a: [float(v) for v in np.nanpercentile(np.concatenate(a), [2.5, 97.5])]
        res[name] = dict(n=n, mean=float(mu.mean()), median=float(np.median(mu)), share_gt05=float((mu > 0.5).mean()),
                         mean_ci=ci(M), median_ci=ci(Md), share_gt05_ci=ci(S))
    return res


def main():
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    label, adir, kind = sys.argv[1], sys.argv[2], sys.argv[3]
    if kind == 'old':
        ids = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
    elif kind in ('fresh', 'new'):
        I2.check_locks4()
        if kind == 'fresh':
            ids = RF.fresh_run_ids()
        else:
            if len(sys.argv) < 5:
                raise SystemExit('new needs <runs root>')
            ids = I2.new_run_ids(sys.argv[4])
    else:
        raise SystemExit('set must be old, fresh or new')
    mus, phs = [], []
    for r in ids:
        m, p = decisions(adir + '\\' + r + '_arrays.npz')
        mus.append(m); phs.append(p)
    cnt = L.boot_counts(len(ids), NB, SEED)
    res = summarize(mus, phs, ids, cnt)
    res['_meta'] = dict(label=label, set=kind, n_runs=len(ids), n_resamples=NB, seed=SEED, arrays_dir=adir)
    out = RF.OUTD + r'\MODEPROB2_%s_%s_v01.json' % (label, kind)
    if os.path.exists(out):
        raise SystemExit('REFUSED: would overwrite ' + out)
    os.makedirs(RF.OUTD, exist_ok=True)
    json.dump(res, open(out, 'w'), indent=1)
    print(out)
    for name in PH:
        print(name, json.dumps(res[name]))


if __name__ == '__main__':
    main()
