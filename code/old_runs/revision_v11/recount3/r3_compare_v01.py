"""Recount3: comparison of RECOUNT3_RESULTS_v01.json (and, if present, r3_extra_v01_out.json) with the first program's files
REV_G_PARTIAL_DRAWS_v01.json, REV_D_BOOTSTRAP_v01.json (D3_sensitivities.m_out_of_n), REV_E3_EXTENDED_GAP2_v01.json and
REV_F2_BRAKING_PRIOR_v01.json. Run only after RECOUNT3_RESULTS_v01.json was written. Changes nothing of the first program.

Every comparison carries a class:
  A  a number the brief asks for; taken from RECOUNT3_RESULTS_v01.json as written before the first program's files were opened
  B  another number of RECOUNT3_RESULTS_v01.json as written before (populations, arms or counts beyond the brief's list),
     or a number of the first program's file that follows by arithmetic from RECOUNT3_RESULTS_v01.json
  C  a number of the first program's file outside the brief's list, recomputed by r3_extra_v01.py, which was written after the
     first program's files had been opened (same library, no change to it)
Usage: python -B -X utf8 r3_compare_v01.py   ->  RECOUNT3_COMPARE_v01.md, RECOUNT3_COMPARE_v01.json"""
import json, math, pathlib, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT1 = HERE.parent / 'analysis' / 'out'
TOL = 1e-9
mine = json.loads((HERE / 'RECOUNT3_RESULTS_v01.json').read_text(encoding='utf-8'))
extra_path = HERE / 'r3_extra_v01_out.json'
extra = json.loads(extra_path.read_text(encoding='utf-8')) if extra_path.exists() else None
G = json.loads((OUT1 / 'REV_G_PARTIAL_DRAWS_v01.json').read_text(encoding='utf-8'))
Dm = json.loads((OUT1 / 'REV_D_BOOTSTRAP_v01.json').read_text(encoding='utf-8'))['D3_sensitivities']['m_out_of_n']
E3 = json.loads((OUT1 / 'REV_E3_EXTENDED_GAP2_v01.json').read_text(encoding='utf-8'))
F2 = json.loads((OUT1 / 'REV_F2_BRAKING_PRIOR_v01.json').read_text(encoding='utf-8'))

rows = []


def undefined(x):
    return x is None or (isinstance(x, float) and not math.isfinite(x))


def add(item, cls, name, first, second):
    """first = the first program's value, second = this recount's value."""
    if isinstance(first, bool) or isinstance(second, bool):
        d = 0. if bool(first) == bool(second) else float('inf')
        note = 'flag'
    elif undefined(first) and undefined(second):
        d = 0.; note = 'undefined in both'
    elif undefined(first) or undefined(second):
        d = float('inf'); note = 'undefined in one'
    else:
        d = abs(float(first) - float(second)); note = ''
    rows.append(dict(item=item, cls=cls, name=name, first=first, second=second, absdiff=d, differs=bool(d > TOL), note=note))


def add2(item, cls, name, first, second):
    first = first if first is not None else [None, None]
    second = second if second is not None else [None, None]
    add(item, cls, name + ' lower', first[0], second[0]); add(item, cls, name + ' upper', first[1], second[1])


def basic(point, ci):
    if undefined(point) or ci is None or undefined(ci[0]):
        return None
    return [2 * point - ci[1], 2 * point - ci[0]]


def outside(point, ci):
    if undefined(point) or ci is None or undefined(ci[0]):
        return False
    return bool(point < ci[0] or point > ci[1])


# ------------------------------------------------------------------------------------------------ item 1
POPMAP1 = dict(all='all', moving='moving', phase1='phase1', phase2='phase2', strat='phase_weighted')
i1 = mine['item1_S12b']['share']
for fp, mp in POPMAP1.items():
    for sh, key in (('P25', '0.25'), ('P50', '0.50'), ('P75', '0.75')):
        f = G['pops'][fp][sh]; m = i1[key]['pops'][mp]
        for st in ('mean', 'min', 'max'):
            add(1, 'A', 'S12b %s %s %s' % (mp, sh, st), f[st], m['RR_' + st])
        dr = np.array(m['RR_draws'])
        add(1, 'B', 'S12b %s %s p5' % (mp, sh), f['p5'], float(np.percentile(dr, 5)))
        add(1, 'B', 'S12b %s %s p95' % (mp, sh), f['p95'], float(np.percentile(dr, 95)))
        add(1, 'B', 'S12b %s %s share_below_zero' % (mp, sh), f['share_below_zero'], float((dr < 0).mean()))
add(1, 'B', 'S12b n_draws', G['n_draws'], len(i1['0.25']['pops']['all']['RR_draws']))
if extra is not None:
    x1 = extra['item1']
    for sh, key in (('P25', '0.25'), ('P50', '0.50'), ('P75', '0.75')):
        f = G['pops']['phase0'][sh]; m = x1['phase0'][key]
        for st in ('mean', 'min', 'max', 'p5', 'p95', 'share_below_zero'):
            add(1, 'C', 'S12b phase0 %s %s' % (sh, st), f[st], m[st])
    if 'of_record' in x1:
        for fp, mp in list(POPMAP1.items()) + [('phase0', 'phase0')]:
            for sh, key in (('P25', '0.25'), ('P50', '0.50'), ('P75', '0.75')):
                add(1, 'C', 'S12b %s %s of_record' % (mp, sh), G['pops'][fp][sh]['of_record'], x1['of_record'][key][mp])

# ------------------------------------------------------------------------------------------------ item 2
STATMAP = dict(R='R', RR_N='RR_N', RR_NA='RR_NA', RR_A1='RR_AM', RR_CK3='RR_CK3', RR_Q='RR_Q', RR0_CK3='RR0_CK3', NA_minus_N='RR_NA_minus_RR_N')
for m in ('15', '20', '25'):
    e = mine['item2_S17']['m'][m]
    for fs, ms in STATMAP.items():
        f = Dm[m][fs]; s = e['stats'][ms]
        add2(2, 'A', 'S17 m=%s %s interval (finite-population factor)' % (m, ms), f['interval_fpc'], [s['lo'], s['hi']])
        th = s['theta']; r35 = math.sqrt(35.); rm = math.sqrt(float(m))
        add2(2, 'B', 'S17 m=%s %s interval without the factor' % (m, ms), f['interval_raw'], [th - s['qh'] / r35, th - s['ql'] / r35])
        add2(2, 'B', 'S17 m=%s %s 2.5 and 97.5 percentiles of the subsample values' % (m, ms), f['subsample_q2p5_q97p5'],
             [th + s['ql'] / rm, th + s['qh'] / rm])
        add(2, 'B', 'S17 m=%s %s n_invalid' % (m, ms), f['n_invalid'], e['n_subsamples'] - s['n_finite'])

# ------------------------------------------------------------------------------------------------ item 3
POPMAP3 = dict(all='all', moving='moving', phase0='phase0', phase1='phase1', phase2='phase2', strat='phase_weighted')
ARM3 = dict(N='N', NA='NA', CK3='CK3', A1='AM', Q='Q')
i3 = mine['item3_S24b']
add(3, 'A', 'S24b pairs unsafe at 2 m, 3 s window (cache)', E3['pairs']['unsafe_as_scored_gap2'], i3['counts']['pairs_unsafe_window_cache'])
add(3, 'A', 'S24b pairs unsafe at 2 m, judged until the stop ends', E3['pairs']['unsafe_est_gap2'], i3['counts']['pairs_unsafe_until_stop'])
add(3, 'A', 'S24b decisions without a row safe until the stop ends', E3['pairs']['decisions_without_safe_row'], i3['counts']['decisions_without_row_safe_until_stop'])
for fp, mp in POPMAP3.items():
    f = E3['pops'][fp]; m = i3['pops'][mp]
    asked = mp in ('all', 'moving', 'phase_weighted')
    c = 'A' if asked else 'B'
    n = m['n']
    add(3, 'B', 'S24b %s n' % mp, f['n'], n)
    add(3, c, 'S24b %s den0 pp' % mp, f['den0']['R_pp'], m['den0_pp']['point'])
    add(3, c, 'S24b %s den0 decision-equivalents' % mp, f['den0']['dec_eq'], m['den0_deceq']['point'])
    add2(3, c, 'S24b %s den0 decision-equivalents interval' % mp, f['den0']['dec_eq_ci'], m['den0_deceq']['ci'])
    add(3, 'B', 'S24b %s den0 (sum over levels)' % mp, f['den0']['point'], m['den0_sum'])
    add2(3, 'B', 'S24b %s den0 (sum over levels) interval = 201 x the pp interval' % mp, f['den0']['ci'], [201. * x for x in m['den0_pp']['ci']])
    add(3, 'B', 'S24b %s den0 share of resamples <= 0' % mp, f['den0']['share_le0'], m['share_den0_not_positive'])
    add(3, 'B', 'S24b %s den0 resamples <= 0' % mp, f['den0']['n_le0'], round(m['share_den0_not_positive'] * i3['nboot']))
    add(3, 'B', 'S24b %s denE (sum over levels)' % mp, f['denE']['point'], m['denE_sum'])
    add(3, 'B', 'S24b %s denE pp' % mp, f['denE']['R_pp'], m['denE_pp']['point'])
    add(3, 'B', 'S24b %s denE decision-equivalents' % mp, f['denE']['dec_eq'], m['denE_sum'] / 201. / 100. * n)
    for fa, ma in [('E', 'E')] + list(ARM3.items()):
        fr = f['E_rr0'] if fa == 'E' else f['arms'][fa]['rr0']
        mr = m['RR0_' + ma]
        ca = c if ma != 'Q' else 'B'
        add(3, ca, 'S24b %s RR0(%s)' % (mp, ma), fr['point'], mr['point'])
        add2(3, ca, 'S24b %s RR0(%s) interval' % (mp, ma), fr['ci'], mr['ci'])
        add(3, 'B', 'S24b %s RR0(%s) resamples left out' % (mp, ma), fr['n_invalid'], mr['n_left_out'])
        add(3, 'B', 'S24b %s RR0(%s) share left out' % (mp, ma), fr['invalid_share'], mr['n_left_out'] / i3['nboot'])
        add2(3, 'B', 'S24b %s RR0(%s) basic interval' % (mp, ma), fr['basic'], basic(mr['point'], mr['ci']))
        add(3, 'B', 'S24b %s RR0(%s) point outside its interval' % (mp, ma), fr['outside'], outside(mr['point'], mr['ci']))
        if fa != 'E':
            add(3, 'B', 'S24b %s D(%s) decision-equivalents' % (mp, ma), f['arms'][fa]['D_dec_eq'], m['D_' + ma] / 201. / 100. * n)

# ------------------------------------------------------------------------------------------------ item 4
POPMAP4 = POPMAP3
i4 = mine['item4_S25']; S20 = F2['S20']
for fp, mp in POPMAP4.items():
    f = S20[fp]
    add(4, 'B', 'S25 %s n' % mp, f['n'], i4['n'][mp])
    add(4, 'B', 'S25 %s denE decision-equivalents' % mp, f['denE_dec_eq'], i4['denE'][mp] / 201. / 100. * i4['n'][mp])
    for a0 in range(1, 8):
        fa = f['arms'][str(a0)]; ma = i4['a0'][str(a0)][mp]
        add(4, 'A', 'S25 a0=%d %s RR' % (a0, mp), fa['rrE']['point'], ma['RR'])
        add2(4, 'A', 'S25 a0=%d %s RR interval' % (a0, mp), fa['rrE']['ci'], ma['RR_ci'])
        add(4, 'A', 'S25 a0=%d %s D decision-equivalents' % (a0, mp), fa['D_dec_eq'], ma['D_deceq'])
        add(4, 'B', 'S25 a0=%d %s RR resamples left out' % (a0, mp), fa['rrE']['n_invalid'], ma['n_left_out'])
        add(4, 'B', 'S25 a0=%d %s RR share left out' % (a0, mp), fa['rrE']['invalid_share'], ma['n_left_out'] / i4['nboot'])
        add2(4, 'B', 'S25 a0=%d %s RR basic interval' % (a0, mp), fa['rrE']['basic'], basic(ma['RR'], ma['RR_ci']))
        add(4, 'B', 'S25 a0=%d %s RR point outside its interval' % (a0, mp), fa['rrE']['outside'], outside(ma['RR'], ma['RR_ci']))
        add(4, 'B', 'S25 a0=%d %s a0' % (a0, mp), fa['a0'], float(a0))
        if extra is not None:
            xa = extra['item4']['a0'][str(a0)][mp]
            add(4, 'C', 'S25 a0=%d %s RR0' % (a0, mp), fa['rr0']['point'], xa['RR0'])
            add2(4, 'C', 'S25 a0=%d %s RR0 interval' % (a0, mp), fa['rr0']['ci'], xa['RR0_ci'])
            add(4, 'C', 'S25 a0=%d %s RR0 resamples left out' % (a0, mp), fa['rr0']['n_invalid'], xa['n_left_out'])
            add(4, 'C', 'S25 a0=%d %s RR0 share left out' % (a0, mp), fa['rr0']['invalid_share'], xa['n_left_out'] / i4['nboot'])
            add2(4, 'C', 'S25 a0=%d %s RR0 basic interval' % (a0, mp), fa['rr0']['basic'], basic(xa['RR0'], xa['RR0_ci']))
            add(4, 'C', 'S25 a0=%d %s RR0 point outside its interval' % (a0, mp), fa['rr0']['outside'], outside(xa['RR0'], xa['RR0_ci']))
    if extra is not None:
        add(4, 'C', 'S25 %s den0 decision-equivalents' % mp, f['den0_dec_eq'], extra['item4']['den0_deceq'][mp])
zm = S20['zero_margin_points_all']
for a in ['F0'] + ['CK%d' % k for k in range(1, 8)]:
    fk = a if a == 'F0' else a + 'x'
    add(4, 'A', 'S25 zero margin %s caution %%' % a, zm[fk]['caution_pct'], i4['zero_margin'][a]['caution_pct'])
    add(4, 'A', 'S25 zero margin %s wrong go %%' % a, zm[fk]['wrong_go_pct'], i4['zero_margin'][a]['wrong_go_pct'])
add(4, 'B', 'cCK3 entries differing from the extraction of record (evaluated decisions)', S20['cCK3_entries_differing_from_record'],
    mine['cck3_identity']['total']['elements_evaluated_differing_bits'])
bn = mine['item4_benign']; S18 = F2['S18']
add(4, 'B', 'benign runs', S18['n_runs'], bn['n_runs'])
add(4, 'A', 'benign evaluated decisions', S18['selection_changed']['evaluated'], bn['total']['evaluated_decisions'])
add(4, 'B', 'benign evaluated decisions (population n)', S18['all']['n'], bn['total']['evaluated_decisions'])
add(4, 'A', 'benign selection differs at g = 0', S18['selection_changed']['at_zero_margin'], bn['total']['differ_g0'])
add(4, 'A', 'benign selection differs at g = 1', S18['selection_changed']['at_g_1'], bn['total']['differ_g1'])
add(4, 'A', 'benign wrong go at zero margin, class average', S18['all']['zero_margin']['F0']['wrong_go_n'], bn['total']['wrong_go_g0_F0'])
add(4, 'A', 'benign wrong go at zero margin, braking prediction', S18['all']['zero_margin']['CK3']['wrong_go_n'], bn['total']['wrong_go_g0_CK3'])
if extra is not None and 'benign' in extra:
    xb = extra['benign']
    for pop in ('all', 'moving'):
        f = S18[pop]; m = xb[pop]
        if pop != 'all':                                   # S18.all.n is compared above (class B)
            add(4, 'C', 'benign %s n' % pop, f['n'], m['n'])
        add(4, 'C', 'benign %s R pp' % pop, f['R_pp'], m['R_pp'])
        for dk in ('denE', 'den0'):
            add(4, 'C', 'benign %s %s' % (pop, dk), f[dk]['point'], m[dk]['point'])
            add2(4, 'C', 'benign %s %s interval' % (pop, dk), f[dk]['ci'], m[dk]['ci'])
            add(4, 'C', 'benign %s %s resamples <= 0' % (pop, dk), f[dk]['n_le0'], m[dk]['n_le0'])
            add(4, 'C', 'benign %s %s share <= 0' % (pop, dk), f[dk]['share_le0'], m[dk]['n_le0'] / xb['nboot'])
            add(4, 'C', 'benign %s %s decision-equivalents' % (pop, dk), f[dk + '_dec_eq'], m[dk + '_deceq'])
        for a in ('N', 'CK3'):
            fa = f['arms'][a]; ma = m['arms'][a]
            add(4, 'C', 'benign %s D(%s) pp' % (pop, a), fa['D_pp'], ma['D_pp'])
            add(4, 'C', 'benign %s D(%s) decision-equivalents' % (pop, a), fa['D_dec_eq']['point'], ma['D_deceq'])
            add2(4, 'C', 'benign %s D(%s) decision-equivalents interval' % (pop, a), fa['D_dec_eq']['ci'], ma['D_deceq_ci'])
            for rk, mk in (('rrE', 'RR'), ('rr0', 'RR0')):
                add(4, 'C', 'benign %s %s(%s)' % (pop, mk, a), fa[rk]['point'], ma[mk])
                add2(4, 'C', 'benign %s %s(%s) interval' % (pop, mk, a), fa[rk]['ci'], ma[mk + '_ci'])
                add(4, 'C', 'benign %s %s(%s) resamples left out' % (pop, mk, a), fa[rk]['n_invalid'], ma[mk + '_left_out'])
                add(4, 'C', 'benign %s %s(%s) share left out' % (pop, mk, a), fa[rk]['invalid_share'], ma[mk + '_left_out'] / xb['nboot'])
                add2(4, 'C', 'benign %s %s(%s) basic interval' % (pop, mk, a), fa[rk]['basic'], basic(ma[mk], ma[mk + '_ci']))
                add(4, 'C', 'benign %s %s(%s) point outside its interval' % (pop, mk, a), fa[rk]['outside'], outside(ma[mk], ma[mk + '_ci']))
        for a in ('F0', 'CK3', 'E'):
            add(4, 'C', 'benign %s zero margin %s caution %%' % (pop, a), f['zero_margin'][a]['caution_pct'], m['zero_margin'][a]['caution_pct'])
            add(4, 'C', 'benign %s zero margin %s wrong go %%' % (pop, a), f['zero_margin'][a]['wrong_go_pct'], m['zero_margin'][a]['wrong_go_pct'])
            if not (pop == 'all' and a in ('F0', 'CK3')):
                add(4, 'C', 'benign %s zero margin %s wrong-go decisions' % (pop, a), f['zero_margin'][a]['wrong_go_n'], m['zero_margin'][a]['wrong_go_n'])
        if 'over_the_scale_grid' in m:
            for k2 in ('mean_caution_diff_pp', 'max_caution_diff_pp', 'mean_wrong_go_diff_pp', 'max_wrong_go_F0', 'max_wrong_go_CK3'):
                add(4, 'C', 'benign %s over the scale grid %s' % (pop, k2), f['over_the_scale_grid'][k2], m['over_the_scale_grid'][k2])

# ------------------------------------------------------------------------------------------------ coverage
SKIP = {'seconds', 'written', 'code', 'status', 'seeds', 'source', 'tuning_runs_of_record', 'setting'}


def leaves(o):
    """Number of numeric (or flag, or undefined) leaves of a result file, lists counted element by element."""
    if isinstance(o, dict):
        return sum(leaves(v) for k, v in o.items() if k not in SKIP)
    if isinstance(o, list):
        return sum(leaves(v) for v in o)
    return 0 if isinstance(o, str) else 1


coverage = {}
for it, name, obj in ((1, 'REV_G_PARTIAL_DRAWS_v01.json', G), (2, 'REV_D_BOOTSTRAP_v01.json: D3_sensitivities.m_out_of_n', Dm),
                      (3, 'REV_E3_EXTENDED_GAP2_v01.json', E3), (4, 'REV_F2_BRAKING_PRIOR_v01.json', F2)):
    coverage[it] = dict(file=name, leaves_in_first_program_file=leaves(obj), compared=sum(1 for r in rows if r['item'] == it))

# ------------------------------------------------------------------------------------------------ report
TITLES = {1: 'Table S12b (partial oracles over 50 draws)', 2: 'Table S17 (subsampling without replacement)',
          3: 'Table S24b (2 m gap, plans judged until their stop ends)', 4: 'Table S25 and the benign-run check'}
CLS = {'A': 'asked for by the brief', 'B': 'other numbers of the results file, or arithmetic on it', 'C': 'supplementary (r3_extra_v01.py, written after the files were opened)'}


def fmt(x):
    if isinstance(x, bool):
        return str(x)
    if undefined(x):
        return 'undefined'
    return repr(float(x)) if isinstance(x, float) else str(x)


lines = ['# Recount3: comparison with the first program', '',
         'Written %s by `r3_compare_v01.py`. First program: `revision_v11\\analysis\\out\\REV_G_PARTIAL_DRAWS_v01.json`, '
         '`REV_D_BOOTSTRAP_v01.json` (`D3_sensitivities.m_out_of_n`), `REV_E3_EXTENDED_GAP2_v01.json`, `REV_F2_BRAKING_PRIOR_v01.json`. '
         'Second program: `RECOUNT3_RESULTS_v01.json`%s. The first program\'s files were opened only after `RECOUNT3_RESULTS_v01.json` '
         'had been written (sha256 in the report) and were not changed.' % (time.strftime('%d %b %Y %H:%M'),
                                                                             ' and `r3_extra_v01_out.json`' if extra is not None else ''), '',
         'A number "differs" when the absolute difference exceeds 1e-9 (or when it is defined in one program only, or a flag differs). '
         'Where both programs give "undefined" (no ratio because the denominator is not positive in the full sample or in every resample), '
         'the number counts as compared and equal.', '',
         'Classes: **A** = %s; **B** = %s; **C** = %s.' % (CLS['A'], CLS['B'], CLS['C']), '',
         '## Counts', '', '| Item | Class | Compared | Differ by > 1e-9 | Largest absolute difference | Undefined in both |', '|---|---|---|---|---|---|']
summary = {}
for it in (1, 2, 3, 4):
    for c in ('A', 'B', 'C', 'all'):
        rr = [r for r in rows if r['item'] == it and (c == 'all' or r['cls'] == c)]
        if not rr:
            continue
        fin = [r['absdiff'] for r in rr if math.isfinite(r['absdiff'])]
        nd = sum(r['differs'] for r in rr)
        summary['%d%s' % (it, c)] = dict(compared=len(rr), differ=nd, max_abs_diff=max(fin) if fin else None,
                                         undefined_in_both=sum(r['note'] == 'undefined in both' for r in rr))
        lines.append('| %d. %s | %s | %d | %d | %.3g | %d |' % (it, TITLES[it] if c in ('A',) else '', c, len(rr), nd, max(fin) if fin else float('nan'),
                                                                 sum(r['note'] == 'undefined in both' for r in rr)))
tot = dict(compared=len(rows), differ=sum(r['differs'] for r in rows))
lines += ['| all items | all | %d | %d | %.3g | %d |' % (tot['compared'], tot['differ'], max(r['absdiff'] for r in rows if math.isfinite(r['absdiff'])),
                                                         sum(r['note'] == 'undefined in both' for r in rows)), '']
lines += ["## Coverage of the first program's files", '',
          'Numeric leaves of each file (a two-element interval counts as two; flags and undefined values count; the run time, the text '
          'fields, the constants under `setting` and the block `S20.tuning_runs_of_record` are left aside) against the number of comparisons made.', '',
          "| Item | File | Leaves in the first program's file | Compared |", '|---|---|---|---|']
for it in (1, 2, 3, 4):
    c_ = coverage[it]
    lines.append('| %d | `%s` | %d | %d |' % (it, c_['file'], c_['leaves_in_first_program_file'], c_['compared']))
lines.append('')
lines += ['## Differences', '']
diffs = [r for r in rows if r['differs']]
if not diffs:
    lines += ['None. No compared number differs by more than 1e-9.', '']
else:
    lines += ['| Item | Class | Number | First program | Second program (recount3) | Absolute difference |', '|---|---|---|---|---|---|']
    for r in diffs:
        lines.append('| %d | %s | %s | %s | %s | %s |' % (r['item'], r['cls'], r['name'], fmt(r['first']), fmt(r['second']),
                                                         ('%.6g' % r['absdiff']) if math.isfinite(r['absdiff']) else r['note']))
    lines.append('')
cause_path = HERE / 'r3_causes_v01.md'
if cause_path.exists():
    lines += ['## Causes', '', cause_path.read_text(encoding='utf-8').strip(), '']
lines += ['## Largest differences per item (all classes, the five largest)', '']
for it in (1, 2, 3, 4):
    rr = sorted([r for r in rows if r['item'] == it and math.isfinite(r['absdiff'])], key=lambda r: -r['absdiff'])[:5]
    lines.append('**Item %d**' % it)
    lines.append('')
    lines += ['| Number | First program | Second program | Absolute difference |', '|---|---|---|---|']
    for r in rr:
        lines.append('| %s | %s | %s | %.3g |' % (r['name'], fmt(r['first']), fmt(r['second']), r['absdiff']))
    lines.append('')
lines += ['## Not compared', '',
          '- `REV_F2_BRAKING_PRIOR_v01.json`, `S20.tuning_runs_of_record`: copied by the first program from `OXSB_CTL_RESULTS_v02.json` '
          '(20 lead-braking tuning runs, 13 Nov 2026); not part of this brief.',
          '- `REV_D_BOOTSTRAP_v01.json` outside `D3_sensitivities.m_out_of_n`: recounted earlier (`revision_v11\\recount`).', '',
          'Every single comparison (name, both values, difference, class) is in `RECOUNT3_COMPARE_v01.json`.', '']
(HERE / 'RECOUNT3_COMPARE_v01.md').write_text('\n'.join(lines), encoding='utf-8')


def clean(o):
    if isinstance(o, float) and not math.isfinite(o):
        return None if math.isnan(o) else 'inf'
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, list):
        return [clean(v) for v in o]
    return o


(HERE / 'RECOUNT3_COMPARE_v01.json').write_text(json.dumps(clean(dict(tolerance=TOL, summary=summary, total=tot, coverage=coverage, rows=rows)), indent=1), encoding='utf-8')
print('compared %d, differing %d' % (tot['compared'], tot['differ']))
for k, v in summary.items():
    print('  item/class %-5s compared %4d  differ %3d  max abs diff %s' % (k, v['compared'], v['differ'], v['max_abs_diff']))
for it in (1, 2, 3, 4):
    print('  coverage item %d: leaves %d, compared %d' % (it, coverage[it]['leaves_in_first_program_file'], coverage[it]['compared']))
for r in diffs[:60]:
    print('  DIFF', r['item'], r['cls'], r['name'], fmt(r['first']), fmt(r['second']), r['absdiff'])
