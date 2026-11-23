"""Recount (second program) of package CD, revision v13: B7, rate x latency (A10 section 3 row B7, section 5.7).
New file, 20 Nov 2026 (Claude Fable 5.2). Scope: B7 only (coordinator decision of 20 Nov 2026: Table III on fresh runs is package
B's; an earlier draft that also covered Table III is kept, unused, as superseded_rc_trackers_v13.py.txt).

Written from AMENDMENT_10_v13.md (sections 2, 3, 5.7, 5.8, 10.1), CD_DEFINITIONS_v13.md, the B7 sections of the writer's
CD_DEFINITIONS_TRK_v13.md, package B's method of record (B_ANALYSIS_DEFINITIONS_v01.md, b_analysis_v01.py for the lag) and A's key
list. No first program of work\\CD_capture\\analysis or work\\CD_capture\\tools was read. The gridless engine is this recount's own
(rc_core_v13 / rc_kern_v13: selection paths, curves, numba kernel); the scoring library of record is used for cross-checks only.
Shared with the first program (A10 section 10.1(b)): the extracted arrays, the B7 detection files, the resample draw.

Modes
  --test-old   old runs only. (1) B7 (i) identity on the one old run with kept sweeps (p1b_fit_finite_0037). (2) The B7 scoring
               path on OLD arrays of the same format (package B's old tracker-variant arrays as stand-ins; NOT B7 values; kept in
               details and compared with package B's values of record). No old-run B7 arrays are defined, so no B7 score.
  (none)       fresh runs. Refused unless revision_v13\\LOCK_A10_2.txt AND LOCK_A10_2c.txt (stage 2) exist.

Families (coordinator, 20 Nov 2026 03:35 EST: A10's B7 row says "both families")
  --family lead    (default) B7.<r>.<L>.* on the 105 fresh lead-braking runs, all evaluated decisions.
  --family cutin   B7CI.<r>.<L>.* on the 105 fresh cut-in runs, in the event window (evaluated decisions with t - t_c in [-1, +4] s
                   around the truth event tick; CD_DEFINITIONS_TRK section 8); as_room and lag are "not applicable". Old-run test:
                   chain (2, 0) = the logged arrays of the 20 cut-in tuning runs, against this recount's rc_c_cutin_v13.py.
                   Outputs RC_B7_v13_cutin<tag>.json / TESTOLD_RC_B7_v13_cutin<tag>.json.

Output: {"family", "program", "test_old", "values": {A key: value}, "details": {...}} (BRIEF_COMMON_v13 convention).
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import argparse, csv, json, pathlib, sys, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import rc_core_v13 as K                      # noqa: E402  (this recount's own core)
L = K.L

PROGRAM = 'rc_b7_v13.py'
BRT = K.ROOT13 / 'work' / 'B_retrack'
OLD_RETRACK = BRT / 'out' / 'retrack'
OLD_RUNS = ['p1b_fit_finite_%04d' % i for i in range(5, 40)]
OLD_B7_RUN = 'p1b_fit_finite_0037'
SEED_OLD = 20261113
NBOOT_OLD = 2000                             # the draw of record's first 2,000 rows (gridless practice of record)
B7_DIR = K.CD / 'b7'
OLD_B7_ARRAYS = K.CD / 'analysis' / 'out' / 'testold_b7_arrays'    # the first program's extraction of the old run 0037 (shared arrays)
IDENT_TOL = 1e-6
DELTA = K.DELTA
LOCK2C = K.ROOT13 / 'LOCK_A10_2c.txt'


def require_locks(what):
    """Two-stage Lock 2 (coordinator, 20 Nov 2026): B7 is a stage-2 addition. No fresh file is opened unless BOTH
    revision_v13\\LOCK_A10_2.txt (stage 1) and revision_v13\\LOCK_A10_2c.txt (stage 2) exist. Fresh arrays may be on disk after
    stage 1; they stay unopened until stage 2."""
    K.require_lock2(what)
    if not LOCK2C.is_file():
        raise SystemExit('REFUSED: %s is sealed until %s exists (stage 2 of Lock 2)' % (what, LOCK2C))


# old tracker-variant arrays used as stand-ins by the format test: folder -> name in package B's record
STAND_INS = ['CV0', 'B3', 'B4', 'B1', 'B2', 'B1_d090', 'B1_d098', 'B3']
B7_CONFIGS = [(2, 0.0), (2, 0.1), (5, 0.0), (5, 0.1), (5, 0.2), (10, 0.0), (10, 0.1), (10, 0.2)]
CRIT = {'F0': 'cF0', 'E': 'cE', 'N': 'cN', 'CK3': 'cCK3'}
NEEDED = ['k', 'evaluated', 'clear', 'vbar', 'idx55', 'des', 'phase', 'lead_found', 'vhat', 'ahat_long', 'dx_pred3', 'now']
POPS = ['all', 'pre', 'brk', 'stop', 'tru_stop']


def lat_txt(lat):
    return '0' if lat == 0 else ('%g' % lat)


def b7_key(r, lat):
    return 'B7.%d.%s' % (r, lat_txt(lat))


def b7_folder(r, lat):
    return 'B7_%d_%s' % (r, lat_txt(lat))


# ------------------------------------------------------------------------------------------------ loading
def run_from_npz(path, rid):
    z = np.load(K.check_path(path), allow_pickle=False)
    miss = [k for k in list(CRIT.values()) + NEEDED if k not in z.files]
    if miss:
        raise SystemExit('REFUSED: %s lacks %s' % (path, miss))
    r = K._run_from_arrays(z, rid, CRIT)
    r['ph'] = np.asarray(z['phase']).astype(np.int64)
    r['lead_found'] = np.asarray(z['lead_found']).astype(bool)
    for k in ('vhat', 'ahat_long', 'dx_pred3', 'now'):
        r[k] = np.asarray(z[k], float)
    if 'age' in z.files:
        r['age'] = np.asarray(z['age'], float)
    r['meta'] = None
    if 'meta' in z.files:
        try:
            r['meta'] = json.loads(str(z['meta']))
        except ValueError:
            pass
    return r


def load_old_variant(folder):
    return [run_from_npz(OLD_RETRACK / folder / (rid + '_arrays.npz'), rid) for rid in OLD_RUNS]


def fresh_cv0_lead():
    """The fresh lead-braking runs of arrays\\CV0 (meta: family lead_braking, no lead variant; ids pc13_*), ascending run id.
    Cross-checked with the lead-braking cases of CASES_C_v13.json: a difference is accepted only as a recorded replacement
    (REPLACEMENTS_C_v13.json present), and the count must be 105."""
    require_locks('fresh-run arrays')
    d = K.ARRAYS / 'CV0'
    runs = []
    for f in sorted(d.glob('pc13_*.npz')):
        z = np.load(f, allow_pickle=False)
        m = json.loads(str(z['meta'])) if 'meta' in z.files else {}
        if m.get('family') != 'lead_braking' or m.get('lead_variant'):
            continue
        runs.append(run_from_npz(f, f.stem))
    ids = [r['run'] for r in runs]
    listed = K.fresh_run_ids('lead_braking')
    rep_file = K.CD / 'REPLACEMENTS_C_v13.json'
    info = dict(n=len(ids), in_arrays_not_in_cases=sorted(set(ids) - set(listed)), in_cases_not_in_arrays=sorted(set(listed) - set(ids)),
                replacements_file_present=rep_file.is_file())
    n_rep = None
    if rep_file.is_file():
        try:
            n_rep = len(json.loads(rep_file.read_text(encoding='utf-8'))['replacements'])
        except (KeyError, ValueError, TypeError):
            n_rep = None
    info['replacements_listed'] = n_rep
    if ids != listed and n_rep == 0:
        raise SystemExit('REFUSED: the lead-braking runs of arrays\\CV0 differ from CASES_C_v13.json although REPLACEMENTS_C_v13.json '
                         'lists no replacement: %s' % info)
    if ids != listed and not rep_file.is_file():
        raise SystemExit('REFUSED: the lead-braking runs of arrays\\CV0 differ from CASES_C_v13.json and there is no '
                         'REPLACEMENTS_C_v13.json: %s' % info)
    if len(ids) != 105 and not K.DRYRUN:               # a dry-run scratch tree (old runs relabelled) holds fewer runs
        raise SystemExit('REFUSED: %d fresh lead-braking runs in arrays\\CV0 (105 expected)' % len(ids))
    return runs, info


def load_fresh_folder(folder, ids):
    """arrays\\<folder>\\<rid>.npz for the given run ids; (None, reason) if the folder or any run is missing."""
    require_locks('fresh-run arrays')
    d = K.ARRAYS / folder
    if not d.is_dir():
        return None, 'folder arrays\\%s not found' % folder
    miss = [rid for rid in ids if not (d / (rid + '.npz')).is_file()]
    if miss:
        return None, 'arrays\\%s lacks %d of %d runs (first: %s)' % (folder, len(miss), len(ids), miss[0])
    return [run_from_npz(d / (rid + '.npz'), rid) for rid in ids], None


def bind_to_cv0(runs, cv0, label):
    """CD_DEFINITIONS_TRK sections 2-3: k, idx55, evaluated and the cleaned clearance must equal the run's CV0 array (they depend on
    the ego state and truth only), otherwise stop; the truth phase of every tracker and chain is the CV0 file's. Returns the number
    of decisions whose own phase array differs (diagnostic only)."""
    ndiff = 0
    for r, c in zip(runs, cv0):
        if r['run'] != c['run']:
            raise SystemExit('REFUSED: %s: run order differs from CV0' % label)
        for key in ('k', 'idx55', 'ev', 'clear1'):
            if not np.array_equal(r[key], c[key]):
                raise SystemExit('REFUSED: %s %s: %s differs from the CV0 array' % (label, r['run'], key))
        ndiff += int((r['ph'] != c['ph']).sum())
        r['ph'] = c['ph'].copy()
    return ndiff


# ------------------------------------------------------------------------------------------------ one tracker / one chain
def lag_of(runs):
    """On the chain's dx_pred3 and lead_found. Method of record (package B, b_analysis_v01; CD_DEFINITIONS_TRK section 6): per run t_stop = `now` of the first decision
    (evaluated or not) with truth phase 2; selected: evaluated, truth phase 2, 0 <= now - t_stop < 1, lead_found; finite dx_pred3
    pooled over runs; median. Beside (diagnostics, never exported): the tick clock (k - k_stop in 0..19) and t_stop taken from the
    evaluated decisions only."""
    v_main, v_tick, v_evstop = [], [], []
    for r in runs:
        ph = r['ph']; ev = r['ev']; k = r['k'].astype(np.int64); dx = r['dx_pred3']; lf = r['lead_found']
        i2 = np.flatnonzero(ph == 2)
        if not i2.size:
            continue
        fin = np.isfinite(dx)
        with np.errstate(invalid='ignore'):
            t = r['now'] - r['now'][i2[0]]
            v_main.append(dx[ev & (ph == 2) & (t >= 0) & (t < 1) & lf & fin])
        d = k - k[i2[0]]
        v_tick.append(dx[ev & (ph == 2) & (d >= 0) & (d < 20) & lf & fin])
        j2 = np.flatnonzero((ph == 2) & ev)
        if j2.size:
            de = k - k[j2[0]]
            v_evstop.append(dx[ev & (ph == 2) & (de >= 0) & (de < 20) & lf & fin])

    def med(v):
        v = np.concatenate(v) if v else np.zeros(0)
        if not v.size:
            return dict(median=None, n=0, q25=None, q75=None)
        return dict(median=float(np.median(v)), n=int(v.size), q25=float(np.percentile(v, 25)), q75=float(np.percentile(v, 75)))
    o = med(v_main)
    o['tick_clock'] = med(v_tick); o['tstop_from_evaluated_tick_clock'] = med(v_evstop)
    o['tick_clock_selects_same_n'] = bool(o['tick_clock']['n'] == o['n'])
    return o


def pop_masks(r):
    ev = r['ev']
    ep = K.est_phase(r['vhat'], r['ahat_long'], r['lead_found'], -1.0)
    return [ev, ev & (ep == 0), ev & (ep == 1), ev & (ep == 2), ev & (r['ph'] == 2)]


def analyse(runs, CNT, label, a9=None, save_boot=None, boot_ck3=False, masks=None, pops=None, boot_pop=0, lag=True):
    """All quantities of one B7 chain on one run set, on the chain's own room (F0 = cF0 with the P-bar of record, E = cE, N = cN,
    CK3 = cCK3 from the chain's states). CNT (B, nrun): bootstrap run counts. The bootstrap covers the all-decisions population:
    N, and CK3 with boot_ck3 (details only).
    Cut-in (B7CI): masks = per-run list of population masks named by pops, and boot_pop = the index of the event window; the
    bootstrap, the saved per-resample arrays and the library cross-check are then on that population, and there is no lag."""
    t0 = time.time()
    n = len(runs)
    out = dict(label=label, n_runs=n, n_dec=int(sum(int(r['ev'].sum()) for r in runs)))
    names = ['F0', 'E', 'N'] + (['CK3'] if all('CK3' in r['crit'] for r in runs) else [])
    boot_ck3 = bool(boot_ck3 and 'CK3' in names)
    pops = POPS if pops is None else pops
    preps = [K.Prep(r) for r in runs]
    if masks is None:
        masks = [pop_masks(r) for r in runs]
    out['margin_ratio'] = K.ratio_summary(np.concatenate([K.margin_ratio_values(r, 'N', 'F0', m[boot_pop]) for r, m in zip(runs, masks)]))
    out['bootstrap_population'] = pops[boot_pop]
    curves = {nm: K.build_curves(runs, preps, nm, lambda k: masks[k]) for nm in names}
    one = np.ones((1, n))
    popd = {}
    for pi, pn in enumerate(pops):
        e = K.Problem(names, [curves[x][pi] for x in names]).evaluate(one)
        den = float(e['denE'][0]); nn = float(e['n'][0])
        popd[pn] = dict(n=int(round(nn)), denE=den, R_pp=den / K.NLEV, R_dec=(L.dec_eq(den, nn) if nn else None),
                        D={x: float(e['D'][x][0]) for x in e['D']}, RR={x: L.ratio(float(e['D'][x][0]), den) for x in e['D']})
    out['populations'] = popd
    p = popd[pops[boot_pop]]
    if a9 is not None:                                          # library of record, full sample, all decisions
        el, _ = K.library_point(a9, runs, names, lambda k: (masks[k][boot_pop],), 0, 'F0', 'E')
        out['library_of_record'] = dict(denE=el['denE'], D=el['D'],
                                        max_abs_diff=float(max([abs(el['denE'] - p['denE'])] + [abs(el['D'][x] - p['D'][x]) for x in p['D']])))
    bn = ['F0', 'E', 'N'] + (['CK3'] if boot_ck3 else [])
    e = K.Problem(bn, [curves[x][boot_pop] for x in bn]).evaluate(CNT)
    den = e['denE']
    b = dict(RR_N=K.ratio_arr(e['D']['N'], den), R_pp=den / K.NLEV)
    pts = dict(RR_N=p['RR']['N'], R_pp=p['R_pp'])
    if boot_ck3:
        b['RR_CK3'] = K.ratio_arr(e['D']['CK3'], den); pts['RR_CK3'] = p['RR']['CK3']
    out['intervals'] = {k: dict(point=pts[k], ci=K.pct_interval(v, 0.95), n_resamples=int(v.size),
                                n_invalid=int((~np.isfinite(v)).sum())) for k, v in b.items()}
    out['bootstrap'] = dict(sources=bn, n_resamples=int(CNT.shape[0]), n_den_le0_dropped=int((~(den > 0)).sum()))
    if save_boot is not None and not pathlib.Path(save_boot).exists():
        arr = dict(denE=den, n=e['n'], D_N=e['D']['N'])
        if boot_ck3:
            arr['D_CK3'] = e['D']['CK3']
        np.savez_compressed(save_boot, **arr)
    if lag:
        out['lag'] = lag_of(runs)
    if lag and all('age' in r for r in runs):                           # the lead track's state age at evaluated decisions (shows rate and latency)
        ag = np.concatenate([r['age'][r['ev'] & r['lead_found'] & np.isfinite(r['age'])] for r in runs])
        out['lead_state_age_s'] = (dict(n=int(ag.size), median=float(np.median(ag)), q90=float(np.percentile(ag, 90)), max=float(ag.max()))
                                   if ag.size else dict(n=0))
    out['seconds'] = time.time() - t0
    return out


# ------------------------------------------------------------------------------------------------ values under A's keys
def nz(x):
    """JSON null for anything undefined."""
    if x is None:
        return None
    if isinstance(x, (list, tuple)):
        return [nz(v) for v in x]
    x = float(x)
    return x if np.isfinite(x) else None


def put_ci(values, key, ci):
    ci = nz(ci)
    values[key] = None if (ci is None or None in ci) else ci
    values[key[:-3] + '.level'] = 0.95; values[key[:-3] + '.cal'] = 'nominal95'


def b7_values(values, r, lat, res):
    p = res['populations']; pre = b7_key(r, lat) + '.'
    values[pre + 'R'] = nz(p['all']['R_pp'])
    values[pre + 'as_room'] = nz(p['tru_stop']['R_dec'])
    values[pre + 'as_room.pp'] = nz(p['tru_stop']['R_pp'])
    values[pre + 'RR_N'] = nz(p['all']['RR']['N']); put_ci(values, pre + 'RR_N.ci', res['intervals']['RR_N']['ci'])
    values[pre + 'RR_CK3'] = nz(p['all']['RR']['CK3'])
    values[pre + 'lag'] = nz(res['lag']['median'])


def b7_rules(values, details):
    """A10 section 3 row B7 (consequence rules), with the strings of CD_DEFINITIONS_TRK section 7. A rule whose inputs are missing
    is null."""
    a10 = values.get('B7.10.0.1.as_room'); a2 = values.get('B7.2.0.as_room')
    values['B7.ratio_10_2'] = (a10 / a2) if (a10 is not None and a2 is not None and a2 > 0) else None
    values['B7.rule_rate'] = None if (a10 is None or a2 is None) else ('consequence' if a10 < 0.5 * a2 else 'holds')
    leaves = {}
    for r, lat in B7_CONFIGS:
        ci = values.get(b7_key(r, lat) + '.RR_N.ci')
        leaves[b7_key(r, lat)] = None if ci is None else (not (ci[0] > -DELTA and ci[1] < DELTA))
    details['B7_rule_N_leaves_by_config'] = leaves
    if any(v is True for v in leaves.values()):
        values['B7.rule_N'] = 'qualified'
    elif all(v is False for v in leaves.values()):
        values['B7.rule_N'] = 'holds'
    else:
        values['B7.rule_N'] = None                      # an interval is missing or undefined, and none is known to leave


# ------------------------------------------------------------------------------------------------ B7 (i) identity
def read_jsonl(path):
    with open(K.check_path(path), encoding='utf-8') as f:
        return [json.loads(x) for x in f if x.strip()]


def identity_run(logged_path, b7_path, last_decision_k=None):
    """A10 B7 (i) for one run: every logged detector row (the online 2 Hz ticks) has a B7 row with the same k, the same
    combined-cloud hash and the same number of boxes, and for each box in order every component of translation and size agrees
    within 1e-6 m. Velocity, rotation, score and class differences are reported only (CD_DEFINITIONS_TRK section 9.4)."""
    lg = read_jsonl(logged_path); b7 = read_jsonl(b7_path)
    ks = [int(r['k']) for r in b7]
    if any(y <= x for x, y in zip(ks, ks[1:])):
        raise SystemExit('REFUSED: %s is not in strictly ascending k' % b7_path)
    byk = {int(r['k']): r for r in b7}
    o = dict(ticks=len(lg), b7_rows=len(b7), missing_k=0, hash_mismatch=0, count_mismatch=0, name_mismatch=0, no_rate2_flag=0,
             not_online_tick_flag=0, boxes=0, max_translation=0., max_size=0., max_velocity=0., max_rotation=0., max_score=0., max_time=0.)
    for r in lg:
        q = byk.get(int(r['k']))
        if q is None:
            o['missing_k'] += 1; continue
        if q.get('combined_hash') != r.get('combined_hash'):
            o['hash_mismatch'] += 1
        if 2 not in q.get('rates_hz', []):
            o['no_rate2_flag'] += 1
        if not q.get('online_tick', False):
            o['not_online_tick_flag'] += 1
        o['max_time'] = max(o['max_time'], abs(float(q['time']) - float(r['time'])))
        A = r['model']; B = q['model']
        if len(A) != len(B):
            o['count_mismatch'] += 1; continue
        for x, y in zip(A, B):
            o['boxes'] += 1
            if x.get('detection_name') != y.get('detection_name'):
                o['name_mismatch'] += 1
            for key, nm in (('translation', 'max_translation'), ('size', 'max_size'), ('velocity', 'max_velocity'),
                            ('rotation', 'max_rotation')):
                dv = float(np.max(np.abs(np.asarray(x[key], float) - np.asarray(y[key], float))))
                o[nm] = max(o[nm], dv) if np.isfinite(dv) else float('inf')
            ds = abs(float(x['detection_score']) - float(y['detection_score']))
            o['max_score'] = max(o['max_score'], ds) if np.isfinite(ds) else float('inf')
    logged_k = set(int(r['k']) for r in lg)
    o['b7_2hz_rows_not_logged'] = int(sum(1 for r in b7 if 2 in r.get('rates_hz', []) and int(r['k']) not in logged_k
                                         and (last_decision_k is None or int(r['k']) <= last_decision_k)))
    o['pass'] = bool(o['missing_k'] == 0 and o['hash_mismatch'] == 0 and o['count_mismatch'] == 0
                     and o['max_translation'] <= IDENT_TOL and o['max_size'] <= IDENT_TOL)
    o['pass_every_component_1e-6'] = bool(o['pass'] and o['name_mismatch'] == 0
                                          and max(o['max_velocity'], o['max_rotation'], o['max_score']) <= IDENT_TOL)
    return o


def fresh_capture_dir(rid):
    """runs\\<rid>\\<rid>\\capture\\<case>\\ (its single capture folder)."""
    require_locks('fresh-run logs')
    base = K.RUNS_DIR / rid / rid / 'capture'
    caps = [p for p in base.iterdir() if p.is_dir()] if base.is_dir() else []
    if len(caps) != 1:
        raise SystemExit('REFUSED: %s does not hold exactly one capture folder' % base)
    return caps[0]


def old_capture_dir(rid):
    with open(K.RUN_INDEX, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['archive'] == rid:
                return pathlib.Path(row['cap'])
    raise SystemExit('REFUSED: %s is not in the run index' % rid)


def identity_all(ids, cap_of, last_k):
    per = {}; missing = []
    for rid in ids:
        f7 = B7_DIR / rid / 'b7_detections_v13.jsonl'
        if not f7.is_file():
            missing.append(rid); continue
        fl = cap_of(rid) / 'detections.jsonl'
        if not fl.is_file():
            missing.append(rid); continue
        per[rid] = identity_run(fl, f7, last_k.get(rid))
    npass = sum(1 for v in per.values() if v['pass'])
    if per and npass < len(per):
        status = 'fail'                                  # one failing run decides
    elif per and not missing:
        status = 'pass'
    else:
        status = None                                    # not every run could be checked, and none failed
    mx = {k: (max(v[k] for v in per.values()) if per else None)
          for k in ('max_translation', 'max_size', 'max_velocity', 'max_rotation', 'max_score', 'max_time')}
    tot = {k: (int(sum(v[k] for v in per.values())) if per else None)
           for k in ('ticks', 'boxes', 'missing_k', 'hash_mismatch', 'count_mismatch', 'name_mismatch', 'no_rate2_flag',
                     'not_online_tick_flag', 'b7_2hz_rows_not_logged')}
    return status, dict(runs_checked=len(per), runs_pass=npass, runs_without_files=missing, tolerance_m=IDENT_TOL, maxima=mx, totals=tot,
                        runs_pass_every_component=sum(1 for v in per.values() if v['pass_every_component_1e-6']), per_run=per)


# ------------------------------------------------------------------------------------------------ B7 on the cut-in runs (B7CI)
CI_POPS = ['all', 'window']
CI_WIN = (-20, 80)                   # ticks: t - t_c in [-1, +4] s at 0.05 s per tick (A10 section 2.5)
CI_SCORE_KEYS = ('R', 'RR_N', 'RR_N.ci', 'RR_CK3')
NOT_APPLICABLE = 'not applicable'


def ci_key(r, lat):
    return 'B7CI.%d.%s' % (r, lat_txt(lat))


def ci_folder(r, lat):
    return 'B7CI_%d_%s' % (r, lat_txt(lat))


def ci_run_from_npz(path, rid):
    """A cut-in chain array: the scoring keys only (no lead-track keys are used on cut-in runs)."""
    z = np.load(K.check_path(path), allow_pickle=False)
    miss = [k for k in ['cF0', 'cE', 'cN', 'k', 'evaluated', 'clear', 'vbar', 'idx55', 'des'] if k not in z.files]
    if miss:
        raise SystemExit('REFUSED: %s lacks %s' % (path, miss))
    return K._run_from_arrays(z, rid, CRIT)


def ci_bind(runs, ref, label):
    """k, idx55, evaluated and the cleaned clearance of a chain must equal the run's CV0 (reference) array."""
    for r, c in zip(runs, ref):
        if r['run'] != c['run']:
            raise SystemExit('REFUSED: %s: run order differs from CV0' % label)
        for key in ('k', 'idx55', 'ev', 'clear1'):
            if not np.array_equal(r[key], c[key]):
                raise SystemExit('REFUSED: %s %s: %s differs from the CV0 array' % (label, r['run'], key))


def ci_masks(r, k_c):
    """[all evaluated decisions, event window]: evaluated decisions with -20 <= k - k_c <= 80 ticks; no event -> empty window."""
    ev = r['ev']
    if k_c is None:
        return [ev, np.zeros(ev.size, bool)]
    dk = np.asarray(r['k']).astype(np.int64) - int(k_c)
    return [ev, ev & (dk >= CI_WIN[0]) & (dk <= CI_WIN[1])]


def ci_event_ticks(runs, truth_file):
    """Event tick of every run (CD_DEFINITIONS_v13 'C, cut-in'): this recount's own rc_c_cutin_v13.truth_of_run (truth of the run,
    route frame; first tick with the primary actor ahead and within 1.75 m of the lane centre), or a truth file that program
    wrote for exactly these runs and decisions."""
    if truth_file:
        t = json.loads(pathlib.Path(truth_file).read_text(encoding='utf-8'))
        if [x['run'] for x in t['truth']] != [r['run'] for r in runs]:
            raise SystemExit('REFUSED: the truth file does not describe this run set')
        for r, x in zip(runs, t['truth']):
            if not np.array_equal(np.asarray(x['k']), np.asarray(r['k'])):
                raise SystemExit('REFUSED: the truth file decisions of %s do not match its arrays' % r['run'])
        return [x['event_tick'] for x in t['truth']], 'truth file %s (sha256 %s)' % (truth_file, K.KN.sha256_file(truth_file))
    import rc_c_cutin_v13 as CC
    return [CC.truth_of_run(r)['event_tick'] for r in runs], 'computed here (rc_c_cutin_v13.truth_of_run)'


def ci_values(values, r, lat, res):
    p = res['populations']['window']; pre = ci_key(r, lat) + '.'
    values[pre + 'R'] = nz(p['R_pp'])
    values[pre + 'RR_N'] = nz(p['RR']['N']); put_ci(values, pre + 'RR_N.ci', res['intervals']['RR_N']['ci'])
    values[pre + 'RR_CK3'] = nz(p['RR'].get('CK3'))
    values[pre + 'as_room'] = NOT_APPLICABLE; values[pre + 'lag'] = NOT_APPLICABLE


def ci_nulls(values, r, lat):
    pre = ci_key(r, lat) + '.'
    for k in CI_SCORE_KEYS:
        values[pre + k] = None
    values[pre + 'RR_N.level'] = 0.95; values[pre + 'RR_N.cal'] = 'nominal95'
    values[pre + 'as_room'] = NOT_APPLICABLE; values[pre + 'lag'] = NOT_APPLICABLE


def main_cutin(a):
    t00 = time.time()
    nthreads = K.set_workers(min(a.threads, 2))
    old = a.test_old
    FRESH_STEM = ('DRYRUN_RC_B7_v13_cutin' if K.DRYRUN else 'RC_B7_v13_cutin')
    stem = ('TESTOLD_RC_B7_v13_cutin' if old else FRESH_STEM) + a.tag
    outf = K.OUT / (stem + '.json')
    if outf.exists():
        raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % outf)
    if not old:
        require_locks('fresh cut-in arrays and truth')          # before anything else
    if a.combine:
        raise SystemExit('REFUSED: --combine is not offered for the cut-in family (run it in one piece)')
    only = [x for x in a.only.split(',') if x]
    values = {}
    details = dict(role='second program (recount), AMENDMENT_10_v13 section 10.1(b)', model='claude-fable-5-2', started=K.clock(),
                   threads=nthreads, delta=DELTA, only=only or 'everything', window_ticks=list(CI_WIN), lateral_threshold_m=1.75,
                   population='event window: evaluated decisions with t - t_c in [-1, +4] s; 3 s commitment',
                   shared='extracted arrays, resample draw; scoring library of record for cross-checks only',
                   status='descriptive (A10 section 5.7); every interval nominal 95% percentile', B7CI={})
    A9 = None if a.no_library else K.try_a9()

    def finish():
        details['written'] = K.clock(); details['seconds'] = time.time() - t00
        bad = [k for k in values if not k.startswith('B7CI.')]
        if bad:
            raise SystemExit('REFUSED: keys outside B7CI: %s' % bad)
        doc = dict(family='B7CI', program=PROGRAM, test_old=bool(old), values=values, details=details)
        if K.DRYRUN and not old:
            doc['WARNING'] = 'DRY RUN: OLD runs relabelled as fresh in a scratch tree outside the project; NOT fresh data, NOT B7 values'
        print('written %s (%.0f s)' % (K.write_new(outf, doc), time.time() - t00), flush=True)

    def events_block(runs, kc, src, masks):
        details['truth_source'] = src
        details['runs'] = [r['run'] for r in runs]
        details['event_ticks'] = kc
        details['events'] = dict(found=int(sum(x is not None for x in kc)), of=len(runs),
                                 runs_without_event=[r['run'] for r, x in zip(runs, kc) if x is None])
        details['counts'] = dict(evaluated=int(sum(int(m[0].sum()) for m in masks)), window=int(sum(int(m[1].sum()) for m in masks)),
                                 window_per_run=[int(m[1].sum()) for m in masks])

    # ---------------- old runs: chain (2, 0) = the logged arrays of the 20 cut-in tuning runs
    if old:
        runs = K.load_old_cutin_runs()
        tf = a.truth_file or str(K.OUT / 'RC_C_CUTIN_TESTOLD_TRUTH_v13.json')
        kc, src = ci_event_ticks(runs, tf if pathlib.Path(tf).is_file() else None)
        masks = [ci_masks(r, x) for r, x in zip(runs, kc)]
        events_block(runs, kc, src, masks)
        nb = a.boot or NBOOT_OLD
        CNT = K.boot_counts(len(runs), K.NBOOT, K.SEED_BOOT)[:nb]
        details['draw'] = ('old-run test: first %d rows of default_rng(%d).integers(0, %d, (20000, %d)) as counts, runs in archive-name '
                           'order' % (nb, K.SEED_BOOT, len(runs), len(runs)))
        for r, lat in B7_CONFIGS:
            ci_nulls(values, r, lat)
        res = analyse(runs, CNT, 'old-run test: logged arrays of the 20 cut-in tuning runs as chain (2, 0)', A9, masks=masks,
                      pops=CI_POPS, boot_pop=1, lag=False)
        ci_values(values, 2, 0.0, res)
        details['B7CI'][ci_key(2, 0.0)] = res
        # against this recount's own K0 / K1 program on the same runs (rc_c_cutin_v13 --test-old)
        refs = sorted(K.OUT.glob('RC_C_CUTIN_TESTOLD_b*.json'), key=lambda f: f.stat().st_mtime)
        refs = [f for f in refs if 'PENDING' not in f.name]
        if refs:
            d = json.loads(refs[-1].read_text(encoding='utf-8'))
            rows = []
            for pop in ('window', 'all'):
                rp = d['point']['populations'][pop]; mp = res['populations'][pop]
                for k, mine in (('n', mp['n']), ('denE', mp['denE']), ('R_pp', mp['R_pp']), ('RR_N', mp['RR']['N'])):
                    ref = rp[k]
                    both_nan = bool(isinstance(ref, float) and np.isnan(ref) and isinstance(mine, float) and np.isnan(mine))
                    rows.append(dict(key=pop + '.' + k, recount_b7=mine, rc_c_cutin=ref, both_undefined=both_nan,
                                     abs_diff=None if both_nan else abs(float(mine) - float(ref))))
            ok = all(x['both_undefined'] or (x['abs_diff'] is not None and x['abs_diff'] <= 1e-9) for x in rows)
            ok = ok and d.get('runs') == details['runs'] and d['counts']['window'] == details['counts']['window']
            details['check_vs_rc_c_cutin'] = dict(reference=str(refs[-1]), rows=rows, same_runs=bool(d.get('runs') == details['runs']),
                                                  window_decisions=[details['counts']['window'], d['counts']['window']], agree=bool(ok))
            print('old cut-in runs, chain (2, 0): window n %d, R %.6g pp, RR_N %s; vs %s: agree %s'
                  % (res['populations']['window']['n'], res['populations']['window']['R_pp'], values['B7CI.2.0.RR_N'], refs[-1].name, ok),
                  flush=True)
        # the window scoring where there IS room: old lead-braking runs with a stand-in event tick (the first truth-phase-1
        # decision), kernel against the library of record. Not a cut-in value.
        if A9 is not None:
            lead = load_old_variant('CV0')
            kcl = [(int(r['k'][np.flatnonzero(r['ph'] == 1)[0]]) if (r['ph'] == 1).any() else None) for r in lead]
            ml = [ci_masks(r, x) for r, x in zip(lead, kcl)]
            CNT35 = K.counts_of(np.random.default_rng(SEED_OLD).integers(0, 35, (20000, 35))[:200], 35)
            rl = analyse(lead, CNT35, 'STAND-IN: old lead-braking runs, window around the first truth-phase-1 decision', A9, masks=ml,
                         pops=CI_POPS, boot_pop=1, lag=False, boot_ck3=True)
            details['window_scoring_check_on_lead_runs'] = dict(
                WARNING='stand-in population on OLD lead-braking runs; tests the window scoring against the library of record; NOT a cut-in value',
                n_window=rl['populations']['window']['n'], R_pp=rl['populations']['window']['R_pp'], RR=rl['populations']['window']['RR'],
                intervals=rl['intervals'], library_max_abs_diff=rl['library_of_record']['max_abs_diff'])
            print('window scoring on old lead runs (stand-in): n %d, R %.6f pp, RR_N %.6g, library max |diff| %.3g'
                  % (rl['populations']['window']['n'], rl['populations']['window']['R_pp'], rl['populations']['window']['RR']['N'],
                     rl['library_of_record']['max_abs_diff']), flush=True)
        values['B7CI.identity'] = None
        details['B7CI_identity'] = dict(note='no old cut-in run kept its sweeps: there is no B7 detection file, so the identity cannot be '
                                             'tested on old cut-in runs (the routine is tested on p1b_fit_finite_0037 in the lead family)')
        return finish()

    # ---------------- fresh cut-in runs
    ref = K.load_fresh_runs('cutin', 'CV0')
    if len(ref) != 105 and not K.DRYRUN:
        raise SystemExit('REFUSED: %d fresh cut-in runs (105 expected)' % len(ref))
    ids = [r['run'] for r in ref]
    if a.truth_file is None:
        for r in ref:
            r['rd'] = K.check_path(K.RUNS_DIR / r['run'] / r['run'])
            r['cap'] = fresh_capture_dir(r['run'])
    kc, src = ci_event_ticks(ref, a.truth_file)
    masks = [ci_masks(r, x) for r, x in zip(ref, kc)]
    events_block(ref, kc, src, masks)
    nb = a.boot or K.NBOOT
    CNT = K.boot_counts(len(ids), K.NBOOT, K.SEED_BOOT)[:nb]
    details['draw'] = ('first %d rows of default_rng(%d).integers(0, %d, (20000, %d)) as counts per run, cut-in runs in ascending run id '
                       'order' % (nb, K.SEED_BOOT, len(ids), len(ids)))
    for r, lat in B7_CONFIGS:
        fo = ci_folder(r, lat); key = ci_key(r, lat)
        ci_nulls(values, r, lat)
        d = K.ARRAYS / fo
        miss = [rid for rid in ids if not (d / (rid + '.npz')).is_file()]
        if (only and fo not in only) or miss:
            details['B7CI'][key] = dict(not_done=('arrays\\%s lacks %d of %d runs' % (fo, len(miss), len(ids))) if miss else 'not selected')
            print('%s: not done (%s)' % (key, details['B7CI'][key]['not_done']), flush=True)
            continue
        runs = [ci_run_from_npz(d / (rid + '.npz'), rid) for rid in ids]
        ci_bind(runs, ref, fo)
        res = analyse(runs, CNT, fo, A9, save_boot=K.OUT / ('%s_boot_%s.npz' % (stem, fo)), boot_ck3=a.ck3_ci, masks=masks, pops=CI_POPS,
                      boot_pop=1, lag=False)
        if (r, lat) == (2, 0.0):                                # diagnostic of B7 (i) at the array level
            with np.errstate(invalid='ignore'):
                res['max_abs_diff_vs_CV0_arrays'] = {
                    nm: float(max(np.max(np.abs(np.where(np.isfinite(x['crit'][nm]) & np.isfinite(c['crit'][nm]),
                                                         x['crit'][nm] - c['crit'][nm], 0.))) for x, c in zip(runs, ref)))
                    for nm in ('F0', 'E', 'N')}
        ci_values(values, r, lat, res)
        details['B7CI'][key] = res
        pw = res['populations']['window']
        print('%-12s window n %d R %.6f pp (%.3f dec-eq) RR_N %s RR_CK3 %s (%.0f s)'
              % (key, pw['n'], pw['R_pp'], pw['R_dec'] or 0., values[key + '.RR_N'], values[key + '.RR_CK3'], res['seconds']), flush=True)
    values['B7CI.identity'] = None
    if not only:                                                # A10 B7 (i) on the cut-in runs (CD_DEFINITIONS_TRK section 8)
        st, det = identity_all(ids, fresh_capture_dir, {r['run']: int(r['k'][-1]) for r in ref})
        values['B7CI.identity'] = st; details['B7CI_identity'] = det
        print('B7CI identity: %s (%d of %d runs pass; %d without files)' % (st, det['runs_pass'], det['runs_checked'],
                                                                           len(det['runs_without_files'])), flush=True)
    finish()


# ------------------------------------------------------------------------------------------------ format test (old runs)
def cmp_stand_in(folder, res, vals, key):
    """The B7 scoring path fed with package B's old arrays of tracker `folder` must reproduce package B's values of record for
    that tracker (out\\banalysis\\B_<folder>_v01.json): same quantities, same draw (first 2,000 rows of the draw of record)."""
    f = BRT / 'out' / 'banalysis' / ('B_%s_v01.json' % folder)
    d = json.loads(f.read_text(encoding='utf-8'))
    P = d['points']; I = d['intervals']['all']; iv = res['intervals']
    pairs = [('n_dec', res['n_dec'], P['all']['n']), ('R', vals[key + '.R'], P['all']['R_pp']),
             ('as_room', vals[key + '.as_room'], P['tru_stopped']['R_deceq']), ('as_room.pp', vals[key + '.as_room.pp'], P['tru_stopped']['R_pp']),
             ('RR_N', vals[key + '.RR_N'], P['all']['RR']['N']), ('RR_CK3', vals[key + '.RR_CK3'], P['all']['RR']['CK3']),
             ('lag', vals[key + '.lag'], d['lag_dx3_first_second_after_stop']['median']),
             ('lag_n', res['lag']['n'], d['lag_dx3_first_second_after_stop']['n']),
             ('RR_N.ci.lo', vals[key + '.RR_N.ci'][0], I['RR_N']['ci'][0]), ('RR_N.ci.hi', vals[key + '.RR_N.ci'][1], I['RR_N']['ci'][1]),
             ('R.ci.lo', iv['R_pp']['ci'][0], I['R_pp']['ci'][0]), ('R.ci.hi', iv['R_pp']['ci'][1], I['R_pp']['ci'][1])]
    if 'RR_CK3' in iv:
        pairs += [('RR_CK3.ci.lo', iv['RR_CK3']['ci'][0], I['RR_CK3']['ci'][0]), ('RR_CK3.ci.hi', iv['RR_CK3']['ci'][1], I['RR_CK3']['ci'][1])]
    rows = [dict(key=k, recount=m, B_record=ref, abs_diff=abs(float(m) - float(ref))) for k, m, ref in pairs]
    mx = max(r['abs_diff'] for r in rows)
    return dict(reference=str(f), n_compared=len(rows), rows=rows, max_abs_diff=mx, agree_1e9=bool(mx <= 1e-9))


# ------------------------------------------------------------------------------------------------ main
SCORE_KEYS = ('R', 'as_room', 'as_room.pp', 'RR_N', 'RR_N.ci', 'RR_CK3', 'lag')
STATUS_KEYS = ('B7.identity', 'B7.ratio_10_2', 'B7.rule_rate', 'B7.rule_N')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--test-old', action='store_true')
    ap.add_argument('--family', default='lead', choices=['lead', 'cutin'], help='lead: B7.* on the fresh lead-braking runs; '
                                                                               'cutin: B7CI.* on the fresh cut-in runs')
    ap.add_argument('--only', default='', help='comma list of B7 folders (e.g. B7_10_0.1) for a run in pieces; use with --tag')
    ap.add_argument('--combine', default='', help='comma list of the tags of fresh piece outputs: merges their values, then the '
                                                  'rules and the identity; writes RC_B7_v13<tag>.json')
    ap.add_argument('--tag', default='')
    ap.add_argument('--threads', type=int, default=2)
    ap.add_argument('--boot', type=int, default=0, help='resamples (default: 20,000 fresh; 2,000 old runs)')
    ap.add_argument('--ck3-ci', action='store_true', help='also bootstrap RR_CK3 (details only; slower)')
    ap.add_argument('--no-library', action='store_true')
    ap.add_argument('--truth-file', default=None, help='cut-in family: a truth file of rc_c_cutin_v13.py (--stage truth) for these runs')
    a = ap.parse_args()
    if a.family == 'cutin':
        return main_cutin(a)
    t00 = time.time()
    nthreads = K.set_workers(min(a.threads, 2))
    old = a.test_old
    FRESH_STEM = 'DRYRUN_RC_B7_v13' if K.DRYRUN else 'RC_B7_v13'      # RC_DRYRUN: a scratch tree of OLD runs relabelled (rc_core_v13)
    stem = ('TESTOLD_RC_B7_v13' if old else FRESH_STEM) + a.tag
    outf = K.OUT / (stem + '.json')
    if outf.exists():
        raise SystemExit('REFUSED: %s exists (outputs are never overwritten)' % outf)
    if not old:
        require_locks('fresh-run arrays')                       # before anything else
    only = [x for x in a.only.split(',') if x]
    values = {}
    details = dict(role='second program (recount), AMENDMENT_10_v13 section 10.1(b)', model='claude-fable-5-2', started=K.clock(),
                   threads=nthreads, delta=DELTA, only=only or 'everything',
                   shared='extracted arrays, B7 detection files, resample draw; scoring library of record for cross-checks only',
                   status='descriptive (A10 section 5.7); every interval nominal 95% percentile', B7={})

    def finish():
        details['keys_beyond_A_KEYS_CD_v13'] = ['B7.<r>.<L>.as_room.pp', 'B7.ratio_10_2', 'B7.rule_rate', 'B7.rule_N', '*.level', '*.cal']
        details['written'] = K.clock(); details['seconds'] = time.time() - t00
        bad = [k for k in values if not k.startswith('B7.')]
        if bad:
            raise SystemExit('REFUSED: keys outside B7: %s' % bad)
        doc = dict(family='B7', program=PROGRAM, test_old=bool(old), values=values, details=details)
        if K.DRYRUN and not old:
            doc['WARNING'] = 'DRY RUN: OLD runs relabelled as fresh in a scratch tree outside the project; NOT fresh data, NOT B7 values'
        print('written %s (%.0f s)' % (K.write_new(outf, doc), time.time() - t00), flush=True)

    # ---------------- old runs: identity on the old run with sweeps; scoring path on stand-in arrays
    if old:
        if a.combine:
            raise SystemExit('REFUSED: --combine is for fresh pieces')
        nb = a.boot or NBOOT_OLD
        CNT = K.counts_of(np.random.default_rng(SEED_OLD).integers(0, 35, (20000, 35))[:nb], 35)
        details['draw'] = ('format test: first %d rows of default_rng(%d).integers(0, 35, (20000, 35)), runs p1b_fit_finite_0005..0039 '
                           'in name order (the draw of record)' % (nb, SEED_OLD))
        cv0 = load_old_variant('CV0')
        last_k = {r['run']: int(r['k'][-1]) for r in cv0}
        st, det = identity_all([OLD_B7_RUN], old_capture_dir, last_k)
        values['B7.identity'] = st
        det['note'] = 'old-run test: the one old run with kept sweeps (%s)' % OLD_B7_RUN
        details['B7_identity'] = det
        print('B7 identity on %s: %s (ticks %s, boxes %s, max |d translation| %.3g, max |d size| %.3g)'
              % (OLD_B7_RUN, st, det['totals']['ticks'], det['totals']['boxes'], det['maxima']['max_translation'], det['maxima']['max_size']),
              flush=True)
        A9 = None if a.no_library else K.try_a9()
        # the old run with B7 detection rows (CD_DEFINITIONS_TRK sections 1 and 6): one run, the fresh seed over one run (every
        # resample is the run itself). A pipeline exercise, not a result.
        ref_f = OLD_B7_ARRAYS / 'CV0' / (OLD_B7_RUN + '.npz')
        if not ref_f.is_file():
            ref_f = OLD_RETRACK / 'CV0' / (OLD_B7_RUN + '_arrays.npz')
        ref = [run_from_npz(ref_f, OLD_B7_RUN)]
        CNT1 = K.boot_counts(1, K.NBOOT, K.SEED_BOOT)
        details['old_run_0037'] = dict(reference_array=str(ref_f), arrays=str(OLD_B7_ARRAYS),
                                       draw='default_rng(%d).integers(0, 1, (20000, 1)) as counts (every resample is the run itself)' % K.SEED_BOOT,
                                       note='pipeline exercise on one old run; not results (A10 B7 asks only for the lag statistics on this run)')
        for r, lat in B7_CONFIGS:
            fo = b7_folder(r, lat); key = b7_key(r, lat)
            f = OLD_B7_ARRAYS / fo / (OLD_B7_RUN + '.npz')
            if (only and fo not in only) or not f.is_file():
                details['B7'][key] = dict(not_done='not selected' if f.is_file() else 'no old-run array %s' % f)
                for k in SCORE_KEYS:
                    values['%s.%s' % (key, k)] = None
                continue
            runs = [run_from_npz(f, OLD_B7_RUN)]
            ndiff = bind_to_cv0(runs, ref, fo)
            res = analyse(runs, CNT1, '%s on %s' % (fo, OLD_B7_RUN), A9, boot_ck3=True)
            res['decisions_own_phase_differs_from_CV0'] = ndiff
            res['array_sha256'] = K.KN.sha256_file(f)
            b7_values(values, r, lat, res)
            details['B7'][key] = res
            print('%s %-10s n %d R %s pp as_room %s RR_N %s RR_CK3 %s lag %s (n %d)'
                  % (OLD_B7_RUN, key, res['n_dec'], values[key + '.R'], values[key + '.as_room'], values[key + '.RR_N'],
                     values[key + '.RR_CK3'], values[key + '.lag'], res['lag']['n']), flush=True)
        b7_rules(values, details)
        ft = dict(WARNING="STAND-INS: the B7 scoring path run on package B's OLD tracker-variant arrays (same format as the B7 arrays). "
                          "These are NOT B7 values; they test the code against package B's values of record.", chains={})
        fv = {}
        for (r, lat), folder in zip(B7_CONFIGS, STAND_INS):
            fo = b7_folder(r, lat); key = b7_key(r, lat)
            if only and fo not in only:
                continue
            runs = load_old_variant(folder)
            ndiff = bind_to_cv0(runs, cv0, folder) if folder != 'CV0' else 0
            res = analyse(runs, CNT, 'stand-in for %s: old arrays of tracker %s' % (fo, folder), A9, boot_ck3=True)
            res['decisions_own_phase_differs_from_CV0'] = ndiff
            b7_values(fv, r, lat, res)
            res['check_vs_B_record'] = cmp_stand_in(folder, res, fv, key)
            ft['chains'][key] = res
            c = res['check_vs_B_record']
            print('format test %-10s <- %-7s: %d values vs package B record, max |diff| %.3g, agree within 1e-9: %s; library max |diff| %s (%.0f s)'
                  % (key, folder, c['n_compared'], c['max_abs_diff'], c['agree_1e9'],
                     res.get('library_of_record', {}).get('max_abs_diff'), res['seconds']), flush=True)
        dd = {}
        b7_rules(fv, dd)
        ft['values_under_stand_ins'] = fv; ft['rules_under_stand_ins'] = dd
        chk = [c['check_vs_B_record'] for c in ft['chains'].values()]
        ft['all_agree_1e9'] = bool(chk and all(c['agree_1e9'] for c in chk))
        details['format_test'] = ft
        return finish()

    # ---------------- fresh runs
    cv0, info = fresh_cv0_lead(); ids = [r['run'] for r in cv0]
    details['run_set'] = info; details['runs'] = ids
    details['n_evaluated_per_run'] = [int(r['ev'].sum()) for r in cv0]
    last_k = {r['run']: int(r['k'][-1]) for r in cv0}
    nb = a.boot or K.NBOOT
    details['draw'] = ('first %d rows of default_rng(%d).integers(0, %d, (20000, %d)) as counts per run, runs in ascending run id order'
                       % (nb, K.SEED_BOOT, len(ids), len(ids)))
    if a.combine:
        pieces = {}
        for tag in [x for x in a.combine.split(',') if x]:
            f = K.OUT / ('%s%s.json' % (FRESH_STEM, tag))
            d = json.loads(f.read_text(encoding='utf-8'))
            if d.get('program') != PROGRAM or d.get('test_old') or d['details'].get('runs') != ids or d['details'].get('draw') != details['draw']:
                raise SystemExit('REFUSED: %s is not a fresh piece of this run set and draw' % f)
            for k, v in d['values'].items():
                if k in STATUS_KEYS:
                    continue
                if values.get(k) is not None and v is not None and values[k] != v:
                    raise SystemExit('REFUSED: %s differs between pieces' % k)
                if values.get(k) is None:
                    values[k] = v
            pieces[tag] = dict(file=str(f), sha256=K.KN.sha256_file(f), only=d['details'].get('only'))
            details['B7'].update({k: v for k, v in d['details'].get('B7', {}).items() if 'not_done' not in v or k not in details['B7']})
        details['combined_from'] = pieces
    else:
        A9 = None if a.no_library else K.try_a9()
        CNT = K.boot_counts(len(ids), K.NBOOT, K.SEED_BOOT)[:nb]
        for r, lat in B7_CONFIGS:
            fo = b7_folder(r, lat); key = b7_key(r, lat)
            if only and fo not in only:
                continue
            runs, note = load_fresh_folder(fo, ids)
            if runs is None:
                details['B7'][key] = dict(not_done=note)
                for k in SCORE_KEYS:
                    values['%s.%s' % (key, k)] = None
                print('%s: not done (%s)' % (key, note), flush=True)
                continue
            ndiff = bind_to_cv0(runs, cv0, fo)
            res = analyse(runs, CNT, fo, A9, save_boot=K.OUT / ('%s_boot_%s.npz' % (stem, fo)), boot_ck3=a.ck3_ci)
            res['decisions_own_phase_differs_from_CV0'] = ndiff
            if (r, lat) == (2, 0.0):                            # diagnostic of B7 (i) at the array level
                with np.errstate(invalid='ignore'):             # inf - inf at rows without a finite scale: not compared
                    res['max_abs_diff_vs_CV0_arrays'] = {
                        nm: float(max(np.max(np.abs(np.where(np.isfinite(x['crit'][nm]) & np.isfinite(c['crit'][nm]),
                                                             x['crit'][nm] - c['crit'][nm], 0.))) for x, c in zip(runs, cv0)))
                        for nm in CRIT}
                res['n_finiteness_differs_from_CV0_arrays'] = {
                    nm: int(sum(int((np.isfinite(x['crit'][nm]) != np.isfinite(c['crit'][nm])).sum()) for x, c in zip(runs, cv0)))
                    for nm in CRIT}
            b7_values(values, r, lat, res)
            details['B7'][key] = res
            print('%-10s n %d R %.6f pp as_room %s RR_N %.6g RR_CK3 %.6f lag %s (%.0f s)'
                  % (key, res['n_dec'], res['populations']['all']['R_pp'], values[key + '.as_room'], res['populations']['all']['RR']['N'],
                     res['populations']['all']['RR']['CK3'], values[key + '.lag'], res['seconds']), flush=True)
    b7_rules(values, details)
    values['B7.identity'] = None
    if not only:
        st, det = identity_all(ids, fresh_capture_dir, last_k)
        values['B7.identity'] = st; details['B7_identity'] = det
        print('B7 identity: %s (%d of %d runs pass; %d without files)' % (st, det['runs_pass'], det['runs_checked'],
                                                                         len(det['runs_without_files'])), flush=True)
    finish()


if __name__ == '__main__':
    main()
