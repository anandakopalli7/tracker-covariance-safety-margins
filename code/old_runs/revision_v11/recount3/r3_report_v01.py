"""Recount3: writes RECOUNT3_REPORT_v01.md from RECOUNT3_RESULTS_v01.json, r3_naive_v01_out.json, r3_extra_v01_out.json and
RECOUNT3_COMPARE_v01.json (tables are generated, so no number is retyped).
Usage: python -B -X utf8 r3_report_v01.py"""
import hashlib, json, pathlib, time
HERE = pathlib.Path(__file__).resolve().parent
res_path = HERE / 'RECOUNT3_RESULTS_v01.json'
r = json.loads(res_path.read_text(encoding='utf-8'))
nv = json.loads((HERE / 'r3_naive_v01_out.json').read_text(encoding='utf-8'))
ex = json.loads((HERE / 'r3_extra_v01_out.json').read_text(encoding='utf-8'))
cp = json.loads((HERE / 'RECOUNT3_COMPARE_v01.json').read_text(encoding='utf-8'))
sha = hashlib.sha256(res_path.read_bytes()).hexdigest()
mtime = time.strftime('%d %b %Y %H:%M:%S', time.localtime(res_path.stat().st_mtime))


def f(x, d=4):
    return 'undefined' if x is None else '%.*f' % (d, x)


def ci(c, d=4):
    return '' if c is None else ' [%s, %s]' % (f(c[0], d), f(c[1], d))


S = cp['summary']
idn = r['cck3_identity']['total']
dat = r['data']
i1 = r['item1_S12b']; i2 = r['item2_S17']; i3 = r['item3_S24b']; i4 = r['item4_S25']; bn = r['item4_benign']
dg = ex['item3_diagnostics']
o = []
o += ['# Recount3: independent second program for Tables S12b, S17 (subsampling), S24b and S25 with the benign-run check', '',
      'Written %s. Brief: `RECOUNT3_BRIEF_v01.md` (this folder), with the inputs, scoring definitions and bootstrap of record of '
      '`revision_v11\\recount\\RECOUNT_BRIEF_v01.md`.' % time.strftime('%d %b %Y'), '',
      '## Result in short', '',
      '- All four analyses were recomputed by a second program. Compared with the first program: **%d numbers, %d differ by more than 1e-9** '
      '(largest absolute difference %.1e).' % (cp['total']['compared'], cp['total']['differ'],
                                             max(v['max_abs_diff'] for k, v in S.items() if k.endswith('all'))),
      '- Numbers the brief asks for: item 1: %d compared, %d differ; item 2: %d, %d; item 3: %d, %d; item 4: %d, %d.' % (
          S['1A']['compared'], S['1A']['differ'], S['2A']['compared'], S['2A']['differ'], S['3A']['compared'], S['3A']['differ'],
          S['4A']['compared'], S['4A']['differ']),
      '- Every numeric entry of the first program\'s four files was compared (item 1: %d, item 2: %d, item 3: %d, item 4: %d), except the block '
      '`S20.tuning_runs_of_record` of `REV_F2_BRAKING_PRIOR_v01.json`, which the first program copied from an older file and which is outside this brief.' % (
          S['1all']['compared'], S['2all']['compared'], S['3all']['compared'], S['4all']['compared']),
      '- `cCK3` identity check: the `cCK3` of `analysis\\out\\ck\\<run>.npz` equals the stored `cCK3` of `A4\\fit\\extract\\<run>.npz` bit for bit in '
      '%d of %d evaluation runs (%d entries, of which %d on evaluated decisions; %d entries differ).' % (
          idn['runs_bit_identical'], idn['runs'], idn['elements'], idn['elements_evaluated'], idn['elements_differing_bits']),
      '- One caveat that is not a difference between the programs (both treat it the same way): in Table S24b, %d decision-row pairs have a '
      'recording that ends before the plan\'s stop does; %d of them are counted safe at 2 m on the frames that exist. See "Ambiguities", point 7.' % (
          dg['censored'], dg['censored_and_counted_safe_at_2m']), '']
o += ['## Independence and order of work', '',
      '- Read before writing the program: the two briefs; `revision_v11\\recount\\rc_lib_v01.py` and `rc_items_v01.py`; '
      '`revision_v11\\recount2\\recount2_ext_v01.py` and `recount2_score_v01.py`; a keyword search of `revision_v11\\recount\\RECOUNT_REPORT_v01.md` '
      '(the earlier second program\'s report: its conventions and the phase-weighted rows of its own tables for R11 and R17, which are other analyses). '
      'Its timing log `rc_items_v01_log.txt`. Arrays opened: the stored runs, the extraction, the pack cache, `recount2\\out`, `analysis\\out\\ck`.',
      '- Not opened at any time: `P\\11_ojits\\A6R\\code`, `<excluded folder 1>`, `<excluded folder 2>`, `<excluded folder 3>`. No file of `revision_v11\\draft` was opened '
      '(a listing of recently changed files, made after the comparison to confirm that nothing was written outside this folder, showed file names there). No network.',
      '- `RECOUNT3_RESULTS_v01.json` was written at %s (sha256 `%s`) and has not been changed since. Only after that were the first '
      'program\'s four result files opened, and then its two scripts `rev_g_partial_oracle_draws_v01.py` and `rev_f2_braking_prior_score_v01.py` '
      '(and the header of `rev_common_v01.py`), to learn the definitions of entries that the brief does not list.' % (mtime, sha),
      '- The supplementary script `r3_extra_v01.py` was written after that. It recomputes entries of the first program\'s files that the brief does '
      'not list (class C in the comparison) with the unchanged library. Nothing in the program was tuned after the comparison; no difference was found.', '']
o += ['## Inputs and checks on them', '',
      '- %d evaluation runs, %d stored decisions, %d evaluated; evaluated decisions by phase: %s before onset, %s lead braking, %s lead stopped, %s unknown.' % (
          dat['runs'], dat['stored_decisions'], dat['evaluated_decisions'], dat['phase_counts_evaluated']['0'], dat['phase_counts_evaluated']['1'],
          dat['phase_counts_evaluated']['2'], dat['phase_counts_evaluated']['3']),
      '- NaN among evaluated decisions: 3 s clearance %d, pack cache (`t0p75_a6p0`) %d, clearance judged until the stop ends %d, `cCK1`..`cCK7` %d.' % (
          dat['nan_clear_evaluated'], dat['nan_cache_evaluated'], dat['nan_clearX_evaluated'], sum(i4['nan_critical_scales_evaluated'].values())),
      '- `k` and the evaluated flags of `recount2\\out` equal the stored ones in every run; `k` of the `ck` folder equals the stored `k` in every run '
      '(the program stops otherwise).',
      '- Clearance judged until the stop ends: key `clearX_t0p75_a6p0` of `recount2\\out\\<run>.npz`.', '']
o += ['## Method', '',
      '- `r3_lib_v01.py` imports the second-program library `rc_lib_v01.py` for the loader of the 35 runs, the selection on the grid of 202 scales, '
      'the batched step frontier, the level grid and the percentile helper. The evaluation for an arbitrary list of arms (`evaluate_g`) and the '
      'per-decision statistics are written here. Each run is reduced to per-scale counts (wrong-go count, caution sum, caution count per population), '
      'so that a resample is a weighted sum of 35 vectors.',
      '- Bootstrap of record: `numpy.random.default_rng(20261113).integers(0, 35, size=(20000, 35))`; everything, levels included, is rebuilt in every '
      'resample; 95% percentile intervals over the resamples with a positive denominator.',
      '- Self-check by a second route (`r3_naive_v01.py`): decisions concatenated (no per-run statistics), selection recomputed from the critical scales, '
      'levels by `numpy.linspace`, the frontier by a loop over levels. It shares only the data loader. %d numbers (every point of items 3 and 4, the '
      'full-sample values of item 2, three draws of item 1, and two resamples or subsamples of each bootstrap) agree with the program to %.1e.' % (
          nv['n_compared'], nv['max_abs_diff']),
      '- `evaluate_g` gives the same values as `rc_lib_v01.evaluate` on the statistics of item 3 (equal arrays: %s).' % i3['evaluate_g_equals_rc_lib_evaluate'], '']
# ---- item 1
o += ['## Item 1. Table S12b: partial oracles over 50 draws', '',
      'For draw i = 0..49, `u = default_rng(20261200 + i).random(9307)`, one value per stored decision (runs in sorted-name order, stored order '
      'within a run). Share p: the oracle\'s critical scales where u < p, the class average\'s elsewhere. The partial arm gets F0\'s zero-margin point '
      'prepended. 3 s commitment, step frontier, points. Cells: mean [minimum, maximum] of RR over the 50 draws.', '',
      '| Population | n | p = 0.25 | p = 0.50 | p = 0.75 |', '|---|---|---|---|---|']
for pn, lab in (('all', 'All'), ('moving', 'Ego moving'), ('phase1', 'Lead braking (phase 1)'), ('phase2', 'Lead stopped (phase 2)'),
                ('phase_weighted', 'Phase-weighted')):
    cells = []
    for key in ('0.25', '0.50', '0.75'):
        v = i1['share'][key]['pops'][pn]
        cells.append('%s [%s, %s]' % (f(v['RR_mean']), f(v['RR_min']), f(v['RR_max'])))
    o.append('| %s | %d | %s |' % (lab, i1['n'][pn], ' | '.join(cells)))
o += ['', 'Evaluated decisions on the oracle, mean over draws: %s (p = 0.25), %s (0.50), %s (0.75) of %d. No frontier level is undefined in any population.' % (
    f(i1['share']['0.25']['evaluated_decisions_on_the_oracle_mean'], 1), f(i1['share']['0.50']['evaluated_decisions_on_the_oracle_mean'], 1),
    f(i1['share']['0.75']['evaluated_decisions_on_the_oracle_mean'], 1), i1['n_evaluated']),
      'Supplementary (class C): phase 0 and the value of the draw of record (`default_rng(20261118)`) were also recomputed and agree with the first program.', '']
# ---- item 2
o += ['## Item 2. Table S17: subsampling without replacement', '',
      'One stream `default_rng(20261124)`; for m = 15, 20, 25 in that order, 5,000 subsamples `rng.permutation(35)[:m]` each. Root = sqrt(m) (theta* - theta); '
      '(ql, qh) = 2.5 and 97.5 percentiles of the roots; interval [theta - qh / (f sqrt(35)), theta - ql / (f sqrt(35))], f = sqrt(1 - m/35). '
      '3 s commitment, all evaluated decisions.', '',
      '| Statistic | Full sample | m = 15 | m = 20 | m = 25 |', '|---|---|---|---|---|']
LAB = dict(R='R (pp)', RR_N='RR(N)', RR_NA='RR(NA)', RR_AM='RR(AM)', RR_CK3='RR(CK3)', RR_Q='RR(Q)', RR0_CK3='RR0(CK3)', RR_NA_minus_RR_N='RR(NA) - RR(N)')
for s, lab in LAB.items():
    o.append('| %s | %s | %s | %s | %s |' % (lab, f(i2['theta'][s]), *['[%s, %s]' % (f(i2['m'][m]['stats'][s]['lo']), f(i2['m'][m]['stats'][s]['hi'])) for m in ('15', '20', '25')]))
o += ['', 'In all %d subsamples denE and den0 are positive and every root is finite (subsamples with denE <= 0: %s; with den0 <= 0: %s; with an undefined '
      'frontier level: %s), so the reading of "finite roots" does not matter.' % (
          3 * 5000, ', '.join(str(i2['m'][m]['n_denE_not_positive']) for m in ('15', '20', '25')),
          ', '.join(str(i2['m'][m]['n_den0_not_positive']) for m in ('15', '20', '25')),
          ', '.join(str(i2['m'][m]['n_undefined_frontier']) for m in ('15', '20', '25'))), '']
# ---- item 3
o += ['## Item 3. Table S24b: 2 m standstill gap, plans judged until their stop ends (tau 0.75 s, 6 m/s2)', '',
      'Wrong go: the selected row\'s clearance judged until the stop ends is <= 2 m. Caution axis: a row is truly safe when its 3 s clearance is > 2 m. '
      'Perfect oracle O: first row in cost order whose clearance judged until the stop ends is > 2 m, the fallback row if none. Intervals: draw of record.', '',
      '| Population | n | den0 (pp) | den0 (decision-equivalents) |', '|---|---|---|---|']
P3 = (('all', 'All'), ('moving', 'Ego moving'), ('phase_weighted', 'Phase-weighted'))
for pn, lab in P3:
    e = i3['pops'][pn]
    o.append('| %s | %d | %s%s | %s%s |' % (lab, e['n'], f(e['den0_pp']['point']), ci(e['den0_pp']['ci']), f(e['den0_deceq']['point'], 2), ci(e['den0_deceq']['ci'], 2)))
o += ['', '| Population | RR0(E) | RR0(N) | RR0(NA) | RR0(CK3) | RR0(AM) |', '|---|---|---|---|---|---|']
for pn, lab in P3:
    e = i3['pops'][pn]
    o.append('| %s | %s |' % (lab, ' | '.join('%s%s' % (f(e['RR0_' + a]['point']), ci(e['RR0_' + a]['ci'])) for a in ('E', 'N', 'NA', 'CK3', 'AM'))))
c3 = i3['counts']
o += ['', 'Counts over the %d evaluated decisions (%d decision-row pairs):' % (c3['evaluated_decisions'], c3['decision_row_pairs']), '',
      '- decisions without any row whose clearance judged until the stop ends is > 2 m: **%d**;' % c3['decisions_without_row_safe_until_stop'],
      '- pairs unsafe at 2 m on the 3 s window\'s reaction-and-stop clearance of record (pack cache): **%d**;' % c3['pairs_unsafe_window_cache'],
      '- pairs unsafe at 2 m when judged until the stop ends: **%d**.' % c3['pairs_unsafe_until_stop'], '',
      'den0 is positive in every resample for the three populations. In phase 0 den0 = 0 in the full sample and in every resample (no ratio), in both '
      'programs. The results file also holds phases 0-2 separately, RR0(Q) and denE; all were compared (class B).', '']
# ---- item 4
o += ['## Item 4. Table S25: braking prediction at a0 = 1..7 m/s2, and the benign-run check', '',
      'Arm = `cCK<a0>` of the `ck` folder; 3 s commitment, step frontier; intervals: draw of record. RR:', '',
      '| a0 | All | Ego moving | Phase 0 | Phase 1 | Phase 2 | Phase-weighted |', '|---|---|---|---|---|---|---|']
P4 = ('all', 'moving', 'phase0', 'phase1', 'phase2', 'phase_weighted')
for a0 in range(1, 8):
    e = i4['a0'][str(a0)]
    o.append('| %d | %s |' % (a0, ' | '.join('%s%s' % (f(e[p]['RR']), ci(e[p]['RR_ci'])) for p in P4)))
o += ['', 'D in decision-equivalents:', '', '| a0 | All | Ego moving | Phase 0 | Phase 1 | Phase 2 | Phase-weighted |', '|---|---|---|---|---|---|---|']
for a0 in range(1, 8):
    e = i4['a0'][str(a0)]
    o.append('| %d | %s |' % (a0, ' | '.join(f(e[p]['D_deceq'], 2) for p in P4)))
o += ['', 'n: %s. Phase 0: one resample of 20,000 has denE <= 0 and is left out (the same in the first program).' % ', '.join('%s %d' % (p, i4['n'][p]) for p in P4), '',
      'Zero-margin points (g = 0, all evaluated decisions):', '', '| Arm | Caution (%) | Wrong go (%) | Wrong-go decisions |', '|---|---|---|---|']
for a, v in i4['zero_margin'].items():
    o.append('| %s | %s | %s | %d |' % (a, f(v['caution_pct']), f(v['wrong_go_pct']), v['wrong_go_decisions']))
t = bn['total']
o += ['', 'Benign-driving tuning runs (%d runs with `meta.family == \'benign\'`, all of the tuning set; `cCK3` from the `ck` folder, `cF0` from `gateR_rt_v01`):' % bn['n_runs'], '',
      '- evaluated decisions: **%d** (of %d stored);' % (t['evaluated_decisions'], t['stored_decisions']),
      '- evaluated decisions whose selected row differs between the braking prediction and the class average: **%d** at g = 0, **%d** at g = 1;' % (t['differ_g0'], t['differ_g1']),
      '- wrong-go decisions at zero margin: **%d** under the braking prediction, **%d** under the class average.' % (t['wrong_go_g0_CK3'], t['wrong_go_g0_F0']), '']
# ---- comparison
o += ['## Comparison with the first program', '', 'Details: `RECOUNT3_COMPARE_v01.md` (counts, largest differences) and `RECOUNT3_COMPARE_v01.json` (every comparison).', '',
      '| Item | Asked for by the brief (A): compared / differ | All classes: compared / differ | Largest absolute difference |', '|---|---|---|---|']
for it, lab in ((1, 'Table S12b'), (2, 'Table S17 subsampling'), (3, 'Table S24b'), (4, 'Table S25 and benign check')):
    o.append('| %d. %s | %d / %d | %d / %d | %.1e |' % (it, lab, S['%dA' % it]['compared'], S['%dA' % it]['differ'], S['%dall' % it]['compared'],
                                                       S['%dall' % it]['differ'], S['%dall' % it]['max_abs_diff']))
n_und = sum(1 for x in cp['rows'] if x['note'] == 'undefined in both'); n_flag = sum(1 for x in cp['rows'] if x['note'] == 'flag')
o += ['', 'No difference above 1e-9 was found, so there is no cause to report. The largest differences are of the size of floating-point rounding.', '',
      'What the counts do and do not show:', '',
      '- Class A (%d numbers) are the brief\'s numbers, taken from the results file as it stood before the first program\'s files were opened.' % sum(S['%dA' % k]['compared'] for k in (1, 2, 3, 4)),
      '- Class B (%d) are further entries of that results file (phases 0-2 of Table S24b, RR0(Q), denE, n, resamples left out) and entries of the first '
      'program\'s files that follow by arithmetic from it (basic intervals, intervals without the finite-population factor, percentiles of the draws, '
      'sums instead of pp). The arithmetic ones are not separate tests of the scoring.' % sum(S['%dB' % k]['compared'] for k in (1, 2, 3, 4)),
      '- Class C (%d) were recomputed after the files were opened: phase 0 and the draw of record of Table S12b (%d), RR0 and den0 of Table S25 (%d), '
      'and the first program\'s full scoring of the benign runs (%d), where the room is 0 and most entries are 0 or undefined.' % (
          sum(S['%dC' % k]['compared'] for k in (1, 4)),
          sum(1 for x in cp['rows'] if x['cls'] == 'C' and x['name'].startswith('S12b')),
          sum(1 for x in cp['rows'] if x['cls'] == 'C' and x['name'].startswith('S25')),
          sum(1 for x in cp['rows'] if x['cls'] == 'C' and x['name'].startswith('benign'))),
      '- Of the %d comparisons, %d are "undefined in both programs" (no ratio: phase 0 of Table S24b, benign runs) and %d are yes/no flags.' % (
          cp['total']['compared'], n_und, n_flag),
      '- In the first program\'s file `REV_F2_BRAKING_PRIOR_v01.json` the sweep over a0 is keyed `S20` and the benign-run check `S18`; in '
      '`rev_g_partial_oracle_draws_v01.py` the partial-oracle draws are called check S19. These are the first program\'s own labels, not the table '
      'numbers of the brief (S25, S12b); the blocks were matched by content.', '']
# ---- ambiguities
sp = dg['sensitivity_points']
o += ['## Ambiguities in the brief and how they were resolved', '',
      '1. **Phase-weighted aggregate, the n.** Taken as n = n0 + n1 + n2, rebuilt in every resample. No evaluated decision has phase 3 here, so this n '
      'equals the number of evaluated decisions (8,290) and the two readings coincide. Decision-equivalents of the aggregate = aggregated D / 201 / 100 x n.',
      '2. **Item 2, "finite roots".** Could mean every finite quotient or only quotients with a positive denominator. Both were computed; they are '
      'identical because all 15,000 subsamples have positive denE and den0.',
      '3. **Item 3, "with the 95% interval of record" for den0.** Given for both units (pp and decision-equivalents). In a resample the decision-equivalents '
      'use the resample\'s own n.',
      '4. **Item 3, "the 3 s window\'s reaction-and-stop clearance of record (the pack cache)".** Taken as key `t0p75_a6p0` of the pack cache. The second '
      'program\'s own 61-frame clearance (`clear61_t0p75_a6p0` of recount2) gives the same count (%d).' % c3['pairs_unsafe_window_own61'],
      '5. **Item 4, "at g = 1".** The grid holds the value 1.0 exactly (%s); selecting at exactly 1.0 and at the grid value gives the same count (%d and %d).' % (
          bn['g1_grid_value_is_exactly_1'], t['differ_g1'], t['differ_g1_gridvalue']),
      '6. **Item 4, "zero-margin point for each a0".** Taken as the arm\'s own point at g = 0 (not the prepended F0 point). "Wrong-go decisions at zero '
      'margin" in the benign runs: the selected row\'s 3 s clearance is <= 0.',
      '7. **Item 3, plans whose recording ends before the stop.** The brief does not say how to judge them. The clearances of recount2 were used as stored: '
      'the minimum over the frames that exist. Of %d pairs, %d stop after the 3 s window and %d of these are cut short by the end of the recording (in %d decisions); '
      '%d of the cut-short pairs are counted safe at 2 m. The first program\'s numbers agree with this reading. As a bound (points only, not compared, '
      'computed after the comparison): if those %d pairs are counted unsafe instead, den0 moves from %s to %s pp (all), %s to %s pp (ego moving) and %s to %s pp '
      '(phase-weighted; %s to %s decision-equivalents), and RR0(CK3) from %s to %s (all) and %s to %s (phase-weighted). Table S24b therefore depends visibly on this choice.' % (
          dg['pairs'], dg['late'], dg['censored'], dg['decisions_with_a_censored_pair'], dg['censored_and_counted_safe_at_2m'], dg['censored_and_counted_safe_at_2m'],
          f(sp['as_computed']['all']['den0_pp']), f(sp['censored_pairs_unsafe']['all']['den0_pp']),
          f(sp['as_computed']['moving']['den0_pp']), f(sp['censored_pairs_unsafe']['moving']['den0_pp']),
          f(sp['as_computed']['phase_weighted']['den0_pp']), f(sp['censored_pairs_unsafe']['phase_weighted']['den0_pp']),
          f(sp['as_computed']['phase_weighted']['den0_deceq'], 2), f(sp['censored_pairs_unsafe']['phase_weighted']['den0_deceq'], 2),
          f(sp['as_computed']['all']['RR0_CK3']), f(sp['censored_pairs_unsafe']['all']['RR0_CK3']),
          f(sp['as_computed']['phase_weighted']['RR0_CK3']), f(sp['censored_pairs_unsafe']['phase_weighted']['RR0_CK3'])),
      '8. **Bootstrap of the benign runs (supplementary only).** The first program resamples the 20 benign runs with seed 20261125 through a function of the '
      'A6R code, which was not opened. The supplementary script used `default_rng(20261125).integers(0, 20, size=(20000, 20))`. Every resample gives a room '
      'of 0 (no wrong go at any scale), so these intervals are [0, 0] or undefined whatever the draw; their agreement does not test the draw.', '']
o += ['## Notes on the results file', '',
      '- `item3_S24b.counts.pairs_late` in `RECOUNT3_RESULTS_v01.json` is an unused placeholder (always 0), not a count. The file was left as written before '
      'the comparison; the count of late pairs (%d) is in `r3_extra_v01_out.json`.' % dg['late'],
      '- Between the 3 s window and the judgement until the stop ends, %d pairs change from safe to unsafe at 2 m and %d the other way; the first safe row '
      'changes in %d decisions.' % (dg['safe_window_cache_unsafe_until_stop'], dg['unsafe_window_cache_safe_until_stop'], dg['decisions_whose_first_safe_row_changes']), '']
o += ['## Files (all in `revision_v11\\recount3`)', '',
      '- `RECOUNT3_RESULTS_v01.json`: the results, one entry per number (item 1 also holds the 50 draw values per cell).',
      '- `r3_lib_v01.py`, `r3_items_v01.py`: the program. `r3_items_v01_log.txt`, `r3_items_v01_stdout.txt`: its log.',
      '- `r3_naive_v01.py`, `r3_naive_v01_out.json`: the self-check by a second route.',
      '- `r3_extra_v01.py`, `r3_extra_v01_out.json`: supplementary numbers (class C) and the diagnostics of item 3, written after the comparison files were opened.',
      '- `r3_compare_v01.py`, `RECOUNT3_COMPARE_v01.md`, `RECOUNT3_COMPARE_v01.json`: the comparison.',
      '- `r3_probe_v01.py`, `r3_show_v01.py`, `r3_peek_v01.py` (`r3_peek_F2.txt`), `r3_report_v01.py`: helpers (input probe, printout of own results, '
      'structure of the first program\'s files, this report).',
      '- `RECOUNT3_RESULTS_v01_quick.json`: a test run on the first 400 rows of the draw of record; not a result.', '']
(HERE / 'RECOUNT3_REPORT_v01.md').write_text('\n'.join(o), encoding='utf-8')
print('report written, %d lines' % len(o))
