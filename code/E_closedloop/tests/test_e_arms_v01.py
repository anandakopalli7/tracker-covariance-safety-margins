"""E0 laptop checks of the online arms against the open-loop sources of record (no CARLA; stored design/old runs only).

Run: set OPENBLAS_CORETYPE=Haswell, then  python -I -B test_e_arms_v01.py [--runs N] [--all]
Uses the dev packet packets\\dev_packet_e_v01\\claude_smoke_v01 and the Codex workspace (read only) as the runtime root.

Checks, per assessment decision of stored lead-braking runs (tuning runs p2_c1109_tune_*, old evaluation runs p1b_fit_*):
  A1  constraints_full reproduces consumer.constraints_for_trajectory (d, p, q, tags, s, v, a, cost, targets) bit for bit
  A2  online critical scales equal the stored open-loop arrays: F0 (gateR_rt_v01 cF0), N (cN), CK3 (A4 extract cCK3),
      TG (v12 a9_7a cTG2; old evaluation runs only); reported as rows differing (exact) and max relative difference
  B1  the E policy (E_F0, E_N, E_CK3, E_TG at g in G_TEST), fed the logged decision inputs in tick order with its track
      history fed from the logged detections and filter events, selects the row the open-loop rule selects (first row
      whose stored critical scale >= g, else the fallback)
  B2  F2's plan acceleration equals design_core_v85.trajectory(targets, model speed, model acceleration)['a'][:2]
  C1  PS phase (online lead rule) against the stored a9_4a lead phase (old evaluation runs): agreement counts
Writes tests\\out\\TEST_E_ARMS_v01.json.
"""
import os
os.environ.setdefault('OPENBLAS_CORETYPE', 'Haswell')
import argparse, glob, hashlib, json, math, pathlib, sys, time
import numpy as np

E = pathlib.Path(__file__).resolve().parents[1]
PK = E / 'packets' / 'dev_packet_e_v01' / 'claude_smoke_v01'
W = pathlib.Path(r'<library folder>')
PRJ = pathlib.Path(r'<library folder>')
SHIMS = PRJ / '09_redesign' / 'm4_perception_model' / 'shims_v01'
GATER = PRJ / '09_redesign' / 'm2_decisions' / 'openloop' / 'gateR_rt_v01'
A4T = PRJ / '11_ojits' / 'A4' / 'dryrun' / 'extract'
A4F = PRJ / '11_ojits' / 'A4' / 'fit' / 'extract'
V12 = pathlib.Path(r'ARS_TRIAL\revision_v12\analysis\out')
OUTD = E / 'tests' / 'out'
G_TEST = (0., 0.25, 1., 4., 16.)

os.environ['CLAUDE_SMOKE_WORKSPACE_ROOT'] = str(W)
sys.path.insert(0, str(PK))
sys.path.append(str(SHIMS))
sys.dont_write_bytecode = True
import e_arms_v01 as earms          # noqa: E402
import e_sources_v01 as es          # noqa: E402
native = earms.native
import consumer                      # noqa: E402  (the module the native policy uses)
import finite_primitive              # noqa: E402
from design_core_v85 import trajectory, support   # noqa: E402

BOUND = ['149_supported_sensor_preparation_20261101/code/consumer.py', '149_supported_sensor_preparation_20261101/code/finite_primitive.py',
         '149_supported_sensor_preparation_20261101/code/sensor_policy.py', '149_supported_sensor_preparation_20261101/code/sensor_execution.py',
         '149_supported_sensor_preparation_20261101/code/acceleration_servo.py', '149_supported_sensor_preparation_20261101/code/execution_core.py',
         '149_supported_sensor_preparation_20261101/code/pi_servo.py', '149_supported_sensor_preparation_20261101/code/forward_state_interface.py',
         '149_supported_sensor_preparation_20261101/code/online_tracker.py', '149_supported_sensor_preparation_20261101/vendor/design_core_v85.py',
         '711_native_decision_capture_20261103/native_capture_v02.py', '712_sensor_capture_integration_20261103/policy_capture_v01.py',
         '807_shared_model_runtime_20261104/shared_policy_v01.py', '747_full_scenario_binding_20261103/outcome_bridge_v01.py']


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def jl(p):
    with open(p, encoding='utf-8') as f:
        for line in f:
            if line.strip(): yield json.loads(line)


def binding_check():
    b = json.loads((PK / 'RUNTIME_SOURCE_BINDING_SMOKE_v01.json').read_text(encoding='utf-8'))
    m = {f['path']: f['sha256'] for f in b['files']}
    out = {}
    for rel in BOUND:
        if '<excluded folder 1>' in rel or '80_decision' in rel: continue
        loc = W / rel
        out[rel] = dict(bound=m.get(rel), local=sha(loc) if loc.exists() else None)
        out[rel]['equal'] = out[rel]['bound'] == out[rel]['local']
    return out


def runs():
    tune = []
    for rd in sorted((PRJ / '08_phase2' / 'archives_c1').glob('p2_c1109_tune_*')):
        cap = next((rd / 'x' / rd.name / 'capture').iterdir())
        if json.loads((cap / 'contract.json').read_text(encoding='utf-8'))['case']['draw']['family'] == 'lead_braking':
            tune.append(('tune', rd.name, cap))
    fit = []
    for rd in sorted((PRJ / '07_fit_runs' / 'archives').glob('p1b_fit_finite_*')):
        if not (V12 / 'tg' / (rd.name + '.npz')).exists(): continue
        cap = next((rd / 'x' / rd.name / 'capture').iterdir())
        fit.append(('fit', rd.name, cap))
    return tune, fit


def first_ok(crit, g, idx55):
    for r, c in enumerate(crit):
        if c >= g: return r
    return -1


def events_prefix(events, i):
    """The events the probe's list holds after detector update i: the logged file in order, up to (not including) the first
    event stamped with a later detector update; unstamped events (reset) are kept in place."""
    out = []
    for e in events:
        if 'timestamp' in e and int(e['timestamp']) > i:
            break
        out.append(e)
    return out


class Feed:
    """Logged detector updates and filter events in order, released up to a decision tick."""

    def __init__(self, cap):
        self.det = list(jl(cap / 'detections.jsonl'))
        ev = list(jl(cap / 'filter_events.jsonl')) if (cap / 'filter_events.jsonl').exists() else []
        self.events = ev; self.i = 0

    def advance(self, hist_owner, k):
        while self.i < len(self.det) and self.det[self.i]['k'] <= k:
            upto = events_prefix(self.events, self.i)
            hist_owner.on_detector(self.det[self.i]['tracks'], upto); self.i += 1


def decisions(cap):
    init = json.loads((cap / 'initial_command.json').read_text(encoding='utf-8'))
    out = [init['decision']]
    for fr in jl(cap / 'frames.jsonl'):
        ex = fr.get('execution')
        if ex and ex.get('new_decision'): out.append(ex['new_decision'])
    return out


def check_run(kind, name, cap, res):
    t0 = time.time()
    zr = np.load(GATER / (name + '.npz'), allow_pickle=False)
    za = np.load((A4T if kind == 'tune' else A4F) / (name + '.npz'), allow_pickle=False)
    zt = np.load(V12 / 'tg' / (name + '.npz'), allow_pickle=False) if kind == 'fit' else None
    zl = np.load(V12 / 'lead' / (name + '.npz'), allow_pickle=False) if kind == 'fit' else None
    decs = decisions(cap)
    case = json.loads((cap / 'contract.json').read_text(encoding='utf-8'))['case']
    desired = float(case['desired_mps'])
    L, Wd = decs[0]['ego_length'], decs[0]['ego_width']
    pbar, _ = earms.load_pbar('CANMOT')
    r = dict(run=name, kind=kind, decisions=0, A1_rows=0, A1_rows_differ=0)
    for src in ('F0', 'N', 'CK3', 'TG'): r['A2_' + src + '_rows_differ'] = 0; r['A2_' + src + '_maxrel'] = 0.
    # ---- A1, A2 with a plain online history (no policy)
    feed = Feed(cap); ctx = earms.ECtx('E_F0', dict(g=1., triple=None, brake_from_k=None), pbar, desired)
    asm = [d for d in decs if d['mode'] == 'assessment']
    ks = np.array([d['tick'] for d in asm]); assert (ks == zr['k']).all() and (ks == za['k']).all()
    for di, d in enumerate(asm):
        feed.advance(ctx, d['tick'])
        ms = d['model_state']; actors = d['actors']; now = d['now']
        diag = consumer.Diagnostics()
        rows_nat = finite_primitive.build_library(ms['model_speed_mps'], ms['model_acceleration_mps2'], desired, actors, L, Wd, now, diag)
        rows_e = []
        for rn in rows_nat:
            tr = trajectory(*rn['targets'], ms['model_speed_mps'], ms['model_acceleration_mps2'], desired)
            if 'prototype_primitive' in rn: tr['prototype_primitive'] = rn['prototype_primitive']
            rows_e.append(es.constraints_full(consumer, support, tr, actors, L, Wd, now, consumer.Diagnostics()))
        for a, b in zip(rows_nat, rows_e):
            r['A1_rows'] += 1
            same = all(np.array_equal(np.asarray(a[k]), np.asarray(b[k])) for k in ('d', 'p', 'q', 's', 'v', 'a')) and a['tags'] == b['tags'] \
                and a['cost'] == b['cost'] and a['targets'] == b['targets']
            r['A1_rows_differ'] += int(not same)
        crit = {}
        for src in ('F0', 'N', 'CK3', 'TG'):
            crit[src] = np.array([es.crit_row(*es.apply_source(tr, actors, now, src, pbar, ctx.hist)) for tr in rows_e])
        stored = dict(F0=zr['cF0'][di], N=zr['cN'][di], CK3=za['cCK3'][di])
        if zt is not None: stored['TG'] = zt['cTG2'][di]
        for src, sv in stored.items():
            mine = crit[src]
            eq = (mine == sv) | (np.isnan(mine) & np.isnan(sv))
            r['A2_' + src + '_rows_differ'] += int((~eq).sum())
            fin = np.isfinite(mine) & np.isfinite(sv) & (sv != 0)
            if fin.any(): r['A2_' + src + '_maxrel'] = max(r['A2_' + src + '_maxrel'], float(np.max(np.abs(mine[fin] - sv[fin]) / np.abs(sv[fin]))))
        r['decisions'] += 1
    # ---- B1, B2: the E policies themselves, fed in tick order
    stored_full = dict(E_F0=zr['cF0'], E_N=zr['cN'], E_CK3=za['cCK3'])
    if zt is not None: stored_full['E_TG'] = zt['cTG2']
    for arm, S in stored_full.items():
        for g in G_TEST:
            ctx2 = earms.ECtx(arm, earms.check_knobs(arm, g), pbar, desired)
            pol = earms._policy_class(ctx2)('finite', desired, L, Wd, g, 0.)
            feed2 = Feed(cap); di = 0; agree = 0; n = 0; f2_bad = 0
            for d in decs:
                feed2.advance(ctx2, d['tick'])
                ms = d['model_state']
                res_d = pol.step(d['tick'], ms['raw_speed_mps'], ms['raw_acceleration_mps2'], d['steer'], d['now'], d['actors'])
                if res_d['mode'] != 'assessment': continue
                out = res_d['output']; exp = first_ok(S[di], g, None)
                got = -1 if out['fallback'] else out['candidate']
                agree += int(got == exp); n += 1
                tr = trajectory(*out['targets'], res_d['model_state']['model_speed_mps'], res_d['model_state']['model_acceleration_mps2'], desired)
                f2_bad += int(not np.array_equal(np.asarray(tr['a'][:2]), ctx2.f2_plan['a_cmd']))
                di += 1
            r.setdefault('B1', {})['%s@%g' % (arm, g)] = [agree, n]
            r.setdefault('B2_f2_plan_mismatch', 0); r['B2_f2_plan_mismatch'] += f2_bad
    # ---- C1: PS phase (online lead rule) against the stored a9_4a phase
    if zl is not None:
        ctx3 = earms.ECtx('E_PS', earms.check_knobs('E_PS', triple=[1., 1., 1.]), pbar, desired)
        feed3 = Feed(cap); agree = same_lead = n = 0; confusion = {}
        for d in asm:
            feed3.advance(ctx3, d['tick'])
            ph, info = es.phase_of(d['actors'], d['now'], ctx3.hist)
            i = n; n += 1
            sp = int(zl['phase'][i]) if np.isfinite(zl['phase'][i]) else -1
            confusion['%d|%d' % (sp, ph)] = confusion.get('%d|%d' % (sp, ph), 0) + 1
            agree += int(sp == ph)
            if info.get('track_id') is not None and bool(zl['lead_found'][i]) and int(zl['track_id'][i]) == info['track_id']: same_lead += 1
        r['C1_phase_agree'] = [agree, n]; r['C1_same_lead_track'] = same_lead; r['C1_confusion_stored|online'] = confusion
    r['seconds'] = round(time.time() - t0, 1)
    res.append(r); print(json.dumps(r), flush=True)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--runs', type=int, default=3); ap.add_argument('--start', type=int, default=0); ap.add_argument('--all', action='store_true')
    a = ap.parse_args()
    OUTD.mkdir(parents=True, exist_ok=True)
    out = dict(schema='E_TEST_ARMS_V01', utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), binding=binding_check(), runs=[])
    print(json.dumps(out['binding'], indent=0))
    tune, fit = runs()
    sel = (tune + fit) if a.all else (tune[a.start:a.start + a.runs] + fit[a.start:a.start + a.runs])
    for kind, name, cap in sel:
        check_run(kind, name, cap, out['runs'])
    tot = {}
    for r in out['runs']:
        for k, v in r.items():
            if k.endswith('_rows_differ') or k in ('A1_rows', 'decisions', 'B2_f2_plan_mismatch'): tot[k] = tot.get(k, 0) + v
            if k.endswith('_maxrel'): tot[k] = max(tot.get(k, 0.), v)
            if k == 'B1':
                for kk, (ag, n) in v.items():
                    t = tot.setdefault('B1', {}).setdefault(kk, [0, 0]); t[0] += ag; t[1] += n
            if k == 'C1_phase_agree': t = tot.setdefault('C1_phase_agree', [0, 0]); t[0] += v[0]; t[1] += v[1]
    out['totals'] = tot
    tag = 'all' if a.all else 's%dn%d' % (a.start, a.runs)
    (OUTD / ('TEST_E_ARMS_%s_v01.json' % tag)).write_text(json.dumps(out, indent=1), encoding='utf-8')
    print('TOTALS', json.dumps(tot, indent=1))


if __name__ == '__main__':
    main()
