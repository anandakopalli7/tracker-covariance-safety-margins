"""Package F (revision v13): the pre-Lock-2 platform test of the pod double bootstrap (f16_calib_remote_v01.py). New file, 20 Nov
2026 (Claude Opus 5.5), at the coordinator's request (01:25 EST): the pod must reproduce the laptop's values exactly or within 1e-9.
Run with work\\F_nuscenes\\venv (numba). Jobs go to out\\calib\\test\\; laptop results to out\\calib\\test\\local\\, pod results to
out\\calib\\test\\pod\\.
  design   kind R on the DESIGN split (A10 section 8.6: F0 and E of CANMOT only, the horizon rule's statistic R = D(E, F0)/201),
           clearances in force (v02), at the v02 primary horizon (3 s if none); test sizes n_outer 40, n_inner 200. The single
           bootstrap (default_rng(20261923), 20,000) is also run; its 95% percentile interval must equal F_HORIZON_RULE_v02.json's.
  synth    kind FULL on the recount's SYNTHETIC val arrays (no nuScenes data) through f06_score_v01.HeldOut (clearance of the
           arrays), test sizes n_outer 40, n_inner 60; also f06's own double_bootstrap on the same job as the reference the remote
           reimplementation must equal exactly (laptop).
  local JOB     run f16_calib_remote_v01 on the laptop (seeds 20261913, 20261914; design also --single 20261923 20000).
  compare JOB   pod against laptop: p_lt, p_le, full equal exactly (NaN = NaN), every full_reproduced true, the single bootstrap
                within 1e-9; writes out\\calib\\test\\F_CALIB_PLATFORM_TEST_<JOB>_v01.json.
Usage: venv\\Scripts\\python.exe -I f16_calib_job_v01.py design | synth | local JOB | compare JOB
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import f_common_v01 as FC                    # noqa: E402
import json                                  # noqa: E402
import numpy as np                           # noqa: E402

TD = FC.OUT / 'calib' / 'test'
SEEDS = (20261913, 20261914)


def write_job(job, kind, args1, args2, n, full, n_outer, n_inner, extra):
    TD.mkdir(parents=True, exist_ok=True)
    jf = TD / (job + '.job.npz')
    if jf.exists():
        raise SystemExit('REFUSED: %s exists' % jf)
    arrs = {'a1_%d' % i: x for i, x in enumerate(args1)}
    if args2 is not None:
        arrs.update({'a2_%d' % i: x for i, x in enumerate(args2)})
    np.savez(jf, kind=kind, **arrs)
    meta = dict(job=job, kind=kind, n_run=int(n), full=[float(x) for x in full], n_outer=n_outer, n_inner=n_inner,
                seed_outer=20261912, seeds_inner=list(SEEDS), job_sha256=FC.sha256_file(jf), written=FC.clock(), **extra)
    (TD / (job + '.meta.json')).write_text(FC.jdump(meta), encoding='utf-8')
    print('WROTE', jf, json.dumps(meta)[:400])


def design():
    import f06_score_v01 as S
    hz = json.loads((FC.OUT / 'F_HORIZON_RULE_v02.json').read_text(encoding='utf-8'))
    h = hz['primary_horizon_s'] or 3
    runs = S.load_runs('T1', 'train', h)
    G = S.TS.gridless(runs, ['F0', 'E'])
    ev = S.Evaluator(G, ['F0', 'E'], 0)
    full = ev.run(np.ones((1, len(runs))))['denE'] / S.NLEV
    write_job('design_R', 'R', ev.args, None, len(runs), full, 40, 200,
              dict(split='train (design)', horizon_s=h, clearance=S.clearance_info(), statistic='R = D_gl(E, F0) / 201'))


def synth():
    import f06_score_v01 as S
    SYN = FC.F / 'recount' / 'synth'
    names = {s: sorted(p.stem for p in (SYN / 'arrays_T1' / s).glob('*.npz')) for s in ('train', 'val')}
    for mod in (FC, S.FC):
        mod.CACHE = SYN; mod.splits = lambda: names; mod.require_split = lambda split: None
    S.CLEAR = 'v01'                       # the synthetic arrays' own clearances; this test is of the kernel path only
    S.B_OUT, S.B_IN = 40, 60
    H = S.HeldOut(3)
    full = H.stats(np.ones((1, H.n)))[0][0]
    write_job('synth_full', 'FULL', H.E1[0].args, H.E2[0].args, H.n, full, 40, 60,
              dict(split='SYNTHETIC (recount\\synth, val)', horizon_s=3, statistics=list(S.STATS)))
    ref = {}
    for seed in SEEDS:
        lt, le = S.double_bootstrap(H, full, seed)
        ref['p_lt_%d' % seed] = lt; ref['p_le_%d' % seed] = le
    np.savez(TD / 'synth_full_f06_reference.npz', full=full, **ref)
    print('f06 reference written')


def local(job):
    import f16_calib_remote_v01 as R
    od = TD / 'local'; od.mkdir(parents=True, exist_ok=True)
    R.run(TD, job, list(SEEDS), (20261923, 20000) if job == 'design_R' else None, od)


def same(a, b):
    return bool(np.array_equal(np.asarray(a), np.asarray(b), equal_nan=True))


def compare(job):
    outf = TD / ('F_CALIB_PLATFORM_TEST_%s_v01.json' % job)
    if outf.exists():
        raise SystemExit('REFUSED: %s exists' % outf)
    res = dict(job=job, written=FC.clock(), seeds={}, ok=True)
    for seed in SEEDS:
        a = np.load(TD / 'local' / ('%s_%d.npz' % (job, seed))); b = np.load(TD / 'pod' / ('%s_%d.npz' % (job, seed)))
        r = dict(p_lt_equal=same(a['p_lt'], b['p_lt']), p_le_equal=same(a['p_le'], b['p_le']), full_equal=same(a['full'], b['full']),
                 full_reproduced_laptop=bool(np.all(a['full_reproduced'])), full_reproduced_pod=bool(np.all(b['full_reproduced'])),
                 platform_laptop=str(a['platform']), platform_pod=str(b['platform']),
                 seconds_laptop=float(a['seconds']), seconds_pod=float(b['seconds']))
        if job == 'synth_full':
            f = np.load(TD / 'synth_full_f06_reference.npz')
            r['remote_equals_f06_double_bootstrap'] = same(a['p_lt'], f['p_lt_%d' % seed]) and same(a['p_le'], f['p_le_%d' % seed])
        res['seeds'][seed] = r
        res['ok'] &= all(v for k, v in r.items() if isinstance(v, bool))
    if job == 'design_R':
        a = np.load(TD / 'local' / 'design_R_single.npz'); b = np.load(TD / 'pod' / 'design_R_single.npz')
        d = np.abs(a['S'] - b['S']); d = d[np.isfinite(d)]
        hz = json.loads((FC.OUT / 'F_HORIZON_RULE_v02.json').read_text(encoding='utf-8'))
        meta = json.loads((TD / 'design_R.meta.json').read_text(encoding='utf-8'))
        ci_h = hz['horizons']['%d s' % meta['horizon_s']]['R_gl_pp']['ci']
        import f06_score_v01 as S
        ci_pod = S.L.pct(b['S'][:, 0]); ci_lap = S.L.pct(a['S'][:, 0])
        res['single'] = dict(max_abs_diff=float(d.max()) if d.size else 0., nan_pattern_equal=same(np.isnan(a['S']), np.isnan(b['S'])),
                             ci_laptop=ci_lap, ci_pod=ci_pod, ci_horizon_rule_v02=ci_h,
                             ci_equal_horizon_rule=bool(ci_lap == ci_h and ci_pod == ci_h))
        res['ok'] &= bool(res['single']['max_abs_diff'] <= 1e-9 and res['single']['nan_pattern_equal'] and res['single']['ci_equal_horizon_rule'])
    outf.write_text(FC.jdump(res), encoding='utf-8')
    print(FC.jdump(res))


if __name__ == '__main__':
    m = sys.argv[1]
    FC.require_split('train')
    dict(design=design, synth=synth)[m]() if m in ('design', 'synth') else (local if m == 'local' else compare)(sys.argv[2])
