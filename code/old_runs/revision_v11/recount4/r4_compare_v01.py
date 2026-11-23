"""Recount4: comparison of RECOUNT4_RESULTS_v01.json (second program) with the first program's
revision_v11\\analysis\\out\\REV_E2_EXTENDED_TRUTH_v01.json (scorings est_*, cens_*, est_signed_*, asscored_*; ii_* and est_gap2_*
are outside the brief). Written after the own results file was hashed (see RECOUNT4_REPORT_v01.md).

Classes of a compared number:
  A  on the brief's list, taken from the own results file as it stood before the first program's file was opened
  B  not on the brief's list, but in that results file or following from it by arithmetic (counts of resamples left out,
     the yes/no flag "point outside its interval", the basic interval 2 pt - q, diagnostics of the perfect oracle's point)
  C  recomputed after the first program's file and script were opened (min, max and undefined levels of the perfect oracle's
     frontier, from boot\\<scoring>.npz; the branch number, by the first program's rule applied to the own numbers)
Conventions of the first program applied to the own numbers before comparing (none changes a stored number):
  * a ratio's point is undefined when its full-sample denominator is not positive (optA_lib_v02.ratio);
  * population 'strat' = the phase-weighted aggregate; arm 'A1' = AM.
Tolerance: absolute difference 1e-9.
Usage: python -B -X utf8 r4_compare_v01.py  -> RECOUNT4_COMPARE_v01.json, RECOUNT4_COMPARE_v01.md
       python -B -X utf8 r4_compare_v01.py negctl   negative control of this script: the own blocks est_t0p75_a6p0 and
              cens_t0p75_a6p0 are swapped in memory and the pair counts of two settings are swapped; the comparison must then
              report differences. Writes only r4_compare_negctl_v01_out.json.
"""
import hashlib, json, math, pathlib, sys, time
import numpy as np
HERE = pathlib.Path(__file__).resolve().parent
FIRST_PATH = HERE.parent / 'analysis' / 'out' / 'REV_E2_EXTENDED_TRUTH_v01.json'
MINE_PATH = HERE / 'RECOUNT4_RESULTS_v01.json'
SHA_RECORDED = 'b5d428524e066e270d52cc31057c23d5c5accf4b1d88659391a5cfcb2f66f04c'
TOL = 1e-9
MAX_INVALID = 0.025      # optA_lib_v02.MAX_INVALID (read after the own results were hashed; used for class C only)
MIN_DEC_EQ = 10.0        # optA_lib_v02.MIN_DEC_EQ

sha_mine = hashlib.sha256(MINE_PATH.read_bytes()).hexdigest()
if sha_mine != SHA_RECORDED:
    sys.exit('REFUSED: RECOUNT4_RESULTS_v01.json changed since its hash was recorded')
sha_first = hashlib.sha256(FIRST_PATH.read_bytes()).hexdigest()
FIRST = json.loads(FIRST_PATH.read_text(encoding='utf-8'))
MINE = json.loads(MINE_PATH.read_text(encoding='utf-8'))
NB = MINE['nboot']
NEG = 'negctl' in sys.argv
if NEG:
    a, b = 'est_t0p75_a6p0', 'cens_t0p75_a6p0'
    MINE['scorings'][a], MINE['scorings'][b] = MINE['scorings'][b], MINE['scorings'][a]
    MINE['counts']['t1p00_a6p0'], MINE['counts']['t1p25_a6p0'] = MINE['counts']['t1p25_a6p0'], MINE['counts']['t1p00_a6p0']
POPMAP = dict(all='all', moving='moving', phase0='phase0', phase1='phase1', phase2='phase2', strat='phase_weighted')
ARMMAP = dict(N='N', NA='NA', CK3='CK3', A1='AM', Q='Q')
SRC = ('N', 'NA', 'AM', 'CK3', 'Q')
FAMILIES = ('est_signed_', 'est_gap2_', 'asscored_', 'cens_', 'est_', 'ii_')
IGNORED = ('ii_', 'est_gap2_')

records = []           # every comparison
matched = set()        # own class-A leaves that found a counterpart: (scoring, pop, path)
not_compared = []      # numeric entries of the first program's file that were not compared: (path, value, reason)


def family(name):
    for f in FAMILIES:
        if name.startswith(f):
            return f[:-1]
    return 'other'


def undef(v):
    return v is None or (isinstance(v, float) and not math.isfinite(v))


def rec(scoring, pop, entry, first, mine, cls, own_path=None):
    if isinstance(first, bool) or isinstance(mine, bool):
        kind = 'flag'; diff = None
        status = 'equal' if (isinstance(first, bool) and isinstance(mine, bool) and first == mine) else 'DIFFER'
    elif undef(first) and undef(mine):
        kind = 'number'; diff = None; status = 'undefined in both'
    elif undef(first) or undef(mine):
        kind = 'number'; diff = None; status = 'DIFFER'
    else:
        kind = 'number'; diff = abs(float(first) - float(mine)); status = 'equal' if diff <= TOL else 'DIFFER'
    records.append(dict(scoring=scoring, family=family(scoring) if scoring != 'pair_counts' else 'pair_counts', pop=pop, entry=entry,
                        first=None if undef(first) and not isinstance(first, bool) else first,
                        second=None if undef(mine) and not isinstance(mine, bool) else mine, abs_diff=diff, kind=kind, cls=cls, status=status))
    if own_path is not None and cls == 'A':
        matched.add((scoring, pop) + tuple(own_path))


def rec_pair(scoring, pop, entry, first, mine, cls, own_path=None):
    """An interval [lo, hi]: two numbers."""
    mine = mine if mine is not None else [None, None]
    for j in (0, 1):
        rec(scoring, pop, '%s[%d]' % (entry, j), first[j], mine[j], cls, None if own_path is None else tuple(own_path) + (j,))


def my_summ(r):
    """The first program's summary of a ratio (optA_lib_v02.summ), rebuilt from the own entry {point, ci, n_left_out}."""
    pt = r['point'] if r['point_denominator_positive'] else None
    ci = r['ci'] if r['ci'] is not None else [None, None]
    out = dict(point=pt, ci=ci, n_invalid=r['n_left_out'], invalid_share=r['n_left_out'] / NB)
    out['outside'] = bool(pt is not None and ci[0] is not None and not (ci[0] <= pt <= ci[1]))
    out['basic'] = [2. * pt - ci[1], 2. * pt - ci[0]] if (pt is not None and ci[0] is not None) else [None, None]
    return out


def cmp_summ(scoring, pop, entry, fs, r, own_path):
    ms = my_summ(r)
    rec(scoring, pop, entry + '.point', fs['point'], ms['point'], 'A', own_path + ('point',))
    if 'ci' in fs:
        rec_pair(scoring, pop, entry + '.ci', fs['ci'], ms['ci'], 'A', own_path + ('ci',))
        rec(scoring, pop, entry + '.n_invalid', fs['n_invalid'], ms['n_invalid'], 'B')
        rec(scoring, pop, entry + '.invalid_share', fs['invalid_share'], ms['invalid_share'], 'B')
        rec(scoring, pop, entry + '.outside', fs['outside'], ms['outside'], 'B')
        rec_pair(scoring, pop, entry + '.basic', fs['basic'], ms['basic'], 'B')
    extra = set(fs) - {'point', 'ci', 'n_invalid', 'invalid_share', 'outside', 'basic'}
    if extra:
        raise RuntimeError('unexpected keys in %s %s %s: %s' % (scoring, pop, entry, extra))


def branch_num(ms, den_dec_eq):
    """The first program's rule (rev_e2_extended_truth_score_v01.branch_num), applied to the own numbers."""
    inv = ms['invalid_share']; lo, hi = ms['ci']
    if inv > MAX_INVALID or not (den_dec_eq is not None and den_dec_eq >= MIN_DEC_EQ):
        return 1
    if lo is None or hi is None:
        return 0
    if hi < 0:
        return 2
    if lo <= 0 <= hi:
        return 3
    return 4 if lo > 0.5 else 5


def o_frontier(name, pi):
    """Class C: the perfect oracle's step frontier on the 201 levels (its point with F0's zero-margin point in front)."""
    z = np.load(HERE / 'boot' / (name + '.npz'))
    c0 = float(z['c0'][0, pi]); w0 = float(z['w0'][0, pi]); hi = float(z['hi'][0, pi]); cO = float(z['cO'][0, pi]); wO = float(z['wO'][0, pi])
    lev = np.linspace(c0, hi, 201)
    f = np.full(201, np.nan)
    for i, x in enumerate(lev):
        cand = [w for c, w in ((c0, w0), (cO, wO)) if np.isfinite(c) and np.isfinite(w) and c <= x]
        if cand:
            f[i] = min(cand)
    fin = np.isfinite(f)
    return (float(np.nanmin(f)) if fin.any() else None, float(np.nanmax(f)) if fin.any() else None, int((~fin).sum()))


# ------------------------------------------------------------------------------------------------ scorings
for name, fsc in FIRST['scorings'].items():
    if name.startswith(IGNORED):
        n_num = 0

        def walk(o):
            global n_num
            if isinstance(o, dict):
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
            elif isinstance(o, (int, float)):
                n_num += 1
        walk(fsc)
        not_compared.append(dict(path='scorings.' + name, n_entries=n_num, reason='outside the brief (ii_* and est_gap2_* are to be ignored)'))
        continue
    if name not in MINE['scorings']:
        raise RuntimeError('scoring %s of the first program has no counterpart' % name)
    msc = MINE['scorings'][name]
    extra = set(fsc) - {'pops', 'oracle_diag', 'signed_caution', 'bootstrap'}
    if extra:
        raise RuntimeError('unexpected keys in scoring %s: %s' % (name, extra))
    rec(name, '-', 'signed_caution', fsc['signed_caution'], msc['signed_caution'], 'B')
    not_compared.append(dict(path='scorings.%s.bootstrap' % name, n_entries=1,
                             reason='a switch of the first program (whether it bootstrapped this scoring), not a result'))
    for fpop, fe in fsc['pops'].items():
        pop = POPMAP[fpop]; me = msc['pops'][pop]
        extra = set(fe) - {'n', 'den0', 'denE', 'denE_over_3s', 'den0_over_3s', 'E_rr0', 'arms'}
        if extra:
            raise RuntimeError('unexpected keys in %s %s: %s' % (name, fpop, extra))
        rec(name, pop, 'n', fe['n'], me['n'], 'A', ('n',))
        for q in ('den0', 'denE'):
            fd = fe[q]
            rec(name, pop, q + '.point', fd['point'], me[q]['sum']['point'], 'A', (q, 'sum', 'point'))
            rec(name, pop, q + '.R_pp', fd['R_pp'], me[q]['pp']['point'], 'A', (q, 'pp', 'point'))
            rec(name, pop, q + '.dec_eq', fd['dec_eq'], me[q]['deceq']['point'], 'A', (q, 'deceq', 'point'))
            if 'ci' in fd:
                rec(name, pop, q + '.share_le0', fd['share_le0'], me['share_%s_le0' % q], 'A', ('share_%s_le0' % q,))
                rec(name, pop, q + '.n_le0', fd['n_le0'], me['n_%s_le0' % q], 'B')
                rec_pair(name, pop, q + '.ci', fd['ci'], me[q]['sum']['ci'], 'A', (q, 'sum', 'ci'))
                rec_pair(name, pop, q + '.R_pp_ci', fd['R_pp_ci'], me[q]['pp']['ci'], 'A', (q, 'pp', 'ci'))
                rec_pair(name, pop, q + '.dec_eq_ci', fd['dec_eq_ci'], me[q]['deceq']['ci'], 'A', (q, 'deceq', 'ci'))
            extra = set(fd) - {'point', 'R_pp', 'dec_eq', 'share_le0', 'n_le0', 'ci', 'R_pp_ci', 'dec_eq_ci'}
            if extra:
                raise RuntimeError('unexpected keys in %s %s %s: %s' % (name, fpop, q, extra))
        cmp_summ(name, pop, 'denE_over_3s', fe['denE_over_3s'], me['rel']['3s_commitment']['denE'], ('rel', '3s_commitment', 'denE'))
        cmp_summ(name, pop, 'den0_over_3s', fe['den0_over_3s'], me['rel']['3s_commitment']['den0'], ('rel', '3s_commitment', 'den0'))
        cmp_summ(name, pop, 'E_rr0', fe['E_rr0'], me['RR0_E'], ('RR0_E',))
        for fa, fent in fe['arms'].items():
            a = ARMMAP[fa]; ms = me['src'][a]
            rec(name, pop, 'arms.%s.D' % fa, fent['D'], ms['D_sum']['point'], 'A', ('src', a, 'D_sum', 'point'))
            rec(name, pop, 'arms.%s.D_pp' % fa, fent['D_pp'], ms['D_pp']['point'], 'A', ('src', a, 'D_pp', 'point'))
            rec(name, pop, 'arms.%s.D_dec_eq' % fa, fent['D_dec_eq'], ms['D_deceq']['point'], 'A', ('src', a, 'D_deceq', 'point'))
            if 'D_dec_eq_ci' in fent:
                rec_pair(name, pop, 'arms.%s.D_dec_eq_ci' % fa, fent['D_dec_eq_ci'], ms['D_deceq']['ci'], 'A', ('src', a, 'D_deceq', 'ci'))
            cmp_summ(name, pop, 'arms.%s.rr0' % fa, fent['rr0'], ms['RR0'], ('src', a, 'RR0'))
            cmp_summ(name, pop, 'arms.%s.rrE' % fa, fent['rrE'], ms['RR'], ('src', a, 'RR'))
            if 'branch' in fent:
                rec(name, pop, 'arms.%s.branch' % fa, fent['branch'], branch_num(my_summ(ms['RR0']), me['den0']['deceq']['point']), 'C')
            extra = set(fent) - {'D', 'D_pp', 'D_dec_eq', 'D_dec_eq_ci', 'rr0', 'rrE', 'branch'}
            if extra:
                raise RuntimeError('unexpected keys in %s %s arm %s: %s' % (name, fpop, fa, extra))
    for fpop, fo in fsc['oracle_diag'].items():
        pop = POPMAP[fpop]; me = msc['pops'][pop]; pi = ['all', 'moving', 'phase0', 'phase1', 'phase2'].index(pop)
        rec(name, pop, 'oracle_diag.F0_g0_caution_pp', fo['F0_g0_caution_pp'], me['F0_zero_margin']['caution_pct'], 'B')
        rec(name, pop, 'oracle_diag.O_caution_pp', fo['O_caution_pp'], me['O_point']['caution_pct'], 'B')
        rec(name, pop, 'oracle_diag.no_safe_row_wrong_go_pp', fo['no_safe_row_wrong_go_pp'], me['O_point']['wrong_go_pct'], 'B')
        fmin, fmax, fnan = o_frontier(name, pi)
        rec(name, pop, 'oracle_diag.O_front_min', fo['O_front_min'], fmin, 'C')
        rec(name, pop, 'oracle_diag.O_front_max', fo['O_front_max'], fmax, 'C')
        rec(name, pop, 'oracle_diag.O_front_n_nan', fo['O_front_n_nan'], fnan, 'C')
        extra = set(fo) - {'F0_g0_caution_pp', 'O_caution_pp', 'no_safe_row_wrong_go_pp', 'O_front_min', 'O_front_max', 'O_front_n_nan'}
        if extra:
            raise RuntimeError('unexpected keys in oracle_diag %s %s: %s' % (name, fpop, extra))

# ------------------------------------------------------------------------------------------------ pair counts
PCMAP = dict(pairs=('pairs', 'A'), unsafe_as_scored=('pairs_unsafe_window', 'A'), unsafe_est=('pairs_unsafe_est', 'A'),
             late_safe_as_scored=('pairs_late_safe_window', 'A'), late_safe_now_unsafe=('pairs_late_safe_window_unsafe_est', 'A'),
             censored_safe_as_scored=('pairs_cens_safe_window', 'A'), censored_safe_est=('pairs_cens_safe_window_safe_est', 'A'),
             unsafe_W1=('pairs_unsafe_3s_commitment', 'B'), decisions_no_safe_row_est=('decisions_without_safe_row_est', 'A'))
for key, fc in FIRST['pair_counts'].items():
    for fk, v in fc.items():
        mk, cls = PCMAP[fk]
        rec('pair_counts', key, fk, v, MINE['counts'][key][mk], cls, (mk,))
for k in ('seconds',):
    not_compared.append(dict(path=k, n_entries=1, reason='run time of the first program'))
for k in ('code', 'status', 'written', 'common_sha256'):
    not_compared.append(dict(path=k, n_entries=0, reason='text, not a number'))


# ------------------------------------------------------------------------------------------------ own class-A leaves without counterpart
def own_A_leaves(name):
    out = []
    for pop in ('all', 'moving', 'phase0', 'phase1', 'phase2', 'phase_weighted'):
        out.append((name, pop, 'n'))
        for q in ('den0', 'denE'):
            for form in ('sum', 'pp', 'deceq'):
                out += [(name, pop, q, form, 'point'), (name, pop, q, form, 'ci', 0), (name, pop, q, form, 'ci', 1)]
            out.append((name, pop, 'share_%s_le0' % q))
            out += [(name, pop, 'rel', '3s_commitment', q, 'point'), (name, pop, 'rel', '3s_commitment', q, 'ci', 0), (name, pop, 'rel', '3s_commitment', q, 'ci', 1)]
        for a in SRC:
            for form in ('D_sum', 'D_pp', 'D_deceq', 'RR0', 'RR'):
                out += [(name, pop, 'src', a, form, 'point'), (name, pop, 'src', a, form, 'ci', 0), (name, pop, 'src', a, form, 'ci', 1)]
        out += [(name, pop, 'RR0_E', 'point'), (name, pop, 'RR0_E', 'ci', 0), (name, pop, 'RR0_E', 'ci', 1)]
    return out


def leaf_group(path):
    """A readable group for an own leaf without counterpart."""
    p = path[2:]
    kind = 'interval' if 'ci' in p else ('share' if str(p[0]).startswith('share_') else 'point')
    if p[0] == 'src':
        what = 'source %s: %s' % (p[1], p[2])
    elif p[0] == 'rel':
        what = '%s relative to 3 s' % p[2]
    elif p[0] in ('den0', 'denE'):
        what = '%s (%s)' % (p[0], p[1])
    else:
        what = str(p[0])
    return '%s, %s' % (what, kind)


own_missing = {}
own_total = {}
for name in MINE['on_brief']:
    leaves = own_A_leaves(name)
    own_total[name] = len(leaves)
    miss = [l for l in leaves if l not in matched]
    g = {}
    for l in miss:
        g.setdefault(leaf_group(l), 0)
        g[leaf_group(l)] += 1
    own_missing[name] = dict(n_on_brief=len(leaves), n_with_counterpart=len(leaves) - len(miss), n_without_counterpart=len(miss), groups=g)
own_counts_total = 9 * 8

# ------------------------------------------------------------------------------------------------ summary
def tally(rs):
    return dict(compared=len(rs), differ=sum(r['status'] == 'DIFFER' for r in rs), undefined_in_both=sum(r['status'] == 'undefined in both' for r in rs),
                flags=sum(r['kind'] == 'flag' for r in rs),
                max_abs_diff=max([r['abs_diff'] for r in rs if r['abs_diff'] is not None], default=0.0))


fams = ['est', 'cens', 'est_signed', 'asscored', 'pair_counts']
summary = dict(by_family={}, by_scoring={}, by_class={})
for f in fams:
    rs = [r for r in records if r['family'] == f]
    summary['by_family'][f] = dict(all=tally(rs), **{c: tally([r for r in rs if r['cls'] == c]) for c in 'ABC'})
for s in list(MINE['scorings']) + ['pair_counts']:
    rs = [r for r in records if r['scoring'] == s]
    if rs:
        summary['by_scoring'][s] = dict(all=tally(rs), **{c: tally([r for r in rs if r['cls'] == c]) for c in 'ABC'})
for c in 'ABC':
    summary['by_class'][c] = tally([r for r in records if r['cls'] == c])
summary['total'] = tally(records)
diffs = [r for r in records if r['status'] == 'DIFFER']
if NEG:
    neg = dict(what='negative control: own blocks est_t0p75_a6p0 and cens_t0p75_a6p0 swapped, pair counts of t1p00 and t1p25 swapped',
               total=summary['total'], by_scoring={s: v['all'] for s, v in summary['by_scoring'].items() if v['all']['differ']},
               by_class={c: summary['by_class'][c] for c in 'ABC'})
    (HERE / 'r4_compare_negctl_v01_out.json').write_text(json.dumps(neg, indent=1), encoding='utf-8')
    print('NEGATIVE CONTROL: compared %d, differ %d' % (summary['total']['compared'], summary['total']['differ']))
    for s_, v in neg['by_scoring'].items():
        print('   %-24s compared %d differ %d' % (s_, v['compared'], v['differ']))
    sys.exit(0)
out = dict(written=time.strftime('%Y-%m-%d %H:%M:%S'), tolerance=TOL,
           first_program_file=str(FIRST_PATH), first_program_sha256=sha_first, first_program_written=FIRST.get('written'),
           second_program_file=str(MINE_PATH), second_program_sha256=sha_mine,
           summary=summary, differences=diffs, not_compared=not_compared,
           own_brief_numbers_without_counterpart=own_missing, records=records)
(HERE / 'RECOUNT4_COMPARE_v01.json').write_text(json.dumps(out, indent=1), encoding='utf-8')

# ------------------------------------------------------------------------------------------------ markdown
L = []
L.append('# Recount4: comparison with the first program')
L.append('')
L.append('Written %s by `r4_compare_v01.py`.' % out['written'])
L.append('')
L.append('- First program: `revision_v11\\analysis\\out\\REV_E2_EXTENDED_TRUTH_v01.json` (written %s, sha256 `%s`).' % (FIRST.get('written'), sha_first))
L.append('- Second program: `RECOUNT4_RESULTS_v01.json` (sha256 `%s`, unchanged since it was recorded before the first file was opened).' % sha_mine)
L.append('- Tolerance: absolute difference 1e-9. An entry that is undefined (no ratio) in both programs counts as compared and not differing.')
L.append('')
t = summary['total']
L.append('## Result')
L.append('')
L.append('**%d numbers compared, %d differ by more than 1e-9.** Largest absolute difference: %.3g. Of the %d comparisons, %d are "undefined in both programs" and %d are yes/no flags.' % (
    t['compared'], t['differ'], t['max_abs_diff'], t['compared'], t['undefined_in_both'], t['flags']))
L.append('')
L.append('Classes: A = on the brief\'s list, from the results file as it stood before the first program\'s file was opened; B = not on the list, in that results file or following from it by arithmetic (resamples left out, the flag "point outside its interval", the basic interval, the point of the perfect oracle, the flag signed caution, the 3 s commitment\'s unsafe pairs); C = recomputed after the first program\'s file and script were opened (minimum, maximum and undefined levels of the perfect oracle\'s frontier; the first program\'s branch number, by its rule applied to the second program\'s numbers).')
L.append('')
L.append('| Scoring family | Compared | Differ | A: compared / differ | B: compared / differ | C: compared / differ | Largest absolute difference |')
L.append('|---|---|---|---|---|---|---|')
names = dict(est='est (9 settings)', cens='cens (6 settings)', est_signed='est_signed (0.75 s, 6 m/s2)', asscored='asscored (0.75 s, 6 m/s2)', pair_counts='pair counts (9 settings)')
for f in fams:
    s = summary['by_family'][f]
    L.append('| %s | %d | %d | %d / %d | %d / %d | %d / %d | %.3g |' % (names[f], s['all']['compared'], s['all']['differ'], s['A']['compared'], s['A']['differ'],
                                                                 s['B']['compared'], s['B']['differ'], s['C']['compared'], s['C']['differ'], s['all']['max_abs_diff']))
L.append('| **Total** | **%d** | **%d** | %d / %d | %d / %d | %d / %d | %.3g |' % (t['compared'], t['differ'], summary['by_class']['A']['compared'], summary['by_class']['A']['differ'],
                                                                          summary['by_class']['B']['compared'], summary['by_class']['B']['differ'],
                                                                          summary['by_class']['C']['compared'], summary['by_class']['C']['differ'], t['max_abs_diff']))
L.append('')
L.append('## Per scoring')
L.append('')
L.append('| Scoring | Compared | Differ | A: compared / differ | B | C | Undefined in both | Largest absolute difference |')
L.append('|---|---|---|---|---|---|---|---|')
for s, v in summary['by_scoring'].items():
    L.append('| `%s` | %d | %d | %d / %d | %d / %d | %d / %d | %d | %.3g |' % (s, v['all']['compared'], v['all']['differ'], v['A']['compared'], v['A']['differ'],
                                                                          v['B']['compared'], v['B']['differ'], v['C']['compared'], v['C']['differ'],
                                                                          v['all']['undefined_in_both'], v['all']['max_abs_diff']))
L.append('')
L.append('## Differences')
L.append('')
if not diffs:
    L.append('None above 1e-9.')
else:
    L.append('| Scoring | Population | Entry | Class | First program | Second program | Absolute difference |')
    L.append('|---|---|---|---|---|---|---|')
    for r in diffs:
        L.append('| `%s` | %s | `%s` | %s | %r | %r | %s |' % (r['scoring'], r['pop'], r['entry'], r['cls'], r['first'], r['second'],
                                                           '%.3g' % r['abs_diff'] if r['abs_diff'] is not None else 'n/a'))
L.append('')
L.append('## Entries of the first program\'s file that were not compared')
L.append('')
L.append('| Entry | Numeric entries | Reason |')
L.append('|---|---|---|')
for e in not_compared:
    L.append('| `%s` | %d | %s |' % (e['path'], e['n_entries'], e['reason']))
L.append('')
L.append('Every other numeric entry of the file (scorings `est_*`, `cens_*`, `est_signed_*`, `asscored_*`, their `oracle_diag` blocks, and `pair_counts`) was compared.')
L.append('')
L.append('## Numbers on the brief\'s list for which the first program\'s file has no counterpart')
L.append('')
L.append('The second program computed every number the brief lists. The first program did not bootstrap every scoring and did not score every source in every scoring, so these numbers of the second program stand alone (they are checked only by the self-check `r4_naive_v01.py`).')
L.append('')
L.append('| Scoring | On the brief\'s list | With counterpart | Without | What is without counterpart |')
L.append('|---|---|---|---|---|')
tot_on = tot_with = 0
for name, v in own_missing.items():
    g = v['groups']
    # condense: kinds
    kinds = {}
    for k, c in g.items():
        kk = k.split(', ')[-1]
        kinds[kk] = kinds.get(kk, 0) + c
    desc = '; '.join('%s: %d' % (k, c) for k, c in sorted(kinds.items())) if kinds else '-'
    L.append('| `%s` | %d | %d | %d | %s |' % (name, v['n_on_brief'], v['n_with_counterpart'], v['n_without_counterpart'], desc))
    tot_on += v['n_on_brief']; tot_with += v['n_with_counterpart']
nA_pc = sum(1 for r in records if r['scoring'] == 'pair_counts' and r['cls'] == 'A')
L.append('| pair counts | %d | %d | %d | - |' % (own_counts_total, nA_pc, own_counts_total - nA_pc))
L.append('| **Total** | **%d** | **%d** | **%d** | |' % (tot_on + own_counts_total, tot_with + nA_pc, tot_on + own_counts_total - tot_with - nA_pc))
L.append('')
L.append('Detail per scoring (groups of entries without counterpart) is in `RECOUNT4_COMPARE_v01.json`, key `own_brief_numbers_without_counterpart`.')
L.append('')
(HERE / 'RECOUNT4_COMPARE_v01.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print('compared %d, differ %d, undefined in both %d, flags %d, max abs diff %.3g' % (t['compared'], t['differ'], t['undefined_in_both'], t['flags'], t['max_abs_diff']))
for f in fams:
    s = summary['by_family'][f]
    print('  %-12s compared %5d differ %3d | A %5d / %d | B %5d / %d | C %5d / %d' % (f, s['all']['compared'], s['all']['differ'], s['A']['compared'], s['A']['differ'],
                                                                                  s['B']['compared'], s['B']['differ'], s['C']['compared'], s['C']['differ']))
print('own brief numbers: %d, with counterpart %d' % (tot_on + own_counts_total, tot_with + nA_pc))
for r in diffs[:60]:
    print('  DIFF', r['scoring'], r['pop'], r['entry'], r['cls'], r['first'], r['second'], r['abs_diff'])
