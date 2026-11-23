"""Recount4: writes RECOUNT4_REPORT_v01.md from the files of this folder (results, comparison, self-check, diagnostics).
The record made before the first program's file was opened is taken verbatim from r4_record_before_compare_v01.md.
Usage: python -B -X utf8 r4_report_v01.py"""
import hashlib, json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
M = json.loads((HERE / 'RECOUNT4_RESULTS_v01.json').read_text(encoding='utf-8'))
C = json.loads((HERE / 'RECOUNT4_COMPARE_v01.json').read_text(encoding='utf-8'))
NV = json.loads((HERE / 'r4_naive_v01_out.json').read_text(encoding='utf-8'))
DG = json.loads((HERE / 'r4_diag_v01_out.json').read_text(encoding='utf-8'))
EX = json.loads((HERE / 'r4_extra_v01_out.json').read_text(encoding='utf-8'))
NG = json.loads((HERE / 'r4_compare_negctl_v01_out.json').read_text(encoding='utf-8'))
S = M['scorings']
SET = M['settings']
A6 = [k for k in SET if k.endswith('_a6p0')]
MAIN = 't0p75_a6p0'
POPS = [('all', 'All evaluated'), ('moving', 'Ego moving'), ('phase0', 'Phase 0 (before onset)'), ('phase1', 'Phase 1 (lead braking)'),
        ('phase2', 'Phase 2 (lead stopped)'), ('phase_weighted', 'Phase-weighted')]
SRC = ('N', 'NA', 'AM', 'CK3', 'Q')


def lab(key):
    t, a = key.split('_')
    return '%s s, %s m/s2' % (t[1:].replace('p', '.'), a[1:].replace('p', '.'))


def f(x, d=4):
    return 'n/a' if x is None else ('%.' + str(d) + 'f') % x


def pc(e, d=4):
    if e.get('point_denominator_positive') is False:
        return 'n/a'
    if e['ci'] is None:
        return '%s [n/a]' % f(e['point'], d)
    return '%s [%s, %s]' % (f(e['point'], d), f(e['ci'][0], d), f(e['ci'][1], d))


def sha(name):
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


rec = (HERE / 'r4_record_before_compare_v01.md').read_text(encoding='utf-8')
i0 = rec.index('## Record made before'); i1 = rec.index('(The rest of this report')
record = rec[i0:i1].rstrip()

t = C['summary']['total']; bc = C['summary']['by_class']
own = C['own_brief_numbers_without_counterpart']
n_on = sum(v['n_on_brief'] for v in own.values()) + 72
n_with = sum(v['n_with_counterpart'] for v in own.values()) + 72
e0 = S['est_' + MAIN]['pops']['all']; c0 = S['cens_' + MAIN]['pops']['all']
L = []
A = L.append
A('# Recount4: independent second program for the scoring of the reaction-and-stop estimate')
A('')
A('Written 18 Nov 2026. Brief: `RECOUNT4_BRIEF_v01.md` (this folder), with the inputs, scoring definitions and bootstrap of record of `revision_v11\\recount\\RECOUNT_BRIEF_v01.md`.')
A('')
A('## Result in short')
A('')
A('- The scoring behind Tables III and IV was recomputed by a second program for every setting, every population and both variants: 17 scorings (the estimate at 9 settings, censored pairs unsafe at the 6 settings with 6 m/s2, signed caution and the 3 s window at 0.75 s and 6 m/s2), 6 populations each, points and 95%% percentile intervals of the draw of record (20,000 resamples), and the pair counts at 9 settings. That is %d numbers on the brief\'s list.' % n_on)
A('- Compared with the first program (`REV_E2_EXTENDED_TRUTH_v01.json`): **%d numbers, 0 differ by more than 1e-9** (largest absolute difference %.1e). %d of them are on the brief\'s list (class A), %d are further entries that were in the results file or follow from it by arithmetic (class B), and %d were recomputed after the first program\'s file was opened (class C).' % (
    t['compared'], t['max_abs_diff'], bc['A']['compared'], bc['B']['compared'], bc['C']['compared']))
A('- %d numbers on the brief\'s list have no counterpart in the first program\'s file, because the first program did not bootstrap every scoring and did not score every source in every scoring (list under "Comparison"). They stand on the second program alone and are covered only by its self-check.' % (n_on - n_with))
A('- Entries of the first program\'s file not compared: the scorings `ii_*` and `est_gap2_*` (242 numeric entries each; outside this brief), the 17 `bootstrap` switches and `seconds`.')
A('- Self-check by a second route (`r4_naive_v01.py`, finished before the first program\'s file was opened): %d points and %d values of three resamples per scoring recomputed without the libraries\' scoring code, largest difference %.1e; all %d intervals, shares and ratios of the results file recomputed from the stored resamples with a hand-written percentile, largest difference %.1e; %d pair counts recounted, 0 differ.' % (
    NV['part1']['points']['n'], NV['part1']['resamples']['n'], max(NV['part1']['points']['max_abs'], NV['part1']['resamples']['max_abs']),
    NV['part2']['n'], NV['part2']['max_abs'], NV['part3']['n']))
A('- Headline values (0.75 s, 6 m/s2, all %d evaluated decisions): den0 = %s pp = %s decision-equivalents; denE = %s pp; relative to the 3 s commitment denE %s and den0 %s. With censored pairs unsafe: den0 = %s pp = %s decision-equivalents.' % (
    e0['n'], pc(e0['den0']['pp']), pc(e0['den0']['deceq'], 2), pc(e0['denE']['pp']), pc(e0['rel']['3s_commitment']['denE']), pc(e0['rel']['3s_commitment']['den0']),
    pc(c0['den0']['pp']), pc(c0['den0']['deceq'], 2)))
A('')
A(record)
A('')
A('## Independence and order of work')
A('')
A('- Read before the program was written: the two briefs; `revision_v11\\recount\\rc_lib_v01.py`; `revision_v11\\recount3\\r3_lib_v01.py`, `r3_items_v01.py`, the start of `r3_naive_v01.py`, `RECOUNT3_REPORT_v01.md` and the timing log; of `revision_v11\\recount2`: `recount2_score_v01.py`, the headers of `recount2_ext_v01.py` and `probe_v01.py`, the start of `RECOUNT2_SCORING_v01.json`. Arrays opened: the stored runs, the extraction, the pack cache (through `rc_lib_v01.load_all`) and `recount2\\out`.')
A('- Not opened before the results file was hashed: anything of `revision_v11\\analysis`, `revision_v11\\draft`, `revision_v11\\package_v11`, `P\\11_ojits\\A6R\\code`. Not opened at any time: `revision_v11\\draft`, `revision_v11\\package_v11`, `<excluded folder 1>`, `<excluded folder 2>`, `<excluded folder 3>`. No network. Nothing was written outside this folder; Python ran with `-B`. (A listing of files changed since the brief, made at the end to confirm this, showed names of files in `revision_v11\\analysis`, `revision_v11\\draft` and `revision_v11` itself that other sessions changed in the meantime; none was opened or written by this recount.)')
A('- Order: program (`r4_items_v01.py`), test on 400 resamples, full run, self-check (`r4_naive_v01.py`), record of the hashes, and only then the first program\'s file. After that, to learn the meaning of entries the brief does not list (`outside`, `basic`, `branch`, `oracle_diag`), `revision_v11\\analysis\\rev_e2_extended_truth_score_v01.py`, `rev_common_v01.py` and parts of `P\\11_ojits\\A6R\\code\\optA_lib_v02.py` were read.')
A('- Nothing in the program or in the results file was changed after the comparison. `RECOUNT4_RESULTS_v01.json` still has the recorded hash (`r4_compare_v01.py` refuses to run otherwise). Written after the comparison: `r4_compare_v01.py`, `r4_diag_v01.py`, `r4_extra_v01.py`, `r4_report_v01.py` and the helpers `r4_peek*_v01.py`.')
A('')
A('## Inputs and checks on them')
A('')
d = M['data']
A('- %d evaluation runs, %d stored decisions, %d evaluated; by phase: %s before onset, %s lead braking, %s lead stopped, %s unknown; ego moving: %d.' % (
    d['runs'], d['stored_decisions'], d['evaluated_decisions'], d['phase_counts_evaluated']['0'], d['phase_counts_evaluated']['1'],
    d['phase_counts_evaluated']['2'], d['phase_counts_evaluated']['3'], d['moving_evaluated']))
A('- `k` and the evaluated flags of `recount2\\out` equal the stored ones in every run (the program stops otherwise).')
A('- NaN among evaluated decisions: 3 s clearance %d; `clearX` %d and `clear61` %d over all nine settings.' % (
    d['nan_clear_evaluated'], sum(M['counts'][k]['nan_clearX'] for k in SET), sum(M['counts'][k]['nan_clear61'] for k in SET)))
A('- In every setting `clearX` <= `clear61` for every pair (%d pairs above), `clearX` = `clear61` wherever `late` is false (%d pairs differ), and every censored pair is late (%d not late).' % (
    sum(EX[k]['clearX_above_clear61'] for k in SET), sum(EX[k]['not_late_but_clearX_differs'] for k in SET), sum(EX[k]['cens_not_late'] for k in SET)))
A('- The pack cache clearance (the first program\'s "as scored") and recount2\'s own `clear61` give the same safe flag for every pair in all nine settings (%d flags differ; %d values differ by more than 1e-9).' % (
    sum(EX[k]['cache_flag_differs_from_clear61'] for k in SET), sum(EX[k]['cache_value_differs_from_clear61_by_more_than_1e9'] for k in SET)))
A('- Anchor inside the second-program lineage: the points of recount2\'s optional scoring (`RECOUNT2_SCORING_v01.json`: 3 s commitment, 3 s window, estimate, censored pairs unsafe; all and ego moving; denE and den0) are reproduced, largest difference %.1e (16 values).' % M['anchor_recount2_scoring']['max_abs_diff'])
A('')
A('## Method')
A('')
A('- Wrong go of a scoring: the selected row is not judged safe by it. `est`: safe when `clearX` > 0. `cens`: safe when `clearX` > 0 and `cens` is false. `asscored`: safe when `clear61` > 0. Reference `w1` (the 3 s commitment): safe when `clear` > 0.')
A('- Caution always uses the 3 s commitment: truly safe rows and the first truly safe row from `clear` > 0; caution = mean over evaluated decisions whose selected row is truly safe of (speed of the first truly safe row - speed of the selected row) / desired speed, in %. Signed caution: mean over every evaluated decision with a truly safe row, at its signed difference.')
A('- Grid of 202 margin scales, selection of the first row whose critical scale is >= the scale (fallback row otherwise), step frontier on 201 levels from F0\'s zero-margin caution to min(largest caution of F0, largest caution of E), levels rebuilt in every population and resample; every arm other than F0 and E, and the perfect oracle O, get F0\'s zero-margin point in front. denE = sum over levels of F_F0 - F_E; D(A) likewise; den0 = D(O), O = per decision the first row the scoring judges safe (fallback row if none). Percentage points = sum / 201; decision-equivalents = sum / 201 / 100 x n with the resample\'s own n.')
A('- Populations: all evaluated; ego moving (`v0` > 0.5); phases 0, 1, 2; phase-weighted = sum over phases 0-2 of (n_p / n) x the phase\'s sum, n = n_0 + n_1 + n_2, ratios formed from the aggregated sums.')
A('- Bootstrap of record: `numpy.random.default_rng(20261113).integers(0, 35, size=(20000, 35))`. Each run is reduced to per-scale counts (wrong-go count, caution sum, caution count per population and arm), so a resample is a weighted sum of 35 vectors. Intervals: `numpy.percentile` at 2.5 and 97.5; for ratios over the resamples with a positive denominator, the number left out is stored.')
A('- Relative to 3 s: denE (or den0) of the scoring divided by denE (den0) of the 3 s commitment, numerator and denominator from the same resample.')
A('- Code: `r4_items_v01.py` uses `rc_lib_v01.load_all` and `run_row` (loader, selection, per-run statistics, signed caution), `r3_lib_v01.evaluate_g`, `boot_g`, `weighted`, `ci_ratio`, `ci_plain` (frontier, bootstrap, aggregate, intervals). The safe flags of the four scorings, the references, the ratios to 3 s, the shares, the decision-equivalents and the pair counts are written in `r4_items_v01.py`. The per-resample sums are kept in `boot\\<scoring>.npz`.')
A('- Self-check (`r4_naive_v01.py`), sharing only the loader and the grid: decisions concatenated, selection by a loop over rows, unsafe flags written out again, levels by `numpy.linspace`, frontier by a loop over levels; all %d points (27 scorings x 6 populations x n, denE, den0, D of five sources) and resamples 0, 7 and 19999 of the draw (%d values); every summary of the results file from the stored resamples with name-based column lookup and a hand-written percentile (%d values); the pair counts with other expressions (%d). Largest difference %.1e; no mismatch. Limit of this check: its second part tests the summaries, not the 20,000 resampled sums themselves, of which three per scoring are tested by the first part.' % (
    NV['part1']['points']['n'], NV['part1']['resamples']['n'], NV['part2']['n'], NV['part3']['n'],
    max(NV['part1']['points']['max_abs'], NV['part1']['resamples']['max_abs'], NV['part2']['max_abs'])))
A('')
A('## Results')
A('')
A('All numbers, with intervals, are in `RECOUNT4_RESULTS_v01.json` (`scorings.<name>.pops.<population>`; `counts.<setting>`). Intervals in brackets are 95% percentile intervals of the draw of record.')
A('')
A('### The estimate, all evaluated decisions (n = %d), by setting' % e0['n'])
A('')
A('| Setting | den0 (pp) | den0 (decision-equivalents) | denE (pp) | denE / denE(3 s) | den0 / den0(3 s) | Share of resamples den0 <= 0 / denE <= 0 |')
A('|---|---|---|---|---|---|---|')
for k in SET:
    e = S['est_' + k]['pops']['all']
    A('| %s | %s | %s | %s | %s | %s | %.4f / %.4f |' % (lab(k), pc(e['den0']['pp']), pc(e['den0']['deceq'], 2), pc(e['denE']['pp']),
                                                     pc(e['rel']['3s_commitment']['denE']), pc(e['rel']['3s_commitment']['den0']),
                                                     e['share_den0_le0'], e['share_denE_le0']))
A('')
A('RR0 (share of den0), all evaluated decisions:')
A('')
A('| Setting | N | NA | AM | CK3 | Q | E |')
A('|---|---|---|---|---|---|---|')
for k in SET:
    e = S['est_' + k]['pops']['all']
    A('| %s | %s | %s | %s | %s | %s | %s |' % ((lab(k),) + tuple(pc(e['src'][a]['RR0']) for a in SRC) + (pc(e['RR0_E']),)))
A('')
A('### The estimate at 0.75 s and 6 m/s2, by population')
A('')
A('| Population | n | den0 (pp) | den0 (decision-equivalents) | denE (pp) | denE / denE(3 s) | den0 / den0(3 s) | Share den0 <= 0 |')
A('|---|---|---|---|---|---|---|---|')
for pn, pl in POPS:
    e = S['est_' + MAIN]['pops'][pn]
    A('| %s | %d | %s | %s | %s | %s | %s | %.4f |' % (pl, e['n'], pc(e['den0']['pp']), pc(e['den0']['deceq'], 2), pc(e['denE']['pp']),
                                                    pc(e['rel']['3s_commitment']['denE']), pc(e['rel']['3s_commitment']['den0']), e['share_den0_le0']))
A('')
A('| Population | RR0(N) | RR0(NA) | RR0(AM) | RR0(CK3) | RR0(Q) | RR0(E) |')
A('|---|---|---|---|---|---|---|')
for pn, pl in POPS:
    e = S['est_' + MAIN]['pops'][pn]
    A('| %s | %s | %s | %s | %s | %s | %s |' % ((pl,) + tuple(pc(e['src'][a]['RR0']) for a in SRC) + (pc(e['RR0_E']),)))
A('')
A('| Population | D(N) | D(NA) | D(AM) | D(CK3) | D(Q) |')
A('|---|---|---|---|---|---|')
for pn, pl in POPS:
    e = S['est_' + MAIN]['pops'][pn]
    A('| %s | %s | %s | %s | %s | %s |' % ((pl,) + tuple(pc(e['src'][a]['D_deceq'], 2) for a in SRC)))
A('')
A('(D in decision-equivalents. In phase 0 the estimate leaves no room at this setting: den0 = denE = 0 in the full sample and in every resample, so no ratio exists there; the same holds in both programs.)')
A('')
A('### Censored pairs unsafe, all evaluated decisions, by setting')
A('')
A('| Setting | den0 (pp) | den0 (decision-equivalents) | denE / denE(3 s) | den0 / den0(3 s) | RR0(AM) | RR0(CK3) | RR0(E) |')
A('|---|---|---|---|---|---|---|---|')
for k in A6:
    e = S['cens_' + k]['pops']['all']
    A('| %s | %s | %s | %s | %s | %s | %s | %s |' % (lab(k), pc(e['den0']['pp']), pc(e['den0']['deceq'], 2), pc(e['rel']['3s_commitment']['denE']),
                                                 pc(e['rel']['3s_commitment']['den0']), pc(e['src']['AM']['RR0']), pc(e['src']['CK3']['RR0']), pc(e['RR0_E'])))
A('')
A('### The four scorings at 0.75 s and 6 m/s2')
A('')
A('| Scoring | Population | den0 (pp) | den0 (decision-equivalents) | RR0(AM) | RR0(CK3) | RR0(E) |')
A('|---|---|---|---|---|---|---|')
for nm, lb in (('est_' + MAIN, 'Estimate'), ('cens_' + MAIN, 'Censored pairs unsafe'), ('est_signed_' + MAIN, 'Estimate, signed caution'),
               ('asscored_' + MAIN, '3 s window only')):
    for pn, pl in (('all', 'All evaluated'), ('moving', 'Ego moving'), ('phase_weighted', 'Phase-weighted')):
        e = S[nm]['pops'][pn]
        A('| %s | %s | %s | %s | %s | %s | %s |' % (lb, pl, pc(e['den0']['pp']), pc(e['den0']['deceq'], 2), pc(e['src']['AM']['RR0']),
                                                pc(e['src']['CK3']['RR0']), pc(e['RR0_E'])))
A('')
es = S['est_signed_' + MAIN]['pops']['all']['rel']
A('Signed caution, relative to 3 s (all evaluated): against the 3 s commitment with the paper\'s caution, denE %s and den0 %s; against the 3 s commitment with signed caution, denE %s and den0 %s.' % (
    pc(es['3s_commitment']['denE']), pc(es['3s_commitment']['den0']), pc(es['3s_commitment_signed']['denE']), pc(es['3s_commitment_signed']['den0'])))
A('')
A('### Pair counts over the %d evaluated decisions (%d decision-row pairs)' % (M['counts'][MAIN]['evaluated_decisions'], M['counts'][MAIN]['pairs']))
A('')
A('| Setting | Unsafe on the 3 s window | Unsafe under the estimate | Late and safe on the window | of those unsafe under the estimate | Censored and safe on the window | of those safe under the estimate | Decisions without a row the estimate judges safe |')
A('|---|---|---|---|---|---|---|---|')
for k in SET:
    c = M['counts'][k]
    A('| %s | %d | %d | %d | %d | %d | %d | %d |' % (lab(k), c['pairs_unsafe_window'], c['pairs_unsafe_est'], c['pairs_late_safe_window'],
                                                  c['pairs_late_safe_window_unsafe_est'], c['pairs_cens_safe_window'], c['pairs_cens_safe_window_safe_est'],
                                                  c['decisions_without_safe_row_est']))
A('')
A('Further counts in the results file (not on the brief\'s list): late pairs, censored pairs, pairs unsafe under the 3 s commitment (%d), decisions with a censored pair, decisions without a safe row when censored pairs count as unsafe.' % M['counts'][MAIN]['pairs_unsafe_3s_commitment'])
A('')
A('## Comparison with the first program')
A('')
A('Details: `RECOUNT4_COMPARE_v01.md` (counts per scoring) and `RECOUNT4_COMPARE_v01.json` (every comparison with both values). First program\'s file: written %s, sha256 `%s`.' % (C['first_program_written'], C['first_program_sha256']))
A('')
A('| Scoring family | Compared | Differ | A: compared / differ | B: compared / differ | C: compared / differ | Largest absolute difference |')
A('|---|---|---|---|---|---|---|')
nm = dict(est='est (9 settings)', cens='cens (6 settings)', est_signed='est_signed (0.75 s, 6 m/s2)', asscored='asscored (0.75 s, 6 m/s2)', pair_counts='pair counts (9 settings)')
for fam in ('est', 'cens', 'est_signed', 'asscored', 'pair_counts'):
    s = C['summary']['by_family'][fam]
    A('| %s | %d | %d | %d / %d | %d / %d | %d / %d | %.1e |' % (nm[fam], s['all']['compared'], s['all']['differ'], s['A']['compared'], s['A']['differ'],
                                                             s['B']['compared'], s['B']['differ'], s['C']['compared'], s['C']['differ'], s['all']['max_abs_diff']))
A('| **Total** | **%d** | **%d** | %d / %d | %d / %d | %d / %d | %.1e |' % (t['compared'], t['differ'], bc['A']['compared'], bc['A']['differ'], bc['B']['compared'], bc['B']['differ'],
                                                                      bc['C']['compared'], bc['C']['differ'], t['max_abs_diff']))
A('')
A('No difference above 1e-9 was found, so there is no cause to report.')
A('')
A('What the counts do and do not show:')
A('')
A('- Class A (%d) are numbers on the brief\'s list, taken from the results file as it stood before the first program\'s file was opened. Class B (%d) are entries not on the list that were in that file or follow from it by arithmetic: resamples left out of a ratio (count and share), the count of resamples with a sum <= 0, the flag "point outside its interval", the basic interval 2 x point - percentile, the perfect oracle\'s point, F0\'s zero-margin caution, the flag signed caution, the pairs unsafe under the 3 s commitment. The arithmetic ones are not separate tests of the scoring. Class C (%d) were recomputed after the first program\'s file and script were read: minimum, maximum and number of undefined levels of the perfect oracle\'s frontier (from the stored points), and the first program\'s branch number (its rule and its two thresholds, 2.5%% of resamples left out and 10 decision-equivalents, applied to the second program\'s numbers; %d entries).' % (
    bc['A']['compared'], bc['B']['compared'], bc['C']['compared'], sum(DG['branch'].values())))
A('- Of the %d comparisons, %d are "undefined in both programs" (ratios in phase 0, where numerator and denominator are 0), %d are yes/no flags, %d are numbers that are exactly 0 in both programs, and %d numbers are bit-identical.' % (
    t['compared'], t['undefined_in_both'], t['flags'], DG['both_exactly_zero'], DG['bit_identical']))
A('- The two programs share the draw of record and the stored inputs. They do not share the clearances judged until the stop ends (first program: `analysis\\out\\ext`; second: `recount2\\out`), the "as scored" clearance (first: the pack cache; second: recount2\'s own 61-frame clearance) or any scoring code.')
A('- Negative control of the comparison script (`r4_compare_v01.py negctl`): with the second program\'s blocks `est_t0p75_a6p0` and `cens_t0p75_a6p0` swapped and the pair counts of two settings swapped, it reports %d differences (%s).' % (
    NG['total']['differ'], '; '.join('%s: %d of %d' % (k, v['differ'], v['compared']) for k, v in NG['by_scoring'].items())))
A('')
A('### Numbers on the brief\'s list without a counterpart in the first program\'s file (%d of %d)' % (n_on - n_with, n_on))
A('')
A('The first program bootstrapped `est` at the six settings with 6 m/s2, `cens` at 0.75 s and `est_signed`; it gave points only for `est` at 4, 5 and 7.6 m/s2, for `cens` at the five other settings and for `asscored`. It scored N, NA, CK3, AM and Q at 0.75 s and 6 m/s2 (`est`, `cens`, `asscored`), N, NA, CK3 and AM for the other `est` settings and for `est_signed`, and N and CK3 for `cens` at the other settings. So without counterpart are:')
A('')
A('- `est` at 0.75 s with 4, 5 and 7.6 m/s2: every interval and share, and source Q (450 numbers each);')
A('- `cens` at 0.5, 1.0, 1.25, 1.5 and 1.8 s: every interval and share, and sources NA, AM and Q (510 each);')
A('- `asscored`: every interval and share (420);')
A('- `est` at 0.5, 1.0, 1.25, 1.5 and 1.8 s: source Q, and the intervals of D as a sum and in pp (186 each);')
A('- `est_signed`: source Q, the intervals of the ratios to 3 s, and the intervals of D as a sum and in pp (210);')
A('- `est` and `cens` at 0.75 s and 6 m/s2: only the intervals of D as a sum and in pp (120 each; the first program gives the interval of D in decision-equivalents only).')
A('')
A('| Scoring | On the brief\'s list | With counterpart | Without |')
A('|---|---|---|---|')
for name in ['est_' + k for k in SET] + ['cens_' + k for k in A6] + ['est_signed_' + MAIN, 'asscored_' + MAIN]:
    v = own[name]
    A('| `%s` | %d | %d | %d |' % (name, v['n_on_brief'], v['n_with_counterpart'], v['n_without_counterpart']))
A('| pair counts | 72 | 72 | 0 |')
A('| **Total** | **%d** | **%d** | **%d** |' % (n_on, n_with, n_on - n_with))
A('')
A('### Entries of the first program\'s file that were not compared')
A('')
for e in C['not_compared']:
    if e['path'].startswith('scorings.') and not e['path'].endswith('.bootstrap'):
        A('- `%s`: %d numeric entries; %s.' % (e['path'], e['n_entries'], e['reason']))
A('- `scorings.<name>.bootstrap` (17 entries): a switch of the first program (whether it bootstrapped the scoring), not a result.')
A('- `seconds`: run time. `code`, `status`, `written`, `common_sha256`: text.')
A('- Every other numeric entry of the file was compared.')
A('')
A('## Ambiguities in the brief and how they were resolved')
A('')
ew = e0['rel']['3s_window_same_setting']
A('1. **"Relative to 3 s".** The definition names "the 3 s commitment" (unsafe when `clear` <= 0), while the list of scorings also has a "3 s window only" scoring (`clear61`). The 3 s commitment was used (`rel.3s_commitment`). The first program reads it the same way and every ratio agrees. As an addition, the ratio to the 3 s-window scoring at the same setting is stored (`rel.3s_window_same_setting`; at 0.75 s and 6 m/s2, all: denE %s, den0 %s). It has no counterpart in the first program\'s file.' % (pc(ew['denE']), pc(ew['den0'])))
A('2. **Signed caution, relative to 3 s.** The denominator can be the 3 s commitment with the paper\'s caution or with signed caution. Both are stored; the first was taken as the reading of record before the comparison (`rel.3s_commitment`: denE %s). The first program gives this ratio as a point only and uses the paper\'s caution in the denominator; the points agree. The ratio with signed caution in the denominator (`rel.3s_commitment_signed`: denE %s) has no counterpart.' % (
    pc(es['3s_commitment']['denE']), pc(es['3s_commitment_signed']['denE'])))
A('3. **`cens`.** Read as: a pair is unsafe when `clearX` <= 0 or `cens` is true. recount2\'s optional scoring had instead flagged only censored pairs that are safe on the 3 s window. The two readings give the same flags for every pair in all nine settings (%d pairs differ), because no censored pair is unsafe on the window and safe under the estimate.' % sum(EX[k]['cens_readings_differ'] for k in SET))
A('4. **Shares "den <= 0".** Taken over all 20,000 resamples. No resample has an undefined den0 or denE in any scoring or population (%d), so counting an undefined sum as "<= 0" (as the first program does) gives the same share.' % len(DG['non_finite']))
und_tot = 0; und_nonzero = []
for name_, sc_ in S.items():
    for pn_, e_ in sc_['pops'].items():
        cand = [('RR0_E', e_['RR0_E'], e_['denE']['sum']['point'])]
        for a_, s_ in e_['src'].items():
            cand += [('RR0', s_['RR0'], s_['D_sum']['point']), ('RR', s_['RR'], s_['D_sum']['point'])]
        for rn_, r_ in e_['rel'].items():
            cand += [('rel.' + rn_, r_['denE'], e_['denE']['sum']['point']), ('rel.' + rn_, r_['den0'], e_['den0']['sum']['point'])]
        for tag_, r_, num_ in cand:
            if not r_['point_denominator_positive']:
                und_tot += 1
                if num_ != 0:
                    und_nonzero.append((name_, pn_, tag_))
assert und_tot == sum(DG['undefined_points_by_scoring_pop'].values())
assert all(pn_ == 'phase0' and tag_ == 'rel.3s_window_same_setting' for _, pn_, tag_ in und_nonzero)
A('5. **Point of a ratio whose full-sample denominator is not positive.** The brief does not say. The results file stores the plain quotient with a flag `point_denominator_positive`; the comparison applies the first program\'s convention (undefined). It occurs in %d entries of the results file, all in phase 0: in %d numerator and denominator are both 0 (undefined either way); in the other %d a positive sum stands over a denominator of 0, and all of these are the added ratio to the 3 s-window scoring of point 1 (not on the brief\'s list, no counterpart). No quotient with a non-positive denominator is stored as a number (%d).' % (
    und_tot, und_tot - len(und_nonzero), len(und_nonzero), len(DG['masked_points'])))
A('6. **Intervals.** Sums, percentage points and decision-equivalents: over all resamples (all are finite). Ratios: over the resamples with a positive denominator; for "relative to 3 s" the denominator is the 3 s commitment\'s denE or den0 of the same resample. The number of resamples left out is stored with every ratio.')
A('7. **"D (sum, percentage points, decision-equivalents with interval)".** Intervals are given for all three forms. The first program gives one for the decision-equivalents only.')
A('8. **Phase-weighted aggregate.** n = n_0 + n_1 + n_2 of the resample (no evaluated decision has phase 3, so this is every evaluated decision); the sums are aggregated with weights n_p / n and every ratio, share and decision-equivalent is formed from the aggregated sums.')
A('9. **Perfect oracle of `cens` and `est_signed`.** O selects by the scoring\'s own safe flag (for `cens`: `clearX` > 0 and not censored); its caution follows the scoring\'s caution (signed for `est_signed`).')
A('10. **Pair counts, "unsafe on the 3 s window".** Read as `clear61` <= 0 (the reaction-and-stop clearance on the 61 frames), not the 3 s commitment. The first program counts on the pack cache; the counts agree at all nine settings. The pairs unsafe under the 3 s commitment are stored as well.')
A('11. **`asscored` at the other settings.** The brief asks for 0.75 s and 6 m/s2 only. It was computed at all nine settings because it is the denominator of the added ratio of point 1; the eight others are not on the brief\'s list and have no counterpart.')
A('12. **Source names.** AM is `cA1`; the first program\'s file calls it `A1`. Its population `strat` is the phase-weighted aggregate.')
A('')
A('## Notes on the results')
A('')
ph0 = [lab(k) for k in SET if S['est_' + k]['pops']['phase0']['den0']['sum']['point'] == 0 and S['est_' + k]['pops']['phase0']['share_den0_le0'] == 1.0]
A('- Phase 0 under the estimate: den0 = 0 in the full sample and in every resample at %d of the 9 settings (%s). Ratios do not exist there.' % (len(ph0), '; '.join(ph0)))
pos = [(k, S['est_' + k]['pops']['all']) for k in SET if S['est_' + k]['pops']['all']['share_den0_le0'] > 0]
A('- The estimate\'s den0 (all evaluated) is <= 0 in some resamples at %d of the 9 settings: %s. At 0.5 s the interval of den0 starts at 0. At the other settings no resample has den0 <= 0.' % (
    len(pos), '; '.join('%s: %d of 20,000 (%.2f%%)' % (lab(k), e['n_den0_le0'], 100. * e['share_den0_le0']) for k, e in pos)))
A('- The censored pairs come from few runs: %s of the 35 runs hold a censored pair (by setting: %s). The `cens` intervals therefore rest on whether those runs are drawn.' % (
    '%d to %d' % (min(EX[k]['runs_with_a_cens_pair'] for k in SET), max(EX[k]['runs_with_a_cens_pair'] for k in SET)),
    '; '.join('%s: %d' % (lab(k), EX[k]['runs_with_a_cens_pair']) for k in SET)))
A('- Between the 3 s window and the estimate no pair changes from unsafe to safe (the estimate\'s clearance is a minimum over more frames); the first row judged safe moves in %s decisions (by setting: %s).' % (
    '%d to %d' % (min(EX[k]['decisions_first_safe_row_moves'] for k in SET), max(EX[k]['decisions_first_safe_row_moves'] for k in SET)),
    '; '.join('%s: %d' % (lab(k), EX[k]['decisions_first_safe_row_moves']) for k in SET)))
A('')
A('## Files (all in `revision_v11\\recount4`)')
A('')
A('- `RECOUNT4_RESULTS_v01.json`: the results, one entry per number (sha256 `%s`). `RECOUNT4_RESULTS_v01.sha256.txt`: hash and time written by the program.' % sha('RECOUNT4_RESULTS_v01.json'))
A('- `r4_items_v01.py`: the program (sha256 `%s`, unchanged since the run). `r4_items_v01_log.txt`, `r4_items_v01_stdout.txt`: its log. `boot\\<scoring>.npz`: the per-resample sums of the 27 scorings (226 MB in all; read by the self-check and by class C of the comparison; a rerun of the program reproduces them and the numbers of the results file, but not that file\'s hash, because it holds the run time).' % sha('r4_items_v01.py'))
A('- `r4_naive_v01.py`, `r4_naive_v01_out.json`, `r4_naive_v01_stdout.txt`: the self-check by a second route.')
A('- `r4_compare_v01.py`, `RECOUNT4_COMPARE_v01.md`, `RECOUNT4_COMPARE_v01.json`: the comparison; `r4_compare_negctl_v01_out.json`: its negative control.')
A('- `r4_diag_v01.py` (`r4_diag_v01_out.json`, `r4_diag_v01_stdout.txt`), `r4_extra_v01.py` (`r4_extra_v01_out.json`): diagnostics and supplementary checks written after the comparison.')
A('- `r4_record_before_compare_v01.md`: the report as it stood before the first program\'s file was opened (sha256 `%s`).' % sha('r4_record_before_compare_v01.md'))
A('- `r4_probe_v01.py`, `r4_show_v01.py`, `r4_peek_v01.py`, `r4_peek2_v01.py`, `r4_peek3_v01.py`, `r4_report_v01.py`: helpers (input probe, printout of own results, structure of the first program\'s file, this report).')
A('- `RECOUNT4_RESULTS_v01_quick.json`, `boot_quick\\`: a test run on the first 400 rows of the draw of record; not a result.')
(HERE / 'RECOUNT4_REPORT_v01.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print('written RECOUNT4_REPORT_v01.md, %d lines' % len(L))
