"""v13 package B: summary of every package-B result on the stored runs and the A10 section 3 consequence rules, read from the output
files only (no number typed). New file, 19 Nov 2026 (Claude Opus 5.5).
Inputs: out\\banalysis\\B_<x>_v01.json (x = CV0, B3, B2, B4, B1, B1_d090, B1_d098), out\\b6\\B6_STOP_v01.json, out\\b9\\B9_CUTIN_lat1p75_v01.json,
out\\b3\\*.json, shared\\trackers\\trk_constants_v01.json, out\\imm2\\IMM_COMPARE_*.json, out\\b0\\*.
Outputs: out\\B_RESULTS_SUMMARY_v13.json and out\\B_RESULTS_SUMMARY_v13.md.
Changed 20 Nov 2026 ~01:08 EST by this machine's clock (coordinator OK in its message stamped 01:35 EST; recorded in work\\locks\\FREEZE_B_add2.json): adds the entry 'second_imm_fresh'
(A10 section 10.1(b) on five fresh lead-braking runs) read from out\\imm2\\IMM_COMPARE_fresh5_v01.json; the expected five run ids are
re-drawn here from ..\\CD_capture\\CASES_C_v13.json with the rule fixed in STATUS.md (19 Nov 21:10 EST). Until that file exists the entry
reads status 'pending' (all_pass None). Every other entry is unchanged.
Changed 20 Nov 2026 ~03:10 EST (coordinator decision of 20 Nov, laptop clock 02:57; recorded in FREEZE_B_add3): the old-run B6 of
record is now out\\fresh_testold\\B6_TESTOLD_v02.json, scored as A10 section 1 fixes it ("plans judged until the stop ends": v11's
extended clearance), entry 'B6' with 'scoring' stated; B6_STOP_v01.json (61-frame stop cache) moves to 'B6_v01_61frame_sensitivity',
labelled as a deviation found afterwards (A10 section 11, Table S4). Both entries have the same fields. Every other entry is unchanged.
Usage: python -I -B -X utf8 b_summary_v01.py
"""
import json, pathlib, time, csv, hashlib
HERE = pathlib.Path(__file__).resolve().parents[1]
OUT = HERE / 'out'
LIB = HERE.parent / 'shared' / 'trackers'
CASES = HERE.parent / 'CD_capture' / 'CASES_C_v13.json'
FRESH = OUT / 'imm2' / 'IMM_COMPARE_fresh5_v01.json'


def fresh_pick():
    """The five fresh runs of the A10 10.1(b) check: pc13_<case>_native ids of the lead-braking cases, sorted ascending;
    default_rng(20261917).choice(n, 5, replace=False), sorted (rule fixed 19 Nov 21:10 EST, before Lock 2)."""
    import numpy as np
    raw = CASES.read_bytes()
    ids = sorted('pc13_%s_native' % c['case'] for c in json.loads(raw.decode('utf-8'))['cases'] if c['family'] == 'lead_braking')
    idx = sorted(int(i) for i in np.random.default_rng(20261917).choice(len(ids), size=5, replace=False))
    return dict(cases_file=str(CASES.relative_to(HERE.parent)), cases_sha256=hashlib.sha256(raw).hexdigest(), n_lead_braking=len(ids),
                seed=20261917, idx=idx, run_ids=[ids[i] for i in idx])


def second_imm_fresh():
    pick = fresh_pick()
    e = dict(check='A10 section 10.1(b): library B1 (IMM, diag 0.95) vs the independent second IMM on five fresh lead-braking runs',
             file=FRESH.name, threshold_rel=1e-9, expected=pick)
    if not FRESH.exists():
        e.update(status='pending', all_pass=None)
        return e
    d = jload(FRESH)
    rid = [next((p for p in pathlib.Path(r['cap']).parts if p.startswith('pc13_')), None) for r in d['runs']]
    match = sorted(rid) == pick['run_ids']
    allp = bool(d['all_pass'])
    e.update(status=('pass' if (allp and match and d['diag'] == 0.95) else ('run set differs from the pick' if not match else 'fail')),
             all_pass=allp, diag=d['diag'], written=d['written'], runs=len(d['runs']), run_ids=rid, runs_match_pick=match,
             ids_identical_all=all(r['ids_identical'] for r in d['runs']), frames_equal_all=all(r['frames'] == r['frames_b'] for r in d['runs']),
             track_states=sum(r['track_states'] for r in d['runs']), car_states=sum(r['car_states'] for r in d['runs']),
             max_rel=max(r['P9_max_rel_diff'] for r in d['runs']), centre_max_abs=max(r['centre_max_abs_diff'] for r in d['runs']),
             velocity_max_abs=max(r['velocity_max_abs_diff'] for r in d['runs']))
    return e
VARS = ['CV0', 'B3', 'B2', 'B4', 'B1', 'B1_d090', 'B1_d098']
LABEL = {'CV0': 'online CV (N)', 'B3': 'B3 CV re-tuned', 'B2': 'B2 adaptive Q', 'B4': 'B4 CA', 'B1': 'B1 IMM 0.95',
         'B1_d090': 'B1 IMM 0.90', 'B1_d098': 'B1 IMM 0.98'}


def jload(p):
    return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))


def f(x, nd=4):
    if x is None:
        return 'n/a'
    try:
        return ('%.' + str(nd) + 'f') % x
    except TypeError:
        return str(x)


def ci(s, nd=4):
    return '%s [%s, %s]' % (f(s['point'], nd), f(s['ci'][0], nd), f(s['ci'][1], nd))


def main():
    S = dict(code='b_summary_v01.py', written=time.strftime('%Y-%m-%d %H:%M:%S'), status='exploratory (A10 section 3), old runs')
    const = jload(LIB / 'trk_constants_v01.json')
    S['constants'] = {k: const[k] for k in ('R_car_diag', 'kappa', 'sigma_a2', 'ca_acc_init_var', 'tuning')}
    # B0
    b0 = list(csv.DictReader(open(OUT / 'b0' / 'harness_match_b0_v13.csv', encoding='utf-8')))
    lb = [x for x in b0 if x['family'] == 'lead_braking']
    exact = lambda x: (x['tracks_exact'] == x['tracks_logged'] and x['actors_exact'] == x['actors_logged'] and x['algebra_exact'] == '1'  # noqa: E731
                       and x['events_exact'] == '1' and x['targets_exact'] == '1')
    S['B0a'] = dict(runs=len(b0), bit_identical=sum(1 for x in b0 if exact(x)), lead_braking_runs=len(lb),
                    lead_braking_bit_identical=sum(1 for x in lb if exact(x)),
                    max_abs_diff_other=max(float(x['tracks_max_abs_diff'] or 0) for x in b0 if not exact(x)) if any(not exact(x) for x in b0) else 0.)
    b0b = []
    for p in sorted((OUT / 'b0').glob('B0B_ARRAYS_part*_v01.jsonl')):
        b0b += [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
    S['B0b'] = dict(runs_checked=len(b0b), all_ok=sum(1 for x in b0b if x.get('all_ok')),
                    worst_abs=max((x.get('worst') or 0.) for x in b0b) if b0b else None,
                    failures=[x['run'] for x in b0b if not x.get('all_ok')])
    imm = sorted((OUT / 'imm2').glob('IMM_COMPARE_frozen_*.json'))
    if imm:
        d = jload(imm[-1])
        S['second_imm'] = dict(file=imm[-1].name, runs=len(d['runs']), all_pass=d['all_pass'],
                               max_rel=max(r['P9_max_rel_diff'] for r in d['runs']))
    S['second_imm_fresh'] = second_imm_fresh()
    # B1-B5 per variant
    V = {}
    for x in VARS:
        p = OUT / 'banalysis' / ('B_%s_v01.json' % x)
        if not p.exists():
            continue
        d = jload(p)
        a = d['intervals']['all']
        V[x] = dict(R_pp=a['R_pp'], R_deceq=a['R_deceq'], RR_N=a['RR_N'], RR_CK3=a['RR_CK3'], RR_NA=a['RR_NA'], RR_AM=a['RR_AM'],
                    RR_Q=a['RR_Q'], E5=a['RR_E5'], E5p=a['RR_E5p'], E5_minus_E5p=a['RR_E5_minus_E5p'], ceiling_c=a['RR_E5x'],
                    E5p_x=a['RR_E5px'], ratio=d['ratio_N_F0'], classification=d['classification_exploratory'],
                    efficiency=d.get('efficiency_r_over_c'),
                    after_stop_room_deceq=d['intervals']['tru_stopped']['R_deceq'] if 'tru_stopped' in d['intervals'] else dict(point=d['points']['tru_stopped']['R_deceq'], ci=[None, None]),
                    after_stop_room_est_deceq=d['intervals']['est_stopped']['R_deceq'] if 'est_stopped' in d['intervals'] else dict(point=d['points']['est_stopped']['R_deceq'], ci=[None, None]),
                    room_by_phase_deceq={pn: d['points'][pn]['R_deceq'] for pn in ('est_before', 'est_braking', 'est_stopped', 'tru_before',
                                                                                  'tru_braking', 'tru_stopped')},
                    grid=d['grid_points'], lag=d['lag_dx3_first_second_after_stop'], nis_nees=d['nis_nees_by_phase'],
                    b8a=d.get('b8a_after_stop_vhat_gt_0p5'))
    for x in V:                                   # N_x - E5_x on the same resamples (coordinator decision 19 Nov ~20:50: printed wherever
        po = OUT / 'banalysis' / ('%s_ORACLE_CHECK_v01.json' % x)   # a point lies above the oracle); E5q post hoc, supplement only
        if po.exists():
            o = json.loads(po.read_text(encoding='utf-8'))
            V[x]['N_minus_E5x'] = o['intervals']['diff_N_minus_E5x']
            V[x]['post_hoc_supplement_only'] = dict(label='POST HOC; supplement only; enters no classification',
                                                    RR_E5q=o['intervals']['RR_E5q'], N_minus_E5q=o['intervals']['diff_N_minus_E5q'],
                                                    share_rows_outside_E5_band=o['diagnostics']['share_rows_outside_band'],
                                                    ratio_q01_q99=o['diagnostics']['ratio_q01_q99'],
                                                    within_decision_spread=o['diagnostics']['within_decision_spread'])
    S['variants'] = V
    # B3 / B4 consequence rule (A10 B3 row; point values)
    if all(k in V for k in ('CV0', 'B3', 'B4')):
        base_as = V['CV0']['after_stop_room_deceq']['point']; base_ck = V['CV0']['RR_CK3']['point']
        tests = {}
        for k in ('B3', 'B4'):
            as_ = V[k]['after_stop_room_deceq']['point']; ck = V[k]['RR_CK3']['point']
            tests[k] = dict(after_stop_room=as_, online_after_stop_room=base_as, below_half=bool(as_ < 0.5 * base_as),
                            RR_CK3=ck, online_RR_CK3=base_ck, ck3_diff=ck - base_ck, ck3_differs_gt_0p10=bool(abs(ck - base_ck) > 0.10))
        dep = any(t['below_half'] or t['ck3_differs_gt_0p10'] for t in tests.values())
        S['B3_B4_rule'] = dict(tests=tests, outcome=('depends on filter tuning: the text gives both; the abstract conditions include filter tuning'
                                                    if dep else 'the mechanism persists with NIS near 2 and with a CA filter'),
                               note='B4 NIS window not reachable (sigma_a2 at the grid end); reported with the outcome')
    # B6: of record = A10 section 1 scoring (B6_TESTOLD_v02.json); the 61-frame v01 values = a labelled sensitivity
    def b6_entry(d):
        e = dict(terciles=[dict(name=t['name'], decel_min_max=t['decel_min_max'], room_ratio_WR_over_3s=t['room_ratio_WR_over_3s'],
                                WR_R_pp=t['W_R']['R_pp'], W1_R_pp=t['W1']['R_pp'], den0_deceq=t['W_R']['den0_deceq'],
                                evaluable=t['W_R']['evaluable_den0']) for t in d['terciles']],
                 delayed_stop=d['delayed_stop'])
        ev = [t for t in e['terciles'][1:] if t['evaluable']]
        e['statement_range'] = dict(evaluable_terciles=[t['name'] for t in ev],
                                    ratio_range=[min(t['room_ratio_WR_over_3s'] for t in ev), max(t['room_ratio_WR_over_3s'] for t in ev)] if ev else None,
                                    decel_range=[min(t['decel_min_max'][0] for t in ev), max(t['decel_min_max'][1] for t in ev)] if ev else None)
        return e
    p2 = OUT / 'fresh_testold' / 'B6_TESTOLD_v02.json'
    if p2.exists():
        d2 = jload(p2)
        if d2.get('stop') != 'ext':
            raise SystemExit('REFUSED: %s is not the A10 section 1 scoring' % p2)
        S['B6'] = b6_entry(d2)
        S['B6'].update(file='out/fresh_testold/B6_TESTOLD_v02.json', scoring='A10 section 1: plans judged until the stop ends (v11 extended clearance)',
                       RS075_rel=d2['RS075_rel'], DS_rel=d2['DS_rel'], reliance_all={a: d2['reliance']['all'][a]['share_safe_only_with_stop']
                                                                                    for a in ('F0', 'N', 'CK3')})
    if (OUT / 'b6' / 'B6_STOP_v01.json').exists():
        S['B6_v01_61frame_sensitivity'] = b6_entry(jload(OUT / 'b6' / 'B6_STOP_v01.json'))
        S['B6_v01_61frame_sensitivity'].update(file='out/b6/B6_STOP_v01.json', scoring='61-frame stop cache (judged over 3 s only)',
                                               label='deviation found afterwards (A10 section 11, Table S4): the B6 of record until 20 Nov; '
                                                     'A10 section 1 fixes the scoring judged until the stop ends')
    # B9
    if (OUT / 'b9' / 'B9_CUTIN_lat1p75_v01.json').exists():
        d = jload(OUT / 'b9' / 'B9_CUTIN_lat1p75_v01.json')
        S['B9'] = dict(lat_m=d['lat_m'], events_found=d['events_found'], rule=d['rule_18_of_20'],
                       window_n=sum(r['n_window'] for r in d['runs']),
                       window_strata={s: sum(r['window_strata'][s] for r in d['runs']) for s in ('<1s', '1-4s', '>=4s', 'untracked')},
                       window=d['gridless']['window'], young=d['gridless']['young'], all_evaluated=d['gridless']['all_evaluated'],
                       ratio_window=d['ratio_window_all'])
    (OUT / 'B_RESULTS_SUMMARY_v13.json').write_text(json.dumps(S, indent=1, default=float), encoding='utf-8')
    # markdown
    L = ['# Package B results on the stored runs (exploratory) — generated by code\\b_summary_v01.py, %s' % S['written'], '',
         'Values are read from the output files; intervals: first 2,000 resamples of the draw of record (gridless).', '']
    L += ['| Tracker | Room R_gl (pp) | RR_gl(N_x) | Amplitude-matched ranking oracle RR_gl(E5_x) (A10 "ceiling share" c_x) | m_x | A_x | within 5% | RR_gl(CK3_x) | After-stop room (dec-eq) | Lag (m) | Class (exploratory) |',
          '|---|---|---|---|---|---|---|---|---|---|---|']
    for x in VARS:
        if x not in V:
            continue
        v = V[x]
        L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s%s |' % (
            LABEL[x], ci(v['R_pp'], 3), ci(v['RR_N']), ci(v['ceiling_c']), f(v['ratio']['median']), f(v['ratio']['A'], 5),
            f(v['ratio']['share_within_5pct'], 3), ci(v['RR_CK3'], 3), ci(v['after_stop_room_deceq'], 1), f(v['lag']['median'], 2),
            v['classification']['classification'], '; barely varies' if v['classification']['barely_varies'] else ''))
    L += ['', '| Tracker | RR_gl(N_x) − RR_gl(E5_x) | Post hoc (supplement only): RR_gl(E5q) | RR_gl(N_x) − RR_gl(E5q) |', '|---|---|---|---|']
    for x in VARS:
        if x in V and 'N_minus_E5x' in V[x]:
            ph = V[x]['post_hoc_supplement_only']
            L.append('| %s | %s | %s | %s |' % (LABEL[x], ci(V[x]['N_minus_E5x']), ci(ph['RR_E5q']), ci(ph['N_minus_E5q'])))
    if 'B3_B4_rule' in S:
        L += ['', '**B3/B4 rule:** ' + S['B3_B4_rule']['outcome'] + '.']
    if 'B6' in S:
        L += ['', '**B6 (A10 section 1 scoring, judged until the stop ends):** ' + json.dumps(S['B6']['statement_range'], default=float)]
    if 'B6_v01_61frame_sensitivity' in S:
        L += ['', '**B6, 61-frame scoring (v01; deviation found afterwards, Table S4):** '
              + json.dumps(S['B6_v01_61frame_sensitivity']['statement_range'], default=float)]
    if 'B9' in S:
        L += ['', '**B9:** events %d/20; window %d decisions; strata %s; room in the window %s pp.' % (
            S['B9']['events_found'], S['B9']['window_n'], S['B9']['window_strata'], f(S['B9']['window']['R_pp'], 3))]
    sf = S['second_imm_fresh']
    if sf['status'] == 'pending':
        L += ['', '**Second IMM, five fresh runs (A10 §10.1(b)):** pending (%s not yet written); expected runs %s.' % (sf['file'], ', '.join(sf['expected']['run_ids']))]
    else:
        L += ['', '**Second IMM, five fresh runs (A10 §10.1(b)):** %s; %d runs (%s); runs match the pick: %s; track ids identical: %s; '
                  'worst relative P9 difference %.3g (threshold 1e-9).' % (sf['status'], sf['runs'], ', '.join(str(r) for r in sf['run_ids']),
                                                                        sf['runs_match_pick'], sf['ids_identical_all'], sf['max_rel'])]
    (OUT / 'B_RESULTS_SUMMARY_v13.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
