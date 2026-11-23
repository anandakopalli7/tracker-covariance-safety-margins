"""Crossing: margin ratio against heading and realised error, per decision tick (EXPLORATORY; coordinator's A12 task 4; sprint panel
item E4 and wording S4, R2 F1). First program. New file, 22 Nov 2026 (Claude Opus 5.5, session CD), written after the X analysis of
record; it tests nothing and changes no value of record.

Runs: the 390 X study runs (CASES_X_PC_v13.json with REPLACEMENTS_X_v13.json; the three retry runs read from their capture id as in
out/ALIAS_RETRIES_X_v13.json). Per run, the archive is checked against its receipt and its logs are extracted to tmp_heading/ with
crossing/x_extract_v13.extract_logs (frozen in add3), used and deleted.

Per decision tick (all ticks; the analysis selects), with the modules of record exactly as trk_arrays_v01.extract (package B, frozen):
library rows, D, Pr (the actor's own P), the normals N, look-ahead TE and predicted centres MU (ol_gateR_core_v01.geometry), Sbar (class
P-bar of record), cF0 and cN. Check: cF0 and cN at row idx55 must equal the stored arrays of record (arrays_x/CV0) bit for bit.
For the PRIMARY actor (olcore_v01.match_actors) at row idx55 (targets (-5, -5)), its 120 constraints only:
  j*       = argmin_j D_j^2 / Sbar_j (the constraint that binds the class margin F0 for this actor; undefined if any D_j < 0)
  y_bind   = 0.5 ln(Pr_j* / Sbar_j*)            the covariance margin relative to the class margin at that constraint
  cos_phi  = (v_hat . n_j*) / |v_hat|           v_hat the tracker's velocity estimate (planner frame); NaN when |v_hat| <= 0.5 m/s
  e_n      = (n_j* . (truth centre - MU)) / sqrt(Sbar_j*)   the realised error along the normal, in class-margin units
             (truth centres as trk_arrays_v01 builds cE: ox.window_truth(..., False), gc.planner_centres)
  te, offset, |v_hat|, age (s since the state time), book.features (updates of age, misses since the last detection), the actor's
  4x4 P and its class P-bar (for the object-frame check), v_hat (vx, vy), y_dec = 0.5 ln(cF0/cN) at row idx55.
Writes crossing/heading/<job id>.npz (never overwritten) and crossing/heading/X_HEADING_EXTRACT_<time>.json.
Usage: python -I -B x_heading_v13.py [--workers 2] [--limit N]
"""
import argparse, hashlib, json, math, os, pathlib, shutil, sys, time
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent; CD = HERE.parent
sys.path.insert(0, str(HERE))
import x_extract_v13 as XE                 # noqa: E402  (frozen in add3: extract_logs, run_paths, PBAR_RECORD, below_normal, sha)
ARCH = CD / 'archives'; TMP = CD / 'tmp_heading'; OUT = HERE / 'heading'; STORED = CD / 'arrays_x' / 'CV0'
CASES_SHA = '58902be5ce022b314148308140cb8fc9373bc7aee401531367d456755409a31e'
NAMES = ('k', 'status', 'prim', 'bind_ok', 'y_bind', 'cos_phi', 'speed', 'e_n', 'te', 'offset', 'age_s', 'age_upd', 'miss', 'y_dec',
         'chkF0', 'chkN', 'vx', 'vy')


def run_list():
    cf = HERE / 'CASES_X_PC_v13.json'
    if XE.sha(cf) != CASES_SHA: raise SystemExit('REFUSED: CASES_X_PC_v13.json differs')
    X = json.loads(cf.read_text(encoding='utf-8'))
    rep = json.loads((HERE / 'REPLACEMENTS_X_v13.json').read_text(encoding='utf-8'))['replacements']
    ali = {a['job']: a['capture_run_id'] for a in json.loads((HERE / 'out' / 'ALIAS_RETRIES_X_v13.json').read_text(encoding='utf-8'))['aliases']}
    jobs = sorted('pc13x_%s_native' % rep.get(r['case'], r['case']) for r in X['cases'] if not r['reserve'])
    assert len(jobs) == 390 == len(set(jobs))
    return [(j, ali.get(j, j)) for j in jobs]


def per_tick(rd, cap, PB):
    import numpy as np
    import trk_env_v01 as env; env.setup()
    import trk_arrays_v01 as A
    gc, oc, ox, consumer, fp = A.gc, A.oc, A.ox, A.consumer, A.finite_primitive
    Lr = A.load_capture(rd, cap)
    T = Lr['T']; book = Lr['book']; draw = Lr['draw']; kmax = Lr['kmax']; contact_k = Lr['contact_k']
    decs = list(gc.decisions(cap)); nd = len(decs)
    F = {n: np.full(nd, np.nan) for n in NAMES}
    Pm = np.full((nd, 4, 4), np.nan); Pb = np.full((nd, 4, 4), np.nan)
    for di, (k, dec) in enumerate(decs):
        ms = dec['model_state']; actors = dec['actors']; now = dec['now']
        Lg, Wd = dec['ego_length'], dec['ego_width']; desired = dec['desired_mps']
        diag = consumer.Diagnostics()
        rows = fp.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], desired, actors, Lg, Wd, now, diag)
        n = len(rows); assert n == 17
        idx55 = next(i for i, x in enumerate(rows) if x['targets'] == (-5., -5.))
        na = len(actors); M = 120 * na
        D = np.stack([x['d'] for x in rows]).reshape(n, M); Pr = np.stack([x['p'] for x in rows]).reshape(n, M)
        N, TE, MU = gc.geometry(rows, actors, now)
        PBs = [np.array(PB[oc.cls_of(a['name'])], float) for a in actors]
        Sbar = gc.s_P(N, TE, PBs)
        cF0 = gc.crit_rows(D, Sbar); cN = gc.crit_rows(D, Pr)
        F['k'][di] = k; F['chkF0'][di] = cF0[idx55]; F['chkN'][di] = cN[idx55]
        with np.errstate(divide='ignore', invalid='ignore'):
            F['y_dec'][di] = 0.5 * np.log(cF0[idx55] / cN[idx55])
        tr = T.get(k)
        m, prim, order = gc.match_many(actors, now, tr)
        full = (k + 60 <= kmax)
        F['status'][di] = 3 if prim is None else (0 if full else (1 if contact_k >= 0 else 2))
        if prim is None: continue
        _, (pi, _) = oc.match_actors(actors, now, tr, order)
        if pi is None or pi < 0 or m[pi] is None: continue
        F['prim'][di] = pi
        a = actors[pi]; blk = slice(120 * pi, 120 * pi + 120)
        d = D[idx55, blk]; sb_ = Sbar[idx55, blk]; pr = Pr[idx55, blk]
        Pm[di] = np.asarray(a['P'], float); Pb[di] = PBs[pi]
        vals = consumer.finite_array([a[kk] for kk in gc.ACTOR_KEYS]); vel = np.asarray(vals[2:4], float)
        sp = math.hypot(vel[0], vel[1]); F['speed'][di] = sp; F['vx'][di] = vel[0]; F['vy'][di] = vel[1]
        F['age_s'][di] = now - a['state_time']
        ag, mb = book.features(int(a['track_id']), a['state_time']); F['age_upd'][di] = ag; F['miss'][di] = mb
        if (d < 0).any(): F['bind_ok'][di] = 0; continue
        with np.errstate(divide='ignore', invalid='ignore'):
            rat = np.where(sb_ > 0, d * d / np.where(sb_ > 0, sb_, 1.), np.inf)
        j = int(np.argmin(rat))
        if not np.isfinite(rat[j]) or not (pr[j] > 0): F['bind_ok'][di] = 0; continue
        F['bind_ok'][di] = 1
        off, jj = divmod(j, 60)
        nrm = N[idx55, 120 * pi + j]
        wtE = ox.window_truth(T, k, kmax, draw, False)[0]
        c = gc.planner_centres(tr['ego'], wtE[m[pi]][0])
        e = c[off + jj] - MU[pi][off + jj]
        F['y_bind'][di] = 0.5 * math.log(pr[j] / sb_[j])
        F['e_n'][di] = float(nrm[0] * e[0] + nrm[1] * e[1]) / math.sqrt(sb_[j])
        F['te'][di] = TE[120 * pi + j]; F['offset'][di] = off
        if sp > A.VMIN: F['cos_phi'][di] = float(vel[0] * nrm[0] + vel[1] * nrm[1]) / sp
    return F, Pm, Pb


def one(job):
    rid, cid = job
    XE.below_normal()
    import numpy as np
    outf = OUT / (rid + '.npz')
    if outf.is_file(): return rid, 'exists'
    t0 = time.time()
    try:
        dest = XE.extract_logs(ARCH, cid, TMP)
        rd, cap = XE.run_paths(dest, cid)
        PB = json.loads(XE.PBAR_RECORD.read_text(encoding='utf-8'))['Pbar']
        F, Pm, Pb = per_tick(rd, cap, PB)
        st = np.load(STORED / (rid + '.npz'), allow_pickle=False)
        i55 = st['idx55']; kk = st['k']
        assert np.array_equal(kk, F['k'].astype(np.int64)), 'ticks differ from the stored arrays'
        sF = st['cF0'][np.arange(len(kk)), i55]; sN = st['cN'][np.arange(len(kk)), i55]
        same = bool(np.array_equal(sF, F['chkF0'], equal_nan=True) and np.array_equal(sN, F['chkN'], equal_nan=True))
        if not same: raise RuntimeError('cF0/cN at idx55 differ from the stored arrays of record')
        meta = dict(run_id=rid, capture_run_id=cid, desired=float(json.loads(str(st['meta']))['desired']), check_cF0_cN_idx55_identical=same,
                    code='x_heading_v13.py', code_sha256=XE.sha(__file__), seconds=time.time() - t0)
        OUT.mkdir(exist_ok=True)
        tmp = outf.with_suffix('.partial.npz')
        np.savez_compressed(tmp, meta=json.dumps(meta), P=Pm, Pbar=Pb, evaluated=st['evaluated'], prim_idx=st['prim_idx'], **F)
        os.replace(tmp, outf)
        return rid, 'ok %.0f s' % (time.time() - t0)
    except Exception as ex:                      # noqa: BLE001  (reported per run; the run is not used)
        return rid, 'ERROR %s: %s' % (type(ex).__name__, str(ex)[:300])
    finally:
        shutil.rmtree(TMP / cid, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=2); ap.add_argument('--limit', type=int)
    a = ap.parse_args()
    XE.below_normal()
    jobs = run_list()[:a.limit] if a.limit else run_list()
    from concurrent.futures import ProcessPoolExecutor
    t0 = time.time(); log = []
    with ProcessPoolExecutor(a.workers) as ex:
        for rid, res in ex.map(one, jobs):
            log.append(dict(run=rid, res=res)); print('[%5.0f s] %s %s' % (time.time() - t0, rid, res), flush=True)
    OUT.mkdir(exist_ok=True)
    (OUT / f'X_HEADING_EXTRACT_{time.strftime("%Y%m%dT%H%M%S")}.json').write_text(
        json.dumps(dict(code_sha256=XE.sha(__file__), n=len(log), errors=sum('ERROR' in r['res'] for r in log), runs=log,
                        seconds=time.time() - t0), indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
