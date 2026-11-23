r"""v13 round 2 (AMENDMENT_12 s3c): IMM mode probabilities by truth phase, descriptive. New file, 22 Nov 2026 (Claude Opus 5.5).
Input: a variant's re-track arrays (<rid>_arrays.npz, written by b_retrack_v01.tracker_record + trk_arrays_v01.extract), which hold the
tracker's mode record (mode_track, mode_frame = detector frame index, mode_stage in birth/update/miss, mode_mu = (mu_CV, mu_CA) after
that step) and per decision k, evaluated, phase (truth phase of record: 0 pre, 1 braking, 2 stopped, 3 none), lead_found and track_id
(the re-tracked lead track).
Per evaluated decision with lead_found and phase in {0, 1, 2}: di = (k - 19) // 10 (the decision's detector frame; 2 Hz rows at ticks
19 + 10 i), mu_CA = the CA probability of the lead track's last mode record with mode_frame <= di. Per phase: mean of mu_CA, median, and
the share with mu_CA > 0.5, pooled over decisions; run-level bootstrap percentile intervals (95 %) on the run set's draw (decisions of a
resampled run enter with its multiplicity).
Run sets: fresh = the 105 fresh C runs (CASES_C_v13 + REPLACEMENTS, ascending), draw optA_lib_v02.boot_counts(105, 20000, 20261911);
          new <runs root> = the A12 s2.4 run ids (b_l12_ids_v02, CD's rule and job map) with LOGS_OK under root, ascending,
          boot_counts(n, 20000, 20261911) (the draw of all A12 s3 analyses).
          old = TEST only: the 35 old evaluation runs p1b_fit_finite_0005..0039 (exploratory data of record), boot_counts(35, 20000,
          20261911); ungated; used to check this program against its second program before the freeze.
REFUSES (fresh, new) unless revision_v13\LOCK_A12a.txt exists. Writes out\modeprob\MODEPROB_<label>_<set>_v01.json.
Usage: python -I -B -X utf8 b_modeprob_v01.py <label> <arrays dir> fresh | new <runs root> | old
"""
import sys, json, pathlib, time, hashlib
import numpy as np
HERE = pathlib.Path(__file__).resolve().parents[1]
WORK = HERE.parent; V13 = WORK.parent; CD = WORK / 'CD_capture'
sys.path.insert(0, r'<library folder>\code')
import optA_lib_v02 as L                        # read-only: boot_counts
LOCK = V13 / 'LOCK_A12a.txt'
PH = {0: 'pre', 1: 'braking', 2: 'stopped'}


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def fresh_ids():
    cases = json.loads((CD / 'CASES_C_v13.json').read_text(encoding='utf-8'))['cases']
    rep = json.loads((CD / 'REPLACEMENTS_C_v13.json').read_text(encoding='utf-8'))['replacements']
    return sorted('pc13_%s_native' % rep.get(c['case'], c['case']) for c in cases if c['family'] == 'lead_braking')


def run_values(z):
    k = z['k']; ev = z['evaluated'].astype(bool); lf = z['lead_found'].astype(bool); ph = z['phase']; tid = z['track_id']
    mt = z['mode_track']; mf = z['mode_frame']; mu = z['mode_mu']
    out = {p: [] for p in PH}
    for i in np.nonzero(ev & lf & (ph <= 2))[0]:
        di = (int(k[i]) - 19) // 10
        sel = np.nonzero((mt == int(tid[i])) & (mf <= di))[0]
        if not sel.size:
            continue
        j = sel[np.argmax(mf[sel] * 10 ** 6 + sel)]          # the last record at the latest frame <= di
        out[int(ph[i])].append(float(mu[j, 1]))
    return {p: np.array(v) for p, v in out.items()}


def summ(vals):
    if not vals.size:
        return dict(n=0, mean=None, median=None, share_gt05=None)
    return dict(n=int(vals.size), mean=float(vals.mean()), median=float(np.median(vals)), share_gt05=float(np.mean(vals > 0.5)))


def main():
    label, adir, rset = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
    if rset != 'old' and not LOCK.is_file():
        raise SystemExit('REFUSED: LOCK_A12a.txt does not exist')
    if rset == 'old':
        ids = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]; seed = 20261911
    elif rset == 'fresh':
        ids = fresh_ids(); seed = 20261911
        assert len(ids) == 105
    else:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import b_l12_ids_v02 as L12          # 22 Nov 00:46: CD layout (job id -> run id map), b_l12_ids_v02
        ids = [r for r in L12.l12_run_ids() if L12.logs_ok(sys.argv[4], r)]; seed = 20261911
    t0 = time.time()
    per = []
    for rid in ids:
        f = adir / ('%s_arrays.npz' % rid)
        if not f.is_file():
            f = adir / ('%s.npz' % rid)
        with np.load(f, allow_pickle=False) as z:
            per.append(run_values(z))
    CNT = L.boot_counts(len(ids), 20000, seed)
    res = {}
    for p, nm in PH.items():
        allv = np.concatenate([r[p] for r in per])
        point = summ(allv)
        bm = []; bmed = []; bsh = []
        for row in CNT:
            v = np.concatenate([np.repeat(r[p], int(c)) for r, c in zip(per, row) if c and r[p].size]) if row.any() else np.array([])
            if v.size:
                bm.append(v.mean()); bmed.append(np.median(v)); bsh.append(np.mean(v > 0.5))
        ci = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))] if len(a) else None   # noqa: E731
        res[nm] = dict(point, mean_ci=ci(bm), median_ci=ci(bmed), share_gt05_ci=ci(bsh), n_resamples=len(bm))
    od = HERE / 'out' / 'modeprob'; od.mkdir(parents=True, exist_ok=True)
    doc = dict(code='b_modeprob_v01.py', label=label, arrays=str(adir), run_set=rset, n_runs=len(ids), seed=seed, nboot=20000,
               lock_sha256=sha(LOCK) if LOCK.is_file() else None, run_ids=ids, by_phase=res, seconds=time.time() - t0, written=time.strftime('%Y-%m-%d %H:%M:%S'))
    (od / ('MODEPROB_%s_%s_v01.json' % (label, rset))).write_text(json.dumps(doc, indent=1), encoding='utf-8')
    print(json.dumps({nm: {k: res[nm][k] for k in ('n', 'mean', 'mean_ci', 'share_gt05')} for nm in res}), flush=True)


if __name__ == '__main__':
    main()
