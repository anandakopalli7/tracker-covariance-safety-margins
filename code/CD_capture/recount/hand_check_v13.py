"""Revision v13, package CD: the hand-check subset of AMENDMENT_10_v13 sec. 10.2 (S10). New file, 20 Nov 2026 (Claude Fable 5.2).

A10 sec. 10.2: 20 evaluated fresh lead-braking decisions (default_rng(20261917)), stratified 7/7/6 by truth phase; the true clearance of
F0's selection at g = 1 is computed by a NEW routine without the scoring library; tolerance 1e-6 m; the cases are tabulated.

Two separate parts (README_HAND_CHECK.md states the rules; written before any fresh value existed):

  PART N, the new routine (functions n_*). Imports: json, math, numpy only. It reads, per selected decision, the run's capture logs
    frames.jsonl            the decision record (execution.new_decision, mode 'assessment'): model state, tracked actors, ego box,
                            desired speed, decision time
    evaluation_truth.jsonl  the truth log: ego centre and route yaw at the decision tick; every true scenario actor's centre, heading
                            and half extents at the 61 ticks of the 3 s plan
  and the parameter file of record pbar_tuning_v01.json (F0's class-average covariance P-bar). From these it rebuilds the 17 candidate
  rows (the planner's row library), F0's critical scale of every row, the row selected at caution scale g = 1 and that row's true
  clearance. It calls none of: optA_lib_v02, a9_common_v01, rev_common_v01, trk_score_v01, cd_common_v13's scoring, the gateR /
  ol_* / ox* extraction code, the planner modules (consumer, finite_primitive, design_core_v85), c_extract_v13.

  PART R, the reference (functions r_*): the arrays of record (fresh: arrays/CV0/<rid>.npz; old: cd_common_v13.load_old_lead()) and
  the scoring library's selection optA_lib_v02.select_grid(cF0, [1.0], idx55) with the stored clearance of the selected row.
  The selection of the 20 cases (which decision is checked) also uses the arrays' k, evaluated and truth phase.

Usage (from work\\CD_capture; PY = .venv\\Scripts\\python.exe -I -B -X utf8; OPENBLAS_CORETYPE=Haswell):
  PY recount\\hand_check_v13.py --test-old [--tag T]     the 35 old evaluation runs (a TEST; no fresh value)
  PY recount\\hand_check_v13.py [--tag T]                the 105 fresh lead-braking runs; REFUSED without revision_v13\\LOCK_A10_2.txt
Outputs (never overwritten): recount\\out\\HAND_CHECK_v13[_T].json, recount\\out\\TESTOLD_HAND_CHECK_v13[_T].json, and a log beside each.
"""
import json, math, pathlib, sys, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
CD = HERE.parent
V13 = CD.parent.parent
LOCK2 = V13 / 'LOCK_A10_2.txt'
OUT = HERE / 'out'
P_ROOT = pathlib.Path(r'<library folder>')
PBAR_RECORD = P_ROOT / '09_redesign' / 'm2_decisions' / 'openloop' / 'pbar_tuning_v01.json'
OLD_ARCH = P_ROOT / '07_fit_runs' / 'archives'
RUNS = CD / 'runs'
ARR = CD / 'arrays' / 'CV0'

SEED = 20261917
SIZES = (7, 7, 6)            # truth phase 0, 1, 2
TOL = 1e-6                   # m
G1 = 1.0                     # caution scale of the check

# =====================================================================================================================================
# PART N: the new routine (json, math, numpy only)
# =====================================================================================================================================
N_H = 0.05                   # s, plan step
N_STEPS = 60                 # 3 s
N_TARGETS = (-5., -2., 0., 2.)
N_FALLBACK = (-5., -5.)
N_SLEW = 8.0                 # m/s^3: the acceleration moves towards its target by at most 8 * h per step
N_VMAX = 20.0


def n_jsonl(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def n_decision(cap, k):
    """The decision record of tick k: frames.jsonl, execution.new_decision with mode 'assessment'."""
    for r in n_jsonl(cap / 'frames.jsonl'):
        if r.get('k') == k:
            dec = (r.get('execution') or {}).get('new_decision')
            if dec and dec.get('mode') == 'assessment':
                return dec
    raise RuntimeError('no assessment decision at k = %d in %s' % (k, cap))


def n_truth(cap):
    """Truth log: k -> (ego centre x, y, route yaw; id of the lead (target) or None; {actor id: (x, y, heading, half length, half
    width)}). Right-handed coordinates of the log ('center_rh', 'heading_rh', 'route_yaw_rh')."""
    T = {}
    for r in n_jsonl(cap / 'evaluation_truth.jsonl'):
        e = r['ego']['derived']
        acts = {}
        for a in r.get('scenario_actors') or []:
            d = a['derived']
            acts[a['actor_id']] = (float(d['center_rh'][0]), float(d['center_rh'][1]), float(d['heading_rh']),
                                   float(a['half_extents'][0]), float(a['half_extents'][1]))
        tg = r.get('target')
        T[int(r['k'])] = (float(e['center_rh'][0]), float(e['center_rh'][1]), float(e['route_yaw_rh']),
                          tg['actor_id'] if tg else None, acts)
    return T


def n_row(first, second, v0, a0, desired):
    """One candidate row: acceleration target `first` during the first second, `second` afterwards; the acceleration is slewed at
    8 m/s^3; the speed saturates at 0 and 20 m/s. Returns positions s (61), speeds v (61) and the planner's cost."""
    v = float(v0); a = float(a0); s = 0.0
    ss = [0.0]; vs = [v]; acc = []; jr = []
    lim = N_SLEW * N_H
    for j in range(N_STEPS):
        target = first if j * N_H < 1.0 - 1e-12 else second
        prev = a
        step = target - a
        if step > lim: step = lim
        elif step < -lim: step = -lim
        a = a + float(step)
        vn = v + a * N_H
        if vn < 0.0 or vn > N_VMAX:
            bound = 0.0 if vn < 0.0 else N_VMAX
            ts = (bound - v) / a
            s = s + (v * ts + 0.5 * a * ts * ts + bound * (N_H - ts)); v = bound
        else:
            s = s + (v * N_H + 0.5 * a * N_H * N_H); v = vn
        acc.append(a); jr.append((a - prev) / (N_H * 8)); ss.append(s); vs.append(v)
    vs_ = np.array(vs); acc_ = np.array(acc); jr_ = np.array(jr)
    cost = float(np.mean(((vs_[1:] - desired) / max(desired, 1)) ** 2) + 0.05 * np.mean((acc_ / 5) ** 2) + 0.02 * np.mean(jr_ ** 2))
    return dict(targets=(float(first), float(second)), s=np.array(ss), v=vs_, cost=cost)


def n_library(v0, a0, desired):
    """The 17 rows in cost order: the 16 target pairs plus the state-dependent row (target K (desired - v) + L a, limited to
    [-5, 2], then 0). Order: cost, then the target pair."""
    rows = [n_row(a, b, v0, a0, desired) for a in N_TARGETS for b in N_TARGETS]
    den = 629. / 800. + (29. / 6000.) * desired ** 2
    K = (101. / 120.) / den; Lc = (desired ** 2 / 480.) / den
    rows.append(n_row(max(-5., min(2., K * (desired - v0) + Lc * a0)), 0., v0, a0, desired))
    rows.sort(key=lambda r: (r['cost'], r['targets']))
    return rows


def n_support(nx, ny, yaw, hl, hw):
    c, s = math.cos(yaw), math.sin(yaw)
    return hl * abs(nx * c + ny * s) + hw * abs(-nx * s + ny * c)


def n_crit_f0(row, actors, now, ego_len, ego_wid, pbar):
    """F0's critical scale of one row: the largest g with d >= 0 and g * s <= d^2 at every constraint, where
      d = the planner's nominal distance of the constraint (separation along the constraint normal minus both half supports minus
          the reserve), from the logged track states;
      s = z' P-bar z, the class-average covariance projected on the normal with look-ahead te (z = [n, n te]), floored at 0.
    -inf if some d < 0; +inf if no constraint has s > 0 (or there is no tracked actor). Constraints: per tracked actor 60 segments x 2
    end points."""
    best = math.inf
    s_ego = row['s']; v_ego = row['v']
    for o in actors:
        age = now - o['state_time']
        Pb = pbar['pedestrian' if o['name'] == 'pedestrian' else 'vehicle']
        vx, vy = float(o['vx']), float(o['vy']); spd = math.hypot(vx, vy)
        # numpy's own arange * h + age, to have the same tick times as the planner (0.05 j in binary64)
        t = list(np.arange(N_STEPS + 1) * N_H + age)
        mx = [o['x'] + tt * vx for tt in t]; my = [o['y'] + tt * vy for tt in t]
        for j in range(N_STEPS):
            ax = 0.5 * (mx[j] + mx[j + 1] - s_ego[j] - s_ego[j + 1]); ay = 0.5 * (my[j] + my[j + 1])
            ln = math.sqrt(ax * ax + ay * ay)
            if ln > 1e-12: nx, ny = ax / ln, ay / ln
            else: nx, ny = 1.0, 0.0
            shape = n_support(nx, ny, 0.0, ego_len / 2, ego_wid / 2) + n_support(nx, ny, o['yaw'], o['length'] / 2, o['width'] / 2)
            reserve = (max(v_ego[j], v_ego[j + 1]) + spd) * N_H / 2 + 0.01
            for off in (0, 1):
                te = t[j + off]
                d = (mx[j + off] - s_ego[j + off]) * nx + my[j + off] * ny - shape - reserve
                if d < 0.0:
                    return -math.inf
                z = (nx, ny, nx * te, ny * te)
                sv = 0.0
                for i in range(4):
                    for q in range(4):
                        sv += z[i] * Pb[i][q] * z[q]
                if sv > 0.0:
                    c = d * d / sv
                    if c < best: best = c
    return best


def n_select(crit, rows, g):
    """The planner's rule at caution scale g: the first row in cost order whose critical scale is >= g; if none, the fallback row
    (targets (-5, -5))."""
    for i, c in enumerate(crit):
        if c >= g:
            return i, False
    return next(i for i, r in enumerate(rows) if r['targets'] == N_FALLBACK), True


def n_corners(cx, cy, h, hl, hw):
    c, s = math.cos(h), math.sin(h)
    return [(cx + sx * hl * c - sy * hw * s, cy + sx * hl * s + sy * hw * c) for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1))]


def n_pt_seg(p, a, b):
    ex, ey = b[0] - a[0], b[1] - a[1]; wx, wy = p[0] - a[0], p[1] - a[1]
    ee = ex * ex + ey * ey
    t = 0.0 if ee <= 0.0 else min(1.0, max(0.0, (wx * ex + wy * ey) / ee))
    return math.hypot(wx - t * ex, wy - t * ey)


def n_overlap(A, B):
    """True if the two rectangles overlap or touch: no edge direction of either separates them strictly."""
    for Pn in (A, B):
        for i in range(4):
            ex, ey = Pn[(i + 1) % 4][0] - Pn[i][0], Pn[(i + 1) % 4][1] - Pn[i][1]
            pa = [-ey * x + ex * y for x, y in A]; pb = [-ey * x + ex * y for x, y in B]
            if max(pa) < min(pb) or max(pb) < min(pa):
                return False
    return True


def n_rect_dist(A, B):
    """Distance between two rectangles (corner lists): 0 when they overlap or touch, else the smallest corner-to-edge distance."""
    if n_overlap(A, B):
        return 0.0
    best = math.inf
    for P_, Q_ in ((A, B), (B, A)):
        for p in P_:
            for i in range(4):
                d = n_pt_seg(p, Q_[i], Q_[(i + 1) % 4])
                if d < best: best = d
    return best


def n_clearance(row, T, k, ego_len, ego_wid):
    """True clearance of one row over the 3 s commitment: the smallest distance, over the 61 plan ticks j = 0..60 and over every true
    scenario actor, between the ego box (truth centre at tick k moved by s_j along the route yaw; logged ego length and width) and the
    actor's true box at tick k + j. Also returned: the clearance to the lead (the truth log's target) alone, and the actor count."""
    ex, ey, yaw, lead, acts = T[k]
    ux, uy = math.cos(yaw), math.sin(yaw)
    per = {}
    for aid in acts:
        m = math.inf
        for j in range(N_STEPS + 1):
            fr = T.get(k + j)
            a = fr[4].get(aid) if fr is not None else None
            if a is None:
                break                                   # an actor counts until its first missing true frame (not expected)
            E = n_corners(ex + row['s'][j] * ux, ey + row['s'][j] * uy, yaw, ego_len / 2, ego_wid / 2)
            m = min(m, n_rect_dist(E, n_corners(*a)))
        per[aid] = m
    return min(per.values()) if per else math.inf, per.get(lead, math.nan), len(per)


def n_evaluated(T, k):
    """A decision is evaluated when the truth log has the lead at tick k and a full 3 s of true frames after it."""
    fr = T.get(k)
    return bool(fr is not None and fr[3] is not None and fr[3] in fr[4] and k + N_STEPS <= max(T))


def n_case(cap, k, pbar, T=None):
    """The whole new routine for one decision: -> dict(row selected at g = 1, its true clearance, ...)."""
    T = n_truth(cap) if T is None else T
    dec = n_decision(cap, k)
    ms = dec['model_state']
    rows = n_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], dec['desired_mps'])
    assert len(rows) == 17
    crit = [n_crit_f0(r, dec['actors'], dec['now'], dec['ego_length'], dec['ego_width'], pbar) for r in rows]
    sel, fb = n_select(crit, rows, G1)
    cl_all, cl_lead, n_act = n_clearance(rows[sel], T, k, dec['ego_length'], dec['ego_width'])
    return dict(row=int(sel), fallback=bool(fb), targets=list(rows[sel]['targets']), crit_selected=float(crit[sel]), crit=[float(c) for c in crit],
                clearance=float(cl_all), clearance_lead_only=float(cl_lead), n_true_actors=int(n_act), n_tracked_actors=len(dec['actors']),
                evaluated=n_evaluated(T, k))


# =====================================================================================================================================
# PART R: reference and selection (arrays of record + scoring library)
# =====================================================================================================================================
def r_setup():
    sys.dont_write_bytecode = True
    p = str(CD / 'analysis')
    if p not in sys.path: sys.path.insert(0, p)
    import cd_common_v13 as CC
    return CC


def r_runs(test_old):
    """Per run (ascending run id): dict(run, cap (capture folder), k, ev, ph (truth phase of record), cF0, idx55, clear)."""
    CC = r_setup()
    out = []
    if test_old:
        for r in sorted(CC.load_old_lead(), key=lambda r: r['run']):
            capr = OLD_ARCH / r['run'] / 'x' / r['run'] / 'capture'
            out.append(dict(run=r['run'], capr=capr, k=np.asarray(r['k']), ev=np.asarray(r['ev'], bool), ph=np.asarray(r['ph']),
                            cF0=np.asarray(r['crit']['F0'], float), idx55=np.asarray(r['idx55']).astype(np.int64), clear=np.asarray(r['clear_raw'], float)))
    else:
        for rid in CC.c_run_ids('lead_braking'):
            z = np.load(ARR / (rid + '.npz'), allow_pickle=False)
            out.append(dict(run=rid, capr=RUNS / rid / rid / 'capture', k=z['k'], ev=z['evaluated'].astype(bool), ph=z['phase'],
                            cF0=np.asarray(z['cF0'], float), idx55=z['idx55'].astype(np.int64), clear=np.asarray(z['clear'], float)))
    assert [r['run'] for r in out] == sorted(r['run'] for r in out)
    return out, CC


def r_cap(capr):
    caps = [d for d in capr.iterdir() if d.is_dir()]
    if len(caps) != 1:
        raise RuntimeError('expected one capture folder in %s, found %d' % (capr, len(caps)))
    return caps[0]


def select_cases(runs):
    """A10 sec. 10.2 selection (README_HAND_CHECK.md, 'Selection rule'). Returns the list of (run index, decision index, phase)."""
    rng = np.random.default_rng(SEED)
    picked = []; pool = {}
    for p, size in zip((0, 1, 2), SIZES):
        cand = [(ri, int(di)) for ri, r in enumerate(runs) for di in np.flatnonzero(r['ev'] & (r['ph'] == p))]
        pool[p] = len(cand)
        take = min(size, len(cand))
        idx = np.sort(rng.choice(len(cand), size=take, replace=False)) if take else np.zeros(0, int)
        picked += [(cand[i][0], cand[i][1], p) for i in idx]
    return picked, pool


def r_reference(CC, r, di):
    """Scoring library of record: F0's selection at g = 1 and the stored true clearance of that row."""
    sel = CC.L.select_grid(r['cF0'][di:di + 1], np.array([G1]), r['idx55'][di:di + 1])
    row = int(sel[0, 0])
    return row, float(r['clear'][di, row]), float(r['cF0'][di, row])


def main():
    args = sys.argv[1:]
    test_old = '--test-old' in args
    tag = ('_' + args[args.index('--tag') + 1]) if '--tag' in args else ''
    if not test_old and not (LOCK2.is_file() and (V13 / 'LOCK_A10_2c.txt').is_file()):   # two-stage Lock 2 (20 Nov, CD lead): stage 2
        raise SystemExit('REFUSED: %s and LOCK_A10_2c.txt must both exist; no value of a fresh run may be computed (A10 sec. 4, 5.2)' % LOCK2)
    name = ('TESTOLD_' if test_old else '') + 'HAND_CHECK_v13' + tag
    out_json = OUT / (name + '.json'); out_log = OUT / (name + '_log.txt')
    if out_json.exists() or out_log.exists():
        raise SystemExit('REFUSED: %s or its log exists (outputs are never overwritten; use --tag)' % out_json)
    OUT.mkdir(parents=True, exist_ok=True)
    logf = open(out_log, 'x', encoding='utf-8')

    def log(msg):
        line = time.strftime('%Y-%m-%d %H:%M:%S ') + msg
        print(line, flush=True); logf.write(line + '\n'); logf.flush()

    t0 = time.time()
    runs, CC = r_runs(test_old)
    gate = CC.require_lock2(test_old)
    log('hand check, %s; %d runs; %s' % ('TEST on the old evaluation runs' if test_old else 'fresh lead-braking runs', len(runs), gate))
    picked, pool = select_cases(runs)
    log('candidates per truth phase 0/1/2: %s; drawn %d' % ([pool[p] for p in (0, 1, 2)], len(picked)))
    pbar = json.loads(PBAR_RECORD.read_text(encoding='utf-8'))['Pbar']
    table = []; truth_cache = {}
    for ci, (ri, di, p) in enumerate(picked):
        r = runs[ri]; k = int(r['k'][di]); cap = r_cap(r['capr'])
        if ri not in truth_cache:
            truth_cache[ri] = n_truth(cap)
        new = n_case(cap, k, pbar, truth_cache[ri])                          # PART N: logs only
        ref_row, ref_clear, ref_crit = r_reference(CC, r, di)                 # PART R
        diff = abs(new['clearance'] - ref_clear)
        ok = bool(np.isfinite(diff) and diff <= TOL) or bool(new['clearance'] == ref_clear)
        table.append(dict(case=ci + 1, run=r['run'], decision_index=di, k=k, truth_phase=p, row_new=new['row'], row_reference=ref_row,
                          same_row=bool(new['row'] == ref_row), fallback_new=new['fallback'], targets_new=new['targets'],
                          clearance_new_m=new['clearance'], clearance_reference_m=ref_clear, abs_difference_m=float(diff), within_tolerance=ok,
                          crit_F0_selected_new=new['crit_selected'], crit_F0_selected_reference=ref_crit,
                          clearance_lead_only_new_m=new['clearance_lead_only'], n_true_actors=new['n_true_actors'],
                          n_tracked_actors=new['n_tracked_actors'], evaluated_new=new['evaluated']))
        log('case %2d %s k=%d phase %d: row new %d / ref %d; clearance new %.9f / ref %.9f m; |diff| %.3e %s' % (
            ci + 1, r['run'], k, p, new['row'], ref_row, new['clearance'], ref_clear, diff, 'ok' if ok else 'DIFFERS'))
    n = len(table); n_ok = sum(t['within_tolerance'] for t in table)
    status = ('all %d within 1e-6 m' % n) if n_ok == n else ('%d of %d within 1e-6 m' % (n_ok, n))
    fin = [t['abs_difference_m'] for t in table if np.isfinite(t['abs_difference_m'])]
    doc = dict(family='lead_braking', program='hand_check_v13.py', test_old=test_old,
               values={'HAND.status': status},
               details=dict(
                   note=('TEST on the 35 old evaluation runs (exploratory data of record); not a fresh value' if test_old else
                         'A10 sec. 10.2 hand check on the fresh lead-braking runs'),
                   gate=gate, seed=SEED, sizes_by_truth_phase=list(SIZES), tolerance_m=TOL, caution_scale=G1,
                   selection_rule=('runs in ascending run id; candidates of phase p = decisions with evaluated == 1 and truth phase == p, ordered '
                                   'by (run id, decision index); one generator default_rng(20261917); for p = 0, 1, 2 in this order: '
                                   'rng.choice(n_p, size, replace=False) with sizes 7, 7, 6; drawn indices sorted ascending within the phase'),
                   n_runs=len(runs), candidates_by_truth_phase={str(p): pool[p] for p in (0, 1, 2)}, n_cases=n, n_within_tolerance=n_ok,
                   shortfall=int(sum(SIZES) - n), n_same_row=int(sum(t['same_row'] for t in table)),
                   n_evaluated_by_new_routine=int(sum(t['evaluated_new'] for t in table)),
                   n_lead_only_differs=int(sum(not (t['clearance_lead_only_new_m'] == t['clearance_new_m']) for t in table)),
                   max_abs_difference_m=float(max(fin)) if fin else None,
                   new_routine=('hand_check_v13.py PART N (json, math, numpy): frames.jsonl decision record -> 17 rows rebuilt -> F0 critical scale per '
                                'row with P-bar of record -> first row with critical scale >= 1, else the fallback row -> smallest box-to-box '
                                'distance to every true scenario actor over the 61 plan ticks from evaluation_truth.jsonl'),
                   reference=('old: cd_common_v13.load_old_lead() (gateR_rt_v01 arrays of record); ' if test_old else 'arrays/CV0/<rid>.npz; ') +
                             'optA_lib_v02.select_grid(cF0, [1.0], idx55); clear[decision, selected row]',
                   shared_inputs=['capture logs of the run (frames.jsonl, evaluation_truth.jsonl)', str(PBAR_RECORD),
                                  'k, evaluated and truth phase of the arrays of record (selection of the cases only)'],
                   pbar_sha256=CC.sha(PBAR_RECORD), lock2=None if test_old else gate, seconds=time.time() - t0, table=table))
    CC.write_once(out_json, doc)
    log('HAND.status = %s; max |difference| %.3e m; rows equal in %d of %d; wrote %s (%.0f s)' % (
        status, max(fin) if fin else float('nan'), doc['details']['n_same_row'], n, out_json, time.time() - t0))
    logf.close()


if __name__ == '__main__':
    main()
