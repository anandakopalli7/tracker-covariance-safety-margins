"""Recount (second program): assemble RECOUNT_RESULTS_v01.json (index, the item files, one flat entry per number) and
RECOUNT_REPORT_v01.md from the per-item JSON files. Reads nothing outside this folder."""
import json, pathlib, time

H = pathlib.Path(__file__).resolve().parent
FILES = dict(anchor='rc_anchor_v01_out.json', item1='RECOUNT_item1_v01.json', item2='RECOUNT_item2_v01.json',
             item3='RECOUNT_item3_v01.json', item4='RECOUNT_item4_v01.json', item5_single='RECOUNT_item5_single_v01.json',
             item5_double='RECOUNT_item5_double_v01.json', item6='RECOUNT_item6_v01.json')
FIVE = ('N', 'NA', 'AM', 'CK3', 'Q')


def ld(name):
    return json.loads((H / name).read_text(encoding='utf-8'))


def flatten(o, pre, out):
    if isinstance(o, dict):
        for k, v in o.items():
            flatten(v, pre + '|' + str(k), out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            flatten(v, pre + '|' + str(i), out)
    elif isinstance(o, bool) or o is None or isinstance(o, str):
        return
    elif isinstance(o, (int, float)):
        out[pre] = o


def f(x, nd=4):
    if x is None:
        return 'n/a'
    return ('%.' + str(nd) + 'f') % x


def ci(e, nd=4):
    c = e.get('ci') if isinstance(e, dict) else e
    if c is None:
        return 'n/a'
    return '[%s, %s]' % (f(c[0], nd), f(c[1], nd))


def pc(e, nd=4):
    s = f(e['point'], nd)
    if 'ci' in e:
        s += ' ' + ci(e, nd)
        if e.get('n_left_out'):
            s += ' (%d left out)' % e['n_left_out']
    return s


def main():
    J = {k: ld(v) for k, v in FILES.items()}
    flat = {}
    for k in FILES:
        flatten(J[k], k, flat)
    res = dict(written=time.strftime('%Y-%m-%d %H:%M:%S'), program='recount (independent second program), rc_*_v01.py',
               index=FILES, n_flat_entries=len(flat), flat=flat)
    res.update(J)
    (H / 'RECOUNT_RESULTS_v01.json').write_text(json.dumps(res, indent=1), encoding='utf-8')

    a = J['anchor']; L = []
    w = L.append
    w('# Recount report (independent second program), revision v11')
    w('')
    w('Written %s by the second program. Code: `rc_lib_v01.py`, `rc_anchor_v01.py`, `rc_items_v01.py`, `rc_item4_v01.py`, `rc_double_v01.py`, `rc_report_v01.py` (this folder). '
      'All numbers below are in `RECOUNT_RESULTS_v01.json` (%d numeric entries; per-item files listed in its `index`).' % (res['written'], len(flat)))
    w('')
    w('## 0. Independence')
    w('The code was written from `RECOUNT_BRIEF_v01.md` and `AMENDMENT_08_ARS_REVISION_v01.md`. It reads the stored arrays with numpy and imports nothing from the data project. '
      '`optA2_lib_v02.py` and `optA2_main_v02.py` (the project\'s own second-program lineage, allowed by the brief) were read for the definitions; nothing was imported from them. '
      'Nothing under `revision_v11\\analysis\\` or `11_ojits\\A6R\\code\\` was opened before this report and the results file were written. '
      'One file outside the listed inputs was consulted: `11_ojits\\review\\optionA_recount_v01\\OPTIONA_SECOND_REPORT_v02.txt` and `..._RESULTS_v02.json` (the earlier second program\'s outputs), for one value only, the reaction-and-stop den0 (see the anchor).')
    w('')
    w('## 1. Anchor check (3 s commitment, all evaluated decisions, step frontier, 35 runs)')
    w('')
    w('| quantity | published | recount | reproduces to the printed digits |')
    w('|---|---|---|---|')
    P = a['W1_point_all']; C = a['W1_ci_all']; R = a['RS_point_all']

    def row(name, pub, mine_s, ok):
        w('| %s | %s | %s | %s |' % (name, pub, mine_s, 'yes' if ok else 'NO'))

    def chk(vals, pubs, nd):
        return all(round(v, nd) == p for v, p in zip(vals, pubs))
    oks = []
    ok = a['n_eval'] == 8290; oks.append(ok); row('evaluated decisions', '8,290', '%d' % a['n_eval'], ok)
    pcnt = a['phase_counts']; ok = [pcnt['0'], pcnt['1'], pcnt['2']] == [678, 755, 6857]; oks.append(ok)
    row('phase decision counts', '678 / 755 / 6,857', '%d / %d / %d (phase 3: %d)' % (pcnt['0'], pcnt['1'], pcnt['2'], pcnt['3']), ok)
    ok = chk([P['R_pp']] + C['R_pp'], [5.5568, 4.4986, 6.6038], 4); oks.append(ok)
    row('room R (pp)', '5.5568 [4.4986, 6.6038]', '%.6f [%.6f, %.6f]' % (P['R_pp'], C['R_pp'][0], C['R_pp'][1]), ok)
    ok = chk([P['RR_N']] + C['RR_N'], [0.00122, -0.00108, 0.00119], 5); oks.append(ok)
    row('RR(N)', '0.00122 [-0.00108, 0.00119]', '%.7f [%.7f, %.7f]' % (P['RR_N'], C['RR_N'][0], C['RR_N'][1]), ok)
    for nm, pub in (('NA', [0.0167, 0.0073, 0.0252]), ('CK3', [0.8315, 0.7528, 0.9033]), ('AM', [0.3758, 0.3156, 0.4254])):
        ok = chk([P['RR_' + nm]] + C['RR_' + nm], pub, 4); oks.append(ok)
        row('RR(%s)' % nm, '%.4f [%.4f, %.4f]' % tuple(pub), '%.6f [%.6f, %.6f]' % (P['RR_' + nm], C['RR_' + nm][0], C['RR_' + nm][1]), ok)
    ok = chk([P['den0']], [1205.2352], 4); oks.append(ok); row('den0 (sum over 201 levels)', '1205.2352', '%.6f' % P['den0'], ok)
    ok_rs = chk([R['den0']], [141.0132], 4)
    row('reaction-and-stop tau 0.75 s, 6 m/s2: den0 (sum)', '141.0132', '%.8f' % R['den0'], ok_rs)
    ok = chk([R['RR0_CK3']], [0.9357], 4); oks.append(ok); row('reaction-and-stop: RR0(CK3)', '0.9357', '%.6f' % R['RR0_CK3'], ok)
    w('')
    w('Result: %d of %d anchor values reproduce to the printed digits. ' % (sum(oks) + int(ok_rs), len(oks) + 1)
      + ('' if ok_rs else 'The one that does not is the reaction-and-stop den0: the recount gives %.8f, which rounds to 141.0133, while the task statement prints 141.0132. '
         'The project\'s earlier second program records 141.01326899879373 (printed there as 141.0133), identical to the recount to every digit, '
         'so the printed 141.0132 is the same number truncated instead of rounded; it is a 1e-4 presentation difference and not a scoring difference. The run was continued.' % R['den0']))
    w('')
    w('Other checks made at the anchor: no NaN clearance inside the evaluated set (3 s: %d, cache: %d), so the "NaN = -1" rule is never used; '
      'the levels equal `numpy.linspace` bit for bit (%s); no frontier is undefined at any level in the point or in any of the 20,000 resamples (%d resamples with an undefined level); '
      'stored decisions %d; moving decisions %d; of the truly safe rows, %d of %d are faster than the first truly safe row (negative caution terms exist).'
      % (a['nan_clear_in_evaluated'], a['nan_cache_in_evaluated'], a['levels_equal_numpy_linspace'], C['n_nan_resamples'], a['n_stored'], a['moving'],
         a['negative_caution_terms_among_safe_rows'][0], a['negative_caution_terms_among_safe_rows'][1]))
    w('')
    w('## 2. Interpretations made (where the brief leaves a choice)')
    for s in [
        'Runs: the 35 names `p1b_fit_finite_0005` to `_0039`; each file\'s metadata was checked (family lead_braking, set fit). Desired speed: the stored per-decision `des`, checked equal to `meta.desired`.',
        'Wrong go under the reaction-and-stop scoring: the selected row\'s cache clearance is <= G, counted for every evaluated decision (the brief\'s wording). The earlier second-program library counts it only where some row is safe; the two differ by the same count for every arm and scale, so D, den and RR are unchanged.',
        'Caution axis: always the 3 s clearance (truly safe = `clear` > G), also when the wrong go is scored by reaction-and-stop. With G = 2 m both the wrong go and the truly safe rows use the 2 m requirement (Amendment R17).',
        'Signed caution (item 1): sum of the signed differences over the population\'s decisions that have a truly safe row, divided by their number; the wrong-go share is over all evaluated decisions of the population. Levels are built from the signed cautions. The oracle O has signed caution 0 and gets F0\'s zero-margin point; because F0\'s zero-margin signed caution is negative, the levels below 0 see only that prepended point, so den0 can be smaller than denE (it is in: %s). Reported as computed.' % ', '.join(k for k, v in J['item1']['pops'].items() if v['RR0_E']['point'] is not None and v['RR0_E']['point'] > 1),
        'Undefined frontier (no point of the arm with caution <= level): kept as NaN and counted; it never occurred in any analysis here.',
        'Phase-weighted aggregate: sum over phases 0-2 of (n_p / n) D_p with n = n_0 + n_1 + n_2, recomputed in every resample, an empty phase contributing 0. RR = aggregated D / aggregated denE; RR0 = aggregated D / aggregated den0; R = aggregated denE / 201; decision-equivalents = aggregated den0 / 201 / 100 * n.',
        'Intervals: numpy percentiles (linear interpolation) at 2.5 and 97.5 over the resamples; ratios over the resamples whose own denominator is positive (denE for RR, den0 for RR0), the others counted as "left out". Decision-equivalent intervals scale each resample by its own n.',
        'Item 2: E stays the stored oracle margin source (`cE`); it is not re-derived for the 2 m requirement, so denE can be negative there. O is the first row whose scoring clearance is > 2 m, else the fallback.',
        'Item 3: k_stop is taken from the stored decisions (evaluated or not), as the brief says. The condition (k - k_stop) * 0.05 < T was evaluated in floating point and as the integer condition k - k_stop < 20 T; the two agree for every decision. Every run has a phase-2 decision, and no phase-0 or phase-1 decision lies after k_stop. In 5 runs the first stored phase-2 decision is not an evaluated one; the reading "first evaluated phase-2 decision" was also computed (points only) and gives the same populations.',
        'Item 4: n = all evaluated decisions (no evaluated decision has phase 3, so phases 0-2 are the whole population). Levels, F1 and F_O are the pooled single-scale ones. The 202^3 triples are not enumerated in the bootstrap: for each level the minimum pooled wrong-go count subject to "pooled caution <= level" is found from each phase\'s distinct (count, caution sum, safe count) triples (method in the header of `rc_item4_v01.py`), with enumeration as a fallback when a triple lies within rounding of a level (never needed). At the point and for the first three resamples every arm\'s frontier was also computed by full enumeration of the deduplicated triples: identical (largest difference 0). The diagonal triples (g, g, g) are the single-scale points; taking them from the single-scale curve or from the triple sums changed nothing in the point or in any of the 400 resamples. Intervals of ratios: resamples with a positive denominator.',
        'Item 5, coverage rule: shares are over the inner values with a positive denominator (all 1,000 in every outer sample). The two inequalities of the brief are evaluated in exact integer arithmetic. The same rule in floating point is printed beside it: at a = 0.05 the float (1 - 0.95)/2 is 0.025000000000000022, just above 25/1000, so an outer sample with exactly 25 inner values at or below the truth is covered under exact arithmetic and not covered under the float rule. Coverage at nominal 1.0 is 1 by the formula (a = 0 makes both inequalities always true).',
        'Item 5, calibrated interval: the smallest grid level whose coverage is >= 0.95 (covered count * 100 >= 95 * outer samples); the interval is numpy.percentile of the draw of record at 100 a/2 and 100 (1 - a/2).',
        'Item 5, stratified draw: groups in increasing alpha (1.642, 5.412, 7.55), the runs of a group in sorted-name order (as listed in the A4 JSON), one generator used for the three groups in turn. Long runs: the 30 runs with >= 100 evaluated decisions, in sorted-name order.',
        'Item 6: m = 1/sqrt(cN/cF0) on the rows of evaluated decisions where cN and cF0 are both finite and positive; "per family (all runs)" pools the fit and tuning files of a family (the per-set split is also given). The median is over rows. Track-age bands: [0, 0.5), [0.5, 1), [1, 2), [2, 4), [4, inf) s.',
        'Not computed (not in the brief\'s list, or no draw specified): the m-out-of-n subsampling of Amendment R9; R10 (extended truth); the smaller checks S13-S20; the convex-hull frontier.']:
        w('- ' + s)
    w('')

    # ---------------------------------------------------------------- item 1
    i1 = J['item1']
    w('## 3. Item 1 (R11): 3 s commitment with signed caution')
    w('Draw of record, %d resamples. Sums are over the 201 levels; R = denE / 201 in pp.' % i1['nboot'])
    w('')
    w('| population | n | R (pp) | denE | den0 | den0 (dec.-eq.) |')
    w('|---|---|---|---|---|---|')
    for pn in ('all', 'moving', 'phase0', 'phase1', 'phase2', 'phase_weighted'):
        e = i1['pops'][pn]
        w('| %s | %d | %s | %s | %s | %s |' % (pn, e['n']['point'], pc(e['R_pp']), pc(e['denE'], 3), pc(e['den0'], 3), pc(e['den0_deceq'], 2)))
    w('')
    for kind, lab in (('RR_', 'RR (share of denE)'), ('RR0_', 'RR0 (share of den0)')):
        w('%s:' % lab)
        w('')
        w('| population | N | NA | AM | CK3 | Q |')
        w('|---|---|---|---|---|---|')
        for pn in ('all', 'moving', 'phase0', 'phase1', 'phase2', 'phase_weighted'):
            e = i1['pops'][pn]
            w('| %s | %s |' % (pn, ' | '.join(pc(e[kind + x]) for x in FIVE)))
        w('')
    d = i1['diagnostics']
    w('Signed-caution axis: F0\'s zero-margin signed caution (= the first level) is %s. Every evaluated decision has a truly safe row (the signed mean is over all of them).'
      % ', '.join('%s %.3f%%' % (k, d[k]['F0_zero_margin_signed_caution_pct']) for k in d))
    w('')

    # ---------------------------------------------------------------- item 2
    i2 = J['item2']
    w('## 4. Item 2 (R17): standstill gap 2 m')
    for key, lab in (('a_3s_commitment', '(a) 3 s commitment'), ('b_reaction_and_stop_t0p75_a6p0', '(b) reaction-and-stop, tau 0.75 s, 6 m/s2 (`t0p75_a6p0`)')):
        o = i2['scorings'][key]
        w('### %s' % lab)
        c = o['counts']
        w('Unsafe pairs under the scoring: %d; pairs not truly safe (3 s clearance <= 2 m): %d; evaluated decisions with no safe row under the scoring: %d; with no truly safe row: %d.'
          % (c['pairs_unsafe_wrong_go'], c['pairs_not_truly_safe_3s'], c['decisions_without_safe_row_scoring'], c['decisions_without_truly_safe_row_3s']))
        w('')
        w('| population | n | den0 (sum) | den0 (pp) | den0 (dec.-eq.) | denE (sum) | share of resamples with denE <= 0 |')
        w('|---|---|---|---|---|---|---|')
        for pn in ('all', 'moving', 'phase0', 'phase1', 'phase2', 'phase_weighted'):
            e = o['pops'][pn]
            w('| %s | %d | %s | %s | %s | %s | %.4f |' % (pn, e['n']['point'], pc(e['den0'], 3), pc(e['den0_pp']), pc(e['den0_deceq'], 2), pc(e['denE'], 3), e['share_denE_le0']))
        w('')
        w('RR0 (share of den0):')
        w('')
        w('| population | N | NA | AM | CK3 | Q | E |')
        w('|---|---|---|---|---|---|---|')
        for pn in ('all', 'moving', 'phase0', 'phase1', 'phase2', 'phase_weighted'):
            e = o['pops'][pn]
            w('| %s | %s |' % (pn, ' | '.join(pc(e['RR0_' + x]) for x in FIVE + ('E',))))
        w('')
    w('The brief asks for intervals for "all" and phase-weighted; the other rows carry them too (same draw). Phase 0 under (b) has den0 = 0 (no ratio).')
    w('')

    # ---------------------------------------------------------------- item 3
    i3 = J['item3']
    w('## 5. Item 3 (R12a): the first T s after the lead\'s stop')
    w('Draw of record, %d resamples. n by phase shows what each population keeps.' % i3['nboot'])
    w('')
    w('| T (s) | n (phase 0 / 1 / 2) | R (pp) | den0 (sum) |')
    w('|---|---|---|---|')
    for T in ('0', '1', '2', '5', '10', '20'):
        e = i3['T'][T]; nb = e['n_by_phase']
        w('| %s | %d (%d / %d / %d) | %s | %s |' % (T, e['n']['point'], nb['0'], nb['1'], nb['2'], pc(e['R_pp']), pc(e['den0'], 3)))
    w('')
    for kind, lab in (('RR_', 'RR'), ('RR0_', 'RR0')):
        w('%s:' % lab)
        w('')
        w('| T (s) | N | NA | AM | CK3 |')
        w('|---|---|---|---|---|')
        for T in ('0', '1', '2', '5', '10', '20'):
            e = i3['T'][T]
            w('| %s | %s |' % (T, ' | '.join(pc(e[kind + x]) for x in ('N', 'NA', 'AM', 'CK3'))))
        w('')
    al = i3['alt_k_stop_first_evaluated_phase2_decision']
    dmax = 0.
    for T in al:
        for k, v in al[T].items():
            m = i3['T'][T][k]['point']
            if v['point'] is not None and m is not None:
                dmax = max(dmax, abs(v['point'] - m))
    w('Sensitivity (points only), k_stop from the first evaluated phase-2 decision: n = %s; R = %s; RR(CK3) = %s. '
      'Largest difference from the main reading over every point of the table: %.3g (in the 5 runs concerned no evaluated decision lies at or after the stop, so the two readings keep the same decisions).'
      % (', '.join('%d' % al[T]['n']['point'] for T in al), ', '.join(f(al[T]['R_pp']['point']) for T in al), ', '.join(f(al[T]['RR_CK3']['point']) for T in al), dmax))
    w('')

    # ---------------------------------------------------------------- item 4
    i4 = J['item4']
    w('## 6. Item 4 (R12b): one margin scale per phase')
    w('Points on the full sample; intervals over the first %d rows of the draw of record. Sums over the 201 pooled single-scale levels.' % i4['nrows'])
    w('')
    w('| quantity | point | 95% interval |')
    w('|---|---|---|')
    lab = dict(den1='den1 = sum(F1_F0 - F1_E), single scale', gain_F0='gain_F0 = sum(F1_F0 - Fps_F0)', den_ps='den_ps = sum(Fps_F0 - Fps_E)',
               den0_ps='den0_ps = sum(Fps_F0 - F_O)', den0_1='den0, single scale (for reference)')
    for k in ('den1', 'gain_F0', 'den_ps', 'den0_ps', 'den0_1'):
        w('| %s | %s | %s |' % (lab[k], f(i4['sums'][k]['point']), ci(i4['sums'][k])))
    for x in FIVE:
        w('| Dps(%s) = sum(Fps_F0 - Fps_%s) | %s | %s |' % (x, x, f(i4['sums']['Dps_' + x]['point']), ci(i4['sums']['Dps_' + x])))
    for x in FIVE:
        w('| D1(%s), single scale (for reference) | %s | %s |' % (x, f(i4['sums']['D1_' + x]['point']), ci(i4['sums']['D1_' + x])))
    w('')
    w('Ratios of these sums (derived; intervals over the same 400 rows):')
    w('')
    w('| ratio | point | 95% interval |')
    w('|---|---|---|')
    rl = dict(gain_F0_over_den1='gain_F0 / den1', den_ps_over_den1='den_ps / den1', den0_ps_over_den0_1='den0_ps / den0 (single scale)')
    for k in ('gain_F0_over_den1', 'den_ps_over_den1', 'den0_ps_over_den0_1'):
        w('| %s | %s | %s |' % (rl[k], f(i4['ratios'][k]['point']), ci(i4['ratios'][k])))
    for x in FIVE:
        w('| Dps(%s) / den_ps | %s | %s |' % (x, f(i4['ratios']['RRps_' + x]['point']), ci(i4['ratios']['RRps_' + x])))
    for x in FIVE:
        w('| Dps(%s) / den0_ps | %s | %s |' % (x, f(i4['ratios']['RR0ps_' + x]['point']), ci(i4['ratios']['RR0ps_' + x])))
    pi = i4['point_info']; ri = i4['resample_info']
    w('')
    w('Distinct (count, caution sum, safe count) triples per phase (0, 1, 2): %s. Full enumeration at the point: largest difference from the fast method %s. '
      'Levels recomputed by enumeration in the 400 resamples: %d; resamples with an undefined frontier level: %d; resamples where the no-diagonal variant differs: %d.'
      % ('; '.join('%s %s' % (k, v) for k, v in pi['points'].items()), max(pi['brute_max_abs_diff'].values()), ri['levels_recomputed_by_enumeration'],
         ri['resamples_with_an_undefined_frontier_level'], ri['resamples_where_alt_differs_from_primary']))
    w('')

    # ---------------------------------------------------------------- item 5
    s5 = J['item5_single']; d5 = J['item5_double']
    ST = ('R', 'RR_N', 'RR_NA', 'RR_AM', 'RR_CK3', 'RR_Q', 'RR0_CK3', 'RR_NA_minus_RR_N')
    nd = dict(R=4)
    w('## 7. Item 5 (R9): validity of the run-bootstrap intervals (3 s commitment, all evaluated decisions)')
    w('### 7.1 The draw of record (20,000 resamples)')
    w('')
    w('| statistic | point | 95% percentile | 95% basic | range over resamples |')
    w('|---|---|---|---|---|')
    for s in ST:
        e = s5['draw_of_record'][s]; n_ = nd.get(s, 5)
        w('| %s | %s | %s | %s | [%s, %s] |' % (s, f(e['point'], n_), ci(e['percentile'], n_), ci(e['basic'], n_), f(e['min'], n_), f(e['max'], n_)))
    w('')
    w('### 7.2 Double bootstrap (%d outer x %d inner)' % (d5['n_outer'], d5['n_inner']))
    w('Coverage of the two-sided percentile interval at each nominal level (exact-arithmetic rule); in brackets the float rule where it differs.')
    w('')
    w('| statistic | 0.90 | 0.95 | 0.99 | 0.999 | 1.0 | basic, 0.95 | smallest level with coverage >= 0.95 | interval of record at that level |')
    w('|---|---|---|---|---|---|---|---|---|')
    for s in ST:
        e = d5['stats'][s]; n_ = nd.get(s, 5)
        cells = []
        for lv in ('0.900', '0.950', '0.990', '0.999', '1.0'):
            c = e['coverage'][lv]; cf = e['coverage_float_rule'][lv]
            cells.append('%.4f' % c + ('' if c == cf else ' (%.4f)' % cf))
        cal = e['calibrated_level']
        w('| %s | %s | %.4f | %s | %s |' % (s, ' | '.join(cells), e['coverage_basic_95'], 'none' if cal is None else ('%g' % cal)
                                          + ('' if e['calibrated_level_float_rule'] == cal else ' (float rule: %s)' % e['calibrated_level_float_rule']),
                                          'n/a' if cal is None else ci(e['record_interval_at_calibrated_level'], n_)))
    w('')
    w('Misses at nominal 0.95, by side (truth below the inner 2.5%% point / above the inner 97.5%% point): %s.'
      % '; '.join('%s %.4f / %.4f' % (s, d5['stats'][s]['miss_below_95'], d5['stats'][s]['miss_above_95']) for s in ST))
    w('Inner values left out for a non-positive denominator: %d in total; inner values exactly equal to the truth: %d in total.'
      % (sum(d5['stats'][s]['inner_values_left_out_total'] for s in ST), sum(d5['stats'][s]['inner_equal_to_truth_total'] for s in ST)))
    w('')
    w('### 7.3 Resampling stratified by the recording setting alpha (seed 20261122) and the 30 long runs (seed 20261123)')
    w('')
    w('| statistic | stratified: 95% percentile | 30 long runs: point | 30 long runs: 95% percentile |')
    w('|---|---|---|---|')
    for s in ST:
        n_ = nd.get(s, 5)
        w('| %s | %s | %s | %s |' % (s, ci(s5['stratified_by_alpha']['stats'][s]['percentile'], n_), f(s5['long_runs']['stats'][s]['point'], n_),
                                     ci(s5['long_runs']['stats'][s]['percentile'], n_)))
    w('')
    w('Long runs: %d runs, %d evaluated decisions; the five short runs and their evaluated decisions: %s.'
      % (s5['long_runs']['n_runs'], s5['long_runs']['n_eval'], ', '.join('%s (%d)' % (k[-4:], v) for k, v in s5['long_runs']['short_runs'].items())))
    w('')

    # ---------------------------------------------------------------- item 6
    i6 = J['item6']
    w('## 8. Item 6 (R19 / R20)')
    w('Margin ratio m = 1/sqrt(cN/cF0), rows of evaluated decisions with finite positive cN and cF0, %d stored files.' % i6['n_files'])
    w('')
    w('| family (all runs) | runs | evaluated decisions | rows | median m | share with abs(m/median - 1) > 0.05 | rows outside |')
    w('|---|---|---|---|---|---|---|')
    for k, e in i6['families'].items():
        w('| %s | %d | %d | %d | %.6f | %.6f | %d |' % (k, e['runs'], e['evaluated_decisions'], e['rows'], e['median_m'], e['share_outside_5pct'], e['rows_outside_5pct']))
    w('')
    w('| family, set | runs | evaluated decisions | rows | median m | share outside 5% | rows outside |')
    w('|---|---|---|---|---|---|---|')
    for k, e in i6['families_by_set'].items():
        w('| %s | %d | %d | %d | %.6f | %.6f | %d |' % (k.replace('|', ', '), e['runs'], e['evaluated_decisions'], e['rows'], e['median_m'], e['share_outside_5pct'], e['rows_outside_5pct']))
    w('')
    b = i6['lead_braking_eval_prim_age']
    w('Lead braking, the 35 evaluation runs, evaluated decisions by the age of the lead\'s track (`prim_age`): %s (n = %d).'
      % ('; '.join('%s s: %d' % (k, v['decisions']) for k, v in b['bands'].items()), b['n']))
    for key, lab2 in (('extra_lead_braking_all_runs_margin_ratio', 'all 55 stored lead-braking runs'), ('extra_lead_braking_eval_margin_ratio', 'the 35 evaluation runs')):
        ex = i6[key]
        w('')
        w('Extra (Amendment R19, not in the brief\'s list), %s: %d rows, median m %.6f, %d rows outside the 5%% band. By track age (rows / rows outside): %s. By `prim_miss`: %s.'
          % (lab2, ex['rows'], ex['median_m'], ex['rows_outside_5pct'],
             '; '.join('%s s: %d / %d' % (k, v['rows'], v['rows_outside_5pct']) for k, v in ex['by_age'].items()),
             '; '.join('miss %s: %d / %d' % (k, v['rows'], v['rows_outside_5pct']) for k, v in ex['outside_by_prim_miss'].items())))
    w('')
    (H / 'RECOUNT_REPORT_v01.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('written RECOUNT_RESULTS_v01.json (%d flat entries) and RECOUNT_REPORT_v01.md' % len(flat))


if __name__ == '__main__':
    main()
